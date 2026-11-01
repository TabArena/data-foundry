---
unique_name: indonesia_dhs_2017_contraceptive_method
name: Indonesia Demographic and Health Survey 2017 (IDHS 2017), women's individual recode
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Ethical Issue
tags:
- AI-Filled (Verify)
original_source: Other
source_links:
- https://www.dhsprogram.com/pubs/pdf/FR342/FR342.pdf
- https://api.dhsprogram.com/rest/dhs/surveys/ID2017DHS?f=json
- https://www.dhsprogram.com/pubs/pdf/FR19/FR19.pdf
- https://api.dhsprogram.com/rest/dhs/surveys?countryIds=ID&f=json
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the 2017 wave of the survey programme `cmc` was cut from (49,627 women against cmc's 1,473), real and well documented, but the curator's open question on cmc (ethics, and whether anyone predicts a method the woman reports in the same interview) applies unchanged.
- Source: Indonesia Demographic and Health Survey 2017, Badan Pusat Statistik and BKKBN with the DHS Program (ICF); final report FR342. DHS API (ID2017DHS): 49,627 women and 10,009 men, report published 2018-09, data released 2019-07-03. As published: the standard DHS recode files (the women's individual recode has one row per woman aged 15-49 and several thousand variables), on registration with a project description. Earlier waves (DHS API): 1987 (11,884 women), 1991 (22,909), 1994 (28,168), 1997 (28,810), 2002-03 (29,483), 2007 (32,895), 2012 (45,607). UCI says of cmc: "a subset of the 1987 National Indonesia Contraceptive Prevalence Survey", the 1987 DHS-I wave (ID1987DHS).
- Use case: cmc's framing, the current method (none, short-term, long-term) from the woman's and the husband's demographics; DHS publishes the survey for indicators (prevalence, unmet need), not for an individual prediction; a family-planning programme targeting outreach would be the actor. Fit approximate at best. Regime: one cross-section per wave; IID within 2017, or temporal across harmonised waves.
- Siblings and duplicates: `cmc` (TBD -> 2nd Tier with `Outdated` and `Ethical Issue`; CC: "Unsure whether this is a reasonable task (ethically and from an ML perspective)", then "Still very likely ethical issues, but need to evaluate again"); `dhs_child_anemia`, `dhs_childhood_anemia` (other DHS tasks, candidates of this run). A newer release of the same survey programme as cmc (PROV-6): the curator decides which one enters. External collections: cmc is in TabSTAR and was a TabArena reject; the 2017 wave in none found. The `Ethical Issue` marker is carried over from cmc as the open concern, not as a decision.
- Better data: found as better data for `cmc`; a newer release of the same source (PROV-6).
- Papers and pages: FR342 (dhsprogram.com/pubs/pdf/FR342/FR342.pdf), FR19 (the 1987 report), the DHS API survey list.
- Metric: none found (the report defines indicators, no prediction task; the cmc UCI page gives none), so the fallback `log_loss` for three classes (MET-8).
- Risks for /add-dataset: SEL-7 (the target is the respondent's own report in the same interview as the features; a screening framing such as unmet need would be the decision-bearing alternative) and SEL-1 as raised on cmc (a reproductive choice predicted from religion, education and the husband's characteristics); target and features rebuilt from the recode, choosing among thousands of variables, several of which sit next to the target (fertility preferences, contact with family-planning workers; LEAK-10); survey weights and clusters ship (a cluster-grouped split is possible); registration (EV-4, no criterion).
- Priority: gap + (multiclass is thin), use case 0, source + (national statistics office with the DHS Program, full documentation), shape + (49,627 women, many mixed features, seven waves), risk - (the cmc questions on ethics and SEL-7).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `cmc`.
- as published: 49,627 women aged 15-49 (and 10,009 men), fieldwork Jul-Sep 2017; earlier waves 1991 (22,909), 1994 (28,168), 1997 (28,810), 2002-03 (29,483), 2007 (32,895), 2012 (45,607) women; cmc is 1,473 ...; target: current contraceptive method (none / short-term / long-term, from the DHS current-method variables), as in cmc; access: registration.
- Why: cmc is a subset of the 1987 National Indonesia Contraceptive Prevalence Survey, which was the Indonesia DHS-I survey (ID1987DHS in the DHS API; the 1989 literature calls it 'the 1987 NICPS/DHS'). The 2017 wave asks the same questions: wife's and husband's age and education, children ever born, religion, work, ...
- Adds: 30 years newer and about 30 times as many respondents (one wave), seven waves 1987-2017 for a temporal split, a measured wealth index instead of the hand-made standard-of-living index. The record's Ethical Issue marker would apply to the new wave as well
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
