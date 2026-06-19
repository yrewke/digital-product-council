# Number Ledger

Every material number must state its unit, geography, provenance, classification, confidence, formula use, limitations, and customer-default safety.

| ID | Number / range | Unit | Geography | Source | Source type | Confidence | Classification | Formula use | Limitations | Safe default? |
|---|---:|---|---|---|---|---|---|---|---|---|
| N-001 | 0 | guaranteed ROI | Any | Company-memory restriction | Internal decision | High | council judgment | Disclaimer only | ROI must never be guaranteed. | Yes, as disclaimer |
| N-002 | 2.9% + AED 1 | per successful domestic-card transaction | UAE | S-006 | Official provider pricing | High | verified fact | Direct payment cost | Stripe standard price only; excludes other providers/international cards/refunds. | Yes, labeled and editable |
| N-003 | +1% | international card surcharge | UAE | S-006 | Official provider pricing | High | verified fact | Payment sensitivity | Stripe only. | Optional advanced input |
| N-004 | +1% | currency-conversion surcharge | UAE | S-006 | Official provider pricing | High | verified fact | Payment sensitivity | Stripe only. | Optional advanced input |
| N-005 | AED 60 | dispute received / manual evidence fee conditions | UAE | S-006 | Official provider pricing | High | verified fact | Failure/dispute cost | Conditions and refundability apply. | No default; warning/input |
| N-006 | Up to 35% | marketplace commission/exposure per order | UAE | S-009, S-010 | Academic-style/journalism | Medium-low | industry benchmark | High-exposure commission scenario | Older and contract-specific; may exclude/include different fees. | As optimistic savings ceiling only |
| N-007 | 25%-35% | Deliveroo commission average claim | Global | S-011 | Vendor/industry guide | Low | vendor claim | Marketplace sensitivity | Not UAE-specific and contract-dependent. | No |
| N-008 | AED 2,000-4,000; average AED 3,155 | monthly bike-delivery salary | UAE | S-012 | Job-market aggregator | Medium-low | industry benchmark | Rider fixed-cost scenario | Salary only, excludes employer, visa, accommodation, bike, fuel, insurance, maintenance. | No; owner input preferred |
| N-009 | AED 2,300-5,000 advertised | monthly rider earnings/salary | UAE | S-013 | Job listings | Low | estimate | Rider sensitivity | May include incentives and different work models. | No |
| N-010 | AED 11-55+ | fulfilment cost/order | UAE | S-014 | Vendor claim | Low | vendor claim | Outsourced-delivery sensitivity | Ecommerce fulfilment broad range, not hot-food delivery. | No |
| N-011 | AED 17.31 | next-day shipment up to 5kg | UAE | S-015 | Vendor claim | Medium | vendor claim | External-cost context only | Not same-day hot-food restaurant delivery. | No |
| N-012 | 30%+ | claimed digital-order AOV uplift vs phone | Global | S-016 | Vendor claim | Low | vendor claim | AOV sensitivity ceiling | Unsafe and likely context-dependent. | No; default uplift 0% |
| N-013 | 0 | Telegram API charge for normal Bot API use | Global | S-008 | Official documentation | High | verified fact | Telegram pass-through API cost | Hosting, development, support, and paid broadcasts remain. | Yes, with caveat |
| N-014 | ~30 messages/second | free bulk broadcast limit | Global | S-008 | Official documentation | High | verified fact | Telegram scale warning | Not relevant to normal small-restaurant transactional flows. | No default needed |
| N-015 | AED 375/month | Foodics Marketplace price visible on UAE pricing page | UAE | S-018 | Vendor pricing | Medium | verified provider price | Competitor/alternative anchor | Package details and applicability require verification. | No calculator default |
| N-016 | USD 19/month | FoodBooking basic plan | Global | S-019 | Vendor pricing | Medium | verified provider price | Alternative-cost context | Not UAE-specific; feature/support differences. | No |
| N-017 | USD 45/month + USD 0.25/order | 247waiter entry pricing | Global | S-019 | Vendor pricing | Medium | verified provider price | Alternative-cost context | Not UAE-specific; feature/support differences. | No |
| N-018 | 15% / 25% / 35% | marketplace deduction scenarios | UAE scenario | Council based on S-009-S-011 | Council model | Medium-low | scenario assumption | Calculator conservative/base/optimistic | Must be replaced with actual restaurant statement. | Yes, visibly editable |
| N-019 | 2% / 7% / 15% | total monthly orders shifted direct | UAE scenario | Council judgment | Council model | Low | scenario assumption | Shifted-order model | No primary UAE conversion evidence. | Yes, visibly editable |
| N-020 | 0% / 2% / 5% | incremental direct orders as total orders | UAE scenario | Council judgment | Council model | Low | scenario assumption | Incremental-order model | Must not be confused with shifted orders. | Yes; conservative is zero |
| N-021 | 3 / 5 / 8 | minutes saved per manual order | UAE scenario | Council judgment | Council model | Low | scenario assumption | Staff-time model | Requires time-motion validation. | Yes, editable |
| N-022 | 1% / 3% / 5% | mistake/missed-order reduction | UAE scenario | Council judgment | Council model | Low | scenario assumption | Error protection model | Requires restaurant logs. | Yes, editable |

## Default-Safety Rule

A number is safe as a customer-facing default only when it is either a transparent neutral scenario assumption or sufficiently supported and clearly editable. All monetary and performance defaults must be shown as assumptions, not facts.
