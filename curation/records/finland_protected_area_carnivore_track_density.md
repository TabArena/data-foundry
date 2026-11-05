---
unique_name: finland_protected_area_carnivore_track_density
name: Finnish large-carnivore FWTS / matched protected-area and control track densities, 1989-2017 (Terraube et al. 2020)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
- Not Representative
tags:
- Two-Regime Zeros
original_source: Other
year: '2020'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.s1rn8pk4w
- https://doi.org/10.1038/s41467-020-16792-7
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: snow-track indices of four large carnivores on Finnish
Wildlife Triangle Scheme routes, with habitat and human-pressure covariates, released as the matched
protected-versus-control subset of a causal study; whether abundance mapping from such a survey is a task is the
family's open species-abundance question.
- Source: Terraube, Van doninck, Helle and Cabeza, Nature Communications 11 (2020), doi:10.1038/s41467-020-16792-7 (read
  via PMC7289803); data on Dryad, doi:10.5061/dryad.s1rn8pk4w (2020-05-28, CC0). As published (Dryad file list, read
  through the Dryad API; files not downloaded, the API answers 401): two matched analysis tables,
  `FinalMatchedData_WintDens_22Nov19_AllIUCNCatSpec.csv` (lynx, wolf, wolverine) and
  `FinalMatchedData_Bear_22Nov19_AllIUCNCat.csv` (2.2-2.3 MB each), two pre-matching unit tables
  (`MatchingDataset_19Nov19.csv`, `MatchingDatasetBear_19Nov19.csv`) and three R scripts. A row is a route (triangle)
  and year; the target is fresh-track crossings per 24 h per 10 km; covariates forest cover, terrain ruggedness,
  distance to settlements, human density, latitude, year and protection status (Methods).
- Use case: none stated. The aim (Introduction) is to "assess the effectiveness of Finland's PA network in supporting
  abundances of four large carnivore species", through "one-to-one, nearest-neighbor covariate matching with
  replacement" (Methods), so control routes repeat. The survey itself "provides yearly estimates of the distribution and
  relative abundance of game species" (Dryad methods): for example a game agency estimating carnivore abundance on
  routes without a count, a framing the source does not make; fit approximate. Regime grouped by route (routes recur
  1989-2017; a matched pair stays in one fold).
- Doubt: the earlier pass set `No` (SEL-3, a treatment-effect design). The aim is causal, but the release is a national
  survey with habitat covariates, so the call falls under the open species-abundance-mapping question
  (settled by Andrej on 2026-10-30, policy question 1 of the zero-inflated review: no new rule, each survey judged on
  its own use case); no fast reject. `Not Representative` added
  for the matched sample.
- Siblings and duplicates: no other record on the Wildlife Triangle Scheme (searched by name, DOI and species). Family
  ecology records of the earlier AI pass, re-screened in this run: `noaa_afsc_bottom_trawl_survey_cpue` and
  `wadden_sea_sibes_macoma_abundance` TBD -> Yes, `nantucket_sound_sea_duck_aerial_survey_counts` 2nd Tier,
  `north_american_breeding_bird_survey_counts` No (no habitat covariates). External collections: none found.
- Papers and pages: the Nature Communications paper; Linden et al. on the survey method (cited there, not read).
- Metric: none found (the paper fits zero-inflated hurdle mixed models for inference and reports no held-out score; PMC
  text and Dryad page checked); fallback `rmse`, with the family's open question on the metric for zero-heavy targets.
- Risks for /add-dataset: the matched subset is a selective sample with reused controls (`Not Representative`); 1,805 of
  2,171 routes were kept ("we discarded transects in mixed agricultural-forest landscapes", Dryad methods), and the full
  series, compiled by the Finnish Game and Fisheries Research Institute (now Luke), is not in this release (access
  unverified); bear comes from summer counts in a separate file; the zero share is not measured (the paper: "zero
  inflation of all time-series").
- Priority: gap 0, use case 0 (none stated), source + (paper and Dryad methods), shape + (about 1,220 matched routes
  over up to 29 years, seven covariates, grouped), risk - (matched sample with reused controls).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2, as screened (verified on the zero-inflated screening review
page).

Finnish Wildlife Triangle Scheme track indices for lynx, wolf, wolverine (winter) and brown bear (late summer) in 12
km triangles inside protected areas and matched controls (Terraube et al. 2020; paper read via PMC7289803). A row is
a triangle x year x species; the target is crossings per 24 h per 10 km; features are forest cover, ruggedness,
distance to settlements, human density, coordinates, year and protection status. The design is causal: "we assess
the effectiveness of Finland's PA network in supporting abundances of four large carnivore species" (Introduction),
measured as "the difference between densities in a unit located inside a PA and its matched control unit" (Methods),
after "one-to-one, nearest-neighbor covariate matching with replacement", so controls repeat. Files of 2.2-2.3 MB;
not downloaded (Dryad blocks automated downloads).

Zero mechanism, from the paper only: no fresh tracks in the 24-hour window; the paper notes "zero inflation of all
time-series" (Methods). Workbook pushback: the 1,220 are matched units, not rows (the paper counts 3,111 unit-years
for 563 pairs), and a treatment-effect design is not a prediction task. A carnivore-track task would need the full
FWTS series rather than this matched subset. Licence: CC0.

## Reference

Terraube J., Van doninck J., Helle P., Cabeza M. (2020). Assessing the effectiveness of a national protected area
network for carnivore conservation. Nature Communications 11. doi:10.1038/s41467-020-16792-7. Data:
doi:10.5061/dryad.s1rn8pk4w.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 60 (Finnish large-carnivore FWTS).
