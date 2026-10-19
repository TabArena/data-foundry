---
unique_name: upper_mississippi_sav_rake_biomass
name: SAV biomass - Upper Mississippi River / developing methods for estimating SAV biomass (LTRM Pools 4 and 8, 2017)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Trivial
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: GOV Website
year: '2020'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.usgs.gov/datacatalog/data/USGS%3A5e2b0313e4b0a79317cf9500
- https://doi.org/10.5066/P9GFFYZH
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

A USGS method-calibration data release (Upper Midwest Environmental Sciences Center, LTRM): submersed aquatic
vegetation on rakes at 100 sites in Pools 4 and 8, 19 June to 9 August 2017, with rake IDs 1-1922, stratum, rake
number (1-6), species and species group, "Fresh weight (g)" (0-4110) and a 0-5 rake density score (`PD_sav_new`).
The metadata states the purpose: "Relationships between submersed aquatic vegetation mass caught on rakes and total
plot biomass were developed". The rake density score is the visual fullness score of the same rake, a direct proxy
for the weight, hence the provisional `Trivial`. The two CSVs sit on ScienceBase behind a Cloudflare challenge (403)
and were not downloaded; counts come from the FGDC metadata.

Zero mechanism, from the metadata only: "a value of 0 means no submersed aquatic vegetation present at the site",
i.e. nothing on the rake, which is non-detection rather than proven absence, and the zero part is given by a density
score of 0; also "weights less than one gram were entered as one gram". Workbook pushback: the data are 2016-17 field
work released in 2020, and no 2026 structural-zero paper using them was found. Licence: public domain (USGS).

## Reference

Drake D., Lund E. (2020). Developing methods for estimating SAV biomass in the Upper Mississippi River. U.S.
Geological Survey data release, doi:10.5066/P9GFFYZH (LTRM completion report LTRM-2018BI03).

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 4 (SAV biomass - Upper Mississippi River).
