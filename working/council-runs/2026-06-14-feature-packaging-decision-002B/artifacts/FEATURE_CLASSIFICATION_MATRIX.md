# Feature Classification Matrix

This matrix records the Chairman-ready proposed classification after economics-gate review. Detailed burden and evidence notes remain in `FEATURE_INVENTORY_NORMALIZED.md`; provider effort classifications require measurement before pricing.

| Feature | Class | Restaurant job / ROI path | Complexity | Support risk | Third-party cost | Package/module |
|---|---|---|---|---|---|---|
| Logo/header, menu categories/items/prices, cart, customer details/notes | Core | Structured order capture; fewer misunderstandings | Low | Low-medium | None | Tier 0 |
| Telegram order receiver, local SQLite history | Core | Bounded notification and basic outcome record | Low | Medium if staff misses orders | Telegram API normally free; hosting/support | Tier 0 |
| Stable URL and source tags | Core | Clear destination and repeat/source measurement | Low-medium | Low | Domain/hosting | Tier 0/1 |
| Item photos/descriptions beyond allowance | Add-on | Menu clarity | Low-medium | Content upkeep | Photography/content | Content module |
| Home page, contact, hours, location, social links | Core | Clear web/social/Google destination | Low-medium | Content accuracy | Domain/maps optional | Tier 1 |
| QR code to site/order page | Core Tier 1 / add-on Tier 0 | Route existing attention | Low | Low | Printing | Tier 1 / QR module |
| Basic structured information/SEO capability | Core Tier 1 | Accurate machine-readable presence | Medium | Low | None | Tier 1 |
| Arabic/English content | Conditional | Audience clarity | Medium | Translation/content upkeep | Translation | Language module |
| WhatsApp order handoff | Add-on | Familiar customer door; reduce free-text leakage | Low-medium | Staff handling remains | WhatsApp policies | WhatsApp 1 |
| Catering/group enquiry form | Add-on | Capture high-ticket leads | Low-medium | Follow-up responsibility | Message/email tools | Catering module |
| Pickup/delivery choice, address/location fields | Core/conditional | Explicit known fulfilment | Medium | Restaurant fulfilment burden | Maps optional | Tier 2 |
| Staff dashboard/auth, accept/reject/status workflow, order history | Core | Own order queue; lost-order/error protection | Medium | Training/peak discipline | Hosting/auth | Tier 2 |
| Availability toggles/menu editor | Core | Menu accuracy; reduce refunds | Medium | Self-service adoption | None | Tier 2 |
| Manual restaurant delivery handling | Conditional core | Track known fulfilment | Medium | Dispatch/complaints | None | Tier 2 |
| Customer notifications | Conditional add-on | Reduce status questions | Medium | Message accuracy | WhatsApp/SMS/email | Notification module |
| Online payment/status/refund workflow | Conditional | Collect and reconcile payment | High | Refund/dispute urgency | Gateway fees | Payment module / Tier 3 |
| Delivery zones/fees/minimums | Conditional core/module | Protect delivery margin | Medium | Rule upkeep | Maps optional | Tier 3 / Fulfilment rules |
| Customer records/saved addresses | Conditional | Repeat convenience and measurement | Medium-high | Privacy/data quality | Storage | Tier 3 |
| Promotions/coupons | Add-on | Test controlled offers | Medium | Margin misuse | None | Promotion module |
| Basic source/outcome analytics | Core limited | Measure direct demand | Medium | Interpretation/support | Analytics optional | Tier 3; basic source tags earlier |
| Table QR | Add-on conditional | Structure dine-in ordering | Medium-high | Service workflow | Printing | Table QR module |
| Staff roles/permissions | Conditional | Access control | Medium | Admin/support | Auth | Tier 3/4 |
| POS integration | Conditional/custom | Remove duplicate entry | High/variable | Vendor failure | POS/API fees | Supported integration module |
| Delivery-company integration | Conditional/custom | Dispatch/tracking | High/variable | SLA/exception burden | Provider/API fees | Supported integration module |
| Telegram deterministic customer bot | Conditional add-on | Chat ordering | Medium-high | Exceptions | Hosting | Telegram 2 |
| WhatsApp deterministic bot | Conditional add-on | Structure high-volume chat | High | Policy/escalation | Meta/BSP/messages | WhatsApp 2 |
| Telegram/WhatsApp bounded AI assistants | Delay/custom | Explain/recommend/guide | Very high | Safety/escalation | LLM/BSP | Channel 3 custom |
| Google Business ordering links | Conditional add-on | Clear Google path | Low-medium | Profile/policy | None | Presence module |
| Webhooks/custom automation | Custom | Connect specified workflow | High | Exceptions | Vendor/API | Custom quote |
| Kitchen view, branch support, advanced reporting | Delay/custom | Advanced operations | High | High | Infrastructure | Future Tier 4/custom |
| Aggregator middleware | Delay/custom | Channel consolidation | Very high | Very high | Vendor/platform | Future/custom |
| Inventory, recipes, procurement, ERP | Refuse now | Outside current product | Very high | Unbounded | Variable | Refuse/current thesis boundary |
| Universal integration, unlimited custom/support, guaranteed outcomes | Refuse | Unsafe/unbounded | Unbounded | Unbounded | Unbounded | Refuse |

## Data Gates

Restaurant data is required before selling delivery rules, payment economics, catering modules as an ROI play, bots, POS/delivery integration, promotions, advanced analytics, or multi-branch work.

## Provider Gates

Compatibility, setup effort, monthly support, vendor access, failure impact, and continuity must be approved before payment, bots, integrations, advanced operations, or managed support.
