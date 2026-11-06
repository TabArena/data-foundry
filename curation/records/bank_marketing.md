---
unique_name: bank_marketing
name: bank-marketing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
original_source: UCI
year: '2011'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1461
- https://doi.org/10.24432/C5K306
notebook_path: datasets/beyond_iid/old_iid/bank_marketing/bank_marketing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/bank_marketing/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

predict if the client will subscribe a term deposit. Might actually require temporal split - but as features seem to be time-invariant the task should be fine

Potential issue: preprocssed date features

Lennart: We can likely ignore the time impact but might need to restore the date features

Andrej: Fits criteria

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (with ALIFT second) in Moro, Cortez & Rita 2014, Decision Support Systems 62:22-31.

CC (2026-10-30, Lennart): `campaign` and `previous` are counts and stay numeric, as the UCI description gives them ("number of contacts performed during this campaign", "... before this campaign"); the BeyondArena notebook had typed them categorical (issue #34, raised by Adrian). CLEAN-14: a count stays numeric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `education` (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `education` (CLEAN-10).

**Assessment (AI, 2026-11-06):** supersedes the comment "features seem to be time-invariant" (a later measurement, EV-2): with the year rebuilt from the file's date order (UCI: "ordered by date"), the subscription rate is 5.1% in 2008 (27,729 rows), 17.1% in 2009 (14,862) and 51.6% in 2010 (2,620); `contact` "unknown" covers all 12,443 rows of May-June 2008; the mean number of calls per client falls from 3.19 to 2.13 to 1.89. Year: the data were first published by the UCI release (donated 2012-02-13), so the definition's 2012 is the year (PROV-9); the record's 2011 is the ESM paper, which only analysed them.

**Assessment (AI, 2026-11-06):** review panel (focused, re-review under LEAK-41, MET-14 to MET-16): ship after changes, those needing no decision applied (notes on `campaign`, `contact`, `pdays` and `balance`, `job` "unknown" as missing, the row text, the `pdays` sentinel accepted); new: clients recur across campaigns, and the random split lets a client's later row give away its earlier row's label through `poutcome` (3.7% of test rows, +0.020 ROC AUC to a model that matches them; LEAK-17), while the source evaluates in time on date-ordered data; disputed: keep or drop `campaign`, which turns on the prediction point (issue 2); for the curator: issues 1 (split by time, against the SPLIT-31 call), 2 (the prediction point and `campaign`), 3 (duplicates).

**Assessment (AI, 2026-11-06):** priority 2 (selection.md, Priority): a good shape (45,211 units, 13 features, categorical and ordinal) +, a strong source (UCI and Moro et al. 2014) +; no gap in the benchmark; the use case's fit is open (issue 2: before the campaign or at a call); a known risk -, the open issues on the split (1) and on `campaign` (2).

## Reference

S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimarães, Portugal, October, 2011. EUROSIS.
