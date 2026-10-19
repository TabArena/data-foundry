---
unique_name: wildlife_insights_camera_trap_detections
name: Wildlife Insights camera traps (public project downloads)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
- No Good Target (yet)
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
