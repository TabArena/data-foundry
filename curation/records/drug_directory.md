---
unique_name: drug_directory
name: drug-directory
checked_by:
- Lennart
suggestion: TBD -> 2nd Tier
tags:
- 2nd Tier / Scientific Discovery
collections:
- TabSTAR
source_links:
- https://www.openml.org/search?type=data&id=43044&sort=runs&status=active
source_row: 456
type_adapter_id: curation-record-v1
---

## Comments

Just a list of drug listings, not a real predictive task

Little to no informative features

**Assessment (AI, 2026-10-31):** the benchmark STRABLE (https://arxiv.org/abs/2605.12292) carries a related version, "Drug NDC", not this record's data, so no collection tag: Related record: drug_directory (TabSTAR; OpenML 43044, the same FDA National Drug Code directory, target PRODUCTTYPENAME; 'not a real predictive task'). STRABLE's version is the openFDA NDC API with target dea_schedule and only 583 rows (scheduled products), so a different target on the same source.

**Assessment (AI, 2026-11-01):** STRABLE's "Drug NDC" now has its own record, `openfda_ndc_dea_schedule`.
