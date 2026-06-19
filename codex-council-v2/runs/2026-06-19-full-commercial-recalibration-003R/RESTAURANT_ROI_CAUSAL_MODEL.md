# Restaurant ROI Causal Model

## Formula Blocks

Shifted marketplace margin delta:

`shifted_orders * (marketplace_cost_avoided - direct_payment_fee - direct_delivery_cost - incentive - loyalty_reward - direct_marketing_cost - incremental_ops_cost - refund_risk)`

Incremental order contribution:

`incremental_orders * AOV * contribution_margin - payment_fee - delivery_cost - incentive - marketing_cost - support/refund_cost`

Operational value:

`measured_minutes_saved * redeployable_value_per_minute + error/refund_cost_reduction`

Catering contribution:

`qualified_enquiries * close_rate * average_catering_order_value * catering_contribution_margin - follow_up_cost - fulfillment_cost`

Twelve-month net benefit:

`sum(monthly_net_benefit months 1-12) - setup_fee - recurring_solution_fees - pass_through_costs`

Payback:

`setup_fee / monthly_net_benefit_after_recurring_cost`, only when monthly net benefit is positive and based on restaurant-specific inputs.

## Rules

- Do not count shifted orders as incremental.
- Do not count gross revenue as profit.
- Do not double count AOV uplift and gross sales uplift from the same order.
- Do not monetize staff time unless cash is saved or time is productively redeployed.
- Do not count customer data as revenue without activation and measured conversion.
- Do not count enquiries as sales until close rate is measured.

## Time Horizons

Launch: setup readiness, menu accuracy, channel links, staff process.

First 30 days: order capture, direct-source tagging, error rate, support burden.

First 90 days: repeat migration, incentive cost, delivery SLA, owner adoption.

Six months: CRM/loyalty activation and campaign cadence.

Twelve months: retention, net contribution, churn risk, package fit.
