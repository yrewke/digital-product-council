# NotebookLM Query Budget Policy

## Configuration

- `active_profile`: manually selected; never rotate automatically
- `daily_estimated_limit`: configured by operator
- `per_run_budget`: configured before each live run
- `dry_run_budget`: `0`
- `live_smoke_test_budget`: maximum `5`

## Rules

1. Search `working/cache/evidence-packs/`, `working/cache/source-extracts/`, and normalized handoffs before any query.
2. Record purpose, notebook IDs, timestamp, estimated cost, observed cost when measurable, evidence-pack path, raw-source avoidance, approval basis, and status in `working/ledgers/notebooklm-query-ledger.csv`.
3. Assume fan-out costs one query per notebook until measured.
4. Use the smallest notebook set. Do not query all four by default.
5. Stop before exceeding the per-run or daily estimated limit.
6. Human approval is mandatory for deep research, source import, bulk source changes, login, and profile switching.
7. A live smoke test must stop after at most five chat queries for human review.
