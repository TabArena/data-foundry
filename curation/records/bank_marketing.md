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
tags:
- Non-IID (Temporal)
original_source: UCI
year: '2012'
required_split:
- Temporal (NON-IID)
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

CC (2026-11-08, Lennart): record field `year` set to the definition's 2012 (UCI's release, donated 2012-02-13), from 2011 (the ESM paper, which only analysed the data); the field row of the folder's REVIEW.md, `update`.

CC (2026-11-08, Lennart): issue 3 of the folder's REVIEW.md, as implemented (ok): the 274 exact copies stay, with a note (LEAK-16, LEAK-18): 274 exact copies (0.6%, label included) and 32 feature-copies with the other label; 93% of the copy rows have a balance of 0, plausible repeats of common profiles; under the random split 0.9% of the test rows have a copy of every feature in training, 0.8% one with the same label.

CC (2026-11-08, Lennart): the declared metric (`roc_auc`) is checked, as declared on the PR #47 review board.

CC (2026-11-08, Lennart): issue 1 of the folder's REVIEW.md, reply (a) to the consistency check, "Split by time (the issue's A)": the split is by time on the file's date order, five expanding windows of 4,521 records at the 50% floor (training on 50% to 90% of the records), keyed by the record's position in the file once `_clean` has rebuilt the year and checked the dates against the order; `required_split` set to `Temporal (NON-IID)`, with the tag `Non-IID (Temporal)`. Supersedes Lennart's keep of the random split under SPLIT-31 (its Cases row since 2026-10-20: "IID kept: optimistic, but it matches how the task is framed") and his comment above, "We can likely ignore the time impact".

CC (2026-11-08, Lennart): issue 2 of the folder's REVIEW.md, reply (a) to the answer, "A: before the campaign, drop campaign": the prediction point is before the campaign's first call, so `campaign` (this campaign's calls, the last included) is dropped under LEAK-10, as heart_failure_followup_survival's `time`; the inputs are twelve and the time key. Supersedes Lennart's keep of `campaign` with a note of 2026-11-06 (the LEAK-10 Cases row on spans the outcome sets).

**Assessment (AI, 2026-11-08):** on the five time windows, newest first (the last contact from 2009-08 to 2010-11, 2009-05 to 2009-08, 2009-04 to 2009-05, 2008-11 to 2009-04 and 2008-08 to 2008-11; 47.1%, 16.1%, 13.1%, 10.5% and 6.2% subscribed), LightGBM (3 seeds, early stopping on the newest tenth of the training side) scores ROC AUC 0.570, 0.679, 0.605, 0.552 and 0.522 (mean 0.586; seed SD 0.029 per window) and logistic regression 0.633, 0.701, 0.640, 0.603 and 0.490 (mean 0.614), against 0.76 on the random split. Task probes: random forest 0.631, linear 0.613, LightGBM 0.610, the best family above the dummy on 5 of 5 windows, flag `no_spread` (random forest against LightGBM +0.043, paired SE 0.022; the BeyondArena tuned results ran on the random split). On the windows `campaign` adds +0.0065 to logistic regression (higher in 5 of 5) and -0.014 to LightGBM (higher in 1 of 5); the month of the last call as a category -0.0096 and -0.0019 (higher in 1 of 5 each; REVIEW.md issue 4); the time key +0.018 and +0.004. In the newest window 703 test records (15.6%) have the same client's later record in that window, whose `poutcome` says "success" for 419 of them, all subscribers (19.7% of the window's positives): a protocol line (LEAK-9). Without `campaign`, 811 records copy another on the twelve inputs, label included (274 with it), and 82 with the other label; 89% of the copy rows have a balance of 0. Leak probes: no input alone above ROC AUC 0.582 (`poutcome`); the subscription rate of the newest periods rises, which is drift, not a cut-off.

CC (2026-11-08, Lennart): issue 4, A (as implemented): the month of the last call stays out of the inputs, with the day: every input exists before the first call, and the period is in the time key (on the windows the month adds nothing: -0.0096 for LightGBM, -0.0019 for logistic regression).

CC (2026-11-08, Lennart, in chat): the protocol line for the newest window's recurring clients (703 test records whose later record in the same window gives the label away; no use of other test rows) is enough ("that sounds valid to me"); the five windows stay as they are.

## Reference

S. Moro, R. Laureano and P. Cortez. Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. In P. Novais et al. (Eds.), Proceedings of the European Simulation and Modelling Conference - ESM'2011, pp. 117-121, Guimarães, Portugal, October, 2011. EUROSIS.
