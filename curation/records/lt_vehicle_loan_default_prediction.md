---
unique_name: lt_vehicle_loan_default_prediction
name: LT-Vehicle-Loan-Default-Prediction
checked_by:
- Lennart
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Non-IID (Temporal)
collections:
- TabSTAR
original_source: Website
year: '2019'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46430&sort=runs&status=active
- https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction
- https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/
v2_path: datasets/_dev/tabarena-v0pt2/lt_vehicle_loan_default_prediction/dataset.py
source_row: 624
type_adapter_id: curation-record-v1
---

## Comments

**Assessment (AI, 2026-10-28; direct add/review redo):** Existing Myunghwan final ship and all four task choices preserved. Fresh full-source/typed-frame reconstruction and nine exact split audits pass; 26 native checks report zero errors/warnings. Six meaningful network/location codes remain categorical, with all 233,154 source rows and labels. Fresh nine-window fixed probes use newest 50,000 training rows per window: source AUC means linear 0.640611, forest 0.630847, LightGBM 0.645303, single feature 0.569564, dummy/drift 0.5; no flags. All 54 saved predictions and 90 training-statistic logs independently checked; no native fitted-model replay claimed. Imputation and learned linear encoding are train-side, while category vocabulary is the full released-frame schema and tree probes use numeric codes. This is bounded diagnostic evidence, separate from prior 200k-cap executions and any tuned benchmark. All 49 prescribed maturity-rate cells reproduce, minimum 93.0236%; the short reference remains only approximately stable, not proof of label availability. Full independent panel supports retention with existing timing, borrower-linkage, source-access and short-cohort limits. New source-quality disclosure: 55,227 January-1 birth dates (23.6869%); no unsupported mask. Numerical implementation unchanged; no new curator mark, build, commit, publication or controller work. Priority 3: gap 0 (no thin finance/binary/temporal axis), use case 0 (approximate retrospective fit), source +1 (organizer archive/dictionary), shape +1 (233k mixed-feature temporal rows), risk 0 (no newly demonstrated leak or irreparable defect).

**Current review status (AI, 2026-10-28):** Explicit final ship approved and applied after independent precedent checking. The earlier local mirror-access failure is superseded by successful vote-ranked listing, all six topic metadata/comment responses and top-three notebook source inspection. No new contrary mechanism emerged. Original organizer-forum and mirror opening-post bodies remain unavailable; no exhaustive coverage or new timing clearance is claimed. Closed verification issue 1 on that bounded evidence, without fabricating a human item mark. All prior qualification and limitations remain applicable.

CC (2026-10-28, Myunghwan): "ship for L&T." Final scientific inclusion of the implemented issued-loan first-instalment default task, source ROC AUC and nine temporal tests. Preserve all four prior choices, including no release-end trim, retrospective finalized labels with zero added maturity gap, and supplied bureau predictors under the existing evidence condition. This does not verify bureau timing or historical label availability and does not authorize build, commit or publication.

Unclear how real the data is, but it was a paid competition.

Still looks real and could be used...

**Assessment (AI, 2026-10-23):** L&T Financial Services' original 2019 competition predicts whether an issued vehicle loan misses its first monthly instalment on the due date. One row is a loan/customer record, with borrower, loan-term and credit-bureau information. The [organizer](https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/) specifies `roc_auc` on default probabilities and forbids UniqueID as a predictor; its original dictionary describes many bureau fields as of disbursement. This provides stronger provenance than the older paid-competition rationale (PROV-3/8, MET-1/4).

Recommend keeping it for curator review, advisory priority 3 (base 1 + original source 1 + published shape 1). The observed cohort contains issued loans, so it supports risk estimation for that population; it does not establish performance on rejected applicants. Availability of every input before the chosen decision point, label maturity and calendar coverage still need checking (USE-3/6/8, LEAK-10). These missing checks are not demonstrated leakage and receive no known-risk deduction. Testing later disbursals is a plausible temporal scenario; the source's random public/private split is only within its test set and does not settle train-versus-test construction (SPLIT-1/5/9/10). Inclusion, exact prediction point and split remain pending. Existing verdict and attribution are unchanged; no data qualification or new human approval is claimed.

CC (2026-10-23, Myunghwan): Accepted for adding: score an issued vehicle loan at disbursement for the original binary loan_default outcome, default on its first monthly instalment due date; use the organizer’s ROC AUC. Train on earlier disbursals and test later issued loans ordered by DisbursalDate. Exclude source-forbidden UniqueID. Prediction point and temporal regime are settled. Exact calendar windows, training-label maturity and weakly anchored bureau-field timing remain add-stage checks; do not infer a fixed label lag/due date or fall back to IID. No rejected-applicant generalization is claimed. Screening and curator review are complete; data qualification and later added-dataset review remain.

**Assessment (AI, 2026-10-23):** Builder diagnostics on the original archive counted 233,154 labeled loans (50,611 defaults), disbursed August-October 2018, and 112,392 unlabeled November loans. The first current v2 definition retains the approved task and ROC AUC, excludes UniqueID and the constant mobile flag, restores birth centuries and history durations, and treats documented non-score bureau codes as missing while retaining their reasons (CLEAN-3/5/10/12/14). No labeled feature duplicates were found. Nine four-day chronological diagnostic windows fit the training floor; this is measured calendar feasibility, not label-maturity verification (SPLIT-9/10/14). Dataset check intentionally remains blocked by two timing TODOs (one error, no warnings). Untuned task probes on five provisional windows give mean ROC AUC 0.6524 for LightGBM, 0.6431 for the linear family and 0.6371 for random forest, with no task flags; three sampled leak windows expose no obvious target encoding, which cannot establish input availability (EV-3/7/8). Training-label availability and weakly anchored bureau freeze dates remain unresolved; no fixed lag, IID fallback, rejection, inclusion re-review, tuned qualification or independent panel completion is claimed. See the isolated builder stage reports and local warehouse for exact inputs, split scopes and ranked draft issues.

**Assessment (AI, 2026-10-23):** Builder self-review found full-frame median filling in the official task probe, not in the dataset definition. A local training-only-imputation rerun on the same five provisional windows gives LightGBM ROC AUC 0.652324 (previous official-convention result 0.652433), with no task flags. Both runs and corrected prediction arrays are retained; these scores do not verify label availability. Source-space reverse comparison preserves every original row and label; independent source-calendar and rank-AUC checks hold. The November-label statement is narrowed to the supplied unlabeled test file; data/split checksum is unchanged. Diagnostic clipping/rounding is disclosed separately from the source ROC AUC. D1/D2 timing gaps and the independent panel remain open. This is builder self-review, not acceptance.

**CC (2026-10-23, Myunghwan):** The observed-rate maturity diagnostic does not indicate release-end right-censoring, so keep the newest labeled cohorts without an added release-end trim. Across 1-, 3-, 7-, 14-, 21- and 28-day windows and all retained history, at end buffers from 0 to 31 days, all 49 recent/default-rate ratios remain at least 90% of the August-September reference; rates rise at the release boundary rather than fall. Preserve the short-history qualification: September is 88.97% of August, so the historical reference is only approximately stable. This decision does not establish when labels would have been available at each historical refit or yet settle the train/test maturity gap.

**CC (2026-10-23, Myunghwan):** Use zero added training-label gap. As with a retrospective fraud outcome, the task asks whether first-instalment default ultimately occurred, regardless of when that label became observable. Temporal eligibility is based on loan disbursal date; earlier-disbursal training rows may use their finalized labels without reconstructing historical label-availability dates. This is an explicit retrospective benchmark approximation, not a claim that every label was operationally available at each historical training cutoff.

**Assessment (AI, 2026-10-24):** Applied the two later curator decisions below the historical builder assessments: keep the newest labeled cohorts without release-end trimming and use finalized first-instalment labels with zero added training-label gap. Earlier maturity holds and the two timing implementation TODOs are superseded. This is retrospective earlier-to-later DisbursalDate evaluation; operational label availability at each historical cutoff is not established. D2 bureau freeze dates/account scope remain unverified, with no demonstrated leakage. Data, labels, features, source ROC AUC and all nine temporal windows are unchanged. Corrected untuned task diagnostics cover the newest five windows (LightGBM mean ROC AUC 0.652324); leak diagnostics cover three sampled windows. Those saved results are reused within their original scope. No new fit, build, independent panel or acceptance is claimed. Current affected validation and remaining limits are recorded in stage-report.md and stage-evidence.json.

**Assessment (AI, 2026-10-24; decision critique):** Compared the final definition and checks with all settled decisions and review criteria. The original first-instalment target, issued-loan/disbursement scope, source ROC AUC, UniqueID exclusion, strictly earlier DisbursalDate training, finalized retrospective labels, zero added gap and no release-end trim remain applied. No operational label-availability claim or active timing TODO was found. Narrowed the blanket PRI/SEC timing sentence to the dictionary's dated account counts/balances/amount totals and preceding-six-month new-account count; other bureau freeze dates and account scope remain unverified (D2), with no demonstrated leakage. The generated decision note now also preserves the curator's short-history qualification: September's default rate was 88.97% of August's, so the August-September reference is only approximately stable. Existing curator comments and valid evidence are preserved. These wording corrections change no data, cleaning, target, metric or split membership; only affected checks are rerun. No model fitting, build, publication, independent panel or system work.

**CC (2026-10-26, Myunghwan):** retain it. Retain the currently supplied bureau predictors, including fields whose exact snapshot timing is not explicitly documented. Some bureau fields have unverified snapshot timing/account scope. No later-populated predictor or concrete leakage mechanism was demonstrated by the completed bounded checks. Retention is not a verification of prediction-time availability. Reopen only if: New concrete source or actual-data evidence demonstrates incompatible field timing or a leakage mechanism. This is not a final ship decision.

**Exception to SPLIT-10 (2026-10-23, Myunghwan):** the accepted task is retrospective earlier-to-later issued-loan cohort evaluation using finalized first-EMI default labels regardless of observation time, with zero added training-label gap. Serves P3 (USE-1): the curator's stated retrospective task, rather than operational historical-refit replay. This does not establish label availability at historical cutoffs or exempt a demonstrated SPLIT-9 shortcut. (superseded 2026-11-04: history: SPLIT-10 was amended on 2026-11-04 and the zero gap is open as Review issue 5) (history since 2026-11-05: Lennart settled issue 5, gap 0 is an application of SPLIT-10 as reworded on 2026-11-05, not an exception; issue 4: the recent rates of shared codes are no SPLIT-9 shortcut)

**Assessment (AI, 2026-10-27):** AI recommends ship for later human added-dataset review; no further dataset changes recommended. Validity: the issued-loan target, original rows/labels and chronological membership hold (USE-1/3/5/8, PROV-3/8, SPLIT-1/14). All four curator choices remain; the retrospective zero-gap choice now has its dataset-specific SPLIT-10 exception, preserving the SPLIT-9 shortcut boundary. Bureau timing, historical label availability and borrower identity remain unverified. Value: separately audited newest-five and older-four untuned diagnostics support modest signal by source ROC AUC (TP-2/5/9, MET-1/2/4); no tuned qualification is claimed. Quality: documented repairs and six unresolved history/age caveats remain, without guessed masking. For the curator: complete PROV-18 scrutiny where access permits. Organizer discussions required login, Kaggle bodies were unreadable and vote-ordered notebook coverage was unverified; this remains cannot-verify. The human added-dataset verdict is still required. Short coverage and incomplete timing/source verification limit the recommendation. Source terms remain release bookkeeping; no build, commit or publication. Priority 3: base 1, gap +0 (no thin domain/type/regime), use case +0 (approximate fit), source +1 (original lender competition and dictionary), shape +1 (substantial mixed-feature temporal sample), risk -0 (no demonstrated likely leak, unclear target or irreparable damage).

**Assessment (AI, 2026-10-26; added-dataset review):** Direct human review prepared from the completed add-stage package, preserving all four prior curator decisions. The new invocation is not a final ship mark. No new dataset or split changes are recommended. The actual outstanding PROV-18 verification is now explicit in REVIEW: fresh public access did not yield readable vote-ordered competition threads/notebooks. Targeted participant source inspection does not complete that coverage. Complete the source scrutiny through readable/authenticated content, then give the final scientific verdict. Retrospective finalized labels, zero added gap, no end trim and evidence-conditioned bureau retention remain settled; source timing and borrower identity limitations are not promoted to passing checks. No build, commit or new model fit.

CC (2026-11-04, Lennart): the use case is the source's approval decision at disbursement, with the issued-loan selection named in `fit_reason` as a gap (USE-8): "follow the recommendation". `PERFORM_CNS.SCORE.DESCRIPTION` stays unordered with a CLEAN-14 note ("keep unordered with the note"). The zero gap was checked ("check it and add gap if needed"): no gap added, see the Assessment; how to record it is open (Review issue 1).

**Assessment (AI, 2026-11-04):** no gap is needed. Untuned LightGBM over the nine windows: ROC AUC 0.6369 with no gap against 0.6202 with a 30-day gap, but only +0.0018 at equal training size, so about 90% of the gain is training size. Recent default rates by supplier, branch, employee or postcode add +0.0026 at equal pool size: a small drift by code, not a row-level link. A 30-day gap would leave 20-53% of the rows for training (SPLIT-14). (superseded 2026-11-04: the panel measured the code-rate part at +0.0026 to +0.0057 ROC AUC, so 'about 90%' overstates it; a 30-day gap meets the 50% floor and costs windows (nine to three), not training size below it)

CC (2026-11-04, Lennart): SPLIT-10 is amended, and the zero gap is an application of it, not an exception: "do (d) but we argue from measurmeent and context taht we dont see this pattern in the data as a problem, the gap is already accounted for by collection or other means and hence iti s fine to do this".

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled. (superseded 2026-11-04: the full review panel ran in a second pass; Review issues 4-7 are open)

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (mediator; data, rows, labels, features, metric, nine windows and gap 0 unchanged; the refuted wording in dataset.py fixed: "nothing through the dealer or staff codes", "about 90% training size", the one-month lag as fact, 41-60%); disputed: SPLIT-9 (recent default rates of shared dealer, branch, employee and postcode codes, +0.0026 to +0.0057 ROC AUC, as a shortcut), SPLIT-10 (application of the amendment or exception; the critic's 30-day gap with three two-day windows); for the curator: issues 4-7. Priority 3: gap 0, use case 0, source +1, shape +1, risk 0 (gap: finance, binary and temporal are not thin among the 107 accepted definitions; use case: the organizer names the underwriting decision, but the fit is approximate, issued loans only and a first-EMI proxy; risk: the open SPLIT-9 question is a small measured effect through shared codes with no row-level link, and the mediator recommends shipping).

**Assessment (AI, 2026-11-04):** text corrections of the second-pass panel applied (Lennart's go-ahead on the review page): the stale lines above carry correction notes, and the `Selection Bias` marker is set (the issued-loan selection, USE-8). The CC of 2026-11-04 that points to 'Review issue 1' means the first PR #33 page; the zero gap is now issues 4 and 5. No data, split, feature or metric change.

CC (2026-11-05, Lennart): the recent default rates of the supplier, branch, employee and postcode codes are not a shortcut, and gap 0 stays with the nine windows (issue 4, A; SPLIT-9 as amended 2026-11-05). They add +0.0026 ROC AUC at equal pool size (up to +0.0057 in other encodings), the size of alfa_battle_2_0_task_2's removed effect, but each code is shared by many borrowers and no borrower recurs, so no test row is linked to its own client's earlier label, and the effect does not grow at the release end. The mechanism goes into SPLIT-9's text and a Cases row, and principles.md's tension row is updated.

CC (2026-11-05, Lennart): gap 0 is an application of SPLIT-10, not an exception (issue 5, B; SPLIT-10 as reworded 2026-11-05: the measurements decide, also where late labels are documented; a fixed outcome horizon removes the selection by the outcome but not the delay). The 2026-10-23 "Exception to SPLIT-10" line is history.

CC (2026-11-05, Lennart): the declared metric (ROC AUC on the default probabilities, the organizer's) is checked and stays as declared.

CC (2026-11-05, Lennart): what sets lt apart from lending_club, home_credit_default_risk, credit_g and give_me_some_credit (Review issue 6, C): "here we know we would want to use more but dont have it, in the others we have the data we want to use": lt's approval decision faces every applicant while the release holds only approved loans, so lt carries `Selection Bias`; the four keep no marker. A USE-8 Cases row.

CC (2026-11-05, Lennart): `Current_pincode_ID` ships as a number (Review issue 7, B, answered (a)): the masking kept the geographic order; +0.0049 ROC AUC over the category on 9 of 9 windows.

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. Second-pass panel after Lennart's PR #33 review of 2026-11-04: ship after changes, with the data,
rows, labels, features, metric, nine windows and gap 0 as they are, unless issue 4 is answered "a shortcut" (re-split)
or issue 7 "numeric" (one dtype). Validity: USE-1 holds (approximate fit); USE-5 holds now that `fit_reason` names the
first-EMI proxy; USE-8 holds once the `Selection Bias` marker is set (the sibling datasets that do not name the
selection are issue 6); LEAK-10 holds (all 116,950 rows without bureau history are 0 on every PRI field); LEAK-24 holds
(labels final at release, the late-October rise is drift, not censoring); SPLIT-14 holds (oldest training side
50.39%); SPLIT-9 and SPLIT-10 are open (issues 4 and 5). Value: TP-2, MET-1, MET-2 and MET-4 hold (ROC AUC 0.65-0.67
against a top private score of 0.673; 961-5,726 defaults per window). Quality: CLEAN-14 for `Current_pincode_ID` is
open (issue 7). Weighed: a real underwriting task with the organizer's labels and metric, and nine windows above the
50% floor (+); a small measured gain from labels a refit would not yet have (+0.0026 to +0.0057 ROC AUC) and a label
lag that is inferred, not documented (-). The text of `dataset.py` was corrected in this pass (the claims the panel
refuted: "nothing through the dealer or staff codes", "about 90% training size", the one-month lag written as fact,
41-60%); no data, split or feature changed. Still to do in the record and the rule files, no decision needed: set the
`Selection Bias` marker (USE-8), mark the 2026-10-23 "Exception to SPLIT-10" line as history, correct this dataset's
row in the SPLIT-10 Cases table, and in the record correct the 2026-11-04 Assessment ("about 90%", "20-53%
(SPLIT-14)"), the pointer to "REVIEW.md issue 1" (now issues 4 and 5) and "review panel (none) ... all are settled".

**Main points:** Is the recent default rate of a dealer or branch a shortcut SPLIT-9 removes (issue 4), and is gap 0
an application of the amended SPLIT-10 or an exception (issue 5)? Also: name the issued-loan selection on four sibling
credit datasets or amend USE-8 (issue 6), and the postcode's dtype (issue 7).

**Issues for Lennart:**

4. **Is the recent default rate of a dealer, branch, employee or postcode a shortcut that the split must remove?**

   * **Problem:**
     - Every window trains on all earlier loans, including the last month's, whose first-instalment outcome a lender
       refitting at the window's start would not yet know (40-60% of each training side)[^split9].
     - Most of what those rows add is training size, but a small part reaches the test window through codes shared by
       many loans: a dealer whose loans of the last weeks defaulted more often gets higher scores in the next days.
     - No borrower recurs, so no test row is linked to its own earlier label, and the question is whether this
       code-level effect is a shortcut that must be removed.
   * **Effect on the task:** Scores sit a little above what a lender's refit would get, and more so for learners that
     build code-level rates. Gap 0 also widens the margin of gradient boosting over logistic regression from 0.0035 to
     0.0079 and flips their order in 3 of 9 windows; the mean order holds.
   * **Experiments:**

     | Measurement (ROC AUC) | Gain | Windows positive |
     |---|---|---|
     | Notes: last-30-day code default rates, at equal training pool size | +0.0026 (0.0005 to 0.0051) | 9 of 9 |
     | Column audit: code rates alone, no other feature (an upper bound) | +0.0052 (-0.0002 to +0.0108) | not reported |
     | Task gamer: code rates from labels 4-34 days old, over the shipped baseline | +0.0057 (-0.0027 to +0.0104) | 8 of 9 |

     The effect does not grow in the newest windows (window 0, the newest: 0.0025 against 0.0028 for the older ones), a
     linear date term changes nothing (0.0025 against 0.0027), and borrowers rebuilt from birth date, postcode and
     bureau fields predict their matched test rows at only 0.517-0.543.
   * **Background:** The rule's own text forbids every training row whose label is not yet known at the prediction
     point, which gap 0 keeps (40-60% of each training side). Only a tension row of the principles narrows it to the
     measurable shortcut, training labels shown to tell a test row's outcome, which is always removed, whatever it
     costs the 50% floor[^tension]. That narrowing was never written into the rule itself.
   * **Consistency:** alfa_battle_2_0_task_2 removed an effect of +0.002 to +0.009, the same size; its mechanism was the
     same client's earlier default (95.1% against 2.3% default after an earlier default). Effect size does not set lt
     apart; only the mechanism does, and no rule text says so yet.
   * **Panel:** The advocate and the critic both accept a Cases row that writes the mechanism down; the critic holds
     that without it this call contradicts the alfa precedent. The mediator recommends A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Not a shortcut: gap 0 (implemented) | nine windows as now; the effect kept and described in the notes as small, through shared codes; a Cases row for the rule (rates over codes shared by many borrowers, no same-client link, no growth at the release end); the tension row's narrowing written into the rule's text | no borrower recurs, so no test row is linked to its own earlier label; the effect does not grow in the newest windows | absolute scores 0.007-0.017 above an operational refit |
     | B | A shortcut: re-split with a 30-day gap | three two-day windows from 26 October (training sides 50.39-56.27%, 31,568 test rows), the only design that keeps the 50% floor[^split14] | no training label a refit would not yet know within 30 days | three windows instead of nine[^split15]; every test row in the 26-31 October month-end and festive peak[^split20]; still short of a lag that may be 1-2 months |

   * **Recommendation:** A, the mediator's call, with the Cases row and the tension row's narrowing written into the
     rule's text. **Decision:** A (not a shortcut) or B (a shortcut, re-split)?

   **Notes for the AI:** on A, add a SPLIT-9 Cases row (rates over codes shared by many borrowers, no same-client
   link, no growth at the release end) and write principles.md's tension-row narrowing into SPLIT-9's text in
   splits.md. On B, re-split with a 30-day gap: three two-day windows from 26 October (training sides 50.39-56.27%,
   31,568 test rows).

   [^split9]: **SPLIT-9** (Must): its own text in splits.md forbids every training row whose label is not yet known at
     the prediction point, which gap 0 keeps (40-60% of each training side).
   [^tension]: principles.md's tension row narrows SPLIT-9 to the measurable shortcut, "training labels shown to tell
     a test row's outcome", which "is always removed, whatever it costs the 50% floor" (SPLIT-14). That narrowing was
     never written into SPLIT-9 itself.
   [^split14]: **SPLIT-14** (Must): every window trains on at least half the rows.
   [^split15]: **SPLIT-15** (Should): as many windows as an IID or grouped task of that size would get folds.
   [^split20]: **SPLIT-20** (Should): what the train side holds is decided from the use case.

   **Resolved (2026-11-05, Lennart):** as implemented. SPLIT-9 is amended: a training label that tells a test row's
   outcome (a row in train because its outcome came early, or a label of the test row's own entity set after its
   prediction point) is removed whatever it costs the floor; rates over codes shared by many entities, with no link to
   the row's own entity and no growth at the release end, fall under SPLIT-10, with their size in the notes. A SPLIT-9
   Cases row for lt (+0.0026 ROC AUC through recent rates of shared codes; no borrower recurs).

5. **Record gap 0 as an application of the amended label-delay rule, or as an exception?**

   * **Problem:**
     - Your CC of 2026-11-04 makes gap 0 an application of the amended label-delay rule[^split10], but read on this
       case the amended text conflicts with itself.
     - Its first sentence sets a gap "where the source or the context documents late labels", and a first-EMI label is
       late by construction, while its "fixed outcome horizon" clause covers completeness at release (every loan has
       its final label, and the unmatured rows are not picked by their outcome), not what a refit knew at a window's
       start.
     - The principles' tension row still prescribes an exception for unmatured labels without a row-level shortcut,
       and the record carries both framings (the 2026-10-23 exception line[^line1023] and the 2026-11-04 CC).
   * **Effect on the task:** Under B nothing. Under A the exception holds only if the lag is 45 days or more; if you
     read it as 30 days, the label-delay rule comes first and the re-split of issue 4 B follows. Either way it decides
     how the rule reads for the next case.
   * **Experiments:** Whether a gap can keep the 50% floor[^floor5] depends on the lag it must cover (the mediator's
     run):

     | Lag | Best design that meets the 50% floor |
     |---|---|
     | 30 days | three two-day windows from 26 October (50.39-56.27%) |
     | 45 days | none (best 38.8%) |
     | 60 days | none (best 29.2%) |

   * **Unknown:** The lag is not documented. The dictionary says only "Payment default in the first EMI on due date";
     "at least about a month" is inferred from "monthly instalment", the lowest rank of evidence[^ev2], and the domain
     practitioner puts it at 1-2 months under fixed EMI dates. So an exception serving the 50% floor holds only on an
     inferred lag of 45 days or more; at 30 days the trade is the label-delay gap against the number of windows, both
     Shoulds, and the label-delay gap comes first[^windows5].
   * **Consistency:** ames_housing and perth_house_prices (month resolution covers the delay) and
     melbourne_housing_market (measured complete) are applications; alfa_battle_2_0_task_2 and lending_club (outcome
     horizons up to 12 and 36 months, the floor) are exceptions; chicago_traffic_crashes (an amendable, unmeasured
     label) got a one-month gap the same day. lt differs from alfa and lending_club by its single due date (so the
     unmatured rows are not selected by their outcome) and by a measured effect with no same-client link (alfa's was
     95.1% against 2.3%).
   * **Link to issue 4:** "A shortcut" there removes the amendment's condition that the measurements show none.
   * **Panel:** The mediator recommends B, because its reason rests on measurements, which outrank an inferred lag;
     the split auditor and the critic prefer A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Exception to the label-delay rule | gap 0 recorded as an exception serving the 50% floor, citing the inferred lag of 45 days or more; the 2026-10-23 line marked as history | follows the principles' tension row as it stands | rests on an inferred lag; the third floor exception after alfa_battle and lending_club, so an amendment proposal follows |
     | B | Application, the amendment reworded (implemented) | gap 0 stays an application (CC 2026-11-04; the notes cite the amendment and say the framing is open here); the amendment reworded so its measured branch wins over the first sentence; it says that a fixed horizon removes selection by outcome but not the delay; the principles' tension row updated; lending_club and alfa re-read against it; the 2026-10-23 line marked as history | its reason rests on measurements, which outrank an inferred lag | until the rewording is done, the amended text and the principles' tension row contradict this reading |

   * **Recommendation:** B, the mediator's call: its reason rests on measurements, which outrank an inferred lag.
     **Decision:** A or B?

   **Notes for the AI:** either way, mark the record's 2026-10-23 "Exception to SPLIT-10" line as history. On A, write
   an Exception to SPLIT-10 serving SPLIT-14 that cites the inferred lag of 45 days or more, and follow it with an
   amendment proposal (third floor exception after alfa_battle_2_0_task_2 and lending_club). On B, reword the SPLIT-10
   amendment so its measured branch wins over the first sentence, say that a fixed horizon removes selection by outcome
   but not the delay, update principles.md's tension row, and re-read lending_club and alfa_battle_2_0_task_2 against
   it.

   [^split10]: **SPLIT-10** (Should; applies SPLIT-9), as amended: a gap of about the label's delay between train and
     test "where the source or the context documents late labels"; no gap under a "fixed outcome horizon" or where the
     measurements show none.
   [^line1023]: The record's line of 2026-10-23 is titled "Exception to SPLIT-10". principles.md's tension row
     prescribes an exception for unmatured labels without a row-level shortcut.
   [^floor5]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^ev2]: **EV-2** (Must): evidence ranks; an inference is its lowest rank.
   [^windows5]: **SPLIT-15** (Should): as many windows as an IID or grouped task of that size would get folds. At 30
     days the trade is SPLIT-10 against SPLIT-15, both Shoulds, and SPLIT-10 comes first.

   **Resolved (2026-11-05, Lennart):** as implemented. SPLIT-10's amendment is reworded: the measurements decide; no gap
   where the collection covers what a gap guards against (a fixed outcome horizon removes the selection by the outcome)
   and the measurements show neither, with the gain of the newest labels at equal training size in the notes. lt's gap 0
   is an application, not an exception; its SPLIT-10 Cases row and the Tensions row are updated, and the 2026-10-23
   exception line is marked history. Read again under the new text, lending_club has no measurement of the shortcut or
   of the newest labels' gain (its exception still stands); alfa_battle_2_0_task_2 reads consistently. Neither is
   relabelled.

6. **Name the issued-loan selection on the sibling credit datasets too, or amend the rule on naming it?**

   * **Problem:**
     - lt follows the fit rule as amended on 2026-10-27[^use8]: `fit_reason` says the model only sees loans L&T
       approved, while the approval decision faces every applicant, and the rule asks for the `Selection Bias` marker.
     - lending_club, home_credit_default_risk and credit_g (fit approximate) and give_me_some_credit (fit direct) have
       the same facts, an approval use case with rows only of granted credit, and do not name the selection.
     - This does not hold lt back, because a precedent that contradicts a rule is flagged, not followed[^consistent].
   * **Effect on the task:** Nothing for lt. On the four siblings a reader takes the fit for an approval decision as
     better than it is.
   * **Background:** Implemented: lt names the selection; the siblings are unchanged. All three options keep lt's
     definition as it is.
   * **Panel:** The advocate prefers C; the mediator leaves the choice to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Reopen the four siblings | lending_club, home_credit_default_risk, credit_g and give_me_some_credit name the selection and set the marker; give_me_some_credit moves to approximate | the siblings follow the rule as lt does | four datasets reopened |
     | B | Amend the rule | the rule says whether accepted-only credit data is a selection the approval setting shares | one answer for every accepted-only credit dataset | the siblings stay as they are until the rule is amended |
     | C | Record what sets lt apart | records the fact that the organizer frames the task as underwriting with rising rejection rates | the advocate's choice; no sibling reopened | lt follows the rule, so it needs no fact that sets it apart and this solves nothing |

   * **Recommendation:** A (the AI): lt follows the rule, and a precedent that contradicts a rule is flagged, not
     followed, so lt needs no fact that sets it apart and C solves nothing. **Decision:** A, B or C?

   **Notes for the AI:** on A, reopen lending_club, home_credit_default_risk, credit_g and give_me_some_credit to name
   the selection in `fit_reason` and set `Selection Bias`; give_me_some_credit's fit moves from direct to approximate.
   On B, amend USE-8. On C, record the fact in lt's record.

   [^use8]: **USE-8** (Must), as amended on 2026-10-27: write how closely the data mirrors the use case, its fit; a
     selection of the rows is named and carries the `Selection Bias` marker.
   [^consistent]: principles.md, "Consistent judgement", cases 1 and 2.

   **Lennart (2026-11-05, change):** Option C: Record what sets lt apart.

   **Consistency check (AI, 2026-11-05):** lt already follows the fit rule (USE-8, a Must, your amendment of
   2026-10-27), so C records a fact for a case that needs none, and lending_club, home_credit_default_risk, credit_g and
   give_me_some_credit (approval use, granted credit only, no marker) keep contradicting a Must. What did you mean?
   - (a) C, with the four records flagged as contradicting USE-8 until they are reopened;
   - (b) A: reopen the four;
   - (c) B: amend USE-8 for credit data that holds only accepted loans.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, change):** we dont need the bias marker here as this is the real data for ther other cases but
   selected subset for this case. In short, here we know we would waant to use more but dont have it, in the others we
   have the data we want to use

   **Resolved (2026-11-05, Lennart):** C. The fact that sets lt apart is recorded (a USE-8 Cases row and a CC line):
   lt's approval decision faces every applicant while the release holds only approved loans, so lt carries `Selection
   Bias`; the four siblings' releases are the data their own use cases use, so they keep no marker.

7. **Type `Current_pincode_ID` as a number, since its masked IDs keep geographic order?**

   * **Problem:**
     - The column holds 6,698 masked postcode IDs, typed categorical, and consecutive IDs share their most common state
       in 99.2% of cases (10.3% when shuffled) and their most common branch in 91.0% (1.6% shuffled).
     - The branch, supplier and employee IDs show no such order, and 0.7-1.3% of test rows carry a postcode not seen in
       training.
     - The typing rule points to numbers for zip code prefixes, whose nearby values are nearby places, and its Cases
       table keeps zip prefixes as numbers[^clean14].
   * **Background:** This is a quality point that does not hold back shipping.
   * **Panel:** The panel makes no recommendation.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Categorical (implemented) | each code its own level | the source calls it a masked ID | nearby postcodes share nothing; a new postcode gets no information |
     | B | Numeric | keeps proximity; a single code can then be isolated only by a tree's splits | keeps the geographic order the masking kept | the source calls it a masked ID; models read an order that is only mostly geographic |

   * **Recommendation:** B (the AI), per the typing rule's zip-prefix clause and its Cases row (the masking kept the
     geographic order). **Decision:** B (numeric), or A (categorical) with a note?

   [^clean14]: **CLEAN-14** (Should): its "zip code prefixes, whose nearby values are nearby places" clause points to
     numeric typing; its Cases table keeps zip prefixes as numbers.

   **Lennart (2026-11-05, change):** Option B: Numeric. Or would it be better to just add some feature based on this and
   keep both, the categorical and the number?

   **Answer (AI, 2026-11-05):** One column, numeric. Shipping the same code twice in two types is a copy (CLEAN-22, as
   the huesken guide positions today), and an encoding derived from it is left to the benchmark (CLEAN-24). As a number,
   a tree can still isolate a single postcode with two splits, so the categorical reading is not lost; as a category,
   the order the masking kept is. A derived feature (say the state a code falls in) would need a mapping the release
   does not give. So B as marked; say "yes" in the note and it is applied.

   **Lennart (2026-11-05, change):** We want a context depdended feature here, what could that be? like a group category
   or so? trees are not the only models so that is not a fair argument A data scientistis in the real world would want
   to handle this somehow more clever

   **Answer (AI, 2026-11-05):** A region built from the postcode order adds nothing; the numeric code is the context
   feature that helps.

   * **Background:**
     - Runs of consecutive postcode IDs that share their most common state give 53 regions (median 9 postcodes each),
   about the states, which already ship as `State_ID`; the branch ships too (`branch_id`).
     - Measured on the 9 shipped windows (untuned LightGBM, ROC AUC): categorical (shipped) 0.6387; numeric only 0.6436
   (+0.0049, paired SE 0.0011, ahead 9 of 9); categorical and the region 0.6381; categorical and the numeric code
   0.6381.
     - For models other than trees, a code with 6,698 levels is a sparse one-hot or an embedding, while the number
   carries the geographic order the masking kept; only LightGBM was measured here.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Numeric only | the code as a number | +0.0049 ROC AUC, 9 of 9 windows; the order the masking kept | the source calls it a masked ID |
     | b | Categorical and numeric | two columns, the code as a category and as a number | each model picks its encoding | no gain measured; the same value twice |
     | c | Categorical and a region | a label-free region from the code order (53 regions) | a group category | no gain measured; repeats `State_ID` |

   * **Recommendation:** a, the measured gain, and the number serves models other than trees as well. **Decision:** a, b
   or c?

   Script: `local-data-warehouse/_runs/2026-11-05_pr33_apply/lt/pincode_region.py`.

   **Lennart (2026-11-05, change):** Agree.

   **Resolved (2026-11-05, Lennart):** (a). `Current_pincode_ID` ships as a number, one column; a CLEAN-14 Cases row;
   `dataset check` clean.

**Review panel:** ship after changes (mediator). Tier full, second pass after Lennart's PR #33 review of 2026-11-04
(claim, column and split auditors, domain practitioner, precedent checker, blind reviewer, task gamer, advocate and
critic with one rebuttal each, mediator). Claims: 26, 19 hold, 4 refuted in part ("nothing through the dealer or
staff codes", "about 90% training size", "not smaller without the codes" for one learner, "an application, not an
exception"), 1 imprecise (41-60%), 2 untested (the one-month lag, the 112,392 November loans); the wording ones are
fixed in `dataset.py`; the record's Assessment and the splits.md row still carry them. Blind review: include with
changes; its main concern is the missing label-maturity gap (its int64 point does not apply, the codes are declared
categorical). Task gamer: best exploit is recent per-code default rates built from not-yet-due training labels,
+0.0057 ROC AUC over the shipped baseline (+0.0117 for the zero gap as a whole); no leak in columns, row order or
copies. Agreed: labels final at release, bureau fields exclude this loan, no row-level link, the text fixes, the
`Selection Bias` marker, the proxy clause. Disputed: whether the code-rate effect is a SPLIT-9 shortcut (issue 4),
application or exception under SPLIT-10 (issue 5), and the critic's 30-day gap with three two-day windows (issues 4
and 5). The mediator's issues 1-4 are issues 4-7 of this file.

<details><summary>Mediator</summary>

**Mediator report: lt_vehicle_loan_default_prediction (second pass, 2026-11-04)**

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes. The data, rows, labels, features, metric, nine windows and gap 0 all stay as they are,
unless the curator answers issue 1 "yes".
Validity: USE-1 holds (approximate fit). USE-5 holds; the proxy gets named. USE-8 holds once the marker is set.
  LEAK-10 holds: all 116,950 no-history rows are 0 on every PRI field, and the bureau-field AUCs are flat by month.
  LEAK-24 holds: the labels are final, and the late-October rise is drift, not censoring.
  SPLIT-9: no row-level link. Whether the code-rate recency effect counts as a shortcut is open (issue 1).
  SPLIT-10: gap 0 under the amendment of 2026-11-04. How to record it is open (issue 2).
  SPLIT-14 holds: 9 windows, the oldest training side is 50.39%.
Value: TP-2, MET-1, MET-2 and MET-4 hold. AUC is 0.65-0.67 against a top private score of 0.673; the dummy scores 0.500
  on 9 of 9 windows; each window has 961-5,726 positives.
Quality: CLEAN-14 for Current_pincode_ID is open (issue 4). PERFORM_CNS.SCORE.DESCRIPTION stays unordered, per the CC.
For the curator: issue 1 (SPLIT-9, Must) and issue 2 (SPLIT-10 framing, a rule-maintenance call).
```

**2. Changes to make now (no decision needed)**

1. **EV-2 / writing.** Replace "nothing through the dealer or staff codes" in `task_summary.split`, `splits_comment` and `_decisions`, and in splits.md:244, with "little: +0.0026 through recent code rates (0.0005-0.0051, 9 of 9 windows), up to about +0.005 by other learners; no row-level link". All four audits and the task gamer refute "nothing".
2. **EV-2.** "About a month" becomes "inferred, at least about a month (monthly instalment); the release gives no due date". No source gives the date: the claim, column and domain audits all checked. Delete dataset.py:107 "No due-date lag is inferred", which contradicts line 106.
3. **SPLIT-14 citation and numbers (my run).**
   - The floor depends on the gap:
     - At a 30-day gap a compliant design exists. Three two-day windows from 26 Oct give training sides of 50.39%, 53.08% and 56.27%, with 31,568 test rows. Three one-day windows give 54.7-57.8%.
     - At 45 days no three-window design meets the floor (best 38.8%). At 60 days the best is 29.2%.
   - So "a 30-day gap would leave 20-53% (SPLIT-14)" is wrong as a reason. State the 30-day and 45-day facts.
   - Further corrections:
     - "41-60%" becomes "40-60%" (measured 40.47-59.55%).
     - "About 90% training size" becomes "recency at equal size +0.0018 to +0.0051 across four learners, 11-44% of the gap's cost".
     - The 0.0019 figure is described as measured "without the codes and the date features".
   - Correct the splits.md:244 row the same way.
4. **USE-8 (Must).** Set `decision_markers: Selection Bias` in the record. The rule says "fit_reason names the selection and the marker stays" (Lennart, 2026-10-27). `fit_reason` already names the selection.
5. **Record.** Mark "Exception to SPLIT-10 (2026-10-23, Myunghwan)" (record line 64) as history, as was done on ames_housing and perth_house_prices. The 2026-11-04 CC supersedes it (newer curator decision). This clears the stale register flags `exception_to_must SPLIT-9` and `exception_to_must USE-1`; the USE-1 flag is a false positive in any case.
6. **SPLIT-20 / SPLIT-12 notes in `splits_comment`.**
   - 55% of test rows fall in the 20-31 Oct festive surge (observed/predicted 1.19-1.36).
   - Every test window starts the day after the newest training labels.
   - Gap 0 widens the margin between learners: 0.0035 becomes 0.0079 (split auditor), and HGB minus logistic changes sign in 3 of 9 windows (claim auditor). The mean order holds.
7. **USE-5 wording, agreed by both sides.**
   - `fit_reason` gets: "the label is a missed first EMI on its due date (21.7%), an early-delinquency proxy for credit loss".
   - `use_case` gets: "at sanction, just before disbursement".
   - The PAR90 figure of about 2% is third-party (EV-2 rank 4), so it does not go in as a fact.
8. **Optional.**
   - MET-1: add the organizer's AUC sentence as a second reference, since the contest page shows no metric in a static fetch.
   - LEAK-10: narrow the D2 caveat with the column auditor's evidence.
   - P7: note the unusual bureau combinations (10,381; 4,266; 2,607 rows) and that `ltv` is on the gross loan while `disbursed_amount` is net.

**3. Issues for the curator, ranked**

**Issue 1. P4, SPLIT-9 (Must): is the entity-level recency effect a "measurable shortcut"?**
- **Problem.** Recent default rates of supplier, branch, employee and postcode predict test outcomes from labels a refit would not have had. The measurements:
  - +0.0026 in the notes (0.0005-0.0051, 9 of 9 windows);
  - at most +0.0052 learner-free (column auditor, an upper bound);
  - +0.0057 over the shipped baseline in the task gamer's encoding (−0.0027 to +0.0104).
- **Why it matters.** principles.md:96 says a measurable shortcut "is always removed, whatever it costs the floor". alfa_battle removed an effect of +0.002 to +0.009, the same size as this one.
- **Effect.** If this is a shortcut, the Must requires a fix. The codes recur in 99.4-100% of test rows, so removing recent same-code rows amounts to a gap. The only floor-compliant fix is the 30-day gap with three two-day windows. That fix:
  - departs from SPLIT-15 (9 windows down to 3);
  - departs from SPLIT-20 (100% of test rows on 26-31 Oct);
  - still falls short of a lag that may be 1-2 months.
- **Advocate's best evidence.** The mechanism differs from alfa's:
  - alfa had a same-client link (95.1% vs 2.3% default after an earlier default);
  - here UniqueID never recurs, and rebuilt borrowers score only 0.517-0.543;
  - the effect does not grow at the release end (window 0: 0.0025 vs 0.0028 in older windows);
  - a linear date term changes nothing (0.0025 vs 0.0027).
- **Critic's best evidence.** The effect matches the literal text "training labels shown to tell a test row's outcome". The gamer's lagged honest version scores 0.6366, below the plain model, so all of the gain comes from unavailable labels. It is the same size as alfa's.
- **My reading.** The rules do not decide this. Effect size does not set the case apart from alfa; only the mechanism does, and that distinction is written nowhere.
- **Decision needed.** Either (a) "no": add a SPLIT-9 Cases row stating the mechanism (rates over shared codes, no same-client link, no growth at the release end). Both sides now accept this row. Or (b) "yes": re-split with the 30-day gap and record the SPLIT-15 and SPLIT-20 departures. I recommend (a).

**Issue 2. P4, SPLIT-10 (Should): record gap 0 as an application of the amendment or as an exception?**
- **Problem.** The amended text conflicts with itself here:
  - "a gap is set where the source or the context documents late labels" applies, since a first-EMI label is late by construction;
  - "a fixed outcome horizon" covers label completeness at release, not availability at a refit;
  - principles.md:96 still prescribes an exception.
- **Settled by my run.** An exception "serving SPLIT-14" holds only if the lag is at least about 45 days, which is inference (EV-2, lowest rank). At 30 days a compliant design exists, so the trade there is SPLIT-10 against SPLIT-15. Both are Shoulds, and SPLIT-10 comes first.
- **Advocate (for the application).**
  - The curator wrote the amendment on this very case.
  - In rule maintenance, an amendment outranks an exception.
  - With a single due date, the unmatured rows are not selected by their outcome, so SPLIT-10's "fast ones" bias does not arise.
  - The application rests on measurements; the exception rests on an inferred lag.
- **Critic (for the exception or a gap).**
  - The first clause applies on the definition's own facts.
  - "The right split against the score" (principles.md:94) follows the application, and the application is a refit without the last month's outcomes.
- **Rule.** Consistency checks, cases 1 and 2.
- **Decision needed.** Either:
  - (b) reword the amendment so that its measured branch wins over the first clause, say that a fixed horizon removes selection by outcome but not the delay itself, and update principles.md:96; or
  - (a) record an exception to SPLIT-10, citing the ≥45-day lag as inference. That would be the third SPLIT-14-floor exception, so an amendment proposal follows.

  This depends on issue 1: "yes" there removes the amendment's "measurements show neither" condition. I recommend (b), because its reason rests on measurements, which outrank inference.

**Issue 3. P3, USE-8 sibling consistency (flag only; it does not block lt).** lt follows USE-8 as amended on 2026-10-27. Four siblings have the same facts but do not name the issued-loan selection: lending_club, home_credit_default_risk and credit_g (approximate) and give_me_some_credit (direct). A precedent that contradicts a rule is flagged, not followed. **Decision:** reopen the siblings, or amend USE-8 to say whether approval-only credit data is a selection the approval setting shares.

**Issue 4. P7, CLEAN-14 (Should): Current_pincode_ID.**
- **Evidence.** The masked IDs keep geographic order. Consecutive IDs share their most common state in 99.2% of cases (10.3% shuffled) and their most common branch in 91.0% (1.6%). Branch, supplier and employee IDs show no such order.
- **Rule.** CLEAN-14's clause "zip code prefixes, whose nearby values are nearby places" points to numeric typing, and "zip prefixes kept as numbers" is a Cases precedent. Against it: the source calls the field a masked ID.
- **Decision.** Type it numeric, or keep it categorical with a note. It does not hold back shipping.

**4. Task gamer's exploits**

| Exploit | Rule | Known? | Gain vs note |
|---|---|---|---|
| #1 Training rows with outcomes not yet due (+0.0117 at a 31-day gap; recency at equal size +0.0051) | SPLIT-10 | Known: "Zero gap" note; the definition has no `Potential leak, kept on purpose:` note | **Differs.** The note says 0.0167 total with about 90% training size; the gamer finds recency is about 44% of the gain. Fixed by change 3 |
| #2 Recent per-entity default rates (+0.0057 over the baseline) | SPLIT-9 | Known (note: +0.0026) | **Differs, about 2x.** Feeds issue 1 |
| #3 Training on rows dated after the test window in `data.parquet` (+0.0044) | SPLIT-11 / harness | New, but kit-only | Not a dataset issue; the container splits exclude these rows |

Day of month, the January-1 birth date, the last digit of `disbursed_amount` and earlier same-entity counts are all known at disbursal: signal, not leaks (LEAK-10).

**5. Agreed facts**

- **Size and target.** 233,154 rows from 2018-08-01 to 2018-10-31; 21.71% defaults. The target is "Payment default in the first EMI on due date", and the release gives no due date.
- **Bureau fields (LEAK-10).** They exclude the current loan: all 116,950 no-history rows are 0 on every PRI field.
- **Labels are final at release.**
  - The organizer scored November loans; the archive is dated 2019-04-10.
  - The October rise (23.5%) shows in every stratum and decile.
  - Month-end excess also appears on mature September labels.
- **Gap measurements.**
  - No gap scores +0.007 to +0.017 above a 30-day gap, depending on the learner.
  - Recency at equal size is +0.0018 to +0.0051 and does not grow in the newest windows.
  - Learner order holds on the mean.
- **No row-level link.** Rebuilt borrowers score 0.517-0.543; position within a day scores 0.496-0.512; the next-row label match is 0.6619 against 0.6601 by chance.
- **Windows.** 40.5-59.6% of each training side is unmatured at a 30-day lag. Each training side ends the day before its window. The oldest training side is 50.39%.
- **Metric.** ROC AUC is the organizer's metric. The ID codes are already declared categorical, so the blind reviewer's int64 point does not apply. The licence is release bookkeeping (selection.md).

**6. Consistency with precedent**

- **SPLIT-10.** No drift.
  - ames_housing and perth_house_prices are set apart by month resolution; melbourne_housing_market by measured completeness.
  - chicago_traffic_crashes (gap set the same day) is set apart by an amendable, unmeasured label.
  - lt differs from alfa_battle_2_0_task_2 and lending_club by its single-date horizon and by having measurements. That holds only if the amendment is clarified (issue 2). Otherwise it is their kind of case, and a third floor exception makes an amendment due.
- **SPLIT-9.** lt departs from alfa_battle's removal of an effect of the same size. The distinguishing fact (the mechanism) is not yet recorded: issue 1.
- **USE-8.** lt follows the rule; the siblings depart from it (issue 3).
- **CLEAN-14 (score description).** Consistent with distribution_transformers' `client_type`; heloc is the contrast, and the second dimension of states sets lt apart.
- **Register.** `amendment_due SPLIT-10` (6 datasets) is stale: it counts three cases that are applications now and one retired dataset.

</details>

<details><summary>Claim audit</summary>

**Claim audit: lt_vehicle_loan_default_prediction (second pass, 2026-11-04)**

**Answer to focus.md.** The zero gap holds up on measurement, but it is not a clean application of the amended SPLIT-10, and two of its written numbers overstate the evidence.

* **The numbers replicate in sign and size with two other learners.** Recency at equal size means a random draw of the no-gap training side, cut to the 30-day-gap side's size, scored against the gap side:
  * LightGBM (the notes' run): +0.0018.
  * Logistic regression on train-side code default rates: +0.0026 (−0.0036 to +0.0088, positive in 8 of 9 windows).
  * sklearn HistGradientBoosting (HGB) on the same inputs: +0.0042 (−0.0025 to +0.0110, positive in 8 of 9).
  * With 7-day and 14-day gaps (logistic), recency adds +0.0012 and +0.0016.
* **The effect does not grow at the release end.** In window 0 (the newest) recency is 0.0025 to 0.0045 across the three learners; the largest values are in windows 7 and 4.
* **"About a month" is not documented.** The dictionary says only "Payment default in the first EMI on due date". The month is inferred from "monthly instalment" (EV-2: inference ranks lowest). The reading does not depend on it, because the 7-day and 14-day gaps give the same picture.
* **The labels are final; the gap is not covered by collection.**
  * The source scored a November test set, so its label snapshot is later than the first instalments of November loans. October's labels are therefore complete.
  * The default rate rises at the end: October's last 7 days 0.2628 against 0.2181 for the rest of October; 31 October alone 0.2965 on 8,826 rows. If unpaid-at-snapshot counted as default, the rate would head toward 100%, which it does not.
  * The newest window's mix is riskier than its training side: no bureau history 58.2% vs 55.4%, bureau score 642 vs 652, loan amount 56.4k vs 54.2k.
  * September also rises in its last 7 days (0.2020 vs 0.1865); August does not.
  * So the rise is drift, not censoring.
  * What collection covers is label completeness: a fixed first-EMI horizon. It does not cover what a refit knew at a window's start: the time column has day resolution and the delay is about 30 days. In ames_housing the month resolution was coarser than the delay; here it is far finer.
* **The +0.0026 from recent code default rates is real but small.** It is positive in all 9 windows (standard error about 0.0005), about 2% of the skill above 0.5, and window 0 is 0.0025.
* **The participant kit shows no within-window labels.** In all 9 splits the training side ends the day before the window starts. In the shipped row order the next-row label match is 0.6619 against 0.6601 by chance, and a row's position within its day scores 0.496–0.512 ROC AUC.
* **The rule fit is weak.** The amended SPLIT-10 opens with "a gap is set where the source or the context documents late labels", and the definition's own notes document 30-day-late labels. The fact pattern is lending_club's: documented late labels, and a gap would break the SPLIT-14 floor (8 of 9 windows below 50%). lending_club was recorded as an exception. principles.md line 96 still says this case "is recorded as an exception".

**Claims**

| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| A1/A4 target is first-EMI default, 21.7% | dataset.py task_summary | dictionary, frame | holds | "Payment default in the first EMI on due date"; 50,611 of 233,154 (0.2171) | USE-5 |
| A3 233,154 rows, Aug–Oct 2018 | task_summary | frame | holds | 2018-08-01 to 2018-10-31, 84 days present, 8 days missing | – |
| A5/B14 PRI/SEC fields as of disbursement, no leak | task_summary, notes | rows with no bureau history; single-feature AUC per window | holds | all 116,950 such rows are 0 on every PRI count, balance and instalment field, so the current loan is not counted; DELINQUENT, OVERDUE and INQUIRIES score 0.504–0.535 per window | LEAK-10 |
| A6/C5/E1 "add little, **nothing** through dealer or staff codes" | task_summary, splits_comment, _decisions | target-rate log; logistic with and without codes | "little" holds; **"nothing" refuted** | recent code rates add +0.0026, positive in 9 of 9; in the logistic model the codes carry 0.0008 of its 0.0026 | SPLIT-9, writing |
| B2 55,227 January-1 birth dates (23.6869%) | notes | count | holds | 55,227 (0.236869) | PROV-13 |
| B7 UniqueID, mobile flag dropped; 39 features become 38 | notes | raw | holds | flag constant; UniqueID unique | CLEAN |
| B9 century repair on 19,866 rows; ages 18.00–69.13 | notes | recompute | holds | 19,866; 18.0–69.13 | PROV-13 |
| B10 six rows history longer than age | notes | recompute | holds | excess 3, 11, 12, 33, 96, 100 months; one AVERAGE.ACCT.AGE +100 | PROV-15 |
| B12 status codes 0, 11, 14–18; 448/61 negative balances | notes | raw | holds | exact sets; 448/61 | CLEAN-3 |
| B16 no copies or borrower linkage across the split | notes | birth date + postcode + employment key (birth dates not 1 January) across each split | holds | 1.0–2.0% of test rows share a key with train; P(default \| earlier default) about 0.28 vs about 0.24 (n=381), mixed by window | SPLIT-9, LEAK-16 |
| B17/C2 9 windows; oldest train 117,490 (50.39%); five-day windows give only 7 | notes, splits_comment | recompute | holds | 9 / 7 / 6 windows for 4, 5, 6 days; windows 6 and 7 hold 3 days of data | SPLIT-14 |
| B19a first EMI due about a month after disbursement | notes, C5 | dictionary, reference page | **untested (inference)** | not in the release; contradicts B18, B20 and CC 2026-10-23 ("do not infer a fixed label lag") | EV-2 |
| B19b 41–60% of each training side unknown at refit | notes | recompute | **imprecise** | 40.47–59.55% | EV-8 |
| B19c no gap +0.0167 (0.009–0.033 per window) | notes | source logs; 2 other learners | holds for LightGBM; learner-specific | logistic +0.0074, HGB +0.0118 | SPLIT-10 |
| B19d/G16 equal-size draw keeps 0.0018; "about 90% training size" | notes, record | logistic, HGB | 0.0018 holds for LightGBM; **"about 90%" refuted as general** | size share 65% (logistic), 64% (HGB); recency 0.0026 and 0.0042 | EV-6, EV-8 |
| B19e without the codes the gain is 0.0039, "not smaller" | notes | logistic, HGB | holds for LightGBM and HGB (0.0055); **refuted for logistic** | 0.0018 < 0.0026 | EV-6 |
| B19f +0.0026 (0.0005–0.0051) from recent code rates | notes | source log | holds | 9 of 9 positive; no trend toward the newest windows | SPLIT-9 |
| B19g daily default rate ranks a window at 0.503–0.530 | notes | day_oracle.csv | holds | 0.5026–0.5301 | – |
| B19h without date features the gain is 0.0019 | notes | fit_level log; logistic | holds, wording | measured without codes **and** dates; logistic without dates 0.0023 vs 0.0026 | writing |
| B19i 30-day gap leaves 20–53% | notes | recompute | holds | 20.38–53.08%, 8 of 9 windows below 50% | SPLIT-14 |
| B20/G7 Oct 23.5% > Aug 21.6% > Sep 19.2%; no censoring | notes, _decisions | monthly, weekly, daily rates | holds | rise at the end; drift (see above) | LEAK-22..26 |
| C1 each window trains on all earlier loans, no gap | splits_comment | max train date per split | holds | equals window start minus 1 day in all 9 | SPLIT-11 |
| F metric roc_auc (origin source) | dataset.py | reference URL; participant README; scorer on 9 folds | holds | reference URL shows no metric in a static fetch; a participant README quotes the organizer: "Submissions are evaluated on area under the ROC curve between the predicted probability and the observed target." Dummy scores 0.500 on 9 of 9 folds; 961–5,726 positives per fold; positive class is Yes (perfect prediction = 1.0) | MET-1, MET-2, MET-3 |
| G5 112,392 unlabeled November loans | record | – | **untested** | test file not in the warehouse | EV-7 |
| G17 zero gap is "an application, not an exception" | record CC 2026-11-04, splits.md:244 | amended rule text, tension row, precedents, register | **refuted as worded** | see focus answer; the 2026-10-23 "Exception to SPLIT-10" line is still in the record and register.json reads it as an exception to SPLIT-9 and USE-1 (flags 11, 18, exception_to_must) | SPLIT-10, principles (consistency 2) |
| Implied: no row-order leak in the shipped frame | – | next-row label match; position within day | holds | 0.6619 vs 0.6601; ROC AUC 0.496–0.512 | LEAK-39 |

**Refuted and untested, ranked**

1. **P4, SPLIT-9 (Must) and SPLIT-10: "add little, nothing through the dealer or staff codes"; "about 90% training size".**
   * **What holds.** The recency effect stays small (0.002–0.004 ROC AUC), so SPLIT-9's measurable-shortcut test is not triggered. There is no row-level link like alfa_battle_2_0_task_2's.
   * **What is wrong.**
     * The size share depends on the learner: 89% for LightGBM, 64–65% for the other two.
     * Some of the gain does run through the codes: +0.0026 by the notes' own target-rate test, 0.0008 in the logistic model.
     * The zero gap favours the more flexible learner. HGB minus logistic is +0.0021 with a 30-day gap (HGB ahead in 5 of 9 windows) and +0.0066 with no gap (9 of 9). The sign flips in 3 of 9 windows, 2 of them through recency alone.
   * **What it changes.** Absolute scores sit 0.007–0.017 above what an operational refit would get. Comparisons between close learners can shift by window.
   * **Mildest remedy:** keep the zero gap and correct the wording. Report recency as "+0.002 to +0.004 at equal size across three learners; 64–89% of the gain is training size", and replace "nothing" with "little (+0.0026 through recent code rates)".
2. **P4, SPLIT-10 consistency: "an application, not an exception" (G17, splits.md:244).**
   * The first clause of the amended rule applies, because the context documents late labels.
   * "Collection covers the delay" holds only as label completeness.
   * principles.md:96 still prescribes an exception for this case, and lending_club was recorded as an exception on the same facts.
   * The stale 2026-10-23 exception line raises two exception-to-Must flags in register.json.
   * **Mildest remedy (curator call):**
     * either (a) record an Exception to SPLIT-10 serving SPLIT-14, as lending_club did;
     * or (b) reword the amendment ("late labels at a fixed outcome horizon, measured without a shortcut and without end selection, need no gap"), then update principles.md:96 and re-read lending_club against it.
     * In either case, mark the 2026-10-23 exception line as superseded.
3. **B19a, "about a month" (untested).** This is inference, and it contradicts B18, B20 and CC 2026-10-23. **Remedy:** "assumed about a month (monthly instalment; the release gives no due date); 7-day and 14-day gaps read the same".
4. **Wording and numbers:**
   * B19b reads "41–60%"; the measured range is 40–60%.
   * B19h should say "without the codes and the disbursal-date features".
   * G5 (112,392 November loans) is untested.
   * F: add the quoted organizer sentence, because the reference URL does not show the metric text in a static fetch (MET-1 itself holds).

Sources:
- [Analytics Vidhya contest page (reference)](https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/)
- [Participant README quoting the evaluation metric](https://github.com/chetanambi/LTFS-Data-Science-FinHack/blob/master/README.md)

</details>

<details><summary>Column audit</summary>

**Column audit: lt_vehicle_loan_default_prediction (column-auditor, 2026-11-04)**

**The focus question (SPLIT-9/10 zero gap).** The zero gap holds on the measurements. Two of its claims are overstated.

- **The labels are final.** The archive members are dated 2019-04-10, 161 days after the last disbursal. The organizer also scored the November-2018 loans on the same first-EMI label, so the October first EMIs had already fallen due when the file was made.
- **The late-October rise in defaults is not censoring.** It appears in every stratum I checked:
  - loans with a bureau history: 0.187 → 0.244;
  - loans without one: 0.228 → 0.258;
  - every LTV band.
  - It is not supplier mix: on the Aug-Sep default rates of their suppliers, late-October loans score 0.199 against 0.204.
  - It coincides with a volume surge of 5,900-8,800 loans per day against 2,000-4,700. This reads as a level shift (festive season, which is my inference). A label not yet due would lower the rate, not raise it.
- **"About a month" is documented nowhere.** The dictionary says only "Payment default in the first EMI on due date". Default rates by day of month form a U in August, September and October alike: higher on the 3rd-10th and 29th-31st, 0.16-0.22 mid-month. That fits a fixed monthly due-date cycle (inference). Under such a cycle the time to the first due date varies with the disbursal day and can approach two months, so even a 30-day gap would not remove every unmatured label.
- **I checked the dealer/staff/postcode channel with a different method.** I used smoothed default rates of the four codes (supplier, branch, employee, postcode), averaged as logits, with no learner.

| gap | full minus gap | equal-size draw minus gap |
|---|---|---|
| 7 days | 0.0034 | 0.0023 (-0.0002..0.0045) |
| 14 days | 0.0064 | 0.0035 (-0.0005..0.0073) |
| 30 days | 0.0125 (0.0076..0.0253) | 0.0052 (-0.0002..0.0108) |

  - The effect does not grow toward the newest windows: 0.0072, 0.0070 and 0.0033 for windows 0-2, with the largest, 0.0108, in window 7.
  - This is an upper bound for the code channel, because no other feature is present. It is consistent with the notes' 0.0026, which was positive in all 9 windows.
  - So "little" is right, but "nothing through the dealer or staff codes" is not.
- **The precedents do not fit.** The amended SPLIT-10 sets a gap "where the source or the context documents late labels". Here the context does document them: the first EMI comes after disbursement, as the notes themselves say. In ames_housing, perth_house_prices and melbourne_housing_market the label is known at the time index. This case ships only through the rule's "fixed outcome horizon" clause, which settles that labels are final at the release, not that they were available when a window's model would have been refit. Whether that is an application of SPLIT-10 or an exception is a question for the curator (consistency check, principles case 1).

**Column table**

| column | meaning (dictionary) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| loan_default | default on first EMI on due date | outcome; final at release | category No/Yes, Yes = event | fine | CLEAN-25, LEAK-24 |
| disbursed_amount | amount disbursed | yes | int; net of deductions (ltv exceeds 100×disbursed/asset by median 2.1 points, 0.29-40.1) | fine | USE-6 |
| asset_cost | asset cost | yes | int | fine | |
| ltv | loan to value | yes | float, 10.03-95 | fine | |
| branch_id | branch of disbursal | yes | category, 82 codes; IDs not geographic (consecutive same state 0.148 vs 0.094 shuffled) | fine | CLEAN-14 |
| supplier_id | dealer | yes | category, 2,953 | fine (recent-label channel above) | CLEAN-14, SPLIT-10 |
| manufacturer_id | manufacturer (Hero, Honda...) | yes | category, 11; no code-to-name map | fine | CLEAN-12 |
| Current_pincode_ID | customer's current pincode, masked | yes ("current" undated, minor) | category, 6,698; **IDs keep geographic order** | question | CLEAN-14 |
| Date.of.Birth | birth date | yes | datetime; 19,866 century repairs verified, ages 18.00-69.13, no break at the 68/69 pivot (3,081/3,147); 1 January is 23.7% of rows against about 0.76% for each other first-of-month, a "day unknown" placeholder; default 25.7% vs 20.5% | fine, already noted | CLEAN-11/12 |
| Employment.Type | Salaried / Self employed | yes | category; 3.29% missing, not linked to outcome (21.5% vs 21.7%) | fine | CLEAN-10 |
| DisbursalDate | disbursal date, time key | yes | datetime; day-of-month U is a real signal known at disbursal | fine | USE-6 |
| State_ID | state of disbursal | yes | category, 22; probe's count_like flag is a false positive | fine | CLEAN-14 |
| Employee_code_ID | employee who logged the disbursal | yes | category, 3,270; code order follows first appearance (Spearman 0.57), a running number | fine | CLEAN-14 |
| Aadhar/PAN/VoterID/Driving/Passport_flag | document shared | yes | 0/1 category, checked to hold only 0 and 1; flags co-occur and stay separate | fine | CLEAN-13/14 |
| PERFORM_CNS.SCORE | bureau score | yes (application pull, below) | float; status codes 0, 11, 14-18 map one-to-one to the No-history/Not-Scored descriptions and become missing; 300 is the floor (all 8,776 M-band rows) | fine | CLEAN-10 |
| PERFORM_CNS.SCORE.DESCRIPTION | bureau band / status | yes | unordered, 20 levels; curator ruling 2026-11-04 (second dimension) | fine | CLEAN-14 |
| PRI.NO.OF/ACTIVE/OVERDUE.ACCTS, PRI.CURRENT.BALANCE, PRI.SANCTIONED/DISBURSED.AMOUNT | own bureau accounts "at the time of disbursement" | yes | int; 448 negative balances; disbursed > sanctioned in 4,266 rows; overdue > active in 2,607 | fine (unusual, not impossible) | CLEAN-11 |
| SEC.* (same six) | accounts as co-applicant or guarantor | yes | int; 61 negative; 175; 324 | fine | CLEAN-11 |
| PRIMARY.INSTAL.AMT, SEC.INSTAL.AMT | EMI of bureau loans (0 for every no-history row, so not this loan) | yes | int; PRIMARY > 0 with zero active accounts in 10,381 rows | fine, no note yet | CLEAN-11 |
| NEW.ACCTS.IN.LAST.SIX.MONTHS | new loans in the 6 months before disbursal | yes | int | fine | |
| DELINQUENT.ACCTS.IN.LAST.SIX.MONTHS | loans defaulted in last 6 months (undated) | yes (measured, below) | int; 0 for all 115,792 rows with zero accounts | fine | LEAK-10 |
| AVERAGE.ACCT.AGE, CREDIT.HISTORY.LENGTH | "average loan tenure", "time since first loan" | yes (inferred) | int months, parsed losslessly; 6 rows with history longer than age, kept with a note | fine | CLEAN-11 |
| NO.OF_INQUIRIES | loan enquiries (undated) | yes (measured) | int; 94.1% zero among no-history rows, so L&T's own enquiry is not counted | fine | LEAK-10 |
| UniqueID (dropped) | customer id | n/a | a sequence in disbursal order (Spearman 0.9998); within-day rank AUC 0.503 | drop is right | organizer, CLEAN-3 |
| MobileNo_Avl_Flag (dropped) | mobile shared | n/a | constant 1 | drop is right | CLEAN-5 |

**Problems, ranked**

1. **P4, SPLIT-10 (Should), a question for the curator.** This is the gap above. Mildest remedy: keep the zero gap and fix the wording in `task_summary.split`, `splits_comment` and `_decisions` from "nothing through the dealer or staff codes" to "little: 0.003-0.005 ROC AUC through the dealer, branch, staff and postcode codes". Mark "about a month" as an inference. Then let the curator decide whether this is an application or an exception.
2. **P4, LEAK-10 (Must): it holds, and the D2 caveat can be narrowed.** The bureau record predates this loan:
   - All 116,950 no-history rows have zero primary accounts, balance, instalment and overdue counts.
   - 99.05% of them have zero history length, and 94.1% have zero enquiries.
   - That includes the 10,665 loans disbursed before 15 August, whose L&T account would show in any pull made after the loan was first reported, and the release postdates November's first EMIs.
   - The single-feature AUCs of the overdue and delinquency fields stay flat by month (0.516/0.518/0.522 and 0.511/0.513/0.514), where a later snapshot would inflate them for the older loans.

   Remedy: none in the data. Optionally replace "unverified (D2)" with this evidence. It remains an inference, since L&T's own trade line could in principle be suppressed.
3. **P4, LEAK-24 (Must): it holds.** The labels are final and the end of the release rises rather than falls. The notes' explanation (October 23.5% against August and September) is right; the stratified evidence above could be added.
4. **P7, CLEAN-14 (Should), a question for the curator about Current_pincode_ID.** The masked IDs keep pincode order:
   - consecutive IDs share their most common state in 99.2% of cases (10.3% shuffled) and their most common branch in 91.0% (1.6% shuffled);
   - branch, supplier and employee IDs do not.

   This is the rule's "zip code prefixes, whose nearby values are nearby places" case, decided from context and not from model runs. 0.7-1.3% of test rows carry a pincode not seen in training. Remedy: type it numeric (keeps identity and proximity), or keep it categorical with a note.
5. **P7, notes (Weigh), optional.** Note the unusual bureau combinations: instalment amount above 0 with no active accounts (10,381 rows), disbursed above sanctioned (4,266), overdue above active (2,607). Also note that `ltv` uses the gross loan while `disbursed_amount` is net. None of these needs a fix.

**Not problems**

- **Raw row order (probe 10 flag).** It comes from branch and employee clustering: 97.9% and 98.6% of consecutive raw rows share the branch and the employee. Same-branch pairs match labels at 0.6715 against 0.6608 for different-branch pairs. The shipped frame is shuffled within each day: 2.6% same branch in consecutive rows, next-row match 0.662 against 0.660 chance.
- **The dtype probe's 7 flags.** Each is answered in the table: the five ID codes and State_ID are categorical by meaning, the score description by the curator's ruling, and Current_pincode_ID is item 4.

</details>

<details><summary>Split audit</summary>

**Split audit: lt_vehicle_loan_default_prediction (split-auditor, 2026-11-04)**

**Verdict: right with notes.** The temporal regime, the nine four-day windows and the zero gap all hold. SPLIT-9 is met: I found no row-level shortcut. A gap the length of the label delay would break SPLIT-14 (a Must) in 8 of 9 windows. The weak points are elsewhere:
- The headline numbers behind the zero gap come from the weakest learner, so they understate the recency effect by about half.
- The definition says the codes add "nothing", but its own notes measure +0.0026.
- The case fits the amended SPLIT-10 text badly. Its facts are those of lending_club and alfa_battle_2_0_task_2, which were recorded as exceptions.

**Focus question, answered directly.** No gap is needed, but not for the stated reason. Collection does not cover the delay here. DisbursalDate has day resolution, about 30 times finer than the delay. A fixed first-EMI horizon makes the label final at release, not known at a refit. And the measurements do show a gain from recent labels, about 0.003-0.004 ROC AUC: small, mostly diffuse drift, not a row-level link. What actually justifies gap 0 is the tension row at principles.md:96: the diffuse unmatured rest goes under SPLIT-10 (a Should), departed from for SPLIT-14's 50% floor.

**Numbers (independent, loaded through dataset_io)**

Window facts reproduce:
- The share of each training side disbursed within 30 days of the window start is 40.5-59.6% (claim: 41-60%).
- A 30-day gap leaves 20.4-53.1% of the rows for training (claim: 20-53%).
- A 14-day gap leaves 35-67% (6 of 9 windows clear the floor); a 7-day gap leaves 42-74% (7 of 9).
- The oldest window trains on 117,490 rows (50.4%). Test windows hold 4,402-23,133 rows, with at least about 960 positives each.

Gap comparison, mean over 9 windows. "Size" is the no-gap score minus the 30-day-gap score. "Recency" is a random draw of the no-gap side at the gap side's size, minus the gap score.

| learner | no gap | gap30 | no gap − gap30 | recency (equal size) | recency share |
|---|---|---|---|---|---|
| notes: LightGBM, native high-cardinality codes | 0.6369 | 0.6202 | 0.0167 | 0.0018 | 11% |
| notes: LightGBM, no codes | 0.6535 | 0.6429 | 0.0106 | 0.0039 | 37% |
| mine: LightGBM + out-of-fold code default rates (2 seeds) | **0.6657** | 0.6540 | 0.0116 | **0.0042** (−0.003 to +0.015) | 36% |
| mine: logistic + code rates (3 seeds) | 0.6578 | 0.6505 | 0.0073 | **0.0025** (−0.003 to +0.006) | 34% |
| mine: logistic, no codes | 0.6373 | 0.6353 | 0.0020 | 0.0015 | 75% |
| mine: logistic + linear date | 0.6579 | 0.6504 | 0.0075 | 0.0027 | 36% |

Shorter gaps (logistic): 7 days costs 0.0020 in total, 0.0012 of it recency; 14 days costs 0.0035, 0.0017 of it recency. LightGBM at 14 days: 0.0035 and 0.0005.

**Ranked problems**

**1. P4, SPLIT-10 (Should) / EV-2: the evidence understates the recency effect, and the definition contradicts its own numbers.**

The +0.0018, "about 90% training size" and the splits.md row 244 all rest on a LightGBM whose native high-cardinality categories overfit. That model scores 0.017-0.03 below the same learner without codes.

On learners that handle the codes, recency at equal size is 0.0025-0.0042, about a third of the gap's cost. It is positive in 8 of 9 windows for the logistic model. Two things show it is drift, not a shortcut:
- It does not grow in the newest windows. Logistic: windows 0-2 give 0.0038/0.0040/0.0020 against an older mean of 0.0022. The notes' code-rate effect: 0.0025/0.0026/0.0009 against 0.0028.
- A linear date term changes nothing (0.0025 against 0.0027).

The effect is about a third to a half of the per-window AUC standard deviation (0.0085).

The codes do carry part of it:
- the logistic recency effect is 0.0025 with code rates and 0.0015 without;
- the notes themselves measure +0.0026 through code rates (0.0005-0.0051, all 9 windows positive).

So "nothing through the dealer or staff codes" in `task_summary.split`, `splits_comment` and `_decisions` is wrong. It should say "little".

Effect on model comparison: the margin between my two sound learners (gradient boosting over logistic) is 0.0079 with no gap and 0.0035 with a 30-day gap. The order holds in 9/9 windows with no gap and 8/9 with the gap, so zero gap more than doubles a real model margin without reordering.

The notes' LightGBM also shows date features costing the gap model 0.0026 but the no-gap model only 0.0006. That is the SPLIT-10 "time as a number" bias at about 0.002, hidden by gap 0.

**Remedy: keep gap 0 and correct the text.**
- Recency drift is about 0.003-0.004 ROC AUC, about 35% of the 30-day gap's cost.
- Codes carry 0.001-0.003 of it.
- No row-level link, no growth in the newest windows.
- Change the splits.md Cases row to match.

A 7- or 14-day gap is not a fix: it does not simulate a delay of about 30 days and it drops windows below the floor.

**2. P4, SPLIT-10 amendment against precedent: a consistency call for the curator (principles.md, "Consistent judgement" cases 1 and 2).**

The amended text (splits.md:88-93) says to set a gap "where the source or the context documents late labels". A first-EMI outcome is late by construction. It allows no gap "where the collection already covers the delay (the time column's resolution, a fixed outcome horizon)". Neither applies here: the resolution is daily, and the fixed horizon matures the label at release, not at a refit.

The precedents differ:
- ames_housing, perth_house_prices and melbourne_housing_market are applications because their month resolution or measured recording covers the delay.
- lt has the facts of lending_club and alfa_battle_2_0_task_2: no outcome dates, a gap that breaks SPLIT-14. Both were recorded as exceptions serving SPLIT-14, and principles.md:96 prescribes that.

The record also carries both framings: "Exception to SPLIT-10 (2026-10-23, Myunghwan)" and the 2026-11-04 "application" CC.

Options for the curator:
- (a) Record lt as an exception serving SPLIT-14. That makes it the third exception for this reason, which triggers an amendment proposal: "where a gap of the delay would break SPLIT-14, gap 0 with the recency effect measured and any row-level shortcut removed (SPLIT-9)".
- (b) Widen the amendment's wording and principles.md:96 so that lending_club and alfa become applications too.
- (c) Set a gap.

I recommend (a). In every case, remove one of the two framings from the record.

**3. P4, SPLIT-20 / SPLIT-12 (Should): the test windows fall in an atypical season and use a short horizon. Note only.**

- The newest three windows (Oct 20-31) hold 63,762 of 115,664 test rows (55%). They fall in the festive surge: about 5,400-6,400 rows a day against about 2,400 before.
- A fixed logistic model trained on Aug 1-Sep 25 predicts a flat 0.20 there. The observed rate is 0.239 and 0.275 (observed/predicted 1.19 and 1.36).
- The three-month history holds no full season.
- The source's own design is train Aug-Oct, test November: a one-month horizon. The four-day windows are a coverage choice (SPLIT-14/15). Combined with gap 0, they always test within 4 days of the newest labels, the setting most favourable to recency.

The per-window mean weights the surge windows 3/9, so it stays bounded. **Remedy:** state the season and horizon in `splits_comment`. This release cannot fix them.

**4. EV-2: "about a month" is an inference written as fact.**

The source gives no due date. The only basis is "monthly instalment". With fixed monthly EMI dates (my inference; no source documents them), the first due date would fall roughly 1-6 weeks after disbursement. **Remedy:** write "inferred, about a month".

**Other focus questions**

- **Are the newest labels final?** Probably yes, and the end-of-release rise is not a label artefact.
  - Mix-shift does not explain it: the fixed model's predicted rate is flat.
  - The excess appears in every risk decile (decile 0: 0.079 to 0.132; decile 9: 0.366 to 0.434), in each of the five largest manufacturers, and for borrowers with and without bureau history.
  - Month-end excess also occurs in September, where labels are surely mature: 0.217 against 0.187 for the rest of the month, while the model predicts 0.205 against 0.202.
  - Ranking holds in the newest weeks: weekly out-of-sample AUC is 0.628-0.641. A random "not yet paid = default" excess of about 7 points would cut it to about 0.60. The excess is more additive than proportional, which explains the mild drop.
  - The organizer scored November-2018 loans in a 2019 contest, so October's outcomes were mature at release. That is an inference; the contest dates are not confirmed.
- **Does the code-rate effect grow in the newest windows?** No (see problem 1).
- **Can the task gamer reach test-window labels?** Not through the split: a window's labels never enter its training indices. The offline kit's `data.parquet` holding every row is a kit matter, not a split matter.
- **Regime:** temporal is right. The use case is approval of new applicants at disbursement. Branch, supplier and employee codes recur in 99.4-100% of test rows, and they are features (SPLIT-4). Borrowers cannot be linked. Exact copies are 0.3% of test rows; near copies seen in train, 0.4%. There is no grouped alternative to run.

Sources (contest context only; none gives a due date):
- [aasu14/AV-LTFS-Data-Science-FinHack-ML-Hackathon](https://github.com/aasu14/AV-LTFS-Data-Science-FinHack-ML-Hackathon)
- [salilmishra23/LTFS_AnalyticsVidhya](https://github.com/salilmishra23/LTFS_AnalyticsVidhya)

</details>

<details><summary>Domain practitioner</summary>

**Domain-practitioner report: lt_vehicle_loan_default_prediction**

I read this as an L&T Finance two-wheeler credit-risk analyst who scores loans at the dealer point. Loan sizes are about INR 40-60k and asset costs 60-100k, so these are two-wheeler loans.

**Direct answer to focus.md (the zero gap)**

**I accept no gap as a benchmark approximation, but two inputs to it are wrong.**

1. **"About a month" is not documented.** I found no due date in the problem statement, the dataset description or the evaluation text. The organizer's wording is only "default ... in the first EMI on the due date". Indian practice puts the first EMI on the lender's next fixed EMI date, or the one after it. Loans disbursed late in the month are pushed later. Two-wheeler loans often collect advance EMIs, which delays the first due instalment further. So 30 days is the lower bound, and the real lag is about 1-2 months plus the bank's bounce-return time.
   - I re-measured the share of each training side that a refit would not yet know, on the full 233,154 rows and the shipped splits:

   | Label lag | Training side not yet known | Training rows left after the gap |
   |---|---|---|
   | 30 days | 40-60% (B19b holds) | 20-53% of all rows (B19i holds) |
   | 45 days | 58-86% | 7-36% |
   | 60 days | 75-100% | 0-23%; the oldest window has no training side |

   - The release covers 92 days, so no realistic gap passes SPLIT-14. The real choice is between gap 0 and no temporal task. That supports gap 0. The notes should give the lag as 1-2 months, with these figures, instead of "about a month".
2. **The labels are final for the newest loans.** The competition ran 13-21 April 2019, and the organizer scored its November test loans with labels. So the extract came after the November loans' first EMIs (about December 2018 to January 2019). Every October loan's first EMI had therefore fallen due. Gaps in collection (censoring) cannot explain the release end.
3. **Why the newest week rises (probe 13: 0.275).** It is a month-end pattern that recurs in every month, amplified by the festive season. It is not loans labelled before they were due. On the full data, the last three days of each month default more than the rest of that month:

   | Month | Last 3 days | Rest of month | Loans in last 3 days |
   |---|---|---|---|
   | Aug | 22.5% | 21.3% | 15,296 |
   | Sep | 21.7% | 18.7% | 11,034 |
   | Oct | 27.5% | 22.6% | 19,052 |

   - 31 Oct alone is 29.6% on 7,584 loans.
   - October volume is 98,364 against 66,788-68,002 in August and September. This is the Navratri-to-Diwali season (Diwali was 7 Nov 2018).
   - Practitioners read month-end disbursals as a sales-target push of weaker loans. This is mix shift, as the focus suspected (B20, E1), and it is a real drift the model has to face.
4. **What "accounted for by collection" covers.** Under the amended SPLIT-10 it holds for censoring: the outcome horizon is fixed and the extract came after it. It does not hold for availability at refit. The lag (30-60 days) is 8-15 times the 4-day window and 30-60 times the daily time column, unlike ames_housing and perth_house_prices, where the delay was shorter than the month resolution. So the case rests only on the amendment's measured branch ("the measurements show neither"). That makes it the same kind of case as melbourne_housing_market. The splits.md row at line 244 should say so.
5. **Dealer rates.** A production dealer or branch early-bounce rate would be computed on matured loans only. The +0.0026 from recent code rates (B19f) is small next to the 0.009-0.033 per-window cost of a 30-day gap. The best single feature is branch_id at 0.570, so code-level risk is real signal. Whether the effect grows in the newest windows is for the split auditor.

**1. Inputs at the moment of prediction**

- **I have them all.** All 38 shipped inputs exist at sanction:
  - Loan terms, and LTV as the lender's own policy output (USE-6).
  - Dealer, branch, employee and postcode codes; date of birth; KYC flags.
  - A CRIF High Mark report pulled at application: "PERFORM" score with A-M risk bands, primary and secondary accounts.
  - The unverified bureau timing (D2) is a low practical risk. The pull happens days before disbursal, and no leak was shown (all features 0.607 against best single 0.570).
- **Missing that I always have:** loan tenure, EMI amount, interest rate, declared income, vehicle model, residence and co-applicant details, field and tele-verification results, NACH mandate status, and repeat-customer history (UniqueID is forbidden and no linkage exists). These cap the AUC at about 0.65 but do not invalidate the task.
- **Wording nit:** approval comes before disbursement (hours to days in two-wheeler lending). "Up for approval at disbursement" in use_case should say "at sanction, just before disbursement".

**2. Target**

It is a proxy. A 21.7% "default" on the first EMI is a bounce on the due date. Industry two-wheeler PAR90 was about 2% (CRIF, December 2017). A bounce includes technical bounces and quick cures. For approval I act on credit loss (60+ or 90+ days past due within 6-12 months on book). The first-EMI bounce is what pre-due-date collection calling acts on. I want a probability, ranked for a cut-off and calibrated for risk-based LTV or pricing. fit_reason does not name this proxy.

**3. Row and test data**

One row is one sanction decision (USE-1). The test windows are the next five weeks of disbursals, including the festive ramp and the month-end surges. That is the drift I meet after deployment. The 4-day refit is finer than practice (scorecards are rebuilt every 6-12 months and monitored monthly). This is harmless, because the expanding windows cover the same five weeks.

**4. Would I use it?**

I would use it as an early-bounce ranking. I trust the out-of-time design and the source-level provenance. I distrust three things:
- the issued-only population, if it is used for approval;
- the bounce label, if it is read as loss;
- an absolute AUC about 0.017 above what a refit with the real lag could reach.

**Fit: approximate (agree)**

The rows, inputs and moment match the dealer-point decision. But the label is a first-EMI bounce rather than loss, only loans L&T approved are seen, and a refit would lack the last 1-2 months of outcomes (USE-5, USE-8).

**Gaps, ranked by how much they change the task**

1. **Issued loans only** for an approval decision: the rejected applicants are never scored (USE-8). This is named in fit_reason.
2. **Target is a bounce-level proxy** (21.7%) for the credit loss that approval acts on (USE-5). **Not named.**
3. **Label lag at refit** of 1-2 months, not "about a month". At 45 days 58-86% of each training side is unknown, and the measured cost at 30 days is +0.0167, mostly training size (SPLIT-9/10/14). It is named, but with the lower-bound lag.
4. **Missing standard underwriting inputs** (listed in section 1). The release cannot fix this.
5. **Unverified bureau freeze dates (D2).** Low practical risk.

**What an expert would change (no edits made)**

- Rewrite B19, C5 and A6 to give the lag as "1-2 months, the next or next-to-next EMI cycle". Add the 45-day and 60-day figures, which show no compliant gap exists.
- Add to B20 and E1:
  - the recurring month-end pattern (+1.2, +3.0 and +5.0 points in August, September and October);
  - that the organizer scored November loans, so October's labels were mature.
- Add to fit_reason: "the label is a missed first EMI on the due date (21.7%), an early-delinquency proxy for credit loss".
- Weigh USE-9 as a curator's call: pre-due-date collection prioritisation of new loans fits both the selection and the label. Against it stands "a use case rephrased only to excuse a gap", since the source frames underwriting ("tightening up of vehicle loan underwriting ... rejection rates"). My view: keep the source's use case and name the proxy.

**Metric: yes**

ROC AUC on probabilities is the organizer's leaderboard metric (MET-4). It is the out-of-time Gini (2·AUC−1) that Indian scorecard teams report. The source fixes no cut-off, cost or k, so none may be invented (MET-6, MET-7). Probabilities are ranked across every cut-off (MET-8). At 21.7% positives there is no case for PR AUC (MET-9). The unit is one loan, and each window holds 961-5,726 defaults (4,402-23,133 loans), so the per-window AUC is stable (MET-2). I would choose the same metric. Only for pricing would I add a calibration check (log loss), and the source does not ask for one.

Rules cited: use_case.md USE-1, USE-5, USE-6, USE-8, USE-9; metrics.md MET-2, MET-4, MET-6 to MET-9; splits.md SPLIT-9, SPLIT-10 (amended), SPLIT-14.

Sources:
- [Analytics Vidhya contest page](https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/)
- [Participant repo quoting the problem statement and AUC metric](https://github.com/chetanambi/LTFS-Data-Science-FinHack/blob/master/README.md)
- [FinHack announcement, 2019](https://groups.google.com/g/ranaresearchgroup/c/ZiTEo7tQ32M)
- [When the first EMI starts after disbursal; month-end pushes it later](https://www.loansjagat.com/loan/emi-start-after-loan-disbursement)
- [First EMI due date after a loan](https://www.loansjagat.com/loan/first-emi-due-date-after-loan)
- [Advance EMI on two-wheeler loans](https://www.bajajfinserv.in/advance-emi-payment-for-bike-loan)
- [CRIF two-wheeler PAR90, December 2017](https://www.business-standard.com/amp/article/pti-stories/two-wheeler-loans-grow-32-pc-in-2017-gujarat-has-highest-npas-118040800441_1.html)
- [CRIF PERFORM score](https://www.crifhighmark.com/credit-information/)
- [CRIF A-M risk bands](https://www.scorekyahua.bank.in/?p=347)

</details>

<details><summary>Precedent check</summary>

**Precedent check: lt_vehicle_loan_default_prediction, decisions of 2026-11-04 (second pass)**

**Direct answer to focus.md (does the amended SPLIT-10 fit, or is it an exception?)**

It fits, but only through the new "a fixed outcome horizon" clause, and this dataset is the only case for that clause. Lennart changed the rule on purpose by choosing option (d) on the PR #33 draft. That is not drift. It does not fit the way ames_housing, perth_house_prices and melbourne_housing_market fit:
- In those three, the label was actually known at each window's start. The delay is shorter than the month resolution, or the weekly sheets were measured complete. SPLIT-9 holds literally.
- Here, 40.5-59.6% of each training side carries first-EMI outcomes that were not yet due at the window's start. The definition's own `fit_reason` says so.
- "The collection already covers the delay" is true only at the release end. The newest cohorts show no censoring (Oct 23.5%, Aug 21.6%, Sep 19.2%). It is not true at each window's start.

On the facts, the case is closer to alfa_battle_2_0_task_2 and lending_club. Two written facts set it apart from them:
- **A fixed one-date outcome.** The dictionary defines `loan_default` as "Payment default in the first EMI on due date". alfa_battle's horizon runs up to 12 months and lending_club's up to 36. So the unmatured rows here are not picked by their outcome; SPLIT-10's "fast ones" bias does not arise.
- **A measurement of the shortcut**, which neither of those cases had.

Neither the source nor the dictionary documents "about a month". It is inferred from "EMI" (a monthly instalment).

**1. Zero gap as an application of amended SPLIT-10 (CC 2026-11-04, Lennart). Verdict: consistent, with stated reasons; four wording and record gaps.**

Precedents, all in `.claude/skills/knowledge-curation/references/splits.md` lines 233-246:

| Case | Date | Call | Fact |
|---|---|---|---|
| brazilian_ecommerce | 2026-10-15 | 1-month gap | measured shortcut |
| house_sales, zillow_prize | 2026-10-20 | gap | documented delay, cheap |
| taxi/ETA sets | 2026-10-21 | 1-day gap wherever any training label ends after the window start | variable durations: unfinished trips are the long ones |
| melbourne_housing_market | 2026-10-21 | no gap | measured complete |
| alfa_battle_2_0_task_2, lending_club | 2026-10-21 / 10-26 | gap 0 as an **exception** | SPLIT-14 floor, variable horizons |
| ames_housing, perth_house_prices | 2026-10-26 | exception, now an application | month resolution |
| chicago_traffic_crashes | **2026-11-04, same curator, same day** | 1-month gap | label "potentially amended later, not a fixed medical follow-up"; not measured; costs about 1% of a training side |

The chicago and taxi decisions differ from this one by facts the amended text names (a variable or amendable label, no measurement), so they are not drift. This was the only decision in this check that replaced an old exception, and it did so deliberately.

Gaps:
- **(a) The rule text conflicts with itself for its own case.** splits.md lines 88-93 say "a gap is set where the source or the context documents late labels". The notes here infer late labels from context ("about a month"), so read literally the first sentence requires a gap. The text should say that the fixed-horizon branch with clean measurements wins over that sentence. It should also say what a fixed horizon covers: no selection by outcome among the unmatured rows, not their availability.
- **(b) The principles.md tension row was not updated** (line 96). It still says the diffuse rest of unmatured labels is "departed from for SPLIT-14's 50% floor and recorded as an exception". SPLIT-9's own text (line 77) also still forbids every training row with an unknown label. The case rests on the tension row's reading of SPLIT-9, which was never written into SPLIT-9 itself. The register flags `exception_to_must SPLIT-9` for this mismatch.
- **(c) The SPLIT-14 citation overstates.** The notes (dataset.py line 106) and the case row (splits.md line 244) cite "20-53%" under SPLIT-14 as a cost. But a 30-day gap with three two-day windows from 26 Oct meets the 50% floor: the cut on 26 Sep is 50.39%, and a 30-day gap leaves 53.08% for the 28 Oct window. The real cost is SPLIT-15 (a Should: nine windows down to three) and a smaller test pool. If the floor is meant as part of the reason, this would be the third floor exception after alfa_battle and lending_club, and an amendment would be due. If it is not, the citation should go.
- **(d) A sentence is stale.** dataset.py line 107 says "No due-date lag is inferred", against line 106's "about a month". This follows Myunghwan's 2026-10-23 CC "do not infer a fixed label lag", which the newer decision supersedes.

**1a. Measured recent-label effect kept (SPLIT-9). Verdict: departs from alfa_battle with a stated reason; reasonable, but not recorded as precedent.**
- alfa_battle (2026-10-21 and 10-26) removed a +0.002 to +0.009 ROC AUC effect: "a shortcut that can be measured is always removed, whatever it costs the floor".
- Here the last-30-day code rates add +0.0026 at equal pool size, between +0.0005 and +0.0051, and positive in all nine windows. It is largest in the older windows (+0.0051 for the 30 Sep window) and +0.0025 in the newest, so it does not grow at the release end.
- The stated fact that sets it apart: a rate over a dealer's, branch's, employee's or postcode's loans, not the same client's earlier label. alfa_battle's mechanism was 95.1% vs 2.3% default after an earlier default. UniqueID never recurs here.
- Two follow-ups:
  - Add a SPLIT-9 Cases row so the next dealer-code case has a threshold or mechanism to cite.
  - "Nothing through the dealer or staff codes" in `task_summary.split`, `splits_comment` and `_decisions` contradicts the notes' own "+0.0026"; "little" matches the measurement.

**2. Approval decision as the use case, issued-loan selection named as a USE-8 gap (CC 2026-11-04, Lennart). Verdict: follows USE-8 (2026-10-27) but departs from like cases without a stated reason; the marker is missing.**
- Siblings with the same facts (an approval use case, rows only of granted credit) do not name the selection:
  - lending_club: approximate, for label maturity only.
  - home_credit_default_risk and credit_g: approximate, for other reasons.
  - give_me_some_credit: **direct**.
  - pakdd_private_label_credit (AI screening, unverified) argues the reverse: "fit direct on approved clients, since only granted credit has a repayment outcome (no `Selection Bias` marker)".
- The draft for issue 2 said lending_club "keeps the approval decision with an approximate fit". That is true, but its `fit_reason` never names the selection.
- USE-8 (use_case.md lines 77-81) and selection.md (line 272) say "the marker stays", but the record has no `decision_markers: Selection Bias`. The AI recommendation the curator followed did not mention the marker.

```text
**Consistency check (AI, 2026-11-04):** your call on lt_vehicle_loan_default_prediction (issued-loan selection
named as a USE-8 gap) differs from lending_club, home_credit_default_risk, credit_g (approximate, selection not
named) and give_me_some_credit (direct), the same facts: an approval use case, rows only of granted credit.
What sets lt_vehicle apart? (a) the organizer frames the task as underwriting with rising rejection rates, so the
selection is documented and shifts across the test windows; recorded as the fact, with the `Selection Bias` marker
set as USE-8 asks; (b) treat lt_vehicle like the siblings (drop the selection from fit_reason; the fit stays
approximate for label and bureau timing); (c) reopen the four siblings to name the selection and set the marker
(give_me_some_credit would move to approximate); (d) amend USE-8 to say whether accepted-only credit data is a
selection the approval setting shares.
```

**3. `PERFORM_CNS.SCORE.DESCRIPTION` unordered with a note (CLEAN-14, CC 2026-11-04). Verdict: consistent.**
- It follows CLEAN-14's "second dimension keeps the column unordered" clause (cleaning_features.md line 161) and distribution_transformers_at_cauca_department's `client_type` (2026-11-01).
- The contrast is heloc (2026-11-01): its bureau scales are ordered, with "no bureau record (-9)" and unknowns set missing. Written facts set this case apart:
  - Of 20 levels, 7 are off-scale states: "No Bureau History" plus six reasoned "Not Scored: ..." states that missing would erase.
  - The band order survives in `PERFORM_CNS.SCORE`.
- Optional: a CLEAN-14 Cases row naming heloc as the contrast.

**4. Record and register state (not curator decisions).**
- The record's `Exception to SPLIT-10 (2026-10-23, Myunghwan)` (line 64) is not marked as history. The ames_housing and perth_house_prices 2026-11-04 CCs say "the line above stays as its history"; this record's CC (line 74) does not.
- Because of that, these register flags are stale and not findings:
  - `exception_to_must SPLIT-9` and `exception_to_must USE-1` on this dataset. The USE-1 one is a false positive: the exception serves USE-1, it does not depart from it.
  - `amendment_due SPLIT-10` (6 datasets): it counts ames_housing, perth_house_prices and lt_vehicle, which are applications now, and house_prices_nominal, which is retired (`No`).
- The record keeps two reasons side by side: "retrospective final labels" (Myunghwan) and "measured, no shortcut" (Lennart). The newer one governs.

**Drift and third exception:** no drift. Lennart's SPLIT-10 line from 2026-10-15 to 2026-11-04 is consistent: a gap where the delay is documented and cheap or is measured to matter, no gap where it is measured clean. No third exception of one reason, unless the floor in 1(c) is counted.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real credit-scoring task with honest features and enough rows and signal to score, but the six ID columns should be declared categorical, and the temporal split should either leave a gap of about one month for the label to mature or say plainly that it does not.

**What the task is.** L&T Finance scores two-wheeler and vehicle loan applications when it decides whether to approve them. The target, per the Kaggle and Analytics Vidhya brief, is "probability of loanee/borrower defaulting on a vehicle loan in the first EMI (Equated Monthly Instalments) on the due date". All feature groups are known at application time: the loan (amount, asset cost, LTV), the borrower (date of birth, employment, ID-proof flags) and the credit bureau record. The values look like small Indian vehicle loans: median disbursed amount is ₹53.8k, median asset cost ₹71k, and LTV is capped at 95. The data is real, not generated, and the use is real.

**Concerns, most serious first**

1. **The temporal split ignores when labels become known (moderate).** The label is first-EMI default, so it is only known 1–2 months after disbursal. The task uses "each test window comes after its training rows" with no gap, so each fold trains on recent loans whose outcome the lender would not yet know. I tested this with nine windows of my own from Sep 1 to Oct 31 (the task's real windows are not given):
   - AUC with no gap: 0.646–0.679.
   - AUC after dropping the last 30 days of training: 0.630–0.650, about 0.005–0.035 lower per window (e.g. 0.6671 vs 0.6302, 0.6457 vs 0.6423).

   This is mild optimism, not leakage. It affects all methods alike, so rankings probably survive. Change: add a 30-day gap between train and test, or record the limitation. The data covers only 84 disbursal days (2018-08-01 to 2018-10-31), so a gap leaves little training data for early windows. Fewer, later windows (from mid-September on) would be fine.

2. **The six ID columns are stored as int64 (moderate, about preparation).** These are `branch_id` (82 levels), `State_ID` (22), `manufacturer_id` (11), `supplier_id` (2,934), `Current_pincode_ID` (6,559) and `Employee_code_ID` (3,261). They are nominal codes, but methods will read them as ordered numbers. They matter:
   - Random-split AUC is 0.6686 with them and 0.6509 without.
   - `Current_pincode_ID` is the second-largest gain feature (9.6%), which partly reflects arbitrary numeric splits.
   - LightGBM scored the same with numeric and categorical coding (0.6686 vs 0.6670), but kNN, linear and neural methods will be hurt by an arbitrary order.

   Change: declare `manufacturer_id`, `State_ID` and `branch_id` as categorical at least. Mark the high-cardinality three as categorical too, so each method chooses its own encoding.

3. **The base rate drifts across test windows (low; worth knowing for metrics).**
   - Monthly default rates: Aug 21.6%, Sep 19.2%, Oct 23.5%.
   - Last week of October: 27.5%; Oct 31 alone: 29.6%, on 7,584 rows in the sample, the largest disbursal day.
   - Disbursals bunch at month-end (sales push) and before the festival season.

   This looks like real seasonal drift, not an artefact. In my windows the test rate ran from 17.6% to 26.3%. AUC is robust to that; log-loss and Brier will mix calibration drift into the comparison. Change: none needed, but prefer AUC, and expect the last window to dominate if windows are size-weighted (25–32k test rows against 7–16k for the others).

4. **The signal is weak, so method differences will be small (low).** LightGBM reaches AUC ≈ 0.65–0.68, in line with the hackathon leaderboard (top scores around 0.67). The task is not trivial: no single feature dominates. Top gains are `ltv` 11%, pincode 10%, CNS description 8% and `disbursed_amount` 8%. Test windows have 7.5k–32k rows, so the AUC standard error is roughly 0.004–0.008, enough to separate methods that differ by about 0.01. It is benchmark-worthy as a realistic "hard, noisy" credit task.

5. **Encoding choices to document (low).**
   - `PERFORM_CNS.SCORE` is NaN for 111,378 rows. That covers all "No Bureau History Available" rows (100,318) and all "Not Scored: …" rows. The raw file holds 0 or small codes there. The information survives in `PERFORM_CNS.SCORE.DESCRIPTION` (20 levels), so NaN is a sensible choice.
   - `AVERAGE.ACCT.AGE` and `CREDIT.HISTORY.LENGTH` were turned from "Xyrs Ymon" strings into months. They are internally consistent: average age never exceeds history length, and there is no history without accounts.
   - `Date.of.Birth` has the right century: 1949–2000, age 18.0–69.1 at disbursal. 23.7% of birth dates are Jan 1, which looks like approximate dates on ID documents and is plausible.
   - Dates are kept as datetime. Age is only implicit, so methods that cannot handle datetimes need a numeric conversion. Derived age is the 7th most important feature.
   - `Employment.Type` is missing in 3.3% of rows; this is in the raw data, and the default rate there (21.2%) is unremarkable.
   - `UniqueID` and the constant `MobileNo_Avl_Flag` were dropped correctly. 39 columns remain, matching the raw 41 minus those two.

6. **Raw-data oddities (very low).** `PRI.SANCTIONED.AMOUNT` reaches 1e9, and there are 376 negative `PRI.CURRENT.BALANCE` values and 57 negative `SEC.CURRENT.BALANCE` values. These are typical bureau-feed noise; leave them as they are.

7. **Licence is unclear (process).** Kaggle lists "Other (specified in description)", but the description states no licence. OpenML says "Public". The data is a third-party re-upload of Analytics Vidhya hackathon data. Check redistribution terms before shipping the data itself.

**Leakage and copies.** No column appears to be known only after the decision; all bureau fields describe the borrower's record before this loan. There are 0 exact duplicate rows and 0 duplicate feature vectors. A proxy for repeat borrowers (same birth date, pincode, CNS score, number of accounts and history length, among borrowers with bureau history) matched only 57 rows, so repeat customers across train and test look negligible.

**What I could not check**
- The task's actual nine window boundaries and whether any gap is applied; task.md gives neither.
- The official `data_dictionary.csv` itself; I only saw secondary quotes of it.
- Whether the bureau pull happened strictly before disbursal, and whether active-account counts could include the new loan.
- Customer identity: `UniqueID` is a loan ID, so repeat borrowers are only checked through the proxy above.
- The 33k rows outside the 200k sample, and the exact licence terms of the Analytics Vidhya hackathon.

Sources:
- [Kaggle dataset (API metadata)](https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction)
- [OpenML 46430](https://www.openml.org/search?type=data&id=46430&sort=runs&status=active)
- [Analytics Vidhya LTFS FinHack](https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/)
- [GitHub write-up quoting the target definition and AUC metric](https://github.com/aasu14/AV-LTFS-Data-Science-FinHack-ML-Hackathon)
- [Another hackathon README](https://github.com/sk48880/LTFS-Data-Science-Finhack---Anlytics-Vidhya/blob/master/README.md)

</details>

<details><summary>Task gamer</summary>

**Verdict:** the task can be gamed only a little. The one real flaw is that the temporal splits have no gap between training and test. Every model, the honest baseline included, trains on loans whose first-EMI outcome was not yet known when the test window opened. That is worth about +0.010 to +0.016 AUC. I found no leak in the columns, formats, row order or copied rows.

The untuned LightGBM baseline on `features()` scores **0.6549** on average (per split 0.6475–0.6735). Adding a column of random numbers moves that mean by between −0.0004 and 0.0000, and single splits by −0.0048 to +0.0032.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Training rows disbursed in the last ~31 days before the test window, whose first EMI was not yet due (the shipped splits include them, so the baseline uses them) | 0.6432 (`features()`, train only on rows ≥31 days before the test start) | 0.6549 (shipped train set) | +0.0117 [+0.0049, +0.0198], 9/9 splits | No | Put a gap of at least 31 days between the end of training and the test window |
| 2 | #1 pushed further: default rates per branch, supplier, employee, pincode, state and manufacturer over the 4–34 days before each row's date, built from those not-yet-due labels | 0.6451 (31-day gap + day of month and age) | 0.6606 | +0.0155 [+0.0042, +0.0270], 9/9; +0.0057 [−0.0027, +0.0104] over the shipped baseline | No | Same gap |
| 3 | Training on every labelled row in `data.parquet` except the test rows, including rows dated after the test window | 0.6553 | 0.6597 | +0.0044 [0.0000, +0.0080], 8/9 | No | A harness issue, not a task issue: give the model only the split's rows |

**Flaws that hurt an honest model:** none found. Every honest subset of the training rows scored below using all of them. For example, the most recent rows, cut to the size of the 31-day-gap set, scored 0.6514 against 0.6553. So the flaw raises scores rather than lowering them.

**Findings**

**#1 Labels not yet known in training.** The target is default on the first EMI, which falls due about a month after disbursal. The windows are 4 days long and training runs up to the day before each window, so roughly the last month of training labels did not exist at the prediction point. Dropping those rows costs 0.0117 AUC on every split (31-day gap) and 0.0163 with a 45-day gap.

About half of the loss is fewer rows and half is recency. A random subsample of the same size scores 0.6483; the most recent rows of that size score 0.6514. With a 15-day gap the gain falls to +0.0061, and 8 of 9 splits are positive.

The mildest fix is to train each split only on rows with `DisbursalDate` ≤ test start − 31 days, or 45 to allow for collection lag. Training sets would then hold about 47k to 124k rows.

**#2 Recent default rates by entity.** Target encodings from labels 4 to 34 days old add +0.0057 over the shipped baseline. That is beyond the noise spread on the mean and positive on 8 of 9 splits. The honest version, with a 35-day lag on a 31-day-gap training set, scores 0.6366, below the plain honest model. So the gain comes entirely from labels a deployed model would not have. The same gap fixes it.

**#3 Rows after the test window.** `data.parquet` holds all 233,154 labelled rows, including those after each window. Training on them adds +0.0044. This only matters if a participant gets the whole file rather than just the split's rows.

**Strong features that are signal, not exploits**
A deployed model has all of these at disbursal:
- **Day of month:** default rises at month end (Oct 31: 0.297; Aug 31: 0.235). With age, it adds +0.002.
- **Earlier loans by the same entity** (customer, employee, branch, supplier or pincode, dated before the row): +0.0023, 9/9 splits.
- **Date of birth recorded as 1 January** (a placeholder, 24% of rows): default rate 0.257 against 0.205.
- **Last digit of `disbursed_amount`:** default rate 0.16 to 0.28 by digit, which looks like the fee and insurance structure of each loan scheme. A model on number formats alone scores 0.563, and 0.540 without these digits.
- **The fee** implied by `ltv`, `asset_cost` and the disbursed amount: no gain (0.6549).

**Attacks that found nothing**
- **Row order:** rows are sorted by date. Position within a date has AUC 0.4996, and consecutive rows agree on the label 0.662 of the time against 0.660 by chance.
- **`UniqueID`** (dropped from the kit): it ranks exactly with the date (Spearman 1.0), and its AUC within a single date is 0.503, so dropping it hid nothing.
- **Exact copies:** none. Only 12 rows are identical once the date is ignored.
- **Customers rebuilt from date of birth, pincode and credit-bureau fields:** 1.1k to 1.5k test rows per split match a training customer. That customer's training label predicts with AUC 0.517 to 0.543 on those rows.
- **Counts over the training and test rows together:**
  - Total counts per entity: +0.0007, within noise.
  - Same-day counts: −0.0009.
  - Later loans by the same customer or entity: −0.0047 on 9 of 9 splits.
  - Daily loan volume: included in the total-counts run.
- **Does the bureau data include the current loan?** No. All 116,950 rows with no bureau history have zero accounts, and the primary sanctioned amount equals `disbursed_amount` in only 3 rows.
- **Format-only model:** 0.563 (see above, signal).
- **Transforms over all rows:** none found. Values are raw, except that a bureau score of 0 became missing and the "yrs/mon" account ages became months.
- **Looking the rows up in the published file:** it would work. The OpenML file holds the same 233,154 rows with the same label rate (0.2171). I did not run the join; this is not ranked.
- **Web search** turned up no leak or "magic feature" thread for this competition. One public solution reports only ordinary engineered features. The top private leaderboard score was 0.673.

**What I could not check**
- **The exact first-EMI date and when default is recorded.** This decides how large the gap should be, and so the size of flaw #1: +0.006 at 15 days, +0.010 at 31, +0.016 at 45.
- **When the bureau data was pulled.** Its structure suggests before disbursal, but the dataset does not say.
- **The competition's own discussion forum** did not show up in my searches.
- **A classifier separating training from test rows:** not run, because `DisbursalDate` separates them trivially.

Sources:
- [OpenML 46430](https://www.openml.org/search?type=data&id=46430)
- [chetanambi LTFS FinHack README](https://raw.githubusercontent.com/chetanambi/LTFS-Data-Science-FinHack/master/README.md)
- [Analytics Vidhya contest page](https://www.analyticsvidhya.com/datahack/contest/ltfs-datascience-finhack-an-online-hackathon/)
- [Kaggle dataset](https://www.kaggle.com/datasets/mamtadhaker/lt-vehicle-loan-default-prediction)

</details>

<details><summary>Advocate</summary>

**Opening brief (advocate): ship `lt_vehicle_loan_default_prediction` as defined, with text fixes**

Proposed record: ship after wording changes. Data, rows, labels, features, metric and the nine splits stay as they are.

**1. Every Must at P4 holds. The zero gap creates no shortcut a model can learn from a row.**
- *Claim.* SPLIT-9 (Must), LEAK-10 (Must) and LEAK-24 (Must) are all met.
- *Evidence on SPLIT-9.* Four agents measured independently.
  - At equal training size, recency adds +0.0018 (LightGBM), +0.0025/0.0026 (logistic), +0.0042 (HGB) and +0.0052 at most (code rates with no other features, an upper bound).
  - The effect does not grow at the release end. Window 0 gets 0.0025–0.0045; the largest values are in windows 4 and 7.
  - A linear date term changes nothing (0.0025 against 0.0027).
  - There is no row-level link. Borrowers rebuilt from birth date, pincode and bureau fields predict at 0.517–0.543 on matched rows. Position within a day scores 0.496–0.512. The next-row label match is 0.6619 against 0.6601 by chance.
  - The task gamer found no leak in columns, format, row order or copies.
- *Evidence on LEAK-10.* All 116,950 no-history rows are 0 on every PRI field, so the current loan is not counted. Overdue and delinquency AUCs are flat by month.
- *Evidence on LEAK-24.* The labels are final. The archive is dated 2019-04-10, and the organizer scored November loans on the same first-EMI label. The October rise appears in every stratum, risk decile and manufacturer, and September shows the same month-end pattern on mature labels. It is drift, not censoring.
- *Why it outranks.* principles.md:96 limits SPLIT-9 to "the measurable shortcut (training labels shown to tell a test row's outcome)". The diffuse recency here is not that. alfa_battle's mechanism (95.1% vs 2.3% default after an earlier default) has no counterpart: UniqueID never recurs.

**2. A gap of the real delay is impossible under SPLIT-14 (Must). The real choice is gap 0 or no temporal task.**
- *Claim.* SPLIT-10 is a Should. Here, setting the gap would break a Must or empty the task.
- *Evidence.*
  - 30-day gap: 20–53% of rows left for training, 8 of 9 windows below the floor.
  - 45-day gap: 7–36%.
  - 60-day gap: 0–23%, and the oldest window has no training side.
  - The domain practitioner and the split auditor both place the realistic lag at 1–2 months (next or next-to-next EMI cycle, advance EMIs).
- *Concession.* The precedent checker found that a 30-day gap with three two-day windows from 26 Oct does meet the floor (50.39% / 53.08%). That design costs SPLIT-15 (nine windows down to three) and most of the test pool. It also only works for a lag no source documents and two agents call a lower bound. At 45 days, that design falls below 50% too.
- *Rule.* SPLIT-14 Must over SPLIT-10 Should (strength). Remedy ladder: keeping the task with a documented departure is milder than exclusion. A 7- or 14-day gap does not simulate the delay and drops windows below the floor (split auditor).

**3. What the gap costs does not distort the comparison the benchmark exists for (P6).**
- *Evidence.*
  - The split auditor's two sound learners keep the same order in 9 of 9 windows with no gap and 8 of 9 with a 30-day gap.
  - The blind reviewer and the task gamer both judge that the inflation "affects all methods alike".
  - Absolute inflation is 0.007–0.017. That is no larger than the 0.0085 window-to-window SD for logistic and 0.0167 for LightGBM, the notes' learner.
  - Value is real: AUC 0.65–0.67 against a top private leaderboard of 0.673, no dominant feature, 961–5,726 positives per window, dummy at 0.500 on 9 of 9 windows.
- *Concession.* The claim auditor found the sign flips between HGB and logistic in 3 of 9 windows. The margin between close learners shrinks (0.0079 to 0.0035), but the mean order holds.
- *Rule.* "The right split against the score": the split follows the application, and a small signal under it is no reason to retire. TP-2 and MET-2 hold.

**4. Application or exception is a question of how to record the call. Either answer keeps the definition unchanged.**
- *Claim.* The curator's 2026-11-04 amendment was deliberate, not drift (precedent checker: "no drift").
- *Evidence.* One fact sets this case apart from alfa_battle (horizon up to 12 months) and lending_club (up to 36): a fixed one-date outcome. SPLIT-10's own "Why" is "the newest training rows are the fast ones". With a single due date, the unmatured rows are not selected by outcome. The bias the rule guards against does not arise; the only date-as-number bias measured is about 0.002.
- *Concession.* The amended text conflicts with itself for this case: its first sentence ("documents late labels") reads literally as requiring a gap. principles.md:96 was not updated. The 2026-10-23 exception line is not marked superseded, which raises stale register flags.
- *Mildest remedy.* A curator call between (a) recording an exception to SPLIT-10 that serves SPLIT-14, or (b) clarifying the amendment ("a fixed outcome horizon removes selection, not availability; where the delay's gap would break SPLIT-14, gap 0 with recency measured") and updating line 96. In both cases, mark the old line as history.
- *Rule.* A newer curator decision beats an older one. In maintenance, an amendment outranks an exception. Neither option touches the data.

**5. The wrong numbers are writing errors (P7 and the writing rules), not validity failures. Fix the text, keep the dataset.**
- *Concessions (all stand):*
  - "nothing through the dealer or staff codes" becomes "little: +0.0026 through recent code rates, 0.001–0.003 across learners";
  - "about a month" becomes "inferred, 1–2 months; the release gives no due date" (EV-2);
  - "41–60%" becomes "40–60%";
  - "about 90% training size" becomes "64–89% depending on the learner; recency +0.002 to +0.004";
  - B19h becomes "without the codes and the date features";
  - remove the stale "No due-date lag is inferred";
  - add the organizer's AUC quote next to the metric reference.
- These sit in `task_summary.split`, `splits_comment`, `_decisions`, the notes and splits.md:244.
- *Why it does not block.* Every agent who replicated the measurement found the same conclusion, small and diffuse. Only the magnitudes in the text are off.

**6. The use case, target and metric hold. The open items are notes and a marker.**
- *Evidence.*
  - USE-1 holds; the practitioner agrees the fit is approximate.
  - MET-1 holds: the organizer's sentence "Submissions are evaluated on area under the ROC curve" is quoted, and it is the out-of-time Gini that Indian scorecard teams report.
- *Concessions.*
  - Add to `fit_reason` that a first-EMI bounce (21.7%) is a proxy for credit loss (USE-5 wording).
  - USE-8 asks for the `Selection Bias` marker, which is missing; add it.
  - The sibling inconsistency the precedent checker raised (lending_club, home_credit_default_risk, credit_g, give_me_some_credit) is a consistency question for the curator about those siblings. It does not decide this dataset: "independent failures are not conflicts" cuts both ways, and naming a real gap is not a defect.

**7. The column concerns are already answered or are P7 notes.**
- The blind reviewer's int64 concern does not apply to the definition. `_feature_types` declares all six ID codes categorical.
- `Current_pincode_ID` keeping geographic order (99.2% of consecutive IDs share a state) is a CLEAN-14 Should at P7. Mildest remedy: keep it categorical with a note, or type it numeric (curator call).
- The unusual bureau combinations need only an optional note.
- The licence is flagged in the definition ("resolve terms before release"), so that is release bookkeeping.
- Gamer exploit #3 (training on all of `data.parquet`) is a matter for the participant kit, not the split.

</details>

<details><summary>Critic</summary>

**Opening brief (opposing): lt_vehicle_loan_default_prediction should not ship as defined. Ship after the changes below. Nothing here is a reason to exclude it.**

The task is real. The metric is the source's own, and no leak was found in the columns, the row order or the copies. My case is about the split's justification, the text, the record and two USE-8 gaps.

**1. P4, SPLIT-10 (Should): the reason given for the zero gap does not hold as written. The departure it hides is a choice between Shoulds.**
- **Problem.** The amended SPLIT-10 (splits.md:88-93) opens: "a gap is set where the source or the context documents late labels". The definition's own note (dataset.py:106) says the first EMI falls due "about a month" after disbursement. The "collection already covers the delay" clause does not fit here:
  - DisbursalDate is daily, so the time resolution does not absorb a delay of about 30 days.
  - The fixed first-EMI horizon makes labels final at release, not known at a refit. 40.5-59.6% of each training side was unknown at its window's start (claim, split and precedent audits).
- **The SPLIT-14 citation is wrong.** The notes say a gap "would leave 20-53% (SPLIT-14)". The same sentence admits that three two-day windows from 26 October fit a 30-day gap. That design meets the Must: oldest train side 50.39%, newest 53.08% (precedent-checker). So at 30 days the zero gap trades SPLIT-10 for SPLIT-15. Both are Shoulds, and SPLIT-10 comes first, so it wins (principles.md, "Conflicts").
- **Effect on the task.**
  - Absolute ROC AUC is +0.0117 (task gamer, 9/9 splits) to +0.0167 (notes) above what an operational refit would get.
  - The recency share alone, at equal training size, is +0.0025 to +0.0042 on learners that handle the codes. That is 8/9 windows positive for logistic, 64-65% size share against the claimed 90% (claim and split auditors).
  - Zero gap more than doubles a real model margin: 0.0079 with no gap against 0.0035 with a 30-day gap. The order holds in 9/9 windows with no gap, 8/9 with the gap (split-auditor).
- **Precedent.** lending_club and alfa_battle_2_0_task_2 have the same facts (documented late labels, no label dates). Both were recorded as exceptions, and principles.md:96 still prescribes that.
- **Remedy (the curator chooses, mildest first):**
  - (a) Keep gap 0 as an **Exception to SPLIT-10 serving SPLIT-14**. That only works if the lag is stated as at least about 45 days, where no compliant design exists: 7-36% of rows left at 45 days, 0-23% at 60 (domain practitioner). That lag is inference (EV-2, rank 5) and must be written as such. This would be the third floor exception, so an amendment proposal follows.
  - (b) Set a 30-day gap with three two-day windows from 26 October. SPLIT-14 holds, and the SPLIT-15 departure is recorded.
  - Under either option, drop "an application, not an exception" and correct the splits.md:244 row.

**2. P4, SPLIT-9 (Must): the amendment's own condition ("the measurements show neither") is not met as written.**
- **Problem.** The last-30-day default rates by supplier, branch, employee and postcode add +0.0026 (0.0005-0.0051), positive in 9/9 windows. The column auditor's learner-free check reaches 0.0052 at 30 days, an upper bound. That is training labels the model could not have had, and they predict test outcomes. principles.md:96 says "a shortcut that can be measured is always removed, whatever it costs the floor". alfa_battle removed an effect of +0.002 to +0.009.
- **The fair distinction exists but is not written into the rule.** These are rates over dealers and branches, not a same-client link (alfa: 95.1% against 2.3%). The effect does not grow at the release end: window 0 is 0.0025, against 0.0028 for the older windows.
- **Remedy.** Add a SPLIT-9 Cases row with that mechanism and a threshold, so the next dealer-code case can cite it. If the curator rejects the distinction, remedy (b) of point 1 removes the effect.

**3. EV-2 (Must) and writing: the definition contradicts its own measurements. Fix the text.**
- "add little, and nothing through the dealer or staff codes" appears in `task_summary.split`, `splits_comment` and `_decisions`. All four audits refute "nothing". Write "little: +0.003 through recent code rates; no row-level link".
- "about 90% training size" holds only for the notes' LightGBM, whose native high-cardinality codes score 0.017-0.03 below the same learner without codes. Report "recency +0.002 to +0.004 at equal size across three learners".
- "about a month" is presented as fact, but no source documents it. Meanwhile line 107 says "No due-date lag is inferred", which is stale (it comes from the 2026-10-23 CC). Write "assumed, about 1-2 months (monthly instalment; the release gives no due date)".
- Minor:
  - "41-60%" should read 40-60%.
  - The 0.0019 figure was measured without the codes *and* without the dates.
  - `splits_comment` should state the season and horizon: 55% of test rows fall in the 20-31 October festive surge (observed/predicted 1.19-1.36), and every test sits within 4 days of the newest labels (SPLIT-12/20, a note).

**4. Consistency (principles, cases 1-2): the record holds two incompatible framings.**
- "Exception to SPLIT-10 (2026-10-23, Myunghwan)" is still in force at record line 64. It sits beside the 2026-11-04 "application" CC.
- register.json therefore flags `exception_to_must SPLIT-9` and `USE-1` on this dataset.
- principles.md:96 was not updated with the amendment.
- **Remedy.** Mark the 2026-10-23 line as history (as was done on ames_housing and perth_house_prices). Make principles.md:96 agree with whichever option point 1 settles on.

**5. P3, USE-8 (Must): the selection is named but the marker is missing, and the siblings are treated otherwise.**
- `fit_reason` names the issued-loan selection, but the record has no `decision_markers: Selection Bias`. use_case.md says "the marker stays" (Lennart, 2026-10-27).
- lending_club, home_credit_default_risk and credit_g (approximate) and give_me_some_credit (direct) do not name the same selection (precedent-checker).
- **Remedy.** Set the marker. Put the precedent-checker's consistency question to the curator: (a) record the fact that sets lt apart, (b) treat lt like its siblings, (c) reopen the siblings, or (d) amend USE-8.

**6. P3, USE-5 and USE-8 (Must): the label is an early-bounce proxy, and `fit_reason` does not say so.**
- The dictionary's label is "Payment default in the first EMI on due date", at 21.7% defaults. Industry two-wheeler PAR90 was about 2% (CRIF, December 2017; a third-party page, EV-2 rank 4, so the gap is indicative, not measured).
- The approval decision acts on credit loss. The label includes technical bounces and quick cures.
- The fit is already approximate, so this needs a note, not a re-target. The organizer chose this label.
- **Remedy.** One clause in `fit_reason`: "the label is a missed first EMI on its due date, an early-delinquency proxy for credit loss". Also change `use_case` to "at sanction, just before disbursement".

**7. P7, CLEAN-14 (Should): `Current_pincode_ID` keeps geographic order.**
- Consecutive IDs share their most common state in 99.2% of cases (10.3% shuffled) and their most common branch in 91.0% (1.6% shuffled). Branch, supplier and employee IDs do not.
- This is the rule's "zip code prefixes, whose nearby values are nearby places" case (cleaning_features.md:186). The precedent "zip prefixes kept as numbers" is in the CLEAN-14 Cases row.
- **Remedy.** The curator decides between typing it numeric and keeping it categorical with a note. This is a quality point, not a reason to hold the dataset.

**Dropped:** the licence (selection.md:311: a licence is no reason and no marker), the blind reviewer's int64 IDs (the definition already declares them categorical), and the harness's `data.parquet` (a kit matter, not the task).

**Judgment record.**
```text
Verdict: ship after changes.
Validity: SPLIT-10 departure mis-framed (point 1); SPLIT-9 distinction unrecorded (point 2); USE-8 marker missing (point 5); USE-5 proxy unnamed (point 6).
Value: holds (MET-1/2/4).
Quality: CLEAN-14 pincode question (point 7).
```

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (advocate): `lt_vehicle_loan_default_prediction`**

The critic and I agree on the verdict: ship after changes, with no reason to exclude. We disagree on one thing only: the critic's remedy 1(b), the 30-day gap with three two-day windows. I dispute that remedy. I concede everything else, and every concession is a text, record or marker change.

**1. SPLIT-10 departure mis-framed: partly conceded, remedy (b) disputed.**
- **Conceded.**
  - Read literally, the first sentence of the amended text ("documents late labels", splits.md:88-89) requires a gap here.
  - "Collection covers the delay" holds only for label completeness. It says nothing about what a refit knew.
  - principles.md:96 still prescribes an exception.
  - Under remedy (a), "an application, not an exception" goes and the splits.md:244 row is corrected. If the curator settles instead by clarifying the amendment, the wording can stay, but line 96 must agree with it.
  - The lag is written as an inference of 1-2 months (EV-2).
- **Disputed: that SPLIT-10 "wins" over SPLIT-15 at 30 days.** That argument assumes a 30-day gap meets SPLIT-10, and it does not.
  - The domain practitioner and the column auditor both put the real lag at 1-2 months, with 30 days as the lower bound. The reasons are the fixed EMI cycle, month-end disbursals pushed to the next cycle, and advance EMIs.
  - The critic's own remedy (a) needs the lag stated at "at least about 45 days". At that lag no design meets SPLIT-14 (Must): 7-36% of rows are left at 45 days, and 0-23% at 60.
  - So (b) breaks SPLIT-15 and still departs from SPLIT-10. It is not a choice between two Shoulds where the earlier one wins; it breaks one Should and only partly meets the other. "Within a file an earlier rule wins" (principles.md:4) does not apply when the earlier rule is not met either.
- **Disputed: (b) is not milder.** It makes the critic's own point 3 worse.
  - All test rows would fall on 26-31 October: month-end and the festive peak. The last three days of October default at 27.5%, and 31 October alone at 29.6%.
  - Today the newest three windows hold 55% of test rows; under (b) it would be 100%. That is the "atypical season" concern (SPLIT-12/20), made total.
  - The cost of not doing (b) is bounded:
    - the zero gap reorders nothing (9/9 windows with no gap, 8/9 with a 30-day gap);
    - the inflation is 0.007-0.017, about the size of the window-to-window SD;
    - under "the right split against the score", a small signal is no reason to change the task.
- **What follows.** Gap 0 stays, with remedy (a) or a clarified amendment, as the curator decides. Remedy (a) makes this the third floor exception after alfa_battle and lending_club, so the amendment proposal the split auditor drafted becomes due. I support that.

**2. SPLIT-9 distinction unrecorded: conceded as a record gap, disputed as a trigger for removal.**
- **Conceded.** No Cases row says that rates over dealers or branches are not a "measurable shortcut". The rule should get one, with the mechanism and a threshold.
- **Disputed: that +0.0026 meets "training labels shown to tell a test row's outcome" (principles.md:96).**
  - The alfa_battle effect it removed was a same-client link: 95.1% default after an earlier default, against 2.3%.
  - Here UniqueID never recurs. Rebuilt borrowers predict at 0.517-0.543 on matched rows.
  - The code-rate effect does not grow at the release end (window 0: 0.0025 against 0.0028 for the older windows). A linear date term changes nothing (0.0025 against 0.0027).
  - Those are the marks of diffuse drift, which line 96 places under SPLIT-10, not SPLIT-9.
  - The fallback, remedy (b), fails for the reasons in point 1.

**3. EV-2 and writing: conceded in full.**
- "nothing" becomes "little: +0.0026 through recent code rates; no row-level link".
- "about 90%" becomes "recency +0.002 to +0.004 at equal size across three learners".
- The lag becomes "assumed 1-2 months; the release gives no due date".
- Remove "No due-date lag is inferred" (dataset.py:107).
- "41-60%" becomes "40-60%".
- 0.0019 is described as measured "without the codes and the date features".
- Add to `splits_comment`: 55% of test rows fall in the 20-31 October surge (observed/predicted 1.19-1.36), and every test window sits within 4 days of the newest labels. This is a SPLIT-12/20 note.

**4. Two framings in the record: conceded.**
- Mark the 2026-10-23 exception line as history, as was done on ames_housing and perth_house_prices.
- That clears the stale `exception_to_must SPLIT-9` and `USE-1` flags. The USE-1 flag was a false positive in any case (precedent checker).
- principles.md:96 follows whichever option point 1 settles on.

**5. USE-8 marker: conceded.**
- Set `decision_markers: Selection Bias`, as use_case.md asks ("the marker stays", Lennart, 2026-10-27).
- Put the sibling question (a)-(d) to the curator. I recommend (a): the organizer frames the task as underwriting with rising rejection rates, so here the selection is documented.
- Under "independent failures are not conflicts", the siblings' gap does not hold this dataset back.

**6. USE-5 proxy: conceded.**
- Add to `fit_reason`: "the label is a missed first EMI on its due date (21.7%), an early-delinquency proxy for credit loss".
- Change `use_case` to "at sanction, just before disbursement".
- The PAR90 comparison (about 2%) is a third-party figure, EV-2 rank 4, so it is indicative only. The fit stays approximate.

**7. CLEAN-14 pincode: conceded as a curator call at P7.**
- Either type it numeric or keep it categorical with a note.
- Either way, it does not hold the dataset back.

**Resulting record.**
```text
Verdict: ship after changes (text, record, marker). Data, rows, labels, features, metric, nine windows, gap 0 unchanged.
Validity: SPLIT-10 framing -> curator: exception serving SPLIT-14 (third; amendment proposal) or clarified amendment;
  SPLIT-9 dealer-rate Cases row; USE-8 marker set; USE-5 proxy named.
Value: holds (MET-1/2/4; AUC 0.65-0.67 vs top private 0.673).
Quality: CLEAN-14 pincode (curator call); writing fixes per point 3.
Disputed: critic's remedy 1(b), the 30-day gap (falls short of the 1-2 month lag, gives up SPLIT-15, and puts all test rows in 26-31 Oct).
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (opposing): lt_vehicle_loan_default_prediction**

The two briefs now agree on the main points. Both say ship after changes, with no change to the data and nothing excluded. We disagree on three things: why gap 0 is allowed, whether gap 0 "affects all methods alike", and whether the code-rate effect needs a SPLIT-9 Cases row.

**Advocate 1: every P4 Must holds, and there is no row-level shortcut.** I concede in part.
- **Conceded.** LEAK-10 holds: all 116,950 no-history rows are 0 on the PRI fields, and the AUCs are flat by month. LEAK-24 holds: the archive is dated 2019-04-10 and the October rise appears in every stratum. There is no row-level link: rebuilt borrowers score 0.517-0.543, row position 0.496-0.512, and UniqueID never recurs.
- **Disputed.** The advocate reads principles.md:96 as limiting SPLIT-9 to "training labels shown to tell a test row's outcome". The recent code rates are exactly that.
  - They are training labels that a refit at the window's start did not have: 40.5-59.6% of each training side.
  - They raise test AUC by +0.0026 at equal pool size, positive in 9/9 windows. The column auditor's learner-free upper bound is 0.0052.
  - The task gamer found the honest version (35-day lag) scores 0.6366, below the plain honest model. So the gain comes entirely from labels a deployed model would not have.
  - alfa_battle removed an effect of +0.002 to +0.009 under the same row: "a shortcut that can be measured is always removed".
- **What I ask.** Not removal. Write the distinction both of us accept (rates over dealer and branch codes, not the same client; no growth at the release end, 0.0025 against 0.0028) into a SPLIT-9 Cases row. Without that row, this call contradicts the text of principles.md:96 and the alfa precedent.

**Advocate 2: a gap of the real delay is impossible under SPLIT-14 (Must).** Disputed.
- The definition states the delay as "about a month" (dataset.py:106). At 30 days a compliant design exists: three two-day windows from 26 October, 50.39% / 53.08%. The advocate concedes this.
- So at the documented delay, SPLIT-14 is not at stake. The trade is SPLIT-10 against SPLIT-15. Both are Shoulds, and "at equal strength the earlier rule wins" (principles.md:75). The "SPLIT-14 Must over SPLIT-10 Should" argument applies only if the lag is put at 45 days or more.
- That lag (1-2 months) is the domain practitioner's inference, EV-2's lowest rank. The advocate's own point 5 wants it written as "inferred". I accept that route: it is my option (a). But then the notes must cite the 45- and 60-day figures (7-36%, 0-23%) as the reason, not "20-53% at 30 days". The current SPLIT-14 citation in dataset.py:106 and splits.md:244 is wrong as written and must change either way.

**Advocate 3: the cost does not distort the comparison (P6).** I concede the conclusion and dispute one claim.
- **Conceded.** No reordering on average: 9/9 windows with no gap, 8/9 with a 30-day gap. A small signal is no reason to retire. Nothing here argues for exclusion.
- **Disputed: "affects all methods alike".** The claim auditor measured HGB minus logistic at +0.0021 with a 30-day gap against +0.0066 with no gap. The sign flips in 3/9 windows, 2 of them through recency alone. The split auditor's margin goes from 0.0035 to 0.0079. The zero gap favours the more flexible learner.
- The row "the right split against the score" says the split follows what the application does. The application here is a refit without the last month's outcomes, so that row argues for the gap, not against it.
- **Remedy (a note).** `splits_comment` states the learner-dependent margin, the festive-season test windows (55% of test rows, observed/predicted 1.19-1.36) and the 4-day horizon (SPLIT-12/20).

**Advocate 4: application or exception is only a question of recording.** I concede almost all of it.
- **Conceded.** The data stays the same under either option. The 2026-10-23 line (record line 64) must be marked as history, and principles.md:96 must be updated.
- **Disputed: "an amendment outranks an exception".** It does not settle this case. The amendment's first clause ("a gap is set where the source or the context documents late labels", splits.md:88-89) applies on the definition's own facts. Its "fixed outcome horizon" branch covers label completeness, not availability at refit. The advocate's own wording proposal says so.
- **What I ask.** If the curator picks the advocate's (b), the amendment text must say that the measured branch wins over the first clause, and row 244 must drop "collection covers the delay". Otherwise the call is an exception (a). Either way the record keeps one framing, not two.

**Advocate 5: the wrong numbers are writing errors.** Conceded.
- I agree they are text fixes, not validity failures. The definition still cannot ship stating "nothing through the dealer or staff codes", because all four audits refute it (EV-2, Must). That is why the verdict is "ship after", which the advocate also says.
- Add the season and horizon note from point 3 to the advocate's list.

**Advocate 6: use case, target and metric hold.** Conceded.
- The marker, the proxy clause in `fit_reason` and the sibling consistency question are agreed.
- I agree the sibling question does not hold lt back. It still goes to the curator as a question (principles, consistency cases 1-2).
- Also change `use_case` to "at sanction, just before disbursement" (domain practitioner). The advocate left this out.

**Advocate 7: column concerns.** Conceded in full: int64 IDs already declared categorical; pincode is a CLEAN-14 curator call; licence and `data.parquet` are not task issues.

**Judgment record after rebuttal**
```text
Verdict: ship after changes; no data change required.
Still disputed: (1) the SPLIT-14 citation at 30 days is wrong; gap 0 rests either on an inferred lag of 45 days or more
(exception to SPLIT-10 serving SPLIT-14) or on a reworded amendment, not on "20-53%";
(2) "affects all methods alike" is refuted (learner margin 0.0035 -> 0.0079, sign flips 3/9), so it needs a note;
(3) the +0.0026 code-rate effect needs a SPLIT-9 Cases row to square with principles.md:96 and alfa_battle.
Agreed: text fixes (EV-2), Selection Bias marker, proxy clause, record line 64 as history, principles.md:96 updated,
pincode CLEAN-14 call.
```

</details>
