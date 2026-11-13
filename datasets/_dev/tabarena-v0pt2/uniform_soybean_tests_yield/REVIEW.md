# uniform_soybean_tests_yield

**Outcome:** added. The AI recommends shipping it: the review panel's changes are made, and one call is left for the
curator, the metric. Seed yield in bu/acre of 92,814 entries of the USDA Uniform Soybean Tests 2003-2015 (a line at
one trial location in one season) from the maturity group of the test, the anonymized line id, its pedigree cluster,
the location and the location's daily weather from April to October, as released by the MLCAS2021 challenge of Shook
et al. (2021); whole seasons held out (7 yearly windows 2009-2015, each trained on every earlier season) in place of
the challenge's random split, under which every test location-year and line was in training; RMSE, the challenge's
metric. The files come from a participant's copy, since the publisher's links are dead for everyone; the copy matches the authors' own files on GitHub (pedigree clusters byte-equal, the 103,365 genotype ids the
same, 1,870 of the 2,000 rows of their subset found with identical weather), now written in the download notes. The
panel's other changes: the use case reworded to the paper's aim (a breeder predicting a new season's entries; the old
text put the prediction after the season, which argued for the rejected random split), the 2009 window added, 13,797
impossible values of the 30 October average temperature set to missing, a protocol line that forbids reading rows
outside a window (a line's later entries give away that it yielded well), a sentence in the notes and the fit text
that on held-out seasons RMSE mostly scores each new location-year's level, and the notes' numbers and wording
corrected.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2 hold; USE-1 triggered (the written post-season use case argued for the rejected random split),
fixed by rewording to the paper's aim with the breeder as actor; USE-8 fit approximate, fit_reason names the gaps in
order; LEAK-10 holds (the season's weather a given condition); LEAK-30 weak, kept with its note; LEAK-9 triggered (a
line's later-season rows read from outside the window), protocol line; SPLIT-1, SPLIT-3, SPLIT-5 hold (held-out
seasons); SPLIT-14 holds; SPLIT-15 triggered, fixed (2009 window, 50.7% of the rows in training); PROV-8 holds with the
match written down; PROV-13 kept with notes (the authors' fill of one weather day and the double-converted rows cannot be
repaired from the origin).
Value: TP-1, TP-2 hold: a small real signal (location mean + trend 13.17, + line history 13.04, against the training
mean's 16.68, 6 windows; 13.31 and 13.13 over the 7 shipped); MET-1, MET-2 against RMSE measured (Kendall tau 0.38 with the within-environment score),
the switch is the curator's (issue 1, switch recommended).
Quality: CLEAN-11 fixed (AvgSur_d213 outside its day's minimum and maximum set to missing); CLEAN-14 maturity group
kept numeric with its reason.
Weighed: source + (paper and challenge, copy matched to the authors' files), size + (92,814 rows), signal - (small but
real), window noise - (74-88 location-years per test season); priority factors gap 0, use case 0, shape +, risk 0.
For the curator: issue 1 (the metric, switch recommended), decided together with genomic_prediction_soy_yield; a switch
adds a metric rule.

**Main points:** One call: keep the challenge's RMSE or score how well a model ranks lines within each location-year
and maturity group (issue 1; the switch is recommended and adds a metric rule; decided together with genomic_prediction_soy_yield, where the
pooled score is recommended under the same rule).

**Record judgment:** valid. The data of Shook et al. (2021, PLOS ONE), the USDA Uniform Soybean Tests' reports of
2003-2015 converted by the authors, as the MLCAS2021 challenge released them; the publisher's download links are dead,
and the copy used matches the authors' own GitHub files. The priority stays 3 (gap 0, use case 0, source +, shape +,
risk 0): the use case is written from the paper's aim, not named by the source, and the fit is approximate.

**Issues for Lennart:**

1. **Keep the challenge's RMSE, or score how well a model ranks the lines within each location-year and maturity group?**

   * **Problem:**
     - Three quarters of the yield variance lies between location-years (one trial location in one season), so on held-out seasons RMSE orders models mostly by how well they guess a new location-year's level, which the features predict only through the location's past mean and the yield trend, and hardly by how they rank the lines within it, which is what the breeder of the use case acts on.
     - Over 13 untuned models on the six windows 2010-2015, the order under RMSE agrees with the order under the mean correlation within location-years at Kendall tau 0.38 (0.09 among the 9 competitive models; 0.37 with the 2009 window, added after the measurement).
     - Decide it together with genomic_prediction_soy_yield (same actor, same question, open in this batch, pooled score kept there by default): a switch in either is the third dataset scored within groups because a pooled score rewards the groups' levels (after protein_model_quality_rf_pcp and huesken_sirna_efficacy), so it changes the metric rules, and here it also overrules a research-run competition's metric, which the rules leave to you case by case.
   * **Background:**
     - The within-group score is `mean_group_pearsonr`: the Pearson correlation of prediction and truth inside each group, averaged over the groups; plant breeders report it as "predictive ability" for new environments (Jarquin et al.'s schemes for tested and for untested lines in untested environments, CV0 and CV00).
     - The release has no test id: a location-year pools 2 to 4 maturity-group tests, so location-year x maturity group is the closest proxy for one test (138 to 158 groups per test season, median 36 to 43 records, none below 5); location-year alone gives 74 to 88 groups per season.
     - The challenge (MLCAS2021, run by the paper's authors) scored RMSE on a random split where every test location-year was in training, so its RMSE scored mostly the deviations within an environment; our held-out seasons make the environment's level the larger part of the error.
   * **Effect on the task:**
     - Knowing each test location-year's mean takes RMSE from about 14 to 7.3-8.2 bu/acre; adding everything known about the line improves it by only 0.0 to 0.3 more.
     - Under RMSE a location mean plus the yield trend, which ranks no lines (correlation 0 within a location-year), is 3rd of 15 models and baselines (12.99, mean of 6 windows), ahead of every LightGBM (13.13 to 14.60, within-location-year r 0.21 to 0.22); a ridge on one-hot ids with the weather ranks lines as well as any model (r 0.214) and is last but one under RMSE (20.18), because its weather term extrapolates the level badly.
     - Under the within-group score the models separate into tiers (LightGBM, ridge and the line's history 0.20 to 0.23; histogram boosting 0.17; random forest and extra trees 0.09 to 0.11; kNN 0.02), the top tier within 0.03.
   * **Experiments:**
     - The mediator trained 13 untuned models (six LightGBM variants with daily, weekly or no weather, histogram boosting, random forest, extra trees, ridge on one-hot ids with and without weather, kNN 50, location mean + trend + shrunk line history) and two baselines once per window, one seed, on the definition before the panel's changes (the 6 windows 2010-2015 then shipped, plus 2009 built the same way; weekly weather means for most models).
     - Kendall tau between the order under RMSE and under the within-location-year r, per test season 2009 to 2015: 0.33, 0.56, 0.18, 0.21, 0.36, 0.38, 0.56 (mean 0.38 over the 6 windows 2010-2015, 0.37 with 2009); grouped by location-year x maturity group 0.35; the two groupings agree with each other at 0.76.
     - RMSE splits into a location-year-level part (each location-year's mean error) and a within part (the rest); its order follows the level part at tau 0.97 and the within part at 0.33; on 3 random folds of the records, as the challenge split, it followed the within part at 0.95 to 0.97 but the within-location-year correlation only at 0.44 to 0.51 (0.13 to 0.18 by location-year x maturity group), so the challenge's RMSE scored the error within an environment, not the ranking B scores.
     - The task gamer's exploit (a line's presence in later seasons, read from outside the window) is within noise under RMSE (-0.07 to +0.01) and worth +0.02 to +0.05 within-location-year r, more than the top tier's spread; the protocol line now forbids it under either metric.
   * **Consistency:**
     - protein_model_quality_rf_pcp and huesken_sirna_efficacy moved to the within-group correlation when a pooled score rewarded the groups' means[^met5]; there it replaced a fallback, here it would overrule a competition's metric.
     - loan_default_prediction_imperial_college overruled a research-run competition's metric on measurements[^met4]; zillow_prize and rossmann_store_sales kept sponsored competitions' metrics, not measured against a changed split.
     - genomic_prediction_soy_yield (same actor, open) keeps Azodi's pooled r by default because there the pooled score orders models like the within-family score (tau 0.91 on the panel's measurement, 0.96 on the means over the splits after its changes, 0.78 per split on average, lowest 0.64); here it is 0.38, and that number is the fact that sets the two apart, so B here and A there is consistent.
   * **Rule change with B or C:** the metric rules gain one sentence: when the use case ranks units within groups and the pooled score orders models unlike the within-group score on the shipped splits, score within the groups from context, also in place of a research-run competition's metric (protein_model_quality_rf_pcp, huesken_sirna_efficacy, this dataset)[^amend]; under it genomic_prediction_soy_yield keeps its pooled r (tau 0.78 per split on average, lowest 0.64; 0.96 on the means). The wording is decided once, as an across-datasets item, together with genomic_prediction_soy_yield.
   * **Panel:**
     - Keep RMSE (the advocate, who argued before the measurement and asked for it): the challenge's verbatim metric; RMSE scores the same quantity, bu/acre per record, under both splits; predicting a new environment's level is the paper's stated aim; a location-year pools tests, so a within-location-year score partly ranks tests.
     - Switch (the critic, the domain practitioner, the mediator): the breeder acts on the ranking within a test against its checks, and the measurement says RMSE barely scores it; grouping by location-year x maturity group answers the pooling objection ("I would pick models by the mean within-environment correlation", the practitioner)[^met1].
     - The practitioner also proposed RMSE of the deviations from each location-year's mean; the mediator did not take it up.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | RMSE (implemented) | the challenge's metric in bu/acre; the notes and fit_reason say that on held-out seasons it mostly scores each new location-year's level | the source's metric, verbatim; a proper score for the yield number; no scoring column | orders models by the new location-year's level, which no feature predicts beyond the location's mean and the trend (tau 0.38 with the within-group score); a baseline that ranks no lines comes 3rd of 15 (4th over the 7 shipped windows) |
     | B | Within location-year x maturity group | the mean correlation within each location-year and maturity group (`mean_group_pearsonr`), on a column of location, year and maturity group that the score reads and models never see; the challenge's RMSE named as the original it replaces | scores the ranking the breeder acts on; the closest proxy for one test; follows protein and huesken | overrules a competition's metric; the third case of the reason, so an amendment comes with it; the absolute level leaves the score |
     | C | Within location-year | the same score grouped by location-year only | the breeders' usual environment; larger groups (74 to 88 per season) | a location-year pools 2 to 4 tests, so part of the score ranks tests, not lines |

   * **Recommendation:** B: on our split RMSE does not score the ranking the breeder acts on (tau 0.38, 0.09 among the competitive models), and grouping by maturity group too answers the objection that a location-year pools tests; B or C adds one rule (below), under which genomic_prediction_soy_yield keeps its pooled r; A if you weigh the challenge's verbatim metric higher. **Decision:** A, B or C (B and C bring the rule change)?

   **Notes for the AI:** on B, add a scoring column in `_clean` (for example `location_year_mg` = location, year and maturity group joined), declare `metric = Metric.from_context("mean_group_pearsonr", reason=..., inputs={"group": "location_year_mg"})` with the reason naming the challenge's RMSE as the overruled original (MET-11 context, amended 2026-11-03), the breeder's within-test ranking, tau 0.38 on the 6 windows 2010-2015 (0.37 on the 7 shipped; 0.09 among the 9 competitive models) and the location-mean-plus-trend baseline ranked 3rd of 15 under RMSE on those 6 windows (4th on the 7 shipped); check that `feature_columns` drops the scoring column; rewrite the Metric bullet of the notes and drop the first gap of `fit_reason` (it then reads "scored within location-year x maturity group"); add the metrics.md Cases row; the amendment of MET-5 / MET-11 takes the wording of the across-datasets item under "### Rules" in the working copy's REVIEW.md (the main session adds it; decided once with genomic_prediction_soy_yield), not a draft of this file; decide genomic_prediction_soy_yield's issue 1 in the same pass and write in each record the tau that sets them apart; re-run `dataset check` and the task probes. On C, the same with location and year only. On A, a CC line in the record naming the reason (the challenge's verbatim metric, kept with the note of what it scores on held-out seasons). Measurements: `m1_metric_order.py`, `m1_summary.log` and `m2_exploit_under_r.py` in the run's work files.

   [^met1]: **MET-1** (Must): the declared metric scores the decision of the use case at the unit the actor acts on. **MET-2** (Must), third bullet: a task we changed keeps the source's metric only when its meaning survives the change. **USE-5** (Must): predict what the actor would act on.
   [^met4]: **MET-4** (Should), amended 2026-11-05 (Lennart, loan_default_prediction_imperial_college): a competition of lesser standing (old, community- or research-run) may give way to the metric the task makes obvious when the measurements favour it, case by case. MLCAS2021 was a workshop challenge run by the paper's authors.
   [^met5]: **MET-5** (Should): exceptions protein_model_quality_rf_pcp and huesken_sirna_efficacy (Lennart, 2026-11-04): context `mean_group_pearsonr`, "the use case ranks guides within a gene and pooled RMSE rewards a gene's mean", in place of the fallback. **MET-11** (Must) `context`, amended 2026-11-03: also covers a source metric overruled under MET-2 or MET-4, the reason naming the overruled original.
   [^amend]: principles.md, "Exceptions and amendments": when the same reason has produced three exceptions, the next pass proposes an amendment. The proposed wording (an amendment of **MET-5** / **MET-11**): "when the use case ranks units within groups and the pooled score orders models unlike the within-group score on the shipped splits, score within the groups from context"; it is decided once, as the across-datasets item under Rules, together with genomic_prediction_soy_yield, issue 1 (open): pooled r against the within-family r, tau 0.91 on the panel's measurement, 0.96 on the means over the splits after its changes, 0.78 per split on average (lowest 0.64).

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator.
Claim audit: 41 claims, none that carries the dataset refuted; the copy matched to the authors' own GitHub files; one
number refuted and fixed ("worse on 4 of 6" is 5 of 6), the weather claim scoped to "beyond each location's mean and
the yield trend"; the post-season use case found at odds with the split (reworded). Column audit: no leak; the authors'
fill of AvgSur_d213 impossible in 14.9% of the rows (set to missing); the maturity group is the test's (wording).
Split audit: held-out seasons right with notes; the source's random split (7.13 against 14.31) and a split grouped by
location-year (12.35-12.52) both overrate a new season; the 2009 window added. Blind review: include with changes; its
main concerns were the small signal under the honest split, the width of the daily weather and the unexplained 214
rows (the exact copies dropped). Task gamer: hard to game; a line's presence in later seasons, read from outside the
window, gains about 1% RMSE (a protocol line now). Debate: agreed on the split, the provenance, the use-case reword and
every fix; disputed: the metric (issue 1). The numbers in the reports below were measured on the definition
before these changes: the 6 windows 2010-2015, AvgSur_d213 as released. The mediator's metric measurement (tau 0.38) is
the mean over those 6 windows, with 2009 run as an extra window (0.37 over 7), and was not re-run on the shipped
definition; the notes re-measured the floor and the task probes on the 7 windows and quote the mediator's metric
numbers.

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: uniform_soybean_tests_yield (panel of 2026-11-08, written 2026-11-09)

Read: principles.md; MET-1/2/4/11, LEAK-9/10/30, USE-1/5/8/9, SPLIT-14/15; dataset.py, the record,
builder_report.md, claims.md; the reports of the claim, column and split auditors, domain practitioner, blind
reviewer, task gamer and precedent checker; the advocate's and the critic's briefs with their rebuttals; the sibling
genomic_prediction_soy_yield's mediator report and REVIEW.md.
New measurements: the run's work files (m1_metric_order.py -> m1_<year>.csv, m1_<year>_preds.npz, m1_summary.log;
m1_metric_order_rand.py -> r1_rand<k>.csv, r1_summary.log; m2_exploit_under_r.py -> m2.log). Thread caps 4; the split
auditor's frame (meta + weekly weather means) and the kit's data.parquet (daily weather); windows rebuilt as
train year < Y, test year == Y, identical to the shipped 6 (checked against the participant kit's splits), plus 2009.

========================================================================================================================
1. JUDGMENT RECORD
========================================================================================================================
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold. USE-1 triggered (the written post-season use case argues for the rejected random split),
  fixed by rewording to the paper's aim with the breeder named as actor (C1); USE-8 fit approximate, fit_reason to
  name the gaps in order (C1). LEAK-10 holds; LEAK-30 weak, kept with its note; LEAK-9 triggered (evaluation-level:
  a genotype's later-season rows read from outside the window), protocol line (C7). SPLIT-1, SPLIT-3, SPLIT-5 hold
  (held-out seasons); SPLIT-14 holds; SPLIT-15 triggered, fixed (2009 window, C4). PROV-8 holds once the match with
  the authors' files is written (C2); PROV-13 kept with notes.
Value: TP-1, TP-2: a small real signal (floor 13.17 / 13.04 against the dummy's 16.68), keep. MET-1/MET-2 against
  RMSE: measured (tau 0.38, section 4); the switch is the curator's (issue 1, switch recommended).
Quality: CLEAN-11 AvgSur_d213 impossible cells to missing (C5); CLEAN-14 maturity group numeric with its reason, and
  wording (C6).
Weighed: source + (PLOS ONE paper and challenge, copy matched to the authors' files), size + (92,814 rows, 74-88
  environments per window), signal - (small but honest), window noise - (about 80 environments per test season).
For the curator: issue 1, the metric (RMSE or mean_group_pearsonr within location-year x maturity group), decided
  with genomic_prediction_soy_yield under one rule but on each one's measured fact.

========================================================================================================================
2. AGREED FACTS (neither side disputes them after the rebuttals)
========================================================================================================================
F1 Data: 92,814 records (93,028 released with yields, 214 exact copies dropped, all within one year), 1,504 features:
   maturity group, genotype (5,838 ids), state (28), location (159 ids, the paper says 150), year, pedigree cluster
   (20), 7 weather variables x 214 days, one series per location-year (1,040 series for 1,117 location-years).
F2 Provenance: publisher links dead for everyone (Drive zip 404, paper folder empty). The CyVerse copy (sha256
   pinned) equals the authors' GitHub files: clusterID_genotype.npy byte-equal to data_subset/k_means_clusters_20.npy;
   the 103,365 genotype ids and (genotype, state) pairs the same multisets; 1,870 of the 2,000 subset rows match a
   training record with identical 214-day weather, the other 130 sit in the test inputs.
F3 Split: the source split records at random (every test location-year and line in training). Held-out seasons are
   the regime of the paper's aim ("unseen and new environments"): random records 7.13 vs 14.31 for the same LightGBM,
   the weather then an environment code (6.68 with weather vs 6.71 with a location-year id); grouped by location-year
   12.35-12.52 (later seasons and the same season's environments in training). 6 windows 2010-2015, train 58.6-93.1%;
   the 2009 window would train on 50.7% of rows.
F4 Leaks: none in the data. Environment never crosses a window (0.0%); pedigree clusters (authors', parentage only)
   worth 13.079 vs 13.115 on new lines (LEAK-30 weak). Task gamer: hard to game; one exploit (section 5).
F5 Signal: dummy 16.68; location mean 13.71; + linear trend 13.17; + shrunk line history 13.04; LightGBM without
   weather 13.60. 75.3% of the variance lies between location-years; oracle environment mean 7.3-8.2; oracle level +
   line effect improves on it by only 0.0-0.3. Weather adds nothing beyond each location's mean and the yield trend,
   but helps a direct LightGBM (14.55 -> 14.19).
F6 Notes misstate: "worse on 4 of 6" is 5 of 6; "the line's maturity group" is the test's (215 lines in two groups,
   11.7% of rows); AvgSur_d213 lies outside [MinSur_d213, MaxSur_d213] in 13,843 rows (14.9%, 178 location-years).
F7 The written use case (post-season) contradicts the split; three agents found it independently; both sides accept
   rewording to the paper's aim with split, features and fit unchanged.

========================================================================================================================
3. CHANGES TO MAKE NOW (no decision needed)
========================================================================================================================
C1 Use case (USE-1 Must, USE-3, USE-8 Must). Actor settled (section 4, D1): a soybean breeder or the UST coordinator.
   use_case, e.g.: "A soybean breeder or the Uniform Soybean Tests coordinator predicts each entry's yield at the
   locations of a season not yet in the data, from the line, the site and that season's weather taken as a given
   condition, to choose which lines to advance and where to test them; the model is fit on the earlier seasons'
   trials." Rewrite the prediction-point bullet the same way (weather a given condition or scenario, not a
   planting-time forecast). fit "approximate"; fit_reason names, in order: the breeder acts on a line's yield relative
   to the other entries and checks of its test while the target is the absolute yield (drop this gap if issue 1
   switches the metric, then it reads "scored within location-year x maturity group"); the season's weather stands
   in for what is known only at harvest; no test id or check flag (a location-year pools 2-4 maturity-group tests);
   no soil, planting date or management. The paper's other named users (insurers, marketing) go in no actor role.
C2 Provenance (PROV-8 Must, EV-2): download_description and the Source bullet state F2 with the GitHub path
   (github.com/tryambakganguly/Yield-Prediction-Temporal-Attention, data_subset/); the State and location bullet adds
   "159 location ids, where the paper and the challenge count 150". Asking the authors for a stable deposit stays
   optional (reproducibility, not provenance).
C3 Measured claims (EV-2): "5 of 6"; scope the weather sentence to "beyond each location's mean and the yield trend,
   the weather adds nothing measurable for the models tried" with the direct-LightGBM gain (14.55 -> 14.19); give the
   floor (location mean + trend 13.17; + line history 13.04). Fix the record's Assessment line of 2026-11-09 through
   the store. splits_comment: add the grouped-by-location-year number (12.35-12.52) and why it was not chosen.
C4 Windows (SPLIT-15 Should; SPLIT-14 Must met): add the 2009 window (train 47,067 of 92,814 rows = 50.7%) with
   explicit cutoffs 2015..2009, since unit="unique" counts seasons, not rows; reword splits_comment by rows. No fact
   was offered for stopping at 6, and both sides lean to adding it. The 2009 window behaves like the others in m1
   (tau 0.33; model order unchanged in the 7-window means).
C5 AvgSur_d213 (CLEAN-11 Should, cheap and safe): set to missing where it lies outside [MinSur_d213, MaxSur_d213]
   (13,843 rows, 178 location-years); give the counts in the Anomaly bullet.
C6 Wording (CLEAN-14, writing.md): "the maturity group of the test" in task_summary.question/known and the Maturity
   group bullet (with the 215 lines / 11.7%); keep it numeric with the reason (equal steps of relative maturity, a
   value between groups means something); "the line's entry mean at the location, as the report prints it" for the
   target; one clause on AP's 0.01 in/h grid (a day under about 0.12 inch reads 0; 77.6% zeros); one clause that
   "surface temperature" runs hotter than 2 m air (303 location-days above 110 F).
C7 LEAK-9 protocol line (Should; section 5): "A method may use only the rows of a window's train indices (with their
   labels) and of its test indices (without labels); rows outside both, the later seasons included, are never read,
   also not to build features such as whether a line is entered again later." State the measured gain (section 5)
   so a check knows what to look for.
C8 Metric bullet and fit_reason (EV-2), whatever issue 1 decides: on held-out seasons RMSE orders models by the
   location-year level part of the error (tau 0.97), the within-environment part only at tau 0.33 (section 4).
After C1-C8: re-run `dataset check`, the task and leak probes, and refresh the README numbers (house rule).

========================================================================================================================
4. DISPUTED POINTS AND ISSUES FOR THE CURATOR
========================================================================================================================
D1 Who is the actor? (P3; USE-1 Must, USE-5 Must.) Settled: the breeder (or UST coordinator).
   Critic: name the breeder; the metric follows from the actor. Advocate: the paper names insurers and marketing
   decisions; absolute yield serves them; which actor is primary is a curator call.
   Ruling by rank: USE-1 requires a decision that fits the row. A row is one experimental line's entry mean at one
   trial location in one season. The source documents say the UST data "are the basis for decisions on the regional
   release of soybean varieties" (UST reports, practitioner) and the paper's aim is a line's performance in new
   environments. Insurers and marketing act on farm yields of released varieties by region, never on an experimental
   line's trial cell (practitioner: trial-plot yields of experimental lines are a poor proxy for farm yield). Both
   rewordings already name "a breeder or test coordinator". So the actor is a fact of the rows, not a weighing.
   USE-5 holds: the reported absolute yield is the measurement from which the breeder's relative yield is read; a
   number is the right form.

Issue 1 (P6; MET-1 Must, MET-2 Must third bullet, MET-4 Should as amended 2026-11-05, MET-11 Must): keep the
   challenge's RMSE, or score within each environment?
   Problem: on held-out seasons, RMSE ranks models by how well they guess a new location-year's level, which no
   feature predicts, not by how they rank lines, which the breeder acts on.
   Decisive measurement (m1, asked by both sides). 13 untuned models (LightGBM x6: defaults on daily and on weekly
   weather, regularised with and without weather, detrended, deep; HistGB; random forest; extra trees; ridge on
   one-hot ids with and without weather; kNN-50; location mean + trend + shrunk line history) plus two baselines
   (training mean; location mean + trend, constant within a location-year), each window trained once, one seed.
   Kendall tau across the 13 models between the order under RMSE and under mean_group_pearsonr (library convention:
   constant truth left out, constant prediction 0):
     test season              2009  2010  2011  2012  2013  2014  2015 | mean of 6 shipped | mean of 7
     by location-year         0.33  0.56  0.18  0.21  0.36  0.38  0.56 |       0.38        |   0.37
     by loc-year x MG         0.36  0.46  0.21  0.26  0.36  0.33  0.51 |       0.35        |   0.36
     RMSE vs its level part   0.92  0.95  1.00  0.97  0.97  1.00  0.95 |       0.97        |
     RMSE vs its within part  0.46  0.51  0.15  0.26  0.18  0.46  0.41 |       0.33        |
   Among the 9 competitive models (no kNN, random forest, extra trees, ridge with weather) the per-window tau by
   location-year is 0.09 on average (-0.39 to 0.72): no agreement at all.
   On the source's own design (3 random record folds): tau(RMSE, within part) 0.95-0.97, tau(RMSE, by location-year)
   0.44-0.51. So the challenge's RMSE ranked models by the within-environment error; ours ranks them by the level.
   Examples (mean of 6 windows): location mean + trend, which cannot rank lines (r 0), is 3rd of 15 under RMSE
   (12.99), ahead of every LightGBM (13.13-14.60, r 0.21-0.22); ridge on one-hot ids + weather ranks lines as well as
   any model (r 0.214) and is last but one under RMSE (20.18), because the weather extrapolates the level badly.
   Within-environment r separates three tiers (LightGBM, ridge, line history 0.20-0.23; HistGB 0.17; random forest
   and extra trees 0.09-0.11; kNN 0.02); the top tier lies within 0.03. The two groupings agree at tau 0.76 per
   window. Group sizes per test season: 74-88 location-years (median 57-74 rows); 138-158 location-year x MG groups
   (median 36-43 rows, none below 5).
   Sibling: genomic_prediction_soy_yield had tau 0.91 (pooled r vs within-family r) on the same test; here 0.38.
   - Advocate, best evidence: the challenge's verbatim metric (MET-4); RMSE scores the same quantity, bu/acre per
     record, under both splits; predicting an unseen environment's level is the paper's stated aim; a location-year
     pools 2-4 tests, so a within-location-year r partly ranks tests.
   - Critic and practitioner, best evidence: the breeder acts on the within-test ranking (CV0/CV00 "predictive
     ability", Jarquin et al.); oracle level + line effect moves RMSE by 0.0-0.3; the measurement above; MLCAS2021 is
     a research-run challenge, the class MET-4's amendment lets give way when measurements favour it
     (loan_default_prediction_imperial_college overruled on that ground, 2026-11-05); location-year x MG answers the
     pooling objection.
   Ruling on the facts: with the actor of D1, MET-1 asks whether the metric scores the breeder's decision, and the
   measurement says RMSE barely does (tau 0.38; 0.09 among competitive models). By the sibling's own MET-2 test the
   meaning did not survive our split (the within part drove RMSE's order at tau 0.96 on the source's design, 0.33
   on ours). The advocate's (c) is met by grouping on location-year x maturity group. The measurement favours the
   switch.
   Why it is still the curator's: MET-4's amendment leaves the replacement of a lesser-standing competition's metric
   "case by case" to the curator, and a switch is the third case of the protein/huesken reason (a pooled score that
   rewards group means), so an amendment of MET-5/MET-11 is due with it, and it would be the first time that reason
   overrides a competition's metric.
   Decision: (a) keep RMSE with C8's note; (b) Metric.from_context("mean_group_pearsonr") grouped by location-year x
   maturity group (a scoring column built from location, year and maturity_group, MET-2 second bullet), RMSE named
   as the overruled original (MET-11), the m1 numbers in the reason; (b') the same grouped by location-year (the
   literature's environment, larger groups). Recommendation: (b).
   Decide together with genomic_prediction_soy_yield under one rule, not one outcome: there the measured tau 0.91
   kept pooled r by default; here 0.38. That number is the fact that sets the two apart, so (b) here and pooled r
   there is consistent; the amendment's wording should carry the test ("when the pooled score orders models unlike
   the within-group score on the shipped splits").
   Note for (b): the LEAK-9 exploit is worth more under it (section 5), so C7 matters more.

No other issue needs a decision. Both sides call the authors' stable deposit optional.

========================================================================================================================
5. TASK GAMER'S EXPLOIT, MAPPED
========================================================================================================================
E1 A genotype's later-season presence, read from rows outside the window (lines advanced later yielded well: +1.2 to
   +1.8 bu/acre above the trial mean against -0.7 to -1.3). Rule: LEAK-9 (Should), an evaluation-level leak: a method
   reads rows beyond its fold; no deployed model has it (whether a line is entered again is decided after this
   season's yield). Not LEAK-10: no feature column carries it. The definition's only `Potential leak, kept on
   purpose:` note covers the pedigree clusters (LEAK-30); no accepted warning covers it. New.
   Measured gain: under RMSE -0.07 to -0.17 (gamer; about 1%, per split -0.83 to +0.40, none in 2015); mediator m2
   (a fixed shift by later presence on three honest models, 2010-2014): RMSE -0.07 to +0.01, within-location-year r
   +0.02 to +0.05 (mean +0.035 over 6 windows, +0.044 over the 5 with later seasons). Under RMSE the gain is within
   noise; under issue 1 (b) it exceeds the spread of the top tier (0.03).
   Remedy (ladder: a protocol line before changing the data): C7. The gamer's per-split cut of the data is a larger
   remedy, a container-format question shared by every temporal dataset with recurring ids; not needed here.

========================================================================================================================
6. CONSISTENCY WITH PRECEDENT (precedent checker, updated)
========================================================================================================================
Followed: D1 provenance (ai4d_lab pattern: a personal copy accepted on a match with the owners' files; pricing_game,
  genomic: originals gone), after C2; D2 seasons over the source's random split (huesken, genomic, bank_marketing,
  forest_fires' tension row), no drift; D3 no_signal kept (forest_fires, noaa_storm_events_damage); D4 weather as a
  given condition (airfoil, superconductivity's setup) once C1 rewords; D6 LEAK-30 kept (2026-10-19 cases); LEAK-9
  protocol line (bank_marketing, fremtpl2, medical_facility_operational_data).
D7 use case: departed without a fact; C1 fixes it (forest_fires: the source's stated use; chicago_traffic_crashes:
  actor set so the data mirror it).
Metric: (a) keeping RMSE follows MET-4's sponsored-competition cases (zillow_prize, rossmann) but those were not
  measured against a changed split; (b) follows protein_model_quality_rf_pcp and huesken_sirna_efficacy (pooled score
  rewarding group means) and loan_default_prediction_imperial_college (a research-run competition's metric overruled
  on measurements). The open pair is genomic_prediction_soy_yield: the distinguishing fact is tau 0.38 here against
  0.91 there.
In-batch note: ugr16_isp_netflow_intrusion reads a personal mirror because the official site refuses this machine,
  checked against the mirror's own manifest; here the original is gone for everyone and the copy is matched to the
  authors' files. If both ship, each record says which fact sets it apart.

Files: the definition, the record and the measurements (the run's work files).
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR REPORT: uniform_soybean_tests_yield (2026-11-09)
Definition: datasets/_dev/tabarena-v0pt2/uniform_soybean_tests_yield/dataset.py (+ README.md)
Claims list: the builder's claims.md (41 claims). Scratch scripts a1-a12.py and outputs in the run's work files (the authors'
GitHub data_subset files downloaded there, read with allow_pickle=False).

VERDICT
No claim that carries the dataset is refuted. The copy is the authors' data, with stronger evidence than the
builder gave (below). The metric holds. One number is misstated (claim 38, "worse on 4 of 6" is 5 of 6). Claim 41
holds only if it is scoped to "beyond a location mean plus the yield trend"; the builder's own run has weather
helping a direct LightGBM. The open point is one nobody wrote down: the use case and the split assume different
information sets (item U1 below). It is a curator call, not something a test can refute.

KEY NEW EVIDENCE (provenance, claims 1, 7, 27, 28)
- The CyVerse zip's sha256 is e2cecf67...67e6 (matches). Last-Modified is 2021-10-23 21:32 GMT. The entries are dated
  2021-08-30. The Drive file (view and usercontent) answers 404. The INFO529 Makefile line 25 fetches this URL.
- clusterID_genotype.npy is byte-equal (np.array_equal) to the authors' GitHub data_subset/k_means_clusters_20.npy.
- Train+test genotype ids (93,028+10,337) are the same multiset as the authors' genotype_id_all_data.npy (103,365
  rows). The (genotype, state) pairs also match the authors' state_list_all_data.csv as a joint multiset.
- The authors' 2,000-row subset (yield, year, location, MG, 214-day weather): 1,870 rows match a training record on
  (yield, year, location, MG) with identical weather (max abs difference 0.0). The other 130 have their (year,
  location, MG) key in the test inputs (130 of 130). So the copy is the authors' released data split 93,028/10,337,
  and no record was altered.
- The authors' kmeans_clustering.py fits KMeans(20, random_state=1) on USTrelmatrix_GenoID.csv (5839x5839), a
  pedigree matrix with no yields. preprocess_yield.py maps the cluster as kmeans_clusters[int(id-1)]. Claims 27 and 28
  hold.

TABLE (claim | source | test | result | evidence | rule)
1 | data = Shook 2021 UST 2003-2015 = MLCAS2021 | claims.md 1, curation_comments | EvalAI API, paper text, authors' subset | holds | API title/description cites the paper; subset equality above | PROV-8
2 | 26 PDFs converted, no-yield records removed | notes "Source" | paper (WebFetch) | holds | "Files from 2003-2015 USTs were downloaded as PDFs", "all 26 PDFs ... converted to .xlsx", "Records that did not have yield data ... removed" | PROV-3
3 | weather = nearest grid point, 30 km, Weather.com | notes "Source" | paper + challenge text | holds | both quote it | -
4 | Drive zip 404, paper folder empty | download_description | curl | holds (file); folder not re-tested | drive file/view 404, usercontent 404 | PROV-8
5 | CyVerse copy by INFO529 participant, 2021-10-23 | download_description | curl -I, Makefile | holds | last-modified Sat, 23 Oct 2021 21:32:16 GMT, 377,495,546 B; Makefile:25 wget of the same URL | PROV-8
6 | files dated 2021-08-30, before the 2021-09-03 opening | download_description | unzip -l, API start_date | holds | entries 2021-08-30 11:12-18:06; start 2021-09-03T05:00Z | -
7 | shapes match challenge: 93,028 + 10,337, 214x7, 5,839 clusters | download_description | np.load shapes | holds | (93028,5)<U32, (93028,214,7)f8, (93028,)f8, (10337,5), (10337,214,7), (5839,)i4; 103,365 total = paper; 28 states = paper. NOTE: 159 location ids (158 in test), while paper and challenge say "150 locations"; unexplained, see N3 | -
8 | sha256 | download_description | sha256sum | holds | e2cecf6793776eb265fab8367317fdf5d81a6c131ab14498c2af7f66dfd867e6 | -
9 | test yields never published; only training ships | notes | zip listing, API | holds | no yield file under Test Inputs; submission is a (10337,) npy | -
10 | year 2021, source Other, URL DOI | metadata | API dates, paper | holds | paper online June 2021 (vol 16(6)), challenge Sep 2021 | PROV-9
11 | licence: academic use, no commercial use without permission | license | API terms_and_conditions | holds | verbatim "Please do not use any part of this challenge data for commercial use without permission. The challenge data can be used for academic purpose." | EV-4
12 | BibTeX Shook 2021 as the challenge asks | bibtex | API description "Attribution" | holds | the challenge asks for this citation | -
13 | use case: breeder after a season judges weather response, model fit on earlier seasons | task_summary.use_case | source search (paper intro, challenge) | untested (no source states a decision) | the aims hold ("unseen and new environments", "plasticity"); the actor and decision are inferred; see U1 | USE-1
14 | fit approximate: weather known only at harvest | fit_reason | read features vs timing | holds | weather runs 1 Apr-31 Oct; no plot trait in the release (5 "others" columns only) | USE-8, LEAK-10
15 | target bu/acre, 0.4-112.4, 45 < 5 kept | notes Anomaly | on shipped data | holds | min 0.4, max 112.4, 45 below 5; all yields on the 0.1 grid | USE-5
16 | metric RMSE, the challenge's | metric | API evaluation_details | holds | verbatim "We will use Root Mean Square Error (RMSE) as the evaluation metric"; "same scale as the yield values" = bu/acre, identity transform | MET-4, MET-3
17 | 214 exact copies, 172 groups, 92,814 ship | notes Duplicates | duplicated() on raw | holds | 214 / 172; shipped 92,814 | LEAK-19
18 | ~45 ties expected by chance among 3,618 groups | notes Duplicates | histogram of rounded within-group |diff| | holds (estimate; ~31 by my method) | 3,618 raw groups confirmed. Pair counts by |diff|: 0: 256, 0.1: 66, 0.2: 64, 0.3: 56. The 0 bin is half as wide, so chance is about 31 pairs and the excess is about 220 | LEAK-16
19 | 7,586 shipped rows share every feature, different yields kept | notes | duplicated(keep=False) | holds | 7,586 rows / 3,486 groups; 3,795 raw genotype-loc-year groups with >1 row, 848 with >1 MG | LEAK-16
20 | every copy within one year, none crosses a split | notes | key contains year; plus a cross-year near-copy test | holds | (g, loc, MG, yield) equal across different years: 179 pairs at |diff|=0 vs 317 at 0.1 (chance ~158): no cross-year copying | LEAK-17/18
21 | weather identical per location-year; 1,040 series / 1,117 loc-years; 77 shared | notes Weather | md5 per record | holds | 0 location-years with >1 series. All 77 shared series are pairs of different locations in the same year and state (16 location pairs, e.g. loc109/110 MO in 13 of 13 years). The paired trials have different yields (corr 0-0.8, 6 equal yields among 2,000+ common lines): separate trials on one grid point, not copies | -
22 | weather column order and units | WEATHER constant, notes | physics + authors' Data_ts_214_days.py | holds | MaxSur>=AvgSur 99.99%, AvgSur>=MinSur 99.94%, MDNI>=ADNI 100%; ARH 10-100; temps in F (Jul MaxSur ~80-100); MDNI max 1026 consistent with W/m^2 | -
23 | AvgSur_d213 = mean(d212, d214) in 100% | notes Anomaly | isclose | holds | 100% for AvgSur (vs 0.18% at day 100); script fills da[873], which is AvgSur's day 213 (661+212) | PROV-13
24 | day 1 = 1 Apr ... day 214 = 31 Oct, same days each year | notes | calendar signal | holds | corn-belt Jul MaxSur peaks in 2012 (99.6 F; driest July 0.0007 in/h), the 2012 drought; April MinSur orders the states by latitude (QUE 33.7 ... LA 55.3) | -
25 | MG -1 = 00; MN/ONT/ND/QUE/MAN + 64 AR records 2003-04 | notes | counts + those lines elsewhere | holds | 3,001 records with -1. The 28 AR "-1" lines appear elsewhere only as MG -1/0 in MN, ONT, ND, QUE, MAN. The AR weather is southern (Apr MinSur 48-53 F), so they are real early-MG tests in AR, not a mis-coded state | -
26 | 159 location ids, one state each; 5,838 genotypes of 1-5,839 | notes | nunique | holds | 0 locations in >1 state; 5,838 genotypes, max id 5,839 (one id absent from both files) | -
27 | cluster = clusterID[id-1] | _load_raw | authors' preprocess_yield.py | holds | `x_data_cluster[i] = kmeans_clusters[int(id_genotype - 1)]` | -
28 | clusters fit over all 5,839 lines, parentage only; weak LEAK-30 | notes Potential leak | kmeans script; measured effect | holds, and the effect is measured as negligible | on new lines (48-56% of a test season), the training-side cluster mean residual gives RMSE 13.079 vs 13.115 without it (mean of 6 windows). All 20 clusters already occur in 2003. A cluster's share of lines first tested 2010+ is 14-57% | LEAK-30 (weak, Should)
29 | no duplicate or constant columns | the builder's columns check | hash all 1,505 columns | holds | 0 duplicate groups, 0 constant | -
30 | paper/challenge split at random 80/10/10 | notes Split | paper + preprocess_yield.py | holds | "Data were randomly split into training (80%), validation (10%) and test (10%)"; train_test_split(..., random_state=42) | SPLIT-5
31 | every challenge test location-year and genotype is in training | notes Split | set membership | holds | unseen location-year 0.0%, unseen genotype 0.0% | SPLIT-5
32 | 6 yearly windows 2010-2015, expanding, train 58.6-93.1% | splits_comment | container splits | holds | windows 2015..2010, train 86,455..54,370 (0.931..0.586), test 5,730-6,939, no index overlap | SPLIT-6
33 | 44.4-51.6% lines tested earlier; 94.7-98.9% locations seen | splits_comment, decisions | recomputed | holds | new-line share 0.48-0.56; locations seen 0.947-0.989 | LEAK-34
34 | no gap: a season's report is out before the next harvest | splits_comment | arithmetic on the use case | holds by the use case's timing (the model is fit after season X on seasons < X; X-1's report is a year old) | publication dates not checked, and not needed | SPLIT
35 | 2009 window trains on 6 of 13 seasons; 50.7% of rows | splits_comment | count | holds | 6/13 = 0.46 < 0.5; rows before 2009: 50.7% | SPLIT-20
36 | genomic_prediction_soy_yield shares no records | claims 36 | - | untested | UST line ids are anonymized, so identity cannot be checked; the argument (other trials, unit, inputs) is sound | PROV-7
37 | task probes: LightGBM 16.59 vs dummy 16.68, 4/6; RF 16.89 | notes Note | the builder's task probes + own dummy | holds | dummy per window 16.67/16.40/16.64/16.92/17.41/16.02 (mean 16.677); probe file: LightGBM 16.590, 67% of splits | TP-1
38 | location mean 13.71; + LightGBM residual (MG, cluster, year) 13.15; + weekly weather 13.92, "worse on 4 of 6" | notes Note | recomputed location mean; re-read experiment_residual.json | partly refuted (one number) | location mean per window 12.05/13.18/14.45/14.53/15.64/12.41 = 13.71 (holds); 13.15 and 13.92 hold. But residual+year+weekly vs residual+year is worse on 5 of 6 windows (2011-2015), better only in 2010. "4 of 6" is the no-year pair (mg+cluster vs mg+cluster+weekly) | EV-2 (numbers as measured)
39 | SD of a loc-year mean around its loc mean 9.5; oracle env mean 7.3-8.2 | notes Note | recomputed | holds | SD 9.46 over 1,117; oracle 7.29-8.18 | -
40 | random folds: LightGBM+daily weather 6.68, + loc-year id 6.71; seasons 13.7-15.4 | notes Split | env-mean on 3 random folds; log | holds (LightGBM numbers read from the log, not rerun) | loc-year mean on random folds 8.06/7.97/8.03 vs train mean ~16; log has 6.679 / 6.707 | SPLIT-5
41 | the gridded weather, as these models use it, does not predict the new season's level | notes Note | another family: ridge (CV alpha) on 49 monthly weather means at the environment level, predicting the loc-year deviation; plus in-sample correlations | holds when scoped to "beyond a location mean plus trend"; overstated as "nothing measurable" | see N1 | TP-2
M | metric computable on every window (MET-2) | metric | scorer(c) on a dummy and a location mean per window | holds | scorer works on all 6 windows; no scoring columns; unit = record; 5,730-6,939 records per test window. Same target and scale as the challenge, but the challenge scored a random split, so its RMSE level (~5.4 MAE in the paper) is not comparable to ours (~13) | MET-2, MET-3, MET-4

IMPLIED CLAIMS ATTACKED
I1 Every feature known at the prediction point: holds. The release has five record fields plus weather; no plot trait.
   year: test years are never in training. genotype: a new line is an unseen category.
I2 No row is a copy across the split: holds (claim 20, cross-year test; leak probe 0.0%).
I3 Target is the real-world target: holds (the reported plot yield; consistent with the authors' records, 0.1 grid).
I4 Genotype ids are stable lines across years: holds. A shrunken per-line effect from earlier seasons improves the
   location+trend baseline from 13.17 to 13.04 (better on 5 of 6 windows). Random ids would give no gain.
I5 "the line's maturity group" (task_summary.question/known): imprecise. MG is the test's maturity group (the notes
   say so correctly): 215 of 5,838 lines carry more than one MG, and 848 genotype-location-years have one line in two
   MG tests. Wording only.
I6 The split is the one the use case needs: see U1.

REFUTED / UNTESTED, RANKED (principles.md: validity first, Must first)

U1 (P3/P4, USE-1 and SPLIT-6/SPLIT-5; untested, a curator call). The use case puts the prediction "after a season".
   At that moment the breeder holds every yield of that season: the checks and the other lines at the same location.
   The split hides all of them. The temporal split is consistent only because the use case adds "the model is fit on
   the earlier seasons' trials", and no source states that decision (claim 13). The source's own aim, "predict
   performance ... in unseen and new environments", fits the held-out season better than the after-season story does
   (a forecast with the season's weather as given). What it changes: the use_case sentence, not the split. Mildest
   remedy: reword the use case around the paper's aim, e.g. a breeder expects a line's yield in a new season's
   environments from their weather and the line's history. Keep the split (builder issue 3a) and the approximate fit;
   say in issue 4 that the after-season reading would argue for the source's random split.

N1 (P6, TP-2; claim 41 overstated, wording). The builder's own experiment_split.log has daily weather improving a
   direct LightGBM on 4 of 6 windows (mean 14.55 -> 14.19). In-sample, the weather relates to the loc-year deviation
   with the expected agronomic sign (Jul-Aug MaxSur r = -0.13, Jul-Aug precipitation r = +0.13; within year -0.06 and
   +0.10). It adds nothing only once the location level and the trend are in: location mean + linear trend 13.17;
   + monthly-weather ridge instead of trend 13.55 (environment-level RMSE 11.17 vs 11.48). What it changes: the Note
   bullet's reading and issue 2's wording. Mildest remedy: write "beyond each location's mean and the yield trend,
   the weather adds nothing measurable for the models tried". Also note that the floor a model must beat is about
   13.0-13.2: location mean + linear trend 13.17 (equal to the builder's LightGBM residual model, 13.15), + line
   history 13.04. Issue 2's recommendation (a, keep) is unaffected; TP-2 holds since a real if small signal exists.

N2 (EV-2, claim 38; refuted number). "worse on 4 of 6 windows" should be "worse on 5 of 6" for the stated pair
   (residual on MG, cluster, year +/- weekly weather). What it changes: one number in curation_comments and the
   record's Assessment line. Mildest remedy: correct the count.

N3 (P5, PROV; unexplained, low). The paper and the challenge say "150 locations". The release holds 159 location ids
   (1-167 with gaps), each in one state, 16 pairs sharing a weather grid point. The copy is still the authors' data
   (subset equality above), so this is the authors' own count. Mildest remedy: one clause in the State and location
   bullet ("159 ids, where the paper counts 150 locations").

N4 (P7, wording). task_summary says "the line's maturity group"; it is the maturity group of the test the line was
   entered in (I5). Mildest remedy: "the maturity group of the test".

Untested: claim 36 (UST ids anonymized; no test possible). Claim 4's Drive folder was not re-parsed (the file link
was). Claim 40's LightGBM numbers were read from the log, not rerun; my environment-mean figure matches (8.06).

On the builder's draft issues: issue 1 (third-party copy) is now much weaker. The copy is byte-identical in clusters
and matches the authors' GitHub subset and genotype list record for record, so (a) ship from the copy is
well-supported. Issue 2: see N1. Issue 3: see U1. Issue 5: no finding.
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR: uniform_soybean_tests_yield (2026-11-09)

Verdict: ship from the column side. No leak. Two P7 cleaning items (one CLEAN-11 departure, one dtype call to record).
One P3 question that changes the status of 1,498 columns (already the builder's issue 4, seen here from the
columns' side). Several wording fixes for the notes.

Validity: USE-3 holds at the written prediction point (after the season). LEAK-10: no column recorded because of the
outcome; the weather block is a location-year id, but none crosses the temporal split. LEAK-30 weak (pedigree
clusters): agree, keep with the note. LEAK-34 (genotype history): legitimate. LEAK-19 (214 copies): correct, and the
key is complete.
Value: not my part (builder issue 2).
Quality: CLEAN-11 departure, AvgSur_d213 (an impossible fill in 14.9% of rows); CLEAN-14, maturity_group numeric
against the bands bullet (keep it numeric, with the reason written down); notes on AP resolution and on what
"surface temperature" is.
For the curator: Q1 (prediction point and weather), F1 (d213), F2 (MG dtype and wording).

Inputs read: dataset.py, README.md, record, builder_report.md, claims.md, the builder's probes; principles.md, use_case.md,
leak_checks.md, cleaning_features.md (the branch's worktree); Shook et al. 2021 Material and methods (PLOS ONE, via
WebFetch). Measurements are on the raw npy files with _clean's steps reproduced (scripts a1-a5.py in
the run's work files). The dtype probe was re-run: 0 of 1,504 columns flagged, no codebook
(the run's work files).

------------------------------------------------------------------------------------------------------------------
COLUMN TABLE (1,504 features + target; the weather is grouped by variable, 214 day columns each)
------------------------------------------------------------------------------------------------------------------
column | meaning | known at prediction? | dtype and cleaning | verdict | rule

yield_bu_acre (target) | the line's seed yield at the location-year as the UST report gives it, bu/acre (paper:
"yearly seed yield"; whether it is a plot value or a mean over replications is not stated) | the outcome | float,
0.4-112.4, 0.1 resolution, no missing; 45 values below 5 kept as crop failures | fine | USE-5, CLEAN-11, CLEAN-15

maturity_group | the maturity group of the UST test the record comes from (00, 0, I-VIII); -1 = 00 | yes, set before
planting (the test the line enters) | float, the integers -1..8 only. -1 = 00 checked: the 28 lines with -1 occur
elsewhere only as -1 or 0, in MN/ONT/ND/QUE/MAN; the two Arkansas locations (53, 69; 2003-04) ran groups 00 to IV/VI, so
-1 is a real level and not a missing code. 215 lines (3.7% of lines, 11.7% of rows) occur in two adjacent groups
(212 of them one step apart; 154 genotype-years), so this is the test's group, not always the line's own | fine as
numeric, with the call written down (F2); wording fix | CLEAN-14, CLEAN-10

genotype | anonymized line id, 1-5,839 (5,838 in training), no names | yes (the breeder knows the line); its earlier
yields are history | category "g0001"... The id order is barely tied to the label: Spearman with first year 0.15, with
mean yield 0.12 (mostly through the yield trend). Cluster 6 holds 694 of the lowest 1,168 ids, so the ids look
assigned in name order. Typed as a category, the order is not used | fine | LEAK-34, USE-10, CLEAN-14

state | two- or three-letter US state or Canadian province (28), quotes stripped | yes | category; a function of
location (each location in one state) | fine | CLEAN-14

year | trial season 2003-2015 | yes | int, numeric; also the time column (time_on). Every test year lies beyond the
training range; it carries the yield trend (43.8 to 56.7 bu/acre) | fine | SPLIT (temporal), CLEAN-14

location | anonymized location id (159; ids not ordered by yield: Spearman 0.02, or by first year: -0.05) | yes |
category "loc001"... ; 94.7-98.9% of test-season records are at locations seen earlier | fine | LEAK-34, CLEAN-14

genotype_cluster | the challenge's K-means cluster (20) of a 5,839 x 5,839 pedigree correlation matrix; paper: "a
completely connected pedigree for all lines with available parentage information"; also "genotypes were clustered
based on the organization which developed them" | yes, parentage is known before planting; only the boundaries are
fit with later lines | category "c00".."c19"; constant per genotype (a coarsening of genotype); cluster shares drift
with the years (cluster 1: 11% of 2003 rows, 0-1% from 2013; cluster 14: none in 2015) | potential leak kept on
purpose (weak), as the notes say. A source file joined by id, not a feature we built (CLEAN-6 does not apply) |
LEAK-30 (Should, weak)

ADNI_d001..d214 | average direct normal irradiance per day, 1 Apr - 31 Oct (unit not stated by the source) | at the
written prediction point (after the season), yes; at planting, no (Q1) | float, 0.01 grid, no missing. Zeros on 2.3% of
location-days, always together with MDNI = 0. Checked as real overcast days: on zero days the diurnal range is 9.2 vs
21.1 F, precipitation >0 on 85% vs 22% of days, RH 88% vs 67%, and this holds in every 30-day block. Zeros are more
common in Oct (7.6% of days 181-210); runs of at most 5 days | fine (the builder's reading is confirmed) | CLEAN-10,
CLEAN-11

MDNI_d001..d214 | maximum direct normal irradiance per day | as ADNI | float, 0-1,026, zeros as ADNI | fine |
CLEAN-11

AP_d001..d214 | average hourly precipitation per day, inches (authors' script) | as ADNI | float with 35 distinct values
on a 0.01 in/h grid. A step is 0.24 inch a day, so a day with up to about 0.12 inch total reads 0 (77.6% of days read 0).
Max 0.36 in/h (8.6 inch/day; AR 2011, day 136); 45 location-days above 0.2 | fine, the source's coarse resolution; one
note line worth adding (N1) | CLEAN-1, PROV (as published)

ARH_d001..d214 | average relative humidity, % | as ADNI | float, 10.3-100, no fill pattern | fine | -

MaxSur_d001..d214 | maximum "surface temperature", F | as ADNI | float, 0.1 grid; 20.5-117.8. 8,079 location-days
above 100 F, 303 above 110 F, including MN (11), ND (3) and MI (1): hotter than 2 m air temperature usually reads, so
"surface" may be the ground or skin temperature of the gridded product | fine as released; meaning note (N2) | CLEAN-1

MinSur_d001..d214 | minimum surface temperature, F | as ADNI | float, -6.2 to 89.4; never above MaxSur | fine | -

AvgSur_d001..d212, d214 | average surface temperature, F | as ADNI | float; corr. with (Max+Min)/2 0.994; inside
[Min, Max] on every day except d213 | fine | -

AvgSur_d213 (30 Oct) | the authors' fill: the mean of d212 and d214 in 100% of rows (authors' script: "Index(873) of
Avg. Surface Temp is NA") | as ADNI | NEW: it lies outside that day's [MinSur_d213, MaxSur_d213] in 13,843 rows (14.9%;
178 of 1,117 location-years; up to 11.9 F; 4.6% to 32% by year). An average outside its own min-max is impossible, and
the value holds no observation of that day | cleaning problem (F1) | CLEAN-11 (Should), CLEAN-5 in spirit

Dropped rows / copies | 214 exact copies (same 6 record fields + cluster + yield) | - | The drop key leaves out the
1,498 weather columns. That is safe: each of the 1,117 location-years has exactly one weather series (0 with two), so
the weather is a function of (location, year). All copies are within one year | fine | LEAK-16, LEAK-19

Not shipped | the 10,337 challenge test records (no yields); no source column was dropped (5 fields + cluster + 7x214
weather all ship) | - | - | fine | CLEAN-22

------------------------------------------------------------------------------------------------------------------
CHECKS ON THE TASK'S FRAMING (from the brief)
------------------------------------------------------------------------------------------------------------------
* A location-year id by another name. The weather block is one: 1,040 distinct series for 1,117 location-years, 0
  location-years with more than one series, 77 series shared by two locations of the same state in the same year,
  none shared across years. (location, year) gives the same id. Under the shipped split the test season is held out
  whole, so no test location-year is in training. hidden_groups confirms it: "(all but genotype)" keys are 0% seen in
  training, and single-day values recur 4-18% by chance. Not a leak here. Under the source's random split (builder
  issue 3, option b) this block is what turns the task into reading off the environment level (builder: 6.68 with
  weather vs 6.71 with a location-year id). That is an argument for keeping the seasons split, not an action on the
  columns.
* A window that ends at the outcome (LEAK-10). No: the window is a fixed calendar span (1 Apr - 31 Oct, 214 days every
  year, no missing value). Neither harvest nor maturity cuts it, and weather is a cause of yield, not a consequence.
  Weather after a line matured (MG 00-0 lines mature in September) is recorded after the yield is fixed, but it is
  exogenous and cannot carry the yield. At the written prediction point (after the season) it is known.
* Daily as released vs the paper's weekly means (CLEAN-19, CLEAN-22). Keeping the daily values is right: CLEAN-19
  builds a feature only when the raw data cannot be used as it is, and the daily values can. The weekly averaging
  (the paper's "downsampling the daily data to weekly", 30 steps; S5 Text: "first 210 days") is the authors' model
  choice. CLEAN-22 forbids narrowing for width. The builder also measured no gain from weekly (14.47) over daily
  (14.76) on held-out seasons.
* Missingness caused by the outcome: no column has a missing value; no proxy codes (MG -1 checked above).

------------------------------------------------------------------------------------------------------------------
PROBLEMS, RANKED (principles.md: P3 > P4 > ... > P7; Must > Should > Weigh)
------------------------------------------------------------------------------------------------------------------
Q1 (P3, USE-1/USE-3; USE-9's weighed factor "a use case rephrased only to excuse a gap" (-); question for the
curator; the same issue as builder issue 4)
  The weather is admissible only because the prediction point is placed after the season, when the yields are in hand
  too. At the decision a breeder takes before a season (which lines to enter or advance, where to place them), the
  season's weather does not exist yet, and all 1,498 weather columns would be LEAK-10 (a value that did not exist at
  the prediction point). The source's own model uses the season's weather (paper, challenge), so the ex-post framing is
  the source's task, and fit "approximate" already names the gap. Evidence that the choice costs little either way:
  on held-out seasons, location mean + residual LightGBM scores 13.15 without weather and 13.92 with the weekly
  weather (builder, experiment_residual.json), so a planting-time version without the weather would score about the
  same.
  Options: (a) keep as built: the ex-post use case, fit approximate, weather as the source's inputs (no change);
  (b) move the prediction point to planting and drop the 1,498 weather columns (a different task of our own, losing
  the source's main inputs). Recommendation: (a), with the use case's ex-post nature kept explicit in fit_reason (it
  already is).

F1 (P7, CLEAN-11 Should; cleaning problem, cheap and safe)
  AvgSur_d213 is an interpolation by the authors in every row. In 13,843 rows (14.9%; 178 of 1,117 location-years) it
  lies outside the same day's [MinSur_d213, MaxSur_d213], by up to 11.9 F. No other day ever does
  (columns_check.txt's "AvgSur outside [Min,Max] share 0.00069" is exactly these cells). The Anomaly bullet says the
  value was filled, but not that the fill is impossible in 15% of rows.
  Mildest remedy: (a) set AvgSur_d213 to missing in the rows where it falls outside [MinSur_d213, MaxSur_d213]. That is
  the rule's own remedy; rows stay. (b) Set it missing in every row, or drop the column, since it holds no observation
  (it is a fixed function of d212 and d214). (c) Keep as released, adding the count to the Anomaly bullet (a
  documented departure). Recommendation (a) or (c); either way the bullet should give the 13,843 rows / 178
  location-years.

F2 (P7, CLEAN-14 Should; a dtype call to write down, plus a wording fix)
  maturity_group ships as a number (-1..8). The bands bullet of CLEAN-14 reads "Bands of a quantity ... are ordered
  categories". The curator's test for scales points the other way: a value between two levels means something (a
  relative maturity of 2.5 lies between groups II and III, and the groups are equal steps of relative maturity, with 00
  one step below 0). Numeric is defensible and lossless. Recommendation: keep numeric and add one clause to the note
  ("bands of equal width on the relative-maturity scale, kept as numbers: a value between groups is meaningful;
  CLEAN-14"). The alternative is an ordered category ["00","0","I",...,"VIII"].
  Wording: task_summary.question and .known say "the line's maturity group". 215 lines (11.7% of rows) appear in two
  adjacent groups, and 154 line-years carry two groups. The value is the group of the test the record comes from:
  "the maturity group of the test" is the accurate wording, and the Maturity group bullet could say so with these
  counts.

N1 (P7, note only) AP has 35 distinct values on a 0.01 in/h grid: a day with up to about 0.12 inch of rain reads 0,
  which is part of why 77.6% of days are 0. One clause in the Weather bullet.

N2 (P7, note only; meaning) "Surface temperature": 303 location-days above 110 F, including Minnesota, North Dakota
  and Michigan, and 8,079 above 100 F. These values look high for 2 m air temperature. The notes already use the
  source's word ("surface temperature"); adding "as the source names it; its values run hotter than 2 m air
  temperature" would stop a reader from assuming screen-height air temperature. No change to the data.

Confirmed fine (no action): genotype_cluster (LEAK-30, weak, kept with the existing note; parentage and breeding
organization are known before planting); genotype (LEAK-34); location, state, year; the zero irradiance days (real
overcast days, by the conditional checks above); the 214 copies (the key is complete); daily weather as released
(CLEAN-19, CLEAN-22); all 1,504 dtypes (dtype probe: 0 flagged).

Files: the report, scripts and outputs (the run's work files).
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR REPORT: uniform_soybean_tests_yield (2026-11-09)
Folder: datasets/_dev/tabarena-v0pt2/uniform_soybean_tests_yield/ (dataset.py read; container built once)
Scratch: the run's work files (prep.py, structure.py, season_share.py, alt_splits.py and their logs)
Numbers: untuned, one seed, LightGBM with the builder's parameters (600 trees, lr 0.03, 31 leaves, min_child 100,
colsample 0.3), weekly means of the weather (30 weeks x 7) in place of the daily columns; thread caps 4.

VERDICT: right with notes.
Held-out seasons (temporal by year, expanding) is the regime the source's stated aim implies and the one that keeps
both new environments and new lines honest. The source's random split and a split grouped by location-year were run
and both overrate what a model does for a new season. The notes: the use_case text describes a moment at which the
season's own results are known, which contradicts the regime (finding 1); the window count stops at 6 on a
seasons-based share though SPLIT-14 counts rows (finding 3).

------------------------------------------------------------------------------------------------------------------
WHAT WAS CHECKED (facts)
------------------------------------------------------------------------------------------------------------------
Windows (from c.experiment_metadata.splits, never re-split): 6 windows, newest first, one season each, expanding train
from 2003, no gap.
  test 2015: 6,359 rows, train 86,455 (93.1%)    test 2012: 6,939, train 67,586 (72.8%)
  test 2014: 5,730, train 80,725 (87.0%)         test 2011: 6,396, train 61,190 (65.9%)
  test 2013: 6,200, train 74,525 (80.3%)         test 2010: 6,820, train 54,370 (58.6%)
SPLIT-14 holds (6 >= 3 windows, smallest train side 58.6% >= 50%). Each window has its own train side. Windows are
contiguous whole seasons (season-shaped, SPLIT-20), 5,730-6,939 test rows each (SPLIT-17 not triggered).

Time column: `year` is the trial season (one location-year per location per year: 1,117 location-years, 74-95 per
year, 159 locations). Each season is a whole planting-to-harvest cycle; the weather columns cover 1 April-31 October
of that season and are shared by every record of a location-year.

Gap / late labels (SPLIT-9, SPLIT-10): the label of a season-Y record is the UST report of season Y; every training
row is from a season strictly before the test season, so no training label is later than the test season's
prediction point. The time unit (a season) is longer than the report delay. No shortcut row; no gap needed. Holds.

Training history (SPLIT-20): all of 2003 onward; no documented break. Yearly mean yield 43.8 (2003) to 56.7 (2015)
bu/acre; location-year means sit +3.6, +4.3, +4.5 above their location's 13-year mean in 2013-2015 (-4.6 to +2.2
before): a trend (genetic gain) the test windows carry, real drift, not an atypical window. 2012 (the Midwest drought
year) is not atypical in these trials (mean deviation +0.17); 2009 is high (+2.2). No window is chosen by score.

Recurring entities (SPLIT-13, USE-10):
  - Lines: the anonymized `genotype` ids are consistent across years (every id has one pedigree cluster in every
    year; 215 of 5,838 ids carry two maturity groups, read as a line entered in two tests). Years per line: 1 year
    4,194, 2 years 1,026, 3 years 355, 4 years 153, 5+ years 110 (13,376 rows; the long runners are most likely the
    check cultivars). Share of a test season's records whose line was tested earlier: 51.6, 50.6, 45.8, 44.4, 49.5,
    47.2% (2010-2015), almost all of them in the previous season (43.5-50.0%); the same line at the same location
    earlier: 32.4-35.7%. A line is grown at a median 10 locations per season, a location-year holds a median 65 lines.
    The task is half warm start (lines with earlier trials, legitimate history, LEAK-34) and half cold start (new
    entries), as the UST is. Measured value of the line history: location mean 13.71 -> location mean + shrunk line
    effect 13.39 on the shipped windows.
  - Locations: 94.7-98.9% of a test season's records are at a location seen earlier; the location-year (the
    environment) is never on both sides (hidden-group probe: `(all but genotype)` keys 0.0% seen in train; exact
    feature copies across windows 0.0%).
  - Variance: the location-year mean explains 75.3% of record variance in-sample (within-environment variance 62.8 of
    254.6); a location-year mean varies around its location's mean with variance 89.4 (SD 9.5), of which the
    season-wide mean over all locations explains only 8.3%; the other environments of the same state and season
    correlate 0.31 with it.

------------------------------------------------------------------------------------------------------------------
THE ALTERNATIVE SPLITS, MEASURED (mean RMSE, bu/acre; per fold in alt_splits.log)
------------------------------------------------------------------------------------------------------------------
                                        temporal (shipped,  random records   grouped by
                                        6 windows)          (3-fold)         location-year (3-fold)
  training mean                         16.68               15.96            15.99
  location mean (state fallback)        13.71               12.01            13.27
  + same-season shift (other locations) 13.71 (n/a)         11.69            12.99
  location mean + line effect           13.39               11.48            12.71
  environment mean + line effect        13.45 (fallback)     7.60            12.71 (fallback)
  LightGBM base, no weather             13.60               9.86             12.52
  LightGBM base + weekly weather        14.31               7.13             12.35
Base = maturity group, genotype, state, year, location, cluster.

Reading:
  - Random records (the source's split): every test record's location-year is in training (100.0%) and 99.9% of its
    lines. The score halves (7.13 against 14.31 for the same model) and the gain is the environment's level read off
    the other lines of it: the environment mean alone reaches 8.02 and the weather becomes the environment's code
    (LightGBM with weather 7.13 against 9.86 without; the builder's one fold: weather 6.68 against a location-year id
    6.71). The ranking flips: under random records the weather model is best by 2.7; on held-out seasons it is the
    worst model but the training mean (14.31 against 13.60 without weather; it loses on 4 of 6 windows, 2012-2015,
    and wins on 2010 and 2011). A benchmark under the random split would rank models by how well they memorize the
    environment code, not by the task the paper names.
  - Grouped by location-year: 0.9-1.4 better than temporal for every predictor. Two things carry it: later seasons in
    training (the yield trend: temporal location means miss +3.6 to +4.5 in 2013-2015) and the same season's other
    environments (the season shift alone moves the location mean 13.27 -> 12.99; the weather gains a little,
    12.35 against 12.52, as it now names a season that is in training). Both are information a new season does not
    have. It is not the regime (SPLIT-3: one regime, the use case's; a new season is a stream over time).
  - "Sparse testing" (fill in a line at a location-year where it was not grown): the random split does not mirror it.
    The held-out records are plots that were grown and reported, among their test's own entries; a UST line is
    missing at an environment mostly because it was not in that test or maturity zone (a median 10 of 74-95 locations
    per season), so the real fill-in queries are structured, not random. The source names no such use (the paper's
    aim: "predict performance (for example, seed yield) in unseen and new environments", Introduction; also climate
    scenarios and "crop insurance recommendations ... based on weather forecasts before planting", Discussion). With
    anonymized ids and a weather block that only codes the environment, it is matrix completion on ids. At most a
    candidate variant (SPLIT-31), not the shipped split.

------------------------------------------------------------------------------------------------------------------
FINDINGS, ranked (principles.md: P3/P4 validity first)
------------------------------------------------------------------------------------------------------------------
1. The use case text describes a moment the split does not mirror (P4 with P3; SPLIT-1, USE-3, USE-10; Should,
   wording).
   Evidence: `use_case` reads "A soybean breeder, after a season, sets the yields each line in the regional trials
   should have given under that season's weather beside what it gave"; `curation_comments` puts the prediction point
   "after a season". At that moment every yield of the season is in hand, the other lines of each location-year
   included, and an actor with them would read the environment's level off them, which is the information the random
   split hands over (environment mean 8.02 against 13.71 for the location mean). The held-out-season regime is right
   for a prediction made without the season's trial results: the paper's "unseen and new environments", a new season
   predicted from its weather (a scenario or the observed season before its results are compiled). As written, the
   use case argues for the split the definition rejects.
   Mildest remedy: reword `use_case` (and the prediction-point bullet) so the season's own trial results are not
   known: e.g. a breeder or test coordinator predicts each entry's yield at each location of a season that is not
   in the data yet, from the line, the site and the season's weather (as a scenario or as observed), with the model
   fit on the earlier seasons' trials. Keep fit approximate (the weather is known only at the season's end). No change
   to the split.

2. The source's random split is a framing to record, not adopt (P4; SPLIT-5, SPLIT-31; Weigh, note).
   Evidence: the table above; random records 7.13 against 14.31 for the same model, ranking flipped, the weather a
   code for the environment. Grouped by location-year (12.35-12.52) leaks the season level and later seasons.
   Mildest remedy: none to the split. Add one line to `splits_comment` (or the curation bullet that already gives
   6.68/6.71) with the grouped-by-location-year number and why it was not chosen (later seasons and the same season's
   environments in training), so issue 3's option (c) is measured, not argued. Issue 3 recommendation (a) holds.

3. The window count rests on the wrong share (P4; SPLIT-14, SPLIT-15; Should, minor).
   Evidence: `TemporalSplits(unit="unique", min_train_fraction=0.5)` measures the train share in distinct seasons, so
   the 2009 window (6 of 13 seasons, 46%) is cut; SPLIT-14's floor is the share of the data, and 2009 would train on
   47,067 of 92,814 rows = 50.7%. SPLIT-15 asks for as many windows as folds (9). `splits_comment` gives the seasons
   reason ("at least half of the 13 seasons").
   Mildest remedy: either keep 6 and reword the comment (the 7th window would sit at 50.7%, on the floor), or add
   the 2009 window (explicit `cutoffs=[2015, ..., 2009]`). Keeping 6 is defensible; the text should say why by rows.

4. For issue 2 (P6, not a split defect): "models near the dummy" is a property of the 1,498 daily weather columns,
   not of the regime. Under the shipped windows a LightGBM without weather reaches 13.60 (beats the location mean on
   4 of 6 windows, 2012-2015), the location mean plus a shrunk line effect 13.39, against the dummy's 16.68 and the location
   mean's 13.71; adding the weather worsens LightGBM to 14.31. So the split leaves a real signal from the site and
   the line's history; what it removes is the environment level, which the weather does not predict for these models
   (unstable across windows: LightGBM without weather ranges 11.26-16.40, the location mean 12.05-15.64).

Not findings (checked, hold): no training label later than a test season (SPLIT-9); no gap needed (SPLIT-10: the
season unit exceeds the report delay); the environment never crosses a window (0.0%); 214 exact copies dropped all
within one year; expanding train sides (SPLIT-11), newest window first; group id question not applicable (temporal),
and the `genotype` id is a recorded, consistent id, not a cluster or hash (SPLIT-24) should a variant ever group on it.

Judgment record:
  Verdict: right with notes.
  Validity: SPLIT-1 holds for the paper's aim (new environments), the use_case wording does not match it (finding 1,
  reword); SPLIT-5 applied (source's random split checked and rejected with numbers); SPLIT-9/10 hold, no gap;
  SPLIT-13/USE-10: half warm start (lines tested earlier, 44-52%), half cold start, as the trials are; SPLIT-14 holds,
  SPLIT-15 note (finding 3).
  Value (for issue 2): signal under the split from site and line history (13.39-13.60 against 16.68), not from weather.
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER: uniform_soybean_tests_yield (2026-11-09)
Actor played: a public soybean breeder who enters lines in the USDA Uniform Soybean Tests (UST), and the UST
coordinator who decides which lines go on from the Preliminary to the Uniform Tests and which locations they go to;
secondarily a seed company predicting a line's yield in a new season and place.

VERDICT
Fit: approximate (agree with the definition), but for a different main gap than the one fit_reason names. The
season's weather known only at harvest is a real but minor gap (it adds nothing measurable anyway). The larger gap:
my decision ranks lines within a test against its checks. The dataset predicts absolute yield and scores it with
RMSE. On held-out seasons that makes the score mostly a test of guessing each location's level that season, which
I do not act on.
Metric scores my decision: PARTLY. I would pick models by the mean within-environment correlation of predicted and
observed yield ("predictive ability", the breeders' CV0/CV00 statistic), i.e. `mean_group_pearsonr` grouped by
location-year (or by location-year x maturity group). RMSE could stay as the second score or as the declared metric
under MET-4, with the gap named.
Little signal beyond the location means: REALISTIC, not useless. Predicting a new season's level at a site from
30 km gridded weather, with no planting date, soil or management, is known to be hard. The line differences that
remain are modest but present (numbers below).

SOURCES USED
- dataset.py and claims.md in the worktree; builder_report.md; the builder's residual experiment (the run's work files).
- Shook et al. 2021, PLOS ONE 16(6):e0252402 (https://doi.org/10.1371/journal.pone.0252402). Its aim is to "predict
  performance ... in unseen and new environments". It calls itself "a retrospective design", splits 80/10/10 at
  random, reports RMSE/MAE/R^2, and says the model is "limited in its ability to generate genotype-specific yield
  predictions". Users it names: "plant breeding decisions, marketing decisions", crop insurers, cooperatives.
- USDA-ARS Uniform Soybean Tests Northern Region (Purdue e-Pubs, https://docs.lib.purdue.edu/ars/83). The tests
  "critically evaluate the best of the experimental soybean lines". "Preliminary Tests are grown at a limited
  number of locations ... for one year" before lines are dropped or advanced. Uniform Tests have more locations and
  replications. The data "are the basis for decisions on the regional release of soybean varieties". The yearly
  report PDFs (ars.usda.gov/ARSUserFiles/50200500/UST/<year>.PDF) are tables by test (UT 00 to IV, PT I to IV): one
  entry mean per location, with check cultivars, means, ranks and LSD/CV.
- The G x E cross-validation schemes in breeding (Jarquin et al.; Vieira, Persa, Chen & Jarquin 2022, Front. Genet.
  10.3389/fgene.2022.905824): CV2 = tested lines in observed environments (sparse testing), CV1 = untested lines in
  observed environments, CV0 = tested lines in untested environments, CV00 = untested lines in untested
  environments. Accuracy is reported as the correlation within environment.
- My own measurement (scratch: rank_skill.py and its log, the run's work files), run on
  the release's npy files with the shipped de-duplication (92,814 rows) and the shipped 6 yearly windows. It used
  untuned LightGBM, one seed, season-period weather means and the genotype id as a category.

MEASURED (breeder's view of the held-out seasons)
- Variance split: SD of yield 15.96 bu/acre. SD within a location-year (yield minus its location-year mean) 7.93.
  So 75.3% of the variance lies between location-years. A location-year holds a median of 69 records (65 lines),
  pooled over the maturity-group tests grown there.
- RMSE, per window 2010..2015:
    location mean of earlier seasons             12.62 16.07 14.56 14.72 13.62 12.77 (mean 14.06)
    LightGBM (all fields + geno id + period wx)  12.02 15.34 15.19 14.14 11.90 11.85 (mean 13.41)
    oracle: test location-year mean               7.29  7.40  8.18  7.57  7.53  8.14
    oracle level + line effect from history       7.20  7.43  7.90  7.53  7.46  7.93
  Knowing each test environment's level removes about 45% of the RMSE. Adding everything the data says about the
  line removes another 0.0-0.3 bu/acre. RMSE therefore ranks models almost entirely by the level term.
- Within-location-year Spearman of prediction vs truth, about 74-87 location-years per window:
    LightGBM, all records                         0.235 0.218 0.213 0.143 0.137 0.206
    shrunken line history (residual vs env mean)  0.224 0.192 0.207 0.168 0.157 0.221
    LightGBM, lines tested in an earlier season   0.251 0.275 0.225 0.225 0.219 0.256
    LightGBM, lines new that season               0.119 0.122 0.112 n/a  0.014 0.128
  For the 44-52% of records whose line has earlier records, the line's history ranks lines at about 0.2-0.3.
  For new lines, maturity group and pedigree cluster give about 0.0-0.13. These are the CV0 and CV00 settings,
  at about the level the literature reports for coarse inputs.
- 263 lines appear in 4 or more seasons and carry 21.9% of the records. Most are likely the check cultivars
  (unflagged in the release), plus lines moving from PT to UT.

1. INPUTS AT THE MOMENT OF PREDICTION
My moment is the winter before a season: choose which lines to advance and enter, and where.
- Maturity group, pedigree cluster, line id (and so the line's earlier UST yields), location, state, year: I have
  all of them. Parentage is known when a line is entered. The clusters were fit over all 5,839 lines (LEAK-30,
  weak; I agree it can stay).
- Daily weather from 1 April to 31 October: I do NOT have it at my moment. I would have the location's climate
  history, which the location id already gives a model. The weather only exists at harvest. Read as a perfect
  seasonal forecast, it is the stand-in that makes the fit approximate (USE-3, USE-8). It adds nothing measurable
  for any model the builder or I tried, so the gap costs the task little in practice.
- What I would always have and the data lacks, ranked:
  (a) The test the record belongs to (PT or UT, which maturity-group test) and which entries are the checks. I judge
      a line only against the checks of its own test at the same location. Location-years here pool 2-4 tests.
  (b) Planting date, soil, irrigation or tillage, and the location's trial quality (CV, LSD, replications). All
      are in or behind the yearly report.
  (c) The line's full relative maturity (the release keeps the integer group only), herbicide trait (RR or
      conventional) and the breeding program.
  None of these can be recovered from the release: line and location ids are anonymized. The dataset can only name
  them as gaps.

2. TARGET
- The record is the entry mean of a line at one location (reps averaged, as the report prints it), in bu/acre.
  task_summary calls it "a plot's yield"; it is a location entry mean. That is fine as a measurement.
- I do not act on the absolute bu/acre. I act on the line's yield RELATIVE to the checks and the other entries of
  its test: the rank, the percent of check mean, and the difference against the LSD, averaged over locations. A
  number is the right form (regression). But the quantity I act on is the within-environment deviation. The
  environment's level is shared by every entry and cancels out (USE-5).
- A seed company or insurer would want absolute yield. Trial-plot yields of experimental lines are a poor proxy for
  farm yield, though, and none of them makes a decision per trial cell.

3. ROW, DECISION UNIT, TEST DATA
- One row is one line x location x season cell. For placement, the cell is a unit I act on. For advancing a line,
  my unit is the line across a test's locations: one decision per line per season, made from about 10-30 cells.
  Scoring per cell is acceptable if the score is centred per environment.
- The test data is what I face: a new season, 95-99% of records at locations seen before, and about half the lines
  with history (the PT-to-UT path and the checks). The held-out-season split mirrors this (SPLIT-5, USE-10: a known
  entity with legitimate history plus new entries). I agree with the builder's choice over the source's random
  split.
- Sparse testing (the source's random split, CV2) is real breeding practice: grow each line at a subset of the
  season's sites and predict the rest from the lines grown there. But the UST does not run that way: each test's
  entries go to all of its locations, and missing cells are lost plots. In that framing the 1,498 weather columns
  only name the environment (builder: RMSE 6.68 with weather against 6.71 with a location-year id), so the dataset
  would be a matrix-completion task with dead features. I would not choose it as the main framing.

4. WOULD I USE THIS MODEL?
- As specified (absolute yield, picked by RMSE): no. A model that guesses a location's level for next season well
  and ranks the lines at random would win over one that ranks lines well and misjudges the level by 8 bu/acre. My
  decision is the reverse.
- I would trust a model that, on held-out seasons, ranks lines within a test better than the lines' own history
  mean (the "shrunken line history" row above, 0.16-0.22). I would also want it to report how it does on new lines
  apart from lines with history, and to stay stable from one season to the next. I would distrust any score from a
  random split (the source's R^2 of 0.80 comes almost entirely from the environment level being in training).
- Is the weak signal useless or realistic? Realistic. Season-to-season level shifts at a site come from rain
  timing, disease, hail, planting date and management, which 30 km gridded daily weather does not capture. CV0 and
  CV00 accuracies in the G x E literature are modest. A benchmark that shows weather adding nothing on held-out
  seasons tells the truth about this data. What is left for a method to win is (i) the location level, through the
  year trend and location history, and (ii) the line effect through a high-cardinality line id. Both are honest
  tabular skills. Under RMSE, (i) dominates and is noisy: about 80 location-years per window and unstable across
  windows (builder: `unstable`, `drift_baseline`).

5. METRIC (MET-1, MET-4, MET-10)
- Declared: RMSE on bu/acre, the MLCAS2021 leaderboard metric (MET-4, origin source). Under the challenge's random
  split, every test location-year was in training. RMSE then mostly scored the within-environment deviations (the
  environment level is known: location-year mean RMSE 8.06, LightGBM 6.68). That is close to the breeder's
  quantity. Our held-out-season split changes what the same metric measures: about 75% of the variance and about
  half of every model's RMSE is now the unseen environment level. This is MET-10's "whether our task is still the
  source's", measured on the shipped splits. It is the evidence MET-4 asks for to overrule the source's metric for
  the use case.
- Scores my decision: PARTLY. RMSE is a proper score for the yield number and is right for an absolute-yield actor
  (insurer, marketing). It barely moves with how well a model ranks lines within an environment (oracle level +
  line effect improves RMSE by 0.0-0.3 bu/acre).
- What I would choose: `mean_group_pearsonr` (in the library, MET-12) with the group = location-year, i.e. the
  breeders' "predictive ability". A tighter group is location-year x maturity_group, as a proxy for the test, since
  the release has no test id. The group is built from features (location, year), so it ships as a scoring column
  (MET-2). An alternative is RMSE after subtracting each environment's mean from truth and prediction (RMSE of the
  deviations), which keeps bu/acre units. MET-6 to MET-9 do not apply: no threshold, cost or k is fixed by the
  source. The UST advances or releases a handful of top lines per test, so `mean_group_top_k_overlap` could be
  argued, but no k is fixed, so I would not use it.
- If the curator keeps RMSE (MET-4, the source's choice), the notes and fit_reason should say that on held-out
  seasons RMSE mostly scores the level of a new location-year, not the line ranking a breeder acts on.

GAPS BETWEEN DATASET AND DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Absolute yield scored by RMSE vs within-test ranking (USE-5, MET-1). The environment level is 75% of the
   variance and about half of the RMSE, and the breeder ignores it. This changes what a winning model is. Fix: the
   metric (above), or a second metric in the notes.
2. Weather known only at harvest (USE-3, USE-8). For a forward decision it stands in for a perfect forecast; for
   the builder's post-season use case there is hardly a prediction decision at all (the breeder then has the real
   yields and the checks). Measured to add nothing, so it changes the task little in practice. It still needs to be
   named, and is named.
3. No test id and no check flag (USE-5). Lines cannot be compared within their own test or against their checks,
   and the location-year pools several tests. This cannot be repaired from the release.
4. No planting date, soil, management or trial-quality fields. These would carry the season-level signal the weather
   does not. Not repairable; name it in fit_reason (it already names soil, planting date and management).
5. The decision unit for advancing a line is the line across locations, not the cell (MET-17-like). Minor: centring
   per environment covers most of it.
6. Pedigree clusters fit over all lines (LEAK-30, weak). Kept, agree.

WHAT AN EXPERT WOULD CHANGE
- Rewrite the use case toward the forward decision the paper names ("unseen and new environments"). For example: "A
  breeder or the UST coordinator, before a season, predicts how each advanced line will yield at each test location
  of the coming season, relative to the other entries there, to choose which lines to advance and where to test
  them. The season's observed weather stands in for a perfect seasonal forecast." The current post-season "compare
  with what the weather predicts" use case is not a decision a breeder makes today. After harvest the breeder
  compares against the checks grown beside the line, and the use case reads as rephrased to fit the data (USE-1,
  the USE-9 weighed factor). Fit stays approximate either way. fit_reason should lead with the relative-vs-absolute
  gap, or the weather-as-perfect-forecast gap, and add the missing test or check structure.
- Score within environments (mean_group_pearsonr by location-year), or at least report it. Keep RMSE only with the
  caveat above.
- Keep the held-out seasons. Do not go back to the random split, under which the weather is an environment code.
- Fix the wording "a plot's yield" to "the line's entry mean at the location (as the report prints it)" if that is
  how the reports present it (the report tables show location means over replications).
- No need to aggregate the weather to weeks; it carries no signal either way (builder's probes).

ISSUES FOR THE REVIEW (rank order)
A. (P6/P3, MET-1, MET-4, MET-10, USE-5; Should) RMSE on held-out seasons scores the environment level, not the line
   ranking the actor acts on. Options: (a) keep RMSE, with the gap in the notes and fit_reason; (b) declare
   mean_group_pearsonr by location-year, with the measured overrule evidence; (c) RMSE of the per-environment
   deviations. My recommendation: (b). (a) is defensible under MET-4 if the curator weighs the challenge's record
   more heavily.
B. (P3, USE-1, USE-9 factor; Weigh) Rewrite the use case as the forward placement/advancement decision with the
   weather as a perfect forecast. The current post-season use case is not a decision made today.
C. (P3, USE-5; Note) Name the missing test or check structure, and the location-years pooling several tests.
D. On the builder's issue 2: the weak signal is realistic. It is no reason to retire the dataset (TP-2). Under (b)
   above, the models measurably separate (Spearman 0.14-0.24, from line history), and the task tests the use of a
   high-cardinality line id.
E. On the builder's issue 3: agree with (a), seasons. Sparse testing is real practice but not the UST's design, and
   with it the weather columns would be dead weight.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW - uniform_soybean_tests_yield
Inputs used: the clean room's data and task description, and the public links in it (plus a search for the MLCAS 2021 challenge). No other local files were opened. The panel folder also holds the other agents' work folders, the register, the participant kit and logs. I saw their names in a directory listing and did not open any of them.
Scratch scripts: the run's work files (a.py to e.py)

VERDICT: Include with changes. This is a real, public, non-synthetic plant-breeding yield table, and the year-based split is the honest one. But the signal left under that split is small and noisy. The 1,498 daily weather columns are one per-environment vector repeated on every row of that environment. And 4.9k rows repeat the same genotype, location and year. These points should be fixed or documented before the scores are trusted.

WHAT THE TASK IS
Uniform Soybean Tests (USDA/university public variety trials, 2003-2015, 159 locations in 28 US states and Canadian provinces). This is the training set of the MLCAS 2021 yield challenge used in Shook et al., PLOS ONE 2021 (doi 10.1371/journal.pone.0252402).
- One row = one breeding line (genotype) grown in one trial at one location in one year.
- Target: yield in bu/acre (mean 50.7, sd 16.0, range 0.4-112.4).
- Features: maturity group, anonymised genotype ID, a pedigree cluster (20 k-means clusters), state, location, year, and 7 daily weather variables x 214 days.
- Paper: weather comes from "the nearest grid point from a gridded 30km product". The window is "214 days (crop growing season, defined April 1 through October 31)".
- Who uses it: breeders and trial programmes. They want to model genotype x environment yield response, rank lines in new seasons, and study weather sensitivity.
- Weather runs to October 31, so the prediction can only be made after the season ends. This is a hindcast or G x E modelling task, not an in-season forecast. That is a legitimate use, but it should be described that way.

CHECKS THAT PASSED
- 92,814 rows x 1,505 columns. No missing values. No exact duplicate rows.
- Weather is constant within each location-year: 1,117 environments, 1,040 distinct weather vectors. The 77 shared vectors are pairs of locations in the same year, which fits the 30 km grid.
- Units look like Fahrenheit and are plausible:
  - AvgSur mean is 50 F on day 1 (April 1) and peaks around day 110-125 (mid/late July).
  - Mid-summer means range from QUE 67 F to OK 85 F.
  - MinSur > MaxSur: 0 cells. ADNI > MDNI: 0 cells.
- Maturity group follows latitude: Canada and Minnesota are MG -1 (= MG 00) to 0, Georgia, Alabama and South Carolina are MG 7. Each location maps to exactly one state, and each genotype to exactly one cluster.
- The yield trend over years is plausible (yearly means rise from 43.8 in 2003 to 56.7 in 2015: genetic gain plus weather).
- No post-harvest traits are present (protein, oil, lodging, height). The itsMustafamr/Yield repo uses a different derived table that has them. Leaving them out here is correct.

CONCERNS, MOST TO LEAST SERIOUS

1. Under the honest split there is little signal, and the scores rest on about 80 environments per window.
   Evidence:
   - Variance: the environment (location-year) mean alone explains R2 = 0.75 of yield variance. Within-environment variance is 62.8 vs 254.6 total.
   - In a new year that environment effect is hardly predictable from the given features. At environment level (1,117 rows, monthly weather + location + year, LightGBM), new-year RMSE is no better than the training mean in 2010 and 2012 and only somewhat better in 2014-2015:

     | test year | training-mean RMSE | LightGBM RMSE |
     |-----------|--------------------|---------------|
     | 2010      | 14.23              | 14.25         |
     | 2012      | 14.42              | 15.86         |
     | 2015      | 15.40              | 10.99         |

   - Row-level LightGBM with expanding windows, test years 2010-2015, mean RMSE:

     | baseline                       | mean RMSE                    |
     |--------------------------------|------------------------------|
     | training mean                  | 16.68                        |
     | weather only                   | 16.73 (no better than the mean) |
     | metadata only                  | 14.39                        |
     | all 1,504 features             | 14.46 (R2 0.16, 0.05-0.26 per window) |
     | metadata + monthly weather     | 14.07                        |
     | oracle using the true test-environment means | 7.68           |

   - Each test year has 6-7k rows but only 74-87 environments. Errors within an environment are strongly correlated, so the effective test size is about 80. Model rankings may be noise.
   - For comparison, the paper's R2 = 0.796 came from a random 80/10/10 row split, where every test environment also appears in training. Its weather vector acts as an environment ID there. So that number is not comparable, and a random split would be leaky.
   Change: keep the year split, and never use a random row split. Report uncertainty with environment-clustered or bootstrap intervals. Treat this as a hard, low-signal task. Make sure inner validation / HPO is also grouped by year or environment, not random.

2. Very wide and highly redundant: 1,498 daily weather columns. They hold only about 1,117 distinct environment vectors, repeated over 92k rows.
   Evidence:
   - Monthly means (49 columns) did as well as or better than daily (14.07 vs 14.46 RMSE).
   - The paper itself downsampled to weekly ("Tx = 30") for most analyses.
   - With about 1,500 columns the benchmark mostly tests how methods cope with width (feature caps on many models, memory, run time), not the agronomy.
   Change: provide weekly aggregates (7 x 30 = 210 columns), or declare the 7 x 214 block as a time-series special feature with a recommended aggregation.

3. Repeated genotype x location x year rows give label noise.
   Evidence:
   - 4,948 extra rows share genotype, location and year. Of these, 4,100 have identical features but different targets.
   - The absolute yield difference within a pair is mean 6.6, median 5.1, max 52.2 bu/acre. The implied noise sd is about 5.6.
   - These are most likely the same line entered in two trials (for example preliminary and uniform tests, and 213 genotypes appear with two maturity groups). The source tables would have a trial/test identifier, but it is missing here.
   - They fall within one year, so the year split has no train/test leak. They would leak in any random inner CV.
   Change: add the trial/test identifier if it is recoverable from the source, or document the repeats. Do not collapse them silently.

4. When the prediction is made, and what the split stands for.
   - The weather covers April 1 to October 31, after harvest, so this is not a forecast. It also ignores planting date (a fixed calendar window, not aligned to the crop).
   - The year feature is always outside the training range in the test windows (trend +13 bu/acre over 13 years). Trees cannot extrapolate it, so part of the score measures trend extrapolation.
   - About 50% of test rows have a genotype never seen in training (2010: 0.516 ... 2015: 0.472). Locations are 95-99% seen.
   Change: state the hindcast / G x E framing in the task description. These properties are acceptable but should be documented.

5. Provenance gaps.
   - The challenge training set is described as "93,028 training records". This table has 92,814: 214 rows missing, unexplained.
   - The 10,337 challenge test rows (targets hidden) are correctly absent.
   - The PURR DOI (10.4231/r7hd7spk) is "Uniform Soybean Tests Northern Region" (CC0). This table also contains the Southern Region (GA, AL, SC, MS, LA, ... MG 5-8), whose source and licence are not linked.
   - The licence of the challenge data itself is unclear.
   - The itsMustafamr/Yield link points to a different derived dataset and should not be cited as the source.
   Change: explain the 214 dropped rows, link the Southern UST reports, and confirm redistribution terms.

6. Minor oddities.
   - 154 rows of MG -1 (00) at two Arkansas locations (loc053, loc069) in 2003-2004. MG 00 lines in Arkansas are agronomically implausible, so this is possibly a location/state coding slip from the challenge. Check, or accept as source noise.
   - 45 yields below 5 bu/acre (probably crop failures; keep them).

PREPARATION
The column types are sensible:
- genotype, state, location and genotype_cluster are categorical.
- maturity_group is a numeric ordinal (-1 encodes 00), which is good.
- year is an integer.
- weather is float.
genotype has 5,838 levels (high cardinality, real and useful). There are no missing values and no encoding problems.

COULD NOT CHECK
- The exact definition of the 6 test windows. I assumed expanding windows with test years 2010-2015.
- The eval.ai challenge page (renders empty without JS) and the Google Drive data folder (not opened), so the raw challenge files, row order and the 214-row difference are not verified.
- Whether the repeated genotype-location-year rows are separate trials or replicates.
- The licence of the Southern region and of the challenge release.
- Whether genotype IDs are mapped the same way as in the paper's pedigree clustering.
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT: uniform_soybean_tests_yield (target yield_bu_acre, RMSE, 6 expanding-window temporal splits, test years 2010-2015)

VERDICT: Hard to game. The only working exploit is that a genotype's appearance in later years can be seen in data.parquet. Lines that come back the next year are the ones breeders advanced, which means they yielded well. It gains about 0.07-0.17 RMSE (about 1%) on the 5 splits that have later years, roughly 1-3x the seed and noise-column spread. Most of the error (75% of the yield variance) is the location-year effect, and nothing in the kit leaks it.

Scores (mean RMSE over the 6 splits; lower is better)
- Untuned LightGBM, all 1505 columns (100 trees): 13.920. With 500 trees: 13.940.
- Compact honest model C: meta columns + weekly weather means: 14.156.
- C + linear year-trend detrending: 13.143.
- C + trend + past-only history (H): 12.993 (3 seeds: 12.978, 13.024, 12.978).
    History = genotype mean of yield minus its trial mean, location means, all from training labels of earlier years only.
- H trained only on the last 5 years: 12.914 (3 seeds).
- Noise reference:
    - random column added to H: 13.093 (3 seeds), i.e. +0.10.
    - random column added to the full baseline: 13.904, i.e. -0.016.
    - seed spread of H: 0.05.
    - per-split swings from a noise column: up to 0.5. Each test year has only about 80 location-years, so single splits are noisy.

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Genotype's later-year presence: number of later years it appears in, advanced flag, gap to next year, total years and rows over the whole file | exp1.py (fut, gtot), exp_full.py fut, exp2.py | H 12.993; full baseline 13.920 | H+gtot 12.819; H+fut 12.927; full+fut+gtot 13.784 | H+gtot -0.174 (3 seeds; per split -0.83 to +0.40). Full -0.136 (r0 -0.37 ... r2 +0.89 ... r4 -0.28). Within-trial isolation (exp2): -0.073 vs honest adjustment (r0 -0.02, r1-r5 -0.05 to -0.12; noise column -0.02) | No. Whether a line is entered again next year is decided after this year's yield is seen. | Make rows after a split's test window invisible to that split: ship per-split data cut at the test year, or keep the genotype key only on rows up to the test year |

Mechanism (#1): every split's training and test rows share the same data.parquet, which holds all years 2003-2015. A genotype's rows in years after the test year are therefore visible, even though their labels are not used. Breeding programmes advance the lines that did well. In every year, rows of genotypes that reappear later sit +1.2 to +1.8 bu/acre above their trial mean, and the others sit -0.7 to -1.3 below (explore3.py). This reduces the within-trial variance from 62.6 to 61.1. It is worth nothing on r0 (test year 2015, nothing after it).

The legit counterpart does not help: the genotype's years and records up to and including the row's year (gpast) score 13.009 vs 12.993. So the gtot gain comes from the future part. The leak is small because within-trial variance is only about 25% of the total. The location-year mean dominates the error and no leak reaches it.

FLAWS THAT HURT AN HONEST MODEL
None clearly attributable to the task.
- Training only on the last 5 years scores 12.914 vs 12.993 (3 seeds; within 1-2x noise). Old years are legitimate training data, so this is a modelling choice, not a flaw.
- The large honest gain is detrending for genetic gain (yearly mean 43.8 in 2003, 56.7 in 2015): 14.156 -> 13.143. Trees cannot extrapolate the trend to an unseen later year. A deployed model can detrend too, so this is signal.

ATTACKS THAT FOUND NOTHING
- Row order: rows are sorted by year and shuffled within each year.
    - Correlation of row position with yield inside a year: 0.017 (2010) and 0.007 (2015).
    - Absolute yield difference to the next row: 17.4, vs 18.0 for a random pair.
- Identifiers:
    - Genotype number vs yield: r=0.078. Vs genotype mean yield: 0.12. Vs first year: 0.15. The ids look randomised or roughly alphabetical.
    - Location number vs location mean yield: r=0.013.
- Copies across the split: none possible.
    - Weather is constant within a location-year (1117 location-years, 1040 distinct weather vectors).
    - Shared weather vectors pair nearby locations in the same year only (77 pairs, never across years).
    - The 4100 exact duplicate feature rows (same genotype, location and year with a different yield; within-group SD 4.1) lie inside one year, so on one side of the split.
- Format artefacts:
    - Yield always has 1 decimal and its last digit is uniform.
    - Weather: 2 decimals for ADNI/ARH/AvgSur/AP, 1 for Max/MinSur, integer MDNI.
    - Per-location-year format features (whole share, decimal share, distinct count, zero share, runs) correlate with the location-year yield residual at |r| <= 0.13. The top one is AP_runs, i.e. dry spells, which is real weather.
- Test-set composition (location-year size, distinct genotypes, mean and number of maturity groups, records per MG):
    - r=0.149 with the location-year residual after the year mean, but 0.004 once the location effect is removed (explore5.py).
    - As features: H+comp 13.096 vs 12.993 (worse; 3 seeds).
- Survivorship: share of a (year, MG) test's entries recorded at a location: r=0.07 with the trial residual. Share of locations at which a genotype has a record: r=0.05 within trial. Not exploitable.
- Same-year genotype entry counts (number of locations this year, records per location-year): legit at entry and about 0 gain (12.966 vs 12.978 for seed 0; exp2 -0.010).
- Transforms over all rows: none; the weather is in raw units.
- Columns from after the prediction point: none. Season weather is allowed by the task. No harvest-date or other outcome-time column.
- Lookup or shallow formula: none. The location-year mean explains 75% of the variance but is unknown for test years.
- Public "leak" or "magic feature" threads: none found.
    - Published work (PLOS ONE 2021 Shook et al.; arXiv 2309.13021) uses random 80/10/10 splits, where location-year effects are shared. Hence RMSE about 6.7 there vs about 12-13 here; that is not applicable to this temporal split.
    - Source notes: records without yield (not planted, or died) were removed upstream. Weather comes from a 30 km grid per location-year.
- Row lookup in the published file: would work. The kit rows are the MLCAS2021 training records, which were released with yields. I did not download the file (it is on Google Drive). Not a task flaw; not ranked.

KIT VS PUBLISHED: published training set 93,028 records; kit 92,814 (214 fewer, reason unknown). Columns match the description: MG, genotype, state, year, location, 20 pedigree clusters, 7 weather variables x 214 days.

COULD NOT CHECK
- The exact rows dropped by the preparation (published file not downloaded).
- Whether the MLCAS hidden test labels exist anywhere.
- Run cost: no subsampling. Exploit sweeps used the compact model (231 columns); #1 was confirmed on the full 1505-column baseline.

Scripts, logs and scores: the run's work files.
Sources: https://ar5iv.labs.arxiv.org/html/2309.13021 ; https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0252402 ; https://github.com/tryambakganguly/Yield-Prediction-Temporal-Attention
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER: uniform_soybean_tests_yield (panel of 2026-11-08, written 2026-11-09)

Read: principles.md; provenance.md (PROV-8/9/13 and Cases), splits.md (SPLIT-1..5, 14, 15, 19 and Cases),
task_probes.md (TP-1/2 and Cases), use_case.md (USE-1/3/8/9 and Cases), leak_checks.md (LEAK-10/29/30 and the
Mechanisms table), metrics.md (MET-1/2/4/5/10/11 and Cases), review_file_format.md (all from the branch's worktree);
the batch's BUILDER_BRIEF.md; dataset.py, the record, builder_report.md, claims.md; the column auditor, domain
practitioner, claim auditor and split auditor reports; register.json (5,423 decisions, 34 flags: none names this
dataset; the scaling-over-all-rows drift and the USE-8 pairs were read and do not bear on it). Sibling of this
batch read: genomic_prediction_soy_yield (definition, mediator and precedent checker reports). Also read for
precedent: the download notes of pricing_game_2017_french_mtpl, ai4d_lab_tanzania_tourism_classification_challenge,
diabetes_3, jm1, aps_failure, qsar_biodeg, ugr16_isp_netflow_intrusion; the use cases of ashrae_great_energy_
predictor_iii_1m, forest_fires, 2024_lusaka_mobility_prediction_hackathon; src/data_foundry/v2/splits.py
(min_train_fraction) and metrics.py (mean_group_pearsonr).
No curator decision exists on this dataset beyond the CC of 2026-11-08 (accepted for adding).

SUMMARY (per decision)
  D1 Files from a course participant's CyVerse copy (PROV-8, PROV-13) ........ consistent, once the notes carry the
                                                                                claim auditor's match against the
                                                                                authors' own files (now they give
                                                                                dates and shapes only)
  D2 Held-out seasons over the source's random split (SPLIT-1/5/19) ......... consistent
  D3 no_signal flag kept, little signal beyond location means (TP-2) ........ consistent
  D4 Season weather (known at harvest) as features (USE-8, LEAK-10) ......... consistent at the written prediction
                                                                                point; depends on D7
  D5 RMSE (challenge) vs mean_group_pearsonr by location-year (MET-4/10/11) . keeping RMSE follows MET-4, but a real
                                                                                pair went the other way (protein,
                                                                                huesken) and the batch sibling
                                                                                genomic_prediction_soy_yield is open
                                                                                on the same question: PROMPT 2
  D6 Pedigree clusters fit on all lines, kept with a note (LEAK-30 weak) .... consistent
  D7 Use case inferred, written as a post-season comparison (USE-1, USE-9) .. departs without a fact that holds:
                                                                                the split follows the paper's stated
                                                                                aim, the use case text does not:
                                                                                PROMPT 1
  Note N1: window count 6 (SPLIT-15) rests on a share of seasons, SPLIT-14 counts rows; minor, no prompt.
  Note N2: in-batch pair ugr16_isp_netflow_intrusion also reads a personal mirror, on different facts.

------------------------------------------------------------------------------------------------------------------
D1. THIRD-PARTY COPY BECAUSE THE PUBLISHER'S LINKS ARE DEAD (PROV-8 Must, PROV-13 Must; builder issue 1)
------------------------------------------------------------------------------------------------------------------
Facts: the challenge zip (Drive 1DoyextA...) answers 404 to everyone and the paper's Drive folder lists no files
(builder, claim auditor). The copy: data.cyverse.org/.../evanmc/Dataset_Competition_Zip_File.zip, uploaded
2021-10-23 by a University of Arizona INFO 529 participant, fetched by that course's public Makefile, sha256 pinned.
The claim auditor then measured it against the authors' own public files (GitHub data_subset): clusterID_genotype
byte-equal to k_means_clusters_20.npy; the 103,365 genotype ids the same multiset as genotype_id_all_data.npy, the
(genotype, state) pairs too; of the authors' 2,000-row subset, 1,870 rows match a training record on yield, year,
location and MG with identical 214-day weather (max abs diff 0.0) and the other 130 have their key in the test inputs.

Precedents where the original was gone or unreachable, and what each rested on:
  - pricing_game_2017_french_mtpl (definition of 2026-11-01, reviewed by Lennart 2026-11-08): toolbox.zip 404 and not
    in the Wayback Machine; taken from CASdatasets at a pinned commit with sha256, a package by the game's organiser
    (Charpentier). The download notes say what it copies.
  - ai4d_lab_tanzania_tourism_classification_challenge (Myunghwan, October 2026): a student's GitHub commit
    (dylannguyen2809/ai4d) with sha256, accepted because it matched the curator-provided official Zindi archive byte
    for byte.
  - genomic_prediction_soy_yield (this batch): SoyBase offline since 2022; the CRAN package by the project's members.
  - diabetes_3, aps_failure, qsar_biodeg, rain_in_australia: Wayback captures of the original URL; jm1: OpenML's file
    byte-identical to PROMISE's.
  Every accepted copy is tied to the original by something checkable: the original bytes (Wayback, byte match), or a
  copy by the data owners.

Comparison: the CyVerse share is neither the original bytes nor the owners' copy, so on the builder's evidence alone
(entry dates before the challenge opened, shapes as the challenge page) it would be weaker than every precedent. The
claim auditor's match closes that: the copy agrees with the authors' own released files record for record, which is
the ai4d_lab pattern (a personal copy accepted on a match with an official piece), with a measurement (EV-2) where
ai4d had a full byte match. The batch brief's bar ("no mirrors of doubtful origin") sits under "Access you cannot get:
... a server that refuses this machine. Do not work around it"; it is about working around access. Here the
original is gone for everyone and the copy's origin is measured, so it is not a mirror of doubtful origin.
PROV-8 holds as written: source and year are the paper (2021), the download instructions name the copy and what it
copies. PROV-13: the damage (AvgSur_d213 filled by the authors, 214 double-converted rows) cannot be repaired from
the origin (the Weather.com grid is not public, line and location ids are anonymized): keep with a note, as the
tension row "repair against cleaning around damage" says ("when the origin cannot be reached, keep with a note").

Verdict: consistent, on one condition that is wording only: the download_description and the Source bullet should
state the match with the authors' files (the three facts above, with the GitHub path), not only dates and shapes.
Builder issue 1 can be settled as (a) ship from the copy; (b) asking the authors for a stable deposit stays optional.
The personal host may vanish (a reproducibility risk, not provenance); ai4d_lab and pricing_game pin the same kind.

------------------------------------------------------------------------------------------------------------------
D2. HELD-OUT SEASONS OVER THE SOURCE'S RANDOM SPLIT (SPLIT-1 Must, SPLIT-5 Must, SPLIT-19 Should; builder issue 3)
------------------------------------------------------------------------------------------------------------------
Precedents followed:
  - SPLIT-5 cases: kick, appliances_energy_prediction (a prescribed split is a claim to check).
  - SPLIT-1/SPLIT-4: superconductivity (2026-10-06), airfoil_self_noise (Lennart 2026-10-20): the regime from what
    the deployed model is asked, whatever the gap.
  - huesken_sirna_efficacy (Lennart 2026-11-04): the source's random flags replaced by gene-held-out folds.
  - genomic_prediction_soy_yield (this batch, panel 2026-11-09): grouped by family over Azodi's random lines.
  - bank_marketing (Lennart 2026-11-08, issue 1): time windows in place of an IID keep; "a weak score under the right
    split keeps no wrong one (forest_fires)".
  - principles.md tension "the right split against the score" (P4 over P6; forest_fires).
Comparison: the paper's aim is "unseen and new environments"; under the random split every test location-year and
line is in training (claim auditor: 0.0% unseen) and the weather becomes an environment code (6.68 with weather vs 6.71
with a location-year id; split auditor: the model ranking flips, 7.13 vs 14.31). The departure from SPLIT-19 (Should)
has its fact and serves SPLIT-1/SPLIT-5 (Musts of P4): reasonable, and the precedents record such replacements as
"applied", not as exceptions. Grouped by location-year rejected under SPLIT-3 (one regime): consistent with the
Lennart 2026-10-12 row "temporal against grouped". No drift: Lennart's three split calls of 2026-11-04 to 2026-11-08
all put the use case over the source's random split.
Verdict: consistent. The only tension is the use case text, which describes a moment the split does not mirror
(claim auditor U1, split auditor finding 1): that is D7, not a split question.

------------------------------------------------------------------------------------------------------------------
D3. LITTLE SIGNAL BEYOND LOCATION MEANS, no_signal KEPT (TP-1 Must, TP-2 Should; builder issue 2)
------------------------------------------------------------------------------------------------------------------
Precedents: forest_fires (kept 2026-10-06, R^2 0.013, TabPFN-3.5 beats the mean on 26 of 32 folds); noaa_storm_
events_damage (no_signal, drift_baseline, unstable kept, Lennart 2026-11-08, after a tuned check); clock_protein_
toxicity and asp_potassco_classification (TP-1: a stronger model resolved the flag); bank_marketing (2026-11-08).
Comparison: the signal here is larger than in forest_fires and comes from simple, honest models on the shipped
windows: dummy 16.68; location mean 13.71; location mean + trend 13.17; + line history 13.04 (claim auditor);
LightGBM without weather 13.60 (split auditor). No tuned or foundation model was run (TP-1 asks to check flags against
tuned methods before acting), but no action is taken on the flag, and the simple baselines already answer it.
Verdict: consistent (keep). Wording, not precedent: the Note bullet should scope "adds nothing" to "beyond each
location's mean and the yield trend" (claim auditor N1; the weather helps a direct LightGBM, 14.55 to 14.19).

------------------------------------------------------------------------------------------------------------------
D4. THE SEASON'S WEATHER, KNOWN ONLY AT HARVEST, AS FEATURES (USE-3/USE-8 Must, LEAK-10 Must)
------------------------------------------------------------------------------------------------------------------
Precedents:
  - ashrae_great_energy_predictor_iii_1m: the observed weather of each hour as input, at an ex-post prediction point
    (measuring retrofit savings, fit on earlier readings), fit direct.
  - kickstarter (USE-1/USE-3): the written prediction point decides which columns leak.
  - 2024_lusaka_mobility_prediction_hackathon (Myunghwan, 2026-10-29): earlier-hour weather used as a stand-in, fit
    approximate; no definition keeps later observed weather as a "perfect forecast" at a forward prediction point.
  - USE-8's list: "one snapshot standing in for a forecast" (account_debt_south_africa) is approximate.
Comparison: at the written prediction point (after the season) the weather exists, so LEAK-10 holds, and the fit is
approximate with the gap named; that follows ashrae's shape and is more cautious. At planting, all 1,498 columns would
be LEAK-10 (column auditor), and no precedent keeps realised future weather as a forecast stand-in, so a forward use
case must make the weather the query's given condition (a scenario, as airfoil's setup or superconductivity's
composition are given), not a forecast. Verdict: consistent as written; the wording it needs depends on D7.

------------------------------------------------------------------------------------------------------------------
D5. METRIC: RMSE (MLCAS2021) vs mean_group_pearsonr BY LOCATION-YEAR (MET-1/2 Must, MET-4 Should, MET-10, MET-11)
------------------------------------------------------------------------------------------------------------------
Precedents:
  - MET-4 keeps: zillow_prize, rossmann_store_sales, g_research, numerai (sponsored competitions).
  - MET-4 as amended 2026-11-05 (Lennart, loan_default_prediction_imperial_college): a competition of lesser standing
    (old, community- or research-run) may give way to the metric the task makes obvious when the measurements favour
    it, case by case. MLCAS2021 was run by a research community (a workshop challenge by the paper's authors): this
    clause applies.
  - protein_model_quality_rf_pcp and huesken_sirna_efficacy (Lennart 2026-11-04, MET-5 exceptions 1 and 2):
    context `mean_group_pearsonr` because a pooled score rewarded the group's mean (each protein's true mean beat
    LightGBM; a gene's mean cut RMSE 0.1582 to 0.1378). Both replaced a fallback, not a source metric.
  - superconductivity (Lennart 2026-11-08): a paper's deliberate RMSE overruled on the unit (MET-17), another reason.
  - genomic_prediction_soy_yield (this batch, open, issue 1): pooled r (Azodi) vs mean_group_pearsonr on family, same
    actor (a soybean breeder); its mediator settled MET-2's third bullet by measurement: Kendall tau 0.91 between the
    model order under pooled r and under within-family r on the shipped folds, so no Must forces the switch there.
Comparison:
  - Same mechanism as protein/huesken, stronger: 75.3% of the variance lies between location-years, the oracle
    environment mean takes RMSE from about 14 to 7.3-8.2, and oracle level + line effect improves it by only 0.0-0.3
    (domain practitioner), so RMSE ranks models mostly by a level the features do not predict.
  - MET-2 third bullet: the challenge scored RMSE on a random split where the level was known (location-year mean
    8.06), so it scored mostly within-environment deviations; our split changed what it measures. That is the evidence
    MET-4 asks for, but the measurement genomic used (rank agreement of models under both metrics on the shipped
    windows) has not been run here. Without it, the switch rests on variance shares, not on the ranking the benchmark
    reads.
  - Different from protein/huesken: here the original is a competition's leaderboard metric (MET-4), there a fallback.
    Different from genomic: there a paper's deliberate r (MET-5) and a between-family part the markers predict; here a
    level no feature predicts (weather adds nothing beyond location and trend).
  - MET-1's unit hangs on D7: the use case as written compares absolute yields after the season (RMSE fits it); the
    practitioner's breeder ranks entries within a test (a within-environment score fits). The release has no test id,
    so a location-year pools 2-4 maturity-group tests; location-year x maturity_group is the tighter proxy.
  - Counting: a switch here or in genomic is the third case of the protein/huesken reason, so the amendment is due
    with it (principles.md, the third exception), and it would be the first time the reason overrides a competition's
    metric. The two soy datasets should get the same answer unless the facts above are written down as what sets them
    apart.
Verdict: keeping RMSE is consistent with MET-4; switching is defensible under the amended MET-4 but not yet measured.
A real pair decided the other way exists, and a sibling is open on the same question: PROMPT 2.

------------------------------------------------------------------------------------------------------------------
D6. PEDIGREE CLUSTERS FIT ON ALL 5,839 LINES, KEPT WITH A NOTE (LEAK-30 Should when weak)
------------------------------------------------------------------------------------------------------------------
Precedents: LEAK-30 keeps with a note, Lennart 2026-10-19 (bioresponse, taiwanese_bankruptcy_prediction, cooking_time,
lung_cancer_epithelial_genexp: the source's transform over all rows, no raw values); numerai28_6 (quantile bins fit on
a larger population). Set apart: sf_permit_time and home_credit_default_risk (LEAK-29, 2026-10-19: our own all-row
computation, fixed) and genomic_prediction_soy_yield D3/C1 (our own environment fit, fixed in this batch).
Comparison: the clustering is the authors' (kmeans_clustering.py, KMeans(20) on USTrelmatrix_GenoID.csv, no yields),
and the 5,839 x 5,839 matrix is in neither the release nor the GitHub subset, so no rebuild is possible (LEAK-30:
"rebuild from the unprocessed values when the source has them"). Parentage is known when a line is entered; the
measured effect is negligible (claim auditor: 13.079 vs 13.115 on new lines). Verdict: consistent.

------------------------------------------------------------------------------------------------------------------
D7. THE USE CASE: INFERRED, WRITTEN AS A POST-SEASON COMPARISON (USE-1 Must, USE-9 Should and its factor)
------------------------------------------------------------------------------------------------------------------
Facts: neither paper nor challenge names an actor's decision. The paper states an aim, "predict performance (for
example, seed yield) in unseen and new environments" (Introduction), with climate scenarios and "crop insurance
recommendations ... based on weather forecasts before planting" (Discussion, quoted by the split auditor), and calls
itself "a retrospective design" (quoted by the domain practitioner). The definition writes: "A soybean breeder, after
a season, sets the yields each line ... should have given under that season's weather beside what it gave".
Three panel agents independently (claim auditor U1, split auditor finding 1, domain practitioner B): at that moment
every yield of the season is known, the other lines at the same location-year included, which is what the random
split hands a model; so the use case as written argues for the split the definition rejects (USE-1: every split
choice is checked against the use case). The practitioner adds that after harvest a breeder compares a line with the
checks grown beside it, not with a weather model.
Precedents:
  - forest_fires: the use case is the paper's stated use. ashrae: an ex-post use case with observed weather, direct,
    because measuring retrofit savings with a weather-driven baseline fit on earlier readings is the established
    practice the competition names. The builder's use case has ashrae's shape but not its fact: no source or practice
    names a post-season weather-expectation comparison for breeders.
  - nba_players_2016_2019 (Lennart 2026-10-26, `No`): "the prediction point moved twice to fit the data". USE-9's
    weighed factor "a use case rephrased only to excuse a gap". This case is far milder (one move, the fit stays
    approximate, the task is real), but the post-season moment was chosen to admit the weather.
  - chicago_traffic_crashes (Lennart 2026-11-05, USE-9): the actor replaced so the data mirror it honestly.
Verdict: departs from the pattern (the use case is the source's stated aim or an established practice) without a
fact that holds, and the text contradicts the split. Mildest remedy on the ladder: reword (fix the definition), split
and fit unchanged. PROMPT 1.

------------------------------------------------------------------------------------------------------------------
NOTES (no prompt)
------------------------------------------------------------------------------------------------------------------
N1 (SPLIT-15 Should, SPLIT-14 Must). splits_comment gives the reason for 6 windows as "training keeps at least half of
   the 13 seasons"; the library's min_train_fraction counts distinct time values for unit="unique"
   (src/data_foundry/v2/splits.py, docstring of the window builder), while SPLIT-14's floor is "50% of the data". The
   2009 window trains on 50.7% of the rows (split auditor), so SPLIT-15's "as many windows as folds" would allow a
   seventh. college_scorecard, kick and melbourne_housing_market use the same min_train_fraction with unit="unique";
   whether their counts differ by rows was not checked. Remedy: reword the comment by rows, or add the 2009 window
   with explicit cutoffs. A library-level point for the curator if it recurs.
N2 (in-batch pair, PROV-8). ugr16_isp_netflow_intrusion reads the Hugging Face mirror mehedi107/ugr-16 because the
   official site answers 403 to this machine; its archives are checked against the mirror's own manifest only. That
   is the situation the brief's bar names (a server that refuses this machine), unlike this dataset (original gone
   for everyone; copy matched against the authors' own files). If the curator accepts one, the record should say
   which fact sets the other apart, so the two are not read as one precedent.
N3 Wording carried by other reports and not repeated here: claim 38 "4 of 6" is 5 of 6 (claim auditor N2); "the
   line's maturity group" is the test's (column auditor F2, claim auditor N4); AvgSur_d213 outside [Min, Max] in
   14.9% of rows (column auditor F1, CLEAN-11, no precedent conflict found).

==================================================================================================================
PROMPTS FOR THE CURATOR (issue shape of review_file_format.md, turns)
==================================================================================================================

PROMPT 1 (D7)

**Consistency check (AI, 2026-11-09):** What sets this dataset's post-season use case apart from the paper's stated aim, which the split already follows?

- **Problem:**
  - The use case puts the breeder after the season, when every yield of that season is known, so it argues for the source's random split that the definition rejects.
  - Neither source names a post-season weather comparison: the paper's aim is yield "in unseen and new environments", and forest_fires and ashrae took the source's stated use or an established practice.
  - Three panel agents found the same gap without seeing each other's work.
- **Background:** The split, the fit (approximate) and the features stay as they are under (a) and (b); only the use case sentence and the prediction-point bullet change.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep the post-season use case (implemented) | Records as its reason that the paper calls itself "a retrospective design" and the challenge asks about a variety's "plasticity", a response to weather read after the season | No edit; the weather is known at the moment, so no leak question | No source names this decision; breeders compare with the checks grown beside a line; the moment still argues for the random split |
| b | Reword to the paper's aim | A breeder or test coordinator predicts each entry's yield at the locations of a season the model has not seen, from the line, the site and that season's weather taken as given (a scenario, or the observed season before its trial results are compiled), fit on earlier seasons | Matches the split and the source's own words; follows forest_fires and chicago_traffic_crashes | The weather stands in for what a real decision would have only as a forecast, so the fit stays approximate and the notes must say the weather is a given condition, not a planting-time forecast |
| c | Planting-time decision, weather dropped | Moves the prediction point to before the season and drops the 1,498 weather columns | No stand-in at all | Drops the source's main inputs; a task of our own; little score lost (13.04-13.17 without weather) but much of the source's design gone |

- **Recommendation:** (b): the split already follows the paper's aim, and the reworded use case removes the contradiction at no cost to the data.[^use1][^use9][^leak10][^prec]
- **Decision:** keep the post-season framing with its stated reason, reword to the paper's aim, or move to planting?

[^use1]: USE-1 (Must): a use case is an actor, a moment and a decision; every column, filter, target and split choice is checked against it.
[^use9]: USE-9 (Should; narrows USE-8), with the weighed factor "a use case rephrased only to excuse a gap" (use_case.md).
[^leak10]: LEAK-10 (Must) and USE-3: a value that did not exist at the prediction point is a leak.
[^prec]: forest_fires (the paper's stated use); ashrae_great_energy_predictor_iii_1m (ex-post retrofit savings with observed weather, direct); nba_players_2016_2019 (Lennart, 2026-10-26: "the prediction point moved twice to fit the data"); chicago_traffic_crashes (Lennart, 2026-11-05, USE-9: actor replaced).

PROMPT 2 (D5)

**Consistency check (AI, 2026-11-09):** Keep the challenge's RMSE, or score within each location-year as protein and huesken do, and decide it together with genomic_prediction_soy_yield?

- **Problem:**
  - On held-out seasons 75% of the yield variance lies between location-years, and knowing each environment's level cuts RMSE from about 14 to 7.3-8.2, while the line effect a breeder acts on moves it by 0.0-0.3.
  - Protein and huesken (2026-11-04) moved to a within-group correlation when a pooled score rewarded group means, and the batch sibling genomic_prediction_soy_yield is open on the same question for the same actor.
  - The model ranking under both metrics on the shipped windows has not been measured here, unlike for the sibling (Kendall tau 0.91 there).
- **Background:** MLCAS2021 was a research-run challenge, so its RMSE may give way to an obvious metric when measurements favour it; it was scored on a random split where every test environment was in training, so its meaning changed with our split.
- **Consistency:** A switch in either soy dataset is the third case of the protein/huesken reason, so a rule amendment is due with it, and the first time that reason overrides a competition's metric.

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Keep RMSE (implemented) | Keeps the challenge's metric and adds to the notes and fit text that on held-out seasons it mostly scores the new environment's level | The source's metric; fits the use case as written (absolute yields); no new scoring column | Ranks models mostly by a level no feature predicts; the sibling may go the other way without a written reason |
| b | mean_group_pearsonr by location-year | Declares the within-environment correlation from context, RMSE named as the overruled original; location-year ships as a scoring column | Scores the ranking a breeder acts on; follows protein and huesken | Overrules a competition's metric on variance shares alone; a location-year pools 2-4 maturity-group tests, so part of the score is ranking tests, not lines; amendment due |
| c | Measure first, then decide both soy datasets | Ranks about ten models under both metrics on the 6 shipped windows (Kendall tau), as the sibling's mediator did, then applies (a) if the orders agree and (b) if they do not, with the same answer for genomic unless a written fact separates them | Facts first; one answer for one actor | One more panel run before the decision |

- **Recommendation:** (c), and settle the use case (Prompt 1) first, since the unit the metric scores follows it.[^met1][^met2][^met4][^met11][^met5x][^amend][^sib]
- **Decision:** keep RMSE, switch to the within-location-year correlation, or measure first and decide both soy datasets together?

[^met4]: MET-4 (Should), amended 2026-11-05 (Lennart, loan_default_prediction_imperial_college): a competition of lesser standing may give way to the metric the task makes obvious when the measurements favour it, case by case.
[^met2]: MET-2 (Must), third bullet: a task we changed keeps the source's metric only when its meaning survives the change.
[^met1]: MET-1 (Must): the declared metric scores the decision of the use case at the unit the actor acts on.
[^met11]: MET-11 (Must) `context`, amended 2026-11-03: also covers a source metric overruled under MET-2 or MET-4; the reason names the original.
[^met5x]: metrics.md Cases: protein_model_quality_rf_pcp and huesken_sirna_efficacy (Lennart, 2026-11-04), exceptions to MET-5, the second "the second exception of this kind".
[^amend]: principles.md, "Exceptions and amendments": when the same reason has produced three exceptions, the next pass proposes an amendment.
[^sib]: genomic_prediction_soy_yield, panel of 2026-11-09, mediator issue 1 (pooled r vs within-family r; tau 0.91 on the shipped folds).

FILES: the definition, the record, the precedent definitions, the rules and the sibling's panel reports (the run's work files).
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE, OPENING BRIEF: uniform_soybean_tests_yield (2026-11-09)
Read: dataset.py, README.md, principles.md, builder_report.md, the seven phase-A reports.
Position: ship as defined, with wording fixes and one cheap cleaning fix (point 7). The use-case reword (point 5)
is the one change that touches a curator prompt; it changes text only, not the data, split, features or metric.

1. The split is right, and every agent who tested it agrees (P4; SPLIT-1 Must, SPLIT-5 Must; SPLIT-19 Should departed
   with its fact).
   Evidence: the paper's aim is to "predict performance (for example, seed yield) in unseen and new environments".
   Under the source's random split, every test location-year and line is in training (claim auditor: 0.0% unseen).
   The weather then only names the environment: 6.68 with the weather vs 6.71 with a location-year id. The model
   ranking flips: LightGBM with weather scores 7.13 on random records and 14.31 on held-out seasons (split auditor).
   Grouped by location-year leaks later seasons and the same season's other sites (12.35-12.52).
   The split auditor ("right with notes"), domain practitioner (E), blind reviewer ("never use a random row split")
   and precedent checker (D2 consistent: huesken, genomic_prediction_soy_yield, bank_marketing) all keep seasons.
   Why it holds: SPLIT-5's Musts outrank SPLIT-19 (Should). The tension "right split against the score" (P4 over
   P6, forest_fires) settles builder issue 3 as (a).

2. The data is what it claims to be (P5; PROV-8 Must, PROV-13 Must).
   Evidence: the claim auditor matched the CyVerse copy against the authors' own GitHub files:
   - clusterID_genotype.npy is byte-equal to k_means_clusters_20.npy;
   - the 103,365 genotype ids and the (genotype, state) pairs are the same multisets as the authors';
   - 1,870 of the authors' 2,000 subset rows match a training record, with identical 214-day weather (max diff 0.0);
     the other 130 are in the test inputs.
   The sha256 is pinned. The publisher's links are dead for everyone, not refused to this machine.
   Precedents: ai4d_lab (a personal copy matched against an official piece) and pricing_game_2017 (the original is
   404). The precedent checker found D1 consistent.
   Remedy: wording only. Put the three match facts into download_description and the Source bullet. Builder issue 1
   becomes (a); asking the authors stays optional (a reproducibility risk, not a provenance one).

3. No leak in the data; the one exploit found is an evaluation-level leak (P4; LEAK-10 Must holds; LEAK-30 Should,
   weak; LEAK-9 Should).
   - The environment never crosses a window: hidden_groups (all but genotype) 0.0%, cross-split copies 0.0%.
   - The 214 dropped copies and the 7,586 kept same-feature rows all lie within one year.
   - The pedigree clusters (the authors', no yields; the matrix is not public, so no rebuild) are measured as
     negligible: 13.079 vs 13.115 on new lines. Kept with a note (LEAK-30; precedents of 2026-10-19).
   - Task gamer: "hard to game". Its one exploit reads whether a genotype reappears after the test year, from rows
     outside that window's train and test indices. It gains 0.07-0.17 RMSE (about 1%), and nothing on the 2015 window.
   Why it is not a data defect: LEAK-9 (amended 2026-11-05) treats a method that reads other rows beyond its fold as
   an evaluation leak. The fix is a protocol line and calling such a method out, not changing the data
   (bank_marketing, fremtpl2). The gamer's fix (ship per-split cut data) is a larger remedy than the ladder needs.
   Remedy: one protocol sentence in the notes.

4. The signal under the honest split is small but real (P6; TP-2 Should; TP-1 Must holds).
   Simple, honest models clearly beat the training mean of 16.68:
     location mean                          13.71
     location mean + trend                  13.17
     + line history                         13.04 (claim auditor)
     LightGBM without weather               13.60 (split auditor)
     task gamer's honest H                  12.99 (seed spread 0.05)
   The no_signal flag comes from untuned models on 1,504 columns. The domain practitioner calls the weak signal
   "realistic, not useless".
   Precedents: forest_fires (R^2 0.013, kept) and noaa_storm_events_damage (no_signal, drift_baseline and unstable
   kept). The precedent checker found D3 consistent.
   The blind reviewer's "about 80 environments per window" is a fact for the notes. It breaks no TP rule: 6 windows,
   5,730-6,939 records and 74-87 environments each.
   Remedy (claim auditor N1): scope the Note bullet to "beyond each location's mean and the yield trend". The weather
   does help a direct LightGBM (14.55 to 14.19). Builder issue 2 becomes (a).

5. The use case: I concede the gap; the fix is a text change (P3; USE-1 Must, USE-9 Should with its weighed factor).
   Three agents (claim auditor U1, split auditor 1, practitioner B) found the same thing independently. The
   post-season moment would hand the model the season's other yields, so as written it argues for the random split.
   Concede that, but it is not grounds to hold the dataset.
   The remedy ladder's "fix the definition" step covers it: reword use_case and the prediction-point bullet to the
   paper's own aim (precedent checker PROMPT 1, option b). A breeder or test coordinator predicts each entry's yield
   at the sites of a season the model has not seen, with that season's weather as a given condition, fit on earlier
   seasons.
   Split, features and fit ("approximate") stay. The weather is then the query's given condition, not a planting-time
   forecast (airfoil, superconductivity), so LEAK-10 holds. The column auditor measured that the weather costs little
   either way (13.15 without vs 13.92 with).

6. Keep RMSE, the challenge's metric (P6; MET-4 Should, amended 2026-11-05; MET-2 Must third bullet).
   - Quote: "We will use Root Mean Square Error (RMSE) as the evaluation metric" (EvalAI 1251).
   - After point 5's reword the predicted quantity is absolute seed yield in new environments. The paper names
     insurers and marketing decisions among its users, and RMSE scores that at the record level (MET-1).
   - The case for a switch to mean_group_pearsonr by location-year rests on variance shares. The measurement MET-4's
     amendment asks for (the model order under both metrics, as the sibling's Kendall tau of 0.91) was not run here.
   - With no test id, a location-year pools 2-4 maturity-group tests, so a within-location-year r partly ranks tests,
     not lines (precedent checker D5).
   The domain practitioner calls keeping RMSE "defensible under MET-4".
   Remedy: add one sentence to the notes and fit_reason: on held-out seasons RMSE mostly scores the new
   environment's level. If the curator wants the soy pair decided together, PROMPT 2 (c) is a measurement, not a
   blocker.

7. The quality findings are P7 and cheap, so they do not hold the dataset (principles step 3; CLEAN-11 Should,
   CLEAN-14 Should).
   Fixes:
   - AvgSur_d213 lies outside the day's [Min, Max] in 13,843 rows (14.9%; column auditor F1). Set those cells to
     missing (the rule's own remedy), or count them in the Anomaly bullet.
   - Wording: claim 38 should read "5 of 6", not "4 of 6"; "the maturity group of the test", not "the line's"; 159
     location ids vs the paper's 150; MG kept numeric, with the reason written down (F2).
   - SPLIT-15: 6 windows. Either explain the count by rows (the 2009 window would train on 50.7%) or add 2009.
   The blind reviewer's other concerns are answered in the evidence:
   - The 214 "missing" rows are the exact copies dropped (claim 17).
   - The AR MG -1 records are real (claim auditor 25, column auditor).
   - The licence is the challenge's terms, quoted verbatim (claim 11).
   - Width is no reason to drop features: the tension "width against model limits" (coad), CLEAN-19 and CLEAN-22.
   - The same-feature rows are documented, and every one lies within a year.

Judgment record
Verdict: ship after changes (wording, one protocol line, one optional cell fix).
Validity: SEL holds; USE-1 met after the reword (point 5); LEAK-10 holds; LEAK-30 weak, kept; LEAK-9 protocol line;
  SPLIT-1/5 hold; PROV-8/13 hold, with the match written down.
Value: TP-2, a small real signal (keep); MET-4 keeps RMSE, with a note.
Quality: CLEAN-11 (d213) fixed or noted; CLEAN-14 MG numeric, with the reason.
For the curator: PROMPT 1 (I back b); PROMPT 2 (I back a, and accept c as a measurement that does not block).
```

</details>

<details><summary>Advocate rebuttal</summary>

```text
ADVOCATE REBUTTAL: uniform_soybean_tests_yield (2026-11-09)
The critic and I agree on the verdict (ship after changes), on the split, on provenance, and on having no leak to fix.
We disagree on one thing: whether the metric question blocks shipping (point 2).

1. Use case (USE-1, USE-3). Concede. This is my point 5: the same reword to the paper's aim, with split and features
   unchanged. I accept the critic's ordered fit_reason (USE-8) with one change. Write "absolute yield, where a
   breeder ranking entries acts on yield relative to the checks" as a gap for that actor. Do not write it as the
   task's actor. The paper's aim and its named users (insurers, marketing decisions) predict absolute yield. Which
   actor is primary is the PROMPT 1 call, and it sets point 2.

2. Metric (MET-1, MET-2, MET-4). Partly concede.
   I accept the critic's remedy: measure the model order under both metrics (precedent checker option c), and decide
   together with genomic_prediction_soy_yield. I also accept the fit_reason and Metric-bullet sentence if RMSE stays.
   I dispute three things:
   (a) That MET-2's third bullet fails.
       - Under both splits, RMSE scores the same quantity: each record's yield error in bu/acre.
       - The split changed which part of that error is hard, not what the metric means.
       - Predicting an unseen environment's level is the paper's stated aim ("unseen and new environments"), not a
         side effect.
       - So RMSE keeps its meaning (MET-2 holds), and MET-4 (Should) keeps the source's metric.
   (b) That the evidence already favours a switch.
       - MET-4's amendment asks for measurements that favour the switch. Variance shares are not the model order the
         benchmark reads.
       - In the sibling, the rank agreement was tau 0.91, and that kept the metric.
   (c) That mean_group_pearsonr by location-year scores the breeder's unit.
       - The release has no test id, so a location-year pools 2-4 maturity-group tests (precedent checker D5).
       - Part of that score is ranking tests, not lines.
   What follows: the metric is a curator weighing call after the measurement. Until then, ship with RMSE and the note.

3. Provenance note (PROV-8, EV-2). Concede. This is my point 2's remedy, plus the clause "159 location ids where the
   paper counts 150".

4. Misstated numbers (EV-2). Concede all three. (a) "5 of 6". (b) Scope the weather sentence to "beyond each
   location's mean and the yield trend". (c) State the floor: 13.17, and 13.04 with line history. TP-2 keep is
   unchanged.

5. Window count (SPLIT-14, SPLIT-15). Concede. Either fix is fine. I lean to adding 2009 (50.7% of rows, above the
   floor), given the blind reviewer's ranking-stability concern and the task gamer's per-window swings of up to 0.5.

6. AvgSur_d213 (CLEAN-11). Concede: set the impossible cells to missing (my point 7).

7. Wording (CLEAN-14, writing.md). Concede (a), (b) and (c): "the maturity group of the test", MG kept numeric with
   its reason, "entry mean at the location", the AP grid clause and the surface-temperature clause.

On the critic's dropped items:
- Later-year genotype presence: we agree it is no defect of this definition. The critic calls it a container
  property; I put it under LEAK-9, with a protocol line. The two are compatible. A library-level note would also
  meet LEAK-9.
- We agree on width, the repeated rows and the low signal.

Net: no Must is left open after the text fixes. The one weighing call is point 2: measure, then decide with the
sibling.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: uniform_soybean_tests_yield (2026-11-09)
Read: dataset.py, principles.md, builder_report.md, the seven phase-A reports. Advocate's brief not read.

POSITION
Ship only after changes. The task is real, the data is the authors' (claim auditor's match), the held-out-season split
is right and there is no leak to fix. But the definition's own text argues against its split, and the declared metric
on that split scores something the actor does not act on. Neither is a reason to exclude: both are fixed in the
definition. Points in rank order.

1. The use case contradicts the split (P3; USE-1 Must, USE-3 Must; USE-9's weighed factor "rephrased only to excuse
   a gap").
   Problem: use_case and the prediction-point bullet put the breeder "after a season". At that moment every yield of
   that season is known, the checks and the other lines at the same location-year included. That is exactly the
   information the source's random split hands a model, and the definition rejects that split. So the use case, as
   written, argues for the split we do not ship (USE-1: every split choice is checked against the use case).
   Effect: a reader or curator who follows the written use case would conclude the random split is right (env mean
   8.02 vs 13.71 location mean: the season's own results are worth ~6 bu/acre). The post-season moment was chosen so
   the weather is admissible; no source names this decision (claim 13 untested; practitioner: after harvest a
   breeder compares a line with its checks, not a weather model).
   Evidence: found independently by the claim auditor (U1), split auditor (finding 1), domain practitioner (B);
   precedent checker D7 "departs without a fact that holds". The paper's aim, "predict performance ... in unseen and
   new environments", is what the split already mirrors.
   Remedy (fix the definition, wording only): rewrite use_case and the prediction-point bullet to the paper's aim: a
   breeder or UST coordinator predicts each entry's yield at the locations of a season not yet in the data, from the
   line, the site and that season's weather taken as a given condition (scenario), fit on earlier seasons. Fit stays
   approximate; fit_reason (USE-8 Must) names the gaps in order: weather as a perfect-forecast/scenario stand-in;
   absolute yield where the breeder acts on yield relative to the test's checks; no test id or check flag (a
   location-year pools 2-4 maturity-group tests); no soil, planting date or management. Split, features unchanged.

2. On the shipped split the metric scores the environment level, not the actor's decision (P3/P6; USE-5 Must,
   MET-1 Must, MET-2 Must third bullet; MET-4 Should as amended 2026-11-05).
   Problem: 75.3% of yield variance lies between location-years. Knowing each test environment's mean takes RMSE from
   ~14 to 7.3-8.2; adding everything known about the line on top of that moves it 0.0-0.3 (practitioner). RMSE
   therefore ranks models almost entirely by how they guess a new location-year's level, which no feature predicts
   (weather adds nothing beyond location mean + trend). Under the challenge's random split the level was known
   (env mean 8.06), so RMSE there scored mostly within-environment deviations; our split changed what the same
   metric measures (MET-2: a changed task keeps the source's metric only when its meaning survives).
   Effect: the practitioner "would not use this model as specified": a model that guesses the level well and ranks
   lines at random beats one that ranks lines well. Within-location-year Spearman does separate models (0.14-0.24
   LightGBM; lines with history 0.22-0.28; new lines 0.0-0.13), so a within-environment score is measurable.
   MLCAS2021 is a research-run challenge, the class MET-4's amendment lets give way when measurements favour it.
   Evidence: domain practitioner MEASURED block; split auditor variance numbers; precedent checker D5 (protein,
   huesken: same mechanism, there a pooled score rewarded group means).
   Remedy, mildest that works: measure first (precedent checker option c): rank ~10 models under RMSE and under
   mean_group_pearsonr by location-year on the 6 shipped windows (Kendall tau, as done for genomic_prediction_soy_
   yield, tau 0.91 there). If the orders disagree, declare mean_group_pearsonr by location-year (location-year as a
   scoring column; MET-11 context, RMSE named as the overruled original). If they agree, keep RMSE and write in
   fit_reason and the Metric bullet that on held-out seasons it mostly scores the new environment's level. Decide
   together with genomic_prediction_soy_yield (same actor), and after point 1, since the unit follows the use case.

3. The provenance note does not carry the evidence that makes the copy acceptable (P5; PROV-8 Must; EV-2 Must).
   Problem: download_description ties the CyVerse copy to the challenge only by file dates and shapes. On that alone
   it is weaker than every accepted precedent (precedent checker D1: all were tied by original bytes or the owners'
   copy). The tie that holds was measured by the claim auditor and is not in the definition: clusterID_genotype.npy
   byte-equal to the authors' GitHub data_subset/k_means_clusters_20.npy; the 103,365 genotype ids (and genotype-
   state pairs) the same multiset as genotype_id_all_data.npy / state_list_all_data.csv; 1,870 of the authors' 2,000
   subset rows match a training record with identical weather, the other 130 in the test inputs.
   Remedy (note): add these three facts with the GitHub path to download_description and the Source bullet; add
   "159 location ids, where the paper and challenge count 150" (claim auditor N3). Asking the authors for a stable
   deposit stays optional (the host is personal: a reproducibility risk, not a provenance failure).

4. Measured claims misstated (EV-2 Must; TP-2 Should for the reading).
   Problem: (a) Note bullet "worse on 4 of 6 windows" is 5 of 6 for the stated pair (claim auditor N2).
   (b) "the gridded weather ... does not predict" is overstated: the builder's own experiment_split.log has daily
   weather improving a direct LightGBM 14.55 -> 14.19 (4 of 6), with the expected agronomic signs; it adds nothing
   only beyond each location's mean and the yield trend (claim auditor N1). (c) The floor a method must beat is
   about 13.0-13.2 (location mean + linear trend 13.17; + line history 13.04), not stated.
   Remedy (note): correct the count, scope the sentence to "beyond each location's mean and the yield trend", give
   the 13.17/13.04 floor. TP-2 keep is unaffected.

5. The window count rests on the wrong share (P4; SPLIT-15 Should, read against SPLIT-14 Must).
   Problem: min_train_fraction with unit="unique" counts seasons; SPLIT-14's floor counts data. The 2009 window
   trains on 47,067 of 92,814 rows = 50.7% (split auditor finding 3), so SPLIT-15 would allow a 7th window, and
   splits_comment gives the seasons reason ("at least half of the 13 seasons").
   Remedy (fix the definition, either): add the 2009 window with explicit cutoffs, or keep 6 and say why by rows.
   With ~80 location-years per window and per-window swings up to 0.5 (task gamer), one more window helps ranking
   stability (blind reviewer concern 1).

6. AvgSur_d213 is an impossible value in 14.9% of rows (P7; CLEAN-11 Should). Quality only, no reason to exclude.
   Problem: the authors' fill (mean of d212, d214) lies outside that day's [MinSur, MaxSur] in 13,843 rows (178 of
   1,117 location-years, up to 11.9 F); no other day ever does (column auditor F1). The Anomaly bullet says filled,
   not impossible.
   Remedy (repair, cheap and safe): set AvgSur_d213 to missing where it falls outside [MinSur_d213, MaxSur_d213];
   or keep and give the counts in the bullet as a documented departure.

7. Wording that misdescribes columns (P7; CLEAN-14 Should, writing.md).
   (a) task_summary question/known say "the line's maturity group": it is the test's (215 lines in two adjacent
   groups, 11.7% of rows; column auditor F2, claim auditor N4); and write down the call to keep it numeric (CLEAN-14
   bands bullet points the other way; equal steps of relative maturity justify numeric). (b) "as the trial reports
   it" is a location entry mean over replications (practitioner). (c) AP's 0.01 in/h grid (a day with <~0.12 inch
   reads 0, 77.6% zeros) and "surface temperature" running hotter than 2 m air (303 location-days >110 F incl. MN,
   ND) deserve one clause each (column auditor N1, N2).
   Remedy (note): reword.

DROPPED (could not back as a definition defect)
- Task gamer's later-year presence of a genotype (gain ~0.07-0.17 RMSE, ~1%): visible only to a participant reading
  the whole shipped table; the harness gives a model train and test rows only. A container-format property of every
  temporal dataset with recurring ids, not this definition's. Worth a library-level note, not a point here.
- Width (1,498 daily columns; blind reviewer 2): "width is no reason to drop features" (tension table, coad).
- Repeated genotype-location-year rows (blind reviewer 3): documented, within one year, no split crossing.
- Low signal (builder issue 2): TP-2 and "the right split against the score" (forest_fires) keep it; I do not argue
  retirement.

Judgment record:
  Verdict: ship after changes.
  Validity: USE-1/USE-3 triggered (use case argues for the rejected split), fixed by rewording (point 1); USE-8 fit
  reason to name the larger gaps; SPLIT-1/SPLIT-5 hold; SPLIT-15 window count by rows (point 5); PROV-8 holds once the
  match is written down (point 3); LEAK-30 weak, kept.
  Value: MET-1/MET-2 open, measure model-order agreement then decide with genomic_prediction_soy_yield (point 2);
  TP-2 keep; EV-2 corrections (point 4).
  Quality: CLEAN-11 d213 (point 6); CLEAN-14 and wording (point 7).
  For the curator: point 1 (wording of the use case) and point 2 (metric, a weighing call under amended MET-4).
```

</details>

<details><summary>Critic rebuttal</summary>

```text
CRITIC REBUTTAL: uniform_soybean_tests_yield (2026-11-09), to the advocate's opening brief, points 1-7
We agree on the verdict (ship after changes). One dispute remains: the metric (advocate 6).

A1 Split (SPLIT-1, SPLIT-5). Concede. My brief keeps seasons too. My point 5 (window count) is the only split change.

A2 Provenance (PROV-8, PROV-13). Concede. The advocate's remedy is the same as my point 3. Add the clause
   "159 location ids where the paper counts 150".

A3 No leak; the later-year genotype exploit is an evaluation-level leak (LEAK-9). Concede. LEAK-9 (amended
   2026-11-05) puts this kind of leak in a protocol line, not in the data. That is compatible with my dropped item.
   The protocol line should say what it forbids: features built from rows outside the window's train and test
   indices. A note that names nothing is not checkable.

A4 Small real signal (TP-2). Concede. I do not argue retirement. The remedy is the same as my point 4.

A5 Use case (USE-1). Concede, with one point the advocate's rebuttal reopens. The reword's actor is "a breeder or
   test coordinator". The advocate later leans on insurers and marketing as the absolute-yield actors. The
   practitioner's evidence says trial-plot yields of experimental lines are a poor proxy for farm yield, and that
   none of those actors decides per trial cell (practitioner, 2. TARGET). The actor the reword names, and the only
   one the cell-level row fits, is the breeder. Settle PROMPT 1 with that actor written down, since point 2 follows
   from it.

A6 Keep RMSE (MET-4). Partly concede, partly dispute.
   - Concede on MET-2's third bullet. Its letter is "same target, same classes, same class balance", and the target
     is unchanged. So MET-2 alone does not force a switch.
   - Concede that variance shares are not the model order. MET-4's amendment asks for measurements that favour the
     switch, so the Kendall tau run comes first.
   - Concede part of the advocate's (c): a location-year pools 2-4 maturity-group tests. The practitioner already
     gave the remedy: group by location-year x maturity_group, a tighter proxy for the test, which builds from
     shipped columns.
   - Dispute that the metric holds under MET-1 (Must, ranked above MET-4's Should). With the breeder as actor (A5),
     the decision is the within-test ranking. Oracle level + line effect moves RMSE by only 0.0-0.3, against ~14 ->
     7.3-8.2 for the level alone (practitioner). A model that ranks lines at random but guesses the level well wins.
     MET-1 asks whether the metric scores that decision, and the measurement says it barely does.
   - Dispute "ship with RMSE until then". The tau run is ~10 untuned models on 6 windows. Shipping first and
     switching later changes every published score of the dataset. Run it before the curator decides. This is not a
     hold on the data: the metric is the only open line.

A7 Quality (CLEAN-11, CLEAN-14, SPLIT-15). Concede. These are the same fixes as my points 5-7. I agree with adding
   the 2009 window (50.7% of rows).

Net: 6 of 7 conceded. Open: the metric. Run the tau measurement (grouped by location-year and by location-year x
maturity_group) before the curator's call. Name the breeder as actor in PROMPT 1. Decide jointly with
genomic_prediction_soy_yield.
```

</details>
