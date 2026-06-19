# Run Charter

## Run ID

2026-06-19-full-commercial-recalibration-003R

## Title

Full Commercial Recalibration, ROI, Product, and Pricing

## Central Question

What current commercial model should govern future restaurant direct-ordering product development, sales materials, ROI reports, pricing, and pilot work?

## Why It Matters

The previous restaurant-product runs created useful package, ROI, fulfilment, and pricing hypotheses, but the current mission requires a fresh commercial recalibration. Future product development, sales materials, ROI reports, pricing decisions, and pilot work need one current model that separates evidence-backed facts, planning assumptions, council decisions, and pilot-validation gaps.

## Allowed Scope

- Reassess historical restaurant categories, product categories, tiers, modules, bundles, delivery models, POS policy, bot policy, payment policy, hosting responsibility, setup fees, recurring fees, support allowances, custom-quote boundaries, ROI assumptions, provider economics, and sales claims.
- Use all completed historical council runs, revised historical claim ledgers, historical decision evidence maps, unresolved gap registers, authoritative evidence libraries, source/query ledgers, company memory, and prior ROI/package/pricing handoffs.
- Conduct bounded NotebookLM and public web research as explicitly requested by the human owner for this run.
- Decide current internal package/pricing/product/ROI/delivery recommendations under uncertainty, using evidence labels and pilot-validation gates.
- Produce internal strategy artifacts and operational decision models; public prices and polished sales copy remain out of scope.

## Excluded Scope

- Do not alter historical run files or silently rewrite prior verdicts.
- Do not write polished public sales copy.
- Do not make guaranteed ROI, aggregator-replacement, universal POS integration, or universal delivery-integration claims.
- Do not hide third-party pass-through costs.
- Do not import sources into NotebookLM, switch accounts, log in, perform paid research, submit forms, or bulk crawl.
- Do not treat repeated historical council opinion as external fact.
- Do not force every benefit into AED precision where only a qualitative or wide-range estimate is defensible.

## Decision-Status Map

{
  "restaurant_direct_ordering_business": "LOCKED",
  "aggregators_as_discovery_not_replacement": "LOCKED",
  "tier_0_real_ordering_page_historical_correction": "CURRENT_REVISABLE",
  "tier_1_to_tier_3_previous_structure": "OLD_HYPOTHESIS",
  "run_002B_packaging_verdict": "OLD_HYPOTHESIS",
  "run_002C_pricing_verdict": "OLD_HYPOTHESIS",
  "previous_roi_assumptions": "CURRENT_REVISABLE",
  "previous_delivery_posture": "CURRENT_REVISABLE",
  "public_sales_copy": "REJECTED",
  "guaranteed_roi_claims": "REJECTED",
  "aggregator_replacement_claims": "REJECTED",
  "universal_pos_or_delivery_integration": "REJECTED",
  "current_product_pricing_delivery_roi_model": "NEEDS_NEW_DECISION"
}

## Required Evidence

- V2 library: `codex-council-v2/library/EVIDENCE_LIBRARY.json` and `SOURCE_LEDGER.csv`.
- Historical audit: `working/evidence-audit-runs/2026-06-18-historical-evidence-audit-001-revision/`.
- Company memory: `handoffs/company-memory.md` and normalized handoffs under `handoffs/normalized/`.
- Historical council runs under `working/council-runs/`, especially Run 001, 002A, 002A-redo, 002B, and 002C.
- NotebookLM: minimum ten substantive queries, with at least two originated by each of the five executives and all four registered notebooks used at least once.
- Public web: minimum twenty substantive tasks, at least four originated by each executive; underlying pages must be opened and inspected, with source quality classified.
- Numerical estimates must be labeled as `VERIFIED_EXTERNAL_FACT`, `SUPPORTED_ESTIMATE`, `INTERNAL_PLANNING_ASSUMPTION`, `SCENARIO_VARIABLE`, `PROVISIONAL_COUNCIL_DECISION`, or `REQUIRES_PILOT_VALIDATION`.

## Role-Specific Starting Briefs

### Contrarian
Challenge optimistic migration, ROI, willingness-to-pay, conversion, delivery, support, and margin assumptions. Identify situations where incentives consume commission savings, the provider loses money despite restaurant value, the customer has no reason to switch, a smaller product is better, or the recommendation depends on fragile assumptions. Originate at least two NotebookLM questions and four web-research tasks.

### First-Principles
Rebuild the restaurant economics, delivery economics, product structure, pricing, and provider unit economics from underlying variables. Check formulas, causal dependencies, units, and double counting. Originate at least two NotebookLM questions and four web-research tasks.

### Expansionist
Identify all credible restaurant value paths and upside modules without double counting or false precision. Separate immediate measurable return, medium-term measurable return, operational return, strategic value, and plausible unquantified value. Originate at least two NotebookLM questions and four web-research tasks.

### Outsider
Compare the proposal against doing nothing, Google Business Profile, Instagram, WhatsApp, phone ordering, freelancers, WordPress, Wix, SaaS ordering platforms, POS products, agencies, and marketplace-only operation. Originate at least two NotebookLM questions and four web-research tasks.

### Executor
Turn the analysis into usable products, qualification rules, prices, delivery guidance, support allowances, responsibility limits, pilot design, and operational constraints. Originate at least two NotebookLM questions and four web-research tasks.

## Model-Routing Plan

{
  "economy": "manual fallback in current Codex session; use for metadata and validation",
  "frontier": "active Codex model from doctor output when available; reserve for Chairman and hard contradictions",
  "standard": "manual fallback in current Codex session; use for ordinary memos and reviews",
  "verified_environment": "Codex Doctor observed model gpt-5.5 on this workstation; per-agent model keys are not guaranteed by local TOML support."
}

## Machine-Readable Veto Assignments

```json
{
  "auditor": [
    {
      "protected_domain": "factual and numerical validity",
      "stage": "ANY"
    }
  ],
  "contrarian": [
    {
      "protected_domain": "unbounded downside claims",
      "stage": "PRE_CHAIR"
    }
  ],
  "executor": [
    {
      "protected_domain": "feasible next action",
      "stage": "PRE_CHAIR"
    },
    {
      "protected_domain": "feasible next action",
      "stage": "POST_CHAIR"
    }
  ]
}
```

## Stop Conditions

Stop on unresolved blocking fact checks, malformed tags, missing final verdict, illegal stage transition, failed old-system hash preservation, or skipped authorized veto holder.

## Output Contract

Produce the required V2 core outputs plus the following run artifacts under this run directory:

- `RESEARCH_AND_QUERY_LEDGER.csv`
- `CURRENT_EVIDENCE_PACK.md`
- `CURRENT_DECISION_REGISTER.md`
- `HISTORICAL_DECISION_SUPERSESSION_MAP.md`
- `RESTAURANT_NEED_READINESS_VALUE_MODEL.md`
- `RESTAURANT_CATEGORY_AND_SEGMENT_MODEL.md`
- `NUMERICAL_ASSUMPTION_LEDGER.csv`
- `FULL_RESTAURANT_VALUE_MAP.md`
- `MARKETPLACE_TO_DIRECT_ECONOMIC_MODEL.csv`
- `DELIVERY_FULFILMENT_DECISION_MODEL.csv`
- `RESTAURANT_ROI_CAUSAL_MODEL.md`
- `RESTAURANT_ROI_SCENARIOS.csv`
- `RESTAURANT_AFFORDABILITY_MODEL.csv`
- `PROVIDER_UNIT_ECONOMICS_MODEL.csv`
- `ALTERNATIVES_AND_COMPETITOR_COMPARISON.md`
- `REVISED_PRODUCT_CATEGORY_MODEL.md`
- `REVISED_PACKAGE_TIER_MODULE_MODEL.md`
- `REVISED_PRICING_MODEL.md`
- `PILOT_VALIDATION_PLAN.md`
- `EXECUTIVE_MEMOS.md`
- `ANONYMOUS_PEER_REVIEW.md`
- `EVIDENCE_AUDITOR_REVIEW.md`
- `DEVILS_ADVOCATE_ATTACK.md`
- `CHAIRMAN_FIRST_SYNTHESIS.md`
- `CHAIRMAN_PROVISIONAL_VERDICT.md`
- `CHAIRMAN_FINAL_COMMERCIAL_RECALIBRATION.md`
