# Codex Council V2

Codex Council V2 is a separate, Codex-only council framework for bounded research and decision support. It preserves the older restaurant council systems and runs beside them instead of replacing them.

## What It Is

- Five permanent executive lenses: Contrarian, First-Principles Thinker, Expansionist, Outsider, and Executor.
- Service agents outside the five: Librarian, Evidence Auditor / Accountant, Devil's Advocate, and Chairman.
- One canonical memo file per executive per run.
- Central evidence memory and request deduplication.
- Permanent factual / numerical evidence veto for the Auditor.
- Mission-specific executive vetoes defined in each run charter.
- Resumable stage status, deterministic validation, and synthetic dry-run coverage.

## New System Root

`codex-council-v2/`

Repository-local Codex entry points:

- Skill: `.agents/skills/codex-council-v2/`
- Agents: `.codex/agents/codex-council-v2-*.toml`

## Commands

Initialize a real run scaffold:

```powershell
python codex-council-v2/scripts/codex_council_v2.py init-run --run-id 2026-06-17-example --title "Example bounded decision" --question "What bounded action should we choose?"
```

Run the synthetic framework test:

```powershell
python codex-council-v2/scripts/codex_council_v2.py synthetic-test
```

Validate a run:

```powershell
python codex-council-v2/scripts/codex_council_v2.py validate-run --run-dir codex-council-v2/runs/synthetic-fixture-001
```

Resume from the last valid stage:

```powershell
python codex-council-v2/scripts/codex_council_v2.py resume --run-dir codex-council-v2/runs/synthetic-fixture-001
```

## First Real Run Prompt

Use `$codex-council-v2` to initialize a new Codex-only council run for `[decision question]`. Create the run charter first, classify imported decisions, assign mission-specific vetoes, and stop before any live NotebookLM or web research unless explicitly approved.
