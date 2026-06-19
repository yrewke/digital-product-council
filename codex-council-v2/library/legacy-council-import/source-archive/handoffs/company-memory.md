# Restaurant Direct-Channel Product — Master Historical Handoff v0.2

**Date:** 2026-06-14  
**Purpose:** Merge all previous restaurant-product handoffs, council outputs, research notebook context, pricing briefs, architecture briefs, channel-bot ideas, and the latest user corrections into one coherent company-memory document.

This file is not a final sales document. It is the **source-of-truth brief** that future council runs and Codex sessions should read before making commercial, packaging, pricing, product, POS, delivery, or sales decisions.

---

## 0. Source-of-Truth Rule

The project has accumulated multiple handoffs and some of them conflict. The rule for this master handoff is:

1. **Latest explicit user correction overrides older handoffs.**
2. **Older handoffs are preserved as history, not automatically treated as current truth.**
3. **Research evidence informs decisions, but does not erase already-made strategic decisions unless it directly contradicts them.**
4. **The council must make bounded decisions under uncertainty. It may label assumptions, but it must still choose a next action.**
5. **NotebookLM is a tool, not the whole research universe. If notebooks are insufficient, targeted external web research is allowed in later runs.**
6. **New channel ideas are added as candidate modules unless explicitly locked as core tier features.**

---

## 1. Project Mission

Build a reusable restaurant direct-channel product for UAE restaurants, especially small and independent restaurants, that gives them a branded owned channel for orders, customer interaction, direct repeat demand, and eventually operational tools.

This is **not** a bespoke website agency model. The goal is to create a repeatable product that can be sold, deployed, supported, and improved across many restaurants without becoming unlimited custom work.

The product should help restaurants use their existing discovery channels more effectively. Discovery channels include:

- Talabat
- Deliveroo
- Noon Food
- Careem Food
- Google Maps
- Instagram
- TikTok
- Facebook
- WhatsApp
- printed menus
- QR codes
- packaging inserts
- table cards

The owned channel should capture repeat demand and structured orders after customers discover or already know the restaurant.

---

## 2. Core Strategic Positioning

### Locked decision: do not replace aggregators

The product must **not** be positioned as a Talabat replacement.

Talabat and other aggregators are useful discovery engines. Restaurants may continue using them for reach, visibility, and marketplace demand.

The product should instead position itself as:

> A restaurant-owned direct ordering and customer channel that sits beside aggregators, captures repeat orders, gives the restaurant more control, and reduces dependence where appropriate.

Allowed framing:

- Keep Talabat for discovery.
- Use the owned channel for repeat customers.
- Use QR, WhatsApp, Google Maps, Instagram, packaging, and staff prompts to bring customers to the direct channel.
- Test whether direct ordering is worth growing for that restaurant.

Forbidden framing:

- “We replace Talabat.”
- “You can leave aggregators.”
- “Guaranteed savings.”
- “Guaranteed ROI.”
- “Direct ordering is always better.”

---

## 3. Target Customers and Geography

### Primary customer type

Independent restaurants and small local restaurant groups in the UAE.

Most attractive early customers are restaurants with:

- one to three branches,
- owner or manager reachable directly,
- active Google Maps profile,
- visible customer demand,
- weak or missing website,
- no clean direct-ordering path,
- existing orders through Talabat, Deliveroo, Careem, Noon Food, WhatsApp, phone, or social media,
- menu suitable for repeat ordering,
- family trays, group meals, catering, office meals, or medium-value baskets,
- operational discipline strong enough to handle orders reliably.

### Geographic focus

Early lead-research geography includes:

- Al Qiyadah
- Hor Al Anz
- Abu Hail
- Al Wuheida
- Al Twar
- Al Mamzar
- Al Qusais
- Deira
- nearby metro-accessible areas
- broader Dubai, Sharjah, Ajman, Abu Dhabi, and Al Ain where commercially justified

Commercial quality is more important than distance.

### Cuisine and restaurant categories of interest

Strong early categories include Arabic-speaking and regional restaurants, especially:

- Sudanese
- Egyptian
- Moroccan
- Syrian
- Lebanese
- Palestinian
- Jordanian
- Iraqi
- Yemeni
- Emirati
- Gulf
- Tunisian
- Algerian
- Saudi
- Turkish, when serving a similar customer base
- Persian as a useful secondary category
- seafood
- mandi / madhbi
- grills / kebab
- traditional meals
- family trays
- group meals
- catering / event meals

---

## 4. Lead Dataset Memory

A lead-research funnel already exists.

Known dataset status from previous handoffs:

- 577 cleaned real restaurant identities.
- 1,404 Google raw restaurant occurrences mapped confidently.
- 14 non-restaurant Google rows excluded but preserved in raw archive.
- Delivery-platform data collected from Talabat, Deliveroo, Noon Food, and related raw occurrence files.
- Intended funnel: broad cleaned dataset → short list of 40–55 → deeper 15–20 → final 10 outreach targets.

Important rule:

- Record and reason at **brand level** when appropriate.
- Do not blindly transfer branch-specific rating, area, fee, delivery time, or delivery-platform data to the brand as a whole.

The dataset should be used in market-action runs to select real restaurants, not only theoretical segments.

---

## 5. Research Notebooks Memory

The NotebookLM research library has four registered notebooks.

### Notebook 1 — Restaurant Website ROI Research

ID: `97f23980-485a-4301-9e07-424f3c0c8825`  
Purpose: restaurant-side value, direct-channel economics, ROI, retention, repeat ordering, customer data, aggregator costs, UX, menu psychology, basket value, restaurant segment fit.

Use for:

- restaurant value,
- payback variables,
- direct-order economics,
- customer behavior,
- segment fit.

Do not use alone to set final provider pricing.

### Notebook 2 — UAE Third-Party Restaurant Delivery Companies Research

ID: `250c6ede-521c-48a2-ad9c-4310d0e9d21d`  
Purpose: delivery providers, white-label delivery, Careem Express, Lyve, Jeebly, Quiqup, Tawseelah, Roadline, Go Delivery, outsourced riders, delivery costs, APIs, dispatch, tracking, SLA and liability risks.

Use for:

- delivery options,
- delivery integrations,
- outsourced delivery and rider models,
- delivery risk and pilot gates.

Do not treat vendor promises as verified SLA performance.

### Notebook 3 — Website and Direct-Ordering Competitors

ID: `9f472613-c991-4447-83d8-008f6e4f89cb`  
Purpose: website builders, direct-ordering competitors, POS/order ecosystems, WhatsApp, QR tools, agencies, SaaS alternatives, aggregator comparison, pricing examples.

Use for:

- alternatives,
- competitive positioning,
- packaging comparison,
- POS/order-system comparison,
- WhatsApp and QR-menu alternatives.

### Notebook 4 — UAE Restaurant Direct-Ordering Product-Market Fit

ID: `d22b2ac2-8915-4108-b06c-2307a80db8ec`  
Purpose: provider viability, GCC foodservice outlook, SaaS benchmarks, acquisition, onboarding, support, churn, customization, profitability boundaries.

Use for:

- provider business model,
- repeatability,
- support burden,
- customization risk,
- SaaS economics.

### Notebook rule

NotebookLM evidence is useful but not sufficient by itself. Later runs may use targeted external web research and direct market validation when notebooks do not answer decisive commercial questions.

---

## 6. Run 001 Council Outcome Memory

Run 001 completed as a commercial council run.

Key outputs:

- 6 conservatively counted NotebookLM attempts out of 25.
- Four ordered evidence requests succeeded.
- 25 evidence claims recorded.
- 197 NotebookLM numbered citations returned.
- 77 NotebookLM source references mapped.
- Five sealed advisor memos completed.
- Five anonymous peer reviews completed.
- Devil’s Advocate memo completed.
- Evidence Auditor memo completed.
- Chairman interim verdict completed.

### Run 001 chairman classification

**Proposed for bounded validation; unresolved for broad sale or final deliverables.**

### Useful Run 001 decisions

Run 001 did not authorize:

- aggregator replacement claims,
- guaranteed ROI claims,
- final public package ladder,
- final public prices,
- final polished sales copy,
- all-in-one launch,
- open-ended custom obligations.

Run 001 did suggest:

- keep aggregators as existing channels,
- test a standardized owned-ordering capability,
- sell or test a controlled validation engagement first,
- let scope follow operational responsibility, not just feature count,
- treat pickup-first as the cleanest initial test configuration, while preserving dissent that it may be too weak to buy or retain.

### Run 001 unresolved gaps

- Incremental direct-channel conversion.
- Profitable channel shift.
- Restaurant payback.
- Direct customer retention.
- UAE provider acquisition cost.
- Onboarding labor.
- Support load.
- Churn.
- Cost-to-serve.
- Gross margin.
- Customization boundaries.
- Restaurant self-service discipline.
- Peak-period reliability.
- Contractual responsibility around refunds, outages, data portability, cancellation, migration, exit, and one-developer continuity.

### Correction after Run 001

The council became too cautious. Future runs must not answer only “insufficient evidence.” They must make bounded decisions under uncertainty, label assumptions, and choose the market action that gets truth fastest.

---

## 7. Product Scope Memory

### What the product is

A reusable restaurant direct-channel system that may include, depending on package or feature selection:

- branded ordering page,
- menu/cart,
- order submission,
- Telegram/WhatsApp/order-dashboard notification,
- order history,
- branded home page / restaurant website,
- QR codes,
- menu management,
- availability toggles,
- structured checkout,
- order dashboard,
- customer records,
- pickup and manual delivery workflows,
- delivery zones and fees,
- payment,
- promotions,
- analytics,
- table QR,
- staff roles,
- branch support,
- POS integration,
- delivery-company integration,
- Telegram ordering bot modules,
- WhatsApp ordering bot modules,
- LLM/agent assistant modules where safe and bounded,
- advanced operations modules.

### What the product is not

It is not:

- a guaranteed replacement for aggregators,
- a guaranteed savings machine,
- unlimited custom software,
- a full POS by default,
- a full ERP by default,
- a delivery company,
- a guaranteed delivery-SLA provider,
- a restaurant marketing agency by default,
- a final public package until validation clarifies scope.

---

## 8. Latest Tier and Feature Corrections

This section overrides older conflicting handoffs.

### Locked latest correction: Tier 0

**Tier 0 is a real lightweight ordering product, not a lead magnet.**

Tier 0 = **Ordering Page**.

Scope:

- one ordering page,
- restaurant logo,
- simple branded header,
- menu/cart,
- customer enters order details,
- order is sent to the restaurant by Telegram,
- small local SQLite order history,
- no authentication,
- no dashboard,
- no full website,
- no payment,
- no customer accounts,
- no POS integration,
- no delivery-company API,
- no table ordering,
- no advanced analytics.

Tier 0 exists to be very small, very fast, very cheap to deploy, and easy to understand.

### Tentative Tier 1

Tier 1 likely adds the restaurant’s basic web presence around the ordering page.

Working name: **Website + Ordering Page** or **Digital Presence**.

Possible scope:

- home page,
- ordering/menu page,
- logo and basic brand colors,
- restaurant story or short intro,
- contact/location/opening hours,
- Google Maps link or embedded map,
- social links,
- QR link,
- Arabic and English where feasible,
- basic SEO / structured information,
- simple order handoff still through Telegram or WhatsApp,
- optional catering or event enquiry form, still undecided.

Tier 1 should remain simple. It should not require a complex dashboard, online payment, delivery API, or POS integration by default.

### Tentative Tier 2

Tier 2 likely becomes the real direct-order workflow tier.

Working name: **Order Dashboard** or **Direct Orders**.

Possible scope:

- login/auth for restaurant staff,
- staff order dashboard,
- order queue,
- accept/reject workflow,
- preparing/ready/completed/cancelled status flow,
- structured customer details,
- pickup orders,
- manual restaurant-owned delivery handling,
- order records,
- basic menu/availability management,
- maybe table QR if council decides it belongs here.

Important boundary:

**Tier 2 should not include guaranteed POS integration as a standard feature.** Staff can manually copy orders into their POS if needed.

### Tentative Tier 3

Tier 3 likely becomes the advanced commerce and supported-integration tier.

Working name: **Direct Commerce + Supported Integrations**.

Possible scope:

- online payment,
- delivery zones,
- delivery-fee rules,
- minimum-order rules,
- customer records,
- saved addresses,
- promotions,
- coupons or offers,
- basic analytics,
- one supported delivery-company integration when adapter exists,
- one supported POS integration path when technically and commercially available.

Important boundary:

Tier 3 must not promise “we integrate with any POS” or “we integrate with any delivery company.” It may include one supported integration path, subject to compatibility and vendor access.

### Future Tier 4

Working name: **Operations Layer**.

Possible scope:

- table QR ordering,
- kitchen view,
- staff roles and permissions,
- branch support,
- advanced reporting,
- multiple delivery-provider integrations,
- own-driver dispatch,
- more serious operational workflows,
- priority support.

### Future Tier 5

Working name: **Integration / ERP Layer**.

Possible scope:

- complex POS integrations,
- aggregator middleware,
- multi-branch operations,
- inventory,
- recipes / ingredient consumption,
- procurement,
- ERP-like operations,
- custom integrations,
- quotation-only enterprise work.

---

## 9. Old Tier History and Conflict Resolution

Older handoffs had two conflicting versions of Tier 0:

1. Tier 0 as an unpriced lead magnet / audit.
2. Tier 0 as a lightweight ordering page.

Latest user correction chooses option 2.

Therefore:

- **Rejected as current truth:** Tier 0 = only a lead magnet.
- **Current truth:** Tier 0 = real ordering page with Telegram orders and local SQLite history.

Old suggested public prices are preserved only as hypotheses. They must not control Run 2 unless the council decides they still make sense.

---

## 10. Packaging Is Not Final

The feature system is clearer than the final pricing system.

The council is allowed to decide between:

1. fixed tiers,
2. feature-based pricing,
3. hybrid tiers plus paid add-ons,
4. setup fee plus recurring support,
5. validation/pilot price first, then real public pricing later,
6. quotation-only for complex integrations.

The council may rearrange features across tiers if it improves sellability, delivery speed, support burden, or profitability.

### Important packaging question

Should restaurants buy a fixed tier, or should they choose features one by one?

Possible answer the council should test:

- Use fixed tiers for clarity.
- Use feature add-ons for flexibility.
- Use custom quotes only for integrations and heavy operations.

But this is not locked yet.

---

## 11. Feature Inventory for Packaging and Pricing

The council should treat this as the working feature inventory.

### Foundation features

- logo/header,
- one ordering page,
- menu categories,
- menu items,
- prices,
- item photos,
- item descriptions,
- cart,
- customer name/phone/order notes,
- Telegram order notification,
- local SQLite order history.

### Website features

- home page,
- restaurant story/introduction,
- contact section,
- opening hours,
- location map,
- social links,
- SEO basics,
- Arabic/English support,
- QR code linking to site or order page.

### Ordering workflow features

- structured checkout,
- pickup/delivery choice,
- address fields,
- location pin,
- staff dashboard,
- accept/reject workflow,
- order status workflow,
- order history,
- customer notifications.

### Commerce features

- online payment,
- payment status,
- refunds workflow,
- delivery zones,
- delivery fee rules,
- minimum order rules,
- promotions,
- coupons,
- customer records,
- saved addresses,
- analytics.

### Restaurant operations features

- table QR,
- area/table management,
- kitchen view,
- staff users,
- roles and permissions,
- branch support,
- advanced reporting,
- availability toggles,
- menu editor,
- content editor.

### Integration features

- POS integration,
- delivery-company integration,
- WhatsApp API,
- Telegram Bot API,
- WhatsApp order handoff,
- deterministic WhatsApp ordering bot,
- WhatsApp AI restaurant assistant,
- deterministic Telegram ordering bot,
- Telegram AI restaurant assistant,
- payment gateway integration,
- webhook integrations,
- Google Business Profile / ordering links,
- aggregator-related middleware in the future.

---

## 12. Channel Add-ons Policy: Website, Telegram, and WhatsApp

Latest user correction: customer-channel bots should be treated as optional modules/add-ons across all tiers, not as features locked to only one tier.

The core product should be understood as:

> An owned ordering system with multiple customer doors.

Possible customer doors:

- website ordering page,
- QR code to website/order page,
- WhatsApp handoff,
- WhatsApp deterministic ordering bot,
- WhatsApp AI restaurant assistant,
- Telegram deterministic ordering bot,
- Telegram AI restaurant assistant,
- future Instagram DM / Messenger channels if later justified.

The website/order backend should remain the source of truth where possible. Bots should be channels into the same menu/order engine, not separate disconnected products.

### Locked channel principle

**LLM can talk. Deterministic system must transact.**

The AI may recommend, explain, answer, translate, guide, and collect intent.

The deterministic backend must own:

- item IDs,
- prices,
- availability,
- cart,
- totals,
- delivery fee,
- address,
- payment status,
- final order confirmation,
- cancellation,
- staff handoff.

No AI assistant should hallucinate prices, invent availability, promise delivery times, create discounts, or confirm an order without controlled backend confirmation.

### Tier relationship

Channel add-ons can be attached to any base tier if the client pays for the module and accepts the operating costs.

Examples:

- Tier 0 can remain a tiny ordering page, but the client may add a Telegram ordering bot.
- Tier 0 can theoretically add a WhatsApp AI assistant, but that should be treated as a paid advanced module, not as default Tier 0 scope.
- Tier 1 can add WhatsApp handoff or Telegram bot.
- Tier 2 can add deterministic bots connected to the order dashboard.
- Tier 3 can add bots connected to payments, customer records, delivery rules, and supported integrations.

The tier defines the base product. Add-ons define extra customer channels.

### Telegram channel modules

#### Telegram 1 — Telegram order receiver

Simplest Telegram layer.

- Orders from website/order page are sent to the restaurant in Telegram.
- This is close to the existing Tier 0 order-notification mechanism.
- Low complexity and low third-party friction.

#### Telegram 2 — Deterministic Telegram ordering bot

A real Telegram bot that guides the customer through ordering.

Possible flow:

- choose language,
- choose category,
- choose dish,
- choose quantity/options,
- add notes,
- choose pickup/delivery,
- enter address or contact,
- confirm order,
- send order to restaurant,
- save order history.

This should use structured menu/cart logic, not free AI generation.

#### Telegram 3 — Telegram AI restaurant assistant

Advanced Telegram assistant.

Possible tasks:

- answer menu questions,
- recommend dishes,
- explain ingredients,
- suggest meals for family/group size,
- handle catering enquiries,
- guide customer into the deterministic cart,
- hand off to staff when uncertain.

The AI layer must call deterministic menu/order tools for prices, availability, cart, totals, and order confirmation.

### WhatsApp channel modules

#### WhatsApp 1 — WhatsApp order handoff

Simplest WhatsApp layer.

- Website/order page prepares a structured WhatsApp message.
- Customer clicks and sends the message to the restaurant.
- No official bot required.
- Low complexity, but the final order still depends on the customer sending the message and staff handling it.

This can be an early add-on or even part of simple packages if commercially useful.

#### WhatsApp 2 — Deterministic WhatsApp ordering bot

A real WhatsApp Business/API-based ordering flow.

Possible flow:

- customer messages restaurant number,
- bot sends categories/menu options,
- customer builds cart,
- bot collects pickup/delivery details,
- bot confirms order,
- order is sent to Telegram/dashboard,
- staff can take over when needed.

This is commercially attractive because many restaurants and customers already use WhatsApp. It is more complex than Telegram because it may require WhatsApp Business Platform setup, webhooks, message templates, account/phone setup, provider/BSP decisions, and per-message or category-based third-party costs.

#### WhatsApp 3 — WhatsApp AI restaurant assistant

Advanced WhatsApp module.

Possible tasks:

- natural-language menu conversation,
- dish recommendations,
- allergen/spice/portion questions,
- catering/event enquiry collection,
- reservation enquiry,
- customer support and order status,
- guided upsell into structured cart.

This should be sold carefully. It must not become an open-domain “ask anything” AI. It must be restaurant-specific, bounded, and connected to deterministic tools.

### Third-party cost policy

Customer-channel modules may create third-party costs outside the builder’s control.

The sales and contract language must distinguish:

- the builder’s setup/build/support fee, and
- pass-through third-party costs.

Examples of third-party costs:

- WhatsApp Business/API message charges,
- WhatsApp provider or BSP fees,
- LLM/API usage fees,
- payment gateway fees,
- SMS/OTP costs,
- delivery-company fees,
- POS vendor/API fees,
- hosting/storage if the client owns infrastructure,
- domain/email/Google Workspace or similar services where relevant.

Recommended customer wording:

> Our price covers setup, software configuration, integration, and agreed support. Third-party usage costs such as WhatsApp messages, AI tokens, payment fees, POS vendor fees, delivery-company fees, hosting, and domains are separate and paid by the restaurant directly or passed through transparently.

### Cost-control policy for AI/bot modules

To control restaurant costs and provider risk:

- prefer deterministic flows for ordering,
- use AI only where it improves conversion or support,
- cache menu explanations where possible,
- limit AI to approved menu and restaurant knowledge,
- set monthly token/message budgets,
- require human handoff for uncertain cases,
- avoid AI confirmation for prices, availability, delivery promises, refunds, or payment status,
- expose usage costs clearly.

### Research tasks for future council

Future council runs should compare:

- website ordering page,
- WhatsApp order handoff,
- deterministic WhatsApp bot,
- WhatsApp AI assistant,
- deterministic Telegram bot,
- Telegram AI assistant,
- hybrid website + WhatsApp + Telegram flow.

The council should decide:

- which modules are easiest to sell,
- which modules are easiest to build,
- which modules have the strongest ROI case,
- which modules have dangerous support or third-party-cost risk,
- whether bots should be sold as add-ons, feature-priced modules, or package upgrades,
- whether Telegram should be used first as the cheaper technical pilot, even if WhatsApp is commercially stronger.

### External reference notes

Reference only; verify again before final customer-facing pricing or contracts:

- Telegram documentation describes the Bot API as a way to create message-based bot interfaces and says Telegram APIs are free of charge.
- Meta documentation describes WhatsApp Business Platform pricing separately from ordinary WhatsApp app usage, and pricing depends on the WhatsApp Business Platform model, message type/category, country, and current Meta rules.
- WhatsApp Business Platform uses webhooks/Graph API-style messaging flows; implementation and policy constraints must be checked before selling advanced WhatsApp modules.

## 13. POS Integration Policy

POS integration is important, but dangerous if promised too broadly.

### Locked boundary

**POS integration is not a standard Tier 2 feature.**

Tier 2 can operate with manual staff workflow. Staff can copy orders into their POS manually if needed.

### Tier 3 / higher boundary

Tier 3 may include a supported POS integration path only when the POS is compatible and the integration is straightforward.

No package should promise “any POS integration.”

### Required future council output

A council run should produce a **POS Integration Compatibility Matrix**.

Each POS system should be classified as:

1. **Supported easily** — API/webhook/order-injection path is clear, accessible, documented, and commercially practical.
2. **Supported with conditions** — possible but requires vendor approval, paid API access, restaurant account tier, middleware, or limited workflow.
3. **Possible but custom/expensive** — should be quoted separately.
4. **Avoid / not supported** — no practical connection path for early product.
5. **Unknown** — requires restaurant-specific inspection.

For each POS, research should check:

- UAE/GCC restaurant adoption relevance,
- API availability,
- webhook support,
- order injection support,
- menu sync support,
- inventory sync support,
- authentication method,
- documentation quality,
- partner program availability,
- pricing or paid API limitations,
- sandbox availability,
- technical difficulty,
- operational reliability,
- support burden,
- whether the integration can be productized.

### Candidate POS/order ecosystems to research

Potential systems mentioned or relevant in previous research include:

- Foodics
- Sapaad
- Syrve / iiko-related ecosystem
- Deliverect / ChatFood ecosystem
- Zyda-connected workflows
- Toast, Square, Lightspeed, Oracle/Micros, and other global systems only if relevant to UAE targets
- any POS discovered in target restaurants during lead calls

The matrix should not be theoretical only. It should help decide whether POS integration belongs in Tier 3, Tier 4, custom quote, or not at all.

---

## 14. Delivery Integration Policy

Delivery integration is valuable but should not be promised too early.

### Locked boundary

Early products should not depend on automated delivery-company API integration.

Tier 0 and Tier 1 have no delivery API.

Tier 2 may support manual pickup and manual restaurant-owned delivery handling.

Tier 3 may include one supported delivery-company integration when a working adapter exists and the provider is suitable.

Tier 4 or custom work may include multiple delivery providers, outsourced rider dispatch, own-driver dispatch, tracking, SLA workflows, and complex fulfilment.

### Delivery providers to research or classify

Previous research included or suggested providers such as:

- Careem Express
- Lyve
- Jeebly
- Quiqup
- Tawseelah
- Roadline
- Go Delivery
- other UAE delivery/white-label providers

Delivery-provider claims must be treated carefully. SLA promises, 99% figures, peak elasticity, and replacement-time claims are vendor claims until validated by pilot or contract.

---

## 15. Technical Architecture Memory

### Tier 0 technical direction

Latest correction:

- local SQLite order history,
- Telegram order delivery,
- one simple ordering page,
- no auth,
- no dashboard.

### Broader product architecture from previous handoffs

Earlier architecture used:

- Astro for public site,
- SvelteKit for dashboard/control panel,
- Supabase for live operational data and auth,
- Cloudflare Pages/Workers for deployment,
- Cloudflare D1 for searchable archive,
- Cloudflare R2 for encrypted durable backups,
- Cloudflare Queues/Workers for archive automation.

### Archive decision

The archive architecture splits live orders from historical storage:

- Supabase stores live operational data and recent orders.
- Cloudflare D1 stores searchable archived order summaries.
- R2 stores durable encrypted order archive objects.

But this must not be overbuilt before the first sale. The architecture is useful for future support and scalability, but the first sellable product should not require the full archive system unless the package demands it.

### Technical-decision boundary for commercial council

The commercial council should not debate frameworks unless they affect:

- customer value,
- restaurant operating burden,
- provider operating cost,
- support burden,
- scalability,
- reliability risk,
- legal or commercial risk,
- profitability,
- delivery time.

---

## 16. Pricing Memory

Pricing is not final.

Old handoffs included suggested prices or ranges, but later pricing briefs instructed the system not to inherit old anchors blindly.

Old prices should be treated as hypotheses, not decisions.

The council may decide:

- validation price,
- launch price,
- setup fee,
- monthly support fee,
- annual support fee,
- per-feature pricing,
- tiered pricing,
- hybrid pricing,
- add-on pricing,
- custom quote for integrations.

### Current pricing reality

The user has urgent cash and licensing constraints. Early sales may need one-time cash or simplified payment terms.

But the product creates ongoing responsibilities. The master handoff must separate:

- **temporary launch selling method**, and
- **correct long-term business model**.

The first few clients may be sold differently from the final mature product.

---

## 17. Support and Responsibility Boundaries

The product must define what the provider is responsible for.

Important responsibility areas:

- uptime,
- order notification reliability,
- Telegram/WhatsApp failure handling,
- dashboard support,
- menu updates,
- payment issues,
- refund workflow,
- delivery failure responsibility,
- POS integration failures,
- restaurant staff mistakes,
- customer complaints,
- data export,
- cancellation,
- migration,
- client infrastructure ownership,
- one-developer continuity.

No package should create unlimited support obligations without recurring revenue or strict boundaries.

---

## 18. Infrastructure Ownership

Open question:

Should early clients run on builder-owned infrastructure first, or client-owned Cloudflare/Supabase accounts from day one?

Previous architecture leaned toward client-owned production infrastructure where possible, but early pilots may require speed.

Recommended handoff stance:

- Client-owned infrastructure is preferred for mature production deployments.
- Builder-owned or shared infrastructure may be acceptable for controlled early pilots if legal, data, and continuity risks are clearly explained.
- Run 2 should decide the pilot posture.

---

## 19. Locked Decisions

These should not be reopened unless new evidence or user correction appears.

1. The product is a reusable direct-channel restaurant product, not unlimited bespoke agency work.
2. The product does not replace Talabat or other aggregators.
3. Aggregators remain discovery channels.
4. The owned channel is for repeat demand, customer control, direct ordering, and structured workflows.
5. Tier 0 is a real ordering page, not a lead magnet.
6. Tier 0 has logo, order page, Telegram orders, local SQLite history, no auth, no dashboard, no payment, no POS, no delivery API.
7. POS integration is not guaranteed generally.
8. POS integration must be researched by POS system and classified by supportability.
9. Delivery API integration is not early by default.
10. Telegram and WhatsApp bot modules are optional customer-channel add-ons, not mandatory core features.
11. Channel add-ons can attach to any base tier if the client pays and accepts third-party costs.
12. LLM assistants may guide and recommend, but deterministic backend systems must own prices, cart, totals, availability, payment status, and final order confirmation.
13. Complex POS, delivery, ERP, AI-agent, and multi-branch operations are higher-tier/custom until validated.
14. Third-party costs must be disclosed separately from builder setup/support fees.
15. Old prices are hypotheses, not final decisions.
16. Councils must make bounded decisions under uncertainty and cannot escape with only “insufficient evidence.”

---

## 20. Open Decisions for Run 2

Run 2 must decide or force market tests for:

1. Fixed tiers versus feature-based pricing versus hybrid pricing.
2. Exact first offer to take to restaurants this week.
3. Whether the first offer is Tier 0, Tier 1, or a validation bundle.
4. Whether Tier 1 includes a home page by default.
5. Whether catering/event enquiry belongs in Tier 1 or is an add-on.
6. Whether table QR belongs in Tier 2, Tier 4, or as an add-on.
7. Whether pickup-first is sellable enough.
8. What exact price or narrow price range to ask first.
9. What recurring support fee or annual support fee to require, if any.
10. What minimum demo is needed before outreach.
11. Which restaurant types and first leads should be approached first.
12. Which POS systems are worth supporting early.
13. Which delivery providers are worth supporting early.
14. What claims are allowed in sales conversation.
15. What claims remain forbidden.
16. Whether WhatsApp/Telegram ordering bots should be core features, optional add-ons, or later modules.
17. Whether deterministic bot flows should be offered before AI assistants.
18. How to separate builder fees from pass-through third-party WhatsApp, Telegram, LLM, payment, POS, delivery, hosting, and domain costs.
19. What market responses validate or kill the offer.

---

## 21. Open Decisions for POS Research

A POS-focused council pass should decide:

- Which UAE-relevant POS systems matter most.
- Which POS systems have public APIs or partner programs.
- Which support order injection.
- Which support menu sync.
- Which support webhooks.
- Which are realistic for one developer.
- Which should be refused or quoted as custom.
- How POS compatibility affects Tier 3 and Tier 4.

This should produce a compatibility matrix, not a vague essay.

---

## 22. Open Decisions for Delivery Research

A delivery-focused pass should decide:

- Which delivery providers are API-friendly.
- Which are only manual/contractual.
- Which are too expensive or risky for early clients.
- Which can support pickup-first, restaurant-owned delivery, outsourced delivery, and tracked delivery.
- Whether delivery integration should be sold as package, feature add-on, or custom quote.

---

## 23. How Future Councils Must Behave

Future councils must start with this master handoff.

They must not behave like a newborn system.

They must distinguish:

- locked decisions,
- latest user corrections,
- old hypotheses,
- evidence-backed claims,
- vendor claims,
- assumptions,
- open decisions,
- market-test decisions.

They may do research, but every stage must end with a decision or market action.

Forbidden final answer pattern:

> “We do not have enough evidence, so no decision.”

Required final answer pattern:

> “Evidence is incomplete. Here is the safest bounded decision, the assumption behind it, the action to test it, and the kill criteria.”

---

## 24. Recommended Next Run

Recommended next run name:

`2026-06-14-decisive-market-action-002`

Run 2 should not be another broad research run. It should be a decisive market-action run that turns the historical handoff and Run 001 into a practical offer to take to restaurants now.

Run 2 should produce:

- immediate offer to take to restaurants,
- exact scope,
- price or narrow price range,
- packaging decision: tiers, features, or hybrid,
- minimum demo requirement,
- target restaurant criteria,
- first outreach targets or target filters,
- owner questions,
- sales conversation structure,
- allowed claims,
- forbidden claims,
- validation criteria,
- kill criteria,
- POS compatibility research plan or first matrix,
- delivery integration posture,
- next upgrade path after first paid client.

---

## 25. Final Memory Sentence

This project is not trying to defeat Talabat. It is trying to help restaurants turn existing attention from Talabat, Google Maps, Instagram, WhatsApp, Telegram, QR, and repeat customers into a structured owned ordering system with multiple customer doors that the restaurant controls, while keeping scope small enough for one builder to sell, deliver, and support.
