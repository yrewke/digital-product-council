# Architecture Overview

## Boundaries

Codex Council V2 lives under `codex-council-v2/` with a repository-local skill at `.agents/skills/codex-council-v2/` and separate agent profiles named `codex-council-v2-*`. It does not modify older restaurant council skills, older agent profiles, or historical run artifacts.

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

## File Ownership

- Executives own only their canonical memo files.
- Librarian owns evidence library, request routing, anonymized packets, and evidence response appends.
- Auditor owns audit files and fact-check records.
- Peer comments are written to controlled review files before deterministic merge.
- Chairman and Devil's Advocate never edit executive memos.
- Scripts use lock files under `_work/locks/` before deterministic writes.

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

See `config/model-routing-policy.md`. The current implementation records routing policy without hardcoding unavailable model names. If dynamic per-subagent routing is unavailable, the operator keeps one Codex session and applies the tier policy manually.

## Validation

`scripts/codex_council_v2.py validate-run` checks canonical executive files, event tags, evidence cache reuse, factual blocking and correction, anonymous peer review, scoped veto handling, Chairman stages, Devil's Advocate stage, resume state, final verdict, and preservation of older council roots.
