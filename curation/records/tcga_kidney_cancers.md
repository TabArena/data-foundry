---
unique_name: tcga_kidney_cancers
name: TCGA Kidney Cancers
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
decision_markers:
- Needs extensive data wrangling
tags:
- Many features
- New IID
collections:
- New (BeyondArena)
source_links:
- https://doi.org/10.24432/C5702T
source_row: 516
type_adapter_id: curation-record-v1
---

## Comments

Not super sure this counts as a full tabular task. Needs more time 

A lot of features! Might need some basic unsupervised feature selection first

Link to the website is broken. Cannot find the exact csv with the number of instances as on UCI website

Very unclear how to go from gov website to a usable merged dataset, as it seems to be merged from various cases. I am missing the domain knowledge to figure out what to do with the data

**Assessment (AI, 2026-10-26):** a question to settle if this record is added, carried from the glioma_grading review (USE-5): is a label correct under the criteria of its era but renamed by a later classification kept with a note? glioma_grading_clinical_and_mutation_features raised it (TCGA's histological grade of 1989-2013, partly renamed by WHO 2021) and was retired on its use case (USE-1, 2026-10-26) before it was decided. Record the answer as a USE-5 Cases row.
