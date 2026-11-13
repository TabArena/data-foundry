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
tags:
- 'Samples: Unknown'
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

**Assessment (AI, 2026-10-26):** The user-supplied official Zindi archive passed the retained CRC check; all four original files match the retained byte counts and SHA-256 hashes, rechecked locally for preparation. The archive was curator-provided; independent authenticated retrieval is not claimed. This supersedes the historical pending-source hold in draft-3. Earlier blanket timing checkpoints were already closed by the fulfilled-plan decision; actual outcome-derived fields remain subject to checking. Corrected hidden-group execution in draft-4 was completed previously. Definition notes and warning reasons now apply these choices; prior experiments remain retained, without refits. Full independent panel, ranked the Review and final curator review remain outstanding; no build or ship decision is inferred.

**Assessment (AI, 2026-10-26; direct add-stage completion):** Ready with noted concerns for curator review, not final ship acceptance. Preserve Myunghwan's fulfilled-plan six-category task, source log loss, all rows and stratified random 3 x 3 folds. Fresh source ZIP CRC/four-file byte equality, exact frame/fold reproduction and nine-fold prior-scorer checks pass; bundle checks have zero errors or active warnings and two curator-accepted duplicate warnings. Retained bounded nine-fold LightGBM/logistic log losses are 1.081636/1.125925 versus prior 1.592079; historical probability files are unavailable, so these are retained results with arithmetic checks, not newly rescored probabilities. Independent claim and blind reviews, reused exact-input column/split/domain/precedent audits, one debate/rebuttal round, mediator and cold editor are retained in the review evidence. Added held-out-record scope and measured package/party coding notes, preserving values and every CC; quoted obsolete timing checkpoints as closed history for collector compatibility. Monetary definitions, survey period, respondent linkage, questionnaire routing and exact official numerical scoring parity remain unverified. No new semantic choice or record-field disagreement is established; no review is retained because the format disallows keeping a panel alone. Final curator review remains. Priority 4: gap + (multiclass is thin among 133 accepted definitions), use case 0 (approximate category guidance; monetary basis unknown), source + (original supplied competition archive and codebook verified), shape + (18,506 rows, 19 mixed inputs), risk 0 (no new material defect established; explicit linkage and provenance limits remain).

**CC (2026-10-28, Myunghwan):** "ship all". Approved this dataset for shipping in the five-dataset final added-dataset review (beMTPL97, Eucalyptus, Tanzania tourism, CPS88 wages and OSSL), on the exact presented definition with previously settled task choices and disclosed limitations retained. This is scientific acceptance for a separately requested build; it does not authorize build, commit or publication.

**Assessment (AI, 2026-10-28):** The independent consistency check supports applying this overall verdict without another task choice. Existing local curator dispositions remain distinct from source verification or shared-rule amendments. No definition, scorer, data, fold or warning acceptance was changed by this final verdict.

**Maintenance (AI, 2026-10-29):** Publication-privacy cleanup removes acquisition/process details from descriptive metadata. Native format-2 rebuild `01a18ad4-f6a0-759d-a526-da34a2568066` verifies on reload and reproduces from its single traced raw input. Every data row, target, scoring semantics and all nine folds exactly match the previous build; only descriptive metadata changes the checksum. Prior containers and scientific decisions are preserved.

CC (2026-11-04, Lennart): the target `cost_category` is an ordered category, Lower Cost < Low Cost < Normal Cost < High Cost < Higher Cost < Highest Cost ("order please"), and `age_group` ordered bands ("yes use ordered categories"); CLEAN-25, CLEAN-14. The metric (log loss, the leaderboard's) is checked as declared.

**Assessment (AI, 2026-11-04):** the source lists the six classes alphabetically and gives no boundaries; Lower and Low are read as comparatives, as High < Higher < Highest are (the reading is in the definition's notes). `dataset check` passes with both orders.

CC (2026-11-04, Lennart): ship, with the ordered `cost_category` and `age_group` ("sounds good, we are ready to ship"). The build is a separate ask.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; the PR #33 review page (a light static review of the definition, README and record) raised the two typing issues, both settled.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (text only, no change to data, target, metric or split; rebuild on the curator's ask. Made in the definition: the label is the party's total trip spending in TZS, bands at about 0.5M / 1M / 5M / 10M / 50M, 97.9% agreement on 2,401 rows linked to the 2020 cut (USE-5, EV-2); the 2020 cut is an earlier subset, a PROV-6 duplicate version, not a different task; year 2022 under PROV-9; `ForcedIIDFromTemporal` under SPLIT-8; the 965 copies kept under LEAK-19's distinct-entity clause, a profile-grouped split costs +0.0047 log loss; no leak and no exploit. This supersedes "no panel ran" above; the 2026-10-26 "retained in the review evidence" has no artefact behind it; `mmu_2022` is `No` / `Duplicate`, not `TBD -> Yes`; the screening's regression-framing risk is answered: keep the six classes, the cost exists only for the 4,809-row 2020 subset); disputed: SPLIT-8 (the tag stays unless the planner actor is replaced), PROV-6 (a record for the 2020 cut), MET-2 (the scorer's class column order, harness or dataset), LEAK-19 (exception line or note, settled as a note; issue 7); for the curator: issues 3-8. Priority 4: gap +, use case 0, source +, shape +, risk 0 (gap: multiclass is thin among the 162 accepted definitions; use case: Zindi names the planner, but the fit is approximate and a better-fitting actor is open, issue 3; source: NBS survey with Zindi's codebook and metric; shape: 18,506 rows, 19 mixed features; risk: no leak, the open issues are the actor, bookkeeping and the harness).

CC (2026-11-05, Lennart): the survey statistician joins the trip planner as actor (Review issue 3, B): NBS and the Bank of Tanzania fill in a departing respondent's spending band from the rest of the exit form when the expenditure answer is missing or implausible. `use_case`, `known` and `fit_reason` name both; the `ForcedIIDFromTemporal` tag stays, since the planner still looks forward; no data change.

CC (2026-11-05, Lennart): the 2020 Pycon / Zindi "Tanzania Tourism Prediction" cut gets a `No` / `Duplicate` record, `tanzania_tourism_prediction`, naming this record as canonical (issue 4, B; PROV-6).

CC (2026-11-05, Lennart): `checked_by` gets Lennart, in line with the ten records shipped on 2026-11-04 (issue 6, B).

CC (2026-11-05, Lennart): `mmu_2022` confirmed as a duplicate of this record; its `checked_by` is Lennart (issue 8, B; PROV-5).

CC (2026-11-05, Lennart): the declared metric (log loss over the six classes, the source's) is checked and stays as declared.

CC (2026-11-05, Lennart): the 965 exact copies stay under LEAK-18 (few coarse features, plausible repeats, as sepsis_survival_minimal_clinical_records), not by widening LEAK-19 (Review issue 7, answered (d)): 17 of 19 inputs are coarse survey answers, and the copies are distinct respondents.

CC (2026-11-05, Lennart): the scorer reads probability columns in the sorted order of the class labels (scikit-learn's classes_) and checks named columns; the ordered categories stay metadata (issue 5, C; MET-2).

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. The AI recommends shipping after a rebuild on your ask: the panel said ship after changes
(mediator), and those changes, all text in `dataset.py`, are made; six calls are left (issues 3-8). Validity: USE-1
holds with an approximate fit; USE-5 holds (the label is the party's total trip spending in Tanzanian shillings,
cut at about 0.5M / 1M / 5M / 10M / 50M, now in the notes); USE-9 open, a better-fitting actor exists (issue 3);
LEAK-10 holds (no leak, no exploit); the 965 exact copies kept as distinct respondents under LEAK-19 (issue 7), with
a residual risk that some are two spouses of one party (LEAK-17), worth at most about 0.005 log loss; SPLIT-1 and
SPLIT-4 hold; SPLIT-8 triggered, fixed by the `ForcedIIDFromTemporal` tag, which goes if issue 3 replaces the
planner; PROV-1, PROV-4 and PROV-6 hold (the 2020 competition is an earlier subset, not shipped; issues 4 and 8);
PROV-9 keeps 2022. Value: TP holds (prior 1.592, models 1.076-1.126, RF beats linear by 0.012, SE 0.001); MET-4
holds; MET-2 holds for the definition, with a scorer risk (issue 5). Quality: CLEAN-3, CLEAN-11, CLEAN-14 and
CLEAN-25 hold. Weighed: source + (NBS survey, the competition's metric), size +, use case − (actor mismatch), gap +
(multiclass is thin).

**Main points:** Keep the tour-operator actor, add the survey statistician next to it, or replace it (issue 3); then
smaller calls: the copies kept under LEAK-19 (issue 7), a duplicate record for the 2020 cut (issue 4), confirming
`mmu_2022` (issue 8), a guard on the scorer's class-column order (issue 5) and `checked_by` (issue 6).

**Record judgment:** valid; NBS's exit survey as Zindi published it in 2022, with the competition's own task and
metric. Four out-of-date statements (the 2026-10-26 "retained in the review evidence", the screening's `mmu_2022`
(`TBD -> Yes`), the unanswered regression-framing risk, and "no panel ran") are corrected in the record's dated panel
line of 2026-11-04. The record fields agree with the definition.

**Issues for Lennart:**

3. **Which actor: the trip planner, the survey statistician, or both?**

   * **Problem:**
     - The definition's actor is a tour operator or the Tourism Board estimating the spending band of a planned trip,
       but an operator quotes from an exact rate card (park fees, lodge tier, vehicle days), so a six-band guess with
       57.6% top-1 accuracy does not change its decision (domain practitioner).
     - The survey's own users, NBS and the Bank of Tanzania, estimate tourism earnings from the exit survey and need to
       fill in a respondent's spending band from the rest of the form when the expenditure answer is missing or
       implausible.
     - That actor has every input when it predicts (the form is complete at departure), and its test is "other
       respondents of the same survey", which is what the random folds measure.
   * **Background:** Under the planner, the nights, activities and package items recorded after the trip stand in for
     a plan made before it (Myunghwan's CC of 2026-10-23); under the statistician they are the inputs that actor really
     has, so this approximation goes. The `ForcedIIDFromTemporal` tag marks a split kept random only because the release
     has no dates, where the use case looks forward[^3-tag]. The rules ask to check for a use case the data mirrors
     before settling on an approximate fit, weighed against "a use case rephrased only to excuse a gap"[^3-mirror].
     That factor does not bite here: the rephrase removes a real stretch and excuses no label gap.
   * **Effect on the task:** Under the planner, the random folds overstate how well a model from one survey wave bins
     next season's trips (prices in shillings drift); under the statistician they measure exactly its use. Data, split
     and metric stay in every option. If the statistician replaces the planner, the task is cross-sectional by its use
     case, so the tag's rule no longer applies and the tag and the forward-looking sentence of `splits_comment`
     go[^3-tag]. If the statistician is added next to the planner, the use case still looks forward and the tag stays.
     The fit stays approximate either way: six bands are coarser than the amount either actor needs[^3-label].
   * **Consistency:** For keeping the planner: Zindi names it ("help tourists across the world estimate their
     expenditure before visiting Tanzania"), and it is the basis of Myunghwan's CCs of 2026-10-23 and 2026-10-25 and of
     your ship call. Precedent: in_vehicle_coupon_recommendation matches the plan-as-scenario reading only in part (its
     inputs are hypothetical scenarios written into the survey, not realized trips).
   * **Panel:** The advocate and the domain practitioner propose B or C; the mediator leaves it to you. That the tag
     stays under B is the critic's point; the advocate agreed in rebuttal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The planner alone (implemented) | actor a tour operator or the Tourism Board; fit approximate; tagged `ForcedIIDFromTemporal` | the actor Zindi names; the basis of the CCs and your ship call | an operator quotes from a rate card; realized trip values stand in for the plan |
     | B | Add the statistician next to the planner | rewrite of `use_case`, `known` and `fit_reason`; the tag stays; no data change | keeps the source's actor; names the one the data mirrors | a rewrite of three fields |
     | C | Replace the planner by the statistician | rewrite of `use_case`, `known`, `fit_reason` and `splits_comment`; the tag and the plan stretch go; no data change | inputs and random folds match its use exactly | the source's actor goes; a rewrite of four fields |

   * **Recommendation:** B, which keeps the source's actor and names the one the data mirrors. **Decision:** keep (A),
     add alongside (B), or replace (C)?

   **Notes for the AI:** on B, rewrite `use_case`, `known` and `fit_reason`; on C, also `splits_comment` (its
   forward-looking sentence goes) and remove the `ForcedIIDFromTemporal` tag. No data change in either.

   [^3-mirror]: **USE-9** (Should): before settling on approximate, ask whether the data as shipped mirrors another
     well-defined use case; weighed against the factor "a use case rephrased only to excuse a gap" (−).
   [^3-tag]: **SPLIT-8**: the rule behind the `ForcedIIDFromTemporal` tag; it no longer applies once the task is
     cross-sectional by its use case.
   [^3-label]: **USE-5**: predict what the actor would act on, at the resolution they act on it.

   **Lennart (2026-11-05, change):** Option B: Add the statistician next to the planner. Do B

   **Resolved (2026-11-05, Lennart):** B. The survey statistician (NBS, the Bank of Tanzania) joins the planner in
   `use_case`, `known` and `fit_reason`; the `ForcedIIDFromTemporal` tag stays; no data change; `dataset check` clean.

7. **Keep the 965 exact copies as distinct respondents?**

   * **Problem:**
     - An exact copy is a row equal to another in every feature and the label; the rule on copies drops them, and its
       clause that keeps them names distinct compounds the descriptors cannot tell apart (hiva_agnostic,
       qsar_tid_11)[^7-copies].
     - The mediator read that clause for survey respondents, so the notes carry the reason and no exception line is
       written.
   * **Effect on the task:** 9.85% of test rows have a twin in training; a split grouped by feature profile costs
     +0.0047 log loss, so the scores are barely optimistic.
   * **Evidence:** For distinct people: 361 repeated profiles are `Alone` travellers (213 with more than one label), and
     67.8% of copy groups are larger than their party.
   * **Consistency:** audiology_diagnosis went the other way (27 copies on different patient ids dropped). What sets
     this apart from audiology_diagnosis: 17 of 19 inputs are coarse survey answers with 2 to 10 levels, so real
     respondents repeat.
   * **Panel:** The critic and the precedent checker asked for an exception; the mediator kept the reason in the notes
     under the clause.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the reason in the notes (implemented), widen the clause | copies kept; the clause widened to distinct entities, an amendment with this case as its row | the mediator's reading | changes the rule |
     | B | An exception with the fact above | copies kept; an exception line naming the coarse survey answers | what the critic and the precedent checker asked for | an exception instead of the rule's clause |
     | C | Drop the copies | the 965 copies leave, as in audiology_diagnosis | follows audiology_diagnosis | drops respondents the evidence shows are distinct people |

   * **Recommendation:** A. **Decision:** A, B or C?

   **Notes for the AI:** implemented: kept, with the reason in the notes; no Cases row in leak_checks.md yet. On A,
   amend LEAK-19's clause to distinct entities (this case as its row); on B, write an `Exception to LEAK-19` line with
   the fact that sets it apart (17 of 19 inputs are coarse survey answers with 2 to 10 levels).

   [^7-copies]: **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped on the
     duplicate key; distinct compounds that the descriptors cannot tell apart stay, with the reason in the notes.

   **Consistency check (AI, 2026-11-05):** keeping the copies under a LEAK-19 clause widened to "distinct entities"
   differs from audiology_diagnosis, whose 27 copies on distinct patient ids were dropped as an artifact of its coarse,
   categorical findings: "distinct entities" covers audiology too, and coarse answers are the reason it dropped. What
   sets ai4d apart?
   - (a) evidence of distinct people beyond the profile (361 `Alone` profiles, 67.8% of copy groups larger than their
     party), written into the amended clause, so audiology stays a drop;
   - (b) drop the copies as audiology did (option C);
   - (c) reopen audiology_diagnosis;
   - (d) keep them under LEAK-18 (few coarse features, plausible repeats, as sepsis_survival) instead of amending
     LEAK-19.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, ok):** Reply (d): keep them under LEAK-18 (few coarse features, plausible repeats, as
   sepsis_survival) instead of amending LEAK… (d)

   **Resolved (2026-11-05, Lennart):** (d). The copies stay under LEAK-18 (few coarse features, plausible repeats), with
   this case added to its Cases beside sepsis_survival_minimal_clinical_records; LEAK-19 is not widened.

4. **Create a `No` / `Duplicate` record for the 2020 cut?**

   * **Problem:**
     - The 2020 Pycon / Zindi "Tanzania Tourism Prediction" (6,476 rows, regression on `total_cost`, MAE) is an earlier
       subset of this release, and a swapped target with added rows is a duplicate version, not a distinct task (the
       notes now say so)[^4-dup].
     - The 2020 cut has no record, so a later screening could take it for a distinct task[^4-distinct], a misreading
       that already happened once in this pass (precedent checker, item 6).
   * **Experiments:** 72.3% of its 4,809 training rows match a row here, against 23.4% by chance and about 75% if all of
     it sits inside the 24,675.
   * **Effect on the task:** None on the benchmark today; nothing ships twice.
   * **Background:** The duplicate rule settles that it is a duplicate[^4-dup]. No rule requires a record for a
     duplicate nobody screened, so this is a new screening verdict.
   * **Consistency:** indabax_eswatini_2022 (duplicate by Zindi file size, Lennart 2026-10-12).
   * **Panel:** The critic: required; the advocate: optional.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No record (implemented) | nothing changes | nothing ships twice | a later screening could take the 2020 cut for a distinct task |
     | B | A `No` / `Duplicate` record | one record naming this record as canonical | stops that misreading | one record to write |

   * **Recommendation:** B, create it. **Decision:** create the record (B) or not (A)?

   [^4-dup]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates when neither adds a
     distinct task: a swapped target, added or dropped rows or columns.
   [^4-distinct]: **PROV-7** (Must): records that share a source but give different tasks are not duplicates.

   **Lennart (2026-11-05, change):** Option B: A No / Duplicate record. Follow the recommendation

   **Resolved (2026-11-05, Lennart):** B. New record `tanzania_tourism_prediction`: `No` / `Duplicate`, naming this
   record as canonical, checked by Lennart.

8. **Confirm `mmu_2022` as a duplicate?**

   * **Problem:**
     - `mmu_2022` is this competition re-hosted on 2022-11-25 (same description, six-class log loss, same file sizes).
     - It is `No` / `Duplicate` with no folder, but its `checked_by` is only `AI (UNVERIFIED)`: the AI checked the
       source, no curator has[^8-source].
   * **Effect on the task:** None on shipping.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unconfirmed (implemented) | `checked_by` stays `AI (UNVERIFIED)` | no effect on shipping | no curator has checked the source |
     | B | Confirm | add `Lennart` to its `checked_by` | a curator has checked the source | no effect on shipping |

   * **Recommendation:** B, confirm. **Decision:** confirm (B) or not (A)?

   [^8-source]: **PROV-5** (Must): confirm the source before marking a duplicate.

   **Lennart (2026-11-05, change):** follow the recommendaiton

   **Resolved (2026-11-05, Lennart):** B. `mmu_2022` is confirmed: its `checked_by` is Lennart instead of AI
   (UNVERIFIED), with a CC line.

5. **Guard the class-column order of the scorer for all ordered targets?**

   * **Problem:**
     - `data_foundry.v2.metrics.scorer` reads the probability columns in the target's category order, which is
       Lower … Highest since your ordering of 2026-11-04.
     - Columns in alphabetical order (Zindi's submission header, and scikit-learn's `classes_` on strings) score 2.537
       instead of 1.592 for the same prior, without an error.
     - The same holds for the other ordered multiclass targets (cardiotocography, dementia_prediction,
       hepatitis_c_prediction, chicago_traffic_crashes).
   * **Effect on the task:** A harness that passes scikit-learn's column order reports a much worse log loss on all
     five datasets, with no error: the score no longer measures what it claims[^5-score].
   * **Background:** The example `benchmark_on_beyond_arena.py` reindexes, so a careful harness scores right. Results
     on the old container `01a18ad4…` were consistent with that container; the risk is mixing them with results on the
     new one. The definition needs no change; after the rebuild only the new container is scored (house rule), so no
     rescoring decision is needed.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nothing (implemented) | no change | none needed in the definition | a harness in scikit-learn's order scores wrong, without an error |
     | B | A README line | on every ordered target, a line saying probabilities are scored in the declared class order | text only | the scorer still takes any column order |
     | C | A label check in the scorer | repo-wide, the scorer fails when the columns are unnamed or out of order | a wrong order fails instead of scoring | a change to the shared scorer |

   * **Recommendation:** C. **Decision:** B, C or neither (A)?

   [^5-score]: **MET-2** (Must): match the data, the metric and the real task; the score measures what it claims.

   **Lennart (2026-11-05, change):** Option C: A label check in the scorer. Add a label check, but also make sure we
   follow the sklearn and default convention of scoring by it being sorted no? we dont want to change this, just the
   metadata we have as needed

   **Answer (AI, 2026-11-05):** Yes: follow scikit-learn's convention, change nothing in the data, and keep the order of
   the classes as metadata only. Today the scorer reads the probability columns in the order of the target's categories,
   which for an ordered target is its declared order (Lower Cost to Highest Cost). scikit-learn, LightGBM and TabPFN
   return `predict_proba` columns in sorted order (`classes_`), so a harness that passes them on unchanged scores 2.537
   instead of 1.592 here. The change, in the shared scorer only:
   - the probability columns are read in the sorted order of the class labels for every target; the ordered categories
     stay in the container unchanged, as type information;
   - the label check: probabilities passed as a table whose columns are the class names are matched by name, and a
     missing or unknown class fails; a plain array is read in sorted order, and the docstring and the examples say so;
   - unordered targets do not change (their categories are already sorted), nor do binary ones (no binary target is
     ordered); the five ordered multiclass targets (cardiotocography, dementia_prediction, hepatitis_c_prediction,
     chicago_traffic_crashes and this one) move from category order to sorted order.

   Is that what you meant? Then mark Change to C again with "yes" in the note, and I apply it with tests.

   **Lennart (2026-11-05, change):** Agree. Option C: A label check in the scorer.

   **Resolved (2026-11-05, Lennart):** C, as answered. The shared scorer reads probability columns in the sorted order
   of the class labels (scikit-learn's `classes_`) for every target, and a DataFrame of probabilities is matched by its
   column names (a missing, unknown or duplicate class fails); the ordered categories stay in the container as type
   information. Only the five ordered multiclass targets change column order; no binary target is ordered, so no
   positive class moves. The examples, CLAUDE.md, the benchmark notes and tests follow; the full suite passes.

6. **Add `Lennart` to `checked_by`?**

   * **Problem:**
     - The record's `checked_by` lists only Myunghwan.
     - The ten other records you shipped on 2026-11-04 (e.g. bemtpl97, chicago_traffic_crashes) list you as well.
   * **Background:** No rule covers it; it is a consistency check of the ship call.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As is (implemented) | `checked_by: [Myunghwan]` | no change | out of line with the ten siblings |
     | B | Add `Lennart` | if it was missed when the CC was applied | in line with the ten siblings | |
     | C | Leave it on purpose | the PR #33 review was a light static review; the record says so | the record states why | out of line with the ten siblings |
     | D | Remove `Lennart` from the ten siblings | the siblings match this record | consistent | changes ten records |
     | E | Change how `checked_by` is filled | a new way to fill it after a review-page verdict | | a process change |

   * **Recommendation:** B. **Decision:** A, B, C, D or E?

   **Notes for the AI:** options B to E are the precedent checker's (a) to (d).

   **Lennart (2026-11-05, change):** Option B: Add Lennart. add checked by

   **Resolved (2026-11-05, Lennart):** B. `checked_by` lists Lennart.

**Review panel:** ship after changes (mediator). Tier full, second pass after Lennart's PR #33 review of 2026-11-04.
The mediator's issues 1-4 are issues 3-6 here (its issue 2 is split into issues 4 and 8).
Claims: 21 rows audited (about 45 claims), 14 hold, 2 refuted (the label "undocumented" and the 2020 cut "a different
task"; both fixed in the notes), 1 contested (the year, settled as 2022 under PROV-9), 1 harness risk (the scorer's
column order, issue 5), 3 untested (the 2026-10-26 scores, the "retained" reviews, the stale build). Blind review:
include; its main concern, the ordered target scored as plain multiclass, is answered (the ranked probability score
ranks the models the same way, so MET-4 holds). Task gamer: no exploit; its best attempt, engineered party size and
total nights, gains 0.0038 against a noise band of 0.0049 and is signal a deployed model has. Agreed: no leak
(LEAK-10), the IID split is honest (SPLIT-4, SPLIT-31), the label is identified (USE-5), six classes and log loss
(MET-4), every cleaning count, the year 2022 (PROV-9). Disputed: SPLIT-8 (the tag stays unless the planner is
replaced, issue 3), PROV-6 (a record for the 2020 cut, issue 4), MET-2 (harness or dataset action, issue 5); LEAK-19
(an exception line or a note) was settled by the mediator as notes under the distinct-entity clause.

<details><summary>Mediator</summary>

**Mediator: `ai4d_lab_tanzania_tourism_classification_challenge`, second pass, 2026-11-04**

**Recommendation**

```text
Verdict: ship after changes (text only: no change to data, target, metric or split; rebuild on the curator's ask).
Validity: SEL holds; USE-1 holds (fit approximate); USE-5 holds, but the notes misstate it (fix, change 1);
  USE-9 not weighed (issue 1); LEAK-10 holds (no leak, no exploit); LEAK-17 residual risk of about 0.005 or less
  (note); LEAK-19 keep falls under the rule's distinct-entity clause (note, change 4); SPLIT-1 and SPLIT-4 hold;
  SPLIT-8 triggered, fixed by a tag (change 3); PROV-1 holds (bytes match); PROV-4 and PROV-6 hold, but the
  stated reason is false (fix, change 2); PROV-9: 2022 holds (change 2).
Value: TP holds (prior 1.592, models 1.076-1.12, RF beats linear by 0.012, SE 0.001); MET-4 holds; MET-2 holds for
  the definition (harness point, issue 3).
Quality: CLEAN-3, -11, -14 and -25 hold; travel_with NA and long stays kept with notes.
Weighed: source + (NBS survey, competition metric), size +, use case − (actor mismatch), gap + (multiclass).
For the curator: issue 1 (which actor), issue 2 (mmu_2022 / 2020-cut records), issue 3 (scorer column order),
  issue 4 (checked_by).
```

**Changes to make now (no decision needed)**

1. **USE-5 (Must) with EV-2: rewrite `predicted`, `fit_reason` and `curation_comments`.** The label is the party's total trip expenditure in TZS. The bands are about <0.5M / 0.5–1M / 1–5M / 5–10M / 10–50M / >50M. Say the bands are approximate because they were reconstructed from a third-party copy of the 2020 files.
   - `fit` stays `approximate`. What remains unknown is the survey year, the linkage between respondents, and the plan-as-realized inputs.
   - This updates the facts behind Myunghwan's CC of 2026-10-25 ("remain unverified"). It does not change his choices: six classes, log loss, and no monetary budget promised.
   - Settled for the critic: the notes now state a measured falsehood, so the fix is a condition for shipping. The advocate agreed to the edit.
2. **PROV-6 (Must): replace "the 2020 regression competition is a different published task/cut".** New text: "an earlier 2020 subset of the same survey with the raw TZS cost; a duplicate version under PROV-6, not shipped".
   - **PROV-8/9 (Must): keep `year = "2022"` and add a one-line reason.** The 2020 file holds neither the target nor about 74% of our rows, so it fails the airfoil test (an earlier publication must hold every value). melbourne_housing_market was one upload growing over its versions; here there are two competitions, each with its own launch. The critic conceded this. The rule decides it, so it does not go to the curator.
3. **SPLIT-8 (Must; splits.md l.59): add `ForcedIIDFromTemporal` and one sentence in `splits_comment`.** The sentence: a dated survey wave would test drift of the TZS band edges and of the visitor mix; recover it if NBS publishes it; there is no valid window to measure the cost.
   - The current actor plans a future trip ("before visiting"), and the release has no dates. That is SPLIT-8's text word for word, and the snapshot precedents carry the tag.
   - This does not contradict Myunghwan's CC of 2026-10-23. That CC removed `Non-IID (Temporal)`, a different regime; the split stays IID.
   - Settled for the critic: adding a second actor next to the planner leaves the use case forward-looking. The tag lapses only if issue 1 *replaces* the planner.
4. **LEAK-19 (Should), LEAK-18, LEAK-17 (Must): rewrite the copy notes and both `accepted_check_warnings` texts.**
   - The copies are distinct respondents the coarse features cannot tell apart:
     - 361 repeated profiles are `Alone`, and 213 of those carry more than one label;
     - 67.8% of copy groups are larger than the party size.
   - This is LEAK-19's own clause ("distinct [entities] that the descriptors cannot tell apart stay, with the reason in the notes"; hiva_agnostic). So it needs a reason in the notes, not an `Exception to` line.
   - Add the measured effect (EV-8): a split grouped by profile costs +0.0047 log loss (+0.0025 without `age_group`), and the copy-lookup attacks gained nothing (1.0765 against 1.0755).
   - Name the residual LEAK-17 risk: `With Spouse` is enriched among the copy rows (44.6% against 27.8%), bounded at about 0.005 or less. SPLIT-24 forbids grouping on a feature hash.
   - Add a leak_checks.md Cases row of kind `applied`.
   - This settles the panel's exception dispute: the numbers go in, but as notes under the clause.
5. **Writing rule: correct the record with dated lines.**
   - The 2026-10-26 claim that the reviews are "retained in the review evidence" has no artefact behind it.
   - The screening line "`mmu_2022` (`TBD -> Yes`)" is stale; it is now `No`.
   - Answer screening risk 37 (is the regression framing better?): keep the classes. The regression target exists only for the 4.8k-row subset, and log loss is the competition's metric (USE-5, MET-4).
   - The precedent checker's item 6 repeated the false "distinct task" premise. Do not carry it forward.
6. **Notes, P7.**
   - LEAK-8: `travel_with` NA rows are 97.2% one-person parties (1,045 of 1,075). Keep them missing.
   - CLEAN-11: 54 trips exceed 90 nights and 1 row has 371. Keep them. The column auditor's USE-7 citation does not apply, because USE-7 is about rows lacking the input. Dropping the 371-night row would need a CC.
7. **House rule:** add a dated `CHANGELOG.md` entry. The README says `build_stale: true`, so rebuild on the curator's ask and score only on the new container.

**Issues for the curator, ranked**

**1. P3, USE-9 (Should, weighed against "a use case rephrased only to excuse a gap"): which actor?**
- **Problem:** the named actor (a tour operator or tourism board planning a trip) quotes from an exact rate card. A six-band label with 0.576 top-1 accuracy does not fit that decision.
- **The alternative actor:** the survey statistician (NBS / Bank of Tanzania) imputing a respondent's band from the rest of the exit form. That actor has every input at the right moment and matches the random split.
- **For keeping the planner:** Zindi names it; it is the source's stated use; it is the current CC basis (Myunghwan 2026-10-23/25, Lennart ship).
- **For the statistician:** the domain practitioner shows the timing and split match exactly. The rewrite does not excuse the label gap: the fit stays approximate because a band is coarser than the number either actor needs (USE-5).
- **Effect:**
  - Replace: the SPLIT-8 tag (change 3) and the plan-as-realized stretch both go.
  - Add alongside: the tag stays.
  - Either way the data is unchanged.
- **Decision:** keep, add alongside, or replace.

**2. P5, PROV-5 (Must) and PROV-6: duplicate bookkeeping.**
- **mmu_2022:** its `No` / `Duplicate` verdict is still `AI (UNVERIFIED)`. A curator should confirm it (same description, metric and file sizes).
- **The 2020 cut ("Tanzania Tourism Prediction", 6,476 rows):** a `No` / `Duplicate` record would stop a later screening from adding it under a misreading of PROV-7.
  - Critic: required; the false premise has already spread once.
  - Advocate: optional, since nothing ships twice.
  - No Must requires the record, so it is your call: it would be a new screening verdict.
- **Effect today:** none on shipping. Uniqueness holds.

**3. P6, MET-2 (harness-wide): scorer column order.**
- `metrics.py` (lines 21-23) scores probability columns in the container's category order. Since the reorder, alphabetical columns (sklearn's `classes_` order) score 2.537 instead of 1.592 for the same prior.
- This hits all five ordered multiclass targets, not only this one. The definition needs nothing.
- Results scored on the old container were consistent with that container. The risk is mixing them with results on the new one.
- **Decision:** add a README line, or a label check in the scorer, repo-wide; and confirm that no cached result from container `01a18ad4…` is reused.

**4. Process: `checked_by`.**
- It lists only Myunghwan. All ten other records you shipped on 2026-11-04 list you too.
- Options from the precedent checker: (a) add `Lennart`; (b) leave it on purpose because the review was light, and say so; (c) remove `Lennart` from the siblings; (d) change how `checked_by` is filled after a review-page verdict.

**Agreed facts (with this pass's checks)**

- **Bytes:** `Train.csv` matches the pinned commit (3,147,987 bytes, sha256 `1a7108…899f`). 18,506 + 6,169 = 24,675 rows. Licence CC BY-SA 4.0, non-commercial.
- **Metric:** Zindi's metric is Log Loss on six classes. The prior scores 1.5919–1.5922 on all nine folds, and each test fold has at least 119 rows of Highest Cost.
- **Label basis, checked by this pass.**
  - I reran the claim auditor's linking script: 2,401 rows link uniquely, and the round cuts on the party total agree 97.9% (per person 58.9%).
  - Fair test with the best possible ordered cuts for each basis: party total 98.9%, per person 66.5%, per person-night 51.1%.
  - So the label is the party's total trip spending.
  - Spearman correlation with the cost: 0.965 for the declared order, 0.945 with Lower and Low swapped. The class order is measured.
- **The 2020 cut is an earlier subset.**
  - By the panel's 16-column key, 72.3% of its training rows match ours, against 23.4% by chance; about 75% is expected if all its rows are inside ours.
  - My rerun with the 17-column key gives 70%.
- **No leak, no exploit.**
  - Leak probe: all features 0.843, any single feature at most 0.716.
  - Task gamer: no gain above the noise of a random column (0.0049).
  - Train-against-test classifier: AUC 0.49–0.50.
  - Row order carries nothing: neighbouring labels agree 0.2211 against 0.2228 by chance.
- **Cleaning counts all reproduce:** Widlife 5,988; UAE 187; BURGARIA 2; 94 zero-party rows; 142 / 104 / 62 / 344 inconsistent codings; 9.8509% copies; 965 / 468 / 410 / 1,324.
- **Model scores:** RF 1.107, LightGBM 1.114, linear 1.126. Ranked probability score ranks the models the same way as log loss, so MET-4's bar to overrule the source's metric is not met.

**Task gamer's attacks mapped to rules.** None of the attacks below gained anything, so none is an issue.
- Copy lookup: LEAK-19 and the accepted warnings. Known; the gain (none) matches the notes.
- Counts over train and test together: LEAK-30. New, no gain; no note needed.
- Row position: SPLIT-22. No gain.
- Missing-value indicators (1.580 against 1.592): LEAK-10 missingness clause. A deployed model sees the same blanks, so it is signal.
- Engineered party size and total nights (−0.0038): signal.
- Looking up labels in the public 2020 file: a source lookup, not a flaw of the task.

The definition has no `Potential leak, kept on purpose:` notes.

**Consistency with precedent**

- **Ordered target:** consistent with CLEAN-25 (cardiotocography, hepatitis_c, chicago_traffic_crashes). This is the first order taken from wording; it is now backed by measurement.
- **`age_group`:** consistent with CLEAN-14 (open_university's `age_band`).
- **SPLIT-8 tag:** follows bank_customer_churn and account_debt_south_africa. The fact that sets this case apart is that no window can be measured.
- **Copies:** follow LEAK-19's distinct-entity clause (hiva_agnostic, qsar_tid_11). They do not count toward a third exception.
- **Year 2022:** departs from melbourne_housing_market because there are two separate competitions, and the earlier one lacks the target and 74% of the rows.
- **Plan-as-realized:** in_vehicle_coupon_recommendation matches only in part, and issue 1 can remove the stretch.
- **`checked_by`:** out of line with its ten siblings (issue 4).
- **Register:** no flag for this dataset.

</details>

<details><summary>Claim audit</summary>

Dataset: `ai4d_lab_tanzania_tourism_classification_challenge`. Claim audit, second pass, 2026-11-04.

**The focus question.** `focus.md` asked the claim auditor to open the metric reference. I opened it (zindi.world, the redirect target). It says "The evaluation metric for this challenge is the Log Loss." The submission header lists six class columns in alphabetical order: "High Cost, Higher Cost, Highest Cost, Low Cost, Lower Cost, Normal Cost". So the declared `Metric.source("log_loss")` is the source's metric, on the source's six classes, with no params and no scoring columns. MET-4, MET-11 and MET-12 hold.

MET-2 holds too. A dummy prediction (the training prior) through `data_foundry.v2.metrics.scorer` scores 1.5919 to 1.5922 on all nine folds. Every test fold has all six classes; the smallest is Highest Cost with 119 or 120 rows.

The same page gives the licence: "access, use and share competition data for any non-commercial, research or education purposes", CC BY-SA 4.0. Claim 22 holds.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 4, 9, 12 | "The release does not document monetary boundaries or the expenditure basis"; currency, per-person vs party and thresholds unspecified, so `fit="approximate"` | task_summary, curation_comments | Linked the 2020 Zindi cut of the same NBS survey (`Train.csv` with `total_cost`; its codebook says "The total tourist expenditure in TZS") to our rows on a 17-column key | **Refuted** (as a statement about what can be known) | 2,401 rows link uniquely. Cutting the party's total trip cost at 0.5M / 1M / 5M / 10M / 50M TZS reproduces the 2022 class for 97.9% of them; the same cuts per person give 58.9%. Medians by class: 250k, 829k, 2.55M, 7.29M, 18.2M, 58.0M TZS | USE-5 (Must), EV-2 |
| 16, 43 | Class order Lower < Low < Normal < High < Higher < Highest | notes, CC Lennart 2026-11-04 | (a) Spearman correlation with linked `total_cost`; (b) ordering classes by how often a model confuses them | **Holds** (now measured, not only read from the names) | (a) 0.965 for the declared order, 0.945 with Low and Lower swapped. (b) Out-of-fold LightGBM confusions put the declared order first (10.85); the swap is worse (11.13). Nights and package counts rise in the same order | CLEAN-25, CLEAN-14 |
| 20 (part) | "The 2020 regression competition is a different published task/cut" | notes | Share of 2020 training rows whose 16-column key is in our `Train.csv`, against a random-half baseline | **Refuted on "different task"** | 72.3% of the 4,809 rows match, against 23.4% by coincidence. About 75% is expected if all 6,476 rows of the 2020 release are inside the 24,675, which are 75% train. So the 2020 file is an earlier subset with the raw target. A swapped target plus added rows is "not a distinct task" | PROV-6, PROV-9 |
| 23 | year 2022, source Zindi 2022 | `dataset.py` | As above | **Contested** (weighing call) | About 26% of our rows (around 4.8k of 18.5k) were first published in December 2020. The binned target and three quarters of the rows first appeared in 2022 | PROV-8, PROV-9 |
| 20, 34 | `mmu_2022` is a duplicate, left alone | notes, record | Its record status; any folder | Holds | `mmu_2022.md` is `No` / `Duplicate`, and no folder exists. The checklist's "not also shipped?" concern is closed | PROV-4 |
| 21 | The pinned public commit recreates `Train.csv` (3,147,987 bytes, sha256 1a7108…899f) | download_description | Downloaded the URL and hashed it; hashed the warehouse file | Holds | Both copies give 3,147,987 bytes and the same sha256. The Zindi archive's CRC is not re-verified (untested: curator-supplied) | PROV-1 |
| 10, 32 | 18,506 labelled rows; 6,169 in the test file; 24,675 in total | notes, record | Count | Holds | 18,506 + 6,169 = 24,675 | |
| 13 | `Tour_ID` is 18,506 unique opaque IDs | notes | Count and length | Holds | 18,506 unique, all 15 characters | LEAK-13 |
| 14, 15 | Widlife 5,988 → Wildlife 2,283; UAE 187; BURGARIA 2 | notes | Count in the raw file | Holds | Exact match; UNITED ARAB EMIRATES 36 and BULGARIA 6 exist already | CLEAN-10 |
| 17 | 94 records with a zero party total | notes | Count | Holds | 94 | |
| 18 | 142 Independent with a Yes inclusion / 104 Package Tour all No / 62 Alone with sum > 1 / 344 non-Alone with sum = 1 | notes | Count | Holds | 142 / 104 / 62 / 344 | writing |
| 19, 28 | 9.8509% of test rows match a training profile; 965 exact row extras | notes, accepted warning | Recomputed over all nine folds from the definition | Holds | 9.8509% pooled (9.39 to 10.33% per fold); 965 extras | LEAK-16, LEAK-18 |
| 29, 30 | 468 extra feature/label combinations; 410 profiles with several labels (1,324 rows); same coarse plan, different spending | accepted warning, Decision | Recount, plus `total_cost` on the linked rows | Holds, and stronger | 468 / 410 / 1,324. The linked costs show that profiles with differing labels have different real spending, so the label ambiguity is genuine (the LEAK-20 exception applies) | LEAK-20 |
| 2, 5, 11, 25 | Realized plan-like attributes stand in for plan inputs | task_summary, CC 2026-10-23 | Dropped each feature group in turn (LightGBM, repeat 0) | Holds as an approximation; no single dominant input | Log loss with all features 1.119. Without nights 1.166, without party 1.178, without packages and arrangement 1.194, without activity 1.127, visitor context only 1.320. The 2020 file's post-trip `most_impressing` is not in our data | USE-3, USE-6, LEAK-10 |
| 6, 24, 26, 27 | Stratified random 3×3 folds; no time column | splits_comment | Fold sizes; prep's hidden-group probe | Holds | 12,337 to 12,338 train / 6,168 to 6,169 test. The `country` gap of +0.084 is a feature new rows keep, not an entity | SPLIT-4, SPLIT-29 |
| 36, Metric | Log loss over six classes from the Zindi Evaluation page | record, `dataset.py` | Opened the page; dummy prediction scored per fold | Holds | See the focus answer above | MET-2, MET-4 |
| Implied (MET-2) | Probabilities are scored in a known column order | scorer | Fed alphabetically ordered probabilities to the scorer without `labels` | **Risk** (harness, not this definition) | The scorer reads columns in category order (Lower … Highest). Alphabetical columns, which is Zindi's header order and sklearn's `classes_` on strings, score 2.537 instead of 1.592 for the same prior. `examples/benchmark_on_beyond_arena.py` reindexes, so a careful harness is fine. The order changed from alphabetical on 2026-11-04, so cached runs on the old order are not comparable | MET-2 |
| 41 | Nine-fold LightGBM / logistic log loss 1.0816 / 1.1259 | record 2026-10-26 | No probability files kept | Untested | My untuned LightGBM gives 1.119; the prep's RF gives 1.107. Same order of magnitude | EV-1 |
| 41 vs 44 | "Independent claim and blind reviews retained in the review evidence" vs "no panel ran" | record | Looked for the evidence | Untested; the record contradicts itself | No REVIEW.md and no panel files from 2026-10-26 | writing |
| 42 | The 2026-10-29 build reproduces the earlier one | record | Load the built container | Untested and superseded | The README marks the build stale (target now ordered), and the container is absent locally. Shipping needs a new build | |
| 1, 3, 7, 8, 31–33, 35, 37–40, 45 | Wording, screening facts, CC history | record | Read | Hold or not material | Record risk 37 "bins from total_cost … whether the regression framing is the better task" was never answered; it is answered now (row 1 of this table) | |

**Refuted and untested, ranked (validity first, Must first)**

1. **P3, USE-5 (Must).** The target is documented after all, through the source's own earlier cut. It is the party's total trip expenditure in TZS, cut at about 0.5M / 1M / 5M / 10M / 50M (97.9% agreement on 2,401 linked rows).
   - **What it changes:**
     - The fit gap in `fit_reason` and claims 4 and 12 is mostly closed: currency, basis and thresholds can now be stated.
     - Claim 16's order is confirmed by measurement, not only by reading the names.
     - The "approximate" fit stays justified by the plan-as-realized inputs and the unknown survey year.
   - **Mildest remedy:** a notes edit in `predicted`, `fit_reason` and `curation_comments` that states the reconstructed bins, their basis and the evidence, and calls them approximate (they come from a third-party copy of the 2020 files). No change to data, target, metric or split.
   - **Curator weighing call (USE-5 resolution, MET-4):** keep the six classes. They have 3.8× the rows of the 2020 regression cut (4,809 rows, MAE), and log loss is the competition's metric. The finer regression target exists only for the subset.
2. **P5, PROV-6, PROV-8, PROV-9 (Must).** The 2020 Pycon / Zindi "Tanzania Tourism Prediction" (6,476 rows, `total_cost`) is an earlier subset of this release, not a "different task". It has no record and nothing ships twice, so uniqueness holds.
   - **What it changes:** claim 20's sentence, and possibly `year`.
   - **Mildest remedy:**
     - Rewrite the note: "an earlier 2020 subset of the same survey with the raw TZS cost; a duplicate version under PROV-6, not shipped".
     - Keep year 2022 with a one-line reason: the binned target and about 74% of the rows first appeared in 2022.
     - Or take 2020 by the melbourne_housing_market grew-over-versions precedent. That is the curator's call.
3. **P6, MET-2 (implied, harness-wide, not this definition).** The scorer assumes probability columns in category order. Since the 2026-11-04 reorder, alphabetical columns score 2.537 instead of 1.592.
   - **Remedy:** none in the definition. Anyone benchmarking must pass `labels=` or reindex, as the example does. Any result cached on the old category order should be rescored.
4. **Untested:**
   - The official archive CRC: curator-supplied, can't be reproduced without authentication.
   - The 2026-10-26 model scores (claim 41): no probability files.
   - The 2026-10-26 "independent reviews retained" (claim 41): no artefact; it contradicts claim 44.
   - The build (claim 42): stale and absent locally.

   None of these blocks shipping. The build is the curator's separate ask.

Nothing else refuted. Copies across the split, cleaning counts, licence, metric and splits all hold as written.

Sources:
- [Zindi AI4D Tanzania Tourism Classification Challenge](https://zindi.world/competitions/ai4d-lab-tanzania-tourism-classification-challenge)
- [Zindi Tanzania Tourism Prediction (2020) data page](https://zindi.world/competitions/tanzania-tourism-prediction/data)
- [fredygerman/Tanzania_Tourism_Prediction](https://github.com/fredygerman/Tanzania_Tourism_Prediction)

</details>

<details><summary>Column audit</summary>

**Column audit: `ai4d_lab_tanzania_tourism_classification_challenge` (second pass, 2026-11-04)**

**Answer to focus.md.** `focus.md` sets no special question, only the standard panel. My answer to the standard question: none of the 19 feature columns or the target has to leave, and I found no leak. The prediction point is a specified trip plan that is assumed to happen as specified (Myunghwan's CC of 2026-10-23, confirmed on 2026-11-04). Under it, every column is either a visitor attribute or a plan attribute. Nothing measures spending, consumption or how the trip was rated afterwards. The leak probe gives 0.843 with all features and at most 0.716 for any single one, and dropping any one column costs at most 0.017. That is a spread signal, not a give-away. The dtype probe flags only `age_group` (`open_end`), and it is already ordinal in the right order.

Codebook: `VariableDefinitions.csv` from the immutable mirror commit `3c3a6f15`.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| country | "country a tourist coming from" | yes, visitor attribute | category, 129 levels, 0 NA. UAE (187 rows) merged into UNITED ARAB EMIRATES and BURGARIA (2) into BULGARIA, 189 rows changed as declared. Other misspellings (SWIZERLAND, MORROCO, MALT, ECUADO, ...) have no correctly spelled twin, so they are harmless labels. SCOTLAND/UNITED KINGDOM and TANZANIA (4 rows) are kept as published | fine | CLEAN-14, CLEAN-17 |
| age_group | age band | yes | ordinal `<18 < 18-24 < 25-44 < 45-64 < 65+`, which matches the band meaning. No unknown code, 0 NA | fine (probe flag answered) | CLEAN-14, CLEAN-25 |
| travel_with | "relation of people a tourist travels with" | yes, plan | category, 5 levels, 1,075 NA (5.8%). See problem 1 | question for the curator (note only) | CLEAN-10, LEAK-10 (missingness) |
| total_female | "Total number of females" | yes, plan | float64 count. 94 zero-total rows set to NA (raw NA 2, now 96). Max 49 | fine | CLEAN-11, CLEAN-14 |
| total_male | "Total number of males" | yes, plan | float64 count, same zero-total fix (raw NA 6, now 100). Max 58 | fine | CLEAN-11 |
| purpose | purpose of the visit | yes | category, 8 levels | fine | — |
| main_activity | "main activity of tourism" | realized, used as the plan's stand-in (accepted) | category, 9 levels. 5,988 rows of "Widlife Tourism" merged into "Wildlife Tourism" | fine | LEAK-10 (scenario), CLEAN-1 |
| info_source | source of information about Tanzania | yes, comes before the trip | category, 8 levels | fine | — |
| tour_arrangement | Independent / Package Tour | yes, booking | category, 2 levels | fine | — |
| package_transport_int … package_insurance (7) | "if the tour package includes X" | yes, booking | category Yes/No, 0 NA, each holds only Yes and No. 142 Independent rows have a Yes; this is noted and kept | fine | CLEAN-14 |
| night_mainland | "nights a tourist spent" on the mainland | realized, used as the plan's stand-in (accepted) | int64, 0 to 365. See problem 2 | fine / question | CLEAN-11, USE-7 |
| night_zanzibar | nights spent in Zanzibar | same | int64, 0 to 240 | fine | CLEAN-11 |
| first_trip_tz | "if it was a first trip to Tanzania" | yes | category Yes/No | fine | CLEAN-14 |
| cost_category (target) | "range of expenditures" | target | ordinal, Lower < Low < Normal < High < Higher < Highest. See problem 3 | fine | CLEAN-25 |
| Tour_ID (dropped) | "unique identifier for each tourist" | n/a | dropped, 18,506 unique opaque values | fine | CLEAN-3 |

**Problems, ranked (P order; none blocks shipping)**

1. **`travel_with` missing values probably mean "Alone". This is a question for the curator; it is not a leak.**
   - Of the 1,075 NA rows, 1,045 (97.2%) have a party total of 1. For "Alone" the share is 7,488 of 7,590.
   - With party = 1, the label mix differs: NA rows have 31.5% Lower Cost, Alone rows 21.5%. The NA rows are spread over the whole raw file (position quartiles 4,559 / 9,418 / 14,054), so they are no block from one survey wave.
   - The missing indicator alone scores 0.521, which is negligible. Nothing suggests the missingness is caused by the outcome (LEAK-10, missingness clause).
   - Mildest remedy: keep the NA, because recoding it to "Alone" would be a guess (LEAK-8). Add one line to `curation_comments` saying the NA rows are almost all one-person parties.

2. **Very long stays.** 54 rows have more than 90 nights in total, 16 more than 180, and row 239 has 365 + 6 = 371. These are mostly Business or Volunteering trips with Independent arrangement.
   - CLEAN-11 says unusual values stay, and none of these is impossible.
   - USE-7 question: a stay of a year or more falls outside the international definition of a visitor (less than 12 months), which matters for the "tourist plan" use case. This affects 1 row (371 nights). 2 more rows sit at 364 and 1 at exactly 365.
   - Mildest remedy: keep all rows and mention them in a note. Removing the single row above 365 nights is optional and would need a curator CC.

3. **Target order is an interpretation, but the data supports it (CLEAN-25, claim 16).** Share of package tours by class, Lower → Highest: 0.083 / 0.086 / 0.270 / 0.746 / 0.900 / 0.969. Share with international transport in the package: 0.041 / 0.049 / 0.143 / 0.508 / 0.646 / 0.805. Both rise in step with the order. Lower sits below Low on the share of regional-Africa visitors (0.675 against 0.432) and on mean nights (7.2 against 9.6). Log loss does not use the order. Remedy: none. The evidence could be added to the README's note on the reading.

4. **Realized exit-survey values stand in for plan inputs** (nights, `main_activity`, party, packages; claims 2 and 11). LEAK-10 accepts this under the scenario named in the CC. I found no column that cannot be supplied as a plan. Remedy: none beyond the existing `fit="approximate"` and the note.

5. **Zero-party fix checked.** "Alone" has a party total of 1 in 98.7% of rows (7,488 of 7,590), so the counts include the respondent and a total of 0 is impossible. The 94 rows set to NA lean slightly towards Higher Cost (36 of 94 against 26% overall). That comes from the source's own coding, not from the outcome, and the missing indicator scores 0.500 and 0.501. Fine under CLEAN-11.

6. **Inconsistent source coding (USE-7, LEAK-8).** 142 Independent rows have a package Yes, 104 Package Tour rows have all seven inclusions No, and 62 Alone rows have a party total above 1. All are declared and kept, which is correct because the questionnaire's routing is unverified.

**Checked and clean:**
- No proxy-missing codes (CLEAN-10).
- No row has zero nights in total.
- No feature is a copy or a constant (CLEAN-5).
- No object column (CLEAN-9).
- No feature encodes the label or comes after it.
- The dropped id does not reach the features.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The stratified random 3x3 IID split fits the use case. The release has no time or entity axis to recover. A split grouped on exact profiles costs +0.005 log loss, which changes nothing. Two notes need wording only: one is a tag, the other is how the 9.85% figure is described. Neither needs a re-split.

**Direct answer to focus.md.** The focus file asks no question of its own ("none beyond the standard panel"). For the standard question: yes, the split is honest for this use case. The two copy-related pointers it lists (hidden-group country gap, 9.9% exact copies) do not call for a grouped split. The numbers are below.

**Regime against the use case**
- **Use case.** The source says the model helps "tourists across the world estimate their expenditure before visiting Tanzania". One prediction is one specified visitor and trip plan. A new visitor brings their country, age band and plan, so it is a cold start for the person. But no entity id would be shared with training, so there is nothing to group on.
- **Declared regime.** IID, record `required_split: Random (IID)`, no `grouping` or `temporal`, stratified 3 folds x 3 repeats. I checked the folds: 12,337/6,169, 12,337/6,169 and 12,338/6,168 rows, with no overlap between train and test.
- **Temporal (SPLIT-7, SPLIT-22).**
  - There is no date column and the survey year is undocumented.
  - The raw file order is not hidden time. Labels of neighbouring rows agree 0.2211 of the time, against 0.2228 by chance. Neighbouring rows share features at 0.422, against 0.421 for shuffled rows.
  - Class shares are flat across ten blocks of the file (for example, Normal Cost runs from 0.282 to 0.310).
  - The `Tour_ID` suffix is 8 random characters on all 18,506 rows.
  - So no window, gap or label-delay question can be checked, and no row's label comes from after its prediction point (one cross-section, label recorded at exit).
- **Grouped.** There is no true group id. Respondent and party linkage is not in the release. Grouping on a similarity cluster or a feature hash would break SPLIT-24.

**Hidden groups and near copies (SPLIT-29, SPLIT-30, SPLIT-4)**
- **Country probe.** 129 values, gap +0.084 (random 0.686, grouped 0.602). Country is known for every new visitor, so it is a feature and not an entity to hold out (SPLIT-4). This is not a hit.
- **Composite keys and near copies.** Leaving out one column, the gap is +0.006 or +0.005. Near copies at similarity 0.85 give a gap of -0.000. Nothing points to a hidden entity.
- **Are the exact copies one person or one party?** My numbers say no. 766 profiles occur more than once, covering 2,199 rows.
  - 361 of those profiles (965 rows) have `travel_with = Alone`, so the copies must be different people. 213 of the 361 carry more than one label.
  - 67.8% of repeated profiles occur more often than the party size (`total_female + total_male`). They cannot all be members of one party.
  - These are common coarse profiles in the survey population, which new data will also contain. Keeping them in test matches what the model will meet in use.
- **Alternative split: LightGBM, 300 trees, the same settings in every run, three folds each.**

| split | log loss (mean of 3) |
|---|---|
| given random folds (first repeat) | 1.0934 |
| grouped by exact feature profile (StratifiedGroupKFold) | 1.0981 (+0.0047) |
| grouped by profile without `age_group` (a stand-in for a party key) | 1.0959 (+0.0025) |

- **Copy rows inside the given folds.** Test rows that have an exact copy in train (9.8% of test) score 0.915. Rows without a copy score 1.113. The difference reflects frequent profiles having well-estimated class shares, not memorisation: removing every cross-split copy moves the total by only 0.005. The task probe's family order is RF 1.107, LightGBM 1.114, linear 1.126, with a paired gap of 0.012 (SE 0.001) between RF and linear. A shift of 0.005 that applies to every family is unlikely to change that order.

**Problems, ranked**

1. **The forced-IID status is not declared (SPLIT-8, a Should-level note; P4 honesty).**
   - Evidence: the use case is forward-looking ("before visiting"), and the class boundaries are money categories that drift with prices and exchange rates. The release is one undated cross-section in shuffled order, and `data_tags` is empty.
   - SPLIT-8 covers "a release with no dates at all (one extract…)": such a task ships IID tagged `ForcedIIDFromTemporal`. The snapshot precedents (bank_customer_churn, account_debt_south_africa) carry the tag. `task_summary.split` already says "does not test future seasons", so the wording is half there.
   - Against it: Myunghwan's CC of 2026-10-23 removed the record's `Non-IID (Temporal)` tag. That was a different tag (a non-IID regime), and the forced-IID tag was never weighed. The curator could reasonably decide the task is a cross-sectional estimate, not temporal in nature.
   - Mildest remedy: put the question to the curator, with no re-split. Either add `data_tags = ("ForcedIIDFromTemporal",)` plus one sentence in `splits_comment` (a dated survey wave would test drift in class boundaries and the visitor mix; recover the wave or year if NBS publishes it), or have the curator state that the task is cross-sectional by design.
2. **The copy wording in `curation_comments` and `accepted_check_warnings` (notes; EV-3).**
   - Evidence: the text says the 9.8509% matching evaluations "do not establish repeated people". That is true, and my numbers above make it stronger (361 Alone profiles, 67.8% of copy groups larger than the party).
   - It omits that a split grouped on profiles costs only +0.005 log loss. That number is the direct answer to "is the score inflated?"
   - Mildest remedy: optionally add one line with the grouped-profile number to `splits_comment`. No change to the split itself.
3. **No problem found with the fold mechanics.**
   - Stratification holds the smallest class at 119 or more test rows per fold (Highest Cost, about 2%).
   - The folds are disjoint, and the three repeats are proper repeats.
   - The probe ran with no `--time-on`, which is correct since there is no time column.

**Rules applied**
SPLIT-1, SPLIT-2, SPLIT-4, SPLIT-7, SPLIT-8, SPLIT-22, SPLIT-24, SPLIT-29, SPLIT-30, SPLIT-31 and EV-3. The decisive rule is SPLIT-4: country is a feature, not an entity to hold out. SPLIT-31 adds that an optimistic IID split which matches how the task is framed stays as it is.

</details>

<details><summary>Domain practitioner</summary>

**Domain-practitioner report: `ai4d_lab_tanzania_tourism_classification_challenge`**

**Focus question.** `focus.md` sets no question beyond the standard panel. My direct answer to the standard question: the use case is real enough to carry the cleaning that was accepted, and `fit="approximate"` is right (USE-5, USE-8). The actor and decision named in `task_summary` (a tour operator or the Tourism Board estimating a planned trip's spending category) are the weakest part of the definition. They are not a reason to block shipping.

**Fit: approximate.** The survey labels are real and the inputs are things a visitor can state. But the target is a party-level spending band with no published currency, basis or thresholds. No tour operator prices a trip from such a band, so the data is a stand-in for the decision, not a mirror of it.

**Who I am and how the decision is made today**

There are two plausible actors, and the source names the first (Zindi: "tour operators and the Tanzania Tourism Board ... help tourists estimate their expenditure").

- **A tour operator or a tourist planning a trip.** Today an operator quotes a price from its own rate card: park fees, lodge tier, vehicle days, flights. That quote is exact, so the operator does not need a model for it. A tourist uses published per-night guides.
- **NBS, the Bank of Tanzania or the Ministry estimating tourism earnings from the International Visitors' Exit Survey.** They work in USD per person per night, split by package and non-package arrangement. Published figures: 2016 package $411 against non-package $136; 2024 package $416; 2025 overall $289. Their real model need is to estimate or impute spending for respondents with a missing or implausible expenditure answer, using the other answers on the same form.

**1. The inputs at the moment of prediction**

- **Inputs I do have.** As a tourist or operator I know country, age, first-trip status, party, purpose, activity, arrangement, package inclusions and planned nights. The realized exit values stand in for the plan (claims 2 and 11; Myunghwan's CC of 2026-10-23). For the survey actor, every input is on the same form at departure, so the timing is exact and no stand-in is needed (USE-3).
- **Input I would not have:** `info_source` (how I heard of Tanzania) is odd for an operator but harmless.
- **Inputs I always have that are missing:** these drive the cost more than any shipped column.
  - Travel month or season (high-season park and lodge rates).
  - Accommodation tier (budget camp vs luxury lodge).
  - Which parks or how many park days (Serengeti or Ngorongoro fees against a Zanzibar beach stay).
  - The year, for inflation and the exchange rate.

  The source does not ship these, so it is a gap to name, not a fix to make.

**2. Target: what I act on, or a proxy?**

It is a proxy, and a coarse one.

- **The label tracks party total, not per person.** Across the six ordered classes, mean party size goes 1.43, 1.41, 1.58, 2.00, 2.52, 4.43, while mean nights do not rise monotonically (7.2, 9.6, 13.0, 12.7, 12.3, 10.7). So the label behaves like the party's total trip spending, not per person per night, which is the unit every official report and practitioner uses. With undocumented band edges I cannot turn a predicted class into a budget, a quote or an earnings estimate. This is the USE-5 gap that `fit_reason` already names, correctly.
- **The data supports the ordinal reading (claim 16).** The share of African visitors falls 0.68 / 0.43 / 0.20 / 0.06 / 0.04 across Lower to Higher. Package-insurance inclusion rises 0.02 / 0.02 / 0.05 / 0.20 / 0.30 / 0.34. Reading Lower < Low is consistent with both. The step from Normal to High is driven by party size and package tours, as expected. The order is backed by the data, not only by the wording.
- **What I would want:** a probability over ordered bands (to plan with ranges) or, better, a number in USD.

**3. Row, decision and test**

- **Row and decision.** One row is one survey respondent's trip. That matches one trip decision for the planner, and exactly one imputation for the survey actor.
- **Test data.** Stratified random folds over the same survey release test "other respondents from the same survey population". That is exactly the imputation case. It is not a planner's next season: prices drift strongly (package $411 in 2016, $479 in 2025). The survey year is undocumented, so no temporal split is possible (SPLIT-3 cannot apply). For the planner use case this is a further approximate gap. The `split` field names it ("does not test future seasons"), which is adequate.
- **Copies.** The 9.9% exact copies across folds (accepted 2026-10-25) are realistic. Coarse profiles really do repeat in a survey population, and the same profile with different labels (410 profiles) is honest noise.

**4. Would I use it?**

- **As an operator:** no. My rate card beats 57.6% top-1 accuracy on six unlabelled bands.
- **As the survey statistician:** possibly, as an ordinal imputation model.
  - **Measured fit** (my rerun, 9 folds, HistGradientBoosting): log loss 1.090 against the prior's 1.592, accuracy 0.576, within one class 0.858.
  - **Errors fall on adjacent classes**, which builds trust.
  - **The Low Cost band is barely predicted:** 21 of 522 correct in fold (0, 0), and Lower is confused with Normal (228 rows). This suggests Low is a narrow band, so I would distrust that class.
- **What would make me trust it:** the band edges and the currency, the survey year, and confirmation that the label is party total.

**5. Metric: partly**

- **Why I keep it.** `log_loss` is the Zindi leaderboard metric, so MET-4 applies. It is strictly proper and scores probabilities, which is what an ordered-band user wants (MET-8). There is no threshold or cost matrix, so a hard-label metric would be wrong (MET-6, MET-7).
- **Why only partly.** Log loss ignores the order the definition now declares (claim 16). It charges a Lower-vs-Highest miss the same as a Lower-vs-Low miss, while the decision (a budget range) does care about distance (MET-1).
- **What I would choose.** On a fresh task I would use the ranked probability score: proper, ordinal and per row.
- **Why I would not overrule.** My run on the shipped 9 folds ranks the models identically under both metrics:

  | model | log loss | RPS |
  |---|---|---|
  | HistGradientBoosting | 1.090 | 0.0817 |
  | logistic regression | 1.126 | 0.0849 |
  | class prior | 1.592 | 0.1528 |

  This is no evidence of bias, so MET-4's bar to overrule is not met. Keep `log_loss`.

**Gaps, ranked by how much they change the task**

1. **Actor mismatch (USE-1, USE-9).** The named actor (an operator or tourist planning a trip) has an exact rate card and no use for an unthresholded band. The survey's own users (NBS/BoT earnings estimation, imputing missing expenditure answers) fit the data, timing and random split directly. Rephrasing the use case to theirs would remove the "realized values as plan" stretch (claims 2, 11) without excusing any other gap. The fit stays approximate either way because of the label (gap 2), so the weighed factor against rephrasing only to excuse a gap does not bite.
2. **Label basis and bands undocumented (USE-5, USE-8).** The data indicates party-total spending, not the per-person-per-night unit practitioners use. Neither the monetary edges nor the currency is known. `fit_reason` already says this; adding "the class profile indicates party-level totals (mean party 1.4 → 4.4 across classes)" would make it concrete.
3. **Missing cost drivers.** Season, accommodation tier, parks and survey year are always known to a planner. They are absent from the source and cannot be fixed.
4. **No time axis.** Random folds suit imputation but not forecasting next season. This is named in `split`.
5. **Metric ignores order.** Small: same model ranking (above).

**What a domain expert would change**

None of these block shipping.

- Restate `use_case` as the survey statistician: "estimate the spending band of a respondent from the rest of the exit-survey form". Alternatively, add it next to the Zindi actor.
- Name the party-total evidence in `fit_reason` / notes.
- Ask the curator whether to keep `mmu_2022` unshipped (claims 20, 34) so the two copies do not double-count.

**Sources**

- Zindi description as quoted in the record.
- [NBS 2022 International Visitors Exit Survey Report](https://www.nbs.go.tz/nbs/takwimu/Tourism/2022_International_Visitors_Exit_Survey_Report.pdf)
- [BoT Tourism Sector Survey reports](https://www.bot.go.tz/Publications/Other/Tanzania%20Tourism%20Sector%20Survey%20Report/en/2020021122482692222.pdf)
- [BoT 2025 report](https://bot.go.tz/Publications/Other/Tanzania%20Tourism%20Sector%20Survey%20Report/en/2025022708182472.pdf)
- [The Citizen: US tourists spend more than Chinese](https://www.thecitizen.co.tz/tanzania/magazines/us-tourists-spend-more-than-chinese-2671458)
- [Guardian: Chinese visitors top in tourism expenses](https://ippmedia.co.tz/the-guardian/news/local-news/read/chinese-visitors-top-in-tourism-expenses-2026-07-03-105402)

The rules cited are from `use_case.md` and `metrics.md`.

</details>

<details><summary>Blind review</summary>

**Verdict:** include. This is a real Tanzania NBS tourist-expenditure survey with a clear six-class target. It has moderate signal and no leaking columns. Only small preparation notes apply.

**What the task is**
- Source: the Zindi "AI4D Lab Tanzania Tourism Classification Challenge" (June–July 2022). The page describes "24,675 rows of up-to-date information on tourist expenditure collected by the National Bureau of Statistics (NBS) in Tanzania", surveyed at three international airports and four border points.
- The Zindi test set (6,169 rows) has no public labels. 24,675 − 6,169 = 18,506, which is exactly our row count, so `data.parquet` is the full labelled Train.csv.
- The use: a tourism statistics office or tourism board estimates a visitor's spending band from the visitor's profile. This is used to impute spending for survey non-responders, to segment markets and to target promotion. It is a real use, though the "prediction" happens at departure (an exit survey), not before the trip.

**Concerns, most serious first**

1. **The target is ordinal, but it is benchmarked as plain multiclass.**
   - The categories are stored in order: Lower, Low, Normal, High, Higher, Highest.
   - That order fits the data. The package-tour share rises from 0.08 to 0.97 across the classes, and mean party size rises from 1.44 to 4.42.
   - The class bins are almost certainly cuts of `total_cost` in TZS, the regression target of the earlier Zindi "Tanzania Tourism Prediction" challenge. Zindi does not publish the cut-points.
   - With accuracy or log-loss, a model that confuses Higher with Highest is penalised as much as one that confuses Lower with Highest.
   - Change: none needed to include it. Optionally record the class order in the metadata. This is acceptable for a multiclass benchmark; Zindi itself scored it with log-loss.

2. **Duplicates and identical inputs with different labels.**
   - 965 rows (5.2%) are exact duplicates including the target.
   - 1,433 rows repeat the same feature values, and 410 of those feature patterns carry more than one label.
   - With few, coarse survey fields (age band, yes/no package items, small counts), real respondents will often answer identically. This is not a copy-paste artifact, and there is no ID to prove otherwise.
   - Effect: under a random split some test rows have an exact twin in train. That modestly inflates scores for memorising models, but it reflects real use.
   - Change: keep the rows; just note it.

3. **Possible time drift that I could not check.**
   - The survey covers an unknown period (one or more years), and there is no date column.
   - A random IID split is the only option, which is reasonable for an imputation-style use. A forward-in-time deployment cannot be checked.

4. **Small preparation points.**
   - `travel_with` has 1,075 missing values (5.8%). They are left as NaN, which is fine.
   - `total_female` and `total_male` are floats with about 100 NaN each and extreme values (max 49 and 58; 27 rows have a party of more than 20). These are plausible group tours, so keep them.
   - `night_mainland` reaches 365 and `night_zanzibar` reaches 240. These are long stays and plausible (volunteers, business).
   - `country` has 129 levels, and 36 of them have fewer than 5 rows. This is a fine test of high-cardinality handling.
   - Only 2 rows are from Tanzania. That is consistent with a foreign-visitor survey.
   - The seven `package_*` items and `tour_arrangement` are binary text categories ("Yes"/"No"), which is acceptable.
   - `tour_arrangement` and `package_accomodation` mostly agree but not fully: 437 package tours have no accommodation and 107 independent travellers have it. That is real survey noise, not an error.
   - No ID column is present, which is correct.

5. **Leakage.** I found none.
   - Every feature (demographics, purpose, activity, package contents, nights) is known at or before the exit interview.
   - Nights stayed and package contents are strong legitimate drivers of cost, not proxies for the target.
   - `total_cost` itself has correctly been left out.

**Signal and size**
- 18,506 rows and 19 features, with classes from 359 (Highest, 1.9%) to 5,471 (29.6%). That is enough for stratified 3-fold CV, though the Highest class has about 120 rows per test fold, which makes its per-class scores noisy.
- A default LightGBM run (300 trees, 3-fold stratified) reached accuracy 0.576 against a 0.296 majority baseline, and log-loss 1.116 against a 1.592 prior baseline. The signal is clear, the task is far from solved, and it is not trivial. This leaves useful room to separate methods.

**What I could not check**
- The VariableDefinitions.csv contents and the cost cut-points per class. The Zindi page does not show them, and I did not download the archive.
- The survey year(s), so I could not test for drift.
- Whether this train set overlaps with the 2018 "Tanzania Tourism Prediction" data, or whether the rows are respondent-level or deduplicated upstream.
- The licence: the Zindi page states none. Check Zindi's terms for redistribution before publishing.
- The test labels, which are not public, so we use only the labelled 18,506 rows.

**Sources**
- [Zindi data page](https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge/data), which redirects to zindi.world
- [Zindi competition page](https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge)
- [Python Tanzania announcement](https://mail.python.org/archives/list/tanzania@python.org/thread/FC7P4QST5IZBW6W7QWNFCCYXAONGLTCQ)
- [Earlier regression challenge](https://zindi.africa/competitions/tanzania-tourism-prediction)

</details>

<details><summary>Task gamer</summary>

**Verdict:** I could not game this task. Nothing I tried beat the honest model by more than the noise of a random column. Engineered party-size and total-nights features help a little (0.0038), but a deployed model would have them too, so that is signal.

**Baselines** (log loss, lower is better; 9 splits, 3 repeats × 3 folds):
- **Untuned LightGBM:** 1.1064 mean (1.0935–1.1315). With a random column added: 1.1167.
- **Regularised LightGBM** (600 trees, learning rate 0.02, 15 leaves, row and column subsampling, L2 penalty 5): 1.0755 mean (1.0641–1.1008). This is the honest reference the attacks are measured against.
- **Noise:** adding a column of random numbers to the regularised model gives 1.0804, a +0.0049 change (+0.003 to +0.007 per split). Any gain smaller than about 0.005 is noise.

**Exploits ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| – | None found | – | 1.0755 | – | – | – | – |

The closest thing to a gain is signal, not an exploit:

| # | Feature | Script | Honest | With feature | Gain | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Party size (`total_female + total_male`), a flag for missing party counts, total nights | `work/attacks.py` | 1.0755 | 1.0717 | −0.0038 (−0.0015 to −0.0059) | Yes: these are trip-specification fields | None needed |

**Flaws that hurt an honest model**

None found. The split is IID with no time column and no groups, so no training rows sit after the prediction point. A classifier of train against test scores AUC 0.49–0.50. The class shares by row-position decile are flat.

**Attacks that found nothing (mean log loss over 9 splits unless noted)**

- **Row position as a feature (untuned model):** 1.1151 against 1.1064. Worse. Next-row label agreement is 0.2197, against 0.2228 expected by chance. No ordering leak.
- **Exact copies across the split:** 11.9% of rows share their full feature vector with another row, but only 40% of rows in those groups share one label. Adding the out-of-fold class counts of identical training rows gives 1.0765, which is worse. The copies are generic trip profiles, not the same trip duplicated.
- **Count of each identical row, from training rows only:** 1.0758 (no change).
- **Counts computed over train and test together** (identical rows, country, night counts): 1.0769 (no gain). Nothing has been transformed over all rows; the numeric columns are raw counts.
- **Formats:** every numeric value is a whole number, with no sentinels. Nights range 0–365 (mainland) and 0–240 (Zanzibar); party counts go up to 49 and 58.
- **Missing-value indicators alone** (logistic regression, first 3 splits): 1.580 against the class-prior baseline of 1.592.
  - Almost all of that comes from missing `travel_with`. Those rows are mostly solo travellers (1,045 of 1,072 with known party size have a party of 1), and twice as often from neighbouring countries (24% against 13%). This is how the survey form was coded. A deployed model sees the same blank, so it is signal.
  - Missing party counts alone add nothing (1.5921).
- **Train vs test classifier:** AUC 0.49–0.50. The test set's makeup gives nothing away.
- **Columns from after the prediction point:** none. Every column describes the trip as specified; no spending or outcome column is present.
- **Web search:** I found no write-up of a winning solution or any leak or "magic feature" thread for this competition. The rows probably also appear in Zindi's sibling regression competition ("Tanzania Tourism Prediction", with `total_cost`) and in a Kaggle copy. Looking rows up there would be a source-file lookup, which is not a flaw of this task; I did not try it.

**What I could not check**

- I did not compare the kit with the published source file. Whether the preparation dropped `Tour_ID` (it is absent here) or changed or filtered rows is unknown.
- I could not check how `cost_category` was binned from total cost. If the bins were per person or per night, party size and nights would be near-deterministic. They are not near-deterministic in this data: the best model is still at about 1.07.

Sources:
- [Zindi AI4D Lab Tanzania Tourism Classification Challenge](https://zindi.africa/competitions/ai4d-lab-tanzania-tourism-classification-challenge)
- [Zindi Tanzania Tourism Prediction (sibling regression competition)](https://zindi.africa/competitions/tanzania-tourism-prediction)
- [Baselight copy of the Kaggle data](https://baselight.app/u/kaggle/dataset/succulentadam_machine_learning_of_tanzania_tourists/table/train)

</details>

<details><summary>Precedent check</summary>

**Precedent check: `ai4d_lab_tanzania_tourism_classification_challenge`** (second pass, 2026-11-04)

**Focus question.** `focus.md` asks nothing beyond the standard panel. Short answers to its pointers:
- **Copies across the split (claims 19, 28, 29):** consistent, with a stated reason.
- **Class order (claim 16):** consistent with CLEAN-25 and with the precedents set the same week.
- **Realized exit-survey values used as plan inputs (claims 2, 11):** consistent, with a stated reason. The precedent it cites matches only in part.
- **mmu_2022 (claims 20, 34):** consistent with PROV-4. That record is `No` with the `Duplicate` marker and has no folder in the working copy.

No decision departs from a rule without a reason. One record field is out of line with how the other ten datasets shipped that day were recorded (item 1). The register (`register.json`, 3,136 decisions, 19 flags) raises no flag for this dataset.

---

**1. Record bookkeeping out of line with its siblings (no rule ID; the ship CC of 2026-11-04).**

Lennart wrote "ship" CCs for 11 records on 2026-11-04. This is the only one whose `checked_by` lacks Lennart (it lists only `Myunghwan`). The other ten list both curators: bemtpl97, chicago_traffic_crashes, cps88wages, eucalyptus, fremtpl2, medical_facility_operational_data, huesken_sirna_efficacy, open_soil_spectral_library, predictive_insights_youth_income_prediction_challenge, protein_model_quality_rf_pcp. `data_foundry_status: WIP (DF)` is the same as on four of those siblings, so that field is fine.

> **Consistency check (AI, 2026-11-04):** your ship call on ai4d_lab_tanzania_tourism_classification_challenge is recorded with `checked_by: [Myunghwan]`. The ten other records you shipped on 2026-11-04 (e.g. bemtpl97, chicago_traffic_crashes) list you as well. What sets this one apart?
> (a) nothing, it was missed when the CC was applied: add `Lennart` to `checked_by`; (b) leave it on purpose because the review was light (PR #33 static page only), and say so in the record; (c) remove `Lennart` from the siblings to match; (d) change how `checked_by` is filled after a review-page verdict.

**2. Ordered target `cost_category` (CLEAN-25, Lennart 2026-11-04): consistent.**

- **Precedents:** cardiotocography (normal < suspect < pathologic), dementia_prediction (CDR) and hepatitis_c_prediction (blood donor < ... < cirrhosis), all Lennart 2026-11-01; chicago_traffic_crashes (KABCO, Lennart 2026-11-04). All are scales ordered by meaning. Unordered targets are only nominal ones (forensic_glass, eryhemato), which this is not. No drift.
- **What differs:** this is the first ordered target whose order comes from the wording, not from a documented scale. The source lists the classes alphabetically and gives no bounds. The CLEAN-14 case of 2026-10-30/31 says low-confidence orders are "checked again without the label". The order was not built from the label, so CLEAN-25's "never by the class sizes" holds.
- **Sanity check I ran on the raw Train.csv:** it does not contradict Lower < Low.

  | | Lower | Low | Normal | High | Higher | Highest |
  |---|---|---|---|---|---|---|
  | Package Tour share | 8.3% | 8.6% | 27.0% | 74.6% | 90.0% | 96.9% |
  | Mean nights | 7.16 | 9.56 | 13.03 | | | |
  | Regional African visitors | 67.5% | 43.2% | 19.5% | | | |

  The order also suits a "binned ranges / bands of a quantity" column (CLEAN-14 open-end rule).
- **Metric:** log loss (MET-4, the competition's metric) ignores the order. This is the same treatment as the 2026-11-01 ordered targets.

**3. `age_group` as ordered bands (CLEAN-14, open-end rule of 2026-11-01): consistent.**

The closest precedent is open_university_learning_analytics_dataset, whose `age_band` (`0-35 < 35-55 < 55<=`) is ordered with an open-end comment. The rule says "the definition says what it holds". The notes list the five levels, including `<18` and `65+`, as the source labels them. Nothing is open.

**4. Keeping 965 exact same-label copies (LEAK-16 Must, LEAK-18/LEAK-19 Should; Myunghwan 2026-10-25, kept by Lennart's ship): departs from LEAK-19, with a stated reason.**

- **Copies dropped:** wine_quality (1,177), audiology_diagnosis (27 copies on different patient ids), hotel_booking_demand (26.80%, fine-grained booking dates).
- **Copies kept:** sepsis_survival (LEAK-18: few features, natural repeats); hiva_agnostic and qsar_tid_11 (Lennart 2026-10-21: "IF the copies dont make any sense from a task use case, we should drop them"; distinct entities kept).
- **Stated fact that sets this case apart:** the inputs are coarse survey answers. 17 of 19 columns are categorical with 2 to 10 levels, apart from country (131). The data supports this:
  - The largest copy group is 49 Italian couples, aged 25-44, on 7-night Zanzibar beach package tours. Their labels are 35 High, 10 Normal and 4 Higher, so these are standard packages, not file artefacts.
  - 370 of the 718 raw copy groups carry more than one label.
  - That label mix also meets LEAK-20's "genuine label ambiguity the task has", which is the reason given in claim 29.
- **Gap:** the decision cites LEAK-16/18 but is not written as an `**Exception to LEAK-19 ...**`. It has no row in the leak_checks.md Cases table either. principles.md asks for both when a Should yields.
- **Fact for the split auditor (it does not break a precedent):** copy rows are enriched for `With Spouse` (44.6% against 27.8% overall; 18.0% of spouse rows sit in copy groups against 10.9% of all rows). Two spouses each answering would be a repeated party (LEAK-17). The record discloses that linkage is unverified, and SPLIT-24 forbids grouping on a feature hash. The mixed labels inside groups argue against pure party copies.

**5. Realized values stand in for plan inputs (USE-3 Must; Myunghwan CCs 2026-10-23 and 2026-10-25): consistent, with a stated reason; the precedent matches only in part.**

- **Cited precedent:** in_vehicle_coupon_recommendation (Lennart 2026-09-30). Its inputs are hypothetical scenarios written into the survey, so they are plans by construction. Here they are realized trips (nights, package, party) read back as plans.
- **Other precedents:** I found no record that rejected this framing on like facts. kickstarter dropped `staff_pick`, which is a downstream decision, not a plan attribute.
- **Counterweight:** the use_case.md factor "A use case rephrased only to excuse a gap (−)". It is met by `fit = approximate` and a fit_reason that names the assumption (USE-8/USE-9). No Must is broken, because the reframing moves the prediction point rather than excusing a value that was unknown at that point.

**6. Duplicate record mmu_2022 (PROV-4 Must, PROV-5): consistent.**

- mmu_2022 is `No`, marker `Duplicate`, and names this record as canonical. The ground is the same precedent as indabax_eswatini_2022 (Lennart 2026-10-12: duplicate by Zindi file size). The 2020 regression cut is a distinct task, which PROV-6 allows (tension row "Uniqueness against a distinct task").
- **Stale text:** this record's screening still says "`mmu_2022` (`TBD -> Yes`)". Its `checked_by` is `AI (UNVERIFIED)` only, so no curator has confirmed the duplicate under PROV-5. It is not shipped, so nothing collides.

**7. Smaller cleaning calls: consistent.**

- Zero-sum party counts made missing (94 rows; CLEAN-11 "impossible values become missing, the row stays"; tension row churn_telco_south_asia).
- `Tour_ID` dropped (CLEAN-3).
- Typo and alias merges (`Widlife` into `Wildlife`, `UAE`, `BURGARIA`) are synonyms of existing levels.
- Metric `Metric.source("log_loss")`, the competition's metric (MET-4; zillow_prize `mae` kept on the same grounds).

**8. Contradictions inside the record (not precedent departures; worth one line on the review page):**

- **Panel history:** the 2026-10-26 AI assessment says independent claim and blind reviews, a debate, a mediator and a cold editor are "retained in the review evidence". The 2026-11-04 AI assessment says "no panel ran for this dataset". One of them is wrong. This pass also supersedes the latter.
- **Priority gap factor:** the screening (2026-10-22) has "gap 0 (multiclass ... not thin)", while 2026-10-26 has "gap + (multiclass is thin among 133 accepted definitions)". The priority stays 4 either way.

**Third-exception and drift checks:** none due. Lennart's CLEAN-25 calls (5 ordered multiclass targets, about 35 binary Yes/No) all follow the rule. There is no third LEAK-19 keep on the "coarse survey profiles" reason: hiva_agnostic and qsar_tid_11 were kept because the entities are distinct, which is a different reason. No register flag touches this dataset.

---


**Rules and precedents checked:** principles.md, cleaning_features.md (CLEAN-3, CLEAN-11, CLEAN-14, CLEAN-25), leak_checks.md (LEAK-16 to LEAK-20), use_case.md (USE-3, USE-8/9, USE-10), splits.md (SPLIT-24, SPLIT-25) and provenance.md (PROV-4 to PROV-6); the records of mmu_2022 and the ten sibling ship records; the decision register; the raw `Train.csv` (read only).

</details>

<details><summary>Advocate</summary>

Verdict: ship after notes-only changes. The data, target, metric and split stay as defined.

**1. Nothing leaks, and nobody could game the task (P4, LEAK-10 Must holds).**
- **Evidence:**
  - The column auditor found every one of the 19 features is a visitor or plan attribute. The leak probe gives 0.843 with all features and at most 0.716 for any single one. Dropping any one column costs at most 0.017.
  - The task gamer found no exploit larger than the noise of a random column (0.0049). Row position made the score worse (1.1151 against 1.1064). Counts of identical rows gave nothing (1.0758 to 1.0769). A train-against-test classifier scores AUC 0.49 to 0.50.
  - The blind reviewer found no leak, and noted that `total_cost` is correctly absent.
- **Why it outranks the objections:** a leak is the only kind of P4 failure a real task cannot carry (principles, step 3). None was found, so every objection below is about notes or weighing at lower stakes.

**2. The IID split is honest, and the repeated profiles are real survey noise (P4: SPLIT-4, SPLIT-31, LEAK-16/18/20).**
- **Evidence:**
  - Grouping the folds by exact feature profile costs only +0.0047 log loss (1.0934 to 1.0981). The country gap of +0.084 comes from a feature every new visitor brings, so it is no entity to hold out (SPLIT-4).
  - 361 of the repeated profiles are `Alone` travellers, so the copies must be different people, and 213 of those 361 carry more than one label. 67.8% of copy groups are larger than the party size.
  - The linked 2020 costs show that profiles with different labels had different real spending. That is genuine label ambiguity, so the LEAK-20 exception applies.
- **Real problems, with the mildest fix:**
  - (a) The keep departs from LEAK-19 (Should) but is not written as an `Exception to LEAK-19` or added to the Cases table. Fix: write the exception (fact: coarse survey answers, 17 of 19 columns with 2 to 10 levels; serves P3/P4).
  - (b) The `ForcedIIDFromTemporal` tag. SPLIT-8 is a Must, not the Should the split auditor called it. I concede it may apply, since the planner use case looks forward. But the regime SPLIT-8 prescribes for "a release with no dates at all" is IID. So compliance costs one tag and one sentence in `splits_comment`, with no re-split. If the curator frames the task as cross-sectional imputation instead, the tag drops out.
  - (c) Optionally add the +0.005 grouped-split number to `splits_comment` (EV-3).

**3. The target is a real, measured quantity, more firmly than the definition claims (P3, USE-5 Must holds; USE-1, USE-3).**
- **Evidence:**
  - 2,401 rows link uniquely to the 2020 cut, whose codebook gives `total_cost` as "The total tourist expenditure in TZS". Cutting the party's total trip cost at 0.5M / 1M / 5M / 10M / 50M TZS reproduces the label for 97.9% of them; the same cuts per person give 58.9%.
  - The class order is measured, not only read from the names. Spearman correlation with `total_cost` is 0.965 for the declared order and 0.945 with Low and Lower swapped. Model confusions also rank the declared order first (10.85 against 11.13).
- **What follows:** the USE-5 gap in `fit_reason` mostly closes. The objection that the label is "undocumented" now argues for the dataset, not against it.
- **Fix:** a notes edit in `predicted`, `fit_reason` and `curation_comments`. It states the reconstructed bands as approximate (they come from a third-party copy of the 2020 files) and states the party-total basis.
- **Answer to the domain practitioner's unit objection (per person per night):** a measured label that is the party's total spending is "the quantity" USE-5 asks about, now identified. National earnings estimates add up totals. The remaining distance to the planner's decision is what `fit="approximate"` already declares (USE-8).
- **The actor mismatch (USE-1, USE-9):** fix it by adding the survey statistician (imputing a respondent's spending band) next to Zindi's named actor. That actor matches the timing and the random split exactly, so the "rephrased only to excuse a gap" factor does not bite. The fit stays approximate either way.
- **Classes against the 2020 regression:** the six classes have 3.8 times the rows (18,506 against 4,809), and log loss is the competition's metric. USE-5 says whether a target ships as classes or as a number is decided by how the source models and scores it.

**4. The data is faithful and ships once (P5, PROV-1/4/6 hold; PROV-9 is a weighing call).**
- **Evidence:**
  - The pinned commit reproduces `Train.csv` byte for byte (3,147,987 bytes, sha256 1a7108…899f).
  - The licence (CC BY-SA 4.0, non-commercial use) was read on the source page.
  - 18,506 + 6,169 = 24,675 rows, as the source says.
  - `mmu_2022` is `No` / `Duplicate` and has no folder. The 2020 cut has no record. Nothing ships twice.
- **Concessions:**
  - The note "the 2020 regression competition is a different published task/cut" is wrong as measured: 72.3% of the 2020 rows match against 23.4% by chance, so the 2020 file is an earlier subset. Under PROV-6 it is a duplicate version that we do not ship, which still leaves uniqueness intact. Fix: rewrite that one sentence.
  - The year is the curator's call. 2022 is defensible: the target and about 74% of the rows first appeared in 2022. That makes the 2022 release a separate publication, not one Kaggle upload growing over its versions (the melbourne precedent). Either year leaves the data unchanged.

**5. Worth benchmarking, and scored by the competition's metric (P6, TP and MET-2/4/8 hold).**
- **Evidence:**
  - The prior scores 1.592 on log loss; models score 1.07 to 1.12, and accuracy is 0.576. The signal is clear and the task is far from solved.
  - The model families separate: RF beats linear by a paired 0.012 (SE 0.001).
  - Every test fold holds at least 119 rows of the smallest class, so every fold can be scored.
  - Log loss is the Zindi metric, confirmed on the page and given as a source metric with no extra parameters.
- **The order objection:** the ranked probability score, which respects the class order, ranks the models the same way (HistGradientBoosting 1.090 / 0.0817, logistic 1.126 / 0.0849). MET-4's bar for overruling the source's metric is not met.
- **The scorer's column-order risk** (2.537 against 1.592 with alphabetical columns) belongs to the harness, not this definition. The example reindexes the columns correctly.

**6. The cleaning is minimal and every count reproduces (P7: CLEAN-3, CLEAN-11, CLEAN-14, CLEAN-25).**
- **Evidence:**
  - All the counts in the notes reproduce exactly: Widlife 5,988, UAE 187, BURGARIA 2, 94 zero-party rows, and 142 / 104 / 62 / 344 inconsistent codings.
  - Setting both party counts to missing when they sum to zero is backed by the data: `Alone` sums to 1 in 98.7% of rows, so the counts include the respondent and a total of 0 is impossible.
  - The orders of `cost_category` and `age_group` follow CLEAN-25 precedents set the same week.
- **The open quality points are cheap notes (remedy ladder: keep with a note):**
  - `travel_with`: 97.2% of its missing values are one-person parties. Keep them missing, since recoding to "Alone" would be a guess (LEAK-8).
  - The one 371-night row: keep it under CLEAN-11. Removing it is optional and needs a curator CC.

**7. The rest is bookkeeping, and none of it is a reason to hold the dataset (writing; the house rules).**
- `checked_by` lacks Lennart, unlike the ten sibling records shipped on 2026-11-04. Most likely it was missed; this is the precedent checker's consistency question (a).
- The record contradicts itself on whether a panel ran on 2026-10-26. This pass supersedes both statements.
- The 2026-10-29 build is stale. A rebuild is a separate ask from the curator.

Independent failures are not conflicts: I checked that each Must holds on its own (LEAK-10, USE-5, SPLIT-1, PROV-4/6, and SPLIT-8 once the tag decision is made). None needs a higher rule to rescue it.

</details>

<details><summary>Critic</summary>

**Verdict: ship only after changes.** No point below is grounds to exclude the dataset. It is a real survey task with no leak (blind reviewer, column auditor, and the task gamer, who found no exploit). But the definition states things the panel measured to be false, and it leaves out a Must tag and a Should exception. These are text fixes to the definition. The build is stale anyway (README `build_stale: true`), so they cost nothing extra before the curator's build.

**1. The target is documented after all, but the definition says it is not (P3, USE-5 Must, with USE-8 Must and EV-2).**
- **Problem:** `predicted` says "The release does not document monetary boundaries or the expenditure basis". `curation_comments` says "no regression target or monetary boundaries are reconstructed". `fit_reason` lists currency, per-person versus party, and thresholds as unknown.
- **Evidence:** the claim auditor linked 2,401 rows uniquely to the 2020 Zindi cut of the same NBS survey. That cut has `total_cost`, defined in its codebook as "total tourist expenditure in TZS".
  - Cuts at about 0.5M / 1M / 5M / 10M / 50M TZS of the party's total trip cost reproduce the 2022 class for 97.9% of the rows. The same cuts per person give 58.9%.
  - Medians by class are 250k, 829k, 2.55M, 7.29M, 18.2M and 58.0M TZS.
  - The domain practitioner found the same thing independently: mean party size rises 1.43 to 4.43 across the classes, while nights do not rise monotonically.
- **Effect:** the definition gives users and the curator a wrong account of what the label is. USE-5 asks us to "check how the source built its label", and here it can be checked. A measurement outranks a page (EV-2).
- **Remedy (fix the definition, notes only):**
  - Rewrite `predicted`, `fit_reason` and `curation_comments`: the label is the party's total trip expenditure in TZS, binned at roughly these edges. The evidence comes from a third-party copy of the 2020 files, so the edges are approximate.
  - Keep the six classes and log loss. The regression target exists for only the 4.8k-row subset, and log loss is the competition's metric (MET-4).
  - `fit="approximate"` stays. The plan-as-realized inputs and the unknown survey year still justify it.

**2. The "different task" sentence about the 2020 cut is false (P5, PROV-6 Must; PROV-8 and PROV-9 Must).**
- **Problem:** `curation_comments` says "The 2020 regression competition is a different published task/cut".
- **Evidence:** 72.3% of the 4,809 training rows of the 2020 cut have their key in our `Train.csv`, against 23.4% by chance. About 75% is the expected share if all 6,476 rows of the 2020 release sit inside the 24,675 (our file is 75% of them). So the 2020 file is an earlier subset of the same release. PROV-6 names "a swapped target … added … rows" as a duplicate, not a distinct task.
- **Effect:**
  - Uniqueness holds today, because the 2020 cut has no record and nothing ships twice.
  - The stated reason is wrong, and a later screening could add the 2020 cut under PROV-7.
  - About 26% of our rows (around 4.8k) were first published in December 2020, which bears on `year` and `source` (PROV-8, PROV-9).
- **Remedy:**
  - Correct the sentence: "an earlier 2020 subset of the same survey with the raw TZS cost; a duplicate version under PROV-6, not shipped".
  - Add a `No` / `Duplicate` record for the 2020 cut, so it is not screened in later.
  - Curator weighing call on `year`: keep 2022 with a one-line reason (the binned target and about 74% of the rows first appeared then), or take 2020 by the melbourne_housing_market grew-over-versions precedent.

**3. Forced IID from a temporal use case, but no tag (P4, SPLIT-8 Must).**
- **Problem:** the use case is forward-looking: an operator estimates "a specified alternative trip plan", which is a future trip. The source says "before visiting". The release is one undated extract, and `data_tags` is empty.
- **SPLIT-8:** it covers this case word for word: "a release with no dates at all (one extract…)" ships IID tagged `ForcedIIDFromTemporal`, "say what the timestamp … would change".
- **Evidence that time matters here:** the target bins are money categories in TZS, and prices drift. The domain practitioner cites package spend of $411 per night in 2016 against $479 in 2025, and TZS inflation adds to that. So a model from one survey wave would mis-bin later trips.
- **Precedent:** the snapshot cases account_debt_south_africa and bank_customer_churn carry the tag.
- **What does not settle it:**
  - `task_summary.split` already says "does not test future seasons", so the wording is half there.
  - Myunghwan's CC of 2026-10-23 removed a different tag (`Non-IID (Temporal)`). The forced-IID tag was never weighed.
- **Remedy (fix the definition, no re-split):** add `data_tags = ("ForcedIIDFromTemporal",)` and one sentence in `splits_comment`: a dated wave would test drift in the class edges and the visitor mix; recover the wave if NBS publishes it. The only way out is the reframing in point 4, which would make the task cross-sectional by its use case.

**4. The named actor has no use for this prediction, and a better-fitting actor was not weighed (P3, USE-9 Should; USE-1 Must holds).**
- **Problem:** the domain practitioner says a tour operator quotes from an exact rate card and cannot act on a six-way band with no thresholds. Top-1 accuracy is 0.576.
- **The alternative:** the survey's own users (NBS, the Bank of Tanzania) impute or estimate spending from the rest of the exit form. That actor has every input at the right moment (no "realized as plan" stretch, claims 2 and 11), and the random split mirrors its use directly.
- **The rule:** USE-9 asks for this check before settling on approximate, weighed against "a use case rephrased only to excuse a gap". Here the rephrase removes a real stretch and does not excuse the label gap. The fit stays approximate either way, because a band is coarser than the number that actor needs (USE-5 resolution).
- **Remedy:** a curator weighing call. Either restate `use_case` as survey imputation, or add it next to the Zindi actor. If it is restated, point 3 becomes moot.

**5. The 965 kept exact copies need a written exception (P4, LEAK-19 Should; principles "Exceptions").**
- **Problem:** LEAK-19 says to drop exact same-label copies. The definition keeps them, citing LEAK-16 and LEAK-18, but writes no `**Exception to LEAK-19 …**` and adds no Cases row (precedent checker, item 4).
- **The keep is justified on the evidence:**
  - 361 of the repeated profiles are `Alone` travellers, so the copies are different people.
  - 67.8% of copy groups are larger than the party size.
  - A split grouped by profile costs only +0.0047 log loss, and +0.0025 without `age_group`.
  - The task gamer's copy attacks gained nothing (1.0765 against 1.0755).
- **The open risk:** copy rows are enriched for `With Spouse` (44.6% against 27.8% overall). That is a possible LEAK-17 party repeat, and its measured cost is about 0.003.
- **Remedy (note):** write the exception: coarse survey profiles of distinct respondents, which serves P3 because new data repeats them. Put the grouped-split number into `splits_comment` and `accepted_check_warnings` (EV-3), add a Cases row, and name the spouse enrichment as the residual risk.

**6. Scores depend on probability column order, and the order just changed (P6, MET-2; harness-wide).**
- **Evidence:** the scorer reads columns in category order, which became Lower … Highest on 2026-11-04. Alphabetical columns (Zindi's header order, and sklearn's `classes_` on strings) score 2.537 instead of 1.592 for the same prior.
- **Effect:** any result cached under the old alphabetical order is not comparable, and a careless harness gets silent garbage.
- **Remedy:**
  - No change to the definition.
  - One line in the notes or README saying probabilities are scored in the declared class order.
  - Rescore any cached results for this dataset after the rebuild.

**7. Record and quality bookkeeping (P7 and process; not reasons to hold the task).**
- `checked_by` lists only Myunghwan. The ten other records Lennart shipped on 2026-11-04 list him too.
- The record contradicts itself. On 2026-10-26 it says the reviews are "retained in the review evidence"; on 2026-11-04 it says "no panel ran". No such artefact exists.
- The screening text still reads "`mmu_2022` (`TBD -> Yes`)". `mmu_2022`'s duplicate call is `AI (UNVERIFIED)`, with no curator check under PROV-5.
- The build is stale, and container `01a18ad4…` is absent locally.
- Optional notes:
  - `travel_with` NA rows are 97.2% one-person parties (keep NaN, LEAK-8).
  - One row has 371 nights, beyond the 12-month visitor definition (USE-7; keep and note, or drop by curator CC).
- **Remedy:** fix the record lines, have the curator confirm `mmu_2022`, and rebuild on the curator's ask.

**Judgment record.**
```text
Verdict: ship after changes.
Validity: USE-1 holds; USE-5 holds but the notes misstate it (fix notes, point 1); USE-9 not weighed (curator call, point 4);
  SPLIT-8 tag missing (fix, point 3, unless reframed); LEAK-19 departure unwritten (exception, point 5);
  PROV-6 reason false, uniqueness holds (fix note + duplicate record, point 2); PROV-9 year (curator call).
Value: TP holds (prior 1.592, models 1.07-1.13); MET-4 holds; MET-2 column-order note (point 6).
Quality: CLEAN calls hold; travel_with NA and 371-night row as notes.
For the curator: points 2 (year), 3/4 (reframe or tag), 7 (checked_by, mmu_2022).
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: `ai4d_lab_tanzania_tourism_classification_challenge`**

The critic and I agree on the substance. Neither of us finds a leak, a broken Must that cannot be fixed, or any reason to change the data, target, metric or split. Every fix the critic asks for is text in `dataset.py` or the record. The build is stale anyway, so these fixes land before the curator's rebuild. "Ship after changes" and "ship after notes-only changes" are the same verdict here.

**1. The target is documented after all (USE-5 Must, EV-2): concede.**
- What follows: rewrite `predicted`, `fit_reason` and `curation_comments`.
  - The label is the party's total trip expenditure in TZS, cut at about 0.5M / 1M / 5M / 10M / 50M.
  - The evidence: 97.9% agreement on 2,401 linked rows, against 58.9% per person.
  - The edges are approximate because they come from a third-party copy of the 2020 files.
- We agree on the rest: keep the six classes, keep log loss, keep `fit="approximate"`.
- The point strengthens the dataset. The label is now a measured, identified quantity rather than an unknown one.

**2. The "different task" sentence about the 2020 cut is false (PROV-6 Must): concede the sentence. The duplicate record is optional. Dispute moving the year.**
- **The sentence.** PROV-6 names "a swapped target … added or dropped rows" as a duplicate. 72.3% of the 2020 rows match ours, against 23.4% by chance, so the 2020 cut is a duplicate version. Rewrite the sentence as the critic words it.
- **A `No` / `Duplicate` record for the 2020 cut.** It is cheap insurance against a later PROV-7 misreading, so I don't object. But shipping does not depend on it: uniqueness holds today because the 2020 cut has no record and no folder.
- **The year.** PROV-9 takes the year of first publication of what we ship. The airfoil_self_noise case gives the test: an earlier publication counts as the source only when it holds every value of the later file.
  - The 2020 cut fails that test twice. It lacks `cost_category`, our target, which first appeared in 2022. It also lacks about 74% of our rows.
  - The melbourne precedent covers one Kaggle upload growing over its versions. Here there are two competitions, each with its own launch.
  - PROV-9 lists "a competition's launch". The competition whose rows and label we ship launched in 2022.
  - So 2022 has the better footing. Add the one-line reason to the notes. The curator still makes the call (PROV-9 Must), and neither year changes the data.

**3. `ForcedIIDFromTemporal` tag (SPLIT-8 Must): concede, conditional on the use case.**
- SPLIT-8 covers "a release with no dates at all (one extract…)" in so many words.
- The use_case.md example is the same shape: "a credit model scores future applicants, so a random split of undated applications stays approximate".
- So while the planner remains the named actor, the tag and one `splits_comment` sentence are required. Neither needs a re-split.
- The fix sits inside the remedy ladder: the regime SPLIT-8 prescribes is the IID split already shipped.
- If the curator restates the use case as survey imputation (point 4), the task is cross-sectional by its use case and SPLIT-8 does not apply. Either way the data is unchanged.

**4. The named actor has no use for this prediction; survey imputation was not weighed (USE-9 Should): concede.**
- I proposed the same fix in my opening brief.
- One refinement from the rule text. USE-9 says that if another use case mirrors the data, "that is the use case and the fit is direct". The imputation actor mirrors the timing and the random split exactly.
- So the only thing keeping the fit at `approximate` is resolution: a six-way band against the number that actor needs. `fit_reason` should say exactly that, so it does not lean on the plan-as-realized stretch, which disappears under that actor.
- This is still a curator weighing call. It does not hold up shipping.

**5. The 965 kept copies need a written exception (LEAK-19 Should): concede the exception. Dispute that the spouse enrichment is more than a note.**
- **The exception.** Write `**Exception to LEAK-19**` (coarse survey profiles of distinct respondents; serves P3), add the Cases row, and put +0.0047 in `splits_comment` (EV-3).
- **The spouse enrichment.** Its measured cost is about 0.003, below the task gamer's noise floor of a random column (0.0049). The copy attacks gained nothing (1.0765 against 1.0755).
- Grouping on the profile is forbidden by SPLIT-24 (a feature hash), so there is no split remedy to apply.
- Mixed labels inside the copy groups (370 of 718 raw groups) argue against pure party copies.
- So name the enrichment as a residual risk in one clause. It does not count as an open problem.

**6. Scores depend on the probability column order (MET-2): concede the note, and say where it belongs.**
- The finding is real: alphabetical columns score 2.537 against 1.592 for the same prior. A notes line saying "probabilities are scored in the declared class order" costs nothing.
- The defect is in the scorer, which reads columns in category order without checking the labels. It applies to every ordered multiclass target shipped this week (cardiotocography, dementia, hepatitis_c, chicago_traffic_crashes).
- So it is a harness issue for the curator, not a condition on this dataset.
- Rescoring cached results follows from the rebuild in any case.

**7. Record and quality bookkeeping: concede all of it. None of it is a ship condition.**
- `checked_by`: the precedent checker's option (a) is the most likely answer. The curator decides.
- The contradiction about the 2026-10-26 panel: this pass supersedes both statements. Correct the record line.
- `mmu_2022` is `AI (UNVERIFIED)`: the curator should confirm the duplicate under PROV-5. It is `No` and has no folder, so nothing ships twice in the meantime.
- `travel_with` missing values and the 371-night row: notes only. Keep the missing values (LEAK-8) and keep the row (CLEAN-11), unless the curator writes a CC.

**Net.** Nothing in dispute affects validity:
- No leak (LEAK-10 holds).
- The target is identified (USE-5 holds).
- The split is honest (SPLIT-1, SPLIT-31).
- Uniqueness holds (PROV-4/6).
- The metric is the competition's (MET-4).

The open items are text edits plus three curator calls:
- the year, where 2022 is better supported under PROV-9 (airfoil test);
- the actor, where restating it as survey imputation makes the SPLIT-8 tag moot;
- `checked_by` and the `mmu_2022` confirmation.

**Verdict: ship after the notes edits above and the curator's three calls, then rebuild on the curator's ask.**

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic). Verdict unchanged: ship after changes.**

The advocate and I agree on the verdict and on most facts. We still disagree on four things:
- whether the fixes are optional;
- whether a second actor makes the `ForcedIIDFromTemporal` tag unnecessary;
- whether the 2020 cut gets a record;
- what happens to cached scores after the class reorder.

**Advocate 1. No leak, no exploit (LEAK-10 Must holds).** Concede. The only open item is the `With Spouse` enrichment of the copy rows (44.6% against 27.8%), a possible LEAK-17 case. Its measured cost is at most +0.0047, the profile-grouped split, so it needs a note, not a fix.

**Advocate 2. The IID split is honest (SPLIT-4, SPLIT-31, LEAK-16/18/20).**
- **Concede:** the evidence, and remedy (a), writing the LEAK-19 exception.
- **Concede (b), with one correction.** splits.md line 59 says "SPLIT-8 (Must…)". The split auditor called it a Should; that was wrong, and the advocate now agrees. The tag is therefore a required fix whenever the use case is forward-looking. It is not a matter of taste.
- **Dispute "if the curator frames the task as cross-sectional imputation instead, the tag drops out".** That only holds if the planner actor is replaced. The advocate's point 3 adds the survey statistician *next to* Zindi's planner. If the planner stays, the use case is still forward-looking ("before visiting", prices in TZS drift), so SPLIT-8 still binds. Precedents: account_debt_south_africa and bank_customer_churn (splits.md lines 229-230).
  - Rule that decides it: SPLIT-8 (Must).
  - Remedy: tag plus one sentence unless the planner actor is removed.
- **Dispute (c) as "optional".** The exception from (a) has to name the fact that sets this case apart (principles, "Exceptions"). The +0.0047 / +0.0025 grouped-split numbers are that fact for the "copies don't inflate the score" claim. So under EV-3 they belong in the exception text and in `accepted_check_warnings`, not in an optional extra.

**Advocate 3. The target is measured (USE-5 Must holds).**
- **Concede:**
  - the 97.9% / 58.9% evidence;
  - Spearman 0.965 against 0.945, so the declared order is measured;
  - keeping six classes and log loss (MET-4; 18,506 rows against 4,809);
  - party total as "the quantity".
- **Dispute the framing that the objection "now argues for the dataset".** The facts favour the dataset. The definition, though, still says the opposite: `predicted` says "does not document … the expenditure basis", and `fit_reason` lists currency, basis and thresholds as unknown. EV-2 says a measurement outranks a page, so leaving the text as it is ships a statement the panel refuted. The fix is the notes edit we both ask for. It is a condition for shipping, not something to add later.
- **Actor (USE-9 Should).** We agree the "rephrased only to excuse a gap" factor does not bite. Restating the actor or adding one alongside it is the curator's call. As argued under point 2, only restating removes the SPLIT-8 tag.

**Advocate 4. Faithful, ships once (PROV-1/4/6).**
- **Concede:** the byte reproduction (3,147,987 bytes, sha256 match), 18,506 + 6,169 = 24,675, and that nothing ships twice today.
- **Concede the year call.** The advocate's argument for 2022 is sound: it is a separate publication carrying the binned target and about 74% of the rows. I accept 2022 if that one-line reason is written into the definition.
- **Dispute that rewriting the sentence is enough.** The false "different task" premise has already spread. In this very pass, the precedent checker (item 6) wrote "The 2020 regression cut is a distinct task, which PROV-6 allows", taken from that note. A cut with no record is open to a future screening under PROV-7. The mildest guard is a `No` / `Duplicate` record for the 2020 Zindi cut that names this record as canonical (PROV-6 Must: "a swapped target … added rows" is not a distinct task).
- **The advocate also leaves out PROV-5.** `mmu_2022`'s duplicate call is `AI (UNVERIFIED)`, and this record's screening still reads "`mmu_2022` (`TBD -> Yes`)". The curator should confirm it and the stale line should be corrected.

**Advocate 5. Worth benchmarking, metric holds (TP, MET-4/8).**
- **Concede:** prior 1.592 against models at 1.07-1.12; RF beats linear by 0.012 (SE 0.001); at least 119 Highest rows per fold; the RPS ranking matches log loss, so MET-4's bar to overrule is not met.
- **Partly dispute "harness, not this definition".** I agree the definition itself needs no change. But the reorder that created the risk is this dataset's own CLEAN-25 decision of 2026-11-04. Any cached result for this dataset scored under the old alphabetical order is off by up to 0.945 (2.537 against 1.592) and cannot be compared.
  - That is a dataset-specific action under MET-2: rescore this dataset's cached results after the rebuild.
  - Plus one line in the README/notes that probabilities are scored in the declared class order.
  - The example reindexing correctly does not protect results that are already cached.

**Advocate 6. Cleaning (CLEAN-3/11/14/25).** Concede in full: all counts reproduce, the zero-party fix is backed by the 98.7% figure, `travel_with` NA is kept (LEAK-8), and the 371-night row is kept with a note.

**Advocate 7. Bookkeeping.**
- **Concede:** none of it holds the task; `checked_by` goes to the curator as question (a).
- **Dispute "this pass supersedes both statements".** A later pass does not delete a false line from the record. The 2026-10-26 line says the reviews are "retained in the review evidence", and no such artefact exists. It stays in the record and misleads the next reader unless it is corrected (writing rule). The fix is one line.

**Where we still differ (all fixes are text; no re-split, no data change):**
1. SPLIT-8 (Must): tag plus a `splits_comment` sentence, unless the planner actor is *replaced*. Adding a second actor does not remove the tag.
2. PROV-6 (Must): a `No` / `Duplicate` record for the 2020 cut, besides the rewritten sentence. A curator check on `mmu_2022` (PROV-5).
3. LEAK-19 exception: the grouped-split numbers are its required fact, not an option (EV-3).
4. USE-5 / EV-2: the notes rewrite is a condition for shipping, not a nicety.
5. MET-2: rescore this dataset's cached results after the rebuild, and add the class-order line.
6. Record: correct the 2026-10-26 "retained" line.

</details>
