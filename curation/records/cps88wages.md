---
unique_name: cps88wages
name: cps88wages
checked_by:
- Myunghwan
data_foundry_status:
- WIP (DF)
claimed_by: Myunghwan
suggestion: 'Yes'
priority: 4
decision_markers:
- Outdated
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: Unknown (survey 1988)
domain: social science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/44984
- https://doi.org/10.1007/s001810000059
- https://search.r-project.org/CRAN/refmans/AER/html/CPS1988.html
v2_path: datasets/_dev/tabarena-v0pt2/cps88wages/dataset.py
source_row: 807
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 4: a real, documented CPS wage table, but built for
econometric specification testing, not for a decision (the curator's CC line and the TabArena reject point the same way).
- Source: March 1988 Current Population Survey (US Census Bureau), sample drawn by Bierens & Ginther (Empirical Economics
  26, 2001) for testing quantile-regression models; distributed as `CPS1988` in the R package AER and as OpenML 44984.
  As published: 28,155 men aged 18-70 x 7 columns: `wage` (target, deflated to 1992 dollars), `education`, `experience`
  (potential), `ethnicity` (cauc/afam), `smsa`, `region`, `parttime`. One table.
- Use case: no actor named by the source; the paper estimates a (median) wage equation, a returns-to-schooling question
  (USE-2). A use case the curation could write (an HR salary benchmark) would be approximate at best and uses 1988 data.
  Regime IID (one cross-section, one survey month).
- Siblings and duplicates: `census_income` (CPS 1994/95, income threshold, also `TabArena Reject`, TBD -> 2nd Tier) is a
  different survey year and task; no duplicate of this extract found. External collections: TabArena Reject, TabSTAR.
- Papers and pages: Bierens & Ginther 2001; OpenML 44984 ("The goal is to estimate the wage using information about
  working individuals"); the original page http://www.personal.psu.edu/hxb11/MEDIAN.HTM (offline).
- Metric: none found as a prediction metric (OpenML page, AER docs; the paper tests model specifications), so the
  fallback (RMSE on log wage would be the econometric habit).
- Risks for /add-dataset: few features (6), `ethnicity` as a sensitive input (the CC line); `Outdated` stays.
- Priority: gap + (social science thin), use case -, source + (paper, CPS documentation), shape + (28k rows, mixed types).

CPS 1988 wages dataset: predict (log) wage from census/survey demographic features. It is a genuine real-world tabular regression with a clear target, but it is outdated (1988) and is already in the TabArena Reject and TabSTAR collections, with a curation note questioning whether predicting wage from sensitive demographic features is desirable. These outdatedness and sensitivity concerns argue against first-tier inclusion rather than against task validity. A human should weigh the ethical/sensitive-feature angle, the age of the data, and whether a fresher CPS extract is preferable, plus confirm the row count.

---

CC: "predict wage based on census/survey data. again census data that is outdated, unclear if the task of predicting the wage based on the selected sensitive features makes sense"

CC (2026-10-26, Myunghwan): Accept historical wage estimation among comparable survey respondents, without future prediction, pay recommendation or causal framing; retain ethnicity as a predictor. Proceed to add-stage checks. Preserve established source evaluation unless measured evidence supports a change; no exact scorer or final ship decision was supplied. This supersedes the historical AI screening recommendation above.

**Assessment (AI, 2026-10-27):** Direct add-stage qualification is in progress. OpenML 44984 v2 matches all seven columns and all 28,155 rows of the AER CSV mirror. The target is raw weekly wage, not log wage. Source study LAD fitting and ICM specification tests do not establish a unique held-out predictive scorer. The executable RMSE fallback is provisional pending curator review. Claims board ownership remains Myunghwan; its existing triage-stage reservation is preserved. No build or commit authorized.

**Assessment (AI, 2026-10-27):** Qualification preserves 28,155 records and six predictors; fixed four nominal columns incorrectly marked ordered. Dataset check has zero errors and three unresolved warnings. Required task probes show LightGBM R2 0.274, linear 0.245, random forest 0.215 on five folds, with no flags; nine-fold scoring and duplicate-sensitivity diagnostics retained. Recommend retention subject to explicit scoring and duplicate decisions and the unresolved first-release-year disposition. The authorized local historical-estimation scope is broader than pinned SEL-3/USE-1/USE-2; no upstream amendment or final ship is claimed. Priority 4: gap + (social science), use case - (source specifies wage-equation research, not an operational decision), source + (paper and AER codebook), shape + (28k mixed-type records), risk - (no demonstrated leak or damaged target; identity and provenance limitations remain explicit).

CC (2026-10-27, Myunghwan): Retain all rows if different wages at matching profiles and train-only lookup checks do not suggest a dominant lookup shortcut. Release year does not affect the task; describe the survey year and treat unknown release year as nonblocking. Log error is a plausible relative-error choice; requested heuristic/model and low-/high-wage error-contribution checks before final scoring choice.

**Assessment (AI, 2026-10-27):** Follow-up conditions for retention are met: 99.74% of repeated profiles have multiple wages; 99.89% of held-out rows with matching training profiles have a different training wage available. Exact-profile log-median lookup log MAE 0.4661 versus modeled 0.3918 (nine actual folds), including worse performance on seen profiles alone. Retain all rows with identity uncertainty. Release-year question is closed by explicit local curator disposition, without claiming a verified first release. Same-model attribution: highest ~1% supplies 46.19% of squared-dollar error versus 3.20% of absolute-log error; lowest ~1% supplies 2.81% of absolute-log error. Recommend exact mean absolute natural-log error, pending approval and portable implementation. Earlier tiny-floor diagnostic is not an approved rule; raw-mean predictions include one nonpositive value. Only final scorer remains a scientific review choice; no final ship/build/commit approval inferred.

CC (2026-10-26, Myunghwan): Use log1p transformation of weekly wage and mean absolute error on that transformed target. This supersedes the earlier exact natural-log error choice and its requirement for positive raw-dollar predictions. Retain all rows, all six predictors including ethnicity, and the approved historical task and random split regime. Release-year uncertainty remains nonblocking.

**Assessment (AI, 2026-10-26):** Applied log1p only to the wage target; no raw-wage copy enters predictors. Declared context-origin portable mean_absolute_log1p_error with target_transform=log1p; scorer is exactly MAE on transformed targets/predictions, without clipping, squaring or raw-dollar MAE. Algebraic cancellation avoids inverse overflow for extreme transformed predictions. All 28,155 rows and six predictors retained. Recomputed canonical row order and actual IID3x3 memberships after target change; prior exact-log/raw-dollar diagnostics remain historical. Nine-fold log1p MAE: constant median0.55968, profile median0.46497, depth-three tree0.43561, LightGBM median0.39091; model beats lookup and small tree on every fold. Error shares: bottom tenth17.78%, middle65.38%, top tenth16.84%; bottom ~1%2.79%, top ~1%3.21%. Final scoring question is settled; no final ship/build/commit authorization is inferred.

**CC (2026-10-28, Myunghwan):** "ship all". Approved this dataset for shipping in the five-dataset final added-dataset review (beMTPL97, Eucalyptus, Tanzania tourism, CPS88 wages and OSSL), on the exact presented definition with previously settled task choices and disclosed limitations retained. This is scientific acceptance for a separately requested build; it does not authorize build, commit or publication.

**Assessment (AI, 2026-10-28):** The independent consistency check supports applying this overall verdict without another task choice. Existing local curator dispositions remain distinct from source verification or shared-rule amendments. No definition, scorer, data, fold or warning acceptance was changed by this final verdict.

**Maintenance (AI, 2026-10-29):** Publication-privacy cleanup removes acquisition/process details from descriptive metadata. Native format-2 rebuild `01a18ad7-7905-7c46-8544-db56a44113a9` verifies on reload and reproduces from its single traced raw input. Every data row, target, scoring semantics and all nine folds exactly match the previous build; only descriptive metadata changes the checksum. Prior containers and scientific decisions are preserved.

## Reference

Bierens, Herman J., and Donna K. Ginther. "Integrated conditional moment testing of quantile regression models." Empirical Economics 26 (2001): 307-324.
