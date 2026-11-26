---
unique_name: maize_nam_flowering_time
name: NAM-maize-DTA (Maize Nested Association Mapping Flowering Time)
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
- Non-IID (Grouped)
original_source: Other
year: '2009'
collection_period: 2006-2007
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1126/science.1174276
- https://www.panzea.org/phenotypes
- https://cornell.box.com/s/su1vodojjq5g8wg2aw8crimdx6328px6
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public
knowledge of this dataset and from the archive's own files, NOT from a built dataset. A human must verify everything
before relying on it.**

**Screening (AI, 2026-11-26):** `TBD -> Yes`, priority 4: days to anthesis of 4,699 maize recombinant inbred lines
of the 25-family Nested Association Mapping population from 1,106 imputed linkage-map markers, the line value a BLUP
across eight environments; the genomic-selection task of `genomic_prediction_maize_flowering_time` on twelve times
the lines, with the families as a group key and the raw plot data shipped beside the line values.
- Source: Buckler et al., "The genetic architecture of maize flowering time", Science 325:714-718, 2009
  (doi 10.1126/science.1174276; the publisher refuses automated fetches, so the paper's own text is unread in this
  run). The data is Panzea's "Buckler_etal_2009_Science_flowering_time_data-090807.zip", listed on its phenotypes
  page as "Flowering time phenotypes and imputed genotypes of our maize NAM population from Buckler et al. 2009"
  and downloaded 2026-11-26 (3.76 MB, seven files). As published, counted in the files: `markergenotypes062508.txt`
  holds 4,699 lines x 1,106 markers coded 0, 0.5, 1, 1.5 and 2 with no missing cell, 1.44% of cells carrying an
  intermediate imputed dosage, and the three traits in the same table, but no line identifier;
  `NAMSum0607FloweringTraitBLUPsAcross8Envs.txt` holds 5,463 lines with the family (25 `Z` groups of 190 to 200
  lines, and 481 rows that carry none), days to anthesis 58.40 to 121.21 (mean 77.04, sd 4.20), days to silk, and
  the anthesis-silking interval; four per-plot tables of 43,459 and 43,055 rows (days to tassel, days to silk and
  the two raw dates) span 9 location-year-rep rows, the paper's 8 environments, with B73 standing in 1,993 plots as
  the check grown everywhere; `markers061208.txt` holds the 1,106 markers with chromosome and position. Target
  `days2anthesis`.
- Use case: a maize breeder, before the season, ranks unphenotyped lines of the breeding population by predicted
  flowering time and chooses which to advance (genomic selection); fit direct inside the population, approximate
  for other germplasm. Collection: one designed population grown in replicated trials over two summers, the
  genotype fixed before the season and the trait read in the field, a line's value a BLUP over its own plots
  (`Samples: No Time Dimension`, `Entities: Recur`); the plot tables date the trials to 2006 and 2007, the line
  table carries no date. Type `Experimental Results` (a closed set of lines measured by one trial protocol,
  SPLIT-34).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the family) because [EXP.meets] is a line of a cross the
  training side does not hold and [EXP.kind-key] is yes (the family, 25 groups of 126 to 196 genotyped lines),
  which is the leaf `genomic_prediction_soy_yield` reached on the same shape; open: whether the breeder instead
  meets a new line of a cross already phenotyped, which is L-EXP.random, and the enough-groups check on 25
  families.
- Siblings and duplicates: `genomic_prediction_maize_flowering_time` (`TBD -> 2nd Tier`, priority 2) is the same
  trait of the same species on another population, Azodi et al. 2019's pan-genome cut of 391 lines; this record is
  the better data that screening named, and from another population it is its own record, not a duplicate (PROV-4).
  `genomic_prediction_soy_yield` (`Yes`, a built folder) is the same task shape in another crop, so a distinct task
  (PROV-7), and its decisions on the group key and the metric are the precedent here.
  `genomic_prediction_rice_flowering_time` and `genomic_prediction_switchgrass_height` are the other Azodi cuts.
  External collections: none.
- Better data: none found for this task in this round. The same source holds a far denser genotype of the same
  population (Panzea's ZeaGBS v2.7, 955,690 SNPs over 17,280 public samples, of which the NAM share is not stated
  on the page), which is more markers for the same lines rather than more units, so it is a version question for
  the curator (PROV-6) and not better data.
- Papers and pages: Buckler et al. 2009 (above); https://www.panzea.org/phenotypes; the archive at
  https://cornell.box.com/s/su1vodojjq5g8wg2aw8crimdx6328px6.
- Metric: none found at the source: Buckler et al. is a QTL-mapping paper and the Panzea page defines no task, so
  there is no deliberate choice (MET-5). The nearest named metric for this task is Azodi et al. 2019's pooled
  Pearson's r, which is context from a sibling and not this source's call. On the shipped BLUPs the between-family
  share of the days-to-anthesis variance is 0.472, so MET-18 applies as it does on `genomic_prediction_soy_yield`
  (54.3%): the metric is declared per family, the pooled score is named as the original from context, and the
  declaration reports the share and what a family-mean predictor scores. Inputs: the family, which ships.
- Risks for /add-dataset: the genotype table ships no line identifier, only the family and the three traits, so its
  join to the BLUP table is positional; checked here, every one of the 4,699 trait values matches a BLUP value of
  its own family to two decimals and the first rows align exactly, so the trait doubles as the key, but a build
  states this and asserts it (PROV-13). The genotype table holds 4,699 of the BLUP table's 5,463 lines, and which
  764 it drops is unchecked. The markers are imputed at the source and cannot be checked from the release
  (LEAK-30 at most); 1,106 markers is a coarse linkage map beside what this population now has. Panzea states no
  licence or terms of use on the pages read (EV-4, no verdict reason). The plot tables hold the check B73, which is
  not a NAM line and must not become a row of the line table. Duplicate marker profiles were checked and there are
  none.
- Priority: gap 0 (biology & life sciences has 11 accepted, thin at 6.5 or fewer, and regression 78 is not thin),
  use case + (the breeder and the selection decision are named by the task's own literature), source + (a Science
  paper, a public archive, and the raw plot values beside the line values), shape + (4,699 lines x 1,106 markers),
  no minus: the positional join is measured and settled here, and the unstated licence is no verdict reason.

CC (2026-11-26, Andrej): accepted, go to `/add-dataset`.
- The screening's verdict stands: 4,699 lines over 25 families, 1,106 markers, the target in days, and the raw plot values beside the line values.
- Priority 4 kept. Nothing was built at screening.
