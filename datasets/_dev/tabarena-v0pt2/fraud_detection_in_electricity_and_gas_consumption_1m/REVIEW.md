# fraud_detection_in_electricity_and_gas_consumption

**Outcome:** added as `fraud_detection_in_electricity_and_gas_consumption_1m`. STEG's meter-fraud finding per client,
one prediction per client from its invoices before 2013, grouped by client: 81,531 clients, shipped as 1.5 million
invoices of 65,603 clients (review panel, 2026-10-20). The panel's changes are in `dataset.py` and change the data (2,343 clients fewer, `counter_number`
dropped, shifted and impossible values set to missing); not built yet.
Verdict: ship after changes, once LEAK-25 is amended (issue 2).
Validity: USE-1 holds; USE-3 and SPLIT-9 fixed in the wording (a screen of the clients not yet inspected, not a
forecast made in 2013; splits comment added), fit approximate (USE-8); USE-5 noted (a 0 means no fraud was found);
LEAK-10 triggered, fixed (history cut at 2013-01-01, issue 1); LEAK-23 and LEAK-24 triggered, fixed (only clients
still billed from 2015 on); LEAK-25 departed from (early leavers located and dropped, issue 2); SPLIT-1, SPLIT-24 and
SPLIT-29 hold (grouped by client); PROV-9 holds (2019).
Value: no task-probe flag (task probe re-run on the changed definition: per-client ROC AUC 0.633-0.686 across model
families, 158 fraud clients in the smallest test fold; the panel's run before the changes gave 0.62-0.67 and 162).
Quality: CLEAN-19 departed from (invoice rows kept, issue 4); CLEAN-11 and PROV-13 repaired; CLEAN-3 applied (issue 8).
Weighed: none open.
For the curator: issue 2 blocks; issues 1, 4 and 8 confirm what is implemented; the record's year.

**Main points:** Amend LEAK-25 so that dropping the clients whose labels look unrecorded counts as recovering them
(issue 2, blocks); keep the 2013 cut rather than the challenge's full history (issue 1); keep the invoice rows rather
than one row per client (issue 4); confirm the drop of the meter serial (issue 8); the record's year is 2019, the
challenge's first run (the year row).

**Record fields that disagree with the definition:**

- `year`: record `2020`, definition `2019`.

**Record judgment:** valid with concerns. Real utility billing with STEG's per-client findings. The invoices from
2013 on carry traces of the inspections, so the history is cut there (issue 1); the labels are undated, so the task
is a screen of other clients over the same years; clients who left early look unrecorded and are dropped, which the
rule as written does not allow (issue 2).

**Issues for Lennart:**

2. **Amend LEAK-25, so that clients whose labels look unrecorded may be dropped instead of retiring the dataset?**
   - Problem: the label counts STEG's findings up to a client's last invoice. Among the clients billed before 2013,
     those whose last invoice is before 2013 are almost never frauds: 21 of 19,133 (0.11%; at most 0.15% a year up
     to 2011, 0.8% for 2012), against 7.8% for the clients kept. Their findings look unrecorded: "no fraud" is mixed
     with "never recorded". Clients who left in 2013 or 2014 show the same effect on a smaller scale (4.0% and 5.5%
     frauds): they had less time to be found.
   - Effect: kept, these clients are easy negatives that teach a recording artefact (client-level LightGBM with the
     full history, before the cut, not re-measured since: ROC AUC 0.869 with the early leavers, 0.848 without).
   - Implemented: the cohort is the 81,531 clients billed before 2013 and still billed from 2015 on. The 19,133 early
     leavers and the 2,343 clients who left in 2013-2014 (110 frauds, 4.7%) are dropped by their
     last invoice date, never by reading the label. From 2015 to 2019 the yearly fraud rates run 7.1-9.3% with no
     trend (Spearman -0.002, the mediator's test), so 2015 is the mildest cut that ends the step. The filter follows
     LEAK-23 and LEAK-24 (Must: an outcome over the rows followed that long; cirrhosis, sf_permit_time) and changes no
     score (client-level LightGBM 0.699 on all, 0.700 on the kept clients, the mediator's run). Cost: 2.8% of the
     clients; the cohort is chosen on billing after the prediction point, which a note in the definition says: of the
     64,969 clients with an invoice in the second half of 2012 it drops 2,411 (3.4% frauds), 779 of them never billed
     after 2012 (1.3% frauds), against 7.8% for the 62,558 kept.
   - Rule: LEAK-25 (Must) says "no event" mixed with "not recorded" is retired "unless the recording process can be
     recovered". Its one case, ghanas_indigenous_intel (2026-10-01), was retired, but there the unrecorded rows
     could not be located. caracas_cervical_cancer (shipped 2026-10-15) dropped located unrecorded rows the same way,
     and account_debt_south_africa (open, its issue 1) asks for the same reading. A Must allows no exceptions, so this
     is an amendment, and the working copy's REVIEW.md holds it as one item for the three datasets.
   - Alternative: retire the dataset as the rule reads now (the task is lost), which would also reopen caracas.
   - Recommendation: amend LEAK-25 so that "recovered" covers "located by a rule that does not read the label, and
     dropped", with caracas, account_debt and this dataset as its cases. The advocate and the critic agree on the
     reading; the critic holds that it must be settled before the dataset ships.
   - Decision: amend LEAK-25 (decided once, with the cross-dataset item), or retire.
   - LEAK-25 is amended (2026-10-21, Lennart): unrecorded rows located by a rule that does not read the label, and
     dropped, count as recovered, so the drop meets the rule; this issue now needs only the curator's ok on the drop.

1. **Keep the history cut at 2013-01-01, rather than the challenge's full history with a potential-leak note?**
   - Problem: the invoices from 2013 on carry the traces of the inspections that set the labels. Among the 116,360
     clients billed from 2013, the fraud rate of clients whose second electricity meter first appears in a quarter is
     7.4-11.9% in each quarter of 2012 and 23.8-25.9% in each quarter of 2013, while the number of such events per
     quarter does not jump; meter-condition code 5 (`counter_statue`, documented codes 0-5) shows the same step (9.5% in 2012Q4, 23.7% in 2013Q1). 47.8% of the
     frauds carry such a trace. The cut date is read off the data; STEG and Zindi do not document it.
   - Effect: with the full history, a model recognises about half of the frauds by the trace of their own
     inspection: client-level LightGBM scores ROC AUC 0.848 with the full history and 0.688 with the cut (3 folds,
     the kept clients). Moving the cut earlier changes the score little (the claim audit's model: 0.694 at the cut, 0.692 at
     mid-2012, 0.687 at the start of 2012), so no trace piles up before 2013.
   - Implemented: the features are the invoices before 2013 (LEAK-10, Must: a consequence of the target). Cost: it
     is not the challenge's task, and the 2013-2019 invoices are discarded.
   - Alternative: the full history with a `Potential leak, kept on purpose:` note. That is the challenge's task, and
     it follows LEAK-38 (Should: a field of a company's own release that may be recorded after the outcome stays with
     such a note), as kick kept `WheelType` and homesite its `PropertyField37` x `PersonalField12` (Lennart,
     2026-10-01). Cost: half of the frauds are found by the leak.
   - Precedent: LEAK-38's scope is anonymised fields whose timing cannot be verified; here the fields are named meter
     codes with a measured step, which kick and homesite never had. expresso_churn_prediction_1m drops REGION on the
     same fact the same day, and the working copy's REVIEW.md asks whether to amend LEAK-38 for both. The cut follows
     mic (LEAK-10) and hotel_booking_demand (an as-of date).
   - Recommendation: keep the cut; decide the LEAK-38 wording with expresso. This does not block the dataset.
   - Decision: keep the cut, or ship the full history with the note.

4. **Keep the invoice rows (one prediction per client from all its rows), rather than one row per client with
   aggregates?**
   - Problem: CLEAN-19 (Should) asks that a history be turned into one row per prediction, with the per-entity
     summaries (aggregates such as the mean consumption or the number of meters) that the top solutions share.
     alfa_battle_2_0_task_2 (Lennart, 2026-10-13), rosbank1 and home_credit_default_risk follow it; amex_non_iid_1m
     keeps its raw statements and scores one prediction per customer, as this dataset does. The blind reviewer's first
     concern was the same.
   - Effect: with the raw rows, the benchmark tests whether a method can use rows grouped by client; with aggregates,
     it tests our features.
   - Evidence: the rows are usable as they are: LightGBM on the invoices, averaged per client, scores ROC AUC 0.682
     against 0.675 for LightGBM on simple per-client aggregates (the definition's folds). The top solutions built their
     aggregates on the full history, which the cut removes, so there is no shared set to copy. Each client's rows are
     scored as one prediction (the mean of its invoice predictions), so no client weighs more for having more
     invoices.
   - Implemented: the invoice rows; the grouping definition gives this reason. Cost: the 1,862,650 invoices exceed
     the row budget, so 1.5 million are sampled by whole clients (65,603 of 81,531), and a method must handle rows
     grouped by client.
   - Alternative: one row per client with aggregates over its invoices before 2013 (81,531 rows, random split by
     client). Cost: we choose the features, and the methods cannot learn their own.
   - Recommendation: keep the rows as an exception to CLEAN-19, recorded as a Cases line next to amex. Either way
     Claude adds a Cases line for `mean` to the grouping guidance ("a per-entity label without a date, every row one
     observation of it").
   - Decision: confirm the exception, or aggregate.

8. **The meter serial `counter_number` is dropped. Confirm?**
   - Problem: `counter_number` is the meter's serial number, stored by the source as a number, so a model reads it as
     a magnitude. It carries no meaning as a number or a code: the fraud rate is 7.3-9.5% across its deciles in no
     order, and it is not related to the account creation year (Spearman -0.04). Clients that share a serial do not
     share labels (ROC AUC 0.50-0.51).
   - Effect: none on the scores (the leak probe, re-run on the changed definition: its largest drop-one change is 0.015, for `region`).
   - Rule: CLEAN-3 (Should) drops an identifier without meaning; sdss_17's `plate` and `fiber_ID` were dropped the same
     way.
   - Implemented: dropped. Without it, 57 rows repeat another row of the same client (two meters with the same
     invoice); they stay.
   - Alternative: keep it as a code that says which of the client's meters an invoice belongs to (a categorical column
     with about 100,000 values). Cost: a very large category with no label signal.
   - Recommendation: keep the drop, unless you see a use the rules miss.
   - Decision: confirm the drop, or keep the serial as a code.

**Review panel:** ship after changes (mediator), once the curator amends LEAK-25. Claim audit: 64 claims; refuted: the use case as a forecast made in 2013, the equal follow-up of the label, the cohort known at the
prediction point and one range in the text of decision 1, all corrected in the definition (the cohort as a note), and
the record's year 2020, which stays open (the year row). Blind review: include
with changes; it asked for one row per client (issue 4) and named the shifted rows and the serial, which are repaired and
dropped. Debate: agreed on the cut, the grouped split and the text; the mediator settled the follow-up filter at 2015
and the drop of `counter_number` for the critic, and a plain note on the client-record snapshot for the advocate. The
mediator's issues 1-5 are here issue 2, issue 1, issue 4, the year row and issue 8.

<details><summary>Claim audit</summary>

The Kaggle mirror was re-downloaded to read its file list and test files. Thread caps 2 on every run. Models are untuned
LightGBM (EV-8): client level = 400 trees on per-client aggregates by counter type, stratified 3-fold CV; row level =
300 trees on the shipped frame and the shipped 3 folds, then aggregated per client.

**Per claim**

| # | Claim (where) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1 | question (task_summary) | label one value per client; Zindi page | holds | 1 distinct target per client (pre-check); Zindi: "detect and recognize clients involved in fraudulent" | USE-5 |
| 2 | use case: on 2013-01-01 STEG scores clients (task_summary) | can a model exist on that date from these labels? | refuted (framing) | the labels are findings of 2013-2019 (claim 5); no label is known on 2013-01-01, so every training label of the grouped split comes from after the prediction point. What the split mirrors is a cross-sectional screen: STEG has inspected some clients over 2013-2019 and scores the others from their pre-2013 history | USE-1, USE-3, SPLIT-9 |
| 3 | row = invoice 2005-2012 of a client billed before and after 2013 (task_summary) | dates of cohort pre-cut invoices | holds | 2005-01-07 to 2012-12-28 (pre-check) | |
| 4 | 7.8% of clients | recount | holds | 6,504 / 83,874 = 7.75%; shipped frame 66,014 clients, 7.75% | |
| 5 | finding falls in 2013-2019 without a date | fraud rate of meter / status-5 events by first quarter, 2005-2019 | holds (inference) | events first seen 2005Q1-2012Q4: 4.2-12.5% (≈ base 7.75%); 2013Q1-2019Q4: 21.6-42.5% (second meter). 21 frauds among clients who left before 2013, so a few findings may be earlier | EV-2 |
| 6 | known features (task_summary) | creation_date rewritten later? | holds | creation_date >= 2013: 0 of 83,874 cohort clients, but 91.2% of the clients first billed from 2013 (so it is the opening date, not a later rewrite); client_catg/region/district snapshots: untested (no history) | USE-3, LEAK-10 |
| 7 | split: other clients over the same years, as in the challenge | client_test.csv / invoice_test.csv of the mirror | holds | 58,069 test clients, 0 ids shared with train; test invoices 1977-07-13 to 2019-12-07, train 1977-06-09 to 2019-12-07. Note: Zindi's test clients come with their 2013+ invoices, ours not | SPLIT-1 |
| 8 | changes: cut, cohort, 1.5M by whole clients | frame + folds | holds | 1,500,000 rows, 66,014 clients, 0 client overlap train/test in all 3 folds | SPLIT-24 |
| 9 | fit approximate; cut date read off the data | Zindi page | holds | the page states no collection period or label period | USE-8 |
| 10 | year 2019, domain, Spatial tag | InstaDeep report of AI Hack Tunisia | year holds; domain/tag untested (judgment) | event 20-22 Sep 2019 with the STEG meter-fraud challenge | PROV-1 |
| 11 | 1,907,490 invoices, 83,874 clients; 66,014 stratified; ~1M/~500k | recount, frame | holds | 1,907,490 after dedup; sub-sample client fraud rate 0.0775 = cohort; folds 999,406-1,000,000 / 499,145-500,000 | |
| 12 | Kaggle mirror 2020-08-24 holds train, test, sample submission | download and list | holds | zip members dated 2020-08-24: SampleSubmission (2).csv, client_test/train, invoice_test/train | PROV-8 |
| 13 | client_train.csv equals GitHub copy of 2020-06-29 | git blob sha via GitHub API | holds | blob a57327056dd9... equal; commit 2020-06-29T16:58:54Z | PROV-9 |
| 14 | invoice profile 4,476,749 x 16; 135,493; 8,275; 201,893 | recount | holds | pre-check, all four match | |
| 15 | sha256 values | recompute | holds | pre-check, both match | |
| 16 | first run AI Hack Tunisia #4 -- Predictive analytics challenge #1, 20-22 Sep 2019 | web | partly: event and dates hold; the title "#4 ... Predictive analytics challenge #1" untested | InstaDeep: AI Hack Tunisia 2019, 20-22 Sep, six individual challenges incl. STEG meter fraud on Zindi | PROV-1 |
| 17, 19 | start files; join on client_id, one row per invoice | load | holds | 0 clients without invoices; validate many_to_one passes | |
| 18 | label is per-client finding | distinct target per client | holds | 1 | |
| 20 | second-meter fraud rate 7.4-11.9% per quarter 2012, 23.8-25.9% per quarter 2013 | recompute | holds | 2012: .083/.074/.119/.095; 2013: .238/.244/.246/.259 | |
| 21 | event counts do not jump at 2013Q1 | counts per quarter | holds | 2012Q4 232 -> 2013Q1 362, but Q1 is high every year (2011Q1 366, 2012Q1 360, 2014Q1 575) | |
| 22 | client LightGBM 0.848 full history; 0.66-0.69 with the cut | client-level LightGBM | holds | full history, cohort 0.852 (116,360 billed-from-2013 clients: 0.865); cut 0.694. Number drift with REVIEW/record (0.61-0.69) and task probe (0.62-0.67): writing only | EV-8 |
| 23 | STEG and Zindi do not document the cut | Zindi page | holds | no period stated | |
| 24-27 | cohort 83,874 / 6,504; 19,133 early leavers, 21 frauds; 32,486 new; 9 dups | recount | holds | all match (pre-check and a_raw.log) | |
| 28 | level_4 all 0 before the cut | recount | holds | 0 non-zero pre-cut; first non-zero 2014-01-04 | CLEAN |
| 29 | counter_number 0 on 12,555 invoices | recount | holds | 12,555 | |
| 30 | shared serials do not share labels (AUC 0.51) | AUC of mean label of the other clients sharing the serial | holds | 6,111 shared serials, 11,825 clients, AUC 0.502 | LEAK-17, SPLIT-29 |
| 31, 32 | renames; dtypes; client_id never a feature | frame columns | holds | columns district, fraud; 18 features = 20 columns minus fraud, client_id | |
| 33 | grouped by client, mean, Zindi scores AUC per client | Zindi page | holds | "The metric used for this challenge is Area Under the Curve" | EV-5 |
| 34-36 | anomalies 34/4, 21/3, 806 (max 412,509), 29,121 invoices after 2019-09-22 | recount | holds | pre-check | PROV-13 |
| 37 | redistribution forbidden; mirror "other" | not tested | untested | licence is never evidence | EV-4 |
| 38 | 1-234 invoices per client, median 21 | recount | holds | pre-check; sub-sample also median 21 | |
| 39 | challenge quote; AUC on clients not in train | Zindi page | holds | quote matches (truncated after "fraudulent") | |
| 40 | Zindi test file holds 58,069 other clients over the same years | client_test.csv | holds | 58,069; 0 overlap; same date range | |
| 41, 45 | mean aggregation; grouping fields | README | holds | as declared | |
| 42 | per-client AUC 0.685 mean, 0.684 max, 0.682-0.684 latest | row LightGBM on the shipped folds | holds (within 0.003) | mean 0.682, max 0.684, latest 0.680-0.682 (folds 0.671-0.693); the ordering mean > max is not reproduced, "the same" is | EV-8 |
| 43 | max follows invoice count more: Spearman 0.31 vs 0.24 | Spearman on non-fraud clients | holds | 0.297 vs 0.222 | |
| 44 | 50% have several invoices on latest date (ELEC and GAZ) | recount | holds | 42,234 / 83,874; 40,923 of them carry both ELEC and GAZ that day | |
| 46 | no splits_comment | read | holds | | |
| 47 | 860 rows, 31 clients trimmed | test-row coverage over the folds | holds | 860 rows never tested, 31 clients, none of them partly tested | |
| 48 | from 2013Q1 on 21-36% per quarter, against 4-12% up to 2012Q4 (decision 1 text) | table extended to 2005-2019 | refuted (range wording) | the range only fits the 2011Q1-2014Q4 window shown. Second meter: 2013Q1-2019Q4 21.6-42.5%; status 5 12.8-33% (2016Q3 n=39, 12.8%); before 2013 second meter 4.2-12.5%, status 5 0-16.7% (2005, n=12). Direction holds and is stronger | writing.md, EV-8 |
| 49, 50 | decision 2 and 3 texts | computed tables | holds | as README tables | |
| 51 | record year 2020 | first run | refuted | first run 20-22 Sep 2019 (claim 16); the definition's 2019 is right | PROV-1 |
| 52-55 | screening summary, Lennart's notes | recount | holds | 4,476,749 rows / 135,493 clients; max date 2019-12-07; 83,874 clients vs 1.9M rows | |
| 56-62 | assessment 2026-10-07 | recount | holds | 47.8% of frauds carry a 2013+ trace (11,731 clients, 30.8% vs 3.8% fraud, flag AUC 0.702); 0.85 full history | |
| 63 | indabax_drc_2022 is the same data | its record | holds | CC 2026-10-12 cites the same STEG files | PROV-6 |
| 64 | priority 3, weighing | not testable | untested (weighing) | | |

**Implied claims**

| Claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|
| every feature is known on 2013-01-01 (no inspection trace before the cut) | client LightGBM with history cut earlier | holds | cut 2013-01-01: 0.694; 2012-07-01: 0.692; 2012-01-01: 0.687; 2011-01-01: 0.668. No signal piles up just before the cut; pre-2013 events carry the base rate | USE-3, LEAK-10 |
| no client is copied across the split | whole-history hashes; shared serials | holds | 0 clients with an identical pre-cut history; shared-serial label AUC 0.502; leak probe: 0.0% exact copies with dates | LEAK-16 to LEAK-21 |
| the label is one outcome for every client (same follow-up) | cohort fraud rate by year of last invoice | refuted (mild) | the label counts findings up to the client's last invoice: clients leaving in 2013 4.0% (n=1,246), 2014 5.5% (1,097), 2015-2019 7.1-9.3%; 68,580 of 83,874 (82%) are billed into 2019 | LEAK-23, USE-5 |
| the cohort is known at the prediction point | who is dropped by "billed after 2013" | refuted (minor) | selecting on future billing drops 1,567 clients whose last invoice is in 2012 (779 in 2012H2, active-looking on 2013-01-01; 0.83% fraud). Coupled with the follow-up point above | USE-3, LEAK-22 |
| the split is what the use case needs | see claim 2 | refuted (framing) | training labels are 2013-2019 findings of other clients; no labels exist before the cut, so no temporal alternative can be built | SPLIT-9, USE-10 |

**Refuted, ranked (validity first, Must first)**

1. Claim 2 + implied split claim (P3/P4, USE-3/SPLIT-9, Must): the use case "on 2013-01-01 STEG scores" cannot be
   served by labels found 2013-2019; the evaluation is a cross-sectional screen of uninspected clients. Changes the
   wording, not the data (no dated labels exist). Mildest remedy: reword `use_case`/`fit_reason` (e.g. "STEG, having
   inspected part of its clients in 2013-2019, scores the rest from their pre-2013 history") and keep `approximate`.
2. Implied: unequal follow-up of the label (P4, LEAK-23, Must; effect mild: 6% of the cohort leaves in 2013-2016 with
   4.0-7.1% fraud). Mildest remedy: a note naming the follow-up; or a fixed window by keeping clients billed into 2018
   or 2019 (82% are billed in 2019).
3. Implied: cohort selected on future billing (P4, USE-3; 779-1,567 near-negative clients). Remedy: a note, or select
   on "billed in 2012H2" instead of "billed after 2013" (changes the cohort; check the label recording first).
4. Record `year` 2020 (P5, PROV-1): set to 2019.
5. Decision 1 text "21-36% from 2013Q1 on, 4-12% up to 2012Q4" (writing): say "in 2011-2014" or give the full range.

**Untested**

* Claim 16, the exact title "AI Hack Tunisia #4 -- Predictive analytics challenge #1" (no source found; event and
  dates hold).
* Claim 10, domain and the Spatial tag (judgment); claim 64, priority (weighing).
* Claim 37, licence (EV-4: never evidence).
* Claim 6 in part: whether `client_catg`, `region`, `district` were rewritten after inspections (single snapshot).
* That the mirror equals Zindi's train.zip (no Zindi login).

</details>

<details><summary>Column audit</summary>

Prediction point (first `curation_comments` bullet): 2013-01-01, STEG scores each client from its client record and
its invoices 2005-2012; label = STEG's per-client fraud finding, placed in 2013-2019 without a date.

Frame: the definition's container rebuilt through `dataset_io.load(..., built=True)` (origin `rebuilt`), 1,500,000 rows x
20 columns, 66,014 clients, 7.75% fraud clients. Codebook: the Zindi STEG data page (variable list as reproduced on
https://zindi.africa/competitions/indabax-nigeria-23/data, same STEG files): Counter_statue = meter condition, up to
5 values (working, not working, on hold, ...); Reading_remarque = notes the STEG agent takes during a visit (a bad
score when the meter shows something wrong); Counter_coefficient = an additional coefficient applied when standard
consumption is exceeded; the other fields are named only. AUCs below are per client, max(AUC,
1-AUC) on the shipped sample.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `client_id` | pseudonymous client key (`train_Client_<n>`) | yes | category; group column, not a feature; its number does not encode the label (AUC 0.493) | fine | CLEAN-3, LEAK-10 (pointing ids) |
| `invoice_date` | invoice date | yes, all < 2013-01-01 (cut) | datetime, ISO | fine | LEAK-10 |
| `tarif_type` | tariff code (8-29 ELEC, 40/45 GAZ) | yes | category, 13 codes; varies within a client by meter type | fine | CLEAN-14 |
| `counter_number` | meter serial | yes | float64 magnitude of an identifier (1 to 9.9e7, 104,827 values); 0 -> missing (0.67%, fraud 8.6% vs 7.7%, no signal); no signal as a number (AUC 0.503-0.522 for mean/max/n distinct) | question: identifier kept as a number | CLEAN-3, CLEAN-14 |
| `counter_statue` | meter condition (documented 0-5) | yes (per invoice) | category; undocumented codes 46, 420, A (28 rows in the sample): 46/420 sit in rows shifted by columns, A on one client's otherwise normal rows | cleaning problem (minor) | CLEAN-11, PROV-13 |
| `counter_code` | meter code, undocumented | yes | category, 35 codes | fine | CLEAN-14 |
| `reading_remarque` | agent's note at the reading visit (documented 6-9) | yes; no inspection footprint: remark 9 first seen in 2012 goes with 6.7% fraud, below the 8-10% of earlier years | category; 203 and 5 come from shifted rows | fine (shifted rows: see counter_statue) | LEAK-10, CLEAN-11 |
| `counter_coefficient` | multiplier when standard consumption is exceeded | yes | int; 1 on 99.96%; 0 on 42 rows (a zero multiplier is doubtful, unknown meaning) | fine, note | CLEAN-11 |
| `consommation_level_1..3` | consumption by tier | yes | int; `new_index - old_index` equals their sum on 99.5% of rows | fine | |
| `consommation_level_4` (dropped) | fourth tier | n/a | 0 on every pre-cut invoice (first non-zero 2014-01-04) | fine (constant) | CLEAN-5 |
| `old_index`, `new_index` | meter readings before/after the period | yes | int; 779 rows new < old (rollover or meter change), kept; mean per client AUC 0.586 (meter age / volume) | fine | CLEAN-11 |
| `months_number` | months the invoice covers | yes | int; > 24 on 655 sample rows (806 in the cohort), up to 412,509; for those rows the gap to the meter's previous invoice is median 0.9 months, and the largest values are meter readings that slid into this field in shifted rows | cleaning problem | CLEAN-11, PROV-13 |
| `counter_type` | ELEC / GAZ | yes | category | fine | |
| `district` | STEG district | snapshot of unknown date; constant per client | category, 4 codes | fine | LEAK-10 |
| `client_catg` | client category | snapshot of unknown date; constant per client; cat 51 has 22.7% fraud | category, 3 codes | question (snapshot date) | LEAK-10 |
| `region` | region code | snapshot of unknown date; constant per client; best single feature (row AUC 0.597) | category, 24 codes (3 regions span 2 districts) | fine | LEAK-10 |
| `creation_date` | account creation date | yes: none after the cut; 3,950 sample clients created after their first invoice, by 1-321 days (median 78), fraud 7.0% vs 7.8% | datetime | fine: a contract date set after the first bill, not a rewrite at inspection | LEAK-10 |
| `fraud` | STEG's per-client finding | target | category Yes/No, constant per client | fine | CLEAN-15 |

**Problems, ranked (principles.md)**

1. **P4, LEAK-10 / LEAK-11, weak, keep with the note it has.** Inspection footprints before the cut: clients with a
   meter change or counter status 5 first seen in 2012H2 are 9.5% fraud against 7.7% (675 clients, 1.3% of the
   frauds, flag AUC 0.501); the README table shows 2012Q3/Q4 at 9.5-11.9% for second ELEC meters against 4-8% in
   2011. A small edge effect, far from the 2013 step (24-36%). The client record (`client_catg`, `region`,
   `district`) is a single snapshot of unknown date, constant per client, so the data cannot show it did not
   change after a finding (LEAK-10 "attributes looked up after the outcome"). No column measured on its own leaks.
   Remedy: none in the data; a sentence that the client record is a snapshot of unknown date (question for the
   curator whether that belongs in the notes).
2. **P5/P7, PROV-13 then CLEAN-11 (Should).** Shifted rows and impossible `months_number`: e.g. the client with serial
   992 has `counter_statue` 46, `reading_remarque` 203, `months_number` 49,905 (a meter reading). The definition
   keeps them "as the source has them"; CLEAN-11 asks impossible values to become missing. Mildest remedy: set the
   fields of the rows with a code outside the documented sets to missing (or realign them when the shift is
   unambiguous), and `months_number` above a bound (e.g. > 120, or larger than the time since the meter's previous
   invoice by a margin) to missing. Effect on scores: nil (under 0.1% of rows).
3. **P7, CLEAN-3 / CLEAN-14 (question).** `counter_number` is a meter serial shipped as float64, so a model reads it
   as a magnitude. It carries no signal (AUC <= 0.522) and the note already rules out cross-client linkage (claimed
   AUC 0.51). Options: keep as is with a note; ship as a string identifier (high cardinality, CLEAN-14) so it keeps
   its meaning of "which meter" within a client; or drop it as an uninformative identifier. Mildest: a note.
4. **P7, CLEAN-11 (minor).** `counter_statue` `A` (one client, 6 sample rows) and `counter_coefficient` 0 (42 rows)
   are undocumented values on otherwise normal rows; the churn_telco_south_asia precedent makes an undocumented code
   missing. Optional.

</details>

<details><summary>Split audit</summary>

Frame and folds rebuilt from the definition (`dataset_io.from_definition`; not built yet), 1,500,000 rows, 66,014
clients. Threads capped at 2.

**Verdict: right with notes**

Grouped by `client_id`, one prediction per client (mean of its invoices), context all rows. It mirrors the use case
as far as the data allow: STEG scores its current clients from their pre-2013 history, and what is "new" about a
test client is only its label. A temporal split is not possible: the label is undated (2013-2019) and one per client.

**What holds (with numbers)**

* Regime (SPLIT-1, SPLIT-3, USE-10, SPLIT-23): the challenge scores one probability per client on clients not in
  the training file; the declaration (`labels=per_group`, `prediction_unit=group`) matches. A known-entity framing
  (previous outcome as a feature) cannot be built: no client has an earlier finding.
* Group id (SPLIT-24, SPLIT-26): `client_id` is the source's key, one label per client (distinct targets per client:
  1). 0 clients in two test folds; 31 clients (860 rows) in no test fold, the accepted 500k cap.
* Folds: 21,996 / 21,983 / 22,004 clients, fraud 7.756% / 7.756% / 7.753%, every fold spans invoices
  2005-01-07 to 2012-12-28, median 21 invoices per client in each. Random client folds score the same as the shipped
  ones (client-aggregate LightGBM 0.678 +- 0.007 vs 0.674 +- 0.008), so the fold assignment adds no bias.
* Grouping is needed (SPLIT-29): group probe IID 0.944 vs grouped 0.599 on 200k rows (gap 0.345), 0.996 vs 0.581 on
  50k (gap 0.415); per-client permutation test p = 0.048 (logreg 0.619 vs null 0.491). The 200k learnability part had
  not finished when read (its log had only the gap line).
* Hidden groups beyond the client (SPLIT-29, SPLIT-30): meter serial + type shared by 2,239 serials, 2,365 client
  pairs, 66.4% of them across folds; P(fraud | partner fraud) 0.0735 vs 0.0717; the other client's label scores
  ROC AUC 0.500 (4,348 clients), 0.533 when the pair shares a region (1,002 clients). Not a hidden group; the
  definition's 0.51 claim holds. 82% of clients share (region, district, category, creation date) with another
  client: a common day of account creation, not an entity.
* Late labels / gap (SPLIT-9, SPLIT-10): every feature row is before 2013-01-01 and every finding falls 2013-2019,
  for train and test clients alike; train and test are exchangeable in time, so no "future label" shortcut separates
  them and no gap applies to a cross-sectional grouped split.

**Problems, ranked**

1. **P3/P4, note. The training labels come from after the prediction point (USE-9, SPLIT-9 by analogy, SPLIT-8 by
   analogy).** A model deployed on 2013-01-01 would train on findings made before 2013 on earlier histories; here it
   trains on 2013-2019 findings of other clients over the same years. Unavoidable (undated labels), already the
   reason for `fit="approximate"`, and not a leak across the split. Evidence: the cut and all labels lie on the same
   side for both train and test. Remedy: state it in a `splits_comment` (none exists; the split's reasoning is spread
   over `task_summary.split`, `grouping.definition` and `version_comment`): "grouped cross-section standing in for a
   temporal deployment; the labels are undated, so no window or gap can be set". Also fix the record's
   `tag: Non-IID (Temporal)` to the grouped regime (REVIEW issue already lists it).
2. **P4, minor. The cohort rule selects on billing after the cut (LEAK-10 kind, SPLIT-20).** "Billed after 2013" is
   not known on 2013-01-01. Measured on the raw files: of the clients with an invoice in 2012H2, 779 are dropped
   because they are not billed after the cut (fraud 1.28%) against 64,190 kept (7.67%); billing cadence median 118
   days. 1.2% of the clients STEG would score; their labels look unrecorded like the other early leavers. Remedy:
   none to the split; one sentence in the cohort bullet that the rule also drops 779 clients active in late 2012.
3. **Information, not a problem. Alternatives that are not the use case (SPLIT-4).** Holding out newer clients by
   creation date (expanding train, 3 windows) scores 0.635 +- 0.022 (fraud 7.1/6.8/6.1% in test vs 8.8% in train);
   holding out whole regions 0.599 +- 0.027. STEG scores all its clients in all regions, and region and account age
   are known for each, so neither split applies. The grouped score is not inflated by them.

Rule IDs: SPLIT-1, -3, -4, -8, -9, -10, -20, -23, -24, -26, -29, -30; USE-9, USE-10; LEAK-10.

</details>

<details><summary>Domain practitioner</summary>

I play the head of revenue protection at a STEG district: I have a fixed number of sworn inspection teams and, on a
given date, I rank clients to decide whose meter to send a team to (USE-1). The definition's use case says the same:
on 2013-01-01, score each client from the client record and its invoices so far, to decide whom to inspect.

**Fit: approximate (agrees with the definition)**

One sentence: the actor, the moment and the per-client ranking are real, but the label is "STEG found fraud at some
undated point in 2013-2019" among clients who were not all inspected, which is a proxy for "an inspection now would
find fraud" with no horizon (USE-8, the alfa_battle_2_0_task_2 pattern: a label without a stated horizon).

USE-9 check: I find no other well-defined use case that the shipped data mirrors directly. A one-shot 2013 audit
ranking with a seven-year outcome window is not a decision a utility makes; rephrasing to it would only excuse the gap
(the weighed factor against USE-9). Approximate stays.

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, and the dataset has them: district, region, client category, account creation date; per invoice the date,
tariff, meter serial, status, code, type, reading remark, tiered consumption, old/new index, months covered. All are
billing-system fields known at billing time; with the cut at 2013-01-01 none is recorded after the prediction point.
Correct choice: the 2013+ meter replacements and status-5 codes are the footprints of the inspection itself (LEAK-10),
and the cut removes them.

I would not have: nothing in the shipped features, as far as I can see. `consommation_level_4` (2014+) is dropped.

Missing, that I would always have:
* the client's earlier inspection history and earlier fraud findings (a recidivist is my first target; USE-10 says
  the history of a known entity is legitimate). This is the largest missing input.
* neighbourhood fraud rates and finer location than district/region (the NTL literature shows neighbourhood features
  help, Glauner et al. 2016);
* meter model/age and whether it is installed outside the home (STEG moved meters outdoors to ease control);
* payment behaviour (arrears, disconnections).
None of these is in the source, so this is a gap of the source, not of the curation.

**2. The target (USE-5)**

What I act on: "will an inspection of this client in my next campaign find tampering", with a horizon of weeks to
months. What the data gives: a per-client flag of a finding somewhere in 2013-2019, undated (the data, not STEG,
place it there). Two proxy gaps:
* horizon: a finding in 2018 is predicted from invoices ending 2012, so the label mixes "fraud now" with "fraud that
  started years later". This dilutes the signal (per-client ROC AUC about 0.68 with the cut against 0.85 with the
  leaked full history).
* selection: a 0 is "not found", not "not fraudulent". Inspected customers are not a random sample (covariate shift
  in inspection labels, Glauner et al. 2017), and the near-zero fraud rate of clients who left before 2013 (21 of
  19,133) shows that the label is "recorded in the system", not the truth. The cohort filter handles the worst of it.
Output: I want a score to rank clients and take the top k my teams can visit; a probability per client is right, and
ROC AUC is an acceptable stand-in for precision at my inspection capacity (Zindi also scores AUC).

**3. Row, decision, test data**

* One row is an invoice, one decision is a client; the group prediction (mean over invoices, prediction_unit group)
  maps rows back to my decision. Fine.
* Test data: other clients scored at the same date with the same label window. In deployment I would train on the
  outcomes of earlier campaigns and score clients forward, so train and test would not share the label window. With
  undated findings a temporal split is impossible; grouped by client at one cut is the honest choice (USE-10 cold
  start is not the case here, but the label is per client, so the grouped split is the only one that does not repeat a
  client's label).

**4. Would I use this model?**

As a triage ranker on top of my inspectors' own rules, yes, after retraining on my current campaigns. I would trust it
because its inputs are all billing data I hold on the date and the inspection footprints are cut out. I would distrust
it because the 0s are not verified negatives, the horizon is undefined, and I would first want the hit rate of the top
decile against my current targeting, not an AUC.

**Gaps, ranked by how much they change the task**

1. Label horizon undefined (finding 2013-2019, undated) - changes the question from "fraud now" to "fraud ever within
   seven years" (USE-5, USE-8). Already named in fit_reason.
2. Negatives are "not found" by a non-random inspection process (USE-5). Not named in the task_summary; worth one
   clause in `predicted` or `fit_reason`.
3. Missing prior inspection / fraud history, a feature every utility holds (USE-6, USE-10). Source gap.
4. Same label window in train and test (no forward split possible) (USE-10, split).
5. The cut date is read off the data, not documented (USE-3); the evidence (step in fraud rate at 2013Q1 with no step in
   event counts) is convincing.
6. Metric: AUC rather than precision at inspection capacity (minor).

**What an expert would change**

* Keep the cut and the cohort; they are what makes the task honest (USE-12: fix the leak, keep the task).
* Add to `predicted` or `fit_reason` that a 0 means "no fraud found", not a verified negative.
* If STEG or Zindi data ever give the inspection date, rebuild with a fixed horizon (e.g. found within 12 months of
  the cut) and add prior findings as a feature.
* Nothing to change in the features or the grouping.

**Sources**

* Zindi challenge page: https://zindi.world/competitions/fraud-detection-in-electricity-and-gas-consumption-challenge
  (aim "detect and recognize clients involved in fraudulent activities"; losses of about 200M TND; AUC; no target
  definition, no mention of inspections).
* Glauner et al., "Is Big Data Sufficient for a Reliable Detection of Non-Technical Losses?" (2017),
  https://arxiv.org/abs/1702.03767 (inspection labels are a biased sample, covariate shift).
* Glauner et al., "Neighborhood Features Help Detecting Non-Technical Losses in Big Data Sets" (2016),
  https://arxiv.org/pdf/1607.00872.
* STEG fraud and control practice (Tunisian press): https://africanmanager.com/tunisie-steg-18-000-cas-de-vol-delectricite-en-2023/,
  https://www.kapitalis.com/archive/186-kapital/27031-la-manipulation-des-compteurs-d-electricite-coute-cher-a-la-steg
  (sworn control teams, bailiff confirms the finding, 5,000-18,000 cases a year, meters moved outdoors).
* The definition, the record, the earlier REVIEW.md and the claim list, use_case.md.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The data is real and useful: STEG (Tunisia) utility billing, used to choose which customers get a meter inspection. But the label belongs to the client and the rows are invoices, so the task should be rebuilt as one row per client before it goes into a benchmark.

**Use case**
STEG wants to "detect and recognize clients involved in fraudulent activities" from "the client's billing history". The losses are about 200M TND. The prediction is used to decide whom to inspect. The Zindi submission is one score per `client_id`, scored by AUC. This is a real and common use.

**Concerns, most serious first**

1. **The unit of prediction is wrong.**
   - `fraud` never varies within a client: 0.0% of clients have more than one value.
   - The client-level columns never vary within a client either: `region`, `district`, `client_catg` and `creation_date` (0.0% varying).
   - The 200k-row sample covers 57,348 clients, and one client has up to 33 rows.
   - So scoring is per invoice. That weights each client by how many invoices it has, which is not how the source frames or scores the task.
   - Fraud rate is 8.6% by row and 8.0% by client.
   - **Change:** build a client-level table. Keep the static client attributes and aggregate each client's invoices (counts, means/std/min/max of consumption levels and index differences, number of counters, gas/electricity share, date span). Then the grouped split is no longer needed and an ordinary stratified split will do.
2. **Label timing is unknown.**
   - The source does not say when the fraud was found or what period the label covers.
   - Invoices issued after the fraud was found may reflect what was done about it, such as a replaced counter (`counter_statue` codes, a new `counter_number`). I could not check this.
   - **Change:** state the assumption in the task description. If the date fraud was found can be obtained, keep only invoices from before it.
3. **Column types and implausible values.**
   - `tarif_type`, `counter_code`, `reading_remarque`, `district`, `region` and `client_catg` are integer codes but are stored as int64. They should be categorical.
   - `counter_number` is an identifier stored as a float. Drop it, or keep only a count of distinct counters per client.
   - `counter_statue` is categorical but has levels with no rows: 420, 46, A.
   - `months_number` goes up to 410,431 (median 4).
   - `counter_coefficient` is 0 in some rows.
   - **Change:** fix the types, and clip or set to missing the impossible values.
4. **There are 36 exact duplicate invoice rows** (ignoring the id). This is minor.
5. **Signal is modest but enough to score.**
   - I ran LightGBM on the raw invoice rows with a 3-fold split grouped by client. AUC is 0.644 per row and 0.661 when the invoice scores are averaged per client.
   - It is not trivial and leaves room between methods. Aggregating features to the client level should give more signal.

**What I could not check**
- The full 1.5M rows. I only saw the 200k sample, and it has only `train_` clients.
- The Zindi Data tab, where the file and column documentation is.
- When the fraud was found.
- Whether the other Zindi copies of this data (InDabaX and others) are the same data.

</details>

<details><summary>Precedent check</summary>

Sources read:
- The register of past decisions
- The earlier REVIEW.md and the checklist
- The definition
- Sibling definitions and REVIEW.md files: amex_non_iid_1m, musk, sat11, alfa_battle_2_0_task_2, rosbank1, home_credit_*, ieee_fraud_detection, account_debt_south_africa, expresso_churn_prediction_1m, caracas_cervical_cancer
- Knowledge files: leak_checks.md, use_case.md, cleaning_features.md, provenance.md, definitions.md (Grouping)

**Issue 1. History cut at 2013-01-01 (implemented) against the full history**

**Verdict: departs from the LEAK-38 line, with a stated reason. Consistent with LEAK-10 and with today's expresso.**

- **Follows:**
  - mic (LEAK-10 Cases): move the prediction point earlier and drop what does not exist yet.
  - hotel_booking_demand (LEAK-12 / SPLIT-9, CC 2026-09-30, Lennart): filter by an as-of date.
  - The post-2013 meter swaps, status-5 codes and code changes are a consequence of the inspection that set the label. That is LEAK-10, Must ("a consequence ... of the target").
- **The alternative it departs from:** keeping the full history with a `Potential leak, kept on purpose` bullet. That would follow LEAK-38 (Should): kick `WheelType`, 0.757 to 0.691 (CC 2026-10-01, Lennart); homesite `PropertyField37` x `PersonalField12`, 0.965 to 0.915 (CC 2026-10-01, Lennart).
- **What sets STEG apart, all written in the definition and the decision table:**
  - a measured timing: the fraud rate steps at 2013Q1 while the number of events per quarter stays flat;
  - named codes with a known mechanism, not anonymised fields;
  - a much larger effect: 0.848 against 0.66-0.69, 47.8% of frauds carry a trace, and the flag alone scores AUC 0.70.

  LEAK-38's own reason ("removing an unverified signal ... is arbitrary") does not hold when the signal is verified.
- **Same-day pair:** expresso_churn_prediction_1m issue 1 drops REGION against kick on the same distinguishing fact ("a measured mechanism that kick never had") and recommends amending LEAK-38. STEG is the second case of that exception, the same day. It is not yet the third, but both should be decided together with the LEAK-38 amendment expresso proposes. Issue 1 should name kick/homesite/expresso as its precedents; today it cites none.
- **ieee_fraud_detection does not apply.** Its `uid` was kept under LEAK-34 (CC 2026-10-01, Lennart): an entity's own history under a temporal split, with labels earlier than the test rows, and worth 0.001-0.007 AUC. Here the traces come after the prediction point and after the label was set. Different mechanism, no conflict.
- **Cut date read off the data:** like sf_permit_time's gap (SPLIT-10, chosen from the data) and account_debt's run threshold (pending today). Consistent. The definition states it (`fit_reason`).

**Issue 2. Cohort: clients billed before and after the cut**

**Verdict: the early-leaver drop departs from LEAK-25 as written. A reason is stated. This is the third exception of its kind, so an amendment is due.**

- **The rule:** LEAK-25 (Must) says "retire unless the recording process can be recovered". Its only Case is ghanas_indigenous_intel, retired (CC 2026-10-01, Lennart). There the unrecorded rows could not be located, and the dataset was also Too Small.
- **The same reading, "located and dropped":**
  1. caracas_cervical_cancer: shipped by Lennart on 2026-10-15. It dropped 108 patients whose results "look unrecorded rather than negative" (0 positives where 11.8 were expected). Not in LEAK-25's Cases table.
  2. account_debt_south_africa issue 1: pending today. It drops eight unrecorded file runs and asks for a LEAK-25 Cases row that reads "recovered" to cover "located and dropped".
  3. STEG: drops 19,133 early leavers (21 frauds, 0.11%) whose labels look unrecorded.
- **The stated fact:** the leavers are locatable by their last invoice date, and the fraud rate is 0-0.15% up to 2011, then 3.9-8.3% from 2013. This matches the reasons given for caracas and account_debt.
- **A residual for the panel (not a departure, a question of where the same rule's threshold falls):** inside the kept cohort, clients whose last invoice is in 2013 or 2014 have 3.9% and 4.7% fraud, against 6.4-8.3% for 2015-2019 (README decision table). That is the same gradient on a smaller scale (about 2,850 clients). Applied consistently, LEAK-25 and LEAK-24 ("cut where follow-up is complete") would at least name it.
- **Newer clients dropped (32,486 with no history before the cut):** consistent with the prediction point (USE-3) and with cirrhosis (LEAK-23: "over the rows followed that long").

```text
**Consistency check (AI, 2026-10-20):** your call on fraud_detection_in_electricity_and_gas_consumption (drop the
19,133 clients who left before 2013, whose labels look unrecorded, instead of retiring) is the third time an
unrecorded-label subset is located and dropped under LEAK-25 (Must: "retire unless the recording process can be
recovered"), after caracas_cervical_cancer (shipped 2026-10-15) and account_debt_south_africa (pending today);
ghanas_indigenous_intel (2026-10-01) was retired. What sets these apart from ghanas?
(a) the unrecorded rows can be located by a rule that never reads the label row by row (here the last invoice
    date), so "recovered" covers "located and dropped": recorded as an amendment of LEAK-25 with the three cases;
(b) treat STEG like ghanas (retire);
(c) reopen caracas to match ghanas;
(d) change the rule (an amendment).
```

**Issue 3. Group prediction rule: `mean` (implemented), `any`, `last`**

**Verdict: consistent with the guidance, with a stated reason. It is the first `mean` in the copy.**

- definitions.md (Grouping) lists:
  - `mean` for replicate measurements of one label;
  - `any` for multiple-instance data (musk);
  - `last` when the latest row carries the label (amex_non_iid_1m: the label is defined "after the latest credit card statement").
- **Against amex `last`:** the STEG label has no date and no horizon anchored to the latest invoice, and 50% of clients have ties on their latest date. Written in the grouping definition.
- **Against musk `any`:** the fraud is found after the cut, so no pre-cut invoice is known to carry it. The maximum also follows the invoice count more (Spearman 0.31 against 0.24). Written.
- The scores tie (0.685 / 0.684 / 0.682-0.684), so the choice changes no ranking-relevant number.
- **No drift:** the three earlier group-unit datasets each match their listed case.
- Suggest a Cases line for `mean` ("a per-entity label without a date, every row one observation of it") so the next undated per-client label follows it.

**Issue 4. Context and size: raw invoice rows with `all_rows` against one row per client**

**Verdict: departs from the CLEAN-19 line. The reason is stated only in the earlier REVIEW.md, and it misquotes the rule.**

- **The CLEAN-19 line** (Should: "a transaction log or a history aggregated to one row per prediction. Take the features the top solutions share"):
  - alfa_battle_2_0_task_2 (Lennart, 2026-10-13: 513 top-solution aggregates);
  - rosbank1 (CoLES aggregates);
  - home_credit_default_risk (kernel aggregates);
  - home_credit_default_stability_1m (TabReD aggregates).
- **The other line:** amex_non_iid_1m keeps raw statements with `prediction_unit="group"` ("simulate a pipeline that can handle raw non-IID grouped data"). STEG follows amex.
- **Distinguishing facts:**
  - CLEAN-19 applies "because the raw data cannot be used as it is". Here the rows can be: the row model averaged per client (0.685) beats simple client aggregates (0.662).
  - The Zindi top solutions aggregate over the full history, which the cut removes.
  - Lennart's record comment.
- **Problems with the current text:**
  - the earlier REVIEW.md says aggregates are "feature engineering the guidelines leave to the pipeline". CLEAN-19 says the opposite for histories.
  - The 0.662 baseline is "simple client aggregates", not the top solutions' features that CLEAN-19 asks for.
  - The definition does not record the choice.

  The issue should cite CLEAN-19 and amex and drop the misquote.

```text
**Consistency check (AI, 2026-10-20):** your call on fraud_detection_in_electricity_and_gas_consumption_1m (ship the
raw invoice rows, one prediction per client by `mean`) differs from alfa_battle_2_0_task_2 (2026-10-13, Lennart:
top-solution aggregates, one row per client; CLEAN-19), rosbank1 and home_credit_default_risk, and follows
amex_non_iid_1m (raw statements, group unit). What sets STEG apart?
(a) the invoices are usable as rows (row model averaged per client 0.685 against client aggregates 0.662) and the
    top solutions' aggregates were built on the full history the cut removes, recorded as the reason in the
    grouping definition and as a CLEAN-19 Cases line next to amex;
(b) treat it like alfa_battle (one row per client with the shared top-solution aggregates over the pre-2013 invoices);
(c) reopen amex to match alfa_battle;
(d) change the rule (CLEAN-19 names when raw grouped rows are kept instead).
```

**Issues 6 and 7. Extract date, source and download, licence**

**Verdict: consistent.**

- **Dates after Sep 2019:** recorded as damage (PROV-13/15). The cut does not touch them. No decision.
- **Kaggle mirror for a login-only original:** a transport copy checked by sha256 against a 2020 GitHub copy and against the starter notebook's profile. This differs from water_quality and the other PROV-1 cases ("every link ends at an anonymous re-upload"): here the original (Zindi, STEG) is known. alfa_battle used a Kaggle mirror as a fallback the same way.
- **"Redistribution forbidden" not a verdict reason:** follows EV-4 (lucas_topsoil, 2026-09-23, Lennart).

**Record fields**

- **`year` 2019 (definition) against 2020 (record):**
  - The definition follows PROV-9 (Must: "a competition's launch", not the copy's date). The first run was AI Hack Tunisia #4, 20-22 Sep 2019, with the same 58,069 test clients.
  - This matches today's PROV-9 cases (airfoil_self_noise, first_principles_tully_fisher, nikuradse: first publication, 2026-10-20, Lennart) and expresso (2020 UmojaHack release).
  - The record's 2020 comes from Lennart's own comment ("release date is 2020"), so he must confirm the change. Consistent.
- **`tag`:** not reproduced. The record now has `tags: Non-IID (Grouped)` and `required_split: Grouped (NON-IID)`, which agree with the definition. The `Non-IID (Temporal)` line in the earlier REVIEW.md looks stale and should be removed.

**Not in the earlier REVIEW.md: `counter_number` kept as a numeric feature**

**Verdict: departs from CLEAN-3 without a reason.**

- CLEAN-3 (Should): drop uninformative identifiers; keep one that carries meaning and process it into that meaning. The meter serial stays as a magnitude.
- The definition only argues that it does not link clients (label AUC 0.51, a claim not re-measured). It does not say what meaning the serial carries.
- No Cases row exists. The nearest precedents:
  - sdss_17 `plate`, `fiber_ID` were dropped (pointing ids, LEAK-10 Cases);
  - ieee `uid` was kept as an engineered entity key (LEAK-34).
- Low stakes: drop-one changes are at most -0.017, and that maximum is for `region`.

```text
**Consistency check (AI, 2026-10-20):** your call on fraud_detection_in_electricity_and_gas_consumption_1m (keep
`counter_number`, the meter serial, as a numeric feature) departs from CLEAN-3 (drop uninformative identifiers; keep
one that carries meaning and process it into that meaning) and gives no meaning for it. What sets it apart?
(a) serial ranges encode the meter's batch or installation period, known at the prediction point, so it carries
    meaning, recorded as the reason (check: fraud rate and meter age by serial decile);
(b) treat it like other uninformative ids: drop it (CLEAN-3);
(c) -;
(d) change the rule.
```

**Also checked, consistent**

- **Grouped split matching Zindi's protocol, no temporal holdout (checklist P4 concern):** the label is undated, so a split by finding date cannot be built. `fit=approximate` with "no date or stated horizon" follows alfa_battle_2_0_task_2 (USE-8: "a label without a stated horizon"). SPLIT-31 (amazon_employee_access, bank_marketing) accepts a split that matches the source's framing.
- **`_1m` sub-sample by whole groups with `subsample_to_budget`:** the same as amex_non_iid_1m, with the same accepted warning (`splits_rows_never_tested`).
- **Drift:** no curator drift found. Lennart's decisions on LEAK-38 (kick, homesite, 2026-10-01), LEAK-34 (ieee, 2026-10-01) and LEAK-25 (ghanas 2026-10-01, caracas 2026-10-15) are each internally consistent. The movement is in the AI's recommendations today (expresso and STEG against LEAK-38; account_debt and STEG on LEAK-25). That is a reason to bring the two amendments to Lennart, not to call it drift.

**For the mediator**
- **Needs the curator:**
  - the LEAK-25 amendment (prompt above; covers caracas, account_debt and STEG together);
  - the LEAK-38 amendment, decided with expresso's issue 1;
  - issue 4's prompt;
  - the `counter_number` prompt.
- **Fixes needing no decision:**
  - cite kick/homesite/expresso in issue 1;
  - fix the CLEAN-19 misquote in issue 4;
  - drop the stale `tag` line;
  - add a Cases line for `mean`.

</details>

<details><summary>Advocate</summary>

1. **The 2013 cut fixes a verified leak and keeps the task (P4, LEAK-10, Must; USE-12; tension "real task against a leak").**
   - **Evidence:** for new second electricity meters, the fraud rate is 7.4-11.9% in every quarter of 2012 and 23.8-25.9% in every quarter of 2013. The number of such events per quarter stays flat (claims 20, 21). Clients with a 2013+ trace are 30.8% fraud, hold 47.8% of all frauds, and the flag alone scores AUC 0.70. Full history scores 0.848; with the cut it scores 0.694.
   - **The cut sits where the step is:** moving it earlier finds nothing piled up before 2013 (2012-07: 0.692; 2012-01: 0.687). The column audit says "no column measured on its own leaks". The 2012H2 edge holds 1.3% of frauds, flag AUC 0.501.
   - **Why this beats keeping the full history:** LEAK-38 is a Should that narrows LEAK-10, and its stated reason is "removing an unverified signal ... is arbitrary". This signal is verified, comes from named codes and has a known mechanism. Expresso applies the same exception today.
   - **Fix to the text:** cite kick, homesite and expresso in issue 1. Bring the LEAK-38 amendment together with expresso.

2. **The split is right (P4: SPLIT-1, -3, -23, -24, -29, Should/Must).** The split audit's verdict is "right with notes".
   - The grouping is necessary: IID scores 0.944 against 0.599 grouped.
   - The folds are balanced: 7.753-7.756% fraud each, all spanning 2005-2012. Random client folds score the same (0.678 against 0.674).
   - There is no hidden group: the label of a client sharing the serial scores AUC 0.500-0.502.
   - Zindi's test file also holds other clients (58,069) over the same years. A temporal split cannot be built because the labels are undated.
   - **Answer to the blind reviewer ("rows are invoices, scored per invoice"):** this is refuted by the definition. `prediction_unit="group"` scores one probability per client, as Zindi does.
   - **Raw rows versus aggregates (CLEAN-19, Should):** the rows are usable as they are. The row model averaged per client scores 0.685 against 0.662 for simple client aggregates. The top solutions' aggregates were built on the full history, which the cut removes. Precedent: amex_non_iid_1m.
   - **Conceded:** write this reason into the grouping definition and add a CLEAN-19 Cases line. Drop REVIEW's misquote of CLEAN-19.

3. **Fit "approximate" is honest (P3, USE-8, Must; USE-9).**
   - The domain practitioner agrees: the actor, the decision and the per-client ranking are real. The gap is a label without a horizon, which is the alfa_battle_2_0_task_2 precedent. No other use case is mirrored directly.
   - **Conceded (claim audit, claim 2):** "on 2013-01-01 STEG scores" overstates the use case, because the training labels are 2013-2019 findings. The mildest remedy is wording only:
     - `use_case`/`fit_reason`: "having inspected part of its clients in 2013-2019, STEG scores the rest from their pre-2013 history";
     - `predicted`: add "a 0 is no fraud found, not a verified negative";
     - add a `splits_comment` saying it is a grouped cross-section standing in for a deployment over time.
   - No data change follows.

4. **The cohort is defensible (P4, LEAK-25, Must).**
   - The early leavers (19,133 clients, 21 frauds, 0.11%) are located by their last invoice date, never by reading the label. Caracas was shipped on this reading; account_debt is pending. Bring the LEAK-25 amendment for all three together.
   - **Conceded, mild:** the follow-up is unequal (LEAK-23/24). Clients who leave in 2013 are 4.0% fraud, in 2014 5.5%, in 2015-2019 7.1-9.3%; 82% are billed into 2019.
   - **Conceded, mild:** the cohort is chosen on billing after the cut (779 clients active in 2012H2 dropped, 1.28% fraud).
   - **Remedy:** a note naming both. If the mediator reads LEAK-24 as triggered, filter the cohort to clients billed into 2015 or later, so every client has the same follow-up. That is a definition fix that keeps the dataset (ladder rung 2), not grounds to exclude it.

5. **Worth benchmarking (P6, TP rules).**
   - The task probe has no flags. Dummy 0.500, linear 0.622, random forest 0.668. Skill +0.335 (SE 0.011) on 3 of 3 splits. Spread +0.091 (SE 0.023).
   - The smallest test-fold class is 162 clients. Permutation test p = 0.048.
   - The modest signal comes from the honest split. Tension "right split against score" (forest_fires): no reason to retire.

6. **Faithful, unique data (P5: PROV-1, PROV-6, PROV-8, PROV-9).**
   - Both sha256 sums match. The client file's GitHub blob is equal to the 2020 copy, and the invoice profile matches.
   - The mirror holds Zindi's train and test files. indabax_drc_2022 is rejected as a duplicate.
   - `year` 2019 is correct (first run 20-22 Sep 2019). Fix the record's 2020 and drop the stale `Non-IID (Temporal)` line.
   - Residual, untested: mirror against Zindi's train.zip (needs a login).

7. **The cleaning gaps are quality issues and cannot block a validity-clean task (P7; principles step 3, "independent failures are not conflicts").**
   - **CLEAN-11 (Should), conceded as a cheap and safe fix:** set to missing the fields of rows with codes outside the documented sets (34 + 21 shifted invoices), and `months_number` values above a bound such as 120. This touches under 0.1% of rows and has no effect on scores.
   - **`counter_number` (CLEAN-3, Should):** no signal (AUC 0.503-0.522) and no linkage across clients (0.502). Keep it with a note giving the reason, or drop it. Either changes the scores by at most 0.017 (that maximum is for `region`, not this column). This is the curator's call.
   - **Writing:** align the AUC drift (0.66-0.69, 0.61-0.69, 0.62-0.67) on the measured 0.62-0.69. Fix decision 1's quarter range to 2011-2014, or give the full range.

**Verdict sought:** ship after the changes in points 3, 4 (a note, or the follow-up filter), 6 and 7. All rules at P1-P5 hold or are fixed in the definition.

</details>

<details><summary>Critic</summary>

**Position: ship only after changes.** The task is real and the 2013 cut is right (LEAK-10). Nothing here calls for
exclusion. But the definition says more than the data supports, and two label-timing Musts are not handled the way
the rules say. Points are in rank order: validity (P3, P4) first, then quality (P5, P7).

**1. The use case says the model is used on 2013-01-01, but every training label was found in 2013-2019 (P3/P4; USE-3, USE-8, SPLIT-9, Must)**

- **Problem.** `use_case` reads "On 2013-01-01, STEG scores each client ... to decide whom to inspect". No label
  exists on that date. Every finding falls in 2013-2019 (claim audit, claim 5: second-meter fraud rate 21.6-42.5% per
  quarter from 2013Q1 against 4.2-12.5% before). So every training row breaks SPLIT-9 as the use case is written.
  The claim audit refutes claim 2 and the implied split claim.
- **Effect.** No shortcut follows from it. Train and test clients share the same window, so they are exchangeable
  (split audit, "Late labels"). The trouble is that the benchmark measures something else: a cross-sectional screen.
  STEG has inspected some clients by 2019 and ranks the others from their pre-2013 invoices. A 2013 forecast trained
  on past campaigns is a different thing.
- **Remedy (fix the definition, text only).**
  - Reword `use_case` and `fit_reason` to the screen: "STEG, having inspected part of its clients in 2013-2019,
    ranks the others from their invoices before 2013". Keep `approximate`.
  - Add a `splits_comment`: a grouped cross-section stands in for a temporal deployment, and the labels are undated,
    so no window or gap can be set (split audit, problem 1).

**2. The label's follow-up is not the same for every client (P4; LEAK-23, LEAK-24, Must)**

- **Problem.** The label counts findings up to the client's last invoice. Fraud rate in the kept cohort by year of
  last invoice:

  | Last invoice | Fraud | Clients |
  |---|---|---|
  | 2013 | 4.0% | 1,246 |
  | 2014 | 5.5% | 1,097 |
  | 2015-2019 | 7.1-9.3% | |

  82% of the cohort (68,580 of 83,874) is billed into 2019 (claim audit, implied claims). This is the same gradient
  as the early leavers the definition drops (precedents, issue 2 "residual"). Clients who leave early had less time
  to be found.
- **Effect.** Some fraud clients with short follow-up are labelled 0 because nobody had found them yet. The effect is
  mild (about 6% of the cohort), but it is a censoring Must.
- **Remedy (filter).** LEAK-23 asks for "an outcome within a fixed horizon, over the rows followed that long", as in
  cirrhosis. So keep the clients billed into a late year, for example 2018 or 2019, and check that the step in the
  fraud rate is gone. If the curator rejects the filter, the fallback is a bullet that gives the gradient in numbers.

**3. Dropping the early leavers departs from LEAK-25 as written, for the third time (P4; LEAK-25, Must)**

- **Problem.** LEAK-25 says "retire unless the recording process can be recovered". The definition instead locates
  and drops 19,133 clients whose labels look unrecorded (21 frauds, 0.11%). caracas_cervical_cancer (shipped
  2026-10-15) and account_debt_south_africa (pending) did the same. A Must has no exceptions, so three silent
  departures mean the rule and the practice disagree (principles, "Exceptions and amendments"; precedents, issue 2).
- **Related problem.** The cohort rule "billed after 2013" is not known on 2013-01-01 (USE-3). It also drops 779
  clients who were active in 2012H2 (fraud 1.28%) (split audit, problem 2; claim audit, implied claims).
- **Remedy (no change to the data).**
  - Before shipping, the curator settles the LEAK-25 amendment ("located by a rule that never reads the label" counts
    as "recovered"; the precedents' prompt, option (a)) together with the other two cases.
  - Add one sentence to the cohort bullet on the 779 clients active in late 2012.

**4. A 0 means "not found", not "no fraud", and the client record is a snapshot of unknown date (P3/P4; USE-5 Must, LEAK-10)**

- **Problem.** Inspected clients are not a random sample. A 0 is "no finding recorded" (practitioner, gap 2; Glauner
  et al. 2017). The task summary does not say this.
- **Related problem.** `client_catg`, `region` and `district` are one snapshot per client, of unknown date. `region`
  is the strongest single feature (AUC 0.597). The data cannot show that these fields did not change after a finding
  (column audit, problem 1; LEAK-10 Cases, "attributes looked up after the outcome").
- **Remedy (notes).**
  - Add one clause to `predicted` or `fit_reason`: a 0 means no fraud was found.
  - Add one bullet: the client record is a snapshot of unknown date. It cannot be tested, so record it as a potential
    leak.

**5. Raw invoice rows are kept instead of per-client aggregates, and the definition does not say why (P7; CLEAN-19, Should)**

- **Problem.** CLEAN-19 asks to aggregate a history to one row per prediction, using the features the top solutions
  share. alfa_battle_2_0_task_2, rosbank1 and home_credit follow it. This dataset follows amex_non_iid_1m instead.
  The reason is stated only in the earlier REVIEW.md, and that text misquotes CLEAN-19 as "feature engineering the guidelines
  leave to the pipeline" (precedents, issue 4). The blind reviewer's first concern was the same one.
- **Note.** `prediction_unit="group"` already answers the blind reviewer's worry about per-row weighting.
- **Remedy (record the exception; quality, not a reason to exclude).** Write the reason in the grouping definition:
  the rows are usable (0.685 against 0.662), and the top solutions' aggregates were built on the full history that the
  cut removes. Add a CLEAN-19 Cases line next to amex. Correct the misquote.

**6. Impossible values and a serial number are shipped as they are (P5/P7; PROV-13, CLEAN-11, CLEAN-3, Should)**

- **Problem.**
  - Some rows are shifted by one column: `counter_statue` 46 or 420, `reading_remarque` 203, and `months_number`
    49,905 is a meter reading.
  - `months_number` is above 24 on 806 invoices, up to 412,509.
  - `counter_number` is a meter serial shipped as a float64 magnitude. The definition gives it no meaning, and its
    AUC is at most 0.522 (column audit, problems 2 to 4; precedents, `counter_number`).
- **Effect.** Nil on scores (under 0.1% of rows). CLEAN-11 is a Should, and its cases (churn_telco_south_asia,
  thyroid_discordant) apply it.
- **Remedy (cheap repair).**
  - Set to missing the fields of rows whose codes fall outside the documented sets, and `months_number` values that
    are impossible (for example above 120 months).
  - Drop `counter_number`, or keep it with a note that says what meaning it carries (CLEAN-3).

**7. Text that the audits refuted or that has drifted (procedure; writing.md, EV-8, PROV-9)**

- The text of decision 1, "21-36% from 2013Q1 on, against 4-12% up to 2012Q4", only fits the 2011-2014 window shown.
  Over 2005-2019 it is 21.6-42.5% against 4.2-12.5% (claim audit, claim 48). Say "in 2011-2014", or give the full
  range.
- The scores with the cut appear as 0.66-0.69 (definition), 0.61-0.69 (REVIEW and record) and 0.62-0.67 (task
  probe). Use one range with its source.
- Record fields: `year` should be 2019 (PROV-9; the first run was 20-22 Sep 2019). The stale
  `tag: Non-IID (Temporal)` line in REVIEW should go.

**Verdict in the judgment-record shape**

```text
Verdict: ship after changes.
Validity: USE-3/USE-8/SPLIT-9 triggered, fix the wording (screen, not 2013 forecast) + splits_comment;
  LEAK-23/24 triggered, fix by a fixed-follow-up cohort (fallback: a note); LEAK-25 departure, needs the curator's
  amendment; USE-5 note (0 = not found); LEAK-10 snapshot note.
Value: TP holds (per-client AUC 0.62-0.69, no flag).
Quality: CLEAN-19 departure to be recorded as an exception; CLEAN-11/PROV-13 and CLEAN-3 repairs.
For the curator: the LEAK-25 amendment; the follow-up filter or a note.
```

</details>

<details><summary>Advocate rebuttal</summary>

We agree on the verdict ("ship after changes"), on the 2013 cut (LEAK-10) and that nothing here calls for exclusion. What is left is how to fix two label-timing points.

**1. Use case worded as a 2013 forecast (USE-3, USE-8, SPLIT-9). Conceded.** This was my point 3. The fix is text only: reword `use_case` and `fit_reason` as a screen, add a `splits_comment`, and keep `approximate`. Both briefs propose the same wording, so this is settled.

**2. Unequal follow-up (LEAK-23, LEAK-24, Must). Fact conceded, remedy disputed.**
- **Conceded:** the gradient is real. Clients whose last invoice is in 2013 are 4.0% fraud (n=1,246), in 2014 5.5% (n=1,097), in 2015-2019 7.1-9.3%.
- **Size:** if the 2013-2014 leavers had the cohort rate of 7.75%, they would have about 72 more frauds (1,246 × 0.037 + 1,097 × 0.022). That is about 1.1% of the 6,504 frauds and about 3% of clients.
- **Why the filter is worse:** keeping only clients billed into 2018 or 2019 chooses the cohort by billing that happens up to six years after the prediction point. That is the USE-3 / LEAK-22 problem the critic raises in its own point 3 (779 clients dropped for not being billed after the cut). The filter would drop about 18% of the cohort (100% minus the 82% billed into 2019) to remove a 1% label shift, and it would make the future-selection problem bigger.
- **What remains:** two P4 Musts pull in opposite directions here: a fixed follow-up (LEAK-23/24) against only what is known at the prediction point (USE-3). The ranking does not settle this, so it is a weighing call for the curator.
- **My position:** a bullet that gives the gradient in numbers resolves it at lower cost. If the curator prefers the filter, choose the mildest cut that ends the step (billed into 2015, not 2019), check that the step is gone, and the dataset still ships. Either way the dataset is not excluded.

**3. Early leavers and LEAK-25. Partly conceded.**
- **Conceded:** the curator should settle the amendment together with caracas_cervical_cancer and account_debt_south_africa, using option (a) of the precedents' prompt. Add the sentence about the 779 clients active in late 2012.
- **Disputed: "before shipping".** LEAK-25 forbids shipping "no event" mixed with "not recorded". Once the 19,133 leavers are dropped, the shipped cohort no longer mixes them. They were found by their last invoice date, never by reading the label, and the kept cohort's rate is 7.75%.
- **What follows:** the shipped data meets the rule's purpose. The amendment brings the rule's wording in line with three cases, and it does not hold up this dataset. If the curator rejects option (a), caracas has to be reopened as well, which is why the three cases are decided together.

**4. "0 = not found" and the snapshot of the client record. The note is conceded; the "potential leak" label is disputed.**
- **Conceded (USE-5):** add the clause about the 0 to `predicted` or `fit_reason`. This was in my point 3.
- **Disputed:** a `Potential leak, kept on purpose:` note gives a mechanism and numbers (LEAK-38 format), and here neither exists.
  - `region` and `district` are geography; a fraud finding has no known way to change them. The claim audit's untested item is only that the data hold a single snapshot.
  - `region` has 24 codes and is the best single feature (AUC 0.597). A geographic signal is what the practitioner expects (neighbourhood features, Glauner et al. 2016).
  - Measurement outranks inference (EV-2), and calling it a leak without one has no evidence behind it.
- **Remedy:** one plain bullet: "the client record (category, region, district) is one snapshot of unknown date". If the critic wants a label, `client_catg` is the only plausible candidate. Its 22.7% fraud for category 51 could equally be a property of the category, so even then it is a note, not a leak flag.

**5. Raw rows instead of aggregates (CLEAN-19, Should). Conceded.** This was my point 2. Record the exception in the grouping definition, add a Cases line next to amex, and correct the misquote. The critic agrees that `prediction_unit="group"` answers the blind reviewer.

**6. Impossible values and `counter_number` (CLEAN-11, CLEAN-3, PROV-13, Should). Conceded, with one choice left to the curator.**
- **Conceded:** the CLEAN-11 repair. Set to missing the fields of rows with codes outside the documented sets, and `months_number` above a bound. This was my point 7.
- **`counter_number`:** whether to drop it or keep it with a note is a curator weighing call. Its AUC is at most 0.522, it does not link clients (0.502), and either choice changes no score.

**7. Text drift and record fields (writing.md, EV-8, PROV-9). Conceded in full.**

**Where this leaves the verdict:** ship after changes. The changes are wording (points 1, 3, 4, 7), the definition and record (points 5, 6, 7) and one bullet or filter (point 2). Two items go to the curator: the follow-up note against the filter (point 2) and the LEAK-25 amendment, decided with caracas and account_debt.

</details>

<details><summary>Critic rebuttal</summary>

The two briefs now agree on most points. Two disputes are left, both in the advocate's point 4: which remedy LEAK-23/24
asks for, and when LEAK-25 has to be settled.

**A1. The 2013 cut (LEAK-10, Must): conceded**

- The step at 2013Q1 holds; claims 20 and 21 confirm it.
- Moving the cut earlier finds nothing piled up before 2013 (0.692 at 2012-07, 0.687 at 2012-01).
- My brief never argued against the cut.
- I agree to cite kick, homesite and expresso, and to bring the LEAK-38 amendment together with expresso.

**A2. The split, and CLEAN-19: conceded**

- The split audit's "right with notes" holds. `prediction_unit="group"` answers the blind reviewer.
- On CLEAN-19 the advocate concedes the same remedy I asked for: write the reason into the grouping definition, add a
  Cases line, and drop the misquote. Nothing is left in dispute here.

**A3. Fit "approximate" (USE-8, USE-9): conceded**

- The advocate concedes the wording fix and the `splits_comment` (my point 1) and the clause "0 means no fraud found"
  (my point 4). Both remedies are the same as mine.
- Still open from my point 4: the advocate does not answer that `client_catg`, `region` and `district` are a snapshot
  of unknown date (column audit, problem 1; LEAK-10 Cases, "attributes looked up after the outcome").
  - `region` is the strongest single feature (AUC 0.597).
  - The data cannot show that these fields did not change after a finding.
  - The mildest remedy is a one-sentence note that names this as a potential leak. I keep this point.

**A4. The cohort: disputed on the remedy, and on when LEAK-25 is settled**

**The follow-up (LEAK-23/24)**

- **The advocate says** a note is enough, and the follow-up filter is needed only "if the mediator reads LEAK-24 as
  triggered".
- **My answer.** The trigger is already established.
  - The advocate concedes the gradient itself: 4.0% fraud for clients who leave in 2013, 5.5% in 2014, 7.1-9.3% in
    2015-2019 (claim audit, implied claims).
  - LEAK-23 and LEAK-24 are Musts. A Must that the definition can fix gets fixed, and a note is not the remedy for it
    (principles, Strengths: "fixed in the definition when it can be"). Only exclusion is out of proportion here.
  - The fix exists: "over the rows followed that long" (LEAK-23 Cases, cirrhosis).
  - The rule's own case therefore decides this against the note.
- **What I accept.** The advocate's cut, "billed into 2015 or later", instead of my 2018 or 2019. One condition: the
  fraud rate by year of last invoice must be flat over the kept years. 7.1-9.3% across 2015-2019 suggests it is, but
  nobody has measured that per year. That is the decisive experiment (EV-1). If a step remains, move the cut later.

**LEAK-25**

- **The advocate says** to "bring the amendment together" with the two other cases.
- **I agree** with the reading in option (a).
- **What I dispute** is the timing. A Must has no exceptions (principles, Exceptions and amendments). So the curator's
  amendment has to come before the dataset ships, not alongside it. This is a condition of shipping, not a note.

**The 779 clients billed in late 2012**

- Conceded as a note. The advocate offers the same remedy as I did.

**A5. Worth benchmarking (TP rules): conceded**

- I raised no value point.
- The tension "right split against score" applies.

**A6. Provenance (PROV-9): conceded**

- The advocate makes the same record fixes as my point 7: `year` 2019, and drop the stale tag.

**A7. Cleaning**

- **CLEAN-11:** conceded. The advocate offers the same repair as I did.
- **`counter_number` (CLEAN-3, Should):** partly disputed.
  - "Keep it with a note" is only an exception when the note names the meaning the identifier carries (CLEAN-3:
    "keep an identifier that carries meaning and process it into that meaning"; principles, an exception names "the
    fact that sets the case apart").
  - The advocate's own reason for keeping it, "no signal, no linkage", is the definition of an uninformative
    identifier.
  - So CLEAN-3 says drop it, unless the precedents' check (a), serial deciles against meter age, shows a meaning.
  - This is quality only: it is no reason to hold the dataset back.
- **Writing:** conceded. One AUC range with its source, and decision 1 restated as "2011-2014" or with the full range.

**Remaining conditions for "ship after changes"**

1. The follow-up filter (clients billed into 2015 or later), once the fraud rate is checked flat by last-invoice year.
2. The curator's LEAK-25 amendment, decided before shipping.
3. The text fixes both sides already agree on, plus the note on the client-record snapshot.

</details>

<details><summary>Mediator</summary>

**Recommendation (judgment record)**

```text
Verdict: ship after changes (on condition that the curator settles the LEAK-25 amendment, issue 1).
Validity: SEL holds; USE-1 holds, USE-8 approximate kept, USE-3/SPLIT-9 wording fixed (a screen, not a 2013
  forecast) + splits_comment; USE-5 note (0 = no fraud found); LEAK-10 triggered, fixed (history cut at 2013-01-01;
  LEAK-38 does not apply: named codes, verified mechanism); LEAK-24/LEAK-23 triggered, fixed (cohort billed into
  2015+); LEAK-25 departure (early leavers located and dropped), needs the curator's amendment; SPLIT-1/-3/-24/-29
  hold (grouped by client, IID gap 0.345); PROV-1/-6/-8/-9 hold (year 2019).
Value: TP holds (per-client AUC 0.62-0.70, skill +0.335, smallest test class 162 clients, no flag).
Quality: CLEAN-19 departure kept as an exception (rows usable, 0.685 vs 0.662; top-solution aggregates use the cut
  history; follows amex_non_iid_1m); CLEAN-11/PROV-13 repaired (shifted rows, months_number > 120 to missing);
  CLEAN-3 applied (counter_number dropped).
Weighed: none open; the disputed points are settled by rule.
For the curator: issue 1 (LEAK-25 amendment with caracas and account_debt); issue 2 (LEAK-38 amendment with
  expresso, does not block); confirmations in issues 3-5.
```

**Decisive measurements (run by the mediator; threads capped at 2; raw files, cohort = first invoice < 2013, last >= 2013)**

Fraud rate by year of the last invoice:

| Last invoice | Clients | Frauds | Rate |
|---|---|---|---|
| 2013 | 1,246 | 50 | 4.01% |
| 2014 | 1,097 | 60 | 5.47% |
| 2015 | 1,249 | 100 | 8.01% |
| 2016 | 1,515 | 108 | 7.13% |
| 2017 | 3,143 | 291 | 9.26% |
| 2018 | 7,044 | 527 | 7.48% |
| 2019 | 68,580 | 5,368 | 7.83% |

* **Keep 2015+:** 81,531 clients (97.2%), rate 7.84%.
  * No monotone trend over 2015-2019 (Spearman -0.002, p = 0.63).
  * The rates still differ across years (chi-square p = 0.025), but 2017 drives this by being *higher*, which is not the direction censoring would push.
  * By half-year, 2017H1-2019H2 runs 7.2-9.8% with no drift.
  * The step ends at 2015.
* **Keep 2014+:** the trend remains (2014 at 5.5%; chi-square p = 0.0015).
* **Size of the bias:** at the 2015+ rate, the 2013-2014 leavers lack about 48 + 26 = 74 frauds (1.1% of 6,504).
* **Score:** client-aggregate LightGBM (400 trees, stratified 3-fold) scores AUC 0.699 on the full cohort, 0.700 on the 2015+ clients scored by the same model, and 0.700 refit on 2015+. The filter changes no score.
* **The leavers are not random noise:** pre-2013 features predict "leaves in 2013-2014" with AUC 0.660, so their 0s are a structured bias. It is small.
* **`counter_number` meaning:**
  * Fraud rate by serial decile is flat (7.0-9.1%, no order).
  * The serial is not related to account creation year (Spearman -0.057; median creation year per decile 1995-2005, no order).
  * No meaning as a magnitude or as a vintage.
* **Client-record snapshot:**
  * Category 51 has 23.3% fraud (807 clients).
  * Its dated per-invoice tariff profile is the same before and after 2013, and for frauds and non-frauds alike (ELEC tariff 11: 98.7% vs 100% before 2013, 98.7% vs 99.5% after).
  * Category 11 and 12 profiles are also unchanged across the cut.
  * No sign of a reclassification at the finding. For `region` and `district` (geography) no mechanism is known.

**Disputed points, settled**

1. **Unequal follow-up: note or filter (LEAK-23/24 against USE-3). Critic wins; filter at 2015.**
   * The fact is measured: a censoring gradient that ends at 2015.
   * LEAK-24 is a Must. A Must the definition can fix is fixed (principles, Strengths; ladder rung 2 before rung 3). The case lines prescribe the fix: cirrhosis "over the rows followed that long", sf_permit_time "cut where follow-up is complete".
   * The advocate's USE-3 objection is not a conflict:
     * The filter selects the cohort on follow-up. It adds no information to the features, and the model cannot use it (score 0.699 vs 0.700).
     * The shipped cohort rule already selects on billing after the cut. The filter moves that same threshold from 2013 to 2015.
     * What remains is a fit gap (the evaluation covers clients who stay), written as a note under USE-8. It is not a leak.
   * Cost: 2.8% of clients, size is no issue. 2015 is the mildest cut that ends the step, so 2018/2019 is not needed.
2. **Does the LEAK-25 amendment come before shipping? Critic wins on timing.**
   * A Must has no exceptions; a departure that no higher Must forces is an amendment, and only the curator makes one (principles, Exceptions and amendments; consistency case 1).
   * Option (b) of the prompt would mean retiring the dataset, so the answer changes the verdict and cannot follow it.
   * This does not hold up the text and definition changes.
   * The advocate's reading ("located by a rule that never reads the label" counts as "recovered") is the likely answer: caracas was shipped by Lennart on that reading. Even so, it is the curator's to adopt.
   * The 2015 filter drops the 2013-2014 leavers on the same basis, so one amendment should cover both.
3. **`counter_number`: drop or keep with a note (CLEAN-3, Should). Critic wins; drop.**
   * CLEAN-3 keeps an identifier only for a meaning it carries. Departing from a Should needs a fact that sets the case apart, and the advocate offers none ("no signal, no linkage" describes an uninformative id).
   * My measurement finds no meaning (flat deciles, no vintage).
   * This follows sdss_17 `plate`/`fiber_ID` (dropped).
   * Quality only.
4. **Client-record snapshot: plain note or a `Potential leak, kept on purpose:` label (LEAK-10, LEAK-38 format). Advocate wins; plain note.**
   * The potential-leak label requires a mechanism and numbers (LEAK-38, definitions.md), and none exists. Geography has no route from a finding. For category, the dated tariffs show no reassignment.
   * Under the LEAK-10 Case "attributes looked up after the outcome", the record is kept "where the data shows they did not change": the tariff check is that evidence, though partial.
   * Write a `Note:` with the check's numbers.

**Changes to make now (no decision needed)**

1. `use_case` and `fit_reason`: "STEG, having inspected part of its clients in 2013-2019, ranks the others from their invoices before 2013"; keep `fit="approximate"` (USE-3, USE-8, SPLIT-9).
2. Add a `splits_comment`: the grouped cross-section stands in for a temporal deployment; the labels are undated, so no window or gap can be set (SPLIT-9, writing.md).
3. `predicted`: "a 0 means no fraud was found, not a verified negative" (USE-5).
4. Cohort filter: last invoice on or after 2015-01-01 (LEAK-24, LEAK-23; cirrhosis, sf_permit_time).
   * Update `changes`, the cohort bullet and decision 2 with the table above.
   * Add one note that the cohort is chosen on billing after the prediction point: it drops clients active in late 2012, the 779 of 2012H2 among them. Re-count both after the filter.
   * Rebuild only on the curator's ask (rebuild.md).
5. CLEAN-11 / PROV-13: set to missing the fields of rows with `counter_statue` or `reading_remarque` codes outside the documented sets (34 + 21 shifted invoices), and `months_number` > 120. The same rule optionally covers `counter_statue` "A" and `counter_coefficient` 0 (churn_telco_south_asia). Update the anomaly bullet.
6. Drop `counter_number` (CLEAN-3).
   * Its bullet becomes the reason: flat fraud rate across deciles, no relation to creation year.
   * Keep the "serials do not link clients (0.50-0.51)" sentence as evidence.
   * `_decisions` still uses the raw serial (fine).
7. Add a `Note:` that the client record (`client_catg`, `region`, `district`) is one snapshot of unknown date, with the tariff-profile check (LEAK-10 Case).
8. Grouping definition: give the CLEAN-19 reason (invoice rows usable, 0.685 vs 0.662; the top solutions' aggregates are built on the history the cut removes; follows amex_non_iid_1m). Remove REVIEW's misquote ("feature engineering the guidelines leave to the pipeline").
9. REVIEW issue 1:
   * Cite kick, homesite and expresso.
   * Add that LEAK-38 does not apply. Its scope is anonymised, unverified fields, and these are named codes with a measured step (0.848 to 0.69; 47.8% of frauds carry a trace).
10. Text drift:
    * Decision 1 reads "in 2011-2014", or gives the full range (21.6-42.5% vs 4.2-12.5%).
    * One AUC range for the cut, with its source, re-measured after the rebuild (now 0.62-0.70 across the probe and the audits).
    * Drop the stale `Non-IID (Temporal)` tag line.

**Issues for the curator (ranked)**

1. **LEAK-25 amendment (P4, Must). A precondition of the verdict.**
   * **Problem:** the definition drops 19,133 early leavers (21 frauds, 0.11%), and with change 4 also 2,343 leavers of 2013-2014, whose labels look unrecorded. LEAK-25 as written says "retire unless the recording process can be recovered".
   * **Effect:** without the amendment, the rule calls for retirement. With it, the shipped cohort no longer mixes "no event" with "not recorded".
   * **Advocate:** the clients are located by last invoice date, never by the label, and the kept rate is flat at 7.8%; caracas shipped on this reading.
   * **Critic:** a Must has no exceptions; this is the third silent departure (caracas, account_debt, STEG).
   * **Decision:** the precedent checker's prompt, option (a): amend LEAK-25 so that located-and-dropped counts as recovered, with Cases caracas, account_debt and STEG. Decide it together with the other two.
2. **LEAK-38 amendment (P4, Should). Does not block this dataset.** Expresso proposes it the same day. This case is the second departure on the same fact (a verified mechanism). Decide with expresso's issue 1.
3. **CLEAN-19 exception (P7, Should).** Both sides agree. An exception needs the curator's name: confirm option (a) of the precedents' prompt and add the Cases line next to amex. Optional with it: a Cases line for `mean` grouping ("a per-entity label without a date, every row one observation").
4. **Record `year` 2020 to 2019 (PROV-9, Must).** The first run was 20-22 Sep 2019. The 2020 comes from your own comment, so confirm the change.
5. **`counter_number` (P7). Only if you see a use the rules miss.** The alternative to dropping it is a within-client meter index (which meter, not a magnitude). The rule's default is to drop, and nothing measured argues otherwise.

**Agreed facts**

* The 2013-01-01 cut fixes a verified LEAK-10 leak:
  * second-meter fraud rate 7.4-11.9% per quarter in 2012 against 23.8-25.9% in 2013, with flat event counts;
  * full history 0.848-0.852, cut 0.694;
  * moving the cut earlier gains nothing (0.692, 0.687).
* The grouped split by client is right: IID 0.944 vs grouped 0.599; folds 7.75% fraud; shared serials carry no label (AUC 0.500-0.502); no temporal split is possible.
* `prediction_unit="group"` answers the blind reviewer's per-invoice concern.
* The labels are 2013-2019 findings, undated; the use case as written (a 2013 forecast) overstates what the split measures.
* A 0 means "not found" (Glauner et al. 2017).
* The cohort is chosen on billing after the cut: 779 clients active in 2012H2 dropped, fraud 1.28%.
* The task probe raises no flag: dummy 0.500, RF 0.668, skill +0.335, spread +0.091, smallest class 162, permutation p = 0.048.
* Provenance: sha256 matches, GitHub blob equal, invoice profile matches, mirror holds Zindi's train/test; indabax_drc_2022 is a duplicate; year 2019. The mirror against Zindi's train.zip remains untested (login).
* Shifted rows and impossible `months_number` touch under 0.1% of rows, with no score effect.

**Consistency with precedent**

* **Cut against keeping the full history with a note:** departs from kick/homesite (LEAK-38) on the stated fact that the fields are named and the mechanism is measured. It matches expresso the same day and follows mic and hotel_booking_demand (LEAK-10). Brought to the curator as issue 2.
* **Follow-up filter:** follows cirrhosis (LEAK-23) and sf_permit_time (LEAK-24).
* **Early leavers:** match caracas (shipped) and account_debt (pending). All three contradict LEAK-25 as written, so the rule is flagged, not followed: issue 1.
* **Raw rows:** follow amex_non_iid_1m against alfa_battle, rosbank1 and home_credit. The distinguishing facts are that the rows are usable and that the top-solution aggregates rely on the removed history. Issue 3.
* **`counter_number`:** follows sdss_17 (dropped ids). ieee `uid` does not apply (an engineered entity key with measured value).
* **Snapshot:** set apart from house_sales (dropped, renovation mechanism) by the absence of any mechanism and by the unchanged dated tariffs. Close to melbourne_housing_market (kept where the data show no change).
* **CLEAN-11:** follows churn_telco_south_asia and thyroid_discordant.
* **Year:** follows the PROV-9 cases of 2026-10-20.
* **Drift:** the precedent checker found no curator drift. The movement is in the AI's recommendations on LEAK-25 and LEAK-38, which is why both amendments are brought to you now.

</details>

<details><summary>Checklist</summary>

Prepared before the panel (verification.md, the checks marked "add", in rank order).

**Automated checks**

* `dataset list`: the class imports and validates (`grouped_non_iid`, `checked`). `uvx ruff@0.15.15 check` and
  `format --check`: clean.
* `dataset check`: 0 errors, 0 warnings, 0 info (26 checks run); 1 accepted: `splits_rows_never_tested` (860 rows,
  31 clients trimmed from a test fold by the 500k cap; the README folds add up to 1,499,140 test rows: holds).
* The README diff after the check is only template drift (new `time_gap` fields, a `REVIEW.md` row, a renamed script
  path); the checksum `v2:6e92005e...0318` is unchanged, so the definition did not drift from its evidence.
* `sync-notebooks --check`: clean (the record's `v2_path` names this `dataset.py`; the class declares `version_of`).
* Raw files: both present; sha256 match `download_description`; the invoice profile (4,476,749 x 16, 135,493 clients,
  8,275 dates, 201,893 serials) matches.

**Probes**

* Leak probes (rows, 3 splits): all features 0.629 ROC AUC; best single feature `region` 0.597, `district` 0.569; drop
  one at most -0.017 (`region`); depth-2/3 tree 0.567/0.584; exact feature copies across the split 0.5% of test rows
  (0.0% with the dates); 1-NN label agreement 0.850 against chance 0.844; label-free distance AUC 0.526. No leak flag.
* Task probes (per client, mean): dummy 0.500, linear 0.622, random forest 0.668, LightGBM 0.655, best single feature
  0.581 (`region` on all 3 splits); best family beats the dummy on 3/3 splits (skill +0.335, SE 0.011); spread RF-linear
  +0.091 (paired SE 0.023); smallest class in a test fold 162 clients. Flags: none.
* Group probes. 200,006-row sample, 8,797 clients: IID split LightGBM 0.944 vs grouped
  0.599, gap 0.345, so a random split would let the model recognise clients and the grouped split is necessary (the
  rest of this run was still going after 90 minutes). 50,010-row run, 2,206
  clients: gap 0.415; learnability per row / per client: logreg 0.619/0.619, random forest 0.584/0.612, LightGBM
  0.577/0.585, kNN 0.542/0.580; permutation test (logreg, 20 runs) 0.619 against null mean 0.491, 95% quantile 0.539,
  p = 0.048 (the smallest p 20 runs can give). Signal across clients is real but modest, which the task probe confirms
  on the full data.

**The checks**

| Rank | Check | Verdict | Evidence | Rules |
|---|---|---|---|---|
| P1 | Ethics | pass | Utility billing records with pseudonymous client ids (`train_Client_<n>`), no names or addresses; fraud detection by the utility is the stated task. No objection found. | SEL-1 |
| P2 | Scope | pass | Published as a Zindi classification challenge ("detect and recognize clients involved in fraudulent activities"); a per-client decision (whom to inspect). | SEL-2 to SEL-15 |
| P2, P5 | Real data | pass | STEG's billing data via Zindi; raw anomalies (shifted columns, `months_number` up to 412,509, 9 double entries) are marks of a real ledger, not of generation. Generated-data probes not run (not marked for a grouped real-source table). | SEL-16, PROV-3 |
| P3 | Use case and fit | concern | Actor (STEG), moment (2013-01-01), decision (inspect) are written; `fit=approximate` names its gap. The prediction date is inferred from the label footprints, not documented; the label has no date, so the horizon is 0-7 years. The panel should judge whether "approximate" is honest. | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern | Target = STEG's per-client finding; ROC AUC on one probability per client as Zindi scores. Censoring: clients billed after 2013 keep a label whose finding date is unknown (2013-2019), so late-found and not-yet-found frauds mix; early leavers (0.11% fraud) are dropped because their labels look unrecorded (measured: 21 / 19,133). | USE-5, LEAK-22 to LEAK-26, EV-5 |
| P4 | Available at prediction time | concern | Invoices from 2013 on are cut (the decision table shows the fraud-rate step 7.4-11.9% -> 23.8-25.9% at 2013Q1 for new second meters). Client fields: `creation_date` never falls after the cut (0 of 83,874), but 5,096 cohort clients have a creation date after their first invoice (fraud 6.9% vs 7.8%; `creation_date` alone AUC 0.453), so it may be rewritten on account changes; `client_catg`, `region`, `district` are single snapshots of unknown date. Inspection traces before 2013 (earlier findings) cannot be excluded. | USE-3, USE-6, LEAK-1, LEAK-2, LEAK-10 to LEAK-12, SPLIT-9, SPLIT-10 |
| P4 | Irreversible and all-row leakage | pass | No feature is built in `_clean`: the codes, readings and consumption are the source's; no label-aware or all-row transform. | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | 9 exact duplicate invoices dropped (measured: 9). 0.5% of test rows have an exact feature copy in train, 0.0% with the dates. 6,111 of 131,952 non-zero meter serials are shared by more than one cohort client; the claimed label AUC 0.51 for the other client's label is not re-measured here (claim audit). | LEAK-16 to LEAK-21, SPLIT-29 |
| P4 | Split regime | concern | Grouped by `client_id`, as the challenge's train/test split by client; IID-vs-grouped gap 0.345 confirms the grouping matters. Open: the test clients share the 2005-2012 window with training (no temporal holdout), which matches Zindi but not a deployment that trains on past findings and scores current clients (SPLIT-9, SPLIT-10); the `mean` aggregation against `any`/`last` is open (the earlier REVIEW.md issue 3); `context=all_rows`. | SPLIT-1 to SPLIT-31, USE-10, USE-11 |
| P5 | Source | pass | Zindi competition page, first run as AI Hack Tunisia #4 (20-22 Sep 2019); data from STEG. `year` 2019 in the definition against 2020 in the record (record field to settle). Raw from the Kaggle mirror, checked against a 2020 GitHub copy (sha256) and the starter notebook's profile. | PROV-1, PROV-2, PROV-8 to PROV-12, PROV-16 to PROV-18 |
| P5 | Uniqueness | pass | `indabax_drc_2022` is rejected as a duplicate of this record (CC 2026-10-12: same STEG files); the other STEG reruns are listed as `source_links` of this record, not as separate records. No other STEG folder in the working copy. | PROV-4 to PROV-7 |
| P5 | Damage and repair | pass | Damage is limited and noted: 34 + 21 shifted rows (measured: 34 invoices / 4 clients, 21 / 3 in the cohort), 806 `months_number` > 24, 29,121 invoices dated after the first run (measured: 17,616 clients, max 2019-12-07). Nothing to rebuild from the origin; the post-Sep-2019 dates do not touch the pre-2013 features. | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | pass | No task-probe flag; per-client AUC 0.62-0.67, spread between families +0.091; 162 fraud clients in the smallest test fold. | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass | Codes categorical; two dates with formats; `counter_number` 0 -> missing (12,555, measured); `consommation_level_4` dropped (0 before the cut; first non-zero 2014-01-04, measured). `counter_number` stays numeric although it is a serial: it is kept as a feature with no meaning as a magnitude (panel: identifier, CLEAN rule on identifiers?). `old_index`/`new_index` (meter readings) kept as numbers. | CLEAN-1 to CLEAN-24 |
| procedure | Notes match the code | concern | Every cleaning step in `_clean` has a bullet. Number drift: the bullet says the cut models score 0.66-0.69, the 2026-10-07 assessment and the earlier REVIEW.md say 0.61-0.69; the task probe now gives 0.62-0.67 per family. The definition has no `splits_comment` (the sub-sampling is in `version_comment`). | writing.md |
| procedure | Licence and citation | pass | `license` "Zindi Competition Rules"; the note says redistribution is forbidden and the mirror says "other" (noted, not a verdict reason). The BibTeX names Zindi and STEG and the first run. | EV-4, PROV-10 |
| procedure | Reproducibility | concern | The Kaggle command and the sha256 sums recreate the raw inputs (sha256 re-measured: match). The mirror is an anonymous re-upload and not pinned (no DOI); the Zindi original needs a login and was not compared. | |

**Cannot verify**

* That STEG set the labels from 2013 on (the cut date is inferred; no STEG or Zindi statement).
* That the Kaggle mirror equals Zindi's `train.zip` (no Zindi login used).
* The serial-sharing label AUC 0.51 and the per-rule AUCs (0.685 / 0.684 / 0.682-0.684) and the full-history 0.848:
  not re-run here; for the claim auditor.

</details>
