---
unique_name: crms_phragmites_cover
name: Phragmites cover / CRMS herbaceous marsh vegetation, Louisiana coast (Phragmites australis cover per plot visit)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: GOV Website
year: '2006'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.lacoast.gov/crms2/
- https://cims.coastal.la.gov/RequestedDownloads/ZippedFiles/CRMS_Marsh_Vegetation.zip
- https://doi.org/10.1002/eap.70246
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Louisiana's Coastwide Reference Monitoring System (CPRA with USGS): vegetation of 4 m2 marsh plots. Downloaded the
full export on 2026-10-19 (10 MB zip, 250 MB long CSV, one row per species per plot visit): 594,288 rows, 75,418
plot visits at 4,619 stations of 401 sites, July 2006 to July 2026, about 3,800 visits a year. A monitoring table
without a prediction task; the 2026 study the workbook cites analyses expansion trends and impacts (abstract summary
only, text not read). A plot-level model would need site hydrology and soils joined from other CIMS tables, and the
same-visit columns (total cover, other species, community class) are co-measurements of the target.

Zero mechanism, confirmed from the data: Phragmites cover is exactly 0 in 94.1% of visits (4,476 visits with cover).
Only 97 of 401 sites ever record it, and 80% of the zero visits are at sites that never had it, so most zeros are
structural absence from the species' range and the rest absence from the plot; 2,576 "Out" rows (seen near the
plot) carry no cover. Workbook pushback: the table is downloadable, and no zero-inflated beta model was found in the
2026 paper's summary. No licence stated beyond a CPRA disclaimer.

## Reference

Coastwide Reference Monitoring System (CRMS), Coastal Protection and Restoration Authority of Louisiana,
https://www.lacoast.gov/crms2/. Guo Y., Roberts B.J., Nyman J.A., Plumlee J.D., Davenport T.M., Hopper G.W., La Peyre
M. (2026). Expansion trends and impacts of Phragmites australis on the Louisiana Gulf Coast. Ecological
Applications. doi:10.1002/eap.70246.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 9 (Phragmites cover / CRMS).
