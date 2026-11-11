---
unique_name: coffee_rating_prediction
name: Coffee_Data_CoffeeReview
checked_by:
- Lennart
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- No Good Target (yet)
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
collections:
- CARTE/TARTE
original_source: Website
year: '2023'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/hanifalirsyad/coffee-scrap-coffeereview
- https://www.coffeereview.com/
notebook_path: datasets/beyond_iid/temporal/coffee_rating_prediction/coffee_rating_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/coffee_rating_prediction/dataset.py
source_row: 481
type_adapter_id: curation-record-v1
---

## Comments

Just coffee reviews and features; est price needs adjustment and preprocessing, might have temporal drift due to review time; multiple descriptions, of which some are duplicated? All text as well which was used for parsing; kind of a well-defined task.

It seems the categories at the end make up the rating in total!

Could still be used for some kind of task, although it is unlikely it is close to any real tasks.

Maybe we could frame it as rating prediction only based on text, but this is closer to NLP than tabular based on the small amount of other information -> then it is a regression task, we could make it binary but that is wrong too.

CC (2026-07-27, Lennart): **Leak concern resolved -- verified against the curation notebook.** The category-score features (aroma, acid, body, flavor, aftertaste, with_milk) that sum to the rating are **dropped** in curation (`df.drop(columns=[... 'aroma','acid','body','flavor','aftertaste','with_milk' ...])`), along with desc_2/all_text (which leak award notes). Target is `rating` (regression); splits are temporal. So there is no circular leak in the shipped data -- `Yes` stands. Aligned `problem_type` -> Regression and `required_split` -> Temporal (NON-IID) to match the curated task.

CC (2026-10-01, Lennart): Leak audit: temporal splits are now 13 two-month windows (>= 50% train, 54-115 test rows each) instead of 5 six-month windows. Total test rows stay about 1,150 under any window size; monthly windows (26, some with 2 reviews) doubled the noise of a LightGBM vs Ridge comparison.

CC (2026-10-06, Lennart): Kept after the task-probe review: the `unstable` flag measures the noise of single windows, not the task. Over all 13 two-month windows (54-115 reviews each) random forest and LightGBM beat the train mean in every window (mean skill +0.25 and +0.27, standard error 0.03), and random forest beats the linear model in all 13 (by +0.20 on average); the standard deviation of about 0.1 per window is expected at this size.

CC (2026-10-21, Lennart): drop the `2ndTierData` tag ("we have this now with use case fit more or less"); the tag is retired from new definitions.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Scraped Kaggle dataset with no task, competition or paper; no metric defined.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `roast` (the README lists their levels).

CC (2026-11-11, Lennart): drop the 2 reviews of October 2023, the scrape's partial last month (cross-dataset item "What to do with a newest period that holds far fewer rows than the periods before it?", A).

**Assessment (AI, 2026-11-11):** October 2023 held 2 reviews against 24 to 65 a month in the rest of 2023; the 2-month windows now walk back from September 2023 instead of October.

CC (2026-11-11, Andrej): review marks applied (Review issues 1, 2, 4 and 5); 12 features to 9, the rows unchanged (2,367).

- Issue 1 (B): `desc_1` (the blind assessment) and `desc_3` (the bottom line) are dropped. The reviewer writes them with the score, one clause per sensory sub-score, and a roaster has neither before the review: ridge on their TF-IDF alone reached skill 0.71 (RMSE 0.861 against the training mean's 1.598) and beat every benchmark method, while the roaster's own information keeps skill 0.34 to 0.36. **Exception to LEAK-35 (2026-11-11, Andrej):** this dataset was the kept-text rule's case at R² 0.25 to 0.67; what sets it apart now is the measured 0.71, a text-only model ranking first, and a use case in which the roaster predicts before the review. The record loses `Free Text (Sentences)`: no long text is left.
- Issue 2 (B): the 606 prices of Taiwanese roasters written "NT $" were read as US dollars (the parser split "NT" off the currency); they are converted at the table's NTD rate (0.031) and the `NT_price` flag is dropped. The Taiwanese median price per gram falls from 1.98 to the others' range.
- Issue 4 (B): `Target: Varying Delay` added to the record's tags: the score comes at the review, weeks or months after the roaster's information, by a delay that differs per coffee.
- Issue 5 (`ok`): kept as the 9-feature roaster-side task. After the rebuild, check the spread of the benchmark methods and retire only if they tie there too.
- `dataset check` passes (0 errors, 0 warnings; the unknown-licence warning stays accepted).

## Review

**Outcome:** added. Kept after the changes of 2026-11-10 (issue 5, 2026-11-11). The data are a 2023 Kaggle
scrape of coffeereview.com: 2,369 coffees reviewed October 2018 to October 2023. The features are the roaster and its
location, the coffee's name and origin, the roast level, the Agtron roast-colour readings, the price per gram (NT$ now
converted) and the review month; the target is the overall score (82 to 98, mean 93). The six sub-scores, the review
notes and, since 2026-11-10, the reviewer's two passages are dropped. Validity: every feature exists before the review,
which is the roaster's use case. Value: untuned LightGBM reaches skill 0.36 on the 13 windows, but LightGBM and ridge
are within 0.007 RMSE of each other (issue 5). Weighed: a real roaster's question with signal +, features known before
the review +, a modest signal and no model spread shown yet -, a scrape without documentation and one rating service -.

**Main points:** kept without the reviewer's text (issue 5, A, 2026-11-11); check the methods' spread after the
rebuild. Issues 1, 2 and 4 were resolved on 2026-11-10 (text dropped, NT$ converted, `Target: Varying Delay`); issue 3
on 2026-11-06.

**Record judgment:** valid, ship after the changes. Lennart resolved the sub-score leak (2026-07-27), set the 13
two-month windows (2026-10-01) and kept the task after the `unstable` flag (2026-10-06; tree models beat the mean in
13 of 13 windows); the fit is approximate because one rating service stands for the quality a buyer meets
(2026-10-14). The record carries `No Good Target (yet)` next to `Yes`, as other records whose target the curation
defined. The licence is `None`: the review text is coffeereview.com's, scraped by the uploader (a note only).

**Issues for Andrej:**

1. **Drop the reviewer's two text passages, which a roaster does not have before the review?**

   * **Problem:**
     - `desc_1` (the blind assessment) and `desc_3` (the bottom line) are written by the reviewer together with the score, one clause per sensory sub-score that adds up to it.
     - The definition's own use case is a roaster predicting the score before the review, who "would have only its own description of the coffee", so these passages do not exist at its prediction point.
     - A word model on the two passages alone explains 71% of the score's variance and beats all 40 benchmark methods: drop them, keep them, or retire the dataset?
   * **Background:** the curation rules keep text written together with the label as the task when it does not map one
     to one onto the score, and this dataset is that rule's case (R² 0.25 to 0.67 then)[^1a]; otherwise a feature
     holds only what existed at the prediction point[^1b]. The six sub-scores were dropped on the same reasoning: they
     add up to the score. The passages describe those sub-scores in words.
   * **Effect on the task:** with the passages, the benchmark mostly measures how well a method reads a reviewer's
     verdict from his vocabulary, a text task where a bag-of-words model beats the tabular methods[^1c]; without them,
     it measures the roaster's question, from the roaster, origin, roast, roast colour, price and the coffee's name.
   * **Experiments:** on the 13 v0.2 windows (shipped container, same rows; Slurm job 1344880), RMSE against the
     training mean's 1.598: ridge on TF-IDF of the two passages 0.861 (skill 0.71, better than the mean in 13 of 13
     windows); the roaster's information (roaster, location, origin, roast, Agtron readings, price with NT$ converted,
     review month, words of the name) 1.268 with ridge (skill 0.34, 12 of 13) and 1.239 with LightGBM (skill 0.39,
     13 of 13). On the shipped splits a ridge regression on the passages ranks 1 of 41 (RMSE 0.805 against 0.985
     for the best benchmark method). Skill is 1 minus the ratio of mean squared errors, averaged over the windows.
   * **Consistency:** departs from Lennart's call that made this dataset the case of the kept-text rule. What sets it
     apart now: the measured share of the score the passages carry alone (0.71 against 0.25 to 0.67), a text-only
     model beating every benchmark method, and a real signal left without them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the passages (implemented) | no change | a text-and-table task; the earlier call | the score is mostly read from the reviewer's words; a bag-of-words model beats every tabular method |
     | B | Drop `desc_1` and `desc_3` | 10 features; the roaster's use case; fit stays approximate (one rating service) | features known before the review; skill 0.34 to 0.39 remains | loses the long text columns; reverses the kept-text case |
     | C | Retire | record `No (Retired)` | none found | loses a real roaster's task with signal |

   * **Recommendation:** B: it makes the features match the definition's own use case, and a real signal remains.
     **Decision:** keep the passages (A), drop them (B), or retire (C)?

   **Notes for the AI:** on B, add `desc_1` and `desc_3` to the drop list in `_clean`, remove them from `string`, update
   `known`, `changes` and `fit_reason` (the fit stays approximate: one rating service), drop the `Free Text
   (Sentences)` tag from the record if no long text remains, remove coffee as the case of the kept-text rule (or note
   the reversal there), re-run `dataset check` and the task probes, and add a `CC (2026-11-04, Andrej):` line.

   [^1a]: **LEAK-35** (Must): text written together with the label is the task when it does not map one to one onto
     the score; coffee_rating_prediction's review text is its case (R² 0.25 to 0.67, kept).
   [^1b]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away.
   [^1c]: **SEL-12** (Must): data from a non-tabular modality is out where modality-specific models are clearly better,
     judged per dataset.

   **Andrej (2026-11-11, change):** Option B: Drop desc_1 and desc_3.

   **Answer (AI, 2026-11-11):** applied, with one change left to the curation rules, which this run does not edit.
   This dataset is the case of the kept-text rule in three places, and the decision turns it into that rule's
   exception: the rule's text ("Cases: coffee_rating_prediction's review text (R^2 0.25 to 0.67; kept)", the keep-text
   rule in the leak checks), the reading probe's row on a long string column that scores close to the full model (the
   same case in the evidence reference), and the case row the exception needs ("the passages alone reach skill 0.71
   and a text-only model ranks 1 of 41; dropped"). The exception itself is written in the record and in the
   definition's notes.

   **Resolved (2026-11-10, Andrej):** B: `desc_1` and `desc_3` dropped in `_clean`; `known`, `changes` and `fit_reason`
   updated (fit stays approximate: one rating service, submission delay not stated). Written as an exception to the
   kept-text rule in the dataset's notes, the record and the rule's cases. The record loses `Free Text (Sentences)`: no
   long text is left. 9 features, 2,369 rows; `dataset check` passes. The task after the change is issue 5.

2. **Convert the prices in New Taiwan dollars?**

   * **Problem:**
     - 606 coffees (25.6%), all from roasters in Taiwan, list prices as "NT $", which the parser reads as US dollars, so `price_per_gram_in_usd` is in NT$ for them.
     - Their median price per gram is 33 times the others' (1.98 against 0.06), and the separate `NT_price` flag is the only hint.
   * **Background:** the definition's own exchange table has a rate for NTD (0.031), but the parser splits "NT" off
     before reading the currency, so the rate is never used. One unit per column[^2a].
   * **Experiments:** shipped container, same rows (Slurm job 1344880): NT rows 606, all located in Taiwan.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As is (implemented) | NT$ prices in the USD column, the `NT_price` flag kept | a tree can split on the flag | one column in two currencies; the flag also trips the constant-column warning |
     | B | Convert and drop the flag | NT$ prices times 0.031; `NT_price` dropped | one unit; the warning goes | none found |

   * **Recommendation:** B, the column's name says US dollars. **Decision:** as is (A) or convert (B)?

   **Notes for the AI:** on B, in `_clean` set `currency_raw` to `"NTD $"` where `NT_price` is "NT" before the
   `fx_to_usd` map, then drop `NT_price`; check that the median price per gram of the Taiwanese roasters falls to the
   others' range; re-run `dataset check`.

   [^2a]: **CLEAN-21** (Should): one unit and one scale per column.

   **Andrej (2026-11-11, change):** Option B: Convert and drop the flag.

   **Resolved (2026-11-10, Andrej):** B: the 606 "NT $" prices are converted at 0.031 and `NT_price` is dropped. The
   median price per gram of the Taiwanese roasters is now 0.062, against 0.059 for the others. The constant-column
   warning is gone; `dataset check` passes.

3. **Time basis: keep the 13 two-month windows with no gap, and write in `splits_comment` how the reviews arrive?**

   * **Problem:**
     - A coffee's score is given at its review and published with the review month, the split's time column, so the
       windows are cut at the time the label arrives, and every training label is published before its window starts.
     - The record carries `Samples: Over Time` and `Time: Dated` (the review month) and no target fact (issue 4); the
       split is temporal, so no use-case prototype applies: the roaster asks about a coffee not yet reviewed[^3a].
     - Keep the windows with no gap and write the arrival facts into the split comment?
   * **Background:**
     - No gap is needed for the training labels: a published review is known at once. What the windows cannot show is
       the time from a roaster's submission to the review, which the source does not state; a coffee submitted before its
       window began is scored by a model that saw reviews published after the submission.
     - Reviews of one month share their scoring: the month alone explains 8.3% of the score's variance (the year 1.1%),
       and some months are themed tastings (December 2021 and August 2023: 28% and 33% of the coffees from Antigua,
       Guatemala, scored 92.6 against 93.1 overall); whole two-month windows keep each month on one side of the cut.
     - Roasters recur across windows as a feature, their earlier scores known history; the newest month holds 2 reviews
       (the scrape stopped in October 2023), inside the newest window of 54.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | 13 two-month windows, no gap; the comment gives the refit cadence and the window size | no edit | why there is no gap and why months stay whole is in the review only |
     | B | Arrival in the split comment | as A, and the comment states the label's arrival, the month effect and the unstated submission delay | the reasons are where the split is | none found |
     | C | Monthly windows | 26 windows of one month | follows the fold count | already declined (2026-10-01): months of 2 to 10 reviews make each window's score noise |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, no `data_tags` change (a temporal split takes no time basis); append to `splits_comment`:
   "A score is published with its review month, so every training label is known when a window starts and no gap is
   needed; the time from a roaster's submission to the review is not stated. Reviews of one month share their scoring
   (the month explains 8% of the score's variance; some months are themed tastings), and whole two-month windows keep
   each month on one side."

   [^3a]: **SPLIT-32** (Should): how the data was collected, when each sample, feature and target come into existence,
     is information for the split; the record carries the source's collection facts, and a split that is not temporal
     names a prototype or a forced tag; a temporal split needs neither.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the arrival notes on temporal
   splits with one mark?" The arrival text (labels published with the review month, so no gap; whole months on one side)
   is appended to `splits_comment`. The split, its gap and `data_tags` are unchanged; a temporal split takes no
   time-basis tag.

4. **Correct the record's collection facts: add `Target: Varying Delay`?**

   * **Problem:**
     - A coffee, its roaster, origin, roast and price exist before it is reviewed, and the score comes at the review,
       weeks or months after a roaster submits it or Coffee Review buys it, a delay that differs from coffee to coffee.
     - The record has no target fact, which the tags reserve for a target that exists with the features; only the
       reviewer's two passages are written with the score, and issue 1 proposes to drop them[^4a].
     - Add `Target: Varying Delay`?
   * **Background:** the fact describes the source, whatever issue 1 decides: the passages are part of the review, the
     event that makes the label, not information the coffee had before it. `Target: Later` would need one shared date or
     a fixed window, and the reviews follow no schedule per coffee.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | As now (implemented) | no target fact | true of the reviewer's passages | reads as a label known with the coffee's information |
     | B | `Target: Varying Delay` | the tag added to the record's `tags` | states that the score comes after the roaster's information | the delay is not stated by the source, only implied |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, add `'Target: Varying Delay'` to the record's `tags`, `Andrej` to `checked_by`, a CC line.

   [^4a]: **SPLIT-32** (Should): `Target: Varying Delay` is a target after a delay that differs between samples;
     `Target: Later` one at a shared date or after a fixed window; no target tag when the target exists with the
     features.

   **Andrej (2026-11-11, change):** Option B: Target: Varying Delay.

   **Resolved (2026-11-10, Andrej):** B: `Target: Varying Delay` added to the record's `tags`, here and in PR #50's copy
   of the record.

5. **Still a valid and meaningful task without the reviewer's text: keep it or retire it?**

   * **Problem:**
     - After the changes, the roaster's own information predicts the score: untuned LightGBM reaches skill 0.36 and beats both the mean and the roaster's past mean score in 13 of 13 windows.
     - The signal is modest (RMSE 1.26 against the mean's 1.60, on scores of 82 to 98), and LightGBM and ridge are within 0.007 RMSE of each other (LightGBM is better in 7 of 13 windows).
     - Keep it as a small roaster-side task, or retire it?
   * **Background:** Andrej's verdict note (2026-11-10): "After applying the changes assess whether this is still a valid and meaningful prediction task and raise a new discussion item." Every feature now exists before the review, so the task fits the use case. A test window's roasters were seen in training for 77% of its coffees.
   * **Experiments:** rows from the edited definition (2,369 rows, 9 features), the 13 two-month windows (Slurm job 1376292). Skill is 1 minus MSE over the mean's MSE, averaged over the windows.

     | Model | RMSE | Skill | Windows better than the mean | Windows better than the roaster's mean |
     |---|---|---|---|---|
     | Training mean | 1.598 | 0 | | |
     | Roaster's past mean score (shrunk to the mean) | 1.436 | 0.18 | 12 | |
     | Ridge (one-hot, words of the name, numbers) | 1.266 | 0.35 | 11 | 11 |
     | LightGBM, untuned | 1.259 | 0.36 | 13 | 13 |
     | Ridge without roaster and location | 1.336 | 0.28 | 12 | 10 |
     | LightGBM without roaster and location | 1.350 | 0.27 | 13 | 10 |

   * **Effect on the task:** beyond the roaster's record, origin, roast, roast colour and price carry signal (skill 0.27 without the roaster). The two model families do not separate, so a spread among the benchmark methods is not yet shown. Before the change the spread came mostly from the text.
   * **Unknown:** the spread of the benchmark methods (TabPFN, tuned trees) on the new columns; it shows only after a rebuild.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | ship the 9-feature task after a rebuild | a real roaster's question; every feature known before the review; beats the roaster's past mean in 13 of 13 windows | modest signal; two simple models tie |
     | B | Retire | record `No (Retired)`, folder removed | no small, noisy task in the benchmark | loses a valid task with signal |

   * **Recommendation:** A: the task is valid and has signal beyond the roaster's history. Check the spread after the rebuild, and retire it only if the benchmark methods tie there too. **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** on B, record `No (Retired)` with the reason as a marker and a CC line, `claims release`, remove the folder and clear `v2_path`. Script and per-window table: `task.py` and `windows.csv` of the marks run of 2026-11-10.

   **Resolved (2026-11-11, Andrej):** A (`ok`): kept as the 9-feature roaster-side task, with a CC line in the record.
   After the rebuild, check the spread of the benchmark methods; retire only if they tie there too.

## Reference

Kaggle
