---
unique_name: bigsoldb_2
name: 'MixtureSolDB: solubility of organic compounds in binary solvent mixtures at various temperatures'
checked_by:
- Myunghwan
data_foundry_status:
- 'DF: Yes'
- WIP (Triage)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Grouped)
original_source: Other
year: '2025'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.18660057
- https://doi.org/10.1038/s41597-026-07047-z
v2_path: datasets/_dev/tabarena-v0pt2/bigsoldb_2/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: MixtureSolDB (2026), 175,166 literature solubility values of 810 organic solutes in 750 binary solvent mixtures at 252-383 K, a large open regression for choosing a solvent mixture; the record also carries BigSolDB 2.0 (single solvents, 2025), a separate dataset of the same group that needs its own record.
- Source: Malikov, Krasnov, Kiseleva, Meshcheriakova, Kuznetsov, Elistratov, Vasiyarov, Tatarin and Bezzubov (Kurnakov Institute of General and Inorganic Chemistry RAS; Lomonosov Moscow State University), "Dataset of solubility values for organic compounds in binary mixtures of solvents at various temperatures", Scientific Data 2026 (doi 10.1038/s41597-026-07047-z, online 2026-03-20); Zenodo 10.5281/zenodo.18660057 (v3, CC BY 4.0). As published: MixtureSolDB.csv (41 MB), 175,166 rows x 20 columns (record id, solute and solvent SMILES, temperature, solubility as mole fraction and in g/100 g with their logs, solvent names, fractions and fraction type, compound name, CAS, PubChem CID, FDA flag, source DOI, a pure-solvent endpoint flag), plus solvent boiling points and an abbreviation legend; 3,001 solute-mixture systems from 1,115 articles, literature searched to October 2025 (Methods). BigSolDB 2.0 (Krasnov et al., Scientific Data 2025, doi 10.1038/s41597-025-05559-8; Zenodo 15094979, 2025-03-27): 103,944 values, 1,448 solutes, 213 single solvents, 243-425 K, 1,595 articles; BigSolDB 1.0 (Zenodo 6984601, 2022, 54,273 values, 830 solutes, 138 solvents) is its earlier version (PROV-6).
- Use case: a process or formulation chemist picks a solvent mixture and a temperature (crystallization, reaction medium, formulation) for a compound before measuring its solubility; the descriptor names the applications (mixtures give "a more diverse set of reaction media and crystallization conditions", measurement is "time- and labor-consuming", Background) but no actor; fit approximate (literature values from many labs); regime grouped by solute, on the Bemis-Murcko scaffold (SPLIT-31), since many temperatures and fractions per solute-mixture system would otherwise sit on both sides.
- Siblings and duplicates: `drug_solubility_binary_solvent_mixtures` (the CheMixHub copy of Bao et al. 2024, 27,166 values, 169 molecules) is the same task from an earlier compilation, which the descriptor's comparison table lists ("BaoDB (2024)": 28,098 values, 125 solutes; "MixSolDB (2025)": 34,734): another source, so not a duplicate (PROV-4), but the rows overlap through the same articles, and MixtureSolDB is larger and newer, so the curator will likely want one of the two; `aqsoldb`, `tdc_aqsoldb` and `somas_aqueous_solubility` are aqueous solubility; `solprop_solvation_free_energy` overlaps BigSolDB in its solid solubilities. This record mixes two datasets: its `unique_name` names BigSolDB 2.0, its `name` and Assessment MixtureSolDB; single-solvent and mixture solubility are distinct tasks (PROV-7), so one record each. External collections: none found.
- Better data: from the curator's Zotero collection (items 50, 72, 99), the awesome-chemistry-datasets list and the dead-link check; no further search this round.
- Papers and pages: the two Scientific Data descriptors (read through Europe PMC, PMC13168504 and PMC12264061); Bao et al. 2024, J Cheminform (doi 10.1186/s13321-024-00911-3; LightGBM, MAE 0.33 in LogS on its holdout).
- Metric: none in the descriptors (no model benchmark; Technical Validation checks the extraction; BigSolDB 2.0 reports the agreement of repeated measurements from different sources, RMSE 0.39 logS and R2 0.90, a noise floor); Bao et al. scored MAE on log g/100 g for the predecessor data; so the fallback `rmse` on the log solubility; inputs none.
- Risks for /add-dataset: ship one target unit (log mole fraction or log g/100 g; the other is a conversion of the target and goes); source DOI, CAS, PubChem CID, the compound name and the FDA flag are identifiers or provenance, not features; the pure-solvent endpoint rows overlap BigSolDB; repeated measurements from different labs disagree (the noise floor above); solutes and solvents come as SMILES and need descriptors (CLEAN-24); split the record before adding.
- Priority: gap 0 (chemistry, regression, grouped not thin), use case 0 (approximate), source +, shape + (175,166 values, 810 solutes, grouped), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the dead-link check of the curator's Zotero collection; the curator's Zotero collection, item 50: "An Ensemble Model for Molecular Solubility Prediction Across Aqueous and Organic Solvents"; the curator's Zotero collection, item 72: "A Model-Mediated Stacked Ensemble Approach for Depression Prediction Among Professionals"; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: 175,166 measured solubility values, 810 solutes, 3,001 solute/binary-solvent systems, 750 binary solvent mixtures, 252-383 K, from 1,115 articles; one CSV of 41 MB with 20 columns (plus a solvent ...; target: solubility of the solute in the mixture at a temperature (log mole fraction, or g/100 g); access: open.
- Why: measured values, large, CC BY 4.0, new (2026). The authors point to it from the BigSolDB 2.0 record. The mixture composition is an input, so it is a different task from mono-solvent solubility. | Large, real, open, and documented in a data paper. | measured target compiled from peer-reviewed articles with a source ...
- Adds: a sibling of the first-pass hit bigsoldb_2_organic_solubility (same group, separate dataset, not a version). Caveats: compiled from many papers (noise between labs); solutes as SMILES need featurizing; split grouped by solute. | Already proposed by zotero_04 (bigsoldb_2) and awesome_chem_1 ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the record holds MixtureSolDB; BigSolDB 2.0 needs its own record.

CC (2026-11-09, Myunghwan): "we should proceed with loge mole-fraction regression as the main candidate. we check next target only if it doesn't look good." Explicitly requested tabarena-add-dataset, then authorized the GPU gateway. Interpret loge literally as ln of measured mole-fraction solubility. Another target is conditional on concrete qualification evidence; no silent target switch. Independent screening precedent check found no conflict. This authorizes qualification and its independent panel, not final inclusion, build or publication.

**Assessment (AI, 2026-11-10):** Actual pinned MixtureSolDB v3 has 175,166 rows and 19 fields (no RecordID); canonical molecular/PEG-grade identities reproduce 750 pairs and 3,001 systems. Curated ln mole-fraction task has 167,112 measurements, 810 solutes and 606 scaffold/identity families. Typed structures replace the older descriptor-shipping suggestion; BigSolDB remains a distinct task, with related links retained in the historical screening text rather than this record's source_links. Exact delivered input+ln-target copies are removed, including negligible machine-decimal tails; distinct delivered labels remain. A source-supported 110-row dapsone solvent-identity repair preserves targets and is documented with original-SI access limits. Twenty-two rows from DOI 10.1021/je3009842 retain unresolved composition mapping pending added review; not every residual conflict is laboratory noise. BigSolDB repeatability is not a measured MixtureSolDB noise floor, and cross-compilation row overlap is unmeasured. Strict train-only LightGBM qualification on all nine current folds gives mean RMSE 2.049564 ln units versus 2.715437 for full-training mean, better 9/9; model training capped at 50,000 rows/fold, full held-out scoring. This is diagnostic evidence, not a tuned leaderboard or final inclusion.

**Assessment (AI, 2026-11-10):** review panel (full): ship after documentation changes and ordinary curator review; disputed: retain 22 unresolved source-composition rows or hold inclusion (PROV-13, EV-7); for the curator: issues 1-2, including explicit PEG-grade representation warnings (CLEAN-24). The documentation changes, source/record reconciliation and final no-fit model-evidence reuse proof are complete; neither inclusion nor warning acceptance is inferred. Priority 2: gap 0 (159 accepted-definition metadata snapshot: chemistry/regression/grouped not thin), use case 0 (approximate literature-to-deployment fit), source + (traceable measured data and paper), shape + (167,112 rows, nine inputs and grouped structure), risk - (unresolved 22-row composition mapping). Independent blind and task-gaming reviews tested the repaired table; no demonstrated exploit.

**Assessment (AI, 2026-11-10):** Official Zenodo versions metadata confirms first release 17846307 on 2025-12-07, followed by 18234735 on 2026-01-13 and selected v3 18660057 on 2026-02-16. Correct the dataset year to 2025 under PROV-9; the 2026 paper citation and selected data bytes remain unchanged. This is provenance metadata, not a target, cohort or split change.

CC (2026-11-10, Myunghwan): Remove the 22 composition-uncertain nominal propylene-glycol/water source rows (10.1021/je3009842) and restrict to molecular solvents, excluding active-polymer conditions. "Remove them for these reasons and do the rest of [tabarena-review-added-datasets]." Original words and snapshot-bound issue marks are preserved in the local review store. No guessed solvent correction or target change.

**Assessment (AI, 2026-11-10):** The source filter protects planned-input fidelity after bounded origin retrieval could not resolve the mapping (PROV-13, USE-6/8). Polymer measurements remain scientifically valid but outside this curator-selected molecular-solvent task population (USE-1); retain molecular pure endpoints even if an unused zero-share component was PEG. Remove now-constant polymer-grade predictors (CLEAN-5). Requalify changed data and all nine folds; previous predictions are historical and not reused. Independent precedent review retained with application evidence.

**Exception to CLEAN-11 (2026-11-10, Myunghwan):** Exclude the 22 composition-uncertain nominal propylene-glycol/water observations from 10.1021/je3009842: internal endpoint comparisons show their inputs may name the wrong mixture, and bounded origin retrieval did not recover a faithful mapping. Serves P3 (USE-6/8) and P5 (PROV-13): the task needs known planned mixture identities. This is a bounded provenance remedy, not target-outlier trimming or a general missing-row policy. The separate PEG exclusion is the explicitly selected molecular-solvent task population, not invalid-measurement removal.

**Assessment (AI, 2026-11-10):** Added-review priority recomputed to 3: base1 + documented first-publisher source1 + measured shape1; gap0 and source-named direct use-case0. The specific open 22-row issue has been remedied by the curator-selected exclusion; generic source-selection and missing-context limitations remain explicit. Prior priority2 and scores are historical.

**Assessment (AI, 2026-11-10):** review panel (focused): ship recommendation after the specified exclusions and completed fresh qualification; disputed: none requiring another issue; for the curator: final ship verdict and declared RMSE-on-ln metric check. Independent claim/column reconstruction confirms 165,781 rows, 810 solutes, 606 families and seven inputs; all nine new folds separate tested identities. Fresh strict training-only fixed LightGBM mean ln-RMSE2.022544 versus full-training mean2.709111 (9/9 better), train cap50,000/full held-out scoring; dependent folds. Native task/leak/dtype/group probes complete with disclosed caps and preprocessing caveats. The tiny17-family group diagnostic is not the full606-family task.0check errors/0warnings; residual82same-inputgroups exceed tenfold with unverified cause. Participant artifacts were reconciled after obsolete writers; no tested useful shortcut. Cold-editor corrections mark both original discussions historical and resolved. Original full panel and old model evidence stay historical; no curator ship/metric mark, build, commit or publication inferred.

CC (2026-11-11, Myunghwan): "yes, ship this. run [tabarena-build-commit]." Accept the reviewed molecular-solvent natural-log mole-fraction regression, with RMSE directly on ln values and whole-solute-family holdout, including the documented limitations. Authorize this dataset's build and commits. Earlier exclusions remain settled. No push, pull request or merge was requested.

**Assessment (AI, 2026-11-11):** Final ship and declared metric check accepted in direct response to the completed package. Independent precedent check found no genuine new rule departure or reflection requirement. Preserve original review snapshot and human marks, issue history, ownership and source evidence; build verification follows without changing the accepted scientific task.

CC (2026-11-11, Myunghwan): the declared metric rmse, scored directly on ln mole-fraction solubility with identity transformation, is checked. Accepted with the final ship approval.


**Assessment (AI, 2026-11-12):** Requested build completed locally: format2 container `01a1d1d6-f565-7392-ad66-859abfb1d4c5`, checksum `v2:e24d51cb9402a5fa6b3281c88ae31c49f40dcdad6a740ba37d1807b05def1069`, 165,781 rows and seven predictors, all nine approved family-held-out folds unchanged. Zero build errors/warnings; saved reload and traced-input checksum reproduction passed from one 41,107,737-byte CSV. Exact row/target/feature/fold/scorer comparison preserves the accepted qualification; no new model fit or scientific decision required. Raw backup remains local. Definitions and verified build documentation committed on the isolated branch; no push, PR or merge. Retain Myunghwan ownership until main integration.

**Assessment (AI, 2026-11-12):** Prepared an independent draft PR against main for the accepted MixtureSolDB task. Migrate equivalent provenance fields to Source metadata and preserve the complete settled review in this record. Under the current framework, complete rows, targets, all seven inputs, all nine ordered folds and the native ln-RMSE scorer exactly match accepted qualification. Build again from the new isolated clean definition revision so its source is reachable in this PR; the earlier verified branch and build remain historical. Retain official ownership and its existing stage until main integration.

**Assessment (AI, 2026-11-12):** Rebuilt the isolated current-main-compatible package as format2 UUID `01a1d1f0-286b-7e20-8dc4-5c1d644767bc`, checksum `v2:0626ceb07c13ab2449c16f6f5daae3d8564ac5b21de738142da9074374f2b729`, from clean source `a6e54dba6f24a54446b7619d0b83cbb98264a3f6`. Saved reload and reproduction from the same sole traced CSV pass with zero errors/warnings. Provenance/container metadata changes the checksum; complete approved scientific rows, targets, seven inputs, all nine train/test memberships and ln-RMSE scoring remain exact. Current-source tests:2,523 passed/304 skipped;188 definitions import; record validation and pointers pass. No new model fit or scientific choice. Earlier builds and source branches remain historical; no unrelated batch dependency.

## Review

**Outcome:** added; specified review changes applied and freshly qualified. MixtureSolDB predicts natural-log mole-fraction solubility for molecular solvents. Myunghwan settled issues 1 and 2 by selecting the bounded source-row exclusion and molecular-only population. Myunghwan accepted the final task and declared RMSE-on-ln metric on 2026-11-11 and explicitly requested build and commit; the requested local build now passes saved reload, checksum and traced-input reproduction with no new scientific issue. Build identity is in the generated README and CHANGELOG.

**Main points:** Final acceptance: Myunghwan, 2026-11-11, "yes, ship this. run [tabarena-build-commit]." Both exclusions remain settled. 165,781 measurements, 810 solutes, 606 chemical families and seven planning-time inputs. Exactly 22 composition-uncertain source rows and 1,309 active-polymer observations leave the prior curated population; all solutes and families remain. Keep molecular pure endpoints even when their unused source component was PEG. The selected scope excludes valid polymer measurements; it does not prove their targets invalid.

**Record judgment:** Useful approximate experimental property prediction, first released in 2025, using pinned MixtureSolDB v3. One row is a published solute/solvent-composition/temperature observation. Predict before measurement from three typed molecular structures, temperature, two initial solvent fractions and their mass-or-mole basis. RMSE directly scores ln(mole fraction), with identity scorer transformation. All nine newly generated folds hold out entire chemical families and separate the tested chemical identities; recurring solvents and related analogs remain possible. Fresh fixed LightGBM qualification with training-only preprocessing and 50,000 training rows per fold scores every held-out row: mean RMSE 2.022544 versus 2.709111 for the full-training mean, better on all nine folds. Repeated folds are dependent. Bundle checks: 0 errors and 0 warnings. Source selection, unrecorded method/polymorph state and 82 same-input groups with over-tenfold target disagreement remain limitations with unverified causes; they are not established laboratory noise or proof all source errors were removed.

**Issues:**

1. **[Resolved] Retain the unresolved solvent-composition rows, or hold inclusion for the source table?**

   - **Problem:** Twenty-two source rows for diazepam and clonazepam have internally inconsistent solvent-composition mappings, and the exact correction is not established[^source].
   - **Background:** In DOI 10.1021/je3009842, both nominal propylene-glycol/water series end at exactly the same values as the corresponding PEG-200/water series, while their nominal water endpoints disagree by hundreds to thousands fold.
   - **Effect on the task:** Wrong mixture identities would associate valid measured outcomes with the wrong planned conditions; switching the solubility target would not repair those inputs.
   - **Experiments:** The bounded audit compared all 44 rows from that source: 22 suspect rows and 22 comparison rows at 298.2 K; the NIST page verifies the source and PEG-200/propylene-glycol/water scope, but numeric retrieval returned HTTP 403 and no primary mixture table was recovered.
   - **Consistency:** The separate 110-row dapsone identity error was repaired from corroborated source descriptions and ten exact endpoint matches; these rows lack equally decisive mapping evidence, so no correction, exclusion or outcome averaging is invented.
   - **Panel:** The advocate favors retaining the explicit uncertainty, while the critic prefers holding inclusion for the primary table; both agree this belongs in the ordinary added review and is not a reason to change the approved target.
   - **Unknown:** The original article's mixture table or supporting information, or an author correction, would establish the intended pair and fraction basis; other residual conflicts cannot all be called laboratory noise.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Retain with stated uncertainty (implemented before this review) | Keep the current table and approximate-fit limits | Preserves the published cohort without an invented correction | Some predictions may be scored against wrong composition inputs |
     | b | Hold inclusion for primary evidence | Preserve the implemented candidate while obtaining the original mixture table | Enables a source-backed repair | Inclusion remains pending source access |

   - **Recommendation:** a is the advocate's recommendation and b the critic's; the mediator leaves this weighing call to Myunghwan. **Original decision prompt (settled below):** retain the documented uncertainty, or hold inclusion?

   **Notes for the AI:** Preserve the original raw bytes and all actual curator words. A source-backed repair must specify a bounded predicate, retain the source evidence, regenerate the table, checks and kits, rerun affected model qualification and independent review, and reconcile changed row/fold identities. Holding inclusion is not a rejection or a new verdict enum. No guessed solvent swap or blanket source exclusion is authorized by the current implementation.

   [^source]: PROV-13 (Must) requires repair from the origin when available; EV-1/2/7 distinguish measured inconsistency from an unverified repair, while USE-8 requires the known fit gap to remain explicit. Primary source identity and scope: https://trc.nist.gov/ThermoML/10.1021/je3009842.html . The supported dapsone repair is documented in dataset.py with https://doi.org/10.1016/j.molliq.2021.118223 and https://doi.org/10.3390/molecules29081743 ; its original experimental SI remains unrecovered.

   **Myunghwan (2026-11-10, change):** "Remove them for these reasons and do the rest of [tabarena-review-added-datasets]." This issue's referent is the 22 suspect source rows.

   **Resolved (2026-11-10, Myunghwan):** Exclude exactly the 22 nominal propylene-glycol/water rows of DOI 10.1021/je3009842; preserve source bytes and historical evidence. No guessed replacement composition.

2. **[Resolved] Keep the measured polymer-solvent conditions with grade identities?**

   - **Problem:** PEG solvent grades are polydisperse materials without a single exact molecular structure, so 1,309 curated rows have missing solvent SMILES despite known grade identities[^polymer].
   - **Effect on the task:** The implemented task includes polymer solvents through explicit source-named categories, while molecular solvents use typed structures; this is a representation limit rather than an unknown solvent.
   - **Experiments:** All observed molecular strings parse; missing entries are confined to the five source grades; the two native warnings count 128 missing first-slot structures and 1,309 missing second-slot structures, including duplicated active-solvent slots at pure endpoints.
   - **Consistency:** Keep complete source identities and the benchmark's typed-structure convention; do not invent a single oligomer or discard an entire valid measurement cohort merely because a polymer has no unique SMILES.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep grade identities (implemented before this review) | Retain polymer conditions and accept the explained structure warnings | Preserves measured conditions and planning-time grade information | Default molecular encoding cannot describe chain-length distributions |
     | b | Restrict to molecular solvents | Remove conditions with active polymer grades and requalify | Every active solvent has an exact molecular graph | Narrows the source population and loses valid measurements |

   - **Recommendation:** a. **Original decision prompt (settled below):** keep the grade-based representation and accept its warnings, or request the narrower cohort?

   **Notes for the AI:** If accepted, the proposed accepted_check_warnings entry is dataset_smiles_column: 'The 1,309 affected conditions contain source-named polydisperse PEG grades, not unidentified solvents; exact molecular SMILES do not exist for these grades. Preserve the five categorical grades and measured rows; 128 pure-polymer conditions occupy both normalized slots.' It covers both warnings with that slug. Leave accepted_check_warnings empty until the curator explicitly decides. A narrower cohort changes rows and folds and requires affected requalification before returning.

   [^polymer]: CLEAN-10/24 govern proxy missing structures and typed molecular inputs; USE-6/7 distinguish a known polymer grade from a missing required identity. See the release https://zenodo.org/records/18660057 and the source paper https://doi.org/10.1038/s41597-026-07047-z .

   **Myunghwan (2026-11-10, change):** "Remove them for these reasons and do the rest of [tabarena-review-added-datasets]." This issue's referent is the active-polymer cohort.

   **Resolved (2026-11-10, Myunghwan):** Restrict to molecular solvents, excluding 1,309 prior curated active-polymer conditions; retain normalized pure molecular endpoints and remove constant grade fields. PEG measurements are valid outside this chosen population.

**Review panel:** ship (focused mediator); specified changes and affected qualification complete. Roles: claim and column audits by one independent investigator, separate split auditor with fresh strict qualification, participant task gamer, decision precedent checker, mediator and cold editor. Earlier full-panel reports remain historical below. No new blind run or advocate/critic debate was required for this focused response to settled review marks. Previous models were not reused after the population change; independent full-frame, feature, target, scorer and all-nine-fold equality proofs link final prose-only edits to the fresh saved models. Native task/leak/group diagnostics retain their explicit smaller row caps and stock full-frame-median caveat; strict training-only qualification supplies the principal signal evidence.

<details><summary>Current mediator</summary>

**Focused mediator judgment — MixtureSolDB molecular-solvent cohort**

2026-11-10 UTC. Independent mediation of the focused claim, column, split/model, precedent and participant reports. Canonical files read only; no source retrieval, model fitting, control-plane operation or curator mark by this role. Current definition SHA256 `1afcc88fda4768245307de6258fa780594de03f609987a989bcd8ec76f1c1d04`.

**Recommendation: ship the changed definition, subject to the curator's final added-review and metric decision.** No new numbered scientific issue is warranted by the completed focused evidence. This is an agent recommendation, not a human ship mark, build or repository-integration authorization. The curator's two exclusions are settled and faithfully implemented; do not ask for them again.

Validity: the measured pre-laboratory property task remains supported (SEL-3, USE-1/3/5/6); its scope is now explicitly molecular solvents and its fit remains approximate (USE-8). The source-specific uncertain mixture inputs leave under a bounded, documented CLEAN-11 exception serving P3/P5; no guessed composition repair is introduced (PROV-13). Exact inputs and all tested chemical identity keys remain separated by the actual grouped folds (LEAK-16, SPLIT-31). Value: fresh training-only model qualification shows useful signal on all nine actual folds, and native task diagnostics flag none (TP-2, SPLIT-28). Quality: valid PEG measurements leave only under the selected population, normalized molecular endpoints survive, constant grade fields are removed, and distinct measured outcomes are not averaged (CLEAN-1/5/11/24). Weighed: traceable publisher and broad molecular support favor inclusion; retrospective selection, incomplete experimental context and residual contradictory outcomes limit transport to a new laboratory.

**Agreed facts and completed follow-through**

- Myunghwan's exact original words and snapshot-bound `changes` marks are preserved. The independent precedent check found no same-facts opposite precedent, unexplained Should departure or third same-reason exception requiring another reflection. The source-row exception is written in the definition, record and owning Cases table; the pinned instruction source was not amended.
- Independent full-row reconstruction verifies exactly 22 source-row and 1,309 active-polymer exclusions, disjoint. These remove 1,331 of the previous 167,112 curated observations (0.7965%); the current table has **165,781 observations, 810 exact solutes, 606 families and seven predictors**. Every surviving input, ln target and family assignment equals the prior table after precisely those filters and removal of the constant grade columns. The separate 110-row dapsone identity correction remains bounded and unchanged; its original experimental SI remains unrecovered, as previously disclosed.
- PEG grades are valid measured conditions outside this curator-selected molecular-solvent task, rather than impossible targets or unidentified planning inputs. Endpoint normalization precedes the molecular filter: all intended molecular endpoints with unused zero-share PEG remain. The current table contains 20,684 pure molecular observations. No solute/family disappears.
- The short question, row and known-input fields now explicitly state molecular solvents. All three molecular structures are complete and parse; temperature, initial fractions and mass-or-mole basis have appropriate timing and types. Alternative solubilities, source DOI, names and identifiers remain excluded from predictors. Native check runs 27 checks with **zero errors and zero warnings**; its conflicting-outcome information is retained. The dtype probe has zero flags among its four inspected ordinary columns; the structure audits separately cover the typed SMILES.
- All nine freshly generated folds hold out 202 families and 51,044–58,374 observations each. Exact solutes, exact delivered-input hashes, declared families and eight independently reconstructed representation/parent/tautomer identity keys have zero cross-fold intersections. The scorer matches direct RMSE of ln targets, with identity transformation, perfect score0 and +1ln-unit error1 on every fold (MET-2/3/11).
- Fresh fixed200-tree LightGBM, train cap50,000/fold, train-only constant masks/medians/categories and full held-out scoring: mean ln-RMSE **2.022544 versus 2.709111** for each fold's full-training mean; better **9/9**, range1.848733–2.235301. Supplemental mean family RMSE is1.843259 versus2.538328; the objective remains per row. Saved indices/truth/scores, selected preprocessing statistics and reloaded model predictions were checked. A separate exact AST/frame/target/features/scorer/fold/hash bridge reconciles final prose-only edits to fit source `f6e6b3e54528b2cb0a28ffe9ca076683d1d2a507d45a56fe5552856f6b8ef4d3`; original manifests are unchanged. No previous-cohort prediction was reused.
- All four new native diagnostics completed successfully. The five-fold task diagnostic gives LightGBM RMSE1.998561 versus dummy2.727710 and flags[]; leakage diagnostics count zero exact copies across all nine complete folds; three model-probed folds and single-feature tests retain their stated caps. These helper model scores use full-frame median imputation and are supplemental; they do not replace the strict training-only study.

**Disputed or adverse diagnostic evidence, settled by its actual scope**

The native group diagnostic uses only **3,346 rows from 17 families**, one repeat/three folds. Its IID R²0.989 versus grouped R²-16.792±23.660 is adverse on that tiny subset. Its separate learnability scores are ridge0.091, random forest-0.106, LightGBM-0.092 and kNN-0.660. There is no applicable group-label permutation for this per-sample-label task. Preserve these results; do not report them as a clean whole-task learnability test. The decisive qualification for the delivered task is the new actual606-family/nine-fold study with full held-out rows and useful signal on every fold. SPLIT-4 keeps the split aligned to unseen families regardless of the IID advantage; SPLIT-27/28 and EV-2/8 require comparing the appropriate task and support, rather than extrapolating one small subset or hiding its failure.

The participant found **no tested predictive shortcut improving its honest comparator** on the nine delivered folds. Its fixed descriptor baseline averages RMSE2.076123 versus the same training-mean baseline2.709111. Row augmentation gains0 on all folds; row-only trees, nearest-row labels and interpolation are worse. Exact/canonical full-input and raw/canonical/nonstereochemical full-solute lookups have zero held-out coverage. This supports the tested defenses, not absence of every possible leak (LEAK-10/16, EV-6/7).

One aggressive largest-fragment/neutral/nonstereo lookup shares the tartaric-acid key on four folds, covering72 or135 test rows, and worsens all four affected scores. Independent raw-name/full-structure inspection identifies **L-tartaric acid** versus **(1R,2R)-(+)-1,2-diaminocyclohexane L-tartrate**. The key drops the diamine and substitutes its organic counterion for the entire solute; this is not equality of the shipped solutes or demonstrated recurrence of one active core. Do not impose a blanket largest-fragment regrouping. `fragment-key-adjudication.json` and its script retain the decisive identity evidence; the worsened scores are supporting context, not the sole reason this is not a demonstrated leak (SPLIT-31, CLEAN-24, EV-6).

Directly reading delivered held-out targets gives zero RMSE, as it would in an offline evaluation kit containing truth. It is an explicit forbidden control, not a predictive input defect. Benchmark execution must maintain its train-label-only contract; this does not create a dataset-specific exclusion issue. External lookup, elaborate similarity attacks and indirect cross-fold label access were not exhaustively tested.

The participant's two obsolete host processes survived outer tool termination and later overwrote partial JSON/report files. The race was detected, original bytes preserved, exact obsolete writers stopped, and current all-nine CSV/membership/saved-baseline predictions reconciled. All nine baseline arrays rescore to CSV within1e-12 and current input hashes match. Attack scores retain the complete-run CSV provenance; attack prediction vectors were not saved, so do not claim their independent vector replay. The current final stability receipt reports no exact-kit writers. This evidence correction is complete and does not warrant rerunning already verified model qualification.

**Remaining limitations and curator boundary**

The exclusions do not certify every remaining extraction. There are82same-input groups/190rows with over-tenfold outcome spread, and1,438same-input groups with distinct measured outcomes; causes are unverified. Do not call all of them laboratory noise or invent averages. Missing polymorph/method context, retrospective literature sampling, possible overlap with older compilations and residual close analogs remain explicit approximate-fit limits (USE-8, PROV-4/7, EV-7). The model evidence does not establish chronological validity, unseen-solvent generalization or prospective laboratory accuracy. Repeated folds share families and are not nine independent experiments.

This is a **focused** re-check. Claim and column roles share one independent investigator; split/model qualification, precedent checking, participant gaming and mediation use separate contexts. No new full debate or blind-review claim is made; the original full-panel history remains historical, with unchanged source evidence distinguished from the fresh cohort evidence. Root must preserve resolved issue IDs/history, update current summary/record/changelog/review snapshot, and have the required independent editor check that package. Those are normal follow-through, not reasons to reopen the exclusions.

The supported runtime suite passed2,014tests with285skipped. The owning checkout's broader tests cannot collect under the pin because unchanged tests require later RowBudget/row_table APIs; this is a disclosed runtime-version limit, not a claim that the entire owning checkout suite passed. Record/pointer validation and changed-source lint results remain root-owned evidence.

After that packaging/editor follow-through, the remaining human action is final acceptance of this concrete task and its declared fallback RMSE directly on ln mole fraction. No additional scientific exception or new numbered issue is indicated. Preserve the actual existing `changes` input rather than inventing a fresh `ship` or metric mark; build, commit, push and publication require their explicit scope.

</details>

<details><summary>Current claim audit</summary>

**Focused independent claim audit — MixtureSolDB review changes**

2026-11-10 UTC. Audited functional definition SHA256 `f6e6b3e54528b2cb0a28ffe9ca076683d1d2a507d45a56fe5552856f6b8ef4d3`. Read-only on canonical files. This is the focused claim-auditor role, with independent raw reconstruction and exact prior-frame comparisons; it does not replace the prior full panel or infer a curator ship mark. `audit.py` and `audit.json` retain the executed tests. Threads capped at two.

**Verdict: changed-data claims hold; complete the small scope/exception documentation follow-through.** Exactly 22 composition-uncertain source rows and 1,309 active-polymer curated rows leave, with no overlap. The final table has **165,781 rows, 810 exact solutes, 606 families and seven predictors**. The exclusions leave the approved target and all surviving delivered physical-input values unchanged. Previous model scores do not qualify the changed folds; root/split roles are rerunning them independently.

| Claim and source | Refutation test actually run | Result and evidence | Rule |
|---|---|---|---|
| Pinned release unchanged (`RAW_SHA256`, download notes) | Hash actual source file and read dimensions | Holds: SHA256 `be72940b1d9ba03eacf142cfb26e774b658617dbf8fefb3cfb96f27c4da5e51d`,175166x19 | PROV-8/13,EV-2 |
| Sole target is natural log of primary measured mole fraction (summary/comments) | Every retained source index against direct `np.log(raw primary)` | Exact array equality, finite -21.416413 to -0.056147 | USE-5,MET-3,LEAK-10 |
| No alternate target/model-score selection (comments) | Compare old/new target construction and exact complete surviving frame | Holds for this change; no target branch or alternate outcome predictor | USE-5,CLEAN-6 |
| Exactly22 suspect source rows excluded (new CC/comment/code) | Independently predicate DOI+PG+water, compare retained source indices |22 raw and prior curated rows; none retained | PROV-13,EV-6 |
| No guessed composition replacement (new comment) | Compare every surviving input to old complete table and independent raw reconstruction | Exact equality; no new replacement (the prior110-row dapsone correction remains) | PROV-13/14,CLEAN-1 |
| Exactly1309 active-polymer prior observations excluded (new CC/comments) | Missing active-solvent structures after independent endpoint normalization, prior-row accounting |1309; disjoint from22;165781 total | USE-1/6,EV-2 |
| Molecular endpoints with unused zero-share PEG remain (new comment) | Source zero-share PEG predicate, canonical delivered-key coverage |139 source rows;92 prior retained source indices; all corresponding prior delivered keys remain | USE-1/6,LEAK-19 |
| No unrequested rows removed (new implementation implication) | Current full frame vs old full frame filtered by precisely the two exclusions and grade drop | Exact `assert_frame_equal`, including source indices and grouping | CLEAN-11,EV-6 |
| Raw lineage faithful after both exclusions | Independently reconstruct corrected raw fields, canonicalization, solvent exchange, pure normalization, target, molecular filter and delivered dedup | Exact frame equality for every non-group column | PROV-13,CLEAN-1,EV-6 |
|810solutes/606families preserved (new comments) | Counts and exact per-row family match to prior | Holds; no solute removed, current grouping assignments unchanged | SPLIT-31,EV-2 |
| Now-constant grade features removed (new comment) | Delivered schema and `_feature_types` | Both grade fields absent; seven predictors remain | CLEAN-5 |
| All three structures ship typed/canonical and complete (comments/special_features) | Distinct-value parsing and dtype/spec inspection |810/127/128 distinct values;0missing,0parse failures | CLEAN-9/24 |
| Input-only planned conditions; other outcomes/IDs removed (summary/comments) | Complete seven-column input list and row reconstruction |3structures,temp,2fractions,basis; no alternate solubility,FDA,DOI,names,CAS,CID,endpoint flag | USE-3/6,LEAK-10 |
| Solvent order and proportions exchange together (comments) | Independent swapped reconstruction across complete table | Holds, including repaired dapsone and pure endpoints | CLEAN-1/14 |
| Pure endpoints use only active solvent and a standard convention (comments) | Independent normalization and delivered table constraints |20684 current pure molecular rows; duplicate structures,1/0,mole | USE-6,LEAK-19 |
| Delivered-input+ln-target dedup only, no averaging (comments) | Independent complete-frame reconstruction; surviving target exact source | Holds;1438 identical-input groups retain distinct outcomes | LEAK-16/19 |
| Prior110-row dapsone repair remains bounded (comments) | Independent source predicate and corrected complete-frame reconstruction | Predicate110; correction only second solvent identity; targets/settings unchanged | PROV-13/14,EV-6 |
| Molecular cohort includes valid PEG exclusions, not invalid targets (new comments) | Inspect decision rationale and actual filter | Holds; filter uses active structure missingness after normalization, not target tails/performance | USE-1,CLEAN-11 |
| RMSE directly scores ln, identity transformation (metric) | Inspect exact unchanged declared Metric object | Fallback,`target_transform='identity'`,no scoring-only inputs | MET-2/3 |
| Every current fold separates chemical families and metric executable | Focused split auditor separately runs complete-fold/scorer tests | Not re-derived by this role; consume that fresh report before readiness | SPLIT-31,MET-2,EV-7 |
| Source defines no deliberate model metric, firstrelease2025,CCBY4,litperiod/atmospheric/noadditives (unchanged provenance comments) | Compare old/current claim text and retained prior full-panel/metadata artifacts | Unchanged source evidence, not independently re-fetched/re-read in this focused pass. Prior full source audit remains evidence; new cohort does not establish these source facts | PROV-9/10/16,EV-7 |
| Original numeric mixture table unrecovered,22inputmapping uncertain (comments) | Inspect retained retrieval/source audit and uncertainty wording | Not newly resolved; exclusion avoids scoring those inputs but does not prove a corrected mapping or wrong measured target | PROV-13,EV-7 |
| Remaining contradictory outcomes are not all known lab noise (comments) | Recount same-input target ranges |82groups/190rows have >10fold outcome spread; max551.639fold; cause not established | USE-8,EV-6/7 |
| No prospective or exhaustive chemistry guarantee (fit/split comments) | Inspect known method/polymorph gaps and unchanged split contract | Appropriately approximate; molecular-only does not resolve these gaps | USE-8,EV-7 |

**Documentation follow-through**

1. The current `TaskSummary.changes` and comments explicitly select molecular solvents, but the question and row are generic. Add “molecular solvents” to those short consumer-facing fields so the narrowed population is visible without reading the cleaning notes (USE-1/8). This is scope clarification, not a further population choice.
2. Record a bounded `Exception to CLEAN-11 (2026-11-10, Myunghwan)` for the source-row exclusion if applying the broad retention default; explicitly name unresolved composition identity, attempted origin recovery, no invented correction, and higher P3/P5 fidelity rationale. The analogous `clock_protein_toxicity` exception is closer than generic missing-value deletion. Preserve the source-selected molecular population rationale separately: known PEG grades are valid measurements outside this chosen population, not proof of no-task rows under USE-7. The independent precedent report found no need to ask Myunghwan again. Canonical exception text belongs in the record, definition notes and owning checkout's Cases table; do not edit the pinned instruction source.
3. Mark previous models/reports and old167112-count summaries historical. New native and strict-model qualification must complete before current readiness is stated. After metadata-only wording edits, reconcile the exact new definition identity and prove frame/folds/features/scorer unchanged before reusing fresh model predictions.

No canonical file, raw data, claim board or control plane was modified by this role. No model fit, full-fold scorer execution, network source retrieval or cross-compilation overlap audit was performed here. The combined exclusions account for1331rows (0.7965% of the prior table); they do not certify all remaining extraction metadata. Build, commit, publication and ship remain outside this role's authority.

</details>

<details><summary>Current column audit</summary>

**Focused independent column audit — MixtureSolDB molecular-solvent cohort**

2026-11-10 UTC. Audited functional definition SHA256 `f6e6b3e54528b2cb0a28ffe9ca076683d1d2a507d45a56fe5552856f6b8ef4d3`. Canonical files were read only. `check_structures.py` and `measurements.json`, together with the separately documented claim-role raw reconstruction (`../claim-auditor/audit.py`), retain reproducible evidence. These two focused roles share the same independent investigator; they are not two independent votes.

**Verdict: seven input columns have appropriate timing and cleaning.** There is no tested post-outcome input or outcome-derived proxy. The curator-selected molecular population retains165781rows,810solutes and606families. Both grade fields become constant in this population and are removed; no replacement features are invented. The task still predicts natural-log mole-fraction solubility before measurement for unseen solute families. The prior full-panel/source interpretation remains applicable to unchanged field meanings; this pass verifies the changed cohort and representations, not every source experiment.

| Column | Meaning and timing | Dtype/cleaning actually checked | Verdict | Rule |
|---|---|---|---|---|
| SMILES_Solute | Planned entire solute structure; known before measurement | Typed canonical SMILES/string;810distinct;0missing,0parsefailures; exact surviving values equal prior | Fine | USE-3/6,CLEAN-9/24 |
| SMILES_Solvent1 | First normalized planned molecular solvent | Typed canonical SMILES/string;127distinct;0missing,0parsefailures; exchanged with own fraction | Fine | USE-6,CLEAN-14/24 |
| SMILES_Solvent2 | Second normalized planned molecular solvent, duplicate active solvent at pure endpoint | Typed canonical SMILES/string;128distinct;0missing,0parsefailures; unused source PEG does not remove pure molecular rows | Fine | USE-6,CLEAN-14/24 |
| Temperature_K | Planned temperature in kelvin, before solubility measurement | Float64;2459distinct;finite,252.55–383.15K;positive | Fine | USE-6,CLEAN-14 |
| Fraction_Solvent1 | Planned first solvent's initial proportion | Float64;5691distinct;finite,[0,1];exchanged with solvent identity | Fine | USE-6,CLEAN-14 |
| Fraction_Solvent2 | Planned second solvent's initial proportion | Float64;5578distinct;finite,[0,1];sums to1with first. Complement is not an exact duplicate column | Fine | USE-6,CLEAN-5/14 |
| Fraction_Type | Whether proportions are mass or mole fractions | Declared unordered category;89686mole/76095mass rows;pure molecular endpoints normalized to mole | Fine;mass0.5 is not mole0.5 | CLEAN-14 |
| ln_solubility_mole_fraction | Measured solute mole-fraction outcome, transformed by natural log | Float64;55737distinct;finite;exact source-ln equality at every retained raw index;sole target,not predictor | Fine | USE-5,LEAK-10,MET-3 |
| solute_family | Split-only connected structural-family identifier | Declared string metadata;606values;exact prior group assignment for every retained row;not a predictor | Fine for its role;fresh split audit determines separation | SPLIT-31 |
| Removed PolymerGrade_Solvent1/2 | Source grade identities in broader prior cohort | After active-molecular population choice both are constant molecular;absent from current features | Appropriate removal after narrowing,not loss from surviving inputs | CLEAN-5,USE-1 |

The independent full-row reconstruction preserves the existing110-row dapsone metadata repair, canonical molecular strings, paired solvent/fraction exchange, endpoint normalization, all surviving natural-log outcomes and delivered-space deduplication. Current frame equals precisely the two-filtered prior frame after grade-column removal. All92prior delivered rows retained at a zero-share PEG source index have their delivered keys represented in the final table;139raw zero-share PEG rows existed before deduplication. There are20684current pure molecular observations. Distinct delivered outcomes remain:1438identical-input groups contain multiple outcomes,82of those groups span more than tenfold mole fraction. They are not silently averaged or dropped.

No numeric nonfinite value or full-row duplicate remains. No alternate linear/log solubility,compound name,CAS,CID,FDA,source DOI or endpoint flag becomes a predictor. The source raw sentinel `-` is decoded only during scratch normalization and no missing structure survives this selected cohort. No learned embedding,label statistic or preprocessing over held-out data is added to the definition.

The root is rerunning the native dtype probe; this role inspected all retained values and declared types independently. The earlier helper caveat remains: native task/leak/group helpers perform full-frame median imputation of encoded inputs. Those diagnostic scores must remain labeled supplementary; the split role's new strict training-only model study supplies the relevant model evidence. The molecular cohort removes missing graph values but descriptor transforms can still yield missing numeric descriptors, so this caveat is not automatically eliminated.

Only documentation follow-through is recommended: put the molecular-solvent scope directly into the short question/row fields, and preserve the bounded human decision/exception rationale rather than describing valid PEG measurements as malformed or fundamentally unavailable planning inputs. These are routine implementation notes, not a repeated request for approval. No newly demonstrated column defect requires a further curator choice.

</details>

<details><summary>Current split audit and strict qualification</summary>

**Focused independent split audit — MixtureSolDB**

2026-11-10. Definition SHA256 `f6e6b3e54528b2cb0a28ffe9ca076683d1d2a507d45a56fe5552856f6b8ef4d3`. This report concerns the molecular-solvent cohort after Myunghwan's two exclusions. Prior-cohort evidence remains historical. No canonical curation source, record or README was edited by this role.

**Split verdict:** the changed definition still evaluates row-level natural-log mole-fraction solubility for held-out chemical families. The planned structures, temperature and initial solvent fractions are available before measurement; solvents may recur. This is cold-start chemical generalization, with no chronological or unseen-solvent claim (SPLIT-1/4/23/31, USE-6).

**New independent actual-data tests:**

- The native plan contains 165,781 measurements, all 810 exact solute structures and 606 families. Each of nine folds tests 202 families and 51,044–58,374 rows; the other 404 families are training-only. Each fold has nonconstant finite targets, and all measurements of a solute/family remain on one side.
- Canonical, nonstereochemical, fragment-removed parent, parent InChI, parent tautomer, neutral-parent, neutral-parent tautomer and fragment-parent diagnostic keys independently reconstructed over all 810 solutes have zero cross-family keys. All eight key types have zero cross-fold test-row overlaps. This tests the intended salts/tautomers/representation protection; it does not establish absence of all close chemical analogs.
- Exact delivered-input hashes, exact solute identities and declared family IDs have zero train/test intersections on all nine full folds (LEAK-16, SPLIT-31). The 606-family mapping is unchanged in size; altered row indices are freshly generated.
- The native standard fallback scorer declares RMSE and `target_transform=identity`. On every fold its training-mean score matches direct RMSE of delivered ln targets to less than 1e-12, perfect predictions score 0 and an added ln-unit scores 1 (MET-2/3/11). Thus no inverse-exponential scoring is being applied accidentally.

`audit.py`, `audit.json` and the chemical-key CSVs preserve the independently reconstructed identity checks; `audit_scorer.py` and `measurements.json` preserve exact fold counts, metric tests and input-copy checks. Supplemental stock probes are root-owned and reported separately.

**Fresh model qualification:** all nine newly fitted fixed200-tree LightGBM models beat the corresponding full-training-mean baseline: mean ln-RMSE 2.022544324 versus 2.709111006, range 1.848733319–2.235300708. Training capped at50,000rows/fold; all held-out rows scored; train-only masks/medians/categories. Mean family RMSE 1.843258652 versus 2.538327746. Saved scores/indices/truth, sampled-training medians/categories and reloaded-model predictions were independently verified. No old prediction was reused. See strict-train-only/REPORT.md and manifests for exact settings, hashes and limits (TP-2,SPLIT-28).

**Final documentation reconciliation:** source `1afcc88fda4768245307de6258fa780594de03f609987a989bcd8ec76f1c1d04` changes only allowed prose fields from the fit source. Full executable AST, delivered data/target/features/scorer, all native folds and saved model/prediction hashes were proved unchanged. Fit manifests remain unmodified; the bridge receipt names both source identities. All810solute-to-family assignments also equal the prior qualified mapping exactly, independently compared in family-map-comparison.json.

**Recommendation from this role:** no new split/metric/qualification issue requires curator action. Preserve the chosen molecular-solvent scope and honest approximate-fit limits. The panel recommends; readiness is not a curator ship or build authorization. Nine repeated folds share chemical families and do not support a naive independent-fold confidence interval.

</details>

<details><summary>Current participant task gamer</summary>

**Independent task-gamer assessment**

**Result: no tested label shortcut beats the honest baseline.** This is a fresh inspection of this kit only, without source/curation notes, external data, network calls, or another run's results. All nine shipped splits were evaluated with fixed configurations; no held-out tuning or split selection.

**Task and honest comparator**

The supplied prediction point is before laboratory measurement: choose solvent composition and temperature for a new solute. The target is log mole-fraction solubility; lower RMSE is better. Group labels are excluded from features. The baseline uses temperature, solvent fractions, fraction type, solvent identities, and eight label-independent RDKit descriptors per solute/solvent (molecular weight, logP, TPSA, donor/acceptor counts, rotatable bonds, rings, fraction sp3). A fixed LightGBM fit uses 180 trees, 31 leaves, learning rate 0.05, seed 42 and two threads. Solute identity labels and row identity are excluded from this baseline. It is a bounded comparator, not a claim of optimal chemistry performance.

**Membership and scoring**

165,781 rows; 810 raw solute SMILES; 606 solute families. Each fold contains 404 train and 202 test families. Every split has unique positions, disjoint train/test positions, full row coverage, and zero family overlap. Every repeat tests every row exactly once. There are no missing values or RDKit parse failures. RangeIndex is unique. 3,087 rows participate in duplicate complete feature records in the full data, but none crosses train/test boundaries on any split.

The supplied score() matched direct sqrt(mean squared error) for baseline predictions on every split; a +1 prediction offset scored 1 and aligned reversal of truth/prediction/indices preserved the score. Target transform is identity, prediction unit is row, and no extra scoring columns are used. This verifies the metric, not label secrecy or membership enforcement by the scoring API.

**Fixed attack results**

|Split|Train mean|Honest baseline|Baseline + row|Row-only trees|Nearest row label|Row interpolation|
|---|---:|---:|---:|---:|---:|---:|
|r0f0|2.856742|2.113184|2.113184|2.859213|3.878898|3.436608|
|r0f1|2.601070|2.043238|2.043238|2.603514|3.795657|3.301803|
|r0f2|2.682863|2.041040|2.041040|2.685156|3.810759|3.332566|
|r1f0|2.645423|2.001167|2.001167|2.647443|3.810999|3.324437|
|r1f1|2.808179|2.234311|2.234311|2.810181|3.877721|3.423368|
|r1f2|2.684450|2.007929|2.007929|2.686537|3.806498|3.345368|
|r2f0|2.823301|2.114724|2.114724|2.825710|3.865214|3.420814|
|r2f1|2.507396|1.981844|1.981844|2.510128|3.754331|3.235550|
|r2f2|2.772575|2.147673|2.147673|2.774624|3.865857|3.403053|
|Mean|2.709111|2.076123|2.076123|2.711390|3.829548|3.358174|

Row-position attacks deliberately use information a deployed model would not have: file position, neighboring training labels, or an augmented position feature. Position augmentation improves RMSE by 0.000000 on every fold; position-only attacks are worse. This provides no evidence of exploitable row ordering.

Exact raw-feature lookup, chemistry-canonical feature lookup, raw/canonical solute lookup, and solute lookup after removing stereochemistry all have **zero test coverage on every split**. Consequently their baseline-fallback RMSE is identical to baseline, with zero gain. Canonicalization changes atom serialization, not chemical composition.

A separate largest-fragment + neutralization + stereochemistry-removal lookup covers 135 rows in r1f1/r2f0 and 72 rows in r1f2/r2f1; other folds have zero coverage. The only shared key is tartaric acid. Inspection shows one original solute is tartaric acid and the other contains tartaric acid together with a diamine. This aggressive normalization therefore conflates distinct solute formulations. Its mean-label override worsens all four affected folds (overall mean 2.079960 versus 2.076123 baseline, a 0.003837 increase). It does not establish a same-solute leak.

The numeric inputs show only modest target correlations (temperature 0.13865; solvent1 fraction 0.08831; solvent2 fraction -0.08831). The fixed feature model does not obtain near-perfect predictions. These checks do not establish scientific provenance or prove the fractions were available independently of the measurements.

**Explicit forbidden control and remaining limits**

Reading held-out targets directly from delivered data.parquet gives RMSE 0 on all nine splits. That is a deliberately forbidden control, a 2.076123 apparent gain over baseline, and a general offline-kit exposure. It is not evidence of predictive feature leakage. An evaluation using this kit must enforce its train-label-only contract outside this scorer: score() accepts supplied truth and does not hide test labels.

Untested: outside reference-database joins/publication lookup, original provenance/timestamp availability, source-study duplication, elaborate tautomer or structure-similarity attacks, target-derived significant-digit encodings, larger tuned chemistry models, and indirect access to other folds' labels. Nothing here proves absence of all leakage or an optimal baseline. Repeats share rows and are not nine statistically independent datasets.

**Reproduction and files**

Run work/gamer.py and then work/identity_extension.py with the authorized project .venv/bin/python. All fitting and prediction calls use two threads. The completed fixed all-nine run took 57.3 seconds. Earlier outer tool timeouts/termination did not stop two host-level processes; those obsolete processes later overwrote results.json and the first generated report with partial results. This race was detected at review, all existing bytes were preserved under work/historical_reconcile_20261110, and the two confirmed exact-kit host processes were stopped. work/reconcile.py rebuilt results.json from the all-nine CSV and membership CSV, verified all input hashes, and independently rescored every saved baseline prediction array against its shipped test indices. Attack scores retain the completed-run CSV provenance; only baseline prediction vectors were saved. No model parameters were changed in response to held-out scores.

Artifacts: work/gamer.py, work/identity_extension.py, work/write_report.py, work/results.json (including SHA256 hashes of shipped inputs/scorer), work/scores.csv, work/membership.csv, work/baseline_predictions.npz, work/identity_extension.json, work/extra_audit.json and work/run.log.

</details>

<details><summary>Current precedent check</summary>

**Independent precedent check — MixtureSolDB added review**

Date: 2026-11-10. Role: independent precedent-checker. Canonical files were inspected only; this report does not apply edits or establish a ship verdict.

Actual curator words (Myunghwan): “Remove them for these reasons and do the rest of [tabarena-review-added-datasets]”. The supplied round context identifies both the 22 suspect nominal propylene-glycol/water source rows and the offered molecular-solvent-only cohort (1,309 active-polymer observations). The previous explanation and read-only impact calculation are part of that scoped choice; no general invalid-row policy is inferred.

**Decision assessment**

**Proceed with both settled changes and affected requalification. No repeated curator question is needed on these exclusions.** The reasons and limiting facts distinguish these decisions from blanket missing-value deletion. Preserve the two decisions separately, and do not mark the new package shipped from this report.

1. **Twenty-two source rows:** the proposed predicate is Source=10.1021/je3009842, Solvent1=propylene glycol, Solvent2=water. The two drug series show exact endpoint coincidences with PEG-200 and inconsistent alleged water endpoints. Original numeric tables were sought but not recovered; HTTP403 is an access result, not evidence that the source data are wrong. PROV-13 requires checking the origin and repair when clean data are obtainable; the documented search satisfies the check, while the absence of a known mapping prevents an invented swap. The mild definition-level filter preserves the usable task instead of rejecting the whole compilation. This resembles clock_protein_toxicity’s documented CLEAN-11 exception: source features do not reliably describe the measured object and a faithful reconstruction is unavailable. It differs from gallstone_disease and ordinary impossible-feature precedents, which kept rows after a known recoding or missing-value conversion. These 22 are uncertain composition identities, not proven impossible targets, so do not justify them under CLEAN-15 or call the full source paper invalid.

2. **Active-polymer observations:** explicitly restrict the benchmark population to molecular solvents and state this in the question/row/scope. Known PEG grades remain valid experimental conditions; polydispersity does not make them malformed molecules. CLEAN-10 supports decoding their sentinel, and CLEAN-24 supports typed molecular graphs; neither independently mandates deleting PEG rows. CLEAN-11’s default is to retain rows when an input becomes missing. The distinguishing fact here is Myunghwan’s explicit choice of the offered narrower, structure-defined molecular-solvent task, with its loss of valid measured conditions explained. Record that bounded population decision and its P3 USE-1 rationale, rather than asserting that USE-7 retrospectively proves every PEG observation was never a task row. The old broad task could represent them using grade categories. No model cap, convenience, or performance improvement may be the reason. Pure molecular endpoints with zero share of an unused PEG component must remain. Dropping the now-constant grade features follows CLEAN-5 only after the population choice.

These choices are documented departures from the broad-table retention recommendation, not amendments to the general rules. CLEAN-11 is a Should rule; the exact reasons and higher principles are already supplied in this curator-selected remedy. Preserve the dated curator choice and evidence in definition comments, record CC/Assessment, and resolved issue turns, with a bounded exception note if applying CLEAN-11 to the exclusions. Do not change the clean instruction pin to invent a general polymer rule. No same-facts opposite curator precedent or third same-reason exception was found requiring a reflection prompt. Relevant analogues were assessed on full rule/case text rather than the register’s keyword outcome alone.

**Register and limits**

Generated the pinned decision_register.py against the actual working-copy records and dataset root, and the pinned knowledge tree. Saved the complete output in decision-register-before-application.txt and .json alongside this report. It contains 4,327 collected decisions and 26 candidate flags; flags are not verdicts. Relevant cases include clock_protein_toxicity (2026-11-01 exception), gallstone_disease (2026-10-31 retain/recode), apistox and molecular siblings (2026-11-01 typed SMILES and retained salts), SUPPORT2/ashrae (origin repairs), and coad/corporate_credit_rating (rebuild when damage cannot be kept).

The read-only impact artifact establishes separate exclusions of 22 and 1,309 from 167,112, with all 810 solutes and 606 families preserved independently. Combined expected 165,781 is not independently confirmed by this report; root must verify disjointness, normalization, deduplication, retained endpoints, final counts, folds, input schema and model/probe reruns. Old saved predictions do not qualify the changed table. No final ship, build, commit, push, or claim-stage transition follows automatically from these marks.

</details>

<details><summary>Current cold editor</summary>

**Cold curator-facing editing review**

Read only `REVIEW_draft.md`. No canonical edit, workflow, model, source request or delegation. This is a structural wording review of the supplied draft; the pending final participant/mediator refresh is not treated as a published final verdict.

**One needed change before presentation.**

1. **Make the two settled issues unmistakably historical.** The leading heading “Issues for Myunghwan,” the two imperative question headings, both explicit “Decision” prompts, and “(implemented)” on the old retain options still read as current requests. Dated “Resolved” turns underneath do not fully remove that ambiguity. Preserve the original scientific discussion and actual curator words, but separate their historical status from the applied decision.

   Preserve the collector-compatible heading `**Issues:**`, then insert:

   > Myunghwan settled both choices on 2026-11-10. The original discussions below explain those decisions and are historical; neither exclusion needs another decision.

   Prefix each title with `[Resolved]`; change the superseded `(implemented)` tags to `(implemented before this review)`; and relabel each old `Decision` prompt as `Original decision prompt (settled below)`. Keep the actual curator quotations, dated resolutions and issue IDs intact. Preserve original bytes in `before-REVIEW.md`. This makes the current state explicit while retaining the record's parseable issue contract.

   Keep the existing source uncertainty and valid-polymer limitations. Do not remove evidence explaining the earlier disagreement. Verify that canonical parsing still recognizes both issues as resolved.

**Other judgments**

- The opening is self-contained about the predicted quantity, observation unit, seven planning-time inputs, molecular-solvent scope, held-out families, scorer scale and intended approximate property-prediction use. The two exclusions are substantive scientific decisions, not generic cleaning defaults.
- The draft distinguishes uncertain composition identity from an invalid measured target and valid PEG measurements from the narrower chosen population. It preserves molecular pure endpoints, surviving solutes/families, and the separate bounded dapsone repair.
- Current qualification has the appropriate boundaries: nine changed folds, capped training, full held-out scoring, training-only preprocessing, dependent repeated folds, and stock diagnostic caveats. Positive scores do not certify source correctness, prospective usefulness or exhaustive chemical separation.
- Full earlier reports are clearly labeled historical. Preserve them, including older counts, scores and recommendations within those historical sections; the leading current summary must continue to identify the 165,781-row cohort and fresh results.
- No curator ship verdict or declared-metric approval is invented. The opening explicitly leaves both for the curator. No additional approval gate or reopened target decision is warranted.
- After inserting the promised final mediator/participant reports, reconcile the leading panel summary against those reports and the already-present final documentation-reconciliation result. Wording such as “require a saved full-frame/fold/scorer proof” should become a completed finding only when the final report actually supports it. This is the known pending assembly step, not a second substantive editing finding.

</details>

<details><summary>Historical panel summary, before the exclusions</summary>

**Original recommendation:** ship after changes (mediator), subject to Myunghwan's source-uncertainty and polymer-warning choices. Full tier: seven evidence roles, advocate and critic with one rebuttal each, mediator and cold editor. The source/target, split and participant checks found no demonstrated unresolved exploit. Model evidence is on the final repaired table: the strict train-only check covers all nine folds; stock diagnostics use explicit smaller row caps and full-frame median imputation, so they are supplementary. An independent no-fit audit verified that final documentation and guard-style edits preserve the complete data, target, features, scorer, preprocessing and model identities, all nine folds and saved predictions; the model evidence applies to the final definition without changing fit manifests. Inclusion and build remain human decisions.

</details>


<details><summary>Historical full panel — Mediator</summary>

**Mediator judgment: MixtureSolDB**

2026-11-10 UTC. Independent mediation of the seven evidence roles and the advocate/critic opening briefs and one rebuttal each. Read-only on curation and definitions; no model, source request, claim operation, controller or delegation. Audited functional definition SHA256 `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`.

**Recommendation**

**Ship after changes, conditional on the ordinary added-review source-uncertainty and PEG-warning decisions.** The implemented ln mole-fraction candidate is ready to present at that gate after the documentation/provenance follow-through below. This is a panel recommendation, not inclusion or build authority. Do not switch targets or reopen the curator's approval to investigate this candidate.

Validity: the source supports an experimental property-prediction task (SEL-3); the planned experiment is a real pre-measurement decision with explicitly approximate fit (USE-1/3/5/8). Other measured outcome representations do not enter predictors (LEAK-10). Current identity families and all nine folds pass the tested separation criteria (SPLIT-31). The bounded 110-row solvent correction is independently reconstructed and corroborated; its original-SI limit remains explicit (PROV-13/16, EV-7). A separate 22-row composition uncertainty is unresolved and goes to the curator; the panel does not certify those rows as correct.

Value: strict train-only qualification demonstrates useful signal on all nine actual folds, and the native task diagnostic raises no task flag. No demonstrated target failure, triviality or irreparable Must failure requires rejection or an alternative target (TP-1/2/6). Positive model results do not establish source correctness or override provenance duties.

Quality: preserve named PEG grades, genuine condition-dependent measurements and full molecular structures; do not invent a polymer graph, average outcomes or remove difficult observations. The two missing-structure warnings remain proposed, not accepted. Weighed: source trace and chemical diversity favor pursuit; incomplete experimental context, retrospective selection and the source-specific ambiguity limit readiness and deployment claims.

**Changes to make now without another scientific decision**

1. Complete the short `Grouping.definition` with neutralized-parent/tautomer keys and the six explicit observed-core links already implemented. The longer split notes are accurate, but metadata-only consumers currently receive an incomplete description. This is documentation, not a new grouping policy (SPLIT-31, EV-7).
2. Add the exact DOI `10.1021/je3009842` uncertainty to the definition's notes and human review: 22 nominal propylene-glycol/water rows across diazepam and clonazepam, compared with 22 PEG-200/water rows. Do not call this proven interlaboratory noise or implement the unverified PEG/PG hypothesis. Preserve the 44 observations and the existing primary target until a scientific decision or stronger source evidence changes them (PROV-13, USE-8, EV-1/6/7).
3. Preserve historical screening prose, but append a current factual assessment: actual file is 175,166 by 19 with no RecordID; this payload reproduces 750 pairs/3,001 systems; BigSolDB repeatability is not a MixtureSolDB noise floor; typed structures ship, not preselected descriptors. Keep the stable `bigsoldb_2` identity and remove unrelated single-solvent BigSolDB DOIs from its current source links. Exact older-compilation overlap remains unmeasured (PROV-4/7/8/12/14, CLEAN-24).
4. Finish normal record pointer, validation, changelog and review-package application. Do not infer a curator ship mark, accept warnings, build, commit or publish from this panel.
5. After prose/metadata edits, record the new definition identity, regenerate the native check/README and prove raw inputs, complete delivered frame, target, features, model/preprocessing settings and exact train/test membership unchanged. Reuse the saved models/predictions only after that proof; a factual correction or population/split change instead requires affected requalification. Record final result hashes and the reconciled process/output provenance (EV-7 and the split-change human-review contract).

**Issues for Myunghwan, ranked**

**1. Retain the specific 22-row composition uncertainty or hold inclusion for the original table?**

**Problem and effect.** For each drug in DOI `10.1021/je3009842`, the nominal PG/water series has an alleged pure-water endpoint hundreds or thousands of times above the PEG/water aqueous endpoint, while its alleged pure-PG endpoint equals that drug's PEG endpoint exactly. All 44 source rows are at 298.2 K and mass-based composition; 22 nominal PG/water rows are implicated. This is a concrete same-source mapping concern, not merely generic lab variation. Incorrect mixture inputs would measure extraction error alongside solubility prediction.

**Agreed evidence.** The critic's endpoint observation was independently followed up. NIST identifies the original PEG/PG/water binary/ternary study, but the accessible page does not provide its mixture table. The original ACS page and the bounded NIST numerical retrieval were unavailable; the latter returned HTTP403 with working SSH. Focused official-source/supporting-file searches supplied no usable mixture table. The proposed PEG-200/PG interpretation is plausible, but not established enough to rewrite identities or interior proportions. The wider blind review reports 84 same-input groups with over-tenfold differences; this does not prove all remaining differences share one cause.

| Option | Consequence | Strongest argument | Limitation |
|---|---|---|---|
| Retain as implemented, with this exact uncertainty and approximate fit | Preserve all observations and current qualified definition; no guessed repair or deletion | The primary measured quantity and useful task are sound; the uncertainty is localized and the bounded repair-at-origin search was performed; no replacement has been established | The 22 rows may carry wrong composition metadata; current models cannot certify their truth or the rest of the extraction corpus |
| Hold inclusion until the original mixture table or authoritative author evidence resolves the series | Preserve current work and evidence, but do not include yet | The critic prefers stronger input/source fidelity before inclusion | Access may delay an otherwise useful candidate; the missing table does not itself prove an irreparable dataset-wide failure |

**Mediation.** This is a genuine weighing call left to Myunghwan, not settled by panel votes. The advocate favors retained, explicit uncertainty; the critic conservatively favors waiting. PROV-13's source-repair duty has been pursued; its source-unavailable limit and USE-8 permit a transparent keep-or-hold judgment rather than fictional verification. Dataset size or good RMSE cannot override a demonstrated Must violation; no such irreparable violation has been established here. Do not add an automatic rejection, arbitrary target-magnitude exclusion, new target, or mandatory full-corpus audit. A source-supported later repair must refresh affected data and qualification.

**2. Accept the known PEG structure-representation warning?**

**Problem and effect.** Five source-named polymer grades do not have a single exact molecular graph. There are 128 missing solvent-1 structures and 1,309 missing solvent-2 structures; these are cell counts, not additive row counts. Grade categories remain known inputs. Molecular encoders lack exact chain distributions for these observations.

**Panel agreement.** Retain the grade identities and measured conditions, represent exact SMILES as missing and propose accepting the two `dataset_smiles_column` warnings with that reason. This applies USE-6 and CLEAN-10/24, not an exception requiring a separate consistency prompt. A fictitious nominal oligomer or blanket PEG-row removal would be less faithful. Strict train-only qualification demonstrates usable signal with the representation, but does not prove PEG subgroup calibration. Myunghwan's warning disposition is still required; no acceptance has been applied by this panel.

The original 2021 dapsone SI limit is material context for the review, but the already well-corroborated 110-row metadata repair need not become a separate invented approval gate. The panel agrees to retain it, with its exact evidence boundary.

**Agreed facts and completed qualification**

- The pinned release contains 175,166 rows, 19 fields, 810 canonical solutes, 750 named molecular/grade solvent pairs and 3,001 solute-pair systems from 1,115 DOIs. All primary mole fractions are finite and strictly between zero and one; source decimal-log values agree numerically. Public release metadata verifies open CC BY4.0 and the exact CSV size/MD5; input SHA256 is `be72940b1d9ba03eacf142cfb26e774b658617dbf8fefb3cfb96f27c4da5e51d`.
- The implemented task contains 167,112 rows, 810 shipped solute structures and 606 grouping families. It predicts ln(source mole fraction) directly with fallback RMSE and identity scorer transformation. Every fold independently passes perfect-prediction and unit-offset scorer checks.
- All nine actual folds have zero tested family, exact/nonstereo, parent, neutral-parent, InChI and tautomer identity intersections. All six explicit core links remain within groups. Each test fold has 202 families. Close training analogs remain for 2.89–7.72% of unique test solutes; this is not complete chemical-distance separation or prospective chronological validation.
- The dapsone repair changes the second solvent identity for exactly 110 guarded source rows and preserves targets, proportions and temperatures; that DOI's other 330 rows remain untouched. Ten corrected endpoints deduplicate, explaining the final ten-row reduction. Two primary follow-on body descriptions and ten exact same-source ethanol matches support the correction; original 2021 SI/interior cells were not recovered.
- Deduplication uses exact delivered inputs plus delivered ln target. The 20 additional float-log collisions versus raw-primary equality differ by at most two machine ULPs, not meaningful assay precision. Distinct delivered outcomes remain; no new outcome averaging was introduced.
- Native check: 27 checks, zero errors, two missing-PEG structure warnings and one conflicting-input info. The warnings are not accepted. Native dtype: zero of six ordinary columns flagged, with typed structures checked separately.
- Current native task diagnostic: 167,112 rows/4,227 encoded features, five of nine folds, 10,000-row cap, no task flags; LightGBM RMSE2.020975, random forest2.158947 and mean baseline2.716196. These are bounded stock-helper diagnostics with full-frame median filling, not strict deployment-honest scores.
- Native leakage diagnostic completed on the current table, three model folds at the 10,000-row cap, with 12 single-feature fits screened into the expensive diagnostic. Exact-copy checks cover all nine actual folds/501,336 repeated test appearances and find zero matches; nearest-neighbor R2 is negative. No outcome-derived input or reliable participant exploit was demonstrated by the tested attacks. This does not prove absence of every possible leak.
- Native group diagnostic also completed successfully: 3,057 sampled rows/16 families, one repeat by three folds. IID R2 is0.989 versus grouped -0.463 in its split-gap comparison; learnability R2 is ridge -0.709, random forest0.072, LightGBM -0.164 and kNN -0.601. This small, transductively imputed subset demonstrates the known-chemical interpolation shortcut and the instability of a small held-out-family sample. It is not a verdict that the full task lacks across-family signal. SPLIT-27 requires checking other families, and the more relevant strict actual-fold evidence below directly addresses full held-out coverage. No per-group-label permutation conclusion applies to this per-sample regression.
- Strict supplement: one fixed 200-tree recommended-encoding LightGBM, deterministic 50,000 training rows per fold, full actual test sides, train-only medians/variance masks/category levels, no HPO or holdout selection. Mean RMSE is2.049564 versus2.715437 for full-train means, better on9/9 folds; range1.844997–2.220950. Mean family RMSE is1.841098 versus2.523385. Saved predictions, indices, truths and preprocessing identities pass no-fit verification. This resolves learnability and preprocessing concerns without claiming full-training performance or model-family superiority.
- The refreshed participant review trained only on supplied training labels and found zero demonstrated exploit improvements on all nine folds. Its broader identity lookups have zero coverage across final families. Row augmentation improves only2/9 folds and averages0.000232 RMSE, while legitimate structural-format inputs explain most of the small combined augmentation difference. Map row/order or unavailable-information attacks to LEAK-10/16 and EV-6: no measured reliable channel remains, so there is no new accepted leak to invent. Structure-format information available from planned molecules is not post-outcome leakage merely because it adds signal.
- The stale167122-row native result is historical. The operation receipt records two exact historical driver groups stopped while the current final-data driver was retained. Current native task/leak JSONs both identify167112 rows; all four commands now return0. Their output files still need the parent's final immutable manifest. No old prediction array is used as current.

**Precedent and remaining evidence limits**

The precedent checker found no demonstrated rule departure, drift or third exception requiring a new curator reflection. Typed molecular structures, grouping-only identity relations, delivered-value copy handling and measured continuous outcomes follow the accepted molecule cases. The dapsone repair follows the repair-first principle while explicitly having weaker original-table recovery than SUPPORT2/framingham. Source-limited repair and named-PEG retention must not be recast as fully recovered experimental truth.

The scientific decision now concerns inclusion with the specific source/representation limits, not approval to do already-authorized add work. The source corpus, method/polymorph state, collection-level overlap and prospective usefulness have not been exhaustively verified. Repeated folds reuse the same chemical families and are not nine independent populations; no naive confidence interval is claimed. No current evidence justifies changing the approved target. Final ship and any later build/commit/publication remain Myunghwan's decisions.

</details>

<details><summary>Historical full panel — Claim audit</summary>

**Independent claim audit: MixtureSolDB**

**Release metadata confirmation**

Dataset-specific licence uncertainty is **resolved** by independent parsing of the public Zenodo API JSON supplied through the parent's explicitly authorized scoped GPU source request. Metadata SHA256: `5163995e25ce05829ac773aa8405ed6b97956e01298a1610784a01ae4fcbf53e`.

- Record18660057 / DOI10.5281/zenodo.18660057 declares `metadata.license.id = cc-by-4.0` and `access_right = open`.
- Its MixtureSolDB.csv entry is41,107,737bytes with `md5:597e31685fe36c78d568f3d37b6e1336`; both match the actual pinned local raw file independently.
- Publication date2026-02-16; modified2026-05-30T21:52:50.585966+00:00. The metadata has no explicit `version` string; version relation index2 is the final version in concept17846306, consistent with the independently viewed release HTML's v3 label. Record ID and file hashes pin the input without relying on a guessed version string.
- `metadata-confirmation.json` retains the bounded verification. This role made no gateway or network request for it. Earlier browser/API access limitations below are preserved as history and no longer leave the dataset licence unknown.

**Current focused confirmation after repairs**

Final functional definition SHA256 `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34` independently reloaded and tested.
Verdict: implemented target, scorer, bounded source correction and specified identity-family guards hold on the current functional bytes. Final actual-data result is **167,112 rows, 810 exact solutes and 606 families**. The full initial claim table below remains historical evidence; the current confirmation supersedes its initial620-group/167122-row counts and open parent-family concern. No curation/definition/README changes were made by this role.

| Current or repaired claim | Independent test | Result | Rule |
|---|---|---|---|
| Sole target remains ln measured mole fraction | Check every retained source index against raw primary values | Exact array equality; no target replacement or outcome averaging | USE-5, MET-3 |
| Bounded dapsone correction affects only110 specified source rows | Independently construct predicate, compare source fields and reconstruct entire delivered frame | Predicate110; other330same-DOIrows unchanged; only Solvent2/name and SMILES changed in reference; all100retained corrected source indices have expected ethanol/ethyl-acetate identities and exchanged fractions | PROV-13, CLEAN-1, EV-6 |
| Correction preserves physical settings and outcomes | Compare target, temperature and original component fractions through explicit slot normalization | Holds; pure endpoints normalized consistently; all ten newly recognized ethanol endpoints deduplicate against existing equivalent delivered rows, explaining167122->167112 | USE-6, LEAK-19 |
| Corrected output is faithful to a separately implemented pipeline | Independent RDKit canonicalization/grade decode/swap/pure normalization/dedup followed by pandas frame equality | Exact equality of all delivered non-group columns at retained source indices | EV-1/6 |
| Six named family links affect grouping only | Check all six explicit source-SMILES pairs in cleaned mapping | All six pairs have same family; shipped structures unchanged and all present structures parse | SPLIT-31, CLEAN-24 |
| Neutral-parent/tautomer families no longer cross groups | Independent FragmentRemover+RemoveStereochemistry+Uncharger+TautomerEnumerator keys over810solutes | Zero normalized keys span families; source solutes remain810, families606 | SPLIT-31 |
| Current nine folds separate rows, exact solutes and declared families | Rebuild native container and check every fold | All nine have zero exact-predictor-hash, exact-solute and family intersections; each test fold202families/51256–58877rows | LEAK-16, SPLIT-31 |
| Current scorer computes RMSE of ln values directly | Native scorer vs manual formula, perfect prediction and unit offset on all nine folds | Every fold agrees<1e-12; perfect0, +1ln offset1; dummy RMSE2.513419–2.867657 | MET-2/3/11 |
| Source correction evidence is bounded | Read domain-practitioner report and run independent raw endpoint/implementation checks | Two primary follow-on body passages and ten exact same-DOIethanol endpoint matches support correction; original2021SI/interior table not recovered | PROV-13/16, EV-7 |

The final-repair evidence is in `final-repair-measurements.json`, executable `audit_final_repair.py`, current `measurements.json` and logs. The earlier initial snapshot is retained in `initial-measurements.json`/`initial-audit.log`. Current code/scorer tests did not run or write native dataset-check documentation.

Source re-opening limits: this role reopened the main MixtureSolDB primary paper successfully. Its later direct requests for the follow-on MDPI/ScienceDirect pages returned429/403, and PMC returned a browser challenge. The domain reviewer independently read those primary body texts; this focused role does not falsely label that review as its own recovered original SI. Dataset-specific Zenodo license is now independently confirmed from the retrieved public metadata as CC BY4.0, resolving the earlier browser-rendering/API-access limit; see Release metadata confirmation above.

At the requested final status read, `probe-status.json` reported task state=running. Its task.log tail contained the Matplotlib writable-cache fallback and repeated descriptor-frame fragmentation warnings, without a completed model/probe summary or traceback. No incomplete probe result is certified here; the driver was not launched, interrupted or modified by this role.

**Initial audit, retained history**

2026-11-10 UTC. Read-only role. Initial audited definition SHA256:
`6f8b4156897f7ddf7a4ad470cc529817444b57e587e3f5623f3ccc84b3021156`.
The approved target is natural-log mole-fraction solubility. This audit tests source,
implementation and scorer claims; it does not replace final model qualification.
Executable `audit_claims.py`, `measurements.json` and `audit.log` preserve the tests.
No source, definition, record or claim changes were made. All numerical runs capped
threads at two. A later focused update must identify any changed definition/folds.

Verdict: primary target and scorer are correctly implemented. The source supports
real experimental solubility prediction. Initial exact identities are separated,
but broader salt/charge family claims need the independent split-audit repair.
Correct historical schema and evidence overstatements and the delivered-space
copy wording. No measured primary-target defect requires trying another target.

**Sources independently read**

- [Malikov et al., Scientific Data 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13168504/):
  Methods, Data Records, Technical Validation and Usage Notes. The Methods limits
  inclusion to atmospheric-pressure measurements without additives and specifies
  literature search to October 2025. The Usage Notes recommends mole-fraction LogS
  for benchmarking. Technical Validation describes extraction validation, not a
  model-evaluation protocol. No model-selection metric is defined by this paper.
- [Zenodo v3 release](https://zenodo.org/records/18660057): schema and pinned CSV
  checksum; paper counts compared with independently measured payload.
- Actual CSV SHA256 `be72940b1d9ba03eacf142cfb26e774b658617dbf8fefb3cfb96f27c4da5e51d`.
- Current definition, generated README and curation record; independent raw/column
  reports used as cross-checks, with own scorer/domain/copy tests below.

**Claim-by-claim tests**

Task-summary fields and every curation/split bullet are covered below. “Holds”
means the stated bounded test or source supports it, not prospective experimental
validation. Recommendations and deliberately qualified gaps are distinguished from
facts. Rule IDs refer to the pinned knowledge skills.

| Claim and location | Source/test | Result and decisive evidence | Rule |
|---|---|---|---|
| Task question: natural log of solute mole-fraction solubility | Direct raw-domain/log test; target and scorer inspection | Holds: all 175,166 primary labels finite, 0<x<1; target constructed by np.log(x) | USE-5, MET-3 |
| Use case: for example a chemist selects compositions/temperature before measurement | Compare published purpose and declared input timing | Plausible, explicitly inferred actor; approximate deployment fit, not a documented prospective decision cohort | USE-1/3/8 |
| Row: one experimental condition and reported solubility | Source Data Records; physical keys and variable settings | Holds as source definition; cannot independently establish truth of every experimental extraction | PROV-1, EV-7 |
| Predicted quantity and example ln(0.001)≈-6.908 | Independent np.log calculation and pipeline inspection | Holds; no double logarithm; negative targets valid | USE-5, CLEAN-16 |
| Known inputs: molecular identities, temperature, fraction and basis | Feature list and source initial-composition definitions | Holds at the declared planning point; incomplete exact PEG graph explicitly qualified | USE-6, CLEAN-24 |
| Split: whole scaffold and identity families held out | Own all-nine-fold tests plus split auditor | Initial exact/canonical-family claim holds; broad parent claim needs repair as described by independent split audit | SPLIT-31, EV-6 |
| Changes: other outcomes and identifiers removed | Enumerate final nine predictors | Holds: three structures, temperature, two fractions, fraction basis and two polymer-grade categories; no outcome, DOI, identifier or group in predictors | LEAK-10, CLEAN-3/24 |
| Approximate fit, unrecorded polymorph/method/context | Source schema and finite input list | Holds as stated limitation; cannot claim identical inputs imply identical physical experiments | USE-8 |
| Prediction point before measurement | Input composition vs outcome construction | Holds by task design; not an empirical chronological experiment | USE-3 |
| Natural log first, alternative only if unsuitable | Actual curator CC words and definition | Holds; no alternate-target sweep or score-driven target choice observed in definition | P3, TP-2/6 |
| Metric scores log values directly and leaves target_transform identity | All nine folds independently scored through native scorer and manual RMSE | Holds exactly to <1e-12; perfect=0, +1 ln-unit offset=1 on every fold | MET-2/3/11 |
| Source defines no model-evaluation metric; fallback reason names inspected sections | Independent paper reading | Holds: Technical Validation validates extraction; paper advertises model-development use without evaluating models | MET-1/5/8/11 |
| Source was searched through October 2025, atmospheric pressure, no additives | Methods independently read | Source-supported; no raw field independently verifies pressure/additives per row | PROV-16, EV-2/7 |
| Pinned v3 file defines actual bytes | SHA256 assertion plus independent file hash | Holds; own read has 175,166x19, no RecordID | PROV-8/13 |
| Stable historical identifier denotes MixtureSolDB; BigSolDB separate | Current title, MixtureSolDB DOI vs additional source links | Holds as task identity, but record still carries unrelated BigSolDB source links: factual metadata cleanup needed | PROV-7/8 |
| Canonical typed structures retain fragments and stereo | Code and independent column audit; present structures parse | Holds; parser checks and output retain whole structures, with grouping-only parent treatment | CLEAN-24 |
| No learned or target-derived input | Inspect cleaning function and exact predictor list | Holds; dedup reads labels only to identify final copies, not to compute features | CLEAN-6/7 |
| Four source outcome representations dropped | Direct feature list | Holds; sole newly named target remains excluded from predictors | LEAK-10 |
| Temperature/fractions numeric, fraction basis categorical | Dtypes and raw source constraints | Holds; original mass/mole information retained for interior mixtures | CLEAN-14 |
| Solvent slots and proportions exchange together | Code plus independent column tests | Holds; source grades exchange as well, no phantom unused solvent after endpoint normalization | CLEAN-1/14 |
| Pure endpoints retained, unused component normalized | Own data counts; independent reconstruction | Holds: 20,826 retained delivered pure-condition rows after dedup; original source has 28,870 endpoints | USE-7, LEAK-19 |
| Remove exact copies while retaining “different measured outcomes” | Exact duplicate tests and independent column collision study | Clarify: equality is delivered inputs + ln target; 20 raw-double differences of at most 2 ULPs collapse, scientifically negligible. Literal every-raw-double preservation is too broad | LEAK-16/19, EV-2 |
| PEG '-' decoded missing and source grades preserved | Missing structure/grade cross-tab and parser checks | Holds: output has 128 solvent1 and 1,309 solvent2 missing structures, all source-named PEG grades; exact polydisperse graph remains unrepresented | CLEAN-10/24 |
| Distinct measurements remain one held-out family | All-nine-fold exact-solute separation | Holds for exact identities; broader parent normalization addressed separately, no proven exact-copy cross-split leak | SPLIT-31, LEAK-16 |
| Older compilation overlap is collection-level concern | Current statement vs no acquired predecessor payload | Reasonable qualification; exact cross-compilation identity/overlap untested and should not be represented as measured | PROV-4, EV-7 |
| Publication date does not establish label-availability split | No chronological split declared; no availability column in source | Holds as limitation; grouped result is not prospective validation | SPLIT-3/9, EV-7 |
| Source lacks systematic uncertainty/experimental-method columns | Actual 19-column schema | Holds; other source papers may contain such context, not available in task inputs | USE-8, EV-2 |
| Contradictions may be conditions/extraction errors, no MixtureSolDB noise floor inferred | Same-input conflicting outcome checks and source scope | Holds as uncertainty; 1,663 excess rows sharing delivered inputs carry different delivered targets; no universal noise floor computed | EV-6/7 |
| Native repeated grouped protocol, row-scored cold-start, shared solvents allowed | Grouping metadata and nine native folds | Holds: prediction_unit row, context none, no aggregation; solvents not held out | SPLIT-23/31, MET-2 |
| Parents remove defined fragments only, shipped structures unchanged | Definition helper and typed structure data | Holds for initial code; additive neutralization/explicit family links require focused recheck after update | CLEAN-24, SPLIT-31 |
| Ringless/oversized scaffolds get individual identities; frequency counts distinct parents | Definition helper calls scaffold_groups on distinct parent table | Holds for declared default policy; broad chemistry/alias separation is not proved by this call alone | SPLIT-31 |

**Historical screening claims requiring correction or qualification**

These are preserved historical notes, not grounds to override the curator's proceed
choice. Add-stage facts should supersede them with an attributed AI assessment.

| Historical claim | Test/result | Mild remedy |
|---|---|---|
| 175,166 rows x20 columns including RecordID | Refuted by pinned payload: 19 columns and no RecordID | Preserve old screening block but state measured schema discrepancy in current notes/assessment |
| 810 solutes, 750 pairs, 3,001 systems, 1,115 articles | Supported by own row/solute/source count plus independently reproduced physical-key counts | Use these payload counts; GitHub's 3,018 is not this file's count |
| “not screened yet” after a screening block | Historical stale wording, not current stage | Current dated assessment/CC supersedes; no need erase history |
| MixtureSolDB and BigSolDB mixed source links need splitting/renaming | Mixture task is unambiguous; stable name should not be silently renamed | Remove unrelated task DOIs from this record's source_links; retain sibling context in history |
| Earlier compilation “rows overlap through the same articles” | Plausible but exact shared articles/observations not independently measured here | Phrase as potential shared-source overlap until matched payload evidence exists; do not claim independently drawn datasets |
| “RMSE0.39 logS … a noise floor” carried from BigSolDB | Not a MixtureSolDB measurement and not a universal statistical floor | Explicit correction; no MixtureSolDB noise floor established |
| SMILES “need descriptors” | Structures are valid special features; present runtime handles recommended encoding | Current definition ships typed SMILES, not hard-coded descriptor columns |
| Target could be either unit | Curator explicitly chooses ln mole fraction first | Preserve approved sole target; alternatives conditional on substantive qualification evidence |
| CC BY4.0 for dataset | Paper is explicitly CC BY4.0. Retrieved Zenodo HTML has Rights/License heading but no license value; API request inaccessible | Dataset-specific license not independently machine-verified by this audit; do not infer a legal defect or reject on licence grounds |
| External collections none found, no better source, BigSolDB version counts | Not independently researched/tested in this audit | Retain as bounded historical search claims, not measured new facts |

**Independent scorer and fold evidence**

The initial definition's native container has 167,122 rows, 810 exact solutes and
620 groups. Every one of nine folds had zero family overlap, zero exact-solute
intersection and zero intersection of exact predictor hashes. Test folds contain
206–207 families and 52,696–61,690 rows. These are row-scored folds, not nine
independent scientific samples. Train-mean dummy RMSE ranges 2.56030–2.86492 ln units.

For every fold the native scorer agreed with sqrt(mean((y−p)^2)) to <1e-12.
Perfect predictions scored0; y+1 scored1. This decisive scale test rules out the
accidental use of RMSE after exp or a second log. Metric inputs are empty, so there
is no missing scoring-only field. The task's grouping key is excluded from features.
No additional custom metric implementation or tests are required.

**Remaining limits and disposition**

No feature/target/scorer Must failure was found. The finite target, source trace and
roughly positive independent task-gamer baseline evidence support continuing the
approved candidate. Actual model usefulness and probe flags must be judged on the
final revised folds, not borrowed from initial folds. Current exact-copy separation
is not an exhaustive guarantee against close analogs, related salts or publication
selection. The independent split auditor owns those stronger checks and repair.

The two PEG-structure warnings require explicit proposed handling at added review;
this audit supports meaningful grade-based retention without fabricating a molecule.
Conflicting measurements and incomplete experimental context must stay disclosed.
Do not remove difficult valid observations, choose another target for a larger score,
or infer final inclusion from a clean source/scorer audit. No curation edit, model
fit, container build, publication or claim mutation was performed in this audit.

</details>

<details><summary>Historical full panel — Column audit</summary>

**Independent column audit: MixtureSolDB**

**Final definition confirmation**

Final audited SHA256: `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`.
The bounded final column pass is favorable: **167,112 delivered rows**, finite
ln target, the same nine predictor columns, no retained alternative outcome or
provenance predictor, and all present molecular structures parse. `audit_final_columns.py`
and `final/measurements.json` independently reproduce the physical-input/ln row
accounting with the bounded repair and retain the exact earlier machine-precision
explanation below. This section supersedes the historical implementation hash and
row/family counts in the original audit body.

The repair predicate selects exactly 110 dapsone/ethyl-acetate rows from
DOI10.1016/j.molliq.2021.117403. Independent assertions establish that only the
second solvent name/structure changes from water/O to ethanol/CCO; source labels,
temperatures, both fractions and all other fields are unchanged. The other 330
rows from the same DOI remain unchanged. All ten zero-ethyl-acetate targets match
that DOI's pure ethanol endpoints exactly. This agrees with the domain role's
primary follow-on source descriptions; the original SI/interior experimental
cells remain unrecovered, so the evidence supports this bounded metadata repair
rather than a claim of complete original-table verification. Final deduplication
removes ten now-redundant endpoints; it does not average or rewrite their targets.
The source-file SHA256 remains unchanged.

Final participant-kit data match every processed definition column value and
exact row hashes in the same order. The plain `DataFrame.equals` boolean is false
because the loaded frames are not identical pandas metadata objects; equality
was therefore established using ordered per-column values and exact row hashes,
not by treating that boolean as a pass. There is no tested target/input row
misalignment. Neutral-parent and six explicit core-family relations affect only
the excluded grouping metadata; molecular predictor strings remain intact.
Their generalization adequacy is independently assessed by the split role.

The final definition now explicitly documents exact delivered-input-plus-ln-target
copy equality and machine-decimal tails. That resolves this role's earlier
nonblocking documentation finding. Original equality counts below remain evidence
for the pre-repair payload; do not reuse those as final post-repair counts.

**Native diagnostic preprocessing and progress**

Reading the current native helper establishes a diagnostic caveat:
`curation_probes/text.py` lines28–44 converts numeric/category inputs and performs
`X.fillna(X.median()).fillna(0.0)` over the full encoded frame. `task.py` calls this
at line271 before selecting/slicing outer folds at294/335. The group helper has
the same full-frame median fill at `groups.py` lines37–46, called at176 before
fits at186. Three recommended SMILES encodings are supplied by dataset_io before
these helpers run. The encoding itself is a fixed molecular transform; **median
imputation is transductive preprocessing** for these native diagnostics. It uses
held-out input distributions, not held-out labels. Native diagnostic scores must
be labeled accordingly; a strict train-only preprocessing supplement is needed
before using model signal as evidence of deployment-honest generalization.
No new model fit was run by this role.

The slow native task is not fitting a single model for every encoded feature:
`numeric_blocks` does contain all encoded columns, but `task.py` lines372–373 rank
by the fitted outer-training LightGBM's gain and keep `N_SINGLE=5` (line92).
There are at most five inner single-feature fits and one selected refit per
outer fold. Full linear Ridge, 200-tree random forest, 300-tree LightGBM and the
wide-table selected-linear family, plus encoding/median preparation, remain real
work. No adapter change is justified by a supposed 7,000-fit inner loop.

At this role's final observation, `probe-status.json` still says task running;
task.log contains Matplotlib cache and RDKit descriptor-fragmentation warnings,
with no task summary. The local tool process namespace showed no matching driver
or task rows, which cannot establish remote/root-job completion or failure.
Completion and scores remain unverified here; the parent must reconcile its
actual driver state. No process was interrupted by this role.

---

**Original pre-repair column audit (historical)**

2026-11-10 UTC. Read-only panel role. Audited the definition with SHA256
`6f8b4156897f7ddf7a4ad470cc529817444b57e587e3f5623f3ccc84b3021156`.
No curation or definition edits. `audit_columns.py`, `measurements.json` and
`dtype/` preserve reproducible evidence; all Python runs capped threads at two.

Verdict: column semantics, timing, target and types are suitable for this proposed
measurement-level regression. No demonstrated feature leakage or blocking column
error. One documentation clarification is required: duplicates are defined in the
delivered natural-log target space; preserve that exact equality convention rather
than claim every distinct raw floating-point value survives. PEG representation
is an explicit incomplete-structure limitation, not an invented molecular graph.

**Source and prediction point**

The publisher's [release](https://zenodo.org/records/18660057) and
[paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13168504/) define a measured solute
mole fraction for two solvents at an initial composition and temperature. Here the
prediction is made before laboratory solubility measurement. The planned molecular
identities, solvent-grade identity, composition and temperature exist at that point;
solubility observations and publication provenance do not become predictors.
The exact source CSV is asserted by SHA256 before the implementation reads it.
The expected scientific interpretation follows USE-1/3/5/6, with approximate fit
because the literature lacks complete method, polymorph and condition information.
No prospective chronological validity is asserted.

**Every cleaned column**

| Column | Meaning | Known before measurement? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| SMILES_Solute | Entire solute molecular structure, retaining stereo and all fragments | Yes, planned solute | Typed canonical SMILES, string; 810 distinct; all parse | Fine | USE-6, CLEAN-24 |
| SMILES_Solvent1 | First normalized solvent's exact molecular structure, when representable | Yes | Typed canonical SMILES; 127 distinct present, 128 missing rows for source PEG grades; all present values parse | Fine with disclosed representation limit | CLEAN-10/24 |
| SMILES_Solvent2 | Second normalized solvent's exact molecular structure, when representable | Yes | Typed canonical SMILES; 128 distinct present, 1,309 missing rows; all present values parse | Fine with disclosed representation limit | CLEAN-10/24 |
| Temperature_K | Planned experiment temperature, kelvin | Yes | Float64, 2,459 values; positive source temperatures | Fine | USE-6, CLEAN-14 |
| Fraction_Solvent1 | Initial proportion of normalized solvent1 | Yes | Float64 in [0,1], exchanged together with solvent identity | Fine | CLEAN-14, USE-6 |
| Fraction_Solvent2 | Initial proportion of normalized solvent2 | Yes | Float64 in [0,1], complementary to fraction1; exchanged together | Fine; complementary is not an exact duplicate column | CLEAN-5/14 |
| Fraction_Type | Whether initial proportions are mass or mole fractions | Yes | Unordered category, two named levels | Fine; do not interpret 0.5 mass as 0.5 mole | CLEAN-14 |
| PolymerGrade_Solvent1 | Source-named grade for a solvent lacking one exact molecular graph; molecular otherwise | Yes | Unordered category, six named levels including molecular | Fine; preserves physical grade information without inventing a chain | CLEAN-10/24 |
| PolymerGrade_Solvent2 | Same grade information for solvent2 | Yes | Unordered category, six named levels | Fine | CLEAN-10/24 |
| ln_solubility_mole_fraction | Natural log of measured mole fraction | Outcome | Float64, finite, -21.4164 to -0.05615; sole target | Fine; never a feature | USE-5, LEAK-10, MET-3 |
| solute_family | Structural family key used only for splitting | Metadata | String, 620 values; not a model input | Fine for its role; independent split audit determines adequacy | SPLIT-31 |

The native dtype probe ran independently: zero of six ordinary columns flagged;
no machine-readable external codebook was fetched by that probe. Its exclusion of
typed SMILES and grouping metadata does not count as a semantic check of those
fields; their semantics and parsing were checked separately above.

**Independent implementation tests**

`audit_columns.py` independently reconstructs the physical inputs from the raw
CSV without the definition's canonicalization helpers: RDKit canonical structures,
source PEG grade keys, normalized solvent order with its corresponding fractions,
and a pure-endpoint identity using the active solvent only. Its final physical
input-plus-ln-target equality count is exactly the implementation's 167,122 rows.
All present delivered SMILES parse. Pure endpoints' two delivered solvent identities
agree, including polymer grades, so an unused solvent cannot remain a phantom input.
The distinct PEG grades remain explicit in the corresponding categories. No outcome
representation, source DOI, compound identifier, compound name, FDA flag or row ID
survives as a predictor.

The natural-log target is computed directly from positive raw mole fractions.
Its agreement with the source decimal logarithm times ln(10) is within
9.97e-13 over all source rows. `Metric.fallback` has `target_transform='identity'`:
RMSE therefore scores the delivered ln-solubility quantity, rather than inverting
it and accidentally scoring physical mole fractions. No task/target selection
result was inferred from that numerical identity.

**Resolved accounting discrepancy and documentation remedy**

Independent equality counts under identical physical inputs are:

| Equality target | Excess duplicate rows | Retained rows |
|---|---:|---:|
| Source published LogS(mole_fraction) | 8,019 | 167,147 |
| Raw measured mole fraction as parsed float64 | 8,024 | 167,142 |
| Delivered np.log(raw measured mole fraction) | 8,044 | 167,122 |

The difference is not a solvent-alias bug. Source logarithms differ for 32 groups
whose raw primary mole fraction is identical; the largest source-log difference
within such a group is 4.25e-13. Separately, 20 groups contain raw floating values
that map to an identical delivered natural log. Their primary values differ by at
most two floating-point ULPs, relative range at most 2.5951e-16, absolute range at
most 1.3553e-20. Literal source examples include `5.586e-07` and
`5.585999999999999e-07` for Benorilate under the same condition and DOI.
`primary-fraction-ln-collisions.json` and
`identical-primary-different-source-logs.json` retain the evidence.

These are decimal serialization/machine-precision differences, far below the
experimental precision represented by these source values. Exact equality on the
delivered input and ln target is a reasonable LEAK-19 convention. No meaningful
experimental label resolution is lost by these 20 additional merges, and preserving
them as indistinguishable delivered rows would change weights without adding
resolvable outcomes. No additional curator choice is needed for this bookkeeping.
The mild fix is to document that exact convention, include current 8,044/167,122
counts, and replace any literal assertion that every distinct raw-double outcome
survives. Substantively different delivered ln observations remain separate.

**PEG and alternative-target limits**

Missing molecular values are precisely decoded source '-' polymer entries; no
missingness was induced by the solubility outcome. Keeping source grades is a
meaningful representation of a polydisperse material. A model cannot recover its
exact chain-length distribution from nominal grade; disclose that limit and propose
accepting the corresponding structure warnings rather than silently inventing a
molecule or discarding otherwise usable conditions. This column audit recommends
retention; the final warning acceptance remains the curator's scientific decision.

The separate raw audit identified 208 discrepancies in recalculating unused mass-
based solubility from graph molecular weights. This audit does not claim to have
resolved their original chemical identity or source calculation. They do not prove
an error in the direct measured mole-fraction target, and provide no established
reason to switch away from the curator's primary target. Do not promote this
limited conversion diagnostic into either target rejection or target verification.

**Findings and limits**

- One nonblocking documentation finding: specify delivered input-plus-ln equality
  and explain the machine-precision row-count difference (LEAK-16/19, EV-2/7).
- No tested input is post-outcome; no outcome proxy survives; types follow meaning.
- PEG missing-graph warnings are an explicit material representation limitation.
- No model fits, cross-compilation overlap measurement or complete original-paper
  chemistry reconstruction was performed in this column audit. Group separation
  and task-gaming validity are for their independent panel roles.

</details>

<details><summary>Historical full panel — Split audit</summary>

**Independent split audit**

**Final installed-definition verification**

**Final verdict: right with disclosed approximation limits; initial identity defect repaired.**
The final installed definition SHA256 is `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`. I independently rebuilt
its actual measured table and native splits: **167,112 rows, 810 solute strings, 606 families**,
with 202 test families in each of the nine folds. Test sizes are 51,256–58,877; target
standard deviations are positive in every fold. All nine actual folds have zero overlap
for declared families, canonical full structures, nonstereo structures, FragmentRemover
parents, parent InChI, parent tautomers, uncharged parents, uncharged tautomers and
the broader largest-fragment diagnostic aliases. No broader diagnostic identity now
spans two declared families. The largest group remains 3,079 rows and 19 solute strings.

The six explicit source pairs and neutral-parent links were checked in the installed
code, not inferred from the earlier proposal. A separate independent input/target
reconstruction matches the full final curated row-content multiset. It includes the
110-row dapsone solvent-identity correction for DOI 10.1016/j.molliq.2021.117403,
normalizes solvent slots/endpoints, and deduplicates exact physical input/target copies.
All retained target values remain direct ln of source mole fractions; no alternate
target or outcome averaging was introduced. The solvent correction changes inputs,
not source outcomes, and removes ten additional duplicate endpoints relative to the
167,122-row initial table. The scorer transform is identity on the logged target.

Final Morgan radius-2/2,048-bit close-analog shares (Tanimoto>=0.7) among unique test
solutes remain 2.89–7.72%, with row-weighted shares 2.17–8.34%; these are measured
limits on the chemical-distance claim rather than evidence of exact identity reuse.
The 110-row source repair cannot change solute-group identity. I checked its
implementation/row accounting, not the original inaccessible experimental SI;
the external publication-backed repair rationale remains the source/domain
auditors' responsibility.

Final evidence is in `final/audit.py`, `final/audit.json`, chemical-key tables,
`final/final_integrity.py` and `final/final-integrity.json`. Both scripts verify actual
installed bytes; the latter also verifies the definition did not change during its
run. No model or native group probe was run in this final audit. Earlier 620-family
results and the 606-family proposal evidence below are retained as historical diagnosis,
and do not replace the final installed-fold evidence.

**Historical initial diagnosis and proposed repair**

**Verdict**

**The grouped cold-start regime is appropriate, but the initial 620-family implementation needs a narrow identity repair.** All native folds separate their declared family labels and exact chemical strings. Nevertheless, neutralized parent and tautomer forms can cross those families. The mild remedy is to union these source-derived structural identities and six explicitly inspected salt/metal-complex relationships, preserving every shipped molecular structure and measured outcome. This is a grouping correction, not a reason to change the approved natural-log mole-fraction target or delete salts.

The repair has been independently tested as a proposal using the native repeated grouped protocol. It gives 606 families and no overlap in the chemical identities tested below. Final installed-byte verification remains a separate step; proposal results are not substituted for it.

**Intended generalization**

The definition predicts solubility before measurement for a new solute family, from its full structure and planned solvent composition and temperature. Row-scored regression with `labels=per_sample`, `prediction_unit=row`, no aggregation and `context=none` matches that unit. A family contains multiple genuine experimental conditions; assigning every solute one average outcome or taking one row per solute would change the task. Solvents may occur in both train and test. Group labels are splitting metadata and are excluded from model inputs.

The 2026 literature compilation is a retrospective collection with no per-measurement availability timestamp in the shipped inputs. A grouped holdout does not establish prospective chronological validity. No temporal train-label-availability claim is made. This is consistent with the stated approximate fit rather than a hidden assertion that labels were collected before a chronological prediction cutoff.

**Initial implementation: independent tests on all nine folds**

The initial definition hash is recorded in `audit.json`. It has 167,122 measurements, 810 solute strings and 620 families. Each test fold holds 206–207 families; training sizes are 105,432–114,426 and test sizes 52,696–61,690.

| Identity tested | Distinct keys | Keys spanning declared families | Affected solute strings | Affected rows |
|---|---:|---:|---:|---:|
| Canonical full structure | 810 | 0 | 0 | 0 |
| Nonstereo full structure | 794 | 0 | 0 | 0 |
| FragmentRemover parent | 787 | 0 | 0 | 0 |
| Parent InChI | 786 | 0 | 0 | 0 |
| Parent canonical tautomer | 786 | 0 | 0 | 0 |
| Uncharged parent | 771 | 9 | 19 | 4,448 |
| Uncharged canonical tautomer | 769 | 10 | 21 | 4,632 |
| Largest-fragment normalized parent, diagnostic only | 762 | 15 | 32 | 5,789 |

For each of the first five identity definitions, every initial train/test fold has zero overlap. Neutralized-parent/tautomer overlap affects 0.59–4.27% of test rows depending on the fold. Affected examples include fumaric acid and its monosodium form, succinic acid and its disodium form, and ibuprofen versus its sodium dihydrate. These are experimentally distinct solubility targets but chemically related parents. Their cross-fold relation weakens the claim that the whole chemical family is new. The test proves a family-policy gap, not a successful target lookup or a quantitative model-gain claim.

Rules: USE-10 requires choosing cold start from the use case; SPLIT-24 uses source-derived identities, not arbitrary similarity clusters; SPLIT-26 keeps the source rows; SPLIT-31 uses scaffold families for molecular tasks. EV-6 distinguishes demonstrated identity overlap from hypothetical leakage benefit.

**Mild repair**

1. Add label-free keys from `Uncharger(FragmentRemover(molecule))`, after removing stereochemistry, and its canonical tautomer. Union these with existing family components. This changes 620 to 612 families, while the largest family remains 3,079 rows. The shipped SMILES retain charge, fragments and stereochemistry.
2. Avoid a blanket largest-fragment salt-removal rule. The molecule guide specifically warns that it can choose an organic counterion instead of the active compound. Inspect only the remaining observed source relationships and encode exact links. Six source-SMILES pairs across five molecular-core sets are retained in `explicit-family-links.json`:
   - TPP and its manganese(III) chloride complex;
   - p-ClTPP and its manganese(III) chloride complex;
   - sorafenib and sorafenib tosylate;
   - dipyridamole and the source structure containing dipyridamole plus two tosylates;
   - L-arginine and L-arginine L-pyroglutamate;
   - L-arginine and L-arginine alpha-ketoglutarate.

The dipyridamole salt has the source name `p-toluene sulfonate`, an imprecise name. Its molecular graph explicitly contains the dipyridamole component and two tosylate fragments. The observed graph relationship supports conservative shared family grouping; it does not justify relabeling that source compound or claiming identical physical solubility.

The six explicit links and the neutral-parent keys produce 606 families. This rule does not join arbitrary molecules merely because they share a counterion, a fingerprint, or a threshold similarity. It does not infer a universal active-component rule for multicomponent salts. Some added links connect distinct metallation states; they are conservative chemical-family links, not identity assertions about experimental targets.

**Independent native-protocol proposal check**

`candidate_fold_audit.py` applies the proposed label mapping to the measured table and invokes the native split builder. All nine proposed folds have:

- zero family overlap;
- zero overlap for canonical, nonstereo, FragmentRemover parent, parent InChI, parent tautomer, uncharged parent, uncharged tautomer and the largest-fragment diagnostic aliases;
- 202 test families, 51,256–58,877 test rows and positive target standard deviations of 2.509–2.859 natural-log units;
- no change to source rows, target values or model inputs.

The largest repaired family remains 3,079 rows and at most 19 distinct solute strings. This does not create a few giant family groups or a small-test support failure.

A seeded row-IID diagnostic puts an exact solute identity in training for 55,707 of 55,708 test rows (99.9982%). Hence such a split would mainly interpolate additional conditions for known solutes. Corrected-family folds have no exact solute reuse. Morgan radius-2, 2,048-bit nearest-training similarities show that 2.89–7.72% of unique test solutes still have an analog with Tanimoto at least 0.7 (row-weighted 2.17–8.34%). The stronger evaluation reduces familiar-identity reuse; it does not claim the absence of close chemical analogs.

**Limits and follow-through**

No model was fit in this audit: root is running the native probe/model program, and the task gamer independently tests exploit gains. The repair was chosen from source molecular identities and the declared cold-start claim, not from whichever split gives the worst score. Existing model outputs on the 620-family folds remain historical once grouping changes. Refresh affected probes, kits, membership evidence and documentation on the final installed definition; do not reuse old predictions without exact train/test alignment.

Repeated folds reuse the same underlying families. Nine folds do not yield nine independent chemical datasets or justify a naive standard error treating every observation as independent. Row RMSE is a coherent primary score for the declared prediction unit; family-aware diagnostic summaries can expose heavy-family weighting without silently changing the metric.

Audit scope: local verified source and definition only, read-only on all curation files. Outputs are `audit.py`, `audit.json`, chemical-key tables, exact proposed links, `candidate_fold_audit.py` and `candidate-fold-audit.json`. No gateway, controller, dataset build, publication, target change or record mutation occurred.

**Strict train-only model qualification supplement**

At the main session's request, I subsequently ran one fixed recommended-encoding LightGBM model on every final fold, using 50,000 deterministic training rows per fold and full held-out scoring. All fitted numeric masks, medians and categorical levels were restricted to each sampled training side; no all-frame median or holdout selection entered the model. The approved target and final grouping were unchanged. Mean RMSE was **2.049564 natural-log units versus 2.715437 for each full-training-side mean**, better on all nine folds, with range 1.844997–2.220950. Mean per-family RMSE was 1.841098 versus 2.523385.

This is a bounded fixed-model signal check, not full-training or tuned superiority evidence. It supplements native diagnostic helper results whose full-frame imputation must not be presented as strict evaluation. Source, definition, input, target, encoder and fold identities, all predictions and fitted preprocessing/model artifacts are retained under the run's the retained qualification evidence. A no-fit verification rebuilt exact current folds, checked saved truths/membership/baselines, rescored all predictions, and recomputed 128 sampled training medians plus every categorical level per fold. All passed. See the inlined strict train-only qualification, `manifest.json`, `summary.json` and `no-fit-verification.json` for exact settings and limits. No curation files were changed.

**Final source documentation/style reuse verification**

Final source SHA256 `d00f833a112c360e44c065f7d69040b556827f5ecbd5a5d9a5224d8dddbe7d30` safely reuses the model-qualified `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34` evidence. A separate no-fit AST/data/scorer/fold audit permits only two description strings, function docstring text and equivalent message-free assertion splitting. Every other executable declaration is unchanged; the full original table/target fingerprints, all nine full train/test index arrays, saved truths, sample membership, baselines, prediction hashes and model hashes match. The native scorer reproduces all nine original scores. Original fit manifests retain their actual fit source hash. See the inlined final model-evidence reuse audit and `final-metadata-reuse-verification.json`. The newly documented 22-row mixture-metadata uncertainty is a scientific review question, not a qualification-data change; this audit does not settle its disposition.

</details>

<details><summary>Historical full panel — Domain practitioner</summary>

**Domain-practitioner review: MixtureSolDB**

2026-11-10 UTC. Independent read-only review; no definition, curation record, claim,
raw-source or model mutation. Recommendation: **qualify the approved ln mole-fraction
candidate after the bounded solvent-identity repair below**. Do not switch targets.
Fit: **approximate**, because structures and planned conditions are known before an
experiment, while literature selection and omitted experimental state limit transport
to a new laboratory or compound family. USE-1, USE-3, USE-5 and USE-8 apply.

**Practitioner assessment**

As a process chemist, I know the proposed solute, solvent identities or PEG grade,
initial solvent proportions and temperature before measuring solubility. Those inputs
support screening formulation or crystallization conditions. I do not know measured
solubility, and the other concentration/log representations must remain excluded.
The source's paper presents experimental property prediction and solvent selection;
this is a real use, not a relabeled survey. One row is one condition-specific
measurement, while a practical solvent-screening decision may compare many such rows.
Pooled regression is a valid first candidate; no source-fixed top-k utility or process
cost function supports inventing a ranking metric (USE-5, MET-6/7).

I would use predictions to prioritize experiments, not replace a solubility assay.
Published compounds and solvent mixtures do not establish prospective coverage of a
new process. pH/ionization, solid form, equilibration protocol, purity and laboratory
conditions can affect measured solubility and are not fully represented. The main
paper says only atmospheric-pressure/no-additive studies were included and imposed
an explicit stable-polymorph criterion where polymorphism was studied; those are
source selection rules, not a proof of identical hidden conditions in every row.
The approximate fit should remain explicit (USE-8). PEG nominal grade is meaningful
at planning time; a missing single-molecule SMILES for a polydisperse grade is not a
missing solvent identity. Preserve named grades and measured rows (USE-6, CLEAN-24).
Pure-solvent endpoints are useful limiting conditions; normalize the zero-share
component and duplicate weighting rather than excluding that population.

The metric scores my decision **partly**. RMSE directly on ln mole fraction measures
multiplicative concentration error and penalizes large log errors. A natural-log unit
means a factor e in concentration. The source recommends a mole-fraction log target
but defines no unique model-selection metric. Thus explicitly declared fallback RMSE
on the log quantity is defensible (MET-1, MET-5, MET-8/11). It is not a downstream
crystallization yield, safety threshold or process-cost score. Keep the scorer's
transformation identity; do not exponentiate before scoring. Row weighting favors
frequently measured solutes, so chemical-family summaries are useful diagnostics,
without silently replacing the primary metric.

**Finding 1: the largest conflict localizes to a wrong solvent identity**

The supposed dapsone/pure-water discrepancy is not adequately described as generic
laboratory noise. My executable `audit_dapsone.py` verifies the pinned raw SHA256 and
finds this exact block:

- `Source == 10.1016/j.molliq.2021.117403`;
- exact solute SMILES `Nc1ccc(S(=O)(=O)c2ccc(N)cc2)cc1`;
- `Solvent1 == ethyl acetate`, `SMILES_Solvent1 == CCOC(C)=O`;
- `Solvent2 == water`, `SMILES_Solvent2 == O`.

It contains exactly 110 rows: ten temperatures and eleven first-solvent mass
fractions. At fraction zero, all ten reported solubilities match the **same DOI's
pure-ethanol endpoints exactly**, not its aqueous endpoints. At 278.15 K the suspect
value is 0.002985; the same-source aqueous endpoint is approximately 1.359e-6.
The 2244-fold largest combined-data conflict also includes the slightly different
2023 aqueous estimate. These are measured comparisons, not a domain expectation.

Primary follow-on literature corroborates the identity:

- Jouyban et al., *Simulation of dapsone solubility data in mono- and mixed-solvents
  at various temperatures*, ScienceDirect Introduction, cites the 2021 experiment
  as reference 13 and explicitly lists its organic pair as **“ethyl acetate + ethanol”**.
  [Publisher body text](https://www.sciencedirect.com/science/article/abs/pii/S0167732221029482).
- Cysewski et al., 2024, *Experimental and Theoretical Insights…*, section 2.2,
  identifies **“ethyl acetate-ethanol [27]”**, with reference 27 the same 2021 DOI.
  [Publisher text](https://www.mdpi.com/1420-3049/29/8/1743),
  [PMC text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11051893/).

Direct DOI/publisher opening for the original 2021 paper was unavailable. Its abstract
was surfaced in copied/indexed text and agrees, but I do not treat that alone as
original full-text/table verification. The two primary follow-on body passages and
all-ten exact endpoint match support a bounded identity repair; the original SI
matrix and each interior cell were **not** independently recovered here.

Recommended mild repair: only for the exact 110-row predicate above, change the
second solvent from water/O to ethanol/CCO **before** canonical slot ordering and
endpoint normalization. Keep both fractions, their mass basis, temperatures and the
measured mole-fraction target. The source describes ethyl acetate as component 1 and
ethanol as component 2, and the fraction-zero endpoint matches component 2; there is
no reason to invert the source fractions in this repair. Subsequent canonical slot
sorting must exchange fractions with their solvent identities as usual. The same
DOI has three other 110-row blocks (acetone/water, ethanol/water, methanol/water);
leave all 330 rows untouched. Guard the source names/SMILES/count/grid in code so a
later release cannot silently broaden this treatment. Do not remove high target
values, average the conflict, swap outcomes or rewrite the raw archive.

This follows repair-at-origin-before-cleaning-around-damage (PROV-13, CLEAN-1/11,
EV-1/2/6), and requires refreshed deduplication, checks, splits, kits and affected
model evidence after application. Report the original-table access limit honestly.

**Other concerns and limits**

The unused mass-based conversion discrepancies in 208 rows do not establish a wrong
mole-fraction label. They remain a separate source/chemical-identity uncertainty;
changing the primary task to that alternative would not resolve the identified
solvent mapping error. All primary mole-fraction labels remain positive and finite.
No independently demonstrated defect requires target replacement.

Salts and charge states can have distinct solubilities while sharing a parent family.
The split auditor should settle their grouping; do not discard these observations
because their continuous outcomes differ. Other conflicting inputs may still reflect
unrecorded state or extraction error. After the specific repair, quantify the
remaining conflicts and avoid calling them all intrinsic experimental noise.

No models or downstream process validation were run by this role. Supplementary
tables, original experimental SI, per-row pH and polymorph state, and completeness of
all 1115 literature sources were not verified. This report does not give final
inclusion, warning acceptance or build authority.

Source inspection also included the MixtureSolDB Methods, Data Records, Technical
Validation and Usage Notes in its [primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13168504/)
and the 2018 [dapsone aqueous-mixture experiment](https://www.sciencedirect.com/science/article/pii/S0021961418302027).
Supporting local evidence: `audit_dapsone.py`, `dapsone-evidence.json`,
`suspected-ethylacetate-water-block.csv`, `suspected-ethanol-endpoint-match.csv`.

</details>

<details><summary>Historical full panel — Domain source follow-up</summary>

**Bounded follow-up: DOI 10.1021/je3009842**

Independent read-only raw/source check, 2026-11-10 UTC. The prior dapsone repair
recommendation is unaffected. This check does not authorize a new correction.

The exact source contributes 44 MixtureSolDB rows: diazepam and clonazepam, each
with 11 PEG-200/water and 11 propylene-glycol/water proportions. Every row is at
298.2 K and uses the mass-fraction convention. There are no other temperatures in
this source block to compare. `audit_je3009842.py` asserts the raw SHA256, source
identity, 44-row scope, temperature and source composition metadata.

| Compound | PEG-200/water f1=0 | PEG-200/water f1=1 | PG/water f1=0 | PG/water f1=1 |
|---|---:|---:|---:|---:|
| Diazepam | 0.000001 | 0.015696 | 0.002009 | 0.015696 |
| Clonazepam | 0.000001 | 0.010049 | 0.000641 | 0.010049 |

The first columns of each pair imply two different pure-water labels, by factors
2009 and 641 respectively. Both supposedly pure-PG endpoints match the pure-PEG
endpoints exactly for the corresponding drug. This pattern raises a concrete
hypothesis that the alleged PG/water series is instead PEG-200/PG, with PEG as
component1. A simple fraction reversal of PG/water cannot on its own explain both
endpoint identities. Endpoint agreement is not enough to reconstruct all interior
mixture identities or determine which source label/unit was mistranscribed.

The [original ACS DOI](https://pubs.acs.org/doi/10.1021/je3009842) returned403.
The authoritative [NIST ThermoML page](https://trc.nist.gov/ThermoML/10.1021/je3009842.html)
identifies the paper and reports that it measured binary/ternary PEG200/PG/water
systems at298.2K and five-temperature neat-solvent data. Its displayed datasets
cover eight five-point neat-solvent sets for PG/NMP/ethanol/water and both drugs;
PEG mixtures are not shown. The page links these exact machine-readable resources:

- https://trc.nist.gov/ThermoML/10.1021/je3009842.json
- https://trc.nist.gov/ThermoML/10.1021/je3009842.xml

The web reader returned opaque JSON without numerical text. A bounded direct
local request failed first sandboxDNS and then connection reset on approved HTTPS.
No SSH/gateway invocation or source/canonical edit was performed by this role.
Root may supply the same exact public file through its already-authorized source
route for numerical inspection. Until those numerical data or the original mixture
table establish identity, recommend **no invented correction, deletion, averaging,
or target switch**. Preserve this as a source-specific unsettled mapping question
in added review if the bounded numerical check cannot settle it.

Evidence files: `diazepam-je3009842-raw.csv`, `je3009842-evidence.json`,
`audit_je3009842.py`. Original experimental mixture tables not yet verified.

**Bounded check disposition**

Root's already-authorized GPU HTTPS request for the exact NIST JSON returned an explicitHTTP403; SSH itself succeeded. No numerical payload was returned, so no pure-PG solubility value was inferred from that attempt. The HTML source metadata remain readable. A final focused search for the DOI with supporting-data/PDF/table terms and the official ACS Figshare domain found no usable official mixture table or supporting file. The publisher issue page confirms the original article citation and availability-to-purchase, not the needed numbers. This is an access/verification limit, not a GPU outage or evidence that the experimental study is wrong.

Scope is exactly22suspect nominal PG/water rows (11diazepam+11clonazepam), compared with22PEG200/water rows at the same temperature. Both alleged PG/water pure-solvent endpoints matching the respective PEG endpoints is a concrete extraction/mapping concern. Its exact correction is unresolved. Keep all44original observations at this stage, retain source-specific uncertainty, and return it as an ordinary added-review choice:

- Retain as implemented with the explicit22-row mapping uncertainty and approximate fit; preserve measured labels and require source-table evidence before a later correction.
- Hold inclusion until the original paper/mixture table or author-supplied support resolves the identities; do not invent a replacement solvent or choose a lower-scoring subset.

A targeted later source-supported repair could change rows/inputs and require affected deduplication, check and model refresh. Neither option authorizes a switch away from the approved natural-log mole-fraction target. This bounded follow-up does not claim every other repeated-input discrepancy is intrinsic laboratory noise, and it does not require an endless full-corpus re-audit.

</details>

<details><summary>Historical full panel — Blind review</summary>

**Independent blind review of updated artifact**

**Judgment**

I would retain this as a **conditional benchmark candidate for solubility prediction on held-out solute families**. The updated table passes the structural identity checks I ran: none of the tested exact or standardized solute identities spans family groups. This resolves the specific cross-family parent-identity concern found in my earlier blind review. Some substantial conflicting measurements remain at identical supplied inputs, and the task card alone does not establish that the full benchmark construction or scientific interpretation is verified.

**Task and independent checks**

The response is natural-log mole-fraction solubility. Predictors describe the solute and two solvents by SMILES, temperature, complementary solvent fractions and their mass/mole basis, and polymer grades. The intended evaluation holds out whole `solute_family` groups across three repeats of three folds. I interpret `solute_family` as split metadata to exclude from predictors, giving nine substantive predictor columns. The supplied card does not explicitly state this exclusion.

The updated artifact has 167,112 rows, 810 distinct solute SMILES and 606 families. Each solute string maps to one family. Family sizes range from 1 to 3,079 rows, with median 180. All observed solute and solvent SMILES parse in RDKit. The row count therefore represents far less independent chemical diversity than 167,112 unrelated samples; performance and uncertainty should reflect this dependence.

The following identity checks were recomputed from the updated table, without reading any grouping implementation:

| Representation | Unique identities | Identities spanning families | Affected rows |
|---|---:|---:|---:|
| Canonical isomeric SMILES | 810 | 0 | 0 |
| Neutralized fragment parent, retaining stereochemistry | 783 | 0 | 0 |
| Neutralized fragment parent, removing stereochemistry | 766 | 0 | 0 |
| Tautomer-canonical neutralized parent, removing stereochemistry | 762 | 0 | 0 |

These checks support identity separation under those transformations. They do not establish a scaffold-distance threshold, recover the family-construction algorithm, or prove that every chemically related pair is grouped. RDKit default tautomer enumeration is bounded, so that result is not an exhaustive tautomer-equivalence proof.

There are no wholly duplicated rows. There are 1,653 repeated predictor rows, forming 1,442 predictor groups with different targets and involving 3,095 rows. Within-group target spans have median 0.12845, 90th percentile 1.25701, 99th percentile 3.92585 and maximum 7.60539 natural-log units. There are 251 groups spanning more than one unit and 84 spanning more than ln(10), or a tenfold solubility difference.

The largest remaining conflict is solute `CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc21` in pure water at 298.2 K, with targets -13.81551056 and -6.21011819. These represent approximately a 2,009-fold solubility difference at identical supplied inputs. Other large conflicts include `O=C1CN=C(c2ccccc2Cl)c2cc([N+](=O)[O-])ccc2N1` in water at 298.2 K, spanning 6.46303 units, and `CCCCc1oc2ccccc2c1C(=O)c1cc(I)c(OCCN(CC)CC)c(I)c1.Cl` in ethanol at 313.2 K, spanning 6.31289 units.

These cases warrant source-level inspection for omitted experimental conditions, solid forms, protocol differences, or transcription/unit problems. The table alone cannot distinguish these possibilities. They need not invalidate the full dataset: assigning each exact predictor group its observed target mean gives an empirical whole-table RMSE floor of 0.06664. This is an in-sample descriptive bound for single-valued predictions, not model performance or a validation score. Large conflicts are sparse enough to warrant targeted investigation rather than automatic removal of all repeated inputs.

All targets are finite and negative, with range -21.41641 to -0.05615. Temperature ranges from 252.55 to 383.15 K. Solvent fractions sum to exactly one, making the second fraction redundant. The 128 missing solvent-1 SMILES and 1,309 missing solvent-2 SMILES all correspond to explicit polymer grades, not the `molecular` grade. Polymer grade must therefore be preserved as meaningful representation. Normalizing solvent slot order and removing zero-weight solvent slots finds no further repeated predictor rows beyond the 1,653 already counted.

**Comparison with my earlier blind findings**

Relative to my earlier reported counts, the updated table has 10 fewer rows and 14 fewer family labels. Cross-family neutral fragment-parent identities decreased from 12 to zero; cross-family parent identities without stereochemistry decreased from 13 to zero. Conflicting-input groups remain at 1,442, while affected rows decreased from 3,105 to 3,095, groups spanning more than ln(10) decreased from 94 to 84, and the empirical identical-input RMSE floor decreased from 0.07722 to 0.06664. These observations establish changed outcomes, not why or how the artifact was changed. I was not supplied a change rationale and did not inspect one.

**What remains unverified**

- Actual split assignments and their reproducibility are not supplied. Group-disjoint train/test folds, repeat construction, and any preprocessing fit boundaries cannot be audited from this table and card.
- The family definition is unspecified. The successful identity checks do not establish whether “family” means scaffold, similarity cluster, standardized parent equivalence, or another relation.
- The feature representation and allowed model capabilities are unspecified. Every held-out solute string is unseen in training under the stated regime. Whole-SMILES categorical treatment cannot directly learn molecular structure; a structural representation or explicit raw-tabular interpretation is needed to make comparisons meaningful. No model was trained, so performance or difficulty is not established.
- The source measurements, experimental context, transformations to mole fractions, and provenance of the remaining large input conflicts were not inspected. No conclusion about their correctness follows from this review.
- The primary metric, explicit exclusion of split metadata, and treatment of family imbalance are unspecified. I would request a metric on the log response and both row-weighted and family-aware summaries.

**Reproducibility and scope**

This review read only the updated directory's `task.md` and `data.parquet`; comparison uses my own prior blind findings. No other project reports, rules, definitions, curation notes, or source sites were consulted. No model, gateway, controller, remote request, or delegated agent was used.

`blind_checks.py` contains the independently written checks. `blind-results.json` records their numerical results, input SHA-256 and library versions; `blind-check-output.txt` contains readable execution output. The script ran successfully with the specified project interpreter and `OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2`. An initial invocation hit the shell tool's default ten-second limit; the bounded rerun completed successfully.

</details>

<details><summary>Historical full panel — Task gamer</summary>

**Final-kit task-gamer review**

**Demonstrated exploits: 0.** The tested identity lookups have no coverage. Row/format augmentation produces small score changes quantified below; these do not by themselves establish a reliable deployment-unavailable shortcut. This is a bounded negative result, not proof that no exploit exists.

This independent rerun used only `participant_kit_final`, plus copies of my own prior scripts. All models and lookup predictions were freshly computed from its data and its 9 shipped splits (r0f0–r2f2). No earlier predictions or results were loaded. All fitted models and lookup values used only the current fold's training labels; test labels were used solely for evaluation. The group column was excluded from models. Threads were capped at 2. The task is row-level log-solubility regression before measurement, holding out whole solute families. The supplied scorer uses ordinary RMSE; no scorer exploit was identified.

**Results**

Arithmetic mean of the 9 fold RMSE values (lower is better):

| Model/check | Mean RMSE |
|---|---:|
| train_mean | 2.715437 |
| honest_lgbm | 2.477959 |
| row_only | 2.719934 |
| format_only | 2.519207 |
| artifact_only | 2.513671 |
| honest_plus_artifacts | 2.472234 |
| honest_plus_row | 2.477726 |
| honest_plus_format | 2.473139 |
| lookup_parent_tautomer_solute | 2.477959 |
| lookup_parent_tautomer_conditions | 2.477959 |

The honest baseline is fixed-parameter LightGBM (250 trees, 31 leaves, learning rate 0.05, seed 17) on allowed inputs, categorical SMILES/solvent/polymer fields, and inexpensive RDKit descriptors. It has no row identifier or group feature. This is a modest baseline, not a tuned molecular model. The same baseline protocol was retained: descriptor function names are columns, so RDKit lambdas sharing names overwrite earlier columns, as represented in the reproducible script. No parameter tuning or test-score-dependent blending was performed.

`row_only` uses original row position and position modulo 10 and 100. `format_only` uses SMILES length and counts of dot and @ characters; `artifact_only` combines those with row features. `honest_plus_artifacts` adds all these inputs to the honest model. A follow-up ablation also adds row features alone (`honest_plus_row`) or format features alone (`honest_plus_format`) to isolate these effects. Format statistics can encode legitimate molecular properties, so predictive power alone does not demonstrate leakage.

**Findings**

1. **No copy or tested chemical-identity overlap across splits.** Every fold has zero train/test family overlap, zero exact allowed-feature matches, and zero canonical-SMILES, stereo-free canonical-SMILES, or fragment/charge/tautomer-parent identity matches. Requiring matching full experimental conditions also has zero coverage. These training-label lookups therefore return the honest fallback unchanged. This covers common serialization variants, stereochemical variants, charge/salt stripping, fragment-parent extraction and canonical tautomers under the stated RDKit transformations.

2. **No useful row-order exploit demonstrated.** The row-only model is worse than the train-mean predictor. Adding row features alone changes mean RMSE by only -0.000232 (about 0.009%), improving 2 of 9 folds and worsening 7. Format features alone account for most of the combined augmentation gain: -0.004819 RMSE versus -0.005725 for all artifacts. This is consistent with a small molecular-representation effect; it does not demonstrate a reliable row-order channel. The row-only model and baseline augmented with row/format artifacts are evaluated independently above. SMILES format models are not automatically exploits: supplied chemical representations retain molecule-size and composition signals that can exist at deployment.
3. **No demonstrated scoring shortcut.** `score.py` excludes the target and group from allowed features. The metric configuration has no target transform, auxiliary scoring input, or group aggregation; it computes ordinary row RMSE. Directly reading held-out labels from the supplied development kit would violate the evaluation protocol and was not attempted as a model.

**Boundaries**

Unrun possibilities include source/publication matching, external database recovery, sophisticated solvent-order equivalence and fraction-unit conversion, cross-family near-neighbor interpolation, and more elaborate order encodings. No external data were retrieved. No claim is made about those possibilities. A stronger honest model may improve on this fixed baseline.

**Reproduce**

Run from this directory:

```bash
python gamer_check.py
python row_probe.py
python augmentation_probe.py
python write_report.py
```

Per-fold evidence: `work/gamer_scores.csv`, `work/row_probe_scores.csv`, `work/augmentation_scores.csv`; match counts and covered-only scores: `work/gamer_diagnostics.json`, `work/coverage_summary.csv`; primary summary: `work/gamer_summary.csv`; process output: `work/gamer_run.log`, `work/row_probe.log`, `work/augmentation_probe.log`. `work/parent_collision_examples.csv` contains 0 distinct solute/family records spanning multiple families after parent normalization. Package versions and input SHA-256 hashes are in `work/gamer_provenance.json`. Original-kit historical files were preserved.

</details>

<details><summary>Historical full panel — Precedent checker</summary>

**Independent full-panel precedent check: MixtureSolDB**

2026-11-10 UTC. Audited final functional definition SHA256
`f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`.
Final source/implementation evidence describes 167,112 measurements, 810 exact
solute structures and 606 families. This role inspected the decision register first,
then rules, actual decisions and current reports. No curation, definition, claims,
controller or gateway change; only this report written. No models fit by this role.

**Verdict**

**Consistent with the applicable rules and the closest accepted precedents. No
established departure requires a new exception or a curator consistency reflection.**
The approved candidate remains natural-log mole-fraction regression. Recommend
retaining it for completed qualification and added-dataset review; do not switch
outcomes because a different scoring scale would look better.

The bounded dapsone correction and PEG incomplete-structure handling are material
facts to explain at the normal final human gate, with their evidence limits. They
are not reasons to invent a separate consistency approval or claim source tables
were recovered when they were not. Model-worthiness is still unconfirmed here:
`probe-status.json` reports task running at this review. No unfinished model score,
no_triviality claim or numerical panel consensus is inferred from that state.

**Inputs and evidence hierarchy**

- `decision-register.json`: generated with `--since
  2026-10-31`, 1,747 selected decisions from 4,288 total and 13 candidate flags.
  Read relevant molecule/repair/metric records and Cases tables; none of the flags
  establishes the present decision as drift or a third exception.
- Actual Myunghwan direction and current `bigsoldb_2` CC: proceed with "loge
  mole-fraction regression" first; another target only if unfavorable evidence.
  The exact direction was checked in the earlier independent screening report.
- Final definition; current claim-auditor focused confirmation; column-auditor
  delivered-ln collision study; split-auditor final identity/fold evidence;
  domain-practitioner dapsone evidence and stated source-access limits.
- Pinned principles, molecule guide, provenance PROV-4/6/7/13/14/15,
  leak checks LEAK-16/17/18/19/20, CLEAN-10/11/16/24, SPLIT-31 and MET-3/5/11.
- Actual checked-out records for qsar_bioconcentration, qsar_oral_toxicity,
  qsar_tid_11, apistox, nci_aids_antiviral_screen and OSSL. Older AI notes are
  distinguished from the actual curator CC decisions and current rule amendments.

This role does not relabel other reviewers' source retrieval as its own. The
current raw reconstruction and primary body-text confirmations are independently
reported by those roles; their original-source gaps remain gaps.

**Choice-by-choice consistency**

| Choice | Closest actual precedent/rule | Assessment and fact that matters |
|---|---|---|
| Natural-log mole-fraction regression first | OSSL scale disclosure, Lennart 2026-11-04/05 (MET-3/5, CLEAN-16); forest_fires log modeling but raw-area scoring, 2026-10-21 | Consistent: curator selected ln concentration; source recommends log mole fraction but has no exclusive model metric. Explicit fallback RMSE scores the ln quantity with identity scorer transform. No accidental exponentiation or double logarithm. OSSL versus forest_fires differs by scored quantity/source criterion; neither mandates changing this approved target. |
| No alternate-target sweep absent a concrete problem | TP-2/TP-6 and principles' right-split-over-score tension | Consistent: valid weak signal is not a reason to invent another target or soften the family split. No bad-label-domain evidence was found in the primary mole fractions. |
| Three typed structures, full fragments/stereo, benchmark-time encoding | qsar_bioconcentration CC 2026-11-01; qsar_tid_11 CC 2026-11-01; qsar_oral_toxicity CC 2026-11-01; CLEAN-24 | Follows accepted molecule policy. No descriptor-dependent collapse and no source-fingerprint advantage defines the dataset. |
| Keep source-named PEG grade with missing exact SMILES | CLEAN-10/24, USE-6, CLEAN-11 | Consistent application, not a new exception. Polydisperse PEG grade is a known experimental input without one exact molecular graph. Named grades preserve information; missing graph is disclosed and can be encoded as missing. Fabricating one oligomer or dropping all affected measured rows would destroy source meaning. There is no accepted precedent requiring such fabrication/exclusion. |
| Normalize solvent ordering, fractions together, active pure endpoint | LEAK-16/19 and CLEAN-1/14 | Consistent: physically identical pure-solvent observations should not differ merely by a zero-share solvent identity. Fraction-basis information stays for interior mixtures. Exact copy removal does not require excluding the entire pure-solvent population. |
| Dedup delivered inputs plus exact delivered ln target | LEAK-19; wine_quality/audiology exact-copy precedents; qsar_oral_toxicity structure-key correction confirmed by curator 2026-11-02 | Follows copy policy. The column auditor measured 20 natural-log collisions differing by at most two raw-float ULPs, not meaningful assay-resolution differences. Exact delivered-value equality is a documented convention, not arbitrary tolerance-based target smoothing. It must not be advertised as preserving every distinct raw floating value. |
| Retain differing continuous outcomes at the same apparent condition | LEAK-20's explicit genuine-label-ambiguity allowance; qsar_tid_11 stereoisomers with measured potency retained (2026-10-21, reaffirmed in 2026-11-01 history) | Consistent. Different experimental conditions/hidden state and extraction errors are possible; not every difference is an ambiguous categorical mislabel. Do not apply the molecule guide's one-structure/two-class-label removal to an entire condition-dependent regression. Actual diagnosed metadata damage is repaired separately. |
| Conservative parent/tautomer/neutral and six observed-core family links, grouping only | SPLIT-31 amendment on qsar_bioconcentration, Lennart 2026-10-26; molecule-guide organic-counterion warning; qsar_tid_11 distinct stereo measurements | Consistent: source-related chemistry defines cold-start families, while all distinct shipped structures and labels remain. No blanket largest-fragment rule replaces a drug by its organic counterion, and no model-score-selected fingerprint cluster defines the split. Explicit metallation/core links are conservative family relations, not claims of identical solubility. Final audit gives zero tested identity-alias crossings in all nine folds and 202 test families each. |
| Stable `bigsoldb_2` ID identifies MixtureSolDB | records.md stable-ID rule (indabax case 2026-10-12); PROV-14 | Consistent: repair/reconciliation stays under its record. The title/source DOI must state the mixture dataset, with unrelated single-solvent BigSolDB DOIs removed from source_links rather than silently renaming or substituting the task. Historical comments remain preserved. |
| Reconcile overlapping older solubility compilations | PROV-4/5/6; hiva_agnostic retirement for full NCI source (Lennart 2026-11-02), PROV-7 distinct-task qualification | Correctly left as a collection/provenance question. Compilation name and size do not establish independent source observations. This review does not authorize also including a correlated older copy or call it a proven duplicate without tracing it. |

**Bounded dapsone repair compared with repair precedents**

The predicate changes 110 dapsone rows in DOI 10.1016/j.molliq.2021.117403 from
ethyl acetate/water to ethyl acetate/ethanol, and leaves that DOI's other 330 rows
untouched. All ten endpoint measurements agree exactly with its existing pure
ethanol endpoints. The domain reviewer read two primary follow-on body passages
that independently identify the original organic pair. The source predicate,
solute and solvent structures, count and 10-temperature/11-fraction grid are guarded.
The current claim auditor independently reconstructed the correction and entire
non-group output. Target values, temperatures and component proportions stay intact.

This follows PROV-13's search/repair-before-keeping-damage principle and PROV-14's
same-record treatment. Closest accepted cases are:

- NCI source charge interpretation, curator 2026-11-02, PROV-13/15: restore the
  represented structure without silently making a different prediction dataset.
- SUPPORT2 source-patient repair and ashrae source-unit repair (provenance Cases):
  correct known release damage rather than hide it by filtering useful observations.
- framingham_heart_study_fhs repair, 2026-10-21, PROV-14: retain same units/features
  and record identity rather than declaring an unrelated new source.

The difference in evidence strength is explicit: original 2021 SI and all interior
cells were not recovered. This is a narrowly corroborated solvent-metadata repair,
not a reconstruction of those unrecovered values. It does not claim the same direct
rowwise source-restoration proof as SUPPORT2/framingham. PROV-13 requires checking
whether clean origin data are available; it does not require pretending access
succeeded or excluding the entire otherwise usable dataset when it did not.
No rule departure follows from the bounded correction when that limit is disclosed.
No human reflection prompt is warranted solely because original SI access failed.
The normal added-review package should expose this repair and its confidence so
the curator understands exactly what is being considered for inclusion.

**Drift, exception count and remaining follow-through**

No prior Myunghwan choice on this record is contradicted. Natural log is now the
actual approved quantity; older either-target AI notes are superseded. No third
exception or new standing-rule amendment is identified. The PEG treatment and
retention of genuine condition-dependent differences apply existing rules' scope
and explicit qualifications; do not invent `Exception to` lines simply to have them.

The final curation assessment should correct the historical 20-column/RecordID
statement, source-link mixture, noisy-version count, pre-encoded-descriptor wording
and BigSolDB-derived "noise floor" claim. Preserve those older notes as history.
Refresh exact final-row/fold probe evidence before declaring model-worthiness, and
use only final-version predictions for that claim. Dataset-specific licence details
not retrieved by the claim role remain an access/provenance note, never a scientific
rejection reason under EV-4. Missing-SMILES warning acceptance and final ship stay
with Myunghwan at the ordinary added-dataset gate. No new consistency question is
needed before completing that package.

</details>

<details><summary>Historical full panel — Advocate opening</summary>

**Advocate opening: MixtureSolDB**

Recommendation: retain and advance the implemented ln mole-fraction candidate toward shipping, conditional on completed qualification of the final 167,112-row artifact. I do not certify the still-running native probes or strict train-only supplement. This brief argues the scientific case; Myunghwan retains final inclusion and warning decisions.

1. **The task has a useful prediction point and the approved outcome.** A process chemist can know structures or polymer grades, initial composition and temperature before a solubility experiment and use estimates to prioritize formulation or crystallization tests. The domain review supports this use while explicitly calling literature-to-deployment fit approximate. This satisfies USE-1/3/5 (Must), with USE-8's declared gap; imperfect experimental context does not by itself establish a nonexistent task. It does not excuse an independently demonstrated data defect.

2. **Natural log is correctly implemented and scored.** Every source primary label is finite and between zero and one; the source log columns agree numerically. The final claim auditor independently reconstructed the sole target and verified all nine scorers against direct RMSE: perfect predictions score zero and a one-ln-unit offset scores one. No exponentiation, extra logarithm, alternate-target sweep or outcome averaging occurs. MET-3 and MET-11 (Must) support this explicit quantity/origin bookkeeping; MET-5 (Should) supports fallback RMSE because the data paper defines no deliberate model-selection criterion. Sparse primary-label problems would need repair, not a target switch chosen for a nicer score.

3. **The identified family-separation defect has been fixed rather than defended.** The current 606-family definition keeps neutral-parent, tautomer, charge and six source-supported core relations together while preserving distinct shipped structures and outcomes. Independent reconstruction and all-nine-fold checks find zero crossings for the tested identities, with 202 held-out families per fold. This is a conservative, label-free application of SPLIT-31 (Should) and honest evaluation under P4, not model-score-selected similarity clustering. Close analogs still occur for 2.89–7.72% of unique test solutes; neither the definition nor this brief promises complete chemical-distance isolation.

4. **The concrete dapsone error received the mild repair supported by its evidence.** The 110-row source/solute/solvent predicate is guarded; ten endpoint values exactly match that DOI's pure ethanol values, and two primary follow-on body passages identify ethyl acetate plus ethanol. Independent final reconstruction confirms only the second solvent identity changes, the other 330 same-DOI rows remain untouched, and labels, proportions and temperatures remain intact. PROV-13/14 (Must) favor restoring this metadata rather than deleting high labels or abandoning the task. Original 2021 SI/interior tables were not recovered: EV-7 (Must) requires keeping that boundary visible, and the repair must not be advertised as full rowwise SI verification.

5. **Residual conflicting measurements warrant a stated limit, not indiscriminate deletion.** The final blind audit reports 1,442 conflicting-input groups, including 84 with a greater-than-tenfold span. They may hide experimental state or further extraction errors; they are not all established intrinsic noise. Yet their empirical identical-input in-sample RMSE bound is 0.06664, so the mere existence of those sparse conflicts does not show that the whole property task is unusable. Delivered-input-plus-ln copy removal follows LEAK-19 (Should); the two-ULP equality nuance is measured and documented. LEAK-20's genuine-label-ambiguity qualification and USE-8 support preserving distinct continuous observations without inventing a mean. Any subsequently demonstrated mapping error still requires repair under PROV-13.

6. **PEG handling preserves known chemistry instead of fabricating it.** Missing exact SMILES corresponds to five named polydisperse grades; those identities and measured conditions remain categorical inputs, while an exact single-molecule graph remains missing. Pure endpoints discard the physically unused component consistently. This applies CLEAN-10/24 (Should) and USE-6 (Must); neither dropping all polymer rows nor inventing a representative oligomer is a more faithful implementation. The missing-SMILES warnings should be proposed to Myunghwan with this precise reason, not marked accepted by the panel.

7. **Existing independent evidence supports pursuing the primary task, with qualification still binding.** The fresh participant test on all nine final folds reports honest RMSE 2.477959 against mean-predictor 2.715437 and no demonstrated identity, row-order or scorer exploit. That is bounded, untuned evidence, not the recommended full-encoding qualification or proof that no exploit exists. TP-1 (Must) and TP-2 (Should) prevent turning a weak probe or limited signal into rejection without a concrete mechanism. The stock diagnostics' full-frame median imputation must remain identified as transductive; the separate train-only supplement is necessary before deployment-honest performance claims. Only final-artifact, completed results can settle model-worthiness. Pending qualification and factual record cleanup are completion work, not a reason to reopen the already-approved target or demand an extra consistency decision.

Evidence read: final claim, column, split, domain and precedent reports; final blind and participant reports; current definition and generated card. Functional definition inspected: f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34. At this reading, task/bigsoldb_2.json still stated 167,122 rows, so its native scores were not used as final-version evidence. Collection-level overlap with older compilations remains unmeasured and does not authorize shipping both collections as independent data.

</details>

<details><summary>Historical full panel — Critic opening</summary>

**Critic opening: MixtureSolDB**

**Recommendation: ship only after qualification provenance is reconciled and the residual source uncertainty is presented honestly at added review.** I do not recommend rejecting the approved ln mole-fraction task, replacing its target, dropping valid PEG measurements or weakening the family holdout. This opening inspected functional definition `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34` and the final phase-A reports. It is provisional while final native/strict model evidence is incomplete.

1. **The current native task result is not identified with the final table.** At this read, `task.log` reports 167,122 rows and five of nine splits, whereas the final definition and refreshed participant artifact have 167,112 rows after the source repair. The result may be historical or have been produced by an earlier process; I have not established its cause. The driver status alone cannot reconcile the mismatch. In addition, the native task/group helpers impute medians from the full encoded frame before folds. Their scores can be labeled transductive diagnostics, but cannot replace deployment-honest qualification. The strict supplement has the correct final hash but only its first fold was present at this opening. **Effect:** an apparently strong score could be attributed to the wrong definition/folds or unsupported preprocessing boundaries. **Rules:** EV-7 (Must), MET-2 (Must), and the split-change requalification requirement; LEAK-30 distinguishes weak input-distribution leakage from label leakage. **Mild remedy:** archive historical native outputs, bind each usable result to exact final row/target/features/fold identities and finish the train-only supplement. No new target or scientific approval is required.

2. **The largest remaining contradiction is localized within one source, so it must not be explained away as interlaboratory noise.** The refreshed blind review finds 84 identical-input groups exceeding a tenfold difference. I independently checked its largest case: at 298.2 K, the same Diazepam structure has a pure-water endpoint `x=0.000001` under PEG-200/water and `x=0.002009` under propylene-glycol/water, both from DOI `10.1021/je3009842`, both first-solvent mass fraction zero. These are the same declared physical condition within one paper, not merely different laboratories. The difference could be omitted experimental state or another extraction/unit/composition error; this test does not establish which. **Effect:** misleading input/target pairs can measure source-recording error rather than solubility prediction. **Rules:** PROV-13 (Must), EV-1/2/6 (Must), USE-8 (Must); quality must not be promoted into a rejection without a demonstrated unfixable validity failure. **Mild remedy:** perform a bounded original-source mixture/endpoint check for this exact case before labeling the residuals as noise. If inaccessible or unresolved, preserve the rows and identify that concrete uncertainty at ordinary added review; do not invent a correction, trim extreme targets or request a substitute target for a better score. The blind review's empirical identical-input RMSE floor is only 0.06664 across the full table, so these sparse conflicts do not themselves prove the entire task unusable.

3. **The 110-row dapsone repair is well corroborated metadata restoration, not complete recovery of its original experiment.** Ten exact ethanol endpoint matches, two primary follow-on body descriptions, narrow source/structure/count/grid guards and independent output reconstruction support the implemented water-to-ethanol substitution. The original 2021 SI and all interior cells remain unrecovered. **Effect:** a correct bounded repair can still coexist with source errors elsewhere; it must not certify all 1,115 source articles or turn a source-limited approximation into a direct-fit task. **Rules:** PROV-13/16 and EV-7 (Must), USE-8 (Must). **Mild remedy:** retain the repair and all outcomes as implemented, show the original-source limit and remaining conflict counts in the human package, and keep approximate fit. No separate consistency gate or unsupported global source correction is warranted.

4. **The PEG warning needs an explicit disposition, not a fictitious molecular graph or an implication that all nine inputs are exact molecular measurements.** The final artifact contains 128 missing solvent-1 structures and 1,309 missing solvent-2 structures, tied to named polymer grades. These grades remain meaningful planned inputs, but one precise molecular graph for a polydisperse PEG grade does not exist here. **Effect:** methods relying entirely on the molecular encoder receive less information for these rows and must also use the grade categories and train-only missing-value handling. **Rules:** USE-6 (Must), CLEAN-24 (Should), CLEAN-10/11 (Should). **Mild remedy:** keep grade identity and measured rows, explicitly propose acceptance of the missing-structure warnings at added review, and show the representation limit. Dropping all PEG rows or inventing a nominal oligomer would be worse remedies.

5. **The reported scope must match 606 held-out chemical families and the exact grouping policy.** The final split audit and refreshed participant attack find zero tested identity overlap in every fold; this resolves the initial defect. Yet 167,112 rows do not supply 167,112 independent new chemistries, repeats reuse the same families, and 2.89–7.72% of unique test solutes still have a close training analog. The short `Grouping.definition` field currently names scaffold/nonstereo/InChI/tautomer keys but omits the implemented neutral-parent and six explicit core relations; the longer notes do disclose them. **Effect:** downstream consumers of only metadata can misunderstand the holdout, and naive row/fold uncertainty can exaggerate evidence. **Rules:** SPLIT-31 (Should), MET-2 (Must), EV-7 (Must). **Mild remedy:** make the short grouping description complete, retain row RMSE as approved, provide family-aware diagnostic summaries, and avoid claiming chemical-distance independence or prospective validation. Collection-level overlap with older compilations remains unmeasured; this need not block MixtureSolDB alone, but it cannot support also including the older candidate as independent data.

**Concessions:** the target domain and ln construction are sound; the scorer directly measures log-scale RMSE on all nine final folds; no retained outcome predictor or demonstrated participant exploit remains; source metadata now verifies open CC BY 4.0 and matching release bytes; the stable historical record ID can remain. The unsupported old 20-column/RecordID, BigSolDB-derived noise-floor and pre-encoded-descriptor statements should be corrected by a current dated assessment rather than erasing history. None of the concerns above establishes an irreparable Must failure or a reason to switch the curator-approved target.

**Evidence read:** final claim/column/split/domain/precedent reports; `clean_room_final/blind-report.md`; `participant_kit_final/task-gamer-report.md`; final definition and generated README; current driver status/log and strict progress; own raw-source read of the two Diazepam endpoint records. No models, gateway requests, curation edits or delegation were performed by this role.

</details>

<details><summary>Historical full panel — Advocate rebuttal</summary>

**Advocate rebuttal: MixtureSolDB**

Recommendation after the critic's five points: the implemented natural-log candidate is worthwhile and can be recommended for shipping at ordinary added review, provided the curator explicitly accepts the source-specific uncertainty and PEG representation limit, and the remaining completion checks finish. No target replacement, invented source correction or automatic acceptance follows from this recommendation.

1. **Qualification provenance: concede the opening concern; its decisive part is now resolved.** The process-reconciliation receipt identifies two historical driver process groups stopped and the current final-data driver retained. The current task JSON states 167,112 rows, 4,227 encoded features and five of nine folds, with no task flags; its stock scores remain transductive diagnostics because of full-frame median imputation. The stronger evidence is the completed strict supplement on functional hash `f2b283fc…21d34`: a fixed model using training-only medians, category levels and variance masks achieves mean ln-RMSE 2.049564 against 2.715437 for the full-training mean, better on all nine full test folds. Mean family RMSE is 1.841098 against 2.523385. Every model trains on a deterministic 50,000-row sample; no holdout selection or tuning is claimed. The no-fit verifier rebuilds current folds and independently rescores saved predictions, checks exact memberships/truths/family separation, all learned categorical levels and 128 fitted medians per fold. This satisfies the specific EV-7/MET-2 (Must) provenance objection for the reported strict evidence; it does not certify every median entry independently or turn repeated folds into independent datasets. At this rebuttal read, native task/leak/dtype have completed, while the native group diagnostic is still running. Completion and receipt checks remain binding.

2. **Diazepam/Clonazepam source discrepancy: concede the mechanism, dispute an automatic exclusion or target switch.** The bounded follow-up makes this more concrete than generic interlaboratory noise: 22 nominal propylene-glycol/water rows disagree with 22 PEG200/water comparison rows in the same source, and the alleged pure-PG endpoints exactly match PEG endpoints. Original mixture tables remain unrecovered; the authoritative NIST page establishes relevant systems, but the requested numerical resource returned HTTP403 and no usable official supplement was found. That source check applies PROV-13 and EV-1/2/6 (Must); it does not establish a correction for interior identities. The appropriate unresolved choice is the one the critic proposes: retain the original observations with this exact source-specific uncertainty and approximate fit, or hold inclusion until the original table resolves it. I favor the former as a bounded benchmark candidate under the principles' explicit repair tension when origin data cannot be reached, because a real, learnable property task remains and no corrected replacement is established. That is a weighing recommendation for Myunghwan, not a claim that uncertain rows are correct or harmless. Do not call all residual discrepancies intrinsic noise, fabricate PEG/PG solvent replacements, trim high labels or hide the issue by changing the target.

3. **Dapsone repair evidence: concede the limit; retain the supported narrow repair.** The claim and split auditors independently reconstructed all final inputs and target values, including the exact 110-row predicate and untouched 330 other same-DOI rows. Ten exact source-ethanol endpoint matches and two published body descriptions support changing only the second solvent identity. Original 2021 SI/interior cells are unverified and must remain stated in the added-review issue and notes. PROV-13/14 and EV-7 (Must) support this bounded restoration with its evidence boundary, rather than pretending the entire source corpus was checked or undoing a supported repair because other source uncertainty exists. The strict model result establishes signal on the implemented version, not experimental truth of every cell.

4. **PEG representation: agree on explicit disposition.** The five named polymer grades remain available at prediction time; the absent single exact graph is a property of the polydisperse representation. Keeping grade categories, typed missing molecular structures and measured rows follows USE-6 (Must) and CLEAN-10/24 (Should). The strict supplement confirms that the recommended molecular encoding can be used without test-derived imputation; it does not manufacture missing chemistry. Myunghwan should accept or decline the missing-structure warning at ordinary review. Neither the advocate nor a passing model may accept it on the curator's behalf.

5. **Scope and grouping metadata: agree on the cheap documentation fix and bounded claims.** Complete the short `Grouping.definition` with the neutral-parent and six explicit core links already present in code and longer notes. This fixes metadata incompleteness, not split construction. Before reusing evidence after that documentation change, record the new definition identity and prove raw inputs, delivered frame/target, learned settings and exact fold membership unchanged; the nine stored predictions then need no new fitting. The strict supplement now supplies the requested family-aware diagnostic while preserving primary row RMSE. The evidence covers 606 families/810 solutes, repeated partitions of the same chemistry and zero tested alias crossings, not complete chemical-distance or prospective independence. Collection overlap remains unmeasured and cannot justify shipping an older compilation as independent observations.

I therefore agree with the critic's bounded source disclosure and completion conditions. The remaining source-specific retain-versus-hold choice and PEG warning disposition belong in the normal added-dataset review. The approved ln target has no demonstrated defect requiring an alternative target. Current strict qualification shows substantive held-out-family signal without relying on the stock probes' global medians; no tuning, model-family superiority or prospective assay replacement is claimed.

Evidence read for this rebuttal: the inlined critic opening; the inlined strict train-only qualification, summary.json, manifest and both saved/no-fit verification records; current native task and leak JSON and driver status; the exact-process reconciliation receipt; the inlined domain source follow-up. No models or curation edits were performed by this role.

</details>

<details><summary>Historical full panel — Critic rebuttal</summary>

**Critic rebuttal: MixtureSolDB**

**Updated recommendation: the ln mole-fraction candidate is qualified enough for ordinary added review, with an explicit source-mapping choice before inclusion.** The earlier stale-score concern is reconciled for the current artifacts; it is no longer an argument against the task. I retain a conservative preference to hold inclusion until the specific 22-row composition ambiguity is resolved, but this is a normal curator weighing choice between documented source uncertainty and waiting for the original table, not a newly invented Must gate, automatic rejection or reason to switch targets.

1. **Useful prediction point: concede.** The advocate correctly limits the fit to approximate pre-measurement experimental screening. The planned structures/grades, proportions and temperature exist before the measured outcome. USE-1/3/5/8 hold as stated. Neither current model scores nor the source's literature selection establish prospective process performance, and the advocate does not claim they do.

2. **Target and metric: concede.** Independent target reconstruction, all-nine-fold direct scorer checks and the completed strict qualification preserve ln(source mole fraction), with identity scoring on that logged quantity. No alternative target or outcome averaging has been introduced. MET-2/3/11 bookkeeping is sound. There is no evidence-based reason to reopen the curator's main-target direction.

3. **Family repair: concede the scientific repair; finish the short metadata description.** Final audits and the participant recheck find no crossing of the tested identities in the actual nine folds. The six core links are conservative grouping relations, not a false assertion that salts or metallation states have equal solubility. The long notes/split comment are adequate; root's planned expansion of `Grouping.definition` should also name neutral-parent and explicit-core relations so standalone metadata does not underdescribe the actual policy. This is a documentation correction. Verify the data/target/feature/fold hashes remain identical and regenerate documentation; no new model fit is needed solely because prose changes. SPLIT-31 and EV-7 support this narrow remedy.

4. **Dapsone repair: concede, with the existing boundary.** The ten exact endpoint matches and two primary follow-on body passages support this 110-row metadata correction more strongly than a generic chemistry expectation. Independent reconstruction proves its bounded implementation and unchanged outcomes. Original 2021 SI/interior values remain unverified; neither side should claim complete original-table restoration. PROV-13/16 and EV-7 favor the implemented narrow repair plus transparent limits over deleting difficult labels.

5. **Residual conflicts: dispute only the treatment of the newly localized 22-row series as ordinary replicate variation.** The advocate already acknowledges possible extraction errors, and I agree that 84 large-span groups do not prove the whole task unusable. The cheap requested follow-up is now complete: DOI `10.1021/je3009842` contributes 44 rows, half nominal PEG-200/water and half nominal propylene-glycol/water. For each of diazepam and clonazepam, both alleged pure-PG endpoints equal the corresponding PEG endpoint exactly while the alleged pure-water endpoints disagree by factors 2009 and 641. This concretely implicates 22 nominal PG/water rows in a composition/mapping uncertainty, beyond a vague laboratory-noise hypothesis. Authoritative NIST metadata confirm PEG/PG/water systems but do not expose the needed mixture table; ACS/NIST numerical retrieval and a bounded official-source search did not recover it. The pattern suggests a possible PEG/PG interpretation, but does not prove enough to rewrite the series or its interior fractions. PROV-13's repair-first duty has been pursued; its source-unavailable limit allows a documented keep-or-hold judgment rather than fictional verification. **An explicit ordinary added-review issue is sufficient:** retain all observations as implemented with the precise 22-row uncertainty and approximate fit, or hold inclusion pending the original mixture table. My conservative preference is the latter; the mediator should present the former's best argument too: only 22 suspected rows among 167,112, no proven correct replacement, and no reason to destroy measured outcomes. Neither alternative licenses a guessed correction, exclusion based on target magnitude or a substitute target. A later factual repair must refresh affected data/splits/probes rather than silently inherit current predictions.

6. **PEG representation: concede.** Grade identity is meaningful and a single exact molecular graph is absent for polydisperse material. Retaining the five grades and missing exact structures follows USE-6 and CLEAN-10/24 more faithfully than fabricating an oligomer. The two missing-SMILES warnings still need their normal human disposition; the panel must not mark them accepted. The completed train-only supplement supports learnability with this representation, but does not recover missing polymer chain distributions or prove subgroup calibration.

7. **Model qualification and provenance: concede the now-completed signal evidence, with scope limits.** The reconciliation receipt records that two historical driver process groups were stopped while the current final-data driver was retained. The current task JSON is 167,112 rows/4,227 encoded features, five of nine folds, 10,000-row cap and no task flags; the current leakage JSON also has 167,112 rows and zero exact-copy matches over all nine shipped folds. These replace the 167,122-row historical result that prompted my opening. More decisively, `the strict qualification summary`, its manifest and saved-prediction verification cover all nine final folds: fixed 200-tree LightGBM, training cap 50,000, full-held-out scoring, train-fitted imputation/masks/category encoding, no holdout selection. Mean RMSE is **2.049564 versus 2.715437** for the full-training-mean baseline, better on 9/9 folds; mean family RMSE is **1.841098 versus 2.523385**. Saved arrays rescore and training samples are subsets of train, disjoint from test. This resolves the concern that favorable signal might require the stock probes' full-frame medians. Native diagnostic scores remain transductive and bounded; the strict single-model supplement is not HPO or a full model leaderboard. Repeats do not create nine independent chemical populations. TP-1/2 and EV-7 support retaining the main candidate while completing/recording any remaining native group/dtype output and final artifact manifest.

**For the mediator:** no demonstrated irreparable Must failure, no target/scorer failure and no reliable tested participant exploit remains. The live inclusion question is the specifically documented source uncertainty, alongside normal PEG warning acceptance. Require factual record cleanup, complete final metadata/documentation and exact artifact provenance. Do not turn unavailable SI into a claim that source quality passed, and do not require an open-ended audit of every article as a new gate.

**Evidence read for this rebuttal:** advocate/opening.md; strict summary/manifest and nine saved-prediction verifications; current native task/leak JSONs; process-reconciliation receipt; domain `JE3009842_FOLLOWUP.md`; original phase-A and participant/blind reports. No new model, source request, curation edit, gateway/controller operation or delegation occurred in this role.

</details>

<details><summary>Historical full panel — Strict train-only qualification</summary>

**Strict train-only qualification supplement**

Completed on final functional MixtureSolDB definition SHA256 `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`.

**Fixed LightGBM mean RMSE: 2.049564 natural-log units, against 2.715437 for the full-training-side mean; better on all nine folds.**
Fold RMSE range: 1.844997–2.220950. Mean relative RMSE reduction is 24.52% when calculated from these means. This is bounded fixed-model qualification, not a tuned leaderboard estimate.

**Strict preprocessing and fit boundaries**

- The primary target remains ln of measured mole-fraction solubility; the scorer evaluates this log quantity directly. No target sweep, hyperparameter search, holdout selection, early stopping, or split change occurred.
- Use all nine actual final grouped folds: 167,112 measurements, 810 solutes and 606 families; 202 test families per fold. Every test row is scored.
- Deterministically sample 50,000 rows from each corresponding training side, then fit all transformations on that sample only. The mean baseline uses every row in the corresponding full training side. The cap can disadvantage the model; this run does not establish full-training performance.
- Cache the installed fixed recommended encoding by unique molecular structure, without fitting any transformation to train or test outcomes: RDKit 2D descriptors, 166 MACCS keys and 1,024 ECFP4 count positions per structure. The cache uses exactly `encode_smiles` with `rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1`; direct encoder calls on 257 actual rows per molecular column verify identical float32 cached values, with explicit missing-vector handling.
- Three structures contribute 4,221 fixed numeric columns; temperature and two fractions add three, for 4,224 before filtering. Remove all-missing or zero-range columns based solely on the sampled training side, leaving 2,380–2,501 columns depending on the fold. This is an unsupervised training-only variance mask, not target-informed feature selection.
- Fit `SimpleImputer(strategy="median")` only on the sampled training numeric matrix. Fit categorical OneHotEncoder levels only there, with unknown test levels ignored. No global medians or all-frame learned preprocessing are used.
- One fixed model: `LGBMRegressor(n_estimators=200, learning_rate=0.05, num_leaves=31, random_state=4267, n_jobs=2)`, other settings from the recorded LightGBM version. No change was made after seeing a test score.

**Results**

| Repeat | Fold | Train sample / full | Full test | RMSE ln | Full-train mean RMSE ln | Mean family RMSE ln |
|---|---|---:|---:|---:|---:|---:|
| 0 | 0 | 50,000 / 111,988 | 55,124 | 2.175329 | 2.867657 | 1.833627 |
| 0 | 1 | 50,000 / 108,235 | 58,877 | 1.989978 | 2.606862 | 1.833074 |
| 0 | 2 | 50,000 / 114,001 | 53,111 | 1.919985 | 2.684601 | 1.766920 |
| 1 | 0 | 50,000 / 109,759 | 57,353 | 2.178996 | 2.646071 | 1.907023 |
| 1 | 1 | 50,000 / 113,591 | 53,521 | 2.092581 | 2.809091 | 1.815184 |
| 1 | 2 | 50,000 / 110,874 | 56,238 | 1.959352 | 2.702459 | 1.851130 |
| 2 | 0 | 50,000 / 109,503 | 57,609 | 2.220950 | 2.823376 | 1.951040 |
| 2 | 1 | 50,000 / 115,856 | 51,256 | 1.844997 | 2.513419 | 1.769864 |
| 2 | 2 | 50,000 / 108,865 | 58,247 | 2.063910 | 2.785397 | 1.842017 |

The mean of per-family RMSEs averages 1.841098, against 2.523385 for the baseline. This supplementary family-weighted diagnostic does not replace the declared row RMSE or introduce a new aggregation task.

The fixed model learns signal for held-out solute families, supporting continued qualification of the approved main target. This result alone does not establish superiority of a model family, exact experimental accuracy, prospective validity or final inclusion. Repeated folds share source families; the nine values are not nine independent datasets and no naive confidence interval is claimed.

**Reproducibility and no-fit verification**

`manifest.json` records source, definition, full row-content and target hashes; fixed encoding identity and cached-vector hash; versions, model settings and sample policy. Every fold saves full/sample training indices, full test indices, exact test truths, predictions, a baseline mean, feature mask, fitted medians, categorical levels, model text, per-family errors and identity hashes. `run_strict.py` reproduces the fits.

`verify_saved.py` performed no model fitting. It rebuilt the final native folds, verified source/frame/target hashes, exact saved full-fold membership and truths, sampled training membership/disjointness, family separation and baseline means, and independently rescored all nine saved prediction arrays. For each fold it additionally recomputed 128 fitted median entries directly from the cached unique structure vectors and sampled training rows, and checked every learned categorical level against that sampled training side. All passed; it does not assert an independent recomputation of every median entry. `no-fit-verification.json` and `saved-prediction-verification.json` retain the checks.

Current definition hash at no-fit verification: `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`; fit definition hash: `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`. Both match. Runtime of all nine fits plus encoding was 251.9 seconds. All outputs remain local and gitignored; no curation edits, dataset build, gateway, controller or publication occurred.

**Final documentation/style update: evidence reuse verified**

The final documented definition is SHA256 `d00f833a112c360e44c065f7d69040b556827f5ecbd5a5d9a5224d8dddbe7d30`.
The original model-qualified source remains SHA256 `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`,
preserved in the state directory as `model-qualified-definition.py`. The original fit manifest,
per-fold artifacts and summary were not relabeled, rewritten or assigned the new source hash.

`verify_metadata_reuse.py` independently compared the preserved fit source with the final source.
After normalizing only the two explicitly permitted description strings (`curation_comments` and
`Grouping.definition`), function docstring text and the splitting of message-free conjunctive
assertions into equivalent sequential guards, the complete ASTs match. Module constants,
all executable function/method bodies under that narrow guard normalization, target/problem
specification, metric spec, special features and scientific grouping fields match. The style
normalization preserves assertion evaluation order and short-circuit failure behavior for these
message-free guards; it does not discard arbitrary executable changes.

The audit rebuilt the final actual table and scorer, then compared its full ordered row-content
and target fingerprints with the ORIGINAL strict fit manifest. It matched 167,112 rows, 606
families and the exact nine original full training/test index arrays. Saved truths, sampled
training membership, group separation, full-training means, prediction hashes and fitted-model
hashes also matched. The current native scorer independently rescored every original prediction
array: mean RMSE stays **2.049564 natural-log units versus 2.715437 baseline**. No new fit ran.
The final source stayed unchanged during verification.

This proves reuse for the final source and the recorded source/data/target/feature/preprocessing/
model/scorer/fold identities. It does not assert that arbitrary future edits can reuse predictions.
`final-metadata-reuse-verification.json` retains both source hashes and the original fit manifest
and summary hashes, the allowed AST differences, executable/constant hashes and all per-fold
checks. The two descriptions now state the neutral-parent/core-family links accurately and disclose
the unresolved 22-row DOI 10.1021/je3009842 mixture-metadata concern. The added note changes no input,
target or cohort in this qualification. Scientific disposition of those rows remains a curator
question; this evidence-reuse result does not settle it.

</details>

<details><summary>Historical full panel — Final model-evidence reuse</summary>

**Final source evidence reuse**

**Final documentation/style update: evidence reuse verified**

The final documented definition is SHA256 `d00f833a112c360e44c065f7d69040b556827f5ecbd5a5d9a5224d8dddbe7d30`.
The original model-qualified source remains SHA256 `f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34`,
preserved in the state directory as `model-qualified-definition.py`. The original fit manifest,
per-fold artifacts and summary were not relabeled, rewritten or assigned the new source hash.

`verify_metadata_reuse.py` independently compared the preserved fit source with the final source.
After normalizing only the two explicitly permitted description strings (`curation_comments` and
`Grouping.definition`), function docstring text and the splitting of message-free conjunctive
assertions into equivalent sequential guards, the complete ASTs match. Module constants,
all executable function/method bodies under that narrow guard normalization, target/problem
specification, metric spec, special features and scientific grouping fields match. The style
normalization preserves assertion evaluation order and short-circuit failure behavior for these
message-free guards; it does not discard arbitrary executable changes.

The audit rebuilt the final actual table and scorer, then compared its full ordered row-content
and target fingerprints with the ORIGINAL strict fit manifest. It matched 167,112 rows, 606
families and the exact nine original full training/test index arrays. Saved truths, sampled
training membership, group separation, full-training means, prediction hashes and fitted-model
hashes also matched. The current native scorer independently rescored every original prediction
array: mean RMSE stays **2.049564 natural-log units versus 2.715437 baseline**. No new fit ran.
The final source stayed unchanged during verification.

This proves reuse for the final source and the recorded source/data/target/feature/preprocessing/
model/scorer/fold identities. It does not assert that arbitrary future edits can reuse predictions.
`final-metadata-reuse-verification.json` retains both source hashes and the original fit manifest
and summary hashes, the allowed AST differences, executable/constant hashes and all per-fold
checks. The two descriptions now state the neutral-parent/core-family links accurately and disclose
the unresolved 22-row DOI 10.1021/je3009842 mixture-metadata concern. The added note changes no input,
target or cohort in this qualification. Scientific disposition of those rows remains a curator
question; this evidence-reuse result does not settle it.

</details>


<details><summary>Historical full panel — Cold review editor</summary>

**Cold review editor: MixtureSolDB**

Verdict: ready for the curator after two small presentation corrections; no additional scientific issue or approval gate is needed.

Read the draft cold, then checked its claims against the final definition, generated README, appended panel evidence and strict-train-only final-source evidence-reuse report. This role made no model fit, source request, network request, controller operation or canonical-file edit.

**Concrete edits, most important first**

1. Update the panel summary's pending-evidence language, because the independent final-source audit is already completed and appended in the same draft.

   Old: “Final documentation and guard-style edits require unchanged-data/fold proof before reusing model evidence.”

   New: “An independent no-fit audit verified that the final documentation and guard-style edits preserve the complete data, target, features, scorer, preprocessing and model identities, all nine folds and saved predictions, so the model evidence applies to the final definition.”

   Reason: the present summary makes qualification sound pending despite the final-source audit. The audit identifies final source d00f833a112c360e44c065f7d69040b556827f5ecbd5a5d9a5224d8dddbe7d30 and original fit source f2b283fcdfdc03d141642eb476ea64558757cea66be2eb0b9487680b42721d34, retains the original fit identity and proves bounded reuse. Keep the historical mediator report intact; its earlier follow-through list is history, while the leading summary should state the present result.

2. Remove the relative run-artifact path from the appended split-audit evidence without deleting the report.

   Old: “See the inlined final model-evidence reuse audit and `final-metadata-reuse-verification.json`.”

   New: “The full final-source evidence-reuse audit is reproduced in the Strict train-only qualification panel below; its verification record preserves the exact source and artifact identities.”

   Reason: the review format prohibits local paths in the public review, and the evidence is already inlined. The replacement preserves traceability without requiring the curator to access a run directory.

**Checks and boundaries**

- The review has exactly two remaining scientific choices: retain the specific 22-row source-mapping uncertainty or hold inclusion, and keep explicit polymer grade identities with explained warnings or narrow the cohort. They are correctly ranked, and no new target decision is requested.
- Both issues have plain-language problems, task effects, decisive evidence, implemented options, alternatives, recommendations and explicit decisions. Issue 1's neutral recommendation accurately preserves the genuine advocate/critic disagreement; it does not invent a panel consensus.
- The task is recoverable from the source and generated use-case tab: a chemist chooses experimental conditions before measurement; each row is one experimental solubility observation; supplied structures, mixture fractions and temperature precede the outcome; the target is natural log of measured mole fraction and RMSE scores those log values directly. Whole solute families, including all conditions for each solute, are held out. This is approximate literature-based experimental property prediction.
- Current counts and qualification match the supplied evidence: 167,112 rows, 810 solutes, 606 families, all nine actual folds, mean RMSE 2.049564 against 2.715437, training capped at 50,000 rows and full test sides. Repeated folds are explicitly dependent. Full-frame median imputation and smaller caps in supplementary native diagnostics are disclosed. No full-training or prospective-performance claim is implied.
- The 22 suspect rows are distinguished from 22 comparison rows and the separate source-backed dapsone repair. PEG warning cell counts are distinguished from affected-row counts. Original SI/source-table limits remain visible, and a model score is not presented as proof of source correctness.
- The two issue tables each mark one implemented option and give consequences, pros and cons. Rule references are in footnotes. There is no duplicate issue number, embedded report-block label inside an issue, unsupported additional choice, media dependency or absolute local path. Apart from edit 2, no run-directory path needs removal.
- Full scientific panel sections remain inline, including their historical and current evidence boundaries. No panel section or source evidence should be removed for brevity. The draft does not claim inclusion, warning acceptance or build approval.

No further curator-facing issue is warranted by this editing review.

</details>
