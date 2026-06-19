# Add-On Module Catalog

All module pricing is `[Run 2C price required]` unless marked `[custom quote]`. Third-party costs are paid directly or passed through transparently.

| Module | What it does | Sell when | Do not sell when | Third-party costs | Support risk | Data/provider gate | Pricing implication |
|---|---|---|---|---|---|---|---|
| WhatsApp 1 - Handoff | Prepares structured order/enquiry for customer to send | Existing WhatsApp demand; staff accepts manual handoff | Owner expects automation/confirmation | Ordinary WhatsApp; policy risk | Low-medium | Staff process | Setup + bounded support |
| WhatsApp 2 - Deterministic bot | Guides menu/cart/details through approved transaction flow | High measurable chat volume and repeated staff work | Low volume, no BSP/account readiness | Meta/BSP/messages | High | Volume, intents, escalation, BSP | Module + recurring/pass-through |
| WhatsApp 3 - Bounded AI assistant | Answers approved questions and guides to deterministic cart | Proven demand, knowledge base, budget, human handoff | Early workflow, unsafe expectations | Meta/BSP + LLM | Very high | Safety, budget, evaluation | `[custom quote]` |
| Telegram 1 - Receiver | Sends website orders to restaurant staff | Staff reliably uses Telegram | Staff will not monitor it | Normal Bot API generally free; hosting | Medium operational | Named owner | Included Tier 0 |
| Telegram 2 - Deterministic bot | Customer chat ordering using controlled menu/cart | Audience uses Telegram; clear demand | Novelty-only request | Hosting | Medium-high | Volume/audience/intents | Module |
| Telegram 3 - Bounded AI assistant | Approved menu Q&A/recommendation to deterministic cart | Proven niche demand and safe knowledge | No measured need | LLM/hosting | High | Safety/budget/handoff | `[custom quote]` |
| Payment | Gateway checkout, status, bounded refund workflow | Merchant account ready; economics known | Cash-only/unknown refund responsibility | Gateway/dispute/refund fees | High | Gateway compatibility/policy | Setup + recurring support + pass-through |
| Delivery zones/rules | Zones, fees, minimums, explicit delivery choice | Known leakage and fulfilment economics | Costs/radius unknown | Maps optional | Medium | Owner delivery data | Module or Tier 3 component |
| Supported POS integration | Connects an explicitly supported POS workflow | Compatible API/access and measured duplicate-entry burden | Unknown/closed POS or universal expectation | POS/API/partner fees | Very high | Compatibility and adapter support | `[custom quote]` or supported-module price |
| Supported delivery integration | Dispatch/tracking through supported provider | Suitable contract/API and known value | Early default or unknown provider | Provider/API/delivery fees | Very high | Compatibility, SLA, responsibility | `[custom quote]` or supported-module price |
| Table QR | Routes table to menu/order workflow | Dine-in workflow is documented and staff accepts it | Table service conflict or novelty | Printing | Medium-high | Table/service pilot | Module |
| Catering/group enquiry | Structured high-ticket enquiry capture | Family-tray/catering demand and follow-up owner | No relevant demand/follow-up process | Email/message optional | Low-medium | Ticket/win/follow-up process | Module; may bundle for relevant Tier 1 |
| Analytics/source tracking | Source tags and bounded outcome reporting | Restaurant will use defined metrics | Broad reporting request without decisions | Analytics tools optional | Medium | Metric definitions | Basic tags core; deeper module/Tier 3 |
| Multi-branch | Branch selection, workflows, reporting | Single-branch pattern proven; processes standardized | Early or inconsistent branches | Infrastructure/vendor | Very high | Branch audit/provider capacity | `[custom quote]`, delayed |
| Advanced reporting | Custom/expanded management views | Defined recurring decisions and data quality | “More dashboards” request | Analytics stack | High | Decision/use gate | `[custom quote]`, delayed |
| Customer notifications | Sends approved order statuses | Status workflow is reliably used | Staff status discipline absent | WhatsApp/SMS/email | Medium-high | Channel consent/cost | Module + pass-through |
| Promotions/coupons | Controlled direct offers | Margin/measurement rules approved | Generic growth promise | None/vendor optional | Medium | Promotion economics | Module |
| Language/content module | Additional approved language/content allowance | Audience and approved content exist | Unlimited translation/content expectation | Translation/content | Medium | Approval/allowance | Setup allowance + maintenance |
