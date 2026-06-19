# Evidence Requests

## Request 1

**Question:** What evidence in the provider-viability notebook distinguishes a lightweight sellable restaurant direct-channel offer from a heavier operational service?

**Decision blocked:** Whether the existing notebooks contain usable boundary signals for a compact evidence pack.

**Smallest notebook set:** `d22b2ac2-8915-4108-b06c-2307a80db8ec` - UAE Restaurant Direct-Ordering Product-Market Fit.

**Why cache/raw-source read is insufficient:** Local evidence-pack and source-extract caches are empty; normalized handoffs contain only constraints and unresolved decisions.

**Targeted query text:** Using only sources already in this notebook, identify evidence that distinguishes a lightweight sellable restaurant direct-channel offer from a heavier operational service. Focus on onboarding, integrations, menu/catalog setup, payment/order handling, delivery/fulfilment involvement, ongoing support, maintenance, customization, and provider repeatability. Return a compact table with: boundary signal, what makes it lightweight or heavy, evidence classification (verified fact, estimate, vendor claim, assumption, inference, contradiction, or unresolved gap), geography, source title, and precise citation. Do not recommend prices, packages, sales claims, or a commercial verdict. Explicitly state gaps.

**Estimated query cost:** `1`

**Approval required:** no; the operator explicitly authorized this live smoke test and limited it to the primary account.

**Stop condition:** Stop after one query if it supplies enough cited boundary evidence for a compact pack; otherwise consider one targeted competitor-notebook query. Never exceed five total queries.

**Outcome:** Query attempted once and failed with `PERMISSION_DENIED`. No answer or citations were returned. Further queries stopped because this is an account/access blocker, not a notebook-selection gap.

**Human review required:** Confirm the manually selected primary account can access the four registered notebook IDs. Any login or profile switch requires separate explicit approval before a future retry.
