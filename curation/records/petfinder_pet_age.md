---
unique_name: petfinder_pet_age
name: PetFinder
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2018'
problem_type: Multiclass Classification
source_links:
- https://www.kaggle.com/c/petfinder-adoption-prediction
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/core-img-cls-petfinder
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4, for the competition's task and not MulTaBench's: PetFinder.my Adoption Prediction (Kaggle Featured, 2018-12-27 to 2019-04-10, 2,023 teams) predicts how fast a listed pet is adopted from the listing's attributes, description and photos; MulTaBench re-targets the same rows to the pet's age in octile bins, a fact the lister enters and no decision needs (SEL-8, USE-5).
- Source: the competition by PetFinder.my, Malaysia's animal welfare platform (https://www.kaggle.com/c/petfinder-adoption-prediction). As published: `train/train.csv`, one row per listing (about 15,000; type, name, age, two breeds, gender, three colours, maturity size, fur length, vaccinated, dewormed, sterilized, health, quantity, fee, state, rescuer id, video and photo counts, description, `AdoptionSpeed`), `test/test.csv` without labels, the photos per listing, Google Natural Language and Vision API outputs per listing as JSON, and breed, colour and state lookup tables; `AdoptionSpeed` has five classes, from adopted on the day of listing to not adopted after 100 days (the competition's data page; not re-read in this session, Kaggle pages do not render here). MulTaBench (core, https://huggingface.co/datasets/multabench/core-img-cls-petfinder) keeps 14,652 listings with a photo, uses `AdoptionSpeed` as a feature and predicts `AGE_BIN`, the age cut into eight equal-frequency bins (Appendix B.1).
- Use case: the competition's: PetFinder.my and the rescuers who list a pet want to know at listing time how quickly it will be adopted, to improve the profile and plan care (the overview frames the models as tools for shelters and rescuers; not re-read in this session). Fit direct: every input is on the listing when it goes live. Regime grouped by `RescuerID` (one rescuer lists many pets; whether the competition's test rescuers were disjoint from training is to verify).
- Siblings and duplicates: no other record of this competition (grep for petfinder, adoption and the slug); `long_beach_animal_shelter_outcomes` (this run's candidate, shelter intake outcomes) is a related task from another source. External collections: MulTaBench (core image set, the age target); the competition is a common multimodal example (AutoGluon multimodal tutorials; TensorFlow Datasets `pet_finder` uses its images).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the competition pages (overview, data, evaluation; the solution threads not read here); MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Sec. 4 Table 2 (the PetFinder analysis on the age target), Table 3 (14,652 rows; 17 structured, 4 text, 1 image), Table 11 (frozen AUC 0.832, task-aware 0.841).
- Metric: the competition's quadratic weighted kappa on `AdoptionSpeed` (Kaggle API `evaluationMetric`: QuadraticWeightedKappa), a leaderboard metric on hard ordinal labels (MET-4); inputs none. MulTaBench's age bins have no source metric.
- Risks for /add-dataset: settle the target first: the record's name says age, the source's task is `AdoptionSpeed`, and `AdoptionSpeed` is then no feature (rename the record or note why it keeps its name); only the training labels are public; the description, photos and API JSON carry part of the signal (photos dropped, JSON scores kept as numbers or dropped, SEL-12); listings of several pets (`Quantity` > 1); `RescuerID` is the group and never a feature (SPLIT).
- Priority: gap + (multiclass, 24 accepted datasets, thin), use case + (the competition names the actor and the decision), source + (a Featured competition with a data page), shape + (about 15,000 listings, mixed types and text, grouped by rescuer), risk - (a target to settle against the record's name).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 14,652 rows; 17 structured, 4 text, 1 image features (MulTaBench Table 3); target: Pet age in 8 equal-frequency bins.
- Why: Predict a listed pet's age band from photo, listing text and listing attributes
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Target binned by MulTaBench, not the source's own target. PetFinder.my 2019 Kaggle competition; the competition target was AdoptionSpeed, MulTaBench repurposes Age. ...
