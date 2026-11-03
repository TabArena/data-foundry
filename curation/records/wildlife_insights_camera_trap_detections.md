---
unique_name: wildlife_insights_camera_trap_detections
name: Wildlife Insights camera traps (public project downloads)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- Two-Regime Zeros
original_source: Website
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.wildlifeinsights.org/
- https://www.wildlifeinsights.org/node/3079
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a platform that hosts many camera-trap projects, not one
dataset; its public download is tabular (deployments and per-image identifications) with no target and no habitat
covariates, so a task would have to be built from one chosen project.
- Source: Wildlife Insights (Conservation International, Google and partners), "providing machine learning models and
  other tools to manage, analyze and share camera trap data" (home page); platform paper Ahumada et al., Environmental
  Conservation 47 (2020), doi:10.1017/S0376892919000298 (not read). Public download
  (https://www.wildlifeinsights.org/node/3079): `projects.csv`, `cameras.csv`, `deployments.csv` ("start date, end date,
  coordinates and other camera settings") and `images.csv` or `sequences.csv` (species identifications with date and
  time), a data dictionary; "You may view the image, but it is not available for download"; embargoed deployments and
  sensitive-species locations removed; licences per project; an account and intended-use questions are needed.
- Use case: the platform's "With access to reliable data, everyone can make better decisions to help wildlife thrive"
  names no actor, moment or decision. For example detections per deployment and occasion, predicted from habitat layers
  joined by coordinates; the source defines no such task. Fit none so far. Regime not set (by project or deployment).
- Modality: the identifications come from images (the platform's models and its users), but the download holds no
  images, so a count table built from it is tabular; the earlier `Image` marker fits the platform's own identification
  task, not such a table, and is dropped.
- Doubt: the earlier pass set `No`. No Must fails in the source's words: there is no task yet (`No Good Target (yet)`,
  which mostly waits as 2nd Tier, selection.md), and one project with a published site-level analysis would get its own
  record.
- Siblings and duplicates: `iwildcam_2020_camera_trap_species` (WCS images, an image task),
  `southeast_asia_predator_prey_camera_trap_counts`, `freiburg_urban_mammal_camera_trap_events`; no duplicate. External
  collections: none found.
- Metric: none (no task).
- Risks for /add-dataset: the whole task is ours (target, unit, effort per occasion, covariates from outside sources);
  joins of identifications, deployments and projects (`Needs extensive data wrangling` added); per-project licences
  (CC0, CC BY, CC BY-NC) are no criterion (EV-4).
- Priority: gap 0, use case 0, source + (the platform's data dictionary and download guide), shape 0 (no table yet),
  risk - (target and covariates to build, heavy joins).

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page).
No reason was given on the page; the record's markers (`No Good Target (yet)`, `Needs extensive data wrangling`) stand
as the reason.

Wildlife Insights is a platform that aggregates camera-trap projects, not one dataset. A public download (account
plus intended-use questions) holds projects, cameras, deployments and per-image or per-sequence identifications
(species, number of individuals, bounding boxes, timestamp, deployment) with a data dictionary; licences are set per
project (CC0, CC BY or CC BY-NC). Images are not included, embargoed deployments and sensitive-species locations are
removed, and deployments carry only dates, coordinates and camera settings: there is no site-level count table and no
habitat covariate. Any count target with features would have to be built by us, and no source defines such a task.
Not downloaded.

Zero mechanism, not confirmed: a zero would be non-detection at a camera over an occasion, once constructed with
effort. Workbook pushback: "Huge" and "No detection -> 0" describe the platform, not a release. If someone proposes
one specific project with a published site-level analysis, that project should be triaged on its own.

## Reference

Wildlife Insights platform, https://www.wildlifeinsights.org/ (public-download documentation:
https://www.wildlifeinsights.org/node/3079). No dataset paper.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 22 (Wildlife Insights camera traps).
