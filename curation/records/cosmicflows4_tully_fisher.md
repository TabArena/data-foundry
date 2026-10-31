---
unique_name: cosmicflows4_tully_fisher
name: 'Cosmicflows-4: The Catalog of ~10,000 Tully-Fisher Distances'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: physics & astronomy
source_links:
- https://doi.org/10.3847/1538-4357/abb66b
- https://arxiv.org/abs/2009.00733
- https://edd.ifa.hawaii.edu/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: a peer-reviewed catalogue of 9,792 spiral galaxies with HI line widths and seven-band photometry, in physics and astronomy, which has no accepted dataset. But the catalogue's distances are computed from these same columns, and no independently measured label that serves a decision has been found.
- Source: Kourkchi, Tully, Eftekharzadeh et al., "Cosmicflows-4: The Catalog of ~10,000 Tully-Fisher Distances", ApJ 902:145 (2020) (https://doi.org/10.3847/1538-4357/abb66b; arXiv 2009.00733, abstract read 2026-10-31). The data is served by the Extragalactic Distance Database (edd.ifa.hawaii.edu), a script-driven site whose catalogue columns were not read. As published (abstract): distances to 9,792 spirals within about 15,000 km/s, mostly ALFALFA HI detections, from the luminosity-rotation relation calibrated in SDSS u, g, r, i, z and WISE W1, W2, with colour as a secondary parameter. The catalogue includes kinematic, photometric and inclination data. A random forest estimates dust attenuation for spirals without infrared photometry. The paper derives H0 = 75.1 km/s/Mpc.
- Use case: none for a prediction. The catalogue measures distances to map peculiar velocities and H0. Predicting a galaxy's absolute magnitude needs its distance, which for most of these galaxies is the TF distance itself, and the galaxy's velocity comes from the same HI spectrum as the line width, so it is known at prediction time. Fit none as published. Regime IID over galaxies, or grouped by galaxy group or cluster.
- Siblings and duplicates: `first_principles_tully_fisher` (`No`, `Too Small`: 18 galaxies read off Tully & Fisher 1977, Fig. 5a). `cosmicflows4_distance_velocity` (a new record of this run) is the CF4 compilation of 55,877 galaxies, which contains these TF distances: a later, larger cut of the same programme (PROV-6), so at most one CF4 record enters. External collections: none found.
- Better data: found as better data for `first_principles_tully_fisher` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the ApJ paper. The calibration paper of the relation (Kourkchi et al. 2020) and the CF4 compilation (Tully et al. 2023) were not read.
- Metric: none found as a prediction metric (the paper fits the relation's slope, zero point and scatter in magnitudes), so the fallback `rmse` once a target is settled (MET-1, MET-8). Inputs none.
- Risks for /add-dataset: the catalogue's distance moduli and absolute magnitudes are computed from the shipped widths, inclinations and magnitudes, so as a target they are `Trivial` (SEL-5). An honest target would be a distance from another method (Cepheid, TRGB, SN Ia or cluster membership, which few galaxies have), or the attenuation the paper predicts with a random forest, a sub-task to examine. Inclination-corrected widths are derived columns (CLEAN).
- Priority: gap + (physics & astronomy, 0 accepted), use case 0 (none), source + (ApJ paper and EDD), shape + (9,792 galaxies with line widths, inclinations and seven bands), risk - (no independent target shown).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `first_principles_tully_fisher`.
- as published: 9,792 spiral galaxies within 15,000 km/s, mostly ALFALFA HI detections. As published (abstract): HI line widths, inclinations and photometry in SDSS u, g, r, i, z and WISE W1, W2, plus 'reduced ...; target: the galaxy's luminosity (absolute magnitude in a band), the quantity of the Tully-Fisher relation, or equivalently its distance modulus; access: open.
- Why: Same relation and quantity as Tully & Fisher 1977 (luminosity against HI rotation width), and Tully is a co-author of both. Here the line widths are measured for thousands of galaxies, where the record's 18 points were read off a figure
- Adds: 9,792 galaxies against 18, seven bands with colour terms (the paper's secondary parameters), and a 2020 calibration. Risk to settle before a record: the catalogue's own TF distance moduli are computed from these widths and magnitudes, so they are a deterministic target. An honest label needs a distance independent of ...
