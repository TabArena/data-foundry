---
unique_name: churn_telco_south_asia_duplicate
name: Churn Telco (duplicate)
suggestion: 'Yes'
type_adapter_id: curation-record-v1
---

## Comments

Another upload of a telco churn file.

CC (2026-10-02, Lennart): a later comment closes the block.

## Review

**Outcome:** not added; duplicate. The files are the 2,000 rows of `churn_telco_south_asia` with renamed values.

**Main points:** The files are the 2,000 rows of `churn_telco_south_asia` with renamed values.

**Issues:**

1. **Leave it out as a duplicate?**

   * **Problem:** Every row matches a row of `churn_telco_south_asia` once the values are renamed[^1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave out (implemented) | the record gets `No` | no copy in the benchmark | none found |
     | B | Add it | a second folder | none found | the same rows twice |

   * **Recommendation:** A. **Decision:** A or B?

   [^1]: **PROV-3** (Must): the data is real, not a real table someone reworked (relabelled, columns renamed).

