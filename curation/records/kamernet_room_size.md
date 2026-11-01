---
unique_name: kamernet_room_size
name: Kamernet Room Size
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
year: '2025'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/amancapy/all-kamernet-rent-listings-w-photos-netherlands
- https://arxiv.org/abs/2605.10616
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: a one-day scrape of Dutch room listings from Kamernet; MulTaBench's target, the room's floor area, is a fact the landlord states, not a prediction anyone acts on, while the natural target, the rent, sits among the inputs.
- Source: Kaggle upload by amancapy, "All Kamernet Rent Listings w. Photos (Netherlands)" (file dated 2025-07-11, CC0): "All listing pages on a given day scraped along with listing photos"; "All visible details on listing pages were scraped and cleaned up for tabulation"; one `listings_df.csv` (3.9 MB) and thumbnails of about 256 px. As MulTaBench ships it (extended release, Table 9): 1,638 rows, 20 structured columns (place and furnishing type, rent, deposit, additional costs, availability dates, tenant preferences, shared facilities, energy label, roommates), the city, age range and extras as text, one photo; target `size` (m²); it dropped the description "because it states the floor area".
- Use case: none for the area: the landlord enters it and a tenant reads it off the listing. A rent framing (a landlord or tenant judging the asking rent of a room from its attributes) would be a price task like the other rent records. Fit approximate at best; regime IID (one day's listings).
- Siblings and duplicates: no record of this source (searched kamernet). Rental siblings: `immoscout24_germany_rental_offers`, `apartment_for_rent_classified` (`TBD -> 2nd Tier`). External collections: MulTaBench (extended release, admitted on joint signal only).
- Better data: a candidate of the benchmark MulTaBench (not searched in this run, by its brief).
- Papers and pages: the Kaggle page; MulTaBench (arXiv 2605.10616, Appendix F.1; Table 8: R² 0.446 from the structured columns, 0.129 from the photo, 0.459 joint).
- Metric: none found (the Kaggle page defines no task; MulTaBench scores R²), so the fallback `rmse`; inputs none.
- Risks for /add-dataset: the target (USE-2, USE-5: no decision rests on the area; the rent is the alternative and then drops out of the inputs); the description states the area (LEAK); 1,638 rows for about 25 columns; the uploader rescrapes "periodically", so later versions may hold more days, with the same room across scrapes as a group (SPLIT).
- Priority: gap 0 (business & marketing, regression, IID), use case 0, source 0 (a scrape described in a paragraph), shape + (1,638 rows, mixed types), risk - (an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark MulTaBench (https://arxiv.org/abs/2605.10616).
- as published: 1,638 rows; 20 structured, 4 text, 1 image features (MulTaBench Table 9); target: Room floor area (m2).
- Why: Predict a Dutch rental room's floor area from listing data and a photo
- Notes: Extended release (admitted on Joint Signal only), not one of the 40 benchmark datasets. Image-tabular: one image column per row (released as image files); out of scope for a tabular-only container unless the image is dropped or embedded. Kaggle 2025 scrape (CC0).
