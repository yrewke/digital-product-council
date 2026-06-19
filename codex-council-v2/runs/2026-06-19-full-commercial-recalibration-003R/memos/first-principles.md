---
run_id: 2026-06-19-full-commercial-recalibration-003R
executive: First-Principles
memo_status: READY
revision: R1
last_updated: 2026-06-19
evidence_gate: PASSED
active_vetoes: []
---

# CURRENT_MEMO

## Assigned Question

Rebuild the commercial model from variables and causal mechanics.

## Position

The model must be a hybrid of product tiers, optional modules, and restaurant-specific ROI calculation. Fixed tiers alone hide delivery and integration variance; pure modular pricing is too hard to buy.

## Reasoning

The restaurant value equation has separate channels:

1. Incremental new direct orders.
2. Marketplace orders shifted to direct.
3. Phone/WhatsApp orders converted to structured orders.
4. Pickup orders.
5. Direct delivery orders.
6. Catering and enquiry revenue.

Only the first is new revenue. Shifted orders create margin delta. Structured phone/WhatsApp orders create operational value and data quality. Catering enquiries create pipeline, not revenue until won. Staff time is not cash unless hours are reduced or redeployed.

Per-order contribution should be:

`AOV - food_cost - packaging - payment_fee - delivery_cost - direct_incentive - loyalty_reward - direct_marketing_cost - incremental_support_cost`.

For shifted marketplace orders, compare this with:

`AOV - food_cost - packaging - marketplace_commission - marketplace_fees - marketplace_promo_cost`.

Provider economics require:

`setup_fee + gross_margin_on_recurring - onboarding_labor - support_labor - hosting - messaging - AI - payment/dispute/admin - integration_maintenance - churn_loss`.

## Evidence Used

EV-0003, EV-0004, EV-0015, EV-0016, EV-0017, EV-0018, EV-0027, EV-0028, EV-0030.

## Assumptions

Use scenario variables rather than false precision: food contribution margin 35%-60%; effective marketplace burden 18%-35%; direct delivery AED 12-35 per order depending model; direct incentive 0%-15%; payment 2.9% + AED 1 when online card is used.

## Risks

The model can still be gamed by selecting only optimistic migration and AOV lift assumptions. The ROI tool must expose sensitivity.

## Economic Consequences

Tier 0/1 can be affordable because they avoid payments, delivery API, POS, and auth. Tier 2/3 need recurring fees because support and operational responsibility rise sharply.

## What Would Change This Position

Reliable UAE pilot data on migration, support minutes, delivery cost, and restaurant willingness to pay by archetype.

## Recommendation

Adopt conservative/base/optimistic ROI scenarios with transparent labels. Use pilot measurement to replace migration, incentive, delivery, and support variables.

# EVIDENCE_REQUESTS

Originated ER-0003, ER-0004, ER-0015, ER-0016, ER-0017, ER-0018.

# FACT_CHECK

No blocking factual claim retained without evidence label.

# PEER_REVIEW

Pending anonymous review.

## [PEER_REVIEW:PR-0001:OBJECTION]
Anonymous reviewer: R-0eab6a
Comment: Objection: ROI mechanics are correct but need explicit channel-mix outputs by restaurant archetype, otherwise the formula can still be sold as a universal calculator.
Evidence:
Requested response: Author must accept, reject, or partially accept.

## [PEER_REVIEW:PR-0010:OBJECTION]
Anonymous reviewer: R-6d9571
Comment: Objection: First-principles model should include delivery capacity constraints as a hard gate before direct delivery ROI is calculated.
Evidence:
Requested response: Author must accept, reject, or partially accept.

## [PEER_REVIEW:PR-0014:OBJECTION]
Anonymous reviewer: R-efb7f2
Comment: Objection: Formula memo should explain which variables are verified facts, supported estimates, planning assumptions, and pilot variables.
Evidence:
Requested response: Author must accept, reject, or partially accept.

## [PEER_REVIEW:PR-0018:OBJECTION]
Anonymous reviewer: R-b1033a
Comment: Objection: First-principles ROI model should output payback only after restaurant-specific data, not from generic default assumptions.
Evidence:
Requested response: Author must accept, reject, or partially accept.

# AUTHOR_RESPONSES

None.

## [AUTHOR_RESPONSE:AR-0002]
Responds to: PR-0001,PR-0010,PR-0014,PR-0018
Disposition: ACCEPTED
Reason: Reviews correctly require archetype-specific channel mix, delivery gates, assumption labels, and payback only from restaurant inputs.
Change made: ROI model will separate verified facts, supported estimates, planning assumptions, scenario variables, and pilot validation items.

# VETOES

None.

# REVISION_LOG

R1: Initial independent memo after evidence retrieval.
