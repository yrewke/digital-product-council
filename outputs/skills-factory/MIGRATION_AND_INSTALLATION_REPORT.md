# Migration And Installation Report

## Destination

- Isolated repository: `C:\dev\restaurants\reserch\consle`
- Git repository initialized: yes
- Initial commit: `bee646d` - `Initialize restaurant commercial research council console`
- Remote push: none

## Migrated Paths

- `.agents\skills`
- `.codex\agents`
- `handoffs`
- `notebooks`
- `reference-sources`
- `working`
- `outputs`
- `AGENTS.md`
- `README.md`

Quarantined third-party material under `reference-sources\github` was copied as read-only reference content without nested foreign `.git` metadata and is excluded by `.gitignore`. Nothing from it was installed globally.

## Preserved Ambiguous Paths

- `C:\dev\restaurants\notebooklm-roi-source-urls.txt`
- All unrelated restaurant-lead research under `C:\dev\restaurants\reserch` outside `reserch\consle`

## Source Cleanup

No original factory path was removed. Cleanup was attempted only after verification but was blocked by the destructive-action approval gate. See `migration\POST_MIGRATION_CLEANUP_REPORT.md`.

## Local Skill Inventory

Exactly three canonical authored skills exist under `.agents\skills`:

1. `restaurant-research-librarian`
2. `restaurant-commercial-council`
3. `restaurant-commercial-deliverables`

## Global Skill Inventory

Exactly the same three authored skills were installed under `C:\Users\ahmed\.agents\skills`.

- Installation mode: copy-and-sync
- Symlink test result: Windows rejected directory symlink creation in the current environment.
- Verification: every global skill file matches its canonical repository file by SHA-256.
- Synchronization script: `scripts\sync-global-codex-assets.ps1`
- Expected Codex behavior: Codex may display both repository-local and global copies with the same skill names. They were not merged or renamed.

## Local Custom-Agent Inventory

Exactly nine canonical TOML profiles exist under `.codex\agents`:

1. `business-builder.toml`
2. `chairman.toml`
3. `competitor-alternatives-analyst.toml`
4. `devils-advocate.toml`
5. `evidence-auditor.toml`
6. `market-economics-analyst.toml`
7. `research-librarian.toml`
8. `restaurant-operator.toml`
9. `restaurant-owner.toml`

The original authored Markdown profiles were converted to TOML in the canonical destination while preserving their role instructions.

## Global Custom-Agent Inventory

The same nine authored TOML profiles were copied to `C:\Users\ahmed\.codex\agents`. Every installed agent matches its canonical repository file by SHA-256. No unrelated personal agent was modified.

The reserved same-name backup location was:

`C:\Users\ahmed\.codex\backups\restaurant-council-20260613-195108`

No same-name existing assets required backup content.

## Smoke-Test Preservation

- Complete smoke-test history is present under `working\council-runs\2026-06-13-live-smoke-test-001`.
- All six required checkpoint artifacts matched their source SHA-256 hashes after copying.
- `outputs\skills-factory\LIVE_SMOKE_TEST_REPORT.md` is present.
- The repository query ledger and run artifacts still preserve the failed `PERMISSION_DENIED` attempt.

## Safety Verification

- No NotebookLM query was executed during migration.
- No NotebookLM deep research was run.
- No NotebookLM login or profile switch occurred.
- No MCP configuration was modified.
- No foreign repository script was executed.
- No third-party skill was installed globally.
- No credential, cookie, token, account detail, or NotebookLM browser-profile data was copied into tracked repository files.
- The restaurant pricing mission was not started.
- No package prices, sales claims, or commercial verdicts were produced.

## Exact Next Human Action

Restart Codex so it discovers the newly installed global skills and custom agents. Separately authorize removal of the nine verified duplicate factory-owned source paths listed in `migration\POST_MIGRATION_CLEANUP_REPORT.md` if parent-folder cleanup is still desired.
