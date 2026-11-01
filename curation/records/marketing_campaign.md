---
unique_name: marketing_campaign
name: Marketing_Campaign
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
original_source: Kaggle
year: '2020'
required_split:
- Random (IID)
source_links:
- https://github.com/nailson/ifood-data-business-analyst-test
- https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign
notebook_path: datasets/beyond_iid/old_iid/marketing_campaign/marketing_campaign.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

From O. Parr-Rud. Business Analytics Using SAS Enterprise Guide and SAS Enterprise Miner. SAS Institute, 2014. train a predictive model which allows the company to maximize the profit of the next marketing campaign. Predict who will respond to a product/service offer

Potential issue: Artificial

Lennart: Likely a valid predictive task

Andrej: License; Need to check book on how the data was obtained - could be artificial

CC (2026-10-06, Lennart): Kept after the task-probe review: the `no_spread` flag (three untuned families at skill +0.77 to +0.80) does not hold for tuned methods. On BeyondArena the best (TabFM) reaches ROC AUC 0.926 and the median 0.909, with no other method within noise of the best (Kendall's W 0.84).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Complain.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset card states a goal (maximise the next campaign's profit) but no evaluation metric.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `Education` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37: Education left unordered with a note (2n Cycle cannot be placed).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `hillstrom_email_campaign` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-01):** generated data (SEL-16, PROV-3; issue #38). The file is the sample data of the iFood Data Analyst Case, the iFood Brain team's hiring test (https://github.com/nailson/ifood-data-business-analyst-test, CSV and PDF added 2020-03-18): all 2,240 rows and 29 columns of the Kaggle upload equal its `ml_project1_data.csv`, as does the upload of `customer_personality_analysis`. The case PDF, page 1: "you are presented a sample dataset, that mocks metainformation on the customer and on iFood campaign interactions with that customer", for a made-up company in the retail food sector. `Z_CostContact` (3) and `Z_Revenue` (11) reproduce the PDF's pilot campaign (6,720 MU cost, 3,674 MU revenue from 334 responders). Measured marks of a generator: 193 groups of identical customers, 21 of their 209 pairs with different labels; `Recency` uniform over 0-99 and unrelated to spend, yet predictive; `Dt_Customer` flat over 699 days; 98.6% of `MntFishProducts` on ceil(1.3 x an integer) against 76-78% in the other spend columns; planted values (`YOLO`, birth year 1893, income 666,666). The first publication is the case of 2020, not the SAS textbook (Parr-Rud 2014) the Kaggle page credits, which no source ties to this file; `year` is now 2020 and the case leads `source_links` (PROV-8, PROV-9). Precedent: `churn` and `healthcare_insurance_expenses` (CC 2026-10-06). The BeyondArena collection keeps its pinned container, as for those two.

CC (2026-11-01, Lennart): Don't ship on the review page of issue #38; retired from the TabArena v0.2 working copy as generated data (`AHDS`). The folder is removed and `v2_path` cleared.

## Reference

https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign
