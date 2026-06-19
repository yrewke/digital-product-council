#!/usr/bin/env python3
"""Codex Council V2 deterministic workflow engine.

Python owns state, validation, cache lookup, locks, packet routing, veto scope,
and resume. Codex owns the reasoning text that is submitted into this engine.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
RUNS = ROOT / "runs"
EXECUTIVES = ["contrarian", "first-principles", "expansionist", "outsider", "executor"]
SERVICES = ["librarian", "auditor", "chairman", "devils-advocate"]

STAGES = [
    "CHARTER_DRAFTED",
    "CHARTER_APPROVED",
    "EVIDENCE_REQUESTS_OPEN",
    "EVIDENCE_READY",
    "MEMOS_DRAFTING",
    "MEMOS_SUBMITTED",
    "AUDIT_IN_PROGRESS",
    "AUDIT_BLOCKED",
    "AUDIT_PASSED",
    "PEER_REVIEW_IN_PROGRESS",
    "AUTHOR_REVISION",
    "PRE_CHAIR_READY",
    "CHAIRMAN_SYNTHESIS",
    "DEVILS_ADVOCATE_COMPLETE",
    "PROVISIONAL_VERDICT",
    "POST_CHAIR_VETO_REVIEW",
    "FINAL_VERDICT_COMPLETE",
    "RUN_COMPLETE",
]

LEGAL_TRANSITIONS = {
    "CHARTER_DRAFTED": ["CHARTER_APPROVED"],
    "CHARTER_APPROVED": ["EVIDENCE_REQUESTS_OPEN"],
    "EVIDENCE_REQUESTS_OPEN": ["EVIDENCE_READY"],
    "EVIDENCE_READY": ["MEMOS_DRAFTING"],
    "MEMOS_DRAFTING": ["MEMOS_SUBMITTED"],
    "MEMOS_SUBMITTED": ["AUDIT_IN_PROGRESS"],
    "AUDIT_IN_PROGRESS": ["AUDIT_BLOCKED", "AUDIT_PASSED"],
    "AUDIT_BLOCKED": ["AUDIT_IN_PROGRESS"],
    "AUDIT_PASSED": ["PEER_REVIEW_IN_PROGRESS"],
    "PEER_REVIEW_IN_PROGRESS": ["AUTHOR_REVISION"],
    "AUTHOR_REVISION": ["PRE_CHAIR_READY"],
    "PRE_CHAIR_READY": ["CHAIRMAN_SYNTHESIS"],
    "CHAIRMAN_SYNTHESIS": ["DEVILS_ADVOCATE_COMPLETE"],
    "DEVILS_ADVOCATE_COMPLETE": ["PROVISIONAL_VERDICT"],
    "PROVISIONAL_VERDICT": ["POST_CHAIR_VETO_REVIEW"],
    "POST_CHAIR_VETO_REVIEW": ["FINAL_VERDICT_COMPLETE"],
    "FINAL_VERDICT_COMPLETE": ["RUN_COMPLETE"],
}

EVENT_KEYWORDS = {
    "EVIDENCE_REQUEST": r"ER-[0-9]{4}",
    "EVIDENCE_RESPONSE": r"EV-[0-9]{4}",
    "FACT_CHECK": r"FC-[0-9]{4}",
    "PEER_REVIEW": r"PR-[0-9]{4}",
    "OBJECTION": r"OBJ-[0-9]{4}",
    "AUTHOR_RESPONSE": r"AR-[0-9]{4}",
    "VETO": r"V-[0-9]{4}",
    "REVISION": r"R[0-9]+",
    "RESOLVED": r"RESOLVED",
    "UNRESOLVED": r"UNRESOLVED",
}

OLD_SYSTEM_PATHS = [
    ".agents/skills/restaurant-commercial-council/SKILL.md",
    ".agents/skills/restaurant-research-librarian/SKILL.md",
    ".codex/agents/chairman.toml",
    "working/council-runs/2026-06-14-pricing-and-commercial-justification-002C/RUN_STATUS.md",
]

REQUIRED_V2_AGENT_NAMES = [
    "contrarian",
    "first-principles",
    "expansionist",
    "outsider",
    "executor",
    "librarian",
    "auditor",
    "devils-advocate",
    "chairman",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def today() -> str:
    return date.today().isoformat()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path, default: Any) -> Any:
    return json.loads(read(path)) if path.exists() else default


def save_json(path: Path, data: Any) -> None:
    write(path, json.dumps(data, indent=2, sort_keys=True))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def normalize_question(question: str) -> str:
    words = re.findall(r"[a-z0-9]+", question.lower())
    stop = {"what", "is", "the", "a", "an", "of", "for", "to", "does", "do"}
    return "-".join(w for w in words if w not in stop)


def run_dir_arg(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else REPO / path


def durable_relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def stored_path(root: Path, value: str) -> Path:
    return root / Path(value.replace("\\", "/"))


@contextmanager
def file_lock(run_dir: Path, name: str):
    lock = run_dir / "_work" / "locks" / f"{name}.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    if lock.exists() and "ACTIVE" in read(lock):
        raise SystemExit(f"Lock already exists: {lock}")
    write(lock, f"ACTIVE {now()}")
    try:
        yield
    finally:
        if lock.exists():
            write(lock, f"RELEASED {now()}")


def status_path(run_dir: Path) -> Path:
    return run_dir / "RUN_STATUS.json"


def status(run_dir: Path) -> dict[str, Any]:
    return load_json(status_path(run_dir), {})


def update_status(run_dir: Path, **updates: Any) -> None:
    data = status(run_dir)
    data.update(updates)
    data["updated"] = now()
    save_json(status_path(run_dir), data)


def event(run_dir: Path, kind: str, payload: dict[str, Any]) -> None:
    record = {"time": now(), "kind": kind, **payload}
    append(run_dir / "RUN_EVENTS.jsonl", json.dumps(record, sort_keys=True) + "\n")


def transition(run_dir: Path, target: str, reason: str) -> None:
    current = status(run_dir).get("stage")
    if current == target:
        return
    if target not in LEGAL_TRANSITIONS.get(current, []):
        raise SystemExit(f"Illegal transition: {current} -> {target}")
    update_status(run_dir, stage=target, last_valid_stage=target)
    event(run_dir, "STAGE_TRANSITION", {"from": current, "to": target, "reason": reason})


def next_id(records: list[dict[str, Any]], key: str, prefix: str) -> str:
    nums = []
    for record in records:
        value = str(record.get(key, ""))
        if value.startswith(prefix + "-"):
            try:
                nums.append(int(value.split("-")[1]))
            except ValueError:
                pass
    return f"{prefix}-{(max(nums) if nums else 0) + 1:04d}"


def current_memo(text: str) -> str:
    match = re.search(r"# CURRENT_MEMO\n(.*?)(?=\n# EVIDENCE_REQUESTS|\Z)", text, re.S)
    return match.group(1) if match else text


def section_text(text: str, section: str) -> str:
    if section == "CURRENT_MEMO":
        return current_memo(text)
    pattern = rf"{re.escape(section)}\n(.*?)(?=\n# [A-Z_]+|\Z)"
    match = re.search(pattern, text, re.S)
    return match.group(1) if match else text


def artifact_text(run_dir: Path, artifact: str, section: str | None = None) -> str:
    if artifact.startswith("memos/"):
        path = run_dir / artifact
    else:
        path = run_dir / artifact
    if not path.exists():
        return ""
    text = read(path)
    return section_text(text, section) if section else text


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = rf"({re.escape(heading)}\n)(.*?)(?=\n# [A-Z_]+|\Z)"
    if re.search(pattern, text, re.S):
        return re.sub(pattern, rf"\1{body.rstrip()}\n", text, flags=re.S)
    return text.rstrip() + f"\n\n{heading}\n{body.rstrip()}\n"


def append_section(path: Path, heading: str, block: str) -> None:
    text = read(path)
    section = re.search(rf"{re.escape(heading)}\n(.*?)(?=\n# [A-Z_]+|\Z)", text, re.S)
    current = section.group(1).rstrip() + "\n\n" if section and section.group(1).strip() else ""
    write(path, replace_section(text, heading, current + block.strip() + "\n"))


def record_old_hashes(run_dir: Path) -> None:
    manifest = {}
    for rel in OLD_SYSTEM_PATHS:
        path = REPO / rel
        manifest[rel] = sha256(path) if path.exists() else None
    save_json(run_dir / "_work" / "old-system-hashes-before.json", manifest)


def verify_old_hashes(run_dir: Path) -> list[str]:
    before = load_json(run_dir / "_work" / "old-system-hashes-before.json", {})
    failures = []
    for rel, expected in before.items():
        path = REPO / rel
        actual = sha256(path) if path.exists() else None
        if actual != expected:
            failures.append(f"Old-system hash changed: {rel}")
    save_json(run_dir / "_work" / "old-system-hashes-after.json", {rel: (sha256(REPO / rel) if (REPO / rel).exists() else None) for rel in before})
    return failures


def release_tree_failures(root: Path = REPO) -> list[str]:
    failures: list[str] = []
    debris = [p for p in root.rglob("_test-tmp") if p.is_dir()]
    for path in debris:
        failures.append(f"Release tree contains test temporary directory: {path}")
    if not (root / ".agents" / "skills" / "codex-council-v2" / "SKILL.md").exists():
        failures.append("Missing .agents/skills/codex-council-v2/SKILL.md")
    for name in REQUIRED_V2_AGENT_NAMES:
        if not (root / ".codex" / "agents" / f"codex-council-v2-{name}.toml").exists():
            failures.append(f"Missing .codex/agents/codex-council-v2-{name}.toml")
    return failures


def validate_release_tree(args: argparse.Namespace) -> None:
    root = run_dir_arg(args.root)
    failures = release_tree_failures(root)
    if failures:
        raise SystemExit("Release tree validation failed:\n- " + "\n- ".join(failures))
    print(f"PASS release tree {root}")


def default_config(run_id: str, title: str, question: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "title": title,
        "question": question,
        "decision_status_map": {},
        "role_briefs": {
            "contrarian": "Find how the proposal fails and what evidence would defeat each objection.",
            "first-principles": "Decompose the decision into load-bearing claims and rebuild from constraints.",
            "expansionist": "Identify upside and reusable leverage without pricing speculation as fact.",
            "outsider": "Compare against doing nothing and low-cost substitutes from buyer perspective.",
            "executor": "Map dependencies, ownership, support burden, failure criteria, and next action.",
        },
        "model_routing": {
            "economy": "manual fallback in current Codex session; use for metadata and validation",
            "standard": "manual fallback in current Codex session; use for ordinary memos and reviews",
            "frontier": "active Codex model from doctor output when available; reserve for Chairman and hard contradictions",
            "verified_environment": "Codex Doctor observed model gpt-5.5 on this workstation; per-agent model keys are not guaranteed by local TOML support.",
        },
        "veto_assignments": {
            "executor": [
                {"stage": "PRE_CHAIR", "protected_domain": "feasible next action"},
                {"stage": "POST_CHAIR", "protected_domain": "feasible next action"},
            ],
            "contrarian": [
                {"stage": "PRE_CHAIR", "protected_domain": "unbounded downside claims"}
            ],
            "auditor": [
                {"stage": "ANY", "protected_domain": "factual and numerical validity"}
            ],
        },
        "pre_chair_revision_cycles_allowed": 1,
        "post_chair_revision_cycles_allowed": 1,
    }


def render_charter(config: dict[str, Any]) -> str:
    briefs = "\n".join(f"### {role.title()}\n{brief}\n" for role, brief in config["role_briefs"].items())
    veto_json = json.dumps(config["veto_assignments"], indent=2, sort_keys=True)
    return f"""# Run Charter

## Run ID

{config['run_id']}

## Title

{config['title']}

## Central Question

{config['question']}

## Decision-Status Map

{json.dumps(config['decision_status_map'], indent=2, sort_keys=True)}

## Role-Specific Starting Briefs

{briefs}
## Model-Routing Plan

{json.dumps(config['model_routing'], indent=2, sort_keys=True)}

## Machine-Readable Veto Assignments

```json
{veto_json}
```

## Stop Conditions

Stop on unresolved blocking fact checks, malformed tags, missing final verdict, illegal stage transition, failed old-system hash preservation, or skipped authorized veto holder.
"""


def init_run(args: argparse.Namespace) -> Path:
    run_dir = RUNS / args.run_id
    if run_dir.exists():
        if not args.force:
            raise SystemExit(f"Run already exists: {run_dir}")
        shutil.rmtree(run_dir)
    for sub in ["memos", "evidence", "reviews", "_work/locks", "_work/review-packets", "_work/merge-queue"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    config = default_config(args.run_id, args.title, args.question)
    save_json(run_dir / "RUN_CONFIG.json", config)
    write(run_dir / "RUN_CHARTER.md", render_charter(config))
    save_json(status_path(run_dir), {
        "run_id": args.run_id,
        "stage": "CHARTER_DRAFTED",
        "last_valid_stage": "CHARTER_DRAFTED",
        "updated": now(),
        "retry_policy": {"default_retries": 1},
        "quorum": {"executives_required": 5, "degraded_mode": "human_approval_required"},
        "pending_tasks": ["validate-charter"],
    })
    for executive in EXECUTIVES:
        memo = read(ROOT / "templates" / "executive-memo.md")
        memo = memo.replace("run_id:", f"run_id: {args.run_id}")
        memo = memo.replace("executive:", f"executive: {executive}")
        memo = memo.replace("last_updated:", f"last_updated: {today()}")
        write(run_dir / "memos" / f"{executive}.md", memo)
    save_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {"sources": [], "evidence": [], "requests": [], "contradictions": []})
    write(run_dir / "evidence" / "SOURCE_LEDGER.csv", "source_id,title,classification,geography,publication_date,retrieval_date,limitations\n")
    write(run_dir / "RUN_EVENTS.jsonl", "")
    record_old_hashes(run_dir)
    event(run_dir, "RUN_INITIALIZED", {"run_id": args.run_id})
    return run_dir


def validate_charter(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    config = load_json(run_dir / "RUN_CONFIG.json", {})
    failures = []
    for role in EXECUTIVES:
        if not config.get("role_briefs", {}).get(role):
            failures.append(f"Missing role brief: {role}")
    if not config.get("veto_assignments"):
        failures.append("Missing machine-readable veto assignments")
    if failures:
        raise SystemExit("Charter validation failed:\n- " + "\n- ".join(failures))
    transition(run_dir, "CHARTER_APPROVED", "charter validated")
    update_status(run_dir, pending_tasks=["open-evidence-requests"])
    print(f"PASS charter {run_dir}")


def open_evidence_requests(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    transition(run_dir, "EVIDENCE_REQUESTS_OPEN", "evidence request window opened")
    update_status(run_dir, pending_tasks=["register-evidence-request"])
    print(f"OPEN evidence requests {run_dir}")


def register_evidence_request_record(run_dir: Path, requester: str, question: str, decision: str, geography: str, freshness_days: int, acceptable_type: str, scope: str = "synthetic") -> dict[str, Any]:
    with file_lock(run_dir, "evidence-library"):
        lib = load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {"sources": [], "evidence": [], "requests": [], "contradictions": []})
        cache_key = normalize_question(question)
        request_id = next_id(lib["requests"], "request_id", "ER")
        reusable = None
        for ev in lib["evidence"]:
            compatible_geo = ev.get("geography", geography) in {geography, "GLOBAL", "SYNTHETIC"}
            fresh = ev.get("freshness_days", freshness_days) <= freshness_days
            no_block = not ev.get("blocked_by_contradiction")
            if ev.get("cache_key") == cache_key and compatible_geo and fresh and no_block:
                reusable = ev
                break
        record = {
            "request_id": request_id,
            "requester": requester,
            "question": question,
            "normalized_question": normalize_question(question),
            "cache_key": cache_key,
            "decision_affected": decision,
            "scope": scope,
            "geography": geography,
            "freshness_days": freshness_days,
            "acceptable_evidence_type": acceptable_type,
            "status": "ANSWERED_FROM_CACHE" if reusable else "OPEN",
            "response_id": reusable.get("evidence_id") if reusable else None,
            "answer_source": "cache" if reusable else None,
        }
        lib["requests"].append(record)
        save_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", lib)
    event(run_dir, "EVIDENCE_REQUEST_REGISTERED", record)
    return record


def register_evidence_request(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    record = register_evidence_request_record(run_dir, args.requester, args.question, args.decision, args.geography, args.freshness_days, args.acceptable_type, args.scope)
    print(json.dumps(record, indent=2, sort_keys=True))


def resolve_evidence_request_record(run_dir: Path, request_id: str, claim: str, classification: str, source_title: str, geography: str = "SYNTHETIC", limitations: str = "fixture") -> dict[str, Any]:
    with file_lock(run_dir, "evidence-library"):
        lib = load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {"sources": [], "evidence": [], "requests": [], "contradictions": []})
        request = next((r for r in lib["requests"] if r["request_id"] == request_id), None)
        if not request:
            raise SystemExit(f"Unknown request: {request_id}")
        source_id = next_id(lib["sources"], "source_id", "SRC")
        evidence_id = next_id(lib["evidence"], "evidence_id", "EV")
        source = {"source_id": source_id, "title": source_title, "classification": classification, "geography": geography, "retrieval_date": today(), "limitations": limitations}
        evidence = {
            "evidence_id": evidence_id,
            "request_id": request_id,
            "cache_key": request["cache_key"],
            "claim": claim,
            "classification": classification,
            "source_id": source_id,
            "geography": geography,
            "freshness_days": request["freshness_days"],
            "answer_source": "user-supplied fact" if limitations == "fixture" else "local source",
        }
        lib["sources"].append(source)
        lib["evidence"].append(evidence)
        request.update({"status": "ANSWERED", "response_id": evidence_id, "answer_source": evidence["answer_source"]})
        save_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", lib)
        append(run_dir / "evidence" / "SOURCE_LEDGER.csv", f"{source_id},{source_title},{classification},{geography},,{today()},{limitations}\n")
    event(run_dir, "EVIDENCE_REQUEST_RESOLVED", evidence)
    return evidence


def resolve_evidence_request(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    evidence = resolve_evidence_request_record(run_dir, args.request_id, args.claim, args.classification, args.source_title, args.geography, args.limitations)
    print(json.dumps(evidence, indent=2, sort_keys=True))


def mark_evidence_ready(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    lib = load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {})
    open_requests = [r["request_id"] for r in lib.get("requests", []) if r.get("status") == "OPEN"]
    if open_requests:
        raise SystemExit(f"Open evidence requests remain: {', '.join(open_requests)}")
    transition(run_dir, "EVIDENCE_READY", "all registered evidence requests answered or reused")
    update_status(run_dir, pending_tasks=["submit-memo"])
    print(f"READY evidence {run_dir}")


def memo_text(run_id: str, executive: str, position: str, reasoning: str, economic: str, evidence_ids: list[str], revision: str = "R1", gate: str = "PENDING") -> str:
    evidence_lines = "\n".join(f"- [EVIDENCE_RESPONSE:{eid}] Synthetic evidence used." for eid in evidence_ids)
    return f"""---
run_id: {run_id}
executive: {executive}
memo_status: READY
revision: {revision}
last_updated: {today()}
evidence_gate: {gate}
active_vetoes: []
---

# CURRENT_MEMO

## Assigned Question
Synthetic fixture decision.

## Position
{position}

## Reasoning
{reasoning}

## Evidence Used
{evidence_lines}

## Assumptions
- Synthetic facts are fixtures, not real market evidence.

## Risks
- Fixture evidence could fail outside the test.

## Economic Consequences
{economic}

## What Would Change This Position
Different support budget or failure threshold evidence.

## Recommendation
Choose the bounded pilot with explicit failure criteria.

# EVIDENCE_REQUESTS

# FACT_CHECK

# PEER_REVIEW

# AUTHOR_RESPONSES

# VETOES

# REVISION_LOG

## [REVISION:{revision}]
Summary: Memo submitted through workflow engine.
Reason: Stage-controlled submission.
Resolved IDs:
Remaining disagreement: bounded upside value.
"""


def submit_memo_record(run_dir: Path, executive: str, content: str) -> None:
    if executive not in EXECUTIVES:
        raise SystemExit(f"Unknown executive: {executive}")
    with file_lock(run_dir, f"memo-{executive}"):
        write(run_dir / "memos" / f"{executive}.md", content)
    event(run_dir, "MEMO_SUBMITTED", {"executive": executive})
    current_stage = status(run_dir)["stage"]
    if current_stage == "EVIDENCE_READY":
        transition(run_dir, "MEMOS_DRAFTING", "first memo submitted")
    memos = [(run_dir / "memos" / f"{e}.md").exists() and "memo_status: READY" in read(run_dir / "memos" / f"{e}.md") for e in EXECUTIVES]
    if all(memos) and status(run_dir)["stage"] == "MEMOS_DRAFTING":
        transition(run_dir, "MEMOS_SUBMITTED", "all five memos submitted")
        update_status(run_dir, pending_tasks=["extract-claims"])


def submit_memo(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    content = read(Path(args.content_file)) if args.content_file else sys.stdin.read()
    submit_memo_record(run_dir, args.executive, content)
    print(f"SUBMITTED memo {args.executive}")


def split_claim_sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text)
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]


def detect_claim_values(sentence: str) -> tuple[list[str], dict[str, Any]]:
    types: list[str] = []
    values: dict[str, Any] = {}
    money = re.findall(r"\b(?:AED|USD|EUR|GBP)\s*[0-9][0-9,]*(?:\.[0-9]+)?|\b[0-9][0-9,]*(?:\.[0-9]+)?\s*(?:AED|USD|EUR|GBP)\b", sentence, re.I)
    percentages = re.findall(r"\b[0-9]+(?:\.[0-9]+)?\s*%", sentence)
    dates = re.findall(r"\b(?:20[0-9]{2}-[0-9]{2}-[0-9]{2}|20[0-9]{2}|Q[1-4]\s*20[0-9]{2}|[0-9]+\s*(?:day|days|week|weeks|month|months|year|years)|per\s+month|per\s+year|annually|monthly|yearly)\b", sentence, re.I)
    quantities = re.findall(r"\b[0-9][0-9,]*(?:\.[0-9]+)?\s*(?:(?:support\s+)?hours/month|orders/day|hours|orders|users|clients|restaurants|seats|items|modules)\b", sentence, re.I)
    ranges = re.findall(r"\b[0-9][0-9,]*(?:\.[0-9]+)?\s*(?:-|to)\s*[0-9][0-9,]*(?:\.[0-9]+)?\b", sentence, re.I)
    comparative = re.findall(r"\b(?:more than|less than|cheaper|higher|lower|better|worse|at least|at most|minimum|maximum|vs\.?|versus)\b", sentence, re.I)
    roi_payback = re.findall(r"\b(?:ROI|return on investment|payback|break even|break-even|margin|profit)\b", sentence, re.I)
    absolute = re.findall(r"\b(?:always|never|best|guaranteed|universal|all|none|replace|eliminate)\b", sentence, re.I)
    ratios = re.findall(r"\b[0-9]+(?:\.[0-9]+)?\s*:\s*[0-9]+(?:\.[0-9]+)?\b", sentence)
    if money:
        types.append("MONEY")
        values["money"] = money
    if percentages or ratios:
        types.append("PERCENTAGE_OR_RATIO")
        values["percentages"] = percentages
        values["ratios"] = ratios
    if dates:
        types.append("DATE_OR_PERIOD")
        values["dates_or_periods"] = dates
    if quantities:
        types.append("QUANTITY_OR_UNIT")
        values["quantities"] = quantities
    if ranges:
        types.append("RANGE")
        values["ranges"] = ranges
    if comparative:
        types.append("COMPARATIVE")
        values["comparatives"] = comparative
    if roi_payback:
        types.append("ROI_PAYBACK_OR_MARGIN")
        values["roi_terms"] = roi_payback
    if re.search(r"\b(?:total|equals|=|annual|monthly|per month|per year|x\s*12|12\s*x)\b", sentence, re.I):
        types.append("CALCULATION")
    if absolute:
        types.append("ABSOLUTE_LANGUAGE")
        values["absolute_terms"] = absolute
    return sorted(set(types)), values


def deterministic_audit_notes(sentence: str, values: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    nums = [float(n.replace(",", "")) for n in re.findall(r"\b[0-9][0-9,]*(?:\.[0-9]+)?\b", sentence)]
    lower = sentence.lower()
    if "per month" in lower and "annual" in lower and len(nums) >= 2:
        monthly, annual = nums[0], nums[-1]
        if abs(monthly * 12 - annual) > 0.01:
            notes.append(f"BROKEN_MONTHLY_TO_ANNUAL: {monthly} x 12 != {annual}")
    if "margin" in lower and len(nums) >= 3:
        revenue, cost, stated = nums[0], nums[1], nums[-1]
        if revenue:
            margin = (revenue - cost) / revenue * 100
            if abs(margin - stated) > 0.5:
                notes.append(f"BROKEN_MARGIN: ({revenue} - {cost}) / {revenue} = {margin:.1f}%, not {stated}%")
    if " of " in lower and "%" in lower and len(nums) >= 3:
        base, pct, stated = nums[0], nums[1], nums[-1]
        calculated = base * pct / 100
        if abs(calculated - stated) > 0.01:
            notes.append(f"BROKEN_PERCENTAGE: {pct}% of {base} = {calculated}, not {stated}")
    for item in values.get("ranges", []):
        left, right = [float(x.replace(",", "")) for x in re.findall(r"[0-9][0-9,]*(?:\.[0-9]+)?", item)[:2]]
        if left > right:
            notes.append(f"BROKEN_RANGE: lower bound {left} exceeds upper bound {right}")
    return notes


def claim_classification(sentence: str) -> str:
    if re.search(r"\b(scenario assumption|assume|assumption|fixture)\b", sentence, re.I):
        return "SCENARIO_ASSUMPTION"
    if re.search(r"\b(source-backed|verified|official|internal project fact)\b", sentence, re.I):
        return "INTERNAL_PROJECT_FACT"
    return "UNKNOWN"


def extract_claims_record(run_dir: Path) -> list[dict[str, Any]]:
    claims = []
    for executive in EXECUTIVES:
        memo = read(run_dir / "memos" / f"{executive}.md")
        body = current_memo(memo)
        for sentence in split_claim_sentences(body):
            claim_types, detected = detect_claim_values(sentence)
            if not claim_types:
                continue
            claims.append({
                "claim_id": f"CL-{len(claims)+1:04d}",
                "memo": executive,
                "section": "CURRENT_MEMO",
                "exact_text": sentence,
                "claim_type": claim_types,
                "detected_values": detected,
                "classification": claim_classification(sentence),
                "evidence_ids": re.findall(r"EV-[0-9]{4}", sentence),
                "audit_status": "NEEDS_AUDIT" if claim_classification(sentence) == "UNKNOWN" else "LABELED",
                "deterministic_audit": deterministic_audit_notes(sentence, detected),
            })
    save_json(run_dir / "CLAIMS.json", claims)
    event(run_dir, "CLAIMS_EXTRACTED", {"count": len(claims)})
    return claims


def extract_claims(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    if status(run_dir)["stage"] == "MEMOS_SUBMITTED":
        transition(run_dir, "AUDIT_IN_PROGRESS", "claim extraction started")
    claims = extract_claims_record(run_dir)
    print(json.dumps(claims, indent=2, sort_keys=True))


def record_fact_check_record(run_dir: Path, claim_id: str, finding: str, required_correction: str, evidence_ids: list[str], status_value: str = "OPEN", contradicted_text: str | None = None, corrected_text: str | None = None, blocking: bool = True) -> dict[str, Any]:
    checks = load_json(run_dir / "FACT_CHECKS.json", [])
    check = {
        "fact_check_id": next_id(checks, "fact_check_id", "FC"),
        "claim_id": claim_id,
        "blocking": blocking,
        "finding": finding,
        "required_correction": required_correction,
        "evidence_ids": evidence_ids,
        "status": status_value,
        "contradicted_text": contradicted_text,
        "corrected_text": corrected_text,
    }
    checks.append(check)
    save_json(run_dir / "FACT_CHECKS.json", checks)
    append(run_dir / "AUDITOR.md", f"""## [FACT_CHECK:{check['fact_check_id']}:{'BLOCKING' if blocking else 'NON_BLOCKING'}]
Claim ID: {claim_id}
Finding: {finding}
Evidence: {', '.join(evidence_ids)}
Required correction: {required_correction}
Status: {status_value}

""")
    event(run_dir, "FACT_CHECK_RECORDED", check)
    return check


def record_fact_check(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    check = record_fact_check_record(run_dir, args.claim_id, args.finding, args.required_correction, args.evidence_ids.split(","), args.status_value, args.contradicted_text, args.corrected_text, not args.non_blocking)
    print(json.dumps(check, indent=2, sort_keys=True))


def validate_audit_record(run_dir: Path) -> list[str]:
    failures = []
    claim_list = load_json(run_dir / "CLAIMS.json", [])
    claims = {c["claim_id"]: c for c in claim_list}
    checks = load_json(run_dir / "FACT_CHECKS.json", [])
    checked_claims = {c.get("claim_id") for c in checks if c.get("status") == "RESOLVED"}
    for claim in claim_list:
        deterministic = claim.get("deterministic_audit", [])
        if deterministic and claim["claim_id"] not in checked_claims:
            failures.append(f"{claim['claim_id']} has deterministic audit issue without resolved fact check: {'; '.join(deterministic)}")
        if "ABSOLUTE_LANGUAGE" in claim.get("claim_type", []) and claim.get("classification") == "UNKNOWN" and claim["claim_id"] not in checked_claims:
            failures.append(f"{claim['claim_id']} uses unsupported absolute language without resolved fact check")
        if claim.get("detected_values") and claim.get("classification") == "UNKNOWN" and claim["claim_id"] not in checked_claims:
            failures.append(f"{claim['claim_id']} has material values without classification, evidence, or resolved fact check")
    for check in checks:
        if not check.get("blocking"):
            continue
        claim = claims.get(check["claim_id"])
        if not claim:
            failures.append(f"{check['fact_check_id']} references unknown claim {check['claim_id']}")
            continue
        memo_current = current_memo(read(run_dir / "memos" / f"{claim['memo']}.md"))
        contradicted = check.get("contradicted_text") or claim["exact_text"]
        corrected = check.get("corrected_text")
        if check["status"] != "RESOLVED":
            failures.append(f"{check['fact_check_id']} blocking check is {check['status']}")
        elif contradicted and contradicted in memo_current:
            claim_line = next((line for line in memo_current.splitlines() if contradicted in line), "")
            if not re.search(r"\b(assumption|assumed|scenario|hypothesis|unverified)\b", claim_line, re.I):
                failures.append(f"{check['fact_check_id']} marked resolved but contradicted claim remains as fact in {claim['memo']} CURRENT_MEMO")
        elif corrected and corrected not in memo_current:
            failures.append(f"{check['fact_check_id']} marked resolved but corrected text not found in {claim['memo']} CURRENT_MEMO")
    for executive in EXECUTIVES:
        memo_path = run_dir / "memos" / f"{executive}.md"
        text = read(memo_path)
        gate = "PASSED" if not failures else "BLOCKED"
        write(memo_path, re.sub(r"evidence_gate: \w+", f"evidence_gate: {gate}", text))
    if failures:
        if status(run_dir)["stage"] == "AUDIT_IN_PROGRESS":
            transition(run_dir, "AUDIT_BLOCKED", "blocking fact checks remain")
        update_status(run_dir, pending_tasks=["record-author-response", "submit-memo", "validate-audit"])
    else:
        if status(run_dir)["stage"] == "AUDIT_BLOCKED":
            transition(run_dir, "AUDIT_IN_PROGRESS", "author corrections submitted")
        transition(run_dir, "AUDIT_PASSED", "all blocking fact checks resolved against current memos")
        update_status(run_dir, pending_tasks=["create-anonymous-review-packets"])
    return failures


def validate_audit(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    failures = validate_audit_record(run_dir)
    if failures:
        raise SystemExit("Audit validation failed:\n- " + "\n- ".join(failures))
    print(f"PASS audit {run_dir}")


def make_packet_text(source: str, memo: str) -> str:
    body = current_memo(memo)
    body = re.sub(r"executive:\s*\S+", "executive: ANONYMIZED", body)
    body = body.replace(source, "anonymous-author")
    return "# Anonymous Review Packet\n\nAuthor: ANONYMIZED\n\n" + body


def create_anonymous_review_packets(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    transition(run_dir, "PEER_REVIEW_IN_PROGRESS", "anonymous review packets created")
    packet_dir = run_dir / "_work" / "review-packets"
    route_map = []
    for reviewer in EXECUTIVES:
        for source in EXECUTIVES:
            if reviewer == source:
                continue
            packet_id = f"PKT-{len(route_map)+1:04d}"
            assignment_id = f"RA-{len(route_map)+1:04d}"
            packet_path = packet_dir / f"{packet_id}.md"
            write(packet_path, make_packet_text(source, read(run_dir / "memos" / f"{source}.md")))
            route_map.append({
                "assignment_id": assignment_id,
                "packet_id": packet_id,
                "source_memo": source,
                "assigned_reviewer": reviewer,
                "packet_path": durable_relpath(packet_path, run_dir),
                "review_id": None,
                "status": "ASSIGNED",
                "submission_time": None,
                "waiver_reason": None,
                "retry_count": 0,
            })
    save_json(run_dir / "_work" / "review-routing-map.private.json", route_map)
    event(run_dir, "REVIEW_PACKETS_CREATED", {"count": len(route_map)})
    update_status(run_dir, pending_tasks=["record-peer-review"])
    print(f"CREATED {len(route_map)} packets")


def record_peer_review_record(run_dir: Path, packet_id: str, comment: str, objection: bool = True) -> dict[str, Any]:
    route_map = load_json(run_dir / "_work" / "review-routing-map.private.json", [])
    route = next((r for r in route_map if r["packet_id"] == packet_id), None)
    if not route:
        raise SystemExit(f"Unknown packet: {packet_id}")
    reviews = load_json(run_dir / "reviews" / "PEER_REVIEWS.json", [])
    review = {
        "review_id": next_id(reviews, "review_id", "PR"),
        "packet_id": packet_id,
        "source_memo": route["source_memo"],
        "anonymous_reviewer": f"R-{hashlib.sha1(route['assigned_reviewer'].encode()).hexdigest()[:6]}",
        "comment": comment,
        "type": "OBJECTION" if objection else "COMMENT",
    }
    reviews.append(review)
    route["review_id"] = review["review_id"]
    route["status"] = "COMPLETE"
    route["submission_time"] = now()
    save_json(run_dir / "reviews" / "PEER_REVIEWS.json", reviews)
    save_json(run_dir / "_work" / "review-routing-map.private.json", route_map)
    event(run_dir, "PEER_REVIEW_RECORDED", {"review_id": review["review_id"], "packet_id": packet_id})
    return review


def waive_peer_review_record(run_dir: Path, assignment_id: str, reason: str) -> dict[str, Any]:
    route_map = load_json(run_dir / "_work" / "review-routing-map.private.json", [])
    route = next((r for r in route_map if r["assignment_id"] == assignment_id), None)
    if not route:
        raise SystemExit(f"Unknown review assignment: {assignment_id}")
    route["status"] = "WAIVED"
    route["waiver_reason"] = reason
    route["submission_time"] = now()
    save_json(run_dir / "_work" / "review-routing-map.private.json", route_map)
    event(run_dir, "PEER_REVIEW_WAIVED", {"assignment_id": assignment_id, "reason": reason})
    return route


def waive_peer_review(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    route = waive_peer_review_record(run_dir, args.assignment_id, args.reason)
    print(json.dumps(route, indent=2, sort_keys=True))


def incomplete_review_assignments(run_dir: Path) -> list[dict[str, Any]]:
    route_map = load_json(run_dir / "_work" / "review-routing-map.private.json", [])
    return [r for r in route_map if r.get("status") not in {"COMPLETE", "FAILED", "WAIVED"}]


def record_peer_review(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    review = record_peer_review_record(run_dir, args.packet_id, args.comment, not args.comment_only)
    print(json.dumps(review, indent=2, sort_keys=True))


def merge_review_events(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    incomplete = incomplete_review_assignments(run_dir)
    if incomplete:
        raise SystemExit("Peer review incomplete:\n- " + "\n- ".join(f"{r['assignment_id']} {r['assigned_reviewer']} reviewing {r['source_memo']} is {r['status']}" for r in incomplete))
    reviews = load_json(run_dir / "reviews" / "PEER_REVIEWS.json", [])
    for review in reviews:
        block = f"""## [PEER_REVIEW:{review['review_id']}:{review['type']}]
Anonymous reviewer: {review['anonymous_reviewer']}
Comment: {review['comment']}
Evidence:
Requested response: Author must accept, reject, or partially accept.
"""
        append_section(run_dir / "memos" / f"{review['source_memo']}.md", "# PEER_REVIEW", block)
    write(run_dir / "reviews" / "ANONYMOUS_PEER_REVIEW.md", f"# Anonymous Peer Review\n\nMerged {len(reviews)} anonymized review events through routing map.\n")
    transition(run_dir, "AUTHOR_REVISION", "peer reviews merged for author response")
    update_status(run_dir, pending_tasks=["record-author-response", "validate-veto"])
    event(run_dir, "PEER_REVIEWS_MERGED", {"count": len(reviews)})
    print(f"MERGED {len(reviews)} reviews")


def record_author_response_record(run_dir: Path, executive: str, responds_to: str, disposition: str, reason: str, change: str) -> None:
    responses = load_json(run_dir / "AUTHOR_RESPONSES.json", [])
    response_id = next_id(responses, "author_response_id", "AR")
    responses.append({"author_response_id": response_id, "executive": executive, "responds_to": responds_to, "disposition": disposition, "reason": reason, "change": change})
    save_json(run_dir / "AUTHOR_RESPONSES.json", responses)
    append_section(run_dir / "memos" / f"{executive}.md", "# AUTHOR_RESPONSES", f"""## [AUTHOR_RESPONSE:{response_id}]
Responds to: {responds_to}
Disposition: {disposition}
Reason: {reason}
Change made: {change}
""")
    event(run_dir, "AUTHOR_RESPONSE_RECORDED", {"author_response_id": response_id, "executive": executive})


def record_author_response(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    record_author_response_record(run_dir, args.executive, args.responds_to, args.disposition, args.reason, args.change)
    print(f"RECORDED author response {args.executive}")


def validate_veto_record(run_dir: Path, holder: str, stage: str, protected_domain: str, challenged_statement: str, reason: str, evidence: str, remedy: str, challenged_artifact: str | None = None, challenged_section: str | None = None) -> tuple[bool, str]:
    config = load_json(run_dir / "RUN_CONFIG.json", {})
    allowed = config.get("veto_assignments", {}).get(holder, [])
    stage_key = "POST_CHAIR" if "POST" in stage else "PRE_CHAIR"
    authorized = any((a["stage"] in {stage_key, "ANY"} and a["protected_domain"].lower() == protected_domain.lower()) for a in allowed)
    if not authorized:
        return False, f"{holder} is not authorized for {stage_key} / {protected_domain}"
    if challenged_artifact:
        all_text = artifact_text(run_dir, challenged_artifact, challenged_section)
    else:
        all_text = "\n".join(read(p) for p in (run_dir / "memos").glob("*.md"))
        if stage_key == "POST_CHAIR" and (run_dir / "CHAIRMAN.md").exists():
            all_text += "\n" + read(run_dir / "CHAIRMAN.md")
    if challenged_statement not in all_text:
        return False, "challenged statement does not exist in reviewed artifacts"
    if not reason or not evidence or not remedy:
        return False, "reason, evidence, and actionable remedy are required"
    return True, "valid scoped veto"


def infer_veto_artifact(holder: str, stage: str) -> tuple[str, str | None]:
    if "POST" in stage:
        return "CHAIRMAN.md", None
    if holder in EXECUTIVES:
        return f"memos/{holder}.md", "CURRENT_MEMO"
    return "CHAIRMAN.md", None


def record_veto_record(run_dir: Path, holder: str, stage: str, protected_domain: str, challenged_statement: str, reason: str, evidence: str, remedy: str, challenged_artifact: str | None = None, challenged_section: str | None = None, verification_method: str = "contains_text", remedy_must_contain: str | None = None) -> dict[str, Any]:
    vetoes = load_json(run_dir / "VETOES.json", [])
    if not challenged_artifact:
        challenged_artifact, inferred_section = infer_veto_artifact(holder, stage)
        challenged_section = challenged_section or inferred_section
    valid, validation_reason = validate_veto_record(run_dir, holder, stage, protected_domain, challenged_statement, reason, evidence, remedy, challenged_artifact, challenged_section)
    veto = {
        "veto_id": next_id(vetoes, "veto_id", "V"),
        "holder": holder,
        "stage": stage,
        "protected_domain": protected_domain,
        "challenged_statement": challenged_statement,
        "challenged_artifact": challenged_artifact,
        "challenged_section": challenged_section,
        "reason": reason,
        "evidence": evidence,
        "required_remedy": remedy,
        "verification_method": verification_method,
        "remedy_must_contain": remedy_must_contain or remedy,
        "status": "OPEN" if valid else "DEMOTED_TO_OBJECTION",
        "valid": valid,
        "validation_reason": validation_reason,
        "chairman_resolution_note": None,
    }
    vetoes.append(veto)
    save_json(run_dir / "VETOES.json", vetoes)
    target = holder if holder in EXECUTIVES else "executor"
    append_section(run_dir / "memos" / f"{target}.md", "# VETOES", f"""## [VETO:{veto['veto_id']}:{stage}]
Holder: {holder}
Protected domain: {protected_domain}
Challenged statement: {challenged_statement}
Reason: {reason}
Evidence: {evidence}
Required remedy: {remedy}
Verification method: {verification_method}
Status: {veto['status']}
Validation: {validation_reason}
""")
    event(run_dir, "VETO_RECORDED", veto)
    return veto


def record_veto(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    veto = record_veto_record(run_dir, args.holder, args.stage, args.protected_domain, args.challenged_statement, args.reason, args.evidence, args.remedy, args.challenged_artifact, args.challenged_section, args.verification_method, args.remedy_must_contain)
    print(json.dumps(veto, indent=2, sort_keys=True))


def verify_veto_remedy(run_dir: Path, veto: dict[str, Any], chairman_note: str | None = None) -> tuple[bool, str]:
    if not veto.get("valid"):
        return True, "invalid veto is ordinary dissent"
    method = veto.get("verification_method", "contains_text")
    if method == "requires_judgment":
        if chairman_note:
            return True, "resolved by explicit Chairman judgment"
        return False, "REQUIRES_JUDGMENT: Chairman resolution note required"
    text = artifact_text(run_dir, veto.get("challenged_artifact", ""), veto.get("challenged_section"))
    needle = veto.get("remedy_must_contain") or veto.get("required_remedy")
    if method == "contains_text":
        if needle and needle in text:
            return True, "required remedy text found"
        return False, f"required remedy text not found: {needle}"
    if method == "challenged_statement_removed":
        if veto.get("challenged_statement") not in text:
            return True, "challenged statement removed"
        return False, "challenged statement still present"
    return False, f"unknown verification method: {method}"


def resolve_veto_record(run_dir: Path, veto_id: str, chairman_note: str | None = None) -> dict[str, Any]:
    vetoes = load_json(run_dir / "VETOES.json", [])
    veto = next((v for v in vetoes if v["veto_id"] == veto_id), None)
    if not veto:
        raise SystemExit(f"Unknown veto: {veto_id}")
    ok, reason = verify_veto_remedy(run_dir, veto, chairman_note)
    if ok:
        veto["status"] = "RESOLVED"
        veto["validation_reason"] = reason
        veto["chairman_resolution_note"] = chairman_note
    elif reason.startswith("REQUIRES_JUDGMENT"):
        veto["status"] = "REQUIRES_JUDGMENT"
        veto["validation_reason"] = reason
    else:
        raise SystemExit(f"Veto remedy not verified for {veto_id}: {reason}")
    save_json(run_dir / "VETOES.json", vetoes)
    event(run_dir, "VETO_REMEDY_VERIFIED", {"veto_id": veto_id, "status": veto["status"], "reason": veto["validation_reason"]})
    return veto


def resolve_veto(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    veto = resolve_veto_record(run_dir, args.veto_id, args.chairman_note)
    print(json.dumps(veto, indent=2, sort_keys=True))


def prepare_chairman_packet(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    vetoes = load_json(run_dir / "VETOES.json", [])
    open_valid = [v["veto_id"] for v in vetoes if v.get("valid") and v.get("status") == "OPEN"]
    if open_valid and not args.allow_open_vetoes:
        raise SystemExit(f"Open valid vetoes remain: {', '.join(open_valid)}")
    transition(run_dir, "PRE_CHAIR_READY", "author revision and pre-chair veto cycle complete")
    packet = ["# Chairman Packet\n"]
    for executive in EXECUTIVES:
        packet.append(f"\n## {executive}\n")
        packet.append(current_memo(read(run_dir / "memos" / f"{executive}.md")))
    packet.append("\n## Audit\n")
    packet.append(read(run_dir / "AUDITOR.md") if (run_dir / "AUDITOR.md").exists() else "")
    packet.append("\n## Vetoes\n")
    packet.append(json.dumps(vetoes, indent=2))
    route_map = load_json(run_dir / "_work" / "review-routing-map.private.json", [])
    waivers = [r for r in route_map if r.get("status") == "WAIVED"]
    packet.append("\n## Peer Review Waivers\n")
    packet.append(json.dumps(waivers, indent=2))
    write(run_dir / "_work" / "CHAIRMAN_PACKET.md", "\n".join(packet))
    update_status(run_dir, pending_tasks=["record-first-synthesis"])
    print("PREPARED chairman packet")


def record_first_synthesis(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    transition(run_dir, "CHAIRMAN_SYNTHESIS", "chairman first synthesis recorded")
    write(run_dir / "CHAIRMAN.md", "# Chairman File\n\n## First Synthesis\n" + args.text + "\n")
    update_status(run_dir, pending_tasks=["record-devils-advocate"])
    event(run_dir, "FIRST_SYNTHESIS_RECORDED", {})
    print("RECORDED first synthesis")


def record_devils_advocate(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    transition(run_dir, "DEVILS_ADVOCATE_COMPLETE", "devils advocate attack recorded")
    write(run_dir / "DEVILS_ADVOCATE.md", "# Devil's Advocate\n\nAttack: " + args.attack + "\nDefeating change: " + args.defeating_change + "\n")
    append(run_dir / "CHAIRMAN.md", "\n## Devil's Advocate Considered\n" + args.attack + "\n")
    update_status(run_dir, pending_tasks=["record-provisional-verdict"])
    event(run_dir, "DEVILS_ADVOCATE_RECORDED", {})
    print("RECORDED devils advocate")


def record_provisional_verdict(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    transition(run_dir, "PROVISIONAL_VERDICT", "provisional verdict recorded")
    append(run_dir / "CHAIRMAN.md", "\n## Provisional Verdict\n" + args.text + "\n")
    update_status(run_dir, pending_tasks=["open-post-chair-review"])
    event(run_dir, "PROVISIONAL_VERDICT_RECORDED", {})
    print("RECORDED provisional verdict")


def open_post_chair_review(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    transition(run_dir, "POST_CHAIR_VETO_REVIEW", "post-chair veto review opened")
    update_status(run_dir, pending_tasks=["record-veto", "record-final-verdict"])
    print("OPEN post-chair review")


def record_final_verdict(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    vetoes = load_json(run_dir / "VETOES.json", [])
    unresolved = [v for v in vetoes if v.get("valid") and v.get("status") != "RESOLVED"]
    ordinary_dissent = [v for v in vetoes if not v.get("valid")]
    text = args.text
    if unresolved:
        text += "\n\nUnresolved valid vetoes surfaced to human owner:\n" + json.dumps(unresolved, indent=2)
    if ordinary_dissent:
        text += "\n\nOut-of-scope veto attempts preserved as ordinary dissent:\n" + json.dumps(ordinary_dissent, indent=2)
    transition(run_dir, "FINAL_VERDICT_COMPLETE", "final verdict recorded")
    append(run_dir / "CHAIRMAN.md", "\n## Final Verdict\n" + text + "\n\n## Human Owner Decision\nHuman owner may accept, reject, or revise.\n")
    write(run_dir / "COMPLETION_REPORT.md", "# Completion Report\n\nDecision: " + args.summary + "\nDisagreement: preserved in Chairman file.\nNext action: " + args.next_action + "\n")
    write(run_dir / "NEXT_RUN_HANDOFF.md", "# Next Run Handoff\n\nCarry forward final verdict, evidence library, unresolved questions, and veto history.\n")
    update_status(run_dir, pending_tasks=["validate-run", "complete-run"])
    event(run_dir, "FINAL_VERDICT_RECORDED", {})
    print("RECORDED final verdict")


def validate_event_tags(text: str, label: str) -> list[str]:
    failures = []
    for keyword, ident in re.findall(r"\[([A-Z_]+):([^:\]]+)", text):
        if keyword not in EVENT_KEYWORDS:
            failures.append(f"{label} has unapproved event tag {keyword}")
        elif not re.fullmatch(EVENT_KEYWORDS[keyword], ident):
            failures.append(f"{label} has malformed {keyword} id {ident}")
    return failures


def validate_run(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    failures: list[str] = []
    expected = {f"{e}.md" for e in EXECUTIVES}
    found = {p.name for p in (run_dir / "memos").glob("*.md")}
    if found != expected:
        failures.append(f"Expected exactly five canonical memos {sorted(expected)}, found {sorted(found)}")
    seen_tags = set()
    for memo_name in sorted(expected):
        path = run_dir / "memos" / memo_name
        if not path.exists():
            continue
        text = read(path)
        for section in ["# CURRENT_MEMO", "# EVIDENCE_REQUESTS", "# FACT_CHECK", "# PEER_REVIEW", "# AUTHOR_RESPONSES", "# VETOES", "# REVISION_LOG"]:
            if section not in text:
                failures.append(f"{memo_name} missing {section}")
        failures.extend(validate_event_tags(text, memo_name))
        for tag in re.findall(r"\[([A-Z_]+:[^:\]]+)", text):
            if tag in seen_tags and not (tag.startswith("EVIDENCE_RESPONSE:") or tag.startswith("REVISION:")):
                failures.append(f"Duplicate event tag {tag}")
            seen_tags.add(tag)
    lib = load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {})
    if not any(r.get("status") == "ANSWERED_FROM_CACHE" for r in lib.get("requests", [])):
        failures.append("No evidence request was answered from real cache logic")
    failures.extend(validate_audit_record(run_dir) if status(run_dir).get("stage") in {"AUDIT_IN_PROGRESS", "AUDIT_BLOCKED"} else [])
    all_checks = load_json(run_dir / "FACT_CHECKS.json", [])
    for check in all_checks:
        if check.get("contradicted_text"):
            claim = next((c for c in load_json(run_dir / "CLAIMS.json", []) if c["claim_id"] == check["claim_id"]), None)
            if claim and check["contradicted_text"] in current_memo(read(run_dir / "memos" / f"{claim['memo']}.md")):
                failures.append(f"{check['fact_check_id']} contradicted claim still appears in CURRENT_MEMO")
    route_map = load_json(run_dir / "_work" / "review-routing-map.private.json", [])
    if route_map:
        if len(route_map) != 20:
            failures.append(f"Expected 20 peer-review assignments, found {len(route_map)}")
        for route in route_map:
            packet = read(stored_path(run_dir, route["packet_path"]))
            if route["source_memo"] in packet:
                failures.append(f"Review packet {route['packet_id']} leaks author identity")
            if route.get("status") not in {"COMPLETE", "FAILED", "WAIVED"}:
                failures.append(f"Review assignment {route.get('assignment_id')} is not complete, failed, or waived")
    else:
        failures.append("No anonymous review routing map exists")
    vetoes = load_json(run_dir / "VETOES.json", [])
    if not any(v.get("valid") for v in vetoes):
        failures.append("No valid scoped veto recorded")
    if not any(not v.get("valid") and v.get("status") == "DEMOTED_TO_OBJECTION" for v in vetoes):
        failures.append("No invalid veto demoted to objection")
    for veto in vetoes:
        if veto.get("valid"):
            ok, reason = verify_veto_remedy(run_dir, veto, veto.get("chairman_resolution_note"))
            if veto.get("status") != "RESOLVED":
                failures.append(f"{veto['veto_id']} valid veto is {veto.get('status')}, not RESOLVED")
            elif not ok:
                failures.append(f"{veto['veto_id']} status says RESOLVED but remedy does not verify: {reason}")
    for path in ["CHAIRMAN.md", "DEVILS_ADVOCATE.md", "COMPLETION_REPORT.md", "NEXT_RUN_HANDOFF.md", "RUN_EVENTS.jsonl"]:
        if not (run_dir / path).exists():
            failures.append(f"Missing {path}")
    chairman = read(run_dir / "CHAIRMAN.md") if (run_dir / "CHAIRMAN.md").exists() else ""
    for section in ["## First Synthesis", "## Devil's Advocate Considered", "## Provisional Verdict", "## Final Verdict"]:
        if section not in chairman:
            failures.append(f"Chairman missing {section}")
    if status(run_dir).get("stage") not in {"FINAL_VERDICT_COMPLETE", "RUN_COMPLETE"}:
        failures.append("Run is not at final verdict or complete stage")
    failures.extend(verify_old_hashes(run_dir))
    for agent in [REPO / ".agents" / "skills" / "codex-council-v2" / "SKILL.md", *[REPO / ".codex" / "agents" / f"codex-council-v2-{name}.toml" for name in ["contrarian", "first-principles", "expansionist", "outsider", "executor", "librarian", "auditor", "devils-advocate", "chairman"]]]:
        if not agent.exists():
            failures.append(f"Missing V2 entry point: {agent}")
    if failures:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(failures))
    write(run_dir / "VALIDATION_RESULTS.md", "# Validation Results\n\nPASS: state machine, cache, audit, review routing, veto validation, resume, and old-system hash checks passed.\n")
    print(f"PASS {run_dir}")


def resume(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    stale = []
    for lock in (run_dir / "_work" / "locks").glob("*.lock"):
        if "ACTIVE" in read(lock):
            stale.append(durable_relpath(lock, run_dir))
    data = status(run_dir)
    stage = data.get("stage", "UNKNOWN")
    next_actions = {
        "CHARTER_DRAFTED": "validate-charter",
        "CHARTER_APPROVED": "open-evidence-requests",
        "EVIDENCE_REQUESTS_OPEN": "register or resolve evidence requests, then mark-evidence-ready",
        "EVIDENCE_READY": "submit-memo for each executive",
        "MEMOS_SUBMITTED": "extract-claims",
        "AUDIT_IN_PROGRESS": "record-fact-check or validate-audit",
        "AUDIT_BLOCKED": "record-author-response and submit corrected memo, then validate-audit",
        "AUDIT_PASSED": "create-anonymous-review-packets",
        "PEER_REVIEW_IN_PROGRESS": "record-peer-review and merge-review-events",
        "AUTHOR_REVISION": "record-author-response, record-veto, then prepare-chairman-packet",
        "PRE_CHAIR_READY": "record-first-synthesis",
        "CHAIRMAN_SYNTHESIS": "record-devils-advocate",
        "DEVILS_ADVOCATE_COMPLETE": "record-provisional-verdict",
        "PROVISIONAL_VERDICT": "open-post-chair-review",
        "POST_CHAIR_VETO_REVIEW": "record-final-verdict",
        "FINAL_VERDICT_COMPLETE": "validate-run or complete-run",
        "RUN_COMPLETE": "no pending workflow",
    }
    expected_agents = {
        "CHARTER_DRAFTED": "codex-council-v2 operator",
        "CHARTER_APPROVED": "codex-council-v2 operator",
        "EVIDENCE_REQUESTS_OPEN": "codex-council-v2-librarian",
        "EVIDENCE_READY": "five executive agents",
        "MEMOS_SUBMITTED": "codex-council-v2-auditor",
        "AUDIT_IN_PROGRESS": "codex-council-v2-auditor",
        "AUDIT_BLOCKED": "blocked memo owner",
        "AUDIT_PASSED": "codex-council-v2-librarian",
        "PEER_REVIEW_IN_PROGRESS": "five executive agents as reviewers",
        "AUTHOR_REVISION": "memo owners and veto holders",
        "PRE_CHAIR_READY": "codex-council-v2-chairman",
        "CHAIRMAN_SYNTHESIS": "codex-council-v2-devils-advocate",
        "DEVILS_ADVOCATE_COMPLETE": "codex-council-v2-chairman",
        "PROVISIONAL_VERDICT": "codex-council-v2 operator",
        "POST_CHAIR_VETO_REVIEW": "authorized veto holders or Chairman",
        "FINAL_VERDICT_COMPLETE": "codex-council-v2 operator",
        "RUN_COMPLETE": "none",
    }
    required_inputs = {
        "EVIDENCE_REQUESTS_OPEN": ["RUN_CHARTER.md", "RUN_CONFIG.json", "evidence/EVIDENCE_LIBRARY.json"],
        "EVIDENCE_READY": ["RUN_CHARTER.md", "evidence/EVIDENCE_LIBRARY.json"],
        "AUDIT_IN_PROGRESS": ["memos/*.md", "evidence/EVIDENCE_LIBRARY.json", "CLAIMS.json"],
        "PEER_REVIEW_IN_PROGRESS": ["_work/review-packets/*.md", "_work/review-routing-map.private.json"],
        "AUTHOR_REVISION": ["memos/*.md", "reviews/PEER_REVIEWS.json", "VETOES.json"],
        "PRE_CHAIR_READY": ["_work/CHAIRMAN_PACKET.md"],
        "POST_CHAIR_VETO_REVIEW": ["CHAIRMAN.md", "VETOES.json"],
    }
    events = [json.loads(line) for line in read(run_dir / "RUN_EVENTS.jsonl").splitlines() if line.strip()] if (run_dir / "RUN_EVENTS.jsonl").exists() else []
    completed = [e["kind"] for e in events]
    failed = [e for e in events if e.get("kind", "").endswith("_FAILED")]
    human_approval = stage == "EVIDENCE_REQUESTS_OPEN" and any(r.get("answer_source") in {"NotebookLM", "approved web research"} for r in load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {}).get("requests", []))
    result = {
        "stage": stage,
        "current_valid_stage": data.get("last_valid_stage"),
        "completed_tasks": completed,
        "pending_tasks": data.get("pending_tasks", []),
        "failed_tasks": failed,
        "stale_locks": stale,
        "expected_next_agent": expected_agents.get(stage, "codex-council-v2 operator"),
        "required_input_files": required_inputs.get(stage, ["RUN_STATUS.json", "RUN_EVENTS.jsonl"]),
        "next_action": next_actions.get(stage, "inspect run"),
        "human_approval_required": human_approval,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


def complete_run(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    validate_run(argparse.Namespace(run_dir=str(run_dir)))
    transition(run_dir, "RUN_COMPLETE", "validation passed and completion accepted")
    update_status(
        run_dir,
        pending_tasks=[],
        release_gate="READY_FOR_BOUNDED_REAL_RUN",
    )
    print(f"COMPLETE {run_dir}")


def status_cmd(args: argparse.Namespace) -> None:
    print(json.dumps(status(run_dir_arg(args.run_dir)), indent=2, sort_keys=True))


def synthetic_test(_: argparse.Namespace) -> Path:
    run_id = "synthetic-fixture-001"
    run_dir = RUNS / run_id
    init_run(argparse.Namespace(run_id=run_id, title="Synthetic fixture decision", question="Choose a bounded fixture launch option.", force=True))
    validate_charter(argparse.Namespace(run_dir=str(run_dir)))
    open_evidence_requests(argparse.Namespace(run_dir=str(run_dir)))
    r1 = register_evidence_request_record(run_dir, "contrarian", "What is the fixture demand cap?", "pilot size", "SYNTHETIC", 9999, "SCENARIO_ASSUMPTION")
    resolve_evidence_request_record(run_dir, r1["request_id"], "Fixture demand is capped at 40 orders/day.", "SCENARIO_ASSUMPTION", "Fixture Operations Note")
    register_evidence_request_record(run_dir, "outsider", "What is the fixture demand cap?", "pilot size", "SYNTHETIC", 9999, "SCENARIO_ASSUMPTION")
    r3 = register_evidence_request_record(run_dir, "executor", "What is the fixture support budget?", "support load", "SYNTHETIC", 9999, "INTERNAL_PROJECT_FACT")
    ev2 = resolve_evidence_request_record(run_dir, r3["request_id"], "Fixture support budget is 20 hours/month, not 200.", "INTERNAL_PROJECT_FACT", "Fixture Cost Sheet")
    r4 = register_evidence_request_record(run_dir, "auditor", "What is the fixture safe price?", "price audit", "SYNTHETIC", 9999, "INTERNAL_PROJECT_FACT")
    ev3 = resolve_evidence_request_record(run_dir, r4["request_id"], "Fixture safe price is AED 499, not AED 999.", "INTERNAL_PROJECT_FACT", "Fixture Price Sheet")
    lib = load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {})
    lib.setdefault("contradictions", []).append({"contradiction_id": "CON-0001", "claim_a": "Fixture support budget is 20 hours/month.", "claim_b": "Fixture support budget is 200 hours/month.", "status": "RESOLVED_BY_EV-0002"})
    save_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", lib)
    mark_evidence_ready(argparse.Namespace(run_dir=str(run_dir)))
    positions = {
        "contrarian": "Proceed only if the fixture has an explicit kill switch.",
        "first-principles": "Choose the smallest reversible experiment that tests demand and support load.",
        "expansionist": "Preserve reusable assets, but do not price upside as certain.",
        "outsider": "The buyer will compare this to doing nothing unless the first step is concrete.",
        "executor": "Run a one-week pilot with a support-hour cap and failure criteria. Launch without support cap.",
    }
    economics = {
        "contrarian": "Scenario assumption: AED 100 per month equals AED 1,200 annually for the fixture pilot.",
        "first-principles": "AED 100 per month equals AED 1,000 annually.",
        "expansionist": "The fixture has 200 support hours/month. The fixture price is AED 999.",
        "outsider": "This fixture is guaranteed to be the best substitute.",
        "executor": "Scenario assumption: the pilot requires 20 support hours/month and one owner. 20% of AED 200 is AED 30. A margin with revenue AED 100 and cost AED 60 is 70%.",
    }
    for executive in EXECUTIVES:
        content = memo_text(run_id, executive, positions[executive], f"{executive} fixture reasoning from role-specific prompt.", economics[executive], ["EV-0001", ev2["evidence_id"]])
        submit_memo_record(run_dir, executive, content)
    claims = extract_claims_record(run_dir)
    if status(run_dir)["stage"] == "MEMOS_SUBMITTED":
        transition(run_dir, "AUDIT_IN_PROGRESS", "synthetic claim extraction started")
    bad_claim = next(c for c in claims if c["memo"] == "expansionist" and "200 support hours" in c["exact_text"])
    bad_price = next(c for c in claims if c["memo"] == "expansionist" and "AED 999" in c["exact_text"])
    bad_annual = next(c for c in claims if c["memo"] == "first-principles" and "1,000 annually" in c["exact_text"])
    bad_guarantee = next(c for c in claims if c["memo"] == "outsider" and "guaranteed" in c["exact_text"])
    bad_percent = next(c for c in claims if c["memo"] == "executor" and "20% of AED 200" in c["exact_text"])
    bad_margin = next(c for c in claims if c["memo"] == "executor" and "margin" in c["exact_text"])
    record_fact_check_record(run_dir, bad_claim["claim_id"], "False. Fixture support budget is 20 hours/month.", "Replace 200 with 20 or explicitly downgrade to assumption.", [ev2["evidence_id"]], "OPEN", "The fixture has 200 support hours/month.", "The fixture support budget is 20 hours/month.")
    record_fact_check_record(run_dir, bad_price["claim_id"], "False AED value. Fixture safe price is AED 499.", "Replace AED 999 with AED 499.", [ev3["evidence_id"]], "OPEN", "The fixture price is AED 999.", "The fixture price is AED 499.")
    record_fact_check_record(run_dir, bad_annual["claim_id"], "Broken monthly-to-annual calculation.", "Replace AED 1,000 annually with AED 1,200 annually.", [], "OPEN", "AED 100 per month equals AED 1,000 annually.", "AED 100 per month equals AED 1,200 annually.")
    record_fact_check_record(run_dir, bad_guarantee["claim_id"], "Unsupported guaranteed/best claim.", "Downgrade to a scenario assumption.", [], "OPEN", "This fixture is guaranteed to be the best substitute.", "Scenario assumption: this fixture may be a useful substitute.")
    record_fact_check_record(run_dir, bad_percent["claim_id"], "Broken percentage calculation.", "Replace AED 30 with AED 40.", [], "OPEN", "20% of AED 200 is AED 30.", "20% of AED 200 is AED 40.")
    record_fact_check_record(run_dir, bad_margin["claim_id"], "Broken margin calculation.", "Replace 70% with 40%.", [], "OPEN", "A margin with revenue AED 100 and cost AED 60 is 70%.", "A margin with revenue AED 100 and cost AED 60 is 40%.")
    try:
        validate_audit_record(run_dir)
    except SystemExit:
        pass
    corrected = memo_text(run_id, "expansionist", positions["expansionist"], "Expansionist fixture reasoning from role-specific prompt.", "The fixture support budget is 20 hours/month. The fixture price is AED 499. Upside remains unpriced optionality.", ["EV-0001", ev2["evidence_id"], ev3["evidence_id"]], "R2")
    submit_memo_record(run_dir, "expansionist", corrected)
    first_corrected = memo_text(run_id, "first-principles", positions["first-principles"], "First-principles fixture reasoning from role-specific prompt.", "AED 100 per month equals AED 1,200 annually.", ["EV-0001"], "R2")
    submit_memo_record(run_dir, "first-principles", first_corrected)
    outsider_corrected = memo_text(run_id, "outsider", positions["outsider"], "Outsider fixture reasoning from role-specific prompt.", "Scenario assumption: this fixture may be a useful substitute.", ["EV-0001"], "R2")
    submit_memo_record(run_dir, "outsider", outsider_corrected)
    executor_corrected = memo_text(run_id, "executor", "Launch without support cap.", "Executor fixture reasoning from role-specific prompt.", "Scenario assumption: the pilot requires 20 support hours/month and one owner. 20% of AED 200 is AED 40. A margin with revenue AED 100 and cost AED 60 is 40%.", ["EV-0001", ev2["evidence_id"]], "R2")
    submit_memo_record(run_dir, "executor", executor_corrected)
    checks = load_json(run_dir / "FACT_CHECKS.json", [])
    for check in checks:
        check["status"] = "RESOLVED"
    save_json(run_dir / "FACT_CHECKS.json", checks)
    record_author_response_record(run_dir, "expansionist", "FC-0001", "ACCEPTED", "Auditor evidence supports 20 hours/month.", "Corrected current memo.")
    failures = validate_audit_record(run_dir)
    if failures:
        raise SystemExit(failures)
    create_anonymous_review_packets(argparse.Namespace(run_dir=str(run_dir)))
    route_map = load_json(run_dir / "_work" / "review-routing-map.private.json", [])
    resume(argparse.Namespace(run_dir=str(run_dir)))
    for route in route_map:
        record_peer_review_record(run_dir, route["packet_id"], "Clarify failure criteria and support cap.")
    merge_review_events(argparse.Namespace(run_dir=str(run_dir)))
    valid_veto = record_veto_record(run_dir, "executor", "PRE_CHAIR", "feasible next action", "Launch without support cap.", "A launch without the support cap violates feasible next action.", ev2["evidence_id"], "Add the 20-hour/month support cap before Chairman review.", challenged_artifact="memos/executor.md", challenged_section="CURRENT_MEMO", remedy_must_contain="20-hour/month support cap before launch")
    invalid_veto = record_veto_record(run_dir, "outsider", "PRE_CHAIR", "brand preference", "Synthetic fixture decision.", "Plain naming is less attractive.", "none", "Rename the fixture.")
    executor_remedied = memo_text(run_id, "executor", "Run a one-week pilot with a 20-hour/month support cap before launch and explicit failure criteria.", "Executor fixture reasoning from role-specific prompt.", "Scenario assumption: the pilot requires 20 support hours/month and one owner. 20% of AED 200 is AED 40. A margin with revenue AED 100 and cost AED 60 is 40%.", ["EV-0001", ev2["evidence_id"]], "R3")
    submit_memo_record(run_dir, "executor", executor_remedied)
    resolve_veto_record(run_dir, valid_veto["veto_id"])
    record_author_response_record(run_dir, "executor", valid_veto["veto_id"], "ACCEPTED", "Support cap added.", "Resolved valid pre-chair veto.")
    resume(argparse.Namespace(run_dir=str(run_dir)))
    prepare_chairman_packet(argparse.Namespace(run_dir=str(run_dir), allow_open_vetoes=False))
    record_first_synthesis(argparse.Namespace(run_dir=str(run_dir), text="The emerging direction is a bounded one-week pilot with a 20-hour support cap."))
    record_devils_advocate(argparse.Namespace(run_dir=str(run_dir), attack="The pilot may validate only the fixture audience and hide real-world support variance.", defeating_change="Require failure criteria and a second evidence gate before scaling."))
    record_provisional_verdict(argparse.Namespace(run_dir=str(run_dir), text="Proceed with the pilot only if owner, support cap, and failure criteria are explicit. Start without owner assignment."))
    open_post_chair_review(argparse.Namespace(run_dir=str(run_dir)))
    post = record_veto_record(run_dir, "executor", "POST_CHAIR", "feasible next action", "Start without owner assignment.", "No executable owner means the next action is not feasible.", "RUN_CHARTER", "Assign owner and date.", challenged_artifact="CHAIRMAN.md", remedy_must_contain="Owner: Fixture Lead")
    append(run_dir / "CHAIRMAN.md", "\n## Post-Chair Veto Review\nExecutor post-chair veto resolved by assigning owner and date. Owner: Fixture Lead. Date: fixture week 1.\n")
    resolve_veto_record(run_dir, post["veto_id"])
    record_final_verdict(argparse.Namespace(run_dir=str(run_dir), text="Final bounded verdict: run the one-week synthetic pilot fixture with owner, 20-hour support cap, and failure criteria.", summary="run the synthetic one-week pilot fixture", next_action="assign owner and start only after failure criteria are accepted"))
    validate_run(argparse.Namespace(run_dir=str(run_dir)))
    return run_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init-run"); p.add_argument("--run-id", required=True); p.add_argument("--title", required=True); p.add_argument("--question", required=True); p.add_argument("--force", action="store_true"); p.set_defaults(func=init_run)
    p = sub.add_parser("validate-charter"); p.add_argument("--run-dir", required=True); p.set_defaults(func=validate_charter)
    p = sub.add_parser("open-evidence-requests"); p.add_argument("--run-dir", required=True); p.set_defaults(func=open_evidence_requests)
    p = sub.add_parser("register-evidence-request"); p.add_argument("--run-dir", required=True); p.add_argument("--requester", required=True); p.add_argument("--question", required=True); p.add_argument("--decision", required=True); p.add_argument("--geography", default="SYNTHETIC"); p.add_argument("--freshness-days", type=int, default=9999); p.add_argument("--acceptable-type", default="UNKNOWN"); p.add_argument("--scope", default="synthetic"); p.set_defaults(func=register_evidence_request)
    p = sub.add_parser("resolve-evidence-request"); p.add_argument("--run-dir", required=True); p.add_argument("--request-id", required=True); p.add_argument("--claim", required=True); p.add_argument("--classification", required=True); p.add_argument("--source-title", required=True); p.add_argument("--geography", default="SYNTHETIC"); p.add_argument("--limitations", default="fixture"); p.set_defaults(func=resolve_evidence_request)
    p = sub.add_parser("mark-evidence-ready"); p.add_argument("--run-dir", required=True); p.set_defaults(func=mark_evidence_ready)
    p = sub.add_parser("submit-memo"); p.add_argument("--run-dir", required=True); p.add_argument("--executive", required=True); p.add_argument("--content-file"); p.set_defaults(func=submit_memo)
    p = sub.add_parser("extract-claims"); p.add_argument("--run-dir", required=True); p.set_defaults(func=extract_claims)
    p = sub.add_parser("record-fact-check"); p.add_argument("--run-dir", required=True); p.add_argument("--claim-id", required=True); p.add_argument("--finding", required=True); p.add_argument("--required-correction", required=True); p.add_argument("--evidence-ids", required=True); p.add_argument("--status-value", default="OPEN"); p.add_argument("--contradicted-text"); p.add_argument("--corrected-text"); p.add_argument("--non-blocking", action="store_true"); p.set_defaults(func=record_fact_check)
    p = sub.add_parser("validate-audit"); p.add_argument("--run-dir", required=True); p.set_defaults(func=validate_audit)
    p = sub.add_parser("create-anonymous-review-packets"); p.add_argument("--run-dir", required=True); p.set_defaults(func=create_anonymous_review_packets)
    p = sub.add_parser("record-peer-review"); p.add_argument("--run-dir", required=True); p.add_argument("--packet-id", required=True); p.add_argument("--comment", required=True); p.add_argument("--comment-only", action="store_true"); p.set_defaults(func=record_peer_review)
    p = sub.add_parser("waive-peer-review"); p.add_argument("--run-dir", required=True); p.add_argument("--assignment-id", required=True); p.add_argument("--reason", required=True); p.set_defaults(func=waive_peer_review)
    p = sub.add_parser("merge-review-events"); p.add_argument("--run-dir", required=True); p.set_defaults(func=merge_review_events)
    p = sub.add_parser("record-author-response"); p.add_argument("--run-dir", required=True); p.add_argument("--executive", required=True); p.add_argument("--responds-to", required=True); p.add_argument("--disposition", required=True); p.add_argument("--reason", required=True); p.add_argument("--change", required=True); p.set_defaults(func=record_author_response)
    p = sub.add_parser("record-veto"); p.add_argument("--run-dir", required=True); p.add_argument("--holder", required=True); p.add_argument("--stage", required=True); p.add_argument("--protected-domain", required=True); p.add_argument("--challenged-statement", required=True); p.add_argument("--reason", required=True); p.add_argument("--evidence", required=True); p.add_argument("--remedy", required=True); p.add_argument("--challenged-artifact"); p.add_argument("--challenged-section"); p.add_argument("--verification-method", default="contains_text"); p.add_argument("--remedy-must-contain"); p.set_defaults(func=record_veto)
    p = sub.add_parser("resolve-veto"); p.add_argument("--run-dir", required=True); p.add_argument("--veto-id", required=True); p.add_argument("--chairman-note"); p.set_defaults(func=resolve_veto)
    p = sub.add_parser("prepare-chairman-packet"); p.add_argument("--run-dir", required=True); p.add_argument("--allow-open-vetoes", action="store_true"); p.set_defaults(func=prepare_chairman_packet)
    p = sub.add_parser("record-first-synthesis"); p.add_argument("--run-dir", required=True); p.add_argument("--text", required=True); p.set_defaults(func=record_first_synthesis)
    p = sub.add_parser("record-devils-advocate"); p.add_argument("--run-dir", required=True); p.add_argument("--attack", required=True); p.add_argument("--defeating-change", required=True); p.set_defaults(func=record_devils_advocate)
    p = sub.add_parser("record-provisional-verdict"); p.add_argument("--run-dir", required=True); p.add_argument("--text", required=True); p.set_defaults(func=record_provisional_verdict)
    p = sub.add_parser("open-post-chair-review"); p.add_argument("--run-dir", required=True); p.set_defaults(func=open_post_chair_review)
    p = sub.add_parser("record-final-verdict"); p.add_argument("--run-dir", required=True); p.add_argument("--text", required=True); p.add_argument("--summary", required=True); p.add_argument("--next-action", required=True); p.set_defaults(func=record_final_verdict)
    p = sub.add_parser("validate-run"); p.add_argument("--run-dir", required=True); p.set_defaults(func=validate_run)
    p = sub.add_parser("resume"); p.add_argument("--run-dir", required=True); p.set_defaults(func=resume)
    p = sub.add_parser("complete-run"); p.add_argument("--run-dir", required=True); p.set_defaults(func=complete_run)
    p = sub.add_parser("status"); p.add_argument("--run-dir", required=True); p.set_defaults(func=status_cmd)
    p = sub.add_parser("validate-release-tree"); p.add_argument("--root", default="."); p.set_defaults(func=validate_release_tree)
    p = sub.add_parser("synthetic-test"); p.set_defaults(func=synthetic_test)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = args.func(args)
    if isinstance(result, Path):
        print(result)


if __name__ == "__main__":
    main()
