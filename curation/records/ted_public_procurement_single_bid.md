---
unique_name: ted_public_procurement_single_bid
name: 'TED (Tenders Electronic Daily) CSV: EU public procurement contract notices and award notices'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://data.europa.eu/data/datasets/ted-csv
- https://www.openml.org/d/42163
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the European Commission's open TED CSV export of EU procurement notices (2006-2023), large and documented; single bidding at the call is the run's framing of a target the data supports, not a task the source names, and the build needs the award-to-call join and the removal of post-award columns.
- Source: European Commission, DG GROW, "Tenders Electronic Daily (TED) (csv subset) – public procurement notices", data.europa.eu (portal API: issued 2015-07-27, modified 2024-01-25): "A subset of Tenders Electronic Daily (TED) data covering public procurement for the European Union and beyond from 2006-01-01 to 2023-12-31 in comma separated value (CSV) format. This data includes the most important fields from the contract notice and contract award notice standard forms, such as who bought what from whom, for how much, and which procedure and award criteria were used." 48 distributions: yearly contract-notice (CN) and contract-award-notice (CAN) files 2006-2023, older exports marked deprecated, a VEAT file; documentation pages "TED CSV Open Data - Notes and Codebook" (no URL in the API) and "Advanced notes on methodology - Version 0.92". The portal notes the switch to eForms on 14 November 2022. OpenML 42163 (`public_procurement` v6, uploaded 2019, the CAN file of 2015) is a copy of one year: 565,163 rows x 75 columns, default target `award_value_euro`; `number_offers` is filled on 460,651 rows (OpenML feature list).
- Use case (written by the curation; the source names no prediction): a contracting authority or a procurement oversight body, when a call for tenders is published, estimates whether it will receive only one offer (single bidding, a common indicator of weak competition), to redesign the tender or to target an audit; target `number_offers` == 1 of the award, features from the call (CPV code, contract type, procedure type `top_type`, award criteria, authority type and main activity, country, estimated value, lots, framework agreement, EU funds). Fit approximate (our framing). Regime temporal (dispatch dates over 2006-2023).
- Siblings and duplicates: no record of TED or OpenML 42163 (grep for procurement, TED, 42163); the World Bank procurement records (`worldbank_corporate_procurement_contracts`, `worldbank_ipf_contract_awards`) are another source and task (PROV-7). External collections: OpenML 42163; the bmdal_reg download script (Holzmüller et al.) lists 42163 only in a commented-out line with `award_value_euro` (moved here from the links, PROV-12: https://github.com/dholzmueller/bmdal_reg/blob/08c28e131d9dc49cf1e47ddb80f7230ca4e10d72/bmdal_reg/download_data.py).
- Better data: from the curator's Zotero collection (item 102); no further search this round.
- Papers and pages: no paper on single-bid prediction from TED was read (this session's web search budget ran out); the procurement-integrity literature that uses TED single bidding was not checked.
- Metric: none found (portal page and API, OpenML page); so the fallback `roc_auc`. Inputs none.
- Risks for /add-dataset: the target and use case are ours (SEL-3 and USE-1 to settle with a paper if one exists); post-award columns leak (winner fields, award values, `number_tenders_*`, `number_offers_electr`, `b_contractor_sme`, `dt_award`, `b_subcontracted`; LEAK-10), and OpenML's `award_value_euro` leaks through `value_euro`, `award_est_value_euro` and `award_value_euro_fin_1` (assessment); the unit (award, lot or notice; several awards per notice) and the CAN-to-CN join (`id_notice_cn`) for call-time fields; cancelled and corrected notices; the eForms change in late 2022; about 18% of awards without `number_offers`; size (millions of awards over 18 years, a cap).
- Priority: gap 0 (no domain value fits; binary and temporal are covered), use case 0 (written by the curation), source + (DG GROW, codebook and methodology notes), shape + (hundreds of thousands of awards per year, mixed types, dates), risk - (our own target, joins, post-award leaks).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 102: "bmdal_reg/bmdal_reg/download_data.py at 08c28e131d9dc49cf1e47ddb80f7230ca4e10d72 · ...".
- as published: OpenML 42163 (public_procurement v6, TED contract award notices 2015) has 565,163 rows x 75 columns. The portal has yearly contract-notice and award-notice CSVs for 2006-2023 (last modified ...; target: Single bidding: the awarded contract or lot received one offer (number_offers == 1, binary). Alternative: award_value_euro, OpenML's default target.; access: open.
- Why: Real administrative data from the EU's official procurement journal: open, maintained, large, with high-cardinality strings.
- Adds: A public-procurement domain no record covers, and a far larger and newer release than OpenML 42163, which has no record either. Caveats: OpenML's award_value_euro target leaks through value_euro, award_est_value_euro and award_value_euro_fin_1. For a notice-time task, outcome columns (winner, number of offers, SME ...
