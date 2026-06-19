# ROI Calculator Specification

## Objective

Give a restaurant owner an editable, non-guaranteed estimate of how an owned channel could gain, save, protect, or risk money. The calculator must expose assumptions, separate shifted from incremental demand, and recommend a channel/fulfilment starting point.

## UI Sections

1. **Quick profile:** archetype, branches, current channels, monthly orders, AOV.
2. **Current economics:** gross margin, aggregator share and actual deductions, payment costs, pickup/delivery mix.
3. **Owned-channel scenario:** expected shifted orders, incremental orders, traffic/conversion, pickup share, promotions.
4. **Operational leakage:** WhatsApp/phone volume, minutes/order, missed orders, mistake rate/cost.
5. **Fulfilment:** current model, driver/rider fixed cost, motorcycle cost, outsourced cost/order, failed-delivery rate.
6. **High-ticket leads:** catering/group enquiries, win rate, average ticket, margin.
7. **System costs:** setup, evaluation period, monthly support, hosting, WhatsApp, Telegram, AI, POS/delivery integration.
8. **Results:** conservative/base/optimistic, break-even, risk, recommendation, warnings.

## Required Inputs and Default Policy

| Input | Unit | Conservative / base / optimistic starting scenario | Default rule |
|---|---|---|---|
| Monthly orders | orders | owner input | Required; no default |
| AOV | AED/order | owner input | Required |
| Contribution/gross margin after food and packaging | % | owner input | Required; explain definition |
| Aggregator share | % orders | owner input | Required if relevant |
| Actual aggregator deductions | % of order value | owner input; optional 15% / 25% / 35% sensitivity | Required for payback; sensitivity is not UAE fact |
| Orders expected to shift direct | orders/month | blank/zero; optional 2% / 7% / 15% sensitivity | Positive values require explicit opt-in |
| Incremental direct orders | orders/month | zero/blank; optional 0% / 2% / 5% sensitivity | Positive values require explicit opt-in |
| Direct AOV uplift | % | zero; optional 0% / 3% / 8% sensitivity | Vendor claims excluded |
| Pickup share of direct orders | % | owner input | Required |
| Direct delivery cost/order | AED | owner input | Required for delivery |
| Gateway fee | % + AED/order | 2.9% + AED 1 reference | Editable; Stripe UAE reference only |
| Direct promotion discount | % | 0% / 5% / 10% | Required if offered |
| Manual orders | orders/month | owner input | Optional |
| Staff minutes/manual order | minutes | blank; optional 3 / 5 / 8 sensitivity | Owner measurement preferred |
| Loaded staff value | AED/hour | owner input | Required for time value |
| Mistake/missed-order rate | % | blank; optional 1% / 3% / 5% sensitivity | Owner measurement preferred |
| Average correction/lost contribution | AED/event | owner input | Required |
| Catering enquiries/month | enquiries | owner input | Optional |
| Incremental won catering orders | orders/month | zero/blank; optional 0 / 1 / 3 sensitivity | Positive values require explicit opt-in |
| Rider fixed monthly cost | AED/month | owner input; reference range 2,000-5,000 salary only | Unsafe as automatic default |
| Motorcycle/fuel/insurance/maintenance | AED/month | owner input | No default |
| Outsourced delivery | AED/order | owner quote; reference 11-55+ broad fulfilment | Unsafe as restaurant default |
| Setup cost | AED | user-entered quote | No public default |
| Monthly support/API/hosting | AED/month | user-entered quote | Required |

## Formula Set

### 1. Direct-order commission savings

`shifted_orders = MIN(expected_shifted_orders, current_aggregator_orders)`

`avoided_marketplace_deductions = shifted_orders x AOV x actual_marketplace_deduction_rate`

`shifted_order_net_benefit = avoided_marketplace_deductions - shifted_orders x (direct_gateway_fee + incremental_direct_delivery_cost + direct_discount + incremental_packaging/support_cost)`

### 2. Incremental-order contribution

`incremental_order_contribution = incremental_direct_orders x direct_AOV x contribution_margin - variable_payment_delivery_discount_costs`

### 3. Pickup contribution

`pickup_benefit = direct_pickup_orders x avoided_delivery_cost_per_order - incremental_pickup_discount_and_packing_cost`

Avoid double counting delivery savings already included in shifted-order comparison.

### 4. Catering/family-tray lead model

`catering_upside = incremental_won_orders x average_catering_ticket x catering_contribution_margin - fulfilment_and_failure_cost`

### 5. WhatsApp error and staff-time model

`time_value = manual_orders x minutes_saved_per_order / 60 x loaded_hourly_value`

`error_value = manual_orders x reduction_in_mistake_rate x average_error_cost`

Only count time as cash saving when overtime/headcount or redeployment value is credible; otherwise label capacity released.

### 6. Repeat-customer capture model

`repeat_contribution = tracked_repeat_direct_orders x contribution_per_direct_order`

Do not assign monetary value to customer records without a measured campaign/order outcome.

### 7. Delivery fulfilment model

`owned_fleet_cost_per_delivery = (rider_fixed_cost + motorcycle + fuel + insurance + maintenance + management + failure_cost) / deliveries`

`outsourced_total = outsourced_cost_per_order x deliveries + failure/refund_cost`

Choose the lower-risk model, not merely the lowest point estimate.

### 8. Bot-assisted ordering model

`bot_net = contained_conversations x minutes_saved x hourly_value / 60 + incremental_bot_orders x contribution/order - API/AI/support/escalation costs`

### 9. Hybrid model

Sum non-overlapping modules only. Each benefit must have a unique order or event basis to prevent double counting.

### Overall

`monthly_net_impact = total_non_overlapping_benefits - monthly_system_cost - monthly_new_fixed_costs`

`payback_months = setup_cost / monthly_net_impact`, only when monthly net impact is positive.

## Outputs

- Estimated shifted direct orders and incremental direct orders
- Avoided marketplace deductions
- Added contribution from incremental orders
- Pickup benefit
- Staff capacity released and cash-equivalent value
- Error/lost-order value protected
- Delivery-model cost comparison
- Catering/group-order upside
- Monthly net impact and annualized scenario
- Break-even period or “no break-even under this scenario”
- Conservative/base/optimistic result
- Risk level and top three sensitivity drivers
- Best starting fulfilment model suggestion
- Best starting channel stack suggestion
- “This works only if…” statement
- “Do not buy yet if…” warning

## Release Modes

### Public quick diagnostic

Returns likely ROI paths, missing data, risk level, best next measurement, and possible channel/fulfilment tests. It does not show predicted AED ROI or payback without records.

### Evidence-based model

Unlocks AED impact and payback only after actual or explicitly confirmed values are entered for core economics and all material costs. Every output shows data-quality/provenance status.

## Recommendation Rules

- Recommend **tiny ordering page + current fulfilment** when demand exists but operational data is weak.
- Recommend **website + WhatsApp handoff** when WhatsApp/social demand is already material.
- Recommend **deterministic WhatsApp bot** only when message volume and repeated staff work justify setup/support.
- Recommend **Telegram receiver** as low-cost staff notification; Telegram customer bot only where customer usage exists.
- Recommend **pickup-first** when delivery economics are unknown or negative.
- Recommend **outsourced/hybrid delivery** before new owned fleet when volume is uncertain.
- Recommend **supported POS integration** only when duplicate-entry burden exceeds integration/support cost.
- Recommend **no purchase/test only** when monthly net impact is negative, source demand is absent, or staff ownership is missing.

## Disclaimers

- Estimates are scenarios, not guarantees.
- Actual marketplace deductions, payment, delivery, WhatsApp, AI, POS, and support costs vary by contract and usage.
- Direct orders may shift existing orders rather than create new revenue.
- Staff time is not cash savings unless it changes paid labor or creates measurable productive capacity.
- Trust, SEO, customer data, and brand legitimacy are not automatically converted to AED.
- Results exclude taxes and financing unless explicitly entered.
- The restaurant remains responsible for menu accuracy, availability, fulfilment, food quality, refunds, and staff process unless contracted otherwise.
