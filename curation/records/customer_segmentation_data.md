---
unique_name: customer_segmentation_data
name: Customer Segmentation Data
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Missing source information
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: business & marketing
problem_type: Other
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ravalsmit/customer-segmentation-data
source_row: 839
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Missing source information`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`; PROV-1, PROV-3, SEL-16): an anonymous Kaggle upload with no traceable origin, and its values look generated.
- Source: Kaggle `ravalsmit/customer-segmentation-data` (file created 2024-03-11, CC0), the only link. The description gives no origin: "This dataset provides comprehensive customer data suitable for segmentation analysis. It includes anonymized demographic, transactional, and behavioral attributes" (Kaggle API metadata); no company, paper, survey or collection named; no other first source found (web search on the file name and columns).
- As published (preview, 2026-10-22): 53,503 rows, 20 columns (`Customer ID`, `Age`, `Gender`, `Marital Status`, `Education Level`, `Geographic Information`, `Occupation`, `Income Level`, `Behavioral Data`, `Purchase History`, `Interactions with Customer Service`, `Insurance Products Owned`, `Coverage Amount`, `Premium Amount`, `Policy Type`, `Customer Preferences`, `Preferred Communication Channel`, `Preferred Contact Time`, `Preferred Language`, `Segmentation Group`).
- Generated (PROV-3): Indian states in `Geographic Information` with German (27%) and French (25%) as the most common `Preferred Language`; placeholder values (`Behavioral Data` = "policy5", `Insurance Products Owned` = "policy2"); `Policy Type` has the same distribution in every `Segmentation Group` (Group 33-35%, Business 25-27%, Individual 16-18%); 40,259 distinct `Customer ID` for 53,503 rows; the curator's note: "distributions seem very weird and too equal".
- Target: `Segmentation Group` (5 segments, 16-26%) is a segment label of unknown origin, not an observed outcome (SEL-3, SEL-4 if it came from clustering).
- Siblings and duplicates: not checked further (no origin to trace).
- Reject check (AI, 2026-10-22): stands. PROV-1 (Must), with PROV-3/SEL-16 as support. The Kaggle API description is the whole source: "This dataset provides comprehensive customer data suitable for segmentation analysis. It includes anonymized demographic, transactional, and behavioral attributes", plus marketing copy; no company, survey, paper or first uploader behind it, and no upstream found (https://www.kaggle.com/datasets/ravalsmit/customer-segmentation-data, metadata re-read 2026-10-22). The preview (Indian states with German/French as top languages, placeholder 'policy5' values) and the curator's note "distributions seem very weird and too equal" back the AHDS marker.

Kaggle 'Customer Segmentation Data' upload with no documented provenance; the curator's note ('distributions seem very weird and too equal') strongly suggests synthetic/handmade data. Segmentation is fundamentally a clustering exercise with no clear supervised target, so it fails criterion 3 (real predictive task) and likely criterion 4B (artificial data). Confidence in rejection is moderate-high. A human should confirm the data is synthetic and that no leak-free supervised target exists before final rejection.

---

Unclear if data is real, distributions seem very weird and too equal
