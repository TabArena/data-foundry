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

**Main points:** Better-data check (2026-11-25, issue 4): Add american_companies_bankruptcy (US listed firms 1999-2018, raw statement items, one extraction for both classes, a dated temporal split) and then retire polish as replaced, which also closes its parked v0.2-page issues 1 and 2; v4finbench is not a replacement, since its label is a ratio rule that its own three ratios predict as well as all 131 features. Earlier: Nothing open: `ForcedIIDFromTemporal` stays, not `AssumedStationaryRelation` (issue 1 resolved on 2026-11-18).

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
     - polish as shipped is scored mostly on which extraction run a record came from (parked v0.2-page issue 1), and its only fix is a rebuilt 27-ratio table with the class periods still different.
     - Add the American data and then retire polish as replaced, add it next to a rebuilt polish, keep polish as is, retire polish now, or take v4finbench?
   * **Background:** "v0.2-page issue N" is the issue's number on the BeyondArena v0.2 review page; those parked issues were never written into this record, whose own issue numbers differ. 
     - polish in v0.2: 5,790 statements (5year file, bankruptcy within one year), 406 bankrupt (7.0%), 64 ratios, random 3x3 split tagged `ForcedIIDFromTemporal`, marker `Selection Bias`. Bankrupt firms are from 2000-2012 and operating ones from 2007-2013, collected in separate runs. Parked on the page (2026-11-11): v0.2-page issue 1 asks whether to retire it, and the AI answer of 2026-11-05 recommends the 27-ratio rebuild (D). v0.2-page issue 2 asks which yearly file to use, and the answer recommends keeping 5year (A). v0.2-page issue 3 is the time basis, which the record since settled (forced tag stays, 2026-11-18).
     - Andrej's note on v0.2-page issue 2 ("in the source we had different datasets for this task") is answered there: the five yearly files are one panel of the same companies at five horizons, and every file carries the same extraction runs.
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
   * **Experiments:** (2026-11-25; downloads: GitHub sowide/bankruptcy_dataset, main branch, `american_bankruptcy_dataset.csv` and `dataset_paper.zip`; Kaggle sebastiantomczak10/v4-group-corporate-bankruptcy, `company_years.parquet`, `company_years_h2.parquet` (paper horizon h=1), `column_descriptions.md`; GitHub genwro-ai/V4FinBench for the label code. Fits on Slurm, untuned LightGBM against logistic regression on quantile-normalised inputs.)
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
       | polish rebuilt, 27 ratios (v0.2-page issue 1, D) | 0.804 | 0.812 | 0.839 |

       Untuned boosting does not beat a linear model on either candidate, nor on the rebuilt polish. polish's wide spread as shipped was mostly the run markers (v0.2-page issue 1). Whether tuned and foundation models separate on the American data is not measured.
   * **Consistency:**
     - Same kind of decision as the other nine datasets of this batch (better data for the same task). Here the current dataset also has an open defect of its own data (v0.2-page issue 1), so its keep verdict is weaker than for most of the others.
     - The pattern for small or dated datasets[^better] makes the American data their own record and leaves polish's verdict to its own data. Its own data's verdict is open in v0.2-page issue 1, where retirement for class-dependent recording[^route] or the rebuild are the choices. Retiring it "as replaced" therefore rests on v0.2-page issue 1's defect, with the American record named as what replaced it[^outdated].
     - taiwanese_bankruptcy_prediction was named by the same scouting run for the same two candidates. It is not affected: its classes share one recording convention, so it keeps its verdict, and its own better-data question is not raised here. company_bankruptcy_prediction is its duplicate and stays `No`.
     - v4finbench comes from polish's database and authors. Its rule-defined label would be judged like the datasets whose label is a rule on their inputs[^rule]. It is a separate question for its own record, not a version of polish[^version].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | polish ships 5year, 64 ratios, random split; v0.2-page issues 1-2 stay parked | no work; the source's published task | run markers alone match the 64 ratios (0.964 against 0.956); periods differ by class |
     | B | Add American, then retire polish as replaced | build american_companies_bankruptcy (relabelled, repaired, temporal split); once it ships, polish becomes `No (Retired)` with `Class-dependent Recording`, naming the American record; v0.2-page issues 1-2 close | raw statements, one extraction for both classes, dated split, 609 events in 78,682 rows; no rebuilt table of ours to defend | a population of listed US firms, not Polish companies; two repairs of the source (label, decimals) to document; polish stays as shipped until then |
     | C | Add American next to a rebuilt polish | v0.2-page issue 1 D (27 rebuilt ratios) and v0.2-page issue 2 A, plus the American record | keeps a second population; every polish company kept | a rebuilt table far from the published one; periods still differ by class; the rebuild signal (0.80-0.84) is weaker than American's |
     | D | Retire polish now, add American later | v0.2-page issue 1 C now; American built separately | no score from the run markers from today | one corporate bankruptcy task fewer until American ships |
     | E | Replace polish by v4finbench | build the one-report horizon of V4FinBench | same database and country, a very large panel | label is a ratio rule that its own 3 ratios predict as well as 129 features; a distress proxy, not bankruptcy; status column leak; country codes mislabelled |

   * **Recommendation:** B: American is the better dataset for this task. Its recording does not separate the classes, it has raw items and real dates, and it is 13x larger. Once it ships, polish's own defect (v0.2-page issue 1) has no reason left to be repaired by a table we rebuild. If you want polish out of the benchmark before American is built, D. **Decision:** A, B, C, D or E?

   **Notes for the AI:**
   - On B or D, American record `curation/records/american_companies_bankruptcy.md` (exists on main, `TBD -> Yes`):
     - Source: `https://github.com/sowide/bankruptcy_dataset` (main), file `american_bankruptcy_dataset.csv`, read with `dtype=str`.
     - Repair: every X1-X18 token without a `.` is divided by 1000. Then check that EBIT + D&A = EBITDA in every row.
     - Column names (the paper's order, not Kaggle's): X1 current_assets, X2 total_assets, X3 cost_of_goods_sold, X4 total_long_term_debt, X5 depreciation_and_amortization, X6 ebit, X7 ebitda, X8 gross_profit, X9 inventory, X10 total_current_liabilities, X11 net_income, X12 retained_earnings, X13 total_receivables, X14 total_revenue, X15 market_value, X16 total_liabilities, X17 net_sales (drop: a copy of X14), X18 total_operating_expenses.
     - Categorical: Division, MajorGroup.
     - Target: `status_label == 'failed'` and `fyear == max fyear of company_name` → 1, else 0 (609 positives, 0.77%).
     - Split: temporal on `fyear`, the source's train 1999-2011, validation 2012-2014, test 2015-2018. Also say how 3x3 temporal folds would reach 33 scored test events.
     - Metric: roc_auc (the paper leads with AUC).
     - Record and README notes: the 8,971 company ids against the README's 8,262; that delistings for other reasons stay 0; CC BY 4.0.
     - Then run dataset check and the marker probe of this item (`scripts/am_markers2.py`).
   - On B, once American ships: polish record `No (Retired)`, add `Class-dependent Recording`, keep `Selection Bias`, a CC line naming american_companies_bankruptcy as the replacement and citing v0.2-page issue 1's numbers, `Andrej` in checked_by. Remove the v0.2 folder, clear `v2_path`, add a CHANGELOG entry. Close v0.2-page issues 1-3 on the page with this decision.
   - On C, apply v0.2-page issue 1 D and v0.2-page issue 2 A as written on the page, and build American as above.
   - On E, v4finbench needs its own review first (label, `operational_status`, country codes).
   - Evidence and scripts: `~/claude_jobs/better_data_1125/work/polish_companies_bankruptcy/` (`scripts/am_repair_check.py`, `am_models.py`, `am_markers2.py`, `am_check2.py`, `v4_explore.py`, `v4_models.py`; logs and JSON in `out/`). The polish numbers are from `~/claude_jobs/polish_fix/`.

   [^better]: Selection, pattern "Small or dated, and the task is still done today": a larger or newer public dataset with the same target and use case is its own record; the old record keeps the verdict its own data earn until the curator decides.
   [^route]: **LEAK-39** (Must): rows of one class recorded through a separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be aligned. **LEAK-15** (Must): a recording artefact through several features that matter, which cannot be undone, retires the dataset.
   [^outdated]: **SEL-18** (Should): a dataset leaves for being outdated only when the task is gone; a `No` that cites the replacement names its other reasons too.
   [^rule]: **SEL-5** (Must): "A label a rule assigns from columns we ship ... Drop the rule's inputs first and test what the rest predicts." Here the rule reads a later report, not the row itself, but the same ratios of the year before carry the score.
   [^version]: **PROV-6** / **PROV-7** (Must): versions of one dataset are duplicates when neither adds a distinct task; records that share a source but give different tasks are not duplicates.

## Reference

Ensemble boosted trees with synthetic features generation in application to bankruptcy prediction
By Maciej Ziȩba, S. Tomczak, Jakub M. Tomczak. 2016

Published in Expert systems with applications
