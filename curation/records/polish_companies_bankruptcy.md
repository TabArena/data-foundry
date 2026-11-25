---
unique_name: polish_companies_bankruptcy
name: Polish Companies Bankruptcy
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Fixed Delay'
- Database Snapshot
original_source: UCI
year: '2016'
collection_period: 2000-2013
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.24432/C5F600
notebook_path: datasets/beyond_iid/old_iid/polish_companies_bankruptcy/polish_companies_bankruptcy.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/polish_companies_bankruptcy/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data from companies from 2000-2012, predict for them from 2007 to 2013, likely temporal but could be made time invariant (as one has a dataset per year). features were already engineered - mostly through arithmetic interactions.

Potential issue: Temporal

Lennart: Could be used without temporal connection

Andrej: task can be conceptualized s.t. the features are time-invariant. Only need to think about whether it is feasible to combine the year datasets or to choose one. If the latter I would use the year with the most observations. Also might reverse the feature engineering.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC, as reported by Zieba, Tomczak & Tomczak (2016), Expert Systems with Applications 58, 93-101.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `american_companies_bankruptcy` (TBD -> Yes, priority 2), `v4finbench_corporate_distress` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (random, 3x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 1, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. The class/period confounding is explicit in the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods.

## Review

**Outcome:** added. Stationarity reasoning of 2026-11-18: the forced tag stays (issue 1, A, Andrej).

**Main points:** The BeyondArena v0.2 review's issues are in this review from 2026-11-25 as 5, 6, 7; the parked ones are open again. Better-data check (2026-11-25, issue 4): Add american_companies_bankruptcy (US listed firms 1999-2018, raw statement items, one extraction for both classes, a dated temporal split) and then retire polish as replaced, which also closes its parked issues 5 and 6; v4finbench is not a replacement, since its label is a ratio rule that its own three ratios predict as well as all 131 features. Earlier: Nothing open: `ForcedIIDFromTemporal` stays, not `AssumedStationaryRelation` (issue 1 resolved on 2026-11-18).

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: The 5year.arff file has no dates; the source's 'years' are forecasting horizons, not calendar years; bankrupt firms are from 2000-2012, operating ones from 2007-2013, so no period can be rebuilt.
     - Use: A lender or investor reads a new annual statement and assesses bankruptcy within a year, after the collected period.
     - Mechanism: Ratio-based failure prediction depends on the business cycle and accounting/insolvency rules; here the two classes come from different periods, so part of the signal may be the period itself.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | Mensah, 'An examination of the stationarity of multivariate bankruptcy prediction models', Journal of Accounting Research 22(1):380-395, 1984 (literature, cited from memory: check) | accuracy and structure of ratio-based bankruptcy models across economic periods | not flat: the ratio-failure relation shifts with the economic environment; models need re-estimation | financial-ratio bankruptcy prediction |
     | taiwanese_bankruptcy_prediction (this collection) | nothing over time (time lost) | unmeasured | ratio-based bankruptcy |

   * **For a stationary use case:**
     - Financial ratios have an accounting-identity link to solvency that does not depend on the date.
   * **Against:**
     - Classes drawn from different periods (2000-2012 vs 2007-2013): structure tied to time, the signal may be the period.
     - The span includes the 2008-2009 crisis; the ratio-failure relation shifts with the economy (Mensah 1984).
     - Insolvency law and accounting rules change (a change of rules).
   * **Earlier views:**
     - CC (2026-11-17, Andrej): blind split walk: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Classes drawn from different periods (2000-2012 vs 2007-2013): structure tied to time, the signal may be the period.; The span includes the 2008-2009 crisis; the ratio-failure relation shifts with the economy (Mensah 1984). |

   * **Recommendation:** A, the class/period confounding is explicit in the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (The class/period confounding is explicit in the source, and bankruptcy-ratio relations are documented as non-stationary across economic periods.)

4. **Retire polish_companies_bankruptcy once american_companies_bankruptcy is added, or keep it?**

   * **Problem:**
     - The American data have none of polish's class artefact: their label-free number-format markers reach ROC AUC 0.54 against polish's 0.96, and adding them to the 17 statement items changes nothing (0.858 against 0.857).
     - polish as shipped is scored mostly on which extraction run a record came from (parked issue 5), and its only fix is a rebuilt 27-ratio table with the class periods still different.
     - Add the American data and then retire polish as replaced, add it next to a rebuilt polish, keep polish as is, retire polish now, or take v4finbench?
   * **Background:** 
     - polish in v0.2: 5,790 statements (5year file, bankruptcy within one year), 406 bankrupt (7.0%), 64 ratios, random 3x3 split tagged `ForcedIIDFromTemporal`, marker `Selection Bias`. Bankrupt firms are from 2000-2012 and operating ones from 2007-2013, collected in separate runs. Parked on the page (2026-11-11): issue 5 asks whether to retire it, and the AI answer of 2026-11-05 recommends the 27-ratio rebuild (D). issue 6 asks which yearly file to use, and the answer recommends keeping 5year (A). issue 7 is the time basis, which the record since settled (forced tag stays, 2026-11-18).
     - Andrej's note on issue 6 ("in the source we had different datasets for this task") is answered there: the five yearly files are one panel of the same companies at five horizons, and every file carries the same extraction runs.
     - Candidates:

       | Candidate | Data | Rows (events) | What it adds | Split it allows | Access / licence | Concerns | Verdict |
       |---|---|---|---|---|---|---|---|
       | american_companies_bankruptcy (Lombardo et al. 2022, GitHub sowide/bankruptcy_dataset) | US companies listed on NYSE/NASDAQ, 1999-2018, 18 raw annual statement items plus SIC division | 78,682 firm-years of 8,971 company ids; 609 filings (Chapter 7/11) in the year after the statement (0.77%) | raw amounts instead of engineered ratios; one extraction for both classes (checked); fiscal year on every row; 13x the rows | temporal (the source's own: train 1999-2011, validation 2012-14, test 2015-18), or grouped by company | open download, CC BY 4.0; company ids anonymised, vendor not named | the published label marks every year of a failing firm (relabel needed); 64% of cells lost their decimal point (repaired by one verified rule); revenue and net sales are the same column; the column names on Kaggle are wrong | **better**: replaces the task |
       | v4finbench_corporate_distress (Kostrzewa et al. 2026, Kaggle) | Polish, Czech, Slovak and Hungarian companies from EMIS (polish's own database and authors), 2006-2021, 131 ratios and metadata | 1,106,879 company-years of 203,557 companies; at the one-report horizon 996,500 rows, 3,054 positives (0.31%) | size and recency; one extraction for both classes | grouped by company (source), or temporal (years present) | Kaggle login, CC BY 4.0 | the label is an accounting rule (equity < 0, EBITDA < 0, current ratio <= 0.6) on the company's last report, positive only when reporting stops; its three ratios alone match all features; "one report ahead" is 2-12 years in 17% of positives; `operational_status` is a snapshot from extraction time and raises the positive rate fivefold | **not better**: another target (rule-defined distress), close to circular |
       | taiwanese_bankruptcy_prediction (UCI, already a record, in v0.2 and BeyondArena) | listed Taiwanese companies, 1999-2009, 95 ratios scaled 0-1 | 6,819 (220) | the bankruptcy task that stays in v0.2 either way | random only (time lost) | open | unknown lag between ratios and bankruptcy; company-years without ids (record issues 1-3, settled) | not a candidate here: kept on its own data (one recording convention, markers 0.51-0.64) |
       | company_bankruptcy_prediction (Kaggle, already a record) | the Taiwanese table, re-uploaded | 6,819 | nothing | as Taiwanese | Kaggle | `No (Duplicate)` of Taiwanese | not a candidate |

   * **Effect on the task:**
     - With the American data the benchmark gets what Andrej asked for on the record ("might reverse the feature engineering"): raw statement items from which a lender builds the ratios, one recording route for both classes, and real dates. That allows a true temporal split instead of a forced random one.
     - The American population differs from polish: listed US companies instead of Polish EMIS companies. The task (a lender or investor scores a company's latest annual statement for a filing within a year) stays the same.
     - With polish retired, corporate bankruptcy in v0.2 is Taiwanese (random, time lost) plus American (temporal). These are two populations with no overlap.
   * **Experiments:** (2026-11-25; downloads: GitHub sowide/bankruptcy_dataset, main branch, `american_bankruptcy_dataset.csv` and `dataset_paper.zip`; Kaggle sebastiantomczak10/v4-group-corporate-bankruptcy, `company_years.parquet`, `company_years_h2.parquet` (paper horizon h=1), `column_descriptions.md`; GitHub genwro-ai/V4FinBench for the label code. Fits, untuned LightGBM against logistic regression on quantile-normalised inputs.)
     - American, the decimal repair. A token without a decimal point is the value with its point lost, so divide it by 1,000. This rule is checked against the paper's own split files, which hold correct values:

       | Check | Result |
       |---|---|
       | cells without a decimal point (repaired) | 914,068 of 1,416,276 (64%); 64.3% of alive and 67.9% of failed rows' cells |
       | paper firm-years found in the main file after repair / before | 6,170 of 6,170 / 972 |
       | EBIT + D&A = EBITDA; COGS + gross profit = revenue; current assets <= total assets; current liabilities <= total liabilities (after repair) | 100% of rows each |
       | revenue (X14) equals net sales (X17) | 100% of rows: one column is a copy |

     - American, the label. The CSV marks all 5,220 rows of the 609 failed companies as `failed`, while the README labels only "the fiscal year before the chapter filing". The paper's own files agree with the README: 496 of 502 failed rows matched to the main file are a failed company's last year, and none is an earlier year. Event = the last year of a failed company: 609 events. Other companies that leave the panel (68% of alive companies end before 2018) stay negative.
     - American, the class-artefact test (the one that sank polish). Label-free recording markers per row: cells without a point, cells ending in `.0`, zeros, whole numbers after repair, decimals of market value. Grouped 5-fold by company, 3 seeds, LightGBM ROC AUC:

       | Inputs | American | polish (shipped, for comparison) |
       |---|---|---|
       | recording markers alone | 0.538 | 0.964 (10 run flags) |
       | company size alone (log total assets, log revenue) | 0.558 | 0.736-0.781 (F1/F2 records) |
       | markers + size | 0.578 | - |
       | 17 items | 0.857 | 0.956 (64 ratios) |
       | 17 items + markers | 0.858 | - |

       Inside the failed companies, the event row and the company's earlier rows carry the same markers (whole numbers 0.82 against 0.76 per row, `.0` cells 1.32 against 1.24). The classes come from one file of one extraction, with no class-dependent route.
     - V4FinBench, the label and the markers (one-report horizon, grouped 5 folds by company as the source does / temporal train <= 2015, test 2016-2019):

       | Inputs | Grouped ROC AUC (AP) | Temporal ROC AUC (AP) |
       |---|---|---|
       | 129 features, LightGBM | 0.897 (0.037) | 0.891 (0.039) |
       | 129 features, logistic | 0.911 (0.055) | 0.900 (0.043) |
       | the label rule's 3 ratios alone, LightGBM | 0.902 (0.039) | 0.903 (0.052) |
       | the rule applied to the row itself (0/1) | 0.674 | 0.686 |
       | missing-value count + `operational_status` | 0.710 | 0.643 |
       | missing-value count alone | 0.581 | 0.539 |

       In addition, 1,104 of 3,054 positives (36%) already meet the rule on their own row. `operational_status` 0 carries 1.1% positives against 0.2% for 1. Years from the positive row to the final report: 1 in 2,536, 2-12 in 518. The country codes in `column_descriptions.md` are wrong: by the EMIS links, 0 = PL, 1 = CZ, 2 = SK, 3 = HU.
     - V4FinBench overlap with polish: 413 of 5,776 polish 5year statements match a Polish V4 row on working capital / assets and equity / assets at 4 decimals, against 50 for the Hungarian rows (about 88 when scaled to Poland's size). Adding net profit / assets leaves 2. A few hundred shared companies are possible, but the ratio definitions differ, so this is unconfirmed.
     - Baseline spread (ROC AUC, average precision in brackets). polish rows are the earlier answer's numbers (9 shipped splits), not re-run:

       | Dataset, split | LightGBM | Logistic | TabPFN 3.5 |
       |---|---|---|---|
       | American, grouped by company (3 seeds) | 0.857 (0.078); +SIC 0.860 (0.088) | 0.869 (0.073) | not run |
       | American, train <= 2014, test 2015-18 (119 events) | 0.881 (0.095); +SIC 0.902 (0.129) | 0.900 (0.218) | not run |
       | American, train <= 2011, test 2015-18 (the source's training years) | 0.855 (0.106) | 0.899 (0.194) | not run |
       | American, label as published (every year of a failed firm), grouped | 0.700 | 0.679 | not run |
       | V4FinBench, grouped / temporal | 0.897 / 0.891 | 0.911 / 0.900 | not run |
       | polish as shipped | 0.956 | 0.926 | 0.993 |
       | polish rebuilt, 27 ratios (issue 5, D) | 0.804 | 0.812 | 0.839 |

       Untuned boosting does not beat a linear model on either candidate, nor on the rebuilt polish. polish's wide spread as shipped was mostly the run markers (issue 5). Whether tuned and foundation models separate on the American data is not measured.
   * **Consistency:**
     - Same kind of decision as the other nine datasets of this batch (better data for the same task). Here the current dataset also has an open defect of its own data (issue 5), so its keep verdict is weaker than for most of the others.
     - The pattern for small or dated datasets[^better] makes the American data their own record and leaves polish's verdict to its own data. Its own data's verdict is open in issue 5, where retirement for class-dependent recording[^route] or the rebuild are the choices. Retiring it "as replaced" therefore rests on issue 5's defect, with the American record named as what replaced it[^outdated].
     - taiwanese_bankruptcy_prediction was named by the same scouting run for the same two candidates. It is not affected: its classes share one recording convention, so it keeps its verdict, and its own better-data question is not raised here. company_bankruptcy_prediction is its duplicate and stays `No`.
     - v4finbench comes from polish's database and authors. Its rule-defined label would be judged like the datasets whose label is a rule on their inputs[^rule]. It is a separate question for its own record, not a version of polish[^version].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | polish ships 5year, 64 ratios, random split; issues 5-2 stay parked | no work; the source's published task | run markers alone match the 64 ratios (0.964 against 0.956); periods differ by class |
     | B | Add American, then retire polish as replaced | build american_companies_bankruptcy (relabelled, repaired, temporal split); once it ships, polish becomes `No (Retired)` with `Class-dependent Recording`, naming the American record; issues 5-2 close | raw statements, one extraction for both classes, dated split, 609 events in 78,682 rows; no rebuilt table of ours to defend | a population of listed US firms, not Polish companies; two repairs of the source (label, decimals) to document; polish stays as shipped until then |
     | C | Add American next to a rebuilt polish | issue 5 D (27 rebuilt ratios) and issue 6 A, plus the American record | keeps a second population; every polish company kept | a rebuilt table far from the published one; periods still differ by class; the rebuild signal (0.80-0.84) is weaker than American's |
     | D | Retire polish now, add American later | issue 5 C now; American built separately | no score from the run markers from today | one corporate bankruptcy task fewer until American ships |
     | E | Replace polish by v4finbench | build the one-report horizon of V4FinBench | same database and country, a very large panel | label is a ratio rule that its own 3 ratios predict as well as 129 features; a distress proxy, not bankruptcy; status column leak; country codes mislabelled |

   * **Recommendation:** B: American is the better dataset for this task. Its recording does not separate the classes, it has raw items and real dates, and it is 13x larger. Once it ships, polish's own defect (issue 5) has no reason left to be repaired by a table we rebuild. If you want polish out of the benchmark before American is built, D. **Decision:** A, B, C, D or E?

   **Notes for the AI:**
   - On B or D, American record `curation/records/american_companies_bankruptcy.md` (exists on main, `TBD -> Yes`):
     - Source: `https://github.com/sowide/bankruptcy_dataset` (main), file `american_bankruptcy_dataset.csv`, read with `dtype=str`.
     - Repair: every X1-X18 token without a `.` is divided by 1000. Then check that EBIT + D&A = EBITDA in every row.
     - Column names (the split files' header order; the Kaggle names and the paper's own Table 2 are both wrong for the CSV, since under them D&A + EBIT = EBITDA holds in 0.01% of rows): X1 current_assets, X2 total_assets, X3 cost_of_goods_sold, X4 total_long_term_debt, X5 depreciation_and_amortization, X6 ebit, X7 ebitda, X8 gross_profit, X9 inventory, X10 total_current_liabilities, X11 net_income, X12 retained_earnings, X13 total_receivables, X14 total_revenue, X15 market_value, X16 total_liabilities, X17 net_sales (drop: a copy of X14), X18 total_operating_expenses.
     - Categorical: Division, MajorGroup.
     - Target: `status_label == 'failed'` and `fyear == max fyear of company_name` → 1, else 0 (609 positives, 0.77%).
     - Split: temporal on `fyear`, the source's train 1999-2011, validation 2012-2014, test 2015-2018. Also say how 3x3 temporal folds would reach 33 scored test events.
     - Metric: roc_auc (the paper leads with AUC).
     - Record and README notes: the 8,971 company ids against the README's 8,262; that delistings for other reasons stay 0; CC BY 4.0.
     - Then run dataset check and the marker probe of this item (`scripts/am_markers2.py`).
   - On B, once American ships: polish record `No (Retired)`, add `Class-dependent Recording`, keep `Selection Bias`, a CC line naming american_companies_bankruptcy as the replacement and citing issue 5's numbers, `Andrej` in checked_by. Remove the v0.2 folder, clear `v2_path`, add a CHANGELOG entry. Close issues 5-3 on the page with this decision.
   - On C, apply issue 5 D and issue 6 A as written on the page, and build American as above.
   - On E, v4finbench needs its own review first (label, `operational_status`, country codes).
   - Evidence and scripts: the run's evidence folder (`scripts/am_repair_check.py`, `am_models.py`, `am_markers2.py`, `am_check2.py`, `v4_explore.py`, `v4_models.py`; logs and JSON in `out/`). The polish numbers are from the run's evidence folder.

   [^better]: Selection, pattern "Small or dated, and the task is still done today": a larger or newer public dataset with the same target and use case is its own record; the old record keeps the verdict its own data earn until the curator decides.
   [^route]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned. **LEAK-15** (Must): a recording artefact through several features that matter, which cannot be undone, retires the dataset.
   [^outdated]: **SEL-18** (Should): a dataset leaves for being outdated only when the task is gone; a `No` that cites the replacement names its other reasons too.
   [^rule]: **SEL-5** (Must): "A label a rule assigns from columns we ship ... Drop the rule's inputs first and test what the rest predicts." Here the rule reads a later report, not the row itself, but the same ratios of the year before carry the score.
   [^version]: **PROV-6** / **PROV-7** (Must): versions of one dataset are duplicates when neither adds a distinct task; records that share a source but give different tasks are not duplicates.

5. **Retire it: the bankrupt and the operating companies come from separate extraction runs?**

   * **Problem:**
     - The source collected the bankrupt companies (2000-2012) and the operating ones (2007-2013) in separate runs over the EMIS database, and each run wrote its records by its own conventions: multi-year fields copied from one year or missing, another sales figure, broken balance-sheet sums, working capital stored in whole units.
     - On the v0.2 table these label-free markers alone separate the classes as well as all 64 ratios do (ROC AUC 0.955-0.964 against 0.956), so the benchmark largely scores whether a model recognises the run.
     - Retire it, cut it down to the records without markers, or keep it?
   * **Background:** the 64 columns are ratios of a few amounts per statement, so exact relations hold between them
     (liabilities over assets plus equity over assets is 1; net profit over assets equals net profit over sales times
     sales over assets). Sorted by label-free rules from an earlier leak analysis: "history-less" records (the
     three-year gross profit equals one year's, retained earnings equal net profit, or sales growth is missing) are
     193 of the 406 bankrupt companies and 10 of the 5,384 operating ones; "operating-run" records (a ratio built on
     another sales figure, a broken balance sheet, equity coded equal to equity minus share capital, operating profit
     exactly 0, or a missing three-year figure) are 2,772 operating companies and 3 bankrupt ones; 2,812 records (210
     bankrupt) carry neither. Across all records, total sales differ from sales in 86% of the bankrupt and 41% of the
     operating companies, and working capital, the one amount in thousands, is a whole number between 1,000 and 10,000 in 18.5%
     against 5.4%.
     The UCI page states the two periods; the conventions are measured, their cause is not documented.
   * **Effect on the task:** in use every statement comes from one extraction and none of these markers carries the
     outcome. Here half of the bankrupt companies are marked by a copied or missing field that almost no operating
     company has, and the leading models put all of them at the top; the rest of the score is set by the 210
     bankrupt companies in unmarked records.
   * **Experiments:** on the shipped table (the v0.2 frame), the 9 shipped splits, untuned LightGBM: the 10 marker
     flags alone ROC AUC 0.964, flags plus three identity residuals 0.955, the 64 ratios 0.956. From an earlier
     leak analysis (TabArena v0.1 copy of the same file): on the unmarked records, with six columns dropped and working
     capital rounded, the markers still reach 0.70 and four identity residuals 0.77, while the ratios reach 0.845; the
     other four yearly files of the source carry the same markers in the same direction.
   * **Consistency:** follows prostate_cancer_detection and hepatitis_c_prediction (retired: the classes were recorded
     through different routes that models recognise)[^1a]; differs from gallstone_disease (kept: its separate route
     was 77 rows that could be dropped)[^1b].
   * **Unknown:** whether the authors or EMIS can supply both classes from one extraction, with raw amounts and dates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 5,790 statements, 64 ratios | the source's task as published | the classes are told apart by the extraction run; markers alone match the ratios |
     | B | Unmarked records only | keep the 2,812 records without markers (210 bankrupt); drop sales growth, three-year gross profit, retained earnings, total sales, total costs over sales and equity minus share capital; round working capital | removes what the markers read; a signal remains (ROC AUC 0.845) | still a selection on a recording convention; identity residuals still reach 0.77; about 70 bankrupt per test fold; the periods still differ |
     | C | Retire | record `No (Retired)` with `Class-dependent Recording`; folder removed | no score from recognising the run; better data for the task are in screening | one corporate bankruptcy task fewer until a replacement ships |

   * **Recommendation:** C: the artefact runs through several ratios a lender relies on (profit history, sales, the
     balance sheet), and the cut-down variant shows it cannot be undone. **Decision:** retire (C), cut down (B) or
     keep (A)?

   **Notes for the AI:** on C, record `suggestion: No (Retired)`, add `Class-dependent Recording` and keep `Selection
   Bias`, a CC line with the numbers of this issue; remove the folder, clear `v2_path`, add a CHANGELOG entry and a
   case row under LEAK-15 in `leak_checks.md`. On B, keep the rows of type "consistent" by the label-free rules of the
   earlier leak analysis (the record types in the Experiments above), drop the six columns, round
   `working_capital_absolute` to 3
   significant digits, re-run `dataset check` and the marker check of this review.

   [^1a]: **LEAK-15** (Must; amended 2026-10-27, Andrej, on gallstone_disease): a recording artefact that runs
     through several features that would matter for prediction in practice, and that cannot be undone, retires the
     dataset; a feature subset does not help when it also separates same-label groups.
   [^1b]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint,
     are dropped when models recognise them and the route cannot be aligned with the other rows.

   **Andrej (2026-11-05, discuss):** Is it possible to fix the task somehow that there is no leakage?

   **Answer (AI, 2026-11-05):**

   * **Found:** yes. When every kept ratio is rebuilt from one set of amounts per statement, the same way for every
     row, and the ratios whose amounts the source copied, coded 0 or left out are dropped (27 of the 64 ratios stay,
     all 5,790 statements), no recording convention tells the records apart within a class except company size, and a
     real signal remains: ROC AUC 0.80 (LightGBM), 0.81 (logistic regression) and 0.84 (TabPFN 3.5), against 0.956,
     0.926 and 0.993 as shipped.
   * **What the runs are:** label-free rules sort the records into three formats, each found in both classes, plus a
     history gap of the bankrupt companies:
     - F1, 2,896 records (295 bankrupt): the reference format; inside it, bankrupt records hold some items separately
       that operating records copy from another item (below).
     - F2, 2,225 records (102 bankrupt), larger companies in both classes (about six times F1's median total assets):
       `sales_to_total_assets` holds total sales over total costs (2,217 of 2,225 records), and several items are
       copies or left out.
     - F3, 669 records (9 bankrupt): operating profit and tax coded 0, costs booked on another basis; 1.3% bankrupt
       at every company size, so it acts as a route of operating companies.
     - History missing (three-year gross profit equal to one year's, retained earnings equal to net profit, or sales
       growth missing): 193 of 406 bankrupt and 10 of 5,384 operating companies, in every format.
   * **Each convention and what the fix does to it, the same rule for every row:**
     - History: retained earnings, sales growth and three-year gross profit are dropped.
     - Sales (F2): the ratios over sales use the real sales figure in every format, so sales are taken from them for
       every row and `sales_to_total_assets` is rebuilt from that figure; total sales and total costs over total
       sales are dropped.
     - Balance sheet (F2): liabilities leave out a third item, so liabilities plus equity fall short of total assets
       in 86% of F2 records (median 2.8% of assets); liabilities become total assets minus equity, and the four
       long-term liability ratios, which would still show the third item, are dropped.
     - Copied or zero items: F2 copies gross profit into extended profit, operating profit into profit on sales and
       equity into equity minus share capital (99% each); F3 codes operating profit 0 (79%), has net profit equal to
       gross profit in 85% (31% of F1 operating companies) and operating expenses of 0.77 of sales (0.96 in F1 and
       F2). Dropped: operating profit and its five ratios, the two profit-on-sales ratios, extended profit, equity
       minus share capital, and the ratios built on net profit (4), operating expenses (2), cost of sales (2) and
       depreciation (3).
     - Inside F1, items that bankrupt records hold separately and operating records copy: total sales differ from
       sales in 82% against 3%, current liabilities from short-term liabilities in 60% against 8%, gross margin from
       the profit-on-sales margin in 66% against 7%, and one liquidity ratio uses another inventory figure in 73%
       against 0.2%. The copies are dropped, and inventory comes from one figure for every row.
     - Working capital, in whole units for part of the bankrupt records and a copy of the current ratio in 174
       records (170 operating): rebuilt as working capital over assets times assets. Every column is rounded to 4
       significant digits, since rebuilt values carry more digits than the source's 5.
   * **Run test:** can a model tell one format, or the history gap, from another within one class? Out-of-fold ROC
     AUC, 5 folds x 3 seeds, LightGBM / logistic regression; 0.5 means it cannot:

     | Within one class | As shipped | Rebuilt (D) | Rebuilt, without the two size columns |
     |---|---|---|---|
     | operating: F1 against F2 | 0.999 / 0.997 | 0.85 / 0.84 | 0.64 / 0.62 |
     | operating: F1 against F3 | 0.989 / 0.980 | 0.53 / 0.57 | not run (size alone 0.48) |
     | bankrupt F1: with against without history | 1.000 / 1.000 | 0.55 / 0.51 | 0.56 / 0.49 |
     | bankrupt: F1 against F2 | 0.998 / 1.000 | 0.73 / 0.77 | 0.56 / 0.56 |

   * **What still separates F1 from F2 is company size:** size alone (log total assets, working capital) tells them
     apart at 0.81-0.83, and on the F1 and F2 records size plus the format predicts bankruptcy no better than size
     alone (LightGBM 0.737 against 0.736, logistic 0.782 against 0.781). Within a size quintile F2's bankrupt share
     is higher than F1's in some and lower in others. The rest without size (0.62-0.64) comes from ratios that go
     with size, such as sales over fixed assets.
   * **Identity check:** on the rebuilt table no relation between two or three columns (equal, summing to 1, product,
     quotient, difference) holds at rates that differ by format or class by more than 0.08; as shipped, 373 such
     relations differ by 0.3 or more.
   * **Label test:** ROC AUC on the 9 shipped splits, LightGBM / logistic regression / TabPFN 3.5:

     | Table | Rows (bankrupt) | Columns | ROC AUC |
     |---|---|---|---|
     | As shipped (A) | 5,790 (406) | 64 | 0.956 / 0.926 / 0.993 |
     | 10 label-free run flags alone | 5,790 (406) | 10 | 0.964 / 0.967 / not run |
     | Rebuilt (D) | 5,790 (406) | 27 | 0.804 / 0.812 / 0.839 |
     | Rebuilt, F3 records dropped instead of their ratios | 5,121 (397) | 40 | 0.811 / 0.823 / 0.869 |
     | Company size alone, F1 and F2 records | 5,121 (397) | 2 | 0.736 / 0.781 / not run |

   * **Models no longer score the run:** on D a bankrupt F1 company is ranked against an operating F3 company no
     better than against an operating F1 company (LightGBM 0.78 against 0.79; as shipped 0.95 against 0.90), and the
     bankrupt companies without history get the same scores as the other bankrupt ones (0.52; as shipped 0.96). The
     40-column variant scores 0.79-0.81 within one format.
   * **Dropping the F3 records instead:** keeps 13 more ratios and scores higher, as a separately recorded route may
     be dropped[^a3]; but it keeps net profit equal to gross profit at different rates by class (60% of bankrupt
     against 32% of operating F1 records), mostly, not fully, explained by losses, so D drops those ratios instead.
   * **Other yearly files:** all five carry the same three formats in the same direction (F3 is 12-13% of operating
     and 1-2% of bankrupt companies in every file; in F1 total sales are copied from sales for 97-99% of operating
     and 9-18% of bankrupt companies), so the same rebuild applies to each, and pooling them adds rows but no fix.
   * **Periods:** the files have no dates, and the formats do not stand for periods (F2's share of operating
     companies is 44%, 32%, 32%, 33% and 40% across the five files), so no period-matched subset can be built; the
     different periods stay, as the `Selection Bias` marker says.
   * **Effect on the task:** D is harder and closer to what a lender sees. The wide spread between benchmark methods,
     which mostly measured who reads the run markers, would have to be measured again.
   * **Consistency:** follows gallstone_disease, kept once its separately recorded rows and number formats were
     harmonised and models no longer recognised them[^a1]; prostate_cancer_detection and hepatitis_c_prediction were
     retired because no fix removed what models recognised[^a2]. B kept the balance-sheet sum as recorded and three
     of the bankrupt-only items (current liabilities, gross margin, the inventory figure), which D rebuilds or drops.
   * **Unknown:** conventions nobody has found yet; the run test and the identity check found none on D beyond size.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 5,790 statements, 64 ratios as published; ROC AUC 0.956 LightGBM, 0.926 logistic, 0.993 TabPFN | the source's task as published | 10 label-free run flags alone match the ratios (0.964 against 0.956); models score the format and the missing history |
     | B | Unmarked records only | 2,812 records (210 bankrupt); six columns dropped; working capital rounded; ROC AUC 0.845 LightGBM (TabArena v0.1 copy) | removes the markers found first; a signal remains | a selection on a recording convention; identity residuals still 0.77 and markers 0.70; half the companies lost |
     | C | Retire | record `No (Retired)` with `Class-dependent Recording`; folder removed | no score from recognising the run; better data for the task are in screening | one corporate bankruptcy task fewer until a replacement ships |
     | D | Rebuild from one set of amounts (new) | all 5,790 statements; 27 ratios rebuilt the same way for every row (sales from the ratios over sales, liabilities as assets minus equity, one inventory figure); 37 ratios dropped (history, copied or zero items, items defined by format); 4 significant digits; ROC AUC 0.804 LightGBM, 0.812 logistic, 0.839 TabPFN | formats and missing history no longer recognised within a class beyond company size; the format adds nothing to the label beyond size; every company kept | a table we rebuilt, not the published one; drops ratios a lender uses (retained earnings, sales growth, operating and net profit); the periods still differ; benchmark methods need re-runs |

   * **Recommendation:** D: every convention found can be undone or its ratio dropped for every row, the rebuilt
     table no longer lets a model recognise the run except through company size, the format adds no label
     information beyond size, and a real signal remains. This replaces the issue's recommendation of C,
     which rested on the cut-down variant B; C stays the choice if a table we rebuilt is too far from the published
     one. **Decision:** D, C, B or A?

   **Notes for the AI:** on D, `_clean` rebuilds every row by label-free rules (Xk is UCI attribute k, the shipped
   column order). Format F2: one of X1/X23, X18/X19, X35/X39, X63·X51 differs from X9 by more than 0.2%, or
   X9·X58 = 1 within 0.2%. Sales S = the median of those four implied figures, X9 where none is usable outside F2.
   In units of total assets: TL = 1 − X10, CA = X4·X51, WC = CA − X51, FA = 1 − CA, inv = X20·S/365,
   rec = X44·S/365, cash = X2 − X30·S. The 27 kept columns, under their shipped names: X2 = TL, X3 = WC, X4,
   X8 = X10/TL, X9 = S, X10, X12 = X18/X51, X17 = 1/TL, X18, X19 = X18/S, X20, X28 = WC/FA, X29,
   X30 = (TL − cash)/S, X40 = (CA − inv − rec)/X51, X43 = (inv + rec)·365/S, X44, X46 = (CA − inv)/X51,
   X50 = CA/TL, X51, X53 = X10/FA, X55 = WC·10^X29, X60 = S/inv, X61 = S/rec, X62 = X51·365/S, X63 = S/X51,
   X64 = S/FA; every other column dropped; infinities to missing; every column rounded to 4 significant digits.
   Then `dataset check`, the run test (formats F1/F2/F3 by the rules of this answer and the history flags as
   label-free groups, adversarial within each class) and the identity scan. Record: keep `Selection Bias`, add
   `Class-dependent Recording`, a CC line with this answer's numbers, `Andrej` in `checked_by`; rewrite `known`,
   `changes` and `fit_reason` of the task summary (27 rebuilt ratios, the periods); CHANGELOG entry. On C, as in the
   notes above.

   [^a1]: **LEAK-13** (Must): class-specific recording conventions are harmonised: every row at the precision of the
     measured values, a column dropped when only one class has it or it was filled in for one class only; first
     measure how much the fix removes.
   [^a2]: **LEAK-15** (Must): a recording artefact through several features that matter for prediction, which cannot
     be undone (no batch id to drop, no format to harmonise, no route to align), retires the dataset; a feature
     subset does not help when it also separates same-label groups. D's subset separates same-label groups only
     through company size.
   [^a3]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint,
     are dropped when models recognise them and the route cannot be aligned with the other rows.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 4 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Note (AI, 2026-11-25):** the BeyondArena v0.2 review's issue 1, parked there on 2026-11-11 and never written into this record; it is kept here under its new number.

6. **Which of the source's five yearly files should the task use?**

   * **Problem:**
     - The five files are one panel of the same companies a year apart, without a company id: a statement's sales
       divided by its sales growth equal the sales of one statement of the previous file, and 97% of the 5year
       statements (5,603 of 5,790) have the same company's statement in 4year, so files pooled under a random split
       put one company on both sides.
     - Each file is another horizon (bankruptcy 5, 4, 3, 2 or 1 year after the statement), and the definition uses
       only 5year, the one-year horizon, which is also the file where the most real signal is left once the
       extraction runs of issue 5 are removed (ROC AUC 0.79-0.84 against 0.61-0.75 in the other files).
     - Keep 5year, switch to another file, pool the files with the horizon as a feature, or ship several horizons?
   * **Background:** UCI 365 calls the five files "five classification cases" distinguished by the forecasting
     period: file k holds statements from year k of the forecasting period with the bankruptcy status after 6 − k
     years; the bankrupt companies are from 2000-2012, the operating ones from 2007-2013, all from EMIS. A company
     keeps its class in every file: a bankrupt company's statements one to five years before its bankruptcy are the
     positives of the five files, and an operating company's statements are negatives in each. The files carry no
     company id and no year.
   * **Effect on the task:** a lender deciding on credit predicts default over the next year, the horizon of 5year;
     a longer horizon is another question with less to go on. Pooling files under a random split would let a model
     recognise a company from its statement of another year, which a new borrower does not offer.
   * **Experiments:**
     - Recurrence: in every pair of consecutive files, 99-100% of the bankrupt statements with a sales growth have
       a previous-year sales figure that equals the sales of a bankrupt statement in the previous file within the
       precision of the stored values (3-5% when the figure is shifted by 0.5%, a null); for operating statements
       82-88% against 13-15% at a tighter tolerance. The linked pairs are nearly one to one (at most 9 earlier
       statements used twice per pair of files) and plausible (total assets within a factor of 2 in 96-97% of pairs,
       20-23% of random pairs). Chained, the 42,603 statements are about 11,600 companies, 3,587 of them in all five
       files. No statement appears twice: no row is identical across files.
     - Per file, the definition's duplicate drop applied; formats as in issue 5 (share of operating / bankrupt
       companies, %):

       | File | Horizon | Rows | Bankrupt | F1 | F2 | F3 | History gap |
       |---|---|---|---|---|---|---|---|
       | 1year | 5 years | 6,863 | 271 (3.9%) | 45 / 55 | 43 / 43 | 12 / 1.8 | 23 / 80 |
       | 2year | 4 years | 9,993 | 396 (4.0%) | 56 / 65 | 31 / 34 | 13 / 1.8 | 31 / 67 |
       | 3year | 3 years | 10,329 | 491 (4.8%) | 56 / 69 | 31 / 29 | 13 / 2.0 | 7 / 55 |
       | 4year | 2 years | 9,628 | 511 (5.3%) | 56 / 73 | 32 / 26 | 12 / 1.2 | 0.6 / 47 |
       | 5year | 1 year | 5,790 | 406 (7.0%) | 48 / 73 | 39 / 25 | 12 / 2.2 | 0.2 / 48 |

     - ROC AUC per file, 3 x 3 stratified cross-validation, LightGBM / logistic regression (/ TabPFN 3.5 for the
       rebuild of issue 5):

       | File | 64 ratios as published | 10 run flags alone | Rebuilt (issue 5, D) |
       |---|---|---|---|
       | 1year | 0.956 / 0.915 | 0.972 / 0.981 | 0.656 / 0.710 / 0.725 |
       | 2year | 0.924 / 0.819 | 0.974 / 0.973 | 0.605 / 0.647 / 0.684 |
       | 3year | 0.930 / 0.875 | 0.972 / 0.972 | 0.652 / 0.708 / 0.717 |
       | 4year | 0.943 / 0.892 | 0.965 / 0.966 | 0.697 / 0.734 / 0.747 |
       | 5year | 0.956 / 0.927 | 0.964 / 0.966 | 0.791 / 0.810 / 0.837 |

     - The run problem of issue 5 is no smaller in any file: the run flags alone score 0.96-0.98 everywhere and
       beat the 64 ratios in every file. The rebuild works in each (operating F1 against F3 0.52-0.56, bankrupt with
       against without history 0.45-0.59), but in 1year and 2year a quarter to a third of the operating companies
       also lack history, and the rebuilt ratios still tell those apart from the others (0.67 and 0.85).
     - Pooled, the rebuilt ratios plus the horizon: LightGBM scores 0.764 over a random split and 0.710 over a split
       grouped by the company chains, so the recurring companies add 0.05; logistic regression, which cannot
       memorise a company, scores the same (0.728, 0.727). On the 5year test rows the grouped pooled model scores
       0.805 / 0.807 against 0.791 / 0.810 for 5year alone: the other horizons add almost nothing to the one-year
       predictions.
   * **Consistency:** TabArena v0.1 (OpenML dataset 46950) and BeyondArena ship 5year alone, for the same reason as
     the definition; OpenML also holds the five files as 42880 and 42984-42987, uploaded without a target or a task.
     The record polish_companies_bankruptcy_duplicate is the same UCI source, rejected as a duplicate, not another
     file[^2a]. A random split over repeated companies rewards recognising them[^2b], and a group key reconstructed by
     choosing among candidates is not an exact one[^2c].
   * **Unknown:** what the paper reports per file: it is closed access and no free copy turned up, so its per-year
     results are unchecked[^2d]; the calendar year of each statement.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 5year (implemented) | one statement per company, bankruptcy within one year; 5,790 rows, 406 bankrupt; rebuilt ROC AUC 0.79 / 0.81 / 0.84 | the horizon a lender acts on; the most real signal of the five files; each company once, so a random split is sound | the smallest file; the other files' statements unused |
     | B | 4year instead | 9,628 rows, 511 bankrupt, bankruptcy two years after the statement; rebuilt 0.70 / 0.73 / 0.75 | two thirds more rows | a horizon a credit decision does not use; less real signal while the run flags still score 0.97 |
     | C | Pool the five files | 42,603 statements, 2,075 bankrupt; the horizon as a feature; split grouped by the company chains | all the source's data | the company key is reconstructed, not given; a random split adds 0.05; the one-year predictions barely gain (0.805 against 0.791); mixes horizons into one score |
     | D | Five horizons as separate tasks | one dataset per file | covers every horizon the source defines | the same 11,600 companies five times; the long horizons are mostly the run artefact (rebuilt 0.61-0.75) |

   * **Recommendation:** A: the one-year horizon is the lender's question and keeps the most signal once the runs
     are removed, every company appears once, and no other file has a smaller run problem; pooling needs a company
     key we can only reconstruct and adds nothing to the one-year predictions. If issue 5 retires the dataset, this
     issue closes with it, as every file carries the same runs. **Decision:** A, B, C or D?

   **Notes for the AI:** on A, nothing changes in `_load_raw`; add to `curation_comments` that the five files are a
   panel of the same companies (linked by sales over sales growth, 97% of 5year statements found in 4year), that
   the other files are longer horizons with less signal after the rebuild, and that pooling them needs a company key
   the source does not give. On B, read `4year.arff`, and the task summary's `predicted` becomes bankruptcy two years
   after the statement. On C, read all five files, add `horizon_years` = 6 − k, build the company chains (a statement
   of file k + 1 linked to the statement of file k, same class, whose sales equal its sales over its sales growth
   within 2e-4, the closest total-assets change among the candidates, within a factor of 3, one to one) and group
   the split on them; the chains are a reconstruction, so the rule on exact group keys needs an exception. On D,
   five folders, each with issue 5's rebuild.

   [^2a]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates when neither adds a
     distinct task; **PROV-7** (Must) narrows it: records that share a source but give different tasks are not
     duplicates.
   [^2b]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have and
     the entity carries the label.
   [^2c]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data, never on a
     similarity-threshold cluster; **SPLIT-25** (Must): when the real groups matter and cannot be recovered, do not
     group on a guess.
   [^2d]: **PROV-17** (Must): a paywalled paper without a free copy: ask the curator for the PDF, and mark claims
     from it as unverified.

   **Andrej (2026-11-05, discuss):** We need to open another discussion point: I believe in the source we had
   different datasets for this task. Reassess them again and check what we should really use.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 4 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Note (AI, 2026-11-25):** the BeyondArena v0.2 review's issue 2, parked there on 2026-11-11 and never written into this record; it is kept here under its new number.

7. **Time basis: tag the random split as forced from temporal?**

   * **Problem:**
     - Each row is one company's statement, labelled by bankruptcy within a year; the bankrupt companies' statements are from 2000-2012 and the operating ones' from 2007-2013, and the file keeps no year and is sorted by class, so the time is lost.
     - The record's collection facts hold (`Samples: Over Time`, `Time: Lost`, `Target: Later`); the definition splits at random and names no time basis.
     - A lender scores next year's statements in a credit climate that moves (2008), so the five questions give the forced tag, at random, since each company appears once in the file[^3a].
   * **Background:**
     - No prototype fits: the statements share no prediction moment, so the target is not a delayed one of one
       snapshot, and bankruptcy is a later outcome, not a present state.
     - The leak test across the split: in 5year each company appears once (issue 6 links the files, not rows within
       one); the raw order is by class only (operating, then bankrupt); the classes come from different periods,
       which the `Selection Bias` marker (2026-10-20) and the extraction runs of issue 5 already cover, so the test
       adds no new leak.
     - If issue 6 pools the five files grouped by the company chains, the tag becomes `ForcedGroupedFromTemporal`;
       if issue 5 retires the dataset, this issue closes with it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to write | `dataset check` notes a split that is not temporal without a basis; the missing years are not stated as a forced split |
     | B | Forced from temporal | `ForcedIIDFromTemporal` and a `Time basis:` line | says that later statements are the use and the years are missing; the leak test finds nothing beyond issue 5 | none found |
     | C | Delayed target | `DelayedTarget` and its line | none | the statements span 2000-2013, with no shared prediction moment |

   * **Recommendation:** B, if the dataset stays (issue 5, D). **Decision:** A, B or C?

   **Notes for the AI:** once the time-basis tags are in this working copy, on B: `data_tags = ("ForcedIIDFromTemporal",)` and in
   `curation_comments` the bullet `- Time basis: ForcedIIDFromTemporal: one statement per company, bankruptcy within
   a year (5year file); bankrupt companies' statements from 2000-2012, operating ones' from 2007-2013, used to score
   later statements. The file keeps no year and is sorted by class (Time: Lost). Leak test across the split: each
   company appears once in the file; the different periods of the classes are the Selection Bias marker and the
   extraction runs. Statement years would allow a split by time.`; the `split` sentence names the forced split;
   `dataset check`. The record's facts stay.

   [^3a]: **SPLIT-32** (Should): the record's collection facts and the five questions; samples over time whose period
     moves the target, with the time lost, get a forced split (SPLIT-8). **SPLIT-8** (Must): the closest regime,
     tagged, after a leak test across the split; grouped by the entity when the entities recur across periods.

   **Andrej (2026-11-11, discuss):** Park it until we decide on checking in with better suited datasets for this task.

   **Answer (AI, 2026-11-25):** the park ends: the better-data check of 2026-11-25 asks in issue 4 of this review whether another dataset replaces this one, so this issue is open again and waits for a decision. It is written as it stood when it was parked; nothing in it was re-measured today.

   **Note (AI, 2026-11-25):** the BeyondArena v0.2 review's issue 3, parked there on 2026-11-11 and never written into this record; it is kept here under its new number.
## Reference

Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction
By Maciej Ziȩba, S. Tomczak, Jakub M. Tomczak. 2016

Published in Expert systems with applications
