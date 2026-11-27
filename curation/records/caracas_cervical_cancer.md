---
unique_name: caracas_cervical_cancer
name: Caracas Cervical Cancer
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- New IID
- 'Samples: Over Time'
- 'Time: Lost'
- Survey
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2017'
collection_period: 2012-2013
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

CC (2026-10-15, Lennart): No `Multi-target` tag: the four test results come from one work-up and the dataset predicts the biopsy alone.

**Assessment (AI, 2026-10-15):** The STD flags are one questionnaire question each and multi-label (9 patients have two or three types; `std_condylomatosis` is the parent of two subtypes, which `stds_number` counts twice), so they stay yes/no categories rather than one combined category. Impossible answers become missing (2 first intercourses after the current age, 2 STD diagnoses longer ago than the patient's age); the other contradictions (5 `dx_*` flags with `dx` 0, 7 STDs with no diagnosis counted) are not impossible and stay.

CC (2026-10-15, Lennart): Ship (review of the 2026-10-07 run): the STD flags stay one yes/no category each, impossible answers become missing.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (area under the ROC curve), Fernandes, Chicco, Cardoso & Fernandes 2018, 'Supervised deep learning embeddings for the prediction of cervical cancer diagnosis', PeerJ Computer Science 4:e154, doi:10.7717/peerj-cs.154 (abstract: 'top AUC ~0.69' for the biopsy); first use Fernandes, Cardoso & Fernandes, IbPRIA 2017, doi:10.1007/978-3-319-58838-4_27.

CC (2026-11-17, Andrej): Review issue 2, A, as implemented: Keep `Survey`: random 3-fold CV, 10 repeats (500 train / 250 test women), `ForcedIIDFromTemporal`.

CC (2026-11-17, Andrej): verdict ship (blind split walk).

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked in the blind split walk.

CC (2026-11-18, Andrej): the forced tag stays (Review issue 3, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A behavioural questionnaire under changing screening and vaccination policy gives no mechanism that time leaves unchanged.

CC (2026-11-27, Andrej): the declared metric (ROC AUC of the predicted probability of a positive biopsy, the source's) is checked and stays as declared. Ship as defined (review of 2026-11-27).

## Review

**Outcome:** added. A question on `CrossSectional` (2026-11-13) was withdrawn when the prototype was dropped.

**Main points:** Task gamer (blind, 2026-11-27): nothing gamed. Untuned LightGBM ROC AUC 0.608 (0.466 to 0.733 over 30 splits; a random column moves it by about 0.01); missing-value flags alone 0.565, format flags 0.515, row position 0.493, nearest-neighbour labels 0.512 to 0.554 (39 rows are exact feature copies, 94% with the same label). The prior-diagnosis `dx_*` items carry the weak signal (0.563 alone), which a deployed model has. Re-audited on 2026-11-27: nothing to decide. The three other screening results, near-copies of the biopsy target (Schiller correlates 0.73), are dropped and absent from the frame. The drop of the 108 patients who skipped the contraceptive question holds even adjusted for their younger age: 7.4 positive biopsies expected among them against 0 observed. The missingness left in the kept 750 rows carries no label signal (a random forest scores 0.669 on values alone and 0.665 with missing flags added), because the drop already removed its strong part. The STD time columns are filled only for women who report an STD, as self-reported history would be; whether any of those diagnoses were made at the screening visit itself cannot be told without a timestamp. Earlier: Nothing open: issue 1 was withdrawn on 2026-11-13; the collection type stays `Survey` with the same
random folds (issue 2, A, 2026-11-17); `ForcedIIDFromTemporal` stays (issue 3, A, 2026-11-18).

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: the result of her screening work-up, read from her answers at that work-up; the biopsy reports her condition then, not a later one, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Background:** the biopsy comes after the questionnaire, so the label is confirmed later, but it reports her condition at the questionnaire; the use case triages for a present disease and forecasts no later state. If you read the work-up as a forecast, A holds.
   * **Recurrence:** the use case meets the same woman again: cervical screening runs in rounds, and she answers the questionnaire at each. A cross-sectional task meets each unit once, so A: the forced tag stays.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** A. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

2. **Collection type: `Clinical Study` instead of `Survey`, with the same random folds?**

   * **Problem:**
     - the rule[^split-34] types patient data without dates as a clinical study when the patients arrived over time, and these are 750 women of one hospital's gynecology service (2012-2013, `Samples: Over Time`, `Time: Lost`) labelled by a biopsy diagnosis.
     - `Survey` covers rows a survey collected by its own questionnaire; here the features are questionnaire answers, but the label comes from the clinic's work-up.
     - Both types reach the same leaf, Random · `ForcedIIDFromTemporal` (later patients of the same clinic, no visit date, one row per woman), so only the record's type tag changes.
   * **The doubt:** Doubt: the rows are patients of one hospital's gynecology service with a biopsy outcome, closer to a Clinical Study (same clinic, later patients) than a survey; walking either type gives the same forced random leaf.
   * **What changes:** The record's `tags` swap `Survey` for `Clinical Study`; split_tree.md lists caracas_cervical_cancer under the Clinical Study branch's 'no, the order is lost' instead of the Survey branch; the rule[^split-34]'s case counts shift by one. `dataset.py` and the folds do not change.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: the tree's Survey branch lists this dataset under 'Does the interview order give the windows ... no -> ForcedFromTemporal step'; ignored.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Survey`: random 3-fold CV, 10 repeats (500 train / 250 test women), `ForcedIIDFromTemporal` (implemented) | No change. | The features are a risk questionnaire's answers, which `Survey` covers ('a clinical one too'). | The type does not fit the rule[^split-34]'s rule for undated patients who arrived over time, labelled by a diagnosis. |
     | B | Tag `Clinical Study`: the same random 3-fold CV, 10 repeats, `ForcedIIDFromTemporal` | The record's type tag becomes `Clinical Study`; `dataset.py`, the tag and the folds do not change; the tree's example moves from the Survey branch to the Clinical Study branch ('no, the order is lost'). | Matches the rule[^split-34]'s rule for undated patient data that arrived over time and a biopsy label from the clinic. | A record-only change; the type rules' examples and the tree's example lists need updating. |

   * **Recommendation:** B, because the rule[^split-34] types undated patients who arrived over time, labelled by a diagnosis, as a clinical study, and the split stays the same.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: change the record's type tag to `Clinical Study`, re-walk the tree from it and check whether the leaf changes; update the type rules' examples.

   [^split-34]: **SPLIT-34** (Should): Every record of a definition names how its source collected the rows with one **data collection type**, set at screening from the source and true whatever task is built on it.

   **Andrej (2026-11-17, ok):** as implemented.

   **Resolved (2026-11-17, Andrej):** A, as implemented: Keep `Survey`: random 3-fold CV, 10 repeats (500 train / 250 test women), `ForcedIIDFromTemporal`.

3. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost: UCI 383 carries no visit date and the record gives no usable file order; patients of one Caracas hospital, 2012-2013.
     - Use: A gynecology service ranks new women for colposcopy/biopsy from the questionnaire, years after 2012-13.
     - Mechanism: Self-reported sexual history, smoking and contraception proxy HPV exposure; the biopsy indication and the population's exposure shift with HPV vaccination and HPV-DNA screening, which time does change.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | Finlayson SG et al., 'The Clinician and Dataset Shift in Artificial Intelligence', NEJM 2021;385:283-286 (literature, cited from memory: check) | review of clinical model failures under practice, population and coding change | not flat (shift common) | clinical prediction deployed after collection |
     | WHO guideline for screening and treatment of cervical pre-cancer lesions, 2nd ed., 2021 (literature, cited from memory: check) | recommends HPV-DNA primary screening over cytology/VIA | changed rules | changes who is referred for biopsy and so the label's case mix |

   * **For a stationary use case:**
     - Two years of one service, a short span.
     - the biopsy reads her condition at the work-up.
   * **Against:**
     - questionnaire answers are behaviour, not physiology read by a fixed test.
     - screening rules and HPV vaccination change who reaches biopsy (changed rules/intake)
     - 108 women skipped a question with results looking unrecorded: recording varies.
     - only 55 positives; no dated comparison possible.
   * **Earlier views:**
     - Resolved 2026-11-13 (Andrej): CrossSectional withdrawn, forced tag stays.
     - CC 2026-11-17 (Andrej): Survey type kept, random 10x3 ForcedIIDFromTemporal checked.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | questionnaire answers are behaviour, not physiology read by a fixed test; screening rules and HPV vaccination change who reaches biopsy (changed rules/intake) |

   * **Recommendation:** A, a behavioural questionnaire under changing screening and vaccination policy gives no mechanism that time leaves unchanged. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A behavioural questionnaire under changing screening and vaccination policy gives no mechanism that time leaves unchanged.)

## Reference

@inproceedings{fernandes2017transfer,
  title={Transfer learning with partial observability applied to cervical cancer screening},
  author={Fernandes, Kelwin and Cardoso, Jaime S and Fernandes, Jessica},
  booktitle={Iberian conference on pattern recognition and image analysis},
  pages={243--250},
  year={2017},
  organization={Springer}
}
