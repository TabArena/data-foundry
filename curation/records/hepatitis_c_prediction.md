---
unique_name: hepatitis_c_prediction
name: Hepatitis C Prediction Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5D612
- https://www.kaggle.com/datasets/fedesoriano/hepatitis-c-dataset
notebook_path: datasets/beyond_iid/new_iid/hepatitis_c_prediction/hepatitis_c_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/hepatitis_c_prediction/dataset.py
source_row: 771
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: donor and patient rows use different recording conventions, which gave the class away.** Share of whole-number values (donor / hepatitis / fibrosis / cirrhosis): ALB 0.11 / 1.00 / 1.00 / 0.97, BIL 0.09 / 1.00 / 1.00 / 1.00, CREA 1.00 / 0.12 / 0.57 / 0.33; ALP is missing for 0 of 533 donors but 18 patients. These four format flags alone give patient-vs-donor AUC 0.9997 and beat the full LightGBM on log loss (0.15 vs 0.27; leak audit 2026-09-24, rechecked). Fix: ALB, ALT, AST, BIL, CREA, GGT and PROT rounded to integers for all rows (median change 0.3-2.6%, worst 2.4 -> 2 in BIL; no value becomes 0) and ALP dropped; CHE and CHOL (single digits, no class difference) stay as recorded. Log loss 0.27 -> 0.35, patient-vs-donor AUC 0.997 -> 0.984; within patients the stage signal is unchanged (OvR AUC 0.80 -> 0.82). Open question answered: no exact or near duplicates (minimum standardised nearest-neighbour distance 0.20), so no evidence of several rows per patient. Class counts: 533 donors, 24 hepatitis, 21 fibrosis, 30 cirrhosis.

Need to check label distribution of class and if multiple entries per patient ID

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Hoffmann et al. 2018 report overall and per-class accuracy under leave-one-out; 88% donors, so accuracy is dominated by donor vs patient; the suspect-donor class is dropped (MET-2). Original rejected: accuracy. log_loss is the multiclass fallback.

CC (2026-10-21, Lennart): the metric is the log_loss fallback, as proposed; balanced accuracy, a threshold metric the paper did not choose, is not used.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_liver_elastography_fibrosis` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target is an ordered category, blood donor < hepatitis < fibrosis < cirrhosis.

**Assessment (AI, 2026-11-05):** marker `Class-dependent Recording`: donors and patients were recorded under different precision conventions (some lab values whole numbers in one group only), and ALP (alkaline phosphatase, a liver enzyme) is missing only for patients. Before the definition's rounding, bilirubin alone gives ROC AUC 0.881, and 0.954 with its number format. The definition rounds seven lab values and drops ALP. Noted in its curation comments; data unchanged.

CC (2026-11-10, Andrej): ALT dropped, recorded another way for most patients.
- **Evidence:** in the 57 patients with ALP recorded, ALT's median is 4.9 to 12.8 U/L by stage, below the donors' 23.1, while AST is raised; the 18 patients without ALP have 66 to 114 U/L, as chronic hepatitis C gives.
- **Why a drop:** a model would learn low ALT with high AST as a sign of disease, and the column cannot be repaired: neither the unit nor the method is stated. The six other rounded lab values stay rounded; ALT is no longer among them.

## Review

**Outcome:** added. The AI asks which time basis fits now that `CrossSectional` names a present state (2026-11-13).

**Main points:** `CrossSectional` instead of `ForcedIIDFromTemporal`?

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the person's liver state (blood donor, hepatitis, fibrosis or cirrhosis), read from the same blood sample, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
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

@article{hoffmann2018using,
  title={Using machine learning techniques to generate laboratory diagnostic pathways—a case study},
  author={Hoffmann, Georg and Bietenbeck, Andreas and Lichtinghagen, Ralf and Klawonn, Frank},
  journal={Journal of Laboratory and Precision Medicine},
  volume={3},
  number={6},
  year={2018},
  publisher={AME Publishing Company}
}
