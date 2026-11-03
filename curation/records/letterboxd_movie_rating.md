---
unique_name: letterboxd_movie_rating
name: Letterboxd Movies
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- MulTaBench
original_source: Kaggle
year: '2024'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/gsimonx37/letterboxd
- https://arxiv.org/abs/2605.10616
- https://huggingface.co/datasets/multabench/core-img-reg-letterboxd-movies
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages and previews of the published tables, NOT from a built dataset. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a 2024 scrape of letterboxd.com (about 950,000 films in ten tables); MulTaBench's task, a film's average member rating from its metadata and poster, is the kind of catalogue-rating target the curators kept as 2nd Tier (`rotten_tomatoes`, `roger_ebert`) or rejected (`filmtv`, `korean_drama`).
- Source: Kaggle upload by gsimonx37, "Letterboxd (Movies Dataset)" (first version February 2024, GPL-3.0): "Data obtained using a program from the site letterboxd.com", whose film metadata comes from TMDb. As published: `movies.csv` (id, name, year, tagline, description, minutes, average rating) with `actors`, `crew`, `languages`, `studios`, `countries`, `genres`, `themes`, `releases` and `posters` tables joined on the film id, and the poster images; "rating (average film rating) is missing for most films". MulTaBench (core, https://huggingface.co/datasets/multabench/core-img-reg-letterboxd-movies) keeps 12,564 films released 2021-2024 with a rating: year, runtime, tagline, themes, two language columns, 19 genre flags and the poster, target `rating`.
- Use case: none in the source. A candidate: a distributor or streaming service judges a film's reception before acquiring it; fit approximate, since the target is the average of Letterboxd members at the scrape date, and recent releases have few ratings. Regime temporal by release date, or IID on one cohort of releases.
- Siblings and duplicates: no duplicate (grep for letterboxd and the Kaggle slug). The same kind of target from other film sites: `rotten_tomatoes` and `roger_ebert` (`TBD -> 2nd Tier`, `No Good Target (yet)`; "predicting rating might not translate / be usable with such features in the real world"), `filmtv`, `korean_drama` and `mydramalist` (`No`, `No Good Target / Scientific Discovery`). External collections: MulTaBench (core image set).
- Better data: a candidate of the benchmark MulTaBench; no further search for this run's finds.
- Papers and pages: the Kaggle page (field descriptions); MulTaBench, Arazi et al. 2026 (https://arxiv.org/abs/2605.10616), Appendix B.1 ("covering releases between 2021 and 2024"), Table 3 (12,564 rows; 23 structured, 3 text, 1 image), Table 11 (frozen R² 0.439, task-aware 0.443).
- Metric: none found (the Kaggle page defines no task; MulTaBench's R² is benchmark-wide, MET-5), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: Letterboxd's `themes` are probably built from members' activity after release (not verified; LEAK-10 for a prediction before release); the rating of recent films rests on few votes and moves after the scrape (USE-5); ten tables to join if cast, crew or studios are used; the poster is dropped (SEL-12); settle with the film-rating precedents above (treat like cases alike).
- Priority: gap 0, use case 0 (written by the curation), source 0 (an individual's scrape), shape + (12,564 films, mixed types and joins), risk - (post-release themes, an unstable target, precedents split).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 12,564 (releases 2021-2024) rows; 23 structured, 3 text, 1 image features (MulTaBench Table 3); target: Average community rating.
- Why: Predict a film's average Letterboxd rating from poster, genres, year, runtime, tagline and themes
- Notes: Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2024 scrape of letterboxd.com (GPL 3).
