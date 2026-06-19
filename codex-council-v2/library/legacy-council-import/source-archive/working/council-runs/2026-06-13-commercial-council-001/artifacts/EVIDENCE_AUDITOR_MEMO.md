# Evidence Auditor Memo

**Run:** `2026-06-13-commercial-council-001`  
**Stage:** Evidence Auditor  
**Scope audited:** Prepared evidence pack, `EVIDENCE_LEDGER.md`, `ASSUMPTION_LEDGER.md`, five advisor memos, five anonymous peer reviews, and `DEVILS_ADVOCATE_MEMO.md`.  
**Role restriction:** This memo audits claims and numbers. It does not vote, select the offer, set prices, or write the commercial verdict.

## Executive Audit

The packet is sufficient to support a bounded Run 1 pilot thesis and explicit exclusions. It is not sufficient to establish a smallest sellable package, a commercially superior pickup-first offer, standalone-core usefulness, profitable aggregator coexistence, a preferred pricing model, self-service adoption, or one-developer repeatability.

The council generally labels weaknesses correctly, but repeated use of the same direction across memos must not be mistaken for independent evidence. The recurring direction of a standardized owned channel, pickup-first testing, deferred delivery/POS, bounded setup plus subscription, self-service administration, and one-developer delivery is a linked set of **scenario assumptions and inferences**. It remains constrained by `A-001`, `A-002`, `A-003`, `GAP-005`, and `GAP-006`.

The strongest evidence supports only these bounded facts:

- Aggregator commissions and associated fees can compress restaurant margins, and some GCC operators object to lost customer data/control. Magnitude and current contract applicability vary (`E-005`).
- Timeliness and order accuracy were important retention determinants in one UAE study of 100 respondents aged 18-25. This cannot be generalized to all UAE restaurant customers (`E-003`).
- Staging and webhook status flows can technically validate integrations before live delivery. This does not validate restaurant operations, service levels, or economics (`E-010`).
- Generic SaaS evidence associates low-ARPA/SMB models with weaker retention. It cannot validate UAE restaurant-provider churn, pricing, or profitability (`E-024`).

No numeric ROI, conversion, channel-shift, payback, willingness-to-pay, setup labor, support allowance, churn, gross-margin, or final pricing claim is supported.

## Evidence-Boundary Rules

The Chairman and any later deliverable must keep the following evidence boundaries explicit:

| Boundary | Permitted use | Prohibited silent generalization |
|---|---|---|
| UAE evidence | Describe the cited UAE sample, provider capability, or vendor claim with its limitation. | Do not generalize a small young-adult study or UAE vendor claim to the full UAE restaurant market. |
| GCC evidence | Establish that a concern or pattern exists in the cited GCC context. | Do not present GCC evidence as current UAE segment economics or buyer behavior. |
| Global evidence | Identify available product models, capabilities, alternatives, or tensions. | Do not treat global capabilities or outcomes as UAE adoption, willingness-to-pay, or profitability evidence. |
| Generic SaaS evidence | Use as cautionary boundary evidence about low-ARPA/SMB retention risk. | Do not use it as UAE restaurant SaaS churn, ARPA, CAC, margin, or pricing evidence. |
| Vendor claims | Describe what vendors claim or make available. | Do not state capability, uplift, SLA, migration ease, support quality, or rapid launch as independently verified outcomes. |

## Evidence Ledger Audit

| ID | Auditor classification | Boundary | Audit finding and restriction |
|---|---|---|---|
| `E-001` | **Vendor claim** | UAE/GCC | The roughly **75% aggregator / 25% owned-channel or call-center split** is not an independently verified market fact. Scope and representativeness are unclear. Safe only as a cited vendor/industry estimate. |
| `E-002` | **Vendor claim** | Global | The **35% higher AOV, 112% reorder increase, and 18-23% higher repeat visits** figures are unsafe for UAE sales, forecasts, or ROI claims. They may be mentioned only as unverified vendor-style claims. |
| `E-003` | **Verified fact** | UAE, limited sample | Safe only as: one UAE convenience-sample study of **100 people aged 18-25** found timeliness and accuracy important to retention. It does not prove pickup-first demand, delivery performance, or full-market behavior. |
| `E-004` | **Inference** | UAE/GCC | QSR, fast-casual, and neighborhood concepts as stronger-fit segments is a plausible targeting hypothesis, not measured product fit, conversion, willingness-to-pay, or retention. |
| `E-005` | **Verified fact** | GCC | Safe to state that commissions/fees can compress margins and some operators object to lost data/control. Unsafe to claim a current UAE commission rate, guaranteed savings, or that direct ordering improves net margin. |
| `E-006` | **Contradiction** | GCC | Loyalty-program availability conflicts with reported consumer use. Loyalty value is unresolved and cannot be treated as an obvious core benefit. |
| `E-007` | **Vendor claim** | UAE/GCC | **Half of surveyed diners preferring BOGO** and **double-digit basket uplift** do not establish profitable demand, retention, or a safe promotion strategy. |
| `E-008` | **Vendor claim** | UAE | Integration capability is available according to vendors. It does not prove restaurant readiness, implementation success, low burden, or reliability. |
| `E-009` | **Inference** | UAE/GCC | Interdependent delivery-failure chains and the importance of status discipline are plausible but rely on indirect vendor discussion. Use as a risk hypothesis, not an observed failure-rate claim. |
| `E-010` | **Verified fact** | Generic SaaS/UAE technical capability | Technical staging/webhook validation is possible. It is only a technical gate and cannot support claims about operational readiness, SLA performance, adoption, or economics. |
| `E-011` | **Scenario assumption** | UAE | On-time, first-attempt success, replacement latency, and peak performance are reasonable pilot metrics. Any **99%**, **96%**, or replacement-performance threshold is a vendor claim, not a validated standard or promise. |
| `E-012` | **Vendor claim** | UAE | Outsourced fleets claim to shift fleet management and scale peaks. Unsafe to imply that restaurant/provider accountability, compliance exposure, or peak risk disappears. |
| `E-013` | **Contradiction** | UAE | Provider delivery-time promises differ and do not establish observed performance. No fixed delivery-time or reliability promise is safe. |
| `E-014` | **Vendor claim** | UAE/GCC/global | First-party data and branded control are available capabilities. They do not prove customer use, incremental profit, superior experience, or channel shift. |
| `E-015` | **Vendor claim** | UAE/global | WhatsApp reach and automation capability are vendor-reported. Its operational scalability and relative effectiveness remain unresolved. |
| `E-016` | **Vendor claim** | GCC/global | QR ordering may reduce manual work, but spend, tip, and turnover uplifts are unsafe outcome claims. QR and off-premise owned ordering are different jobs unless a buyer use case links them. |
| `E-017` | **Vendor claim** | Global | POS-integrated SaaS capability exists. No claim is supported about ease, burden, UAE fit, implementation success, or whether integration is required for retention. |
| `E-018` | **Contradiction** | UAE/global | Aggregators provide reach while direct ordering may not improve customer price or experience. Any general superiority or replacement claim is unsafe. |
| `E-019` | **Vendor claim** | UAE/global/generic SaaS | Aggregator/direct coexistence is an available strategy. Successful migration, profitable shift, and migration ease are unquantified. |
| `E-020` | **Inference** | UAE/GCC | Digital/social discovery and contribution-margin discipline do not establish an efficient acquisition channel for this provider. Founder-led qualification is a scenario assumption, not a validated CAC strategy. |
| `E-021` | **Vendor claim** | UAE/GCC | Rapid standardized launch is vendor-reported; manual setup and mapping burden are acknowledged. No launch-time, labor-hour, or revision-cycle claim is safe. |
| `E-022` | **Vendor claim** | UAE | Competitors advertise broad support models. This does not establish buyer requirements, actual service quality, ticket load, cost, or acceptance of business-hours support. |
| `E-023` | **Contradiction** | Global | Personalization demand conflicts with standardization. The acceptable UAE customization boundary and its effect on close rate and retention are unresolved. |
| `E-024` | **Verified fact** | Generic SaaS only | Safe as a caution that low-ARPA/SMB SaaS often has weaker retention. Unsafe as a claim about UAE restaurant SaaS churn, suitable price level, or this provider's economics. |
| `E-025` | **Vendor claim** | Global/UAE | Subscription, hybrid, and commission-free-positioned models exist. Their existence does not establish the preferred model, willingness-to-pay, recurring value, or provider profitability. |
| `GAP-005` | **Unresolved gap** | UAE | Incremental direct conversion, profitable channel shift, restaurant payback, and direct-customer retention remain unquantified. Blocks economic and outcome promises. |
| `GAP-006` | **Unresolved gap** | UAE | CAC, sales effort, onboarding labor, support load, churn, cost-to-serve, and gross margin by segment/package remain unavailable. Blocks profitability, repeatability, support, and pricing conclusions. |

## Material Council-Claim Audit

| Material claim or direction | Classification | Audit disposition |
|---|---|---|
| Pickup is the strongest first workflow. | **Inference / scenario assumption** | Operationally plausible because it avoids delivery dependencies, but no evidence proves buyer demand, willingness-to-pay, retention, reachable pickup demand, or provider economics. Safe only as a Run 1 test configuration. |
| Pickup-first is commercially safer. | **Inference** | It may reduce fulfilment dependencies, but could create a weak second queue and lose to WhatsApp, aggregators, POS ecosystems, or doing nothing. "Safer" must be limited to a narrower operational test, not a commercial conclusion. |
| A standalone core is useful without delivery or POS integration. | **Unresolved gap / scenario assumption** | This is `A-003`. The packet repeatedly acknowledges that the offer may add reconciliation work or be too weak to buy and retain. It must not be treated as established. |
| Delivery and POS should be deferred. | **Scenario assumption** | Deferral can bound early complexity, but may defer the capabilities required to make the workflow authoritative and useful. Safe as a Run 1 scope control, not a validated package boundary. |
| Delivery and POS are natural add-ons. | **Inference** | They are separable responsibility areas, but no evidence establishes buyer acceptance, add-on economics, integration burden, or retention value. |
| Aggregators can remain discovery channels while the owned channel captures repeat demand. | **Scenario assumption** | This is `A-002`. Coexistence is available; profitable repeat-demand capture is unproven. Do not state that aggregators actually function as discovery and the owned channel captures repeat demand for this offer. |
| The offer should target QSR, fast-casual, and neighborhood restaurants. | **Inference** | Safe as an initial recruitment hypothesis. Unsafe as proven segment fit or as grounds for conversion, price, retention, or margin claims. |
| Premium/fine dining and exposed mid-market casual are poor fits. | **Inference** | Safe only as lower-priority hypotheses from `E-004`; not a categorical exclusion supported by direct product evidence. |
| A standardized product can serve multiple UAE restaurant segments. | **Scenario assumption** | This is `A-001`; `E-023` directly preserves the personalization/standardization contradiction. |
| Package boundaries should follow responsibility and operational burden. | **Inference** | A defensible design principle supported by the identified risk categories, but not evidence that buyers will accept or pay for the resulting packages. |
| Bounded setup plus recurring subscription is the preferred direction. | **Scenario assumption** | `E-025` only proves model existence. No evidence establishes willingness-to-pay, recurring value, retention, provider margin, or that setup labor can be bounded. Treat as a pricing experiment, not a preferred validated model. |
| Separately priced finite add-ons will contain labor variance. | **Scenario assumption** | Scoping can expose labor, but no evidence shows buyers will accept add-on pricing or that work remains finite in practice. |
| Per-order pricing should be deferred. | **Inference** | Reasonable because channel shift and variable responsibility are unproven, but no comparative pricing-model evidence establishes the best deferral decision. |
| Self-service can contain recurring provider work. | **Scenario assumption / unresolved gap** | Self-service is a required proposed boundary, not validated restaurant behavior. Adoption failures, restaurant discipline, and provider interventions must be measured under `GAP-006`. |
| One named shift owner and fallback will make the workflow reliable. | **Scenario assumption** | A reasonable operational control, but no evidence shows target restaurants can sustain it or that it is sufficient during peaks. |
| One authoritative queue reduces work. | **Inference** | Plausible, but the proposed non-integrated core may not create one authoritative queue. Actual labor reduction and reconciliation burden are unmeasured. |
| A one-developer provider can repeatedly sell and service the bounded offer. | **Unresolved gap / scenario assumption** | No capacity, continuity, recovery, acquisition, onboarding, support, or gross-margin evidence establishes repeatability. `GAP-006` blocks this conclusion. |
| Founder-led qualification will keep early CAC observable and reject poor fits. | **Scenario assumption** | It creates a measurement method but is not evidence of efficient acquisition or repeatability. |
| Business-hours support is commercially sustainable or acceptable. | **Scenario assumption** | No evidence establishes buyer acceptance, actual incident urgency, support load, or the provider's ability to cover restaurant operating hours. |
| A controlled pilot can resolve the major unknowns. | **Inference** | A well-designed multi-account pilot can generate relevant primary evidence. A single favorable launch cannot resolve segment fit, repeatability, churn, or unit economics. |

## Number Audit

| Number or numeric direction | Classification | Restriction |
|---|---|---|
| Roughly **75% / 25%** aggregator versus owned/call-center share | **Vendor claim** | Do not present as verified UAE market share or use in forecasts. |
| **35% AOV**, **112% reorder**, **18-23% repeat-visit** uplift | **Vendor claim** | Unsafe for any outcome, ROI, forecast, or sales claim. |
| UAE study **N=100**, ages **18-25** | **Verified fact** | Must accompany any use of `E-003`; prevents generalization to the UAE market. |
| BOGO preferred by **half** of surveyed UAE diners | **Vendor claim** | Does not prove profitable promotion demand or fit for the proposed offer. |
| "Double-digit" combo basket uplift | **Vendor claim** | Unsafe outcome claim; detail and applicability are undisclosed. |
| Delivery performance figures such as **99%** and **96%** | **Vendor claim** | May inform candidate pilot measures only; never promise or state as observed performance. |
| **24/7** support availability | **Vendor claim** | Describes competitor positioning, not required support scope, quality, or economically sustainable coverage. |
| One designated customer owner, one review cycle, bounded content import, fixed launch path | **Scenario assumption** | These are proposed scope controls, not evidence-backed labor allowances or accepted buyer terms. |
| Multiple normal periods and at least **two** representative peak periods | **Scenario assumption** | A proposed pilot design, not a validated sufficiency threshold. A broader pilot portfolio is needed for generalization. |
| No final package price or price range appears in the packet | **Verified fact** | Any previous or future price must remain an anchor or hypothesis until `GAP-005` and `GAP-006` are measured. |

## Contradictions That Must Be Preserved

1. **Operational safety versus commercial usefulness:** Pickup-first and non-integrated scope may reduce dependency risk, but may be too weak to buy, retain, or operate without adding a second queue (`A-003`).
2. **Aggregator coexistence versus economic reason to buy:** Coexistence avoids an unsafe replacement claim, but profitable direct-channel shift remains unproven (`E-018`, `E-019`, `GAP-005`).
3. **Standardization versus local personalization:** Tight boundaries protect one-developer repeatability, while customization may be necessary to close or retain accounts (`E-023`, `A-001`, `GAP-006`).
4. **Self-service versus restaurant operating discipline:** Self-service protects provider capacity, but restaurants may fail to maintain menus, availability, statuses, users, or promotions (`GAP-006`).
5. **Deferring integrations versus authoritative workflow:** Delivery/POS deferral reduces early implementation and SLA exposure, but may preserve manual reconciliation and reduce standalone value (`E-017`, `E-021`, `A-003`).
6. **Recurring subscription versus unproven recurring value:** A subscription can align with ongoing service, but willingness-to-pay, retention, cost-to-serve, and margin are unknown (`E-024`, `E-025`, `GAP-006`).
7. **Narrow scope versus provider economics:** A narrow core may be repeatable but unable to command enough revenue; broader add-ons may create the support and integration burden the model is designed to avoid (`GAP-006`).

## Claims Safe Enough for Run 1

The following are safe only as internal pilot framing or carefully bounded customer language:

- "This is a controlled pilot of an owned ordering channel; it is not an aggregator-replacement promise."
- "Aggregators can remain in use while the restaurant tests whether some suitable customers choose a direct route." The second clause must remain a test, not an expected outcome.
- "Pickup-first is the initial test scope because it removes delivery-partner dependencies and makes operational behavior easier to observe." Do not call it the strongest commercial offer.
- "Delivery and POS integration are outside the initial scope and may be reconsidered if the pilot shows they remove more burden than they introduce."
- "The product can provide a branded direct-ordering capability and access to first-party customer data." Do not imply adoption, ownership free of legal constraints, profit, or superior experience.
- "The pilot will measure direct usage, restaurant workload, operational reliability, support demand, and provider effort."
- "QSR, fast-casual, and neighborhood restaurants are initial recruitment hypotheses, not proven best-fit segments."
- "Commercial terms and responsibility boundaries will be explicit and bounded." This is safe only if the actual terms are drafted and applied; the current packet does not validate them.
- "No conversion, savings, ROI, payback, delivery-time, labor-saving, or channel-shift outcome is guaranteed."

## Claims That Must Wait for Run 2 or Primary Validation

### Blocked by `GAP-005`

- Pickup-first or the standalone core creates meaningful restaurant value.
- Customers will adopt the owned channel or shift from aggregators.
- Aggregator coexistence produces profitable repeat-order capture.
- The offer increases orders, AOV, reorders, repeat visits, loyalty, or customer retention.
- The offer saves commission expense on a net basis.
- The offer produces incremental profit, a payback period, or positive ROI.
- QSR, fast-casual, or neighborhood restaurants have superior conversion or willingness-to-pay.
- Promotions, loyalty, first-party data, or brand control create measurable economic value.
- Any per-order, performance, or value-based pricing rationale.

### Blocked by `GAP-006`

- The provider can repeatedly acquire, onboard, support, and retain restaurants profitably.
- A one-developer operating model is viable, resilient, or scalable.
- Setup work, review cycles, customization, training, and support can be bounded at the proposed levels.
- Restaurants will reliably self-serve routine administration.
- Business-hours support is accepted and sufficient.
- A standardized product will avoid becoming a custom-development service.
- A bounded setup charge plus recurring subscription is the preferred or profitable pricing model.
- Add-ons can be scoped and priced profitably.
- Low-price or low-ARPA positioning is viable.
- Delivery/POS deferral improves provider economics, or their later addition creates net value.

### Requires Primary Operational or Contractual Validation

- Pickup-first creates one authoritative queue or reduces restaurant labor.
- Staff can maintain availability, acceptance, status, handoff, and exception discipline during normal and peak periods.
- Delivery partner performance meets any threshold in live conditions.
- Responsibility for failures, refunds, outages, data handling/export, cancellations, migrations, and exit is clear and accepted.
- The provider has workable continuity and incident coverage despite one-developer concentration risk.

## Unsafe Sales Claims

The following claims are unsafe and must not appear in customer-facing material unless later supported by appropriately scoped primary evidence:

- "Reduce commissions," "save money," or "improve margins" without a restaurant-specific net-cost comparison.
- "Move repeat customers off aggregators," "own repeat demand," or any migration-rate claim.
- "Increase orders, AOV, repeat orders, repeat visits, loyalty, retention, or profit."
- "Fast," "rapid," "easy," or fixed-time launch without measured onboarding distributions and stated restaurant dependencies.
- "No integration needed," "standalone core is enough," or "pickup-first is the best package."
- "Seamless POS/delivery integration," "reliable delivery," "guaranteed delivery time," or vendor SLA figures presented as provider performance.
- "Reduce staff work," "fewer errors," "one authoritative queue," or "self-service" as an achieved outcome.
- "Built for QSR/fast casual/neighborhood restaurants" if it implies proven segment outcomes.
- "Scalable," "repeatable," "profitable," or "sustainable for one developer."
- "24/7 support," guaranteed resolution times, unlimited customization, unlimited revisions, or dedicated success coverage.
- "Commission-free" if third-party, payment, fulfilment, provider, incentive, or operating costs make the phrase misleading.
- Any final package price, price range, ROI calculator, payback period, or savings estimate derived from the current packet.

## Minimum Evidence Gates

No broad commercial claim should advance beyond Run 1 until primary validation records, by restaurant archetype and package boundary:

- Restaurant choice against aggregators, WhatsApp, relevant POS/order ecosystems, and doing nothing.
- Incremental or demonstrably shifted orders and net contribution after incentives, payment, fulfilment, staff, and service costs (`GAP-005`).
- Pickup and standalone-core usage, operational burden, manual reconciliation, peak deterioration, errors, cancellations/refunds, and retention.
- Acquisition effort/CAC, sales-cycle length, onboarding labor, restaurant delays, revision cycles, training, support minutes, recurring provider interventions, custom requests, infrastructure/vendor costs, churn signals, and contribution margin (`GAP-006`).
- Self-service completion and failure rates.
- Delivery/POS add-on burden and net value before either becomes a standard package claim.
- Accepted responsibility, refund, outage, data portability, cancellation, migration, and exit terms.
- Continuity and incident-response coverage appropriate to restaurant operating hours.

A single favorable pilot may validate that one configuration can work for one restaurant. It cannot establish segment fit, repeatable provider economics, a preferred pricing model, or general customer outcomes.

## Auditor Restrictions for Chairman Synthesis

1. Preserve pickup-first as a proposed Run 1 test configuration, not a confirmed smallest useful or sellable offer.
2. Preserve standalone-core usefulness as unresolved under `A-003`.
3. Preserve aggregator coexistence as positioning and a testable scenario, not a proven channel-shift strategy.
4. Preserve delivery/POS deferral as a scope-control hypothesis with an explicit risk that deferral removes required usefulness.
5. Preserve subscription/setup-plus-recurring as a pricing-model experiment. Do not call it preferred, validated, or profitable.
6. Preserve segment fit as an inference and recruitment hypothesis.
7. Preserve self-service and one-developer repeatability as unresolved provider-side assumptions under `GAP-006`.
8. Treat all prior or future prices as anchors or hypotheses until primary evidence supports willingness-to-pay, restaurant value, and provider economics.
9. Do not import UAE, GCC, global, generic SaaS, or vendor evidence across boundaries without naming the boundary and limitation.
10. Do not convert repeated advisor agreement into evidence strength.
