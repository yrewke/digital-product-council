---
name: restaurant-research-librarian
description: Build query-efficient, citation-preserving evidence packs for restaurant direct-channel commercial questions using local caches and the four registered NotebookLM notebooks. Use for evidence requests, notebook routing, query plans, provenance, and evidence gaps. Require approval before deep research or source changes; do not use for council verdicts or deliverables.
---

# Restaurant Research Librarian

Convert a bounded commercial question into a compact evidence pack. Treat NotebookLM queries as metered actions, not a default first step.

## Required Reads

Read `references/notebook-registry.md`, `references/evidence-taxonomy.md`, and `references/query-budget-policy.md`. Use the templates in `assets/`.

## Workflow

1. Restate the commercial question and decision it supports. Reject engineering-only framing unless it changes a commercial variable.
2. Search `working/cache/evidence-packs/`, `working/cache/source-extracts/`, and `handoffs/normalized/` first.
3. Select the smallest useful notebook set. Explain every selected notebook and every excluded notebook.
4. Draft targeted questions and estimate fan-out cost before any live query.
5. Read `notebooks/registry/query-budget-policy.md` and the active ledger. Stop if the per-run ceiling would be exceeded.
6. Prefer a known raw-source read when it can answer the question without a chat query.
7. For live execution, record each query before and after use. Never query NotebookLM during a zero-query dry run.
8. Classify every material claim using the evidence taxonomy and preserve source links, source titles, notebook IDs, dates, geography, and limitations.
9. Write the evidence pack under `working/cache/evidence-packs/`. Write unresolved requests separately using the evidence-request template.

## Hard Gates

- Ask for explicit human approval before NotebookLM deep research, source import, bulk source changes, login, or profile switching.
- Use the manually selected profile only. Never rotate accounts automatically.
- Assume a cross-notebook request costs one query per notebook until measured.
- Stop when budget is exhausted. Report what remains unanswered.
- Never fabricate unavailable facts, silently merge contradictions, or present vendor claims as verified facts.
- Do not run the restaurant pricing mission during skill-authoring or dry-run tests.
