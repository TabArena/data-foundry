---
unique_name: new_brunswick_depth_to_bedrock
name: New Brunswick depth-to-bedrock (Pennell et al. 2026; provincial borehole, well, drillhole and outcrop points)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
- Available on Request
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
year: '2025'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1016/j.geoderma.2025.117651
- https://doi.org/10.3390/rs13214210
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: depth to bedrock at a point from LiDAR terrain and
geology covariates, with outcrops as true zeros, is a real mapping task, but no table is deposited and a rebuild from
the provincial databases is heavy.
- Source: Pennell, Comeau, Zhang, Feng and Heung (2026), Geoderma 465:117651 (gold open access, CC BY-NC-ND 4.0,
  online 8 December 2025 per Crossref; not read: ScienceDirect returned 403 and the Elsevier API only metadata). Its
  predecessor Furze et al. (2021), Remote Sensing 13:4210 (read): DTB from "publicly available soil profiles, boreholes,
  drill holes, well logs, and outcrop transects (n = 203,238)" (abstract); Sec. 2.5.3: "The result was 398 covariates
  for 176,658 DTB observations"; Table 2: outcrops 126,849 (77%), all from NBERD transects. Its Data Availability
  Statement: "The data used for this study can be downloaded from the following sources" (LiDAR, drillholes,
  boreholes, pedons, site cards, well logs on GeoNB and provincial portals); the outcrop transects are not in the list.
- Target and zeros: DTB in m; an outcrop is an observed 0. Furze Sec. 2.2: outcrops are "on-ground transects conducted
  throughout the province to locate areas in which bedrock was exposed at the surface", while positive depths come
  from drilling and wells, so zero against positive also tracks the programme that measured the point.
- Use case: Furze Sec. 1: DTB serves "water supplies, mineral exploration, road building, and forest management"; for
  example a provincial forestry or road planner reading depth at a site without a borehole. No actor named; fit
  approximate (a point stands for a 10 m map cell). Regime grouped (spatial blocks), since a map serves places without
  a measurement (SPLIT-4); Furze "split 70:30 for model development and validation" (abstract), not by area (a claim,
  SPLIT-5).
- Siblings and duplicates: `sweden_depth_to_bedrock` (the same task in another country, not a duplicate); soil-mapping
  precedents `lucas_topsoil` (TBD -> Yes) and `wosis_soil_profiles` (TBD -> 2nd Tier), both AI drafts. External
  collections: none found.
- Papers and pages: Pennell et al. 2026 (not read); Furze et al. 2021 (read).
- Metric: the 2026 paper not read; Furze reports R², MAE and RMSE side by side (abstract), so the fallback `rmse`
  (MET-5) unless the 2026 paper ranks by one.
- Risks for /add-dataset: the 2026 paper's data statement is unread (ask the curator for the PDF, PROV-17); a rebuild
  joins GeoNB point databases with 10 m LiDAR rasters; maybe a label-derived feature: Furze computes distances "to the
  rock outcrop locations" (Sec. 2.5.1; covariate `Out_Dist`), which are 0 on every outcrop if those locations are the
  zero-labelled points (LEAK); PCA over all covariates (LEAK-30, weak); Furze dropped the well logs "due to
  inconsistencies" (Sec. 2.3). Open policy question: whether mapping a field property from covariates counts as a
  prediction task (the family's species-abundance mapping question, by analogy).
- Markers: `Not Available (from Paper))` dropped: the observations are public at their sources (Furze's statement) and
  a table on request is no reason for a marker (EV-4); `Needs extensive data wrangling` stays.
- Priority: gap 0, use case 0 (applications named, no actor), source + (provincial databases documented by two papers),
  shape + (about 177k points, hundreds of covariates, spatial), risk - (no table, heavy rebuild, a possible
  label-derived covariate).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 2, as screened (verified on the zero-inflated screening review
page).

CC (2026-10-30, Andrej): "Rebuild is heavy": why it stays 2nd Tier while `sweden_depth_to_bedrock` goes to `Yes`.

Depth-to-bedrock (DTB) mapping for New Brunswick with explicit zeros at bedrock outcrops (Pennell, Comeau, Zhang,
Feng and Heung, Geoderma 465:117651, online December 2025). Its points come from public provincial databases
(NBERD boreholes, drillholes and outcrop transects; NBELG well logs via GeoNB; pedons; till site cards), the same
sources as the predecessor compilation of Furze et al. (2021), whose PDF was read: "The result was 398 covariates for
176,658 DTB observations" (Sec. 2.5.3), multi-scale LiDAR terrain derivatives plus bedrock and surficial geology,
for a provincial DTB map with a 70:30 split. One row is an observation point; a spatial (grouped) split fits the
mapping use case, as for `lucas_topsoil` and `wosis_soil_profiles`.

Zero mechanism, from the 2021 paper only: structural, an outcrop has depth 0. In Furze Table 2 outcrops are 126,849
points (77%), all from one programme (NBERD transects), while positive depths come from wells and drillholes, so
zero against positive also tracks the data source and its sampling geography; a model can learn the programme rather
than the soil. The analytical table is not deposited; the workbook says it is "available on request", and the 2026
paper's text (and its data availability statement) could not be read (ScienceDirect 403). Workbook pushback: it calls
the same table both "public" and "available on request". To check: the PDF's data statement (Google the title plus
"pdf"); whether to request the table or rebuild it from GeoNB and the provincial LiDAR. Licence: article CC BY-NC-ND
4.0; the provincial sources are public.

## Reference

Pennell T., Comeau L.-P., Zhang J., Feng C., Heung B. (2026). The importance of zeros in digital soil mapping II: A
case study of depth-to-bedrock mapping in New Brunswick, Canada. Geoderma 465:117651.
doi:10.1016/j.geoderma.2025.117651. Predecessor compilation: Furze S. et al. (2021), Remote Sensing 13:4210,
doi:10.3390/rs13214210.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 1 (New Brunswick depth-to-bedrock).
