---
unique_name: opengeoai_2023_hack
name: opengeoai-2023-hack
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Image
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/opengeoai-2023-hack/data
- https://zindi.africa/competitions/opengeoai-2023-hack
source_row: 954
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: olive-parcel classification from Sentinel-2 image time series in a 24-hour student hackathon; the inputs are satellite imagery, which SEL-13 counts as image-derived, but a curator kept a sibling Sentinel-2 cropland task at `TBD -> Yes`.
- Source: Zindi hackathon "OpenGeoAI 2023 Hack", 11-12 November 2023, open to Tunisian participants, by AGEOS (a Tunisian geospatial association) and the IEEE Sup'Com GRSS chapter, within the EU-funded Innovi project. Subtitle: "Using Sentinel-2 image time series, can you map Olive crops at parcel level in Central Tunisia?". Data description: "classify and map olive parcels using open Sentinel-2 multispectral time series data. Please find the images for the challenge here." Files: train.rar (143 KB), test.rar (74 KB), a starter notebook (1.7 MB); the imagery is linked elsewhere. The old `Missing source information` marker is refuted: the host and the page are known.
- Use case: Tunisian agricultural planners map olive parcels; fit approximate (a 24-hour hackathon task). Regime: spatially grouped by parcel or area if the rows are pixels; not settled.
- Siblings and duplicates: `geoai_challenge_for_cropland_mapping_in_dry_environments` (Andrej `TBD -> Yes`, Sentinel time series), `crop_type_classification_challenge` (AI `TBD -> 2nd Tier`, `Wrong Domain / Source Modality`). External collections: none.
- Papers and pages: the Zindi page and the starter notebook only; discussions private.
- Metric: "The error metric for this competition is Accuracy" (Zindi Evaluation page; API `straight_accuracy`), a competition's metric (MET-4).
- Risks for /add-dataset: the features are remote-sensing spectra of an image (SEL-13, `Image`) unless the starter notebook ships per-parcel band statistics that tabular models are used on; the label files are tiny (likely a few hundred parcels, a `Too Small` risk, TP-5); access was restricted to Tunisian participants (a question for the curator).
- Priority: gap 0, use case 0, source 0 (a hackathon page), shape 0 (tiny label files, size unknown), risk - (image modality). Markers: `Image` added as the provisional flag; `Missing source information` and `TBD` dropped. Consistency question for the curator: if `Image` holds here (SEL-13), does it hold for the Andrej-kept cropland sibling too?

A 2023 Zindi 'OpenGeoAI' hackathon with no description in the record. The 'GeoAI' framing strongly suggests geospatial and likely satellite-imagery or raster inputs, which would put it outside representative tabular ML, but this is not certain from the record. Too little info to reject outright. Suggest TBD -> 2nd Tier; a human must open the competition data page to confirm whether inputs are tabular features or raw imagery and identify the target.
