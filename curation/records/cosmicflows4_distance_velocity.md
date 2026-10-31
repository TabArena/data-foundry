---
unique_name: cosmicflows4_distance_velocity
name: 'Cosmicflows-4: distances and velocities of 55,877 galaxies'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Website
domain: physics & astronomy
problem_type: Regression
source_links:
- https://doi.org/10.3847/1538-4357/ac94d8
- https://arxiv.org/abs/2209.11238
- https://edd.ifa.hawaii.edu/
- https://doi.org/10.3847/1538-3881/ab620e
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: Cosmicflows-4, measured distances of 55,877 galaxies in 38,065 groups with their velocities and sky positions; the record's framing (velocity from distance) fits no decision, since a velocity is measured far more exactly than a distance, but the reverse (distance from velocity and position, what the EDD distance-velocity calculators give) is a task astronomers use; few features and a noisy target.
- Source: Tully, Kourkchi, Courtois, Anand, Blakeslee et al., "Cosmicflows-4", ApJ 944:94, 2023 (doi 10.3847/1538-4357/ac94d8; arXiv 2209.11238, read 2026-10-31): "distances are compiled for 55,877 galaxies gathered into 38,065 groups. Eight methodologies are employed" (Abstract). As published (Appendix; the data are in the Extragalactic Distance Database, edd.ifa.hawaii.edu): Table 2, "All CF4 Individual Distances", one row per galaxy with PGC, 1PGC (the group), T17 (the Tempel group), Vcmb, DM ("derived from an MCMC analysis incorporating all methodologies"), the DM of each methodology with its uncertainty (SN Ia, TF, FP, SBF, SN II, TRGB, CPLR, MASER) and celestial, galactic and supergalactic coordinates; Table 3, group distances; Table 4, group velocities, distances, peculiar velocities and Hubble parameters.
- Use case: an astronomer who has only a galaxy's redshift and position (the host of a transient, say) needs its distance; the EDD tools "provide relationships between the distances and velocities of galaxies based on smoothed versions of the velocity fields derived by the Cosmicflows program" (Kourkchi et al., "Cosmicflows-3: Two Distance-Velocity Calculators", AJ 159:67, 2020, doi 10.3847/1538-3881/ab620e, Abstract); fit approximate: the calculators model the flow field, and the CF4 paper serves cosmology ("Peculiar velocities can be inferred from the measured distances", Abstract). The record's stated direction fits no decision (USE-2), so the task would be re-targeted. Regime grouped by group (1PGC): members of a group share a distance.
- Siblings and duplicates: `first_principles_hubble` (`No`, `AHDS`; 32 points), the record this was found for; `cosmicflows4_tully_fisher` (`TBD -> 2nd Tier`, priority 3, `No Good Target (yet)`): the 9,792 TF galaxies of CF4, so the two are cuts of one programme (PROV-6) and at most one CF4 record enters, with one target; `first_principles_tully_fisher` (`No`). External collections: none among the records; the web was not searched (budget used up).
- Better data: found as better data for `first_principles_hubble` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: Tully et al. 2023 (Sections 12-13, Appendix); Kourkchi et al. 2020 (the calculators); Kourkchi et al. 2020, ApJ 902:145 (the CF4 TF catalogue, see `cosmicflows4_tully_fisher`).
- Metric: none found (the paper fits H0 and propagates distance-modulus uncertainties; no prediction is scored), so the fallback `rmse` on the distance modulus (MET-1, MET-8); the per-galaxy uncertainties could weight a score, but the source defines none and we do not invent one; inputs: the group id for the split.
- Risks for /add-dataset: the features are only the velocity and the sky position (about three informative columns); the per-method DM columns and the DM uncertainties measure the target and must go (LEAK-10); the Hubble law alone (DM from Vcmb) may match the models, a TP-4 check against that one-feature rule, the gain beyond it being the noisy peculiar-velocity field (distance errors of about 20% for TF, per the run's Assessment); group members share a distance (LEAK-17; group on 1PGC); EDD is script-driven, so the download path is to be found.
- Priority: gap + (physics & astronomy has no accepted dataset), use case 0 (approximate; the source's own use is cosmology), source + (ApJ paper, EDD), shape 0 (55,877 galaxies but about three informative features), risk − (likely close to the Hubble-law rule; one CF4 record only).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `first_principles_hubble`.
- as published: 55,877 galaxies in 38,065 groups, with distances from eight methods (Tully-Fisher, Fundamental Plane, SN Ia, SBF, SN II, Cepheids, TRGB, maser) and observed velocities (abstract). Columns and row ...; target: recession velocity (km/s) from distance, as in the record; the direction with a user is the reverse: distance modulus from velocity and sky position; access: open.
- Why: The real Hubble diagram: the same two quantities as the record, measured for tens of thousands of galaxies instead of 32 points; distances and velocities are measured independently, so the relation is not deterministic (peculiar velocities and distance errors of about 20% for TF)
- Adds: 55,877 galaxies against 32. Caveats: thin use case (curator to judge; screening may reject it as 'no use case' or Scientific Discovery); overlaps the recorded cosmicflows4_tully_fisher (its 9,792 TF galaxies are part of CF4), so one CF4 record with one target may be the rule
