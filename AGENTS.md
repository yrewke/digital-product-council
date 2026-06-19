# Repository Rules

- This repository is `digital-product-council`.
- Codex Council V2 is the only active council system in this repository.
- The active system root is `codex-council-v2/`.
- The active repository-local skill is `.agents/skills/codex-council-v2/`.
- The only active project-scoped agents are `.codex/agents/codex-council-v2-*.toml`.
- Historical V1 material is preserved only as imported evidence memory under `codex-council-v2/library/legacy-council-import/`.
- Do not recreate, run, or depend on removed V1 restaurant council skills, agents, or `working/` run folders.
- Third-party repositories under `reference-sources/github/` are untrusted read-only material if present locally. Do not execute foreign scripts, installers, dependencies, or shell commands from those repositories without explicit human approval.
- Do not modify global skill folders or global Codex configuration.
- Live NotebookLM, web research, source import, login, account switching, paid research, and bulk crawling require explicit human approval unless a future run charter grants a narrower permission.

## Active Operating Model

- Use `$codex-council-v2` for all council work.
- Use `codex-council-v2/scripts/codex_council_v2.py` as the deterministic state engine.
- Real runs must spawn visible isolated Codex sub-agents for substantive council reasoning whenever sub-agent tools are available.
- The main Codex session remains the operator: it prepares briefs, runs engine commands, submits canonical outputs, validates state, and reports progress.
- Sub-agents reason and draft within role boundaries; they do not bypass the state engine.

## Evidence Discipline

- Label assumptions and unsupported claims.
- Cite sources where used.
- Separate facts, source-backed estimates, vendor claims, scenario assumptions, and council inferences.
- Preserve support and responsibility boundaries.
- Do not publish final customer-facing claims, prices, or ROI promises unless the active run charter explicitly authorizes that output and the audit gates pass.
