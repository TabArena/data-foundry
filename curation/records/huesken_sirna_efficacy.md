---
unique_name: huesken_sirna_efficacy
name: Huesken siRNA efficacy
checked_by:
- Myunghwan
- Lennart
suggestion: 'Yes'
priority: 4
decision_markers:
- Data Requested
tags:
- Non-IID (Grouped)
- Revisit later
collections:
- New (BeyondArena)
year: '2005'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2510.02476
- https://doi.org/10.1038/nbt1118
v2_path: datasets/_dev/tabarena-v0pt2/huesken_sirna_efficacy/dataset.py
source_row: 865
type_adapter_id: curation-record-v1
---

## Comments

**Current review status (AI, 2026-10-28):** Final ship explicitly approved in the current conversation. Prior individual decisions and completed qualification remain; this new approval supersedes the previously pending overall verdict.

CC (2026-10-28, Myunghwan): "ship for siRNA." Explicit final scientific inclusion of the current reviewed 2,431-row/266-predictor Huesken reporter-assay task, retaining original normalized activity, RMSE and unchanged gene-held-out folds. Earlier scope clarification remains historical; this new explicit ship settles overall inclusion. No build, commit or publication requested.

**Current review status (AI, 2026-10-27):** Add-dataset follow-through is complete; final review-added-datasets verdict is pending. Earlier assertions of scientific inclusion/ship below are superseded agent interpretations, not current curator authority.

CC (2026-10-27, Myunghwan): Clarified that the earlier instruction meant completing tabarena-add-dataset after review for both Youth employment and siRNA, not a final ship verdict. The limited-gene warning and independently confirmed 2005/grouped metadata remain settled. Final overall inclusion is unconfirmed.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 4: siRNA knockdown efficacy on the Huesken et al. (2005) library, 2,361 siRNAs over 29 target mRNAs, a grouped regression in a thin domain; the paper's two patent-derived sets are not public.
- Source: the efficacy data was first published by Huesken et al. (2005), "Design of a genome-wide siRNA library using an artificial neural network", Nature Biotechnology (doi:10.1038/nbt1118, supplementary data); this record's paper, Li, McCarthy, Zhang and Young (2025), arXiv:2510.02476, re-uses it ("We divided the Huesken dataset (2361 data points) into 29 subsets, each corresponding to a different mRNA target") and adds Target1 (patents of institutions A, B, C: 295, 366, 9 points) and Target2 (a patent of institution D: 252 points), with no data availability statement. So `year` 2025 is the re-use; the data dates from 2005 (left as is, metadata is filled only where empty). Features in the paper: 574 per siRNA (361 one-hot positions of a 57-nt window, 189 trimer counts, 24 thermodynamic values); target the knockdown efficacy.
- Use case: a researcher designing siRNAs for a new gene picks the candidates to synthesise and test (Huesken: a genome-wide library designed by a network); fit direct; regime grouped by target mRNA (a new gene at prediction time; the paper used 5-fold CV on Huesken and few-shot on new targets).
- Siblings and duplicates: no record of Huesken or siRNA data (grep: huesken, sirna, knockdown). External collections: none known; Huesken is a standard set of siRNA efficacy predictors.
- Papers and pages: Huesken et al. 2005; Li et al. 2025 (TabPFN on sequence features beats specialised siRNA predictors, their claim).
- Metric: MAE and Pearson correlation reported side by side, correlation emphasised in the conclusion but not named as the criterion (MET-5); Huesken's own evaluation not read; so the fallback `rmse` (MET-8) unless the curator takes Pearson.
- Risks for /add-dataset: sequence data (SEL-12): one-hot and k-mer features where sequence models may win (the paper argues tabular wins); the features are a design choice of ours, to be derived from the sequences as published; the group column (target mRNA) must ship; the `New IID` tag contradicts the grouped regime; Target1 and Target2 not available (`Data Requested`, 14/03/2026).
- Priority: gap + (biology & life sciences and grouped are thin), use case + (siRNA design), source + (Nature Biotechnology paper), shape + (2,361 rows, grouped structure), risk - (sequence modality, SEL-12).

Dataset(s) from a 2025 arXiv paper on tabular foundation models for biomolecule efficacy prediction; this is a genuine tabular predictive task (efficacy regression/classification on molecular descriptor features) and explicitly relevant to tabular ML. The record notes the data was preprocessed from prior work, was requested on 14/03/2026, and could possibly be reconstructed manually. Risks: the features may be derived/transformed descriptors, and a grouped (by scaffold/assay) split may be required. A human must verify data availability, that the features are not lossy/irreversible transforms, the exact target, and the appropriate split.

---

Their data could be used; it is from another work and has been preprocessed.

Lennart: requested their versions of the dataset for benchmarking on 14/03/2026. But we could also likely reproduce one/some of their data state manually

CC (2026-10-26, Myunghwan): Requested the siRNA efficacy add-dataset stage; this is not a final ship or build decision.

**Assessment (AI, 2026-10-26):** Actual-data source reconstruction uses the corrected Huesken 2005 Table 3, 2,431 observed guides across 30 source species/gene groups. The OligoFormer raw copy omits 70 UBE2H guides and assigns NAS 18412 a human target window although the original marks it rodent. Restored from Table 2 and Table 3 species flags; the reusable loader no longer depends on that copy. Keep original normalized activity, not the processed copy's division by 1.341. Qualification and independent panel are in progress; prior screening claims remain historical. Priority 4: gap + (biology/grouped), use case + (library design), source + (corrected primary supplement), shape + (2,431 rows and grouped features), risk - (10 held-out genes per fold and assay transfer limits).

**Assessment (AI, 2026-10-26):** Final add-stage result. Added for Myunghwan's added-dataset review, not final inclusion or build. Corrected Huesken 2005 data: 2,431 guides, 30 species/gene groups, 266 predictors (88 categorical, 178 numeric). The exact primary measured labels, guide chemistry, target context and all 30 native gene-held-out splits have independent checks. Final task probe: LightGBM mean RMSE 0.161820 versus training-mean 0.202355, better in every split; random forest 0.164815 and linear 0.175294; no task-probe flags. Dataset check: 0 errors, one still-unaccepted groups_test_groups_few warning (ten genes per test fold). Repeated partitions reuse the same thirty genes; pooled row scoring is not a demonstration of within-gene shortlist utility or endogenous/clinical transfer. Complete independent/blind ten-role panel recommends ship after documentation and curator dispositions. Descriptor terminal-sign and enthalpy-rounding conventions are now explicit; final documentation edits preserve exact data, dtypes, model inputs, metric and split memberships, with a reuse receipt rather than another model run.

Priority corrected from the earlier AI proposal to 3: start 1 + corrected primary source 1 + shape 1. Current accepted-inventory factors give no biology/grouped gap point, the reporter use is approximate rather than direct, and no qualifying risk deduction is established. No human priority-4 decision is overridden. Year 2025 versus source 2005, New IID versus current grouped task, and the residual '?' split entry remain explicit REVIEW field rows for curator marks; they are not silently changed. The real historical Data Requested entry is retained: Huesken has now been obtained, whereas the reuse paper's patent-derived Target1/Target2 data and identities were not reconstructed here. Its assertion of public patent sources does not support our earlier blanket 'not public' wording. Original full methods and redistribution terms remain unconfirmed; the inspected corrigenda, corrected supplement and later paper do not establish a uniquely mandated original metric, so RMSE remains a qualified fallback. Full evidence and historical notes are preserved; no warning acceptance or human semantic verification is claimed.

CC (2026-10-26, Myunghwan): Approved scientific inclusion. In this case 30 genes are acceptable; even five test genes can be acceptable when the number of test records is sufficient. Confirmed grouped prediction for new gene IDs (OOD in that sense), and asked whether the tag fits. Existing ten-gene test folds are retained; no repartitioning was requested. The original chat words and scoped marks are preserved in the review history.

CC (2026-10-26, Myunghwan): Metadata `tag`: update; Non-IID (Grouped), meaning unseen gene IDs.

CC (2026-10-26, Myunghwan): Metadata `year`: update; 2005 original-source year.

**Assessment (AI, 2026-10-26):** Applied the actual curator approval and accepted `groups_test_groups_few` with the case-specific rationale and multi-family grouped evidence. No fixed minimum number of genes is imposed for this row-level continuous target; no blanket row-count-only rule is introduced. The unchanged folds have ten test genes and 648-942 records. Confirmed grouped cold start; SPLIT-2 already covers unseen IDs under Non-IID (Grouped), with no separate OOD vocabulary. Year/tag choices are applied only where explicitly marked; unanswered rows remain in REVIEW. Exact data, dtypes, target, metric and ordered split memberships are preserved, so completed model qualification is reused. Scientific approval does not authorize build, commit or redistribution.

CC (2026-11-04, Lennart): renamed `huesken_sirna_efficacy` from `dataset_from_uncertainty_guided_model_selection_for_tabular_foundation_models_in_biomolecule_efficacy_prediction`, the title of the 2025 paper that reused the data, since what ships is Huesken et al. 2005 (PROV-1, PROV-8; "give it a proper name"); the other names of the PR #33 batch were checked and stay. The few-groups acceptance is reworded in his words: a group is a large set of observations over which we want to generalize, so from the context a few groups suffice, as for a few hospitals.

**Exception to MET-5 (2026-11-04, Lennart):** the metric is `mean_group_pearsonr` on `target_gene` (origin context) instead of the RMSE fallback for papers that report several metrics ("change"). Fact: the use case ranks guides within a gene, and pooled RMSE rewards a gene's mean (knowing each gene's mean cuts it from 0.1582 to 0.1378), while the literature reports pooled correlation, MAE or AUC with no unique criterion; both metrics pick LightGBM over ridge. Serves P6: scored by the metric the real task would use (MET-1).

CC (2026-11-04, Lennart): sequence encoding: "go ahead with (b)": the preprocessing stays here, with the descriptors, and the record is tagged `Revisit later` "to check if we should drop it like we did for other protein models" (SEL-12) or to declare a sequence kind later.

**Assessment (AI, 2026-11-04):** review panel (none): no panel ran; the issues came from the light static review of the PR #33 page and the research behind each mark, and all are settled. Only `splice` and this dataset are sequence tables in the working copy; pure-sequence candidates were mostly rejected under SEL-12.

**Assessment (AI, 2026-11-04):** review panel (full, second pass after Lennart's PR #33 review): ship after changes (mediator; the wording fixes are applied in the definition: the 97%/80% figure restated as 30 of 30 by RMSE and 29 of 30 by the metric, the `Revisit later` text naming its reopening test, notes on redundancy, scope and the gene offset); disputed: whether the unrun CNN gates shipping (SEL-12), the NaN on a constant prediction (MET-2), dropping or noting the redundant guide columns (CLEAN-8); for the curator: issues 4, 5, 6 and 8 (the rule rows moved to the cross-dataset REVIEW.md). Priority 4: gap + (biology & life sciences is thin among the accepted definitions), use case - (fit approximate, reporter assay), source + (Nature Biotechnology supplement as first publication), shape + (2,431 rows, grouped), risk - none (SEL-12 open but it drops only on a positive finding; no leak, no recommendation against shipping). This supersedes the priority 3 and the "direct" fit of the 2026-10-26 and 2026-10-28 lines.

CC (2026-11-04, Lennart): the declared metric is checked and stays as declared (`mean_group_pearsonr` per target gene, the Exception to MET-5 above; second review page).

CC (2026-11-05, Lennart): kept as a tabular task with the reworded `Revisit later` tag; the sequence-model run stays optional (Review issue 4, A; SEL-12).

CC (2026-11-05, Lennart): `guide_position_01..19` dropped, the base-by-base complement of `target_window_position_38..20` (issue 5, B; CLEAN-22): 247 features, the guide's two DNA overhang bases kept.

CC (2026-11-05, Lennart): "I would like to have usable metrics and them be safe guarded against such failure modes": the shared `mean_group_pearsonr` scores a gene whose predictions are all equal as 0 instead of leaving it out, so a constant baseline scores 0 (issue 6, B; MET-2). A gene with a constant target stays out.

CC (2026-11-05, Lennart): the notes name a companion measure for the bench decision, the precision of the top few guides per gene or the per-gene Spearman correlation; the declared metric is unchanged (issue 8, B; MET-6, MET-7).

CC (2026-11-05, Lennart): reopened with `grouping.context="all_rows"` like protein_model_quality_rf_pcp (protein's Review issue 9, A); a focused panel measures the effect. Open as huesken's Review issue 9 (now or after the panel).

CC (2026-11-05, Lennart): `grouping.context="all_rows"` now, panel after (Review issue 9, B). Per-gene context adds nothing on the 30 splits (LightGBM 0.6708 rows alone against 0.6699 with context, paired SE 0.0025).

CC (2026-11-05, Lennart): ship. Every issue of the second-pass review page is settled, and a record with no open issue ships by default; the definition joins the accepted set, built on the curator's ask. The claim stays until the PR that takes it to `main` sets `DF: Yes`.

## Review

**Outcome:** added. Huesken et al. (2005) siRNA knockdown efficacy, rebuilt from the corrected original supplement: 2,431 guides, 266 features, 30 target genes held out whole, scored by the per-gene correlation. The second-pass review panel (full tier, after your PR #33 review of 2026-11-04) recommends shipping after wording changes, applied in `dataset.py` (the README rebuild is pending your ask); no leak, no refuted claim on the data, no exploit beyond noise. What stays open is whether the unrun sequence-model test gates the shipment (SEL-12), and three small choices (the optional rule rows are an item across datasets).

**Main points:** Is a small CNN on the 30 folds a gate for shipping, or does the `Revisit later` tag with a named reopening test suffice (issue 4)? Make the shared metric score a constant prediction (issue 6)? Drop the 19 redundant guide columns or only note them (issue 5)? Add a companion view (issue 8)? Open: the split count, 20 x 3 in genes instead of 10 x 3 (issue 10).

**Record judgment:** valid, keep (`Yes`).
Validity: SEL-12 open (no sequence model run, no finding of "clearly better"); USE-1, USE-3, USE-5 hold with an approximate fit (USE-4, USE-8); LEAK-10 holds (266 features from guide and insert, best exploit +0.0015); SPLIT-4, SPLIT-5 hold (0 shared genes in 30 splits); PROV-13 holds (both PDF hashes, control scale 0.900/0.354, 2,431 rows).
Value: real signal (LightGBM +0.357 over a constant, 30 of 30 splits); MET-1 holds with the exception to MET-5 kept; MET-2 holds on 30 folds (random -0.006, oracle 1.000) with a constant-prediction edge case (issue 6).
Quality: CLEAN-8 hidden duplication (issue 5); descriptors kept against the CLEAN-24/26 direction for a stated reason (issue 4).
Weighed: signal +, use case +, provenance +, size (2,431 rows, 30 genes) -, sequence modality open.
Left for you: issues 4, 6, 5, 8.

**Issues for Lennart:**

4. **Is the unrun sequence-model test a gate for shipping?**

   * **Problem:**
     - Nobody ran a CNN or LSTM on these folds, so "tabular models are competitive" rests on tabular against tabular
       numbers.
     - If a small CNN clearly beats LightGBM (about 0.65 to 0.67 per-gene correlation), the benchmark would ship a
       sequence task as a tabular one.
     - The reject checks of three other sequence datasets did run this test; this dataset was added without it.
   * **Background:** The rule drops a sequence table only where modality-specific models are clearly better, judged per
     dataset[^sel12]. The dropped sequence cases were raw variable-length strings or frozen language-model embeddings (a
     ready-made numeric summary of a protein sequence from a pretrained model) with a measured gap (PEER); the kept ones
     are `splice`, `ecoli_proteins` and `protein_model_quality_rf_pcp`, and none of them faced a sequence-model test.
     The reject checks of `african_snake_antivenom_binding_challenge`, `ecoli_sigma70_promoters_regulondb` and
     `brca1_variant_effect_evo2` did run "GBM on the positions against a small CNN/LSTM". The `Revisit later` tag in
     `dataset.py` names what reopens it: a small CNN or LSTM on the one-hot guide and window clearly beating LightGBM on
     the 30 gene-held-out folds, then `No` with `Wrong Domain / Source Modality`. The Sequence-kind trigger (a second
     sequence table) has fired with `splice`; none is declared because the positions are already lossless categoricals.
     Keeping the 24 descriptors departs from the direction of the cleaning rules for your reason (no general `Sequence`
     kind)[^clean].
   * **Experiments:** LightGBM +0.357 skill over a constant on 30 of 30 splits; (9 splits) a tree model on the guide
     columns alone 0.67 per-gene correlation; (12 splits) a one-hot ridge 0.621 against 0.652 for all 266 columns; the
     24 descriptors add only 0.03 over the raw positions.
   * **Consistency:** Keeping follows the kept `splice`, `ecoli_proteins` and RF-PCP; the dropped cases were raw strings
     or embeddings with a published gap.
   * **Panel:** The critic prefers the CNN run before shipping; the advocate holds that it applies a stricter bar than
     any kept sequence table faced; the mediator recommends keeping with the reworded tag and treating the run as
     optional.
   * **Unknown:** Whether a small CNN clearly beats LightGBM on these folds, and the paper's claim that tabular
     foundation models match specialised predictors, which was not tested on these folds[^ev6]. Source:
     https://doi.org/10.1038/nbt1118, https://arxiv.org/abs/2510.02476.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the reworded tag (implemented) | kept as a tabular task, tagged `Revisit later`; the tag names the reopening test; the CNN run is optional | follows the kept `splice`, `ecoli_proteins` and RF-PCP; no compute needed | "competitive" rests on tabular against tabular numbers |
     | B | Run one small CNN first | one small CNN on one-hot guide and window on the 30 folds; a clear win means `No`, `Wrong Domain / Source Modality`, and `splice` then needs the same test; otherwise the tag is dropped | settles the question; matches the reject checks of the other sequence datasets | needs your compute approval; a stricter bar than any kept sequence table faced |

   * **Recommendation:** A, the mediator's call: the tag names what reopens it. **Decision:** keep with the reworded
     tag, or run the CNN first?

   **Notes for the AI:** on B, the run needs the curator's compute approval; a clear win means `No` with
   `Wrong Domain / Source Modality`, and `splice` needs the same test for consistency; otherwise drop the tag.

   [^sel12]: **SEL-12** (Must, P2): drop a sequence table only where modality-specific models are clearly better,
     judged per dataset.
   [^clean]: **CLEAN-24** and **CLEAN-26**: the raw entity ships and derived encodings are left to the benchmark.
   [^ev6]: **EV-6**: a paper's claim is not a measurement on these folds.

   **Resolved (2026-11-05, Lennart):** A. Kept as a tabular task with the reworded `Revisit later` tag; the
   sequence-model run stays optional.

6. **Should the per-group correlation score a constant prediction?**

   * **Problem:**
     - `mean_group_pearsonr` leaves out groups with zero variance, so a constant prediction scores NaN in every gene.
     - A constant baseline therefore cannot be scored on the leaderboard[^met2].
   * **Background:** It is the shared function's design, documented in its docstring and also used by
     `protein_model_quality_rf_pcp` and the Numerai metric; the panel computed the dummy skill outside the scorer. The
     definition keeps the shared scorer unchanged; the metric reason in `dataset.py` now states the reproduced figures
     (LightGBM over ridge in 30 of 30 splits by RMSE, 29 of 30 by the metric).
   * **Panel:** The critic calls it a real defect with a one-line fix; the advocate holds that a note is enough.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave and note (implemented) | the shared scorer stays unchanged; the NaN is documented | no change for the other users or the Numerai semantics | a constant baseline cannot be scored |
     | B | Return 0 for a zero-variance group | one line in the shared function | a constant baseline scores | changes the shared function for the other users and the Numerai semantics |

   * **Recommendation:** A (the advocate's call). **Decision:** leave and note, or change the shared scorer?

   [^met2]: **MET-2** (Should): the metric must be computable for a baseline on every fold.

   **Lennart (2026-11-05, change):** Option B: Return 0 for a zero-variance group. I would like to have usable metrics
   and them be safe guarded against such failur modes

   **Resolved (2026-11-05, Lennart):** B. The shared `mean_group_pearsonr` scores a gene whose predictions are all equal
   as 0; a gene with a constant target stays out. Both are decided on the raw values, so a float constant such as 0.3
   cannot pass as a ranking through rounding noise; tests cover 0.3, 0.5, 0.25 and abstaining on some genes. It applies
   to protein_model_quality_rf_pcp (its issue 6, resolved with this) and numerai_v5_2_1m too; their records say so.

5. **Drop the 19 redundant guide position columns, or only note them?**

   * **Problem:**
     - `guide_position_01..19` are the base-by-base complement of `target_window_position_38..20`, so 19 of the 266
       features (7%) restate window positions[^clean8].
     - A check for exact duplicate columns does not see it, and the single-feature signal appears twice (0.181 each).
   * **Background:** Five of the ten yes/no descriptors repeat a single position (U_1, G_1, C_1, U_2, A_19), five more
     are fixed by two positions, and DG_1 and DH_1 are near-bijective. The definition keeps the columns as published, so
     a reader with an aligned window is served too; `dataset.py` now says which columns are redundant and which are
     derived (164 trimer counts, 24 descriptors).
   * **Effect on the task:** There is no leak; the cost is dilution for models that sample features per tree, and extra
     width.
   * **Panel:** The advocate and critic accept either; the column auditor calls it a question and no blocker.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Note only (implemented) | all 266 columns kept as published; the redundancy is stated in `dataset.py` | the guide stays readable on its own; serves a reader with an aligned window | 7% of the features restate window positions; dilution for models that sample features per tree |
     | B | Drop `guide_position_01..19` | keep the two DNA overhang columns (`guide_position_20`, `guide_position_21`): 247 features | no information lost; narrower | the guide is no longer readable on its own |

   * **Recommendation:** A. **Decision:** note only, or drop the 19?

   [^clean8]: **CLEAN-8** (Should, P7): a column that restates others is noted or dropped.

   **Resolved (2026-11-05, Lennart):** B. `guide_position_01..19` left as a copy of window positions 38 to 20 (the rule
   is CLEAN-22, not CLEAN-8 as the footnote says): 247 features, the overhang bases 20 and 21 stay, `dataset check`
   clean.

8. **Name a top-k or per-gene Spearman companion in the README?**

   * **Problem:**
     - The domain practitioner says the bench scientist orders 3 to 8 guides per gene, and Pearson weights the whole
       line[^met6].
     - The shipped Pearson already picks the same model family.
   * **Background:** The definition has nothing about a companion metric now.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave it (implemented) | nothing added | no change | the README does not name the measure the bench scientist acts on |
     | B | One README sentence | names the companion; the declared metric stays unchanged | tells the reader which measure matches the decision | none found |

   * **Recommendation:** B, since the declared metric stays unchanged (a leave is acceptable; the Pearson already picks
     the same family). **Decision:** add the sentence or leave it?

   [^met6]: **MET-6**, **MET-7** (Should): the metric reflects the part of the ranking the user acts on.

   **Resolved (2026-11-05, Lennart):** B. The notes name the companion (the precision of the top few guides per gene, or
   the per-gene Spearman correlation); the declared metric is unchanged.

9. **Declare `context="all_rows"` now, or after a focused panel?**

   * **Problem:**
     - You reopened this dataset with `context="all_rows"` (protein_model_quality_rf_pcp issue 9, A, 2026-11-05), so it
       matches protein, where a target's candidates are held together, as in sat11_hand_algo_runtime[^context].
     - The definition still declares `context="none"`, a panel choice of 2026-11-04 that was never your call.
     - A focused panel measures what context adds here and checks the one fact that could set huesken apart: whether
       a gene's 81 guides are the pool a researcher would design, or a sample of Huesken's library.
   * **Effect on the task:** None on the data, the split or the metric: `context` is metadata. Today no model in the
     example harness sees which test rows share a gene (the group column is not an input), so the gain is not yet
     reachable; that gap is noted for the benchmark.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `none` until the panel (implemented) | the panel runs on `none` and proposes the change | the panel's numbers come first | huesken and protein differ until then |
     | B | `all_rows` now, panel after | the definition declares it today; the panel measures it | huesken and protein agree today | a change before its measurement |

   * **Recommendation:** B: the direction is your call, `context` changes no data, and the panel can still find the
     library-sample fact and propose `none` back. **Decision:** A or B? The panel (claim auditor, split auditor,
     domain practitioner, mediator, editor) needs your go-ahead as well.

   **Notes for the AI:** on B, set `grouping.context="all_rows"` in `dataset.py` with a CC line, run `dataset check`,
   then the focused panel; add a SPLIT-23 Cases row (protein, sat11, huesken) once both are settled.

   [^context]: **SPLIT-23** (Must): the source's use case decides what one prediction is and what is known about a new
     group when predicting; the grouping's `context` declares it.

   **Answer (AI, 2026-11-05):** the data for B. On the 30 shipped gene-held-out splits, untuned LightGBM scores 0.6708
   per-gene correlation on the rows alone and 0.6699 with each numeric feature's z-score and rank within its gene and
   the gene's size added (the protein context model's recipe): a gain of -0.0010, paired SE 0.0025, ahead in 17 of 30
   splits. On protein the same recipe gains +0.161 (0.483 against 0.322). So `all_rows` changes no score here: what
   decides it is what the researcher knows when ranking (the use case, SPLIT-23), not the size. B costs nothing and
   keeps the two datasets alike; A would only delay the same answer.

   **Lennart (2026-11-05, change):** Option B: all_rows now, panel after.

   **Resolved (2026-11-05, Lennart):** B. `grouping.context="all_rows"`; `dataset check` clean; a SPLIT-23 Cases row
   beside protein and sat11. The focused panel waits for your go-ahead; the measurement it would make is above (context
   adds nothing here).

10. **Twenty repeats of the gene split, as the split count in scored units gives, instead of ten?**

   * **Problem:**
     - The score averages one correlation per target gene, and the split holds out whole genes, so the split count
       now counts the 30 genes, not the 2,431 guides; 20 training genes give 20 x 3 splits, where the definition was
       built with 10 x 3.
     - The same change on protein_model_quality_rf_pcp (its issue 10) showed that three repeats there rank close
       methods by chance; here the count moves from ten to twenty, which was not measured.
     - Ship 20 x 3, or keep 10 x 3?
   * **Effect on the task:** not measured here (the raw supplement is not in the local warehouse). Each test fold
     holds about 10 genes; the panel's LightGBM beat ridge on 29 of 30 splits by the metric, a gap far larger than
     the protein dataset's.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 10 x 3 (implemented) | the splits as built | 30 fits per method | departs from the rule without a measured reason |
     | B | 20 x 3 | the split count in scored units, at the next `dataset check` | the count the rule gives for 30 held-out genes | 60 fits on 2,431 rows |

   * **Recommendation:** B: the split holds out the genes the metric scores, the case the rule is written for, and
     60 fits on 2,431 rows cost little[^10a]. **Decision:** A or B?

   [^10a]: **SPLIT-33** (Should): repeated 3-fold cross-validation with 20, 10, 3 or 1 repeats by the size of the
     train side, counted in the units the metric scores when the split holds each one out whole.

   **Notes for the AI:** on B, `dataset check` (the definition is unchanged; the protocol gives 20 x 3), a CC line in
   the record, CHANGELOG.

**Review panel:** ship after changes (mediator). Tier full, second pass after your PR #33 review of 2026-11-04. Claim audit: 21 claims, 15 hold, 3 partly hold (constant prediction scores NaN, the RMSE gene-mean figure reproduced only in size, stale record text), 1 refuted and fixed (a metric-reason figure, not the data: the "97% and 80% of folds" figure; the reproduced values are 30 of 30 by RMSE and 29 of 30 by the metric), 2 untested (Kendall tau 0.64 and the sequence-model test). Blind review: include with changes; main concern `target_gene` as a feature, refuted because the kit's `features()` excludes it (266 features). Task gamer: nothing games the task; best exploit overlap-graph features of the target windows, +0.0015 per-gene correlation on 30 splits (noise), and the honest gain of a gene-centred training target without the window columns, 0.6461 to 0.6686 (single seed, about one split SD). Agreed: no exclusion, the data, splits, hashes and control scale verified, no leak, the exception to MET-5 stands, and the edit list (applied). Disputed: whether the unrun CNN gates shipping (SEL-12, issue 4), whether the NaN on a constant prediction is a defect or a note (MET-2, issue 6), and whether the redundant guide columns are dropped or noted (CLEAN-8, issue 5).

<details><summary>Mediator</summary>

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-12 open, kept (no positive finding of "clearly better"; the sequence-model test is unrun; tag `Revisit later` stays, reworded to name the reopening fact); USE-1/USE-3/USE-5 hold (approximate fit, USE-4/USE-8 stated); LEAK-10 holds (266 features from guide + insert, no label/NAS id/flag/order; task-gamer best gain +0.0015, noise); SPLIT-4/SPLIT-5 hold (whole genes held out, 0 shared genes in 30 splits); SPLIT-24 few groups accepted with a stated reason (LOGO 0.688 vs shipped 0.670); PROV-13 holds (PDF hashes, control scale, 2431 rows verified).
Value: TP-2 real signal (LightGBM +0.357 over dummy, 30/30 splits); MET-1 holds, exception to MET-5 kept (per-gene ranking is the decision); MET-2 holds on 30 folds (random -0.006, oracle 1.000), edge case noted.
Quality: CLEAN-8 hidden duplication (guide_position_01..19 = complement of window 38..20) kept with a note or dropped (curator); CLEAN-24/26 direction vs shipped descriptors, a stated reason (no Sequence kind).
Weighed: signal +, use case +, size (2431 rows, 30 genes) -, source/provenance +, sequence modality -/open.
For the curator: issue 4 (SEL-12 gate), issue 6 (constant-baseline NaN), issue 5 (redundant guide columns), issue 8 (top-k companion), and the rule rows as an item across datasets.
```

No exclusion is argued by any agent; advocate and critic agree on the edit list. No P1-P5 failure found.

**2. Changes to make now (no decision needed)**

1. MET-5 exception reason (`curation_comments`, `metric` reason). Facts first (EV-1): I re-ran the check from the panel's output. LightGBM beats ridge in 30/30 splits by RMSE and 29/30 (97%) by the metric. The text says "97% and 80%": the 80% is wrong. Write "30 of 30 by RMSE, 29 of 30 by the per-gene correlation". Rerun the gene-mean figure and the Kendall tau 0.64 with a stored script and write the reproduced numbers (claim-auditor got RMSE 0.1608 -> 0.1405, not 0.1582 -> 0.1378), or drop the unreproduced figures. Rule: EV-2 (measurement over a page), MET-1.
2. Reword the `Revisit later` line (dataset.py line 167, record). Say: kept as a tabular task, tabular models competitive on the folds (guide-only LightGBM 0.67 per-gene r; one-hot ridge 0.621 against 0.652 for all 266 columns); `splice` already is the second sequence table, so the stated trigger has fired, yet no `Sequence` kind is declared because the positions are already lossless categoricals; reopening fact: a small CNN/LSTM on one-hot guide + window clearly beating LightGBM on the 30 gene-held-out folds (the african_snake_antivenom test). Rule: SEL-12, EV-1.
3. Document in `curation_comments`/README (CLEAN-8, USE-8, SPLIT-24): the redundancy (guide 01..19 vs window 38..20, six yes/no descriptors repeating position columns, DG_1/DH_1 near-bijective); which columns are derived (164 trimers, 24 descriptors); the gene offset in the target that the metric ignores (17.1% of variance between genes; gene-centred training plus dropping window columns gave 0.6461 -> 0.6686, single seed, about one split SD, indicative); scope (no chemically modified siRNA, one reporter system, 2005 chemistry); the one cross-gene homology pair (9 shared 20-mers, Hs P2RX3 / Rn P2rx2, 0 exact feature copies); the row shuffle (raw Table 3 lag-1 0.345, shipped 0.006).
4. Housekeeping: the "88 categorical" count is 78 positions + 10 flags; the README is `build_stale` and names the old folder (a rebuild is pending, on the curator's ask only); the record's top status block of 2026-10-28 (RMSE, priority 4, "direct") is superseded by the 2026-11-04 lines; the prep note that PDF checksums were unchecked is outdated (they match). Dated CHANGELOG entry for the folder.
5. Blind reviewer's top concern (`target_gene` is a feature) is refuted: the kit's `features()` excludes it (266 features). No change. Its other concerns (derived columns, bounded target, scope) are covered by items 3 above.

**3. Issues for the curator, ranked**

**(file issue 4) Issue 1. SEL-12 (Must, P2): is the unrun CNN a gate for shipping? (rule leaves the gate open)**
- Problem: SEL-12 drops only where modality-specific models are clearly better, judged per dataset. No sequence model was run on these folds.
- Rank and strength: SEL-12 is the only Must in play. It drops on a positive finding; none exists. It cannot be an independent failure: the rule is not violated by absence of the test. So keep is the mildest remedy on the ladder.
- Advocate's best evidence: no fact separates it from kept splice (60 DNA positions), ecoli_proteins, RF-PCP; dropped cases were variable-length strings or learned embeddings with a published gap (PEER 0.839 vs 0.528); LightGBM +0.357, one-hot ridge 0.621 vs 0.652 all columns, descriptors add only 0.03. A pre-ship CNN would hold it to a stricter bar than the kept analogues.
- Critic's best evidence: all the "competitive" numbers are tabular against tabular (the tiny MLP 0.511 and ExtraTrees 0.503 are no CNN test); the antivenom, sigma70 and brca1 rejects ran the GBM-vs-CNN step; huesken was added without it.
- Decision needed: (a) keep with the reworded tag, the CNN optional (my recommendation; the tag names what reopens it); (b) run one small CNN on the 30 folds first (needs compute approval; would settle it: a clear win -> `No`, `Wrong Domain / Source Modality`; otherwise drop the tag). If (b) goes to the curator's option "no", the precedent checker's consistency question (below) applies to splice.

**(file issue 5) Issue 2. CLEAN-8 (Should, P7): the 19 redundant guide position columns**
- Effect: 19 of 266 columns (7%) restate window positions 38..20; the same single-feature signal appears twice (0.181). Dilution only for feature-subsampling models. No leak.
- Advocate/critic: both accept a note as the minimum; both accept dropping `guide_position_01..19` (keep the two overhangs) as the alternative. Column-auditor: a curator question, not a blocker.
- Decision needed: note only, or drop the 19. The note is the default (the representation is as published and also serves a non-aligned reader); a drop is a cheap, safe fix if the curator prefers fewer columns.

**(file issue 6 and 8) Issue 3. MET-2 / MET-6,7 (value): constant-prediction NaN and a top-k companion**
- Fact: `_mean_group_pearsonr` leaves out groups with zero variance, so a constant prediction gives NaN (all groups undefined). This is the shared metric's design (documented in its docstring, used by RF-PCP and numerai too), not a huesken-only defect.
- Critic: a leaderboard needs a scorable constant baseline, one-line fix (0 for a zero-variance group). Advocate: note is enough. A change to the shared function affects the other users and the Numerai metric semantics, so it is the curator's call; the dummy skill of the panel was computed outside the scorer.
- Practitioner's top-k/Spearman suggestion: Should-level, not a block; Pearson already picks the same family. If wanted, a README companion only.
- Decision needed: leave and note, or change the shared scorer.

**(across datasets) Issue 4. Optional rule rows (consistency, no validity effect)**
- Add a Cases row for few-groups acceptance (`heart_disease`, huesken) and one in metrics.md noting this is the second grouped-ranking MET-5 exception; the third forces an amendment of MET-5.

**4. Task gamer's exploits mapped**
| Exploit | Rule | Note / known? | Gain |
|---|---|---|---|
| overlap-graph features on windows | LEAK-30/LEAK-adjacent (neighbours within one gene) | new, no `Potential leak` note exists; only 2 overlapping pairs cross genes | +0.0015 (noise) |
| position along the gene | USE-3 | new; the deployed model knows the sequence | -0.004 |
| smoothing over neighbours | LEAK-adjacent | new; neighbours of a test row are never in train | negative |
| row order / group size | LEAK-10 | new; shipped order shuffled (lag-1 0.006, task-gamer -0.043) | 0 |
| gene-centred training target, drop window columns | not a leak (honest modelling) | new; add the sentence in item 3 | +0.02 (single seed, about one SD) |
No exploit differs from noise; none is an issue. No `Potential leak, kept on purpose:` notes exist and none is needed.

**5. Agreed facts**
- 2431 rows, 266 features + target + `target_gene`; 30 genes (46-150 rows, mean 81); 30 splits, 10 test genes and 648-942 test rows each; 0 shared genes in all splits; Mmp7 pair together.
- Target 0.0-1.341, 134 rows above 1, kept; control scale 0.900/0.354 matches the footnote; both PDF hashes match.
- No feature is a label, NAS id, train/test flag or order; 0 of 24,310 test rows have an exact feature copy in train.
- LightGBM +0.357 skill over dummy on 30/30 splits (grouped R^2 0.353 vs ridge 0.245); a single descriptor +0.209. Per-gene r on 12 splits: all columns 0.652, sequence only 0.623, ridge one-hot 0.621, descriptors alone 0.585, MLP 0.511.
- Grouped vs IID: R^2 0.355 vs 0.460, but per-gene r 0.670 vs 0.689 (the metric already removes the gene mean channel).
- Metric: random -0.006, oracle 1.000; LightGBM over ridge 30/30 by RMSE, 29/30 by per-gene r (re-run by me).
- No CNN/LSTM was run by anyone; the paper's TabPFN claim (Li et al. 2025) is not tested on these folds (EV-6).
- No license stated (EV-4: not a reason for No). Fit approximate (reporter vs endogenous).

**6. Consistency with precedent**
- Keep under SEL-12 matches splice, ecoli_proteins, protein_model_quality_rf_pcp (Lennart kept 2026-11-04); the dropped sequence cases are raw variable-length strings or learned embeddings (instadeep kinase/enzyme, protein_location, indabax_tunisia_2023, antigen_avida_hil6, deeploc2, peer_tem1, fusionai). No fact on file sets huesken apart toward a drop. The measured "GBM vs small CNN/LSTM" step of african_snake_antivenom, ecoli_sigma70, brca1 is the reopening test (issue 1).
- MET-5 exception follows RF-PCP (same day, same curator); weaker support (here the gene mean helps little, the literature reports pooled metrics), but the use case carries MET-1. Second such exception: amendment watch. Register flag `exception_to_must MET-1` is a parser false positive (also fires on RF-PCP).
- Few groups follows heart_disease (3 hospitals, grouped); covertype (IID) is distinguished by use case.
- Keeping the 24 descriptors runs against the CLEAN-24/26 direction (SMILES 11-01, spectra 11-02) with a stated reason; not a formal exception. Declaring a `Sequence` kind is not needed now. The consistency check of the precedent checker (option (a): keep and name the reopening fact) is what item 2 of the changes does.
- Rename follows churn_telco_south_asia_duplicate, nyc_taxi, mic_duplicate, chicago_traffic_crashes: the house sentence "names stay" lags practice (wording fix).

</details>

<details><summary>Claim audit</summary>

**Answer to the focus question (SEL-12, "Revisit later")**
Keep, as a tabular task; the evidence points to "tabular models are competitive", but the decisive comparison (a sequence model on these folds) is untested.
Metric = mean_group_pearsonr, 12 gene-held-out splits:
| input | model | score |
|---|---|---|
| all 266 columns | LightGBM | 0.652 |
| pure sequence (78 positions + 164 trimers, no descriptors) | LightGBM | 0.623 |
| pure sequence | ridge (one-hot) | 0.621 |
| positions only | LightGBM | 0.638 |
| 24 descriptors only | LightGBM | 0.585 |
| trimers only | LightGBM | 0.297 |
| positions, one-hot, 64-unit MLP | sklearn | 0.511 |
| pure sequence | ExtraTrees | 0.503 |
- The descriptors add only 0.03 over raw sequence columns. They do not hide a sequence task: a linear model on raw one-hot positions already reaches 0.62.
- Trees and ridge on plain positions are within 0.03 of the best. A tiny MLP and ExtraTrees are worse. That is weak evidence a sequence net does not clearly win; it is not a CNN test.
- SEL-12's test is "modality-specific models clearly better". Nobody has shown that here. Li et al. 2025 (TabPFN beats specialised predictors) is the paper's claim and not on this split (EV-6).
- Remedy if the curator wants the point closed: one small CNN on one-hot guide + window on the 30 folds, with compute approval. Otherwise keep with the `Revisit later` tag as is. Declaring a `Sequence` special kind now is not needed. The raw positions are already shipped categorical, and the spectra precedent was about a type with no usable default encoding, which is not the case here.

**Claim table**
| claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|
| A3/F-G: 2,431 rows, 30 genes, 266 features | task_summary, README | load kit | holds | 2431x268 (266 + target + gene), 30 genes, 46-150 rows/gene, mean 81 | CLEAN-8 |
| D1/C1: 10 genes, 648-942 test rows, 1489-1783 train rows, 30 splits | splits_comment, README | read splits | holds | genes {10}, test 648-942, train 1489-1783, no gene shared train/test in all 30 splits | SPLIT-24 |
| C5/A6: whole genes held out, Mmp7 pair together | grouping | disjointness check | holds | 0 shared genes in 30 splits | SPLIT-4 |
| A4/B4: scale, controls 0.900/0.354, values >1 kept | task_summary, comment | table3.txt footnote line 2558-59; counts | holds | footnote text matches; y range 0.0-1.341, 134 rows >1; PDF SHA256 of both tables match the stated hashes | MET-3, PROV-13 |
| B3: 70 UBE2H guides restored | comment | table2 has Hs UBE2H; 2431 rows in table3 | holds (rows, the omission itself not re-derived) | | PROV-13 |
| B5: NAS 18412 rodent, 19819 human | comment, `_load_raw` | table3.txt flags | holds | rows 18412 (X X X X pattern) and 19819 present; code asserts the flag strings | PROV-13 |
| E1: metric computes on each fold | metric | random, oracle prediction | holds | random -0.006, oracle 1.000 over 30 splits, each test fold has 10 genes with >=46 rows | MET-2 |
| E1/MET-2: edge case, constant prediction | metric | constant 0 vector | partly refuted (minor) | score is NaN, not 0; a dummy/constant baseline cannot be scored | MET-2 |
| E2: "knowing the gene mean cuts RMSE 0.1582 to 0.1378" | metric reason | LGB pred, shift each test gene's predictions to the true gene mean | holds in size, numbers not reproduced | mine: 0.1608 -> 0.1405 (training-mean 0.2024); same ~0.020 drop | MET-5 |
| B8/E2: "97% and 80% of folds" LightGBM beats ridge | comment | prep csv (30 splits) | refuted as stated | prep: RMSE 100% (30 of 30 splits); metric 97% (prep summary says 97% by the metric). The comment says RMSE 97%, correlation 80%. Wrong or from different models; the direction holds | MET-5 |
| E2: Kendall tau 0.64 over nine models | metric reason | not reproduced | untested | nine models and setup are not on file | MET-5 |
| E2/B8 exception to MET-5 is justified | record F16 | origin context, no `original` | holds as a documented exception | `Metric.from_context` with reason; both RMSE and metric rank the families the same way in my runs | MET-1 |
| E3: target_gene is in frame, not a feature | dataset_check | kit `features()` | holds | 266 features, gene excluded from kit; info only | LEAK-10 |
| B2/A5: known at prediction point | comment | read `_clean` | holds | features come from guide, insert window and rules; no assay value, NAS id or train/test flag in the 266 | USE-3 |
| B7: 24 descriptors label-free, fixed constants | `descriptors()` | read code | holds | pure function of the 19 core bases | LEAK-10 |
| B1: modality (SEL-12) | comment | ablation above | see focus answer | | SEL-12 |
| F17: record says RMSE (F11, F15) vs definition correlation | record | read | holds, a documented supersession | F16 states it; the F11 text stays as history | MET-1 |
| F8/F12: priority 3 vs 4 text, fit "direct" vs "approximate" | record | read | stale text only | | |
| G: build_stale true, build path names old folder | README | grep | holds (README line 20) | a rebuild is pending | |
| A8: fit "approximate" | task_summary | n/a | holds (judgment) | single reporter assay | USE-4 |
| License: none stated | dataset.py | n/a | holds (stated as unknown) | EV-4 says not a reason for No | EV-4 |

**Refuted or untested, ranked**
1. Untested, validity-relevant (Must, SEL-12): no sequence model was run, so "tabular competitive" rests on tree/linear ablations. Mildest remedy: keep and leave the tag, or one small CNN run with approval.
2. Refuted (documentation, MET-5/MET-1): the comment B8 "97% and 80% of folds" does not match the prep rerun (RMSE 30 of 30, metric 29 of 30). The tau 0.64 and the 0.1582/0.1378 numbers cannot be traced to a script on file. Remedy: rerun once with a stored script and rewrite the numbers; the direction holds (my 0.1608/0.1405).
3. Minor (MET-2): the metric returns NaN for a constant prediction within a gene (mean_group_pearsonr in src/data_foundry/v2/metrics.py). A constant dummy baseline would score NaN. Remedy: leave and note, or have the scorer return 0 for a zero-variance group.
4. Housekeeping: README `build_stale: true`; the record's F8/F10/F11 lines still mention RMSE, priority 4 and "direct" as history; the prep note that PDF checksums could not be checked is out of date, the PDFs are in the warehouse and match.
5. Open, unchanged: the raw Table 3 order shows lag-1 autocorrelation 0.345 in leak_raw; the shipped order has none, and the splits are by gene, so no effect on the grouped score.

</details>

<details><summary>Column audit</summary>

Frame: 2,431 rows, 268 columns = 266 features + target + group `target_gene`. Dtype probe: 0 of 266 flagged. Python checks on the panel's output

**Answer to focus.md (sequence or tabular?)**
Keep as a vectorized tabular task; no `Sequence` special feature is needed now. Column-level reasons:
- Every input is a fixed-length, aligned vector: the guide is always 19 RNA + 2 DNA bases (21 columns), the window always 57 positions. No variable-length sequence, so a sequence model has no structural advantage except locality (CNN). This is the opposite of the protein case (variable length).
- The encoding is lossless (positions are categorical letters), so a sequence model loses nothing by it, and a tabular model gets the same information plus the 24 thermodynamic descriptors, which carry signal alone (descriptor_ends 0.212 R^2 single feature; all features 0.343).
- Tabular models have measured skill on the gene-held-out folds (LightGBM +0.357 skill, 30 of 30 splits, grouped R^2 0.353 vs ridge 0.245). That meets SEL-12 sentence 2 ("vectorized data is fine where tabular models are competitive") as far as it can be met without running a sequence model. A clear sequence-model win is untested (no compute approved); it remains the paper's claim (EV-6) that TabPFN on these features beats specialised predictors.
- Declaring a Sequence kind (spectra precedent) needs a type with a default encoding; only `splice` (Duplicate) is a second sequence table, so waiting is consistent. If the curator wants a firm drop, the marker is `Wrong Domain / Source Modality`, but the evidence above argues against it.

**Column table**
Prediction point: before synthesis and assay; guide and target insert are known. All 266 features are deterministic functions of guide + insert; none uses a label, NAS id, original train/test flag or row order. Rule IDs: USE-3, LEAK-10, CLEAN-8, CLEAN-14.

| column(s) | meaning | known at prediction? | dtype / cleaning | verdict | rule |
|---|---|---|---|---|---|
| guide_position_01..19 (19) | RNA base at guide position i (A,C,G,U) | yes (candidate design) | category, 4 levels, no missing | fine as feature; redundant, see problem 1 | CLEAN-8 |
| guide_position_20, 21 (2) | DNA overhang bases (lowercase a,c,g,t, ~600 each) | yes | category; lowercase letters distinguish DNA from RNA (t not U), intended | fine | - |
| target_window_position_01..57 (57) | base of 57-nt target window (19 flank, 19 binding, 19 flank); X = outside insert, N/R = source ambiguity | yes (insert known) | category; no column dropped as constant. N/R/X singleton levels in 15 columns (1-5 rows) | fine; rare levels harmless for GBMs, note only | CLEAN-14 |
| target_window_position_20..38 | window binding site = reverse complement of guide 1..19 | yes | exact complement of guide_position_19..01 (checked 1.0 match on positions 1, 5, 19) | redundant, see problem 1 | CLEAN-8 |
| guide_trimer_* (64) | count of each 3-mer in 19-nt core | yes | int16 count (a count typed int, right). Row sum 17 for all rows; none dropped | fine | CLEAN-14 |
| target_window_trimer_* (100 of 125) | 3-mer counts over AUCGX window (N/R mapped to X) | yes | int16; 25 constant/duplicate trimers dropped (from 189) | fine | CLEAN-8 |
| descriptor_ends | terminal DG difference with sign correction, range -2.49..2.49 | yes (from guide) | float; fixed rule, differs from printed formula (documented) | fine | - |
| descriptor_DG_1, DG_2, DG_13, DG_18 | nearest-neighbour free energy of pair i, 10 values each | yes | float, discrete grid (table lookup) | fine | - |
| descriptor_DH_1, DH_all | enthalpy of first pair / whole duplex (1,920 values) | yes | float | fine; DH_1 and DG_1 are near-bijective (10 x 10 values, 10 co-occurring cells) | - |
| descriptor_U_all, G_all, GG_all, UA_all, CC_all, GC_all, UU_all | base / dinucleotide fractions | yes | float fraction of 19 or 18 | fine | CLEAN-14 |
| descriptor_U_1, G_1, UU_1, GG_1, GC_1, U_2, C_1, CC_1, CG_1, A_19 (10) | yes/no sequence flags | yes | category (0/1), as declared | fine; U_1/G_1/C_1 repeat guide_position_01, U_2 repeats position 02, A_19 repeats position 19 as one-hot | CLEAN-14 |
| target_gene | species + gene symbol, 30 groups, 46-150 rows (mean 81) | known for training genes only; group, not a feature | category; in frame as group | fine (info: metric input; excluded from features) | SPLIT-24 |
| normalized_inhibitory_activity | target, 0..1.341, mean 0.693 | outcome | float, original scale, >1 kept | fine | MET-3 |

**Problems, ranked**
1. Hidden duplication (CLEAN-8, mild). `df.T.duplicated()` misses 19 guide position columns because their letters are the complement of window positions 20..38 (exact bijection, 100% match on checked positions). Guide trimers likewise restate window content. Effect: 19 columns, 7% of features, carry no new information; best-single-feature probe shows guide_position_01 and target_window_position_38 tied at 0.181, the same signal twice. Not a leak; model-dilution for random-feature-subsampling models only. Mildest remedy: keep as is and say so in `curation_comments` (the representation is intentionally redundant), or drop guide_position_01..19 and keep the two overhangs. A curator question, not a blocker.
2. Documentation count (info). focus.md says "88 categorical positions"; the real split is 78 positions + 10 binary descriptors = 88 categorical features (+ target_gene = 89). No data change.
3. Cross-group homology (LEAK-adjacent, weak). Exactly 9 shared 20-mers between windows of Hs P2RX3 and Rn P2rx2 (different groups, so can fall across a train/test fold); no other pair of genes shares any 20-mer. Zero exact feature copies across folds (0.0% of 24,310 test rows). The UBE2 paralog family (17 genes, incl. UBE2B/C/D3/E3/G1/H/I/J1/L3/L6/M/N/S/V1) is homologous at protein level but not at 20-mer level; fine for cold-start gene evaluation. Mention in the split text if desired; no remedy needed.
4. Rare levels (info). N/R/X singleton categories in 15 window columns (1-5 rows); harmless, a model sees them as unseen levels at test time. Kept on purpose (B6).
5. Descriptor redundancy (info). DG_1/DH_1 near-bijective; six one-hot-like flags repeat positions. Intended as published 24 descriptors.
6. Raw-order autocorrelation (lag-1 0.345 in raw Table 3, 0.006 shipped): untraced by prep; the shipped order is safe and the frame has no id or order column, so no column-level action.

No leak: no id, NAS number, original train/test flag, assay value, or outcome-caused missingness. Verdict for every feature: fine, except the redundancy note.

</details>

<details><summary>Split audit</summary>

Verdict: right with notes. Grouped by target gene is the right regime. The focus question (keep or drop under SEL-12) is answered below.

**Focus answer (SEL-12 "Revisit later")**
Keep. This is a tabular task where tabular models are competitive; I did not run a sequence model (no compute approval), so the "clearly better" half is unmeasured, not refuted.
- Under the shipped gene-held-out protocol (9 splits, 3 repeats, my LightGBM, 300 trees): mean per-gene Pearson 0.670 with all 266 columns. Guide-only columns (guide positions + guide trimers, no descriptors, no target window) give 0.671. Positions + trimers without the 24 descriptors give 0.650. The 24 descriptors alone give 0.626. A tree model on a fixed one-hot/k-mer vector therefore already captures what the representation holds. A CNN would have to beat about 0.67 clearly.
- Panel probes: LightGBM skill +0.357 against a dummy 0 (30 of 30 splits), a single descriptor +0.209, linear +0.241. The signal is a short 19-nt guide with position-specific and thermodynamic rules. That is vectorized sequence data of the kind SEL-12 sentence 2 allows. SEL-13 does not apply: the descriptors come from fixed rules on the sequence, not from an image or spectrum pipeline.
- The source paper (a 2005 neural network on exactly this table) and Li et al. 2025 (TabPFN beats specialised predictors, in a different split) point the same way. Both are the papers' claims (EV-6), not measured here.
- Consistency: protein or sequence sets dropped under SEL-12 were raw sequences of variable length. This one is a fixed 19-nt window with a measured tabular skill. A declared `Sequence` special feature is not needed now (there is one dataset; `splice` is `Duplicate`). The comment in dataset.py is right to defer it. Suggest rewording the Revisit-later reason to "kept: tabular models competitive (guide-only tree 0.67 per-gene r)".

**Regime against the use case (right)**
- Use case: pick siRNAs for a gene with no measured candidates. That is a new entity with a cold start, so grouped by gene is correct (SPLIT-4, SPLIT-5, USE-3). The group id is a true source id (species + gene symbol from the Table 2 insert), not a cluster or hash. Both Mmp7 inserts share one group.
- One prediction is one row; context "none" (nothing about the new gene beyond its sequence, which is a feature). The aggregation (per-gene correlation, mean over genes) matches the decision, which is a ranking inside a gene. Exception to MET-5 is documented.
- Split sizes: 30 genes, 46 to 150 rows each (mean 81), 10 test genes and 648 to 942 rows per fold. No train/test copies (leak probe 0.0%).

**Alternative splits run (LightGBM, same settings, per-gene Pearson / pooled RMSE)**
| split | per-gene r | RMSE |
|---|---|---|
| shipped grouped 3-fold (9 splits) | 0.670 +- 0.028 | 0.158 |
| leave-one-gene-out (30 folds) | 0.688 +- 0.087 | 0.147 |
| IID 3-fold (random rows) | 0.689 +- 0.009 | 0.145 |
| IID 10-fold | 0.660 +- 0.070 | 0.143 |
Panel probe, R^2: IID 0.460 against grouped 0.355 (gap 0.105).
Reading: the IID versus grouped gap is large for pooled R^2 and RMSE (a gene's mean level is learnable from the window in IID), and almost absent for the shipped per-gene correlation (0.670 against 0.689, inside the spread). The metric already removes the gene-mean channel. The grouped split matters most for any pooled-error reading and for the honest "new gene" claim. The IID 3-fold row is 3 folds on one seed, so a difference of 0.02 is not resolved.

**Problems, ranked by principles.md**
1. Few groups (P4, SPLIT-24 area). 30 genes, 10 test genes per fold. Repeats reuse the same genes, so the fold spread is descriptive. Per-fold gene-r spread is 0.028 (3-fold) and 0.087 (leave-one-gene-out). The paired SE of 0.010 in the task probe counts splits, not genes. The warning is accepted with a stated reason, and I agree it is a case-by-case call (a gene is a large group of 81 rows). Mildest remedy: none; keep the `splits_comment` sentence. Optionally report leave-one-gene-out as a secondary view.
2. Metric rests on a gene-level claim I could not confirm (MET-5 exception, EV-6). The "RMSE 0.1582 to 0.1378" figure and the "97% / 80% of folds" figures are the author's. Prep's reduced rerun gave LightGBM over ridge on 100% of folds by RMSE and 97% by the metric. My rerun is 0.158 with no gene means given, consistent in magnitude. Remedy: restate the 80% as the reproduced figure, or drop the percentages.
3. Raw-order autocorrelation (LEAK-type, low). The raw Table 3 order has target lag-1 autocorrelation 0.345; the shipped order shows none (0.006). Grouped splits make it harmless for the score, but the cause was not traced. Remedy: confirm the shuffle is a documented step (not a split issue).
4. No temporal regime applies (one 2005 assay). No time column, so there is no gap, label-delay or season issue to check.
5. Row-sharing note: `target_window` features identify the gene within a group, so under IID they act as a gene id. This is the reason the IID split is the wrong one here, and the grouped split removes it. It is not a problem for the shipped split.

**Remedies**
None required for the split. Keep the grouped 3-fold x 10 repeats protocol. Edit only the Revisit-later wording, and optionally the 80% claim.

</details>

<details><summary>Domain practitioner</summary>

Role: a bench scientist who designs siRNAs for a gene and picks a handful to order. Sources: dataset.py (task_summary, curation_comments), the record, the panel's output and prep_report.md, use_case.md (USE-1 to USE-12), metrics.md (MET-1, MET-5 to MET-9), selection.md SEL-12. Domain background is my own knowledge of siRNA design practice (Reynolds 2004 rules, Ui-Tei 2004, Amarzguioui 2004, Huesken/BioPredsi 2005, i-Score, DSIR, OligoFormer 2024), recalled and not re-fetched here. I ran no model.

**Answer to focus.md: keep. It is a tabular task.**

1. siRNA design in practice is a feature-table problem. The guide is a fixed-length, aligned 19-nt (+2 overhang) string. Position matters (position 1 and 19 asymmetry, A/U at 19, G/C at 1, U at 10, 5' vs 3' duplex stability). A categorical column per position is the natural, lossless representation. This is unlike a protein: there is no variable length, no long-range fold, and no alignment problem. SEL-12's second sentence ("vectorized data is fine where tabular models are competitive") fits.
2. The field's working tools are tabular. The rule sets (Reynolds, Ui-Tei, Amarzguioui), DSIR, siRNA Scales, i-Score and BIOPREDsi are linear models or small networks over exactly these engineered features. Huesken's own network used a one-hot encoding of 19 positions, which is this table. A practitioner reads the 24 descriptors (terminal DG asymmetry, 5' U/G, A/U content) as the standard design rules, not as a hidden sequence task.
3. Measured here: a single descriptor gives +0.209 skill, LightGBM +0.357, RF +0.336, linear +0.241, on 30 gene-held-out folds. A thermodynamic feature carrying over half the best model's skill is the signature of a tabular problem. Published sequence models (OligoFormer and similar) report only small gains over this feature family. Li et al. 2025 argue that tabular foundation models match or beat them. I could not verify that last point and it is in the random-split setting.
4. The one caveat is that a CNN or transformer might beat LightGBM on these folds. It was not run, so nobody can say "clearly better", and the drop marker `Wrong Domain / Source Modality` needs that evidence. Without it, the SEL-12 drop is unsupported here. I would not drop on this ground.
5. I would not declare a `Sequence` special feature now. The 88 positions are already categorical, and a Sequence kind would invite benchmarks to feed raw strings to models. With one real sequence table (`splice` is a Duplicate), there is nothing to generalize from. Revisit only if a variable-length sequence dataset arrives. I would drop the `Revisit later` tag once the curator accepts this reasoning.

**Fit: approximate (agree)**

Reason: it is a pre-synthesis ranking task on a new gene, within a single reporter-assay system, and transfer to endogenous knockdown is not established (USE-8).

**Gaps ranked by how much they change the task**

1. **What I act on is the top few guides per gene, not a point value.** I order about 3 to 8 siRNAs per gene and want the top ones to hit above roughly 70 to 80% knockdown (here, above about 0.7 on this scale; the scale is a control-normalized activity, with 0.354 as the negative control and 0.900 as the positive control). The target is the right quantity (a measured activity, not a proxy, USE-5). A number is the right form, because I rank by it. Gap size: large for the metric (see below), small for the task itself.
2. **Cold-start is correct for my use, but I would also have a few tested guides in many real projects.** A gene I design for is new to the model (USE-10, grouped split). That matches. Sometimes I have pilot data on the same gene, which this task ignores. This is a known simplification, small.
3. **Reporter assay vs endogenous knockdown.** The activity comes from a reporter construct with the target insert. Endogenous mRNA accessibility and secondary structure differ (the 57-nt window partly covers this). This is what keeps the fit approximate. It is already stated in `fit_reason`.
4. **30 genes, 10 per fold.** For the question "does a model rank guides for an unseen gene", I would want the spread across genes shown, not only the mean. The acceptance of few groups is reasonable (a gene is a large group of 81 siRNAs on average). Repeats reuse the same 30 genes, so standard errors are descriptive. That is already declared.
5. **Features known at prediction time: yes for every input.** Guide, overhang and target window are known before ordering. The 24 descriptors are computed by fixed rules from the sequence. No assay result, NAS id or original train/test flag is an input. Nothing I would have is missing, except a gene-level feature such as expression level or transcript variant, which the source does not give. Minor.
6. **Row matches decision: yes.** One row is one candidate guide (prediction_unit row). Test is a held-out gene, which is what I face.
7. **Trust / distrust:** I would trust a model that beats the thermodynamic-asymmetry rules by a clear margin on unseen genes. I would distrust one trained only on 34 inserts from the 2005 library (older chemistry, one cell system) for modified siRNAs, other lengths or lipid delivery. Neither is a dataset defect.

**What an expert would change**

- Report the within-gene top-k outcome as a second view (see the metric below). Do not change the shipped inputs.
- State in the README that the dataset does not cover chemically modified siRNA or non-HEK-style assays.
- If a sequence benchmark is wanted, run one small CNN on one-hot guide+window on the 30 folds before deciding on `Wrong Domain`. This needs compute approval, which the panel does not have.
- License is not stated. It is a provenance matter, outside my role.

**Metric: partly**

Declared: `mean_group_pearsonr` per target gene (origin context, exception to MET-5). It matches my decision on level: scored per gene, genes weighted equally, ranking inside a gene, and not rewarding the gene mean (MET-1, MET-8 unit of action). Pooled RMSE would reward knowing which genes are easy, which I do not act on, so the exception is justified.

It is partial because:
- Pearson rewards the whole line, including the many mid-range guides. I only act on the top 3 to 8, and the gain I want is whether those top picks work. A rank correlation with weight at the top, or a top-k outcome, scores that (MET-6, MET-7).
- Pearson is sensitive to a few extreme values per gene (activities range up to above 1).
- Only 80% of folds agree between ridge and LightGBM by this metric, against 97% by RMSE. A noisier model choice, though the family ranking holds (Kendall tau 0.64).

Metric I would choose: mean over held-out genes of the mean measured activity of the top-4 predicted guides (or the hit rate of the top-4 above 0.7), reported with per-gene Spearman as a smoother companion. If a single number must stay, per-gene Spearman is closer to my choice than Pearson. This is a suggestion for the curator and not a block, because the shipped metric already ranks within the gene and picks the same family.

**Verdict**

Keep. Fit approximate. Do not drop under SEL-12 and do not add a Sequence special feature now. Metric partly scores the decision.

</details>

<details><summary>Precedent check</summary>

**Precedent check: `huesken_sirna_efficacy`, second pass, 2026-11-04**

**The focus question.** Should it stay under SEL-12 or go as `Wrong Domain / Source Modality`? Against the precedents, it sits on the keep side. Dropping it "like we did for other protein models" would need a fact that sets it apart from two kept datasets, `splice` and `ecoli_proteins`. No such fact is on file.

- **What was dropped:** 7 AI-screened rejects plus one curator reject. They take one of two forms:
  - raw amino-acid strings of full or variable length: `instadeep_kinase_classification_challenge` (up to 560 aa), `instadeep_enzyme_classification_challenge`, `protein_location_prediction_challenge`, `indabax_tunisia_2023` (AI, 2026-10-22), and `antigen_avida_hil6` (Lennart, Mustafa, Alex: "NLP task / data", undated);
  - frozen language-model embeddings: `deeploc2_fungi_membrane_esm2`, `peer_tem1_beta_lactamase_esm2` and `fusionai_gene_fusion_ntv2` (AI, 2026-10-31).

  Where a gap was measured, the source showed it. PEER Table 3 gives fine-tuned ESM-1b 0.839 against frozen ESM-1b 0.528 (Spearman).
- **What was kept:**
  - `splice`: 60 DNA positions as categoricals, `Yes`, in TabArena v0.1 and the working copy (Lennart, Andrej).
  - `ecoli_proteins`: six fixed scores computed from the amino-acid sequence, `Yes` (Lennart). It is the same localisation use case as the dropped `protein_location_prediction_challenge`.
  - `protein_model_quality_rf_pcp`: kept 2026-11-04 by Lennart, who said shipping the structures "would make it a structure task (SEL-12)".

  The line the precedents draw is about what ships: a raw full-length string or a learned embedding goes out; aligned positions or fixed-rule descriptors stay in.
- **Huesken's facts:**
  - 88 positional categoricals, 164 trimer counts and 24 fixed-rule descriptors.
  - No learned embedding, so CLEAN-6 holds.
  - A fixed 21-nt guide and a 57-nt window, so the positions are lossless, as in `splice`.
  - Measured tabular skill: LightGBM +0.357 and beats the dummy on 30/30 splits; ridge +0.241; one descriptor alone +0.209.
  - No sequence model has been measured. SEL-12 drops a dataset only "where modality-specific models are clearly better, judged per dataset", so nothing on file meets that bar.
  - Possible lead, not read (EV-2 inference): DSIR (Vert 2006) and i-Score (Ichihara 2007) reported linear positional models roughly level with Huesken's network.
- **The test the precedents already set (EV-1):** the reject check of `african_snake_antivenom_binding_challenge` (AI, 2026-10-22; a 16-mer as positions) set it as "GBM on the positions against a small CNN/LSTM on the same rows; if the sequence model is clearly better, `No` with SEL-12". `ecoli_sigma70_promoters_regulondb` and `brca1_variant_effect_evo2` carry the same "SEL-12 measured" step. Huesken was added without it.
- **SEL-13 does not apply by analogy.** It is scoped to images and video. Reading sequence descriptors as "hidden modality" would contradict `ecoli_proteins`, `protein_model_quality_rf_pcp` and `clock_protein_toxicity`.

So: precedent says keep, and decide the revisit by that one experiment. A drop without it would be decision 1's departure, below.

---

**1. SEL-12: keep the preprocessing, tag `Revisit later` (CC 2026-11-04, Lennart, option "(b)")**

**Status: consistent for now. Two weak points:**

- **Keeping the 24 descriptors goes against the CLEAN-24/CLEAN-26 direction, with a reason stated.** Lennart's own recent amendments ship the raw entity and leave derived encodings to the benchmark: SMILES on 2026-11-01, spectra on 2026-11-02. The AI recommended (c), dropping the descriptors. Lennart's reason for not doing so is on the review page: no general `Sequence` kind exists, and "otherwise we can do the preprocessing here and add a tag". Neither rule covers sequences, so this is not a formal exception.
- **The deferral's trigger has already happened.** The definition says a `Sequence` kind will be considered "when a second sequence dataset arrives". `splice` is already a second one in the working copy, and the 2026-11-04 Assessment line says so itself. The spectra kind was declared when it covered two datasets (`pancreatic_cancer_mouse_detection`, `micro_mass`, 2026-11-02).
- **The tag does not name what would reopen it.** The only other `Revisit later` record, `fraud_detection_in_electricity_and_gas_consumption` (2026-10-26), does: "dated inspections … would reopen it". Huesken's tag says neither what evidence would decide a drop nor what would trigger the kind.


```text
**Consistency check (AI, 2026-11-04):** your call on huesken_sirna_efficacy (kept, `Revisit later` "to check if we
should drop it like we did for other protein models", SEL-12) points at the dropped cases (instadeep_kinase/enzyme,
protein_location, indabax_tunisia_2023, 2026-10-22; deeploc2, peer_tem1, fusionai, 2026-10-31; antigen_avida_hil6),
but its facts match the kept ones: splice (60 DNA positions, Yes) and ecoli_proteins (fixed scores from the sequence,
the localisation task protein_location was dropped for, Yes). What would set huesken apart if it were dropped?
(a) The AI's best guess: nothing yet. The dropped cases are full-length strings or language-model embeddings with a
published clear gap (PEER: 0.839 against 0.528); huesken is a fixed 21+57-nt window with measured tabular skill
(LightGBM +0.357, 30/30 splits). Keep it, and name the reopening fact in the tag: a small CNN/LSTM on the positions
clearly beating LightGBM on the 30 gene-held-out folds (the african_snake_antivenom test); (b) treat it like the
dropped cases: `No` + `Wrong Domain / Source Modality`, and reopen splice with it; (c) reopen splice and
ecoli_proteins under the same measured SEL-12 test; (d) amend SEL-12, or add a Weighed factor like "A spectrum",
saying where a biological sequence sits (and whether splice already counts as the "second sequence dataset").
```

**2. Exception to MET-5: `mean_group_pearsonr` on `target_gene` (2026-11-04, Lennart)**

**Status: departs with a stated reason; a reasonable exception.** MET-5 is a Should, and here it yields to MET-1 (Must, P6), which the exception serves. It follows `protein_model_quality_rf_pcp` (the same exception, the same day, the same curator), which also has a Cases row in `metrics.md` (line 236). The exception is recorded in all three places: record, definition, and the Cases table (line 237). MET-2 holds: genes have 46 to 150 rows (mean 81), 10 genes per test fold, and `target_gene` is the group, not a feature. The declaration has the same shape as RF-PCP and numerai.

Not a departure from earlier MET-5 calls either. `gallstone_disease` and `ljubljana_breast_cancer` (2026-10-21) went to the fallback, but they are IID classifications with no within-group ranking. I found no grouped regression with a within-group ranking use case on a pooled fallback: `airfoil_self_noise`, `concrete_compressive_strength` and `qsar_*` estimate magnitudes.

Two ways huesken's support is weaker than RF-PCP's:
- In RF-PCP the per-protein mean alone beats LightGBM (0.134 against 0.188). In huesken, between-gene differences are 17.1% of the variance, and knowing each gene's mean only cuts LightGBM's RMSE from 0.1582 to 0.1378 (not reproduced by the prep pass).
- RF-PCP has field practice behind it (CASP scores per target). For huesken, the literature reports pooled metrics only (OligoFormer, siDPT). The per-gene choice rests on the use case alone.

**Amendment watch:** this is the second exception of this kind; the third makes an amendment of MET-5 due (principles, "Exceptions and amendments").

**Register flag `exception_to_must MET-1`:** a false positive. The parser read "Serves P6 … (MET-1)" as the rule being departed from. The same flag fires on RF-PCP.

**3. Rename to `huesken_sirna_efficacy` (CC 2026-11-04, Lennart; PROV-1, PROV-8)**

**Status: departs from house guidance, with a reason; consistent with practice.** `records.md` line 83 says "names stay". Lennart has renamed before, each time before a build: `churn_telco_south_asia_duplicate` (2026-10-15), `nyc_taxi_trip_duration_1m` (2026-10-21), `mic_duplicate` (2026-10-26) and `chicago_traffic_crashes` (2026-11-04). The house sentence now lags the practice. "Names stay once built" would match all five; that is a wording fix, not a curation amendment.

**4. Few-groups acceptance reworded (Myunghwan 2026-10-26; Lennart 2026-11-04)**

**Status: consistent.** It follows `heart_disease` (3 hospitals kept grouped, 2026-10-27). `covertype` (3 areas, made IID) is distinguished by the use case: here, a new gene is the real cold start. Lennart's wording is general ("a group is a large set of observations … a few groups suffice"). The definition calls it "a case-by-case call", so no `splits.md` amendment is due. A Cases row under the "Few groups" factor would make it citable.

**5. Record notes (not decisions, low rank)**

- **`Data Requested`:** huesken is the only `Yes` record carrying this marker. Since the rename, the pending request concerns the 2025 paper's patent sets, not what ships.
- **Stale status block:** the top "Current review status (AI, 2026-10-28)" block still reads "retaining … RMSE". The 2026-11-04 metric decision supersedes it, but a reader sees the old line first.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is real, well-known siRNA efficacy data (Huesken 2005, Nat Biotech) with a sensible grouped-by-gene split and real signal, but it needs the group column handled and some feature redundancy documented.

I did not open the arXiv paper or the DOI page. Everything below comes from `task.md` and `data.parquet`.

**Concerns, most serious first**

1. **`target_gene` is still a feature column.**
   - It has 30 levels and 46 to 150 rows per gene (median 76).
   - The split holds out whole genes, so the test levels are never seen in training. A model that uses the column gets nothing from it, and a naive pipeline may one-hot or target-encode it, which adds noise.
   - Change: mark it explicitly as the group or split key and drop it from the model inputs.

2. **The use case is real, but the evaluation is slightly optimistic.**
   - The decision is real: choose which siRNAs to synthesise for a new gene. The grouped-by-gene split matches that.
   - Different genes can still share sequence similarity (homologs, overlapping windows, near-identical guides). I did not check this.
   - Within a gene, overlapping sliding-window siRNAs are correlated, which is fine under grouped holdout.
   - The data are one lab's single-assay screen, so cross-lab generalisation is not tested. I would state this in the README.

3. **Heavily redundant and derived features (268 columns for 2,431 rows).** The feature groups are:
   - `guide_position_*`: 19 nucleotide columns, stored as categories.
   - `guide_trimer_*`: 64 count columns, derived from the positions.
   - `target_window_position_*`: 57 columns.
   - `target_window_trimer_*`: 79 columns, with an `X` padding or unknown symbol.
   - `descriptor_*`: 25 columns. These are thermodynamic values (DG, DH) and base-composition values, also derived from the sequences.
   - The count and descriptor columns are deterministic functions of the sequence columns. This is legitimate feature engineering from the original paper, but it inflates the width. Column-type handling is right: the nucleotide columns are categories and the counts are int16.
   - Change: document which columns are derived, and consider offering a reduced raw-position variant.
   - The descriptor columns are an odd subset. `descriptor_DG_18` and `descriptor_A_19` look like a selected list from the paper, not all positions. Check whether that selection was made using the full data, because that would be mild leakage.

4. **Target is bounded and slightly censored.**
   - Values run from 0 to 1.341, with mean 0.693 and sd 0.20. A minimum of exactly 0 and a maximum above 1 suggest clipping or normalisation to control.
   - This is plausible, since "normalized inhibitory activity" is relative to a control. I would note it in the README, but it is not a blocker.

5. **Size is modest but adequate.** There are 2,431 rows. With 10 repeats of 3 folds, each test fold holds about 10 genes (roughly 800 rows), which gives usable but fairly noisy scores. Fold variance is high because genes differ in size (46 to 150 rows).

**Checks that came out clean**
- There are no missing values and no duplicate rows. There are also no duplicate feature rows, so there are no copies across train and test.
- No column looks like it would be unknown at prediction time. The features are all sequence- or thermodynamics-derived, and the target is the assay readout.
- The task is not trivial. A quick LightGBM (300 trees, learning rate 0.03) with 3-fold GroupKFold by gene, using the label-encoded features without `target_gene`, gave a Pearson r of about 0.61 between predicted and observed values. That is consistent with published siRNA-efficacy models (about 0.65 to 0.7). So there is real signal, and it is not saturated.

**What I could not check**
- The source paper and DOI page, so I could not confirm that the 30 genes and 2,431 rows match the original (the original set is, as I recall, about 2,431 siRNAs from a small number of genes).
- Sequence homology between genes across folds.
- How `descriptor_*` was selected.
- Whether the target was clipped.
- Whether the repeats use different gene partitions. With only 30 groups, 10 repeats of 3 folds will overlap heavily.

</details>

<details><summary>Task gamer</summary>

**Verdict:** I found nothing that games this task. Baseline LightGBM scores 0.6461 mean `mean_group_pearsonr` (SD 0.027 over 30 splits), and every exploit scored at or below it. Only two honest changes help: gene-centring the training target and dropping the window columns.

**Exploits, ranked by gain**

| # | Exploit | Script | Honest | Exploited | Gain (range) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Overlap-graph features (degree, near-neighbour count, component size) from the 57-nt target windows | `work/positions.py`, `work/exploit_neighbors.py` | 0.6461 | 0.6476 | +0.0015 (-0.025 to +0.022), inside noise | Yes, it knows the gene sequence | none needed |
| 2 | Reconstructed position along the gene | same | 0.6461 | 0.6422 | -0.004 | Yes | none |
| 3 | Smoothing test predictions over overlapping neighbours | same | 0.6461 | 0.626 at shift ≤1, falling to 0.43 at shift ≤10 | negative | n/a | none |
| 4 | Row order and group size | inline check | 0.6461 | no signal | 0 | n/a | none |

Noise reference: adding a random column to the baseline changed the mean by -0.005, -0.0003 and -0.004. Single splits swung by up to ±0.03.

**Findings**
- **Overlap graph:** Windows of different siRNAs on one gene overlap. I rebuilt 14,278 overlapping pairs from shared 15-mers. Only 2 pairs cross genes (Rn P2rx2 and Hs P2RX3), so no label can come from a training gene.
- **Neighbour label correlation:** Neighbours 1 to 10 nt apart have label correlations of 0.25 to 0.58 (r = 0.575 at shift 1, 371 pairs). That is real biology, not a leak. Whole genes are held out, so neighbours of a test row never sit in training.
- **Row order:** Within-gene correlation of the target with row index is -0.012, and lag-1 autocorrelation is -0.043. Rows are shuffled.
- **Duplicates:** There are 0 duplicate guides and 0 duplicate windows.
- **Published file:** I did not try looking the rows up in the Huesken 2005 source file.
- **`descriptor_DH_all`:** It correlates with the target at 0.18 overall and 0.14 within gene, but I could not reproduce it from the guide with the 19-, 20- and 21-nt enthalpy tables I tried. It is a sequence-only descriptor, so I don't see a leak, but I didn't pin down the formula.

**Flaws that hurt an honest model**
The splits are by gene and the metric is within-gene Pearson, so the between-gene offset in the training target is noise.

| Choice | Score |
|---|---|
| Baseline | 0.6461 |
| Train on the target with each training gene's mean removed | 0.6559 |
| Drop the `target_window_*` columns | 0.6587 |
| Both of the above | 0.6686 (SD 0.0225) |
| Ridge on one-hot features, gene-centred | 0.5919 (worse) |

These are single-seed default LightGBM runs. The +0.02 gain is about one split SD, so treat it as indicative. The mildest fix is to note in `task.md` that the metric ignores gene offsets. The window columns are not a flaw: a deployed model has the gene sequence, so I would keep them.

**Not checked**
- The lookup in the published Huesken file.
- Tuned or larger models.
- The exact formula for `descriptor_DH_all`.

- `report.md`
- `honest.py`

`work/` already held scripts from an earlier run (`positions.py`, `overlap.py`, `exploit_neighbors.py` and others). I re-ran them and used their outputs.

</details>

<details><summary>Advocate</summary>

Case: ship as defined. Every fix below is documentation or a tag wording; none touches data, splits or metric.

1. **No fact separates it from the kept sequence tables, so SEL-12 does not drop it.**
   - Evidence (precedent-checker, column-auditor): dropped cases were raw variable-length strings (instadeep kinase/enzyme, protein_location, indabax) or frozen LM embeddings (PEER: 0.839 vs 0.528). Kept: `splice` (60 DNA positions, Yes), `ecoli_proteins` (fixed scores, Yes), `protein_model_quality_rf_pcp`. Huesken is a fixed 19+2 nt guide and 57-nt window, lossless categoricals, no learned embedding (CLEAN-6).
   - Measured tabular skill: LightGBM +0.357 over dummy, 30/30 splits; one descriptor alone +0.209; ridge on one-hot positions reaches 0.621 per-gene r against 0.652 for all 266 columns.
   - Rule: SEL-12 drops only "where modality-specific models are clearly better, judged per dataset". Nobody has shown that. It outranks the objection because the drop needs a positive finding, and none exists.
   - Concession: no CNN/LSTM was run (claim-auditor, split-auditor). "Competitive" rests on tree/linear ablations. Mildest remedy that keeps the dataset: keep `Revisit later` and name the reopening fact, a small CNN clearly beating LightGBM on the 30 folds (the african_snake_antivenom test).

2. **The data and its labels are verified.**
   - Evidence (claim-auditor): 2,431 x 266 features, 30 genes, 30 splits, 10 test genes and 648-942 test rows per fold, 0 shared genes in all splits. Both PDF SHA256s match the stated hashes. The control scale 0.900/0.354 matches the footnote. Target 0.0-1.341, 134 rows above 1, kept (MET-3, PROV-13). Random prediction scores -0.006, oracle 1.000 (MET-2).
   - Rule: SPLIT-4, MET-2. Nothing in the claim audit is refuted on data.

3. **No leak, and the task cannot be gamed.**
   - Evidence (column-auditor, task-gamer): all 266 features are deterministic functions of guide and insert. No label, NAS id, train/test flag or order is an input (USE-3, LEAK-10). The task-gamer ran four exploits (overlap graph, gene position, neighbour smoothing, row order). The best gain was +0.0015, inside noise, and the rest were negative. Neighbour label correlation (0.25-0.58) is biology, and neighbours never sit in training because whole genes are held out. Leak probe 0.0% of 24,310 test rows.
   - The blind reviewer's top concern (`target_gene` is a feature) is refuted. The kit's `features()` excludes it, 266 features exclude the group, and the claim-auditor's E3 row confirms it. That reviewer saw the raw frame and not the kit.
   - Cross-gene homology: only 9 shared 20-mers (Hs P2RX3 and Rn P2rx2), 0 exact feature copies. LEAK-adjacent and weak. Fix: one sentence in the split text.

4. **Grouped by gene is the right regime, and few groups are accepted on a stated reason.**
   - Evidence (split-auditor): the use case is a gene with no measured candidates, which is a cold start (SPLIT-4, SPLIT-5, USE-3). The group id is a true source id. Leave-one-gene-out gives 0.688 +- 0.087 against shipped 0.670 +- 0.028, so 10 test genes per fold does not distort the mean. Myunghwan (2026-10-26) and Lennart (2026-11-04) accepted `groups_test_groups_few`. It follows `heart_disease` (3 hospitals kept grouped). No amendment is due (precedent-checker, item 4).
   - Rule: P4 and the SPLIT-24 warning, answered by the case-by-case acceptance. Remedy if wanted: report leave-one-gene-out as a secondary view. Standard errors from repeats are descriptive and already declared.

5. **The MET-5 exception is justified, because MET-1 (Must, P6) outranks MET-5 (Should).**
   - Evidence: the use case ranks guides within a gene. The domain-practitioner says the metric matches the decision on level (per gene, genes weighted equally, gene mean not rewarded; MET-8). Split-auditor: IID vs grouped gap is 0.105 in R^2 but almost nil under per-gene r (0.670 vs 0.689), so the metric already removes the gene-mean channel. The task-gamer found no exploit. It matches the RF-PCP precedent and Cases row (metrics.md line 236-237), and the exception is recorded in the record, the definition and the Cases table.
   - Concessions: (a) the record's "97% and 80% of folds" is not reproduced. Prep found LightGBM over ridge in 30/30 splits by RMSE and 29/30 by metric. The numbers 0.1582/0.1378 reproduce in size only (mine 0.1608 -> 0.1405), and tau 0.64 is untraceable. Fix: rerun once with a stored script and restate the numbers, the direction holds. (b) The metric returns NaN for a constant within-gene prediction. Fix: return 0 for a zero-variance group, or note it. Neither moves the family ranking. (c) The practitioner prefers top-k or Spearman. That is a suggestion, not a block, and Pearson already picks the same family.
   - Note: the register flag `exception_to_must MET-1` is a parser false positive (precedent-checker).

6. **Fit "approximate" is honest, and the use case is real.**
   - Evidence (domain-practitioner): target is a measured activity (USE-5), one row per candidate guide, and every input is known before ordering. Fit is stated as approximate for reporter-versus-endogenous transfer (USE-4, USE-8), in `fit_reason`. Missing context is minor: pilot data on the same gene, modified siRNA, other cell systems.
   - Fix: one README sentence saying modified siRNA and other assay systems are out of scope.

7. **The remaining findings are documentation, not blockers, and each has a mild remedy.**
   - Descriptor choice (CLEAN-24/26 direction, precedent-checker): the AI recommended dropping the 24 descriptors, but Lennart kept them for a stated reason (no general `Sequence` kind, "otherwise preprocessing here and a tag"). They add only 0.03 over raw columns (0.652 vs 0.623), so they do not hide a task.
   - Concession: `splice` already counts as a second sequence dataset, so the deferral's own trigger may have fired. Do not declare a `Sequence` kind now. The column-auditor and domain-practitioner agree it is not needed, since the positions are already shipped lossless and categorical. Fix: reword the tag to name the reopening fact.
   - Hidden duplication (CLEAN-8, mild): the 19 guide positions are the complement of window positions 20-38 (7% of features). Fix: say so in `curation_comments`, or drop the 19 columns. A curator question.
   - Housekeeping: README `build_stale: true`, stale RMSE/priority-4/"direct" lines in the record kept as history, the "88 categorical" count (78 positions + 10 flags), and the license being unstated (EV-4, not a reason for No).
   - Raw-order autocorrelation: lag-1 0.345 in raw Table 3, but 0.006 shipped and splits are by gene. The task-gamer measured -0.043.
   - Gene-centred training target and dropping window columns give +0.02 (0.6461 to 0.6686, about one split SD, single seed). That is an honest modelling choice and not a defect. Keep the window columns, since a deployed model has the gene sequence.

Ask: ship as defined. Edits: reword the `Revisit later` reason to name the CNN-vs-LightGBM test, correct the 97%/80% figures, and add the README notes on redundancy, scope and the homology pair.

</details>

<details><summary>Critic</summary>

Position: do not exclude. Ship only after the changes below. None is an exclusion; the task is real (new-gene siRNA ranking, grouped split, measured skill, no leak found by any agent). Ordered validity, value, quality.

**1. SEL-12 is open and its reopening test was never run (Must, validity)**
- Problem: the record is kept under `Revisit later`, but nothing on file shows tabular models are competitive with a sequence model on these folds. No CNN or LSTM was run (claim-auditor, split-auditor, column-auditor all say untested). SEL-12 drops only where modality-specific models are clearly better, judged per dataset, so the keep rests on an unmeasured half.
- Effect: if a small CNN clearly beats LightGBM (about 0.65 to 0.67 per-gene r), the benchmark ships a sequence task as a tabular one.
- Evidence: precedent-checker. african_snake_antivenom, ecoli_sigma70_promoters and brca1 carry the measured "GBM vs small CNN/LSTM" step; huesken was added without it. Ablations: ridge on one-hot positions 0.621, LightGBM 0.623 to 0.652; tiny MLP 0.511 (weak, not a CNN test).
- Also the tag is vague: the definition defers a `Sequence` kind "when a second sequence dataset arrives", but `splice` is already that second one (precedent-checker). The only other `Revisit later` record names what would reopen it; this one does not.
- Remedy (mildest): rewrite the tag to name the reopening fact (a small CNN on one-hot guide plus window clearly beating LightGBM on the 30 folds) and state that splice already counts. Better: run that one CNN with compute approval before ship. Do not drop now.

**2. Numbers in the shipped `metric` reason and comment are wrong or untraceable (value, MET-5 exception rests on them)**
- Problem: `curation_comments` says LightGBM beats ridge in "97% and 80% of folds". Prep rerun: 30 of 30 by RMSE, 29 of 30 (97%) by the metric. The 80% figure is not reproduced. "RMSE 0.1582 to 0.1378" reproduced only in size (claim-auditor: 0.1608 to 0.1405). "Kendall tau 0.64 over nine models" has no script or model list on file.
- Effect: the exception to MET-5 (a Should, yielding to MET-1) is justified in the definition by figures a reader cannot verify. The practitioner also reads the 80% as a sign of a noisier model choice, so the wrong figure changes the judgment.
- Rule: MET-5 exception needs a stated, true reason; MET-1 (Must) is served.
- Remedy: rerun once with a stored script, write the reproduced numbers (or drop percentages and tau). The exception itself stands.

**3. Metric edge case and unreported top-of-list view (MET-2, MET-6/7)**
- Problem: `mean_group_pearsonr` returns NaN for a constant prediction in a gene (claim-auditor: constant-0 gives NaN). A dummy baseline cannot be scored.
- Effect: a constant baseline, standard in a leaderboard, breaks or is silently dropped.
- Remedy: return 0 for a zero-variance group, or note it. Optional (Should, not a block): domain-practitioner acts on the top 3 to 8 guides per gene; Pearson weights the whole line. Name a top-k or per-gene Spearman view as a companion in the README. Do not change the declared metric.

**4. Hidden column redundancy not documented (CLEAN-8, quality)**
- Problem: `df.T.duplicated()` misses `guide_position_01..19`, which are the exact complement of `target_window_position_38..20` (100% match on checked positions). Guide trimers restate window content. Six of the ten yes/no descriptors repeat position columns (U_1, G_1, C_1, U_2, A_19, others) as one-hot.
- Effect: 19 columns (7% of 266) with no new information; tied single-feature signal 0.181 twice. Dilutes random-feature-subsampling models. The comment says only exact duplicates were dropped, which reads as if redundancy was handled.
- Remedy: state in `curation_comments` that the representation is intentionally redundant, or drop `guide_position_01..19` and keep the two overhangs. The curator picks. Not a blocker.

**5. Gene-offset noise: the task text should say the target carries a gene offset the metric ignores (quality)**
- Problem: the metric ignores between-gene level, but the training target contains it (17.1% of variance between genes).
- Effect: task-gamer: training on gene-centred target gave 0.6461 to 0.6559; dropping window columns 0.6587; both 0.6686 (single seed, about one split SD). Not an exploit; an honest improvement a participant would find.
- Remedy: a one-sentence note in `task_summary` or README. No data change. Window columns stay (a deployed model has the gene sequence).

**6. Scope limits and homology not stated (USE-8, note only)**
- Problem: the README does not say the data hold no chemically modified siRNA, one reporter system, 2005 chemistry (domain-practitioner). Exactly 9 shared 20-mers between Hs P2RX3 and Rn P2rx2 can fall across a train/test fold; the guide sets overlap in 2 pairs only (task-gamer, column-auditor). Zero exact feature copies across folds.
- Effect: small. Fit "approximate" already covers the main limit.
- Remedy: one line each in README/splits_comment. No exclusion.

**7. Housekeeping before ship (quality)**
- README `build_stale: true`, build path still names the old folder (line 20). A rebuild is pending.
- Record: top "Current review status (2026-10-28)" still says RMSE; F8/F10/F11 say priority 4, "direct", RMSE as live text. The prep note that PDF checksums were unverified is outdated (they match).
- Raw Table 3 order has lag-1 autocorrelation 0.345; shipped order 0.006. Cause untraced (harmless for gene splits). Document the shuffle step.
- Add a Cases row for few-groups acceptance and note this is the second MET-5 grouped-ranking exception (RF-PCP was the first); a third forces an MET-5 amendment (precedent-checker).

**Not argued (dropped for lack of evidence)**
- Few groups (30 genes, 10 per fold): accepted with a stated reason; split-auditor agrees. Leave-one-gene-out gives 0.688 vs 0.670, so no harm shown.
- License unstated: EV-4, not a reason for No.
- Leak: no agent found one; I drop it.

</details>

<details><summary>Advocate rebuttal</summary>

The critic and I agree on the outcome: do not exclude, ship after text fixes. Nothing in the critic's seven points touches data, splits or the metric family. Two points are disputed in part (1 and 5). The rest I concede.

**1. SEL-12 and the unrun CNN: partly disputed**
- Conceded: no CNN or LSTM was run (claim-auditor, split-auditor, column-auditor). The `splice` trigger has fired. The tag does not name a reopening fact. Fix: reword the `Revisit later` reason. It should say that tabular models are competitive (guide-only LightGBM 0.671, ridge on one-hot positions 0.621 against 0.652 for all columns). It should name the reopening fact: a small CNN on one-hot guide plus window clearly beating LightGBM on the 30 folds. It should also say that `splice` already counts as a second sequence table and that no `Sequence` kind is declared now.
- Disputed: running the CNN "before ship" as the better option. SEL-12 drops a dataset only on a positive finding ("clearly better, judged per dataset"). The precedent-checker found that the kept analogues (`splice`, `ecoli_proteins`, RF-PCP) were never put through that test. The dropped cases were raw variable-length strings or learned embeddings. A pre-ship CNN run would apply a stricter bar than any kept sequence table faced, and it needs compute approval that does not exist. The `Revisit later` tag with a named test is the mildest remedy that keeps the dataset (the remedy ladder). The critic also says "do not drop now", so the two of us only differ on whether the run is a gate. It is not.
- The critic's "tiny MLP 0.511" is not a CNN test. The claim-auditor says the same, so it should not count against the keep.

**2. Wrong and untraceable numbers: conceded**
- 97%/80% is refuted. The prep rerun gives LightGBM over ridge on 30/30 splits by RMSE and 29/30 by the metric. 0.1582/0.1378 reproduces only in size (0.1608/0.1405). Tau 0.64 is untraceable.
- Follow-up: rerun once with a stored script and restate the figures, or drop the percentages and tau. The exception stands, since MET-1 (Must) outranks MET-5 (Should) and both RMSE and the metric rank the families the same way.
- One consequence works for the keep. The domain-practitioner called the metric "partly" matching because of "80% of folds" and tau 0.64. With the true figure (29/30), that doubt falls away.

**3. NaN on a constant prediction, and a top-k view: conceded, mild**
- Fix: return 0 for a zero-variance gene, or note it, so a constant baseline scores.
- A top-k or Spearman companion is a Should-level suggestion (domain-practitioner: "not a block"). It would go in the README only. The declared metric stays: Pearson picks the same family, and the task-gamer found no exploit.

**4. Hidden redundancy (CLEAN-8): conceded**
- `guide_position_01..19` is the complement of window positions 38..20. That is 7% of features and mild. The curator chooses: state it in `curation_comments`, or drop the 19 columns and keep the two overhangs.
- My limit: the column-auditor measured no harm beyond dilution for feature-subsampling models, and the descriptors add only 0.03. This is not a validity issue.

**5. Gene-offset note: conceded as a note, not as a flaw**
- A sentence in `task_summary` or the README is fine. It should say that the training target carries a gene level which the metric ignores.
- Weight: the gains are single-seed and about one split SD (0.6461 to 0.6686, SD 0.0225-0.027). The task-gamer called them "indicative". Gene-centring is an honest modelling step that a participant is free to take. It is not an exploit, and nothing in the data changes. The window columns stay, since a deployed model has the gene sequence.

**6. Scope and homology: conceded**
- One line each in the README and `splits_comment`: no modified siRNA, one reporter system, 2005 chemistry. The 9 shared 20-mers between Hs P2RX3 and Rn P2rx2 are the only cross-gene overlap, with 0 exact feature copies across folds.

**7. Housekeeping: conceded**
- Stale README `build_stale` and build path, stale RMSE, priority-4 and "direct" lines at the top of the record, the outdated checksum note (the PDFs match), and the undocumented shuffle step (lag-1 0.345 raw, 0.006 shipped, harmless for gene splits).
- A `Cases` row for few-groups acceptance is useful. Note the watch item: this is the second grouped-ranking MET-5 exception after RF-PCP, so a third forces an amendment. The register flag `exception_to_must MET-1` remains a parser false positive.

**Net**
No point of the critic's brief is an exclusion, and none is refuted on data. The edit list is the union of both briefs:
1. Reword the `Revisit later` reason to name the CNN-vs-LightGBM test and `splice`.
2. Restate or drop the 97/80/tau figures.
3. Return 0 for zero-variance genes.
4. Add README and `curation_comments` notes: redundancy, gene offset, scope, homology and the shuffle.
5. Fix the housekeeping items.
The CNN run stays optional, and is not a gate. Ship as defined with these edits.

</details>

<details><summary>Critic rebuttal</summary>

Position unchanged: do not exclude; ship after the named edits. The advocate's ask ("ship as defined" plus tag rewording, corrected figures, three README notes) is close to mine. I concede most points and dispute four details.

**Advocate point 1 (SEL-12 does not drop it): concede the drop, dispute the evidence offered**
- Concede: a drop needs a positive finding (SEL-12 "clearly better, judged per dataset"). None exists. I never asked for a drop.
- Dispute: "measured tabular skill" (+0.357 over dummy, 30/30) shows tabular models beat a dummy, not that they are competitive with a sequence model. Ridge 0.621 / LightGBM 0.623-0.652 are tabular-versus-tabular. The only neural test (MLP 0.511, ExtraTrees 0.503) is weaker, and is not a CNN test (claim-auditor). The precedent test (african_snake_antivenom, ecoli_sigma70, brca1) is "GBM against small CNN/LSTM"; huesken skipped it.
- Rule: SEL-12 (Must) with EV-1. Remedy stays: the tag names the reopening fact (small CNN on one-hot guide plus window clearly beating LightGBM on the 30 folds). A CNN run before ship is better but optional.
- Agreed with the advocate's own concession: `splice` already is the second sequence table. The tag text must say the deferral trigger has fired and why no `Sequence` kind is declared (positions already lossless and categorical). Not a block.

**Advocate point 2 (data and labels verified): concede**
Counts, splits, hashes, control scale, range 0-1.341 are all confirmed by the claim-auditor. I have no data objection.

**Advocate point 3 (no leak, not gameable): concede, with one small note**
- Concede: blind reviewer's `target_gene` concern is refuted (kit `features()` excludes it); homology is 9 shared 20-mers only; task-gamer best exploit +0.0015.
- Keep as a note, not a defect: training on the gene-centred target and dropping window columns gives 0.6461 to 0.6686. Single seed, about one split SD, so I call it indicative only. One sentence in `task_summary` that the metric ignores the gene offset is cheap and honest (USE-8). The advocate lists it as "not a defect"; we agree it is not, and differ only on whether to write one sentence.

**Advocate point 4 (few groups): concede fully**
Leave-one-gene-out 0.688 against shipped 0.670, two curators accepted, heart_disease precedent. I had dropped this already. Only addition: a Cases row under "Few groups" in splits.md to make it citable (precedent-checker). Optional.

**Advocate point 5 (MET-5 exception): concede the exception, dispute "the direction holds" as sufficient**
- Concede: MET-1 (Must) outranks MET-5 (Should). Within-gene ranking is the decision (practitioner). Fixes (a) rerun with stored script, (b) constant-prediction NaN to 0 or a note, (c) top-k/Spearman as suggestion only.
- Dispute 1: the exception is weaker than the RF-PCP precedent it leans on. In RF-PCP the per-protein mean alone beats LightGBM (0.134 against 0.188). Here between-gene variance is 17.1% and the gene mean cuts RMSE only 0.1608 to 0.1405 (my reproduction of the author's 0.1582 to 0.1378). The literature reports pooled metrics only (OligoFormer, siDPT), so the choice rests on the use case alone (precedent-checker). That is enough for MET-1, but it means the stated reason must be true and short. The unreproduced "80%" and "tau 0.64" should go from the definition unless a stored script backs them. "Direction holds" is shown for 97% (29/30), not for the 80% claim, and the advocate cannot say the family ranking is unmoved by a figure nobody reproduced.
- Dispute 2: the advocate says (b) "neither moves the family ranking". Agreed for ranking, but a leaderboard needs a constant/dummy baseline scorable. A NaN is a real MET-2 defect on the metric's own edge, not a note-level item, though the fix is one line.
- Add: this is the second grouped-ranking MET-5 exception (RF-PCP the first). A third requires an MET-5 amendment (principles, "Exceptions and amendments"). Say so in the Cases row. The register flag `exception_to_must MET-1` is a parser false positive; agreed.

**Advocate point 6 (fit approximate, real use case): concede**
Add the README line on modified siRNA, other assay systems, 2005 chemistry, one reporter system. We agree.

**Advocate point 7 (housekeeping): concede, one dispute**
- Concede: license (EV-4), build_stale, stale RMSE/priority/"direct" lines, 88-categorical count, raw-order autocorrelation (task-gamer lag-1 -0.043 shipped; harmless under gene splits).
- Dispute: the advocate treats descriptor redundancy as settled by "Lennart kept them". That is a curator decision with a stated reason (no `Sequence` kind), but it runs against the CLEAN-24/26 direction (raw entity shipped, derived encodings left to the benchmark; SMILES 11-01, spectra 11-02). Descriptors alone score 0.585 to 0.626 against 0.623 raw, so they carry most of the signal a sequence model would learn. That is a reason to keep them labelled as fixed-rule features, and to say in the README which columns are derived (all 24 descriptors, 164 trimers). Not a block.
- Hidden duplication: advocate and I agree on remedy (document, or drop `guide_position_01..19`). I ask that the curator pick one; "say so in `curation_comments`" is the minimum. Six yes/no descriptors repeating position columns should be named in the same sentence.
- Housekeeping I keep: document the row shuffle (raw lag-1 0.345, shipped 0.006); stale "Current review status (2026-10-28)" block at the top of the record; PDF-checksum note in prep is outdated (they match).

**Net list of edits (the mildest set)**
1. Tag text: name the reopening fact and say splice already counts (SEL-12). Optional CNN run.
2. Rerun the 97%/80%/RMSE/tau figures with a stored script; write reproduced numbers or drop them (MET-5 exception reason).
3. Metric: zero-variance group returns 0, or a note (MET-2).
4. README/curation_comments: redundancy (guide 01-19 vs window 38-20, six flags), derived columns, scope (modified siRNA, one reporter system), the homology pair, the gene-offset sentence, shuffle step.
5. Optional: top-k or per-gene Spearman companion view; Cases rows (few groups, second MET-5 exception).
6. Housekeeping: rebuild (`build_stale`), record header lines.

No remaining point calls for exclusion.

</details>
