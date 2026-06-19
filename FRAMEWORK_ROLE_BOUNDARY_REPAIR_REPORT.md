# Framework Role Boundary Repair Report

## Cause Of Boundary Failure

The previous Codex Council V2 framework treated Chairman and Devil's Advocate as executable internal Codex service agents. The engine exposed commands that wrote `CHAIRMAN.md`, `DEVILS_ADVOCATE.md`, provisional verdicts, final verdicts, completion reports, and run-complete states. The skill, README, architecture doc, model-routing policy, agent registrations, synthetic fixture, and validation logic all reinforced that old behavior.

## Files And Components Changed

- `codex-council-v2/scripts/codex_council_v2.py`: state machine, role registry, forbidden artifact validation, external handoff generation, external artifact intake, completion semantics, evidence/revision gates, legacy invalidation marker command, synthetic fixture.
- `codex-council-v2/tests/test_engine.py`: role-boundary, handoff, arithmetic, provenance, revision, external-artifact, and legacy-contamination tests.
- `.agents/skills/codex-council-v2/SKILL.md`: operator workflow now stops at external Chairman handoff.
- Deleted `.codex/agents/codex-council-v2-chairman.toml` and `.codex/agents/codex-council-v2-devils-advocate.toml`.
- `codex-council-v2/README.md`, `codex-council-v2/docs/ARCHITECTURE.md`, and `codex-council-v2/config/model-routing-policy.md`: documentation and routing updated to match external role ownership.
- Deleted obsolete `codex-council-v2/templates/chairman.md`.
- Added reusable external prompt templates in `codex-council-v2/templates/`.
- Added legacy invalidation manifests in `codex-council-v2/library/legacy-council-import/`.

## New Role Ownership Model

Codex may run the five executives, Librarian, Auditor, anonymous peer review, author revisions, scoped veto handling, final internal validation, and handoff generation.

Codex must not act as Chairman, Devil's Advocate against the Chairman, final commercial decision-maker, Ahmed, or human veto resolver outside factual/numerical verification. Chairman and Devil's Advocate work belongs to separate external ChatGPT sessions. Ahmed remains the final human authority.

## Exact Codex Stop Condition

Codex stops at:

`CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`

Validation requires five canonical memos, completed evidence/audit/review/veto gates, genuine revision handling for accepted material objections, no forbidden internal external-role artifacts, completion report boundary statements, handoff package, handoff manifest, and external startup prompts.

## External ChatGPT Workflow

1. External ChatGPT Chairman receives the Codex handoff package and creates only a provisional consolidated Chairman memo.
2. External ChatGPT Devil's Advocate attacks the Chairman's provisional memo, using the Codex package only for verification.
3. External ChatGPT Chairman receives the attack, classifies objections, revises where needed, and produces a final Chairman verdict for Ahmed review.
4. Ahmed reviews and records the final human decision.

Human-supplied external artifacts can be recorded with `record-external-artifact`; Codex copies them into separated external directories without editing their substantive judgment.

## Tests Performed

- `python -m unittest discover -s codex-council-v2/tests -v`
- `python codex-council-v2/scripts/codex_council_v2.py mark-legacy-role-boundary-crossings`
- `python codex-council-v2/scripts/codex_council_v2.py validate-release-tree --root .`

## Test Results

- Unit suite: 24 tests passed.
- Legacy invalidation marker: 12 historical external-role simulation artifacts marked `INVALID_ROLE_BOUNDARY_CROSSING_NOT_AUTHORITATIVE`.
- Release-tree validation: passed after removing generated test temp output.

## Legacy Migration Notes

Historical artifacts were not deleted. They are listed in:

- `codex-council-v2/library/legacy-council-import/INVALID_ROLE_BOUNDARY_CROSSINGS.md`
- `codex-council-v2/library/legacy-council-import/INVALID_ROLE_BOUNDARY_CROSSINGS.json`

Those records are preserved for audit history and excluded from authoritative decision loading by default.

## Remaining Limitations

The framework can enforce repository-local engine commands, agent registrations, run validation, and generated handoff structure. It cannot prevent a human from manually pasting external-role text into arbitrary files outside the engine; validation catches prohibited artifacts in run space before a Codex handoff is accepted.

## Confirmation

Codex can no longer declare a full final verdict by itself through the V2 engine. Internal completion now means the package is awaiting external ChatGPT Chairman review, with no Chairman verdict, no Devil's Advocate attack, and no final commercial decision produced by Codex.
