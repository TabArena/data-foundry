---
unique_name: osha_inspection_violations
name: 'OSHA Enforcement Data: Inspection and Violation tables (US Department of Labor)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- AI-Filled (Verify)
original_source: GOV Website
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.osha.gov/data
- https://apiprod.dol.gov/v4/datasets
- https://data.dol.gov/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: OSHA's own inspection and violation tables, updated daily, from which "did the inspection find a (serious) violation" can be built for the inspections OSHA plans; the task of `labour_inspection_compliance` at another inspectorate, with dates and far more inspections.
- Source: US Department of Labor, OSHA enforcement data on the DOL Open Data Portal (osha.gov/data points to data.dol.gov; catalog read 2026-10-31): `OSHA_inspection` (id 10334, "the inspection case detail for OSHA inspections"), `OSHA_violation` (10338, "details about violations and penalty assessments resulting from OSHA inspections"), `OSHA_violation_event` (10357, "the current status OSHA violations, including penalty, abatement and settlement"), `OSHA_related_activity` (10336), `OSHA_emphasis_codes` (10337) and `OSHA_optional_code_info` (10356), all updated "Daily"; the osha.gov inspection search holds data through 12/04/2025. Row counts and the data dictionary were not read (the API needs a key): one row per inspection, joined to violations on the inspection number (`activity_nr` per the scout), federal and state-plan inspections from the 1970s per the scout.
- Use case: an OSHA area office (or a state plan) chooses establishments for programmed inspections before the visit, from the industry, state, size, ownership and inspection history known then; the target is whether the visit finds a (serious) violation. The decision is documented for OSHA's targeting programmes (the Site-Specific Targeting programme studied by Johnson, Levine and Toffel, AEJ: Applied 2023, named by the scout, not read here) and, for the Norwegian inspectorate, by Flogard and Mengshoel 2022 (the `labour_inspection_compliance` task). Fit direct for programmed inspections; unprogrammed ones (complaints, accidents, referrals) are not chosen by a model. Regime temporal (inspection open dates).
- Siblings and duplicates: `labour_inspection_compliance` (`Yes`, shipped: 63,634 Norwegian inspections of 2012-2019 without a date column, so IID) is another inspectorate, not a duplicate (PROV-4); `osha_accidents_data` (`TBD -> 2nd Tier`) and `osha_severe_injury_reports` (this run) are other OSHA tables with other tasks (PROV-7). No other record of the enforcement tables (grep: osha, dol.gov). External collections: none found.
- Better data: found as better data for `labour_inspection_compliance`; no further search this round.
- Papers and pages: the DOL portal catalog; Johnson, Levine and Toffel 2023 (the scout's reference, not read).
- Metric: none found for the OSHA data (no competition or paper read that scores it; the web search budget was used up). The sibling's source scores precision at the median score (Flogard and Mengshoel 2022, Sec. 6.5), a deliberate choice for that inspectorate (MET-5); here the fallback `roc_auc` (MET-8), unless the curator carries the sibling's metric over.
- Risks for /add-dataset: build the target from the violation table (deleted, contested and vacated citations, the violation type) and decide "any" or "serious" (USE-5); keep programmed inspections only, or the inspection type as a feature; drop fields recorded at or after the visit (close dates, inspection scope, reasons for no inspection, penalties) and check the establishment size and union status, which may be recorded on site (LEAK-10); history features from earlier inspections only (LEAK-12); several tables to join and millions of rows to cut to a time window.
- Priority: gap 0 (industry & manufacturing, binary, temporal not thin), use case + (OSHA's targeting of programmed inspections, documented), source + (DOL, maintained tables), shape + (many dated inspections, mixed types), risk - (target and history built from joined tables, post-visit fields).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `labour_inspection_compliance`.
- as published: one row per inspection (federal and state-plan OSHA, from the 1970s to date), joined to violations by activity_nr; the catalog listing does not give row counts (millions of inspections; to confirm ...; target: whether an inspection finds non-compliance: at least one (serious) violation cited, from the Violation table joined on the inspection number; access: open (bulk files on the DOL portal; the API needs a free key).
- Why: the same task as labour_inspection_compliance (Flogard and Mengshoel's non-compliance problem: will the inspected organisation be found non-compliant), from another labour inspectorate; features of the same kind (organisation profile, inspection type) known before the inspection; a peer-reviewed line of work uses it ...
- Adds: dated inspections (LICD has no date column, so its split is forced IID; here a temporal split is possible), far more units than LICD's 63,634 Norwegian inspections of 2012-2019, and a maintained, daily-updated government source; risks to settle at screening: inspection types triggered by complaints or accidents, ...
