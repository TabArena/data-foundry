---
unique_name: uspto_patex_grant_outcome
name: USPTO Patent Examination Research Dataset (PatEx)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.uspto.gov/ip-policy/economic-research/research-datasets/patent-examination-research-dataset-public-pair
- https://data.uspto.gov/bulkdata/datasets/ecopair
- '# technical documentation of the 2019 release and the 2022 addendum'
- https://www.uspto.gov/sites/default/files/documents/PatEx-2019-Technical-Doc.pdf
- https://www.uspto.gov/sites/default/files/documents/oce-patex-technical-addendum-2022.pdf
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> Yes`, priority 2: the USPTO's research release of every public patent application (more than 13 million in the 2022 release) with filing data, examiner unit, classes and the current status; whether a utility application ends granted or abandoned matters to applicants, but the source poses no prediction, the inputs are thin until other tables are joined, and pending applications have no label.
- Source: USPTO Office of the Chief Economist, Patent Examination Research Dataset (PatEx): first release 2014 (SSRN 2702637), releases from PEDS since 2019; the 2022 release, from PEDS data of June 2023, holds "more than 13 million publicly-viewable provisional and non-provisional patent applications" (page). The 2019 technical documentation (read): `application_data` has one row per application (15,494,295 in that release) and 22 columns (`application_number`, `filing_date`, `application_invention_type`, `examiner_full_name`, `examiner_art_unit`, `uspc_class`, `uspc_subclass`, `confirm_number`, `atty_docket_number`, `appl_status_desc`, `appl_status_date`, `file_location`, `file_location_date`, `earliest_pgpub_number`, `earliest_pgpub_date`, `wipo_pub_number`, `wipo_pub_date`, `patent_number`, `patent_issue_date`, `invention_title`, `small_entity_indicator`, `aia_first_to_file`). Other tables join by application number: `all_inventors`, `all_applicants` (2022), `transactions` (the prosecution history), `continuity_parents` and `continuity_children`, `foreign_priority`, `pat_term_adj`, `correspondence_address`, `attorney_agent`, `cms_documents` (2022 addendum: 549,192,929 document records). Sizes (2022): `application_data` 887 MB CSV, the full set 12.1 GB CSV.
- The task's table: utility applications with a final disposition (patented, or abandoned by `appl_status_desc`) from filing years old enough that nearly all are disposed; the count is not stated (13M+ in all; provisional 12% and design 5.6% in the 2019 release) x about 8 inputs from `application_data` known at or soon after filing (filing date, application type, USPC class and subclass, entity size, AIA flag, examiner art unit, title text), plus counts and countries of inventors and applicants, foreign priority claims and parent applications from the joined tables. Access: open through the USPTO Open Data Portal (a temporary signed URL per file); no licence stated.
- Use case: a patent attorney or applicant, when an application is filed or first examined, estimates the chance of allowance to plan the prosecution and its budget (appeals, continuations, abandonment), and an investor values pending applications the same way. Ours: PatEx is released for research on the examination process. Fit approximate: metadata only, without the claims a practitioner reads. Regime temporal by filing date.
- Siblings and duplicates: no patent-examination record (grep: patent, uspto: chemistry records built from patent texts and `uspto_reaction_yields`, other tasks). The Harvard USPTO Patent Dataset (HUPD, Suzgun et al. 2022, not read) poses acceptance prediction from the application texts of 2004-2018 filings, a text task with the same target (no record). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the PatEx page, the 2019 technical documentation and the 2022 addendum (read); "patent grant prediction" in the patent NLP literature (survey arXiv 2403.04105, not read).
- Metric: none found (the PatEx page and documentation pose no task), so the fallback `roc_auc` (MET-1, MET-8). Inputs: none.
- Risks for /add-dataset: pending applications have no outcome and the newest filing years are right-censored (LEAK-24, SPLIT-9: keep matured filing years, or fix a horizon); `examiner_full_name` and `examiner_art_unit` are those "as of the last office action" or "at the time of disposal" (documentation, A.2), so known only after examination starts (LEAK-10; the unit at first action would be the input); status, file location, publication and patent numbers and dates, transactions, term adjustments and child continuations come after filing (LEAK-10); a continuation of an abandoned parent ties two rows (SPLIT-13); `invention_title` is free text; inventor and examiner names are no inputs; the joins are heavy.
- Priority: gap 0 (no thin domain; binary and temporal covered), use case 0 (ours), source + (USPTO release with technical documentation), shape + (millions of applications, mixed inputs, filing years), risk - (censored newest years, examiner fields of the last action, heavy joins).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates, round 2 (wide tables outside biology and medicine, tables with 2M+ rows).
