# numerai_v5_2

**Outcome:** added as `numerai_v5_2_1m`. Numerai's v5.2 tournament data: one row is one stock in one weekly era (an
era is one Friday; Numerai publishes no dates), the target is the stock's 20-day return ranked within the era, the
780 features are Numerai's disguised `medium` set, and three test years of 52 eras follow a 4-era gap. The data, the
split and the use case hold; the review panel recommends shipping after the text changes it asked for, which are in
the definition. The Faith features (75 features Numerai designed with the targets of test eras), the version and `medium`
against `all` are yours to decide; the metric is Numerai's per-era CORR (`mean_group_pearsonr`, MET-4, 2026-10-21).

```text
Verdict: ship after changes.
Validity: SEL-11 holds and TP-10 does not apply (the stock id changes every era, so there is no series per stock;
  a stock's newest known target correlates about 0 with its target; whether some features are trailing returns
  cannot be tested). USE-5 holds (target_ender_20 equals Numerai's `target` on 100% of rows). USE-8 approximate
  (the Faith features, in fit_reason). SPLIT-9/SPLIT-10 hold (the 4-era gap covers the
  3-era overlap of the 20-day targets); inner validation (tuning, early stopping) must hold out a block of later
  eras after a 4-era gap, not random rows (a note in splits_comment). LEAK-31 triggered by the 75 Faith features
  (issue 3). LEAK-27 not triggered (largest single-feature correlation 0.0076). PROV holds (SHA-256 of the three
  files match, 6,881,281 rows, 0 duplicate rows).
Value: TP-2, a small real signal (per-era correlation 0.0071 / 0.0142 / 0.0154, t 3.3 / 7.7 / 8.1); TP-1 open
  until tuned results (as zillow_prize: tuned methods must beat 0.5 window by window); the metric: Numerai's per-era CORR declared (`mean_group_pearsonr`, MET-4, 2026-10-21).
Quality: CLEAN-22: the reason given for `medium` is not admissible (issue 4); CLEAN-10 holds (Numerai's fill of a
  feature-era without data set to missing).
Weighed: source +, size +, realness +, signal - (tiny, fragile on the newest window), leak - (Faith).
For the curator: issue 3 (Faith: drop, or keep through the LEAK-31 item across datasets), issue 7 (v5.2 or v5.3), issue 4 (`medium` or `all`).
```

**Main points:** Drop the 75 Faith features or keep them (issue 3, recommended drop); Numerai's per-era CORR is declared
(`mean_group_pearsonr`, MET-4); keep v5.2 or also open v5.3 (issue 7); measure near-copies and keep
`medium`, or ship `all` (issue 4).

**Record judgment:** valid with concerns. Numerai's own data and use case, first-hand: each Friday a tournament
participant scores every stock, and Numerai trades on the combined scores. A ranking of the stocks within each week,
not forecasting of a series. Concerns: the Faith features (issue 3) and the metric (now Numerai's per-era CORR). Licence: Numerai's
Terms of Service, section 4.2, limit the data to tournament use and forbid redistribution; the terms are in `license`
and are no verdict reason (EV-4, as lucas_topsoil).

**Issues for Lennart:**

3. **Drop the 75 Faith features?** Numerai designs its features to predict the target. The Faith features are a
   family of 372 that Numerai released at era 1192 (late 2025), 75 of them in `medium`; Numerai built them with the
   targets of the eras before, so test eras 1080-1191 lie in their design period. No participant had them in those
   eras.
   - Effect: in those eras a model sees features chosen with its own test labels, so its score is higher than a
     participant could have reached. On the shipped splits, ridge with the 75 gains +0.0043 ± 0.0006 per-era
     correlation in eras 1080-1131 (about 28% of the signal there), +0.0013 ± 0.0007 in 1132-1183 (about 9%), +0.0056
     ± 0.0018 in 1184-1191 and +0.0010 ± 0.0006 after the release. In the newest window only 8 of 52 eras are in the
     design period, so the window mean shifts by about 12% (arithmetic, not a measurement). Midnight, a second family
     of 122 released at about era 1098 inside the oldest test window, shows no gain before its release (-0.0005 ±
     0.0011), so only Faith is in question.
   - Implemented: kept, with a `Potential leak, kept on purpose:` note giving these numbers.
   - Alternative: drop the 75 (705 features left). Cost: the source's published live inputs leave; a build.
   - Rule: LEAK-31 (P4, Should): a selection made with labels that include test rows stays with a note when small and
     goes when we can. It can go here, and the effect is a quarter of the signal in one window. LEAK-38 (anonymised
     fields that may be post-outcome) does not cover it: the values are not post-outcome and the effect is measured;
     the advocate conceded this. Precedent: home_credit_default_risk removed its selection even at zero effect
     (Lennart, 2026-10-19, LEAK-31's only case). The advocate's fact for a keep: these are the source's own published
     inputs, not a third party's selection. Its weakness: in eras 1080-1191 nobody had them, so keeping them does not
     mirror the use case there. A keep would be the third source-published selection kept under LEAK-31, after
     qsar_oral_toxicity and qsar_bioconcentration; the item across datasets "Amend LEAK-31 for a selection the source
     published?" covers the three, so a keep goes through that amendment, not a third exception.
   - Recommendation: drop the 75 (mediator, critic).
   - Decision: drop the 75, or keep them through the LEAK-31 amendment. If `all` is chosen in issue 4, the same call
     covers its 372 Faith features.

   **Lennart (2026-10-26, discuss):** Please explain more slowly what these features potentially mean. Did they just arrive
   later, or were they computed later? We don't care to be faithful to the exact old features at the time of the
   competition. But if these features are correct and they exist in the same way for test data, we should be allowed
   to use thenm no?

   **Answer (AI, 2026-10-26):** both: they arrived late and their history was computed late, and the values are likely
   correct. The problem is how they were chosen.
   - Numerai engineers every feature "to be predictive of the target or additive to other features", and computes
     each value from the data available at its era ("extreme care to make sure all features are point-in-time",
     [docs](https://docs.numer.ai/numerai-tournament/data)). Faith I (186 features, era 1192) was released because a
     model with it "does better than an identical model built on the V5 dataset in nearly every period", and Faith II
     (186 more) added "variations" of "our most powerful features ever released"
     ([forum 8200](https://forum.numer.ai/t/data-v5-1-release-faith/8200),
     [8209](https://forum.numer.ai/t/new-target-for-payouts-and-data-v5-2-faith-ii/8209)).
   - So the features were picked because they predicted the target over past weeks, and those weeks include our test
     eras 1080-1191. It is like choosing features by their test-set score: every value is right, but the set was
     tuned on our test labels, so every model looks better on those weeks than it could on new ones. After the
     release (era 1192 on) your reading holds: there they are fair inputs.
   - The gain fits that: +0.0043 ± 0.0006 per-era correlation in eras 1080-1131 (about 28% of the signal), +0.0013 in
     1132-1183, +0.0056 in 1184-1191, and +0.0010 ± 0.0006 after the release. A drop at the release is what a
     selection effect predicts (a fading edge once public could add to it).
   - Keeping them with clean windows would mean testing only after era 1192: 44 eras (307,129 rows). With Numerai's
     example model that scores 0.0062 ± 0.0027, too few for more than one window, and no more eras will come (v5 is
     retired, issue 7).
   - `medium` itself is not re-chosen: it is the 705 v5.0 features of July 2024 plus 35 Faith I and 40 Faith II.
   - Recommendation unchanged: drop the 75 (705 features left).

7. **Keep v5.2, or open v5.3 as a new record?** v5.3 ("Quantum", July 2026) is Numerai's current release, and its
   payout target is `target_ender_60`, the 60-day return (correlation 0.47 with the 20-day target; it needs a 12-era
   gap and is unresolved for eras 1228-1240). Numerai still updates the v5.2 files weekly.
   - Effect: the v5.2 task is valid either way; v5.3 is the version participants are paid on.
   - Implemented: v5.2 with `target_ender_20`, as the record names it.
   - Alternative: open v5.3 as a new record and folder. Cost: a new download (3.3 + 5.7 GB) and the full add.
   - Rule: TP-6 (P6, Must): a better version the source defines replaces ours. eryhemato_squamous_disease and
     corporate_credit_rating moved to the version their source describes; neither case was a newer payout target, so
     no precedent decides this one. Not disputed by the panel.
   - Recommendation: none; the panel left TP-6's question (is the 60-day payout target the better version?)
     unanswered.
   - Decision: keep v5.2 only, or also open v5.3 as a new record.

   **Lennart (2026-10-26, discuss):** Is it the same data but a different target? then I would create a new record and
   retire 5.2 and move to 5.3? or is it completely new data? how much does it differ? would it justify to keep both
   versions in the benchmark?

   **Answer (AI, 2026-10-26):** the same data with more features, not a new target; keep v5.2 only.
   - v5.3 ("Quantum", 2026-07-16) is v5.2 plus 807 `quantum` features: all 2,748 v5.2 features, its 18 feature sets
     (`medium` included) and its 41 targets are unchanged, and Numerai's staff write "v5.2 is a subset of 5.3". The
     live files share the 6,861 stocks and agree on every shared feature.
   - The 60-day payout target (`target_ender_60`, for rounds from 2026-08-28) is no v5.3 feature: our v5.2 files hold
     it already. Choosing it is a separate call inside v5.2 (it needs a 12-era gap).
   - The quantum features have the Faith problem on every window: released at about era 1229, after nearly all our
     test eras, so LEAK-31 would drop them, which leads back to v5.2. Keeping both versions would ship the same rows
     and targets twice (a duplicate).
   - New fact: Numerai retired v5. "On October 16, 2026, Classic v6.0 becomes available to download, and public
     v5.0–v5.3 training and validation downloads are retired" (docs). Our `download_description` no longer works from
     Numerai; we hold the files, and community mirrors exist (not checked). v6.0 is new data: a new stock universe
     with tickers and dates, 1,040 features (none shared with v5), 24 targets.
   - Recommendation: keep v5.2 as a frozen release, note the retirement in the definition, and open v6.0 as a new
     record for a current Numerai task (its tickers and dates reopen the forecasting question).

4. **Restate the reason for `medium`, or ship `all`?** v5.2 has 2,748 features; the definition ships Numerai's
   `medium` set of 780, which Numerai describes as features "each unique in some way". CLEAN-22 lets a column leave
   only for a reason of the task (a near-copy, a leak), not for runtime or memory.
   - Effect: 1,968 features a participant has are left out. On the newest window `medium` and `all` cannot be told
     apart: their order flips with the random 1M train sample (LightGBM per-era correlation 0.0006 to 0.0088 for
     `medium` over four samples, 0.0044 to 0.0060 for `all` over two).
   - Evidence: the admissible reason would be that the 1,968 are near-copies of the 780; nobody has measured that.
     The column audit adds an unverified counter-point: `medium` holds Faith features, so its membership was fixed
     after era 1192 and could itself be a selection made with labels.
   - Implemented: `medium`, with a note that the two sets cannot be told apart and that the near-copy question is
     not measured.
   - Alternative: `all`. Cost: a rebuild with 2,748 features (1,510 of them with missing eras).
   - Rule: CLEAN-22 (P7, Must). Precedent: coad_colon_adenocarcinoma ships 36,355 features; "a model's input limit or
     runtime is no argument" (Lennart, 2026-10-15).
   - Recommendation: keep `medium` only if a near-copy measurement supports it; otherwise `all` (critic and
     advocate; the mediator leaves it open). Quality only; it does not hold the dataset.
   - Decision: have the near-copy measurement run and keep `medium` if it holds, or ship `all` now.

   **Lennart (2026-10-26, discuss):** taking all features seems more reasonable and leaving it to the model to select or
   prune as needed, also maybe the models we tested for the probes are just not strong enough?

   **Answer (AI, 2026-10-26):** agreed on `all`; the stronger models lift both sets but still cannot tell them apart.
   - With Numerai's own settings, the example model (2,000 trees, learning rate 0.01, depth 5, column sample 0.1) and
     the docs' deep benchmark model (30,000 trees, learning rate 0.001, 1,024 leaves), per-era CORR on the newest
     window is 0.0035-0.0102 for `medium` and 0.0035-0.0108 for `all`, against 0.0006-0.0088 for the probes' untuned
     LightGBM. The sign of all minus medium follows the training sample (+0.0055 and -0.0050 for two samples of the
     same size), and on the full history (6.49M rows) the two tie.
   - Training on the full history helps more than the feature set (newest window 0.0072 to 0.0102).
   - Within `all` the `medium` features carry 26-27% of the gain, about their share of the columns; the other 1,968 add
     no signal of their own, but nothing shows them to be near-copies. So CLEAN-22 gives no task reason to leave them
     out, and `all` costs no score.
   - Recommendation: ship `all`, without its Faith features (issue 3), which leaves exactly v5.0's `all` (2,376
     features). Mark "Change" with issue 3's drop and I rebuild the definition.

**Review panel:** ship after changes (mediator). Claim audit: most claims hold; four were refuted and are corrected
in the notes (the target resolves about five weeks later, not four; the Faith gains are about half the stated size
after era 1184; the Midnight gain does not hold; `medium` does not beat `all`); the licence, the weekly snapshot, the
adapter and the metadata were not tested. Blind review: exclude as prepared, mainly because RMSE cannot rank methods
on a signal this small; its concern about a missing gap does not hold (the definition has the 4-era gap). Agreed: the
temporal split, the gap, the scope reading, the target, the zillow_prize condition, the `History:` line and the text
fixes, all applied. Disputed: the metric (issue 2; the mediator's experiment favours `pearsonr`) and the Faith
features (issue 3); open: the version (issue 7) and `medium` against `all` (issue 4). The mediator's report numbers
these 1-4; they are issues 2, 3, 4 and 7 here.

<details><summary>Claim audit</summary>

**Claim audit: numerai_v5_2_1m (2026-10-20)**

Claim numbers as in `claims.md`. Data: the definition's frame and split plan rebuilt from the raw files
(`scratch_claim/frame.parquet`, `splits.pkl`, 2,025,745 x 782), and the raw v5.2 files. Scripts and logs are in
`scratch_claim/`. Every Python run was capped at 2 threads. Models: Ridge(alpha=1e6) on the bins with NaN set to 2;
LightGBM with 600 trees (lr 0.02, depth 5, 31 leaves, colsample 0.1, min_child 1000), as in the 2026-10-07 analysis;
LightGBM with Numerai's example settings (2000 trees, lr 0.01). Per-era score = Pearson correlation inside each era.

**Table**

| # | Claim (short) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1 | question: rank of the 20-day return within the week | read hello_v52 and the docs | holds | "target ... stock-specific returns ... next 20 (business) days", binned 5 levels | USE-1 |
| 2 | use case: weekly Friday scoring by a participant | docs_data | holds | "eras ... represent the Friday of each week" | USE-1 |
| 3 | row = stock x era, no dates or names | `id` in the raw files | holds | 6,915,716 ids, all unique (not a stock key) | USE-1 |
| 4, 27 | target "known about four weeks later" | target availability by era in the download; era dates estimated from the forum anchor (era 1051 = 2023-02-18) | **refuted (minor)** | at download (era 1240 = 2026-10-03) targets run to 1235: about 5 weeks; the definition's own splits_comment says T-5; forum: the 20-day window starts on the Friday after the round opens | USE-3 |
| 5, 30 | 780 features, bins 0-4 within the era | raw min/max, bin shares per era | holds | all values 0-4; in populated feature-eras every bin holds at most 20.05% | CLEAN |
| 6, 14 | train = random 1M of earlier eras, every era kept | era counts of each train side against the proportional share | holds | chi2 962 / 904 / 872 on 1178 / 1126 / 1074 dof; last 52 train eras 5.10% obs vs 5.11% expected | SPLIT |
| 7 | changes: fill set to NaN, medium set | frame dtypes and NaNs | holds | 290 features carry NaN | CLEAN |
| 8, 9 | fit approximate; everything except designed features known on Friday | single-feature per-era correlation, test windows and train eras | holds (circumstantial) | largest single-feature mean per-era corr 0.0073 (1080-1235), 0.0072 (1-1075): no feature carries the target | LEAK-1 |
| 10 | medium 780 of 2,748 | features.json | holds | small 42, medium 780, all 2,748 | - |
| 11, 52, 32, 58 | targets resolved up to 1235; 1236-1240 data_type test, no target | raw target NaN by era | holds | NaN target only in eras 1236-1240 (34,435 rows, data_type test) | SPLIT |
| 12, 35, 36 | Numerai fills a missing feature-era with 2; no single stock filled | bincount per feature-era over 1-1235 | holds | 290 features have all-2 eras; 0 feature-eras with bin 2 > 25% that are not all-2; bin 2 at most 20.02% | CLEAN |
| 13, 56 | test keeps all rows (327,025-361,712); frame keeps only used rows | split plan | holds | test = every row of its 52 eras; n_test 361,712 / 333,081 / 327,025; 0 unused frame rows | SPLIT |
| 13 | one random order for all windows | train of window k restricted to the eras of window k+1 | holds | 100% of the 948,986 (947,274) such rows are in the next window's train | SPLIT |
| 15 | 6,881,281 rows; frame 2,025,745 | raw counts | holds | 2,746,268 + 4,135,013 = 6,881,281 | - |
| 16, 18, 24, 61 | metadata (year 2025, finance, Other, Anonymized, bibtex, markers) | none | untested | descriptive; "Needs extensive data wrangling" is a judgment | - |
| 17, 67 | licence text | not tested | untested | licence is never evidence (EV-4); terms.html is script-rendered | EV-4 |
| 19, 21, 23 | numerapi download, file sizes, SHA-256 | stat, sha256sum | holds | sizes 323,414 / 2,597,791,287 / 4,417,740,944; all three SHA-256 match; eras 1-574 and 575-1240 | PROV |
| 20, 22 | API serves only the current snapshot; a later download gives the same rows | needs a second download | untested | - | PROV |
| 25, 57 | target_ender_20, 5 levels, regression | raw values | holds | values {0, .25, .5, .75, 1}; Numerai's notebook fits LGBMRegressor | - |
| 26 | built from train + validation, medium | definition | holds | - | - |
| 28 | target_ender_20 == target; era mean 0.5 | raw comparison | holds | equal on 100% of rows of both files; era means 0.49989-0.49997 | - |
| 29 | the other 40 target columns are future returns | raw schema | holds (nit) | 41 target columns; one of the "other 40" is `target`, an alias of target_ender_20 | - |
| 31 | newest window, LightGBM: medium 0.0064 > all 0.0055 > small 0.0011 | same model on other random 1M train samples | **refuted (ranking)** | medium 0.0006 / 0.0062 / 0.0088 (seeds 1-3), 0.0071 on the shipped train; all 0.0060 (seed 1), 0.0044 (seed 2); small -0.0013. The sample moves medium by 0.008; medium vs all flips with the seed | EV-8, EV-9 |
| 33, 34 | era -> integer time column; id not a stock key | frame dtype; id uniqueness | holds | era int32; id unique across all 6.9M rows | - |
| 37 | no duplicate rows | hash of feature rows | holds | 0 duplicate feature rows; 0 test rows in their own train | LEAK-21 |
| 38 | universe 2,314 in era 1 to 6,057-7,231 per era since era 1100 | era sizes | holds (nit) | numbers exact; but eras before 1100 reach 7,309, so "grows" is not monotone | - |
| 39, 64 | LightGBM 0.006 / 0.014 / 0.018 per era, t 3.0 / 7.2 / 8.7; R2 <= 0.0003 | refit on the shipped splits | holds (fragile on the newest window) | 600 trees: 0.0071 (t 3.3), 0.0142 (7.7), 0.0154 (8.1); example 2000 trees: 0.0068, 0.0153, 0.0183; R2 -0.0004 to 0.00025. Ridge over 5 other train samples: newest window 0.0020-0.0073 (t 0.8-3.7), the others t 3.6-13 | TP-1, TP-2 |
| 40, 70 | constant 0.5 beats LightGBM and ridge under RMSE on the newest window | RMSE on the shipped split | holds | 0.223675 const vs 0.223692 ridge, 0.223693 LGBM, 0.223716 example LGBM; on the two older windows the models beat the constant by 0.00001-0.00003 | EV-5 |
| 41 | TabArena adapter accepts only rmse | not re-read here | untested | code fact, not data | - |
| 42 | faith released at era 1192; 75 faith in medium | hello_numerai.ipynb; features.json | holds | `get_loc("1192")` in Numerai's notebook; 75 of 372 faith features in medium; era 1192 estimated 2025-11-01 | LEAK-30 |
| 43, 65 | ridge faith gain +0.0041 / +0.0016 / +0.0097 / +0.0019 | ridge with and without the 75 faith features on the shipped splits, paired per era | **partly refuted (magnitudes)** | +0.0043 +- 0.0006 (1080-1131), +0.0013 +- 0.0007 (1132-1183) hold; +0.0056 +- 0.0018 (1184-1191) and +0.0010 +- 0.0006 (1192-1235) are about half the stated values; direction holds | LEAK-30, EV-8 |
| 44 | midnight features add +0.0017 in 1080-1097 | ridge without the 122 midnight features | **refuted** | -0.0005 +- 0.0011 (18 eras); +0.0001 after 1098 | LEAK-30, EV-8 |
| 45 | kept because every method sees them | rule reading | holds as a reading | a weak leak (+0.001-0.006 per era) kept with a note, LEAK-30 tension row | LEAK-30 |
| 46, 62, 66 | neutralization is post-processing | fn_v52.ipynb | holds | operates on predictions per era | - |
| 47, 68 | numerai28_6 is an older, era-less sample | prior log v_numerai28_6.log | untested here | not re-run | PROV-6 |
| 48, 49, 50 | 3 windows of 52 eras, gap 4, train ends at start-5 | split plan | holds | test 1184-1235 / 1132-1183 / 1080-1131; train 1-1179 / 1-1127 / 1-1075; gap 4 eras | SPLIT |
| 51 | at era T the newest known target is T-5 | download at era 1240 has targets to 1235; era dates estimated | holds | consistent with the forum's start-on-the-next-Friday rule | SPLIT |
| 53 | Numerai's notebook skips only 3 eras | read hello_v52 code | holds | `[last_train_era + i for i in range(4)]` includes the last train era itself | - |
| 54, 55 | rationale (long OOS, 3 windows) | none | untested (rationale) | - | - |
| 59 | missing only in older eras: 4.97% / 0.006% / 0 over 290 / 10 / 0 features | frame | holds | 4.969% / 0.0059% / 0; 290 / 10 / 0 features; last all-2 era 894 | CLEAN |
| 60 | NaN features float32, others int8 | frame dtypes | holds | 290 float32, 490 int8 | - |
| 63 | assessment: eras, target, windows | as above | holds | - | - |
| 69 | priority 2 | judgment | untested | - | - |
| 71 | reference URL | - | untested | - | - |

**Claims nobody wrote down**

| Implied claim | Test | Result | Evidence |
|---|---|---|---|
| Every feature known at the prediction point | single-feature per-era correlation; 1-NN probe | holds (circumstantial) | max per-era corr 0.0073; 1-NN R2 -1.1 (leak_probes.log); only the Faith and Midnight design-period selection, already noted |
| No row copied across the split | hash of feature rows; near-copy probe | holds | 0 exact copies; 12.8% near copies at 0.85, but the 1-NN target R2 is negative: same stocks in other weeks, not label copies |
| The split is the one the use case needs | gap against target resolution | holds | train ends 5 eras before test, exactly when the newest target resolves |
| The target is the real-world target | docs | holds | v5.2's payout and main target is the 20-day one (`target` == `target_ender_20`); v5.3 moved to 60 days (record issue 6) |
| Train sample does not decide the result | ridge and LightGBM over other random 1M train samples | concern | newest window: LightGBM 0.0006-0.0088, ridge 0.0020-0.0073 by sample; one sample in five gives no signal (t 0.2-0.8) |

**Refuted, ranked**

1. **C44, Midnight design-period gain** (P4, LEAK-30, Should): -0.0005 +- 0.0011 on the shipped splits, not +0.0017.
   Effect: the second leak concern goes away. Remedy: write "the 122 midnight features show no measurable gain before
   their release (-0.0005 +- 0.0011)".
2. **C43, Faith gain magnitudes** (P4, LEAK-30): direction and the 1080-1183 numbers hold; 1184-1191 is +0.0056, not
   +0.0097, and after the release +0.0010, not +0.0019. Effect: none on the keep decision. Remedy: state the numbers of
   the shipped splits, or say which train sample the old numbers came from.
3. **C4 / C27, "known about four weeks later"** (P3, USE-3, wording): the data and the source give about five weeks
   (T-5). The gap is right; the text disagrees with its own splits_comment. Remedy: "about five weeks later".
4. **C31, medium beats all** (P7, CLEAN, EV-8): within the noise of the train sample (medium 0.0006-0.0088 by seed, all
   0.0044-0.0060). Remedy: say medium and all are not distinguishable at this size; the choice rests on size and fit
   time.

Concern (not a refutation): C39 holds on the shipped train sample, but the newest window's signal depends on which
random 1M rows are drawn (1 of 5 ridge samples t 0.8). Relevant for TP-1/TP-2 and the window choice (C55).

**Untested**

C17/C67 licence (EV-4: never evidence), C20/C22 snapshot behaviour (needs a later download), C41 adapter metric (code,
not data), C47/C68 numerai28_6 (not re-run), C54/C55 rationale, C16/C18/C24/C61/C69/C71 metadata and judgments.
Era dates (C4, C51) rest on a forum anchor, not on a Numerai document.

Sources: https://forum.numer.ai/t/eras-to-years-mapping/6188 (era 1051 = 2023-02-18; target window starts the Friday
after the round opens).

</details>

<details><summary>Column audit</summary>

**Column audit: numerai_v5_2_1m (re-check, full tier, 2026-10-20)**

Prediction point (first `curation_comments` bullet): every Friday after the close (one era), score each stock from its
features as of that day; target = its 20-market-day return rank, known about 4 weeks later.

Frame: rebuilt from the definition through `dataset_io.from_definition` (2,025,745 rows x 782 columns: `era`, target,
780 features; 490 int8, 290 float32 features, 1 int32). Raw checks on the full 6,881,281 rows (eras 1-1235). Scripts
and logs: `scratch_column/stats.py`, `stats.log`, `feature_stats.csv` (one row per feature), `raw_checks.py`,
`raw_checks.log`. Correlations are on samples (300k rows of eras 1080-1235 and of eras < 1076; 150k rows for the
column-pair check).

Codebook: Numerai documents the features only as "meticulously designed and engineered by Numerai", "point-in-time",
"attributes as of that point in time", binned 0-4, "missing feature-eras use the middle bin 2"
(docs.numer.ai/numerai-tournament/data; the page now describes v6). Families come from `features.json` (v5.2).

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `era` | weekly date index (Numerai publishes no dates); era 1 is about Jan 2003 (faith release at era 1192 = Oct/Dec 2025) | yes, it is the Friday | int32 from the string "0001"; time column, sorted; 1,235 eras, no NaN; also a model feature (781 features probed); target corr 0.0013 on the test eras | fine | CLEAN-3, CLEAN-14 |
| `target_ender_20` | stock-specific 20-market-day return, ranked and binned within the era; equals `target` (raw check: 100% equal) | no, the label (resolves about 4 weeks later; gap 4 eras is the split auditor's) | float32, 5 levels with shares 5/20/50/20/5% (not quintiles), per-era mean 0.477-0.522 in the sample, 0 NaN in kept rows | fine | CLEAN-15 |
| intelligence (12 + 2 shared with sunshine) | unknown (obfuscated, v4-era family) | yes per Numerai (point-in-time); designed before the test windows | int8 bins 0-4, no missing era | fine | LEAK-38, LEAK-32 |
| charisma (92 + 22 with sunshine + 2 with constitution) | unknown | yes, as above | 2 + 22 float32 with missing old eras (first data by era 192 / 106) | fine | CLEAN-10 |
| strength (52 + 2 with constitution) | unknown | yes, as above | int8, complete | fine | |
| dexterity (21) | unknown | yes, as above | 1 float32 (first era 14) | fine | CLEAN-10 |
| constitution (130 + 4 shared) | unknown | yes, as above | int8, complete | fine | |
| wisdom (56) | unknown | yes, as above | int8, complete | fine | |
| agility (58) | unknown | yes, as above | 4 float32 (first era up to 205) | fine | CLEAN-10 |
| serenity (26 + 8 with sunshine) | unknown | yes, as above | int8, complete | fine | |
| sunshine (98 + 32 shared) | unknown (v4.2 family) | yes, as above | 98 float32; 16.5% missing in eras 1-574, none after 894 | fine | CLEAN-10 |
| midnight (122) | unknown (released about era 1098) | values yes; design overlaps test eras 1080-1097 (+0.0017 +- 0.0012 ridge, not significant) | 108 float32, first data by era 79 | fine, noted | LEAK-31, LEAK-38 |
| faith (75) | unknown (released with v5.1/v5.2, era 1192) | values point-in-time per Numerai, but designed with the targets of test eras 1080-1191 | 55 float32; 17.9% missing in eras 1-574, first data by era 482; mean abs. corr with target 0.0025 (others 0.0006-0.0025) | potential leak, weak, kept on purpose | LEAK-31 (Should), LEAK-38 |
| 2 features in no family (`feature_dividual_uncomplaisant_freeing`, `feature_phototactic_dire_ethnarchy`) | unknown | yes, as above | int8, complete | fine | |
| `id` (raw index, not read) | row id; 4,169,448 distinct of 4,169,448 validation rows, so no stock id across eras | n/a | dropped | fine | CLEAN-3, LEAK-17 n/a |
| `data_type` (raw, not read) | train / validation / test (unresolved) | n/a | used as the row filter, dropped | fine | CLEAN-15 |
| 40 other `target_*` (raw, not read) | other future returns (20 and 60 days) | no, post-outcome | not loaded | fine | LEAK-10 |
| the other 1,968 of `all` (not read) | Numerai features outside `medium` (incl. 666 `rain`, 297 more `faith`) | yes (as above) | not loaded | question | CLEAN-22 |

Checks behind the feature rows (all 780 features):

* Missing values (CLEAN-10): on the full data, 28,390 feature-eras take a single value, every one of them 2; no
  feature-era has 2-4 distinct values; in populated feature-eras each bin holds 19.92-20.05% of the stocks (bin 2 at
  most 20.02%). So the fill is per feature-era, never per stock, and the NaN rule catches all of it. Missingness is
  whole-era, ends by era 894, and cannot follow the outcome (LEAK-10: missingness not caused by the outcome).
* Within-era binning is a cross-section of the same Friday, known at the prediction point: not a statistic over all
  rows (LEAK-30, LEAK-29 do not apply). The NaN conversion also uses only the era's own cross-section.
* Copies (CLEAN-5): no exact duplicate column; 1 pair at |r| = 0.990, 31 above 0.95, 255 above 0.9 (largest
  `feature_dreggy_jansenism_arborvitae` / `feature_veteran_philhellene_chantal`); near-copies stay. The bundle checks skip
  this check above 50M cells, so this is its only run.
* Single-column signal: max |corr| with the target 0.0076 (test eras) and 0.0076 (train eras); no column stands out
  (leak probes: every single feature R^2 about 0, all features -0.022).
* Dtypes (CLEAN-14): ordinal bins as numbers is right; the int8 / float32 mix only follows which features have a
  missing era.

**Problems, ranked (principles.md)**

1. **P4, LEAK-31 (Should) with LEAK-38: the 75 `faith` features were designed with the targets of test eras
   1080-1191.** Evidence: release at era 1192 (v5.3 notebook, per the definition); the paired ridge gains in the
   definition (+0.0041 in 1080-1131 against a LightGBM signal of 0.018, about a quarter; +0.0097 in 1184-1191 against
   +0.0019 after release); here faith has the highest mean |corr| of any family on train eras (0.0031). Weak in
   absolute terms, not small relative to the signal. Mildest remedy: keep with the existing `Potential leak, kept on
   purpose:` note (LEAK-38 covers host-designed anonymised fields). Note: the definition's stated reason, "every method
   sees them", is not the rule's reason; cite LEAK-31/LEAK-38 (small, host-designed, revisit) instead. Alternative:
   drop the 75 (705 left) or start the test windows after era 1200 once there are enough eras. Curator call (issue 3).
2. **P4, LEAK-31 (question): the `medium` set itself.** It contains the faith features, so Numerai fixed its
   membership at or after era 1192, after two of the three test windows. If membership was chosen with the targets, the
   choice of 780 columns is a selection over the test eras; Numerai describes `medium` as features "each unique in some
   way" (not by importance, unlike `small`), so this is unverified. Evidence that would settle it: Numerai's statement
   of how `medium` was built, or the `medium` vs `all` gap on eras before 1080 against the gap on the test eras.
3. **P7, CLEAN-22 (Must): 1,968 of 2,748 features are left out, partly for width.** Issue 4 argues from frame size
   (14.8 GB), pipeline memory and fit time (3.5x), which CLEAN-22 and EV-4 exclude as arguments. The admissible
   reasons are that `medium` is the source's own set (CLEAN-1, a Should, cannot outrank a Must) and point 2's
   selection question, which cuts the other way. Mildest remedy: record why `medium` is the task's feature set in a
   way CLEAN-22 allows (for example that the `all` extras are near-copies, the `rain` variants or legacy equivalents,
   if the data shows it), else switch to `all`. Question for the curator.
4. No other column problem: `era`, target, missing-value handling, dropped `id` / `data_type` / other targets and the
   780 features' dtypes hold (rows above).

</details>

<details><summary>Split audit</summary>

**Split audit: numerai_v5_2_1m (2026-10-20, re-check, full tier)**

Folder `datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/`. Scripts and outputs: `scratch_split/` (s1_load.py: built
frame and split boundaries, full-data era counts; s2_lag.py -> lag_overlap.json; s3_alt.py -> alt_split.json;
s4_era.py -> era_feature.json; s5_inner.py -> inner_validation.json). Thread caps 2 on every run. The container was
rebuilt from the definition by `dataset_io.load` (no build path in the README record).

**Verdict: right with notes**

Temporal on `era`, three 52-era windows (1184-1235, 1132-1183, 1080-1131), train = random 1M of eras before a 4-era
embargo (train ends 1179 / 1127 / 1075). The regime, the gap and the windows match the use case; the alternative (IID)
is badly optimistic, measured below.

**Facts measured**

1. **Regime (USE-10, SPLIT-1, SPLIT-3, SPLIT-13).** The use case scores every stock of the current week, most of them
   known stocks with a past; a stream of weekly eras. Temporal is the right regime; a grouped (new-stock) split would
   answer a question no participant faces, and `id` changes per era, so no stock key exists anyway (SPLIT-24 would bar a
   similarity cluster).
2. **The gap covers the label overlap (SPLIT-9, SPLIT-10).** Matching each stock of era T to its 1-NN in era T-k on the
   780 features (L1; a clear match when d1 < 0.5 d2) and correlating the targets, at T = 1184 / 1132 / 1210:

   | lag k | 1 | 2 | 3 | 4 | 5 | 6-10 |
   |---|---|---|---|---|---|---|
   | target corr | 0.60 / 0.61 / 0.62 | 0.42 / 0.36 / 0.39 | 0.20 / 0.14 / 0.21 | 0.01 / -0.03 / 0.02 | 0.01 / -0.00 / -0.01 | within +-0.04 |
   | clear-match share | 98-99% | 92-97% | 81-94% | 68-88% | 56-75% | 21-58% |

   The 20-day targets of a stock overlap for 3 eras, as 15/20, 10/20, 5/20 days would predict. Train ends at T-5 for
   the first test era (the newest target known then, matching eras 1236-1240 unresolved in the download): the 4-era gap
   removes every overlapping row with one era to spare. No training row has a label unknown at the prediction point.
3. **IID alternative (SPLIT-29, SPLIT-1).** Same 72,342 test rows (20% of eras 1184-1235), same train size 289,370;
   per-era Pearson correlation (mean, t):

   | model | shipped temporal | IID within the same eras |
   |---|---|---|
   | LightGBM (600 trees, Numerai-like) | -0.0007 (t -0.2), R^2 vs 0.5 -0.001 | 0.261 (t 53), R^2 +0.026 |
   | 1-NN (10k test rows) | -0.011 | 0.618 |
   | 20-NN | -0.003 | 0.279 |

   An IID split rewards recognising a stock next to its own overlapping label; the hidden-group probe's 12.8% near-copy
   share (14 coarse columns) understates it: on all 780 features 98% of stocks have a clear match one era back.
4. **Windows and training history (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-20).** Expanding train side; train-side share of
   the full data 94.4% / 89.5% / 84.8% (>= 50%). Each window is 52 weekly eras, one full year, so no season-shaped
   window. Train is a uniform random 15% of rows per era (TabReD convention, version_comment), so the last 52 train eras
   hold 51k-56k of the 1M rows; Numerai's own examples train on all eras, so all history is the right history. The
   universe grows from 2,314 to about 6,500 stocks; no break that calls for cutting early eras.
5. **`era` is shipped as a feature (781 features).** It is known on the Friday (LEAK-10 holds) and out of range in test.
   LightGBM 300k rows, full window: window 1 corr 0.0063 without / 0.0061 with, window 3 0.0114 / 0.0133; `era` takes
   0.6-0.8% of the gain. No measurable effect.
6. **Inner validation inside train.** A random 80/20 hold-out of the window-1 train side (300k fit, 200k validate):
   LightGBM 0.040 (t 16.8), 1-NN 0.090; an era-blocked hold-out (eras 1128-1179 after a 4-era gap): LightGBM 0.004
   (t 1.1), 1-NN 0.000. TabArena's task-specific validation is forward for a `time_on` task
   (`resolve_holdout_split`, autogluon_utils.py) but has no embargo; at ~15% row density and a validation block of many
   eras the 3 overlapping boundary eras are a small share, so the forward path is nearly clean. A model run without
   task-specific validation (random bagging) would select on a 10x-optimistic score.

**Problems, ranked (principles.md)**

1. **P4, Should (SPLIT-10 applied to inner validation; EV note).** Overlapping 20-day labels make any random hold-out
   inside the train side optimistic (fact 6). Not a fault of the outer split, which is honest. Mildest remedy: a sentence
   in `splits_comment` that inner validation must be era-blocked with a 4-era embargo (TabArena's forward holdout
   already blocks; an embargo there is a benchmark-side change). Curator question, not a re-split.
2. **P4, note (SPLIT-13, SPLIT-29).** Stocks recur across eras and are recognisable from their features (98% at lag 1);
   under the temporal split with the gap this is a known entity, legitimate (USE-10), and carries no label (lag >= 4
   correlation ~0). Keep; the measurement could replace the 12.8% probe figure in REVIEW.md as the hidden-group answer.
3. **P4, note (SPLIT-12).** A model frozen for 52 weeks while participants retrain more often; and per-window scores are
   noisy (LightGBM on a 289k-row train sample scored -0.0007, on 300k with the full window 0.0063). Window length is
   argued in REVIEW.md issue 5; no change.
4. **P7, cosmetic.** `era` kept as a feature (no effect, fact 5); `horizon_unit` / `gap_unit` "weeks" on an int index
   (checker info): optional `steps`. Optional drop of `era` from features; no remedy needed.

Outside the split (for the leak auditor): window 1 includes eras 1184-1191 of the Faith design period (LEAK-27 to
LEAK-31), already issue 3.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: numerai_v5_2_1m (2026-10-20, re-check, full tier)**

Actor (USE-1): I am a Numerai tournament participant (and, behind me, Numerai's meta model). Each round, after the
market close, I download the live features of the current universe (~6-7k stocks), score every stock, and submit the
scores. I am paid (stake-weighted) on per-era CORR of my ranked predictions against the 20-day target and on MMC, my
contribution to the meta model; scores resolve about a month later.

**Fit: approximate (USE-8)**

The rows, the inputs and the label timing mirror my weekly submission (features as of the era, 20-day target, 4-era
embargo), but the score (pooled RMSE) is not what I am paid on, and the 75 Faith features carry target information
from the test years.

I agree with the definition's `fit = "approximate"`; its `fit_reason` names only the Faith leak and should also name
the metric gap. USE-9 does not lift it to direct: no other practitioner use case is scored by pooled RMSE on a
within-era rank.

**1. Inputs at the prediction point (USE-3, USE-6)**

* Have: all 780 `medium` features as of the era; Numerai ships them in the live file the same day. The binning within
  the era is what I get live too. The missing-bin to NaN change is what a careful participant does; fine.
* Have but not given: the other 1,968 features of `all` (a choice the curator measured: `medium` beats `all` on the
  newest window, so this is no loss), and the 40 auxiliary targets, which I train on (multi-target ensembles are
  standard) but which are not inputs at prediction time. Not having them is correct for the benchmark.
* Should not have: the 75 Faith features in eras 1080-1191 are inputs I do have live, but their values were designed
  by Numerai with the targets of those eras (LEAK-10 kind; kept on purpose, USE-12). Live, a feature never knows its
  future; here it partly did (+0.004 and +0.010 per-era CORR in the design period against +0.002 after).
* Era id: I know the era, but no participant uses it as a feature; it is the time column only. Correct.

**2. Target (USE-5)**

* `target_ender_20` is the target I am scored on (CORR20 uses the main target), so the label is the real one.
* What I output is a ranking within the era, not a number; Numerai rank-gaussianises my scores before scoring. The
  level and scale of my prediction do not matter to me at all.
* RMSE over the pooled test rows rewards shrinkage towards 0.5: on the newest window the constant 0.5 beats LightGBM
  and ridge. I would never use a model chosen that way. This is the largest gap: the target is right, the scoring of
  it is not what I act on. Per-era Pearson/Spearman (Numerai's CORR) would be.

**3. Row vs decision; the test data (USE-10, SPLIT)**

* My decision is one era's submission: the whole cross-section at once. A row is one stock in one era, and the score
  that matters is computed within an era and averaged over eras. Pooled RMSE ignores that grouping; per-era
  correlation would respect it.
* The entities are known stocks, but ids are hidden and per-era, so no stock history is usable; that mirrors my live
  situation (Numerai hides it from me too). USE-10 does not apply in practice.
* Test: the next 52 eras after a 4-era embargo, train on a random 1M of the earlier eras. This mirrors a participant
  who trains once and submits for a year, which many do. Most retrain a few times a year on all eras (or every 4th
  era to cut overlap of the 20-day targets); a random 1M of rows is a reasonable stand-in for that. The 4-era gap is
  the right embargo (the source's notebook skips 3; 4 is stricter).
* Numerai has submitted daily rounds since 2024, but the training data and the scoring stay weekly-era; the weekly
  framing is fine.

**4. Would I use this model?**

* Trust: the data is Numerai's own, the timing is honest, the signal is real and consistent (per-era CORR
  0.006-0.018, t = 3-9 in all three windows), which is the size I expect ("+/- 0.05 is normal").
* Distrust: a model ranked first here by RMSE may be the one that predicts closest to a constant; I would rank models
  by mean per-era CORR and its Sharpe (mean / std over eras), and look at feature-neutral CORR and max drawdown. I
  would distrust any gain concentrated in eras 1080-1191 because of the Faith features.

**Gaps ranked by how much they change the task**

1. Metric: pooled RMSE instead of per-era correlation (USE-5 at the resolution I act on; the fit cannot be direct).
   Changes which model wins, since shrinkage beats signal under RMSE.
2. Faith features designed with test-era targets (USE-8 approximate, USE-12 keep the task; LEAK-10). Inflates
   per-era CORR by 0.004-0.010 in 2 of the 3 windows; every method sees them, so the ranking effect is smaller.
3. No per-era grouping in the score: one decision is one era, not one row (USE-1 checklist item 1).
4. Train is a random 1M sample instead of all eras (or every 4th era) and is not retrained within the test year;
   matches a lazy participant, fine for a benchmark.
5. Feature set fixed to `medium` (measured as best; minor).

**What an expert would change**

* Score with per-era Pearson or Spearman CORR (Numerai's own), averaged over eras; at minimum report it next to RMSE.
  If the benchmark can only score regression by RMSE, say in `fit_reason` that RMSE ranks shrinkage, not stock
  selection.
* Drop the 75 Faith features, or move the test windows after era 1192 once enough post-release eras exist (the
  definition already names this as the revisit).
* Add the metric gap to `fit_reason` (USE-8: name the known gap).
* Feature neutralization stays out of the data (it is a post-processing step); agreed.

**Sources**

* `datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/dataset.py`, its README.md and REVIEW.md; `curation/records/numerai_v5_2.md`
* `.claude/skills/knowledge-curation/references/use_case.md` (USE-1, USE-3, USE-5, USE-8, USE-9, USE-10, USE-12)
* Numerai docs, Correlation (CORR): https://docs.numer.ai/numerai-tournament/scoring/correlation-corr
* Numerai forum, scoring and payouts (CORR, MMC): https://forum.numer.ai/t/changing-scoring-payouts-again-to-mmc-only/6794
* Numerai example scripts (embargo, every-4th-era training, neutralization): https://github.com/numerai/example-scripts

</details>

<details><summary>Blind review</summary>

**Blind review: numerai_v5_2 (target_ender_20)**

**Verdict: exclude as prepared** (at most "include with changes" if rebuilt with an era embargo, the full rows, and a per-era rank-correlation metric; I would still not use it as a general regression benchmark).

**Task**
Numerai tournament: obfuscated stock features (era = weekly date), predict the 20-day relative return of each stock, as ranks within each era. Hedge-fund participants make this prediction weekly to stake on it. The use is real, but the decision depends on the ranking within an era, not on the RMSE of a pooled regression.

**Concerns (most serious first)**
1. **There is almost no signal at this size, so the scores are noise.** I took the 200k-row sample, trained LightGBM on eras <=600/800/1000 and tested on later eras. Pooled corr was -0.003 to 0.000, R2 about -0.0013, per-era rank-corr mean -0.006 to +0.002 (std 0.08-0.09, 50% of eras positive). The largest univariate |corr| on train is 0.015. Feature-target correlations from train and test agree at only 0.06. Even with the full data, Numerai models reach a per-era corr of about 0.02. A pooled R2/RMSE metric cannot rank methods on that. Change: score with the mean per-era Spearman (Numerai CORR), or drop the dataset.
2. **The target is ordinal on 5 values** {0, .25, .5, .75, 1}, with 50% at 0.5. It is rank-binned within each era, so regression on raw values ignores the per-era ranking. The source notebook calls it "the previous 20-day payout target". The main `target` is not the one used here.
3. **The 20-day target overlaps across weekly eras.** Targets in the last ~4 train eras overlap the test period, and task.md mentions no embargo. Change: leave a gap of at least 4 eras before each test window. In my runs the gap changed nothing because there is no signal to leak.
4. **Era composition is uneven.** Rows per era range from 31 to 762 in the sample. Eras <=600 hold only 25% of the rows, yet the public train file alone has 2,746,268 rows in about 574 eras. The full 2.0M rows must therefore be a subsample that I cannot trace. Document it.
5. **Missing values follow the feature version.** 291 float features are NaN in the early eras (100% in era 1, 0 after about era 500). This is consistent with features added later. It is fine, but it shifts the distribution over time.
6. **The features are obfuscated.** The values are ints 0-4 and the 780 names are random words, so plausibility and meaning cannot be checked. I found no exact duplicate rows.

**Could not check**
The full 2.0M rows, how the 2.0M was built from the 2.7M train plus validation files, the exact split boundaries, and stock IDs (there are none, so I could not check for cross-era copies of the same stock). The source page has no data documentation, and I read only the first part of hello_numerai.ipynb.

</details>

<details><summary>Precedent check</summary>

**Precedents: numerai_v5_2 (`datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/`)**

**Inputs:**
- the panel's register of cases. Its flags list has no entry for numerai, g_research or zillow, so every pairing below comes from reading the cases themselves.
- the panel's `REVIEW_before.md` and `checklist.md`
- the record `curation/records/numerai_v5_2.md` and the definition `dataset.py`
- the sibling records numerai28_6, g_research_crypto_forecasting, stock and cryptocurrency_closing_price_prediction
- the Cases tables of `task_probes.md`, `leak_checks.md` and `selection.md`
- the across-dataset items in `datasets/_dev/tabarena-v0pt2/REVIEW.md`
- the REVIEW.md files of g_research_crypto_forecasting_1m, zillow_prize and qsar_bioconcentration (all 2026-10-20)

**No curator decision exists on numerai yet.** The record has two AI assessments and no `CC` line. Its `suggestion: Yes` and `checked_by: Lennart` have exactly the status of g_research's (an import, with no dated acceptance). So everything below compares the AI's implemented choices and the open issues with the precedents.

**Per decision**

**D1. Scope: in scope as a cross-sectional fixed task (P2; SEL-10, SEL-11, TP-10, all Must)**
- **Verdict:** departs from the nearest sibling, with a stated reason that is only partly tested.
- **Precedents:**
  - g_research_crypto_forecasting: panel recommends `No` + `Time-series (Forecasting)`, 2026-10-20, `datasets/_dev/tabarena-v0pt2/g_research_crypto_forecasting_1m/REVIEW.md` issue 1. It fails TP-10 on both legs.
  - ashrae_great_energy_predictor_iii: kept, 2026-10-15, after passing both legs (`task_probes.md` Cases).
  - stock and cryptocurrency_closing_price_prediction: `No` + forecasting (records).
  - numerai28_6 has a CC: "stock market predictions might also be seen as time-series".
- **The stated reason:** the g_research review itself says "numerai_v5_2 differs in its source's point-in-time features, which are no lagged target" (leg 2). Two further facts would set numerai apart:
  - the stock id changes every era, so the data holds no per-entity series a model could forecast;
  - the features are Numerai's, not lags of the target that we built.
- **What is untested:**
  - Leg 2: the features are obfuscated, so whether some of them are trailing returns (in effect a lagged target) cannot be checked.
  - Leg 1: if TP-10 applies, it would fail here exactly as in g_research. The constant 0.5 beats LightGBM and ridge under RMSE on the newest window.
  - Whether TP-10 applies at all depends on whether a panel with no published entity id is "a panel with one series per entity".
  - The g_research advocate's argument (the actor ranks assets cross-sectionally) was rejected there as needing an amendment. Numerai's keep must not rest on that same argument.

> **Consistency check (AI, 2026-10-20):** your call on numerai_v5_2 (in scope) differs from g_research_crypto_forecasting (recommended `No`, 2026-10-20; the same kind of target: an asset's residual return over a horizon, with near-zero signal under RMSE). What sets numerai apart?
> (a) The ids change per era, so there is no entity series, and the features are the source's point-in-time attributes, not lags of the target, so TP-10 does not apply. Record this as the reading of SEL-11/TP-10, with the untested leg-2 fact named.
> (b) Treat numerai like g_research (`No` + `Time-series (Forecasting)`).
> (c) Reopen g_research to match numerai (the TP-10 amendment item).
> (d) Amend TP-10 to cover cross-sectional asset ranking explicitly.

**D2. Keep despite `no_signal`, `drift_baseline` and `unstable` (P6; TP-1 Must, TP-2 Should)**
- **Verdict:** the direction (keep) is consistent; the evidence departs from the standard of every earlier TP-2 keep.
- **Precedents:**
  - forest_fires (Lennart, 2026-10-06): TabPFN-3.5 beats the mean on 26 of 32 folds under RMSE.
  - mortgage (2026-10-07): LightGBM beats the baseline log loss in 3 of 3 quarters.
  - african_credit_scoring_challenge (2026-10-07): AUC 9 of 9, under the shipped metric.
  - clock_protein_toxicity and asp_potassco (Lennart, 2026-10-06).
  - zillow_prize (panel, 2026-10-20): kept on condition that "if tuned methods do not beat the train mean window by window, the dataset goes to `TBD -> 2nd Tier`".
- **The departure:**
  - Each of those keeps showed models beating the dummy under the metric that ships. Numerai's signal (t = 3.0-8.7) is a per-era correlation that does not ship. Under RMSE, the constant beats both fitted models on the newest window, and the untuned probes lose on all three windows.
  - TP-1 (Must) asks for tuned results, and there are none.
  - Unlike zillow, sf_permit_time and bias_correction, the note does not say "re-check with tuned results".
  - The g_research mediator read the same pattern as "real under correlation, not separable from the noise under RMSE"; there it was moot under `No`.

> **Consistency check (AI, 2026-10-20):** your call on numerai_v5_2 (keep under TP-2) rests on a signal measured by per-era correlation, while forest_fires (kept 2026-10-06) and mortgage (2026-10-07) showed a signal under the shipped metric. What sets numerai apart?
> (a) Numerai's real decision is scored by per-era correlation and the signal is significant in all three windows. Keep with zillow's condition: tuned methods must beat 0.5 under the shipped metric window by window, or the dataset goes to `TBD -> 2nd Tier`.
> (b) Treat it like the precedents: hold it until the shipped metric shows the signal.
> (c) Reopen nothing; record that TP-2 accepts a signal under the source's own measure.
> (d) Amend TP-2 to say which measure of signal counts.

**D3. Metric RMSE instead of Numerai's correlation (P6; TP-6 Must against definitions.md "Field mapping")**
- **Verdict:** consistent with one group of precedents and departs from the other. The stated reason does not set numerai apart.
- **Follows:**
  - g_research_crypto_forecasting (RMSE "until dataset-specific metrics are supported")
  - zillow_prize (RMSE, not the competition's MAE)
  - african_credit_scoring_challenge (default metric kept)
- **Departs from:** these definitions set their competition's metric although the adapter falls back to the default all the same (`BENCHMARK_CHANGES_TODO.md`, "Dataset-specific metrics"):
  - amex_non_iid_1m (`amex_metric`)
  - allstate_claims_severity (`mae`)
  - 5g_energy_consumption (`mape`)
  - sepsis_prediction_1m (PhysioNet utility)
- **Why the reason fails:** numerai's note says "TabArena's adapter accepts only `rmse` for regression". The same adapter limit holds for those four, so it does not distinguish numerai.
- **No curator decision on either side.** The open item "TP-6 and definitions.md disagree on a competition's metric" (`datasets/_dev/tabarena-v0pt2/REVIEW.md`) proposes an amendment: the source's metric replaces ours when it scores what the use case needs and can rank model outputs. Under that wording numerai's CORR would qualify. Numerai is not listed in that item; it appears only in the G-Research item "decide numerai_v5_2 and g_research alike".
- **A fact for that item:** Numerai's CORR is a mean over eras, so it needs the era grouping, like the PhysioNet utility per patient. `pearsonr` over pooled rows is not Numerai's score.

> **Consistency check (AI, 2026-10-20):** your call on numerai_v5_2 (ship `rmse`) differs from amex_non_iid_1m, allstate_claims_severity, 5g_energy_consumption and sepsis_prediction_1m (each ships its competition's metric under the same adapter limit). What sets numerai apart?
> (a) Numerai's score needs the era grouping, which the metadata cannot express yet, so RMSE ships with a note until a grouped metric exists. Record it in the TP-6 item.
> (b) Treat it like amex: set the correlation as `metric` now.
> (c) Reopen the four to match the default.
> (d) Settle it through the proposed TP-6 amendment, with numerai added to its list.

**D4. Faith features kept as a potential leak (P4; LEAK-31 Should, LEAK-27 Must as a question)**
- **Verdict:** departs without a reason that sets the case apart.
- **Precedents:**
  - home_credit_default_risk: the kernel's importance-based selection removed, even at zero effect (Lennart, 2026-10-19). This reversed the CC of 2026-10-01, which had kept it. It is LEAK-31's only case.
  - qsar_bioconcentration (panel, 2026-10-20): the mediator recommends dropping the 9 selected descriptors, effect ≤ 0.015, and offers an amendment, "a selection the source published stays with a note when small".
  - qsar_oral_toxicity (panel, 2026-10-20): LEAK-31 read as very weak, no remedy.
  - kick: fit `approximate` with a potential leak kept (USE-8). Numerai's fit follows it.
- **Why it departs:**
  - LEAK-31 says to keep with a note *when small*, and to remove *when we can*. Removal is possible here: drop the 75 columns, leaving 705.
  - The effect is not small against this signal. LightGBM gains +0.0109 in eras 1184-1191 against +0.0008 after the release; ridge gains +0.0097 against +0.0019. From the note's numbers, the design-period excess comes to roughly a quarter of the newest window's LightGBM correlation of 0.0064 (my arithmetic).
  - The definition's reason, "because every method sees them", holds for every leak, so it does not set the case apart.
  - The note and the checklist cite "the leak_checks precedent ... kept and noted". The rule's only case went the other way.
  - LEAK-32 (anonymised features that *may* hide a transform: no action) does not cover a design-period excess that has been measured.
  - Open question, not a finding: if Numerai *built* the Faith features from a model fit on targets, rather than selecting them, LEAK-27 (Must) would apply. The obfuscation prevents a test.

> **Consistency check (AI, 2026-10-20):** your call on numerai_v5_2 (keep the 75 Faith features, a departure from LEAK-31) differs from home_credit_default_risk (selection removed, 2026-10-19; the same mechanism: supervised feature design on labelled rows that include test rows). What sets numerai apart?
> (a) The features are the source's own published set that every participant receives, and the excess fades after release. Record this as an exception (serving P5), or as the qsar_bioconcentration amendment, though the "when small" condition does not clearly hold here.
> (b) Treat it like home_credit: drop the 75 columns.
> (c) Reopen home_credit to match.
> (d) Amend LEAK-31 (source-published selections).

**Third-case watch:** qsar_oral_toxicity, qsar_bioconcentration and numerai would be the third keep of a source-published selection under LEAK-31. If the curator keeps all three, the amendment proposed in qsar_bioconcentration is due, not three exceptions.

**D5. Feature set `medium` (P7; CLEAN-22 Must, EV-4)**
- **Verdict:** the outcome may hold, but the arguments depart from the rule.
- **Precedent:** coad_colon_adenocarcinoma ships 36,355 features; "a model's input limit or runtime is no argument" (Lennart, 2026-10-15).
- **The departure:** issue 4 argues with fit time (3.5 times), frame size (14.8 GB against 3.4 GB) and pipeline memory (200+ GB). CLEAN-22 rules all three out.
- **Admissible reasons:**
  - `medium` is a set the source defines and recommends ("each unique in some way"); under CLEAN-22, columns may leave as copies.
  - 105 `all` features are empty before era 575.
  - `small` was correctly rejected (an importance selection, LEAK-31). Whether `medium` was chosen with labels is untested.

> **Consistency check (AI, 2026-10-20):** your call on numerai_v5_2 (`medium` over `all`) cites runtime and memory, which coad_colon_adenocarcinoma (2026-10-15) ruled out. What sets numerai apart?
> (a) `medium` is the source's own de-duplicated set ("each unique"), so the dropped columns leave as near-copies. Restate the reason without runtime or memory.
> (b) Treat it like coad: ship `all`.
> (c) not applicable.
> (d) Amend CLEAN-22 to admit infrastructure limits.

**D6. Licence noted, not a verdict reason (EV-4; selection.md "Ethics, licence")**
- **Verdict:** consistent.
- **Precedents:** lucas_topsoil (licence rule, Lennart, 2026-09-23); numerai28_6 issue 2.
- **Ordering:** REVIEW_before puts the licence first, ahead of the P3, P4 and P6 issues. That departs from "What the curator reads first" (rank order). The checklist's draft already moves it to third.

**D7. numerai28_6 as a duplicate of numerai_v5_2 (P5; PROV-6, PROV-7)**
- **Verdict:** consistent.
- **Precedents:** older versions or cuts of one source with the same task were marked duplicates:
  - colleges (Lennart, 2026-10-12)
  - melbourne_housing_snapshot (2026-10-12)
  - indabax_eswatini_2022 (2026-10-12)
  - arsenic_male_lung (2026-07-27)
- **The checklist's concern is answered:** numerai28_6's collections are `TabArena Reject` and `TabSTAR`, so no shipped Data Foundry collection holds it. TabSTAR is no reference (EV-4, Lennart, 2026-10-15).
- **Still open:** its record still reads `suggestion: 'Yes'` until its issue 1 is decided.

**D8. Numerai's bin-2 fill set to missing (P5/P7; CLEAN-11, PROV-13)**
- **Verdict:** consistent.
- **Precedents:** documented sentinels set to missing in sdss_17 (-9999), heart_disease_va_long_beach (chol 0) and churn_telco_south_asia.

**D9. Split and training history (P4; SPLIT-9, SPLIT-10, SPLIT-19, SPLIT-20)**
- **The gap:** 4 eras for a label delay of about 4-5 weeks is consistent with sf_permit_time (6-month label gap) and g_research (1-day gap).
- **SPLIT-19:** the windows depart from the source's train/validation boundary at era 575, and the splits comment gives the reason (three windows near the newest data). That is a departure with a reason.
- **The training history:**
  - Like g_research, the train side is a random sample of the whole history (the TabReD `_1m` protocol).
  - g_research got issue 6 for it (SPLIT-20 Should, no use-case reason written); numerai has neither an issue nor a `History:` line.
  - Of the two, only aeolus_1m and g_research carry a `History:` note.

> **Consistency check (AI, 2026-10-20):** the training history of numerai_v5_2 (all eras, no reason written) is not raised, while the same choice in g_research_crypto_forecasting (2026-10-20) is issue 6. What sets numerai apart?
> (a) Numerai's example model trains on every available era (untested here). Write it as the `History:` reason.
> (b) Raise it as an issue, as for g_research.
> (c) Drop g_research's issue 6 to match.
> (d) not applicable.

**D10. Target `target_ender_20` and version v5.2 (issues 6 and 7; P3/P6; USE-5, TP-6 Must)**
- **No departure yet, and no decision.**
- TP-6 (Must) asks whether a version the source defines is better: v5.3, with its payout target `target_ender_60`. Precedents:
  - eryhemato_squamous_disease (2026-10-06): replaced by the stage the source describes.
  - corporate_credit_rating: rebuilt under a new record (2026-10-16).
- The issue presents v5.3 as optional and does not answer TP-6's question.

**D11. Reproducibility (issue 8)**
- No precedent found in the register; nothing to compare.

**Drift and third exceptions**
- **Drift:** none. There is no curator decision on numerai. home_credit's change between 2026-10-01 and 2026-10-19 was deliberate: LEAK-31 was written on the 19th.
- **Third exceptions:**
  - LEAK-31: see D4. Numerai would be the third keep of a source-published selection, so the amendment becomes due.
  - TP-6 (metric): an amendment is already proposed in the cross-cut item. Add numerai to its list.
- **Writing:** the record's 2026-10-07 assessment says "two test windows". The note's era range 1080-1191 touches all three.

</details>

<details><summary>Checklist</summary>

**Checklist: numerai_v5_2_1m (re-check, 2026-10-20)**

Folder `datasets/_dev/tabarena-v0pt2/numerai_v5_2_1m/`. Run folder P = this folder. Re-check mode: steps 0-3 skipped, no
curation decision changed, `dataset.py` untouched.

**Automated**

* `dataset list`: imports and validates (temporal_non_iid, checked). `uvx ruff@0.15.15 check`: clean; `format --check`:
  already formatted.
* `dataset check`: 0 errors, 0 warnings, 2 info (`dataset_duplicates_skipped`, `meta_time_horizon_unit`), 1 accepted
  (`task_target_low_cardinality`). Log: `P/dataset_check.log`. Peak RSS 53 GB, 2:47 min.
* README diff: the checksum moved from `v2:985f08...` to `v2:8a62d2...`, and the README gained `time_gap: 4` /
  `time_gap_unit: weeks` and the REVIEW.md file row. `dataset.py` is unchanged since commit 58ee235; the split
  metadata now records the gap (`src/data_foundry/v2/dataset.py` writes `time_gap`), which explains the new checksum.
  Not a drift of the data.
* `meta_time_horizon_unit` (info): `era` is an int32 week index, so "weeks" cannot be cross-checked; each era is one
  week by Numerai's docs, so the unit is right. Optional edit: `horizon_unit="steps"`, `gap_unit="steps"`.
* `dataset_duplicates_skipped` (info): measured by hand instead (below).
* Record pointer: `sync-notebooks --check` clean (v2_path matches).
* Raw files: present; SHA-256 of all three match `download_description`.

**Probes (outputs under `P/probes/`)**

* Leak probes (3 splits, 50k rows per side, 300 single features): all features R² -0.022, depth-2/3 tree -0.001, no
  single feature or missing indicator above 0, drop-one changes nothing, exact feature copies test-in-train 0.0%, 1-NN
  R² -1.1. No leak flag. `probes/leak/numerai_v5_2_1m.json`.
* Task probes (3 splits, 50k rows): best family random forest skill -0.005, LightGBM -0.011, linear -0.014; flags
  `no_signal`, `drift_baseline`, `unstable`, the same three as on 2026-10-07. `probes/task/`.
* Hidden groups (temporal: entity on the train side): no entity-like column, no composite key; near-copy clusters at
  similarity 0.85 on 14 columns put 12.8% (11.5-13.5%) of test rows next to a train row. `probes/hidden/`.
* Duplicates and split boundaries (own script on the full frame): 0 duplicate feature rows, 0 duplicate full rows, 0
  test feature rows found in train, 0 index overlap; train eras 1-1179 / 1-1127 / 1-1075 against test 1184-1235 /
  1132-1183 / 1080-1131 (4 eras left out each); 0 missing targets; target values {0, 0.25, 0.5, 0.75, 1}.
  `probes/duplicates_and_splits.json`.

Reading the task flags (evidence.md, "Reading a probe"): first the flag itself. The probe's untuned models on 50k
sampled rows score by R² / squared error, which the stated note already says RMSE cannot separate from shrinkage. The
first reading of `no_signal` (a bug in the target) does not hold: the target is the source's `target` column, binned
0-1 as documented, with no NaN. The second (a split that removes the signal) does not apply to a temporal split of a
weekly cross-section. The third (a small real signal) is what the notes claim, with the per-era correlation of a
Numerai-shaped LightGBM on 1M rows (t = 3.0-8.7, measured 2026-10-07, not re-run here). `drift_baseline`: the target is
ranked within each era (mean 0.5 by construction), not censored: every era 1080-1235 has resolved targets and data_type
`test` eras are dropped; reading 2 (no level drift; the constant is optimal by design). `unstable`: reading 3 (a small
real signal). TP-1/TP-2: keep is consistent with the existing note; whether RMSE makes the task worth benchmarking
stays the open question (TP-3, REVIEW_before issue 2).

The hidden-group reading: stocks recur across eras with no stock id (by design: `id` changes per era). A model may
recognise a stock from its features in later eras; at the prediction point a stock's history is legitimately known, so
the temporal split is the right regime (SPLIT-29). The 12.8% near-copy share on 14 coarse-binned columns is
circumstantial and not a leak reading.

**The checks, in rank order**

| Rank | Check | Verdict | Evidence | Rules |
|---|---|---|---|---|
| P1 | Ethics | pass | Stock data obfuscated by its publisher for ML use; no subjects. | SEL-1 |
| P2 | Scope | pass | Numerai publishes it for a predictive tournament: rank each stock's 20-day return per weekly era; a cross-sectional prediction, not series forecasting of one entity. | SEL-2 to SEL-15, TP-10 |
| P2, P5 | Real data | pass | Real equities, obfuscated (Numerai docs); no generated marks (no formula, tree depth 3 R² -0.001). Underlying data cannot be inspected (obfuscation). | SEL-16, PROV-3 |
| P3 | Use case and fit | concern | Actor, moment and decision are named (tournament participant, Friday, submission); `fit="approximate"` names the Faith-feature gap. The real decision (Numerai's trading) is scored by per-era correlation, which the shipped metric does not measure (USE-8: the fit should name the metric gap too). | USE-1, USE-2, USE-8, USE-9 |
| P3, P4 | Target and metric | concern | Target complete in every test era (0 NaN; eras 1236-1240 dropped). Metric RMSE: the constant 0.5 beats fitted models on the newest window (note, 2026-10-07); task probes: best untuned R² -0.005. RMSE barely measures the task. | USE-5, EV-5, LEAK-22 to LEAK-26 |
| P4 | Available at prediction time | concern | All features are as of the era's Friday (docs); the 4-era gap covers the 20-market-day label delay (train ends 1179 for test 1184). Faith features (75) were designed by Numerai with targets of eras 1080-1191 (ridge +0.0041/+0.0016/+0.0097 per era; claim 43, not re-run here): a design-time leak kept on purpose. | USE-3, LEAK-1, LEAK-2, LEAK-10 to LEAK-12, SPLIT-9, SPLIT-10 |
| P4 | Irreversible and all-row leakage | concern | Features are binned per era (within-row-era statistics, no future rows): fine. The Faith/Midnight feature design is a supervised selection over labelled eras that include test windows (the leak_checks precedent: feature selection on the full labelled set, kept and noted). | LEAK-13 to LEAK-15, LEAK-27 to LEAK-31 |
| P4 | Copies across the split | pass | 0 duplicate rows, 0 test feature rows in train (own script, full frame); leak probe 5: 0.0%. Recurring stocks have no id by design. | LEAK-16 to LEAK-21, SPLIT-29 |
| P4 | Split regime | pass | Temporal on `era`, three 52-era windows, 4-era gap matching the label delay; train sub-sampled at random over all earlier eras (TabReD convention). Verified boundaries in `probes/duplicates_and_splits.json`. | SPLIT-1 to SPLIT-31 |
| P5 | Source | pass | Numerai itself (numer.ai/data/v5.2, example-scripts repository); year 2025 for v5.2. The bibtex cites Numerai's dataset page. | PROV-1, PROV-2, PROV-8 to PROV-12 |
| P5 | Uniqueness | concern | numerai28_6 (OpenML 23517) is an older sample of the same source (note bullet: not added separately). If numerai28_6 is in any collection the two overlap in source; the curator should confirm it is not shipped. | PROV-4 to PROV-7 |
| P5 | Damage and repair | pass | Numerai's middle-bin fill for missing feature-eras is repaired to NaN (decision 1: 4.97% of values in eras 1-574, none after 894). | PROV-13 to PROV-15 |
| P6 | Worth benchmarking | concern | Probe flags no_signal, drift_baseline, unstable, answered by a note (TP-2, small real signal per-era correlation t = 3.0-8.7). Every fold scorable (regression, 327k-362k test rows). Whether RMSE spreads methods is untested with tuned methods (no BeyondArena results: new dataset). | TP-1 to TP-10 |
| P7 | Dtypes and cleaning | pass | Features int8 bins 0-4, float32 where a feature-era was set to NaN (291 columns); `era` int32; `id` and `data_type` not kept; the 40 other targets not read. | CLEAN-1 to CLEAN-24 |
| procedure | Notes match the code | concern | Every bullet is implemented. Two notes rest on measurements of 2026-10-07 that were not re-run here (claims 31, 39, 40, 43, 44). The fit_reason says "75 released at era 1192"; the note says the same; the record's assessment says "designed over two test windows", while the note says eras 1080-1191, which spans parts of all three windows (1184-1191 in the newest): the record line is imprecise. | writing.md |
| procedure | Licence and citation | concern (noted, not a verdict reason) | `license` quotes Numerai ToS §4.2: tournament use only, no redistribution, confidential. Shipping a container conflicts with it. Citation names Numerai's dataset page. | EV-4, PROV-10 |
| procedure | Reproducibility | concern | The API serves only the current weekly snapshot (no versioned URL); `LAST_ERA = 1235` and the SHA-256 pin our files, and the local files still match the hashes (checked 2026-10-20). A fresh download reproduces the rows only if Numerai never revises past eras; the raw files (7.0 GB) need a backup. | |

**Draft issues for the curator, in rank order**

1. Metric and task worth (P3/P6, USE-8, EV-5, TP-3): RMSE ranks shrinkage towards 0.5; untuned probes all below the
   dummy. Same as REVIEW_before issue 2; nothing new measured.
2. Faith features designed with test-era targets (P4, LEAK-27 to LEAK-31): kept and noted; same as issue 3.
3. Licence (procedure, EV-4): same as issue 1.
4. Reproducibility (procedure): same as issue 8; the local raw files still match the SHA-256.
5. Uniqueness against numerai28_6 (P5, PROV-4 to PROV-7): confirm the older sample is not shipped in a collection.
6. Minor: `meta_time_horizon_unit` info; the record assessment's "two test windows" wording against the note's era
   range 1080-1191 (three windows).

**Cannot verify here**

* The per-era correlation numbers of the notes (claims 31, 39, 43, 44): measured 2026-10-07 on the full 1M train side;
  not re-run (the probes here are untuned on 50k rows and score R²).
* Numerai's current Terms of Service text and the v5.2 notebook's embargo wording: not re-fetched in this run.
* Tuned-method spread (TP-3): no BeyondArena results exist for this new dataset.

</details>

<details><summary>Advocate</summary>

**Advocate: ship numerai_v5_2_1m as defined (opening brief, 2026-10-20)**

Position: ship, with three text fixes and one curator condition. Every real problem the evidence agents found has a fix
milder than dropping the dataset. Those fixes are wording, one note and a re-check with tuned results. None of them
re-splits, re-targets or removes the data.

**1. The split is honest and mirrors the application (P4; SPLIT-9 Must, SPLIT-10 Should, SPLIT-1)**

- **Evidence (split audit, fact 2).** Each stock was matched to its nearest neighbour in earlier eras, and the targets
  were correlated. The correlation is 0.60 at lag 1, 0.36-0.42 at lag 2, 0.14-0.21 at lag 3, and -0.03 to 0.02 at lag 4.
  So a target overlaps the next 3 eras. Train ends at T-5. That is the newest target known at T, and it matches eras
  1236-1240 being unresolved in the download. The 4-era gap removes every overlapping row, with one era to spare. The
  gap is also one era stricter than Numerai's own notebook (claim audit, C53).
- **Evidence (split audit, fact 3).** The IID alternative on the same test rows scores a per-era correlation of 0.261
  (t 53). The shipped temporal split scores -0.0007. The temporal split is what makes this benchmark honest, and the
  definition already has it.
- **Against the blind review's concern 3 ("no embargo").** The definition has the embargo. The clean room did not show
  it.
- **Why it outranks.** This is the highest-ranked check the data could fail, and it holds. The one split problem found
  is that a random inner hold-out is optimistic (fact 6). That is a property of the benchmark harness, not of the outer
  split. The mildest remedy is one sentence in `splits_comment`: inner validation must be era-blocked with a 4-era gap.

**2. In scope: a fixed cross-sectional task, not series forecasting (P2; SEL-11 Must narrows SEL-10; TP-10)**

- **Evidence: there is no entity series.** `id` is unique across all 6,881,281 rows (claim audit, C3/C33). The target
  is a rank within the era, with era means of 0.49989-0.49997 (C28). So there is no level to forecast.
- **Evidence: the naive forecast is measured, and it fails.** A matched stock's latest known target (lag 5) correlates
  0.01 / -0.00 / -0.01 with its target (split audit, fact 2). The model reaches a per-era correlation of
  0.0071 / 0.0142 / 0.0154 on the shipped splits (claim audit, C39). So the model clearly beats the naive per-entity
  forecast, which is leg 1 of TP-10.
- **My inference, not measured.** Under RMSE, a lagged value with zero correlation would score about
  sqrt(2) x 0.2237 = 0.32, against 0.2237 for the models.
- **Leg 2.** Numerai publishes the features as point-in-time attributes it designed. Neither the source nor we built
  lags of the target.
- **What sets it apart from g_research (precedents D1).** g_research has persistent asset ids and lag-based features.
  Here the id changes every era. That is option (a) of D1. It does not rest on the "the actor ranks cross-sectionally"
  argument that was rejected for g_research.
- **Conceded as untested.** Whether some obfuscated features are trailing returns is unknown. The 1-NN lag table bounds
  what such features could carry: about 0 beyond lag 4.

**3. A real use case with its real target (P3; USE-1, USE-5, USE-8 Must)**

- **Evidence.** `target_ender_20` equals Numerai's `target` on 100% of rows (C28). It is the target v5.2 participants
  are paid on (practitioner, section 2).
- The inputs, their timing and the embargo mirror a live weekly submission (practitioner, sections 1 and 3).
- The practitioner rates the fit `approximate` and agrees with the definition.
- **Real gap, mildest fix.** The `fit_reason` names only the Faith features. Add the metric gap (USE-8 asks to name
  the known gap): "pooled RMSE, not Numerai's per-era correlation, ranks the models". This is one sentence; nothing
  changes in the data.

**4. The signal is real and consistent; keep it under TP-2 (P6; TP-2 Should, TP-1 Must)**

- **Evidence.** The per-era correlation is significant in all three windows on the shipped splits: t = 3.3 / 7.7 / 8.1
  with 600 trees, and 0.0068 / 0.0153 / 0.0183 with Numerai's example model (C39).
- For scale, Numerai says "+/- 0.05 is normal in quantitative finance" for per-era scores.
- **Tensions table.** "The right split against the score: the split follows the application; a small signal under it
  is no reason to retire" (forest_fires, R^2 0.013).
- **Against the blind review's concern 1 (no signal).** Its runs used a 200k sample with training cut at eras
  600/800/1000. The measurement on the shipped splits outranks it (EV-2: a measurement on the data, on the right
  data).
- **Conceded.**
  - TP-1 (Must) asks for tuned results, and there are none.
  - The newest window depends on the train sample: 1 of 5 ridge samples has t 0.8 (claim audit, concern).
  - The mildest remedy is zillow_prize's condition (precedents D2, option a). If tuned methods do not beat the train
    mean under the shipped metric, window by window, the dataset goes to `TBD -> 2nd Tier`. That is a re-check, not a
    reason to hold the dataset now. TP-2 says "until [a concrete reason] is found, the task stays".

**5. RMSE is a known gap of the benchmark, not of the data (P6; TP-6 Must read with the precedents)**

- **Conceded fact.** The constant 0.5 beats the untuned models under RMSE on the newest window, by 0.00002
  (0.223675 against 0.223692; C40). On the two older windows the models beat the constant.
- **Why this does not block shipping.**
  - TP-6 says that a better version the source defines, including "the scoring it uses", replaces ours. Numerai's
    scoring is the mean per-era correlation. No metric in the metadata expresses that, and a pooled `pearsonr` is not
    it (precedents D3).
  - So no metric is available that would be the source's own scoring. Switching to `pearsonr` swaps one approximation
    for another and changes nothing in the adapter.
- **Mildest remedy.** Keep `rmse` with the existing note, and add numerai to the open cross-cut TP-6 item ("the
  source's metric replaces ours when ..."), with the fact that Numerai's score needs the era grouping. That is option
  (a) of D3.
- **My inference, not measured.** The minimum MSE a calibrated predictor can reach is var(y)(1 - r^2). Tuned models that
  shrink well therefore rank by the same correlation, compressed. Untuned models lose to the constant through their
  variance, which is exactly what tuning fixes.

**6. The Faith features stay with a note: LEAK-38, not LEAK-27 (P4; LEAK-38 Should, LEAK-31 Should, USE-12 Must)**

- **The rule that fits.** LEAK-38: "anonymised fields ... in data a company released for its own competition stay,
  with a `Potential leak, kept on purpose:` note giving the mechanism, the numbers, why they stay and when to revisit."
  Its reason is that removing an unverified signal from host-designed data is arbitrary. Precedents: homesite (AUC
  0.965 to 0.915) and kick (0.757 to 0.691). Both effects are far larger than this one.
- **Evidence: the effect is weak, and smaller than stated.** The claim audit's paired ridge gain on the shipped splits
  is:
  - +0.0043 in eras 1080-1131, against a signal of about 0.015-0.018;
  - +0.0013 in 1132-1183, against about 0.014;
  - +0.0056 in 1184-1191, which is only 8 of the newest window's 52 eras;
  - +0.0010 after the release.

  The `midnight` gain is refuted (-0.0005 +- 0.0011).
- **Not LEAK-27.** No single feature correlates above 0.0076 with the target (column audit). A feature that was a
  model's prediction fit on the targets would carry more than the 0.015 a full model gets. The 1-NN leak probe gives
  R^2 -1.1.
- **What sets it apart from home_credit (LEAK-31's case).** There, the selection was a third-party kernel's, applied on
  top of the source's data. Here, the features are the source's own published data, the live input every participant
  receives (practitioner, section 1).
- **Conceded.**
  - "Every method sees them" is not the rule's reason.
  - Dropping the 75 features is possible.
  - Faith's share of the signal in 1080-1131 is about a quarter, which makes this a weighing call for the curator.
- **Mildest remedy.** Rewrite the note: cite LEAK-38, give the shipped-split numbers, drop the midnight sentence, and
  keep the revisit trigger (test windows after era 1192 once there are enough eras).

**7. The data is faithful and cleaned as documented; licence and width are not verdict reasons (P5, P7; PROV, CLEAN-10, EV-4 Must)**

- **Evidence: provenance holds.**
  - The SHA-256 of all three files match.
  - The row counts are exact: 2,746,268 + 4,135,013 = 6,881,281.
  - There are 0 duplicate feature rows and 0 test rows in their own train side.
  - The bin-2 fill is per feature-era, never per stock: the bin-2 share is at most 20.02% in populated feature-eras.
    Numerai documents the fill (C12, C35, C36, column audit).
- **Licence.** EV-4 (Must) says a licence is "never evidence" and is not even a curator issue. It is a one-line note in
  the record. REVIEW_before ranks it first, which departs from both EV-4 and the "rank order" rule. Precedent:
  lucas_topsoil.
- **Conceded on `medium` (C31 refuted).** `medium` versus `all` is within the sampling noise. Issue 4's size, memory
  and fit-time arguments are barred by CLEAN-22 and EV-4.
  - `medium` is a set the source defines, "each unique in some way". I cannot show that the 1,968 extra features are
    near-copies, so that reason is not yet earned.
  - Remedy, still keeping the dataset: restate the reason without runtime. If the curator finds it insufficient, ship
    `all`, which is a definition fix (P7, lowest rank).
- **Training history.** Numerai's example models train on all eras (split audit, fact 4). Add that as the `History:`
  line, which closes the SPLIT-20 gap raised against g_research.

**Judgment record**

```text
Verdict: ship (as defined), with text fixes.
Validity: SEL-11 holds (no entity series; the naive lag-5 forecast has r about 0); USE-5 holds (the paid target);
  USE-8 approximate (add the metric gap); SPLIT-9/SPLIT-10 hold (4-era gap covers the 3-era overlap);
  LEAK-38 triggered, kept with a note (Faith, +0.001-0.004 outside the 8 design eras of window 1).
Value: TP-2, a small real signal (t 3-9 per era); TP-1 open until tuned results (zillow condition).
Quality: CLEAN-10 holds (fill set to missing); CLEAN-22 reason for `medium` to restate; EV-4 licence noted only.
For the curator: Faith keep vs drop (LEAK-38 vs LEAK-31), RMSE until a per-era metric exists (TP-6 cross-cut item).
```

</details>

<details><summary>Critic</summary>

**Critic: numerai_v5_2_1m (opening brief, 2026-10-20)**

**Position: ship only after changes** (points 1 and 3 change the definition; 2 needs a recorded reading; 4-7 are
notes or wording). Nothing here is a reason to exclude: the task (rank next-20-day returns within a weekly era) is
real and the outer split is honest (split audit: verdict right; 4-era gap clears the 3-era label overlap).

**1. The shipped score measures shrinkage, not stock ranking (P3 USE-5 Must; P6 TP-6 Must)**

- Problem: the actor acts on a ranking within an era and is paid on per-era CORR (practitioner §2; Numerai docs). We
  ship pooled RMSE.
- Effect: on the newest window the constant 0.5 beats ridge and both LightGBMs (0.223675 vs 0.223692 / 0.223693 /
  0.223716, claim audit C40, holds); on the older windows models win by 0.00001-0.00003. The model ranked first is the
  one closest to a constant, while per-era correlation is significant (t 3.3-8.1, C39). The benchmark would rank the
  wrong thing.
- Rule: USE-5 (the resolution the actor acts on: one era's cross-section); TP-6 (a scoring the source itself uses is
  the better version and replaces ours). The adapter limit is no distinguishing fact: amex_non_iid_1m,
  allstate_claims_severity, 5g_energy_consumption and sepsis_prediction_1m set their source's metric under the same
  limit (precedents D3).
- Remedy (fix the definition): set the metric to Numerai's per-era correlation (era as the grouping); if only a pooled
  metric can be declared now, `pearsonr` with the adapter override, and add numerai to the cross-cut TP-6 item. Do not
  ship it scored by RMSE alone.

**2. Scope reading not recorded; the sibling went the other way (P2 SEL-10/SEL-11, TP-10 Must)**

- Problem: the target is an asset's future return over a horizon, the case SEL-10 names ("a price over a horizon").
  g_research_crypto_forecasting, the same kind of target with near-zero signal under RMSE, was recommended `No` +
  `Time-series (Forecasting)` today (precedents D1).
- Evidence for keeping: `id` is unique per row across all 6.9M rows (C3, C33), so there is no entity series to
  forecast, and the features are the source's point-in-time attributes. Evidence missing: TP-10 leg 1 under the shipped
  metric would fail as in g_research (point 1); leg 2 (no feature is a trailing return) cannot be tested.
- Remedy (note): write the reading in the definition and record ("ids change per era, no entity series; TP-10 does not
  apply"), with the untested leg named, and answer the D1 consistency check so both datasets are decided alike.

**3. The 75 Faith features were designed with the test-era targets; removal is possible (P4 LEAK-31 Should)**

- Problem: released at era 1192 (C42 holds); test eras 1080-1191 lie in their design period.
- Effect, measured on the shipped splits (C43): ridge gain +0.0043 +- 0.0006 in 1080-1131, +0.0056 +- 0.0018 in
  1184-1191, against +0.0010 +- 0.0006 after release. Against a newest-window LightGBM signal of 0.0071 (C39) that is
  not "small"; the column audit agrees ("weak in absolute terms, not small relative to the signal").
- Rule: LEAK-31 "keep with a note when small, remove it when we can". It can be removed (705 features left). Its only
  case, home_credit (2026-10-19), removed the selection even at zero effect. "Every method sees them" holds for every
  leak and is not the rule's reason; LEAK-38 is about fields that may be post-outcome, not supervised design.
- Remedy (fix the definition): drop the 75 `faith` features. If kept as an exception, the note must use the measured
  numbers (+0.0056 / +0.0010, not +0.0097 / +0.0019) and drop the Midnight claim, which is refuted (-0.0005 +- 0.0011,
  C44). Open question (column audit #2): `medium` membership was fixed after era 1192; how Numerai chose it is
  unverified.

**4. Inner validation can be 10x optimistic; history reason missing (P4 SPLIT-10, SPLIT-20 Should)**

- Evidence (split audit fact 6): random 80/20 hold-out inside train: LightGBM 0.040 (t 16.8); era-blocked with a 4-era
  gap: 0.004 (t 1.1). A method that tunes or bags on random hold-outs selects on overlapping labels.
- g_research got an issue for its random whole-history train sample (SPLIT-20); here there is no `History:` line.
- Remedy (note): in `splits_comment`, say inner validation must be era-blocked with a 4-era embargo, and add the
  `History:` reason (Numerai's examples train on all eras).

**5. The keep rests on a signal not shown under the shipped metric, and fragile on the newest window (P6 TP-1 Must, TP-2 Should)**

- Evidence: every earlier TP-2 keep showed models beating the dummy under the shipped metric (forest_fires, mortgage;
  precedents D2). Here no tuned results exist (TP-1), and the newest window's signal depends on the train draw:
  LightGBM 0.0006-0.0088 over seeds, one ridge sample in five at t 0.8 (claim audit, "Train sample does not decide the
  result").
- Remedy (note): the zillow condition: if tuned methods do not beat 0.5 window by window under the shipped metric, the
  dataset goes to `TBD -> 2nd Tier`. Point 1 largely resolves this.

**6. `medium` is argued with runtime and memory (P7 CLEAN-22 Must)**

- Evidence: REVIEW issue 4 cites fit time (3.5x), frame size and 200+ GB peak, which CLEAN-22 rules out (coad,
  2026-10-15). The performance argument is also refuted: medium vs all flips with the train seed (C31).
- Remedy (note): restate the reason as the source's own de-duplicated set, if the data shows the extras are
  near-copies; otherwise ship `all`. Quality only; not a reason to hold the dataset.

**7. Text that disagrees with the data (P3 USE-3, USE-8 Must)**

- "known about four weeks later" (task_summary, curation_comments) contradicts the data and the splits_comment: targets
  resolve at T-5, about five weeks (C4/C27 refuted).
- `fit_reason` names only the Faith leak; the metric gap is the largest gap (practitioner) and USE-8 asks for the known
  gap to be named.
- Remedy (repair the text): "about five weeks later"; add the metric gap to `fit_reason` (unless point 1 is fixed).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate rebuttal: numerai_v5_2_1m (2026-10-20)**

We agree on the facts: the outer split is honest, the task is real, and nothing here is a reason to exclude. Most of
the critic's points are the fixes my brief already proposed, so I concede them. I dispute the remedy of point 1 and the
size argument of point 3.

**1. Metric: the problem is conceded, the remedy is disputed**

- **Conceded.** Pooled RMSE ranks shrinkage, not stock selection, and the constant 0.5 wins on the newest window (C40).
  The note and `fit_reason` must say so.
- **Disputed: the critic's fix does not change the score.** With `pearsonr` set, the adapter still falls back to
  `rmse` (REVIEW issue 2; precedents D3). The benchmark would rank models exactly as it does now. The fix only changes
  the declared name.
- **Disputed: `pearsonr` is not the source's scoring.** TP-6 replaces ours with "the scoring [the source] uses". That is
  CORR: a mean of per-era correlations, computed on rank-gaussianised predictions. Pooled `pearsonr` is a third
  approximation, not the source's version. The metadata cannot express a per-era metric today (precedents D3).
- **The fact that sets numerai apart from amex, allstate, 5g and sepsis.** Their metrics are declarable functions of
  pooled rows; Numerai's is not.
- **Disputed: USE-5.** USE-5 governs the target, and the target holds: `target_ender_20` equals `target` on 100% of rows
  (C28).
- **What follows.** Ship with `rmse` and the strengthened note. Add numerai to the TP-6 cross-cut item, flagged as
  needing an era-grouped metric.
- **Concession.** If the curator wants Numerai's intent declared in the definition, I do not object to `pearsonr`, as
  long as the note says it is pooled, not CORR. It costs nothing.

**2. Scope reading: conceded**

Write the reading into the definition and the record, name the untested leg, and answer D1 with option (a).

- **One correction.** Leg 1 is not "would fail". It was never tested under RMSE against the naive forecast. The naive
  per-entity forecast (lag 5) correlates about 0 with the target (split audit, fact 2), so it loses to the 0.5 constant
  and to the models.
- **What decided g_research's `No`.** It was the persistent entity series. That is the fact absent here.

**3. Faith features: partly conceded**

- **Conceded.**
  - LEAK-31 is the literal rule. LEAK-38 is written for possibly post-outcome fields, so my keep needs an exception.
    The fact: these are the source's own published features, the live inputs every participant gets. It serves P3.
  - The numbers must be the measured ones, and the Midnight claim goes.
  - Removal is possible.
- **Disputed: "not small".** The critic sets +0.0043, measured in eras 1080-1131, against 0.0071, the newest window's
  signal. In its own window the signal is 0.0154, so the gain is about 28%. In 1132-1183 it is +0.0013 against 0.0142,
  about 9%.
  - In the newest window only 8 of 52 eras are in the design period. My arithmetic, not a measurement: that shifts the
    window mean by about 0.0056 x 8/52 = 0.0009, about 12%.
  - So the leak is material in one window of three and small in two.
- **What follows.** This is a weighing call for the curator: keep with an exception, or drop the 75 (705 features
  left). I accept either. Neither is a reason to hold the dataset.
- **Disputed: home_credit as a precedent.** There the selection was a third-party kernel's, layered on the source's
  data. That is a different fact.

**4. Inner validation and the history line: conceded**

Same fixes as my brief: the `splits_comment` sentence and the `History:` line.

**5. TP-1 and TP-2: conceded**

The zillow condition applies. The fragility of the newest window (1 of 5 ridge samples at t 0.8) is real. The other two
windows hold across samples (t 3.6-13).

**6. `medium`: conceded**

Restate the reason, or ship `all`. This is quality (P7), not a hold.

**7. Text: conceded**

"About five weeks later", and add the metric gap to `fit_reason`.

**Net position**

**Verdict:** ship after text changes. They are the critic's 2, 4, 5, 6 and 7, and my brief's 1, 3, 4 and 7.

**For the curator:**

- Faith: keep with an exception, or drop the 75.
- The declared metric: `rmse`, or a pooled `pearsonr` declared for intent only. Neither changes the score until the
  benchmark has an era-grouped metric.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate (numerai_v5_2_1m, 2026-10-20)**

No new points. Two disputes remain (the metric and the Faith features). The rest I concede.

**Conceded**

- **A1, split.** Conceded. The 4-era gap covers the 3-era overlap (split audit, fact 2). The inner-validation sentence
  is the remedy we both ask for (my point 4).
- **A2, scope.** Conceded. The advocate measured leg 1 of TP-10: a matched stock's lag-5 target correlates
  0.01 / -0.00 / -0.01, against model CORR of 0.007-0.015 (C39). The ids change every era (C3/C33). That is the fact
  that sets the case apart from g_research (D1 option a). My point 2 becomes a note: record this reading, with leg 2
  (whether some features are trailing returns) named as untestable.
- **A3, use case.** Conceded. Add the metric gap to `fit_reason` (my point 7). "Four weeks" also has to become "about
  five" (C4/C27 refuted); the advocate does not dispute that.
- **A4, signal.** Conceded. TP-2 keep with the zillow condition. One caveat: the condition has to be checked under the
  metric that ships. With RMSE it tests shrinkage, not signal (see A5).
- **A7, provenance, licence, `medium`.** Conceded, including the `History:` line. On `medium`: restate the reason
  without runtime, otherwise ship `all` (CLEAN-22 Must, a P7 fix).

**Disputed**

**A5. RMSE is kept with a note. Disputed (USE-5 Must, TP-6 Must)**

- **Facts we agree on.**
  - Under the shipped metric the constant 0.5 ranks above ridge and both LightGBMs on the newest window (C40).
  - On the other two windows the models win by only 1-3e-5.
  - Per-era correlation separates the models at t 3.3-8.1 (C39).
- **"Switching to `pearsonr` changes nothing in the adapter."**
  - The same holds for amex_non_iid_1m, allstate_claims_severity, 5g_energy_consumption and sepsis_prediction_1m. All
    four declare their source's metric under the same adapter limit (precedents D3).
  - So the adapter limit is no fact that sets numerai apart. The definition should declare the metric that is closest
    to the source's scoring, as those four do.
- **"`pearsonr` is only another approximation."**
  - It is scale-invariant, so it cannot reward shrinking towards 0.5. That is exactly the failure measured in C40.
  - RMSE can reward shrinking, and C40 shows it does. A closer approximation is still the better version (TP-6), at
    the resolution the actor acts on (USE-5).
- **The var(y)(1 - r^2) argument.**
  - The advocate marks it as inference. It holds only for calibrated predictors.
  - The benchmark scores whatever the methods output. The measured gaps between models (about 2e-5) are smaller than
    the gaps that shrinkage alone produces.
- **What would settle it.** Rank the probe models and the constant on the shipped windows three ways: by RMSE, by
  pooled `pearsonr` and by mean per-era CORR. Keep the metric whose ranking agrees with per-era CORR. If pooled
  `pearsonr` agrees and RMSE does not, set `pearsonr`.
- **My fallback, if the curator keeps RMSE.** The zillow condition must then also require that tuned methods beat 0.5
  under RMSE in every window.

**A6. The Faith features are kept under LEAK-38. Disputed (LEAK-31 Should is the rule that applies)**

- **LEAK-38 is the wrong rule.**
  - It covers anonymised fields "that may be post-outcome" (it narrows LEAK-10). Its reason is that removing an
    *unverified* signal is arbitrary.
  - The Faith features are not post-outcome. Their mechanism is supervised design over labelled eras that include the
    test eras, which is LEAK-31's case.
  - The effect is also verified, not suspected. The paired gain is +0.0043 +- 0.0006 in 1080-1131 (C43), and that
    window lies entirely inside the design period, not just 8 eras of it.
- **LEAK-31 says "keep with a note when small, remove it when we can".**
  - The advocate concedes that removal is possible, and that the gain is about a quarter of the signal in 1080-1131.
  - homesite and kick are LEAK-38 cases with suspected post-outcome fields, so they do not set the threshold for this
    rule.
- **The home_credit distinction.**
  - The advocate's distinguishing fact is that the features are the source's own published set, not a third-party
    kernel's. That fact is real. It is option (a) of D4.
  - Under the strengths, it makes keeping an *exception* to LEAK-31 that the curator records. It is not a reading of
    LEAK-38.
  - It is also the third keep of a source-published selection, after qsar_oral_toxicity and qsar_bioconcentration.
    That makes the amendment due (precedents, third-case watch).
- **Conceded.**
  - The Faith features are not LEAK-27 (max single-feature correlation 0.0076; 1-NN R^2 -1.1).
  - The final call is the curator's.
  - Whatever is decided, the note gets the shipped-split numbers and loses the refuted Midnight sentence.
- **What I ask.**
  - Drop the 75 features by default under LEAK-31.
  - Keeping them is an exception, or the LEAK-31 amendment, decided by the curator. LEAK-38 is not the basis.

</details>

<details><summary>Mediator</summary>

**Mediator: numerai_v5_2**

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-11 holds and TP-10 does not apply (id is unique per row, so there is no entity series; the naive lag-5
  forecast has r 0.01 / -0.00 / -0.01; leg 2 cannot be tested on obfuscated features); USE-5 holds (target_ender_20
  == target on 100% of rows); USE-8 approximate (the fit_reason must also name the metric gap); SPLIT-9/SPLIT-10 hold
  (the 4-era gap covers the 3-era label overlap); SPLIT-10 for inner validation: a note (random hold-out 0.040 vs
  era-blocked 0.004); LEAK-31 triggered by the 75 Faith features: drop by default (issue 2); LEAK-27 not triggered
  (max single-feature r 0.0076, 1-NN R^2 -1.1); PROV holds (SHA-256 match, exact row counts, 0 duplicates).
Value: TP-2, a small real signal (per-era r 0.007 / 0.014 / 0.015, t 3.3 / 7.7 / 8.1); TP-1 open until tuned results
  (the zillow condition); TP-6: the metric (issue 1).
Quality: CLEAN-22: the reason given for `medium` is not admissible; restate it or ship `all` (issue 3); CLEAN-10 holds
  (bin-2 fill set to NaN per feature-era).
Weighed: source +, size +, realness +, signal - (tiny, fragile on the newest window), leak - (Faith).
For the curator: issue 1 (metric, tied to the TP-6 amendment), issue 2 (Faith: drop, or an exception/amendment),
  issue 3 (`medium` vs `all`), issue 4 (v5.3 under TP-6).
```

**The decisive experiment (metric)**

Setup:
- The frame and splits the claim audit rebuilt from the definition (2,025,745 rows; 3 windows; 1M train rows each).
- The 780 features, without `era`.
- Thread cap of 4.

Models:
- the constant 0.5 and the train mean;
- ridge with alpha 1e4, 1e6 and 1e8;
- LightGBM with 600 trees, as in the audits;
- the same LightGBM predictions rescaled around 0.5 by x0.3 and by x3 (identical ranking, different scale);
- a loose LightGBM (300 trees, lr 0.1, 127 leaves).

| window | Kendall tau with per-era CORR: RMSE | pooled `pearsonr` | RMSE winner | pooled-r winner | CORR winner |
|---|---|---|---|---|---|
| 1184-1235 | -0.11 | 0.89 | LGBM x0.3 | ridge 1e6 | ridge 1e6 |
| 1132-1183 | 0.11 | 0.89 | LGBM x0.3 | LGBM | LGBM |
| 1080-1131 | 0.39 | 0.93 | LGBM | LGBM | LGBM (the three scales tie) |

What it shows:
- **Pooled r tracks per-era CORR.** Pooled r is within 0.0002 of per-era CORR for every model. The era means of the target are constant (0.49989-0.49997), so pooling adds almost nothing between eras.
- **RMSE ranks scale.**
  - The same LightGBM predictions get RMSE 0.223669 at x0.3, 0.223693 as fitted and 0.224052 at x3 (newest window). The x3 copy loses to the constant in every window.
  - The loose LightGBM has CORR t 3.2-4.7, yet it loses to the constant in all three windows.
  - In the newest window, ridge 1e8 has CORR 0.0030, less than half of LightGBM's, and still beats it under RMSE.
- **Limit.** These models are untuned. Tuned methods may calibrate their scale, but scale invariance is structural: RMSE can reorder models whose rankings are identical, and `pearsonr` cannot.

**Changes to make now (no decision needed)**

1. **"Known about four weeks later" becomes "about five weeks later"**, in `task_summary.predicted` and `curation_comments`. Rule: USE-3 (C4/C27 refuted: targets resolve at T-5).
2. **Name the metric gap in `fit_reason`**, and remove "because every method sees them", which is not a rule's reason. Rule: USE-8.
3. **Rewrite the Faith note in any case:**
   - give the numbers on the shipped splits: +0.0043 ± 0.0006 (1080-1131), +0.0013 ± 0.0007 (1132-1183), +0.0056 ± 0.0018 (1184-1191), +0.0010 ± 0.0006 after release;
   - cite LEAK-31 instead of the "leak_checks precedent";
   - replace the Midnight sentence with its refutation (-0.0005 ± 0.0011).

   Rules: LEAK-31, EV-2.
4. **`splits_comment`:** say that inner validation must be era-blocked with a 4-era gap (random hold-out 0.040, t 16.8, against era-blocked 0.004, t 1.1). Rule: SPLIT-10.
5. **Add a `History:` line:** Numerai's example models train on all eras. Rule: SPLIT-20, consistent with g_research issue 6.
6. **Write the scope reading into the definition and the record:**
   - ids are unique per row, so there is no entity series;
   - the naive lag-5 forecast has r ≈ 0;
   - leg 2 (whether a feature is a trailing return) cannot be tested.

   Rules: SEL-11, TP-10; precedent D1 option (a).
7. **Task-probe note:**
   - use the numbers on the shipped splits (0.0071 / 0.0142 / 0.0154; t 3.3 / 7.7 / 8.1);
   - name the fragility: 1 of 5 ridge train samples gives t 0.8 on the newest window;
   - add the zillow condition: if tuned methods do not beat 0.5 window by window under the metric that actually scores, the dataset goes to `TBD -> 2nd Tier`.

   Rules: TP-1, TP-2.
8. **RMSE note:** replace "the adapter accepts only rmse" with the measured fact (RMSE rewards scale; the tau values above), and add numerai to the TP-6 cross-cut item in the collection's REVIEW.md. Rule: TP-6.
9. **`medium` text:**
   - remove "medium beats all" (C31 refuted: the order flips with the train seed);
   - remove the runtime, memory and frame-size arguments from REVIEW issue 4.

   Rules: CLEAN-22, EV-4.
10. **Record and REVIEW.md:**
    - the 2026-10-07 assessment says "two test windows"; it is three;
    - move the licence out of the issues into a one-line note (EV-4; lucas_topsoil);
    - order the issues by rank;
    - optional: `horizon_unit` / `gap_unit` = "steps" (an info-level check message).

**Issues for the curator (ranked)**

**1. The metric: P6, TP-6 (Must) against definitions.md "Field mapping"**

- **Problem.** Numerai scores per-era CORR. The definition ships pooled RMSE, which ranks the scale of the predictions, not stock selection.
- **Effect.**
  - The constant 0.5 beats every unscaled model on the newest window.
  - RMSE's ranking agrees with CORR at tau -0.11 to 0.39; pooled `pearsonr` agrees at 0.89 to 0.93.
- **Critic's best evidence.** The four siblings (amex_non_iid_1m, allstate_claims_severity, 5g_energy_consumption, sepsis_prediction_1m) declare their source's metric under the same adapter limit. `pearsonr` cannot reward shrinkage.
- **Advocate's best evidence.** Numerai's metric is a per-era mean that pooled rows cannot express. The adapter falls back to `rmse` either way.
- **Settled by measurement.** On this data pooled r reproduces per-era CORR within 0.0002 per model. That removes the advocate's distinguishing fact, so declaring RMSE has nothing that sets numerai apart from the four siblings.
- **What stays open.** TP-6 (Must) and definitions.md ("a competition keeps our default") conflict. The amendment is pending in the collection's REVIEW.md, and the AI does not settle that conflict. Under the proposed amendment wording, `pearsonr` qualifies.
- **Decision needed:**
  - (a) set `metric = "pearsonr"`, with a note that it is pooled, matches CORR's ranking here, and that the adapter still falls back to rmse (recommended);
  - (b) keep `rmse` with the note, as a recorded departure from the four siblings.

  Either way: as long as the adapter scores RMSE, this dataset measures the scale of the predictions. Decide whether it may enter a scored TabArena run before the adapter honours `pearsonr`. That is a benchmark-side change; until then the zillow condition is checked under RMSE.

**2. The 75 Faith features: P4, LEAK-31 (Should)**

- **Problem.** Numerai designed these features with targets of eras 1080-1191, which lie inside the test windows. They were released at era 1192.
- **Effect (measured).** Ridge gain is about 28% of the signal in 1080-1131 and about 9% in 1132-1183. In the newest window it is about 12%, by arithmetic: only 8 of its 52 eras fall in the design period.
- **Rule.** LEAK-31 governs: the mechanism is supervised design on labelled eras that include test eras.
  - LEAK-38 narrows LEAK-10 (post-outcome fields). These values are not post-outcome, and the effect is measured, not "unverified". The advocate conceded this.
  - LEAK-31 says "remove it when we can"; removal leaves 705 features. home_credit removed its selection even at zero effect.
- **Critic.** Drop by default.
- **Advocate.** Keep, as an exception. The fact that sets the case apart: these are the source's own published live inputs, not a third-party selection (which is a real difference from home_credit).
- **Weakness of the exception.** It claims to serve P3, but in eras 1080-1191 no participant had these features, so keeping them does not mirror the use case in those eras.
- **Third-case watch.** A keep would be the third source-published selection kept under LEAK-31 (after qsar_oral_toxicity and qsar_bioconcentration). The amendment is then due, not a third exception.
- **Decision needed:**
  - (a) drop the 75 (recommended; the default);
  - (b) keep them as an exception;
  - (c) amend LEAK-31 for source-published selections.

  If `all` is chosen in issue 3, the same call covers its 372 Faith features.

**3. `medium` versus `all`: P7, CLEAN-22 (Must)**

- **Problem.** 1,968 features are left out. The only reasons given are runtime and memory, which CLEAN-22 rules out (coad, 2026-10-15). The performance argument is refuted.
- **Admissible reason, if earned.** `medium` is the source's own "each unique" set, so the dropped features could leave as near-copies. Nobody has shown that they are near-copies.
- **Counter-point (column audit).** `medium` membership was fixed after era 1192, so it could itself be a selection made with labels. This is unverified.
- **Decision needed:**
  - (a) restate the reason once the near-copy measurement supports it;
  - (b) ship `all`.

  Quality only; it does not hold the dataset.

**4. Version and target: P6, TP-6 (Must; not disputed, still unanswered)**

- **Question.** v5.3 is current and pays on `target_ender_60` (12-era embargo; r 0.47 with the 20-day target). TP-6 asks whether this is a better version the source defines.
- **Status.** REVIEW_before presents it as optional and does not answer TP-6. The v5.2 task is valid either way.
- **Decision needed:** keep v5.2, or open v5.3 as a new record.

**Agreed facts**

- **Split.** Temporal on `era`: test 1184-1235 / 1132-1183 / 1080-1131, train ends 1179 / 1127 / 1075.
  - Targets overlap for 3 eras (r 0.60 / 0.36-0.42 / 0.14-0.21 at lags 1-3; about 0 at lag 4). The 4-era gap clears that overlap.
  - An IID split would give per-era r 0.261 against -0.0007 for the temporal split.
- **Rows.** id is unique across all 6.88M rows, so there is no stock key. The naive lag-5 forecast has r about 0.
- **Target.** target_ender_20 equals `target` on 100% of rows. It has 5 levels, and every era's mean is 0.5.
- **Signal.** Per-era r 0.0071 / 0.0142 / 0.0154 (t 3.3 / 7.7 / 8.1). On the newest window it depends on the train sample (1 of 5 ridge samples gives t 0.8). R² is at most 0.00025.
- **RMSE.** The constant 0.5 beats ridge and both LightGBMs on the newest window (0.223675 against 0.223692 or more).
- **Faith.** Release at era 1192 holds. The ridge gains are as above. The Midnight gain is refuted.
- **Provenance and cleaning.** SHA-256 of all three files match. 6,881,281 rows. 0 duplicate rows. The bin-2 fill is per feature-era only.
- **Feature sets.** `medium` vs `all` cannot be told apart from the noise.
- **No tuned results yet.** The fit is approximate.

**Consistency with precedent**

- **D1, scope.** Follows option (a). The fact that sets numerai apart from g_research: no entity series (id per row) and a measured naive forecast with r ≈ 0.
- **D2, TP-2 keep.** Follows zillow's condition. It departs from forest_fires and mortgage, which showed signal under the shipped metric. The fact that sets it apart: the signal is measured under the source's own scoring, and pooled r reproduces that scoring. Under option (a) of issue 1, the shipped metric would show it too.
- **D3, metric.** Option (a) of issue 1 follows amex, allstate, 5g and sepsis. Keeping RMSE would depart from them with no distinguishing fact left after the experiment, so it needs the curator's recorded reason.
- **D4, Faith.** Dropping follows home_credit. Keeping departs from it: it needs an exception with its fact, and it triggers the third-case amendment.
- **D5, `medium`.** The coad precedent rules out runtime as a reason, so the text has to change either way.
- **D9, History line.** Matches g_research issue 6.
- **D6, licence.** EV-4 / lucas_topsoil: a note only.
- **D7, numerai28_6.** Consistent: the duplicate status stands, and it is shipped in no Data Foundry collection.

</details>
