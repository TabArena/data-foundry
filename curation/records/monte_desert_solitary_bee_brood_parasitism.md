---
unique_name: monte_desert_solitary_bee_brood_parasitism
name: Bee brood parasitism / trap-nesting solitary bees across the Monte Desert, Argentina (2021-22)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Too Small
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Too Small`, TP-5; `No Good Target / Scientific Discovery`, SEL-3): a
one-season driver analysis of brood parasitism at nine sites, whose predictors are all constant within a site, so a
model sees nine independent units.
- Source: dos Reis Diniz et al., Figshare doi:10.6084/m9.figshare.29310806.v1 (2025-06-13, CC BY 4.0), described as
  "Evaluation how nest and brood cell abundance, climate, and latitude drive brood parasitism in wild cavity-nesting
  solitary bees across a broad environmental gradient in the Monte Desert of Argentina"; paper dos Reis Diniz et al.
  2026, Apidologie 57:43 (open access, read on link.springer.com): "528 solitary bee nests comprising 2080 brood
  cells".
- Size (TP-5): the reject check measured `data-emerg-2021.csv` on 2026-10-27: 529 rows, 78.3% zero `prop.paras`;
  `latitudeS`, `mean.temp`, `mean.rh`, `total.nests` and `total.cells` each take 9 values, constant within a site.
  The other nest-level columns are outcome counts or species coded from emergence (`sp.hosp` = "-" when a nest was
  fully parasitized, a target leak). Nine independent units, against 38 in `qtp_urban_wasteland_plant_diversity`
  (`TBD -> 2nd Tier`, this run); the earlier triage's LightGBM grouped by site scored R^2 -0.47.
- Use case: none. Sec. 1: "Here, we evaluated whether host abundance, climate, and latitude drive brood parasitism"
  in cavity-nesting bee communities; Sec. 2.3: "We used zero-inflated binomial models (ZIBMs) to assess how biotic
  factors" (nest and brood-cell abundance) and temperature, humidity and latitude drive parasitism; one season,
  September 2021 to April 2022, at "nine sites distributed across the latitudinal extent of the Monte Desert ecoregion"
  (Sec. 2.1-2.2). The paper names no prediction or management use.
- Siblings and duplicates: none (grep brood parasit, solitary bee, trap-nest). External collections: none.
- Metric: none (no task).
- Reject check (AI, 2026-10-27): stands, re-grounded on TP-5 (Must). Every predictor in the Figshare CSV takes one
  value per site at 9 sites (https://doi.org/10.6084/m9.figshare.29310806.v1), so a held-out site leaves eight to
  learn from.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 48 (Bee brood parasitism).
