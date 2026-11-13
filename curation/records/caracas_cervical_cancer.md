---
unique_name: caracas_cervical_cancer
name: Caracas Cervical Cancer
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2017'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Z310
- https://www.openml.org/search?type=data&id=46592
- http://vcmi.inescporto.pt/reproducible research/ibpria2017/CervicalCancer/
v2_path: datasets/_dev/tabarena-v0pt2/caracas_cervical_cancer/dataset.py
source_row: 688
type_adapter_id: curation-record-v1
---

## Comments

Some features are multi-categoricals as one-hot encoding. Might want to reverse this.

Has 4 target variables, unsure which one to use. Likely want to use Biopsy as the real ground truth (not just an indicator).

**Assessment (AI, 2026-10-07):** Target: Biopsy. The creators predict it "where only behavioral and demographic information is observable" (Fernandes et al., PeerJ Comput. Sci. 2018, Results), so Hinselmann, Schiller and Citology are dropped as results of the same work-up (Schiller alone: ROC AUC 0.92). The STD and Dx columns are multi-label (43 of 740 patients have 2-4 STD types) and stay binary flags. The 108 patients who skipped the contraceptive question are dropped: they have no positive biopsy, Hinselmann or Schiller result where 8, 5 and 11 are expected, although their answers show no lower risk. Their results look unrecorded. All 55 positives stay. The folder ships the biopsy only; the Multi-target tag stays.

CC (2026-10-15, Lennart): No `Multi-target` tag: the four test results come from one work-up and the dataset predicts the biopsy alone (review page, issue 5).

**Assessment (AI, 2026-10-15):** The STD flags are one questionnaire question each and multi-label (9 patients have two or three types; `std_condylomatosis` is the parent of two subtypes, which `stds_number` counts twice), so they stay yes/no categories rather than one combined category. Impossible answers become missing (2 first intercourses after the current age, 2 STD diagnoses longer ago than the patient's age); the other contradictions (5 `dx_*` flags with `dx` 0, 7 STDs with no diagnosis counted) are not impossible and stay.

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run): the STD flags stay one yes/no category each, impossible answers become missing.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (area under the ROC curve), Fernandes, Chicco, Cardoso & Fernandes 2018, 'Supervised deep learning embeddings for the prediction of cervical cancer diagnosis', PeerJ Computer Science 4:e154, doi:10.7717/peerj-cs.154 (abstract: 'top AUC ~0.69' for the biopsy); first use Fernandes, Cardoso & Fernandes, IbPRIA 2017, doi:10.1007/978-3-319-58838-4_27.

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** `CrossSectional` instead of `ForcedIIDFromTemporal`?

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the result of her screening work-up, read from her answers at that work-up; the biopsy reports her condition then, not a later one, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Background:** the biopsy comes after the questionnaire, so the label is confirmed later, but it reports her condition at the questionnaire; the use case triages for a present disease and forecasts no later state. If you read the work-up as a forecast, A holds.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

## Reference

@inproceedings{fernandes2017transfer,
  title={Transfer learning with partial observability applied to cervical cancer screening},
  author={Fernandes, Kelwin and Cardoso, Jaime S and Fernandes, Jessica},
  booktitle={Iberian conference on pattern recognition and image analysis},
  pages={243--250},
  year={2017},
  organization={Springer}
}
