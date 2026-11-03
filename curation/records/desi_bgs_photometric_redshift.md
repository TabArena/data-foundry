---
unique_name: desi_bgs_photometric_redshift
name: 'DESI PROVABGS catalogue: Bright Galaxy Survey galaxies with spectroscopic redshift and Legacy Surveys photometry'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Website
domain: physics & astronomy
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.desi.lbl.gov/doc/releases/edr/vac/provabgs/
- '# the PROVABGS mock challenge on synthetic spectra (methods paper), not the source of the rows'
- https://arxiv.org/abs/2202.01809
- https://huggingface.co/datasets/MultimodalUniverse/desi_provabgs
- https://arxiv.org/abs/2606.07771
- https://data.desi.lbl.gov/public/edr/vac/edr/provabgs/v1.0/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: photometric redshift of DESI One-Percent Survey bright galaxies from four Legacy Surveys magnitudes, a real spectroscopic target; few inputs of one kind, an early cut of a survey whose DR1 catalogue (record `desi_dr1_star_galaxy_quasar`) holds millions of such galaxies, and the photo-z task is our framing of an SED-modelling catalogue.
- Source: DESI Early Data Release, value-added catalogue PROVABGS v1.0 (data.desi.lbl.gov/doc/releases/edr/vac/provabgs/, read 2026-10-31): "all BGS galaxies in the DESI One-Percent Survey (SV3)", with physical properties "inferred jointly from Legacy Surveys photometry and DESI spectroscopy" by Bayesian SED modelling; columns TARGETID, RA, DEC, HPIX_64, Z_HP (Redrock redshift) and ZERR, extinction-corrected g, r, z and W1 magnitudes, FIBMAG_R, SCHLEGEL_COLOR (for BGS Faint selection), best-fit and posterior SED parameters and stellar mass, weights for redshift failure and fibre assignment, TSNR2_BGS, BGS Bright and Faint flags; file `BGS_ANY_full.provabgs.sv3.v0.hdf5` at data.desi.lbl.gov/public/edr/vac/edr/provabgs/v1.0/; papers Hahn et al. 2023, ApJ (doi 10.3847/1538-4357/ac8983) and Kwon et al. 2023, ApJS (doi 10.3847/1538-4365/acba14). The page gives no galaxy count; the Hugging Face copy (MultimodalUniverse/desi_provabgs, MIT on its card) has 100,000 rows x 22 columns. arXiv 2202.01809 in the links is the PROVABGS mock challenge on synthetic L-GALAXIES spectra and photometry, not the source of these rows (PROV-10).
- Use case: an imaging survey's pipeline assigns a redshift from broadband photometry to galaxies without a spectrum (ours; the release defines no photo-z task); fit approximate: BGS galaxies were picked for a spectrum by magnitude cuts, so many targets of the use case lie fainter (`Selection Bias`, as on `sdss_17` and `happy_teddy_sdss_photo_z`); regime IID (as `sdss_17`), with HEALPix pixels (`HPIX_64`) as a candidate group.
- Siblings and duplicates: `happy_teddy_sdss_photo_z` (`TBD -> Yes`, priority 3: the same photo-z task on SDSS DR12 from a paper that built it as a photo-z benchmark; another survey, so no duplicate under PROV-4, though the curator may want one photo-z task); `desi_dr1_star_galaxy_quasar` (`TBD -> Yes`, priority 3: the DESI DR1 redshift catalogue with Legacy Surveys photometry, about 13M galaxies; the same survey's later and far larger release, from which the same regression can be cut: a version under PROV-6, the curator's call); `sdss_17` (`Yes`). External collections: Multimodal Universe (Hugging Face); the AION-1 uncertainty benchmark (Tame-Narvaez, Ćiprijanović, Trivedi, arXiv 2606.07771, 2026, the Zotero item: redshift, stellar mass, age, metallicity and sSFR from frozen AION-1 embeddings, scored by interval coverage).
- Better data: from the curator's Zotero collection (item 206); no further search this round (the larger DR1 catalogue is already a record, above).
- Papers and pages: the VAC page; Hahn et al. 2023; Kwon et al. 2023; Tame-Narvaez et al. 2026.
- Metric: none found for a photo-z prediction in the release; the Zotero paper scores interval coverage on embeddings (another task); the field's normalised error (z_phot - z_spec)/(1 + z_spec) with its scatter and outlier rate would be custom (MET-13); so the fallback `rmse` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: five or six numeric inputs of one kind (four magnitudes, a fibre magnitude, one colour); every PROVABGS output (stellar mass, SED parameters, mass-weighted metallicity and age, SFR) and ZERR and TSNR2_BGS come from the spectrum: drop them as features (LEAK-10); the Hugging Face copy is a 100,000-row subset of unstated selection (build from the DESI file, PROV-8, PROV-15); the redshift-failure weights and Redrock quality flags for the target; the DR1 version question (PROV-6).
- Priority: gap + (physics & astronomy has no accepted dataset), use case 0 (ours), source + (DESI's documented release), shape 0 (100,000 rows, but five or six numeric inputs of one kind), risk - (an early cut while the survey's DR1 catalogue is a record; the photo-z task overlaps `happy_teddy_sdss_photo_z`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 206: "Beyond Point Estimates: Benchmarking Uncertainty Quantification Methods on the AION-1 ...".
- as published: galaxies of the DESI One-Percent Survey (SV3, 2021); the Hugging Face copy has 100,000 rows; columns: Z_HP, ZERR, extinction-corrected g/r/z/W1 magnitudes, r fibre magnitude, a selection colour, ...; target: spectroscopic redshift Z_HP predicted from photometry (photo-z regression); the SED-fit properties are model outputs and lean out; access: open.
- Why: real measured target from DESI spectra, a standard tabular regression where GBDT and kNN photo-z are used in practice; HEALPix gives a spatial grouped split
- Adds: an astronomy regression (sdss_17 is a classification only); risks: few features (4-5 magnitudes), magnitude-cut selection as in sdss_17, a larger DR1 version may exist (not checked)
