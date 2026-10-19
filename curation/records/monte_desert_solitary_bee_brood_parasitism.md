---
unique_name: monte_desert_solitary_bee_brood_parasitism
name: Bee brood parasitism / trap-nesting solitary bees across the Monte Desert, Argentina (2021-22)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Too Small
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2025'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6084/m9.figshare.29310806.v1
- https://doi.org/10.1007/s13592-026-01287-z
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Parasitized and total brood cells of trap-nesting solitary bees at 9 sites along the Monte dryland gradient (dos Reis
Diniz et al. 2026). Downloaded from Figshare on 2026-10-19: 529 rows x 16 columns (528 nests after one exact
duplicate), 2,082 cells, no missing values; the share of nests with zero parasitism (`prop.paras`) is 78.2%, and the
flags give 115-117 parasitized nests against the paper's 116. All five predictors are site-level (latitude,
temperature, humidity, total nests and cells), so n is effectively 9: a within-site mean explains R^2 0.13 in sample,
and LightGBM grouped by site scores R^2 -0.47. Sec. 2.3 uses "zero-inflated binomial models (ZIBMs) to assess how
biotic factors" drive parasitism.

Zero mechanism: zeros confirmed from the data, but the two regimes are not observable; the Fig. 2 caption says the
never-at-risk versus sampling-zero "classification is not directly observable". Also, `sp.hosp` = "-" marks fully
parasitized nests, a target leak if kept. Licence: CC BY 4.0 (Figshare).

## Reference

dos Reis Diniz M., et al. (2026). Drivers of brood parasitism in solitary bees across a South American dryland
ecoregion. Apidologie 57:43. doi:10.1007/s13592-026-01287-z. Data: doi:10.6084/m9.figshare.29310806.v1.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 48 (Bee brood parasitism).
