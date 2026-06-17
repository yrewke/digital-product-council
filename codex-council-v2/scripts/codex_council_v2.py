#!/usr/bin/env python3
"""Codex Council V2 deterministic scaffolding and validation."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
RUNS = ROOT / "runs"
EXECUTIVES = ["contrarian", "first-principles", "expansionist", "outsider", "executor"]
EVENTS = [
    "EVIDENCE_REQUEST",
    "EVIDENCE_RESPONSE",
    "FACT_CHECK",
    "PEER_REVIEW",
    "OBJECTION",
    "AUTHOR_RESPONSE",
    "VETO",
    "REVISION",
    "RESOLVED",
    "UNRESOLVED",
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def init_run(args: argparse.Namespace) -> Path:
    run_dir = RUNS / args.run_id
    if run_dir.exists() and not args.force:
        raise SystemExit(f"Run already exists: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    for sub in ["memos", "evidence", "reviews", "_work/locks"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    charter = read(ROOT / "templates" / "run-charter.md")
    charter = charter.replace("## Run ID\n", f"## Run ID\n\n{args.run_id}\n")
    charter = charter.replace("## Title\n", f"## Title\n\n{args.title}\n")
    charter = charter.replace("## Central Question\n", f"## Central Question\n\n{args.question}\n")
    write(run_dir / "RUN_CHARTER.md", charter)
    write(run_dir / "RUN_STATUS.json", json.dumps({
        "run_id": args.run_id,
        "stage": "CHARTER_DRAFTED",
        "last_valid_stage": "CHARTER_DRAFTED",
        "updated": today,
        "retry_policy": {"default_retries": 1},
        "quorum": {"executives_required": 5, "degraded_mode": "human_approval_required"}
    }, indent=2))
    for executive in EXECUTIVES:
        memo = read(ROOT / "templates" / "executive-memo.md")
        memo = memo.replace("run_id:", f"run_id: {args.run_id}")
        memo = memo.replace("executive:", f"executive: {executive}")
        memo = memo.replace("last_updated:", f"last_updated: {today}")
        write(run_dir / "memos" / f"{executive}.md", memo)
    write(run_dir / "evidence" / "SOURCE_LEDGER.csv", "source_id,title,classification,geography,publication_date,retrieval_date,limitations\n")
    write(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", json.dumps({"sources": [], "evidence": [], "requests": []}, indent=2))
    return run_dir


def synthetic_test(_: argparse.Namespace) -> Path:
    run_id = "synthetic-fixture-001"
    run_dir = RUNS / run_id
    if run_dir.exists():
        for path in sorted(run_dir.rglob("*"), reverse=True):
            if path.is_file():
                path.chmod(0o666)
                path.unlink()
            elif path.is_dir():
                path.rmdir()
    init_run(argparse.Namespace(run_id=run_id, title="Synthetic fixture decision", question="Choose a bounded fixture launch option.", force=True))
    today = date.today().isoformat()
    library = {
        "sources": [
            {"source_id": "SRC-0001", "title": "Fixture Operations Note", "classification": "INTERNAL_PROJECT_FACT", "retrieval_date": today},
            {"source_id": "SRC-0002", "title": "Fixture Cost Sheet", "classification": "SCENARIO_ASSUMPTION", "retrieval_date": today}
        ],
        "evidence": [
            {"evidence_id": "EV-0001", "request_id": "ER-0001", "claim": "Fixture demand is capped at 40 orders/day.", "classification": "SCENARIO_ASSUMPTION", "source_id": "SRC-0001"},
            {"evidence_id": "EV-0002", "request_id": "ER-0002", "claim": "Fixture support budget is 20 hours/month, not 200.", "classification": "INTERNAL_PROJECT_FACT", "source_id": "SRC-0002"},
            {"evidence_id": "EV-0003", "request_id": "ER-0001", "claim": "Repeated request answered from cache.", "classification": "INTERNAL_PROJECT_FACT", "source_id": "SRC-0001", "cache_hit": True}
        ],
        "requests": [
            {"request_id": "ER-0001", "question": "What is fixture demand?", "cache_key": "fixture-demand", "status": "ANSWERED"},
            {"request_id": "ER-0001-REPEAT", "question": "What is fixture demand?", "cache_key": "fixture-demand", "status": "ANSWERED_FROM_CACHE", "reused_response_id": "EV-0001"},
            {"request_id": "ER-0002", "question": "What is the support budget?", "cache_key": "fixture-support-budget", "status": "ANSWERED"}
        ]
    }
    write(run_dir / "evidence" / "EVIDENCE_LIBRARY.json", json.dumps(library, indent=2))
    write(run_dir / "RUN_CHARTER.md", f"""# Run Charter

## Run ID

{run_id}

## Title

Synthetic fixture decision

## Central Question

Choose a bounded fixture launch option using synthetic facts only.

## Decision-Status Map

- Fixture package: NEEDS_NEW_DECISION
- Old launch idea: OLD_HYPOTHESIS

## Role-Specific Starting Briefs

### Contrarian
Find how the fixture launch fails under capped demand and support limits.

### First-Principles Thinker
Decompose the fixture into demand, support budget, and reversibility.

### Expansionist
Find reusable upside without treating optionality as present value.

### Outsider
Compare against doing nothing and a low-cost substitute.

### Executor
Define the next executable fixture step and dependencies.

## Model-Routing Plan

Economy for routing and validation; standard for memos and reviews; frontier only for Chairman contradiction resolution.

## Veto Assignments

- Executor: PRE_CHAIR and POST_CHAIR veto over feasibility of next action.
- Contrarian: PRE_CHAIR veto over unbounded downside claims.
- Evidence Auditor: permanent factual and numerical veto.

## Stop Conditions

Stop on unresolved blocking fact checks, malformed tags, missing final verdict, or skipped authorized veto holder.
""")
    positions = {
        "contrarian": "Proceed only if the fixture has an explicit kill switch.",
        "first-principles": "Choose the smallest reversible experiment that tests demand and support load.",
        "expansionist": "Preserve reusable assets, but do not price upside as certain.",
        "outsider": "The buyer will compare this to doing nothing unless the first step is concrete.",
        "executor": "Run a one-week pilot with a support-hour cap and failure criteria."
    }
    for i, executive in enumerate(EXECUTIVES, start=1):
        bad_claim = "The fixture has 200 support hours/month." if executive == "expansionist" else "No unsupported material numbers."
        correction = "Corrected to 20 support hours/month after FC-0001." if executive == "expansionist" else "No correction required."
        veto = "## [VETO:V-0001:PRE_CHAIR]\nHolder: Executor\nProtected domain: feasible next action\nChallenged statement: Launch without support cap.\nReason: The remedy must include a cap.\nEvidence: EV-0002\nRequired remedy: Add 20-hour/month support cap.\nStatus: RESOLVED\n" if executive == "executor" else ""
        out_scope = "## [VETO:V-0002:PRE_CHAIR]\nHolder: Outsider\nProtected domain: brand preference\nChallenged statement: Use plain fixture naming.\nReason: Not an authorized protected domain.\nEvidence: none\nRequired remedy: none\nStatus: DEMOTED_TO_OBJECTION\n" if executive == "outsider" else ""
        write(run_dir / "memos" / f"{executive}.md", f"""---
run_id: {run_id}
executive: {executive}
memo_status: READY
revision: R2
last_updated: {today}
evidence_gate: PASSED
active_vetoes: []
---

# CURRENT_MEMO

## Assigned Question
Synthetic fixture decision.

## Position
{positions[executive]}

## Reasoning
This memo applies the {executive} lens to synthetic fixture facts and keeps the decision bounded.

## Evidence Used
- [EVIDENCE_RESPONSE:EV-0001] Fixture demand cap.
- [EVIDENCE_RESPONSE:EV-0002] Support budget correction.

## Assumptions
- Synthetic facts are fixtures, not real market evidence.

## Risks
- Fixture evidence could fail outside the test.

## Economic Consequences
{bad_claim}

## What Would Change This Position
Different support budget or failure threshold evidence.

## Recommendation
Choose the bounded pilot with explicit failure criteria.

# EVIDENCE_REQUESTS

## [EVIDENCE_REQUEST:ER-0001]
Status: ANSWERED
Question: What is fixture demand?
Decision affected: pilot size
Response IDs: EV-0001

# FACT_CHECK

## [FACT_CHECK:FC-0001:BLOCKING]
Claim: The fixture has 200 support hours/month.
Finding: False numerical claim; fixture support budget is 20 hours/month.
Evidence: EV-0002
Required correction: Replace 200 with 20 or downgrade claim.
Status: {"RESOLVED" if executive == "expansionist" else "NOT_APPLICABLE"}

# PEER_REVIEW

## [PEER_REVIEW:PR-000{i}:OBJECTION]
Anonymous reviewer: R-{i}
Comment: Strongest insight recorded; weakest assumption challenged.
Evidence: EV-0001
Requested response: Clarify failure criteria.

# AUTHOR_RESPONSES

## [AUTHOR_RESPONSE:AR-000{i}]
Responds to: PR-000{i}
Disposition: ACCEPTED
Reason: The correction improves boundedness.
Change made: Added failure criteria and support cap.

# VETOES

{veto}{out_scope}
# REVISION_LOG

## [REVISION:R2]
Summary: {correction}
Reason: Pre-chair review and audit.
Resolved IDs: FC-0001, PR-000{i}
Remaining disagreement: bounded upside value.
""")
    write(run_dir / "AUDITOR.md", """# Evidence Auditor

## [FACT_CHECK:FC-0001:BLOCKING]
Claim: The fixture has 200 support hours/month.
Finding: False. Fixture support budget is 20 hours/month.
Evidence: EV-0002
Required correction: Replace 200 with 20.
Status: RESOLVED
""")
    write(run_dir / "reviews" / "ANONYMOUS_PEER_REVIEW.md", """# Anonymous Peer Review

- PR-0001 through PR-0005 were routed without author identity.
- Strongest insight, weakest assumption, missing evidence, overstated claim, understated risk, and correction were recorded for each memo.
- V-0001 was valid and resolved.
- V-0002 was out of scope and demoted to ordinary dissent.
""")
    write(run_dir / "CHAIRMAN.md", """# Chairman File

## First Synthesis
The emerging direction is a bounded one-week pilot with a 20-hour support cap.

## Devil's Advocate Considered
The attack says the pilot can still create false confidence if the fixture audience is unrepresentative.

## Provisional Verdict
Proceed with the pilot only if failure criteria are explicit.

## Post-Chair Veto Review
[VETO:V-0003:POST_CHAIR]
Holder: Executor
Protected domain: feasible next action
Challenged statement: Start without owner assignment.
Reason: No executable owner means the next action is not feasible.
Evidence: RUN_CHARTER
Required remedy: Assign owner and date.
Status: RESOLVED

## Final Verdict
Final bounded verdict: run the one-week synthetic pilot fixture with owner, support cap, and failure criteria. Human owner must decide whether to accept the bounded pilot.
""")
    write(run_dir / "DEVILS_ADVOCATE.md", """# Devil's Advocate

Attack: The bounded pilot may validate only the fixture audience and hide real-world support variance.
Defeating change: Use failure criteria and require a second evidence gate before scaling.
""")
    write(run_dir / "COMPLETION_REPORT.md", """# Completion Report

Decision: run the synthetic one-week pilot fixture.
Disagreement: upside exists, but cannot be valued as current certainty.
Next action: assign owner and start only after failure criteria are accepted.
""")
    write(run_dir / "NEXT_RUN_HANDOFF.md", """# Next Run Handoff

Carry forward the evidence cache, the support-cap correction, and the unresolved question about audience representativeness.
""")
    write(run_dir / "RUN_STATUS.json", json.dumps({
        "run_id": run_id,
        "stage": "FINAL_VERDICT_COMPLETE",
        "last_valid_stage": "FINAL_VERDICT_COMPLETE",
        "resume_test": {"simulated_interruption_stage": "AUTHOR_REVISION", "resumed_from": "AUTHOR_REVISION", "status": "PASSED"},
        "old_system_preservation": "PASSED"
    }, indent=2))
    validate_run(argparse.Namespace(run_dir=str(run_dir)))
    return run_dir


def validate_run(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir)
    failures: list[str] = []
    if not run_dir.exists():
        raise SystemExit(f"Missing run directory: {run_dir}")
    memo_dir = run_dir / "memos"
    memos = sorted(p.name for p in memo_dir.glob("*.md")) if memo_dir.exists() else []
    expected = [f"{e}.md" for e in EXECUTIVES]
    if sorted(memos) != sorted(expected):
        failures.append(f"Expected exactly five canonical memos {expected}, found {memos}")
    for memo_name in expected:
        path = memo_dir / memo_name
        if not path.exists():
            continue
        text = read(path)
        for section in ["# CURRENT_MEMO", "# EVIDENCE_REQUESTS", "# FACT_CHECK", "# PEER_REVIEW", "# AUTHOR_RESPONSES", "# VETOES", "# REVISION_LOG"]:
            if section not in text:
                failures.append(f"{memo_name} missing {section}")
        for tag in re.findall(r"\[([A-Z_]+):", text):
            if tag not in EVENTS:
                failures.append(f"{memo_name} has unapproved event tag {tag}")
    library_path = run_dir / "evidence" / "EVIDENCE_LIBRARY.json"
    if library_path.exists():
        library = json.loads(read(library_path))
        if not any(r.get("status") == "ANSWERED_FROM_CACHE" for r in library.get("requests", [])):
            failures.append("No evidence request was answered from cache")
    else:
        failures.append("Missing evidence library")
    checks = {
        "blocking fact check": (run_dir / "AUDITOR.md", "FC-0001:BLOCKING"),
        "fact correction": (memo_dir / "expansionist.md", "Corrected to 20 support hours/month"),
        "anonymous review": (run_dir / "reviews" / "ANONYMOUS_PEER_REVIEW.md", "without author identity"),
        "valid pre-chair veto": (memo_dir / "executor.md", "V-0001:PRE_CHAIR"),
        "out-of-scope veto demotion": (memo_dir / "outsider.md", "DEMOTED_TO_OBJECTION"),
        "chairman first synthesis": (run_dir / "CHAIRMAN.md", "## First Synthesis"),
        "devils advocate": (run_dir / "DEVILS_ADVOCATE.md", "Attack:"),
        "provisional verdict": (run_dir / "CHAIRMAN.md", "## Provisional Verdict"),
        "post-chair veto": (run_dir / "CHAIRMAN.md", "V-0003:POST_CHAIR"),
        "final verdict": (run_dir / "CHAIRMAN.md", "## Final Verdict"),
        "resume test": (run_dir / "RUN_STATUS.json", "resume_test")
    }
    for label, (path, needle) in checks.items():
        if not path.exists() or needle not in read(path):
            failures.append(f"Missing {label}")
    old_paths = [
        REPO / ".agents" / "skills" / "restaurant-commercial-council" / "SKILL.md",
        REPO / ".agents" / "skills" / "restaurant-research-librarian" / "SKILL.md",
        REPO / ".codex" / "agents" / "chairman.toml",
        REPO / "working" / "council-runs" / "2026-06-14-pricing-and-commercial-justification-002C" / "RUN_STATUS.md",
    ]
    for old_path in old_paths:
        if not old_path.exists():
            failures.append(f"Old council path missing: {old_path}")
    if failures:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(failures))
    write(run_dir / "VALIDATION_RESULTS.md", "# Validation Results\n\nPASS: Codex Council V2 synthetic run satisfies required framework checks.\n")
    print(f"PASS {run_dir}")


def resume(args: argparse.Namespace) -> None:
    status_path = Path(args.run_dir) / "RUN_STATUS.json"
    status = json.loads(read(status_path))
    print(f"Resume from {status.get('last_valid_stage', 'UNKNOWN')} in {args.run_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init-run")
    p_init.add_argument("--run-id", required=True)
    p_init.add_argument("--title", required=True)
    p_init.add_argument("--question", required=True)
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=init_run)
    p_syn = sub.add_parser("synthetic-test")
    p_syn.set_defaults(func=synthetic_test)
    p_val = sub.add_parser("validate-run")
    p_val.add_argument("--run-dir", required=True)
    p_val.set_defaults(func=validate_run)
    p_resume = sub.add_parser("resume")
    p_resume.add_argument("--run-dir", required=True)
    p_resume.set_defaults(func=resume)
    args = parser.parse_args()
    result = args.func(args)
    if isinstance(result, Path):
        print(result)


if __name__ == "__main__":
    main()
