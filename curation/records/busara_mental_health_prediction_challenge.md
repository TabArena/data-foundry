---
unique_name: busara_mental_health_prediction_challenge
name: busara-mental-health-prediction-challenge
checked_by:
- Myunghwan
data_foundry_status:
- 'DF: Suspended'
suggestion: TBD -> Yes
priority: 3
collections:
- New (BeyondArena)
original_source: Zindi
year: '2018'
domain: social science
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/busara-mental-health-prediction-challenge/data
source_row: 923
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: a depression-screening task on a household survey with a named actor (clinics, NGOs, community health volunteers), in thin social science.
- Source: Zindi competition hosted by the Busara Center for Behavioral Economics, 2018-11-17 to 2019-01-28; data "from a 2015 study conducted by the Busara Center in rural Siaya County ... more than 70 features, including information about household composition, economic activity, financial flows and health", target `depressed` from "a depression screening tool" ("an epidemiological rather than clinical measure"); one table keyed by `surveyid`; row count not seen (data needs a login).
- Use case: "mental health providers such as local clinics, NGOs or community health volunteers" reach out to those at risk (the source's words); fit direct; regime IID, one respondent per row, one survey wave.
- Siblings and duplicates: no other Busara or Siaya record found. External collections: none found.
- Papers and pages: https://zindi.africa/competitions/busara-mental-health-prediction-challenge (Description, Data Description, Evaluation); the 2015 Busara study itself was not traced to a paper.
- Metric: error rate, "the percentage of survey respondents for whom you predict the 'depressed' variable incorrectly" (Zindi Evaluation page), a leaderboard metric (MET-4) on hard labels; the source fixes no threshold beyond the 0/1 submission (MET-6), inputs none.
- Risks for /add-dataset: check that no item of the screening tool is among the features (SEL-5) and that the health columns are not post-screening (USE-3); the label is a screening score from the same interview, which SEL-7 allows because respondents do not know it; Zindi's rule "Your models should not use any of the metadata provided" names columns to drop; size near the floor.
- Priority: gap + (social science thin), use case + (actor named by the host), source - (only the Zindi page; the study is not published), shape - (row count unknown, likely near 1,000), risk 0.

Zindi Busara challenge to predict mental-health (depression) status from household survey/socioeconomic data collected in Kenya. This is a genuine real-world predictive classification task on structured survey features with a clear binary target, which fits the IID tabular criteria well. The main risks are sample size after cleaning and possible heavy missingness/many sparse survey columns. A human should verify the row count, the exact target definition, the proportion of usable (non-text) features, and confirm there are no ethical concerns given the sensitive mental-health target.

CC (2026-11-05, Myunghwan): "Let's defer this then. Non-trivial modification seems required". Preserve the completed investigation; no current ship decision or authorization to implement an unspecified modification follows.

**Assessment (AI, 2026-11-05):** The bounded nested study retained 1,143 respondents, 65 predictors and all 30 original outer pairs, selecting configurations and thresholds using training data only. Selected accuracy was 82.878% versus 83.115% majority. ExtraTrees reached 83.167%, an uncertain gain that did not persist outside matching profiles; modest ranking signal does not establish source-accuracy improvement. Exact-profile lookup scored 82.992% overall, below majority: the measured 2.598% overlap does not make this a simple lookup task and supports the curator's conditional retention position. The original depressed indicator remains an epidemiological moderate-depression screen with undocumented instrument/cutoff and assessment timing, not a verified clinical diagnosis. Raw collection-time fields are excluded; questionnaire ordering and household links remain unverified. Carry forward the applied hold as TBD -> Yes / DF: Suspended with priority 3. Reopen only on a separate curator request grounded in a substantively justified revision or stronger source evidence, then qualify the affected task. Do not infer a Trivial, Too Small or No Signal finding, automatic metric replacement, warning acceptance or permission for more model search.
