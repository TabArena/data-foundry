---
unique_name: distribution_transformers_at_cauca_department
name: Distribution Transformers at Cauca Department
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- New IID
- 'Samples: One Moment'
- 'Target: Fixed Delay'
- Database Snapshot
collections:
- New (BeyondArena)
original_source: Other
collection_period: '2020'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- 'download link (down for me): https://data.mendeley.com/datasets/yzyj46xpmy/4'
- 'data proof: https://ieee-dataport.org/documents/data-driven-predictive-maintenance-distribution-transformers'
v2_path: datasets/_dev/tabarena-v0pt2/distribution_transformers_at_cauca_department/dataset.py
source_row: 741
type_adapter_id: curation-record-v1
---

## Comments

paper: https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance

used SVMs

No time stamp, might be able to do only one split. Unclear if it would have a temporal impact, data seems very time-independent. Features are averages across year

15,869 transformers -> might have grouped/temporal leakage if we split and take data from both years at once? need to check. For just one year, it is IID, for two years it is not.

**Assessment (AI, 2026-10-07):** Source: Mendeley Data v4 (doi:10.17632/yzyj46xpmy.4, public API) with the Data in Brief article (doi:10.1016/j.dib.2021.107454); the IEEE DataPort link is a processed 2025 copy. Both yearly files hold the same 15,873 transformers and one inventory, taken after the 2020 burns. Added as IID on 2020 (629 burned): two years cannot give three temporal windows. SELF-PROTECTION (an internal switch, item C) behaves in the data as a mark of replacement units: self-protected units without an earlier burn burned at 42% in 2019 and 2020, those with one at 13% and 9%. It is dropped. burn_rate counts only earlier years. Open: power_kva may show replacement units.

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 4: power_kva/installation_type may describe replacement units (post-outcome leak); issue 3 unrepairable source bug). Real utility predictive-maintenance task with a documented source, but the post-outcome inventory makes leaks hard to rule out.

**Assessment (AI, 2026-10-20):** re-check by the review panel; recommend shipping after the changes now in the definition (the curator has the call). Facts: the files hold 15,873 rows (15,869 is the paper's count, which the authors' MATLAB table also has); the attributes are one static inventory, identical in the 2019 and 2020 files, not yearly averages; the one typo the definition corrects is the 2020 file's mounting category `POLE WITH ANTI-FRAU NET`, not a target label. LEAK-10 (Must): power_kva changed on replacement (none of the 163 self-protected first burns of 2020 is 5 kVA, against 9% of the other 277), so power_kva and installation_type are dropped and the energy not supplied is kept only as outage hours (EENS / (1.08 x kVA)); lightning densities of 0.0 (one area, 487 rows) are set to missing. LightGBM ROC AUC is now 0.639 on the shipped random folds and 0.648 trained on 2019 and tested on 2020. Open for the curator: an amendment of LEAK-10 to keep the two columns, and the shared split amendment for tasks with too few periods. Priority 2: gap -, use case - (fit approximate: forced random split, label coverage of 2020 not stated), source + (Mendeley v4 with the Data in Brief article), shape + (15,873 units, 12 features), risk - (the source's dropped zeros in lv_network_km cannot be repaired row by row).

CC (2026-10-21, Lennart): LEAK-10 stays as written (option (a) of the cross-dataset item "Amend LEAK-10 for a looked-up attribute that changed for an unknown subset of positives?"): power_kva and installation_type stay dropped, no definition change.

CC (2026-10-21, Lennart): option (a) of the cross-dataset item on tasks with too few periods: the closest regime that keeps the rows, tagged as forced from temporal, with the cost measured against the valid windows (SPLIT-8 amended).

**Assessment (AI, 2026-10-21):** keeps one year, IID, `ForcedIIDFromTemporal`; the notes cite the amended SPLIT-8. Cost: LightGBM ROC AUC 0.648 trained on 2019 and tested on 2020 against 0.639 on the random folds. Review issue 2 settled.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: urban, keraunic_criticality, removable_connectors, overhead_lv_network, circuit_end.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — a data article with no prediction benchmark or score.

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `client_type` (a level outside the scale is a state of its own).

CC (2026-11-01, Lennart): marks on the review board of PR #37: client_type stays unordered (non-residential types beside the strata), noted in the definition.

CC (2026-11-13, Andrej): time basis `DelayedTarget` instead of `ForcedIIDFromTemporal` (Review issue 1, B):
- One inventory ranked at the start of 2020, the year's burns after it: one shared moment and a closed window, which the sharpened one-moment rule names a `DelayedTarget`.
- The random split stays.

CC (2026-11-16, Andrej): time basis `StationaryRelation` instead of `DelayedTarget`, which was dropped before it shipped:
- Trained on the 2019 burns and tested on 2020, LightGBM scores ROC AUC 0.648 against 0.639 on the random folds: the one forward window of the source's two years costs nothing.
- The random split stays.

CC (2026-11-18, Andrej): time basis `AssumedStationaryRelation` in place of `StationaryRelation` (Review issue 3, C; stationarity reasoning): the operator ranks its transformers for the year right after the inventory, and burns follow lightning density and network exposure, which one year does not change. The stationary-relation test of 2026-11-18 is inconclusive on the source's one forward period, so the tag rests on this reason; the random folds stay.

## Review

**Outcome:** added. The time basis went from `ForcedIIDFromTemporal` to `DelayedTarget` (2026-11-13), to `StationaryRelation` when `DelayedTarget` was retired (2026-11-16), and to `AssumedStationaryRelation` (2026-11-18).

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Untuned LightGBM ROC AUC 0.628 (0.606 to 0.660 over 9 splits; a random column moves it by about 0.015); exact-twin labels (48 to 67 test rows per split) add nothing, the nearest neighbour's label scores 0.519, row order carries no signal. It asks over which years `outage_hours` and the lightning columns are measured; the definition treats them as history before 2020 (the 15 h floor marks the 2015-2018 failures), and the release states no window, so this stays as recorded. Re-audited 2026-11-27 against both Mendeley v4 files (sha256 match): nothing needs a decision. Only the 2020 file ships, one row per transformer, so no unit is on both sides of a split; among the kept columns the 2019 and 2020 first-burn groups look alike, so no kept attribute shows a post-failure recording (self_protected, power_kva and installation_type are already dropped). The burn counts, the burn_rate identity, the forward against random comparison (0.644 against 0.640) and the accepted urban warning reproduce. Text fixes: the time-basis bullet of `curation_comments` skips `DelayedTarget` (2026-11-13 to 11-16), and the README is stale (still shows `ForcedIIDFromTemporal`). Earlier: The time basis is `AssumedStationaryRelation` (Andrej, 2026-11-18); issue 1 was resolved on 2026-11-13
as `DelayedTarget`, changed on 2026-11-16 and 2026-11-18 (CC lines).

**Issues for Andrej:**

1. **Retag `DelayedTarget` instead of `ForcedIIDFromTemporal`, now that a one-moment release is forced only when its target is of that moment?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal` (Lennart, 2026-10-21), from when every release with too few periods was forced[^8a-x].
     - Every row is predicted at one shared moment, the start of 2020, when the operator ranks its transformers, and the target arrives after it, with the burns during 2020, a year that has closed for every transformer, which is a `DelayedTarget`[^32a-x].
     - The tag alone changes: the split stays random.
   * **Background:** both files carry one inventory of the same transformers; trained on the 2019 burns and tested on 2020, LightGBM scores ROC AUC 0.648 against 0.639 on the random folds.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision of 2026-10-21 stands | the tag says time was lost, which the one shared moment contradicts |
     | B | `DelayedTarget` | the tag and its `Time basis:` line name the shared moment and the target's window | follows the record's facts and the sharpened rule; the measured transfer from 2019 to 2020 shows no cost | changes a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag in `data_tags` and write the `Time basis:` line as SPLIT-32 asks for a `DelayedTarget` (the moment, the window, closed for every row, what the split cannot test: the next moment); add a CC line; the split code does not change.

   [^8a-x]: **SPLIT-8** (Must, sharpened 2026-11-13): a release that is one moment, every row predicted at the same point, is forced only when its use case looks forward from a target of that moment or of unknown timing; otherwise SPLIT-32 gives it `Retrospective` or `DelayedTarget`.
   [^32a-x]: **SPLIT-32** (Should): `DelayedTarget` is one shared prediction moment with the target arriving after it, in a window closed for every row; a random or grouped split then draws train and test from that one moment and window.

   **Andrej (2026-11-13, change):** Option B: DelayedTarget.

   **Resolved (2026-11-13, Andrej):** B. The tag is `DelayedTarget`, with its `Time basis:` line in the definition; the split does not change.

3. **`AssumedStationaryRelation`, or `ForcedIIDFromTemporal`, now that the test is inconclusive?**

   * **Problem:**
     - Time: Two label years (2019, 2020 burns) on one static inventory of the same 15,873 transformers, no per-row dates; the stationary-relation test (2026-11-18) is inconclusive on the single period even pooled, and the source (Mendeley v4, Data in Brief 2021) holds no further year.
     - Use: The Cauca grid operator ranks its transformers at the start of a year for that year's burns: use right after the collected period (2019 burns -> 2020 ranking), the definition's own use case.
     - Mechanism: Burns follow lightning density, overhead exposure, network length and load (physical drivers recorded as features); one year between inventory and use does not change that physics, though weather intensity and grid investment vary by year.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | distribution_transformers_at_cauca_department itself | LightGBM trained on 2019 burns, tested on 2020: ROC AUC 0.648 vs 0.639 random folds | flat on one forward window (thin); v3 test inconclusive | same data, the only forward window |
     | aps_failure / other equipment-failure sets in the collection | no dated equipment-failure set tested flat or not flat | none | failure of grid/vehicle equipment |

   * **For a stationary use case:**
     - Use right after the collected period: rank this year's risk from last year's inventory and history.
     - Physical drivers (lightning density, overhead network, circuit end) that a year does not change.
     - The one forward window costs nothing (0.648 forward vs 0.639 random).
     - No adversary, price or market in the outcome.
   * **Against:**
     - One forward window only, and the v3 test is inconclusive, so no measured support for longer horizons.
     - Year-to-year lightning and rainfall vary (ENSO cycles in Colombia), moving the burn rate.
     - Grid investment and replacement after burns change the fleet; the inventory was taken after the 2020 burns (post-outcome concerns, power_kva/installation_type dropped).
     - Whether the 2020 label covers the whole year is not stated.
   * **Earlier views:**
     - CC (2026-10-21, Lennart): forced from temporal, cost measured against valid windows (SPLIT-8 amended).
     - CC (2026-11-13, Andrej): DelayedTarget instead of ForcedIIDFromTemporal (issue 1 B).
     - CC (2026-11-16, Andrej): StationaryRelation, from the 2019->2020 window costing nothing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `StationaryRelation` as shipped (implemented) | No change | No rebuild | The test it rests on is inconclusive |
     | B | `ForcedIIDFromTemporal` | The folds stay; the line names the inconclusive test | Claims only what is measured | |
     | C | `AssumedStationaryRelation` | The folds stay; the line opens `AssumedStationaryRelation (Andrej, 2026-11-18): the operator ranks its transformers for the year right after the inventory, and burns follow lightning density and network exposure, which one year does not change` | Documents why random folds stand for later samples | One forward window only, and the v3 test is inconclusive, so no measured support for longer horizons.; Year-to-year lightning and rainfall vary (ENSO cycles in Colombia), moving the burn rate. |

   * **Recommendation:** C, both valid reasons hold: use right after the period and a physical mechanism, and the one forward window agrees; 'measure' no longer helps since the source's two years were measured (inconclusive) and no later year exists, so only a release with more years could settle it. Confidence: medium. **Decision:** A, B or C?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, change):** Option C: AssumedStationaryRelation.

   **Resolved (2026-11-18, Andrej):** C. `data_tags` names `AssumedStationaryRelation` in place of `StationaryRelation`, and the `Time basis:` line opens `AssumedStationaryRelation (Andrej, 2026-11-18): the operator ranks its transformers for the year right after the inventory, and burns follow lightning density and network exposure, which one year does not change`; the random folds stay.

## Reference

[1] L. Alvarez, Predictive Maintenance of Distributions. Transformers. Case Study: Department of Cauca (Colombia), first ed., Our Knowledge Publishing, 2021. ISBN 978-620-3-93390-1
https://www.researchgate.net/publication/355264319_Dataset_of_Distribution_Transformers_for_Predictive_Maintenance
