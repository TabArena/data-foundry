---
unique_name: ibrd_loans_historical_snapshots
name: IBRD Statement Of Loans and Guarantees - Historical Data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: GOV Website
domain: finance
required_split:
- Temporal (NON-IID)
original_data_state: One Table
source_links:
- https://financesone.worldbank.org/ibrd-statement-of-loans-and-guarantees-historical-data/DS00975
- https://financesone.worldbank.org/ibrd-statement-of-loans-and-guarantees-latest-available-snapshot/DS00047
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the World Bank's monthly snapshots of every IBRD loan and guarantee since April 2011, the history behind `loan_ibrd`; real and maintained, but no target is defined yet, and the curator decides which version enters.
- Source: World Bank Group, Finances One, "IBRD Statement Of Loans and Guarantees - Historical Data" (DS00975): "This dataset contains historical snapshots of the Statement of Loans including the latest available snapshots"; 1,585,498 rows x 35 columns, "Monthly historical snapshot from April 2011 onward, covering all Loans and Guarantees provided since inception"; data as of 2026-09-30, updated monthly, CC BY 4.0, the bulk file over 300 MB (the page recommends the API). The latest snapshot alone (DS00047) has 9,538 rows x 35 columns, with loan types NPL, CPL, SCPD, SCPM, SCPY, SCL, FSL, BLNR, GURB, BLNC, GUBF. The column list was not shown on the pages read; it is the latest snapshot's, which `loan_ibrd` holds (region, country, borrower, guarantor, loan type and status, interest rate, amounts committed, cancelled, disbursed, repaid and due, and the approval, signing, effective, closing and repayment dates).
- Use case: none named: the statement is published for transparency of IBRD lending. The run's framing (treasury staff or a borrower's debt office assessing an active loan at a reporting date: its status later on, the share cancelled by closing) is ours, so fit approximate. Regime temporal on the snapshot date (`end_of_period`), one row per loan at a prediction date.
- Siblings and duplicates: `loan_ibrd` (`TBD -> Yes` by Lennart, `Needs extensive data wrangling`; its notes: "Check if we can get newer version of data from source, yes we can and should take the newest data!", "Unsure if this is a reasonable task or not"; copies in TabSTAR and STRABLE): the same source and columns, this record a newer and longer release (PROV-6, a version: the curator decides which one enters). `worldbank_ida_statement_of_credits` (a candidate of this run, STRABLE) is the sibling statement of IDA, another lending arm; the other World Bank finance records (trust funds, FIFs, procurement) are other tables of the same publisher. External collections: the latest snapshot is in TabSTAR and STRABLE, as `loan_ibrd`.
- Better data: found as better data for `loan_ibrd` (a newer release of the same source, PROV-6); no further search this round.
- Papers and pages: the two Finances One dataset pages; STRABLE (arXiv 2605.12292) and TabSTAR use the latest snapshot.
- Metric: none found (the Finances One pages define no task), so the fallback for whichever target the curator picks (MET-8). Inputs none.
- Risks for /add-dataset: the target is ours to define (`No Good Target (yet)`): a loan's status at a later snapshot or its cancelled share at closing, each with a horizon and only loans whose outcome has matured (SPLIT-9, SPLIT-10); amounts and statuses after the prediction date leak (LEAK); a per-loan panel can drift into forecasting a series, so the framing must pass SEL-11 and TP-10; the loan type that the static copies predict is fixed at approval and may follow from the approval date (the product menu changed over time; TP-4 to probe); about 186 snapshots of the same loans, reduced to one row per loan.
- Priority: gap 0 (finance not thin), use case 0 (no decision named), source + (World Bank, documented and maintained), shape + (9,538 loans over about 186 monthly snapshots, mixed columns, a time axis), risk - (no target yet).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `loan_ibrd`.
- as published: 1,585,498 rows x 35 columns: monthly snapshots of every IBRD loan and guarantee since inception, from April 2011 to September 2026; target: the record's target (Loan_Type) is still there; the snapshots add targets that change over time, e.g. a loan's status at a later snapshot or the share of the ...; access: open.
- Why: the same source and columns as loan_ibrd, which is one latest snapshot; the curator's note asks for the newest data from the source
- Adds: a time axis: about 186 monthly snapshots instead of one, so a temporal split and a target defined after the prediction date become possible, which answers the record's doubts ('unsure if this is a reasonable task', no time structure); CC BY 4.0
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
