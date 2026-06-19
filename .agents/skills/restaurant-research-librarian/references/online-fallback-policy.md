# Online Fallback Policy

Use online research to fill a narrow, decision-relevant gap after local material and the selected NotebookLM boundary fail to provide sufficient evidence, or immediately after a recorded NotebookLM connection/access failure. Online search is a fallback, not a default expansion of the research mission.

## Activation Test

Record a bounded gap statement before searching. It must include:

- the exact missing claim or variable;
- the decision blocked by the gap;
- what local caches, raw sources, and notebook boundary were checked;
- why the notebook result is absent, stale, unsupported, or insufficient;
- geography, date range, and acceptable evidence types;
- a small search budget and stop condition.

A recorded NotebookLM connection or access failure activates direct online fallback for the targeted request. Record the failed attempt in the NotebookLM query ledger, stop NotebookLM retries, and search public online sources without waiting for login or profile switching. This does not prove the notebook lacks the evidence; record the distinction and label the route `connection-failure fallback`.

## Source Priority

1. UAE government, regulator, official statistics, legislation, or primary public records.
2. Original research, methodology-bearing datasets, company filings, and official technical or commercial documentation.
3. Reputable industry or news sources that identify their evidence and dates.
4. Vendor pages, blogs, and marketplace listings only as vendor claims or discovery leads.

Prefer UAE evidence, then GCC evidence. Use global or generic SaaS evidence only when the limitation is explicit. For material commercial claims, seek two independent sources when practical. Do not treat repeated syndication of one source as corroboration.

## Search And Capture Rules

- Search for the bounded gap, not the entire commercial mission.
- Open and inspect the underlying page or document. Never cite a search-result snippet as evidence.
- Record source title, publisher, URL, publication date when available, retrieval date, geography, evidence type, supported claim, and limitation.
- Preserve a short paraphrase or compliant excerpt sufficient for later audit.
- Label vendor assertions as `Vendor claim`; label calculations and conclusions according to the evidence taxonomy.
- Separate absence of evidence from evidence of absence.
- Do not bypass paywalls, log in, submit forms, purchase reports, bulk crawl, or import sources into NotebookLM without explicit human approval.

## Default Budget And Stop Conditions

Unless the operator sets another limit, use at most:

- 3 targeted search queries per bounded gap;
- 5 opened candidate sources per bounded gap;
- 2 strong supporting sources for a material claim.

Stop when the gap is sufficiently answered, the budget is exhausted, sources materially contradict, or only weak/vendor evidence remains. Record the residual gap instead of stretching the conclusion.
