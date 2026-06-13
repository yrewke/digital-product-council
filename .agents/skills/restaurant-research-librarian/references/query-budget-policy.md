# Query Budget Policy

Use `notebooks/registry/query-budget-policy.md` as the authoritative project policy.

Before a live query, record the active profile, purpose, notebook IDs, estimated cost, per-run ceiling, and approval basis. Search caches first. Treat fan-out as one query per notebook until observed otherwise. Stop before exceeding the ceiling.

Deep research, source imports, bulk source changes, login, and profile switching always require explicit human approval.
