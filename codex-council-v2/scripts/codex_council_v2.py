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
SERVICES = ["librarian", "auditor"]
EXTERNAL_ROLES = ["external_chairman", "external_devils_advocate", "ahmed"]

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
    "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN",
    "EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING",
    "EXTERNAL_DEVILS_ADVOCATE_PENDING",
    "EXTERNAL_CHAIRMAN_FINAL_PENDING",
    "AWAITING_AHMED_DECISION",
    "HUMAN_DECISION_RECORDED",
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
    "AUTHOR_REVISION": ["CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN"],
    "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN": ["EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING"],
    "EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING": ["EXTERNAL_DEVILS_ADVOCATE_PENDING"],
    "EXTERNAL_DEVILS_ADVOCATE_PENDING": ["EXTERNAL_CHAIRMAN_FINAL_PENDING"],
    "EXTERNAL_CHAIRMAN_FINAL_PENDING": ["AWAITING_AHMED_DECISION"],
    "AWAITING_AHMED_DECISION": ["HUMAN_DECISION_RECORDED"],
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
]

FORBIDDEN_INTERNAL_ARTIFACT_PATTERNS = [
    r"^CHAIRMAN(?:_.*|\.MD|$)",
    r"^CHAIRMAN_FIRST_SYNTHESIS\.MD$",
    r"^CHAIRMAN_PROVISIONAL_VERDICT\.MD$",
    r"^CHAIRMAN_FINAL.*\.MD$",
    r"^FINAL_COMMERCIAL_.*VERDICT\.MD$",
    r"^.*FINAL.*VERDICT.*\.MD$",
    r"^DEVILS_ADVOCATE(?:_.*|\.MD|$)",
    r"^DEVILS_ADVOCATE_ATTACK\.MD$",
]

ALLOWED_EXTERNAL_TEMPLATE_NAMES = {
    "START_EXTERNAL_CHAIRMAN_SESSION.md",
    "START_EXTERNAL_DEVILS_ADVOCATE_SESSION.md",
    "RETURN_TO_EXTERNAL_CHAIRMAN_AFTER_ATTACK.md",
    "EXTERNAL_ROLE_HANDOFF_MANIFEST_TEMPLATE.md",
}

LEGACY_INVALID_MARKER = "INVALID_ROLE_BOUNDARY_CROSSING_NOT_AUTHORITATIVE"
LEGACY_INVALIDATION_PATTERNS = [
    r".*CHAIRMAN.*(?:SYNTHESIS|VERDICT).*\.md$",
    r".*DEVILS?_ADVOCATE.*(?:ATTACK|MEMO)?.*\.md$",
    r".*FINAL.*VERDICT.*\.md$",
    r".*chairman-verdict\.md$",
    r".*devils-advocate\.md$",
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
    for name in ["chairman", "devils-advocate"]:
        if (root / ".codex" / "agents" / f"codex-council-v2-{name}.toml").exists():
            failures.append(f"Forbidden executable external-role agent registered: .codex/agents/codex-council-v2-{name}.toml")
    return failures


def legacy_role_boundary_records(root: Path = ROOT) -> list[dict[str, Any]]:
    archive = root / "library" / "legacy-council-import" / "source-archive"
    if not archive.exists():
        return []
    records = []
    for path in archive.rglob("*.md"):
        rel = durable_relpath(path, root)
        normalized = rel.replace("\\", "/")
        if any(re.fullmatch(pattern, normalized, re.I) for pattern in LEGACY_INVALIDATION_PATTERNS):
            records.append({
                "path": normalized,
                "sha256": sha256(path),
                "marker": LEGACY_INVALID_MARKER,
                "authoritative_by_default": False,
                "reason": "Codex-generated Chairman, Devil's Advocate, or final-verdict artifact from a pre-repair role-boundary-crossing run; preserved for audit history only.",
            })
    return sorted(records, key=lambda r: r["path"])


def mark_legacy_role_boundary_crossings(args: argparse.Namespace) -> None:
    root = run_dir_arg(args.root) if getattr(args, "root", None) else ROOT
    records = legacy_role_boundary_records(root)
    target = root / "library" / "legacy-council-import" / "INVALID_ROLE_BOUNDARY_CROSSINGS.json"
    save_json(target, {"marker": LEGACY_INVALID_MARKER, "records": records})
    lines = [
        "# Invalid Legacy External-Role Simulations",
        "",
        f"Marker: `{LEGACY_INVALID_MARKER}`",
        "",
        "These imported historical artifacts are preserved for audit history but must not be loaded as authoritative external Chairman, Devil's Advocate, final commercial verdict, or Ahmed decision artifacts by default.",
        "",
    ]
    for record in records:
        lines.append(f"- `{record['path']}` - {record['marker']}")
    write(root / "library" / "legacy-council-import" / "INVALID_ROLE_BOUNDARY_CROSSINGS.md", "\n".join(lines) + "\n")
    print(f"MARKED {len(records)} legacy role-boundary artifacts")


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
            "standard": "manual fallback in current Codex session; use for ordinary memos, audit, and reviews",
            "frontier": "active Codex model from doctor output when available; reserve for hard internal contradictions only",
            "verified_environment": "Codex Doctor observed model gpt-5.5 on this workstation; per-agent model keys are not guaranteed by local TOML support.",
        },
        "veto_assignments": {
            "executor": [
                {"stage": "PRE_CHAIR", "protected_domain": "feasible next action"},
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

Codex stops after five revised executive memos, completed evidence/audit/review/veto gates, the external Chairman handoff manifest, and reusable external role startup prompts exist. The terminal Codex-owned state is `CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`; Codex must not generate Chairman, Devil's Advocate, final verdict, or Ahmed decision artifacts.
"""


def init_run(args: argparse.Namespace) -> Path:
    run_dir = RUNS / args.run_id
    if run_dir.exists():
        if not args.force:
            raise SystemExit(f"Run already exists: {run_dir}")
        shutil.rmtree(run_dir)
    for sub in ["codex_internal", "external_chairman", "external_devils_advocate", "human_decision", "handoff", "templates", "memos", "evidence", "reviews", "_work/locks", "_work/review-packets", "_work/merge-queue"]:
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


def external_prompt_templates() -> dict[str, str]:
    return {
        "START_EXTERNAL_CHAIRMAN_SESSION.md": """# Start External Chairman Session

## Stable Role

You are the independent external ChatGPT Chairman for Ahmed's second council system. You are not Codex, not an executive memo author, not the Devil's Advocate, and not Ahmed.

## Run Variables

- Run ID: `{{RUN_ID}}`
- Run mission: `{{RUN_MISSION}}`
- Handoff package path or uploaded files: `{{HANDOFF_PACKAGE_PATH}}`
- Expected artifact list: `{{EXPECTED_ARTIFACT_LIST}}`
- Historical context file: `{{HISTORICAL_CONTEXT_FILE}}`
- Current decision questions: `{{CURRENT_DECISION_QUESTIONS}}`
- Known unresolved gaps: `{{UNRESOLVED_GAPS}}`

## Context

Ahmed is evaluating a restaurant direct-ordering product and related commercial decisions. Codex has already run the internal council only: five independent executive lenses, research/librarian routing, evidence and arithmetic audit, anonymous peer review, author revisions, scoped veto handling, and final internal validation.

## Required Process

1. Inventory the uploaded/path-listed files before analysis.
2. Verify that five revised executive memos, evidence provenance, numerical ledger/model files where applicable, peer reviews, author responses, audit report, unresolved defects, and the handoff manifest are present or explicitly marked missing.
3. Distinguish facts, estimates, assumptions, decisions, and pilot-validation requirements.
4. Inspect arithmetic and evidence before synthesizing.
5. Preserve material disagreement and uncertainty instead of smoothing it away.
6. Do not invent missing artifacts or fill missing evidence as fact.
7. Produce a provisional consolidated Chairman memo only.

## Prohibited Actions

- Do not act as the Devil's Advocate.
- Do not issue a final Chairman verdict.
- Do not claim Ahmed has decided.
- Do not create guaranteed ROI claims, aggregator-replacement claims, hidden pass-through costs, or universal integration promises.

## Required Output

Produce `CHAIRMAN_PROVISIONAL_MEMO` with: file inventory, process completeness check, agreement/disagreement map, evidence/arithmetic caveats, provisional synthesis, rejected or uncertain claims, required Devil's Advocate focus areas, and questions for Ahmed.

## Stop Condition

Stop after the provisional consolidated Chairman memo and request a separate external Devil's Advocate stage. Ahmed remains the final human authority.
""",
        "START_EXTERNAL_DEVILS_ADVOCATE_SESSION.md": """# Start External Devil's Advocate Session

## Stable Role

You are acting only as the independent external ChatGPT Devil's Advocate. Your primary target is the Chairman's provisional consolidated memo, not the five executive memos as a new executive reviewer.

## Run Variables

- Run ID: `{{RUN_ID}}`
- Chairman provisional memo: `{{CHAIRMAN_PROVISIONAL_MEMO}}`
- Codex handoff package: `{{CODEX_HANDOFF_PACKAGE}}`
- Protected decision domains: `{{PROTECTED_DECISION_DOMAINS}}`
- Known unresolved evidence gaps: `{{UNRESOLVED_GAPS}}`

## Required Process

1. Read the Chairman provisional memo first.
2. Inspect Codex evidence, audit, ledger, models, peer reviews, and revised memos only as needed to test the Chairman's claims.
3. Attack assumptions, arithmetic, evidence quality, sequencing, implementation realism, pricing, affordability, ROI logic, delivery/support logic, and failure modes.
4. Distinguish fatal defects from ordinary uncertainty and from pilot-testable risks.
5. Preserve contradictions and identify what evidence or model change would defeat each objection.

## Prohibited Actions

- Do not rewrite all five executive memos.
- Do not act as Chairman.
- Do not issue a final verdict.
- Do not claim Ahmed has decided.

## Required Output

Produce `DEVILS_ADVOCATE_ATTACK` with: target claim, objection, severity, evidence basis, arithmetic check, implementation failure mode, what would change the objection, and recommended return questions for the Chairman.

## Stop Condition

Stop after the structured attack for return to the external Chairman. Ahmed remains the final human authority.
""",
        "RETURN_TO_EXTERNAL_CHAIRMAN_AFTER_ATTACK.md": """# Return To External Chairman After Attack

## Stable Role

You are returning as the independent external ChatGPT Chairman after receiving the Devil's Advocate attack. You are not Codex, not the Devil's Advocate, and not Ahmed.

## Run Variables

- Run ID: `{{RUN_ID}}`
- Prior Chairman provisional memo: `{{CHAIRMAN_PROVISIONAL_MEMO}}`
- Devil's Advocate attack: `{{DEVILS_ADVOCATE_ATTACK}}`
- Codex handoff package: `{{CODEX_HANDOFF_PACKAGE}}`
- Scoped vetoes or protected domains: `{{SCOPED_VETOES}}`
- Known unresolved gaps: `{{UNRESOLVED_GAPS}}`

## Required Process

1. Read the Devil's Advocate attack in full.
2. Classify each material objection as accepted, partially accepted, rejected, or unresolved.
3. Give reasons and cite the relevant evidence, arithmetic, model, or assumption boundary.
4. Revise the commercial model or decision logic where required.
5. Review valid scoped vetoes and preserve unresolved issues.
6. Separate what is decided, provisional, rejected, superseded, and awaiting pilot validation.
7. State which decisions remain for Ahmed.

## Prohibited Actions

- Do not claim the whole external process is complete until Ahmed has reviewed the verdict.
- Do not hide pass-through costs, unsupported assumptions, or missing integrations.
- Do not turn pilot-validation requirements into facts.

## Required Output

Produce `CHAIRMAN_FINAL_VERDICT_FOR_AHMED_REVIEW` with objection-by-objection disposition, revised synthesis, final Chairman recommendation, assumptions, estimates, pilot-validation requirements, and Ahmed decision points.

## Stop Condition

Stop after the final Chairman verdict for Ahmed review. Ahmed remains the final human authority.
""",
        "EXTERNAL_ROLE_HANDOFF_MANIFEST_TEMPLATE.md": """# External Role Handoff Manifest

- Run ID: `{{RUN_ID}}`
- Mission: `{{RUN_MISSION}}`
- Codex completion status: `CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`
- Files included: `{{HANDOFF_FILE_LIST}}`
- Files missing: `{{FILES_MISSING}}`
- Research quota status: `{{RESEARCH_QUOTA_STATUS}}`
- Notebook status: `{{NOTEBOOK_STATUS}}`
- Web-research status: `{{WEB_RESEARCH_STATUS}}`
- Executive memo revisions: `{{EXECUTIVE_MEMO_REVISIONS}}`
- Audit status: `{{AUDIT_STATUS}}`
- Unresolved defects: `{{UNRESOLVED_DEFECTS}}`
- Numerical-ledger status: `{{NUMERICAL_LEDGER_STATUS}}`
- Models included: `{{MODELS_INCLUDED}}`
- Known stale artifacts: `{{KNOWN_STALE_ARTIFACTS}}`
- Required next external role: `External ChatGPT Chairman`
- Codex stop instruction: Codex has stopped and must not generate Chairman, Devil's Advocate, final verdict, or Ahmed decision content.
""",
    }


def write_external_prompt_templates(run_dir: Path) -> None:
    for name, text in external_prompt_templates().items():
        write(run_dir / "templates" / name, text)


def handoff_file_list(run_dir: Path) -> list[str]:
    candidates = [
        "RUN_CHARTER.md",
        "RUN_CONFIG.json",
        "RUN_STATUS.json",
        "RUN_EVENTS.jsonl",
        "CLAIMS.json",
        "FACT_CHECKS.json",
        "AUDITOR.md",
        "VETOES.json",
        "reviews/ANONYMOUS_PEER_REVIEW.md",
        "reviews/PEER_REVIEWS.json",
        "evidence/EVIDENCE_LIBRARY.json",
        "evidence/SOURCE_LEDGER.csv",
    ]
    candidates.extend(f"memos/{executive}.md" for executive in EXECUTIVES)
    return [path for path in candidates if (run_dir / path).exists()]


def prepare_chairman_packet(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    vetoes = load_json(run_dir / "VETOES.json", [])
    open_valid = [v["veto_id"] for v in vetoes if v.get("valid") and v.get("status") == "OPEN"]
    if open_valid and not args.allow_open_vetoes:
        raise SystemExit(f"Open valid vetoes remain: {', '.join(open_valid)}")
    transition(run_dir, "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN", "internal council handoff complete")
    packet = ["# External Chairman Handoff Package\n"]
    packet.append("Status: CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN\n")
    packet.append("No Chairman verdict has been produced. No Devil's Advocate attack has been produced. The commercial decision is not final.\n")
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
    write(run_dir / "handoff" / "EXTERNAL_CHAIRMAN_HANDOFF_PACKAGE.md", "\n".join(packet))
    write_external_prompt_templates(run_dir)
    manifest = external_prompt_templates()["EXTERNAL_ROLE_HANDOFF_MANIFEST_TEMPLATE.md"]
    manifest = manifest.replace("{{RUN_ID}}", status(run_dir).get("run_id", ""))
    manifest = manifest.replace("{{RUN_MISSION}}", load_json(run_dir / "RUN_CONFIG.json", {}).get("question", ""))
    manifest = manifest.replace("{{HANDOFF_FILE_LIST}}", "\n  - " + "\n  - ".join(handoff_file_list(run_dir)))
    manifest = manifest.replace("{{FILES_MISSING}}", "None detected by Codex validator")
    manifest = manifest.replace("{{RESEARCH_QUOTA_STATUS}}", "See evidence/EVIDENCE_LIBRARY.json requests")
    manifest = manifest.replace("{{NOTEBOOK_STATUS}}", "No NotebookLM query performed unless separately recorded in evidence")
    manifest = manifest.replace("{{WEB_RESEARCH_STATUS}}", "No web research performed unless separately recorded in evidence")
    manifest = manifest.replace("{{EXECUTIVE_MEMO_REVISIONS}}", "See memos/*.md REVISION_LOG sections")
    manifest = manifest.replace("{{AUDIT_STATUS}}", "Final Evidence Auditor report complete or unresolved defects listed")
    manifest = manifest.replace("{{UNRESOLVED_DEFECTS}}", json.dumps([v for v in vetoes if v.get("valid") and v.get("status") != "RESOLVED"], indent=2))
    manifest = manifest.replace("{{NUMERICAL_LEDGER_STATUS}}", "Claims and material values recorded in CLAIMS.json; model files listed where included")
    manifest = manifest.replace("{{MODELS_INCLUDED}}", ", ".join(str(p.relative_to(run_dir)).replace("\\", "/") for p in run_dir.rglob("*MODEL*") if p.is_file()) or "None")
    manifest = manifest.replace("{{KNOWN_STALE_ARTIFACTS}}", "Legacy invalid role-boundary simulations are excluded by default")
    write(run_dir / "handoff" / "EXTERNAL_ROLE_HANDOFF_MANIFEST.md", manifest)
    write(run_dir / "COMPLETION_REPORT.md", "# Codex Internal Completion Report\n\nInternal council work is complete.\n\nNo Chairman verdict has been produced.\n\nNo Devil's Advocate attack has been produced.\n\nThe package is awaiting external ChatGPT Chairman review.\n\nThe commercial decision is not final; commercial decision is not final.\n")
    update_status(run_dir, pending_tasks=["external ChatGPT Chairman review"], release_gate="AWAITING_EXTERNAL_CHAIRMAN")
    event(run_dir, "CODEX_HANDOFF_PREPARED", {"handoff": "handoff/EXTERNAL_CHAIRMAN_HANDOFF_PACKAGE.md"})
    print("PREPARED external chairman handoff")


def record_first_synthesis(args: argparse.Namespace) -> None:
    raise SystemExit("Forbidden role boundary crossing: Codex must not record Chairman synthesis. Use external_chairman/ with human-supplied artifacts.")


def record_devils_advocate(args: argparse.Namespace) -> None:
    raise SystemExit("Forbidden role boundary crossing: Codex must not record Devil's Advocate attacks. Use external_devils_advocate/ with human-supplied artifacts.")


def record_provisional_verdict(args: argparse.Namespace) -> None:
    raise SystemExit("Forbidden role boundary crossing: Codex must not record Chairman provisional verdicts.")


def open_post_chair_review(args: argparse.Namespace) -> None:
    raise SystemExit("Forbidden role boundary crossing: post-Chair review belongs to the external Chairman process.")


def record_final_verdict(args: argparse.Namespace) -> None:
    raise SystemExit("Forbidden role boundary crossing: Codex must not record final Chairman or commercial verdicts.")


def validate_event_tags(text: str, label: str) -> list[str]:
    failures = []
    for keyword, ident in re.findall(r"\[([A-Z_]+):([^:\]]+)", text):
        if keyword not in EVENT_KEYWORDS:
            failures.append(f"{label} has unapproved event tag {keyword}")
        elif not re.fullmatch(EVENT_KEYWORDS[keyword], ident):
            failures.append(f"{label} has malformed {keyword} id {ident}")
    return failures


def is_forbidden_internal_artifact(path: Path, run_dir: Path) -> bool:
    rel = path.relative_to(run_dir)
    parts = rel.parts
    if parts and parts[0] in {"templates", "handoff", "external_chairman", "external_devils_advocate", "human_decision", "library"}:
        return False
    if path.name in ALLOWED_EXTERNAL_TEMPLATE_NAMES:
        return False
    upper = path.name.upper()
    return any(re.fullmatch(pattern, upper) for pattern in FORBIDDEN_INTERNAL_ARTIFACT_PATTERNS)


def forbidden_internal_artifact_failures(run_dir: Path) -> list[str]:
    failures = []
    for path in run_dir.rglob("*.md"):
        if is_forbidden_internal_artifact(path, run_dir):
            failures.append(f"Forbidden Codex-generated external-role artifact in internal run space: {durable_relpath(path, run_dir)}")
    return failures


def revision_number(text: str) -> int:
    nums = [int(n) for n in re.findall(r"\[REVISION:R([0-9]+)\]", text)]
    return max(nums) if nums else 0


def peer_review_revision_failures(run_dir: Path) -> list[str]:
    failures: list[str] = []
    reviews = load_json(run_dir / "reviews" / "PEER_REVIEWS.json", [])
    responses = load_json(run_dir / "AUTHOR_RESPONSES.json", [])
    accepted = [r for r in responses if str(r.get("disposition", "")).upper() in {"ACCEPTED", "PARTIALLY_ACCEPTED"}]
    for response in accepted:
        target = response.get("responds_to", "")
        if not target.startswith("PR-"):
            continue
        review = next((r for r in reviews if r.get("review_id") == target), None)
        if not review or review.get("type") != "OBJECTION":
            continue
        executive = response.get("executive")
        source_memo = review.get("source_memo")
        if executive != source_memo:
            failures.append(f"{response['author_response_id']} responds to {target} for {source_memo} from wrong executive {executive}")
            continue
        memo_path = run_dir / "memos" / f"{executive}.md"
        text = read(memo_path) if memo_path.exists() else ""
        if revision_number(text) < 2:
            failures.append(f"{executive} accepted {target} but memo has no R2+ revision")
        if "# REVISION_LOG" not in text or target not in text:
            failures.append(f"{executive} accepted {target} but revision log does not reference the objection")
        current = current_memo(text)
        if response.get("change") and response["change"] not in current and "append" in response["change"].lower():
            failures.append(f"{executive} accepted {target} with append-only response; substantive CURRENT_MEMO change required")
    material_objections = [r for r in reviews if r.get("type") == "OBJECTION"]
    for review in material_objections:
        if not any(r.get("responds_to") == review["review_id"] for r in responses):
            failures.append(f"{review['review_id']} material peer-review objection has no author disposition")
    return failures


def evidence_provenance_failures(run_dir: Path) -> list[str]:
    failures: list[str] = []
    lib = load_json(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", {})
    sources = {s.get("source_id"): s for s in lib.get("sources", [])}
    for ev in lib.get("evidence", []):
        source = sources.get(ev.get("source_id"), {})
        title = source.get("title", "")
        limitations = source.get("limitations", "")
        if ev.get("answer_source") == "local source" and (not title or not limitations or limitations.lower() in {"local source", "unknown", "n/a"}):
            failures.append(f"{ev.get('evidence_id')} uses local source without traceable provenance")
        for field in ["classification", "geography"]:
            if not ev.get(field):
                failures.append(f"{ev.get('evidence_id')} missing {field}")
    return failures


def validate_run(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    failures: list[str] = []
    failures.extend(forbidden_internal_artifact_failures(run_dir))
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
    failures.extend(evidence_provenance_failures(run_dir))
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
    failures.extend(peer_review_revision_failures(run_dir))
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
    for path in ["handoff/EXTERNAL_CHAIRMAN_HANDOFF_PACKAGE.md", "handoff/EXTERNAL_ROLE_HANDOFF_MANIFEST.md", "COMPLETION_REPORT.md", "RUN_EVENTS.jsonl"]:
        if not (run_dir / path).exists():
            failures.append(f"Missing {path}")
    for name in ALLOWED_EXTERNAL_TEMPLATE_NAMES:
        if not (run_dir / "templates" / name).exists():
            failures.append(f"Missing external prompt template templates/{name}")
    report = read(run_dir / "COMPLETION_REPORT.md") if (run_dir / "COMPLETION_REPORT.md").exists() else ""
    for required in ["No Chairman verdict has been produced", "No Devil's Advocate attack has been produced", "awaiting external ChatGPT Chairman review", "commercial decision is not final"]:
        if required not in report:
            failures.append(f"Completion report missing boundary statement: {required}")
    if status(run_dir).get("stage") != "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN":
        failures.append("Run is not at CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN")
    failures.extend(verify_old_hashes(run_dir))
    for agent in [REPO / ".agents" / "skills" / "codex-council-v2" / "SKILL.md", *[REPO / ".codex" / "agents" / f"codex-council-v2-{name}.toml" for name in REQUIRED_V2_AGENT_NAMES]]:
        if not agent.exists():
            failures.append(f"Missing V2 entry point: {agent}")
    for removed in ["chairman", "devils-advocate"]:
        path = REPO / ".codex" / "agents" / f"codex-council-v2-{removed}.toml"
        if path.exists():
            failures.append(f"Forbidden executable external-role V2 agent still registered: {path}")
    if failures:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(failures))
    write(run_dir / "VALIDATION_RESULTS.md", "# Validation Results\n\nPASS: Codex internal state machine, cache, audit, peer review, revision, veto, handoff, prompt-template, role-boundary, and old-system hash checks passed.\n")
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
        "AUTHOR_REVISION": "record-author-response, record-veto, resolve-veto, then prepare-chairman-packet",
        "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN": "validate-run; then Ahmed starts external ChatGPT Chairman session",
        "EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING": "await human-supplied external Chairman provisional memo",
        "EXTERNAL_DEVILS_ADVOCATE_PENDING": "await human-supplied external Devil's Advocate attack",
        "EXTERNAL_CHAIRMAN_FINAL_PENDING": "await human-supplied external Chairman final verdict",
        "AWAITING_AHMED_DECISION": "await Ahmed decision",
        "HUMAN_DECISION_RECORDED": "no pending workflow",
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
        "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN": "external ChatGPT Chairman, not Codex",
        "EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING": "external ChatGPT Chairman",
        "EXTERNAL_DEVILS_ADVOCATE_PENDING": "external ChatGPT Devil's Advocate",
        "EXTERNAL_CHAIRMAN_FINAL_PENDING": "external ChatGPT Chairman",
        "AWAITING_AHMED_DECISION": "Ahmed",
        "HUMAN_DECISION_RECORDED": "none",
    }
    required_inputs = {
        "EVIDENCE_REQUESTS_OPEN": ["RUN_CHARTER.md", "RUN_CONFIG.json", "evidence/EVIDENCE_LIBRARY.json"],
        "EVIDENCE_READY": ["RUN_CHARTER.md", "evidence/EVIDENCE_LIBRARY.json"],
        "AUDIT_IN_PROGRESS": ["memos/*.md", "evidence/EVIDENCE_LIBRARY.json", "CLAIMS.json"],
        "PEER_REVIEW_IN_PROGRESS": ["_work/review-packets/*.md", "_work/review-routing-map.private.json"],
        "AUTHOR_REVISION": ["memos/*.md", "reviews/PEER_REVIEWS.json", "VETOES.json"],
        "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN": ["handoff/EXTERNAL_CHAIRMAN_HANDOFF_PACKAGE.md", "handoff/EXTERNAL_ROLE_HANDOFF_MANIFEST.md", "templates/*.md"],
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


def record_external_artifact(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    source = Path(args.content_file)
    if not source.exists():
        raise SystemExit(f"External artifact file not found: {source}")
    text = read(source)
    if args.role == "chairman-provisional":
        if status(run_dir).get("stage") != "CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN":
            raise SystemExit("Chairman provisional artifact can only be recorded after Codex handoff")
        target = run_dir / "external_chairman" / "CHAIRMAN_PROVISIONAL_MEMO.md"
        transition(run_dir, "EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING", "human supplied external Chairman provisional memo")
        transition(run_dir, "EXTERNAL_DEVILS_ADVOCATE_PENDING", "await external Devil's Advocate attack")
    elif args.role == "devils-advocate":
        if status(run_dir).get("stage") != "EXTERNAL_DEVILS_ADVOCATE_PENDING":
            raise SystemExit("Devil's Advocate artifact requires external Chairman provisional memo first")
        target = run_dir / "external_devils_advocate" / "DEVILS_ADVOCATE_ATTACK.md"
        transition(run_dir, "EXTERNAL_CHAIRMAN_FINAL_PENDING", "human supplied external Devil's Advocate attack")
    elif args.role == "chairman-final":
        if status(run_dir).get("stage") != "EXTERNAL_CHAIRMAN_FINAL_PENDING":
            raise SystemExit("Chairman final artifact requires external Devil's Advocate attack first")
        target = run_dir / "external_chairman" / "CHAIRMAN_FINAL_VERDICT_FOR_AHMED_REVIEW.md"
        transition(run_dir, "AWAITING_AHMED_DECISION", "human supplied external Chairman final verdict")
    elif args.role == "ahmed-decision":
        if status(run_dir).get("stage") != "AWAITING_AHMED_DECISION":
            raise SystemExit("Ahmed decision requires external Chairman final verdict first")
        target = run_dir / "human_decision" / "AHMED_DECISION.md"
        transition(run_dir, "HUMAN_DECISION_RECORDED", "human supplied Ahmed decision")
    else:
        raise SystemExit(f"Unknown external role: {args.role}")
    write(target, text)
    event(run_dir, "HUMAN_SUPPLIED_EXTERNAL_ARTIFACT_RECORDED", {"role": args.role, "path": durable_relpath(target, run_dir)})
    update_status(run_dir, pending_tasks=[])
    print(f"RECORDED human-supplied external artifact {durable_relpath(target, run_dir)}")


def complete_run(args: argparse.Namespace) -> None:
    run_dir = run_dir_arg(args.run_dir)
    validate_run(argparse.Namespace(run_dir=str(run_dir)))
    update_status(
        run_dir,
        pending_tasks=["external ChatGPT Chairman review"],
        release_gate="CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN",
    )
    print(f"CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN {run_dir}")


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
        record_peer_review_record(run_dir, route["packet_id"], "Clarify failure criteria and support cap.", objection=False)
    merge_review_events(argparse.Namespace(run_dir=str(run_dir)))
    valid_veto = record_veto_record(run_dir, "executor", "PRE_CHAIR", "feasible next action", "Launch without support cap.", "A launch without the support cap violates feasible next action.", ev2["evidence_id"], "Add the 20-hour/month support cap before Chairman review.", challenged_artifact="memos/executor.md", challenged_section="CURRENT_MEMO", remedy_must_contain="20-hour/month support cap before launch")
    invalid_veto = record_veto_record(run_dir, "outsider", "PRE_CHAIR", "brand preference", "Synthetic fixture decision.", "Plain naming is less attractive.", "none", "Rename the fixture.")
    executor_remedied = memo_text(run_id, "executor", "Run a one-week pilot with a 20-hour/month support cap before launch and explicit failure criteria.", "Executor fixture reasoning from role-specific prompt.", "Scenario assumption: the pilot requires 20 support hours/month and one owner. 20% of AED 200 is AED 40. A margin with revenue AED 100 and cost AED 60 is 40%.", ["EV-0001", ev2["evidence_id"]], "R3")
    submit_memo_record(run_dir, "executor", executor_remedied)
    resolve_veto_record(run_dir, valid_veto["veto_id"])
    record_author_response_record(run_dir, "executor", valid_veto["veto_id"], "ACCEPTED", "Support cap added.", "Resolved valid pre-chair veto.")
    resume(argparse.Namespace(run_dir=str(run_dir)))
    prepare_chairman_packet(argparse.Namespace(run_dir=str(run_dir), allow_open_vetoes=False))
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
    p = sub.add_parser("record-external-artifact"); p.add_argument("--run-dir", required=True); p.add_argument("--role", required=True, choices=["chairman-provisional", "devils-advocate", "chairman-final", "ahmed-decision"]); p.add_argument("--content-file", required=True); p.set_defaults(func=record_external_artifact)
    p = sub.add_parser("complete-run"); p.add_argument("--run-dir", required=True); p.set_defaults(func=complete_run)
    p = sub.add_parser("status"); p.add_argument("--run-dir", required=True); p.set_defaults(func=status_cmd)
    p = sub.add_parser("validate-release-tree"); p.add_argument("--root", default="."); p.set_defaults(func=validate_release_tree)
    p = sub.add_parser("mark-legacy-role-boundary-crossings"); p.add_argument("--root", default=str(ROOT)); p.set_defaults(func=mark_legacy_role_boundary_crossings)
    p = sub.add_parser("synthetic-test"); p.set_defaults(func=synthetic_test)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = args.func(args)
    if isinstance(result, Path):
        print(result)


if __name__ == "__main__":
    main()
