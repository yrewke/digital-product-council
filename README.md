# Digital Product Council

Codex-only council framework for bounded digital product research, strategy, pricing, evidence review, and decision support.

## Active System

The only active council system is Codex Council V2:

- System root: `codex-council-v2/`
- Skill entry point: `.agents/skills/codex-council-v2/`
- Agent profiles: `.codex/agents/codex-council-v2-*.toml`
- Engine: `codex-council-v2/scripts/codex_council_v2.py`

Older V1 restaurant council skills, agents, and working run folders have been removed from the active repository. Historical material imported from those runs is preserved inside `codex-council-v2/library/legacy-council-import/`.

## Quick Commands

Check a run:

```powershell
python codex-council-v2/scripts/codex_council_v2.py status --run-dir codex-council-v2/runs/<run-id>
```

Validate a run:

```powershell
python codex-council-v2/scripts/codex_council_v2.py validate-run --run-dir codex-council-v2/runs/<run-id>
```

Run the test suite:

```powershell
python -m unittest discover -s codex-council-v2/tests -v
```

## Operating Rule

For real council runs, the main Codex session is the operator. Substantive role reasoning must be delegated to visible isolated Codex sub-agents whenever sub-agent tools are available.
