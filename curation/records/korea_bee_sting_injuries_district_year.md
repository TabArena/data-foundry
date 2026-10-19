---
unique_name: korea_bee_sting_injuries_district_year
name: Bee-sting injuries / emergency-department bee-sting counts by district-year, South Korea 2014-2021
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Not Available (from Paper))
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.3389/fpubh.2026.1742966
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

An exploratory association study of bee-sting injuries with climate and land cover (Kim and Min 2026; paper read via
its JATS XML): the "annual count of bee sting injuries aggregated at the administrative district level by year"
(Sec. 2.2), 250 districts x 8 years = 2,000 rows, modelled with a zero-inflated negative binomial. The outcome comes
from NEDIS, the restricted national emergency-department database. Data availability: "The original contributions
presented in the study are included in the article/Supplementary material, further inquiries can be directed to the
corresponding author"; the supplement is one image and two DOCX tables that, going by their captions, hold AIC
values and annual counts, not a district-year table. So no released table, and the aim is association, not
prediction.

Zero mechanism, from the paper only: no emergency-department case in a district-year, "469 zeros among 2,000
district-year observations (23.4%)". The workbook's size is right; its access is not.

## Reference

Kim Y., Min K.-D. (2026). Associations of bee sting injuries with environmental and social factors: an exploratory
study. Frontiers in Public Health 14:1742966. doi:10.3389/fpubh.2026.1742966.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 12 (Bee-sting injuries).
