# ROI Variables Model

## Core Formula

For each fulfilment model:

`Net ROI contribution = incremental gross profit - direct fulfilment cost - software/support cost - payment cost - channel cost - failure/refund cost - labor burden - CAC/amortized setup`

This is a decision model, not a public pricing model.

## Variables

| Variable | Definition | Unit | Source or assumption label | ROI effect | Sensitivity |
|---|---|---|---|---|---|
| monthly_total_orders | Total restaurant orders in a month | orders/month | owner data | Higher base volume increases the value of any conversion gain and can dilute fixed costs | High |
| monthly_delivery_orders | Delivery orders per month | orders/month | owner data | Determines exposure to delivery labour, bike, and outsourced delivery cost | High |
| monthly_pickup_orders | Pickup orders per month | orders/month | owner data | Determines whether pickup-only can stand alone | High |
| average_order_value | Average ticket value | AED/order | owner data | Raises absolute margin and commission base | High |
| gross_margin | Gross profit after food cost, before channel cost | % | owner data | Main ceiling on recoverable channel cost | High |
| food_cost_percentage | Food cost as share of revenue | % | owner data | Lower margin leaves less room for delivery cost and software overhead | High |
| aggregator_commission | Marketplace commission and fees | % or AED/order | estimate/vendor claim | Baseline cost to beat versus aggregator-heavy model | High |
| payment_gateway_cost | Card/wallet fee on direct orders | % or AED/order | estimate | Small but persistent direct-channel cost | Medium |
| delivery_cost_per_order | Variable cost to complete a delivery | AED/order | estimate | Determines whether own-driver or outsourced delivery can beat aggregators | High |
| driver_salary | Monthly salary for hired driver | AED/month | estimate | Fixed cost that must be spread across delivery volume | High |
| rider_salary | Monthly salary for hired rider | AED/month | estimate | Fixed labour cost in rider-based models | High |
| rider_visa_labor_cost | Visa, labor, and compliance burden per rider | AED/month | estimate | Increases fixed monthly burden | Medium |
| motorcycle_rental_or_ownership | Bike lease, depreciation, or ownership cost | AED/month | estimate | Raises fixed cost for motorcycle-based models | High |
| fuel_cost | Fuel and operating fuel cost | AED/month or AED/order | estimate | Small fixed/variable cost depending on route density | Medium |
| maintenance_cost | Maintenance and repairs | AED/month | estimate | Supports true full-cost delivery economics | Medium |
| insurance_compliance_cost | Insurance, permits, and compliance cost | AED/month | estimate | Matters for owned fleet economics and legal risk | Medium |
| outsourced_delivery_fee | Third-party per-order delivery fee | AED/order | estimate/vendor claim | Core comparison against own fleet and aggregator fees | High |
| failed_delivery_rate | Share of deliveries failed or redelivered | % | estimate | Increases refund, complaint, and re-delivery cost | High |
| refund_complaint_cost | Cost of refunds, redelivery, goodwill, support | AED/order | estimate | Direct drag on direct-order economics | High |
| staff_time_per_order | Extra staff minutes per order | minutes/order | estimate | Hidden labour cost for manual ordering or complex fulfilment | High |
| manual_whatsapp_error_rate | Share of orders requiring correction/rework | % | estimate | Raises support and refund costs in manual ordering | High |
| direct_channel_conversion_rate | Share of visitors or contacts that order | % | scenario assumption | Determines traffic efficiency for owned channel | High |
| repeat_order_rate | Share of customers returning | % | scenario assumption | Main source of owned-channel payback | High |
| discount_promo_cost | Launch discounts or promos | AED/order or AED/month | scenario assumption | Can stimulate conversion but erodes margin | Medium |
| customer_acquisition_cost | Paid or organic acquisition cost | AED/customer | scenario assumption | Important where traffic is not already owned | High |
| qr_packaging_google_instagram_traffic | Traffic from physical and social touchpoints | visits/month | scenario assumption | Fuels direct-channel demand | Medium |
| website_order_page_conversion | Conversion from web visits to orders | % | scenario assumption | Key for website-first channel | High |
| whatsapp_bot_conversion | Conversion from WhatsApp flows to orders | % | scenario assumption | Key for chat-first channel | High |
| telegram_bot_conversion | Conversion from Telegram flows to orders | % | scenario assumption | Useful where Telegram audience already exists | Medium |
| ai_assistant_usage_cost | LLM/token cost for AI assistant interactions | AED/month or AED/conversation | estimate | Small but grows with usage | Low to Medium |
| software_setup_cost | Initial setup cost amortized over months | AED/month equivalent | estimate | Important for payback period | High |
| monthly_support_cost | Ongoing support and changes | AED/month | estimate | Major provider burden in low-ARPA accounts | High |
| hosting_database_api_cost | Hosting and backend cost | AED/month | estimate | Usually small but non-zero | Low |
| pos_integration_cost | Setup/support burden for POS integration | AED/month equivalent | estimate | Can materially change economics and burden | High |
| delivery_integration_cost | Setup/support burden for delivery partner integration | AED/month equivalent | estimate | Can materially change economics and burden | High |

## Most Sensitive Variables

1. Monthly delivery orders.
2. Delivery cost per order versus aggregator commission.
3. Gross margin / food cost percentage.
4. Conversion rate from owned traffic or chat traffic.
5. Repeat-order rate.
6. Fixed labour cost for any owned rider model.
7. Support and correction burden for manual ordering.

## Practical Interpretation

- If delivery volume is low, owned delivery is usually a cost trap.
- If pickup demand exists, pickup-first can be positive ROI with almost no fulfilment cost.
- If the restaurant already has a driver, the incremental ROI hurdle is lower than hiring new delivery labor.
- If the restaurant has strong repeat customers and sufficient traffic, direct ordering can beat aggregators on retained margin even with modest conversion.
- If traffic is weak, direct ordering adds work without enough orders to recover setup and support.

