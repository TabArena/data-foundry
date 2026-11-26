---
unique_name: deafness_gene_carrier_hearing_loss
name: Hearing loss among carriers of GJB2/SLC26A4/MT-RNR1 variants (Luo et al. 2021, Mendeley 6mh8mpnbgv)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 1
decision_markers:
- Selection Bias
tags:
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
original_source: Other
year: '2021'
collection_period: Oct 2009 - Aug 2020
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://data.mendeley.com/datasets/6mh8mpnbgv/1
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
- https://doi.org/10.17632/6mh8mpnbgv.1
- https://doi.org/10.1016/j.ebiom.2021.103322
v2_path: datasets/_dev/tabarena-v0pt2/deafness_gene_carrier_hearing_loss/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: real genotype data of a Chinese hereditary hearing loss case-control study (Luo et al. 2021, Mendeley Data, CC BY 4.0), 1,209 + 569 people with variants at 144 sites of GJB2, SLC26A4 and MT-RNR1; the target is hearing-loss patient against variant carrier with normal hearing, not "inheritance" as Shaktah labels it; small, sparse (280 distinct genotype patterns in the 1,209 discovery rows) and with family members among the rows.
- Source: Luo, Li, Xu, Hong, Yang, Chen, Chen, Wu, "Machine learning-based genetic diagnosis models for hereditary hearing loss by the GJB2, SLC26A4 and MT-RNR1 variants", EBioMedicine 69:103322 (2021), doi 10.1016/j.ebiom.2021.103322 (read from Europe PMC, PMC8237285); data: Mendeley Data 6mh8mpnbgv v1, "Data for: Machine learning-based genetic diagnosis models ...", published 2021-03-16, CC BY 4.0. Record description: "The two data sets were processed sequencing data, of which the Discovery Set was from the medical records and the Validation Set was from the Disabled Persons' Federation. PS: No mutations found were indicated by 0, heterozygous mutations by 1, and homozygous mutations by 2". As published (previewed): `Discovery Set.xlsx` 1,209 rows x 145 columns (`Diagnoses` 918 patients = 1 / 291 carriers = 0, 144 variant columns under a gene header row; one cell is a blank string); `Validation Set.xlsx` 569 rows (436 / 133). Every row has 1 to 6 variant alleles (all wild types excluded, Methods). The paper counts 1,898 subjects with 411 discovery carriers; the release holds 1,778, 120 discovery carriers fewer (unexplained; to ask or note).
- Target: Methods, "Sample collection": "the sample data were divided into carriers and HHL patients according to whether they passed the hearing screening test or not ... (1) 1354 patients with GJB2, SLC26A4 and MT-RNR1 hot spot variants who failed the hearing screening test and were diagnosed as HHL; (2) 544 people with GJB2, SLC26A4 and MT-RNR1 hot spot variants who passed the hearing screening test and were diagnosed as HHL gene carriers". So the label is the hearing phenotype of a variant carrier (penetrance / genetic diagnosis), not the mode of inheritance; the record's `unique_name` and Shaktah's "hereditary hearing loss inheritance" misname it (renaming is the curator's call).
- Use case: Interpretation: "an efficient and effective tool for HHL prediction when high throughput sequencing data are available"; actor: a genetic counsellor interpreting a carrier's variants (newborn or family screening) on whether they explain or predict hearing loss; fit approximate (in the clinic the hearing test itself is cheap and the label; the model stands in for expert variant interpretation, which the paper's EI baseline is). Collection: "electronic medical records of 2660 patients and their immediate family members from October 2009 to April 2017" (discovery), no date per row (`Samples: Over Time`, `Time: Lost`); hearing status exists with the genotype (no target tag); family members are among the rows, with no family id (a group key the release lacks); type Clinical Study.
- Split: leaf [L-PLACE.random] (Random · `ForcedIIDFromGrouped`, the transfer untested) because [CLI.meets] the source validates at another recruiting source (the Disabled Persons' Federation and community screening), [PLACE.several] the release holds two sources, one per file, short of the enough-groups check, [PLACE.units] one row per person (families unkeyed). Open: whether to ship the source's discovery-to-validation split (Arasteh and Shaktah both keep it) as a recorded departure; the family clusters, which no id recovers (SPLIT-9).
- Siblings and duplicates: `audiology_diagnosis` (retired `Trivial`, a different task: hearing-loss type from the audiogram), `hbdc_audiogram_air_bone_gap` (audiograms, another task); no record of these genotype files. Arasteh et al. 2024 used the two Mendeley files as its training and test sets ("1209 (76/24)" and "569 (77/23)", Table 1) without changes beyond median imputation; Shaktah et al. 2026 kept that split and dropped training columns with under 0.5% ones (`TabPFN_HearingLoss_CPU.py`). Both are copies (PROV-4, PROV-8): /add-dataset starts from the Mendeley record. External collections: Arasteh et al. 2024; Shaktah et al. 2026.
- Better data: none found (data scout, 2026-11-25: Mendeley, Zenodo, the web). A 2025 newborn screening study of the same genes (Frontiers in Pediatrics, about 15.8k newborns) releases no data and has another use case.
- Papers and pages: Luo et al. 2021 (SVM AUC 0.803 in 10-fold CV, 0.751 external; genetic risk score and expert interpretation baselines); Arasteh et al. 2024 (ChatGPT ADA RF 0.773, re-implemented SVM 0.762); Shaktah et al. 2026 (Bagging 0.758, LR 0.534, TabPFN 0.770).
- Metric: Luo et al.: "The predictive performance of all model types was evaluated by two important classifier performance evaluation indicators in machine learning: the receiver operating characteristic curve (ROC) and area under the curve (AUC)" (Methods), with accuracy, sensitivity, precision and F1 also defined; models ranked by AUC, so `roc_auc`, deliberate or the fallback either way (MET-5, MET-8); inputs none.
- Risks for /add-dataset: a textbook rule exists (Methods: "The GJB2 and SLC26A4 homozygous and compound heterozygous genotypes are deafness-causing genotypes, and MT-RNR1 variants are drug-sensitive genotypes, these two were diagnosed as HHL, while GJB2 and SLC26A4 heterozygotes were diagnosed as carriers"): run it as the rule baseline (TP-4, SEL-5; the paper's expert interpretation scored below the SVM); 280 distinct genotype patterns in 1,209 rows, so many test rows repeat a training pattern (decide whether that is the use case or a duplicate issue, LEAK-19); family members unkeyed (SPLIT-9); case-control recruitment, carriers from screening (`Selection Bias`); the 120 missing carriers; the blank cell in `c.235delC`.
- Priority: gap 0 (medical, binary), use case 0 (approximate, stated only as a tool), source + (paper and CC BY deposit), shape 0 (1,778 rows but one feature type, sparse, 280 patterns), risk - (unkeyed families and pattern repeats).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.

CC (2026-11-25, Andrej): accepted for adding in the screening review (issues 1 A (every person a row; reopen on the added dataset) and 2 A (repeated 3-fold CV)).

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes, made (three recruiting sources, the 53-carrier block's cause unknown, the benign wording with p.T123N, use case and fit reason reworded, the rule baseline by part of the release); disputed: TP-4 step 2, keep all rows (advocate) or the 1,220 with a non-benign variant (critic), and the variant aliases (CLEAN-12; the mediator departs from the panel); for the curator: issues 3-6. Priority 1: gap 0, use case 0 (approximate, penetrance for an untested relative), source + (paper and CC BY deposit), shape 0 (1,778 people, 341 genotypes), risk - (the gain over the rule sits mostly in recruitment-shaped rows).

## Review

**Outcome:** added. 1,778 carriers of GJB2, SLC26A4 or MT-RNR1 variants (Luo et al. 2021, Mendeley 6mh8mpnbgv), hearing loss (76%) from 126 allele counts, every person a row and 10 x 3-fold cross-validation on random people as decided (issues 1 and 2). Valid: no leak, and no attack moves the score beyond noise. Value: the methods beat the textbook rule on all 30 splits, but on the 1,220 people with a variant other than three benign-listed GJB2 polymorphisms gradient boosting only matches it (issue 5). The panel recommends shipping after changes; the wording changes are made, and four questions are yours: the recording marker for a block of 53 carriers (issue 3), the repeated genotypes you asked to reopen (issue 4), where the gain over the rule sits (issue 5) and the variant aliases (issue 6).

**Main points:** Mark the 53-carrier block `Class-dependent Recording` (issue 3); keep every person a row (issue 4, reopened); keep all rows although most of the gain over the textbook rule sits in the people with only benign-listed variants (issue 5); keep or merge the variant aliases (issue 6).

**Issues for Andrej:**


1. **Keep people with the same genotype as separate rows?**

   * **Problem:**
     - The 1,209 discovery rows hold only 280 distinct genotype patterns, so most test people share their genotype with a training person.
     - They are different people (some of them relatives, with no family id), not copies of one record[^leak19].
     - A textbook rule on the genotype (homozygous or compound heterozygous GJB2 or SLC26A4, any MT-RNR1 variant) gives the diagnosis; /add-dataset runs it as the baseline.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep every person (implemented) | rows as released | a new carrier with a common genotype is the use case; genotype frequencies kept | relatives on both sides of a fold |
     | B | Collapse identical genotype and label into one row | drops repeats | no repeated rows | loses how common each genotype is; not copies of one record |
     | C | Group the folds by genotype pattern | each pattern on one side | tests unseen genotypes | not the use case: common genotypes are the ones met |

   * **Recommendation:** A: these are distinct people, and the copies rule is about one record entered twice. **Decision:** A, B or C?

   **Andrej (2026-11-25, ok):** A, but also keep in mind to have this as a discussion item after adding the dataset for the review.

   **Resolved (2026-11-25, Andrej):** A: every person stays a row. /add-dataset reopens the question as an issue in the added dataset's review, with the built data in hand.

   [^leak19]: **LEAK-19** (Should): exact copies with the same label: drop them rather than group on the duplicate key.

2. **Random split, or the source's discovery-to-validation files?**

   * **Problem:**
     - The release has two files from two recruiting sources (medical records; the Disabled Persons' Federation), short of the groups the tree needs, so it reaches a forced random leaf[^split36].
     - Both benchmark papers (Arasteh 2024, Shaktah 2026) kept the two files as train and test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Repeated 3-fold cross-validation on all 1,778 (implemented) | the forced random leaf | varied training sides | transfer to another recruiting source untested |
     | B | The source's split as a recorded departure | train on 1,209, test on 569 | the source's external validation | one training side only |

   * **Recommendation:** A, as for the other two-cohort clinical studies of this batch. **Decision:** A or B?

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: repeated 3-fold cross-validation on all 1,778 people; the source file is no feature.

   [^split36]: **SPLIT-36** (Should): a definition's split is decided by walking the split decision tree; a forced leaf is for the curator to look at.
   [^source]: Source task before our own: the source's own task and split are tested first and preferred when valid.

3. **Mark the 53-carrier block `Class-dependent Recording`?**

   * **Problem:**
     - The discovery file opens with a block of 53 carriers (no patients), none of whom has the common GJB2 polymorphisms p.V27I, p.E114G or p.I203T recorded, while 61% of the other 238 discovery carriers have at least one, so the block was probably typed another way, for a reason the source does not give[^leak39].
     - The record marker `Class-dependent Recording` flags a dataset whose classes were recorded differently, and it is set also when the rows are kept with a note[^marker].
   * **Effect on the task:** small: models give the block's people a lower patient probability (0.55 against a 0.76 base rate), but untuned gradient boosting scores the other test people at ROC AUC 0.733 with the block in training and 0.739 without it (30 splits); the usual test for dropping such rows (do models pick them out among people of both classes?) cannot run, as the block holds carriers only.
   * **Consistency:** pheochromocytoma_paraganglioma_metastasis got the marker the same day for 14 patients with converted plasma values, kept with a note; gallstone_disease got it and dropped its rows, which models recognised at ROC AUC 0.993.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No marker (implemented) | nothing | no change | departs from the marker rule and the same-day precedent |
     | B | Add the marker, keep the rows | marker; the existing note stays | follows the marker rule and the same-day precedent | the route is inferred, not confirmed |
     | C | Add the marker, drop the 53 rows | rows dropped as gallstone_disease did | removes the route | may remove real carriers (18% of the discovery carriers); gallstone's rows were recognised at 0.993, these cannot be tested |

   * **Recommendation:** B: the marker rule asks for it whether the rows stay or go, and dropping them would remove 18% of the discovery carriers for an effect the measurement does not show; the advocate and the critic agree. **Decision:** A, B or C?

   **Notes for the AI:** On B or C: add `Class-dependent Recording` to the record's `decision_markers`; on C also filter the block in `_clean` (discovery rows 3-55, carriers without any of the three polymorphisms at the file's start), update the counts, re-run `dataset check` on the cluster.

   **Andrej (2026-11-26, discuss):** Can we analyze better whether this could be a leak that models may exploit or whether this is part of the task?

   **Answer (AI, 2026-11-26):** an artefact, but a small one: training on the block lifts the shipped score by 0.006 (gradient boosting) to 0.012 (lookup) through the block's own test rows, lowers the other hospital test people's score by up to 0.011, and gives a participant nothing to exploit.

   * **Problem:**
     - The 53 carriers have no polymorphism recorded, likely because they were typed another way, and the block holds carriers only, so their recorded genotypes are probably incomplete for this class alone[^a1].
     - Most of the block holds a single p.V37I allele and nothing else; outside the block that genotype is 77% patients (60 of 78), with the block 53%.
     - In the hospital file, carriers are more common without a recorded polymorphism only because of the block: 25.7% against 22.6% with it, 18.1% against 22.6% without it.
   * **Experiments:** ROC AUC (higher is better) on the shipped 10 x 3-fold splits (30 runs); gradient boosting untuned; the lookup is each genotype's share of patients in training; the rule is the textbook rule without the three polymorphisms; recognition measured out of fold.

     | Measure | Result |
     |---|---|
     | block against the other hospital carriers, from the features (boosting / logistic regression) | 0.922 / 0.934 |
     | the same, among carriers without any polymorphism | 0.829 / 0.835 |
     | people outside the block with the same genotypes as block people | 164 (30% carriers); only 4 block people have a genotype of their own |

     | Model | Trained | All test people | Outside the block | Hospital people outside the block | Block carriers against test patients |
     |---|---|---|---|---|---|
     | gradient boosting | with the block | 0.750 | 0.731 | 0.716 | 0.886 |
     | gradient boosting | without the block | 0.744 | 0.738 | 0.727 | 0.783 |
     | lookup | with the block | 0.776 | 0.758 | 0.741 | 0.907 |
     | lookup | without the block | 0.764 | 0.758 | 0.744 | 0.805 |
     | rule | not trained | 0.677 | 0.670 | 0.686 | 0.725 |

     | Exploit (paired gain over gradient boosting, 30 runs) | All test people | Outside the block |
     |---|---|---|
     | indicator "genotype seen only in the block" | +0.000 (0/30) | +0.000 |
     | knowing who is in the block (not available: rows shuffled, no file column) | +0.021 (30/30) | +0.008 (25/30) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | No marker, keep the rows (implemented) | nothing | no change | the block inflates the score by 0.006-0.012 and is not flagged |
     | b | Add the marker, keep the rows | `Class-dependent Recording` and these numbers in the note | real carriers kept; the effect documented | the most common single-allele genotype keeps a carrier share made up by the block; the other hospital people lose 0.011 |
     | c | Add the marker, drop the 53 rows | marker; the block filtered in cleaning; its own PR | removes a recording that differs by class and cannot be aligned; the genotype-to-label relation is the hospital's again | loses 18% of the hospital carriers (patients 76.2% to 78.5%); the shipped score falls by 0.006-0.012 |

   * **Recommendation:** c: the block's recording cannot be aligned with the other rows, it changes the label share of the most common single-allele genotype, and models use it in the wrong direction for the other hospital people (worse on 28 of 30 runs); b if you would rather keep every carrier. **Decision:** a, b or c?

   [^a1]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned with the other rows; the marker is set whether such rows are dropped, kept with a note or still open.

   [^leak39]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned with the other rows.
   [^marker]: Decision marker `Class-dependent Recording` (selection.md, markers table): the classes were measured, formatted or filled differently; set on kept and retired datasets, whether the artefact was fixed, is kept with a note or is still open.

4. **Keep every person a row, now that the data is built? (issue 1, reopened as you asked)**

   * **Problem:**
     - 341 distinct genotypes among 1,778 people; 1,390 rows repeat a genotype and label; 85% of test people share their genotype with a training person[^leak18].
     - Relatives sit among the rows without a family id; about 22-30 family clusters can be found from the raw row order.
   * **Experiments:** ROC AUC (higher is better) over 30 splits (10 x 3 folds); gradient boosting untuned; the lookup scores a test person by the share of patients among training people with the same genotype (a logistic model for a genotype not seen); the rule is the textbook reading of the genotype. Held out by genotype, no test genotype is ever in training, so the models fall below chance.

     | Split | Gradient boosting | Lookup | Rule |
     |---|---|---|---|
     | random 10 x 3 (shipped) | 0.750 | 0.781 | 0.677 |
     | grouped by recovered family | 0.752 | 0.779 | 0.677 |
     | grouped by exact genotype | 0.41-0.49 | 0.41 | 0.63-0.68 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep every person (implemented) | rows as released | distinct people; a common genotype is the case a counsellor meets; families change nothing | models learn each genotype's share of patients, not what a variant does |
     | B | Collapse to 388 genotype-and-label rows | one row per pair | no repeats | loses how common each genotype is |
     | C | Group the folds by genotype | each genotype on one side | tests unseen genotypes | not the use case; models fall below the rule |

   * **Recommendation:** A, unchanged; every panel agent that looked keeps every person. **Decision:** A, B or C?

   **Andrej (2026-11-26, discuss):** If you say family clusters, do you mean literally related humans? Or just families in the genotypes that might come from humans who have nothing to do with each other in the real world?

   **Answer (AI, 2026-11-26):** literally related people, inferred from the raw file's row order; the data has no family key, so they are likely relatives, not confirmed ones.

   * **Problem:**
     - The paper recruited patients "and their immediate family members" in both sources, and the release keeps no family id.
     - In the raw files, people who share a rare variant sit next to each other far more often than chance, in the pattern of a family entered together: a patient with two different pathogenic alleles next to two carriers with one allele each (the parents), or siblings with the same genotype.
     - Unrelated people who merely share a common genotype are not counted: the clusters link only neighbours within three rows who share a variant carried by at most 30 people.
   * **Experiments:** raw row order of both files; the shipped data is shuffled, so participants never see it.

     | Measure | Observed | By chance |
     |---|---|---|
     | pairs sharing a variant carried by exactly 2 people, within 3 rows | 40% of 28 pairs | 0.8% |
     | the same pairs, within 10 rows | 55% | 2.3% |
     | neighbouring pairs sharing a variant carried by at most 30 people | 16 | 0.45 |
     | clusters recovered (window of 3 rows, variant carried by at most 30 / 60 people) | 22 clusters, 49 people / 30 clusters, 67 people | |
     | same label within a cluster | 0.62-0.64 (the base rate is 0.64); 12 of 22 clusters hold both labels | |
     | ROC AUC, untuned gradient boosting, 10 x 3 folds: random / grouped by cluster | 0.750 / 0.752 | |

   * **Effect on the task:** none measurable: the label does not travel with the family (patients sit next to their carrier parents), and grouping the folds by these clusters leaves the score unchanged. Families that share only common variants (such as c.235delC) cannot be recovered at all.
   * **Recommendation:** nothing changes for issue 4: keep every person a row (A); the relatives note in the definition says the same. **Decision:** agree, or say what to change.

   [^leak18]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so.

5. **Keep all rows although the gain over the textbook rule sits mostly in the people with only benign variants?**

   * **Problem:**
     - The methods beat the textbook rule on all 30 splits, but on the 1,220 people with a non-benign variant gradient boosting only matches it and only the lookup still leads[^tp4].
     - The 558 people whose only variants are the benign-listed GJB2 polymorphisms p.V27I, p.E114G or p.I203T, which the rule calls unaffected, are 83% patients against 73% of the others, a gap that comes mostly from how the validation file recruited its carriers and is small in the hospital's own records.
   * **Experiments:** ROC AUC by group of test people (higher is better), models trained on all rows of each fold, gradient boosting untuned; the mediator's own 10 x 3 stratified draws, so the all-rows scores differ slightly from issue 4's shipped splits:

     | Test people | Rule | Gradient boosting | Lookup | Boosting minus rule (splits ahead) | Lookup minus rule (splits ahead) |
     |---|---|---|---|---|---|
     | All 1,778 | 0.677 | 0.753 | 0.784 | +0.076 (30/30) | +0.107 (30/30) |
     | Hospital file, without the block (1,156) | 0.685 | 0.721 | 0.753 | +0.036 (28/30) | +0.068 (30/30) |
     | Validation file (569) | 0.639 | 0.761 | 0.789 | +0.122 (30/30) | +0.150 (30/30) |
     | Not benign-only (1,220) | 0.782 | 0.779 | 0.822 | -0.003 (13/30) | +0.039 (29/30) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows, state where the gain sits (implemented) | the table above in the notes | a real gain in the hospital rows too; the rule misranks people whose hearing loss no accepted genotype explains | most of the gain on all rows comes from the selection pockets |
     | B | Keep only the 1,220 people with a non-benign variant | rows filtered by a feature value; its own PR | the gain left is the genotype's | the task then sits near trivial for boosting; the test set chosen to suit the rule |
     | C | Retire as `Trivial` | record `No` | none | the lookup still leads the rule on 29 of 30 splits |

   * **Recommendation:** A: in the hospital's own records, where the benign-only people are patients at about the base rate, the methods still beat the rule on 28 to 30 of 30 splits, and B would pick the test set by a feature value to suit the rule. The critic recommends B; a population sample with wild types (newborn screening) would settle it. **Decision:** A, B or C?

   [^tp4]: **TP-4** (Must): `Trivial` needs proof; read what the dominant feature means first, then judge it in two steps, of which only the first is a test.

6. **Merge the variant names that are the same allele?**

   * **Problem:**
     - Some alleles appear under several column names, some names in one file only: GJB2 c.508_511dup under three, SLC26A4 c.916dupG under two, and more sets are probable[^clean12].
     - About 40 people carry one of these names, all at rare sites; a model sees one allele as unrelated columns, but the names do not separate the classes.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the files' columns, note the alias sets (implemented) | columns as released; a note listing the sets (not yet written) | fix only what separates the classes for non-target reasons[^minimal] | one allele spread over columns |
     | B | Merge the certain sets, maximum per person | fewer columns; its own PR | how an expert would ship the data; names no longer split by file | a feature change |

   * **Recommendation:** A: the aliases touch about 40 people at rare sites and do not separate the classes, so by your line on minimal preprocessing they stay as released, with a note; the advocate, the critic, the column auditor and the blind reviewer favour B, and the mediator departs from them on this ground. **Decision:** A or B?

   **Notes for the AI:** On A: add a note to `curation_comments` listing the certain alias sets (GJB2 `c.507insAACG`, `c.507_508insAACG`, `c.512insAACG`; SLC26A4 `c.915insG`, `c.915_916insG`) and the probable ones from the mediator's report. On B: merge the certain sets in `_clean` by the maximum allele count per person, one column per allele, update the site counts in the notes, re-run `dataset check`.

   [^clean12]: **CLEAN-12** (Should): reconstruction that restores what the file split (codes into categories, dates split across columns) is always welcome.
   [^minimal]: The curator's line on minimal preprocessing (Andrej): fix what separates the classes for non-target reasons, nothing more.

7. **Split: a grouped split instead of random folds?**

   * **Problem:**
     - The data supports few groupings: two source files, three recruiting sources of which the community screening is unmarked (no proxy found in the row order or the genotypes), 22 recovered family clusters (49 people), the 53-carrier block, and the exact genotype, which is similarity, not a group of people[^b1].
     - The issues sit in who was recruited per class inside each file, which no split removes; a counsellor mostly meets common genotypes, and each fold needs its own training side[^b2].
   * **Background:** your note on the split (Andrej, 2026-11-26): "It seems like there are several issues due to different collection routines in the dataset and subgroups in the dataset. Could we get rid of issues by designing a grouped split somehow?"
   * **Experiments:** ROC AUC (higher is better); gradient boosting untuned; lookup = each genotype's share of patients in training; rule = textbook rule without the three polymorphisms; the 10 x 3-fold rows give the mean over 30 runs, the file rows each fold.

     | Split | Groups | Folds | Removes | Gradient boosting | Lookup | Rule | Ahead of the rule (boosting / lookup) |
     |---|---|---|---|---|---|---|---|
     | random 10 x 3 (implemented) | 1,778 people | 30 | nothing | 0.750 | 0.776 | 0.677 | 30/30, 30/30 |
     | recovered families | 1,751 | 30 | relatives on both sides | 0.749 | 0.780 | 0.677 | 30/30, 30/30 |
     | families plus the block as one group | 1,699 | 30 | relatives; the block informing its own test rows | 0.739 | 0.769 | 0.676 | 30/30, 30/30 |
     | exact genotype | 341 | 30 (test sides 203-1,016) | repeated genotypes (the use case) | 0.498 | 0.401 | 0.677 | 2/30, 0/30 |
     | source file, discovery to validation | 2 | 1 of 2 | source overlap | 0.747 | 0.776 | 0.639 | |
     | source file, validation to discovery | 2 | 2 of 2 | source overlap | 0.672 | 0.724 | 0.695 | |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random 10 x 3-fold over all people (implemented) | as shipped | varied training sides; common genotypes on both sides, as in the use case | relatives and, if kept, the block on both sides |
     | B | 10 x 3 folds grouped by recovered families, the block as one group | the 22 clusters and the block each on one side | relatives never split; the block cannot score itself (-0.013) | clusters inferred from row order; test sizes 538-646; moot if the block is dropped |
     | C | The source's file split, as a recorded departure | train on one file, test on the other, both ways | the transfer the source tested | two fixed training sides, one half the size; the rule beats boosting from validation to discovery; the community subgroup stays mixed in |
     | D | Grouped by exact genotype | each genotype on one side | tests unseen genotypes | not the use case; models fall below chance and below the rule |

   * **Recommendation:** A, with the block dropped as recommended under issue 3: no grouping removes the selection, which sits in the labels of both files, and grouping by family leaves the score unchanged (0.749 against 0.750); if the block stays, B. **Decision:** A, B, C or D?

   [^b1]: **SPLIT-24** (Must): group on a true group id, or on one constructed from the data exactly or by a calibrated link whose match rule comes from how the data were recorded, never from the score.
   [^b2]: Folds that share one training side are one split; the training side must vary across folds.

**Review panel:** ship after changes (mediator). Claims: 34 tested, 28 hold, 4 refuted (the 53-carrier block's cause, three sources not two, the collection period, the benign wording; all reworded), 2 untested. Blind review: include with changes. Task gamer: not gameable, no exploit above ±0.0024. Agreed: no leak, the split, every person a row, the marker for the 53-carrier block. Disputed: where the gain over the rule counts (issue 5); the mediator departs from the panel on the aliases (issue 6).

<details><summary>Mediator</summary>

**mediator: deafness_gene_carrier_hearing_loss (2026-11-25)**

Tier `full`: claim auditor, column auditor, split auditor, domain practitioner, precedent checker, blind reviewer,
task gamer, advocate and critic (each with one rebuttal), mediator. One decisive experiment run (a cluster run), results in
`subset_gain.json` next to it).

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL holds (CC BY 4.0, real genotypes; the blind reviewer and the task gamer rebuilt the table from Mendeley
  and found the (genotype, label) multiset identical). USE-1 approximate holds (USE-8: selection alone does not make
  it None); use_case and fit_reason reworded (change 7). LEAK: no column leak, nothing to game (task gamer, 13 attack
  families, all within ±0.0024). LEAK-18/19/20: repeated genotypes are distinct people, kept (issue 2, reopened as
  the curator asked). LEAK-39 marker: the 53-carrier block, kept, marker for the curator (issue 1). SPLIT-36
  L-PLACE.random holds (forced, decided 2026-11-25); the family proxy and the source split show no optimism; the
  "two sources" reason is wrong in wording only (three sources, still too few; change 2).
Value: TP-4 step 1 passes (methods ahead of the textbook rule on 30/30 splits); step 2 is the curator's (issue 3).
  The gain is real in the hospital's own records too (HGB +0.036, lookup +0.068), not only in the selection pockets.
Quality: one allele split over several columns (issue 4, CLEAN-12, Should); wording fixes from the claim audit.
Weighed: source +, size 0, selection -, gap 0.
For the curator: issue 1 (marker), issue 2 (repeats, reopened), issue 3 (TP-4 step 2, all rows or the 1,220),
  issue 4 (merge the variant aliases).
```

**Changes to make now (no decision needed)**

All wording or record metadata; none changes rows, features, target, split or metric.

1\. **The 53-carrier block's cause** (curation_comments, "recording by class" anomaly; EV-6, PROV). Replace "(the
   community NGS screening, unconfirmed)" with "cause unknown: the paper's community NGS screening is in the
   validation file (Table 1), and the discovery file is the hospital's Sanger-sequenced records". In the selection
   note, the sentence "The paper adds carriers from a community's NGS hotspot screening at the same hospital to offset
   the patients" must say these 103 people are in the validation file (Table 1: 2020.5-2020.8, NGS hotspot).
2\. **Three sources, not two** (group_basis, splits_comment, task_summary.split; SPLIT-36 reasoning, PROV). The
   validation file holds 466 people of the Disabled Persons' Federation (Sanger, 2011.8-2017.4) and 103 of a community
   screening (NGS hotspot, 2020.5-2020.8), with no column or row block that tells them apart; three sources are still
   too few for a grouped split, so the leaf stands. In time_basis, replace "Not tested: carriers screened later, or with
   another sequencing panel that finds other variants" with: a second panel (NGS hotspot, 96% site overlap) is already
   in the validation file for 103 people screened in 2020, unmarked; carriers from other panels or clinics are not
   tested.
3\. **Record `collection_period`**: `Oct 2009 - Aug 2020` (Table 1; the discovery file alone is Oct 2009 - Apr 2017,
   as time_basis already says). Add `Andrej` to `checked_by` (already there).
4\. **Benign wording** (selection note; EV-6/EV-7). Write: p.V27I, p.E114G and p.I203T are benign in DVD; in ClinVar
   p.I203T is benign and the other two are of uncertain significance; the paper calls them "widely regarded as benign"
   but contested (homozygous p.V27I/p.E114G linked to mild-to-moderate loss; our 63 double homozygotes are 84%
   patients). Replace "Their hearing loss is not explained by these genes" with "not explained by an accepted
   pathogenic genotype". Add p.T123N (40 carriers, ClinVar likely benign/benign): with it the benign-only group is 581
   people, 83.1% patients against 72.8% (the conclusion stands).
5\. **The source-split sentence** (splits_comment). After "0.750 against 0.750" add: "in the source's direction;
   trained on the validation file and scored on the discovery file, a training side half as large, it scores 0.672,
   below the expert-like rule (0.695)".
6\. **Where the gain over the rule sits** (rule-baseline note, TP-4). Add the mediator's per-part numbers (table under
   issue 3): in the hospital file without the 53-carrier block, rule 0.685, untuned gradient boosting 0.721, lookup
   0.753 (ahead on 28/30 and 30/30); in the validation file 0.639, 0.761, 0.789. Benign-only people are 0.816
   patients in the hospital file (others 0.784) and 0.857 in the validation file (others 0.721).
7\. **use_case and fit_reason** (USE-1, USE-5, USE-8; advocate, critic and domain practitioner agree). use_case: the
   counsellor estimates whether a person's GJB2, SLC26A4 and MT-RNR1 genotype predicts hereditary hearing loss for a
   relative or newborn whose hearing is not yet tested, in place of the expert's rule-based reading. fit_reason adds:
   the label is hearing status at one screening, not the lifetime outcome for p.V37I (reduced penetrance), SLC26A4
   (progressive loss) and MT-RNR1 (aminoglycoside exposure) carriers; the controls are partly obligate-carrier parents;
   people carrying only the common GJB2 polymorphisms are mostly patients because of who was sequenced. The fit stays
   `approximate`.
8\. **Relatives** (curation_comments, repeats note; LEAK-42/43). Add: about 22-30 small family clusters can be found
   from the raw order (neighbouring rows sharing a rare variant, 49-67 people); the label does not travel with them
   (trios of a biallelic patient and two carrier parents), and grouping the folds by them leaves ROC AUC unchanged
   (untuned gradient boosting 0.752 against 0.750, split auditor).
9\. **Small notes.** The comment's `c.919-2A>G` is the column `SLC26A4_c.919_2A>G` as the files write it (say so once,
   or write the column name). MT-RNR1 `c.1438G>A` (2 people) is the haplogroup polymorphism m.1438A>G, so "any MT-RNR1
   variant" in the rule baseline is too broad for it; one clause. Keep the blank `GJB2_c.235delC` cell missing (CLEAN-10;
   the task gamer's "impute 0" would invent a value; the missing-indicator gain is 0.0000).
10\. **Tooling, not the definition**: the generated README lists `HearingLoss` under "Feature types: categorical (1)"
    instead of `source_file` (claim auditor). A generator quirk for the main session, not a dataset change.

**Issues for the curator (ranked)**

**1. `Class-dependent Recording` marker for the 53-carrier block (P4, marker under LEAK-39)**

- **Problem:** the discovery file opens with 53 carriers, none recorded with p.V27I, p.E114G or p.I203T (61% of the
  other 238 discovery carriers, 54% of the patients), so they were likely recorded another way; the cause is unknown
  (the stated NGS cause is refuted, change 1). The marker rule sets the marker "whether the artefact was fixed, is kept
  with a note or is still open". The definition writes "recording by class, kept" but the record has no marker.
- **Effect:** small: other test people score 0.733 with the block in training and 0.739 without it (paired -0.0065,
  sd 0.0094); the block's people get a patient probability of 0.55 against 0.76. Without the block, all rows: rule
  0.670, gradient boosting 0.735, lookup 0.766 (mediator).
- **Evidence both sides:** advocate and critic agree on (a). LEAK-39's drop test cannot run: the block has no
  patient. Precedents: pheochromocytoma_paraganglioma_metastasis (same day, marker for a fixed artefact),
  gallstone_disease (marker, route dropped at 0.993 recognition); pancreatic_cancer_mouse_detection kept `Selection
  Bias` only because both classes shared one route.
- **Options:** (a) add the marker, keep the rows, the note becomes the marker's note; (b) add the marker and drop
  the 53 rows (18% of discovery carriers, for an effect the measurement does not show); (c) no marker (departs from the
  marker rule and the same-day precedent with no distinguishing fact except that the route is unconfirmed).
- **Recommendation:** (a).

**2. Repeated genotypes and relatives (P4, LEAK-18/19/20, Should; reopened as the curator asked on 2026-11-25)**

- **Problem:** 341 genotypes among 1,778 people; 85% of test people share their exact genotype with a training person;
  relatives sit on both sides with no family id.
- **Effect, measured:** grouping by a recovered family proxy: 0.752 against 0.750 (no optimism). Genotype-grouped
  folds: models 0.41-0.49, below the rule (0.63-0.68), because no held-out genotype is ever seen (a similarity key, not
  a group; SPLIT-24). The source's file split scores like random (0.750).
- **Evidence both sides:** every agent that looked (advocate, critic, split auditor, task gamer, blind reviewer)
  keeps every person; the blind reviewer and practitioner ask only that the lookup nature be documented (it is).
  Precedents: sepsis_survival, ai4d_lab_tanzania_tourism, hiva_agnostic (distinct entities with the same vector
  stay).
- **Options:** A keep every person (implemented); B collapse identical genotype+label; C group by genotype.
- **Recommendation:** A, unchanged; add change 8.

**3. TP-4 step 2: does the gain over the textbook rule matter? (P6, TP-4 Must; step 2 is the curator's)**

- **Problem:** the methods beat the paper's expert reading on every split, but most of the all-rows gain sits in the
  558 people (31%) who carry only the common GJB2 polymorphisms: the rule calls them unaffected and 83% are patients.
  Without them, gradient boosting only matches the rule; the lookup still leads.
- **Decisive experiment (mediator, own 10x3 stratified draws, models trained on all rows of each fold, scored by
  part):**

  | Test people | n | Rule (polymorphisms not counted) | Untuned gradient boosting | Genotype lookup | GB - rule (sd, ahead) | Lookup - rule (sd, ahead) |
  |---|---|---|---|---|---|---|
  | All | 1,778 | 0.677 | 0.753 | 0.784 | +0.076 (0.019, 30/30) | +0.107 (0.017, 30/30) |
  | Hospital file without the 53-carrier block | 1,156 | 0.685 | 0.721 | 0.753 | +0.036 (0.022, 28/30) | +0.068 (0.023, 30/30) |
  | Validation file | 569 | 0.639 | 0.761 | 0.789 | +0.122 (0.035, 30/30) | +0.150 (0.033, 30/30) |
  | Without the benign-only people, all | 1,220 | 0.782 | 0.779 | 0.822 | -0.003 (0.025, 13/30) | +0.039 (0.021, 29/30) |
  | Without the benign-only people, hospital file | 787 | 0.781 | 0.765 | 0.808 | -0.016 (0.030, 10/30) | +0.027 (0.028, 26/30) |

- **What it settles (the disputed fact):** the critic is right that the selection widens the gain: it is three times
  larger in the validation file, whose carriers were recruited for a hotspot variant. The advocate is right that it is
  not only selection: in the hospital's own records, where benign-only people are patients at about the base rate
  (0.816 against 0.784), the methods still beat the rule on 28-30 of 30 splits, because the rule ranks those people
  last. Outside the benign-only group the lookup's lead (+0.027 to +0.039) is the graded penetrance of p.V37I and the
  MT-RNR1 carriers, where the practitioner places the clinical uncertainty.
- **Rule:** TP-4 step 1 passes on all rows (no `Trivial` proof; a match only on the 1,220 for gradient boosting, and
  the lookup leads there too). Step 2 is a weighing the AI does not settle. Restricting rows to where the rule is
  strongest is not on the remedy ladder for a step-2 doubt: no Must is broken.
- **Options:**
  - (a) keep all rows; changes 6 and 7 state where the gain sits (advocate, practitioner's C).
  - (b) restrict to the 1,220 people with a non-benign variant (a task change, its own PR); gradient boosting then
    matches the rule and only the lookup leads, so the task sits near `Trivial` (critic).
  - (c) retire as `Trivial` (no one supports it: the lookup leads on 29/30 even on the 1,220).
- **Recommendation:** (a). The hospital rows show the gain is not only an artefact of recruitment, and (b) removes the
  rows the rule gets wrong by a feature value, which selects the test set to suit the rule. What would change it: a
  population-based sample (newborn or community screening with wild types) where benign-only people sit at the
  population rate.

**4. One allele split over several columns (P7, CLEAN-12, Should)**

- **Problem:** the files name some variants several ways. Certain: GJB2 c.508_511dup as `c.507insAACG` (17),
  `c.507_508insAACG` (3, discovery only), `c.512insAACG` (2, validation only); SLC26A4 c.916dupG as `c.915insG` /
  `c.915_916insG`. Probable: `c.36insG` / `c.35_36insG` (one carrier has both), `c.1546insC` / `c.1548insC`, the two
  del7666 names, GJB2-style names in the SLC26A4 block (`c.508insAACG`, `c.234_235delC`). About 40 people, rare sites.
- **Effect:** a model sees one allele as unrelated sparse columns, partly split by file. Not by class: the file is
  told from the genotype only at 0.58, and no check shows the names separating the classes. Score effect small.
- **Evidence both sides:** advocate, critic, column auditor and blind reviewer favour merging the certain sets (max
  over aliases). Against: the curator's standing line on minimal preprocessing (credit_g 2026-10-15; gallstone
  2026-10-21: fix only what lets a model separate the classes for non-target reasons, keep and document the rest).
- **Options:** (a) keep the files' columns, list the alias sets in curation_comments; (b) merge the certain sets into
  one column each (max per person), note the probable ones (a feature change, its own PR); (c) (b) plus the probable
  sets.
- **Recommendation:** (a), by the curator's minimal-preprocessing line, which the panel did not weigh; (b) is the
  panel's agreed choice and is safe if the curator reads the aliases as wrong rather than unhelpful.

**Disputed points**

Only one survives the rebuttals: issue 3 (TP-4 step 2). The advocate rests on the remedy ladder (a note before a
change of rows) and on the hospital rows; the critic on `Selection Bias` ("judge the model comparison on the data")
and on the validation file's wider gap. Both concede no Must forces (b). The experiment above confirms both factual
claims; what remains is a weighing, the curator's. Issue 4 is a departure of mine from the panel's agreement,
grounded in the curator's standing preference; the curator decides.

**Agreed facts**

- 1,778 people (1,209 discovery: 918 patients, 291 carriers; 569 validation: 436, 133); the table equals the Mendeley
  files row for row as multisets; CC BY 4.0. 120 discovery carriers of the paper are missing, cause unknown.
- 144 sites, 16 constant and 2 copy columns dropped, 126 shipped; values 0/1/2 allele counts, MT-RNR1 0/1; one blank
  cell shipped missing.
- 341 genotypes; 85% of test people share a training genotype; 47 genotypes carry both labels (penetrance).
- Validation file = 466 DPF (Sanger) + 103 community NGS (2020), unmarked; discovery = hospital records, Sanger.
- Discovery to validation: 0.750 (as random); reverse 0.672 on half the training side; file from genotype 0.58.
- Family proxy grouping: no change (0.752 vs 0.750). Row order shuffled.
- Rule (polymorphisms not counted) 0.677; gradient boosting 0.750; lookup 0.78; per-part numbers in issue 3.
- `roc_auc` fallback is right (the paper ranks by AUC, no threshold or cost); every fold holds 141+ negatives.
- No exploit: the task gamer's best honest model is the lookup (0.7785); its ceiling near the leave-one-out group mean
  (0.775).

**Task gamer's exploits mapped**

The definition has no `Potential leak, kept on purpose:` note and no accepted warnings; the relevant notes are the
repeats note (LEAK-19), the blank cell and the row order.

| # | Exploit | Gain | Rule | Known? |
|---|---|---|---|---|
| 1 | Pseudo-labelling the test rows | +0.0016 | LEAK-30 (transductive) | new, nil |
| 2 | Genotype-group size over train+test | -0.0024 | LEAK-30 | new, nil |
| 3 | Allele frequencies / ranks over all rows | -0.0007 | LEAK-30 | new, nil |
| 4 | Missing sentinel of the blank cell | 0.0000 | LEAK-13/14 (format by class), CLEAN-10 | known (blank-cell anomaly note), size as noted |
| 5 | Row position / neighbour labels | 0 | order (time probe), SPLIT | known (rows shuffled, note), size as noted |
| 6 | Train-vs-test composition | 0 (AUC 0.49) | SPLIT-36 | new, nil |
| 7 | Restoring the 2 dropped copy columns | 0.0000 | CLEAN-5 | known (drop note), size as noted |
| - | Genotype lookup | +0.032 over LightGBM | LEAK-18/19 (the task itself) | known (repeats note, lookup 0.781); the gamer's 0.7785 matches |
| - | Matching rows to the public Mendeley files | 0.893 | none (any public dataset) | not a dataset flaw |

None is an issue: no known exploit differs in size from its note.

**Consistency with precedent**

- Followed: TP-4 keep on a real gain (differentiated_thyroid_cancer_recurrence, thyroid_discordant; against
  sepsis_survival's 0.001 and ljubljana's match). `Selection Bias` kept (wild_type_attr_cardiac_amyloidosis,
  gallstone_disease). Repeats kept (sepsis_survival, tanzania_tourism, hiva_agnostic). Forced random split over two
  cohorts (pheochromocytoma_paraganglioma_metastasis, wild_type_attr_cardiac_amyloidosis, both 2026-11-25).
- Departure as implemented: no `Class-dependent Recording` marker for the block, against pheochromocytoma and the
  marker rule; issue 1 asks the curator.
- New ground: no precedent covers a gain over a rule concentrated in rows whose labels the selection shapes (precedent
  checker); issue 3's decision becomes the case.
- Implementation difference, not a departure: `source_file` is a provenance `NonFeature` here, while pheochromocytoma
  drops its cohort flag; same decision. Either align pheochromocytoma later or leave it (precedent checker's (a)).
- The blind reviewer's wish for 5- or 10-fold CV departs from the curator's 10x3 decision of 2026-11-25 (issue 2 of
  the screening review); not raised again.

</details>

<details><summary>Claim audit</summary>

**Claim audit: deafness_gene_carrier_hearing_loss**

Scope: 34 claims (task_summary, curation_comments, splits_comment, time/group basis, metric, record screening/assessment). **28 hold, 4 refuted or overstated (all wording or provenance; no change to the task, split or metric), 2 untested.**

Evidence: the raw files re-read independently (`claim-auditor_work/raw_checks.py`, `clean_checks.py`, `validation_checks.py`); the paper's full text from Europe PMC (`claim-auditor_work/paper/full.txt`); the Mendeley public API; the metric and rules scored on the **shipped** splits (`metric_check.py`, login node, no fitting); the model claims re-run on the shipped splits in a cluster run ((a script in the run folder) -> `claim-auditor_work/rerun.json`).

**Refuted or overstated (ranked)**

1\. **The 53-carrier block is attributed to "the community NGS screening" (curation_comments, the "recording by class" anomaly), but the source puts that screening in the validation file.** Luo et al. Table 1: "Internal 10-fold cross validation (n = 1329): Hospital electronic medical records, 2009.10–2017.4, Sanger sequencing | External validation (n = 569): Disabled persons' federation, 2011.8–2017.4, Sanger | Community screening, 2020.5–2020.8, NGS hotspot screening". By sex: 682+647 = 1,329; 243+223 = 466 DPF; 103 community (all female, age 27 ± 4); 466+103 = 569. So the discovery file is all Sanger-sequenced hospital records. The block itself holds: 53 leading carriers, 0 with p.V27I/p.E114G/p.I203T, 36 with one p.V37I allele, 9 with one c.919-2A>G allele, and 61% of the other 238 discovery carriers carry one of the three. Only the guessed cause is wrong. What it changes: wording only; the block result (0.733 vs 0.739) stands. Mildest remedy: replace "(the community NGS screening, unconfirmed)" with "cause unknown; the paper's community NGS screening is in the validation file (Table 1)". Rule: EV (claims match the source), PROV.
2\. **"Two recruiting sources, one per file" (group_basis; splits_comment "The two files are two recruiting sources").** Per Table 1 the validation file mixes two sources: 466 DPF people (Sanger, 2011–2017) and 103 community screenees (NGS, 2020). No column marks them, and I found no row-order block (validation carriers spread over rows 11–563; P(has a benign polymorphism) is 0.47 for carriers and 0.51 for patients). There are three sources, one of them unidentifiable, so the conclusion still holds: too few sources for a grouped split. What it changes: the stated reason and the time_basis "Not tested: ... another sequencing panel". A different panel is already in the data, unkeyed: 103 of the 569 validation people. Remedy: say "two files, three sources (the validation file holds the DPF and a 2020 community NGS screening, 103 people, not marked)". Rule: SPLIT-36 (forced-leaf reasoning recorded correctly), PROV.
3\. **The record's `collection_period: Oct 2009 - Apr 2017` covers the discovery set only.** The validation set runs 2011.8–2017.4 (DPF) and 2020.5–2020.8 (community), so the release spans Oct 2009 – Aug 2020. The time_basis sentence itself is scoped correctly ("the discovery people were seen from …"). Remedy: set the record field to Oct 2009 - Aug 2020, or note the 2020 batch. Rule: record metadata (collection facts).
4\. **The selection note overstates the benign reading: "the GJB2 polymorphisms … which the paper's experts read as benign (Discussion; DVD and ClinVar) … Their hearing loss is not explained by these genes".** The paper says p.V27I and p.E114G are "benign genotypes in the DVD database and variant of undetermined significance in the ClinVar database"; only p.I203T is benign in both. It then adds: "Although they are widely regarded as benign variants, there is still some controversy", citing Chen et al.: homozygous p.V27I/p.E114G is associated with mild-to-moderate HHL. The data echo this: the 63 people homozygous for both are 84% patients. The counts hold exactly: 558 benign-only people, 82.97% patients; 1,220 others, 73.03%. The inference "the label says who was sequenced, not what the genotype does" is an interpretation, not a tested fact. Remedy: write "benign in DVD (p.I203T also in ClinVar; the other two VUS there), contested by the paper itself (Discussion)" and soften "not explained" to "not explained by an accepted pathogenic genotype". The rule-baseline and Selection Bias conclusions are unaffected. Rule: EV-6/EV-7 (claim stronger than its evidence), SEL.

**Untested**

- Why 120 discovery carriers are missing (paper 411, release 291): the counts hold (Table 1 internal n = 1,329 = 918 + 411; the release has 918 + 291). The paper and the record give no cause, and nothing in the data can decide it.
- How many relatives there are: the paper says "patients and their immediate family members" for both the hospital and the DPF. No family id exists, so their number cannot be tested.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Discovery 1,209 rows (918 / 291), validation 569 (436 / 133) | comments, task_summary | raw read | holds | exact | PROV |
| 2 | 144 sites: 47 GJB2, 90 SLC26A4, 7 mtDNA = MT-RNR1 | comments | header row 1; paper Methods quote | holds | identical headers in both files | PROV |
| 3 | Values are 0/1/2 allele counts; MT-RNR1 only 0/1 | comments | value set | holds | {0, 1, 2}; mt max 1; Mendeley description quoted verbatim | — |
| 4 | Every row has 1–6 variant alleles | record | row sums | holds | min 1, max 6 | — |
| 5 | 16 sites carried by no one | comments | constant columns | holds | 16 listed | — |
| 6 | p.G160S ≡ p.N206S (one patient); c.1541T>C ≡ c.1519_1520insCA (two validation people) | comments | pairwise column equality | holds | the only two duplicate pairs; 1 discovery patient; 2 validation people (1 patient, 1 carrier) | — |
| 7 | 126 sites remain; 95 carried by < 5; 17 validation-only; 73 discovery-only | comments | counts | holds | 126 / 95 / 17 / 73 | — |
| 8 | One blank cell, `GJB2_c.235delC`, discovery sheet row 497, a patient with one SLC26A4 p.G222V allele | comments, known | raw scan | holds | value `' '`; only other variant p.G222V = 1 | — |
| 9 | 1,778 of the paper's 1,898; all 1,354 patients here; 120 discovery carriers missing | comments | paper Methods / Table 1 | holds (cause untested) | 918 + 411 internal in the paper | PROV |
| 10 | 341 distinct genotypes (280 in discovery); 1,390 repeat genotype + label; 47 mixed-label genotypes held by 1,100 people | comments | recount | holds | exact | LEAK-19 |
| 11 | Rows include immediate family members, no family id | comments, task_summary | paper Methods | holds (count untested) | "2660 patients and their immediate family members"; "895 patients and their immediate family members from the DPF" | SPLIT-9 |
| 12 | 558 benign-only people, 83% patients vs 73% of 1,220 others | comments | recount | holds | 558: 0.830; 1,220: 0.730 | SEL |
| 13 | The three polymorphisms are read as benign by the paper's experts (DVD, ClinVar); their HHL is not explained by these genes | comments | paper Discussion | **overstated** | VUS in ClinVar for V27I/E114G; "still some controversy" | EV-6 |
| 14 | Paper adds community NGS hotspot carriers to offset the patients; "most samples were HHL"; 96% site overlap | comments | paper text | holds | verbatim quotes found | — |
| 15 | Class-only sites no more than chance: 71 vs 65.6, 10 vs 15.0 | comments | hypergeometric recount | holds | 71 / 65.6; 10 / 15.0 | — |
| 16 | 53-carrier block at sheet rows 3–55; 36 one p.V37I, 9 one c.919-2A>G; none with the 3 polymorphisms vs 61% of 238 others, 54% of patients | comments | recount | holds | 0 / 53; 0.609 of 238; 0.541 of discovery patients | — |
| 17 | The block is the community NGS screening (unconfirmed) | comments | paper Table 1 | **refuted** | community NGS = 103 people in the validation set, 2020 | PROV |
| 18 | Block: 0.55 mean predicted vs 0.76; 0.733 with vs 0.739 without (30 splits) | comments | experiments_block.json; script read | holds (builder's own draws; not re-run) | script correct: train-side exclusion, same test rows | — |
| 19 | Order drift = this block plus a run of patients mid-validation | comments | label runs | holds | 110-patient run, validation sheet rows ≈ 199–308 | — |
| 20 | Textbook rule AUC 0.652; 0.677 without the 3 polymorphisms | comments (TP-4) | rule scored on the **shipped** splits | holds | 0.652 ± 0.018; 0.677 ± 0.010 | TP-4 |
| 21 | The rule is the paper's stated reading | comments | paper Methods | holds | verbatim; the paper's EI also classes benign-variant carriers as carriers, so the "without the 3" rule is the closer EI analogue (the paper's EI also weights p.V37I by Table S3 probabilities) | TP-4 |
| 22 | Untuned GBM 0.750, lookup 0.781, ahead of the rule on all 30 folds | comments | re-run, shipped splits | holds | HGB 0.749, lookup 0.778–0.781; ahead 30/30; lookup > HGB 30/30; default LightGBM 0.742 | TP-4 |
| 23 | Without the 558: rule 0.782 ≈ GBM 0.774 (GBM ahead 10/30); lookup +0.026 | comments | re-run, shipped folds restricted | holds | rule 0.782, HGB 0.776, HGB ahead 11/30 | TP-4 |
| 24 | Discovery → validation GBM 0.750, same as random | splits_comment | re-run | holds | 0.7500 | — |
| 25 | File from genotype, AUC 0.58 | splits_comment | re-run with HGB | holds | 0.579 (builder used LR: 0.578) | — |
| 26 | 85% of test people share their genotype with a training person | splits_comment | shipped splits | holds | 0.847 ± 0.015 | LEAK-19 |
| 27 | Held out by genotype: models 0.41–0.49, rule 0.63–0.68 | splits_comment | re-run, other seeds | holds | HGB 0.470, LR 0.421; rule 0.638 / 0.682 | — |
| 28 | Two recruiting sources, one per file | group_basis, splits_comment | paper Table 1 | **refuted** | 3 sources: validation = 466 DPF + 103 community NGS | SPLIT-36 |
| 29 | Discovery seen Oct 2009 – Apr 2017; no date per person | time_basis | paper | holds | Table 1 | — |
| 30 | Record `collection_period: Oct 2009 - Apr 2017` | record | Table 1 | **refuted** | release spans to Aug 2020 | — |
| 31 | Target = failed hearing screening + HHL diagnosis vs passed carrier; 76% | task_summary, comments | paper Methods; recount | holds | quotes verbatim; 0.7615 | — |
| 32 | License CC BY 4.0; deposit 2021 | sources | Mendeley public API | holds | `data_licence: CC BY 4.0`, published 2021-03-16 (the article itself is CC BY-NC-ND; irrelevant for the data) | — |
| 33 | `source_file` is no feature | non_features | `from_definition` feature cols | holds | 126 features, `source_file` not among them | — |
| 34 | Metric: ROC AUC fallback; the paper reports acc/sens/prec/F1/AUC with no threshold or cost fixed | metric | paper §2.5, Results; MET-2 dummy scoring | holds | quote verbatim; no threshold given (the paper states a preference "to sacrifice specificity for sensitivity" but fixes none); each shipped test fold has 592–593 rows, 451–452 positives, 141–142 negatives; constant prediction scores 0.500 and random ≈ 0.50 with the library's `score` | MET-5, MET-8, MET-2 |

**Metric (MET-2), in short**
Unit = person = row; no inputs; every shipped fold holds both classes in quantity (≥ 141 negatives); a dummy scores 0.5. Target and classes are the paper's, and the class balance matches (76% vs the paper's 71% of 1,898, the gap being the 120 missing carriers). The paper's CV is 10-fold while ours is 3-fold, so its 0.803 is not directly comparable; our honest models give 0.75–0.78. The paper ranks by AUC and leans on sensitivity, but names no threshold, so the fallback is correct.

**Implied claims checked**
- Every feature is known at the prediction point: yes (germline genotype).
- No row is a copy across the split except true repeats of genotype (settled by the curator, issue 1 A).
- The split is the one the use case needs: forced random, settled (issue 2 A). New fact for it: the validation file is itself two sources, one of them on a different sequencing panel and four years later, so discovery → validation already tests a panel change for 103 people. It still scores like random (0.750).

Minor, cosmetic: the comment writes `c.919-2A>G` where the column is `SLC26A4_c.919_2A>G` ("as the files write the variant"). In the generated README, "Feature types: categorical (1)" lists `HearingLoss`, not the declared `source_file` (a generator quirk, not a dataset claim).

</details>

<details><summary>Column audit</summary>

**column-auditor: deafness_gene_carrier_hearing_loss**

Scope: the two Mendeley files (both read by `_load_raw`; the record holds no other file), 144 raw site columns -> 126 shipped + `source_file` (non-feature) + target. Light pandas on the login node only (no model fit); scripts and site table in `panel/column_auditor/` (`column-auditor_sites.csv` = per-site carriers/homozygotes/patients by file). Paper read from Europe PMC (PMC8237285); Supplementary Tables S1/S2 (the site list) not obtained. dtype probe flagged nothing.

**Column table (grouped; every shipped column falls in one row)**

| column(s) | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `HearingLoss` | failed hearing screening + HHL diagnosis (1) vs passed, carrier (0) | target | `Diagnoses` 0/1 decoded No/Yes; counts 1,354/424 match paper's patients, carriers short by 120 (noted) | fine | - |
| `source_file` | file = recruiting arm | n/a | categorical, non-feature | fine | - |
| GJB2 pathogenic / hotspot: `c.235delC`, `c.299_300delAT`, `c.176del16bp`, `p.V37I`, nonsense/frameshift sites (`p.W3X`, `p.W77X`, `p.E47X`, `c.93delT`, `c.443delC`, `c.605ins46`, `c.35insG`, `c.35delG`, ...) and rare missense (36 columns incl. below) | allele count 0/1/2 at the site | yes (germline) | numeric dosage, right; `p.V37I` = mild/incomplete penetrance (paper) | fine | - |
| GJB2 benign polymorphisms `p.V27I`, `p.E114G`, `p.I203T` | allele count | yes | numeric | fine as features; carry the selection note already in the record | SEL (record marker) |
| GJB2 `p.T123N` (40 carriers) | allele count | yes | numeric | fine; **ClinVar Likely benign/Benign (VCV 44743), not in the record's benign set** (finding 3) | - |
| GJB2 `c.507insAACG` (17), `c.507_508insAACG` (3), `c.512insAACG` (2) | one allele, c.508_511dup (p.A171fs), under three legacy names | yes | **one variant split over 3 columns** (finding 1) | cleaning problem | CLEAN-12 / CLEAN-5 |
| MT-RNR1 block (files' `mtDNA`): `A1555G`, `C1494T`, `c.1452T>C`, `c.1598G>A`, `c.1519_1520insCA`, `c.1438G>A` | presence 0/1 (mito, homoplasmy not recorded) | yes | rename to MT-RNR1 correct: all 7 positions lie in MT-RNR1 (m.648-1601) and the paper names 7 MT-RNR1 variants; counts never 2. `c.` prefix should be `m.`; `c.1438G>A` is the haplogroup polymorphism m.1438A>G (benign), direction as the file writes it | fine (cosmetic names) | - |
| SLC26A4 `c.919_2A>G` (178 carriers, 39 hom.) | IVS7-2A>G = **c.919-2A>G**, the commonest Chinese SLC26A4 allele | yes | name is a typo (`_` for `-`) carried into the shipped name | cosmetic; rename | CLEAN-12 (Weigh) |
| SLC26A4 `c.915insG` (4), `c.915_916insG` (2) | both = c.916dupG (p.V306fs) | yes | **one allele over 2 columns** | cleaning problem | CLEAN-12 / CLEAN-5 |
| SLC26A4 `c.36insG` (5), `c.35_36insG` (1) | the same insertion written two ways (and both GJB2-style names; possibly GJB2 c.35dupG misfiled, unconfirmed) | yes | **alias pair; one carrier (disc. row 460, label carrier) has 1 in both** | cleaning problem + question | CLEAN-12 |
| SLC26A4 `c.1548insC` (4), `c.1546insC` (1, hom.) | probable aliases of c.1547dupC (insertion in a C run) | yes | probable alias pair | question | CLEAN-12 |
| SLC26A4 `g.-1064A6602del7666` (1), `c.-2071_307+3801del7666` (1) | probably the same 7,666-bp deletion | yes | probable alias pair | question | - |
| SLC26A4 `c.508insAACG` (2), `c.234_235delC` (1) | GJB2-style names inside the SLC26A4 block (GJB2 c.508_511dup, c.235delC); unconfirmed | yes | **disc. row 706 has GJB2 c.507_508insAACG + "SLC26A4" c.508insAACG + GJB2 c.235delC** = 3 GJB2 alleles if misfiled | question | - |
| SLC26A4 other sites (about 75 columns: `p.H723R`, `p.T410M`, rare missense/frameshift, `G1442A` with unknown nomenclature) | allele count | yes | numeric; most carried by 1-5 people, the block tail (sheet columns ~100-143) is discovery-only | fine | - |
| 16 dropped constant columns | sites no one carries | - | correctly dropped (verified 16) | fine | CLEAN-5 |
| dropped `GJB2_p.G160S`, `MT-RNR1_c.1541T>C` | exact copies of `p.N206S` (1 person) / `c.1519_1520insCA` (2 people) | - | asserted equal in code; dropping is right, copies are coincidental co-carriage, not meaning | fine | CLEAN-5 |
| blank cell `GJB2_c.235delC`, disc. row 497 (patient, only other allele SLC26A4 p.G222V het) | unknown | - | shipped missing; the only missing cell. Not inferable (every row has >=1 allele already) | fine | CLEAN-10 |

No column is post-outcome: all are germline genotypes. No leak found (LEAK checks n/a beyond the selection issue the record carries).

**Problems ranked**

1\. **Variant aliases split one allele over several columns (CLEAN-12, Should; mildest remedy: merge).** The headers mix legacy names: GJB2 c.507insAACG / c.507_508insAACG / c.512insAACG are one sequence change (inserting AACG next to the duplicated AACG at c.508-511 = c.508_511dup, p.A171fs; ClinVar lists 511-512insAACG as its alias, and a 2015 study notes several mis-names); SLC26A4 c.915insG / c.915_916insG (= c.916dupG); SLC26A4 c.36insG / c.35_36insG; probably c.1546insC / c.1548insC and the two del7666 names. ~40 people affected. The names also split by arm: `c.507_508insAACG` is discovery-only, `c.512insAACG` validation-only, `c.507insAACG` both; `c.915insG` discovery-only, `c.915_916insG` both. So a model sees one allele as unrelated sparse columns, partly by recruiting arm. Remedy: merge each certain alias set into one column named by HGVS (count = max over the aliases when the same person has two, see 2), note the probable ones. Low score impact (rare sites), but it is the expert state.
2\. **Two rows look double-entered (question for the curator).** Discovery sheet row 460 (carrier) has 1 in both `c.36insG` and `c.35_36insG`: merged as a sum it is a homozygote labelled carrier; as one entry it is a het. Row 706 (patient) has GJB2 c.507_508insAACG + "SLC26A4" c.508insAACG + GJB2 c.235delC. Options: take max on merge (assume double entry, recommended) or leave and note.
3\. **Benign set in the curation note omits p.T123N (note correction).** T123N is Likely benign/Benign in ClinVar (VCV000044743). Adding it to V27I/E114G/I203T moves the benign-only people from 558 to 581 (patient share 83.1% vs 72.8% for the rest), so the record's selection argument holds; only the stated numbers and the rule-baseline variant "without the three benign polymorphisms" would shift slightly. Remedy: mention T123N in the note (and optionally rerun the rule variant).
4\. **The 53-carrier block attribution contradicts the paper's Table 1 (claim fix).** The note says the block was "likely typed with a panel that does not report the three polymorphisms (the community NGS screening, unconfirmed)". Table 1 of Luo et al. puts the community NGS hotspot screening (2020.5-2020.8, 103 women aged 27 +/- 4) in the **external validation** set only; the internal (discovery) set is hospital records, Sanger only. The block also carries rare non-hotspot sites (GJB2 p.G4D, p.V63L, p.M195V; SLC26A4 p.S49R, p.D661E, p.R409H), so it is not obviously a hotspot panel. Remedy: drop the "community NGS" guess; say the cause is unknown (maybe the carriers selected or recorded without polymorphisms). Related: the summary's "carriers from a community's NGS hotspot screening ... to offset the patients" should say they went into the validation file. In the validation file the NGS arm cannot be told apart: 71 of 133 validation carriers lack all three polymorphisms (53% vs 39% of other discovery carriers). The two files share one 144-site header in the same order, so the panels differ only in which sites are carried: 73 discovery-only sites (mostly the SLC26A4 tail of rare Sanger finds) and 17 validation-only.
5\. **Cosmetic names (Weigh).** `SLC26A4_c.919_2A>G` -> `c.919-2A>G`; MT-RNR1 `c.` -> `m.`; `SLC26A4_G1442A` has no readable nomenclature. Rename only with the merge in 1.

Verified claims (exact): 16 constant + 2 copy drops -> 126 sites; 95 sites with <5 carriers; 17 validation-only, 73 discovery-only; 71 patient-only, 10 carrier-only; one blank cell at the stated place; 558 benign-only people, 83% vs 73% patients; MT-RNR1 values 0/1; rows carry 1-6 alleles.

Sources: https://ncbi.nlm.nih.gov/clinvar/variation/44732 (GJB2 c.508_511dup, alias 511-512insAACG), https://www.pubmed.gov/25891447/ (mis-names -> c.508_511dup), https://https.ncbi.nlm.nih.gov/clinvar/variation/44743/ (T123N), Europe PMC PMC8237285 (Table 1, Sample collection).

</details>

<details><summary>Split audit</summary>

**split-auditor: deafness_gene_carrier_hearing_loss**

**Verdict: right, with notes.** 10x3 stratified random CV over 1,778 people (L-PLACE.random, ForcedIIDFromGrouped) holds up. The hidden families are real and can partly be found from the raw row order, but the label does not travel with them. Grouping by them leaves the score unchanged.

**Tree walk (SPLIT-36)**
Clinical Study → [CLI.meets] yes: another site (the source validates on a second recruiting source) → no date per person (`Time: Lost`) → [PLACE.several] two sources, one per file: too few for the enough-groups check → [PLACE.units] one row per person; families have no id → **L-PLACE.random**. This is the leaf the definition names (`split_leaf`, splits_comment, group basis) and the split it ships. The leaf is forced, and the curator has already decided it (issue 2 A). Shipped kit checked: 30 folds with 592-593 test rows each, every row tested once per repeat. Row order is shuffled: neighbouring rows share a label at 0.620, against 0.637 by chance, and 0 neighbouring pairs share a rare variant.

**Findings (ranked)**

1\. **Hidden families exist and the raw order shows them. They are not material to the split (LEAK-42 verdict: natural or not material; LEAK-43 tests).**
   - Is the link real? Yes. 40% of the 28 pairs that share a variant carried by exactly 2 people sit within 3 rows of each other in their file, against 0.8% for random pairs. Within 10 rows it is 55% against 2.3%. 16 neighbouring pairs share a variant carried by ≤30 people, against 0.45 after shuffling.
   - Linking neighbours (window 3) that share a variant carried by ≤30 people gives 22 clusters with 49 rows (2.8%). A looser threshold (≤60) gives 30 clusters with 67 rows. Families that share only common variants (for example c.235delC) cannot be recovered.
   - Does the label travel with the link? No. Label agreement between people who share a rare variant is 0.62-0.64, the same as the 0.64 base rate. 12 of the 22 clusters hold both labels, in the classic trio pattern: a compound-heterozygous patient next to two parents, each a carrier of one allele (validation rows 1359-1361, 1240-1242). Siblings with the same biallelic genotype also occur (discovery rows 915-918).
   - Grouped CV on the family proxy against random CV, 10x3 on the same seeds: untuned HGB 0.752 vs 0.750 (paired difference -0.002), genotype lookup 0.779 vs 0.777, expert-like rule 0.677 vs 0.677.
   - Use-case note: cascade testing of a patient's relatives is a core job of genetic counselling, so relatives on both sides of a fold partly match the use case.
   - Remedy (mildest): none to the split. Optionally, one clause in the curation note on relatives: "about 20-30 small family clusters can be found from the raw order (rows sharing a rare variant side by side). Grouping by them leaves ROC AUC unchanged (0.750 vs 0.752)."

2\. **The splits_comment's transfer claim holds in one direction only.** "Trained on the discovery file and scored on the validation file … 0.750 against 0.750 … close to the random split" is correct. The reverse direction (train on validation, test on discovery) gives HGB 0.672, below the expert-like rule (0.695), and lookup 0.724. 77% of discovery test people have a genotype seen in training, against 88% the other way. Training size (569 people, against about 1,185 in a random 3-fold) explains at least part of the drop, so this is not clear evidence of a shift between sources. Remedy: qualify the sentence ("in the source's direction; the reverse, on a training side half as large, scores 0.672"), or leave it as is. This is a wording note, not a split change.

3\. **The genotype-grouped numbers come from a similarity key, not a group id (SPLIT-24).** In the builder's genotype-grouped CV, the lookup scores exactly what its logistic fallback scores (0.409 both), because no held-out genotype is ever seen. The scores below 0.5 (0.41-0.49) show that models learn how often a genotype occurs among patients, not the two-hit biology. The rule keeps 0.63-0.68. That supports the splits_comment's sentence, and issue 1 A settled it (that split is not the use case). Remedy: none. If the sentence stays, "held out by exact genotype" makes clear it is a similarity key.

**Not found**
- The time probe's order drift is the 53-carrier opening block and a run of patients in the validation file. Shipped rows are shuffled, so the order does not reach participants.
- No group column, date or family id exists in the release. The two-file source split is the only true group structure, and it is too small to hold out.

Scripts: (a script in the run folder), fam2.py, cv.py} (a cluster run); numbers in panel/split-auditor_cv.json.

</details>

<details><summary>Domain practitioner</summary>

**domain-practitioner: deafness_gene_carrier_hearing_loss**

I review this as a clinical geneticist / genetic counsellor reading a person's GJB2, SLC26A4 and MT-RNR1 variants.

**Fit: approximate, at the weak end (the definition's `approximate` holds, but its use case needs rewording).** The genotype and the phenotype are real. But the person a counsellor sees with this report already has a hearing test, and the test is the label. The decision where I hold the genotype but not the hearing outcome is a different one. It is the penetrance of a genotype: prenatal diagnosis in a family with a deaf child, a sibling, or a newborn who passed screening, asked about later-onset loss. This sample's case-control design distorts that penetrance (USE-1, USE-5, USE-8, USE-9). Selection alone does not make the fit None (USE-8), and I do not argue for None.

**Answers in the actor's voice**

1\. **Inputs.** I would have the variant counts at the moment of prediction. What I always have and the data lacks:
   - age, and age at onset (prelingual or postlingual);
   - aminoglycoside exposure for MT-RNR1 carriers. m.1555A>G and m.1494C>T are drug-susceptibility variants, and whether they cause hearing loss depends mainly on exposure;
   - which test was run: full GJB2 Sanger in the clinic or a hotspot panel in the community. This decides whether a "monoallelic" patient really has a single variant or has a second one the test did not look for;
   - whether the person is a proband or a relative (an obligate-carrier parent);
   - inner-ear CT for SLC26A4 (enlarged vestibular aqueduct).
2\. **Target.** "Failed the hearing screening" is not what I act on. I act on whether the genotype explains or predicts hearing loss (a genetic diagnosis, a recurrence risk, a penetrance estimate). For three groups, "passed the screening" does not mean "will not lose hearing":
   - p.V37I homozygotes: mild, late-onset loss with reduced penetrance;
   - SLC26A4 biallelic people: progressive, often postlingual loss;
   - MT-RNR1 carriers: loss only after drug exposure.

   For those groups the label is the hearing status at one moment, not the outcome. I would want a probability per genotype (penetrance), not a class.
3\. **Unit and test set.**
   - One row is one person. My decision is per genotype, made for a new family.
   - The test data are relatives and same-genotype people from the same two recruitment streams, so 85% of test people have an exact genotype twin in training. That mirrors "a common genotype I have seen before", which is fair for a lookup table but not for a new population.
   - The controls are largely obligate-carrier parents of deaf probands. In a family, the proband is biallelic and each parent is heterozygous by construction, so part of the rule's accuracy comes from the family structure.
4\. **Would I use the model? No, unless it beats the ACMG / textbook reading where it matters. It does not** (the definition's own numbers):

   | Rows | Textbook rule (benign polymorphisms not counted) | Untuned gradient boosting | Exact-genotype lookup |
   |---|---|---|---|
   | All 1,778 | 0.677 | 0.750 | 0.781 |
   | Without the 558 benign-only people | 0.782 | 0.774 | 0.808 (0.026 above the rule) |

   All values are ROC AUC on the 10x3 random splits. The model's whole gain over the rule comes from the 558 people with only p.V27I, p.E114G or p.I203T.

   My own tabulation of patient share by clinical category, on the shipped data:

   | Genotype class | People | Share with hearing loss |
   |---|---|---|
   | c.235delC homozygous | 182 | 1.00 |
   | GJB2 biallelic, no p.V37I | 347 | 0.99 |
   | SLC26A4 biallelic | 137 | 0.99 |
   | p.V37I homozygous | 52 | 0.87 |
   | p.V37I + one other GJB2 pathogenic allele | 40 | 0.68 |
   | Any MT-RNR1 variant (m.1555A>G: 99, 0.81) | 115 | 0.79 |
   | GJB2 single pathogenic allele, nothing else | 380 | 0.50 |
   | c.235delC heterozygous only | 118 | 0.34 |
   | SLC26A4 single allele only | 123 | 0.43 |
   | GJB2 single + SLC26A4 single (not causal) | 36 | 0.44 |
   | p.V37I heterozygous only | 166 | 0.58 |
   | Benign polymorphisms only | 558 | 0.83 |
   | Rule-positive with normal hearing | 48 | 0 (21 involve p.V37I, 24 MT-RNR1, 1 SLC26A4) |

   Where the reading is clinically confident, it is essentially perfect. The remaining uncertainty is in three places:
   - p.V37I: real, graded penetrance, and the only place a learned per-genotype rate adds anything clinical;
   - single-allele patients: most likely a missed second allele or a non-genetic cause, which the genotype columns cannot show;
   - MT-RNR1: depends on exposure, which the data lacks.

   I would trust a model only if it learned the p.V37I penetrance. I distrust any gain from the benign-only group.
5\. **What the benign polymorphisms mean.**
   - p.V27I and p.E114G are common in Chinese people: allele frequencies of about 23% / 15% in Zhejiang controls and 31% / 22% in the Taiwan Biobank, mostly as one V27I-E114G haplotype. They are read as benign.
   - p.I203T is rarer (about 6% in Taiwan, about 0% in Zhejiang controls) and contested: some sources call it pathogenic.
   - At those frequencies, about half of any normal-hearing Chinese community sample would carry one of them. Yet benign-only people here are 83% patients.
   - They enter the data because patients were Sanger-sequenced, which reports every GJB2 change, while carriers entered through a pathogenic hotspot variant. Wild-type people were excluded entirely.
   - So in this group the label records who was sequenced and with which test, not what the genotype does. This is the decisive evidence: it confirms the `Selection Bias` note with population frequencies, and it explains why the model "beats" the expert. I would never predict on the benign-only part of this sample.

**Gaps between the data and the real decision, ranked**

1\. **Ascertainment of the benign-only group** (558 people, 31% of rows). The label is set by sequencing method and recruitment, not biology, and it carries all of the model-over-rule gain.
2\. **Case-control design with family structure** (patients against largely obligate-carrier parents, no family id). The patient share of 76% and the genotype mix are nothing like newborn or prenatal screening, where hearing loss affects about 1-3 per 1,000.
3\. **Label timing.** "Passed screening" is not "will not lose hearing" for p.V37I, SLC26A4 and MT-RNR1 carriers. No age and no exposure history.
4\. **Single-allele patients.** A missed second allele is likely, and there is no record of which test was used.
5\. **Mixed panels.** Hotspot panel against full Sanger. The 53-row block of the discovery file was likely typed with a panel that does not report the polymorphisms; this is already noted.

**What an expert would change**

These are options for the curator, not prescriptions:

- **A.** Keep the dataset as is, and reword `use_case` from "judges whether a person's variants explain hearing loss" to "estimates the penetrance of a genotype for a relative or newborn whose hearing cannot yet be tested". Name the benign-only ascertainment in `fit_reason`.
- **B.** As A, and drop the 558 benign-only people as rows whose label reflects who was sequenced, not the genotype (a case-mix change, so its own PR per house rules). The rule then matches gradient boosting (0.782 against 0.774), so the task becomes close to trivial against the rule. That is `Trivial`-like evidence the curator should weigh.
- **C.** Keep all rows, and report the rule baseline on the non-benign-only people next to the all-rows score, so the gain is visibly an ascertainment gain.

My recommendation is C at minimum. A clinician would read the current benchmark as rewarding a model for learning recruitment.

Minor points:
- MT-RNR1 c.1438G>A (2 people, written in the files' notation; in mitochondrial notation it is m.1438A>G) is a near-fixed haplogroup polymorphism, not a susceptibility variant. m.1452T>C and m.1598G>A are of uncertain significance. This affects only 4 people, but "any MT-RNR1 variant" in the rule baseline is clinically too broad.
- The `known` field says "at the sites seen in the data". Clinically, the panel used is the missing context.

**Metric: partly**

- ROC AUC is the right family for a case-control sample. A proper scoring rule (log loss, Brier) would score calibration to a 76% base rate that no real population has (MET-8, MET-9).
- My decision is a per-genotype penetrance estimate. On all rows, AUC is driven by the benign-only ascertainment group, so it ranks models by how well they learn recruitment (MET-1).
- I would keep `roc_auc` and add the rule-baseline comparison on the non-benign-only rows (option C), rather than switch metrics.
- There is no threshold or cost I would act on, so no threshold metric fits (MET-6, MET-7).

**Sources**

- Luo et al. 2021, EBioMedicine 69:103322 (Methods and Discussion as quoted in the record and definition)
- The definition's experiments (`experiments.json` in the run folder)
- My tabulation: `panel/domain-practitioner_scratch/domain-practitioner_inspect.py`, run on the shipped data, light pandas only
- [PMC4456361, Zhejiang GJB2 variant frequencies](https://pmc.ncbi.nlm.nih.gov/articles/PMC4456361)
- [PMC4529078](https://pmc.ncbi.nlm.nih.gov/articles/PMC4529078)
- [PMC12428318, Taiwan Biobank](https://pmc.ncbi.nlm.nih.gov/articles/PMC12428318)
- [J Transl Med 7:79](https://translational-medicine.biomedcentral.com/articles/10.1186/1479-5876-7-79/tables/1)
- Clinical knowledge: p.V37I reduced penetrance; MT-RNR1 m.1555A>G aminoglycoside susceptibility; SLC26A4 progressive loss with enlarged vestibular aqueduct; m.1438A>G haplogroup polymorphism.

</details>

<details><summary>Blind review</summary>

I verified the prepared table against the public source, which I downloaded into an isolated scratch directory. I opened nothing outside the clean room except those downloads and public web pages.

---

**Verdict**

**Include with changes** — this is a real, correctly-copied clinical genotype table with genuine, non-linear (recessive/zygosity) signal, but it must be documented and scored as what it actually is: a ~341-distinct-genotype lookup problem with 76% prevalence, pooled across two cohorts whose original train/test separation has been discarded, and with a label that in most of the cohort was known *before* the features were measured.

---

**What the task is**

Each row is one individual sequenced on a three-gene hereditary-hearing-loss panel (GJB2, SLC26A4, MT-RNR1); each feature is one variant site coded 0 = not found, 1 = heterozygous, 2 = homozygous; the target is whether that person failed bilateral hearing screening. The Mendeley page states it exactly: *"No mutations found were indicated by 0, heterozygous mutations by 1, and homozygous mutations by 2"*, and that *"the Discovery Set was from the medical records and the Validation Set was from the Disabled Persons' Federation."*

The decision behind it is real and reasonably common: a lab or clinical geneticist has a panel result in front of them and must decide whether this genotype explains/predicts hearing loss — variant interpretation and triage of screen-positive individuals. The paper frames it as *"a … tool for HHL prediction when high throughput sequencing data are available"* and identifying the *"HHL high-risk population … in the screening process."*

**Provenance check passed.** Source files `Discovery Set.xlsx` (1209 data rows) + `Validation Set.xlsx` (569) = 1778 rows, exactly the prepared size. Label counts match exactly: 918+436 = 1354 positives, 291+133 = 424 negatives. Comparing the two tables as multisets of (features, label): **identical, zero rows differing in either direction**. The preparer renamed the `mtDNA_*` block to `MT-RNR1_*` (correct — those sites are in MT-RNR1), prefixed each variant with its gene from the merged header row, dropped 22 all-zero columns, and mapped 1→Yes / 0→No correctly. The row order was shuffled. That is a careful, faithful preparation.

---

**Concerns, most to least serious**

**1. The label was known before the features in most of the cohort — the "prediction" is retrospective ascertainment, not a forward decision**

Subjects entered via hospital electronic medical records of patients *with hearing loss* (2009–2017) and via the Disabled Persons' Federation, i.e. a disability registry. For those people, deafness is why they were sequenced at all. Only the small community-screening subset (NGS hotspot, 2020, ~100 people by the paper's Table 1) has the genotype genuinely preceding the audiometry. Prevalence in the prepared file is **76.2% Yes** (1354/1778), against a population prevalence of congenital hearing loss of roughly 0.1–0.3%.

No individual column leaks — germline genotype is fixed at conception and is available whenever you'd run this — so this is not column leakage. But it is severe selection on the outcome, which means (a) predicted probabilities carry no transportable meaning, and (b) a model is partly learning "who gets sent for a deafness panel," not penetrance.

**Change:** state in the task card that this is a case/carrier-contrast cohort at 76% prevalence, score it with AUC/AP only, and do not present accuracy as the headline (see #3).

**2. The original external-validation split was discarded in favour of pooled random CV**

`task.md` says "Regime: IID (random rows)", pooling the two source files. The source cohorts differ in era, recruitment, age and **assay** — hospital/DPF samples were Sanger-sequenced, the community samples used *"NGS hotspot screening"* with only *"an overlap ratio of 96% between the NGS hotspots and Sanger sequencing sites."* So a `0` means "tested, nothing found" for some rows and "site not on the assay" for others, and which one it means is correlated with cohort.

I measured how much this actually costs, and the honest answer is: not much.

| | AUC |
|---|---|
| LightGBM, pooled 10×3 random CV (the proposed regime) | 0.746 ± 0.017 |
| LightGBM, train = Discovery → test = Validation (paper's design) | 0.752 |
| LightGBM, train = Validation → test = Discovery | 0.685 |
| Genotypes → predict which cohort a row came from | 0.578 |
| Positive rate, Discovery vs Validation | 0.759 vs 0.766 |

Variant frequencies do shift (SLC26A4 c.919-2A>G: 12.3% of Discovery vs 5.1% of Validation; MT-RNR1 A1555G: 7.1% vs 2.3%), but the random split is not materially optimistic here.

**Change:** keep IID if you want, but say in the card that the pool merges two cohorts with different assays and that a `0` is "no mutation found or site not covered." I would not add a cohort indicator column — it is not available at prediction time.

**3. 85% of test rows are exact copies of a training row, and the ceiling is a lookup table**

With 126 sparse 0/1/2 columns there are only **341 distinct feature vectors among 1778 rows** (388 distinct feature+label combinations). Under the proposed 10×3 split:

- **84.6%** of test rows have their exact feature vector present in train;
- **82.7%** are exact duplicates of a train row *including the label*;
- only ~91 of ~593 test rows per fold present a genotype never seen in training.

A pure pattern-frequency lookup table beats every model I tried (AUC **0.777**, accuracy 0.796). LightGBM scores 0.767 on previously-seen patterns but only **0.631** on novel ones. Majority-class accuracy is 0.7615; LightGBM's accuracy is 0.7695 — a 0.8-point gain.

This is *not* a curation error — it is intrinsic to a discrete genotype space, and the duplicates are genuinely different people. But it means the benchmark is measuring frequency estimation over ~341 cells with heteroscedastic cell counts, not generalisation to new genotypes, and that accuracy is near-degenerate as a metric.

**Change:** document the 341-cell effective support and the lookup-table baseline (AUC 0.777) as the reference to beat; score with AUC/log-loss, not accuracy; and prefer 5- or 10-fold over 3-fold, since the informative quantity is the number of distinct patterns, not rows.

**4. Unverifiable family structure — the one thing that could still be inflating the random split**

The paper recruited *"patients and their immediate family members."* Relatives share genotypes, and genotype is the entire feature set, so a parent and child land in different folds as literally identical rows. There are no subject or family IDs in either the prepared file or the public spreadsheets, so **I could not check this, and no grouped split can be constructed from what is shipped.** Given #3 it is also indistinguishable from ordinary genotype recurrence. Flag it in the card as a known, unfixable limitation.

**5. 115 of 126 columns are noise, and several are the same variant written twice**

Nonzero counts: **56 columns have exactly one carrier, 84 have ≤2, 99 have ≤5.** Eleven variants (≥40 carriers) carry essentially all the signal — LightGBM on those 11 alone scores **AUC 0.743** vs 0.746 on all 126.

Worse, the long tail is visibly free-text data-entry residue: `GJB2_c.507_508insAACG` / `GJB2_c.507insAACG` / `GJB2_c.512insAACG` / `SLC26A4_c.508insAACG` are the same GJB2 insertion under four spellings, one of them filed under the wrong gene; likewise `SLC26A4_c.35_36insG` / `c.36insG` (a GJB2 variant), `SLC26A4_c.234_235delC` (GJB2 c.235delC), `SLC26A4_c.1546insC` / `c.1548insC`, and `SLC26A4_c.-2071_307+3801del7666` / `SLC26A4_g.-1064A6602del7666` (the same 7666-bp deletion twice). None of these pairs ever co-occur in a row, consistent with alternative spellings of one event across records.

They are singletons and change nothing numerically, but they inflate "126 features" into something the dataset doesn't have. **Change:** either keep them and say in the card that ~100 columns are near-constant nomenclature variants (a legitimate robustness test), or merge the obvious synonym groups. Do not silently present this as a 126-feature problem.

**6. Minor preparation issues**

- One cell is NaN (`GJB2_c.235delC`, a single row), which makes that one column `float64` while the other 125 are `int64`. Harmless, but inconsistent; set it to 0 or to a shared nullable integer dtype.
- Two non-constant source columns were dropped along with the 22 all-zero ones: `mtDNA_c.1541T>C` (2 carriers, one Yes one No) and `GJB2_p.G160S` (1 carrier). No impact, but the drop rule in the card should say so.
- `task.md` names **no training-weight column**, and none is needed — there is nothing to criticise here.

---

**What is good, and why I would still include it**

**The data is real and biologically coherent.** The zygosity structure is exactly what inheritance predicts, which is strong evidence against fabrication or label scrambling:

| variant | het (1) | hom (2) |
|---|---|---|
| GJB2 c.235delC | 66.3% HL (n=297) | **100% HL (n=182)** |
| SLC26A4 c.919-2A>G | 68.3% (n=139) | **100% (n=39)** |
| GJB2 p.V37I (hypomorphic) | 62.9% (n=248) | 86.5% (n=52) |
| GJB2 p.V27I (benign polymorphism) | 77.2% | 79.8% ≈ base rate 76% |

c.235delC and c.919-2A>G are the most common pathogenic GJB2/SLC26A4 alleles in Chinese populations, V37I is the known incompletely-penetrant one, V27I/E114G are benign — the table reproduces all of that correctly, with benign sites sitting flat at the base rate.

**It discriminates methods, and for the right reason.** Pooled 10×3 CV, AUC:

| method | AUC |
|---|---|
| pattern lookup table | 0.777 ± 0.019 |
| RandomForest (500) | 0.772 ± 0.015 |
| HistGB | 0.748 ± 0.015 |
| LightGBM | 0.746 ± 0.017 |
| kNN (k=25) | 0.724 ± 0.022 |
| LogReg, one-hot | 0.656 ± 0.021 |
| LogReg, 0/1/2 scale | 0.576 ± 0.016 |
| BernoulliNB | 0.530 ± 0.021 |

The 0.20 AUC gap between linear-on-ordinal-genotype and tree models is real dominance/interaction structure (heterozygote below base rate, homozygote at 100%), not noise — a genuinely useful thing for a tabular benchmark to test. Fold-to-fold SD is ~0.015–0.02, so differences above ~0.03 are resolvable. It is neither trivial (nothing reaches 0.8) nor signal-free, and 1778 rows is small but scoreable.

---

**What I could not check**

- **Family relatedness / repeat subjects across the two files.** No IDs exist anywhere in the public release; with 85% pattern duplication, overlap would be undetectable even in principle.
- **How "hearing loss" was thresholded.** The paper only says subjects were split *"according to whether they passed the hearing screening test or not"*; the dB threshold, test type and age at test are not stated per subject, and none of it is in the data.
- **A row-count discrepancy with the paper.** The public Discovery file has 1209 rows (918 patients / 291 carriers) but the paper's internal-CV set is n=1329 (918 / **411** carriers) — the same patients, 120 fewer carriers. The paper's total is 1898; the public release supports 1778. So the shipped data is not exactly the data the published models were fit on, and the release gives no explanation.
- **Whether `0` ever means "not assayed" for a specific row.** Only the aggregate 96%-overlap statement is available.
- **Full text of the two citing papers** (Nat Commun 2024;15:1603 and BMC Med Inform Decis Mak 2026;26:364 — both real, both cite Luo et al. as a reference). Both are behind login walls, so I could not confirm whether either benchmarked this exact table or how they split it.

</details>

<details><summary>Task gamer</summary>

**Audit — `deafness_gene_carrier_hearing_loss` (HearingLoss, roc_auc, 10×3 IID folds)**

**Verdict: this task is not gameable — I found no exploit that beats the honest baseline by more than noise; every bit of signal in the table is genotype, which is exactly what the prediction point ("once GJB2, SLC26A4 and MT-RNR1 have been sequenced") hands a deployed model.**

Honest baseline (untuned `LGBMClassifier(n_estimators=200)` on `features()`, 30 shipped splits): **0.74663** (sd across splits 0.01841, range 0.7107–0.7865; identical for model seeds 0–4). Noise reference: adding one `N(0,1)` column moves it to **0.655–0.673** (5 draws), i.e. −0.074 to −0.091 — the untuned baseline is very sensitive to any continuous column, so a feature-engineering comparison carries a ±0.09 reference spread; like-for-like comparisons below are paired per split instead.

Better honest model (step 3 reference for the exploits): **exact-genotype lookup** — target-encode the full 126-column genotype vector on the training rows, smoothed (`(sum + ȳ)/(n + 1)`), fall back to the training rate for unseen vectors: **0.77850** (sd 0.01627), **+0.0319 on all 30/30 splits** (per-split +0.009 to +0.073). A rank blend of 0.7·lookup + 0.3·LGBM gives 0.78066. This is not an exploit: it is the same genotype the counsellor has, just fitted better than the baseline fits it.

**Exploits, ranked by gain**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Transductive pseudo-labelling of the test rows (fit, pseudo-label confident test rows, refit) | `work/final_exp.py` | 0.74663 | 0.74818 | **+0.0016** mean | n/a — gain is inside noise | none needed |
| 2 | Genotype-group size counted over train **+ test** rows | `work/transductive.py` | 0.78315 (train-only counts) | 0.78074 (all-row counts) | **−0.0024** | — | none needed |
| 3 | Allele frequency + rank/quantile transform computed over all rows | `work/af_honest.py` | 0.77837 (train-only) | 0.77767 (all rows) | **−0.0007** (−0.015 … +0.014) | — | none needed |
| 4 | Missing-value sentinel (the one `NaN` in `GJB2_c.235delC`) as a feature | `work/transductive.py` | 0.74663 | 0.74663 | **0.0000** | — | none needed |
| 5 | Row position / next-row label agreement | inline | 0.74663 | AUC(position)=0.5078; P(yᵢ=yᵢ₊₁)=0.620 vs 0.637 chance | **0** | — | none needed |
| 6 | Train-vs-test covariate classifier (test composition) | `work/transductive.py` | — | AUC 0.4918 | **0** | — | none needed |
| 7 | Restoring the 2 non-constant source columns the kit dropped | `work/final_exp.py` | 0.74663 | 0.74663 | **0.0000** | yes (they are sequenced variants) | none needed |

No ranked exploit clears the noise floor. **Flaws that hurt an honest model: none found** — restoring everything the preparation removed changes the score in the fifth decimal (below), and the split regime is not pessimistic either.

Not ranked, per the brief: the rows are in the published Mendeley file **with their labels**. Matching each kit row to `Discovery Set.xlsx`/`Validation Set.xlsx` by genotype vector and predicting that vector's full-data label rate scores **0.89281** (that is the ceiling of this route — rows sharing a genotype are not individually identifiable). Every public dataset allows this; it is not a flaw of the task. Separately, `data.parquet` ships `HearingLoss` for the test rows too, so a pipeline that scores a submitted prediction file rather than refitting per split would be trivially gameable; `score.py`'s docstring makes clear the intended protocol is fit-on-train, and I treated it that way.

**Mechanisms**

**Why there is nothing to steal.** The kit is exactly the published source: I downloaded both Mendeley files, merged them (1209 + 569 = 1778 rows) and confirmed the multiset of genotype vectors is **identical** to `data.parquet`, and that the per-vector label tables (`sum`, `count`) match exactly. The preparation did two things: it dropped 18 of the 144 variant columns (16 are all-zero across all 1778 rows; `GJB2_p.G160S` has 1 non-zero cell and `MT-RNR1_c.1541T>C` has 2), and it shuffled the rows. Restoring the two non-constant columns from the source leaves the baseline at 0.74663 — bit-identical. The shuffle is independent of source order (Spearman 0.027 between kit position and source position over the 239 rows whose genotype vector is unique). Every feature is a 0/1/2 genotype dose at the prediction point; there is no id, no time, no weight, no post-outcome column.

**The whole score is genotype memorisation, and that is legitimate.** 1778 rows collapse to **341 distinct genotype vectors** (1539 rows sit in a repeated vector). The exact-genotype lookup at 0.77850 is essentially the ceiling: a leave-one-out oracle group mean over all rows scores 0.77496, so there is almost no headroom left above the lookup without using test labels. The predictive content is ordinary biology — `GJB2 c.235delC` homozygous is 182/182 deaf, `SLC26A4 c.919-2A>G` homozygous is 39/39 deaf, `GJB2 p.V37I` is the one protective column (AUC 0.460) because it is hypomorphic. The duplicate vectors are not duplicated *records*: with 126 mostly-rare variants, most people carry one or two, so 341 patterns is what the biology produces. Fix: none.

**Format attacks find a single artefact with no consequence.** All feature values are `0`, `1` or `2`; there are no decimals, sentinels or precision differences to read. `GJB2_c.235delC` is `float64` only because one cell was a literal space `' '` in `Discovery Set.xlsx` (row 494, a patient whose only other variant is `SLC26A4 p.G222V`); the kit carries it as `NaN`. One row cannot move AUC, and an is-missing indicator leaves the baseline unchanged. `MT-RNR1` columns only ever take 0/1 (correct for a mitochondrial locus), so the classes were not coded with different zygosity conventions. Mildest fix: impute that one cell as 0 and make the column `int64`, so the only format asymmetry in the table disappears.

**The IID regime is not optimistic here, which I checked rather than assumed.** The kit pools two differently recruited cohorts (hospital electronic medical records 2009–2017; Disabled Persons' Federation plus a 2020 community screen) that the source paper used as train and external-validation sets. I recovered a cohort label for each kit row consistent with the per-(vector, label) counts. Genotype distinguishes the cohorts only weakly (D-vs-V classifier AUC 0.578) and their positive rates are nearly equal (918/1209 = 0.759 vs 436/569 = 0.766). Training on Discovery and testing on Validation gives LGBM 0.7563 / lookup 0.7743 against a size-matched random split's 0.7433 / 0.7813 — the cross-cohort direction is not worse, so merging the cohorts and splitting randomly buys no inflation. No fix needed.

**One structural caveat I can flag but not measure.** The source paper states both cohorts contain "patients and their immediate family members", and `task.json` declares no `group_columns`. A deaf proband and their carrier parent can therefore fall on opposite sides of a random fold. They are not duplicate rows (the proband is homozygous where the parent is heterozygous, so the vectors differ), and the cross-cohort test above shows no detectable optimism, but the kit carries no family id, so I cannot bound the effect. The fact that would decide it is a family/pedigree identifier in the original records; if one exists, the honest fix is a grouped split on family.

**Attacks that found nothing**

1 Row position vs target (AUC 0.508), next-row label agreement (0.620 vs 0.637 chance), label-run structure — the shuffle is clean. 2 Any id, key or hash — there is none. 3 Exact and near copies across the split — present in abundance but they are genuine shared genotypes, and the lookup that uses them is the honest model. 4 Cross-file duplicate individuals: of the 299 genotype vectors with ≤4 rows, 20 appear in both source files, all with 1–4 common variants (shared haplotypes, not re-enrolled people). 5 Training-row attacks (rows dated after the prediction point, label-dependent inclusion, time relative to the split date) — not applicable, no time column and no temporal regime. 6 Test-set composition: train-vs-test classifier AUC 0.4918; folds are stratified so the test positive rate is fixed at 0.7615, which AUC ignores. 7 Columns from after the prediction point — every column is a sequenced variant. 8 The weight — `sample_weight` is null. 9 Transforms over all rows (all-row allele frequencies, percentile ranks, all-row group counts) — all within ±0.0024 of their train-only counterparts. 10 Transductive pseudo-labelling — +0.0016. 11 Format-only features (missingness, dtype, value ranges) — a single `NaN` cell, zero gain. 12 Metric manipulation: `metrics.py` calls `sklearn.metrics.roc_auc_score` on the positive-class column with no weights and no inputs, and `_check_true_values` verifies the supplied `y_true` against the dataset at `test_idx`, so the metric itself offers no handle. 13 Lookup/shallow-rule recovery of the target — the best such rule is the genotype lookup at 0.7785, well short of deterministic.

**What I could not check**

Whether relatives (or the same individual) appear on both sides of a fold — the kit has no person or family id, and genotype alone cannot distinguish a parent from an unrelated carrier with the same variant. Whether the 120 carriers that the paper counts (544) but the public files omit (424) were dropped in a way that depends on their genotype; the paper gives no explanation, and only the authors' full records would settle it. The paper's per-model AUC figures live in a figure image I could not read, so I compared only against its reported SVM numbers (0.803 internal CV, 0.751 external) — my honest lookup at 0.7785 on this merged table sits between them, which is consistent with no hidden shortcut being available.

Sources: [Mendeley 10.17632/6mh8mpnbgv.1](https://data.mendeley.com/datasets/6mh8mpnbgv/1), [Luo et al., EBioMedicine 2021 (PMC8237285)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8237285), [DOAJ record](https://doaj.org/article/a213c8a31c424250aa476a05e974fde7).

</details>

<details><summary>Precedent check</summary>

**precedent-checker: deafness_gene_carrier_hearing_loss (2026-11-25)**

Register: 7,375 decisions, 46 flags. Relevant flags: TP-4 drift and opposite outcomes (thyroid_discordant keep before the 2026-11-12 amendment, exclusions after it); `mechanism: trivial` (6 keep / 8 exclude). None of the flags is about this dataset; I read the cases behind them.

| # | Decision (as implemented) | Verdict | Closest precedents |
|---|---|---|---|
| 1 | TP-4: keep; the textbook rule loses (0.652 / expert-like 0.677 against GBM 0.750, lookup 0.781; models ahead on 30 of 30) | consistent | differentiated_thyroid_cancer_recurrence (2026-10-26, Lennart: methods +0.032 on 59 of 60, kept); thyroid_discordant (2026-11-12, Andrej, kept); against: audiology_diagnosis (rule beats, retired 11-10/11-11), ljubljana_breast_cancer (match, retired 11-12), sepsis_survival (+0.001 on every fold, retired at step 2, 11-10/11-12) |
| 2 | Selection Bias marker for the patients and carriers recruited separately; kept | consistent, with a stated reason | wild_type_attr_cardiac_amyloidosis (same day, 1:1 case-control, Selection Bias, kept); gallstone_disease, pancreatic_cancer_mouse_detection (kept with the marker). The datasets retired for how their classes were collected (naticusdroid 11-13, biogeographical_ancestry, early_stage_diabetes 11-10/11, south_africa_coronary 11-10) had their classes collected entirely apart or a label that is the selection. Here the definition shows otherwise: sites seen in one class only are at chance (71 against 65.6 expected, 10 against 15.0), and carriers include relatives from the same clinic |
| 3 | The 53-carrier block typed without the three polymorphisms: kept with a note, **no `Class-dependent Recording` marker** | **departs without a stated reason** | pheochromocytoma_paraganglioma_metastasis (same day, Andrej: marker set for a format artefact that scored ROC AUC 0.531, fixed by rounding); gallstone_disease (marker set, second route dropped, LEAK-39); pancreatic_cancer_mouse_detection (2026-11-12, Andrej: Selection Bias *only* because "both classes went through the same instrument, m/z grid, chips and number format") |
| 4 | LEAK-18/19/20: every person stays a row (1,390 repeats; 47 genotypes with both labels) | consistent (curator settled 1 A; reopened as asked) | sepsis_survival (110,204 rows over 975 profiles, kept under LEAK-18; its later retirement was TP-4 step 2, not the repeats); ai4d_lab_tanzania_tourism (2026-11-05, Lennart: 965 copies kept, 410 profiles with several labels); hiva_agnostic and qsar_tid_11 (distinct entities with the same vector stay). Copies of one record were dropped (splice 11-12, jm1, qsar_oral_toxicity, gallstone) and are not this case |
| 5 | L-PLACE.random, `ForcedIIDFromGrouped`, 10x3 CV, the source's split not shipped | consistent | pheochromocytoma_paraganglioma_metastasis and wild_type_attr_cardiac_amyloidosis, both resolved A on 2026-11-25 by Andrej with the same reasoning (two cohorts too few, one training side) |
| 6 | Genotype-grouped folds bring models to 0.41-0.49 (below the rule, 0.63-0.68); the random split stays | consistent | SPLIT-28 keeps known groups when the use case allows them (santander_customer_satisfaction var38, ashrae building_id); here the curator settled that common genotypes are the use case (issue 1 A); LEAK-43 / SPLIT-30: the size of the gap does not decide |
| 7 | `source_file` shipped as a `NonFeature("provenance")` | minor inconsistency in implementation, not in decision | pheochromocytoma (same day, same decision "the cohort is no feature") *drops* the cohort flag; this is the only definition in the working copy that declares a `non_features` column |

**Notes on the consistent decisions**

**1 (TP-4).** Step 1 on the shipped splits: the methods beat the rule on every split, so step 2 applies and the AI does not retire on it. The gain is +0.098 AUC (sd 0.023) over the textbook rule and +0.073 (sd 0.019) over the expert-like reading, far above sepsis's 0.001 and above differentiated_thyroid's kept 0.032. A fact for the curator's step 2, already in the definition: on the 1,220 people with a non-benign variant, GBM *matches* the expert-like rule (-0.008, sd 0.019, ahead on 10 of 30, which reads as ljubljana's pattern), while the genotype lookup still beats it (+0.026, sd 0.014, ahead on 29 of 30). So most of the gain on all rows comes from the 558 people who carry only benign polymorphisms. The definition says their label "says who was sequenced". No precedent covers a gain over a rule that lies in rows whose labels come from the selection. The closest is early_stage_diabetes (retired 2026-11-10/11 for selection together with other reasons). This is not a departure. It belongs to the mediator/critic as a step-2 question and is only noted here.

**4 (LEAK-18).** The 126 sites act as a few coarse features (1 to 6 alleles a person), which is the case LEAK-18 calls "natural, keep and say so". LEAK-20 lets a vector with both labels stay when the ambiguity is the task's own. Here that ambiguity is incomplete penetrance, stated in the definition, which follows tanzania.

**Reflection item (decision 3)**

**Mark the dataset `Class-dependent Recording` for the 53-carrier block?**

* **Problem:**
  - The definition writes the block up as "Anomaly (recording by class, kept)". It holds 53 carriers, all of one class, likely typed on a panel that does not report p.V27I, p.E114G and p.I203T (the community NGS screening, against Sanger in the clinic). That is a separate recording route, not a sampling difference[^leak39].
  - The marker rule asks for `Class-dependent Recording` "whether the artefact was fixed, is kept with a note or is still open", with one note in the definition. It separates this from `Selection Bias`, which covers which rows were sampled "with the measurements alike"[^marker].
  - Same-day precedent: pheochromocytoma_paraganglioma_metastasis got the marker for 14 metastatic patients with converted plasma values, an artefact that scored 0.531 on its own and was fixed by rounding. pancreatic_cancer_mouse_detection (2026-11-12, Andrej) was kept at `Selection Bias` *only* because both classes went through the same instrument and format. Here they did not.
  - The effect is small (other test people 0.733 trained with the block against 0.739 without it, paired -0.0065, sd 0.0094), but the block's people get a patient probability of 0.55 against a base rate of 0.76. The LEAK-39 check on the other class's rows of the same route cannot be run, because no patient is in the block.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Add the marker, keep the block with its note (AI's best guess at the reading) | `Class-dependent Recording` next to `Selection Bias`; the definition's note becomes the marker's one note | follows pheochromocytoma, gallstone and the marker rule; no change to the data | the route is inferred (unconfirmed by the source) |
  | b | Add the marker and drop the 53 rows (as gallstone did) | 1,725 people; marker with "dropped" | removes the route entirely | gallstone's route was recognised at 0.993; here the block's carriers lacking the polymorphisms are also what the target predicts, so the drop removes real carriers; costs 3% of carriers |
  | c | No marker: the distinguishing fact is that the route is unconfirmed and costs nothing | as implemented | no change | departs from the marker rule's "also when kept or still open" and from the same-day sibling; nothing in the record states this reason yet |

* **Recommendation:** a.

[^leak39]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned.
[^marker]: Marker `Class-dependent Recording` (leak_checks.md, after LEAK-40; verification.md P4): set where LEAK-13 to LEAK-15, LEAK-39 or LEAK-40 applies, also when the artefact is kept or still open.

**Minor (decision 7), with options**

The same decision ("the cohort/file is no feature") was made for two datasets today and implemented two ways: pheochromocytoma drops the column, and this dataset keeps `source_file` as a provenance `NonFeature` and also lists it under `_feature_types(categorical=...)`. Options:
(a) keep it as it is, since the API supports provenance non-features and the column lets someone rerun the source's split;
(b) drop it as pheochromocytoma does.
Recommendation (a). If the curator wants the two datasets alike, the pheochromocytoma cohort flag could become a provenance `NonFeature` too. No reflection prompt is needed, because this is an implementation choice and not a curator departure.

**Drift and amendments**

- No drift by Andrej on TP-4, Selection Bias or LEAK-18/19 in the cases read. The register's TP-4 drift flag (Lennart: keep through 2026-10-21, exclude from 2026-11-11) comes from the 2026-11-12 amendment and does not bear on this keep.
- No third exception of the same kind is pending from this dataset.

</details>

<details><summary>Advocate (brief and rebuttal)</summary>

**advocate: deafness_gene_carrier_hearing_loss (opening brief, 2026-11-25)**

**Position: ship as defined, after the definition fixes below.** Those fixes are wording, one column merge and one marker. None of them changes the task, the split or the metric. Every validity rule (P1-P5) holds. The value question (TP-4 step 2) is a real gain, and step 2 belongs to the curator. The problems the panel found are quality problems (P7) or wording, and each has a mild remedy.

**1. The data is real, faithful and licensed (P5, P2; PROV, SEL-2)**

- The blind reviewer rebuilt the table from Mendeley with no access to our notes. The multiset of (genotype, label) rows is **identical** to ours, with zero rows differing either way. The task gamer confirmed this independently.
- The claim auditor tested 34 claims. 28 hold, and none of the 4 refuted or overstated ones changes the task, the split or the metric.
- The licence is confirmed from the Mendeley API: CC BY 4.0, published 2021-03-16.
- The biology checks out (blind reviewer):

  | Variant | Heterozygous: share with hearing loss | Homozygous: share with hearing loss |
  |---|---|---|
  | c.235delC | 66% | 182/182 |
  | c.919-2A>G | 68% | 39/39 |
  | p.V37I (reduced penetrance) | 63% | 87% |
  | p.V27I (benign) | flat at the 76% base rate | flat at the 76% base rate |

  This is the pattern inheritance predicts, and it is strong evidence against fabricated or scrambled labels.
- Why it outranks the doubts: P5 is the faithfulness test, and a measurement on the data beats inference (EV-2). The 120 carriers missing from the release (1,778 people against the paper's 1,898) are an untested gap of the source. They are already noted, and nothing in the data suggests they were dropped by genotype.

**2. Not trivial: the methods beat the textbook rule on every split (TP-4, Must; step 1 passes)**

- The rule is not fitted on these data. It is the paper's expert reading: biallelic GJB2 or SLC26A4, or any MT-RNR1 variant, means hearing loss.
- Scored on the shipped splits:

  | Model | ROC AUC | Against the rule |
  |---|---|---|
  | Textbook rule | 0.652 | |
  | Rule without the three benign polymorphisms | 0.677 | |
  | Untuned gradient boosting | 0.750 | ahead on 30/30 splits |
  | Exact-genotype lookup | 0.781 | ahead on 30/30 splits |

- The gain is +0.098 AUC over the rule (sd 0.023) and +0.073 over the reading without the polymorphisms (claim auditor, precedent checker). That is far above sepsis_survival's 0.001 (retired) and differentiated_thyroid's 0.032 (kept).
- Under TP-4 a gain on most splits goes to step 2. The AI does not retire on step 2.
- I concede the domain practitioner's fact. On the 1,220 people with a non-benign variant, gradient boosting only matches the rule (0.774 against 0.782, ahead on 10/30 splits). Most of the gain on all rows comes from the 558 people who carry only the benign polymorphisms.
- Two things still keep the gain real:
  - On those 1,220 people the lookup still beats the rule by +0.026 (sd 0.014, ahead on 29/30 splits). That gain sits where the practitioner says the clinical uncertainty is: the graded penetrance of p.V37I (87% homozygous, 68% with one other allele) and the MT-RNR1 carriers.
  - "The label of the 558 says who was sequenced" is overstated (claim auditor, issue 4). p.V27I and p.E114G are VUS in ClinVar. The paper itself calls them contested and cites mild-to-moderate hearing loss in homozygotes. Our 63 double homozygotes are 84% patients.
- Mildest remedy (the practitioner's option C): keep all rows, and keep the non-benign-only rule comparison in the notes, where it already is, so the curator and readers see where the gain lies.
- Option B (drop the 558) is a case-mix change and its own PR. It would make the task more nearly trivial, not more honest. It does not rest on the stronger rule.

**3. Repeated genotypes are natural, the curator has settled them, and they are the use case (LEAK-18, LEAK-19, LEAK-20: Should)**

- 341 genotypes among 1,778 people is what the biology produces: 126 sparse sites, and 1 to 6 alleles per person. That is LEAK-18's "few features and plausible repeats: natural, keep them and say so", the same pattern as sepsis_survival (975 profiles over 110k rows) and tanzania_tourism (Lennart, 2026-11-05), both kept.
- LEAK-19 is about copies of one record. These are different people, and the curator decided so (issue 1 A).
- The 47 genotypes with both labels are incomplete penetrance, a genuine ambiguity of the task. LEAK-20's own exception covers them.
- The task gamer calls the lookup "the honest model": the genotype is exactly what a counsellor holds.
- The genotype-grouped split (0.41-0.49) tests unseen genotypes, which is not the use case, since the common genotypes are the ones a counsellor meets (issue 1 A; SPLIT-28 keeps known groups when the use case allows).
- The curator asked to reopen this issue with the built data in hand. The data supports A.

**4. The forced random split is honest here; tested, not assumed (SPLIT-36, Should; P4)**

- The tree walk reaches L-PLACE.random, and the curator decided it (issue 2 A). It matches the same-day siblings pheochromocytoma_paraganglioma_metastasis and wild_type_attr_cardiac_amyloidosis.
- The evidence that random folds do not inflate the score:

  | Check | Result |
  |---|---|
  | Discovery file to validation file vs random folds (split auditor, gradient boosting) | 0.750 against 0.750 |
  | Discovery to validation vs size-matched random (task gamer) | 0.756 against 0.743 |
  | Telling the file from the genotype | 0.58 |
  | Patient share, discovery vs validation | 0.759 vs 0.766 |
  | Grouping by a recovered family proxy instead of random (22-30 clusters from the raw order) | 0.752 against 0.750, unchanged (LEAK-42/43: not material) |

- In the family clusters, the label does not travel with the family: the classic trio is a biallelic proband with two carrier parents.
- Relatives on both sides of a fold partly match the use case: cascade testing of relatives is core genetic counselling (split auditor).
- Concede, as wording only:
  - The validation file holds two sources: 466 DPF people and 103 community NGS screenees, unmarked (claim auditor). Three sources is still too few, so the leaf stands; fix the group_basis and splits_comment sentences.
  - The reverse direction scores 0.672. Training on half as many people explains at least part of that (split auditor). Add one clause, or leave it.

**5. No leak, nothing to game (P4; LEAK checks)**

- Every column is a germline genotype count known at the prediction point (column auditor). There is no id, no date, no weight and no column recorded after the outcome.
- The task gamer ran 13 attack families. Every one falls within ±0.0024 of the honest model, and no exploit clears the noise. Restoring the two dropped copy columns leaves the score bit-identical.
- The single shipped-missing cell is harmless (CLEAN-10).
- P4 is the highest-ranked rule a benchmark can fail on evaluation. It holds outright.

**6. The quality defects are real; fix them in the definition, do not exclude (P7; CLEAN-12, Should; remedy ladder)**

- Merge the certain alias sets the column auditor names into one HGVS column each, taking the max per person:
  - GJB2 c.507insAACG / c.507_508insAACG / c.512insAACG, which are one allele, c.508_511dup;
  - SLC26A4 c.915insG / c.915_916insG;
  - SLC26A4 c.36insG / c.35_36insG.
- Note the probable aliases (c.1546/1548insC, the two del7666 names, the GJB2-style names in the SLC26A4 block) as probable. Rename `c.919_2A>G` to `c.919-2A>G`.
- These affect about 40 people at rare sites, so the score barely moves. But the merge is the expert state, and it removes a split of names by recruiting arm.
- The blind reviewer reaches the same conclusion ("merge the obvious synonym groups"), and his verdict is "include with changes", not exclude.
- Per P7, a quality gap makes the benchmark "a little worse": fix it when cheap and safe. This fix is both.

**7. The 53-carrier block: set the marker, keep the rows (LEAK-39 marker rule; precedent: pheochromocytoma)**

- I accept the precedent checker's option (a): add `Class-dependent Recording` next to `Selection Bias`, keep the block, and let the existing note serve as the marker's one note. The marker rule asks for it "also when kept".
- The LEAK-39 Must (drop rows when models learn the route) is not established:
  - The harm test is null. The other test people score 0.733 with the block in training and 0.739 without it (paired -0.0065, sd 0.0094).
  - The route itself is unconfirmed, and the note's guess at it is wrong: the community NGS screening sits in the validation file (Table 1). Replace the guess with "cause unknown".
  - The check on the other class's rows of the same route cannot be run, because the block holds no patients.
- Dropping 53 real carriers (option b) costs 18% of the discovery carriers (53 of 291) to fix an effect the measurement does not show. That is not the mildest remedy.

**The record fixes I concede outright (wording, EV-6/EV-7)**

- `collection_period` should read Oct 2009 - Aug 2020.
- The benign set should be worded "benign in DVD; p.I203T also benign in ClinVar, the other two VUS; contested by the paper". Name p.T123N (ClinVar likely benign; the benign-only group grows from 558 to 581 people, patient share 83.1% against 72.8%, and the conclusion is unchanged).
- Reword `use_case` toward the practitioner's option A: penetrance for a relative or newborn whose hearing cannot yet be tested. Name the benign-only ascertainment in `fit_reason`. The fit stays approximate (USE-8: selection alone does not make it None, and the practitioner does not argue None).
- The metric stays `roc_auc` (MET-5 fallback, the paper ranks by AUC). Every fold has 141 or more negatives, and the practitioner agrees.

**Judgment record (advocate):** Verdict: ship after changes.
- **Validity:** SEL holds; USE-8 approximate (reword the use case); LEAK-18/19/20 natural repeats, kept; SPLIT-36 forced random, tested as not optimistic; PROV holds (identical to the source).
- **Value:** TP-4 step 1 passed 30/30; step 2 is the curator's (gain +0.073 to +0.098 on all rows, +0.026 for the lookup on the non-benign rows).
- **Quality:** CLEAN-12 alias merge; the `Class-dependent Recording` marker with a note; wording fixes.

**Rebuttal (to the critic's opening brief)**

The critic and I agree on most of this. We agree to ship after changes. We agree that points 2 to 5 are fixes in the definition and the record. We agree that issue 1 stays A. The one dispute is the remedy in point 1.

**1. The gain over the rule comes from the selection: concede the item, dispute remedy (b)**

**I concede:**
- On all rows, the methods' gain over the rule lies almost entirely in the 558 people who carry only benign variants.
- The definition must give the curator a TP-4 step-2 item with options. Today it does not.
- Option (a) is the minimum: name the gain in `fit_reason`, and report the rule against the methods on the 1,220 people next to the all-rows score. This is the same as my option C.

**I dispute (b), restricting the rows to the 1,220 people.** The critic's own new table is the evidence against it.

| Part of the release | Benign-only: patient share | Others: patient share |
|---|---|---|
| Hospital records (discovery file, without the 53-carrier block) | 0.816 | 0.784 |
| Validation file | 0.857 | 0.721 |

- **The hospital is where the actor works.** In its records, benign-only people are patients at about the base rate. So a sequenced person whose genes do not explain their hearing loss is a real clinical case: their hearing loss has another cause. A model that learns this learns the clinic's population. The rule gets these people wrong in the hospital's own records too, because it calls every one of them unaffected.
- **The selection gap is in the carriers, not in these people.** The excess (0.857 against 0.721) sits in the validation file's carriers and in the 53-carrier block. That selection affects which carriers were recruited. Dropping the people who carry only benign variants does not remove it.
- **(b) chooses the test rows to suit the rule.** It drops 31% of the people by a feature value: the very rows the rule gets wrong. That is not the mildest remedy (principles, remedy ladder). A note (a) answers the problem, and an exclusion of rows is only for a Must that a note cannot meet.
- **"Clinically inverted" is an inference, not a measurement.** In a general population, a heterozygote of a recessive allele and a carrier of benign variants both sit near the population rate. The ranking that matters for the actor is the one among people who are sequenced, and the hospital rows show it.

**Rule that wins:** TP-4 step 2 is the curator's to weigh. The AI recommends the mildest remedy that resolves it (principles, remedy ladder), which is (a). I would add one line to the item for the curator: "within the hospital's records, benign-only people are 0.816 patients against 0.784 for the others".

**2. The use case names a decision whose label the actor already holds: concede**

- I proposed the same rewording to the penetrance question (option A in my brief).
- I accept the critic's two additions to `fit_reason`:
  - the label is hearing status at one screening, which is not the outcome for p.V37I, SLC26A4 (progressive) and MT-RNR1 (drug exposure);
  - the controls are partly relatives who are obligate carriers.
- The fit stays approximate (USE-8). No data change.

**3. The 53-carrier block: concede (agreed)**

- Add `Class-dependent Recording`.
- Replace the stated cause with "cause unknown".
- Keep the rows: the LEAK-39 test cannot run (the block has no patients), and the effect is small (0.733 against 0.739).
- This is the same as my point 7.

**4. Claims the source contradicts: concede all four**

- **Three sources.** The definition should say three sources, two of them in the validation file. The time basis's "Not tested: another sequencing panel" must change to say that a second panel (103 people, NGS, 2020) is already in the data and is unmarked.
- **Collection period.** `collection_period` should read Oct 2009 - Aug 2020.
- **Benign wording.** Reword as in my brief, and name p.T123N.
- **Transfer claim.** Add the reverse direction to the splits_comment: trained on the validation file, the model scores 0.672, against 0.695 for the expert-like rule, on a training side half as large.

**5. One allele split over several columns: concede, with one correction to my own brief**

- I agree with the merge, taking the maximum over the aliases.
- I listed `c.36insG` / `c.35_36insG` as a certain pair. The column auditor and the critic treat it as probable, and one carrier has both. So it moves to the probable list, with a note. The certain sets are the GJB2 c.508_511dup names and SLC26A4 c.915insG / c.915_916insG.

**Not pressed**

- **Repeats and relatives:** agreed, issue 1 stays A.
- **The 120 missing carriers:** agreed, the note suffices.

**Where the panel stands:** ship after changes. The only open call for the mediator and the curator is TP-4 step 2. The critic recommends (b), restricting to the 1,220 people. I recommend (a), keeping all rows with a stated note, on the evidence of the hospital rows.

</details>

<details><summary>Critic (brief and rebuttal)</summary>

**critic: deafness_gene_carrier_hearing_loss (opening brief, 2026-11-25)**

Position: **ship only after changes.** The data is real and faithfully copied (blind reviewer, task gamer: multiset
identical to Mendeley), no column leaks, and the split is settled (issue 2 A; the split auditor and task gamer find
the random split not optimistic). I do not argue for exclusion. I argue that, as defined, the score mostly rewards
learning how the sample was recruited, and that the definition says several things the source contradicts.

New measurement of mine (light pandas on the two raw files, no model): the share of people carrying only the benign
GJB2 polymorphisms (p.V27I, p.E114G, p.I203T), by part of the release.

| Part | Carriers | Patients | Benign-only: patient share | Others: patient share |
|---|---|---|---|---|
| Discovery, without the 53-carrier opening block | 238 (28.6% benign-only) | 918 (32.8%) | 0.816 | 0.784 |
| Discovery, the 53-carrier block | 53 (0%) | 0 | - | - |
| Validation | 133 (20.3% benign-only) | 436 (37.2%) | 0.857 | 0.721 |
| All | 424 | 1,354 | 0.830 (558 people) | 0.730 (1,220) |

In the hospital's own records (first row) the polymorphisms are near neutral, as the biology says. The record's
83%-against-73% gap comes from the 53-carrier block and from the validation file's carriers, recruited for a hotspot
variant (the paper's "people with ... hot spot variants who passed the hearing screening test").

**1. The model's gain over the expert reading is the sample's prevalence, in a clinically inverted ranking (P6, TP-4 step 2, Must; SEL marker)**

- Problem: the textbook rule calls a person with no pathogenic genotype unaffected. In this case-control sample such
  people are mostly patients: benign-only 0.83, GJB2 single pathogenic allele 0.50, c.235delC heterozygote only 0.34
  (domain practitioner's table on the shipped data). A model learns to rank polymorphism-only people above
  heterozygous carriers of a pathogenic allele; in any real population (hearing loss 1-3 per 1,000) the order is the
  reverse.
- Effect on the task: this is where all of the methods' gain over the rule lies. All rows: rule 0.677 (benign not
  counted), untuned GBM 0.750, lookup 0.781. Without the 558 benign-only people: rule 0.782, GBM 0.774-0.776 (ahead
  on 10-11 of 30, a match), lookup +0.026 (29 of 30) (definition note; claim auditor re-ran on the shipped splits;
  precedent checker). So on all rows ROC AUC ranks models largely by how well they learn recruitment (MET-1 as the
  practitioner reads it); the real gain left is the lookup's p.V37I penetrance.
- Rule: TP-4 (Must), step 1 passes on all rows; step 2 is the curator's call and the definition does not put it to
  him. `Selection Bias` (selection.md): judge the model comparison on the data, not on the marker. The precedent
  checker found no case of a gain that sits in rows whose labels come from the selection.
- Remedy (mildest that works): a TP-4 step-2 item for the curator with options. (a) Keep all rows, name the
  ascertainment gain in `fit_reason` and report the rule against the methods on the 1,220 people next to all rows.
  (b) Restrict the rows to people with a variant other than the three polymorphisms (1,220; a task change, its own
  PR); the methods then match the rule except the lookup, so the curator weighs `Trivial` there. (c) Retire on a
  match (not supported: the lookup beats the rule on 29 of 30). I recommend (b), else (a) at minimum.

**2. The use case names a decision whose label the actor already holds (P3, USE-2, USE-5, USE-8, Must)**

- Problem: the counsellor "judges whether variants explain or predict hereditary hearing loss". The person in front
  of them already has the hearing test, and the test is the label (the definition's own `fit_reason`; domain
  practitioner). Where the genotype is known and the hearing is not (a relative, a newborn, prenatal testing), the
  question is the genotype's penetrance, and the label is hearing status at one screening, not the outcome for
  p.V37I, SLC26A4 (progressive) and MT-RNR1 (drug exposure) carriers.
- Effect: the stated use case does not tell a participant what a good prediction is for; the fit is approximate at
  its weak end (practitioner), not None.
- Remedy: reword `use_case` to the penetrance question for a person whose hearing is not yet tested (USE-9 does not
  apply: the fit stays approximate, so this is no rephrasing to excuse a gap); add to `fit_reason` the label timing
  and that the controls are partly obligate-carrier relatives. No change to the data.

**3. The 53-carrier block needs the `Class-dependent Recording` marker, and its stated cause is refuted (P4, marker under LEAK-39; P5, PROV)**

- Problem: 53 carriers, one class only, none with any of the three polymorphisms (61% of the other 238 discovery
  carriers, 54% of patients), likely recorded through another route. The definition calls it "recording by class,
  kept" but sets no marker. Its guessed cause ("the community NGS screening") is wrong: Luo et al. Table 1 puts the
  2020 NGS screening (103 people) in the validation file; the discovery file is all Sanger hospital records (claim
  auditor, column auditor).
- Effect: small on other people (GBM 0.733 with the block, 0.739 without), but it is one of the two pockets that make
  benign-only people look like patients (table above).
- Rule: the marker is set "whether the artefact was fixed, is kept with a note or is still open" (leak_checks.md,
  after LEAK-40); precedent pheochromocytoma_paraganglioma_metastasis (same day, marker for a kept/fixed artefact);
  pancreatic_cancer_mouse_detection kept `Selection Bias` only because both classes shared the route.
- Remedy: add the marker (precedent checker's option a); replace the attribution with "cause unknown". Dropping the
  block (gallstone) is not supported: the LEAK-39 test on the other class's rows of the route cannot run (no patient
  in it), and the effect is small.

**4. Claims the source contradicts (EV, PROV; Should)**

- "Two recruiting sources, one per file": three; the validation file holds 466 DPF people (Sanger, 2011-2017) and
  103 community screenees (NGS hotspot, 2020), unmarked. The forced leaf still holds (too few sources), but the
  reason and the time basis's "Not tested: another sequencing panel" are wrong: a second panel is already in the data.
- Record `collection_period: Oct 2009 - Apr 2017`: the release runs to Aug 2020.
- The three polymorphisms "read as benign (DVD and ClinVar)": p.V27I and p.E114G are VUS in ClinVar, and the paper
  itself calls them contested; p.T123N (40 carriers, ClinVar likely benign/benign) is left out of the set (581
  people, 83.1% against 72.8%; conclusion unchanged).
- splits_comment's transfer claim holds in the source's direction only; trained on validation, GBM 0.672, below the
  expert-like rule (0.695) (split auditor; smaller training side explains part).
- Remedy: reword these four in the definition and the record; no task change.

**5. One allele split over several columns, partly by file (P7, CLEAN-12, Should)**

- Problem: GJB2 c.508_511dup appears as `c.507insAACG` (17), `c.507_508insAACG` (3, discovery only) and
  `c.512insAACG` (2, validation only); SLC26A4 c.916dupG as `c.915insG` / `c.915_916insG`; probable pairs
  `c.36insG` / `c.35_36insG` (one carrier has both), `c.1546insC` / `c.1548insC`, the two del7666 names; GJB2-style
  names inside the SLC26A4 block (column auditor; blind reviewer independently).
- Effect: about 40 people; a model sees one allele as unrelated sparse columns, split partly by recruiting source.
  Small on the score.
- Remedy: merge the certain alias sets (max over aliases, so a double entry stays one allele), note the probable ones.
  Quality only: no reason to hold the dataset if the curator prefers the files' columns with a note.

**Not pressed**

- Repeated genotypes and relatives (issue 1, reopened as asked): grouping by a family proxy leaves ROC AUC unchanged
  (0.752 against 0.750, split auditor) and genotype-grouped folds test a use case nobody has; I concede A.
- The 120 missing carriers: unexplained and untestable; the note suffices.

**Rebuttal**

We agree on most points. One dispute is left: whether the gain over the rule is a gain a benchmark should reward
(advocate 2, my 1).

| Advocate point | Reply |
|---|---|
| 1. Faithful, licensed, biologically coherent | Concede. |
| 2. Not trivial; keep all rows, comparison stays in the notes (option C) | Dispute in part, see below. |
| 3. Repeated genotypes natural, issue 1 A | Concede (my "not pressed"). |
| 4. Forced random split tested, not optimistic; three sources is wording | Concede. |
| 5. No leak, nothing to game | Concede. |
| 6. Merge the certain alias sets | Concede; we propose the same. |
| 7. `Class-dependent Recording` marker, keep the block, "cause unknown" | Concede; we propose the same. |
| Record fixes (period, benign wording with p.T123N, use case, `fit_reason`, metric) | Concede. These meet my points 2 and 4. |

**On point 2.** I agree that TP-4 step 1 passes and that the AI does not retire on step 2. I dispute two of the
advocate's arguments.

- **"The label of the 558 is contested biology, not ascertainment."**
  - In the hospital's own records (discovery, without the block), benign-only people are 0.816 patients, against
    0.784 for everyone else there. That is close to neutral.
  - In the validation file the same genotypes give 0.857 against 0.721.
  - The same variants with the same biology show a gap four times wider in one file. That is how the carriers were
    recruited (people with a hotspot variant) plus the 53-carrier block, not penetrance.
  - The 63 double homozygotes (84% patients) are 11% of the 558 and cannot carry the whole group.
  - Rule: EV-2, a measurement on the data beats a reading of the literature.
- **"Dropping the 558 makes the task more trivial, not more honest."**
  - Without them, gradient boosting only matches the rule (-0.008, ahead on 10 of 30 splits). That is the honest
    size of a method's advantage on genotypes whose labels are not set by recruitment.
  - The all-rows gain (+0.098, which the advocate sets against sepsis_survival's 0.001) is mostly the sample's 80%
    prevalence among people with no pathogenic genotype. It ranks polymorphism-only people above heterozygotes of
    c.235delC, the reverse of any real population.
  - `Selection Bias` (selection.md): "judge the model comparison on the data, not on the marker". TP-4 step 2 asks
    whether the gain matters for the decision, and this one does not help a counsellor.

**What I concede on point 2.** No Must forces option B. It is the curator's weighing call under TP-4 step 2, and
option C is defensible.

**What I keep.** A note in `curation_comments` is not the decision. The step-2 question must reach the curator as a
review item with options:

- (a) keep all rows with the subset comparison reported;
- (b) restrict to the 1,220 people with a non-benign variant (its own PR);
- (c) retire on the match (not supported, as the lookup still leads by +0.026 on 29 of 30 splits).

I recommend (b); the advocate recommends (a).

**Verdict (critic, after rebuttal):** ship after changes. These are the agreed definition fixes (alias merge, the
marker, wording of sources, period, benign set, use case and `fit_reason`) and one open curator item, TP-4 step 2:
rows (a) or (b).

</details>
