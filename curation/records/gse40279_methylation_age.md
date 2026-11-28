---
unique_name: gse40279_methylation_age
name: GEO-GSE40279-Methylation-Age (Blood DNA Methylation Age)
checked_by:
- Andrej
suggestion: 'Yes'
priority: 2
tags:
- Many features
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- TabBench-Bio
original_source: Other
year: '2012'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1016/j.molcel.2012.10.016
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279
- https://arxiv.org/abs/2609.07441
v2_path: datasets/_dev/tabarena-v0pt2/gse40279_methylation_age/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 2: chronological age from whole-blood 450K methylation of 656 people (Hannum et al. 2012), the cohort behind a standard epigenetic clock, published with a predictive model validated on a second cohort; a larger blood cohort with age (GEO GSE55763, 2,664 people) is better data for the same task.
- Source: Hannum, Guinney, Zhao et al., "Genome-wide Methylation Profiles Reveal Quantitative Views of Human Aging Rates", Mol Cell 49(2):359-367, 2012 (https://doi.org/10.1016/j.molcel.2012.10.016, read on PMC3780611); data GEO GSE40279, public 2012-11-21. As published: 656 samples, one per person, x 473,034 probes of average beta (BeadStudio v3.2; the paper's QC subset of the 485,577 manifest probes), with `age (y)` (19-101), `gender`, `ethnicity`, `source` (UCSD 304, Utah 178, USC 139, Boston 35) and `plate` (9 plates). Files: series matrix, average betas, signal intensities (5.0 GB); `RAW.tar` holds only the manifests, no IDATs (size check of 2026-11-08 on PR #67). TabBench-Bio keeps 30,000 complete probes picked by probe-ID hash.
- Use case: a study reading the residual as an aging rate, or a lab estimating the age of a blood donor; the paper names both ("from health assessment and prevention of disease to forensic analysis", Conclusions); fit direct for age estimation from blood. Collection: volunteers' blood measured once by a study protocol, no date per sample, age a fixed fact at the draw (`Samples: No Time Dimension`, no target tag); one row per person. Type Experimental Results (SPLIT-34 rule 5; as `biogeographical_ancestry_prediction`).
- Split: leaf L-PLACE.groups (Grouped · `UnseenGroup` (groups)) because [EXP.meets] is another laboratory, site or cohort (a clock is applied to samples run elsewhere; the paper validates on a second cohort, "two different cohorts (N1 = 482, N2 = 174)", which the GEO sites UCSD + Utah and USC + Boston match), and [PLACE.several] is yes (4 sites, 9 plates); open: the group key, plate or site (the enough-groups check: 4 sites, 2 cohorts), and plate and site confounded with age and ethnicity (plate means 38.5 to 76.2 years; USC 138 of 139 Hispanic).
- Siblings and duplicates: no other record on this branch holds GSE40279; `skull_bone_molecular_age` is the same quantity from another tissue (PROV-7); GSE207605 re-analyses it with `gse42861_rheumatoid_arthritis_methylation` and `gse147221_schizophrenia_methylation`. On the open large-datasets PR (#67) this record carries Lennart's `Yes` (2026-11-08) and a review panel (2026-11-09), not on this branch. External collections: TabBench-Bio (Table 4).
- Better data: GEO GSE55763 (Lehne et al., Genome Biology 2015, Imperial College London, public 2015-01-22, https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55763): 2,664 people, 2,711 peripheral-blood 450K arrays, `age` 23.7-75.0 and `gender`; 4 times the people and newer, a narrower age range (no one over 75, against 19 to 101 here); its record `gse55763_methylation_age` exists on PR #67, not on this branch.
- Papers and pages: Hannum et al. 2012 (above); Varshavsky et al. 2023 (GSE207605) trains on it; TabBench-Bio registry `GEO-GSE40279-Methylation-Age`.
- Metric: Hannum reports two criteria side by side, a correlation of 96% and "an error of 3.9 years" (section "A predictive model for the aging methylome"), the error unnamed; no single deliberate one, so the fallback `rmse` in years (MET-5, MET-8). Inputs: the group (plate or site) for the split, a sample characteristic that ships, never a feature.
- Risks for /add-dataset: plate and site confounded with age and ethnicity (the group from the use case, SPLIT-3); betas processed over all samples and missing cells KNN-imputed over all samples per the paper (LEAK-30, weak; the rebuild route is the signal-intensity file, PROV-13); 473k probes, no subset chosen on the target (CLEAN-22, LEAK-31); an ultra-wide table may need library changes to build.
- Priority: gap 0 (biology & life sciences 10, regression and grouped not thin), use case + (the paper names the uses), source + (paper and documented GEO characteristics), shape 0 (656 rows), risk - (better data found: GSE55763).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 656 x 30,000 (of 473,034 probes); target: age (y).
- Why: Chronological age from whole-blood 450K methylation (Hannum epigenetic clock cohort)
- Notes: CV grouped by 9 assay plates (plate-age imbalance).

**CC (2026-11-25, Andrej):** accepted for adding, after the re-screening of the TabBench-Bio candidates on the current rules.
- Added with `/add-dataset`; the open points go into this record's `## Review`.

**Assessment (AI, 2026-11-25):** review panel (full tier, 11 roles): ship after changes, with the mediator's nine settled changes applied (the use case rewritten on the clock builder who chooses a model by held-out error, `ethnicity` dropped as an exact coarsening of the plate key, the split's stated grounds replaced by the pseudo-plate experiment that separates batch from cohort, the Sentrix lot finding, the 304 measured cells that ship as missing, both check warnings accepted in writing, and the metric reason rewritten to say where we looked); disputed: how far the published-clock contamination is declared (an evaluation-level leak kept with a note, LEAK-9, whose carrier the rules on another party's model put out of reach, EV-4 and PROV-15, and which the supervised-output rule does not reach, LEAK-27) and the metric (the metric the task makes obvious against the fallback, MET-11); for the curator: issues 1-5. Two items went to the working copy's cross-dataset file instead of this record: the amendment for a measured overlap with another party's model, and the wide-parquet reader fix, which blocks any build of this folder. Priority 2: gap 0, use case +, source +, shape 0 (656 rows), risk - (two published clocks fitted on these rows' labels, which no check can detect, and a larger, newer cohort found for the same task).

**CC (2026-11-26, Andrej):** the review decisions on the five open issues; all five are settled.
- Issue 1, change to C: the published-clock contamination is declared with the full note and a protocol line. The definition's notes name Hannum et al. 2013 and Lin et al. 2016, the measured numbers (best honest 5.279, Hannum alone recalibrated 4.949, honest + Hannum + Lin 4.645, honest + all five 4.487, the external-clock control +0.115, an honest refit on Hannum's own 71 sites 5.299), that no definition change removes it, that nothing detects it, and the revisit condition; the protocol line says an entry must not use a model fitted on this series and that the bound is declared because it cannot be enforced. `fit_reason` names the leak and the floor; the fit stays `direct`.
- Issue 2, as implemented: `ethnicity` stays dropped, as an exact coarsening of the plate key; `sex` stays.
- Issue 3, as implemented: the plate key stays, with the measured batch as the record of its departure and no separate exception line.
- Issue 4, change to B: the declared metric becomes `mae` in years with origin `context`, the paper's undefined "error of 3.9 years" as the original and the field's reporting convention as the context (clock MAE 4.57 and median AE 3.58 against RMSE 6.14). The errors in years measured elsewhere in the definition are RMSEs and are now labelled as such. `dataset check` has not been re-run for this change, so the generated README is stale against `dataset.py` and still shows the `rmse` fallback until it is.
- Issue 5, as implemented: both check-warning acceptances stand with `plate` as `int64`, and the three documentation facts stay; the `groups_test_groups_few` acceptance now names its metric alongside the new declared one.

**CC (2026-11-26, Andrej):** the declared metric and the declared split are signed off and the verdict is ship.
- Verdict: ship. Every issue of the review is resolved, no record field disagrees with the definition, and nothing is parked; the record's `Yes` stands and the dataset joins the accepted set, to be built later.
- The declared metric is checked as it stands: `mae` in years, origin `context`, with the paper's unnamed "error of 3.9 years" as the original (the sign-off line below).
- The declared split is checked as it stands: whole assay plates held out, 20 repeats of 3 folds (the sign-off line below).
- No change to `dataset.py` and no `dataset check` was run: the deferred check of this folder (656 x 473,037) is still outstanding, so the generated README stays stale against the definition and still shows the `rmse` fallback, as the review already records.

CC (2026-11-26, Andrej): the declared metric (`mae` in years, from context, with Hannum et al.'s unnamed "error of 3.9 years" as the original and the field's reporting convention as the context) is checked and stays as declared.

CC (2026-11-26, Andrej): the declared split (grouped on `plate`, 20x3 folds, `UnseenGroup`) is checked and stays as declared: a clock is applied to blood measured in a batch the model never saw, the nine plates are every batch the series has, and the key is the measured level of the batch (a test row never keeps its own plate in training, while holding out BeadChips or Sentrix lots costs almost nothing).

## Review

**Outcome:** added. Hannum et al.'s GEO series as deposited, rebuilt from BeadStudio's own signals: 656 whole-blood
450K samples, one person each, 473,034 probes, chronological age 19 to 101, with whole assay plates held out. A full
review panel ran (eleven roles: seven evidence agents, an advocate and a critic with one rebuttal each, a mediator and
the review editor); both sides reached ship after changes, and everything the panel settled without a decision is
applied. Validity holds: the authors' KNN imputation is undone from the origin (BeadStudio's formula reproduces the
deposit to 3.14e-07 over 318,108,009 cells), `ethnicity` is dropped as an exact coarsening of the group key, the use
case is rewritten on the actor who predicts something (the clock builder, the fit stays direct), and the split's
stated grounds are replaced by the experiment that decides the key. Value holds: four model families beat the dummy on
all 60 splits and shuffled ages on none of them over three seeds, the best honest model errs 5.279 years against a
constant's 16.065, and a tuned method still takes about 1.6 years off the best single probe. The one thing nothing in
the table carries is a leak that is now kept on purpose and declared: two published clocks were fitted on the ages of
these very rows, their coefficients are public, and recalibrating one of them beats every honest model measured here,
with no check able to detect its use, so the notes carry the mechanism, the numbers and a protocol line (issue 1).
Weighed: use case +, source +, provenance +, gap 0, size - (656 rows), contamination - (bounded and
measured). Blocker: nothing is built until the wide-parquet reader fix of the working copy's cross-dataset file lands,
because the container cannot be read by the call the collection documents.

**Main points:** All five decisions are settled (2026-11-26): the clock contamination is declared with the full note
and a protocol line (issue 1), `ethnicity` stays dropped and the plate key stays on its measured batch (issues 2 and
3), the metric becomes `mae` in years under the context origin (issue 4), and the two check-warning acceptances stand
(issue 5). Nothing is left to decide: on the same day the declared metric and the declared split were signed off and
the verdict set to ship, with the folder's own check still deferred, so its README stays stale against the
definition.

**Record judgment:** valid. The screening read the source correctly, and the build met the risks it named: the KNN
imputation (undone), the plate and age confound (the split key), the width (shipped), and the better data it found
(GSE55763, weighed in issue 1 and still its own record's call). Two of its readings are superseded by measurement: the
use case it gives, a study reading an aging rate, has no actor who predicts anything, and the aging-rate residual is
not clean; and its metric line, the `rmse` fallback, is superseded by the curator's `mae` under the context origin
(issue 4). The record's
fields agree with the definition and none needs a mark.

**Issues for Andrej:**

1. **Declare the published-clock contamination, and how far?**

   * **Problem:**
     - Two published epigenetic clocks were fitted on the ages of these very rows, their coefficients are public, and
       every site they use is in our table[^clocks].
     - Pasting 71 public numbers into a dot product and recalibrating it per split beats every honest model measured
       here, with no learning on our features at all.
     - Nothing in the table carries it, no change to the definition removes it, and no check can detect its
       use[^carrier].
   * **Effect on the task:** a leaderboard entry is bounded below at about 4.9 years with no modelling at all, and
     the gain from stacking the clocks on an honest model, 0.791 years, is more than the whole spread of the honest
     ridge's feature sweep (5.279 to 6.059) and about 70% of the distance from ridge to gradient boosting, so model
     families would reorder on who fetched the weights; the fit stays direct, because a leak kept on purpose does not
     by itself make a fit approximate[^fit].
   * **Experiments:** mean RMSE in years over the 60 shipped splits; the last column says whether the published model
     was fitted on these rows' ages.

     | model | RMSE | fitted on these 656? |
     |---|---|---|
     | best honest (ridge, fold-honest top-5000, z-scored) | 5.279 | no |
     | honest elastic net, the published clock recipe (12 splits; ridge 5.280 there) | 5.428 | no |
     | Hannum alone, recalibrated per split, no honest model at all | 4.949 | yes |
     | Lin alone, recalibrated | 5.517 | yes |
     | Horvath v1 alone, recalibrated (the best external) | 5.976 | no |
     | honest + Hannum + Lin | 4.645 | mixed |
     | honest + all five clocks | 4.487 | mixed |
     | control: honest + the three clocks fitted elsewhere | 5.163 | no |
     | honest refit on Hannum's own 71 sites (masking does not work) | 5.299 | no |

     The control isolates 0.4 to 0.68 of the 0.791 years as label information rather than better modelling, and the
     contrast holds for single clocks: the only one that beats the honest baseline alone is Hannum, one of the two
     fitted on these labels. Every one of the 60 test folds holds rows Hannum was fitted on, on average 75%, at least
     40%.
   * **Consistency:** the one comparable kept exploit, `medical_facility_operational_data`, was kept with a protocol
     line and a benchmark-side check, because there a model that learns from the test block can be seen; here no check
     exists, which is the fact that sets this case apart and the reason the declaration has to carry more
     weight[^medfac]. The remedy ladder lands on keep with a note, because nothing in the data can be repaired and
     exclusion is for a rule that cannot be fixed[^ladder].
   * **Panel:** the critic opened at "do not ship as a fitting task" and withdrew it after the blind reviewer matched
     archive samples to our rows at max abs diff 0.0, which makes the plain label-lookup route (RMSE 0) dominate the
     clock route; the advocate accepted every number and the naming of the clocks, and both ask for the declaration,
     differing only on the protocol line.
   * **Unknown:** whether this series is in Horvath v1's fitting set; it is treated as external because it behaves
     like the other external clocks (recalibrated 5.976, no gain alone), and if it were fitted on these samples the
     leak share rises and the control weakens.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as it is (implemented) | ships the table with no leak note and nothing in `fit_reason`, so the shipped dataset's leaderboard is floored at about 4.9 years by a public dot product nobody is told about | nothing to write | both sides rule it out; the exploit reaches the leaderboard unannounced, and honest participants are the ones who trip it |
     | B | A note only | ships the same table with a kept-leak note carrying the mechanism, the clocks by name, the numbers, the floor, that nothing detects it and when to revisit; the floor named in `fit_reason` | states everything measured; the shape we use for a kept leak elsewhere | leaves the norm unwritten for a participant who reads only the task card |
     | C | Note plus a protocol line | ships B's table and note, plus one line that a submitted model may not use coefficients fitted on these samples, with the admission that it is unenforceable | turns an invisible norm into a written one; follows the one comparable precedent | an unenforceable line can read as a false assurance |
     | D | C plus a benchmark-side entry | C, plus an item asking the benchmark to flag submissions whose predictions track the Hannum clock beyond an honest model's | the only detection route anyone named | weak by construction: a stacked clock is invisible in a prediction vector, so it would catch only the careless |
     | E | Evaluation-only set | score this series as a held-out validation set for clocks instead of a fitting task | removes the exploit by removing the fitting task | not a shape this collection has: containers ship splits and we fit on them |
     | F | Retire in favour of GSE55763 | drop this cohort for the 2,664-person Lehne series, which postdates both contaminating clocks | four times the people, newer | a different study, not a version this source defines; nobody over 75, exactly the band where this clock is most biased (-4.40 years at 80 to 101); the same contamination check has not been run on it; adding it is its own record's call |

   * **Recommendation:** C, with the note carrying the eight parts in the notes below, and D raised separately as a
     benchmark item rather than a condition of shipping. F stays a candidate of its own rather than a substitute.
     **Decision:** which option, and does the note carry all eight parts?

   **Notes for the AI:** on B or C the note is a `Potential leak, kept on purpose:` bullet in `curation_comments`
   stating, in this order: (i) Hannum et al. 2013 (71 CpGs) and Lin et al. 2016 (99 CpGs) were fitted on the ages of
   these 656 samples, 482 of them in Hannum's primary cohort, their coefficients are public and all their sites are in
   our table; (ii) every one of the 60 test folds holds such rows, on average 75%, at least 40%; (iii) the numbers of
   the table above, with the external control as the thing that identifies the gain as label information; (iv) the
   floor, about 4.9 years with no model of our features; (v) that no change to the definition removes it, because the
   leak is in the weights and not in the site list; (vi) that no check can detect its use; (vii) a warning for the
   second reader, that anyone using this series to validate a new clock will reach for Hannum's published predictions
   as the comparison and on these rows they are not honest; (viii) the revisit condition, that if the collection ever
   scores predictions it did not fit itself the note is not enough and the dataset is re-examined. `fit_reason` then
   names the leak as kept and states the floor; the fit stays `direct`. On C the protocol line goes in the same
   bullet. On D the benchmark item goes into the working copy's `BENCHMARK_CHANGES_TODO.md`, as the comparable
   precedent's check did.

   [^clocks]: Hannum et al., Mol Cell 49(2):359-367, 2013, "A predictive model for the aging methylome"
     (https://doi.org/10.1016/j.molcel.2012.10.016); Lin et al. 2016 on the same series; the coefficients of both
     ship in a public Bioconductor data package.
   [^carrier]: **EV-4** (Must) and **PROV-15** (Must): another collection's version of the data, pretraining overlap
     and other benchmarks' scores never change a decision, "they are no evidence". **LEAK-27** (Must) reaches "a
     feature that is the output of a supervised transform fit on the whole labelled set", a column in our table; the
     column audit flagged none of the 473,036 columns it saw, counted before `ethnicity` was dropped (the table now
     ships 473,037 columns, 473,035 features). Whether the first pair of rules should be amended for a measured case
     is the cross-dataset item of the working copy's `REVIEW.md`; under either reading this dataset ships with the note.
   [^fit]: **USE-8** (Must): "A potential leak kept on purpose does not by itself make a fit approximate, however much
     signal it carries ... the fit is that of the task without the leak, and the leak is named in the notes and in
     `fit_reason`".
   [^medfac]: **LEAK-9** (Should; amended 2026-11-05, Lennart, on `medical_facility_operational_data`): an
     evaluation-level leak is fixed in the scoring or by a protocol line in the definition "and the benchmark checks
     models for it (2026-11-04, Lennart: 'we can check if the model cheats')".
   [^ladder]: principles, "The remedy ladder": repair from the origin, fix the definition, keep it with a documented
     note, exclude; "Exclusion is for a Must that cannot be fixed."

   **Andrej (2026-11-26, change):** Option C: Note plus a protocol line.

   **Resolved (2026-11-26, Andrej):** C. The definition's `curation_comments` now carry a `Potential leak, kept on
   purpose:` bullet with all eight parts: the mechanism, Hannum et al. 2013 (71 CpGs, 482 of these samples its
   primary cohort) and Lin et al. 2016 (99 CpGs) by name with their public coefficients; that every one of the 60
   test folds holds rows they were fitted on, on average 75% and at least 40%; the measured numbers (best honest
   5.279, Hannum alone recalibrated 4.949, honest + Hannum + Lin 4.645, honest + all five 4.487 for a gain of
   0.791, the external-clock control +0.115 at 5.163, and an honest refit on Hannum's own 71 sites 5.299, so
   masking the sites does not work); that no change to the definition removes it, because the leak is in the
   published weights and not in the site list; that no check can detect its use; the warning to the second reader
   who would compare against Hannum's published predictions; and the revisit condition, that the note is not enough
   once this collection scores predictions it did not fit itself. The protocol line is in the same bullet: an entry
   must not use a model, or coefficients, fitted on the ages of these 656 samples, and the bound is declared rather
   than enforced, because nothing in the data or in a submitted prediction shows it was crossed. `fit_reason` names
   the kept leak and the floor of about 4.9 years; the fit stays `direct`. Option D, the benchmark-side check, was
   not part of this decision and stays a separate item.

2. **Drop `ethnicity`, as applied?**

   * **Problem:**
     - Each of the nine plates holds exactly one ethnicity, so the column is a deterministic two-level coarsening of
       the group key and hands a model back part of what the split withholds[^leak33].
     - What it carries is measured to be the study's recruitment design, not biology.
     - The definition already drops `site` because it names a cohort a new sample is not from, which is the same thing
       said of a coarser key.
   * **Effect on the task:** none on the score, since a real model is hurt by it; what changes is that one of the 60
     folds stops being degenerate (its test side is all Hispanic with no Hispanic training row) and the split stops
     handing back its own key.
   * **Experiments:** leave-one-plate-out unless stated, RMSE in years.

     | measurement | RMSE |
     |---|---|
     | `ethnicity` alone | 13.645 |
     | `site` alone | 15.071 |
     | `sex` alone | 15.566, exactly the constant |
     | constant | 15.566 |
     | each test row predicted by its ethnicity's training-side mean age | 14.18 against 16.07, beating the dummy on 52 of 60 folds |
     | honest model with `sex` and `ethnicity` added | 5.553 against 5.279 |
     | 100-probe clock without and with `ethnicity` | 6.046 / 6.060 |

     The fact that separates the two covariates: each of the nine plates holds exactly one ethnicity, while both sexes
     occur on every plate (female share 0.312 to 0.728, overall 0.515). So `sex` passes the test `ethnicity` fails,
     and keeping one while dropping the other rests on the key and not on a preference about demographics.
   * **Consistency:** the precedent offered for keeping it does not hold. `gossis_icu_hospital_mortality` keeps its
     group id out of its features, and its `ethnicity` is a patient attribute spread over 147 hospitals rather than a
     function of the group; the advocate read it on disk and withdrew the precedent. No precedent covers a feature
     that is a function of the group key, so this case sets one, and the cross-dataset file proposes the Cases row.
   * **Panel:** the column auditor raised it, the practitioner and the critic measured it, and the advocate withdrew
     its "either call ships" after reading the precedent on disk; all three now agree it should go.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop it (implemented) | `_clean` drops it with `site`; `sex` stays, and the notes carry the plate and sex contrast | removes the coarsening of the key; costs nothing measured; makes the `site` reason consistent | one fewer recorded covariate |
     | B | Keep it as a feature | what the definition had before this panel | it is the paper's own covariate | an exact function of the split key; the paper itself could not separate it from the batch; one fold is degenerate in it |
     | C | Keep it with a written exception | B, plus an exception naming the fact that sets it apart | keeps a genuine attribute of the person | no such fact was found; the exception would rest on "it is a genuine attribute", which does not answer the key argument |
     | D | Drop `sex` as well | the features become the probes only | simplest | unjustified: every actor holds `sex`, it scores exactly the constant alone, and both sexes are on every plate |

   * **Recommendation:** A, which is applied, with the distinguishing fact recorded in the notes. If you prefer C, the
     exception has to name a fact that answers the key argument. **Decision:** confirm the drop, or keep it with an
     exception?

   **Notes for the AI:** on B or C, `ethnicity` goes back into `_clean` and `_feature_types` and into
   `task_summary.known`, the dropped bullet returns to a keep bullet, and `dataset check` runs again; on C the
   exception line goes into the record, the notes and the rule's Cases table. On A, the Cases row for a deterministic
   function of the group key is the cross-dataset item.

   [^leak33]: **LEAK-33** (Must): "A group id column is split metadata, never a feature." Its object is the id itself;
     this is the one-step extension to an exact coarsening of it, which is what the Cases row would record.

   **Andrej (2026-11-26, as implemented):** A.

   **Resolved (2026-11-26, Andrej):** A, the drop confirmed. `ethnicity` stays out of the features, as applied:
   each of the nine plates holds exactly one ethnicity, so the column is an exact coarsening of the group key,
   while `sex` stays because both sexes sit on every plate. No exception line is written, and the definition keeps
   the contrast in its notes. Nothing in the data or the splits changes.

3. **Is the measured batch enough to record the group key's departure?**

   * **Problem:**
     - What the plate key withholds is measured and large (of the 1.79 years the plate split costs over folds of
       random people, 1.5 is plate membership and 0.25 cohort composition), while the key departs from the two
       closest precedents, which grouped on the population unit the source's own validation held out, and that
       departure was recorded nowhere[^split4].
     - The reasons the definition gave for rejecting the site key were the number of distinct partitions and the fold
       sizes, which are exactly the grounds that never decide a key; they are replaced.
     - The only key that holds out batch and cohort at once is a two-group split the rules do not allow as a shipped
       split, so two transfers stay untested.
   * **Effect on the task:** none on the data or the splits, since the key is right and stays; what is decided is
     whether the measured batch is enough to record the departure, or whether it needs an exception line of its own.
   * **Experiments:** RMSE in years, ridge over all probes and a 100-probe clock; the pseudo-plates permute plate
     labels inside cells of ethnicity by age quintile, so each keeps its real plate's size, its single ethnicity and
     its age histogram while only about 29% of samples keep their real plate.

     | split | groups | ridge | sd | clock | dummy |
     |---|---|---|---|---|---|
     | random people | – | 6.92 | 0.48 | 5.38 | 14.75 |
     | by chip | 67 | 7.09 | 0.55 | 5.39 | 14.86 |
     | by plate (shipped) | 9 | 8.71 | 1.24 | 5.81 | 15.98 |
     | by site | 4 | 8.81 | 2.67 | 5.55 | 16.63 |
     | plate by site cell | 12 | 8.56 | 1.46 | 5.66 | 16.03 |
     | UCSD against the rest | 2 | 10.15 | 2.20 | 6.30 | 17.62 |
     | pseudo-plates, age and ethnicity matched (3 seeds) | 9 | 7.17-7.20 | 0.59-0.93 | 5.40-5.52 | ~15.7 |

     So of the plate split's 1.79 years over random people, 1.5 is plate membership and 0.25 is cohort composition. On
     the shipped splitter the plate key gives 41 distinct training sides of 60 splits, folds of 146 to 267 rows and
     0.0% of test rows keeping their own plate, against the site key's 10 distinct training sides, folds of 35 to 482
     rows and 32.3%. The batch is recoverable from the features at 0.891 accuracy against 14.0% by chance, and the
     inferred plate's mean age alone scores 11.96 against 14.73.
   * **Consistency:** `heart_disease` (the hospital, the same leaf) and `open_soil_spectral_library` (where "93-96% of
     test layers kept their survey in training", the same shape as the 94.5% here) were resolved the other way, and
     `early_learning_predictors` moved back to the facility from the collection round. What sets this case apart is
     that the batch is measured and strong, which is the test `lung_adenocarcinoma_metastasis` required before
     grouping on a processing unit, and that the site key tests measurably less.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Plate, the departure recorded by the measured batch (implemented) | the splits comment carries the pseudo-plate decomposition, the 41 distinct training sides, the 0.0% against 32.3%, the lot finding, the named place and distance, the untested transfers with UCSD's 100%, and the two-component split as the bound with its price | the stated reasons are the real ones; the departure is recorded with its fact; the bound is named without pretending to test it | the departure rests on a fact in the splits comment rather than on a written exception |
     | B | A, plus a written exception | A, plus an exception line in the record and the rule's Cases table | the departure is findable from the rule's side | a second place to keep in step |
     | C | Site key | 4 groups | matches the shape of the source's own validation | tests measurably less (32.3% keep their plate, lower clock error, sd 2.67 against 1.24) and gives folds of 35 rows |
     | D | UCSD against the rest | two groups, one leave-one-out pair | holds out cohort and batch together | not a split protocol: 2 groups, one pair, no 60 scored evaluations, and the 304-row side leaves 46.3% for training, below the training floor |

   * **Recommendation:** A, which is applied. D is not a weighing call, since the rules rule it out as a shipped split;
     it belongs in the text as the bound on what the plate split cannot test, with its price named, which is where it
     now is. **Decision:** is the measured batch enough, or do you want the exception of B?

   [^split4]: **SPLIT-4** (Must): "The split follows what the task does in reality, not the size of the gap";
     **SPLIT-5** (Must): the split a paper prescribes "is a claim to check against the task design". The paper's own
     N1 and N2 cohorts share plates 2 and 5 with its training side (plate 2 holds 65 N1 and 19 N2, plate 5 holds 44
     and 46), are one fold, and are easier than the average plate fold (N1 to N2 clock 4.64 years, N2 to N1 7.76).

   **Andrej (2026-11-26, as implemented):** A.

   **Resolved (2026-11-26, Andrej):** A. The plate key stays, with the measured batch as the record of its
   departure and no separate exception line: the splits comment carries the pseudo-plate decomposition (of the 1.79
   years the plate split costs over folds of random people, 1.5 is plate membership and 0.25 cohort composition),
   the 41 distinct training sides of the 60 splits, the 0.0% of test rows keeping their plate against the site
   key's 32.3%, the Sentrix lot finding, and the two-component split named as the bound the shipped split cannot
   test, with its price. Nothing in the data or the splits changes.

4. **`mae` in years, or the `rmse` fallback?**

   * **Problem:**
     - Every actor in this field states and acts on absolute error in years, while the declared metric is the
       problem-type fallback[^met].
     - The paper's own unnamed "error of 3.9 years" sits between the measured MAE and median absolute error and
       nowhere near the RMSE.
     - The reason the definition gave did not engage the question at all and did not say where else we looked; it is
       rewritten either way.
   * **Effect on the task:** small and not a validity question, since over nine model variants the two metrics rank at
     Kendall tau 0.889; what changes is which band of ages drives the score.
   * **Experiments:** pooled over the 60 folds, a 100-probe clock against the constant.

     | | clock | dummy |
     |---|---|---|
     | RMSE | 6.14 | 14.73 |
     | MAE | 4.57 | 11.91 |
     | median absolute error | 3.58 | – |
     | within 5 years | 64.2% | – |
     | correlation | 0.909 | – |

     RMSE is driven by the band where the clock is most biased (+2.59 years at 19 to 39, -4.40 at 80 to 101,
     calibration slope 0.93 to 0.95), and both error metrics penalise the calibrated clock: stretching by 1.1 nearly
     removes the age trend in the residual while costing RMSE 6.00 to 6.23.
   * **Consistency:** `corporate_credit_rating` took MAE over the rmse fallback for a source that gave absolute
     differences and named no scalar metric, and `forest_fires` points the same way; against that, a source reporting
     several criteria side by side has no unique original, which is the ground the fallback rests on today. The
     benchmark this candidate comes from states RMSE is its primary regression metric, which is no evidence for us and
     is named for provenance only.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `rmse`, reason rewritten (implemented) | the fallback stays; the reason now says where we looked, weighs the field's practice and says why the context was judged short of clear | honest about the call; the source names no metric at all | leaves the metric decided by a default on a task whose field has a convention |
     | B | `mae` in years, context origin | declares MAE, names the overruled fallback and why the field's practice is clear | matches every actor and the paper's own figure; not driven by the oldest band, where the clock is most biased; a precedent went this way on the same shape | the context test is "only when the context is clear", and tau 0.889 means little moves |
     | C | Median absolute error | the standard clock's own reported statistic | closest to how clocks are reported | invents a choice the source did not fix; not one of our fallbacks |

   * **Recommendation:** B. The field's practice is uniform (forensic tools report an MAE of about 3.2 years,
     inter-laboratory work a MAD of 3.62, the standard clock a median absolute deviation), the paper's own number is
     an absolute error, and the one argument on the other side that looked decisive, the other benchmark's declared
     RMSE, is not evidence we may use. If you find the context short of clear, A is the honest second.
     **Decision:** `mae` under the context origin, or the `rmse` fallback as it now stands?

   **Notes for the AI:** on B the declaration becomes `Metric.from_context("mae", reason=...)`, the reason naming
   the overruled fallback, the field's practice and the paper's own figure, and `dataset check` runs again; the
   metric reads only the target and the prediction, so no scoring column changes.

   [^met]: **MET-11** (Must), the `context` origin ("the source defines no metric, but the task makes one obvious, so
     the default would score the wrong thing ... Only when the context is clear; otherwise the fallback") against the
     `fallback` origin, whose reason "says where we looked"; **MET-5** (Should) on a paper reporting several criteria
     side by side; **EV-4** (Must) on another benchmark's choices.

   **Andrej (2026-11-26, change):** Option B: `mae` in years, context origin.

   **Resolved (2026-11-26, Andrej):** B. The declaration is now `Metric.from_context("mae", ...)`: mean absolute
   error in years, origin `context`. The reason names the paper's own undefined "error of 3.9 years" as the
   original, the field's reporting convention as the context that fixes it (forensic age tools about 3.2 years, an
   inter-laboratory mean absolute deviation of 3.62, the standard clock a median absolute deviation), the measured
   support (a 100-probe clock over the 60 folds: MAE 4.57 and median absolute error 3.58 against RMSE 6.14, so the
   paper's 3.9 sits between the first two and nowhere near the third), and what is rejected: the `rmse` fallback,
   which this overrules and which is driven by the band where the clock is most biased, and median absolute error,
   which no source fixes. The rows, the features and the splits are untouched, and little moves (Kendall tau 0.889
   over nine model variants). Every error in years measured for this record was measured as an RMSE and is kept as
   measured, now said so: the splits comment opens with it, the dropped-`ethnicity` bullet says it, and the
   acceptance for `groups_test_groups_few` gives the clock's pooled MAE next to its RMSE (issue 5). `dataset check`
   has not been re-run for this change, so the generated `README.md` is stale against `dataset.py`: it still reads
   `metric: rmse` with `metric_origin: fallback` and carries the old metric reason and the old acceptance text.
   The next check regenerates it; nothing else in the definition depends on the metric, since the checks fit no
   model.

5. **Confirm the two check-warning acceptances and the documentation items?**

   * **Problem:**
     - Two check warnings fired with no acceptance text, although the evidence for both now exists[^warn].
     - Three facts were missing rather than wrong: the Sentrix lot finding, the 304 measured cells that ship as
       missing, and the fold-level count of distinct splits.
     - One change the column auditor proposed, declaring `plate` categorical, runs against a settled decision.
   * **Effect on the task:** none on any score; the warnings were the only item a check would still flag.
   * **Experiments:** the evidence written into the acceptances and the notes.

     | fact | measurement |
     |---|---|
     | the task is not hollow at nine groups | four model families beat the dummy on 60 of 60 splits, shuffled ages on 0 of 60 over three seeds |
     | what a score has to be read against | per-split RMSE 4.62 to 6.66, fold-to-fold sd 1.24, 41 distinct training sides of 60 splits |
     | the groups | plates of 17 to 92 samples, folds of three plates and 146 to 267 rows |
     | nothing binds above the plate | 8 Sentrix lots, 4 of 8 crossed by a plate, a lot-held-out split easier than the plate split (clock 5.93 against 6.12) |
     | the restored cells | 304 of 430,448 are measured, not imputed (284 deposited as exactly 0.0, over 188 samples and 186 probes) |

   * **Consistency:** `huesken_sirna_efficacy` is the template for the few-groups acceptance, and `heart_disease`
     accepted both warnings with three hospitals. On the dtype, integer-coded categories were decided to stay integers
     (2026-11-04, Lennart: "we only care about it being correctly read from our setup and changing this would make the
     data state less correct, so integer code should stay"), and `plate` is a group column that is never a model
     input, so the argument that an integer implies an order has even less force here.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The three written, `plate` left as `int64` (implemented) | both warnings accepted with the evidence; the lot finding in the split reasons; the 304-cell clause in the imputation bullet; the 41 distinct training sides of the 60 splits stated | clears the checks; `plate` stays consistent with the settled decision | none found |
     | B | A plus `plate` as a string category | A, and `plate` declared categorical | removes an order the column does not have | reverses a curator decision of 2026-11-04 for a column that is never a model input |
     | C | Leave the warnings unaccepted | the acceptances come out again | the curator signs each acceptance himself | the evidence exists and the check keeps flagging them |

   * **Recommendation:** A, which is applied. **Decision:** confirm, or also change the `plate` dtype?

   [^warn]: the two slugs are `task_group_count_low` and `groups_test_groups_few`; an acceptance is one reason per
     slug in `accepted_check_warnings`, which the curator signs off.

   **Andrej (2026-11-26, as implemented):** A.

   **Resolved (2026-11-26, Andrej):** A. Both check-warning acceptances stand as written, with `plate` left as
   `int64`, the settled dtype for an integer-coded column that is never a model input. The three documentation
   facts stay in the definition: the Sentrix lot finding in the split reasons, the 304 measured cells in the
   imputation bullet, and the 41 distinct training sides of the 60 splits. The acceptance for
   `groups_test_groups_few` is reworded only to name its metric, now that the declared metric is `mae` (issue 4):
   it gives the clock's per-split RMSE range of 4.62 to 6.66 with a fold-to-fold sd of 1.24 as measured, and the
   same model's pooled MAE of 4.57 against RMSE 6.14.

**Review panel:** ship after changes (mediator). Full tier, eleven roles: claim auditor, column auditor, split
auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator and review
editor. Claim audit: 34 claims, 31 hold, 2 refuted in wording, 1 holds with a qualification, 3 untested; no claim that
changes validity was refuted. Column audit: nothing flagged in the 473,036 columns it saw, counted before `ethnicity`
was dropped (the table now ships 473,037 columns, 473,035 features); five issues, all documentation or a weighing
call. Blind review, from outside the repository and without our notes: include with changes, with the provenance
matched to the public archive at max abs diff 0.0; its count of five distinct test sets rested on a reconstruction it
could not check and is set aside, three agents that read the shipped split file measuring 41 distinct training sides
of the 60 splits. Task gamer: the table is clean, 11 attacks found nothing, and the
task is gameable through the published literature. Debate: the critic opened at "do not ship as a fitting task" and
moved to ship after changes; what is disputed and left to the curator is how far the contamination declaration goes
(issue 1) and the metric (issue 4). Three probes ran out of memory on the first attempt and were re-run with more; the
group probe did not finish, and the split auditor's own experiments replace it.

<details><summary>Claim audit</summary>

34 claims checked, 31 hold, 2 refuted in wording, 1 with a qualification, 3 untested. The audit rebuilt every beta
from the raw signals rather than trusting the deposit.

| Claim | Test | Result |
|---|---|---|
| the deposit's betas are BeadStudio's `max(B,0)/(A+B+100)` | all 318,108,009 cells rebuilt from the signals | holds to 3.14e-07 |
| 430,448 restored cells (405,768 blank, 24,680 changed), at most 34 per probe | the rebuild | holds; 34 is exactly 5% of the 681 samples at which the paper ran its own missing-value filter |
| every restored cell is an imputed value | the rebuild | qualified: 304 are reproduced by the sample's own signals (284 deposited as exactly 0.0, over 188 samples and 186 probes), so they are measured, not imputed |
| the average-beta file holds the series matrix's values | all 310,310,304 cells | holds (other row order); `RAW.tar` holds the four manifests only |
| the QC subset is the paper's | 485,577 - 11,648 X/Y - 65 `rs` - 830 | holds exactly (the 830 are 827 `cg` and 3 `ch`) |
| the exact zeros are the formula's floor | signals of three samples | holds; all but 3,243 reproduced from the sample's own signals |
| "Sentrix prefixes form 8 lots that cross plates" | the lots against the plates | refuted in wording: 8 lots, only 4 of 8 cross a plate, and a lot-held-out split is easier than the plate split (clock 5.93 against 6.12) |
| the metric reason says where we looked | the reason's text | refuted: it did not |
| the site mapping is the paper's N1 and N2 | the sums | holds numerically (482 and 174), but plates 1+2 and 2+5 also sum to 174, so the mapping is not the only partition that fits |
| the split comparison table, the clock against the dummy, `cg16867657`, the plate table, the folds, the duplicate checks | re-measured | reproduced exactly, including 60/60 against the dummy and 0/60 on shuffled ages over three seeds, `cg16867657` rank 1 at +0.8585 reaching 83.2% of the clock's skill, and the `rs` pair X5056/X5057 at 62 of 65 on one plate |

Untested, because the deposit cannot settle them: that a blank export cell always means a failed detection p-value;
that the mask catches every imputed cell (a KNN value landing within 1e-6 would be invisible, though the smallest
change among the 24,680 is 4.87e-05); and that the 830-marker filter cannot be undone. It also noted the gap that
`accepted_check_warnings` was empty while two warnings fired.

</details>

<details><summary>Column audit</summary>

0 of the 473,036 columns it audited flagged, counted before `ethnicity` was dropped: 0 constant probes, 0 duplicate
probe columns (all hashed), no impossible beta, no proxy
missing value, no untyped column, no duplicate people, `age` equal to every sample title, `plate` in the group columns
and not in the features, and no column recorded after the blood draw. Every file of the release that is not read has a
written reason. Five issues:

1. `ethnicity` is a feature that is also a two-level coarsening of the group key (constant within every plate, mean
   age 54.6 against 69.1; alone 13.645 against the constant's 15.566; one of the 60 folds degenerate in it). Whichever
   way it goes, the fact that separates it from the dropped `site` must be stated. Applied as a drop, issue 2.
2. The three omitted probe classes need a reason per class: removing X and Y is real (only 80 of the 473,034 kept
   probes separate the sexes by more than 0.1 beta, against 7,024 of the 12,478 dropped non-`rs` probes), the 65 `rs`
   probes are a genotype fingerprint with a privacy reason of its own, and the 830 QC probes cannot be identified one
   by one, so "make up the rest exactly" is arithmetic and should say so.
3. No column is declared a non-feature and there is no mechanism for one; re-adding `site` later costs a rebuild that
   re-reads the 1.2 GB series matrix only, since the prepared raw file is cached.
4. The restored missingness is patterned but unusable: per-sample counts correlate with age at 0.106, but within a
   plate at 0.002, and a kernel ridge on the indicators alone scores 15.22 against the constant's 15.57.
5. `plate` ships as `int64`, implying an order it does not have; it is never a model input, so no score moves.

Both covariates are largely readable from the probes themselves (sex at AUC 0.998 under leave-one-plate-out, ethnicity
at 0.999 under IID folds), which is why neither moves a clock, and the batch is a strong fingerprint too (plate
one-vs-rest AUC median 0.996). The exact zeros were settled two ways: `beta == 0` exactly where `SignalB <= 0` with no
exception over three samples by 485,577 probes, and zero counts ranking exactly by the probe's methylation level.

</details>

<details><summary>Split audit</summary>

Right with notes; the key settles on `plate` by measurement. The tree walk is `Experimental Results` to "another
laboratory, site or instrument" to the place step to several places, which is the leaf that ships; the one thing the
tree does not answer is which place, of which the data holds 9 batches, 4 cohorts and 1 laboratory. Read strictly as
"another laboratory" the walk would end at a random split, which would be wrong for a clock, so the shipped reading,
that the place is the assay batch, is right and needs saying.

The decisive experiment is the pseudo-plates (plate labels permuted inside cells of ethnicity by age quintile, each
pseudo-plate keeping its real plate's size, single ethnicity and age histogram, only about 29% of samples keeping
their real plate): of the plate split's 1.79 years over random people, 1.5 is plate membership and 0.25 is cohort
composition. The site key tests less on every measure it took (10 distinct training sides against 41, folds of 35 to
482 against 146 to 267, 32.3% of test rows keeping their own plate against 0.0%, fold-to-fold sd 2.67 against 1.24,
and a lower clock error, 5.55 against 5.81). "Hold out both" is unavailable at any finer key: the plate and site
incidence graph has exactly two components, and the 12-cell pair key is the opposite of "both" (25.2% keep their
plate). It also measured that 94.5% of test rows keep their site under the shipped folds, 96.9% over all 84 possible
three-plate folds and 100% for UCSD's 46% of the rows.

Its problems: the leaf's place is not named; two transfers stay untested without being named; "plate explains 0.45 of
the variance of age" is evidence of the cohort design, not of the batch signal; the "12 groups" sentence reads as its
own opposite; and the 69% nearest-neighbour figure is Euclidean (60.4% by sample correlation). It recommended keeping
the key and the leaf, accepting both warnings, and rewriting the reasons; all of that is applied.

</details>

<details><summary>Domain practitioner</summary>

The use case was written on an actor who predicts nothing. Its three readings:

| Reading | Fit | Why |
|---|---|---|
| aging rate (the residual as a biomarker) | none | the actor already holds the chronological age, and the quantity they act on has no column in this deposit |
| forensic (the age of an unknown donor) | approximate | a real decision with an unknown label, but casework uses a targeted 3 to 44 CpG assay rather than a research array, a self-reported ethnicity is not something a laboratory holds, and the cohort has 12 people under 30 |
| clock builder or validator (what the benchmark scores) | direct | "which model do I ship as my clock?" is decided exactly this way: fitted on profiled cohorts, chosen by held-out error in years on arrays from a batch not in training |

Why the aging-rate clause cannot carry the fit: the score runs against that purpose, since age acceleration's
mortality association attenuates as chronological accuracy rises; no outcome ships; and the residual is not clean,
carrying age (slope -0.147 years per year, 12.5% of its variance) and batch (5.9% between the three test plates, up to
24.5% in one fold), while the same person's residual moves with a median SD of 2.82 years depending only on which
plates were in training. It would keep `sex` and drop `ethnicity` (no actor holds it; predicting each test row by its
ethnicity's training-side mean age cuts RMSE 16.07 to 14.18 and beats the dummy on 52 of 60 folds, which is the
recruitment design and not biology). On the metric it would declare `mae` in years (clock MAE 4.57, median absolute
error 3.58, RMSE 6.14; the field reports absolute error, and RMSE is driven by the band where the clock is most
biased, -4.40 years at 80 to 101). It calls the dominant probe biology rather than a flaw: `cg16867657` in ELOVL2 is
the anchor marker of the forensic field, and the headroom between it and a tuned method on 473k columns is about 1.6
years. It is also the agent that first named the contamination: the 71 published coefficients were fitted on 482 of
these 656 rows.

</details>

<details><summary>Blind review</summary>

Saw only the participant kit's data file, its task card and the public web; voted include with changes. It verified
the provenance from outside: three samples pulled from the public archive matched our rows at max abs diff 0.0 (the
next-best row 0.41 to 0.52 away), all 396 distinct label tuples have identical counts in our table and in the 656
archive records, and probe counts, beta range and the absence of genotype probes all check out. No duplicate samples
(max cosine between standardised rows 0.675). The signal is real and not trivial (top probe at r = +0.859, 402 probes
above |r| = 0.5, grouped RMSE 5.48 against a constant's 15.45).

Its concerns, ranked: (1) the file cannot be opened with default pandas or pyarrow settings, so most users' first line
of code fails (now the working copy's framework item); (2) the task card never says which
columns are features, and `plate` is a target proxy (plate-mean age R^2 0.446); (3) "60 splits from 9 groups", where
it reported 5 distinct test-plate sets and warned that the error bars are weaker than 20 by 3 suggests; (4) the source
study's own split was dropped, which it reproduced on the 593 rows it could assign (RMSE 3.92), and it found that
plates 2 and 5 straddle the published cohorts; (5) plate is confounded with ethnicity and strongly with age, so the
grouped constant baseline is worse than the random one (15.45 against 14.75), while in defence of the key plate is
recoverable from the methylation at 89.2% accuracy against 14.0% chance; (6) 473k features is a heavy, unusual shape;
(7) minor points about the NaN cells, the missing sample identifier and integer ages.

Its concern 3 rests on a reconstruction it states plainly it had to make, because it could not read the stored split
indices. Three agents that read the shipped split file measured 41 distinct test sets (41 distinct training sides) of
the 60 splits, 18 of the 20 repeats distinct, so the "5 distinct test sets" is set aside and the fold-level count of
41 is now written into the definition.

</details>

<details><summary>Task gamer</summary>

The table is clean; the task is gameable through the published literature. Honest baselines over the 60 splits:
constant 16.065, ridge on all 297,564 complete sites 8.527, gradient boosting on a fold-honest top-1000 6.406, and the
best honest model a ridge on a fold-honest top-5000, z-scored, at 5.279; 20 extra random columns move a base of 5.505
by at most 0.03, which is the noise band.

| # | Exploit | Honest | Exploited | Gain |
|---|---|---|---|---|
| 1 | stack all five published clocks | 5.279 | 4.487 | +0.791 |
| 2 | stack Hannum and Lin, the two fitted on these samples | 5.279 | 4.645 | +0.633 |
| 3 | stack Hannum alone | 5.279 | 4.783 | +0.496 |
| 3b | Hannum alone, recalibrated per split, no honest model at all | 5.279 | 4.949 | +0.330 |
| 4 | control: stack three clocks fitted elsewhere | 5.279 | 5.163 | +0.115 |
| 5 | clip predictions to the training age range | 5.279 | 5.264 | +0.014, noise |

Its verdict on remedies, knowing none of our rules: "none that saves the task", the honest options being to score the
series as a held-out evaluation set for clocks or to accept that a leaderboard entry is bounded below by the Hannum
clock and say so. Two handicaps for an honest model: the plate confound (per-plate bias -2.68 to +4.33 years, per-split
RMSE 4.62 to 6.66), where it still says keep the grouped split because it is the right regime; and that the 60 splits
are 41 distinct test sets, counted directly from the shipped file, so the across-split sd understates the variance.
`score.py` does not run for the same thrift limit the blind reviewer hit. 11 attacks found nothing: row order and ids,
copies and near-copies (0 pairs above 0.995), missingness, the exact zeros as a second missing code, formats and
decimals, transductive scaling (+0.018, inside noise), test-block batch removal, transductive recalibration, the group
structure (plate recoverable at 0.891 accuracy, but the grouped split defuses it), the recorded covariates (together
14.209 alone, -0.275 added to the honest model), and clipping to the full table's range. Out of scope and named: the
target ships for every row, the union of the 60 training sides is all 656 rows, and the public archive publishes the
labels.

</details>

<details><summary>Precedent check</summary>

Five of six decisions consistent; the group key departs.

| Decision | Verdict |
|---|---|
| undo the authors' KNN imputation | consistent: the curator instruction on the sister `sarcoma` record asks for exactly this rebuild, `coad` was retired for want of it, and the refusals elsewhere were all conditioned on not being able to rebuild |
| group on the plate, not the site | departs from `heart_disease` and `open_soil_spectral_library`, which chose the population unit the source's own validation held out, and from `early_learning_predictors`, which moved back to the facility |
| ship the full width (the 473,036 features it saw, 473,035 since the `ethnicity` drop) | consistent: width is no reason to drop features and a model's input cap is never an argument; `kdd_cup_09_appetency` replaced a 230-column version with the 15,000-column original on this ground |
| keep `sex` and `ethnicity` | it read `gossis_icu_hospital_mortality` as the precedent for keeping; the critic and then the advocate checked that record on disk and showed it is not on point |
| the `rmse` fallback | consistent, but `corporate_credit_rating` took MAE over the fallback on the same shape; it drafted a reflection prompt |
| accept the two warnings | acceptable, but the evidence was thinner than all four precedents required at the time it looked |

Three facts it measured: only 3 of the 12 site and plate pairs break nesting; the graph has 2 components; and over all
84 possible three-plate folds 96.9% of test rows keep their own site, UCSD 100%. Its reflection prompt offered the
plate key with the distinguishing fact recorded, the site key, the two components, or the plate key plus correcting
the pair-key line, and recommended the first with the last.

</details>

<details><summary>Advocate</summary>

Argued ship with four wording and metadata fixes, and ran the one measurement the task gamer most wanted: the honest
elastic net, the published clock recipe fitted per split with the alpha chosen on grouped inner folds, over 12 splits.

| same 12 splits | RMSE |
|---|---|
| honest ridge top-5000 | 5.280 |
| honest elastic net, clock recipe | 5.428 |
| elastic net plus Hannum and Lin | 4.638 |
| elastic net plus the three external clocks | 5.242 |

It conceded that this goes against its own case: the clock recipe fitted honestly does not beat ridge and does not
shrink the measured gains. Its argument on the contamination: nothing in the shipped table carries it, the carrier is
a third party's published model, which our rules name as never changing a decision, the exploit is strictly weaker
than the public archive's own labels, no change to the definition removes it, and the ladder therefore lands on keep
with a note. It proposed the kept-leak note plus one sentence in the task card, and conceded that this is a policy
guarantee and not a data guarantee. On the other points it conceded the use case, the split's forbidden grounds and
the documentation gaps, and in its rebuttal it changed position three times: it read the `gossis` precedent on disk
and withdrew it, agreeing `ethnicity` should go; it reproduced the parquet failure and narrowed the remedy to the
reader, having established that the file already has one row group so column groups would make the footer larger; and
it accepted the critic's caveat on its elastic net. It disputed that the two-component split should be adopted rather
than named as the bound.

</details>

<details><summary>Critic</summary>

Opened at "do not ship as a fitting task in its current form", conceding at the start that the imputation rebuild is
exemplary, the plate key is right, the task is learnable and not trivial, and no leak sits inside the table. Its case
rested on four facts said to make the clock exploit differ in kind from "the labels are public": that no row
identification is needed, that it is indistinguishable from legitimate modelling, that no definition change fixes it,
and the task gamer's own verdict. It named the 60-fold honest elastic net as the measurement that would settle the
size of the gains, and reported that it had stopped its own run rather than spend that compute.

In its rebuttal it conceded the verdict and two framings. Its own elastic-net number was wrong, and it found the error
itself (`enet_path` without an intercept), so the advocate's measurement stands. Its reason (a) fell to the blind
reviewer's archive match, so the label-lookup route dominates the clock route and the rules place the carrier out of
reach of a validity objection; its verdict changed to ship after changes. What survives, and it is not nothing: the
exploit does not require a bad actor, because using a published clock as a feature is what this field does, and
nothing can detect it, where the one comparable kept exploit had a check. It corrected the floor the note must state
from the raw clock output (6.667) to the recalibrated one (4.949), taken from the advocate's own recalibrated per-split numbers. It
holds its changes to be conditions rather than suggestions, and still prefers the larger GSE55763 cohort as a
weighing factor for the curator, not as a reason to withhold this one.

</details>

<details><summary>Mediator</summary>

Verdict: ship after changes. Validity: the selection rules hold; the use case fails as written and is fixed in text,
with the direct actor supplied by the rule that narrows the fit rule; the transductive imputation triggered and was
repaired from the origin; the group-id rule triggered and `ethnicity` is dropped; the split rules hold, with the
forbidden grounds replaced; the published-clock contamination is an evaluation-level leak whose carrier the evidence
and provenance rules place out of reach of a validity objection, so the ladder lands on keep with a note. Value: a
large real signal, two check warnings to accept in writing, the metric open. Quality: the 304 measured cells keep
their clause, `plate` stays `int64` on the settled decision. Weighed: use case +, source +, provenance +, gap 0, size
-, contamination -. Blocker: nothing is built until the parquet reader fix lands.

It re-measured three points itself, each from a cached file: the recalibrated clock error per split over the 60 folds
(Hannum 4.949, Lin 5.517, Horvath v1 5.976, PhenoAge 8.202, Zhang-10 14.441), the plate by ethnicity and plate by sex
tables (each of the 9 plates exactly one ethnicity; both sexes on every plate, female share 0.312 to 0.728), and the
parquet footer (1 row group, 656 rows, 473,038 column chunks; it reads correctly with the two thrift limits raised).
It adopted the critic's withdrawal of its opening position, holding that a rule barring the 71-number compression
while allowing the archive's own labels would be incoherent.

It mapped every exploit the task gamer found to a rule and to a place: the clock exploits to issue 1 and to the rule
question, the external-clock control as the thing that identifies them, the plate confound and the fold-level count to
the warning acceptances, the container failure to the framework item, and the covariates to the `ethnicity` drop. It
listed nine changes to make at once, all of them applied: the use case on the clock builder, the `ethnicity` drop, the
split reasons, the pair-key correction, the named place and distance and the untested transfers, the lot finding, the
two warning acceptances, the 304-cell clause, and the metric reason. Its precedent table records the group key as the
one departure, with the measured batch as the fact that sets it apart, and the `sex` and `ethnicity` split as a
precedent this dataset sets.

</details>

<details><summary>Review editor</summary>

Applied the mediator's nine changes to the definition, each checked against the agent reports it came from, and wrote
this review. In the definition: the use case, `fit_reason` and the prediction-point bullet now rest on the clock
builder, with the forensic estimate named as the decision the clock serves; `ethnicity` is dropped in `_clean` with
`site` and out of the feature types and the task summary, its bullet rewritten as a drop reason with the plate and sex
contrast; the splits comment carries the pseudo-plate decomposition, the 41 distinct training sides and test sets, the
0.0% against 32.3%, the Sentrix lot finding, the named place (the assay batch) and distance (Euclidean, 60.4% by
sample correlation), the two untested transfers with UCSD's 100%, and the two-component split as the bound with its
price, while the pair-key sentence now says the 12-group key is the weakest of the three; the imputation bullet gains
the 304 measured cells; `accepted_check_warnings` carries both acceptances with their evidence; and the metric reason
says where we looked and weighs the context origin against the fallback. The width line goes from 473,038 to 473,037
columns with `ethnicity` gone. Two items go to the working copy's cross-dataset file rather than to this record, as
the mediator asked: the rule amendment on another party's model, and the wide-parquet reader fix, whose blocker line
stands in the outcome above. The `plate` dtype proposal was not applied, on the settled decision of 2026-11-04.

</details>
