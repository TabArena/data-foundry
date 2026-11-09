# loan_default_prediction_challenge

**Outcome:** added. Myunghwan settled issues 1–3 on 2026-11-05: keep recorded current terms, keep undated mutable profiles, and accept the documented participant-copy provenance gap. All 32 predictors remain. Validity: tested history cutoffs and borrower independence support the implementation (USE-3, LEAK-10/16); accepted timing/provenance uncertainties remain unverified. The split remains a same-cohort random approximation under SPLIT-8. Value and quality: modest signal, adequate fold support, curator-selected AUROC, semantic typing and tested history aggregation support the bounded task (TP-2, MET-4/11, CLEAN-14/19). The real task and reproducible implementation favor retention; restricted coverage and missing availability records limit interpretation. Myunghwan subsequently chose AUROC on 2026-11-08; the source-metric departure is documented below. On 2026-11-08 Myunghwan accepted random or temporal evaluation with attention to borrower overlap. The record now matches the unchanged Random (IID) definition. All issues, field rows and the metric are settled. Myunghwan explicitly said 'ship this' on 2026-11-08, confirming the earlier default-ship disposition. The subsequently requested local build is verified as `01a1be30-45b2-71ef-901f-e94be6c0c4dd`; its generated README records the checksum and clean definition revision.

**Main points:** All four issues and the required_split field are settled; AUROC is primary. Fresh raw-ID lineage checks confirm 4,368 distinct scored borrowers and zero borrower overlap in every one of the nine unchanged folds. Scientific review is complete and Myunghwan explicitly approved ship. The requested build passes save/reload, traced-input reproduction and exact fold/borrower checks with zero errors or warnings. Release permission remains separate and unresolved.

**Record judgment:** Retain the published Good/Bad timely-settlement labels and all 32 predictors. Myunghwan's keep/keep/accept decisions accept the stated limitations; they establish neither application-time snapshots nor organizer-byte equality. The panel below is the preserved original add-stage report; its three proposed issue choices have now been settled. Unknown label-arrival/grace rules and granted-only July coverage remain limitations. The original panel below predates the AUROC and split-field choices and is preserved as historical evidence. Independent actual-mark consistency checks found both choices consistent; no new split exception is required.

**Issues for Myunghwan:**

1. **Keep recorded loan terms when their application-time availability is unknown?**

   The [source dictionary](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data) describes issued/taken amounts, total due and duration, without proposed-versus-final versions. If terms were fixed after the lending decision, including them could overstate application-time prediction. No such timing mechanism is demonstrated. USE-3 and LEAK-10 are Must rules; approximate fit cannot waive a confirmed later input.

   Implemented: retain `loanamount`, `totaldue` and `termdays`, explicitly conditional on recorded issued-loan terms, with availability unverified. Both debate sides recommend this bounded version, while acknowledging that Olist's known checkout promise does not establish when these terms were fixed. Alternative: request a strict pre-offer variant dropping these three fields and requalifying it; this removes recorded contract information and requires a new assessment, while profile timing remains unresolved. Original proposal/version records would settle the fact. Recommendation: retain the conditional approximate version. Decision needed: keep it or request the stricter variant.

   **Myunghwan (2026-11-05, as implemented):** keep

   **Resolved (2026-11-05, Myunghwan):** Keep the recorded current loan terms, with their application-time availability unverified.

2. **Keep customer profiles without historical snapshot dates?**

   Employment, bank and location values may have changed after application. The demographic join is deterministic and uses no labels or fitted statistics, but this cannot date the profiles. Employment is missing for 20.17% of Bad versus 13.61% of Good loans. A diagnostic predicting whether employment is missing from dated history and application information improves its prediction loss by only 0.00171 when also given the outcome. Risk-linked nonresponse remains a competing explanation, so neither leakage nor availability is proved (USE-3/LEAK-10 Must; EV-6 Should, EV-7 Must).

   Implemented: retain the supplied profiles with an explicit cannot-verify limitation. The adverse kick/Cauca/African-credit precedents had an established later-recording mechanism; none is established here. Alternative: remove bank account type, bank name, branch, employment, education and GPS coordinates, then requalify; this loses profile information and requires a new assessment. Completed age remains. Dated profiles or a source statement would settle availability. If later updating is established, reconstruct, mask or drop affected fields. Recommendation: retain the current profiles with availability explicitly unverified. Decision needed: keep these profiles or request the stated conservative variant.

   **Myunghwan (2026-11-05, as implemented):** keep

   **Resolved (2026-11-05, Myunghwan):** Keep the undated mutable customer profiles, with timing unverified.

3. **Accept the documented participant-copy provenance gap?**

   The original [DSN/Zindi task](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction) is traced, but qualification uses the [Megan Beckett copy at a pinned commit](https://github.com/MeganBeckett/zindi-loan-prediction/tree/16379560b10bda88b957c180d4767a37a61454a3). File identities verify that copy; no organizer-byte comparison exists. Unobserved uploader changes could alter the benchmark, although no damage or generated-label mechanism was found. PROV-2 (Should, narrowing PROV-1 Must) permits bounded consideration; hr_analytics shows why a copy's hashes must not be presented as original-label authentication.

   Implemented: name the original source and exact copy, with organizer equivalence explicitly unverified. Alternative: defer inclusion until organizer files can be compared, leaving this task unavailable pending that evidence. Recommendation: knowingly accept the bounded-copy provenance. Decision needed: proceed with this identified copy or defer for comparison. Differing redistribution terms remain a separate release prerequisite, not a scientific rejection reason (EV-4).

   **Myunghwan (2026-11-05, as implemented):** accept

   **Resolved (2026-11-05, Myunghwan):** Accept the identified participant-copy provenance gap, without certifying organizer-byte equality.

4. **Use AUROC instead of source hard-label error?**

   - **Problem:** The source scores misclassification error, represented previously as accuracy. Always Good obtains 78.2051% accuracy; matched untuned LightGBM obtains 78.7698% accuracy and 0.694156 AUROC over the same nine folds. Its hard-label threshold was selected within training. These results motivate the curator's preference; they do not prove accuracy invalid.[^metric4]
   - **Myunghwan (2026-11-08, change):** I think AUROC looks better than. Accuracy is skiewed
   - **Answer (AI, 2026-11-08):** AUROC compares discrimination without choosing a threshold. The preceding chat explained that this overrides the competition's hard-label score. Independent consistency review accepts the informed metric-only choice; no split or operational lending-cost claim is inferred.
   - **Resolved (2026-11-08, Myunghwan):** Declare context `roc_auc`; retain source accuracy and matched diagnostic results in the evidence. This case-specific MET-4 departure serves P3 and is recorded in the definition, record and Cases table. All data, features and folds stay unchanged.

[^metric4]: MET-4 normally retains competition scoring; MET-11 permits context origin for an overruled source metric. This is an explicit curator choice, not a general imbalance rule.

**Review panel:** ship after changes (mediator), conditional on the three curator choices. Full tier: all ten roles, with one rebuttal per debate side. Independent audits found no current numeric/implementation claim refuted, while proposed-term status and snapshot timing remained unverified. Blind review: include with changes; raw-ID and event-cutoff audits answer its mechanical questions. Both debate sides agree on the bounded recommendation; the remaining choices are not settled human decisions. The evidence and debate reports below assess the wording before repair. The final draft now describes recorded issued-loan terms, the midnight due-proxy cutoff, sub-hour event boundaries and nominal branch categories. Input timing and organizer equivalence remain unverified; the repairs change no predictors, labels, folds or metric. The review editor confirmed the presentation corrections; the editor section gives its current conclusion.


<details><summary>Mediator</summary>

**SuperLender mediation, 2026-11-05**

Verdict: ship after changes, as a recommendation for the bounded approximate task, conditional on curator disposition of the three issues below. This is not acceptance, a new exception, build, commit or release authorization.

Validity: USE-1/5/8 support a real timely-settlement task; USE-3/LEAK-10 remain cannot-verify for current terms and mutable profiles. SPLIT-8 supports ForcedIIDFromTemporal; mature chronological refits are not certified under SPLIT-9/10. PROV-1/2 permit bounded consideration of the identified copy, without organizer authentication. No irreparable Must violation is demonstrated.

Value: TP-2 supports modest real signal; fold support is adequate. MET-4/11 retain source error as accuracy by exact identity. Quality: CLEAN-14/19 support semantic typing and tested history aggregation; the explanations need small repairs.

Weighed: real repeat-lending decision and reproducible mechanics favor retention; uncertain application inputs, restricted cohort/label documentation and copy authenticity limit what the benchmark establishes. Lower-ranked value cannot clear a validity failure.

No new experiment was necessary: the existing decisive tests settle computational disputes, while another model cannot recover missing timestamps.

**Changes now, without a scientific decision**

- Replace unsupported “proposed” claims with recorded issued-loan terms and explicit unverified application-time availability throughout the task summary/notes; regenerate README. Preserve the application decision and conditional approximation (USE-1/3/8; EV-7).
- State that all 756 masked settlements and 664 first payments fall within one hour after application on supplied clocks (maxima .99444/.82556 hours). Retain strict masks; infer neither a clock correction nor multi-day outstanding borrowing (LEAK-7/10; EV-6/7).
- Name `2017-07-30 00:00` for the 299 due-proxy count; 339 is before July 31 midnight. Neither is measured label arrival or proof temporal evaluation is impossible (SPLIT-9/10; EV-7).
- Document the nominal real-branch interpretation supporting categorical type, retaining raw entries and missingness (CLEAN-14 Should). No arbitrary merges, coordinate clipping or sparse-field deletion is justified.

Record/definition alignment is a field correction, not another issue (writing.md):

| Field | Current record | Definition / recommendation |
|---|---|---|
| required_split | `?` | Random (IID), explicitly ForcedIIDFromTemporal and approximate; align when recording the curator's disposition, without implying prior human approval. |

**Three curator issues, ranked**

- Current terms at application (P3/P4; USE-3 and LEAK-10 Must). Recorded amount, total due and duration may follow the approval/offer decision; treating them as proposals could overstate application-time performance. The advocate's strongest case is that contractual terms can be known before outcome and no later-value mechanism is established. The critic's strongest case is the source's taken/disbursed definitions and absent proposal versions; dropping approval does not date the remaining fields. Both now agree on cannot-verify. Recommend retaining the conditional approximate version with this risk explicit. Decision: accept that bounded version, or request a strict pre-offer variant dropping the three current-term fields and requalifying it. That variant reduces inputs without proving the remaining snapshots timely. Proposal/version documentation would settle the fact; the curator is not asked to supply nonexistent evidence. A later-stage framing needs an independently real decision (USE-9).

- Mutable demographic snapshots (P3/P4; USE-3/LEAK-10 Must; EV-6 Should). Later employment/bank/location updates could improve prediction using information unavailable then. Advocate: deterministic joins recover legitimate profiles without targets or fitted statistics. Critic: profile effective dates are absent; employment missingness is 20.17% for Bad versus 13.61% for Good, with conditional log-loss improvement .00171 after adding outcome. Risk-linked nonresponse remains equally plausible; this is neither demonstrated leakage nor clearance. Recommend explicit cannot-verify retention for the bounded version. Decision: accept that uncertainty or request a conservative variant removing undated mutable profiles, with requalification. Owner snapshot semantics/dated versions would settle timing; if later updates become established, reconstruct, mask or drop affected fields. Approximate fit grants no waiver.

- Participant-copy authenticity (P5; PROV-1 Must, narrowed by PROV-2 Should). The copy is reproducible, but unobserved uploader changes could alter the benchmark. Advocate: seven hashes match the pinned participant manifest, source/schema are traceable, and no corruption/generation mechanism was found. Critic: hashes authenticate this copy only; organizer equivalence remains untested. Recommend knowingly accepting this documented provenance gap under amended PROV-2. Decision: accept bounded-copy qualification or defer for organizer comparison. Neither choice establishes byte equality. Redistribution terms remain a separate release matter (EV-4).

**Agreed facts and settled disputes**

The 4,368 rows represent distinct scored borrowers/loans: 3,416 Good, 952 Bad, July 1–30, 2017. Bad means not timely settlement, not permanent default. Independent raw-ID and invariance tests answer the blind review's borrower/join/event-cutoff concerns: no per-fold borrower/exact-copy overlap, no current/history loan overlap, and all 18 history predictors independently reconstructed. Nine borrowers lack supplied history; 32 counts differ from sequence minus one. Demographic union recovers 1,099 profiles without conflicting keys.

Nine folds each test 1,456 loans, including 317–318 Bad. Claim-auditor mean AUC .6942 and accuracy gain .00565 over constant Good demonstrate modest signal, not timing validity. Chronological windows can be constructed, but label maturity cannot be certified. SPLIT-8 resolves the regime; neither offer-value grouping gaps nor shared GPS establishes an entity. No additional curator choice or model suite is warranted for these settled points.

**Precedent consistency**

Follow mobile_churn/Cauca for forced IID, not Alfa/Lending Club's dataset-specific maturity exceptions; preserve source metrics as in Porto Seguro/African credit. Distinguish mutable-profile cases kick/Cauca/African credit by the absence here of an established downstream mechanism, not by immunity for demographics. Olist's known checkout promise does not authenticate these terms. PROV-2 supports transparent copy risk; hr_analytics warns against claiming hashes prove original labels. No conflicting Myunghwan decision, third exception or new amendment is established. Qualification authorization alone remains the only current human decision.

</details>

<details><summary>Claim audit</summary>

**Independent claim audit — SuperLender add-dataset Phase A**

Independent audit of the identified participant-copy task, completed 2026-11-05.

The strongest remaining uncertainty concerns whether the demographic snapshot and current loan's recorded terms actually existed at application. The definition acknowledges it, but `fit="approximate"` does not verify these inputs. The independent tests found no implemented outcome-event leakage, row multiplication, relabeling, repeated customer across folds or exact feature copies. All nine declared native accuracy scores are computable and agree with the source's error identity. Temporal deployment performance and organizer-byte equivalence remain unverified, as the definition says.

The auditor independently regenerated the native frame and all declared splits, checked source-row target lineage and raw identifiers, reconstructed history predictors, and scored all nine folds. Measurements apply to the pinned participant copy, not authenticated organizer bytes.

Fresh native frame values and order equal the supplied panel Parquet. A strict pandas `.equals` comparison differs only in category storage dtypes after Parquet round-trip (object versus string category storage), not content; normalized `assert_frame_equal(check_dtype=False, check_categorical=False)` passes. Native `order_rows` deliberately orders/shuffles rows; source-to-native lineage was independently joined one-to-one using creation date, sequence, amount, total due, coordinates and age, then every target was checked against its source row. A direct source-order target comparison was rejected as an inappropriate test after this documented native row ordering was inspected. The 60-row reduced-cohort invariance comparison allows harmless int/float promotion caused by the presence of missing history outside the subset; values match.

**Primary source checks**

Opened both primary pages directly through web retrieval on audit date (not merely a search snippet):

- [Original challenge, Evaluation](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction), lines 33–47: the application-level repeat lending framing is explicit and Evaluation states: “The error metric used will be the percentage of loans you predict incorrectly.” Submitted outcomes are binary labels; this page states no probability threshold, cost matrix, averaging choice or scoring weights. Accuracy reverses this row-level error and model direction. MET-1/3/4/11/12 hold for this declared mapping; MET-5/6 are paper rules, not a reason to replace this competition's metric.
- [Original challenge, Data](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data), lines 39–71: describes demographics, a repeat scored loan, previous loans, creation/approval, settlement and first payment dates. It defines Good as timely settlement and Bad as failure to settle on time. This is not a documented permanent-default target. It does not document demographic snapshot times, the finalization time of current terms, label arrival dates, extraction cutoff or grace period. Its description of amount as a value taken and total due as disbursed capital plus charges cannot establish that those stored values were already fixed at application.

No source quote or page comparison authenticates participant CSV bytes to the organizer release. The primary source corroborates schema and narrative, not exact file equivalence. No new organizer files or labels were manufactured.

**Claim table**

“Holds” means the stated bounded claim survived the named refutation test; it never means absence of every possible leak. “Untested” includes cannot-verify from these data. The quoted statements are from the definition before wording repair. The implementation tests remain relevant to the unchanged predictors, labels, folds and metric; the quoted proposed status was unverified and has been replaced by recorded issued-loan terms.

| Exact claim | Source | Test designed to refute it | Result | Evidence | Rule |
|---|---|---|---|---|---|
| “Will this customer's repeat loan be settled on time?” | `task_summary.question` | Compare published target meaning with primary dictionary and check loan sequence | holds as published label task | Original Data page defines timely settlement; no alternative default target constructed; all 4,368 labels preserved | USE-1/5, EV-2 |
| “SuperLender scores an existing customer's application, with its proposed terms and earlier borrowing history, to inform approval and the offer. The source describes this repeat-business lending decision.” | `task_summary.use_case` | Read original application/repeat-risk framing; inspect source schema for proposed-vs-final terms | holds for actor/decision/history; untested for “proposed” status of stored terms | Primary task states application-time lending decision and repeat-risk history. No stored-term finalization timestamp exists | USE-1/3/6, LEAK-10 |
| “One of 4,368 labeled SuperLender loans, one per customer, applied for during July 1-30, 2017.” | `task_summary.row` | Count rows, unique loan/customer IDs, date extrema and calendar months | holds on participant copy | 4,368 rows/customer IDs/loan IDs; 2017-07-01 00:35:20 to 2017-07-30 21:55:43; one month | USE-1, PROV-1, EV-1/2 |
| “The published Good or Bad flag: settled on time or not settled on time. The grace period, extraction cutoff and exact label-arrival dates are not supplied; Bad includes failure to settle on time.” | `task_summary.predicted` | Read primary target description; inspect current-loan schema for outcome-arrival fields | holds for label meaning and missing documentation; exact operational construction untested | Good=3,416; Bad=952; current performance contains no settlement/first-payment/label-arrival date | USE-5/8, EV-7 |
| “Application time, recorded offer amount, total due and duration, loan sequence and referral status; customer age, location, bank, employment and education; summaries of issued history and only payments and settlements recorded before application. Demographic snapshot and offer timing are unverified.” | `task_summary.known` | Check fields, timestamps, event masks; change unavailable events/current approval; inspect primary collection timing | holds for implemented masks and admission of uncertainty; untested for full application-time availability | 756 future settlements and 664 future first payments; replacing with missing does not change features; demographics/offer timestamps absent | USE-3/8, LEAK-10, EV-2/7 |
| “Random held-out customers from this July cohort, not a verified simulation of later applications. All labels come from one month and their arrival times are missing, preventing verified temporal refits.” | `task_summary.split` | Rebuild all splits; check cohort and outcome timestamp availability | holds in the stated limited sense | 3 repeats ×3 folds, independent customers within each fold; only July labeled cohort; cannot verify chronology of training-label arrival | SPLIT-8/9/10/14, EV-7 |
| “We unite the two unlabeled demographic files, collapse exact demographic copies, join one row per scored loan, and aggregate earlier history while masking later payment/settlement events.” | `task_summary.changes` | Recount union/dedup/join and assert cardinality; perturb masked events | holds | 5,833 demographic input rows−15 exact copies=5,818 customers; no conflicts; one output per scored row; perturbation passes | LEAK-10/16, PROV-13, EV-1 |
| “Evaluation is forced IID from temporal; no current loan is relabeled or added from history.” | `task_summary.changes` | Inspect task regime/tag, reconstruct lineage, compare current/history loan IDs and all target values | holds on this copy | IID tag declared; zero current/history ID overlap; all current targets preserved after native row ordering | SPLIT-8, LEAK-4/10, USE-5 |
| “This is one granted-loan cohort with unavailable label-arrival dates, an unspecified label grace rule and unverified demographic/offer timing. Random splits cannot establish chronological deployment performance. The pinned participant copy is not authenticated against organizer bytes.” | `task_summary.fit_reason`; `fit="approximate"` | Inspect rows, schema, split and provenance; look for verification artifacts | holds as accurate limitation statement; underlying unverified timings remain untested | Primary dictionary describes taken loans; no rejected applications, label arrivals or organizer hashes in inspected evidence | USE-5/8, PROV-1/2, EV-7 |
| “Current approval time is dropped because it follows creation.” | curation prediction-point bullet | Count creation/approval order and change all current approvals | holds | 4,368/4,368 approvals after application; approval column absent from cleaned feature frame; perturbation leaves features unchanged | USE-3, LEAK-10 |
| “preserve both classes and all 4,368 labeled loans. There are 3,416 Good and 952 Bad outcomes.” | curation source-label bullet | Compare raw/clean/native row counts and row-level target lineage | holds | Exact counts and labels preserved; no history relabeling | USE-5, PROV-13, MET-2 |
| “The 5,818 distinct customer records have no conflicts; 1,099 labeled customers' profiles are in testdemographics. No test labels or fitted all-row statistics are used.” | curation demographic bullet | Union/dedup, conflict check, match test demographic IDs; target shuffle and reduced scored cohort | holds for this implementation | 0 conflicting duplicates; 1,099 recovered profiles; no missing joined profiles; test demographic schema has no labels; features invariant to shuffled target and removing other borrowers | LEAK-4/5/10/30, EV-1 |
| “retain loans whose creation and approval precede the scored application's published creation timestamp.” | curation history bullet | Timestamp compare on every joined raw history row | holds | All 18,183 prior rows have both earlier creation and approval; zero current-loan ID overlap | LEAK-10 |
| “Nine scored customers have no supplied prior rows despite loan sequence at least two; their observed counts are zero and historical means stay missing.” | curation history bullet | Compare scored borrowers with history keys and inspect outputs | holds | Nine absent-history customers; counts zero; unchanged missing numerical aggregates; zero rows dropped | CLEAN missingness rules, USE-5, EV-1 |
| “Counts match sequence minus one for 4,336 of 4,368 loans, so complete history is not asserted.” | curation history bullet | Direct equality of observed count with raw sequence−1 | holds | 4,336 equality cases; 32 do not match | USE-5, PROV-2, EV-7 |
| “Mask 756 later settlements and 664 later first payments. Scheduled first-due dates are known loan terms, including future due dates.” | curation history-events bullet | Count future events; replace them with missing; read source due-date semantics | holds for masking; holds as scheduled dates, with schedule-revision timing untested | Future event counts exact; perturbation leaves feature values unchanged; 1,574 future scheduled first dues. No before-approval history payments/closures found | LEAK-10, USE-3/6, EV-2/7 |
| “birthdate becomes completed age at application; drop raw borrower/loan/referrer identifiers, birthdate and current approval time. Retain referral as a category.” | curation features bullet | Inspect transformations and resulting feature names/types | holds | Age calculated from birthday comparison at application; listed raw IDs and approval absent; referral is categorical; 32 features | USE-3, CLEAN type/identifier rules |
| “Physically invalid coordinates become missing without dropping a loan. Missing categorical fields remain missing for the model pipeline.” | curation features bullet | Inspect bounds logic and raw values; compare row count/missingness | holds as implemented rule; no invalid-coordinate case exercises masking here | 0 supplied coordinate values beyond physical bounds; no dropped rows. Category missingness is retained | CLEAN missingness/types, EV-7 |
| “At July 30, only 299 loans reach the contractual due proxy before cutoff; even all 919 shortest-term loans are below the 2,184-row training floor. Due dates are not measured label-arrival times.” | curation split bullet, `_decisions` | Independently reconstruct approval+term proxy and count cutoff; inspect missing actual arrival fields | holds with exact midnight cutoff; actual maturity untested | July 30 00:00 proxy=299; July 31 00:00=339; minimum-term cohort=919; floor=2,184. No arrival dates; early settlement not inferred | SPLIT-8/9/10/14, EV-7 |
| “The source test file has no labels and clock-only application dates.” | curation split bullet | Inspect actual testperf columns and date-string patterns | holds on copy | `good_bad_flag` absent; 0/1,450 creationdate strings contain a calendar date | SPLIT-8, PROV-2, EV-1 |
| “source hard-label error, represented by accuracy with error = 1 - accuracy. The source fixes no 0.5 probability threshold; any threshold must be chosen only from training data.” | curation metric bullet; `Metric.source("accuracy",...)` | Open original Evaluation; inspect native spec; score dummy/perfect labels on each fold and test identity | holds | Explicit original error metric; native prediction=`label`, identity transform, no inputs/weights; all 9 fold identities exact, perfect=1 | MET-1/2/3/4/11/12 |
| “Default stratified IID splits, forced from temporal under SPLIT-8: held-out loans/customers of the same July 2017 cohort, not prospective refits.” | `splits_comment` | Rebuild split indices and compare every SHA with package identity; test borrower/copy overlap | holds for disclosed IID stand-in | All nine split SHA pairs match; each train=2,912/test=1,456; both labels in all folds; no per-fold row/customer/feature-copy overlap | SPLIT-8/14, MET-2, LEAK-16/17 |
| “only granted loans, one July cohort, uncertain label grace/recording window, potential demographic/offer snapshot timing, and participant-copy provenance.” | curation cohort/source-limits bullet | Attempt to find denied applications, wider labeled periods or timing metadata | holds as stated limitation; completeness of source population untested | Inspected scored copy has only taken loans and July labels; none of missing metadata recovered | USE-5/8, PROV-1/2, EV-7 |
| “Git blob hashes authenticate that copy only, not equivalence to organizer bytes.” | download description | Re-hash all seven acquired CSVs against manifest; search for organizer equality evidence | holds; organizer equivalence untested | All seven SHA-256 hashes match manifest; participant commit pinned `16379560b10bda88b957c180d4767a37a61454a3`; no organizer byte comparison | PROV-1/2/13, EV-2/7 |
| “Accepted warnings {}” / README reports no bundle errors or warnings | claims and generated README | Compare accepted map and native initial output | holds only as existing native result | Accepted map empty; parent native check records 0 errors/warnings/infos and 26 checks; no implication that timing questions are resolved | EV-3/7 |
| Implicit: every shipped input was known at application | definition's feature inclusion | Compare primary descriptions to precise prediction point; seek snapshot/finalization timestamps | untested | Proposed terms, changing employment/education/bank/location profiles, referral entry and possible schedule revisions lack their own known-at timestamps. Post-event masks do not prove these fields' availability | P3/P4: USE-3, LEAK-10, EV-2/7 |
| Implicit: no row is a copy across a split | all nine split definitions | Exact feature duplication with/without creation time; native train/test feature hashes and restored customer IDs | holds for exact-copy and named-customer mechanisms tested | Zero full-feature duplicate rows even after dropping time; zero exact-copy/customer intersection on every fold. Supplied hidden-group near-copy test also ran and found 0% at 0.85 similarity | LEAK-16/17/18/19/20, EV-3 |
| Implicit: native metric is meaningful on this release's targets/classes/balance | source metric metadata | Compare unchanged source-copy classes/balance and evaluation unit, then score all folds | holds within participant release; organizer-label equality untested | No class merge, resampling or target transform; one loan/customer per row, no scoring-only inputs needed; 317–318 Bad per test fold | MET-2/3 |

**Native scoring, all nine folds**

Accuracy accepts hard class labels, not probabilities. A constant Good prediction is only a computability/identity check; its high accuracy is not learnability evidence under EV-5. The target's native categories are Bad, Good. No k, grouping, patient sequence, cost or weight columns are required.

| repeat | fold | train rows | test rows | test Good | test Bad | native constant-Good accuracy | 1−direct error | perfect score |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 2912 | 1456 | 1139 | 317 | 0.7822802198 | 0.7822802198 | 1 |
| 0 | 1 | 2912 | 1456 | 1139 | 317 | 0.7822802198 | 0.7822802198 | 1 |
| 0 | 2 | 2912 | 1456 | 1138 | 318 | 0.7815934066 | 0.7815934066 | 1 |
| 1 | 0 | 2912 | 1456 | 1139 | 317 | 0.7822802198 | 0.7822802198 | 1 |
| 1 | 1 | 2912 | 1456 | 1139 | 317 | 0.7822802198 | 0.7822802198 | 1 |
| 1 | 2 | 2912 | 1456 | 1138 | 318 | 0.7815934066 | 0.7815934066 | 1 |
| 2 | 0 | 2912 | 1456 | 1139 | 317 | 0.7822802198 | 0.7822802198 | 1 |
| 2 | 1 | 2912 | 1456 | 1139 | 317 | 0.7822802198 | 0.7822802198 | 1 |
| 2 | 2 | 2912 | 1456 | 1138 | 318 | 0.7815934066 | 0.7815934066 | 1 |

An independent bounded LightGBM diagnostic adds source-metric context: 150 trees, 15 leaves, minimum child 30, learning rate .05, two threads, one fixed configuration. The threshold is chosen exclusively on a stratified 25% subset of each training side from a pre-fixed grid; the same configuration is then refit on the whole training side before testing. No test labels choose thresholds or models. Across all nine native folds, mean accuracy=0.7876984 against constant-Good 0.7820513 (difference +0.0056471); it exceeds that baseline in eight folds and loses in one. Mean ROC AUC=0.6941556; held-out log losses range 0.47118–0.49913. This confirms usable ranking/probability signal while showing that the declared hard-label metric resolves only a modest gain for this quick model. It does not justify replacing the competition metric, declaring triviality/no signal, or claiming tuned performance. Repeated folds are dependent, so no independent-sample significance claim is made.

**Existing native probes read adversarially**

These are supplied native results, not independently rerun model suites:

- Task probes: nine splits; linear AUC 0.66933, random forest 0.68413, LightGBM 0.67631; selected single-feature AUC 0.62394; smallest class=317; no flags. This does not prove input timing. The independent quick model above tests the stronger concern that source accuracy might hide the available ranking signal.
- Leak probes: three splits, 31 numeric/category features (datetime omitted by that probe); all-feature AUC 0.67366; depth-2/3 trees 0.63639/0.63389. Exact-copy share=0. Nearest-neighbor distance AUC=0.50431, unlike the full model. No reported single-feature saturation. These tests do not answer demographic snapshot/finalization timing.
- Hidden groups: ten candidates, no hits; 528 composite keys checked with zero repeated key rows. Near copies explicitly ran on all 32 columns: no paired clusters at 0.85; at relaxed 0.7 threshold, 0.87% of rows are paired. No source-backed shared entity was established. The `totaldue` random-vs-grouped skill gap 0.27525 is a feature-value holdout gap, not borrower identity evidence; amount/price terms are ordinary features. Do not group on it from the gap alone (SPLIT-4/30, EV-3).
- Generated probes: 60.8% of 508 column pairs dependent, 1/20 uniform (creation date); within-class 62.9% of 952 pairs dependent, 2/35 uniform; no pure-minority leaves; no flags. Combined source narrative and these checks supply no generated-data mechanism. Absence of these marks does not authenticate source bytes or prove all data are real (EV-3, PROV-3).

**Historical assessments, not current findings**

The 2026-11-03 screening explicitly supersedes older unverified statements. The 2026-11-04 curator line authorizes qualification and this panel, not final inclusion or a timing exception.

| Historical claim | Test | Result and consequence | Rule |
|---|---|---|---|
| 2026-10-22: “hard labels at 0.5 with no costs stated, so a candidate for overruling under MET-4 and MET-6 once probed” | Read original Evaluation and inspect submitted labels | refuted as a claimed source threshold/rationale. Source fixes binary decisions and error, not probability=0.5; MET-6 concerns paper thresholds. Already superseded by later screening/current definition | MET-4/6/11, EV-2 |
| 2026-10-22: previous payment/settlement fields “known only for loans closed before the application date” | Check event-specific masks and source meanings | refuted if interpreted to require whole loan closure before using any first-payment/history information. Payment and settlement have separate event times; previously issued outstanding loans have usable terms and observed status. Current implementation correctly distinguishes them | USE-3/6, LEAK-10, EV-1 |
| 2026-10-22: “fit direct; regime temporal” | Compare actual missing label timing and current stand-in split | refuted as a current fit claim. Actual copy cannot verify chronological mature-label refits; current definition accurately declares approximate fit/IID stand-in. Not a new contradiction requiring restoration of the old claim | USE-8, SPLIT-8/9/10/14 |
| Older unverified source numbers/one customer per scored row | Independently count supplied files and identifiers | counts now hold on the participant copy, not authenticated organizer files; historical absence of measurement must not be treated as evidence | EV-2/7 |
| Screening duplicate/source-history claims about the full 1,293-record catalog, absence of papers, participant-winning narrative and source-test discussion threads | No new catalog sweep, paper search, thread scrape or winner reproduction in this audit | untested here, already bounded/provisional in screening. None is needed to assert the measured package claims above | EV-4/7, PROV-4/5/16/18 |

**Ranked unresolved and refuted items, with mildest remedies**

- **P3/P4, Must — input timing remains untested (USE-3, LEAK-10).** Offered terms and demographic records plausibly exist at application but their stored versions are not timestamped. The source describes amounts as taken/disbursed and terms as an outcome of the approval/offer decision. Mechanical event masking cannot establish they were proposed rather than finalized values, nor that snapshots predate the scored application. Keep this uncertainty visible for the mediator. Mildest remedy: obtain primary timing/collection documentation or a source-backed proposed-offer/updated-profile timestamp and compare stored values as of application. If the source confirms they are later updates, use earlier versions or drop the affected fields; a source-described post-offer, pre-outcome prediction stage may be considered only if it represents a real decision. Do not mark this “no leak” because scores are modest, and do not treat approximate fit as an exception to a demonstrated leak. No demonstrated timing leak was found in this audit.

- **P3/P4 — exact label rule and chronological maturity remain untested (USE-5/8; SPLIT-9 Must, SPLIT-10 Should, SPLIT-8/14 Must).** The real-world flag is primary-source supported, but grace, cutoff, early settlement and recording delays are not supplied for current loans. The 299/339 contractual due proxies are diagnostics, not observed mature-label counts; 919 shortest-term loans are below 2,184 but do not establish that no labels arrived early. Mildest remedy: retain the explicit ForcedIIDFromTemporal/approximate wording; recover actual arrival/settlement timestamps and wider cohorts before making chronological deployment claims. The current definition already avoids the overclaim. No valid temporal comparison was fabricated, and none can currently be certified.

- **P5 — participant-copy origin is pinned; organizer equivalence remains untested (PROV-1 Must, PROV-2 Should, EV-7).** Seven local hashes match the acquisition manifest and the package is reproducible from those bytes. This does not establish equality to the organizer release or correctness of every uploader transformation. Mildest remedy: retain the pinned-copy caveat; compare organizer hashes/bytes if acquired with authorized access. No observed corruption warrants invented repairs or exclusion solely because authentication is incomplete; the mediator should weigh the precise provenance gap under PROV-1/2.

- **P6 — source metric has a small empirical gain for the bounded model, not a metric failure (MET-2/4, TP-1/2).** Mean native accuracy improves 0.00565 over majority while AUC is 0.69416; eight of nine folds improve. Mildest remedy: report this limited resolution alongside the declared source accuracy. If future tuned results raise a task-value concern, compare appropriate methods on these same splits. This quick diagnostic does not support changing metric, rejection, or “solved/trivial” claims.

- **Historical refutations already repaired in current text (MET-4/6; USE-3/8; LEAK-10).** Unsupported source threshold=0.5, whole-history-loan closure gating and direct prospective fit should not re-enter future summaries. Mildest remedy: continue to mark older paragraphs superseded; current definition already corrects them.

- **Quality clarification — July 30 cutoff is midnight.** The 299 figure is correct for `2017-07-30 00:00`; by July 31 midnight the due proxy is339. Mildest remedy: if rewording notes, name the time boundary explicitly. Both remain far below half the cohort, so the substantive maturity conclusion does not change.

License/redistribution terms are not a curation rejection reason (EV-4). The task is not declared ethically objectionable from ordinary demographic fields, no source population expansion was invented, and no release permission decision was made here. No material current numeric or implementation claim was refuted; crucial unverified claims remain explicitly untested rather than upgraded to holds.

Additional clock check, independently measured after the first pass: the 756 masked later settlements occur at most 0.994444 hours after the scored application, and the 664 masked first payments at most 0.825556 hours after it. This concentration supports clock-offset uncertainty as an alternative explanation, not proof of an offset or of chronological event availability. Strict recorded-time masking remains justified; no one-hour adjustment was inferred. The minimum current loan sequence is two, and every tested historical mean/max for the nine absent-history customers is missing as claimed (`measurements.json`).

</details>

<details><summary>Column audit</summary>

**SuperLender independent column audit — Phase A**

Independent column assessment completed 2026-11-05.

**Recommendation:** no demonstrated outcome leak or broken history aggregation was found. Do not mark application-time offer and mutable-profile availability verified. The source describes realized loan terms. The repaired definition calls them recorded issued-loan terms and explicitly leaves application-time availability unverified. Employment missingness warrants a measured, explicitly unresolved timing question. The conservative history-event masking is correct on the published clocks, but its effect is entirely inside a one-hour boundary and should be described accurately. These are distinct from a demonstrated post-outcome field that would have to leave under LEAK-10.

- Primary [Zindi codebook](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data) and [competition use case](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction) were opened in this audit. The former defines the raw columns; the latter places the credit decision at application and describes determining the offer from risk. No collection/update timestamps for demographics or proposed-offer history are provided there. The codebook's previous-loan `loanamount` description repeats the application-date text; its monetary interpretation is supported by the performance-field definition and measured positive numeric values, not that apparent typo.
- Raw copy identity: Megan Beckett participant repository commit `16379560b10bda88b957c180d4767a37a61454a3`; organizer-byte equality remains unverified. Measurements below apply to this copy.

**Independent tests actually run**

All 18 history predictors were independently reconstructed for all 4,368 loans; frame values and row order agree after accounting for category-storage differences. The independent calculations, rather than a strict category-container equality check, establish semantic parity.

- **Identity/cohort:** 4,368 unique scored customers and loans; Good 3,416, Bad 952. Zero feature duplicates, zero constant/all-missing columns and zero exact copied columns. No nonfinite numeric values.
- **History cutoffs and bounds:** all 18,183 joined historical creations and approvals precede score time; every historical sequence is below its current sequence. No nonpositive principals, repayment totals below principal, settlement/payment before approval, first payment after settlement, or first due date before approval. Counts obey `closed + open = observed`, observed-payment count never exceeds observed loans, and overdue-unpaid never exceeds unpaid.
- **Counterfactual tests:** deleting future payment/settlement values leaves the cleaned features unchanged; moving current approval to 2099 leaves them unchanged; permuting the target leaves every predictor unchanged; permuting history order leaves features equal to floating tolerance. These directly test the relevant computational mechanisms. They do not authenticate snapshot timing or missing records.
- **History completeness:** observed count equals current sequence minus one for 4,336 rows. Differences are -1 for 26, -2 for 4, -3 for 1, and -5 for 1. Nine customers have no supplied history. The observed-count name and missing historical means are appropriate; zero observed is not an assertion that the borrower never borrowed.
- **Clock boundary:** 756 settlements are at/after application on the supplied clocks, but *all* are less than one hour later: min 0.00056 h, median 0.80292 h, max 0.99444 h. The 664 later first payments are all less than 0.826 h later. Median current approval-minus-creation is 1.00194 h; historical median 1.00222 h. This is substantial evidence of a clock/recording-boundary issue, not evidence of loans remaining open for days after the scored application. No timezone correction was guessed.
- **Demographics/cleaning:** exact-deduplicated profiles have no conflicting customer keys and all scored rows match. Completed age independently recomputes identically, range 21–55. All supplied coordinates pass physical bounds and none is a (0,0) pair. Distant but valid coordinates were not declared impossible merely because this is a Nigerian source. No common proxy strings (`?`, negative sentinel codes, `unknown`, etc.) were found in the five original categorical fields. Missing branch 4,325, employment 657 and education 3,763 remain missing.
- **Conditional missingness diagnostic:** three-fold crossfitted random forests (150 trees, leaf minimum 30) predict demographic missingness from dated history, current loan sequence, application day/hour. A paired diagnostic adds the outcome, never as a shipped feature. Results:

| Field | Missing Bad / Good | Missingness AUC without / with outcome | Log loss without / with outcome |
|---|---:|---:|---:|
| branch | 98.95% / 99.03% | .5967 / .5862 | .06454 / .07741 |
| employment | 20.17% / 13.61% | .7233 / .7309 | .36934 / .36762 |
| education | 87.18% / 85.86% | .8858 / .8839 | .26059 / .26212 |

For employment, the model without outcome underpredicts Bad missingness by 3.55 percentage points and overpredicts Good missingness by 1.20 points. This is modest residual conditional association. It cannot distinguish risk-linked nonresponse at application from post-outcome profile updates; covariates and dated versions are incomplete. It is a **maybe-leak / cannot-verify**, not a cleared timing claim or proof of the recording mechanism. Branch and education show no benefit from adding outcome in this bounded diagnostic. Demographic values themselves still have no as-of timestamps. A repeat profile or data-owner timing statement would settle the timing question; another generic AUC cannot.

Native probes provide context, not timing proof: leak full AUC .67366 over three splits, strongest single field prior first-payment delay .62018, totaldue .60445; no exact train/test feature copies. Nine-fold task RF AUC .68413 versus dummy .5, smallest Bad test support 317. Hidden-group report has no hits, and generated-data report has no flags. The native leak probe tests 31 fields because it does not score the datetime column in its standard single-field sweep; this audit examines `creationdate` too. No native probe establishes proposed-offer/profile availability.

**Column-by-column table**

**Availability conventions:** A = intrinsic application fact; O = recorded current offer, availability at the written application point **unverified**; D = undated customer profile, original as-of availability **unverified**; H = prior creation/approval before application, with event facts separately restricted to dates before application. H is conditional on supplied clock semantics and source completeness, both disclosed. Derived meanings below come from the inspected definition and independently reproduced formulas; raw-field meanings follow the primary codebook.

| Column | Meaning | Known at prediction? | Dtype / cleaning and measured checks | Verdict | Rule |
|---|---|---|---|---|---|
| loannumber | Current loan ordinal | A, prior-borrowing sequence | int64; 2–27; no missing | Fine; count/sequence remains numeric | USE-3; CLEAN-14 |
| creationdate | Application timestamp | A | datetime64; July 1–30, 2017; no missing; current approval excluded | Fine on published clock; real prospective split is separate | USE-3; CLEAN-14 |
| loanamount | Realized principal | O | float64; 10,000–60,000; positive; no missing | Cannot verify that realized equals proposed at application | USE-1/3; LEAK-10; EV-7 |
| totaldue | Contractual repayment total | O | float64; 10,000–68,100; never below principal | Same offer-timing question; not an observed repayment | USE-3/6; LEAK-10/37 |
| termdays | Contract duration | O | int64; 15/30/60/90; no missing | Same offer-timing question; numeric duration correct | USE-3; CLEAN-14 |
| good_bad_flag | Timely settlement class | Outcome, not input | categorical Bad/Good; 952/3,416; no relabeling or missing | Fine target interpretation; precise grace/horizon/arrival unknown | USE-5/8; CLEAN-15/17 |
| bank_account_type | Account kind | D | category; Current/Other/Savings; no missing | Fine encoding; original snapshot timing cannot verify | USE-3; CLEAN-9/14 |
| longitude_gps | GPS longitude | D | float64; -149.034–151.209; physical bounds pass | Fine numeric; as-of/location meaning not established beyond GPS | USE-3; CLEAN-11/14 |
| latitude_gps | GPS latitude | D | float64; -33.869–71.228; bounds pass | Same profile-timing question; no speculative Nigeria clipping | USE-3; CLEAN-11/14 |
| bank_name_clients | Bank name | D | category; 18 levels; no missing | Fine encoding; as-of bank unverified | USE-3; CLEAN-14 |
| bank_branch_clients | Branch location entry | D | category; 39 levels among 43 nonmissing rows; optional missingness retained | Quality question: effectively free-form names/addresses may merit string dtype; timing unverified | CLEAN-14 Should; USE-3 |
| employment_status_clients | Employment kind | D | category; 6 levels, 657 missing; original blanks preserved | Maybe timing leak: modest conditional missingness association; cannot verify collection mechanism | USE-3; LEAK-10; EV-6/7 |
| level_of_education_clients | Education level | D | category; 4 levels, 3,763 missing | Correct nonordinal category; snapshot timing unverified | USE-3; CLEAN-12/14 |
| age_years | Completed age at application | Birthdate intrinsic; reported birthdate accuracy unverified | int64; 21–55; independently reproduced completed birthdays; birthdate dropped | Fine transformation; no assumed adult clipping | CLEAN-3/11/19 |
| was_referred | Referrer recorded | A under source referral semantics | category Yes/No; no missing; raw identity removed | Fine; absence explicitly means not referred in codebook | CLEAN-3/10/14 |
| observed_prior_loan_count | Number of supplied prior issued loans | H | int64 0–26; zero for nine no-history customers | Fine observed-count semantics; incomplete source history documented | CLEAN-2/14/19; LEAK-10 |
| prior_loanamount_mean | Mean historical principal | H | float64; 5,000–36,666.67; nine missing | Fine; independent as-of reconstruction passes | CLEAN-19; LEAK-10 |
| prior_loanamount_max | Max historical principal | H | float64; 5,000–60,000; nine missing | Fine; no all-row statistics | CLEAN-7/19; LEAK-29 |
| prior_totaldue_mean | Mean historical contractual total | H | float64; 5,750–41,252.38; nine missing | Fine historical terms, not actual collected money | CLEAN-19; LEAK-10 |
| prior_termdays_mean | Mean historical duration | H | float64; 15–60; nine missing | Fine numeric average | CLEAN-14/19 |
| prior_loan_sequence_max | Largest observed historical ordinal | H | float64 for missing support; 1–26; nine missing; all < current | Fine numeric sequence; no fabricated history completion | CLEAN-14/19 |
| prior_closed_count | Prior loans settled before application | H event cutoff | int64 0–26; 756 later settlements ignored | Correct masking on supplied clocks | USE-3; LEAK-10 |
| prior_open_count | Supplied prior loans not yet settled on supplied clocks | H event cutoff | int64 0/1; count, not categorical flag; closed+open=observed | Fine conservative clock-based count; all open boundaries <1 h | CLEAN-14; LEAK-7/10 |
| prior_observed_first_payment_count | Prior first payments observed before application | H event cutoff | int64 0–26; ignores 664 later first payments | Correct masking; no future paid status | LEAK-10; CLEAN-14 |
| prior_overdue_first_unpaid_count | Due first installment without observed first payment | H event cutoff; due schedule assumed contractual | int64 0/1; never exceeds unpaid; retains supplied due schedules | Fine conditional on schedules not subsequently revised | USE-3/6; LEAK-10/37 |
| prior_first_payment_delay_mean_days | Mean first-payment minus scheduled-due delay | H paid subset | float64; -31.197–219.195 days; 175 missing | Fine; negative means early payment, not impossible; future actual payments masked | LEAK-7/10; CLEAN-11/19 |
| prior_settled_duration_mean_days | Mean settlement minus historical approval | H settled subset | float64; .02590–250.242 days; 181 missing; no negatives | Fine on supplied clock; future settlement durations masked | LEAK-7/10; CLEAN-19 |
| days_since_first_prior_application | Age of earliest supplied prior application | H | float64; .15578–544.986 days; nine missing | Fine; independent reference matches | CLEAN-19; LEAK-10 |
| days_since_last_prior_application | Age of latest supplied prior application | H | float64; .15578–544.986 days; nine missing | Fine; all strictly positive | CLEAN-19; LEAK-10 |
| days_since_last_observed_settlement | Time since latest pre-application settlement | H settled subset | float64; .0000463–526.633 days; 181 missing | Fine; missing when none yet observed, not backfilled from future | LEAK-10; CLEAN-2/19 |
| prior_first_due_offset_mean_days | Mean scheduled first-due minus current application | H contractual schedule | float64; -513.637–29.546 days; nine missing; 1,574 individual due dates in future | Future schedule is legitimate if fixed at issue; later revision unavailable | USE-6; LEAK-37; CLEAN-19 |
| prior_approval_delay_mean_hours | Mean prior approval minus prior creation | H | float64; 1.00111–37.12167 hours; nine missing; no negative delays | Fine historical quantity; one-hour clock semantics unverified | CLEAN-19/21; LEAK-10 |
| prior_referred_share | Share of supplied prior loans with referrer | H | float64; only 0/1 here, nine missing; proportion retains numeric type | Fine share, not categorical solely because this copy has endpoints | CLEAN-14/19 |

**Ranked findings and mildest remedies**

**1. P3/P4: current realized terms are not established proposed inputs**

**Status: cannot-verify, not a confirmed outcome leak.** USE-1 and USE-3 are Must; LEAK-10 becomes a Must violation if the values did not exist at prediction. The codebook calls `loanamount` a taken value and defines `totaldue` from disbursed capital and charges. It gives no proposed/final comparison or terms timestamp. The audited wording called these proposed terms without evidence; the repaired definition removes that claim. All approvals follow creation (minimum 1.0011 h; maximum 42.876 h), but this does not prove when terms were fixed. Current-approval perturbation tests that approval itself is dropped; it cannot establish offer availability.

**Mildest remedy:** obtain an original terms/version statement establishing that these recorded values were fixed by the stated scoring point. Without it, retain an explicit unresolved conditional-offer task description and avoid claiming a verified application/offer-sizing simulation. For a strict pre-offer application task, dropping the three current-term fields is the smallest definite feature remedy. Moving to post-offer scoring could be a real separate framing, but should not be asserted as source-authenticated merely to excuse these columns (USE-9). `fit="approximate"` documents gaps; it cannot authorize a field once later timing is established. Do not exclude the whole dataset for this repairable question (USE-12).

**2. P4: undated mutable profiles, with employment missingness carrying conditional association**

**Status: maybe a leak / cannot-verify.** Bank, employment, education and GPS profile values have no collection/update timestamps. Exact agreement in duplicate profile copies establishes no conflict, not that the values were collected before the scored applications. The independent conditional experiment is more informative than the native marginal missingness AUC (.533 for employment), but does not isolate a post-outcome recording process: adding outcome improves missingness AUC by .00756 and log loss by .00171. A legitimate risk/nonresponse association remains a competing explanation. No dated repeated-profile evidence exists here to resolve it. Do not describe that modest association alone as proof of a timing leak, and do not mark availability passed.

**Mildest remedy:** seek data-owner snapshot semantics or dated original profiles; retain pre-application values/blank later values if identifiable (LEAK-7/10). Until then, preserve the explicit cannot-verify finding for the curator and note the employment diagnostic. If a conditional investigation identifies downstream fill/update behavior, LEAK-10 requires removing/masking the affected siblings even if score loss is small; approximate fit alone does not fix it. Birthdate-derived age is inherently different from mutable employment/location, although recording error remains possible.

**3. P4/P7: the event masks describe sub-hour boundary uncertainty**

**Status: correct conservative implementation, materially incomplete explanation.** The existing count claims (756 settlements, 664 first payments) are reproduced, but every event falls within one hour after application. This is consistent with a one-hour clock offset or near-simultaneous recording; it does not demonstrate multi-day outstanding borrowing. No documented common timezone permits choosing one interpretation. Counts and date differences remain internally correct under the supplied timestamps.

**Mildest remedy:** keep conservative masking and disclose the measured sub-hour boundary and unavailable clock semantics. Do not add one hour, drop these loans, or relabel historical repayment without an authoritative time basis. If the source later confirms an offset, normalize all affected clocks consistently before recomputing and rechecking (CLEAN-21, LEAK-7). This observation does not invalidate the mask.

**4. P7: branch location encoding deserves a small dtype review**

**Status: quality question under CLEAN-14 (Should), not a Must failure.** `bank_branch_clients` has 39 distinct values among only 43 filled rows. Entries are a mixture of addresses and branch-name text, including punctuation/whitespace variants. The declaration treats this as a fixed category vocabulary; interpreting these supplied values as free-form branch descriptions favors string dtype. No untyped object survives now, so CLEAN-9 is met. It is also defensible to treat real branches as categories; no source canonical branch code list was found.

**Mildest remedy:** explicitly choose string for free-form branch entries or document the real-branch categorical interpretation. Do not geocode, infer branch merges from address resemblance, or drop the column because it is sparse. This lower-ranked uncertainty is no reason to reject the task.

**Boundaries of this recommendation**

The native IID split is explicitly approximate/forced from temporal, and current label-arrival times and grace rules remain missing. This column audit does not independently approve the split workaround, infer mature labels, authenticate organizer files, or authorize inclusion/build/commit/release. Source redistribution terms are already a release note; they do not decide this scientific column verdict (EV-4). No new categorical remapping, arbitrary GPS clipping, history completion, target transformation or timezone repair is recommended. The next owner is the main add-stage agent/mediator, which must reconcile these questions with the other independent evidence and the curator's actual decisions.

</details>

<details><summary>Split audit</summary>

**Independent split audit — SuperLender**

Verdict: **right with notes** for the declared **approximate, ForcedIIDFromTemporal** task. This is a defensible same-July held-out-customer approximation under SPLIT-8. It is **not a verified evaluation of prospective refitting or mature-label deployment**. No mandatory re-split is established by the evidence inspected. Final scientific acceptance remains the curator's decision.

Independent split assessment completed 2026-11-05 on the pinned participant copy.

**Basis and strongest contrary reading**

The real decision is temporal: SuperLender assesses an existing customer's repeat application using prior repayment history. The organizer's [description](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction), read on 2026-11-05, says the drivers are determined “at the point of each application” (lines 35–36). The [data dictionary](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data), also read directly, identifies the scored loan as a repeat loan, `customerid` as a join key, `systemloanid` as the loan identifier, `creationdate` as application creation, and `closeddate` as settlement. It defines Good/Bad by timely settlement, without an exact grace rule, label-arrival date or extraction cutoff. These are source statements; identity of the downloaded participant bytes to organizer bytes remains unverified.

The strongest argument against IID is that 30 dated application days can mechanically support three later windows with at least half the rows in the training side. I ran exactly that counter-test below. Chronology is mechanically recoverable; it is incorrect to say there is no time axis. However, the only labeled applications are from July 1–30, 2017, and current-loan settlement and label-arrival times are absent. Those mechanical windows cannot be verified as trainable at their cutoffs. The release cannot establish SPLIT-9/10-compliant refits plus SPLIT-14's training floor, and SPLIT-8 expressly permits preserving a restricted temporal release in its closest regime. The existing definition correctly keeps the forced tag, approximate fit and non-deployment interpretation.

SPLIT-8 narrows SPLIT-7, SPLIT-14 and USE-10; it does not declare unseen labels known or excuse outcome features. Neither the availability gap nor a quick score proves that a genuinely mature temporal design is impossible. A source-authenticated release with more labeled periods and actual availability timestamps could change the decision. No current loans were relabeled and no history loans were promoted into labeled training examples.

**Ranked findings, rules and mildest remedies**

- **P3/P4, cannot verify: current-label arrival and grace rule.** There are 4,368 distinct labeled loans and customers, 3,416 Good and 952 Bad, with application dates `2017-07-01 00:35:20`–`2017-07-30 21:55:43`. No current-loan outcome timestamp is shipped. In particular, `approveddate + termdays` is a contractual-due diagnostic, not actual label availability. Before July 30 it counts 299 rows; before July 31 it counts 339, against a 2,184-row half-cohort floor. There are only 919 15-day loans, 3,129 30-day, 288 60-day and 32 90-day loans. Even all shortest-term loans are fewer than half, but this is **not** an upper bound on true known outcomes: early full settlement on longer loans and the exact Bad-label rule are unobserved. **Rules:** USE-8, SPLIT-1/6/8/9/10/14, EV-7. **Mildest remedy:** retain the current approximate/forced-IID wording and explicitly retain this uncertainty; recover organizer availability/outcome records and wider labeled history if later available. Do not substitute the proxy for observed maturity or characterize the sensitivity below as a valid deployment score. No new embargo exception is warranted from these measurements.

- **P4, pass with scope note: borrower grouping is unnecessary after aggregation.** Independently checked raw IDs: 4,368/4,368 unique customers/loans among scored rows; every shipped test fold has zero customer overlap with train. Official training/test scored borrowers overlap zero; neither history file contains a currently labeled scored loan; train/test history loan IDs overlap zero; train-history customers overlap official test borrowers zero and test-history customers overlap labeled borrowers zero. There are no repeated scored borrowers that need grouping. The use case is warm history for a new repeat application, not cold-start borrowers without history. Held-out customers in this extract nevertheless have their legitimate pre-application histories supplied. **Rules:** USE-10, SPLIT-3/4/13/23/24/29. **Mildest remedy:** no grouping change; keep one row per scored loan and the factual distinction between being unseen in supervised training and having no borrower history.

- **P4, pass: history is as-of application under the published clocks, with incomplete coverage noted.** All 18,183 supplied train-history loans have creation and approval strictly before their scored application's creation. There are 756 settlements and 664 first payments at/after application; code masks them from realized-event aggregates. Scheduled first-due dates extend beyond application for 1,574 history rows and are legitimate known schedule information, rather than realized payments. History supplies 4,359 of 4,368 customers; nine have none, and observed count equals sequence minus one for 4,336 scored loans. Current approval and raw IDs are dropped. Code inspection plus independent event counts support the strict mask; the supplied feature-invariance artifact corroborates it, but this auditor did not rerun that artifact's intervention test. **Rules:** USE-3/6, LEAK-10/12, SPLIT-9/10/13, EV-7. **Mildest remedy:** keep masks and observed-history wording, do not assert complete histories or repair time zones without source clock evidence. The parent supplied an additional column-audit observation that masked events lie within about one hour of application; that is cross-panel context, not independent proof of a clock offset here.

- **P4, pass: offered-term groups do not establish borrower entities.** The supplied hidden-group run tests ten candidates; no hit/entity-like key, no composite key, no repeated near-copy cluster at similarities 0.8, 0.85 or 0.9. Full cleaned feature duplicates are independently zero. Its largest diagnostic gap is `totaldue`: skill 0.35714 IID versus 0.08189 grouped, gap 0.27525. I independently tested withholding all examples of each `totaldue` value below; the drop reproduces qualitatively. Source semantics establish this as repayment required for an offer, not a borrower identifier. New applications can use already-seen offer values. Withholding a useful offer value tests novel offers; it does not follow the declared existing-customer application use. **Rules:** SPLIT-4/24/29/30, EV-3. **Mildest remedy:** no re-split by offer terms or similarity clusters; preserve the diagnostic and explanation. The score drop alone cannot decide the split.

- **P6, pass: shipped folds are scorable.** Nine shipped folds, each train 2,912 and test 1,456; each test contains 317–318 Bad and 1,138–1,139 Good; each train contains 634–635 Bad. No borrower overlaps across any train/test pair. There is no minority-support reason to invoke Too Small or change the split. **Rules:** SPLIT-14, TP fold-support principle, EV-5. The bounded comparison has nonzero predictive signal in ROC AUC and log loss; it does not establish tuned benchmark performance.

- **P3/P4, cannot verify: offer and demographic snapshot timing.** Source labels current amounts as taken/disbursed value and says the approval decision determines terms; no version timestamps establish that final terms and demographic snapshots were exactly the inputs proposed at application. The current task is explicitly conditional on recorded terms and labels this gap. A split cannot cure feature availability. **Rules:** USE-3/6/8, LEAK-10. **Mildest remedy:** retain the explicit uncertainty and obtain source timing/offer-version documentation; change/drop only a field shown to be unavailable. I do not turn an unverified timing assumption into a proven leak or infer that approximate fit waives LEAK-10.

**Independently run bounded alternatives**

Loaded through maintained `dataset_io.py` (`definition`, `from_definition`), which regenerates the declared split plan without a build. The regenerated frame equals the supplied panel frame in values/order; pandas category storage dtype differs after Parquet roundtrip, so dtype/category-container identity was excluded from that equality assertion. The framework reorders rows; raw lineage was recovered by an asserted unique exact full cleaned row, not assumed to be original CSV position.

All fits use the same 32 declared features; creation time is days since a fixed date, numeric missing values get train-only medians, categories get train-only imputation and one-hot encoding with unknown handling. Untuned LightGBM: 150 trees, 15 leaves, learning rate 0.05, seed 42, two threads. Twelve total fits, no tuning, test-directed feature selection or window optimization. Every Python execution had the required OMP/MKL/OpenBLAS/Polars caps. ROC AUC is for Good; the Bad-class AUC is identical after reversing outcome and probability. Log losses are natural-log units. Fixed-0.5 accuracy exists only as an explicitly labeled diagnostic in the JSON, not as a learned threshold or signal criterion (EV-5).

| Design | Train / test counts | ROC AUC by fold | Log loss by fold | Train-prior dummy log loss |
|---|---|---|---|---|
| Shipped IID, repeat 0 | 2912 / 1456, each | 0.6814, 0.6807, 0.7127 | 0.4903, 0.4928, 0.4724 | 0.5240, 0.5240, 0.5249 |
| Chronology only, **label maturity unverified** | 2233/797; 3030/717; 3747/621 | 0.7258, 0.7185, 0.6978 | 0.4511, 0.4372, 0.5283 | 0.5033, 0.4884, 0.5593 |
| IID with corresponding train/test sizes | same counts as chronology | 0.6983, 0.7101, 0.6564 | 0.4787, 0.4709, 0.5051 | 0.5248, 0.5238, 0.5236 |
| GroupKFold by offer `totaldue`, **not an entity split** | 2728/1640; 3004/1364; 3004/1364 | 0.6313, 0.6813, 0.6224 | 0.6181, 0.4988, 0.4142 | 0.6416, 0.5034, 0.4508 |

Chronology sensitivity uses expanding application-date trains before July 17, July 22 and July 27, testing July 17–21, July 22–26 and July 27–30 respectively. Every train is at least 50%; test Bad counts are 160, 136 and 152. The five/five/four-day windows are a bounded counter-test, not a source-derived refit cadence or seasonal design. Label maturation is **not filtered or assumed resolved**. Mean AUC is 0.7140 versus 0.6883 for matched-size IID and 0.6916 for shipped repeat-0 IID. This does not show a reliable temporal cost or IID equivalence; windows contain different class proportions and calendar compositions, sample sizes are small, and neither valid mature windows nor a complete season can be established. SPLIT-21 forbids choosing the regime/windows from these scores.

Offer-term grouping mean AUC is 0.6450 versus shipped IID 0.6916 with this auditor's model. That difference and the upstream hidden-group skill difference use different procedures and are not interchangeable effect sizes (EV-8). Both show useful offer-value structure; neither establishes an unseen borrower entity.

Retain the current split and its explicit caveats. Add the chronology-only sensitivity as diagnostic evidence if useful, with the maturity warning in the same sentence/table. Recover richer source evidence before offering a verified temporal version; do not speculate groups, infer current labels from history, or promote due-time proxies into observed label-arrival timestamps.

</details>

<details><summary>Domain practitioner</summary>

**Domain-practitioner independent Phase A review**

Independent domain assessment completed 2026-11-05; no model fitting or additional raw-data computation was performed.

**Fit: approximate.** I have a real repeat-loan timely-settlement prediction problem, but this granted-only July cohort, uncertain label rule, unverified application-time profiles/terms and retrospective IID evaluation do not mirror my prospective approval decision (USE-1, USE-3, USE-5, USE-8, USE-10).

**Metric scores the decision: partly.** Accuracy faithfully represents the competition's loan-level error rate; it does not establish the economic value of my approval or pricing policy. Keep the declared source metric unless the curator accepts source- or split-based evidence sufficient to overrule MET-4. My practical preference is a calibrated probability of non-timely settlement assessed with log loss or Brier score, followed by decision evaluation using actual lender costs when available. This is a recommendation for operational use, not a metric replacement.

**My decision and the source's decision**

I am deciding whether to extend another loan to an existing borrower and on what terms when that borrower applies. My question is whether that loan will settle on time. The organizer describes repayment odds informing approval and offer size, price and tenure, and distinguishes repeat-business models using earlier performance. The organizer's evaluation is hard-label misclassification percentage. [Original Zindi description and evaluation](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction).

The source schema describes the performance row as a repeat loan already taken. It calls `loanamount` “Loan value taken” and defines `totaldue` using disbursed capital plus interest and fees. The target distinguishes settlement on time from failure to do so. Demographics have no stated snapshot date. Prior-loan settlement and first-payment dates are separate events, and first-due dates describe scheduled installments for longer loans. These are the source facts; they do not establish that issued terms were a proposed offer at application. [Organizer data dictionary](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data).

The 2022 rerun independently specifies the same hard-label error metric. Its generic statement about competitions that require probabilities does not convert this particular task into probability scoring. [Rerun evaluation and rules](https://zindi.world/competitions/loan-default-prediction-challenge).

My domain judgments below are implications of those facts and the inspected local package, not evidence that SuperLender followed an undocumented underwriting process.

**Inputs I can actually have at the prediction point**

| Input family | My assessment at application |
|---|---|
| Application time, repeat-loan sequence, referral status | Plausible inputs at application. The raw identifiers are appropriately excluded from predictors; referral presence is a reasonable representation. I cannot infer how a referral was recorded beyond the supplied data. |
| Current `loanamount`, `totaldue`, `termdays` | The actual contract is observable by issuance. I could know an explicit proposed contract before choosing to lend, but the released issued contract is not proof that this proposal existed at application or was unchanged. Describing these columns as proposed terms is an unsupported upgrade. Dropping current approval time alone does not resolve it (USE-3, USE-6). |
| Age | Birth date is plausibly established at onboarding; converting it to completed age at application is sensible. The source supplies no verification/collection timestamp, so even here I distinguish plausibility from proof. |
| GPS, employment, education, bank/account/branch | Plausible application/onboarding inputs. Location, job and bank details can change. The joined snapshot has no effective time, so an eventual profile may differ from what I knew then. Combining unlabeled demographic partitions fixes coverage, not this timing gap (USE-3, USE-8). |
| Earlier loan amounts, contractual terms, approval delays and issued-loan counts | Legitimate history once the earlier loan was issued. A scheduled future installment date is known from its existing contract and is not an outcome leak merely because it lies after my current decision (USE-6, USE-10). |
| Earlier observed payments and closures | Usable only if those events had occurred before my decision. The implementation masks later events while preserving open-loan and overdue-first-payment states; this matches what I would see more closely than assuming every prior loan is already settled (USE-3, USE-12). |
| History completeness and live exposure | The packet reports nine borrowers without supplied earlier rows despite repeat-loan sequence and only 4,336/4,368 exact sequence/count matches. Zero observed history does not mean no borrowing history. I would want a completeness indicator and my true outstanding exposure in operations, but this release does not support inventing either. |

For a live approval decision I would also want verified ability-to-pay information and current obligations. Neither income/cash flow nor a full repayment ledger is supplied. These are useful deployment improvements, not a claim that every lender always collects a particular field, and not a reason by themselves to reject the published task. More immediately, an offer decision requires identifying the candidate terms being evaluated; these issued-loan rows cannot tell me what would happen under different amounts/prices/tenures. Treating the model as an optimizer over hypothetical offers would add an unsupported causal interpretation.

**Target, row and test population**

The row is one labeled loan, and the inspected raw profile confirms 4,368 distinct borrowers and loan IDs. This matches the unit I act on. A borrower is still an existing customer with legitimate earlier history; uniqueness of the scored row does not make this new-customer lending (USE-10, USE-11).

I act on repayment risk, and timely settlement is a useful component. I must not translate `Bad` into permanent default, principal loss, or a standardized days-past-due event. The flag does not identify recovery amount, duration of lateness, or whether a later payment settled the debt. The definition correctly names the absent grace rule, extraction cutoff and label-arrival dates. USE-5/USE-8 permit an explicitly approximate label with this gap; they do not let me fabricate a conventional default horizon.

The supplied raw profile has 3,416 Good and 952 Bad outcomes, all applications in July 1–30, 2017. Terms are 15, 30, 60 or 90 days; their distribution is 919/3,129/288/32. The target is consequently a contract-specific timely-settlement event, not a common 30-day future horizon. These measured facts come from `raw-profile.json`.

The test folds hold random customers from this same cohort. My real next applications occur later, after portfolio policy and borrower circumstances can change. All observed loans were granted; I lack outcomes for rejected applications. I could use this task as evidence of association in the lender's previously accepted repeat-borrower population. I could not use its IID score as validated performance on next month's full applicant pool, a new lender, first loans, or applicants newly approved by a changed policy. A change of policy can change who is observed. No rejected outcomes should be reconstructed from this release.

The definition's due-date proxy and 299 loans contractually due before the July 30 cutoff explain why mature-label temporal windows are not verified. They are not measured label-arrival times, and they do not prove there was no possible early settled training population. I leave the formal SPLIT-8 decision to the split audit; from my role, the resulting IID test remains approximate (USE-8), not prospective deployment evidence.

**Ranked gaps and changes I would request**

- **Establish the stage and the current terms before claiming application-time offer prediction.** Replace unsupported “proposed terms” language with “recorded issued-loan terms; application-time availability unverified.” Seek a source statement or timestamped proposal/contract history. If the intended application-stage task is retained and availability cannot be established, assess a version excluding `loanamount`, `totaldue` and `termdays`; retain legitimate historical contract summaries. If a genuine later decision is proposed instead, name its actor, action and source evidence explicitly. Do not silently move the task to post-approval risk monitoring to excuse the inputs (USE-1/3/4/6/9/12). Approximate fit does not establish the availability of a field that is actually post-decision; if confirmed post-decision, fix it.

- **Get the exact timely-settlement label rule and outcome availability.** Ask for contractual final due date, grace convention, observation cutoff and when the flag became knowable. Keep the source flag unchanged while these are unavailable. Without loss/recovery data, do not advertise economic default or expected loss prediction (USE-5, USE-8).

- **Obtain application-time profiles or qualify mutable inputs explicitly.** An effective-date or collection-date record is preferable. The union of demographic tables is a defensible coverage repair because there are no target labels or fitted statistics in those fields, but it cannot verify what profile was known when. If a field is confirmed to have been updated later, remove or reconstruct it. Do not declare leakage absent merely because no single feature is very predictive (USE-3, USE-6, USE-12).

- **Validate on later applications with mature labels and preserve the granted-cohort restriction.** A longer, dated labeled release is the meaningful repair. Do not create a temporal success claim from clock-only unlabeled test dates, or describe same-July IID holdouts as later applicants. The current one-month cohort is still a real approximate prediction task, not fit none (USE-8, USE-10).

- **Keep history availability and sampling limits visible.** Preserve as-of event masking and counts of open loans. Call empty history “no supplied prior rows,” and do not imply a complete current liability balance. Seek a complete event ledger only as a future improvement. Source performance on granted loans cannot establish gains from accepting previously rejected borrowers.

- **Separate competition scoring from the lender's deployment objective.** Keep accuracy with its exact error-rate identity and training-only threshold selection. Supplement with proper probability scoring, calibration and discrimination; evaluate actual economic decisions only when real costs/outcomes exist. No invented cost ratio, 0.5 decision threshold, top-k budget, or metric override (MET-1/2/4/6/7/8/9/11).

**Would I use it, and what would I trust?**

I would use it to compare repeat-borrower prediction methods under its stated retrospective restrictions and to investigate whether historic repayment behavior adds signal. I would not approve deployment or promise profit gains from this panel. The native task probes report mean random-forest AUC 0.6841 and log loss 0.4867 over nine IID evaluations, against dummy AUC 0.5 and log loss 0.5243. These numbers show modest predictive association on this task; they are not the declared accuracy results and do not resolve chronology, costs or availability. The leak probes report no exact feature-copy leakage, and the recorded invariance test confirms masking of future payments/closures. These checks increase confidence in implementation but cannot date a demographic snapshot or turn final terms into a proposal.

I would trust the model more after the first four changes above, source-byte authentication, and calibration/decision evaluation on a later representative cohort. The source-copy issue is also a provenance limitation; pinning a participant commit proves which copy was used, not organizer equivalence. Source permission remains a separate release question and is not settled by this domain judgment.

**Metric judgment in detail**

The evaluation unit is correct: one decision per loan, with one loan per customer here (MET-1/2). Accuracy is exactly one minus the source error proportion, so the supplied `Metric.source` declaration is a valid direction-reversed identity under MET-11. Neither classes nor sampling were deliberately rebalanced. Accuracy weights a Bad loan accepted as Good equally to a Good loan rejected as Bad, and gives every loan the same weight despite differing amounts. The majority-only accuracy of about 78.21% is a useful reference, not evidence by itself that error scoring is gamed or invalid.

For real lending I prefer a calibrated probability of Bad rather than a bare class, because I can use it at different approval thresholds when the lender supplies real margins, loss severity and operating constraints. Log loss or Brier score would assess this probability; ROC AUC would assess discrimination but not calibration. The Bad flag alone does not furnish principal losses, recoveries, funding costs or opportunity costs, so this packet cannot establish a defensible economic cost matrix (MET-7). Class imbalance alone does not justify average precision, and no top-k operational capacity is documented (MET-9).

However, MET-6's paper-only rejection of unsupported hard-label thresholds does not overrule a competition. MET-4 explicitly gives this hard-label challenge its source metric and lets the method select a threshold on training data. The official source fixes no probability threshold of 0.5. A practitioner preference for probabilities, or the availability of AUC/log-loss diagnostics, is not the measured/source-based counter-evidence required for a metric override. Preserve accuracy and clearly label probability diagnostics; propose a change for curator review only if qualifying evidence emerges. Metric shortcomings are P6; they do not require dataset exclusion under the principles.

Counts and probe results are attributed to the qualification measurements; this role independently assessed the task and primary source descriptions without fitting models.

</details>

<details><summary>Blind review</summary>

**Include with changes:** this is a plausible, nontrivial small tabular benchmark for repeat-loan repayment risk, but I would require documented feature cutoffs, borrower independence, source lineage, and explicit outcome semantics before admitting this exact version.

I inspected only `task.md` and `data.parquet` in the supplied clean room, plus public webpages. General workspace instructions were inherited in conversation; I did not open surrounding project files or use repository-specific evidence.

The operational task is credible. A lender scores an existing customer’s next loan, conditional on the available loan terms, to inform lending decisions. However, the source defines “Bad” as failing to settle **on time**, which also includes delinquency followed by eventual repayment. Calling the target permanent default would overstate its meaning. The source also distinguishes application timing from approval and describes the loan fields and historical payment dates. [Zindi data dictionary](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction/data)

**Independent measurements**

- 4,368 rows, 32 predictors: 25 numeric, six categorical, one datetime.
- Target: 3,416 Good and 952 Bad; adverse-outcome prevalence **21.79%**.
- Current applications span **1–30 July 2017**. Loan terms are 15, 30, 60, or 90 days.
- No exact duplicate rows, duplicate predictor rows, or duplicates after removing application time. All observed demographic profiles are distinct.
- No infinite numeric values, negative elapsed-time features, or inverted first/last prior-application intervals.
- Historical counts satisfy `closed + open = observed prior loans` for every row. Observed first payments never exceed observed loans, and unpaid-overdue counts never exceed open counts.

I ran untuned models using three repeats of stratified three-fold cross-validation, seed 4621. All preprocessing for logistic regression was fitted within folds. “Bad” was the positive class.

| Model / inputs | ROC AUC | Average precision | Log loss | Accuracy |
|---|---:|---:|---:|---:|
| Constant prevalence | 0.500 | 0.218 | 0.524 | 0.782 |
| Regularized logistic regression, all inputs | 0.676 | 0.403 | 0.491 | 0.793 |
| LightGBM, all inputs | **0.701** | **0.429** | **0.480** | **0.794** |
| LightGBM, no historical summaries | 0.632 | 0.332 | 0.509 | 0.781 |
| LightGBM, historical summaries only | 0.663 | 0.396 | 0.499 | 0.789 |
| LightGBM, no current amount/due/term | 0.690 | 0.419 | 0.485 | 0.793 |
| LightGBM, no date/GPS/branch | 0.692 | 0.419 | 0.486 | 0.792 |

LightGBM used 200 trees, 15 leaves, learning rate 0.04, minimum leaf size 30, and L2 regularization 2. Its fold standard deviation was 0.020 AUC; overlapping repeated folds do **not** provide nine independent estimates.

The best single-feature depth-two tree reached **0.639 AUC**, using prior first-payment delay. A permuted-label check produced **0.513 AUC**. These results show meaningful but modest signal, without an obvious trivial target proxy. The 0.5-threshold balanced accuracy was only **0.584**; accuracy alone conceals weak adverse-outcome detection.

**Ranked concerns and remedies**

- **Historical repayment inputs lack an auditable availability cutoff.** Prior settlement duration, first-payment delay, and time since settlement are legitimate only when the underlying events were observed before scoring. Their names and plausible values do not prove that condition. There are 756 rows with open prior loans, so censoring matters concretely.
   **Remedy:** document and verify row-level filtering against the prediction timestamp; mask future repayments and settlements before aggregation. Define every denominator and missing-value rule. Positive future due-date offsets—584 rows—can be legitimate scheduled information and should not automatically be treated as leakage.
- **IID borrower independence is not established.** Borrower and loan identifiers have been removed. Exact-profile uniqueness is encouraging but cannot establish that customers are unique, that loans do not recur across folds, or that historical loans do not overlap evaluation loans. Forty-one rows share exact GPS pairs; this is insufficient to infer borrower identity.
   **Remedy:** audit original identifiers and joins outside the predictive matrix. If customers recur, group their rows or justify the specific repeat-customer evaluation. Publish stable split assignments and preserve an audit mapping.
- **The prediction moment and target horizon need a concrete contract.** Current amount, repayment obligation, and tenure may reflect an existing lender’s pricing and approval policy. They are honest inputs for scoring a proposed loan with known terms, but their availability for an earlier application decision is unverified. Only issued repeat loans are observed, so performance cannot establish lending-policy value for rejected applicants.
   **Remedy:** state “predict on-time settlement of an issued/proposed repeat loan, conditional on recorded terms,” fix the timestamp, and document label maturity, grace periods, and observation cutoff.
- **One month supports a narrow retrospective IID benchmark, not prospective validation.** A July-21 chronological diagnostic yielded **0.696 AUC** on 1,486 later rows, versus 2,882 earlier rows. This was deliberately unpurged: many earlier loans would not yet have matured when later applications arrived. It therefore does **not** validate deployment performance.
   **Remedy:** retain the IID claim narrowly, or obtain more months and use time splits with label-availability gaps. Three repeats do not increase the underlying sample size.
- **Source copies and applicable redistribution terms need resolution.** Both linked Zindi competitions describe the same SuperLender problem and expose matching source-table names and displayed sizes. A public GitHub project also contains a `raw_data` directory and model template. These establish substantial prior exposure, not exact prepared-file identity. [Public project](https://github.com/MeganBeckett/zindi-loan-prediction)
   Importantly, the Nigeria page restricts redistribution, while the Tanzania competition expressly permits reuse under CC BY-SA 4.0.
   **Remedy:** identify the exact acquisition route, hashes, attribution, applicable terms, and relationship between releases. Treat these aliases as one dataset family when checking benchmark overlap. [Nigeria rules](https://zindi.world/competitions/data-science-nigeria-challenge-1-loan-default-prediction), [Tanzania rules](https://zindi.world/competitions/loan-default-prediction-challenge)
- **Sparse and questionable inputs need ordinary preparation.** Branch is **99.02% missing**: only 43 observed values across 39 categories. Education is **86.15% missing**, employment **15.04%**. Nine records lack observed history; historical settlement features are missing in 181. Thirty-eight GPS points fall outside a broad Nigeria bounding box, including clearly overseas coordinates. Observed historical counts differ from `loannumber − 1` in 32 rows, which could reflect incomplete history or intentional time filtering.
   **Remedy:** document these mechanisms, drop or justify branch, handle missingness within folds, retain categories as nominal, and investigate suspect coordinates without assuming all nonlocal points are errors. Explain count discrepancies rather than silently imputing complete history.

**What remains unverified:** original joins, unique borrowers, source-file identity, raw-event timing, target reconstruction and maturity, demographic snapshot timing, any prior imputation, and overlap with existing benchmark collections. The supplied task file also lacks evaluation metric, split seeds, and executable split definitions.

</details>

<details><summary>Precedent check</summary>

**SuperLender independent precedent check — full add-dataset Phase A**

Observed: 2026-11-05 UTC. This is the required evidence-stage precedent check of the provisional definition, not a final inclusion decision or merely a check of the curator's earlier authorization.

**Recommendation:** the provisional ForcedIIDFromTemporal/approximate evaluation, timely-settlement target, source error represented by accuracy, and dated history aggregation follow the relevant rules and precedents. No actual conflicting Myunghwan decision, new maturity exception, or third exception is established. Application-time availability of the recorded current terms and mutable demographic profiles remains cannot-verify. Do not convert the provisional treatment into a finding that those inputs were available, and do not use approximate fit to excuse a field shown to be later. The unqualified word “proposed” needs qualification because the source describes realized terms; that factual wording issue is not evidence of a curator deciding a like case differently.

Validity: USE-1/5/8 and SPLIT-8 support a real but approximate task; USE-3 and LEAK-10 remain open on current terms/profile timing. SPLIT-9/10 have not been certified for chronological refits. PROV-1/2/8/9 support transparent participant-copy qualification, with organizer equivalence unverified. Value: MET-4/11 support source accuracy by identity; supplied probes do not establish triviality or Too Small. Quality: CLEAN-14/19 support semantic types and one-row history aggregates; branch typing is a minor judgment. For the curator: the remaining questions are factual availability/provenance and acceptance judgments, not already-granted exceptions.

The precedent comparison began with the decision register, candidate and sibling records, and applicable rules; other reports were consulted afterward. Numerical findings are attributed to the independent audits.

**Register and attribution findings**

The supplied register contains 2,271 entries. Its flags are search leads, not findings. There is exactly one Myunghwan CC: SuperLender, 2026-11-04, which authorizes add-dataset qualification, actual-data checks/probes and the independent panel. It expressly does not authorize final inclusion, build, commit, a timing exception or a final split.

The register's opposite-outcome flags concern few-minority, one-feature and trivial mechanisms in other cases; the drift flag is Lennart's scaling-over-all-rows sequence, subsequently governed by the LEAK-30 amendment. Neither establishes a conflict here. Its exception-to-Must flags require reading the actual exception text: Alfa and Lending Club explicitly record exceptions to SPLIT-10, while citing SPLIT-9/14 in their rationale. A parser finding those IDs is not a new exception to every cited Must. No Myunghwan pair exists from which to infer same-curator drift. No third exception is created by applying amended SPLIT-8 to this one-cohort release.

**Decision-by-decision comparison**

**1. Continue qualification without treating Yes metadata as final acceptance**

**Consistent.** The sole current curator instruction is the November 4 qualification CC above. The November 3 screening is an AI recommendation; older AI-filled material is explicitly superseded. Principles' precedence makes later measured evidence supersede screening inferences, but gives the human acceptance decision to the curator. An older direct-fit/temporal claim, or the present `suggestion: Yes`, cannot be converted into Myunghwan's acceptance of the measured version. No reflection question is needed: there are no conflicting human calls.

**2. Keep timely settlement as the target and disclose the unknown grace/arrival rule**

**Consistent.** USE-5/8 permit an imperfectly documented source label with approximate fit when the actual quantity is not refuted. This copy preserves all 4,368 source-copy labels, Good 3,416 and Bad 952. Bad means not settled on time, not proven permanent loss or a newly invented days-past-due definition. Closest cases are the [USE-5/8 Cases](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-use_case.md): diabetes_3 and differentiated_thyroid_cancer_recurrence (Lennart, 2026-10-21), kept approximate for an undocumented quantity/recurrence breadth, and Alfa's unstated label horizon (2026-10-21). In contrast, corporate_credit_rating was retired after checkable labels proved to be the wrong issuer quantity (2026-10-16). No corresponding wrong-quantity finding exists here. Do not reconstruct labels from historical closure or invent a grace period merely to improve windows.

**3. Use ForcedIIDFromTemporal with approximate fit for the one labeled month**

**Consistent as a provisional SPLIT-8 application; chronological validity cannot be certified.** The relevant rule is the amended SPLIT-8 (Must, narrowing SPLIT-7/14 and USE-10), not an assertion that missing arrival timestamps turn lending naturally IID. This release has one labeled July cohort, 4,368 loans with application dates July 1–30, and no current-loan settlement/label-arrival dates. The provided test performance file has no labels and no calendar dates to supply wider labeled windows.

Closest decided precedents: [mobile_churn](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/mobile_churn.md), CC 2026-10-21, one stock month/undated snapshot, ForcedIIDFromTemporal; [distribution_transformers_at_cauca_department](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/distribution_transformers_at_cauca_department.md), CC 2026-10-21, too few yearly periods, keep one year IID with the forced tag; and [account_debt_south_africa](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/account_debt_south_africa.md), CC 2026-10-12, one extract standing in for a forecast. The [splits Cases](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-splits.md) also distinguish stacked recurrent entities (NBA/Open University, 2026-10-21), which use forced grouped splits. SuperLender has one scored row per borrower, not repeated scored rows stacked over cohort months, so that forced-grouped rationale does not apply.

The source's real application remains future repeat lending. IID estimates held-out loans/customers within this July cohort. This is a disclosed approximation, not a new use case invented to make direct fit. This follows USE-8/9's warning that random undated credit applications stay approximate. There is no validated temporal cost comparison here: SPLIT-8 asks for it where valid windows exist, not a score manufactured with unmatured labels. Recover arrival times and broader cohorts if later available, then revisit the regime.

**4. Do not manufacture a maturity exemption from Alfa/Lending Club**

**Consistent; the differences are substantive, not a departure needing an exception.** [Alfa](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/alfa_battle_2_0_task_2.md), 2026-10-21 Lennart exception, has a reconstructed multi-month temporal axis, a possible year-long delay, training floors 13–27% for a 12-month gap or 35–53% for six months, and removal of the test-window clients' products to address a measured shortcut. [Lending Club](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/lending_club.md), 2026-10-21 Lennart exception, has multiple issue years with finished-loan selection repaired and a 36-month gap leaving 5–9% (12-month gap 33–46%). Those are expressly SPLIT-10 Should exceptions serving SPLIT-14, with the principles' measurable-shortcut boundary for SPLIT-9. They are not universal permission to train on unarrived outcomes.

Here, no multi-window mature-label temporal protocol is established and no new human exception exists. The proposed IID stand-in follows SPLIT-8. Approval plus term is a contractual due proxy, not measured label arrival: 299 before July 30 midnight, or 339 before July 31 midnight; all 919 shortest-term loans remain below the 2,184-row half-cohort floor. Early settlement and grace/recording delays are unknown, so those figures cannot prove that only 299 labels had arrived or that temporal deployment is mathematically impossible. The current definition correctly disclaims that stronger conclusion. An unpurged July-21 diagnostic in the blind report is explicitly invalid as prospective validation and supplies no counter-precedent.

[seismic_bumps](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-splits.md), 2026-09-30, is also distinguished: it is a nonstationary sequence with tiny minority support per valid window, for which SPLIT-16/TP-9 forbid IID fallback to hide Too Small. This is a one-cohort/missing-arrival limitation with 317–318 Bad loans per declared IID fold, not that demonstrated low-positive-window mechanism.

**5. Treat repeat-borrower history as known-entity information, without inventing cold start**

**Consistent.** USE-10/LEAK-34 protect legitimate pre-prediction history; SPLIT-3 chooses the regime from the use case. The closest finance sibling is [african_credit_scoring_challenge](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/african_credit_scoring_challenge.md), 2026-10-07 assessment, where repeat customers are history known at disbursement rather than a reason for grouping. Corporate credit rating's USE-10 case likewise treats earlier ratings as legitimate known-entity input. In_vehicle_coupon_recommendation is the contrasting true cold-start task, grouped by respondent ([USE Cases](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-use_case.md)).

“Held-out customers” here means no customer's scored label is shared across a fold. It does not mean a new-to-lender borrower without a supplied history. `raw-profile.json` records 4,368 unique scored customer IDs and loan IDs; the claim audit independently checks zero customer and exact-copy intersection per fold. Amounts, branch names and the 41 shared GPS pairs do not establish repeated borrower identity. Grouping on totaldue or GPS from a probe gap would conflict with SPLIT-4/24/30. Keep actual lineage for review; do not call raw history a forbidden train/test outcome overlap simply because it belongs to a held-out scored borrower.

**6. Aggregate prior loans once per score row; mask payment and closure by their own event time**

**Consistent.** CLEAN-19 permits normal transaction/history aggregation; Alfa's 2026-10-13/21 decisions are the closest construction precedent. CLEAN-20 forbids copying competition exploits, and LEAK-7/10 favor the smallest causal repair. This definition filters historical creation/approval before score time, then masks first repayment and closure separately before forming event-dependent aggregates. It does not require the whole loan to have closed before using its previously issued terms or an already-observed payment. Scheduled due dates in the future are different from future realized payments.

The supplied invariance artifact and independent column crosscheck support this implementation, including 756 masked closures and 664 first payments, all 18 historical predictors independently reconstructed, no current/history loan-ID overlap, and one output per scored loan. The column auditor finds all those “later” events within one hour, so describe them as recorded-clock boundary uncertainty rather than proved multi-day outstanding borrowing. No guessed one-hour repair is warranted. Nine absent supplied histories and 32 sequence-count discrepancies require “observed” counts, missing means and no claim of completeness; the current definition does that.

**7. Combine unlabeled demographic partitions without fitting statistics across scored rows**

**Consistent for the join; timing remains separate.** LEAK-29/CLEAN-7 prohibit our fitted all-row feature values, not deterministic entity-key lookup. [Home Credit](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/home_credit_default_risk.md), CC 2026-10-19, dropped a pooled organization median and mean fill while preserving legitimate source information; the relevant distinction is computation, not whether a file's name says test. Here `join-qualification.json` records 5,833 profile rows minus 15 exact copies = 5,818 unique customer profiles, zero conflicting keys and 1,099 labeled borrowers recovered from testdemographics. No test targets or target encodings are used. A one-to-many history join before row splitting would repeat scored loans, but the current aggregation/unique-key assertions avoid that. Deterministic recovery of these profiles does not establish their historical availability.

**8. Keep mutable profile fields as explicitly unverified pending a factual timing decision**

**Consistent as an unresolved qualification finding; no final clean-timing verdict is supported.** Closest adverse precedents are [Cauca transformers](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/distribution_transformers_at_cauca_department.md), CC 2026-10-21, where changed post-burn inventory fields stayed dropped; [African credit](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/african_credit_scoring_challenge.md), 2026-10-20, where an undatable pull-time lender count was dropped with changing outcome association; and [kick](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/kick.md), CC 2026-10-22, where conditional missingness tests caused WheelType and the related fields to be dropped. LEAK-10 is Must when later or outcome-dependent values are established; modest score loss never rescues them. Zillow/Melbourne's 2026-10-21 [LEAK-7/10 Cases](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-leak_checks.md) show partial blanking when later-looked-up rows can be isolated.

The distinction here is the evidence of the mechanism, not that demographic fields receive an automatic exception. Their collection/update times are absent; identical duplicate copies do not show they were unchanged since application. The column audit's employment missingness diagnostic gives a modest residual association (AUC .7233 to .7309 after adding the outcome; log loss improvement .00171), with risk-linked nonresponse still a competing explanation and no identified post-outcome process. This cannot be declared either proved leakage or cleared availability. Report cannot-verify and the actual diagnostic; seek owner snapshot semantics or dated profiles, then retain as-of values/blank later values/drop affected siblings if the mechanism is established.

LEAK-38's host-competition treatment is explicitly for anonymized untestable fields. These named mutable profiles do not inherit Homesite's dataset-specific keep (2026-10-01/21). Nor does USE-8's kept-leak fit amendment authorize a new leak: approximate fit here has genuine separate cohort/label/split gaps. On present evidence there is no real like-case opposite outcome to trigger a consistency reflection; a future proposal to keep confirmed later profiles would require the Must to be fixed, not an exception under approximate fit.

**9. Current recorded loan terms are not authenticated proposed inputs**

**Consistent as an explicit cannot-verify; the asserted “proposed” wording requires qualification.** The closest positive precedent is [Brazilian ecommerce](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/brazilian_ecommerce.md), CC 2026-10-15, keeping the delivery date promised at checkout because it is fixed and known then (USE-6/LEAK-37). The contrast is the measured post-disbursement repay amounts in African credit, which grow with penalties and were dropped (2026-10-07). Contractual total due is not automatically actual collections; neither example alone establishes when SuperLender fixed these terms.

The source descriptions reproduced by both auditors concern amounts taken/disbursed and repayment obligations. All current approvals follow creation, but that timestamps approval, not proposed/final offer versions. No proposed-vs-final comparison is present. Therefore retaining the three recorded term columns provisionally with an explicit limitation is not a demonstrated opposite decision to Olist or African credit; calling their “proposed” status source-proven would outrun the evidence. State the conditional recorded-term framing without asserting a version history. Seek owner evidence; if strict pre-offer prediction is required without it, dropping current loanamount/totaldue/termdays is the smallest definite feature remedy. A source-described later pre-outcome decision could be considered, but USE-9 forbids relabeling a task as direct solely to excuse a gap. No final timing exception has been granted.

**10. Pin the participant copy while retaining the original source/year and authenticity gap**

**Consistent for bounded qualification, not proof of organizer identity.** PROV-8/9 distinguish original publication from download location. The definition names the 2018 Zindi/DSN challenge and the Megan Beckett copy at commit `16379560b10bda88b957c180d4767a37a61454a3`, with organizer-byte equality explicitly unverified in `raw-manifest.json`. [Airfoil's 2026-10-20 source/year Cases](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-provenance.md) illustrate the general original-versus-copy distinction. The stronger caution is [hr_analytics](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/hr_analytics.md), CC 2026-10-14: the Kaggle copy had 2,623 manufactured positive labels and was repaired from the hackathon source. It shows why schema/narrative and Git hashes do not authenticate organizer labels.

Unlike hr_analytics, no damage or manufactured label mechanism has been found on this copy, so PROV-13 does not justify an invented repair or automatic exclusion. PROV-2's amended case-by-case treatment of plausible but incomplete provenance (2026-10-21 mobile_churn/tour_travels) supports explicitly bounded consideration, not silent upgrade of authenticity. Organizer hashes/bytes are the settling evidence if accessible. Keep this gap for curator assessment.

**11. Treat aliases as one source family; do not infer duplicates from other lenders**

**Consistent.** My search of the same checkout's records for SuperLender and the two canonical challenge slugs returns only this record. The record's 2018 original and 2022 rerun are aliases/source-history leads, not two independently qualifying datasets. PROV-4/5/6 require confirmed shared origin; the Cases' colleges check (2026-10-12) confirms how strong duplicate claims must be. The [Zimnat](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/zimnat_loan_default_predictio.md), [African credit](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/african_credit_scoring_challenge.md) and [LT vehicle](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/lt_vehicle_loan_default_prediction.md) records have other lender/platform origins. Shared finance target/name is not confirmed common data. Their AI screening text is not equivalent to accepted precedent. This bounded record search is not an exhaustive external overlap certification or a new claim that all rerun bytes are identical.

**12. Preserve source hard-label error as accuracy by identity**

**Consistent.** MET-4 applies to a competition's hard-label leaderboard choice; MET-6's criticism of unmotivated paper thresholds does not override it. [African credit](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/african_credit_scoring_challenge.md), source F1 accepted under the 2026-10-21 metric decision, is the closest hard-label competition case. [Porto Seguro](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/porto_seguro.md), 2026-10-21, is the closest MET-11 identity case: binary normalized Gini is declared as ROC AUC with its identity retained. Error = 1 − accuracy is equally exact with reversed optimization direction. Same labels, balance and per-loan unit are preserved here; no missing scoring metadata is needed.

No source-fixed 0.5 probability threshold has been demonstrated. Methods choose any threshold only on training data. ROC AUC/log loss are appropriate learnability diagnostics under EV-5, without replacing source accuracy. The claim audit's small bounded accuracy gain (.00565 over constant Good, not tuned performance) is not evidence that the source metric is biased/wrong, nor a Trivial/no-signal finding. Older October 22 AI suggestions to overrule error and assume 0.5 were superseded, not a prior Myunghwan decision now being reversed.

**13. Preserve a modest real task and ordinary semantic cleaning**

**Consistent.** Supplied task results show no native flags and at least 317 Bad test rows; they do not resemble parkinsons' 2–3 healthy units per fold or Alvin's tiny rare classes carrying half the loss (TP-5/8 Cases, 2026-10-05/12). Forest_fires/HR analytics show that a modest but real signal is not itself exclusion (TP-1/2/3). This does not clear validity questions: P4 precedes P6, and a clean probe never proves timing.

CLEAN-11/14/19 support completed age, real missingness, nominal flags, numeric counts/durations/shares even when endpoints 0/1 occur, and physically valid unusual coordinates without arbitrary Nigeria clipping. Home Credit's 2026-10-21 semantic typing revision is the closest count-versus-flag precedent. Branch's 39 observed values in 43 filled rows may be real branch categories or free-form address text; its categorical declaration is a lower-ranked CLEAN-14 judgment, not untyped-object failure or a demonstrated like-case reversal. Document the interpretation or use string when free-form semantics prevail; sparsity or a quick model score alone is no reason to drop it.

**14. Keep redistribution terms separate from the scientific verdict**

**Consistent.** EV-4 and SEL-1 distinguish release restrictions from an objection to ML use. [EV-4 Cases](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/.claude/skills/knowledge-evidence.md), 2026-09-23 and 2026-10-21 Lennart, explicitly include lucas_topsoil, African credit and other Zindi data; noncommercial/no-redistribution terms are release checklist matters, not a No/marker/scientific issue. The [Alfa record](https://github.com/TabArena/data-foundry/blob/1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b/curation/records/alfa_battle_2_0_task_2.md), 2026-10-07, also notes forbidden data passing separately from scientific qualification. Keeping the differing original/rerun terms visible before redistribution follows that treatment. The blind report's call to resolve terms is appropriate for release, not a precedent-based reason to exclude this scientific task. No transfer or release permission is inferred here.

**Departures, reflection prompts and handoff**

No current curator departure without a distinguishing fact is established. There is therefore no filled consistency prompt asking Myunghwan to explain a decision he has not made. The one-cohort differences from mature-label multi-year lending are stated above as facts applying the amended rule, not as new exceptions. Likewise, unresolved snapshot/offer timing is an evidence gap, not permission to import Homesite's keep, Alfa's gap exception, or Lennart's acceptance.

The two necessary boundaries for the debate are concrete: (1) “proposed terms” is not authenticated and should be qualified as recorded terms/conditional availability; (2) explicit uncertainty cannot become a passed application-time check. If evidence establishes later/outcome-dependent values, LEAK-10 requires the mildest repair. Keeping a confirmed violation without repair would be **not reasonable under the ranking**, because no lower-ranked value/quality argument or Should exception overrides that Must. That is a conditional rule boundary, not an accusation that the violation is already proven.

</details>

<details><summary>Advocate</summary>

**Advocate opening — SuperLender**

**Position: keep with narrow wording repairs and curator disposition of cannot-verify inputs.** Unconditional unchanged acceptance is unsupported. Evidence below is attributed to the six independent reports.

- **A real target survives availability objections.** The source names repeat lending at application; all 4,368 labels remain, with 952 Bad meaning not settled on time. USE-1/5/8/12 (**Must**) support approximate fit and input repair. Concede “proposed terms” is unsupported: say recorded issued terms, availability unverified. Seek proposal evidence; otherwise dropping current amount/due/term is the smallest definite pre-offer remedy. Mutable profiles remain cannot-verify; employment's conditional missingness AUC .7233→.7309 is inconclusive. Seek dated profiles; reconstruct/mask/drop fields if later recording is established. EV-6 (**Should**), EV-7 and LEAK-10 (**Must**) forbid declaring timing cleared. Approximate fit waives no leak; independent failures are not conflicts.

- **History cutoffs are tested.** Column/claim audits reproduce all 18 predictors; deleting 756 later closures and 664 payments leaves features unchanged. All 18,183 historical creations/approvals precede scoring. USE-3/6, LEAK-10 (**Must**) and CLEAN-19 (**Should**) support retention, answering the blind cutoff concern. Concede masked events lie within one hour: document clock uncertainty, retain masks, invent no offset. Future scheduled dues differ from realized payments.

- **Forced IID is the prescribed disclosed approximation.** One July cohort lacks label-arrival timestamps; mechanical chronological windows cannot certify mature training labels. SPLIT-8 (**Must**, narrowing SPLIT-7/14 and USE-10) supports this regime; mobile_churn and Cauca are closer precedents than multi-year lending embargo exceptions. Due-proxy 299 before July-30 midnight, 339 before July-31, is not actual maturity or proof that temporal evaluation is impossible. Keep approximate fit and no deployment claim; recover wider dated outcomes when available. SPLIT-9 (**Must**) receives no new exception.

- **Borrower independence and joins have measured answers.** Raw audits find 4,368 unique scored borrowers/loans, no current/history loan overlap, zero per-fold borrower/exact-copy overlap. Demographic union recovers 1,099 profiles without targets, fitted statistics or conflicting keys. EV-1/2, LEAK-16/17/29 and SPLIT-24/30 (**Must**) outweigh identity guesses from shared GPS or offer-value score gaps. Preserve the blind concerns and audit mapping; profile timing remains separate.

- **Traceable copy provenance warrants bounded consideration.** Seven hashes match the pinned participant manifest; organizer equality is unverified. PROV-2 (**Should**, narrowing PROV-1 **Must**) supports a documented case-specific gap, not invented authentication or automatic exclusion. Obtain organizer comparison if available. Redistribution restrictions remain a release matter under EV-4 (**Must**).

- **Value and source scoring both survive.** Each test has 317–318 Bad loans; independent native-fold AUC .6942 and log loss .471–.499 show modest signal. TP-2 (**Should**) opposes retiring real small signal; TP-5 (**Must**) finds no Too Small mechanism. MET-4 (**Should**) and MET-11 (**Must**) preserve accuracy = 1−official error; training-only thresholds, no invented 0.5 rule. The .00565 accuracy gain is limited metric resolution, not triviality or permission to replace the metric. P6 never clears P4.

- **Cleaning remedies are small.** CLEAN-11/14/19 (**Should**) support age, observed counts, missingness and no speculative Nigeria clipping. Concede branch's 39 values among 43 filled rows merit type clarification. Document that choice, nine absent histories and 32 sequence discrepancies; the remedy ladder favors repair over exclusion.

**Advocate rebuttal — SuperLender**

The critic identifies no irreparable Must violation and recommends the same bounded keep as my opening. I concede the five points with these consequences; textual repairs do not resolve factual timing gaps.

- **Current terms — concede.** The source's issued/taken contract descriptions cannot establish proposed versions. USE-1/3 and EV-7 (**Must**) require the prepared wording correction. Application-time availability remains cannot-verify. If strict pre-offer inputs are required without source evidence, drop current amount/due/term; a later stage requires a real decision. LEAK-10 (**Must**) cannot be waived by approximate fit. No demonstrated post-decision timing presently requires rejecting the entire task; USE-12 (**Must**) favors repair.

- **Mutable profiles — concede.** The .00171 conditional log-loss improvement does not distinguish post-outcome updating from risk-linked nonresponse. Under EV-6 (**Should**) and EV-7 (**Must**), neither a clean timing verdict nor a proved leak follows. Preserve this as an explicit curator acceptance question; source snapshot semantics or dated versions are decisive. If later updates are established, reconstruct/mask/drop affected fields under LEAK-10 (**Must**). No generic model rerun is needed.

- **Outcome arrivals/split — concede the limitation; retain the split.** The split auditor's mechanical windows are not certified mature-label refits. SPLIT-8 (**Must**) supports ForcedIIDFromTemporal with approximate fit, not prospective performance or an exception to SPLIT-9 (**Must**). Keep the source label, unknown grace/arrival rules and granted-July scope. The prepared midnight clarification preserves the proxy's diagnostic status.

- **Participant copy — concede.** Pinned hashes authenticate that copy, not organizer equality. PROV-2 (**Should**, narrowing PROV-1 **Must**) permits bounded consideration with the gap explicit. No measured damage justifies invented repair or automatic exclusion. Organizer comparison remains the settling evidence; redistribution stays separate under EV-4 (**Must**).

- **Quality/clock — concede.** Prepared sub-hour and nominal-branch explanations address the stated wording gaps. Retain conservative masks without guessing an offset; CLEAN-14 (**Should**) permits the documented semantic typing judgment. Preserve unusual valid coordinates and missingness. These repairs leave unresolved availability findings intact.

No feature, split, metric or curator acceptance change is implied by this rebuttal.

</details>

<details><summary>Critic</summary>

**Critic opening: SuperLender**

Verdict: ship only after the factual wording changes and an explicit curator decision on the unresolved availability gaps. No irreparable Must violation is demonstrated.

The critic reviewed the six independent evidence-stage reports and the definition, README and record before wording repair.

- Current terms are asserted to be proposed without evidence. This weakens the stated application-time approval/offer simulation: realized contracts may follow the decision being modeled. The claim, column and practitioner reports independently identify the source's taken/disbursed terms and absent proposal/version timestamps; dropping approval itself does not date the other fields. P3 USE-1/3 (Must), P4 LEAK-10 (Must if unavailable then), EV-7 (Must). Remedy: replace "proposed" with "recorded issued-loan terms; application-time availability unverified" throughout. Seek proposal/version evidence; if strict pre-offer availability is required without it, drop current amount/due/term. Any later-stage task needs a real decision. Uncertainty establishes neither leakage nor availability.

- Mutable profiles remain undated, and employment missingness has an unresolved conditional association. Eventually recorded employment/bank/location may differ from application inputs. the Column audit section reports employment missingness 20.17% for Bad versus13.61% for Good; adding outcome to its conditional diagnostic improves log loss by .00171. Risk-linked nonresponse remains a competing explanation. P3 USE-3 and P4 LEAK-10 (Must); EV-6 (Should), EV-7 (Must). Remedy: present cannot-verify explicitly for acceptance; obtain owner snapshot semantics or dated versions. Reconstruct/mask/drop affected fields if later updates are established. Another generic AUC would not settle this; approximate fit grants no timing exception.

- Missing outcome arrivals limit what the split measures. the Split audit section constructs chronological windows mechanically, but cannot certify mature training labels. Contractually due counts299 before July30 midnight and339 before July31 are proxies; early settlements remain unknown. P3 USE-5/8 and P4 SPLIT-8/9 (Must), SPLIT-10 (Should). Remedy: retain ForcedIIDFromTemporal and same-July/granted-cohort restrictions; name the midnight cutoff. Preserve source timely-settlement labels and unknown grace/arrival rules. Accepting this approximation cannot establish prospective performance or a maturity exemption.

- Participant-copy reproducibility leaves organizer equivalence open. Claim and precedent reports authenticate commit `16379560b10bda88b957c180d4767a37a61454a3`, with no organizer-byte comparison. P5 PROV-1 (Must), PROV-2 (Should). Remedy: retain explicit copy provenance and authenticity uncertainty; compare organizer bytes when available. No observed damage supports exclusion or invented repair. Redistribution remains a separate release matter.

- Clarify the small quality questions. Column measurements place every masked repayment/settlement within one hour after application; branch has39 values among43 filled rows. P4 LEAK-10 (Must), P7 CLEAN-14 (Should), EV-7 (Must). Remedy: disclose clock-boundary uncertainty while retaining strict masks; document nominal-branch interpretation. Neither sparsity nor physically valid overseas GPS warrants dropping rows/features.

I concede the independently tested ID/join/event-mask mechanics, adequate fold support and nontrivial signal. Blind clean-room omissions do not refute those tests. Source accuracy remains justified under MET-4 (Should)/MET-11 (Must); modest diagnostic gains do not establish metric failure or exclusion.

**Critic rebuttal: SuperLender**

The advocate accepts the substantive boundaries in my opening. I concede the seven points within their stated scope. The prepared wording repairs support a changed package; they do not establish the missing timing facts or constitute curator acceptance.

- Concede a real timely-settlement target, and agree to qualify recorded issued terms and mutable profiles. USE-1/3/5/8/12 (Must) preserve the task while requiring honest inputs; LEAK-10 and EV-7 (Must) prevent treating cannot-verify as passed. Employment's residual association remains inconclusive under EV-6 (Should). A strict pre-offer version without timing evidence requires the stated feature remedy; no such change is currently applied.

- Concede the tested history mechanics. Independent reconstruction and event-removal interventions answer the blind cutoff question under USE-3/6 and LEAK-10 (Must). Retain strict masks and the prepared sub-hour clock clarification. Neither all-history closure gating nor an invented offset is justified.

- Concede ForcedIIDFromTemporal as the disclosed SPLIT-8 (Must) approximation. Actual arrivals remain missing; chronological sensitivities cannot validate refitting under SPLIT-9 (Must)/SPLIT-10 (Should). The prepared midnight clarification correctly limits the299 proxy. No maturity exemption follows.

- Concede the raw-ID and deterministic-join evidence. Measured unique customers, zero scored/history loan overlap and zero per-fold borrower/copy intersections answer the named mechanisms. LEAK-16/17/29 (Must) require no offer-value or GPS grouping here. Profile availability remains independent.

- Concede bounded provenance treatment under PROV-2 (Should, narrowing PROV-1 Must). Manifest agreement identifies the participant copy; organizer equivalence remains open. EV-4 (Must) separates redistribution from scientific disposition.

- Concede adequate support, real modest signal and source accuracy. MET-4 (Should)/MET-11 (Must) support the error identity. The measured gain justifies neither metric replacement nor a triviality verdict; value cannot clear input timing.

- Concede small cleaning remedies and nominal branch clarification under CLEAN-14 (Should). Existing observed-history wording appropriately preserves missing coverage. Sparse branches and unusual valid GPS provide no exclusion basis.

Recommendation remains ship after the agreed wording repairs and explicit curator disposition of the unresolved availability gaps. Canonical files remain unchanged; no new research was required.

</details>

<details><summary>Review editor</summary>

Ready for the curator. The three choices are separated and ranked: current-term availability, undated mutable profiles, and participant-copy provenance. Each states the implemented version, alternative, evidence, rule and decision needed; none treats uncertainty as verified availability or a timing exception. The outcome records validity, value, quality and the factors weighed. The split disagreement is a field correction. The repaired draft distinguishes historical audit wording from its current claims, and the supporting role reports retain the substantive evidence and debate.

The requested editorial corrections have been checked against the revised draft. No additional scientific issue or experiment is needed. Final inclusion and the three open acceptance choices remain Myunghwan's decisions.

</details>
