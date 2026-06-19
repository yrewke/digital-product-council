---
name: codex-council-v2
description: Run or maintain the separate Codex-only Council V2 decision-support system in this repository. Use when the user asks for the new Codex-only council, bounded council runs, executive lenses, evidence-audited memos, anonymous peer review, scoped vetoes, external Chairman handoff, synthetic council tests, or V2 council run initialization. Do not use for old restaurant-commercial-council runs unless explicitly migrating evidence into a new V2 run.
---

# Codex Council V2

Use the separate system rooted at `codex-council-v2/`. Preserve old council skills, agents, runs, templates, and historical artifacts.

## Required Reads

Read `codex-council-v2/AGENTS.md`, `codex-council-v2/README.md`, `codex-council-v2/docs/ARCHITECTURE.md`, `codex-council-v2/config/model-routing-policy.md`, and the active run charter. For event grammar, read `codex-council-v2/schemas/event-tags.schema.json`.

## Workflow

1. Inspect applicable `AGENTS.md` files and confirm no governance conflict.
2. Initialize or resume a run under `codex-council-v2/runs/`.
3. Use `python codex-council-v2/scripts/codex_council_v2.py status|resume --run-dir <run-dir>` before dispatching work.
4. Advance only through legal engine commands; do not hand-edit state files to skip stages.
5. Create one run charter before executive work and validate it with `validate-charter`.
6. For real runs, dispatch isolated visible sub-agents for the five executive roles before executive reasoning. Use `codex-council-v2-contrarian`, `codex-council-v2-first-principles`, `codex-council-v2-expansionist`, `codex-council-v2-outsider`, and `codex-council-v2-executor`.
7. Give each sub-agent a role-specific brief, the run charter, only the relevant evidence packet, and a required output contract. Do not give a generic shared prompt.
8. Keep the main Codex session as operator only: run engine commands, maintain state, collect sub-agent outputs, submit canonical text, validate, and report progress.
9. Route evidence through engine cache commands before new NotebookLM or web research. Use `codex-council-v2-librarian` as an isolated sub-agent for nontrivial evidence routing when sub-agent tools are available.
10. Submit each executive's one canonical memo through `submit-memo`.
11. Run `extract-claims`, then dispatch `codex-council-v2-auditor` for substantive fact/accounting review and record its findings with `record-fact-check`; run `validate-audit` before peer review.
12. If audit blocks a memo, return the issue only to the original author sub-agent for revision; `validate-audit` must confirm the contradicted claim is removed, corrected, or explicitly downgraded in the claim text.
13. Use `create-anonymous-review-packets`, dispatch isolated peer-review sub-agents by assigned role, then use `record-peer-review`, optional `waive-peer-review`, and `merge-review-events`; never let reviewers rewrite another executive's memo. Merge only after every assignment is complete, failed after retry, or waived.
14. Use `record-veto` so invalid vetoes become ordinary dissent. Use `resolve-veto` to verify required remedies before treating a valid veto as resolved.
15. Use `prepare-chairman-packet` to create the external Chairman handoff package, handoff manifest, completion report, and reusable external startup prompts.
16. Validate the run with `python codex-council-v2/scripts/codex_council_v2.py validate-run --run-dir <run-dir>`.
17. Stop at `CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`. Do not run the external Chairman, Devil's Advocate, final Chairman verdict, or Ahmed decision stages.

## Isolated Sub-Agent Rule

- Real council runs must use visible Codex sub-agents for substantive role reasoning whenever the `spawn_agent` capability is available in the current session.
- The five executive agents must be spawned separately so their first-pass reasoning stays independent.
- Service agents are spawned at their stage boundaries: Librarian for evidence routing and Auditor for fact/accounting review. Chairman and Devil's Advocate are external ChatGPT roles and must not be spawned as Codex agents.
- The operator must not silently replace sub-agent dispatch with single-session roleplay. If sub-agent spawning is unavailable, state that limitation to the user before continuing and label the run log as `MANUAL_SINGLE_SESSION_FALLBACK`.
- Sub-agents should not receive the full repository by default. Pass bounded context: charter, role brief, status summary, evidence packet IDs or excerpts, output format, allowed files, and forbidden actions.
- Sub-agents may reason and draft, but deterministic state transitions remain the operator's responsibility through `codex_council_v2.py`.

## Hard Gates

- Do not run OpenCode, Hermes, NVIDIA NIM, Gemini APIs, OpenRouter, external agent runners, or a separate orchestration service.
- Do not query NotebookLM, import sources, search the web, log in, switch accounts, or do paid/bulk research without explicit approval.
- Do not let the Librarian choose strategy or the Auditor judge strategy.
- Do not conceal unresolved valid vetoes.
- Do not mark a run complete beyond `CODEX_COUNCIL_COMPLETE_AWAITING_EXTERNAL_CHAIRMAN`.
- Do not create `CHAIRMAN.md`, `DEVILS_ADVOCATE.md`, `CHAIRMAN_FIRST_SYNTHESIS.md`, `CHAIRMAN_PROVISIONAL_VERDICT.md`, `CHAIRMAN_FINAL*.md`, `FINAL_COMMERCIAL_*VERDICT.md`, or `DEVILS_ADVOCATE_ATTACK.md` inside Codex-owned run space.
- External prompt templates may mention Chairman or Devil's Advocate only under `templates/` or `handoff/`.
- Do not use a real commercial or pricing mission as the framework test.
- Do not mark a blocking fact check `RESOLVED` unless the current memo itself passes the audit validator.
- Do not advance to author revision with incomplete peer-review assignments.
- Do not mark a veto `RESOLVED` unless the engine verifies the remedy. External Chairman judgment artifacts may be recorded only with `record-external-artifact` after the Codex handoff and must be human-supplied.
