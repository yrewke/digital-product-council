# Live Smoke Test Report

## Run

- Run ID: `2026-06-13-live-smoke-test-001`
- Date: 2026-06-13
- Workflow: repository-local restaurant research librarian only
- Hard limits: maximum 5 chat queries, 0 deep-research runs, 0 new sources
- Actual live activity: 1 attempted chat query, 0 deep research, 0 source changes

## Narrow Question

What evidence already exists in the four notebooks that helps distinguish a lightweight sellable restaurant direct-channel offer from a heavier operational service?

## Outcome

The librarian selected the provider-viability notebook as the smallest relevant first target and excluded the other three from the initial query. The exact query was recorded before execution in both the run ledger and repository ledger. The call failed with `API error (code 7): PERMISSION_DENIED`; the failure and quota uncertainty were recorded after execution. No further query was made.

No source-backed answer or NotebookLM citation was available, so the commercial evidence question remains unresolved.

## Verification Results

| Goal | Result | Observation |
|---|---|---|
| Intelligent routing | PASS | Provider-viability notebook selected first for onboarding, support, and repeatability evidence. |
| Avoid unnecessary notebook fan-out | PASS | Only one notebook was queried; all-four querying was avoided. |
| Correct spending records | PASS | Pre-query and post-query entries exist in both ledgers; denied attempt conservatively counted as one. |
| Separate evidence types and gaps | PASS | Evidence pack distinguishes repository-verified facts, inference, and unresolved notebook gaps. |
| Preserve citations | BLOCKED | No NotebookLM answer or citations were returned due to `PERMISSION_DENIED`. |
| Create compact evidence pack | PASS | `working/council-runs/2026-06-13-live-smoke-test-001/artifacts/SMOKE_TEST_EVIDENCE_PACK.md` |
| Write resumable checkpoint | PASS | Run status and next-session handoff state the exact next action and safety conditions. |
| Stop after no more than five queries | PASS | Stopped after one attempted query. |

## Guardrail Results

- No restaurant pricing mission started.
- No package prices, sales claims, or commercial verdicts produced.
- No full council or advisor agents spawned.
- No deep research run.
- No NotebookLM sources added or changed.
- No reserve account, login, profile switch, or account rotation used.
- No query was made outside the librarian workflow.

## Failures And Human Review

1. The primary account could not access the selected registered notebook through the NotebookLM connector.
2. NotebookLM did not expose whether the denied attempt counted against quota.
3. Source-level citation preservation could not be tested because no answer was returned.
4. The workspace has no `.git` directory, so the requested local Git checkpoint commit could not be created.

## Required Human Action

Confirm that the manually selected primary account has access to the registered notebook IDs. Any login or profile switch requires separate explicit approval. After access is confirmed, resume from the handoff and retry the same first query against only the provider-viability notebook.
