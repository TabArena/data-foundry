---
unique_name: loan_default_prediction_imperial_college
name: Loan Default Prediction - Imperial College London (Kaggle 2014)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
decision_markers:
- Data Quality Issue
tags:
- Two-Regime Zeros
- Non-IID (Temporal)
original_source: Kaggle
year: '2014'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/loan-default-prediction
- https://www.kaggle.com/competitions/loan-default-prediction/discussion/6962
- https://www.kaggle.com/competitions/loan-default-prediction/discussion/7115
v2_path: datasets/_dev/tabarena-v0pt2/loan_default_prediction_imperial_college/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: the earlier `No` rested on two leaks measured on the data
that a definition can remove (drop the f527/f528 pair, never use the row order), so it is no fast reject (USE-12); it
stays secondary because the rows may be snapshots of one loan that end at its default, as in `iranian_churn`, which no
drop fixes.
- Source: Kaggle research competition "Loan Default Prediction - Imperial College London", 2014-01-17 to 2014-03-14
  (Kaggle API: "Constructing an optimal portfolio of loans"); an unnamed lender's data, "standardized, de-trended, and
  anonymized" (data page, earlier AI triage). Files train_v2 and test_v2 (Kaggle API); train_v2: 105,471 rows x 769
  anonymised features, `loss` 0 for 90.7%, else 1-100 (earlier AI triage, 2026-10-20, measured).
- Use case: for example, a lender or investor prices or selects a loan by its expected loss at origination; the host:
  "each row containing the header fact corresponds to ex-ante information available on either the individual getting the
  loan, based on his personal features, on his history, etc or on the loan" (Arnaud de Servigny, topic 6862); fit
  approximate (anonymised fields, unnamed lender). Regime temporal by the row order (earlier AI; the data page names no
  time).
- Siblings and duplicates: `loan_default_prediction_challenge` (Zindi, binary) and the other loan-default records are
  other data. External collections: none found.
- Papers and pages: topic 6962 (Kaggle removed 9 fields that "incorporate some ex-post information"; "If there's
  leftover leakage, it's fair game"), topic 7115 (the golden features).
- Metric: MAE (Kaggle API, "Mean Absolute Error"), the leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: f528 - f527 alone gives AUC 0.92 for a loss, as the removed pairs did (earlier AI): LEAK-38
  keeps an unverified anonymised suspect, but the host found ex-post aggregates of this kind, so a drop is the likely
  call; 96.5% of defaults are the last row of an f274 block (earlier AI): if a block is one loan's snapshots up to
  default, the features are anchored at the outcome (`iranian_churn`, retired with `Data Quality Issue`, Lennart,
  2026-10-01), which is why `Data Quality Issue` stays as the open concern; open family question: coded zeros (the host,
  topic 6862: "a few loans where there has been full recovery are with a zero loss").
- Priority: gap 0 (finance), use case 0 (none named), source 0 (a data page only; lender and fields anonymised), shape +
  (105,471 rows, 769 features), risk - (leaks, unclear row unit).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. The
verdict and priority stay: the leaks and `Data Quality Issue` are the screening's other risks.

**Consistency check (AI, 2026-10-30):** the review page sets `Yes`, priority 1 ("Give it your best to resolve the
leaks"). The leak that remains after dropping f527/f528 is the one `iranian_churn` was retired for (Lennart,
2026-10-01): 96.5% of defaults are the last row of an f274 block. Options: `Yes`, with /add-dataset testing whether f274
is a loan id and grouping or dropping it; TBD -> Yes until that test (as for `pricing_game_2015_french_mtpl`); or `No`
like iranian_churn.

CC (2026-10-30, Andrej): `TBD -> Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated
screening review page, after the AI's consistency check). "Give it your best to resolve the leaks. If an unresolvable
leak remains, explain it and move to No. If the iranian_churn leak and this one can be resolved in the same way then we
should resolve both"

**Assessment (AI, 2026-11-01):** the leak work the curator asked for ("Give it your best to resolve the leaks"), on
train_v2.csv (105,471 rows). Leak 1, the forum's golden features f527/f528 (topic 7115): a scan of all 227,475 pairwise
column differences finds only three above AUC 0.75 for a loss, all involving f527 or f528 (f274-f528 0.938, f527-f528
0.915, f274-f527 0.907; best single column 0.633). Consecutive rows of one entity are linked by running aggregates of a
hidden per-period quantity x: f274 is x of the previous period, and f527/f528 are moving averages that include the
current period, so the default's own period is recorded (x changes in 99.8% of default rows against 38.3% of the others;
the same kind of ex-post field the host removed, f462/f463 and f473/f474). Fix: drop f527, f528 and six sibling
aggregates (f529-f531, f534, f535, f537). After the drop no column's change from its previous row beats AUC 0.607 (f528
0.973, f527 0.931 before). LightGBM on three row-order windows: all columns with the golden differences AUC 0.998, R^2
of log1p(loss) among defaults 0.52; f527/f528 dropped 0.716 and 0.525; all eight dropped 0.718 and 0.524. Leak 2,
defaults at the end of f274 blocks: f274 is no id but x of the previous period (f275 = f274^2); a default changes x, so
the entity's next row falls into a new block; the 96.5% is leak 1 seen through the sort. Rebuilt entities: 32,152
chains, the row id increasing along 100% of links; a default does not end the entity (9.4% on a chain's last row and on
the others; 70.3% of default rows have a successor). Under a random split 34.6% of test rows have the same f274 at the
next period in training (flag AUC 0.689); with row-order windows 0.2% (AUC 0.501), and only 2.1% of chains cross the
cutoff (LEAK-34). On the fixed definition the probes are clean (depth-2/3 trees 0.628/0.636, missingness <= 0.54, no
exact copies, label-free distance 0.51). Both leaks are resolved: drop the eight aggregates, keep all rows, split by
row-order windows. Caveats: x is anonymised, so its timing is inferred from the mechanism; the record's claim that each
block ends at its default, like `iranian_churn`, is wrong; MAE cannot separate honest models from predicting zero (0.801
against 0.800), so /add-dataset chooses another metric. `iranian_churn`: a different mechanism (one row per customer,
features over a window ending at the churn month, no panel or row-order effect), so the same fix does not apply and it
stays retired.

CC (2026-11-01, Andrej): `Yes`, priority 1, by the curator's rule on the page ("Give it your best to resolve the leaks.
If an unresolvable leak remains, explain it and move to No. If the iranian_churn leak and this one can be resolved in
the same way then we should resolve both"): both leaks resolved (Assessment above); iranian_churn not resolvable the
same way, so it stays retired.

Kaggle research competition sponsored by researchers at Imperial College London (2014), data from an unnamed lender,
"standardized, de-trended, and anonymized" (data page). Target `loss`: 0 unless the loan defaulted, else the loss as
a percentage of the notional. Measured on train_v2.csv (2026-10-20): 105,471 rows x 769 anonymised features, 90.7%
zeros, 9,783 positives (integers 1-100, median 5), no missing or negative values. A host reply in forum topic 6862
says a default with full recovery also has loss 0. The rows are listed old to new, so a split would be temporal.
This is not `loan_default_prediction_challenge` (Zindi, a binary good/bad-loan task).

No for data quality. Mid-competition the host removed 9 columns that "incorporate some ex-post information" and
called any remaining leakage "fair game" (topic 6962). Two leaks remain. The difference f528 - f527 alone reaches
ROC AUC 0.92 for loss > 0, while untuned LightGBM on all raw columns reaches 0.72-0.73 (row-order, random and
f274-grouped 80/20 splits; R^2 0.53-0.55 on log1p loss among positives); a competitor noted that the removed pairs
f462/f463 and f473/f474 behaved the same way (topics 7115, 7398). And the rows are not independent loans: sorted by
f274 and f521, 96.5% of defaults are the last row of an f274 block (20.6% default rate there, 0.6% elsewhere), so a
sequence ends at its default, as in `iranian_churn`; that flag alone gives AUC 0.79, with the pair 0.94. The leak rules
keep unverified anonymised suspects (`homesite_quote_conversion`, `kick`), but here the host found ex-post aggregates of the same kind, and
with anonymised columns neither the prediction point nor the entity can be rebuilt. To check: whether a curator would
rather take TBD -> 2nd Tier with the pair and the id-like columns dropped. Terms: Kaggle rules, data for the
competition only.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/loan_default_prediction_imperial_college/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping as changed; issues 1 to 3 (the precautionary block, the gap, the metric's origin) are weighings, none a reason for `No`. Corrections to the Assessment above: "f275 = f274^2" holds in only 0.42% of rows (rank correlation 0.967); "both leaks resolved: drop the eight aggregates" was incomplete: the panel found 28 columns that record the entity's previous loan's loss after the fact (f221: ROC AUC 0.993) and f468, f471, f536, which record the loan's own period, so 33 measured leak columns go, 7 more as a precaution (the six and f533). The screening's iranian_churn concern is refuted: a chain's last row has a loss as often as its other rows (9.42% against 9.38%). Measured: the hurdle model's normalized Gini 0.196 (0.146 to 0.230), above 0 on 9 of 9 windows. `Data Quality Issue` stays until your mark on its removal. Priority 1: gap 0 (nothing thin), use case 0 (ours, fit approximate), source 0 (a data page; lender and fields anonymised), shape + (105,471 loans, 638 features, temporal), risk - (leak timing inferred on anonymised fields; issue 1 open).

CC (2026-11-03, Andrej): issue 1, A: f529-f531, f533-f535 and f537 stay dropped with f527/f528 as one block.

**Exception to LEAK-10 (2026-11-03, Andrej):** unlike online_shoppers `PageValues` and account_debt_south_africa, kept once the data showed them behaving like history, the block stays out: aggregates of the same hidden x as two measured leaks (f527, f528), and with anonymised fields a test without labels is indirect. Serves P4 (honest evaluation) over P7.

CC (2026-11-03, Andrej): issue 2, A: the gap of 5,800 loans stays. Issue 3, B: "We go with B and can change the rule. If the source metric is bad we don't want to use it." The normalized Gini is declared from context under MET-11 as amended (an overruled source metric, the task making one obvious), not as an exception.

CC (2026-11-03, Andrej): ship (review page verdict); the declared metric, the normalized Gini from context, checked.

CC (2026-11-03, Andrej): the check warning `task_target_value_dominant` accepted: "for these tasks this is natural and a core challenge" (zero-inflated target).

CC (2026-11-08, Lennart): the declared metric (`normalized_gini`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

**Assessment (AI, 2026-11-08):** ships by default (no open issue on the PR #47 board), but the definition's changes of 2026-11-06 (the exposure paragraph) have not passed `dataset check`, and the re-review panel under LEAK-41 and MET-14 to MET-16 has not run: both wait for the competition files, which download only after the Kaggle competition rules are accepted. No container is built before both pass.

**Assessment (AI, 2026-11-08):** the competition files are in the warehouse, so `dataset check` and the re-review ran; the Assessment of 2026-11-08 above (both waiting for the files) is superseded. Changes from the panel, no decision needed: the check warning `dataset_missing_value_sentinel` is accepted, since -1 in f72, f586-f588, f648-f651 and f763 is a change of -100%, not a missing code (it predicts the loss differently from missing: f648 14.4% against 8.5%; CLEAN-10, a value kept as in home_credit_default_risk); the exposure bullet and `task_summary.predicted` mark "a share of the loan's amount" as our reading of the host's "loss = loss given default = scaled number between 0 and 100" (topic 6862), and the equal-notional sentence rests on that reading; the exposure bullet adds that the planned term varies by a factor of 1 to 3 and ships only as the maturity-range code f4 (MET-14); the metric reason adds that the Gini also leans on the tail (the 1% of loans with the largest losses hold 38-46% of a window's loss sum). `dataset check`: 0 errors, 0 warnings. The notes above that call the target "the loss as a percentage of the notional" give our reading too, not the host's words.

**Assessment (AI, 2026-11-08):** review panel (focused: claim auditor, column auditor, mediator; re-review under LEAK-41, MET-14 to MET-16, after the raw data arrived): ship after changes (wording and one accepted warning, now made); disputed: none; for the curator: issue 4 (remove `Data Quality Issue`; both auditors' data support B: `f528 - f527` ranks a loss at ROC AUC 0.916 on the raw file and is dropped, and a chain's last row has a loss in 9.42% of cases against 9.38%).

## Reference

Imperial College London and Kaggle (2014). Loan Default Prediction - Imperial College London. Kaggle research
competition, closed 2014-03-14, https://www.kaggle.com/competitions/loan-default-prediction.

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
