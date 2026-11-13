---
unique_name: biogeographical_ancestry_prediction
name: Human Genome data
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- Tiny Data
- New IID
- 'Samples: No Time Dimension'
collections:
- New (BeyondArena)
original_source: Other
year: '2023'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.internationalgenome.org/
- https://www.kaggle.com/datasets/i191796majid/human-genetic-data
- https://www.fsigenetics.com/article/S1872-4973(25)00070-5/fulltext
- https://github.com/CarolaHeinzel/BGA-Classification/blob/main/datat/filtered_population_eur_update.xlsx
notebook_path: datasets/beyond_iid/new_iid/biogeographical_ancestry_prediction/biogeographical_ancestry_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/biogeographical_ancestry_prediction/dataset.py
source_row: 686
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Fixed a source artefact: dropped the Turkey class and set no-calls to missing.** The data is Ruiz-Ramirez et al. 2023 (VISAGE Enhanced Tool), Supplementary Table S1A, as used by Heinzel et al. 2025 (Sec. 2.1), which pools 1000 Genomes, HGDP-CEPH, Middle East, SGDP and Estonian Biocentre samples. By sample ID, the inter-European classes come from three sources: 1000 Genomes (HG/NA IDs: British, Finnish, Iberian, Toscani, Utah CEPH), HGDP (HGDP IDs: Russian, Basque, French, Sardinian) and Turkey (IDs 2TR-..., source not confirmed; the Ruiz-Ramirez PDF was not reachable). Turkey's source has an assay artefact: rs3857620 is AG in 24 of 28 samples, 0 AA (about 5 expected under Hardy-Weinberg equilibrium), and GG in all 607 others; with the no-calls it separated Turkey at AUC 0.96-0.98 (leak audit 2026-09-24). Changes: Turkey dropped (635 -> 607 rows, 10 -> 9 classes, a deviation from the paper's ten); rs3857620 and rs367953206 (constant without Turkey) dropped; "NN" no-calls set to missing (28 cells in 24 HGDP rows, none in 1000 Genomes, so a weak source hint remains). Each class still comes from one source; the task stays hard (LightGBM log loss worse than the class prior on the shipped splits). rs2789823 (AG in 7 rows, all Iberian) may be a smaller artefact; kept.

The Kaggle version already did PCA.

This dataset is very close to the data from one of my collaborations (https://www.sciencedirect.com/science/article/pii/S1872497325000705,https://www.biorxiv.org/content/10.1101/2025.11.08.687358v1.abstract) and we could easily find more similar data / create a real task from it. It comes with different kinds of marker sets. Moreover, some of the default tasks are trivial to solve.

This could give us a "real" dataset with a lot of features.

From going through the project, let us try to use the version from my collaboration. We use the Inter European version as the continental task is the "simpler" task. Moreover, note that these datasets come with expert-based feature selection.

Basic preprocessing: https://github.com/CarolaHeinzel/BGA-Classification/blob/main/CrossValidation_Code/run_convert_excel_data.py, All data is categorical, target Population

Relevant classes we should have: 09. Russia - Russian        British in England and Scotland        Finnish in Finland        France        Iberian population in Spain        Italy        Turkey        Utah Residents (CEPH) with N & W European ancestry

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Heinzel et al. 2025 compare models by ROC AUC, accuracy and log loss (repository README); which one decides was not verified (full text not read). log_loss is the multiclass fallback and one of the reported metrics.

CC (2026-10-21, Lennart): biogeographical_ancestry: roc_auc stays (the paper's metric); declared as the source's metric, one-vs-rest macro ROC AUC over the populations.

CC (2026-10-21, Lennart): correction to the line above: log loss stays; ROC AUC does not make sense as a good metric for this multiclass task.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 3: gap +, use case + (the source states the forensic use), source + (journal supplement), shape -, risk - (one source population per class).
CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: each population comes from one reference project (1000 Genomes or HGDP), so the classes were collected apart and project differences coincide with the label (failed calls occur only in the HGDP groups, as the fit_reason says); the reference donors were chosen for their ancestry, not drawn from case samples.

**Assessment (AI, 2026-11-05):** marker `Class-dependent Recording`: the Turkey samples come from a separate source with their own genotyping artefact, so how a sample was genotyped told its class; the definition drops the class, as the rule for a class from a separate source or assay asks. Noted in the definition's curation comments; data unchanged.

CC (2026-11-12, Andrej): reviewed under the rule for cuts of growing scientific catalogues. Reference panels do grow, but they grow by adding populations, which are classes here, not items; the only wave the sample identifiers recover is the reference project (104 HGDP people against 503 from 1000 Genomes, 364 of them already in the phase-1 release of 2010-11-23), and the project coincides with the label, so the random split over people stands (Review issue 4, open).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: the one measurable form of a project artefact (a Hardy-Weinberg failure or a project-only genotype, the pattern that got the Turkey class dropped) is absent in all nine populations, and the methods separate widely; what stays open is the 27 failed typing calls, which occur only in the four HGDP populations. Priority 3: gap 1, use case 1, source 1, shape 0, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 3, B, through the cross-dataset item on routine `Timeless` issues): genotypes are fixed at birth and the population label was set at sampling, with no date recorded. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-10, Andrej): review page marks: ship as defined (issue 1, A): the one measurable project artefact (Hardy-Weinberg failures, project-only genotypes) is absent beyond the failed calls; the failed typing calls stay missing (issue 2, A), the curation note now gives the hint's size (log loss 1.95 from missingness alone against 2.03 for the class shares). The licence question stays open.

CC (2026-11-12, Andrej): review page mark (issue 4, A): the random split over people stays. The only arrival wave the sample identifiers recover is the reference project (1000 Genomes phase 1 against phase 3, HGDP-CEPH in no release), which coincides with the population, so a split by entry date would test the project, not later people; the counts are in the `Time basis:` note.

## Review

**Outcome:** added. Reviewed without a review panel, from the evidence already gathered: the record, the earlier
leak audit, a model run on the shipped data and two checks run for this review. The data is Supplementary
Table S1A of Ruiz-Ramirez et al. 2023 (the VISAGE Enhanced Tool), as used by Heinzel et al. 2025: 607 reference people
of nine European populations, each typed at 102 ancestry markers of a forensic marker panel, and the task is the
population of origin, scored by log loss over the nine populations. The AI recommends shipping it, with one open
choice about the failed typing calls. Validity: the Turkey class, whose separately typed source carried a marker that
alone separated it, is dropped with the two markers it made constant, and failed calls are missing (Lennart,
2026-09-30); a check for this review found no second artefact of that kind: in each of the nine populations the
markers sit in Hardy-Weinberg proportions (observed over expected heterozygosity 0.967 to 1.016; one marker of 615
tests below p = 0.001, as chance gives), and no genotype is confined to the four populations of the second reference
project. What remains is that each population comes from a single reference project, so project and label coincide,
and the 27 failed calls occur only in that project's rows (issue 2); the definition records this as an approximate
fit. Value: the methods separate widely. On the data as it ships in the current collection (635 people and the ten
populations, so Turkey included) the 40 benchmark methods run from log loss 1.31 for the best and 1.35 for TabPFN-3.5 to
1.69 for a default boosted tree and 1.87 for logistic regression, against 2.12 for predicting the class shares; the
v0.2 frame drops Turkey, whose class shares give 2.03, so the ordering carries over but the numbers are not the v0.2
ones. An earlier note that a boosted tree stays worse than the class shares is not supported by those results. Quality: rs2789823, heterozygous in 7 Iberian rows and in no other population, is kept; it fits
Hardy-Weinberg in that population (7 heterozygotes against 6.8 expected), unlike the dropped Turkey marker.
Weighed: a journal supplement with the forensic use stated +, a real forensic lead +, nine populations from two
reference projects -, 607 people -, methods clearly ordered +. Left for Andrej: issues 1 and 2.

**Main points:** All four issues are settled; the random split over people stays (issue 4, A, 2026-11-12).

**Record judgment:** a forensic ancestry task on a marker panel built for that use, with a known confound between
reference project and population, recorded on the record by its `Selection Bias` and `Class-dependent Recording`
markers. Two corrections need no decision. The definition's `license` reads `"None"` with a comment guessing
Apache-2.0, while the journal supplement the rows come from is CC BY-NC-ND 4.0 (Crossref) and the code repository the
file is downloaded from states no licence: that is a one-line note and an item for the release checklist, not a
curation question, and one of the curators is a co-author of Heinzel et al. 2025, who can say what may be
redistributed. The build is stale against the current definition, so the dataset needs a rebuild.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**

   * **Problem:**
     - The changes of 2026-09-30 (the Turkey class dropped, ten populations down to nine, failed calls set to
       missing) and the metric (log loss, 2026-10-21) are settled, and the `Class-dependent Recording` marker of
       2026-10-27 records the dropped source.
     - What was left open was whether the remaining confound between reference project and population should be
       measured before the dataset ships.
     - Ship as defined, or hold it?
   * **Background:** five of the nine populations (British, Finnish, Iberian, Tuscan and Utah residents of northern
     and western European ancestry) come from the 1000 Genomes Project and four (Russian, Basque, French, Sardinian)
     from the HGDP-CEPH panel, so a difference between the two projects' typing would separate the two groups of
     classes rather than the people[^1a]. The Turkey class was dropped for exactly such a difference: one marker was
     heterozygous in 24 of its 28 samples and never homozygous for the rarer letter, which cannot happen by chance in
     a population, and that one marker separated the class[^1b].
   * **Experiments:** the confound is now measured on the shipped frame. Within each of the nine populations the
     markers follow Hardy-Weinberg proportions, the test a failed assay fails: 0 to 2 of 64 to 75 markers per
     population below p = 0.01, one of 615 tests below p = 0.001, and observed over expected heterozygosity between
     0.967 and 1.016. No genotype occurs three or more times in the HGDP populations and never in the 1000 Genomes
     ones; the 19 genotypes that occur only on the 1000 Genomes side are rare ones in a group five times as large, as
     their rarity predicts. The one trace of the two projects left is the failed calls, which are issue 2.
   * **Effect on the task:** a forensic case sample is typed with another assay in another laboratory, so a model that
     learned a project's signature would not carry over; the measurements above say there is no such signature left
     beyond the failed calls.
   * **Unknown:** whether models can tell the two projects apart beyond that cannot be measured directly, because
     project and population coincide exactly, so any separation is also ancestry.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 607 people, nine populations, 102 markers, log loss | the artefact that was found is removed; no second one is measurable; methods separate from 1.31 to 1.87 | project and population still coincide, which the fit text records |
     | B | Hold it until the project confound is measured | nothing ships yet | would catch a project signature before release | the measurement above is the one that can be made; a direct one is impossible while project and population coincide |

   * **Recommendation:** A, ship as defined: the one measurable form of a project artefact was tested for and is
     absent, and the fit text says that project and population coincide. **Decision:** A or B?

   [^1a]: **LEAK-15** (Must; amended 2026-10-27, Andrej): a recording artefact that runs through several features
     that would matter for prediction in practice, and that cannot be undone, retires the dataset; one confined to
     features a practical model would not rely on is fixed or kept with a note.
   [^1b]: **LEAK-14** (Must): a class that comes from a separate source or assay is dropped once the paper confirms
     it; this dataset is the rule's case.

   **Resolved (2026-11-10, Andrej):** A, ship as defined; a CC line in the record. The licence note stays an item for the
   release checklist.

2. **Leave the 27 failed typing calls as missing values, although they occur only in four of the nine populations?**

   * **Problem:**
     - A failed call is a marker a laboratory could not read; the definition sets these 27 cells to missing, which is
       what they are.
     - They all sit in the four populations of the HGDP panel: 24 of its 104 people have one, and none of the 503
       people of the 1000 Genomes populations does, so whether a row has a missing value is a hint at four of the
       nine labels that comes from the laboratory, not from the person.
     - Keep them as missing with the note, or remove the hint?
   * **Effect on the task:** a forensic case sample has its own failed calls, unrelated to the population, so a model
     that reads missingness as a population hint gains in the benchmark what it would lose in use.
   * **Experiments:** the hint is small and was measured on the v0.2 frame. A predictor that knows only whether a row
     has a failed call scores log loss 1.95 against 2.03 for the class shares, counted over all 607 people rather than
     across folds, so it is an upper bound: a gain of 0.08 where the best benchmark method is about 0.7 below the class
     shares, at most a tenth of what there is to win. The 27 calls are spread
     over 24 of the 102 markers, two of which are among the five most informative for the populations, and the 24
     affected people are a quarter of the four HGDP populations.
   * **Consistency:** the gallstone case set the rule that a recording convention tied to a class is harmonised and
     that setting values to missing is no fix when the gaps follow the classes[^2a]; it also set the rule that we
     measure the fix before applying it. The imputation itself is the benchmark pipeline's job, not ours[^2b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as missing, documented (implemented) | 607 people, 102 markers; the curation notes name the hint | the data stays as typed; the cost of the hint is at most 0.08 log loss; nothing is invented | a model can read "has a failed call" as a hint at four labels |
     | B | Drop the 24 markers that carry a failed call | 78 markers; the hint is gone | no laboratory hint left in the frame | drops a quarter of the panel, among them the second most informative marker; the panel is the forensic instrument |
     | C | Drop the 24 people with a failed call | 583 people; the hint is gone | no laboratory hint left; keeps all 102 markers | costs a quarter of the four smallest populations, which hold 17% of the rows |

   * **Recommendation:** A, keep them as missing and name the hint in the curation notes: the measured gain is at most
     a tenth of the signal, while both fixes cost either the most informative markers or a quarter of the four small
     populations. **Decision:** A, B or C?

   **Notes for the AI:** on A, extend the existing `curation_comments` bullet with the measured size (a predictor that
   knows only whether a row has a failed call scores log loss 1.95 against 2.03 for the class shares) and re-run the
   dataset check. On B or C, make the change in `_clean`, state the cost in the notes and re-check the split sizes and
   the class counts.

   [^2a]: **LEAK-40** (Should; 2026-10-26, Andrej, on gallstone_disease): gaps the source filled are tested, not
     assumed to leak, and setting cells to missing is no fix when the gaps follow the classes, because the missing
     values then mark a class; **LEAK-13** (Must; amended 2026-10-26, Andrej) asks that a class-specific recording
     convention be harmonised and the fix measured first.
   [^2b]: **CLEAN-2** (Must): the benchmark's pipeline encodes, imputes and scales, so the definition does not.

   **Resolved (2026-11-10, Andrej):** A: the failed calls stay missing; the `curation_comments` bullet on the "NN"
   no-calls now gives the hint's size (log loss 1.95 from missingness alone against 2.03 for the class shares, an upper
   bound). `dataset check` re-run.

3. **Time basis: name the random split over people `Timeless`, as ancestry fixed at birth?**

   * **Problem:**
     - A person's genotype at the 102 markers is fixed at birth and the population label was recorded when the
       reference person was sampled, so no part of a row arrives later and the sampling date plays no role.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits; the split is random
       over people and has no time-basis tag yet.
     - Ancestry is a fixed property of the person, the case the `Timeless` prototype names; the confound that
       remains, project and population coinciding, is issues 1 and 2, not time[^3a].
   * **Background:** the table has no date column, and its order is one block per population, so the raw order is
     the label (the only flag of the time probe). The reference sets are the projects' published releases (1000
     Genomes, HGDP-CEPH), pooled in a 2023 journal supplement; nothing was revised later.
   * **Experiments:** whether relatives sit on both sides of the split (another person of one family carrying the
     label), checked on the 607 people with a kinship estimate (KING's robust estimator) per pair within each
     population, model-free:
     - 1.3% of the 26,448 pairs within a population score as first-degree relatives or closer (kinship above 0.177),
       against 0.9% to 1.7% of pairs drawn across two populations of one project, who cannot be relatives; per
       population 0.8% (French) to 2.5% (Utah); no two people share a genotype.
     - 102 ancestry markers cannot tell a relative from chance at that rate, so the check rules out duplicates and a
       large share of relatives, not a few; the population sizes of the 1000 Genomes part (91 British, 99 Finnish,
       107 Iberian, 107 Tuscan, 99 Utah) are those of its release of unrelated people.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time-basis tag (implemented) | as now | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random split, `Timeless` | as now; the tag and a `Time basis:` line naming the fixed genotype and the label set at sampling | states the fact the split rests on; matches the study | none found |

   * **Recommendation:** B: ancestry and the genotypes do not change, and no row carries information from after the
     sampling. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `IID`), a curation
   bullet `- Time basis: Timeless: genotypes are fixed at birth and the population label was set when the reference
   person was sampled (1000 Genomes, HGDP-CEPH); no date is recorded and the table is ordered by population. No
   duplicate genotypes, and no excess of related pairs beyond chance at 102 markers (2026-11-06).`, `splits_comment`
   unchanged; `dataset check`.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (people typed outside the reference project of their population); the split and `data_tags` are
   unchanged. The tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

4. **Keep the random split over people, or split by when a reference person entered the panel?**

   * **Problem:**
     - The one arrival wave the sample identifiers recover is the reference project's release, and project coincides
       with population, so a forward split puts four of the nine classes wholly on one side[^4a].
     - Within the 1000 Genomes part a wave is recoverable (364 of its 503 people were already in the phase-1 release
       of 2010-11-23, 139 arrived by phase 3), but those arrivals are more people of the same five populations, not
       the populations a panel grows by.
     - Keep the random split over people, or split by an arrival key?
   * **Background:**
     - A wave here would be a population added to the forensic panel: the VISAGE reference set did grow that way,
       pooling 1000 Genomes, HGDP-CEPH, Middle East, SGDP and Estonian Biocentre samples, and a later panel adds
       further populations.
     - A population added later is a new class, not a new item, so no split of these 607 people tests it: that is an
       open-set question about the label set, which this task does not pose.
     - Under the population there is no family key in the data: no two people share a genotype and related pairs are
       no more frequent than pairs drawn across two populations that cannot be relatives (issue 3), so the item key
       and the family key coincide with the random split.
     - The use case fills in a reference set that already exists: a forensic laboratory assigns a trace to one of the
       nine populations the panel holds, which it holds before the case arrives.
   * **Experiments:** the sample identifiers of the shipped 607 people against the 1000 Genomes phase-1 release
     (`integrated_call_samples.20101123.ALL.panel`, 1,092 samples), 2026-11-12:

     | Reference project | Population | People | In the phase-1 release | Arrived later |
     |---|---|---|---|---|
     | 1000 Genomes | British in England and Scotland | 91 | 81 | 10 |
     | 1000 Genomes | Finnish in Finland | 99 | 89 | 10 |
     | 1000 Genomes | Iberian population in Spain | 107 | 14 | 93 |
     | 1000 Genomes | Toscani in Italia | 107 | 96 | 11 |
     | 1000 Genomes | Utah residents (CEPH) | 99 | 84 | 15 |
     | HGDP-CEPH | Russian, Basque, French, Sardinian | 104 | 0 | 104 |

     - The four HGDP populations carry HGDP identifiers and are in no 1000 Genomes release, so "arrived later" there
       means only that they come from the other project, not that they came after.
     - The one population with a real wave is the Iberian one, which grew from 14 people to 107 between the two
       releases; the other four 1000 Genomes populations grew by 10 to 15 people each.
   * **Effect on the task:** a split on the phase would train on five populations and test on a set in which the
     Iberian population holds two thirds of the rows and the four HGDP classes are absent from one side, so it would
     score the project confound the dataset already records rather than hold out later people.
   * **Consistency:** follows the screen whose only recoverable order predated the programme, where the family key
     was kept (`nci_aids_antiviral_screen`, 2026-11-11), and the inventory screen and the company collection at the
     edge of the catalogue case (`qsar_oral_toxicity`, `bioresponse`).
   * **Sources:** Ruiz-Ramírez J, de la Puente M, Xavier C, et al., "Development and evaluations of the ancestry
     informative markers of the VISAGE Enhanced Tool for Appearance and Ancestry", Forensic Science International:
     Genetics 2023;64:102853, <https://doi.org/10.1016/j.fsigen.2023.102853>; the 1000 Genomes phase-1 sample panel,
     <https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase1/analysis_results/integrated_call_sets/integrated_call_samples.20101123.ALL.panel>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the random split over people (implemented) | no change; the finding goes in the notes | the panel's nine populations are fixed and the use case assigns a trace to one of them; no key under the population exists | the project confound stays, which the fit text and the two markers record |
     | B | Split by the 1000 Genomes release phase | train on the phase-1 people, test on those added by phase 3 | follows the one arrival the identifiers recover | the four HGDP classes sit on one side, and 93 of the 139 later arrivals are Iberian, so it tests the project, not time |
     | C | Hold out the reference project | train on 1000 Genomes, test on HGDP-CEPH | the cleanest reading of a wave here | the two sides share no class, so the task cannot be scored |

   * **Recommendation:** A: the panel's growth adds classes, not items, and the only recoverable wave is the
     reference project, which is the label. **Decision:** A, B or C?

   **Notes for the AI:** on A, extend the `Time basis: Timeless:` bullet in `curation_comments` with one sentence
   giving the phase counts above and stating that the recoverable wave is the project, not an entry date; no data,
   split or score changes, `dataset check`, no rebuild. On B or C, the sample identifier would have to be carried
   into the frame as a scoring column, and the class counts of each side checked before anything is declared.
   Query and output: `~/claude_jobs/borderline_splits/force_dates/` (the panel file and the counting script).

   [^4a]: **SPLIT-34** (Should): a dataset drawn from an expanding science catalogue, a cut of a database or testing
     programme that keeps growing, can be split by the item, by its family or by when it entered the catalogue, and
     where the actor predicts for items the catalogue does not hold yet the entry date holds out what a family key
     leaves in. A catalogue that is not growing, a recoverable date that is not the date items entered, and labels
     that are not final each put a dataset outside the case, and there the family key is the one that stands for the
     use case.

   **Resolved (2026-11-12, Andrej):** A: the random split over people stays. The `Time basis: Timeless:` bullet in
   `curation_comments` now gives the phase counts (364 of 503 1000 Genomes people in phase 1, 139 later, 93 of them
   Iberian; the 104 HGDP-CEPH people in no release) and says the recoverable wave is the project, not an entry date;
   record CC line. Data, split and score unchanged; `dataset check` re-run.

## Reference

@article{heinzel2025advancing,
  title={Advancing biogeographical ancestry predictions through machine learning},
  author={Heinzel, Carola Sophia and Purucker, Lennart and Hutter, Frank and Pfaffelhuber, Peter},
  journal={Forensic Science International: Genetics},
  volume={79},
  pages={103290},
  year={2025},
  publisher={Elsevier}
}
