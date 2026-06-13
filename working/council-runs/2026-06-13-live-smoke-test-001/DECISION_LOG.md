# Decision Log

## D-001 - Librarian-only execution

- Decision: Do not spawn the commercial council or advisor agents.
- Basis: Operator instruction and smoke-test objective.
- Status: Active.

## D-002 - Initial notebook routing

- Decision: Query only the UAE Restaurant Direct-Ordering Product-Market Fit notebook first.
- Included because: Its boundary explicitly covers onboarding, support, retention, and provider-side repeatability, which directly distinguish lightweight products from heavier services.
- Excluded initially:
  - Restaurant Website and Direct-Ordering Competitors: conditionally useful for a second query if offer/service boundary evidence remains unclear.
  - UAE Third-Party Restaurant Delivery Companies Research: delivery operations are only one possible heavy-service boundary and are not needed for the first query.
  - Restaurant Website ROI Research - Consolidated: restaurant value and economics do not directly answer the operational-scope distinction.
- Status: Active.

## D-003 - Budget interpretation

- Decision: Treat the explicit five-query run ceiling as the available estimated daily budget because the actual account daily quota is unknown.
- Limitation: Remaining daily budget is a conservative run-local proxy, not an observed NotebookLM quota.
- Status: Active.

## D-004 - Stop after permission failure

- Decision: Stop live NotebookLM retrieval after the first `PERMISSION_DENIED` response.
- Basis: The failure indicates an account/access blocker rather than an evidence gap; querying another notebook under the same profile would risk wasting budget and would not test intelligent routing.
- Budget treatment: Conservatively count the failed attempt as one query, leaving four run-authorized queries.
- Status: Active.

## D-005 - Do not initialize Git repository

- Decision: Do not run `git init` merely to satisfy the requested checkpoint commit.
- Basis: The workspace is not currently a Git repository; initializing repository metadata is a broader setup change that was not explicitly authorized.
- Result: Local commit remains blocked and is recorded for human review.
- Status: Active.
