# eryhemato_squamous_disease

**Outcome:** added. In the working copy since the migration; GitHub issue #48 (a column-type review of #37) found that
the 10 clinical scores ship as unordered categories, although the definition's notes say they are numbers. The AI
recommends numbers.

**Main points:** Ship the 10 clinical scores 0 to 3 as numbers, as ordered categories, or keep them unordered?

**Issues for Lennart:**

1. **Ship the 10 clinical scores 0 to 3 as numbers?**

   * **Problem:**
     - `_clean` turns the 10 scores into numbers (`SCORES`, the decoding of 2026-11-01), but `_feature_types` declares every column except `age` and the target categorical, so they ship as unordered categories (README: 12 categorical).
     - The notes contradict each other: "We encode all features but age as categorical, since they are ordinal features in nature" and "10 scores with no words per level are numbers".
     - Issue #48 found it and proposes an ordered category 0 < 1 < 2 < 3.
   * **Background:** The source gives words only at the two ends of the scale: "0 indicates that the feature was not present, 3 indicates the largest amount possible, and 1, 2 indicate the relative intermediate values" (`dermatology.names`, [UCI](https://doi.org/10.24432/C5FK5P))[^1].
   * **Effect on the task:** Unordered, a model cannot use that grade 2 lies between 1 and 3, and with 366 patients each grade as its own level splits the few patients further.
   * **Consistency:** The 15 other definitions with a `SCORES` list ship every listed column as a number (checked against each README's type list, 2026-11-05); this is the only one where a blanket categorical in `_feature_types` casts them back.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered categories (implemented) | keeps the blanket cast of `_feature_types` | none found | the order of the grades is lost; contradicts the definition's own notes |
     | B | Numbers | `_feature_types` declares only `family history` categorical | the source names only the two ends; what the notes already say; as in the 15 other definitions | the step from 0 to 1 counts as much as from 2 to 3 |
     | C | Ordered categories 0 < 1 < 2 < 3 | the 10 scores in `FeatureTypes(ordinal=...)` | issue #48's proposal; keeps the order without a spacing | departs from the rule for a score without words per level |

   * **Recommendation:** B, the rule's form and what the 2026-11-01 decoding meant to ship. **Decision:** A, B or C?

   **Notes for the AI:** on B, `_feature_types` returns `FeatureTypes(categorical=["family history"])` (age stays
   numeric); remove the bullet "We encode all features but age as categorical, since they are ordinal features in
   nature." from `curation_comments`; on C, `FeatureTypes(ordinal={c: [0, 1, 2, 3] for c in SCORES},
   categorical=["family history"])` and a Cases row of kind `exception` under CLEAN-14. Then `dataset check`, a
   CHANGELOG entry, a CC line in the record.

   **Lennart (2026-11-05, change):** Option B: Numbers.

   **Resolved (2026-11-05, Lennart):** B. The 10 scores ship as numbers; `_feature_types` declares only `family
   history` categorical, the contradicting note is gone, and a test checks that every `SCORES` column ships numeric.

   [^1]: **CLEAN-14** (Should): a score or rating with no words per level, or words only at its two ends, is a
     number, as shipped; the test is whether the source says in words what each level is.
