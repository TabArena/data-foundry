---
unique_name: alerce_ztf_light_curve_classes
name: 'ALeRCE Light Curve Classifier: labeled set, features and classifications (ZTF)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.3847/1538-3881/abd5c1
- https://doi.org/10.5281/zenodo.4279623
- https://arxiv.org/abs/2008.03311
- https://arxiv.org/abs/2503.19698
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the labelled set and features of the ALeRCE light-curve classifier (ZTF alert stream, 15 classes, about 123,000 labelled sources, 152 features), a production multiclass task whose own model is a balanced random forest on these features; physics & astronomy has no accepted dataset.
- Source: Sánchez-Sáez et al., "Alert Classification for the ALeRCE Broker System: The Light Curve Classifier", The Astronomical Journal 161, 141 (2021; arXiv 2008.03311, August 2020); data on Zenodo 4279623, "The ALeRCE Light Curve Classifier: labeled set, features, and classifications" (2020-11-18, CC BY 4.0), one 1.12 GB tar.gz with three CSVs: the labelled set ("the labeled set described in Section 2.2 of the paper"), features_for_lc_classifier_20200609.csv ("the features computed for the unlabeled ZTF set (up to 2020/06/09)") and the classifier's outputs. Counts from the scout (paper Table 1, not re-read): 123,496 labelled sources (transient 1,718, stochastic 34,713, periodic 87,065) and 152 features (variability features of the ZTF g and r light curves, AllWISE and ZTF colours, galactic coordinates, alert metadata). Labels come from cross-matched catalogs (abstract: Catalina Surveys, Gaia DR2 variable stars, the Million Quasars catalog, among others).
- Use case: the ALeRCE broker classifies every ZTF source with at least six detections and updates the classes daily ("providing updated classifications for sources with new alerts every day", abstract), in preparation for the Rubin Observatory; astronomers then pick follow-up targets from the classes (the scout's reading); fit direct for the broker's classification; regime IID over sources (independent objects, catalog labels), a split by first detection to be checked.
- Siblings and duplicates: `first_principles_leavitt`, `first_principles_supernovae_zg` and `first_principles_supernovae_zr` (all `No`, `AHDS`) use ZTF light curves in other, non-tabular framings; `htru2_2` (TBD -> Yes) is the closest precedent for features extracted from a signal; `sdss_17` (Yes, `Selection Bias`) classifies objects from photometry; the run's other astronomy candidates (`desi_dr1_star_galaxy_quasar`, `sdss_mpajhu_bpt_class`, `happy_teddy_sdss_photo_z`) are other surveys and tasks (PROV-7). No other ALeRCE record (grep: alerce, zwicky). External collections: none found.
- Better data: found by the gap scout for physics & astronomy, next to `first_principles_leavitt` and the two supernovae records; no further search this round. The scout notes a 2025 expansion (arXiv 2503.19698: 219,792 labelled sources, a TDE class) without a confirmed data release.
- Papers and pages: the paper and the Zenodo record above; the ALeRCE Explorer.
- Metric: the paper reports macro-averaged precision and recall at both levels ("macro-averaged precision and recall scores of 0.57 and 0.76" at the bottom level, abstract), threshold metrics side by side with no fixed decision (MET-5, MET-6), so the fallback `log_loss`; inputs none.
- Risks for /add-dataset: the Zenodo features file is described as covering the unlabelled set, so check first that the labelled sources' features ship (otherwise the ALeRCE API); the features are vectorized light curves, so the `Time-series (Classification)` question is judged on the data (SEL-12; the field's own tool is the random forest on these features); catalog labels favour bright, already known sources, so the class mix is not the alert stream's (`Selection Bias`, as on `sdss_17`); missing features coded -999 (from the scout); the classes are hierarchical: ship the 15 classes, the top level being another framing.
- Priority: gap + (physics & astronomy: 0 accepted; multiclass thin), use case +, source +, shape + (about 123,000 sources, 152 features), risk - (the labelled set's features unconfirmed; vectorized series).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `first_principles_leavitt`, `first_principles_supernovae_zg`, `first_principles_supernovae_zr`; the gap scout for physics and astronomy.
- as published: ZTF sources with at least 6 detections in g or r: labeled set of 123,496 sources in 15 classes (transient 1,718; stochastic 34,713; periodic 87,065; paper Table 1), 152 features (124 detection and ...; target: Class among 15 (SNIa, SNIbc, SNII, SLSN, QSO, AGN, Blazar, YSO, CV/Nova, LPV, E, DSCT, RRL, CEP, Periodic-Other), labels cross-matched from independent ...; access: open.
- Why: The production classifier is a balanced random forest on exactly these features, so tabular models are the field's tool; labels come from catalogs independent of the features; large and openly licensed | The supernovae records are one ZTF light curve each (flux vs days after peak, about 240 points, a curve fit, not a ...
- Adds: A large hierarchical multiclass task (15 classes, heavy imbalance). Risks: vectorized light curves (Time-series (Classification) marker, SEL-12 judged per dataset; HTRU2 precedent); the Zenodo text says the features file covers the 'unlabeled ZTF set', so whether the labelled sources' features ship must be checked ...
