---
unique_name: kdd_cup_09_appetency
name: KDDCup09_appetency
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Anonymized
original_source: Other
year: '2009'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://kdd.org/kdd-cup/view/kdd-cup-2009/Data
- https://www.openml.org/search?type=data&id=1111
notebook_path: datasets/beyond_iid/old_iid/kdd_cup_09_appetency/kdd_cup_09_appetency.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/kdd_cup_09_appetency/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Marketing data to predict the propensity of customers to buy a product. Data has been already preselected, subsampled and maybe also preprocessed.

Potential issue: ? potential user groups

Lennart: No objection, but need to check data for IDs and maybe preprocess (remove some features) following the description

Andrej: Not in TabRepo, but seems like a good task

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (area under the ROC curve), per task; the ranking averaged churn, appetency and up-selling AUC (Guyon et al. 2009, Analysis of the KDD Cup 2009, JMLR W&CP 7; https://kdd.org/kdd-cup/view/kdd-cup-2009).

CC (2026-10-27, Lennart): marker Anonymized, from the AI review of PR #17: the definition carries the Anonymized data tag; Orange released Var1 to Var230 with hidden meanings and scrambled categories, so it cannot be checked that they were known before the purchase (LEAK-32 names this case).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after dropping seven columns that copy another (three relabelled categoricals, four numeric columns times a constant); the cup's appetency task and AUC are kept and methods spread (0.792 to 0.845). Priority 3: gap 0, use case 0, source 1, shape 1, risk -0.

CC (2026-11-06, Andrej): time basis `DelayedTarget` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on `DelayedTarget` issues of one-moment releases): one extract of Orange's customer datamart, the purchase label read as arriving after it (its window not stated). The random split is IID here, as every row shares the moment and the outcome window, so no test row is later than a training row. The `Time basis:` line is in the definition's notes; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, issue 3 (B): `Target: Later` added to the tags; appetency read as a purchase after the extract; window not stated by the source. Record fields set to the definition's values: `original_source` Other, `domain` business & marketing.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, issue 1 (B): the seven columns that copy another are dropped (CLEAN-5), 205 features remain: `Var220` and `Var222` relabel `Var198`, `Var214` relabels `Var200`; `Var156`, `Var91`, `Var128` and `Var105` are `Var66`, `Var71`, `Var88` and `Var104` times a constant. Keeping them gained no measurable score. The constant-column (presence flags) and pure-feature-value (segments without buyers) check warnings are accepted.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, issue 4 (B) and issue 5 (B): the cup's large training set, cleaned.
- Source switched to the large set: the same 50,000 customers and appetency labels (890 buyers), 15,000 features in place of 230; LightGBM ROC AUC 0.877 against 0.820 on the small set's columns.
- Dropped (CLEAN-5): 109 empty and 1,422 constant columns; 580 exact or scaled copies of an earlier column, the first of each group kept (the seven small-set copies of issue 1 fall in these groups); presence flags stay.
- Dropped as generated: `Var5963` (the variable of the cup's artificial toy target) and `Var11750`, both uniform without signal.
- 12,887 features remain (12,729 numeric, 158 categorical); the download takes the five large-set chunks and their labels from kdd.org.

## Review

**Outcome:** added. The KDD Cup 2009 data of the French telecom operator Orange, large version since 2026-11-11
(issue 4): 50,000 customers with 12,887 features whose names and categories are hidden (empty, constant, copied and
two generated columns dropped); until then the small version, 212 features. The target is appetency, whether the
customer bought a new product or service (1.8%), scored by ROC AUC as the cup scored each of its three tasks (its
ranking averaged churn, appetency and up-selling), on random customers. The AI recommends shipping it after dropping
seven columns that copy another column (issue 1). Reviewed without a review panel, from the gathered evidence: the
record, a model run on the TabArena v0.1 version of the same 50,000 customers, the BeyondArena results and
checks on the shipped data. Validity: the definition keeps one of the cup's three tasks with its metric; the features
are masked (`Anonymized`; the rule on masked features names this dataset), and the label has no stated window (fit
`approximate`); no duplicate rows, no exact copy across the split, and the row order carries nothing. Value: on four
BeyondArena folds the methods spread from ROC AUC 0.714 (random forest) and 0.792 to 0.819 (linear model) to 0.845
(LIMIX-2, TabPFN-3.5), with stable ranks (Kendall's W 0.97); the best single raw feature (`Var126`) reaches 0.750.
Quality: three categorical columns relabel another one and four numeric columns are another times a constant
(issue 1). Weighed: a large operator's own data and the cup's metric, and a clear spread +, masked features and an
undated label -.

**Main points:** Nothing open. The definition ships the cup's large set, cleaned: 12,887 features on the same 50,000
customers and label (issue 4, resolved 2026-11-11), the two generated uniform columns dropped (issue 5); the copies are
dropped (issue 1), the random split is a `DelayedTarget` (issue 2) and `Target: Later` is in the record (issue 3).

**Record judgment:** valid. The use case is the cup's: Orange's marketing decides which customers to approach with an
offer. The cup's other two labels (churn and up-selling of the same customers) are not shipped, so nothing of them
enters as a feature. Two bundle-check warnings have no acceptance yet; both describe the data as it is and can be
accepted: five columns hold one value or nothing (presence flags), and four category levels hold almost no buyer
(segments that do not buy). About 297 buyers fall in a test fold, so one fold's ROC AUC has a standard error near
0.02 (model run). Like the other undated snapshots of the benchmark, the split is not tagged as forced from
temporal (a note across datasets).

**Issues for Andrej:**

1. **Drop the seven columns that copy another column?**

   * **Problem:**
     - `Var220` and `Var222` are one-to-one relabellings of `Var198` (4,291 levels each), and `Var214` of `Var200`
       (15,415 levels, missing in the same 51% of rows).
     - `Var156`, `Var91`, `Var128` and `Var105` are `Var66`, `Var71`, `Var88` and `Var104` times 1.75, 2/3, 1.4 and
       2/3 in every filled row, with the same rows missing.
     - The definition ships all of them, so seven attributes enter twice: drop the copies, or keep them?
   * **Background:** checked on the shipped data, 50,000 rows: each pair takes one value of the other column for
     each of its values, both ways, and the numeric ratios are constant in all 694 to 1,129 filled rows. The
     model run found the categorical copies too: the AutoGluon preprocessing its models run behind drops them as
     duplicates before a model sees them. The cleaning rules drop exact copies of another column[^1a].
   * **Effect on the task:** none on what can be predicted; a copied column gives methods that sample or weigh
     columns a double vote for one attribute.
   * **Consistency:** follows credit_approval's issue 2 of this round (`A4`, a relabelled copy of `A5`, recommended
     drop) and boreal_postfire_lichen_biomass (one-to-one recodings dropped).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all (implemented) | 212 features as now | the file as Orange released it | seven attributes twice |
     | B | Drop the seven copies | 205 features; `Var198`, `Var200`, `Var66`, `Var71`, `Var88`, `Var104` keep the information | no copied column | the checksum changes; a rebuild |

   * **Recommendation:** B, an exact copy of another column goes. **Decision:** keep (A), or drop the copies (B)?

   **Notes for the AI:** on B, add `"Var214", "Var220", "Var222", "Var91", "Var105", "Var128", "Var156"` to the drop
   in `_clean`, remove the three categoricals from `_feature_types`, add a `curation_comments` bullet with the pairs
   and ratios; accept `dataset_constant_column` ("presence flags: one value or missing") and
   `dataset_pure_feature_value` ("segments without buyers; no column documentation to check, masked by the host");
   `dataset check`; CHANGELOG entry.

   [^1a]: **CLEAN-5** (Should): drop constant columns, all-missing columns and exact copies of another column.

   **Andrej (2026-11-11, discuss):** Does the ordering of the numeric level codes differ? They might still be different
   due to that, right?

   **Answer (AI, 2026-11-11):** for the three categoricals the order differs only under alphabetical codes, and keeping
   them does not measurably help any model; the double vote can hurt.
   - The categorical levels are hashed strings (`ka_ns41` → `1YVfGrO`). Sorted alphabetically, a copy's codes are
     unrelated to its source's (Spearman 0.00 to 0.02), so a tree on such codes gets other split points.
   - Under frequency codes, first-appearance codes, one-hot, target encoding or native categorical splits, copy and
     source are identical: same counts, same first rows, same missing rows.
   - The four numeric copies are their source times a positive constant: same order, same splits under any encoding.
   - Either alphabetical order is an artefact of the masking: neither the source's nor the copy's carries meaning.
   - Measured on the 50,000 rows, 5-fold CV × 3 repeats, paired folds. "Same order" replaces the three copies by
     exact duplicates of their source, so `all − same order` is the order effect and `same order − none` the double vote.

     | Model (encoding) | ROC AUC, all 212 | without 7 copies | all − without (SE) | order effect (SE) | double vote (SE) |
     |---|---|---|---|---|---|
     | LightGBM, alphabetical codes | 0.8221 | 0.8208 | +0.0013 (0.0017) | +0.0008 (0.0012) | +0.0005 (0.0013) |
     | Random forest, alphabetical codes | 0.7813 | 0.7826 | −0.0013 (0.0019) | +0.0014 (0.0015) | −0.0027 (0.0017) |
     | LightGBM, native categorical | 0.7728 | 0.7766 | −0.0038 (0.0012) | 0 (identical) | −0.0038 (0.0012) |

   - The order effect stays within one standard error for both code-based models; the double vote costs the native
     model 0.004 (three standard errors). The AutoGluon preprocessing behind most benchmark models drops the copies anyway.

     | | Option | Effect |
     |---|---|---|
     | A | Keep all 212 | the alternative split points of an arbitrary code order; a double vote for seven attributes |
     | B | Drop the seven copies (recommended) | 205 features, no information lost |

   **Recommendation:** B: the extra code order holds no measurable signal and no meaning. **Decision:** keep (A), or
   drop the copies (B)?


   **Andrej (2026-11-11, discuss):** Reply (B): Drop the seven copies (recommended).

   **Resolved (2026-11-11, Andrej):** B: `Var214`, `Var220`, `Var222`, `Var91`, `Var105`, `Var128` and `Var156` are
   dropped in `_clean` (205 features), the three categoricals left `_feature_types`, and a `curation_comments` bullet
   gives the pairs and ratios; the `dataset_constant_column` and `dataset_pure_feature_value` warnings are accepted.
   `dataset check` run: 0 errors, 0 warnings; the checksum changed, so the build is stale.

2. **Time basis: name the random split a `DelayedTarget`, though the purchase window is not stated?**

   * **Problem:**
     - Orange took one extract of its customer datamart to choose whom to approach with an offer, so every customer shares one moment, but neither the window of the purchase label nor the windows of the masked features are stated.
     - The record says `Samples: One Moment` without a target tag, which reads the label as existing with the features (issue 3), and the random split, the cup's own, carries no time basis.
     - Name it a `DelayedTarget` with the unknowns in its line, a `Snapshot`, or leave it untagged with a line saying why none fits?
   * **Background:** a delayed target needs its window closed for every row and every feature in existence at the
     moment[^2t1]; neither can be checked here, as the host masked and rescaled the features and states no window.
     The cup's own report frames the label in the future tense: the participants' "goal was to predict whether a
     customer will switch provider (churn), buy the main service (appetency) and/or buy additional extras
     (up-selling)" (Guyon et al., "Analysis of the KDD Cup 2009", JMLR W&CP 7, 2009, Sec. 2,
     http://proceedings.mlr.press/v7/guyon09/guyon09.pdf); it gives no window. When no prototype fits, the facts go to the curator rather than under the nearest tag; fields of a
     host's own competition whose timing no test can establish are kept with a note[^2t2].
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | claims nothing unverified | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `DelayedTarget` | `data_tags` gain `DelayedTarget`; the `Time basis:` line names the extract and says the label and feature windows are not stated | the reading the marketing use case needs; the line says what cannot be checked | rests on a reading, not a stated window |
     | C | Random, named `Snapshot` | as B with `Snapshot`, the label read as a status at the extract | none found | the cup asks whether a customer will buy, not whether it holds the service |
     | D | Random, a line without a tag | a `Time basis:` line saying why no prototype is named | names the gap without a tag | `dataset check` still notes the missing basis |

   * **Recommendation:** B: the use case fixes the reading, and the line keeps the unknowns visible. **Decision:** A, B,
     C or D?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Anonymized", "DelayedTarget")` and the curation
   bullet "- Time basis: DelayedTarget: one extract of Orange's customer datamart (date not stated, before mid-2009),
   100,000 customers resampled toward the labels and split at random by the host; the target, appetency, is read as a
   purchase of a new product or service after the scoring date, as the marketing use case needs. The label window and
   the features' windows are not stated and the features are masked, so neither the closed window nor the features'
   timing can be checked. Not tested: the next campaign."; on D the same text after "- Time basis: no prototype
   named:" without the tag; `dataset check`.

   [^2t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `DelayedTarget` has one prediction moment for all rows and the target after it; its line
     names the moment and the window, the window has closed for every row, and every feature existed at the moment.
     When none of the prototypes fits, the dataset and its use case go to the curator as an issue with the arrival
     facts found, rather than under the nearest tag.
   [^2t2]: **LEAK-38** (Should): fields that may be post-outcome, whose timing the source leaves undocumented and no
     test can establish, in data the data owner released for its own competition, stay with a note.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the `DelayedTarget` issues of
   one-moment releases with one mark?" The `Time basis: DelayedTarget:` bullet is in `curation_comments`; it says why
   the random split is IID here (every row shares the moment and the outcome window, so no test row is later than a
   training row) and ends with what the split cannot test (the next campaign). The split and `data_tags` are unchanged;
   the tag `DelayedTarget` enters `data_tags` once PR #50 is in the working copy. The line keeps the unstated label and
   feature windows in view.

3. **Correct the record's collection facts: add `Target: Later`?**

   * **Problem:**
     - The record carries `Samples: One Moment` and no target tag, which says the label exists with the features.
     - The cup's report asks whether a customer "will" buy the main service, a purchase after the scoring date, though it states no window.
     - Add `Target: Later`, or keep the record as it is?
   * **Background:** the target facts are `Target: Later` (after the features, at one shared date or after a fixed
     window), `Target: Varying Delay` and `Target: Revised Later`; no tag when the target exists with the
     features[^3t1]. No fact says that the timing is unknown.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | no target tag | claims no window the source does not state | reads the purchase as existing with the features |
     | B | Add `Target: Later` | the record's `tags` gain `Target: Later` | matches the purchase reading of issue 2's B | a reading, not a stated window |

   * **Recommendation:** B, with issue 2's B; A if issue 2 takes C. **Decision:** A or B?

   **Notes for the AI:** on B, add `Target: Later` to the record's `tags`, a `CC (<date>, Andrej):` line ("appetency
   read as a purchase after the extract; window not stated by the source"), and `Andrej` in `checked_by`.

   [^3t1]: **SPLIT-32** (Should): the record's collection facts: `Samples:` one of three; `Time:` for samples over
     time; `Target: Later` (after the features, at one shared date or after a fixed window), `Target: Varying Delay` or
     `Target: Revised Later`, and no target tag when the target exists with the features.

   **Resolved (2026-11-11, Andrej):** B: `Target: Later` added to the record's `tags` (also in the PR #50 worktree's
   copy of the record), with a CC line: appetency read as a purchase after the extract, its window not stated by the
   source.

4. **Ship the cup's large version (15,000 features) instead of the small one?**

   * **Problem:**
     - Andrej's note (2026-11-11): "The descriptions says this is the competitions small training set - if there is
       a larger why don't we use it?"
     - The large version holds the same 50,000 training customers with the same appetency labels (890 buyers),
       65 times as many features, and scores 0.06 ROC AUC higher with the same model.
     - The small set's 230 variables are a subset of the large set's 15,000, reshuffled; the large set was the cup's
       main track, and all winners scored best on it (Guyon et al. 2009, Sec. 2 and 7.1)[^4a]: keep the small set,
       or switch?
   * **Facts:** checked on the files of kdd.org (2026-11-11); run: LightGBM, the same settings on both, 5-fold CV × 3.

     | | Small (shipped) | Large |
     |---|---|---|
     | Training customers / appetency labels | 50,000 / published | the same 50,000, in another row order / published (890 buyers in both) |
     | Test set (50,000) labels | never published | never published |
     | Features | 230 (205 shipped) | 15,000 (14,740 numeric, 260 categorical); 13,419 not constant |
     | Download | 8 MB zip | 5 × 53 MB zips, 1.7 GB of text |
     | Licence | none stated; released "with no restriction of confidentiality ... for benchmark purpose" | the same |
     | ROC AUC, LightGBM | 0.820 (SE 0.002) | 0.877 (SE 0.003); its worst fold (0.856) beats the small set's best (0.832) |
     | Cup's best test AUC, appetency | | 0.885 (Table 2) |

   * **Background:** a newer or larger release of the same source is a version, and the curator decides which one
     enters; a model's feature cap is no reason against width[^4b]. The large set has not been through the
     column checks (empty, constant and copied columns; issue 1 found seven copies among 230).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the small set (implemented) | 50,000 × 205 as now | checked; light | drops most of the information Orange released: 0.06 AUC |
     | B | Switch to the large set | the same customers and label, about 13,400 features after the column checks; a new `/add-dataset` pass and a rebuild | the cup's main data; the full signal | heavy (1.7 GB raw); many methods must select features |
     | C | Ship both | two definitions | both widths | one task twice[^4b] |

   * **Recommendation:** B: same rows and label, and the small set loses a measured 0.06 AUC. **Decision:** A, B or C?

   **Notes for the AI:** on B, point `_load_raw` at the five `orange_large_train.data.chunk*.zip` files (chunk 1 has
   the header) and `orange_large_train_appetency.labels`, numeric `Var1`-`Var14740`, categorical
   `Var14741`-`Var15000`; drop empty, constant and copied columns (CLEAN-5) with the copy test of issue 1; update the
   download text, `row`, `known` and the first `curation_comments` bullet; `dataset check`, leak and task probes;
   CHANGELOG.

   [^4a]: Guyon et al., "Analysis of the KDD Cup 2009", JMLR W&CP 7, 2009,
     http://proceedings.mlr.press/v7/guyon09/guyon09.pdf: Sec. 2 ("the same data entries, the 230 variables of the
     small version being just a subset of the 15,000 variables of the large version"; "no restriction of
     confidentiality ... for benchmark purpose"); Sec. 7.1 ("All the winning teams scored best on the large
     dataset"). Files: https://kdd.org/kdd-cup/view/kdd-cup-2009/Data.
   [^4b]: **PROV-6** (Must): versions or cuts of one dataset are duplicates unless they add a distinct task.
     **CLEAN-22** (Must): width itself is no reason to drop columns.

   **Andrej (2026-11-11, discuss):** Measure how much is gained by using more features first. Also, is it even
   reasonable to have this amount of features or are they artificial to test models feature selection capabilities?

   **Answer (AI, 2026-11-11):** the gain is real and sits in a few hundred columns: the 230 large-set columns a training
   fold ranks highest score 0.875, all 13,419 score 0.877. The columns are Orange's own constructed customer
   variables, not added probes; only two are generated noise.
   - Gain, same 50,000 customers, LightGBM 5-fold CV × 3 (logistic regression: the first 5 folds); every selection
     uses the training fold only; difference paired by fold against the small set's columns.

     | Columns of the large file | Number | LightGBM ROC AUC | vs small set (SE) | Logistic regression |
     |---|---|---|---|---|
     | the small set's columns, found in the large file | 199 | 0.820 | 0 | 0.801 |
     | random 230 | 230 | 0.675 | −0.145 (0.009) | |
     | top 230 by training-fold importance | 230 | 0.875 | +0.055 (0.002) | 0.841 |
     | top 500 | 500 | 0.875 | +0.055 (0.003) | |
     | top 1,000 | 1,000 | 0.876 | +0.056 (0.002) | 0.833 |
     | top 2,000 | 2,000 | 0.878 | +0.058 (0.002) | 0.817 |
     | all but the small set's columns | 13,220 | 0.859 | +0.039 (0.003) | |
     | all not constant | 13,419 | 0.877 | +0.057 (0.002) | 0.807 |

   - The small set's columns score the same inside the large file (0.820), so the gain comes from other columns, not
     from a different preparation.
   - A random 230 scores 0.675: most columns carry little, and Orange's small set was an informed pick, not a random
     one. LightGBM gives about 2,530 columns any split per fold.
   - A linear model gains from 230 selected columns (+0.040) and loses most of it on all 13,419 (0.807): the full width
     rewards methods that select or shrink columns.
   - Real or artificial, checked on the 50,000 rows:

     | Check | Large set |
     |---|---|
     | Source | Orange's marketing platform built 20,000 variables from a datamart of about ten tables with its feature construction language; constant ones and identifiers removed, 15,000 kept, each numeric one times a random factor (Guyon et al. 2009, Sec. 4)[^4c]; the FAQ names no probe or random columns |
     | Empty / one value | 109 / 1,472 |
     | Exact or scaled copies of another column | 544 (in 389 groups) |
     | Distinct columns with values | 12,875 |
     | Single-column ROC AUC above the best of the same columns against a shuffled label (0.526) | 1,135 (shuffled label: 0); 72 at 0.60 or more; best 0.768 (`Var9045`) |
     | Shape | median 99.7% zeros; half the numeric columns are counts (all values multiples of one step) |
     | Generated columns | `Var5963`, uniform on 0-2 with no signal (0.511): the variable of the cup's toy target, "generated by an artificial stochastic process" (FAQ)[^4c]; `Var11750`, uniform on 0-9 (0.501) |

   - The width is the form Orange's platform gives every marketing task: sparse aggregate counts, many redundant, about
     one in ten carrying signal. Apart from the two uniform columns, nothing points to columns added to test feature
     selection. The shipped small set holds a third uniform column, `Var57` (issue 5).
   - Selecting columns before shipping would use the labels of every customer, test folds included, so a narrower
     large version cannot be cut cleanly; width alone is no reason to drop columns[^4d].

     | | Option | Effect |
     |---|---|---|
     | A | Keep the small set | 205 columns; 0.057 ROC AUC of Orange's released information not available |
     | B | Switch to the large set, cleaned (recommended) | about 12,870 columns: empty, constant, the 544 copies and the two uniform columns dropped; the full signal; a heavy download and a test of column selection, as Orange's own use case is |
     | C | Small set plus the top large columns | 230 to 2,000 columns ranked on all 50,000 labels: the selection sees the test folds |

   **Recommendation:** B: the same customers and label, real columns, a measured +0.057, and the width is the task's
   real form. **Decision:** A, B or C?


   [^4c]: Guyon et al., "Analysis of the KDD Cup 2009", JMLR W&CP 7, 2009,
     http://proceedings.mlr.press/v7/guyon09/guyon09.pdf, Sec. 4 ("the feature construction language was used to
     generate 20,000 features ... After discarding constant features and removing customer identifiers, we narrowed
     down the feature set to 15,000 variables"; "multiplying each continuous variable by a random factor"), Sec. 5
     (toy target: "one single predictive continuous variable (V5963) uniformly distributed on the interval [0, 2.0]").
     FAQ, https://kdd.org/kdd-cup/view/kdd-cup-2009/FAQ: "The toy target is generated by an artificial stochastic
     process"; "The small dataset is a downsized version of the large one: same examples, a subset of the features."
   [^4d]: **CLEAN-22** (Must): columns leave for what they are (a leak, an identifier, a copy), never for how many
     there are; width is no reason to propose a narrower version.

   **Andrej (2026-11-11, discuss):** Reply (B): Switch to the large set, cleaned (recommended).

   **Resolved (2026-11-11, Andrej):** B: `_load_raw` reads the five `orange_large_train.data.chunk*.zip` files and
   `orange_large_train_appetency.labels` (copied to the warehouse; download text updated). `_clean` drops 109 empty and
   1,422 constant columns, 580 exact or scaled copies of an earlier column (the first of each group stays: the 544
   found, 24 more scaled copies the float32 check had missed, 12 presence flags missing in the same rows as another),
   and the two generated columns of issue 5. The 50 presence flags (one value or missing) stay, as in the small set;
   the seven copies of issue 1 fall into the copy groups. 12,887 features (12,729 numeric, 158 categorical); the same
   50,000 customers, label, random split and ROC AUC. `row`, `known`, the download text and `curation_comments`
   updated. `dataset check`: 0 errors, 0 warnings (the duplicate and pure-value checks skip at this width; forced,
   they find no duplicate column or row, and the accepted presence flags and buyer-free segments). The build is stale.
   Leak probe (untuned LightGBM, 3 splits), no leak sign:

   | Probe | ROC AUC |
   |---|---|
   | all 12,887 features | 0.851 |
   | best feature alone (`Var9045`) | 0.771 |
   | without `Var9045` | 0.844 |
   | number format alone | 0.769 (decimals mark a nonzero value of a rescaled count) |
   | exact feature copies across the split | 0.0% of test rows |


5. **Drop the generated uniform columns (`Var57`; on a switch also `Var5963` and `Var11750`)?**

   * **Problem:**
     - The shipped small set's `Var57` is uniform on 0 to 7 (25,614 distinct values in 50,000 rows, none missing), has
       no match among the large set's 15,000 columns, and scores 0.503 ROC AUC alone.
     - The large set holds two more such columns: `Var5963` (uniform on 0 to 2, the variable of the cup's generated toy
       target, 0.511) and `Var11750` (uniform on 0 to 9, 0.501).
     - They describe no customer: drop them, or keep the file as released?
   * **Background:** the cup's report and FAQ say the small set's columns are a subset of the large set's, so a small
     column without a match was added; the toy target was "generated by an artificial stochastic process" on
     `V5963`[^5a]. The deciles of all three are evenly spaced (Kolmogorov-Smirnov distance to uniform 0.004 for the
     two large columns; the next column 0.16). Columns leave for what they are[^5b].
   * **Effect on the task:** none on the signal; a noise column a method has to learn to ignore.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | `Var57` stays; on a switch the other two too | the file as released | columns generated by the host, not customer data |
     | B | Drop them | `Var57` leaves the small set (204 columns); on a switch `Var5963` and `Var11750` leave too | only customer variables | a rebuild; the checksum changes |

   * **Recommendation:** B: generated noise is no property of a customer. **Decision:** A or B?

   **Notes for the AI:** on B, add `"Var57"` to the drop in `_clean` with a `curation_comments` bullet ("`Var57` is
   uniform on 0-7 and matches no column of the large set: a column the host generated, ROC AUC 0.503 alone");
   `dataset check`; CHANGELOG. If issue 4 takes B, drop `Var5963` and `Var11750` in the large definition instead.

   [^5a]: Guyon et al., "Analysis of the KDD Cup 2009", JMLR W&CP 7, 2009,
     http://proceedings.mlr.press/v7/guyon09/guyon09.pdf, Sec. 2 and 5; FAQ,
     https://kdd.org/kdd-cup/view/kdd-cup-2009/FAQ ("Are the variables in the small dataset a subset of those in the
     large dataset? Yes."; "The toy target is generated by an artificial stochastic process").
   [^5b]: **CLEAN-22** (Must): columns leave for what they are (a leak, an identifier, a copy, the measurement that
     defines the label), never for how many there are.

   **Resolved (2026-11-11, Andrej):** B, with issue 4's B: `Var5963` (uniform on 0-2, the variable of the cup's toy
   target) and `Var11750` (uniform on 0-9) are dropped in the large definition (`GENERATED_COLUMNS`), with a
   `curation_comments` bullet. `Var57` belongs to the small set only and has no match in the large set, so it leaves
   with the switch.
