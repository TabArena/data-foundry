---
unique_name: raman_adenine_interlaboratory
name: Adenine Interlaboratory SERS Study
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
- Not Representative
tags:
- AI-Filled (Verify)
- Many features
- Spectral Data
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
collections:
- RamanBench
original_source: Other
year: '2019'
collection_period: Unknown
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.1021/acs.analchem.9b05658
- https://doi.org/10.5281/zenodo.3572359
- https://arxiv.org/abs/2605.02003
v2_path: datasets/_dev/tabarena-v0pt2/raman_adenine_interlaboratory/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-11-27, Andrej): the probes ran after the review was written and their numbers are in it. They raise a new Review issue 4: each substrate was prepared with its own concentration series (cAu to 0.90, cAg to 1.82, sAu to 4.50, sAg to 9.00), so the three bench columns alone score R2 0.341 on the shipped splits where the 534 bands alone score 0.272 and both 0.456. The spectrum inside one substrate, one laboratory held out at a time, reaches 0.19 at best. What the task measures is open until that is decided.
CC (2026-11-27, Andrej): renamed from `raman_adenine_colloidal_gold` to `raman_adenine_interlaboratory` (Review issue 3, `change` B). The record was screened as the 225-spectrum colloidal-gold cut; the definition is the whole European interlaboratory study over all four substrates, which the record itself proposes. The folder, the class, the warehouse folder, the two sibling records that named it and the claim moved with it.
CC (2026-11-27, Andrej): Review issue 2, `ok`: the whole 534-band axis ships with its gaps, where two laboratories' instruments did not reach every band.

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a documented 15-laboratory SERS study (3,516 spectra with lab, substrate and laser columns), but adenine in buffer is a model analyte of a method-reproducibility study, the concentrations are a few designed levels, and this record's cut (colloidal gold, 225 spectra) is the smallest of four.
- Source: Fornasaro et al., "Surface Enhanced Raman Spectroscopy for Quantitative Analysis: Results of a Large-Scale European Multi-Instrument Interlaboratory Study", Analytical Chemistry, online 2020-02-21 (PMC7997108); data on Zenodo, doi 10.5281/zenodo.3572359, 2019-12-16, CC BY 4.0, "isSupplementTo" the paper. As published: "all the 3516 spectra uploaded by all participants" in one CSV whose rows carry "labcode", "substrate", "laser", "method", "sample", "type", "conc", "batch", "replica" and the intensities 400-2000 cm-1 (NA outside a lab's range), plus one TXT per spectrum. Six methods (cAg@532, cAg@785, cAu@785, sAg@532, sAg@785, sAu@785) in 15 labs; calibration and test samples prepared centrally (the levels are in the Supporting Information, not read). RamanBench cuts it by substrate: colloidal gold 225, colloidal silver 630, solid gold 810, solid silver 1,851 spectra (534 bins).
- Use case: the study aimed "to define a methodology to assess the reproducibility and trueness of a quantitative SERS method and to compare different methods" (Abstract), and "this study is more about methodology than performance" (Limitations); nobody acts on an adenine concentration. Fit approximate at best (a lab quantifying an analyte by SERS): each lab fit its own linear calibration on the band 715-750 cm-1 and predicted its own test samples. Regime grouped by lab and batch: a new lab or substrate batch is the interlaboratory question.
- Siblings and duplicates: no other record of these data (grep by DOI, Zenodo id, "adenine"); the other three substrate cuts are aliases of this record (PROV-6: cuts by substrate add no task; one dataset over all 3,516 spectra with the method columns as features, or the largest cut, replaces them). Other SERS records of the run: `raman_hair_dyes_sers`, `raman_cancer_cell_cooh`, `raman_serum_prostate_cancer`. External collections: RamanBench (four "Adenine" datasets).
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Papers and pages: the paper (PMC7997108, read through a page summary), the Zenodo record.
- Metric: RMSEP, the study's accuracy figure that combines precision and trueness ("RMSEP² ≅ SEP² + BIAS²", Table 1), compared across methods in Table 3 after range normalisation: a deliberate choice (MET-5), so rmse on the concentration. Inputs none.
- Risks for /add-dataset: few distinct concentration levels (TP-5 on the target's spread); a model analyte with no decision (`Not Representative`, USE-2 borderline); the source calibrates per lab, while pooling labs makes a transfer task (decide the regime from the use case, SPLIT-23); labs cover different spectral ranges (NA padding); raw spectral bins (SEL-15).
- Priority: gap - (regression, chemistry not thin), use case - (a method study, no decision), source + (paper, Zenodo with full metadata), shape + (3,516 spectra over the source with categorical method columns, grouped by lab), risk - (few target levels, model analyte).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 225 spectra x 534 wavenumber features; 1 target(s) (raman-data id: adenine_colloidal_gold); target: adenine concentration.
- Why: Quantify adenine from SERS spectra on colloidal gold substrates measured in many European labs (interlaboratory study) | Quantify adenine from SERS spectra on colloidal silver substrates measured in many European labs (interlaboratory study) | Quantify adenine from SERS spectra on solid gold substrates measured in ...
- Notes: Raw Raman spectral bins (534 wavenumber points, 400-1999 cm-1) as features; SEL-15 judges such signals case by case. Paper marks Adenine as newly released, but raman-data loads it from the 2019 Zenodo record of Fornasaro et al. Few concentration levels; laboratory is a natural group. HF mirror: ...

## Review

**Outcome:** added, on the reframing you asked for. The European interlaboratory SERS study (Fornasaro et al. 2020)
as one dataset over its own Zenodo table: 3,512 spectra from 15 laboratories, 4 substrates and 2 lasers, predicting
the adenine concentration of a centrally prepared solution, with whole laboratories held out. `dataset check` gives 0
errors and 2 warnings. The probes have run since and their numbers are below; they raise a fourth issue, which is
now the one that matters. The axis and the name are settled: the whole axis ships with its gaps, and the record was
renamed from `raman_adenine_colloidal_gold`.
Validity: USE-1 is the open question (issue 1). SPLIT-1 holds: the split is the study's own question, whole
laboratories held out, the tree's Place step[^a1]. LEAK-14 avoided: the solution id, which has the same concentration
in every laboratory, is dropped, as is the blank/calibration/test label[^a14]. LEAK-19: four spectra filed twice are
deduplicated.
Value: measured. LightGBM beats the mean predictor on 30 of 30 shipped splits, by 30.5% of its loss (RMSE 1.943
against 2.794, skill +0.513 with a standard error of 0.093), and the families spread: LightGBM over the linear model
by +0.111 with a paired standard error of 0.031, no flag. The transfer costs what the study said it would: a held-out
laboratory scores R2 0.488 (SE 0.070) where a random split scores 0.803 (SE 0.007), a gap of 0.315, and across
held-out laboratories a random forest reaches 0.515 and LightGBM 0.487 against a baseline of 0, which answers the
few-groups warning. No test row has an exact copy in training on any of the 30 splits, and the nearest-neighbour fit
is negative. The catch is which column carries the signal, which is issue 4.
Quality: the spectrum ships as published and is declared, state `raw`; 179 rows have bands their laboratory did not
cover (issue 2).
Weighed: source + (paper, Zenodo with the full metadata), use case - (a method study; the transfer framing is what
carries it), gap 0, shape + (3,512 spectra, 15 groups), risk - (a model analyte).
For the curator: issue 4 (the substrate, measured after the rest was written) and issue 1 (the use case, which
decides whether it ships). Issues 2 and 3 are settled.

**Main points:** Issue 4 came out of the probes and should be read first: the substrate column fixes the range of the
answer, and the bench columns alone score better than the whole spectrum. Issue 1 is still the one that decides it,
and issue 4 changes the number it is decided on. Issues 2 and 3 are settled.

**Record judgment:** the record is valid but its name is not. It was screened as the smallest of four substrate cuts
(225 spectra) and says the other three are aliases of it; this definition is the one dataset over all four that the
record itself proposes, built from the study's table rather than the benchmark's files, which carry only the
concentration. Priority rises from 2 to 3: the shape factor turns plus (3,512 spectra over 15 laboratory groups).

**Issues for Andrej:**

1. **Does holding out laboratories make a method study into a task?**

   * **Problem:**
     - The screening's objection was that adenine in buffer is a model analyte and "nobody acts on an adenine concentration", which is a use-case objection, not a size one[^a1u].
     - The reframing answers it by changing what is predicted about: not the concentration for its own sake, but whether a calibration reaches a bench it has never seen.
     - That is the study's own stated aim, and the decision behind it is whether a laboratory trusts a transferred calibration or builds its own.
   * **Effect on the task:** everything. If the framing does not carry it, the dataset is `No Good Target / Scientific Discovery` whatever its size; if it does, this is the largest Raman regression set in the collection with 15 real groups.
   * **Experiments:** none decide a use case. What the data shows is that the study's design supports the question: 15 laboratories, 6 substrate-and-laser methods, 3 substrate batches, the same centrally prepared solutions measured in every laboratory.
   * **Consistency:** heart_disease ships three hospitals as groups for the same reason, and `early_learning_predictors` holds out facilities; in both the transfer, not the quantity, is what the task tests.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship with the transfer framing (implemented) | whole laboratories held out, fit `approximate` with the gap named | the study's own question, with a decision behind it; 15 groups is a real split | the quantity itself is a model analyte, so the fit stays approximate at best |
     | B | Don't ship, marker `No Good Target / Scientific Discovery` | the record returns to `2nd Tier` or `No` | the strictest reading of the screening's objection | discards the only interlaboratory design in the collection |

   * **Recommendation:** A, which is the reframing you asked for; the fit is `approximate` and says why. **Decision:** A or B?

   **Notes for the AI:** on B, `suggestion` `No`, the marker, a CC line, and the folder removed.

   [^a1]: **SPLIT-1** and the split tree's Place step: the model is used at a laboratory the data does not contain, and the data holds 15 of them, so whole laboratories are held out (leaf L-PLACE.groups, beside heart_disease).
   [^a14]: **LEAK-14**: a column that identifies the prepared solution carries its concentration across every laboratory.
   [^a1u]: **USE-1**: a dataset no decision fits is not added; the decision here is whether to trust a transferred calibration.

2. **Keep the whole axis with its gaps, or cut to the 355 bands every laboratory covered?**

   * **Problem:**
     - The laboratories' instruments cover different ranges, and the source leaves a band outside a laboratory's range empty.
     - 179 of the 3,512 rows (5.1%) have a gap, almost all in two laboratories: P15 misses 16.8% of its bands and P07 3.7%.
     - 355 of the 534 bands, from 517 to 1,579 cm-1, are complete for every row.
   * **Effect on the task:** with the gaps, the processing encodings return those spectra as missing, so a method that preprocesses will drop or impute 5% of the rows, and the two laboratories are the ones it loses. Cutting to 355 bands makes every row whole and throws away a third of the axis for all 15 laboratories, including the 1,700 to 1,999 cm-1 region.
   * **Experiments:** the counts above are from the source table; no model comparison was run.
   * **Consistency:** the spectrum rule keeps what the source publishes and treats cutting a range as a modelling choice[^a26]; it drops a fill at an edge position and sets an inner fill missing, which is neither case here, because these bands were never measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The whole axis, gaps kept (implemented) | 534 bands, 179 rows with a gap | what the source published; the two laboratories keep their full spectra where they have them | preprocessing encodings return 5% of rows as missing |
     | B | Cut to the 355 complete bands | 517 to 1,579 cm-1, every row whole | every method can use every row | a third of the axis is dropped for all 15 laboratories because two could not reach it |
     | C | Keep the axis and drop the 179 rows | 3,333 rows, every row whole | both the axis and whole rows | P15 loses most of its spectra, so a laboratory group all but disappears |

   * **Recommendation:** A. The gaps are a property of the instruments the study set out to compare, and hiding them by cutting the axis or dropping the rows would remove the variation the task is about. **Decision:** A, B or C?

   **Resolved (2026-11-27, Andrej):** `ok`, A as implemented: the whole 534-band axis ships with its gaps, and the
   179 rows whose laboratory could not reach a band keep them empty.

   [^a26]: **CLEAN-26**: the spectrum ships as the source publishes it; cutting a range off is a modelling choice.

   **Notes for the AI:** on B, trim in `_clean` to the complete bands and say so in the notes and the Spectrum description; on C, drop the rows with any missing band and re-run the group counts.

3. **Rename the record, now that it is not the colloidal-gold cut?**

   * **Problem:**
     - The record is `raman_adenine_colloidal_gold`, screened as the 225-spectrum colloidal-gold file, the smallest of four.
     - The definition is the one dataset over all four substrates and 15 laboratories, which the record itself proposes.
     - The name now describes a quarter of the data and names a substrate that is one of four columns.
   * **Effect on the task:** none on the data. The name is what a reader sees first, and it is wrong.
   * **Experiments:** none.
   * **Consistency:** records have been renamed when the task changed; the cost is the claim, the `v2_path`, the folder and any reference to the old name.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the name (implemented) | the notes say it is historical | nothing to re-point | the name misdescribes the dataset |
     | B | Rename to `raman_adenine_interlaboratory` | record, folder, `v2_path`, claim and the sibling records' references | the name says what it is | touches the claims board and every reference |

   * **Recommendation:** B, and best done before anything is built on the name. **Decision:** A or B?

   **Resolved (2026-11-27, Andrej):** `change`, B: renamed to `raman_adenine_interlaboratory`. The record file, its
   `unique_name`, `name` and `v2_path`, the dataset folder, the class, the warehouse folder and the two sibling
   records that named it all moved; the claim was retaken under the new name. The raman-data id in the screening
   block stays as the benchmark spells it, since that is the name of the file there, not of this dataset.

   **Notes for the AI:** on B, rename the record file and its `unique_name`, the folder and the class, re-run `sync-notebooks`, release and re-take the claim under the new name, and update the sibling records that name it.

4. **The substrate says what the answer's range is, and most of the score is that, not the spectrum.**

   * **Problem:**
     - Each substrate was prepared with its own concentration series, so the substrate column fixes the range of the answer before a band is read: cAu runs from 0 to 0.90, cAg to 1.82, sAu to 4.50 and sAg to 9.00.
     - On the shipped splits the three bench columns alone reach R2 0.341, where the 534 bands alone reach 0.272 and the two together 0.456, against the mean predictor's -0.101.
     - Inside one substrate, with one laboratory held out at a time, the spectrum alone reaches R2 0.19 on sAg (10 laboratories, 4 of them negative), 0.11 on cAg (12, 4 negative) and 0.07 on sAu (6, 3 negative).
   * **Effect on the task:** as it stands the benchmark would rank methods mostly on how well they use a four-value category that stands in for the concentration range, which is the study's design and not something a laboratory holds about an unknown sample. It does not make the task invalid, but it does decide what the score means, and it is the strongest input by the leak probe's own count: `substrate` is the single feature chosen on 30 of 30 splits.
   * **Experiments:** LightGBM over 3 repeats of the 3 shipped grouped folds, as above; ridge diverges on the raw bands (R2 -19) and is not read. The dropped solution id was removed for the same kind of reason, one step closer to the target.
   * **Consistency:** a column that reaches the target through the study's design rather than through the use case is dropped or the task is re-framed; here the laboratory does know its substrate, which is why it was kept in the first place[^a4].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the substrate, the laser and the batch (implemented) | 537 inputs, R2 0.456 | a laboratory does know all three about its own bench before it measures | the score is mostly the series indicator, so the benchmark would rank methods on the study's design |
     | B | Drop the substrate and the laser, keep the spectrum and the batch | 535 inputs, R2 0.272 | the task becomes reading a concentration from a spectrum, which is what the use case asks | the model loses what a laboratory really knows, and the target still mixes four ranges |
     | C | Ship the sAg cut alone | 1,851 spectra, 10 laboratories, one series | one concentration range and one method, so the transfer question stands on its own | the thinnest version: R2 about 0.19 across held-out laboratories, negative on 4 of 10, and three substrates leave |

   * **Recommendation:** B. The use case is a laboratory reading an unknown sample, which the substrate does not bound, and the measured value of the task drops from 0.456 to 0.272 when that stand-in goes, which is the number worth knowing before issue 1 is decided. C is the cleanest question and the weakest dataset. **Decision:** A, B or C?

   [^a4]: **LEAK-14** reaches a column that carries the target through the collection's design, not only a copy of it; the solution id was dropped here for that reason.

   **Notes for the AI:** on B, add `substrate` and `laser` to the dropped columns with the reason, rewrite `task_summary.known` and `changes` and the input bullet of the notes, and re-run `dataset check` and the three probes. On C, filter `_clean` to the sAg rows, re-count the laboratories and the batches, and rewrite the question, the notes and the group definition.
