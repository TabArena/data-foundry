# early_learning_predictors

**Outcome:** added. In the working copy since the migration; GitHub issue #48 (a column-type review of #37) found that
`ward_best`, a ward number, ships as a number. The AI recommends the national ward code as a category in its place.
Its other points on this dataset were settled in #37 or already hold (see the notes of issue 1).

**Main points:** Ship the ward as a code (which one), or drop it?

**Issues for Lennart:**

1. **Ship the ward as a code, not a number?**

   * **Problem:**
     - `ward_best` (1 to 130, missing for 53% of the children) is the ward's number within its municipality, and it ships as a number.
     - The same number names different places: ward 4 of Steve Tshwete (`id_ward_best` 83103004) and ward 4 of Dr JS Moroka (83106003) are two wards; 101 numbers stand for 569 wards.
     - The national ward code `id_ward_best` is dropped with the ids; issue #48 proposes a category, or dropping both.
   * **Background:** The definition keeps the province, district and municipality (`prov_best`, `dc_best`, `mn_best`) as categories; the Zindi release dropped all of them[^1].
   * **Effect on the task:** As a number, a model reads ward 4 < ward 23 as an order of places that does not exist; as a category, `ward_best` still pools wards of different municipalities.
   * **Experiments:** A ward holds 1 to 18 facilities (median 3; 28.5% of the wards hold one); the split groups by facility, so a test facility shares its ward with training facilities in most wards, as it shares its municipality.
   * **Consistency:** A code the source ships as a number ships as a category, unless its digits carry meaning (zip code prefixes)[^1]; the municipality here already ships that way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Number (implemented) | as now | none found | an order of places that does not exist |
     | B | `ward_best` as a category | one line in `_feature_types` | smallest change; issue #48's first proposal | one level pools up to several wards of different municipalities |
     | C | National ward code as a category | ships `id_ward_best` as a category in place of `ward_best` | one level per ward; the same form as the municipality | brings back a column the notes list with the ids; 569 levels with few facilities each |
     | D | Drop the ward | removes `ward_best` | the location stays at the municipality | loses the finest location the data has |

   * **Recommendation:** C, one level per real ward, kept like the municipality. **Decision:** A, B, C or D?

   **Notes for the AI:** on C, remove `id_ward_best` from `indicator_cols` (it is listed twice), drop `ward_best`,
   add `id_ward_best` to `categorical` (integer codes stay integers, restored as categories by the container,
   Lennart 2026-11-04), and state in `curation_comments` why the ward code stays while the other ids leave. On B,
   add `ward_best` to `categorical`; on D, add it to `drop_columns` with the reason. Then `dataset check`, the group
   probe, a CHANGELOG entry and a CC line in the record. Issue #48's other points on this dataset, not raised here:
   `programme` is categorical already (it was at e24d557 too); the seven `pra_agency_*` columns stay unordered and
   `pra_job` stays a category, as the #37 ordinal review decided (a bipolar choice whose fourth answer, "disagree
   with both", sits off the line; job roles differ in kind); the 26 "other" free-text columns are strings by the
   cleaning of 2026-10-30.

   **Lennart (2026-11-05, change):** Option C: National ward code as a category.

   **Consistency check (AI, 2026-11-05):** Why does the ward code ship when the survey's sampling cluster
   `id_cluster_original`, of the same grain (430 clusters, median 3 facilities), is dropped as "leaks with
   school-based split"? The fact that sets them apart: the cluster exists only in the 2021 round (5,222 children),
   a unit of that survey's sample design that marks the dropped round; the ward is a place, in the 2020-2022 rounds.

   **Lennart (2026-11-05, chat):** Ward ships, note why.

   **Resolved (2026-11-05, Lennart):** C. `id_ward_best` ships as a category, `ward_best` is dropped, and the notes
   say why the ward stays while the sampling cluster leaves.

   [^1]: **CLEAN-14** (Should): a code the source ships as a number (an id, a type code, a detector column) is a
     category, unless its digits carry meaning a model can use (zip code prefixes, whose nearby values are nearby
     places).
