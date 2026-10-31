---
unique_name: census_pdb_self_response
name: 'Census Planning Database: 2020 Census self-response rate by block group (Low Response Score task)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: GOV Website
domain: social science
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.census.gov/topics/research/guidance/planning-databases.html
- https://www.kaggle.com/c/us-census-challenge
- https://www.census.gov/newsroom/blogs/research-matters/2014/10/low-response-score-arises-out-of-crowdsourcing-solution.html
- https://www.census.gov/newsroom/blogs/random-samplings/2026/03/updating-the-planning-database.html
- https://api.census.gov/data/2026/pdb/blockgroup/variables.json
- https://www.census.gov/topics/research/guidance/planning-databases.2012.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the Census Bureau's own task, predicting a block group's census self-response from the Planning Database to target outreach and field follow-up, posed as the 2012 Census Return Rate Challenge on Kaggle (MAE weighted by population); 220,000 to 242,000 block groups per vintage; the vintage decides what is known before the census.
- Source: U.S. Census Bureau, Planning Database (PDB), annual vintages 2012-2026 at block group and tract level. The 2012 PDB (ACS 2006-2010 and 2010 Census statistics) is `pdb2012bgv9_us.csv`, "220354 rows x 179 columns" (its page); the 2026 PDB (ACS 2020-2024, 2020 Census operational variables, the Low Response Score) has 242,336 block groups x 385 columns and 85,396 tracts x 531 columns, reissued 2026-09-17 to correct the LRS. The 2020 Census self-response rates entered with the 2023 PDB and "the definitions were updated for the 2024 PDB" (Census blog, 2026-03). Kaggle "U.S. Census Return Rate Challenge" (2012-08-31 to 2012-11-11, 243 teams by the Kaggle API): "You're predicting Mail_Return_Rate_CEN_2010, the census mail return rate for each block group" (Data page). The year waits for the vintage we pin (PROV-9).
- Use case: Census Bureau planners, before a census or survey, find areas likely to self-respond poorly and target outreach, partnerships and costly nonresponse follow-up (the ROAM tool); the challenge's Description: "The Census Bureau will use this model for planning purposes for the decennial census and for demographic sample surveys"; the 2014 blog: the score helps planners "manage field resources and develop targeted self-response and nonresponse follow-up strategies more efficiently". Fit direct for the challenge's task, approximate where inputs are concurrent with the census predicted. Regime grouped: the challenge split by tract ("Each census tract ... randomly assigned to "Training", "Public Leaderboard", or "Private Leaderboard". So all block groups from a given tract are in the same set"); a split across census rounds (2010 to 2020) mirrors the use more closely but the geographies change (SPLIT-3, to decide).
- Siblings and duplicates: none in `curation/records/` (searched planning database, low response, census challenge, self-response); `anes_voting_2026` and `ces_validated_turnout` are person-level participation tasks, not area response. External collections: none found.
- Better data: from the gap scout for social science; no further search this round.
- Papers and pages: the PDB page and its 2012 vintage page; the Kaggle competition (Description, Data, Evaluation, Rules and Winners pages read through the Kaggle API); Census blog "Low Response Score Arises Out of Crowdsourcing Solution" (2014): the LRS is an ordinary least squares model on PDB variables, after the winning entry (342 variables); Census working paper RRS2014-08 on the challenge (fetched, text not extracted).
- Metric: "Mean absolute error (weighted by Tot_Population_CEN_2010)" (Kaggle Evaluation page; the API names it "Normalized Weighted Mean Absolute Error"), a competition metric (MET-4); the winner came within 2.598 percentage points (Winners page). Inputs: the block group's 2010 population as a weight, a scoring column that ships in the 2012 PDB (MET-2); a 2020 target would need the 2020 population as its weight.
- Risks for /add-dataset: which target and vintage: the 2010 mail return rate with the 2012 PDB (the challenge's task; its 2010 Census counts come from the census being predicted, which the challenge allowed) or the 2020 self-response rate with a vintage whose ACS precedes the census (the 2026 PDB uses ACS 2020-2024, after the 2020 Census: inputs after the outcome, LEAK); drop the LRS (a model fit on the target, LEAK-27) and every other response or return rate of the same census; 2010 and 2020 geographies differ; the challenge's rules allowed some outside data (2000 participation rates), not needed.
- Priority: gap + (social science has one accepted dataset), use case + (the Bureau names the decision), source + (Census Bureau documentation and a competition), shape + (220,000+ block groups, 179 to 385 columns, tracts and counties as groups), risk - (the vintage and concurrent census inputs, the LRS leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for social science.
- as published: 2026 PDB: 242,336 block groups x 385 columns (tract file 85,396 x 531), 50 states, DC and Puerto Rico; 2010 Census mail return rate in the older vintages on 2010 geographies; target: self_response_rate_cen_2020: percentage of housing units providing a sufficient internet, paper or phone self-response in the 2020 Census (regression; the ...; access: open.
- Why: An agency's own predictive task with a named decision and a public competition behind it; documented variables; areas, not people, so no SEL-1 question.
- Adds: Public services; a large regression on aggregate area features; grouped regime (state, county) and two census rounds (2010, 2020). Risks for /add-dataset: drop Low_Response_Score (a model fit on the target, LEAK-27) and all mode-specific *_cen_2020 response and return rates; choose a vintage whose ACS inputs precede ...
