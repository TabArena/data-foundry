---
unique_name: open_policing_stop_outcome
name: 'Stanford Open Policing Project: standardized traffic and pedestrian stop records'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
original_source: Website
year: '2017'
domain: social science
source_links:
- https://openpolicing.stanford.edu/data/
- https://github.com/stanford-policylab/opp/blob/master/data_readme.md
- https://doi.org/10.1038/s41562-020-0858-1
- https://arxiv.org/abs/1706.05678
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the Stanford Open Policing Project's standardized stop records (over 200 million stops of dozens of agencies), published to investigate police stops and racial disparities; the run's target, the officer's own disposition (`outcome`), fits no actor's decision, the doubt that keeps `traffic_violations` at 2nd Tier.
- Source: Stanford Computational Policy Lab (Pierson, Simoiu, Overgoor, Corbett-Davies, Jenson, Shoemaker, Ramachandran, Barghouty, Phillips, Shroff, Goel), https://openpolicing.stanford.edu/data/, first released with arXiv 1706.05678 (2017); paper "A large-scale analysis of racial disparities in police stops across the United States", Nature Human Behaviour 4, 2020. Purpose: "help researchers, journalists, and policymakers investigate and improve interactions between police and the public" (home page). As published: one cleaned file per state patrol or city (88 in 42 states, 2000-2020, by the run's count, not recounted), one row per stop, standardized columns whose coverage varies by location; "Fields with an asterisk were removed for public release due to privacy concerns" and most columns are digit-sanitized (data README). Targets: `outcome` ("The strictest action taken among arrest, citation, warning, and summons"), `citation_issued`, `warning_issued`, `arrest_made`, `search_conducted`, `contraband_found`.
- Use case: none for `outcome`: the officer decides it at the stop, and a model of it describes enforcement practice (a look back, SEL-3, USE-2). `contraband_found` given a search (the paper's hit rate) would sit on a search decision, but scoring drivers by race, sex and age for searches is the profiling the source studies (a SEL-1 question). Fit none for now. Regime grouped by agency or temporal by stop date.
- Siblings and duplicates: `traffic_violations` (`TBD -> 2nd Tier`, priority 2, `No Good Target / Scientific Discovery`; Montgomery County's own log, cut to 5% on OpenML; Montgomery County is no separate file here, so no duplicate, PROV-4). External collections: none found.
- Better data: found as better data for `traffic_violations`.
- Papers and pages: the project page, the data README (github.com/stanford-policylab/opp), Pierson et al. 2020.
- Metric: none found (home page, README; the paper runs outcome and threshold tests, no prediction), so the fallback `log_loss` for `outcome`.
- Risks for /add-dataset: the target (SEL-3, USE-2); race and sex as inputs to a model of policing (SEL-1); recording differs by agency (one agency per task, or a grouped split); the `violation` text can fix the outcome (SEL-5, TP-4), as `Charge` does in the sibling.
- Consistency: a `No` under SEL-3 here holds for `traffic_violations` as well (same kind of record, same target); decide both together.
- Priority: gap 0 (social science is thin, but a police record fits it loosely, as in the sibling), use case 0, source + (a research lab, a README per location, a paper), shape + (millions of stops, dates, agencies), risk - (no decision for the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `traffic_violations`.
- as published: over 200 million records (project home page); 88 datasets in 42 states, statewide patrols and cities, from 6,921 stops (Owensboro, KY) to 31,778,515 (California State Patrol); start dates 2000-2014, ...; target: `outcome`: 'the strictest action taken among arrest, citation, warning, and summons' (README), plus citation_issued, warning_issued, arrest_made; also ...; access: open, Open Data Commons Attribution License.
- Why: same target as the OpenML traffic_violations cut (Violation.Type: citation, warning or repair order issued at a traffic stop) with features of the same kind: stop date, time and place, violation, vehicle make and model, driver age, sex and race
- Adds: a curated, documented, multi-jurisdiction release with a paper, about 100x the rows of the full Montgomery County table and 3,000x the OpenML 5% cut; standardized columns with a per-column coverage report per jurisdiction; jurisdictions as natural groups for a grouped split. Caveats: the use-case gap that tags the ...
