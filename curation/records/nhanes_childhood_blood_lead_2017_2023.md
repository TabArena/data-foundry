---
unique_name: nhanes_childhood_blood_lead_2017_2023
name: NHANES blood lead, cadmium, total mercury, selenium and manganese files for 2017-March 2020 pre-pandemic (P_PBCD) and August 2021-August 2023 (PBCD_L)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
year: '2021'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/PBCD_L.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_PBCD.htm
- https://tableshift.org/datasets.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the NHANES blood-lead files after TableShift's cycles (2017-March 2020 and 2021-2023), a newer release of the source behind `childhood_lead` (PROV-6) that allows a temporal test; the public 2017-2020 file has no blood lead for children aged 1-5.
- Source: CDC/NCHS NHANES laboratory files P_PBCD (2017-March 2020 pre-pandemic, first published November 2021) and PBCD_L (August 2021-August 2023, first published September 2024), joined by SEQN to the demographics and questionnaire files. The task as published: TableShift's Childhood Lead (Gardner et al. 2023), "the goal is to identify children 18 or younger with elevated lead blood levels" from questionnaire data, label blood lead above the CDC reference value of 3.5 ug/dL, 27,499 rows, shift by poverty-income ratio (tableshift.org). As published: P_PBCD 13,772 records, 11,107 with blood lead, lead for ages 6 and over only ("Blood Lead data for youth aged 1-5 years" are in the Research Data Center file P_PBY_R); PBCD_L 8,727 records, 7,586 with blood lead, "Examined participants aged 1 year and older were eligible", no restriction named. Children 18 or younger not counted.
- Use case: a paediatrician or health department decides which children to send for a blood lead test from questionnaire answers known before the draw (TableShift's framing); fit approximate: the curator doubted the setup on `childhood_lead` ("questionable setup", `No Good Target (yet)`); regime temporal by survey cycle, the reason this version exists (test on the newest children).
- Siblings and duplicates: `childhood_lead` (`TBD -> Yes`, TableShift): the same source and task, so this is a version of it (PROV-6), and the curator decides whether the build of `childhood_lead` takes these cycles or this record enters instead; `nhanes_undiagnosed_diabetes` and the run's other NHANES candidates are distinct tasks (PROV-7). External collections: TableShift has the earlier cycles (Childhood Lead, up to 2017-2018 per the run).
- Better data: found as better data for `childhood_lead`; no further search this round.
- Papers and pages: TableShift (Gardner, Popovic, Schmidt, NeurIPS 2023 Datasets and Benchmarks) and its datasets page; the P_PBCD and PBCD_L file pages.
- Metric: TableShift's page names none for Childhood Lead, and the benchmark reports accuracy for every task, a house convention (precedent `anes_voting_2026`, CC 2026-10-21: the fallback, not TableShift's accuracy); so the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none.
- Risks for /add-dataset: ages 1-5, the core screening age, are missing from the public 2017-2020 file; PBCD_L notes "a change to the lab methods for the August 2021-August 2023 cycle", a measurement shift right at the temporal test; P_PBCD merges 2017-2018 with the cut-short 2019-2020 fieldwork; about 67% of examined children aged 1-17 gave blood (PBCD_L), a selection to note; questionnaire items change across cycles; heavy joins per cycle.
- Priority: gap 0 (medical, binary and temporal are not thin), use case 0 (TableShift's framing, doubted by the curator), source + (NCHS file documentation and TableShift's task), shape + (several thousand children over several cycles, mixed features), risk - (a version of `childhood_lead`, ages 1-5 missing in 2017-2020, a lab-method change in the test wave).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `childhood_lead`.
- as published: P_PBCD: 13,772 records, 11,107 with blood lead, ages 6+ public (ages 1-5 in the Research Data Center); PBCD_L: 8,727 records, 7,586 with blood lead, examined participants aged 1+; participants aged ...; target: blood lead LBXBPB (ug/dL) at or above the reference value (3.5 ug/dL, TableShift's threshold), or the level itself; access: open.
- Why: the same target, population and questionnaire features as TableShift's Childhood Lead (27,499 rows, cycles up to 2017-2018, the latest cycle its page links); answers the record's own comment 'could use newer data?'
- Adds: the cycles after 2018 (2019-March 2020 and 2021-2023), so a temporal split can test on the newest children; about 18,700 more blood-lead measurements of all ages
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
