---
unique_name: pancreatic_cancer_mouse_detection
name: NCI Pancreatic
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
decision_markers:
- Selection Bias
tags:
- Many features
- Non-IID (Grouped)
- Spectral Data
- 'Samples: No Time Dimension'
- 'Entities: Recur'
collections:
- FS Benchmark
original_source: Other
year: '2003'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://home.ccr.cancer.gov/ncifdaproteomics/CancerCellPanINDataBinned.zip
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
notebook_path: datasets/beyond_iid/grouped/pancreatic_cancer_mouse_detection/pancreatic_cancer_mouse_detection.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/pancreatic_cancer_mouse_detection/dataset.py
source_row: 1035
type_adapter_id: curation-record-v1
---

## Comments

Original data is multiple serums collected per mouse

CC (2026-10-06, Lennart): Kept in TabArena v0.2 as a valid tiny, high-dimensional task after the task-probe review (flag `unstable`). Grouped by mouse, each test fold holds about 12 PanIN and 13 control mice. The signal is weak but real: on BeyondArena RealTabPFN-2.5 (ROC AUC 0.664), EXAONE (0.654) and TabSwift (0.628) beat 0.5 on all 11 of their folds, while the median of 29 configurations is 0.54 (gradient-boosted trees near chance). Open question, the one that could make this a batch-effect case like prostate_cancer_detection (same NCI-FDA data bank, retired for processing artefacts; Baggerly et al. 2004 found such artefacts in the program's ovarian spectra): the file names' `t` suffix (42% of control spectra, 30% of PanIN spectra; 37 of the 73 mice have spectra with and without it). Within the controls, `t` spectra separate from the others at ROC AUC 0.67 (logistic model, grouped by mouse); within PanIN they do not (0.45). The suffix alone could explain at most about AUC 0.56 of the label, which reaches 0.63-0.66, so the label signal is not only the suffix; what `t` marks needs the authors.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — the paper reports sensitivity and specificity at its classifier's operating point, with no single threshold-free metric.

CC (2026-10-21, Andrej): Keep, with the raw spectra. Each row is one serum mass spectrum (intensities in 6,771 mass bins) of one of 73 mice; checked against shuffled labels, standard spectral processing and the `t` file marker.
- Raw instrument signal: the rows are spectra before the usual processing (smoothing, removing the slowly varying background called the baseline, scaling each spectrum to its total intensity, log). Done on each spectrum without labels, that processing raises logistic regression from ROC AUC 0.66 to 0.74 and TabPFN 3.5 from 0.66 to 0.73 (better on 11 and 12 of 12 mouse-grouped folds); the data page itself asks for "normalization, baseline correction, and alignment prior to any such analysis". Not a reason to drop: after processing, ordinary tabular models are still the best tools. The data stays raw; the processing belongs in the evaluation pipeline (PR #21).
- Weak signal: logistic regression reaches ROC AUC 0.66; with the labels shuffled between mice (200 times) it reaches 0.51 on average and 0.62 at the 95th percentile (p ≈ 0.01). Shuffled labels also beat 0.5 on at least 11 of 12 folds in 14% of the shuffles, so "above chance on every fold" alone is weak evidence. Not severe: the signal beats shuffled labels on the mouse-grouped split.
- `t` file marker (66 files: 42 control, 24 PanIN): not a measurement batch. The run numbers and chip positions in the file names show marked and unmarked spectra, and both classes, measured mixed on the same 8-spot chips, more evenly than chance would place them. It marks about half the samples of mice bled several times and almost never a mouse's only sample (1 of 29), so it splits each mouse's bleeds in a way the files do not explain. Not severe: without the marked spectra logistic regression still reaches 0.63.
To do: ask the authors what `t` marks and where the 10 missing control spectra went.
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `debernardi_urinary_pancreatic_cancer` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-02, Lennart): The serum spectrum is declared as a spectrum (`spectra`, CLEAN-26; PR #21, Andrej's proposal): it ships raw as the NCI-FDA page publishes it (6,771 bins of 400 ppm, m/z 800 to 11,993), the container records the bins in m/z order as a feature group, and the benchmark encodes it row by row, by default with MALDIquant's steps (square root, Savitzky-Golay over 21 points, SNIP baseline, total ion current). On the 60 shipped splits the default lifts the tree models by 0.10 to 0.15 ROC AUC, PLS-DA by 0.06 and TabPFN v3.5 by 0.03 (0.659 to 0.690); logistic regression loses 0.02. A reconstruction of PR #21's own chain, which ends in a log, scores higher for TabPFN (0.716) and the linear models; the default stays the published workflow. Full resolution: the width is the benchmark's feature-limit step's job.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: Andrej's keep with the raw spectra (2026-10-21) and the spectrum declaration (2026-11-02) settle it; only questions for the authors (the t marker, 10 missing control spectra) remain. Priority 1: gap 0, use case 0, source 1, shape 0, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on routine `Timeless` issues): the label is the mouse's genotype, fixed at birth, and its undated bleeds are held out with it. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the 73 mice gave 1 to 6 serum samples each (median 2, 29 one), the label is the mouse's, and the use case reads each sample of an unseen mouse as a new patient's test, so a mouse bled six times counts as six patients. Weighting each sample by 1 over its mouse's samples ranks 8 untuned models at Kendall tau 0.66 per split (lowest -0.07, on 24 test mice) and 0.86 for the ranking by the mean over 30 of the shipped splits, the same best model on 23 of 30, the largest shift of the scan. Open for Lennart as issue 1 of the record's Review; recommended: each mouse counts once (B), unless the use case is a person tested again and again; ROC AUC would first need an optional weight input.

CC (2026-11-08, Lennart): issue 5, B: each mouse counts once, as one patient. The ROC AUC weights a serum sample by 1 over its mouse's number of samples (`mouse_weight`, a scoring column for the metric only); each sample is still read on its own. The weight is for scoring only, never a `sample_weight`, also though it does not follow from the inputs (Lennart's rule of 2026-11-08, MET-15 amended, MET-17); the bundle warning accepted with that reason.

**Assessment (AI, 2026-11-08):** training with the weight does not help: it changes a regularised logistic regression's weighted ROC AUC by -0.015 (SE 0.006, lower on 39 of 60 grouped random splits). New checksum v2:bcf94742... (not built); `dataset check` 0 errors, 0 warnings.

CC (2026-11-08, Lennart): the declared metric (roc_auc, weighted by mouse_weight) is checked.

CC (2026-11-11, Andrej): `Selection Bias` marker; the controls were bled about a month older than the mutants (review issue 3, C).
- Hingorani et al. 2003, Table 2 (prospective study): mutants 5.5 ± 0.25 months (33 mice), controls 6.5 ± 0.2 months (39 mice), though the text calls them "aged-matched"; the pilot study, not in this download, was matched (9.4 against 9.0 months, Table 1). Re-read from the paper's PDF on the data page on 2026-11-11.
- The release has no age per bleed, so the share of the signal that is age cannot be measured; written into `curation_comments` and `fit_reason`.
- A third question for the authors, after what `t` marks and where the 10 control spectra went: the age of each mouse at each bleed.

CC (2026-11-12, Andrej): the age gap is `Selection Bias` only, neither a leak nor `Class-dependent Recording` (BeyondArena v0.2 review page, issue 4, A): both classes went through the same instrument, m/z grid, chips and number format, and no feature holds the age or the class. Revisit if the authors say the `t` marker is a separate recording route.

## Review

**Outcome:** added. The NCI-FDA Clinical Proteomics Program's serum mass spectra of the PanIN mouse study (Hingorani
et al. 2003, Cancer Cell 4(6):437-450, https://doi.org/10.1016/S1535-6108(03)00309-X; data at
https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp): 181 spectra of 73 mice, 6,771 intensity bins each, and
whether the mouse carries pancreatic intraepithelial neoplasia (PanIN, preinvasive lesions) or is a littermate control
(44% of the spectra); split by mouse, ROC AUC (fallback). The AI recommends shipping it as defined; Andrej's decision of
2026-10-21 (keep, with the raw spectra) and the spectrum declaration of 2026-11-02 settle issue 1. Reviewed on
2026-11-04 without a panel, from the gathered evidence (the record, the CHANGELOG, Andrej's earlier experiments, a
model run on the shipped data). Validity: the label comes from the folder (genotype), the file names' class code
never enters the features, and the mouse split removes the paper's sample-level overlap; the `t` file marker is no
measurement batch and the signal stays without the marked spectra (ROC AUC 0.63 against 0.66). Value: on the 60
shipped splits logistic regression beats shuffled labels (0.66 against a null mean of 0.51, 95th percentile 0.62); a
simple model on processed spectra (total-ion-current scaling, log, merged bins, sparse logistic
regression) reaches 1 - ROC AUC 0.251 against 0.334 for the best of 40 benchmark methods on raw bins (median 0.465),
which
is the gain the declared encoding hands to every method. Quality: 10 control spectra of the paper are missing from the
download and the meaning of `t` is unknown; both are questions for the authors. Weighed: a published study set with the
genotype as label +, a mouse-grouped split +, a weak but real signal +, a tiny high-dimensional task and open questions
on the files -.

**Main points:** Ship as defined (issue 1 resolved; the authors' answers on `t`, the 10 missing control spectra and
the age per bleed are still outstanding). The controls were bled about a month older: noted and marked `Selection
Bias` (issue 3, C, resolved 2026-11-11); neither a leak nor `Class-dependent Recording` (issue 4, A, resolved
2026-11-12; revisit if the authors say `t` is a separate recording route). The mouse split is named `Timeless`
(issue 2, resolved 2026-11-06). Issue 5 (Lennart, 2026-11-08): Resolved on 2026-11-08: each mouse counts once in the ROC AUC, weighted by 1 over its number of serum samples (issue 1).

**Record judgment:** valid, decided. Andrej's CC of 2026-10-21 holds the evidence and the to-do (ask the authors what
`t` marks and where the 10 control spectra went); Lennart's CC of 2026-11-02 the spectrum declaration. An earlier chat
read the paper's Table 2 as giving the controls a mean age about a month above the mutants' (6.5 against 5.5 months)
although the text calls them age-matched; it was not re-read for this review and belongs with the questions for the
authors. Two small definition fixes need no mark: `bibtex` holds the entry inside stray double quotes, and the accepted
`dataset_missing_value_sentinel` warning no longer fires (the check now skips spectrum bins; `dataset check` reports it
as unused). The data scouting found `debernardi_urinary_pancreatic_cancer` (human urine biomarkers for pancreatic
cancer); it is screened in its own record and does not change this task's validity.

**Issues for Andrej:**

1. **Keep the dataset, and ship the spectra raw or processed?**

   * **Problem:**
     - Andrej disputed Lennart's keep (2026-10-15): the signal is weak, the rows are mass spectra shipped before the
       usual spectral processing, and a file marker `t` of unknown meaning separates some control spectra.
     - Processing each spectrum without labels (smoothing, baseline removal, scaling to the total intensity) lifts every
       model, so the form the spectra ship in decides how the methods rank.
     - Keep it with the raw spectra declared as a spectrum, ship processed spectra, or retire it?
   * **Background:** a SELDI-TOF mass spectrum is a list of ion counts over mass-to-charge bins; each spectrum carries
     its own baseline (a slowly varying background) and overall intensity, which the field removes before analysis.
     The data page asks for "normalization, baseline correction, and alignment prior to any such analysis". A spectrum
     ships as the source publishes it and is declared as one, so a benchmark encodes it[^1a].
   * **Experiments:**
     - On the 60 shipped splits, raw bins against the declared default encoding (MALDIquant's square root,
       Savitzky-Golay smoothing, SNIP baseline, total ion current): TabPFN v3.5 0.659 to 0.690, LightGBM 0.577 to
       0.676, random forest 0.536 to 0.681, PLS-DA 0.635 to 0.691, logistic regression 0.663 to 0.646 (CHANGELOG,
       2026-11-02).
     - Logistic regression on raw bins 0.66 against 200 mouse-level label shuffles (mean 0.51, 95th percentile 0.62,
       p about 0.01); 0.63 without the 66 `t` spectra; run numbers and chip positions show both classes and both
       markers measured mixed on the same chips (Andrej, 2026-10-21).
   * **Consistency:** prostate_cancer_detection, from the same NCI-FDA data bank, was retired for batch artefacts across
     its features; here no batch separates the classes, so it does not carry.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Raw spectra, declared (implemented) | 6,771 raw bins as published, declared `Spectrum(state="raw")` with the MALDIquant default encoding | the data as published; every method gets the field's processing | the score depends on the benchmark applying the encoding |
     | B | Processed spectra in the data | the processing done in `_clean` | models see processed spectra without a declaration | departs from shipping data as published; one processing chain fixed for all |
     | C | Retire | `No (Retired)` | removes a tiny, weak task | loses a real, grouped, high-dimensional task whose signal beats shuffled labels |

   * **Recommendation:** A, as decided: the data stays as published and the field's processing reaches every method
     through the declaration. **Decision:** raw and declared (A), processed in the data (B) or retire (C)?

   **Resolved (2026-10-21, Andrej):** (A), keep with the raw spectra; the processing belongs to the evaluation
   pipeline (PR #21). Lennart declared the serum spectrum as a spectrum on 2026-11-02, with MALDIquant's
   steps as the recommended encoding. Open for the authors: what `t` marks and where the 10 control spectra went.

   [^1a]: **CLEAN-26** (Should): a spectrum ships as the source publishes it, one numeric column per position on its
     axis, and is declared as a spectrum, never processed in the data.

2. **Time basis: name the mouse split `Timeless`?**

   * **Problem:**
     - The label is the mouse's genotype (compound mutant or littermate control), fixed at birth, and each of its 1 to
       6 serum spectra comes from a bleed at least 5 days after the last one; no bleed date or age ships, and the raw
       order follows the two class folders, not time (the time probe's only flag).
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits a designed study whose
       only time order lies within each mouse; the split holds out whole mice and names no time basis yet.
     - A genotype is a fixed property of the mouse, the case the `Timeless` prototype names[^2a].
   * **Background:** the lesions the genotype stands for grow with age (a third of the ducts diseased at 5.5 months,
     Hingorani et al. 2003), so a young mutant's serum may show little; that is label noise of the design, not time
     reaching the label through other rows. All bleeds of a mouse are held out together, so no later bleed informs an
     earlier one. The classes were bled at different ages (issue 3), a question of its own.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Mouse split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Mouse split, `Timeless` | as now; the tag and a `Time basis:` line naming the genotype and the bleeds held out together | states the fact the split rests on | none found |

   * **Recommendation:** B: the label is fixed at birth and the serial bleeds stay with their mouse. **Decision:** A
     or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: the label is the genotype, fixed at birth; each mouse gave 1 to 6 bleeds
   at least 5 days apart, undated, all held out with the mouse (Hingorani et al. 2003).`, `splits_comment`
   unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts (a time order found only within each entity does not count as dated), and a definition
     can name the use-case prototype it follows with a `Time basis:` line. `Timeless`: the target is a fixed property
     of the item, the same whenever it is measured; the split is random or grouped by item family.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (mice of another cohort, or spectra from another instrument run); the split and `data_tags` are
   unchanged. The tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

3. **Write down that the controls were bled about a month older than the mutants, and mark it?**

   * **Problem:**
     - The paper's Table 2 gives the prospective study's mutants an average age of 5.5 ± 0.25 months (33 mice, 95
       samples) and the controls 6.5 ± 0.2 months (39 mice, 125 samples), although its text calls the controls
       "aged-matched".
     - The classes were therefore bled at different ages, so a serum change with age can separate them as well as the
       lesions; nothing in the definition says so, and the record judgment still calls the gap an unverified reading.
     - Write it into the notes, also set the `Selection Bias` marker, or retire?
   * **Background:** the pilot study, which this download does not hold, was matched (9.4 ± 0.3 against 9.0 ± 0.2
     months, Table 1). The release has no age per bleed, and the mouse numbers do not settle it (controls' median
     4,580 against 4,804, Mann-Whitney p = 0.11, and their order is not documented). Paper:
     <https://home.ccr.cancer.gov/ncifdaproteomics/pdf/cancercell-panin.pdf>, Table 2 and "Serum proteomics".
   * **Effect on the task:** part of what separates the classes may be the extra month of the controls rather than
     the lesions; the signal is weak (logistic regression ROC AUC 0.66 against 0.51 for shuffled mice), so even a
     small age effect is a real share of it. The mouse grouping cannot remove it, since the age gap runs between the
     classes, not within a mouse.
   * **Unknown:** each bleed's age; the authors, already asked about `t` and the 10 missing control spectra, could
     give it, and then the age could be matched or measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nothing written (implemented) | as now | none | a known difference in how the classes were sampled stays undocumented |
     | B | Note it | a curation bullet and a clause in `fit_reason` with Table 2's ages; the age per bleed added to the questions for the authors | the user knows the classes differ in age; the mildest fix | no flag on the dashboard |
     | C | Note it and mark it | as B, plus the `Selection Bias` marker on the record | the marker's own case, cases and controls collected apart; visible next to the verdict | one more marker on a kept dataset |
     | D | Retire | `No (Retired)` | removes a possibly confounded weak signal | the confound is one month in adult mice and unmeasured; the keep of 2026-10-21 stands on other evidence |

   * **Recommendation:** C: the age gap is a fact of how the classes were sampled, which is what the marker records[^3a],
     and the note says how large it is; it cannot be measured until the authors give the ages. **Decision:** A, B, C
     or D?

   **Notes for the AI:** on B or C, a curation bullet: "The classes were bled at different ages: mutants 5.5 ± 0.25
   months, controls 6.5 ± 0.2 months (Hingorani et al. 2003, Table 2), though the text calls them age-matched; the
   release has no age per bleed, so the share of the signal that is age cannot be measured." `fit_reason` adds "the
   controls were bled about a month older". The record's CC line names the age as a third question for the authors;
   on C, `Selection Bias` in `decision_markers`; `Andrej` in `checked_by`; `dataset check`.

   [^3a]: Selection guidelines, "Selection bias" (Andrej, 2026-10-20; Lennart, 2026-10-27): when the rows are not
     drawn from the population the use case predicts for, such as cases and controls collected apart or in different
     periods, mark it `Selection Bias`, name the gap in `fit_reason` and judge the model comparison on the data; the
     verdict is usually still `Yes`.

   **Andrej (2026-11-11, discuss):** We should definitely mark it as selection bias, but is that also a leak and a
   outcome specific recording?

   **Answer (AI, 2026-11-11):** marked; neither a leak nor class-dependent recording on the evidence so far. The
   question is a decision of its own, issue 4.

   **Resolved (2026-11-11, Andrej):** C ("We should definitely mark it as selection bias"): `Selection Bias` in the
   record's `decision_markers`; a curation bullet with Table 2's ages (re-read from the paper's PDF today: mutants
   5.5 ± 0.25 months, controls 6.5 ± 0.2, text "aged-matched"; pilot matched at 9.4 against 9.0) and why the share of
   age cannot be measured; `fit_reason` adds that the controls were bled about a month older; the record's CC line names
   the age per bleed as a third question for the authors. Data unchanged; `dataset check`: 0 errors, 0 warnings (1 info, the known unused accepted warning).

4. **Is the age gap also a leak, or `Class-dependent Recording`?**

   * **Problem:**
     - The age gap is in which mice were bled when, not in how their spectra were recorded: both classes went through
       the same instrument, grid and chips, and no feature holds the age or the class.
     - A leak needs a feature that carries the label or comes after the prediction point; here the label comes from the
       folder, the file names' class code never enters the features, and a serum change with age is biology of the
       sampled mice, a confound.
     - `Class-dependent Recording` needs the classes measured, formatted or filled differently; its rule says
       "`Selection Bias` is about which rows were sampled, with the measurements alike"[^4a].
   * **Experiments:** the files by class (pandas, no model; chips from the record's CC of 2026-10-21):

     | Check | Mutants | Controls |
     |---|---|---|
     | Spectra | 80 | 101 |
     | Bins, grid | 6,771, same m/z | 6,771, same m/z |
     | Number format | one decimal throughout | one decimal throughout |
     | Chips and runs | mixed with controls on the same 8-spot chips | mixed |
     | `t` marker | 24 (30%) | 42 (42%) |
     | Total ion current, median | 3.80 M | 3.48 M |

     - The overall intensity is not the signal: scaling each spectrum to its total raises logistic regression from 0.66
       to 0.74 ROC AUC.
     - The one open point is `t`: unequal by class, it separates control spectra from each other (0.67) and marks about
       half the bleeds of mice bled several times, so it may be later bleeds, which is age again; without the `t`
       spectra the signal stays (0.63 against 0.66).
   * **Unknown:** what `t` marks; if the authors name a separate processing or recording route, the recording rules
     apply after all.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Selection Bias` only (implemented) | as now | names what is known: a sampling gap, the measurements alike | none found |
     | B | Also `Class-dependent Recording` | the marker, a CC line | flags `t` before the authors answer | no recording difference shown; the marker's rule excludes a sampling gap |
     | C | Treat as a leak, retire | `No (Retired)` | removes a possibly confounded weak signal | no feature carries the label; the age effect is unmeasured |

   * **Recommendation:** A; revisit B if the authors say `t` is a separate route. **Decision:** A, B or C?

   **Notes for the AI:** on B, `Class-dependent Recording` in `decision_markers`, a CC line naming `t` as the reason
   and that no format or grid differs. On C, `No (Retired)` with the marker, the folder stays until a retirement PR.

   [^4a]: leak_checks.md, "Artefacts that differ by class" (LEAK-13 to LEAK-15, LEAK-39, LEAK-40): the marker
     `Class-dependent Recording` says the classes were measured, formatted or filled differently, so the recording can
     give the label away; `Selection Bias` is about which rows were sampled, with the measurements alike.

   **Resolved (2026-11-12, Andrej):** A (`ok` on the recommendation): `Selection Bias` only, as implemented; no
   `Class-dependent Recording` marker and no retirement, since both classes share instrument, grid, chips and number
   format and no feature carries the age or the class. Revisit B if the authors say `t` marks a separate recording
   route. Record CC line; nothing else changed.

5. **Count each mouse once in the ROC AUC, or each serum sample, as now?**

   * **Problem:**
     - A row is one serum spectrum, and the 73 mice gave 1 to 6 samples each (median 2, 29 mice one), so a mouse bled six times counts six times in the ROC AUC.
     - The label is the mouse's (PanIN or control), and the use case reads each sample of an unseen mouse as "a new patient's test", so one mouse stands for up to six patients.
     - Should each sample weigh 1 over its mouse's number of samples in the score, so that each mouse counts once while each sample is still read on its own?
   * **Background:**
     - 181 spectra: 80 of 35 PanIN mice and 101 of 38 control mice; the largest 10% of the mice hold 25% of the
       spectra. The release gives no bleed dates; the paper says the bleeds were at least 5 days apart.
     - Unlike superconductivity and boreal_postfire_lichen_biomass, the inputs differ between a mouse's samples (each
       bleed has its own spectrum), so a model gives each sample its own score; the weight changes only how much each
       sample counts.
     - Weighted this way, the ROC AUC is the chance that a random sample of a random PanIN mouse scores above a random
       sample of a random control mouse.
     - One prediction per mouse from all its samples would change the use case (a test from one serum sample) and is
       not proposed.
   * **Rules:** the use case decides at which unit the score counts[^pc-unit]. The rules ask for the score weight to be
     the training weight when it is a realized amount at risk, and waive that when it follows from the inputs[^pc-weight];
     this weight is neither, so B accepts the check's warning with a reason the rules do not name yet (a weight that
     gives each unit one vote).
   * **Effect on the task:** per sample, a mouse bled often decides more of the score; per mouse, each animal, the
     study's stand-in for a patient, counts once. With about 24 test mice per fold, a mouse with five or six samples
     moves a fold's AUC more per sample than per mouse.
   * **Experiments:** the scan of 2026-11-08, 8 untuned predictors (two logistic regressions, random forest, extra
     trees, two LightGBM, kNN and the class shares) on 30 of the shipped splits, on the raw spectrum standardized per
     bin (not the recommended encoding).
     - The weighted score ranks the models like the per-sample one at Kendall tau 0.66 per split on average (lowest
       -0.07, on 24 test mice) and 0.86 for the ranking by the mean over the splits; the same best model on 23 of 30
       splits. Kendall tau measures how far two orders of the models agree, 1 when they are the same.
     - In the ranking by the mean, two pairs swap, both near ties: the two LightGBM (ROC AUC 0.582 and 0.579 per
       sample) and kNN against the class shares (0.4999 and 0.5000 per mouse). The logistic regression leads under both
       (0.665 per sample, 0.644 per mouse).
     - The largest shift of the scan (boreal_postfire_lichen_biomass: 0.81 per split, 0.86 for the mean).
   * **Consistency:**
     - boreal_postfire_lichen_biomass counts each plot once since 2026-11-08[^pc-boreal]; there every input belongs to
       the plot, here only the label belongs to the mouse.
     - micro_mass counts each strain once in its score (1 to 6 spectra per strain); musk and
       fraud_detection_in_electricity_and_gas_consumption_1m predict once per group, a different use case.
     - The same scan raised superconductivity (per composition) and dementia_prediction (per person).
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per sample (implemented) | ROC AUC over all spectra | fits a person tested again and again, each test a decision; nothing changes | a mouse counts by how often it was bled, up to six times |
     | B | Each mouse counts once | ROC AUC weighted by 1 over the mouse's samples, a scoring column for the metric only; ROC AUC first gets an optional weight input | one vote per animal, the unit that stands for a patient; the pattern boreal follows | a framework change; the check's warning accepted with a reason the rules do not name yet; on 24 test mice the per-split ranking stays noisy |

   * **Recommendation:** B, since the use case reads each mouse as a new patient; A if the use case is a person tested
     again and again, each test a decision, and then the use case says so. **Decision:** A or B?

   **Notes for the AI:** on B: (1) `roc_auc` takes no `weight` today; give it an optional row weight in
   `src/data_foundry/v2/metrics.py` (scikit-learn's `sample_weight`, `optional_inputs=("weight",)`,
   `weighted_definition` so the unweighted spec and the built containers' checksums stay unchanged), with a test, as
   `rmse` got for boreal; (2) in `_load_raw`, add `mouse_weight`, 1 over the mouse's number of samples
   (`1.0 / df.groupby("mouse_id")["mouse_id"].transform("size")`), declared as
   `ScoringColumn(column="mouse_weight", role="weight", used_by="roc_auc", ...)`; (3)
   `Metric.fallback(reason=..., inputs={"weight": "mouse_weight"})`, the reason adding that each mouse counts once;
   no `sample_weight`; (4) accept `task_metric_weight_without_sample_weight`: a design weight of the score that gives
   each mouse one vote (SPLIT-23), not an amount at risk (MET-15) nor a survey weight (MET-16); it does not follow
   from the inputs, so the main session adds this reading to MET-15 (or, if the curator prefers, declares it as the
   `sample_weight` too); (5) the grouping's definition and the task summary's `split` keep "each sample read on its
   own" and add the weighting; `dataset check`, the CC line, a CHANGELOG entry, a Cases row in metrics.md. On A:
   reword the use case so that each test sample is one test of a person tested repeatedly, and add a note that a
   mouse counts by its number of samples (tau 0.66 per split against one vote per mouse).

   [^pc-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group). **MET-1** (Must): the declared metric scores the real task, at the unit the actor acts on.
   [^pc-weight]: **MET-15** (Must): a realized denominator is the metric's row weight and the task's sample weight; a
     metric weight that is a function of the features needs no sample weight, and the bundle check
     `task_metric_weight_without_sample_weight` is then accepted with that reason. **MET-16** (Should): a survey or
     design weight is never a feature, and the task is scored unweighted unless the use case is a population estimate
     (boreal's `plot_weight` was read as no such weight: it is ours, not the source's).
   [^pc-boreal]: boreal_postfire_lichen_biomass, issue 7, Lennart, 2026-11-08: "Option B: Each plot counts once."

   **Lennart (2026-11-08, change):** Option B: Each mouse counts once.

   **Resolved (2026-11-08, Lennart):** B, each mouse counts once. `roc_auc` got an optional `weight` input, and the
   ROC AUC is weighted by `mouse_weight`, 1 over the mouse's number of samples, a scoring column for the metric only
   with no training weight (Lennart's rule of 2026-11-08: a one-vote weight is for scoring only, also when it does not
   follow from the inputs; training with it measured -0.015 ROC AUC). Each sample is still read on its own; the use
   case now says each mouse counts once, as one patient.

## Reference

@article{hingorani2003preinvasive,
  title={Preinvasive and invasive ductal pancreatic cancer and its early detection in the mouse},
  author={Hingorani, Sunil R and Petricoin, Emanuel F and Maitra, Anirban and Rajapakse, Vinodh and King, Catrina and Jacobetz, Michael A and Ross, Sally and Conrads, Thomas P and Veenstra, Timothy D and Hitt, Ben A and others},
  journal={Cancer cell},
  volume={4},
  number={6},
  pages={437--450},
  year={2003},
  publisher={Elsevier}
}
