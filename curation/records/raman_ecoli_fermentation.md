---
unique_name: raman_ecoli_fermentation
name: E. coli Fermentation
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Multi-target
- Many features
- Non-IID (Grouped)
- Spectral Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Entities: Recur'
- Experimental Results
collections:
- RamanBench
original_source: Other
year: '2025'
collection_period: Unknown
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1002/bit.70006
- https://huggingface.co/datasets/chlange/RamanSpectraEcoliFermentation
- https://arxiv.org/abs/2605.02003
- https://git.tu-berlin.de/bvt-htbd/kiwi/tf3/raman-kiwi-experiments
v2_path: datasets/_dev/tabarena-v0pt2/raman_ecoli_fermentation/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-27, Andrej): Review issue 1 stays open, with the question answered. The benchmark makes one task per target and runs both of this release's: glucose (TabPFN v2 at R2 0.971) and acetate (0.491), so the shipped target is its first and its stronger one. The `Multi-target` tag stays on the record although the folder ships one target, to keep the second visible until the benchmark can take a two-target regression.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: at-line Raman spectra of cell-free supernatant from 24 high-throughput E. coli fed-batch cultivations with analyzer reference values, built to feed glucose and acetate predictions into the feeding control; the open points are the spectra (SEL-15) and the cultivation id, which does not ship.
- Source: Lange, Seidel, Altmann, Stors, Kemmer, Cai, Born, Neubauer and Cruz Bournazou, "A Setup for Automatic Raman Measurements in High-Throughput Experimentation", Biotechnology and Bioengineering 122(10):2751-2769, online 2025-07-11 (https://doi.org/10.1002/bit.70006, CC BY 4.0, PMC12417782), with the data in the paper's repository "Raman Kiwi Experiments" (https://git.tu-berlin.de/bvt-htbd/kiwi/tf3/raman-kiwi-experiments, public, created 2025-04-09, named in the Data Availability Statement), so 2025. As published: folders `train/`, `val/`, `test/` with one `data.csv` each (the test file: 122 rows, 838 spectral columns from 300.78 cm-1, then `Glucose`, `Acetate`; header read by a range request). The Hugging Face copy chlange/RamanSpectraEcoliFermentation (created 2025-10-07, CC BY 4.0) has 379 rows (139/118/122) x 1,870 bins (391-3385 cm-1) + 2 targets, glucose missing in 6 rows. "We measured Raman spectra in 24 E. coli fermentations"; samples about hourly over a 4 h batch and a 4 h glucose-limited feed phase, two 10 s spectra per sample; reference glucose and acetate by a Cedex Bio HT analyzer.
- Use case: in a high-throughput bioprocess facility the platform predicts glucose and acetate for each at-line sample, and "the predictions are written to the database to allow other models to use them for adjusting feeding strategies" (Sec. 2.3); fit direct. Regime grouped by cultivation: "we divided the experiments into three groups at random" of 8 cultivations for training, validation and test (Sec. 2.6.4), and the three folders are those groups, so three folds over whole cultivations can be built exactly from the source (SPLIT-19, SPLIT-24); the two spectra of a sample share their target values.
- Siblings and duplicates: no duplicate (grep for the DOI and the HF id). Same platform and lab: `raman_ecoli_metabolites` (pipetted mixtures), `raman_bioprocess_analytes_anton_532` (the eight-instrument set the paper adds to its training data), `raman_bioprocess_substrates`. The same task on other runs: `raman_kaiser_ecoli_fermentation` (Kögler 2018, 14 samples of one run), `raman_yeast_fermentation` (screened `TBD -> 2nd Tier`, 2), `raman_ralstonia_fermentations`. External collections: RamanBench (arXiv 2605.02003, A.18.2 and Table 36, an existing dataset [97]).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (a 1-D CNN tuned by Bayesian optimisation with Hyperband, 2,261 extra spectra from eight spectrometers in training; Sec. 2.6, 3.3); the HF card; RamanBench A.18.2.
- Metric: `mae` per analyte: "the mean absolute error of 0.27 g L-1 for glucose and 0.06 g L-1 for the acetate predictions" (Sec. 3.3) is the one error the paper reports on its test cultivations, so the source's metric (MET-5), on glucose or per target; inputs none.
- Risks for /add-dataset: no cultivation id in either copy: build the folds from the source's three groups (SPLIT-19) or ask the authors for the run ids (SPLIT-25 if neither works); the two copies differ in their spectral axis (838 columns from 300.78 cm-1 against 1,870 from 391 cm-1): take the repository's files and check which is raw (PROV-8, PROV-13); two targets: glucose, or both declared (CLEAN-18); raw spectral bins (SEL-15, weighed against), though calibrating on spectra is exactly the use case.
- Priority: gap 0 (regression, grouped not thin; domain unset), use case + (the source names the feeding decision), source + (paper, repository and card by the authors), shape 0 (about 190 samples in 24 cultivations, one feature type), risk - (no cultivation id, spectral bins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 379 spectra x 1,870 wavenumber features; 2 target(s) (raman-data id: ecoli_fermentation); target: glucose, acetate concentrations (2 targets).
- Why: Predict glucose and acetate in E. coli fed-batch supernatant from at-line Raman spectra
- Notes: Raw Raman spectral bins (1,870 wavenumber points, 391-3385 cm-1) as features; SEL-15 judges such signals case by case. Multi-target. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/ecoli_fermentation

## Review

**Outcome:** added. Lange et al. (2025): glucose in a fed-batch E. coli culture from an at-line Raman spectrum of its
supernatant, the reading the facility's feeding strategy acts on. 373 spectra of 187 samples from 24 cultivations, held
out as the source's own three random groups of eight. `dataset check` gives 0 errors and 4 warnings, all consequences
of the design. The probes find no exact copy, no dominant band, and no flag at all: a selected linear model scores MAE
0.3202 against the dummy's 1.1903 on 100% of the splits, close to the paper's own 0.27. Two things are for you: half
the glucose values sit exactly on the analyser's floor, and the split has only three groups.
Validity: USE-1, USE-5 hold, fit direct, the paper's own feeding decision. LEAK-10 holds, the spectrum is the only
input. SPLIT-19 applied: the three files are the source's own random groups of eight cultivations[^e19]. PROV-8
decided which copy is the data[^e8].
Value: real signal, and real across groups: holding a group out costs 0.042 of R2 against a random split, and across
held-out groups ridge reaches 0.780 (baseline 0)[^e5].
Quality: the spectrum ships as published and is declared, state `raw`. The censored target is the open question.
Weighed: source + (paper, the authors' release), use case + (the feeding decision is named), gap 0, shape - (373 rows,
24 cultivations, 3 groups), risk - (half the target on its floor).
For the curator: issue 1 (the target), issue 2 (three groups), issue 3 (the copy, to confirm).

**Main points:** Issue 1 is the one with teeth: 51.5% of the glucose values are exactly 0, so half the target is the
analyser's limit rather than a measurement. Issue 2 asks you to accept three groups on the group probe's evidence.

**Record judgment:** valid. The screening said 379 spectra, 24 cultivations, two targets and no cultivation id, and the
data confirms each. Its open point, which copy to read, is settled in issue 3.

**Issues for Andrej:**

1. **Glucose, acetate, or both, when half the glucose values are the analyser's floor?**

   * **Problem:**
     - 192 of the 373 glucose values are exactly 0.0, which is 51.5%, spread evenly over the three groups (49.1%, 50.8%, 54.0%).
     - The next smallest values are 0.0279, 0.0660 and 0.0742 g/L, so the zeros are a floor with a gap below the rest, not the low tail of a distribution.
     - The analyser reports a concentration below its limit of quantification as 0, and a glucose-limited fed-batch spends half its samples there by design[^e1].
   * **Effect on the task:** a regression whose target is at its floor half the time is partly a classification, "has the culture run out of glucose yet", and the error measure rewards getting the floor right over reading the concentration. Acetate has 2 zeros in 373 rows and runs to 1.592 g/L, so it is the continuous reference of the same samples.
   * **Experiments:** on the shipped splits a selected linear model reaches MAE 0.3202 against the dummy's 1.1903, beating it on 30 of 30 probed splits; the paper reports MAE 0.27 for glucose and 0.06 for acetate on its own test cultivations. The bands the single-feature probe picks sit at 2877 to 2934 cm-1, the C-H stretch region, on 30 of 30 splits.
   * **Consistency:** the records treat a censored target case by case rather than by a rule; nothing here has a precedent that decides it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Glucose (implemented) | one target, 373 rows | the quantity the feeding strategy acts on, and the source's first reported number; the floor is a real state of the culture | half the target is one value, so part of the score is a detection problem |
     | B | Acetate instead | one target, 373 rows | continuous over its whole range, so the score reads concentration throughout | not the quantity the feeding decision acts on; the paper's smaller number |
     | C | Both, as a multi-target | two targets on the same rows | keeps the use case and the continuous reference | a multi-target task is rarer in the benchmark and the metric must say which target it averages |

   * **Recommendation:** C if the benchmark takes a two-target regression, otherwise A with the floor named in the notes, as it is. The use case is glucose, and dropping it to escape a censored target would ship a task the source does not have. **Decision:** A, B or C?

   **Answer (2026-11-27, open):** "We currently don't have multi-target in the benchmark, but you could add the
   appropriate tag for that. What target did RamanBench use?"

   Both, and glucose first. The benchmark does not choose between the targets of a release: it makes one prediction
   task per target, 163 of them over its 53 regression datasets, and this dataset gives it two. Its own table reports
   "E. Coli Fermentation - Glucose" with TabPFN v2 at R2 0.971 and "- Acetate" with the same model at 0.491. So the
   target we ship is its first one, and the one it reads best; acetate is the weaker of the two there, which is an
   argument against option B that was not in the table above.

   The tag is already on this record: it carries `Multi-target` from the screening, and it stays, by your decision,
   although the folder ships one target and the rule would otherwise strip it[^e18]. That keeps the second target
   visible for a round where the benchmark can take one. The floor is a separate matter and earns no tag: the
   two-regime marker is for a lowest value independent of the rest of the distribution, and a reporting floor was
   ruled out as a second regime when the tag was written.

   The decision between A, B and C is still yours and the issue stays open.

   [^e18]: **CLEAN-18**: a release with several targets ships one and names the rest; the tag goes when the dataset
   predicts one target.

   **Notes for the AI:** on B, `target = "acetate_g_per_l"`, keep acetate in `_clean` and drop glucose, rewrite `task_summary` and the first notes bullet, re-run the checks and the probes. On C, declare both and say in `metric` which target the score averages.

   [^e1]: **CLEAN-11**: a value that is unusual but not shown impossible stays; the zeros are the analyser's floor, a real state of the culture, not missing data.
   [^e19]: **SPLIT-19**: the source's own split is preferred where it is valid; the three released files are its random groups of eight cultivations.
   [^e5]: **TP-5** and the few-groups rule: a score on few groups is kept only when the signal across groups is real.
   [^e8]: **PROV-8**: the copy that is the measurement is the data.

2. **Accept three groups, on the group probe's evidence?**

   * **Problem:**
     - The split has three groups, so a test fold holds one, and the largest holds 37% of the rows.
     - No cultivation id ships in either copy, so 24 cultivations cannot be the groups; the file a sample comes from is the finest cut the release allows.
     - The check raises `task_group_count_low`, `groups_test_groups_few` and `groups_largest_share_high`, each a consequence of that.
   * **Effect on the task:** scores rest on three held-out sets rather than 24, so the standard error across folds understates how much a new cultivation could differ.
   * **Experiments:** holding a group out costs little: LightGBM scores R2 0.696 (SE 0.040) grouped against 0.738 (SE 0.069) on a random split, a gap of 0.042 over 3 repeats of 3 folds. Across held-out groups ridge reaches 0.780, LightGBM 0.696 and a 5-nearest-neighbour 0.585, against a baseline of 0, so the signal is not a property of one group.
   * **Consistency:** heart_disease ships with three hospitals as groups on the same reasoning, and micro_mass and sarcoma were kept at few units per class inside large folds.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept the three warnings with the probe's reason (implemented) | the reasons go into `accepted_check_warnings` | the signal across groups is measured and real; three hospitals carry heart_disease | three is few, and one group carries 37% of the rows |
     | B | Ask the authors for the cultivation ids | the split waits for 24 groups | the honest split the data was collected for | an open ask with no date; the record stays `TBD` |

   * **Recommendation:** A, and B as a note worth sending anyway. **Decision:** A or B?

   **Notes for the AI:** on A, add `accepted_check_warnings` for `task_group_count_low`, `groups_test_groups_few` and `groups_largest_share_high`, each citing the group probe's numbers; re-run `dataset check`.

3. **Confirm that the release, not the paper's repository, is the data.**

   * **Problem:**
     - The paper's repository and the authors' release hold the same validation and test samples but differ in the training file and the axis.
     - The repository's training file has 2,400 rows against the release's 139, and its axis is 838 bands from 300.78 to 1,941.12 cm-1 against 1,870 from 390.63 to 3,384.7.
     - The difference of 2,261 rows is exactly the extra spectra from eight spectrometers the paper adds to its training set, which our records carry as their own dataset.
   * **Effect on the task:** reading the repository file would train the task on another dataset's spectra without saying so and would put every spectrum on a grid shared across instruments rather than the one the fermentation was measured on.
   * **Experiments:** the two copies' validation and test targets are the same multisets, row order aside (118 and 122 rows); the training counts are 2,400 against 139, and 2,400 - 139 = 2,261.
   * **Consistency:** the provenance rule prefers the copy that is the measurement[^e8b]; the same reading sent raman_mlrod to its deposit and raman_adenine_interlaboratory to its study's own table.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The Hugging Face release (implemented) | the fermentation samples on the measuring instrument's grid | the measurement, and no second dataset mixed in | the training side is 139 rows, as the source measured it |
     | B | The repository file | the paper's training matrix | reproduces the paper's own model exactly | mixes in 2,261 spectra of another record and a cross-instrument grid |

   * **Recommendation:** A. **Decision:** confirm A, or B?

   [^e8b]: **PROV-8**: the copy that is the measurement is the data.

   **Notes for the AI:** on B, read the repository CSVs, declare the eight-instrument spectra as a part source, and say in the notes which record they also belong to.
