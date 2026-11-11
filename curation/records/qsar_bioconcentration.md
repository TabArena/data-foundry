---
unique_name: qsar_bioconcentration
name: QSAR_BIOCONCENTRATION
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
collections:
- TabSTAR
original_source: UCI
year: '2016'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C56S46
- https://www.kaggle.com/datasets/ishandutta/qsar-bioconcentration-classes-data-set
- https://michem.unimib.it/download/data/
v2_path: datasets/_dev/tabarena-v0pt2/qsar_bioconcentration/dataset.py
source_row: 683
type_adapter_id: curation-record-v1
---

## Comments

Need to understand if class or regression target should be used and how they differ

Contains SMILES string that might need preprocessing in some expert way, or we drop as done by prior work

Data in paper sounds very different to data we have from Kaggle/UCI. We only have the version after feature selection

Super hard to parse if the dataset could be used but I think we can train a model to do so. Might still have problems and result in leaks but worth including for now

**Assessment (AI, 2026-10-07):** Added as the 3-class task of UCI 510 (458 / 64 / 254 chemicals). The class is read from logBCF and the experimental logKOW (Env. Int. SI Sec. 1); an inferred band of ±0.5 log units around the TGD line reproduces 600 of 607 classes with logKOW ≥ 1. So logBCF is dropped, and no descriptor completes the rule. The 779 are the chemicals of the 2015 table (1,056) with an experimental KOW. Benzene/cyclohexane, naphthalene/tetralin and chlorobenzene/chlorocyclohexane carry each other's SMILES and descriptors: swapped back (2015 SI table); triticonazole and two dioxins dropped. SMILES kept as a string. Alternative target: logBCF regression (random forest R² 0.72).

CC (2026-10-14, Lennart): Drop the SMILES as a feature, as in every SMILES dataset, and add RDKit's 2D descriptors next to the 9 Dragon descriptors.

**Assessment (AI, 2026-10-14):** LightGBM macro AUC 0.735 with the 9 descriptors, 0.752 with RDKit's 193 added (better on 13 of 15 splits), 0.723 with the SMILES as text instead. With RDKit's descriptors no two chemicals share their values; with the 9 alone 61 did, 14 of them with another class.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape -, no known risk. Small (776 chemicals) multiclass QSAR task with repaired rows and documented source; the use case is curated.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; add the logKOW the class is read against as an input or rewrite the use case, `approximate` unless that and a drop of the 9 selected Dragon descriptors remove both gaps, and drop the 9 by LEAK-31 (open issues 8, 9, 5 in the Review). Applied in the definition: the split text (the SMILES gives exact Murcko scaffolds; 34% of chemicals in 42 congener series, random forest 0.754 to 0.650 with them held out; a SPLIT-31 candidate), the selection note corrected (at most about 0.015 macro AUC is the selection; the home_credit citation removed), the label provenance (122 shipped chemicals have a predicted logKOW in the 2015 table, so the 2026-10-07 statement that the 779 all have an experimental KOW holds only for the 2016 re-curation), the LightGBM numbers as reproduced (0.745 / 0.757). TabSTAR's copy (OpenML 46585) swaps the names of classes 2 and 3, a problem of that copy; our labels follow the archived UCI page and the rule. The tag `Free Text (Short)` is stale (no string feature since 2026-10-14), and the open issues replace the 'no known risk' of the earlier 2026-10-20 line. Priority 2: gap +, use case -, source +, shape -, risk - (multiclass is thin; the use case is the curation's and its fit is contested; Grisoni et al. document the data; 776 chemicals; an input the actor holds is missing and a potential leak is kept).

**Assessment (AI, 2026-10-20):** the 'no known risk' of the first 2026-10-20 line no longer holds: the open issues of the Review (the logKOW input, the fit label, the 9 selected descriptors) are the known risks. Evidence task, not an issue: read Grisoni et al. 2016 (Environment International 88) for the class thresholds, which are inferred from the data (600 of 607 chemicals with a logKOW of at least 1) and match the archived UCI page.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: B02(C-N) and the 24 RDKit fragment counts that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: B02(C-N) (presence of a C-N pair at topological distance 2). Reverted: the 24 RDKit fragment counts that hold only 0 and 1.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Grisoni et al. (2016) report NER (balanced accuracy) with per-class rates at argmax, no costs. Original rejected: NER.

CC (2026-10-26, Lennart): the `Free Text (Short)` tag is removed, as the definition has it: no string feature since the SMILES was dropped on 2026-10-14.

CC (2026-10-26, Lennart): issue 8, option (a): add the logKOW with its measured/predicted flag from the authors' 2015 table (USE-6, USE-3: the assessor of the use case holds it before any fish test).

**Assessment (AI, 2026-10-26):** issue 8 applied. `logKOW` and `logKOW_type` come from the Chemosphere SI table (1-s2.0-S0045653515000879-mmc2.xlsx, sha256 53787477...), matched on the CAS numbers of the cell and the logBCF both tables list: 774 of 776 chemicals (652 measured, 122 predicted), 2 missing. dataset check: 0 errors, 0 warnings; task probes: no flags; leak probe: logKOW alone 0.657, no copies. Random forest, macro ROC AUC on 30 of our splits: 0.760 with everything, 0.756 without the logKOW, 0.759 without the authors' 9 descriptors (paired -0.002, SE 0.001). Answers on the page: issue 1 (class or logBCF, raised again), issue 5 (the 9 come from commercial Dragon 6, the pool is unpublished), issue 9 (follows issue 5), issue 10 (a scaffold-grouped split recommended, as drug_induced_autoimmunity_prediction).

CC (2026-10-26, Lennart): issue 1: "let us keep the clf task": the class only, no logBCF regression.

CC (2026-10-26, Lennart): issue 5: "replace with mordred descriptors from the additional source when rebuilding". The authors' 9 Dragon descriptors are dropped (LEAK-31); this supersedes CC 2026-10-14 (RDKit next to the 9) and makes the categorical typing of B02(C-N) (CC 2026-10-21) moot. The Mordred part waits for the consistency answer on the page.

**Assessment (AI, 2026-10-26):** the 9 descriptors are dropped in dataset.py (dataset check: 0 errors, 0 warnings; RDKit's descriptors alone give all 776 chemicals distinct vectors). Mordred measured before adding it: RDKit + logKOW scores macro ROC AUC 0.759 (random forest) and 0.765 (LightGBM) on 3 x 10 folds; adding Mordred's 1,220 2D descriptors that do not copy an RDKit column gives 0.746 and 0.745 (paired -0.013 ± 0.002, -0.020 ± 0.003). The precedent check finds Mordred a departure from CLEAN-24 and the scaffold split (issue 10) a drift from qsar_oral_toxicity, whose stated reason (structures linked by row order) no longer holds; both are asked on the page.

CC (2026-10-26, Lennart): issue 5, option (b): RDKit's descriptors and the logKOW only, no Mordred "for now"; the background on Mordred goes into data_foundry.v2.chemistry, "to revisit if we want to add them at scale".

CC (2026-10-26, Lennart): issue 10, option (d): SPLIT-31 amended, molecule datasets with exact structures group on the Bemis-Murcko scaffold (ring-less molecules and a scaffold of more than a tenth of the molecules alone), "and also do the right split for oral". Issue 9: `direct`.

**Assessment (AI, 2026-10-26):** issues 5, 9 and 10 applied: no Mordred (its background is in data_foundry.v2.chemistry); scaffold groups (`scaffold_groups`: 104 ring-less and 262 bare-benzene chemicals alone; test folds of 188-345 chemicals); fit `direct` (6.4% of the test chemicals have a training analog at Tanimoto 0.7 or more, 12.6% at random). dataset check: 0 errors, 0 warnings. The task probes flag `unstable`: random forest macro ROC AUC 0.673 (0.756 under IID), log-loss skill +0.068, beating the class shares on 77% of the splits; 7 to 30 rows of the rarest class per test fold. Checked against a stronger model (TP-1): TabPFN v3.5 log loss 0.786 against 0.888 for the class shares (skill +0.118), macro ROC AUC 0.708, better on 26 of 30 splits. A weak but real signal (TP-2). No open issue left.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `bcf_lunghini_2019` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): SMILES ship as a typed structure column, not pre-encoded and never as text (path C of the discussion doc "SMILES Handling in Data Foundry and TabArena v0.2" (https://claude.ai/artifact/6r49WpR9Uard5ogo7qK4rB)): the benchmark encodes it; the recommended encoding in Data Foundry is RDKit's 2D descriptors with the MACCS keys.

**Assessment (AI, 2026-11-01):** the definition now ships `SMILES` (RDKit's canonical form of the repaired SMILES) in `smiles_columns` and no longer RDKit's 193 descriptors; logKOW stays. In the recommended encoding every chemical has its own values. MACCS keys next to the descriptors: -0.003 (LightGBM) / +0.009 (random forest) macro ROC AUC.

CC (2026-11-02, Lennart): the declared metric checked and kept as declared (review page).

CC (2026-11-02, Lennart): on the review page, issue 1: "ok keep logkow for now, but remove logkow_type  and then
ship the dateaset unless this creates any problems", and on the consistency check that followed, "go with (a)".
Applied. `logKOW` stays, all 774 values, which confirms the first half of the CC of 2026-10-26; `logKOW_type` leaves
the frame, which revises its second half. The shipped frame is the `SMILES` and the `logKOW`, 776 rows and 2
features. The review closes and the folder's `REVIEW.md` goes.

**Assessment (AI, 2026-11-02):** the fact that takes `logKOW_type` out of CLEAN-22's "keep every relevant feature"
is what it is, not what it is worth: it records how the authors filled their 2015 table, not a property of the
chemical, which is the shape of `early_learning_predictors`' `teacher_duration` (CLEAN-22, 2026-10-30, a timer of
the data collection). That distinguishes it from the provenance flags the collection keeps, which sit in the actor's
own record: `pva_revenue_prediction_kddcup98`'s `AGEFLAG`, `DATASRCE` and `LIFESRC`, `thyroid_discordant`'s five
`*_measured` and `sf_permit_time`'s `point_source`. Written as a Cases row under CLEAN-22, kind `applied`; CLEAN-22
is a Must and takes no exception line.

The effect sizes are not the reason and are recorded for the leak question the column was raised under, measured
over the 30 scaffold-grouped splits with untuned LightGBM on the recommended SMILES encoding (macro ROC AUC):
`logKOW_type` scores 0.534 alone against 0.5 for chance, adds nothing at all on top of the structure (0.6806 with
it, 0.6806 without it) and is worth -0.0013 in the full model. `logKOW` itself is worth +0.0121 over the encoding
alone, better on 22 of 30 splits and -0.0241 in log loss on 21 of 30; as the only feature it scores 0.629 where
RDKit's `MolLogP` scores 0.594, though RDKit's 16 logP-related descriptors together reach 0.628, and a model on the
encoding reproduces the table's logKOW out of fold at R-squared 0.877 (mean absolute error 0.44 log units against a
spread of 1.86). So the column is a real measurement that the structure nearly, but not quite, recovers.

No leak in either, which was the worry behind the question: the class is a band around the TGD line through the
measured logBCF, which is dropped, and the band reproduces the shipped class for 94.7% of the rows with a measured
logKOW but for only 72.5% of the 122 predicted ones, so the value shipped for those rows is not the number the
authors read their label from. The class shares differ by provenance (lipid storage 61% of the measured rows, 48%
of the predicted ones), and that is exactly what the flag's 0.534 measures: which chemicals get a logP measured, not
which mechanism they have.

What it costs, written down because it is not recoverable: the 122 predicted rows can no longer be told apart in the
shipped frame, so `logKOW` ships as 84% measurement and 16% the authors' consensus prediction with no marker on the
row. The counts and their split by class are decision table 4 of the README and a bullet of `curation_comments`, and
CLEAN-24's "measured properties stay (qsar_bioconcentration's logKOW)" now carries the qualifier that a column
mixing a measurement with a prediction of the same property stays whole under USE-6.

Verified on the final definition: `dataset check` 0 errors and 0 warnings (27 checks), 776 rows and 2 features; the
task probes raise no flag (random forest macro ROC AUC 0.678, LightGBM 0.689, best single feature 0.589, smallest
test class 9 rows) and the leak probes none (all features 0.705, shallow tree 0.581, no test row with an exact
feature copy in training, 1-NN label agreement 0.621 against a chance of 0.462).

## Review

**Outcome:** added. The bioconcentration class of 776 organic chemicals in fish (Grisoni et al. 2016, UCI 510), from
the structure and the measured logKOW, grouped on the Bemis-Murcko scaffold (558 groups). Opened on 2026-11-11 from
the review of how catalogues of fixed properties split: the definition names no time basis for its scaffold split.

**Main points:** Date the chemicals through their source tables before naming the time basis, as the three sibling
Milano sets were asked to do, or name the scaffold split `Timeless` now (issue 1)?

**Issues for Andrej:**

1. **Time basis: date the chemicals first, or name the scaffold split `Timeless`?**

   * **Problem:**
     - The definition splits on the scaffold and names no time basis, while the record carries
       `Samples: No Time Dimension`.
     - A chemical's bioconcentration factor is a fixed property of the chemical, the case the `Timeless` prototype
       names[^1a].
     - The chemicals carry CAS numbers, and a catalogue whose items enter in eras counts as arising over time even
       where each item's own value is fixed, so the identifier is worth checking before the tag is set.
   * **Background:** the use case is an assessor judging an untested chemical before a fish test, holding its
     structure and its logKOW; the measured BCF values were compiled from the authors' 2015 table, drawn in turn from
     VEGA and the EURAS BCF collection, neither of which ships a test date in this release.
   * **Experiments:** the share of test chemicals with a close training analog (Tanimoto 0.7 or more, Morgan radius 2)
     fell from 12.6% under a random split to 6.4% under the scaffold groups when the split was adopted; no split by
     year has been measured, because no year is in the release.
   * **Consistency:** on 2026-11-11 qsar_biodeg was sent to be dated through NITE, and qsar_fish_toxicity and
     qsar_aquatic_toxicity through ECOTOX, before their time basis is named; this dataset is the fourth of that
     family and its chemicals carry the same kind of key.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | no change | nothing to write | the definition does not say why a split that is not temporal is safe in time |
     | B | Date through the source tables, then decide | look for a measurement year per CAS number in the EURAS BCF collection and the authors' 2015 table, then measure a split by year as the siblings will | decides on a measurement; the same route as the three siblings | the compilations may carry no year, and then the answer is C anyway |
     | C | Scaffold split, `Timeless` | the tag and a `Time basis:` line naming the fixed property, the undated compilation and the measured analog shares | nothing to measure; as the other molecule sets | assumes the catalogue does not drift, which the siblings are being asked to check |

   * **Recommendation:** B, for the same reason you gave the three siblings: the key is in the release, so the
     question can be settled by measurement rather than assumed. **Decision:** A, B or C?

   **Notes for the AI:** on B, join the CAS numbers to the EURAS BCF collection and the authors' 2015 supporting
   table, report the share dated and the year range, and if dated measure as qsar_tid_11 did (expanding windows by
   first year against scaffold folds on the same test chemicals, close-analog shares for both). On C,
   `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`) and a `curation_comments` bullet naming the
   property, the undated compilation and the fall from 12.6% to 6.4% close analogs; then `dataset check`, a CHANGELOG
   entry and a record CC line with `Andrej` in `checked_by`.

   [^1a]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows; `Timeless` when the target
     is a fixed property of the item. Question 1 also asks which identifier a parent source could date the items by,
     and "none published" is an answer; a catalogue whose items enter in eras arose over time even when each item's
     value is fixed.

   **Andrej (2026-11-11, change):** Option B: Date through the source tables, then decide.

## Reference

@article{grisoni2016investigating,
  title={Investigating the mechanisms of bioconcentration through QSAR classification trees},
  author={Grisoni, Francesca and Consonni, Viviana and Vighi, Marco and Villa, Sara and Todeschini, Roberto},
  journal={Environment international},
  volume={88},
  pages={198--205},
  year={2016},
  publisher={Elsevier}
}
