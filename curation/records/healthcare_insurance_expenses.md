---
unique_name: healthcare_insurance_expenses
name: healthcare_insurance_expenses
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
year: '?'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/arunjangir245/healthcare-insurance-expenses/
notebook_path: datasets/beyond_iid/old_iid/healthcare_insurance_expenses/healthcare_insurance_expenses.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

predict medical insurance costs incurred by the insured person based on basic features. Likely very simple tasks

Potential issue: unclear source of data

Lennart: no direct objection, weird task anyhow

Andrej: Might be trivial and not a meaningful task

**Assessment (AI, 2026-10-06):** generated data, with the generator recovered. The Kaggle upload (arunjangir245, 2023) is a copy of mirichoi0218's "Medical Cost Personal Datasets" `insurance.csv`, which comes from Brett Lantz's book Machine Learning with R (via github.com/stedy/Machine-Learning-with-R-datasets); the CRAN package `liver`, which ships the same data, says "This dataset is simulated on the basis of demographic statistics from the US Census Bureau" (https://rdrr.io/cran/liver/man/insurance.html). The charges of 1,220 of the 1,338 rows (91.2%) equal, to the cent: 1072 + 3.363 age^2 + 1.39 bmi + 589 children - 489 [male] + region (northeast 0, northwest -200, southeast -583, southwest -583) + [smoker] (1500 + 489 bmi + 15000 [bmi > 30]). The other 118 rows add an extra cost of mean 14,482 and sd 4,890 (2,380 to 25,741, no skew), drawn independently of every feature (about 9% of each subgroup). The features were sampled with dependencies (smoking by sex and region, BMI by region, children by age; ages 18 and 19 twice as frequent as the others). So the best possible prediction is known: RMSE 0.358 on log charges (skill 0.848), and the best BeyondArena configurations reach 0.357 (CAUSILO; the top seven within 0.004), so the ranking at the top is noise. The curation guidelines exclude simulated data (criterion 4B, marker `AHDS`). None of our probes flagged it (task probes: no flags; best untuned skill 0.825).

CC (2026-10-06, Lennart): Retired: simulated data (criterion 4B). The charges are a formula of the features plus a random extra cost (the assessment above has the formula and the evidence), so the best possible score is known and the benchmark's best methods already reach it. The new generated-data probe flags it (`formula`: 72% of rows fit exactly, 2% for a shuffled target).

## Reference

https://www.kaggle.com/datasets/arunjangir245/healthcare-insurance-expenses/
