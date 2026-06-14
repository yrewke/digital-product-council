# Feature Inventory Normalized

## Classification Rules

- **Core candidate:** standardized, job-defining, bounded support.
- **Add-on candidate:** clear optional job with repeatable boundary.
- **Delayed candidate:** plausible value, but insufficient demand/support evidence.
- **Custom candidate:** variable vendor/workflow effort requiring quote.
- **Refuse/avoid:** contradicts strategy or creates unbounded promise.
- **Unknown:** compatibility or value cannot yet be classified.

| Feature | Initial class | Restaurant job | ROI path | Archetype fit | Operational burden | Provider burden | Third-party exposure | Owner data gate | Demo-ready | Sell without overclaiming |
|---|---|---|---|---|---|---|---|---|---|---|
| Logo/simple branded header | Core Tier 0 | Recognizable order destination | Clarity/legitimacy | Broad | Low | Low | None | No | Yes | Yes, as capability |
| Menu categories/items/prices | Core Tier 0 | Browse current menu | Structured ordering | Broad | Menu accuracy | Setup/data cleanup | None | Menu approval | Yes | Yes |
| Item photos/descriptions | Add-on/content allowance | Improve menu clarity | Semi-quantitative | Visual/social concepts | Content upkeep | Content burden | Photography optional | Approved assets | Yes | Yes, no conversion claim |
| Cart | Core Tier 0 | Build structured order | Fewer misunderstandings | Broad | Low | Low | None | No | Yes | Yes |
| Customer name/phone/notes | Core Tier 0 | Capture required details | Error reduction | Broad | Privacy/accuracy | Low | None | Required fields | Yes | Yes |
| Telegram order receiver | Core Tier 0 | Notify restaurant | Order capture | Broad if staff uses Telegram | Staff monitoring | Low | Telegram dependency | Named owner | Yes | Yes with monitoring caveat |
| Local SQLite history | Core Tier 0 | Basic order record | Measurement/audit | Tiny deployments | Basic local handling | Low | None | Retention/export agreement | Yes | Yes |
| Stable restaurant-owned URL | Core Tier 0/1 | Clear link destination | Source/repeat measurement | Broad | Low | Domain ownership | Domain/hosting | Ownership choice | Yes | Yes |
| Source tracking | Core measurement feature | Know traffic/order source | Repeat/direct measurement | Broad | Requires tagging | Low-medium | Analytics tools optional | Source definitions | Yes | Yes, no causality claim |
| Home page/contact/hours/location/social | Core Tier 1 | Clear web/social/Google destination | Trust/enquiry support | No/weak website | Content upkeep | Template/content setup | Maps/domain | Approved content | Yes | Yes |
| Basic structured information/SEO | Core Tier 1 capability | Machine-readable presence | Visibility capability | No/weak website | Low | Low-medium | Search engines | Accurate business data | Yes | Yes as capability only |
| Arabic/English content | Conditional/add-on | Serve target audience | Clarity/conversion hypothesis | Relevant audience | Content accuracy | Translation/support | Translation service | Approved translations | Yes | Yes, no uplift claim |
| QR code to site/order page | Core Tier 1 / add-on Tier 0 | Route existing attention | Source/repeat capture | Pickup/dine-in/packaging | Placement/promotion | Low | Printing | Source tagging | Yes | Yes |
| WhatsApp order handoff | Add-on | Familiar customer door | Manual leakage/clarity | WhatsApp-heavy | Staff handling remains | Low-medium | WhatsApp app/policies | Current volume | Yes | Yes with handoff caveat |
| Catering/group enquiry form | Add-on | Capture high-ticket leads | Catering contribution | Family tray/catering | Follow-up responsibility | Low-medium | Email/message delivery | Lead process/ticket | Yes | Yes as capture, not wins |
| Pickup/delivery choice | Tier 2 core; simple pickup optional earlier | Explicit fulfilment | Pickup/clarity | Pickup-capable | Staff fulfilment | Low-medium | None | Fulfilment rules | Yes | Yes |
| Address/location fields | Tier 2 core for manual delivery | Structured delivery details | Error reduction | Own/manual delivery | Address verification | Medium | Maps optional | Delivery process | Yes | Yes |
| Staff dashboard/auth | Tier 2 core | Own order queue | Operational clarity | Volume/discipline | Training/status use | Medium | Auth/hosting | Named staff/roles | Yes | Yes |
| Accept/reject/status workflow | Tier 2 core | Acknowledge and close orders | Lost-order/error reduction | WhatsApp/manual leakage | Staff discipline | Medium | Notifications optional | Workflow agreement | Yes | Yes |
| Availability toggles/menu editor | Tier 2 core | Keep menu accurate | Refund/error protection | Broad | Self-service discipline | Medium | None | Named admin | Yes | Yes |
| Manual delivery handling | Tier 2 core/conditional | Track restaurant-owned fulfilment | Clarity | Existing driver | Dispatch burden | Medium | None | Existing process | Yes | Yes, no SLA |
| Customer notifications | Conditional Tier 2 add-on | Reduce status questions | Support clarity | Higher volume | Message accuracy | Medium | WhatsApp/SMS/email costs | Channel consent | Yes | Yes with cost caveat |
| Online payment/payment status | Tier 3 conditional core/module | Collect payment | Completion/no-show hypothesis | Suitable merchants | Refund/reconciliation | High | Gateway fees/policies | Merchant account | Yes | Yes, no uplift claim |
| Refund workflow | Conditional with payment | Resolve paid orders | Risk control | Paid orders | Restaurant decisions | High | Gateway policies | Refund policy | Yes | Yes as workflow |
| Delivery zones/fees/minimums | Tier 3 module/core where relevant | Protect fulfilment margin | Zone/fee leakage | Delivery-heavy | Rules upkeep | Medium | Maps optional | Delivery economics | Yes | Yes |
| Customer records/saved addresses | Tier 3 conditional | Repeat convenience/measurement | Repeat capture | Repeat-heavy | Privacy/data quality | Medium-high | Storage/privacy | Consent/process | Yes | Yes, no value claim |
| Promotions/coupons | Add-on/conditional | Test offers | Discount control | Measured campaigns | Margin control | Medium | None | Promotion economics | Yes | Yes, no uplift |
| Basic analytics | Tier 3 core limited | Measure source/outcome | ROI measurement | Broad | Interpretation | Medium | Analytics optional | Metric definitions | Yes | Yes |
| Table QR ordering | Add-on/conditional | Structure dine-in orders | Staff-time hypothesis | Dine-in/QSR | Table/service workflow | Medium-high | Printing | Table process | Yes | Conditional |
| Kitchen view | Delay/custom | Improve production handoff | Operational hypothesis | High-volume | Major workflow change | High | Hardware/display | Kitchen study | Demo possible | Not early |
| Staff roles/permissions | Tier 3/4 conditional | Control access | Risk/operations | Larger teams | Admin burden | Medium | Auth | Role design | Yes | Conditional |
| Branch support | Delay/custom | Multi-branch operations | Reporting/control | Small groups | High complexity | High | Infrastructure | Branch process/data | Demo possible | Not early |
| Advanced reporting | Delay | Management insight | Unproven | Multi-branch/high volume | Use discipline | High | Analytics stack | Defined decisions | Demo possible | No ROI claim |
| POS integration | Conditional/custom | Remove duplicate entry | Staff-time/error | Compatible POS only | Vendor/process dependency | High/variable | POS vendor/API fees | POS compatibility | Adapter demo only | Only supported path |
| Delivery-company integration | Conditional/custom | Dispatch/tracking | Fulfilment clarity | Supported provider only | SLA/exception burden | High/variable | Provider fees/API | Contract/quote | Adapter demo only | Only supported path |
| Telegram deterministic ordering bot | Add-on conditional | Customer chat ordering | Channel convenience | Telegram-using audience | Exception handling | Medium-high | Telegram/hosting | Volume/audience | Yes | Conditional |
| Telegram bounded AI assistant | Delay/custom | Explain/recommend/guide | Unproven | Niche | Handoff/safety | High | LLM tokens | Knowledge/budget | Demo possible | Not early |
| WhatsApp deterministic ordering bot | Add-on conditional | Structure high-volume chat | Manual leakage | WhatsApp-heavy | Policy/escalation | High | Meta/BSP/message fees | Volume/BSP/account | Yes | Conditional |
| WhatsApp bounded AI assistant | Delay/custom | Explain/recommend/guide | Unproven | High-volume complex menu | Safety/escalation | Very high | Meta/BSP/LLM | Volume/budget/knowledge | Demo possible | Not early |
| Google Business ordering links | Add-on/conditional | Clear Google path | Source capture | Active profile | Profile ownership | Low-medium | Google policies | Profile access | Yes | Capability only |
| Webhooks/custom automation | Custom | Connect known workflow | Variable | Specific client | Exception handling | High | Vendor/API | Specification | Demo limited | Quote only |
| Aggregator middleware | Delay/custom | Consolidate channels | Operational | High volume | Major dependency | Very high | Vendor/platform | Compatibility | No | Not early |
| Inventory/recipes/procurement/ERP | Refuse for current product; future custom thesis | Full operations | Outside current ROI gate | Large groups | Very high | Very high | Vendors/data | Extensive | No | Refuse now |
| Universal POS/delivery integration | Refuse | Impossible broad promise | None | None | Unbounded | Unbounded | Unbounded | N/A | No | No |
| Unlimited custom design/workflows/support | Refuse | Bespoke agency/managed ops | None | None | Unbounded | Unbounded | Variable | N/A | No | No |
| Guaranteed ROI/SLA/conversion | Refuse | Unsafe claim | None | None | Liability | High | Third parties | N/A | No | No |
