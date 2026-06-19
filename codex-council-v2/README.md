# Codex Council V2

Codex Council V2 is a separate, Codex-only council framework for bounded research and decision support. It preserves the older restaurant council systems and runs beside them instead of replacing them.

## What It Is

- Five permanent executive lenses: Contrarian, First-Principles Thinker, Expansionist, Outsider, and Executor.
- Service agents outside the five: Librarian, Evidence Auditor / Accountant, Devil's Advocate, and Chairman.
- One canonical memo file per executive per run.
- Central evidence memory and request deduplication.
- Permanent factual / numerical evidence veto for the Auditor.
- Mission-specific executive vetoes defined in each run charter.
- Resumable state machine, append-only event ledger, deterministic validation, and synthetic dry-run coverage through the same engine used by real runs.

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

Run the test suite:

```powershell
python -m unittest discover -s codex-council-v2/tests -v
```

Validate a run:

```powershell
python codex-council-v2/scripts/codex_council_v2.py validate-run --run-dir codex-council-v2/runs/synthetic-fixture-001
```

Resume from the last valid stage:

```powershell
python codex-council-v2/scripts/codex_council_v2.py resume --run-dir codex-council-v2/runs/synthetic-fixture-001
```

Check status:

```powershell
python codex-council-v2/scripts/codex_council_v2.py status --run-dir codex-council-v2/runs/synthetic-fixture-001
```

## Real Run Pattern

The Codex skill orchestrates these engine operations: `init-run`, `validate-charter`, `open-evidence-requests`, `register-evidence-request`, `resolve-evidence-request`, `mark-evidence-ready`, `submit-memo`, `extract-claims`, `record-fact-check`, `validate-audit`, `create-anonymous-review-packets`, `record-peer-review`, `merge-review-events`, `record-author-response`, `record-veto`, `prepare-chairman-packet`, `record-first-synthesis`, `record-devils-advocate`, `record-provisional-verdict`, `open-post-chair-review`, `record-final-verdict`, `validate-run`, `resume`, and `complete-run`.

Python validates state, locks, cache reuse, review routing, audit resolution, veto scope, and old-system hashes. Codex supplies the reasoning text submitted into those commands.

For real runs, the main Codex session is the operator, not the hidden author of every role. It must spawn visible isolated sub-agents for substantive council reasoning whenever the current Codex session exposes sub-agent tools:

- Executive memo drafting: spawn `codex-council-v2-contrarian`, `codex-council-v2-first-principles`, `codex-council-v2-expansionist`, `codex-council-v2-outsider`, and `codex-council-v2-executor` separately.
- Evidence routing: spawn `codex-council-v2-librarian` for nontrivial routing, cache checks, and provenance-preserving evidence packets.
- Audit: spawn `codex-council-v2-auditor` for substantive factual and numerical review before peer review.
- Synthesis and attack: spawn `codex-council-v2-chairman` for synthesis and `codex-council-v2-devils-advocate` only after a Chairman direction exists.

Each sub-agent receives a bounded role brief, the run charter, only relevant evidence or review packets, and a strict output contract. The operator collects outputs and submits them through `codex_council_v2.py`; sub-agents do not bypass the deterministic state machine.

If sub-agent spawning is unavailable, the operator must tell the user before continuing and label the run as `MANUAL_SINGLE_SESSION_FALLBACK` in the run notes. The fallback is allowed only because it is explicit, not silent.

## Legacy Council Memory

The old restaurant council memory has been imported into `codex-council-v2/library/`. Start future continuation work from `codex-council-v2/library/START_HERE.md`, then inspect `EVIDENCE_LIBRARY.json` and `SOURCE_LEDGER.csv` before requesting new research. To regenerate the archive and indexes from local legacy artifacts, run:

```powershell
python codex-council-v2/scripts/import_legacy_council_memory.py
```

Additional hardening commands:

```powershell
python codex-council-v2/scripts/codex_council_v2.py waive-peer-review --run-dir <run-dir> --assignment-id RA-0020 --reason "Reviewer failed after retry"
python codex-council-v2/scripts/codex_council_v2.py resolve-veto --run-dir <run-dir> --veto-id V-0001
```

## Release Status

`READY_FOR_BOUNDED_REAL_RUN`

The first real mission must still be treated as a controlled pilot. Live NotebookLM, web research, source import, login, account switching, paid research, and bulk crawling still require explicit approval.

## First Real Run Prompt

Use `$codex-council-v2` to initialize and run a new Codex-only council for `[decision question]`. Use `codex-council-v2/scripts/codex_council_v2.py` as the deterministic state engine, spawn visible isolated V2 sub-agents for reasoning, and stop before live NotebookLM or web research unless explicitly approved.
