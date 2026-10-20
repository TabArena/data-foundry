---
unique_name: north_american_breeding_bird_survey_counts
name: North American Breeding Bird Survey (USGS), 2026 release, 1966-2025
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: GOV Website
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5066/P144YU3S
- https://www.usgs.gov/data/2026-release-north-american-breeding-bird-survey-dataset-1966-2025
- https://www.sciencebase.gov/catalog/item/6a0b0b0ab66b0188da36aedd
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

The North American Breeding Bird Survey, released by USGS: every June a skilled volunteer runs a 39.2 km roadside
route with 50 three-minute point counts, about 3,000 routes a year in recent decades and none in 2020 (ScienceBase
abstract). The release has Routes.csv, Weather.csv (run history: date, times, weather, observer, RunType),
SpeciesList.csv, VehicleData.csv and the counts in States.zip and 50-StopData.zip. Only Routes.csv was measured (5,845
routes: 4,458 US, 1,387 Canada), from a Wayback copy: ScienceBase answers automated requests with a Cloudflare
challenge and the archive holds no other file. The stated purpose is "scientifically credible measures of the status,
trends, and environmental associations of North American birds" (ScienceBase item, Purpose).

Zeros: a species counts as zero on every run of Weather.csv without a count row for it (zero-filling, not confirmed
from the data). A tabular task would predict one species' route-year count from route coordinates, stratum, BCR,
year, date, start time, weather and observer. The release has no habitat covariates, so a model reduces to route,
observer and year effects, the structure of a trend analysis, and with a route's earlier counts as features it becomes
forecasting of route series up to 60 years long. Same verdict as `great_lakes_marsh_bird_point_counts` (trend
monitoring). A habitat-based abundance task would need land cover joined from elsewhere, which would be our
construction; if reopened, group by route. Licence: CC0 1.0.

## Reference

Ziolkowski D., Lutmerding M., Skalos S.M., English W.B., Hudson M.-A.R. (2026). 2026 Release - North American
Breeding Bird Survey Dataset (1966 - 2025). U.S. Geological Survey data release. doi:10.5066/P144YU3S.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
