---
name: codex-council-v2
description: Run or maintain the separate Codex-only Council V2 decision-support system in this repository. Use when the user asks for the new Codex-only council, bounded council runs, executive lenses, evidence-audited memos, anonymous peer review, scoped vetoes, Chairman synthesis, synthetic council tests, or V2 council run initialization. Do not use for old restaurant-commercial-council runs unless explicitly migrating evidence into a new V2 run.
---

# Codex Council V2

Use the separate system rooted at `codex-council-v2/`. Preserve old council skills, agents, runs, templates, and historical artifacts.

## Required Reads

Read `codex-council-v2/AGENTS.md`, `codex-council-v2/README.md`, `codex-council-v2/docs/ARCHITECTURE.md`, `codex-council-v2/config/model-routing-policy.md`, and the active run charter. For event grammar, read `codex-council-v2/schemas/event-tags.schema.json`.

## Workflow

1. Inspect applicable `AGENTS.md` files and confirm no governance conflict.
2. Initialize or resume a run under `codex-council-v2/runs/`.
3. Create one run charter before executive work.
4. Give the five executives role-specific briefs, not a generic shared prompt.
5. Route evidence through the Librarian cache before new NotebookLM or web research.
6. Keep exactly one canonical memo per executive under `memos/`.
7. Run the Evidence Auditor gate before peer review.
8. Route anonymous peer review through controlled review files.
9. Allow authors to revise only their own canonical memo.
10. Let the Chairman synthesize; run Devil's Advocate; then produce provisional and final verdicts.
11. Validate the run with `python codex-council-v2/scripts/codex_council_v2.py validate-run --run-dir <run-dir>`.

## Hard Gates

- Do not run OpenCode, Hermes, NVIDIA NIM, Gemini APIs, OpenRouter, external agent runners, or a separate orchestration service.
- Do not query NotebookLM, import sources, search the web, log in, switch accounts, or do paid/bulk research without explicit approval.
- Do not let the Librarian choose strategy or the Auditor judge strategy.
- Do not conceal unresolved valid vetoes.
- Do not mark a run complete without `CHAIRMAN.md`, `COMPLETION_REPORT.md`, and `NEXT_RUN_HANDOFF.md`.
- Do not use a real commercial or pricing mission as the framework test.
