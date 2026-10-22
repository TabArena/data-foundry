---
unique_name: moneyball
name: Moneyball
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2000'
domain: Other
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/wduckett/moneyball-mlb-stats-19622012/data
- https://www.openml.org/search?type=data&id=41021
source_row: 802
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: MLB team seasons 1962-2012 with runs scored as the target and same-season batting rates as features; a teaching dataset for the Moneyball story, an explanatory regression more than a prediction.
- Source: The Analytics Edge (MITx 15.071x on edX), data "gathered from baseball-reference.com"; re-uploaded to Kaggle by wduckett (baseball.csv, 67 KB) and to OpenML as 41021 "Moneyball" (2018, target `RS`). As published: 1,232 rows x 15 columns (Team, League, Year, RS, RA, W, OBP, SLG, BA, Playoffs, RankSeason, RankPlayoffs, G, OOBP, OSLG; 3,600 missing values, the playoff ranks and the opponent rates mostly). Year in the record (2000) is the Moneyball era, not the publication (the course, about 2013; Kaggle about 2017).
- Use case: the source's own framing is understanding: the data "can be used to better understand their methods", with questions such as "How does a team make the playoffs?" (OpenML description, copied from Kaggle). The course used the regression of RS on OBP and SLG to estimate how many runs a roster would score from its players' rates; here the rates are measured in the same season as the runs, so the fit to a decision is approximate at best. Regime temporal by Year if kept (the CC's point).
- Siblings and duplicates: none among the records; OpenML 41021 and the Kaggle copy are the same table (one record). External collections: TabSTAR. TabArena v0.1 put it on its reject list (CC: "clearly not a predictive performance task but an analytics task. Linear model best in TabRepo. Could include to also cover this bias").
- Papers and pages: The Analytics Edge lecture on Moneyball; no paper defines a task.
- Metric: none found (OpenML 41021, the Kaggle page, the course description; the course reports R-squared of a linear model, not a deliberate criterion), so the fallback (rmse).
- Risks for /add-dataset: same-season outcomes as features (W, Playoffs, RankSeason, RankPlayoffs follow from RS; RA is the opponents' runs), to drop under LEAK rules; RS is close to linear in OBP and SLG (TP-4 to probe, the CC's "linear model best"); temporal split by Year.
- Priority: gap 0 (domain Other is never thin), use case 0 (explanatory framing), source 0 (a course dataset re-uploaded, no codebook beyond column names), shape + (1,232 team seasons over 50 years, a temporal structure), risk - (same-season leaks, a near-linear target).

The Moneyball MLB stats dataset (1962-2012, OpenML 41021), estimating runs scored from team-season statistics. The curator notes it is clearly an analytics task rather than a predictive-performance task, with a linear model best in TabRepo, and may require a temporal split. It is in TabArena Reject but the curator suggests it could be included to cover the linear-model bias. This is borderline: a real dataset with a clear regression target but weak as a predictive benchmark and likely small. TBD -> 2nd Tier; a human must confirm size, the temporal split, and whether the analytics framing is acceptable.

---

CC: "Baseball dataset that estimates the runs scored. Might be relevant task. Might require temporal split, but need to understand the task better. In general this is clearly not a predictive performance task but an analytics task. Linear model best in TabRepo. Could include to also cover this bias"

## Reference

Kaggle (https://www.kaggle.com/datasets/wduckett/moneyball-mlb-stats-19622012/data), originally from The Analytics Edge course on EdX (https://www.edx.org/learn/analytics/massachusetts-institute-of-technology-the-analytics-edge). Data collected from baseball-reference.com
