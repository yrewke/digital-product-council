# Full Restaurant ROI Map

## Core Economic Rule

Owned-channel ROI is not one number. It is the sum of measurable gains and protected losses, minus channel, fulfilment, promotion, payment, staff, support, and failure costs.

`Monthly net impact = shifted-order savings + incremental-order contribution + pickup contribution + operational savings + won lead contribution + other measured gains - system/support/API costs - new fulfilment costs - promotion costs - failure/refund costs`

Shifted orders and incremental orders must remain separate. A shifted aggregator order is not new revenue. An incremental order is not automatically commission savings.

## Direct Financial ROI

| ROI path | Mechanism | Quantification | Strength | Customer-safe treatment |
|---|---|---|---|---|
| Repeat orders shifted from aggregator | Avoid some marketplace deductions while keeping aggregator for discovery | Shifted orders x AOV x avoided fee rate, less payment/delivery/promotion deltas | Strongest when actual deductions and repeat capture are known | Show as scenario, never guaranteed |
| Incremental direct orders | Converts otherwise lost or unplaced demand | Incremental orders x AOV x contribution margin after variable costs | Strong only with tracked source/incrementality | Owner-entered assumption; conservative default |
| Pickup orders | Avoids delivery expense and may capture nearby demand | Pickup orders x avoided delivery cost, adjusted for discounts/packing | Strong and explainable | Safe model with editable costs |
| Higher basket through structured menu | Modifiers, combos, clear categories, family trays | Direct orders x AOV x assumed uplift x contribution margin | Vendor-claim-heavy | Default uplift should be 0%; optional scenario |
| Catering/family-tray enquiries | Website/form converts high-ticket enquiries | Won incremental enquiries x average ticket x contribution margin | Strong for relevant archetypes, weak elsewhere | Separate module, owner inputs required |
| Delivery-fee and zone control | Avoids undercharging distant/low-value orders | Orders affected x corrected fee or avoided loss | Strong if current leakage exists | Safe when based on owner records |
| Discount control | Avoids blanket marketplace promotions or targets offers | Orders x reduction in discount percentage | Strong if restaurant currently funds discounts | Explicit input, not assumed |
| Payment collection | Reduces cash friction or no-shows, but adds gateway fee | Incremental completed orders benefit less gateway fees/refunds | Conditional | Show cost first; upside optional |

## Operational ROI

| ROI path | Mechanism | Quantification | Strength | Risk |
|---|---|---|---|---|
| Fewer missed WhatsApp/phone orders | Structured queue and required fields | Recovered orders x contribution/order | Medium; requires baseline logging | Staff may ignore new queue |
| Fewer order mistakes | Structured item IDs, totals, address, notes | Avoided errors x average correction/refund cost | Medium | Errors can move to menu setup or kitchen |
| Staff-time reduction | Less manual menu explanation, total calculation, address collection | Orders x minutes saved x loaded hourly value / 60 | Medium | Time saved may not convert to cash |
| Faster customer browsing | Self-service menu and clear availability | Optional conversion input; track completion | Weak as monetary default | Usability can be poor |
| Lost-order prevention | Order history and acknowledgement | Recovered contribution plus complaint avoidance | Medium | Requires notification reliability |
| Support clarity | Status and structured records reduce disputes | Avoided support minutes/refunds | Medium-low | Status discipline creates work |
| Operational reporting | Channel, item, source, status history informs decisions | Quantify only through measured action | Qualitative/semi-quantitative | Reports may not be used |
| POS workflow | Avoids duplicate entry only where compatible | Orders x duplicate-entry minutes/errors avoided | Conditional | Integration cost/support may exceed savings |
| Bot-assisted ordering | Handles repeated questions and guides cart | Contained conversations x minutes saved plus incremental conversion | Conditional | AI errors, escalation, API cost |

## Marketing and Trust ROI

| ROI path | Mechanism | Quantification | Strength | Calculator treatment |
|---|---|---|---|---|
| Website credibility / legitimacy | Consistent branded destination with menu, hours, location | Track visits, menu views, calls, enquiries, orders | Real but causality weak | Score and optional owner assumption; no automatic AED uplift |
| Google presence | Structured website can clarify business details and support search eligibility | Track impressions/clicks/actions | Medium for visibility, weak for revenue causality | Non-monetary KPI plus optional conversion |
| Instagram/social destination | Converts profile interest into clear menu/order/enquiry path | Social clicks x completion rate x contribution | Medium when traffic exists | Owner-entered traffic and conversion |
| QR destination | Packaging/table/card QR routes repeat customers | Scans x order/enquiry conversion x contribution | Medium and measurable | Include as traffic source |
| Menu clarity | Reduces uncertainty and questions | Measure abandonment, questions, errors | Medium operationally | Avoid generic conversion claim |
| Shareability | Customers share stable menu/order link | Track referred sessions/orders | Low-medium | Track, no default revenue |
| Reservation/enquiry capture | Captures non-order intent | Won leads x contribution/value | Archetype-specific | Separate optional module |

## Customer-Data and Strategic ROI

| ROI path | Value | Monetization rule | Strength |
|---|---|---|---|
| First-party customer records | Enables repeat contact, service recovery, and cohort measurement | Monetary value only through measured repeat campaigns/orders | Strategic, not automatic cash |
| Repeat behavior visibility | Shows reorder rate, preferred items, order intervals | Use for decisions and measured campaign response | Medium |
| Promotion testing | Tests offers without marketplace-only dependency | Measure incremental contribution after discount | Medium |
| Reduced marketplace dependency | Protects optionality and direct relationship | Treat as risk score, not guaranteed AED | Strategic |
| Brand/customer relationship | Direct service recovery and feedback | Track repeat and complaint outcomes | Strategic |
| Channel resilience | Multiple customer doors reduce single-channel failure exposure | Qualitative risk protection | Strategic |

## Money at Risk

- Setup and recurring support cost may exceed realized value.
- Shifted orders may receive direct-channel discounts that erase avoided commission.
- Direct delivery may cost more than marketplace fulfilment.
- Pickup can create queue congestion, packaging cost, and customer no-shows.
- Staff can miss or mishandle a second order queue.
- Incorrect menu/availability creates refunds and trust damage.
- Payment gateway, dispute, WhatsApp, AI, POS, and delivery-provider costs are pass-through costs.
- AI can mislead unless transaction facts remain deterministic.
- Integration and customization can create unbounded support.
- Customer acquisition may remain entirely aggregator-owned.

## Strength Classification

**Strongest and safest to model:** actual shifted-order fee exposure, pickup delivery-cost avoidance, actual delivery-zone leakage, actual manual-order time/errors, catering wins for relevant concepts.

**Useful but conditional:** incremental direct orders, repeat-customer capture, structured upsell, bots, POS workflow, outsourced/hybrid delivery.

**Weakest as automatic money claims:** generic trust uplift, generic SEO uplift, universal AOV uplift, universal loyalty uplift, customer-data value without campaigns.

## Safe Mention Rules

- Safe: “Estimate using your numbers,” “can,” “may,” “scenario,” “break-even depends on…”
- Unsafe: guaranteed revenue, guaranteed savings, universal commission rate, universal AOV lift, fixed payback promise, aggregator replacement.
