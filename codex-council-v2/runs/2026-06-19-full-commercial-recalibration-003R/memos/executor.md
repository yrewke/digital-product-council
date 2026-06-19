---
run_id: 2026-06-19-full-commercial-recalibration-003R
executive: Executor
memo_status: READY
revision: R1
last_updated: 2026-06-19
evidence_gate: PASSED
active_vetoes: []
---

# CURRENT_MEMO

## Assigned Question

Turn the analysis into products, qualification rules, pricing, delivery guidance, pilots, and operating limits.

## Position

Adopt a staged hybrid commercial model:

1. Ordering Page.
2. Website + Ordering.
3. Direct Orders Dashboard.
4. Direct Commerce.
5. Add-on modules.
6. Custom operations/integrations.

## Reasoning

The smallest independently valuable product is a real ordering page with Telegram order notification and local order history. It is not a lead magnet. It is useful for restaurants that need a structured link from Instagram, Google, QR, packaging, or staff prompts.

Tier 1 adds web presence. Tier 2 adds dashboard/status/menu management. Tier 3 adds commerce: payments, delivery zones, customer records, promotions, basic analytics. Modules attach by need: WhatsApp handoff/API bot, Telegram bot, catering, CRM/loyalty, QR/table, AI assistant, payment gateway, delivery integration, POS integration.

Default early delivery posture: pickup and restaurant-managed manual delivery. Third-party delivery integration, dedicated rider, and POS integration are not default; they require quote, pilot, or compatibility check.

Pricing should triangulate affordability, value, alternatives, support burden, and provider cost:

- Launch Ordering Page: AED 1,500-2,500 setup, AED 150-300/mo support/hosting, pilot discount floor AED 1,000 setup plus AED 150/mo.
- Website + Ordering: AED 3,000-5,500 setup, AED 250-500/mo.
- Direct Orders Dashboard: AED 6,000-10,000 setup, AED 500-900/mo.
- Direct Commerce: AED 10,000-18,000 setup, AED 900-1,500/mo.
- WhatsApp handoff: AED 500-1,500 setup.
- Deterministic Telegram bot: AED 2,000-5,000 setup, AED 200-500/mo.
- Deterministic WhatsApp bot: AED 4,000-9,000 setup, AED 500-1,200/mo plus pass-through.
- AI assistant: AED 6,000-15,000 setup, AED 800-2,000/mo plus AI usage cap.
- POS/delivery integration: custom quote only.

## Evidence Used

EV-0009, EV-0010, EV-0015, EV-0016, EV-0027, EV-0028, EV-0029, EV-0030.

## Assumptions

Prices are internal provisional council decisions, not public price claims. They assume one provider, bounded support, transparent third-party costs, and UAE small/independent restaurant affordability constraints.

## Risks

The provider may undercharge early to close deals and inherit recurring obligations. Every sale needs a written support allowance, pass-through policy, and custom-work boundary.

## Economic Consequences

Provider sustainability depends on recurring revenue, setup cash, and no unlimited integrations. Pilot data must measure onboarding hours, support minutes, menu-change frequency, order failures, and churn.

## What Would Change This Position

If pilots show close resistance above AED 2,000 setup for Tier 0, keep Tier 0 as a cash-entry product and move ROI-heavy selling to Tier 1/2.

## Recommendation

Take Ordering Page and Website + Ordering to pilot first. Use the ROI calculator as a diagnostic, not a promise. Refuse or custom quote delivery/POS/AI complexity until a restaurant passes readiness gates.

# EVIDENCE_REQUESTS

Originated ER-0009, ER-0010, ER-0027, ER-0028, ER-0029, ER-0030.

# FACT_CHECK

No blocking factual claim retained without evidence label.

# PEER_REVIEW

Pending anonymous review.

## [PEER_REVIEW:PR-0004:OBJECTION]
Anonymous reviewer: R-0eab6a
Comment: Objection: Price ranges need support caps and pass-through rules on the face of the offer, not buried in implementation notes.
Evidence:
Requested response: Author must accept, reject, or partially accept.

## [PEER_REVIEW:PR-0008:OBJECTION]
Anonymous reviewer: R-5b4f3e
Comment: Objection: Pricing tiers must expose minimum viable implementation details; otherwise buyers compare custom commerce work against cheap websites incorrectly.
Evidence:
Requested response: Author must accept, reject, or partially accept.

## [PEER_REVIEW:PR-0012:OBJECTION]
Anonymous reviewer: R-6d9571
Comment: Objection: Executor prices look commercially usable but need explicit pilot learning goals and stop conditions for each tier.
Evidence:
Requested response: Author must accept, reject, or partially accept.

## [PEER_REVIEW:PR-0016:OBJECTION]
Anonymous reviewer: R-efb7f2
Comment: Objection: Executor package model should name what is not included: POS, delivery guarantees, ad spend, marketplace replacement, and unlimited support.
Evidence:
Requested response: Author must accept, reject, or partially accept.

# AUTHOR_RESPONSES

None.

## [AUTHOR_RESPONSE:AR-0005]
Responds to: PR-0004,PR-0008,PR-0012,PR-0016
Disposition: ACCEPTED
Reason: Reviews correctly require visible support caps, exclusions, pilot stop conditions, and implementation minimums.
Change made: Package and pricing model will put pass-throughs, exclusions, caps, and pilot learning goals on the face of the offer.

# VETOES

None.

## [VETO:V-0001:POST_CHAIR]
Holder: auditor
Protected domain: factual and numerical validity
Challenged statement: Use internal launch prices only, not public guaranteed pricing.
Reason: This is directionally correct but insufficient unless the final model also labels every material number, exposes support caps, separates pass-through costs, and marks pilot-validation assumptions.
Evidence: FC-0023 through FC-0032 and EV-0004, EV-0015, EV-0016, EV-0027, EV-0028 require numeric labels, support caps, pass-throughs, and pilot replacement measurements.
Required remedy: Final verdict and artifacts must include number labels, support caps, pass-throughs, and pilot validation.
Verification method: contains_text
Status: OPEN
Validation: valid scoped veto

# REVISION_LOG

R1: Initial independent memo after evidence retrieval.
