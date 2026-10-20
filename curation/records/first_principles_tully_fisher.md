---
unique_name: first_principles_tully_fisher
name: first_principles_tully_fisher
suggestion: 'No'
decision_markers:
- Too Small
original_source: Other
year: '1977'
required_split:
- '?'
source_links:
- '# First publication: Tully and Fisher, A&A 54, 661-673 (1977); PMLB''s 18 rows were read off its Fig. 5(a)'
- https://ui.adsabs.harvard.edu/abs/1977A&A....54..661T
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/first_principles_tully_fisher/metadata.yaml
type_adapter_id: curation-record-v1
---

## Comments

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

18 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small

`first_principles_*` are artificial datasets generated from physical first-principles formulas (PMLB) — excluded as artificial/simulated.

CC (2026-10-20, Lennart): year 1977 and source Tully and Fisher (A&A 54, 661), not PMLB: PMLB's file was read off Fig. 5(a) of that paper (its metadata says so), so it is a copy (PROV-9). The data is real, the measured rotation widths and luminosities of 18 galaxies, so the note above on `first_principles_*` and the `AHDS` marker do not apply to it; the marker is now `Too Small`, the reason both curators gave. Still `No`: 18 rows, 6 per test fold (TP-5).
