---
unique_name: fsa_foreign_gifts_and_contracts
name: Foreign Gift and Contract
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
domain: education
original_data_state: One Table
source_links:
- https://studentaid.gov/data-center/school/foreign-gifts
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/foreign-gift-and-contract
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the STRABLE release and a preview of its files; a human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the Department of Education's register of foreign gifts and contracts that US colleges report under Section 117 of the Higher Education Act (a source reaching $250,000 in a calendar year); a large, dated register in a thin domain, but the amount of a reported gift is a disclosure no named decision predicts.
- Source: U.S. Department of Education, Section 117 foreign gift and contract data (https://studentaid.gov/data-center/school/foreign-gifts); ED publishes biannual spreadsheets of all institutionally reported foreign gifts and contracts since the section's enactment in 1986 (CRS In Focus IF12927, updated 2026-03-25). As read by STRABLE (Sec117PublicRecordsCompleteFeb2025.xlsx): one row per reported gift or contract with OPEID, school, state, transaction type (gift, contract, restricted contract and others), foreign-government source, attribution country, amount, receipt date, contract start and end dates, restricted-transaction government and description, foreign-ownership fields and a Legacy flag. STRABLE subsampled to 75,000 rows (497 institutions in the sample) x 18 columns, target Amount under a signed log; negative amounts occur.
- Use case: none named: the register is a public disclosure and the basis of ED's compliance work; a reviewer estimating what an institution should have reported is the nearest use, approximate. Regime: temporal (receipt and contract dates over decades).
- Siblings and duplicates: `fsa_cohort_default_rate` and `fsa_gainful_employment` (other FSA files); no other Section 117 record (searched section 117, foreign gift). External collections: STRABLE ("Foreign Gift and Contract", App. C.2: "to predict the gift value").
- Better data: a candidate of the benchmark STRABLE (the run searched no further).
- Papers and pages: CRS In Focus IF12927, "Section 117 of the Higher Education Act: Reporting of Foreign Gifts and Contracts"; STRABLE (arXiv 2605.12292, App. C.2 and D.1).
- Metric: none found (ED's page defines no prediction task), so the fallback `rmse` on a log amount; STRABLE scores R^2 (App. D.1) (MET-1).
- Risks for /add-dataset: what a row is (one transaction, or a source's total for a year) and the negative amounts (corrections) are to check; Legacy rows may follow an older reporting format; the free-text description may state amounts (LEAK); the full row count (above 75,000) is to count; the receipt date is missing on 45% of the sample.
- Priority: gap + (education), use case 0, source + (ED's register, documented by CRS), shape + (over 75,000 reports, mixed types, dated), risk - (no decision fits the target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 75,000 rows x 18 columns incl. target (STRABLE parquet); capped at 75,000 by STRABLE; target: Amount.
- Why: Predict the value of a foreign gift or contract reported by a US college (Section 117)
- Notes: Raw file Sec117PublicRecordsCompleteFeb2025.xlsx. Subsampled by STRABLE to 75,000 rows.
