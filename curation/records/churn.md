---
unique_name: churn
name: churn
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
year: '2005'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=40701
notebook_path: datasets/beyond_iid/old_iid/churn/churn.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

5000 sample telephony account churn data. Likely outdated; in the book (old and new eversion) that mentions the original data, it only talks about 3333 samples and a slightly different class ratio; likely the book only used a train split but test split somehow was able to be used by openml

Potential issue: Outdated, source missing

Lennart: source information missing otherwise okay

Andrej: Fits criteria

**Assessment (AI, 2026-10-06):** artificial data. The data comes from the MLC++ library (SGI); the R package `modeldata` (`mlc_churn`) quotes a note in the source files: the data are "artificial based on claims similar to real world" (https://modeldata.tidymodels.org/reference/mlc_churn.html). The data agrees: the area code (408, 415, 510: three California codes) is spread over all 51 states independently of the state (chi-squared p = 0.37); day, evening and night calls share one distribution (mean 100, sd 20), evening and night minutes another (200, 50); every charge is minutes times a fixed rate (0.17, 0.085, 0.045, 0.27); and the label follows crisp rules: an international plan with more than 13 international minutes churns in 79 of 79 rows, with fewer than 3 international calls in 89 of 89, and a depth-5 tree reaches 97.9% accuracy. The curation guidelines exclude simulated data (criterion 4B, marker `AHDS`). None of our probes flagged it (task probes: no flags).

CC (2026-10-06, Lennart): Retired: artificial data (criterion 4B; MLC++ calls it "artificial based on claims similar to real world", evidence in the assessment above). The new generated-data probe flags it (`rule_leaves`: pure rules cover 26% of the churners on held-out rows).
