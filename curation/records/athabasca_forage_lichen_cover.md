---
unique_name: athabasca_forage_lichen_cover
name: Lichen percent cover / forage-lichen plots for caribou habitat mapping (Keim et al. 2017)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Not Available (from Paper))
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2017'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.1002/ece3.2625
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5243790/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Forage-lichen cover in 2 x 2 m plots with QuickBird, Landsat and SPOT reflectance, LiDAR height, groundwater depth and
Sphagnum cover as covariates; the objective is to "delineate the geographic distribution and abundance of
terrestrial forage lichens" (Introduction). Results: "Field crews sampled 438 vegetation plots (251 fixed and 187
opportunistic plots)", 98 of them with zero cover. No table is released: the three DOCX appendices hold site
conditions, caribou feeding sites and a Sphagnum model, and the paper has no data statement. So `No` with
`Not Available (from Paper))`, as the workbook's access queue already suspects.

Zero mechanism, from the paper only: no lichen in the plot, but the zero share is set by the design, since
opportunistic plots were taken only "if crews encountered a lichen patch with >10% lichen cover" (Methods). Not the
same study as the post-fire lichen biomass releases (`boreal_postfire_lichen_biomass`).

## Reference

Keim J.L., DeWitt P.D., Fitzpatrick J.J., Jenni N.S. (2017). Estimating plant abundance using inflated beta
distributions: applied learnings from a lichen-caribou ecosystem. Ecology and Evolution 7:486-493.
doi:10.1002/ece3.2625.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 19 (Lichen percent cover).
