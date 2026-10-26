# Across datasets

### Probes (`curation_probes/hidden_groups.py`)

- **Let the hidden-group probe consider float columns with repeated values.** Its single-column check takes a float
  column only when every value is a whole number (`is_candidate` in the general probe library), so a computed
  per-entity value never becomes a candidate. In airfoil_self_noise the boundary-layer thickness alone separates 104
  of the 106 wind-tunnel runs, and the probe missed the runs until composite keys were added (review-panel pilot,
  2026-10-19). lgd is a second case: its borrower runs are marked only by a repeated loan-to-value ratio (1,958
  values over 2,545 rows, each value in one run of consecutive rows), which the probe cannot see either (lgd review,
  2026-10-20). The proposal below would still miss lgd: 2,545 rows over 1,958 values is 1.3 rows per value, below
  the 1.5 the integer rule asks for. Its runs show only in the file order. Proposal: take a float column as a
  candidate when its distinct values are few against the rows (the same share rule as for integers), then re-run the
  hidden-group sweep and compare the hits. The probe library changes; no definition does.
  **Resolved (2026-10-21, Lennart):** a float column is a candidate under the integers' share rule, and every
  candidate now needs at least 20 values held by two or more rows (a sparse bin crashed micro_mass and sarcoma).
  airfoil's thickness is now a hit; lgd's loan-to-value ratio (1.3 rows per value) still is not, as predicted. One
  new hit in an IID dataset is the new follow-up "drug_induced_autoimmunity_prediction" below.

### Framework

- **Keep the newest rows when `task_probes.py` caps a temporal task's train side.** The probe caps the train side at
  50,000 random rows, so on a drifting panel the newest periods are thin. On mortgage (2026-10-20) the capped
  LightGBM (skill +0.113) falls below `time` alone (+0.123) and raises `one_feature`, while LightGBM on the full train
  side beats the previous quarter's class shares in every window. Proposal: for temporal tasks, cap by keeping the
  newest rows. Also: the 1-NN label agreement in `leak_probes.py` mostly measures panel repetition on loan-period
  data. The probe library changes; no definition does.
  **Lennart (2026-10-21, go ahead):** Yes go ahead, but also feel free to raise the row cap maybe as needed and as
  we have compute?
  **Resolved (2026-10-21, Lennart):** the task probe keeps a temporal task's newest train rows and the cap is now
  200,000 rows (`MAX_ROWS`); the dummy uses the whole train side. mortgage at 200k raises no flag (LightGBM +0.151,
  drift +0.122, one feature +0.117), as uncapped. A full sweep at the new cap (about 2-3 hours) is not run yet. The
  1-NN reading on panels is a new reading of probe 6 in evidence.md.
- **Consistency check: sberbank_housing_market_forecasting keeps its macro columns unlagged.** mortgage lags each
  macro series to its release (LEAK-10), while sberbank joins each month's or quarter's own statistics to sales inside
  that period, with a note that the release dates are unknown (mortgage review panel, precedent check, 2026-10-20).
  What sets sberbank apart? (a) its roughly 100 series have unknown release dates, so no lag can be rebuilt: record
  a `Potential leak, kept on purpose:` note; (b) lag its monthly and quarterly series by one period, like mortgage;
  (c) amend LEAK-10 for statistics whose release date is unknown. For sberbank's review; it does not block mortgage.
  **Resolved (2026-10-21, Lennart):** (b): sberbank's monthly, quarterly and yearly macro series are lagged one
  period, like mortgage (LEAK-10); the daily market series keep the sale date. RMSE 0.2528 to 0.2520 over its 5
  windows.

### Molecule datasets (fingerprints and descriptors)

- **One dtype convention for 0/1 fingerprint bits.** qsar_oral_toxicity ships its 1,024 bits as `int64`,
  hiva_agnostic its binary descriptors as `category`, qsar_tid_11 its bits as `float64` (qsar_oral_toxicity review
  panel, column audit, 2026-10-20). Nothing is wrong in any of the three, but a reader comparing them sees three
  types for the same thing (CLEAN-14, Should). Proposal: pick one form for binary presence flags and apply it to the
  three definitions in one change.
  **Lennart (2026-10-21, go ahead):** Assuming it is binary, the categorical dtype might be best?
  **Resolved (2026-10-21, Lennart):** categorical, after checking the values are only 0 and 1 (CLEAN-14 amended for
  a molecule's presence flags); qsar_oral_toxicity and qsar_tid_11 changed, hiva_agnostic already was.
- **Consistency check: hiva_agnostic keeps 23 exact copies.** It keeps the 23 compounds that repeat another's
  descriptor vector with the same label (AI, 2026-10-14, no reason given), while qsar_oral_toxicity drops its 477
  under LEAK-19, as wine_quality did (Lennart, 2026-09-30). Same mechanism: exact copies of a compound's descriptor
  vector, one label, binary IID screen. What sets hiva_agnostic apart? (a) the copies are 0.5% of the rows and only 3
  cross the challenge's training/validation cut, so the effect is negligible, recorded as an exception; (b) drop its
  23 copies as well; (c) reopen qsar_oral_toxicity and keep its copies; (d) amend LEAK-19 with a share below which
  copies may stay. For hiva_agnostic's review; it does not block qsar_oral_toxicity.
  **Lennart (2026-10-21, discuss):** IF the copies dont make any sense from a task use case, we should drop them as
  far as I understand
  **Answer (AI, 2026-10-21):** the 23 copies are not one compound entered twice: the challenge's structure release
  has 4,229 distinct NSC numbers, and at most 19 of its structures repeat another (7 exact, 9 ignoring stereo, 19
  counting salt forms), so at least 4 of the 23 are different compounds the descriptors cannot tell apart. All 46
  rows are inactive. By your note they stay (they are real screened compounds); the facts are now in the notes and
  the record. Mark ok to close, or change to drop them anyway.
  **Resolved (2026-10-21, Lennart):** kept, by your note: the copies are distinct screened compounds; the facts are
  in hiva_agnostic's notes and record.
- **qsar_tid_11 has no decision on its repeated fingerprints.** 870 of its 5,741 rows (15%) sit in 387 repeated FCFP
  vectors (116 exact copies; within a vector the pChEMBL standard deviation is 0.25 against 1.54 overall), with no
  decision recorded, while LEAK-16 (Must) asks for one every time (qsar_oral_toxicity review panel, precedent check,
  2026-10-20). Ways out: (a) the repeated vectors come from different ChEMBL records with different measured values,
  so they are not copies with one label, and the decision is to keep them with that reason written down; (b) one row
  per vector, LEAK-19 and LEAK-20 adapted to regression; (c) group on the vector, which needs the ChEMBL id the
  definition drops (SPLIT-24 bars a bare feature hash); (d) amend the rule for repeated vectors with differing
  regression targets. For qsar_tid_11's review.
  **Lennart (2026-10-21, discuss):** THis might be a grouped task, investigate if that makes most sesne here, or if
  we should do (a) or (b)
  **Answer (AI, 2026-10-21):** all 5,742 rows carry distinct ChEMBL compound ids, so the repeats are different
  compounds: of 798 traced rows, 179 vectors are stereoisomers, 125 analogs (F against Cl), 31 salt forms of one
  parent (target sd 0.006, real copies). LightGBM RMSE: random split 0.765, grouped on the vector 0.781, one row per
  vector 0.757; predicting a repeated row by its vector-mates' mean gives 0.798, worse than the model. A grouped
  task does not fit (SPLIT-24 bars a bare fingerprint hash, and grouping would test whether the fingerprint resolves
  stereoisomers). Recommendation: (a) keep the repeats with this reason, and drop the 31 salt-form copies as LEAK-19
  does in qsar_oral_toxicity. Not applied yet.
  **Lennart (2026-10-21, go ahead):** Yes, follow your recommendation
  **Resolved (2026-10-21, Lennart):** applied: one row per ChEMBL parent, so 37 salt-form copies leave (the 31
  whole-vector pairs and 6 pairs inside larger vectors; the parent's own row stays), 5,741 to 5,704 rows; the
  decision to keep the stereoisomers and analogs is written in qsar_tid_11's notes. If only the 31 should go, 6 ids
  come off the list.

### Rules and the benchmark harness

- **TP-6 and definitions.md disagree on a competition's metric.** TP-6 (Must) says a version the source defines, "the
  scoring it uses" included, replaces ours when it is the better version; definitions.md ("Field mapping") says a
  competition with its own metric keeps our default and the notes name the original. No dated curator decision
  exists on either side: amex_non_iid_1m, allstate_claims_severity, porto_seguro, 5g_energy_consumption and
  sepsis_prediction_1m ship their competitions' metrics, african_credit_scoring_challenge keeps the default
  (force_2020 review panel, precedent check, 2026-10-20). A Must has no exceptions, so one text needs an amendment.
  zillow_prize keeps RMSE although the competition scored MAE; under the proposed amendment it would switch to `mae`
  (0.38% of its rows hold half the squared error; zillow_prize review panel, 2026-10-20).
  digicow_farmer_training_adoption_challenge keeps ROC AUC; its notes name Zindi's rubric (log loss 0.75 and ROC AUC
  0.25 over the 7-, 90- and 120-day targets; 7-day log loss 0.65, 7-day ROC AUC 0.15). Under the proposed amendment it
  would switch to log loss. There, log loss would mostly score how well a model guesses the next window's adoption
  rate, which moves with the trainers' recording waves. The point is moot while digicow is recommended `No` (digicow
  review panel, 2026-10-20).
  numerai_v5_2 keeps RMSE, while Numerai scores CORR (per era, one week of stocks, the correlation of the predictions
  with the target across the era's stocks, averaged over eras). Over nine untuned models on its three test windows,
  RMSE's ranking agrees with CORR's at Kendall tau -0.11, 0.11 and 0.39, pooled `pearsonr`'s at 0.89 to 0.93; pooled
  `pearsonr` tracks CORR within 0.0002 per model there because every week's target mean is 0.5. RMSE rewards the scale
  of the predictions (the same LightGBM predictions stretched by 3 lose to the constant 0.5 in every window). Under the
  proposed amendment it would switch to `pearsonr` (numerai_v5_2 review panel, mediator, 2026-10-20; its issue 2).
  Proposal: amend TP-6 so that a competition metric replaces ours only when it scores what the use case needs and
  can rank the models' outputs (a hard-label metric such as FORCE 2020's penalty matrix or African Credit's F1 then
  stays a note), and align definitions.md with it. The knowledge files change; the five definitions are then checked
  against the amended rule.
  **Lennart (2026-10-21, go ahead):** Ok maybe change the skill and update these cases as you see fit, in short this
  is what I want: we want to correctly document the metric that was used by the original use case. We only want to
  overule it, if the metric was biased or wrong (based on some evidence we can infer from the paper). In general, we
  watn to keep the note of the metric, as it makes no difference for the benchmark later which currently ignores
  this field
  **Resolved (2026-10-21, Lennart):** TP-6 amended: a definition declares the metric its source's competition or
  paper scored, overruled only on written evidence that it is biased or wrong; the notes always name the original.
  Changed: zillow_prize `mae`, numerai_v5_2_1m `pearsonr`, african_credit `f1`, force_2020 its penalty matrix,
  digicow `log_loss`, porto_seguro `roc_auc` (Gini is linear in it), dataorg `f1_weighted`, g_research `pearsonr`,
  huntprohibited `average_precision`, bioresponse `log_loss`, mercedes `r2`; notes only for kick,
  home_credit_default_stability_1m, sberbank, california_house_prices_2020, 5g_energy_consumption. Six unclear cases
  are the item "Metrics still to settle" below.
- **Check TabArena's LightGBM default on force_2020 before reading its rank.** Untuned LightGBM with the default
  `min_child_weight` of 0.001 diverged on this dataset (grouped fold 0, 100k rows: test log loss 14-15, task probe
  2.68 against a random forest's 0.744); with `min_child_weight=1` it gave 0.81 (force_2020 review, 2026-10-20;
  mice_protein shows the same divergence). After the definition masked a few hundred impossible readings (DCAL
  10,006.8, DRHO -7,429.3 and others) the task probe's LightGBM gives 0.872 and no longer diverges, so extreme
  values were the likely trigger. Proposal: check the benchmark's LightGBM default on this dataset once it is built.
  **Lennart (2026-10-21, go ahead):** we dont need to check the benchmark case, we can do that later, it is fine as
  is for now
  **Resolved (2026-10-21, Lennart):** left for later, as is.

### Churn datasets

- **Consistency check: tag the other one-snapshot churn sets `ForcedIIDFromTemporal`?** expresso_churn_prediction_1m
  now carries the tag (SPLIT-8, Must: a task temporal in nature that ships as IID because the release has no time
  index), as account_debt_south_africa does (Lennart, 2026-10-12): the operator scores each window with a model
  trained on an earlier one, but the file is one undated snapshot (expresso review panel, split audit, 2026-10-20).
  churn_telco_south_asia, bank_customer_churn and tour_travels_churn are churn snapshots of the same kind
  and have no `data_tags`. mobile_churn now carries the tag too (mobile_churn review panel, 2026-10-20), with the cost
  measured on its only later rows (training on June gives ROC AUC 0.661 against 0.690 under the IID split on the
  1,533 July and August joiners, a gap that mixes cohort with time). Its release has a record month, but only one
  month of the customer base, so whether SPLIT-8's "no time index" covers a release with a few cohort months is part
  of this item (its issue 4). Ways out: (a) tag all of them, with one sentence each on what a dated window would
  change, and word SPLIT-8 to cover a release with one stock month; (b) record why a churn snapshot is not "temporal
  in nature", and drop the tag from expresso and mobile_churn as well. Nothing in the data changes either way.
  **Resolved (2026-10-21, Lennart):** (a): SPLIT-8 amended to cover a release with one stock month or a few cohort
  months; churn_telco_south_asia, bank_customer_churn and tour_travels_churn tagged `ForcedIIDFromTemporal`.
- **Consistency check: LEAK-38 and kick's `WheelType` after expresso's REGION drop.** expresso_churn_prediction_1m
  drops REGION under LEAK-10 (its missing flag separates churners at ROC AUC 0.936 among customers active on all 62
  days, while no column that summarises the window passes 0.59), while kick (Lennart, 2026-10-01) kept `WheelType`
  under LEAK-38 on the same release facts: a named field in the company's own competition release, an undocumented
  recording process, the same missingness in the host's test set (expresso review panel, precedent check,
  2026-10-20). LEAK-38 speaks of "anonymised" fields, which `WheelType` is not. Ways out: (a) amend LEAK-38's scope to
  fields whose timing cannot be tested; (b) reopen kick and run the same conditional test on `WheelType` (missingness
  by an in-window covariate, separately for good and bad buys); (c) amend LEAK-38's wording only. It does not block
  expresso, whose issue 1 asks only whether the drop stands.
  A second case the same day: fraud_detection_in_electricity_and_gas_consumption_1m cuts STEG's invoice history at
  2013-01-01 instead of keeping the full history with a `Potential leak, kept on purpose:` note, as kick and homesite
  (`PropertyField37` x `PersonalField12`, Lennart, 2026-10-01) kept theirs. The fact that sets it apart is the same
  as expresso's: named meter codes with a measured mechanism (the fraud rate of new second meters steps from
  7.4-11.9% per quarter in 2012 to 23.8-25.9% in 2013 while the number of such events stays flat; 47.8% of the
  frauds carry the trace; ROC AUC 0.848 with the full history against 0.688 with the cut). Option (a) covers both
  datasets; it does not block STEG either, whose issue 1 asks whether the cut stands (STEG review panel, precedent
  check and mediator, 2026-10-20).
  **Lennart (2026-10-21, go ahead):** Reopen kick here
  **Resolved (2026-10-21, Lennart):** kick reopened: the expresso test gives the same signature (`WheelType` missing
  for 24.9% of bad buys and 1.5% of good ones in every band of age, odometer and price). kick's REVIEW.md issue 1
  asks to drop it, issue 2 a new finding on `PRIMEUNIT`/`AUCGUART`.

### Flight-delay records

- **Judge `pnwflights14` against aeolus for uniqueness.** The `airlines` and `airlines_depdelay_10m` records carry a
  dated note that defers whether they are a second flight-delay task or a duplicate of aeolus; `pnwflights14` (BTS
  on-time data of 2014, AI-unverified) has none, though all of them end at the same BTS on-time table (aeolus review
  panel, precedent check, 2026-10-20). Under PROV-6 (Must) a cut of one source without a distinct task is a
  duplicate, and the record processed later decides. Proposal: add the same dated note to `pnwflights14`, with
  aeolus as the task it is judged against. A record edit outside aeolus; it does not block aeolus.
  **Resolved (2026-10-21, Lennart):** the dated note is in the pnwflights14 record.

### Rules from the Framingham review

- **Amend PROV-14 to separate a repair from a rebuild?** PROV-14 (Must) says a rebuild that does not match the release
  exactly is a new dataset with its own record. SUPPORT2 (2_month_survival_rate_prediction) and
  cirrhosis_patient_survival_prediction were repaired in place, and framingham_heart_study_fhs now is too (same
  participants and feature values row for row, the damaged label restored from the origin's event columns), while
  corporate_credit_rating became corporate_issuer_credit_rating (new data from new sources, Lennart 2026-10-16). A
  precedent that contradicts a rule is flagged, not followed (framingham review panel, mediator and precedent check,
  2026-10-20). Proposal: amend PROV-14 so that a repair (same units, same features, damaged values restored from the
  origin) stays under its record, and only a rebuild from other sources gets a new one. It does not block
  framingham, whose issue 7 asks only how to record it.
  **Lennart (2026-10-21, go ahead):** I agree to this
  **Resolved (2026-10-21, Lennart):** PROV-14 amended: a repair stays under its record; framingham's issue 7 is
  answered.
- **Amend PROV-3 for an owner's disclosure control on a real cohort?** PROV-3 (Must) excludes a real table whose values
  someone replaced, and its four cases were all retired on a test that fired. The Framingham teaching data was
  anonymised by its owner (BioLINCC, methods undocumented; permutation or visit selection named by a textbook), and
  no test fires (digit preference intact, within-person correlations 0.90 and 0.71). Proposal: if more such datasets
  are expected (other BioLINCC teaching sets), amend PROV-3: values perturbed by the owner for privacy, with no
  measurable damage, are kept with a note saying what was checked; otherwise record framingham alone as a case
  (its issue 3).
  stroke_prediction may be a second case: its ages 78 to 82 hold about 1,029 more patients than the trend gives, and
  the extra rows carry the stroke risk of older ages, as recording every age above 82 inside that range would (its
  issue 1; this points that way and does not prove it).
  **Lennart (2026-10-21, go ahead):** agree, but also add a note about selection bias in the curation record here
  **Resolved (2026-10-21, Lennart):** PROV-3 amended for an owner's disclosure control with no measured damage;
  framingham's record, notes and issue 3 now name the selection: the teaching set is 4,434 of the 5,209 enrolled,
  period 1 is about 1956, and how the subset was drawn is not documented.
- **SelectArena's Framingham copy carries MIT's defective label and a wrong domain.**
  `datasets/_dev/feature_selection/framingham_heart_study/framingham_heart_study.ipynb` builds a container from the
  Kaggle file aasheesh200 with MIT's `TenYearCHD`, which counts 265 deaths and losses among its 644 positives
  (framingham_heart_study_fhs, decision table), and sets `domain_str="physics & astronomy"`. Not touched. Proposal:
  fix both when SelectArena is next rebuilt, or note them there.
  **Lennart (2026-10-21, leave as is):** We dont care about the select arena copy, ignore it
  **Resolved (2026-10-21, Lennart):** left as is (SelectArena is out of scope).

### Rules from the sarcoma review

- **Does a weak potential leak kept on purpose make a fit `approximate`?** USE-8 lists "a potential leak kept on
  purpose" among the gaps of an approximate fit, and sarcoma now reads `approximate` (its closed set of five confirmed
  types is a gap of its own). But most datasets kept with a LEAK-30 note read `direct` (lung_cancer_epithelial_genexp,
  bioresponse, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m), as does ljubljana_primary_tumor with a
  named gap; only kick applied the text (sarcoma review panel, mediator and precedent check, 2026-10-20). A
  precedent that contradicts a rule is flagged, not followed. Proposal: amend USE-8 so that a weak LEAK-30 keep does
  not by itself make a fit approximate; otherwise reopen the fit labels of those datasets. It does not block sarcoma,
  which stays approximate either way.
  **Lennart (2026-10-21, go ahead):** let us stay with direct fit if the task (without leakage) would be a direct
  fit and only move to approixmate fit if we had to change a lot to avoid the leak
  **Resolved (2026-10-21, Lennart):** USE-8 amended: a potential leak kept on purpose does not by itself make a fit
  approximate; the fit is approximate only when avoiding the leak needed a large change to the task. One question
  follows in "Strong kept leaks and the fit" below.

### Rules from the G-Research review

- **Amend TP-10 to keep g_research_crypto_forecasting?** TP-10 (Must) admits a forecasting-like panel only when a
  model clearly beats each entity's naive forecast and the top solutions use no lagged target. g_research fails both:
  under RMSE no window's gain over the coin's mean lies outside the day-to-day noise, and its features (the coin's
  past 60- to 900-minute returns against the 14-coin market) correlate 0.80-0.83 with sums of the coin's own past
  targets (g_research review panel, mediator, 2026-10-20). The advocate's amendment: leg 2 becomes "no lag of the
  target column itself" and leg 1 is measured by the task's own measure of signal (correlation, positive on 70-74 of
  91 test days), on the fact that the actor ranks 14 coins against the market each minute. Against it: a rule change
  written for one dataset; it would have to say why stock stays out, and leg 1 needs a metric the adapter does not
  have yet. Proposal: no amendment; g_research goes `No` + `Time-series (Forecasting)` (its issue 1). Only if you
  amend do its issues 2 and 6 and the next item apply to it.
  **Lennart (2026-10-21, discuss):** Mhm, double check this in depth, does the Kaggle best solutions not use taublar
  models? do they use foreacsting models?
  **Answer (AI, 2026-10-21):** the top three were all LightGBM (G-Research's wrap-up), not sequence models; the 3rd
  place trains one LightGBM per coin on the coin's and the market's past 60/300/900-minute returns, the 14th adds
  the coin's last 15-minute return (close to the last target), and no top solution used an LSTM or ARIMA. So they
  are tabular models, but their inputs are the coin's own trailing returns, which correlate 0.80-0.83 with its past
  targets: TP-10's second leg fails in substance, and its first leg (beating the coin's naive forecast) fails on the
  data. Recommendation unchanged: no amendment, g_research goes No + Time-series (Forecasting). Its metric is now
  `pearsonr` under the amended TP-6 either way.
  **Resolved (2026-10-21, Lennart):** the research is answered above; the decision is
  g_research_crypto_forecasting_1m's issue 1 (No + Time-series (Forecasting) recommended), which now cites the top
  solutions.
- **RMSE ranks shrinkage on low-signal finance panels: decide numerai_v5_2 and g_research_crypto_forecasting alike.**
  Under RMSE a model that predicts closer to the mean wins over one with more signal: in g_research's window 2 the
  model correlating 0.058 with the target scores R² -0.0090, the one correlating 0.049 scores +0.0004. numerai_v5_2
  has the same profile (per-era correlation 0.006-0.018, R² at or below 0.0003); both competitions scored a
  correlation, which the adapter does not support yet (BENCHMARK_CHANGES_TODO.md, "Dataset-specific metrics").
  g_research's test windows are also sampled by row (about 3.8 of 14 coins per minute), so the per-minute score
  across coins cannot be computed. numerai's declared metric is its issue 2 (pooled `pearsonr` tracks Numerai's
  per-week score there); this item decides only whether the two enter a scored run while the adapter still scores
  RMSE. Ways out: (a) enter now with a note, then sample whole minutes (or eras) per test window (advocate, TP-2
  Should); (b) hold both back until the adapter honours their metric (critic, EV-5; numerai mediator, 2026-10-20).
  For g_research it
  applies only if TP-10 is amended (previous item).
  **Lennart (2026-10-21, discuss):** Here we might want to adapt the task to approximate it with RMSE later and add
  this as a note, what would this look like? how are models usually scored here?
  **Answer (AI, 2026-10-21):** both sources score a correlation (Numerai: per-era correlation of rank-gaussianised
  predictions; G-Research: a Pearson correlation weighted by asset over the test period; practitioners: IC and its
  mean over its sd). RMSE fails because MSE = 1 - 2s*rho + s^2 for standardised target and a prediction of
  correlation rho and scale s: a model 3 times too wide loses to a weaker one. An RMSE that ranks like the
  correlation: z-score predictions and target per era (Numerai) or over the window weighted by asset (G-Research)
  before RMSE; then RMSE = sqrt(2 - 2*rho), exactly monotone in the correlation. That needs the scorer to get the
  era ids (a harness change). Both definitions now declare `pearsonr` with this note. Recommendation: keep both out
  of a scored run until the harness scores `pearsonr` or the z-scored RMSE; binarising the target to ROC AUC would
  run now but changes the task.
  **Lennart (2026-10-21, discuss):** What did people on Kaggle, or as a baseline use? Tabular models? Also, could we
  change the target for regression to match what we want it to be? Or would this only make sense if we add custom
  metrics? (i am not opposed to adding custom metrics now, can you do a quick survey what metrics we need and how
  many accepted datasets owuld change as a result?)
  **Answer (AI, 2026-10-21):** Models: Numerai's example and benchmark models are LightGBM regressors on the raw
  features, and strong participants use GBDT ensembles (some add MLPs); G-Research's top three were LightGBM. All
  tabular, all scored by a correlation. Changing the target alone is not enough: for standardised y, MSE = 1 -
  2*s*rho + s^2 for predictions of correlation rho and spread s, so RMSE still punishes a model whose predictions
  are wider than its signal (rho 0.05 at spread 0.3 scores 1.06, worse than the constant; rho 0.03 at spread 0.03
  scores 0.9991 and wins), whatever the target's scale. Numerai's target is already rank-binned per era and
  G-Research's already residualised, so a per-era transform changes almost nothing. The cheapest faithful fix needs
  no new scorer: AutoGluon has `pearsonr`, both definitions declare it, and the harness adapter only allows
  `roc_auc`, `log_loss` and `rmse` today (it falls back silently otherwise); passing the declared metric through
  needs a guard for a constant prediction, where `pearsonr` is undefined. Survey of 173 definitions (130 accepted):
  allowing AutoGluon's built-in metrics changes the scored metric of 11 datasets (4 accepted: 5g_energy_consumption,
  allstate_claims_severity, mercedes_benz_greener_manufacturing, bioresponse; 7 open); adding the three declared
  custom scorers (amex_metric, the PhysioNet utility, FORCE's penalty matrix) brings it to 14 (6 accepted); scoring
  the originals behind today's stand-ins (Gini stability, PAR10 for sat11, per-strain accuracy for micro_mass, per-
  era correlation, AP@k) to 17 (9 accepted), with about 8 custom scorers, 4 of which need group, era or time ids the
  harness does not pass today. Recommendation: allow the built-in metrics now (pearsonr for numerai and g_research);
  custom scorers later, starting with the three already declared.
  **Lennart (2026-10-21, discuss):** We implemented this now through a bigger change to how we handle metrics in
  data foundry, so this point should be resolved.
  **Resolved (2026-10-21, Lennart):** numerai_v5_2_1m declares `mean_group_pearsonr` (Numerai CORR, per era) and
  g_research `weighted_pearsonr` (asset-weighted), both custom metrics of `data_foundry.v2.metrics`, tested against
  the official code; the TabArena adapter's changes are in BENCHMARK_CHANGES_TODO.md.

### Rules from the AlfaBattle review

- **Record the SPLIT-9 / SPLIT-14 reading and the SPLIT-10 exceptions.** SPLIT-9 (Must) says a training row whose
  label is not yet known at the window start must not be in training, and it comes before the 50% floor of SPLIT-14
  (Must). alfa_battle_2_0_task_2 and lending_club both keep training products whose default can still be flagged after
  the window starts, because a gap of the label delay would leave less than half of the rows for training (alfa: 13-27%
  with 12 months). The reading both rely on is written nowhere: SPLIT-9 is met by removing the measurable shortcut (alfa
  drops the products of the test window's clients), and the diffuse rest of unmatured labels falls under SPLIT-10
  (Should), departed from for SPLIT-14 (alfa review panel, mediator and precedent check, 2026-10-20). Neither departure
  is recorded as an exception, and a third case of the same kind triggers an amendment. Proposal: add a Tensions row
  for this reading and record the SPLIT-10 exception for both datasets (alfa's issue 3 decides alfa's gap).
  **Resolved (2026-10-21, Lennart):** Tensions row added in principles.md; the SPLIT-10 exception is recorded for
  alfa_battle_2_0_task_2 and lending_club (lending_club: a 36-month gap leaves 5-9% of the rows for training).
  alfa's issue 3 (gap 0 or 1) stays open.

### QSAR siblings (from the qsar_bioconcentration review)

- **One `domain` for the QSAR siblings.** qsar_bioconcentration, qsar_oral_toxicity, qsar_tid_11, hiva_agnostic and
  clock_protein_toxicity read "chemistry & material science"; qsar_fish_toxicity, qsar_aquatic_toxicity, qsar_biodeg,
  bioresponse and apistox read "biology & life sciences" (qsar_bioconcentration review panel, claim audit and
  precedent check, 2026-10-20; its earlier issue 6). No rule decides it, and the split makes the domain counts of the
  benchmark depend on who added which dataset. Proposal: pick one value for molecule-property datasets and apply it to
  the ten definitions and records in one change.
  **Resolved (2026-10-21, Lennart):** "chemistry & material science" for all ten molecule-property definitions and
  records.
- **Decide the fit label of the QSAR siblings in one pass.** qsar_oral_toxicity's issue 6 (random members of the
  tested set against the untested chemicals the actor screens) applies word for word to qsar_bioconcentration (its
  issue 9, which adds the authors' selected descriptors as a kept potential leak) and to qsar_fish_toxicity (`direct`,
  same selection mechanism, the gap not in its `fit_reason`), while qsar_aquatic_toxicity is `approximate` for the
  same mechanism (qsar_bioconcentration review panel, mediator and precedent check, 2026-10-20). The sarcoma item on
  USE-8 above asks the general question. Proposal: answer qsar_oral_toxicity's issue 6 first and apply the answer to
  the four QSAR definitions in the same change.
  **Deferred (2026-10-21):** waits on qsar_oral_toxicity's issue 6; the USE-8 amendment moves qsar_aquatic_toxicity
  to direct once that issue is decided.

### Rules from the NBA review

- **Amend SPLIT-14 (or add a rule next to SPLIT-8) for a task with too few periods.** Three datasets need a temporal
  split by their use case (USE-10, Must: a known entity gets a temporal split and its previous outcome as a feature)
  but have too few periods for SPLIT-14 (Must: three test windows, each with half the rows or more before it), and
  each took a different way out: nba_players_2016_2019 stacks its three seasons and groups by player (the one valid
  window, 2018-19, scores 0.745 against grouped 0.744 with the same order of model families; its issue 2);
  open_university_learning_analytics_dataset groups by module-presentation (its issue 1); and
  distribution_transformers_at_cauca_department ships one year IID and keeps one year rather than stacking the two
  and grouping by unit (the one valid window, 2019 to 2020, scores 0.648 against 0.639 on the random folds; its
  issue 2). USE-10 outranks SPLIT-14, so none of the three is a valid exception as
  the rules are written, and a third case of the same reason calls for an amendment (nba review panel, mediator and
  precedent check, 2026-10-20). Options: (a) the closest regime that keeps the rows, tagged "forced from temporal" with
  the cost measured against the valid windows, as SPLIT-8 does for a forced IID split (the schema has only the
  `ForcedIIDFromTemporal` tag, so a grouped fallback would need a new tag); (b) a one-window temporal task, a
  framework change; (c) `No` for all three. Proposal: (a), applied to all three in one change; distribution_transformers
  already says in its notes why it keeps one year instead of stacking (the two files hold the same units with identical
  attributes, and its 2019 rows are more contaminated by the later inventory).
  **Resolved (2026-10-21, Lennart):** (a): SPLIT-8 amended; new tag `ForcedGroupedFromTemporal` (schema, validation,
  bundle check). nba_players_2016_2019 and open_university carry it, distribution_transformers
  `ForcedIIDFromTemporal`, each with the measured cost.

### Rules from the rosbank1 review

- **Does a peer-reviewed baseline count as what a data scientist would build (CLEAN-19)?** rosbank1 ships the CoLES
  aggregates (Babaev et al. 2022, as pytorch-lifestream configures them), while alfa_battle_2_0_task_2, a bank
  competition on the same platform, replaced its organizers' baseline with the features the top solutions share (CC
  2026-10-13; rosbank1 review panel, precedent check and mediator, 2026-10-20). rosbank1's issue 5 decides rosbank1
  alone. Proposal: (a) none, keep CLEAN-19 as written and settle rosbank1 by its issue 5; (b) reopen alfa to match
  rosbank1; (c) amend CLEAN-19 so that a peer-reviewed tabular baseline for the data counts as what a data scientist
  would build.
  **Lennart (2026-10-21, discuss):** It is both, we need to think what all kind of teams of data scientists would
  build, so the combination of baselines from competitions and their top solutions.
  **Answer (AI, 2026-10-21):** proposed CLEAN-19 wording: "It is what teams of data scientists on this task would
  build: the union of the organizers' or a published baseline for the data and the features the top solutions
  share." Consistency check: on 2026-10-13 you chose alfa's top-solution aggregates instead of the organizers'
  127-feature baseline. What sets alfa apart? (a) its top-solution aggregates already cover what the baseline
  computes, so alfa stays; (b) rosbank1 takes the top solutions only, like alfa; (c) reopen alfa and add the
  baseline features back; (d) amend CLEAN-19 as worded above and apply it to both (rosbank1 then also needs the top
  2018 solutions' features). Not applied yet.
  **Lennart (2026-10-21, discuss):** Okay, we here the case is that we want to take the best of both, or a
  reasonable combination, and not a union. so here we take the best for alfa as it is the top-solution etc, does
  that make sense?
  **Resolved (2026-10-21, Lennart):** yes, it makes sense. CLEAN-19 now says: take the best of the organizers' or a
  published baseline and the top solutions' features, or a reasonable combination, not their union.
  alfa_battle_2_0_task_2 keeps its top-solution aggregates; rosbank1's issue 5 now asks whether a 2018 top
  solution's features beat the CoLES aggregates.

### Rules from the house_sales review

- **The fit label of the house-price datasets with values kept from after the sale.** house_sales keeps view,
  waterfront and the neighbours' areas as of July 2015, after its sales; about 145 rows changed after the sale, and
  masking them changes nothing measurable (RMSE 0.2147 against 0.2132). USE-8 (Must) lists "a potential leak kept on
  purpose" under an approximate fit, so house_sales now reads `approximate`, while melbourne_housing_market (AI draft)
  reads `direct` with the same kind of remnant (house_sales review panel, mediator, 2026-10-20). zillow_prize reads
  `approximate` for another reason: the Zestimate and the listing data were never released (USE-6; zillow_prize review
  panel, 2026-10-20).
  This is the question of "Does a weak potential leak kept on purpose make a fit `approximate`?" above, for the
  house-price family. Options: (a) keep USE-8 as written: the three read `approximate`; (b) amend USE-8 so that a
  remnant measured to carry no signal keeps `direct`, and apply it to all three. Proposal: decide it with the item
  above, in one pass.
  perth_house_prices reads `approximate` under the rule as written; its other gaps (a truncated target, attributes as
  of a later scrape) fall outside option (b), and whether an amendment names them is its issue 1.
  **Resolved (2026-10-21, Lennart):** house_sales back to `direct` under the amended USE-8; melbourne stays direct,
  perth approximate (its issue 1).
- **One window length for the house-price datasets.** house_sales tests 9 windows of three weeks (617 to 1,458 sales
  each); the length follows the 3 x 3 window count (SPLIT-15), not a refit cadence the source states (SPLIT-12,
  Should). Six calendar months (a monthly refit) would give 911 to 2,084 sales; SPLIT-21 forbids picking by score. The
  siblings differ: perth_house_prices one month, house_prices_nominal two months, zillow_prize one month with a gap
  (Zillow's monthly ask, the only one from the source), melbourne_housing_market three weekly sheets, and perth and
  melbourne cite house_sales as their precedent. house_sales now has a one-week gap for the recording delay of a sale
  (median 6 days; zillow_prize has a gap for the same county mechanism), which perth and melbourne would follow.
  california_house_prices_2020's `min_train_fraction=0.25` contradicts SPLIT-14 (Must; half the rows before every
  window) and should not be copied (house_sales review panel, precedent check and mediator, 2026-10-20). Proposal: the
  3 x 3 weeks of house_sales for the family where the size allows it, with the recording gap, decided once.
  perth_house_prices adds a spacing option for the family: windows at the refit cadence, spaced with `step` (how far
  each window moves back) where one atypical stretch would hold them all, as rain_in_australia does (`step=42`);
  perth's case is its issue 6.
  **Lennart (2026-10-21, discuss):** We can keep the horion divers as is, as different task might forecast
  diffeerntly long, maybe standardize some of it as you see fit but in general, all is fine here and we dont need to
  force the same split
  **Resolved (2026-10-21, Lennart):** no family-wide window length. california_house_prices_2020 did break SPLIT-14
  (its oldest window trained on 25% of the rows) and now trains on 50%, 67% and 83%.
- **Cite the first publication in nyc_taxi_trip_duration.** Like house_sales before this review, it names a
  government source but cites the Kaggle re-upload in its `bibtex`; PROV-10 (Must) cites the work that published the
  data, as airfoil_self_noise and now house_sales do (house_sales precedent check, 2026-10-20). Proposal: cite the
  original publisher there too.
  **Resolved (2026-10-21, Lennart):** the TLC trip records are cited first.
- **Reopen california_house_prices_2020's newest-only deduplication.** It keeps only the newest entry of 63 houses that
  appear more than once ("to avoid group-related target leakage"). Under its temporal split an earlier sale is history
  (USE-10, SPLIT-13), and house_sales, melbourne_housing_market and zillow_prize keep resales (house_sales precedent
  check, 2026-10-20). Proposal: keep the repeated sales there too.
  **Lennart (2026-10-21, go ahead):** we want to keep real repeats, as hosue can be sold several times
  **Resolved (2026-10-21, Lennart):** california keeps its resales; 51 pairs with the same price are one sale
  scraped twice and keep their newest copy (39,060 rows).

### Rules from the house_prices_nominal review

- **One form of the recording-delay gap (SPLIT-10) for the house-price datasets.** Sales reach these files with a
  delay, so the newest month is short: house_prices_nominal's June 2010 holds about 78% of a usual June. The family
  answers it three ways: house_sales a one-week gap (median delay 6 days), zillow_prize a one-month gap (AI draft), and
  house_prices_nominal no gap, which perth_house_prices cites for its own no-gap split. house_prices_nominal's issue 4
  proposes an exception that rests on the mechanism (its short month's normal sales show no price selection, mean
  residual -0.001), not on the small effect of a gap (under 0.003 RMSE), since the tension row "the right split
  against the score" (forest_fires) rules out the effect size as the fact (house_prices_nominal review panel,
  precedent check and mediator, 2026-10-20). This is the gap half of "One window length for the house-price
  datasets" above. Proposal: decide house_prices_nominal's issue 4, then require perth_house_prices and
  melbourne_housing_market to either measure their newest months the same way or take a gap.
  perth_house_prices measured it and would be the second exception of that reason; its sales are dated by month, so
  its only possible gap is one whole month (its issue 7).
  **Resolved (2026-10-21, Lennart):** melbourne measured: no recording shortfall in its newest sheets (every sheet
  complete against the companion file; newest window's residual +0.009), so no gap. house_prices_nominal's own issue
  still decides its exception.
- **Amend CLEAN-11 for target outliers the source names: the third exception.** CLEAN-11 (Should) keeps unusual rows;
  three definitions drop target-outlier rows against it: mercedes_benz_greener_manufacturing ("We remove the one
  outlier from y"), qsar_tid_11 ("Remove one negative outlier row") and house_prices_nominal (De Cock's three partial
  sales over 4,000 sq ft, which he calls "Partial Sales that likely don't represent actual market values", all in the
  training rows only, recorded as an exception via CLEAN-1). principles.md asks for an amendment at the third
  exception of the same reason (house_prices_nominal precedent check, critic and mediator, 2026-10-20). Proposed
  text: "a row whose target the source names as not the task's quantity, or a single extreme target in the training
  period only, may leave, with the source's words". Proposal: amend CLEAN-11 with this text and check in the same
  change whether the mercedes and qsar_tid_11 drops meet it (neither has a recorded reason).
  **Resolved (2026-10-21, Lennart):** CLEAN-11 amended with the proposed text; mercedes meets its second clause
  (265.3 s against a next highest of 169.9 s, a training row), qsar_tid_11's row now leaves as an impossible value
  (pXC50 -6.24, CLEAN-15), house_prices_nominal cites the amended rule.

- **Say in SPLIT-10 when no gap is needed?** ames_housing's (until 2026-10-26 house_prices_nominal) issue 4 is decided
  (2026-10-26, Lennart): no gap,
  recorded as an exception to SPLIT-10 on the mechanism (the short last month's normal sales show no price selection)
  and the month resolution (sales are dated by month, so the smallest gap is a whole month, longer than the delay).
  perth_house_prices (its issue 7, also dated by month, the same test) would be the second exception of that reason.
  SPLIT-10 then holds three exceptions (alfa_battle_2_0_task_2 and lending_club for SPLIT-14, ames_housing)
  against two applied gaps; with perth it would be four, and principles.md asks for an amendment at the third
  exception of one reason. Proposal: amend SPLIT-10 with "no gap when the delay is shorter than the time column's
  resolution and the newest period shows no selection by the outcome", which perth would then follow without an
  exception (ames_housing marks, consistency check, 2026-10-26).

### Rules from the zillow_prize review

- **Keep a post-outcome lookup because removing it changes no score?** melbourne_housing_market (attributes scraped
  after the sale; blanking them changes the error by 0.0004) keeps values looked up after the outcome on that reason,
  which no rule states (african_credit_scoring_challenge no longer does: it keeps its two lender-share columns at the
  data pull under LEAK-38 because they show no link to the outcome within a loan product, and its panel set the score
  comparison aside under LEAK-5), while LEAK-6 (Must) says a confirmed leak goes even when small. zillow_prize had the same pattern; its
  review blanked the tax delinquency looked up after the sale instead (LEAK-10 via LEAK-7: the "did not change"
  clause fails, 1.5% flagged before the snapshot against 3.8% after, and blanking costs no measurable skill), so it is
  not a third case (zillow_prize review panel, precedent check and mediator, 2026-10-20). Options: (a) apply the same
  smallest fix (LEAK-7: blank or lag the values for the rows before the lookup) to melbourne_housing_market; (b) amend LEAK-11 to read
  "a post-outcome lookup with no measurable effect stays with a note naming the effect". Proposal: (a), since a fix
  that removes every post-outcome value at no cost needs no new rule.
  onlinenewspopularity is a further case that (a) does not reach: its keyword and self-reference statistics hold the
  share counts of earlier articles at the crawl of 2015-01-08, not at publication, and only the cells traced to a
  unique count can be blanked. Blanking the 2,907 traced to an article under 8 days older changes R^2 by -0.0004
  (0.1553 to 0.1549, seed range 0.1543-0.1563); the rest cannot be found. Its panel proposes keeping the columns with
  a note and amending LEAK-10: "a value read at a later pull stays with a note when its effect is measured small",
  with house_sales, aeolus and onlinenewspopularity as its cases, plus melbourne_housing_market unless (a) fixes it
  instead. One amendment, of LEAK-10, would then cover this
  item in place of (b)'s LEAK-11 wording; decide the two together (onlinenewspopularity review panel, precedent check
  and mediator, 2026-10-20; its issue 5).
  perth_house_prices has the same mechanism: its house, station and school columns are the site's record at the
  scrape of January 2021. Its review applied (a) where an opening date is known (147 station values and the school, its
  distance and its rank for 58 sales blanked before the opening), wrote LEAK-10's "did not change" evidence for the rooms (bedrooms or bathrooms differ
  from a second scrape's sold listings in 0.7% of the 2007-2016 sales), and keeps the school rank (one ranking of 2019
  or later) with a `Potential leak, kept on purpose:` note (perth_house_prices review panel, column audit and
  mediator, 2026-10-20).
  **Resolved (2026-10-21, Lennart):** (a) for melbourne: its six scraped attributes are blank for the 7,578 sales
  before the batch lookup of 10 April 2017 (RMSE +0.0011 to +0.0016); onlinenewspopularity's issue 5 stays open.

### Rules from the nyc_taxi_trip_duration review

- **Which datetime encoding the v0.2 runs use, decided once for every dataset whose only time feature is a
  datetime.** CLEAN-2 (Must) leaves the encoding of a datetime to the pipeline, so a definition cannot add an hour
  column. BeyondArena's `tabarena_default` encodes datetimes with skrub's DatetimeEncoder and keeps the hour of day;
  the v0.1 `default` uses AutoGluon's year, month, day and day of week, and loses it. On nyc_taxi_trip_duration
  LightGBM scores RMSE 0.373 / 0.357 / 0.381 with the hour kept and 0.429 / 0.414 / 0.441 without (weekly windows,
  test standard deviation 0.75). pkdd_15_taxi_trip_time_prediction_ii_1m is the same case: LightGBM (300 trees,
  learning rate 0.1, 63 leaves, one fit per split) scores R^2 0.503 / 0.482 / 0.498 on its June / May / April windows
  with the local hour, weekday and day of year, and 0.483 / 0.452 / 0.462 with AutoGluon's date parts. Under `default`
  the scores of these tasks measure the encoding as much as the models (nyc and pkdd review panels, 2026-10-20).
  Proposal: run v0.2 with `tabarena_default`, or change the harness to keep the hour for every datetime-only dataset.
  **Lennart (2026-10-21, discuss):** Why did you propose this? we will always run with datetime encoding in v0.2,
  most likely some evolution of tabarena_default. If you do something in your skills, feel free to use this for your
  tests or checks and probes
  **Answer (AI, 2026-10-21):** it was proposed because the v0.1 default encodes a datetime as year, month, day and
  weekday and loses the hour, which on nyc_taxi_trip_duration and pkdd_15 moves the score more than the models do.
  If the v0.2 runs encode datetimes with the hour (as tabarena_default does), nothing is needed; the probes already
  use their own encoding. Mark ok to close.
  **Resolved (2026-10-21, Lennart):** nothing to change while the v0.2 runs encode datetimes with the hour, as you
  wrote.
- **Align the row-budget wording of definitions.md.** The check-table row `splits_train_over_budget` says "a `_1m`
  version for a frame above 1.5M rows, otherwise narrower windows"; the temporal `_1m` section of the same file (and
  `default_splits` in the code) accepts a temporal `_1m` version whenever a train side exceeds 1M, whatever the frame
  size, and narrower windows never shrink a train side. nyc_taxi_trip_duration (1,447,167 rows, train sides 1.28M to
  1.39M) is the first case between the two (its issue 5; nyc review panel, precedent check and mediator,
  2026-10-20). Proposal: reword the check-table row to match the temporal `_1m` section, or to the amendment the
  curator chooses in nyc's issue 5.
  **Lennart (2026-10-21, go ahead):** we want at moast 1m train samples and the naming can follow as is consient and
  best
  **Resolved (2026-10-21, Lennart):** definitions.md states the budget once: at most 1M training rows; a dataset
  with a train side above it ships as a `_1m` version. nyc_taxi_trip_duration then needs one (see "A `_1m` version
  of nyc_taxi_trip_duration" below).
- **Decide pkdd_15's trips that end where they start like nyc's.** nyc_taxi_trip_duration drops its 4,539 trips whose
  drop-off coordinates equal the pickup coordinates (USE-7, Must: a named destination is never the pickup point, so
  the row lacks the input the ETA acts on; mean target 6.04 against 6.47). **Answer (AI, 2026-10-20):** done in
  pkdd_15_taxi_trip_time_prediction_ii_1m: its definition now drops the 90 trips whose end point equals the start
  point (USE-7), and like nyc it keeps the trips that end near the start but not at it (CLEAN-11); its old issue 3 is
  settled (pkdd review panel, mediator, 2026-10-20). Both folders are still AI drafts that cite each other; the
  proposal to settle the two taxi folders in one sitting stands.
  **Resolved (2026-10-21, Lennart):** done earlier.

### Probes (from the huntprohibited review)

- **The near-copy check of the hidden-group probe cannot see copies of text.** It turns each row into one token per
  column value and clusters only rows that share at least `COPY_MIN_SHARED` (10) tokens. A table with fewer
  informative columns leaves every row single, and a text column is one token, so an edited repost of a description
  never matches. On huntprohibited_1m (9 features) the probe left all 1.5M rows single and its near-copy share read
  0.0%; exact keys on the description found a near copy in train for 1.4-4.9% of the test ads (split audit,
  2026-10-20). A "0.0%" from this check is therefore no evidence on a narrow or text-heavy table (EV-3); whether
  the copy checks of the other text datasets (emscad, consumer_complaints_1m, mercari_price_suggestion) lean on it is
  not checked. Proposal: report the check as not run when no row reaches the token floor, and add an exact key on
  each normalised text column (as SPLIT-24 allows); then re-run the probe on the text datasets. The probe library
  changes; no definition does.
  **Resolved (2026-10-21, Lennart):** the near-copy check reports "not run" when no row reaches the token floor (32
  of 173 datasets), and each string column of 3 or more words gets an exact key on its normalised text. No text key
  is a hit: huntprohibited_1m's description key holds 3.3% of the rows (gap 0.001), matching the split audit;
  emscad's keys sit inside its known group.

### Rules from the open_university review

- **Narrow LEAK-10's "earlier grades" row to grades not yet known at the prediction point?** The Mechanisms table of
  LEAK-10 (Must: a part or another encoding of the target is dropped) lists "earlier grades when the target is the
  final grade: drop it", with student_portuguese_performance as its case (G1 and G2 dropped, because its prediction
  point comes before those period grades). Two datasets of the copy keep earlier grades because they are known at
  their prediction point and the actor acts on them: predict_students_dropout_and_academic_success keeps the
  first-year grades (Lennart and Andrej, TabArena v0.1), and open_university_learning_analytics_dataset keeps the
  assessment marks returned by day 60, which carry 10-30% of the continuous-assessment weight of the final result (its
  issue 11). As written, the row says to drop both; the fact that sets the cases apart is whether the grade is known
  at the prediction point, which LEAK-10 itself already asks (open_university review panel, precedent check and
  mediator, 2026-10-20). Proposal: reword the row to "earlier grades not yet known at the prediction point: drop
  them", so the two kept datasets need no exception. The rule file changes; no definition does.
  **Resolved (2026-10-21, Lennart):** the row now reads "earlier grades not yet known at the prediction point: drop
  them".

### Rules from the glioma_grading review

- **Is a cross-check of a label that already exists a use case (USE-1)?** glioma_grading_clinical_and_mutation_features
  predicts the histological grade, which the pathologist has read from the tissue before the DNA is sequenced, so its
  use case is a lab that checks the grade against the mutation profile and flags a disagreement for review. Every
  diagnostic precedent predicts before the label exists (eryhemato_squamous_disease, lung_cancer_epithelial_genexp,
  sdss_17, breast_cancer_prediction), and no Cases row of USE-1 covers a cross-check (glioma review panel, precedent
  check and mediator, 2026-10-20). Whatever the curator decides on glioma's issue 5 sets the reading for any later
  dataset whose label is known at the prediction point. Proposal: once glioma's issue 5 is decided, record the answer
  as a Cases row of USE-1 (option b: a cross-check is a weak use case; option c: a kind of use case of its own), or
  amend USE-1/USE-3 (option d). The knowledge files change; no
  definition does.
  **Deferred (2026-10-21):** waits on glioma_grading's issue 5.
- **A USE-5 Cases row for a label right in its era but renamed later.** glioma_grading keeps TCGA's histological
  grade of 1989-2013, which WHO 2021 partly renames; corporate_credit_rating was retired under USE-5 (2026-10-16)
  because its labels were wrong for their own date and repairable from the origin (glioma review panel, 2026-10-20;
  glioma's issue 1). Other TCGA-era labels, such as tcga_kidney_cancers if it is added, raise the same question.
  Proposal: once glioma's issue 1 is decided, add the reading as a USE-5 Cases row ("a label correct under the
  criteria of its era, renamed later: kept with a note"). The knowledge files change; no definition does.
  **Deferred (2026-10-21):** waits on glioma_grading's issue 1.
- **Decide sarcoma's and glioma_grading's tissue-site question alike.** Both are TCGA sets whose tissue source site
  carries the label (glioma: 45 sites, each pure in the label) and both ship a random split by patient. In glioma the
  features do not predict the site (below the majority rate within each grade) and holding sites out leaves the mean
  per-fold ROC AUC unchanged (random forest 0.927 against 0.924); in sarcoma the hospital is weakly visible from the
  features (ROC AUC 0.70-0.75 overall, 0.69-0.73 within dedifferentiated liposarcoma) and holding sites out raises the log loss from 0.64 to 0.77 (sarcoma's issue 4; glioma
  split audit and precedent check, 2026-10-20). The measured visibility of the site is the fact that sets the two
  apart. Proposal: decide sarcoma's issue 4 with that fact written as the reason, and check glioma's split against the
  decision.
  **Deferred (2026-10-21):** waits on sarcoma's issue 4.

### Rules from the distribution_transformers review

- **Amend LEAK-10 for a looked-up attribute that changed for an unknown subset of positives?** LEAK-10 (Must) drops
  attributes looked up after the outcome "unless the data shows they did not change". The datasets kept so far meet
  that clause or remove the changed values: house_sales keeps its assessor record because the about 145 rows that
  changed after the sale carry nothing measurable, melbourne_housing_market keeps `Bedroom2` because it equals `Rooms`
  in 98-100% of the rows, and zillow_prize blanks the tax delinquency looked up after the sale. In
  distribution_transformers_at_cauca_department the clause fails and no record isolates the change: the inventory was
  taken during or after 2020, none of the 163 replacement-marked first burns of 2020 is rated 5 kVA (against 9% of the
  other 277), and there is no replacement log to blank by. Its definition now drops `power_kva` and
  `installation_type` (ROC AUC 0.639 without them; the panel measured about 0.06 more with them), and the advocate asks
  for an amendment: "a looked-up attribute that changed for an unknown subset of positives is kept with a note
  when no record can isolate the change" (distribution_transformers review panel, precedent check and mediator,
  2026-10-20). This differs from "Keep a post-outcome lookup because removing it changes no score?" above: here
  removing the columns does change the score. Options: (a) keep LEAK-10 as written: the columns stay dropped; (b)
  adopt the amendment, cite LEAK-10 in the note instead of "kept on purpose", and grade the fit with the item "Does a
  weak potential leak kept on purpose make a fit `approximate`?" above (USE-8). Proposal: (a);
  the "unless" clause already serves the cases where the data can show the change is harmless, and (b) would admit a
  gain that sits on the replacements.
  **Resolved (2026-10-21, Lennart):** (a): LEAK-10 stays; the two columns stay dropped (a Cases row records it).

### Rules from the pkdd_15_taxi_trip_time_prediction_ii review

- **Check SPLIT-9 on the TabReD ETA sets.** delivery_eta_1m, maps_router_eta_1m and cooking_time_1m ship weekly test
  windows with no gap (`TemporalSplits(window=7, unit="days", n_windows=3)`), though SPLIT-10 names a delivery time
  as its first example of a label that arrives late. SPLIT-9 (Must) keeps out of training every row whose label is not
  yet known at the window start. nyc_taxi_trip_duration found 77 to 127 such trips per window and pkdd_15 48, 36 and 8;
  both now take a one-day gap, measured 0 after (nyc and pkdd review panels, precedent check and mediator,
  2026-10-20). For the three TabReD sets the late labels were never measured, so they are an unchecked precedent, not
  a decision. Proposal: count, per window, the training rows whose order or trip ends after the window start (when
  the files give an end time or a duration), and add a gap where the count is above zero.
  **Resolved (2026-10-21, Lennart):** cooking_time_1m (108-172 late training orders per window) and
  maps_router_eta_1m (578-656) now have a one-day gap, which brings them to 0; delivery_eta_1m has none late (orders
  stop overnight).

### Rules from the credit_card_customers review

- **PROV-3 evidence standard: when are measured marks of generated data enough without a source statement or a
  generator?** PROV-3 and SEL-16 (Must) retire generated data, and EV-6 (Should) leaves a borderline case as "maybe"
  for the curator, but no rule sets the bar when the source says nothing and no generator is written down. Every
  dataset retired under PROV-3 so far had a mechanism, a generator or a source statement, or label-linked artefacts
  (homeq_default_prediction). credit_card_customers has several calibrated marks (the 12-month count equals Q4 + Q1 in
  every row; inactivity and spend independent of activity where real card tables are not; tenure set by age) but weak
  label-linked tests (label-free distance AUC 0.559; test 5 without a sign change), and its source is offline
  (credit_card_customers review panel, mediator, 2026-10-20). The same standard binds hepatitis_c_egypt (AI
  recommendation of `No` + `AHDS`, not a decision, so not a precedent) and stroke_prediction (only if its issue 5
  keeps it), the other two datasets with measured marks; framingham_heart_study_fhs, where no test fires, passes either bar (its owner's disclosure
  control is the separate question "Amend PROV-3 for an owner's disclosure control" above). Ways out: (a) "N calibrated marks from at least two PROV-3 tests are enough without a generator"; (b)
  "without a generator, the marks must predict the label (test 5 or 7)". Either way, amend PROV-3 and EV-3 in
  provenance.md and evidence.md, and decide the three datasets in one pass; credit_card_customers' issue 1 asks for it.
  Open wording question for (a): do the marks count on the file as published, or only on the columns we ship? It
  decides stroke_prediction: after the three columns that carried nothing beyond age were dropped, its shipped
  columns keep only marks of uneven distributions (glucose, ages 78 to 82), none linked to the label (the spike at 65
  is no larger among patients with a stroke than among those without, p 0.45); its issue 1 applies the answer if its
  issue 5 keeps the dataset.
  **Lennart (2026-10-21, discuss):** we can keep it case by case but work towards having both a and b imo, it is
  hard to tell in general
  **Answer (AI, 2026-10-21):** draft: "Without a source statement or a written-down generator, measured marks are
  judged case by case. The strongest case has both (a) calibrated marks from at least two PROV-3 tests and (b) marks
  linked to the label (test 5 or 7). With only one of the two, the curator decides, and the record says which is
  missing." Two questions before it goes in: is one of (a) or (b) enough to retire, or only both? And do the marks
  count on the file as published or on the columns we ship (this decides stroke_prediction)?
  **Lennart (2026-10-21, discuss):** either might be strong enough; on the columns we ship, and if the marks on the
  published file leak/extend to the shipped version (which is again case-by-case)
  **Resolved (2026-10-21, Lennart):** PROV-3 and EV-3 amended in your words: either kind of mark can be strong
  enough; they count on the shipped columns, and marks on the published file count when they extend to the shipped
  version, case by case. credit_card_customers' issue 1, stroke_prediction's issue 1 and hepatitis_c_egypt's block
  say what that means for each and stay open for you.
- **Amend PROV-1/PROV-2 for a named course or teaching platform.** PROV-1 (Must) allows no exceptions, yet
  bank_customer_churn (data from a named data-science course) and tour_travels_churn (a bare Kaggle upload with no
  named origin) were kept; credit_card_customers (Analyttica's LEAPS teaching case 11, offline) and mobile_churn (an
  anonymous Kaggle upload of 2019 with no description, no other datasets by the uploader and no churn rule) are open on
  the same question (review panels of both, precedent checks, source search and mediators, 2026-10-20). Course churn
  data that also looked generated went `No` (customer_churn_dataset, predictive_analytics_for_customer_churn_dataset,
  ibm_telco_customer_churn), as did water_quality_and_potability under PROV-1 although its data were judged sound.
  Proposal: widen PROV-2 to "a named first platform (a course or teaching provider) counts as a known source when the
  data shows no PROV-3 marks", worded to fit the PROV-3 evidence standard above; it covers credit_card_customers and
  bank_customer_churn. tour_travels_churn and mobile_churn name no platform, so keeping them needs a wider wording, for
  example "an untraceable first upload stays when the data passes PROV-3, the prediction point and label timing are
  measured on the data, and the gaps (source, label rule) are written as an approximate fit with a potential-leak
  note", which must also say whether an undefined label rule is allowed. Otherwise those two are `No` with `Missing
  source information`. Decide the wording once for all four datasets (and newspaper_churn the same way);
  credit_card_customers' issue 3 and mobile_churn's issue 1 ask for it.
  **Resolved (2026-10-21, Lennart):** PROV-2 widened for a named course or teaching platform with no PROV-3 marks
  (credit_card_customers, bank_customer_churn). tour_travels_churn and mobile_churn are the item "Sources with no
  named platform" below.

### Rules from the fraud_detection_in_electricity_and_gas_consumption review

- **Amend LEAK-25 so that unrecorded labels located and dropped count as "recovered"?** LEAK-25 (Must) says that
  "no event" mixed with "not recorded" is retired "unless the recording process can be recovered"; its one case,
  ghanas_indigenous_intel (Lennart, 2026-10-01), was retired, but there the unrecorded rows could not be located and
  the task was also `Too Small`. Three datasets locate the unrecorded rows by a rule that never reads the label row by
  row, drop them, and ship the rest: caracas_cervical_cancer (shipped by Lennart, 2026-10-15: 108 patients who
  skipped the contraceptive question, 0 positive results where 11.8 were expected), account_debt_south_africa (open,
  its issue 1: eight file runs without debt data) and fraud_detection_in_electricity_and_gas_consumption_1m (open,
  its issue 2: 19,133 STEG clients who left before 2013, 21 frauds or 0.11%, and with the follow-up filter 2,343 who
  left in 2013-2014, 4.7%, against 7.8% for the clients kept). A Must allows no exceptions, so the three need the
  rule's wording, not three silent departures (STEG review panel, precedent check and mediator, 2026-10-20). Ways
  out: (a) amend LEAK-25 so that "recovered" covers "located by a rule that does not read the label, and dropped",
  with the three as Cases; (b) retire the two open datasets like ghanas; (c) reopen caracas to match ghanas. The two
  open datasets wait for this decision.
  **Lennart (2026-10-21, go ahead):** do (a)
  **Resolved (2026-10-21, Lennart):** (a): LEAK-25 amended; account_debt_south_africa's issue 1 and
  fraud_detection's issue 2 now ask only for your ok on the drop.

### Tags (from the credit_card_customers review)

- **Define `2ndTierData` or drop it?** The schema's tag ("not of the highest quality but still a reasonable task") is
  defined in no knowledge file, yet it is used as an outcome: credit_card_customers carries it from the v1 migration,
  coffee_rating_prediction carries it. A
  tag cannot stand in for a Must such as PROV-3: a dataset is either retired or shipped with its doubts written as a
  finding (credit_card_customers review panel, precedent check and mediator, 2026-10-20). Ways out: (a) define it in
  the knowledge files (what earns it, what a benchmark run does with it) and apply it alike; (b) drop it from the
  schema and the definitions. Proposal: (b), unless the runs are to weight or filter by it.
  **Lennart (2026-10-21, go ahead):** Do (b), we have this now with use case fit more or less
  **Resolved (2026-10-21, Lennart):** (b): new definitions may not set `2ndTierData`; it stays readable because a
  shipped BeyondArena container (coffee_rating_prediction) carries it. Removed from credit_card_customers and
  coffee_rating_prediction.

### Rules from the diabetes_3 review

- **USE-5 for a label whose quantity no source documents: a reading or an amendment?** USE-5 (Must) says "check how
  the source built its label before accepting it", but neither its text nor its Cases say whether a label that cannot
  be checked fails it; the cases decided so far rest on a measured mismatch (corporate_credit_rating, 17% of the
  checkable labels wrong). diabetes_3 (Efron et al. 2004, the authors' own file) has a label described only as "a
  quantitative measure of disease progression one year after baseline", with no measure, scale, clinic or inclusion
  rule anywhere; mobile_churn has no churn rule; blood_tests_drink_prediction was kept as approximate, but there the
  quantity (drinks per day) is known and only its recording is not, so it is a partial precedent (diabetes_3 review
  panel, precedent check and mediator, 2026-10-20). A Must allows no exceptions, and a third keep makes the wording
  due. Ways out: (a) read USE-5 as met when the label comes from a peer-reviewed paper whose named authors publish the
  rows, shipped with `fit="approximate"` and a note; (b) amend USE-5, for example "a label from a named publication
  whose construction is undocumented may ship with `fit="approximate"` and a note naming the gap", saying whether it
  covers an unknown quantity (diabetes_3) or only an unknown recording (blood_tests_drink_prediction). Either way add
  the three as Cases. The panel proposes neither over the other; both sides prefer either one to retiring diabetes_3. A keep of mobile_churn also needs the item "Amend PROV-1/PROV-2 for a named course or teaching platform", whose wider wording must say whether an undefined label rule is allowed: that is this question. diabetes_3's issue 1 decides this item.
  **Lennart (2026-10-21, go ahead):** In general, I would like to keep the data and just mark it as approximate, and
  we can case-by-case decide the details
  **Resolved (2026-10-21, Lennart):** USE-5 amended: an undocumented label from a named publication ships
  approximate with a note naming the gap, case by case; diabetes_3's issue 1 is settled.

### Rules from the digicow review

- **Which rule asks for a note on a known input that tracks a dropped post-outcome column?** In
  digicow_farmer_training_adoption_challenge, `topics_list` (the day's topics, known at the prediction point, so kept
  under LEAK-37, Must) predicts the dropped flag `has_topic_trained_on` (whether the farmer was trained on the topic;
  dropped under LEAK-10 because it is recorded together with the adoption) with ROC AUC 0.885-0.902. The definition
  gives it a `Potential leak, kept on purpose:` note, but no rule asks for one: LEAK-30 covers transforms over all rows
  and LEAK-38 anonymised fields only, so the note borrows LEAK-38's format by analogy (digicow review panel, mediator,
  2026-10-20). Nothing changes for digicow while it is recommended `No`; the next dataset with such a column faces the
  same question of which rule to cite. Ways out: (a) leave it as a precedent; (b) widen LEAK-38 to host-released fields
  that may carry a post-outcome signal (an amendment). Option (b) overlaps option (a) of the item "Consistency check:
  LEAK-38 and kick's `WheelType` after expresso's REGION drop", so one amendment of LEAK-38's scope can settle both.
  Optional: no dataset waits on it.
  **Resolved (2026-10-21, Lennart):** (a): kept as a precedent (a Cases row names the pattern).

### Rules from the differentiated_thyroid_cancer_recurrence review

- **Does an unverified label definition alone make a fit `approximate` (USE-8)?** USE-8 (Must) lists "a label
  without a stated horizon" among the gaps of an approximate fit, but says nothing of a label whose breadth is
  unverified. differentiated_thyroid_cancer_recurrence's `Recurred` seems to count persistent disease (all 32 patients
  of the American Thyroid Association's high-risk class recurred) and the paper that would define it is paywalled; UCI
  states at least 10 years of follow-up, while the cohort paper (Khazaei et al. 2024) gives the period 2008-2023. Its fit reads `approximate` already,
  because `M` is a potential leak kept on purpose, so the answer decides only whether the fit goes back to `direct`
  if the paper clears `M` but not the label. churn_telco_south_asia (undocumented label timing) and thyroid_discordant
  (undefined label) read `approximate`; glioma_grading_clinical_and_mutation_features moved there in this run
  (differentiated_thyroid_cancer_recurrence review panel, precedent check and mediator, 2026-10-20). The critic reads a
  horizon the sources contradict and a label broader than described as a gap; the advocate reads UCI's stated horizon
  as enough and the label as the guideline's target under either reading. Ways out: (a) amend USE-8 to say an
  unverified label definition is a known gap that makes the fit approximate; (b) amend it to say it is not, when every
  reading of the label is the target the actor acts on. The panel proposes neither. Related: the sarcoma item "Does a
  weak potential leak kept on purpose make a fit `approximate`?" above, which asks the same of the other half of this
  fit, and the diabetes_3 item "USE-5 for a label whose quantity no source documents: a reading or an amendment?",
  whose two ways out both ship such a label as `approximate`: deciding that item answers this one. No dataset waits
  on it.
  **Lennart (2026-10-21, go ahead):** as above, yea it does
  **Resolved (2026-10-21, Lennart):** USE-8 amended: a label definition the sources do not settle makes the fit
  approximate; differentiated_thyroid_cancer_recurrence's fit rests on it.
- **thyroid_discordant's `Trivial` marker was never tested under TP-4.** TP-4 (Must) says `Trivial` needs proof, a
  test fold by fold of the best single feature against the methods. thyroid_discordant ships with a `Trivial` marker
  taken from a curation comment ("It still seems trivial", after a simple test on another target, Hypothyroid), and its
  definition says the curators found the task close to
  trivial; no TP-4 test was run. In this run the marker is refuted on TP-4 evidence for
  differentiated_thyroid_cancer_recurrence (the risk class alone gives ROC AUC 0.896; a random forest beats it on 59
  of 60 splits), diabetes_3 (a field row) and house_prices_nominal (issue 3, "Remove the `Trivial` marker?")
  (differentiated_thyroid_cancer_recurrence review panel, precedent check, 2026-10-20). A precedent that contradicts a
  rule is flagged, not followed. Ways out: (a) run the TP-4 test on thyroid_discordant and keep or remove its marker by
  the result; (b) record why the marker stands without the test. Those three are settled in their own files by their own tests; this item asks only about
  thyroid_discordant.
  **Resolved (2026-10-21, Lennart):** (a): `FTI` alone gives ROC AUC 0.822 against 0.974 for a random forest, lower
  on 30 of 30 splits, so the marker is refuted; thyroid_discordant's REVIEW.md issue 1 asks you to remove it.

### Rules from the numerai_v5_2 review

- **Amend LEAK-31 for a selection the source published?** LEAK-31 (Should) keeps a feature selection made with labels
  that include test rows with a note when small and removes it when we can; its only case, home_credit_default_risk,
  removed the selection even at zero effect (Lennart, 2026-10-19). Three definitions keep a selection their source
  published: qsar_oral_toxicity (the fingerprint settings, read as very weak), qsar_bioconcentration (the authors' 9
  descriptors, at most about 0.015 macro ROC AUC; its issue 5) and numerai_v5_2 (the 75 Faith features Numerai released
  at era 1192 and designed with the targets of test weeks (eras) 1080-1191: ridge gains +0.0043 per-week correlation
  with the target in 1080-1131, about 28% of the signal there, and +0.0010 after the release; its issue 3). The
  qsar_bioconcentration review proposed the amendment "a selection the source published stays with a note when small"; a
  third keep makes it due rather than a third exception (numerai_v5_2 review panel, precedent check and mediator,
  2026-10-20). numerai's case would not meet "when small" in its oldest window. Proposal: decide the three alike; the
  panels recommend dropping the selection in qsar_bioconcentration and numerai_v5_2, so the amendment is needed only if
  you keep them.
  **Lennart (2026-10-21, leave as is):** keep it case by case
  **Resolved (2026-10-21, Lennart):** no amendment; LEAK-31 says a selection the source published is decided case by
  case.

### Rules from the african_credit_scoring_challenge review

- **Amend EV-4, or keep every licence a one-line note?** EV-4 (Must) makes a licence a one-line note and never an
  issue for the curator, yet the earlier reviews of numerai_v5_2 (issue 1), aeolus (issue 5),
  corporate_credit_rating_cat (issue 5) and african_credit_scoring_challenge (issue 5) raised it as one; their current
  review files carry it as a note (numerai_v5_2_1m in its record judgment). digicow, with the
  same "Zindi Competition Rules" and a participant's copy of the files, raised none
  (african_credit_scoring_challenge review panel, precedent check and mediator, 2026-10-20). In
  african_credit_scoring_challenge the licence is a note in the outcome; all four files now carry the licence as a
  note. Ways out: (a) keep EV-4 as it stands, with the Zindi rules' "private property of the client" as a
  release-checklist item; (b) amend EV-4 to allow one release note per dataset, never a verdict reason.
  corporate_credit_rating_cat, mortgage and lgd carry the same Credit Risk Analytics terms (no commercial use, no
  redistribution) as a one-line note each; under (b) the three take one note together.
  **Resolved (2026-10-21, Lennart):** (a): EV-4 stays; the licence terms are release-checklist items.

### Rules from the corporate_credit_rating_cat review

- **When is a rating or grade target regression, and when classes?** No rule says when an ordinal target ships as a
  number. wine_quality (0-10 grade) and numerai_v5_2_1m ship regression because their sources model it so;
  corporate_credit_rating was framed as 6 letter classes with the rare grades merged or dropped (carried into
  corporate_issuer_credit_rating, CC 2026-10-16); corporate_credit_rating_cat ships its 1-10 rating code as
  regression because its source scores an ordered logit by notch distance and only "1 = AAA" is known (its issue
  2). Each acceptance of the check warning for a numeric target with few values (`task_target_low_cardinality`)
  rests on a different fact, so the two credit-rating tasks
  can drift apart (corporate_credit_rating_cat review panel, precedent check and mediator, 2026-10-20). Proposal:
  a short rule in TP-7 or USE-5 (for example: regression when the source scores by distance or models a number,
  classes when the source's classes are known and a field convention merges the rare ones), with these four as
  its Cases rows. Deciding corporate_credit_rating_cat's issue 2 first gives the rule its fourth case.
  **Lennart (2026-10-21, leave as is):** In general, we decide this by the source but also check the soruce against
  common sense and best pratices in similiar use cases, so it reamins case by case
  **Resolved (2026-10-21, Lennart):** left case by case, as you wrote: by the source, checked against common sense
  and the practice of similar use cases.

### Rules from the stroke_prediction review

- **SEL-7 scope for has-had labels.** **Resolved (2026-10-20):** decided in stroke_prediction's issue 5 (options (b)
  and (c) there).

### Follow-ups from the marks of 2026-10-21

- **Strong kept leaks and the fit.** USE-8 as amended (a kept leak alone does not make a fit approximate) also moves
  kick and homesite_quote_conversion to `direct`, though their kept fields carry a large signal (ROC AUC +0.066 and
  +0.050). kick is now `direct`, pending its issue 1. Should a strong kept leak still make the fit approximate? The
  answer also decides the fit labels not yet changed: homesite_quote_conversion, qsar_aquatic_toxicity and
  onlinenewspopularity would read `direct`; perth_house_prices, credit_card_customers, african_credit_scoring_challenge
  and zillow_prize stay approximate, and their `fit_reason` would stop counting the kept leak as a gap.
  **Resolved (2026-10-21, Lennart):** applied: homesite_quote_conversion, qsar_aquatic_toxicity and
  onlinenewspopularity read `direct`; perth_house_prices, credit_card_customers, african_credit_scoring_challenge
  and zillow_prize stay approximate without counting the kept leak; perth's issue 1 is settled.
- **Sources with no named platform.** Under PROV-1 as written and PROV-2 as widened, tour_travels_churn (shipped) and
  mobile_churn name no first platform and would be `No` with `Missing source information`, like
  water_quality_and_potability. Keeping either needs a wider wording (an untraceable upload that passes PROV-3, with
  the gaps written as an approximate fit). Retire both, or widen the rule?
  **Lennart (2026-10-21, discuss):** it is still case by case, if the data looks good enough even without a good
  source but there is a source, we want to keep it for now and risk it
  **Resolved (2026-10-21, Lennart):** PROV-2 amended as you wrote: a sound upload (passes PROV-3) with a source to
  point to is kept for now, case by case, as an approximate fit with a note. tour_travels_churn stays (the
  generated-data probes raise nothing); mobile_churn's issue 1 and credit_card_customers' issue 3 are settled.
  water_quality_and_potability is now out of line; see the new item below.
- **A `_1m` version of nyc_taxi_trip_duration.** Its train sides hold 1.28M to 1.39M rows, above the 1M budget. Under
  the reworded definitions.md it ships as `nyc_taxi_trip_duration_1m` (a new folder with `version_of` and
  `subsample_to_budget`, as delivery_eta_1m). Create it?
  **Resolved (2026-10-21, Lennart):** done: the folder is now `nyc_taxi_trip_duration_1m` (1,166,477 rows, 1M rows
  per train side, the same test windows).
- **Metrics still to settle.** expresso_churn_prediction_1m (the first competition, UmojaHack Ghana 2020, scored log
  loss; its 2021 re-run with the same files scored AUC), hiva_agnostic (probably the balanced error rate, not
  verified), aps_failure (a cost of 10 per false positive and 500 per false negative on hard labels), coil_2000
  (policy owners among the top 800), rossmann_store_sales (RMSPE, not a registered name) and churn_telco_south_asia
  (unknown). Also: african_credit's F1 and force_2020's penalty matrix score hard labels; the sources give no evidence
  that this is wrong, so both stay declared. digicow declares log loss although its panel measured that log loss there
  tracks the trainers' recording waves; that is our measurement, not the source's. Keep these as they are?
  **Resolved (2026-10-21, Lennart):** kept as they are (your ok).
- **Small rule questions.** (1) Refuse `ForcedIIDFromTemporal` on a grouped or temporal split, as the new grouped tag is
  refused on an IID one? (2) CLEAN-14's categorical convention covers a molecule's 0/1 flags only; extend it to every
  0/1 flag (mercedes' options are int)? (3) Does CLEAN-11's "with the source's words" also bind its second clause (a
  single extreme training target)? If so, mercedes' drop has no source words. (4) maps_router_eta_1m's gap assumes
  `track_length` is in metres (minimum 1,000.0; in km drives would last thousands of hours).
  **Lennart (2026-10-21, go ahead):** (1) yes, (2) yes we should have one clear way to treat 0/1 flags, (3) no it
  also bind to what experts did by default, so again more complicated case by case, (4) check this error for track
  length and how often it occurs
  **Resolved (2026-10-21, Lennart):** (1) `ForcedIIDFromTemporal` is now refused with a grouping or temporal split
  (validation and bundle check); no definition breaks. (2) CLEAN-14 amended: every 0/1 flag, booleans included, is
  categorical after a check on the data; 35 definitions changed (the list is in the CHANGELOG). (3) CLEAN-11
  amended: a single extreme training target may leave with the source's words or where experts of the field drop it
  by default, case by case; mercedes cites it. (4) `track_length` is in metres (in km the median drive would last
  194 h); 31 of 13.6M rows look implausible and none of them is late, so the one-day gap stands and no row is
  cleaned.
- **drug_induced_autoimmunity_prediction: two descriptors mark groups of molecules.** The hidden-group probe, now
  taking float columns, finds `SMR_VSA10` (gap 0.172) and `SMR_VSA7` (gap 0.112) against a random-split skill of 0.657
  on this IID task of 587 molecules: about 2 molecules per value, so they may mark analog series (hidden-group sweep,
  2026-10-21). Proposal: check the source's structures (SMILES) for duplicates and analog series, and group the split
  on the series if the gap holds there.
  **Lennart (2026-10-21, go ahead):** Yes do so, it likely is a grouped dataset, in the open PRs, there is a finding
  from Andrej on this as well
  **Resolved (2026-10-21, Lennart):** done: the working copy now groups the split on the Bemis-Murcko scaffold
  (443 groups), taken from Andrej's PR #15 with its helper and tests, as you asked; PR #15 is to be updated later.
  Scaffold-grouped ROC AUC 0.771 against 0.826 random (LightGBM). The two descriptors do not mark the scaffolds
  (adjusted Rand 0.04 and 0.08); their gap comes from the value 0 landing in one fold. No duplicate structures.
- **water_quality_and_potability against the amended PROV-2.** It was retired in the v1 workbook for its untraceable
  source alone; no PROV-3 test is on record, and nothing written sets it apart from mobile_churn or
  tour_travels_churn, which PROV-2 as amended now keeps. Ways out: (a) re-check it with the PROV-3 tests and keep it
  if they raise nothing; (b) name the fact that sets it apart and record it.
  **Lennart (2026-10-21, go ahead):** recheck it and add it for me to be verified here, if it passes otherwise
  **Resolved (2026-10-21, Lennart):** rechecked: it fails PROV-3 (the first upload of 2021 names its source
  "Synthetically generated"; dissolved solids run about 50 times the conductivity, Spearman 0.021; 1,277 of 1,278
  potable rows exceed 1,000 mg/l). It is on the review page for you to verify, as the record's issue 1
  (recommendation: keep No and add `AHDS`).
- **Which 0/1 columns are flags?** Applying CLEAN-14 literally also made categorical some counts that hold only 0 and
  1 in this data (RDKit fragment counts in apistox, `NoOfURLRedirect` in phiusil_phishing, sberbank's
  `mosque_count_*`, coil_2000's count columns, cardiotocography's `DS`), and left constant 0 or 1 columns as they are
  (for example `ca` in the two heart_disease sets, homesite's `PropertyField6`). Ways out: (a) keep it literal, as
  now; (b) a flag is a yes/no by meaning, so counts stay numeric even when only 0 and 1 occur (those five folders go
  back). Either way the rule text would say that a constant column is not a flag.
  **Lennart (2026-10-21, discuss):** no if we can infer from the semantic context, keep it a number, this is a real-
  world bias. We want to make thins categorical if we know from the context they are indeed such
  **Resolved (2026-10-21, Lennart):** CLEAN-14 amended in your words: a 0/1 column is categorical when its meaning
  says it is a yes/no flag; a count or a measured quantity stays numeric even when only 0 and 1 occur; with no
  semantic context it stays as the source ships it; a constant column is no flag. 19 of this morning's 35
  definitions changed back in part or whole (fragment counts, `mosque_count_*`, coil_2000's counts,
  cardiotocography's `DS` and the anonymized columns of amex, ieee, homesite and bioresponse are numeric again); the
  other 16 typed only real flags. Two open doubts: home_credit_default_risk's `CC_NAME_CONTRACT_STATUS_*` min/max
  aggregates (reverted; a max of a one-hot reads as "ever had this status") and early_learning_predictors'
  `practitioner` and `quintile_used` (reverted for lack of a codebook).

### Follow-ups from the marks of 2026-10-22

- **Re-check stock and appliances_energy_prediction under the amended TP-10?** TP-10 now measures leg 1 by the
  task's declared metric and allows trailing summaries of the series as features, only no lag of the target column
  itself (Lennart, 2026-10-22, on g_research_crypto_forecasting). Both datasets were retired as `No` + `Time-series
  (Forecasting)` under the earlier wording (stock: an undated CC; appliances_energy_prediction: 2026-07-27), and both
  records also carry `Wrong Domain / Source Modality`, which the amendment does not touch. Ways out: (a) re-run the
  two legs on both and reopen any that passes; (b) leave both retired on their other marker. Nothing changes until you
  mark it.
  **Lennart (2026-10-22, leave):** leave both retired, we know from the context and data state that these are indeed
  forecasting tasks.
  **Resolved (2026-10-22, Lennart):** both stay retired as `No` + `Time-series (Forecasting)`; no re-check.
