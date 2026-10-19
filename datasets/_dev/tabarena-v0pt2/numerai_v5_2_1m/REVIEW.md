# numerai_v5_2

**Outcome:** added as `numerai_v5_2_1m`. Numerai's v5.2 tournament data (eras 1-1235, the 780 `medium` features),
target the stock's 20-day return rank (regression, RMSE), temporal with three 52-era test windows after a 4-era gap,
sampled to the 1M budget. Ship with concerns: the licence (issue 1) and a very small signal that RMSE barely measures
(issue 2).

**Main points:** RMSE mostly ranks how far a model shrinks towards 0.5. The Faith features are kept as a potential leak.
Numerai's terms are noted.

**Record judgment:** valid with concerns. The source is Numerai itself; ranking each stock's next 20-day return at a
weekly date is a fixed predictive task with a temporal split, not series forecasting. Concerns: the licence (issue 1),
the small signal under RMSE (issue 2), the Faith features designed over the test windows (issue 3), and a source that
serves only its current weekly snapshot (issue 8).

**Issues for Lennart:**

1. **Licence (noted, not a verdict reason).** Numerai's Terms of Service, section 4.2 (updated 2026-08-31), license the
   data "solely for the purpose of participating in Tournaments". They forbid "(i) use the Data for any commercial
   purpose outside of the Services" and making it "available to any third party", and they require keeping the data "in
   confidence". Both a shipped container and a company running the benchmark would fall under this. Implemented: the
   terms are in `license`. Alternatives: ship only the definition and let users download with `numerapi`, or ask Numerai
   for permission.

2. **Metric and task worth.** On RMSE:
   - The best model I fit reaches R^2 of 0.0003 at most, while its per-era correlation is significant in every window
     (t = 3.0-8.7). Numerai on per-era scores: "+/- 0.05 is normal in quantitative finance".
   - Under RMSE the constant 0.5 beats both fitted models on the newest window, so RMSE mostly ranks shrinkage towards
     0.5.
   - Numerai scores per-era correlation (CORR). `pearsonr` is a canonical regression name in
     `bundle_checks.KNOWN_METRICS`, but TabArena's adapter allows only `rmse` for regression (`DEFAULT_EVAL_METRICS` in
     `tabarena/benchmark/task/data_foundry/adapter.py`) and falls back to it with only a DEBUG log.
   - Implemented: RMSE, with the Note bullet. Alternatives: `metric = "pearsonr"` plus an adapter override, or drop the
     dataset if the benchmark scores regression only by RMSE.

3. **Faith features.** Numerai designed the 75 Faith features of `medium` before releasing them with v5.1/v5.2:
   October/December 2025, marked at era 1192 in the v5.3 notebook. So eras 1080-1191 of the test windows lie in their
   design period.
   - Paired ridge gain in per-era correlation: +0.0041 +- 0.0007 in 1080-1131, +0.0016 +- 0.0007 in 1132-1183,
     +0.0097 +- 0.0021 in 1184-1191, and +0.0019 +- 0.0008 after the release.
   - LightGBM gain for the same periods: +0.0027, -0.0006, +0.0109, +0.0008.
   - The 122 `midnight` features show a smaller effect that is not significant (+0.0017 +- 0.0012 before their
     release, +0.0004 +- 0.0006 after).
   - Implemented: keep them, with a note (the leak_checks precedent for feature selection on the labelled set).
     Alternative: drop the 75 Faith features (705 left, LightGBM correlation 0.0041 instead of 0.0064 on the newest
     window), or move the test windows after era 1200 once there are enough eras.

4. **Feature set.** Implemented: Numerai's `medium` set (780 features, "each unique in some way").
   - LightGBM per-era correlation on the newest window: `medium` 0.0064 (34/52 eras positive), `all` (2,748 features)
     0.0055 (31/52), `small` (42 features) 0.0011 (30/52). `all` also takes 3.5 times the fit time (789 s against 223
     s).
   - With `all`, the frame would be 14.8 GB instead of 3.4 GB: 1,510 of its features have missing eras and would become
     float32 (5.6 GB without that conversion). The pipeline peak would grow from 53 GB to an estimated 200+ GB.
   - 105 of the `all` features, all from the `faith` set, are empty in every era before 575.
   - `small` holds the features "that have the highest feature importance" on data Numerai does not name, possibly
     including our test eras.

5. **Window length.** Implemented: 3 windows of 52 eras with the 4-era gap. A model's per-era correlation has a standard
   deviation of about 0.015. So a window's mean has a standard error of 0.0021 with 52 eras, 0.0029 with 26 and 0.0042
   with 13, against signals of 0.006-0.018.

6. **Target.** Implemented: `target_ender_20`, v5.2's main target (20-day horizon). Alternative: `target_ender_60`, the
   payout target since v5.3. It needs a 12-era embargo, is unresolved for eras 1228-1240, and correlates 0.47 with the
   20-day target.

7. **Version.** The record names v5.2. v5.3 ("Quantum", July 2026, 807 new features, 3.3 + 5.7 GB) is now current, and
   Numerai still updates the v5.2 files weekly. Implemented: v5.2 as recorded. Moving to v5.3 needs a record rename and
   a new folder.

8. **Reproducibility.** The API serves only this week's files: older rounds return the same object. The definition pins
   the rows with `LAST_ERA = 1235`, and `download_description` gives the SHA-256 of our files. A later download
   reproduces the data only if Numerai never revises past eras. Keep the raw files (7.0 GB) in the rebuild skill's
   backup zip.

9. **Missing values.** Implemented: feature-eras filled with bin 2 become NaN (Numerai: "If data for a particular
   feature is missing for that era ..., then all values will be set to 2"). Inside populated feature-eras every bin
   holds 20.0% of the stocks (bin 2 at most 20.02%), so no single stock was filled. Alternative: keep Numerai's 2s,
   which keeps all features int8 (frame 1.6 GB instead of 3.4 GB).

11. **Framework notes (not patched):**
   - Above 50M cells the bundle checks skip the duplicate-row and duplicate-column checks, so every `_1m` dataset needs
     them by hand.
