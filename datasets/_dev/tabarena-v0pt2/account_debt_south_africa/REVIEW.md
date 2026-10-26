# account_debt_south_africa

**Outcome:** added. Verdict: ship; the panel's changes are in `dataset.py` (not built yet). Validity: the label-rule
columns and the payment totals stay dropped (LEAK-10); the unrecorded stretches of the file are dropped by one
run-level rule (LEAK-25, a reading for the curator); the billing totals of the label window are kept on a measured
fact (LEAK-10, a reading for the curator); `TotalElectricityBill` is kept as a potential leak (LEAK-10 against
LEAK-6, for the curator); the task text says it predicts a status at the extract (USE-5, USE-8, fit approximate); the
random split (IID) is forced because the file has no dates, with its cost written down (SPLIT-8). Value: the task is
not trivial (TP): ROC AUC 0.874 against 0.787 for the best single feature, 101,686 rows. Quality: placeholders set to
missing (CLEAN-10/11); 6.2% duplicate rows kept (LEAK-18). Weighed: a rare real public-finance task and its size,
against the approximate fit and the missing municipality key. Left for the curator: issues 1, 8 and 9.

**Main points:** Keep the billing totals of the label window through a LEAK-10 amendment (issue 9)? Settled on 2026-10-26: the
unrecorded runs dropped, `TotalElectricityBill` kept with its note (issues 1 and 8).

**Record judgment:** valid with concerns. Eight municipalities' billing accounts summarised over two years by the
uploader (Kaggle owner dmsconsultingsa; named DMS Technologies in the bibtex); the label is mostly arrears older than
the window, so the task is the status at the extract, a stand-in for the data card's forecast.

**Issues for Lennart:**

9. **Keep the billing totals of the label window?** `TotalBilling` and `AverageBilling` sum the two years at whose
   end the label is read. If billing moved with the debt (interest or penalties on arrears billed in the window), a
   model would read part of the label from it. LEAK-10 (Must) lists a feature computed from the window that defines
   the target as out "even when known at snapshot time", and mutual_funds_india (`rating`, dropped) and iranian_churn
   (retired) were decided that way. What sets this case apart, measured: billing is set by tariff and property, not
   by the holder's behaviour. Within file blocks of 2,500 rows and property-value bins, the billing left over once
   block and property value are accounted for (the residual) separates the classes at ROC AUC 0.509 (total), 0.501
   (per billing line) and 0.496 (number of lines), that is not at all, unlike iranian_churn's usage, which fell in
   the churn month. Implemented: kept, with a note in `dataset.py` (ROC AUC 0.874). Alternative: drop them, which
   leaves the static profile (category, property value and size, `HasIDNo`) at 0.832, or amend LEAK-10. Advocate and
   critic agree on the keep. Recommendation: keep and record a LEAK-10 Cases row: a window sum that the data shows
   does not move with the outcome stays.
   Decision needed: the Cases row, an amendment of LEAK-10, or the drop.

   **Lennart (2026-10-26, ok):** keep

   **Consistency check (AI, 2026-10-26):** the keep follows the facts (the billing left over once municipality and property
   value are accounted for separates the classes at ROC AUC 0.509 / 0.501 / 0.496, unlike mutual_funds_india's
   `rating` and iranian_churn's usage), but LEAK-10 is a Must that puts a sum over the label's window out "even when
   known at snapshot time", with no clause for "the data shows it does not move with the outcome". A Cases row cannot
   carry a Must's departure, so the keep needs a short amendment of that clause, for example: "unless the data shows
   the window's values do not move with the outcome, given the covariates known at the prediction point". It would sit
   next to LEAK-10's existing "did not change" clause for lookups, and should be worded together with
   onlinenewspopularity's issue 5 (the values read at a later pull), whose check asks the same question. Adopt this
   amendment (then I add the Cases row and the keep stands), or drop the two columns (ROC AUC 0.874 to 0.832)?

**Review panel:** ship after changes (mediator). Claim audit: 41 claims; the task text ("turned into bad debt") and
the electricity note refuted in part (both fixed), a 186-row unrecorded run found (dropped), the record's quote
untested. Blind review: would include with changes; main concern the label window shared with the billing features.
Debate: agreed on the task rewording, the billing keep, the cost line and the placeholders; disputed:
`TotalElectricityBill` (issue 8, left to the curator) and the form of the run drop (settled by the mediator's
experiment: one run-level rule, issue 1).

<details><summary>Claim audit</summary>

Method: a raw recount; the definition frame and splits; LightGBM tests (default parameters), curated rows aligned
back to their file position by replaying `_clean` + `content_order` + the seed-42 shuffle and asserting equality; the
OpenML 43838 copy downloaded and compared; Kaggle metadata read via the public API (`currentVersionNumber` 1,
`lastUpdated` 2020-06-04, 13,118,848 bytes). Licence never weighed (EV-4).

Model note: default LightGBM on split 0/0 gives 0.870 where the notes say 0.874 (other hyperparameters); every
with/without difference below has the same sign and a similar size, so the AUC claims are read as holding.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "Has a municipal billing account turned into bad debt?" | D task_summary | Compare 90+ debt + write-off to what the two-year window could create | **refuted (framing)** | Of 57,199 curated bad debts, 83.7% hold more 90+ debt + write-off than the window's net arrears (billing - receipts), 69.1% more than the whole two-year billing; 16.9% paid >= 87.5% of their window billing. The label mostly marks debt that already existed before the window, not an account that turned bad over it. | USE-5, USE-3 (P3) |
| 2 | Use case: forecast how many / how much will turn bad | D | data card | holds as the source's aim; not what the label measures (see 1, 9) | Kaggle card: "forecast the number (and value) of accounts that are at risk of developing into a Bad Debt" | USE-1 |
| 3 | Row = one account, summarised over two years | D | data card; implied bill count | holds | Card: "over a 2 year period"; TotalBilling/AverageBilling median 48 lines (all services), max 200 | PROV |
| 4 | Status at the end of the two years; 56% | D | count | holds (56.1%); "at the end of those two years" is unsupported by the card, which says only "resulted in a Bad Debt" | 57,199 / 101,871 | USE-5 |
| 5 | Known: category, property, ID, billing, not payments | D | columns of the frame | holds | 7 features: AccCategory, PropertyValue, PropertySize, TotalBilling, AverageBilling, TotalElectricityBill, HasIDNo | LEAK-1 |
| 6 | Random accounts, same municipalities, same time | D | splits | holds | 3x3, 67,914/33,957, positive rate 0.5615 in every fold, no index overlap | SPLIT-1 |
| 7 | Changes listed | D | code read + counts | holds | see 18-23 | writing |
| 8-9 | fit approximate; status at the extract stands in for the forecast | D | see 1 | holds as stated, but understates the gap: the label is mostly pre-window debt, so the task is detecting a standing arrears status from the bill profile | 83.7% / 69.1% above | USE-8 |
| 10 | year 2020, Kaggle, source_url | D | Kaggle API | holds | lastUpdated 2020-06-04, owner dmsconsultingsa | PROV-1 |
| 11 | v1 only, 4 June 2020, 138,509 rows, md5 | D | md5sum, API | holds | md5 d5fa5aaf...; 138,509 rows; currentVersionNumber 1; 13,118,848 bytes = local file | PROV |
| 12 | OpenML 43838 = same rows, same order | D | download parquet, compare column by column in order | holds | 138,509 x 16, all 16 columns equal in order | PROV-6 |
| 13 | bibtex Rawlins 2020, DMS Technologies | D | Kaggle API | holds (creator Dylan Rawlins); "DMS Technologies" not on the card (owner ref dmsconsultingsa) | | writing |
| 14 | Seven runs 1,185-8,762; longest other run 334 rows, paying | D comment | runs recount | holds | 8,762/5,320/4,428/2,948/2,781/2,514/1,185; next 334 (99.4% paid), 218 (99.1% paid), 186 | |
| 15 | binary, roc_auc, IID, 3x3 stratified | D/README | splits | holds | as 6 | |
| 16 | 138,509 accounts, eight municipalities, v1 | D cc | count; card | holds | | |
| 17 | Prediction point at the extract | D cc | see 1 | holds as written; see 1 for what the label is | | USE-3 |
| 18 | Debt columns set the label | D cc | crosstab | holds | debt -> 63,600 bad / 0 not; no debt -> 74,538 not / 371 bad | LEAK-1 |
| 19 | 27,938 rows (20.2%); never-payers inside 0% bad vs 91.5% | D cc | recount | holds | 27,938 (20.17%); 0 of 11,984 vs 91.53% of 40,984 | PROV-13 |
| 20 | 186-row run from 91,971 stays; lower threshold drops 218/334 | D cc | recount | holds | 185 curated rows, 0 bad, HasIDNo = 1 in all, 98.4% billed never-paid: it looks like the dropped runs (debt unrecorded) and stays labelled No | PROV-13 |
| 21 | 8,700 dropped (no net billing / debt predates window / negative payments) | D cc | recount | numbers hold; the reason "whose debt predates the window" does not separate them: 83.7% of the kept bad debts also have debt beyond the window's arrears | 903 zero, 7,722 net credit, 121 negative pay; 77.8% bad | writing |
| 22 | Payments dropped; 0.952 with, 0.874 without | D cc | LightGBM split 0/0 | holds | 0.949 vs 0.870 | LEAK-10 |
| 23 | category encodings duplicate; 0 -> missing | D cc | 1:1 check; zeros | holds | each encoding maps 1:1; 0 zeros left; 8.8% / 8.7% missing | CLEAN |
| 24 | Elec: signal mostly whether billed; same share of bill by class (median 0.33); cut-offs leave no trace; 0.874 vs 0.865 | D cc, R CC 2026-10-12 | share by class; AUC of the share; model with a 0/1 flag | **refuted (part)** | medians 0.353 (not bad) vs 0.301 (bad), pooled 0.338; the share alone separates the classes among billed accounts at AUC 0.562 (lower share for bad debts, the direction a cut-off would leave). "Mostly whether billed" holds: 0.870 with, 0.860 without, 0.868 with only a billed flag | LEAK-11 (Should, weak) |
| 25 | HasIDNo: 64% vs 47%; 0.874 vs 0.872 | D cc | rates; model | holds | 64.2% vs 46.5%; 0.870 vs 0.8675 | LEAK-11 |
| 26 | 6,355 duplicates (6.2%); 0.874 -> 0.867 without copied test rows | D cc | duplicated(); model | holds | 6,355 (6.24%); 8.1% of test rows have a feature copy in train (7.9-8.1% over the 9 splits); 0.870 -> 0.864 | LEAK-16 |
| 27 | Unknown run rows 134,192-138,276, 2,396 curated, mostly 1-3 bills, 53% vs 86% | D cc | runs of the category | holds ("mostly" = 56%) | run 134,192-138,276 (4,085 rows), 2,396 curated; 53.4% of 1,102 vs 85.9% of 4,020. Note an adjacent Unknown run 133,853-134,185 (the paying 334-row run) | |
| 28 | IID forced, one extract without dates | D cc | file columns | holds | no date column | SPLIT, USE-10 |
| 29 | 0.877 random -> 0.843 blocks of 2,500 -> 0.786 thirds | D cc, R CC | GroupKFold on file position | holds | 0.870 / 0.842 / 0.788 | SPLIT-4 |
| 30 | no splits_comment | D | read | holds | | |
| 31 | 162 accounts billed R6 in six R1 lines | D warning | groupby dropna=False | holds | largest group 162 (Unknown, no property, R6/avg 1, bad); 203 such accounts in all | LEAK-16 |
| 32 | 371 exceptions; uploader drops the columns | D decisions | crosstab | holds (371; 321 of them in the curated rows) | | |
| 33 | 91.5% -> 14.7% | D decisions | bands | holds | 0.915 (41,081) / 0.147 (28,918) | |
| 34 | runs: no never-payer bad; rows from 0 | D decisions | as 19 | holds | | |
| 35 | Quote "about 20 million records ... PostgreSQL" | R | Kaggle description via API | **untested / not found** | neither "million" nor "PostgreSQL" is in the current Kaggle description; may come from the column metadata or the notebook | EV-2 |
| 36 | DMS / Rawlins, 8 municipalities, OpenML same | R | API, parquet | holds | | |
| 37 | as 19, 22; 89.6% for paid at most half | R | bands | holds (0.896 of 6,631) | | |
| 38 | OpenML ships the debt columns with baddebt | R | parquet columns | holds | all 16 columns present | LEAK-1 |
| 39 | CC 2026-10-12: elec "same share (median 0.33)" | R | as 24 | **refuted (part)** | as 24 | LEAK-11 |
| 40-41 | priority, front matter | R | not testable on data | untested (judgment / metadata) | | |

**Claims nobody wrote down**

| Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| The target is the real-world target (an account becoming bad debt over the window) | as 1 | **refuted** | 69.1% of bad debts carry more 90+ debt than the window's whole billing: the status is mostly inherited; the actor already knows it from the age analysis at the extract | USE-5 (Must, P3) |
| Every feature is known at the prediction point | elec share; ID | holds with notes | elec share carries a small cut-off trace (24); ID possibly captured in collection (25) | LEAK-11 |
| The split is the one the use case needs | blocks | holds for "a municipality scores its own accounts" | random 0.870 vs municipality-like blocks 0.842 / thirds 0.788 | SPLIT-4 |
| No row is a copy across the split | key match | holds as an accepted, documented warning | 8.1% of test rows with a train copy, 0.006 AUC | LEAK-16 |
| The kept rows record debt | 186-row run | **refuted (small)** | 185 kept rows of billed never-payers with ID numbers, none bad: the same signature as the dropped runs | PROV-13 |

**Ranked**

Refuted:
1. Claims 1 / 4 / 8-9 and the implied real-world target (P3, USE-5): the label is mostly pre-existing arrears
   (83.7% above the window's net arrears, 69.1% above its billing), not "turned into bad debt" over the window. Changes
   the task statement and the fit reason; mildest remedy: rewrite `question`, `predicted` and `fit_reason` ("is
   currently in 90+ arrears or written off") and keep `fit="approximate"`; the curator weighs whether such a status
   task is still a use case (the municipality reads it from its age analysis).
2. Claims 24 / 39 (P4, LEAK-11, weak): "the same share of the bill (median 0.33)" and "cut-offs leave no trace" are
   false: 0.353 vs 0.301, share AUC 0.562 in the cut-off direction. Model effect ~0.002 beyond a billed flag. Mildest
   remedy: correct the note and CC; optionally replace the column by a 0/1 "electricity billed" flag (0.868).
3. Claim 21 reason (writing): "debt predates the window" does not set the 8,700 apart; reword to what the filter does.
4. Implied (PROV-13, small): the 186-row run looks unrecorded too; drop it by its signature or note it as such.

Untested: 35 (quote not in the Kaggle description), 40-41 (judgment and metadata).

</details>

<details><summary>Column audit</summary>

Frame: rebuilt from the definition through `dataset_io.load(..., built=True)` (no build record path, so `rebuilt`):
101,871 rows x 8 columns. Codebook: the Kaggle data card "Content" (as copied in the OpenML 43838 description).
Prediction point (curation_comments bullet 1): the account at the extract date; billing of the two years before; the
label is the bad-debt status then. "Block" below = 2,500 consecutive rows of the raw file, a stand-in for the
municipality, which has no column (the curated rows keep their raw index).

**Column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| AccCategory | "A classification of the type of account" (12 levels) | yes, static | category; `accountcategoryid`, `acccatabbr` dropped as exact 1:1 copies (checked both ways) | fine; minor question: `Unknown` (7,217 rows, 69% bad, mostly the file-end run) is a proxy-missing level that also marks a segment; keep and say why | CLEAN-5, CLEAN-10 |
| PropertyValue | "market value of the property" | yes (valuation roll) | float; 0 -> NaN (8.8%); 25 rows of exactly 1 (a placeholder, 40% bad) stay | fine; cheap fix: values of 1 to missing | CLEAN-10, CLEAN-11 |
| PropertySize | "size of the property in square metres" | yes | float; 0 -> NaN (8.7%); max 270M m2 are Agricultural farms (plausible); 2 rows of 1 | fine | CLEAN-11 |
| TotalBilling | "total amount billed ... for all services", two-year window ending at the label | value exists at the extract; window ends at the outcome | int; cohort filter `> 0` (uploader) | fine, documented in fit_reason. Measured: within block x property-value bin (Residential) the billing residual separates classes at AUC 0.509, so no outcome-dependent part (interest on arrears, credit notes) shows | LEAK-10 (window clause) checked, USE-8 |
| AverageBilling | "average amount billed" per billing line, same window | as TotalBilling | int, rounded at source: 2,594 rows of 0 with positive total; Total/Average = implied lines 1-200 | fine; residual AUC 0.501 (avg), 0.496 (implied number of lines) | LEAK-10 checked, CLEAN-14 |
| TotalElectricityBill | "total billed for electricity"; "put in place because it is used as a means to recover debt" (cut-off) | the value exists at the extract, but a cut-off or prepaid conversion is a consequence of arrears | int; 59 negatives, 652 rows above TotalBilling (net credits; unusual, not impossible; keep) | potential leak, kept on purpose; the note's premise is partly refuted (below) | LEAK-10, LEAK-6, LEAK-11 |
| HasIDNo | holder has an ID number; "useful in legal proceedings"; "often not captured" | probably; may be captured during collection | int64 0/1 (binary, fine as numeric) | potential leak, kept with note: holds. Residential within-block AUC 0.529 (35 blocks, 0.42-0.63) | LEAK-10, LEAK-6 |
| BadDebt (target) | "1 = considered to be a Bad Debt"; a rule of 90+ debt or write-off | label | category Yes/No, 56.1% Yes | fine | CLEAN-15 |
| dropped: total90debt, totalwriteoff, debtbillingratio | the debt that sets the label | parts of the target | dropped | correct | LEAK-10 |
| dropped: totalreceipting, avgreceipting, collectionratio | payments of the label window | window ends at the outcome; arrears = billing - payments | dropped (0.952 -> 0.874) | correct | LEAK-10 (mutual_funds_india) |

**Problems, ranked (principles.md)**

1. **P4, LEAK-10 / LEAK-6 (weighing call for the curator): `TotalElectricityBill` carries a within-municipality signal
   that the kept-on-purpose note and the CC of 2026-10-12 say is absent.** The note argues the signal is "mostly whether
   the municipality bills electricity at all". In blocks where 80%+ of accounts are billed for electricity, the
   accounts billed none are bad debts at 38.6% against 19.2% (1,791 vs 10,134 rows); in 50-80% blocks 54.5% vs 35.7%;
   Residential in blocks >= 50%: 54.3% vs 27.0%. Within-block AUC of "no electricity billed" alone: 0.588 (12 blocks).
   Those accounts never paid anything 33.3% of the time, against 6.2%, and are bad more often even at equal payment
   status (paid something: 32.2% vs 23.3%; never paid: 88.7% vs 77.4%). This is what the data card's mechanism
   predicts (a cut-off, or a prepaid conversion, for the whole window), but vacant or unconnected properties would look
   the same: circumstantial, not proof (EV-6). The share-of-bill argument does hold where it applies: among billed
   accounts in electricity blocks the median share is 0.334 for both classes (the claim auditor's 0.353 vs 0.301 comes
   from pooling municipalities). Effect of the column: ROC AUC 0.874 -> 0.865 (note). Mildest remedy: keep it, rewrite
   the note with the within-block numbers and ask the curator whether the CC still holds; alternative: drop it (LEAK-10)
   if a zero electricity bill is read as a cut-off.
2. **P4, LEAK-10 window clause (checked, holds as documented): the billing columns sum the window that ends at the
   label.** Billing is set by tariffs and consumption, not by payment behaviour, as far as the data shows: residuals of
   log TotalBilling, log AverageBilling and the implied number of billing lines within block x property-value bin give
   AUC 0.509 / 0.501 / 0.496. No action beyond the existing `fit="approximate"` reason.
3. **P4, LEAK-10 (holds): `HasIDNo`.** Within-block Residential AUC 0.529; among Residential payers 40.0% bad with an ID
   vs 24.9% without. Consistent with the note (0.874 vs 0.872). Keep with the note.
4. **P4/P5, row selection on the label's own columns (not a column; for the split and claim auditors):** the no-debt
   run filter reads `total90debt`/`totalwriteoff` in file order; its fairness is LEAK-25 territory (issue 1 of the
   REVIEW), not a column problem.
5. **P7, CLEAN-10 / CLEAN-11 (cheap):** `PropertyValue` = 1 in 25 rows and `PropertySize` <= 10 in 5 rows look like
   placeholders; set to missing with the 0s, or leave with a line. `AccCategory = Unknown` is a proxy-missing level
   tied to the file-end segment; keeping it as a level is defensible (it carries the segment), say so.
6. **P7, CLEAN-14 (note only):** `AverageBilling` is rounded to whole rand at source (2,594 zeros with a positive
   total); `TotalElectricityBill` has 59 negative and 652 above-total values (net credits). No change.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** IID, 3 repeats x 3 stratified folds (67,914 / 33,957 rows, 56.1-56.2% positive in every
test fold, no train/test index overlap), tagged `ForcedIIDFromTemporal`. It is the applied precedent of SPLIT-8
(Lennart, 2026-10-12), and the numbers behind it reproduce.

Model: LightGBM (300 trees, lr 0.05,
63 leaves, 2 threads) on the frame from `_clean` in raw file order (the container shuffles rows with seed 42, so its
order is not the file order; the frame from `_clean` has the same 101,871 rows).

**Regime against the use case (SPLIT-1, SPLIT-4, SPLIT-8, USE-10)**

* Use case: a municipality scores its own accounts. The entity is known (the same accounts at the next extract), and so
  is the municipality. The faithful split would be temporal on the same accounts, with the previous status as a
  feature (USE-10). The file is one extract with no date and no account id, so that split cannot be built. SPLIT-8
  applies: IID, forced, tagged, and `fit="approximate"` names the gap. The task_summary `split` text ("Random accounts
  of the same municipalities at the same time") is accurate.
* Temporal checks (time column, windows, gap against the label delay, training rows with an unknown label, history,
  season): not applicable. There is no time axis. The label is a status at the extract, not a delayed outcome.
* Grouped alternative: the eight municipalities have no column (`accountcategoryid` is a global category code from 1 to
  13 shared by every part of the file, not a municipality code). File position is the only trace, and it is strong:
  per 5,000-row block the bad-debt rate runs from 0.000 to 0.968, `HasIDNo` from 0.000 (blocks 6-12) to 0.87, and the
  share billed for electricity from 0.00 to 0.87.

**Alternative splits (run because the municipality structure raised doubt)**

| split | ROC AUC per fold | mean |
|---|---|---|
| random stratified 3-fold (as shipped) | 0.873 / 0.879 / 0.878 | 0.877 |
| file blocks of 500 rows, round-robin to 3 folds | 0.864 / 0.871 / 0.861 | 0.865 |
| file blocks of 2,500 rows | 0.822 / 0.864 / 0.861 | 0.849 |
| file blocks of 10,000 rows | 0.755 / 0.850 / 0.873 | 0.826 |
| thirds of the file | 0.789 / 0.791 / 0.782 | 0.787 |
| random + file position as a feature | 0.890 / 0.893 / 0.893 | 0.892 |

The note's 0.877 -> 0.843 / 0.786 reproduces (0.849 / 0.787 here). The drop measures a new municipality, which the use
case does not need: a municipality scores its own accounts. Under SPLIT-4 a gap alone never decides, so a grouped split
on file blocks would also be a guess (SPLIT-24). The random split is the right one.

**Problems, ranked (principles.md: validity P4 first, then notes)**

1. **P4, note: the municipality is known in deployment but missing from the features (SPLIT-4, SPLIT-24, SPLIT-31).**
   Adding file position, a stand-in for the municipality, raises random-split ROC AUC from 0.877 to 0.892. The
   shipped task therefore under-informs the model about a fact the actor has, and lets it rebuild that fact from
   feature combinations (`HasIDNo` = 0 blocks, electricity billed or not). This is not a split error: IID is the
   regime the use case implies. Mildest remedy: none in the split. Write it down in the notes as the SPLIT-8 cost
   ("what the timestamp and the municipality key would change"), and ask the uploader (DMS Technologies) for the
   municipality key, which would be a feature, not a group. Do not construct it from file blocks (a guess, SPLIT-24).
   The container's seed-42 shuffle drops the file order, so a later variant needs the raw file.
2. **P4, note: copies across the split (LEAK-16 to LEAK-21, SPLIT-29).** In my random folds 7.9-8.1% of test rows have
   an exact feature copy in train (the leak probe reports 7.3% on the shipped split). The train majority label of a
   copy matches the test label for 87.6-88.1% of them. AUC drops from 0.873-0.879 on all test rows to 0.867-0.872
   without the copied rows. Of the 2,327 duplicate groups, 91.1% span fewer than 2,500 file rows (median 36), so the
   copies sit within one municipality. That fits flat charges or shared property records, not a shared entity that new
   data would lack. The hidden-group probe has no hits (top `TotalBilling` +0.020, composite key +0.008, 0.0% near
   copies). Kept with an accepted warning. No remedy needed.
3. **P3/P4, note: snapshot instead of forecast (SPLIT-8, USE-10).** Train and test share the extract date, and the
   features cover the two years at whose end the label is read. A real forecast would score accounts at a later
   extract. This is declared (`fit="approximate"`, `ForcedIIDFromTemporal`). Remedy: recover dates if a later release
   has them.

No wrong split, no re-split, no gap needed.

</details>

<details><summary>Domain practitioner</summary>

Actor: the revenue manager / CFO of a South African local municipality. Two decisions use such a score: (a) the
year-end impairment of consumer debtors under GRAP 104 (the allowance for accounts not expected to be recovered,
grouped by category and payment history, with 90 days of non-payment as the impairment indicator), and (b) the
credit-control plan (which accounts get final demands, electricity cut-off, hand-over to collectors). Prediction
point I would actually use: an account at the year-end extract, scored for whether it will be (or become) a bad debt
over the next period.

**Fit: approximate (confirmed, USE-8)**

The label is the account's status at the same extract that closes the two-year window its features summarise, so the
model classifies the current state from the static profile and the billing pattern instead of forecasting the next
period; the one-snapshot stand-in for a forecast is exactly the USE-8 case listed for this dataset. USE-9 gives no
direct alternative: the only use case where these features are known and the label is not (a municipality whose age
analysis is unreliable estimating which accounts are in arrears) is a rephrasing to excuse the gap (weighed factor
against), and a new municipality without history would need a grouped split on a municipality key the file lacks.

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, legitimately: account category, property market value and size (valuation roll), whether an ID number is on
file, the billing over the past two years (total, per bill, electricity). `TotalElectricityBill` = 0 for 69% of the
curated accounts (bad-debt rate 66% against 33% with electricity billed): to me that marks an area where the
municipality does not sell electricity or the meter is prepaid, i.e. I lack the cut-off lever. That is known up front
and a legitimate input (USE-6), consistent with keeping it.

Would not have at a true forecast point: nothing among the shipped features beyond the window overlap itself
(features end at the label date, USE-3). `HasIDNo` is a holder property per the data card, but capture during
collection is plausible; its effect is small (0.002 AUC), keeping it is acceptable as a named potential leak (USE-8).

Missing that I would always have: (1) the debtors' age analysis and payment history of the period before the
prediction point, by far my strongest inputs (they were dropped correctly here only because the file's payment
window coincides with the label window, LEAK-10 via USE-3); (2) which municipality / ward; (3) indigent registration
(free basic services, written-off charges); (4) prepaid vs conventional meter; (5) owner vs tenant, account age.
Their absence makes the task harder and different, not wrong.

**2. Target (USE-5)**

What I act on: the probability that an account is not recovered (for the allowance, weighted by the amount) and,
for collection, the probability that a currently paying account slips into 90+ days. The shipped label is a binary
"any debt aged 90+ days or any write-off" at the extract, regardless of amount: R1 of 90-day arrears counts like
R100,000. 56% of accounts are positive, typical of struggling municipalities. A probability is the right output and
ROC AUC is acceptable for prioritisation; for the impairment I would want calibrated probabilities and the amount.
It is a proxy close to what I act on, not the exact target. The use_case text says "how many, and how much"; the
"how much" is not predicted, so the wording slightly overstates the task.

**3. Row and test data (USE-10, USE-11)**

One row is one account, which is the unit I score: matches. The entity is a known account (USE-10: I score my
existing book every year), so the realistic split is temporal (this year's book, next year's outcome), impossible
from one undated extract: `ForcedIIDFromTemporal` is the honest tag. Random accounts of the same municipalities at
the same time is not what I face, but the municipality-level shift it hides is the right one to hide: I score my own
accounts, so my municipality's level is known to me. The 20% of rows from runs without recorded debt are accounts I
would not score with this model either (their debt sits in another system or was never loaded), so dropping them
matches my use (USE-7 in spirit: rows lacking the outcome record are not task rows).

**4. Would I use it?**

As a segmentation aid, yes: category, property value and the electricity lever are how municipal impairment and
credit-control policies already group debtors, and AUC 0.874 from the static profile and billing is useful for
ranking accounts with thin payment data. I would trust it for that. I would distrust it as a forecast: it never saw
a future outcome, it cannot tell "already in arrears" from "will fall into arrears", and in practice my age analysis
answers the current-status question exactly. For a benchmark this is a real, rare African public-finance task with
a stated gap; that justifies approximate, not none (USE-2 does not apply).

**Gaps, ranked by how much they change the task**

1. Concurrent label: status at the end of the feature window, not a later outcome (USE-3, USE-8). Largest change: a
   state classification standing in for a forecast.
2. Prior-period payments and age analysis absent (always known in practice; dropped here because of the window
   overlap). Changes which signal the model can use; real models would lean on them.
3. Binary "any 90+ amount" instead of a probability of non-recovery weighted by amount (USE-5). Changes the
   resolution, not the direction.
4. No municipality key; random split mixes eight municipalities (USE-10). Small for my use, since I score my own.
5. Missing indigent / prepaid / owner-tenant fields. Harder task, same decision.
6. `HasIDNo` possibly captured during collection (kept, named; 0.002 AUC). Negligible.

**What an expert would change**

* Within this file: nothing structural; keep the fit approximate and keep the current drops. Tighten the use-case
  wording to "which accounts are (or will be) bad debts" and drop "how much", or say the amount is not predicted.
* With a richer extract (ask DMS Technologies): features from the age analysis and payments up to T0, label =
  account 90+ days in arrears or written off at T0 + 12 months, restricted optionally to accounts current at T0;
  temporal split; municipality as a column. That would make the fit direct.

**Sources**

* Kaggle data card, via OpenML 43838 description: https://www.openml.org/search?type=data&id=43838 (the Kaggle page,
  https://www.kaggle.com/datasets/dmsconsultingsa/municipal-debt-risk-analysis, did not render).
* Laingsburg Municipality impairment policy (90 days of non-payment as impairment indicator):
  https://laingsburg.gov.za/download_document/1278
* Metsimaholo debt impairment methodology 2023/24:
  https://www.metsimaholo.gov.za/wp-content/uploads/2026/08/DEBT-IMPAIRMENT-METHODOLOGY-2023-24.pdf
* Auditor-General findings on GRAP 104 impairment (payment history and age analysis used in impairment), e.g.
  https://lg.treasury.gov.za/supportingdocs/FS162/FS162_Audit%20Report_2024_Y_20250627T101557Z_ymak27.pdf
* Mamusa LM MFMA briefing note (risk assessed through the year, credit control):
  https://pmg.org.za/files/210302Briefing_note_template_MFMA_18-19-Mamusa_LM.pdf
* The definition, its README and the earlier REVIEW.md; electricity and category rates computed on the curated
  frame; the task probes (RF AUC 0.874, single feature 0.787).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes** - a real, useful municipal-credit task with honest-enough features after the obvious leaks were removed, but the label definition is undocumented, billing features share the label's time window, and the IID split hides an 8-municipality structure.

**Task**
Municipal revenue/credit-control officers in South Africa flag accounts likely to become bad debt so they can prioritise collection, electricity cut-offs, or provisions. Source (OpenML 43838, CC0): "extracted from the billing systems of 8 South African municipalities over a 2-year period, then summarized by account"; goal is to forecast at-risk accounts "by number and value". Real use.

**Concerns (most to least serious)**
1. **Label undefined and window concurrent with features.** The source does not say how BadDebtIndic is set; sibling columns TotalDebt ("debt at 90 days or more"), TotalWriteOff, CollectionRatio, DebtBillingRatio suggest it is a rule on those. Those were correctly dropped here, but TotalBilling / AverageBilling / TotalElectricityBill cover the same 2-year window the label summarises, so this is a cross-sectional "is it bad debt now" classification, not a forecast. Acceptable as a benchmark, but document it as such; no fix possible without dates.
2. **Hidden groups / split.** 8 municipalities, no municipality id, no dates. Random 3-fold IID split mixes municipalities; the use case (score accounts of a known municipality) makes IID tolerable, but the task card should say so. 6,355 exact duplicate rows (6.2%), 6,909 duplicate feature vectors, 554 with conflicting labels: likely distinct accounts with rounded values (e.g. PropertyValue 60000 appears 5,167 times), so I would keep them but note it.
3. **Base rate 56% bad debt** is high but consistent with SA municipal arrears; plausible.
4. **Preparation.** Types fine (AccCategory categorical, 12 levels incl. "Unknown" 7,217 and one "Environmental Management" singleton). PropertyValue/Size ~8.8% NaN (informative: 64% vs 55% bad debt). TotalElectricityBill has negatives (min -16,171, credits) - plausible. HasIDNo flagged by source as "not reliable". Heavy-tailed monetary values (max 26M) - fine for trees.
5. **Signal.** LightGBM 3-fold AUC 0.876 all features; PropertyValue alone 0.788, billing alone 0.804; not trivial, clear signal, 101,871 rows is ample.

**Could not check**
Kaggle page did not render; exact label rule; municipality or time of each account; whether duplicates are real distinct accounts.

</details>

<details><summary>Precedents</summary>

Inputs: the register of past decisions (808 decisions; none of its four flags touches this dataset), the record, the definition, the Cases tables of `leak_checks.md` and the Tensions
table of `principles.md`, sibling records (credit default, utility, churn, snapshot datasets). The definition did not
change since the 2026-10-12 decision; this checks the definition and the issues of the earlier review (label-rule columns, payments, run drop, cohort
filter, duplicates); only the run drop is still an issue here (issue 1).

**Summary**

| Decision | Verdict | Closest precedents |
|---|---|---|
| Label-rule columns dropped (issue 2) | consistent | SEL-5 / LEAK-10 case row of this dataset; central_international (SEL-5, Trivial); PROV-15 OpenML 43838 row; TabSTAR rule (Lennart, 2026-10-15) |
| Payment totals dropped (issue 3) | consistent | mutual_funds_india `rating` (Lennart, 2026-10-01, LEAK-10 "snapshot data"); african_credit_scoring repay amounts (AI, 2026-10-07) |
| Billing totals kept (`TotalBilling`, `AverageBilling`) | departs without a stated reason | iranian_churn retired (Lennart, 2026-10-01; LEAK-10 "window ends at the outcome"); mutual_funds_india (LEAK-10 "computed from the window that defines the target") |
| `TotalElectricityBill` kept | departs with a stated reason whose fact only partly holds | Lennart CC 2026-10-12 on this record; LEAK-11 south_africa_coronary_heart_disease |
| `HasIDNo` kept | consistent (stated reason) | Lennart CC 2026-10-12; LEAK-11 (weakens the signal: 0.874 with, 0.872 without) |
| No-debt runs dropped by a file-order rule (issue 1) | departs from the wording of a Must (LEAK-25) with a fact that sets it apart; needs a confirmation or an amendment, not an exception | ghanas_indigenous_intel retired (Lennart, 2026-10-01, LEAK-25); obesity_estimation (file-order filter, 2026-10-14); african_credit_scoring (rows labelled 0 by construction dropped, AI 2026-10-07, open) |
| Uploader's cohort filter (issue 6) | consistent | LEAK-22 diabetes_130_us; mobile_churn never-activated SIMs (open issue, not yet decided) |
| Duplicates kept (issue 7) | consistent | LEAK-18 sepsis_survival; caracas_cervical_cancer, breast_cancer_prediction, expresso_churn accepted warnings; contrast wine_quality, jm1, obesity_estimation (dropped) |
| IID, `ForcedIIDFromTemporal`, no municipality grouping | consistent (stated reason) | Lennart CC 2026-10-12 on this record; contrast maternal_health_risk (retired 2026-09-30, sites not in the file) |
| Snapshot status standing in for a forecast (fit approximate) | consistent, with a pair worth naming | mutual_funds_india retired 2026-10-14 (`No Good Target`: one snapshot, a trailing window shared by all) |

**Per decision**

**1. Label-rule columns dropped (issue 2): consistent**

* Follows its own case row (SEL-5 / LEAK-10 Cases: "the deterministic rule's inputs dropped; the rest still makes a
  real task") and LEAK-10 ("a part, a consequence or another encoding of the target").
* Against central_international_medical_college_and_hospital_health_risk_prediction (SEL-5: the label is NEWS2 and
  its inputs are the whole task: `Trivial`), the fact that sets this case apart is in the data: without the three
  columns the rest still predicts (ROC AUC 0.874, best single feature `PropertyValue` 0.787, no `solved` or
  `one_feature` flag).
* PROV-15 row "OpenML 43838 (account debt): the label columns shipped as features: a problem of that copy": followed.
* The issue's sentence on TabSTAR ("its preprocessing was not checked") is within Lennart's rule of 2026-10-15
  (PROV-15: another collection's columns or labels are no reference; named only for provenance or a duplicate). It
  should not be read as an open task.

**2. Payment totals dropped (issue 3): consistent**

* Follows mutual_funds_india `rating` (CC 2026-10-01, Lennart; LEAK-10 Cases: "snapshot data: a feature computed from
  the window that defines the target: drop it, even though its value is known at snapshot time"). Arrears are billing
  less payments plus the opening balance, and the status is read at the end of the window the payments sum.
* Sibling: african_credit_scoring_challenge dropped the repay amounts that grow after a default (AI assessment
  2026-10-07, AUC 0.907 -> 0.639), the same direction.
* The alternative "keep them as the uploader does" would depart from both without a distinguishing fact.

**3. Billing totals kept (`TotalBilling`, `AverageBilling`): departs without a stated reason**

* The same mutual_funds reading applies to the billing side: billing is the other term of the arrears arithmetic and
  sums the same two years at whose end the label is read (checklist P4 row; `fit_reason` names it). LEAK-10 lists "a
  feature computed from the window that defines the target" as out, and its Cases row for iranian_churn (Lennart,
  2026-10-01, retired) says "features summarise a window that ends at the outcome: retire when no common prediction
  point can be rebuilt".
* The curator's CC of 2026-10-12 gives reasons for `TotalElectricityBill` and `HasIDNo` only; for the two billing
  totals neither the record nor the definition names what sets them apart from the payment totals dropped by the same
  rule. The fit_reason states the gap but does not argue it.
* A plausible distinguishing fact exists and is checkable: billing is set by tariff and property, not by the holder's
  behaviour, so it does not move with the outcome the way iranian_churn's usage fell in the churn month. Against it:
  the Unknown run's accounts are billed only 1-3 times, and electricity cut-offs for arrears would lower billing.

**Consistency check (AI, 2026-10-20):** keeping `TotalBilling` and `AverageBilling` (a departure from LEAK-10, "a
feature computed from the window that defines the target") differs from mutual_funds_india `rating` (dropped
2026-10-01) and iranian_churn (retired 2026-10-01): the same mechanism, features over the window at whose end the
label is read. What sets them apart?
(a) billing is set by the tariff and the property, not by the holder's payments, so it carries no trace of the
outcome (to be shown: billing per line for bad debts and others within category and property-value bands), recorded
as an exception; (b) treat them like the payment totals and drop them (static profile only, AUC 0.832); (c) reopen
mutual_funds_india / iranian_churn to match; (d) amend LEAK-10 to say which window-sums stay in a snapshot task.

**4. `TotalElectricityBill` kept: departs with a stated reason whose fact only partly holds**

* CC 2026-10-12 (Lennart) keeps it as a `Potential leak, kept on purpose` because "among billed accounts electricity
  is the same share of the bill for bad debts and others (median 0.33)". The checklist (procedure row) does not
  reproduce this by class: median share 0.353 (not bad) against 0.301 (bad); 0.338 pooled; Residential 0.334 against
  0.286. The other half of the reason (most signal is whether the municipality bills electricity) is not contested.
* Per "Arguing a call", a documented reason contradicted by a measurement goes back to the curator. With it the AUC
  gain is small (0.874 against 0.865), which fits LEAK-11 if the column weakens, but a lower share for bad debts is
  what a cut-off for arrears would leave.

**Consistency check (AI, 2026-10-20):** your keep of `TotalElectricityBill` (2026-10-12, a departure from LEAK-10
resting on "the same share of the bill for bad debts and others") rests on a fact that does not reproduce by class
(0.301 bad against 0.353 not bad). Does the keep still stand?
(a) the gap comes from the mix of categories and municipalities, not from cut-offs (to be shown: the share by class
within category and electricity-billing municipality block), and the note is corrected to the measured medians;
(b) drop it like the payment totals (0.865); (c) keep it, with the note saying a lower share for bad debts is
measured and may be cut-offs (LEAK-11 reading); (d) amend LEAK-10 / LEAK-11.

**5. `HasIDNo` kept: consistent**

Stated reason in the CC of 2026-10-12 and the definition's `Potential leak, kept on purpose` note; the gain is 0.002,
which matches LEAK-11 (south_africa_coronary_heart_disease: kept with a note when it does not strengthen the signal).

**6. No-debt runs dropped by a file-order rule (issue 1): departs from the wording of a Must, with a fact**

* LEAK-25 (Must): "'No event' mixed with 'not recorded' is a censoring bias: retire unless the recording process can
  be recovered." Its case, ghanas_indigenous_intel (CC 2026-10-01, Lennart), was retired (`Too Small`, `Data Quality
  Issue`).
* What sets this case apart, evident from the data: in ghanas the unrecorded rows could not be located (a "likely
  rather than proven" bias, spread over farmers, on top of a too-small task); here they sit in seven contiguous runs
  that are measured, not guessed (0 of 11,984 billed never-payers bad inside against 91.5% outside; membership AUC
  0.988), and the rest of the file is large. Partial recovery of the recording process (where it failed) rather than
  of the missing values.
* Other file-order or by-construction row drops: obesity_estimation keeps its first 498 rows (AI assessment
  2026-10-14, followed by the curator's CC the same day), but there the cut was confirmed by the paper's Fig. 1 counts;
  here no source confirms it (DMS Technologies not asked). african_credit_scoring_challenge drops 8,899 rows labelled 0
  by construction (AI, 2026-10-07; still an open issue). in_vehicle_coupon_recommendation uses file-order blocks as
  groups (SPLIT-24). So a rule on the raw file order has precedent; one without a source's confirmation does not.
* Residual of the rule: the 186-row run of never-payers with ID numbers stays (anomaly bullet), so shorter unrecorded
  stretches may remain; the threshold 1,000 is set on this file.
* Tension row "Repair against cleaning around damage" (PROV-13): when the origin cannot be reached, keep with a note
  or retire. Dropping the runs is cleaning around damage, which that row allows only as "keep with a note"; that fits.
* LEAK-25 is a Must, so this cannot be an exception: either the curator reads "recovered" to cover "the unrecorded rows
  can be located and dropped" (a Cases row for LEAK-25, which settles it for later datasets), or LEAK-25 is amended.

**Consistency check (AI, 2026-10-20):** dropping the seven no-debt runs instead of retiring departs from the wording
of LEAK-25 (a Must) and from ghanas_indigenous_intel (retired 2026-10-01, "no rain" mixed with "not measured"). What
sets this case apart?
(a) the unrecorded rows are located, not guessed (contiguous runs, 0% against 91.5% bad among never-payers,
membership AUC 0.988) and the rest is large, so the recording process is recovered where it failed: recorded as a
Cases row of LEAK-25 that reads "recovered" this way; (b) treat it like ghanas and retire (`Data Quality Issue`);
(c) reopen ghanas (not applicable as it was also `Too Small`); (d) amend LEAK-25 to "retire unless the recording
process can be recovered or the unrecorded rows located and dropped".

**7. The uploader's cohort filter (issue 6): consistent**

Follows LEAK-22 ("follow the paper's cohort", diabetes_130_us); the uploader's notebook is the only documented cohort.
The dropped rows are mostly debts that predate the window (77.8% bad), rows whose label the window cannot explain.
mobile_churn's drop of never-activated SIMs is the nearest sibling, still an open issue, so no curator precedent
either way.

**8. Duplicates kept (issue 7): consistent**

* Follows LEAK-18 (few features, plausible repeats: natural, keep and say so; sepsis_survival) and the accepted
  `dataset_duplicate_rows` warnings of caracas_cervical_cancer, breast_cancer_prediction, expresso_churn_prediction_1m,
  hotel_booking_demand: distinct entities with a coarse profile. Seven features with zero-to-missing property fields and
  flat charges (162 accounts billed R6 in six R1 lines) fit that.
* The issue's named alternative (wine_quality, LEAK-19) is the opposite pole: many continuous lab values, collection
  copies. jm1 and obesity_estimation were dropped for the same kind of reason (copies of one entity). The evidence
  here is weaker than caracas's (a recombination test) but the direction matches; no departure.

**9. IID with `ForcedIIDFromTemporal`, no municipality grouping: consistent**

* Curator decision with a stated reason (CC 2026-10-12, Lennart; register "ships as IID, tagged forced IID from
  temporal"): a municipality scores its own accounts, so its level is known.
* Pair to name: maternal_health_risk was retired (CC 2026-09-30) because its collection sites are not in the file. The
  fact that sets this case apart is the use case (scoring the municipality's own accounts needs no unseen-site
  generalisation), plus maternal_health's 74% test copies. Consistent with the Tensions row "Temporal against grouped:
  one regime, the one the use case implies".

**10. One snapshot standing in for a forecast (fit approximate): consistent, a pair to watch**

mutual_funds_india was retired on 2026-10-14 (Lennart, `No Good Target`) because a one-snapshot label over a window
all funds share supports no decision. account_debt was kept on 2026-10-12 on a similar one-snapshot construction. The
distinguishing fact is in the data: the label is per account and driven by the account (the fund's sub-category alone
gave R^2 0.776 of 0.783; here no feature dominates, best single 0.787 of 0.874). Not drift, but the panel's point that
"a deployed model mostly flags accounts the age analysis already lists" bears on it, and decision 3 above is where it
would surface.

**Drift and third exceptions**

* No drift found in Lennart's LEAK-10 decisions: window-sums of the target were dropped in mutual_funds (2026-10-01)
  and here (payments, 2026-10-07/12); the billing keep is an unargued gap, not a reversal.
* `Potential leak, kept on purpose` under LEAK-10/LEAK-11: `TotalElectricityBill` and `HasIDNo` here, plus the
  scaling-over-all-rows notes (a different rule, LEAK-30). No third exception of the same reason under LEAK-10.
* LEAK-25: if (a) of decision 6 is chosen, it is the first reading of "recovered" as "located"; write it as a Cases
  row so later datasets follow it.

</details>

<details><summary>Advocate</summary>

Position: ship as defined. The definition stays; the real problems the panel found are in the notes and the task text,
and each has a fix at the "keep with a documented note" rung or below. Nothing found needs a change to the rows, the
columns or the split.

**1. A real use case at an approximate fit, which the rules already record for this very dataset**

* Claim: the task is a real municipal credit-control / impairment task, shipped honestly as approximate.
* Evidence: the practitioner (revenue manager, GRAP 104 impairment) confirms "approximate" and "would use it as a
  segmentation aid"; the blind reviewer, with no notes, says "include", "a real, useful municipal-credit task". USE-8
  lists account_debt_south_africa as its own Cases example of approximate ("one snapshot for a forecast"); SPLIT-8
  likewise (Lennart, 2026-10-12). The label's resolution, 90+ days of non-payment, is the impairment indicator
  municipalities use (practitioner's sources: Laingsburg, Metsimaholo policies).
* Rules: USE-1, USE-5, USE-8 (Must, P3) hold.
* Answers the claim auditor's refutation of "turned into bad debt" (83.7% of bad debts hold more 90+ debt than the
  window's net arrears). Conceded as wording, not as validity: the target is still the status the actor acts on (USE-5
  holds); the question text overstates "turned into". Mildest fix: rewrite `question`, `predicted`, `fit_reason` to
  "is in 90+ day arrears or written off at the extract" and drop "how much" from `use_case` (practitioner). That is a
  task-summary edit; the curator's 2026-10-12 decision already accepted a status at the extract standing in for a forecast.
  It does not reopen the mutual_funds_india pair: there the sub-category alone gave R^2 0.776 of 0.783; here the best
  single feature gives 0.787 of 0.874 (precedents, decision 10).

**2. The leaks that matter are removed, and what remains is a non-trivial task**

* Evidence: the label rule reproduces exactly (debt or write-off -> 63,600 bad / 0 not; 371 exceptions) and its three
  columns are dropped; the payment totals of the window go (0.949 -> 0.870 in the auditor's run). The rest still
  predicts: ROC AUC 0.874, best single feature 0.787, no `solved` / `one_feature` flag.
* Rules: LEAK-10 (Must, P4) fixed in the definition; TP (P6) holds. Precedents consistent: SEL-5/LEAK-10 case row of this
  dataset, mutual_funds_india `rating`, african_credit_scoring repay amounts, PROV-15 (OpenML 43838 ships the lookup).
* Answers nothing open: every agent agrees on these drops.

**3. The split is right: IID, forced, tagged**

* Evidence: split auditor "right with notes", no re-split. Its reruns reproduce the cost of the missing municipality key
  (random 0.877, blocks of 2,500 0.849, thirds 0.787). The use case scores a municipality's own accounts, so the
  municipality is not unseen.
* Rules: SPLIT-8 (Must, names this dataset), SPLIT-4 (Must: "not the size of the gap"); Tension row "Temporal against
  grouped: one regime, the one the use case implies" (Lennart, 2026-10-12). A grouped split on file blocks would be
  a guess (SPLIT-24).
* Answers the "municipality as a feature" note (random + file position 0.892): conceded as a SPLIT-8 cost line in the
  notes and a request to DMS for the key; building it from file blocks would be the guess SPLIT-24 forbids.

**4. The no-debt runs: a fix in the definition, not a reason to retire**

* Claim: dropping the seven runs fixes the LEAK-25 censoring by locating where recording failed.
* Evidence: inside the runs 0 of 11,984 billed never-payers are bad debts, against 91.53% of 40,984 outside; non-payers
  with 24-100 billing lines 0% against 97-98%; ID numbers 0-0.7% against 53%; membership AUC 0.988. The rest is large
  (101,871 rows). The practitioner: these are accounts "I would not score with this model either (their debt sits in
  another system)", USE-7 in spirit.
* Rules: LEAK-25 (Must, P4). principles.md, Strengths: a Must violation "is fixed in the definition when it can be
  (drop, lag, filter, re-split, re-target); otherwise the verdict is No". A filter is on that list, and the remedy
  ladder puts it before exclusion. ghanas_indigenous_intel is set apart by facts: its unrecorded rows could not be
  located, and it was also `Too Small` (precedents, decision 6).
* What follows: the curator records the reading "recovered = the unrecorded rows located and dropped" as a LEAK-25
  Cases row (precedent checker's option a), so later datasets follow it. Conceded: the 186-row run (185 curated rows,
  0.18%, no bad debts, all with ID numbers) looks unrecorded too. Mildest fix: say so in its anomaly bullet. Dropping
  it by its signature is the alternative; with 0.18% of rows the choice cannot move the task.

**5. The billing totals: the fact that sets them apart from the dropped payments is now measured**

* Claim: `TotalBilling` and `AverageBilling` carry no trace of the outcome, unlike the payments.
* Evidence: within municipality block x property-value bin (Residential), the billing residuals separate the classes at
  ROC AUC 0.509 (total), 0.501 (per line), 0.496 (number of lines) (column audit, problem 2). Billing is set by tariff and
  property. The claim auditor's own number cuts the same way: 83.7% of bad debts carry more debt than the window's net
  arrears, so the label is mostly not built from this window's billing. Payments are the opposite: 91.5% bad among
  never-payers against 14.7% among those who paid 87.5-105%.
* Rules: LEAK-10 (Must). Its window clause is aimed at a feature that moves with the outcome: iranian_churn's usage fell
  in the churn month, mutual_funds' rating was computed from the target window. The measurement (EV-2: data over
  inference) shows billing does not move with the outcome, so the clause is not triggered.
* Answers the precedent checker's "departs without a stated reason". Conceded: the reason was not written. Mildest fix:
  write the residual AUCs into the notes as the fact that sets the case apart (its option a, as a LEAK-10 Cases row).
  Dropping them would leave the static profile at 0.832 to guard against a trace the data does not show.

**6. `TotalElectricityBill`: correct the note, keep the column**

* Evidence: the note's "same share (median 0.33)" fails pooled (0.353 vs 0.301, share AUC 0.562; claim auditor) but holds
  within electricity-billing blocks (0.334 for both classes; column auditor): the pooled gap is municipality mix. The
  open signal is "no electricity billed" within a block (38.6% vs 19.2% bad, AUC 0.588). The column auditor rates it
  "circumstantial, not proof (EV-6)": vacant or unconnected properties look the same. The practitioner reads zero
  electricity as no municipal supply or a prepaid meter, both known up front (USE-6). Effect of the whole column: 0.874
  -> 0.865.
* Rules: LEAK-11 (Should, narrows LEAK-10) for a weak suspected trace kept with a `Potential leak, kept on purpose`
  note; LEAK-10 needs a feature that holds what did not exist at the prediction point, and that is not shown (EV-6:
  an untested mechanism is a question, not a finding).
* What follows: rewrite the note and the CC basis with the within-block numbers and ask the curator whether the
  2026-10-12 keep stands ("Arguing a call"). A billed 0/1 flag (0.868) is the fallback if the curator reads zero as a
  cut-off. Either way the dataset ships.

**7. The rest is consistent with precedent and needs at most cheap cleaning**

* Duplicates: 6,355 rows (6.2%), seven features, flat charges (162 accounts billed R6); 91.1% of duplicate groups lie
  within 2,500 file rows (one municipality); hidden-group probe no hits; AUC 0.870 -> 0.864 without copied test rows.
  LEAK-18 (Should) keep-and-say-so; consistent with sepsis_survival, caracas, expresso_churn (accepted warnings).
* Cohort filter: LEAK-22 (Must) followed (the uploader's notebook is the only documented cohort); precedents consistent.
  Conceded: its reason "debt predates the window" does not set the 8,700 apart (claim 21); reword to what the filter does.
* `HasIDNo`: 0.874 vs 0.872, within-block AUC 0.529; LEAK-11, consistent with the CC of 2026-10-12.
* P7: `PropertyValue` = 1 (25 rows) and `PropertySize` <= 10 (5 rows) to missing is cheap and safe (CLEAN-10/11); take it
  or note it. The README quote "about 20 million records ... PostgreSQL" is untested (EV-2): source it or cut it.

**Judgment record (advocate's reading)**

Verdict: ship (definition as is; notes and task text corrected).
Validity: USE-5/USE-8 hold (approximate, wording fixed); LEAK-10 triggered, fixed (label rule, payments); LEAK-25
triggered, fixed by a filter (Cases row for the curator); SPLIT-8/SPLIT-4 hold; LEAK-22 followed.
Value: TP holds (0.874, best single 0.787, 101,871 rows).
Quality: LEAK-11 keeps (`TotalElectricityBill` note rewritten, `HasIDNo`); LEAK-18 duplicates kept; CLEAN-10 placeholders
cheap.
For the curator: the LEAK-25 reading (point 4), the billing-window fact (point 5), the electricity keep (point 6).

</details>

<details><summary>Critic</summary>

**Position: ship only after changes.** No point calls for exclusion: each problem can be fixed in the definition or
with a note. But the task statement describes a different label from the one shipped, one Must (LEAK-25) is met only
in part, and the reason given for one kept-on-purpose leak does not hold up when measured.

**1. The task statement promises a forecast that the label does not measure (P3, USE-5 Must, USE-8 Must)**

* Problem: `question` asks "Has an account turned into bad debt?" and `predicted` says "at the end of those two years".
  Most positive labels are debt the account already carried before the window began.
* Effect: a model user reads this as detecting accounts that went bad during the window. What it actually does is
  classify a standing arrears status from the billing profile. That status is also the one the municipality's age
  analysis already gives (practitioner, section 4).
* Evidence: of 57,199 curated bad debts, 83.7% hold more 90+ debt plus write-off than the window's net arrears, and
  69.1% hold more than the whole two-year billing. 16.9% of them paid at least 87.5% of their billing (claim audit,
  claim 1 and the implied target). The use case also promises "how much", but no amount is predicted (practitioner,
  section 2).
* Remedy (fix the definition text): reword `question` and `predicted` to "is in arrears of 90+ days or written off
  at the extract". Drop "and how much" from `use_case`. Make `fit_reason` say that most of the status is inherited.
  Keep `fit="approximate"`.

**2. A 186-row run that looks just like the dropped unrecorded runs stays in, labelled No (P4, LEAK-25 Must)**

* Problem: the drop rule leaves in one stretch that has the same signature as the dropped ones. The run drop as a
  whole also departs from the wording of LEAK-25 ("retire unless the recording process can be recovered").
* Effect: 185 rows where debt was not recorded stay in as "not a bad debt". This is the same censoring bias at small
  scale.
* Evidence: in the 185 kept rows, 0 are bad debts, 98.4% were billed and never paid, and all have an ID number. Outside
  the runs, 91.5% of billed never-payers are bad debts (claim audit, implied claim and claim 20). The precedent checker
  (decision 6) finds that dropping the runs needs a Cases row or an amendment of LEAK-25, not an exception.
* Remedy (fix the definition): drop this run by its signature (billed never-payers with an ID and no bad debt), not
  by a lower length threshold. The curator records the LEAK-25 Cases row: "recovered" covers "located and dropped".

**3. `TotalElectricityBill`: the reason for keeping it is partly refuted (P4, LEAK-10 Must; LEAK-11 Should)**

* Problem: the curator's CC of 2026-10-12 and the note rest on two statements: the signal is "mostly whether the
  municipality bills electricity", and "cut-offs leave no trace". Within municipalities, accounts billed no electricity
  are bad debts about twice as often. A cut-off for arrears would leave exactly that trace.
* Effect: a possible consequence of the label stays in as a feature. LEAK-11 covers a value that weakens the signal.
  This one strengthens it (0.865 to 0.874).
* Evidence: in file blocks where 80% or more of accounts are billed for electricity, accounts billed none are bad debts
  at 38.6%, against 19.2% for the rest. "No electricity billed" alone separates the classes within blocks at AUC 0.588
  (column audit, problem 1). The share among billed accounts holds within blocks (0.334 for both classes), but the
  pooled medians are 0.353 vs 0.301 (claim audit, claim 24). Vacant properties would look the same, so this is not
  proof (EV-6).
* Remedy (a note plus a curator call): rewrite the note and the CC with the within-block numbers, and send the keep
  back to the curator ("Arguing a call"). If a zero electricity bill reads as a cut-off, drop the column (LEAK-10).

**4. The billing totals are kept without the reason the precedents require (P4, LEAK-10 Must)**

* Problem: `TotalBilling` and `AverageBilling` sum the same window at whose end the label is read. The LEAK-10 Cases
  rows dropped or retired that mechanism: mutual_funds_india `rating`, and iranian_churn. Neither the record nor the
  definition says what sets these two columns apart.
* Effect: like cases are treated differently with no written fact behind it. The keep is probably right.
* Evidence: within block and property-value bin, the billing residuals separate the classes at AUC 0.509, 0.501 and
  0.496 (column audit, problem 2), so billing carries no trace of the outcome. Precedent checker, decision 3: departs
  without a stated reason.
* Remedy (a note): add a `curation_comments` bullet giving the fact: billing is set by tariff and property, with the
  residual AUCs. The curator records it as a LEAK-10 Cases row.

**5. The municipality is known in deployment but missing from the features (P4, SPLIT-8 Should, SPLIT-31)**

* Problem: the split is right. The note on what the missing municipality key costs is incomplete.
* Effect: the model has to rebuild a fact the actor has (from `HasIDNo` blocks and electricity zones), so scores
  understate a deployed model.
* Evidence: adding file position as a stand-in raises random-split ROC AUC from 0.877 to 0.892 (split audit,
  problem 1).
* Remedy (a note): add this to the IID bullet. Do not build a key from file blocks (SPLIT-24).

**6. Wrong reasons in the notes and the record (writing; EV-2)**

* The cohort bullet says the 8,700 dropped accounts are those "whose debt predates the window". That does not set them
  apart: 83.7% of the kept bad debts carry debt older than the window too (claim audit, claim 21). Reword the bullet
  to say what the filter does: no net billing, or negative payments.
* The record's quote "about 20 million records ... PostgreSQL" is not in the Kaggle description (claim audit, claim 35).
  Cite where it comes from, or remove it.

**7. Placeholder property values (P7, CLEAN-10 Should; quality, not a reason to exclude)**

* `PropertyValue` is exactly 1 in 25 rows and `PropertySize` is 10 or less in 5 rows (column audit, problem 5).
* Remedy (cheap repair): set them to missing along with the zeros.

**Judgment record**

Verdict: ship after changes.
Validity: USE-5 triggered, fix the wording (1); LEAK-25 partly met, drop the 186-row run and add a Cases row (2);
LEAK-10 `TotalElectricityBill` reason refuted in part, back to the curator (3); LEAK-10 billing keep needs its stated
fact (4); SPLIT-8 note incomplete (5).
Quality: CLEAN-10 cheap repair (7); writing fixes (6).

</details>

<details><summary>Advocate rebuttal</summary>

The critic and I agree on the verdict's substance: no point calls for exclusion, and the split, the label-rule drops and
the payment drops stand. What is left is how much of the definition changes. I concede points 1, 4, 5, 6 and 7. I
dispute how point 2's fix is written and one step of point 3.

**1. Task statement promises a forecast: conceded**

Same remedy as my point 1: reword `question`, `predicted`, `fit_reason` ("is in 90+ day arrears or written off at the
extract; most of the status is inherited") and drop "how much" from `use_case`. Keep `fit="approximate"`. What follows:
a text fix under USE-5/USE-8 (Must, P3). The target stays the one the actor acts on (90 days is the impairment
indicator), so this does not reopen USE-2.

**2. The 186-row run: the fix is conceded, its form is disputed**

* Conceded: the run has the dropped runs' signature (185 rows, 0 bad, 98.4% billed never-paid, all with ID numbers), so
  under LEAK-25 (Must) dropping it is more consistent than a note. I move from "note it" to "drop it". The LEAK-25 Cases
  row ("recovered" covers "located and dropped") is common ground.
* Disputed: the critic's rule, "billed never-payers with an ID **and no bad debt**", selects rows on the label. That is
  a filter that reads the target row by row, and it would also catch genuine non-bad never-payers elsewhere in the file
  (8.5% of the 40,984 outside the runs are not bad). The seven runs are dropped as contiguous stretches of the file, by
  a run-level rule. Mildest fix that keeps that property: drop this one stretch as a run (its file range, or a run rule
  on runs of billed never-payers with no recorded debt), and name the range in the anomaly bullet. Rule: LEAK-10/LEAK-25
  (P4); a row filter on the target is itself a selection leak, while a run-level rule is the documented recovery.
* Effect either way: 0.18% of rows. It does not move the task, so it is no reason to hold the dataset.

**3. `TotalElectricityBill`: partly conceded**

* Conceded: LEAK-11 does not cover it. The column strengthens the signal (0.865 -> 0.874), and LEAK-11's text is for
  "a value ... that weakens the signal". My brief leaned on LEAK-11 wrongly. Conceded too: the note's "cut-offs leave
  no trace" is not supported, and the note and CC need the within-block numbers. The keep goes back to the curator
  ("Arguing a call").
* Disputed: that leaves LEAK-10 alone, and LEAK-10 needs a feature that holds what did not exist at the prediction
  point. That has not been shown. The critic and the column auditor both rate the within-block signal (38.6% vs 19.2%,
  AUC 0.588) "not proof (EV-6)"; vacant, unconnected or prepaid properties give the same pattern, and the practitioner
  reads zero electricity as no municipal supply or a prepaid meter, known up front (USE-6, Must). The within-block share
  test, the trace a partial-window cut-off would leave, finds none (0.334 for both classes). So the dispute is a weighing
  call for the curator, not a found leak. Fallback if the curator reads zero as a cut-off: drop the column (0.865), the
  task still ships. Rule: EV-6 (an untested mechanism is a question), USE-6 against LEAK-10.

**4. Billing totals need their stated fact: conceded**

Same remedy as my point 5: a `curation_comments` bullet with the residual AUCs (0.509 / 0.501 / 0.496), and a LEAK-10
Cases row for the curator. The critic agrees the keep "is probably right".

**5. The municipality-key cost: conceded**

Add 0.877 -> 0.892 (file position as a stand-in) to the IID bullet; no key built from blocks (SPLIT-24). One
correction: SPLIT-8 is a Must, not a Should; its "cost of the missing time axis measured" clause is what this note
fulfils.

**6. Wrong reasons in the notes: conceded**

Reword the cohort bullet to what the filter does (no net billing, net credit, negative payments). Source or cut the
"20 million records ... PostgreSQL" quote (EV-2).

**7. Placeholder property values: conceded**

`PropertyValue` = 1 (25 rows) and `PropertySize` <= 10 (5 rows) to missing (CLEAN-10/11). Cheap and safe.

**Where this leaves the verdict**

I accept "ship after changes". The changes are: text (1, 4, 5, 6), two small row/value fixes (2: 185 rows as a run;
7: 30 values), and one curator call (3). None is a validity failure left unfixed. The LEAK-25 reading (2) and the
electricity keep (3) go to the curator.

</details>

<details><summary>Critic rebuttal</summary>

We agree on almost every fact and remedy. Three disputes remain: the advocate's verdict label, the 186-row run, and
which rule frames the electricity keep.

**Point 1: real use case, approximate fit**

Conceded: USE-5 holds once the text is fixed. The 90+ days status is the impairment indicator municipalities act on
(practitioner), and the advocate accepts the same rewording I asked for (my point 1).

Disputed: the verdict label, "ship, definition as is". The rewording changes `task_summary` (`question`, `predicted`,
`use_case`, `fit_reason`), and `task_summary` is a field of `dataset.py`. So the definition does change, and the
verdict is "ship after changes". This matters for the record: USE-8 (Must) is met only when the fit text names the
real gap (the status is mostly inherited: 83.7% and 69.1%, claim audit, claim 1).

**Point 2: the leaks that matter are removed**

Conceded. The label-rule columns and the payment totals are dropped, and the task stays non-trivial (TP).

**Point 3: the split**

Conceded. IID, forced and tagged (SPLIT-8, SPLIT-4). The SPLIT-8 cost line goes into the notes, and no key is built
from file blocks (SPLIT-24). This matches my point 5.

**Point 4: the no-debt runs**

Conceded: the filter fixes LEAK-25 in the definition, and ghanas_indigenous_intel is set apart by facts.

Disputed: the 186-row run should be dropped, not noted.
* By the advocate's own Cases-row reading of LEAK-25 ("recovered = the unrecorded rows located and dropped"), a run
  that has been located must be dropped. Keeping it with a note contradicts the reading the curator is asked to adopt.
* LEAK-25 is a Must, and a Must is "fixed in the definition when it can be" (principles.md, Strengths). This fix is
  cheap: a mask on billed never-payers with an ID number and no bad debt inside that run.
* Its small size (0.18% of rows) bears on the effect, not on the rule. LEAK-25 has no severity grade.
* Evidence: 185 rows, 0 bad, 98.4% billed and never paid, all with an ID number, against 91.5% bad among billed
  never-payers elsewhere (claim audit, claim 20).

**Point 5: billing totals**

Conceded. The residual AUCs (0.509, 0.501, 0.496) are the fact that sets billing apart from the dropped payments, so
the LEAK-10 window clause is not triggered (EV-2). The remedy is the same as my point 4: a note plus a Cases row.

**Point 6: `TotalElectricityBill`**

Conceded: the pooled share gap is municipality mix (0.334 for both classes within blocks). The "no electricity
billed" signal is circumstantial (EV-6). We agree on the remedy: rewrite the note and send the keep to the curator.

Disputed: LEAK-11 does not cover this case. LEAK-11 keeps a post-outcome value "that weakens the signal". This column
raises ROC AUC from 0.865 to 0.874, and "no electricity billed" alone separates the classes within blocks at 0.588. So
the keep is a LEAK-10 (Must) call for the curator, not a LEAK-11 default. The note should say that, and not cite
LEAK-11. A billed 0/1 flag is no fallback: it keeps exactly the suspect part of the signal, since a 0 is what a
cut-off would show.

**Point 7: duplicates, cohort, `HasIDNo`, placeholders, the quote**

Conceded. Duplicates are kept under LEAK-18, the cohort reason gets reworded, `HasIDNo` is kept under LEAK-11 (it
weakens the signal: 0.872 without it, 0.874 with), and CLEAN-10 and the EV-2 quote fix are agreed.

**Verdict after the rebuttal**

Ship after changes:
* the `task_summary` rewording (USE-5, USE-8);
* drop the 186-row run (LEAK-25);
* the corrected notes (points 4 to 6 of my brief);
* the cheap CLEAN-10 repair.

For the curator: the electricity keep under LEAK-10, and the LEAK-25 Cases row.

</details>

<details><summary>Mediator</summary>

**Mediator report: account_debt_south_africa (re-check, 2026-10-20)**

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1/USE-5/USE-8 hold once the task text is reworded (approximate: a status at the extract,
83.7% of bad debts predate the window); LEAK-10 triggered, fixed (label-rule columns, payment totals); LEAK-10 billing
totals kept on a measured fact (residual AUC 0.509/0.501/0.496), a Cases-row reading for the curator; LEAK-25
triggered, fixed by dropping eight located runs (the seven plus the 186-row run, one run-level rule), a Cases-row
reading for the curator; LEAK-22 followed; SPLIT-8/SPLIT-4 hold (IID forced, cost line added); LEAK-18 duplicates kept.
Value: TP holds (ROC AUC 0.874, best single feature 0.787, 101,686 rows).
Quality: CLEAN-10/11 placeholders to missing; two wrong reasons corrected; an unsourced quote sourced or cut (EV-2).
Weighed: real rare public-finance task +, size +, approximate fit -, municipality key missing -.
For the curator: issue 8, `TotalElectricityBill` keep or drop (LEAK-10, unconfirmed consequence of the target);
issue 1, the LEAK-25 reading; issue 9, the LEAK-10 billing reading.
```

**Changes to make now (no decision needed)**

1. **Reword the task text (USE-5, USE-8; Must, P3).** In `question` and `predicted`, say that the account "is in arrears of 90+ days or written off at the extract". Remove "and how much" from `use_case`. In `fit_reason`, say that most of the status is inherited: 83.7% of bad debts hold more 90+ debt plus write-off than the window's net arrears, and 69.1% hold more than the window's whole billing. Keep `fit="approximate"`.
2. **Drop the 186-row run with a run-level rule (LEAK-25; Must, P4).** Details are under disputed point A. The rule changes `NO_DEBT_RUN_ROWS`, the anomaly bullet, the drop bullet (28,124 raw rows in eight runs), the decision table and the counts in the notes: 101,686 rows, 57,199 positive.
3. **Add a SPLIT-8 cost line to the IID bullet (SPLIT-8, Must; SPLIT-24).** The municipality is known in deployment but has no column. Adding file position as a stand-in raises random-split ROC AUC from 0.877 to 0.892. Do not build a key from file blocks. Ask DMS for the key.
4. **Add a billing-totals note (LEAK-10).** Add a `curation_comments` bullet: billing is set by tariff and property. Within block and property-value bin, the residuals give AUC 0.509 (total), 0.501 (per line) and 0.496 (number of lines). The curator records the Cases row (issue 9).
5. **Correct two wrong reasons (EV-2, writing).**
   - The cohort bullet: "whose debt predates the window" does not set the 8,700 apart, because 83.7% of the kept bad debts carry such debt too. Say what the filter does: no net billing, a net credit, or negative payments.
   - The `TotalElectricityBill` note and its CC basis: "same share (median 0.33)" and "cut-offs leave no trace" are refuted in part. Pooled, the medians are 0.353 vs 0.301. Within electricity blocks, the median share is 0.334 for both classes, but accounts billed no electricity are bad debts at 38.6% vs 19.2% (within-block AUC 0.588). Cite LEAK-10 and LEAK-6, not LEAK-11. The decision itself is issue 8.
6. **Treat placeholders as missing (CLEAN-10/11, Should, P7).** Set `PropertyValue` == 1 (25 rows) and `PropertySize` <= 10 (5 rows) to missing, along with the zeros.
7. **The record's quote "about 20 million records ... PostgreSQL" (EV-2).** It is not in the Kaggle description. Source it or cut it.

**Issues for the curator (ranked)**

**Issue 8. `TotalElectricityBill`: keep or drop (P4, LEAK-10 Must, with LEAK-6 Must).**
- **Problem:** the data card says electricity billing exists "as a means to recover debt", so a cut-off is a consequence of arrears. Under the reworded task (the status at the extract), a cut-off made for earlier arrears would be a consequence of the target, which LEAK-10 rules out.
- **Effect:** ROC AUC 0.874 with the column, 0.865 without.
- **Critic's best evidence:** within blocks where 80% or more of accounts are billed for electricity, accounts billed none are bad debts at 38.6% vs 19.2%. In 50-80% blocks the rates are 54.5% vs 35.7%. Among Residential accounts in blocks of 50% or more they are 54.3% vs 27.0%. The gap remains at equal payment status (paid something: 32.2% vs 23.3%; never paid: 88.7% vs 77.4%). The column raises the signal, so LEAK-11 cannot apply, and both sides concede that.
- **Advocate's best evidence:** the partial-window trace a cut-off within the window would leave is absent: the share among billed accounts is 0.334 for both classes within blocks. Vacant, unconnected or prepaid properties give the same zero, and the practitioner reads a zero as no municipal supply or a prepaid meter. Both are known up front (USE-6).
- **What I settled:** the 0/1 "billed" flag is not a fallback. It scores 0.868 against 0.870 for the full column and 0.860 without it (claim audit), so it keeps nearly all of the column's gain, and the zero it keeps is exactly the suspect signal. The real choices are keep with a corrected note, or drop.
- **Why this goes to the curator:** LEAK-6 lets a measured effect with a known benign cause stay with a note and makes a confirmed leak go even when small. The data cannot tell a cut-off from a vacant or prepaid property (EV-6), and no cheap experiment separates them. Deciding whether this circumstantial evidence counts as "a consequence of the target" is a weighing call, not a rank conflict.
- **What would settle it:** DMS Technologies saying what a zero electricity bill means (no municipal supply, prepaid, or disconnected), or a meter-type column.
- **Decision needed:** (a) keep, with the corrected note recorded as a reading under LEAK-6; or (b) drop under LEAK-10 (0.865; the task still ships).

**Issue 1. LEAK-25 reading (Must; P4).**
- **Problem:** dropping located runs instead of retiring departs from the wording "retire unless the recording process can be recovered". Its precedent, ghanas_indigenous_intel, was retired.
- **What sets this case apart (measured):** the unrecorded stretches are located. Billed never-payers inside the runs are 0 bad out of 12,167 (11,984 plus the 183 in the 186-row run), against 91.5% bad out of 40,984 outside. Membership AUC is 0.988, and 101,686 rows remain. ghanas could not locate its unrecorded rows and was also `Too Small`.
- **Both sides agree:** record a LEAK-25 Cases row that reads "recovered" to cover "the unrecorded stretches located and dropped". A Must has no exceptions, so this has to be a Cases-row reading or an amendment. The other way out is to retire as `Data Quality Issue`.
- **Decision needed:** the Cases row, an amendment, or retirement.

**Issue 9. LEAK-10 reading for the billing totals (Must; P4).**
- **Problem:** `TotalBilling` and `AverageBilling` are computed from the window at whose end the label is read. LEAK-10 lists such features as out "even when known at snapshot time" (mutual_funds_india `rating`; iranian_churn).
- **What sets this case apart (measured):** the billing residuals carry no class signal (AUC 0.509, 0.501, 0.496). Billing is set by tariff and property, not by the holder's behaviour.
- **Both sides agree:** keep the columns and record the reading as a LEAK-10 Cases row ("a window sum that the data shows does not move with the outcome stays").
- **Other options:** drop them, which leaves the static profile at 0.832, or amend LEAK-10.
- **Decision needed:** the Cases row, an amendment, or the drop.

**Disputed points and how they were settled**

**A. How to drop the 186-row run.**
- **Critic:** a mask on "billed never-payers with an ID and no bad debt" inside that run.
- **Advocate:** drop it as a stretch, the way the seven runs are dropped. A row mask reads the target row by row.
- **Rules:** both rest on LEAK-25 (Must, P4) with LEAK-7 (the smallest fix), so this is not a rank conflict. It turns on fact and on consistency with the seven-run rule, which the curator implemented as a run-level rule.
- **Experiment** (two scripts on the raw file): I listed every no-debt run of 30 rows or more with its count of billed never-payers.

  | Run | Billed never-payers | Bad debts |
  |---|---|---|
  | the seven dropped runs | 1,313 / 4,583 / 1,644 / 1,151 / 1,457 / 1,547 / 289 | 0-3 per run |
  | the 186-row run (from file row 91,971) | 183 of 185 billed | 0 |
  | the paying runs of 334 and 218 rows | 2 each | 0 |
  | every other run | 13 or fewer | |

  The rule "drop a no-debt run that holds at least K billed never-payers" selects the same eight runs for every K from 20 to 150. It drops 28,124 raw rows and leaves 101,686 curated rows (57,199 positive, 56.25%). It needs no length threshold, keeps the paying runs, and reads the same debt and billing columns at run level that the existing rule reads. It does not read `baddebt`.
- **Settled:** take the run-level rule (for example K = 100) and write the 183 vs 13 gap into the notes. The critic's row mask would drop nearly the same rows (183 of 186), but it selects on the label row by row and is not the documented recovery unit. One caveat for the notes: like the 1,000-row threshold, K is set on this file.

**B. The verdict label.** The advocate conceded "ship after changes": the task text, a row filter and a value repair change `dataset.py`.

**C. `TotalElectricityBill`.**
- Settled by fact: LEAK-11 does not apply (conceded), and the 0/1 flag is not a remedy (0.868 of 0.870).
- Not settled: keep or drop is a weighing of circumstantial evidence under LEAK-10 and LEAK-6. That is issue 8.

**Agreed facts**

- **Label rule:** accounts with debt or a write-off are 63,600 bad and 0 not bad; 371 accounts without either are bad anyway. The three label-rule columns are dropped; AUC is 0.999 with them.
- **Payment totals:** dropped. AUC is 0.952 with them and 0.874 without (0.949 vs 0.870 under default LightGBM).
- **Signal:** best single feature 0.787. No `solved` or `one_feature` flag.
- **Label meaning:** 83.7% of bad debts hold more 90+ debt plus write-off than the window's net arrears; 69.1% hold more than the window's whole billing.
- **Seven runs:** 27,938 raw rows (20.2%). Inside them, 0 of 11,984 billed never-payers are bad, against 91.5% of 40,984 outside. ID numbers are on file for 0-0.7% of accounts inside, against 53% outside.
- **Split:** IID, forced, tagged `ForcedIIDFromTemporal`.

  | Split | ROC AUC |
  |---|---|
  | random (as shipped) | 0.877 |
  | file blocks of 2,500 rows | 0.849 |
  | thirds of the file | 0.787 |
  | random + file position as a feature | 0.892 |

  A grouped split from file blocks would be a guess (SPLIT-24).
- **Duplicates:** 6,355 rows (6.2%). 91.1% of duplicate groups lie within 2,500 file rows. AUC is 0.870 on all test rows and 0.864 without the copied ones. The hidden-group probe found nothing.
- **`HasIDNo`:** 0.874 with, 0.872 without; within-block AUC 0.529. Kept with a note (LEAK-11 fits, because it does not strengthen the signal much).
- **`TotalElectricityBill`:** the facts are those listed under issue 8.
- **Cohort filter:** follows the uploader (LEAK-22).
- **Placeholders:** `PropertyValue` is exactly 1 in 25 rows; `PropertySize` is 10 or less in 5 rows.
- **The quote** "about 20 million records ... PostgreSQL" is not in the Kaggle description.

**Consistency with precedent (precedent checker)**

- **Followed:** this dataset's own SEL-5/LEAK-10 Cases row (label columns); mutual_funds_india `rating` and african_credit_scoring (payments); LEAK-22 diabetes_130_us (cohort); LEAK-18 sepsis_survival, caracas, expresso_churn (duplicates); the 2026-10-12 IID call against maternal_health_risk, set apart because a municipality scores its own accounts; LEAK-11 south_africa_coronary_heart_disease (`HasIDNo`).
- **Departures, each with its distinguishing fact:**
  - Run drop vs ghanas_indigenous_intel: the stretches are located and the remaining data is large (issue 1).
  - Billing keep vs mutual_funds_india and iranian_churn: the residual AUCs are about 0.5 (issue 9).
  - mutual_funds_india pair (`No Good Target`): set apart because its sub-category alone gave R^2 0.776 of 0.783, while here the best single feature gives 0.787 of 0.874.
- **No distinguishing fact yet:** the `TotalElectricityBill` keep. Its stated fact is refuted in part, so it goes back to the curator (issue 8).
- **No drift and no third exception** under LEAK-10 or LEAK-11. If the curator accepts issue 1, it is the first reading of "recovered" as "located"; write it as a Cases row so later datasets follow it.

</details>
