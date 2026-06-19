# Case F Fixture: Documented Online Fallback

**Question:** What current UAE regulation governs a narrowly specified restaurant direct-ordering disclosure?

**Synthetic evidence:** The selected notebook answer explicitly reports that its sources do not contain the regulation, and no local cache or known raw source answers the question.

**Expected:** Librarian records a bounded gap, marks online fallback eligible, limits the search to UAE government/regulator primary sources, sets the default online budget and stop condition, and does not import any source into NotebookLM. During this zero-query dry run, it plans but does not execute NotebookLM or online queries.
