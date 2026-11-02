---
unique_name: hiv_qsar
name: HIV_QSAR
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Duplicate
collections:
- TabSTAR
source_links:
- https://www.openml.org/d/1039
source_row: 436
type_adapter_id: curation-record-v1
---

## Comments

In TabArena

**Assessment (AI, 2026-11-02):** the duplicate pointer moves to `nci_aids_antiviral_screen`, the live record. The
chain: this record's only source link is OpenML 1039, which is the upload of `hiva_agnostic` (the 2007 Agnostic
Learning vs. Prior Knowledge challenge's HIVA cut), and that cut is 4,229 compounds of the NCI DTP AIDS antiviral
screen, which `nci_aids_antiviral_screen` ships in full. `hiva_agnostic` was itself retired as a duplicate of it on
2026-11-02, so pointing here at the retired record would leave the chain dangling.
