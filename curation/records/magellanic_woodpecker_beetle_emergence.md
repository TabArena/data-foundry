---
unique_name: magellanic_woodpecker_beetle_emergence
name: Magellanic woodpecker / wood-dwelling beetle emergence in excavated and control trees
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- Two-Regime Zeros
original_source: Other
year: '2025'
domain: biology & life sciences
required_split:
- '?'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.crjdfn3hj
- https://doi.org/10.1111/icad.70025
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: beetle counts per emergence trap and season in 22
landscapes, with wood decay and environmental covariates, sampled case-control (trees used by Magellanic woodpeckers
against control trees) to test the woodpecker as an indicator; a multi-site survey with environmental covariates, so
the family's open species-abundance question decides it.
- Source: Vergara, Quiroz, Alaniz et al. 2025, "Magellanic woodpeckers as indicators of wood-dwelling beetle diversity
  in trees with different levels of decay and under changing environmental conditions", Insect Conservation and
  Diversity 19(1):211-227 (doi:10.1111/icad.70025, online 29 Sep 2025); Dryad doi:10.5061/dryad.crjdfn3hj (11 Sep
  2025, CC0, 360.78 KB): `Data.Vergara.2025.csv` (305 KB; counts of 297 beetle species per trap and season over five
  seasons, summer 2023 to summer 2024), `Environment.csv` (wood decay by sonic tomography, trunk diameter, PSRI, VCF,
  temperature, elevation), `Taxa.csv`, an R script and a README. `Land` is "a 22-level categorical variable containing
  the landscape code in which the traps were deployed", with 3 plots per landscape (README). The README and script
  load `Datos.csv`, which is not in the file list. Not downloaded; the paper was not read (abstract only).
- Aim, in the source's words: "We investigated whether the trees used by Magellanic woodpeckers" have "a greater
  diversity of wood-dwelling beetles of different functional groups"; "These results suggest Magellanic woodpeckers
  can serve as indicators of wood-dwelling beetle communities" (Abstract). `Wood` (foraging holes) is case-control
  sampling, not a treatment (reject check).
- Use case: none named for a prediction. For example a forest manager estimating a beetle guild's abundance in stands
  from wood decay and environmental covariates, to choose trees or stands to retain; fit approximate, with the
  case-control sampling as a named gap (a use case the curation wrote). Regime grouped by landscape, a trap's seasons
  together (SPLIT-3, SPLIT-13).
- Zeros: no beetle of a guild emerged into a trap in a season; not measured, and the workbook's "ZIP fitted" could not
  be checked.
- Siblings and duplicates: none in the log. Family records on the same open question:
  `great_lakes_marsh_bird_point_counts`, `plains_wanderer_spotlight_counts`. External collections: none found.
- Metric: none found (abstract and README only; the paper was not read), so the fallback `rmse`.
- Risks for /add-dataset: deposit completeness (the README and script load `Datos.csv`, not in the file list; probably
  the data file under another name); rows (trap x season) and trees per plot; the target as one guild's abundance
  built from the species columns through Taxa.csv, those columns then dropped (SEL-5); the zero share per guild; the
  join with Environment.csv; split grouped by landscape with a trap's seasons together; PSRI and VCF are
  remote-sensing products, to check as measurements (SEL-15) rather than image descriptors (SEL-13); the open
  species-abundance question (triage summary, "Policy questions"; SEL-3, USE-1).
- Priority: gap 0 (biology & life sciences 4; regression and grouped not thin), use case 0 (none named), source +
  (paper, a documented deposit), shape 0 (rows not counted; 22 landscapes), risk - (target to build from species
  columns, a data file missing).
- Reject check (AI, 2026-10-27): does not stand. Traps in 22 landscapes over five seasons with environmental
  covariates make a multi-site observational survey, the woodpecker holes are case-control sampling rather than a
  treatment, and "the tool is the woodpecker sign, not a model" was a reading of the abstract.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page).
No reason was given on the page; the record's markers (`No Good Target / Scientific Discovery`) stand as the reason.

Wood-dwelling beetles caught in emergence traps on stem sections excavated by Magellanic woodpeckers and on control
trees (Vergara et al. 2025). Dryad abstract: "We investigated whether the trees used by Magellanic woodpeckers ...
have a greater diversity of wood-dwelling beetles", sampled "using emergence traps ... comparing stem sections
excavated by woodpeckers with those of control trees". A case-control indicator test analysed with structural
equation paths, in which woodpecker use is the sampling stratum. Files: a 0.31 MB data CSV plus environment and taxa
tables; not downloaded (Dryad blocks automated downloads), and the number of trees and sections is not stated in the
text that could be read.

Zero mechanism: no beetle of a guild emerged into a trap; not confirmed, and the workbook's "ZIP fitted" could not be
checked because the paper text was not reachable. Licence: CC0.

## Reference

Vergara P.M., Quiroz M., Alaniz A.J., et al. (2025). Magellanic woodpeckers as indicators of wood-dwelling beetle
diversity in trees with different levels of decay and under changing environmental conditions. Insect Conservation
and Diversity 19:211-227. doi:10.1111/icad.70025. Data: doi:10.5061/dryad.crjdfn3hj.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 15 (Magellanic woodpecker / beetle abundance).
