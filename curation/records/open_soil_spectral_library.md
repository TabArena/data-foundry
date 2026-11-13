---
unique_name: open_soil_spectral_library
name: Open Soil Spectral Library (OSSL) / KSSL MIR soil spectra
checked_by:
- Myunghwan
- Lennart
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Many features
- Non-IID (Grouped)
- Spectral Data
- 'Samples: Over Time'
- 'Time: Dated'
collections:
- New (BeyondArena)
original_source: Website
year: '2023'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1371/journal.pone.0296545
- https://doi.org/10.5281/zenodo.7599269
- https://docs.soilspectroscopy.org/
- https://github.com/soilspectroscopy/ossl-models
v2_path: datasets/_dev/tabarena-v0pt2/open_soil_spectral_library/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: a well documented open library of lab spectra with wet-chemistry reference values, built to calibrate the models that predict soil properties from a scan, in a spatially grouped regime; the open point is whether spectra are in scope (SEL-15).
- Source: Soil Spectroscopy for Global Good, Open Soil Spectral Library; data on Zenodo (doi 10.5281/zenodo.7599269, v1.2), paper Safanelli et al., PLOS ONE 20(1): e0296545, 2025. As published: 135,651 entries harmonised from KSSL, LUCAS, AfSIS1/2, ICRAF-ISRIC and smaller libraries; MIR and VisNIR scans plus about 40 soil properties (SOC, clay/silt/sand, pH, CEC, extractable cations, ...); 87,707 entries with coordinates; separate tables for site, lab values and each spectral range, joined by sample id. Licences differ per library (LUCAS under a JRC agreement; noted only, EV-4).
- Use case: the paper: users "need to predict soil properties from spectra collected on any spectrometer", and the OSSL Engine returns predictions for uploaded spectra; the actor is a soil lab or survey that scans a sample instead of running wet chemistry; fit direct. Regime grouped by location or profile (several layers per site); the paper's own 10-fold CV does not say it was grouped (SPLIT-3).
- Siblings and duplicates: `open_soil_data` (Lennart `No`: 96% of its values are spectroscopy-model predictions; this is a measured parent), `lucas_topsoil` (AI `TBD -> Yes`; LUCAS VisNIR spectra are inside OSSL), `africa_soil_property_prediction_challenge` (AfSIS MIR is inside OSSL), `bloodsai_blood_spectroscopy_classification_challenge` (the same spectroscopy question). Precedent for spectra: `micro_mass` (MALDI-TOF spectra, `Yes`, Lennart and Andrej). External collections: none found.
- Papers and pages: the PLOS ONE paper (Cubist ranked best; SNV and the first 120 principal components), docs.soilspectroscopy.org, github.com/soilspectroscopy/ossl-models.
- Metric: the paper reports RMSE, bias, R2, Lin's CCC and RPIQ and ranks models by CCC together with RPIQ, several side by side, so the fallback `rmse` on one property (MET-5, MET-11). Inputs: none.
- Risks for /add-dataset: pick one spectral range and one library cut (KSSL MIR is the largest single-instrument set) to avoid overlap with `lucas_topsoil` and the AfSIS records (PROV-6); one target, or a declared multi-target (CLEAN-18); some KSSL coordinates are county centroids, so group by profile or site, not by coordinate; about 1,700 MIR bins (raw spectral bins weigh -, SEL-15).
- Priority: gap + (Grouped thin), use case + (the paper names the users and the decision), source + (paper, Zenodo, docs), shape + (tens of thousands of samples, grouped), risk - (joins across tables, overlap with sibling libraries, the spectra question).

Safanelli et al., PLOS One 20(1):e0296545, 2025. Compilation of soil spectra with laboratory reference values, v1.2 on Zenodo (CC BY 4.0, 2021-12-26): "MIR (91,631) and VisNIR (65,063) spectral scans + soil calibration data (>60,000 unique locations)"; "from more than 135,000 entries in the OSSL, 87,707 samples have spatial coordinates". Table 1: KSSL (USA) 21,857 MIR + 10,521 VisNIR, CC; LUCAS (EU) 21,711 VisNIR under a "JRC license agreement" with geographic restrictions; AFSIS1 1,457 MIR (ODbL); AFSIS2 3,573 MIR (CC); ICRAF-ISRIC 1,841 MIR; CAF 715; Schiedung 422; Garrett 263; Serbia 410 (shared internally, not redistributable). Reference properties: >40 harmonised (SOC, clay/silt/sand, pH, CEC, extractable K/Ca/Mg/Na/P/B/Zn/Mn, EC, bulk density, ...). Own models: "Cubist was adopted as many studies have found it to be one of the top performing models", SNV preprocessing, "first 120 principal components" of each range; 10-fold CV Lin's CCC 0.95 for SOC (MIR), 0.84 pH, 0.74 clay.

Why it is the dataset to settle the spectroscopy question on: the incumbent models in this field are Cubist, PLSR and memory-based learning, i.e. tabular-style learners on ~1,700 wavenumber bins, so "modality-specific models clearly superior" (criterion 4A) is not obvious here; the `Wrong Domain / Source Modality` marker is the provisional flag, not a verdict. Same call would settle `bloodsai_blood_spectroscopy_classification_challenge`. Licence mix (LUCAS under a JRC agreement, Serbia internal) is noted, not a factor. Points to decide: one spectral range (MIR), spatially grouped split by site (many layers per location), and the library "spatially over-represents USA and European Union". Data not inspected.

Drafted 2026-09-23 as a follow-up to `open_soil_data` (iSDA), whose 49k rows are 96% spectroscopy-model predictions; this is one of the measured-data parents of that family (`open_soil_spectral_library`, `africa_soil_property_prediction_challenge`, `africa_soil_profiles_database`, `lucas_topsoil`, `wosis_soil_profiles`).

CC (2026-10-26, Myunghwan): yes, pursue this. but if the target is weight percent, we need to check if transofmration this into [0, 1] is better or not.

**Assessment (AI, 2026-10-27):** Applied the actual saved screening approval, original SHA256 cdf3786fbf6f124bbdafb2a29bffbd9c8a682ef8cea1b4140a1a63f6c5b45e75, after independent consistency review. No final transform, split, scorer, inclusion or build choice is inferred. The provisional modality concern remains for qualification. The task has one target; existing triage reservation and historical comments are preserved.

**Assessment (AI, 2026-10-27):** Current add-stage measurements supersede historical source-only counts and direct-assay/direct-fit interpretations above. The archived KSSL subset joins one-to-one on dataset code and layer UUID: 86,603 source rows, 76,813 complete MIR scans, 75,929 usable scan/reference pairs and 20,626 native LIMS keys. Source OC is a total-C-based analytical estimate, exactly reconstructed S-first/N-fallback; 62 usable zeros are retained, no negative or >100 targets remain, and upstream pre-import sentinel counts cannot be recovered. All 1,701 spectral bins are predictors; all chemistry and identifiers are excluded. All nine folds separate native keys, but every key is not certified as one physical profile; archive/standard groups and possible shared WoSIS/ISRIC origins are disclosed. The proposed source-origin RMSE cites original-unit external evaluation while distinguishing deliberate inner log1p RMSE. Bounded percent/fraction checks show no material aggregate improvement; final scorer, split, representation, scope and inclusion remain with Myunghwan. No build or dataset source commit. Priority 3: gap 0 (133 accepted definitions show this domain/problem/regime is not thin), use case + (source scan-upload laboratory calibration), source + (institution, immutable archive and paper), shape + (75,929 rows and grouped structure), risk - (physical-group/assay-equivalence and spectral-scope limitations).

**Assessment (AI, 2026-10-27):** Existing-folder recheck in a fresh pinned copy: native dataset check passed with zero errors/warnings and the disclosed heavy-check information item; the regenerated README is byte-identical to the retained qualified card. Current full frame and all nine fold memberships match the retained science, including exact sampled rows and retained paired predictions. No learner was refitted. Source/reference, leakage/task and bounded group evidence is reused only for this unchanged task; the native group command remains interrupted, not passing. Full earlier panel reports are inherited; the current focused panel and cold final-package review remain to run. All five published choices remain open; no build or inclusion decision. Priority 3: gap 0 (133 accepted definitions), use case + (source laboratory calibration), source + (documented archive), shape + (75,929 rows, grouped), risk - (spectral scope and reference/physical-group limitations).

**Assessment (AI, 2026-10-27):** Current focused independent claim, column, split and domain audits and mediation support the bounded archived calibration proposal, subject to all five published human choices. Corrected the source-key evidence limit: the importer first aggregated taxonomy per native key, so archived taxonomy agreement cannot certify physical-profile identity. The new complete column audit supersedes the inherited physical-profile wording for the grouping row. No rows, predictors, references, numeric metric, fold memberships or target representation changed; no learner refit. Required cold exact-package editor review remains pending. Priority 3: gap 0, use case +, source +, shape +, risk - (spectral scope and reference/group interpretation).

**Assessment (AI, 2026-10-27):** Cold independent editor reviewed the compact and human-facing draft. Clarified retention of all usable scan/reference rows after documented missing-input/reference exclusions; no discretionary row exclusion or numerical method changed. Corrected native review-evidence capture to include actual custom tool calls/results and explicitly distinguish encrypted dispatch payloads from readable child task readbacks. Exact final-byte re-review/completion is pinned in the external package receipt. All five human choices remain open; no build or inclusion decision.

**Assessment (AI, 2026-10-27):** Direct add-dataset continuation preserves the current definition, all prior scientific measurements and the five published issue IDs. Earlier pending external-package-receipt statements describe the interrupted controlled run, not a scientific requirement. The current task is unchanged: finish editor corrections, regenerate the card and verify the final review documents. No new screening, model fit, inferred human decision, build or dataset commit. Priority 3: gap 0, use case +, source +, shape +, risk - (spectral scope and reference/group interpretation).

**Assessment (AI, 2026-10-27):** Direct pre-human-review add-dataset work is complete. The regenerated card passed 26 native checks with zero errors and warnings; heavy automatic duplicate checks remain a disclosed information skip with unchanged-frame full-spectrum audit evidence. Exact full-frame, all nine folds and saved paired-prediction scores match the retained investigation, with zero new fits. Record, pointer, priority, table and review-format checks passed. The final independent editor found no necessary document edits. The existing full and focused scientific panels are preserved, not rerun or replaced by self-review. The earlier interrupted native group command and fresh-machine decode limitation remain explicit; bounded follow-up group evidence is distinct. All five published choices await Myunghwan, and no ship, representation, split or scorer decision is inferred. Priority 3: gap 0, use case +, source +, shape +, risk - (spectral scope and reference/group interpretation).

CC (2026-10-27, Myunghwan): “For 1, let's use the measurements. For 3, let's stck to the orignal target and eval.” Retain all 1,701 measured MIR inputs, the original weight-percent target and per-row RMSE; the reference target itself is accepted (“It's fine even for the archieved reference”). The normalization discussion's number 3 did not approve a split.

CC (2026-10-27, Myunghwan): “OK. group id is slightly better. stick to group id.” Further scope: “we can regard each id as the "experiment/measurement batch". still OK in real-world scenario”. Keep whole native source-ID groups together, predicting and scoring each row separately. Measurement-batch interpretation is the chosen benchmark scenario, not verification of one-to-one experimental batch or physical-profile identity.

**Assessment (AI, 2026-10-27):** Applied all five settled task-definition choices and removed their resolved open issues, retaining their full panel and decision history in the run. The definition's executable loading, cleaning, target values, feature list and fold memberships are unchanged. Removed the provisional modality marker after approval of the measured spectral inputs. Added the bounded same-fold few-band/PCA findings without replacing raw inputs or choosing a preprocessing method. Final add-stage checks and editorial review precede the requested review-added-datasets discussion. No overall ship verdict, build or dataset commit is inferred. Priority 3: gap 0, use case +, source +, shape +, risk - (reference and source-group interpretation limits).

CC (2026-10-27, Myunghwan): Finish add-dataset work and then move to review-added-datasets on this dataset. This instruction supplies no overall ship verdict.

**Assessment (AI, 2026-10-27):** Add-dataset is complete with the confirmed task choices applied. Post-choice regeneration returned 26 checks, zero errors and warnings, with heavy duplicate checks explicitly skipped and separate applicable spectrum audits retained. The complete frame hash and all nine fold memberships are unchanged; records, pointers and the generated table passed. Independent decision-consistency and final editorial review found no necessary corrections. All five original issue IDs are resolved in preserved history. Review-added-datasets now considers the completed definition and disclosed limits, with the overall curator verdict still open. No build, dataset commit or publication. Priority 3: gap 0, use case +, source +, shape +, risk - (reference/group interpretation limits).

**CC (2026-10-28, Myunghwan):** "ship all". Approved this dataset for shipping in the five-dataset final added-dataset review (beMTPL97, Eucalyptus, Tanzania tourism, CPS88 wages and OSSL), on the exact presented definition with previously settled task choices and disclosed limitations retained. This is scientific acceptance for a separately requested build; it does not authorize build, commit or publication.

**Assessment (AI, 2026-10-28):** The independent consistency check supports applying this overall verdict without another task choice. Existing local curator dispositions remain distinct from source verification or shared-rule amendments. No definition, scorer, data, fold or warning acceptance was changed by this final verdict.

CC (2026-11-04, Lennart): the 1,701 MIR bins are declared as a spectrum ("delacre it"): renamed `mir_<n>`, `Spectrum(name="mir_spectrum", prefix="mir_", unit="cm-1", technique="infrared", state="raw")` (CLEAN-26). The target ships on the source's scale, log1p with the transform ("Follow the source metric and scale"); the metric on it is open (Review issues 2-3).

**Assessment (AI, 2026-11-04):** with the spectrum declared, ALS + SNV improves LightGBM from 1.74 to 1.33 % RMSE on all three folds (repeat 0, untuned); a Savitzky-Golay first derivative, not registered, gives 1.24. LightGBM then beats ridge, which reverses the earlier 5,000-row diagnostic. `state="raw"` holds: KSSL exports averaged absorbance on the 600-4000 cm-1 grid and OSSL applies SNV only inside its models.

CC (2026-11-04, Lennart): the metric is the source's cross-validation metric, `rmsle` on the log1p target ("follow the recommendation, following the source"); the group description stands; the 600 cm-1 bin, a fill in 53 spectra, is dropped for every row ("do (b), document how to find this in the skills going forward"), and spectra.md now says how to find edge fill values.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled. (superseded 2026-11-04: the full review panel ran in a second pass)

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (text, notes and filing; no row, split or metric change; the definition's text fixes are made: the four texts that said "scored in weight percent", the group description, the shift to later scans and new projects (8-26% worse, LightGBM), the encodings on the declared scale, the layers above 58% organic carbon, which equal the source's measured total carbon); disputed: MET-5 (holds, or departs until its fact is filed), CLEAN-16 (rename by default); settled by the mediator: EV-7 (shift note states the error level only), EV-1 (encoding evidence on the declared scale), CLEAN-11 (high values kept); for the curator: issues 6-10. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (gap: no thin domain, problem type or regime among 107 accepted definitions; use case: the source names the actor, but the fit is approximate, with instrument transfer and later scans untested; risk: no open issue raises a leak, an unclear target or damage).

**Assessment (AI, 2026-11-04):** the CC of 2026-11-04 that cites "Review issues 2-3" means issues 2 and 3 of the first PR #33 review page (metric origin, target scale), which never became a file in the folder. `curation_comments` now say that only the three layers above 70% organic carbon were checked against the source's measured total carbon (second-pass panel; Lennart's go-ahead on the review page).

CC (2026-11-05, Lennart): the spectrum only, with the source's scan-upload service as the actor (issue 6, ok on the implemented option; USE-3, USE-6). A KSSL laboratory also knows the layer's two depths and the preparation code (XS or XN), and adding them lowered RMSLE by 3.6% on the two folds tried; leaving them out is a choice of actor, now said in the task summary. The service accepts none of them: the OSSL API v1.2 prediction call takes the spectra file, the property, the spectral range, the subset (KSSL or OSSL) and the model; depth is only a filter for downloading library rows; every v1.2 model is coded `na`, "only the spectra data" (api.soilspectroscopy.org, the ossl-models README; checked 2026-11-05).

CC (2026-11-05, Lennart): the fact that sets the log-scale metric apart from forest_fires is filed as a MET-5 case (issue 8, A; MET-5): the source tunes by RMSE on log1p and reports its 10-fold CV on log1p for exactly this cut (n = 75,929, RMSE 0.114, CCC 0.995), with the laboratory and instrument the split keeps; its ranking by CCC with an RPIQ cut-off is a compound grade, and its percent results come from the independent sets, the instrument transfer this task does not test.

CC (2026-11-05, Lennart): the dropped 600 cm-1 edge is filed as an amendment of the spectrum rule (issue 10, A; CLEAN-26 as amended 2026-11-05, narrowing CLEAN-11): a fill at an edge position drops that position for every row, a fill at an inner position is set missing and the column stays. Re-counted on the raw export: 53 spectra read 0 at 600 cm-1 beside 1.27 to 1.86 at 602 cm-1.

CC (2026-11-05, Lennart): the declared metric (`rmsle` on weight percent, the RMSE of the shipped log1p values, the source's) is checked and stays as declared.

CC (2026-11-05, Lennart): the target column is renamed to `log1p_organic_carbon_weight_percent` (was `organic_carbon_weight_percent`), the values unchanged (issue 9, A with (a); CLEAN-16, filed as a case): the old name stated a unit, weight percent, that the shipped log1p values (0 to 4.375) contradict, and the blind reviewer took them for something other than percent; the names kept with a declared `target_transform` (diamonds and mercari `price`, allstate `loss`, forest_fires `area`) state no unit.

CC (2026-11-05, Lennart): the `no_spread` flag is left unrecorded for this dataset only (Review issue 7, (b)): its default families all reach skill 0.98-0.985.

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. The KSSL part of the Open Soil Spectral Library v1.2: 75,929 archived soil layers, each with its
mid-infrared spectrum (1,700 bins from 602 to 4,000 cm-1, declared as a spectrum, `state="raw"`) and its laboratory
organic carbon, shipped as log1p and scored by `rmsle` (the RMSE of the shipped log1p values, the source's
cross-validation and tuning scale), with whole KSSL pedon keys held out. Verdict: ship after changes (review panel,
full, second pass after your PR #33 review of 2026-11-04); the text changes in the definition are made, while the
record's AI note on "issues 2-3" and the `spectra.md` table and its "1,701" are still to be updated. Validity: USE-3 and USE-5 hold (fit approximate); USE-6 holds for the source's scan-upload actor, and which
actor to model is your call (issue 6); LEAK-1, LEAK-10, LEAK-16 and CLEAN-23 hold (rows shuffled, no attack beat the
honest baseline); SPLIT-1, SPLIT-23, SPLIT-24 and SPLIT-29 hold, and the notes now describe the group as it is and the
untested shift to later scans and new projects (SPLIT-31). Value: MET-3 holds; MET-11 failed in four texts that still
said "scored in weight percent" (fixed); MET-5 departs from `forest_fires` without the fact on file (issue 8); TP-3
`no_spread` has no recorded disposition (issue 7). Quality: CLEAN-16 says to rename a transformed target, against four
precedents that kept the name (issue 9); the CLEAN-26 edge-bin drop is not filed (issue 10); CLEAN-11 keeps the 151
layers above 58% organic carbon (the three above 70% equal the source's measured total carbon; note added). Weighed:
size +, source +, use case +, saturation (R² 0.98) -, transfer to other instruments and to later scans untested -.
Left for you: issues 6-10, five decisions; a rebuild on your ask (the container of 2026-10-29 predates the target,
metric and bin changes); and Myunghwan, who holds the claim and approved ("ship all", 2026-10-28) the definition
before those changes, should be told before shipping.

**Main points:** Spectrum only, or also the depths and preparation code a KSSL lab knows (6)? Record the `no_spread`
keep (7)? File the fact that sets the log-scale metric apart from `forest_fires` (8)? Rename the target to
`log1p_organic_carbon_weight_percent` (9)? Confirm the CLEAN-26 amendment for the dropped edge bin (10)?

**Record judgment:** valid. Your CC lines of 2026-11-04 replace Myunghwan's percent target and RMSE (2026-10-27) and
come after his "ship all" (2026-10-28); `claimed_by: Myunghwan` still reflects his stage. The CC line that cites
"REVIEW.md issues 2-3" means issues 2 and 3 of the PR #33 review page (metric origin, target scale), which never became a
file in the folder; an AI note saying so is still to be added to the record. The Assessment "review panel (none)" is superseded by this panel's line.

**Issues for Lennart:**

6. **Inputs: the spectrum only, or also the depths and preparation code a KSSL lab always has?**

   * **Problem:**
     - The task follows the OSSL Engine, the source's scan-upload service, where a lab uploads a spectrum and gets an
       estimate back, so the inputs are the 1,700 bins only.
     - A KSSL laboratory scanning its own sample also knows the layer's upper and lower depth and its preparation code
       (XS or XN, part of the scan id) when the sample arrives, and anything known at the prediction point is a
       legitimate input whose removal changes the task[^use6].
     - Under the OSSL Engine actor the service never sees the depths, so that rule holds; under a KSSL lab's own use,
       leaving them out breaks it, so which actor to model is a framing call[^use3].
   * **Effect on the task:** In effect, a model here predicts as the upload service does, about 3.6% worse than it
     would with what a KSSL lab knows.
   * **Experiments:** Adding the three lowered RMSLE by 3.6% on both folds tried (0.1428 to 0.1376 and 0.1446 to
     0.1393; LightGBM on SNV and 80 principal components, repeat 0; domain practitioner).
   * **Unknown:** On the Engine's inputs, the definition's notes say it "does not require" field metadata, while the
     panel's evidence (claim C1, the domain practitioner, the mediator) has it taking the spectrum only; whether it
     accepts optional depth was not checked, and if it does, the actor argument is weaker.
   * **Consistency:** No precedent has the same facts; the rule's cases (`brazilian_ecommerce`,
     `bias_correction_r_bias_correction_r_2`) are about a company's own estimate.
   * **Panel:** No panel member argues the spectrum-only task is wrong.
   * **Cost of B:** a different actor from the source's service, three non-spectral inputs, and a task the source's
     models do not address.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Spectrum only (implemented) | OSSL Engine actor; 1,700 bins | the source's service | about 3.6% worse |
     | B | KSSL in-house laboratory | adds the two depths and the preparation code | -3.6% RMSLE | another actor |

   * **Recommendation:** A (mediator): keep the spectrum only, and say in `known` that leaving depth and preparation
     out is a choice of actor. **Decision:** which actor?

   **Notes for the AI:** under A, `known` says field metadata is not an input to the source's task; add that leaving
   depth and preparation out is a choice of actor.

   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input; dropping it changes the
     task. Cases: brazilian_ecommerce, bias_correction_r_bias_correction_r_2.
   [^use3]: **USE-3** (Must): name the prediction point, when the model is used and what is known then.

   **Resolved (2026-11-05, Lennart):** as implemented. The OSSL Engine and API take the spectrum alone (no depth input;
   every v1.2 model uses "only the spectra data"), so the spectrum-only actor stands; `known` says so.

7. **Record the `no_spread` flag as "keep pending tuned results"?**

   * **Problem:**
     - The task probe flags `no_spread`: the best and worst default model families differ by less than twice the
       standard error of their per-split difference.
     - Each precedent recorded its keep with numbers, and this record has no line on the flag[^tp3].
     - A filing call: record the keep, or treat the flag differently?
   * **Background:** Skill (1 minus the model's error over a dummy's error) is 0.985 linear, 0.980 LightGBM and 0.978
     random forest, on the first 5 of the 9 splits (the probe's default for a large dataset), so default models
     converge on this large, low-noise task.
   * **Experiments:** On the declared scale they still spread: in one run (repeat 0, three folds, untuned, fitted on
     log1p) LightGBM scores 0.155 on the spectrum as it is and 0.118 with a Savitzky-Golay first derivative, PLS 0.158
     and ridge 0.142.
   * **Consistency:** `amex_non_iid_1m`[^tp2], `electric_motor_temperature_prediction`[^tp3] and
     `open_university_learning_analytics_dataset` ("kept pending tuned results", you, 2026-10-22) each recorded the
     keep with numbers. More than 15 `no_spread` keeps in the rule's cases were kept without looking into the flag,
     and no fact here sets this case apart.
   * **Panel:** The source's Cubist 0.114 stays out of the spread: it comes from a cross-validation the paper does not
     call grouped (the critic's point, accepted).
   * **Cost of B:** like cases would be treated unlike, and the dataset waits on an investigation with no named
     question.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep pending tuned results | spread 0.118-0.158 in the record; cases row | as the precedents | none stated |
     | B | Look into the flag | the dataset waits on an investigation | none stated | like cases treated unlike |
     | C | Nothing recorded (implemented) | no line on the flag | none stated | unlike the precedents |

   * **Recommendation:** A (mediator). **Decision:** A or B?

   **Notes for the AI:** on A, write the keep with the spread 0.118 to 0.158 into the record and add a TP-3 Cases row;
   the Cubist 0.114 stays out.

   [^tp3]: **TP-3** (Must): if tuned methods spread, keep the dataset; its Cases table holds more than 15 `no_spread`
     keeps.
   [^tp2]: **TP-2** (Should): a small but real signal is no reason to retire; the precedent's keep is filed here.

   **Lennart (2026-11-05, ok):** Remove this comment or ignore it going forward, we can move one as is

   **Answer (AI, 2026-11-05):** Done for this dataset: nothing is recorded on the flag (TP-3 holds; the default families
   all reach skill 0.98-0.985). "Ignore it going forward" sounds like a standing rule; where should it go?
   - (a) the `no_spread` row of the flag table in task_probes.md: on a large dataset whose default models all reach a
     skill near 1, the flag is not raised;
   - (b) only here.

   **Lennart (2026-11-05, ok):** Reply (b): only here

   **Resolved (2026-11-05, Lennart):** (b). Nothing is recorded on the flag here, and no standing rule.

8. **File the fact that sets the log-scale metric apart from `forest_fires`?**

   * **Problem:**
     - Your CC of 2026-11-04 declares `rmsle` on the log1p target, the source's tuning and cross-validation criterion,
       while the paper ranks its model types by Lin's CCC with an RPIQ cut-off of 2.
     - `forest_fires` (2026-10-21) declared the criterion its paper ranks by, and the reason on file here, "follow the
       source", does not say why this case differs[^met5].
     - A consistency check: is the fact that sets this case apart filed?
   * **Consistency:** `gallstone_disease` and `heart_disease` took the fallback when a paper used several criteria,
     and the screening and Myunghwan's CC of 2026-10-27 had the fallback `rmse` in percent.
   * **Background:** The AI's best guess at the fact: the source's 10-fold cross-validation on log1p was run on exactly
     this cut (n = 75,929, RMSE 0.114, CCC 0.995, in the
     [source's model-performance table](https://github.com/soilspectroscopy/ossl-models)), with the laboratory and
     instrument our split keeps, while its percent-scale results come from independent sets, the instrument transfer
     this task does not test. The practitioner's weighting by organic-carbon band supports it: `rmsle` weights the
     mineral soils at or below 3%, where the decisions sit.
   * **Effect on the task:** Under B the score is set by the 16% of organic layers, which carry 78 to 87% of the
     squared error.
   * **Panel:** No panel member disputes the choice; the critic and the mediator hold that it departs from the rule
     until the fact is filed[^met5].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | File the fact | the fact above as a cases row | keeps your CC | none stated |
     | B | Fallback `rmse` in percent | scored in weight percent | none stated | reverses your CC; organic layers rule |
     | C | Reopen `forest_fires` | `forest_fires` matched to this case | none stated | none stated |
     | D | Amend the metric rule | tuning on the same cut beats a compound ranking | none stated | none stated |
     | E | Nothing filed (implemented) | `rmsle` on log1p, origin `source` | none stated | case not set apart |

   * **Recommendation:** A (mediator). **Decision:** A, B, C or D?

   **Notes for the AI:** on A, record the fact above as a MET-5 Cases row; on D, amend MET-5 so that a tuning
   criterion run on the same cut beats a compound ranking criterion.

   [^met5]: **MET-5** (Should): a paper's metric is the source's metric only when it is one deliberate choice, the
     criterion it ranks, tunes or selects models by. Cases: forest_fires (MAD and RMSE, ranked by MAD: kept).

   **Lennart (2026-11-05, change):** Option A: File the fact.

   **Resolved (2026-11-05, Lennart):** A. A MET-5 Cases row: the source tunes and cross-validates by RMSE on log1p on
   this cut (n = 75,929, RMSE 0.114), so `rmsle` is the source's criterion; unlike gallstone_disease and heart_disease,
   which list several criteria with none named as deciding.

9. **Rename the target to `log1p_organic_carbon_weight_percent`?**

   * **Problem:**
     - The column `organic_carbon_weight_percent` holds log1p values, 0 to 4.375 (0 to 78.45%), and a logged target
       is named after its transform[^clean16].
     - The blind reviewer, reading the data without our notes, concluded the values could not be weight percent, the
       misreading the rule guards against.
     - Four precedents kept the source's name, and a precedent that contradicts a rule is flagged rather than
       followed, so the mediator leaves this to you.
   * **Consistency:** Renamed: `log1p_meter_reading` (ashrae), `log1p_trip_duration` (nyc_taxi), `log1p_travel_time`
     (pkdd), `log_price` (house_sales). Names kept with a declared `target_transform`: `price` (diamonds, mercari),
     `loss` (allstate) and `area` (forest_fires), your cases of 2026-10-21.
   * **Effect on the task:** No score changes; a reader of the data takes log1p values for percent, as the blind
     reviewer did.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Rename | no value changes; the rebuild carries it | the name says the scale | none stated |
     | B | Keep name, amend rule | `target_transform` names the scale | matches the four kept cases | none stated |
     | C | Keep name, exception | an exception with its reason (critic's fallback) | none stated | none stated |
     | D | Source's name (implemented) | the name with `target_transform="log1p"` | none stated | nothing on file |

   * **Recommendation:** A (critic, advocate); the mediator leaves it to you because the precedents split.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, amend CLEAN-16 so that a declared `target_transform` names the scale; on C, file an
   `Exception to CLEAN-16` with its reason.

   [^clean16]: **CLEAN-16** (Should): log a skewed positive target when the source has not, case by case, and name the
     column after the transform (`log_days_to_death`).

   **Lennart (2026-11-05, change):** Option A: Rename.

   **Consistency check (AI, 2026-11-05):** renaming follows CLEAN-16 and ashrae, nyc_taxi, pkdd and house_sales, but
   differs from your keeps of 2026-10-21 (diamonds `price`, mercari, allstate `loss`, forest_fires `area`). What sets it
   apart?
   - (a) the name states a unit, weight percent, that the log1p values contradict (the blind reviewer misread it); the
     four state none: recorded as a CLEAN-16 case;
   - (b) keep the name;
   - (c) reopen the four;
   - (d) amend CLEAN-16.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, change):** Reply (a): the name states a unit, weight percent, that the log1p values contradict
   (the blind reviewer misread it); the… Option A: Rename.

   **Resolved (2026-11-05, Lennart):** A, with (a). The target is `log1p_organic_carbon_weight_percent` (values
   unchanged; as ashrae's `log1p_meter_reading`): the old name stated a unit, weight percent, that the log1p values
   contradict. A CLEAN-16 Cases row; the metric (`rmsle`) scores the same; `dataset check` clean.

10. **Confirm the amendment of the spectrum rule for the dropped 600 cm-1 bin?**

   * **Problem:**
     - 53 spectra read exactly 0 at 600 cm-1 beside a 602 cm-1 reading of 1.27 to 1.86, a fill, and your "do (b)" of
       2026-11-04 dropped the bin for every row, so each spectrum stays whole.
     - The rules keep the whole range the source publishes and set a fill missing while keeping the
       column[^clean26][^clean11].
     - You asked for this "going forward", but the remedy went only into `spectra.md`, which adds no rules of its own.
   * **Background:** A per-row encoding returns a spectrum with a missing value as missing. The bin is neither
     constant nor a copy (27,193 distinct values). The remedy in `spectra.md`: "an edge bin: drop it for every row;
     inner positions: set them missing". The record has no exception line and `cleaning_features.md` no cases row.
   * **Consistency:** Fills set missing with the column kept: `heart_disease`, `sdss_17`, `mortgage`[^clean11].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Amend the spectrum rule | the edge and inner remedy in the rule | you asked for it going forward | none |
     | B | Exception for this dataset | an exception line with the fact | none stated | none stated |
     | C | Nothing filed (implemented) | bin dropped, reason in notes | none stated | no exception or cases row |

   * **Recommendation:** A (critic, mediator), since you asked for it going forward. **Decision:** A or B?

   **Notes for the AI:** on A, amend CLEAN-26 in `cleaning_features.md` with the edge and inner remedy; on B, record
   an `Exception to CLEAN-26 (2026-11-04, Lennart)` with the fact and "Serves P6".

   [^clean26]: **CLEAN-26** (Should): a spectrum ships as the source publishes it, one numeric column per position on
     its axis, never processed in the data.
   [^clean11]: **CLEAN-11** (Should): impossible values become missing, and the row stays.

   **Lennart (2026-11-05, change):** Option A: Amend the spectrum rule.

   **Resolved (2026-11-05, Lennart):** A. CLEAN-26 is amended: a position holding a fill is set missing and the column
   stays; when only an edge position holds it, that position is dropped for every row, so each spectrum stays whole
   (narrows CLEAN-11). The facts checked on the export: 53 of 75,929 spectra read exactly 0 at 600 cm-1 beside 1.27-1.86
   at 602 cm-1. A Cases row; spectra.md cites the amendment.

11. **Keep `Timeless` without measuring whether the catalogue drifts?**

   * **Problem:**
     - The definition is tagged `Timeless` (2026-11-13) because the organic carbon of a sampled soil layer is a fixed property of the item[^tb-11].
     - `Timeless` also asks that the catalogue does not drift, and the record says the samples arrived over time and are dated, which nobody has measured here.
     - superconductivity, the same kind of catalogue, was measured and drifts in waves of families, so it carries no prototype tag[^sc-11].
   * **Background:** the split holds out whole pedons; the scan date is the dated order a forward split would use.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Timeless` (implemented) | the tag and its line stay as they are | no work; the target is a fixed property | the "does not drift" half rests on no measurement |
     | B | Measure, then decide | a forward split on the scan date against the grouped folds, as measured for the qsar sets: `Timeless` if it costs nothing, else no prototype tag with the measurement in the line | the tag rests on a measurement, as for the qsar sets and superconductivity | one Slurm run |

   * **Recommendation:** B. **Decision:** A or B?

   [^tb-11]: **SPLIT-32** (Should): `Timeless` holds when the target is a fixed property of the item, the same whenever it is measured, and the use case meets items drawn like the catalogue's; a catalogue that drifts goes on to the question whether the samples' arrival over time affects the target.
   [^sc-11]: superconductivity's `Time basis:` line: windows by first report year leave 23-51% of the test compositions an element-set sibling in training, against 79-86% when the same compositions are held out from all years.

**Review panel:** ship after changes (mediator). Tier full, second pass after your PR #33 review of 2026-11-04: twelve
reports (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent checker, advocate
and critic with one rebuttal each, mediator). Claims: 22; 14 hold, 5 refuted or partly refuted (the metric text, the
"1,701" count and the group description, all fixed in the definition; the prep report's row-order claim, wrong since
the shipped rows are shuffled; `rmsle` failing on extreme predictions, a framework matter), 3 untested (uniqueness
against the other libraries, the reproduction script, the then-missing REVIEW.md). Blind review: include with changes;
its main concern the target name, which hides the log1p (issue 9). Task gamer: no exploit; the best candidate,
format-only features of the spectra, made the honest baseline slightly worse (0.1756 against 0.1749). Agreed: no
exclusion, no leak, the grouped split, `rmsle` on log1p, the TP-3 keep, the notes on the group, on the shift to later
scans (8 to 26% worse, LightGBM only), on the 36 tilted spectra and on the layers above 58%. Disputed: whether MET-5
holds before its fact is filed (issue 8); the rename by default (issue 9); settled by the mediator: the shift note states
the error level only (EV-7), the encoding evidence is replaced on the declared scale (EV-1; done in the definition, open
in `spectra.md`), the TP-3 spread
leaves out the ungrouped Cubist, and the layers at 73 to 78% stay (they equal the source's measured total carbon).

<details><summary>Mediator</summary>

**Mediator ruling: `open_soil_spectral_library` (second pass, 2026-11-04)**

**Recommendation**

```text
Verdict: ship after changes (text, notes and filing; no row, split or metric change).
Validity: USE-3 holds; USE-6 framing (spectrum only) is a curator call, issue 6. USE-5 holds (fit approximate).
  LEAK-1, LEAK-10, LEAK-16 and CLEAN-23 hold (lag-1 0.0035; no attack beat 0.17490). SPLIT-1, SPLIT-23, SPLIT-24
  and SPLIT-29 hold; the description of the group is wrong (fix). The shift to later scans or new projects is not
  stated (SPLIT-31 note). PROV counts reproduce; C13 and the S/N source were not tested (EV-7).
Value: MET-3 holds (rmsle = RMSE of the shipped log1p values, 1.1676 both ways). MET-11 fails in the text (4 strings
  say percent). MET-5 holds by its text but departs from the forest_fires precedent, and the reason that sets this
  case apart is not on file (issue 8). TP-3 no_spread: keep pending tuned results (issue 7).
Quality: CLEAN-16 rule against precedents (issue 9). CLEAN-26 edge-bin drop not filed (issue 10). CLEAN-11: the >58% OC
  rows stay with a note (measured, below). The 36 tilted spectra stay with a note.
Weighed: size +, source +, use case +, saturation (R² 0.98) -, instrument and date transfer untested -.
For the curator: issues 6-10.
```

**How the disputed points were settled**

1. **Wording of the shift note.** The advocate wins under EV-7 (Must), which bars claiming a check nobody ran. Only LightGBM was run under the alternative splits, so the note states how much the error rises, not that rankings change.
2. **Description of the group.** Both sides adopted the split auditor's wording, so this is no longer disputed.
3. **C5 and the `spectra.md` table.** The critic wins under EV-1. On the declared scale the PLS and Ridge conclusions reverse, so a "percent-scale" label alone leaves wrong findings standing. The default encoding does not change, because CLEAN-26 sets it from the field's published default, not from our folds.
4. **Whether MET-5 holds.** The critic wins. MET-5's text is met, since the source tunes by RMSE on log1p. But `forest_fires` was decided on the criterion the paper ranks by, and the fact that sets this case apart is not filed (principles, consistency case 2).
5. **The TP-3 spread.** The critic wins under EV-1. Take the spread from one run with stated settings, and leave out Cubist 0.114: it comes from an ungrouped CV, a different regime.
6. **Target values above 58% OC.** The advocate wins. I ran the decisive check on the raw L0 and L1 tables:
   * The 3 rows at 73.4–78.45% equal the source's own measured total carbon (`c.tot_usda.a622`: 78.45214, 75.21588, 73.42797).
   * CaCO3 was not measured for them, so OC equals total C.
   * The source's L0 `oc_usda.c1059` carries the same values. We reproduce the source exactly; this is not a derivation error.
   * CLEAN-11 says "values that are only unusual stay". Implausible for litter is not the same as shown to be impossible.
   * The remedy is a note. What would reopen it is a later KSSL release that revises these samples; that would be a repair from the origin (P5).
7. **The rename (CLEAN-16).** By rank the rule beats precedent, so renaming is the default. But four of Lennart's 2026-10-21 cases keep the source name together with `target_transform` (`diamonds` and `mercari` keep `price`, `allstate` keeps `loss`, `forest_fires` keeps `area`). A precedent that contradicts a rule is flagged, not followed, so this goes to the curator (issue 9).

**Changes to make now (no decision needed)**

1. **MET-11.** Rewrite T4, C10, the last sentence of C11 and the reason of the `_decisions` "Reference scale" entry to say "RMSE on log1p (`rmsle` on weight percent), the source's CV and tuning scale".
2. **EV-1.** In C5, mark the percent numbers as fitted and scored in percent, and drop or explain the 1.85 that does not reproduce. Add the declared-scale table from the 2026-11-04 encoding run (log1p fit, `rmse_log1p`, the three folds of repeat 0; folds won in parentheses):
   * LightGBM: 0.155 as is / 0.130 ALS+SNV (3/3) / 0.136 SNV (3/3) / 0.118 SG d1 (3/3)
   * PLS 30: 0.158 / 0.164 (0/3) / 0.145 (3/3) / 0.150 (3/3)
   * Ridge: 0.142 / 0.146 (0/3) / 0.138 (2/3) / 0.144 (0/3)

   Make the same change to the `spectra.md` table and its sentence "PLS gains... ridge reads best as is". Mark C15's numbers as percent-scale, measured before the edge bin was dropped.
3. **SPLIT-24 (description).** In `Grouping.definition`, `task_summary.split` and C9, use: "a pedon key, usually one profile; archive campaigns and research projects share a key (the largest has 640 rows); replicate pits at one site have separate keys (348 locations; grouping by location gives about 0.150 against 0.148 RMSLE)". Drop "bulk standards", which key 10520's SD of 0.517 refutes.
4. **SPLIT-31 / USE-9.** Add to `fit_reason` and `splits_comment`: "93–96% of test rows have their project in training; a model applied to later scans or new projects scores about 8–26% worse in RMSLE (LightGBM, 2026-11-04); whether rankings change is untested." List a project or scan-date split as a candidate variant, not to build now.
5. **writing.md.** Change "1,701" to 1,700 in C15, in the Spectrum description (`dataset.py` line 93) and at `spectra.md` line 113.
6. **PROV-8.** Cite C11's 0.114 / 0.995 / n = 75,929 to `ossl-models/out/fitted_models_performance_v1.2.csv`. The PLOS S2 Table has 2 decimals and no n.
7. **CLEAN-11 and CLEAN-26 notes.**
   * 151 rows are above 58% OC (3 above 70%, RaCA MO14, XN preparation, O horizons). They are the source's measured total C, kept unclipped.
   * 36 spectra have a tilted baseline (negative mean absorbance). They are kept, because dropping them hurt an honest model by 0.0005 to 0.006 per split.
8. **EV-7.** Mark C13 (uniqueness against other libraries) and the S-before-N reference source as not tested.
9. **Record.**
   * Add a new Assessment that supersedes "no panel ran".
   * Add an AI note that CC5's "REVIEW.md issues 2-3" points to a file that does not exist. Leave the CC line itself unedited.
   * Tell Myunghwan before shipping: he holds the claim, and target, metric and bins have changed since his "ship all".
   * The container from 2026-10-29 is stale. Rebuild only when the curator asks.

**Issues for the curator, ranked**

**Issue 6. Spectrum-only inputs (P3, USE-6 Must; a framing call).**
* Problem: a KSSL lab always knows the layer's depths and the preparation code. Adding them lowers `rmsle` by 3.6% (0.1428 to 0.1376 and 0.1446 to 0.1393, two folds).
* For spectrum-only: the source's scan-upload service (OSSL Engine) takes only the spectrum (C1).
* Against: USE-6, "anything known at the prediction point is a legitimate input".
* Decision: keep the OSSL Engine actor and say in `known` that this was a choice of actor (recommended), or reframe as the KSSL in-house lab and add the depths and preparation code.

**Issue 8. MET-5 consistency (P6, Should).**
* Problem: `rmsle` on log1p (CC6) is the source's tuning criterion. `forest_fires` instead used the criterion its paper ranks by, and the fallback cases used `rmse`. The paper here ranks model types by CCC with RPIQ.
* Fact that sets this case apart: the source's 10-fold CV on log1p was run on exactly this cut (n = 75,929, RMSE 0.114), with the same lab and instrument our split keeps. Its percent-scale results come from the instrument transfer, which this task does not test.
* Supporting evidence: `rmsle` puts 54–75% of the weight on layers at or below 3% OC, while percent RMSE puts 78–87% of the squared error on layers above 12%. Each scale picks a different model on 3 of 3 folds.
* Decision: (a) file that fact as an exception, a MET-5 Cases row (recommended); (b) the fallback `rmse` in percent; (c) reopen `forest_fires`; (d) amend MET-5.

**Issue 7. TP-3 `no_spread` disposition (P6, Must).**
* Probe skill: linear 0.985, LightGBM 0.980, random forest 0.978.
* On the declared scale, untuned methods spread from 0.118 to 0.158 (one run).
* Decision: record "keep pending tuned results" with those numbers, like `open_university_learning_analytics_dataset`.

**Issue 9. Target name (P7, CLEAN-16 Should).**
* Problem: `organic_carbon_weight_percent` holds values from 0 to 4.375. The blind reviewer, reading cold, concluded the values were not percent at all.
* Decision: (a) rename to `log1p_organic_carbon_weight_percent` (the rule; `ashrae` did this); or (b) keep the name and amend CLEAN-16 so that a declared `target_transform` names the scale, which would match `diamonds`, `mercari`, `allstate` and `forest_fires`.

**Issue 10. Filing the edge-bin drop (P7, CLEAN-26 Should).**
* Problem: 53 spectra hold an exact 0 at 600 cm-1, a fill. Your "do (b)" dropped the bin for every row, but the remedy lives only in `spectra.md`, which adds no rules of its own.
* Decision: amend CLEAN-26 in `cleaning_features.md` (fits "going forward"), or file `Exception to CLEAN-26`.

**Agreed facts**

* Rows: 86,603 raw, 76,813 with a scan, 75,929 shipped. 20,626 pedon keys and 62 zero targets.
* Inputs: 1,700 bins from 602 to 4,000 cm-1. `pedon_id` is not a feature.
* Rows are shuffled (lag-1 0.0035). No key crosses a split. 0% exact copies, and near copies occur at chance rates.
* Grouped/IID gap: 0.1482 against 0.1424. Grouping by location gives about 0.150; a project split gives 0.1634.
* Later scans cost +8–11% (split auditor) to +26% (practitioner's control). Both used LightGBM only.
* Each layer has one scan: 55,886 XS and 20,043 XN, none scanned in both preparations.
* Largest key: 39678, an archive campaign, 640 rows.
* `rmsle` raises an error only for extreme predictions (−40, +800 or NaN on the log1p scale).
* My check: OC exceeds total C by more than 0.1 in 17 of 85,669 source rows. This is not chased further.

**Consistency with precedent**

* The register has 0 flags.
* Shipping the target as log1p follows `mercari_price_suggestion` and `forest_fires`.
* The declared spectrum and `state="raw"` follow `pancreatic_cancer_mouse_detection`.
* Keeping the 36 tilted spectra and the >58% OC rows follows the tension row "a real task against imperfect cleaning" (`churn_telco_south_asia`).
* Three departures need the curator: MET-5 against `forest_fires` (issue 8), CLEAN-16 against four precedents (issue 9), and CLEAN-26 not filed (issue 10).

</details>

<details><summary>Claim audit</summary>

**Claim audit: `open_soil_spectral_library`** (claim-auditor, second pass, 2026-11-04)

**Answer to the focus question.** The declared metric is the one Lennart meant, and the text that contradicts it is stale. CC6 (2026-11-04) chose "`rmsle` on the log1p target". The spec and the scorer compute exactly that: the RMSE of the shipped log1p values. On all 9 folds, a train-mean prediction scores `rmsle` 1.1676, the same as the RMSE on the log scale (1.1676), while the RMSE in percent is 14.78. Four texts still say percent: T4 ("is scored in weight percent"), C10 ("score RMSE in weight percent after the inverse"), the last sentence of C11 ("The declared RMSE in percent") and the reason in the `_decisions` "Reference scale" entry, which goes into the README and the container. All four come from CC5, when the metric was still open. The 1,700/1,701 tension: 1,700 is right and every "1,701" is stale. On the C5 numbers: the encoding ranking holds on the declared metric (test below), but the C5 levels are on the percent scale.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | `rmsle` with `target_transform="log1p"` is the RMSE of the shipped values | spec `definition`, C2 | ran `metrics.score(spec, …)` with a constant prediction on 9 folds | holds | `rmsle` equals the log RMSE on every fold (1.144–1.169) | MET-3, MET-11 |
| 2 | "scored in weight percent" / "declared RMSE in percent" | T4, C10, C11, `_decisions` reason | same as #1 | **refuted** | log scale, not percent (1.17 vs 14.8) | MET-11, writing.md |
| 3 | Source tunes by RMSE (inner 5-fold, about 2,000 samples), uses log1p for all but clay/silt/sand/2 pH, back-transforms with expm1 at the end, ranks by CCC with RPIQ 2 (Fig 5) | C11, spec `original` | read the PLOS paper | holds | quotes match; the paper does not say the CV was grouped | MET-1, MET-5 |
| 4 | Source CV on log1p: KSSL MIR OC n = 75,929, RMSE 0.114, CCC 0.995 | C11 | supplement s002 and `ossl-models/out/fitted_models_performance_v1.2.csv` | holds, citation imprecise | s002 notes "reported in the natural logarithm space" but gives 0.11 / 0.99 to 2 dp and no n. The 3-dp numbers and n = 75,929 (`unit_transform` log1p) are in the GitHub CSV. Our row count equals the source's n | PROV-8, EV |
| 5 | The metric is computable on every fold | implied (MET-2) | scored dummy and mean predictions; counted units per fold | holds | test groups 6,875–6,876, test rows 24,870–25,969, 0 group overlap, dummy `rmsle` 1.62–1.65, no scoring columns needed | MET-2 |
| 6 | Predictions anywhere on the log scale score | prep ("no domain failure") | edge predictions | **partly refuted** | −1 and −5 score; −40, +800 and NaN raise ValueError, because expm1 reaches −1.0 or overflows. This is a framework-wide edge case and unlikely in practice | MET-2 |
| 7 | 1,700 bins, 602–4,000 cm-1; `pedon_id` not a feature | T5, C1 | `feature_cols` | holds | 1,700 columns `mir_602`..`mir_4000`; `pedon_id` is excluded | USE-3 |
| 8 | "All 1,701 measured predictors remain"; "1,701 positions" | C15, Spectrum description; also spectra.md line 113 | same | **refuted** (stale) | 1,700 ship | writing.md |
| 9 | 600 cm-1 fill: 53 spectra, 602 value 1.27–1.86, 50 from 2011, 42 on two days, 32 other zeros above 2,000, 27,193 distinct values, range 23k–55k | C4 | memory-mapped raw bins | holds | 53; 1.265–1.863; 50 in 2011; 27 + 15 on two days; 32 zeros, the lowest at 2,176; 27,193; 22,669–54,385 | PROV-13 |
| 10 | 86,603 / 76,813 / 75,929 rows, 20,626 keys, 62 zeros, target within 0–100 | A2, `_decisions` | definition frame | holds | all counts match; maximum 78.45 % | — |
| 11 | XS 55,855 + 31 N fallback, XN 20,043 | C14 | `id.scan_local_c` suffixes | totals hold; S/N reference source untested | 55,886 XS, 20,043 XN, no sample number scanned twice | — |
| 12 | Encodings: LightGBM gains from SNV and from the SG first derivative on every fold; fitted on log1p and scored in percent, LightGBM as is gives 1.85 | C5, A9 | LightGBM defaults (n_jobs 4), fitted on log1p, 3 folds of repeat 0 | direction holds; level not reproduced | `rmsle`: as is 0.174, SNV 0.148, SG1 0.126, lower on 3 of 3 folds. In percent: 2.14 / 1.67 / 1.44, not 1.85 (settings unstated) | EV-1 |
| 13 | Layers above 12 % OC are 16 % of rows | C5 | count | holds | 15.6 % | — |
| 14 | The shipped frame keeps the raw order (lag-1 0.735), a candidate exploit | prep, focus | lag-1 in the definition frame (= kit `data.parquet`); nearest training row by position as the prediction | **refuted** | lag-1 0.004; neighbour `rmsle` 1.63, worse than the train mean (1.16). No exploit | LEAK-13 |
| 15 | No row is a copy across the split | implied | probe 5 (exact); same point and upper depth in another pedon in training (r0f0) | holds | 0 % exact copies; 621 of 24,870 test rows have a same-site match, and copying its label gives 0.368 vs LightGBM 0.174. No shortcut | LEAK-16, SPLIT-29 |
| 16 | A group is "one sampled soil profile whose layers are the rows"; "a few large keys" | T2, T6, C9, Grouping | key composition | **partly refuted** | key 39678 has 640 rows over 151 upper depths (North Dakota archive campaign). 190 keys exceed 10 rows. 1,779 keys (10,689 rows, 14 %) repeat an upper depth. The grouped/IID gap is 0.001, so the impact is small | SPLIT, USE-10 |
| 17 | Every feature is known at the prediction point | implied | features are spectra only | holds | no chemistry, IDs or coordinates | LEAK-1, LEAK-10 |
| 18 | Target is the real-world target | T4, C7 | — | holds as disclosed | an analytical estimate from total C. The S-before-N coalescence is untested: the local L0 export has one OC column | USE-5 |
| 19 | No exact full-grid copies against 8,871 other-library spectra | C13 | — | untested | needs the non-KSSL rows of `ossl_mir_L0` (.qs); no Rscript is installed | PROV-4 |
| 20 | The `download_description` script recreates the raw inputs | metadata | — | untested | needs network and R 4.3 | PROV |
| 21 | CC5's "REVIEW.md issues 2-3" | record | `ls` | untested / dangling | no REVIEW.md on disk | EV-7 |
| 22 | Metric as source origin (MET-5) | spec | the paper | holds, with a caveat | RMSE on log1p is the tuning criterion, which makes it a deliberate choice. CCC ranks the model types, a second candidate the curator set aside in CC6 | MET-5, MET-10 |

**Refuted and partly refuted claims, ranked (validity first, Must first)**

1. **Metric text says percent; the metric is log1p (#2).** Rules: MET-11 (Must), notes must match the code. The score itself is right. The problem is a reader who compares a percent RMSE with the shipped scores (about 2.1 vs 0.17) and misreads the task by a factor of about 12. Mildest fix, text only:
   - T4: "…and is scored by RMSLE on weight percent, the RMSE of the shipped log1p values."
   - C10: drop "score RMSE in weight percent after the inverse".
   - C11, last sentence: "The declared RMSLE is on the scale of the source's CV and tuning; its independent evaluation reports RMSE in original units."
   - `_decisions` "Reference scale" reason: the same wording as C10.
2. **Group described as one profile (#16).** Rules: P4 (split validity) and the description. 14 % of rows sit in keys that repeat a depth, and the largest key is a campaign, not a profile. The measured consequence is small (gap 0.001, no same-site shortcut). Fix: change "a few large keys" to "most keys are one profile; 1,779 keys (14 % of rows) repeat a depth and the largest (640 rows) is an archive campaign".
3. **"1,701" survives in C15, the Spectrum description and spectra.md line 113 (#8).** Rule: writing.md. Fix: "1,700 ship (602–4,000 cm-1); the 600 cm-1 fill bin is dropped". Mark C15's numbers as measured before the drop and on the percent scale.
4. **C5 levels are on the percent scale and the 1.85 does not reproduce (#12).** Rule: EV-1. The direction holds on the declared metric. Fix: add the declared-scale line (LightGBM `rmsle` 0.174 / 0.148 / 0.126, as is / SNV / SG1, 3 of 3 folds) and state the LightGBM settings. Separately, SG1 is 28 % lower than the recommended `spectrum-as-is-r1`. That is a spectra.md benchmark question ("one dataset is a case"), not a definition defect.
5. **C11 cites "S2 Table" for 0.114 / 0.995 / n (#4).** Rule: PROV-8. Fix: cite `soilspectroscopy/ossl-models/out/fitted_models_performance_v1.2.csv`; the PLOS supplement has 2 dp and no n.
6. **Prep's row-order exploit (#14).** This is not a definition claim. The task gamer can drop it: lag-1 is 0.004 in the shipped order.
7. **Domain edge of `rmsle` with log1p (#6).** A framework matter, not this dataset's. An optional remedy is to clip or guard predictions in the metric code.

**Untested, ranked:** C13 uniqueness against the other libraries (#19, needs R and qs); the S-before-N reference source in C7/C14 (#18, the archived S/N columns are not in the local export); the reproducibility script (#20); the dangling REVIEW.md reference (#21). The group permutation test is still unfinished from the prep.

</details>

<details><summary>Column audit</summary>

**Focus answer.** `focus.md` asks the column auditor nothing specific ("none beyond the standard panel"). The direct answer to the standard audit is that no column of the shipped frame is a leak. Every model input is one of the 1,700 MIR absorbance bins, and every bin exists before the laboratory reference. The other two columns are the target and the group key `pedon_id`, which is excluded from the model inputs (`feature_cols` = 1,700; `pedon_id` not among them). The dtype probe flags 0 of 1,700 columns.

One correction to the prep report. It says "the shipped frame keeps that order", and that is wrong. The definition frame is shuffled, and so are both the participant kit's and the clean room's data: lag-1 autocorrelation of the target is 0.0035 (the raw order gives 0.735), Spearman with row position is 0.002, and only 0.02% of adjacent rows share a pedon. CLEAN-23 holds, and the task gamer has no row-order exploit.

**Column table**

The frame I rebuilt with `dataset_io.from_definition` has 75,929 rows and 1,702 columns: 1,701 float64 and 1 category. The built container dates from 2026-10-29 and is stale.

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `mir_602` … `mir_4000` (1,700 bins, every 2 cm-1) | KSSL absorbance of the ground (<80 mesh) sample, from the Bruker Vertex 70 with HTS-XT, replicates averaged, 5 decimals (C3) | Yes. The scan exists before any new reference (C1). | float64, finite, none missing, none constant, no identical adjacent bins, no duplicate spectra; 22,669 to 54,385 distinct values per bin; all values at 5 decimals; declared `Spectrum(state="raw")`, untransformed | fine | CLEAN-26, CLEAN-5, CLEAN-9 |
| (same block) 32 exact zeros | sign changes of near-zero absorbance; `mir_3994` and `mir_4000` hold one each | yes | real readings, not fills; no edge bin is a fill anymore (0 zeros in `mir_602`..`mir_610`) | fine | spectra.md pitfall |
| (same block) negative values | 159,653 negative cells in 746 rows: 455 rows have at least 100 negative bins, 42 rows at least 850 (half the spectrum or more). 75% of the negative cells lie above 2,500 cm-1. | yes | 36 spectra have a negative mean absorbance (row mean down to -0.39), sloping from about 0.3-0.4 at 602 cm-1 to between -0.5 and -0.97 at 3,998 cm-1. Median OC in these rows is 0.93%, against 1.19% overall, so they are not organic soils. This looks like a tilted or mis-referenced baseline, not a soil's absorbance. | question for the curator (keep with a note) | CLEAN-11, CLEAN-1 against CLEAN-26 |
| (same block) flat runs | 3 rows with 52 to 113 equal adjacent values, all with OC 45-49%, absorbance range 0.66-1.19 | yes | 5-decimal quantisation of the low-contrast spectra of organic soils, not a fill | fine | |
| (same block) saturation | 1 row reads above 3 between 602 and 674 cm-1 (max 3.61, OC 9.6%) | yes | a single high-absorbance edge, plausible | fine | |
| `mir_600` (dropped) | 600 cm-1 edge, a fill (exact 0) in 53 spectra | yes | dropped for every row, by the curator's call ("do (b)", 2026-11-04). This matches the spectra.md edge-fill pattern. `mir_602` carries nearly the same signal (raw probe 20: 0.104 against 0.108). | fine | CLEAN-26, spectra.md |
| `pedon_id` | KSSL `lims.pedon.id`, exported as `id.dataset.site_ascii_txt`. A sampled profile, but some large keys hold archive campaigns or bulk standards: the largest has 640 rows, then 210 and 112 | not an input; it is the group | category with 20,626 levels, all numeric strings, none empty. Declared categorical in `_feature_types` and dropped from features by the grouping. Spearman of the numeric key with the target is 0.05, irrelevant since the key is not a feature. | fine (whether one key is one physical profile is the split auditor's question) | CLEAN-3, CLEAN-9 |
| `organic_carbon_weight_percent` (target) | OC estimated analytically from total C; the S-preparation reference comes first, the N preparation fills in (C7, C14) | n/a | float64, log1p of weight percent: range 0 to 4.375 (0 to 78.45%), 62 zeros, none negative or above 100 before the log; expm1 round-trips with error 0.0. Rows without a spectrum (9,790) or a label (884) dropped. The name says weight percent but the values are log1p, and the text says the score is in percent while the metric is on log1p. | cleaning problem, and the text contradicts the metric | CLEAN-16, CLEAN-15, MET-3 |

**Problems, ranked by `principles.md`**

No problem ranks P1 to P5. No column breaks LEAK or USE.
- **No post-outcome input.** The only inputs are the spectra. C1 records that other chemistry, carbon equivalents and field metadata are left out (USE-3, LEAK-10).
- **Missingness from the outcome is weak.** The upstream importer had already set negative references to missing before the data reached us (C7). That removes a few calcareous layers with near-zero OC, the pre-import count cannot be recovered, and it is disclosed. Of the 10,674 dropped raw rows, the labelled ones have a lower median target (0.79% against 1.19%), but almost all of them are dropped for lacking a spectrum, which is not caused by the outcome.
- **No identifier encodes the label.** The only identifier is the group key, which is not a feature.
- **Depth and site fields are left out on purpose.** They would be known at the lab, but the source's scan-upload models are spectrum-only (C1).

**1. P6 / MET-3: the text says one score, the metric computes another (text fix, Should).**
- I ran the shipped metric with `score(ds.metric, …)` on toy data. With `target_transform="log1p"` and `rmsle`, it equals the RMSE of the shipped values on every case: 0.00846 and 0.00846; 0.02952 and 0.02952; 0.86605 and 0.86605. A negative log1p prediction is accepted (sklearn 1.7.2), so a linear model with clipped-free output does not crash.
- So the score is RMSE on log1p, as C2 and CC6 (2026-11-04) say.
- Four places still say it is in weight percent: `task_summary.predicted` ("is scored in weight percent"), C10 ("score RMSE in weight percent after the inverse"), C11 ("The declared RMSE in percent…"), and the "Reference scale" Decision text ("RMSE is scored in weight percent after the inverse").
- C5's numbers are percent-scale RMSE, measured before the metric moved to log scale. They are fine as history, but should be labelled so.
- Remedy (mildest): change those four strings to "RMSE on log1p (the source's CV scale)". No data change.

**2. P7 / CLEAN-16: the target name does not say log1p (Should, cheap).**
- `organic_carbon_weight_percent` holds log1p values.
- CLEAN-16 says to name a transformed target after its transform. The precedents disagree:
  - renamed: `log1p_meter_reading` (ashrae), `log1p_travel_time` (pkdd), `log1p_trip_duration` (nyc_taxi), `log_price` (house_sales), `log_delivery_days` (brazilian_ecommerce)
  - not renamed: `price` (diamonds, mercari), `loss` (allstate), `area` (forest_fires)
- Remedy: rename to `log1p_organic_carbon_weight_percent`. Otherwise keep the name and note it as a departure. That is a consistency question for the curator, because the precedents split.

**3. P7 / CLEAN-11 against CLEAN-26: 36 spectra (0.05%) with negative mean absorbance (question for the curator).**
- The evidence is in the table above. A finely ground soil reads 0.18 to 1.53 mean absorbance in 99.8% of rows; these 36 slope steadily to -0.97 at the high-wavenumber end, in 21 pedons.
- CLEAN-26 says to ship the spectrum as published, and the baseline encodings (`vib-als-snv-r1`, `vib-sg11-d1-r1`) remove a linear tilt. Setting values missing (CLEAN-11) would break whole spectra, against the spectra.md pattern that keeps each spectrum whole.
- Remedy (mildest): keep the rows and add one sentence to C4 or C3 naming the 36 baseline-tilted scans. Before deciding, the curator may want to check their scan dates in the warehouse, as was done for the 600 cm-1 fill.

**4. P7 / writing: stale bin counts (text only).**
- C15 ends "All 1,701 measured predictors remain". 1,700 ship.
- C1 and T5 say 1,700. The `Spectrum` description says 1,701 published with the edge dropped, which is consistent.
- Remedy: change C15 to "All 1,700 retained predictors remain (the 600 cm-1 fill bin dropped)".

**Not a problem:**
- Row order (CLEAN-23 holds, measured above).
- Dropping `mir_600`: the curator decided it, it matches the spectra.md edge-fill pattern, and the ranks of the other bins are unchanged.
- The dtypes (0 flags).
- The 82 raw rows that are copies of one another: none survive in the shipped frame, which has 0 duplicate spectra and 0.0% exact copies across splits in the leak probe.

**Judgment record (columns only).** Validity: USE-3 and LEAK-10 hold; CLEAN-23 holds. Value: MET-3 text contradicts the declared metric (problem 1). Quality: CLEAN-16 departure (problem 2), and a CLEAN-11/CLEAN-26 weighing call on 36 tilted spectra (problem 3). Ship after the text fixes.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** Holding out whole KSSL pedon keys fits the use case: a laboratory predicts organic carbon for layers from a profile it has never seen, on the same instrument. The key is a native id, and no near copies cross the split. What the split does not test is a shift to later scans or to new survey projects, and that is worth about 10% in RMSLE. The notes should say this. The split itself needs no change.

**Focus question** ("the grouping key: 20,626 pedon keys, a few hold archive campaigns or bulk standards; the grouped/IID gap is 0.001"): the key is the right group, and the small gap does not argue for IID.
- **The gap is real but small.** Under IID, RMSLE is 0.1424 against 0.1482 for the shipped split, about 4% lower. R² is 0.9848 against 0.9835, which matches the probe's 0.001. Under SPLIT-4 the size of the gap never decides. In deployment every profile is new, so the split stays grouped (USE-10, SPLIT-1).
- **The large keys only make the split stricter.** Only 9 keys hold more than 50 rows (1,314 rows in all).
  - The largest, 39678, is the archive campaign "Archive MIR Scanning – North Dakota MLRA54": 640 rows (0.84% of the data), 151 distinct depths, 2 locations. It sits in one fold.
  - Calling some of them "bulk standards" is not supported. Key 10520 ("Additional Data") has 210 rows at one depth and one location, but its log1p target has SD 0.517. One reference soil would be close to constant. Keys 6273 and 28853 look the same and are research projects (Rio Grande P Study, Lake Tahoe Runoff).

**Facts measured.** Loaded through `dataset_io.from_definition(raw=True, encode_special=False)`. Model: LightGBM, untuned (600 trees), on the raw spectrum using every 4th bin (425 of the 1,700). Repeat 0, 3 folds. RMSLE is the RMSE on the shipped log1p target.
- **Shipped folds:** 24,870 to 25,969 test rows per fold. No pedon key is on both sides in any of the 9 folds.
- **One scan per layer:** each of the 75,929 rows has its own lab sample number (55,886 XS and 20,043 XN preparations). No layer is scanned in both preparations, so there are no preparation copies across the split.

| Split (3 folds) | RMSLE (mean ± sd) | R² |
|---|---|---|
| Shipped, by pedon key | 0.1482 ± 0.0056 | 0.9835 |
| IID (random) | 0.1424 ± 0.0018 | 0.9848 |
| By location: plus code where present (50% of rows), else pedon key; 19,664 groups | 0.1429 / 0.1585 / 0.1474 (≈0.150) | – |
| By project (`id.project_ascii_txt`, 1,548 projects) | 0.1634 ± 0.0105 | 0.9797 |

**Scan-date check.** Training rows are older scans whose pedons have no later scan. The comparison holds out half of the later pedons and trains on rows of any date, at the same training size, scored on the same test rows.

| Cutoff | Older scans only | Rows of any date, same size |
|---|---|---|
| 2017 | 0.1599 | 0.1443 |
| 2018 | 0.1829 | 0.1694 |
| 2019 | 0.1944 | 0.1767 |

**Problems, ranked by principles.md**

1. **The scan-date and project shift is untested and unstated (P4; SPLIT-1, SPLIT-31; USE-9 fit approximate).**
   - Evidence: the shipped split leaves 93–96% of test rows with their project present in training. Training only on older scans costs 0.014–0.018 RMSLE (+8–11%). A project split costs +0.015 (+10%).
   - The two are partly one effect. Scan years follow the project mix: archive rescans happened in 2011 and 2019, and the observation year differs from the scan year. 10,044 rows have no scan date (32% of XN, 7% of XS).
   - A temporal split would therefore measure a change of cohort rather than instrument drift, and it would lose 13% of the rows. It is not a fix.
   - The use case is still a new profile on the same instrument, and the definition already marks the fit approximate.
   - Mildest remedy: notes only. Add one sentence to `splits_comment` (and `fit_reason`): under the shipped split 93–96% of test rows have their project in training, and the score is optimistic by about 10% RMSLE for a calibration applied to new projects or later scans. List a project or scan-date split as a candidate variant (SPLIT-31), not to build now.

2. **One key is not always one profile, and one site can hold several keys (SPLIT-24, SPLIT-26: should, met).**
   - Evidence: 348 locations hold 2 to 77 pedon keys (4,321 rows). These are DSP replicate pits and 5-year revisits, plus RaCA sites with 5 pedons (105 locations hold exactly 5).
   - RaCA covers 16,727 rows, but only 6.4% of them carry a location, so their sites cannot be recovered. Ids of same-site pedons are consecutive in only 58% of sites, so a block of ids is a guess. SPLIT-24 bars grouping on a guess.
   - The cost is measured as negligible: the location-grouped split scores about 0.150 against 0.148.
   - The same-location, same-depth pairs across the split (2,672 pairs, 688 test rows) are different samples, not copies. Their median spectral distance is 4.18 against 1.76 for the nearest layer within a profile, and the median target difference is 0.218.
   - Remedy: none needed for the split. The definition and `task_summary.split` call the key "a sampled soil profile", while Myunghwan's 2026-10-27 line in the record calls it a "measurement batch". Wording only: "a pedon key, usually one profile; archive campaigns and research projects share a key, and replicate pits at one site have separate keys (location grouping measured: about 0.150 vs 0.148 RMSLE)". Also replace "bulk standards" with "research plots" unless someone can show a reference soil.

3. **No near copies across the split (SPLIT-29, SPLIT-30: pass).**
   - On fold 0 of repeat 0, 1.24% of test rows have a training neighbour closer than the 1st percentile of within-profile neighbour distance (about 1% expected).
   - 5.0% are closer than the 5th percentile (5% expected). Distances were measured on the first 30 principal components of the SNV-normalised spectrum.
   - The leak probe already found 0% exact copies.
   - No remedy.

4. **What one prediction is (SPLIT-23: pass).** `prediction_unit="row"`, `context="none"`, labels per sample. This matches the source's service: one uploaded scan in, one estimate out, and no reference value of the profile is known when it is scanned. No aggregation.

5. **The group probe's permutation test never finished (SPLIT-27: not needed).** SPLIT-27 guards a small grouped task against being called unlearnable. Here R² is 0.98 across groups. I mark it cannot-verify, not a concern (EV-7).

Temporal checks (gap, label delay, season windows) do not apply: there is no time column and the declared regime is grouped. I fitted no other model family under the alternative splits; the comparisons above are LightGBM only.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: `open_soil_spectral_library`**

I read this as two actors. One is a KSSL or NRCS soil-survey lab that scans a ground sample and wants its organic carbon without the wet chemistry. The other is a carbon-monitoring (MRV) lab using the OSSL models.

**Answer to focus.md (the metric text against the metric):** the declared metric is correct and the prose is wrong. `rmsle` with `target_transform="log1p"` is the RMSE of the shipped log1p values, which matches the metric `definition`, C2 and the record line CC6 (Lennart, 2026-11-04). Three passages still say the score is in weight percent, and they should be rewritten to say "RMSE on log1p (`rmsle` on the percent)":
- T4: "and is scored in weight percent".
- C10: "score RMSE in weight percent after the inverse".
- C11: "The declared RMSE in percent is on the independent evaluation's scale".

C5's encoding numbers are RMSE in percent. They need re-measuring in `rmsle` or a label saying they are not the benchmark score. This matters because the two metrics pick different models (point 1 under "Metric" below). The README's "scored on the original scale after the inverse of log1p" is literally true for `rmsle` but will be read as "RMSE in %". It is generated text, so the fix belongs in the prose.

**Fit: approximate** (agree with the declared `fit`). The rows, label, row unit and pedon holdout match a KSSL lab predicting a new sample. Two things are untested: the deployed instrument (NRCS field-office spectrometers, other labs on OSSL), and later scan dates. The second I measured below, and `fit_reason` does not name it.

**My five questions, in the first person**

1. **Inputs (USE-3, USE-6).** At scan time I have the spectrum, so the inputs are legitimate and nothing comes from after the lab result. The definition drops field metadata because the OSSL scan-upload service does not take it. But as a KSSL lab I always have the layer's depths and the prep code (XS/XN, the scan-id suffix) when the sample arrives. I measured them on repeat 0, folds 0 and 1:
   - Adding upper depth, lower depth and the prep code to an SNV + PCA80 LightGBM lowers `rmsle` by 3.6% on both folds: 0.1428 to 0.1376 and 0.1446 to 0.1393.
   - That is a small gain. Leaving them out is defensible given the OSSL Engine actor, but `known` should say it is a choice of actor.
2. **Target (USE-5).** KSSL's organic carbon (c729) is total carbon minus the carbonate carbon (from the CaCO3 measurement). It is the number KSSL reports and the one I act on, not a proxy. In calcareous soils it carries the CaCO3 error, which practitioners accept. A number is the right output. The OSSL Engine also returns a conformal interval and a Q-statistic flag for samples outside the library (PLOS paper). A point score cannot test those, which is a minor gap.
3. **One row = one decision.** Yes: one layer sample gives one prediction (`prediction_unit="row"`, `context="none"`). Holding out whole pedons fits how samples arrive, since a new profile's layers come together.
   - Whether the test data is what I would face: partly. KSSL predicts *later* scans, and the instrument ages and the mix of projects shifts. Scan dates are in the raw metadata (`scan.mir.date.begin`, missing for 10,044 rows, 13%).
   - I trained on scans up to 2017 (38,333 rows) and tested on 2018 to 2022 (26,765). For a fair control I held out random pedons among the dated rows, with the same training size. Same model as in point 1.
   - Result: `rmsle` 0.178 on the later scans against 0.141 for the control, **+26%**.
   - The error is higher in every OC band: ≤0.5% 0.129 vs 0.122; 0.5-1% 0.128 vs 0.118; 1-3% 0.185 vs 0.137; 3-12% 0.306 vs 0.197; >12% 0.163 vs 0.153.
   - At 3-12% OC the later scans are under-predicted more (log bias −0.081 vs −0.046), which looks like drift.
   - Caveat: the year is confounded with which projects KSSL ran that year.
4. **Would I use it?** Yes, for within-KSSL calibration, which is what NRCS does: regional calibrations from KSSL spectra applied to newly collected samples (NRCS MIR page).
   - I would trust it because the reference chemistry comes from the same lab and instrument, the holdout is by pedon, and there are 75,929 rows.
   - I would distrust a leaderboard gap smaller than the date shift above (about 0.035 `rmsle`) as evidence of what happens in deployment.
   - For an OSSL user on another instrument, the paper's independent evaluation is the honest number, and this task does not reproduce it.
5. **Metric: see below.**

**Gaps, ranked by how much they change the task**

1. **Instrument transfer (named in `fit_reason`).** Already declared. KSSL calibrations run on NRCS spectrometers in 21 soil-survey offices and 3 state or area offices (NRCS). The paper finds "external performance is highly dependent on the characteristics of the test spectra". This cannot be fixed inside KSSL-only data.
2. **Scan dates (not named).** Later scans are +26% `rmsle` against a matched grouped control. An expert would at least name this in `fit_reason` and `splits_comment`. The stronger option, for the curator, is a temporal or date-grouped regime. USE-10 and SPLIT-3 apply, but the year is missing for 13% of rows.
3. **Metric prose against the declared metric.** Covered in the focus answer. The prose fails MET-11's requirement to state what is scored, and C5 is measured on the wrong scale.
4. **Inputs a KSSL lab always has (USE-6).** Depth and prep code are worth −3.6% `rmsle`. Acceptable under the OSSL scan-upload actor, but name the choice.
5. **No interval or out-of-library flag scored.** Common to every regression task here. Note only.
6. **Minor provenance point.** The paper's text says "natural-log transformed", while the definition cites `log1p()` from the code. Probably the code is right. The claim auditor should confirm the S2 wording ("reported in the natural logarithm space") against the ossl-models code.

**Metric: does `rmsle` score the decision? **Yes**, once the prose is fixed**

- **MET-5.** The source tunes Cubist with RMSE on log1p and reports its 10-fold CV in log space. That is a deliberate choice, so `source` is the right origin.
- **MET-3.** `rmsle` with `target_transform="log1p"` is exactly the shipped scale.
- **MET-1 (my unit and my decision).** The OC distribution is very skewed: median 1.19%, 90th percentile 30.7%, 15.6% of rows above 12%, 71% at or below 3%.
  - RMSE in % is decided by the organic layers. On repeat 0, rows above 12% carry 78-87% of the squared error; rows at or below 3% carry 6-13%.
  - `rmsle` puts 54-75% of the weight on the ≤3% mineral soils. Those are where MRV and fertility decisions sit, and where a 0.1-0.3% change matters (Sanderman et al. 2021).
  - Organic layers have about 5-10x lower bulk density, so in a carbon *stock* (Mg C/ha) RMSE% over-weights them further.
- **The two metrics pick different models.** On all three folds of repeat 0, fitting on log1p wins `rmsle` (0.143/0.145/0.152 against 0.166/0.169/0.173). Fitting on the percent wins RMSE% (1.454/1.417/1.494 against 1.597/1.525/1.655). So the scale choice is decisive (MET-10), and log1p is the one I would pick models by.
- **What I would use:** `rmsle` as declared. Lin's CCC on log1p, the source's ranking criterion, is a reasonable report alongside it but not something to select by: it rewards agreement with the test fold's spread rather than error alone. RMSE in % would be my choice only for a peat-specific programme.

**What an expert would change**

1. Rewrite T4, C10 and C11 to say "RMSE on log1p (`rmsle`)", and re-run or relabel C5.
2. Add later scan dates to `fit_reason`, with the +26% figure. Optionally offer a date-based holdout for curator decision.
3. In `known`, say that depth and prep code are left out by choice of actor (−3.6% `rmsle` when added).
4. Keep `fit="approximate"`.

**Sources**

- [Safanelli et al. 2025, PLOS ONE e0296545](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0296545)
- [NRCS mid-infrared spectroscopy](https://www.nrcs.usda.gov/conservation-basics/natural-resource-concerns/soil/mid-infrared-spectroscopy)
- [Sanderman et al. 2021, Remote Sensing 13:2265](https://www.mdpi.com/2072-4292/13/12/2265/htm)
- [OSSL manual](https://docs.soilspectroscopy.org/)
- The definition, the record and the README, plus `use_case.md` and `metrics.md`.

The row order of the clean room's and the participant kit's data differs from what `_clean` returns: only 0.09% of target values match by position. That bears on the prep report's claim that "the shipped frame keeps that order" (probe 10), so the task gamer should check it.

</details>

<details><summary>Blind review</summary>

**Verdict:** include with changes. This is a real, well-used MIR soil-spectroscopy regression task with honest pedon-grouped splits, but the target is log1p-transformed while its name says weight percent, `pedon_id` must not be used as a feature, and the task is close to saturated (grouped R² of about 0.98).

**Concerns, most to least serious**

1. **The target is not what its name says.**
   - `organic_carbon_weight_percent` runs from 0 to 4.375, with a median of 0.784 and a 99th percentile of 4.00. Organic carbon in weight percent cannot look like that.
   - Under `expm1`, the values become plausible: median 1.19%, 90th percentile 30.7%, maximum 78.45%.
   - Once back-transformed, 65% of values sit exactly on a 0.01 grid. The stored values sit on it only 0.08% of the time.
   - This matches the source: OSSL models "natural-log transformed with log1p()" most properties, OC included. The column holds log1p(OC %).
   - Modelling on the log scale is a reasonable choice. But the name is wrong, and the metric scale (log RMSE versus % RMSE) changes which methods win.
   - **Change:** rename it to `log1p_organic_carbon_pct`, or store raw % and let the benchmark decide. State the transform in task.md.

2. **Physically impossible values.**
   - After back-transforming, 151 rows exceed 58% OC and the maximum is 78.45%. Pure organic matter is about 50–58% C.
   - The source defines the variable as "Estimated Organic Carbon based on Total C", so these are probably lab or derivation errors in very organic horizons.
   - 62 rows are exactly 0. These are plausible as OC estimates for calcareous samples, clipped at zero.
   - **Change:** drop or cap rows above about 60% OC, or at least document them. They are 0.2% of rows but sit at the extreme of a skewed target.

3. **`pedon_id` is in the feature table.**
   - It is a `category` column with 20,626 levels, and it is also the grouping variable.
   - Under a grouped split, every test pedon is unseen, so as a feature it is pure noise. It may also trigger high-cardinality handling, memory use or crashes in some methods.
   - **Change:** mark it as the group column only and exclude it from X.

4. **The task is near ceiling, so there is limited headroom.**
   - LightGBM on every 4th wavenumber, with 400 trees and no tuning, on a subsample of about 21.7k rows (6,000 pedons):
     - GroupKFold(3): R² 0.978, RMSE 0.171
     - random KFold: R² 0.980, RMSE 0.163
     - target std: 1.16
   - MIR prediction of SOC is a well-known, largely solved calibration problem.
   - Methods will still differ in RMSE, and spectral preprocessing (SNV, derivatives, PLS/Cubist, CNNs) matters, so the dataset still discriminates. It is just less informative than its size suggests.
   - **Change:** acceptable as is. It is worth noting in the benchmark that ranks will hinge on small RMSE differences, and the log versus raw scale (point 1) matters here.

5. **The grouping is plausible, but I could not fully check what it means.**
   - Rows per pedon: median 3, mean 3.7. One group has 640 rows, another 210, and another 112.
   - 640 layers in a single soil profile is not credible. That ID is probably a placeholder, a pooled site, or a whole small sub-library collapsed into one group.
   - Its spectra and target look like the rest (mean OC log1p 0.63), so this is not obviously harmful. It just forces about 0.8% of the data into one fold.
   - OSSL's own documentation has no explicit pedon field, only `site.pit_src_txt`, `id.location_olc_txt` and similar, so I cannot confirm where `pedon_id` came from.
   - The small gap between grouped and random CV (R² 0.978 vs 0.980) suggests leakage within pedons is modest either way.
   - **Change:** check what the large IDs are. If they are placeholders, split them, or group by location instead.

6. **Size and dimensionality.**
   - 75,929 rows × 1,700 float MIR columns (600–4000 cm⁻¹ at 2 cm⁻¹, matching the OSSL spec: "between 600 and 4000 cm-1, with an interval of 2 cm-1").
   - The columns are highly collinear absorbances. That is about 129M cells, heavy for some tabular methods (in-context learners, kNN, GPs).
   - The absorbance range (−0.97 to 3.61) is plausible against the OSSL note "usually between 0 and 3". There are no missing values, no duplicate rows and no duplicate spectra; the nearest-neighbour check found no near-exact pairs.
   - **Change:** keep the spectra declared as a spectral special feature. Optionally offer a subsampled or coarser-resolution version.

**Task realism and honesty (no concern)**
- The use is real. Soil labs such as USDA KSSL, along with carbon-monitoring and soil-survey programmes, predict OC from a cheap MIR scan of a dried, ground sample instead of running dry combustion or Walkley-Black.
- Every feature is measured on the same physical sample before the lab value exists, so nothing in X is unavailable at prediction time.
- Holding out whole pedons matches how the model is used: new profiles arrive, not new layers from known profiles.
- The data is real lab data from a CC-BY public library (OSSL v1.2, Zenodo; Safanelli et al. 2023, PLOS ONE), not generated.

**What I could not check**
- Which OSSL sub-libraries are included. 75,929 rows is below the OSSL total of 91,631 MIR scans, consistent with KSSL-only or KSSL-dominated data. Instrument or library mixing would matter for the split.
- Where `pedon_id` comes from and what the 640- and 210-row groups are.
- The PLOS S1 and S2 tables (OC summary stats and the published MIR OC CV metrics), which were not rendered, so I could not compare my R² against the published one.
- Whether repeat scans of the same physical sample were already averaged upstream.
- The full 3×3 split: I ran only one 3-fold grouped CV on a subsample with features thinned to every 4th wavenumber.

Sources: https://docs.soilspectroscopy.org/db-desc.html, https://zenodo.org/record/7599269, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0296545, https://github.com/soilspectroscopy/ossl-models

</details>

<details><summary>Task gamer</summary>

**Verdict:** I found no way to game this task. The only inputs are 1,700 raw MIR absorbance columns. The rows are shuffled, the split is properly grouped by pedon, and no exact or near copy crosses it. Every attack I built scored at or below the honest baseline (mean RMSLE 0.17490).

Honest baseline: untuned LightGBM on `features()`. It scores 0.1712, 0.1687, 0.1819, 0.1719, 0.1768, 0.1792, 0.1742, 0.1720 and 0.1781 on r0f0 to r2f2, mean **0.17490**. Predicting the training mean gives 1.157.

Noise check: adding a random column moves a split by at most ±0.0003 (mean 0.17490).

**Exploits ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| none | No attack beat the baseline | – | 0.17490 | – | – | – | – |

The closest candidate was format-only features of the spectra. These are the last-digit distribution, the share of trailing zeros, the number of distinct values, repeated adjacent values and the share of negative values.
- **Alone** they predict quite a lot: RMSLE 0.974 against 1.157 for the mean. `nuniq` has r = -0.26 with the target and `last_odd` has r = -0.22.
- **Added to the baseline** they make it slightly worse: 0.1756 mean, per-split change -0.0006 to +0.0010, inside or just beyond the noise spread.
- **Why the digits are uneven:** it is resampling. Some wavenumber columns (602, 802, 2602) take last digits 0, 2, 5 and 8 about 90% of the time. Others, like 1602, are uniform. That pattern fits interpolation onto a 2 cm⁻¹ grid followed by rounding to 5 decimals. The digit features are a function of the spectrum's own values and shape (flat or saturated spectra), which the deployed instrument also produces.
- **Judgement:** this is signal the model already has, not a leak.

**Flaws that hurt an honest model**

None found. The one honest training filter I tried hurt. It dropped 62 training rows with OC = 0 and 501 spectra with more than 5% negative absorbances, and scored 0.1783 mean, worse on every split by +0.0005 to +0.0060. The same kinds of rows sit in the test folds, so the model needs to see them.

**Attacks that found nothing**
- **Row order:** the target's correlation with row position is 0.004. Neighbouring rows' labels correlate at 0.0035, and neighbouring rows share a pedon in 0.02% of cases, so the rows are shuffled.
- **Exact copies:** no two rows have the same spectrum. The OSSL KSSL import notes say repeat scans were averaged and duplicates dropped.
- **Near copies across the split** (nearest neighbour in a 60-component PCA of the spectra): using the nearest training row's label scores 0.282–0.288, and a distance-weighted 10-neighbour version 0.219–0.227. Both are far worse than the baseline. Only 12–19 test rows per split have a training neighbour closer than 0.2, and their labels differ by 0.024–0.028 in log1p space. That is ordinary similarity, not the same sample under two IDs. Of the cross-pedon nearest pairs, 405 share an identical label, but that comes from labels rounded to 2 decimals.
- **Split integrity:** no pedon appears on both sides of any split. The train and test label means are within 0.03 on every split, so I did not fit a train-versus-test classifier.
- **Missing values, sentinels and transforms over all rows:** there are no NaNs, all spectra are rounded to 5 decimals, and values run from -0.97 to 3.61. These are raw absorbances: nothing was standardised, min-max scaled or ranked over the whole table.
- **Columns from after the prediction point and lookup formulas:** there are none. The only non-spectral columns are the target and `pedon_id`, which is not a feature.
- **Label precision as a source marker:** 65% of labels have 2 decimals. The 35% with 3–4 decimals have a much lower mean (0.74 against 1.44 in log1p), so they probably come from a different lab or calculation route. This marker is a property of the label, not of any input, and the spectra's own digit pattern does not differ between the two groups (5th-digit-zero share 0.175 against 0.174). Nothing usable.
- **Pedon structure:** pedon 39678 has 640 rows and pedon 10520 has 210. Both look like project-level placeholders rather than single profiles. That makes some folds lumpy, but nothing exploitable came out of it.

**What I could not check**
- **Lookup in the published file:** finding the rows in the public OSSL KSSL MIR file would probably work, since the import rounds spectra to 5 decimals just as the kit does. I did not download it; it is not ranked.
- **Target range against the documented snapshot:** the kit's maximum OC is expm1(4.375) ≈ 78%. The current OSSL import summary lists maxima of 63.45% (c729) and 56.40% (c1059). So the kit was built from a different snapshot, or the target was built differently, and I could not see what the preparation changed.
- **Sites and projects:** the split groups by pedon, but KSSL also has site and project IDs. Pedons from the same site or project could make the score optimistic. That would be a split-design question rather than an exploit, and without those IDs I could not measure it.
- **Within-test pedon reconstruction:** grouping test rows into pedons by spectral similarity and smoothing predictions across them was not tried. The task allows no group context, and no labels would flow from it.

Sources:
- [OSSL manual, database description](https://soilspectroscopy.github.io/ossl-manual/database-description.html)
- [OSSL KSSL import notes](https://raw.githubusercontent.com/soilspectroscopy/ossl-imports/main/dataset/KSSL/README.md)
- [OSSL tools and users](https://soilspectroscopy.github.io/ossl-manual/soil-spectroscopy-tools-and-users.html)

</details>

<details><summary>Precedent check</summary>

**Precedent check: open_soil_spectral_library (second pass, 2026-11-04)**

The register has no flag for this dataset (19 entries, 0 flags). The two 2026-11-04 decisions with the most at stake (the metric, and dropping the edge bin) both give reasons. Neither is filed the way precedents are filed, and the C5 evidence was measured on a scale the dataset no longer scores on.

**Direct answer to focus.md (`no_spread` TP-3, encodings claim C5)**

**`no_spread` (TP-3): keeping the dataset is consistent with precedent, but the record has no line on it.**
- **Probe result:** linear 0.985, LightGBM 0.980, random forest 0.978 skill, on 5 of 9 splits. That is a large, low-noise task where strong methods converge.
- **Closest precedents:**
  - `amex_non_iid_1m`: kept under TP-2 (2026-10-06), "strong methods converge".
  - `electric_motor_temperature_prediction`: kept under TP-3 (2026-10-06), R^2 0.94-0.97 for every probe model.
  - `open_university_learning_analytics_dataset`: "kept pending tuned results" (Lennart, 2026-10-22).
  - All three are in `.claude/skills/knowledge-curation/references/task_probes.md`, Cases.
- **Methods do spread on the declared scale.** I recomputed from the 2026-11-04 encoding run (fitted on log1p, scored as `rmse_log1p`, which is what `rmsle` computes):
  - LightGBM: 0.155 as is, 0.118 with the SG first derivative.
  - PLS: 0.158.
  - The source's Cubist reaches 0.114 in its 10-fold CV.
- **The gap:** every precedent wrote its keep down with numbers. This record does not. See prompt 2.

**C5 (encodings): the decision follows precedent; the evidence is on the wrong scale.**
- **The decision is consistent.** Recommended stays "as is", the candidates are registered, and the benchmark compares them later. That matches CLEAN-26 and `pancreatic_cancer_mouse_detection` (2026-11-02, Lennart): the default stays the published workflow even where another chain scores higher, and "one dataset is a case".
- **The evidence is on the wrong scale.** C5, and the vibrational table in `spectra.md` that cites this dataset as its only case, report RMSE in percent from fits in percent. The declared metric is RMSE on log1p. Fitted on log1p and scored as declared:

| Model | As is | ALS+SNV | SNV | SG d1 |
|---|---|---|---|---|
| LightGBM | 0.155 | 0.130 (3/3) | 0.136 (3/3) | 0.118 (3/3) |
| PLS 30 | 0.158 | 0.164 (0/3) | 0.145 (3/3) | 0.150 (3/3) |
| Ridge | 0.142 | 0.146 (0/3) | 0.138 (2/3) | 0.144 (0/3) |

- **What survives and what flips:**
  - The LightGBM conclusion holds.
  - The PLS conclusion reverses. C5 says PLS gains from ALS+SNV or the derivative and that SNV wins on 0/3 folds. On the declared scale SNV wins on 3/3 and ALS+SNV on 0/3.
  - "Ridge best as is" no longer holds: SNV wins on 2/3 folds.
  - The default does not change.
  - Future vibrational datasets will be compared against the `spectra.md` table, so it should carry the declared-scale numbers, or say that it is not on that scale.

**Decisions, ranked**

**1. Metric `rmsle` with `target_transform="log1p"` (CC6, Lennart, 2026-11-04). Departs from precedent with a stated reason, and the written reason contradicts itself.**
- **Under MET-3 (Must) it is consistent.**
  - It matches the pattern row in `metrics.md` ("RMSLE: `rmsle` with `target_transform="log1p"`").
  - Precedent: `mercari_price_suggestion` (2026-10-21).
  - The spec computes RMSE of log1p(percent). That is the source's tuning loss, which I checked in the source's training script `script_03h1_run_cubist_train.R`: `log1p` at line 92, `msr("regr.rmse")` at line 152.
- **Under MET-5 (Should) it is a new kind of case.**
  - The paper tunes by RMSE on log1p but ranks model types by Lin's CCC with an RPIQ cut-off of 2 (C11).
  - `forest_fires` (2026-10-21): fitted on log1p, but the declared metric was the one the paper *ranks* by (MAD on the area).
  - `gallstone_disease` and `heart_disease` (Lennart, 2026-10-21 and 2026-10-27): several criteria, so they took the fallback.
  - Following those precedents would give the fallback `rmse` in percent. That is what the screening (S5), the AI draft's issue 2 (PR #33 review page) and Myunghwan's CC2 (2026-10-27) all had.
- **What sets this case apart:**
  - The source's CV on log1p was run on exactly this cut (n = 75,929, RMSE 0.114) under the same lab and instrument that our split keeps.
  - The percent-scale evaluation is on independent sets, which is the transfer `fit_reason` says is not tested.
  - This fact appears only implicitly (C11 together with `fit_reason`).
- **The written reason contradicts itself.**
  - C11 ends "The declared RMSE in percent is on the independent evaluation's scale".
  - C10, T4 and the `_decisions` "Reference scale" text say "scored in weight percent after the inverse".
  - These state the old `rmse` metric. That collides with MET-3's warning against declaring a metric on another scale "by accident" in the text.
- **Not on file:** there is no MET-5 Cases row for "tuning criterion chosen over a compound ranking criterion". → Prompt 1.

**2. Drop the 600 cm-1 bin for every row ("do (b)", Lennart, 2026-11-04). Departs with a stated reason; not recorded as an exception or amendment.**
- **CLEAN-26 (Should, 2026-11-02)** says: "Keep the whole range the source publishes; dropping constant or copied bins is fine, cropping a range is a modelling choice."
  - The 600 bin is neither constant nor a copy: 27,193 distinct values, and the raw column alone has R^2 0.108.
  - The `micro_mass` drop (constant and copied bins, 2026-11-02) is a different reason.
- **CLEAN-11 (Should)** sets fills and impossible values to missing and keeps the column. Lennart's own precedents all did that:
  - `heart_disease`: `chol == 0` set to missing.
  - `sdss_17`: -9999 set to missing.
  - `mortgage` (2026-10-22): balances set to missing.
  - Here 53 of 75,929 values (0.07%) take the whole column with them.
- **The stated reason:** keep every spectrum whole, because per-row encodings return a spectrum with a missing value as missing (`spectra.md`, Pitfalls). This is a P6/P7 reason, and no higher Must is broken. CLEAN-22's reasons for removing a column are about what the column is, never width, and width is not the motive here.
- **The filing gap:**
  - Lennart asked to "document how to find this in the skills going forward". The new remedy ("an edge bin: drop it for every row; inner positions: set them missing") went into `spectra.md`, which says it "adds no rules of its own".
  - There is no `Exception to CLEAN-26` line in the record and no CLEAN-26 row in the `cleaning_features.md` Cases.
  - "Keeping the rules current" in `principles.md` puts a standing rule in its topic file. That makes this an amendment of CLEAN-26 that has not been written yet, not a one-off.

**3. Target ships as log1p (CC5, Lennart, 2026-11-04), reversing Myunghwan's CC2 (2026-10-27) and his "ship all" (CC4, 2026-10-28). Consistent.**
- It follows MET-3 and CLEAN-16, with precedents `forest_fires`, `mercari_price_suggestion`, `allstate_claims_severity` and `diamonds`.
- The newer curator decision wins, and C10 names the reason: CC2 compared percent with a fraction, never with log1p.
- This is not drift: two different curators, and the reason is explicit.
- Myunghwan holds the claim, and the definition he approved has since changed (target, metric, bins), so someone needs to tell him.

**4. Spectrum declared, `state="raw"`, columns renamed `mir_<n>` (CC5, Lennart). Consistent.**
- Follows CLEAN-26 and `pancreatic_cancer_mouse_detection` (raw, 2026-11-02).
- Replicate scans averaged by the instrument, with no baseline, SNV or derivative applied, matches the `raw` definition in `spectra.md`.
- `pedon_id` is typed categorical in `_feature_types` and is also the group. Precedent: `micro_mass` (`Strain`).

**5. Group description stands: pedon key, with a few archive or bulk-standard keys (CC6, Lennart). Consistent.**
- Follows SPLIT-23/SPLIT-29: replicates of one specimen are one group.
- The tensions table settles a group gap of 0.001: "the split follows the application" (P4 over P6, `forest_fires`).

**6. A correction to focus.md and the prep report: the "shipped frame keeps the raw order" claim is wrong.**
- `shuffle` keeps its default (True, seed 42) in `src/data_foundry/v2/preprocessing.py:order_rows`.
- Measured lag-1 autocorrelation of the target in the clean room's and the participant kit's data: 0.0035 (the raw order gives 0.735).
- CLEAN-23 (Must) holds.

**Smaller text drift.** These are writing problems, not decisions. "1,701" survives in the Spectrum description, in C15 ("All 1,701 measured predictors remain") and in the `spectra.md` case text. CC5 cites "REVIEW.md issues 2-3", but no such file exists.

**Reflection prompts**

**Prompt 1.** **Consistency check (AI, 2026-11-04):** your call on open_soil_spectral_library (`rmsle` on log1p as the source metric) differs from forest_fires (2026-10-21, MAD: the criterion the paper ranks by, not its fit scale) and from gallstone_disease / heart_disease (several criteria, so the fallback). The OSSL paper tunes by RMSE on log1p but ranks by CCC with RPIQ. What sets OSSL apart?
- (a) The source's 10-fold CV on log1p was computed on exactly this cut (n = 75,929, RMSE 0.114) under the same lab and instrument our split keeps, and the percent-scale RMSE belongs to the untested instrument transfer. Recorded as a MET-5 Cases row; C10, C11, T4 and `_decisions` reworded to "RMSE on log1p".
- (b) Treat it like forest_fires and gallstone: fallback `rmse` in percent (Myunghwan's CC2).
- (c) Reopen forest_fires to match.
- (d) Amend MET-5 to say a tuning criterion beats a compound ranking criterion.

**Prompt 2.** **Consistency check (AI, 2026-11-04):** `no_spread` (TP-3) has no recorded disposition here. amex_non_iid_1m, electric_motor_temperature_prediction and open_university_learning_analytics_dataset each have one, with numbers. What is the call?
- (a) Keep pending tuned results: a large, low-noise task where defaults converge, and on the declared scale methods spread from 0.118 (LightGBM, SG d1) to 0.158 (PLS). Recorded as a TP-3 Cases row.
- (b) Treat it differently from those precedents and look into the flag.

Edge bin (decision 2): the reason is stated, so this is not a prompt, only a filing question. Record `**Exception to CLEAN-26 (2026-11-04, Lennart):** a fill in an edge bin (53 spectra) is removed by dropping the bin so each spectrum stays whole; serves P6.` Or, since it was asked for "going forward", amend CLEAN-26 in `cleaning_features.md` to carry the edge-and-inner remedy that `spectra.md` now states.

</details>

<details><summary>Advocate</summary>

**Advocate opening brief: `open_soil_spectral_library` (ship after text-only fixes)**

The case for shipping: all validity rules (P1–P5) hold on measured evidence. What the panel found are text and filing defects. Each can be fixed without changing a row, a column, a fold or the metric.

**1. No leak, and the task cannot be gamed (P4: LEAK-1, LEAK-10, LEAK-16, CLEAN-23, all Must). This holds.**
- **Inputs.** The only inputs are 1,700 MIR absorbance bins, and each exists before the lab reference. No chemistry, identifiers, coordinates or depth are inputs. `pedon_id` is the group and is excluded from `feature_cols` (column auditor), so the blind reviewer's concern 3 is already met in code.
- **Row order.** The prep report's lag-1 exploit is refuted by three agents. The shipped lag-1 is 0.0035 and the raw order's is 0.735. Using the nearest row by position as the prediction scores `rmsle` 1.63, worse than the train mean (1.16).
- **Copies across the split.** None: 0% exact copies on 9 of 9 splits. Copying the label of the nearest spectral neighbour scores 0.28, and the same-site/same-depth label scores 0.368. The honest baseline is 0.175.
- **Task gamer.** Every attack scored at or below the honest baseline.
- **Why this outranks the objections.** Nothing in P4 is broken. The objections below rank lower (P6 or P7), or they are notes about P4 that come with a mild remedy.

**2. The split matches the use case (P4: SPLIT-1 and USE-10, Must; the tensions row "Temporal against grouped").**
- **Pedon split.** No pedon key appears on both sides of any of the 9 folds. Near copies across the split occur at chance rates: 1.24% below the 1st percentile and 5.0% below the 5th (SPLIT-29). Grouping by location instead scores about 0.150 against 0.148, so the extra site structure costs nothing measurable.
- **Large keys.** Key 39678 (640 rows, an archive campaign) sits in one fold, which only makes the split stricter.
- **What I concede.** The split does not test a shift to later scans or new projects. That shift costs +8–11% under the split auditor's matched control and +26% under the domain practitioner's, and the text does not name it.
- **Mildest remedy.** Add one sentence each to `fit_reason` and `splits_comment`, and list a project or scan-date split as a SPLIT-31 candidate variant.
- **Why not re-split.** A temporal split is not a fix:
  - The scan year is confounded with the project mix (archive rescans in 2011 and 2019).
  - 10,044 rows (13%) have no scan date.
  - The use case is a new profile on the same instrument, and `fit="approximate"` already discloses the transfer gap.
  - The tensions row says to pick one regime, the one the use case implies (Lennart, 2026-10-12).

**3. The metric is right; only its prose is wrong (P6: MET-3 Must, MET-5 Should, MET-2 Must).**
- **The scorer.** `rmsle` with `target_transform="log1p"` computes the RMSE of the shipped log1p values on every fold, and the claim and column auditors confirm this independently. Dummy scores range 1.62–1.65, so every fold can be scored (MET-2).
- **Source origin (MET-5).** The source tunes and cross-validates on exactly this scale: `log1p` at line 92 and `regr.rmse` at line 152 of `script_03h1_run_cubist_train.R`. Its CV runs on the same n = 75,929. The pattern row in `metrics.md` and the `mercari_price_suggestion` precedent match.
- **Practitioner view.** The domain practitioner would select models by this metric. It puts 54–75% of the weight on mineral soils at or below 3% OC, where MRV and fertility decisions are made. RMSE in percent gives 78–87% of the squared error to organic layers.
- **What I concede.** Four texts say "scored in weight percent": T4, C10, the last sentence of C11, and the `_decisions` "Reference scale" reason. Each needs a one-line rewrite (claim auditor's wording).
- **Precedent filing.** Record precedent-checker prompt 1(a) as a MET-5 Cases row. It names the fact that sets this case apart from `forest_fires` and `gallstone_disease`: the source's CV on log1p was run on this exact cut, with the same lab and instrument, and the percent scale belongs to the untested instrument transfer.
- **Why this outranks the objection.** The defect is in the text, not the score. On the remedy ladder, fixing the definition's prose is the mildest step that resolves it.
- **Edge case.** Predictions of −40 or 800 overflow `expm1`. This is a framework-wide matter for the metric code, not this dataset's.

**4. The task is worth benchmarking (P6: TP-3; precedents `amex_non_iid_1m`, `electric_motor_temperature_prediction`).**
- **Why `no_spread` fired.** R² of 0.98–0.985 hides the spread.
- **The spread on the declared scale:**
  - LightGBM: 0.155 as is, 0.118 with an SG first derivative (28% apart, lower on 3 of 3 folds).
  - PLS: 0.158.
  - Ridge: 0.142.
  - The source's Cubist: 0.114.
- **Size.** 75,929 rows and 1,700 bins, a large task with low noise. The two TP-3 precedents were kept with the same pattern of strong methods converging.
- **What I concede.** The record has no TP-3 disposition. Remedy: one line, prompt 2(a), with these numbers. The blind reviewer's "near ceiling" is a note on headroom, not a reason under TP-3.

**5. The data is faithful (P5: PROV), and its oddities are real readings kept with notes (P7: CLEAN-26, CLEAN-1; the "real task against imperfect cleaning" tension).**
- **What reproduces.** Every count: 86,603 / 76,813 / 75,929 rows, 20,626 keys, 62 zeros. The source's own n is 75,929. The join is one-to-one, with 0 duplicate spectra and the XS/XN totals intact.
- **36 tilted-baseline spectra** (0.05% of rows). CLEAN-26 says to keep the spectrum as published. When the task gamer dropped these and similar rows from training, the score got worse on every split (+0.0005 to +0.006). Remedy: one sentence in C3 or C4.
- **The 151 rows above 58% OC.** The definition deliberately does not clip ("never clip"), and the value is an analytical estimate from total C. I concede the maximum of 78.45% against the current OSSL summary's 63.45% is unexplained. Remedy: a note. Dropping the rows would need evidence that they are errors, and none is measured (EV-1).
- **Untested.** C13 uniqueness against the other libraries (needs R) and the S/N source. Neither is contradicted by evidence. Mark them as unverified in the notes (EV-7).

**6. Dropping the 600 cm-1 bin was a decision with a stated reason; it only needs filing (CLEAN-26, Should).**
- **The facts.** 53 spectra (0.07%) hold an exact 0 beside 602 cm-1 readings of 1.27–1.86, so the bin is a fill. `mir_602` carries the same signal (raw R² 0.104 against 0.108).
- **The reason.** Lennart's "do (b)" keeps every spectrum whole. Per-row encodings return a spectrum with a missing value as missing, which serves P6 and P7. No Must is broken.
- **What I concede.** There is no `Exception to CLEAN-26` line, and the standing remedy sits in `spectra.md`, not in `cleaning_features.md`. Remedy: write the exception now, or the amendment the precedent checker drafted, since Lennart asked for this "going forward". On the remedy ladder, filing beats undoing a curator decision.

**7. Everything else is writing (P7 and writing.md, all text-only).**
- **"1,701".** Change to 1,700 in C15, the Spectrum description and line 113 of `spectra.md`.
- **Group wording.** Replace "a few large keys / bulk standards" with: "usually one profile; 1,779 keys (14% of rows) repeat a depth; the largest is an archive campaign". No reference soil is shown (split auditor).
- **C5.** Relabel it as percent-scale. Add the declared-scale line (LightGBM 0.174 / 0.148 / 0.126) and update the `spectra.md` table, where the PLS and Ridge conclusions reverse. The recommended default stays "as is" (CLEAN-26, `pancreatic_cancer_mouse_detection`).
- **C11 citation.** Cite `ossl-models/out/fitted_models_performance_v1.2.csv`, not S2 Table.
- **Dangling reference.** Drop "REVIEW.md issues 2-3".
- **Target name.** Rename to `log1p_organic_carbon_weight_percent` (CLEAN-16, Should). The precedents split, so either rename (cheap) or record it as a departure. It is the curator's call.
- **Process.** Myunghwan holds the claim and approved an older definition, so someone needs to tell him. Rebuilding the stale container (2026-10-29) happens only when the curator asks.

**Judgment record**
```text
Verdict: ship after changes (text and filing only).
Validity: USE-3, USE-5 hold (fit approximate); LEAK-1, LEAK-10, LEAK-16, CLEAN-23 hold; SPLIT-1, SPLIT-23, SPLIT-29 hold, scan-date/project shift to be noted (SPLIT-31 variant); PROV counts reproduce, C13 and S/N untested.
Value: MET-3, MET-5 hold for rmsle on log1p, MET-11 prose fix; TP-3 no_spread, keep (spread 0.118-0.158 on the declared scale).
Quality: CLEAN-26 edge-bin departure to file as exception or amendment; CLEAN-16 name is the curator's call; 36 tilted spectra and >58% OC rows kept with notes.
Weighed: size +, source +, use case +, saturation -, instrument transfer untested -.
For the curator: MET-5 Cases row (prompt 1a); TP-3 line (prompt 2a); CLEAN-26 exception vs amendment; target rename.
```

</details>

<details><summary>Critic</summary>

**Opening brief against shipping `open_soil_spectral_library` as defined (opposing advocate)**

**My position: ship only after changes. I am not asking for exclusion.** The panel found no leak and no exploit: the task gamer beat no baseline (0.17490), the rows are shuffled (lag-1 0.0035), and 0 pedons cross the split. The use case is real. What is wrong is how the definition describes the task, the metric and the target. Several of these descriptions are false as written, and two evidence lines were measured on a scale the dataset no longer scores on. Points 2 and 3 are text fixes that the Musks SPLIT-24 and MET-11 require. The others are notes, a rename or filing.

**1. The split hides a 10–26% shift to later scans and new projects, and no note says so (P4; SPLIT-1 Must, SPLIT-31 Should, USE-9).**
- **Problem.** `fit_reason` names only the change of instrument. A lab using this model scores newly arrived samples: later scans, often from projects the training set lacks. The shipped split does not test that. 93–96% of test rows have their project in training (split auditor).
- **Evidence.**
  - Domain practitioner: trained on scans up to 2017 and tested on 2018–2022, `rmsle` is 0.178, against 0.141 for a matched grouped control of the same training size. That is +26%. The error is higher in every OC band; at 3–12% it is 0.306 against 0.197.
  - Split auditor, with a different design: +8–11% at the 2017, 2018 and 2019 cutoffs, and +10% for a project split (0.1634 against 0.1482).
- **Effect.** Leaderboard gaps smaller than about 0.035 `rmsle` say little about deployment, and the definition does not warn readers of this.
- **Why not a re-split.** The scan year is confounded with the project mix and missing for 13% of rows. SPLIT-3 and USE-10 make grouped the defensible single regime.
- **Remedy (a note).** Add to `fit_reason` and `splits_comment`: "93–96% of test rows have their project in training; a calibration applied to later scans or new projects scores about 10–26% worse in RMSLE (measured 2026-11-04)". List a project or scan-date split as a candidate variant (SPLIT-31).

**2. The group is described as something it is not (P4; SPLIT-24 Must for the key, met; the description is what fails).**
- **Problem.** The `Grouping.definition`, `task_summary.split` and C9 call each key "a sampled soil profile, whose layers are the rows", with "a few large keys" holding "bulk standards".
- **Evidence.**
  - Key 39678 is the North Dakota MLRA54 archive campaign: 640 rows over 151 upper depths.
  - 1,779 keys (10,689 rows, 14%) repeat an upper depth.
  - 348 locations hold 2–77 keys each (replicate pits and revisits).
  - "Bulk standards" is contradicted: key 10520 has a log1p SD of 0.517, which no single reference soil would show.
  - The measured cost is small: grouping by location scores about 0.150 against 0.148.
- **Effect.** A reader of the definition is told the split is cleaner than it is. The blind reviewer, reading cold, could not tell what the 640-row key was.
- **Remedy (text).** "A pedon key, usually one profile; archive campaigns and research projects share a key (the largest has 640 rows), and replicate pits at one site have separate keys (grouping by location: about 0.150 against 0.148 RMSLE)." Drop "bulk standards".

**3. Four texts say the score is in weight percent, but the metric is on the log1p scale (P6; MET-3 Must, MET-11 Must).**
- **Problem.** The spec is right: `rmsle` with `target_transform="log1p"` equals the RMSE of the shipped values on all 9 folds (1.1676 for both). But these texts still describe the old percent-scale `rmse`:
  - T4 ("is scored in weight percent", README line 93)
  - C10 ("score RMSE in weight percent after the inverse")
  - C11 ("The declared RMSE in percent…")
  - the `_decisions` "Reference scale" reason (README line 314)
- **Second problem: the C5 evidence is on the wrong scale.** It was measured as RMSE in percent. Refitted on log1p and scored as declared (precedent checker):
  - PLS flips: SNV now wins on 3 of 3 folds, ALS+SNV on 0 of 3.
  - "Ridge best as is" fails: SNV wins on 2 of 3.
  - C5's 1.85 does not reproduce (claim auditor: 2.14).
  - The `spectra.md` vibrational table cites this dataset as its only case.
- **Effect.**
  - A percent RMSE (about 2.1) and the benchmark score (about 0.17) differ by a factor of about 12.
  - The two scales pick different models: fitting on log1p wins `rmsle` on 3 of 3 folds, fitting on percent wins RMSE in percent on 3 of 3.
  - MET-3 exists so that "a metric on another scale is never declared by accident" in the text.
- **Remedy (text and relabelling).**
  - Rewrite the four strings to "RMSE on log1p (`rmsle` on the percent), the source's CV and tuning scale".
  - Relabel C5 as percent-scale history, or replace it with the declared-scale numbers: LightGBM 0.155 as is, 0.130 ALS+SNV, 0.136 SNV, 0.118 SG d1.
  - Correct the `spectra.md` table the same way.

**4. The metric departs from MET-5 precedent, and no distinguishing fact is on file (P6; MET-5 Should; principles "Consistent judgement", case 2).**
- **Problem.** The paper tunes by RMSE on log1p but ranks model types by Lin's CCC with an RPIQ cut-off of 2.
  - `forest_fires` declared the criterion the paper ranks by.
  - `gallstone_disease` and `heart_disease` took the fallback when a paper used several criteria.
  - The screening (S5) and Myunghwan's CC2 both had the fallback `rmse` in percent.
- **I do not dispute the choice.** The practitioner's evidence supports `rmsle`: it puts 54–75% of the weight on soils at or below 3% OC, where the decisions are made. RMSE in percent puts 78–87% of the squared error on the 16% of organic layers above 12%.
- **What is missing.** A Should departure must name its fact. CC6 gives only "following the source".
- **Remedy (filing).** Add a MET-5 Cases row with the fact: the source's 10-fold CV on log1p was run on exactly this cut (n = 75,929, RMSE 0.114, CCC 0.995), and the percent-scale evaluation belongs to the untested instrument transfer. Also fix C11's citation: these numbers are in `ossl-models/out/fitted_models_performance_v1.2.csv`, not the PLOS S2 Table, which has 2 decimals and no n (PROV-8).

**5. Target values above the physical maximum go unmentioned (P7; CLEAN-11 Should; P5 if it is a snapshot question).**
- **Evidence (my count on the clean room's data).** After expm1, 151 rows exceed 58% OC, 71 exceed 60%, 14 exceed 63.45% and 3 exceed 70%. The maximum is 78.45%.
  - Organic matter holds about 58% carbon (blind reviewer).
  - The current OSSL KSSL import summary gives maxima of 63.45% (c729) and 56.40% (c1059) (the OSSL KSSL import notes). That is a later snapshot, so it proves nothing, but our 14 rows above it are unexplained.
  - Separately, 36 spectra have a negative mean absorbance, down to -0.97 at the high-wavenumber end, which looks like a tilted baseline (column auditor).
- **Effect.** About 0.1–0.2% of rows, sitting at the top of the log scale. They are probably harmless to the ranking, but they are undisclosed. The definition's `between(0, 100)` assert lets them through silently.
- **Remedy (mildest).**
  - Trace the 14 rows above 63.45% to their preparation (S or N) and project.
  - Then either add a note (char or coal fragments are plausible), or set the impossible ones missing under CLEAN-11 (the `heart_disease` `chol == 0` precedent).
  - Add one sentence on the 36 tilted spectra. Keep those rows: dropping them hurt an honest model by +0.0005 to +0.0060 per split.

**6. The target's name hides the log1p (P7; CLEAN-16 Should).**
- **Evidence.** `organic_carbon_weight_percent` holds values from 0 to 4.375. The blind reviewer's first concern was that "the target is not what its name says". It concluded the values were not weight percent, the exact misreading the rule guards against. Precedents that renamed: `log1p_meter_reading`, `log1p_trip_duration`, `log_price`. Precedents that kept the name: `price` (diamonds, mercari), `loss`, `area`.
- **Remedy.** Rename to `log1p_organic_carbon_weight_percent`. Or, if the curator keeps the name, record the departure as an exception with its reason.

**7. Filing and stale text (house rules and writing.md, plus three unrecorded decisions).**
- **The 600 cm-1 bin drop departs from CLEAN-26** ("keep the whole range") and from CLEAN-11 (set the fill missing, keep the column). Its reason is real: keep each spectrum whole. But Lennart asked for it "going forward", and the remedy went only into `spectra.md`, which "adds no rules of its own". Remedy: amend CLEAN-26 in `cleaning_features.md`, or record `Exception to CLEAN-26`.
- **No TP-3 (`no_spread`) disposition is recorded** (probe skill: linear 0.985, LightGBM 0.980). Every precedent has one, with numbers. Remedy: a "keep" line with the declared-scale spread (0.118 to 0.158).
- **Stale text.**
  - "1,701" survives in C15, the Spectrum description ("1,701 positions") and `spectra.md` line 113; 1,700 ship.
  - CC5 cites a REVIEW.md that does not exist.
  - The last Assessment says "no panel ran".
  - The built container (2026-10-29) predates every 2026-11-04 change.
- **Myunghwan holds the claim** and approved ("ship all", 2026-10-28) a definition whose target, metric and bins have since changed. He should be told before shipping.

**What I do not argue.** No leak (LEAK-1, LEAK-10, LEAK-16 hold). No re-split (SPLIT-4: the grouped/IID gap of 0.001 to 0.006 decides nothing). No change of metric. No exclusion. A failing permutation test is not a concern either: the group permutation test (SPLIT-27) never finished, but with R² of 0.98 its result cannot matter. The edge case where `rmsle` raises on an extreme prediction (below -37 or above about 709 on the log1p scale) is a framework matter, not this dataset's.

**Judgment record.**
- Verdict: ship after changes.
- Validity: SPLIT-1 and SPLIT-24 hold; the shift to later scans and new projects needs a note (point 1); the group description is false (point 2).
- Value: MET-3 and MET-11 text contradicts the declared metric (point 3); the MET-5 departure is unrecorded (point 4).
- Quality: CLEAN-11 on the target values above 60% (point 5); CLEAN-16 (point 6); CLEAN-26 and TP-3 not filed (point 7).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: `open_soil_spectral_library`**

The critic and I agree on the verdict ("ship after changes"), on every validity rule, and on almost every remedy. I concede six of the seven points in substance. I dispute two narrower things: the conclusion the critic draws in point 1, and the "set missing" option in point 5.

**1. Shift to later scans and new projects (SPLIT-1, SPLIT-31, USE-9).**
- **Conceded:** the note, its wording, and listing a project or scan-date split as a SPLIT-31 candidate variant. The numbers match mine:
  - 93–96% of test rows have their project in training.
  - The cost is +8–11% (split auditor) and +26% (domain practitioner).
- **Disputed:** "leaderboard gaps smaller than about 0.035 `rmsle` say little about deployment".
  - Both shift measurements used LightGBM only. The split auditor says so: "I fitted no other model family under the alternative splits".
  - So the evidence shows that the error level goes up. It does not show that models change order.
  - A note that infers a ranking from a level makes a claim nobody measured (EV-1). Under SPLIT-4, the size of a gap decides nothing.
  - The +26% also comes from a control of random pedons among the dated rows, which mixes year and project. The practitioner flags this confound himself.
- **Suggested note wording:** "scores about 10–26% worse in RMSLE for a model applied to later scans or new projects (LightGBM, measured 2026-11-04); whether rankings change is untested."

**2. Group description (SPLIT-24).**
- **Conceded in full.** "Bulk standards" is refuted: key 10520 has a log1p SD of 0.517. Key 39678 is an archive campaign. 1,779 keys (14% of rows) repeat a depth.
- The critic's wording, which comes from the split auditor, is better than mine because it also names replicate pits and gives the location-grouping figure (about 0.150 against 0.148). I adopt it.
- This is a text fix only. The key is native and the split stays.

**3. Metric text and the scale of C5 (MET-3, MET-11).**
- **Conceded in full,** including the 1.85 that does not reproduce (the claim auditor gets 2.14, with settings unstated).
- **Remedy:** relabel C5 as percent-scale history and add the declared-scale line (LightGBM 0.155 / 0.130 / 0.136 / 0.118). Correct the `spectra.md` table, where the PLS conclusion and "Ridge best as is" both reverse.
- **What does not change:** the score, the default encoding ("as is", per CLEAN-26 and the `pancreatic_cancer_mouse_detection` precedent), and every row.

**4. The MET-5 departure is not on file.**
- **Conceded.** This is the same remedy I gave (prompt 1a), and I adopt the critic's PROV-8 fix to the C11 citation (`ossl-models/out/fitted_models_performance_v1.2.csv`).
- Nobody disputes the choice itself. The departure only needs its fact written down.

**5. Target values above the physical maximum (CLEAN-11).**
- **Conceded:**
  - Trace the 14 rows above 63.45% to their preparation (S or N) and project.
  - Add a note on the 151 rows above 58% OC.
  - Add one sentence on the 36 tilted spectra and keep those rows.
- **Disputed:** setting these values to missing now.
  - CLEAN-11 applies to impossible values, and every precedent had proof of impossibility: `chol == 0`, `age = 455`, an LTV above 300%, a pXC50 implying 1.7 million mol/L.
  - About 58% C is the conventional carbon share of soil organic matter, not a physical ceiling. Charcoal, char and coal fragments carry 60–90% C, and the critic names them as plausible.
  - The source defines the value as estimated from total C, so an OC above 58% is possible.
  - Setting the target missing removes the row by CLEAN-15, which is a step up the remedy ladder taken without evidence that these are errors (EV-1).
  - The 63.45% figure comes from a later snapshot. The critic concedes it "proves nothing".
- **Remedy:** a note now. Set values missing only if the trace finds a documented error.
- **On the `between(0, 100)` assert:** it is a sanity bound, and the definition says "never clip" on purpose. The 151 rows are known and should be disclosed in the notes. They are not hidden by the code.

**6. Target name (CLEAN-16, Should).**
- **Conceded.** The blind reviewer's misreading is direct evidence of the harm the rule guards against, and the rename (`log1p_organic_carbon_weight_percent`) changes no row.
- I withdraw "either way is fine" and support the rename. It stays the curator's call because the precedents split.

**7. Filing and stale text.**
- **Conceded in full:**
  - the CLEAN-26 exception or amendment
  - the TP-3 keep line
  - "1,701" in three places
  - the dangling "REVIEW.md issues 2-3"
  - telling Myunghwan before shipping
- The critic adds one fact I lacked: the last Assessment says "no panel ran". That needs updating too.
- The container dated 2026-10-29 is stale. It gets rebuilt only when the curator asks, and no rebuild is needed to settle any point here.

**Where we end up.** We share the verdict: ship after text, filing and naming changes, with no change to rows, splits or metric. Two disagreements remain:
- **Point 1:** the shift note should state an error level, not that rankings are unreliable.
- **Point 5:** a note now, and a value set missing only if the trace shows it is an error.

Both follow the remedy ladder and EV-1.

```text
Verdict: ship after changes (text, filing, rename; no row, split or metric change).
Validity: LEAK-1/10/16, CLEAN-23, SPLIT-1/23/24/29 hold; SPLIT-31 note on scan/project shift (level only, ranking untested); group wording per split auditor.
Value: MET-3/MET-11 four strings + C5 relabel + spectra.md table; MET-5 Cases row (prompt 1a) + C11 citation (PROV-8); TP-3 keep line (0.118-0.158).
Quality: CLEAN-16 rename (supported); CLEAN-26 exception or amendment; >58% OC traced and noted, set missing only on evidence of error (CLEAN-11, EV-1); 36 tilted spectra noted and kept.
Process: stale Assessment, 1,701, dangling REVIEW.md; tell Myunghwan; rebuild only when the curator asks.
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal to the advocate (`open_soil_spectral_library`)**

We agree on the verdict: ship after changes, with no exclusion, no re-split and no change of metric. The advocate says the changes are "text and filing only". I dispute that on one point (5): the target rows above the physical maximum need a trace, and probably a CLEAN-11 decision. On the other points we differ only in wording or in what goes on file.

**New fact (used under advocate point 5, not a new point).** I traced the 14 rows above 63.45% OC. I joined the claim auditor's aligned scan metadata to the shipped target and took expm1 of the target.
- **All 3 rows above 70% are N-preparation (XN) rows of the RaCA MO14 project, in surface layers:**
  - 150180XN, Oi, 78.45%
  - 165168XN, Oa1, 75.22%
  - 150179XN, Oi, 73.43%
- **The other 11 rows:**
  - 5 more are RaCA XN rows (MO14/MO12, Oa, 63.6–67.8%).
  - 6 are XS rows from Dismal Swamp and NWCA (63.45–65.6%).
- **The 151 rows above 58%:** 76 XS and 75 XN, all O horizons or blank.
- **Against the source's import table** (the OSSL KSSL import notes): both columns are `eoc_tot_c`. c1059 has n = 63,499 and a maximum of 56.40; c729 has n = 2,231 and a maximum of 63.45.
- **Why this matters:** an Oi layer is fresh litter, about 45–50% C. A value of 73–78% is not a reading the source's current table would allow. Charcoal is not a plausible cause in litter.

---

**Advocate 1: no leak, no gaming (LEAK-1, LEAK-10, LEAK-16, CLEAN-23). Concede in full.**
My brief says the same. `pedon_id` is excluded from `feature_cols` (column auditor). Lag-1 is 0.0035. The task gamer beat no baseline (0.17490).

**Advocate 2: the split matches the use case (SPLIT-1, USE-10). Concede the split and the remedy. Dispute the group wording.**
- **The shift note.** The advocate concedes the +8–11% / +26% shift and the SPLIT-31 note. We agree.
- **The proposed wording for the group** ("usually one profile; 1,779 keys repeat a depth; the largest is an archive campaign") leaves out the other half of the finding. 348 locations hold 2–77 separate keys each (4,321 rows: replicate pits, 5-year revisits, RaCA five-pedon sites).
- **Why it must be named.** SPLIT-24 (Must) is met only because grouping by location costs about 0.150 against 0.148. That number is the evidence the key is good enough, so it belongs in the text. Without it, a reader cannot tell why the split is not grouped by site.
- **"Large keys only make the split stricter."** True for the 640-row key. It says nothing about same-site pedons that sit in different keys.
- **Remedy (unchanged).** My point 2 wording: add the location sentence with the 0.150/0.148 figures, and drop "bulk standards". The split auditor showed key 10520 has an SD of 0.517, which no single reference soil would show.

**Advocate 3: the metric is right, only its prose is wrong. Concede the metric and the four rewrites. Dispute two parts.**
- **(a) "MET-5 holds" (judgment record).** It does not hold yet.
  - MET-5 is a Should, and following precedent gives the fallback (`forest_fires`; `gallstone_disease`/`heart_disease`; S5; CC2).
  - The distinguishing fact is on file only implicitly (precedent checker), and CC6's stated reason, "follow the source metric and scale", is not that fact. Principles, "Consistent judgement": a departure is filed with its fact.
  - The advocate lists the Cases row under "For the curator", so this is a disagreement in labelling only. Until the row exists, the record should read "MET-5 departs from precedent, fact to file", not "holds".
- **(b) The evidence is wrong as well as the prose.** The C5 conclusions are not only labelled on the wrong scale. Two of them reverse on the declared scale:
  - PLS: SNV wins on 3 of 3 folds; ALS+SNV wins on 0 of 3.
  - Ridge: SNV beats "as is" on 2 of 3.
  - The `spectra.md` vibrational table cites this dataset as its only case. C15 (dataset.py line 67) also states its numbers as "percentage points".
  - EV-1 requires the evidence behind a decision to be measured as declared, so a "percent-scale" label alone does not fix C5's conclusions.
  - **Remedy:** replace the C5 numbers with the declared-scale table (or add it beside them) and correct the `spectra.md` table. Relabel C15 too.

**Advocate 4: TP-3, keep. Concede the keep and the one-line disposition. Dispute one number.**
- **Cubist 0.114 does not belong in the spread.** It is the source's 10-fold CV, and the paper does not say that CV was grouped (claim auditor, row 3). Putting it next to grouped-split scores overstates headroom and mixes regimes.
- **Two runs are quoted as one.** The advocate cites LightGBM "0.155 / 0.118" (precedent checker, results.csv) in point 4 and "0.174 / 0.148 / 0.126" (claim auditor) in point 7. These are different runs with different settings.
- **Remedy:** state the TP-3 spread from one run with its settings: 0.118–0.158 (precedent checker), leaving out Cubist. This follows EV-1.

**Advocate 5: the data is faithful, keep the oddities with notes. Concede the PROV counts, the 36 tilted spectra (keep, one sentence) and the untested C13/S-N items (mark them EV-7). Dispute the target values above the maximum.**
- **The advocate's position** is that dropping the rows "would need evidence that they are errors, and none is measured".
- **The fact above is that evidence for the top 3.** They are Oi/Oa1 litter at 73–78% C, all from one project (RaCA MO14) and one preparation (XN). The source's own current import caps OC at 63.45 (c729) and 56.40 (c1059).
- **Which rule applies.** CLEAN-11 (Should) sets impossible values to missing (precedent: `heart_disease` `chol == 0`, Lennart). "Never clip" is about not moving real values to a bound. It does not cover keeping impossible ones. EV-1 is met for the rows above about 70%.
- **The borderline rows.** The 63.45–67.8% rows sit at or just above the c729 maximum, and Oa horizons can approach 58–60%. For those, a note is the mildest remedy that works.
- **Cost.** 3 rows out of 75,929. The ranking is unaffected. But a target value no soil can have is a P7 defect, not a matter of wording.
- **Remedy:**
  - Set the 3 RaCA MO14 XN rows above 70% to missing. That drops them, because rows without a label drop.
  - Or file `Exception to CLEAN-11` with a reason.
  - Note the 11 rows from 63.45 to 67.8% with their projects.
  - Also flag that the XN (N-preparation) route supplies the outliers. That bears on the untested S-before-N claim (C7, C14).

**Advocate 6: edge bin, file it. Concede.**
I prefer the CLEAN-26 amendment in `cleaning_features.md` over a one-off exception, because Lennart asked for it "going forward" and `spectra.md` "adds no rules of its own" ("Keeping the rules current"). That is the curator's choice.

**Advocate 7: everything else is writing. Concede, except the rename.**
- **Conceded:** "1,701" (also at dataset.py line 93), the C11 citation (PROV-8), the dangling REVIEW.md reference, the Myunghwan notice, and no rebuild until asked.
- **Disputed: the rename is "the curator's call" because the precedents split.** That is not neutral.
  - CLEAN-16 is a Should, and a Should applies unless a reason for departing is on file.
  - The `price`/`loss`/`area` precedents carry no reason showing their names were not misread.
  - Here the blind reviewer did misread the name ("the target is not what its name says"), which is the harm CLEAN-16 guards against.
  - **Remedy:** rename to `log1p_organic_carbon_weight_percent`. If the curator keeps the name, file a CLEAN-16 exception with its reason. That is the advocate's own fallback, so we differ only on which is the default.

---

**Judgment record (critic, after rebuttal)**
```text
Verdict: ship after changes. Not exclusion.
Agreed: no leak (LEAK-1/10/16, CLEAN-23); grouped split stays (SPLIT-1, USE-10); rmsle on log1p stays; TP-3 keep;
  36 tilted spectra kept with a note; edge bin filed; stale text fixed; Myunghwan told.
Still disputed:
  1. CLEAN-11: the 3 targets of 73-78% OC (RaCA MO14, XN, Oi/Oa1) set missing or filed as an exception; the 11 at
     63.45-67.8% noted. More than a note.
  2. EV-1: C5 conclusions (PLS, Ridge) reverse on the declared scale; replace them and the spectra.md table, not only relabel.
  3. MET-5: "departs, fact to file" until the Cases row exists, not "holds".
  4. SPLIT-24 wording must include the 348 multi-key locations and the 0.150 vs 0.148 figure.
  5. TP-3 spread from one run (0.118-0.158), without the ungrouped Cubist 0.114.
  6. CLEAN-16: rename by default; keeping the name needs a filed exception.
```

</details>

## Reference

Safanelli JL, Hengl T, Parente LL, Minarik R, Bloom DE, Todd-Brown K, et al. (2025). Open Soil Spectral Library (OSSL): Building reproducible soil calibration models through open development and community engagement. PLoS ONE 20(1): e0296545.
