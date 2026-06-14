# ROI Numbers and Ranges Ledger

This artifact mirrors the working `NUMBER_LEDGER.md` and highlights calculator-safe use.

## Strongest Reference Numbers

| Number | Meaning | Classification | Confidence | Calculator use |
|---|---|---|---|---|
| `2.9% + AED 1` | Stripe UAE standard domestic-card fee | Verified provider price | High | Editable payment-cost reference |
| `+1%` | Stripe international-card surcharge | Verified provider price | High | Advanced sensitivity |
| `+1%` | Stripe currency-conversion surcharge | Verified provider price | High | Advanced sensitivity |
| `AED 60` | Stripe dispute-related fee conditions | Verified provider price | High | Warning/advanced failure-cost input |
| `0` | Normal Telegram Bot API charge | Verified official documentation | High | Cost line, with hosting/support caveat |

## Bounded Market and Cost Ranges

| Range | Meaning | Classification | Confidence | Limitation | Default safety |
|---|---|---|---|---|---|
| Up to `35%` | UAE delivery-app commission exposure reported in older sources | Industry/academic-style benchmark | Medium-low | Contract-specific and older | Use only as high scenario |
| `AED 2,000-4,000`, average `AED 3,155` | UAE bike-delivery salary data | Job-market benchmark | Medium-low | Salary only; excludes full fleet/employer cost | Owner input preferred |
| `AED 11-55+` | UAE broad fulfilment cost/order | Vendor claim | Low | Ecommerce fulfilment, not restaurant delivery | Unsafe default |
| `30%+` | Claimed digital-order AOV uplift | Vendor claim | Low | Global vendor claim | Never default; use 0% base default |

## Calculator Scenario Assumptions

| Range | Use | Confidence | Falsification |
|---|---|---|---|
| `15% / 25% / 35%` | Marketplace-deduction sensitivity | Medium-low | Replace with actual statement |
| `2% / 7% / 15%` | Orders shifted direct | Low | Source-tagged pilot orders show lower/higher shift |
| `0% / 2% / 5%` | Incremental direct orders | Low | Controlled source tracking shows incrementality |
| `3 / 5 / 8 minutes` | Manual-order time saved | Low | Time-motion study |
| `1% / 3% / 5%` | Mistake/missed-order reduction | Low | Pre/post error log |
| `0 / 1 / 3` | Incremental catering wins/month | Low | Tracked enquiry funnel |

## Safety Verdict

Use actual restaurant records wherever possible. Defaults are scenario controls, not UAE averages. Trust, SEO, credibility, customer-data ownership, and loyalty must not receive automatic AED values.
