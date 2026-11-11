---
unique_name: otto_group_product_classification_challenge
name: Otto-Group-Product-Classification-Challenge
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
tags:
- Larger IID Data
- 'Samples: One Moment'
collections:
- TabArena Reject
original_source: Kaggle
year: '2015'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/otto-group-product-classification-challenge/overview
notebook_path: datasets/beyond_iid/new_iid/otto_group_product_classification_challenge/otto_group_product_classification_challenge.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/otto_group_product_classification_challenge/dataset.py
source_row: 648
type_adapter_id: curation-record-v1
---

## Comments

CC: "Distinguish products in 10 groups based on 93 features. Competition not won through leaks, but test-time adaptation helped. In general seems like a good tabular data task for random splits. Kaggle licence forbids distribution, but as the data is on OpenML with 'Unknown' license. Although this is one of the best datasets we might not be able to use it."

**Assessment (AI, 2026-10-14):** 9 classes, not 10: the training file's `target` holds Class_1 to Class_9 (61,878 products) and the competition's sample submission has nine class columns.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source log_loss — multi-class logarithmic loss, the competition's evaluation metric (Kaggle evaluation page).

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, otto_group_product_classification_challenge:
- Issue 1, A: ship as defined. The declared split (random products) and the declared metric (multi-class log loss, the competition's) checked and kept.
- Issue 3, B: the record's collection fact is `Samples: One Moment` in place of `Samples: No Time Dimension`: the release is one 2015 extract of a live catalogue, and the 93 features are event counts as of that extract. No time or target fact.
- The `Time basis: Timeless` bullet of issue 2 (settled 2026-11-06) was missing from this working copy's definition and is now in the curation comments.

## Review

**Outcome:** added. The Otto Group's Kaggle competition of 2015: 61,878 products with 93 anonymised counts of events,
the target the product's main category, one of nine anonymised classes (the largest 26.1%, the smallest 3.1%), scored
by multi-class log loss, the competition's metric, on random products. The AI recommends shipping it as defined.
Reviewed without a review panel, from the gathered evidence: the record, a model run on the shipped data, the
BeyondArena results and checks on the shipped data. Validity: the definition keeps the competition's task and metric;
the features are anonymised (`Anonymized`); no duplicate rows and no column that copies another; the class-sorted row
order of Kaggle's file, which our experiments found readable through the row index of the shipped data, does not
reach v0.2, whose rows are shuffled. Value: on the one BeyondArena fold the methods spread from log loss 0.380 (TabFM)
and 0.394 (TabPFN-3.5) over 0.455 to 0.461 (tuned boosted trees) to 0.622 to 0.753 (linear model), against 1.950 for
the class shares. Quality: nothing open. Weighed: a large retailer's catalogue, its task and metric, and a wide spread
+, anonymised features -.

**Main points:** Shipped as defined (issue 1, resolved); the random split named `Timeless` (issue 2, resolved
2026-11-06); the release recorded as one extract, `Samples: One Moment` (issue 3, resolved 2026-11-09).

**Record judgment:** valid, and the record's fields match the definition. The use case is the host's: products that
its subsidiaries classify differently are assigned to their main category, so existing products and a random split
fit (fit `direct`). Lennart's note that Kaggle's rules forbid redistribution is a release-checklist item, not a
curation question. The metric review page proposes accuracy for this dataset; that question stays there.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing is open: the definition keeps the competition's task and metric, and no check found a leak, a copy or a
       spread problem in v0.2.
   * **Background:** what was checked: on the shipped data no duplicate feature row and no pair of columns that copy
     each other; the hidden-group probe sweep of 2026-10-14 found no hidden group. The one leak our experiments found
     belongs to the shipped BeyondArena file: Kaggle's `train.csv` is sorted by class and the shipped container kept
     that order, so a row index decodes the class (the benchmark's test side resets the index, so it did not score).
     The v0.2 definition orders rows by their content and shuffles them, so the index carries nothing there. The
     masked features are a known risk the `Anonymized` marker covers[^1a].
   * **Experiments:** BeyondArena, one fold, log loss: TabFM 0.380, TabPFN-3.5 0.394, LIMIX-2 0.394, tuned LightGBM
     0.455, tuned XGBoost 0.456, tuned CatBoost 0.461, linear model 0.622 (tuned) and 0.753 (default), class shares
     1.950. Residual boosting on TabPFN's out-of-fold predictions found no information left in the
     raw counts. The methods spread, so the dataset stays on value[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | nothing changes | a real catalogue task with the host's metric; a wide spread | anonymised features |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | less weight on anonymised Kaggle data | no defect found; one of the clearest separating tasks leaves |

   * **Recommendation:** A, nothing found that changes the task. **Decision:** ship (A), or retire (B)?

   **Resolved (2026-11-04, Andrej):** ship as defined (A); the declared split and metric checked and kept.

   [^1a]: **LEAK-32** (Should): masked or anonymised features that may hide a transform are a known risk of anonymised
     data, covered by its tag and the `Anonymized` marker: no action.
   [^1b]: **TP-3** (Must): if tuned methods spread, keep the dataset.

2. **Time basis: name the random split `Timeless`?**

   * **Problem:**
     - The rows are the products of one 2015 extract of Otto's catalogue: each product's 93 event counts as of the
       extract (over a window the host does not state) and its main category; no date, and the file's id order
       follows the class, not time.
     - The split is random, as the competition chose its products, and names no time basis yet; the use case assigns
       existing products to their main category.
     - A product's main category is a fixed property of the product, the case the `Timeless` prototype names; the
       `Snapshot` reading (fill in one extract) fits the use case too, but asks about a target time could move[^2a].
   * **Background:** the counts depend on how long a product has been listed, so the features carry the product's
     age, but the category does not change with it. Random products of one extract are the host's own split, and a
     cleanup of a catalogue meets the same products.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time basis (implemented) | as now | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random split, `Timeless` | as now; the tag and a `Time basis:` line naming the category as a fixed property | the first question settles it: the category is the same whenever it is read | says nothing of the extract, which the record's collection fact (issue 3) carries |
     | C | Random split, `Snapshot` | as now; the line names the 2015 extract | names the one moment the use case fills in | the prototype is for a target that time could move, and a category does not move |

   * **Recommendation:** B: the category is a property of the product; the extract belongs in the record (issue 3).
     **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Anonymized", "Timeless")` (the class adds `IID`),
   a curation bullet `- Time basis: Timeless: a product's main category is a fixed property of the product; the rows
   are one 2015 extract of the catalogue, its event counts as of the extract, and the competition chose its test
   products at random.`, no `splits_comment` change; `dataset check`. On C, `"Snapshot"` with the line naming the
   2015 extract and the counts as of it.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; a definition can name the
     use-case prototype it follows with a `Time basis:` line. `Timeless`: the target is a fixed property of the item,
     the same whenever it is measured; the split is random or grouped by item family. `Snapshot`: the use case only
     fills in a time the data covers (one census, one scrape), and the line names the moment.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (products listed after the 2015 extract, or a revised category tree); the split and `data_tags` are
   unchanged. The tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

   **Resolved (2026-11-11, Andrej):** the `Time basis: Timeless` bullet was missing from this working copy's
   definition and is now in `curation_comments`. `dataset check`: 0 errors, 0 warnings.

3. **Correct the record's collection facts: one extract, not `No Time Dimension`?**

   * **Problem:**
     - The release is one extract of a live catalogue: each product's 93 counts of events were read at one point in
       2015, so they depend on when the product was listed and when the extract was taken.
     - The record carries `Samples: No Time Dimension`, the fact for designed runs or a catalogue whose values do not
       depend on when an item was measured; `Samples: One Moment` names "one extract, census, scrape or exam
       round"[^3a].
     - Set `Samples: One Moment` in place of `Samples: No Time Dimension`?
   * **Effect on the task:** none on the split: one moment with the target known at it is IID data, and the category
     makes the definition `Timeless` (issue 2) either way. The fact tells a later reader that the counts are a
     snapshot, not properties.
   * **Unknown:** the window of the counts; Otto does not name the events.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Samples: No Time Dimension` (implemented) | as now | the category plays no part in time | misstates the features, which are counts as of an extract |
     | B | `Samples: One Moment` | the record's tag replaced | the source as it is: one extract of event counts | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, in the record's `tags`, `'Samples: No Time Dimension'` becomes `'Samples: One
   Moment'`; no time or target fact; `Andrej` added to `checked_by`.

   [^3a]: **SPLIT-32** (Should): the record describes the source by independent collection facts: `Samples: No Time
     Dimension` (designed runs, or a catalogue of properties where it plays no role when an item was measured),
     `Samples: One Moment` (one extract, census, scrape or exam round) or `Samples: Over Time`.

   **Resolved (2026-11-09, Andrej):** B: the record's `tags` carry `Samples: One Moment` in place of `Samples: No Time
   Dimension`; no time or target fact.

   **Andrej (2026-11-11, change):** Option B: Samples: One Moment.

   **Resolved (2026-11-11, Andrej):** B again; the record of this working copy still carried `Samples: No Time
   Dimension` and now carries `Samples: One Moment`.

## Reference

Benjamin Bossan, Josef Feigl, and Wendy Kan. Otto Group Product Classification Challenge. https://kaggle.com/competitions/otto-group-product-classification-challenge, 2015. Kaggle.
