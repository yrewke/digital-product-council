from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "2026-06-18-historical-evidence-audit-001-revision"
RUN_DIR = ROOT / "working" / "evidence-audit-runs" / RUN_ID
LIB_DIR = ROOT / "codex-council-v2" / "library"
TODAY = date(2026, 6, 19).isoformat()


SOURCES = [
    {
        "id": "REV-WEB-001",
        "title": "Pricing & Fees | Stripe United Arab Emirates",
        "publisher": "Stripe",
        "url": "https://stripe.com/ae/pricing",
        "date": "current pricing page inspected 2026-06-19",
        "geo": "United Arab Emirates",
        "type": "official pricing page",
        "limitations": "Pricing is date-sensitive and may vary for custom contracts or additional Stripe products.",
        "review": "Review before any external quote or client proposal.",
    },
    {
        "id": "REV-WEB-002",
        "title": "Workers pricing",
        "publisher": "Cloudflare Developers",
        "url": "https://developers.cloudflare.com/workers/platform/pricing/",
        "date": "current documentation inspected 2026-06-19",
        "geo": "Global",
        "type": "official pricing documentation",
        "limitations": "Usage tiers and included quotas are date-sensitive; exact production cost depends on architecture and traffic.",
        "review": "Review before infrastructure budgeting.",
    },
    {
        "id": "REV-WEB-003",
        "title": "API Pricing",
        "publisher": "OpenAI",
        "url": "https://openai.com/api/pricing/",
        "date": "current pricing page inspected 2026-06-19",
        "geo": "Global",
        "type": "official pricing page",
        "limitations": "Model availability and prices are date-sensitive; actual spend depends on token usage and caching.",
        "review": "Review before AI-cost modeling.",
    },
    {
        "id": "REV-WEB-004",
        "title": "Careem Express",
        "publisher": "Careem",
        "url": "https://www.careem.com/en-AE/express/",
        "date": "current product page inspected 2026-06-19",
        "geo": "UAE, KSA, Qatar",
        "type": "official vendor product page",
        "limitations": "Vendor claims; no public price table, liability terms, or SLA remedies were found on the inspected page.",
        "review": "Review before delivery-provider commitments.",
    },
    {
        "id": "REV-WEB-005",
        "title": "Deliverect Careem Express integration",
        "publisher": "Deliverect",
        "url": "https://www.deliverect.com/en-ae/integrations/careem-express",
        "date": "current integration page inspected 2026-06-19",
        "geo": "UAE-relevant",
        "type": "official vendor integration page",
        "limitations": "Vendor capability claim; requires both Careem Express and Deliverect subscriptions and does not prove universal POS compatibility.",
        "review": "Review for each target restaurant stack.",
    },
    {
        "id": "REV-WEB-006",
        "title": "Foodics pricing",
        "publisher": "Foodics",
        "url": "https://www.foodics.com/pricing/",
        "date": "current pricing page inspected 2026-06-19",
        "geo": "GCC/MENA vendor page; UAE-relevant",
        "type": "official vendor pricing page",
        "limitations": "Displayed prices/currency and final package may require local sales confirmation; page says specialist quote follows demo.",
        "review": "Review before POS-cost comparison.",
    },
    {
        "id": "REV-WEB-007",
        "title": "Sapaad pricing/contact for pricing",
        "publisher": "Sapaad",
        "url": "https://www.sapaad.com/pricing",
        "date": "current page inspected 2026-06-19",
        "geo": "Global/UAE-relevant",
        "type": "official vendor pricing access page",
        "limitations": "Inspected page redirects to contact-for-pricing; fixed public package prices were not available.",
        "review": "Review after vendor quote or current public price page appears.",
    },
    {
        "id": "REV-WEB-008",
        "title": "Wix Restaurant Website Builder",
        "publisher": "Wix",
        "url": "https://www.wix.com/restaurant/website",
        "date": "current product page inspected 2026-06-19",
        "geo": "Global",
        "type": "official vendor capability page",
        "limitations": "Vendor claims; UAE operational fit, payment availability, and POS compatibility require account-level validation.",
        "review": "Review before competitor comparison.",
    },
    {
        "id": "REV-WEB-009",
        "title": "Wix Pricing Plans",
        "publisher": "Wix",
        "url": "https://www.wix.com/plans",
        "date": "current pricing page inspected 2026-06-19",
        "geo": "Global; prices vary by location",
        "type": "official pricing page",
        "limitations": "USD reference prices; page states prices/currency vary by location and taxes depend on billing address.",
        "review": "Review before competitor-price claims.",
    },
    {
        "id": "REV-WEB-010",
        "title": "GloriaFood pricing",
        "publisher": "GloriaFood",
        "url": "https://www.gloriafood.com/pricing",
        "date": "current pricing page inspected 2026-06-19",
        "geo": "Global",
        "type": "official pricing page",
        "limitations": "Date-sensitive vendor pricing; inspected evidence supports POS price line but not a complete UAE cost stack.",
        "review": "Review before competitor-price claims.",
    },
    {
        "id": "REV-WEB-011",
        "title": "SaaS Retention Report",
        "publisher": "ChartMogul",
        "url": "https://chartmogul.com/reports/saas-retention-report/",
        "date": "2025 report page inspected 2026-06-19",
        "geo": "Global SaaS benchmark",
        "type": "industry benchmark report",
        "limitations": "Generic SaaS benchmark; not restaurant-specific, UAE-specific, or direct-channel-specific.",
        "review": "Review when using as support-load/churn proxy.",
    },
    {
        "id": "REV-WEB-012",
        "title": "Meta WhatsApp Business Platform pricing docs access note",
        "publisher": "Meta",
        "url": "https://developers.facebook.com/docs/whatsapp/pricing/",
        "date": "current documentation attempted 2026-06-19",
        "geo": "Global/UAE-relevant",
        "type": "official documentation access note",
        "limitations": "Exact UAE rates were not extracted from an inspectable public page in this revision; treat as unresolved.",
        "review": "Resolve before quoting WhatsApp pass-through costs.",
    },
]


def claim(cid, text, loc, status, geo, conf, etype, srcs="", notes="", gap="", material="yes"):
    run, path, section = loc
    urls = "; ".join(s["url"] for s in SOURCES if s["id"] in srcs.split(";"))
    return {
        "claim_id": cid,
        "claim_text": text,
        "source_file": path,
        "source_section": section,
        "originating_run": run,
        "original_locations": f"{run} | {path} | {section}",
        "current_evidence_status": status,
        "geography": geo,
        "confidence": conf,
        "freshness_or_review_date": TODAY,
        "material_to_historical_decision": material,
        "evidence_type": etype,
        "supporting_source_ids": srcs,
        "supporting_urls": urls,
        "audit_notes": notes,
        "unresolved_gap_id": gap,
    }


LEGACY_PACK = (
    "2026-06-13-commercial-council-001",
    "working/cache/evidence-packs/2026-06-13-commercial-council-001-evidence-pack.md",
    "Evidence pack and gap register",
)
RUN2A = (
    "2026-06-14-full-restaurant-roi-research-calculator-002A-redo",
    "working/council-runs/2026-06-14-full-restaurant-roi-research-calculator-002A-redo/NUMBER_LEDGER.md",
    "Number ledger",
)
RUN2B = (
    "2026-06-14-feature-packaging-decision-002B",
    "working/council-runs/2026-06-14-feature-packaging-decision-002B/PROVIDER_COST_LEDGER.md",
    "Provider cost ledger",
)
RUN2C_PRICE = (
    "2026-06-14-pricing-and-commercial-justification-002C",
    "working/council-runs/2026-06-14-pricing-and-commercial-justification-002C/PRICING_LEDGER.md",
    "Pricing ledger",
)
RUN2C_COMP = (
    "2026-06-14-pricing-and-commercial-justification-002C",
    "working/council-runs/2026-06-14-pricing-and-commercial-justification-002C/COMPETITOR_LEDGER.md",
    "Competitor ledger",
)
REV = (RUN_ID, f"working/evidence-audit-runs/{RUN_ID}", "Public web verification")


CLAIMS = [
    claim("HCR-0001", "A prior evidence pack represented aggregators as roughly 75% of mobile orders in key UAE/Saudi ordering contexts and owned channels/call centers as roughly 25%.", LEGACY_PACK, "STALE_OR_DATE_SENSITIVE", "UAE/GCC", "low", "legacy vendor/secondary claim", notes="The exact public source was not re-opened in this revision; do not reuse as a verified current market share.", gap="GAP-AUD-001"),
    claim("HCR-0002", "A prior UAE young-adult study was used to support that timely delivery and order accuracy are primary retention determinants.", LEGACY_PACK, "SUPPORTED_ESTIMATE", "UAE", "medium", "academic/primary study from prior pack", notes="Material direction is plausible but narrow sample and prior source should be re-opened before external use.", gap="GAP-AUD-002"),
    claim("HCR-0003", "Aggregator commission and platform fees can compress restaurant margins.", LEGACY_PACK, "SUPPORTED_ESTIMATE", "UAE/GCC/global", "medium", "cross-source inference", notes="Direction supported by prior evidence; exact UAE commission rates remain vendor/contract dependent.", gap="GAP-AUD-004"),
    claim("HCR-0004", "Restaurant operators objected in prior evidence to losing customer data and control through aggregator channels.", LEGACY_PACK, "SUPPORTED_ESTIMATE", "UAE/GCC/global", "medium", "prior evidence pack", notes="Preserve as qualitative support, not a quantified market fact."),
    claim("HCR-0005", "Owned-channel orders can integrate with POS, order management, dispatch, tracking, or order-status systems when supported by the relevant vendor stack.", LEGACY_PACK, "VENDOR_CLAIM", "UAE-relevant", "high", "official vendor pages", "REV-WEB-005;REV-WEB-006;REV-WEB-008", "Supported as a capability claim, not as universal compatibility."),
    claim("HCR-0006", "Delivery/POS staging and API/webhook testing can validate technical flows but cannot by itself prove operational readiness.", LEGACY_PACK, "COUNCIL_INFERENCE", "UAE/GCC/global", "medium", "engineering inference", notes="Keep as audit interpretation; validate per vendor sandbox and live operating procedure."),
    claim("HCR-0007", "On-time delivery, first-attempt success, replacement handling, and peak-period performance were selected as candidate pilot gates.", LEGACY_PACK, "SCENARIO_ASSUMPTION", "UAE/GCC", "high", "internal operating assumption", notes="Useful gate design, not an externally proven threshold."),
    claim("HCR-0008", "Direct-ordering tools can increase first-party data/control but still require logistics, payments, integration, and support choices.", LEGACY_PACK, "COUNCIL_INFERENCE", "UAE/GCC/global", "high", "cross-source inference", "REV-WEB-005;REV-WEB-008", "Capability pages support pieces of the stack; economics remain unresolved."),
    claim("HCR-0009", "Aggregator and direct ordering can coexist; exact profitable channel-shift rates for UAE restaurants remain unresolved.", LEGACY_PACK, "UNRESOLVED_GAP", "UAE/GCC", "high", "gap finding", notes="No current public source inspected in this revision quantified reliable UAE direct-channel conversion or substitution.", gap="GAP-AUD-001"),
    claim("HCR-0010", "Standardized rapid launch is a vendor-style capability claim, while POS, delivery, menu, payments, and local process setup introduce manual work.", LEGACY_PACK, "SUPPORTED_ESTIMATE", "UAE/GCC/global", "medium", "vendor pages plus council inference", "REV-WEB-005;REV-WEB-006;REV-WEB-008", "Do not present rapid launch as universal."),
    claim("HCR-0011", "The prior record contains a tension between limiting customization for cost control and needing local personalization for restaurants.", LEGACY_PACK, "COUNCIL_INFERENCE", "UAE/GCC", "high", "historical-audit interpretation", notes="Contradictory pressure preserved rather than resolved away."),
    claim("HCR-0012", "Low-ARPA SaaS businesses generally show weaker net revenue retention than higher-ARPA SaaS businesses in ChartMogul's benchmark sample.", LEGACY_PACK, "VERIFIED_FACT", "Global SaaS", "high", "industry benchmark", "REV-WEB-011", "Relevant as a support-load/churn caution only; not restaurant-specific."),
    claim("HCR-0013", "ChartMogul reports that only 2.7% of SaaS businesses with ARPA below $10/month had net revenue retention above 100%, versus 41.1% for ARPA above $500/month.", LEGACY_PACK, "VERIFIED_FACT", "Global SaaS", "high", "industry benchmark", "REV-WEB-011", "Use as exact benchmark with report limitations."),
    claim("HCR-0014", "Guaranteed ROI claims were prohibited in the historical commercial council artifacts.", RUN2A, "INTERNAL_PROJECT_FACT", "Project", "high", "internal decision", notes="Decision preserved; audit only checks evidence condition."),
    claim("HCR-0015", "Marketplace commission scenarios of 15%, 25%, and 35% were used as scenario inputs, not verified UAE restaurant contract rates.", RUN2A, "SCENARIO_ASSUMPTION", "UAE/GCC", "high", "scenario model input", notes="Keep out of verified-fact language.", gap="GAP-AUD-004"),
    claim("HCR-0016", "Shifted-order scenarios of 2%, 7%, and 15% were used as assumptions requiring validation.", RUN2A, "SCENARIO_ASSUMPTION", "UAE/GCC", "high", "scenario model input", notes="No inspected public UAE source supported these exact rates.", gap="GAP-AUD-001"),
    claim("HCR-0017", "Incremental-order scenarios of 0%, 2%, and 5% were used as assumptions requiring validation.", RUN2A, "SCENARIO_ASSUMPTION", "UAE/GCC", "high", "scenario model input", notes="Do not state as expected uplift.", gap="GAP-AUD-002"),
    claim("HCR-0018", "Minutes-saved scenarios of 3, 5, and 8 minutes per order were model assumptions requiring validation.", RUN2A, "SCENARIO_ASSUMPTION", "UAE/GCC", "high", "scenario model input", notes="Requires live pilot timing evidence.", gap="GAP-AUD-002"),
    claim("HCR-0019", "Mistake-reduction scenarios of 1%, 3%, and 5% were model assumptions requiring validation.", RUN2A, "SCENARIO_ASSUMPTION", "UAE/GCC", "high", "scenario model input", notes="Requires live pilot defect-rate evidence.", gap="GAP-AUD-002"),
    claim("HCR-0020", "Stripe UAE lists domestic card pricing at 2.9% plus AED 1.00 per successful transaction.", RUN2A, "VERIFIED_FACT", "UAE", "high", "official pricing page", "REV-WEB-001", "Date-sensitive payment cost."),
    claim("HCR-0021", "Stripe UAE lists an additional 1% fee for international cards.", RUN2A, "VERIFIED_FACT", "UAE", "high", "official pricing page", "REV-WEB-001", "Date-sensitive payment cost."),
    claim("HCR-0022", "Stripe UAE lists an additional 1% fee if currency conversion is required.", RUN2A, "VERIFIED_FACT", "UAE", "high", "official pricing page", "REV-WEB-001", "Date-sensitive payment cost."),
    claim("HCR-0023", "Stripe UAE lists AED 60 per dispute received and AED 60 for manual evidence submission, returned if the dispute is won.", RUN2A, "VERIFIED_FACT", "UAE", "high", "official pricing page", "REV-WEB-001", "Date-sensitive payment cost."),
    claim("HCR-0024", "Stripe Checkout or Payment Links custom domains are listed at $10 per month.", RUN2A, "VERIFIED_FACT", "Global/UAE", "high", "official pricing page", "REV-WEB-001", "Date-sensitive optional cost."),
    claim("HCR-0025", "Telegram Bot API cost was treated as zero for normal Bot API use in a prior ledger.", RUN2A, "STALE_OR_DATE_SENSITIVE", "Global", "low", "prior ledger item", notes="Not re-verified in this revision; keep out of current cost claims until re-opened.", gap="GAP-AUD-007"),
    claim("HCR-0026", "Tier 0 launch setup price was set internally at AED 2,900 and standard setup at AED 3,600.", RUN2C_PRICE, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal pricing verdict", notes="Historical decision preserved; not a market price."),
    claim("HCR-0027", "Tier 0 managed monthly fee was set internally at AED 350, with optional client-owned support at AED 250.", RUN2C_PRICE, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal pricing verdict", notes="Historical decision preserved; not externally verified."),
    claim("HCR-0028", "Tier 1 launch setup price was set internally at AED 5,900 and standard setup at AED 7,500.", RUN2C_PRICE, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal pricing verdict", notes="Historical decision preserved; not externally verified."),
    claim("HCR-0029", "Tier 1 managed monthly fee was set internally at AED 650, with optional client-owned support at AED 450.", RUN2C_PRICE, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal pricing verdict", notes="Historical decision preserved; not externally verified."),
    claim("HCR-0030", "Tier 2 launch setup price was set internally at AED 12,000 after AED 2,500 discovery, with standard setup at AED 15,000 after discovery.", RUN2C_PRICE, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal pricing verdict", notes="Historical decision preserved; not externally verified."),
    claim("HCR-0031", "Tier 2 managed monthly fee was set internally at AED 1,100 and client-owned support was unavailable for the initial cohort.", RUN2C_PRICE, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal pricing verdict", notes="Historical decision preserved; not externally verified."),
    claim("HCR-0032", "A cheap AED 300 WordPress/freelancer alternative was logged as an owner-objection hypothesis rather than a sourced market benchmark.", RUN2C_COMP, "INTERNAL_PROJECT_FACT", "UAE", "high", "internal competitor framing", notes="Do not cite AED 300 as verified competitor pricing.", gap="GAP-AUD-004"),
    claim("HCR-0033", "Manual WhatsApp and phone ordering remained a strong real alternative in the historical competitor ledger.", RUN2C_COMP, "COUNCIL_INFERENCE", "UAE/GCC", "medium", "internal competitive analysis", notes="Needs current WhatsApp/payments/support cost verification for pricing claims.", gap="GAP-AUD-007"),
    claim("HCR-0034", "Delivery API and courier integrations were excluded from early core dependency and treated as integration-gated scope.", RUN2B, "INTERNAL_PROJECT_FACT", "Project", "high", "internal scope decision", notes="Decision preserved; current provider details remain incomplete.", gap="GAP-AUD-005"),
    claim("HCR-0035", "POS integration was not promised universally in the historical packaging decisions.", RUN2B, "INTERNAL_PROJECT_FACT", "Project", "high", "internal scope decision", notes="Consistent with current vendor-specific support evidence.", gap="GAP-AUD-006"),
    claim("HCR-0036", "Foodics displayed a QSR/cafes Starter Bundle at 423 per month, or 392 per month when billed annually, on the inspected pricing page.", REV, "STALE_OR_DATE_SENSITIVE", "GCC/MENA vendor page", "medium", "official pricing page", "REV-WEB-006", "Currency and final quote should be confirmed locally."),
    claim("HCR-0037", "Foodics displayed QSR/cafes Basic at 801 monthly or 742 annually and Advanced at 1224 monthly or 1133 annually.", REV, "STALE_OR_DATE_SENSITIVE", "GCC/MENA vendor page", "medium", "official pricing page", "REV-WEB-006", "Currency and final quote should be confirmed locally."),
    claim("HCR-0038", "Foodics displayed Cloud Kitchen Basic at 612 monthly or 567 annually and Advanced at 936 monthly or 867 annually.", REV, "STALE_OR_DATE_SENSITIVE", "GCC/MENA vendor page", "medium", "official pricing page", "REV-WEB-006", "Currency and final quote should be confirmed locally."),
    claim("HCR-0039", "Foodics displayed Dine-in Basic at 1183 monthly or 1096 annually.", REV, "STALE_OR_DATE_SENSITIVE", "GCC/MENA vendor page", "medium", "official pricing page", "REV-WEB-006", "Currency and final quote should be confirmed locally."),
    claim("HCR-0040", "Foodics package text listed API Integration in selected higher packages.", REV, "VENDOR_CLAIM", "GCC/MENA vendor page", "high", "official vendor capability page", "REV-WEB-006", "Capability requires package and implementation validation."),
    claim("HCR-0041", "Foodics Cloud Kitchen package text listed food delivery integration and delivery-zone features.", REV, "VENDOR_CLAIM", "GCC/MENA vendor page", "high", "official vendor capability page", "REV-WEB-006", "Capability requires package and implementation validation."),
    claim("HCR-0042", "Sapaad did not expose a fixed public package price on the inspected pricing URL and redirected to contact-for-pricing content.", REV, "UNRESOLVED_GAP", "UAE-relevant", "high", "official vendor pricing access page", "REV-WEB-007", "Requires quote or updated public page.", "GAP-AUD-004"),
    claim("HCR-0043", "Wix Restaurant Website Builder claims support for online menus, reservations, payments, and one dashboard.", REV, "VENDOR_CLAIM", "Global", "high", "official vendor capability page", "REV-WEB-008", "Not UAE-specific validation."),
    claim("HCR-0044", "Wix Restaurant Website Builder claims delivery integration, loyalty, marketing, and POS syncing capabilities.", REV, "VENDOR_CLAIM", "Global", "high", "official vendor capability page", "REV-WEB-008", "Compatibility and UAE availability require account-level checks."),
    claim("HCR-0045", "Wix states that Wix Restaurants offers commission-free online ordering.", REV, "VENDOR_CLAIM", "Global", "high", "official vendor capability page", "REV-WEB-008", "Commission-free platform claim does not include payment, delivery, or app costs."),
    claim("HCR-0046", "Wix pricing page displayed Core at $29.77/month, Business at $39.77/month, and Business Elite at $159.77/month on the inspected page.", REV, "STALE_OR_DATE_SENSITIVE", "Global; location varies", "medium", "official pricing page", "REV-WEB-009", "Wix states prices and currency vary by location."),
    claim("HCR-0047", "GloriaFood displayed Restaurant POS System pricing at US$49/month/location with a two-year commitment.", REV, "STALE_OR_DATE_SENSITIVE", "Global", "high", "official pricing page", "REV-WEB-010", "Not a complete restaurant-ordering cost stack."),
    claim("HCR-0048", "Careem Express claims 30-40 minute delivery, advanced mapping and dispatch, and real-time tracking.", REV, "VENDOR_CLAIM", "UAE/KSA/Qatar", "high", "official vendor product page", "REV-WEB-004", "No price, liability, or SLA-remedy table found on inspected page."),
    claim("HCR-0049", "Careem Express states it operates in 11 cities across the UAE, KSA, and Qatar.", REV, "VENDOR_CLAIM", "UAE/KSA/Qatar", "high", "official vendor product page", "REV-WEB-004", "City-level coverage must be checked per restaurant location."),
    claim("HCR-0050", "Careem Express page offers delivery-volume bands of 0-50, 50-100, 100-200, 200-300, and 300+ monthly deliveries.", REV, "VERIFIED_FACT", "UAE/KSA/Qatar", "high", "official vendor product page", "REV-WEB-004", "Intake form bands, not pricing bands."),
    claim("HCR-0051", "Deliverect says its Careem Express integration can connect Careem to an in-house order-management system and integrate online orders directly to the POS.", REV, "VENDOR_CLAIM", "UAE-relevant", "high", "official vendor integration page", "REV-WEB-005", "Requires Careem Express and Deliverect subscriptions."),
    claim("HCR-0052", "Deliverect says the Careem Express integration supports automated dispatch and real-time delivery tracking.", REV, "VENDOR_CLAIM", "UAE-relevant", "high", "official vendor integration page", "REV-WEB-005", "Vendor claim; validate operational SLA separately."),
    claim("HCR-0053", "Deliverect describes more than 1000 integration partners across POS, marketplace, online ordering, on-site ordering, third-party dispatch, and loyalty/CRM categories.", REV, "VENDOR_CLAIM", "Global/UAE-relevant", "medium", "official vendor integration page", "REV-WEB-005", "Broad vendor count; does not prove support for a specific restaurant's POS."),
    claim("HCR-0054", "Cloudflare Workers Paid plan has a $5 per month minimum and includes Workers, Pages Functions, KV, Hyperdrive, and Durable Objects usage.", REV, "VERIFIED_FACT", "Global", "high", "official pricing documentation", "REV-WEB-002", "Date-sensitive infrastructure cost."),
    claim("HCR-0055", "Cloudflare Workers pricing documentation lists KV and D1 availability on Free and Paid plans with included limits.", REV, "VERIFIED_FACT", "Global", "high", "official pricing documentation", "REV-WEB-002", "Exact quota planning requires current page review."),
    claim("HCR-0056", "Cloudflare Durable Objects are available with Free and Paid Workers tiers, with separate request/duration/storage pricing details.", REV, "VERIFIED_FACT", "Global", "high", "official pricing documentation", "REV-WEB-002", "Architecture-dependent cost."),
    claim("HCR-0057", "OpenAI API pricing page displayed GPT-5.5 at $5.00 per 1M input tokens, $0.50 cached input, and $30.00 output.", REV, "VERIFIED_FACT", "Global", "high", "official pricing page", "REV-WEB-003", "Date-sensitive AI cost."),
    claim("HCR-0058", "OpenAI API pricing page displayed GPT-5.4 at $2.50 per 1M input tokens, $0.25 cached input, and $15.00 output.", REV, "VERIFIED_FACT", "Global", "high", "official pricing page", "REV-WEB-003", "Date-sensitive AI cost."),
    claim("HCR-0059", "Exact UAE WhatsApp Business Platform pass-through rates were not verified from an inspectable public Meta page in this revision.", REV, "UNRESOLVED_GAP", "UAE", "high", "official docs access note", "REV-WEB-012", "Resolve before quoting WhatsApp costs.", "GAP-AUD-007"),
    claim("HCR-0060", "Provider CAC, onboarding labor, support load, churn, and margins for the proposed builder model remain unsupported by public evidence in this revision.", LEGACY_PACK, "UNRESOLVED_GAP", "UAE/GCC", "high", "gap finding", "REV-WEB-011", "Generic SaaS retention evidence is only a proxy.", "GAP-AUD-003"),
    claim("HCR-0061", "Restaurant ROI and payback for the proposed direct-channel package remain unresolved because public evidence did not verify conversion, substitution, labor saving, or defect reduction assumptions.", RUN2A, "UNRESOLVED_GAP", "UAE/GCC", "high", "gap finding", notes="Requires pilots or narrowly matched primary research.", gap="GAP-AUD-002"),
    claim("HCR-0062", "Delivery-provider public pages inspected in this revision did not expose complete price, SLA-remedy, and liability terms.", REV, "UNRESOLVED_GAP", "UAE", "high", "gap finding", "REV-WEB-004;REV-WEB-005", "Vendor capability evidence exists; commercial/legal terms remain incomplete.", "GAP-AUD-005"),
    claim("HCR-0063", "UAE-relevant POS integration support is vendor-specific rather than universal.", REV, "SUPPORTED_ESTIMATE", "UAE/GCC", "high", "official vendor pages", "REV-WEB-005;REV-WEB-006;REV-WEB-008", "Matches historical decision not to promise universal POS integration.", "GAP-AUD-006"),
    claim("HCR-0064", "Current competitor and freelancer pricing remains only partially verified: Wix, GloriaFood, and Foodics anchors were found, but cheap freelancer pricing and full UAE agency pricing were not verified.", RUN2C_COMP, "UNRESOLVED_GAP", "UAE/GCC/global", "high", "gap finding", "REV-WEB-006;REV-WEB-009;REV-WEB-010", "Use verified anchors separately from unsupported cheap-freelancer claims.", "GAP-AUD-004"),
    claim("HCR-0065", "Current domain, hosting, AI, payment, and WhatsApp costs remain partly verified: Stripe, Cloudflare, and OpenAI were verified; WhatsApp and domain/commodity hosting remain incomplete.", REV, "UNRESOLVED_GAP", "UAE/global", "high", "gap finding", "REV-WEB-001;REV-WEB-002;REV-WEB-003;REV-WEB-012", "Do not roll unresolved items into a verified monthly cost.", "GAP-AUD-007"),
]


GAPS = [
    ("GAP-AUD-001", "UAE direct-channel conversion and channel shift", "No inspected current public source quantified reliable UAE restaurant direct-channel substitution or conversion rates.", "High", "Pilot analytics, aggregator/direct channel order logs, current UAE restaurant studies."),
    ("GAP-AUD-002", "Restaurant ROI and payback", "Payback remains model-dependent because conversion, incremental demand, minutes saved, and error reduction are assumptions.", "High", "Restaurant pilots with order mix, labor timing, defect rates, CAC/payback model."),
    ("GAP-AUD-003", "Provider CAC, onboarding, support load, churn, and margins", "Only generic SaaS retention proxy found; no builder-specific UAE economics verified.", "High", "Internal time tracking, support tickets, churn cohorts, sales funnel metrics."),
    ("GAP-AUD-004", "Current competitor and freelancer pricing", "Official SaaS anchors were added, but cheap freelancer/agency benchmarks and custom-quote vendors remain incomplete.", "Medium", "Fresh UAE marketplace quotes, agency quotes, Sapaad/Foodics local quotes."),
    ("GAP-AUD-005", "Delivery-provider prices, APIs, SLAs, and liability", "Careem and Deliverect capability evidence found; public price, SLA remedies, and liability terms were not found.", "High", "Provider commercial terms, API docs, contracts, SLA schedules."),
    ("GAP-AUD-006", "UAE-relevant POS integration support", "Vendor pages show capabilities but not universal support for every target POS/version/package.", "Medium", "POS-by-POS matrix with package, API access, webhook, and UAE availability."),
    ("GAP-AUD-007", "Current WhatsApp, payment, hosting, domain, and AI costs", "Stripe, Cloudflare, and OpenAI were verified; WhatsApp exact rates and commodity domain/hosting anchors remain incomplete.", "High", "Meta pricing calculator/docs, registrar/domain quotes, chosen hosting architecture."),
]


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows, headers):
    out = ["|" + "|".join(headers) + "|", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("|" + "|".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", " ") for h in headers) + "|")
    return "\n".join(out)


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    LIB_DIR.mkdir(parents=True, exist_ok=True)

    claim_fields = list(CLAIMS[0].keys())
    write_csv(RUN_DIR / "HISTORICAL_CLAIM_LEDGER.csv", CLAIMS, claim_fields)

    query_rows = [
        {"query_id": "QREV-001", "agent": "Research Librarian", "query": "Stripe UAE pricing domestic international currency conversion dispute custom domain", "source_opened": "https://stripe.com/ae/pricing", "result": "Used", "notes": "Official page supported payment-cost claims."},
        {"query_id": "QREV-002", "agent": "Research Librarian", "query": "Cloudflare Workers pricing KV D1 Durable Objects paid plan", "source_opened": "https://developers.cloudflare.com/workers/platform/pricing/", "result": "Used", "notes": "Official docs supported infrastructure-cost claims."},
        {"query_id": "QREV-003", "agent": "Research Librarian", "query": "OpenAI API pricing GPT-5.5 GPT-5.4", "source_opened": "https://openai.com/api/pricing/", "result": "Used", "notes": "Official pricing page supported AI-cost claims."},
        {"query_id": "QREV-004", "agent": "Research Librarian", "query": "Careem Express UAE delivery API SLA pricing", "source_opened": "https://www.careem.com/en-AE/express/", "result": "Partial", "notes": "Capabilities found; no public price/SLA/liability schedule."},
        {"query_id": "QREV-005", "agent": "Research Librarian", "query": "Deliverect Careem Express integration POS dispatch tracking", "source_opened": "https://www.deliverect.com/en-ae/integrations/careem-express", "result": "Used", "notes": "Vendor integration claims and prerequisites captured."},
        {"query_id": "QREV-006", "agent": "Research Librarian", "query": "Foodics pricing API integration delivery zones UAE", "source_opened": "https://www.foodics.com/pricing/", "result": "Used", "notes": "Public pricing and capabilities captured with caveats."},
        {"query_id": "QREV-007", "agent": "Research Librarian", "query": "Sapaad pricing UAE POS API integration", "source_opened": "https://www.sapaad.com/pricing", "result": "Partial", "notes": "Contact-for-pricing; no fixed public prices captured."},
        {"query_id": "QREV-008", "agent": "Research Librarian", "query": "Wix restaurant website online ordering commission free POS syncing pricing", "source_opened": "https://www.wix.com/restaurant/website; https://www.wix.com/plans", "result": "Used", "notes": "Capability and USD/location-variable price anchors captured."},
        {"query_id": "QREV-009", "agent": "Research Librarian", "query": "GloriaFood pricing restaurant POS monthly location", "source_opened": "https://www.gloriafood.com/pricing", "result": "Partial", "notes": "POS price line captured; complete UAE stack not captured."},
        {"query_id": "QREV-010", "agent": "Evidence Auditor / Fact Checker", "query": "UAE direct channel restaurant conversion payback SaaS CAC support churn WhatsApp pricing", "source_opened": "Multiple public searches and inspected pages", "result": "Gap", "notes": "No inspectable current public source resolved the seven historical gaps completely."},
    ]
    write_csv(RUN_DIR / "QUERY_LEDGER.csv", query_rows, list(query_rows[0].keys()))

    source_rows = []
    for src in SOURCES:
        supported = [c["claim_id"] for c in CLAIMS if src["id"] in c["supporting_source_ids"].split(";")]
        source_rows.append({
            "source_id": src["id"],
            "source_title": src["title"],
            "publisher": src["publisher"],
            "publication_or_update_date": src["date"],
            "retrieval_date": TODAY,
            "geography": src["geo"],
            "evidence_type": src["type"],
            "exact_source_url": src["url"],
            "supported_claim_ids": "; ".join(supported),
            "limitations": src["limitations"],
            "freshness_or_review_date": src["review"],
        })

    source_md = "# Source Ledger\n\n"
    source_md += f"Revision: `{RUN_ID}`\n\nNotebookLM queries used in this revision: `0`.\n\n"
    source_md += md_table(source_rows, list(source_rows[0].keys())) + "\n"
    (RUN_DIR / "SOURCE_LEDGER.md").write_text(source_md, encoding="utf-8")

    gap_rows = [{"gap_id": gid, "gap": title, "condition": condition, "priority": priority, "next_evidence_needed": needed} for gid, title, condition, priority, needed in GAPS]
    gaps_md = "# Unresolved Evidence Gaps\n\n"
    gaps_md += "These gap IDs are the authoritative unresolved set for this revision and are referenced from `HISTORICAL_CLAIM_LEDGER.csv`.\n\n"
    gaps_md += md_table(gap_rows, ["gap_id", "gap", "condition", "priority", "next_evidence_needed"]) + "\n"
    (RUN_DIR / "UNRESOLVED_EVIDENCE_GAPS.md").write_text(gaps_md, encoding="utf-8")

    status_counts = Counter(c["current_evidence_status"] for c in CLAIMS)
    fact_md = "# Fact Checker Report\n\n"
    fact_md += f"Run: `{RUN_ID}`\n\nAgents used: Evidence Auditor / Fact Checker; Research Librarian.\n\nNotebookLM used: `No`.\n\n"
    fact_md += "## Evidence Condition\n\n"
    fact_md += "\n".join(f"- `{k}`: {status_counts[k]}" for k in sorted(status_counts)) + "\n\n"
    fact_md += "## Principal Findings\n\n"
    fact_md += "- The repaired ledger is atomic: each row now represents one independently checkable factual statement, number, policy, price, capability, comparison, or assumption.\n"
    fact_md += "- Stripe UAE payment fees, Cloudflare Workers baseline infrastructure costs, OpenAI API model prices, selected Wix/GloriaFood/Foodics price anchors, and several Careem/Deliverect capability claims now have current inspected public web sources.\n"
    fact_md += "- Stale, vendor-dependent, scenario, and internal project claims are explicitly separated from verified facts.\n"
    fact_md += "- The seven historical unresolved areas remain unresolved where public evidence did not support the exact claim. They are preserved as gaps rather than softened into facts.\n"
    fact_md += "- No previous pricing, package, verdict, or strategy decision was reopened or changed.\n\n"
    fact_md += "## High-Risk Caveats\n\n"
    fact_md += "- UAE direct-channel conversion, restaurant payback, and provider economics still require first-party pilot or commercial data.\n"
    fact_md += "- Vendor pages support capability claims but do not prove universal POS/delivery compatibility, SLA remedies, or liability boundaries.\n"
    fact_md += "- WhatsApp exact UAE pass-through pricing was not verified from an inspectable public page in this revision.\n"
    (RUN_DIR / "FACT_CHECKER_REPORT.md").write_text(fact_md, encoding="utf-8")

    lib_md = "# Library Update Report\n\n"
    lib_md += f"Run: `{RUN_ID}`\n\n"
    lib_md += f"Added {len(SOURCES)} revision source records and {len(CLAIMS)} atomic claim records.\n\n"
    lib_md += "## Shared Library Updates\n\n"
    lib_md += "- Created `codex-council-v2/library/HISTORICAL_AUDIT_REVISION_OVERLAY_2026-06-19.json`.\n"
    lib_md += "- Appended additive `REV-WEB-*` records to `codex-council-v2/library/SOURCE_LEDGER.csv` when absent.\n"
    lib_md += "- Preserved contradictory and unresolved evidence instead of overwriting historical decisions.\n\n"
    lib_md += "## New Source Records\n\n"
    lib_md += md_table(source_rows, ["source_id", "source_title", "publisher", "geography", "evidence_type", "supported_claim_ids", "limitations"]) + "\n"
    (RUN_DIR / "LIBRARY_UPDATE_REPORT.md").write_text(lib_md, encoding="utf-8")

    map_rows = [
        {"decision_area": "Run 001 commercial direction", "historical_decision_preserved": "Yes", "evidence_condition": "Directional support remains, but UAE channel-shift and direct conversion rates are unresolved.", "claim_ids": "HCR-0001; HCR-0008; HCR-0009; HCR-0010"},
        {"decision_area": "Run 2A ROI calculator discipline", "historical_decision_preserved": "Yes", "evidence_condition": "ROI guarantee prohibition verified as internal decision; model inputs remain scenario assumptions.", "claim_ids": "HCR-0014; HCR-0015; HCR-0016; HCR-0017; HCR-0018; HCR-0019; HCR-0061"},
        {"decision_area": "Run 2B feature packaging", "historical_decision_preserved": "Yes", "evidence_condition": "Delivery/POS integration gating remains supported by current vendor-specific evidence.", "claim_ids": "HCR-0034; HCR-0035; HCR-0051; HCR-0052; HCR-0063"},
        {"decision_area": "Run 2C price card", "historical_decision_preserved": "Yes", "evidence_condition": "Prices are internal project facts, not market-verified facts; third-party costs have partial current verification.", "claim_ids": "HCR-0026; HCR-0027; HCR-0028; HCR-0029; HCR-0030; HCR-0031; HCR-0065"},
        {"decision_area": "Competitor positioning", "historical_decision_preserved": "Yes", "evidence_condition": "Official SaaS price anchors added; cheap freelancer/agency pricing remains unresolved.", "claim_ids": "HCR-0032; HCR-0042; HCR-0043; HCR-0044; HCR-0045; HCR-0046; HCR-0047; HCR-0064"},
    ]
    map_md = "# Historical Decision Evidence Map\n\n"
    map_md += "This map reports evidence condition beneath historical decisions. It does not reopen, edit, or replace those decisions.\n\n"
    map_md += md_table(map_rows, ["decision_area", "historical_decision_preserved", "evidence_condition", "claim_ids"]) + "\n"
    (RUN_DIR / "HISTORICAL_DECISION_EVIDENCE_MAP.md").write_text(map_md, encoding="utf-8")

    handoff_md = "# Next Run Evidence Handoff\n\n"
    handoff_md += "Use this handoff only for future evidence work. Do not treat it as a pricing or strategy revision.\n\n"
    handoff_md += "## Carry Forward\n\n"
    handoff_md += "- Use `HISTORICAL_CLAIM_LEDGER.csv` as the authoritative claim ledger for the revision.\n"
    handoff_md += "- Keep `GAP-AUD-001` through `GAP-AUD-007` aligned with `UNRESOLVED_EVIDENCE_GAPS.md`.\n"
    handoff_md += "- Re-check all `STALE_OR_DATE_SENSITIVE` rows before customer-facing use.\n"
    handoff_md += "- Treat all vendor capability rows as vendor claims until tested against a target restaurant stack.\n\n"
    handoff_md += "## Priority Evidence Tasks\n\n"
    handoff_md += "\n".join(f"- `{gid}`: {title}." for gid, title, *_ in GAPS) + "\n"
    (RUN_DIR / "NEXT_RUN_EVIDENCE_HANDOFF.md").write_text(handoff_md, encoding="utf-8")

    run_status = "# Run Status\n\n"
    run_status += f"Run: `{RUN_ID}`\n\nStatus: `COMPLETE`\n\n"
    run_status += "## Completion Checks\n\n"
    checks = [
        "Material claims are atomic rather than whole-document summaries.",
        "Every material claim has a clear evidence status.",
        "Current public web sources are attached where available.",
        "Unresolved gaps in the claim ledger agree with `UNRESOLVED_EVIDENCE_GAPS.md`.",
        "Stale and vendor-dependent claims are not presented as verified facts.",
        "Previous decisions remain untouched.",
        "The shared evidence library is enriched with revision source records and overlay JSON.",
        "NotebookLM was not used.",
    ]
    run_status += "\n".join(f"- [x] {c}" for c in checks) + "\n\n"
    run_status += f"Atomic claims: `{len(CLAIMS)}`\n\nSource records: `{len(SOURCES)}`\n\n"
    (RUN_DIR / "RUN_STATUS.md").write_text(run_status, encoding="utf-8")

    inv_src = ROOT / "working" / "evidence-audit-runs" / "2026-06-18-historical-evidence-audit-001" / "HISTORICAL_RUN_INVENTORY.md"
    if inv_src.exists():
        (RUN_DIR / "HISTORICAL_RUN_INVENTORY.md").write_text(inv_src.read_text(encoding="utf-8"), encoding="utf-8")

    overlay = {
        "run_id": RUN_ID,
        "retrieval_date": TODAY,
        "notebooklm_used": False,
        "agents_used": ["Evidence Auditor / Fact Checker", "Research Librarian"],
        "source_records": source_rows,
        "claim_count": len(CLAIMS),
        "status_counts": dict(status_counts),
        "gap_ids": [g[0] for g in GAPS],
    }
    (LIB_DIR / "HISTORICAL_AUDIT_REVISION_OVERLAY_2026-06-19.json").write_text(json.dumps(overlay, indent=2), encoding="utf-8")

    lib_source = LIB_DIR / "SOURCE_LEDGER.csv"
    existing_ids = set()
    if lib_source.exists():
        with lib_source.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing_ids.add(row.get("source_id", ""))
    with lib_source.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source_id", "title", "classification", "geography", "retrieval_date", "legacy_run_id", "original_path", "archive_path", "sha256", "limitations"])
        if lib_source.stat().st_size == 0:
            writer.writeheader()
        for src in SOURCES:
            if src["id"] in existing_ids:
                continue
            writer.writerow({
                "source_id": src["id"],
                "title": src["title"],
                "classification": "CURRENT_WEB_SOURCE",
                "geography": src["geo"],
                "retrieval_date": TODAY,
                "legacy_run_id": RUN_ID,
                "original_path": src["url"],
                "archive_path": f"working/evidence-audit-runs/{RUN_ID}/SOURCE_LEDGER.md",
                "sha256": "",
                "limitations": src["limitations"],
            })

    print(f"Wrote {len(CLAIMS)} claims, {len(SOURCES)} sources, {len(GAPS)} gaps to {RUN_DIR}")


if __name__ == "__main__":
    main()
