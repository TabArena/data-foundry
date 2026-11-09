---
unique_name: springleaf_marketing_response
name: Springleaf Marketing Response
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Many features
original_source: Kaggle
year: '2015'
domain: business & marketing
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/springleaf-marketing-response
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a 2015 Kaggle competition of the consumer lender Springleaf, one row per customer with about 1,930 anonymized columns and the response to a direct-mail offer as the target, scored by ROC AUC; the company names the decision, but what the columns measure cannot be checked.
- Source: Kaggle competition "Springleaf Marketing Response" by Springleaf (Featured, enabled 2015-08-14, deadline 2015-10-19, 2,221 teams; Kaggle API). As published (Data page): "a high-dimensional dataset of anonymized customer information. Each row corresponds to one customer. The response variable is binary and labeled "target""; "The features have been anonymized to protect privacy and are comprised of a mix of continuous and categorical features", with "placeholder" values for cases such as missing values kept "to match with internal systems at Springleaf". Files: `train.csv.zip` 157 MB, `test.csv.zip` 157 MB (no labels), `sample_submission.csv.zip`; about 145,000 training rows and about 1,930 columns as participants report, not counted here.
- Use case: Springleaf's marketing team decides whom to send a direct-mail loan offer: "Determine whether to send a direct mail piece to a customer" (Kaggle API description); "Springleaf must be sure they are focusing on the customers who are likely to respond and be good candidates for their services" (Description); fit direct. Regime IID unless a mailing or account date among the columns orders the rows (then temporal, SPLIT-7); not checked.
- Siblings and duplicates: `pva_revenue_prediction_kddcup98` (`Yes`, shipped; KDD Cup 98 donors' response to a charity mailing, scored by a stand-in `roc_auc`): the same kind of task from another source and decade, no duplicate (PROV-4). No other Springleaf record. External collections: none found (searched only this repository; the session's web search budget was used up).
- Better data: found as better data for `pva_revenue_prediction_kddcup98`; no further search this round.
- Papers and pages: the competition's Description, Evaluation and Data pages (read through the Kaggle API); the example script "xgboost-example" linked from the Data page.
- Metric: "Submissions are evaluated on area under the ROC curve between the predicted probability and the observed target" (Evaluation page): `roc_auc`, the leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: the columns are anonymized (`Anonymized`): what each one measures, whether it is known before the mailing, and whether a field records the response cannot be checked (LEAK-32, LEAK-38); placeholder codes for missing values can only be decoded by pattern; only the training file has labels; the row order and any date-like columns decide the regime; Kaggle's competition rules (registration) are a note, not a criterion (EV-4).
- Priority: gap 0 (business & marketing and binary are not thin), use case + (the company names the mailing decision), source 0 (a competition page that does not document the columns), shape + (about 145,000 customers, wide and mixed), risk - (anonymized features, leaks that cannot be ruled out).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `pva_revenue_prediction_kddcup98`.
- as published: customers, one row each; train.csv.zip 157 MB and test.csv.zip 157 MB (Kaggle file listing); about 145,000 training rows x about 1,930 anonymized columns as reported by participants (verify at ...; target: binary: whether the customer responds to the direct-mail offer; access: registration.
- Why: the same task as KDD Cup 98 (response to a direct-mail solicitation, one row per customer from the customer file, binary response, AUC as our stand-in metric there)
- Adds: 17 years newer and about 1.5x the rows of the KDD98 learning file (95,412); a commercial lender instead of a charity. Caveats: columns anonymized (Anonymized marker), no column descriptions; Kaggle competition rules (registration)

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: the task's table is 145,231 labelled customers x 1,879 inputs once 5 constant and 48 copied columns leave (1,836 numeric, 27 string, 16 dates), with 33,773 responders (23.3%). The call stands at priority 2. Two facts bear on the split: a date column that likely orders the mailings, and 3,712 customers who appear more than once.
- As published: Kaggle competition files (CLI listing, 2026-11-08): `train.csv.zip` 157,109,169 bytes (965,757,797 unpacked), `test.csv.zip` 157,224,887, `sample_submission.csv.zip` 210,385. `train.csv` counted: 145,231 rows x 1,934 columns, namely `ID`, 1,932 anonymised columns numbered `VAR_0001` to `VAR_1934` (two numbers unused) and `target` (111,458 zeros, 33,773 ones). `ID` runs from 2 to 290,463 in row order and uses about half the numbers in that range; the test file has no labels. The data page: "a high-dimensional dataset of anonymized customer information. Each row corresponds to one customer", with "many "placeholder" values ... to match with internal systems at Springleaf". One table, no join.
- The task's table: one row per training customer, 145,231 rows (counted). Of the 1,932 inputs, 5 are constant (3 empty, 2 with one value) and 48 copy another column, which leaves 1,879: 1,836 numeric, 27 string (a US city with 12,385 values, two state columns, two job-title columns with 1,823 and 608 values, flags) and 16 dates. 51 further columns hold one value besides missing, so they act as missingness flags. The placeholder codes are spread over many columns: among the kept numeric columns, 257 contain 999999999 and 272 contain 9999. Three columns bear on the split. `VAR_0217` is filled in every row but 56 and runs from 2011-10-02 to 2012-11-01, 5,299 to 13,958 rows in each full month, while the response rate rises from 0.21 in late 2011 to 0.25 in autumn 2012; the other dates also end on 2012-11-01. `VAR_0204` runs from 2014-01-29 to 2014-02-01 in the same rows, next to `VAR_0202` = "BatchInquiry". `VAR_0212` reads as a person key ("starting with postal code plus 6 other digits", a forum post after the deadline, topic 17088): 7,632 rows (5.3%) share it with another row, in 3,712 groups of up to 5 rows. In 88.6% of these groups every row has the same target, and a row responded in 81.6% of cases when another row of its group responded, against 7.9% when none did. `VAR_0217` differs between the rows of 99.8% of the groups.
- Access: Kaggle login and the competition rules. This account has entered the competition (`userHasEntered` true), so the download works; the training file was read in a scratch folder on 2026-11-08. The rules: "Participants must use the Data solely for the purpose and duration of the Competition" and "Any use of Data outside of the Competition is prohibited" (a licence note, never a verdict reason, EV-4).
- Changes the call: the regime and an identifier; the priority stays 2 (gap 0, use case +, source 0, shape +, risk -, the risk point already taken). `VAR_0217` is a date for every row that differs between the rows of one person, so it is likely the mailing or record date: a temporal split by it is available (SPLIT-7), though the column's meaning is hidden and has to be argued at /add-dataset. `VAR_0212` is an identifier and leaves (CLEAN-22). The repeat customers carry their response across rows: Kaggle's random split let teams copy it from train to test ("from a naive xgboost of 0.79321 we went up to 0.79787"), so a temporal or grouped split must keep one person's rows apart (SPLIT-13, SPLIT-29). `VAR_0204`, a batch inquiry 15 months after the latest other date, raises a timing question: if the bureau attributes were pulled then, they postdate the mailing (LEAK-10, LEAK-38), and the anonymised columns do not say which ones came from that inquiry.
- Not checked: the test file (not downloaded); what `VAR_0217` and the 2014 inquiry record; the winners' write-ups (topic 17081, "Solution Sharing", not read).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).
