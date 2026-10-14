---
unique_name: corporate_credit_rating_cat_data_set_ratings_raitings_duplicate
name: Multiclass_Classification_for_Corporate_Credit_Ratings (OpenML 46372)
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Duplicate
collections:
- TabSTAR
original_source: OpenML
year: '2024'
domain: finance
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46372
type_adapter_id: curation-record-v1
---

## Comments

**Assessment (AI, 2026-10-12):** OpenML 46372 (uploaded 2024-11-20; 5,000 rows, 500 per rating) is simulated from the 197 rows of the Credit Risk Analytics book's `ratings.csv`, which corporate_credit_rating_cat_data_set_ratings_raitings curates. Each ratio is drawn uniformly between the minimum and maximum of the book's rows with the same rating: every value falls inside, the class means sit at the midpoints, and the correlations within a rating are 0.03-0.04 against 0.21-0.42 in the book's rows. OpenML also labels rating 1 "very_bad", while the book's best rating is 1. The evidence is in the canonical record's assessment of 2026-10-07.

CC (2026-10-12, Lennart): No: generated data (AHDS), a simulated copy of the book's rows that corporate_credit_rating_cat_data_set_ratings_raitings curates.
