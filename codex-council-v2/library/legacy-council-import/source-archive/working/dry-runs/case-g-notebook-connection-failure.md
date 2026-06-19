# Case G Fixture: NotebookLM Connection Failure

**Question:** Find a current UAE primary source for a narrow, decision-relevant restaurant direct-channel requirement.

**Synthetic evidence:** Local caches and known raw sources are insufficient. The selected NotebookLM query attempt returns a connection error.

**Expected:** Librarian records the failed NotebookLM attempt, stops NotebookLM retries, and immediately plans narrow online fallback for the targeted request. It labels the route `connection-failure fallback` and does not claim that the notebook lacks the evidence. During this zero-query dry run, it does not execute NotebookLM or online queries.
