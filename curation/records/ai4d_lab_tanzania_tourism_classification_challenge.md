---
unique_name: ai4d_lab_tanzania_tourism_classification_challenge
name: ai4d-lab-tanzania-tourism-classification-challenge
checked_by:
- Myunghwan
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 4
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/ai4d_lab_tanzania_tourism_classification_challenge/dataset.py
source_row: 901
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: a 24,675-row NBS tourist-expenditure survey classified into six cost bins, with a stated actor and a log-loss leaderboard.
- Source: Zindi competition "AI4D Africa's Anglophone Research Lab Tanzania Tourism Classification Challenge", 2022-06-01 to 2022-07-01, 522 participants (Zindi API, read 2026-10-22); "The dataset describes 24,675 rows of up-to-date information on tourist expenditure collected by the National Bureau of Statistics (NBS) in Tanzania", from an exit survey at seven departure points. As published: Train.csv, Test.csv ("6,169 rows"), VariableDefinitions.csv; target six classes (Low, Lower, Normal, High, Higher, Highest Cost). An earlier cut of the same NBS survey was the Pycon Tanzania hackathon "Tanzania Tourism Prediction Challenge" (2020-12-12, 6,476 rows, regression on `total_cost`, MAE), the second link.
- Use case: "The model can be used by different tour operators and the Tanzania Tourism Board to automatically help tourists across the world estimate their expenditure before visiting Tanzania" (Zindi description); fit approximate: the survey is answered at departure, so trip-plan columns (party size, nights, package items) are known before the trip, while any spending or in-trip answers are not; regime IID (one survey cross-section, no date column known), so the `Non-IID (Temporal)` tag needs a check against the columns.
- Siblings and duplicates: `mmu_2022` (`TBD -> Yes`) is the same competition re-hosted on 2022-11-25 ("Tanzania Tourism Classification Challenge", same 24,675 rows, same log loss): a duplicate of this record (PROV-4); the 2020 regression cut has no record. External collections: none found.
- Papers and pages: the Zindi pages; NBS International Visitors' Exit Survey reports (not read).
- Metric: log loss over the six classes (Zindi Evaluation page: "The evaluation metric for this challenge is the Log Loss"); a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: columns answered after the trip (LEAK); the bins come from `total_cost` (whether the cut points are stated, and whether the regression framing is the better task); the 2020 6,476-row cut overlaps (PROV-6); the regime tag versus `Random (IID)`.
- Priority: gap 0 (business, multiclass and IID are not thin), use case + (tour operators and the Tourism Board named), source + (NBS survey, variable definitions), shape + (24,675 rows, mixed survey columns), risk 0.

Predict the range (bins) of expenditure a tourist spends in Tanzania; the record specifies using the 2022 multiclass version with ~24,675 rows. This is a genuine real-world tabular classification task with a clear, meaningful target and adequate size. The record carries a Temporal tag, so the split regime needs confirmation (it may simply be the year of collection rather than a true temporal dependency, in which case an IID split fits). A human must verify the row count, the number/definition of expenditure bins, and whether a temporal or random split is appropriate.

---

predict the range of expenditures a tourist spends in Tanzania

One challenge used the cost as a regression task on 2020 data with 6476 rows, the other as multi-class classification on bins with 2022 data with 24675 rows. We would use the second dataset

**Historical timing checkpoints (closed):** The two original AI checkpoint blocks below are retained verbatim as quoted history. Myunghwan closed them under the fulfilled-plan scenario in the 2026-10-23 CC immediately below; they are not current open issues.

> **Open issues (AI, 2026-10-23):** Column timing checks requested by Myunghwan for the proposed before-travel task (USE-3, LEAK-10). These are checking points, not an acceptance, rejection or automatic feature drop.
> 1. `night_mainland`, `night_zanzibar`: the dictionary defines nights already spent. Check for a separately documented pre-trip planned duration; do not relabel these realized values as plans. Highest concern.
> 2. `main_activity`: establish whether this records an activity intended/booked before travel or the main activity actually undertaken during the trip.
> 3. `tour_arrangement` and `package_transport_int`, `package_accomodation`, `package_food`, `package_transport_tz`, `package_sightseeing`, `package_guided_tour`, `package_insurance`: check whether these describe the original booking or services actually used, added or changed during the visit. Their names alone do not settle timing.
> 4. `travel_with`, `total_female`, `total_male`: lower-priority check of planned party composition versus people actually travelling or counted at exit.
> 5. `purpose`, `info_source`: lower-priority check of original trip purpose and pre-trip information source versus retrospective or in-trip answers.
> Country, age group and first-trip status have no specific later-outcome mechanism identified here. The inspected headers contain no date columns or planned/actual snapshots. Resolve the suspicious fields from the original questionnaire or source documentation before deciding retention. The earlier screening's claim that nights are known trip-plan inputs is not established. Dictionary and headers were inspected in corroborating public competition copies, not an authenticated original download: <https://github.com/dylannguyen2809/ai4d/blob/main/data/VariableDefinitions.csv>.
>
> **Open issues (AI, 2026-10-23):** Column timing checks requested by Myunghwan for the proposed before-travel task (USE-3, LEAK-10). These are checking points, not an acceptance, rejection or automatic feature drop.
>
> 1. `night_mainland`, `night_zanzibar`: the dictionary defines nights already spent. Check for a separately documented pre-trip planned duration; do not relabel these realized values as plans. Highest concern.
> 2. `main_activity`: establish whether this records an activity intended/booked before travel or the main activity actually undertaken during the trip.
> 3. `tour_arrangement` and `package_transport_int`, `package_accomodation`, `package_food`, `package_transport_tz`, `package_sightseeing`, `package_guided_tour`, `package_insurance`: check whether these describe the original booking or services actually used, added or changed during the visit. Their names alone do not settle timing.
> 4. `travel_with`, `total_female`, `total_male`: lower-priority check of planned party composition versus people actually travelling or counted at exit.
> 5. `purpose`, `info_source`: lower-priority check of original trip purpose and pre-trip information source versus retrospective or in-trip answers.
>
> Country, age group and first-trip status have no specific later-outcome mechanism identified here. The inspected headers contain no date columns or planned/actual snapshots. Resolve the suspicious fields from the original questionnaire or source documentation before deciding retention. The earlier screening's claim that nights are known trip-plan inputs is not established. Dictionary and headers were inspected in corroborating public competition copies, not an authenticated original download: <https://github.com/dylannguyen2809/ai4d/blob/main/data/VariableDefinitions.csv>.
>
>

**CC (2026-10-23, Myunghwan):** Assess expenditure category for a specified visitor and proposed trip plan, assuming the trip happens as planned. Realized plan-like attributes in historical trips can stand for the scenario inputs: nights, activity, party composition, tour arrangement and package inclusions do not need separate planned-versus-actual timing checks. Close checkpoints 1-5 above as timing objections under this scenario. Check information that cannot be supplied as a plan or known visitor context, such as realized spending, unplanned consumption or post-trip evaluations. This clarifies the task; it does not yet accept the dataset or choose a split.

**Assessment (AI, 2026-10-23):** The earlier blanket timing objections are resolved by this conditional-plan use case. The inspected header contains no actual meal-count, spending-amount or satisfaction predictor; `package_food` means food-service inclusion in the package and is a legitimate plan attribute. Keep `cost_category` target-only and assess `Tour_ID` as an identifier, not a chronological anchor. The closest scenario precedent is `in_vehicle_coupon_recommendation` (CC 2026-09-30, Lennart: hypothetical driving-scenario inputs); its respondent-grouped split is a separate property, not inherited here. The independent consistency check found no required reflection. Document that this predicts spending conditional on a plan; it does not establish causal effects of changing the plan (USE-1/3/6/8).

**CC (2026-10-23, Myunghwan):** Keep the original six expenditure classes and the source's log-loss metric. Accept a random split for the specified-plan task; no timestamp column is available. The test represents other visitors and trip plans from the represented survey population, assuming the plan is fulfilled. Remove the conflicting temporal tag. The monetary meaning/class boundaries, class support and source-file/duplicate checks remain factual work; these task choices do not establish completed data qualification.

**CC (2026-10-23, Myunghwan):** Accepted for adding and the subsequent curator review before build. Predict the original six expenditure classes for a specified visitor and trip plan, assuming the trip happens as planned; retain source log loss and random evaluation of other represented visitors/plans. Plan-like attributes remain legitimate scenario inputs. Expenditure meaning/class boundaries, class support and source/sample integrity remain factual checks during adding. Final ship and build are not approved by this screening decision.

**CC (2026-10-25, Myunghwan):** Use past observed visitor/trip records to estimate the spending category for a specified alternative trip plan, conditional on fulfillment. Use “spending category”; keep the six original labels, source log loss and represented-population stratified random evaluation. Monetary thresholds, currency and person/party or daily/trip basis remain unverified; no monetary budget or causal effect is promised. This settles the limited category interpretation in draft-1 without final ship acceptance.

**CC (2026-10-25, Myunghwan):** Retain all rows and the current stratified random evaluation after reviewing the measured profile mixture. Across nine saved folds, 9.8509% of test evaluations match training profiles and 90.1491% do not; these pool three repeats rather than distinct people. Accept both duplicate-related checker warnings with this evidence. Similar profiles do not establish a respondent/party key; preserve linkage uncertainty. This settles retention and warning application in draft-2; do not deduplicate or impose profile grouping on this basis.

**Assessment (AI, 2026-10-26):** The user-supplied official Zindi archive passed the retained CRC check; all four original files match the retained byte counts and SHA-256 hashes, rechecked locally for preparation. The archive was curator-provided; independent authenticated retrieval is not claimed. This supersedes the historical pending-source hold in draft-3. Earlier blanket timing checkpoints were already closed by the fulfilled-plan decision; actual outcome-derived fields remain subject to checking. Corrected hidden-group execution in draft-4 was completed previously. Definition notes and warning reasons now apply these choices; prior experiments remain retained, without refits. Full independent panel, ranked REVIEW.md and final curator review remain outstanding; no build or ship decision is inferred.

**Assessment (AI, 2026-10-26; direct add-stage completion):** Ready with noted concerns for curator review, not final ship acceptance. Preserve Myunghwan's fulfilled-plan six-category task, source log loss, all rows and stratified random 3 x 3 folds. Fresh source ZIP CRC/four-file byte equality, exact frame/fold reproduction and nine-fold prior-scorer checks pass; bundle checks have zero errors or active warnings and two curator-accepted duplicate warnings. Retained bounded nine-fold LightGBM/logistic log losses are 1.081636/1.125925 versus prior 1.592079; historical probability files are unavailable, so these are retained results with arithmetic checks, not newly rescored probabilities. Independent claim and blind reviews, reused exact-input column/split/domain/precedent audits, one debate/rebuttal round, mediator and cold editor are retained in the review evidence. Added held-out-record scope and measured package/party coding notes, preserving values and every CC; quoted obsolete timing checkpoints as closed history for collector compatibility. Monetary definitions, survey period, respondent linkage, questionnaire routing and exact official numerical scoring parity remain unverified. No new semantic choice or record-field disagreement is established; no REVIEW.md is retained because the format disallows keeping a panel alone. Final curator review remains. Priority 4: gap + (multiclass is thin among 133 accepted definitions), use case 0 (approximate category guidance; monetary basis unknown), source + (original supplied competition archive and codebook verified), shape + (18,506 rows, 19 mixed inputs), risk 0 (no new material defect established; explicit linkage and provenance limits remain).

**CC (2026-10-28, Myunghwan):** "ship all". Approved this dataset for shipping in the five-dataset final added-dataset review (beMTPL97, Eucalyptus, Tanzania tourism, CPS88 wages and OSSL), on the exact presented definition with previously settled task choices and disclosed limitations retained. This is scientific acceptance for a separately requested build; it does not authorize build, commit or publication.

**Assessment (AI, 2026-10-28):** The independent consistency check supports applying this overall verdict without another task choice. Existing local curator dispositions remain distinct from source verification or shared-rule amendments. No definition, scorer, data, fold or warning acceptance was changed by this final verdict.

**Maintenance (AI, 2026-10-29):** Publication-privacy cleanup removes acquisition/process details from descriptive metadata. Native format-2 rebuild `01a18ad4-f6a0-759d-a526-da34a2568066` verifies on reload and reproduces from its single traced raw input. Every data row, target, scoring semantics and all nine folds exactly match the previous build; only descriptive metadata changes the checksum. Prior containers and scientific decisions are preserved.

CC (2026-11-04, Lennart): the target `cost_category` is an ordered category, Lower Cost < Low Cost < Normal Cost < High Cost < Higher Cost < Highest Cost ("order please"), and `age_group` ordered bands ("yes use ordered categories"); CLEAN-25, CLEAN-14. The metric (log loss, the leaderboard's) is checked as declared.

**Assessment (AI, 2026-11-04):** the source lists the six classes alphabetically and gives no boundaries; Lower and Low are read as comparatives, as High < Higher < Highest are (the reading is in the definition's notes). `dataset check` passes with both orders.

CC (2026-11-04, Lennart): ship, with the ordered `cost_category` and `age_group` ("sounds good, we are ready to ship"). The build is a separate ask.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; the PR #33 review page (a light static review of the definition, README and record) raised the two typing issues, both settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (text only, no change to data, target, metric or split; rebuild on the curator's ask. Made in the definition: the label is the party's total trip spending in TZS, bands at about 0.5M / 1M / 5M / 10M / 50M, 97.9% agreement on 2,401 rows linked to the 2020 cut (USE-5, EV-2); the 2020 cut is an earlier subset, a PROV-6 duplicate version, not a different task; year 2022 under PROV-9; `ForcedIIDFromTemporal` under SPLIT-8; the 965 copies kept under LEAK-19's distinct-entity clause, a profile-grouped split costs +0.0047 log loss; no leak and no exploit. This supersedes "no panel ran" above; the 2026-10-26 "retained in the review evidence" has no artefact behind it; `mmu_2022` is `No` / `Duplicate`, not `TBD -> Yes`; the screening's regression-framing risk is answered: keep the six classes, the cost exists only for the 4,809-row 2020 subset); disputed: SPLIT-8 (the tag stays unless the planner actor is replaced), PROV-6 (a record for the 2020 cut), MET-2 (the scorer's class column order, harness or dataset), LEAK-19 (exception line or note, settled as a note; issue 7); for the curator: issues 3-8. Priority 4: gap +, use case 0, source +, shape +, risk 0 (gap: multiclass is thin among the 162 accepted definitions; use case: Zindi names the planner, but the fit is approximate and a better-fitting actor is open, issue 3; source: NBS survey with Zindi's codebook and metric; shape: 18,506 rows, 19 mixed features; risk: no leak, the open issues are the actor, bookkeeping and the harness).

CC (2026-11-05, Lennart): the survey statistician joins the trip planner as actor (REVIEW.md issue 3, B): NBS and the Bank of Tanzania fill in a departing respondent's spending band from the rest of the exit form when the expenditure answer is missing or implausible. `use_case`, `known` and `fit_reason` name both; the `ForcedIIDFromTemporal` tag stays, since the planner still looks forward; no data change.

CC (2026-11-05, Lennart): the 2020 Pycon / Zindi "Tanzania Tourism Prediction" cut gets a `No` / `Duplicate` record, `tanzania_tourism_prediction`, naming this record as canonical (issue 4, B; PROV-6).

CC (2026-11-05, Lennart): `checked_by` gets Lennart, in line with the ten records shipped on 2026-11-04 (issue 6, B).

CC (2026-11-05, Lennart): `mmu_2022` confirmed as a duplicate of this record; its `checked_by` is Lennart (issue 8, B; PROV-5).

CC (2026-11-05, Lennart): the declared metric (log loss over the six classes, the source's) is checked and stays as declared.

CC (2026-11-05, Lennart): the 965 exact copies stay under LEAK-18 (few coarse features, plausible repeats, as sepsis_survival_minimal_clinical_records), not by widening LEAK-19 (REVIEW.md issue 7, answered (d)): 17 of 19 inputs are coarse survey answers, and the copies are distinct respondents.

CC (2026-11-05, Lennart): the scorer reads probability columns in the sorted order of the class labels (scikit-learn's classes_) and checks named columns; the ordered categories stay metadata (issue 5, C; MET-2).

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.
