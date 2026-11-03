# avito_demand_prediction

**Outcome:** added as `avito_demand_prediction_1m`. The AI recommends shipping it; only issue 1 (whether Avito's
undocumented deal score counts as an observed outcome) can turn it to `No`. The data are Avito's Kaggle competition of
2018: 1,503,324 classified ads posted on Avito from 15 to 28 March 2017, in 28 Russian regions without Moscow or St
Petersburg. The target is `deal_probability`, Avito's 0-1 estimate that the ad led to a deal (0 for 64.8%). The task:
when a seller posts an ad, Avito estimates the demand it will meet. The split is temporal by posting date: three
two-day windows without a gap, each trained on the ads before it (a random million when there are more). The metric
is RMSE, the competition's own. The review panel's changes are made: the seller id `user_id` ships as a categorical,
and the notes carry the corrected numbers; the rows, the split and the metric are as drafted.

Validity:
* SEL-3 is open (issue 1). The label is an undocumented Avito score, not a counted sale, but it follows what happened
  to each ad after posting: identical reposts get different labels in 859 of the 983 groups with a positive ad. So it
  is neither a clustering label nor a rule computed from the ad's columns (SEL-4, SEL-5 do not apply).
* USE-1 holds for half of the use case: how much interest a seller should expect. The other half, advice on what to
  change, needs causal effects and is not tested; the text now says so. USE-5 and USE-8: fit approximate for the
  label, as diabetes_3.
* USE-6 and LEAK-37 hold: Avito's categories and photo class are made at posting, and nothing suggests the photo class
  learned from these labels. LEAK-10 holds with a note: edits after posting are rare where the text shows them.
* USE-10 and LEAK-34 were broken by the draft, which dropped the seller id on a number the claim audit refuted. Fixed:
  `user_id` ships as a categorical, as ieee_fraud_detection's `uid`. The hidden-group probe now shows the seller as
  the one entity across the split (29% of the test ads), which is the task (SPLIT-13).
* SPLIT-6, SPLIT-9, SPLIT-14 and LEAK-24 hold. SPLIT-10 (a gap of about the label's delay before each test window) is
  departed from. There is no gap, because any gap of the delay leaves a window with under half the ads for training
  (SPLIT-14). This is an exception for you to confirm (issue 2). It is the third for this reason, after
  alfa_battle_2_0_task_2 and lending_club; you declined the SPLIT-10 amendment on 2026-11-02, so it is an
  exception of its own.

Value: TP-2, a real signal (untuned LightGBM removes 25-26% of the squared error of predicting the training mean, on 3
of 3 windows, and is 0.037 ahead of a linear model on that scale); MET-4, RMSE kept; SEL-12 holds (the Russian text adds
+0.016 R^2 and ships as text).

Quality: the price codes 0 and 1 explained (CLEAN-10); the six copied pairs kept as distinct ads of different sellers
(LEAK-19, LEAK-20); `image_top_1` stored as integer codes (CLEAN-14); the zeros warning accepted under your zero
policy (2026-10-30).

Weighed: the host's own data and named task +; 1.5M dated ads of mixed types +; undocumented label -; less context than
Avito has (no competing ads, one photo class, no promotion) -.

For you: issue 1 (SEL-3, a validity call on the label), issue 2 (confirm the no-gap exception).

**Main points:** Does Avito's undocumented deal score meet SEL-3 (an observed outcome or an expert annotation)? The AI
says yes, on the repost fact (issue 1). Confirm training without a gap before each test window (issue 2), an exception
of its own.

**Issues for Andrej:**

1. **Record Avito's deal score as an observed outcome or an expert annotation?**

   * **Problem:**
     - The target has to be an observed outcome or an expert annotation[^1a].
     - Avito calls `deal_probability` "the likelihood that an ad actually sold something" and never said how it is
       computed.
     - So the label either meets the rule for a stated reason, or the rule changes, or the dataset goes.
   * **Background:** the welcome thread asks three times how it is computed and gets no answer
     (https://www.kaggle.com/competitions/avito-demand-prediction/discussion/55299). Your `Yes` of 2026-10-30 was given
     on a record whose Assessment calls the label "not an observed outcome (criterion 3)" and which still carries
     `No Good Target (yet)`. The rule is a Must and has no exceptions.
   * **Sources:** Avito cannot observe a deal: deals happen off the platform, and its seller team uses contacts as the
     proxy (https://habr.com/ru/articles/879680).
   * **Experiments:** what the label is, measured on the 1.5M ads: in services (4.3% of the ads) its 22 values are all
     fractions k/n with n at most 8, like a share of a few counted events. In goods it sits on category-level values:
     0.80323 on 46,668 personal-item ads, 0.76786 on 26,474 electronics ads; 41.8% of the positive goods ads share a
     value with 1,000 ads or more. It is decided per ad, after posting: 4,490 groups of identical reposts (same seller,
     title, description, price, category and town) hold 983 groups with a positive ad. In 859 of them (87%) the copies
     differ: a zero beside a positive in 698, two or more positive values in 198. In the 511 two-ad groups with one zero
     and one positive, the zero falls on the later copy in only 46%, so it does not look like Avito blocking the
     duplicate (circumstantial evidence[^1b]: a seller may delete the first copy, which is also an event after posting).
   * **Effect on the task:** models are scored against Avito's assessment of each ad's outcome, on Avito's scale per
     category; part of the error is learning that scale. If Avito's score is a calibrated probability, ranking models
     by RMSE against it gives the same order as scoring them against the real deals[^1c]. That supports the metric,
     not the target.
   * **Panel:** the advocate reads the label as the host's annotation of each ad's outcome, the best target this actor
     can have, since the use case decides how a scope rule is read[^1d]. The critic accepts the repost fact, notes
     that a few category levels make it weaker than an agency's rating, and leaves the call to you.
   * **Consistency:** corporate_issuer_credit_rating, the rebuild Lennart asked for (record of 2026-10-16, no folder
     yet), takes an agency's own rating as the target; diabetes_3 and alfa_battle_2_0_task_2 settle the approximate
     fit[^1e], not whether the target is an observed outcome.
   * **Unknown:** Avito's definition of the score would settle it; no page found gives it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The rule is met (implemented) | label shipped as released, fit approximate; the record states the reason and loses the marker `No Good Target (yet)` | the repost fact shows a label decided per ad after posting; nothing changes in the dataset | the reading becomes the precedent for every label a host scores and publishes as ground truth |
     | B | Amend the rule | the label rule amended to admit a host's published assessment of an outcome it cannot observe; the dataset as in A | the case is named in the rule | reaches other datasets |
     | C | Retire | verdict `No` with `No Good Target / Scientific Discovery`; the dataset leaves | the label rule stays as written | the host's own data and named task are lost |

   * **Recommendation:** A: identical reposts carry different labels, so the label is decided per ad after posting.
     **Decision:** A, B or C?

   **Notes for the AI:** the definition implements A already: the target bullet and the target decision carry the
   services rates, the goods levels and the repost check, and the target bullet and `fit_reason` say that Avito cannot
   observe a deal. The record keeps `No Good Target (yet)` until the curator decides. On A, record SEL-3 as met with
   the reason "the host's record of each ad's outcome after posting, on its published 0-1 scale; identical reposts
   carry different labels in 859 of 983 groups with a positive ad", and remove the marker. On B, amend SEL-3 in
   `selection.md`. On C, the verdict `No` with `No Good Target / Scientific Discovery`.

   [^1a]: **SEL-3** (Must): the dataset is published for a predictive task, and the target is an observed outcome or
     an expert annotation; a table without a genuine predictive target is out.
   [^1b]: **EV-6** (Should): say which evidence is proof (a test that could have refuted the claim) and which is
     circumstantial.
   [^1c]: **MET-8** (Should): for the same goal prefer the probabilities; with no metric fixed by the source, the
     fallback for regression is `rmse`.
   [^1d]: **SEL-2** (Must): when a scope rule seems to exclude a dataset, check how the prediction is made in
     practice, and let the use case decide (Lennart, 2026-10-15).
   [^1e]: **USE-5** (Must): a label from a named publication whose construction is undocumented may ship with
     `fit="approximate"` and a note naming the gap. **USE-8** (Must): write how closely the data mirrors the use
     case, its fit (direct, approximate or none).

2. **Confirm the split without a gap?**

   * **Problem:**
     - When a label arrives some time after its row, a model refit when a window starts knows only the labels that have
       arrived, so a gap of about the label's delay goes between training and test[^2a].
     - The split has none, so the newest training days carry labels Avito would not yet have.
   * **Label delay:** undocumented, but long. Of the competition's supplementary ads activated on 15 March, 96.0% were
     still listed more than 3 days later and 89.4% on 28 March (`periods_train.csv`; being listed is not a deal, and
     these are not the training ads). The third-place team left a 4-day gap
     (https://www.kaggle.com/competitions/avito-demand-prediction/discussion/59885).
   * **Why no gap:** the release covers 14 days, and a temporal task needs three windows, each trained on at least
     half the ads[^2b]. Any gap of 4 days or more breaks that at every window width:

     | Windows | Gap | Training share, newest to oldest |
     |---|---|---|
     | 2 days | none | 85%, 71%, 57% |
     | 2 days | 1 day | 77%, 64%, 49.97% |
     | 1 day | 3 days | 71%, 64%, 57% |
     | 1 day | 4 days | 64%, 57%, 49.97% |

   * **Experiments:** at equal training size a 3-day gap moves RMSE by 0.0002 (the draft's 0.0008-0.0012 was mostly
     smaller training sets), so the scores here are optimistic by about 0.0002 RMSE against a model that skips the 3
     newest days (about 0.001 on the Value line's scale, where LightGBM and a linear model differ by 0.037). The rule
     against training labels unknown at the prediction point holds[^2c]: reposts can move a window by 0.00006 RMSE at
     most, and the seller's labels act as a lasting trait (an 8-day history ending 4 days before the window keeps 91% of
     the gain of the most recent 8 days).
   * **Consistency:** the departure serves the training floor, as the principles settle the tension between unmatured
     training labels and the training floor[^2d]. It is the third exception of this reason after
     alfa_battle_2_0_task_2 (gap 0 although a partial gap was possible[^2e]) and lending_club. You declined the
     amendment of the gap rule on 2026-11-02 (issue 4), so this is an exception of its own. ames_housing and
     perth_house_prices depart for another reason and do not count.
   * **Panel:** the advocate and the critic both recommend it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No gap (implemented) | three two-day windows without a gap, recorded as an exception with the delay and the shares above | meets the training floor; windows cover six weekdays; costs about 0.0002 RMSE of optimism | the newest training days carry labels Avito would not yet have |
     | B | One-day windows with a 3-day gap | three one-day windows, each with a 3-day gap after its training days | meets the training floor | covers 3 days of a delay of weeks (the partial gap passed over for alfa); three weekdays instead of six; costs 0.0001-0.0009 RMSE on the same days |

   * **Recommendation:** A: it meets the training floor over six weekdays for about 0.0002 RMSE of optimism.
     **Decision:** A or B?

   **Notes for the AI:** A is written in the definition as an exception to SPLIT-10 that serves SPLIT-14, with the
   delay and the training shares above. SPLIT-9 holds (the reposts and the seller history above).

   [^2a]: **SPLIT-10** (Should; applies SPLIT-9): when a label is known only some time after its row, train on the
     rows whose outcome is known by the window's start, with a gap of about the label's delay between train and test.
   [^2b]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50%
     of the data.
   [^2c]: **SPLIT-9** (Must): a training row whose label is not yet known at the prediction point must not be in
     train.
   [^2d]: principles.md, Tensions, "Unmatured training labels against the training floor": SPLIT-9 is met by removing
     the measurable shortcut; the diffuse rest falls under SPLIT-10 (Should), departed from for SPLIT-14's 50% floor
     and recorded as an exception (alfa_battle_2_0_task_2, lending_club; Lennart, 2026-10-21).
   [^2e]: Lennart, 2026-10-26, alfa_battle_2_0_task_2: gap 0 although a partial gap was possible.

   **Andrej (2026-11-03, change):** Moved to 2nd tier

   **Andrej (2026-11-03, dataset note):** Since this is recsys/CTR, we move it to 2nd tier for now. Also, add the click
   prediction tag

   **Resolved (2026-11-03, Andrej):** not shipped for now: the record is `TBD -> 2nd Tier` with the marker
   `Out-of-scope Task (CTR/RecSys/Ranking)` (the vocabulary has no click-prediction tag; this marker is its closest
   entry), its `v2_path` cleared and its claim released; the folder leaves the working copy (copies of its last files in
   the run folder of 2026-11-03, `avito_retired/`). Issue 1 (ok) and the metric mark (change) stand with the move.

**Review panel:** ship after changes (mediator). Claim audit: 50 claims, 34 hold, 12 refuted (all fixed: the
seller drop by shipping `user_id`, the rest in the text), 3 untested (whether Avito's models learned from deals, the
label's delay, the competition's test balance), 1 superseded. Blind review: would include with changes (text declared
as text, the date out of the features, `image_top_1` categorical, the dropped rows documented); all but the date are
in the definition, and the date stays a feature as the house template has it. Debate: agreed on the rows, the split,
the metric, shipping `user_id` and the text fixes; disputed: whether Avito's score meets SEL-3 (issue 1); the advocate
first kept the seller drop for SPLIT-9 and conceded once the seller's value was measured as a lasting trait; the
no-gap exception and its amendment go to you (issues 2 and 4).

<details><summary>Mediator</summary>

**Mediator: avito_demand_prediction_1m (mediator, 2026-11-01)**

**Recommendation: ship after changes.** The advocate and the critic end on the same verdict: keep the rows, the split and the metric, ship the raw seller id, fix the text. Two calls stay with Andrej: the SEL-3 reading of Avito's deal score (issue 1), and confirming the no-gap exception, which brings the SPLIT-10 amendment due (issue 2). My two checks, the repost recount and the equal-length seller histories, ran on the raw file.

```text
Verdict: ship after changes.
Validity: SEL-3 for Andrej to record (issue 1): an undocumented Avito score, but one that follows each ad's fate after
  posting (identical reposts differ in 859 of the 983 groups with a positive ad), so SEL-4 and SEL-5 do not apply;
  USE-1 holds for the expectation half (text narrowed); USE-5/USE-8 approximate (diabetes_3); USE-6/LEAK-37 hold
  (Avito's codes made at posting); LEAK-10 holds with a note (edits rare); USE-10/LEAK-34 triggered by the dropped
  seller id, fixed (raw `user_id` shipped as a categorical; CLEAN-6 bars an encoding of our own); SPLIT-6, SPLIT-14,
  LEAK-24 hold; SPLIT-9 holds (no measurable shortcut); SPLIT-10 departed, exception serving SPLIT-14 (a delay of
  weeks; third of the floor reason, issue 2).
Value: TP-2 real signal (skill 0.252-0.256 over the mean, 3 of 3 windows); MET-2, MET-3, MET-4 hold (RMSE, Kaggle's
  metric); SEL-12 holds (text +0.016 R^2 at the shipped size).
Quality: CLEAN-10 note (price codes 0 and 1); LEAK-19/LEAK-20 pairs kept as distinct ads; EV-2 corrections.
Weighed: the host's own data and named task +; 1.5M dated ads of mixed types +; undocumented label -; context narrower
  than Avito's (no competing ads, one photo class, no promotion) -.
For the curator: issue 1 (SEL-3: record the reading, amend, or No); issue 2 (confirm the SPLIT-10 exception and the
  amendment it brings due).
```

**Agreed facts** (both sides and the evidence reports; numbers reproduced where marked)

- Frame: 1,503,324 ads of 15-28 March 2017 after the 100 ads dated 29 March to 7 April are dropped (84% positive against 35%). Three two-day windows (27-28, 25-26, 23-24 March); train sides 1M, 1M and 861,064; tests 227,748, 210,617 and 203,895.
- Target: 64.8% zeros, 0.67% ones, 18,407 values. Services (64,385 ads, 4.3%): 22 values, all k/n with n at most 8. Goods: category-level values (0.80323 on 46,668 personal-item ads, 0.76786 on 26,474 electronics ads). Avito never documented it (thread 55299: three questions, no answer). Avito cannot observe a deal; its seller team uses contacts as the proxy (Habr 879680).
- No leak found: leak probe best single column `param_1` (R^2 0.150 of 0.185); exact feature copies across the split 0.05% of test ads (0.0% with the text); hidden-group probe in temporal mode: no hits; same-seller reposts move a window's RMSE by 0.00006 at most (oracle bound); daily target mean flat at 0.136-0.141 (LEAK-24).
- Edits after posting are rare where the text shows them: 2 titles marked sold, 43 descriptions saying "уже продано", 741 ads (0.05%) with a price-lowered phrase (mean label 0.123 against 0.139); missing shares of photo, description and price flat over the 14 days.
- `image_top_1`: Spearman 0.41 with the mean target, -0.09 against the residual after the category mean; worth 0.0028 RMSE, less than `price` (0.0049).
- Seller: 30.9% of the newest window's test ads come from a seller in the shipped train side. As LightGBM's native category the id adds 0.00023 RMSE (builder); as a past-mean encoding 0.0011-0.0015 overall and 0.0039-0.0046 on known sellers (claim audit). Positive after a positive same-seller ad 1-3 days earlier 43.5%, 4-12 days earlier 41.5% (alfa: 95.1% against 2.3%).
- Equal-length seller histories (reproduced by the mediator): on the 18.7% of test ads whose seller has training ads in both, structured columns 0.18856, the 8 days just before 0.18365, the 8 days ending 4 days before 0.18407. Older labels keep 91% of the gain; label age is worth 0.00042 RMSE on those ads.
- Delay: of the supplementary ads activated on 15 March, 96.0% were still listed more than 3 days later, 92.6% more than 7 days, 89.4% on 28 March (`periods_train.csv`; display is not a deal, and these are not the train ads). The third-place team's gap was 4 days, not 3 (59885).
- Training-pool share by window width and gap (reproduced from the daily counts): two-day windows, no gap 85/71/57%, 1-day gap 77/64/49.97%, 3-day gap 64/49.97/35%; one-day windows, 3-day gap 71/64/57%, 4-day gap 64/57/49.97%. At equal training size a 3-day gap costs 0.00024 and 0.00020 RMSE (paired SE 0.00004-0.00005); the draft's 0.0008-0.0012 is mostly training size.
- Population: 28 regions, none of Moscow, Moscow Oblast, St Petersburg or Leningrad Oblast; 9 parent categories, no jobs.
- Value: skill over the mean 0.255, 0.256, 0.252; LightGBM over linear 0.037; text adds +0.016 R^2 at the shipped size (alone 0.206); RMSE is Kaggle's `evaluationMetric`.
- The claim audit's 12 refuted claims are slips in the text; none changes the rows, the split or the metric.

**Changes to make now** (no decision needed)

1. Ship `user_id` as a categorical: take it out of `drop_columns` and add it to `categorical`. Rule: USE-10 and LEAK-34 (Must) make a known seller's history legitimate; CLEAN-3 (Should) keeps a meaningful id, and the draft's departure rested on a refuted number; CLEAN-6 (Must) bars building the past-mean column ourselves. Precedents: ieee_fraud_detection `uid`, african_credit_scoring_challenge `customer_id`, brazilian_ecommerce `seller_id`, all categoricals. Update `task_summary.known` and `changes`, the ids bullet, the seller bullet (both measurements above and the equal-length result), and `splits_comment` ("the seller id is not a feature" goes). Re-run the dataset check and the hidden-group probe; the seller will show as an entity across the split, which is the task (SPLIT-13, USE-10).
2. Accept `task_target_value_dominant` with its reason: Avito's own zeros, not a cap or placeholder (the maximum is 1.0); the zero policy (Andrej, 2026-10-30, question 2), as across this batch.
3. `splits_comment` and the end of `fit_reason` (SPLIT-10, SPLIT-12; EV-2): replace the no-gap reasons with the delay proxy, the floor shares by window width, the 4-day citation, "two days is the longest window that keeps three windows above half the ads; the competition's 15-21-day horizon cannot be repeated in 14 days", and the gap's cost at equal training size. Write the exception as one to SPLIT-10 that serves SPLIT-14, pending issue 2 (the register reads other wordings as an exception to a Must).
4. A SPLIT-9 sentence in `splits_comment`: reposts 0.47-0.60% of a window with an oracle bound of 0.00006 RMSE; the seller signal is a lasting trait (43.5% against 41.5%; older histories keep 91% of the gain); no measurable shortcut, as lending_club records.
5. Target bullet, the target Decision and `fit_reason` (USE-5, USE-8): the services rates, the goods levels, the repost result (859 of 983; a zero beside a positive in 698; two or more positive values in 198; the zero is the later copy in 46% of two-ad groups) and Avito's statement that it cannot observe a deal. The SEL-3 line waits for issue 1.
6. `use_case`: the benchmark tests how much interest to expect, not advice on what to change (an ad without a price scores 0.215 against 0.135). `row`: the 28 regions without the two capitals and their oblasts, no jobs category. `fit_reason`: the narrowed context and that the label is a deal assessment, not views or contacts (USE-1, USE-8).
7. Prediction-point bullet: the edit counts; `image_top_1` note: the residual Spearman and the 0.0028 RMSE, and that under USE-6 a code made at posting stays an input (LEAK-10 second clause, LEAK-37, LEAK-27).
8. EV-2 corrections: `task_summary.split` (the oldest window trains on all 861,064 ads); the competition test is 12-18 April plus 65 ads on 19-20 April; the 54 town names stand for 2 to 7 regions (43, 8, 2, 1); 13 of 731,655 pairs (7 after the drop); reposts 86, 126 and 87 per two-day window; the text numbers at the shipped size; drop the 56531 quote (6.2% measured, not 30%); the late ads look posted later (33 of 39 checkable), the drop stands; the version comment 228k; the price counts on the frame 85,360 and 4,645; the hidden-group probe ran (temporal, no hits).
9. CLEAN-10: explain the price codes 0 (4,645 ads, mean 0.35) and 1 (3,696, mean 0.27) as the seller's "free" or "contact me", kept as codes. LEAK-19/LEAK-20: replace "negligible" with the fact that each of the 6 pairs comes from two sellers; with `user_id` shipped they are no longer copies. Optional: `image_top_1` as integer labels (CLEAN-14, cosmetic).

**Changes that need the curator**

1. SEL-3 (Must, P2): record the reading of Avito's deal score. Both sides ask for it; the rules leave open whether a host's published assessment of an outcome it cannot observe directly is an "observed outcome". Best evidence for "holds" (advocate): the label follows each ad's fate after posting (twins differ in 87% of groups with a positive ad, pairs correlate 0.47 against 0.135 for random pairs of the same category and town); the actor cannot observe deals, so for it a deal label is always an estimate (SEL-2: let the use case decide); the host published it as the ground truth of a named task (corporate_issuer_credit_rating). Best evidence against (critic): in goods the label sits on a few category levels (41.8% of positive goods ads on a value shared by 1,000 ads or more), so it is a scored scale, not a count; the record's own Assessment called it "not an observed outcome (criterion 3)"; Andrej's `Yes` gave no SEL-3 reason. What would settle it: Avito's definition of the score (none found). Options: (a) SEL-3 holds with the repost fact, marker `No Good Target (yet)` removed; (b) amend SEL-3; (c) `No` with `No Good Target / Scientific Discovery`. I recommend (a).
2. SPLIT-10 (Should): confirm the exception (no gap, serving SPLIT-14) and the amendment proposal. Rules and facts settle the remedy (the Tensions row on unmatured labels), but an exception carries the curator's name, and this is the third of its reason (alfa_battle_2_0_task_2, lending_club), so principles.md asks for the consistency check and an amendment. I recommend the precedent checker's option (a) and its amendment text.

**Disputed points**

1. *`user_id`: drop, raw id, or a seller-history encoding.* The advocate first dropped it for SPLIT-9 (Must); the critic kept it under USE-10 and LEAK-34 (Must) and CLEAN-3 (Should). Not a conflict: SPLIT-9 asks to remove a measurable shortcut, and the reproduced equal-length test shows the seller's value is a trait (label age 0.00042 RMSE on 18.7% of test ads, about 0.0001 at window level), so SPLIT-9 holds with the id as without it. That leaves CLEAN-3 with no fact for a departure, so its default holds; the advocate conceded. Between the raw id and an encoding, CLEAN-6 (Must) decides: we never build target or mean encodings. LEAK-34 and USE-10 make the history legitimate without requiring us to build it, so the raw id meets all three rules, and each method encodes it on its own train side. A single column could not hold the encoding anyway: one frame serves all three windows, and a 28 March ad's history would include 27 March, a test day of the same window. Remedy: fix the definition (ship the raw id).
2. *The repost counts: 87% against 161 of 983.* Both are right; they count different parts of one partition (the mediator's recount): of the 983 twin groups with a positive ad, 124 hold one value (12.6%) and 859 differ (87.4%): 698 have a zero beside a positive (71.0%) and 161 several positive values without a zero (16.4%). Counting the 37 groups that have a zero and two positive values, 198 (20.1%) hold two or more positive values; that, not 161, is the count for "different positive values". The critic's caveat (a zero may be Avito blocking a duplicate) does not hold up: in the 511 two-ad groups with one zero and one positive, the zero falls on the later copy (by `item_seq_number`) in 46.4% (47.2% of the 464 same-day pairs), where blocking would put it on the later copy. This is circumstantial (EV-6): a seller may delete the first copy, which is still an event after posting. The fact to record: "identical reposts carry different labels in 859 of the 983 groups with a positive ad (87%): a zero beside a positive in 698, two or more positive values in 198."
3. *Third or sixth SPLIT-10 exception.* The claim audit counts six by rule ID; the precedent checker counts three of the floor reason. principles.md counts "the same reason", so this is the third of the floor reason (alfa, lending); ames_housing and perth_house_prices have another reason with its own open proposal.
4. *One-day windows with a 3-day gap* (claim audit). It meets SPLIT-14 and looks like it meets SPLIT-10, but SPLIT-10 asks for a gap of about the delay, and 3 days is a small part of a delay of weeks, the partial gap Lennart passed over for alfa (gap 0, 2026-10-26). It costs 0.0001-0.0009 RMSE and gives up the longest window that fits (SPLIT-12, Should). It goes to issue 2 as the alternative, not as the recommendation.
5. *The blind reviewer's preparation fixes.* Text as strings, `image_top_1` categorical and the late-ad drop are already in the definition; dropping `activation_date` as a feature is not adopted (the house template keeps the time column as a datetime feature, as kick does). Both sides agree.

**Consistency with precedent** (precedent checker's report)

| Decision | Precedent | Follows? |
|---|---|---|
| `user_id` shipped as a categorical | ieee_fraud_detection `uid` (Lennart, 2026-10-01; labels carried forward, LEAK-34), african_credit_scoring_challenge, brazilian_ecommerce | follows (option (b) of prompt 2). african's training labels were settled and avito's are not, but the measured age effect is small, so no fact sets avito apart |
| No gap, an exception serving SPLIT-14 | alfa_battle_2_0_task_2 (gap 0 against a delay of up to a year), lending_club | follows on the delay fact (option (a) of prompt 1); the third of the reason, so the amendment is due. Apart from house_sales and the trip-time family (short delays, gaps set): here any gap of the delay breaks the floor at every window width |
| Target as released, fit approximate | diabetes_3, alfa_battle_2_0_task_2 (USE-5, USE-8) | follows. SEL-3: corporate_issuer_credit_rating supports keeping; valuation's AI screening reads the other way but is no precedent (unverified, not accepted) |
| Zeros as released, warning accepted | Andrej, 2026-10-30, question 2; this batch | follows |
| The six copied pairs kept | african_credit_scoring_challenge, brazilian_ecommerce (distinct entities); huntprohibited dropped its copies without a seller key | follows the first two; the seller key sets it apart from huntprohibited |
| Reposts kept | huntprohibited ("the label is per ad") | follows |
| 100 late ads dropped | none | first of its kind (LEAK-10, LEAK-7); could become a Cases row |
| Two-day windows instead of the competition's split | aeolus_1m, acquire_valued_shoppers_challenge (SPLIT-19 departed for SPLIT-14) | follows |
| RMSE | zillow_prize (MET-4) | follows |
| Russian text as strings | huntprohibited_1m, mercari_price_suggestion | follows |

</details>

<details><summary>Claim audit</summary>

**Claim audit: avito_demand_prediction_1m (claim-auditor, 2026-11-01)**

**Verdict:** 50 claims tested. 34 hold, 12 refuted (most are small slips; two carry a decision), 3 untested, 1 superseded. The metric holds: Kaggle's own metadata names RMSE (MET-4), it is computable per row on every test fold with no extra inputs (MET-2), and the target ships on its 0-1 scale (MET-3). The two refuted claims that carry a decision:
(1) "`user_id` adds little". When the seller id is encoded as the seller's past mean (from the train side only), it is worth 5-6 times what the note says, and the actor (Avito) knows the seller when the ad is posted (USE-10, LEAK-34).
(2) "a 3-day gap breaks the 50% training floor". This is true only for the two-day windows we chose ourselves. With one-day windows, a 3-day gap still keeps 57% or more of the data on every training side (SPLIT-10, SPLIT-12, SPLIT-14).

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "How likely is a new classified ad ... to end in a deal, on Avito's own 0-1 score?" | task_summary.question | read against the target | holds | the target is Avito's 0-1 score, and the question says so | USE-5 |
| 2 | Use-case quote "Avito can inform sellers on how to best optimize their listing ..." | task_summary.use_case; bullet 1 | fetched the GitHub mirror (raw.githubusercontent.com/wangz19/Avito_Demand_Prediction_Challenge, README line 2) | holds | quoted word for word. The same paragraph lists "similar ads already posted" and "historical demand for similar ads in similar contexts" among the inputs | USE-1, EV-2 |
| 3 | One ad of 15-28 March 2017, 1.5M ads | task_summary.row | rebuilt the frame with `dataset_io.from_definition` | holds | 1,503,324 rows, 2017-03-15 to 2017-03-28 | - |
| 4 | "65% of the ads have 0" | task_summary.predicted | count | holds | 64.83% | - |
| 5 | Everything the model sees is in the ad when it is posted | task_summary.known, fit_reason, bullet 1 | (a) words meaning "sold" or "reserved" in the text against the label; (b) `item_seq_number` checked as a counter set at posting | holds as far as it can be tested | "продан(о/а)" appears in 2 titles; the 1,640 descriptions with it have mean label 0.120 against 0.139 overall, so the text does not mark the outcome. "уже продан": 43 ads. No seller has the same `item_seq_number` twice, and it runs against the date in 7 of 731,614 consecutive pairs | LEAK-10, USE-6 |
| 6 | "training is a random million of the ads posted before it" | task_summary.split | `make_splits` | refuted (wording) | the oldest window trains on all 861,064 earlier ads, not a random million (the splits_comment gets this right) | writing |
| 7 | Ids and the 100 late ads are dropped | task_summary.changes | frame columns and row count | holds | 15 columns, no ids; 1,503,424 - 100 rows | - |
| 8 | Fit approximate: the label's construction and delay are undocumented | fit, fit_reason | read thread 55299 and the data page | holds | none of the pages read gives a construction; three people ask in 55299 and get no answer from the hosts | USE-5, USE-8 |
| 9 | 1,503,424 ads; the test file (12-20 April) has no labels | bullet intro | counted the raw file; downloaded test.csv | holds | 508,438 test ads dated 2017-04-12 to 04-20 (64 on the 19th, 1 on the 20th). Two public EDA notebooks give 12-18 and 12-19 April | PROV |
| 10 | Target quote (data page via SRK's notebook), Wendy Kan's quote, "asks three times" | bullet Target | read the saved notebook and thread | holds | the target quote is word for word in simple-exploration-baseline-notebook-avito. RyanCaldwell, Validation and dd MlStart ask and get no host answer. Wendy Kan's line (2018-04-28) is word for word | EV-2 |
| 11 | 64.8% zeros, 0.67% ones, 18,407 values, 0.80323 on 46,683 ads, 88.0% / 80.7% in one parent category | bullet Target, Decision 1 | recount, and a calibration (EV-9) | holds | every number reproduces. 6,520 of the 18,406 positive values occur on a single ad, so they sit in one category trivially. Among values shared by at least 100 ads, 76.4% still occur in one parent category, so the reading as the output of a scoring step survives | EV-9 |
| 12 | Zeros policy (Andrej, 2026-10-30, question 2) | bullet on zeros | found the source | holds | the triage summary of the zero-inflated review, question 2: "We don't care. ..." | principles, who decides |
| 13 | 100 ads dated 29 March to 7 April; 84% against 35% positive; mean 0.65 against 0.14 | bullet on late ads, Decision 1 | recount | holds | 100 ads; 0.840 against 0.352; 0.653 against 0.139 | - |
| 14 | "their date was probably set by a later event" | same bullet | each late ad's `item_seq_number` against the same seller's ads dated up to 28 March | refuted in part (it was an inference) | 39 late ads have a seller with earlier ads. 33 of them carry a higher sequence number than all of that seller's March ads, so they were posted later, as dated. 6 carry a lower one, so they look re-dated | EV-2 |
| 15 | `image` missing exactly where `image_top_1` is (112,588 ads) | bullet on ids | crosstab | holds | 112,588 ads miss both; none miss only one | - |
| 16 | Seller counts: 61,949 ads (27%) from a seller with an ad at least 3 days earlier, 39,982 from one with an ad in the 3 days before | seller bullet | recount with the raw ids | holds | 61,949 (27.2%) and 39,982 | - |
| 17 | "`user_id` as a feature adds little" (0.22210 against 0.22187) | seller bullet; builder report | `user_id` encoded as the seller's smoothed past mean label and ad count, from the train side only (what a method that encodes the id would learn). Random 1M train sample as shipped; the two newest windows; untuned LightGBM | refuted in size | overall RMSE 0.22230 to 0.22084 (-0.00146) and 0.22739 to 0.22632 (-0.00107). On ads of known sellers (31% and 26% of the test ads): 0.20166 to 0.19710 and 0.21241 to 0.20852 (-0.0046 and -0.0039). That is 5-6 times the builder's -0.00023, which used LightGBM's built-in categorical handling on an id with about 300k levels. The 3rd-place write-up (59885): "For the time series approach, user_id likelihoods gave a good boost" | USE-10, LEAK-34, USE-6, CLEAN-6, EV-6 |
| 18 | Column counts: 28 regions, 1,804 towns, 1,733 names, 54 names on 31,770 ads; 9 / 47 / 371 / 271 / 1,219 / 3 / 3,062 values | column bullet | recount | holds | every count reproduces | - |
| 19 | The 54 names "stand for towns in two or three regions" | column bullet | regions per name | refuted (detail) | 43 names are in two regions, 8 in three, 2 in four and 1 in seven (Октябрьский) | - |
| 20 | `item_seq_number` rises with the date "in all but 10 of 731,655" pairs | column bullet | recount | refuted (detail) | 13 of 731,655 pairs on the raw file, 7 of 731,614 after the drop | - |
| 21 | Data-page quotes on the categories and on `image_top_1` | note on Avito's model | read the saved notebook | holds | word for word | EV-2 |
| 22 | Avito's image model was not fit on deal outcomes | same note | - | untested | no document says either way; cannot be verified | USE-6, LEAK-27 |
| 23 | Price: 85,362 missing (mean label 0.215 against 0.135), 4,646 at 0, 158 above 1e8, 5 above 1e9 "most in real estate" | price bullet | recount | holds | every number reproduces; of the 5 above 1e9, 3 are real estate and 2 business | - |
| 24 | Quote from 56531: "About 30% of the top 10% deal_prob percentile are missing prices" | price bullet | share of top-decile ads with no price (top decile: label at least 0.7376, 10.4% of the ads) | refuted on the data | 6.2% of top-decile ads have no price, and 11.3% of the ads without a price are in the top decile | EV-2 (a measurement beats a thread) |
| 25 | 2 exact copies; 4 rows conflict | duplicates bullet | `duplicated()` on the frame | holds | 2 exact copies; 4 conflicting pairs (the bundle check counts 4 rows) | - |
| 26 | Reposts are 0.69% of the ads; "40 to 55 ads per test window (0.04%)" | duplicates bullet | repost key counted per two-day window | holds / refuted (detail) | 10,422 ads (0.69%). Per window: 86, 126 and 87 ads (0.04-0.06%); the builder's 42-43 were per one-day window | LEAK-18 |
| 27 | Top solutions built seller aggregates; the display periods run past the posting date | supplementary bullet | read 59871 and 59885 | holds (aggregates) / untested (period dates) | 59871: "average number of days the each advertisement had been active", built from periods_*. The periods files were not downloaded | CLEAN-19 |
| 28 | Text: R^2 0.185 to 0.191, title alone 0.095, "on the first window"; the text "adds a little" | text bullet | leak-probe JSON; out-of-fold ridge on a TF-IDF of title and description (1-2 grams, 200k terms), fed to LightGBM; newest window, shipped 1M train sample | holds in direction; refuted on size and window | the probe numbers are the mean of all three windows at 50k training rows. At the shipped size: structured columns 0.22230 (R^2 0.257), with the text ridge 0.21986 (R^2 0.273); the text ridge alone reaches R^2 0.206 | EV-8, SEL-12 |
| 29 | 218 descriptions with a phone number, 4 with an e-mail | text bullet | re-read small_checks | holds | - | - |
| 30 | Metric RMSE (Kaggle API `evaluationMetric`) | Metric bullet; `Metric.source` | Kaggle API `competitions_list`, 2026-11-01 | holds | evaluationMetric = "Root Mean Squared Error". Thread 55299 agrees (anokas: "Using RMSE for probabilities however is a weird choice") | MET-4, MET-11 |
| 31 | Terms quote ("only for the purposes of the Competition") | Terms bullet | - | untested | the rules page renders only with JavaScript; terms are never evidence (EV-4) | EV-4 |
| 32 | The newest three two-day windows; train 1M / 1M / 861,064 (57%) | splits_comment, version_comment | `make_splits` | holds | test 227,748 / 210,617 / 203,895 ads; earlier ads available 1,275,576 / 1,064,959 / 861,064. Training ends the day before each window; no overlap; the samples are nested (drawn from one random order) | SPLIT-11, SPLIT-14 |
| 33 | The competition's test starts 15 days after the last training day | splits_comment | test.csv dates | holds | 28 March to 12 April | - |
| 34 | Six of the seven weekdays; posting volume and the share of zeros vary by weekday | splits_comment | weekday table | holds | 23 March (Thursday) to 28 March (Tuesday). Zero share Saturday 0.659, Sunday 0.669, other days 0.640-0.646; ads over the two weeks: 196k on Fridays, 230k on Mondays | - |
| 35 | "a gap of three days (the third-place team's scaled copy of the competition's gap, discussion 59885)" | splits_comment | read 59885 | refuted (detail) | the team trains on days 0-5 and validates on days 10-13: "days six through nine were excluded", which is 4 days. For likelihoods: "we always applied a gap of 4 days" | EV-2 |
| 36 | A 3-day gap "leaves the oldest window under half of the ads (SPLIT-14)" | splits_comment | training-side share under other window widths | holds for two-day windows, but the floor does not force it | two-day windows with a 3-day gap: 525,526 ads (35.0%); even a 1-day gap leaves only 751,251 (49.97%). One-day windows (26, 27, 28 March) with a 3-day gap: 861,064 / 967,608 / 1,064,959 (57-71%), so SPLIT-14 holds. With a 4-day gap: 751,251 (49.97%) | SPLIT-10, SPLIT-12, SPLIT-14 |
| 37 | A gap costs 0.0008-0.0012 RMSE, and 0.0013-0.0019 on 6% of the ads | splits_comment | re-read the builder's gap output | holds | 0.00085 / 0.00124; 0.00133 / 0.00186; 6.1% / 6.4%. Measured on all earlier ads (1.28M / 1.06M), not on the shipped 1M sample | EV-8 |
| 38 | Decision 2: the target is stable over the posting days | Decision 2 | recounted the by-day table | holds as far as it can be tested | daily means 0.1362-0.1414; 28 March 0.1390 / 0.6398 zeros against 15 March 0.1401 / 0.6432. There is one release, so LEAK-24's two-download test cannot be run | LEAK-24 |
| 39 | The metric is computable per row with no inputs | Metric | `data_foundry.v2.metrics.scorer` on each fold | holds | predicting the training mean: 0.25786 / 0.26363 / 0.25857 (the scorer equals the formula computed by hand); predicting 0: 0.29227 / 0.29844 / 0.29336. No scoring columns are needed | MET-2 |
| 40 | The metric means the same as in the competition, on the same scale | Metric | `target_transform`; zero share per test window | holds; the competition's test balance is untested | identity transform, 0-1 scale. Zero share per test window 0.643 / 0.664 / 0.643 against 0.648 overall. The competition never released its test labels | MET-2, MET-3 |
| 41 | `task_target_value_dominant` proposed for acceptance | bundle check; builder report | raw values | holds | the zeros are the source's values, not a cap or a placeholder (the maximum is 1.0; 0.67% of the ads sit exactly at 1). The warning is not yet in `accepted_check_warnings`; adding it is the curator's step (definitions.md) | - |
| 42 | Record screening: files, sizes, dates, description | record | Kaggle API file list and metadata | holds | train_active 9.2 GB, test_active 8.5 GB, train_jpg.zip 53 GB; opened 2018-04-24, deadline 2018-06-27; "Predict demand for an online classified ad" | - |
| 43 | Siblings: huntprohibited Yes, avito_context_ad_clicks No | record | their records | holds | - | PROV-6 |
| 44 | Earlier AI numbers: RMSE 0.2264 tabular, 0.2238 with a text SVD, 0.2597 for the mean, AUC 0.81 | record | - | superseded | measured on another split (train 15-25 March, test 26-28 March). On the shipped newest window: 0.2223 structured, 0.2199 with the text ridge, 0.2579 for the mean | EV-2 (a later stage) |
| 45 | 771,769 sellers | record Assessment | count | holds | - | - |
| 46 | Threads 55922 and 56533 got no answer; 58948 found the 88% | record Assessment | - | untested | those pages were not saved; only 55299 was checked | EV-7 |
| 47 | Builder: "Hidden-group probe not run (IID only)" | builder report | read the hidden-group probe and ran it | refuted (process); the probe finds no hits | the script has a temporal mode, which reports "temporal: no hits". Description as a text key: 5.4% of the ads share a description, 3.5% of test ads have one seen in training; near copies 0.2% | SPLIT-13, EV-7 |
| 48 | Builder: this is the "third exception for the same reason" | builder report | register.md | refuted | SPLIT-10 already has exceptions on 5 datasets (alfa_battle_2_0_task_2, lending_club, ames_housing, house_prices_nominal, perth_house_prices), and the register already flags `amendment_due: SPLIT-10`. This would be the sixth | principles (exceptions) |
| 49 | Implied: no row is copied across the split | - | leak probe and repost key | holds | exact copies on the feature columns: 0.05% of test ads, 0.0% once the text is included; reposts 0.04-0.06% | LEAK-16, LEAK-18 |
| 50 | Implied: the download can be reproduced | download_description | sha256 and file sizes | holds | 333,463,334 bytes, sha256 413b78...43f; train.csv 952,929,135 bytes | PROV |

**Refuted claims, ranked (by principle rank, then strength, then effect)**

1. **The seller drop (#17), P3 (USE-10, USE-6, LEAK-34; weighed against CLEAN-19).** The note says `user_id` adds little. That rests on a test that gave the id to LightGBM as a native category with about 300k levels, which LightGBM cannot use well. Encoded as the seller's past mean from the train side, the id cuts RMSE by 0.0011-0.0015 overall and by 0.004-0.005 on the ads of known sellers (26-31% of each test window). That gain is larger than the text's gain in the leak probe (+0.006 R^2), which was the reason given for shipping the text. Avito knows the seller when the ad is posted, and the competition overview lists "historical demand for similar ads" as an input. *What it changes:* the drop loses its stated reason. As shipped, the task is "predict for a seller the model cannot recognise", a narrower task than the use case. *Mildest remedy:* ship `user_id` as a categorical feature. We build no label feature ourselves (CLEAN-6 holds), and methods encode the id on the train side (precedent: ieee_fraud_detection's `uid`, LEAK-34). Otherwise keep the drop, correct the numbers in the note and name it in `fit_reason`. This is a weighing call for the curator (the builder's draft issue 3).
2. **The premise of the gap exception (#36, #35, #48), P4 (SPLIT-10 Should, SPLIT-12 Should; SPLIT-14 Must).** "A 3-day gap breaks SPLIT-14" holds only for the two-day horizon, which is our own choice ("as for a model refit every two days"), not the source's. One-day windows with a 3-day gap meet both SPLIT-10 and SPLIT-14 (training sides at 57-71% of the data). With two-day windows, even a 1-day gap fails the floor (49.97%). The cited gap is 4 days, not 3. The register already holds 5 SPLIT-10 exceptions and flags an amendment as due. *What it changes:* the departure from SPLIT-10 trades a gap against window width and weekday coverage, not against SPLIT-14. The measured effect is small: 0.0008-0.0012 RMSE. *Mildest remedy:* rewrite the splits comment to name that trade-off and the 4-day citation, and let the curator choose between two-day windows without a gap and one-day windows with a 3-day gap. Fold the case into the SPLIT-10 amendment.
3. **The text's size (#28), P2 (SEL-12 holds) and EV-8.** The note's numbers are the leak probe's mean over the three windows at 50k training rows. At the shipped size the text adds +0.016 R^2, and on its own it reaches R^2 0.206 against 0.257 for all structured columns. This changes no decision: the text ships, and tabular models stay competitive (in 59885 the team's best single LightGBM scored 0.2163, its best neural network 0.2180). *Remedy:* correct the bullet.
4. **The quote from discussion 56531 (#24), P7 note (EV-2).** The data refutes the thread: 6.2% of top-decile ads have no price, not 30%. *Remedy:* drop the quote; the measured means (0.215 against 0.135) already make the point.
5. **The late-ad mechanism (#14), P7 note.** For 33 of the 39 late ads that can be checked, the sequence number says the ad really was posted after 28 March. They are a selected set (84% positive) outside every window. The drop stands. *Remedy:* reword the reason.
6. **The hidden-group probe (#47), process (EV-7).** It does run on temporal tasks, and it finds no hits here. *Remedy:* record the result.
7. **Detail slips (#6, #19, #20, #26; the version comment's "227k" should be "228k").** None changes a decision. *Remedy:* correct the wording.

**Untested claims, ranked**

1. **Whether Avito's category model and image class (`image_top_1`) were fit on deal outcomes (#22), P4 (LEAK-27, USE-6).** No document says. It stays a cannot-verify item for the curator.
2. **The label's delay after posting (part of #38), P4 (SPLIT-10).** No source states it. The stable by-day means are the only evidence, and a two-download comparison is impossible with one release.
3. **The class balance of the competition's test (part of #40), P6 (MET-2).** Its labels were never released, so this cannot be checked.
4. **Whether the display periods run past the posting date (#27).** The periods files were not downloaded. The tables are not used, so this changes nothing.
5. **Threads 55922, 56533 and 58948 (#46), and the terms quote (#31).** The pages were not saved, and the rules page renders only with JavaScript. Terms are never evidence (EV-4).

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): avito_demand_prediction_1m**

**Verdict:** no column has to go and no cleaning step is wrong. Two notes in `curation_comments` should carry the numbers below: text and price that may have been edited after posting (LEAK-10, second clause), and Avito's model-made inputs (USE-6, LEAK-37 against LEAK-27). One CLEAN-10 wording gap: the price codes 0 and 1 are kept but not explained. The target's undocumented construction (USE-5, USE-8) is the only P3 item, and it is already the builder's draft issue 1.

Basis: the cleaned frame loaded through `dataset_io.from_definition` (1,503,324 ads x 15 columns, three windows: train 1,000,000 / 1,000,000 / 861,064, test 227,748 / 210,617 / 203,895). Meanings come from the data page as quoted in SRK's notebook (simple-exploration-baseline-notebook-avito) and threads 55299, 55897 and 56531.

**Column table**

| column | meaning (data page) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `region` | "Ad region" | yes: the seller picks it in the form | categorical, 28 levels, no missing | fine | USE-3, CLEAN-14 |
| `city` | "Ad city" | yes | categorical, 1,804 levels after the region is appended: 54 of the 1,733 names stand for towns in two or three regions (31,770 ads); no missing | fine: the town gets its full name back, which is not a hand-made feature | CLEAN-12, CLEAN-14 |
| `parent_category_name` | "Top level ad category as classified by Avito's ad model" | yes, Avito's classification at posting (re-classification during moderation is not documented) | categorical, 9 levels | fine | USE-6, LEAK-37 |
| `category_name` | "Fine grain ad category as classified by Avito's ad model" | yes, as above | categorical, 47 levels | fine | USE-6, LEAK-37 |
| `param_1` | "Optional parameter from Avito's ad model" (form field: car used/new, sell/rent/buy in real estate, type of clothing) | yes | categorical, 371 levels; 4.1% missing; 92% of an ad's values sit in one category | fine: missing means the field does not exist or was left empty, not a proxy code | CLEAN-10, CLEAN-14 |
| `param_2` | as above (car make, the kind of service) | yes | categorical, 271 levels; 43.5% missing (structural: categories without the field) | fine | CLEAN-14 |
| `param_3` | as above (car model, size); mixed meaning across categories, 11.6% of the labels look like numbers | yes | categorical, 1,219 levels; 57.4% missing (structural) | fine: a finite set of form values whose meaning differs by category, so a number would be wrong | CLEAN-14 |
| `title` | "Ad title" (Russian) | yes as posted; whether it was edited later is undocumented (see problem 2) | string, 788,334 distinct, no empty strings (428 titles shorter than 3 characters) | fine, with the note in problem 2 | LEAK-10 (second clause), LEAK-35 |
| `description` | "Ad description" (Russian) | as `title` | string; 116,269 missing (7.7%, mean target 0.076 against 0.144); no blank proxy strings; 218 descriptions hold a phone-like number and 4 an e-mail address | fine. Missing means the seller wrote no description: the share is flat over the posting days (7.1-8.9%, highest on weekends), so the outcome did not remove it | LEAK-10, CLEAN-10 |
| `price` | "Ad price" (rubles) | yes as posted; last edits are undocumented (problem 2) | float64, all whole numbers. 85,360 missing (5.7%, flat over the days at 5.1-6.1%; mean 0.215). 0 for 4,645 ads (mean 0.346) and 1 for 3,696 (mean 0.266), mostly cats, dogs and services, i.e. free, give-away or "contact me". 158 ads above 100 million, the largest 7.95e10 for a land plot, 7.0e8 for a sofa | fine to keep as entered. The codes 0 and 1 should be explained (problem 4). The extremes are typed in by the seller and show on the ad. Making them missing would mix them with "no price given", which has its own meaning | CLEAN-10, CLEAN-11 |
| `item_seq_number` | "Ad sequential number for user" | yes: the seller's running ad number, assigned at posting; it rises with the date within a seller in all but 10 of 731,655 consecutive pairs | int64, 1 to 204,429 (median 17 for private sellers, 125 for companies, 2,279 for shops) | fine: a count, numeric | CLEAN-14, LEAK-34 |
| `activation_date` | "Date ad was placed" | yes, it is the prediction moment | datetime, 14 days (15-28 March 2017). The 100 ads dated 29 March to 7 April are dropped. Also the split column | fine (see the note on the drop below) | SPLIT-6, CLEAN-14 |
| `user_type` | "User type" (Private, Company, Shop) | yes: an account attribute, constant for each of the 771,769 sellers in the release | categorical, 3 levels | fine | CLEAN-14 |
| `image_top_1` | "Avito's classification code for the image" | yes, Avito's class of the main photo at posting; whether that image model learned from deal outcomes is undocumented (problem 3) | categorical, 3,062 integer codes (0-3,066). 112,569 missing, exactly the ads without a photo (in the raw file `image` is missing on exactly the same 112,588 rows); the share is flat over the days (6.5-8.1%, lower on weekends). Category labels are floats (`1008.0`) | fine, with the note in problem 3; the float labels are cosmetic (problem 5) | USE-6, LEAK-37, LEAK-27, CLEAN-14 |
| `deal_probability` | target: "the likelihood that an ad actually sold something ... can be any float from zero to one" | n/a | float64 in [0, 1], no missing, 18,407 distinct, 64.8% zeros | how it is computed is undocumented: fit approximate, builder's issue 1 | USE-5, USE-8, MET-3 |
| `item_id` (dropped) | "Ad id" | | a 12-character hex hash, unique; neither its integer value nor the file order tracks the target (Spearman 0.0005 and -0.001) | fine to drop | CLEAN-3 |
| `user_id` (dropped) | "User id" | the seller is known at posting | a 12-character hex hash, 771,769 sellers; 27% of the newest window's ads come from a seller with an ad at least three days earlier | a defensible drop; measured gain 0.0002 RMSE (builder); weighing call, builder's issue 3 | CLEAN-3, USE-10, LEAK-34 |
| `image` (dropped) | "Id code of image" | | a 64-character hex hash of the jpg file, unique; its presence repeats `image_top_1`'s missingness | fine to drop | CLEAN-3, CLEAN-5 |

The dropped late ads (step 1 of `_clean`): Kaggle participants made the same cut. Thread 55897 shows the line `train_data[pd.to_datetime(train_data.activation_date) <= pd.to_datetime('2017-03-28')]`. The comment's reading, "their date was probably set by a later event", is not supported where it can be checked. 39 of the 100 late ads have a seller with an ad in the window, and 33 of those carry a running number above that seller's highest number in the window, so they look posted after 28 March rather than re-dated. Whether a re-activated ad gets a new number is unknown, so the evidence is circumstantial. The drop stands either way: the ads fall outside the release's posting window and are 84% positive. Suggested wording: "dated after the release's last posting day; 84% positive against 35%; whether posted later or re-dated cannot be told".

**Problems, ranked (principles.md: rank, then strength, then effect)**

1. **P3, USE-5 and USE-8 (Must): `deal_probability` is an undocumented Avito score.** I found nothing new at the column level: the range is [0, 1], nothing is missing, no capped values (LEAK-26 does not apply, and the 0.67% exact ones are not a pile-up). It stays the builder's issue 1 (keep with fit approximate, diabetes_3 precedent).

2. **P4, LEAK-10 second clause (Must, narrowed): `title`, `description` and `price` may be as last edited, not as posted.** The file does not say, and the display history (`periods_*`, `train_active`) is not used. Where an edit can be traced in the text, there are few edits and no gain:
   * Titles marked as sold ("продано/продана/проданы"): 2 ads. "продал": 6.
   * Descriptions saying "уже продано" (already sold): 43 ads, mean target 0.197 against 0.139. "нет в наличии" (out of stock): 209, mean 0.038.
   * Price-lowered phrases ("цена снижена", "снизил цену", "новая цена"): 741 ads (0.05%), mean 0.123 against 0.139. Their share is 0.07% on 15 March and 0.04% on 28 March.
   * "upd" and edit markers: 458 ads, mean 0.160.

   None of these groups is large or pure enough to move a score. Older ads do not carry more missing text, price or photo either (problem table), which an outcome-driven edit would produce. Under the clause, late values that cannot be located row by row stay with a note when the traceable part shows no gain (onlinenewspopularity precedent). Mildest remedy: keep, and add one sentence to the prediction-point bullet: "Edits are rare where the text shows them: 2 titles marked sold, 741 ads (0.05%) with a price-lowered phrase, mean deal probability 0.123 against 0.139." Evidence strength: circumstantial (EV-6), since an edit that leaves no words cannot be seen.

3. **P4, USE-6 and LEAK-37 against LEAK-27: `image_top_1` and the categories are outputs of Avito's own models.** LEAK-27 would apply only if the image model had been fitted to deal outcomes on these labels. The data points the other way:
   * The codes classify what is pictured. On average 87.5% of a code's ads fall in one parent category and 78.5% in one category; codes below 667 are 98% personal items (clothing).
   * The code number does track the mean target (Spearman 0.41 over 2,567 codes with 50 or more ads), but that is category composition. Against the residual after the category mean it is -0.09, and codes below 667 average 0.05 because clothing does.
   * The value is moderate, not leak-sized. Alone it gives R^2 0.094 (category_name 0.12). Dropping it costs untuned LightGBM 0.0028 RMSE on the shipped windows (300k training rows per window, structured columns: 0.22867 against 0.23145, all three windows the same way), about as much as dropping `param_1` to `param_3` (0.0027) and less than dropping `price` (0.0049). In-sample, category plus photo class explains about what category plus `param_1` does (eta^2 0.197 against 0.202).

   Mildest remedy: keep (USE-6), and put these numbers into the existing note so the cannot-verify item reads as tested as far as the data allows.

4. **P7, CLEAN-10 (Should): price codes 0 and 1 are kept but not explained.** The anomaly bullet counts 0 for 4,646 ads but does not say what it means, and does not mention 1. CLEAN-10 asks to keep a meaningful code and say why. Mildest remedy, one clause: "0 (4,645 ads) and 1 (3,696) are mostly cats, dogs and services, the seller's way of writing free or contact-me; mean deal probability 0.35 and 0.27; kept as codes." Also, the bullet's counts (85,362 missing, 4,646 zeros) are raw-file counts. After the late ads are dropped the frame holds 85,360 and 4,645, so "of the raw file" or the frame's numbers would be exact.

5. **P7, CLEAN-14 (cosmetic): `image_top_1`'s categories are floats (`1008.0`).** The raw column is float because of the missing values. Optional: `df["image_top_1"] = df["image_top_1"].astype("Int64")` in `_clean`, so the labels are integers. It changes no model.

**Not problems (checked)**

* Missingness caused by the outcome. The missing shares of the photo, description, price and `param_1` are flat across the 14 posting days, with weekday wiggles only. Removal after a sale would pile up in the oldest ads.
* Ids that encode the label. `item_id`, `user_id` and `image` are hashes; the file order is random against the target and the date.
* `item_seq_number` as a future count. It is the per-ad running number, monotone in date within a seller, so it is not a count over the whole release.
* `user_type` changing over time: it is constant per seller across the release.
* Window features ending at the outcome: there are none; every column describes the ad itself.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): avito_demand_prediction_1m**

**Verdict: right with notes.** The temporal split on `activation_date` fits the use case: three 2-day windows (27-28, 25-26 and 23-24 March 2017), an expanding train side capped at a random 1M, and no gap. Not having a gap is the right call. The reasons written for it are not: the deciding fact is the label's delay, and that can be bounded from the data. Two facts in `splits_comment` are wrong. The SPLIT-9 reading and the consistency check against alfa_battle_2_0_task_2 are missing. This would be the third SPLIT-10 exception for SPLIT-14's floor, so an amendment proposal is due.

```text
Verdict: right with notes.
Validity: SPLIT-1, SPLIT-3, SPLIT-6 hold (temporal by posting date; each ad is new, the seller recurs and is known: SPLIT-13, USE-10);
  SPLIT-14 holds (train sides 66.5%, 66.5%, 57.3% of the ads); LEAK-24 holds (no censoring in the newest days);
  SPLIT-9 holds under the Tensions reading (no measurable shortcut of consequence); SPLIT-10 departed (no gap):
  an exception that serves SPLIT-14. Its facts need restating, and it is the third of this reason.
For the curator: issue 1 (the exception and the amendment), issue 2 (the consistency check against alfa_battle's client filter).
```

**What I checked, with numbers** (untuned LightGBM as the builder ran it: structured columns plus weekday and text lengths, 400 trees, 2 threads)

- *Shipped plan* (from `dataset_io.from_definition`): 1,503,324 ads, dates 15-28 March. Each train side ends the day before its window, with no overlap. Train sides 1,000,000 / 1,000,000 / 861,064 (66.5%, 66.5%, 57.3% of the ads). The 1M draws are uniform over the days: 78.1-78.6% of every day for the newest window and 93.8-94.0% for the middle one. Tests 227,748 / 210,617 / 203,895. Untuned RMSE 0.22260 / 0.22744 / 0.22367 against a dummy of 0.25786 / 0.26363 / 0.25857 (skill 0.255 / 0.256 / 0.252).
- *Regime against the use case:* the predicted entity is the ad, which is new every time. The seller recurs: 30.9% of the newest window's ads come from a seller in the shipped train side (33.3% in the full pool). Avito knows its sellers at posting, so a known seller is part of the task (SPLIT-13, USE-10). A split grouped by seller would test a cold start this use case does not have. Temporal is right (SPLIT-6, SPLIT-3).
- *Time column:* `activation_date` is "Date ad was placed" (data page, as quoted in SRK's notebook). Day resolution. Dropping the 100 ads dated 29 March to 7 April is needed: without it the newest window would fall in April. The competition's test file has the same artefact. Its 508,438 ads cover 12-18 April (508,373), plus 64 ads on 19 April and 1 on 20 April (test.csv, measured).
- *Label delay:* not documented, but it can be bounded. `periods_train.csv` (16.7M display periods of the supplementary ads, displayed 15-28 March, downloaded for this audit) shows that ads stay listed long after posting. Of the ads activated on 15 March, 96.0% were still listed more than 3 days later, 92.6% more than 7 days later, and 89.4% on 28 March. For 16-18 March the 28-March figure is 85-86%. This is a proxy: display is not a deal, the supplementary ads are not the train ads (0 shared ids), and the file stops at 28 March. Still, a deal can settle weeks after posting, so nearly every training label would be unknown when a window starts. The stored labels are settled: the target by day is flat (mean 0.136-0.141, zero share 0.639-0.670), so the newest days were not cut short (LEAK-24).
- *What a gap costs, with training size held equal*: a 3-day gap against a random draw of the same size from all earlier ads. Newest window: +0.00024 RMSE (paired SE of the MSE difference 0.000039; two random draws differ by 0.00014). Middle window: +0.00020 (SE 0.000048; draws differ by 0.00025). The builder's 0.0008-0.0012 compares 1.28M and 1.06M training rows against 0.97M and 0.75M, so most of it is training size, not recency.
- *Alternative split, fitted*: three 1-day windows (26, 27, 28 March) with a 3-day gap. This meets the floor: the train pools are 57.3%, 64.4% and 70.8% of the ads.

  | design | window | train rows | RMSE | skill |
  |---|---|---|---|---|
  | shipped, 2 days, no gap | 27-28 / 25-26 / 23-24 Mar | 1.00M / 1.00M / 0.86M | 0.22260 / 0.22744 / 0.22367 | 0.255 / 0.256 / 0.252 |
  | 1 day, no gap | 28 / 27 / 26 Mar | 1.00M each | 0.22239 / 0.22245 / 0.22695 | 0.263 / 0.249 / 0.254 |
  | 1 day, 3-day gap | 28 / 27 / 26 Mar | 1.00M / 0.97M / 0.86M | 0.22250 / 0.22271 / 0.22789 | 0.262 / 0.247 / 0.248 |

  On the same days the gap costs 0.0001 / 0.0003 / 0.0009 RMSE. The 0.0009 on 26 March also has 139k fewer training rows. In skill that is 0.0007 / 0.0017 / 0.0062. The model spread (LightGBM against linear, 0.037 skill) is at least six times larger. Comparing the windows against each other decides nothing (SPLIT-21).
- *Training history and season:* the oldest window trains on 8 days (15-22 March), a full weekly cycle. There is no break in 14 days. The windows fall on Thu-Fri, Sat-Sun and Mon-Tue. The weekend window has more zeros (dummy 0.2636 against 0.2579 and 0.2586), but its skill is the same (0.256). No window is atypical.
- *Hidden-group probe, temporal mode*: no hits. `param_1` looks like an entity (95.9% of test rows have a value seen in training), but it is a form field that new ads keep (SPLIT-4). Near copies: 0.6% of the rows, 0.2% of the test rows seen in training. The same normalised description is shared by 5.4% of the rows and seen in training for 3.5% of the test rows.

**Problems, ranked (principles.md: P4 first, Must before Should)**

1. **P4, SPLIT-10 (Should): the no-gap exception is right, but its stated fact does not decide it, and two facts are wrong.**
   - *Evidence:* `splits_comment` and `fit_reason` say no delay can be stated. The display periods bound it: weeks, for most ads.
   - *Wrong fact 1:* the third-place gap was four days, not "three". Topic 59885 says the team "trained on the first six days of training and used days ten through thirteen as validation. This meant days six through nine were excluded", and its target likelihoods "always applied a gap of 4 days".
   - *Wrong fact 2:* "leaves the oldest window under half" holds only for 2-day windows. With them, a 3-day gap leaves 35.0% and even a 1-day gap leaves 49.97% (751,251 ads, 411 short of the floor). With 1-day windows a 3-day gap fits (57.3%).
   - *The facts that do decide:* no gap that fits in a 14-day release comes close to the delay. At equal training size the largest feasible gap is worth 0.0002 RMSE. Two days is the longest window that keeps three windows above the floor, which is the closest we can get to the competition's 7-day test week.
   - *Remedy (the mildest):* keep the split. Rewrite the no-gap sentences of `splits_comment` and the end of `fit_reason` with these facts, and record the exception. Suggested wording: "No gap. Exception to SPLIT-10 (date, curator): a deal can settle weeks after posting (89% of the supplementary ads activated on 15 March were still listed on 28 March, periods_train.csv), longer than any gap the 14-day release allows: with two-day windows even a one-day gap leaves the oldest window 49.97% of the ads, and with one-day windows the largest gap is three days. Serves SPLIT-14 (Must). At equal training size a three-day gap costs untuned LightGBM 0.0002 RMSE on the two newer windows."
   - *Third exception for this reason* (after alfa_battle_2_0_task_2 and lending_club): the facts match (no label dates, and a delay longer than the floor allows). principles.md therefore asks for a consistency check and an amendment. Draft text for SPLIT-10: "When the label's delay is longer than any gap that keeps SPLIT-14's floor (no label dates, and a delay as long as the release or longer), the windows train without the gap: SPLIT-9's measurable shortcut is removed first, the newest period is checked for censoring (LEAK-24), the cost of the largest gap the floor allows is measured at equal training size, and the departure is stated in the splits comment. Cases: alfa_battle_2_0_task_2, lending_club, avito_demand_prediction." The other way out is the 1-day windows with a 3-day gap above. It meets both rules on paper, but by the display proxy it covers only about 4-7% of the closures, and it trades the window length for a gap the delay does not match. I recommend against it.

2. **P4, SPLIT-9 (Must): holds, but the reading is not written down, and the seller channel needs a consistency check against alfa_battle_2_0_task_2.**
   - *Reposts:* same-seller copies of a test ad's description are 0.47-0.60% of a window. Their labels correlate 0.52-0.55 with the test label. An oracle blend fitted on those ads themselves moves the window RMSE by at most 0.00006. Ads whose description appeared only in the three days before show +0.0016 and +0.0082 RMSE on 925 and 1,218 ads, about 0.00004 at window level. This is circumstantial (EV-6).
   - *Seller id:* it is not shipped. Dropping `user_id` is also the SPLIT-9-safe choice: the seller's training labels would not be settled when the window starts. This supports issue 3's current choice from the split side.
   - *The precedent:* alfa dropped the training rows of the test window's clients. The same filter here would drop 13.1%, 11.1% and 13.7% of the train sides and leave the oldest at 49.5% of the ads. On the newest window it raises RMSE by 0.0009 against an equal random removal (0.22362 against 0.22271). All of that is on the 31% of test ads from a seller in training (+0.0032); the others are unchanged (0.23181 against 0.23180).
   - *What sets the case apart*: a test ad is positive in 43.5% of cases after a positive ad by the same seller 1-3 days earlier, and 14.7% after zeros only (base rate 35.7%). For ads 4-12 days earlier the figures are 41.5% and 16.0%. Only 20.8% of the positive test ads had a seller with a positive training ad. Alfa showed 95.1% against 2.3%, with 45.5% of later defaults preceded by an earlier one: an outcome stamped on all of a client's products at once. Here the signal is a moderate, persistent seller trait, of the kind a model refit on settled history would also learn.
   - *Remedy:* add one SPLIT-9 sentence to `splits_comment` with these numbers, as alfa's and lending_club's comments do. If the curator reads the seller effect as a shortcut anyway, the alfa filter is the fix. The floor then gives way (Tensions row: "a shortcut that can be measured is always removed, whatever it costs the floor").

3. **P4, SPLIT-12 (Should): the horizon reasoning is incomplete.**
   - *Evidence:* the competition trains on 14 days, skips 14, and tests on the 7-day week of 12-18 April, a horizon of 15-21 days. The shipped horizon is 0-2 days. `splits_comment` explains the 2-day windows by weekday coverage. The stronger reason is that 2 days is the longest window that fits.
   - *Remedy:* one sentence: "two days is the longest window that leaves three windows above half the ads; the competition's 15-21-day horizon cannot be repeated within the release".

4. **Procedure (EV-2, EV-7): small factual corrections.**
   - The competition test is "ads of 12-18 April" plus 65 stragglers on 19-20 April, not "12-20 April". This appears in `splits_comment` and `curation_comments`.
   - `task_summary.split` says "training is a random million of the ads posted before it". The oldest window trains on all 861,064.
   - Builder report: "Hidden-group probe not run (IID only)" is inaccurate. the hidden-group probe has a temporal mode. Run here, it finds no hits.
   - Builder report: "27% of the newest window's ads from a seller already in training" counts only sellers with an ad at least 4 days before the window. The full figure is 33.3% (30.9% in the shipped 1M draw).
   - The 0.0008-0.0012 RMSE "gap cost" should be read as mostly training size (see the equal-size numbers above).

**Checks that pass:** SPLIT-1/3/6 (regime), SPLIT-11 (expanding train side, newest window first), SPLIT-14 (3 windows, at least 57.3% each), SPLIT-15 (3 windows, the default protocol), SPLIT-17 (204k-228k test rows), SPLIT-19 (cannot be followed: no public test labels, stated), SPLIT-20 (a full weekly cycle, no break), SPLIT-22 (n/a), LEAK-24 (no censoring), and the row budget (random 1M, uniform by day).

**Cannot verify:** when Avito's score becomes final (the display periods are a proxy). Whether a seller's earlier outcomes carry the later ad's outcome or only a persistent trait: settling it would need labelled ads from weeks before the release, which the release does not have.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: Avito's seller-experience team, advising a seller at posting (avito_demand_prediction_1m)**

**Verdict.** Fit **approximate**. I agree with `fit="approximate"`. Every input is in the ad when it is posted, and one
row is one piece of advice to one seller. The gap is the label: an undocumented Avito score that is built in two
different ways depending on the category. It stands for a deal that Avito, as a classifieds site, never observes, and
it is not the interest (views, contacts) that the advice talks about (USE-5, USE-8). Metric: **yes**. RMSE on the
score ranks models the same way as a Brier score on the deal would, and I act on one ad at a time with no threshold
(MET-4, MET-8). The panel should note one new fact (gap 1) and make four text changes. No data change is needed for
this version.

**How the decision is made today (domain sources)**

- Deals on Avito happen off the platform. Avito's own Seller Experience team trains its listing-advice model on
  "target contacts" (calls and chats). It says it cannot know whether a contact led to a purchase ("мы точно не знаем,
  привёл ли контакт к покупке") and that the contact metric is "очень близка к фактическому количеству сделок"
  (Habr 879680). In other words, a deal on Avito is always an estimate, never an observation.
- The forecast Avito actually shows sellers today is a range of views for a promotion budget. It is computed "на
  основе данных продвижения похожих объявлений" (AiF on Avito's view forecast). It forecasts views, not deals, and it
  uses the context of similar ads.
- The competition overview (the text of the EDA kernel, matching the GitHub mirror) names two complaints: sellers get
  too little demand (a wrong product or listing) or too much (an underpriced item). Its inputs are the ad, "its
  context (geographically where it was posted, similar ads already posted) and historical demand for similar ads in
  similar contexts". Its aim: "inform sellers on how to best optimize their listing and provide some indication of how
  much interest they should realistically expect to receive".

**1. Do I have these inputs at the moment of advice?**

- I have all 14 at posting. Title, description, price, place, category, `param_1`-`param_3`, the photo class, the date,
  `user_type` and `item_seq_number` (the seller's running ad count, as of posting).
- `image_top_1` and the category columns are outputs of Avito's models, computed at posting. Under USE-6 they are
  inputs whether or not Avito's models learned from earlier deal outcomes: a company's own estimate made before the
  outcome is an input. Only a code fitted on these very ads' labels would be a leak. `image_top_1` alone gives R^2
  0.094, below `param_1` (0.150), so nothing points that way. The builder's "cannot verify" item on this point
  therefore does not affect the keep.
- Text edited after a sale. I checked this on the raw file:
  - Titles with "продано/продан/бронь/sold": 58 ads, mean score 0.097 against 0.139 overall.
  - Descriptions with these words: 2,186 ads, mean 0.143.
  - So there is no sign that sellers rewrote their ads to mark a sale.
- What I would always have and the dataset lacks:
  - (a) **The seller's history.** Account age, earlier ads and their contacts, reviews. The seller is almost always
    known (USE-10): the median private seller is on their 17th ad (`item_seq_number`; companies 125, shops 2,279), and
    65% of the ads come from sellers with more than one ad in these 14 days alone. The dataset keeps the as-of count
    (`item_seq_number`) and `user_type`. The builder measured that `user_id` as a category adds only 0.0002 RMSE, and
    CLEAN-6 bars a history built from labels. This is acceptable for the release.
  - (b) All photos and their count. Only the class of the main photo ships.
  - (c) **The market at that moment.** How many similar ads are live in the same city and category. The overview names
    this as an input. `train_active` and `periods_train` could give an as-of count.
  - (d) The paid promotion the seller buys.
  - (e) The hour of posting.

  With these missing, the task is "the demand an ad will meet, judged from the ad alone". That is narrower than
  Avito's own task, but still a real one.

**2. Is the target what I act on?**

It is a proxy. I act on the interest an ad will get (contacts in its first days) or on whether it sells within some
days. `deal_probability` is Avito's score, whose construction is undocumented. My probe adds one fact that the
definition does not state: **the score is built differently by category.**

- In offers of services (64,385 ads, 4.3%), every positive value is a fraction k/n with n at most 8. There are 22
  values, from 1/8 to 1: 0.2 on 8,085 ads, 0.4 on 6,298, 1.0 on 10,071. These read as a share of a few counted events.
- Outside services, only 39 of 479,572 positive ads carry such a fraction. Their values are category-level numbers:
  0.80323 on 46,668 ads, 0.7376 only on cars (13,922 ads).

So one column holds an observed rate for services and a scored level for goods. A number on 0-1, calibrated within
each category, is what I would want. Regression on this score is the right form.

**3. One row, one decision; is the test data what I would face?**

Yes: one ad is one piece of advice. Each test window is the next two days of new ads, which matches a model that is
refit often. Two differences:

- (a) **No gap.** Avito would not yet have the score for yesterday's ads: the score is known only after the ad has run
  its course. The organisers' own test started 15 days after the last training day. A three-day gap costs 0.0008 to
  0.0012 RMSE on untuned LightGBM, so the optimism is small, and SPLIT-14 justifies leaving it out.
- (b) **Population.** The data covers 28 of Russia's regions, without Moscow, Moscow Oblast, St Petersburg or Leningrad
  Oblast (Avito's largest markets). It has no jobs category, and it covers two weeks of March. The `row` field does not
  say any of this.

**4. Would I use this model?**

Yes, as a baseline indicator of expected demand.

- Untuned LightGBM reaches R^2 0.216 (builder's task probe). The parent category alone gives R^2 0.094 and `param_1`
  0.150, and the text adds 0.006. So the model mostly tells a seller what ads like theirs score in their category and
  town.
- I would trust it as a calibrated level per category. The daily mean is flat at 0.136-0.141 (decision 2).
- I would distrust it as advice on what to change, which is the first half of the use case. Its associations are not
  effects. An ad without a price scores 0.215 against 0.135, because services, giveaways and ads that make buyers ask
  questions have no price (discussion 56531). A model read as "remove your price" would give wrong advice.
- With 65% zeros, most sellers would be told "low".
- What would raise my trust: Avito's definition of the score, calibration by category, and results on the capitals.

**5. Does the metric score my decision? Yes.**

- RMSE is a monotone function of MSE, so per window it ranks models as MSE does.
- Suppose the score s is a calibrated posterior P(deal | Avito's signals), and the ad's fields are part of those
  signals. Then E[(p - deal)^2] = E[(p - s)^2] + E[(s - deal)^2], and the second term does not depend on the model. So
  MSE against the score ranks models exactly as the expected Brier score against the unobserved deal would: a strictly
  proper rule for the deal probability given the ad (Gneiting & Raftery 2007; MET-8).
- The same holds for the services' k/n values, which are unbiased estimates of a rate.
- It is the competition's leaderboard metric (MET-4). The forum's "weird choice for probabilities" (discussion 55299)
  is a complaint, not evidence of bias or gaming, so MET-4 is not overruled.
- MET-6, MET-7 and MET-9 do not apply. The advice is per ad, at no threshold, cost or top k. The unit (one ad) exists
  in the data (MET-2), and the scale is the source's (MET-3).
- The only alternatives I would consider are the Brier score itself (it ranks models the same) or the soft-label log
  loss that Kaggle could not compute (also proper, harder on confident misses). Neither is a reason to switch
  (MET-10, a competition's track record).
- Caveat: if Avito's score is not calibrated, RMSE scores agreement with Avito's score. That is the same gap the
  approximate fit already names.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **The label** (USE-5, USE-8). Avito's undocumented score stands for a deal that the platform never observes, and it
   is built two ways: k/n rates with n at most 8 in services, category-level values in goods. It is not the contacts or
   views that "interest" means in the use case. This is what makes the fit approximate. It matches diabetes_3 and
   coffee_rating_prediction.
2. **The use case is half counterfactual** (USE-1). "How to improve the listing" needs effects, which a predictive
   benchmark does not test. The benchmark tests only "how much interest to expect". This changes how the task is read,
   not the data.
3. **Context the actor always has is missing** (USE-3, USE-10): seller history beyond an ad count, all photos,
   competing live ads, the promotion bought. The task narrows to "from the ad alone".
4. **Population and period**: 28 regions without the two capitals, no jobs category, two weeks of March. The test
   stands for the next days in the same regions, not a new month or market.
5. **Split timing**: there is no gap, while the label delay is unknown (the organisers left 15 days). The measured cost
   is about 0.001 RMSE.

**What a domain expert would change**

1. **Target bullet.** Add the services fact. In offers of services (64,385 ads, 4.3%) every value is a fraction k/n
   with n at most 8 (22 values), while elsewhere values repeat by category. Add Avito's own statement that it cannot
   observe a sale and uses contacts as its deal proxy (Habr 879680). Then the approximate fit rests on the domain, not
   only on the forum's silence.
2. **`use_case` or the prediction-point bullet.** Keep the expectation half. Say that the "how to improve the listing"
   half is not what the benchmark tests, and give the missing-price example.
3. **`row`.** Add "in 28 of Russia's regions (not Moscow or St Petersburg)", and possibly "no jobs category".
4. **Prediction-point bullet and the builder's cannot-verify list.** Cite the sold-word check for later edits. Reword
   the `image_top_1` note: under USE-6, a code computed at posting stays an input even if Avito's model learned from
   earlier deals.
5. **A later version, optional.** An as-of count of competing live ads by city and category from
   `train_active`/`periods_train`, plus as-of seller features from earlier ads (count, categories; not labels). The
   overview names this context.
6. **`split` sentence.** "as for a model refit every two days" could add "with the labels of the days just before,
   which Avito would not yet have". `fit_reason` already says it.
7. **For the claim auditor.**
   - The splits comment calls a three-day gap "the third-place team's scaled copy of the competition's gap". The
     write-up (59885) trains on "the first six days" and validates on "days ten through thirteen", so "days six through
     nine were excluded". Under its 0-based numbering that is four days.
   - The EDA kernel gives the test as 12-19 April, while the notes say 12-20 April.

**Sources**

- Competition overview and data page, as quoted in the public kernels avito-eda-fe-time-series-dt-visualization and simple-exploration-baseline-notebook-avito; GitHub mirror https://github.com/wangz19/Avito_Demand_Prediction_Challenge/blob/master/README.md
- Kaggle discussions 55299 (welcome; target asked three times, Wendy Kan on log loss), 56531 (missing price), 59871 and 59885 (2nd and 3rd place)
- Habr, Avito Seller Experience team, interpretable model of service-listing liquidity, target contacts as the deal proxy: https://habr.com/ru/articles/879680
- AiF, Avito's forecast of views for promotion: https://aif.ru/money/business/prognoz-prosmotrov-na-avito-kak-effektivno-planirovat-prodvizhenie
- My probes on the raw file (sold words; values by category) plus inline checks (regions, repeat sellers, error share by category); the builder's task, leak, seller-id and count probes.
- Rules: use_case.md USE-1, USE-3, USE-5, USE-6, USE-8, USE-10; metrics.md MET-2, MET-3, MET-4, MET-6 to MET-10.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is real Avito data from a known Kaggle task, with real but modest signal and no leakage I could find. Before it goes in, it needs four small preparation fixes: declare the text columns, keep the raw date out of the features, make `image_top_1` categorical, and document the target and the dropped rows.

**What the task is.** Avito is Russia's largest classifieds site. At the moment a seller posts an ad, it predicts how likely the ad is to lead to a deal. The organisers' stated use is "inform sellers on how to best optimize their listing and provide some indication of how much interest they should realistically expect to receive". Avito could also use it for ranking or promotion. This is a real use. Every feature in the table is known when the ad is posted:

- category and params (both "as classified by Avito's ad model")
- region and city
- title, description and price
- `item_seq_number` ("Ad sequential number for user")
- `user_type`
- `image_top_1` ("Avito's classification code for the image")

The target is defined after the fact. Source: the Kaggle data page as mirrored on GitHub (for example soundwave-77/ML-project DATA_DESCRIPTION.md). The Kaggle pages themselves render empty without JavaScript.

**What I checked** (on the 300,000-row sample, using pandas and LightGBM 4.7):

- **Dates and target drift.** There are 14 activation dates, 2017-03-15 to 2017-03-28, with about 19-23k rows per day. The rows are sorted by date. The daily target mean is flat at 0.136-0.144, and the zero share is 0.63-0.67, slightly higher on weekends. There is no sign of right-censoring: ads posted late do not have lower targets.
- **Target shape.** Mean 0.139, sd 0.260. 64.9% of rows are exactly 0 and 0.66% are exactly 1. There are 9,554 distinct values.
- **Signal.** I trained LightGBM on the categoricals, log price, `item_seq_number`, `image_top_1`, day-of-week and text lengths. Each run trained on earlier days and tested on later days.

| Test days | Model RMSE | Train-mean baseline RMSE | R² |
|---|---|---|---|
| 03-25 to 03-26 | 0.2334 | 0.2640 | 0.218 |
| 03-27 | 0.2262 | 0.2563 | 0.221 |
| 03-28 | 0.2255 | 0.2572 | 0.232 |

- **Signal from simpler or different inputs.** With category plus `user_type` only, R² is 0.13-0.14. A TF-IDF ridge on title and description alone reaches R² 0.187. Adding that ridge prediction to LightGBM gives RMSE 0.2228 and R² 0.247 on 03-27 to 03-28.
- **Comparison with the competition.** Strong competition single models scored about 0.213-0.219 RMSE (darraghdog/avito-demand README: "lgb_1406 ... 5CV Val 0.2136"). Those models used user, image and active-period features that are not in this table. So the task is learnable, far from trivial, and leaves headroom.

**Concerns, from most to least serious**

1. **Much of the signal sits in two free-text columns.** `title` has 186,801 unique values and `description` has 267,314 in 300k rows; both are stored as `string`. Text alone gives R² 0.19. On top of the tabular features it adds about 0.02 R² (0.229 to 0.247 on the same days). If a pipeline treats these columns as categoricals, it either blows up or learns noise. If it silently drops them, the task becomes a different one.
   - Change: mark both as text in the task metadata so every method sees the same declared modality. Alternatively, drop them and say so. Do not leave them as an unspoken nominal column.

2. **The target is an Avito-made soft score, not an observed sale.** The source says: "This is the likelihood that an ad actually sold something. It's not possible to verify every transaction with certainty, so this column's value can be any float from zero to one." The data show how the score is built:
   - Each parent category has a hard ceiling, and that ceiling is also the most common non-zero value: 0.76786 for electronics, 0.80323 for personal items, 0.86521 for home, 0.82668 for hobbies, 0.78503 for animals, 0.78912 for business.
   - In personal items, the non-zero values divided by 0.80323 give 1.0 (9,495 rows), 0.1566, 0.34, and so on.
   - Services (`Услуги`) has only 22 distinct values, all fractions k/n with n ≤ 8: 0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8, 1.0, and so on.

   So the label looks like a category-level conversion rate times an activity fraction. That is a legitimate target and it is the official one. But part of the RMSE comes from learning the per-category ceilings, and the label has a built-in noise floor.
   - Change: none to the data. Document that the target is a bounded, zero-inflated, category-capped score, and keep RMSE (the competition metric).

3. **`activation_date` is the split key and is a raw datetime column.** It has 14 values. In every test window the dates lie beyond the training range, so a model that uses the date as a number is extrapolating on a column with no real use at prediction time.
   - Change: drop it from the features after splitting, or replace it with day-of-week. Day-of-week carries weak real signal: 1.6% of LightGBM gain.

4. **`image_top_1` is a classification code stored as float64.** It has 3,028 unique codes in the sample, all whole numbers, from 0 to 3066. Missing (7.5%) means the ad has no image, and the target differs: 0.192 without an image versus 0.135 with one. It is the 5th-ranked feature by gain.
   - Change: cast it to categorical, and keep NaN as its own "no image" level.

5. **100 rows were dropped without a note.** The Kaggle train file has 1,503,424 rows (for example the Erlemar/Avito_demand_prediction_2018 notebook prints "(1503424, True)"). The prepared table has 1,503,324. The original file has a handful of rows dated 2017-03-29 to 2017-04-03; darraghdog's fold definition lumps them in with "2017-03-27", "2017-03-28", and so on. The sample contains no dates after 03-28. So the dropped rows are very likely these stragglers, which is a sensible choice.
   - Change: state it in the task description.

6. **The table is thinner than the competition data.** `item_id`, `user_id` and `image` were removed, and the supplementary train_active and periods files are not used. Dropping the IDs is right for a tabular benchmark. The consequence is that scores here are not comparable with the Kaggle leaderboard, and the task under-represents what Avito actually had available.
   - Change: none required. Note it.

7. **Reposts across rows are rare.** In the sample there are 2 exact feature duplicates. There are 140 groups covering 304 rows that share title, description, price, city and category. Within those groups the target sd is 0.028 (against 0.26 overall), and 78% of groups share a single target value. Most of these groups (mean 1.24 dates per group) fall on a single day. Scaling the pair count from the 20% sample gives an estimate of roughly 0.5% of rows in the full data. Reposting by repeat sellers is real deployment behaviour, so the effect is negligible.
   - Change: none.

8. **Price has junk placeholders, which is normal for classifieds.** Examples: 2,000,025,000 for "Продам холодильники" (fridges), 180,007,000 for used sheepskin coats, 896 zero prices, 1,984 prices under 10, and 5.7% missing (where the target mean is 0.217 versus 0.134 when a price is given).
   - Change: keep as is. It is real noise, and tree models and log transforms handle it.

9. **Size and cost.** The full data has 1.5M rows and long text, which is heavy for some methods. The benchmark's subsampling should be fine: 300k rows already gave stable scores across the three windows.

**Preparation that is already done well.** `city` is made unique by appending the region, for example "Краснодар (Краснодарский край)". This turns 1,515 raw names into 1,561 city-region values and resolves cities that share a name across regions. Categoricals are stored as `category`. The NaNs in `param_2` and `param_3` (43.6% and 57.4%) are structural: those parameters do not exist for some categories. Strings are already stripped. The "/\n" line breaks in descriptions are in the original data.

**What I could not check**

- The full 1.5M rows; I only had the 20% sample. Duplicate rates are scaled estimates.
- The exact boundaries of the 3 test windows; my windows are my own choice.
- How Avito actually computed `deal_probability`. It is not published; my reading comes from the value patterns only.
- That `image_top_1` is assigned at posting time. The source wording implies it but does not say so.
- The Kaggle pages directly. They render empty without login or JavaScript, so I relied on GitHub copies of the data description and on public solution code.

</details>

<details><summary>Precedent check</summary>

**Precedent check: avito_demand_prediction_1m (precedent-checker, 2026-11-01)**

**Verdict:** two decisions need the curator: the split without a gap (SPLIT-10) and the dropped seller id (CLEAN-3, LEAK-34). Every other choice follows its precedents. The builder calls the no-gap split the third exception of its kind. That count holds only once the record states a label delay of 4 days or more. As drafted, the reason rests on the chosen 2-day windows, not on SPLIT-14.

**Register flags read** (the decision register of 2026-11-01):

* `amendment_due SPLIT-10` counts five dataset names by rule ID. By reason there are two pairs. The floor reason (SPLIT-14) has alfa_battle_2_0_task_2 and lending_club. The time-resolution reason has ames_housing (= house_prices_nominal) and perth_house_prices. The second pair has its own amendment proposal, open for Lennart (splits.md, Cases, "proposed", 2026-10-26). That row says alfa and lending "depart for another reason ... and do not count". So avito could only be the third of one reason, not the sixth of the rule.
* `exception_to_must SPLIT-9 / SPLIT-14` (alfa, lending) is a parser artefact. The exceptions are to SPLIT-10 and cite SPLIT-9 and SPLIT-14 as the rules they serve. An avito exception worded the same way will raise the same false flag.
* `amendment_due CLEAN-19` (amex_non_iid, fraud_detection) is the "history kept as rows" reason. Avito does not add to it (see the table below).
* No drift. Andrej has no earlier SPLIT-10, CLEAN-3 or LEAK-34 decision in the register. Lennart's SPLIT-10 line holds together. He sets a gap when a delay is measured or sourced (brazilian_ecommerce, sf_permit_time, house_sales, zillow_prize, the trip-time family). He sets no gap, as an exception, when the gap of the delay breaks the floor (alfa, lending) or when dates are coarser than the delay and show no selection (ames, perth). He sets no gap, as applied, when as-of data show no selection (melbourne_housing_market).

**Per decision**

| Decision | Verdict | Closest precedents |
|---|---|---|
| `_1m` folder, `version_of`, a random 1M per train side | consistent | definitions.md "Larger than the row budget" (Lennart, 2026-10-21); nyc_taxi_trip_duration_1m (train sides 1.28-1.39M); huntprohibited_1m (the Avito sibling, shipped only as `_1m`, 2026-10-26); delivery_eta_1m. Avito's train sides are 1.28M, 1.06M and 0.86M before the cap. |
| Target `deal_probability` as released, fit `approximate` | consistent, with one open point (SEL-3, below) | diabetes_3: undocumented label kept as approximate, USE-5 amended (Lennart, 2026-10-21; shipped 2026-10-26); alfa_battle_2_0_task_2: approximate for a label without a stated horizon (USE-8); a source's own assessment as target: corporate_issuer_credit_rating (2026-10-16), wine_quality (2026-10-21) |
| Zeros kept as released, `task_target_value_dominant` accepted | consistent | Andrej, 2026-10-30, zero-inflated policy question 2; the same warning is accepted with the same reason across this batch (allstate_claim_prediction_challenge_1m, blogfeedback, frempl and others) |
| Drop `item_id`, `image` | consistent | CLEAN-3; huntprohibited drops its random `itemid` (shipped 2026-10-26, Lennart) |
| Drop `user_id` | **departs, with a stated reason that the closest precedent weighed the other way**: prompt 2 | ieee_fraud_detection `uid` kept (Lennart, 2026-10-01); african_credit_scoring_challenge `customer_id` kept (shipped 2026-10-26); brazilian_ecommerce `seller_id` kept (shipped 2026-10-15) |
| Drop the 100 ads dated 29 March to 7 April | consistent with the rules (LEAK-10: the date marks the outcome, 84% positive against 35%; LEAK-7: the smallest fix, and such a row cannot be placed in a window). No close precedent, so it is the first case of its kind and could become a Cases row. | none found |
| `city` written with its region | consistent | perth_house_prices: `Vic` split into Victoria Street and Victoria Park (review of 2026-10-20, shipped) |
| Keep 2 exact copies and 4 conflicting rows | departs from LEAK-19/LEAK-20 (Should). The reason given is size ("negligible"), but a better fact exists: I measured that in all 6 pairs the two ads come from **two different `user_id`s**. That makes them distinct ads, like african_credit_scoring_challenge's 267 copies with their own loan ids (2026-10-26) and brazilian_ecommerce's same-second orders. huntprohibited dropped its copies (Lennart, 2026-10-22), but its file has no seller key. Replace "negligible" with this fact; no prompt needed. | huntprohibited (dropped); african_credit_scoring_challenge, brazilian_ecommerce (kept as distinct entities) |
| Keep reposts (0.69%) as separate postings | consistent | huntprohibited: edited reposts stay because "the label is per ad" (Lennart, 2026-10-22). LEAK-21's emscad case rests on the source paper's own drop; Avito made none. |
| No seller aggregates, no `train_active`/`periods` tables | consistent (not an exception to CLEAN-19) | CLEAN-20 bars copying a feature computed over all rows (the whole-release seller statistics). The display periods run past posting (LEAK-10). african_credit_scoring_challenge's added `earlier_loans` (a label-free as-of count, 2026-10-26) already has its counterpart in Avito's `item_seq_number`. CLEAN-19's "raw data cannot be used as it is" condition does not hold for one row per ad. alfa and rosbank1 aggregated because their raw data is a transaction log. |
| `image_top_1` and Avito's categories kept; photos not used | consistent | USE-6 (brazilian_ecommerce's promised date, bias_correction's LDAPS forecast). SEL-12/13 are judged per dataset: one image class among 17 columns, worth 0.001 RMSE. athabasca_forage_lichen_cover (Andrej, 2026-10-30, SEL-13) differs: all of its covariates were remote-sensing reflectance. |
| `title`, `description` as Russian text strings | consistent | huntprohibited_1m (Avito, Russian text as strings, shipped 2026-10-26); mercari_price_suggestion (CC 2026-10-06) |
| `Spatial` tag | consistent | definitions.md ("region"); huntprohibited has no tag because it has no geographic column (Lennart, 2026-10-22). Avito has `region` and `city`. |
| Three 2-day windows instead of the competition's split | departs from SPLIT-19 with a stated reason: 14 days cannot hold three windows of the competition's 9 test days above the floor (SPLIT-14, Must). The weekday argument is SPLIT-20 reasoning, as in aeolus (Lennart, 2026-10-12). Reasonable. It interacts with the gap; see departure 1. | aeolus_1m, acquire_valued_shoppers_challenge (5 x 5 days) |
| No gap | **departs from SPLIT-10 with a stated reason that does not yet match the precedents it would join**: prompt 1 | alfa_battle_2_0_task_2, lending_club, melbourne_housing_market, ames_housing, perth_house_prices |
| RMSE, `Metric.source` | consistent | MET-4 cases (zillow_prize `mae` kept, mercari_price_suggestion, rossmann_store_sales); principles.md Tensions row (Lennart, 2026-10-21) |

**Departure 1: the split without a gap (SPLIT-10, Should)**

What the draft says: the delay is undocumented, and a 3-day gap "leaves the oldest window under half of the ads (SPLIT-14)". The facts against the precedents:

* alfa (exception 2026-10-21, gap 0 on 2026-10-26) and lending (2026-10-21) each state a label delay: up to 12 months, and up to 36 months. The gap of that delay breaks the floor whatever the windows are. Avito states no delay. The 3 days are the third-place team's scaled copy of the competition's separation, not a delay.
* The floor breaks because of the 2-day width, not because of the gap. From the builder's daily counts:

  | Windows | Gap | Train shares, newest first | Floor (50%) |
  |---|---|---|---|
  | 2-day | 0 | 85%, 71%, 57% | holds |
  | 2-day | 1 day | 77%, 64%, 49.97% | fails |
  | 2-day | 3 days | 64%, 49.97%, 35% | fails on two windows, not only the oldest (correct the splits comment) |
  | 1-day (26, 27, 28 March) | 3 days | 71%, 64%, 57% | holds |
  | 1-day | 4 days | 64%, 57%, 49.97% | fails |

* Melbourne, ames and perth cannot carry this case either. Their no-selection evidence sits at the edge of the extract (as-of weekly sheets; the extract's last, short month). Avito's file holds ads dated up to 7 April, and Avito also scored the test ads of 12-20 April. So the newest training day was at least 10 days old when the labels were drawn. The stable daily means (0.136-0.141) show that labels settle within about 10 days. They say nothing about a delay of 1-3 days.
* What alfa settled and avito can reuse: alfa's one-month gap would have kept 55% for training, and Lennart still chose gap 0 (2026-10-26). That was the side the panel's advocate and practitioner argued, because "one month does nothing against a delay of up to a year" (alfa REVIEW.md issue 3, in the history of commit 1fc9ee06). If Avito's label matures over 4 days or more, a 1-3 day gap is the same partial gap, and gap 0 follows alfa.
* SPLIT-9: alfa removed a measured shortcut. lending records that none was measured. Avito's draft should say the same as lending, in one line: the seller id is not a feature, and 40-55 test ads per window have a repost in training. The RMSE cost of the gap (0.0008-0.0012) is an effect size, as in alfa's notes, never the reason (SPLIT-4; the trip-time family took a 1-day gap where as few as 8-48 training rows a window had a late label, pkdd; Lennart, 2026-10-21).
* What would settle the fact (EV-1): how long ads stay up after posting, from the competition's `periods_train` file (date_from, date_to). If ads typically stay up for 4 days or more, (a) below holds on data.

**Consistency check (AI, 2026-11-01):** the draft's call on avito_demand_prediction_1m (no gap, an exception to SPLIT-10 that "serves SPLIT-14") would be the third exception of the floor reason, after alfa_battle_2_0_task_2 and lending_club (Lennart, 2026-10-21). Those two state a label delay whose gap breaks the 50% floor whatever the windows. Avito states no delay, and its 3-day gap breaks the floor only with 2-day windows: 1-day windows keep 57-71% for training. What sets avito apart, or makes it the same?
(a) A deal follows buyers seeing the ad, so Avito's label matures over the days the ad stays up after posting. Any gap of that delay, 4 days or more, leaves a window under 50% at every width (1-day windows with a 4-day gap: 49.97%), and a shorter gap does nothing against it, like alfa's one-month gap, which Lennart passed over for gap 0 (2026-10-26). Record it as the third exception of the floor reason with the delay stated; the SPLIT-10 amendment is then due.
(b) Treat avito like the SPLIT-10 cases with a short delay (house_sales, the trip-time family): 1-day windows with a 3-day gap, and no exception.
(c) Reopen alfa_battle_2_0_task_2 and lending_club to match (not suggested: both state their delays).
(d) Change the rule: amend SPLIT-10 so that an undocumented delay allows no gap. This would be a new reason, with avito the first case.

If (a), the amendment proposal (principles.md, "Exceptions and amendments"), worded from the Tensions row: "SPLIT-10 ... When the gap of the label's delay would leave a window's train side under SPLIT-14's floor at any window width, the windows have no gap: SPLIT-9 is met by removing the measurable shortcut, and the delay is stated with the split (alfa_battle_2_0_task_2, lending_club, avito_demand_prediction_1m)."

**Departure 2: `user_id` dropped (CLEAN-3 Should; LEAK-34, USE-10)**

The seller is a known entity for part of the ads: 27% of the newest window's ads come from a seller with an ad at least three days earlier. CLEAN-3 keeps an identifier that carries meaning, and LEAK-34 makes an entity's history legitimate under a temporal split. The draft drops the id because it adds 0.0002 RMSE (0.00016 with a 3-day gap; 0.0009 on the ads of sellers with at least 2 training ads). ieee_fraud_detection kept its `uid` on the same kind of measurement: dropping it moved AUC by only -0.007 to -0.001 (Lennart, 2026-10-01). The draft's issue 3 files this under CLEAN-19 as a "Weigh". CLEAN-19 is a Should, and the id question belongs under CLEAN-3, LEAK-34 and USE-10.

**Consistency check (AI, 2026-11-01):** your call on avito_demand_prediction_1m (drop the seller id, a departure from CLEAN-3) differs from ieee_fraud_detection (uid kept 2026-10-01, the same mechanism: a recurring entity's id worth little under a temporal split), african_credit_scoring_challenge (customer_id kept, shipped 2026-10-26) and brazilian_ecommerce (seller_id kept because "sellers recur over time, the seller is known at checkout", shipped 2026-10-15). What sets avito apart?
(a) Avito's windows have no gap, so a seller id would let a model read the seller's labels from the days just before each window, labels that were not final when the model was refit (SPLIT-9). The three precedents keep their id over settled training labels (ieee and brazilian_ecommerce with a one-month gap, african with a settlement cut). Record it as an exception to CLEAN-3, serving P4 (SPLIT-9). This ties the id to departure 1: under (b) there, the reason weakens.
(b) Treat avito like ieee and brazilian_ecommerce: keep `user_id` as a categorical (USE-10, LEAK-34).
(c) Reopen ieee_fraud_detection's uid to match.
(d) Change the rule: amend CLEAN-3 so that an entity id that adds no measurable signal is dropped.

**Consistent, but the wording should change**

* Issue 1 cites USE-5 and USE-8 (P3). The record's own Assessment calls the label "the output of an undocumented Avito scoring step, not an observed outcome". SEL-3 (Must, P2) asks for "an observed outcome or an expert annotation", and it outranks USE-5. Andrej's `Yes` (2026-10-30) gives no reason under SEL-3. This is a question, not a precedent departure. The fact to record if the curator keeps the target: the host's own judgement of a deal, published as the ground truth of a named task, like an agency's issuer rating (corporate_issuer_credit_rating). One contrary reading exists but is no precedent: valuation's AI screening read an assessor's model output as failing SEL-3 (2026-10-22, AI, unverified, not accepted by a curator).
* The record keeps `No Good Target (yet)` on a `Yes`. coffee_rating_prediction (Lennart) and basque_offshore_* (Andrej, 2026-10-30) have the same pairing, so this is consistent for now. Once issue 1 is settled, remove the marker or keep it with its reason, as ames_housing's `Trivial` was removed after its review (2026-10-26).
* The note on seller history cites CLEAN-6. That is right for label-based counts, and african_credit_scoring_challenge built only a label-free count. The stronger reason here is the unknown delay: there is no settled label to count.

</details>

<details><summary>Advocate</summary>

**Advocate: opening brief, avito_demand_prediction_1m (advocate, 2026-11-01)**

**Position: ship as defined.** Keep the data, the split, the metric and the dropped seller id as they are, and correct the text. No evidence agent found a Must that fails. The six reports agree on the keep: the column audit says "no column has to go and no cleaning step is wrong", the split audit says "right with notes", the practitioner says fit approximate and metric yes, the blind reviewer says "include with changes", and the claim audit says the metric holds. Their real findings are wrong reasons and wrong numbers in the text. The mildest remedy on the ladder fixes those: correct the definition's text. Two points are weighing calls for the curator: the no-gap exception (point 4) and the seller id (point 5).

**1. A real task, and every shipped input is known at posting (P3: USE-1 Must, USE-6 Must; P4: LEAK-10 Must, LEAK-37 Must).**
- *Evidence.* The host's use-case quote holds word for word (claim audit #2): Avito advises the seller at posting. The practitioner: "I have all 14 at posting". The audits looked for post-posting edits and found no signal:
  - 2 titles are marked sold; 58 ads use sold words, mean label 0.097 against 0.139 overall;
  - 741 ads (0.05%) say the price was lowered, mean 0.123;
  - the missing shares of the photo, description and price are flat over the 14 days.
- *Avito's model-made inputs.* `image_top_1` is worth 0.0028 RMSE, less than `price` (0.0049). Against the category-mean residual its Spearman is -0.09, so nothing points to a code fit on these labels (LEAK-27).
- *Rule.* USE-6 and LEAK-37 make a company's own estimate made before the outcome an input.
- *Why it outranks the objection.* Text "as last edited" falls under LEAK-10's second clause: a late value that cannot be located row by row stays with a note when the traceable part shows no gain (onlinenewspopularity, cited by the column audit). Mildest fix: one sentence with these counts in the prediction-point bullet.

**2. The target ships under the rule written for this case (USE-5 Must, amended 2026-10-21 on diabetes_3; USE-8 Must: approximate). SEL-3 holds.**
- *Evidence.* Every target number reproduces (claim audit #11). Among values shared by at least 100 ads, 76.4% still occur in one parent category, so "a scoring step" survives the calibration.
- *The practitioner's facts.* Deals on Avito happen off the platform, and Avito's own team says it cannot know whether a contact led to a purchase (Habr 879680). For this actor, a deal label is always an estimate. In services, every value is a count ratio k/n with n at most 8 (64,385 ads).
- *The score holds information beyond the ad.* The best model reaches R^2 0.27, so the score is not a rule over the columns. That rules out SEL-4 (an unsupervised label) and SEL-5 (a deterministic rule).
- *Precedents.* diabetes_3 (undocumented label, approximate), coffee_rating_prediction (one rating service), corporate_issuer_credit_rating (an agency's own judgement as the target), alfa_battle_2_0_task_2 (no stated horizon).
- *Why it outranks the SEL-3 objection (precedent check).* USE-5's text covers "a label from a named publication whose construction is undocumented". principles.md: "P3 informs P2 ... let the use case decide". The curator's `Yes` (Andrej, 2026-10-30) was given with the undocumented target in the screening and in the Assessment, and a curator's decision ranks above an AI reading. The one contrary reading (valuation) is an unverified AI screening that no curator accepted. The "checked and found to be another quantity" clause does not apply: nothing was checked and found to differ; the construction is unknown, which is the approximate branch.
- *Mildest fix.* Add the services fact and the Habr quote to the target bullet. The curator then removes `No Good Target (yet)` or keeps it with its reason (as ames_housing's `Trivial` was removed).

**3. No leak or copy channel survived the probes (P4: LEAK-16 Must, LEAK-18 Should, LEAK-24 Must, SPLIT-9 Must, SPLIT-13 Should).**
- *Evidence.*
  - Leak probe: no column dominates (all columns R^2 0.185, the best single column `param_1` 0.150).
  - Exact feature copies across the split: 0.05% of the test ads, 0.0% with the text.
  - Hidden-group probe, temporal mode: no hits (claim audit #47, split audit).
  - Same-seller reposts: an oracle blend moves the window RMSE by at most 0.00006.
  - LEAK-24: the daily mean stays at 0.136-0.141, so the newest days are not censored.
- *The seller channel.* A test ad is positive 43.5% of the time after a positive same-seller ad, against 14.7% after zeros only. That is a moderate, persistent trait: 41.5% against 16.0% for ads 4-12 days earlier. Alfa showed 95.1% against 2.3%, an outcome stamped on all of a client's products at once.
- *Why it outranks the objection.* The Tensions row on unmatured labels: SPLIT-9 is met by removing a *measurable shortcut*. The audit measured none. An alfa-style filter would cost 0.0009 RMSE and push the oldest train side to 49.5%, below SPLIT-14's floor, to remove a trait rather than a shortcut.
- *Mildest fix.* One SPLIT-9 sentence with these numbers in `splits_comment`, as lending_club's comment has.

**4. The split is the right regime, and no gap is the right call on measured facts (SPLIT-6 Must, SPLIT-3, USE-10 Must; SPLIT-14 Must holds; SPLIT-10 Should departed).**
- *Evidence.*
  - Train sides hold 66.5%, 66.5% and 57.3% of the ads.
  - The delay was measured in `periods_train`: of the ads activated on 15 March, 96.0% were still listed more than 3 days later, 92.6% more than 7 days later, and 89.4% on 28 March. So the label settles over weeks.
  - A gap of even 4 days breaks the floor at every window width (1-day windows: 49.97%).
  - At equal training size, a 3-day gap costs 0.00024 and 0.00020 RMSE (paired SE 0.00004-0.00005).
- *Rule and precedent.* This is precedent check option (a): alfa's reason, a gap of the delay breaks the floor whatever the windows. Lennart chose gap 0 for alfa even though a partial one-month gap would have kept 55% ("one month does nothing against a delay of up to a year").
- *Why it outranks the objection.* 1-day windows with a 3-day gap meet SPLIT-10 and SPLIT-14 on paper. But that gap is a partial one against a delay of weeks, about 4-7% of the closures by the display proxy. It gives up the longest window that fits (SPLIT-12) for no measured gain. SPLIT-10 is a Should, and this departure serves SPLIT-14, a Must.
- *Concession.* The written reasons are wrong. The cited gap is 4 days, not 3. The floor breaks only because of the 2-day width. The 0.0008-0.0012 RMSE is mostly training size.
- *Mildest fix.* Rewrite the no-gap sentences of `splits_comment` and the end of `fit_reason` with the delay evidence, and record the exception. This is the third exception of the floor reason (alfa, lending, avito), so the SPLIT-10 amendment proposal is due. Curator's call.

**5. Dropping the seller id is the cautious side under a no-gap split (CLEAN-3 Should departed, serving P4: SPLIT-9 Must; LEAK-34 permits the id but does not require it).**
- *Concession.* "`user_id` adds little" is refuted in size. Encoded as the past mean, the id gains 0.0011-0.0015 RMSE overall and 0.004-0.005 on the ads of known sellers (claim audit #17). Those numbers replace the note's.
- *What sets the case apart.* ieee_fraud_detection, brazilian_ecommerce and african_credit_scoring_challenge kept their ids over *settled* training labels (a one-month gap, a settlement cut). Here every training label is still unsettled at refit (point 4), and an id puts the seller's own recent labels within the model's reach. The split audit calls the drop "the SPLIT-9-safe choice".
- *What stays.* The seller's as-of state ships: `item_seq_number` and `user_type`.
- *Why it outranks the objection.* USE-10 decides the regime ("before choosing the split"), and the regime is temporal. LEAK-34 says keeping the id would be legitimate. Neither rule makes dropping it a violation, so the question is CLEAN-3, a Should.
- *Mildest fix.* Record an exception to CLEAN-3 with the corrected numbers (precedent check prompt 2, option (a)). Shipping `user_id` instead is also within the rules, so this call does not block shipping either way.

**6. Worth benchmarking, and scored by the source's metric (P6: TP-2 Should, MET-2 Must, MET-3 Must, MET-4 Should, MET-8 Should; P2: SEL-12 Must holds).**
- *Signal and headroom.* Skill over the dummy is 0.252-0.256 on all three windows, and LightGBM beats linear by 0.037. The competition's single models scored 0.2136-0.2163 against our untuned 0.222, so there is headroom.
- *Metric.* RMSE is Kaggle's `evaluationMetric` and is computable per row on every fold. If the score is a calibrated deal probability, MSE against it ranks models as the Brier score against the deal would (practitioner). The forum's "weird choice" is a complaint, not the evidence of bias MET-4 asks for to overrule a competition metric.
- *Text (SEL-12).* The text adds +0.016 R^2 at the shipped size, and tabular models stay competitive: the 3rd-place team's best LightGBM scored 0.2163, its best neural network 0.2180.
- *Size and target.* 1.5M ads of mixed types, a zero-inflated regression, the family this batch adds. `task_target_value_dominant` is accepted under Andrej's zero policy (2026-10-30), as across this batch.
- *Precedents.* huntprohibited_1m (the Avito sibling, Russian text as strings, shipped 2026-10-26), zillow_prize (MET-4).

**7. Every other finding is a text correction; none touches the data, the split or the metric (remedy ladder: fix the definition; "independent failures are not conflicts": no Must fails).**
- *Wording and counts.*
  - `task_summary.split`: the oldest window trains on all 861,064 earlier ads, not a random million.
  - The competition's test is 12-18 April plus 65 stragglers, not 12-20 April.
  - The 54 town names stand for two to seven regions.
  - 13 of 731,655 consecutive pairs (7 after the drop), not 10.
  - Reposts are 86-126 ads per two-day window.
  - The text gain, at the shipped size.
  - The version comment: 228k, not 227k.
- *Statements to drop, reword or add.*
  - Drop the discussion 56531 quote: the data gives 6.2%, not 30%.
  - Reword the late-ad reason: 33 of 39 checkable ads were posted later. The drop stands: they are outside the release window, 84% positive, and Kaggle participants made the same cut (55897).
  - Replace "negligible" for the 6 copied pairs: each pair comes from two different sellers.
  - Explain the price codes 0 and 1 (CLEAN-10).
  - Add "28 regions, without Moscow or St Petersburg" to `row`.
  - Record the hidden-group result.
- *Optional.* Cast `image_top_1` to integer labels (cosmetic).
- *The blind reviewer.* Three of its four preparation fixes are already in the definition (text as strings, `image_top_1` categorical, the 100 late ads dropped). The fourth, the date as a feature, is the house template for temporal tasks (a datetime in `_feature_types`, kick).

**Judgment record (advocate's reading)**

```text
Verdict: ship after text changes (data, split and metric as defined).
Validity: SEL-3 holds (host's published ground truth, P3 informs P2); USE-1, USE-6 hold; USE-5/USE-8 approximate
  (undocumented score, diabetes_3); LEAK-10 holds with a note on edits; SPLIT-6, SPLIT-14, LEAK-24 hold; SPLIT-9 holds
  (no measurable shortcut); SPLIT-10 departed, exception serving SPLIT-14 (delay of weeks, alfa).
Value: TP-2 real signal with headroom; MET-4 RMSE kept; SEL-12 holds.
Quality: CLEAN-3 departure (seller id) kept as an exception serving SPLIT-9; CLEAN-10 note on price codes.
For the curator: the SPLIT-10 exception and amendment; the seller id (weighing call).
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief: avito_demand_prediction_1m (critic, 2026-11-01)**

**Verdict: ship only after changes.** One Must is open, and only the curator can close it. The label is a scored estimate, but SEL-3 asks for an observed outcome or an expert annotation (point 1). Read strictly, that makes the verdict `No`. If the curator finds SEL-3 met, the dataset ships after one change to the definition (the seller id, point 2) and text fixes (points 3 to 7). I found no leak, and I count no quality point as a reason to exclude.

```text
Verdict: ship after changes, pending the curator's SEL-3 call.
Validity: SEL-3 open (a scored label; USE-5's allowance sits one part lower); USE-10/CLEAN-3 departed on a refuted
  number (seller id dropped); USE-1/USE-8 text overstates the task; SPLIT-10 exception stated on a refuted fact;
  SPLIT-9 holds but is not written down; LEAK-10 and USE-6 hold as far as tested, but the notes lack the numbers.
Value: TP holds (skill about 0.25 over the mean in 3/3 windows); MET-4 holds.
Quality: CLEAN-10 and LEAK-19/LEAK-20 notes; EV-2 corrections.
For the curator: point 1 (SEL-3), point 2 (seller id), point 4 (the SPLIT-10 consistency check).
```

**1. The label is Avito's scored estimate, not an observed outcome, and SEL-3 is not answered (P2, SEL-3 Must).**
- *Problem.* Outside services (95.7% of the ads), the label is a category-level score. My counts on the raw file:
  - 27.4% of the positive ads in goods categories sit on one value per parent category. In six of the eight categories that value is the category's maximum: 0.80323 on 46,668 personal-item ads, 0.76786 on 26,474 electronics ads, 0.86521 on 23,265 home ads. The value 0.7376 sits on 13,922 car ads.
  - 41.8% of these ads sit on a value shared by 1,000 ads or more.
  - Below the ceiling, the values are not fractions of it. Apart from the ceiling itself, only 1-5% of a category's positive ads equal k/n of the ceiling with n of 10 or less.

  Only services (64,385 ads, 4.3%) look counted: 22 values, all k/n with n of 8 or less (domain practitioner; recounted). The data page says a deal cannot be verified. Avito's own seller team writes that it cannot know whether a contact led to a purchase (Habr 879680, domain practitioner).
- *Effect.* On more than 95% of the test ads, the benchmark scores how well a model reproduces Avito's undocumented scoring step, caps included. The blind reviewer puts it this way: "part of the RMSE comes from learning the per-category ceilings".
- *Rule.* SEL-3 (Must, P2): "The target is an observed outcome or an expert annotation."
  - USE-5's allowance for undocumented labels is in P3, one part lower. It cannot carry a SEL-3 failure (principles: "a higher part wins"; "every Must has to hold").
  - Andrej's `Yes` (CC 2026-10-30) gives no SEL-3 reason, and the record still carries `No Good Target (yet)` (precedent checker).
  - The practitioner's Brier argument (MET-8) assumes the score is a calibrated posterior of the deal. Avito never observes the deal, so that cannot be checked. It is also a P6 argument and does not answer P2.
- *Remedy.* No change to the data can fix this. Before the dataset ships, the curator records an explicit SEL-3 call:
  - (a) SEL-3 holds, with the fact that sets this case apart, as in corporate_issuer_credit_rating: the host's own judgment of a deal, published as the ground truth of its named task. That analogy is weaker than it looks. An agency rating is an analyst's judgment, while this score repeats one value on tens of thousands of ads.
  - (b) Amend SEL-3 so that it covers labels scored by the host.
  - (c) `No` with `No Good Target / Scientific Discovery`.

  Whatever the call, the target bullet and `fit_reason` get the two constructions above, and the marker either goes or stays with its reason.

**2. The seller id is dropped on a refuted number, against USE-10 and three precedents (P3, USE-10 Must; LEAK-34 Must; CLEAN-3 Should).**
- *Problem.* The note says `user_id` "adds little" (-0.00023 RMSE). That test gave LightGBM the id as a native category with about 300k levels. Encoded instead as the seller's past mean from the train side, the id cuts RMSE by 0.0015 and 0.0011 on the two newer windows. On the ads of known sellers (31% and 26% of the test ads) it cuts RMSE by 0.0046 and 0.0039. That is 5-6 times what the note says (claim auditor #17).
- *The SPLIT-9 objection does not save the drop.* The seller effect is a lasting trait, not the outcome of the day before:
  - A test ad is positive in 43.5% of cases after a positive ad by the same seller 1-3 days earlier, and in 41.5% after one 4-12 days earlier (split auditor).
  - I measured it on the newest window, with the shipped 1M train sample and the same untuned LightGBM, cutting the seller history 4 days before each row (settled labels only). RMSE is 0.22124, against 0.22084 with no cut and 0.22230 without the seller. On known sellers it is 0.19873, against 0.19710 and 0.20166.
  - So settled history alone keeps 73% of the gain overall and 64% on known sellers.
- *Effect.* As shipped, the model cannot recognise the seller, a cold start this use case does not have. Avito knows the seller at posting. 65% of the ads come from sellers with more than one ad in these 14 days (domain practitioner). The overview lists "historical demand for similar ads" among the inputs.
- *Rule.*
  - USE-10 (Must): the history of a known entity is legitimate.
  - LEAK-34 (Must) says the same for a temporal split.
  - CLEAN-3 (Should): keep an identifier that carries meaning. A departure needs a fact, and the fact given here is refuted.
  - Precedents: ieee_fraud_detection kept its `uid` at a smaller measured gain (Lennart, 2026-10-01); african_credit_scoring_challenge kept `customer_id`, and brazilian_ecommerce kept `seller_id` (precedent checker).
- *Remedy.* Fix the definition: keep `user_id` as a categorical. No label feature is built, so CLEAN-6 holds. If the curator keeps the drop, record it as an exception to CLEAN-3, with the corrected numbers and a fact that holds.

**3. The use case and the row claim more than the benchmark tests (P3, USE-1 and USE-8 Must; text only).**
- "Advise the seller how to improve the listing" needs causal effects. A predictive benchmark tests only "how much interest to expect". An ad without a price scores 0.215 against 0.135, so a model read as advice would tell sellers to remove their price (domain practitioner).
- "Interest" in the use case means views and contacts. The label is a deal score (point 1).
- `row` says "one ad posted on Avito". It is one ad from 28 regions, none of them Moscow, Moscow Oblast, St Petersburg or Leningrad Oblast, and there is no jobs category (domain practitioner; I confirmed the 28 regions, none of the four, and 9 parent categories without jobs).
- Context Avito always has is missing: competing live ads, the seller's history beyond `item_seq_number`, all photos, and the promotion bought. The task is "the demand an ad will meet, judged from the ad alone" (domain practitioner).
- *Remedy.* Notes:
  - `use_case`: say that the benchmark tests the expectation half.
  - `row`: name the regions and the missing jobs category.
  - `fit_reason`: name the narrowed context and the gap between the label and "interest".

**4. The no-gap split rests on a stated fact that is wrong (P4, SPLIT-10 Should; SPLIT-9 Must, not written down; SPLIT-12 Should).**
- *Problem.* The exception says a 3-day gap "leaves the oldest window under half of the ads (SPLIT-14)". That holds only for the two-day windows we chose ourselves:
  - One-day windows with a 3-day gap keep 57-71% of the ads for training.
  - With two-day windows, a 3-day gap fails two windows, not one, and even a one-day gap fails (49.97%).
  - The cited third-place gap was 4 days, not 3.

  Sources: claim auditor #35 and #36, split auditor, precedent checker.
- *The deciding fact is missing.* Labels take weeks to settle: 89.4% of the supplementary ads activated on 15 March were still listed on 28 March (periods_train.csv, split auditor). That is longer than any gap the 14-day release allows. At equal training size, a 3-day gap costs 0.0002 RMSE. The note's 0.0008-0.0012 is mostly the smaller training side.
- *Effect.* The effect on scores is small. But a departure from a Should needs "the fact that sets the case apart and the higher principle it serves" (principles), and the fact written down is refuted. This would be the third exception for the floor reason, after alfa_battle_2_0_task_2 and lending_club, so a consistency check and an amendment proposal are due.
- *Remedy.* A note, not a re-split:
  - Rewrite the no-gap sentences of `splits_comment` and the end of `fit_reason` with the delay fact, the training shares for each window width, the 4-day citation and the horizon reason: two days is the longest window that keeps three windows above the floor (SPLIT-12).
  - Add one SPLIT-9 sentence: reposts are 0.47-0.60% of a window, with an oracle bound of 0.00006 RMSE, and settled seller history carries most of the seller's value (point 2).
  - The curator answers the consistency check (precedent checker, option a), and the SPLIT-10 amendment is proposed.

**5. Cannot-verify items are left without the numbers that test them (P4, LEAK-10 second clause and USE-6/LEAK-37, Must; notes).**
- Edits after posting are rare where the text shows them. There are 2 titles marked sold and 43 descriptions saying "уже продано". 741 ads (0.05%) carry a price-lowered phrase, with a mean label of 0.123 against 0.139 (column auditor). 58 titles carry sold words, with a mean of 0.097 (domain practitioner).
- `image_top_1` tracks the category, not the outcome. Its Spearman correlation with the mean target is 0.41, but -0.09 on the residual after the category mean. Dropping it costs 0.0028 RMSE, about as much as `param_1` to `param_3` (column auditor).
- *Remedy.* Add these sentences to the prediction-point bullet and to the `image_top_1` note, so that both items read as tested as far as the data allows.

**6. The notes contradict the data in places (EV-2 Must; procedure).** None of these changes a decision on its own:
- The 56531 quote ("about 30% of the top 10% are missing prices"): 6.2% measured (claim auditor #24). Drop the quote.
- The text numbers are the leak probe's mean over three windows at 50k training rows, not "the first window". At the shipped size, the text adds +0.016 R^2, and on its own it reaches 0.206 (claim auditor #28). The SEL-12 sentence should carry these numbers.
- The late ads: 33 of the 39 that can be checked carry a higher `item_seq_number` than all of that seller's March ads. They were posted later, not re-dated. Reword the reason; the drop stands.
- Reposts per two-day window are 86, 126 and 87, not 40-55.
- `task_summary.split`: the oldest window trains on all 861,064 earlier ads, not on a random million.
- The competition test covers 12-18 April, plus 65 stragglers on 19-20 April.
- City names: 43 are in two regions, 8 in three, 2 in four and 1 in seven.
- `item_seq_number` runs against the date in 13 of 731,655 pairs on the raw file (7 after the drop).
- The version comment should say 228k, not 227k.
- The price counts on the frame are 85,360 and 4,645.
- The hidden-group probe runs in temporal mode and finds no hits. Record that.

**7. Quality: two codes and one reason (P7 CLEAN-10 Should; LEAK-19/LEAK-20 Should; not a reason to exclude).**
- CLEAN-10: the price codes 0 (4,645 ads, mean 0.35) and 1 (3,696 ads, mean 0.27) are kept but not explained. Most of these ads are animals and services, where the code is the seller's "free" or "contact me" (column auditor).
- LEAK-19/LEAK-20: the 2 copies and 4 conflicting rows are kept as "negligible". The stronger fact is that in all six pairs the two ads come from different sellers, so they are distinct ads (precedent checker).
- `image_top_1` categories are stored as floats (`1008.0`). An `Int64` cast is cosmetic (column auditor, CLEAN-14).
- *Remedy.* One clause each; the cast is optional.

**Dropped, not backed:** the blind reviewer's advice to drop `activation_date` as a feature (the house convention keeps the time column as a datetime feature, as kick does); the terms line, which is never evidence (EV-4).

*Measurements of my own:* the label counts in point 1 and the regions in point 3 are counts on the raw file. The settled-history seller test in point 2 adapts the claim audit's seller script (newest window, shipped 1M sample, seller history cut 4 days before each row).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate: rebuttal, avito_demand_prediction_1m (advocate, 2026-11-01)**

**Where this leaves the case.** The panel agrees on five of the critic's seven points (3 to 7). They are text fixes, and I had proposed most of them. I concede point 2: ship `user_id`. I contest point 1 with a new check: the label is not a score of the ad. The dataset still ships, after one change to the definition (`user_id`) and text fixes. The SEL-3 call stays with the curator, and the check gives it the fact the critic asks for.

**1. SEL-3: the label is a scored estimate. Contested, narrowed to recording the fact.**
- *New check* (on the raw file). A repost is a group of ads with the same seller, title, description, price, category, city and region. There are 4,490 such groups with 10,422 ads in all, mostly posted on the same day. A score computed from the ad would give each copy the same value. The labels differ:
  - Among the 983 groups with any positive ad, only 12.6% hold one value.
  - 71.0% hold a zero and a positive (73.3% when the copies were posted the same day).
  - The rest, 16.4%, have no zero but different positive values.
- *Pairs.* The first two ads of each group correlate at 0.47. Random pairs from the same category and town correlate at 0.135. So the ad sets part of the label (as it should for a predictable outcome), and the rest is decided after posting.
- *What this establishes.* The category levels the critic counted (0.80323 on 46,668 ads) are calibration levels. *Which* ad gets a level is decided per ad, after posting, by something the ad does not contain. Two of the critic's descriptions fail on this:
  - "reproduces Avito's undocumented scoring step": the step's input is what happened to the ad, and no model can read that from the twin ads.
  - "one value on tens of thousands of ads", as the reason the label is weaker than corporate_issuer_credit_rating: the value is shared, but its assignment is per ad.
  The late ads fit this reading too: the 100 ads dated after 28 March are 84% positive.
- *Caveat.* A zero on one twin may be a removal by moderation (Avito blocks duplicates). That is still an event after posting, not a score of the ad. The 16.4% of groups with different positive values cannot be explained that way.
- *Rule.* SEL-3 (Must, P2) asks for "an observed outcome or an expert annotation". The check shows the host's assessment of what happened to each ad, put on a probability scale per category. In substance that is an annotation of an outcome, not a prediction from the ad. SEL-3's examples of a failing target (a scientific-discovery or survey table) do not fit a regression competition published for a decision. principles.md: "P3 informs P2 ... let the use case decide". Avito cannot observe deals itself (Habr 879680), so for this actor an assessed deal is the best real-world target there is.
- *I agree with the critic* that USE-5 alone does not carry a SEL-3 failure, and that the curator should record the call explicitly. Remedy (a) of the critic, with this fact:

  `SEL-3 holds: the host's after-the-fact assessment of each ad's outcome, on a 0-1 scale per category; identical reposts get different labels in 87% of groups with a positive ad, so the label records each ad's outcome, not a score of the ad.`

  Then the marker `No Good Target (yet)` goes. The target bullet and `fit_reason` carry both constructions (the k/n rates in services, the category levels in goods) and this check.
- *I keep* that MET-8 is a P6 argument. I used it for the metric, not for SEL-3.

**2. The seller id. Conceded.**
- *What decides it.* The critic measured that seller history with a 4-day cut keeps 73% of the id's gain (64% on known sellers). The split audit's signature points the same way: 43.5% positive after a positive same-seller ad 1-3 days earlier, against 41.5% after one 4-12 days earlier. The seller effect is a lasting trait, not a shortcut through recent labels.
- *My fact does not single out the id.* I wrote that "every training label is unsettled at refit". That holds for every training row alike, and the Tensions row on unmatured labels puts that diffuse rest under the SPLIT-10 exception, not under SPLIT-9. Only a measurable shortcut must go, and none was measured.
- *What follows.* The departure from CLEAN-3 (Should) has no fact left. USE-10 and LEAK-34 make the history legitimate, and ieee_fraud_detection kept its `uid` at a smaller gain. Mildest remedy that keeps the dataset: fix the definition and ship `user_id` as a categorical. No label feature is built, so CLEAN-6 holds. The cardinality (771,769 sellers) is no argument (Tensions row: a model's input cap is never an argument).
- Drop the seller bullet's "adds little" and its numbers. Replace them with the claim audit's 0.0011-0.0015 overall and 0.004-0.005 on known sellers.

**3. The use case claims more than the benchmark tests. Conceded as text, narrowed on "interest".**
- *Agreed.* `use_case` should say the benchmark tests the expectation half, not advice on what to change (the missing-price example shows why). `row` should name the 28 regions without Moscow, Moscow Oblast, St Petersburg and Leningrad Oblast, and the missing jobs category. `fit_reason` should name the narrowed context: no competing live ads, all photos or promotion bought.
- *Narrowed.* "Interest" against a deal score is not a new gap. The competition is named "Demand Prediction", and the host offers the deal likelihood as its measure of the demand an ad meets. `fit_reason` already names the label as the gap (USE-5, USE-8). One clause can add that the label is a deal assessment rather than views or contacts. It changes no verdict.

**4. The no-gap split. Agreed.** This is my point 4. Keep the split. Rewrite the no-gap sentences with the facts below, answer the consistency check with option (a), and propose the SPLIT-10 amendment for the floor reason (alfa, lending, avito). The facts:
- labels settle over weeks (periods_train);
- the training shares for each window width;
- the 4-day citation, not 3;
- two days is the longest window that keeps three windows above the floor (SPLIT-12);
- at equal training size the gap costs 0.0002 RMSE.

Add the critic's SPLIT-9 sentence. With `user_id` shipped (point 2), it should say that settled history carries most of the seller's value, so the id is a trait and not a shortcut.

**5. Cannot-verify items without their numbers. Agreed** (my point 1 had the same fix). Add to the prediction-point bullet and the `image_top_1` note:
- sold words: 2 titles, 58 ads with a mean label of 0.097;
- price-lowered phrases: 741 ads with a mean of 0.123;
- `image_top_1`'s residual Spearman of -0.09, and the 0.0028 RMSE it is worth.

**6. Notes that contradict the data. Agreed** (my point 7). Every item stands as listed. None changes a decision.

**7. Quality. Agreed.** Add one clause on the price codes 0 and 1 (CLEAN-10). Replace "negligible" with "each copied pair comes from two different sellers" (LEAK-19/LEAK-20). The `Int64` cast is optional.

**Updated judgment record (advocate)**

```text
Verdict: ship after changes (user_id kept as a categorical; text fixes).
Validity: SEL-3 holds on the repost check (per-ad outcome assessment), the curator records it; USE-1, USE-6 hold;
  USE-5/USE-8 approximate; USE-10/LEAK-34 met by shipping user_id; SPLIT-6, SPLIT-14, LEAK-24 hold; SPLIT-9 holds
  (no measurable shortcut); SPLIT-10 departed, exception serving SPLIT-14 (delay of weeks; alfa, lending).
Value: TP-2 real signal with headroom; MET-4 RMSE kept; SEL-12 holds.
Quality: CLEAN-10, LEAK-19/LEAK-20 notes; EV-2 corrections.
For the curator: the SEL-3 call (fact above); the SPLIT-10 exception and amendment (option a).
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: avito_demand_prediction_1m (critic, 2026-11-01)**

**Where we stand.** I answer the advocate's opening brief point by point, and I take into account the one new fact in its rebuttal (the repost check). The advocate and I now agree on almost everything:
- keep the data, the split and the metric;
- ship `user_id` (the advocate conceded it in its rebuttal; a new check of mine, under point 5, supports that);
- make the text fixes.

One question stays with the curator: the SEL-3 call. Both sides now ask the curator to record it, and the advocate's repost check supplies the fact for it. I narrow my point 1 to that. My recommendation: **ship after changes**, meaning `user_id` kept as a categorical, the SEL-3 call recorded, and the text fixes made.

**The opening claim, "No evidence agent found a Must that fails": narrowed.** No Must fails on the evidence. But SEL-3 was open, not settled. The precedent checker raised it, and the record's own Assessment (AI, 2026-10-30) calls the label "not an observed outcome (criterion 3)". Criterion 3 is SEL-3 to SEL-11 (selection.md). The advocate's rebuttal now agrees that the curator records the call.

**Advocate 1 (every input is known at posting): conceded.** Same evidence and the same fix as my point 5: one sentence with the edit counts in the prediction-point bullet, and the `image_top_1` numbers in its note.

**Advocate 2 (SEL-3 holds): narrowed to a recorded call. I concede part of my description.**
- *Conceded on a new fact.* I recounted the advocate's repost check on the raw file (seller, title, description, price, category, city and region all equal), and every number reproduces:
  - 4,490 groups with 10,422 ads;
  - 983 groups hold a positive ad. Of these, 12.6% hold one value, 71.0% a zero and a positive (73.3% of the 828 same-day groups), and 16.4% several positive values with no zero.
  - The 161 groups with several positive values are mostly personal items (74) and real estate (44), that is, goods.

  So within goods, twin ads get different labels. The label depends on what happened to each ad after posting, not only on the ad. My phrase "how well a model reproduces Avito's undocumented scoring step" overstated this. The category values I counted are the levels of a scale; which level an ad gets is decided ad by ad.
- *Still disputed: that the opening brief's arguments already settle SEL-3.*
  - The four precedents settle USE-5 and USE-8, not SEL-3. coffee_rating_prediction and corporate_issuer_credit_rating ship human judgments, diabetes_3 a clinical measure, alfa an observed default.
  - "P3 informs P2" is a valid route, but it only works when it is written into the record with its fact (principles, "Consistent judgement", case 1: a Must has no exceptions).
  - The advocate's rebuttal accepts both points.
- *Caveat on the proposed fact sentence.* The advocate itself notes that the 71% zero-and-positive groups may be duplicates blocked by moderation. The 16.4% with different positive values cannot be explained that way. The sentence should therefore lead with them: "identical reposts carry different positive values in 161 of the 983 groups with a positive ad (and a zero beside a positive in 71%, which may include moderation removals)".
- *Remedy (agreed).* The curator records SEL-3 as met with this fact (or amends SEL-3), and then `No Good Target (yet)` goes. The target bullet and `fit_reason` carry three things: the k/n rates in services, the category levels in goods, and the repost check. There is no change to the data.

**Advocate 3 (no leak or copy channel): conceded for the columns as defined.** SPLIT-9 holds under the Tensions reading. With `user_id` shipped, the SPLIT-9 sentence should give the age profile below, so that the seller channel reads as a trait that has been measured.

**Advocate 4 (the split, no gap): conceded.** This is my point 4 with the same remedy:
- keep the split;
- rewrite the no-gap sentences with the facts: labels settle over weeks (periods_train), the training share for each window width, the 4-day citation, and two days as the longest window above the floor (SPLIT-12);
- give the gap cost at equal training size (0.0002 RMSE);
- record the exception, answer the consistency check with option (a), and propose the SPLIT-10 amendment for the floor reason.

The advocate's claim that a 4-day gap fails at every window width holds: one-day windows with a 4-day gap leave 49.97% for training (precedent checker).

**Advocate 5 (drop the seller id as the cautious side): disputed. The advocate conceded it in its rebuttal, and a new check settles the open fact.**
- *The contradiction in the opening brief.* Point 3 calls the seller signal "a trait rather than a shortcut". Point 5 drops the id for SPLIT-9. Under the Tensions row on unmatured labels, only a measurable shortcut must go, and the diffuse rest falls under the SPLIT-10 exception, which advocate 4 accepts. Every training label is already unsettled; the id adds none.
- *A correction to my own evidence, which cut the other way until checked.* In my opening I called labels at least 4 days old "settled". By the display proxy they are not: 92.6% of ads are still listed 7 days after posting. I also cut the history further back. Newest window, shipped 1M sample, untuned LightGBM, seller past mean and count:

  | seller history used | RMSE | known sellers (30.7%) | test ads with history |
  |---|---|---|---|
  | none (as shipped) | 0.22230 | 0.20166 | - |
  | all train-side labels | 0.22084 | 0.19710 | 30.7% |
  | labels at least 4 days old | 0.22124 | 0.19873 | not counted |
  | at least 7 days old | 0.22179 | 0.20047 | 16.7% |
  | at least 10 days old | 0.22213 | 0.20135 | 10.9% |

  The gain falls with the cut. But the history window also shrinks, from 12 days to 5 and then 2, and so does the share of ads with any history. Label age and history length move together here.
- *The check that separates the two.* I compared two histories of equal length, 8 days each: the most recent 8 days before the window, and 8 days ending 4 days before it. On the 18.7% of test ads whose seller appears in both:
  - structured columns: RMSE 0.18856;
  - recent history: 0.18365 (-0.00491);
  - history at least 4 days old: 0.18407 (-0.00449).

  Older labels give 91% of the gain of the newest ones on the same ads. The age effect is 0.00042 RMSE on 18.7% of the test ads, about 0.0001 at window level. It matches the split audit's signature (43.5% positive after a positive ad 1-3 days earlier, 41.5% after one 4-12 days earlier). So the seller's value is a lasting trait, and the fall in the table above comes from shorter histories, not from label age.
- *Rule.* CLEAN-3 (Should) keeps an identifier that carries meaning. The departure has no fact left. USE-10 and LEAK-34 make the history legitimate. The precedent is ieee_fraud_detection, which kept its `uid` even though it carries labels across the temporal split (Lennart, 2026-10-01).
- *Remedy (agreed).* Ship `user_id` as a categorical. Replace the "adds little" numbers with 0.0011-0.0015 overall and 0.004-0.005 on known sellers, and add the equal-length result to the SPLIT-9 sentence.

**Advocate 6 (worth benchmarking, the source's metric): conceded.** TP-2, SEL-12, MET-2, MET-3 and MET-4 hold. I never disputed the metric. The advocate keeps MET-8 for the metric only, and I accept that.

**Advocate 7 (the rest are text corrections): conceded, with the additions now agreed.**
- `use_case`: the benchmark tests the expectation half, not advice on what to change.
- `row`: 28 regions without the two capitals and their oblasts, and no jobs category.
- `fit_reason`: the narrowed context, and one clause saying that the label is a deal assessment, not views or contacts. I accept the advocate's narrowing that this is part of the label gap already named, not a new gap.

The blind reviewer's date-as-feature point: agreed, it is the house template.

**Judgment record (critic, after rebuttal)**

```text
Verdict: ship after changes (user_id kept as a categorical; SEL-3 call recorded; text fixes).
Validity: SEL-3 for the curator to record as met (the label depends on each ad's fate after posting: twin ads differ in
  161 of 983 groups with a positive ad) or amend; USE-5/USE-8 approximate; USE-10/LEAK-34 met by shipping user_id
  (seller value a lasting trait: equal-length histories 4 days older keep 91% of the gain); SPLIT-9 holds;
  SPLIT-10 departed, exception serving SPLIT-14 (delay of weeks), amendment due; LEAK-10, USE-6 hold with notes.
Value: TP-2 holds; MET-4 RMSE kept; SEL-12 holds.
Quality: CLEAN-10, LEAK-19/LEAK-20 notes; EV-2 corrections.
For the curator: the SEL-3 call; the SPLIT-10 exception and amendment (option a).
```

*Checks of my own in this round:* the repost recount and the two seller-history runs (the 7- and 10-day cuts, and the equal-length recent-against-old comparison) ran on the raw file, following the method of the claim audit's seller script.

</details>
