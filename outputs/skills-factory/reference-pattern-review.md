# Reference Pattern Review

| Reference repository | Commit | Useful pattern borrowed | Rejected or modified | Destination | Security/compatibility concern |
|---|---|---|---|---|---|
| karpathy/llm-council | `92e1fcc` | Independent opinions, anonymous review, chairman synthesis | No app/runtime or model-provider setup | commercial council | Foreign dependencies and API calls |
| jacob-bd/notebooklm-mcp-cli | `6d41c75` | Explicit workflows and destructive-action confirmation | No login, queries, imports, or MCP changes during authoring | librarian and query policy | Live operations require approval and budget |
| ngmeyer/skills | `2934439` | Scope preflight, distinct reasoning, adversarial artifact review | Removed research-performance claims and complex optional modes | council, auditor | Avoid bloated multi-round execution |
| teemutuo/boardroom_skills | `dc097fc` | Sealed contexts, role distinctness, mandatory dissent | Replaced executive roles with restaurant commercial roles | thinker profiles and council | Personas must not become unsupported theater |
| tenfoldmarc/llm-council-skill | `0dc0327` | Legible framing and actionable synthesis | Removed broad workspace scan and aggressive triggers | council | Prevent context leakage and accidental mission start |
| yogirk/agent-council | `f6d1e1a` | Quorum, revisit, outcome, targeted nudge concepts | Rejected external CLI execution and global installation | council run records | External CLIs expand tool and prompt-injection risk |
| BayramAnnakov/agent-tower-plugin | `54a70c3` | Mode routing and dynamic perspectives | Fixed this council to five required thinkers | council | User questioning and mode explosion can add friction |
| Weizhena/Deep-Research-skills | `e5479f8` | Outline/fields separation, batching, resume, human checkpoints | Rejected global paths and automatic research execution | librarian | Deep research and source changes need approval |
| WenyuChiou/ai-research-skills | `336e10e` | Verify generated briefs against source bundles | Rejected installers and live NotebookLM workflows | librarian, auditor | Do not trust generated briefs without provenance |
| product-on-purpose/pm-skills | `f82e5d2` | Atomic boundaries, explicit invocation, stop-on-empty/failure | Simplified orchestration and state machinery | all skills and organizers | Avoid hidden autonomous chains |
| rohitg00/agentbrain | `c84e1df` | Claim ledger, required artifacts, stop when evidence missing | Avoided wrapper/registry complexity | librarian, auditor, deliverables | Prevent rationalizing missing evidence |
| addyosmani/agent-skills | `d187883` | Artifact-plus-contract isolation, fresh-context doubt, reconciliation | No external cross-model CLI execution | Devil's Advocate and auditor | Fresh review must remain read-only and bounded |

All repositories remained quarantined under `reference-sources/github/`; no foreign script or installer was executed.
