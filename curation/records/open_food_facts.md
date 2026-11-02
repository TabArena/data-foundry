---
unique_name: open_food_facts
name: Open Food Facts
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Website
domain: Other
required_split:
- Random (IID)
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/openfoodfacts/world-food-facts
- https://world.openfoodfacts.org/data
source_row: 836
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: a crowdsourced product database with no predictive target of its own; the obvious target (Nutri-Score) is computed by a published rule from the nutrient columns.
- Source: Open Food Facts, a volunteer non-profit (world.openfoodfacts.org), crowdsourced from barcode scans; the Kaggle copy `openfoodfacts/world-food-facts` is uploaded by the organisation itself (file `en.openfoodfacts.org.products.tsv`, 1.0 GB, 2019-09-19 snapshot; the Kaggle description now says "over 4 million products from 150 countries" and "over 150 columns"). As published: one wide table of products (ingredients, allergens, categories, countries, nutrients per 100 g, Nutri-Score and NOVA where computed), heavy missingness.
- Use case: none from the source as a prediction; the organisation's list of AI tasks (github.com/openfoodfacts/openfoodfacts-ai) is mostly extraction from product photos and text. A tabular framing (the NOVA group or the category from nutrients) would be ours. Fit: none yet. Regime IID by product, but near-duplicate products across countries would need grouping.
- Siblings and duplicates: none in `curation/records/`. External collections: none found.
- Papers and pages: the Kaggle page and the Open Food Facts data page; no paper defines a task.
- Metric: none found (Kaggle dataset page, Open Food Facts data page), so the fallback for whichever target is chosen (MET-1, MET-11).
- Risks for /add-dataset: Nutri-Score grade and points are a deterministic function of the nutrient columns (SEL-5, `Trivial`); NOVA is assigned by a rule on the ingredient list (text); the table is a moving snapshot of a living database; text-heavy columns.
- Priority: gap 0, use case 0, source + (the organisation documents the data), shape + (millions of rows, mixed types), risk - (no target; the natural one is rule-computed). Markers: `No Good Target (yet)` replaces `No Good Target / Scientific Discovery` (a database built for another purpose, waiting for a target, not a discovery table); `Needs extensive data wrangling` kept.

Open Food Facts is a large crowdsourced product/nutrition database (Kaggle world-food-facts) rather than a dataset with a defined predictive target. It is multi-table/database-shaped with heavy missingness and would need extensive wrangling and a chosen target (e.g. nutri-score or food category). As-is it reads as a reference/scientific-discovery table. Suggest TBD -> 2nd Tier; a human must define a meaningful, non-leaking target (e.g. Nutri-Score prediction) and assess usable row count after cleaning.
