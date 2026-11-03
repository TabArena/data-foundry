---
unique_name: ces_validated_turnout
name: Cumulative CES Common Content (Cooperative Election Study), validated general-election turnout
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: '2026'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.7910/DVN/II2DB6
- https://github.com/kuriwaki/cces_cumulative
- https://tischcollege.tufts.edu/research-faculty/research-centers/cooperative-election-study
- https://sda.berkeley.edu/Abstracts/CEScum2024.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the pre-election turnout task of the accepted `anes_voting_2026` with about 541,000 even-year respondents and turnout validated against official voter files instead of self-report; the match fields and post-election items must go.
- Source: Cooperative Election Study (CCES/CES; Harvard and Tufts, fielded by YouGov), Common Content since 2006; the cumulative file by Shiro Kuriwaki on Harvard Dataverse (doi 10.7910/DVN/II2DB6), version 12 of 2026-07-14, CC0. As published: "n = 718,955" respondents of 2006-2025, one table (dta, feather, rds) with 109 columns ("demographics, geography, vote choice, validated vote, representative approval, and views on the economy"), and a guide (guide_cumulative_2006-2025.pdf). Target `vv_turnout_gvm`, "Validated turnout General Election" (guide p. 25): Voted 312,185, No Record of Voting 227,038, No Voter File 1,733, missing 177,999; even years 2006-2024.
- Use case: a campaign or pollster, before the election, scores who will turn out from pre-election answers (likely-voter screens, get-out-the-vote contact lists); our framing, as for `anes_voting_2026`; the CES names no prediction. Fit direct for a likely-voter model. Regime temporal by election year, like the sibling; each year is a new cross-section.
- Siblings and duplicates: `anes_voting_2026` (`Yes`, ANES, about 70,000 respondents, self-reported turnout) is the record it was found for, a different study (PROV-4: its own record); `social_pressure_turnout_michigan_2006` and `voter_mobilization_turnout_iowa_michigan_2002` are field experiments on registered voters, other tasks. No earlier record of the CES. External collections: none known.
- Better data: found as better data for `anes_voting_2026`, and by the gap scout for social science; no further search this round.
- Papers and pages: the guide and the cces_cumulative GitHub README; Ansolabehere and Hersh (2012), cited by the guide for the vote validation.
- Metric: none found: the CES defines no prediction task (Dataverse description, guide). The fallback `roc_auc`, as for `anes_voting_2026`; inputs none.
- Risks for /add-dataset: the guide: "the result of not matching to a voter file is collapsed with the result of matching to a voter file and having no indication of turning out to vote", so a non-match counts as a non-voter (USE-5); the match vendor changed from Catalist to TargetSmart in 2022 (guide), a shift in how the target is measured across test years; drop the other `vv_*` fields and `vvweight*` (from the same match, "missing for anyone not validated as a actively registered voters") and every post-election item (`voted_*`, `voted_turnout_self`, `tookpost`, `*_post`), as in the ANES leak fix (LEAK-10); keep the pre-election `intent_turnout_self`; above the row cap, so a cut of elections.
- Priority: gap + (social science has one accepted dataset), use case 0 (our framing), source +, shape + (about 541,000 validated rows, mixed types, ten elections), risk - (match fields that leak, the collapsed non-match).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `anes_voting_2026`; the gap scout for social science.
- as published: 718,955 respondents x 109 columns, survey years 2006-2025 (Dataverse description and repo README); validated turnout in even (federal election) years only; voter-file match by Catalist up to 2020, ...; target: vv_turnout_gvm: validated turnout in the general election, from YouGov's match of respondents to official voter files (guide: 'Validated turnout General ...; access: open.
- Why: Same task as anes_voting_2026 (pre-election interview -> turnout) with about 50 times the respondents and a target measured from official voter files rather than self-report (ANES self-reports 78% voting; over-reporting is the known flaw). Strong source: a national academic election study with a codebook, CC0 on ...
- Adds: A second elections dataset with a better-measured target; temporal regime (election years 2006-2024); mixed types (state, congressional district, party ID, ideology, approval, economy views, demographics, pre-election vote intent intent_turnout_self). Risks for /add-dataset: drop post-election items (voted_*, *_post) ...
