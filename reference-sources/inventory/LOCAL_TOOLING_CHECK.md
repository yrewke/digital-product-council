# Local Tooling Check

Checked on 2026-06-13 from PowerShell without login, account switching, notebook inspection, or NotebookLM queries.

| Check | Result |
|---|---|
| `command -v nlm` equivalent (`Get-Command nlm`) | Not found on current PowerShell `PATH` |
| `command -v notebooklm-mcp` equivalent (`Get-Command notebooklm-mcp`) | Not found on current PowerShell `PATH` |
| `nlm --version` | Not run because `nlm` was not found |

Human attention: confirm whether the expected executables are exposed only in another shell/environment. Do not install a second implementation.
