# pva_revenue_prediction_kddcup98

**Outcome:** added. In the working copy since the migration; GitHub issue #48 (a column-type review of #37) proposes
ordering `DOMAIN_urbanicity`. The AI recommends keeping it unordered and adding the note the rule asks for.

**Main points:** Keep the neighbourhood's urbanicity unordered, with a note, or order it?

**Issues for Lennart:**

1. **Keep `DOMAIN_urbanicity` unordered, with a note on why?**

   * **Problem:**
     - `DOMAIN_urbanicity` (Urban, City, Suburban, Town, Rural, the first byte of `DOMAIN`) ships as an unordered category, and the notes do not say why.
     - Issue #48 proposes Rural < Town < Suburban < City < Urban, with low confidence: it did not check City against Suburban.
   * **Background:** The dictionary lists the levels U, C, S, T, R and calls `DOMAIN` "A nominal or symbolic field" ([cup98dic.txt](https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98dic.txt)); it does not say whether a city neighbourhood is denser than a suburb[^1].
   * **Effect on the task:** Five levels in 191,769 rows; ordered or not, a model sees each level, so the choice changes little beyond the documented state.
   * **Consistency:** The second byte, `DOMAIN_ses`, is ordered because the dictionary names each level in words on one line.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered, no note (implemented) | as now | none found | the rule asks for a note when the order stays unclear |
     | B | Unordered, with a note | one bullet in `curation_comments` | the source calls it nominal and gives no density order | a model cannot use that rural and urban are the two ends |
     | C | Ordered, Rural < Town < Suburban < City < Urban | `FeatureTypes(ordinal=...)` | the ends are clear; the dictionary's listing order read backwards | the City-Suburban step is a guess |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, add a dated bullet to `curation_comments`: the dictionary lists U, C, S, T, R and calls
   the field nominal, the density order of City and Suburban is not given, so the column stays unordered (CLEAN-14).
   On C, add it to `ORDINAL_LEVELS` and remove it from `categorical`. Then `dataset check`, a CHANGELOG entry and a CC
   line in the record. Issue #48's `WEEKDAY_APPR_PROCESS_START` point (home_credit_default_risk) is not raised: the
   curator's rule of 2026-11-01 orders a named cycle from Monday with the wrap not shown.

   **Lennart (2026-11-05, change):** Option B: Unordered, with a note.

   **Resolved (2026-11-05, Lennart):** B. `DOMAIN_urbanicity` stays unordered; `curation_comments` say why.

   [^1]: **CLEAN-14** (Should): an order still unclear after the sources are checked stays unordered, with a note.
