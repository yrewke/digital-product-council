# Architecture Overview

## Boundaries

Codex Council V2 lives under `codex-council-v2/` with a repository-local skill at `.agents/skills/codex-council-v2/` and separate agent profiles named `codex-council-v2-*`. It does not modify older restaurant council skills, older agent profiles, or historical run artifacts.

## Deterministic Workflow Engine

`scripts/codex_council_v2.py` owns the state machine, event ledger, event IDs, file locks, evidence cache lookup, anonymous review packet routing, review assignment completeness, deterministic review merges, veto-scope validation, veto remedy verification, audit consistency checks, resume guidance, and completion validation.

The legal stages are:

`CHARTER_DRAFTED`, `CHARTER_APPROVED`, `EVIDENCE_REQUESTS_OPEN`, `EVIDENCE_READY`, `MEMOS_DRAFTING`, `MEMOS_SUBMITTED`, `AUDIT_IN_PROGRESS`, `AUDIT_BLOCKED`, `AUDIT_PASSED`, `PEER_REVIEW_IN_PROGRESS`, `AUTHOR_REVISION`, `CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`, `EXTERNAL_CHAIRMAN_PROVISIONAL_PENDING`, `EXTERNAL_DEVILS_ADVOCATE_PENDING`, `EXTERNAL_CHAIRMAN_FINAL_PENDING`, `AWAITING_AHMED_DECISION`, `HUMAN_DECISION_RECORDED`.

Every transition is recorded in `RUN_EVENTS.jsonl`. Illegal transitions are rejected.

## Codex Reasoning Layer

Codex and the custom V2 agents own executive reasoning, evidence-question formulation, Librarian synthesis, Auditor judgment, peer-review comments, author revision text, final internal validation, and the external-role handoff package. External ChatGPT sessions own Chairman synthesis, Devil's Advocate attack, final Chairman verdict, and any later Ahmed-facing judgment. Codex must not write those external-role judgments.

For real runs, substantive reasoning is delegated to visible isolated Codex sub-agents when the session exposes sub-agent tools. The main Codex session acts as operator: it prepares bounded briefs, dispatches role agents, collects outputs, runs engine commands, and validates state.

The default real-run dispatch is:

- Five executives are spawned independently for first-pass memos: Contrarian, First-Principles Thinker, Expansionist, Outsider, and Executor.
- The Librarian is spawned for nontrivial evidence routing and cache/provenance work.
- The Auditor is spawned for factual and numerical review after claim extraction.
- No Chairman or Devil's Advocate Codex agent is registered or spawned. Those roles run in separate external ChatGPT conversations using the startup prompts in `templates/`.

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
9. Require genuine revised memos for accepted material objections.
10. Resolve or explicitly mark blocking factual/numerical defects.
11. Produce the external Chairman handoff package, external-role handoff manifest, completion report, and startup prompts.
12. Stop at `CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`.

## File Ownership and Merge Control

- Executives own only their canonical memo files.
- Librarian owns evidence library, request routing, anonymized packets, and evidence response appends.
- Auditor owns audit files and fact-check records.
- Peer comments are written to controlled review files before deterministic merge.
- External Chairman and Devil's Advocate artifacts are preserved under `external_chairman/` and `external_devils_advocate/` only when human-supplied through `record-external-artifact`.
- Codex-owned run space rejects substantive Chairman, Devil's Advocate, and final-verdict artifacts.
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

`scripts/codex_council_v2.py validate-run` checks canonical executive files, event tag grammar, evidence cache reuse, factual blocking and current-memo correction, evidence provenance, arithmetic issues, complete peer-review assignments, genuine accepted-objection revisions, anonymous peer review routing, scoped veto handling, veto remedy verification, prohibited external-role artifacts, handoff manifest/prompts, V2 entry points, and old-system hash preservation.

The test suite in `tests/test_engine.py` covers event parsing, cache deduplication, stage transitions, audit correction enforcement, expanded claim extraction, deterministic arithmetic checks, anonymous packet generation, review completeness and waivers, accepted-objection revision enforcement, veto scope and remedy verification, role-boundary violations, external artifact intake, legacy contamination, lock behavior, resume guidance, full synthetic handoff pipeline, and old-system hash preservation.
