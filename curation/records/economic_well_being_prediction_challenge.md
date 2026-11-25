---
unique_name: economic_well_being_prediction_challenge
name: economic-well-being-prediction-challenge
checked_by:
- Myunghwan
- Andrej
data_foundry_status:
- WIP (Triage)
- 'DF: Yes'
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Features: Read Later'
- Survey
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
collection_period: 1994-2016
domain: social science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://zindi.africa/competitions/economic-well-being-prediction-challenge/data
v2_path: datasets/_dev/tabarena-v0pt2/economic_well_being_prediction_challenge/dataset.py
source_row: 909
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: survey-cluster wealth index predicted from Africa-wide geospatial layers for countries not in training; a known poverty-mapping task with a grouped (country) split; the inputs are remote-sensing products, the one scope question.
- Source: first published as the Zindi "AIMS Data Science Hackathon" (Microsoft, for AIMS and CMU Africa students, 25 Jan 2021), re-opened publicly as "Economic Well-Being Prediction Challenge" (16 Apr - 15 Aug 2021, https://zindi.africa/competitions/economic-well-being-prediction-challenge); same text and the same Train.csv (5,829,604 bytes), Test.csv and SampleSubmission.csv. As published: one row per survey cluster; target "a derived 'wealth index' based on responses in various household surveys ... on a scale from 0 to 1"; features: GHSL built-up fractions by epoch, water surface, population density (5 km radius), Copernicus land-cover fractions (crops, urban, permanent and seasonal water), nighttime lights, distance to capital and to shoreline, urban or rural. Rows not counted (login); the survey programme is not named (likely DHS).
- Use case: "Granular information on economic well-being is extremely useful for governments, policy makers, and NGOs ... A successful model could be useful for filling in the gaps between the more expensive surveys" (Description): an agency estimates wealth where no recent survey exists; fit direct; regime grouped because "you must correctly predict the cluster-level estimated wealth measures found from surveys in 7 different countries not covered in the training data" (only Train.csv has labels: group by country within it).
- Siblings and duplicates: no other record of the AIMS hackathon or of DHS wealth mapping found (`grep` for wealth, poverty, well-being, aims); the old `Missing source information` marker is refuted (the competition documents every layer). External collections: none found.
- Papers and pages: the competition tabs (read through Zindi's API); the task follows the satellite poverty-mapping literature (Jean et al. 2016, Yeh et al. 2020), not checked as a source of these rows.
- Metric: RMSE ("The evaluation metric for this competition is Root Mean Squared Error", Evaluation tab); MET-4; inputs: a country column for the grouped split (to check that it ships; the API listed the AIMS parent's metric as MAE while its page says RMSE).
- Risks for /add-dataset: SEL-13 (land-cover fractions and night lights are classified satellite products aggregated to 5 km, a layer of abstraction above spectra; argue it from the columns); whether Train.csv carries country and survey year; clusters near each other across surveys (spatial leakage within a country).
- Priority: gap + (social science and the grouped regime are thin), use case + (the source names the actors and the gap-filling decision), source 0 (the competition documents the layers, not the surveys), shape + (thousands of clusters in 18 countries, grouped), risk - (SEL-13 question).


Zindi 'Economic Well-Being Prediction Challenge'; the record has no body, but the title strongly implies predicting a household/regional wealth or well-being index, typically a regression task over survey and/or geospatial covariates. This is a plausible real-world tabular task in the social-science domain. There is a risk the features are derived from satellite imagery (which would lean non-tabular) or require a grouped/spatial split. A human must check the feature set (tabular vs. imagery-derived), the exact continuous target, sample size, and whether a grouped/spatial split is needed.

**Assessment (AI, 2026-10-31; screening review):** The curator-supplied training CSV has 21,454 labeled survey-cluster rows, 18 countries and survey years 1994–2016, with no missing cells or duplicate IDs. This is medium-sized. Country/year are present, supporting the proposed whole-country evaluation; RMSE remains the source metric. The earlier direct-fit claim is not established: 18,129 rows predate 2015, whereas the linked Copernicus land-cover product covers 2015–2019, and built-up fields extend through 2014. Exact extraction epochs remain unknown. Consider a retrospective geographic-transfer task, not proven survey-year deployment. Scope under SEL-13/15 requires an argument from these geographic measurements; numeric representation alone does not settle it. Target construction/harmonization and the source's restriction on metadata inputs need clarification. The data contain 173 rows with repeated complete predictor profiles; no erroneous duplication or outcome leakage is established. The inspected fourth-place discussion also notes mixed percentage scales and country transfer; its random-CV/count-encoding suggestions are not adopted as benchmark evidence. Recommend bounded add-stage qualification only if the curator wants this retrospective task; existing suggestion/priority retained pending their decision. No curator acceptance, feature approval, scope exception or build is inferred. Evidence: Zindi competition/data pages, https://zindi.africa/competitions/economic-well-being-prediction-challenge/discussions/7283 and https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_Landcover_100m_Proba-V-C3_Global.

CC (2026-10-31, Myunghwan): Proceed to add-dataset with the necessary audits, as explicitly requested in chat. Keep columns absent established leakage. Later-created measurements of past states are acceptable; fields describing a later state or a period after the row's survey/prediction time are not. Investigate temporal or future-unseen-country evaluation. This accepts investment in qualification, not final inclusion, a build or publication.

**Assessment (AI, 2026-10-31; add-stage implementation):** Forward-year country-exclusive qualification is being implemented. Explicit future settlement periods and their through-2014 residual are masked by survey year; four source-described land-cover snapshots lack a resolvable epoch and are omitted. No row or target is dropped. Population, lights and water epochs and target harmonization remain unverified; retained columns are not certified safe by lack of a detected leak. Earlier survey-year and release-date interpretations are superseded by Myunghwan's represented-state criterion above. Checks, probes and the full independent panel remain pending.

**Assessment (AI, 2026-10-31; completed add-stage review):** Recommend retaining for added-dataset review with approximate fit. This supersedes earlier no-inspection/direct-fit, original-download byte-identity and pending-check claims: the AIMS task origin is traced, but original AIMS bytes and the survey programme are not verified. Known future GHSL periods and their complementary residual are masked; four temporally unmapped land-cover snapshots are omitted. All 21,454 rows and labels remain. Water, population and light represented epochs, target formula/harmonization and interview-level endpoint order remain unverified (USE-3/5/8, LEAK-10, EV-7). Sixteen strictly later, country-exclusive tests pass independent reconstruction (SPLIT-4/14); the explicit curator direction supplies the candidate-specific combined-split departure from SPLIT-3, without amending that rule. Native checks have zero errors/warnings; leak probes show zero exact cross-split feature copies, which cannot date covariates. Native no_spread is retained: two-option, train-only forward-country tuning gives macro-cell RMSE ridge 0.118259, LightGBM 0.118795, RF 0.120413, against dummy 0.185473 over all sixteen dependent cells. Signal supports retention (TP-1/2/3); it does not prove family separation or temporal safety. The full independent ten-role panel, one debate rebuttal each and cold editor are documented in the Review; their recommendation is advisory, not a human verdict. No warning acceptance, final inclusion or build is inferred. Priority 3: gap + (local social-science coverage), use case + (survey-gap mapping), source 0 (incomplete extraction/survey provenance), shape + (21,454 rows with supported transfer cells), risk - (unresolved represented epochs and target comparability).

CC (2026-11-02, Myunghwan): Accept calendar-year timing as an approximation and resolve issue 1 after the requested within-country, across-year check. Actual follow-up: "OK. then 1 can be resolved. please finish tabarena-add-dataset part on this". Continue the add stage; no target, split-field or overall ship/build/commit decision is inferred.

**Assessment (AI, 2026-11-02):** The requested check covers 18 countries and 70 country-year samples. Water, population and light means change in all 52 comparisons between consecutive observed years; the known fixed 2000–2014 construction layer also changes in all 52 because yearly samples can contain different clusters. Five exact country/distance signatures spanning 1994–1995 cover 25 rows with all 14 numeric geographic inputs unchanged; these signatures do not prove cluster identity. Independent review reproduced the counts. Exact feature epochs remain cannot-verify (EV-1/2/6/7, USE-3/8, LEAK-10); Myunghwan has resolved the scientific review using an annual approximation. A demonstrated actual later-state measurement would still require repair. No data or split change is justified. Prepared definition checks have 26 checks, zero errors and zero warnings, with three infos. The full frame, target and all sixteen exact memberships plus non-prose implementation AST are identical, supporting reuse of the completed native probes and bounded training-only tuning. No temporal-safety certificate or new model ranking is claimed. Issue 2 and the split metadata row remain open. Priority 3: gap + (social science), use case + (survey-gap mapping), source 0 (incomplete provenance), shape + (supported transfer cells), risk - (unverified epochs and target comparability).

CC (2026-11-02, Myunghwan): "ok. ship it. but it's not just purely temporal -- temporal x unseen". Accept the reviewed definition for a separately requested build, with temporal × unseen-country evaluation.

**Assessment (AI, 2026-11-02; ship application):** Ship accepts the supplied 0–1 wealth-index target with documented approximate fit (issue 2); it does not verify the unknown construction or harmonization. Issue 1 remains resolved under the accepted annual approximation. The explicit joint-split correction is represented by both existing required_split values, Temporal and Grouped. This is a candidate-specific departure from generic SPLIT-3 and the one-value record guidance: the source task and actual custom memberships enforce both year < t and country != c. Temporal is the backend representation, while the scientific protocol is temporal × unseen-country; no new backend enum or global rule is introduced. Independent consistency review supports application (USE-5/8, SPLIT-4, curator precedence). All rows, targets, feature handling, learner/scorer settings and sixteen memberships are preserved; documentation-only equivalence supports reusing the completed probes and bounded tuning. Preserve all source/timing limits. Archive the completed review; no open issue or metadata row remains. Claim ownership stays with Myunghwan until later integration; ship does not authorize a container build, commit or publication. Priority 3: gap + (social science), use case + (survey-gap mapping), source 0 (incomplete provenance), shape + (supported transfer cells), risk - (unverified feature epochs and target comparability).

CC (2026-11-03, Myunghwan): Run tabarena-build-commit on this dataset and then update the claim, as explicitly requested in chat. The earlier instruction to keep a new dataset out of the existing PR remains in force.

**Assessment (AI, 2026-11-03; build completion):** Built one format-2 container, UUID 01a1a3a9-2ea2-7373-813a-aa5517164da9, checksum v2:64f4ac51f0d0aa0026de5f978ca2b3d2c32605800d8a7bc08bcfb3ee9fa1e701, from clean source commit 609f0b8442ea36a88f179370c36e5e06696d45a7. Saved-container reload/checksum and reproduction from the sole traced Train.csv (5,829,604 bytes) pass. Native checks: 26, zero errors and warnings, three infos. The accepted frame, target and all sixteen exact memberships match the completed qualification, so existing probes and bounded tuning are reused; no new models or unresolved task flags. The previously investigated no_spread result remains disclosed. The protocol is temporal × unseen-country, with 21,454 rows, twelve predictors and 6,256 distinct tested rows. Accepted annual timing and supplied-index approximations retain their unknown epoch and harmonization limits. The official claim note and expiry are updated for Myunghwan; existing triage stage is preserved independently of the accepted verdict. Local commits remain separate from the existing PR. Retain ownership until integration; no code push, PR update, raw-data upload or claim release.

CC (2026-11-05, Myunghwan): Repeat add-dataset → review-added-datasets → build-commit against updated main, reusing our past decisions; return only new input requirements. This requests local commits and does not authorize adding to the existing PR.

**Assessment (AI, 2026-11-05; main migration):** Previous curator decisions and their original dates are retained from the accepted local branch; they are not fresh review marks on a new source fingerprint. Requalification against main 9048f36a is in progress. Preserve temporal × unseen-country, accepted annual timing approximation and supplied-index approximate fit unless new evidence contradicts them.

**Exception to SPLIT-3 (2026-11-02, Myunghwan):** "ok. ship it. but it's not just purely temporal -- temporal x unseen". This candidate-specific higher-ranked USE-1 (Must, P3) override preserves the approved future-year survey-gap task in an unseen country: either single-regime substitution changes that task. It is not an ordinary waiver of SPLIT-3 Must and makes no general rule amendment. The current request expressly carries this prior decision forward. Serves USE-1 (Must, P3): preserve the approved future-year survey-gap task in an unseen country.

CC (2026-11-05, Myunghwan): the declared metric rmse is checked by reuse of the 2026-11-02 ship decision, as explicitly requested for this repeated cycle. This preserves the prior source-RMSE decision; it is not a fresh mark on a new page snapshot.

**Assessment (AI, 2026-11-05):** review panel (focused): ship; disputed: none newly open; for the curator: no new issue. Claim, column, split and precedent audits, fresh independent participant-input review, mediation and cold editor completed. The independent replacement participant review followed an input-access contract without enforced filesystem isolation. Current-main checks have 27 checks, zero errors/warnings and three infos. Decode R/U as Rural/Urban under CLEAN-12; targets and numeric inputs are unchanged and all train/test ID sets are preserved, while canonical indices are regenerated. Current sixteen-split probes retain useful signal and the known no_spread flag; ID-remapped prior predictions reproduce all 48 scores, without claiming identical stochastic refits. The participant review finds no demonstrated unavailable-information exploit: whole-data frequency gain is matched by random features and exceeded by train-only frequencies. Annual timing and supplied-index approximations remain accepted; exact epochs and harmonization remain unknown. The resolved issues are restored as history in the Review under current retention guidance. The formal SPLIT-3 register warning is explicitly reconciled against the higher-ranked accepted use case and original human authority; no flag is suppressed. Priority 3: gap + (social science), use case + (survey-gap mapping), source 0 (incomplete extraction/target provenance), shape + (supported mixed-feature transfer cells), risk - (unverified epochs and comparability).

**Assessment (AI, 2026-11-05; requested build):** The requalified definition built from clean source 197d469d2931d8949f5454bc4d839f6b05558ef8 as format 2 UUID 01a1adf2-7ba6-7a75-a157-1c1451ba511e. Reload/checksum and reproduction from the sole traced CSV pass with zero errors/warnings. New Rural/Urban labels and regenerated positional splits match final qualification; all original scientific membership ID sets remain unchanged. The earlier accepted container is retained for its historical branch. Local commits remain separate from the existing PR; no code push or claim release.

CC (2026-11-05, Myunghwan): Repeat add-dataset → review-added-datasets → build-commit after the review-procedure update, using our past decisions; return only genuinely new input requirements.

**Assessment (AI, 2026-11-05; qualification reuse):** The reviewed source remains 9048f36a, already requalified in the previous cycle. Current runtime/scientific procedures and all prepared data, targets, dtypes, metric and sixteen positional splits match; the completed seven-role panel, probes and prior decision provenance remain applicable. A focused independent claim/reuse audit, mediation and cold editor found no new input. The current review store records this request’s carry-forward authority, not copied closed-item marks or a fresh independent scientific verdict. The requested rebuild from clean b4ac95ff0f853de54117555ae24bd013c3630fd4 produced UUID 01a1ae48-ee3d-73ae-bf99-a2b037658716 with the same checksum. Reload and traced-input-only reproduction plus local manifest backup pass; native27checks have zero errors/warnings. The annual approximation, source-index approximate fit, temporal × unseen-country protocol, known no_spread disposition and unverified epochs/harmonization remain explicit. Earlier containers/commits and original decision fingerprints are preserved. Local commit only; no PR/code push, claim release.

**Assessment (AI, 2026-11-21):** collection facts set from the split audit: survey clusters of 18 countries, 1994-2016, target from the survey's own household answers; the GHSL, population and night-light layers are later products joined onto older clusters (`Features: Read Later`); no cluster is followed across rounds, so no `Entities: Recur` (exact location repeats are 41 groups and 205 rows, all in the CAR 1994-95 survey, whose positions are locality points; measured 2026-11-21). Water, population density and night lights are each one read for all rows: at the same place they do not change between surveys up to 22 years apart.

**Assessment (AI, 2026-11-21):** review panel (full re-check): ship after changes; disputed: SPLIT-3 (the USE-1 override of the joint split fails on the written use case and the source's all-years Test.csv; rec. grouped by country over all years), LEAK-10 (population density a later read, rec. mask under the leaf or drop under the joint split; night lights undated, rec. keep with a note), TP-4 (methods beat night lights alone on 9 of 9 leaf splits, 10 of 16 shipped cells); for the curator: issues 3-7 and H (6, 7 and H only if issue 3 stays A). Signal real (TP-2: tuned LightGBM RMSE 0.1135 against 0.1855 dummy, shuffled labels 0.1857-0.1885), no model spread (ridge 0.1137). Licence checked: the competition rules allow commercial and non-commercial use under CC BY-SA 4.0, so the string stays. Priority 3: gap + (social science, grouped by country), use case + (survey-gap mapping for targeting), source 0 (undocumented index and undated layers), shape + (21,454 rows, 18 countries), risk - (split regime and undated population and lights).

CC (2026-11-24, Andrej): review issue 3, B: whole countries are held out with all their survey years (3 folds by country, 3 repeats), the source's own task (its Test.csv holds 7 other countries over 1998-2016); the use case is an agency mapping a country without surveys of its own. This replaces the temporal × unseen-country split and its SPLIT-3 exception (Myunghwan, 2026-11-02). Time basis `UnseenGroup`; split-tree leaf L-PLACE.groups. Issues H, 6 and 7 applied only to the joint split and lapse.

CC (2026-11-24, Andrej): review issue 8, B: the warning that a test fold holds few countries (6 of 18) is accepted; a few whole countries per fold is what an unseen-country task is, and the signal carries over to held-out countries.

CC (2026-11-24, Andrej): review issue 8, C: leave one country out on the 10 countries surveyed in 2014-2016 (one split each, all survey years), in place of 3 x 3 country folds, whose repeats share most of their training countries. Accepted with it: the 8 other countries are never tested, and the splits are 1 x 10.

CC (2026-11-24, Andrej): review issues 4 and 5, use case b: "I agree with use case b". The prediction point is today: an agency maps the past survey years of a country without surveys of its own with every layer as read today, the source's gap-filling framing. Population density and night lights stay on every row (issue 4 A, issue 5 A); the construction masks are removed and the four land-cover columns restored, all as read today. This replaces Myunghwan's call of 2026-10-31 against fields that describe a later state than the survey, for this use case.

CC (2026-11-24, Andrej): review issue 10, B: "Option B: Ship for non-commercial use. We are building a non-commercial academic benchmark". The licence note names the competition's CC BY-SA 4.0 grant, the DHS terms of use (no commercial use; the labels are cluster-level indices) and that the benchmark uses the data for non-commercial academic research only.

CC (2026-11-24, Andrej): review issue 9, B: "Option B: Add Test.csv with recovered labels." Step 1, the validation of the row join on Train.csv, ends below the 99.9% bar its notes set (97.43% of rows within 0.0012), so Test.csv is not added: 18 countries ship and issue 9 stays open with the measured answer.

**Assessment (AI, 2026-11-24):** use case b applied: no masks, the four land-cover columns back, 16 inputs on all 21,454 rows; licence note for non-commercial academic use. Row join of issue 9 on Train.csv (africa_poverty `dhs_wealth_index.csv` at commit cb769c74, Natural Earth coastline, ellipsoidal distances): every row matched within its country, year and urban/rural cell, distance to the capital agreeing within 0.002 km; 20,903 of 21,454 rows (97.43%) within 0.0012 of Target, 21,321 (99.38%) within 0.0014; the remaining 133 are 131 Central African Republic 1994-95 rows at shared locality points, which no distance separates, and one Cameroon 2004 pair. Zindi's Target is the rescaled `wealthpooled` plus a per-row deviation spread evenly over about ±0.0013, so 0.0012 sits inside it. Check: 0 errors, 0 warnings (3 accepted), 1 info (129 conflicting duplicate rows). Task probes (10 splits): random forest RMSE 0.110, LightGBM 0.111, linear 0.117, single feature 0.126, training mean 0.192; random forest ahead of night lights alone on 9 of 10 countries (mean lead 0.0105). Group probe: R² -0.41 to -0.53 per row with one country per fold, IID 0.78. Leak probe: 0 test rows with a feature copy in training.

CC (2026-11-24, Andrej): review issue 9, b: "Reply (b): Add Test.csv on a bar matched to the data". The 7 countries of Zindi's Test.csv join with labels recovered from the source's cluster table (sustainlab-group/africa_poverty `data/dhs_wealth_index.csv`, commit cb769c74), Target = 0.245034 × wealthpooled + 0.343664 refit on Train.csv; a match counts only where it is unambiguous (distance to the capital within 0.002 km, no second cluster as close, no shared coordinate), which on Train.csv finds the right cluster for every accepted row; Train.csv keeps its released Target. Leave one country out (issue 8) now holds out the 16 countries surveyed in 2014-2016 among 25.

**Assessment (AI, 2026-11-24):** issue 9 b applied: 28,618 rows in 25 countries (21,454 Train.csv, 7,164 of Test.csv's 7,194 with recovered labels; 30 near-ties left out). The join reproduces the earlier run exactly: 21,321 of 21,454 Train.csv rows (99.38%) get the right cluster, largest deviation of a right match 0.0013; the bar accepts 21,146 Train.csv rows, all right, and 7,164 Test.csv rows (none at a shared coordinate, largest capital-distance gap 0.0018 km). 16 test countries now (Angola, Burkina Faso, DR Congo, Uganda, Zambia, Zimbabwe added); Benin and 8 Train.csv countries (5,923 rows) are never tested. Task probes (16 splits): LightGBM RMSE 0.110, random forest 0.111, linear 0.118, single feature (night lights) 0.123, training mean 0.200; random forest ahead of night lights alone on 15 of 16 countries (mean lead 0.0116; Malawi the exception). Group probe: LightGBM R² 0.60 grouped against 0.78 IID; per row -0.20 to -0.31. Leak probe: 0 of 22,695 test rows with a feature copy in training.

CC (2026-11-25, Andrej): the declared split (leave one country out over the 16 countries surveyed in 2014-2016, all their survey years, among 25 countries; leaf L-PLACE.groups) is checked, as implemented.

CC (2026-11-25, Andrej): verdict ship; nothing open in the review. The build is stale until rebuilt.

## Review

**Outcome:** added. Ship: leave one country out over the 16 countries surveyed in 2014-2016, among 25, replaces the joint split by year and country; the full re-check of 2026-11-21 that led there is summarised below, its numbers measured on the earlier rows and splits. Validity: a task whose test differs from training is split either by group or by time, never both, and the use-case override behind the joint split fails on the record's own use case and on the source's Test.csv (7 unseen countries over 1998-2016); population density is a later read on the 18,129 rows before 2015 (issue 4) and the night-lights epoch is unknown (issue 5); 0 copies cross the split in 16 splits. Value: a large real signal, tuned LightGBM RMSE 0.1135 against 0.1855 for the training mean, with shuffled labels at 0.1857-0.1885; a fit on night lights alone (RMSE 0.1232 on the shipped split, 0.1223 on the country holdout) is beaten by the best model on 9 of 9 country-holdout splits but on only 10 of 16 cells of the shipped split; ridge and LightGBM tie (0.1137 against 0.1135): the dataset does not separate models, which the panel found no reason to retire it for. Quality: wording fixes applied to the definition without a decision (the same-place check, the pooled rescale of the target, water, scope, the metric's country offset, the conflicting duplicates, the source's Test.csv); nothing rebuilt. Decided 2026-11-24: whole countries over all years (issue 3, B, applied; the joint split's items H, 6 and 7 lapse); leave one country out on the 10 countries surveyed in 2014-2016 (issue 8, C, applied); the prediction point is today, an agency mapping past survey years with every layer as read today, so population density and night lights stay, the construction masks go and the four land-cover columns return (issues 4 and 5, A under use case b); the dataset ships for non-commercial academic research only (issue 10, B). The source's 7 test countries join with labels recovered from the source table on a bar matched to the data (issue 9, b, applied): 25 countries, 28,618 rows, 16 of them tested one at a time. Nothing open.

**Main points:** nothing open. On 2026-11-24 Test.csv joined (issue 9, b): 7,164 of its 7,194 rows with labels recovered from the africa_poverty table, accepted only where the match is unambiguous (on Train.csv every accepted match gives the right cluster, 99.38% of all rows; the labels deviate from Zindi's by up to about 0.0013), and leave one country out over the 16 countries surveyed in 2014-2016 among 25.

**Record judgment:** a real task with approximate fit: the wealth index of survey clusters in 18 countries (1994-2016), predicted from mapped settlement, population, light and distance layers. The record requires the split by year and by country together, which issue 3 reopens; the construction of the index and the dates of the population and light layers are not documented (issues 2, 4 and 5).

**Horizon:**

* **Verdict:** to be asked only if issue 3 stays A (under issue 3 B the folds span all years and this block falls away; under A the windows are those of a split that departs from the split tree's leaf, which holds out countries over all years); then change to a one-year gap (C), low confidence, since the source states neither a horizon nor a label delay.
* **Length:** one survey year, the time unit the year column records; a deployed model is assumed to be refit once a year. The source is silent on both: this is our assumption, which a person signs off[^x21e1].
* **Gap:**
  - The joint split tests a later year in a country never surveyed before, which is a forward reading: at deployment in year t, only surveys already published exist.
  - A survey's index appears about a year after fieldwork (our assumption, not the source's), so under that reading the gap follows the delay and the newest training year is not yet available[^x21e4].
  - Read as historical gap-filling, as the written use case says, no gap is needed, but then the later-year requirement has no reason either (issue 3).
* **Time frame:**
  - The release covers 1994-2016; the test windows are the newest three years, 2014-2016.
  - Each window tests every country observed that year with the country removed from training: 16 cells, 10 of the 18 countries.
  - Each cell's training side differs from every other (another year, or another country left out), so the 16 cells count as 16 training sides against the 9 the target asks for[^x21e2].
  - Why the newest three years and not years spread over the history is not written; that every training side keeps 66% or more is no reason, since the floor is half the rows[^x21e3].
  - The 2015-16 Malawi and Tanzania surveys and probably the 2014-15 Rwanda survey fall into two year cells each; their country is out of every training side, so no leak.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One year, no gap, 2016/2015/2014 (implemented) | Each country-year cell of 2014-2016, trained on earlier years of other countries | 16 cells: 1,222 / 2,103 / 2,931 rows by year; train 66-89% | newest period; 16 training sides against a target of 9 | earlier years untested; no gap although the joint split reads forward; the 2015-16 surveys fall into two windows |
  | B | One year, no gap, years spread (e.g. 2016, 2014, 2012) | Replace 2015 with an older year that keeps half the rows for training | not measured | tests more of the history | lower training shares; needs the year counts |
  | C | One year, one-year gap, 2016/2015/2014 | Train only on years before t-1 | 16 cells, same rows; train 75.9-79.4% (2016 cells), 59.8-68.5% (2015 cells), 58.3-62.8% (2014 cells) | matches the forward reading the joint split implies | drops the newest training year; the 2014 cells keep only 58-63% of the rows |

* **Recommendation:** C, if issue 3 stays A: the joint split only makes sense as a forward test, and a forward test waits for the label delay; the splits comment then names the length, the gap, the time unit and the count. **Decision:** keep A, or change to B or C?

**Notes for the AI:** Ask only if issue 3 stays A. On C, train on `year < test_year - 1` in `_make_splits` and `_extra_checks` (the check becomes `tr["year"].max() < te["year"].min() - 1`), add to the splits comment: "Length, step and time unit: one survey year, refit yearly; the source states none, this is assumed. Gap: one year, an assumed delay between fieldwork and a published index, as the joint split tests a later year. Count: 16 training sides over 3 years, against the 9 an IID split of 21,454 rows gets. The 2015-16 Malawi and Tanzania surveys and the 2014-15 Rwanda survey each fall into two year cells; their country is out of every training side." On A, the same text with "Gap: none, as the use case fills in past years; a survey's publication delay is unknown." and a reason for the newest three years other than the training share. For B, run `dataset windows economic_well_being_prediction_challenge` on a compute node first: rows per year and per country-year, and the training share with each country removed for 2010-2013.

**Resolved (2026-11-24, AI):** no longer applies: issue 3 is B (Andrej, 2026-11-24), whole countries over all years; this item concerned only the joint split by year and country.

[^x21e1]: **SPLIT-12** (Should): the horizon, the refit cadence, the gap and the time unit come from the use case and the source; the splits comment names each, or says the source is silent and what is assumed. The split tree's windows check: a length, refit cadence or gap the source does not give is proposed by the agent and signed off by a person.
[^x21e2]: **SPLIT-14** (Must) and **SPLIT-15** (Should for the count): every window trains on at least half the rows and tests at least 33 scored units; the count aims at SPLIT-33's count for two thirds of the scored units (here 9, the scored unit being the row); training sides shared by several test parts count once.
[^x21e3]: **SPLIT-15** (Must for the newest window, Should for the others): the newest window is always a test window; the others need a reason, and other years are preferred. The training floor is 50% (cooking_time_1m), so a 66% share does not set the newest three years apart.
[^x21e4]: **SPLIT-10** (Should): the gap follows the label delay or a planning lead. In the split tree, no gap where the gap rules ask for one is the windows exception only a person allows; the agent does not take it.

**Issues for Myunghwan:**

1. **Use calendar-year timing as an approximation?**

   - **Problem:** Retained water, population and lights lack exact represented epochs; a year comparison cannot establish them.
   - **Experiments:** The previously requested within-country comparison showed changes across observed survey years but could not distinguish a changed layer from changed sampled locations.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Annual approximation (implemented) | Keep the reviewed inputs and explicit future-period masks | Preserves the accepted reconstruction task | Exact retained epochs remain unknown |
     | B | Defer for exact provenance | Wait for dated source layers | Could establish historical alignment | No recovered exact extraction history |

   - **Recommendation:** A, carrying forward the accepted approximation. **Decision:** Already resolved; no repeated mark requested.

   **Resolved (2026-11-02, Myunghwan):** “OK. then 1 can be resolved. please finish tabarena-add-dataset part on this.” The annual approximation is accepted; this does not certify exact epochs. Evidence of an actual later-state measurement still requires repair.

2. **Include prediction of the supplied wealth index with approximate fit?**

   - **Problem:** The challenge supplies an asset-related cluster-average index on 0–1 without the survey instruments, formula or cross-survey harmonization pipeline.
   - **Effect on the task:** Predicting the released index does not establish comparable welfare measurement or exclude future-dependent normalization in the unknown source pipeline.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Predict the supplied index (implemented) | Keep all labels unchanged and source RMSE | Preserves the published prediction target | Construction and harmonization remain unknown |
     | B | Defer for target documentation | Wait for the construction pipeline | Could verify comparability | Delays the accepted source-index task |

   - **Recommendation:** A, carrying forward the accepted source-index interpretation. **Decision:** Already resolved; no repeated mark requested.

   **Resolved (2026-11-02, Myunghwan):** “ok. ship it. but it's not just purely temporal -- temporal x unseen”. Ship accepted the reviewed source-index task with approximate fit and explicitly confirmed the joint regime. Both required-split values are retained. The 2026-11-05 request authorizes reuse of that decision against the requalified package, not relabeling old marks as new ones.

3. **Hold out whole countries over all years instead of the joint split by year and country?**

   - **Problem:**
     - The definition holds out both a later year and the test country, but a task whose test differs from training is split either by group or by time, never both, and that rule has no exceptions unless a higher-ranked rule overrides it[^x21e5].
     - The override cited is the use case, yet the written use case ("historical local wealth where survey coverage is missing"), the source's aim ("filling in the gaps between the more expensive surveys") and the source's own Test.csv (7 other countries over 1998-2016) all describe unseen countries over all years, the split the split tree gives for this survey (whole countries held out; the country holdout below)[^x21e6].
     - So the override does not hold on the record's own facts, the split tree sends a use case that meets both another place and a later time to the place step with the later time named as untested[^x24e1], and keeping the joint split as "a listed departure" would treat a rule without exceptions as one that has them.
   - **Background:**
     - The joint split was set by Myunghwan on 2026-11-02 ("it's not just purely temporal -- temporal x unseen"), before the split tree (2026-11-17); the written use case was not changed with it.
     - A third reading, a purely temporal split that keeps the test country's own earlier surveys, is a different task (a country already surveyed); nobody on the panel argues for it, but it is what an analyst between two surveys of one country faces[^x21e7].
   - **Effect on the task:** the joint split tests 10 of the 18 countries on 6,256 rows of 2014-2016; the country holdout tests all 18 countries on all 21,454 rows (3 folds by country, 3 repeats) and drops the requirement that training years come before the test year.
   - **Experiments:**
     - Mean RMSE (lower is better) on the 16 shipped cells and on the 9 splits of the country holdout; tuning on the training side only with folds grouped by country (ridge on log inputs with missing flags, 7 alphas; random forest, 6 configurations; LightGBM, 16 random configurations); night lights alone as an isotonic fit, the feature chosen by training R² (lights on all 25 splits); shuffled labels as 5 permutations of the training labels, scored on the true test labels.

       | | Shipped split (16 cells) | Country holdout (9 splits) |
       |---|---|---|
       | Training mean | 0.1855 | 0.1938 |
       | Shuffled labels, LightGBM | 0.1885 | 0.1958 |
       | Shuffled labels, ridge | 0.1857 | 0.1940 |
       | Night lights alone | 0.1232 | 0.1223 |
       | Ridge, tuned | 0.1137 | 0.1165 |
       | Random forest, tuned | 0.1158 | 0.1167 |
       | LightGBM, tuned | 0.1135 | 0.1164 |
       | LightGBM, default | 0.1246 | 0.1221 |

     - Paired, night lights alone minus the methods (RMSE, positive when the methods are better):

       | Split | Compared with | Mean difference | SE | Splits where the methods are better |
       |---|---|---|---|---|
       | Shipped | tuned LightGBM | +0.0098 | 0.0066 | 10 of 16 |
       | Country holdout | tuned LightGBM | +0.0059 | 0.0015 | 8 of 9 |
       | Shipped | best family per split | +0.0150 | 0.0054 | 10 of 16 |
       | Country holdout | best family per split | +0.0085 | 0.0011 | 9 of 9 |

     - The signal is real on both splits: the lowest shuffled run never beats the best method on any of the 25 splits. On the shipped split lights alone wins the six cells with large country offsets (Malawi 2014, 2015 and 2016, Rwanda 2014 and 2015, Ethiopia 2016), so the comparison is borderline there (issue 7); on the country holdout the best model is ahead on 9 of 9.
     - The cost of leaving out the test country's own earlier surveys (domain practitioner, mean RMSE over the 16 cells, untuned HistGradientBoosting and ridge; its own inputs and settings, so not comparable with the tuned table above; only the change between rows counts):

       | Training side | HistGradientBoosting | Ridge |
       |---|---|---|
       | Shipped: earlier years, other countries | 0.1270 | 0.1133 |
       | Earlier years, all countries | 0.1105 | 0.1092 |

   - **Consistency:** wadden_sea_sibes_macoma_abundance has the same shape (a map between the places of a survey) and went grouped only; lt_vehicle_loan_default_prediction's use-case override of a split rule was replaced by an amendment of the rule. B follows the first, C the second, and A follows neither[^x21e8].
   - **Panel:** the advocate first defended the joint split and then conceded that the override does not hold on the written use case or on the source's all-years test; advocate, critic and mediator now agree on B unless the curator writes a forward use case. The split auditor finds the joint split sound in its mechanics (no copies across the split, the training floor and the test sizes pass).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the joint split (implemented) | No change to the splits; the splits comment names the split tree's leaf and the reason, and the departure goes to a reviewer, who lists it in the tree's table of definitions that ship another split | keeps Myunghwan's task of 2026-11-02; stricter test | two regimes against a rule without exceptions; the override it cites fails on the written use case and on the source's test; tests 10 of 18 countries; the comparison with lights alone is borderline (issue 7) |
     | B | Hold out whole countries over all years | 3 folds by country with 3 repeats over all 21,454 rows; the use case says the test stands for a country without surveys of its own | follows the split tree, the source's test and wadden_sea; tests all 18 countries; the best model beats lights alone on 9 of 9 splits; the check warning goes (issue 6) | drops the later-year test Myunghwan asked for; a rebuild |
     | C | Keep the joint split with a written forward use case and an amended rule | The use case names an agency mapping a never-surveyed country in a year after its training surveys; the one-regime rule gets an amendment for this case, and the split tree a branch for it | keeps the joint task by the route lt_vehicle took | needs a forward use case nobody has written; changes a rule for one dataset and the tree, which sends a use case meeting another place and a later time to the place step (only a reviewer adds a branch); the comparison with lights alone stays borderline |
     | D | Fill in country-year surveys (Andrej, 2026-11-24) | Group by survey round (one country in one year, 70 rounds); 3 folds of whole rounds with 3 repeats; every other round trains, also the same country's earlier and later years; the country is an input; the use case: a year's map for the countries not surveyed that year | the use case of mapping between survey rounds; tests every country and year; the split tree's leaf for it (L-FILL.unit); the country's own average stays weak (RMSE 0.184 against 0.196 for the overall mean), so the task rests on the map inputs | no source names this use case or split: the source tests other countries; tests neither a never-surveyed country nor a later year; a rebuild |

   - **Recommendation:** B: the source's own task (its Test.csv holds 7 other countries over 1998-2016) is a valid predictive task, and the source's task comes before one we define; D is a sound task too, but no source names it, and its lower error comes from the same country's other rounds in training. **Decision:** keep the joint split (A), or change to B, C or D?

   **Notes for the AI:** On D: add a `survey` column (`country` and `year`, e.g. "Kenya 2014") in `_clean`; remove `temporal`, `TEST_YEARS` and `_make_splits` (default grouped splits: 3 folds, 3 repeats) and add `grouping = Grouping(on="survey", labels="per_sample", prediction_unit="row", context="none", definition="One group is a survey round, one country in one year, held out with all its clusters; the other rounds train, the same country's other years included.")`; keep `country` and `year` as inputs; `time_basis = TimeBasis("RetrospectiveFillIn", "survey clusters of 18 countries, 1994-2016; a held-out round stands for a country in a year it was not surveyed, filled in from the other rounds, earlier and later. Not tested: a never-surveyed country, a later year.")` and `split_leaf = "L-FILL.unit"`; `use_case`: "An agency maps local wealth for a year in the countries no survey reached that year, from the survey rounds of other years and other countries."; `split`, `splits_comment` and the split-walk bullet to match; drop the evaluation bullet and the SPLIT-3 override bullet; record: `required_split` Grouped only, drop `Non-IID (Temporal)`, a CC line. Re-run `dataset check` and the probes on the new folds (Slurm). On B: remove `temporal`, `TEST_YEARS` and `_make_splits` (default grouped splits: 3 folds, 3 repeats) and add `grouping = Grouping(on="country", labels="per_sample", prediction_unit="row", context="none", definition="One group is a country, held out with all its survey years: a test country stands for a country without surveys of its own, as in the source's test of 7 other countries over 1998-2016.")`; keep the masking part of `_extra_checks` and `_decisions` and drop their year and country checks; drop `ID` in `_clean` and keep `country` only as the group; keep `data_tags = ("Spatial",)` and declare `time_basis = TimeBasis("UnseenGroup", "survey clusters of 18 countries, 1994-2016; a test country stands for a country without surveys of its own, mapped for the years the other countries' surveys cover, which are all in training. Not tested: a later year.")` (the build adds the tag and renders the `Time basis:` line; never write either by hand) and `split_leaf = "L-PLACE.groups"`; delete the evaluation bullet and the SPLIT-3 override bullet of `curation_comments`; `use_case`: "An agency estimates local wealth in a country without surveys of its own, to inform geographic targeting of support. A model trained on the surveys of other countries is evaluated on every survey of a held-out country."; `split` and `splits_comment` to match; add to `fit_reason` that the test stands for a country never surveyed, not for the gap between two surveys of one country. Record: `required_split` Grouped only, drop the `Non-IID (Temporal)` tag, and a CC line that the 2026-11-02 SPLIT-3 exception is replaced. Re-run `dataset check` (the missing-in-training warning should go), the leak, task and group probes, and TP-4 on the new folds. On C: the curator writes the forward use case; add an amendment to SPLIT-3 in splits.md and a row to its cases table, as for lt_vehicle_loan_default_prediction, and cite it in the splits comment; the split tree needs a branch for a forward use case that meets another place and a later time, which only a reviewer adds, so put it to Andrej before writing code; no `split_leaf` until the branch exists. On A: add to the splits comment "The split decision tree (SPLIT-36) reaches L-PLACE.groups for this survey (Survey, whom and when the model predicts for: places outside the training surveys; the place step, several countries): Grouped · UnseenGroup, countries held out over all years; the source holds out 7 countries over all years. We also require earlier years, the curator's temporal × unseen-country task (Myunghwan, 2026-11-02), a departure confirmed by <reviewer, date>."; once the reviewer confirms, add `split_leaf = "L-PLACE.groups"` and the row to split_tree.md's table "Definitions that ship another split" (Definition, Leaf L-PLACE.groups, Ships "temporal × unseen country, 16 country-year cells", Reviewer, Date, Reason). Evidence: the run folder (tp24.py, tp24_cells.csv, 1401950.log) and `.../domain-practitioner/` (actor.py, actor_cells.csv).

   **Answer (AI, 2026-11-21):** the source's own test years, measured.
   - The source's Test.csv (a public GitHub copy) covers 1998-2016 in 7 other countries (Angola, Benin, Burkina Faso, DR Congo, Uganda, Zambia, Zimbabwe): its test years spread over the whole period.
   - So the source's task is unseen countries over all years, and the split tree gives whole countries held out over all years; the later-year requirement is the curator's departure from it, as option A lists it.
   - The recommendation stays A.

   **Answer (AI, 2026-11-21):** the full re-check revised this issue.
   - This replaces the recommendation of the answer above (A); its Test.csv fact is now in the problem.
   - The panel read the override against the rule ranking: a rule without exceptions yields only to a higher-ranked one, and the use case it cites describes the country holdout, so the recommendation changed from A to B; the earlier option C (a new tree branch) became the amendment route.
   - The panel measured the country holdout against the shipped split (tables above): the signal is the same, and only the country holdout gives a clear lead of the methods over night lights alone.
   - Issues 4, 6 and 7 and the Horizon block depend on this one: decide it first; issue 5 does not.

   **Answer (AI, 2026-11-24):** what the split rules of 2026-11-24 change.
   - The split tree now names this case: a use case that meets both another place and a later time takes the place step, with the later time named as untested. Walked from the record's type (Survey), it reaches whole countries held out over all years, the split B ships, with `UnseenGroup` as its time basis.
   - The time basis under B is now declared as a structured `TimeBasis` with the tree's leaf named, not written as a tag and a line by hand; the notes above say so.
   - A stays possible only as a departure a reviewer confirms and lists in the tree; C now needs a tree branch as well as the rule amendment, and only a reviewer adds one.
   - The rules do not decide the item: the choice between B and a confirmed departure (A) stays with the curator. The recommendation stays B.

   [^x24e1]: **SPLIT-36** (Should), split_tree.md, "How to walk it": a use case that meets both another place and a later time takes the place step; its time basis names the later time as untested.
   [^x21e5]: **SPLIT-3** (Must): a non-IID task is grouped or temporal, never both; the use case decides which. principles.md, "Exceptions and amendments": a Must has no exceptions; only a higher-ranked Must overrides it, anything else is an amendment.
   [^x21e6]: **SPLIT-36** (Should): walk the split tree from the collection type; a definition that ships another split than its leaf names the leaf, what the source prescribed and the reason, and the departure goes to a reviewer. The walk for this survey: [SUR.meets] places outside what the training surveys covered (a country without surveys of its own) → place step [PLACE.several] yes, 18 countries → [L-PLACE.groups] Grouped · `UnseenGroup`. The source's Test.csv (7 other countries, all years) matches the leaf, so it fills in the leaf (SPLIT-19). **USE-1** (Must): the use case names the actor, the moment and the decision; the record's use case is "An agency estimates historical local wealth where survey coverage is missing".
   [^x21e7]: **USE-10** (Must): decide from the use case whether the entity predicted for is new or known; a known entity's own history is a legitimate input.
   [^x21e8]: wadden_sea_sibes_macoma_abundance (Andrej, 2026-11-02): grouped by station over all years, not temporal. lt_vehicle_loan_default_prediction (Lennart, 2026-11-05): its use-case override of a split rule was replaced by an amendment.

   **Andrej (2026-11-24):** Before I decide on this, show me a table with years x countries and the no. of samples for each combination as the cells.

   **Answer (AI, 2026-11-24):** survey clusters per country and survey year in the shipped frame (21,454 rows, 18 countries, 19 survey years; an empty cell has no survey). Bold: the 16 country-year cells the shipped split tests (option A), each trained on every earlier year of the other 17 countries (14,231 to 19,133 training rows).

   | Country | 1994 | 1995 | 1996 | 1998 | 1999 | 2003 | 2004 | 2005 | 2006 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | Total |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   | Cameroon |  |  |  |  |  |  | 464 |  |  |  |  |  |  | 577 |  |  |  |  |  | 1,041 |
   | Central African Republic | 141 | 90 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 231 |
   | Cote d'Ivoire |  |  |  | 77 | 63 |  |  |  |  |  |  |  |  | 45 | 296 |  |  |  |  | 481 |
   | Ethiopia |  |  |  |  |  |  |  | 528 |  |  |  |  |  | 571 |  |  |  |  | **622** | 1,721 |
   | Ghana |  |  |  | 221 | 179 |  |  |  |  |  | 404 |  |  |  |  |  | **423** |  | **192** | 1,419 |
   | Guinea |  |  |  |  | 293 |  |  |  |  |  |  |  |  |  | 300 |  |  |  |  | 593 |
   | Kenya |  |  |  |  |  | 399 |  |  |  |  | 181 | 216 |  |  |  |  | **1,585** | **245** |  | 2,626 |
   | Lesotho |  |  |  |  |  |  |  |  |  |  |  | 338 | 57 |  |  |  | **399** |  |  | 794 |
   | Malawi |  |  |  |  |  |  |  |  |  |  |  |  | 827 |  | 140 |  | **140** | **581** | **269** | 1,957 |
   | Mali |  | 98 | 202 |  |  |  |  |  | 405 |  |  |  |  |  | 260 | 153 |  | **177** |  | 1,295 |
   | Mozambique |  |  |  |  |  |  |  |  |  |  |  | 270 |  | 609 |  |  |  |  |  | 879 |
   | Nigeria |  |  |  |  |  | 360 |  |  |  |  | 885 |  | 239 |  |  | 889 |  | **322** |  | 2,695 |
   | Rwanda |  |  |  |  |  |  |  |  |  |  |  |  | 272 | 220 |  |  | **183** | **309** |  | 984 |
   | Senegal |  |  |  |  |  |  |  |  |  |  | 196 | 122 | 158 | 227 | 78 | 122 |  |  |  | 903 |
   | Sierra Leone |  |  |  |  |  |  |  |  |  |  | 350 |  |  |  |  | 435 |  |  |  | 785 |
   | Swaziland |  |  |  |  |  |  |  |  | 205 | 65 |  |  |  |  |  |  |  |  |  | 270 |
   | Tanzania |  |  |  |  |  |  | 232 | 113 |  | 286 | 180 | 42 | 416 | 60 | 513 |  |  | **469** | **139** | 2,450 |
   | Togo |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 129 | **201** |  |  | 330 |
   | **Total** | 141 | 188 | 202 | 298 | 535 | 759 | 696 | 641 | 610 | 351 | 2,196 | 988 | 1,969 | 2,309 | 1,587 | 1,728 | 2,931 | 2,103 | 1,222 | 21,454 |

   - Under A, the test cells come from the three newest survey years: 2014 (6 countries), 2015 (6) and 2016 (4); the smallest cell holds 139 clusters (Tanzania 2016), the largest 1,585 (Kenya 2014).
   - Under B, a test fold holds whole countries, every survey year of each (the Total column: from 231 clusters for the Central African Republic to 2,695 for Nigeria).
   - 10 of the 18 countries have a survey in 2014-2016; Cameroon, the Central African Republic, Cote d'Ivoire, Guinea, Mozambique, Senegal, Sierra Leone and Swaziland have none after 2013, so A never tests them, while B does.
   - Survey years differ by country: no year covers more than 7 countries (2011), and each year from 1994 to 2007 holds 1 to 3 countries.

   **Andrej (2026-11-24, discuss):** I feel like B is also not the right use case fit. Shouldn't it be a grouped-temporal split where the prediction point is one specific year and we have observed some countries for this year and want to predict others that we didn't measure, retrospectively??

   **Answer (AI, 2026-11-24, later):** yes, that is a use case of its own, and the split tree has a leaf for it; added as option D. A tests later years in unseen countries, B countries without any survey; D fills in a year's map for the countries the survey rounds missed, with everything else observed.
   - The walk from the collection type Survey: [SUR.meets] the model predicts for countries of this survey's population in years they were not surveyed, places the survey did not sample inside what it covered → Fill-in step → [FILL.later] the labels arrive with their round: no → [FILL.scattered] the missing country-years lie among surveyed ones (a country's years between its surveys, a year's other countries): scattered → [FILL.units] the unit is the survey round, which has many clusters, and the use case meets new rounds: yes → leaf L-FILL.unit, Grouped · `RetrospectiveFillIn`, whole rounds held out.
   - One reading in that walk is a judgment: the survey round, not the country, is the unit. With the country as the unit the walk ends at random rows, which would put clusters of the very round being filled into training; the use case lacks that whole round.
   - Training side: "retrospectively" lets every other round train, also the same country's later rounds. If a map may only use earlier rounds, the split is A without the country left out, a temporal split by year.
   - Measured (one Slurm job, untuned LightGBM, mean RMSE over the splits; the target's spread is about 0.2):

     | Split | Test rows per split | Overall mean | Same country's mean of other years | LightGBM, shipped inputs | LightGBM, shipped inputs + country |
     |---|---|---|---|---|---|
     | A shipped (16 cells of 2014-16) | 391 | 0.186 | (country not in training) | 0.130 | (country unseen) |
     | B whole countries (3 x 3) | 7,151 | 0.196 | (country not in training) | 0.125 | (country unseen) |
     | D survey rounds (3 x 3) | 7,151 | 0.196 | 0.184 | 0.113 | 0.096 |

   - Under D the country's own average from its other rounds is barely better than the overall mean, so the task does not collapse into a country lookup; the map inputs carry it, and the country as an input adds 0.017.
   - Issues 4 and 5 (population density and night lights from other years than the round) apply under every option; under D a round's own year is known, so they matter as much as under B.

   **Andrej (2026-11-24, discuss):** Did you simply agree with me? Is the source's split and use case a valid predictive task? If yes, we should prefer that over something we made up

   **Answer (AI, 2026-11-24, later):** partly yes: D was added on your framing and led the recommendation without first testing the source's task. Tested now, the source's task holds, so the recommendation is B again.
   - The source's split: Test.csv holds 7 countries not in Train.csv (Angola, Benin, Burkina Faso, DR Congo, Uganda, Zambia, Zimbabwe), each over 1998-2016; the task is a country without surveys, over all years. B reproduces it on the 18 training countries.
   - The source's use case: "filling in the gaps between the more expensive surveys". The words could also mean D, but its test shows the gap it means: countries the surveys do not reach.
   - Valid as a predictive task: an agency without a survey in a country maps its local wealth, the stated aim of satellite poverty mapping (Jean et al. 2016, Yeh et al. 2020); every input is an Africa-wide layer that exists for an unsurveyed country; the country holdout tests that transfer. The one condition, a wealth index comparable across countries, is the approximate fit already accepted in issue 2.
   - D's lower error (0.113 against 0.125) is no argument for it: the same country's other rounds in training make the task easier, not truer to a use.

   **Resolved (2026-11-24, Andrej):** B, applied. `dataset.py`: `temporal`, `TEST_YEARS` and `_make_splits` removed; `grouping = Grouping(on="country", ...)` (default grouped splits, 3 folds by country, 3 repeats, 6 countries per test fold; changed the same day to leave one country out on the 10 countries surveyed in 2014-2016, issue 8 C); `ID` dropped in `_clean`, `country` only the group; `time_basis = TimeBasis("UnseenGroup", ...)` and `split_leaf = "L-PLACE.groups"`; question, use case, split, changes, fit reason, splits comment and the split-walk bullet rewritten; the evaluation and SPLIT-3 override bullets removed; the masking of future construction periods, its check and its decision table kept. Record: `required_split` Grouped only, `Non-IID (Temporal)` dropped, CC line. Checks (Slurm): `dataset check` 0 errors, 1 warning (`groups_test_groups_few`, issue 8), the earlier warning on fields missing in training is gone; no test row has a feature copy in training (9 splits); task probes on 5 of 9 splits: random forest RMSE 0.119, LightGBM 0.124, linear 0.129, night lights alone 0.126, training mean 0.198 (random forest beats the dummy on 5 of 5); group probe: R² 0.58-0.59 on unseen countries against 0.77 on a random split, so the signal carries across countries. Issues H, 6 and 7 lapse.

4. **Mask population density before 2015, like construction in 2000-2014?**

   - **Problem:**
     - Population density at the same place does not change between surveys up to 22 years apart, so one read serves every row.
     - It responds to construction from 2000-2014 as strongly as the 2015-2019 land cover does, so it is most likely GHS-POP's 2015 epoch, allocated on the 2014 built-up layer that the definition masks.
     - It stays unmasked on the 18,129 rows before 2015, against the curator's rule that a field describing a later state is not allowed[^x21col1].
   - **Effect on the task:** training rows before 2015 pair a 2015 population with an older wealth label; the test rows of 2014-2016 are roughly contemporary, so nothing leaks to a test label.
   - **Experiments:**
     - Same-place pairs (1,204 pairs of one country agreeing within 0.3 km on both distances and 0.005 on pre-1975 built-up), mean later-minus-earlier difference:

       | Years between surveys | Pairs | Night lights (log1p) | Population (log1p) | Target |
       |---|---|---|---|---|
       | 0 | 414 | -0.002 | -0.007 | +0.001 |
       | 1-3 | 197 | -0.020 | -0.035 | +0.016 |
       | 4-7 | 421 | -0.027 | -0.015 | +0.066 |
       | 8-12 | 118 | +0.010 | +0.032 | +0.124 |
       | 13+ | 54 | -0.016 | -0.017 | +0.158 |

     - Log of the layer regressed on built-up area (column audit, fit 1), weights:

       | Layer | Built by 1990 | Added 1990-2000 | Added 2000-2014 |
       |---|---|---|---|
       | Population density | 0.943 | 0.009 | 0.463 |
       | Urban land cover 2015-2019 (control) | 0.729 | 0.114 | 0.319 |

     - LightGBM with one fixed configuration (400 trees, not tuned) on the 16 shipped cells, 3 seeds, mean RMSE (lower is better):

       | Variant | Mean RMSE | Cells better than shipped |
       |---|---|---|
       | Shipped | 0.1231 | |
       | Population masked before 2015 | 0.1225 | 9 |
       | Population dropped | 0.1216 | 12 |

     - Population density 0 marks places with no construction through 2014 (claim audit): of the rows before 2014 with no built-up by 2000, the rows with population 0 almost never gain built-up in 2000-2014, so the column partly reveals the masked field.

       | Rows before 2014, no built-up by 2000 | Built 2000-2014 = 0 | Built 2000-2014 > 0 |
       |---|---|---|
       | Population = 0 | 1,098 | 1 |
       | Population > 0 | 622 | 756 |

   - **Consistency:** construction from 2000-2014 is masked before 2014 and land cover is dropped for the same reason; issue 1 (resolved 2026-11-02) asked for a repair once a later-state measurement is shown[^x21col2].
   - **Panel:** the column audit (2026-11-21), on the source's Train.csv (a public GitHub copy with the curator's SHA-256); advocate, critic and mediator agree that the answer follows issue 3.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep for all rows (implemented) | No change | no new missing values | a later state on 18,129 rows; breaks the masking rule used for built-up and land cover |
     | B | Mask before 2015 | Missing where the year is before 2015, as for construction in 2000-2014 | the same rule as the other masks; keeps the value where it is current | the 2015 epoch is inferred, not documented; under the joint split population is missing in training on 12 of 16 cells (all of 2014 and 2015), so there B works like C; adds a third column to the check warning (issue 6) |
     | C | Drop | Remove the column, as for land cover | simplest | loses a valid value on the rows of 2015 and 2016 |

   - **Recommendation:** B if issue 3 changes to B, since population is then present on the 2015-16 rows on both sides of every fold; C if the joint split stays, since there B leaves the column out of training on 12 of 16 cells and C scores best (12 of 16 cells better). **Decision:** keep A, or change to B or C?

   **Notes for the AI:** For B, add `"ghsl_pop_density": 2015` to `PERIOD_ENDS` (the loop masks year < end), and extend the curation comment: "Mask ghsl_pop_density before 2015: at the same place it does not change across surveys up to 22 years apart, and it responds to 2000-2014 construction like the 2015-2019 land cover (log coefficient 0.46 vs 0.32), so it is GHS-POP's 2015 epoch." `_extra_checks` and `_decisions` follow `PERIOD_ENDS`; re-run `dataset check` and the leak probes. For C, add it to `drop_columns`. Night lights are issue 5. Evidence: the run folder (explore2.py, explore4.py, explore5.py).

   [^x21col1]: **LEAK-10** (Must), the clause on values read at a later pull: blanked where the late cells can be located (here by survey year); the curator's call of 2026-10-31: "fields describing a later state or a period after the row's survey/prediction time are not [acceptable]".
   [^x21col2]: Issue 1, resolved 2026-11-02 (Myunghwan): "Evidence of an actual later-state measurement still requires repair."

   **Andrej (2026-11-24, discuss):** Since this is now a retrospective grouped task, it should be fine to keep, right?

   **Answer (AI, 2026-11-24):** not by itself: the split is grouped by country, which says where the test goes, not when the actor predicts. What decides this issue, issue 5 and the masks already applied is the prediction point, and the record holds two.
   - Targeting in the survey's own year (the use case's "to inform geographic targeting of support"; the prediction-point bullet's "same-year or earlier-state inputs"): the agency holds only that year's layers, so a 2015 read on a 1998 cluster is a later state[^x24e2]. Then B stays right here and the construction masks stay.
   - Mapping past survey years today (the source's aim, "filling in the gaps between the more expensive surveys"): the agency holds every layer as read today, so nothing needs masking. The source itself shipped one read of each layer on every year, its 2015-2019 land cover on rows from 1998.
   - The record's "no change at the same place" check does not settle it: population and lights are one read used on every row, so they cannot change between surveys of a place.
   - So the choice is the use case, and it carries more than this column:

     | | Prediction point | Population density (this issue) | Night lights (issue 5) | Construction masks (applied) | Four land-cover columns (dropped) |
     |---|---|---|---|---|---|
     | a | In the survey year, for targeting then (as written) | mask before 2015 (B) | keep (A): no link to a later state measured | stay | stay dropped |
     | b | Today, mapping the survey years (the source's gap-filling) | keep (A) | keep (A) | removed: every layer as read today | restored |

   - Recommendation: b, the source's framing, which its own feature release follows; on b the use case and the prediction-point bullet are rewritten to an agency mapping past wealth with today's layers, and Myunghwan's call of 2026-10-31 against later states is replaced, for this use case only. a keeps the record's targeting use, which a contemporaneous agency would have; then this issue takes B. Either way, the decision is yours, and the check and probes run again after it.

   [^x24e2]: **LEAK-10** (Must): attributes looked up after the outcome are out, "unless the data shows they did not change".

   **Andrej (2026-11-24):** I agree with use case b

   **Resolved (2026-11-24, Andrej):** A, under use case b, applied: the prediction point is today, an agency mapping the past survey years of a country without surveys of its own with every layer as read today (the source's gap-filling framing), so population density stays on every row. `dataset.py`: `use_case`, `known`, `changes`, `fit_reason` and the prediction-point bullet rewritten to that framing; population density gets a `Potential leak, kept on purpose:` note (most likely GHS-POP 2015, kept because the agency maps today); `PERIOD_ENDS`, the masking in `_clean`, its check (`_extra_checks`) and its decision table (`_decisions`) removed, with the "Temporal repair" bullet; `LAND_COVER` no longer dropped, so the four land-cover columns are back (16 inputs). Myunghwan's call of 2026-10-31 against later states is replaced for this use case (CC line). Checks (Slurm): `dataset check` 0 errors, 0 warnings (3 accepted), 1 info (129 conflicting duplicate rows, unchanged); leak probe: no test row has a feature copy in training (10 splits); task probes on 10 of 10 splits: random forest RMSE 0.110, LightGBM 0.111, linear 0.117, single feature 0.126, training mean 0.192, before 0.119 / 0.121 / 0.126 / 0.129 / 0.196 with the masks and without land cover.

5. **Keep night lights for every survey year, mask them before 2012, or drop them?**

   - **Problem:**
     - Night lights at the same place do not change across surveys up to 22 years apart, so one read of an undated layer serves rows from 1994 to 2016.
     - The values reach 383, above the raw DMSP scale of 0-63, which fits VIIRS (from 2012 on) or a radiance-calibrated DMSP composite, but the source names no product.
     - The same question led to masking construction of 2000-2014 and is open for population (issue 4), so lights need an answer of their own[^x21n1].
   - **Effect on the task:** training rows of earlier years pair an older wealth label with a lights read that may be later; no test label is reached, and at the same place the read does not rise with the target.
   - **Experiments:**
     - Lights against population, from the same-place pairs of issue 4 and the claim audit:

       | Measure | Night lights | Population density |
       |---|---|---|
       | Mean log change at the same place, 13+ years apart (target +0.158) | -0.016 | -0.017 |
       | Decodes a masked field | none shown | 0 means no 2000-2014 construction in 1,098 of 1,099 rows |

     - Log of each layer regressed on built-up area (column audit; fit 1 splits built-up before 2000 into before 1990 and 1990-2000, fit 2 keeps it as one term). Weight on construction added 2000-2014:

       | Layer | Fit 1 | Fit 2 |
       |---|---|---|
       | Night lights | 0.119 | 0.002 |
       | Population density | 0.463 | 0.29 |
       | Urban land cover 2015-2019 (masked as a later read) | 0.319 | 0.225 |

     - What the column is worth (16 shipped cells, mean RMSE, lower is better):

       | Variant | Mean RMSE | Cells |
       |---|---|---|
       | Night lights alone, isotonic fit | 0.1232 | |
       | Tuned LightGBM, all inputs | 0.1135 | |

     - Dropping lights (untuned LightGBM, 3 seeds, 16 shipped cells): RMSE +0.0134 against the shipped inputs, worse on 16 of 16 cells.

   - **Consistency:** construction of 2000-2014 is masked and land cover dropped as later reads; water is kept because it describes stable water bodies that the data shows did not change[^x21n2].
   - **Panel:** the advocate keeps lights, since the read does not follow later wealth, weighs little on later construction and masking it would remove it from most training rows; the critic answers that population is just as flat at the same place and that the construction weight is unstable between two fits.
   - **Unknown:** the product name and year of the lights layer; the source would settle it.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep for every year (implemented) | No data change; the notes get a `Potential leak, kept on purpose:` line with the reason and the unknown epoch | the one input that carries most of the signal stays; no measured link to a later state | an undated read on rows up to 22 years older; differs from the masks on construction and possibly population |
     | B | Mask before 2012 | Missing where the year is before 2012, the start of VIIRS | follows the masking rule if the layer is VIIRS | the epoch is inferred; removes lights from most training rows; close to dropping them |
     | C | Drop | Remove the column | no epoch question left | worse on 16 of 16 cells; loses a valid read on the recent rows |

   - **Recommendation:** A: unlike population, the lights read puts little or no weight on construction after 2000 and reveals no masked field, so nothing shows a later state; masking it would rest on an inferred epoch. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On A, replace in the water/population/lights bullet of `curation_comments` the sentence on lights with "Potential leak, kept on purpose: nighttime_lights is one read of an undated layer (values up to 383, so VIIRS from 2012 or a radiance-calibrated DMSP composite) used on rows from 1994 on. At the same place it does not change over 13 or more years (log change -0.016) while the target rises by +0.158, and it shows no link to a masked field, so it carries no later state of the label; revisit if the source names the product." On B, add `"nighttime_lights": 2012` to `PERIOD_ENDS` with a curation bullet; on C, add it to `drop_columns`. Re-run `dataset check` and the leak and task probes after B or C.

   [^x21n1]: **LEAK-10** (Must), the clause on values read at a later pull: blanked where the late cells can be located; CC 2026-10-31 (Myunghwan): "fields describing a later state or a period after the row's survey/prediction time are not [acceptable]".
   [^x21n2]: **LEAK-10** (Must): attributes looked up later are dropped, or kept "where the data shows they did not change".

   **Andrej (2026-11-24, discuss):** Since this is now a retrospective grouped task, it should be fine to keep, right?

   **Answer (AI, 2026-11-24):** it follows issue 4's answer of today: the lights read is kept (A) under either prediction point, since no link to a later state was measured; under the targeting reading (a) A rests on that measurement, under the gap-filling reading (b) on the actor holding today's layers. The decision on the prediction point is in issue 4.

   **Andrej (2026-11-24):** I agree with use case b

   **Resolved (2026-11-24, Andrej):** A, under use case b (issue 4): night lights stay on every row, as read today. The water/population/lights bullet of `curation_comments` now carries the note "Potential leak, kept on purpose: nighttime_lights is one read of an undated layer (values up to 383, so VIIRS from 2012 or a radiance-calibrated DMSP composite) used on rows from 1994 on; kept because the agency maps today with today's read", with the same-place measurement (log change -0.016 over 13 or more years against a target rise of +0.158). Random forest ahead of night lights alone on 9 of 10 test countries (mean lead 0.0105 RMSE; Malawi the exception), before 8 of 10 (0.0056).

7. **Count the shipped split's comparison with night lights alone as the models ahead (applies only if issue 3 stays A)?**

   - **Problem:**
     - A dataset on which one raw input matches tuned models measures little beyond that input, so the models have to be ahead of the best single input on most splits[^x21n4].
     - On the 16 shipped cells the tuned models beat a fit on night lights alone on 10 cells, by a mean that is 1.5 standard errors, between "matches" and "beats".
     - Under issue 3 B this question does not arise: the best model per split is ahead on 9 of 9 splits (tuned LightGBM on 8 of 9).
   - **Effect on the task:** read as a match, the dataset becomes a candidate to drop as trivial; read as ahead, it stays.
   - **Experiments:** paired, night lights alone minus the methods (RMSE, positive when the methods are better); the full tables are in issue 3.

     | Compared with | Mean difference | SE | Cells where the methods are better |
     |---|---|---|---|
     | Tuned LightGBM | +0.0098 | 0.0066 | 10 of 16 |
     | Best family per cell | +0.0150 | 0.0054 | 10 of 16 |

     - Lights alone wins the six cells with large country offsets (Malawi 2014, 2015 and 2016, Rwanda 2014 and 2015, Ethiopia 2016): the fitted models carry the training countries' offsets into a new country.
     - The gain is about 8% of the error; the domain practitioner's within-country rank correlation of 0.68-0.70 shows the full models rank places, and lights alone was not measured on a ranking.
   - **Consistency:** california_house_prices_2020 was kept with the listed price as the one input that carries most of the signal because the methods beat it; ljubljana_breast_cancer was retired because a fixed index matched the methods[^x21n5].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Models ahead, keep (implemented) | No change | lights are the one input that carries most of the signal and the methods add to it on most cells | the lead is 1.5 standard errors and 10 of 16 cells |
     | B | A match | The dataset becomes a candidate to drop as trivial, for the curator's weighing | strict reading of a small lead | discards a real gain of about 8% of the error |

   - **Recommendation:** A, if issue 3 stays A: the methods are ahead on most cells, and the cells they lose are those of a known country-offset effect. **Decision:** keep A, or change to B?

   [^x21n4]: **TP-4** (Must): the methods must beat the natural core on most splits; one that only matches them makes the dataset a candidate to drop, and the curator decides.
   [^x21n5]: Cases of TP-4 in task_probes.md: california_house_prices_2020 kept (2026-10-06); ljubljana_breast_cancer retired, `Trivial` (2026-11-10).

   **Resolved (2026-11-24, AI):** no longer applies: issue 3 is B (Andrej, 2026-11-24), whole countries over all years; this item concerned only the joint split by year and country.

6. **Accept the check warning that two settlement fields are missing in training in the 2014 cells (applies only if issue 3 stays A)?**

   - **Problem:**
     - Under the joint split the check warns that `ghsl_built_2000_to_2014` and `ghsl_not_built_up` are missing on every training row of the 2014 cells and present on their test rows.
     - Our own mask causes it: both fields describe construction through 2014, so they are blank on all earlier rows, and the 2014 cells train only on earlier rows.
     - Under issue 3 B every fold spans all years, so the warning should go and this issue falls away.
   - **Effect on the task:** in the six 2014 cells the models never see the two fields in training and meet them only in test; under issue 4 B population would also be missing in training, on all 12 cells of 2014 and 2015.
   - **Experiments:** training rows with the two fields observed (claim audit):

     | Test year | Cells | Training rows with the fields observed |
     |---|---|---|
     | 2014 | 6 | 0 |
     | 2015 | 6 | 1,346-2,931 |
     | 2016 | 4 | 4,313-5,034 |

   - **Consistency:** anes_voting_2026 and delivery_eta_1m accepted this warning with the curator's decision, each for a field the deployed model met the same way[^x21n3].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave it open (implemented) | The warning stays in every check run | no decision taken for the curator | the check stays unclean |
     | B | Accept with the reason | An entry in `accepted_check_warnings` | the mask is correct and the model of 2014 met the same gap | none beyond a written reason |
     | C | Drop the two fields | Remove them from every row | no warning | loses valid values on 2014-2016 rows |

   - **Recommendation:** B, if issue 3 stays A: the gap is the correct mask, not a recording change. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On B, `accepted_check_warnings = {"splits_feature_missing_in_test": ("Decided (<curator>, <date>, review issue 6, B): ghsl_built_2000_to_2014 and ghsl_not_built_up describe construction through 2014 and are masked before 2014, so the 2014 cells train without them; a model fit in 2014 met the same gap (curation_comments, 'Temporal repair').")}`. Ask only if issue 3 stays A; under B re-run `dataset check` to confirm the warning is gone.

   [^x21n3]: The check `splits_feature_missing_in_test` is accepted only with the curator's decision (definitions.md).

   **Resolved (2026-11-24, AI):** no longer applies: issue 3 is B (Andrej, 2026-11-24), whole countries over all years; this item concerned only the joint split by year and country. The check warning on fields missing in training is gone with it (`dataset check`, 2026-11-24).

8. **Accept the check warning that each test fold holds only 6 of the 18 countries?**

   - **Problem:**
     - Under issue 3 B every test fold holds 6 whole countries, so a fold's score rests on 6 independent units, and the check warns (`groups_test_groups_few`).
     - The data has 18 countries, so no fold count removes it: more folds give fewer countries per fold.
   - **Background:** the check asks to keep such a dataset only if its signal across groups is real, and to accept the warning with that reason[^x24e1].
   - **Experiments:** group probe (Slurm, 2026-11-24): R² on unseen countries 0.58-0.59 (ridge, random forest, LightGBM) against 0.77 for LightGBM on a random split; task probes: random forest beats the training mean on 5 of 5 splits (RMSE 0.119 against 0.198).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave it open (implemented) | No acceptance; the warning stays in the README | nothing decided by default | the dataset cannot ship with an unaccepted warning |
     | B | Accept with the reason | `accepted_check_warnings` names the measured signal across countries | the signal is real on unseen countries; the source's own test has 7 countries | a fold's score stays noisy; benchmarks should read it over all 9 splits |
     | C | Leave one country out, the 10 countries with a 2014-16 survey | 10 splits, each holding out one of Ethiopia, Ghana, Kenya, Lesotho, Malawi, Mali, Nigeria, Rwanda, Tanzania, Togo with all its years; the other 17 countries train | each split trains on 17 countries; a per-country score | 1 country per split, so the warning holds more strongly and still needs accepting; 8 countries never tested; the later survey adds no later test, since every year of the country is tested; per-split RMSE spread 0.014 against 0.005 |
     | D | Leave one country out, all 18 | 18 splits, one country each | every country tested once; each split trains on 17 countries (RMSE 0.120 against 0.124) | 1 country per split; per-split RMSE spread 0.025 against 0.005, up to 76% of a split's squared error one offset for the country; 18 splits instead of 9 |

   - **Recommendation:** B: the group probe shows the signal holds on countries the model never saw, and the 3 x 3 folds score each split over 6 countries, which keeps one country's offset from deciding a split. **Decision:** keep it open (A), accept it (B), or change to C or D?

   **Notes for the AI:** On B, `accepted_check_warnings = {"groups_test_groups_few": "Decided (Andrej, <date>, review issue 8, B): 18 countries give 6 per test fold; the signal carries across countries (group probe R^2 0.58-0.59 on unseen countries against 0.77 on a random split), and the source tests 7 unseen countries itself."}`; re-run `dataset check` (Slurm).

   [^x24e1]: The check's hint: "Keep the dataset only if its signal across groups is real (group_probes.py), and accept the warning with that reason."

   **Andrej (2026-11-24, discuss):** Why don't we do leave one country out evaluation for nine countries that were measured in the later surveys to get the 9 splits?

   **Answer (AI, 2026-11-24):** it moves the warning the wrong way: a split then holds one country instead of six, and its score is mostly that country's offset. Added as option C (and all 18 countries as D); B stays recommended. Measured (Slurm, untuned LightGBM; night lights alone a LightGBM on that one column):

     | Split | Splits | Countries tested | LightGBM RMSE, mean | Spread of the split RMSE (sd) | Beats night lights alone |
     |---|---|---|---|---|---|
     | Shipped 3 x 3 country folds | 9 | 18, three times each | 0.124 | 0.005 | 4 of 9 |
     | C: one country out, the 10 with a 2014-16 survey | 10 | 10 | 0.119 | 0.014 | 7 of 10 |
     | D: one country out, all 18 | 18 | 18, once each | 0.120 | 0.025 | 12 of 18 |

   - 10 countries, not 9, have a survey in 2014-2016.
   - In a one-country split the mean error over the country is a large part of the error: 76% of the squared error for Sierra Leone, 40-55% for Ethiopia, Malawi and Rwanda. Over six countries it averages out (at most 16% in a fold).
   - Choosing the countries surveyed later adds no later test: the held-out country is tested on all its years, 1994 to 2016.
   - Not part of this question, but measured here: untuned models only match night lights alone on the country folds (LightGBM 0.124 against 0.125, ahead on 4 of 9; random forest 0.1244 against 0.1253, ahead on 5 of 9). Tuned, they lead (the panel of 2026-11-21: tuned LightGBM +0.0059 RMSE, SE 0.0015, ahead on 8 of 9; the best family per split +0.0085, SE 0.0011, 9 of 9), so the rule that the methods beat the best single input (TP-4) holds, by a margin of 5-7% of the error.

   **Andrej (2026-11-24, chat):** Why is it even an issue that we have few test countries, this is an UnseenGroup task so it is fine.

   **Andrej (2026-11-24, chat):** I want to implement the leave one country out split on the 10 countries from the latest surveys. This is more accurate since 3x3 CV produces too similar splits

   **Resolved (2026-11-24, Andrej):** C, applied (it replaces the B of earlier today; the warning on few test countries stays accepted, with one country per split). `_make_splits` holds out each of the 10 countries surveyed in 2014-2016 (Ethiopia, Ghana, Kenya, Lesotho, Malawi, Mali, Nigeria, Rwanda, Tanzania, Togo) once with all its survey years, one repeat of 10 folds; the other 17 countries train (18,759 to 21,124 rows). Grouping definition, task summary split, splits comment and split-walk bullet rewritten. Two warnings follow from the split and are accepted with it: 5,183 rows (24.2%, the 8 other countries) never tested, and 1 x 10 instead of the protocol's 3 x 3 (the splits comment gives the reason). Checks (Slurm):

     | Check | Result |
     |---|---|
     | `dataset check` | 0 errors, 0 warnings after the acceptances (3 accepted) |
     | Task probes (10 splits), RMSE | random forest 0.119, LightGBM 0.121, linear 0.126, night lights alone 0.129, training mean 0.196; random forest ahead of the dummy on 10 of 10 |
     | Task probe flags | `unstable` (skill SE 0.085) and `no_spread`: the per-country swing one country per split brings; a flag is a question for the tuned benchmark |
     | Random forest against night lights alone (untuned) | ahead on 8 of 10 countries, mean lead 0.0056 RMSE |
     | Group probe, R² per row | -0.43 to -0.55: with one country per fold R² is taken against that country's own mean, so the country's offset counts as error (up to 76% of a split's squared error) |

9. **Add the 7 test countries of the source, with their labels recovered from the source table (25 countries instead of 18)?**

   - **Problem:**
     - The competition's data is the cluster table of Yeh et al. 2020 (`dhs_wealth_index.csv`, sustainlab-group/africa_poverty, MIT, public since 2020-04-09): Train.csv and the hidden Test.csv together hold every cluster of that table that has coordinates, 28,648 rows in 25 countries (cluster counts match in 95 of 96 country-years)[^x24e3].
     - The table also holds the wealth labels of the 7,194 Test.csv rows (Angola, Benin, Burkina Faso, DR Congo, Uganda, Zambia, Zimbabwe, 1998-2016), which the competition never released.
     - The shipped dataset therefore uses 18 of the 25 countries the source prepared, and leaves out exactly the countries the source chose to test on.
   - **Background:**
     - The target is that table's `wealthpooled` (an asset index from one principal component pooled over all surveys, averaged per cluster), min-max rescaled over the 25 countries: within each country-year, Target = 0.24504 × wealthpooled + 0.34366, deviating by at most 0.0012. This answers issue 2's open question: the index is comparable across countries by its pooling.
     - Zindi's features were extracted at the table's (displaced) coordinates: the distance to the capital matches the haversine distance with correlation 0.99999.
     - Test.csv has no cluster id or coordinates, so its labels need a row join: matching on the distance to the capital alone recovers the right label for only 8-38% of Train.csv rows; a second feature recomputed at the coordinates (distance to the shoreline, a built-up value) would be needed, validated on Train.csv against its known Target.
     - Surveys of the table without coordinates (CM1998, KE1998, MZ1997, RW2013, SN2006, SN2015, TZ2003, UG1995, and 5 more countries) cannot be added: their features cannot be computed.
   - **Effect on the task:** 25 countries and 28,648 clusters instead of 18 and 21,454; the leave-one-country-out test (issue 8) could hold the countries surveyed in 2014-2016 among 25.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep Train.csv (implemented) | 18 countries, the released labels | no new code; labels exactly as released | leaves out the 7 countries the source tests on |
     | B | Add Test.csv with recovered labels | Build and validate the row join (recompute one or two features at the source table's coordinates, assign within country × year × urban, check on Train.csv), rescale with the fitted formula, ship 25 countries | the source's whole task; more countries per split | a join to build and prove; recovered labels differ from Zindi's hidden values by up to 0.0012; the coordinates are DHS data (issue 10) and must not ship |
     | C | Rebuild from the source table | Compute every feature at the table's coordinates from the public layers (GHSL, VIIRS, distances), with the documented survey ids and years | fully documented provenance and features | a new dataset rather than a re-source; much more work |

   - **Recommendation:** B if issue 10 keeps the dataset: it ships the source's own task, its 25 countries, with the join proven on the 21,454 known labels before any recovered label is used. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** On B, first a Slurm job: download `dhs_wealth_index.csv` (pin its commit), recompute the distance to the shoreline (or a GHSL layer) at its coordinates, match Train.csv rows within country × year × urban by the two distances, and report the share of Train.csv rows whose matched label equals Target within 0.0012; only above 99.9% go on to Test.csv. Never ship coordinates or survey cluster ids.

   [^x24e3]: Measured 2026-11-24 from the public files: Zindi Train.csv and Test.csv against the repository's `data/dhs_wealth_index.csv` (commit cb769c74, "Add clean DHS CSV", 2020-04-09; documented in its `data/README.md`).

   **Andrej (2026-11-24, change):** Option B: Add Test.csv with recovered labels.

   **Answer (AI, 2026-11-24):** step 1 of the notes, run: the join finds the right cluster for nearly every Train.csv row, but the share within 0.0012 is 97.43%, below the 99.9% bar, so Test.csv is not added; 18 countries ship and this issue stays open.
   - The join: `data/dhs_wealth_index.csv` of sustainlab-group/africa_poverty at commit cb769c744872e52c35f9c60e94b0dc2a696d389a (SHA-256 e68c0466…efba8; the file is in the tree at that commit); the distance to the capital recomputed as an ellipsoidal (WGS84) distance from each country's capital point fitted to the released distances, and the distance to the shoreline from Natural Earth's coastline (nvkelso/natural-earth-vector at a726d637, 10 m, 50 m and 110 m tried); rows assigned within country × year × urban/rural by both distances (a one-to-one assignment, not nearest neighbours). Zindi's Test.csv in the warehouse equals the public copy in simiel/economic-well-being-prediction-competition (SHA-256 e1d61ea1…49ab).
   - The distance to the capital is recomputed exactly: every matched pair agrees within 0.002 km (haversine distances were off by up to 14 km). The shoreline is not: Natural Earth's coastline differs from the source's by a median 2.4-8.7 km, so it only breaks near-ties.
   - Refit on Train.csv: Target = 0.245034 × wealthpooled + 0.343664 (given 0.24504 and 0.34366).

     | Train.csv rows (21,454) | Rows | Share |
     |---|---|---|
     | Matched label within 0.0012 of Target (the bar) | 20,903 | 97.43% |
     | Within 0.0014 (the right cluster) | 21,321 | 99.38% |
     | Wrong cluster: Central African Republic 1994-95, rows at shared locality points | 131 | 0.61% |
     | Wrong cluster: Cameroon 2004, two urban clusters 0.0012 km apart in distance to the capital | 2 | 0.01% |

   - Why 0.0012 fails: Zindi's Target is the rescaled `wealthpooled` plus a per-row deviation spread evenly over about ±0.0013 (sd 0.0007 in every country-year, mean 0; a separate affine fit per country-year leaves up to 0.0014). So 418 right matches land between 0.0012 and 0.0013, and no join can pass a 0.0012 bar on all rows.
   - Why the 131 fail: the 41 locality points of the Central African Republic 1994-95 survey (issue 3's 129 conflicting duplicates) hold several clusters at one coordinate, so every input is equal and no recomputed feature can tell their labels apart; the assignment there is arbitrary (42 of 173 such rows happen to land on the right cluster).
   - Test.csv: all 7,194 rows match with the distance to the capital within 0.002 km, and none sits at a shared coordinate, so the failure causes seen on Train.csv do not occur there; recovered labels would differ from Zindi's hidden values by up to about 0.0013, the deviation Zindi added.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep 18 countries (implemented) | Train.csv only, the bar of the notes not met | labels exactly as released | leaves out the 7 countries the source tests on |
     | b | Add Test.csv on a bar matched to the data | Accept the join when the right cluster is found (within 0.0014) on the rows outside shared coordinates (21,279 of 21,281); ship 25 countries | the source's whole task; the join is validated on 99.38% of rows, and Test.csv has no shared coordinates | recovered labels differ from Zindi's hidden values by up to 0.0013; the bar is set after the measurement |
     | c | Rebuild from the source table | Compute every feature at the table's coordinates | documented provenance | a new dataset; much more work |

   - Recommendation: b, if the curator accepts a bar set on what the measurement shows: the join is exact up to Zindi's added deviation and to the CAR locality points, which Test.csv does not have. **Decision:** keep a, or change to b or c?

   **Andrej (2026-11-24, discuss):** Reply (b): Add Test.csv on a bar matched to the data

   **Resolved (2026-11-24, Andrej):** b, applied: Test.csv joins with labels recovered from the source table, on a bar matched to the data, and leave one country out (issue 8) now runs over 25 countries. `dataset.py`: a `_prepare_raw_files` step (`prepared_raw_files = ("Test_labelled.csv", "join_check.csv")`) checks the SHA-256 of Train.csv, Test.csv (e1d61ea14428f23643547b5a322ffc9015e4df0fc9bb798ec675cf2475c149ab), `data/dhs_wealth_index.csv` of sustainlab-group/africa_poverty at commit cb769c74 (e68c0466…efba8) and Natural Earth's 50 m coastline at a726d637 (271f1c4c…a283), all downloaded by the recipe in `download_description` (the build reads local files only); it assigns each Zindi row one-to-one to a cluster within country × year × urban by the distance to the capital (WGS84 ellipsoid, a capital point fitted per country), the shoreline distance breaking near-ties, as the earlier run did, and writes the accepted Test.csv rows with Target = 0.245034 × wealthpooled + 0.343664 (refit on Train.csv). The bar: a match counts only when the distance to the capital agrees within 0.002 km, no second cluster of the cell agrees as well, and no other cluster sits at the same coordinate; the build stops if fewer than 99.9% of accepted Train.csv matches give the right cluster. Train.csv rows keep their released Target. No coordinates, survey ids or cluster ids ship, and no source indicator: the framework has no non-input column besides the target, the group and the metric's scoring columns, and a row's file follows from its country. `TEST_COUNTRIES` is now the 16 countries surveyed in 2014-2016; task summary (row, split, changes, fit reason), time basis, grouping definition, splits comment, the split walk and the curation bullets (the join, the recovered labels, the bar and their deviation; counts measured again on 28,618 rows) rewritten; the two accepted split warnings carry the new numbers. Results (Slurm):

     | Join | Train.csv (labels known) | Test.csv |
     |---|---|---|
     | Rows | 21,454 | 7,194 |
     | Matched within 0.002 km of the distance to the capital | 21,454 | 7,194 (largest gap 0.0018 km) |
     | Right cluster (recovered label within 0.0014 of Target) | 21,321 (99.38%) | not known (hidden) |
     | At a shared coordinate | 173 (Central African Republic 1994-95) | 0 |
     | Second cluster within 0.002 km (near-tie) | 135 outside the shared points (133 of them right anyway) | 30 (Angola 9, Uganda 11, Benin 6, Burkina Faso 2, Zimbabwe 2) |
     | Accepted by the bar | 21,146, all the right cluster | 7,164, added with recovered labels |

     | Country | Train.csv rows | Test.csv rows (recovered labels) | Tested | Random forest RMSE | Night lights alone RMSE |
     |---|---|---|---|---|---|
     | Angola | 0 | 846 | yes | 0.1391 | 0.1478 |
     | Benin | 0 | 740 | no | | |
     | Burkina Faso | 0 | 995 | yes | 0.1025 | 0.1118 |
     | Cameroon | 1,041 | 0 | no | | |
     | Central African Republic | 231 | 0 | no | | |
     | Cote d'Ivoire | 481 | 0 | no | | |
     | DR Congo | 0 | 785 | yes | 0.1033 | 0.1207 |
     | Ethiopia | 1,721 | 0 | yes | 0.1106 | 0.1412 |
     | Ghana | 1,419 | 0 | yes | 0.1132 | 0.1427 |
     | Guinea | 593 | 0 | no | | |
     | Kenya | 2,626 | 0 | yes | 0.1127 | 0.1268 |
     | Lesotho | 794 | 0 | yes | 0.1010 | 0.1145 |
     | Malawi | 1,957 | 0 | yes | 0.1439 | 0.1168 |
     | Mali | 1,295 | 0 | yes | 0.1034 | 0.1205 |
     | Mozambique | 879 | 0 | no | | |
     | Nigeria | 2,695 | 0 | yes | 0.1340 | 0.1457 |
     | Rwanda | 984 | 0 | yes | 0.0946 | 0.0953 |
     | Senegal | 903 | 0 | no | | |
     | Sierra Leone | 785 | 0 | no | | |
     | Swaziland | 270 | 0 | no | | |
     | Tanzania | 2,450 | 0 | yes | 0.1143 | 0.1212 |
     | Togo | 330 | 0 | yes | 0.0878 | 0.1042 |
     | Uganda | 0 | 1,573 | yes | 0.0796 | 0.0952 |
     | Zambia | 0 | 1,038 | yes | 0.1243 | 0.1391 |
     | Zimbabwe | 0 | 1,187 | yes | 0.1392 | 0.1459 |
     | Total | 21,454 | 7,164 | 16 of 25 | 0.1127 (mean) | 0.1243 (mean) |

     | Check (Slurm, 2026-11-24) | Result |
     |---|---|
     | `dataset check` | 0 errors, 0 warnings after the acceptances (3 accepted), 1 info (129 conflicting duplicate rows, the Central African Republic locality points, unchanged) |
     | Task probes (16 splits), RMSE | LightGBM 0.110, random forest 0.111, linear 0.118, single feature (night lights, chosen on all 16) 0.123, training mean 0.200; LightGBM ahead of the dummy on 16 of 16; flag `no_spread` (random forest - linear +0.030, paired SE 0.024), as before |
     | Random forest against night lights alone (untuned) | ahead on 15 of 16 countries, mean RMSE 0.1127 against 0.1243 (lead 0.0116); Malawi the exception, as before |
     | Country offset share of a split's squared error (random forest) | 0.1% (Lesotho) to 53% (Malawi), mean 17% |
     | Group probe | LightGBM R² 0.60 ± 0.21 on held-out countries against 0.78 on a random split; per row -0.20 to -0.31 (R² against each country's own mean) |
     | Leak probe | 0 of 22,695 test rows with a feature copy in training (16 splits) |

   - Tested now: Angola, Burkina Faso, DR Congo, Uganda, Zambia and Zimbabwe (6 of the source's 7 test countries; Benin's surveys are 2011-2012) join the 10 countries tested before (Ethiopia, Ghana, Kenya, Lesotho, Malawi, Mali, Nigeria, Rwanda, Tanzania, Togo); each split trains on the other 24 countries (25,923 to 28,288 rows). Never tested: Benin and 8 Train.csv countries, 5,923 rows (20.7%).
   - The two split warnings follow from the leave-one-country-out rule the curator chose (issue 8) and stay accepted with the new numbers (16 of 25 countries tested; 9 countries never tested; 1 x 16), the curator's acceptance already given by the mark.

10. **Under which terms does the dataset ship, given that its labels come from DHS surveys?**

   - **Problem:**
     - The labels are cluster means of DHS and Malaria Indicator Surveys.
     - The DHS terms of use say the data "will not be used for any marketing or commercial venture", is not "shared with other researchers without the written consent of The DHS Program", and "DHS micro-level data will not be re-distributed"[^x24e4].
     - The record ships the dataset under CC BY-SA 4.0, the competition's grant, which allows commercial use.
   - **Background:**
     - Cluster-level means are arguably not micro-level data; SustainBench (Yeh et al. 2021) ships the same kind of DHS cluster labels under CC BY-SA 4.0 on that reading, and the africa_poverty repository under MIT.
     - The competition never names DHS; its licence was granted by Zindi, not by DHS.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep CC BY-SA 4.0 (implemented) | The record names the DHS origin and the cluster-level reading, as SustainBench does | the competition's grant; precedent in SustainBench | DHS's ban on commercial use is not addressed by the competition's grant |
     | B | Ship for non-commercial use | Licence note: research use only, the DHS terms named | follows the stricter terms | narrows who may use the benchmark |
     | C | Ask DHS | Write to the DHS Program for consent to redistribute cluster-level indices | settles it | takes time; the dataset waits |

   - **Recommendation:** C, with A in the meantime documented: the conflict sits between two parties' terms, and only DHS can settle it; the precedent of SustainBench makes A defensible until then. **Decision:** keep A, or change to B or C?

   [^x24e4]: DHS Program, Terms of Use, https://dhsprogram.com/data/terms-of-use.cfm (read 2026-11-24).

   **Andrej (2026-11-24, verdict discuss):** Please do a search for this dataset. I suspect that the full data with all countries in every survey might be available somewhere

   **Answer (AI, 2026-11-24):** found: the source is the Yeh et al. 2020 cluster table, and Train.csv plus Test.csv are all of its clusters with coordinates; the full labels of the 7 test countries are in it, but not more surveys with features. Issues 9 (re-source to 25 countries) and 10 (the DHS terms) follow from it. Other releases of the same kind of task:

     | Source | Countries | Years | Clusters | Target | Features | Licence |
     |---|---|---|---|---|---|---|
     | Zindi Train.csv (shipped) | 18 | 1994-2016 | 21,454 | pooled asset index, scaled 0-1 | 14 geospatial columns | CC BY-SA 4.0 (competition) |
     | Zindi Test.csv | 7 others | 1998-2016 | 7,194 | hidden | same | same |
     | africa_poverty `dhs_wealth_index.csv` | 30 (25 with coordinates) | 1994-2016 | 35,235 (28,649 with coordinates) | the same index, before scaling | coordinates only | MIT |
     | SustainBench, asset wealth | 48 (about 32 in Africa) | 1996-2019 | 86,936 | pooled asset index | satellite images only | CC BY-SA 4.0 |
     | temporal-eo-wealth (Pettersson et al. 2023) | 36 in Africa | 1991-2019 | 57,195 | International Wealth Index | coordinates only | none stated |

   **Andrej (2026-11-24, change):** Option B: Ship for non-commercial use. We are building a non-commercial academic benchmark

   **Resolved (2026-11-24, Andrej):** B, applied, following the repository's convention for terms beyond a licence name: a free-text `Source(license=...)` string, as for ai4d_lab_tanzania_tourism_classification_challenge ("CC BY-SA 4.0; publisher also states non-commercial research or education use") and body_density_prediction, plus a one-line note (the evidence rule on licences). `dataset.py`: the publication's `license` reads "CC BY-SA 4.0 (competition rules); the labels are cluster-level wealth indices from DHS surveys, whose terms of use bar commercial use; used for non-commercial academic research only."; a "Licence" bullet in `curation_comments` names the CC BY-SA 4.0 grant, the DHS terms (no marketing or commercial venture, no redistribution of micro-level data; the rows are cluster-level indices without coordinates or cluster ids) and the non-commercial academic use. Record: CC line. `dataset check` passes with the new string (0 errors).

**Review panel:** ship after changes (mediator, 2026-11-21, full re-check). Applied without a decision: the same-place check in place of the year-comparison bullet, the target's pooled min-max rescale as a kept-on-purpose note, water kept as unchanged at the same place, the scope reading of the geospatial inputs, the metric's country offset, the 129 conflicting duplicates (Central African Republic 1994-95 locality points, 0 copies across the split), the source's Test.csv in the splits comment, the tables of signal and of night lights alone in issue 3; the licence stays CC BY-SA 4.0 (the competition rules allow commercial use). Disputed and settled: the use-case override of the one-regime rule does not hold on the written use case (advocate conceded); population's answer follows issue 3 (B under the country holdout, C under the joint split); the gamer's "lights alone equals the full model" compared lights with untuned LightGBM, tuned models are 0.010 RMSE ahead; ridge and LightGBM tie, no reason to retire. For the curator: issues 3-7 and H (6, 7 and H only if issue 3 stays A). Earlier panel (2026-11-05): ship; its reports follow the 2026-11-21 ones below.

<details><summary>Mediator (2026-11-21)</summary>

**Mediator: economic_well_being_prediction_challenge (economic), 2026-11-21**

Read: principles.md, task_probes.md (TP-2, TP-4), the record (Comments, Review: issues 1-4, Horizon), dataset.py,
all seven panel reports (claim auditor, domain practitioner, precedent checker, advocate and critic openings and
rebuttals), the blind review and task gamer reports, the column audit summary, check.log, task.log, leak.log,
group.log, dtype.log. All probe logs are present.

Decisive experiment run (both sides agreed on it): Slurm job 1401950, script and per-cell output in
the run folder (`tp24.py`, `tp24_cells.csv`,
`1401950.log`). Frame and splits come from the definition. The cached TabArena runs do not hold this dataset
(`cache_check.py`), so `tuned_results.py` could not be used. I tuned locally instead:

- ridge (log inputs + missing flags, 7 alphas), random forest (6 configs), LightGBM (16 random configs incl. default);
- tuning on the training side only, with folds grouped by country (3 folds);
- the raw feature: an isotonic fit on the training side, the feature chosen by training R²; it was `nighttime_lights`
  on all 25 splits;
- shuffled labels: 5 permutations of the training labels, default LightGBM and ridge (alpha 1), scored on true test
  labels.
- Two splits: the 16 shipped cells, and the leaf of issue 3 B (3-fold by country over all years, 3 repeats = 9 splits).

**Recommendation (judgment record)**

```text
Verdict: ship after changes (issue 3 first; issues 4, N1, N2 and H follow from it).
Validity: SPLIT-3 (Must) not met by the joint split; the USE-1 override fails on the record's own use case and on the
  source's all-years Test.csv. Fix: issue 3 B (grouped by country, all years), unless the curator writes a forward,
  never-surveyed-country use case and an amendment to SPLIT-3. LEAK-10 triggered on population density (issue 4,
  fix B or C); night lights open (N1). LEAK-1 holds (0 copies in 16 splits). USE-5/USE-8 hold (approximate fit, resolved).
Value: TP-2 holds, a large real signal: tuned methods 0.1135 RMSE against dummy 0.1855; shuffled labels 0.1857-0.1885,
  never better than the best method on any of 25 splits. TP-4: night lights alone is beaten on the leaf (9 of 9
  splits, +0.0085 RMSE, SE 0.0011); on the shipped split it is close (methods ahead on 10 of 16, +0.0098, SE 0.0066).
  TP-3: no spread (ridge 0.1137 = LightGBM 0.1135); no reason to retire.
Quality: CLEAN-12 decoding done; doc fixes listed below.
Weighed: source + (published poverty-mapping task), size + (21,454 rows, 18 countries), provenance - (undocumented
  index, undated lights/population layers), separation - (no spread).
For the curator: issue 3 (split regime), then 4 (population), N1 (night lights), N2 (check warning, only if A stays),
  H (only if A stays).
```

**Decisive experiment: results**

Mean RMSE (lower is better).

| | Shipped split (16 cells) | Leaf, issue 3 B (9 splits) |
|---|---|---|
| Dummy (train mean) | 0.1855 | 0.1938 |
| Shuffled labels, LightGBM | 0.1885 | 0.1958 |
| Shuffled labels, ridge | 0.1857 | 0.1940 |
| Night lights alone (isotonic) | 0.1232 | 0.1223 |
| Ridge, tuned | 0.1137 | 0.1165 |
| Random forest, tuned | 0.1158 | 0.1167 |
| LightGBM, tuned | **0.1135** | **0.1164** |
| LightGBM, default | 0.1246 | 0.1221 |

Paired, night lights minus tuned LightGBM (the best family on the mean):

| Split | Mean difference | SE | Splits where the methods are better |
|---|---|---|---|
| Shipped | +0.0098 | 0.0066 | 10 of 16 |
| Leaf | +0.0059 | 0.0015 | 8 of 9 |

Against the best family per split (an optimistic choice): shipped +0.0150 (SE 0.0054, 10/16), leaf +0.0085 (SE 0.0011, 9/9).

Reading:

- **TP-2, step 1: signal, settled.** Shuffled labels stay at the dummy on both splits. The lowest of 5 shuffled runs
  never beats the best method on any split (0 of 25). The gap is about 0.07 RMSE. Caveat: the shuffled runs were
  not tuned (TP-2 asks for the same pipeline). Tuning on noise cannot close a 0.07 gap, so this does not change the
  reading.
- **TP-4, step 1.**
  - On the leaf, the methods beat night lights on 9 of 9 splits (best family per split) and 8 of 9 (LightGBM), by
    5x the SE. Their gain is real: go to step 2.
  - On the shipped split it is close. Lights alone wins on 6 of 16 cells: Malawi 2014, 2015 and 2016, Rwanda 2014
    and 2015, and Ethiopia 2016. Those are the cells with the large country offsets the practitioner measured
    (Malawi about +0.15). The fitted models carry the training countries' offsets into a new country, and the
    one-feature fit carries less of that. The mean gap is 1.5 SE. Methods ahead on 10 of 16 is "most splits" only
    narrowly. Under TP-4's own words this sits between "matches" and "beats".
  - What decides it is issue 3. Under B the beat is clear. Under A the curator has to call it (N3).
- **TP-4, step 2 (information, no retirement by the AI):** the methods' gain over lights is 0.006-0.010 RMSE. That
  is about 5-8% of the error and 8-14% of the dummy-to-best gap, on a 0-1 index. The decision the use case makes is
  ranking places for targeting. The practitioner's within-country Spearman (0.68-0.70) shows the full models rank
  places. The run did not measure lights alone on a ranking metric.
- **TP-3:** ridge and LightGBM tie on both splits (0.1137 against 0.1135; 0.1165 against 0.1164), so `no_spread`
  is confirmed. It is not a reason to retire (TP-2 step 2).
- **Untuned versus tuned:** the gamer's "lights alone equals the full model" (0.1237 against 0.1246) compared lights
  with *default* LightGBM. That model scores 0.1246 in my run too. Tuning moves LightGBM to 0.1135.

**Changes to make now (no decision needed)**

1. Record the TP-2 and TP-4 tables above in the record (an Experiments block under N3, or in the Assessment), with
   the paths. Rule: TP-2, TP-4, EV-1.
2. Rewrite the "Year-comparison check" bullet as the same-place check: at the same place, water, population and
   lights do not change; the 52 of 52 changes come from sampling different clusters. Rule: EV-7. Sources: claim audit
   #17, column audit doc fix 1.
3. Target bullet: the index was rescaled with one min-max over the whole release (one 0 in 2005, one 1 in 2013, both
   in training years). Write it as a `Potential leak, kept on purpose:` note. Rule: LEAK-30 (shape of its Cases).
4. Water line: kept under LEAK-10's "unless the data shows they did not change" clause (stable water bodies;
   same-place check). Both sides agree.
5. Metric note: RMSE stays (MET-4). 25-32% of each cell's MSE is one offset per country, and within-country ranking is
   what targeting uses (practitioner). Rule: MET-1, MET-4.
6. Scope line in `curation_comments`: the inputs are mapped quantities aggregated to 5 km plus GIS distances, read
   as SEL-15 measurements (covertype, geoai, airqo), not raw reflectance (the crop_type, cropharvest and cropmapil
   rejections). This closes the SEL-13 question from screening. Rule: SEL-13, SEL-15 (precedent F7).
7. Licence: read the Zindi page and the competition rules, then align the string with ai4d_lab_tanzania if the same
   non-commercial clause is there. This is a fact check, not a decision. Rule: PROV (precedent F8).
8. Note on the 129 conflicting duplicate rows: CAR locality points from 1994-95, 0 cross-split copies.
9. `## Review` outcome and main points: remove "No new question" and "No new curator decision is needed"; issues 3
   and 4 are open. Both sides conceded this.
10. Issue 4, independent of the option: add the claim audit's pop = 0 table to Experiments (pop = 0 implies no
    2000-2014 construction in 1,098 of 1,099 rows). Correct option B's Con (see below).
11. `splits_comment`: cite the source's Test.csv (7 unseen countries, 1998-2016). Column audit doc fix.

**Open issues in the record: keep / revise / withdraw**

| # | Verdict | What and why |
|---|---|---|
| 1 | settled | Resolved 2026-11-02; no change. |
| 2 | settled | Resolved 2026-11-02; no change. The pooled rescale goes in as a note (change 3). |
| 3 | **revise** | Change the framing and the recommendation (details below). |
| 4 | **revise** | Correct B's Con. Make the recommendation depend on issue 3. Move lights out to N1 and give water its line. Ask after issue 3. |
| H | **revise, ask last** | Ask only if issue 3 stays A (it falls away under B). If asked: drop "keeps 66%" as the reason for the newest three years, because SPLIT-15's floor is 50% (cooking_time_1m). Measure option B with `dataset windows`. Make the gap reasoning consistent with a forward reading: under a forward reading, SPLIT-10 asks for the label delay (option C). Say how the 16 cells count against SPLIT-33. |

**Issue 3, revised**

- **Problem as it should read.** SPLIT-3 is a Must: one regime, never both. principles.md: a Must takes no exception
  unless a higher-ranked Must overrides it.
  - The record's override cites USE-1. But the written `use_case` ("historical local wealth where survey coverage
    is missing"), the source's aim ("filling in the gaps between the more expensive surveys") and its Test.csv
    (1998-2016, 7 unseen countries) all read as historical, which the leaf tests.
  - So the override does not hold on the record's facts. Option A ("a listed departure") treats a Must as a Should.
- **Consistency** (precedent F1):
  - wadden_sea_sibes_macoma_abundance (Andrej, 2026-11-02) is the same shape and went grouped only.
  - lt_vehicle_loan_default_prediction: its USE-1 "override" of a split Must was replaced by an amendment (Lennart,
    2026-11-05).
- **Options to offer:**
  - B, the leaf (recommended).
  - C, keep the joint split. This needs two things: a written use case for a never-surveyed country in a later year,
    and an amendment to SPLIT-3, as for lt_vehicle.
  - Drop A as worded.
  - A pure temporal split that keeps the country's own history (H1: 0.1246 to 0.1098) is a different, known-entity
    task, and nobody argues for it. Mention it only as the reading the practitioner's actor would face.
- **New evidence for the issue:**
  - My run shows the leaf gives a clean TP-4 result (methods beat lights 9 of 9). The shipped split leaves TP-4
    borderline.
  - The leaf tests all 18 countries on 21,454 rows instead of 10 countries on 6,256.
- **On B, also rewrite `use_case`/`fit_reason`:** the test stands for a country without surveys of its own
  (practitioner finding 1). This is one change within B, not its own issue.

**Issue 4, revised**

- **Correct B's Con.** Under the shipped split, B leaves population 100% missing in training for 10 of 16 cells (all
  of 2014 and 2015), so there B works like C. It also adds a third column to the check warning.
- **Measured** (issue 4 table): shipped 0.1231, B 0.1225 (better on 9 cells), C 0.1216 (better on 12 cells).
- **Recommendation, conditional:**
  - under issue 3 B: B, because population is present on the 2015-16 rows on both sides;
  - under the joint split: C.
  - Both sides now agree on this.
- **Remove "Night lights stay: their epoch is undetermined"** from the Notes; that goes to N1.

**New issues for the curator (one decision each)**

**N1. Night lights: keep for all rows, mask before an inferred epoch, or keep with a written reason? (LEAK-10, Must;
CC 2026-10-31.)**

- **Problem.** Lights at the same place do not change across surveys up to 22 years apart (Δlog1p −0.016 at 13+
  years, while the target rises by +0.158), so they are one read used on rows from 1994 to 2016.
  - The epoch is unknown. The values are continuous with a maximum of 383, which is not raw DMSP (0-63). That fits
    VIIRS (2012 onward) or a radiance-calibrated DMSP composite.
  - The masking rule applied to construction and land cover would ask the same question here.
- **Advocate's best evidence.**
  - The regression puts little weight on 2000-2014 construction: 0.119, against 0.463 for population.
  - Population, unlike lights, decodes a masked field (1,098 of 1,099).
  - Masking lights before 2012 would remove them from most training rows. Dropping them costs +0.0134 RMSE and worsens
    16 of 16 cells.
- **Critic's best evidence.**
  - Population shows the same flat same-place values (−0.017), so flatness cannot set lights apart from population.
  - The weight on construction is unstable: 0.002 in one column-audit fit (1401879.log), 0.119 in the other
    (1401892.log).
- **What I settled.**
  - Nothing leaks to a test label. Lights are the task's natural core (TP-4), so their dominance rules out a leak.
  - The validity question (an older label paired with a later lights read in training) is a weighing the rules leave
    to the curator: it depends on an undocumented epoch.
- **Options.**
  - A: keep with a written reason plus a `Potential leak, kept on purpose:` note that the epoch is unknown (both
    sides accept this as an outcome).
  - B: mask before 2012.
  - C: drop.
- **Recommendation:** A. What would settle it: the product name and year of the lights layer from the source.

**N2. Accept the `splits_feature_missing_in_test` warning? (check rule; precedents anes_voting_2026,
delivery_eta_1m.)** Ask only if issue 3 stays A.

- Under A, `ghsl_built_2000_to_2014` and `ghsl_not_built_up` (plus population under issue 4 B) are 100% missing in
  training in the 2014 cells. Our own correct mask causes it.
- Under issue 3 B the folds span all years and the warning should go away; re-run `dataset check` to confirm.
- Recommendation: accept, with the reason, if A stays.

**N3. TP-4 on the shipped split: methods ahead or a match?** Ask only if issue 3 stays A.

- Methods are ahead on 10 of 16 cells, mean +0.0098 RMSE, SE 0.0066.
- Lights win the six cells with large country offsets.
- Recommendation: count it as the methods ahead (a gain of 8% of the error, and the within-country ranking
  improves). Keep the dataset. Under B this question does not arise (9 of 9).

**Gamer exploits mapped**

| Exploit | Rule | Known? | Reading |
|---|---|---|---|
| Survey-level feature means over the test window (−0.009) | LEAK-9 / USE-6 (prediction point) | NEW in kind, small | A deployed model has the cluster list before fieldwork; signal, not a leak. Uneven: 4 cells worse. No change. |
| Within-survey ranks (−0.007) | same | NEW, small | same |
| H1: test country's own history left out (−0.015) | USE-10, SPLIT-3 | KNOWN (issue 3) | Not an exploit; it is the regime question. Under an unseen-country task, it is by design. |
| Lights alone equals the full model | TP-4 | KNOWN (task.log flag) | Untuned comparison; tuned methods are 0.010 ahead (above). |

No `Potential leak, kept on purpose:` note is contradicted by a measured gain.

**Agreed facts**

- 21,454 rows, 18 countries, 1994-2016; 12 features; 0 cross-split copies in all 16 splits (claim audit, leak.log, gamer).
- The six GHSL fractions sum to 1 on every row. The masks are correct (0 unmasked cells) and are a pure function of
  `year`; the missing flags alone score R² −0.52.
- The source tests 7 unseen countries over 1998-2016 (Test.csv).
- Population, lights and water are each one read per place; population decodes the masked 2000-2014 field.
- The target is one pooled min-max over the release (one 0, one 1, both in training years).
- Signal: large and real (TP-2, this run). Spread: none (TP-3).
- 25-32% of per-cell MSE is a country offset.

**Consistency with precedent**

- Issue 3 B follows wadden_sea_sibes_macoma_abundance and the split tree's leaf.
- Keeping A would be the second USE-1 "override" of a split Must. The first (lt_vehicle) became an amendment, so C is
  the route that fits precedent if the curator wants the joint task.
- Issue 4 B/C follows this definition's own GHSL masks, its land-cover drop and melbourne_housing_market.
- N1 A departs from the masking applied to population only by the construction-weight fact, which is unstable. That
  is why it is the curator's call, not settled.
- The notes (rescale, water, scope) follow LEAK-30's Cases, LEAK-10's "did not change" clause, and covertype/geoai.
- The TP-4 reading follows california (kept, methods beat the feature), not the ljubljana_breast_cancer match.

</details>

<details><summary>Advocate (2026-11-21)</summary>

**Advocate opening: economic_well_being_prediction_challenge (economic)**

Advocate, 2026-11-21. Read: dataset.py, README, the record (Comments, Review, issues 3 and 4, Horizon), principles.md,
the claim audit, column audit, domain practitioner, precedent check, blind review, task gamer, check.log, task.log,
leak.log, group.log. No new runs.

**Position:** ship. The task is real and its signal is large; no audit refuted a claim, and the gamer found no
exploit. Two items need a curator mark: the split (issue 3) and the population mask (issue 4). Neither is a reason to
drop the dataset. Where the evidence goes against the definition as shipped, I name the mildest fix that keeps it.

**1. The signal is real and large on every shipped split (TP-2 step 1, Should; TP-1, Must)**

| Source | Dummy RMSE | Best method RMSE | Splits beaten |
|---|---|---|---|
| task.log (untuned, 5 of 16 splits) | 0.192 | 0.118 (random forest) | 100% |
| claim audit + 11-05 retained tuned runs (16 splits) | 0.1855 | 0.1183 (ridge), 0.1188 (LightGBM) | 16 of 16 (linear) |
| domain practitioner (16 splits) | | 0.113 (ridge), 0.127 (HGB) | |
| blind review (16 windows) | 0.199 | 0.122 | |

- The error falls by about 36% against the train mean, and four independent runs agree.
- The domain practitioner gets a within-country Spearman of about 0.70 and recalls the poorest 20% at about twice
  chance. That matches the published level for satellite poverty mapping (Yeh et al. 2020; Chi et al. 2022).
- A shuffled-label run has not been done, as TP-2 asks. A drop from 0.185 to 0.118 on all 16 cells is too large for
  shuffled labels to match, but the run should be done before shipping. It is cheap.

**2. No leak reaches a test label; the gamer and the leak probe found nothing (LEAK-1, LEAK-10, Must)**

- There are 0 exact feature copies across all 16 splits (leak.log, claim audit, gamer).
- The masks are a pure function of `year`. On its own, the missing indicator scores R² −0.52 (leak.log), and the gamer
  says it "carries nothing beyond `year`".
- Format features, global ranks and a kNN label all score worse than the 0.1246 baseline (gamer).
- The gamer's two gains (0.009 and 0.007) come from survey-level means of features. A deployed model has those,
  because the cluster list is fixed before fieldwork. They are signal, not an exploit.
- The six GHSL fractions sum to 1.000000 on every row, so masking `not_built_up` before 2014 is needed; `_extra_checks`
  finds 0 unmasked cells (claim audit, claims 7-8). The repair the curator asked for on 10-31 is in place and checked.

**3. Issue 4 (population density): accept B; it is the mildest fix and costs nothing (LEAK-10, Must)**

- I do not deny the problem. Population at one place does not change over 22 years. Its coefficient on 2000-2014
  construction is 0.463 (column audit). Population 0 implies no 2000-2014 construction in 1,098 of 1,099 rows (claim
  audit, finding 1). So it is a later state on the 18,129 rows before 2015.
- Masking it before 2015 follows LEAK-10's "blank the located cells" clause and the definition's own masks. It changes
  the score by noise: LightGBM 0.1231 shipped, 0.1225 masked (issue 4).
- The effect on the task is small: the target mean is 0.192 against 0.188 across those groups (claim audit). The test
  rows of 2014-2016 are roughly contemporary with a 2015 layer.
- **Night lights stay.** At the same place their mean change is −0.016 (log1p) over 13+ years, while the target rises by
  +0.158 (issue 4 table). A later lights read would track later wealth. These lights do not, so they carry no later
  state of the label. The regression weight on 2000-2014 construction is also small (0.119 against 0.463 for
  population). This is the distinguishing fact that the precedent checker (F5) asks us to write down. Write it into the
  curation comment; no mask is needed.
- Water: LEAK-10's "unless the data shows they did not change" applies. Write that down as a note.

**4. The split: every option keeps the dataset, and the country holdout is the source's design (USE-10, SPLIT-3, Must)**

- **Not in dispute.** Every one of the 16 tests is a country held out of training. The source's own test is "surveys
  in 7 different countries not covered in the training data", and its Test.csv covers 7 unseen countries over
  1998-2016 (column audit). Under USE-10 the entity is new (a cold start), so a grouped test is right.
- **This answers H1** (gamer and practitioner: the test drops the country's own earlier surveys). Adding them back
  would test a known entity. The source deliberately tests unseen countries. The H1 gain (0.125 to 0.110) measures how
  much easier a different task is, not a flaw in this one.
- **What is in dispute** is the extra "earlier years only" constraint. I concede the precedent checker's F1. SPLIT-3 is
  a Must, and principles.md says a Must takes no exception. The source's all-years Test.csv and the definition's own
  `use_case` ("historical local wealth") read as retrospective, so the USE-1 override written into splits.md Cases does
  not hold on its stated facts.
- **Mildest fix that keeps the definition's task:** a written forward fact (precedent option a). An agency that
  deploys in year t holds only the surveys fielded before t, so a model trained at t never sees later labels. Under
  that reading the temporal half is a fact of deployment, not a second regime. The curator asked for it twice
  (2026-11-02, 2026-11-05).
- **If the curator does not state that fact:** take B, the leaf (Grouped · UnseenGroup by country, all years), as in
  wadden_sea_sibes_macoma_abundance. It also ships, tests all 18 countries and does not need the 2014-only check
  warning (point 5).
- Either way this is a split choice. It is not a reason to exclude the dataset.

**5. The new check warning needs a curator acceptance, not a data change (check.log; precedents anes_voting_2026, delivery_eta_1m)**

- `splits_feature_missing_in_test`: `ghsl_built_2000_to_2014` and `ghsl_not_built_up` are 100% missing in training
  for the 2014 cells. The cause is our own mask, which point 2 shows is correct.
- Five definitions accepted this warning in `accepted_check_warnings`, each with a curator decision. Do the same here,
  or fold it into issue 4's mark, because option B adds `ghsl_pop_density` to the same pattern.
- Under issue 3 B the 2014-only pattern disappears, because folds span all years.

**6. The flags `no_spread` and `one_feature` are questions, not verdicts (TP-1, TP-3, TP-4, Must)**

- `no_spread` does not retire a dataset. TP-3 keeps a dataset whose methods spread. It says nothing against one whose
  methods do not, and TP-2 step 2 says that being hard to separate is no reason to retire.
- `one_feature` (nighttime_lights): lights are the natural core of geospatial wealth mapping. TP-4: such a core "is
  expected to dominate, which rules out a leak but not the test".

  | Comparison | Lights alone | Best method | Basis |
  |---|---|---|---|
  | task.log | 0.121 | 0.118 (forest) | untuned, 5 of 16 splits |
  | gamer | 0.1237 | 0.1246 (LightGBM) | untuned |
  | claim audit | | 0.1183 (ridge, retained tuned) | 16 splits |

- That is a TP-4 candidate (it matches), not proof of `Trivial` (it does not beat the methods). TP-4 step 1 needs the
  paired comparison of tuned methods over all 16 splits before any marker.
- The light-only rule is also fitted on the data, not a field rule.
- The within-country ranking (Spearman about 0.70) and the method gains on the offset-removed RMSE (practitioner) are
  where the extra inputs earn their place.

**7. Target, metric, scope and provenance hold as decided (USE-5, USE-8, MET-4, SEL-15)**

- **Target.** It is a supplied 0-1 index, accepted as approximate fit (issue 2, resolved 2026-11-02). The single pooled
  min-max rescale has one 0 (2005) and one 1 (2013). Both are in training years, and an affine rescale gives no
  row-level information (claim audit, finding 3). Add a `Potential leak, kept on purpose:` note, as in LEAK-30's Cases.
- **Metric.** RMSE is the source's metric (MET-4). The practitioner keeps it. Its point that a quarter to a third of
  each cell's MSE is a country offset goes in a note.
- **Scope.** The inputs are mapped quantities and GIS distances, not raw reflectance. That is the covertype and geoai
  reading (SEL-15), against the crop_type rejections. One line in `curation_comments` closes it (precedent check F7).
- **Duplicates.** 129 conflicting rows (0.6%) are Central African Republic locality points from 1994-95, with 0
  cross-split copies. A note is enough.
- **Licence.** Align the string with the ai4d_lab_tanzania wording after reading the page (F8). This is a doc fix.

**Changes that keep it shippable:**
1. Issue 4 B.
2. Issue 3: a written forward fact, or else B.
3. Accept the check warning with a curator mark.
4. A shuffled-label run.
5. A paired tuned comparison with lights alone.
6. The doc fixes: lights note, water note, rescale note, scope line, licence, the same-place check that replaces the
   year-comparison bullet.

</details>

<details><summary>Advocate rebuttal (2026-11-21)</summary>

**Advocate rebuttal: economic_well_being_prediction_challenge (economic)**

Advocate, 2026-11-21, answering the critic's opening. No new runs. One new fact came up: the critic's point 4 changes
my choice on issue 4. I keep the position: ship after the marks. The critic also asks for no exclusion. We differ on
the remedy, not on the verdict.

| # | Critic's point | Concede / dispute | What follows |
|---|---|---|---|
| 1 | The joint split fits neither reading | Concede the rule, dispute one premise | B is the default; A needs a forward fact or an amendment |
| 2 | Lights are an undated later read | Concede the process; dispute the mask | Own item; recommend keeping lights with a written reason |
| 3 | `one_feature` has no TP-4 test | Concede | Run the paired tuned test on all 16 cells |
| 4 | Warning unaccepted; issue 4 B makes it larger | Concede; this changes my issue 4 choice | C (drop) if the joint split stays; B under issue 3 B |
| 5 | The Horizon contradicts the split | Concede the order; dispute "3 windows" | Ask it after issue 3 |
| 6 | Target scale and the country offset | Concede | Notes only |
| 7 | The documentation contradicts itself | Concede | Rewrite the lines |

**1. Split: concede SPLIT-3; dispute that a forward reading means keeping the country's history**

- **Conceded.** SPLIT-3 is a Must. The USE-1 override in splits.md does not hold on the definition's retrospective
  `use_case` or on the all-years Test.csv. Option A, a "listed departure", treats a Must as a Should. Without a written
  forward fact, B (the leaf, like wadden_sea) is the right call. I said the same in my point 4.
- **Disputed.** "Forward reading → temporal, with the country's own history kept" does not follow.
  - USE-10 decides new against known from the use case.
  - The source's use case tests countries the model has never seen: "7 different countries not covered in the
    training data". That makes the entity new, which is a cold start.
  - Adding the country's history (0.125 to 0.110, gamer; 0.127 to 0.111, practitioner) scores a known-entity task the
    source did not set.
  - So the forward reading that matches the source is the critic's third reading, "an unseen country in a later
    year". It is not unwritten: the source's design is its grouped half. Only the later-year half lacks a written fact.
- **What follows.**
  - B by default.
  - Option C (an amendment to SPLIT-3) only if the curator writes the forward fact: at deployment in year t, only
    surveys before t exist.
  - A temporal split that keeps the country's own history is not on the table. It changes the task.

**2. Night lights: concede a separate item; dispute masking**

- **Conceded.** Under one decision per issue, lights need their own item. The distinguishing facts must be written
  down: a weight of 0.119 on 2000-2014 construction, against 0.463 for population, and water's line ("did not
  change").
- **Disputed: lights do not describe a later state of the label.** LEAK-10 and the 10-31 rule target values that carry
  what happened after the row's time.
  - At the same place, lights move by −0.016 (log1p) over 13+ years while the target rises by +0.158 (issue 4 table).
    A read that tracked later wealth would rise with it. This one does not.
  - Its weight on 2000-2014 construction is small (0.119), unlike population's (0.463). So no later development is
    visible through it.
  - Population differs: pop = 0 decodes the masked 2000-2014 field in 1,098 of 1,099 rows. No such link to a masked
    field is shown for lights.
- **The alternative costs the task.** If lights are VIIRS, masking them before 2012 leaves them missing on most
  training rows. That is close to dropping them: +0.0134 RMSE, worse in 16 of 16 cells (ablation.csv). Doing that
  would rest on an inferred epoch, and the column audit calls the evidence for that epoch contradictory (its two
  regressions disagree).
- **Recommendation for the item:** keep lights, with the reason written down (the same-place stability and the low
  weight on construction). Also add a `Potential leak, kept on purpose:` line that the epoch is unknown.

**3. TP-4 on night lights: concede**

- This matches my point 6. Lights score 0.121-0.124 against 0.118 for the best methods. Lights are a candidate, not
  `Trivial`.
- Run the paired tuned comparison on all 16 cells before shipping. The curator decides on a match.
- I add one thing: under issue 3 B the folds change, so run the test on the split that ships.

**4. Check warning and issue 4 B: concede; my issue 4 choice changes**

- **Conceded.** The warning needs a curator mark (anes_voting_2026, delivery_eta_1m). B's Con is understated.
- **What follows.** Under the joint split, population becomes missing in training for 10 of 16 cells. In those cells
  B is C. The measurements also favour C:

  | Variant | Mean RMSE | Cells better than shipped |
  |---|---|---|
  | Shipped | 0.1231 | |
  | B: masked before 2015 | 0.1225 | 9 |
  | C: dropped | 0.1216 | 12 |

- C also keeps the warning to the two columns it has now. So:
  - **if the joint split stays:** recommend C;
  - **if issue 3 goes to B:** keep B. In all-year folds, population is present on the 2015-16 rows on both sides, so
    there is no train-only gap.
- I withdraw "B, the mildest fix" as an unconditional recommendation. The choice depends on issue 3, so issue 4 should
  be asked after it.

**5. Horizon: concede the order; dispute the count of 3 windows**

- **Conceded.** The no-gap and newest-three-years reasons rest on a reading that issue 3 decides. Ask the Horizon after
  issue 3. Under issue 3 B it falls away. If the split stays temporal, "keeps 66%" is not a reason SPLIT-15 accepts
  (cooking_time_1m).
- **Disputed: "3 windows".** The rule counts folds whose training sides differ.
  - Here each training side leaves out a different country, 129 to 2,381 rows (gamer), so the 16 training sides do
    differ.
  - They are not test-only sub-folds of one training side.
  - They do overlap heavily, so a reviewer should say whether that counts. This is moot under issue 3 B.

**6. Target scale and RMSE offset: concede**

The same notes as my point 7:
- a `Potential leak, kept on purpose:` line on the pooled rescale;
- a line on the within-country ranking gap;
- RMSE stays (MET-4).

**7. Documentation: concede**

- Also concede that the `## Review` line "No new curator decision is needed" is wrong while issues 3 and 4 are open.
  Remove it.
- The year-comparison bullet, the licence and the scope line are the doc fixes already on my list.

**Where we still differ**

- **Lights (point 2).** Keep with a written reason (me), against an open item that may end in a mask (critic). We agree
  it is a separate item.
- **Count (point 5).** We differ on whether the 16 cells count as 3 windows. This matters only if the joint split
  survives.

Everything else is agreed. The order for the curator: issue 3 first, then issue 4 (C or B, following issue 3), the
lights item, the TP-4 run on the shipped split, the warning mark, and the notes.

</details>

<details><summary>Critic (2026-11-21)</summary>

**Critic opening: economic_well_being_prediction_challenge (2026-11-21)**

**Position:** do not ship as defined. It is a real task with real signal, so nothing here asks for exclusion. It needs
three decisions first: the split (issue 3), the dating of night lights, and a TP-4 test on night lights. Most fundamental first.

**1. The joint year × country split fits neither reading of the use case (validity; SPLIT-3 Must, USE-10 Must)**

- **Problem.** SPLIT-3 is a Must: one regime, never both. principles.md, "Exceptions and amendments": only a
  higher-ranked Must overrides a Must. The exception row in splits.md cites USE-1. But the written use case does not
  ask for a future year:
  - `use_case`: "estimates **historical** local wealth where survey coverage is missing";
  - the source's aim: "filling in the gaps between the more expensive surveys";
  - the source's Test.csv covers 1998-2016 in 7 unseen countries (issue 3 Answer, claim audit #19).
- **Either reading gives one regime.**
  - Historical: the leaf, Grouped · UnseenGroup (countries), which is also the source's design.
  - Forward, "between surveys" in a surveyed country: USE-10 says the country's own history is legitimate, so the
    split is temporal and keeps that history.
  - Only the "never-surveyed country in a later year" reading needs both regimes. Nobody wrote that use case down,
    and all 16 test cells have 1 to 9 earlier surveys of their own country in the file (domain practitioner).
- **Measured effect of removing the country's own history** (mean over the 16 cells):

  | Source | Model | Shipped split | With the country's earlier surveys |
  |---|---|---|---|
  | Task gamer | LightGBM | 0.1246 | 0.1098 (15/16 cells better) |
  | Domain practitioner | HGB | 0.1270 | 0.1105 (13/16) |
  | Domain practitioner | ridge | 0.1133 | 0.1092 (16/16) |

- **Precedents.** wadden_sea_sibes_macoma_abundance has the same shape: a survey that maps unsampled places in past
  rounds. Andrej split it grouped only (2026-11-02). lt_vehicle_loan_default_prediction also claimed a USE-1
  "override" of a split Must, and Lennart replaced it with an amendment (2026-11-05). Precedent checker F1.
- **Remedy (mildest that works):** issue 3 option B, grouped by country over all years. Or option C: write down the
  forward "unseen country" use case and get an amendment to SPLIT-3. Option A, a "listed departure", calls a Must a
  Should. SPLIT-36 is a Should, but SPLIT-3 is the binding rule.

**2. Night lights are one undated read that carries the task; issue 4 treats population but not lights (validity; LEAK-10 Must, CC 2026-10-31)**

- **Problem.** At the same place, lights do not change between surveys up to 22 years apart, while the target rises.
  Same-place pairs 13+ years apart: lights Δlog −0.016, target +0.158 (issue 4 table). So lights are a single
  snapshot used for rows from 1994 to 2016.
- **Its epoch is unknown.** The values are continuous with a maximum of 383 (task gamer). That rules out raw DMSP
  stable lights (0-63). It fits VIIRS (2012 onward) or a radiance-calibrated DMSP composite. The column audit leaves
  it "undetermined".
- **Why it matters.** Lights are the task's main feature: about 60% of the gain (blind review). Dropping them costs
  +0.0134 RMSE, worse in 16 of 16 cells (column audit ablation.csv).
- **The rule.** The curator's 2026-10-31 rule says fields describing a later state are not acceptable. LEAK-10's
  later-pull clause applies. The same rule masks the 2000-2014 construction fields and dropped land cover.
- **Effect on the task.** If lights are VIIRS, a 1994-2013 training row pairs a later light reading with an older
  wealth label, while the 2014-2016 test rows are about current. Nothing leaks to a test label. But the model learns
  a mismatched relation, and the definition breaks its own masking rule on its strongest column.
- **Remedy.**
  - Give lights their own decision item, one decision per issue: keep with a written reason, mask before the
    inferred epoch, or keep with a `Potential leak, kept on purpose:` note.
  - Issue 4 now says only "epoch undetermined". To set lights apart from population it must state the distinguishing
    fact: the regression puts little weight on 2000-2014 construction (0.119 against 0.463 for population).
    Precedent checker F5. Water also needs its one line: stable water bodies, LEAK-10's "did not change".

**3. The `one_feature` flag has no TP-4 test yet (value; TP-4 Must, TP-3)**

- **Problem.** The probe flags `one_feature` and `no_spread`. TP-4 step 1 compares the raw feature, chosen per
  training side, with the best tuned methods, paired per split. Nobody has run that test.
- **Evidence it may match:**

  | Run | Lights alone | Best methods |
  |---|---|---|
  | Task probe, 5 splits | single feature 0.1211 | linear 0.1207, random forest 0.1181, LightGBM 0.1233 |
  | Task gamer, 16 splits | 0.1237 | full LightGBM 0.1246 |
  | Earlier gamer and mediator, 16 splits | 0.1237 | ridge 0.1183, forest 0.1179 (task-final) |

  The best methods are about 0.005 RMSE ahead. The cell-to-cell spread is 0.137-0.276 even for the dummy.
- **Reading.** Lights are the field's standard wealth proxy, the natural core of the task. That rules out a leak, not
  the test.
- **Remedy.** Run `tuned_results.py --feature auto` on all 16 cells. If the methods beat lights on most cells,
  record the gain (step 2). If they match, the dataset is a `Trivial` candidate and the curator decides. Exclusion
  only on that outcome.

**4. A check warning ships without a curator acceptance, and issue 4 B makes it larger (process; check rule, precedent F6)**

- **Problem.** check.log (28 checks) warns `splits_feature_missing_in_test`. `ghsl_built_2000_to_2014` and
  `ghsl_not_built_up` are 100% missing in training for the 2014 cells and observed in their tests.
  `accepted_check_warnings` is empty. Every precedent took a curator mark: anes_voting_2026, college_scorecard,
  onlinenewspopularity, home_credit and delivery_eta_1m.
- **Issue 4 B makes it larger.** It masks population before 2015. Population is then 100% missing in training for the
  2014 and 2015 cells, 10 of 16, and it can be learned only in the 2016 cells. So in most cells B works like C. Issue
  4's Con says only "the 2014 test cells train without it".
- **Remedy.** Add the warning to issue 4, or give it its own mark. Correct B's Con.

**5. The Horizon contradicts the split's own reason (SPLIT-10, SPLIT-15, SPLIT-33)**

- **No gap.** The Horizon recommends no gap because the use case "reads as historical". The split exception needs a
  forward reading. Under a forward reading, SPLIT-10 asks for the label delay as a gap: option C. Precedent F2.
- **Newest three years.** The reason given is "keeps every training side at 66% or more". SPLIT-15 does not accept
  that reason; its floor is 50%. cooking_time_1m was reopened for the same reason. The history has 19 survey years.
  Precedent F3.
- **16 cells or 3 windows?** Within a year, the training sides differ only by the test country's rows. The record's
  own mediator calls them "three annual windows ..., not sixteen independent temporal replications". Counted as 3,
  they fall below SPLIT-33's target of 9. Precedent F4.
- **Remedy.** Ask the Horizon after issue 3. It falls away under issue 3 B. If the split stays temporal: measure
  option B (`dataset windows`), and give the gap and the count with reasons the rules accept.

**6. The target scale is fitted on all years, and RMSE is a third country offset (notes; LEAK-30, MET-1, USE-8)**

- **Problem.** The target has exactly one 0 (2005) and one 1 (2013), so it was rescaled once over the whole release.
  Its construction is undocumented (issue 2, resolved as an approximate fit).
- **The metric.** 25-32% of the per-cell MSE is one offset per country, and that offset plays no part in ranking
  places within a country (domain practitioner).
- **Effect.** Small. A single affine rescale gives no row-level information, and both extremes fall in training years.
- **Remedy.** Notes only:
  - a `Potential leak, kept on purpose:` line on the pooled rescale (LEAK-30 shape, precedent F9);
  - a line naming the within-country ranking gap.
  - Keep RMSE: MET-4, the source's metric.

**7. The documentation contradicts itself or is unsupported (quality; EV-7, SEL-13/15)**

- **Year-comparison bullet.** It says water, population and lights change in 52 of 52 comparisons, which reads as
  if the layers vary by year. The 11-21 Assessment and the same-place check show they do not. Claim audit #17,
  column audit doc fix 1.
- **The `## Review` outcome.** It says "No new curator decision is needed", while issues 3 and 4 are open.
- **Licence.** `CC BY-SA 4.0` has no evidence in the record. The Zindi sibling, ai4d_lab_tanzania, also records a
  non-commercial clause from the competition rules (F8).
- **Scope.** The SEL-13 scope question from screening was never answered. One SEL-15 line, "mapped quantities as
  measurements", like covertype and geoai, closes it (F7).
- **Remedy.** Rewrite these lines. No data change.

**Ranking for the curator:** 1 decides the task. 2 and 3 decide whether the strongest column is valid and whether it
alone is the task. 4-7 are mostly repairs and notes.

</details>

<details><summary>Critic rebuttal (2026-11-21)</summary>

**Critic rebuttal: economic_well_being_prediction_challenge (2026-11-21)**

The advocate and I agree on most points: ship after changes, no exclusion on the evidence so far. Three points are
still in dispute: the forward-fact option for the split (A4), whether population masking "costs nothing" (A3), and
the reason given for keeping night lights (A3).

**A1. The signal is real: concede**

- The dummy RMSE of 0.185-0.199 falls to 0.113-0.122 in four independent runs, and linear beats the dummy on 16 of 16
  cells. I agree that a shuffled-label run (TP-2) is still needed. It is cheap.

**A2. No leak reaches a test label: concede**

- I agree, and my point 2 said the same: zero cross-split copies, and the masks encode only `year`. Lights and
  population are a question of training validity, not of a test leak.

**A3. Issue 4: concede B as a fix; dispute "costs nothing" and the reason for keeping lights**

**Population, B: concede.** B is a valid fix. C would be equally mild: dropping population scores 0.1216 and is
better than shipped in 12 of 16 cells, while B scores 0.1225 and is better in 9 (issue 4 table).

**"Costs nothing": dispute.** Every training side of the 2014 and 2015 cells holds only years before 2015. Under B,
population is 100% missing in training for 10 of the 16 cells. B therefore works like C on most of the benchmark. It
also adds a third column to the unaccepted `splits_feature_missing_in_test` warning. Issue 4's Con must say so; it
now names only the 2014 cells.

**"Lights stay because they do not track later wealth": dispute.**

- The advocate's fact is: at the same place, the lights value stays flat while the target rises. Population passes
  the same test:

  | Same-place pairs, 13+ years apart | Change |
  |---|---|
  | Lights (log1p) | −0.016 |
  | Population (log1p) | −0.017 |
  | Target | +0.158 |

  The advocate masks population anyway. So this fact cannot set lights apart from population. It shows only that
  both columns are a single read.
- LEAK-10 asks something else: was the value looked up after the row's survey, "unless the data shows they did not
  change"? A flat value in the file shows a single read. It does not show that the place's real lights stayed the
  same.
- The one fact that could set lights apart is the weight on 2000-2014 construction: 0.119 for lights against 0.463
  for population. But the column audit calls the lights epoch undetermined, because its two fits disagree. In
  1401879.log the log-OLS weight on 2000-2014 is 0.002; in 1401892.log it is 0.119.
- The value range does not settle it either. A maximum of 383 is not raw DMSP (0-63). It fits VIIRS (from 2012) or a
  radiance-calibrated DMSP composite.
- Keeping lights may be the right outcome. But it is a curator call on the task's strongest column, and the stated
  reason does not hold.
- I hold point 2: lights get their own decision item. Keeping them with a written reason, a mark, and a
  `Potential leak, kept on purpose:` note would satisfy me. The advocate's water note under LEAK-10's "did not change"
  clause: concede.

**A4. The split: concede the leaf; dispute the forward-fact option**

**Agreed.** The advocate concedes precedent F1: a Must takes no exception, and the record's USE-1 override fails on
its own facts. Under an unseen-country task, H1 (leaving out the country's own earlier surveys) is not a flaw: concede.

**Dispute option a**, "an agency deploying in year t holds only the surveys before t, so the temporal half is a fact
of deployment, not a second regime". This does not escape SPLIT-3:

1. A rule that keeps later rows out of training is a temporal split. With the country holdout on top, that is still
   two regimes. Naming it a deployment fact does not change the memberships. It needs an amendment to SPLIT-3, as on
   lt_vehicle_loan_default_prediction, not a reworded note.
2. A forward agency mapping a country between its surveys holds that country's earlier surveys. Every one of the 16
   test cells has 1 to 9 of them. USE-10 (Must) then makes the entity known, so the split is temporal and keeps that
   history (H1: 0.1246 to 0.1098). The joint split stands only for a country that has never been surveyed, and no
   test cell is one.
3. A forward reading needs the label delay as a gap (SPLIT-10). The Horizon chose no gap because it read the use
   case as historical (precedent F2).

**Remedy.** Issue 3 B, as the advocate's fallback: grouped by country over all years, as the source designed it and as
in wadden_sea_sibes_macoma_abundance. Under B, the 2014-only check warning and the Horizon questions (my point 5)
fall away. Option C only with a written never-surveyed-country use case and an amendment to SPLIT-3.

**A5. The check warning needs a curator acceptance: concede**

- Fold it into issue 4's mark, together with the larger B footprint described under A3.

**A6. The flags are questions, not verdicts: concede, with one correction**

- I asked for the test, not for a marker. On TP-4 step 1 we agree.
- "The light-only rule is fitted on the data" does not exempt lights. TP-4 step 1 tests "the raw feature, chosen on
  each split's training side" against the tuned methods.
- The advocate's own table calls it a match. A match makes the dataset a `Trivial` candidate, and the curator decides.
  So the paired tuned run over all 16 cells is a precondition for shipping, not a nice-to-have.

**A7. Target, metric, scope, duplicates and licence: concede**

- I agree on each of the advocate's notes.
- One addition the advocate did not answer: the `## Review` outcome line "No new curator decision is needed"
  contradicts the open issues 3 and 4. It must be rewritten.

**The shared fix list**

| # | Change | Status |
|---|---|---|
| 1 | Issue 3 B, the grouped leaf by country over all years | split dispute ends here |
| 2 | Issue 4 B or C, with the Con corrected (10 of 16 cells lose population in training) | agreed |
| 3 | Lights: their own decision item, with a reason that holds | in dispute |
| 4 | Accept the check warning with a curator mark | agreed |
| 5 | A shuffled-label run | agreed |
| 6 | The paired tuned comparison with lights alone over all 16 cells | agreed |
| 7 | The documentation fixes, including the Review outcome line | agreed |

</details>

<details><summary>Claim audit (2026-11-21)</summary>

**Claim audit: economic_well_being_prediction_challenge (economic)**

Claim-auditor, 2026-11-21. Data: the Train.csv and Test.csv under the run folder (same SHA-256 as the curator's file). Frame and splits are built through the definition (`dataset_io.definition`). Scripts and logs: the run folder (audit.py → 1401910.log, zeros.py → 1401921.log, popmask.py → its log).
Probe outputs (check.log, leak/, task/, group.log) were **not present** in `pr59_panel/economic_well_being_prediction_challenge/` when I ran; only `precedent/` existed. I used the README's check block (27 checks, 0 errors, 0 warnings, 3 infos) as given.

**Result: 0 claims refuted. 1 NEW piece of evidence for the KNOWN issue 4 (population density). 2 claims are misleading as worded (both KNOWN from the column audit). Metric holds.**

**Claim table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 21,454 rows, 18 countries, 1994–2016 | task_summary.row | count on raw | holds | 21,454 rows; 18 countries; 1994–2016 | EV-1 |
| 2 | No missing cells, no duplicate IDs | assessment 10-31 | count | holds | 0 and 0 | |
| 3 | Target 0–1, higher = wealthier | task_summary.predicted | min/max | holds | min 0 (one row, 2005), max 1 (one row, 2013): one pooled min-max rescale over the whole file (KNOWN, column audit) | MET-3 |
| 4 | "Original labels are unique" | curation bullet "Keep all rows" | duplicated Target values | holds | 0 duplicated values | |
| 5 | 173 rows with repeated complete predictor profiles | assessment 10-31 | duplicated on all raw features | holds | 173 (also 173 without land cover); after masking, 129 rows conflict (bundle info) | |
| 6 | 18,129 rows predate 2015 | assessment 10-31, issue 4 | count | holds | 18,129 | |
| 7 | not_built_up is a residual that reconstructs future construction | curation "Temporal repair" | sum of the six GHSL fractions | holds | sum = 1.000000 on every row, so masking it before 2014 is needed | LEAK-10 |
| 8 | Masks: 1990–2000 before 2000, 2000–2014 and not_built_up before 2014 | curation, Decisions table | masked counts in the frame | holds | 1,364 / 15,198 / 15,198 masked; `_extra_checks` finds 0 unmasked cells | LEAK-10 |
| 9 | Four land-cover columns omitted | changes, curation | frame columns | holds | absent. Raw values are on 0–100, not fractions (19,697 crops values > 1); irrelevant once dropped | |
| 10 | In 2014 tests the two 2014-ending fields are missing throughout training but observed in test | curation | count observed per side | holds | 0 training rows observed in all 6 tests of 2014; 1,346–2,931 training rows (the 2014 rows only) in the 2015 tests; 4,313–5,034 in 2016 | |
| 11 | 12 predictors; country and ID dropped | curation, assessment 11-03 | model-frame columns | holds | 12 features: year, urban_or_rural, 6 GHSL, pop, lights, 2 distances | |
| 12 | 16 country-year tests in 2014–2016, 10 countries | split, splits_comment | rebuild splits | holds | 16 tests; 10 countries; tests 1,222 / 2,103 / 2,931 rows by year; 6,256 distinct tested rows | SPLIT-4 |
| 13 | Every training side is strictly earlier, excludes the test country and holds > 50% of rows | splits_comment, curation | per split: max train year, country overlap, share | holds | max train year = t−1 every time; overlap 0; share 0.663–0.892 | SPLIT-14 |
| 14 | No row is a copy across the split (implied) | definition | exact 12-feature string match, test vs train | holds | 0 copies in all 16 tests | LEAK-1 |
| 15 | Five exact distance-signature groups span 1994–95 (25 rows), all 14 geographic inputs unchanged | curation "Year-comparison check" | group by country + both distances | holds | 5 groups, 25 rows, all in the Central African Republic, all 14 inputs constant | |
| 16 | 41 exact location groups, 205 rows, all CAR 1994–95 | assessment 11-21 | same grouping, any year | holds | 41 groups, 205 rows. Also: 31 of them hold both a Rural and an Urban row at the same point (see sample rows 1 and 4 in the README), consistent with locality points (KNOWN) | |
| 17 | Water, population and lights means change in all 52 consecutive observed-year comparisons; 70 country-year samples | curation, assessment 11-02 | country-year means | holds, misleading | 70 cells; 52 of 52 change for water, pop, lights and the fixed 2000–2014 layer. The change comes from different sampled clusters: at the same place these inputs do not change (column audit). The bullet reads as if the layers vary by year (KNOWN, column audit doc fix 1) | EV-7 |
| 18 | "Zero numeric measurements remain zero; the source documents no alternative missing-code convention" | curation | zeros per column, their relation to built-up | holds, with a note | 1,397 rows have pop density 0 (6.5%), 10,074 have lights 0. Pop 0 is not a missing code: 1,396 of the 1,397 have no built-up at all through 2014. See finding 1 | CLEAN |
| 19 | Source Test.csv covers 1998–2016 in 7 other countries | issue 3 answer | read Test.csv | holds | 7,194 rows, 1998–2016, Angola, Benin, Burkina Faso, DR Congo, Uganda, Zambia, Zimbabwe; no overlap with training countries | SPLIT-36 |
| 20 | Dummy macro RMSE 0.185473; ridge 0.118, LightGBM 0.119 | assessment 10-31 | train-mean predictor per cell | dummy holds | mean of 16 per-cell RMSEs 0.18547 (range 0.137–0.276). Model numbers not refit (issue 4's own run: LightGBM 0.1231) | TP-1 |
| 21 | Metric RMSE, origin source | `Metric.source` | Zindi page | holds | "The evaluation metric for this competition is Root Mean Squared Error." | MET-1 |
| 22 | Licence CC BY-SA 4.0 | Source | Zindi page | holds | "under a CC-BY SA 4.0 license" | |
| 23 | Target construction not documented | fit_reason, curation | Zindi page | holds | the page gives no index method or normalisation | USE-8 |
| 24 | Two-year surveys split over two year cells but never leak | Horizon block | country overlap | holds | Malawi and Tanzania in 2015 and 2016, Rwanda in 2014 and 2015: country out of every training side | |
| 25 | Source url / reference resolve | sources, metric.reference | fetch | holds | zindi.africa redirects (301) to zindi.world, the URL the definition uses | |
| 26 | Starter notebook uses urban_or_rural | curation | not run | untested | notebook not fetched; low stakes | |

**Metric (MET-1, MET-2)**

| Question | Answer |
|---|---|
| Does the source define it? | Yes, RMSE on the Zindi evaluation text, no params |
| Target scale | same 0–1 index as shipped; no transform |
| Unit of evaluation | one row; every test fold holds 139–1,585 rows |
| Inputs | y and prediction only; no scoring columns needed |
| Computable on each fold | yes: a train-mean prediction scores 0.137–0.276 in all 16 folds (computed directly with numpy, not through `metrics.scorer`) |
| Same meaning as the source | close: the source pools 7 unseen countries over 1998–2016; we score per country-year cell in 2014–2016, so cell RMSEs vary with each cell's target spread (dummy 0.137 to 0.276) |

**Findings**

1. **NEW (evidence for the KNOWN issue 4): population density is 0 only where the 2014 built-up layer is empty.**
   - Of the 1,397 rows with ghsl_pop_density = 0, 1,396 have zero built-up in every GHSL epoch, including 2000–2014.
   - On the rows before 2014 with no built-up by 2000 (2,477 rows), pop = 0 implies no 2000–2014 construction in 1,098 of 1,099 rows. So pop density partly reveals the masked 2000–2014 field.

     | Rows before 2014, no built-up by 2000 | built 2000–14 = 0 | built 2000–14 > 0 |
     |---|---|---|
     | pop = 0 | 1,098 | 1 |
     | pop > 0 | 622 | 756 |

   - This supports issue 4's reading: the population layer is allocated on the 2014 built-up layer that the definition masks. It adds a direct link to the masked field to the issue's regression evidence.
   - Effect on the task: small. The target mean barely differs between those groups (0.192 vs 0.188), so little label information comes through.
   - Rule: LEAK-10 and the curator's later-state rule (CC 2026-10-31). Remedy: none beyond issue 4's option B (mask pop before 2015), which removes this as well. Add the table to issue 4's Experiments.

2. **KNOWN (column audit doc fix): the "Year-comparison check" bullet is misleading.** The numbers hold (52/52, 5 groups, 25 rows), but the means change because different clusters are sampled. At the same place water, pop and lights do not change. The 11-21 assessment already says this, so the curation bullet and the assessment read as contradicting each other. Remedy: replace the bullet with the same-place check, as the column audit proposes.

3. **KNOWN: the target is one pooled min-max rescale over the whole release.** Exactly one 0 (2005) and one 1 (2013). Both extremes are in training years, so the test labels do not set the scale. This makes "Target harmonization using future actual states cannot be ruled out" partly testable: the rescale constants do use 2013 data for earlier rows, but an affine rescale gives no row-level information. Remedy: state it in the target bullet, as the column audit proposes.

Nothing refuted. Ranked, the only item that could change the data is finding 1, and it falls under issue 4's decision. The rest are wording changes.

</details>

<details><summary>Domain practitioner (2026-11-21)</summary>

**Domain practitioner: economic_well_being_prediction_challenge**

I am the analyst who maps local wealth between household surveys from geospatial layers, so that an agency can target support by place.

**Fit: approximate.** I agree with the shipped fit. The task is a real one, but the shipped test removes the one input I would always have: my country's own earlier surveys. The label construction and the dates of the layers are also undocumented (USE-5, USE-8).

**Metric: partly.** RMSE scores the wealth level, which I need when I compare countries. A quarter to a third of the error in each test cell is one offset for the whole country, and that offset plays no part in ranking places within a country.

**What I tested**

- One Slurm job (1401908), using the same cleaning and the same 16 country-year cells as the definition.
- Two learners: HistGradientBoosting (300 iterations) and ridge on log-scaled inputs.
- Two training sets: the shipped one (earlier years, other countries) and "own history" (earlier years, all countries, so my country's earlier surveys are included).
- A no-model baseline: the mean of my country's last survey.

Scripts and results are in the run folder (`actor.py`, `actor_cells.csv`, `1401908.log`). The definition's `dataset check` and probe logs are absent from the run folder, which holds only `precedent/`, so I could not read them.

| Training set | Model | RMSE | RMSE after removing each cell's offset | Spearman within cell | Recall of the poorest 20% | Share of MSE from the offset |
|---|---|---|---|---|---|---|
| shipped | HGB | 0.1270 | 0.0979 | 0.684 | 0.425 | 0.32 |
| shipped | ridge | 0.1133 | 0.0933 | 0.699 | 0.430 | 0.29 |
| own history | HGB | 0.1105 | 0.0913 | 0.725 | 0.478 | 0.25 |
| own history | ridge | 0.1092 | 0.0923 | 0.702 | 0.433 | 0.25 |
| own history | last survey mean | 0.1712 | 0.1588 | n/a | n/a | 0.12 |

Each value is the mean over the 16 cells. A random ranking recalls 0.20 of the poorest 20%.

- **Own history helps.** Adding my country's earlier surveys lowers RMSE in 13 of 16 cells for HGB and in 16 of 16 for ridge.
- **Every test country has earlier surveys in the file:** 1 to 9 earlier survey years per cell (Togo 2014 has 1, Tanzania 2016 has 9).
- **The offsets are large for HGB on the shipped split:** +0.146 for Malawi 2016, +0.156 for Malawi 2014, +0.136 for Rwanda 2014 and -0.133 for Mali 2015. The target runs from 0 to 1.

**Answers as the actor**

1. **Inputs at the moment I predict.**
   - Survey year: yes.
   - Distances, water and settlement history: yes.
   - Population and night lights: yes, and I would use the epoch that matches the year I map (WorldPop and GHS-POP are annual or 5-yearly; DMSP lights cover 1992-2013, VIIRS starts in 2012). Here they are one unknown epoch, likely 2015 for population. That is issue 4, KNOWN.
   - Urban/rural: in the data it is the survey's own cluster code. For places that were not surveyed I would take it from the census frame, so it is roughly available.
   - Missing although I would always have it: my country's earlier surveys (finding 1). I would also use admin units or coordinates and country-level covariates, which the source does not ship.
2. **Target.** I act on relative poverty by place. The asset index is the standard proxy in this field (DHS-style wealth index), but its formula, its harmonisation across surveys and the min-max rescaling over the training file are undocumented. That is issue 2, KNOWN, already accepted as approximate. I would want a number, and a ranking within the country.
3. **One row against one decision.** A row is one survey cluster, roughly a village. I usually target admin-2 districts, so I would aggregate clusters, and cluster-level error overstates my error. A test cell, "a later year in one country", is what I face. Training without that country's history is not what I face (finding 1).
4. **Would I use the model?** As a coarse prior, yes. A within-country Spearman of about 0.70 recalls the poorest 20% at about twice chance, roughly the within-country level reported in the satellite literature (Yeh et al. 2020, Chi et al. 2022). I would not use it for household-level targeting. I would distrust the country offsets: Malawi is placed about 0.15 too rich in both 2014 and 2016.
5. **Metric.** RMSE on the level scores my comparison of countries (MET-1). For targeting within a country I would choose by Spearman within the cell, or by RMSE after removing each cell's offset. On those measures, ridge's lead over HGB shrinks from 0.014 to 0.005 RMSE, and HGB is ahead on recall of the poorest 20%. RMSE is the competition's metric (MET-4). That competition was a student hackathon (AIMS, with Microsoft), so it carries less weight, but nothing on the shipped splits shows RMSE to be wrong. Keep RMSE and name the within-country ranking gap in the notes.

**Findings (ranked by how much they change the task)**

1. **NEW: the test denies the actor's own-country history (USE-10, USE-1).**
   - The use case is "filling in the gaps between the more expensive surveys". Every one of the 16 test countries has 1 to 9 earlier surveys in the file.
   - Under USE-10, a known entity's history is a legitimate input, which would make the split purely temporal.
   - The joint split instead stands for a country that has never been surveyed, which is closer to the source's unseen-country test.
   - Measured cost of removing that history: RMSE 0.127 → 0.111 for HGB (13/16 cells) and 0.113 → 0.109 for ridge (16/16).
   - Proposal: `use_case` and `fit_reason` should say that the test stands for a country without surveys of its own. Otherwise the stated use case ("between surveys") fits a temporal split that includes the country's own history. This bears on issue 3 (option B or C); it is not a separate leak. A reviewer decides.
2. **NEW: RMSE partly misses within-country targeting (MET-1, MET-4).**
   - 25-32% of per-cell MSE is one offset per country.
   - Within-country ranking (Spearman about 0.70, recall of the poorest 20% about 0.43) is what targeting uses.
   - Proposal: keep RMSE as the source's metric and add a note naming the gap. Changing the metric is not required.
3. **KNOWN (issue 4): population and lights are not from the year mapped.** As the actor I would use layers matched to the year. My view supports issue 4's option B for population.
4. **KNOWN (issue 2): the label is undocumented.** It is also min-max rescaled over the training file, with exactly one 0 and one 1 (column audit). That is fine for an approximate fit.
5. **Minor, NEW: the cluster is not the unit I act on.** Districts aggregate clusters. This needs a note only.

**What a domain expert would change**

- Write the use case as mapping a country that has no survey of its own, or else allow the country's own earlier surveys.
- Use covariate layers matched to the survey year (WorldPop or GHS-POP epochs, DMSP or VIIRS lights by year).
- Report a ranking measure within the country next to RMSE.

**Sources**

- The record, `dataset.py` and README.
- The column audit findings, the run folder.
- `use_case.md` (USE-1, USE-5, USE-8, USE-10) and `metrics.md` (MET-1, MET-4).
- The Zindi challenge description, as quoted in the record ("filling in the gaps between the more expensive surveys").
- Yeh et al. 2020, Nature Communications, and Chi et al. 2022, PNAS, from my own knowledge of the domain; I did not fetch them this session.

</details>

<details><summary>Precedent check (2026-11-21)</summary>

**Precedent check: economic_well_being_prediction_challenge (2026-11-21)**

**What I tested**

- Decision register run on the login node with thread caps: the run folder. It has 5,933 decisions and 43 flags. Four flags are on this dataset, all `exception_to_must`: two on SPLIT-3 (the record line and the splits.md Cases row) and two on USE-1. The USE-1 flags are a parsing artefact: the record cites USE-1 as the higher principle, it is not an exception to USE-1. The register finds no drift and no opposite-outcome pairs for this dataset.
- Read: the record (Comments, Review, issues 1-4, Horizon), dataset.py, the column-audit summary and logs, and the panel outputs. check.log has 28 checks: 0 errors, **1 warning**, 3 infos. task/ has the `no_spread` flag (known). group.log says "not a grouped task". leak/ and dtype/ are present.
- Precedents: the Cases tables of splits.md (SPLIT-3/10/12/14/15/33), split_tree.md (the Survey branch, "Definitions that ship another split"), leak_checks.md (LEAK-10, LEAK-30), selection.md (SEL-13/15) and use_case.md (USE-1). Sibling and closest records: wadden_sea_sibes_macoma_abundance, noaa_afsc_bottom_trawl_survey_cpue, anes_voting_2026, lt_vehicle_loan_default_prediction, ai4d_lab_tanzania_tourism_classification_challenge, geoai_ground_level_no2_estimation_challenge, airqo, crop_type/cropharvest/cropmapil, covertype, melbourne_housing_market, onlinenewspopularity, and the definitions that accept `splits_feature_missing_in_test`.

**Verdict per decision**

| Decision | Verdict | Closest precedents |
|---|---|---|
| Joint temporal × unseen-country split (SPLIT-3 exception; issue 3) | **not reasonable under the ranking, and departs from a like case without a fact that holds** (F1) | wadden_sea_sibes_macoma_abundance (grouped, not temporal, CC 2026-11-02 Andrej); lt_vehicle_loan_default_prediction (Myunghwan's USE-1 "exception" to a split Must, replaced by an amendment, Lennart 2026-11-05) |
| No gap (Horizon) | departs: the stated reason contradicts the reason for the split (F2) | zillow_prize, house_sales (gap for delayed labels); wadden_sea (historical map, no temporal test) |
| Newest three years as test windows (Horizon A) | departs from SPLIT-15's preference; the reason given is not one the rule accepts (F3, partly KNOWN) | anes_voting_2026 and noaa_afsc (nine windows spread back over the history); cooking_time_1m (reopened when its window reason rested on the floor) |
| 16 cells counted against the SPLIT-33 target of 9 | no precedent; a reviewer should confirm how they are counted (F4) | memory rule and SPLIT-15: "test parts that share one training side are one split"; the record's own mediator: "three annual windows ..., not sixteen independent temporal replications" |
| Issue 4, mask population density before 2015 (B) | consistent; two facts are missing from it (F5) | LEAK-10 later-pull clause ("blank located cells"); melbourne_housing_market (blanked late lookups); this definition's own GHSL masks and land-cover drop |
| 2014 cells: masked GHSL fields missing in train, present in test | **new check warning without a curator acceptance** (F6) | anes_voting_2026, college_scorecard, onlinenewspopularity, home_credit, delivery_eta_1m (each accepted by Lennart in `accepted_check_warnings`, 2026-11-10/11) |
| Scope: remote-sensing products (SEL-13 against SEL-15) | consistent if written down; never decided in the record (F7) | covertype (Yes, GIS layers); geoai and airqo (retrieved quantities read as measurements, Myunghwan accepted geoai on 2026-10-30); crop_type, cropharvest, cropmapil, athabasca (No: raw reflectance used to recognise content) |
| Licence `CC BY-SA 4.0` and a public GitHub mirror | mirror consistent; licence string inconsistent with its Zindi sibling (F8) | ai4d_lab_tanzania (pinned GitHub commit with size and SHA; licence "CC BY-SA 4.0; publisher also states non-commercial ...") |
| Target rescaled over the training file (column-audit doc fix) | consistent if the note follows LEAK-30's shape (F9, KNOWN) | LEAK-30 Cases (keep with a `Potential leak, kept on purpose:` note) |
| Supplied index, approximate fit (issue 2, resolved) | consistent | diabetes_3 and blood_tests_drink_prediction (USE-5); ljubljana_primary_tumor (USE-8, approximate fit) |
| RMSE, the source's metric (MET-4) | consistent | the 2026-11-05 metric CC |
| Year as an input | consistent (the time-column actor test: the agency knows the year it maps) | |
| R/U decoded (CLEAN-12); country and ID dropped after the split | consistent | |
| Land cover dropped; GHSL 1990-2000 and 2000-2014 fields and the not-built residual masked (LEAK-10) | consistent | onlinenewspopularity; melbourne_housing_market |

**Findings**

**F1 (NEW angle on issue 3): the joint split is a Must exception that the ranking does not allow, and a like case went the other way**

- **Rule.** SPLIT-3 is a Must ("never both; the use case decides which"). principles.md, "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment."
- **The stated override does not hold on the record's own facts.** The record claims that USE-1 (P3) requires a future-year test. But:
  - the definition's `use_case` says "An agency estimates **historical** local wealth where survey coverage is missing";
  - the source says "filling in the gaps between the more expensive surveys";
  - the Horizon block says "the use case reads as historical";
  - the source's own Test.csv covers 1998-2016 in seven other countries (issue 3's Answer).
  A grouped-only split does not break USE-1. It fits the written use case. So the exception rests only on the curator's call of 2026-11-02, not on a higher Must.
- **Like case decided the other way: wadden_sea_sibes_macoma_abundance** (CC 2026-11-02, Andrej). Its splits comment says: "Grouped rather than temporal: the use case maps a surveyed year between stations, not a future year (SPLIT-3) ... the later surveys are in training too; they add rows, not the test year's outcome." It is the same shape: a survey over places and years, and a map of past rounds where no sample was taken.
- **Same curator, same pattern: lt_vehicle_loan_default_prediction.** Myunghwan's "Exception to SPLIT-10 (2026-10-23) ... Serves P3 (USE-1)" was not kept as an exception to a Must. Lennart replaced it with an amendment and an application (CC 2026-11-05: "an application, not an exception"). The register lists these two as the only "USE-1 override" exceptions.
- **Effect on issue 3.** Option A ("a listed departure") treats this as a SPLIT-36 (Should) departure. The binding rule is SPLIT-3 (Must), which takes no exception. The options that fit the principles are B (the leaf, as wadden_sea) or C (an amendment or a new branch, as lt_vehicle), unless a forward fact is recorded (option a below). This belongs in issue 3's Consistency bullet and options. Per the scoping rule it is not a new issue.

Drafted for issue 3 (turn shape):

> **Consistency check (AI, 2026-11-21):** the joint year × country split departs from SPLIT-3, a Must, and wadden_sea_sibes_macoma_abundance (2026-11-02, Andrej) mapped a past survey between unsampled places with a grouped split only, later rounds in training. What sets this dataset apart?
>
> - **Problem:**
>   - SPLIT-3 takes no exception; the record's override cites USE-1, but the written use case ("historical local wealth where survey coverage is missing"), the source's gap-filling aim and its Test.csv (1998-2016) all read as historical, which the grouped leaf already tests.
>   - The only other USE-1 "override" of a split Must (lt_vehicle_loan_default_prediction, Myunghwan, 2026-10-23) was replaced by an amendment (Lennart, 2026-11-05).
>
> | | Option | What it does | Pro | Con |
> |---|---|---|---|---|
> | a | Record a forward use case | The agency maps the newest round in countries whose last survey is older; the use case is rewritten so, and the gap follows SPLIT-10 (Horizon C) | keeps the curator's 2026-11-02 task with a fact behind it | contradicts the source's gap-filling text and its all-years Test.csv; needs the gap |
> | b | Treat it like wadden_sea | Grouped · UnseenGroup by country, 3-fold over all years (issue 3 B) | follows the tree, the leaf and the precedent | drops the later-year test the curator asked for |
> | c | Reopen wadden_sea to match | A joint split there too | one rule for both | wadden_sea measured that later rounds add rows, not the outcome |
> | d | Amend SPLIT-3 | Allow the joint split where a source holds out places and the curator requires later years | a deliberate change, as for lt_vehicle | one dataset; issue 3's own con for C |
>
> **Recommendation:** b, unless the curator states the forward fact of (a).
>
> [SPLIT-3: a non-IID task is grouped or temporal, never both.] [principles.md, "Exceptions and amendments": a Must has no exceptions.] [SPLIT-36: a departure from the leaf goes to a reviewer.]

**F2 (NEW): the no-gap reason contradicts the reason for the split**

- The Horizon recommends no gap because "the use case reads as historical (filling the gaps between past surveys)". The SPLIT-3 override needs the opposite reading ("future-year survey-gap task").
- Both cannot hold. Read as forward, SPLIT-10 asks for the label's delay (Horizon C; precedents zillow_prize, house_sales). Read as historical, the temporal half of the split has no use-case reason (F1).
- The Horizon decision depends on issue 3. It should be asked after issue 3, or say that A holds only under a forward reading with a gap. It falls away under issue 3 B.

**F3 (partly KNOWN, footnote x21e3; NEW precedent angle): newest three years**

- SPLIT-15 (amended 2026-11-10, Lennart and Andrej): prefer windows in other years. "Walking back from the newest ... needs its reason, such as a history too short for others."
- The notes give "keep every training side at 66% or more". The rule's floor is 50%, so this is not a reason the rule accepts. cooking_time_1m was reopened when its reason ("the only weeks above the floor") rested on the floor.
- Like cases with long histories spread their windows: anes_voting_2026 (nine elections, 1996-2024) and noaa_afsc (nine windows, 2009-2026).
- With 19 survey years, option B should be measured (`dataset windows`) before A is recommended.

**F4 (NEW, low): how the 16 cells are counted**

- Each cell's training side is "year < t and country != c". Within a year the training sides differ only by one country's rows.
- The Horizon counts 16 splits against SPLIT-33's target of 9. The record's mediator calls them "three annual windows with country-specific training sets".
- No precedent counts such cells. Under the "test parts that share one training side are one split" reading, the count is 3 windows, which triggers `splits_below_target` and needs a reason in the comment.
- A reviewer should say which reading applies. This is moot under issue 3 B.

**F5 (issue 4; consistent, two facts missing)**

- **B follows precedent.** LEAK-10's later-pull clause says to blank cells that can be located. melbourne_housing_market blanked its late lookups. This definition already masks the 2000-2014 GHSL fields and drops land cover for the same reason.
- **Like cases not treated alike.** The 2026-11-21 Assessment says water, population and night lights are each "one read for all rows". Issue 4 masks only population:
  - Night lights stay because "their epoch is undetermined". Any single epoch inside 1994-2016 is a later state for the rows before it. onlinenewspopularity keeps such values only when the traceable part shows no gain. Lights carry the largest gain: dropping them costs +0.0134 RMSE, and 16 of 16 cells get worse (ablation.csv). The fact that could set them apart is the regression: little weight on construction in 2000-2014 (0.119 against 0.463 for population). It should be stated as the reason.
  - Water is not mentioned. LEAK-10's "unless the data shows they did not change" is its likely distinguishing fact (stable water bodies). It should be written down.
- **B's Con is understated.** Masking population before 2015 leaves it 100% missing in training for the 2015 cells too, because they train on years before 2015, not only the 2014 cells. The 2014 cells lack it on both sides. This adds a third column to the warning in F6.

**F6 (NEW): a check warning with no curator acceptance**

- check.log (28 checks) warns `splits_feature_missing_in_test`. `ghsl_built_2000_to_2014` and `ghsl_not_built_up` are 100% missing in training and observed in the 2014 test cells. `accepted_check_warnings` is empty. The 2026-11-05 runs had zero warnings (27 checks), so this is new on the current check.
- Every precedent accepted this warning with a curator decision written in `accepted_check_warnings`: Lennart's cross-dataset item of 2026-11-11 (anes_voting_2026, college_scorecard, onlinenewspopularity, home_credit) and issue 2 A of 2026-11-10 (delivery_eta_1m).
- Here the gap comes from our own mask, not from a recording change. The curation comment calls it "an intentional coverage change", which is not a curator acceptance.
- It needs a curator mark (or it joins issue 4, whose option B adds `ghsl_pop_density`).

**F7 (NEW, low): scope under SEL-13 was raised at screening and never settled**

- Screening (2026-10-22) and the 2026-10-31 Assessment asked for an argument from the columns. No CC line and no Resolved turn answers it.
- The precedents point to keeping it:
  - The inputs are mapped quantities aggregated to 5 km (built-up fractions, modelled population, calibrated lights) plus GIS distances. That is close to covertype (Yes) and to geoai and airqo (retrieved quantities read as SEL-15 measurements; geoai accepted by Myunghwan, 2026-10-30).
  - The crop_type, cropharvest, cropmapil and athabasca rejections had raw reflectance used to recognise image content.
- One line in `curation_comments` stating the SEL-15 reading would close it. A curator issue is needed only if the panel disagrees.

**F8 (NEW, low): the licence string**

- The definition says `CC BY-SA 4.0`, and the record holds no evidence for it.
- The Zindi sibling ai4d_lab_tanzania records the page's own words: "CC BY-SA 4.0; publisher also states non-commercial research or education use (competition rules)". Other Zindi definitions say "Zindi Competition Rules".
- Read the source page and align with Tanzania if it carries the same clause. The column audit's GitHub-mirror download follows Tanzania's pinned-commit precedent (size and SHA check) and is consistent.

**F9 (KNOWN, column-audit doc fix): the target rescaled over the training file**

- The target has one 0 and one 1, so it was rescaled over the whole training file.
- By analogy with LEAK-30, write it as a `Potential leak, kept on purpose:` note (scaling over all rows, rows of later years included), not as a plain fact.

**Not found**

- No drift by Myunghwan on the same rule. Every other decision of his here follows his CCs of 2026-10-31 and 2026-11-02.
- No third exception of the same reason, except that two USE-1 "overrides" of split Musts now exist (lt_vehicle, already amended; this one). If issue 3 keeps A, it is the second exception of that kind, and the next one makes an amendment due.

</details>

<details><summary>Blind review (2026-11-21)</summary>

**Blind review: economic well-being prediction challenge (Zindi)**

**Verdict:** I would include it with changes. The task is real, the signal is real and the data look genuine. But the prepared version drops the country column, which carries the source's own evaluation design, and uses a split on survey year that does not stand for any use. The hiding of post-survey features is half done, and the boosted trees and linear models are tied on it.

**Concerns, most serious first**

**1. The country is gone, and the year split does not stand for the use**

- **Source design.** The source holds out whole countries. The challenge page says the test set is "surveys in 7 different countries not covered in the training data" (training covers 18 countries). It states the use as "filling in the gaps between the more expensive surveys". A forum thread ("Country Column") confirms the raw file has a `country` column. It is missing here.
- **What the year windows really are.** Survey years are irregular (1994–2016, no 1997/2000–2002). Each year holds one or a few country surveys, so a year window is a mix of country-surveys. Some come from countries already in training and some do not, and that mix is not controlled. Only 8.5% of target variance lies between years, so the split mostly measures transfer across surveys.
- **Measured gap between splits (LightGBM, all features):**

| Split | R² | RMSE |
|---|---|---|
| Random 5-fold | 0.77 | 0.093 |
| Expanding year windows (mean of 16) | 0.49 | 0.126 |

- **Unstable windows.** Results swing by window: the 1998 window has R² of −0.11 and a mean bias of +0.14.
- **Change:** restore `country`. Then split by country, as the source does (unseen countries), or by country-survey. Or keep a forward split and make the country explicit, so that "next survey in a country already seen" is what gets scored. Drop or merge the first windows: 1998 trains on 531 rows and 1999 on 829.

**2. Hiding post-survey features is inconsistent, and the missingness encodes the year**

- **What was hidden.** `ghsl_built_2000_to_2014` and `ghsl_not_built_up` are NaN for every row before 2014. `ghsl_built_1990_to_2000` is NaN for every row before 2003 (all rows from 1994–1999). The missingness is therefore a pure function of `year`.
- **What was left.** `nighttime_lights` and `ghsl_pop_density` are also single snapshots. The source does not give their year. GHSL population and VIIRS lights are very likely about 2015, yet they are kept for 1994–2013 rows. So a 1994 cluster is described by lights about 20 years later.
- **Why it matters.** Nighttime lights is by far the top feature (about 60% of total gain).
- **Change:** pick one rule. Either treat all layers as static covariates and keep them all, which is honest for the "fill gaps now" use. Or restrict to survey years where every layer predates the survey. Document the product years either way. I could not confirm them from the Zindi page.

**3. Weak separation between methods**

Mean RMSE over the 16 year windows:

| Model | RMSE | R² |
|---|---|---|
| Train mean | 0.199 | — |
| Ridge on log-transformed features | 0.122 | 0.53 |
| LightGBM, all features | 0.126 | 0.49 |
| LightGBM, no year | 0.122 | 0.52 |
| LightGBM, 3 features (urban, lights, population density) | 0.126 | 0.49 |

- **Reading.** There is real signal, but the task barely ranks methods under this split. Including `year` hurts (0.126 vs 0.122).
- **Change:** give `year` as a feature only if the split makes it meaningful.

**4. Repeated coordinates with different targets (minor)**

- **Evidence.** 205 rows share exact (`dist_to_capital`, `dist_to_shoreline`) pairs with others, mostly in the 1994–1995 surveys. Within such a group the satellite features are identical, but `urban_or_rural` and the target differ (target SD about 0.036). 129 rows have fully identical feature vectors.
- **Reading.** These look like coarse or region-level coordinates for old surveys, not copies of the same record. Expect a little label noise. No change needed beyond a note.

**5. Target definition is vague**

- **Source wording.** "a derived 'wealth index' based on responses in various household surveys ... scale from 0 to 1". It calls the index one measure across surveys and countries, but gives no formula.
- **Evidence.** Exactly one row sits at 0 and one at 1, which suggests min–max scaling over the training file.
- **Reading.** DHS-type wealth indices are normally relative within a survey. Comparability across countries and years is claimed, not documented. This is acceptable, but note it.

**Other points**

- **Weight column:** none is labelled.
- **Preparation:** column types and encodings are fine. `urban_or_rural` is categorical, and there are no NaNs other than the hidden layers.

**What I could not check**

- The exact year and product of the nighttime-lights and GHSL population layers.
- The formula of the wealth index and the underlying surveys (DHS?).
- The licence and redistribution terms of the Zindi data.
- Which countries fall in each year window.
- The exact 16 windows used by the curators. I assumed expanding windows, each testing one survey year from 1998 to 2016.
- Strong models (TabPFN, tuned GBMs). I ran only default LightGBM and ridge.

Sources: https://zindi.world/competitions/economic-well-being-prediction-challenge (overview), .../data (data page), .../discussions (country column thread). Scripts and logs: work/baseline.py, work/1401920.log. I opened no file outside the clean room except the allowed interpreter.

</details>

<details><summary>Task gamer (2026-11-21)</summary>

**Task gamer report: economic_well_being_prediction_challenge**

**Verdict:** I found no exploit beyond the noise level. The largest effect works against an honest model: each split leaves the test country's own earlier surveys out of training. Adding them back cuts the mean RMSE from 0.1246 to 0.1098.

All numbers are the mean RMSE over the 16 shipped splits from an untuned LightGBM (`work/attack.py`, log `work/1401922.log`, Slurm). Lower is better. To set the noise level, I refit the baseline 5 times, each with a random column added. The mean RMSE ranged from 0.1225 to 0.1241, and a single split moved by up to 0.011.

**Exploits**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Survey-level feature means over the test window (urban share, mean lights, cluster count) | attack.py `unit_mean_only` | 0.1246 | 0.1154 | -0.009 mean (+0.024 to -0.045) | Probably yes: the cluster list of a survey is fixed before fieldwork | None needed. If the curator decides the cluster list is not known, say so in the prediction point |
| 2 | Within-survey ranks of each feature | `unit_rank_only` | 0.1246 | 0.1178 | -0.007 mean (+0.009 to -0.026) | Same as 1 | Same as 1 |

**A flaw that hurts an honest model**

| # | What is wrong | Honest choice | Shipped score | Honest score | Gain | Fix |
|---|---|---|---|---|---|---|
| H1 | Training leaves out every row from earlier surveys of the test country. In each split, 129 to 2,381 rows dated before the test year are missing from training: repeat 2 drops 2010, 2012, 2014 and 2015, and repeat 4 drops 2003, 2008, 2009 and 2014. | Train on every row dated before the test year | 0.1246 | 0.1098 | -0.015 mean. 15 of 16 splits improve (r2: 0.176 to 0.099; r5: 0.133 to 0.099). r9 is unchanged (0.0985 to 0.0994, within noise). | Make the regime and the prediction point agree. **Either** put the test country's earlier surveys back into training (a pure temporal split, as the prediction point describes) **or** declare the task as "a new country, later in time" in `task.md`. Right now the kit says temporal only. |

**Mechanisms**

- **H1.** I identified the excluded rows by comparing each split's training set with all rows dated before its test year. Each excluded set is a few whole survey years, and the same set recurs across repeats that share a country: repeats 2, 5 and 13 all drop `{2010: 827, 2012: 140}`. The model's error is mostly a survey-level offset. The baseline's mean bias per window runs from -0.133 to +0.158. If each window's mean bias were removed, the RMSE would be about 0.095 instead of 0.125. The country's own past surveys pin that offset down. A model deployed at the stated prediction point ("location and year known, before the survey is fielded") would have those past surveys, so the split is harder than the use case it states. This is a design question, not a leak. The original Zindi competition tests on unseen countries, and the kit has no country column.
- **Exploits 1 and 2.** These group rows by survey. For the test side, I used the test window itself. For training, I rebuilt country-surveys from the split membership pattern, which is an approximation: the other countries' rows are pooled by year. The gain comes from estimating the country-level offset from aggregate geography. I count it as signal, not an exploit, because the cluster list is known before fieldwork. One fact would settle it: whether a deployed model gets a whole survey's cluster list at once. Two caveats:
  - The gain is uneven. Four splits get worse by more than the noise level (r6, r7, r8, r12).
  - Exploit 1 adds about 20 extra columns. Do not compare it with the one-column noise run as if they were the same test.

**Attacks that found nothing (mean RMSE; the baseline is 0.1246)**

| Attack | Score |
|---|---|
| Format-only features (decimals, zeros, missing flags per column) | 0.1314, worse than the baseline: no recording artefact |
| Format features added to the full model | 0.1242, within noise |
| Global percentile ranks over all rows (train and test) | 0.1252 |
| Year dropped from the inputs | 0.1232, within noise. Its effect on single splits can be large in either direction (r13 0.189 to 0.126; r10 0.115 to 0.148) |
| kNN label (k=10) on standardized geography | 0.1366 |
| Exact copies of test rows in training: whole feature vector, or the (dist_to_capital, dist_to_shoreline) pair | 0 copies in every split |
| Missing values | The masks are deterministic by year: built_1990_to_2000 is missing for survey years before 2003, built_2000_to_2014 and not_built_up before 2014. The mask carries nothing beyond `year`. |

Single features (lowest RMSE wins):

| Feature | RMSE |
|---|---|
| nighttime_lights | 0.1237 |
| urban_or_rural | 0.1334 |
| ghsl_pop_density | 0.1439 |
| built_1975_to_1990 | 0.1461 |
| built_pre_1975 | 0.1545 |
| built_1990_to_2000 | 0.1548 |
| not_built_up | 0.1658 |
| built_2000_to_2014 | 0.1702 |
| dist_to_capital | 0.1804 |
| water | 0.1851 |
| year | 0.1880 |
| shoreline | 0.1886 |

**Nighttime lights alone (0.1237) equals the full model (0.1246).** That makes the task close to a one-feature task. It is also the one column whose date I could not check:
- Its values (continuous, maximum 383) look like VIIRS, which starts in 2012, so it is probably a single composite for every row.
- For the 2014-2016 test rows, that composite may be from the survey year or later, which would be after the prediction point.
- The fact that settles it is the year of the lights composite (and of `ghsl_pop_density`). The Zindi data page does not give either year.

**Comparing the kit with the published data**

The Zindi data page lists columns the kit does not have:
- the landcover fractions (crops, urban, permanent and seasonal water);
- the country, latitude/longitude and ID metadata.

The kit also masks the GHSL built-up epochs that end after the survey year. Those changes remove the obvious time artefacts. I did not download the Zindi files (login required), so I could not look rows up in the published data.

**What I could not check**

- The years of the nighttime lights and population density rasters.
- The country of the training rows that never appear in a test window.
- Winning write-ups: I found no leak or "magic feature" thread. The only public post is the 4th-place thank-you note (https://zindi.world/competitions/economic-well-being-prediction-challenge/discussions/7283), which has no method.
- Public sources I used: https://zindi.world/competitions/economic-well-being-prediction-challenge and its /data tab.

</details>

<details><summary>Column audit (2026-11-21)</summary>

**economic column audit — built from public GitHub copy (same SHA); 1 issue (pop density mask); issue 3 answered (Test.csv 1998-2016, 7 countries); facts hold**
Doc fixes (8): replace year-comparison bullet with same-place check; known text (one read each); lights radiance scale epoch undetermined; dist_to_capital official capital km; target one 0 and one 1 (rescaled over training file); CAR locality points; splits_comment source Test.csv; download_description public mirror (curator call).

</details>

<details><summary>Mediator</summary>

**Focused current-main mediation: economic well-being**

Observed 2026-11-05 UTC. Independent AI advisory judgment for Myunghwan. Current-main base: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Audited postdecode definition SHA-256: `43a922924f61ca63478edd77c10a1df5506c01245cfa2d7031d86f17744b2b6f`.

Verdict: **ship after the routine documentation changes below; no new curator input.** Preserve Myunghwan's existing ship decision and his November 5 request to reuse the earlier decisions. This recommendation records the requalification, not a fresh human mark.

Validity: USE-1/5/8 support the accepted retrospective survey-gap task and supplied-index approximate fit. Established future-state fields remain masked or omitted under LEAK-10. SPLIT-1/4/14 are supported by reconstructed chronology, whole-country exclusion and support. The joint regime departs from SPLIT-3; document its candidate-specific higher-ranked USE-1 override and explicit user authority, retaining the general rule. Exact retained epochs, target construction/harmonization, interview ordering, original publisher-byte identity and label publication dates remain cannot-verify under EV-7. No new evidence establishes a contradiction of the accepted interpretation.

Value: fresh sixteen-cell probes and verified reuse of bounded train-only tuning support useful signal (TP-1/2). The `no_spread` flag remains investigated and disclosed; neither the fresh probes nor the historical tuning establish reliable family separation. The actual gamer report demonstrates no unavailable-information exploit. Quality: the lossless CLEAN-12 Rural/Urban decoding is complete, with refreshed row ordering and ID-aware reuse evidence.

Weighed: source and temporal/target provenance gaps remain a limitation; supported transfer-cell sizes and measured signal favour retention. For the curator: **zero genuinely new questions**. No issue should be invented to fill a quota.

**Changes to make now**

1. Complete the formal SPLIT-3 departure in the record, dataset notes and `knowledge-curation/references/splits.md` Cases table, as the precedent checker specifies. Name the actual November 2 confirmation and November 5 preservation request separately. State that replacing either strictly earlier years or unseen-country transfer changes this accepted USE-1 task; USE-1 is Must at P3 and outranks P4 SPLIT-3. Describe this as a candidate-specific higher-ranked use-case override in the workflow's `exception` category. Keep SPLIT-3's general Must wording, existing vocabulary and temporal backend unchanged. This is documentation of existing authority, not an ordinary Should exception or a newly granted generic waiver. If the register flags the formal Must departure, explain its resolution rather than suppressing the flag.
2. Preserve a decision/application ledger with the original inputs, dates and snapshot identities, the current package identity, and the verified unchanged semantic scope. Keep resolved issues 1 and 2 with their original resolution dates in the current REVIEW.md. Earlier deletion/archive handling remains dated history; do not claim it followed today's retain-resolved-issues instruction. Use current focused-panel attribution and preserve the historical full ten-role panel/debate separately. These follow review-added Step 4 and EV-7/8.
3. Use `qualification-final.json`, `final-split-audit.md`, final leak/raw outputs and `task-final` for present identities/counts. Preserve predecode reports as historical. Add the completed gamer report with the access limitation below. Complete the focused editor's review, refresh generated documentation/checks after the note changes, and perform the already requested build-stage verification under its own procedure. This mediation does not attest to a build or editor pass that has not happened.

**Issues for the curator**

None newly established. Keep the existing repair trigger: concrete evidence of an actual later-state measurement, materially different target, broken membership or other new validity defect reopens the affected decision. Unknown epochs remain unknown; their continued absence alone supplies no new contrary evidence or reason to repeat approval. Later production of a historical-state layer is already permitted by the October 31 decision. The gamer's GHSL observation, imagery through 2014 produced in 2015, therefore adds no new scientific choice for the accepted reconstruction task.

**Agreed facts and evidence**

The source-index task predicts one released survey-cluster observation's 0–1 wealth index for a later survey year in a country wholly absent from training. The frame has 21,454 rows and twelve predictors. Country and opaque ID construct/check the splits and leave the learner frame. Source RMSE remains appropriate; the metric audit finds native and direct arithmetic equal on every fold (MET-1/2/3/4/11). No new metric input or target transformation is required.

The final split auditor independently reconstructs all 32 train/test ID sets. Every test is one observed country-year cell in 2014–2016; train is exactly `year < t AND country != c`. The sixteen tests contain 6,256 distinct IDs, each once; test sizes are 139–1,585 and every target varies. The smallest train is 14,231 rows, 66.33% of the full sample. These are three annual windows with country-specific training sets, not sixteen independent temporal replications. Tests share countries and training rows; no independence or significance claim follows.

The CLEAN-12 decoding preserves all IDs, targets, numeric values, masks and feature meanings. It changes 21,436 canonical ID positions. Final frame hash is `aaf6121b72ee2b21705252cf7afc10ac8342dd345e3bef1321174543424b9100`. Reversing only the labels and restoring historical ID order reproduces historical hash `039c9d0cb264d52d0a0481d21ef4c08b95d84c3eae602c4258092a888fdec9ab`. The independent final auditor reindexes all 48 retained family/cell prediction vectors by ID, verifies their truths and test ID sets, and reproduces native/original/direct scores within 1e-14. This supports reuse of those exact predictions, not direct reuse of old positional arrays or a claim that stochastic refits must be identical.

`qualification-final.json` records 27 native checks, zero errors, zero warnings and three infos: conflicting predictor profiles, integer-year calendar metadata, and the explicit time/country repair check. `final-split-audit.md` reports zero full-profile cross-split copies across all sixteen splits and 6,256 test evaluations, and successful final leak/raw reruns. Classification-only format/interpolation diagnostics are inapplicable to this regression. Exact-copy absence does not date layers or prove absence of spatial dependence. The inspected suite log records 2,016 passed, 286 skipped and twelve warnings; these pytest warnings are distinct from the dataset's zero check warnings.

Fresh `task-final/economic_well_being_prediction_challenge.json` covers every shipped split. Macro-cell RMSE is dummy 0.185473, linear 0.118280, random forest 0.117899 and untuned LightGBM 0.127248. Linear beats the dummy on all sixteen cells; the only flag is `no_spread`. The historical bounded two-option, training-only qualification, preserved and re-scored through final ID alignment, has ridge 0.118259, LightGBM 0.118795 and forest 0.120413. This is limited local tuning, with no exhaustive HPO or formal benchmark-method comparison. TP-1/2 and EV-3 support retaining the real signal without converting the unresolved spread limitation into a rejection or claiming TP-3's demonstrated-spread premise.

**Gamer findings and their rule interpretation**

I inspected the actual final `participant_kit/task-gamer-report.md`, its primary attack/control scripts, per-split/summary outputs, input identity list and task files. Report SHA-256 is `b5267716a0ceb0763d79b434f65e0de0133415965a296da55ddb95e28b8b91bf`; the inspected task-final JSON hash is `bc62f61fd5332e0bcbedb9aebc7f933e493637a60a222eab09b7397bbb11b352`. I independently verified all six kit input hashes against the gamer's recorded identity list. I did not repeat model fits or independently reproduce every auditor experiment.

| Suspected shortcut | Actual measured comparison across all sixteen splits | Mediation |
|---|---|---|
| Whole-frame frequencies, using future/test feature rows | Honest LGBM 0.124379 RMSE; whole-frame frequency 0.120247; train-only frequency 0.118123; eleven-random-feature control 0.120303. Three further random seeds give 0.120890, 0.121343 and 0.120935. Frequency adds twelve columns, so the random control is comparable rather than exactly width-matched. | All-row statistics would implicate LEAK-5/30 if supplied by curation. None are shipped. A participant method learning from unavailable test-block information is an evaluation issue under LEAK-9. These attack comparisons establish no distinct unavailable-information advantage; legitimate train-only frequencies are better, and the nominal gain is close to random-feature fitting effects. No significance assertion or new fix follows (EV-1/6/9). |
| Apparent format-only gain | The first representation scores 0.117969 but includes urban/rural, zeros and string lengths that can encode numeric magnitude. Removing urban/zero indicators scores 0.128041, worse than baseline. Raw CSV token precision is absent from the kit. | No class/target-dependent recording mechanism is demonstrated under LEAK-13/15. Deterministic coarse feature signal available for the row is legitimate USE-6 input. This result does not prove all source formatting harmless. |
| Row position, copies, chronology | Row-order gain is only 0.000166, improving five cells; position-only is worse. Full, no-year and distance-pair exact lookups find no cross-split matches; the tested near-copy threshold also finds none. No train/test row overlap or training year at/after the test year. | No new order shortcut, repeated-entity leak or chronology failure is shown (LEAK-16/17/21, SPLIT-9/22). Country-disjointness is unavailable from the kit alone and is established separately by the split auditor. More distant geographic dependence remains outside this test. |
| Removing endpoint surfaces or older history | Dropping the two 2014 surfaces improves RMSE by 0.000464 on six cells; restricting history to 2010 onward worsens it by 0.001992. Single-feature lights is 0.123667. | No harmful-history defect or new later-state mechanism is established. Score changes cannot date a feature (EV-2), and history/splits cannot be selected from these gains (SPLIT-21). No feature removal is justified. |

Whole/test ranks worsen mean RMSE; test-only frequencies equal baseline. Missingness-only is 0.185329, close to dummy. The gamer used training labels for fitted rules and evaluated completed predictions against held-out labels. These are bounded adversarial checks, not proof that the task cannot be gamed. External label matching, geographic coordinate matching, exhaustive vintage reconstruction, source notebooks and uncertainty resampling were not executed.

The initial participant-review attempt did not run. A replacement independent review received only the participant inputs and public sources. The inspected scripts and report show no apparent curation-note contamination. Access separation was contractual, not OS-enforced; no independently audited complete read log is claimed. Input hashes establish identity rather than access enforcement.

**Consistency and retained uncertainty**

I agree with `precedent-review.md`. The decision-register's zero flags are a search result, not semantic clearance; its selected entries omit important enriched rule labels. USE-5's undocumented-label allowance and the diabetes_3 / blood_tests_drink_prediction Cases support the unchanged approximate supplied-index interpretation. Current MET-4 does not require replacing suitable source RMSE. CLEAN-12 supports the completed nominal-code expansion. SPLIT-3 requires the formal scoped override described above; there is no evidence of a third repeated exception or authority to amend the general rule.

The original annual-timing and ship decisions remain authoritative, including the explicit temporal × unseen-country correction and supplied-index acceptance. The fixed-period control also varied across all 52 country-year comparisons, so that comparison did not establish feature epochs.

This is the current **focused** claim/column/split/precedent/gamer plus mediator review. The editor still owns its cold read; the earlier full panel/debate remains historical. Exact water/population/light epochs, survey programme, target normalization/harmonization, interview timing, publisher-byte authentication and label publication delay remain unverified. The retrospective approximate framing and already accepted limits must stay visible (USE-8, EV-7). The current evidence supports no additional scientific remedy.

This mediator inspected the supplied qualification evidence and input hashes. It did not fit models or rerun raw-data qualification.

</details>

<details><summary>Claim audit</summary>

**Focused claim audit: economic_well_being_prediction_challenge**

Editor chronology note: this report inspected the predecode definition. Its byte/order-equivalence statements describe that snapshot; the Final split audit and Mediator sections establish the final decoded package and ID-aware score reuse.

Observed: 2026-11-05. Reviewer: independent claim-auditor, AI advisory assessment for Myunghwan. Checkout base: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Audited definition SHA-256: `dc4703333b0eb11ab3d422daec3ca3fa2914be926a6410d4dfe7f9e2264d86b3`.

Verdict: ready for the remainder of the focused requalification, with the previously accepted limitations preserved. This audit finds no new scientific issue and needs no new curator input. It is not a full replacement panel, a final human verdict, or a claim-ownership operation.

Validity: the actor and retrospective survey-year target remain coherent (USE-1/5/8); the exact frame and all sixteen country-exclusive forward-year memberships match the accepted qualification. The annual timing approximation and candidate-specific joint-regime decision retain their original October 31/November 2 provenance. Feature epochs, target construction/harmonization, and interview-level ordering remain unknown, as before (EV-7). Their continued absence is not new contradictory evidence.

Value: the current source explicitly names RMSE, the current native scorer matches direct RMSE on every fold, and re-scoring the retained predictions reproduces all 48 family-cell results. Prior signal and `no_spread` interpretation can be reused; no fresh model ranking is claimed. Priority remains 3.

**Tests executed**

`audit-claims.py` loaded the migrated definition through Python, ran native checks without report writes, independently reconstructed masking and omissions from raw rows aligned by ID, reconstructed every train/test membership, checked exact predictor copies across every split, and compared every fold's native RMSE with direct arithmetic. It also compared the full frame hash, row manifest and all exact memberships with the retained October 31 qualification.

`audit-rescore.py` checked the retained predictions' truth and row positions against the current frame and splits, then recomputed every score through the updated-main scorer. `claim-priority-factors.json` came from the current main priority helper. No models were fitted by this auditor.

- Raw: 5,829,604 bytes, SHA-256 `caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c`; 21,454 × 19; no missing cells.
- Prepared: 21,454 × 13 including target; twelve predictors; 31,760 masked cells. Frame hash `039c9d0cb264d52d0a0481d21ef4c08b95d84c3eae602c4258092a888fdec9ab` equals the prior qualification.
- Native check: 27 checks, zero errors, zero warnings, three infos. The infos are 129 rows sharing final predictors with different targets, integer-year calendar metadata, and the explicit time/country verification. The historical 26-check statements are dated evidence, not current counts.
- Sixteen exact memberships match; 6,256 distinct tested rows. Native dummy RMSE ranges 0.1367695300–0.2755898383 and equals direct RMSE within 1e-14 for every cell. No exact cross-split predictor copies.
- All 48 retained family-cell RMSE values reproduce within 1e-14. Macro-cell RMSE: ridge 0.1182589259, LightGBM 0.1187945709, random forest 0.1204131913; retained dummy macro-cell RMSE 0.1854727267. These are reused bounded train-only qualification results, not new training.

**Claim ledger**

“Holds” below means the specific claim was supported, including claims that expressly acknowledge uncertainty. It does not upgrade those uncertain underlying facts to verified.

| Claim in definition / current record | Test or source | Result and evidence | Rules |
| --- | --- | --- | --- |
| 21,454 labeled survey-cluster observations, 18 countries, 1994–2016 | Raw count, unique countries/year range; official source describes cluster-level surveys | Holds: 21,454 rows, 18 countries, stated range | USE-1, EV-2 |
| Agency survey-gap mapping is the decision | Current official competition description names policy makers, NGOs and survey gaps | Holds for retrospective approximate framing | USE-1/8 |
| Supplied target is a 0–1 wealth index, not currency or poverty probability | Raw range; preserved source documentation in accepted record | Holds: min 0, max 1; label interpretation remains as previously accepted | USE-5 |
| Every source row and label remains unchanged | ID alignment, target equality, complete ID set | Holds: all 21,454 rows and labels preserved | USE-5, PROV-13 |
| Exact target formula/harmonization is unverified | Definition explicitly preserves this limit; no new establishing evidence | Holds as an uncertainty statement; underlying fact remains cannot-verify | USE-5/8, EV-7 |
| Proposed retained measurements have unresolved epochs | Definition notes; earlier accepted investigations | Holds as an uncertainty statement; this audit does not date them | USE-3/8, EV-7 |
| Through-2000 settlement masked before 2000 | Independent raw reconstruction | Holds: 1,364 masked; endpoint and later values unchanged | LEAK-10 |
| Through-2014 settlement masked before 2014 | Independent raw reconstruction | Holds: 15,198 masked; endpoint and later values unchanged | LEAK-10 |
| Through-2014 not-built residual masked before 2014 | Independent raw reconstruction | Holds: 15,198 masked; endpoint and later values unchanged; rationale retained from prior algebra audit | LEAK-10 |
| Four land-cover snapshots omitted | Independent expected frame | Holds: all four absent, no replacement extraction added | LEAK-10, PROV-13 |
| Water, lights, population remain; their temporal safety is not established | Expected-frame equality and explicit notes | Holds; no new later-state evidence obtained | USE-6, EV-7 |
| Annual endpoint approximation is accepted | Dated November 2 CC and fit_reason | Holds as curator decision; interview-time ordering is not verified | USE-8, curator precedence |
| Country and opaque ID excluded from learner inputs | Native feature_columns and frame checks | Holds; both absent from final model frame | CLEAN, SPLIT-4 |
| Year retained as numeric time input, urban/rural categorical | Current dtypes and model columns | Holds; urban/rural categories R/U; twelve predictors | USE-6, CLEAN-14 |
| No full-data frequency features or label-derived transformations added | Full frame equals independently cleaned raw data | Holds; only three masks and four omissions | LEAK-27/30 |
| Zeros and all other numeric scales retained | Expected frame equality | Holds; no unrecorded scale or missing-code transform | PROV-13, CLEAN-1 |
| Sixteen observed country-year tests in 2014–2016, newest year first | Reconstruct observed cells and ordered memberships | Holds; exact match with accepted plan | SPLIT-4 |
| Train strictly earlier and excludes every row from test country | Independent formulas for all sixteen train sets | Holds; zero year/country violations | SPLIT-4 |
| Every train side exceeds half the full sample | Per-split assertions | Holds on all sixteen tests | SPLIT-14 |
| Some rows training-only; repeated histories and countries imply dependent tests | Exact memberships, 6,256 distinct tested rows | Holds; no independence inference permitted | EV-2/7 |
| Scientific regime is temporal × unseen-country; backend is temporal | Current memberships, Temporal metadata, dated CC | Holds; both required_split values retain the candidate-specific override | SPLIT-3/4, curator precedence |
| RMSE is the source metric on the shipped target scale | Official parent and rerun evaluation sections, current MetricSpec | Holds: rmse/source/identity, no additional scoring columns | MET-1/2/3/4/11 |
| RMSE computes on every test cell | Direct/native score comparison | Holds: finite, nonconstant test targets; all scores equal direct RMSE | MET-2 |
| Current native checks have no errors/warnings; no warning acceptances | Actual ds.check result and accepted_check_warnings | Holds: 0/0, empty acceptance dict | EV-7 |
| Previous model evidence remains applicable | Exact raw/frame/splits plus all retained prediction scores | Holds under stated equivalence, with `no_spread` and dependency limits retained | TP-1/2/3, EV-7 |
| Original AIMS bytes, exact survey programme, interview dates and publication delays are not verified | Explicit current definition notes; no new provenance evidence | Holds as uncertainty statements; not newly resolved | PROV-1/8/10, EV-7 |
| Priority 3 still reflects measured gap/shape and unchanged judgments | Main priority helper and prior judgment factors | Holds: 159 accepted definitions now, social-science gap +1 and shape +1 unchanged; use case +1/source 0/risk −1 | selection priority, EV-2 |

**Source metric and rule refresh**

Opened the official [Economic Well-Being challenge](https://zindi.world/competitions/economic-well-being-prediction-challenge) and [AIMS parent](https://zindi.world/competitions/aims-data-science-hackathon) on November 5. Both evaluation sections state: “The evaluation metric for this competition is Root Mean Squared Error.” The source pages also support the task's unseen-country origin; this benchmark adds the accepted forward-year requirement. This audit does not claim original-parent/rerun byte identity.

Current main's MET-2 scoring-input clarification requires no change: rowwise RMSE has no auxiliary inputs. MET-4's November 5 amendment permits reconsidering weaker competitions when measurements favour an obvious contextual metric; it does not require replacing a sensible, computable RMSE, and no such contrary measurements were found. MET-11's context expansion likewise supplies no reason to relabel the source metric. The new MET-13 stability wording does not require dataset-local code for the standard library RMSE. Updated target/fit and provenance wording preserves the documented approximate use case rather than establishing a new acceptance gate. Verification now makes more checks explicit; their execution outside this narrow claim audit belongs in the parent run's combined report, and is not claimed here.

**Reuse conditions and remaining input**

Reuse is supported by identical raw identity, full frame hash, row manifest, sixteen exact memberships, model feature ordering and native scores. The current definition bytes also equal the accepted definition in the earlier checkout; its four data/type/split methods are AST-identical. The retained predictions' SHA-256 is `37ecda65ac165c5b299afbc63e62a28759f89365405252fee7fde773c1f4beca`. No current-engine probe result is implied merely by these facts; the main requalification must run newly relevant probe/check coverage.

No new curator input is needed from this audit. Preserve the accepted timing/target/split decisions with their original dates and the exact known unknowns. Do not ask the curator to reapprove them solely because this is a newer source fingerprint. Demonstrated later-state measurements or a changed label/protocol would be concrete contradictory evidence; none was found here.

Evidence files: `claim-audit-evidence/facts.json`, `claim-audit-evidence/retained-rescore.json`, `claim-audit-evidence/method-equivalence.json`, `claim-priority-factors.json`; reproduction scripts `audit-claims.py` and `audit-rescore.py`. This auditor edited only run artifacts and performed no record/definition edits, commits, claims operations or new qualification.

</details>

<details><summary>Column audit</summary>

**Focused current-main column and dtype audit**

Editor chronology note: this report inspected the predecode definition and recommended the now-completed label expansion. Preserve its measurements as that snapshot; final labels, row order and score alignment are reported in the Final split audit and Mediator sections.

Verdict: no new validity finding and no new scientific decision. The migrated definition reproduces the accepted data exactly under current main. One routine CLEAN-12 presentation update is recommended: expand the established R/U urban/rural labels to Rural/Urban while retaining an unordered category. It does not warrant a new approval issue.

**Scope and identities**

Audited current-main base: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. The installed current and accepted old definitions both have SHA-256 `dc4703333b0eb11ab3d422daec3ca3fa2914be926a6410d4dfe7f9e2264d86b3` at this audit. The raw file remains `caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c`.

Read the current main add skill, both knowledge indexes, principles, cleaning, leak, evidence, use-case, definition and probe procedures; the column-auditor role; and the prior column/source reports and verification evidence. This is the column member of a focused recheck, not another full panel. Primary-source meanings below reuse the source investigation retained in `20261031_economic_add/source-column/source-findings.json` and the full prior column report; no new source epoch or publisher-byte authentication is asserted.

The current dtype probe ran once using the declared qualification code and wrote `dtype/economic_well_being_prediction_challenge.json`: 0 of 12 predictor columns flagged, no automatic codebook (the automatic fetcher supports UCI/OpenML, while this source is Zindi). Therefore there are no flagged columns to resolve; the table below supplies the semantic inspection the probe cannot replace.

`column_check.py` and `column-check-evidence.json` hold the independent current-main measurements. No dataset, record, historical report or raw file was changed. No model, container build, remote inquiry or additional qualification ran.

**Reproduction and cleaning evidence**

- Both canonical metadata-bearing frames and final model frames are exactly equal between old and current definitions, including dtypes and column order; all sixteen split dictionaries are exactly equal.
- Current model-frame SHA-256 using the prior verification's `hash_pandas_object(..., index=True)` algorithm is `039c9d0cb264d52d0a0481d21ef4c08b95d84c3eae602c4258092a888fdec9ab`, matching the prior native verification hash. Dtypes and per-column missing counts match the prior receipt exactly. This establishes reproduction, not a fresh certification of unresolved source provenance.
- All 21,454 unique raw IDs and all 21,454 targets survive unchanged. ID alignment independently checks that every other surviving value is unchanged except the declared masks. The final frame contains twelve predictors plus Target; ID, country and all four land-cover fields are absent.
- The three masks are exact: 1,364 cells for the 2000-ending built-up interval and 15,198 each for the 2014-ending built-up interval and not-built residual. No explicit future-period cell remains. No other missingness is introduced; no infinities or untyped object columns survive.
- `_load_raw`, `_clean`, `_feature_types`, `_make_splits`, `_extra_checks` and `_decisions` have identical ASTs in the migrated and accepted definitions. Current schema/probe APIs require no dtype migration for these columns. Numeric fractions remain measurements even when 0 occurs; year remains numeric annual time; R/U remains nominal categorical.

**Every raw column**

| Column | Meaning / represented time | Dtype and cleaning | Assessment and rule |
|---|---|---|---|
| ID | Opaque unique source row key | String internally, dropped after split construction | Correct exclusion, CLEAN-3. |
| country | Survey country | Category internally, dropped after country-excluded split construction | Correct metadata handling; no model input. |
| year | Survey-content year, 1994-2016 | int64, retained | Numeric annual time is correct, CLEAN-14. Exact interview/publication timing stays unknown. |
| urban_or_rural | Rural/urban cluster context; assignment provenance not fully documented | Unordered category, exactly R/U, no missing values | Correct dtype; routine label expansion to Rural/Urban recommended under current CLEAN-12. Retention remains supported by the source starter, USE-6. |
| ghsl_water_surface | GHSL water-area fraction; actual epoch unverified | float64, retained, observed range 0-0.970 | Measurement dtype correct. Existing disclosed timing uncertainty remains, USE-3/8, LEAK-38, EV-7. No new later-state evidence. |
| ghsl_built_pre_1975 | First construction before 1975 | float64 fraction, retained | Interval precedes surveys; later past-state reconstruction allowed by accepted convention, LEAK-10. |
| ghsl_built_1975_to_1990 | First construction in 1975-1990 | float64 fraction, retained | Same conclusion; no new evidence of future conditioning. |
| ghsl_built_1990_to_2000 | First construction in 1990-2000 | float64; masked for year < 2000 | Exact annual repair, LEAK-7/10. Same-year endpoints follow the accepted approximation. |
| ghsl_built_2000_to_2014 | First construction in 2000-2014 | float64; masked for year < 2014 | Exact annual repair, LEAK-7/10. The known 2014 coverage transition remains intentional. |
| ghsl_not_built_up | Land unbuilt through the last mapped epoch, 2014 | float64; masked for year < 2014 | Correctly removes the future residual/complement route, LEAK-7/10. |
| ghsl_pop_density | Population around cluster; exact product epoch/unit mapping unresolved | float64, nonnegative, retained | Correct numeric dtype. Existing disclosed unknown epoch stays unknown; do not invent a 2015 date or physical unit, EV-7, LEAK-38. |
| landcover_crops_fraction | Cropland fraction in an unspecified slice of linked 2015-2019 product | Omitted | Accepted conservative repair preserved; no safe selected epoch established, LEAK-7/10. |
| landcover_urban_fraction | Urban cover, same product | Omitted | Same conclusion. |
| landcover_water_permanent_10km_fraction | Permanent-water cover within 10 km, same product | Omitted | Same conclusion. |
| landcover_water_seasonal_10km_fraction | Seasonal-water cover within 10 km, same product | Omitted | Same conclusion. |
| nighttime_lights | Night-light indicator; exact composite/satellite epoch unresolved | float64, nonnegative, retained | Correct measurement dtype; same accepted unresolved timing note and repair trigger, LEAK-38, EV-7. |
| dist_to_capital | Distance to capital; GIS vintage/unit not fully verified | float64, positive, unchanged | Correct measurement dtype; no established future-state mechanism, USE-6. No invented kilometre claim. |
| dist_to_shoreline | Distance to ocean shoreline; GIS vintage/unit not fully verified | float64, positive, unchanged | Same conclusion. |
| Target | Supplied cluster-average wealth index on 0-1; full construction/harmonization unverified | float64, no missing, 21,454 distinct values, unchanged | Correct regression target under accepted approximate fit, USE-5/8, CLEAN-15. No log transform: source RMSE and source scale are preserved. |

**Ranked outcome and minimal follow-through**

There are zero new P3/P4/P5 issues. Calendar-year timing, the supplied-index target and the joint time/country regime remain accepted. Unknown epochs are not new evidence or a reason to repeat permission. The existing trigger remains: actual established later-state content must be masked, repaired historically or omitted if unrepaired. No further feature drop is supported by this audit.

One P7 routine edit is recommended under CLEAN-12: decode `urban_or_rural` as `{"R": "Rural", "U": "Urban"}` with `decode` and a short curation note. This is a lossless nominal label expansion; it adds no feature or ordinal order. The dtype probe does not flag word abbreviations, so its zero flags do not settle that presentation rule. If applied, regenerate the native report and refresh any frame/split identity receipts, because content-based canonical ordering can change even after a lossless label rename. Compare by source ID and decoded values when proving equivalence; old positional hashes should remain historical. The retained numeric and temporal decisions need no repair.

`proposed_label_check.py` independently tested exactly that mapping through an in-memory `_clean` override, with no definition edit. All column values and targets match after ID alignment and decoding. The predictor names/count and dtype names stay the same; the two levels become Rural/Urban, still unordered. However, 21,436 of 21,454 canonical ID positions change under the base class's content sort. The proposed frame hash becomes `aaf6121b72ee2b21705252cf7afc10ac8342dd345e3bef1321174543424b9100`. Every one of the 32 train/test sides retains its exact ID set, while every ordered ID list and every positional-index list differs. Thus scientific membership is unchanged, and old positional identities must be regenerated. Categorical level storage uses an object-backed category Index after `decode`, while the expected `rename_categories` comparison initially used pandas' new string-backed Index; comparison by decoded values explicitly accounts for that internal representation distinction. Full measured results are in `proposed-label-evidence.json`.

The script's first attempt used pandas `stack()` for finiteness and encountered the expected masked NaNs under the current runtime. The final script explicitly permits only NaN or finite numeric cells; it passed. This scratch assertion correction did not touch the product or establish a data defect.


</details>

<details><summary>Final split audit</summary>

**Final split audit after category decoding**

Independent focused recheck, 2026-11-05 UTC. **0 new actionable findings.** Retain the accepted temporal × unseen-country memberships and source RMSE. The R/U → Rural/Urban decoding changes category names and the framework's canonical row order; it does not change the task's observations or ID memberships. This supersedes the earlier audit's byte/order-equivalence claim for the final definition, while preserving that earlier evidence as history.

Final candidate `dataset.py` SHA-256: `43a922924f61ca63478edd77c10a1df5506c01245cfa2d7031d86f17744b2b6f`. Auditor script: `audit_final_splits.py`; machine-readable evidence: `final-split-audit.json`. The definition hash was checked before and after the audit. Candidate files and records were not edited by this auditor; no container save, claim operation, commit or publication occurred.

**ID-aware fidelity and scoring**

- All 21,454 source IDs remain unique and present. Reordering the final frame to the historical `split-row-manifest.parquet` ID order and reversing only category labels reproduces the historical frame hash exactly: `039c9d0cb264d52d0a0481d21ef4c08b95d84c3eae602c4258092a888fdec9ab`. Numeric values, all supplied targets, null masks, dtypes and the 12-feature list therefore match the prior qualification by ID. Final unordered category levels are exactly Rural and Urban and match the raw R/U meaning on every ID.
- Canonical ID positions changed on 21,436 rows. The final frame hash is `aaf6121b72ee2b21705252cf7afc10ac8342dd345e3bef1321174543424b9100`; old positional arrays must not be applied directly to it.
- Independently reconstructed every train/test side from the raw year/country associated with final IDs. All **32 ID sets** match the historical `split-memberships.npz` plus row manifest. Each of the 16 tests contains exactly one country-year cell in 2014–2016; train contains exactly every earlier-year row outside that entire country. All sides remain disjoint and every train exceeds 50% of all rows. The tests contain the same 6,256 distinct IDs, once each. No split was selected using scores.
- Reindexed the historical 48 family/cell prediction vectors through old row position → source ID → final row position. Each retained truth equals the final target, and its ID set equals the corresponding final test set. Current native RMSE agrees with both the original recorded score and direct sqrt(mean squared error) within 1e-14 on all 48 vectors. This verifies metric/prediction-score equivalence without fitting a new learner. Refitted stochastic learners can vary with row order; the equivalence statement is about the same retained predictions after correct ID alignment.
- The native current-main check was rerun with `write_report=False`; it has no errors or warnings. Existing informational observations remain the conflicting feature profiles, numeric calendar-year horizon and verified time/country repair.

**Affected probes rerun on final code**

The following qualification checks were run:

1. `leak_probes.py economic_well_being_prediction_challenge --splits 3 --n-jobs 2 --out leak-final`, with log `leak-final.log`. Models use the newest three shipped cells. Exact copies use every full row on all 16 shipped splits: **0 matches across 6,256 test evaluations**, including every same-label, other-label and mixed-label partition, and zero on each split. The yearly period check still reports no out-of-band newest row-count/mean/median/p90 statistic. This does not establish label publication availability or covariate epochs. Three-cell diagnostic full-model R² remains about 0.250, lights alone 0.447 and shallow depth-2/3 trees 0.429/0.450; these untuned checks do not replace the earlier sixteen-cell tuned evidence or prove timing safety.
2. The same command with `--raw --out leak-raw-final`, with log `leak-raw-final.log`. Lineage traces all 21,454 rows, with no row removal. Raw target-position Spearman remains -0.01218 and lag-1 autocorrelation 0.00995, no order flag. Raw profiles repeat on 173 rows in 44 mixed-target groups, with zero full-row copies. The four omitted land-cover fields remain correctly omitted; their predictive scores do not establish represented epochs. Classification-only number-format/interpolation diagnostics remain inapplicable to regression.

These final artifacts cover the only new implementation change. Preserve the annual endpoint approximation, supplied-index approximate fit, explicit joint-split exception and known unresolved timing/provenance limits from `split-audit.md`. No new evidence justifies reopening those decisions. Exact-copy absence is limited to the shipped profile and does not certify all spatial dependence.

</details>

<details><summary>Precedent checker</summary>

**Independent consistency review: economic well-being, current main**

Editor chronology note: this report preceded inspection of the completed replacement gamer and final postdecode artifacts. Its stated evidence limits remain historical; the Mediator section records the later inspection and the Final split audit records the completed data checks.

Observed 2026-11-05 UTC. Advisory reviewer: independent precedent checker for Myunghwan. Base: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. **No new curator input is required by the evidence inspected.** Carry forward the accepted annual timing approximation, supplied-index approximate fit, temporal × unseen-country evaluation and ship decision. Complete current procedural documentation and checks without asking those questions again.

I read the current review-added-datasets skill, both knowledge indexes, principles, splits, metrics and evidence rules, relevant USE-1/3/5/8/10 and CLEAN-12 wording and Cases, the candidate record and definition, the November 2 annual and ship consistency reports and actual ship input, the current migration, column/claim/split audit reports and proposed-label evidence. I also read the integration adaptation and human-review contract and the current task-gamer role/hook. This report does not independently repeat the other auditors' data experiments or attest to work they have not completed.

The current decision register ran. It compared against 4,029 collected decisions and displayed six selected decisions, with **zero flags**. This is a mechanical search aid, not consistency clearance: the selected CCs generally lack rule IDs; several enriched Assessment labels in the actual record are not parsed by the script's narrower label regex. In particular, the explicit combined-regime departure is visible in the record but is absent from the selected rule grouping. The direct reading below therefore governs. No script or rule was changed to suppress a flag.

| Preserved human decision | Actual authority and historical identity | Current application and consistency |
|---|---|---|
| Proceed with audits; later reconstructions of past states allowed, actual later states forbidden | Myunghwan CC 2026-10-31, preserved in the candidate record | Keep the existing represented-state criterion and repair established later-state content. Unknown epochs are not certification of safety and do not themselves establish a newly observed later-state defect. |
| Annual timing approximation and resolution of issue 1 | Myunghwan's November 2 annual answer and later “OK. then 1 can be resolved” follow-up; original annual snapshot `b093dad69fbbdb15c53902e1d14fb82e4d5a3607275e4826f0ba8f5f8d851ba0`, version 0, remains historical | Preserve annual endpoints and the documented interview-level limitation. The requested within-country experiment did not date layers: fixed-period construction also changes in all 52 country-year comparisons. This interpretation was already disclosed and accepted; no new contradiction is supplied. |
| Ship the supplied wealth index with approximate fit | Actual November 2 input: “ok. ship it. but it's not just purely temporal -- temporal x unseen”; ship snapshot `f45952073e7699f581848154a0c6be7085a9d2b3b5637ef72765fb46cb0b9776`, version 0; contemporaneous consistency report explains acceptance of remaining issue 2 in context | USE-5 permits a named-source label whose construction cannot be checked with approximate fit and the gap named; diabetes_3 and blood_tests_drink_prediction are the closest Cases. Unknown formula/harmonization remains unknown. No measured different target or broken scale has been found. Do not re-open the supplied-index choice. |
| Temporal × unseen-country, both record requirements, temporal backend | Same exact November 2 ship input; October 31/November 2 dated record and consistency report | The real memberships require `year < t AND country != c`. Both constraints are deliberate, not an incidental group structure or alternative variant. Preserve them and both existing vocabulary values. Complete the formal scoped-departure record described below. |
| Repeat add → review → build against updated main using past decisions; local commits authorized | Myunghwan CC 2026-11-05, preserved separately from prior marks | This is current authorization to reuse the old decisions and execute the requested stages. It is not a fresh mark on a new snapshot. Keep the existing-PR exclusion and preserve original human words/dates. |

The current review should carry a **preservation/application ledger**, identifying the old input, original snapshot and decision date, current source identity, and the verified unchanged semantic scope. It must not copy old marks onto a freshly fingerprinted page as if Myunghwan had newly reviewed that page. A current no-new-input finding is an AI consistency assessment under the explicit reuse request. Old marks, snapshots, assessments and earlier counts remain historical; current checks and newly generated output identities are recorded separately. The newer current rule to retain resolved review issues also means the historical removal of REVIEW.md is preserved as history rather than silently rewritten into a claim that it followed today's procedure.

The SPLIT-3 documentation needs deliberate completion. Current SPLIT-3 is still **Must**, saying never both temporal and grouped, and the current `splits.md` Cases table contains no economic-well-being entry. The record's AI prose acknowledges the departure, and the human correction already establishes its authority. Current review Step 4 requires a confirmed departure in the record, dataset notes and rule's Cases table. Thus **yes, a formal candidate-specific Case entry is needed when carrying this departure forward**, together with a clearly attributed formal departure note; this is an agent-owned documentation repair, not a new approval request or a global amendment.

There is an important terminology constraint: principles allow ordinary exceptions only to Should rules. A Must can be overridden only by a higher-ranked Must; the current user instruction also expressly preserves this candidate's decision. Do not describe this as a generic waiver of a Must or claim curator preference alone changes the written scientific rule. Document the narrow conflict with the accepted USE-1 (Must, P3) use case: replacing either actual future-year transfer or source-origin unseen-country transfer with a single dependency would change this specifically approved evaluation. USE-1 ranks above P4 SPLIT-3. Preserve SPLIT-3's general text unchanged. In the review workflow's `exception` Cases category, explicitly describe it as a **candidate-specific higher-ranked use-case override**, rather than an ordinary Should exception. A suitable row for the stage owner to apply is:

```text
| SPLIT-3 | economic_well_being_prediction_challenge | Candidate-specific override: temporal × unseen-country, explicitly confirmed by Myunghwan on 2026-11-02 and carried forward at his request on 2026-11-05. Each test country-year trains only on earlier years from other countries. Serves USE-1 (Must, P3): the accepted task is future-year survey-gap mapping in an unseen country; either single-regime replacement changes that task. Temporal is the backend representation, not a new enum or a general amendment. | exception |
```

The accompanying formal `Exception to SPLIT-3` note must make the same override qualification and retain November 2 as the actual decision date, with November 5 separately identified as preservation. The register will correctly flag a formal `exception` on a plain Must; resolve that warning explicitly against the higher-ranked USE-1 conflict and exact user authority. Do not alter the rule's strength, remove the flag, invent a fresh curator confirmation or let a zero-flag report conceal the conflict. This is one candidate, not a demonstrated third repeated exception or a general rule change.

Other current changes supply no new decision. Source RMSE on the unchanged 0–1 target still satisfies MET-1/2/3/4/11: MET-4's new weaker-competition wording permits reconsideration when measurements justify an obvious contextual metric; it does not mandate changing a suitable RMSE. Native rowwise RMSE needs no auxiliary scoring columns. The current claim audit reports native/direct equality on every fold and unchanged historical scores before decoding; these are auditor evidence, not experiments run by this reviewer.

Expanding established R/U meanings to Rural/Urban is ordinary CLEAN-12 application, supported by its November 1 decoding amendment and Cases; preserve an unordered category. The proposed-label experiment reports identical per-ID values after decoding, same predictor count/dtypes and all sixteen train/test ID sets unchanged. It also reports 21,436 changed canonical ID positions and changed index arrays/order. Therefore this is not byte-identical model input or permission to reuse position-bound predictions blindly. Regenerate canonical arrays and current probes/checks, and either refit affected model evidence or explicitly remap and verify reuse by ID with the relevant preprocessing/model/scorer conditions. Retain historical results as historical. The stage owner reports current probes rerun; this report does not claim independently to have checked their final postdecode artifacts. None of this changes the accepted target, population or semantic split, and none needs a new curator mark.

The unknown water/population/light epochs, survey programme, target harmonization, interview dates, publisher-byte authentication and label publication delay remain the already disclosed limits. EV-2/6/7 prohibit converting them into passes. The new current split/claim audits report no exact cross-split copies, intact chronology/country exclusion, sufficient train/test support and no new release-end selection finding; these checks do not date covariates, prove target harmonization or certify historical label availability. An actually demonstrated later state, different label or changed membership would justify reopening the affected decision. None is established in this review.

The supplementary participant review used a fresh independent context with only participant inputs and public sources. It followed a declared access contract without enforced filesystem isolation. A report citing only those inputs supports the review; self-reported access is not an independently audited complete read log. At this report's date the replacement review was not yet complete, so this is an assessment of its setup rather than its final findings.


</details>

<details><summary>Participant task gamer</summary>

**Participant gaming report**

**Result**

**No demonstrated exploit using unavailable-at-prediction information.** Honest untuned LightGBM achieves mean window RMSE **0.124379**, pooled RMSE **0.123355** over all 16 exact shipped splits (6,256 test-row evaluations). Whole-data frequency features yield a nominal 0.004132 mean gain, but training-only frequency features yield 0.006256 and an 11-random-feature control yields 0.004076. The frequency method adds twelve columns, so this control is comparable rather than exactly width-matched. Three additional random seeds yield mean RMSE 0.120890, 0.121343, and 0.120935. This pattern is consistent with finite-model fitting effects; no distinct transductive advantage is established. No significance claim is made from these selected comparisons.

**Setup**

Read task.md first. Target Target; geographic cluster wealth regression. Prediction point: estimate survey-year wealth in a country absent from training, from proposed same-year or earlier-state inputs. All fitted supervised transformations and label rules used only that split's training labels. Test labels were used only by score.py to evaluate completed predictions. No tuning or early stopping. LightGBM uses 100 trees, learning_rate .1, num_leaves 31, seed42, n_jobs2; other library defaults. Category urban_or_rural remains categorical. Same model and scorer used in every model comparison. OMP/MKL/OpenBLAS/Polars are capped at2. Runtime of primary suite was approximately one minute; follow-up controls approximately 20seconds. There was brief overlap of two independently capped two-thread processes, so aggregate CPU concurrency could reach four then; no GPU used.

Mean RMSE weights windows equally; pooled RMSE weights squared errors by test size. Windows span 2014, 2015, 2016. Country identifiers are absent, so I cannot independently verify country disjointness from kit columns; this is an evidence limit, not a finding of overlap.

**Attack and control comparisons**

Positive gain means lower RMSE than honest baseline.

| Method | mean_rmse | pooled_rmse | gain_vs_honest | windows_better |
|---|---|---|---|---|
| honest_lgbm | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| whole_feature_frequency_added | 0.120247 | 0.120563 | 0.004132 | 11.000000 |
| train_feature_frequency_added | 0.118123 | 0.119875 | 0.006256 | 10.000000 |
| test_feature_frequency_added | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| whole_feature_rank_added | 0.124827 | 0.123854 | -0.000448 | 6.000000 |
| test_feature_rank_added | 0.124874 | 0.123848 | -0.000494 | 8.000000 |
| row_order_added | 0.124214 | 0.123356 | 0.000166 | 5.000000 |
| format_only | 0.117969 | 0.122302 | 0.006410 | 7.000000 |
| pure_format_only | 0.128041 | 0.132965 | -0.003662 | 5.000000 |
| missing_only | 0.185329 | 0.190290 | -0.060949 | 3.000000 |
| position_only | 0.193296 | 0.196648 | -0.068917 | 0.000000 |
| random_features_added | 0.120303 | 0.120371 | 0.004076 | 14.000000 |
| random_seed_11 | 0.120890 | 0.120750 | 0.003489 | 14.000000 |
| random_seed_29 | 0.121343 | 0.120831 | 0.003036 | 16.000000 |
| random_seed_73 | 0.120935 | 0.120888 | 0.003444 | 12.000000 |
| honest_drop_2014_surfaces | 0.123915 | 0.123197 | 0.000464 | 6.000000 |
| honest_recent_2010plus | 0.126371 | 0.125542 | -0.001992 | 3.000000 |

format_only includes missingness, decimal-string length, zero indicators and urban_or_rural. Its 0.117969 mean RMSE is **ordinary coarse feature signal**, not a demonstrated format exploit: zero and urban indicators are available at prediction and string length can encode numerical magnitude. pure_format_only removes urban and zero indicators and scores 0.128041, worse than baseline. Because raw CSV tokens are not shipped, string formatting here means deterministic Python rendering of parquet numerical values, not original source formatting.

Global ranks/frequencies are computed on all shipped feature rows, including future/test rows. Test ranks/frequencies are computed from exactly the test batch, without labels. These deliberately test unavailable-batch information when deployment predicts one cluster. Training-only ranks/frequencies are the legitimate counterpart. Whole-data ranks and test ranks worsen mean RMSE. The frequency improvement is matched or exceeded by legitimate controls; it does not demonstrate a usable exploit.

Row-order features include global row index and within-year ordinal position. Position-only control additionally uses within-year fraction (a transductive denominator). Neither establishes an advantage. Synthetic row positions are not proposed deployment inputs.

**Copies and time**

All 16 splits have zero train/test row overlap and zero training rows at or after the earliest test year. No exact cross-split matches using all features, all except year, or the two distance features alone. No near-copy matches at standardized Euclidean distance below 1e-5 using all numeric features; the minimum distance across splits is 0.207048. Standardization and imputation were fitted on training rows only. Lookup attacks preserve the honest baseline where no match exists, so all four lookup/near-copy methods equal baseline. These tests do not exclude more distant or unobserved geographical dependence.

Feature endpoint audit: ghsl_built_1990_to_2000 has zero nonmissing values before2000; ghsl_built_2000_to_2014 and ghsl_not_built_up each have zero before2014. Removing the latter two yields 0.123915 mean RMSE, a negligible 0.000464 improvement. Restricting training to2010 onward worsens mean RMSE to0.126371. Single-feature and urban-group mean rules are fully tabulated below. Nighttime lights alone reaches0.123667, which is credible legitimate geographic signal and not evidence of leakage.

**Public-source inquiry**

The [competition data page](https://zindi.world/competitions/economic-well-being-prediction-challenge/data) describes cluster survey wealth, spatial inputs, and a public training file containing labels. Public source-label matching may therefore be possible in principle for rows derived from that file, but it was not attempted or ranked as an exploit.

The [first-place writeup](https://zindi.world/competitions/economic-well-being-prediction-challenge/discussions/6028) and [fourth-place writeup](https://zindi.world/competitions/economic-well-being-prediction-challenge/discussions/7283) describe frequency encoding and conventional models; the former also describes aggregating related features and clipping. A bounded web search did not reveal a documented label leak. The linked [public winning-code repository](https://github.com/ASSAZZIN-01/Economic-Well-Being-Prediction) was inspected at its landing page only; no source dataset was downloaded.

The competition's linked [GHSL catalog](https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2016_BUILT_LDSMT_GLOBE_V1) says the historical built-up layer uses imagery through2014 and was produced in2015. This is an availability ambiguity for a strictly real-time2014 deployment. The task explicitly allows earlier/same-year *state* inputs, and does not give an estimation date or release-time policy; I therefore do not call this a demonstrated future-state exploit. Population and light feature vintage remain unverified. A release-time deployment interpretation needs a separate availability audit.

**Full method results**

| Method | mean_rmse | pooled_rmse | gain_vs_honest | windows_better |
|---|---|---|---|---|
| format_only | 0.117969 | 0.122302 | 0.006410 | 7.000000 |
| train_feature_frequency_added | 0.118123 | 0.119875 | 0.006256 | 10.000000 |
| whole_feature_frequency_added | 0.120247 | 0.120563 | 0.004132 | 11.000000 |
| random_features_added | 0.120303 | 0.120371 | 0.004076 | 14.000000 |
| random_seed_11 | 0.120890 | 0.120750 | 0.003489 | 14.000000 |
| random_seed_73 | 0.120935 | 0.120888 | 0.003444 | 12.000000 |
| random_seed_29 | 0.121343 | 0.120831 | 0.003036 | 16.000000 |
| single_nighttime_lights | 0.123667 | 0.126886 | 0.000712 | 7.000000 |
| honest_drop_2014_surfaces | 0.123915 | 0.123197 | 0.000464 | 6.000000 |
| train_feature_rank_added | 0.124178 | 0.123141 | 0.000201 | 11.000000 |
| row_order_added | 0.124214 | 0.123356 | 0.000166 | 5.000000 |
| exact_all_lookup | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| stable_geo_lookup | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| honest_lgbm | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| near_copy_override | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| test_feature_frequency_added | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| exact_no_year_lookup | 0.124379 | 0.123355 | 0.000000 | 0.000000 |
| whole_feature_rank_added | 0.124827 | 0.123854 | -0.000448 | 6.000000 |
| test_feature_rank_added | 0.124874 | 0.123848 | -0.000494 | 8.000000 |
| honest_recent_2010plus | 0.126371 | 0.125542 | -0.001992 | 3.000000 |
| pure_format_only | 0.128041 | 0.132965 | -0.003662 | 5.000000 |
| single_urban_or_rural | 0.133383 | 0.140597 | -0.009004 | 6.000000 |
| urban_mean_rule | 0.133383 | 0.140597 | -0.009004 | 6.000000 |
| single_ghsl_pop_density | 0.143903 | 0.147425 | -0.019524 | 5.000000 |
| single_ghsl_built_1975_to_1990 | 0.146125 | 0.153916 | -0.021746 | 5.000000 |
| single_ghsl_built_pre_1975 | 0.154508 | 0.163281 | -0.030129 | 3.000000 |
| single_ghsl_built_1990_to_2000 | 0.154835 | 0.157115 | -0.030456 | 3.000000 |
| single_ghsl_not_built_up | 0.165771 | 0.176469 | -0.041391 | 3.000000 |
| single_ghsl_built_2000_to_2014 | 0.170266 | 0.179910 | -0.045887 | 3.000000 |
| single_dist_to_capital | 0.180357 | 0.186816 | -0.055978 | 3.000000 |
| single_ghsl_water_surface | 0.185078 | 0.189961 | -0.060698 | 2.000000 |
| missing_only | 0.185329 | 0.190290 | -0.060949 | 3.000000 |
| train_mean | 0.185473 | 0.190545 | -0.061094 | 3.000000 |
| single_year | 0.187961 | 0.189941 | -0.063582 | 0.000000 |
| single_dist_to_shoreline | 0.188618 | 0.195416 | -0.064239 | 4.000000 |
| position_only | 0.193296 | 0.196648 | -0.068917 | 0.000000 |

**Exact per-window comparison**

| Method | honest_lgbm | whole_feature_frequency_added | train_feature_frequency_added | test_feature_frequency_added | row_order_added | random_features_added |
|---|---|---|---|---|---|---|
| r0f0 | 0.124530 | 0.125686 | 0.158164 | 0.124530 | 0.124807 | 0.125423 |
| r1f0 | 0.103862 | 0.105044 | 0.100255 | 0.103862 | 0.102312 | 0.102706 |
| r2f0 | 0.179208 | 0.162485 | 0.144824 | 0.179208 | 0.176625 | 0.173125 |
| r3f0 | 0.075717 | 0.068989 | 0.069731 | 0.075717 | 0.077506 | 0.070042 |
| r4f0 | 0.120557 | 0.117344 | 0.126037 | 0.120557 | 0.118283 | 0.116705 |
| r5f0 | 0.133438 | 0.138627 | 0.108981 | 0.133438 | 0.133469 | 0.131178 |
| r6f0 | 0.148380 | 0.148188 | 0.166001 | 0.148380 | 0.158654 | 0.147589 |
| r7f0 | 0.145188 | 0.147623 | 0.151841 | 0.145188 | 0.149037 | 0.145543 |
| r8f0 | 0.101083 | 0.097290 | 0.089316 | 0.101083 | 0.093308 | 0.089227 |
| r9f0 | 0.097875 | 0.094462 | 0.100873 | 0.097875 | 0.099300 | 0.095347 |
| r10f0 | 0.115466 | 0.112453 | 0.118190 | 0.115466 | 0.116012 | 0.114836 |
| r11f0 | 0.115606 | 0.112888 | 0.108375 | 0.115606 | 0.115722 | 0.113313 |
| r12f0 | 0.108511 | 0.107213 | 0.107309 | 0.108511 | 0.108724 | 0.105235 |
| r13f0 | 0.189241 | 0.169681 | 0.132510 | 0.189241 | 0.191859 | 0.180360 |
| r14f0 | 0.139987 | 0.123092 | 0.120774 | 0.139987 | 0.129589 | 0.124361 |
| r15f0 | 0.091417 | 0.092893 | 0.086782 | 0.091417 | 0.092211 | 0.089860 |

**Reproduction and artifacts**

The participant analysis used the supplied inputs only. Its tables below report each tested exploit, honest baseline, random-feature control and training-only control.

Executed: 16-split baseline; format/missingness; row position; full-data and test feature ranks/frequencies; train-only equivalents; four random-feature seeds; exact and near matches; temporal intersections; historical endpoint masks; two stronger honest restrictions; every feature alone and urban-group label means; public source/writeup search.

Not executed: external-label matching, source-data download, source-code notebooks, exhaustive feature-vintage reconstruction, extensive hyperparameter or threshold sweeps, geographic coordinate matching (coordinates absent), independent country-disjointness reconstruction, uncertainty resampling. These bounded checks do not prove absence of every exploit.

**Access disclosure**

Task files read: task.md, task.json, score.py, data.parquet, splits.parquet, and metrics.py (imported by score.py). Generated work files were read for analysis/reporting: task-gamer-report.md, make_report.py, run_attacks.py, controls.py, test_frequency.py, results.csv, summary.csv, per_split.csv, controls.csv, test_frequency.csv, diagnostics.json, feature_timing.csv, run.log, controls.log, and listings of work. Input files were never edited. No other project file, parent-directory contents, instructions, memories, other kit, credentials, remote host was inspected. Initial ls -la exposed the kit's parent directory entry metadata (..), not its contents.

The review necessarily loaded its Python dependencies, and imports caused incidental cache writes. No cache contents were inspected. Task-file access followed a participant-input-only contract rather than an enforced filesystem boundary; read-log completeness was not independently audited.

</details>

<details><summary>Review editor</summary>

**Independent cold review editor: economic well-being**

Observed 2026-11-05 UTC. **Ready for the stage owner's documented follow-through; zero genuinely new curator questions.** The review recommends shipping after the scoped split-rule documentation, preserving Myunghwan's November 2 decisions and November 5 request to reuse them. This is an editorial judgment, not a new human mark or an attestation that the documentation or build is complete.

**Assessment**

Validity: the review states the retrospective survey-gap use case, accepted annual approximation, supplied-index approximate fit and whole-country exclusion. The missing exact epochs, target construction/harmonization, interview ordering, original publisher-byte identity and label publication dates remain explicit. It does not turn unknown provenance into verified safety. The candidate-specific USE-1 / SPLIT-3 documentation follows the precedent and mediator recommendation; no generic Must waiver or new curator confirmation is invented.

Value: the final sixteen-cell probe and retained bounded-tuning evidence support signal while leaving reliable family separation unestablished. The `no_spread` finding, dependent tests and lack of exhaustive HPO remain visible. Quality: lossless Rural/Urban decoding changes canonical row order, so the review relies on verified ID-set membership and ID-aligned retained predictions, rather than applying old positional arrays.

The report retains the actual role findings and limits, including the gamer's comparisons, non-executed attacks, incomplete initial participant attempt and contractual replacement access. Its public-source GHSL observation does not establish a new future-state defect under the already accepted reconstruction framing. The two resolved issues retain their original numbers and November 2 dates; November 5 is separately attributed as preservation authority. No old mark is rebound to a current fingerprint.

**Concrete edits made**

- Changed the panel headline from “ship (focused mediator)” to “ship after documentation changes (focused mediator)” to match the actual mediator verdict and pending scoped override documentation.
- Made the outcome and main points explicit about zero new questions, the weighed evidence and remaining build follow-through. The prior scientific decisions stay settled.
- Added chronology notes to the full claim, column and precedent reports. Their predecode equivalence and then-incomplete gamer observations remain intact as dated evidence; final decoded identities and later inspection are identified separately.
- Replaced the gamer's “matched 11-random-feature control” wording with the exact twelve-versus-eleven-column limitation already stated by the mediator. Qualified “enforced by command construction” as contractual access without an OS-enforced boundary. Replaced the remaining absolute temporary-cache path with its meaningful description, preserving the incidental-exposure disclosure.
- Appended this editor report and completed the panel attribution. No role findings, measured comparisons, original resolutions or substantive evidence limits were removed.

**Evidence and verification**

I read the draft first as a curator, then the current editor role, review workflow/format, writing/principles and both knowledge indexes, the integration adaptation and decision-preservation contract. I inspected the final definition and qualification/split evidence, original annual and ship inputs, native gamer session result and full embedded role reports. The audited scientific definition is `43a922924f61ca63478edd77c10a1df5506c01245cfa2d7031d86f17744b2b6f`; its current frame hash is `aaf6121b72ee2b21705252cf7afc10ac8342dd345e3bef1321174543424b9100`. The inspected final evidence records 27 native checks, zero errors/warnings, three infos, all 32 membership sets unchanged, and all 48 retained scores reproduced after ID alignment. These are inspected audit results; I did not repeat model fits or the data experiments.

The current collector/parser accepts the edited run-local review, with issues 1 and 2 resolved, no record-field rows and seven role sections ending in Review editor. The file has no heading after its title and no local absolute path. No new scientific issue or repeated confirmation is warranted by this edit.


</details>

<details><summary>Claim and reuse audit (qualification reuse)</summary>

**Independent claim and reuse audit**

Observed 2026-11-06 UTC. Dataset: `economic_well_being_prediction_challenge`. Advisory focused claim/reuse assessment for Myunghwan; this is a new independent audit of evidence applicability, not a new human scientific decision, ownership inspection, full panel or model sweep.

**Verdict: previous scientific decisions, independent panel and probe/model evidence remain applicable; no new curator input is required.** The qualification code now selects exactly the `9048f36a1bcf7da3687fde04b18ef79cd7a1201e` scientific runtime and written procedures used for the completed November 5 qualification. No new source, feature, target, dtype, cleaning, metric, split or probe obligation was found. The current requested build still requires its own executed build, reload and traced-input reproduction evidence; this audit does not attest to their completion.

Validity: USE-1/5/8 retain the accepted retrospective survey-gap task and supplied-index approximate fit. LEAK-10 repairs and the joint forward-year/country-exclusive protocol are unchanged. The existing candidate-specific higher-ranked USE-1 / SPLIT-3 override retains its original authority and explanation; it is not a new generic waiver. Value: TP-1/2 and the existing bounded training-only experiments support useful signal; the known `no_spread` disposition remains a limitation rather than demonstrated family separation. Quality: Rural/Urban decoding, category order and canonical row/split positions remain exactly the already accepted final version. EV-7 applies to every unresolved provenance/timing statement below.

**Independently executed verification**

The new run's `independent_reuse_audit.py`, executed with the declared qualification code, writes `independent-reuse-evidence.json`. It performs native checks without report writes and fits **zero** models.

| Claim tested | Actual result |
|---|---|
| Installed code/procedure source matches the previously qualified checkout | Compared every tracked member under `src/data_foundry` and `.claude`, including role/hook files. **128 files are byte-identical**. The sole differing file is `knowledge-curation/references/splits.md`; deleting exactly one existing economic-well-being SPLIT-3 Cases row restores exact vendor bytes. No rule text changed. This extends the stage owner's 110-file native/skill check to the role/hook sources. |
| Exact final definition is unchanged | SHA-256 `04b05f736bcc376e866c3ce81cc4a11e1cff12fd151c825a4f5ce7444b13b04b`, identical to prior `qualification-final.json`. Earlier role reports' pre-documentation hashes remain historical, not the claimed present definition identity. |
| Actual raw bytes and final data remain the accepted task | Train.csv SHA-256 `caf159ff5c84630ca3ec61793ab362073cfed396e348ecca12f60f4d13efa93c` matches prior qualification. Independently reloaded prior UUID `01a1adf2-7ba6-7a75-a157-1c1451ba511e`, verified its checksum and compared its complete frame, dataset metadata, task metadata and experiment metadata with the installed-runtime check. All compare exactly, including dtype/category state, predictor/target ordering, metric and all sixteen positional memberships. Checksum remains `v2:67814a2cb764b9b4774b509d02aeb05b24c17f34e225e371229d3163fcf821f3`; stage-owner frame hash is `aaf6121b72ee2b21705252cf7afc10ac8342dd345e3bef1321174543424b9100`. |
| Memberships really implement the accepted task | Reconstructed each train side as `year < test_year AND country != test_country` and each test side as its single country-year cell. All sixteen positional arrays equal these formulas and all 32 ordered-ID hashes equal final qualification. Prior independently established counts remain 21,454 rows, twelve predictors and 6,256 distinct tested rows. |
| Actual dependency versions agree with prior build metadata | Python 3.12.3, pandas 3.1.0, numpy 2.5.4, pyarrow 26.0.0, scikit-learn 1.7.2 and polars 2.0.0 match exactly; actual LightGBM is 4.6.0. |
| Retained model evidence scores on the exact current task | Reindexed all **48** retained family/cell prediction vectors by ID, independently checked their truths and exact held-out membership, then recomputed native and direct RMSE. Every score agrees with the original retained result within `1e-14`. Prediction artifact SHA-256 is `37ecda65ac165c5b299afbc63e62a28759f89365405252fee7fde773c1f4beca`. This is score/applicability verification, not a claim of newly fitted models or identical stochastic refits. |
| Current native checks expose no new finding | 27 checks; zero errors, zero warnings, three unchanged infos: 129 conflicting-label feature profiles, integer-year calendar metadata, and explicit time/country verification retaining timing uncertainty. |

The model recipes/preprocessing and bounded selection remain their original historical experiments. Unchanged actual data/features/metadata, scientific runtime and dependency versions support their continued applicability, while the independent 48-vector rescore verifies scoring rather than reconstructing training. No new prediction or model ranking is claimed.

**Procedures, prior probes and independent panel**

The focused reuse check covered the curation rules, prior qualification and verification evidence. Features, target and splits were unchanged, so the completed bounded probes remain historical evidence rather than new fitting work.

Inspected prior final qualification/build/decision receipts, claim/column/split/precedent reports, mediator/editor reports and final dtype/leak/raw/task outputs. Their exact hashes are captured in the new independent evidence file. The final dtype probe has twelve columns and no flags. Final native leak/raw outputs and all-sixteen task results retain their original dates. `no_spread` remains investigated; the finite bounded tuning and dependent country-year cells do not establish reliable method separation or exhaustive HPO. No claim that new leak/task/model probes ran in this qualification refresh is justified or needed by this result.

The previous focused seven-role review remains applicable: claim, column, split, precedent, participant gamer, mediator and editor. The older full panel and debate remain dated evidence. The replacement participant review used contractual input separation without enforced filesystem isolation. It demonstrated no unavailable-information exploit against its random-feature and training-only controls; these bounded attacks do not prove that every exploit is absent.

**Human authority and preserved unknowns**

The new `human-input.json` preserves the exact request to repeat the three stages after the review-procedure update while reusing past decisions. Original annual-approximation and ship/joint-split decisions remain in their original dated inputs/snapshots, including the November 2 words “ok. ship it. but it's not just purely temporal -- temporal x unseen.” The original issues 1 and 2 remain resolved with their original dates, and the explicit prior-reuse CC already preserves the checked source RMSE. No changed metric or unsettled field disagreement was found.

A current review/application receipt may record carry-forward under this current explicit reuse request. Attribute that as **reuse/application authority**, distinguish it from the original scientific decisions and retain the current request verbatim; do not manufacture a fresh independent scientific ship statement or copy closed-item marks into a new fingerprint. The current review procedure also applies ship by default when issues, field disagreements and metric are all settled. This conclusion supplies no authorization for push, PR integration, claim release or global rule changes.

Cannot-verify remains cannot-verify: exact retained feature epochs, survey programme/interview dates, label availability dates, target construction and cross-survey harmonization, and original publisher-byte authentication. Annual endpoint alignment does not establish interview-time order. The sixteen evaluations share histories/countries and are dependent, not sixteen independent temporal replications. These are accepted limits of the approximate retrospective task; continued absence of evidence is no new contradiction. Concrete later-state evidence, changed labels/protocol or a demonstrated shortcut would reopen its affected decision. None arose in this alignment audit.

For the curator: **no new scientific input required**. Preserve all original decisions and qualifications. Finish current build-stage checks and review-page/application provenance under the authorized scope.

**Review scope**

This audit verifies reuse of the supplied qualification evidence and does not report new raw-data qualification, fitting or source retrieval.


</details>


<details><summary>Mediator (qualification reuse)</summary>

**Focused qualification reuse mediation: economic well-being**

Observed 2026-11-06 UTC. Independent AI advisory assessment for Myunghwan. **Verdict: ship; no new scientific decision or dataset remedy is required.** This preserves the original acceptance under the explicit request to repeat add → added review → build while reusing past decisions. It does not attest that the current build or its verification has finished.

Validity: USE-1/5/8 retain the accepted retrospective survey-gap task and supplied-index approximate fit. Existing LEAK-10 repairs and forward-year, wholly unseen-country evaluation remain unchanged. The documented candidate-specific higher-ranked USE-1 override of SPLIT-3 remains applicable; it changes no general rule. Unverified epochs, target construction/harmonization, survey/interview dates, label publication dates and original publisher-byte authentication remain cannot-verify (EV-7).

Value: TP-1/2 support the measured signal under the accepted protocol. The known `no_spread` flag remains investigated and disclosed; bounded tuning and dependent country-year tests do not establish reliable model-family separation or exhaustive HPO. Quality: the accepted Rural/Urban decoding, dtypes and canonical positions are unchanged. Weighed: measured signal and supported transfer cells favour retention; unresolved provenance and timing remain limitations. **For the curator: zero new questions.**

**Routine follow-through**

1. Preserve original decisions, dates, issue IDs and resolved turns. A current snapshot may record `ship` with a note identifying the current explicit carry-forward request and the original scientific authority. This is present reuse/application authority, not a newly invented scientific statement. Do not copy closed-item marks or reassign old fingerprints. The current review procedure also applies ship when issues, fields and metric are all settled; the exact request and current package identity should remain inspectable (review-added Step 4; EV-7/8).
2. Append the current focused claim/reuse audit, this mediation and the forthcoming editor assessment to the existing review block, preserving the previous seven-role reports and their dates. Distinguish the new three-role applicability review from the prior focused scientific work and the older full panel/debate. No additional column/split auditor or gamer is triggered when those subjects are unchanged (panel Tiers).
3. Complete the already authorized build, saved-container reload/checksum and traced-input reproduction on the installed runtime. Mint a new UUID; record the actual clean source commit and expected unchanged scientific checksum. The prior build proves its own result only. Review-only documentation additions and their final commit may follow a build from the existing clean scientific commit, provided the recorded identity is accurate and no definition changes intervene. Report skipped checks and actual outcomes; do not claim newly fitted probes or models (rebuild Steps 2/3/6; EV-7).

No candidate change is recommended. The editor and stage owner retain their own completion obligations.

**Agreed facts and inspected evidence**

I read the completed independent reuse audit and its evidence JSON, the stage-owner reuse verification and current attributed request, prior mediator/editor/decision-reuse/register-disposition reports, current definition and record, final qualified review summary, updated runtime test result, and current add/panel/review/build and principles/evidence guidance. The decisive new applicability checks were executed by the independent auditor; I did not rerun them or fit models.

The installed scientific source is `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, the same source used for final November 5 qualification. The auditor extends the earlier 110-file comparison to **128 identical runtime, skill, role and hook files**; the sole additional difference is the already accepted economic-well-being SPLIT-3 Cases row. No rule text or new obligation changed. Actual dependency versions match the previous build metadata. A changed import location therefore supplies no scientific reason to refit unchanged experiments.

Definition SHA-256 remains `04b05f736bcc376e866c3ce81cc4a11e1cff12fd151c825a4f5ce7444b13b04b`; frame hash remains `aaf6121b72ee2b21705252cf7afc10ac8342dd345e3bef1321174543424b9100`. Raw bytes, complete frame, metadata, target, twelve predictors, dtype/category state and all sixteen positional split arrays equal the previously saved container. The auditor independently reconstructs train as `year < t AND country != c` and test as the country-year cell, verifies all 32 ordered-ID hashes and reproduces all 48 retained prediction scores within `1e-14`. This verifies applicability and scoring, not new model training or identical stochastic refits. The protocol retains 21,454 rows and 6,256 distinct tested rows; its overlapping histories and countries remain dependent.

Current native checks report 27 checks, zero errors/warnings and three unchanged infos: 129 conflicting-label feature profiles, numeric-year calendar metadata, and explicit chronology/country verification with unresolved epoch limits. The updated-runtime suite log reports **2,017 passed, 286 skipped and twelve pytest warnings**; those warnings are separate from the native dataset findings.

No new gamer run is reported because features, target and splits are unchanged. Prior bounded attacks demonstrated no unavailable-information exploit, while leaving untested attacks explicit. Their mapping to LEAK-5/9/30, LEAK-13/15 and LEAK-16/17/21 remains the prior mediator's analysis. The completed independent replacement review used contractual input separation; no enforced filesystem isolation or complete independently audited read log is claimed.

**Consistency and remaining uncertainty**

The original November 2 annual-approximation and supplied-index ship decisions remain the scientific authority, including the explicit temporal × unseen-country correction. The current request is separately retained as reuse and local-stage authority. No contradictory fact, changed mechanism or new weighing choice is established. The prior register disposition still explains the scoped higher-ranked USE-1/SPLIT-3 relationship and USE-1 lexical overassociation; repeated documentation of the same candidate is not another exception. Do not suppress flags or amend the general Must rule to obtain a clean report.

Unknown represented epochs and harmonization do not become verified through byte identity or rescoring. Concrete actual later-state content, changed labels, broken membership or a demonstrated shortcut would reopen the affected decision. None was found in this alignment check. The current request adds no authority for push, PR publication, claim release.


</details>


<details><summary>Review editor (qualification reuse)</summary>

**Independent cold editor: qualification reuse**

Observed 2026-11-06 UTC. Independent AI advisory assessment for Myunghwan. **Ready for the stage owner's current review/application and requested build follow-through; zero genuinely new curator questions.** Preserve the November 2 scientific acceptance under the current explicit carry-forward request. This editorial assessment does not attest that a new review-store entry, build, reload or traced-input reproduction has completed.

Validity: the existing review clearly describes the accepted retrospective survey-gap task, annual timing approximation, supplied-index approximate fit and whole-country exclusion. Existing repairs and the documented higher-ranked USE-1 / SPLIT-3 override remain intact. Value: measured signal supports retention; `no_spread`, bounded tuning and dependent country-year evaluations leave reliable model-family separation unestablished. Quality: the accepted Rural/Urban decoding and canonical ordering are unchanged. Weighed: identical scientific inputs/protocol and supported signal favour reuse; unresolved timing/provenance still limit the interpretation. No new choice is hidden in the current reports.

**Cold read and evidence**

I read the existing candidate REVIEW.md before the new request, reuse audit and mediator. Its original issues 1 and 2 remain resolved on November 2, with November 5 reuse authority separately identified. The historical seven-role focused reports preserve their differing predecode/postdecode scopes, measured comparisons and limits. They are intelligible as dated evidence; the current three-role assessment must supplement them rather than claim to rerun them or replace the older full panel/debate.

I then read the actual current request, stage-owner reuse verification, complete independent reuse report/evidence and completed current mediation, plus current editor, panel, review-format, writing/principles and decision-preservation guidance. The independent auditor verifies 128 identical runtime/skill/role/hook files, with the preserved economic-well-being SPLIT-3 Cases row as the sole difference. The installed and previously qualified scientific base is `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Current definition SHA-256 is `04b05f736bcc376e866c3ce81cc4a11e1cff12fd151c825a4f5ce7444b13b04b`; the older embedded report hashes describe their historical snapshots.

The inspected evidence verifies the same raw bytes, complete frame/category state, all dataset/task/experiment metadata and all sixteen positional memberships against the prior saved container. All 32 ordered-ID hashes match; independently reconstructed train/test formulas match; all 48 retained prediction scores reproduce within `1e-14` after ID alignment. Native checks remain 27 with zero errors/warnings and three infos. These are inspected audit results, not experiments I independently reran. No new model fit or new leak/task probe run is implied. The current mediation reports the updated-runtime suite as 2,017 passed, 286 skipped and twelve pytest warnings, distinct from the zero native dataset warnings.

**Concrete editorial changes for the stage owner**

1. Replace the outcome's stale “Recommend shipping the previously accepted temporal × unseen-country task after documenting its scoped split-rule override” with “Recommend shipping the accepted temporal × unseen-country task under the current explicit reuse request; the qualification code selects the same qualified scientific source.” Keep its validity/value/quality limits. Replace “the requested build remains a subsequent step” with the actual executed build disposition only after that work is verified.
2. Replace the panel recommendation “ship after documentation changes (focused mediator)” with “ship (focused qualification reuse mediator)”. Replace the sentence “No new curator input; preserve the prior decisions and complete the scoped split-rule documentation before the requested build” with “No new curator input; preserve the original decisions and completed scoped split-rule documentation. The current claim/reuse auditor, mediator and cold editor verify applicability after qualification reuse; the prior seven-role scientific review and older full panel/debate remain dated evidence.” Keep the original reports unchanged and append the three current reports under the single existing panel label. The new recommendation describes this current focused pass, not a retroactive rewrite of the prior mediator's verdict.
3. Keep Main points explicit that no new question is raised and issues 1 and 2 retain their original numbers and November 2 dates. Do not create an issue for unchanged unknown provenance, an identical `no_spread` disposition or a repeated request to approve the joint split. No new field disagreement or metric choice is established.

**Review/application provenance**

A fresh current snapshot may carry a `ship` entry based on the actual current request to repeat add → review → build using past decisions, with the request retained verbatim and its note explicitly calling this carry-forward/application authority. That is an honest recording of current authority, consistent with the review procedure's settled-issues default. It must not be described as a newly elicited independent human scientific verdict. Do not copy the old closed-item marks, replace their original fingerprints or invent fresh issue/metric marks. Preserve the original scientific decisions, words, dates and source identities separately. Bind any later operator-application receipt to the exact final files it actually applied; the present report reviews this plan, not an entry or receipt that does not yet exist.

A new UUID with the unchanged scientific checksum is compatible with the requested repeat build. Record the actual clean build-source commit and final documentation commit separately. Only executed build/reload/reproduction evidence can establish this cycle's completion. Neither unchanged bytes nor this editor's recommendation proves a new build succeeded.

**Gamer and scientific limits retained**

No new gamer run is reported for unchanged features, target and splits. The initial attempt did not run; its completed independent replacement followed a participant-input-only contract without enforced filesystem isolation or an independently audited complete read log. Dependency imports, incidental cache exposure and directory-entry metadata remain access limitations. Input hashes establish identity, not enforcement. Bounded attacks found no unavailable-information exploit; external-label lookup, coordinate matching and exhaustive vintage reconstruction remain unexecuted.

Exact retained covariate epochs, survey programme/interview ordering, target construction and cross-survey harmonization, label publication dates and original publisher-byte authentication remain unverified. Annual alignment is not interview-time ordering; shared histories and countries are not independent temporal replications. Byte identity and rescoring do not resolve these accepted limits. Concrete later-state content, changed target/protocol, broken membership or a demonstrated shortcut would reopen the affected decision; none is established here.

**Review scope**

The run-local proposed concatenation passes the installed current collector and panel parsers: one panel, ten role sections, original issues 1 and 2 resolved, zero open issues and zero field rows. The three appended reports retain their full substantive content with headings converted to bold and the private absolute import path replaced by its meaningful repository-relative module path. No second panel label or post-title heading is introduced. This is format verification, not proof that the stage owner has installed these edits.

This editorial review makes no new scientific or experimental claim.

</details>
