---
unique_name: deafness_gene_carrier_hearing_loss
name: Hearing loss among carriers of GJB2/SLC26A4/MT-RNR1 variants (Luo et al. 2021, Mendeley 6mh8mpnbgv)
checked_by:
- Andrej
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
collection_period: Oct 2009 - Apr 2017
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://data.mendeley.com/datasets/6mh8mpnbgv/1
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
- https://doi.org/10.17632/6mh8mpnbgv.1
- https://doi.org/10.1016/j.ebiom.2021.103322
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

## Review

**Outcome:** not added; screened `TBD -> 2nd Tier`, priority 1. Luo et al. 2021 (Mendeley, CC BY 4.0): 1,209 + 569 carriers of GJB2, SLC26A4 or MT-RNR1 variants, hearing loss or normal hearing; the label is the phenotype, not the mode of inheritance; 280 genotype patterns in 1,209 rows and family members without an id.

**Main points:** Repeated genotypes as the task or as copies (issue 1); random split or the source's two files (issue 2).

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
