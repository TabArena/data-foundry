---
unique_name: cars
name: cars
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
collections:
- TabArena Reject
- TabSTAR
source_links:
- https://www.openml.org/d/44994
source_row: 379
type_adapter_id: curation-record-v1
---

## Comments

CC: ""predict car price as listed from tables in a book, only a specific brand, only from one year.

Deterministic function, as I found with some digging. The paper says ""retail price was calculated from the tables provided in the 2005 Central Edition of the Kelly Blue Book"" The Kelly Blue Book contains values for "suggested retail" for that exact car (2005 GM, specified trim/options, mileage, excellent condition). The value was determined using a proprietary algorithm for exactly those features.

need to check duplicates with our cars datasets;
- cars: Deterministic function, as I found with some digging. The paper says "retail price was calculated from the tables provided in the 2005 Central Edition of the Kelly Blue Book" The Kelly Blue Book contains values for "suggested retail" for that exact car (2005 GM, specified trim/options, mileage, excellent condition). The value was determined using a proprietary algorithm for exactly those features.
""
