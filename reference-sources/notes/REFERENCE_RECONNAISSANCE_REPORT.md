# Reference Reconnaissance Report

This is bounded text-only reconnaissance. No cloned code, scripts, installers, dependencies, research operations, or NotebookLM operations were executed.

## 1. Council deliberation patterns

| Source repository | Exact local file path | Pattern and value | Disposition |
|---|---|---|---|
| llm-council | `reference-sources/github/llm-council/README.md` | Independent opinions, anonymized peer ranking, then chairman synthesis. Establishes the core protocol. | Modify |
| ngmeyer-skills | `reference-sources/github/ngmeyer-skills/skills/productivity/council-review/SKILL.md` | Distinct reasoning methods, parallel dispatch, scope preflight, confidence and diversity checks. Helps prevent theatrical consensus. | Borrow selectively |
| boardroom_skills | `reference-sources/github/boardroom_skills/SKILL.md` | Sealed role contexts, mandatory dissent, quantitative anchors, and orphaned-risk synthesis. Useful for commercial decisions. | Borrow |
| llm-council-skill | `reference-sources/github/llm-council-skill/SKILL.md` | Legible framing and synthesis structure with one concrete first action. | Borrow |
| agent-tower-plugin | `reference-sources/github/agent-tower-plugin/SKILL.md` | Routes among council, debate, and producer/reviewer deliberation; suggests dynamic personas. | Modify |

## 2. Organizer and librarian patterns

| Source repository | Exact local file path | Pattern and value | Disposition |
|---|---|---|---|
| pm-skills | `reference-sources/github/pm-skills/agents/pm-workflow-orchestrator.md` | Explicit invocation, ordered steps, minimal carried state, disk artifacts, and stop-on-empty/failure. | Borrow |
| agent-council | `reference-sources/github/agent-council/README.md` | Session registry concepts: list, replay, revisit, outcome, and targeted nudge. Useful for durable council history. | Modify |
| agentbrain | `reference-sources/github/agentbrain/.claude/skills/brain-research/SKILL.md` | Thin wrapper points to authoritative command/registry and required artifact. Reduces duplicated instructions. | Borrow |
| Deep-Research-skills | `reference-sources/github/Deep-Research-skills/skills/research-codex-en/research/SKILL.md` | Separates item outline, field definitions, execution config, and human confirmation. | Modify |

## 3. Evidence and verification patterns

| Source repository | Exact local file path | Pattern and value | Disposition |
|---|---|---|---|
| agent-skills | `reference-sources/github/agent-skills/skills/doubt-driven-development/SKILL.md` | Isolate artifact plus contract, use fresh-context adversarial review, reconcile every finding, enforce stop limits. | Borrow |
| agentbrain | `reference-sources/github/agentbrain/.claude/skills/brain-research/SKILL.md` | Requires a research claim ledger and stops when evidence or approval is missing. | Borrow |
| ai-research-skills | `reference-sources/github/ai-research-skills/docs/researcher-workflow-checklist.md` | Verify generated briefs against source bundles before trusting them. | Borrow concept only |
| ngmeyer-skills | `reference-sources/github/ngmeyer-skills/skills/engineering/adversarial-review/SKILL.md` | Separates artifact-breaking review from open-question council deliberation and triages findings. | Borrow |

## 4. Research workflow patterns

| Source repository | Exact local file path | Pattern and value | Disposition |
|---|---|---|---|
| Deep-Research-skills | `reference-sources/github/Deep-Research-skills/skills/research-codex-en/research/SKILL.md` | Preliminary framework, user confirmation, explicit fields, then handoff to deep phase. | Modify |
| Deep-Research-skills | `reference-sources/github/Deep-Research-skills/skills/research-codex-en/research-deep/SKILL.md` | Batch execution, resume checks, uncertain markers, and approval before the next batch. | Borrow selectively |
| notebooklm-mcp-cli | `reference-sources/github/notebooklm-mcp-cli/src/notebooklm_tools/data/references/workflows.md` | Documents destructive-operation confirmation and explicit workflow stages. Useful only as future tooling reference. | Modify heavily |

## 5. Skill anatomy and folder patterns

| Source repository | Exact local file path | Pattern and value | Disposition |
|---|---|---|---|
| pm-skills | `reference-sources/github/pm-skills/agents/pm-workflow-orchestrator.md` | Narrow orchestrator contract, authoritative references, explicit tool exclusions, and no hidden auto-trigger. | Borrow |
| agentbrain | `reference-sources/github/agentbrain/.claude/skills/brain-research/SKILL.md` | Minimal activation wrapper with source-of-truth marker and required reads/artifact. | Borrow |
| boardroom_skills | `reference-sources/github/boardroom_skills/SKILL.md` | Main skill delegates role detail to separate role files and output templates. | Borrow |
| agent-council | `reference-sources/github/agent-council/skills/claude-code/agent-council-nudge/SKILL.md` | Atomic follow-up actions around a durable council session. | Modify |

## 6. Patterns that appear dangerous, bloated, or irrelevant

- Reject all global installers and setup commands found in `agent-council/README.md` and `ai-research-skills/docs/researcher-workflow-checklist.md`.
- Reject external CLI council execution by default; it expands tool access, authentication, cost, and prompt-injection risk.
- Reject hard-coded global paths such as `~/.codex/skills/...` in `Deep-Research-skills/.../research-deep/SKILL.md`.
- Reject automatic broad workspace scanning and overly aggressive trigger phrases unless tightly bounded.
- Reject claims of research superiority that are not independently verified during the high-effort pass.
- Reject running NotebookLM workflows described in `notebooklm-mcp-cli/.../workflows.md` during setup.
- Avoid large persona rosters, repeated embedded prompt templates, and multi-round debate without explicit cost/stop controls.

## 7. Questions that the high-effort skill-authoring pass must resolve

1. Which council roles are fixed, dynamically selected, or mission-specific?
2. What evidence schema and claim-ledger format will be authoritative?
3. How will sealed contexts receive enough evidence without leaking other roles' conclusions?
4. When is anonymous peer review worth its cost, and what is the lite mode?
5. What are quorum, timeout, retry, and stop rules?
6. Which actions always require human approval, especially NotebookLM, web research, and external CLIs?
7. How are source extracts normalized and handed off without losing provenance?
8. How will council sessions, decisions, outcomes, and revisions be registered locally?
9. What evals prove role distinctness, evidence coverage, dissent quality, and anti-rationalization?
10. How will active skills remain concise and repository-local under `.agents/skills/`?
