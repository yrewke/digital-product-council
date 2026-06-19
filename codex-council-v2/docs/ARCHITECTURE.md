# Architecture Overview

## Boundaries

Codex Council V2 lives under `codex-council-v2/` with a repository-local skill at `.agents/skills/codex-council-v2/` and separate agent profiles named `codex-council-v2-*`. It does not modify older restaurant council skills, older agent profiles, or historical run artifacts.

## Deterministic Workflow Engine

`scripts/codex_council_v2.py` owns the state machine, event ledger, event IDs, file locks, evidence cache lookup, anonymous review packet routing, review assignment completeness, deterministic review merges, veto-scope validation, veto remedy verification, audit consistency checks, resume guidance, and completion validation.

The legal stages are:

`CHARTER_DRAFTED`, `CHARTER_APPROVED`, `EVIDENCE_REQUESTS_OPEN`, `EVIDENCE_READY`, `MEMOS_DRAFTING`, `MEMOS_SUBMITTED`, `AUDIT_IN_PROGRESS`, `AUDIT_BLOCKED`, `AUDIT_PASSED`, `PEER_REVIEW_IN_PROGRESS`, `AUTHOR_REVISION`, `PRE_CHAIR_READY`, `CHAIRMAN_SYNTHESIS`, `DEVILS_ADVOCATE_COMPLETE`, `PROVISIONAL_VERDICT`, `POST_CHAIR_VETO_REVIEW`, `FINAL_VERDICT_COMPLETE`, `RUN_COMPLETE`.

Every transition is recorded in `RUN_EVENTS.jsonl`. Illegal transitions are rejected.

## Codex Reasoning Layer

Codex and the custom V2 agents own executive reasoning, evidence-question formulation, Librarian synthesis, Auditor judgment, peer-review comments, author revision text, Chairman synthesis, and Devil's Advocate attack. Their outputs are submitted back through the deterministic engine before the run advances.

For real runs, substantive reasoning is delegated to visible isolated Codex sub-agents when the session exposes sub-agent tools. The main Codex session acts as operator: it prepares bounded briefs, dispatches role agents, collects outputs, runs engine commands, and validates state.

The default real-run dispatch is:

- Five executives are spawned independently for first-pass memos: Contrarian, First-Principles Thinker, Expansionist, Outsider, and Executor.
- The Librarian is spawned for nontrivial evidence routing and cache/provenance work.
- The Auditor is spawned for factual and numerical review after claim extraction.
- The Chairman is spawned for synthesis after peer review and veto handling.
- Devil's Advocate is spawned only after an emerging Chairman direction exists.

Sub-agents receive minimal context needed for their role: charter, status summary, role brief, relevant evidence or review packet, allowed files, forbidden actions, and output contract. They do not advance the state machine directly.

If sub-agent tools are unavailable, the operator may run a manual single-session fallback only after telling the user and labeling the run notes `MANUAL_SINGLE_SESSION_FALLBACK`.

## Workflow

1. Inspect repository governance and applicable scoped rules.
2. Create a run charter.
3. Collect independent evidence requests from the five executives.
4. Route requests through the Librarian cache and evidence library.
5. Draft exactly five canonical executive memos.
6. Run the Evidence Auditor gate.
7. Route anonymous peer review.
8. Let authors revise only their own memos.
9. Produce Chairman first synthesis.
10. Run Devil's Advocate attack.
11. Produce provisional verdict.
12. Run post-chair veto review.
13. Produce final verdict, completion report, and next-run handoff.

## File Ownership and Merge Control

- Executives own only their canonical memo files.
- Librarian owns evidence library, request routing, anonymized packets, and evidence response appends.
- Auditor owns audit files and fact-check records.
- Peer comments are written to controlled review files before deterministic merge.
- Chairman and Devil's Advocate never edit executive memos.
- Scripts use lock files under `_work/locks/` before deterministic writes. In the Windows sandbox, released locks are marked `RELEASED` instead of deleted.

## Evidence Memory

The reusable library lives under `codex-council-v2/library/` in real runs and under each test run for fixtures. It tracks source IDs, evidence IDs, request IDs, cache keys, classifications, limitations, dates, geography, and contradictions.

Evidence classifications:

- `VERIFIED_FACT`
- `INTERNAL_PROJECT_FACT`
- `SOURCE_BACKED_ESTIMATE`
- `VENDOR_CLAIM`
- `INDUSTRY_BENCHMARK`
- `SCENARIO_ASSUMPTION`
- `COUNCIL_INFERENCE`
- `USER_PREFERENCE`
- `CONTRADICTION`
- `UNKNOWN`

## Model Routing

See `config/model-routing-policy.md`. The implementation records routing policy without hardcoding unavailable model names. Visible isolated sub-agent dispatch is required for real runs when available; per-agent model overrides remain optional and must not be invented if the current Codex environment does not expose them.

## Validation

`scripts/codex_council_v2.py validate-run` checks canonical executive files, event tag grammar, evidence cache reuse, factual blocking and current-memo correction, complete peer-review assignments, anonymous peer review routing, scoped veto handling, veto remedy verification, Chairman stages, Devil's Advocate stage, final verdict, V2 entry points, and old-system hash preservation.

The test suite in `tests/test_engine.py` covers event parsing, cache deduplication, stage transitions, audit correction enforcement, expanded claim extraction, deterministic arithmetic checks, anonymous packet generation, review completeness and waivers, veto scope and remedy verification, lock behavior, resume guidance, full synthetic pipeline, and old-system hash preservation.
