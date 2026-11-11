---
unique_name: protein_model_quality_rf_pcp
name: RF-PCP (quality assessment of modeled protein structures, CASP and decoy sets)
checked_by:
- Myunghwan
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 3
decision_markers:
- Outdated
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2014'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://sourceforge.net/projects/rf-pcp/files/
- https://doi.org/10.1142/S0219720015500055
v2_path: datasets/_dev/tabarena-v0pt2/protein_model_quality_rf_pcp/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-10-29, Myunghwan): Include GDT_TS as a historical tabular quality benchmark with the documented descriptor uncertainties. Use source year 2014 and retain the paper's 2015 citation. Exclude the 4,893 explicitly named native references; retain the 95,094-row candidate population (superseded 2026-11-05: 94,083 rows, the 1,011 relaxed natives of the rosetta62 set leave too, CC below), including the three documented ambiguous zero-RMSD cases. Preserve all six supplied descriptors and the canonical-protein holdout.

**Assessment (AI, 2026-10-29):** The author archive has 99,987 rows. A row is a candidate protein structure; the six numeric inputs are surface area, cumulative aliphatic C-beta distances, empirical energy, secondary-structure score, sequence length and aliphatic pair count. Identifiers and both alternative outcomes are excluded from predictors. GDT_TS is the supplied fractional average agreement at 1, 2, 4 and 8 angstrom tolerances. Predict it after candidate generation, before the experimental reference is available.

The source paper fits three separate regressions. Its Section 3 reports multiple measures without a unique criterion, so regression RMSE is the fallback (superseded 2026-11-04: the metric is `mean_group_pearsonr` on `protein_id`, Exception to MET-5 below). Our diagnostic R-squared is 1-SSE/SST, whereas the paper reports squared Pearson correlation. Section 4.1 uses tolerance plus/minus 1 angstrom for RMSD and plus/minus 0.1 for TM/GDT. The first archive release is August 2014; the article appeared online in December 2014 and in a 2015 issue.

Exclude source IDs beginning native_ or ending _native.pdb by reference identity, not target value. Retain casp5_T0156_1nxj.nNh1.pdb and ROSETTA_1aa2_1aa2h2.pdb despite perfect labels because their reference role is unverified. Retain CASP10_T0676_HOMER_TS2.pdb with RMSD0/GDT0.0116: exact alignment coverage is unavailable, so neither a numerical repair nor deletion is supported. The paper's headline native count is not a measured count of independent protein groups.

SS has an equation/prose disagreement and 5,620 values above modeled sequence length. ED/PN have 134 inconsistent zero combinations under the simple common-pair interpretation. Preserve those values and signed/extreme finite Energy (superseded 2026-11-04 for ED/PN: the 134 zero combinations are set missing, CC below; Energy stays as supplied). Feature-generation code and exact row-level alignment outputs were not recovered; no native-dependent feature leakage, sentinel mechanism or supported numerical correction was demonstrated.

Source-backed identity checks merge six biological components spanning 14 PDB keys, reducing 453 source keys to 445 canonical proteins. Official CASP links cover 339 targets; three more are sequence-verified. The required hash-checked identity map prevents silently restoring the earlier same-protein alias leak. Nine repeated group-disjoint folds have zero known identity or exact-predictor overlap. Protein-family independence, modern-generator transfer and top-one structure-selection usefulness are not claimed.

On the same five held-out-protein folds, Ridge RMSE0.19318568 versus training-side-selected LightGBM0.17894541 gives a 7.37% reduction. The all-nine-fold LightGBM RMSE is0.17804637 and R-squared0.227478; it beats the training mean in every fold. These are descriptive repeated-fold results, not proof of a significant advantage over TM-score or maximum future improvement. The bounded stronger comparison addresses the untuned no_spread question without promising a benchmark-wide ranking.

Priority 2 balances traceable source and grouped biological coverage against unresolved source conventions and approximate historical fit. The three original targets remain one source family, with only GDT_TS selected. The current measurements and curator decisions supersede the provisional counts, source year, tolerances and target recommendations in the historical screening below.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata and notes below were drafted by an AI assistant from the release files and the paper's abstract; a human must verify them before relying on them.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: predict the quality (RMSD, TM-score or GDT_TS) of a modelled protein structure without its native, from six physicochemical properties; the decoy file names give the target protein, so the split can be grouped by target.
- Source: Rana, Sharma, Bhattacharya, Shukla, "Quality assessment of modeled protein structure using physicochemical properties", J Bioinform Comput Biol 13(2):1550005, April 2015 (doi:10.1142/S0219720015500055), with the authors' release on SourceForge (project rf-pcp, RF-PCP-DataSet.zip, 5.3 MB, 2014-08-18, user psrana; no licence stated). The abstract (Crossref): "a total of 95,091 modeled structures of 4896 native targets", features "total surface area, euclidean distance (ED), total empirical energy, secondary structure penalty (SS), sequence length (SL), and pair number (PN)", targets RMSD, TM-score and GDT_TS, k-fold cross-validation over structures. As published (per the old note, not re-opened): a full file of ~100k rows and CASP5-9 / CASP10 files with PDB-ID, RMSD, TM, GDT and the six features.
- Use case: a structure-prediction group or a CASP assessor ranks the candidate models of a new target before its native structure is known; fit approximate (the paper says the method makes "the prediction faster and inexpensive" but names no actor or decision); regime grouped by target protein because a new target has none of its decoys in training (the leak that retired `physiochemical_protein`).
- Siblings and duplicates: `physiochemical_protein` (UCI 2013, the same group's earlier file, `No (Retired)` by Lennart on 2026-10-06 because no copy has target ids; the CC line names RF-PCP as a candidate to triage) and `physiochemical_protein_duplicate`; this release has other features and cannot be joined to the UCI rows, so it is a distinct dataset (PROV-7). External collections: none found.
- Papers and pages: the 2015 paper above; Pathak, Rana et al., Int J Data Mining and Bioinformatics (online 2015-11, RMSD <= 5 A with the same six properties) used the same features.
- Metric: the paper reports RMSE, correlation, R^2 and accuracy (within +-0.1) for each of the three targets, none ranked, so the fallback `rmse` on the chosen target (MET-5); inputs none.
- Risks for /add-dataset: which target to ship (GDT_TS or TM-score, the bounded scores QA methods predict, against RMSD of the UCI file); the rows mix CASP decoys with classic decoy sets and native structures (RMSD 0, not known at prediction time for a new target); Energy outliers up to 7e11; SL and PN near-constant within a target; six coarse features that structure-based deep QA models have since replaced (`Outdated` question, SEL-12 boundary).
- Priority: gap + (biology & life sciences and the grouped regime are thin), use case 0 (no actor named by the source), source +, shape +, risk - (target choice, natives, outdated features).

**What it is (AI, 2026-10-06).** The supplement of Rana, Sharma, Bhattacharya and Shukla (2015), "Quality assessment of modeled protein structure using physicochemical properties" (J Bioinform Comput Biol 13(2):1550005): predict the RMSD, TM-score and GDT_TS of a modeled protein structure, without its native structure, from six physicochemical properties (total surface area, Euclidean distance, total empirical energy, secondary structure penalty, sequence length, pair number). The abstract reports "95,091 modeled structures of 4896 native targets" and k-fold cross-validation over the structures (random forest best, R^2 0.92 for RMSD). The files are on SourceForge (project rf-pcp, registered 2014-08-18, RF-PCP-DataSet.zip, 5.3 MB): RF-PCP-Full-dataset.csv (99,987 rows), RF-PCP-Training-Testing-CASP-5-9.csv (92,597) and RF-PCP-Validation-CASP-10.csv (5,119), with the columns PDB-ID, RMSD, TM, GDT, Area, ED, Energy, SS, SL and PN.

**Why a candidate.** It can replace physiochemical_protein (retired 2026-10-06): the same group's UCI file has no target ids, so its decoys could not be split by protein. Here the PDB-ID names each decoy file, so the target is known: CASP5-10 decoys of 342 targets (34,288 rows, a median of 101 per target; e.g. `CASP10_T0719_PconsD_TS5.pdb`), classic decoy sets named by the native's PDB code (ROSETTA 17,077, lattice 14,329, fisa 8,334, rosetta62 7,189, John2002 5,923, 4state 4,160, lmds 3,863 rows) and 4,478 native structures. The use case, judging the models of a new target, needs grouped splits by target (the native protein; one native can occur in several decoy sets); the source's CASP10 file is a natural test on a new CASP round.

**Open questions for triage.**
- Licence: none stated on the SourceForge page.
- Target: GDT_TS or TM-score (the bounded scores that quality-assessment methods predict) or RMSD (the UCI version's target).
- Rows: CASP decoys only, or all decoy sets; the native structures are trivially perfect (RMSD 0), and in a new-target setting the native is not known.
- Features: six only; Energy reaches 7e11 (outliers to check); SL and PN are constant within most CASP targets (80% and 71%), so they identify the protein, which is fine under a grouped split.
- One PDB-ID occurs twice in the full file.

CC (2026-11-04, Lennart): impossible descriptor values become missing ("Yes, mark them as missing"). Applied to ED = 0 with PN > 0 (71 rows) and PN = 0 with ED > 0 (63 rows); the rows stay (CLEAN-11). Energy is open: its extreme values are the tool's output for unminimized models (Review issue 2).

**Exception to MET-5 (2026-11-04, Lennart):** the metric is `mean_group_pearsonr` on `protein_id` (origin context) instead of the RMSE fallback for a paper that reports several metrics ("yes new metric is better"). Fact: the use case ranks the candidates of one protein, and pooled RMSE rewards each protein's typical quality: the per-protein true mean, which orders no candidate, beats LightGBM on it (0.134 against 0.188), while CASP scores quality assessment per target. Serves P6: scored by the metric the real task would use (MET-1).

CC (2026-11-04, Lennart): `Energy` stays as supplied ("keep as is"); the ED/PN zeros stay missing. `Outdated` is set ("ok agree"): six global descriptors of 2002-2012 server models, while CASP15 on uses the predictor's own pLDDT; kept as a small grouped biology task with no new features. Not a SMILES case: a protein model is a 3D structure, and shipping structures would make it a structure task (SEL-12).

CC (2026-11-04, Lennart): the per-protein correlation stands as implemented (Review issue 1 closed).

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran for this dataset; its issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled. (Superseded the same day by the full second-pass panel below.)

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes, once the metric is fixed in the library (issue 6), the relaxed natives are excluded (issue 4) and `context` is settled (issue 5), and the definition is rebuilt (USE-7 triggered by 1,011 rosetta62 relaxed natives kept as candidates, the archive's `relaxed_natives/` folder; SPLIT-23 and USE-6 triggered by `context="none"`, a context model scores 0.517 against 0.355; MET-2 and MET-13 triggered by proteins with constant predictions left out of the score, 0.355 to 0.428 without labels; USE-8 wording for CASP10 and EV-6/EV-8 notes fixed in the definition); disputed: the metric fix as a gate (MET-2, MET-13; settled, a gate), what `rn` means (USE-7; settled from the archive), CASP10 as P5 or USE-8 (settled, USE-8), the `Outdated` keep against first_order_theorem_proving (open); for the curator: issues 4-9. Priority 3: gap +, use case 0, source +, shape +, risk - (gap: biology & life sciences is thin among the 107 accepted definitions; use case: the source names no actor and the fit is approximate; source: the Rana et al. 2015 paper and the authors' archive; shape: 95,094 rows, 6 features, 445 protein groups; risk: rows that exist only after the reference, issue 4, and the metric's left-out proteins, issue 6).

**Assessment (AI, 2026-11-05):** the shared `mean_group_pearsonr` changed on 2026-11-05 (Lennart, huesken_sirna_efficacy issue 6): a group whose target varies but whose predictions are all equal scores 0 instead of being left out; a group with a constant target stays out. Scores of non-constant predictions are unchanged (this is the fix of this record's Review issue 6).

CC (2026-11-05, Lennart): the rosetta62 set's 1,011 relaxed natives leave by identity, like the 4,893 named natives (Review issue 4, B; USE-7 via CLEAN-11). Their IDs (`rosetta62_<pdb>_rn<pdb>.out.N.pdb`) sit in the folder `relaxed_natives/` of the set's own archive (Zenodo 48780): the experimental structure energy-minimised, which exists only once the reference is known. They held the best candidate in 55 of the 56 rosetta62 proteins. The pattern matches only these rows and none of the three zero-RMSD cases; 94,083 rows and 445 proteins remain. On the declared metric and the nine shipped splits, untuned LightGBM scores 0.322 against ridge 0.272, higher in 9 of 9 (0.355 against 0.294 with the relaxed natives).

CC (2026-11-05, Lennart): the declared metric (`mean_group_pearsonr` on `protein_id`; since 2026-11-05 a protein whose predictions are all equal scores 0) is checked and stays as declared.

CC (2026-11-05, Lennart): `grouping.context="all_rows"` (Review issue 5, B, confirmed through issue 9, A, which reopens huesken_sirna_efficacy to follow): the researcher holds all of a target's candidates when ranking them. A context model scores 0.483 against 0.322 for a row-only one (without the relaxed natives).

CC (2026-11-05, Lennart): `Outdated` stays as a note on a kept borderline dataset, now rule SEL-18 (issue 7, D); a Tensions row in principles.md says a measured target scored within groups is no ranking task (issue 8, B).

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. Verdict: ship after changes (review panel, second pass after the PR #33 review), once the metric
is fixed in the library (issue 6), the relaxed natives are excluded (issue 4) and `context` is settled (issue 5), and
the definition is rebuilt. Validity: SEL-9, USE-3 and LEAK-10 hold (RMSD and TM dropped); SPLIT-1,
SPLIT-24 and SPLIT-26 hold (445 proteins, none shared across the 9 splits, the alias map hash-checked, no drift across
CASP rounds through CASP9); USE-7 is triggered by 1,011 relaxed native structures kept as candidates (issue 4);
SPLIT-23 and USE-6 are triggered by `context="none"` (issue 5); USE-8 was triggered by the sequence-length wording for
CASP10, fixed in the notes. Value: MET-1 holds (the per-protein correlation stands in for top-1 GDT_TS loss; the MET-5
exception is Lennart's of 2026-11-04); MET-2 and MET-13 are triggered by proteins with constant predictions being left
out of the score (issue 6); TP-3 holds on the declared metric (LightGBM 0.355 against ridge 0.294, 9 of 9 splits).
Quality: CLEAN-11 applied (ED/PN zeros missing, Energy kept); EV-6 and EV-8 fixed in the notes this pass. Weighed:
grouped biology is thin in the collection +, 445 proteins and 95,094 rows +, a traceable source +, historical
descriptors (`Outdated`) -, 64% classic decoy sets -. Not checked by the panel: the paper's definition of SS (STRIDE
against PSIPRED, as the notes cite from Sections 2.2-2.3; EV-7). No action proposed; a native-based SS would be a leak
(LEAK-10).

**Main points:** Three changes the panel could not make itself: drop the relaxed natives (issue 4), let models see a
protein's other candidates (issue 5) and fix the metric's left-out proteins in the library (issue 6); then the
`Outdated` consistency check (7), a SEL-9 Tensions row (8) and whether `huesken_sirna_efficacy` follows issue 5 (9). Open: the split count, 20 x 3 in proteins instead of 3 x 3 (issue 10).

**Issues for Lennart:**

4. **Exclude the 1,011 relaxed native structures of the rosetta62 set?**

   * **Problem:**
     - Next to its de novo decoys, the rosetta62 set has 15-20 files per protein named
       `rosetta62_<pdb>_rn<pdb>.out.N.pdb`, which in the set's own archive
       ([Zenodo 48780](https://zenodo.org/record/48780), `rosetta_decoys_62proteins.tgz`) sit in a folder named
       `relaxed_natives/`.
     - They are the experimental structure, energy-minimised, so they exist only once the reference is known.
     - `_clean` drops references by name (`native_...`, `..._native.pdb`) and misses them.
   * **Effect on the task:** in 55 of the 56 rosetta62 proteins the best candidate is a relaxed native (median GDT_TS
     0.961; 8 of the 10 rows with GDT_TS 1). They make ranking in those proteins easy: a researcher never has the
     refined experimental structure among a new target's candidates, so in these 56 proteins the benchmark rewards
     spotting a near-copy of the answer.
   * **Experiments:** LightGBM scores 0.596 inside them with these rows and 0.310 without; overall 0.355 against
     0.322, lower in 9 of 9 splits.
   * **Consistency:** excluding them treats like cases alike with the accepted native exclusion (Myunghwan,
     2026-10-29)[^task-row]; the filter is on identity, not on the label.
   * **Panel:** the column auditor found it, the advocate and the critic both concede it, and the mediator confirmed
     the folder name.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 95,094 rows; a named note | none found | rewards spotting a near-copy |
     | B | Exclude by identity | 94,083 rows, 445 proteins | like the 4,893 named natives | counts and notes change |

   * **Recommendation:** B, exclude. **Decision:** B (exclude the relaxed natives) or A (keep them with a named
     note)?

   **Notes for the AI:** on B, exclude them by identity (`_rn[0-9a-z]{4}\.out\.` in `PDB-ID`), as the 4,893 named
   natives already are. 94,083 rows, still 445 proteins; each rosetta62 protein keeps its de novo decoys (at least 99,
   median 109). `task_summary.row`, `changes` and the counts in the notes change; the build is stale either way.

   [^task-row]: **USE-7** (Must): a row that is no task row leaves; applied through **CLEAN-11**.

   **Resolved (2026-11-05, Lennart):** B. The 1,011 `rosetta62_*_rn<pdb>.out.N` relaxed natives leave by identity (the
   archive keeps them in `relaxed_natives/`): 94,083 rows, still 445 proteins; the three ambiguous zero-RMSD rows stay.
   Re-measured without them: LightGBM 0.322 against ridge 0.272 (9 of 9 splits; 0.355 against 0.294 before). A USE-7
   Cases row records it; `dataset check` clean, leak and group probes without a new flag.

5. **Let models see a protein's other candidates (`context="all_rows"`)?**

   * **Problem:**
     - `grouping.context` says what a model may use about the other rows of a test protein, and it is `"none"`: each
       candidate is scored as if it came alone.
     - In the use case the researcher holds all candidates of a target at once (CASP releases a target's server
       models together, about 20 in stage 1 and 150 in stage 2)[^known].
     - The metric compares candidates only within a protein, so where a candidate stands among its siblings is what
       the task is about[^group].
   * **Experiments:**
     - A model that z-scores and ranks each descriptor within its protein scores 0.517 against 0.355 row-only on the
       9 shipped splits (the mediator; the domain practitioner's 3 folds: +0.150 to +0.165 in each), and 0.615
       against 0.050 on the 67 CASP10 targets, whose descriptors follow another convention.
     - "none" cannot be enforced: the task gamer rebuilt proteins inside the test fold from the sequence length alone
       and reached 0.476 (0.516 with the true groups), so it rewards whoever breaks it.
   * **Background:**
     - With `all_rows` a model gets all test rows of a protein at once; no new column, so the "no new features"
       decision of 2026-11-04 stands.
     - Its cost: a method that predicts row by row is scored on a task it cannot fully use (about 0.16 below a
       context model).
     - With `all_rows`, the 67 CASP10 proteins (15% of the scored proteins) become learnable (0.615), so nobody needs
       to drop them.
     - If "none" stays, two things follow: `fit_reason` states the 0.476 gap as a rule the harness cannot enforce,
       and CASP10 stays near 0.05 for a row-only model, so keeping or dropping CASP10 becomes a decision of its own
       (the panel left it to you).
   * **Consistency:** `all_rows` follows `sat11_hand_algo_runtime` (`all_rows`, the candidate solvers of one
     instance); the implemented `none` follows `huesken_sirna_efficacy` (the same day; issue 9).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `none` (implemented) | each row scored alone | suits row-by-row methods | not enforceable; CASP10 near 0.05 |
     | B | `all_rows` | a protein's test rows at once | as the use case; CASP10 learnable | row-by-row ~0.16 lower |

   * **Recommendation:** B, `all_rows`. **Decision:** B (declare `all_rows`) or A (keep `none` with the gap written
     down)?

   [^group]: **SPLIT-23** (Must): the use case decides what is known about a new group.
   [^known]: **USE-6** (Must): what is known at the prediction point is a legitimate input.

   **Lennart (2026-11-05, change):** Option B: all_rows.

   **Consistency check (AI, 2026-11-05):** `context="all_rows"` here differs from huesken_sirna_efficacy
   (`context="none"`, 2026-11-04), with the same `mean_group_pearsonr` and candidates ranked inside a held-out group.
   What sets them apart?
   - (a) huesken's guides (about 81 per gene) are a sample of Huesken's library design, not the pool a researcher would
     design for a new gene, while CASP releases a target's whole set of server models at once: recorded on huesken under
     SPLIT-23, and B is applied here;
   - (b) treat huesken like this one: reopen it with `all_rows` (issue 9, A), and B is applied here;
   - (c) keep `none` here, like huesken;
   - (d) amend SPLIT-23: a metric that ranks within groups implies `all_rows`.

   Give the letter in the note; nothing is applied until then. Issue 9 asks the same question from huesken's side.

   **Resolved (2026-11-05, Lennart):** B, with issue 9 A as the answer (b) to the check above.
   `grouping.context="all_rows"`; a context model scores 0.483 against 0.322 for a row-only one on the new frame.
   SPLIT-23 Cases rows for sat11_hand_algo_runtime and this dataset. The example harness does not yet give a model the
   group of its test rows; that gap is in BENCHMARK_CHANGES_TODO.md.

6. **Fix the metric so that a protein with constant predictions scores 0, before shipping?**

   * **Problem:**
     - `mean_group_pearsonr` leaves out every protein whose predictions do not vary, so a participant can choose
       which proteins are scored by predicting an exact constant on the ones the model is least sure of.
     - Whether a constant drops the protein or scores about 0 depends on floating-point rounding (0.5 drops it; 0.3 or
       the training mean scores about 1e-16), and all-constant predictions return NaN.
     - The advocate and the critic agree it is a gate before shipping[^edge].
   * **Background:** the cut is `corr = corr[var > 0]` in `_mean_group_pearsonr`.
   * **Experiments:** without any label, LightGBM goes from 0.355 to 0.428 when it abstains on half the proteins and
     to 0.492 on three quarters (a gain in 9 of 9 splits), more than the 0.061 between LightGBM and ridge. Predicting
     the raw sequence length scores 0.410, and 0.084 once the left-out proteins count.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave out (implemented) | constant proteins not scored | none found | abstaining pays; NaN if all constant |
     | B | Score them 0 | constant predictions score 0 | abstaining no longer pays | changes 2 other datasets |

   * **Recommendation:** B, fix the library. **Decision:** approve B for all three datasets?

   **Notes for the AI:** the code is `_mean_group_pearsonr` in `src/data_foundry/v2/metrics.py`. On B: a protein whose
   target varies but whose predictions do not scores 0; drop a protein only when its target is constant (none here).
   Tests with the constants 0.3 and 0.5 and with all proteins constant, then restate the Metric text. `dataset.py`
   does not change. The same code scores `huesken_sirna_efficacy` and `numerai_v5_2_1m` (`method="numerai_corr"`);
   their scores change only for constant predictions.

   [^edge]: **MET-13** and **MET-2** (Must): a metric undefined at the edge of its domain gets a defined score, and
     the score rewards the decision.

   **Lennart (2026-11-05, change):** Option B: Score them 0.; Note that this is also a problem for another dataset,
   check if it is algiend already

   **Answer (AI, 2026-11-05):** it is aligned: the fix is in the one shared function, so it holds for all three datasets
   that use it (this one, huesken_sirna_efficacy and numerai_v5_2_1m); each record says so.

   **Resolved (2026-11-05, Lennart):** B, by your mark on huesken_sirna_efficacy issue 6 (the same shared function): a
   protein whose predictions are all equal scores 0, a protein with a constant target stays out.


7. **Keep `Yes` with `Outdated`, when `first_order_theorem_proving` is `No` on `Outdated` alone?**

   * **Problem:**
     - Your call of 2026-11-04 (keep, `Outdated`: six global descriptors of 2002-2012 server models, the field now on
       pLDDT) differs from `first_order_theorem_proving` (`No` on `Outdated` alone, 2026-07-27).
     - That call has an open consistency check of 2026-10-19 against its ASlib siblings, and most precedents keep
       (`heart_disease`, `covertype`, `horse_colic_survival`).
     - It is a weighing call, since selection.md gives `Outdated` no rule.
   * **Background:** the AI's guess at what sets this one apart: the grouped biology regime is thin in the collection
     and the descriptors are a documented measurement set.
   * **Panel:** the advocate answers A; the critic holds that an open check is no precedent.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Record the fact | the fact that sets it apart goes on record | the advocate's answer | none found |
     | B | Like `first_order_theorem_proving` | this one treated like it | none found | none found |
     | C | Reopen `first_order_theorem_proving` | keep it, like its siblings | none found | none found |
     | D | A rule for `Outdated` | an amendment | none found | none found |

   * **Recommendation:** none from the AI; the advocate answers A. **Decision:** A, B, C or D?

   **Lennart (2026-11-05, change):** Option D: A rule for Outdated. There might be task that are so outdated that we
   dont need them anymore (or this was just teh first tag we found that is enouhg, first order might also have other
   problems). But here, it is more a note for us that the task itself is outdated but we keep it as it is borderline

   **Resolved (2026-11-05, Lennart):** D. New rule SEL-18 (Should) in selection.md: `Outdated` alone leaves no dataset
   out; on a borderline dataset whose task is still real it is a note; a dataset leaves only when the task itself is
   gone, and a `No` that cites `Outdated` names its other reasons too. Cases rows: this dataset (kept, applied) and
   first_order_theorem_proving (proposed: its `No` cites `Outdated` alone, so its open consistency check now asks for
   its other reasons); its record says so.

8. **Add a Tensions row: a measured target scored within groups is not a ranking task?**

   * **Problem:**
     - Ranking tasks are out, also when a mirror serves them as regression (`microsoft_mslr`, `istella22`,
       `yahoo_learning_to_rank_challenge_data`, all `No`)[^ranking].
     - This use case now "ranks the candidate models", like `numerai_v5_2_1m` and `huesken_sirna_efficacy`, and all
       three are kept because the target is an absolute measurement and the source's task is regression[^scope],
       while learning-to-rank grades exist only per query.
     - No record and no Tensions row says so, and principles.md asks that a new decision on a tension not listed
       becomes a row.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No row (implemented) | the decision stays unwritten | none found | principles.md asks for a row |
     | B | Add the row | the AI writes it into principles.md | the reason is written down | none found |

   * **Recommendation:** B. **Decision:** approve the row (B)?

   **Notes for the AI:** proposed row: "a measured target scored per group against SEL-9 ranking: the source's
   regression target decides".

   [^ranking]: **SEL-9** (Must) excludes ranking tasks "also when a mirror serves them as ... regression".
   [^scope]: **SEL-8** (Must): the original task decides the scope.

   **Lennart (2026-11-05, change):** Option B: Add the row. Ranking predictions and using the prediction for ranking ar
   etwo different tasks and metrics, we care about the metrics driving it

   **Resolved (2026-11-05, Lennart):** B. A Tensions row in principles.md: a measured target scored within groups stays
   when the source's task is regression; grades that exist only per query stay out; ranking predictions and using a
   prediction for ranking are two tasks, and the metric follows the one the use case drives. Cases: numerai_v5_2_1m,
   huesken_sirna_efficacy and this dataset kept; the three learning-to-rank datasets out.

9. **Should `huesken_sirna_efficacy` declare `context="all_rows"` too?**

   * **Problem:**
     - With issue 5 accepted, this dataset follows `sat11_hand_algo_runtime` and departs from
       `huesken_sirna_efficacy`, decided the same day with `context="none"` and the same metric.
     - In huesken's use case a researcher selects which siRNAs to synthesize for a gene from candidate guides designed
       against its known target sequence.
     - The AI's best guess is yes, since a gene's candidates then form one set in hand before any is tested, like a
       protein's candidates here.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Reopen huesken, `all_rows` | a focused panel measures it | consistent with issue 5 | none found |
     | B | Record the fact that sets it apart | huesken keeps `none` | none found | none found |

   * **Recommendation:** A, reopen. **Decision:** does a researcher ranking siRNAs for a gene hold all of that gene's
     candidates at once? If so, A: reopen `huesken_sirna_efficacy` (a focused panel measures the effect there).

   **Lennart (2026-11-05, change):** Option A: Reopen huesken, all_rows.

   **Resolved (2026-11-05, Lennart):** A. huesken_sirna_efficacy is reopened as its issue 9 (`context="all_rows"` now or
   after a focused panel), with a CC line in its record. This also answers the consistency check on issue 5 with (b):
   huesken follows this dataset.

10. **Twenty repeats of the protein split, as the split count in scored units gives, instead of three?**

   * **Problem:**
     - The score averages one correlation per protein, so the split count now counts the 445 proteins, not the 94,083
       rows; 297 training proteins give 20 x 3 splits, where the definition was built with 3 x 3.
     - Three repeats do not rank close methods reliably: on two of three disjoint blocks of three repeats LightGBM and
       the random forest come out in the opposite order to the full run.
     - Ship 20 x 3, or keep fewer splits with these measurements as the reason?
   * **Effect on the task:** LightGBM (500 trees), a random forest and ridge, untuned, on the 20 x 3 splits under the
     declared metric (the per-protein Pearson correlation, averaged over proteins); t is the mean difference over its
     standard error across repeats:

     | Repeats | Order | LightGBM - forest | LightGBM - ridge | Forest - ridge |
     |---|---|---|---|---|
     | 0-2 | ridge, forest, LightGBM | -0.003 (t -1.1) | -0.009 (t -3.0) | -0.006 |
     | 3-5 | ridge, LightGBM, forest | +0.001 (t 0.5) | | |
     | 6-8 | ridge, LightGBM, forest | +0.002 (t 0.8) | | |
     | 0-9 | ridge, forest, LightGBM | -0.001 (t -0.5) | -0.006 (t -2.1) | -0.005 (t -2.0) |
     | 10-19 | ridge, forest, LightGBM | -0.004 (t -3.9) | | |
     | all 20 | ridge, forest, LightGBM | -0.003 (t -2.6) | -0.008 (t -4.5) | -0.006 (t -3.8) |

     Mean scores over the 60 splits: ridge 0.328, forest 0.322, LightGBM 0.320. The 60 fits took 34 s (LightGBM), 42 s
     (forest) and 1 s (ridge) in all. Ridge leading differs from the panel's LightGBM 0.355 against ridge 0.294 on the
     9 earlier splits, which predate the exclusion of the relaxed natives (issue 4); worth a look of its own.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 x 3 (implemented) | the splits as built | 9 fits per method | close methods ranked by chance (two of three blocks flip LightGBM and the forest) |
     | B | 20 x 3 | the split count in scored units, at the next `dataset check` | separates all three pairs; the count the rule gives; cheap for these methods | 60 fits per method, more for heavy ones |
     | C | 10 x 3 | an exception to the rule | 30 fits | one block of ten separates LightGBM and the forest, the other does not |

   * **Recommendation:** B: twenty repeats are the first that rank the three methods the same way every time, and the
     cost is in compute, not in the data[^10a]. **Decision:** A, B or C?

   [^10a]: **SPLIT-33** (Should): repeated 3-fold cross-validation with 20, 10, 3 or 1 repeats by the size of the
     train side, counted in the units the metric scores when the split holds each one out whole.

   **Notes for the AI:** on B, `dataset check` (the definition is unchanged; the protocol gives 20 x 3), a CC line in
   the record, CHANGELOG. On C, a `splits_comment` naming the measurement and the exception, and a SPLIT-33 Cases
   row. Evidence: `~/claude_jobs/protein_splits/` (run.py, res_*.csv, summary.txt).

**Review panel:** ship after changes (mediator). Tier full, second pass after Lennart's review of PR #33 on 2026-11-04.
Claims: 43 listed, 19 audit rows: 12 hold, 2 refuted (the "each such row has a same-length sibling" note, now 132 of
134; the metric's left-out proteins, issue 6), 3 untested (the five-fold RMSE figures, now marked historical; the CASP10
quote, which also names pooled scoring; the paper's Sections 2.2, 2.3 and 4.1), 2 concerns (decoy collections mixed
inside 19 merged proteins, about +0.01; the use case's "choose which to refine" against a whole-list correlation; both
now in the notes). Blind review: include with minor changes; its main concern is that the paper's random-split R² is not
comparable to the grouped task, and it could not confirm the SS definition. Task gamer's best exploit: rebuilding
proteins from the sequence length inside a test fold, 0.350 to 0.476, legitimate under `all_rows` (issue 5); the
abstention gap adds 0.008 (issue 6). Agreed: the rows match the author's file, the split and the alias map, the RMSD/TM
drop, the ED/PN and Energy calls, the per-protein metric. Disputed and settled by the mediator: the metric fix is a gate
(issue 6); "rn" means relaxed native, from the archive's folder (issue 4); CASP10 is a wording fault under USE-8, not a
P5 failure, fixed in the notes. Still disputed: the `Outdated` keep (issue 7). The mediator's curator issues 1-3 are
issues 7-9 here; its changes 1-3 are issues 6, 4 and 5 because they change the metric code, the rows or the grouping;
its changes 4-8 and 10 are applied to the notes, change 9 to the record.

<details><summary>Mediator</summary>

Verdict: ship after changes, after a library fix to the metric and a rebuild. Three disputed facts are now settled by my own experiments.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-9 holds (GDT_TS is a measured target and the source's task is regression; not a learning-to-rank task);
  USE-3 holds (direct fit fails, approximate fit stated); LEAK-10 holds (RMSD and TM dropped);
  native-reference exclusion triggered again: the 1,011 `rosetta62_*_rn<pdb>.out.N` rows are relaxed natives,
  confirmed (the Baker archive keeps them in a folder named `relaxed_natives/`); fixed by excluding them by identity
  (CLEAN-11 via USE-7, like cases alike);
  SPLIT-23 triggered: `context="none"` contradicts the use case (the actor holds all of a protein's candidates);
  fixed by declaring `context="all_rows"` (as for sat11_hand_algo_runtime);
  SPLIT-1, SPLIT-24 and SPLIT-26 hold (0 groups shared across 9 splits, alias map hash-checked);
  USE-8 triggered: the SL wording is wrong for CASP10; fixed in the text.
Value: MET-1 holds (Pearson stands in for top-1 loss and ranks models the same way); MET-5 departure kept (exception,
  Lennart 2026-11-04); MET-2 and MET-13 triggered by the abstention gap in `_mean_group_pearsonr`; fixed in the library;
  TP-3 holds on the declared metric (LightGBM 0.355 vs ridge 0.294, LightGBM ahead 9 of 9).
Quality: CLEAN-11 applied (ED/PN set missing, Energy kept); EV-6 and EV-8 triggered by stale or overstated text, fixed.
Weighed: grouped biology is thin in the collection +, 445 groups / 95k rows +, traceable source +,
  historical descriptors (Outdated) -, 64% classic decoy sets -.
For the curator: issue 1, the Outdated consistency check against first_order_theorem_proving.
```

**Disputes settled**
- **Abstention gap: gate or alongside?** Gate. Both sides agree MET-2 and MET-13 are Musts and the rebuttals agree it lands before shipping. My test with the library scorer on split 0:
  - an exact constant (0.5 or 0.25) returns NaN;
  - 0.3 or the training mean scores about 0 (1e-16);
  - noisy predictions score 0.736. Set half the proteins to the constant 0.5 and the score goes up to 0.745. Use 0.3 instead and it falls to 0.378.
  - It is an independent failure, not a conflict with another rule.
- **What "rn" means.** Settled from the source archive itself (EV-2, a primary document ranks above inference). In Zenodo 48780 `rosetta_decoys_62proteins.tgz`, the files `rn<pdb>.out.N.pdb` sit under `relaxed_natives/`, next to `first_decoys/` and `low_score_decoys/`.
  - With these rows, LightGBM scores 0.355 overall. Without them it scores 0.322, lower in 9 of 9 splits.
  - Inside the 56 rosetta62 proteins the score falls from 0.596 to 0.310.
  - The critic's gate holds and the remedy is the same for both sides: the identity filter. Every group keeps its BOINC decoys.
- **Is CASP10 "unlearnable", and is it a P5 failure?** Neither. On the shipped folds, a LightGBM that uses group context (each feature's z-score and rank within its protein, plus SL/max SL and group size) scores:

  | | CASP10 groups | All groups |
  |---|---|---|
  | Context model | 0.615 (0.574-0.667) | 0.517 |
  | Row-only model | 0.050 | 0.355 |
  | Raw SL alone | 0.502 | n/a |

  The values match the author's release row for row, so P5 holds. What is wrong is our `known` text (USE-8), and the fix is text. Dropping CASP10 is not needed once the context is declared.

**Changes to make now (no decision needed)**
1. **`src/data_foundry/v2/metrics.py` `_mean_group_pearsonr` (MET-13, MET-2).** A group whose target varies but whose predictions do not scores 0. Drop a group only when its target is constant (none here). Add tests with the constants 0.3 and 0.5 and with all groups constant (now NaN). This also covers huesken and numerai. Then restate the Metric text.
2. **`_clean` (CLEAN-11 via USE-7, the existing native exclusion).** Exclude `_rn[0-9a-z]{4}\.out\.` by identity. That gives 94,083 rows and still 445 groups. Update `task_summary.row`, `changes` and the comments' counts. Cite the archive folder as evidence.
3. **`grouping.context="all_rows"` (SPLIT-23, USE-6).** No new column, so Lennart's "no new features" stands. Task gamer exploit #1 (0.476; 0.516 with the true groups) becomes legitimate use, which matches my 0.517.
4. **SL wording in `known` and the comments (USE-8).** In CASP10, SL is the candidate's own length (it varies within 67 of 67 targets); in CASP6-9 it is constant per target. Also:
   - add the forward-window numbers to `splits_comment` (CASP8 0.340, CASP9 0.483, CASP10 0.016) and the source's CASP10 hold-out;
   - add one line on the 2,259 CASP10 rows that are not in the paper's validation file.
5. **`fit_reason` (USE-8).** Name the inputs the actor knows but we leave out: the server and its TS index, the decoy generator, and the target's full length. Name the collections mixed inside 19 merged proteins (about +0.01).
6. **Use case and metric reason (MET-1, USE-1).** Say "rank the candidates". Name top-1 GDT_TS loss as the decision Pearson stands in for (practitioner's three models: 0.360 / 0.522 / 0 Pearson against 0.158 / 0.118 / 0.199 top-1 loss). Rest the per-target choice on the use case, because the CASP10 quote also endorses pooled scoring.
7. **TP-3 text (EV-8; the `african_credit_scoring_challenge` precedent).** Replace the 5-fold RMSE comparison (7.37%) with LightGBM 0.355 vs ridge 0.294, 9 of 9 splits. Mark the 5-fold figures historical.
8. **ED/PN bullet (EV-6).** Write "132 of 134 have a same-length sibling". The other two (`CASP10_T0692_FALCON-TOPO_TS5.pdb`, `CASP10_T0716_sysimm_TS4.pdb`) have same-protein siblings with positive values.
9. **Record.** Mark as superseded the 2026-10-29 lines "RMSE is the fallback" and "Preserve those values". Replace the "no panel ran" Assessment.
10. **Optional (CLEAN-11).** Add to the SS bullet: 5,414 rows exceed the largest SL of their protein.

After these, the build is stale. A rebuild happens only when the curator asks (house rule).

**Issues for the curator, ranked**
1. **`Outdated` keep against `first_order_theorem_proving` (`No` on `Outdated` alone).** Consistency case 2; a weighing.
   - Advocate: the majority of precedents keep (heart_disease, covertype, horse_colic_survival), grouped biology is thin, and the descriptor set is documented.
   - Critic: an open check is not a precedent.
   - What settles it: answer the precedent-checker's prompt: (a) the gap and the documented measurement set, recorded as the fact; (b) treat this one like first_order; (c) reopen first_order to keep; (d) an amendment that gives `Outdated` a rule. Choosing `Outdated` or `Not Representative` as the marker is a minor part of the same call.
2. **SEL-9 Tensions row.** Rule: principles.md says "a new decision on a tension not listed becomes a row".
   - The pattern: numerai, huesken and this dataset are measured regression targets scored within groups.
   - The proposed fact: the source's regression target decides.
   - Decision: approve the row.
3. **Huesken's `context="none"`.** Change 3 follows sat11 (`all_rows`, candidates of one instance) and departs from huesken, decided the same day, which declares `none`. Decision: does huesken's actor also hold a gene's whole candidate pool? If so, reopen huesken.
4. **Already decided, no action unless you reopen.** Shipping the server index, the generator or the target length (USE-6 makes them legitimate). "No new features" (2026-11-04) covers them; change 5 names them.

**Task gamer's exploits** (the definition has no `Potential leak, kept on purpose:` notes and no accepted warnings, so all are new)
- **#1 and #1b, test-pool pseudo-groups:** +0.126 over baseline (true groups 0.516). Rule SPLIT-23 / USE-6. Resolved by change 3: legitimate under `all_rows`.
- **#2 abstention on top of #1:** +0.008. **#2b raw SL:** 0.410, which falls to 0.084 under the fix. The claim auditor's version: 0.428 and 0.492 against 0.355. Rule MET-13 / MET-2. Resolved by change 1.
- **Training-row choices and the format, order and copy attacks:** no gain. Missing inputs: USE-6, covered by issue 4.

**Agreed facts**
- **Rows:** 99,987 raw; 4,893 natives dropped by identity; 95,094 kept. All of them match `RF-PCP-Full-dataset.csv`.
- **Groups:** 453 source keys become 445 groups; hash checked; 0 groups shared across 9 splits; 0 copies of the six features. The (SL, PN) collisions are unrelated proteins.
- **Grouping matters:** under the declared metric, IID 0.511 against grouped 0.366. No drift through CASP9 (within 0.03).
- **Metric numbers:** the per-protein oracle reaches 0.134 RMSE against 0.187 for LightGBM (9 of 9 splits). Each fold holds 148-149 groups of at least 13 rows. Noise scores 0.0007.
- **Columns:** RMSD and TM alone give R² 0.84 and 0.87, so they are dropped correctly. ED/PN set missing in 71 + 63 rows, with no signal in the missingness. Energy reaches 6.98e11 and stays.
- **SS** compares STRIDE with PSIPRED per the record's reading of the paper; the panel did not re-open the paper (EV-7). OpenML 42903's sibling is already retired.

**Consistency with precedent**
- **MET-5 exception:** follows huesken and numerai. This is the second exception with this reason; the third triggers an amendment.
- **ED/PN and Energy calls:** follow caracas, heart_disease and mortgage (CLEAN-11); set apart from clock_protein_toxicity.
- **`rn` exclusion:** extends the accepted native exclusion; the same fact (a reference structure, not a candidate).
- **`all_rows`:** follows sat11_hand_algo_runtime. The departure from huesken is issue 3.
- **SEL-12:** follows ecoli_proteins (hand-made descriptors, not learned embeddings).
- **Split:** follows sat11 and huesken (entities, not families).
- **`Outdated` keep:** departs from first_order_theorem_proving; issue 1.
- **Register flag** `exception_to_must MET-1`: a parser false positive. The exception is to MET-5.

</details>

<details><summary>Claim audit</summary>

**Claim audit: `protein_model_quality_rf_pcp` (claim-auditor, second pass, 2026-11-04)**

**Answer to focus.md.** focus.md asks no question of its own. I tested every pointer it names:
- **Holds:** the key recovery and the alias map, the group split, the native-row exclusion, the ED/PN rule, the two kept perfect-label rows, and the 0.134 against 0.188 numbers.
- **Refuted, and the most important finding:** the metric's edge case. `mean_group_pearsonr` leaves out a group whose predictions have no variance. So a model can skip the proteins it is unsure of by predicting an exact constant there, and its score goes up. Whether such a group is left out or scored about 0 depends on floating-point rounding of the constant chosen.

All numbers come from the definition's own frame (`dataset_io.from_definition`, raw state traced by index) on the 9 shipped splits, with untuned LightGBM and ridge models.

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 3, 12, 27 | 99,987 raw rows; 4,893 native rows dropped; 95,094 kept | task_summary.row, CC | ran `_clean` on the raw CSV | holds | 99,987 → 4,893 dropped → 95,094; the only duplicated PDB-ID (`native_1H30.pdb`) is among the dropped rows | CLEAN |
| 12, 29 | two kept perfect-label rows, plus T0676 with RMSD 0 | CC | count rows with GDT = 1 or RMSD = 0 | holds | 3 rows with RMSD 0 (the named ones). 10 rows have GDT 1.0; the other 8 are rosetta62 decoys of 1a68/1vie with RMSD 0.46-0.54 and TM ≥ 0.955, which are real near-native decoys | CLEAN-11 |
| 17, 31 | 453 source keys become 445 groups; 6 components hold 14 keys; hash-checked map | CC | recomputed keys; checked the hash; listed the non-CASP aliases | holds | 453 → 445. The 8 non-CASP aliases form 6 components holding 14 keys: 1aa2/1bkr, 1aiu/1erv, 1enh/1hdd, 1igd/1pgb/1pgx, 1lou/1ris, 1ig5/3icb/4icb. The hash check passed | SPLIT / P4 |
| 6, 18 | 342 CASP keys, 339 linked to a PDB, none shared with a classic key | split, CC | set overlap; duplicate alias values | holds (internally) | 342 CASP keys; 339 aliases; CASP alias values ∩ classic keys = ∅; 0 duplicated values. Only 1 filename cross-check was possible (`casp5_T0156_1nxj` → 1nxj, agrees). I did not re-open the 339 organizer links | P4 |
| implied | the split holds out whole proteins, with no copies across it | splits | group overlap and exact feature copies | holds | 0 shared groups in all 9 folds; 0 rows anywhere with an exact 6-feature copy. Grouping is decisive: IID R² 0.723 against grouped 0.156 (prep) | SPLIT, LEAK |
| 15, 39 | 71 rows with ED = 0, PN > 0 and 63 with PN = 0, ED > 0 set missing; PN constant in 1,146 of 1,249 protein × length cells | CC | recount | holds | 71 / 63; 1,146 of 1,249 on source keys (1,141 of 1,245 after aliases) | CLEAN-11 |
| 15 | "Each such row has a same-protein, same-length sibling with the value positive" | CC | per-row sibling search | **refuted (2 of 134)** | `CASP10_T0692_FALCON-TOPO_TS5.pdb` (SL 462) and `CASP10_T0716_sysimm_TS4.pdb` (SL 54) are the only rows of their length in their protein. Their proteins do have positive PN (119/120 and 129/130 rows) | EV-6 |
| 20 | Energy reaches 7e11; extreme rows have mean GDT 0.339 against 0.398 | CC | thresholds 5e5 to 2e6 | holds approximately | max 6.98e11; Energy > 1e6: 0.337 against 0.398 (4,479 rows); > 7e5: 0.342. The threshold is not stated | EV-8 |
| 19, 40 | the per-protein true mean beats LightGBM on pooled RMSE, 0.134 against 0.188 | metric reason | per-fold RMSE of the oracle group mean | holds | 0.1343 against 0.1865 (mean of 9 folds; oracle wins 9/9) | MET-1 |
| 19 | each test fold holds 148-149 proteins, median 103-113 candidates, none under 5 | CC | count per fold | holds | 148-149 groups; medians 103-112(.5); minimum 13; 0 groups with constant GDT | MET-2 |
| metric (computable) | `mean_group_pearsonr` on `protein_id` is computable and tells models apart | `dataset.py` metric | scored dummies and models with the definition's spec | holds | LightGBM 0.355; ridge 0.294 (LightGBM higher in 9/9 folds); Gaussian noise 0.0007; constant train mean 0.000; LightGBM on SL+PN only 0.006 | MET-2 |
| metric (edge case) | "groups with undefined correlation are left out" scores the decision | library docstring, README Metric block | label-free abstention: predict an exact constant on the proteins with the lowest predicted spread | **refuted** | Constant 0.5 on the bottom 50% → **0.428**; on the bottom 75% → **0.492**; the real model scores 0.355 (gain in 9/9 folds). The same move with constant 0.3 gives **0.220**: 0.3's group mean is inexact in float, so those groups are scored about 0 instead of left out (147 of 149 counted in a test fold). | P6, MET-2, MET-13 (Must) |
| 19, metric reason | CASP10 scores QA per target ("we use both of them") | metric reason | web search; PMC and CORE full text blocked | untested verbatim | The quoted sentence itself says CASP used both per-target and pooled correlation. So the citation does not single out per-target; the use case (ranking one protein's candidates) does | MET-1, MET-11 |
| implied (metric unit) | a protein's candidates form one ranking pool | grouping | 19 merged groups span 2 or more decoy collections; scored per protein and per (protein, collection) | concern | 24,945 rows (26%) sit in those 19 groups. LightGBM per protein: 0.48-0.75; per (protein, collection): 0.22-0.56. A model that only knows each collection's mean GDT scores 0.46-0.79 per protein. Weight in the fold mean is about 6/148 groups, roughly +0.01 | MET-2 (Weigh) |
| 11, 32 | Ridge 0.19318568 against LightGBM 0.17894541 on 5 folds (7.37%) | CC | 9-fold untuned recompute | untested exactly; stale | The 5-fold frames are not in the folder. Untuned 9-fold RMSE is 0.1865 (LightGBM) against 0.1871 (ridge). RMSE is no longer the metric; on the declared metric the spread is +0.061 in 9/9 folds, which answers `no_spread` better | TP-3, EV-8 |
| 2 against 31 | the use case says "to choose which to refine"; the record says top-one selection usefulness is not claimed | use_case, record | read both | concern | Pearson over all candidates is not a top-1 selection loss. The two texts disagree mildly | USE-1 (Weigh) |
| 9, 5 | every feature is known at the prediction point | CC | read the source descriptions | holds (P4 partly unverifiable) | All six features come from the model structure and the target sequence (PSIPRED from sequence). The archive has no feature-generation code | P4 |
| 25 | 0 warnings, 1 info | check.txt (prep) | not re-run | holds per prep | n/a | n/a |
| 14, 28 | source Sections 2.2, 2.3 and 4.1 | CC | paywalled paper | untested | I did not open the paper | EV-7 |

**Refuted and untested, ranked by principles.md (validity first, Must first)**

1. **Metric edge case (P6, MET-2, MET-13 Must; refuted).**
   - The library's `_mean_group_pearsonr` drops groups with `var == 0`. A participant who predicts an exact float constant such as 0.5 on uncertain proteins lifts LightGBM from 0.355 to 0.428 (abstaining on 50%) or 0.492 (75%) without any label.
   - The use case has the researcher rank every protein, so abstaining should not pay.
   - The score also depends on rounding: 0.5 gets the groups dropped, while 0.3 gets them scored about 0, giving 0.220.
   - The same code path serves `huesken_sirna_efficacy`. `numerai_v5_2_1m` (`method="numerai_corr"`) has the same left-out rule; I did not test it.
   - **Mildest remedy, in the library, not this `dataset.py`:** a group whose target varies but whose predictions do not (exactly, or below a relative tolerance) scores 0 instead of being left out. Keep dropping only groups whose target is constant (none here). Add tests with constants 0.3 and 0.5, then re-state the definition's Metric text.
2. **Claims 11 and 32 are stale and untested (EV-8 Should).** The 7.37% RMSE comparison argues for a metric that has since been replaced, and its 5-fold frames are not available. **Remedy:** restate on the declared metric (LightGBM 0.355 against ridge 0.294, higher in 9/9 folds) or mark it historical.
3. **Collections mixed inside merged proteins (MET-2 Weigh; concern).** In 19 groups, the per-protein correlation partly rewards telling decoy collections apart; the effect on the fold mean is about +0.01. **Remedy:** one sentence in the metric reason; no change to the data.
4. **Claim 15's "each such row" (EV-6; refuted in 2 of 134 rows).** **Remedy:** "132 of 134 rows have a same-length sibling; the other two have same-protein siblings with positive PN". The CLEAN-11 decision is unaffected.
5. **Use case against metric (USE-1 Weigh).** "Choose which to refine" implies top-1 selection, which the record disclaims and Pearson does not score. **Remedy:** reword the use case to "rank the candidates", or note the gap in `fit_reason`.
6. **Untested (EV-7):**
   - the 339 CASP organizer links (only 1 filename cross-check agrees);
   - the verbatim CASP10 quote (full text blocked; as quoted, it also endorses pooled scoring);
   - the paper's Sections 2.2, 2.3 and 4.1;
   - the Energy cut behind 0.339.

Sources:
- [MULTICOM CASP10 QA paper (PMC3996498)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3996498/)
- [Assessment of the assessment, CASP10 (unibas record)](https://forschdb2.unibas.ch/inf2/rm_projects/object_view.php?r=2158297)
- [PMC4180100 (blocked by a CAPTCHA)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4180100)
- [CORE PDF (403)](https://core.ac.uk/download/54299431.pdf)

</details>

<details><summary>Column audit</summary>

**Column audit: protein_model_quality_rf_pcp (column-auditor, 2026-11-04)**

**About focus.md.** It asks nothing beyond the standard panel, so I audited every column. Of its pointers, I re-measured the native exclusion, the ED/PN missing rule and the perfect-label rows. Two hold up. The native exclusion does not quite: the identity rule misses about 1,011 rows that look like relaxed natives (problem 1 below).

How I read the frame: through `dataset_io.from_definition`, rebuilt from the raw files without a container. That gives 95,094 rows × 8 columns. `feature_cols` holds the six descriptors, without `protein_id`. The dtype probe flagged 0 of 6 columns (`--no-fetch`, no codebook online).

**Column table**

| column | meaning (paper Sec. 2.2-2.3, via record) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| Area | Total solvent-accessible surface area of the candidate, Å² | Yes, from the model's own coordinates | float64; 0 missing, 0 zeros; Area/SL 29.6-141.5 Å² per residue, plausible | fine | USE-6, CLEAN-14 |
| ED | Sum of C-beta distances over the PN aliphatic pairs | Yes, from the model | float64. 71 cases of ED=0 with PN>0 set to missing (CLEAN-11, Lennart). ED/PN (mean pair distance) runs 8.0-160 Å with median 16.6; 22 rows exceed 100 Å, unusual but not impossible for extended decoys. The missing rows sit 0.022 GDT below their protein's mean; the prep indicator R2 is -0.003, so the missingness carries no signal. | fine | CLEAN-11, LEAK-13 |
| Energy | ProSEE empirical energy, signed | Yes, from the model | float64. Runs -15,906 to 6.98e11; 4,479 rows above 1e6, 48,258 negative. Kept as supplied (Lennart). | fine (decided) | CLEAN-11 |
| SS | Secondary-structure penalty, STRIDE (model) against PSIPRED (sequence) | Yes; neither input uses the native | int64, 394 values, 39 zeros. 5,620 rows have SS > SL; 5,414 exceed the largest SL in their protein; 944 exceed 2×SL. The equation and the prose disagree. If SS counted residues, these values would be impossible. Kept, since "the source gives no bound" (Lennart). | fine (decided); small open point below | CLEAN-11 |
| SL | Sequence length of the candidate model | Yes | int64, a count, numeric. Constant within 79.6% of proteins. Where it varies (91 proteins), mean within-protein Spearman with GDT is +0.416. That is model coverage, which is legitimate, because GDT_TS is normalised by the target length. | fine | USE-6, CLEAN-14 |
| PN | Number of aliphatic residue pairs (set by the sequence) | Yes | float64 (a count; missing values force float). 63 cases of PN=0 with ED>0 set to missing. 0 rows have PN > SL(SL-1)/2. | fine | CLEAN-11, CLEAN-14 |
| GDT (target) | GDT_TS, the fraction aligned within 1/2/4/8 Å, from 0 to 1 | Outcome | float64, 0.0116-1.0, no transform. 10 rows have GDT = 1.0: the 2 named ones and 8 rosetta62 `rn` rows (problem 1). | fine | USE-5, CLEAN-15 |
| protein_id | Canonical target key from the filename, plus the alias map (hash 6ca86a5b checked in `_clean`) | Group, not a feature | category, 445 levels, used as the group and as the metric input. Not in `feature_cols`. | fine | LEAK-33, SPLIT-29 |
| PDB-ID (dropped) | Filename of the candidate structure | Partly (see problem 3) | Turned into protein_id, then dropped. One duplicate (`native_1H30.pdb` ×2) leaves with the natives. | fine | CLEAN-3 |
| RMSD, TM (dropped) | Alternative outcomes measured against the native | No, they need the reference | Dropped. Raw probe: alone they give R2 0.84 and 0.87. | fine (dropping them is correct) | LEAK-10 |

No column is a post-outcome field, and no missingness is caused by the outcome. No window ends at the outcome. protein_id does not encode the label.

**Problems, ranked (principles.md: P3/P4 validity first)**

**1. Probable relaxed-native rows kept in rosetta62 (P3/P4: USE-3, USE-7, and the curator's own native exclusion). Question for the curator, validity rank. Effect is strong.**
- **What I found:** `_clean` removes references only by the `native_` prefix or the `_native.pdb` suffix. The rosetta62 set has two filename families in each of its 56 proteins:
  - de novo decoys `..._BOINC_ABRELAX_...` (6,125 rows, median GDT 0.415);
  - `rosetta62_<pdb>_rn<pdb>.out.N.pdb` (1,011 rows, 15-20 per protein).
- **Why the `rn` rows look derived from the reference:**
  - Their RMSD is 0.44-2.82 Å (median 0.82) and their GDT is 0.74-1.00 (median 0.961).
  - Within their protein they rank 0.92 on GDT and are the most compact (Area rank 0.22, ED rank 0.19).
  - In 55 of 56 proteins the best-GDT row is an `rn` row.
  - "rn" fits Rosetta's naming for relaxed natives, i.e. the experimental structure refined.
  - No other set has rows like these: lattice, fisa, John2002 and lmds have 0 rows above GDT 0.9, ROSETTA has 1 and 4state has 14.
- **Effect on the metric:** in those 56 groups (12.6% of the 445 the per-protein metric averages over), the mean within-protein Pearson with GDT moves as follows when the `rn` rows go:

  | descriptor | with `rn` | without `rn` |
  |---|---|---|
  | Area | -0.558 | -0.335 |
  | ED | -0.464 | -0.281 |
  | SS | -0.394 | -0.165 |
  | Energy | -0.228 | -0.103 |

- **Why it matters:** if "rn" does mean relaxed native, these candidates cannot exist before the reference is available. They are the same kind of row as the 4,893 natives Myunghwan excluded by identity, so like cases should be treated alike.
- **Not confirmed:** the meaning of "rn". The Zenodo record of the Baker decoy sets ([zenodo.org/record/48780](https://zenodo.org/record/48780), file `rosetta_decoys_62proteins.tgz`, CC0) says only "Rosetta decoy training sets for various uses".
- **Mildest remedy:**
  1. Check the README or paper of that archive.
  2. If "rn" means relaxed native, add `_rn[0-9a-z]{4}\.out\.` to the identity exclusion. That takes 95,094 rows to 94,083 and changes task_summary.row and the comments' counts.
  3. If it stays unverified, name these rows in a bullet, as is already done for the two perfect-label IDs.

**2. SS above the sequence length (P7, CLEAN-11). A note, already decided.** In 5,414 rows SS exceeds every SL of the protein, and in 944 it exceeds 2×SL. Lennart's line "SS has no bound the source gives" covers it. The only gap: the comment gives the 5,620 count against the row's own SL, not the stronger fact that 5,414 exceed the protein's largest SL. No change proposed. A one-clause addition to the existing bullet is optional.

**3. Information in the filename that is known at the prediction point but not shipped (P7: CLEAN-3, CLEAN-19, USE-6). A weighing call, probably already settled.** PDB-ID carries the generator (CASP server, decoy set) and the server's own model rank (TS1-5). The rank is known before the reference. Across 342 CASP targets, the mean per-target Spearman of the model index with GDT is -0.141. It is not a leak. Lennart's 2026-11-04 line "Kept as a small grouped biology task, with no new features" covers it. I raise it only so the call is explicit. Recommendation: no change.

**4. Rows with GDT = 1. Fine as documented.** The 2 named rows (casp5_T0156_1nxj.nNh1.pdb and ROSETTA_1aa2_1aa2h2.pdb, with RMSD 0 and TM 1) and CASP10_T0676_HOMER_TS2.pdb are as the comments state. The other 8 GDT = 1 rows are all rosetta62 `rn` rows, so they fall under problem 1.

**Verdicts in judgment-record form**

- Validity:
  - USE-3 and LEAK-10 hold for all six features.
  - LEAK-33 holds.
  - The RMSD/TM drop is correct.
  - Open: whether the population includes 1,011 rows that probably derive from the reference (issue 1).
- Value: not my role.
- Quality:
  - CLEAN-11 is applied to ED/PN (71 + 63 rows; they add no signal).
  - Energy and SS are kept by the curator's decision.
  - CLEAN-14 dtypes are all correct: counts numeric, the group categorical.
  - The dtype probe has no flags to answer.
- For the curator, issue 1: confirm "rn" in the Baker 62-protein archive, then exclude by identity, or keep with a note.

Sources:
- [Rosetta Decoy Datasets, Zenodo 48780](https://zenodo.org/record/48780)
- [Tsai et al. 2003, improved Rosetta decoy set](https://www.ipd.uw.edu/publication-pdfs/100/548835f180655b28e23343f85444072a/Proteins%20-%202003%20-%20Tsai%20-%20An%20improved%20protein%20decoy%20set%20for%20testing%20energy%20functions%20for%20protein%20structure%20prediction.pdf)

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The grouped split by canonical protein matches the use case. The source's own temporal design (train on CASP5-9 plus the classic sets, validate on CASP10) adds nothing for CASP5-9: forward windows there score the same as the grouped folds. CASP10 fails under both splits, because its descriptors follow another convention, so that is a data question rather than a split question.

**Focus question.** `focus.md` asks nothing beyond the standard panel. On its pointer about the group split (probe gap 0.567): the grouped split is correct, and the gap is not what decides it (SPLIT-4). The use case decides it (USE-10, SPLIT-23).

**Regime against the use case**
- **Actor and entity.** A researcher ranks the candidate models of one protein whose experimental structure is not yet known. The model is trained on proteins with known references and applied to a new target. That is a new entity, a cold start (USE-10), so a grouped split is right (SPLIT-2).
- **What one prediction is.** One prediction is one candidate row, scored as the correlation within each protein, which is how CASP assesses quality per target (SPLIT-23). Grouping on `protein_id` with `prediction_unit="row"` and `mean_group_pearsonr` on `protein_id` agree with this.
- **Group id (SPLIT-24, SPLIT-26).** The id comes from the source filenames: CASP T identifiers, PDB accessions for the classic sets, and a hash-checked alias map from organizer pages, RCSB and UniProt. It is not a similarity cluster or a hash of features.
  - There are 445 groups. 9 of them span more than one classic collection (1ctf, 1enh, 1fc2, 1ig5, 1igd, 1r69, 1shf, 2cro, 4pti), so the merges work.
  - Over all 9 shipped splits, no group is on both sides.
- **Missed-alias check (mine).** 354 groups have a constant length (SL) within the group. Among them, 4 pairs of different groups share an identical (SL, PN) pair: 1cew/1s04, 1e6i/2hh6, 2i9c/3nkl, 1m6y/3nyi. RCSB sequences show all 4 pairs are unrelated proteins (for example, chicken cystatin against Pyrococcus PF0455). So no missed alias turned up. Independence of sequence families is still not claimed, as `splits_comment` says.
- **IID against grouped under the declared metric (3x3 folds, mine).** LightGBM scores 0.511 IID against 0.366 grouped, a gap of 0.145. Ridge scores 0.327 against 0.330. The grouped folds' spread for LightGBM is SD 0.021 (range 0.328-0.403). Each test fold holds 148-149 groups.
- **Temporal rules.** The task has no time column, so the gap, label-delay and window rules do not apply. The CASP edition is an implicit time index, though (SPLIT-7), and the source's own split is temporal, so I tested it next.

**The alternative split I ran: the source's split, then forward windows by CASP edition**

The archive's `RF-PCP-Training-Testing-CASP-5-9.csv` and `RF-PCP-Validation-CASP-10.csv` amount to "train on everything before CASP10, test on CASP10". SPLIT-5 says to check a split the source prescribes, and SPLIT-19 says to follow it when it is the source's definition. Models are untuned LightGBM (400 trees) and a ridge on signed-log, standardised features. The score is the mean correlation within each protein.

| Test window (train on everything earlier) | Train rows | Groups | LightGBM | Ridge | Same groups in the shipped folds (LightGBM) |
|---|---|---|---|---|---|
| CASP8 | 72,698 (76%) | 74 | 0.340 | 0.292 | 0.369 |
| CASP9 | 79,524 (84%) | 77 | 0.483 | 0.394 | 0.489 |
| CASP10 | 87,761 (92%) | 67 | 0.016 | 0.033 | 0.048 |
| CASP10, trained on CASP only | n/a | 67 | 0.029 | 0.033 | n/a |
| Control: 67 random CASP5-9 groups held out, 5 draws | n/a | 67 | 0.415 | 0.326 | n/a |

- **No drift over time.** Through CASP9, forward windows match the grouped folds to within 0.03.
- **CASP10 is a break, not drift.** It stays near 0 even when two thirds of the CASP10 targets are in training (shipped folds 0.048). Under random IID folds LightGBM reaches 0.310 on CASP10 and ridge only 0.031.
- **Conclusion on the split.** A temporal split would only re-test this break, on a single 67-group window. Keep the grouped split.

**Problems, ranked by `principles.md`**

**1. Concern (P5/P4, for the column and claim auditors): CASP10's descriptors follow another convention, and a trivial ranking beats every trained model on those targets.**
- **Evidence:**
  - SL varies within a protein in 99% of CASP10 groups (the paper's validation rows) and 80% of the other CASP10 rows. In CASP6-9 it varies in 0%, in CASP5 in 5%.
  - The median Spearman correlation of GDT with SL within a protein is +0.57 in CASP10, against 0 or undefined in CASP6-9. Area's correlation flips sign: +0.07 to +0.24 in CASP10 against -0.18 to -0.42 in CASP5-9.
  - Ranking the candidates of a protein by raw SL gives 0.501 on CASP10. The best trained model gives 0.016-0.048.
  - Reading: in CASP10, SL is the model's own residue count, so it measures coverage of a GDT that is normalised by the full target length. In CASP5-9, SL is constant per protein, so it acts as a property of the target.
- **Why it matters:** the definition's `known` text calls SL "sequence length" for every row (P5, "the data is what it claims to be"). 15% of the scored groups (67 of 445) are close to unlearnable from per-row inputs, which pulls down every model's mean.
- **Mildest remedy:** document it, with no re-split and no filter.
  - Add to `splits_comment`: the source's CASP10 hold-out, the forward-window numbers above, and that CASP10 descriptors measure the candidate model.
  - Correct the SL wording in `known` / `curation_comments`.
  - Whether to keep CASP10 is the curator's call.

**2. Note (SPLIT-23, USE-6): what is known about a new group.**
- **Evidence:** at the prediction point the researcher knows the target sequence, so its length, and holds the protein's whole set of unlabelled candidates. The task declares `context="none"`, and the group column is not a feature, so a row-level model cannot normalise SL by target length. That is exactly the signal worth 0.50 on CASP10.
- **Rule:** SPLIT-23 requires stating what is known about a new group, and USE-6 makes anything known at the prediction point a legitimate input. Lennart's decision of 2026-11-04 says no new features.
- **Mildest remedy:** one sentence in `fit_reason` or `splits_comment` saying the per-row setup leaves out the target length and the candidate-set context. No change to the split.

**3. Note (provenance, not the split): rows the paper's validation file does not contain.**
- **Evidence:** the full CSV holds 2,259 CASP10 rows that are not in the paper's validation file. They spread over 66 of the 67 CASP10 targets, with median GDT 0.238 against 0.441 in the validation file and median SL 264 against 204.
- **Remedy:** record the fact. This is for the claim auditor.

**4. Note: fold sizes are uneven in rows, even in groups.**
- **Evidence:** test folds hold 25,023-36,376 rows, because the classic decoy groups are large (95th percentile 922 rows, largest 3,794 for 1ctf). The metric weights each protein equally and each fold holds 148-149 groups, with at least 13 candidates per group.
- **Remedy:** none needed.

**What passes.**
- The regime is right (USE-10, SPLIT-1).
- The group id is true and exact (SPLIT-24, SPLIT-26).
- No group crosses the split.
- No missed alias was found by the (SL, PN) signature check.
- The grouped split is decisive under the declared metric too (0.511 against 0.366).
- No temporal drift through CASP9 (SPLIT-7 checked, so the source's temporal split is not needed).

</details>

<details><summary>Domain practitioner</summary>

**protein_model_quality_rf_pcp: domain-practitioner review (second pass, 2026-11-04)**

**focus.md asks** for nothing beyond the standard panel. My direct answer: the use case is real and approximate is the right fit. But two things the definition does not say change what the benchmark measures. First, the shipped grouped split hides a descriptor-convention break in CASP10. Second, `grouping.context="none"` denies the model the sibling candidates that the actor always has.

**Fit: approximate (agree, USE-8).** The data mirrors CASP-era single-model quality assessment of a new target's candidates. However, 64% of rows are classic decoy sets rather than a researcher's candidates, and the descriptors do not follow one convention across CASP rounds (gap 1). That makes it a stand-in with known gaps, not a mirror.

**How the decision is made (actor: a QA researcher or structure predictor at CASP time).** For each new target the organisers release all server models at once: about 20 in stage 1 and about 150 in stage 2. I score every model and pick the top one(s) to refine or submit. CASP7-10 used GDT_TS as the main measure, and CASP10 used per-target correlation and top-1 loss side by side. From CASP11 on, "the main emphasis is placed on the ability … to identify the best models". Consensus methods won by comparing the models of the same target.

**Gaps, ranked by how much they change the task**

1. **CASP10 follows another descriptor convention, so the next round is not served (USE-3, USE-8, P4).**
   - SL varies within 100% of CASP10 targets (67/67) but within 0% of CASP6-9 targets and 5% of CASP5.
   - Area's mean per-target Pearson with GDT flips from about -0.22 to -0.46 in CASP5-9 to +0.157 in CASP10. SL/PN go from no variance to +0.50.
   - LightGBM trained on everything except CASP10 and tested on the 67 CASP10 targets scores mean_group_pearsonr 0.006. Its top-1 loss is 0.317, against 0.224 for a random pick. With group context it is worse: -0.059 and 0.409.
   - On the shipped kind of split (random grouped, 3-fold GroupKFold) the same model scores 0.360, because every fold mixes the rounds.
   - The source's own files split CASP5-9 (train) from CASP10 (validation), which is the split a practitioner would face.
   - Whatever the cause (models trimmed to common residues vs. full-length models, or SL meaning target length vs. model length), the inputs are not one pipeline. The record's "unresolved descriptor conventions" understates this.
   - I would not trust predictions for a new round's candidates computed by any one pipeline.

2. **`grouping.context="none"` contradicts the use case (USE-3, USE-6).** When I rank a target's candidates I hold all of them. Normalising each descriptor within the target, as a z-score and a rank, is legitimate and standard. It changes the score a lot:

   | Model (3-fold grouped) | mean_group_pearsonr | CASP top-1 loss |
   |---|---|---|
   | Row only | 0.360 | 0.158 |
   | With group context | 0.522 | 0.118 |
   | Random pick | about 0 | 0.199 |

   The gain holds in all three folds (+0.150 to +0.165). Declaring `context="all_rows"` is the faithful setting. Methods that cannot use sibling rows are otherwise judged on a handicapped task. This is the curator's call, since it changes what the harness allows.

3. **Inputs I would always have that are missing (USE-6).**
   - **The server name and its model index**, both in `PDB-ID` (`CASP10_T0703_Mufold-MD_TS5.pdb`). They parse for 78% of CASP rows, across 173 servers. A server's TS1 sits at +0.183 within-target SD in GDT, against -0.135 for TS5. That index is the generator's own ranking, the kind of "own estimate" USE-6 keeps.
   - **The coordinates**, which would allow consensus (pairwise GDT between candidates).
   - **The target's full sequence length**, needed for coverage, since GDT_TS is normalised by the target length.
   - Claim 21 ("no new features") decides against adding these. That is defensible for a small historical task, but `fit_reason` should name the server index as a known, omitted input.

4. **Population (USE-8).** Classic decoy sets (ROSETTA, lattice, fisa, 4state, lmds, John2002, rosetta62) make up 60,760 of 95,094 rows (64%). They hold 103 groups (lattice median 1,803 rows per group) and are decoy-discrimination sets, not candidates someone would refine. The per-protein metric limits them to about 23% of the weight; pooled RMSE gave them most of it. The task is acceptable as long as `fit_reason` names the mix, which it does.

5. **The target is right for its era (USE-5).** GDT_TS is a number, and it was CASP7-10's measure of choice. Today's practice is lDDT or pLDDT, so the `Outdated` marker is correct.

**Metric: partly scores the decision (MET-1).**
- **What is right:**
  - The unit is right: the protein, as CASP scores QA per target.
  - It is immune to between-target offsets. Each protein's true mean scores -0.0015 on it, while that same mean beats LightGBM on pooled RMSE (0.134 vs 0.189). I reproduced those numbers as 0.1342 vs 0.1892.
  - The MET-5 exception and the `context` origin (MET-11) are justified.
- **What it misses:** the stated decision is "choose which to refine", a top-1 or top-k selection. Pearson scores the order of the whole candidate list, including the ordering among bad decoys.
- **What I would choose:** the mean per-target top-1 GDT_TS loss (best GDT_TS minus the GDT_TS of the top-ranked model), which is CASP11-14's selection measure. It needs a custom metric shipped under MET-13. On my runs it ranks the three models the same as Pearson (0.158 / 0.118 / 0.199 random vs 0.360 / 0.522 / 0). So Pearson is an adequate lower-variance proxy, and keeping it is defensible if the reason names top-1 loss as the decision measure.
- MET-6 to MET-9 do not apply: this is regression with no threshold or k fixed by the source.

**What a domain expert would change**
1. State the CASP10 convention break in the notes and `fit_reason`. Either drop CASP10 or keep it with a measured caveat; at minimum, record the 0.006 transfer number.
2. Declare `grouping.context="all_rows"` (curator's call).
3. Name the server and model index as a known omitted input.
4. Name top-1 GDT_TS loss in the metric reason as the decision measure that Pearson proxies.

**Sources**
- Rana et al. 2015, doi:10.1142/S0219720015500055
- [CASP14 EMA assessment (top-1 GDT-TS loss, per-target z-scores)](https://predictioncenter.org/casp14/doc/presentations/2020_12_03_EMA_Assessment_Seok.pdf)
- [CASP11/12 EMA assessments (identify the best models; consensus vs single-model)](https://escholarship.org/content/qt2mn4d5rz/qt2mn4d5rz.pdf?t=rzlcwf), [also](https://escholarship.org/content/qt6nb045d4/qt6nb045d4.pdf)
- [MULTICOM CASP10 QA, BMC Struct Biol 2014](https://bmcstructbiol.biomedcentral.com/articles/10.1186/1472-6807-14-13/tables/4)
- [CASP10 QA assessment (PMC3996498)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3996498): a captcha blocked it, so I used the definition's own CASP10 quote.

</details>

<details><summary>Blind review</summary>

**Verdict:** include with minor changes. The table matches the public RF-PCP source and the grouped split is honest. Across unseen proteins the signal is modest but real (R² about 0.2–0.28) and depends heavily on the model, so the task is hard and separates methods well. The changes needed are documentation, plus one check on the SS feature.

**What the task is.** You predict the GDT_TS quality of a computed 3D protein model, without knowing the native structure, from six features of the model: surface area, ED, energy, secondary-structure penalty (SS), sequence length (SL) and pair number (PN). This is model quality assessment. It is a real use: you choose or rank decoys before the true structure is known, as in the CASP QA category. The features are from 2014 and hand-crafted, and today pLDDT-style confidence scores have largely replaced them. That makes the task less relevant now, but it is still a real one.

**What I checked.** I downloaded `RF-PCP-DataSet.zip` from SourceForge and matched it row by row against `data.parquet` on Area, SS, SL, GDT and Energy. All 95,094 rows match a source row.
- The PubMed abstract says "95,091 modeled structures of 4896 native targets". The full source file has 99,987 rows.
- The preparer dropped all 4,478 `native_*.pdb` rows and 415 `CASPx_Txxxx_native.pdb` rows. All of them have GDT = 1. Dropping them is correct: a native structure is not a model.
- RMSD and TM-score are correctly left out. They are other measures of the same quantity and would leak the answer.
- `protein_id` was built by the preparer, and well. CASP targets are mapped to PDB ids, and superseded entries are merged: `lattice_ssfit_4icb` became `pdb:1ig5`, and `fisa_1hdd-C` became `pdb:1enh`. So the same protein seen through different decoy sets is held out together. The result is 445 groups (prefixes: pdb 93,601 rows, legacy 1,095, casp 398).
- There are no exact duplicate rows and no duplicate feature vectors.

**Concerns, most to least serious**

**1. The published random-split result is far from what the grouped task supports, and results depend strongly on the model.** Measured with grouped 3-fold CV:

| Setup | R² | RMSE | Median within-protein Spearman |
|---|---|---|---|
| Default LightGBM (500 trees, 63 leaves), grouped | −0.01 | 0.204 | 0.33 |
| Same model, random KFold | 0.81 | 0.089 | — |
| Regularised LightGBM on raw features, grouped | 0.18–0.23 | — | — |
| Ridge on log features, grouped | 0.15–0.20 | — | — |
| LightGBM on log/ratio features, grouped | 0.274–0.276 (3 random group assignments) | — | — |

- The paper's "R² … 0.84" for GDT_TS comes from K-fold CV over models. Since SL and PN are nearly constant within a protein (median 1 distinct value per group), they act as protein fingerprints, and a random split lets the model recognise proteins it has already seen.
- 56% of GDT variance lies between proteins.
- The grouped split is therefore the right one. I would keep it.
- Change: in the task notes, say that leaderboard numbers are not comparable to the paper's.

**2. Groups are very unequal in size.** The median group has 108 rows, the largest (`pdb:1ctf`) has 3,794, and the top 8 proteins hold about 18k rows. With 3 folds the fold sizes ranged from 25,192 to 39,462 rows. Scores were stable across my 3 group assignments (±0.002 for the best model), so this is acceptable. Optional change: cap the number of decoys per protein, or report a group-weighted metric.

**3. The decoy-generator mix sets the target distribution, and no column records it.** Rows come from ROSETTA (17k), lattice_ssfit (14k), fisa, 4state, lmds, John2002, rosetta62 and CASP5–10. The decoy set largely sets the GDT range for its proteins. Without a source column the model must infer the generator from the features. That is legitimate: at prediction time you would know which generator produced the model, so adding it as a categorical would be valid, though it would make the task more about the dataset than about physics. I would leave it out but mention it in the notes.

**4. Feature preparation.**
- In the source, ED = 0 in 71 rows and PN = 0 in 63 rows. The preparer turned these zeros into NaN, which is sensible since they look like failed computations. This should be documented.
- Energy is extremely heavy-tailed: the 99th percentile is 2.4e8, the maximum is 6.98e11, and 2,794 rows exceed 1e7. These are clashing or broken decoys.
- Default tree models overfit here. A sign-log transform helped (R² 0.18 to 0.27). I would keep the raw values, which is a fair test, but note the tail.
- Types are fine: SS and SL are int, PN is float because of the NaNs, and `protein_id` is a categorical used only for grouping. Make sure `protein_id` is excluded from the features.

**5. Possible leak through SS, which I could not verify.** The abstract says only "secondary structure penalty (SS)". If it compares the model's secondary structure to the native's DSSP, it uses information you would not have when making the prediction. If it compares to a sequence-based prediction such as PSIPRED, it is fine. The full text is paywalled (worldscientific returned 403), so I could not check. SS varies within a protein (up to 394 distinct values), so it is not a fingerprint. Change: confirm the definition before release.

**6. Overlap with an existing benchmark dataset.** The same author's UCI/OpenML "Physicochemical Properties of Protein Tertiary Structure" set (OpenML 42903, 45,730 CASP 5–9 decoys, target RMSD) shares the source decoys and some features: total area, ED, SS. This one differs in target (GDT), adds non-CASP decoy sets, and has a grouped split, so it is not a duplicate. It is a near-sibling, though, and should not sit in the same suite unless that is deliberate.

**7. A small gap in protein mapping.** 398 CASP6 rows kept a `casp:` id because they were not mapped to a PDB id. If any of those targets also appear under a `pdb:` id from another decoy set, the same protein would sit in two groups. With only 398 rows the risk is small, and I did not check it.

**What I could not check**
- The paper's full text, so the exact definitions of SS, ED and PN are unconfirmed.
- Whether the CASP-to-PDB mapping is right for every target.
- Whether the features were computed identically across decoy sets that use reduced (C-alpha-only) models.

Sources:
- [SourceForge RF-PCP files](https://sourceforge.net/projects/rf-pcp/files/)
- [PubMed 25524475 (Rana et al., JBCB 2015)](https://www.pubmed.gov/25524475/)
- [DOI 10.1142/S0219720015500055](https://doi.org/10.1142/S0219720015500055) (paywalled, 403)
- [OpenML 42903](https://api.openml.org/d/42903)

</details>

<details><summary>Task gamer</summary>

The task can be gamed moderately. Normalising each row against the other test rows that share its sequence length (SL) raises the score from 0.350 to 0.476, and a gap in the metric adds about 0.008 more. Neither works for a model that scores one new 3D model at a time.

All numbers are mean_group_pearsonr: the mean over the 9 shipped splits, with the per-split range in brackets.

- **Untuned LightGBM baseline:** 0.350 [0.318–0.396].
- **Random-column noise check:** adding a column of random numbers moves the mean by +0.0003 to +0.0005, and single splits by up to ±0.006.
- **Best honest model:** 0.420 [0.397–0.458]. It uses only row-level information:
  - size-ratio features: Area/SL, ED/SL², PN/SL, SS/SL, Energy/SL and a signed log of Energy;
  - a training target with each training protein's mean subtracted (training labels only);
  - the prediction ranked by SL first, with the model breaking ties (`SL*10 + p`).

  This is signal a deployed model has. LightGBM on its own does not learn that a shorter, truncated model of the same protein is worse: it scores 0.146 inside the 91 proteins whose SL varies, while SL alone scores 0.41 there.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Test-pool pseudo-groups: rebuild the protein from the SL value inside the test fold, then use within-group ranks and z-scores of every feature, SL / max SL and the group size | 0.350 baseline / 0.420 best honest | 0.476 [0.427–0.504] | +0.126 vs baseline (+0.11 to +0.15); +0.056 vs best honest (+0.03 to +0.08) | No. The prediction is made per model right after it is generated; group context is `none`. | Score each row independently, or in batches that mix proteins with the same SL. Alternatively, if a decoy pool is really available in use, declare group context and ship the pool. |
| 1b | Same, with the true protein_id (upper bound for #1) | 0.420 | 0.516 [0.496–0.544] | +0.096 | No | Same as #1 |
| 2 | Abstention: proteins whose prediction is constant are dropped from the mean. On top of #1, I output a constant in the half of the pseudo-groups with the lowest prediction spread. | 0.476 (#1) | 0.484 [0.446–0.515] | +0.008 (−0.009 to +0.018) | No, it is a metric artefact | Count a group with constant predictions as correlation 0, or drop a group only when its y_true is constant |
| 2b | Same flaw, no pool: predict raw SL. SL is constant in 354 of 445 proteins, so only the 91 proteins with truncated models are scored. | 0.350 baseline | 0.410 [0.327–0.482] | +0.060 vs baseline; −0.010 vs best honest | No | Same as #2. Under the fixed metric this rule scores 0.084. |

**#1, test-pool pseudo-groups.** The metric correlates predictions within each protein, so what helps is a feature's position relative to the other models of the same protein. SL nearly identifies a protein inside a test fold: about 148 proteins and 435 distinct SL values overall. Grouping the test rows by SL and ranking or z-scoring Area, ED, Energy, SS and PN within those groups gives 0.476. The true groups give 0.516, so the SL reconstruction recovers most of that upside. Merging rare SL values (truncated models) into the next larger SL cluster did not help (0.474). Adding the SL tie-break on top lowers the score (0.465). The mildest fix is to predict test rows one at a time, or in batches stratified so that a batch never holds most of one protein's models. Giving the true target length as a feature would make the honest model stronger and would not leak anything.

**#2, abstention.** In `_mean_group_pearsonr`, groups with zero prediction variance are removed from the mean (`corr = corr[var > 0]`). A participant can therefore choose which proteins get scored. Predicting raw SL scores only the 30 of about 148 test proteins per split where SL varies. That reaches 0.410, but it would fall to 0.084 if constant-prediction groups counted as 0. The gain here is small because the honest model is not much weaker on the dropped proteins. A better guess at which proteins are hard would enlarge it.

**Flaws that hurt an honest model**

None of the training-row choices I tried beats the honest model. Each line gives the plain model, then the model with the SL tie-break.

| Choice | Score | With SL tie-break |
|---|---|---|
| Honest model, all training rows | 0.378 | 0.420 |
| Drop the 10 rows with GDT = 1 | 0.379 | 0.421 |
| Weight rows by 1/√(protein size) | 0.377 | 0.418 |
| Weight rows by 1/(protein size) | 0.375 | 0.417 |

Of the 10 rows with GDT = 1, two are native structures (RMSD 0) that the preparation left in, and eight are Rosetta decoys. Dropping them changes nothing measurable.

The real weakness is a framing issue, not a training-row issue. The kit lacks two things a deployed model would know:
- **The target sequence length.** Group max SL stands in for it, but only through the test pool.
- **The decoy generator** (CASP server, ROSETTA, lattice, fisa, lmds, …). It is in the source file names. 22 proteins mix several decoy sets, and inside those proteins the decoy set explains a median 41% of the GDT variance (R²).

Neither is an exploit. Shipping them would be fair and would narrow the gap to #1.

**Comparison with the published file**

Matching rows against the published file works: all 95,094 kit rows match `RF-PCP-Full-dataset.csv` on Area, SS, SL and GDT. The file has 99,987 rows. The preparation:
- dropped RMSD and TM, which are computed against the reference structure, so dropping them is correct;
- dropped 4,893 rows with GDT = 1, mostly the `native_*` files, and left 10 such rows in;
- turned ED = 0 (71 rows) and PN = 0 (63 rows) into missing values;
- dropped the decoy-set name;
- merged decoy sets of the same PDB code into one `protein_id`.

**Attacks that found nothing**

- **Formats.** Every float carries at most 6 significant digits. Format-only features (decimals, significant digits, last digit, missing flags) score 0.091, which is only the magnitude effect. The within-protein correlation of GDT with the number of Energy decimals is −0.003. Adding format features to the ratio model gives 0.3736 against 0.3719, which is within noise. Rows with missing ED or PN have a GDT mean of 0.41 and 0.38, against 0.395 overall.
- **Order and ids.** Rows are shuffled: only 0.9% of consecutive rows share a protein, and the within-protein correlation of GDT with row position is 0.007. The id prefixes (pdb, legacy, casp) are held out by group, and the group column is not a feature.
- **Copies across the split.** No Area|ED|Energy triple is shared by two proteins. Using the mean label of the 5 nearest training rows as the prediction scores 0.20–0.25, below the baseline. The legacy and casp proteins do not duplicate any pdb protein.
- **Columns from after the prediction point.** None remain. Every feature taken alone scores |r| ≤ 0.32 except SL (0.41, which is the abstention effect in #2b). Energy outliers up to 7e11 are clashes, which is real signal.
- **Transforms over all rows.** None found: the values are raw and unscaled.
- **Training rows.** See the table above; nothing beat the honest model.

**What I could not check**

- I did not run a classifier separating train from test rows; the groups are randomly assigned.
- I did not search for decoy-generator signatures recoverable from the features alone, beyond the format test.
- I did not tune any model. The size of #1 against a strongly tuned honest model is open.
- The RF-PCP paper was not opened, only its search abstract and the dataset. I found no competition forums or leak threads for this dataset.

Sources: [RF-PCP files (SourceForge)](https://sourceforge.net/projects/rf-pcp/files/), [Quality assessment of modeled protein structure using physicochemical properties (PubMed)](https://www.pubmed.gov/25524475/), [RFMQA (PMC4164442)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4164442/), [MASS (PMC7336608)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7336608/)

</details>

<details><summary>Precedent check</summary>

**Precedent check: `protein_model_quality_rf_pcp` (second pass, 2026-11-04)**

**Answer to focus.md.** focus.md asks no question. It points to the metric exception and its numbers, the ED/PN rule, the native-row exclusion, the two perfect-label rows and the protein key/alias grouping. Against precedent, every one of the 2026-11-04 decisions is either consistent or departs with a stated, reasonable reason. I found no departure without a reason and nothing that breaks a higher Must. One pair of similar cases was decided differently: the `Outdated` keep here against `first_order_theorem_proving` (`No` on `Outdated`). That conflict is already under an open consistency check, and this case leans it towards keep. A new tension (SEL-9) is not written down yet. The TP-3 answer still rests on RMSE, which is no longer the declared metric.

**1. Exception to MET-5 (2026-11-04, Lennart): `mean_group_pearsonr` on `protein_id`. Departs with a stated reason, reasonable**

- **Strength:** MET-5 is a Should. The stated fact is that the use case orders candidates within one protein, and pooled RMSE rewards each protein's typical quality. The principle served is P6, through MET-1 (a Must). The higher Must is served, not broken.
- **Precedents:**
  - `numerai_v5_2_1m`: the same metric per era (MET-4, applied 2026-10-21). The evidence was that RMSE rewards shrinkage on a low-signal target.
  - `huesken_sirna_efficacy`: the same exception the same day (2026-11-04, Lennart). Same reason: knowing the per-gene mean cuts RMSE from 0.1582 to 0.1378.
  - `sat11_hand_algo_runtime`: a within-group decision scored within the group (source `par_k`, `select_min`).
  - All three follow "score the decision at the unit the actor acts on".
- **Register flag `exception_to_must MET-1`:** a false positive, and it fires on huesken too. The exception is to MET-5; MET-1 is only named in "Serves P6 (MET-1)". No action needed beyond the parser.
- **Rule of three:** this is the first of two exceptions with the same reason (huesken is the second, per CHANGELOG and the metrics.md Cases table). No amendment is due yet. The next grouped regression whose decision ranks within a group makes the third, and then a MET-5 amendment is due.
- **Re-measured on the shipped 3x3 splits** (my run, untuned models):

  | | Ridge | LightGBM | Per-protein true mean (oracle) |
  |---|---|---|---|
  | Pooled RMSE | 0.1871 | 0.1865 | 0.1343 |
  | Per-protein Pearson | 0.294 | 0.355 | – |

  - The oracle's 0.134 reproduces the record's figure. My LightGBM RMSE (0.1865) is close to the record's 0.188 but not identical, because my hyperparameters differ.
  - Under RMSE, ridge wins 4 of 9 splits. Under the declared metric, LightGBM wins 9 of 9. The library scorer equals my implementation.
- **Gap against the huesken precedent:**
  - Huesken's exception recorded that both metrics pick the same model family.
  - Here the record and `curation_comments` still answer TP-3's `no_spread` with the RMSE comparison (7.37%, 0.19318568 vs 0.17894541).
  - Precedent: `african_credit_scoring_challenge` was judged by the declared metric, not the dropped one (task_probes Cases).
  - Under the declared metric the spread is clear (+0.061, 9/9 splits). The TP-3 answer could cite that instead.

**2. SEL-9 (Must, P2) against a within-group metric: consistent by an evident fact, not written down**

- **The tension:** the use case now reads "ranks the candidate models ... scored by the correlation per protein". SEL-9 excludes ranking tasks "also when a mirror serves them as ... regression". Precedents: `microsoft_mslr`, `istella22` (AI 2026-10-31), `yahoo_learning_to_rank_challenge_data`, all `No`.
- **The evident distinguishing facts:**
  - GDT_TS is an absolute measured quantity.
  - The source's task is regression (SEL-8).
  - Learning-to-rank relevance grades exist only per query.
- `numerai_v5_2_1m`, `huesken_sirna_efficacy` and this dataset now form a pattern: a regression scored within groups is not a SEL-9 ranking task. No record and no Tensions row says so. principles.md asks that "a new decision on a tension not listed becomes a row". Suggested row: "a measured target scored per group against SEL-9 ranking; the source's regression target decides".

**3. `Outdated` set, kept `Yes` priority 2 (2026-11-04): follows the majority; one opposite precedent is open**

- **Follows:**
  - `heart_disease` (Yes, priority 2)
  - `covertype`, `video_transcoding_time_prediction`, `horse_colic_survival`, `south_africa_coronary_heart_disease` (all Yes)
  - selection.md gives `Outdated` no rule. The open check calls keeping such datasets "the precedents".
- **Opposite:** `first_order_theorem_proving` is `No` on `Outdated` alone (Lennart, 2026-07-27). It has an open **Consistency check (AI, 2026-10-19)** against its ASlib siblings. The facts are similar: a dated generator or solver portfolio, and a field that has moved to other models. This is the same curator four months apart; the open check already records that drift.
- **Marker choice:** `Not Representative` is defined as "features practitioners no longer use for the task". That fits the pLDDT note too. `audiology_diagnosis`, `credit_approval` and `body_density_prediction` carry both markers. Minor, but worth a deliberate choice.

**4. SEL-12 "not a SMILES case" (2026-11-04): consistent**

- **Follows `ecoli_proteins`** (Yes): hand-made biological descriptors kept, even though sequence models dominate the field.
- **Differs from `peer_tem1_beta_lactamase_esm2` and `deeploc2_fungi_membrane_esm2`** (No, SEL-12). Their inputs are learned embeddings (CLEAN-6), and PEER shows sequence models clearly better (0.839 vs 0.528).
- **Differs from `huesken_sirna_efficacy`**, tagged `Revisit later` for SEL-12 the same day. Huesken ships the sequence itself (one-hot); this dataset ships no structure. That is evident, not written.
- **Weak point:** SEL-12 is "judged per dataset" by whether modality models are clearly better. The record cites pLDDT as the modern standard but no comparison. Naming `ecoli_proteins` as the precedent would close it.

**5. CLEAN-11: ED = 0 with PN > 0 (71 rows) and PN = 0 with ED > 0 (63 rows) set missing, rows stay (2026-11-04). Consistent**

- **Follows** the CLEAN-11 Cases: `caracas_cervical_cancer` (logically inconsistent pairs set missing), `heart_disease` (`chol == 0`), `churn_telco_south_asia` and `mortgage` (2026-10-22).
- **Set apart from `clock_protein_toxicity`** (2026-11-01, exception, rows dropped). There, 62-68 descriptors per molecule had failed. Here one descriptor per row is wrong, and each such row has a positive sibling of the same protein and length.
- **Overrides Myunghwan's 2026-10-29 "preserve those values".** A newer curator decision wins; this is a different curator, so not drift.

**6. `Energy` kept as supplied (2026-11-04): consistent**

CLEAN-11 says "values that are only unusual stay". The fact is written: the values are continuous with the rest and carry signal (mean GDT_TS 0.339 vs 0.398). This differs from `mortgage`, where the values were impossible (LTV above 300%).

**7. Native-row exclusion by identity, two perfect-label rows kept (Myunghwan 2026-10-29, accepted). Consistent**

- The exclusion matches CLEAN-11's "a row leaves only when it is no task row" (USE-7): a reference structure is not a candidate.
- It filters by identity, not by label, which matches "do not filter on labels".
- No rule ID is cited for the exclusion. Adding USE-7 or CLEAN-11 would make it register-visible.

**8. Split: canonical protein held out, no sequence family. Consistent**

- **Follows:**
  - `sat11_hand_algo_runtime` (Lennart 2026-10-06: instances, not families, on purpose)
  - `huesken_sirna_efficacy` (genes)
- **Not departed from:** SPLIT-31's scaffold clause, which covers small molecules with structures, not proteins.
- Unlike sat11, the record gives no reason why a family split is unneeded; it only says "not claimed". This is optional to add.

**9. Year 2014 = first release (August 2014 archive): consistent with PROV-9**

**10. Stale text (not a precedent issue)**

- The record's 2026-10-29 Assessment still says "regression RMSE is the fallback" and "Preserve those values" (ED/PN). Both were superseded on 2026-11-04 but are not marked as such.
- `curation_comments` bullet 3 and record claims 11 and 32 still frame qualification on RMSE.

**Reflection prompt (one; the only pair of similar cases decided differently)**

```text
**Consistency check (AI, 2026-11-04):** your call on protein_model_quality_rf_pcp (keep `Yes`, priority 2, with
`Outdated`: six global descriptors of 2002-2012 server models, the field now on pLDDT) differs from
first_order_theorem_proving (`No` on `Outdated` alone, 2026-07-27: a dated algorithm-selection benchmark; open
check of 2026-10-19). What sets this one apart?
(a) the grouped biology regime is thin in the collection and the descriptors are a real, documented measurement
set, while first_order adds no gap, recorded as the fact; (b) treat protein_model_quality_rf_pcp like
first_order_theorem_proving; (c) reopen first_order_theorem_proving to match (keep, as its ASlib siblings); (d)
give `Outdated` a rule (an amendment).
```

</details>

<details><summary>Advocate</summary>

**Opening brief for shipping `protein_model_quality_rf_pcp`**

Verdict I argue for: ship after small changes. None of the problems the panel found breaks a Must that the definition, the library or a note cannot fix. Each one has a remedy below the bottom rung of the remedy ladder (exclusion).

**1. The validity core holds: real use case, honest split, faithful data (P3, P4, P5, all Must).**
- **Evidence for the data:**
  - The blind reviewer matched all 95,094 rows to the author's `RF-PCP-Full-dataset.csv`.
  - RMSD and TM are dropped. Alone they give R² 0.84 and 0.87, so keeping them would leak the target (LEAK-10).
  - The column auditor found no post-outcome column and no missingness caused by the outcome.
- **Evidence for the split:**
  - No group is on both sides in any of the 9 splits, and no row has an exact copy of its six features.
  - The alias map is hash-checked: 453 source keys become 445 groups.
  - The split auditor's (SL, PN) signature check found no missed alias. The 4 colliding pairs are unrelated proteins.
  - Grouping matters even under the declared metric: LightGBM scores 0.511 on IID folds against 0.366 grouped.
  - Forward windows by CASP edition match the grouped folds within 0.03 through CASP9, so SPLIT-19 needs no temporal split.
- **Rules:** USE-10 and SPLIT-2 (a new target is a cold start), SPLIT-24 (a true group id), PROV-7. The UCI sibling `physiochemical_protein` is already retired, so OpenML 42903 is no duplicate in the suite.
- **What I concede (EV-7):** nobody re-opened the paper's Sections 2.2 and 2.3, so the blind reviewer's SS question ("PSIPRED, not native DSSP") rests on the record's reading. SS varies within a protein (394 values), so it is no fingerprint. Remedy: confirm it from the paper, without changing the data.

**2. The declared metric is the right one and separates models. The abstention hole is real but is a library bug.**
- **Why the metric is right:**
  - The oracle per-protein mean wins pooled RMSE 0.134 against 0.187, and it wins in 9 of 9 folds. RMSE scores the wrong decision (MET-1, Must).
  - On `mean_group_pearsonr`, LightGBM scores 0.355 and ridge 0.294. LightGBM is higher in 9 of 9 folds. Gaussian noise scores 0.0007 and a constant scores 0.000.
  - Each fold holds 148-149 groups, with at least 13 candidates per group, so every fold is scorable (MET-2).
  - The exception to MET-5 has a stated fact and two precedents: `huesken_sirna_efficacy` and `numerai_v5_2_1m`.
- **What I concede:** the claim auditor showed that an exact constant on the least certain proteins lifts the score to 0.428 or 0.492 (MET-2, MET-13, Must).
- **Why it does not outrank shipping:**
  - The flaw is in `_mean_group_pearsonr` (`corr = corr[var > 0]`), shared with huesken and numerai.
  - It is an independent failure, not a conflict, and the remedy ladder fixes it in the code. A group whose target varies but whose predictions do not should score 0. Add tests with the constants 0.3 and 0.5.
  - Then re-state the Metric text. Nothing in this `dataset.py` changes.

**3. The 1,011 rosetta62 `_rn<pdb>.out.N` rows: I concede, and fixing the definition keeps the dataset (P3/USE-7, treat like cases alike).**
- **Evidence:**
  - Median GDT is 0.961.
  - The best-GDT row is an `rn` row in 55 of 56 proteins.
  - These rows inflate within-protein correlations, for example Area from -0.335 to -0.558.
- **Remedy:** these rows have the same status as the 4,893 natives already excluded by identity. If the Baker archive confirms that "rn" means relaxed native, add the filename pattern to `is_reference`. That leaves 94,083 rows, and every rosetta62 group keeps its BOINC decoys (6,125 rows), so no group is lost. If it stays unconfirmed, the mildest remedy is a named note, as for the two perfect-label IDs.
- This is fixing the definition, two rungs above exclusion.

**4. The CASP10 descriptor break is a documentation fix, not a P5 failure.**
- **Evidence:**
  - SL varies within 67 of 67 CASP10 targets and within 0% of CASP6-9 targets.
  - A model trained without CASP10 scores 0.006-0.016 on it.
- **Why it is not a P5 failure:** the values are the author's own release, matched row by row. What is wrong is our `known` text, which calls SL "sequence length" for every row.
- **Rule:** the tension "the right split against the score" (P4 over P6, SPLIT-4). A hard 15% of the groups lowers every model's mean and does not make the split or the data dishonest.
- **Remedy:**
  - Correct the SL wording.
  - Add the source's CASP10 hold-out and the forward-window numbers to `splits_comment`.
  - Name the break in `fit_reason`. The fit is already `approximate` (USE-8).
  - Dropping CASP10 stays the curator's call. It is not needed for validity.

**5. Declare `grouping.context="all_rows"`: a one-field fix that serves two Musts and removes the task gamer's main exploit.**
- **Evidence:**
  - The actor gets all server models of a target at once (CASP stage 1 has about 20, stage 2 about 150).
  - With target context, the practitioner's grouped score goes from 0.360 to 0.522 (+0.150 to +0.165 in all 3 folds), and CASP top-1 loss improves from 0.158 to 0.118.
  - The task gamer's #1 (+0.126 from pseudo-groups built on SL) is an exploit only because `context="none"` forbids what the actor really has.
- **Rules:** USE-6 (Must) makes anything known at the prediction point a legitimate input. SPLIT-23 (Must) says the use case decides what is known about a new group.
- **Why this keeps Lennart's decision:** it adds no column, so his "no new features" line stands. The choice is the curator's.

**6. The stale or loose text is quality work and has fixes ready (EV-6, EV-8, USE-1 Weigh, P7).**
- **TP-3:** restate `no_spread` on the declared metric: +0.061, 9 of 9 folds. The 5-fold RMSE figures (7.37%) are stale; mark them historical.
- **Claim 15:** change "each such row has a same-length sibling" to "132 of 134".
- **Use case:** change "to choose which to refine" to "rank the candidates". Name top-1 GDT_TS loss in the metric reason as the decision measure Pearson stands in for. Both rank the practitioner's three models the same way: 0.360 / 0.522 / 0 on Pearson against 0.158 / 0.118 / 0.199 on top-1 loss.
- **Mixed collections:** add one sentence. Merged proteins that span several decoy collections are worth about +0.01 on the fold mean.
- **Record:** mark the 2026-10-29 lines superseded ("RMSE fallback", "preserve those values").
- Under step 3 of "How to decide", a real task carries these when they are written down.

**7. The precedents favour keeping (Weigh, P2).**
- **`Outdated` keep:** follows `heart_disease`, `covertype` and `horse_colic_survival`. The opposite case, `first_order_theorem_proving`, already has an open consistency check that leans toward keep.
- **SEL-12:** follows `ecoli_proteins` (hand-made biological descriptors). It is set apart from `peer_tem1_beta_lactamase_esm2`, whose inputs are learned embeddings.
- **SEL-9 (Must):** not breached. GDT_TS is a measured, absolute target and the source's task is regression (SEL-8), as with huesken and numerai. Remedy: add that as a row to principles.md's Tensions table.
- **Factors:** grouped biology is thin in the collection (+); 95k rows and 445 groups (+); a hash-checked, traceable source (+); historical descriptors (-).

</details>

<details><summary>Critic</summary>

**Opposing brief: `protein_model_quality_rf_pcp`. It should not ship as defined. It can ship after the changes below.**

Judgment record:
- **Verdict:** ship after changes. No point needs exclusion.
- **Validity:** USE-7 and the native exclusion are open (point 1). SPLIT-23 and USE-6 are triggered by `context="none"` (point 2). P5 and USE-8 are triggered by CASP10 (point 3).
- **Value:** MET-2 and MET-13 are triggered by the abstention edge case (point 4). MET-1 holds as a proxy (point 5).
- **Quality:** EV-8 and EV-6 are triggered by stale and overstated claims (point 6).

**1. About 1,011 probable relaxed-native rows are kept while 4,893 natives are excluded (P3/P4, USE-7 Must; treat like cases alike)**
- **Problem:**
  - `_clean` excludes reference structures only by the `native_` prefix or the `_native.pdb` suffix.
  - The rosetta62 family `rosetta62_<pdb>_rn<pdb>.out.N.pdb` (15-20 rows in each of its 56 proteins) looks like the reference structure refined:
    - RMSD 0.44-2.82 Å (median 0.82) and GDT median 0.961;
    - the best-GDT row in 55 of 56 proteins;
    - 8 of the 10 rows with GDT = 1.0.
  - No other decoy set looks like this. lattice, fisa, John2002 and lmds have 0 rows above GDT 0.9.
- **Effect:** these candidates cannot exist before the reference does. In 56 of 445 groups they inflate the within-protein signal (column-auditor):

  | descriptor | Pearson with `rn` rows | without |
  |---|---|---|
  | Area | -0.558 | -0.335 |
  | SS | -0.394 | -0.165 |

- **Evidence:** the column auditor's measurements. What "rn" means is not confirmed; the Zenodo 48780 record is silent.
- **Remedy (fix the definition, conditional):**
  - Check the Baker 62-protein archive's docs.
  - If "rn" means relaxed native, add the pattern to the identity exclusion. That gives 94,083 rows; update task_summary.row and the counts.
  - If it stays unverified, name the rows in a bullet, as the comments already do for the two perfect-label IDs.

**2. `grouping.context="none"` contradicts the use case and cannot be enforced (P4, SPLIT-23 Must, USE-6 Must)**
- **Problem:** the use case is "ranks the candidate models generated for one protein". CASP releases all of a target's server models at once, so the actor holds the whole pool. The definition declares that the pool is not known.
- **Effect, two ways:**
  - **Honest models lose signal.** Domain practitioner, 3-fold grouped: row-only 0.360, with group context 0.522 (+0.150 to +0.165 in every fold). Top-1 loss improves from 0.158 to 0.118.
  - **The harness cannot stop the move anyway.** The task-gamer rebuilds proteins from SL inside the test fold and reaches 0.476 against a 0.350 baseline (+0.11 to +0.15 per split), with 0.516 as the upper bound using the true group. So declaring "none" rewards whoever breaks it.
- **Rule:** SPLIT-23 says the cited use case decides what is known about a new group. USE-6 makes anything known at the prediction point a legitimate input.
- **Remedy (fix the definition):** declare `context="all_rows"`. This is not a new feature, so it does not conflict with Lennart's "no new features" line. If the curator keeps "none", `fit_reason` must state the 0.476 exploit as a known gap.

**3. CASP10 descriptors follow another convention, and the `known` text misstates SL (P5 "the data is what it claims to be"; USE-3 and USE-8 Must)**
- **Evidence (split auditor and domain practitioner):**
  - SL varies within the protein in 67 of 67 CASP10 targets, against 0% in CASP6-9 and 5% in CASP5.
  - Area's within-target sign flips: -0.18 to -0.42 in CASP5-9, +0.07 to +0.24 in CASP10.
  - Trained on the earlier rounds and tested on CASP10, models score 0.006-0.033. On the shipped folds CASP10 scores 0.048, while ranking by raw SL gives 0.501.
  - 2,259 CASP10 rows are not in the paper's validation file.
- **Effect:**
  - 15% of the scored groups (67 of 445) are close to unlearnable from the inputs.
  - In CASP10, SL measures the candidate's coverage, not the target's length, yet `known` calls it "sequence length" for every row.
  - "Unresolved descriptor conventions" in `fit_reason` understates this.
- **Remedy (a note, plus a curator call):** correct the SL wording in `known` and the comments. Add the CASP10 break and the forward-window numbers to `splits_comment` and `fit_reason` (CASP8 0.340, CASP9 0.483, CASP10 0.016). The curator decides whether CASP10 stays. There is no re-split: through CASP9 there is no drift.

**4. The metric lets a model skip proteins: a group with constant predictions drops out of the mean (P6, MET-2 Must, MET-13 Must)**
- **Problem:** `metrics.py:775` keeps only groups with `var > 0`, so a protein where the model predicts one constant value is left out of the score.
- **Effect (claim auditor, 9 of 9 folds):**
  - Predicting an exact constant 0.5 on the 50% of proteins with the least predicted spread lifts LightGBM from 0.355 to 0.428; on 75% it gives 0.492. No labels are needed.
  - The result depends on float rounding: the constant 0.3 is not exact after centring, so those groups are scored about 0, giving 0.220.
  - Predicting raw SL scores only the 91 proteins whose SL varies: 0.410, against 0.084 if those groups counted.
- **Rule:** MET-13 says a metric undefined at the edge of its domain gets a score rather than none. The use case scores every protein.
- **Remedy (repair in the library):**
  - A group whose target varies but whose predictions do not, exactly or within a relative tolerance, scores 0.
  - Drop a group only when its target is constant (no such group here).
  - Add tests with the constants 0.3 and 0.5, and re-state the Metric text.
  - The same code path serves `huesken_sirna_efficacy` and `numerai_v5_2_1m`.

**5. The use case names a top-1 decision that the metric does not score (MET-1 Must, here a note)**
- **Problem:** "to choose which to refine" is a top-1 selection, and CASP11-14 score it by top-1 GDT_TS loss. Pearson scores the order of the whole candidate list. The record itself disclaims top-1 usefulness.
- **Evidence:** the domain practitioner found that top-1 loss and Pearson rank the three models the same way. So Pearson is an adequate proxy, and I do not ask for a new metric.
- **Remedy (a note):** reword the use case to "rank the candidates", or name top-1 loss in the metric reason as the decision that Pearson stands in for.

**6. Stale and overstated claims (EV-8 Should, EV-6)**
- **Stale:** `curation_comments` bullet 3 (Ridge 0.19318568 against LightGBM 0.17894541, 7.37%) argues TP-3 on RMSE, which is no longer the metric, and its 5-fold frames are not in the folder. The record's 2026-10-29 Assessment ("RMSE is the fallback", "Preserve those values") is superseded but not marked.
- **Overstated:** "Each of those rows has a same-protein, same-length sibling" is false for 2 of 134 rows: `CASP10_T0692_FALCON-TOPO_TS5.pdb` and `CASP10_T0716_sysimm_TS4.pdb`.
- **Remedy (fix the text):**
  - Restate TP-3 on the declared metric: LightGBM 0.355 against ridge 0.294, LightGBM higher in 9 of 9 splits. This follows the `african_credit_scoring_challenge` precedent.
  - Write "132 of 134".
  - Mark the old Assessment lines as superseded.

**7. Omitted known inputs and an unrecorded tension (USE-8 Must for stating the fit; principles.md "Tensions")**
- **Omitted inputs** that the actor has and `fit_reason` does not name:
  - the server and its own model index in `PDB-ID` (TS1 sits at +0.183 within-target SD in GDT, against -0.135 for TS5);
  - the decoy generator (in the 22 proteins that mix decoy sets, it explains a median 41% of within-protein GDT variance);
  - the target's full length.
- **Mixed collections:** in 19 merged groups (26% of rows), the per-protein correlation partly rewards telling decoy collections apart (about +0.01 on the fold mean).
- **Unrecorded tension:** the call that a measured regression target scored within groups is not a SEL-9 ranking task (numerai, huesken, this dataset) has no Tensions row.
- **Remedy (notes):**
  - one sentence in `fit_reason` naming the omitted inputs and the collection mix;
  - a Tensions row for SEL-9 against a within-group metric;
  - answer the open `Outdated` consistency check against `first_order_theorem_proving` (the precedent-checker's prompt).

**Not argued.** The grouped split and the alias map hold: 0 shared groups, 445 groups, the hash is checked. Dropping RMSD and TM is correct. The ED/PN missing rule and keeping Energy are consistent with CLEAN-11 precedent. I do not count those quality calls against shipping.

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal for shipping `protein_model_quality_rf_pcp`**

The critic and I give the same verdict: ship after changes, and no point needs exclusion. The critic disputes none of my validity evidence. Its "Not argued" section accepts the grouped split, the alias map, the RMSD/TM drop and the ED/PN and Energy calls. So this rebuttal is about rank and remedy, not about whether the dataset stays. I checked two facts again:
- `metrics.py:775` reads `corr = corr[var > 0]`.
- The schema allows `context="all_rows"` ("all rows" of the group; `schema.py:133`). `dataset.py:159` now declares `"none"`.

**Critic 1: about 1,011 `rn` rows kept while the natives are excluded. Conceded.**
- The evidence is strong:
  - median GDT 0.961;
  - the best-GDT row is an `rn` row in 55 of 56 proteins;
  - 8 of the 10 rows with GDT = 1.0;
  - none of the other decoy sets has rows like these.
- Treating like cases alike (USE-7, CLEAN-11's "a row leaves only when it is no task row") means these rows go if "rn" means relaxed native.
- **What follows:** the remedy is the critic's and mine. Add an identity rule in `_clean`, giving 94,083 rows. Every rosetta62 group keeps its 6,125 BOINC decoys, so the group count stays at 445. If "rn" stays unconfirmed, name the rows in a bullet.
- One limit on the effect: the task gamer found that dropping the 10 GDT = 1 training rows moved the honest model by +0.001. The effect on scoring is real (Area -0.558 against -0.335 inside 56 groups). But it is not a leak an honest model exploits, so it ranks as fixing the definition, not as a P3 failure that blocks shipping.

**Critic 2: `context="none"` contradicts the use case. Conceded, and it strengthens my point 5.**
- SPLIT-23 (Must) lets the cited use case decide what is known about a new group. USE-6 (Must) makes the whole released candidate pool a legitimate input.
- Two numbers show this:
  - the 0.476 SL pseudo-group "exploit" against 0.516 with the true groups;
  - the practitioner's +0.150 to +0.165 in all 3 folds.
- Under "none" the benchmark rewards whoever breaks the declared rule, and the harness cannot enforce it.
- **What follows:** change the one field to `all_rows`. This adds no column, so Lennart's "no new features" line stands. If the curator keeps "none", the critic's fallback is right: name the 0.476 gap in `fit_reason`.

**Critic 3: CASP10 convention break, framed as a P5 trigger. The facts and the remedy are conceded. The P5 label is disputed.**
- **Conceded:**
  - SL varies within 67 of 67 CASP10 targets against 0% in CASP6-9.
  - Area's sign flips.
  - Transfer scores are 0.006-0.033.
  - Our `known` text misstates SL.
  - "Unresolved descriptor conventions" understates the break.
  - The 2,259 CASP10 rows outside the paper's validation file belong in the notes (PROV).
- **Disputed:** P5 asks whether the data is what it claims to be. The values are the author's release, matched row by row (blind reviewer, task gamer: 95,094 of 95,094). What is wrong is our description of SL, and the fix for that is a note (EV-6), not a change to the data.
- The split is not at fault either. The split auditor found no drift through CASP9 (within 0.03), and a temporal split would only re-test the break on 67 groups.
- On "close to unlearnable": that holds for a per-row model under `context="none"`. Within-target ranking by SL alone gives 0.501 on CASP10, and that signal needs the group context the critic's point 2 grants.
  - Nobody has measured a context model on CASP10 within the shipped folds. The practitioner's -0.059 is a transfer with no CASP10 targets in training. So I do not claim that `all_rows` fixes CASP10. I claim only that the label "unlearnable" is not established under the corrected definition.
  - Recommended check before the curator's keep/drop call: score a context model on the CASP10 groups of the shipped folds.
- **What follows:**
  - Fix the SL wording.
  - Add the forward-window numbers (CASP8 0.340, CASP9 0.483, CASP10 0.016) to `splits_comment` and `fit_reason`.
  - Keeping or dropping CASP10 is the curator's call (P4 over P6, SPLIT-4: a hard slice lowers every mean and does not make the split dishonest).

**Critic 4: the abstention hole in the metric. Conceded as a Must (MET-2, MET-13). Disputed only as a reason to change this dataset.**
- The numbers are not in dispute:
  - 0.355 rises to 0.428 when half the proteins are abstained, and to 0.492 at 75%;
  - the result depends on float rounding (0.5 drops the groups, 0.3 scores them at about 0 and gives 0.220).
- The flaw is in `_mean_group_pearsonr`, which `huesken_sirna_efficacy` and `numerai_v5_2_1m` share. It is an independent failure, not a conflict: it says nothing against this dataset's use case, split or data. The critic itself puts the repair in the library.
- **What follows, and I add a precondition:**
  - The library fix must land before this dataset ships. A Must hole live on the leaderboard is not acceptable just because it is shared.
  - The fix: a group whose target varies but whose predictions do not scores 0. Add tests with the constants 0.3 and 0.5, then re-state the Metric text.
  - With the fix, raw SL scores 0.084 instead of 0.410, so the hole closes. Nothing in `dataset.py` changes.

**Critic 5: the use case names a top-1 decision that the metric does not score. Agreed. The critic already grants that Pearson is a sound stand-in.**
- Both measures rank the three models the same way: 0.360 / 0.522 / 0 against 0.158 / 0.118 / 0.199 top-1 loss. MET-1 holds.
- **What follows:** reword the use case to "rank the candidates" and name top-1 GDT_TS loss in the metric reason.

**Critic 6: stale and overstated claims. Conceded in full (EV-8 Should, EV-6).**
- Restate TP-3 on the declared metric: LightGBM 0.355 against ridge 0.294, LightGBM higher in 9 of 9 splits (the `african_credit_scoring_challenge` precedent).
- Mark the 7.37% RMSE figures as historical.
- Write "132 of 134". The two exceptions still have same-protein siblings with a positive PN, so the CLEAN-11 decision stands.
- Mark the 2026-10-29 Assessment lines as superseded.

**Critic 7: omitted inputs and an unrecorded tension. Conceded as notes. Disputed only where it would reopen "no new features".**
- **One sentence in `fit_reason` (USE-8)** naming:
  - the server and its TS index (+0.183 against -0.135 within-target SD);
  - the decoy generator (a median 41% of within-protein GDT variance in the 22 mixed proteins);
  - the target's full length;
  - the mix of collections (about +0.01 on the fold mean).
- **Disputed:** naming these inputs does not oblige us to ship them.
  - Lennart decided on 2026-11-04 to add no new features. The column auditor calls the decision covered and recommends no change.
  - USE-6 makes these inputs legitimate. It does not oblige the curator to ship every known input when `fit_reason` already says the fit is `approximate`.
- **Tensions row:** agreed. Add "a measured target scored per group against SEL-9 ranking; the source's regression target decides" (numerai, huesken, this dataset).
- **`Outdated` consistency check:** I answer option (a). The grouped-biology regime is thin in the collection, and the descriptors are a documented measurement set. `first_order_theorem_proving`'s own open check already leans towards keep.

**Net position**
- **Ship after:**
  1. the library fix for groups with constant predictions, with tests;
  2. `context="all_rows"`;
  3. the `rn` identity exclusion if confirmed, otherwise a named note;
  4. the CASP10 and SL corrections in `known`, `splits_comment` and `fit_reason`;
  5. the text fixes for TP-3, 132 of 134, the use-case wording, the omitted inputs and the superseded record lines;
  6. a Tensions row for SEL-9.
- **Curator's calls:** keep or drop CASP10, and confirm "rn".
- **Still open (EV-7):** the paper's definition of SS (PSIPRED or DSSP). Confirm it from Sections 2.2 and 2.3. If it is DSSP of the native, that becomes a leak question (LEAK-10), and it would outrank everything above.

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal: `protein_model_quality_rf_pcp`**

The advocate and I agree on the verdict: ship after changes, with no exclusion. We differ on one thing. The advocate lists the metric repair, the `rn` resolution and the CASP10 text as small changes that sit beside shipping. I hold that they come before it, because each one is an open Must.

**A1. The validity core holds (P3, P4, P5). Conceded in part.**
- **Conceded:**
  - Every row matches the author's file (95,094 rows).
  - Dropping RMSD and TM under LEAK-10 is correct.
  - No group is shared across the 9 splits, and the alias map is hash-checked.
  - The SL/PN signature check found no missed alias.
  - The grouped split decides the score (LightGBM 0.511 on IID folds against 0.366 grouped).
  - I accept the SS confirmation under EV-7 as a note.
- **Disputed:** "the validity core holds" cannot stand while the advocate's own point 3 is open. USE-7 (Must) asks whether the population contains rows made after the reference. With 1,011 probable relaxed natives in 56 of 445 groups, that question is not settled. It is the only validity question still open on the population, so I keep it as a gate. My remedy is unchanged.

**A2. The declared metric is right; the abstention hole is a library bug that does not outrank shipping. Metric choice conceded; ranking disputed.**
- **Conceded:**
  - `mean_group_pearsonr` scores the decision and pooled RMSE does not. The per-protein true mean scores 0.134 against 0.187.
  - LightGBM beats ridge (0.355 against 0.294, 9 of 9 splits).
  - The MET-5 exception has two precedents.
  - The repair goes in the library, not in `dataset.py`.
- **Disputed:** that the hole does not outrank shipping. MET-2 and MET-13 are Musts about the score this dataset ships with. Until the repair lands, the leaderboard pays a label-free abstention +0.073 to +0.137 (0.428 and 0.492 against 0.355, 9 of 9 folds). That is a larger gap than the LightGBM-to-ridge spread the advocate uses to show the metric separates models.
- **The code backs this.** `metrics.py:775-776` reads:

  ```python
  corr = corr[var > 0]
  return float(corr.mean()) if len(corr) else float("nan")
  ```

  - So the advocate's evidence that "a constant scores 0.000" depends on the constant.
  - The train mean happens to centre inexactly, so every group is kept and scores about 0.
  - An exact constant such as 0.5 empties every group, and the scorer returns NaN.
  - A metric that gives 0, NaN or a reward depending on float rounding is not well defined at its edge. That is a MET-13 failure.
- **Remedy (unchanged):** repair the library and add tests with the constants 0.3 and 0.5. This is a gate before shipping, not something done alongside it. The same repair covers `huesken_sirna_efficacy` and `numerai_v5_2_1m`.

**A3. The 1,011 rosetta62 `rn` rows: fix the definition. Conceded.**
- My check confirms the advocate's claim that no group is lost. After the exclusion, each of the 56 rosetta62 proteins keeps 99-ish BOINC rows at minimum (median 109). No protein is left empty, so MET-2 still holds.
- One condition: the Baker-archive check, or the named note if "rn" stays unconfirmed, must be settled before shipping. It must not be left to a later pass.

**A4. The CASP10 break is a documentation fix, not a P5 failure. Remedy conceded; rule disputed.**
- **Conceded:** the remedy is the same as mine.
  - Correct the SL wording.
  - Add the forward-window numbers (CASP8 0.340, CASP9 0.483, CASP10 0.016) to `splits_comment`.
  - Name the break in `fit_reason`.
  - Keeping CASP10 is the curator's call, and there is no re-split.
- **Disputed:** the advocate frames this as the tension "the right split against the score" (P4 over P6, SPLIT-4). The split auditor found that CASP10 fails under every split: 0.016 forward, 0.048 grouped, and 0.031 with ridge under IID. So the split is not the issue. What is wrong is the inputs' meaning:
  - In CASP10, SL is the candidate's own length. It varies within the protein in 67 of 67 targets.
  - In CASP6-9, SL is the target's length. It varies within the protein in 0% of targets.
  - The `known` text gives one meaning for all rows.
  - The rule that applies is P5 together with USE-8 (Must): the data must be what the text says it is. The fix is still a text fix, but it is a Must-level correction and a gate.
- **Omitted by the advocate:** the 2,259 CASP10 rows that are not in the paper's validation file. They cover 66 of the 67 targets, with median GDT 0.238 against 0.441. This needs one line in the comments, under PROV.

**A5. Declare `grouping.context="all_rows"`. Conceded in full.**
- The evidence is the same as mine: 0.360 to 0.522 with group context, +0.150 to +0.165 in every fold.
- One addition: if the curator keeps `"none"`, `fit_reason` must state the 0.476 exploit as a known gap. Under SPLIT-23, a declaration the harness cannot enforce must at least be written down as unenforced.

**A6. Stale and loose text: quality work with fixes ready. Conceded.**
- The fixes match mine:
  - restate TP-3 on the declared metric (+0.061, 9 of 9 splits);
  - write "132 of 134";
  - reword the use case and name top-1 loss in the metric reason;
  - add one sentence on the mixed decoy collections;
  - mark the 2026-10-29 record lines as superseded.
- I agree these are quality issues and do not hold back a real task once they are written down.

**A7. The precedents favour keeping. Conceded in part.**
- **Conceded:**
  - SEL-9 is not breached, and the remedy is a Tensions row (my point 7).
  - The SEL-12 call follows `ecoli_proteins`.
  - Keeping despite `Outdated` follows the majority.
- **Disputed:** "already leans toward keep" does not close the conflict with `first_order_theorem_proving`. The precedent-checker's reflection prompt is a curator decision and stays open until it is answered, for example with option (a) or (c). An open consistency check is not a precedent. The same goes for the marker choice between `Outdated` and `Not Representative`.

**What remains between us.** Only the order of the work. These must be done before shipping, because each is a Must:
1. the library repair of the metric (MET-2, MET-13);
2. the `rn` rows resolved, by exclusion or a named note (USE-7);
3. the SL wording and the CASP10 note (P5, USE-8);
4. the `context` decision, or the exploit written into `fit_reason` (SPLIT-23, USE-6).

Everything else is a note that can ship with the dataset.

</details>

## Reference

Rana PS, Sharma H, Bhattacharya M, Shukla A. Quality assessment of modeled protein structure using physicochemical properties. J Bioinform Comput Biol 13(2):1550005 (2015). doi:10.1142/S0219720015500055
