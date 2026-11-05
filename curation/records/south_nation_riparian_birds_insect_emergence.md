---
unique_name: south_nation_riparian_birds_insect_emergence
name: Riparian bird communities / aquatic insect emergence, South Nation River agro-ecosystems
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
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.sbcc2frfk
- https://doi.org/10.5281/zenodo.11186734
- https://doi.org/10.3389/fsufs.2024.1484377
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Too Small`, TP-5; `No Good Target / Scientific Discovery`, SEL-3): 24 sites,
each visited once for birds, so any task has about five test units per fold; the study links bird communities to
aquatic insect emergence and predicts nothing.
- Source: Rideout et al., Dryad doi:10.5061/dryad.sbcc2frfk (2025-01-28, CC0; Zenodo companion record 11186734);
  paper Rideout et al. 2025, Frontiers in Sustainable Food Systems 8:1484377 (read on frontiersin.org). As published
  (README and file list from Dryad's metadata, 2026-10-27; not downloaded, Dryad refuses automated downloads):
  `sites_full.csv` (29 sites), `environment.csv` (land use, hedges, water chemistry), `emergence.csv`,
  `emergence_seasonality.csv`, `sites_bird.csv` (24 sites), `benthic.csv` (genus presence/absence), `bird.csv`
  ("Riparian avian community abundance matrix") and `benthic_classifications.csv`.
- Size (TP-5): biotic sampling "was completed at a subset of 24 sites" (Sec. 2.4); "All three point counts were
  combined for each site, resulting in an abundance matrix of total species per site" (Sec. 2.4); "for logistical
  reasons we were unable to visit sites for point counts more than one time" (Sec. 4.2). One row per site, 24 in all,
  about five per test fold, whatever the target.
- Use case: none stated. README: "*Objective:* Examine the secondary productivity of emerging aquatic insects as an
  ecosystem service and determine the linkage between aquatic insect emergence and riparian avian communities in an
  agro-ecosystem in eastern Ontario, Canada". The analyses model the proportion of insectivorous birds (binomial GLMM)
  and species richness (Sec. 2.5.3) and compare communities by NMDS and PERMANOVA (Sec. 2.5.4); the zero-inflated
  abundance target is the workbook's reading, and the paper fits no such model. The site covariates in
  `environment.csv` set it apart from a table without features, so SEL-3 is the second ground, not the first (cf.
  `qtp_urban_wasteland_plant_diversity`, `TBD -> 2nd Tier` with 38 wastelands, this run).
- Siblings and duplicates: none (grep riparian, insect emergence, South Nation). External collections: none.
- Metric: none (no task).
- Reject check (AI, 2026-10-27): stands, re-grounded on TP-5 (Must). 24 sites with one bird visit each (Rideout et
  al. 2025, Sec. 2.4 and 4.2, https://www.frontiersin.org/journals/sustainable-food-systems/articles/10.3389/fsufs.2024.1484377/full)
  give about five test units per fold in any framing.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

CC (2026-10-30, Andrej): the reason for the `No`: "No good target".

Bird point counts, aquatic insect emergence, benthic samples and environment at agricultural streams in eastern
Ontario (Rideout et al. 2025; paper read on frontiersin.org). Sec. 2.4: "Biotic sampling ... was completed at a
subset of 24 sites", and "All three point counts were combined for each site"; Sec. 4.2: "we were unable to visit
sites for point counts more than one time". So `bird.csv` is a 24-site by 50-species matrix (5 KB; not downloaded,
Dryad blocks automated downloads). The analyses (Sec. 2.5.3) regress "the proportion of insectivorous birds (binomial
GLMM) or bird species richness" and run NMDS/PERMANOVA; nothing is predicted.

Zero mechanism, from the paper only: a species not detected in one site's single 15-minute survey. Workbook
pushback: the paper fits no zero-inflated model, so "zero-inflated abundance" is the workbook's reading. Licence:
CC0.

## Reference

Rideout N.K., Alavi N., Lapen D.R., et al. (2025). Quality versus quantity: response of riparian bird communities to
aquatic insect emergence in agro-ecosystems. Frontiers in Sustainable Food Systems 8:1484377.
doi:10.3389/fsufs.2024.1484377. Data: doi:10.5061/dryad.sbcc2frfk.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 41 (Riparian bird communities / aquatic insect
emergence).
