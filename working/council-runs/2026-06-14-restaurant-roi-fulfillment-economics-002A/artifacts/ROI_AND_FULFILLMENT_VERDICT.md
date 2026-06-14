# ROI and Fulfilment Verdict

## Executive Summary

The owned direct-ordering channel creates positive ROI only under a bounded set of fulfilment conditions. The strongest positive-ROI cases are:

1. Pickup-only restaurants with existing pickup demand and low fulfilment burden.
2. Restaurants with existing staff or an existing restaurant driver already handling deliveries.
3. Restaurants with enough stable local delivery volume to justify a hired rider or a rider-plus-motorcycle setup.
4. Restaurants where direct traffic already exists and the owned channel mainly converts repeat demand away from aggregator commission.
5. Hybrid models with clear nearby pickup/own-driver zones and outsourced overflow, when delivery density is uneven but repeat demand is real.

The weakest cases are:

1. Low-volume restaurants with little repeat traffic.
2. Restaurants that depend almost entirely on aggregators for discovery and do not have owned traffic.
3. Manual WhatsApp ordering at any scale where errors, missed messages, and staff time dominate.
4. Motorcycle-only ownership without enough delivery density to amortize the asset.

## The ROI Logic in Plain English

Owned direct ordering pays back when it captures repeat orders and avoids enough aggregator commission, manual labor, or external delivery cost to cover setup, support, and fulfilment burden.

It does not pay back when the restaurant has too few orders, too little repeat behavior, or too much delivery complexity for the traffic it has.

The right question is not "Can direct ordering work?"

It is "Does this restaurant already have enough repeat demand and enough fulfilment discipline for direct ordering to beat the alternative after all costs?"

## Fulfilment Model Ladder

From easiest to hardest to make positive ROI:

1. Pickup only.
2. Existing staff or existing restaurant driver.
3. Outsourced delivery.
4. Hybrid model.
5. WhatsApp/manual ordering.
6. Delivery API/provider integration.
7. Hired rider.
8. Motorcycle plus rider.
9. Motorcycle only.
10. Aggregator-only dependence for owned-channel ROI testing.

## Scenario Ranges

These are scenario assumptions, not verified Dubai averages.

| Scenario | Likely ROI shape | Why money can be gained | Why money can be lost | Net verdict |
|---|---|---|---|---|
| A. No website, no structured ordering | Weak unless pickup demand is already present | Captures missed repeat demand | Setup, traffic, and support effort are too high relative to current demand | Usually negative unless the restaurant already has local repeat traffic |
| B. Instagram/WhatsApp only | Can be positive at low scale | Cheap to start, familiar to customers | Manual errors and staff time grow fast | Positive only for very small order volumes or highly familiar customer bases |
| C. Existing weak website, no ordering | Slightly better than nothing | Can convert existing visitors | No transaction engine, low capture | Usually neutral to weakly positive only after adding ordering |
| D. Aggregator-heavy restaurant | Often strongest near-term direct-channel candidate | Immediate commission avoidance on repeat orders | Customer acquisition still comes mostly from aggregators | Positive if repeat order rate and owned traffic are real |
| E. Restaurant with existing own driver | Strong candidate | Delivery cost already embedded; incremental direct orders can improve utilization | Route inefficiency and slack time | Usually positive if delivery volume is steady |
| F. Restaurant considering hiring rider or motorcycle | Conditionally positive | Can reduce third-party delivery cost at scale | Fixed labor/asset cost can outrun demand | Positive only above a meaningful monthly delivery threshold |
| G. Catering/family-tray restaurant | Strong candidate for owned logistics | Large tickets can absorb delivery cost | Failure cost is expensive | Often positive if routes are few and orders are chunky |
| H. Dine-in restaurant considering table QR or pickup | Pickup/QR can be positive; delivery often weaker | Less manual ordering, more repeat pickup | Dine-in is not a natural delivery business | Positive for pickup and QR, weaker for fleet delivery |
| I. Restaurant with POS system | Positive if POS removes manual burden | Better workflow and fewer errors | Integration/setup burden | Positive when POS already exists and order volume justifies it |

## Break-Even Variables

The main break-even drivers are:

- Monthly delivery orders.
- Average order value.
- Gross margin.
- Aggregator commission.
- Delivery cost per order.
- Driver/rider fixed monthly cost.
- Failed-delivery and refund cost.
- Staff time per order.
- Conversion rate from owned traffic.
- Repeat-order rate.
- Support/setup amortization.

### Bounded Break-Even Rules

- Pickup-only can work at very low volume if pickup demand already exists.
- Existing-driver delivery becomes attractive once incremental orders fill otherwise idle capacity.
- Hired rider or motorcycle-plus-rider needs enough stable daily deliveries to amortize labor and compliance cost.
- Outsourced delivery is usually the safest variable-cost bridge where density is not enough for own fleet.
- Manual WhatsApp ordering breaks down earlier than a structured ordering page because labor and error rates rise nonlinearly.

## Where Owned Direct Ordering Makes Sense

Owned direct ordering likely makes sense when:

- The restaurant already has repeat customers.
- Delivery radius is compact.
- Pickup is already common or easy to encourage.
- The owner wants customer control and repeat capture.
- The restaurant can keep channel discipline.
- The order volume is large enough to justify either variable delivery fees or a small dedicated fleet.

Best-fit types:

- Neighborhood QSR.
- Fast casual.
- Family-tray and catering-led concepts.
- Restaurants with regular lunch demand.
- Restaurants with stable local repeat customers.

## Where It Does Not Make Sense

Owned direct ordering likely does not make sense when:

- The restaurant has weak repeat demand.
- Orders are highly irregular or low volume.
- Menu complexity creates many corrections.
- Delivery radius is broad and inconsistent.
- Staff cannot sustain status discipline.
- The restaurant is still mostly a discovery-only business.

Worst-fit types:

- High-end fine dining.
- Highly variable casual dining with low repeat frequency.
- Restaurants with very low order volume.
- Concepts relying on one-off discovery spikes.

## Pickup-Only ROI Verdict

**Verdict: Positive ROI in the broadest set of cases.**

Pickup-only is the easiest fulfilment model to make work because it minimizes delivery cost and operational complexity. It is positive when pickup demand exists or can be stimulated from nearby traffic.

**Caveat:** It can be too weak as a standalone commercial story if the restaurant wants delivery revenue.

## Own-Driver ROI Verdict

**Verdict: Positive only when the restaurant already has delivery density or an existing driver.**

If an existing driver is already on payroll or available, the incremental ROI can be strong because the channel can redirect repeat demand into direct orders without adding a new fleet cost.

If the restaurant must hire the driver from scratch, ROI depends on enough monthly delivery volume to cover salary, idle time, and compliance cost.

## Hire-Rider ROI Verdict

**Verdict: Conditionally positive, but only above a meaningful delivery threshold.**

Hiring a rider introduces fixed cost and operational management. It becomes sensible only when daily delivery volume is stable enough to keep the rider busy most of the time.

This is a better fit than outsourced delivery only if:

- the route density is predictable,
- the restaurant wants control,
- and the delivery volume is high enough to amortize labor.

## Motorcycle-Only / Rider-Only / Motorcycle-Plus-Rider Verdict

**Motorcycle only: weak to negative unless paired with a rider and enough demand.**

**Rider only: better than motorcycle only, but still fixed-cost sensitive.**

**Motorcycle plus rider: the most expensive owned-fleet form, so it is only justified by dense, stable delivery volume.**

This family is usually not the first positive-ROI test. It is a later-stage optimization for restaurants with already proven local delivery demand.

## Third-Party Delivery Verdict

**Verdict: Often the best bridge model when own fleet economics are not yet justified.**

Outsourced delivery is a variable-cost way to serve delivery demand without taking on fleet management. It usually wins over hiring riders or buying motorcycles when order volume is uncertain.

It does not create the strongest margin, but it is often the lowest-risk way to keep delivery in the owned-channel stack.

## Hybrid Fulfilment Verdict

**Verdict: Strongest practical model for many restaurants.**

Hybrid works when the restaurant can use pickup and nearby own delivery for the core zone, then hand overflow or distant orders to a third party.

This is usually the best compromise between control and burden.

It is especially strong where:

- nearby orders are frequent,
- distant delivery is sporadic,
- and the restaurant wants a single direct channel without overbuilding fleet capacity.

## Aggregator Coexistence Verdict

**Verdict: Keep aggregators as discovery engines.**

The owned channel should not try to replace Talabat, Deliveroo, Noon Food, or Careem Food.

The economic case is strongest when aggregators keep feeding discovery and the owned channel captures repeat orders, pickup, and direct relationship value.

## WhatsApp/Manual Ordering Comparison

**Verdict: Good as a low-friction starting point, weak as a scalable operating model.**

WhatsApp/manual ordering can be positive for very small volumes or very familiar customer relationships.

It becomes fragile because:

- order errors rise,
- staff time rises,
- totals are harder to control,
- and operational auditability is weak.

Compared with a structured website or ordering page, it usually loses once order volume grows past a small threshold.

## Website vs WhatsApp Bot vs Telegram Bot vs Hybrid Channel

### Website ordering

Best when the restaurant wants a stable branded ordering surface and can drive traffic from QR, Google, Instagram, or repeat customers.

### WhatsApp bot

Best when customer behavior already lives in WhatsApp and the restaurant wants a familiar chat entry point.

### Telegram bot

Best as an add-on or niche channel, especially for repeat customers who already use Telegram.

### Hybrid channel

Best overall for most serious cases because it can combine website ordering with chat handoff and optional channel routing.

**Verdict:** website plus WhatsApp is the most practical default; Telegram is optional and usually secondary.

## Which Fulfilment Model Should Be Tested First

**Test pickup-only first, then existing-driver delivery or outsourced delivery, then hybrid.**

Reason:

- Pickup gives the cleanest economic signal.
- Existing-driver delivery tests whether already-paid capacity can be utilized.
- Outsourced delivery tests the least risky delivery bridge.
- Hybrid should follow once the restaurant proves nearby volume and channel discipline.

## Which Restaurant Segment Should Be Tested First

**Test first with neighborhood QSR, fast casual, family-tray, or catering-led restaurants that already have repeat demand and a compact service radius.**

These segments have the best chance of converting owned-channel traffic into enough repeat orders to beat commission-heavy alternatives.

## What Data Must Be Collected from Restaurant Owners During Sales Calls

- Monthly orders.
- Delivery percentage.
- Pickup percentage.
- AOV.
- Gross margin or food cost.
- Aggregator share.
- Current delivery method.
- Driver/rider cost.
- WhatsApp order volume.
- Phone order volume.
- Customer repeat behavior.
- Delivery radius.
- Common order mistakes.
- Complaints/refunds.
- POS system.
- Current website/social traffic.
- Interest in QR/WhatsApp/Telegram ordering.
- Willingness to test direct channel.

## Allowed Claims

- Direct ordering can improve control over repeat demand.
- Pickup-only is the lowest-burden fulfilment mode.
- Aggregators remain discovery channels.
- Hybrid fulfilment is often the strongest operational compromise.
- WhatsApp/manual ordering is useful but limited.
- Positive ROI depends on volume, margin, and fulfilment cost.

## Forbidden Claims

- "We replace aggregators."
- "We guarantee revenue growth."
- "We guarantee ROI within a fixed time."
- "We reduce delivery cost in every restaurant."
- "We are cheaper than every competitor."
- "We improve customer experience universally."
- Any exact Dubai-wide commission or payback claim without restaurant-specific data.

## Kill Criteria

Kill the owned-direct-ordering thesis for a restaurant if:

1. Monthly order volume is too low to support any repeat capture.
2. Pickup demand is absent and delivery volume is too thin.
3. Manual order errors or support burden are already high.
4. The restaurant lacks operational discipline for menu and status handling.
5. Delivery radius is too broad for economical own or hybrid fulfilment.
6. Aggregator dependence is so complete that direct traffic is effectively absent.
7. The restaurant cannot provide the minimum data needed to model ROI.

## What Run 2B Should Decide Next

Run 2B should decide the feature packaging and pricing structure that best fits the positive-ROI models found here.

It should not reopen whether the restaurant needs direct ordering at all.

It should answer:

1. Which feature bundle matches pickup-first, existing-driver, outsourced, and hybrid fulfilment.
2. Which add-ons are justified by the economics.
3. Which packaging keeps the offer out of open-ended service territory.

