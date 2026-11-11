# qsar_bioconcentration

**Outcome:** added. The bioconcentration class of 776 organic chemicals in fish (Grisoni et al. 2016, UCI 510), from
the structure and the measured logKOW, grouped on the Bemis-Murcko scaffold (558 groups). Opened on 2026-11-11 from
the review of how catalogues of fixed properties split: the definition names no time basis for its scaffold split.

**Main points:** Date the chemicals through their source tables before naming the time basis, as the three sibling
Milano sets were asked to do, or name the scaffold split `Timeless` now (issue 1)?

**Issues for Andrej:**

1. **Time basis: date the chemicals first, or name the scaffold split `Timeless`?**

   * **Problem:**
     - The definition splits on the scaffold and names no time basis, while the record carries
       `Samples: No Time Dimension`.
     - A chemical's bioconcentration factor is a fixed property of the chemical, the case the `Timeless` prototype
       names[^1a].
     - The chemicals carry CAS numbers, and a catalogue whose items enter in eras counts as arising over time even
       where each item's own value is fixed, so the identifier is worth checking before the tag is set.
   * **Background:** the use case is an assessor judging an untested chemical before a fish test, holding its
     structure and its logKOW; the measured BCF values were compiled from the authors' 2015 table, drawn in turn from
     VEGA and the EURAS BCF collection, neither of which ships a test date in this release.
   * **Experiments:** the share of test chemicals with a close training analog (Tanimoto 0.7 or more, Morgan radius 2)
     fell from 12.6% under a random split to 6.4% under the scaffold groups when the split was adopted; no split by
     year has been measured, because no year is in the release.
   * **Consistency:** on 2026-11-11 qsar_biodeg was sent to be dated through NITE, and qsar_fish_toxicity and
     qsar_aquatic_toxicity through ECOTOX, before their time basis is named; this dataset is the fourth of that
     family and its chemicals carry the same kind of key.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | no change | nothing to write | the definition does not say why a split that is not temporal is safe in time |
     | B | Date through the source tables, then decide | look for a measurement year per CAS number in the EURAS BCF collection and the authors' 2015 table, then measure a split by year as the siblings will | decides on a measurement; the same route as the three siblings | the compilations may carry no year, and then the answer is C anyway |
     | C | Scaffold split, `Timeless` | the tag and a `Time basis:` line naming the fixed property, the undated compilation and the measured analog shares | nothing to measure; as the other molecule sets | assumes the catalogue does not drift, which the siblings are being asked to check |

   * **Recommendation:** B, for the same reason you gave the three siblings: the key is in the release, so the
     question can be settled by measurement rather than assumed. **Decision:** A, B or C?

   **Notes for the AI:** on B, join the CAS numbers to the EURAS BCF collection and the authors' 2015 supporting
   table, report the share dated and the year range, and if dated measure as qsar_tid_11 did (expanding windows by
   first year against scaffold folds on the same test chemicals, close-analog shares for both). On C,
   `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`) and a `curation_comments` bullet naming the
   property, the undated compilation and the fall from 12.6% to 6.4% close analogs; then `dataset check`, a CHANGELOG
   entry and a record CC line with `Andrej` in `checked_by`.

   [^1a]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows; `Timeless` when the target
     is a fixed property of the item. Question 1 also asks which identifier a parent source could date the items by,
     and "none published" is an answer; a catalogue whose items enter in eras arose over time even when each item's
     value is fixed.

   **Andrej (2026-11-11, change):** Option B: Date through the source tables, then decide.

