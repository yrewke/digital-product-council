# Pre-Migration Inventory

Destination: `C:\dev\restaurants\reserch\consle`

This inventory was created before factory material was copied. Ownership was checked against `outputs/skills-factory/SKILLS_FACTORY_REPORT.md`, the factory file structure, and the contents of each top-level candidate.

| Source path | Destination path | Type | Why it appears factory-owned | Copy | Ambiguous | Human review required |
|---|---|---|---|---|---|---|
| `C:\dev\restaurants\.agents` | `C:\dev\restaurants\reserch\consle\.agents` | Directory | Contains exactly the three authored restaurant council skills described by the factory report. | Yes | No | No |
| `C:\dev\restaurants\.codex` | `C:\dev\restaurants\reserch\consle\.codex` | Directory | Contains exactly the nine authored restaurant council custom-agent profiles described by the factory report. | Yes, then convert the canonical destination profiles from Markdown to TOML. | No | No |
| `C:\dev\restaurants\handoffs` | `C:\dev\restaurants\reserch\consle\handoffs` | Directory | Contains normalized factory handoffs and empty source scaffolding. | Yes | No | No |
| `C:\dev\restaurants\notebooks` | `C:\dev\restaurants\reserch\consle\notebooks` | Directory | Contains the factory notebook registry and query-budget policy. | Yes | No | No |
| `C:\dev\restaurants\reference-sources` | `C:\dev\restaurants\reserch\consle\reference-sources` | Directory | Contains the factory reference inventory, reconnaissance notes, and quarantined third-party reference clones. | Yes, excluding nested third-party `.git` metadata. | No | No |
| `C:\dev\restaurants\working` | `C:\dev\restaurants\reserch\consle\working` | Directory | Contains factory caches, dry runs, ledgers, and the complete live smoke-test run. | Yes | No | No |
| `C:\dev\restaurants\outputs` | `C:\dev\restaurants\reserch\consle\outputs` | Directory | Contains factory reports and empty future-mission scaffolding. | Yes | No | No |
| `C:\dev\restaurants\AGENTS.md` | `C:\dev\restaurants\reserch\consle\AGENTS.md` | File | Repository rules specifically describe the skills factory. | Yes | No | No |
| `C:\dev\restaurants\README.md` | `C:\dev\restaurants\reserch\consle\README.md` | File | Describes the commercial research-council skills factory. | Yes | No | No |
| `C:\dev\restaurants\FNN` | None | Directory | Unrelated repository/work area; not named by the factory report. | No | Yes | No, preserve in place |
| `C:\dev\restaurants\restaurant-website-template` | None | Directory | Unrelated repository/work area. | No | Yes | No, preserve in place |
| `C:\dev\restaurants\reserch` except `reserch\consle` | None | Directory | Contains substantial restaurant-lead research and scripts unrelated to the factory migration. | No | Yes | No, preserve in place |
| `C:\dev\restaurants\notebooklm-roi-source-urls.txt` | None | File | Not listed by the factory report and may belong to separate NotebookLM work. | No | Yes | Yes |

## Safety Notes

- No NotebookLM operation, login, profile switch, MCP configuration change, or foreign script execution is part of this migration.
- Files with credential-like names found under `reference-sources\github` are third-party source-code fixtures, not active credentials. The quarantined reference tree remains ignored by the new repository.
- Existing parent paths marked ambiguous will not be deleted.
