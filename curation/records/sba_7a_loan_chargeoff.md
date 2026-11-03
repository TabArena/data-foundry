---
unique_name: sba_7a_loan_chargeoff
name: SBA 7(a) & 504 FOIA loan data (loan-level approvals with paid-in-full / charge-off outcome)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://data.sba.gov/dataset/7a-504-foia
- https://catalog.data.gov/dataset/sba-7a-and-504-loan-data-reports
- https://data.sba.gov/sites/default/files/uploaded_resources/7a_504_foia_data_dictionary.xlsx
- https://www.tandfonline.com/doi/full/10.1080/10691898.2018.1434342
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the SBA's loan-level FOIA files of every 7(a) and 504 loan approved since FY1991, with the charge-off or paid-in-full outcome and its date; a real approval-time default task once the label is built at a fixed horizon.
- Source: U.S. Small Business Administration, "7(a) & 504 FOIA" (data.sba.gov, issued 2021-03-09, updated quarterly, files "as of September 30, 2026", licence "U.S. Government Works"): four 7(a) files by decade (FY1991-FY1999 to FY2020-present) and two 504 files, one row per loan. The data dictionary (read 2026-10-31) defines the approval fields (GrossApproval, SBAGuaranteedApproval, ApprovalDate, InitialInterestRate, FixedorVariableInterestInd, TermInMonths, NaicsCode, FranchiseCode, BusinessType, BusinessAge, ProcessingMethod, JobsSupported, CollateralInd, lender and project location) and the outcome: LoanStatus "CANCLD = Cancelled", "CHGOFF = Charged Off", "COMMIT = Undisbursed", "EXEMPT = The status of loans that have been disbursed but have not been cancelled, paid in full, or charged off are exempt from disclosure under FOIA Exemption 4", "PIF = Paid In Full", with PaidInFullDate, ChargeOffDate and GrossChargeOffAmount. Rows not counted. A teaching cut of an earlier release, Li, Mickel & Taylor 2018, J. Stat. Educ. 26(1):55-66, "Should This Loan be Approved or Denied?", holds "historical data from 1987 through 2014 (899,164 observations) with 27 variables" (quoted from its copy on OpenML, 43539, which is a 2,102-row California subset).
- Use case: the lender, with SBA as guarantor, decides at approval whether to grant or how to price a guaranteed small-business loan; the JSE paper's title frames this decision. Fit direct with the approval fields only. Regime temporal by approval date.
- Siblings and duplicates: no record of the SBA files or the JSE cut (grep: SBA, 7(a), SBAnational, Mickel, 43539). `zimnat_loan_default_predictio` (`TBD -> Yes`, a Zimbabwean lender's snapshot), `lending_club` and the Freddie Mac and Fannie Mae records are other lenders and populations. External collections: OpenML 43539 (the teaching subset); others not checked.
- Better data: found as a related task next to `zimnat_loan_default_predictio` (the data-scouting run of 2026-10-30/31); no further search.
- Papers and pages: the data.sba.gov page and data dictionary; Li, Mickel & Taylor 2018 (not read: HTTP 403).
- Metric: none found (SBA publishes no task, and the JSE paper could not be read), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the outcome of running loans is withheld (EXEMPT), and a status at the file date is a shared window (SEL-6), so build "charged off within N years of approval" from ChargeOffDate on vintages approved at least N years before AsOfDate. Drop the outcome columns and the fields set after approval: FirstDisbursementDate, SoldSecMrktInd ("a static field once it is sold") and BankName ("the bank that the loan is currently assigned to") (LEAK). Drop BorrName and BorrStreet (personal data of sole proprietors). 7(a) and 504 differ in columns (ship 7(a), or two datasets). JobsSupported is "self-reported" by the lender. The size calls for a sample by vintage.
- Priority: gap 0 (finance, binary and temporal are not thin), use case + (the approval decision, framed by the JSE paper), source + (SBA with a data dictionary), shape + (likely over a million loans, mixed types, 35 years of vintages), risk - (a label to build under censoring; post-approval columns).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `zimnat_loan_default_predictio`.
- as published: loans; 7(a) loans approved FY1991-present in four decade files (FY2010-FY2019 file 255 MB) plus 504 loans in two files; 42 columns; derived teaching version (Li, Mickel & Taylor 2018, J. Stat. ...; target: LoanStatus charged off (CHGOFF) vs paid in full (P I F), with ChargeOffDate and GrossChargeOffAmount (a loss severity per charged-off loan); access: open.
- Why: same domain and decision as the Zimnat loan-default task (predict which loans will not be repaid), with the outcome dated and the features fixed at approval; a strong public source with a predictive target a lender acts on, over 30 years of vintages, so a temporal split by approval date is natural
- Adds: orders of magnitude more loans than Zimnat's ~12,000, dated approvals and outcomes (no snapshot label), public domain (U.S. Government Works), documented columns; a different borrower population (US small businesses), hence related rather than better. Notes: loans still running (status EXEMPT/COMMIT/CURR) must be ...
