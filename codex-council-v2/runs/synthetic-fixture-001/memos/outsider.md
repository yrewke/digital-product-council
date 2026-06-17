---
run_id: synthetic-fixture-001
executive: outsider
memo_status: READY
revision: R2
last_updated: 2026-06-17
evidence_gate: PASSED
active_vetoes: []
---

# CURRENT_MEMO

## Assigned Question
Synthetic fixture decision.

## Position
The buyer will compare this to doing nothing unless the first step is concrete.

## Reasoning
This memo applies the outsider lens to synthetic fixture facts and keeps the decision bounded.

## Evidence Used
- [EVIDENCE_RESPONSE:EV-0001] Fixture demand cap.
- [EVIDENCE_RESPONSE:EV-0002] Support budget correction.

## Assumptions
- Synthetic facts are fixtures, not real market evidence.

## Risks
- Fixture evidence could fail outside the test.

## Economic Consequences
No unsupported material numbers.

## What Would Change This Position
Different support budget or failure threshold evidence.

## Recommendation
Choose the bounded pilot with explicit failure criteria.

# EVIDENCE_REQUESTS

## [EVIDENCE_REQUEST:ER-0001]
Status: ANSWERED
Question: What is fixture demand?
Decision affected: pilot size
Response IDs: EV-0001

# FACT_CHECK

## [FACT_CHECK:FC-0001:BLOCKING]
Claim: The fixture has 200 support hours/month.
Finding: False numerical claim; fixture support budget is 20 hours/month.
Evidence: EV-0002
Required correction: Replace 200 with 20 or downgrade claim.
Status: NOT_APPLICABLE

# PEER_REVIEW

## [PEER_REVIEW:PR-0004:OBJECTION]
Anonymous reviewer: R-4
Comment: Strongest insight recorded; weakest assumption challenged.
Evidence: EV-0001
Requested response: Clarify failure criteria.

# AUTHOR_RESPONSES

## [AUTHOR_RESPONSE:AR-0004]
Responds to: PR-0004
Disposition: ACCEPTED
Reason: The correction improves boundedness.
Change made: Added failure criteria and support cap.

# VETOES

## [VETO:V-0002:PRE_CHAIR]
Holder: Outsider
Protected domain: brand preference
Challenged statement: Use plain fixture naming.
Reason: Not an authorized protected domain.
Evidence: none
Required remedy: none
Status: DEMOTED_TO_OBJECTION

# REVISION_LOG

## [REVISION:R2]
Summary: No correction required.
Reason: Pre-chair review and audit.
Resolved IDs: FC-0001, PR-0004
Remaining disagreement: bounded upside value.
