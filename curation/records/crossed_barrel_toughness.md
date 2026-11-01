---
unique_name: crossed_barrel_toughness
name: Crossed barrel toughness (BEAR autonomous lab, Liang et al. benchmark)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/PV-Lab/Benchmarking/tree/main/datasets
- https://arxiv.org/abs/2603.04692
- https://doi.org/10.1038/s41524-021-00656-9
- https://doi.org/10.1126/sciadv.aaz1708
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 600 3D-printed crossed-barrel designs from a factorial grid of four design parameters, each tested three times by a robot, with real measured toughness; a designed response surface with four numeric inputs, published to benchmark Bayesian optimisation rather than prediction.
- Source: Gongora, Xu, Perry, Okoye, Riley, Reyes, Morgan, Brown, "A Bayesian experimental autonomous researcher for mechanical design", Science Advances 6(15):eaaz1708 (2020; PMC7148087): "600 distinct designs were tested in triplicate without human intervention" (Results); the design x = (n, θ, r, t), number of columns, twist angle, outer radius and wall thickness; toughness "Defined as the area under the force (F)–displacement (D) curve" (Results); raw data at kablab.org/data (Data and materials availability; not opened). As used here: Liang et al., "Benchmarking the performance of Bayesian optimization across multiple experimental materials science domains", npj Comput Mater 7:188 (2021), repository github.com/PV-Lab/Benchmarking, file `datasets/Crossed barrel_dataset.csv` (48 KB; read 2026-10-31): 1,800 rows x 5 columns `n, theta, r, t, toughness`, n in {6, 8, 10, 12}, theta at 9 levels from 0 to 200, r at 11 levels from 1.5, t in {0.7, 1.05, 1.4}; 600 distinct designs with three rows each. Licence: MIT in the GitHub metadata, BSD-2-Clause in the README (noted only, EV-4).
- Use case: an engineer or an autonomous lab decides which design to print and test next, from a surrogate model's toughness prediction for untested designs (the paper's BEAR loop); fit approximate: the benchmark would score prediction over the grid, while the source scores how fast the optimisation finds the best design; regime grouped by design (the three replicates of a design are one unit, SPLIT-23), with designs IID.
- Siblings and duplicates: none (grep: crossed barrel, PV-Lab, Gongora, AgNP, P3HT, AutoAM, TREDBench); the repository's four other experimental sets (AgNP, P3HT, perovskite, AutoAM) have no record. Precedent for an experimental engineering regression: `concrete_compressive_strength`. External collections: the Liang et al. BO benchmark; TREDBench (Regenwetter, Yu, Picard, Ahmed, arXiv 2603.04692, 83 real-world regression datasets, the Zotero item; its abstract does not list the datasets, so the membership is from the run's first pass).
- Better data: from the curator's Zotero collection (item 115); no further search this round.
- Papers and pages: Gongora et al. 2020; Liang et al. 2021 (doi 10.1038/s41524-021-00656-9); Regenwetter et al. 2026.
- Metric: none found for a prediction: Liang et al. score the optimisation with acceleration and enhancement factors (README abstract), Gongora et al. the campaign's best toughness; so the fallback `rmse` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: four numeric inputs on a regular grid, so models interpolate a smooth surface and replicate noise may cap them all (probe TP-4 and TP-2); keep the replicates of a design together (SPLIT-23, SPLIT-24) or average them (the source's unit is the design); whether a designed grid of measured parts is a "real random draw" in the sense of SEL-16 (the values are measured, the inputs are set by design) is the curator's call; the paper's force threshold (about 5 kN) and the raw force-displacement curves at kablab.org are not in the benchmark file.
- Priority: gap 0 (regression, materials and grouped not thin), use case 0 (the source's decision is the next experiment; prediction over the grid approximates it), source + (a Science Advances paper and a benchmark repository), shape 0 (600 designs, but four numeric inputs), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 115: "Engineering Regression Without Real-Data Training: Domain Adaptation for Tabular ...".
- as published: 3D-printed crossed-barrel structures: 1,800 rows, 600 grid designs tested in triplicate (Gongora et al. 2020, PMC7148087). 'Crossed barrel_dataset.csv' is 48 KB with columns n, theta, r, t, toughness.; target: Toughness measured in a robotic compression test (regression); access: open.
- Why: Real experimental engineering data; TREDBench's other engineering sets are simulated.
- Adds: Real lab-measured design regression. Weak shape: 4 features on a full grid, 600 distinct designs (grouped split by design), replicates as noise. Low priority. Sizes and grid confirmed against the first pass.
