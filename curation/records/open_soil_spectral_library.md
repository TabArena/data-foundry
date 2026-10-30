---
unique_name: open_soil_spectral_library
name: Open Soil Spectral Library (OSSL) / KSSL MIR soil spectra
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Many features
- Non-IID (Grouped)
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

## Reference

Safanelli JL, Hengl T, Parente LL, Minarik R, Bloom DE, Todd-Brown K, et al. (2025). Open Soil Spectral Library (OSSL): Building reproducible soil calibration models through open development and community engagement. PLoS ONE 20(1): e0296545.
