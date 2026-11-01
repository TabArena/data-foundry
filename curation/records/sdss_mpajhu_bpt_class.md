---
unique_name: sdss_mpajhu_bpt_class
name: 'SDSS MPA-JHU galaxies: BPT emission-line class'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Class-dependent Recording
tags:
- AI-Filled (Verify)
original_source: Other
domain: physics & astronomy
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.sdss4.org/dr17/spectro/galaxy_mpajhu/
- https://arxiv.org/abs/2607.09865
- https://wwwmpa.mpa-garching.mpg.de/SDSS/DR7/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the MPA-JHU spectroscopic catalog of SDSS galaxies (about 1.47 million spectra with a BPT emission-line class), where the task is the class without the red lines that define it, as a survey without Hα and [NII] would need; the catalog records metallicity and SFR differently by class, which a model can read, so those columns go.
- Source: the MPA-JHU (Max Planck Institute for Astrophysics and Johns Hopkins University) galSpec catalog, built with the methods of Kauffmann et al. 2003, Brinchmann et al. 2004 and Tremonti et al. 2004; public since SDSS DR4, a DR7 release at wwwmpa.mpa-garching.mpg.de/SDSS/DR7, and in the SDSS data releases since DR8 (sdss4.org/dr17/spectro/galaxy_mpajhu, read 2026-10-31): files galSpecInfo, galSpecLine, galSpecIndx and galSpecExtra, "line-by-line matched with the specObj file", computed for the spectra of run2d=26 (the DR7 plates). BPT classes: Star Forming, Composite, AGN, Low S/N Star Forming, Low S/N AGN and Unclassifiable. The page calls the catalog "deprecated in favor of the Wisconsin, Portsmouth, and Granada team analyses". Size: 1,843,200 rows, 1,472,581 with a class, per the run's note (not counted here).
- Use case: the candidate paper's: Gui, "Six-Class BPT Galaxy Classification for Survey-Scale AGN Candidate Prioritization: Deep Tabular Model and Informative Missingness Signals", arXiv 2607.09865 (July 2026; abstract only): a survey team ranks galaxies as AGN candidates for follow-up when the high-S/N lines of the BPT diagram are not measured, from 27 features of "raw survey measurements, derived quantities, and missingness indicators". Fit approximate: low-redshift SDSS galaxies stand in for the surveys that lack the red lines. SEL-5: the class is a published rule on line ratios and S/N, so its inputs (Hα, Hβ, [OIII], [NII] and their S/N) are dropped, and the rest still makes a task. Regime IID over galaxies, with repeat spectra of one object to group.
- Siblings and duplicates: `sdss_17` (`Yes`, `Selection Bias`: photometric star, galaxy or quasar), `desi_dr1_star_galaxy_quasar` and `happy_teddy_sdss_photo_z` (candidates, `TBD -> Yes`, 3) are other tasks on survey data (PROV-7); no other emission-line record (grep: MPA-JHU, BPT, emission-line). External collections: none found.
- Better data: from the curator's Zotero collection (item 225, the arXiv paper); no further search this round.
- Papers and pages: the SDSS galSpec page; the MPA DR7 page (not read); the arXiv abstract.
- Metric: the abstract reports hard-classification metrics led by accuracy (0.8266 for the best model), precision-recall curves, top-k retrieval and a ROC AUC for star-forming against AGN, side by side, so no single deliberate one: the fallback `log_loss` (MET-5, MET-6, MET-11); inputs none.
- Risks for /add-dataset: `Class-dependent Recording`: the SDSS page says metallicity is computed only for "Star Forming" objects, and that for "AGN and weak-line galaxies, SFRs are estimated from the photometry", so metallicity, its missing flag (the paper's top feature, `OH_P50N_missing`) and the SFR give the class away and go, or are rebuilt one way for all rows (LEAK-13 to LEAK-15); the low-S/N classes depend on the S/N of the dropped lines, which the errors of the kept lines may carry (check); the unclassifiable class (keep or drop, TP-8); SDSS's spectroscopic target selection (`Selection Bias` as in `sdss_17`, to weigh); three tables to join by spectrum.
- Priority: gap + (physics & astronomy has no accepted dataset; multiclass is thin), use case 0 (approximate: SDSS stands in for the target surveys), source + (MPA-JHU catalog with its method papers, SDSS documentation), shape + (about 1.47 million classified spectra), risk - (class-dependent metallicity and SFR; a label set by a rule on dropped columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 225: "Six-Class BPT Galaxy Classification for Survey-Scale AGN Candidate Prioritization: Deep ...".
- as published: one row per galaxy spectrum: 1,843,200 rows; 1,472,581 with a BPT class. The paper uses 8 columns (redshift, stellar mass, SFR, gas metallicity, [NeIII] 3869 and [OII] 3727 fluxes and errors); the ...; target: BPT class: star-forming, low-S/N star-forming, composite, AGN, low-S/N LINER, unclassified (6 classes; AGN 1.8%); access: open.
- Why: Large, real, well documented public catalog with a standard label and a defined deployment gap (the red lines are missing)
- Adds: Emission-line galaxy classification at million-row scale, unlike sdss_17 (photometric star/galaxy/QSO from DR17). Caveats: leakage risk. The catalog computes gas metallicity mainly for star-forming galaxies, and the paper's top feature is the missing flag on metallicity. The SFR method also differs by class. Features ...
