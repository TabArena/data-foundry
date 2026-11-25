---
unique_name: american_companies_bankruptcy
name: 'Machine Learning for Bankruptcy Prediction in the American Stock Market: Dataset and Benchmarks (American bankruptcy dataset)'
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
decision_markers:
- Data Quality Issue
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Panel Data
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Entities: Recur'
original_source: Github
year: '2022'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.3390/fi14080244
- https://github.com/sowide/bankruptcy_dataset
- https://www.kaggle.com/datasets/utkarshx27/american-companies-bankruptcy-prediction-dataset
- https://github.com/sowide/Multi-modal-bankrutpcy
- https://doi.org/10.1109/ACCESS.2024.3476621
v2_path: datasets/_dev/tabarena-v0pt2/american_companies_bankruptcy/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, the downloaded files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: 78,682 firm-years of US listed companies (fiscal years 1999-2018) with 18 raw statement items, one extraction for both classes (recording markers alone ROC AUC 0.54) and the source's own dated split; usable after two documented repairs of the published CSV (decimal points, label). Found as better data for `polish_companies_bankruptcy`.
- Source: first publication Lombardo, Pellegrino, Adosoglou, Cagnoni, Pardalos, Poggi, "Machine Learning for Bankruptcy Prediction in the American Stock Market: Dataset and Benchmarks", Future Internet 14(8):244, published 2022-08-22 (doi 10.3390/fi14080244; full text read 2026-11-25), data on GitHub sowide/bankruptcy_dataset, CC BY 4.0. Section 3: "We collected accounting data from 8262 different companies in the period between 1999 and 2018", "we consider the same companies used in [6,37]" (the authors' earlier 10-K papers), "the resulting dataset of 78,682 firm-year observations". The repo's `dataset_paper.zip` (the split files) is not from this paper: it is the multimodal set of sowide/Multi-modal-bankrutpcy, 6,190 companies, one row per company with a 3-year window of the same items plus 10-K Items 1, 5 and 7 as text, train fiscal years 2001-2014 (2,739/403), validation 2015 (206/27), test 2016-2018 (2,743/72), published with Lombardo, Bertogalli, Consoli, Reforgiato Recupero, "Natural Language Processing and Deep Learning for Bankruptcy Prediction: An End-to-End Architecture", IEEE Access 2024 (doi 10.1109/ACCESS.2024.3476621; abstract: "a dataset including 6190 companies from 1999 to 2018"). Measured 2026-11-25 on the files: 78,682 rows, fiscal years 1999-2018, 8,971 company ids (the README and paper say 8,262), 18 items X1-X18 plus SIC `Division` and `MajorGroup`, `status_label` alive/failed; the vendor is not named ("The non-anonymized version of this dataset can NOT be available because of the license used to retrieve the dataset").
- Use case: a financial institution assesses a listed firm's credit risk from its latest annual statement, for a Chapter 7 or 11 filing in the next year (Abstract: "Predicting corporate bankruptcy is one of the fundamental tasks in credit risk assessment ... a priority for most financial institutions"; Section 3: "predict bankruptcy at least one year before it happens"); fit direct; collection `Samples: Over Time`, `Time: Dated` (`fyear` on every row), `Target: Fixed Delay` (the filing in the year after the statement), `Entities: Recur` (about 8 years per company, Section 6): time lives in `fyear`; type `Panel Data` (the same companies at yearly occasions, identified by an anonymised id).
- Split: leaf [L-ORDER.windows] because [PAN.when] after the data, [PAN.units] the same and new companies, [PAN.calendar] a shared calendar (fiscal year), [ORDER.order] `fyear` recorded, [ORDER.windows] by the paper's Table 1, fiscal years 1999-2008 hold 45,046 rows (57%), and three windows on 2009-2011, 2012-2014 and 2015-2018 hold 83, 87 and 119 events (at least 33 each); a one-year gap follows from the label's delay (SPLIT-10). The source's own split (Sections 3 and 6: "We used data from 1999 until 2011 for training, data from 2012 until 2014 for validation and model comparison, and the remaining years from 2015 to 2018 as a test-set") is temporal and agrees with the leaf, but has no gap: 2011 rows are labelled by 2012 filings. Open: whether companies seen in training stay in the test windows (the leaf keeps them; the use case scores known and new listed firms).
- Siblings and duplicates: `polish_companies_bankruptcy` (`Yes`, shipped; its decision item of 2026-11-25 recommends adding this record and then retiring polish as replaced, because polish's extraction runs alone score ROC AUC 0.964), `taiwanese_bankruptcy_prediction` (`Yes`, kept on its own data), `company_bankruptcy_prediction` and `analcatdata_bankruptcy` (`No`, `Duplicate`), `qualitative_bankruptcy` (`No`), `v4finbench_corporate_distress` (`TBD -> Yes`; measured 2026-11-25 as a rule-defined distress label, another target), `us_accounting_fraud_aaer` (US firm-years, a fraud label): no duplicate (PROV-4). The Kaggle copy (utkarshx27) is this source re-uploaded without the SIC columns, kept on this record. External collections: none found.
- Better data: found as better data for `polish_companies_bankruptcy`. Nothing better found for this record: ECL (Arno et al., FinNLP 2023; 10-K filings with LoPucki labels) does not ship its Compustat items ("we are unable to share the complete benchmark dataset"); Zhang et al. 2026 (arXiv 2606.05623, SEC XBRL data, 40,475 firm-years 2010-2021, 128 events) is smaller and releases no table; V4FinBench has another target (above).
- Papers and pages: the Future Internet 2022 paper; Pellegrino et al., Future Internet 16(3):79, 2024 (multi-head LSTM on the same data, 4-year windows best); Lombardo et al., IEEE Access 2024 (the multimodal split files); Ranjbaran et al., EPJ Data Science 2023 (augmentation, uses it among others); GitHub sowide/bankruptcy_dataset and sowide/Multi-modal-bankrutpcy; Kaggle utkarshx27/american-companies-bankruptcy-prediction-dataset.
- Metric: ROC AUC, the paper's selection criterion (Section 8: "we compared all the models in terms of the AUC, and we identified the best model for both tasks using this metric ... due to the imbalance test set, but also because it is most commonly used in literature"); deliberate, though its Conclusions argue that per-class precision, recall and macro-F1 "would better define the models' performance", with no threshold fixed; inputs none (MET-1, MET-5, MET-6). The IEEE Access 2024 paper reports accuracy, recall and type II error on its own split files.
- Baselines (measured 2026-11-25, untuned, ROC AUC with average precision in brackets, event = a failed company's last year): train fiscal years up to 2014, test 2015-2018 (119 events): LightGBM 0.881 (0.095), logistic regression 0.900 (0.218); grouped 5-fold by company: 0.857 against 0.869. The paper's best average on its validation years is 0.748 (random forest, balanced resampling), its best test AUC 0.861 (ANN, Table 4).
- Risks for /add-dataset:
  - Decimal points (`Data Quality Issue`, PROV-13): 914,068 of 1,416,276 item cells (64%) lost their decimal point; dividing every token without a point by 1,000 (read with `dtype=str`) matches 6,170 of 6,170 firm-years of the split files exactly (972 before the repair), and after it EBIT + D&A = EBITDA, COGS + gross profit = revenue, current assets <= total assets and current liabilities <= total liabilities hold in 100% of rows. Document the rule in the definition.
  - Label (USE-5): the CSV marks all 5,220 rows of the 609 failed companies as `failed`, while the paper and README label only "the fiscal year before the chapter filling". Relabel: event = a failed company's last fiscal year, 609 events (0.77%); the paper's Table 1 counts exactly 609 bankrupt firms over 2000-2019 with 78,682 rows, and 496 of 502 failed rows of the split files matched to the main file are a last year, none an earlier one. With the label as published, grouped ROC AUC falls to 0.70 (LightGBM). Companies that leave for other reasons (68% of alive companies end before 2018) stay 0; a later filing after delisting is not in the data.
  - Column names: the Kaggle names and the paper's own Table 2 (X1 current assets, X2 COGS, X3 D&A, X4 EBITDA, ...) are wrong for the CSV: under them D&A + EBIT = EBITDA holds in 0.01% of rows. The split files' header order is right (X1 current_assets, X2 total_assets, X3 cost_of_goods_sold, X4 total_long_term_debt, X5 depreciation_and_amortization, X6 ebit, X7 ebitda, X8 gross_profit, X9 inventory, X10 total_current_liabilities, X11 net_income, X12 retained_earnings, X13 total_receivables, X14 total_revenue, X15 market_value, X16 total_liabilities, X17 net_sales, X18 total_operating_expenses).
  - X17 (net sales) equals X14 (total revenue) in 100% of rows: drop one.
  - Selection: the firm set is the one of the authors' earlier 10-K papers, and the paper says the bankruptcy rate "can be underestimated due to the exclusion of some companies in the past because of their small market capitalization"; 8,971 ids against 8,262 stated is unexplained.
  - Class artefact checked and absent: label-free recording markers (cells without a point, `.0` endings, zeros, whole numbers) reach ROC AUC 0.538 alone and add nothing to the 17 items (0.858 against 0.857), measured 2026-11-25 (LEAK-39).
- Priority: gap 0 (finance, binary and temporal are not thin), use case + (the source names credit risk assessment by financial institutions, one year ahead; fit direct), source + (a dataset paper and the authors' repository), shape + (78,682 firm-years, 17 items and SIC codes, dated), risk - (two repairs of the published CSV, the label and the decimal points, plus wrong column names).
- Not checked: the vendor (not named anywhere read); why the CSV holds 8,971 ids; which filings the 609 events are (no dates or names ship). Licence: CC BY 4.0 on the repository (EV-4, no reason for a verdict).

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 78,682 firm-years of 8,262 US listed companies (1999-2018) with 18 raw accounting items and a legal-filing label for the next year, published with a temporal split; a preview shows a decimal-point corruption to repair before anything else.
- Source: Lombardo, Pellegrino, Adosoglou, Cagnoni, Pardalos, Poggi, "Machine Learning for Bankruptcy Prediction in the American Stock Market: Dataset and Benchmarks", Future Internet 14(8):244, 2022 (doi 10.3390/fi14080244); data on GitHub sowide/bankruptcy_dataset (`american_bankruptcy_dataset.csv`, 12.4 MB, CC-BY-4.0, plus `dataset_paper.zip`). README: "We collected accounting data from 8262 different companies in the period between 1999 and 2018", "the resulting dataset of 78682 firm-year observations"; label: "we label the fiscal year before the chapter filling as "Bankruptcy" (1) for the next year. Otherwise, the company is considered alive (0)" (Chapter 11 or Chapter 7, per the SEC). Header (previewed): company_name (anonymised `C_n`), fyear, status_label (alive/failed), X1-X18, Division, MajorGroup (SIC). The Kaggle copy (utkarshx27, 2023, CC0) is the same data without the SIC columns and names X1-X18 (current assets, COGS, D&A, EBITDA, inventory, net income, receivables, market value, net sales, total assets, long-term debt, EBIT, gross profit, current liabilities, retained earnings, revenue, total liabilities, operating expenses). "The non-anonymized version of this dataset can NOT be available because of the license used to retrieve the dataset"; the vendor is not named.
- Use case: a lender or investor scores a listed firm from its latest annual accounts for a filing within a year; the paper's own statement of who acts was not read (the MDPI pages returned 403), so the fit is approximate for now; regime temporal: the source trains on 1999-2011, validates on 2012-2014 and tests on 2015-2018 (README), with firms repeated across years.
- Siblings and duplicates: `polish_companies_bankruptcy` (`Yes`), `taiwanese_bankruptcy_prediction` (`Yes`), `qualitative_bankruptcy` (`No`), `analcatdata_bankruptcy` (`No`), `company_bankruptcy_prediction` (`No`), `v4finbench_corporate_distress` (unscreened, a rule-defined distress label for Visegrad firms): other sources, no duplicate (PROV-4). The Kaggle upload is a copy of this source, kept on this record. External collections: none found; the curator's Zotero items 49 and 182 use it.
- Better data: found as better data for `polish_companies_bankruptcy`, `qualitative_bankruptcy` and `taiwanese_bankruptcy_prediction`; no further search this round.
- Papers and pages: the Future Internet paper; Pellegrino et al. 2024, Future Internet 16(3):79 (an LSTM on the same data, cited in the README); GitHub sowide/Multi-modal-bankrutpcy.
- Metric: the paper proposes "AUC, precision, recall, type I error, type II error, and macro- and micro-F1" for future benchmarking and leads with AUC (random forest 0.748 on average), with no threshold fixed: several metrics side by side, so the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none. Read from search snippets; the full text was not reachable.
- Risks for /add-dataset: in the preview, values jump by a factor of 1,000 inside one firm's series (C_1: X2 740998 in 1999, 701.854 in 2000; X14 606337 in 2002, 651.958 in 2003, 897284 in 2005), the pattern of a decimal point read as a thousands separator when a value has three decimals; repair it from the origin or by a documented rule (`Data Quality Issue`, PROV-13). X14 and X17 are identical in all 24 previewed rows, and X1 (current assets by the Kaggle names) exceeds X10 (total assets) wherever both are on one scale, so the names need the paper's table. Whether `failed` marks only the year before the filing or every year of a firm that failed decides the label (USE-5); firms delisted for other reasons stay `alive`. Check what `dataset_paper.zip` holds (possibly the paper's own split files).
- Priority: gap 0 (finance, binary and temporal are not thin), use case 0 (the paper's statement not read), source + (a paper and the authors' repository), shape + (78,682 firm-years with a temporal split), risk - (the decimal corruption, the column names, the label's semantics).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `polish_companies_bankruptcy`, `qualitative_bankruptcy`, `taiwanese_bankruptcy_prediction`; the curator's Zotero collection, item 182: "V4FinBench: Benchmarking Tabular Foundation Models, LLMs, and Standard Methods on ..."; the curator's Zotero collection, item 49: "Are Foundation Models Useful for Bankruptcy Prediction?".
- as published: 78,682 firm-years of 8,262 US public companies (NYSE, NASDAQ), 1999-2018; 18 accounting variables (X1-X18: current assets, COGS, EBITDA, net income, total assets, long-term debt, retained earnings, ...; target: bankruptcy (Chapter 7 or Chapter 11 filing) in the following year, binary, labelled on the fiscal year before the filing; access: open.
- Why: same task as polish_companies_bankruptcy: firm-year financial statement data, target bankruptcy within the next year, features known at the fiscal year end | the same task as the Taiwan record: listed firms, legal bankruptcy as the target, financial-statement features of the year before | Same target (corporate ...
- Adds: almost twice the firm-years (78,682 vs about 43,000), 20 years instead of 2000-2012, raw accounting items instead of pre-engineered ratios (the Polish record notes the features were already engineered), a population (all listed US firms) rather than a sample, and a published temporal split; no missing values | 11.5 ...

**Assessment (AI, 2026-11-25):** correction to today's screening (/add-dataset): the source's CSV has two releases on GitHub. The first (commit 7f56a80b, 2022-07-26, published with the paper) keeps its decimal points and orders its columns as the paper's Table 2; the current one (commit 279e4275, 2024-04-10) lost the points, reordered the columns and added `Division` and `MajorGroup`. The settled repair (a token without a point divided by 1,000) reproduces the 2022 release in 100% of cells, which the definition asserts. So the screening's "the Kaggle names and the paper's own Table 2 ... are wrong for the CSV" holds only for the 2024 file: Table 2 names the 2022 file correctly. The 2022 file marks every year of a failed company as well, so the relabel stands.

**Assessment (AI, 2026-11-25):** further corrections to today's screening from the review panel: the paper's AUCs (best test 0.861) were scored on about one sample per company (Table 4: 105 positives of 3,345 samples, 3.1%), so they are not comparable with the Baselines line's firm-year scores; the four accounting identities hold in all but 1 to 3 rows each, not in 100%; the split is now eleven one-year windows, fiscal 2018 back to 2008, with no gap (the Split line's three windows and one-year gap were reversed: the window length rested on a misread rule, and the gap showed no shortcut at equal training size, +0.007 ROC AUC); the fit is approximate, since no filing dates ship and the horizon cannot be verified.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: the protocol line for a test row's next-year row (LEAK-9, settled: added), the gap (SPLIT-10, settled by a measurement at equal training size: none), the window length (SPLIT-12, SPLIT-15, settled: one year, the three-year windows having misread SPLIT-14 and TP-9); for the curator: issues H and 1-2. Priority 2: gap 0 (finance, binary and temporal are not thin), use case 0 (named by the source, but the fit is approximate: the horizon cannot be verified), source + (a dataset paper and the authors' repository, both releases pinned), shape + (78,682 firm-years, 20 features, temporal panel), risk - (a test row's next-year row in the file gives its label away, closed only by a protocol line, issue 2).

CC (2026-11-25, Andrej): review of the added dataset (Review H, 1, 2):
- Nine windows (issue 1): 2008 and 2018 kept; of the years between, the two with the fewest bankruptcies leave, 2017 (21) and 2009 (23). Tested years 2018, 2016-2010 without 2009, and 2008.
- Asked whether the next-year rows can leak inside a split (they cannot: only the whole file holds them) and whether the company id should be an input; both open (issues 2 and 3).

CC (2026-11-25, Andrej): the declared horizon (one-year windows, an annual refit, no gap; Review H, as implemented) is checked.

CC (2026-11-25, Andrej): review issue 2, a: "Reply (a): Keep the protocol line." The line stays in the notes and the splits comment; inside a split nothing leaks, and the line guards only a method that reads the whole shipped file.

CC (2026-11-25, Andrej): review issue 3, B: "Option B: The id as a categorical input." `company_name` ships as `company` (8,971 levels), categorical: a lender knows which company a statement belongs to.

**Assessment (AI, 2026-11-25):** marks applied. Issue 3: `company` ships as a categorical input (21 features); the notes' bullet on the dropped id, the protocol bullet and the splits comment now say it ships. `dataset check`: 0 errors, 0 warnings (1 accepted), 1 info. Task probe on 5 of the 9 windows: random forest ROC AUC 0.920, LightGBM 0.915, linear 0.832, `net_income` alone 0.793, no flags (before the id, on 5 of the then eleven windows: 0.916, 0.908, 0.829 and 0.794; the measured effect of the id is the review's table, +0.002 on average). Issue 2: no change.

CC (2026-11-25, Andrej): the declared metric (roc_auc, the source's: Lombardo et al. 2022, Section 8) is checked, as implemented.

CC (2026-11-25, Andrej): the declared split (temporal on `fyear`: nine one-year windows, 2018, 2016 to 2010 and 2008, each trained on every earlier year, no gap) is checked, as implemented.

CC (2026-11-25, Andrej): verdict ship; nothing open in the review. The build is stale until rebuilt.

## Review

**Outcome:** added. The AI recommends shipping it as now defined: the panel's recommendation was ship after changes, and every change is made. 78,682 firm-years of US listed companies (fiscal years 1999-2018) with 17 statement items, the fiscal year, the anonymised company id (`company`, categorical, Andrej 2026-11-25) and the SIC division and major group; the target is Yes on a failed company's last fiscal year (609 events, 0.77%), the source's own label, which matches the paper's Table 1 one year later in all 20 years. The decimal points the 2024 release lost are restored, and `_clean` asserts every repaired cell against the source's July 2022 release. Split: nine one-year windows, fiscal 2018 back to 2008 without 2017 and 2009, each trained on every earlier year with no gap (52.3% to 96.5% of the rows), metric ROC AUC (the source's). Validity: no column leaks (the best single feature, `net_income`, scores 0.83 on the builder's earlier three-year windows; recording markers alone 0.53); a test row's next-year row of the same company gives its label away to a method that reads the whole file (never inside a split), guarded by a protocol line, kept by Andrej (issue 2). Value: untuned LightGBM scores ROC AUC 0.85 to 0.95 per window (mean 0.915 over 2009-2018); the task probe on 5 of the 9 windows, with the company id: random forest 0.920, LightGBM 0.915, linear 0.832, `net_income` alone 0.793, no flags. No exact copies across the split; 7.8% of test rows have a near copy in training, the same company's previous year. `dataset check`: 0 errors, 0 warnings (the early-year and large-sector base rates accepted as not leaks), 1 info. Not built.

**Main points:** Settled 2026-11-25 by Andrej: the horizon (one year, annual refit, no gap), nine windows with 2008 and 2018 (issue 1), the protocol line kept (issue 2, a) and the company id shipped as a categorical input (issue 3, B). Nothing open.

**Record judgment:** The panel reversed two calls of the builder's draft, and the definition now ships the panel's version. The three-year windows rested on a misread rule (a window was widened to hold 33 bankruptcies, while the floor counts scored rows and few positives in a window are part of the task); they also left a test row's next year inside its own test window. They are now one-year windows, as in the other yearly panels. The one-year gap was measured at equal training size and showed no shortcut (+0.007 ROC AUC on average for the newest training year), so it is dropped, as in lt_vehicle_loan_default_prediction, wisconsin_local_government_property_insurance_fund and spanish_homeowners_motor_insurance_2010_2014, and fiscal 2008, the recession filings, becomes an ordinary window. Changed without a decision, as the panel settled: `fit` is `approximate` (the horizon cannot be verified: no filing dates), the record carries `Selection Bias` (the firm set of the authors' earlier papers, small caps excluded, as polish_companies_bankruptcy), the label is noted as "bankruptcy while listed" with the measured distress exits, the SIC codes as one lookup per company, the metric note says the paper's AUCs are per company and not comparable, and four numbers in the notes are corrected. Not raised, since the panel agreed with the builder: companies seen in training stay in the test windows (seen and new companies score alike, 0.910 against 0.908), and the previous year's items stay out (−0.013 to +0.010). The screening's statement that the paper's Table 2 names the columns wrongly holds only for the 2024 file (Comments, Assessment of 2026-11-25).

**Horizon:**

* **Verdict:** one-year windows with no gap (medium confidence: the refit cadence is our assumption, the gap is measured).
* **Length:** the source predicts one year ahead ("predict bankruptcy at least one year before it happens", Section 3) and names no refit cadence; statements are annual, so a lender refits once a year, the assumption you sign off[^h12]. The other yearly panels test one year a window (spanish_homeowners_motor_insurance_2010_2014, wisconsin_local_government_property_insurance_fund, college_scorecard, predict_students_dropout_and_academic_success). The builder's three-year windows were chosen so that each held 33 bankruptcies, but the floor counts scored rows (each year holds over 2,700) and few positives in a window are part of the task[^h14].
* **Gap:**
  - The outcome horizon is fixed (a filing in the year after the statement) and every label is final at release, so a fiscal year's labels are known before the next year's statements are filed. A training Yes is a company's last year, so no test company's own label can be in training[^h10].
  - Measured at equal training size (untuned LightGBM, 3 seeds; the no-gap training side subsampled to the gapped size), the newest training year adds +0.007 ROC AUC on average over 2009-2018, inside the spread of single windows:

    | Test year | Rows | Events | Train share, gap | Train share, no gap | Gap | No gap, equal size | No gap, full |
    |---|---|---|---|---|---|---|---|
    | 2018 | 2,723 | 36 | 92.7% | 96.5% | 0.894 | 0.912 | 0.911 |
    | 2017 | 3,014 | 21 | 88.7% | 92.7% | 0.931 | 0.918 | 0.927 |
    | 2016 | 3,191 | 29 | 84.4% | 88.7% | 0.897 | 0.905 | 0.911 |
    | 2015 | 3,354 | 33 | 79.9% | 84.4% | 0.934 | 0.943 | 0.941 |
    | 2014 | 3,504 | 33 | 75.5% | 79.9% | 0.918 | 0.909 | 0.916 |
    | 2013 | 3,484 | 28 | 71.1% | 75.5% | 0.919 | 0.920 | 0.925 |
    | 2012 | 3,485 | 26 | 66.6% | 71.1% | 0.944 | 0.944 | 0.937 |
    | 2011 | 3,513 | 25 | 62.0% | 66.6% | 0.893 | 0.936 | 0.946 |
    | 2010 | 3,625 | 35 | 57.3% | 62.0% | 0.845 | 0.848 | 0.849 |
    | 2009 | 3,743 | 23 | 52.3% | 57.3% | 0.878 | 0.883 | 0.885 |
    | 2008 | 3,857 | 58 | 47.3% | 52.3% | 0.868 | 0.902 | 0.892 |
    | Mean 2009-2018 | | | | | 0.905 | 0.912 | 0.915 |

  - The one residue: fiscal years that do not end in December, whose next-year filings may run past the next statements; the data carry no month, so it cannot be measured.
* **Time frame:** fiscal 1999-2018, the whole release (the source's data end with 2019 filings). The windows cover 2008-2018: a twelfth window, 2007, would train on 47.3%, under the half-the-rows floor. Which windows to keep is issue 1.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One year, no gap (implemented) | Each fiscal year 2008-2018 is tested alone and trained on every earlier year | 11: 2,723 to 3,857 rows, 21 to 58 events; train 52.3% to 96.5% | annual statements and an annual refit; the gap measured unneeded; tests the 2008 recession filings; follows the yearly-panel precedents | each window's AUC is noisier (21 to 58 events); the annual refit is our assumption |
  | B | One year, one-year gap | As A, each training side ending a year before its test year | 10: 2,723 to 3,743 rows, 21 to 36 events; train 52.3% to 92.7% | safe if some labels arrive late (fiscal years not ending in December) | no shortcut measured; drops the newest training year; 2008 falls under the floor and is not tested; departs from the no-gap precedents |
  | C | The source's periods, one-year gap (the builder's draft) | Tests 2015-2018, 2012-2014 and 2009-2011, training up to 2013, 2010 and 2007 | 3: 12,282, 10,473 and 10,881 rows, 119, 87 and 83 events; train 79.9%, 66.6%, 52.3% | follows the source's validation and test periods; a steadier score per window | rests on the misread 33-events argument; 3 windows against a target of 9; the 2018 rows are scored by a model trained up to 2013; 2009-2011 is not the source's; a test row's next year sits in its own window (the next-year flag alone scores ROC AUC 0.85, 0.81, 0.81) |
  | D | Two years, one-year gap | Tests 2017-2018 back to 2009-2010 | 5: 5,700 to 7,400 rows, 51 to 62 events; train 52% to 89% | fewer, steadier windows | no source points to two years; the next-year row is back inside each test window; 5 windows against 9 |

* **Recommendation:** A: one year is the source's horizon and the cadence of the statements, and no gap is what the rule asks for once the measurement shows no shortcut; it is also the only option that tests a downturn without an exception to the half-the-rows floor. **Decision:** sign off A, or change to B, C or D?

**Notes for the AI:** A is implemented: `Temporal(on="fyear", splits=TemporalSplits(window=1, unit="unique", n_windows=11), horizon=1, horizon_unit="years", time_unit="years")`, leaf `L-ORDER.windows`. For B add `gap=1` to `TemporalSplits` and `Temporal` (`gap_unit="years"`) and set `n_windows=10`; for C or D restore the windows in `_make_splits` (fixed windows of unequal length) and add the next-year leak to the protocol bullet as within-window. On any change rewrite `task_summary.split`, the splits comment's length and gap paragraphs and the window table; re-run `dataset check` and the task probe. The gap table is the panel's measurement (2026-11-25); the window counts are from `dataset windows` with `--window 1 --unit unique` at gap 0 and 1.

[^h12]: **SPLIT-12** (Should): the horizon is a human judgment from the source (how far ahead the actor predicts, the refit cadence); the splits comment names the horizon, the cadence, the gap and the time unit, or says the source is silent and what is assumed.
[^h14]: **SPLIT-14** (Must): at least 3 windows, each training on at least 50% of the data, each test window with at least 33 scored units (here rows). **TP-9** (Must): "Few positives in a window are part of the task, not a reason for `Too Small` or for another split".
[^h10]: **SPLIT-10** (Should; amended 2026-11-04 and 2026-11-05): a gap of about the label's delay, but the measurements decide; no gap where a fixed outcome horizon leaves no training label selected by its outcome and the newest labels add nothing beyond their size, stated at equal training size (cases lt_vehicle_loan_default_prediction, wisconsin_local_government_property_insurance_fund). **SPLIT-9** (Must): no training label that tells a test row's outcome and was not known at its prediction point.

**Andrej (2026-11-25, ok):** as implemented.

**Resolved (2026-11-25, Andrej):** A: one-year windows, an annual refit, no gap. Which years are tested is issue 1.

**Issues for Andrej:**

1. **Keep all eleven yearly windows, or nine?**

   - **Problem:**
     - Every fiscal year from 2008 to 2018 keeps half the rows for training, so the definition ships all 11 as windows, two more than the target of 9, the number of evaluations a random split of this size gets[^acb15].
     - Beyond the newest year, which windows to test is a choice from the use case, and fiscal 2008, the 2009 recession filings, is the only downturn year among them (58 events, 1.5%, against 0.6% to 1.3% in the other years).
   - **Effect on the task:** a credit model is judged above all on downturns (the domain practitioner), so dropping 2008 leaves no crisis year in the test; two windows more cost two more fits for every method.
   - **Experiments:** the windows as shipped, from the definition's splits:

     | Test year | Test rows | Events | Train share |
     |---|---|---|---|
     | 2018 | 2,723 | 36 | 96.5% |
     | 2017 | 3,014 | 21 | 92.7% |
     | 2016 | 3,191 | 29 | 88.7% |
     | 2015 | 3,354 | 33 | 84.4% |
     | 2014 | 3,504 | 33 | 79.9% |
     | 2013 | 3,484 | 28 | 75.5% |
     | 2012 | 3,485 | 26 | 71.1% |
     | 2011 | 3,513 | 25 | 66.6% |
     | 2010 | 3,625 | 35 | 62.0% |
     | 2009 | 3,743 | 23 | 57.3% |
     | 2008 | 3,857 | 58 | 52.3% |

   - **Panel:** the mediator recommends keeping 2008, with either all 11 windows or 2008 plus 8 of 2010-2018; the split auditor and the domain practitioner asked for the recession year.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All 11, 2008-2018 (implemented) | Every eligible year is a window | keeps the recession year; no year dropped by choice; more evidence over a decade | two windows over the target of 9; two more fits for every method |
     | B | The newest 9, 2010-2018 | `n_windows=9` | exactly the target count | no downturn tested; walks back from the newest without a use-case reason |
     | C | 2008 and 2011-2018 | Nine windows, the recession year kept, 2009 and 2010 left out | the target count with the downturn kept | which two years go is arbitrary; 2009-2010, the recovery, untested |

   - **Recommendation:** A: it keeps the downturn without choosing which ordinary years to leave out, and two extra yearly windows are cheap on 78,682 rows. **Decision:** keep A, or change to B or C?

   **Notes for the AI:** B: `TemporalSplits(window=1, unit="unique", n_windows=9)`. C: `TemporalSplits(window=1, unit="years", cutoffs=(2008, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018))` (check that `fyear` works with calendar cutoffs; otherwise build the windows in `_make_splits` from a `TEST_YEARS` constant). For B or C, add to the splits comment the count 9 against the target of 9 and the reason for the years left out, and re-run `dataset check`.

   [^acb15]: **SPLIT-15** (Must for the newest window, Should for the others): the newest window is always tested; the others are the curator's choice from the use case (other years first); the number aims at **SPLIT-33**'s count for two thirds of the scored units, here 9 (3 repeats of 3-fold for a training side of 2,500 to 250,000 rows).

   **Andrej (2026-11-25, discuss):** Use 2008 and the last year and find a heuristic how to drop years to get to 9 windows.

   **Resolved (2026-11-25, Andrej):** nine windows: 2018, 2016, 2015, 2014, 2013, 2012, 2011, 2010 and 2008. The first and the last eligible year stay, as asked; of the nine years between them, the two with the fewest bankruptcies leave, 2017 (21) and 2009 (23), whose scores are the noisiest. The rule reads event counts, never a model's score, and the two years stay in the training sides of the later windows. `TemporalSplits(window=1, unit="unique", cutoffs=(2008, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2018))`; `task_summary.split` and the splits comment say so (301 of the windows' 303 bankruptcies are of companies seen in training). `dataset check`: 0 errors, 0 warnings. Another rule (even spacing, or the two years nearest the target's middle) is a one-line change.

2. **Keep the later rows of each test year in the shipped file, under a protocol line?**

   - **Problem:**
     - Whether a test row's company has a row in the next fiscal year gives its label away (a Yes row is a failed company's last row, so a row with a successor is always No), and the shipped file holds that next year for every test year but 2018.
     - The company ids do not ship, but linking each row to its successor from the features alone lifted the mean ROC AUC from 0.867 to 0.938 on the builder's earlier three-year windows.
     - One-year windows move the successor out of the test window but not out of the file, and the format has no way to ship a split's data cut at its last test year.
   - **Effect on the task:** a method that reads other rows of the file can score far above an honest model; one that predicts each test row from the training rows and its own features cannot use it.
   - **Experiments:** the link rebuilt by the task gamer on the earlier three-year windows (untuned LightGBM, 3 splits, mean ROC AUC):

     | Model | Mean ROC AUC |
     |---|---|
     | Features only, no link | 0.867 |
     | Plus the next-year link rebuilt from the features, no ids | 0.938 |
     | Plus the next-year link from the true ids | 0.978 |

     The next-year flag per one-year test window as shipped, with the true ids (the ids do not ship):

     | Test year | Events | Next-year row in the file | ROC AUC of "no next-year row" |
     |---|---|---|---|
     | 2018 | 36 | no | - |
     | 2017 | 21 | yes | 0.942 |
     | 2016 | 29 | yes | 0.958 |
     | 2015 | 33 | yes | 0.952 |
     | 2014 | 33 | yes | 0.952 |
     | 2013 | 28 | yes | 0.962 |
     | 2012 | 26 | yes | 0.96 |
     | 2011 | 25 | yes | 0.957 |
     | 2010 | 35 | yes | 0.954 |
     | 2009 | 23 | yes | 0.956 |
     | 2008 | 58 | yes | 0.969 |

   - **Consistency:** the same channel (an entity's later row, found from shipped columns, gives the earlier row's outcome) was closed by a protocol line in loan_default_prediction_imperial_college and spanish_motor_insurance_coverage_level_2022_2024[^l9].
   - **Panel:** the critic asked for the line, the advocate first called the later rows a layout question for every temporal dataset and then accepted the line; both agree the cut of the file is a question across datasets.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Protocol line (implemented) | The file is unchanged; each test row is predicted from the training rows and its own features only, and a method that reads another row of the same company is called out and not benchmarked | follows the two precedents; no data or format change | the channel stays in the file; the benchmark must check each method |
     | B | Cut each split's data at its last test year | Raise across datasets a format in which a split ships only the rows up to its last test year | closes the channel in the data, for every temporal panel | a format change for the whole collection; not possible for this dataset alone |

   - **Recommendation:** A for this dataset; B, if you want it, goes to the items across datasets, since every temporal panel ships its later rows the same way. **Decision:** keep A, or raise B across datasets?

   **Notes for the AI:** A is in the curation notes ("Potential leak, kept on purpose") and the splits comment ("Protocol"). For B, write a cross-dataset item in the working copy's `REVIEW.md` (the format change and the datasets it touches); nothing changes in this definition until it is decided.

   [^l9]: **LEAK-9** (Should; amended 2026-11-05): an evaluation leak, where a model can read other test rows, is fixed in the scoring or by a protocol line the benchmark checks, not in the data; a method that learns from the test block is called out and not benchmarked.

   **Andrej (2026-11-25, discuss):** Can we reconstruct the company ids? This would be a feature to be used in the actual use case, right? I also don't see how there can be a leak. For each train/test split we would use all previous years as train and only one year as test, so whether a company is still present the year after is not known?

   **Answer (AI, 2026-11-25):** you are right: inside a split nothing leaks; the line only guards a method that reads the whole shipped file.

   * **Problem:**
     - A method is given each split's training rows (every earlier year) and its one test year, so a test row's next-year row of the same company never reaches it, and its presence the year after is unknown, as you say.
     - The channel exists only for someone who reads the whole shipped file, which holds every year: the task gamer worked from such a file, and the protocol line asks that no method do so.
     - The ids need no reconstruction: the file carries them (`company_name`, `C_1` to `C_8971`), and the definition drops them as an identifier; whether they become an input is a choice of its own, issue 3.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the protocol line (implemented) | the notes keep the line for a method that reads the whole file | costs nothing; as the two precedents | guards a case the benchmark's own harness never creates |
     | b | Drop the line | the notes say the next-year row is outside every split, with no protocol | shorter notes | the shipped file still holds the later rows; a method outside the harness could read them |

   * **Recommendation:** a: the line is free, and the file a participant downloads does hold the later rows. **Decision:** a or b?

   **Andrej (2026-11-25, discuss):** "Reply (a): Keep the protocol line."

   **Resolved (2026-11-25, Andrej):** a: the protocol line stays in the curation notes ("Potential leak, kept on purpose") and the splits comment ("Protocol"), now saying that inside a split nothing leaks and the channel is open only to a method that reads the whole shipped file, and that the company id now ships (issue 3). No other change to the definition.

3. **Ship the company id as an input?**

   - **Problem:**
     - A lender knows which company a statement belongs to and its history, and the file carries the id (`company_name`, `C_1` to `C_8971`), so the id can be an input that is known at the prediction point[^acb13].
     - Added as a categorical input, the id changes untuned LightGBM's ROC AUC by +0.002 on average over the nine windows (better on 5 of 9), inside the spread of single windows; the previous year's items add nothing either.
     - Ship the id as an input, or keep it out as an identifier?
   - **Effect on the task:** 92% to 98% of each test year's firm-years are of companies seen in training, so a method can learn a company's own level; a new company has an unseen id.
   - **Experiments:** the nine windows as defined, no gap, untuned LightGBM, 3 seeds, ROC AUC:

     | Test year | Events | As shipped | + company id | + previous year's items | + both |
     |---|---|---|---|---|---|
     | 2018 | 36 | 0.909 | 0.900 | 0.899 | 0.896 |
     | 2016 | 29 | 0.893 | 0.918 | 0.891 | 0.907 |
     | 2015 | 33 | 0.943 | 0.917 | 0.938 | 0.881 |
     | 2014 | 33 | 0.919 | 0.902 | 0.916 | 0.909 |
     | 2013 | 28 | 0.909 | 0.900 | 0.902 | 0.878 |
     | 2012 | 26 | 0.915 | 0.930 | 0.875 | 0.886 |
     | 2011 | 25 | 0.914 | 0.923 | 0.899 | 0.918 |
     | 2010 | 35 | 0.818 | 0.829 | 0.850 | 0.832 |
     | 2008 | 58 | 0.869 | 0.886 | 0.873 | 0.867 |
     | Mean | | 0.899 | 0.900 | 0.894 | 0.886 |

   - **Consistency:** duolingo_spaced_repetition_recall_1m keeps the learner id as an input (your decision of 2026-11-24, its review issue 13, B), and ga_merchandise_store_sessions ships the visitor's history but not the visitor id.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No id (implemented) | `company_name` stays dropped | no high-cardinality code; a model cannot lean on a company's own level | leaves out what a lender knows |
     | B | The id as a categorical input | `company_name` ships as `company` (8,971 levels) | the lender's view; as duolingo's learner id | no measured gain; 8,971 levels for every method to encode |
     | C | B plus the previous year's 17 items | a lagged copy of the items, missing in a company's first year | the history a lender holds | no gain measured, worse with the id; engineered columns |

   - **Recommendation:** B, weakly: the id is known at the prediction point and your duolingo decision keeps such an id; the measurement says it neither helps nor harms an untuned model. A stays reasonable if the code's 8,971 levels weigh more. **Decision:** A, B or C?

   **Notes for the AI:** on B, keep `company_name` in `_clean` (rename to `company`), declare it categorical in `_feature_types`, move the bullet "Dropped: `company_name` ..." to say it ships, and re-run `dataset check` and the task probe. On C also add the previous year's items in `_clean` by company and `fyear - 1`. The experiment: the nine windows, LightGBM with default settings, seeds 0 to 2.

   [^acb13]: **SPLIT-13** (Should): an entity that recurs across the cutoff is part of the task when the model predicts for known entities, and a question when the use case is a new entity. **USE-3** (Must): an input is known at the prediction point.

   **Andrej (2026-11-25, change):** "Option B: The id as a categorical input."

   **Resolved (2026-11-25, Andrej):** B: `_clean` keeps `company_name` and renames it `company` (8,971 levels), and `_feature_types` declares it categorical; the task summary's known inputs name the id; the curation notes' bullet on the dropped id now says it ships and why, and the protocol bullet and the splits comment ("Companies recur", "Protocol") say the id ships. `dataset check`: 0 errors, 0 warnings (1 accepted), 1 info. Task probe on 5 of the 9 windows, 21 features: random forest ROC AUC 0.920, LightGBM 0.915, linear 0.832, `net_income` alone 0.793, no flags.

**Review panel:** ship after changes (mediator). Claims: 21, 12 hold, 5 refuted in part (four wording slips and the paper's metric unit, all fixed in the notes), 4 untested (no filing dates, the vendor, the 8,971 ids). Blind review: include with changes; main concern the label's unchecked timing. Debate: agreed on one-year windows, the approximate fit, `Selection Bias` and the metric note; disputed the protocol line for the next-year rows (settled: added) and the gap (settled by a measurement at equal training size: none). For the curator: the horizon and issues 1-2.

<details><summary>Mediator</summary>

**Mediator report: `american_companies_bankruptcy`**

The advocate and the critic reach the same verdict and the same main fix. I ran two experiments: one settles the gap, the other settles the protocol line.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-5 holds (label moved to the failed firm's last year, matches Table 1 in all 20 years);
  USE-8 triggered, fixed (fit approximate: horizon unverifiable, no filing dates); LEAK-1/LEAK-10 hold (no column
  leaks; SIC looked up once per firm, kept with a note); LEAK-9 triggered (next-year row of the same firm gives the
  label away), fixed by a protocol line; PROV-13 holds (repair asserted cell for cell against the 2022 release);
  SPLIT-10 gap: no shortcut at equal training size, so no gap (decisive experiment below); SPLIT-12/15: 3-year windows
  rest on a misread of SPLIT-14/TP-9, re-split to 1-year windows (curator signs the horizon).
Value: TP holds (honest AUC 0.84-0.94 per year window); MET-5 roc_auc kept, note that the paper's AUC is per company.
Quality: wording fixes (identities, 0.49, event counts), derived columns named.
Weighed: size +, source +, real use case +, selection - (Selection Bias marker), accounting-only inputs -.
For the curator: issue 1 (window length and which windows, horizon sign-off); issue 2 (collection-wide cut of later
  rows, cross-dataset).
```

**Changes to make now (no decision needed)**

1. **LEAK-9 protocol line** in `curation_comments` and `splits_comment`, worded as in loan_default_prediction_imperial_college: "each test row is predicted from the training rows and its own features only; no feature or model step may use other rows of the file; a method that reads another row of the same company is called out and not benchmarked". The 1-year windows do not close this channel; they make it stronger.
2. **`fit="approximate"`** (USE-8). `fit_reason` names the unverifiable horizon and the accounting-only inputs.
3. **Notes in `curation_comments`** (USE-5, LEAK-10):
   - The label means "bankruptcy while listed". Exits for distress stay No: among No rows they score AUC 0.60, 0.64 and 0.58, and they make up 11–19% of the top 1% of scores.
   - A last statement may have been published after the filing. This cannot be checked, and the subject-to-compromise test found no sign of it.
   - SIC codes are one lookup per company.
4. **`Selection Bias` marker** on the record. The Selection bullet gets the 1999–2002 event counts (3, 7, 10, 17) and the gap between 8,971 company ids and the 8,262 stated. This follows polish_companies_bankruptcy.
5. **Metric note** (MET-5, MET-6):
   - `roc_auc` stays.
   - The paper scored about one sample per company (3,345 samples, 3.1% positive), so its 0.861 is not comparable with our baselines. Remove that comparison from the record.
   - Quote Sections 8.1 and 9 exactly, and add "no threshold fixed".
6. **Wording fixes** (EV-2):
   - "every row" becomes "all but 1–3 rows".
   - `ebitda`, `gross_profit` and `total_operating_expenses` are named as derived columns (operating expenses is off in 4 rows).
   - The id's Spearman correlation with first year is 0.49, not 0.59.
   - "21 to 59 events" holds only for 2003–2018.
7. **`splits_comment`:** drop the "33 events SPLIT-14 asks for" argument (it misreads SPLIT-14 and TP-9). Set `Temporal(horizon=...)` to match the windows; today `horizon=3` sits beside a 4-year window.
8. **Accept `dataset_pure_feature_value`** with its reason: early years and large sectors are base-rate effects, not leaks.

**Issues for the curator, ranked**

**1. Window length and which windows (P4; SPLIT-12 Should, the curator signs the horizon; SPLIT-15 Should; SPLIT-10 Should).**
- **Problem:** the 3-year windows rest on a misread rule and leave 3 windows against a target of 9. The 2018 rows are scored by a model trained up to 2013. Inside a 3-year window, the test rows themselves show which firms have a next-year row (flag AUC 0.85, 0.81, 0.81).
- **Both sides:** both want 1-year windows (annual statements, annual refit). The split auditor and the precedent checker agree, as do the yearly-panel precedents (spanish_homeowners, wisconsin, college_scorecard, predict_students_dropout).
- **Gap, settled by measurement.** I compared 1-year windows with and without the gap at equal training size (no-gap training side subsampled to the gapped size; LightGBM, 3 seeds).

  | | gap 1 | no gap, equal size | no gap, full |
  |---|---|---|---|
  | mean AUC, 2009–2018 | 0.905 | 0.912 | 0.915 |
  | per window, no gap (equal size) minus gap | −0.013 to +0.044; 7 of 10 positive, 9 of 10 within ±0.02 | | |

  The labels are final at release and the horizon is fixed. A training Yes is a firm's last year, so no test firm's own label can be in training (SPLIT-9 cannot arise). SPLIT-10 as amended therefore means no gap, with +0.007 (equal size) stated in the notes. This matches lt_vehicle_loan_default_prediction, wisconsin and spanish_homeowners. One residual: fiscal years that do not end in December. It cannot be measured, because the data carry no month.
- **Decision needed:** sign off the horizon (1 year, annual refit, gap 0). Then choose the windows. Without the gap, 11 yearly windows are eligible (2008–2018, all ≥52.3% train, 21–58 events). SPLIT-15 aims at 9, the newest is a Must, and the others are your choice from the use case.
  - **Recommended:** keep fiscal 2008, the recession filings (58 events, 1.5%). The domain practitioner says a credit model is judged on downturns. Either ship all 11, or 2008 plus 8 of 2010–2018.
  - **Alternative:** keep the source's periods under SPLIT-19 with the comment fixed. This is weak, because 2009–11 is not from the source.

**2. Later rows stay in the shipped file (P4; LEAK-9, protocol; cross-dataset).**
- **Problem:** after the re-split, every test year but 2018 still has its next year in `data.parquet`. With true ids, "no row in t+1" scores AUC 0.94–0.97 in each of the 10 windows 2008–2017. Matching rows on features alone recovers most of that: the task gamer measured +0.035 to +0.115 on the old windows.
- **Advocate:** the protocol line covers this dataset. Cutting the file per split is a layout question for every temporal dataset.
- **Critic:** the LEAK-9 precedents settle it per dataset with the line.
- **By rule:** both agree on the line (change 1). What stays open is whether the collection should ship each split's data cut at its last test year (the task gamer's fix).
- **Decision needed:** a cross-dataset item for the working copy's `REVIEW.md`. It does not block this dataset.

**Agreed facts (both sides, measured)**

- The target equals Table 1 one year later in all 20 years (609 events). The published label (every year of a failed firm) is wrong for the task.
- The repair reproduces the July 2022 release in every cell. No duplicate rows, no copies across the split, no column leaks. The best single feature is `net_income` at 0.83, and recording markers alone give 0.53.
- 82–88% of test firm-years belong to firms seen in training. Seen and new firms score alike (0.910 against 0.908).
- 1-year windows from 2009 give 10 windows (2.7k–3.7k rows, 21–36 events, train 52.3–92.7%). Without the gap, 2008 is an eleventh window at 52.3%.
- The horizon cannot be verified (no filing dates). Exits for distress stay No. The firm set is fixed by the authors' earlier papers, which excluded small caps.
- `roc_auc` is the source's deliberate choice, with no threshold fixed. The paper's AUC is per company, not per firm-year.

**The task gamer's exploits, mapped**

| # | Exploit | Rule | Kept-on-purpose note or accepted warning? | Status |
|---|---|---|---|---|
| 1 | Next-year successor matched on features (+0.035 to +0.115) | LEAK-9 (evaluation leak) | none (no `Potential leak, kept on purpose:` note; `accepted: {}`) | **new**: within-window part removed by 1-year windows; later rows covered by the protocol line (change 1) and issue 2 |
| 1a | Same with true ids, by lookup in the public CSV (0.978) | LEAK-9; ceiling of 1 | none | new; same remedy |
| 1b | Plain nearest-neighbour distance (+0.013 mean, −0.097 to +0.096) | LEAK-9 | none | new, inside noise on the mean; same remedy |
| — | Formats, row order, drift, transforms | LEAK-39, PROV-4 | — | nothing found |

**Consistency with precedent**

- **Follows precedent:**
  - the relabel (ames_housing, rain_in_australia);
  - the PROV-13 repair;
  - known firms in the test windows (spanish_homeowners, wisconsin, diabetes_130_us);
  - `roc_auc` (lt_vehicle);
  - yearly windows (the four yearly panels);
  - no gap (lt_vehicle, wisconsin, spanish_homeowners; the equal-size measurement is the fact SPLIT-10 asks for);
  - the protocol line (loan_default_prediction_imperial_college, spanish_motor_insurance_coverage_level_2022_2024);
  - `Selection Bias` (polish_companies_bankruptcy).
- **Departures:** none left once the changes are made. Keeping the 3-year windows or the gap would each depart from these precedents, and no fact sets this case apart. If the curator keeps either, ask them to reflect first.

</details>

<details><summary>Claim audit</summary>

I found no validity problem in `american_companies_bankruptcy`. The target, the repair and the split all hold under tests that could have refuted them. Three things need fixing or a sentence in the notes. The most important: the paper scored its AUC on a different unit and class balance than ours, so its AUC figures can't be compared with our baselines.

I read the paper's full text from MDPI's file host (mdpi-res.com), after mdpi.com refused direct downloads.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Target Yes = a failed company's last fiscal year: 609 events (0.77%); per fiscal year this equals the paper's Table 1 one year later | `predicted`, curation notes (Label), Decision 2 | Read Table 1 from the PDF and compare it with the raw CSV, year by year, for all 20 years | **holds, strongly** | Rows per fiscal year t equal Table 1's "Total Firms" in year t+1 for every year (5,308 … 2,723, total 78,682). Events per year t equal "Bankrupt Firms" in year t+1 for every year (3, 7, 10 … 21, 36; total 609). No company carries both labels. The paper (Sec. 3) labels "the fiscal year before the chapter filing". | USE-5 |
| 2 | Tokens without a decimal point divided by 1,000 restore the July 2022 values in every cell | curation notes (Decimal points), `_clean` asserts | Load through the definition (the assertions run), and count tokens without a point in the 2022 file | holds | The assertions pass when the data loads. The 2022 file has 0 tokens without a point out of 1,416,276. | PROV-13 |
| 3 | After the repair, EBIT + D&A = EBITDA, COGS + gross profit = revenue, CA ≤ TA and CL ≤ TL "in every row" | curation notes (Column names) | Recompute on the data | **refuted (wording only)** | They hold in 99.996% to 99.999% of rows, not all. EBITDA fails in 3 rows (e.g. 13.461 + 3.316 ≠ 25.895), COGS + gross profit = revenue fails in 2, CA ≤ TA in 1, CL ≤ TL in 2. The column naming itself holds. | EV-2 |
| 4 | The column names follow the split files and agree with the 2022 Table 2 | `ITEMS` / `ITEMS_2022` | Same check as #2, plus Table 2 read from the PDF | holds | Table 2 matches `ITEMS_2022` (X1 current assets … X18 operating expenses). | PROV-13 |
| 5 | ROC AUC is the source's metric (`Metric.source`): "the paper's selection criterion (Sections 6 to 8)" | `metric`, README Metric block, notes | Read Sec. 5, 6.1, 8 and 9 | **holds on the function; refuted on the unit and balance** | Sec. 8: "we compared all the models in terms of the AUC, and we identified the best model ... using this metric", so it is one deliberate choice. But Table 4 (WL=1) shows the paper's test set (2015-18) has TP+FN = 105 positives and FP+TN = 3,240 negatives: 3,345 samples, 3.1% positive. Sec. 5 says "~96–97%" healthy. Ours has 12,282 firm-years with 119 events (0.97%). The paper scored about one sample per company of the test period, not every firm-year. | MET-2, MET-10, MET-11 |
| 6 | "Its conclusions add that macro-F1 and per-class precision and recall should be read beside it" | notes (Metric), record screening | Read Sec. 8.1 and 9 | **refuted (understated)** | Sec. 9: AUC is questioned, "precision, recall for the single classes, and the macro-F1 score would better define the models' performance". Sec. 8.1: a regulatory body "should design and compare the ML models using the macro-F1 score and then the AUC". No threshold or costs are fixed, so the metric itself still stands: macro-F1 is barred by MET-6, and the MET-8 fallback would be roc_auc anyway. | MET-5, MET-6, MET-8 |
| 7 | Metric is computable on every fold | MET-2 | Random scores on each fold; count events | holds | Both classes in every fold, 119 / 87 / 83 events; random AUC 0.52 / 0.52 / 0.53. No scoring columns are needed. | MET-2, SPLIT-14 |
| 8 | Windows 2015-18, 2012-14, 2009-11; train up to 2013 / 2010 / 2007; 62,896 / 52,414 / 41,189 train rows; 457 / 378 / 262 train events; 119 / 87 / 83 test events | `splits_comment` | Count from the definition's splits | holds | Every count reproduced. | SPLIT-10, SPLIT-14 |
| 9 | 83.9%, 81.5% and 88.3% of test firm-years are of companies with earlier training years, holding 108 / 80 / 81 events | `splits_comment` | Map rows back to company ids | holds | 0.839 / 0.815 / 0.883; 108 / 80 / 81. | SPLIT-3 |
| 10 | "Before 2009 no window keeps half the rows for training" | `splits_comment` | A 2006-08 window trains on fiscal years up to 2004 | holds | That is 28,847 rows (36.7%). | SPLIT-14 |
| 11 | "Single years hold 21 to 59" events | `splits_comment` | Count events per year | **refuted (wording)** | True for 2003-2018 only; 1999-2002 hold 3 to 17. | — |
| 12 | One-year gap: the year before a window's labels are not all known when its first statements arrive | `splits_comment` | Reasoning on 10-K timing (no filing dates in the data) | holds as a conservative choice; untested on data | A fiscal t−1 label can resolve up to about 12 months after the t−1 statement, which overlaps the release of the t statements. The builder measured no-gap AUC +0.003 to +0.027. | SPLIT-10 |
| 13 | Implied: no row is a copy across the split | — | Hash all features except `fyear` | holds | 0 duplicate feature vectors overall; 0 test rows with an identical training row in any split. | LEAK / PROV-4 |
| 14 | Implied: every feature is known at the prediction point | `known` | Column review; check for rows full of zeros (a "last row" marker) | holds | Year-end statement items, `fyear` and SIC codes only. 0 rows have 10 or more zero items. | LEAK-1 |
| 15 | 5,675 of 8,362 never-failed companies end before 2018; 710 companies miss a year; 8,971 ids | notes | Count | holds | 5,675 / 8,362; 710; 8,971. | — |
| 16 | The company id "is numbered roughly by first year (Spearman 0.59 with it)" | notes | Spearman correlation of id number with first year | **refuted (number)** | 0.49 per company by first year; 0.16 per row by fiscal year. The conclusion that the id is not a feature stands. | — |
| 17 | Every major group lies in its division's range; 73 codes; negatives in 6 / 6 / 13 rows | notes | Check against SIC 1987 ranges; count | holds | 100% in range; 73; 6 / 6 / 13. | CLEAN |
| 18 | The split files match 6,170 of 6,170 firm-years | notes | Not rerun | **untested** | Made redundant by the cell-for-cell check against the 2022 release (#2). | — |
| 19 | `net_sales` equals `total_revenue` in every row | notes | Not rerun by me | **untested** | The builder measured it; low risk. | — |
| 20 | A failed company's last statement is the year before its filing | notes (Note) | — | **untested** | The data has no filing dates; Table 1's agreement shows the source used the same convention. | USE-5 |
| 21 | Vendor; 8,971 ids against 8,262 stated | notes | — | **untested** | Neither the paper nor the README explains the difference or names the vendor ("license used to retrieve the dataset"). | PROV |

**Refuted and untested claims, ranked**

Nothing is refuted at P1 to P5. Every Must-level claim I could test holds: the relabelled target, the repair against the 2022 release, the split counts, no copies across the split, and no feature unknown at the prediction point.

1. **P6, Should: the metric's unit and class balance differ from the source's (#5).** The paper scored its AUC on about 3,345 test samples with 105 positives (3.1%), roughly one per company. We score 12,282 firm-years with 119 events (0.97%).
   - **What it changes:** ROC AUC itself stays. Scoring every firm-year fits the use case of a lender re-scoring each annual statement. But the paper's AUCs (best test 0.861, ANN) cannot be compared with our baselines (0.88 to 0.91), which the record's Baselines line and the screening do.
   - **Mildest remedy:** one sentence in the Metric note. It should say the paper's T1 test set is about one sample per company (Table 4: 105 positives out of 3,345; Sec. 5: "~96–97%" healthy), that we score every firm-year because the use case re-scores each statement, and that the paper's numbers are not comparable. Keep the origin as `source`. A curator who reads the unit change as changing the task could call it a `stand-in`; that would only change the label, not the scores.
2. **P6, Should: the notes understate the paper's own criticism of AUC (#6).** The paper says macro-F1 and per-class precision and recall "would better define the models' performance", and that a regulator should compare models "using the macro-F1 score and then the AUC".
   - **What it changes:** nothing in the declared metric. The paper fixes no threshold, so macro-F1 fails MET-6, and the MET-8 fallback would also be roc_auc.
   - **Mildest remedy:** quote Sec. 9 and Sec. 8.1 exactly in the notes, and add "no threshold fixed (MET-6)".
3. **P7, wording: three numbers in the notes are off (#3, #11, #16).**
   - The identities hold in all but 1 to 3 rows each, not "in every row".
   - Single years hold "21 to 59" events only from 2003; 1999-2002 hold 3 to 17.
   - The id's correlation with first year is 0.49, not 0.59.
   - **What it changes:** nothing material.
   - **Mildest remedy:** replace "every row" with "all but 1 to 3 rows (99.996%)", write "2003-2018 years hold 21 to 59", and write 0.49.
4. **Untested (#18 to #21).**
   - Filing dates: whether some last statements come more than a year before the filing cannot be checked here. Table 1 shows the source used the same convention.
   - The vendor, and why the CSV has 8,971 ids against the 8,262 stated: not documented anywhere I read.
   - The split-file match (#18) and the `net_sales` copy (#19): I did not rerun them. The first is covered by the check against the 2022 release.
   - These are already stated as not checked in the notes; no further remedy is needed.

</details>

<details><summary>Column audit</summary>

I found nothing that blocks shipping. No column leaks, the cleaning reaches the expert state, and the file list is complete. There are two questions for the curator and two small wording fixes.

**What I checked**
- **Files:** HEAD (8bcd8db3) holds `american_bankruptcy_dataset.csv`, `dataset_paper.zip`, `README.md` and `LICENSE.md`. The CSV was last changed in the pinned commit 279e4275; the newest commit only added the zip. `curation_comments` gives a reason for leaving out the zip, the README and the licence. Nothing is missing.
- **Dtype probe:** I read the builder's output. It flags only `MajorGroup` (`numeric_levels`), which is a two-digit SIC code and correctly typed categorical. There are no ordinal columns.
- **Missing values by period:** none in any column. Zero shares are flat across 1999-2018 (long-term debt 21–31%, inventory 23–27%, receivables 2–4%, D&A 0.4–1.6%), so no column starts or stops being recorded within the history.

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| fyear | fiscal year of the statement | yes | int; time column and a feature | fine | – |
| Division | SIC division, decoded from its letter | yes; constant per company in all 8,971, so looked up once at extraction | category, decoded; matches `MajorGroup` | fine, with a note | LEAK-10 (registry precedent: keep with a note) |
| MajorGroup | two-digit SIC major group | as for `Division` | category, 73 codes; written "1", "2" without the leading zero (cosmetic only) | fine | – |
| current_assets | balance sheet item | yes, at fiscal year end | float, decimals repaired; 6 negative; above total assets in 1 row | fine | – |
| total_assets | balance sheet item | yes | float, repaired | fine | – |
| cost_of_goods_sold | income statement item | yes | float; 0.4% zero, 5% in Finance (real or missing, can't tell); 6 negative | fine | CLEAN (zero as missing): no rule tells them apart, leave |
| total_long_term_debt | balance sheet item | yes | float; 26.5% zero, stable by year | fine | – |
| depreciation_and_amortization | income statement item | yes | float; 0.8% zero | fine | – |
| ebit | income statement item | yes | float | fine | – |
| ebitda | = ebit + D&A (off in only 3 rows) | yes | float; a derived column, not a copy | fine | – |
| gross_profit | = revenue − COGS (off in only 2 rows) | yes | float; derived | fine | – |
| inventory | balance sheet item | yes | float; 25% zero, following industry (Services 60%, Finance 67%, Retail 3%), so real zeros | fine | – |
| total_current_liabilities | balance sheet item | yes | float; above total liabilities in 2 rows | fine | – |
| net_income | income statement item | yes | float | fine | – |
| retained_earnings | balance sheet item | yes | float | fine | – |
| total_receivables | balance sheet item | yes | float; 2.8% zero (4.3% on events) | fine | – |
| total_revenue | income statement item | yes | float; 13 negative, kept as recorded | fine | – |
| market_value | market capitalisation at fiscal year end | yes, before the 10-K | float; no zeros | fine | – |
| total_liabilities | balance sheet item | yes | float | fine | – |
| total_operating_expenses | = revenue − ebitda (off in only 4 rows) | yes | float; derived | fine | – |
| bankruptcy_next_year (target) | a failed company's last fiscal year | – | "No"/"Yes" | see question 1 | USE-5 |
| *dropped:* company_name, status_label, net_sales | id; source of the target; copy of revenue | – | correctly dropped | fine | – |

**Questions and fixes, ranked**

1. **Question: some last statements may have been published after the filing (prediction point, Weigh).** The task scores "the latest annual statement". A company that files in the first months after its fiscal year end may publish that 10-K after the filing, so a lender would not have had it before the outcome. The data has no filing or report dates, so this can't be measured. I tested the accounting a post-filing statement would show, where liabilities subject to compromise move out of current and long-term debt:
   - The share of liabilities in neither category stays flat on the event rows: median 0.060, against 0.066 the year before and 0.052 for companies that left for other reasons. Only 2.8% of event rows exceed 0.5, the same as the year before.
   - On event rows, long-term debt falls (its share of liabilities 0.18 against 0.38 the year before) and current liabilities rise (0.64 against 0.45). That fits debt reclassified as current after a covenant default, which happens before the filing.

   So there is no sign of post-filing statements. Mildest remedy: one sentence in `curation_comments` (Note) saying that for a filing soon after fiscal year end, the last statement may come after the filing, that this can't be checked, and that the subject-to-compromise test found nothing.

2. **Fix: SIC is looked up once per company (LEAK-10, applied precedent).** `Division` and `MajorGroup` arrived only with the 2024 release and never change within a company, so they are one lookup at extraction, not the industry of each year. No mechanism ties a change of industry to bankruptcy, and the `tunisian_fraud_detection_challenge` decision keeps registry attributes like this with a note. Remedy: add that note to the `fyear`/`Division` bullet. The verdict stays keep.

3. **Question: very few early events.** Fiscal years 1999–2002 have 3, 7, 10 and 17 events, through the dot-com bust when US public bankruptcies peaked. This fits the selection concern already noted (firm set fixed by the authors' earlier papers, small caps excluded). It only touches training rows (every training side includes them), not any test window. Remedy: add these counts to the Selection bullet so the curator sees them.

4. **Fix: two claims say "every row", which is slightly too strong.** The claim is "EBIT + D&A = EBITDA, COGS + gross profit = revenue, current assets ≤ total assets and current liabilities ≤ total liabilities hold in every row". Above a 0.01 tolerance it fails in 3, 2, 1 and 2 rows. Also, `total_operating_expenses` equals revenue − EBITDA in all but 4 rows, which the notes don't mention. Remedy: change "in every row" to "in all but 1 to 3 rows" and say that EBITDA, gross profit and operating expenses are derived columns. Keep all three: they are not copies, unlike `net_sales`.

There is no training weight, so the weight check does not apply.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The regime, leaf, gap and training sides are sound. The window length is argued from a rule the definition misreads, and the horizon has no sign-off yet.

**Tree walk (SPLIT-36)**
The record's collection type is `Panel Data` (Samples: Over Time, Time: Dated, Target: Fixed Delay, Entities: Recur).
- **[PAN.when]:** predict after the panel. A lender scores each new annual statement.
- **[PAN.units]:** both the same and new companies.
- **[PAN.calendar]:** shared, since `fyear` is one calendar for all companies. This leads to the Order step on `fyear`.
- **[ORDER.order]:** yes, the order is dated.
- **[ORDER.windows]:** yes. At a 1-year window, 10 windows (2009–2018) each train on ≥52.3%.
- **[ORDER.small]:** no. An IID training side would hold about 52k units, far above 2,500.

I reach **L-ORDER.windows**. This matches `split_leaf`, the `Temporal` declaration and the record's `Split:` line. No answer was forced, every answer fit, and no exception was needed.

**Findings, ranked (P4)**

**1. The window length rests on a misread rule; the IID target is reachable (SPLIT-12, SPLIT-15, TP-9 Must).**
- The splits comment says "three-year windows give each window the 33 events SPLIT-14 asks for … so 3 windows instead of the 9 an IID split would get." That is not what SPLIT-14 says. It asks for 33 **scored units**, which here are rows.
- TP-9 says few positives per window "are part of the task, not a reason … for another split". Only a window with no positive is a problem.
- Each single fiscal year holds 2,723–3,743 rows and 21–36 events. None is empty.
- `dataset windows --window 1 --gap 1` (measured): 1-year windows 2009…2018 give 10 windows with train shares 52.3%–92.7%. That reaches the target of 9.
- So "what stops more windows" is the chosen length, not the floor. A 3-year refit cadence is an assumption the source doesn't support. The source states a one-year horizon. Statements are annual, so an annual refit is the natural cadence (our assumption; the source names no cadence).
- The current windows also test long refit lags. The 2018 rows of the newest window are scored by a model trained on years up to 2013, which is 5 fiscal years stale.
- **Mildest remedy:** keep the leaf and put the length to the curator in the Horizon block. Either:
  - re-split to 1-year windows, or
  - keep the source's periods (2012–14 validation, 2015–18 test) under SPLIT-19 as the stated reason. The splits comment must then drop the "33 events" argument and say the IID target is given up for the source's periods.

**2. Note: `Temporal(horizon=3)` while the newest window is 4 years long.** The metadata says one length and the split ships two. State the unequal length in the comment, or align it with whatever the curator decides in finding 1.

**3. Note: crisis year option (SPLIT-14 exception, SPLIT-15).**
- Fiscal 2008 carries the 2009 recession filings: 58 events at 1.5%, against 0.6–1.0% in the windows that ship. No shipped window covers it.
- As a 1-year window it trains on 47.3%. That is under half, so it is a curator's exception, down to the 30% floor.
- The 3-year 2007–09 window would train on 42%.
- Offer it. Don't implement it on the AI's word.

**4. Note: the firm set's late entries are thin (selection, not fixable by a split).**
- Only 87 companies enter in 2017 and 47 in 2018. The panel shrinks from 5,308 to 2,723 companies.
- So the newest window is 84% known companies, probably more than a lender's real book.
- Keep this as the selection note it already is.

**Checks that hold**
- **Gap of 1 fiscal year.** The label is a filing in the year after the statement. For fiscal year F−1, those filings fall during F, so they are not all known when the F statements arrive. Training on years up to F−2 is right (SPLIT-10).
  - The builder measured the no-gap AUC as +0.003 to +0.027 higher (optimistic).
  - Residual risk: a company whose last statement came more than a year before its filing. The data has no filing dates, so this cannot be measured; the notes already say so.
- **Time column (USE-3).** `fyear` is the statement's year, and the prediction is made at release. No outcome is open at a window's start beyond what the gap covers.
- **No input is issued ahead of the time column.** Market value is taken at year end.
- **The newest period is complete.**
  - Rows: 2018 is 0.90× of 2017, and 2017 is 0.94× of 2016. The year-on-year decline holds steady.
  - Target rate: 2018 is 1.32%, against 0.7–1.0% earlier. It is higher, not lower, so there's no sign of a cut that dropped open outcomes.
  - Fiscal 2018 alone scores AUC 0.898 (LightGBM) and 0.916 (logistic regression), in line with other years. That gives no sign that 2018's events include filings two years later.
- **Recurring entities.**
  - The use case scores known and new companies, and no id is a feature.
  - The builder measured AUC on companies seen in training vs new ones as about equal: 0.910 vs 0.908.
  - A company's earlier rows are all No, which is true at the time they were recorded. No earlier label is carried forward (LEAK-44).
- **Train floor.** Every window trains on ≥50%: 79.9%, 66.6% and 52.3%. Every test window holds ≥33 rows (10–12k each).
- **Window choice.** The newest window is included. No near copy of the newest was chosen. The windows were chosen from the source's split, not from a model score.
- **No training weight and no season** (annual data).

**Horizon block (for the curator's sign-off)**
- **Length:** the source states one year ahead (statement → filing next year).
- **Gap:** 1 fiscal year, for the label delay. This is from the source's definition of the label.
- **Refit cadence:** the source is silent. We assume annual, since statements are annual.
- **Time frame:** 2009–2018. Earlier windows fall under 50% training.

| Option | Windows | Train share | Test rows / events per window | Per-window AUC SE (LGBM) |
|---|---|---|---|---|
| **Implemented:** 2009–11, 2012–14, 2015–18 (source periods) | 3 | 52–80% | 10.5–12.3k / 83–119 | 0.015–0.020 |
| 1-year, 2009–2018 | 10 (target 9 reached) | 52–93% | 2.7–3.7k / 21–36 | 0.021–0.032 |
| 2-year, 2009–10 … 2017–18 | 5 | 52–89% | 5.7–7.4k / 51–62 | 0.016–0.026 |
| 1-year + 2008 (exception) | 11 | 47–93% | adds 3,857 rows / 58 events (crisis) | 0.024 |

**Recommendation:** 1-year windows, 2009–2018. They match the one-year horizon and an annual refit, and reach the IID target.
- The per-window AUC error is larger, but it is spread over 10 windows. SPLIT-15's reason for many windows covers this, and SPLIT-17's "widen" applies to rows near 33, which these windows are far above.
- Add 2008 only as the curator's exception.
- If the curator prefers the source's periods (SPLIT-19), keep the split and fix the comment as in finding 1.
- The scores in the AUC-SE column are reported only. None of them decided an option (SPLIT-21).

</details>

<details><summary>Domain practitioner</summary>

**Domain-practitioner report: `american_companies_bankruptcy`**

I read this as a credit analyst at a bank or bond fund who watches a portfolio of US listed issuers. Each year, when a company's 10-K arrives, I re-score it to decide whether to lend, hold, put it on a watchlist or reprice its debt.

**Fit: approximate. The definition says "direct", and I would downgrade it.** The rows, the inputs and the split match my annual review closely. But the target's horizon cannot be checked. The label is "the last statement before a filing", not "a filing within 12 months of this statement". USE-8 lists exactly this as approximate: "a breadth or horizon that cannot be verified". `curation_comments` admits it: "a failed company whose last statement came more than a year before its filing is labelled on that last statement all the same; that cannot be checked here". The per-year counts matching the paper's Table 1 one year later make the horizon plausible, but that is not a check.

**1. Inputs at the prediction point (USE-3, USE-6)**

**What I have.** When the 10-K is filed, about 60 to 90 days after fiscal year end, I have all 17 items. Year-end market value is in a filing I already hold. The fiscal year and the SIC codes are known. None of the inputs is late, and nothing a deployed model would lack.

**What I would always have but is missing**, from most to least important:
1. **Equity market data beyond year-end market value**: trailing stock return, return volatility, share price.
   - These are the core of the standard models for listed firms: Shumway 2001; Campbell, Hilscher and Szilagyi 2008; Merton / KMV distance-to-default; Moody's EDF.
   - The literature finds that the market variables carry most of the signal.
   - The task is therefore "accounting-only default prediction". That is a legitimate and common narrower tool (Altman Z, Ohlson O-score), and the `fit_reason` already names this gap.
2. **Interest expense, cash and operating cash flow are absent.** Interest coverage and cash burn are what an analyst looks at first. Altman Z is fully computable; Ohlson's O-score is not (it needs funds from operations).
3. **Prior-year items and changes.** I always have last year's 10-K. The builder measured that lag features add −0.013 to +0.010 AUC. Leaving them out is fine, but a model can't rebuild them because rows carry no company id. That is a small, deliberate gap.

**2. Target (USE-5)**

I act on **default**, which includes missed payments and distressed exchanges. The dataset gives me Chapter 7/11 filing while listed, which is a proxy. That proxy is standard in academic default studies and acceptable.

I want a **calibrated probability of default** for pricing and capital, and a **ranking** for the watchlist.

Two label problems change what is being predicted:
- **Horizon (above).** A distressed firm often stops filing before it files for bankruptcy. Its last statement can then sit more than a year before the filing and still be labelled Yes.
- **Exits stay No.** The 5,675 firms that leave the panel before 2018 have their last year labelled No. Some of those exits are distress delistings or later bankruptcies that I would count as defaults. I measured this (LightGBM, the shipped windows):
  - Among the No rows, early-exit last years rank above other No rows: AUC 0.60 / 0.64 / 0.58 for the windows 2015-18 / 2012-14 / 2009-11.
  - They make up 11%, 19% and 13% of the top 1% of scores, against about 7% of all rows.
  - So part of what the model flags as false positives are probably real distress cases. This is label noise. It holds every model back by the same amount and is not a leak, but it caps how meaningful the top of the ranking is. Worth one line in `curation_comments`: the label is "bankruptcy while listed".

**3. Row and test data (USE-10)**

- **One row is one annual credit review of one issuer.** That matches my decision.
- **The test windows are later fiscal years, and 82 to 88% of test firm-years belong to firms seen in training.** That is my case: I monitor a known portfolio and add new names now and then.
- **The one-year gap is right.** When I score fiscal 2014 statements I don't yet know which fiscal 2013 firms will file in 2014.
- **The windows cover only 2009 to 2018.** That leaves out the 2001 and 2008 crisis waves. A credit model is judged above all on downturns, so this is a weakness, not an error. The builder's option D (adding a 2007-09 window) is the one I would ask about.

**4. Would I use it?**

**As a benchmark of accounting-only PD models, yes.** I would trust these points:
- The baselines are believable: AUC 0.88 to 0.93, and Altman-type ratios with logistic regression alone reach 0.88 to 0.91. That is the range expected for one-year bankruptcy prediction.
- The decimal-point repair is asserted against the 2022 release.
- Failed firms' last years look the way distress should: median market value / total liabilities 0.27 against 2.27 overall, and positive net income in 15% of them against 57% of other rows.

I would distrust:
- the unverifiable horizon;
- a firm set fixed by earlier papers, small caps excluded (the paper itself says the bankruptcy rate "can be underestimated");
- 8,971 company ids where the paper says 8,262;
- the absence of market data, which means no production desk would deploy this model alone.

**5. Metric (MET-1, MET-5, MET-6, MET-8, MET-9): **yes****

- **ROC AUC is how a credit desk selects a default model.** Basel validation practice (BCBS Working Paper 14) uses AUROC, or its accuracy ratio = 2·AUC − 1, for discriminatory power. It is also the paper's own deliberate selection criterion (MET-5).
- **No threshold or cost is fixed by the source**, so a hard-label metric is ruled out (MET-6, MET-7).
- **Imbalance alone doesn't justify AUPRC (MET-9).** A watchlist does act on the top of the ranking, but no k is fixed. And with 83 to 119 events per window, AP is noisy: 0.08 to 0.30 in my runs.
- **One gap:** I would also want calibration, since PD feeds pricing and capital. But log loss across windows would mostly score how well a model guesses each period's default rate, which moves with the economy. So I would keep `roc_auc` as the selection metric and not switch to log loss.

**Gaps ranked by how much they change the task**

1. **No equity-market variables** (returns, volatility), so this is the accounting-only version of the task. That is defensible and stated in `fit_reason`.
2. **The label horizon cannot be checked** (no filing dates). This is why the fit should be approximate under USE-8.
3. **Distress exits are labelled No.** Measured: early-exit No rows rank above other No rows (AUC about 0.6) and are over-represented in the top 1% (11 to 19% against 7%). Note it in `curation_comments`.
4. **No crisis window in the test periods** (2001 and 2008-09 are not tested).
5. **No interest expense, cash or operating cash flow.**
6. **Firm set fixed by earlier papers, small caps excluded**, and 8,971 vs 8,262 companies unexplained.

**What a domain expert would change**

1. Set `fit="approximate"`. Name the reason as an unverifiable horizon and an accounting-only view.
2. Add a note: "a company delisted for distress that files later stays No (the label is bankruptcy while listed)", with the measured over-representation.
3. Consider the 2007-09 recession window as the curator's exception (the builder's issue 2, option D).
4. Keep the metric as it is.

**Sources**

- The paper (Lombardo et al., Future Internet 2022), as quoted in the record and the definition.
- Shumway 2001 (Journal of Business); Campbell, Hilscher and Szilagyi 2008 (Journal of Finance); Altman 1968; Ohlson 1980.
- BCBS Working Paper 14 (2005) on validating internal-ratings-based models.
- Cited from domain knowledge, not fetched in this run.

</details>

<details><summary>Precedent check</summary>

**Precedent check: american_companies_bankruptcy (panel, 2026-11-25)**

I checked 11 of the builder's calls against earlier decisions. Seven follow precedent. Two depart from precedent: the 3-year window length and the one-year gap. One step is left open with no reason given: whether to set the `Selection Bias` marker. One more call follows precedent, but the source's own split could be cited for it (the source periods as windows).

None of the register's flags concern this dataset. The flags on LEAK-38 and the others are about other datasets. My only computation gives the rows, events and train share per fiscal year, with and without the gap.

**The calls that follow precedent**

| Call | Verdict | Precedents |
|---|---|---|
| Label moved to the failed company's last fiscal year, as the paper defines it (USE-5) | consistent | ames_housing / house_prices_nominal (2026-10-26, Lennart: "we know from the metadata what data to use to build the real task"); rain_in_australia (2026-10-26, Lennart) |
| Decimal points restored by a rule checked cell for cell against the 2022 file (PROV-13) | consistent | the PROV-13 pattern. The repair is checked against the source's own first release, which is stronger than most precedents. |
| Firms seen in training stay in the test windows; the use case is a firm the lender knows (USE-10, SPLIT-13) | consistent (issue 1, option A) | spanish_homeowners_motor_insurance_2010_2014 (Andrej, 2026-11-02: 91% of test rows are known customers); wisconsin_local_government_property_insurance_fund (Andrej 2026-11-02, Lennart 2026-11-08: 97.6-98.8% known); diabetes_130_us (Andrej, 2026-11-11: temporal kept with `Entities: Recur`) |
| `fyear` used as a feature, since it dates the statement and not the label | consistent | the default for a time column; apistox, qsar_tid_11 and sdss_17 set `time_of="label"` only when the year arrives with the label |
| Previous-year items left out (issue 4) | consistent | USE-10 allows a known firm's history but does not require built features. tunisian_fraud_detection_challenge (2026-11-05, Lennart) added the previous *label* as held history. Here the previous label is always No, so there is nothing to add. TP-6: features we invent are no better version. |
| `net_sales` dropped as a copy of revenue; `company_name` and `status_label` dropped | consistent | house rules |
| Metric `roc_auc` taken from the source (MET-5) | consistent | lt_vehicle_loan_default_prediction (2026-11-05, Lennart: the declared ROC AUC stays) |

**Finding 1: the 3-year window departs from the yearly-panel precedents, and its stated reason misreads SPLIT-14 and TP-9**

**Departs, with a stated reason that the rules do not accept.**

- **The stated reason misreads the rules.** The splits comment says: "Three-year windows give each window the 33 events SPLIT-14 asks for (single years hold 21 to 59)."
  - SPLIT-14 asks for 33 *scored units*, which for this task means rows.
  - TP-9 (Must) says: "Few positives in a window are part of the task, not a reason … for another split."
  - SPLIT-16 says the same. Only a window with no positive at all is a problem.
- **Yearly windows are valid.** Each fiscal year holds 2,723-3,857 rows and 21-36 events after 2008.
- **The refit cadence was assumed.** The builder writes "refit cadence 3 years assumed (source names none)".
- **The precedents for yearly panels all test one year per window:**
  - spanish_homeowners_motor_insurance_2010_2014 (Andrej, 2026-11-02): an insurer refits once a year.
  - wisconsin_local_government_property_insurance_fund (Andrej, 2026-11-02): "three splits, one for each year".
  - college_scorecard: one cohort per window.
  - predict_students_dropout_and_academic_success (Andrej, 2026-11-19): one cohort per window.
- **Yearly windows reach SPLIT-15's target, which the 3-year windows fall short of:**
  - With the one-year gap: 10 windows (2009-2018), every train side at 52.3% or more.
  - Without a gap: 11 windows (2008-2018). This includes fiscal 2008 (filings in 2009, 58 events, train 52.3%), the recession window that the builder's option D could only reach by an exception at 42%.
  - The 3-year windows give 3 windows and raise `splits_below_target`.
- **A fact that could set this case apart:** the source's own validation and test periods (2012-14 and 2015-18). Under SPLIT-19 they can be taken as the windows, as medical_facility_operational_data kept "the source's two-week test windows" (2026-11-05, Lennart; SPLIT-12, SPLIT-19).
  - But there the source's windows were its horizon. Here they are the periods of a single paper split, and the third window (2009-11) is not from the source at all.

**Draft issue for the record's review:**

> Should a window be one fiscal year, as for the other yearly panels, rather than three years?
>
> * **Problem:**
>   - The 3-year windows were chosen so that each holds 33 bankruptcies. SPLIT-14 counts rows, and TP-9 treats few positives in a window as part of the task[^w14].
>   - The other yearly panels test one year per window, because the actor refits once a year: spanish_homeowners_motor_insurance_2010_2014 and wisconsin_local_government_property_insurance_fund (both Andrej, 2026-11-02), college_scorecard, predict_students_dropout_and_academic_success.
>   - Yearly windows give 10 windows with the gap (2009-2018) or 11 without it (adding 2008, the recession filings: 58 events, train 52.3%). The 3-year windows give 3, against a target of 9[^w15].
>
> | | Option | Pro | Con |
> |---|---|---|---|
> | a | Keep 3-year windows, with the source's periods as the fact that sets this case apart (SPLIT-19, as medical_facility_operational_data), and drop the 33-events sentence | follows the source's evaluation periods | 3 windows against a target of 9; the 2009-11 window is not the source's; the refit cadence stays assumed |
> | b | Yearly windows, newest 9 (2010-2018, or 2008-2018 without the gap) | the lender's yearly refit; the same as the other yearly panels; meets SPLIT-15's target | 21-36 events per window, so each window is noisier and the mean over windows is compared (as spanish_homeowners) |
> | c | Change TP-9 / SPLIT-14 so that windows are widened to 33 events | gives each window a steadier score | a rule amendment that reverses TP-9 (Must) and the seismic_bumps precedent |
>
> **Recommendation:** b, unless you name the source's periods as the reason, which is (a).
>
> [^w14]: **SPLIT-14** (Must): "at least 33 scored units, counted as SPLIT-33 counts them (the scored unit, else the row)". **TP-9** (Must): "Few positives in a window are part of the task, not a reason … for another split".
> [^w15]: **SPLIT-12** (Should): the horizon comes from the use case or the refit cadence, and the curator signs it off. **SPLIT-15** (Should): the number of windows aims at the IID count (9 here). **SPLIT-19** (Should): follow the source's split.

**Finding 2: the one-year gap departs from SPLIT-10 as amended and from three precedents**

**Departs, with a stated reason that the amended rule no longer accepts on its own.**

- **What SPLIT-10 now says.** It was reworded 2026-11-05 (Lennart, on lt_vehicle_loan_default_prediction):
  - "the measurements decide, also where late labels are documented";
  - a fixed outcome horizon removes the selection by the outcome;
  - no gap is needed where the time step is longer than the delay;
  - the notes give what the newest labels add *at equal training size*.
- **The facts here.** The horizon is fixed: a filing in the year after the fiscal year. Every label is final at release (the data end in 2018, the filings in 2019).
  - The label of fiscal year t−1 is known by the end of calendar year t. The fiscal-year-t statements are filed months later. So the step is about as long as the delay, and the gap mostly guards against nothing.
  - The splits comment says "when the first statements of a window arrive, the labels of the year before are not all known". That holds at most for fiscal years that do not end in December.
- **No shortcut was measured.** SPLIT-9's shortcut through a firm's own earlier label cannot happen here: a training row is Yes only on a firm's last year, so that firm has no test rows.
- **The measurement is not the one the rule asks for.** The builder measured +0.003 to +0.027 AUC without the gap, but with 3.5k-3.9k more training rows, not at equal size. Calling that "optimistic" does not separate a shortcut from the larger training set.
- **Precedents that set no gap:**
  - lt_vehicle_loan_default_prediction (2026-11-05, Lennart): gap 0 as an application of SPLIT-10 with a fixed horizon.
  - wisconsin_local_government_property_insurance_fund (2026-11-08, Lennart): no gap, because "every policy year ships with its final claim amounts".
  - spanish_homeowners_motor_insurance_2010_2014 (2026-11-02, Andrej): no gap in a yearly panel, with hidden-claims tests inside the noise.
- **Precedent that sets a gap:** predict_students_dropout_and_academic_success. There the label matures 3 years after enrolment, longer than the step, so it does not apply here.

**Draft issue for the record's review:**

> Should the one-year gap go, since every label is final at release and the delay is no longer than a fiscal year?
>
> * **Problem:**
>   - The gap cites the label's delay. Since 2026-11-05, SPLIT-10 asks for a measured shortcut, or for late labels that the collection does not cover[^g10].
>   - The label horizon is fixed (a filing in the year after the statement) and final at release. A fiscal year's labels are known before the next year's statements are filed.
>   - No AUC was measured at equal training size, and SPLIT-9's shortcut through a firm's own label cannot arise (a Yes row is a firm's last year).
>   - Precedents with no gap: lt_vehicle_loan_default_prediction and wisconsin_local_government_property_insurance_fund (Lennart, 2026-11-05 and 2026-11-08), spanish_homeowners_motor_insurance_2010_2014 (Andrej, 2026-11-02).
>
> | | Option | Pro | Con |
> |---|---|---|---|
> | a | Keep the gap: some fiscal years do not end in December, so their next-year filings run past the time the next statements arrive (the AI's guess at the distinguishing fact; check it with an AUC at equal training size) | safe if the overlap is real | not measured; the data carry no fiscal-year-end month or filing dates |
> | b | No gap, as lt_vehicle_loan_default_prediction and wisconsin_local_government_property_insurance_fund | follows the amended rule and the precedents; adds a window (2008) and 3.5k-3.9k training rows | the newest training year's filings, made during the year, are known only at its end |
> | c | Reopen the precedents to match a gap here | one rule for yearly panels | reverses three settled decisions |
>
> **Recommendation:** b, after the measurement at equal training size shows no shortcut.
>
> [^g10]: **SPLIT-10** (Should; amended 2026-11-04 and 2026-11-05, Lennart): no gap where the collection covers the delay and the measurements show neither a shortcut nor a selection at the release end; a fixed outcome horizon removes the selection. **SPLIT-9** (Must).

**Finding 3: `Selection Bias` is left to the curator with no reason (minor)**

**Open; the builder records no reason against the marker.**

- **The facts.** The firm set is fixed by the authors' earlier papers. Small market caps are excluded, and the paper says this "can underestimate" the bankruptcy rate. The panel shrinks from 5,308 firms to 2,723 with few new listings.
- **The pattern.** selection.md, "Selection bias" (Andrej 2026-10-20, Lennart 2026-10-27) marks rows "not drawn from the population the use case predicts for". The use case scores listed firms, small caps included.
- **Precedents.** polish_companies_bankruptcy carries `Selection Bias`. None of the pattern's "No marker when" cases applies here.
- **The fit.** `fit_reason` already names the gap, so the marker is the only thing missing. Whether the fit stays `direct` (a lender's own setting has the same bias) is the pattern's open question.

> Set `Selection Bias`, since the small caps the paper says it excluded are part of the population a lender scores?
>
> | | Option | Pro | Con |
> |---|---|---|---|
> | a | No marker: the firm set approximates the listed market each year (Section 3), and that fact sets it apart (the AI's best guess) | the source's own claim | the paper itself says the bankruptcy rate is underestimated |
> | b | `Selection Bias` with a direct fit, as the pattern allows | follows the pattern; a concern flag, usually on `Yes` | none worth weighing |
>
> **Recommendation:** b.

**Nothing to report**

- **Drift and amendments due:** I found no drift by one curator and no third exception of the same kind triggered by this dataset.
- **Retiring polish:** the decision to retire polish as replaced is not this panel's call. Its draft follows SEL-18 and the "Small or dated" pattern.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real and useful one-year-ahead bankruptcy task on public company accounts. The data is real and the temporal split is honest. But the label is built from "last year the firm appears", which I cannot fully verify, and each test window has only 57–87 bankruptcies, so scores will be noisy.

**What the task is.** A lender, credit analyst or investor uses a firm's annual accounts for fiscal year t to estimate whether it files for bankruptcy (Chapter 7 or 11) in year t+1. That is a standard, real credit-risk decision. The table has 78,682 rows, one per company and year, from 8,971 US public companies over 1999–2018. There are 18 accounting values (in millions of USD, by their magnitude), plus SIC Division, SIC MajorGroup and `fyear`. Only 609 rows are positive (0.77%). `task.md` names no training-weight column, so there is nothing to judge on that point.

**Concerns, most serious first**

1. **The label is derived, and its timing is unchecked.**
   - **Evidence:** The original file I downloaded from the GitHub repo has `status_label` = failed on all 5,220 rows of 609 failed companies, not just one year. The prepared target is "Yes" on exactly the last observed year of each of those 609 companies. The counts match the repo file's last-year-of-failed-firm counts year by year: 1999: 3 … 2008: 58 … 2018: 36.
   - **Why that is roughly right:** It matches the source's own definition: *"we label the fiscal year before the chapter filling as 'Bankruptcy' (1) for the next year."*
   - **The risk:** Companies often stop filing accounts a year or more before they file for bankruptcy. 710 companies have gaps in their yearly records. So some "Yes" rows may be 2+ years before the filing, and earlier rows of failing firms count as "No".
   - **Also:** About 5,600 companies leave the data before 2018 for other reasons (merger, delisting) and their last row is "No". That is defensible, but it should be stated.
   - **Change:** Document this rule in `task.md`. If filing dates can be obtained, check the t+1 timing against them.

2. **Few positives per test window, so scores are noisy.**
   - **Evidence:** I used 3 windows of my own choosing (the real split boundaries are not given): train up to 2011 / test 2012–14; up to 2014 / 2015–16; up to 2016 / 2017–18. The test windows have 87, 62 and 57 positives.
   - **Scores:** LightGBM reached ROC-AUC 0.934 / 0.928 / 0.921 and average precision 0.21 / 0.37 / 0.21. A model on `fyear` alone scores AUC 0.50.
   - **What that means:** There is clear signal and the task is not trivial. But with about 60 positives, average precision will swing a lot between methods.
   - **Change:** Use wider test windows (for example 3 years each), and report AUC or log-loss rather than accuracy.

3. **No company ID, and companies repeat across years.**
   - **Evidence:** Each company appears up to 20 times. There are no exact duplicate rows, not even ignoring `fyear`.
   - **Why it is acceptable:** The temporal split matches real use: you score known firms on new years. Same-firm rows before the cutoff are legitimate history.
   - **Limits:** Without an ID, methods cannot use year-over-year changes, and we cannot check same-firm effects.
   - **Change:** Keep an anonymised firm ID as a grouping or metadata column, not as a feature.

4. **Minor preparation points.**
   - `Division` is redundant: it is a coarser grouping of the same SIC code as `MajorGroup` (73 levels). Its "Public Administration" level has only 13 rows.
   - A few values are negative where that is implausible: current assets (min −7.76), revenue (min −1,965) and cost of goods sold. There are few of them; keep them.
   - The internal arithmetic checks out:
     - EBITDA = EBIT + depreciation and amortisation (median gap about 1e-15).
     - Gross profit = revenue − cost of goods sold (median gap about 1e-15).
   - Data types are sensible (categories for the SIC codes) and there are no missing values.

5. **The source repo's CSV has broken numbers; the prepared table does not.**
   - **Evidence:** In the GitHub CSV the decimal point is missing on many values. For example, company C_1 has 740998 in 1999 and 701.854 in 2000 in the same column.
   - The prepared table passes the arithmetic checks above, so it seems to come from the cleaner Kaggle copy. That is good.
   - **Change:** Record which copy was used.

**What I could not check:**
- The actual filing dates, so I cannot confirm that "Yes" means a filing in t+1.
- Whether market value is measured at fiscal year end.
- The data vendor (probably Compustat, but the repo README does not name it) and the units.
- The MDPI paper (the site returned 403 Forbidden) and the Kaggle description (only the title loaded).
- The exact split boundaries.

I downloaded the public source CSV to compare it with the prepared table.

</details>

<details><summary>Task gamer</summary>

**Verdict:** this task can be gamed by a lot. Positives are exactly the last row a failed company has in the table. So whether a company shows up again in the next year's rows decides the label, and those later rows sit in `data.parquet`. Rebuilding that link from the features alone, with no company ids, raises mean AUC from **0.867 to 0.938**. With exact company ids the same feature reaches 0.978.

Baseline: untuned LightGBM on `features()`, no weight (task.json names none). Per split r0/r1/r2: 0.908 / 0.884 / 0.809, mean 0.867. Adding a column of random numbers, five times, gave means of 0.862–0.880 and moved single splits by up to ±0.03, so gains under about 0.015 are noise.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Does a matching company appear in year t+1? (one-to-one match within the same industry code in the next year's rows; the match cost is the feature; the baseline model is kept for rows with no next year) | 0.867 | **0.938** (0.948 / 0.944 / 0.924 with all link features) | +0.035 / +0.059 / +0.115 | No. It reads next year's financial statement. | Give each split only rows dated ≤ the last test year, so no later years are in the file, and drop the final test year from each test window. Or score each test year using only rows up to that year. |
| 1a | Same leak using the true company ids from the published CSV (the ceiling) | 0.867 | 0.978 | +0.064 / +0.099 / +0.171 | No | as above |
| 1b | Plain nearest-neighbour distance to next year, with no special handling of the last year | 0.867 | 0.880 | −0.097 / +0.042 / +0.096 | No | as above |

**How exploit 1 works.** I matched the kit to the published file: 78,389 of 78,682 rows match exactly. A row is labelled Yes only when it is a failed company's last row: 607 of 609 positives are, and no other row is. Every row whose company appears in year t+1 is a No (68,369 rows, 0 positives). So "has a successor next year" alone gives AUC 0.85–0.96.

The kit removes company names and shuffles rows within each year. But one year's balance sheet sits close to the next year's: my nearest neighbour in the same industry code (MajorGroup) is the true successor 76% of the time. The one-to-one match cost alone gives AUC 0.887 on rows before 2018. Positives sit at a median distance of 0.53 against 0.21 for negatives.

The leak is strongest in r1 and r2. Their tests end in 2014 and 2011, so `data.parquet` still holds the following years for every test row. In r0, the 2018 rows have no next year, so those rows fall back to the baseline model.

**Mildest fix:** drop the last test year from each test window and the years after it from that split's data. Failing that, score each test year with the data cut at that year.

**Flaws that hurt an honest model**

I found none that measurably hurt it:
- **Previous-year history** (distance to the matching company's row in t−1), which a lender would know at the prediction point: 0.877 against 0.867, inside the noise. It is signal, not an exploit.
- **Dropping `fyear`:** 0.863, also noise.
- **Gap year:** each training window stops one year before its test window, so every training label was knowable before the test starts.

**Attacks that found nothing**

- **Formats:** decimal places, zeros and signs. Decimals alone give 0.526, and baseline plus decimals 0.876 (noise). The kit's /1000 fix to the source's scaling errors left no class-dependent artefact.
- **Row order:** shuffled within year. Spearman correlation of row position with company id is about 0. Next-row positive pairs: 5 against 4.7 expected.
- **Columns from after the outcome:** no single feature comes near the full model. The best is `net_income` at AUC 0.83; `fyear` alone gives 0.50; industry alone 0.59.
- **Train-versus-test classifier:** AUC 0.70–0.73, which is ordinary drift.
- **Weight and global transforms:** there is no weight, and there are no z-scored or rank columns.
- **Exact copies across splits:** not applicable. The panel holds one row per company per year, so the leak goes through the next-year link above.
- **Looking rows up in the published file:** this works (99.6% of rows match exactly). It is not ranked, but it is how I measured the 1a ceiling.

**What the preparation changed** compared with the published CSV:
- relabelled from the source's per-company `status_label` ("failed" on all 5,220 rows of failed companies) to the last row only;
- dropped the company name and X17 (a duplicate of revenue);
- fixed the ×1000 scaling errors in the source;
- shuffled rows within each year.

The source's all-years "failed" label would have been a much bigger leak; the kit removed it.

**What I could not check**

- **Statement date against filing date.** I don't know whether the last statement is always dated before the bankruptcy filing. It decides whether that final row's features (net income alone scores 0.83) can include post-filing results. Settling it needs the 10-K dates against the filing dates (e.g. from the LoPucki Bankruptcy Research Database), which are not public in this dataset.
- **Gaps before the last row.** I couldn't tell whether a failed company with missing years gets a 1 more than a year before it failed.
- **Forums.** My web search found no Kaggle discussion of leaks for this dataset.

Sources: [Lombardo et al. 2022, MDPI](https://www.mdpi.com/1999-5903/14/8/244), [sowide/bankruptcy_dataset](https://github.com/sowide/bankruptcy_dataset), [Datasets for Advanced Bankruptcy Prediction (arXiv)](https://arxiv.org/html/2411.01928v1), [From Numbers to Words (arXiv 2401.12652)](https://arxiv.org/html/2401.12652v1)

</details>

<details><summary>Advocate (brief)</summary>

**Advocate's opening brief: `american_companies_bankruptcy`**

My position: ship it after one re-split. The panel found one real problem, a leak inside the 3-year test windows. It is fixed by the same change to 1-year windows that two other agents asked for on separate grounds. Everything else the panel raised needs only a note or a marker.

---

**1. The target is the source's own target, checked year by year.** (USE-5, P3, Must)
- **Evidence:**
  - The claim auditor read Table 1 from the paper's PDF. For all 20 fiscal years, our row counts match the paper's "Total Firms" one year later and our events match its "Bankrupt Firms" (3, 7, 10 … 21, 36; 609 in total).
  - The paper, Section 3: "the fiscal year before the chapter filing as 'bankruptcy' (1)".
  - The split files agree: 496 of 502 failed rows are a company's last year, and none is an earlier year.
- **Why it wins:** a target confirmed against the source in every year is P3 at its strongest. The published label is worse, not an alternative. It marks every year of a failed company, which drops grouped AUC to about 0.70, and the task gamer calls it "a much bigger leak" that the kit removed. Precedents: ames_housing and rain_in_australia (Lennart, 2026-10-26).

**2. The data is faithful: repaired from the origin, with the repair asserted in the code.** (PROV-13, P5, Must)
- **Evidence:**
  - `_clean` asserts that every repaired cell equals the July 2022 release. The claim auditor reran it, and the 2022 file has 0 of 1,416,276 tokens without a decimal point.
  - No feature vector appears twice, and no test row copies a training row.
  - The recording markers carry no class signal: 0.538 alone, 0.858 against 0.857 when added to the items (LEAK-39). The task gamer agrees: decimals alone give 0.526.
- **Why it wins:** this is the top rung of the remedy ladder (repair from the origin), and it is stronger than most PROV-13 precedents.

**3. No column leaks; every input is known at the prediction point.** (LEAK-1, P4, Must)
- **Evidence:**
  - The column auditor found all 20 features to be year-end statement items, the fiscal year or SIC codes.
  - Its test for statements filed after the bankruptcy found nothing. On event rows, the share of liabilities in neither current nor long-term debt has median 0.060, against 0.066 the year before.
  - The task gamer: the best single feature is `net_income` at 0.83, `fyear` alone gives 0.50, and the train-versus-test classifier reaches 0.70–0.73, which is ordinary drift.
- **Why it wins:** Must-level, measured, and no agent disputes it.

**4. Conceded: the 3-year test windows leak. The fix is a re-split, not a reject.** (P4, Must; remedy ladder rung 2)
- **The problem is real.** A Yes row is a failed company's last row, so a company with a row in the next year is always No. In a 3-year window, the test rows themselves show which companies have a next-year row.
- **My measurement:**
  - With true company ids and only the window's own test rows, a "no next-year row" flag scores AUC 0.851, 0.807 and 0.808.
  - It catches 83, 54 and 58 of the 119, 87 and 83 positives: every positive outside the window's last year.
  - With 1-year windows the flag is 0.500 in all 10 windows. The test side then holds no next-year rows.
- **The task gamer's figures:** rebuilt without ids, the link raises mean AUC from 0.867 to 0.938, and true ids give 0.978.
- **The rest of its gain is out of scope for this dataset.** It also read container rows after the test window, which are neither train nor test rows of that split. A model fitted by the protocol (`train_idx`, `test_idx`) never receives them, and every temporal dataset in the collection has the same layout. If the curator wants to forbid that, it is a protocol rule for all datasets.
- **Why 1-year windows (2009–2018) are the mildest fix:**
  - The split auditor and the precedent checker already recommend them, independently, under SPLIT-15 (10 windows against a target of 9) and TP-9 (Must: few positives in a window are part of the task).
  - They match the yearly-panel precedents: spanish_homeowners, wisconsin_local_government_property_insurance_fund, college_scorecard and predict_students_dropout_and_academic_success.
  - Each window still holds 2.7k–3.7k rows and 21–36 events, so SPLIT-14 holds.
- **Also fix:** `Temporal(horizon=1)` and the splits comment, dropping the misread "33 events" argument.

**5. It is worth benchmarking, and it is the better replacement for polish.** (P6: TP, SPLIT-14)
- **Evidence:**
  - 78,682 firm-years and 609 events.
  - Honest AUCs per window range from 0.81 to 0.93 (task gamer, blind reviewer, split auditor), so the task is neither trivial nor saturated.
  - Every window holds both classes, and random scores give 0.52–0.53.
  - Firms are known when tested (82–88% seen in training), which matches a lender's portfolio. Seen and new firms score alike (0.910 against 0.908).
- **Why it wins:** no P6 rule is triggered after point 4's re-split. The domain practitioner would use it "as a benchmark of accounting-only PD models".

**6. The metric is right; the paper's AUCs need one sentence.** (MET-5 Should, MET-6)
- **Evidence:**
  - ROC AUC is the paper's deliberate selection criterion (Section 8) and the Basel practice for validating PD models (domain practitioner).
  - The source fixes no threshold, so its macro-F1 suggestion fails MET-6, and the MET-8 fallback would be ROC AUC anyway.
- **Conceded:** the paper scored about one sample per company (3,345 samples, 3.1% positive). Its 0.861 is not comparable to our baselines.
  - Remedy: a note in the Metric bullet that quotes Sections 8.1 and 9 in full. The metric stays.

**7. The other findings are notes or markers.** (remedy ladder: keep with a note)
- **Horizon cannot be verified (USE-8):** concede `fit="approximate"`. The Table 1 match makes the horizon plausible but does not check it.
- **Distress exits stay No:** this is label noise (early exits score about AUC 0.6 among No rows) that holds every model back alike. It is not a leak. Note "bankruptcy while listed".
- **Selection:** concede the `Selection Bias` marker, which follows the polish precedent.
- **Gap:** a Should-level weighing call (SPLIT-10). I concede that the builder's +0.003 to +0.027 was not measured at equal training size. Measure it at equal size; either outcome keeps the dataset.
- **Thin early events (3–17 per year, 1999–2002):** they sit in training sides only. Note them under Selection.
- **Wording fixes:**
  - "every row" becomes "all but 1–3 rows";
  - "21 to 59" events per year holds only for 2003–2018;
  - the company id's Spearman correlation with first year is 0.49, not 0.59;
  - say that SIC codes are looked up once per company (LEAK-10 note).
- None of these is a failed Must, so "independent failures" do not apply. Each is a Should or Weigh item, settled with a note.

**Summary judgment.** Verdict: ship after changes.
- **Validity:** USE-5, PROV-13 and LEAK-1 hold. The within-window leak (P4) is fixed by re-splitting to 1-year windows, 2009–2018.
- **Value:** TP and MET hold, with a metric note.
- **Quality:** wording fixes.
- **For the curator:** the gap, the 2008 crisis window as an exception, and the `approximate` fit and `Selection Bias` marker.

</details>

<details><summary>Critic (brief)</summary>

**Critic's opening brief: `american_companies_bankruptcy`**

**Verdict: ship only after changes.** I am not asking to exclude it. The task is real, the label repair matches the paper's Table 1 every year, and the decimal repair is checked cell for cell against the 2022 file. But the split as defined lets a model read the answer from other test rows, and the fit is labelled "direct" when it should be "approximate". Both can be fixed in the definition.

**1. Positives can be read off other rows in the same test window (P4, LEAK-9 Should; the strength is set by how large the effect is).**
- **Problem:** the target is Yes only on a failed company's last row. So every row whose company appears again the next year is No. Inside a 3- or 4-year test window, that next row sits in the same test set.
- **Effect:** a model that compares test rows with each other can find most of the No rows without looking at the accounts.
- **Evidence:**
  - My check (using the true company ids): 61–70% of No test rows have their next-year row inside the same window, and no positive does. That flag alone scores AUC 0.851, 0.807 and 0.808 on the three windows.
  - The task-gamer rebuilt the link from the features alone, with no ids. It raised mean AUC from 0.867 to 0.938 (+0.035, +0.059, +0.115 per split). With true ids it reached 0.978.
- **Remedy:** one-year test windows (point 2). A test set then holds a single fiscal year, so no test row's next year is in it. Add the protocol line the precedent uses: each test row is predicted from the training rows and its own features only. That is what loan_default_prediction_imperial_college did (LEAK-9 applied, Andrej, 2026-11-10).

**2. The 3-year windows rest on a misread rule (P4, SPLIT-12 Should, SPLIT-15 Should; TP-9 Must).**
- **Problem:** the splits comment says three-year windows were chosen to give each window "the 33 events SPLIT-14 asks for". SPLIT-14 counts scored units, which here are rows. TP-9 says few positives in a window "are part of the task, not a reason … for another split".
- **Effect:**
  - Only 3 windows, against a target of 9.
  - Long refit lags: the 2018 rows are scored by a model trained on data up to 2013.
  - A model can exploit the rows in point 1.
- **Evidence:**
  - Split-auditor: 1-year windows from 2009 to 2018 give 10 windows, each training on 52.3–92.7%, each with 21–36 events and at least 2,723 rows.
  - Precedent-checker: the other yearly panels test one year per window (spanish_homeowners, wisconsin, college_scorecard, predict_students_dropout).
  - The builder assumed the 3-year refit cadence itself ("source names none").
- **Remedy:** 1-year windows from 2009 to 2018, with an annual refit, since statements are annual. Set `Temporal(horizon=1)`; today `horizon=3` contradicts the 4-year newest window. If the curator instead keeps the source's periods under SPLIT-19, the comment must drop the 33-events argument, and point 1 then needs at least the protocol line.

**3. The one-year gap is neither measured nor in line with precedent (P4, SPLIT-10 Should, amended 2026-11-05).**
- **Problem:** the horizon is fixed (a filing in the year after the statement), and the labels are final at release. The builder's measurement (+0.003 to +0.027 AUC without the gap) adds 3.5k–3.9k training rows, so it does not compare at equal training size as SPLIT-10 asks.
- **Effect:**
  - Each window loses its newest training year for no shown reason.
  - Fiscal 2008, the recession year with 58 events, cannot be a test window. Without a gap it trains on 52.3% (precedent-checker), and no crisis year is ever tested otherwise. The domain practitioner says a credit model is judged above all on downturns.
- **Precedents:** no gap in lt_vehicle_loan_default_prediction, wisconsin and spanish_homeowners.
- **Remedy:** measure at equal training size. Drop the gap unless that shows a shortcut, which would make the windows 2008 to 2018.

**4. The fit should be approximate, not direct (P3, USE-8 Must).**
- **Problem:** USE-8 names "a breadth or horizon that cannot be verified" as approximate. There are no filing dates, so whether a last statement comes within a year of the filing cannot be checked; the notes admit this. On top of that, companies that leave the panel in distress and file later stay No.
- **Effect:** the label is "bankruptcy while listed, after the last statement", which is not exactly a one-year default.
- **Evidence:** the domain practitioner measured that No rows which are a company's last year before an early exit rank above the other No rows (AUC 0.60, 0.64, 0.58). They make up 11–19% of the top 1% of scores, against about 7% of all rows.
- **Remedy:** set `fit="approximate"`, give the reason in `fit_reason`, and add the exit note to `curation_comments`. No change to the data.

**5. The `Selection Bias` marker is missing (P5 Should pattern; the polish_companies_bankruptcy precedent).**
- **Evidence:**
  - The firm set is fixed by the authors' earlier papers.
  - The paper itself says small caps were excluded and the bankruptcy rate "can be underestimated".
  - Fiscal 1999–2002, the dot-com bust, hold only 3, 7, 10 and 17 events (column auditor).
  - 8,971 company ids against the 8,262 stated, with no explanation.
- **Remedy:** set the marker and add the early-year event counts to the Selection bullet.

**6. The metric note leaves out two facts (P6, MET-5 Should, MET-6 Must).**
- **Evidence (claim auditor):**
  - The paper's AUC was scored on about one sample per company: 3,345 test samples, 3.1% positive. We score 12,282 firm-years at 0.97%. So the paper's 0.861 cannot be compared with our baselines, as the record currently does.
  - The paper says macro-F1 and per-class precision and recall "would better define the models' performance" (Sec. 9; Sec. 8.1 on regulators).
- **Remedy:** a note only. Keep `roc_auc` (MET-6 bars macro-F1 without a threshold), but state the difference in unit and quote the paper exactly.

**7. Wording errors (P7, EV-2), a quality fix, not a reason to block.**
- The accounting identities hold in all rows but 1 to 3, not "in every row". `total_operating_expenses` is revenue − EBITDA, also off in a few rows.
- The id's correlation with first year is 0.49, not 0.59.
- "Single years hold 21 to 59" events holds only from 2003.
- The SIC codes are one lookup per company (LEAK-10 note, as in the tunisian precedent).

I concede that these hold, per the panel: no feature leaks, the relabelled target is correct, the decimal repair is exact, and `roc_auc` is the right metric. The remedy for points 1–3 is one re-split. After that and the notes in 4–7, I would not oppose shipping.

</details>

<details><summary>Advocate (rebuttal)</summary>

**Advocate's rebuttal: `american_companies_bankruptcy`**

The critic and I now want the same verdict (ship after changes) and the same main fix (1-year test windows). We still differ on three things: what the protocol line can do, the gap default, and the `horizon` value. I settle each below.

**1. Positives readable from other test rows: conceded. I accept the protocol line as a note.**
- We each measured the leak separately and got the same flag AUCs: 0.851, 0.807 and 0.808. The task gamer's 0.867 → 0.938 confirms it.
- The 1-year windows remove it. In my run the flag scores 0.500 in all 10 windows.
- **The protocol line:** I accept it as the loan_default_prediction_imperial_college precedent applied it (LEAK-9, 2026-11-10). After the re-split it costs nothing. One limit should be stated plainly. Container rows after the test window are a layout every temporal dataset shares. A line in one dataset documents the problem there but does not solve it across the collection. That stays a protocol question for the curator. It does not count against this dataset.

**2. The 3-year windows rest on a misread rule: conceded in full.**
- My opening point 4 asks for the same change: windows 2009–2018 (or 2008–2018, see 3), `Temporal(horizon=1)`, and no "33 events" sentence.
- I also concede the critic's extra point. `horizon=3` is already wrong today, because the newest window spans 4 years.
- Option (a), keeping the source's periods under SPLIT-19, is weak. The precedent checker notes that the 2009–11 window does not come from the source. I would not offer it as the main option.

**3. The gap: the critic's default is better than mine, so I take it.**
- In my opening I called this a weighing call where "either outcome keeps the dataset". The precedent checker shows more than that:
  - The horizon is fixed, and labels are final at release.
  - The label of fiscal year t−1 is known before the statements for year t are filed.
  - SPLIT-9's shortcut cannot happen here: a training Yes is a firm's last year, so that firm has no test rows.
  - Three settled precedents set no gap: lt_vehicle_loan_default_prediction, wisconsin and spanish_homeowners.
- Under SPLIT-10 as amended (2026-11-05), the gap needs a measured shortcut, and none has been shown. So I accept the critic's remedy: measure at equal training size, and drop the gap unless that measurement shows a shortcut. That gives 11 windows, 2008–2018, and adds the recession year (58 events, 52.3% train) without making an exception.
- The split auditor's one argument for keeping it is fiscal years that do not end in December. The data carry no fiscal-year-end month, so this argument is unmeasured too. It cannot outrank the precedents unless a number backs it.

**4. `fit="approximate"`: conceded.** This was already in my opening point 7.
- USE-8 lists a horizon that cannot be verified as approximate, and there are no filing dates to verify it.
- The distress exits that stay No (AUC 0.60, 0.64 and 0.58 among No rows) go in `curation_comments` as "bankruptcy while listed".
- One addition from me: this is label noise that every model faces equally. It is not a leak, and the data stay as they are.

**5. `Selection Bias` marker: conceded.** It follows the polish_companies_bankruptcy precedent.
- The Selection bullet should list the early-year events (3, 7, 10 and 17 for 1999–2002).
- It should also note the gap between 8,971 company ids and the 8,262 the paper states.
- After the re-split, the thin early years appear only in training sides.

**6. Metric note: conceded, including the critic's sharper wording.**
- The record compares the paper's 0.861 with our baselines. It should not, because the units differ: about one sample per company (3,345 samples, 3.1% positive) against 12,282 firm-years at 0.97%.
- The note should quote Sections 8.1 and 9 exactly. `roc_auc` stays: MET-6 bars macro-F1 when no threshold is given.

**7. Wording errors: conceded.** My list and the critic's are the same: "all but 1–3 rows" instead of "every row", `total_operating_expenses` off in a few rows, a correlation of 0.49 rather than 0.59, "21–59 events" only from 2003, and the SIC lookup (a LEAK-10 note).

**What is left for the curator**
1. Gap or no gap, after the equal-size measurement. The critic and I now both default to no gap, which gives windows 2008–2018.
2. Whether rows after the test window should be barred by a collection-wide protocol rule. This is not a question about this dataset.

Everything else both sides have conceded. Validity rests on USE-5, PROV-13 and LEAK-1, and neither side disputes them. Verdict: ship after the re-split and the notes.

</details>

<details><summary>Critic (rebuttal)</summary>

**Critic's rebuttal: `american_companies_bankruptcy`**

The advocate and I agree on almost everything: one re-split to 1-year windows from 2009 to 2018, plus notes and markers. The one real dispute is whether 1-year windows close the leak alone. They do not.

**Advocate 1 (the target), 2 (the repair), 3 (no column leaks): conceded.** I conceded all three in my opening brief. The evidence is the year-by-year match with Table 1, the asserted repair against the 2022 file, and the column auditor's and task gamer's tests.

**Advocate 4 (the leak, fixed by 1-year windows): partly disputed.**
- **Conceded:** 1-year windows are the right split. A window's own test rows then hold no next-year rows, which is the advocate's 0.500 in all 10 windows.
- **Disputed:** that 0.500 counts only the test window's own rows. The task gamer's exploit read the following years from `data.parquet`, and that file stays the same under any re-split. With 1-year windows from 2009 to 2018, every test year except 2018 still has its next year in the container. That is 9 of 10 windows. The task gamer says the leak is strongest exactly when later years are in the file: +0.059 and +0.115 on r1 and r2, against +0.035 on r0, whose newest test year is 2018. The re-split moves those later rows out of the test set, but a participant can still read them from the container.
- **Disputed: "a protocol rule for all datasets."** In kind, yes. But the house closes this channel per dataset, with a protocol line in the notes and in `splits_comment` (LEAK-9 Should, applied 2026-11-10 by Andrej on loan_default_prediction_imperial_college, and 2026-11-09 on spanish_motor_insurance_coverage_level_2022_2024). Those cases are the same as this one: an entity's later row, found from shipped columns, gives away the outcome of the row before it. The ruling there was a protocol line, not a drop.
- **Rule that wins:** LEAK-9 with its two applied precedents. A rule that may come later for every dataset does not replace the precedent that applies now.
- **Remedy (unchanged from my point 1):** 1-year windows plus the line, worded as in loan_default: "each test row is predicted from the training rows and its own features only; no feature or model step may use other rows of the file; a method that reads another row of the same company is called out and not benchmarked". It costs one sentence. Without it, a +0.04 to +0.11 exploit stays open in 9 of 10 windows.

**Advocate 5 (worth benchmarking, better than polish): conceded.** No P6 rule fails after the re-split.

**Advocate 6 (the metric): conceded.** We agree: keep `roc_auc`, and add a note that the paper scored about one sample per company and that its 0.861 cannot be compared with our baselines.

**Advocate 7 (notes and markers): conceded, with one correction.**
- I concede the `approximate` fit, the `Selection Bias` marker, the early event counts under Selection, and the wording fixes.
- I concede that distress exits are label noise, not a leak. The note "bankruptcy while listed" plus `fit_reason` is enough.
- **Correction on the gap:** the advocate calls the 2008 crisis window "an exception". It is not one. If the gap is dropped after a measurement at equal training size (SPLIT-10 Should), 2008 becomes an ordinary window that trains on 52.3%, and the windows run from 2008 to 2018. If the gap stays, 2008 is simply not tested. Either way it stays a weighing call for the curator, and neither outcome blocks shipping.

**Where we stand.** Ship after these changes:
- 1-year windows and `Temporal(horizon=1)`;
- the LEAK-9 protocol line;
- the gap measured at equal training size;
- `fit="approximate"` and the `Selection Bias` marker;
- the metric note and the wording fixes.

The only point still in dispute is the protocol line, and the LEAK-9 precedents settle it.

</details>
