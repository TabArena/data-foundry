---
unique_name: boreal_postfire_lichen_biomass
name: Terrestrial lichen - Northwest Territories / Terrestrial lichen - Saskatchewan (post-fire forage-lichen biomass, Greuel et al. 2021)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
original_source: Other
year: '2021'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.t1g1jwt15
- https://doi.org/10.5061/dryad.tb2rbnzzj
- https://doi.org/10.1002/ecs2.3481
- https://doi.org/10.5061/dryad.76hdr7sth
v2_path: datasets/_dev/tabarena-v0pt2/boreal_postfire_lichen_biomass/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a regional post-fire survey of caribou forage lichen
(567 plots in the Northwest Territories and Saskatchewan) with stand age, stand type and ecoprovince as covariates, not
a designed experiment, so the family's open species-abundance question decides it rather than a fast reject; the
biomass target is an allometric estimate from cover and height.
- Source: Greuel et al. 2021 (Ecosphere 12:e03481), two Dryad deposits, CC0: Northwest Territories
  (doi:10.5061/dryad.t1g1jwt15, first version 2021-02-03, now version 5 of 2026-05-18; site info, destructive biomass
  samples, lichen data and quadrat cover sheets) and Saskatchewan (doi:10.5061/dryad.tb2rbnzzj, 2021-02-18; lichen data
  and destructive biomass sheets). Dryad methods: "346 plots were established with 5, 1 by 1 m quadrats within
  predetermined burn age classes" (NWT) and "221 plots were established with 2, 2 by 2 m quadrats within three age
  categories" (SK). About 1,730 and 440 quadrat rows (earlier AI triage, 2026-10-19, an estimate); not downloaded
  (Dryad answers 401 to file requests).
- Use case: the authors "used estimates of lichen biomass to quantify patterns of lichen recovery in different stand
  types, ecoprovinces, and with time following stand-replacing fire", and the results "provide a basis for estimating
  future caribou habitat" (Dryad abstract); for example a caribou range planner estimating forage lichen in a stand of
  known fire age and type. No actor or decision is named, so the fit is approximate at best. Regime grouped by plot or
  site, since quadrats nest in plots (SPLIT-3); the two regions differ in protocol (quadrat size, age classes).
- Siblings and duplicates: `athabasca_forage_lichen_cover` is another study (Alberta, data not released); no duplicate
  among the records. No ecological record of the family had a curator's verdict yet; the triage of 2026-10-19 named
  `wadden_sea_sibes_macoma_abundance`, `great_lakes_marsh_bird_point_counts` and
  `nantucket_sound_sea_duck_aerial_survey_counts` as the cases to settle the question on (since settled by Andrej on
  2026-10-30, policy question 1 of the zero-inflated review: no new rule, each survey judged on its own use case).
  External collections: none found.
- Papers and pages: Greuel et al. 2021 (text not read: Wiley 403; claims from the Dryad abstract and methods, the
  authors' text); the companion deposit doi:10.5061/dryad.76hdr7sth (Baltzer et al.) describes the mature stands.
- Metric: none found (the Dryad abstract reports a hurdle GLM judged by significance and a logistic growth model; the
  paper's text was not reachable), so the fallback `rmse`.
- Risks for /add-dataset: the target. Biomass comes from "allometric equations to estimate lichen biomass from field
  measurements of lichen cover and height" (Dryad abstract), so cover and height are the label's inputs and go
  (SEL-5); measured lichen cover is the alternative target. The two protocols need one target definition, the sheets
  need joining, and what the site sheet holds beyond stand age, type and ecoprovince is unseen. The question of
  species-abundance mapping from habitat covariates is settled (Andrej, 2026-10-30, policy question 1 of the
  zero-inflated review: no new rule, each survey judged on its own use case); `No Good Target / Scientific Discovery`
  stays as the marker of that concern.
- Priority: gap 0 (biology, regression and grouped are not thin), use case 0 (none named), source + (a paper and two
  documented deposits), shape 0 (about 567 plots, few covariates), risk - (allometric target, two protocols).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening
review page).

Workbook rows 37 and 38 are one study (Greuel et al. 2021, one paper, overlapping authors) released as two regional
Dryad deposits with different field protocols, so they share this record. Northwest Territories: "346 plots were
established with 5, 1 by 1 m quadrats within predetermined burn age classes (37-38 and 46-49 years post-fire) and ...
'control' (>70 years)". Saskatchewan: "221 plots were established with 2, 2 by 2 m quadrats within three age
categories". About 1,730 and 440 quadrat rows by estimate; not downloaded (Dryad blocks automated downloads).

The study is a fire-recovery chronosequence: the abstract's hurdle GLM "identified stand age, stand type and
ecoprovince as significant predictors of lichen presence", inference on three design variables with no remote-sensing
covariates, mapping or validation mentioned. Biomass is itself estimated: "allometric equations to estimate lichen
biomass from field measurements of lichen cover and height", so cover and height would be the target's own inputs.
Zero mechanism, from the abstract only: no forage lichen in the quadrat, hence allometric biomass 0. Workbook
pushback: "Verified strict match" and "Core: Yes" rest on the hurdle model, which is inference, not a prediction task.
Paper text not read (Wiley 403). Licence: CC0.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/boreal_postfire_lichen_biomass/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping as changed: the caribou range-plan biologist named as the actor, the NT plots grouped by burn area and the SK plots per plot (216 groups), three NT plots' coordinates repaired from the site sheet. Superseding the screening's guesses above: 516 plots and 2,010 quadrats; fetched from Dryad's version zips without a token (the 2022 revision of the NT sheet), not "Dryad answers 401". The marker `No Good Target / Scientific Discovery` stays until your mark on issue 1. Priority 3: gap 0, use case 0 (fit approximate), source + (CC0 deposits and a paper), shape +, risk 0.

CC (2026-11-03, Andrej): the two duplicate-row warnings are accepted as worded (issue 3 (A) in boreal_postfire_lichen_biomass).

CC (2026-11-03, Andrej): read Greuel et al. (2021) through Wiley's HTML page (issue 4): stand age by tree-ring dating, a pooled volume allometry with no significant variation across ecoprovinces, Saskatchewan's total heights adjusted by a live-to-total ratio of 0.76, an observed-versus-fitted R2 of 0.18 without held-out evaluation, no explanation of the missing plots: "We can now replace the blanket warning with specific references for confirmed claims."

**Assessment (AI, 2026-11-03):** the paper is read from the publisher's PDF (Wayback Machine copy of 2021-07-16); the notes now cite it by section, and the claim that the two regions convert cover differently is removed (one pooled allometry; 12.633 is its volume slope in kg/ha). Its stated aim is the task itself: "accurately predicting the availability of lichen forage under current and future fire regimes".

CC (2026-11-03, Andrej): ship after the changes (verdict). Issue 1 (A): the paper's own forecast with the range-plan actor and the burn-area split; the `No Good Target / Scientific Discovery` marker is removed, as the paper's predictive aim answers it. Issue 2 (A): the tree-ring stand age stays. Issue 5 (A): kg/ha, decided for this task alone ("I go with your recommendation"). Issue 6 (A): RMSE on kg/ha ("We can keep RMSE in this case").

CC (2026-11-03, Andrej): ship (verdict); the metric, RMSE on kg/ha, checked.

## Reference

Greuel R.J., Degre-Timmons G.E., Baltzer J.L., Johnstone J.F., et al. (2021). Predicting patterns of terrestrial
lichen biomass recovery following boreal wildfires. Ecosphere 12:e03481. doi:10.1002/ecs2.3481. Data:
doi:10.5061/dryad.t1g1jwt15 (Northwest Territories), doi:10.5061/dryad.tb2rbnzzj (Saskatchewan).

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master rows 37 (Terrestrial lichen - Northwest
Territories) and 38 (Terrestrial lichen - Saskatchewan).
