# Skills Factory Report

## Outcome

The repository-local restaurant commercial research-council skills factory is complete. The restaurant pricing mission was not started, and no package price, sales claim, or commercial verdict was finalized.

## Skills Created

Exactly three active skills exist under `.agents/skills/`:

1. `restaurant-research-librarian` - routes bounded evidence requests, protects query budgets, preserves citations, and builds evidence packs.
2. `restaurant-commercial-council` - runs sealed commercial thinker analysis, disagreement review, Devil's Advocate attack, Evidence Auditor review, and Chairman synthesis.
3. `restaurant-commercial-deliverables` - turns an approved verdict into evidence-safe business artifacts.

Each skill includes its required references and assets. Each also has local `agents/openai.yaml` interface metadata.

## Custom Agents Created

Thinkers:
- `.codex/agents/restaurant-owner.md`
- `.codex/agents/restaurant-operator.md`
- `.codex/agents/market-economics-analyst.md`
- `.codex/agents/competitor-alternatives-analyst.md`
- `.codex/agents/business-builder.md`

Organizers:
- `.codex/agents/research-librarian.md`
- `.codex/agents/evidence-auditor.md`
- `.codex/agents/chairman.md`
- `.codex/agents/devils-advocate.md`

## Other Files Created

- Notebook registry and reusable budget policy under `notebooks/registry/`
- Empty query ledger schema under `working/ledgers/`
- Six normalized handoff notes under `handoffs/normalized/`
- Five synthetic fixtures and results under `working/dry-runs/`
- `outputs/skills-factory/reference-pattern-review.md`
- `outputs/skills-factory/LIVE_SMOKE_TEST_OPERATOR_GUIDE.md`
- Updated repository-local `AGENTS.md`

## Reference Patterns

Borrowed:
- Karpathy council stages and anonymous review
- Boardroom sealed contexts and explicit dissent
- ngmeyer scope preflight and separation of council vs adversarial review
- PM Skills atomic boundaries, explicit invocation, and stop-on-empty/failure
- AgentBrain claim-ledger and evidence-gate discipline
- Addy Osmani artifact-plus-contract doubt and reconciliation
- Deep Research outline, batching, and human checkpoints
- NotebookLM CLI destructive-action confirmation
- Agent Council quorum and durable-session concepts

Modified or rejected:
- All global installers, foreign scripts, global paths, and external CLI council execution
- Broad automatic workspace scans and aggressive triggers
- Automatic research, source import, login, profile switching, or account rotation
- Unsupported research-performance claims and unbounded multi-round debate
- Framework and architecture debate without commercial consequence

Full comparison: `outputs/skills-factory/reference-pattern-review.md`.

## Security Precautions

- Third-party repositories remained quarantined and text-only.
- No foreign scripts, installers, dependencies, or shell files were executed.
- No global skill folders or Codex/MCP configuration were modified.
- No NotebookLM query, deep research, source import, login, profile switch, or notebook change occurred.
- Active skills were authored from scratch.
- Live NotebookLM actions are gated by budget and human approval.

## Dry-Run Results

All five synthetic zero-query cases passed:

| Case | Result |
|---|---|
| One-notebook routing | PASS |
| Justified cross-notebook routing and fan-out estimate | PASS |
| Unsupported 30% savings claim rejection | PASS |
| Engineering-drift refusal | PASS |
| Contradictory Tier 0 handoff preservation | PASS |

Results: `working/dry-runs/DRY_RUN_RESULTS.md`. NotebookLM chat queries used: `0`.

## Validation

- Skill count: `3`
- Project-agent count: `9`
- Built-in `quick_validate.py`: PASS for all three skills
- Unresolved TODO markers in authored artifacts: none
- Source handoffs found: none; normalized notes explicitly preserve that absence

## Unresolved Design Questions

- Exact live per-day NotebookLM limit and active profile name
- Whether anonymous full cross-review or compact disagreement review becomes the default
- Council timeout and quorum tuning after real observations
- Final claim-ledger ID convention
- Which local market archetypes become validated target segments
- Tier 0 role, package boundaries, pricing model, and price points

## Later Five-Query Live Smoke Test

1. Get human approval and confirm the existing `nlm`/`notebooklm-mcp` executables in the intended shell.
2. Manually select the active profile; do not log in or switch profiles without separate approval.
3. Create a run ID and set a hard per-run budget of `5`.
4. Search local caches first, choose one bounded question, and select the smallest notebook set.
5. Record estimated fan-out cost before querying and log every query in `working/ledgers/notebooklm-query-ledger.csv`.
6. Stop at five chat queries or earlier when sufficient evidence or a blocker appears.
7. Do not use deep research, import sources, or modify notebooks.
8. Produce an evidence pack and stop for human review before convening the council.

Operator guide: `outputs/skills-factory/LIVE_SMOKE_TEST_OPERATOR_GUIDE.md`.
