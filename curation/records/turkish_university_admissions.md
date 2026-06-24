---
unique_name: turkish_university_admissions
name: turkish-university-admissions
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- 2nd Tier / Scientfic Discovery
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2025'
domain: education
required_split:
- Temporal (NON-IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/ramazanizci/turkish-university-admissions
- https://github.com/izcir/turkish-university-admissions-dataset
source_row: 457
type_adapter_id: curation-record-v1
---

## Comments

Looks like good data, but predictive task is not obvious

"Raw data was programmatically collected from the YÖK Atlas web portal using `YokAPI`(https://github.com/izcir/YokAPI/), a custom-built Python package developed specifically for this project. Following collection, the raw data underwent an extensive cleaning and processing pipeline using the Pandas library in Python. This process involved: 1. Standardizing university, faculty, and department names across all years. 2. Handling data inconsistencies and missing values. 3. Creating normalized relational tables (dimension and fact tables) for structural integrity. 4. Finally, generating a denormalized main CSV file (`university_admissions_turkey_2019_2024.csv`) by joining all tables for ease of analysis."
