# Library Update Report

Run: `2026-06-18-historical-evidence-audit-001-revision`

Added 12 revision source records and 65 atomic claim records.

## Shared Library Updates

- Created `codex-council-v2/library/HISTORICAL_AUDIT_REVISION_OVERLAY_2026-06-19.json`.
- Appended additive `REV-WEB-*` records to `codex-council-v2/library/SOURCE_LEDGER.csv` when absent.
- Preserved contradictory and unresolved evidence instead of overwriting historical decisions.

## New Source Records

|source_id|source_title|publisher|geography|evidence_type|supported_claim_ids|limitations|
|---|---|---|---|---|---|---|
|REV-WEB-001|Pricing & Fees \| Stripe United Arab Emirates|Stripe|United Arab Emirates|official pricing page|HCR-0020; HCR-0021; HCR-0022; HCR-0023; HCR-0024; HCR-0065|Pricing is date-sensitive and may vary for custom contracts or additional Stripe products.|
|REV-WEB-002|Workers pricing|Cloudflare Developers|Global|official pricing documentation|HCR-0054; HCR-0055; HCR-0056; HCR-0065|Usage tiers and included quotas are date-sensitive; exact production cost depends on architecture and traffic.|
|REV-WEB-003|API Pricing|OpenAI|Global|official pricing page|HCR-0057; HCR-0058; HCR-0065|Model availability and prices are date-sensitive; actual spend depends on token usage and caching.|
|REV-WEB-004|Careem Express|Careem|UAE, KSA, Qatar|official vendor product page|HCR-0048; HCR-0049; HCR-0050; HCR-0062|Vendor claims; no public price table, liability terms, or SLA remedies were found on the inspected page.|
|REV-WEB-005|Deliverect Careem Express integration|Deliverect|UAE-relevant|official vendor integration page|HCR-0005; HCR-0008; HCR-0010; HCR-0051; HCR-0052; HCR-0053; HCR-0062; HCR-0063|Vendor capability claim; requires both Careem Express and Deliverect subscriptions and does not prove universal POS compatibility.|
|REV-WEB-006|Foodics pricing|Foodics|GCC/MENA vendor page; UAE-relevant|official vendor pricing page|HCR-0005; HCR-0010; HCR-0036; HCR-0037; HCR-0038; HCR-0039; HCR-0040; HCR-0041; HCR-0063; HCR-0064|Displayed prices/currency and final package may require local sales confirmation; page says specialist quote follows demo.|
|REV-WEB-007|Sapaad pricing/contact for pricing|Sapaad|Global/UAE-relevant|official vendor pricing access page|HCR-0042|Inspected page redirects to contact-for-pricing; fixed public package prices were not available.|
|REV-WEB-008|Wix Restaurant Website Builder|Wix|Global|official vendor capability page|HCR-0005; HCR-0008; HCR-0010; HCR-0043; HCR-0044; HCR-0045; HCR-0063|Vendor claims; UAE operational fit, payment availability, and POS compatibility require account-level validation.|
|REV-WEB-009|Wix Pricing Plans|Wix|Global; prices vary by location|official pricing page|HCR-0046; HCR-0064|USD reference prices; page states prices/currency vary by location and taxes depend on billing address.|
|REV-WEB-010|GloriaFood pricing|GloriaFood|Global|official pricing page|HCR-0047; HCR-0064|Date-sensitive vendor pricing; inspected evidence supports POS price line but not a complete UAE cost stack.|
|REV-WEB-011|SaaS Retention Report|ChartMogul|Global SaaS benchmark|industry benchmark report|HCR-0012; HCR-0013; HCR-0060|Generic SaaS benchmark; not restaurant-specific, UAE-specific, or direct-channel-specific.|
|REV-WEB-012|Meta WhatsApp Business Platform pricing docs access note|Meta|Global/UAE-relevant|official documentation access note|HCR-0059; HCR-0065|Exact UAE rates were not extracted from an inspectable public page in this revision; treat as unresolved.|
