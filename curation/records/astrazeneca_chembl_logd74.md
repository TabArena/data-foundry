---
unique_name: astrazeneca_chembl_logd74
name: lipophilicity
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Grouped)
- Experimental Results
- 'Samples: Over Time'
- 'Time: Dated'
collections:
- ChemPile
original_source: Other
year: '2015'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6019/CHEMBL3301361
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/lipophilicity ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/lipophilicity ; MoleculeNet mirror: https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv (MoleculeNet) ; https://tdcommons.ai/single_pred_tasks/adme/#lipophilicity-astrazeneca'
- https://arxiv.org/abs/2505.12534
- https://www.ebi.ac.uk/chembl/api/data/assay/CHEMBL3301363
- https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv
- https://www.ebi.ac.uk/chembl/document_report_card/CHEMBL3301361/
v2_path: datasets/_dev/tabarena-v0pt2/astrazeneca_chembl_logd74/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: 4,200 logD7.4 values measured at one company under one
shake-flask protocol, the standard lipophilicity regression of molecular ML. Verdict and priority unchanged; the
deposit now reads as experimental results rather than a catalogue cut, and the scaffold hold-out is the tree's leaf.
- Source: AstraZeneca's deposition in ChEMBL, document CHEMBL3301361, "Experimental in vitro DMPK and physicochemical
  data on a set of publicly disclosed compounds" (Mark Wenlock and Nicholas Tomkinson; doc_type DATASET, ChEMBL_20,
  creation_date 2015-01-14, doi 10.6019/CHEMBL3301361). The assay is CHEMBL3301363: "ASTRAZENECA: Octan-1-ol/water
  (pH7.4) distribution coefficent measured by a shake flask method described in J. Biomol. Screen. 2011, 16, 348-355.
  Experimental range -1.5 to 4.5"; the ChEMBL API returns 4,200 activities of standard_type LogD7.4 for it, in
  document CHEMBL3301361, which carries no document year (re-checked 2026-11-25). The copy in use is MoleculeNet's
  Lipophilicity.csv (columns CMPD_CHEMBLID, exp, smiles; header previewed), also served by TDC as
  Lipophilicity_AstraZeneca (Harvard Dataverse file 4259595, 4,200 compounds in TDC's own size table). One table.
- Use case: a DMPK scientist or medicinal chemist, before a compound is made or progressed, estimates its logD7.4
  ("Lipophilicity is an important feature of drug molecules that affects both membrane permeability and solubility",
  MoleculeNet Sec. 3.1.6); the deposition itself names no actor or decision, so the use case is ours to state and the
  fit is approximate until the curator settles it. Collection: one deposit of a closed compound set measured under
  one protocol, each value a fixed property of the molecule and no date per row (`Samples: No Time Dimension`; the
  deposit's ChEMBL document has no year); one activity per compound, so no `Entities: Recur` (the TabBench-Bio build
  of the same file reports "no invalid or duplicate structures"); type `Experimental Results` — a company's own
  deposit of molecules measured by a laboratory protocol, not the growing database that serves it (SPLIT-34 rule 4).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the Bemis-Murcko scaffold) because [EXP.meets] is a chemical
  series the data does not contain (the chemist asks for compounds of series this DMPK set never measured, the case
  SPLIT-31 was amended on) and [EXP.kind-key] yes (the SMILES compute the scaffold; 2,447 scaffold groups over the
  4,200 compounds in the TabBench-Bio build, enough to hold out whole); open: whether the use case is instead a new
  compound of the series the company already works on ([EXP.meets] → L-EXP.random), which is what MoleculeNet's
  random split assumes while TDC's scaffold split does not, and how the ring-less compounds are grouped (the
  `qsar_bioconcentration` amendment keeps them, and the bare benzene ring, apart).
- Siblings and duplicates: `tdc_lipophilicity_astrazeneca` (TabBench-Bio) is the same 4,200 compounds as 2,048-bit
  ECFP4 fingerprints, a processed copy of this source (PROV-4, PROV-6): one of the two records stays, and the SMILES
  route is the one CLEAN-24 asks for — the fingerprint table cannot even compute the scaffold its own split needs.
  `hepatocyte_clearance_astrazeneca` is another assay of the same deposition, a different target and task (PROV-7),
  not a duplicate; the deposit also holds solubility, pKa and plasma protein binding assays. External collections:
  ChemPile / ChemNLP (`lipophilicity`), MoleculeNet, TDC, TabBench-Bio.
- Better data: none found (searched 2026-11-25 for a larger public logD7.4 set): the hand-curated logd74 collection
  of 1,130 organic compounds is smaller, and the larger public lipophilicity compilations (SangsterLogP and the
  ChEMBL logP extractions used by D-MPNN) measure logP, not logD at pH 7.4, which cannot be pooled without a pH
  correction. The deposit's own sibling endpoints are other tasks, not better data.
- Papers and pages: the ChEMBL document report card CHEMBL3301361; MoleculeNet (Wu et al. 2018, Chem Sci, Table 1 and
  Sec. 3.1.6); TDC's ADMET benchmark group.
- Metric: the two task definers disagree. MoleculeNet's Table 1 gives "Lipophilicity SMILES 1 Regression 4200 Random
  RMSE" ("For each dataset, we propose a metric and a splitting pattern that best fit the properties of the
  dataset"); TDC's ADMET group gives MAE with a scaffold split. No unique source metric, so the fallback `rmse` on
  logD (MET-5, MET-8), which agrees with MoleculeNet; inputs none beyond the scaffold group the split needs, which a
  build computes from the SMILES.
- Risks for /add-dataset: the assay's stated range (-1.5 to 4.5) suggests censored values at the ends, so check for
  pile-ups at the bounds (CLEAN-11); take the ChEMBL route or the MoleculeNet CSV, both of which keep the compound
  id, and check salt forms, stereoisomers and near-duplicate structures that collapse onto the same 2D descriptors
  and can sit on both sides of a scaffold split (LEAK-17, LEAK-19, CLEAN-24); ChEMBL's licence is CC BY-SA 3.0 (no
  verdict reason, EV-4).
- Priority: gap 0 (chemistry & material science has 15 accepted datasets and regression 85, neither thin), use case 0
  (the deposition names no decision), source + (a documented assay with its protocol), shape + (4,200 compounds),
  risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the benchmark ChemPile (https://arxiv.org/abs/2505.12534); the curator's Zotero collection, item 52: "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ..."; the curator's Zotero collection, item 82: "Amsterdam Medical Data Science".
- as published: 4,200 compounds (TDC / MoleculeNet); in ChemPile-LIFT 42,000 text prompts over 1 config(s); target: logD 7.4; access: open.
- Why: Predict the octanol/water distribution coefficient (logD at pH 7.4) of a compound | one company, one assay protocol, real project compounds: a consistent measurement, and the first publication is traceable in ChEMBL rather than through the DeepChem CSV the list links | One lab, one protocol, real measurements: ...
- Adds: | no lipophilicity or ADME task in the benchmark; sibling endpoints in the same deposition. The MoleculeNet and TDC copies drop the ChEMBL ids, the ChEMBL route keeps them | No lipophilicity or DMPK dataset is recorded. The deposit's other assays (solubility, PPB, clearance) are sibling tasks from the same source.
- Notes: AstraZeneca deposition in ChEMBL (CHEMBL3301361), curated by MoleculeNet. Licence CC BY-SA 3.0 (ChEMBL). Reported already in this run by bench_2609.07441 as tdc_lipophilicity_astrazeneca (TabBench-Bio uses an ECFP4 version). Features: SMILES string only, so a container keeps the string and adds computed descriptors, ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: the same data, once as SMILES and once as a fingerprint build (`tdc_lipophilicity_astrazeneca`; PROV-6). The curator keeps one, or both as distinct tasks.

**CC (2026-11-25, Andrej):** accepted for adding, after the re-screening of the TabBench-Bio candidates on the current rules.
- Added with `/add-dataset`; the open points go into this record's `## Review`.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes, with every change the panel settled already applied (the group key moved to the structure without its salts, solvents and repeated fragments, which closes LEAK-17 on the one row that straddled 6 of 9 folds; the five download pages pinned by sha256 and the six salt/hydrate records asserted under PROV-8; the fit statement, the time-basis reason and the stereoisomer decision rewritten, with ten refuted or missing statements corrected); disputed: USE-8 with selection.md's marker (the critic opened for `approximate` plus `Selection Bias` and withdrew both in its rebuttal; shipped as `direct` with no marker) and PROV-13 against CLEAN-24 on the six multi-fragment records (repair the four ChEMBL re-pointed onto hydrates after the deposit, or keep the shipped SMILES whole); for the curator: issues 1-5.
- Priority 2: gap 0, use case 0, source +, shape +, risk - (chemistry and regression are both well covered; the deposit names no actor and no decision, so the use case is ours; the assay, its protocol and its reporting range are documented on the source's own page under a DOI; 4,190 compounds in 2,411 chemical series; one feature column, so a score depends on the benchmark's encoding, and issue 4 may change four rows' structures).

**CC (2026-11-26, Andrej):** the review decisions on the five open issues.
- Issue 1, as implemented: the fit stays `direct` and no selection marker is added; both selections fall under the written carve-outs, and the definition keeps their measured cost.
- Issue 2, discuss, still open: "There is no leak since the repeated entities would both be either in train or test, so we can just keep. Or are there real issues coming with doing B?" Answered in the review: no leak either way, but B scores five compounds twice, pairs feature-identical rows with targets 0.03 to 0.57 apart, and would need a 0.5 scoring weight per row to count a compound once.
- Issue 3, change to A: the collection facts become `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension`, and the definition's time-basis reason says so. The split does not change: the recoverable order dates a compound's first public disclosure, not its measurement (one 2015 deposit, one document, one assay), the target does not drift along it (Spearman 0.028), and a middle block is as hard as the newest when equally isolated (R^2 0.542 to 0.705, tracking the close-analog share at Pearson 0.81).
- Issue 4, as implemented: all six multi-fragment rows ship whole and the four ChEMBL re-pointed are not repaired; the definition now states the drift as a kept, documented fact, with the four ids, the bound on the score and what it costs a reader.
- Issue 5, discuss, still open: "If there is disagreement, we most likely still don't want the fallback but whatever is the right metric. So in this case a human should be presented all arguments of the different sources and then decide on the right metric, where an ai can also make a recommendation for one of the sources or the fallback as always." The issue now lays MoleculeNet's RMSE and TDC's MAE side by side with the fallback and recommends TDC's MAE; the metric ships unchanged until the decision.

**CC (2026-11-26, Andrej):** the second round of review decisions; issues 2 and 5 are settled and nothing is open.
- Issue 2, as implemented after the answer: the five twice-measured compounds stay averaged into one row each, and the departure is written down as the exception it is (record, definition notes, and an exception row of the splits rules' Cases table). No leak either way, as he read it: both rows of a pair carry the same structure and scaffold, so no pair straddles a fold.
- Issue 5, change to B, his words: "Option B: mae in log units, TDC's choice." The declared metric becomes `mae` in log units with the origin `context`, taken as TDC's declared criterion for this data and not as the regression fallback; the reason names TDC as the definer whose task design this definition follows and MoleculeNet's RMSE as the other definer's choice, not taken because it is paired with the random split over MoleculeNet's reprocessed copy.
- Measured, unchanged by the metric: over eight candidate models the ranking is identical under MAE, RMSE, median absolute error, the share within 0.5 and within 1.0 log, Spearman and a 3-band accuracy (per-fold Kendall tau 1.00 on 7 of the 9 folds, 0.929 on the other two); an L1-trained LightGBM does not win on MAE either (0.552 against 0.528).
- `dataset check` after the change: 0 errors, 0 warnings, 0 info over 28 checks; the README is regenerated and carries `mae`. Not built: no container exists for this folder.
- Not changed: the data, the split, the rows and every other field. The errors in log units in the notes were measured as RMSEs over the nine shipped folds and are labelled as such; the one bound stated in the metric's own units now reads about 0.0014 on the declared MAE per fold.

**Exception to SPLIT-26 (2026-11-26, Andrej):** we do not ship the source's rows as they are: the five compounds the assay measured twice (CHEMBL1626, CHEMBL170, CHEMBL273575, CHEMBL499, CHEMBL517712) ship as one row each, holding the mean of their two activities, where the rule that keeps the source's rows says deduplicating with averaged targets makes a different dataset. Three facts set the case apart from `superconductivity`, which kept both rows and counted a composition once with a scoring weight: the repeats are 0.12% of the deposit here (5 compounds, 10 of 4,200 activities) against 40% of the rows there; they are true protocol replicates inside one document and one assay, not separate literature reports; and there is no split consequence either way, both rows of a pair carrying the same structure and therefore the same scaffold, so no pair straddles any of the nine folds. Serves P4: the Must above the kept rule lets the source's use case decide what one prediction is, and here it is the compound, so the scored unit matches the prediction unit, no compound is weighed twice in a fold, and no pair of feature-identical rows with targets 0.03 to 0.57 apart puts an error floor into the score.

**CC (2026-11-26, Andrej):** the declared metric and the declared split are signed off and the verdict is ship.
- Verdict: ship. All five issues of the review are resolved, no record field disagrees with the definition and nothing is parked; the record's `Yes` stands and the dataset joins the accepted set, to be built later.
- The declared metric is checked as it stands: `mae` in log units under the context origin, TDC's declared choice for this data rather than the regression fallback it shipped with until 2026-11-26 (the sign-off line below).
- The declared split is checked as it stands: whole chemical series held out on the Bemis-Murcko scaffold, 3 repeats of 3 folds (the sign-off line below).
- No change to `dataset.py` and nothing built: the folder has no container, as the second round of decisions already records.

CC (2026-11-26, Andrej): the declared metric (`mae` in log units, origin `context`, taken as TDC's declared choice for exactly this task and not as the regression fallback, with MoleculeNet's RMSE the other definer's choice and not taken) is checked and stays as declared.

CC (2026-11-26, Andrej): the declared split (grouped on `scaffold`, the Bemis-Murcko scaffold of the structure without its common salts and solvents, 2,413 groups over 4,195 compounds, 3x3 folds, `UnseenGroup`, split leaf `L-EXP.kind`) is checked and stays as declared: a test compound belongs to a chemical series this assay never measured, which is the prediction the use case asks for, and 23.0% of test compounds still have a close training analog against 46.7% under random draws of the same test sizes.

CC (2026-11-26, Andrej): issue 6, option B. The five ids that carry two activities are not one compound measured
twice; each is two compounds the deposit registered and measured separately, merged onto one ChEMBL id since
(quinine and quinidine, atropine and its tropane-defined form, and three more). All ten activities are dropped.
- The set is 4,190 compounds in 2,411 scaffold groups; the split is unchanged in kind and the largest group is
  still the bare benzene ring at 76 compounds (1.8%). The group counts in the CC above predate this.
- The averaging decided in issue 2 is withdrawn, and the SPLIT-26 departure is rewritten around the merge: the
  source's own rows can no longer be rebuilt from the source, because ChEMBL serves one structure for both values.
- The metric is unchanged. Its reason loses the clause about "the assay's own repeats", a spread that is
  stereochemistry between two compounds rather than assay repeatability.
- Issue 7 is opened and left open, on three numbers in the notes: the noise floor quoted as about 0.11 from 43
  enantiomer pairs re-measures as 31 pairs and SD 0.211; MolLogP's R^2 of 0.134 re-measures as -0.167 against the
  training mean; and every fold figure predates the drop, re-measuring in the same range but not on the same values
  (RMSE 0.698 -> 0.710, MAE 0.528 -> 0.542). None is read outside the notes and none changes a decision.

## Review

**Outcome:** added. AstraZeneca's shake-flask logD7.4 assay as deposited in ChEMBL, 4,190 compounds with the
structure as the one feature, whole chemical series held out in 3x3 grouped splits and scored by `mae` in log units.
A full review
panel ran (seven evidence agents, an advocate and a critic over two rounds, a mediator) and recommends shipping after
changes; everything the panel settled is applied. The signal is real and not trivial: an untuned LightGBM beats the
training mean on all nine folds (R^2 0.659), while a 1-NN over the same fingerprints does worse than that mean. The
one leak the panel found is closed by the group key, now the structure without its common salts and solvents and
without repeated identical fragments: a levofloxacin hemihydrate, written as its parent twice plus a water, had been
grouped apart from the same chemical and landed on the other side of 6 of 9 folds. The download is pinned by the
checksums of its five pages and guarded by an assert on the six activities ChEMBL records on a salt or hydrate; the
fit statement, the time-basis reason, the stereoisomer decision and ten refuted or missing statements are rewritten.
The AI recommends shipping it, and the curator signed it off. All five decisions were settled on 2026-11-26: the
direct fit with no selection marker, the collection facts, the six multi-fragment rows kept whole, the averaging of
the five twice-measured compounds kept and written as an exception, and the metric, which becomes TDC's `mae` in log
units under the context origin in place of the regression fallback. On the same day the declared metric and the
declared split were checked and the verdict set to ship: nothing is left to decide, no record field disagrees with
the definition, and the folder waits only for a build, since no container exists for it yet.

**Main points:** Nothing left to decide; the dataset is signed off and ships. All five issues are resolved, and on
2026-11-26 the declared metric (`mae` in log units, TDC's choice rather than MoleculeNet's RMSE or the fallback it
shipped until then) and the declared split (whole Bemis-Murcko scaffolds held out, 3x3 folds) were checked and the
verdict set to ship. The five twice-measured compounds stay averaged into one row each, written down as the
exception it is. Not built yet.

**Record judgment:** valid. One company's deposit of one assay, with the protocol, the reporting range and the
document quoted on the source's own page; the screening's reading of the source holds, two of its counted numbers do
not (2,447 scaffold groups reproduces as 2,414 on the shipped compounds and 2,413 on the key now used, and its
coverage counts of 15 chemistry and 85 regression datasets are 12 and 74 against today's accepted definitions).
Neither changes a field.

**Issues for the curator:**

1. **Is the fit direct, with no marker for the way the compounds were selected?**

   * **Problem:**
     - The ground truth a chemist would get instead of asking the model, the shake flask itself, reports only -1.5
       to 4.5 and is run on the compounds a design round sends it, so both selections are ones the real setting
       makes too[^sel2].
     - The deposit holds only compounds AstraZeneca later disclosed in patents, and only those whose logD7.4 fell
       inside that range, so two selections stand between this table and the design ideas a chemist would ask about.
     - The panel crossed on whether either makes the fit approximate or earns the marker that flags objects picked
       for measurement, and both sides ended at a direct fit with no marker.
   * **Effect on the task:** Nothing in the data changes, and the definition names both selections and their
     measured cost whatever the grade is. What changes is what a reader takes an RMSE of 0.698 to cover: the
     decision the use case names, flagging a compound as too lipophilic, is made at the end of the range where the
     model is most shrunk, and a chemotype nobody has measured scores worse than the headline.
   * **Experiments:** Nine shipped folds, untuned LightGBM on the recommended encoding; the analog share is the
     share of test compounds with a training compound at Tanimoto 0.7 or more (Morgan radius 2, 2,048 bits),
     re-measured on the folds the new group key gives (two panel agents independently measured the same pair as
     22.9% against 46.0% on the old key; the shrinkage and the analog-stratified error are theirs).

     | Measured | Value |
     |---|---|
     | test compounds with a close training analog | 23.0% (fold SD 2.1) |
     | the same over random draws of the same test sizes | 46.7% (SD 1.3) |
     | RMSE on test compounds with no close analog | 0.823 |
     | RMSE on test compounds with one | 0.544 |
     | mean error above logD 3.5 | -0.71 (under-called) |
     | mean error below logD 0 | +0.98 (over-called) |

     The range is a selection of compounds and not a censoring of values, so a value at a bound is a real
     measurement:

     | Where | Compounds |
     |---|---|
     | exactly at -1.5 | 1 |
     | in the band -1.5 to -1.0 | 36 |
     | in the band 4.0 to 4.5 | 135 |
     | exactly at 4.5 | 4 |
     | outside the range | 0 |
     | carrying a relation or upper-value flag | 0 of 4,200 |

   * **Consistency:** None of the nine shipped molecule datasets carries a selection marker for the way its
     compounds were picked for testing, and six of them ship a direct fit; the three molecule records that do carry
     the marker carry it for another mechanism (two classes drawn from two registries, designed actives and decoys,
     a compilation of many sources). `superconductivity` moved to approximate because its actor screens a population
     that is almost entirely the excluded class, which is not the shape here: the ground truth a chemist would
     obtain instead, the shake flask itself, has the same reporting bound[^sel].
   * **Panel:** The critic opened asking for the marker and an approximate fit on the `superconductivity` reading,
     then withdrew both after finding the carve-out for tested compounds; the advocate conceded a marker it did not
     owe and kept the direct fit, arguing the two selections separately.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Direct, no marker, both limits written (implemented) | the fit stays `direct` and the record carries no marker; the notes name the disclosure population, the end-of-range shrinkage and the analog-stratified error | follows the carve-out for tested compounds that stand for a screen's candidates; the norm of the molecule family; the assay the prediction replaces has the same bound | the disclosure population stays a gap the reader must weigh for themselves |
     | B | Direct with a selection marker | the record gets `Selection Bias`; the definition is unchanged | the page then flags the disclosure population | would be the family's first marker for a tested-compound selection; the carve-out says no |
     | C | Approximate with a selection marker | `fit="approximate"` in the definition and `Selection Bias` on the record | follows `superconductivity` | there the real setting meets the excluded class; here it meets the same range bound, and the shift in which structures were measured is what the scaffold split tests |

   * **Recommendation:** A, because both selections fall under the written carve-outs[^sel2] and the family has
     decided the same way nine times. **Decision:** A, B or C?

   **Notes for the AI:** on B, add `Selection Bias` to the record's `decision_markers` through the store API and name
   the disclosure population in the record's comments. On C, also set `fit="approximate"` in `dataset.py`, say in
   `fit_reason` which selection makes it approximate, re-run `dataset check` and regenerate the README. The measured
   numbers behind the bullets are already in `curation_comments` ("The fit is direct, and these are its limits").

   [^sel]: **USE-8** (Must): the fit is judged against the real-world setting, and the reason names the selection
     either way; the fit is direct when the real setting meets the same selected cases, approximate when it does not.

   [^sel2]: selection.md, "No marker when" (Lennart, 2026-10-27): no marker where "tested compounds
     stand for the candidates a screen would test (the QSAR sets): how far a new candidate lies from the tested ones
     is a question for the split", and none where "the selection is how the label comes to exist, so every dataset of
     the task has it".

   **Andrej (2026-11-26, as implemented):** A.

   **Resolved (2026-11-26, Andrej):** A. The fit stays `direct` and the record carries no selection marker. Both
   selections fall under the written carve-outs: the shake flask a chemist would run instead reports the same -1.5
   to 4.5, and tested compounds stand for the candidates a screen would test, which is a question for the split.
   The definition keeps both limits with their measured cost (the patent-disclosed population, and the shrinkage at
   the ends of the range: -0.71 above logD 3.5, +0.98 below 0). Nothing in the data, the split or the definition
   changes.

2. **Record the averaging of the five twice-measured compounds as the first exception to keeping the source's rows?**

   * **Problem:**
     - The rule that lets the source's use case decide what one prediction is, replicates averaged, outranks the
       one that keeps the source's rows as they are, so the averaging the definition does is permitted[^rep].
     - What is missing is the departure written down where the next curator will find it: five compounds carry two
       activities each and ship as one row holding their mean.
     - The note in the definition cites the rule about one feature vector carrying two labels, which is a different
       case and does not carry the call.
   * **Effect on the task:** None on the data, the split or the score. A departure recorded nowhere is a departure
     the next curator cannot check, and this is the first of its kind.
   * **Experiments:** The five pairs, from the raw activities; all five are one document, one assay, distinct
     `record_id`, `potential_duplicate` 0, and all five share a scaffold with their own copy, so the split is the
     same either way.

     | Compound | Lower | Higher | Spread | Shipped |
     |---|---|---|---|---|
     | CHEMBL1626 | 3.04 | 3.48 | 0.44 | 3.26 |
     | CHEMBL170 | 2.16 | 2.26 | 0.10 | 2.21 |
     | CHEMBL273575 | 2.08 | 2.11 | 0.03 | 2.095 |
     | CHEMBL499 | -0.35 | -0.22 | 0.13 | -0.285 |
     | CHEMBL517712 | -0.66 | -0.09 | 0.57 | -0.375 |

   * **Consistency:** `superconductivity` (2026-11-08, issue 1 B) kept both rows and counted a composition once
     through a scoring column instead. Three facts set this case apart: 0.12% of rows here against 40% there; true
     protocol replicates in one document against separate literature reports; and no split consequence either
     way[^rep].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the averaging and write the exception (implemented) | nothing in the data, which already averages; the exception is added to the record, the definition's notes and a cases row of the splits rules | both measurements count and the compound stays one row; the departure becomes checkable | one more exception to carry |
     | B | Ship both rows per compound | 4,200 rows, the same structure twice | the source's rows as they are | re-creates a repeated-entity exposure the definition closed; the same compound would be two predictions |
     | C | Keep one of the two values | 4,195 rows, one measurement dropped | the source's rows as they are | throws away a measurement and does not say which, as MoleculeNet's copy does |

   * **Recommendation:** A, with the three distinguishing facts named. **Decision:** A, B or C?

   **Notes for the AI:** on A, add an `**Exception to SPLIT-26 (2026-__-__, <curator>):**` line to the record with the
   three facts and `Serves P4: ...`, a bullet to `curation_comments` replacing the LEAK-20 citation with SPLIT-23, and
   a row of kind `exception` to the Cases table of `.claude/skills/knowledge-curation/references/splits.md`. On B or C,
   change the `groupby` in `_clean`, re-run `dataset check` and the leak and group probes.

   [^rep]: **SPLIT-26** (Should): keep the source's rows; deduplicating with averaged targets is a different dataset.
     **SPLIT-23** (Must), which outranks it: the source's use case decides what one prediction is, a row or a whole
     group, replicates averaged. **LEAK-20**, cited in the definition until now, is about one feature vector
     occurring with two different labels and its remedy is to drop every copy.

   **Andrej (2026-11-26, discuss):** There is no leak since the repeated entities would both be either in train or
   test, so we can just keep. Or are there real issues coming with doing B?

   **Answer (AI, 2026-11-26):** no split leak arises either way, and what B costs is a double-counted compound and
   a pair of rows a model cannot tell apart.

   * On the leak you are right, and it is measured, not assumed: each of the five compounds has the same structure
     in both of its activities, so both rows carry the same scaffold and land on the same side of every one of the
     nine folds. B changes no split and opens no leak.
   * What B does change is the scoring unit. The use case asks for one number per compound (one structure in, one
     logD7.4 out), and under B five compounds are scored twice while every other compound is scored once, so those
     five carry twice the weight in the fold's score.
   * The two rows of a pair are feature-identical with different targets: the one feature column is the structure,
     which is identical, and the targets differ by 0.03 to 0.57 log units (mean 0.254). No model can separate them,
     so whatever it predicts it is wrong on at least one by the spread; the pair contributes an error floor that
     says nothing about the model.
   * Counting the compound once under B needs a scoring weight of 0.5 on each row, which is a new scoring column
     (the route `superconductivity` took, where 40% of rows were repeats). Without it the score is weighted as
     above; with it, B scores exactly what A scores and only the row count differs.
   * The size of all this: 5 compounds, 10 of 4,200 activities, 0.12% of the set.

     | Under option B | |
     |---|---|
     | rows | 4,200, over 4,195 distinct compounds |
     | compounds scored twice | 5 |
     | spread between the two values of a pair | 0.03 to 0.57 log units, mean 0.254 |
     | folds where a pair is split across sides | 0 of 9 |
     | to count a compound once | a weight of 0.5 per row, as a new scoring column |

   * A third point, smaller: a feature-identical pair carrying two labels is the shape the duplicate rule names, so
     B re-opens a flag that A closes; A keeps both measurements and the compound as one row.

   **Andrej (2026-11-26, as implemented):** A, after the answer.

   **Resolved (2026-11-26, Andrej):** A, confirmed after the answer: the five twice-measured compounds stay
   averaged into one row each, and the departure is written down where the next curator will find it. The exception
   line now stands in the record's comments, in the definition's notes and as an exception row of the splits rules'
   Cases table, with the three facts that set the case apart: the repeats are 0.12% of the deposit against 40% of
   the rows at `superconductivity`, they are true protocol replicates inside one document and one assay, and the
   split is the same either way, both rows of a pair carrying the same structure and scaffold. Nothing in the data,
   the split or the score changes.

   **Re-decided (2026-11-26, Andrej):** overturned by issue 6. One of the three facts that carried this decision,
   "they are true protocol replicates inside one document and one assay", is refuted by the data: each of the five
   is two compounds the deposit registered and measured separately, which ChEMBL has merged onto one id since. The
   averaging is withdrawn, the ten activities are dropped, and the SPLIT-26 exception is rewritten around the merge
   instead of around replicates.

6. **The five "twice-measured" compounds are merged pairs, not repeats: drop them?**

   * **Problem:**
     - MoleculeNet's copy of CHEMBL_20 holds 4,200 rows with **4,200 distinct compound ids and 4,200 distinct
       structures**, so the deposit measured 4,200 compounds and repeated none.
     - The five ids that carry two activities today are five pairs of separately registered compounds that ChEMBL
       has merged since, each a stereo-defined form and an undefined or differently defined one. One pair is
       quinine and quinidine; another is atropine and its tropane-defined form.
     - Averaging therefore builds a row for a compound that was never measured, and gives quinine quinidine's
       value. It also contradicts the stereoisomer decision three rows down, which keeps 168 compounds in 77
       2D-structure groups precisely because stereoisomers "are distinct compounds, not copies".
     - The merge did not take in every stereoisomer: nomifensine's other enantiomer (CHEMBL400964) and a third
       cinchona alkaloid (CHEMBL1294) keep their own id and their own row, so the set still holds the near-copies
       the split has always had.
   * **Effect on the task:** ten activities leave, 4,195 compounds become 4,190, and five rows that paired a
     structure with a value measured on a different compound are gone. The split is unaffected in kind: 2,411
     scaffold groups instead of 2,413, the largest still the bare benzene ring at 76 compounds (1.8%).
   * **Experiments:** each pair was resolved by its 2D structure group, taking as partner the member that no longer
     carries an activity of its own; every pairing is confirmed by an exact value match against MoleculeNet.

     | Merged id | The two compounds CHEMBL_20 registered | logD7.4 |
     |---|---|---|
     | CHEMBL1626 | CHEMBL1626 (both centres defined) + CHEMBL315157 (neither) | 3.48 / 3.04 |
     | CHEMBL170 | CHEMBL97 quinine + CHEMBL522505 quinidine | 2.16 / 2.26 |
     | CHEMBL273575 | CHEMBL273575 (racemate) + CHEMBL51697 (one enantiomer) | 2.08 / 2.11 |
     | CHEMBL499 | CHEMBL173706 (undefined) + CHEMBL499 (S) | -0.35 / -0.22 |
     | CHEMBL517712 | CHEMBL9751 (fully undefined) + CHEMBL517712 (tropane defined) | -0.09 / -0.66 |

     Six of the twenty MoleculeNet ids that no longer carry this activity are the members that lost their id; four
     are the compounds whose activity moved onto a salt or hydrate form; ten are other drift.
   * **Consistency:** the stereoisomer decision in this same definition keeps stereo variants as distinct
     compounds. Dropping is the only option that agrees with it, since the two structures cannot be recovered from
     this download.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the averaging, rewrite its reason | 4,195 rows; the SPLIT-26 exception rests on the merge | row count as signed off | five rows still average two different compounds |
     | B | Drop the five merged ids (implemented) | 4,190 compounds; ten activities leave | no row holds a value measured on another compound; agrees with the stereoisomer decision | 0.24% of the deposit leaves, five of them compounds other benchmarks carry |
     | C | Restore both structures from MoleculeNet | 4,200 rows, matching MoleculeNet and TDC | the deposit's own task | reads structures out of the processed mirror this definition rejects |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Andrej (2026-11-26, as implemented):** B.

   **Resolved (2026-11-26, Andrej):** B. The ten activities of the five merged pairs are dropped and the dataset
   ships 4,190 compounds. `MERGED_IDS` names each pair and `_clean` asserts the exact set, so a further merge fails
   the check rather than changing a row unseen. The metric reason loses its appeal to "the assay's own repeats
   differ by 0.254 log units on average": that spread is stereochemistry between two compounds, not assay
   repeatability. `mae` itself is unchanged, since it rests on TDC's declaration for this task.

7. **Three measured numbers in the notes do not reproduce, or predate the drop.** (open)

   * **Problem:**
     - `fit_reason` and the stereoisomer decision both state "a single measurement of this assay has an SD of about
       0.11 (the 43 enantiomer pairs in the set, matching AstraZeneca's published 0.07 to 0.10)", and the claim is
       what says the task is not noise-limited.
     - Re-measured on the shipped data, no recipe gives 43 pairs: 31 pairs are true enantiomers (every tetrahedral
       centre inverted), 64 2D-structure groups hold exactly two compounds, and 106 within-group pairs exist in all.
     - The SD does not reproduce either. On the 31 enantiomer pairs it is 0.211, not 0.11. About 0.12 is reachable
       only by dropping the one 1.55 pair, which this definition already calls a label error - defensible, but the
       exclusion is not stated.
   * **Effect on the task:** nothing in the data, the split or the metric. It is a claim in the notes that a reader
     would use to judge whether the headline error is near the measurement floor, and at 0.211 the margin is half
     what the text implies.
   * **Second, MolLogP.** The notes call MolLogP "the strongest single feature of the task (R^2 0.134 alone,
     chosen on 6 of 9 splits)", and the six multi-fragment rows are argued from it. A re-measure on the shipped
     folds (random forest on MolLogP alone, R^2 against the training mean) gives -0.167, so the feature does not
     beat the training mean by itself. The two numbers are probably different baselines rather than a different
     fact, but the recipe behind 0.134 is not written down and could not be reproduced.
   * **Third, the fold figures predate the drop.** Every RMSE, MAE and analog share quoted in the notes and in the
     splits comment was measured on the 4,195-row build, before issue 6. An independent re-measure on the shipped
     4,190 rows (untuned LightGBM on the recommended encoding, nine folds) puts them in the same range but not on
     the same values, and the gap is bigger than five rows can explain, so the panel's recipe and this one differ
     in details not recorded:

     | | in the notes (4,195) | re-measured (4,190) |
     |---|---|---|
     | LightGBM RMSE | 0.698 | 0.710 |
     | LightGBM MAE | 0.528 | 0.542 |
     | R^2 against the training mean | 0.659 | 0.651 |
     | test compounds with a close analog | 23.0% | 22.7% |
     | the same, random draws | 46.7% | 45.3% |
     | RMSE, no close analog | 0.823 | 0.747 |
     | RMSE, with a close analog | 0.544 | 0.567 |
     | 1-NN RMSE | 1.243 | 1.243 |
     | training-mean RMSE | 1.204 | 1.202 |
     | mean error above logD 3.5 | -0.71 | -0.75 |
     | mean error below logD 0 | +0.98 | +1.01 |

     Nothing here changes a decision: the signal is real on either set of numbers, the 1-NN baseline still loses to
     the training mean, and the analog-stratified gap still runs the same way.
   * **Options:** (a) restate the noise floor as the measured 31 pairs and SD 0.211, give MolLogP's baseline, and
     re-run the fold figures once under one recorded recipe; (b) keep about 0.12 with the 1.55 label-error pair
     named as excluded, and otherwise as (a); (c) drop the noise-floor and MolLogP claims and leave only
     AstraZeneca's published 0.07 to 0.10 and the fold figures.
   * **Recommendation:** (b). The excluded pair is already argued to be an error, and one recorded re-run would
     settle all three at once. **Decision:** (a), (b) or (c)?

   **Notes for the AI:** the noise floor appears in `fit_reason` and in the "Stereoisomers keep their own row"
   decision text; MolLogP in the multi-fragment bullet. None of the three is read outside the notes, so no field
   or build depends on the answer.

3. **Do the record's collection facts change to samples over time?**

   * **Problem:**
     - The record says the source has no time dimension, but these compounds were first disclosed between 1974 and
       2022 and ChEMBL dates them, so two rows' prediction points can lie decades apart.
     - The split does not change either way, and the definition's reason has been rewritten to the measurement
       already, so what is open is only the pair of facts on the record.
     - The choice is whether a parent source's first-publication year counts as the row's date or only as an order.
   * **Effect on the task:** None on the data or the split. The facts are what the next definition built on this
     source will read, and what a scan for datasets with a usable clock will find.
   * **Experiments:** Eight blocks of 524 compounds held out of the molecule-id order at the same training size,
     untuned LightGBM on the recommended encoding; the analog share is measured as in issue 1.

     | Held-out block | R^2 | Close training analogs |
     |---|---|---|
     | newest eighth | 0.526 | 5.5% |
     | oldest eighth | 0.672 | 10.9% |
     | middle 1/8 | 0.705 | 35.9% |
     | middle 2/8 | 0.698 | 40.8% |
     | middle 3/8 | 0.602 | 15.6% |
     | middle 4/8 | 0.542 | 9.2% |
     | middle 5/8 | 0.590 | 7.6% |
     | middle 6/8 | 0.613 | 10.9% |

     A middle block is as hard as the newest one when it is equally isolated, and the score tracks the analog share
     (Pearson 0.81) rather than recency. The order itself is recoverable: a compound's first publication year, read
     from its other ChEMBL documents, follows the molecule id at Spearman 0.912 over the 146 datable of 160 sampled
     compounds. The target does not move along it (Spearman 0.028), and every value arrived in one 2015 batch
     (contiguous record ids, one document, one assay, no document year).
   * **Consistency:** `qsar_tid_11` pulled the same first-publication years from ChEMBL and changed its split on them
     (2026-11-11), and `drug_induced_autoimmunity_prediction` pulled first-approval years. The fact that sets this
     deposit apart is the single 2015 batch: a compound's literature year is not when its measurement entered, which
     the rules for catalogues exclude and which this deposit is not[^facts].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Samples: Over Time` and `Time: Dated` | two record tags change; no split change | matches the wording for a parent source that keeps the date, matched by an id; ChEMBL gives a calendar year for 146 of 160 sampled compounds | the year is a disclosure year, not the day the row was made |
     | B | `Samples: Over Time` and `Time: Inferred` | two record tags change; no split change | the honest reading if a first-disclosure year is a lagging proxy with an unknown lag; what the split auditor and both briefs propose | understates a year a parent source really does record |
     | C | Keep `Samples: No Time Dimension` (implemented) | nothing changes | no churn | refuted by the measurement; fails the test of whether two rows' prediction points could lie at different times |

   * **Recommendation:** A or B, both defensible and neither changing the split; A on the wording of the rule, B if
     the curator holds that a first-disclosure year is not the row's date. **Decision:** A, B or C?

   **Notes for the AI:** change the tags through the store API after a fresh `load_record`, then run
   `tests/test_collection_types.py` and `tests/test_time_basis_facts.py`. The definition's `time_basis` reason already
   carries the measurement and the distinguishing fact, so it needs no further change under A or B.

   [^facts]: **SPLIT-32** (Should): the collection facts are read from the source, `Samples: Over Time` where two
     rows' prediction points can lie at different times, `Time: Dated` where "a parent source keeps the date ...
     matched by an id", `Time: Inferred` where only an order can be rebuilt. **SPLIT-37** step 4, which excludes a
     literature year that is not when the measurement entered, governs catalogues; this deposit is not one
     (**SPLIT-34** rule 4).

   **Andrej (2026-11-26, change):** Option A: `Samples: Over Time` and `Time: Dated`. Why does the split not change
   once we reconstruct the order?

   **Resolved (2026-11-26, Andrej):** A. The record now carries `Samples: Over Time` and `Time: Dated` in place of
   `Samples: No Time Dimension`, and the definition's time-basis reason states both facts. The split stays the
   scaffold hold-out, for three reasons already measured: the order we can reconstruct dates a compound's first
   public disclosure and not its measurement, since all 4,200 activities of this assay arrived in one 2015 deposit,
   one document, one assay; the target does not drift along that order (Spearman 0.028), as logD7.4 is a fixed
   property of the molecule under one protocol; and a block held out of the middle of the order is as hard as the
   newest block when it is equally isolated (R^2 0.542 to 0.705 over the eight blocks, tracking the close-analog
   share at Pearson 0.81 rather than recency). A forward split would therefore test chemical neighbourhood under
   another name, which is what the scaffold split tests directly.

4. **Repair the four rows whose structure ChEMBL re-pointed after the deposit?**

   * **Problem:**
     - For four of the six multi-fragment records the shipped structure is not what AstraZeneca deposited: ChEMBL
       re-pointed those activities onto hydrate records registered years after the 2015 release, and a 2015-era copy
       still carries the parent id with the identical value for all four.
     - Six of the 4,195 records hold more than one fragment, so the descriptors a benchmark computes from them are
       the substance's and not the compound's, worst on docetaxel trihydrate, whose MolLogP reads 0.79 against the
       compound's 3.26 on a compound whose logD is 3.40.
     - Each of those rows names its parent, so restoring the deposit's structure costs six requests on ChEMBL's
       molecule endpoint, and it changes shipped feature values.
   * **Effect on the task:** Almost nothing on the score, six rows in 4,195 bounding the change at about 0.001 RMSE
     per fold even if every one of them were predicted a full log worse. It matters for anyone who reads a row: on
     four of them the structure we publish is not the one the source published, and the strongest single feature of
     the task is computed from it.
   * **Experiments:** Descriptors of each variant (molecular weight / MolLogP / topological polar surface area). The
     compound's own values are the last column except for docetaxel, whose trihydrate the deposit itself recorded.

     | Row | Substance | Shipped | Fragment-dedup only | Salts and solvents off | Both |
     |---|---|---|---|---|---|
     | CHEMBL5315124 | levofloxacin hemihydrate | 740.76 / 2.26 / 181.52 | 379.39 / 0.72 / 106.51 | 722.75 / 3.09 / 150.02 | 361.37 / 1.54 / 75.01 |
     | CHEMBL3545252 | docetaxel trihydrate | 861.94 / 0.79 / 318.95 | 825.91 / 2.43 / 255.95 | 807.89 / 3.26 / 224.45 | 807.89 / 3.26 / 224.45 |
     | CHEMBL5416410 | dasatinib hydrate | 506.03 / 2.49 / 138.01 | unchanged | 488.02 / 3.31 / 106.51 | 488.02 / 3.31 / 106.51 |
     | CHEMBL5483011 | indinavir hydrate | 631.82 / 2.04 / 149.53 | unchanged | 613.80 / 2.87 / 118.03 | 613.80 / 2.87 / 118.03 |
     | CHEMBL1355736 | theophylline monohydrate | 198.18 / -1.86 / 104.18 | unchanged | 180.17 / -1.04 / 72.68 | 180.17 / -1.04 / 72.68 |
     | CHEMBL1409 | fluvoxamine maleate | 434.41 / 2.91 / 131.44 | unchanged | unchanged | unchanged |

     MolLogP is the task's strongest single feature (R^2 0.134 alone, chosen on 6 of 9 splits). The parent structure
     is not in the download: the activity record carries the parent's id but only the measured molecule's structure,
     so a repair costs six extra requests on the molecule endpoint. All six parents are a single fragment, and none
     of them is separately a row of this set.
   * **Consistency:** `qsar_tid_11` recovered its structures from the ChEMBL release the data came from and found its
     salt forms through the molecule hierarchy rather than through InChIKeys. `clock_protein_toxicity` is the
     precedent for keeping a row whose features are not the molecule's with a note. The rule that keeps the shipped
     SMILES whole is what holds the two un-drifted rows in place[^repair].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Repair the four re-pointed rows | the four take the deposit's parent structure; docetaxel and the maleate stay as deposited and are named in the notes | restores what the source published; verifiable against an independent 2015 copy; the mildest rung that is a repair | six more requests in the download; a rebuild; four rows' features change |
     | B | Ship the stripped structure for all six | the shipped SMILES becomes the structure without salts and solvents | one line, no new download; all six descriptor sets become the compound's | also rewrites docetaxel, which the deposit itself recorded as a trihydrate; a cleaning choice dressed as a repair |
     | C | Keep all six whole and name them in the notes (implemented) | no data change; the notes name the six rows and the size of each descriptor shift | nothing to download; the shipped SMILES stays the source's | leaves four rows carrying a structure the deposit does not have, with the origin reachable |
     | D | Rebuild from the 2015 release files | the row set itself becomes the deposit's | the strongest answer to the drift | a multi-gigabyte download; the only measured row-set difference from the 2015 copy is the same four re-pointings |

   * **Recommendation:** A. It is the ladder's first rung for the rows it covers, it is verifiable against an
     independent copy of the same assay from the deposit's own year, and it stops where a repair would turn into
     cleaning. This changes shipped feature values, so it is a task change: its own pull request, and the rebuild
     waits for the curator's ask. **Decision:** A, B, C or D?

   **Notes for the AI:** on A, read the parent structures from `https://www.ebi.ac.uk/chembl/api/data/molecule/<id>`
   for the four ids (`CHEMBL33`, `CHEMBL1421`, `CHEMBL190`, `CHEMBL115`), add the files and their checksums to
   `download_description`, substitute them in `_clean` before `canonical_smiles`, keep `SALT_FORMS` as the drift
   guard, and re-run `dataset check` and the leak, task and group probes; the group key needs no change, since
   `group_structures` already reduces those rows to the parent. On B, replace the shipped `SMILES` with
   `group_structures(...)` and say so in `curation_comments` and `task_summary.changes`.

   [^repair]: **PROV-13** (Must): what we ship is the deposit; a damaged value is repaired from the origin where the
     origin is reachable. **PROV-14**: a repair stays under its record even when the table then differs from the
     release. **CLEAN-24** and its application in molecules.md: "Keep the shipped SMILES whole. Use the stripped form
     only for the copy key and the scaffold." **CLEAN-11**: a row whose features are not the thing's can stay with a
     note. The tension row "Repair against cleaning around damage (P5 over P7)" is this case.

   **Andrej (2026-11-26, as implemented):** C.

   **Resolved (2026-11-26, Andrej):** C. All six multi-fragment rows ship whole and the four re-pointed ones are not
   repaired: no extra request in the download, no change to a shipped feature value, no rebuild. The drift stays a
   kept and documented fact rather than an open question, so the definition's note now names the four re-pointed ids
   and the 2015-era copy that still carries them under the parent, the bound on the score (six rows in 4,195, about
   0.001 RMSE per fold even if each were a full log worse), that the group key already reduces all six to their
   parent so no split is touched, and what the decision costs: on those four rows the structure we publish is the
   hydrate ChEMBL now records and not the compound the deposit published, and the descriptors a benchmark computes
   from them are the hydrate's.

5. **Which metric does the task take: MoleculeNet's RMSE, TDC's MAE, or the fallback?**

   * **Problem:**
     - The two benchmarks that made a task of this deposit declare different metrics, MoleculeNet RMSE and TDC MAE,
       while the deposit itself declares none.
     - The definition ships the regression fallback, which happens to be `rmse`, so the metric is settled by a
       default rather than by reading what either definer meant.
     - This issue first asked only whether to write that default into the metric rules; the curator's guidance
       below turns it into the choice of the metric itself.
   * **Effect on the task:** Which number a leaderboard reports and how heavily it weighs a large miss; it changes
     nothing in the data or the split, and it does not change the ranking, which is identical under every measure
     tested.
   * **Background:** The two definers side by side, with what taking each would mean here.

     | | MoleculeNet (Wu et al. 2018, Chem Sci) | TDC ADMET benchmark group |
     |---|---|---|
     | declares | RMSE, in its dataset table row for Lipophilicity, next to "Random" | MAE, next to "Scaffold" |
     | its stated reason | "For each dataset, we propose a metric and a splitting pattern that best fit the properties of the dataset" | none on the page |
     | the split it pairs the metric with | random over the 4,200 compounds, which we rejected as not the use case | the Bemis-Murcko scaffold hold-out, which is the split we ship |
     | its copy of the data | strips salts, restandardises tautomers, keeps one value of each repeated measurement | the same 4,200 compounds, served from its own Dataverse file |
     | taking it would mean | `rmse`, the number the definition already computes | `mae` in log units, a change of the declared metric |

   * **Experiments:** Eight candidate models on the nine shipped folds, scored under seven measures.

     | Measure | Agreement with the RMSE ranking |
     |---|---|
     | MAE, median absolute error, within 0.5 log, within 1.0 log, Spearman, 3-band accuracy | identical ranking; per-fold Kendall tau 1.00 on 7 of 9 folds, 0.929 on the other two |
     | MAE, with an L1-trained LightGBM added | the L1 model does not win on MAE either (0.552 against 0.528) |

   * **Consistency:** `nci_aids_antiviral_screen` (2026-11-02) is the complement and took the later definers' metric
     because they agree; five qsar siblings take the regression fallback where the paper's measure is a house
     measure; `gse40279_methylation_age` moved off the fallback to absolute error on 2026-11-26, because its field
     states and acts on one unit[^met].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `rmse` as the fallback (implemented) | nothing changes: the metric stays the problem type's default, with the reason it has now | nothing to re-run; the number coincides with what MoleculeNet declares; it weighs the large misses at the ends of the range, where the too-lipophilic flag is set | the metric is decided by a default rather than by reading either definer |
     | B | `mae` in log units, TDC's choice | declares `mae`, the reason naming TDC as the definer whose task design this definition follows and the field's reading of an error in log units | the definer whose split we actually ship; an error in log units is how the decision reads it, the share within half a log being the band a design round works in; the assay's own repeats differ by 0.25 log units on average, which a squared error punishes harder than the decision does | a change of the declared metric and of its origin; a miss at the ends of the range, where compounds are flagged, then counts like one in the middle |
     | C | `rmse`, declared as MoleculeNet's choice | the same scorer as today, but the origin and reason become the definer's declaration instead of the default | says where the number comes from and leaves the scorer untouched | takes the metric of the definer whose split and whose processed copy we rejected |

   * **Recommendation:** B. Both definers are later definers, so neither is a source metric and the tie is ours to
     break; the one we follow everywhere else in this definition is TDC, whose scaffold split and per-compound
     prediction unit are what we ship, while MoleculeNet's random split over its own reprocessed copy is what we
     rejected. C is the honest second if you hold that a miss at the ends of the range should weigh more than one in
     the middle, since it ships today's scorer and only says where it comes from. Nothing rides on it numerically:
     the ranking is the same under either. **Decision:** A, B or C?

   **Notes for the AI:** on B, `metric = Metric.from_context("mae", reason=...)`, the reason naming TDC's
   declaration, MoleculeNet's, and why the tie is broken this way; on C, `Metric.from_context("rmse", reason=...)`
   with MoleculeNet's declaration as the reason. Either way the origin is `context` and not `source`, since a later
   definer's metric is not the source's; re-run `dataset check`, and update the ranking bullet in
   `curation_comments` and the metric block of the generated README. The cases row this issue first proposed is
   held until the metric is decided: under the curator's guidance it would record that two disagreeing definers are
   put to a human with both arguments and a recommendation, not that the fallback applies, and it is a change to
   `.claude/skills/knowledge-curation/references/metrics.md` that belongs in the items across datasets.

   [^met]: **MET-5**: a metric a later definer set is no source metric. **MET-8**: the fallback for a regression is
     `rmse`. **MET-11**: the `context` origin, where the source defines no metric but the task makes one obvious.
     **MET-4** by analogy is what `nci_aids_antiviral_screen` used where the later definers agree.

   **Andrej (2026-11-26, discuss):** If there is disagreement, we most likely still don't want the fallback but
   whatever is the right metric. So in this case a human should be presented all arguments of the different sources
   and then decide on the right metric, where an ai can also make a recommendation for one of the sources or the
   fallback as always.

   **Andrej (2026-11-26, change):** Option B: mae in log units, TDC's choice.

   **Resolved (2026-11-26, Andrej):** B. The declared metric is `mae` in log units, taken as TDC's declared
   criterion for this data rather than as the regression fallback, with the origin `context`: neither benchmark is
   the source, the deposit defines no metric, and the task makes TDC's the obvious one, so the fallback is
   overruled rather than filled in. The reason now names TDC as the definer whose criterion is taken, because its
   task design is the one shipped here (the Bemis-Murcko scaffold hold-out and one prediction per compound), and
   MoleculeNet's RMSE as the other definer's choice that is not taken, because it is paired with the random split
   over MoleculeNet's own reprocessed copy, both rejected in this definition; the argument for the fallback is
   gone. The measured ranking invariance stays: over eight candidate models the ranking is identical under MAE,
   RMSE, median absolute error, the share within 0.5 and within 1.0 log, Spearman and a 3-band accuracy (per-fold
   Kendall tau 1.00 on 7 of the 9 folds, 0.929 on the other two), and an L1-trained LightGBM does not win on MAE
   either (0.552 against 0.528). `dataset check` passes with 0 errors, 0 warnings and 0 info over 28 checks, and
   the regenerated README carries `mae`. The errors in log units quoted elsewhere in the notes were measured as
   RMSEs over the nine shipped folds, are labelled as such and were not re-run; the one bound that was stated in
   the metric's own units, the six multi-fragment rows, now reads about 0.0014 on the declared MAE per fold.

**Review panel:** ship after changes (mediator). Full tier, all ten roles: a claim auditor, a column auditor, a split
auditor, a domain practitioner, a blind reviewer, a task gamer and a precedent checker, then an advocate and a critic
with one rebuttal round, then a mediator who re-measured the crossed points. The panel ran before the group key was
changed, so its reports carry the numbers of that build (2,414 groups, 78 stereo groups of 170 compounds, dummy
1.203, 1-NN 1.239, R² 0.666); the issues, the outcome and the definition carry the re-run's (2,413, 79 of 172, 1.204,
1.243, 0.659). Claim audit: 45 claims, 35 hold, 7
refuted, 3 untested. Blind review: would include; main concerns the publicly recoverable labels and six
multi-component structures. Task gamer: 14 attacks, the only positive one transductive self-distillation at +0.007,
which carries no label information. Debate: both sides reached ship after changes and
agreed on every change; disputed: the fit grade and the marker (issue 1), and which rung of the remedy ladder the six
multi-fragment rows take (issue 4).

<details><summary>Claim auditor</summary>

45 claims of the definition and the record tested on the rebuilt frame and the shipped 3x3 splits, the five raw ChEMBL
pages, MoleculeNet's `Lipophilicity.csv`, and against the ChEMBL API, the MoleculeNet paper and TDC. 35 hold, 7 are
refuted, 3 are untested.

Holding, in selection: the question and the row (4,200 activities of assay CHEMBL3301363 in document CHEMBL3301361,
4,195 distinct compounds, frame 4,195 x 3); the target range (min -1.50, max 4.50, median 2.3600, 556 distinct
values); the deposit's metadata verbatim (Wenlock and Tomkinson, `doc_type DATASET`, CHEMBL_20 of 2015-01-14, doi
10.6019/CHEMBL3301361, `"year": null`), the assay description character for character including its double space and
the source's spelling "coefficent"; `value == standard_value` on all 4,200, and the only feature being the structure,
which no measurement enters; the range selecting compounds rather than censoring values (1 at -1.5, 36 in
[-1.5,-1.0), 135 in (4.0,4.5], 4 at 4.5, 0 outside; `relation`, `standard_relation`, `upper_value` and
`standard_upper_value` null on all 4,200); the five twice-measured compounds and their spreads; 4,195 distinct
InChIKeys and 0 of the stereo groups straddling any of the 9 folds; the licence quoted verbatim; release CHEMBL_37 of
2026-05-01 from `status.json`; MoleculeNet's and TDC's table rows verbatim, with no third definer found.

| Verified measurement | Value |
|---|---|
| dummy RMSE over the 9 folds | 1.127 to 1.303, mean 1.2030 |
| test folds | 1,306 to 1,518 rows, 804 to 805 groups |
| Crippen MolLogP used as the answer, pooled RMSE | 1.7526 (affine recalibration on the training side reaches 1.095, so it loses on offset and scale, not rank, r = 0.415) |
| test rows with a training neighbour at Tanimoto >= 0.9 | 2.08% (0.99% at >= 0.95); copying that neighbour's label scores 0.584 on them against the fold's LightGBM 0.692 |
| MoleculeNet join | 4,180 shared ids, 4,176 equal to the shipped mean, the 4 that differ being 4 of the 5 repeats; 20 MoleculeNet-only ids, 15 ChEMBL-only; the parents of 4 of the 6 salt/hydrate rows are among the 20 |

Refuted, ranked:

- R1 (LEAK-17, a Must in kind, one row in size). Levofloxacin hemihydrate (row 767, written `core.core.O`, logD -0.35)
  and ofloxacin (row 404, the racemate of the same chemical, logD -0.45) are the same chemical at Tanimoto 0.98 and
  0.10 log apart. The hemihydrate's scaffold string is the parent scaffold twice, so they sit in different groups and
  land on opposite sides in 6 of the 9 folds. Two written statements are wrong because of it: "the Bemis-Murcko
  scaffold is the parent's either way", and the splits comment's claim that the salt, hydrate and stereoisomer forms
  of one parent share a scaffold with it. The `FragmentRemover` check did not catch it because `FragmentRemover`
  keeps both identical parent copies. Mildest remedy: group on the de-duplicated fragment set.
- R2 (EV-1/EV-2). The 26.1% / 50.5% analog figures are not the shipped split's: on the shipped folds it is 22.88%
  (fold SD 1.79) against 46.01% (SD 1.34). The quoted pair reproduces only at an 80/20 holdout (25.3% / 49.8%). The
  argument survives; the numbers do not.
- R3 (EV-6). "Almost every group is a real series" is overstated: 1,866 of 2,414 groups (77.3%) hold one compound,
  2,128 (88.2%) at most two, only 139 (5.8%) hold five or more; 44.5% of compounds are alone.
- R4 (PROV-1). "Each other field is one value across all 4,200" is false for `activity_id`, `record_id`,
  `molecule_pref_name` and `parent_molecule_chembl_id` (which differs on exactly the 6 salt/hydrate rows, the
  cheapest route to R1). The five fields named explicitly in the sentence are constant as claimed.
- R5. The identifier drop cites CLEAN-21 ("one unit and one scale per column"); the governing rules are
  CLEAN-3/CLEAN-22.
- R6. The record's screening numbers: "2,447 scaffold groups" does not reproduce (2,412 on those 4,200 compounds,
  2,414 on the shipped 4,195); "15 chemistry / 85 regression accepted" is 12 / 74. Neither changes a field.

Untested: the use case itself (a domain judgment); "no better public logD7.4 set" (a negative search claim); the
sibling fingerprint record (no folder to compare).

Reported to the mediator, not as a claim of the definition: a 2026 NeurIPS paper on the TDC version reports that the
labels can be recovered by looking the compounds up in the source ChEMBL assay (MAE 0.0069), which is inherent to
shipping a public assay.

</details>

<details><summary>Column auditor</summary>

The 3 shipped columns, the 47 raw fields and the files of the release.

Files: all 5 API pages read (`page_meta.total_count` 4,200, `next` null at offset 4,000, 4,200 distinct `activity_id`,
no page overlap). The deposit's other 14 assays (5 pKa, solubility, 5 plasma-protein-binding, 3 intrinsic-clearance)
are correctly not read: exactly one assay is logD7.4 and the rest are sibling endpoints that do not exist before
synthesis. MoleculeNet's CSV is a cross-check only.

Shipped: `SMILES` (string, declared as a structure, 4,195 distinct, all parse), correct in form but one row's value is
not the compound's structure; `logd74` (float64, 0 missing, 556 distinct, -1.50 to 4.50), fine; `scaffold` (2,414
groups, largest benzene 76 = 1.8%, 5 ring-less compounds as `single: <SMILES>`), right construction with one row's
group wrong.

Dropped, judged: `molecule_chembl_id` (the 5 repeated ids are exactly the 5 repeated SMILES, so the dedup key is
sound); `standard_type` (constant, the right drift guard). Of the 45 fields never read, `molecule_pref_name` is a
right drop on timing but not on the stated reason (647 names on 651 rows; the "has a name" flag alone explains R^2
0.032 of the target, named mean 1.69 against unnamed 2.28, and a name is given long after the assay), and
`parent_molecule_chembl_id` differs on 6 rows and is the diagnostic for the salt and hydrate forms. All censoring
markers, units, validity and quality flags, assay and ontology terms, document fields (`document_year` null on all
4,200), target fields and bioactivity fields are null or constant. No field of the release is a feature we are
missing, and nothing in the ChEMBL molecule record would qualify either, all of it being computed from the structure.

Problems, ranked:

1. One 2D-identical pair straddles the split: the same finding as the claim auditor's R1, reached from the raw
   fields. It also refutes the stereo decision table's counts (78 groups / 170 compounds on the shipped SMILES, 79 /
   172 on solvent-stripped structures) and the claim that `FragmentRemover` gives "exactly the same 2,414 groups"
   (stripping gives 2,413 and these two rows merge).
2. The hemihydrate's encoded features are not the compound's. RDKit runs on the whole multi-fragment string: MolWt
   740.76 against 361.37, HeavyAtomCount 53 against 26, TPSA 181.52 against 75.01, MolLogP 2.26 against 1.54, and
   MolLogP is the strongest single feature of the task (R^2 0.134 alone, chosen on 5 of 9 splits). The four hydrates
   are a weaker version (water adds MolWt +18, TPSA +31.5, MolLogP -0.82; theophylline monohydrate ships MolLogP
   -1.86 against -1.04). The maleate is unaffected, `FragmentRemover` keeping the organic counter-ion. Precedent
   `clock_protein_toxicity`. Options offered: (a) ship as published with a note, (b) de-duplicate repeated identical
   fragments only, (c) also remove water for the four hydrates. It recommends (b).
3. The file is sorted by the target. `activity_id` is monotonically increasing; the values form two long
   non-decreasing runs (longest 2,509 of 4,200); Spearman(`activity_id`, logD) = -0.348; a 40-bin step function of
   raw row position fits the target at R^2 0.757 in sample, above the honest model's 0.666. Nothing leaks as shipped
   (`_load_raw` never reads the ids, the frame is shuffled with seed 42, measured Spearman of row position against
   the target 0.029), but the shuffle is load-bearing and the definition does not say so.
4. The stated reason for the dropped fields is wrong on six fields, as the claim auditor's R4.

Checked clean: the censoring claim (all four relation and upper-value fields null on all 4,200; smooth tails); target
precision (1,361 values with one decimal, 2,839 with two, no block structure, +-0.05 against an RMSE of 0.69);
duplicates beyond the five (0 collisions after solvent stripping; none of the 6 parents is itself a row); the dtype
probe (0 of 0 flagged); temporal checks not applicable.

</details>

<details><summary>Split auditor</summary>

The split is right, with notes. The tree was walked independently: type `Experimental Results` is right, one company's
one-off deposit (`doc_type DATASET`, CHEMBL_20, `src_id 27`, `year: null`, one `chembl_release`) being explicitly not
a catalogue, so the entry-date route never opens; `[EXP.meets]` gives a chemical series the data does not contain,
`[EXP.kind-key]` gives yes (2,414 groups, largest 1.81%, 5 ring-less compounds alone), so `L-EXP.kind`, Grouped and
`UnseenGroup`, with 3x3 splits for this size. All of that matches what is shipped.

On the builder's open question it agrees that `L-EXP.kind` and `L-EXP.random` ship identical folds here, so only the
tag differs, but it adds that the framing omits the third answer at `[EXP.meets]`, later samples one after another,
which is the only one that would change the split. It answers that no.

A date does exist and still does not earn a temporal split. For 160 compounds sampled 20 per eighth of the id range
the earliest dated ChEMBL activity outside this deposit was fetched; 146 are datable, Spearman(molecule id, first
publication year) = 0.912, median year per eighth 1994, 2004, 2005, 2008, 2010, 2011, 2012, 2013, range 1974-2022.
What settles it instead:

| Held-out block of 524, same train size (3,671) | R^2 | Close training analogs |
|---|---|---|
| newest eighth (forward) | 0.526 | 5.5% |
| oldest eighth (backward) | 0.672 | 10.9% |
| middle 1/8 | 0.705 | 35.9% |
| middle 2/8 | 0.698 | 40.8% |
| middle 3/8 | 0.602 | 15.6% |
| middle 4/8 | 0.542 | 9.2% |
| middle 5/8 | 0.590 | 7.6% |
| middle 6/8 | 0.613 | 10.9% |

A middle block trained on both older and newer compounds is as hard as the newest one when equally isolated, and R^2
tracks the analog share across all eight (Pearson 0.81, Spearman 0.87), so the extra difficulty of a forward split is
a chemical-neighbourhood effect and not aging. The target does not move along the order (Spearman(id, logD) = +0.028,
p 0.07; eighth means 1.79, 2.37, 2.27, 2.40, 2.35, 1.87, 2.20, 2.24), and logD7.4 is a physical constant under one
fixed protocol, so the feature-target relation cannot drift; only which chemistry is measured can. The deposit is one
batch (`record_id` 2127435-2133334 and `activity_id` 14759005-14770250 contiguous, one document, one `src_id`,
`document_year` null throughout). The recovered clock is disclosure and not measurement, with an unknown signed lag,
and it is contaminated at the top: the five highest ids are salt and hydrate forms ChEMBL registered years after the
deposit, old chemistry in the newest window; 9% of sampled compounds have no other dated activity.

For completeness: windows on the rebuilt order are buildable (3 windows of 524, training shares 87% / 75% / 63%, all
over the floor, at least 33 scored units each). The reason not to build them is the meaning of the key, not the
arithmetic.

Problems, ranked: the time basis claims there is no clock and there is one, so the reason should be rewritten with
the three measurements and the closing clause kept, with no re-split; `Samples: No Time Dimension` is the wrong
collection fact, the test being whether two rows' prediction points could lie at different times, with
`Samples: Over Time` and `Time: Inferred` proposed as the curator's call; and the headline analog numbers are not the
shipped folds' (22.9 +- 1.8 against 45.9 +- 1.3, measured independently of the claim auditor).

Checked clean: `scaffold` is a true chemical series computed from the structure and not a cluster or a hash; 0.0% of
test scaffolds appear in training on all 9 folds; 4,195 distinct SMILES and InChIKeys; the 78 stereo sets never fall
in different groups because the scaffold is computed without chirality, so the claim holds structurally and not by
luck; the 6 salt and hydrate forms have no parent separately in the set; one prediction is one compound; the leak
probe finds 0.0% copies and a 1-NN R^2 of 0.081; the hidden-group probe raises no flag; the folds are balanced
(train 2,677-2,889).

Recommendation: keep `L-EXP.kind` and the `UnseenGroup` tag; rewrite the time-basis reason; no temporal split, with
the facts recorded rather than the question left open.

</details>

<details><summary>Domain practitioner</summary>

Fit direct, would use the model, keep `rmse`. At the moment of asking, a structure is all that exists; logD7.4 is the
quantity itself and not a proxy, going into the lipophilic ligand efficiency, the 1 to 3 design window and the too
lipophilic flag; one compound is one decision.

| What the practitioner would use today | RMSE | MAE | Within 0.5 log | 3-band accuracy |
|---|---|---|---|---|
| dummy (train mean) | 1.203 | 0.975 | 29.6% | 0.544 |
| desktop cLogP, recalibrated on the training side | 1.095 | 0.884 | 32.5% | 0.554 |
| read-across, 5-NN Tanimoto on ECFP4 | 1.017 | 0.781 | 41.7% | 0.598 |
| LightGBM on the recommended encoding | 0.692 | 0.528 | 57.6% | 0.720 |

(9 shipped folds, predictions clipped to the assay range.) The incumbent tool is
barely better than the mean because Crippen cLogP is logP and the ionisation term dominates: cLogP minus logD7.4
averages 3.14 over the 465 carboxylic acids, 1.32 over basic amines and 0.52 over neutrals. That the probe's single
feature is `MolLogP` five times and `fr_COO` four times is real chemistry.

The task is not noise-limited. 43 true enantiomer pairs (a single stereocentre inverted, each verified to have exactly
one centre) must have identical logD7.4 in an achiral octanol/pH 7.4 system, so their differences are pure assay
error: median 0.06, mean 0.122, 95th percentile 0.28, a single-measurement SD of about 0.11, matching AstraZeneca's
published 0.07 to 0.10 for this assay. Against a best model at 0.692 that is 3 to 6 times headroom.

Gaps, ranked:

1. The model is shrunk toward the middle exactly where the call is made: on test rows with true logD above 3.5 (1,524
   of 12,585 predictions) LightGBM under-calls by 0.71, below 0 it over-calls by 0.98, and nothing above 4.5 exists in
   the deposit to teach it. Not a fit problem, the assay having the same ceiling, but a reader who sees only
   "RMSE 0.69" will over-trust the flagging use.
2. The population is 2015 AstraZeneca patent-disclosed compounds (MW median 388, 3 aromatic rings, TPSA 80, 82%
   Ro5-compliant, 11% acids, 39% basic amines): lead-optimisation chemistry from programmes advanced far enough to
   disclose, with the early ugly ideas and today's modalities under-represented. The disclosure selection is the part
   not named.
3. Only the harder half is scored: test rows with a close training analog (22.9%) score RMSE 0.544 and 68.9% within
   0.5, while rows with nothing above 0.5 similarity (42.3%) score 0.823 and 47.5% within 0.5. The scaffold split is
   still right; 1,866 of 2,414 groups are singletons, so even a random split gives no deep series.
4. The stereoisomer decision reads its evidence backwards. The 1.55-log spread cited as a floor comes from an
   enantiomer pair, CHEMBL1770464 (2.03) and CHEMBL1770465 (3.58), whose true values must be equal, so one
   measurement is wrong by 15 to 22 times the assay's uncertainty. A second pair, CHEMBL2325742 (3.30) and
   CHEMBL2325743 (2.67), differs by 0.63. Of the 78 groups, 43 are enantiomer pairs whose differences are label error
   (median 0.06) and the other 35 are genuine diastereomers or partly defined centres whose largest spread is 0.49, so
   the real stereochemistry floor is 0.5 or less. Keep all four rows and reword the decision.
5. Nothing scores how sure the model is (3.7% of predictions are off by more than 1.5 log). An honest limitation, not
   a change requested.

What an expert would change: keep the task as defined and close the record's open question in favour of the scaffold
split; reword the stereoisomer decision; add the noise floor, the end-of-range shrinkage and the analog-stratified
RMSE; name the disclosure selection in the fit statement.

Metric: keep `rmse`. On the merits the cost of error is convex (below about 0.3 log the model cannot be told from the
assay, past about 1 log the compound crosses a design band); the usual case for MAE (heavy-tailed noisy labels) does
not apply, label noise being about 0.1 log, the target a bounded 6-log window, and the worst 1% of rows holding 13.9%
of the squared error; and empirically the ranking of eight candidates is identical under RMSE, MAE, median absolute
error, within 0.5, within 1.0, Spearman and 3-band accuracy (per-fold Kendall tau 1.00 on 7 of 9 folds, 0.929 on the
other two), while an L1-trained LightGBM does not even win on MAE (0.552 against 0.528). It asks only that the notes
record this so the next reader need not re-open MoleculeNet against TDC.

Integrity note, not its call: a NeurIPS 2026 paper reports a lookup predictor reaching MAE 0.0069 on TDC's scaffold
test fold for this assay, because the labels are public in ChEMBL, while published models sit at 0.42 to 0.54.

</details>

<details><summary>Blind reviewer</summary>

Include. It saw only the data file, a task description and the public web, and built its own 3x3 scaffold folds.

What it thinks the task is: predict logD7.4 from structure, the measurements being one AstraZeneca shake-flask assay
(CHEMBL3301363, description quoted verbatim, "Experimental range -1.5 to 4.5"), the MoleculeNet and TDC
"Lipophilicity" task. A real and standard use: rank unsynthesised compounds before committing synthesis. Nothing about
a SMILES can be unknown at prediction time, so no temporal leakage, and scaffold-grouped evaluation is the right
regime.

Provenance verified against the primary source: it pulled all 4,200 activities from the ChEMBL API, found 4,200 rows
over 4,195 molecules with every canonical SMILES present in the shipped data, a perfect 4,195-row match, and the 5
replicate pairs averaged correctly (CHEMBL1626 3.04 and 3.48 to 3.26; CHEMBL517712 -0.66 and -0.09 to -0.375), which
it calls better handling than the deepchem CSV the task description cites.

Concerns, ranked:

1. The exact labels are in a public pretraining corpus: `jablonkagroup/chempile-lift` contains these structure-value
   pairs as answered multiple-choice text, and it canonicalised three rows and matched them exactly (3.54, 3.69,
   3.14). Irrelevant for gradient-boosted trees, not irrelevant for a pretrained chemical or tabular foundation model
   or an LLM baseline, whose score then cannot be read as generalisation. Should be stated in the dataset notes.
2. One input column, and a naive tabular model gets nothing from it.

   | Encoding, 9 scaffold-grouped folds of its own construction | RMSE |
   |---|---|
   | mean baseline | 1.203 |
   | SMILES as a categorical column, LightGBM | 1.203 |
   | character counts and length | 1.002 |
   | character 2-5-gram TF-IDF and Ridge | 0.889 |
   | Morgan r=2, 2048 bits, LightGBM | 0.853 |
   | RDKit descriptors (217) | 0.719 |
   | Morgan and descriptors | 0.698 |

   The spread is almost entirely a featurisation contest, so the structured declaration with a reference encoding is
   load-bearing, and `scaffold` must not reach the model as a feature.
3. Six multi-component SMILES corrupt descriptor features, found independently: row 767 (levofloxacin hemihydrate) MW
   740.8 against 361.4 and cLogP 2.26 against 1.54; row 1015 (taxane trihydrate) cLogP 0.79 against 3.26; row 1980
   (maleate) MW 434.4 against 318.3, whose Murcko scaffold it claims collapses to plain benzene and dumps it into the
   76-row group; rows 1309, 1317 and 2745 hydrates. 6 rows is 0.14% and "the fix is one line, keep the largest
   organic component". (The advocate and the critic both refuted the maleate part independently: fluvoxamine's parent
   carries one ring, so its scaffold is benzene either way and the row's group is correct as shipped.)
4. The target is range-selected (1 row at -1.5, 4 at 4.5, 7 at or below -1.4, 19 at or above 4.4, no relation flags):
   the deposit looks filtered to in-range compounds rather than clipped. Benign for scoring, since clipping
   predictions gains exactly 0.0000, but the benchmark never tests the lipophilic tail that matters in discovery.
5. "Grouped" is real but mild and should not be oversold: grouped 0.698 against IID 0.637 with Morgan and
   descriptors, 0.853 against 0.781 with Morgan alone; 2,414 scaffolds, median group size 1, 44.5% singletons,
   largest 1.8%; test-to-train nearest-neighbour Tanimoto median 0.56 and p90 0.77; only 1.2% of test rows have a
   neighbour above 0.95 and even those differ by a mean 0.34 logD; 1-NN scores RMSE 1.229, worse than the mean.
   Nothing is solvable by lookup.
6. About 4% near-replicate rows set the noise floor: 78 sets (170 rows) share a 2D skeleton and none spans more than
   one scaffold group; 107 pairs give an RMS difference of 0.227, a per-measurement SD of about 0.16, median absolute
   difference 0.10, with 3 pairs above 0.5 and one at 1.55, "that one looks like an annotation error". Separately, 89
   groups (192 rows) are identical under binary Morgan-2048 with differing targets and 9 span scaffolds, all checked
   and genuinely different molecules (ring size 5 against 6, positional isomers): a featuriser limitation, arguably a
   point in the benchmark's favour.
7. Source-link hygiene: the task description cites the deepchem CSV as "original", but the shipped table is not that
   table (the deepchem copy strips salts and hydrates and restandardises tautomers, 21 full-InChIKey differences, 5
   connectivity skeletons present in one and not the other, and it does not average the repeats). Cite ChEMBL as the
   source and the mirrors as mirrors.
8. Licence flagged as not checked (ChEMBL is CC BY-SA; share-alike worth a look).

Could not check: the actual shipped splits (its clean room carried only the three data columns), the objective metric
(not named in what it was given), and how the harness types the columns, on which concern 2 hinges.

</details>

<details><summary>Task gamer</summary>

Could not game it. With the participant kit only, its honest baseline is RDKit descriptors (217) and Morgan counts
(r=2, 2048) with LightGBM 600 x 0.05, scored on all 9 shipped splits: mean RMSE 0.68948 (0.6449 to 0.7268). Its
measured noise floor (the baseline plus one random column, 3 seeds) is a mean gain of -0.0028, -0.0029, +0.0000 with a
per-split spread of +-0.008, so anything inside +-0.003 mean and +-0.008 per split is noise.

| # | Exploit | Honest | Exploited | Gain | Does a deployed model have it? |
|---|---|---|---|---|---|
| 1 | Pseudo-labelling on the whole test batch (fit, predict test, refit on train and test at weight 0.5) | 0.68948 | 0.68238 | +0.0071 (+0.0054 to +0.0091, every split) | Partly: it needs all about 1,400 test structures at fit time, which a virtual-screening run has and a single designed compound does not |
| 2 | Full-table z-scoring over train and test | 0.68948 | 0.68831 | +0.0012 (-0.008 to +0.007), inside noise | n/a |

Nothing else was positive and no exploit reaches 1.5% of the metric. Its fix for the first: none needed at this size,
self-distillation carrying no label information, the transductive gain any batch-scored benchmark allows.

The lookup, reported separately as its brief asked: fetching MoleculeNet's `Lipophilicity.csv` and matching on
RDKit-canonical SMILES recovers the exact label for 4,161 of 4,195 rows, of which only 4 differ, each the mean of a
merged duplicate pair. Zueco et al. (NeurIPS 2026) report the same through ChEMBL (4,183 of 4,200 rows from this
assay; an accession-lookup predictor reaching MAE 0.0069 on TDC's scaffold fold). A property of any public dataset and
not of this task; the same paper's nearest-neighbour baseline (MAE 0.787) confirms the split itself is not easy.

Flaws that hurt an honest model: none found. Clipping predictions to the label range has exactly zero effect on all 9
splits, the model never predicting outside the range.

The split is clean, and that is its main result: 0 shared scaffolds and 0 shared canonical SMILES between train and
test on all 9 splits; the shipped `scaffold` column equals RDKit's Murcko scaffold without stereochemistry for 4,190
of 4,195 rows; nearest-neighbour Tanimoto from test to train averages 0.544, only 3.5% of test rows have a neighbour
above 0.85, and a 1-NN prediction (RMSE 1.239) is worse than predicting the training mean (1.203). Adding
kNN-label features made it worse (-0.025).

Attacks that found nothing, 14 in all: row order and index (-0.0022; label autocorrelation between adjacent rows
0.016; index-target correlation 0.027; the kit's order is a shuffle of the source file); file-neighbour train labels
(-0.0044); copies across the split (0 exact, 0 canonical duplicates); SMILES string format (all already
RDKit-canonical, so no writing-style artefact; 6 salts, 99 permanently charged, 0 parse failures); target format
(1-decimal rows mean 2.41 against 2-decimal 2.08, r = -0.117, a label recording artefact, but precision is not an
input); group-column misuse (-0.0011); transductive ranks (-0.0019); adversarial validation (train-against-test AUC
0.767, the expected scaffold shift, but importance weighting cost -0.0077); transductive shrinkage to test-fold group
means (-0.008 / -0.027 / -0.093); prediction-variance calibration including the cheating version using the test
fold's own SD (-0.036 / -0.032); clipping (0.00000); metric quirks (plain RMSE, identity transform, no weight, no
scoring columns, nothing to bend); split bookkeeping (every row is a test row exactly 3 times, each repeat partitions
all 4,195 rows, test folds overlap across repeats at Jaccard 0.16 to 0.24, the splits file sorted ascending so it
encodes nothing).

Columns from after the prediction point: none. The one input is the designed structure; stereochemistry is a design
choice and not an assay result, and the charged species are permanent charges, not the pH-7.4 ionisation state the
assay would reveal.

Could not check: its last batch (error by similarity bucket, generic-scaffold crossers, a 1-NN blend, three honest
training filters) had not printed at hand-back, and nothing in it can change the ranking. It did not try a pretrained
chemical model or a graph network (a stronger honest baseline could only shrink the one positive gain), nor whether a
larger external logD corpus helps beyond the source-assay lookup (the audit paper's number for non-source assays, MAE
0.764 at 27% coverage, suggests not).

</details>

<details><summary>Precedent checker</summary>

Three of five decisions consistent, two depart. It read the curation principles, the molecule, split, split-tree, leak,
metric, provenance and verification rules, the decision register (5,865 decisions, 35 flags, none on the rules at
issue), the 10 molecule definitions and the sibling records, and made four measurements of its own on the raw pages.

1. Structure-only molecular regression, scaffold-grouped, `L-EXP.kind` and `UnseenGroup`: consistent, with five
   precedents (the SPLIT-31 amendment on `qsar_bioconcentration` issue 10(d), `qsar_oral_toxicity` with 24.7% falling
   to 16.3% close analogs, `drug_induced_autoimmunity_prediction` "as the TDC ADMET benchmarks do", `qsar_tid_11`
   with 79.7% to 59.2%, and `nci_aids_antiviral_screen`, `qsar_biodeg`, `qsar_fish_toxicity`,
   `qsar_aquatic_toxicity` with the same grouping wording), plus the CLEAN-24 amendment making the structure the
   feature. `fit="direct"` follows `qsar_bioconcentration`, `nci_aids` and `qsar_tid_11`; `approximate` was used only
   where a separate untested reference set was measurable (`qsar_oral_toxicity`), which does not exist here. This is
   the first molecule dataset in the experimental-results branch, every other walking the catalogue type, but both
   branches end at Grouped and `UnseenGroup` on the scaffold, so the re-typing changes the leaf id and nothing else.
   Open point, evidence and not outcome: the time basis says the deposit carries no date, true of its document but
   not of the route the closest precedents took, `qsar_tid_11` having gone to ChEMBL for per-compound
   first-publication years and changed its split on them (2026-11-11) and `drug_induced` having pulled
   `first_approval` for 496 of 587 drugs. Its own sample: 10 of 10 random compounds carry a first-disclosure year
   from their other ChEMBL documents, 1979-2012. The fact that settles it is that every value arrived in one 2015
   deposit, one document, one assay, which the catalogue rules exclude and which this record is not. It recommends
   one clause in the time-basis reason rather than re-opening the split.
2. `rmse` as the fallback where MoleculeNet says RMSE and TDC says MAE: consistent.
   `nci_aids_antiviral_screen` (2026-11-02) is the complement, its later definers agreeing, so the metric comes from
   them; five qsar siblings take the regression fallback where the paper's measure is a house measure;
   `Metric.context` is used in 25 definitions and in every one the source defines none and the task makes one obvious
   that the fallback would get wrong. Nothing here points at MAE or a per-group score. One note: the reason reads
   MET-5 as covering two definers who disagree with each other, the same principle one step out, and no cases row
   states it yet.
3a. Five compounds averaged into one row: departs from SPLIT-26, with the distinguishing fact in the data but not
   written as an exception. The precedent `superconductivity` (2026-11-08, issue 1 B) kept every entry and counted a
   composition once through a scoring column, as `boreal_postfire_lichen_biomass` did. LEAK-20, which the curation
   comments cite, is about feature vectors occurring with both labels and its remedy is to drop every copy, so the
   citation does not carry the call. The facts that set this case apart, the first two measured by it on the raw
   pages: 0.12% of rows against 40%; true protocol replicates (all five pairs in one document, one assay, distinct
   `record_id`, `potential_duplicate` 0) where `superconductivity`'s are separate literature reports; no split
   consequence either way; and SPLIT-23, a Must above SPLIT-26, permits it. It drafted a three-row options table
   recommending the averaging kept and the exception written. This would be the first exception to SPLIT-26's
   averaging clause, so no amendment is due.
3b. 170 compounds in 78 stereoisomer groups kept: consistent. `qsar_tid_11` is the precedent and is cited correctly
   (474 rows in 217 groups kept, written into LEAK-19's case row), with `hiva_agnostic`'s 23 repeated vectors as the
   sibling case. One line worth adding: the LEAK-19 drop that did fire on `qsar_tid_11` (37 salt forms of a ChEMBL
   parent also in the data, found through the molecule hierarchy and not through InChIKeys) has nothing to drop here,
   its own measurement being that 6 of the 4,200 activities carry a different parent id and none of those parents is
   in the set.
4. The ChEMBL API at the current release with asserts instead of a pinned file: the source choice is squarely the
   precedent (`qsar_tid_11` from the ChEMBL 17 release, `nci_aids` from the DTP release, the qsar trio from the
   authors' releases over the UCI copies), and the unread cross-check CSV is clean. What departs is the pinning:
   `qsar_tid_11` pins its FTP dump with bytes and sha256, `chicago_traffic_crashes` pins a live portal export by
   date, row count and sha256, `rain_in_australia` pins by download date, and 53 of 186 definitions record a sha256.
   Here the five JSON pages carry no checksum and the asserts cover counts and the standard type only, so a revised
   structure or value passes unseen, and the definition's own MoleculeNet comparison shows that kind of drift
   happened between CHEMBL_20 and CHEMBL_37. It recommends the checksums as the mildest remedy.
5. Retiring the sibling `tdc_lipophilicity_astrazeneca`: consistent in shape, but "retire" is the wrong word and the
   decision is already applied. The precedent is exact (`hiva_agnostic` against `nci_aids_antiviral_screen`,
   2026-11-02, where the structure release stayed and the fingerprint cut went as a duplicate), and the facts here
   are the same shape (202 of 4,200 rows share a bit vector with a different molecule, 183 carrying a different
   logD). But `No (Retired)` is for a shipped dataset, and this record was never added and already carries `No` with
   `Duplicate` naming this dataset as the survivor. The panel should not carry it to the curator as an open item.

Drift and amendment checks: no drift; this would be the first exception to SPLIT-26's averaging clause; the register's
amendment-due flags touch none of these decisions; no opposite-outcome or drift flag on any rule at issue.
`bradley_open_melting_point` has a record but no folder, so it sets no precedent here.

</details>

<details><summary>Advocate</summary>

Opening brief: ship after four cheap edits (one line of code, three of prose). Nothing the panel found is a Must that
cannot be fixed in the definition.

Its case: honest evaluation holds, verified from three mutually blind directions (the task gamer with only the
participant kit, the split auditor walking the tree, the blind reviewer building its own folds), with the repo probes
agreeing (0.0% test rows with an exact feature copy in train, 1-NN R^2 0.081, no hidden-group flag, `dataset check` 0
errors and 0 warnings over 28 checks). The hemihydrate is conceded in kind and closed by the mildest rung on the
ladder. The use case is real at `fit="direct"` and the model beats the tool the chemist uses today, with the task not
noise-limited (3 to 6 times headroom over a measured floor of about 0.11). The signal is real and provably not
trivial (LightGBM beats the dummy on 9 of 9 splits by +0.511 RMSE, 42.5% of the dummy's loss, R^2 0.666; the best
single feature alone reaches R^2 0.134, a depth-2 or depth-3 tree 0.315 and 0.376, and Crippen MolLogP used as the
answer scores 1.753, worse than the dummy). The metric is right and measurably not worth re-opening. Averaging the
five repeats is permitted by a Must that outranks the Should it departs from, and what is owed is documentation, not
a data change. The time basis reaches the right answer for a wrong reason, so the reason is rewritten and the split
stays.

What it conceded outright: the hemihydrate; the analog numbers (22.9 +- 1.8 against 46.0 +- 1.3); the overstated
series claim; the dropped-field sentence and the rule citation; the unpinned download; the stereoisomer decision
reading its evidence backwards; the publicly recoverable labels, as a note for pretrained-model baselines; and the
end-of-range shrinkage and analog-stratified error, to be stated.

Its rebuttal moved it up the ladder against its own brief, on two facts it measured in the round. First, the
de-duplication both briefs proposed does not fix the features:

| Row 767's string | MW | MolLogP | TPSA | Murcko scaffold |
|---|---|---|---|---|
| shipped `core.core.O` | 740.76 | 2.26 | 181.52 | the parent scaffold twice |
| de-duplicated `core.O` | 379.39 | 0.72 | 106.51 | the parent scaffold once |
| the compound `core` | 361.37 | 1.54 | 75.01 | the parent scaffold once |

so the error changes sign rather than going away, and the group fix and the feature fix are not the same line.
Second, the drift is concentrated on exactly the rows that cause the problem: molecule ids in the shipped frame have a
median of 1,221,551 and a 99th percentile of 2,335,907, and exactly five of 4,195 exceed 3.4M, the ceiling at
CHEMBL_20, four of those five being multi-fragment rows. It therefore argued for repair from the origin through the
parent id, which it believed was one extra field and no new download, noting that pinning CHEMBL_37 would freeze the
drift rather than undo it, and that the sha256 of the five pages is still owed for a different question.

On the fit it conceded the Must half (the reason must name the selection either way) and disputed that
`superconductivity` is the matching shape, arguing the range selection separately: the prediction stands in for the
assay, whose own reporting range is -1.5 to 4.5, so the real setting meets the same bound. It put the disclosure
selection to the curator as the one weighing call and did not claim it settled.

</details>

<details><summary>Critic</summary>

Opening brief: ship after changes, not as defined. It does not argue against the task, which it calls real with a
settled metric and the right split shape; it argues that the definition as written makes five statements the data
refutes, one of which hides a Must-level split defect, and omits what a reader needs about what the benchmark can
claim. Its seven points:

1. The fit statement names neither selection the deposit made (patent disclosure, and the -1.5 to 4.5 range), and the
   record carries no selection marker. Its own half-log bands at the top: (3.0,3.5] 654, (3.5,4.0] 373, (4.0,4.5] 135,
   above 4.5 zero, which by continuing the decay puts about 77 compounds (1.8%) above 4.5 and about 26 (0.6%) below
   -1.5. It asked for the marker and put direct against approximate to the curator, citing `superconductivity`.
2. One chemical sits on both sides of 6 of 9 folds and the definition says it cannot. Measured from the shipped
   splits: rows 404 and 767 fall on opposite sides in repeats 0.0, 0.1, 1.1, 1.2, 2.0 and 2.2. It reproduced the
   `FragmentRemover` check and found that it gives 2,414 groups because it leaves row 767 with both identical parent
   copies, so the check passed for the wrong reason, while de-duplicating identical fragments gives 2,413 and changes
   exactly one row's group.
3. The time basis rests on a fact that is not true, with the distinguishing fact against `qsar_tid_11` missing.
4. The download is unpinned and has already drifted on the rows at issue: CHEMBL5315124, CHEMBL5416410 and
   CHEMBL5483011 are molecule records that did not exist at the 2015 release, and five of the six multi-fragment rows
   are absent from the 2015-era MoleculeNet copy. The definition records a sha256 for the one file it never reads.
5. Five statements the data refutes, including the two numbers the split's framing rests on, plus the raw file's sort
   by the target and the load-bearing seed-42 shuffle.
6. Six rows' encoded features are not the compound's, with its own table of MolLogP, MW and TPSA for each; row 1015's
   MolLogP is wrong by -2.47 on a compound whose logD is 3.40.
7. The stereoisomer decision reads its own evidence backwards: it verified the 1.55 pair is enantiomers (one assigned
   centre each, S against R), found only 2 of 78 groups above 0.5 and a median spread of 0.10.

What it declined to raise, so the curator is not spent on it: the public-corpus contamination and the label lookup
(the rules are explicit that pretraining overlap and another collection's copy never change a decision, and the record
already lists ChemPile); the metric; the task gamer's pseudo-labelling gain; and the averaging of the five repeats,
which it conceded and asked to be written as the first exception. It also corrected the blind reviewer on the
maleate's scaffold, independently of the advocate.

Its rebuttal conceded point 1 outright and withdrew both the marker and the approximate fit, on the carve-out list it
had read past: tested compounds standing for the candidates a screen would test, and a selection that is how the label
comes to exist. It added that the disclosure selection is a covariate shift and not a label shift, since logD7.4 is a
function of structure and physics, so what survives is one sentence of prose and nothing for the curator to weigh. It
refined the remedy for the hemihydrate instead, measuring four candidate keys:

| Key | Groups | Rows whose group changes | Row 767's key | New exact-structure collisions |
|---|---|---|---|---|
| shipped (whole SMILES) | 2,414 | - | `core.core.O` | 0 |
| FragmentRemover alone (what was checked) | 2,414 | 0 | `core.core` | 0 |
| fragment-dedup alone | 2,413 | 767 | `core.O` | 0 |
| FragmentRemover then fragment-dedup | 2,413 | 767 | `core` (the parent alone) | 0 |

and argued the last row is the clean one, against de-duplicating the shipped string, which would write a monohydrate
stoichiometry ChEMBL does not record for that compound. That leaves the corrupted descriptors on the six rows open as
a separate, smaller call: keep the shipped SMILES and name the rows, or strip water only. It kept the rank of the
hemihydrate high not for the metric effect, which it agrees is nil, but because the definition asserts the opposite
twice in reader-facing text.

</details>

<details><summary>Mediator</summary>

Verdict: ship after changes. Both sides reached it and agree on almost everything; the mediator settled the two
crossed points by the rules and by its own measurements, and corrected both sides where the measurement says they were
wrong.

Judgment record: the use-case rules hold, with the fit direct and no selection marker (the carve-out covers both
selections), the fit statement corrected; LEAK-17 triggered on 1 row and fixed in the definition by the group key;
SPLIT-24 and SPLIT-31 hold and the leaf `L-EXP.kind` is confirmed independently; the SPLIT-26 departure is kept as its
first exception under SPLIT-23; the SPLIT-32 reason is refuted and rewritten with the split unchanged; PROV-4 and
PROV-8 hold and PROV-13 is triggered on 4 rows. Value: a large real signal (R^2 0.666, LightGBM beating the dummy on 9
of 9 folds), not trivial (Crippen MolLogP as the answer scores 1.753 against the dummy's 1.203), `rmse` with the
ranking measured metric-agnostic. Quality: 4 of the 6 corrupted rows to be repaired, 2 kept with a note. Weighed:
source +, use case +, shape +, gap 0.

What it measured itself, from the worktree, the five raw pages, the shipped folds, 12 ChEMBL molecule records and one
request on the 2015 release file:

| Group key | Scaffold groups | Rows whose group changes | Compounds sharing a 2D skeleton |
|---|---|---|---|
| shipped (whole SMILES) | 2,414 | - | 170 (78 groups) |
| FragmentRemover alone (what the definition checked) | 2,414 | 0 | 170 |
| fragment-dedup alone | 2,413 | 1 (row 767) | 170 |
| FragmentRemover then fragment-dedup | 2,413 | 1 (row 767) | 172 (79 groups) |

It confirmed the advocate's rebuttal (fragment-dedup alone leaves a monohydrate, MolLogP 0.72 against the compound's
1.54, so the error changes sign) and the critic's recipe with one correction (FragmentRemover alone leaves
`core.core`, MolWt 722.75, still not the compound), and it corrected the critic's "0 new exact-structure collisions":
the stripped key makes levofloxacin and the ofloxacin racemate one 2D skeleton, so the stereo counts become 79 groups
and 172 compounds, with nothing falling due, the two carrying different stereochemistry and different measured
values. The straddle was re-measured as 6 of 9 folds (0.0, 0.1, 1.1, 1.2, 2.0, 2.2), and the metric effect of
perfectly exploiting it as +0.00024 per fold, at most +0.0010, against a noise floor of +-0.003 mean and +-0.008 per
split.

On the drift it refuted the advocate's "no new download": the activity record has 44 fields, one structure (the
measured molecule) and the parent's id but not the parent's structure, so a repair costs six requests on the molecule
endpoint (it ran them; all six parents are a single fragment) or the 2015 release file (which answers 200,
139,150,368 bytes, Last-Modified 2015-02-02). Measured against the contemporary copy, MoleculeNet carries the parent
id with the identical value and a single-fragment structure for four of the six (CHEMBL115 2.90, CHEMBL1421 3.41,
CHEMBL190 -0.09, CHEMBL33 -0.35), so today's ChEMBL has re-pointed exactly 4 of 4,195 activities since the deposit;
docetaxel's trihydrate is in MoleculeNet under the same id, so it is the deposit's own record, and fluvoxamine maleate
predates the deposit and is absent from MoleculeNet, so nothing says it drifted. The deposit's own molecule ids top
out at CHEMBL2364624 while five sit far above it. The remaining 16 MoleculeNet-only and 11 ChEMBL-only ids have no
exact structure match either way, which is MoleculeNet's own desalting and tautomer standardisation, not evidence
about ChEMBL.

On the marker it checked the whole molecule family: none of the nine shipped molecule datasets carries `Selection
Bias`, six ship `fit="direct"`, and the three approximates are approximate for a different reason; the molecule
records that do carry the marker carry it for another mechanism (`clintox` two registries,
`muv_maximum_unbiased_validation` designed actives and decoys, `bbbp_martins` a compilation of many sources).

Its three settled questions: the fit grade and the marker (no marker, direct, with the critic's rebuttal right and its
own opening wrong, and the advocate's concession of the marker wrong while its separation of the two selections and
its direct are right); the remedy for the hemihydrate and the six corrupted rows, which splits in three rungs that do
not collapse into one (the group fixed in the definition, the four drifted rows repaired from the origin, the two the
deposit itself recorded kept with a note); and what the drift requires beyond a checksum (the sha256 answers
reproducibility, while faithfulness is answered by the repair plus naming CHEMBL_20 against CHEMBL_37 in the download
description and guarding the structures, not only the counts).

Agreed facts it recorded as needing no decision: the split is clean (0 shared scaffolds and 0 shared canonical SMILES
on all 9 folds, 1-NN RMSE 1.239 worse than the training mean 1.203, 14 attacks finding nothing, the one positive
exploit being transductive self-distillation at +0.0071 with no label information); the maleate's group is correct as
shipped, so the blind reviewer is wrong on grouping and right on descriptors; the analog numbers; the overstated
series claim; the recoverable disclosure clock with the conclusion surviving its own control; the deposit being one
batch and the task not noise-limited; the 1.55 "floor" being an enantiomer pair, a label error; the dropped-field
sentence wrong on six fields and the wrong rule cited; the raw file sorted by the target with the seed-42 shuffle
load-bearing; the labels publicly recoverable, changing no decision; the metric settled and measurably
ranking-invariant; the sibling `tdc_lipophilicity_astrazeneca` already decided and not an open item; and the five
averaged repeats being true protocol replicates at 0.12% of rows with no split consequence.

Consistency with precedent: the scaffold-grouped structure-only shape is consistent with five precedents, and this is
the first molecule dataset in the experimental-results branch, which changes the leaf id and nothing else; `rmse` as
the fallback is consistent and the complement of `nci_aids_antiviral_screen`; the averaging departs from SPLIT-26 with
the distinguishing facts in the data, to be written as its first exception; the stereoisomers kept are consistent with
`qsar_tid_11` and `hiva_agnostic`; the ChEMBL source over the MoleculeNet mirror is consistent, while the pinning
departs with no distinguishing fact; and no selection marker on a tested-compound selection is consistent with the
whole molecule family.

</details>
