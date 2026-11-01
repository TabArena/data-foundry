---
unique_name: hmda_mortgage_denial
name: 'HMDA public loan-level data (CFPB/FFIEC): mortgage application denied or approved'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://ffiec.cfpb.gov/data-publication/
- https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields
- https://vincentarelbundock.github.io/Rdatasets/doc/AER/HMDA.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the same FFIEC/CFPB public HMDA loan/application register and the same target, `action_taken` "3 - Application denied" against originated or approved, as `hmda_mortgage_application_decision` (screened `TBD -> Yes`, priority 2, in this run), which keeps the task.
- Source: both records link "Public HMDA - LAR Data Fields" (https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields): `action_taken`, "The action taken on the covered loan or application", 1 originated, 2 approved but not accepted, 3 denied, 4 withdrawn, 5 closed for incompleteness, 6 purchased, 7 and 8 preapproval requests. This record's https://ffiec.cfpb.gov/data-publication/ is the parent page of the other record's Snapshot National Loan-Level Dataset link.
- Siblings and duplicates: `hmda_mortgage_application_decision` names this record as the same data ("one of the two is a `Duplicate` (PROV-4)"), and its risks already hold this record's notes (post-decision pricing fields, denial reasons and purchaser type to drop; race, ethnicity, sex and age as an ethics call for the curator). The third link, Rdatasets AER `HMDA`, is another dataset: the Boston Fed's study of 1990 Boston applications, 2,380 rows x 14 variables (Munnell, Tootell, Browne, McEneaney, "Mortgage Lending in Boston: Interpreting HMDA Data", AER 86:25-53, 1996; Stock and Watson's textbook data); it has no record of its own and is related work here (PROV-12).
- Better data: from the curator's Zotero collection (item 131, the Rdatasets index); no search for better data in this run.
- The task stays a candidate under `hmda_mortgage_application_decision`.
- Reject check (AI, 2026-10-31): stands. Both records link 'Public HMDA - LAR Data Fields' (https://ffiec.cfpb.gov/documentation/publications/loan-level-datasets/lar-data-fields) and take action_taken, denied against approved, as the target. This record's https://ffiec.cfpb.gov/data-publication/ is the parent page of the other record's Snapshot link, and its leak and ethics notes are already in hmda_mortgage_application_decision's risks. The Rdatasets AER HMDA link is another dataset with no record (Boston Fed, 2,380 applications of 1990, Munnell et al., AER 1996; it has credit history, which the public LAR lacks): name it in the survivor's comments so the curator can decide whether it gets a record.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 131: "vincentarelbundock.github.io/Rdatasets/datasets.html".
- as published: One row per mortgage application, about 99 columns (loan type, purpose, amount, term, property value, CLTV and DTI bands, income, applicant age band, race, ethnicity, sex, census tract and tract ...; target: action_taken: application denied vs approved/originated; access: open.
- Why: The public, maintained, far larger version of the classic Boston HMDA lending task, with real lender decisions on every US application.
- Adds: Millions of rows per year over many years, mixed types. Caveats: post-decision fields (interest_rate, rate_spread, total_loan_costs, denial_reason, purchaser_type) leak and must go; race, ethnicity, sex and age are protected attributes, so the curator needs an ethics call (SEL-1: drop them as features or argue a ...
