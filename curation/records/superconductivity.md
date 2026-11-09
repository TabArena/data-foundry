---
unique_name: superconductivity
name: superconductivity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Selection Bias
original_source: UCI
year: '2018'
required_split:
- Grouped (NON-IID)
source_links:
- https://www.openml.org/search?type=data&id=44964
- https://doi.org/10.24432/C53P47
notebook_path: datasets/beyond_iid/old_iid/superconductivity/superconductivity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/superconductivity/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

recent and likely still useful predictive task but I am missing domain knowledge

 Talent uses UCI version. Initially, custom train/test split. Task: Predict critical temperature. Might require some special split based on molecules.Paper uses a random split 2/3 - but might be wrong. Data was preprocessed already. Moreover, there is an additional file with information about the molecules.

Potential issue: -

Lennart: No objection

Andrej: But need to check for leaks after obtaining results due to split & preprocessing.

CC (2026-10-06, Lennart): Grouped by composition (was IID). The split follows what the task does in reality: the source predicts the critical temperature from the formula alone, and a model like that is used for compositions without a measured temperature, so a test composition must be new to it. A random split gave 35% of the test rows an identical feature row in train. The key is the composition: each element's share, from the element counts in `unique_m.csv` (shipped with the release, row-aligned with `train.csv`, same temperatures), compared at 6 decimals, which only removes floating-point noise (5 to 8 decimals give the same 15,164 compositions; 4 decimals would merge 28 different ones). It joins formulas that write one composition differently (`Dy1Ir2Rh2B4` and `Dy1Rh2Ir2B4`, `V2Zr1` and `V66.6Zr33.3`), which a key on the formula string would split; no set of identical feature rows lies in two groups. 2,422 compositions have 2 to 110 entries (6,099 repeated rows); their temperatures differ by a median standard deviation of 1.3 K and by more than 30 K for 132, likely other samples, phases or pressures, which the release does not record, so one composition can hide several materials that no model on these features can tell apart. Every entry is kept and scored per row. Not grouped by element set (R^2 on log1p(Tc) 0.913 random, 0.899 by composition, 0.845 by element set): a new composition is usually another proportion of known elements, not a new family; Meredig et al. (2018) study the new-family case. Not deduplicated: Stanev et al. (2018) average a material's entries when their standard deviation is below 5 K and drop the rest (76% of our repeated compositions would be averaged); we keep the release's rows. The cost of grouping is small but real: R^2 on Tc random / grouped, 2 x 3 folds: extra trees 0.921 / 0.919, random forest 0.919 / 0.910, LightGBM 0.916 / 0.913, kNN-5 0.890 / 0.883, ridge 0.735 / 0.732. Its size did not decide: the use case did. Task probes on the build: no flags.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — out-of-sample RMSE of the critical temperature in Hamidieh 2018 (R2 reported alongside).

CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: SuperCon lists only superconductors, and all 21,263 rows have a critical temperature above 0 K (the lowest is 0.00021 K), while the use case screens candidate compositions, most of which do not superconduct. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): a screen meets mostly materials that do not superconduct, so the selection is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `supercon_mdr_2024` (TBD -> Yes, priority 2), `systematically_verified_thermoelectric_zt` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the per-row RMSE counts a composition as often as SuperCon lists it, 1 to 110 times (YBa2Cu3O7 110); the 2,422 compositions with two or more entries hold 40% of the 21,263 rows, and all 81 inputs are equal within 99.8% of them, so a model predicts per composition. Weighting each entry by 1 over its composition's entries (each composition counts once) ranks 8 untuned models at Kendall tau 0.98 per split (lowest 0.93) and 0.93 for the ranking by the mean over the 9 shipped splits, the same best model on 9 of 9. Open for Lennart as issue 1 of the record's Review; recommended: each composition counts once (B), RMSE already takes the weight.

CC (2026-11-08, Lennart): issue 1, B: each composition counts once. The RMSE weights an entry by 1 over its composition's number of SuperCon entries (`composition_weight`, a scoring column for the metric only, no training weight; the bundle warning accepted, since the composition fixes all 81 inputs), and the metric is declared from context with Hamidieh's per-entry RMSE named as the original, overruled on the unit the scientist decides on (MET-1, MET-17), as Stanev et al. (2018) count each material once. Every entry is still kept (SPLIT-26). Supersedes "Every entry is kept and scored per row" of Lennart's CC of 2026-10-06.

CC (2026-11-08, Lennart): the declared metric (rmse, weighted by composition_weight) is checked.

## Review

**Outcome:** added. In the working copy since the migration; a scan of 2026-11-08 for units with unequal numbers of
rows (raised on boreal_postfire_lichen_biomass's issue 7) found that the RMSE counts a composition as often as
SuperCon lists it, 1 to 110 times. Resolved on 2026-11-08: each composition counts once in the RMSE (issue 1).

**Main points:** Open: none. Resolved on 2026-11-08: each composition counts once in the RMSE, weighted by 1 over its
number of SuperCon entries (issue 1).

**Issues for Lennart:**

1. **Count each composition once in the RMSE, or each SuperCon entry, as now?**

   * **Problem:**
     - A row is one SuperCon entry, and the per-row RMSE counts a composition as often as SuperCon lists it, from 1 to 110 times (YBa2Cu3O7 110, Bi2Sr2Ca1Cu2O8 83).
     - Every input is computed from the formula, so a model predicts one value per composition, and the materials scientist decides per composition which to synthesize.
     - Should each entry weigh 1 over its composition's number of entries in the score, so that each composition counts once, as each plot of boreal_postfire_lichen_biomass does since 2026-11-08?
   * **Background:**
     - 15,164 compositions: 12,742 with one entry, and 2,422 (16%) with 2 to 110 entries that hold 40% of the 21,263
       rows. Their entries are other samples, phases or pressures, which the release does not record; their critical
       temperatures differ by a median standard deviation of 1.3 K, and 1.6% of the target's variance lies within a
       composition.
     - All 81 inputs are equal within 99.8% of the compositions with several entries. With one prediction per
       composition, the per-entry squared error splits into a floor (the spread of a composition's entries around
       their mean, the same for every model) plus each composition's squared error counted by its number of entries.
     - The source, Hamidieh (2018), scores RMSE per entry on a random split; Stanev et al. (2018) average a material's
       entries when they spread less than 5 K, drop the rest, and so count each material once. The weight keeps the
       release's rows and counts each composition once.
   * **Rules:** the use case decides at which unit the score counts[^sc-unit], and the source's rows stay[^sc-rows]. A
     score weight that follows from the inputs needs no training weight[^sc-weight]; this one follows from the
     composition, which fixes the inputs. A score that departs from the source's names the original[^sc-origin].
   * **Effect on the task:** per entry, the compositions SuperCon lists often (well-studied cuprates among them) weigh
     by their number of entries; per composition, the 12,742 compositions with one entry carry 84% of the weight
     (60% of the rows), and an error on YBa2Cu3O7 counts like an error on any other composition.
   * **Experiments:** the scan of 2026-11-08, 8 untuned predictors (random forest, extra trees, two LightGBM, two
     ridge, kNN and the training mean) on the 9 shipped splits. The weighted score ranks the models like the
     per-entry one at Kendall tau 0.98 per split on average (lowest 0.93) and 0.93 for the ranking by the mean over the
     splits, with the same best model on 9 of 9 splits. Kendall tau measures how far two orders of the models agree, 1
     when they are the same.
   * **Consistency:**
     - boreal_postfire_lichen_biomass counts each plot once since 2026-11-08 (1 over the plot's quadrats, for scoring
       only), on the same grounds: every input belongs to the unit, and the actor acts per unit[^sc-boreal].
     - Your call of 2026-10-06 keeps every entry and scores per row[^sc-cc]; B keeps the entries and changes how much
       each counts.
     - The same scan raised pancreatic_cancer_mouse_detection (per mouse) and dementia_prediction (per person), where
       the inputs differ within the unit.
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per entry (implemented) | RMSE over all SuperCon entries, as the source scores it | the source's score; nothing changes | a composition counts as often as SuperCon lists it; YBa2Cu3O7 weighs 110 times a composition measured once |
     | B | Each composition counts once | RMSE weighted by 1 over the composition's entries, a scoring column for the metric only, no training weight | one vote per composition, the unit the scientist acts on; the pattern boreal follows; RMSE takes a weight already | departs from the source's per-entry score; the ranking moves little (tau 0.93 to 0.98) |

   * **Recommendation:** B: every input belongs to the composition, so a model predicts per composition and the
     scientist decides per composition; RMSE already takes a weight, so the cost is one scoring column and the
     departure from the source's score named in the metric. **Decision:** A or B?

   **Notes for the AI:** on B: (1) in `_load_raw`, after `composition`, add `composition_weight`, 1 over the number of
   rows of the composition (`1.0 / df.groupby("composition")["composition"].transform("size")`); (2) declare
   `scoring_columns = (ScoringColumn(column="composition_weight", role="weight", used_by="rmse", description="1 over
   the number of SuperCon entries of the row's composition, so that each composition counts once in the RMSE; for
   scoring only, never a feature or a training weight"),)`; (3) map it in the metric, `inputs={"weight":
   "composition_weight"}`, keep `Metric.source` with `original` naming Hamidieh's RMSE per entry and a `definition`
   that says each composition counts once (MET-11); if the precedent check reads a weighted score as no longer the
   source's, `Metric.from_context("rmse", reason=..., inputs=...)` with the same text; no `sample_weight`; (4) accept
   `task_metric_weight_without_sample_weight` with MET-15's reason: the weight follows from the composition, which
   fixes all 81 inputs in 99.8% of the compositions with several entries, as boreal's `plot_weight` follows from
   `jurisdiction`; (5) replace "Every entry is kept and scored per row" in the notes and "Each row is one prediction"
   in the grouping's definition with the weighting and the scan's taus; (6) `dataset check`, a CC line in the record
   (it supersedes the "scored per row" part of Lennart's CC of 2026-10-06), a CHANGELOG entry, and a Cases row in
   metrics.md next to boreal's (MET-1, MET-15, SPLIT-23). On A: a sentence in the notes that a composition counts by
   its number of entries (1 to 110) and that counting each once ranks 8 untuned models at tau 0.98 per split (0.93
   for the mean ranking). The scan's table and script: the run folder `one_vote_scan/` of the exposure review.

   [^sc-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group: replicates averaged, any instance positive, the latest row, the best of several candidates). **MET-1**
     (Must): the declared metric scores the real task, at the unit the actor acts on.
   [^sc-rows]: **SPLIT-26** (Should): keep the source's rows; deduplicating with averaged targets is a different
     dataset. Cases: superconductivity.
   [^sc-weight]: **MET-15** (Must), its clause on score weights: a metric weight that is a function of the features
     (liberty_mutual_fire_peril_loss_cost's `var11_weight`, boreal_postfire_lichen_biomass's `plot_weight`) needs no
     sample weight; the bundle check `task_metric_weight_without_sample_weight` is then accepted with that reason.
   [^sc-origin]: **MET-11** (Must): every metric has one origin, and the notes name the original whenever the declared
     metric is not exactly it.
   [^sc-boreal]: boreal_postfire_lichen_biomass, issue 7, Lennart, 2026-11-08: "Option B: Each plot counts once."
   [^sc-cc]: Lennart, CC of 2026-10-06: "Every entry is kept and scored per row."

   **Lennart (2026-11-08, change):** Option B: Each composition counts once.

   **Resolved (2026-11-08, Lennart):** B, each composition counts once. The RMSE is weighted by `composition_weight`,
   1 over the composition's number of SuperCon entries, a scoring column for the metric only with no training weight
   (the bundle warning accepted: the composition fixes all 81 inputs); the metric is now
   `Metric.from_context("rmse")`, its reason naming Hamidieh's per-entry RMSE as the original and Stanev et al.
   counting each material once. Every entry is kept; the notes, the grouping's definition and the record say so, and
   the CC line supersedes "scored per row" of 2026-10-06.

## Reference

Hamidieh, Kam. "A data-driven statistical model for predicting the critical temperature of a superconductor." Computational Materials Science 154 (2018): 346-354.
