---
unique_name: south_nation_riparian_birds_insect_emergence
name: Riparian bird communities / aquatic insect emergence, South Nation River agro-ecosystems
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 41 (Riparian bird communities / aquatic insect
emergence).
