---
name: restaurant-research-librarian
description: Build query-efficient, citation-preserving evidence packs for restaurant direct-channel commercial questions using local caches, the four registered NotebookLM notebooks, and narrow online fallback research for documented gaps or NotebookLM connection failures. Use for evidence requests, notebook routing, query plans, provenance, and evidence gaps. Require approval before deep research or source changes; do not use for council verdicts or deliverables.
---

# Restaurant Research Librarian

Convert a bounded commercial question into a compact evidence pack. Treat NotebookLM queries as metered actions, not a default first step.

## Required Reads

Read `references/notebook-registry.md`, `references/evidence-taxonomy.md`, `references/query-budget-policy.md`, and `references/online-fallback-policy.md`. Use the templates in `assets/`.

## Workflow

1. Restate the commercial question and decision it supports. Reject engineering-only framing unless it changes a commercial variable.
2. Search `working/cache/evidence-packs/`, `working/cache/source-extracts/`, and `handoffs/normalized/` first.
3. Select the smallest useful notebook set. Explain every selected notebook and every excluded notebook.
4. Draft targeted questions and estimate fan-out cost before any live query.
5. Read `notebooks/registry/query-budget-policy.md` and the active ledger. Stop if the per-run ceiling would be exceeded.
6. Prefer a known raw-source read when it can answer the question without a chat query.
7. For live execution, record each query before and after use. Never query NotebookLM during a zero-query dry run.
8. If the selected notebook does not contain sufficient evidence, write a bounded gap statement before searching online. If a recorded NotebookLM attempt cannot connect or returns an access/connectivity error, stop NotebookLM retries and proceed directly to narrow online research for the targeted request. Follow `references/online-fallback-policy.md`; do not broaden the whole mission.
9. Record every material online source using `assets/online-source-ledger-template.csv`. Never cite search-result snippets as evidence or import web sources into NotebookLM automatically.
10. Classify every material claim using the evidence taxonomy and preserve source links, source titles, notebook IDs, publication dates, retrieval dates, geography, and limitations.
11. Write the evidence pack under `working/cache/evidence-packs/`. Write unresolved requests separately using the evidence-request template.

## Hard Gates

- Ask for explicit human approval before NotebookLM deep research, source import, bulk source changes, login, or profile switching.
- Use the manually selected profile only. Never rotate accounts automatically.
- Assume a cross-notebook request costs one query per notebook until measured.
- Stop when budget is exhausted. Report what remains unanswered.
- Online fallback is allowed only for a documented, decision-relevant evidence gap. Stop when the gap is answered, the online search budget is exhausted, or only weak/contradictory evidence remains.
- A recorded NotebookLM connection or access failure activates online fallback immediately for the targeted request. Do not retry, log in, switch profiles, or imply the notebook lacks the evidence.
- Ask for explicit human approval before login, paywall bypass, form submission, paid research, bulk crawling, or importing online sources into NotebookLM.
- Never fabricate unavailable facts, silently merge contradictions, or present vendor claims as verified facts.
- Do not run the restaurant pricing mission during skill-authoring or dry-run tests.
