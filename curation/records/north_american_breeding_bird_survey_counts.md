---
unique_name: north_american_breeding_bird_survey_counts
name: North American Breeding Bird Survey (USGS), 2026 release, 1966-2025
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
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
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: the largest bird survey of the family (5,845 routes,
1966-2025), published for status and trends, without habitat covariates; USGS itself maps mean abundance away from the
routes, so the family's open species-abundance question decides whether a prediction task exists.
- Source: the North American Breeding Bird Survey (USGS with Environment and Climate Change Canada), run since 1966;
  this record is the 2026 release (Ziolkowski, Lutmerding, Skalos, English and Hudson, doi:10.5066/P144YU3S, 3 June
  2026, CC0). As published: route, weather (run) and species tables and the counts per route, year and species; the
  fields are survey date, start and end times and weather, observer, route id and location (country, state, BCR) and
  start coordinates, and a run quality flag (USGS data page). Routes.csv, which also has the stratum, holds 5,845
  routes (earlier AI triage, 2026-10-20, measured from a Wayback copy); the counts were not downloaded (ScienceBase
  answers with a Cloudflare challenge, 403 again on 2026-10-27).
- Purpose, in the source's words: the program "provides reliable population data and trend analyses on more than 500
  bird species" and serves "to evaluate the status of continental bird species" (USGS EESC, "North American Breeding
  Bird Survey"); the release's Purpose names "status, trends, and environmental associations" (ScienceBase, as read by
  the earlier AI triage on 2026-10-20). USGS's BBS Mapping Products (Sauer et al., 28 Jan 2025): "mean abundances for
  the interval 2018-2022 are spatially smoothed from data for each species collected on BBS routes"
  (https://www.usgs.gov/data/north-american-breeding-bird-survey-mapping-products-1966-2022, as quoted by the reject
  check; the sentence's start checked).
- Use case: none named for a prediction. For example a wildlife agency estimating a species' breeding abundance where
  no route runs, to set conservation priorities, as USGS's own smoothed maps do; fit approximate (a use case the
  curation wrote). Regime grouped by route (SPLIT-3); years repeat per route (SPLIT-13).
- Zeros: a species counts as zero on every run without a count row for it (zero-filling against Weather.csv; earlier
  AI triage, not confirmed from the data).
- Siblings and duplicates: no duplicate in the log. `great_lakes_marsh_bird_point_counts` is also a trend survey but
  ships habitat covariates (`TBD -> 2nd Tier`, priority 2 in this pass). External collections: none found. Harris,
  Taylor and White 2018 (PeerJ 6:e4278) hindcast BBS richness at 1,237 sites with climate and remote sensing, and none
  of their models "consistently outperformed a baseline model that predicted constant richness at each site": the
  forecasting framing to avoid (SEL-10).
- Metric: none found for a prediction (USGS program and data pages; the trend and mapping products report estimates,
  no prediction score), so the fallback `rmse`.
- Risks for /add-dataset: measure (EV-1) whether a task from the release alone (start coordinates, BCR, stratum, date,
  weather, observer), split by route, beats a per-stratum or spatial-smoothing baseline; a habitat-joined version
  (NLCD or similar) is a separate record (PROV-11, PROV-14); the target is one species' count per route and year,
  zeros filled against the runs of Weather.csv (RunType 1); no lagged counts as features (SEL-10, TP-10); observer and
  first-year-observer effects; getting past ScienceBase's Cloudflare block; the open species-abundance question
  (SEL-3, USE-1; settled by Andrej on 2026-10-30, policy question 1 of the zero-inflated review: no new rule, each
  survey judged on its own use case).
- Priority: gap 0 (biology & life sciences 4; regression and grouped not thin), use case 0 (none named for a
  prediction), source + (USGS data release with documentation), shape + (5,845 routes over 60 years, grouped and
  temporal structure), risk - (no habitat columns, target species unsettled).
- Reject check (AI, 2026-10-27): does not stand. "The only model it supports is a trend model" was a reading: the
  release carries start coordinates, BCR and stratum, and USGS's own mapping products smooth abundance away from the
  routes, which is the subject of the open species-abundance question.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening review page).
"No predictive task"

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
