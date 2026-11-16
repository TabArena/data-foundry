---
unique_name: fannie_mae_single_family_loan_performance
name: Fannie Mae Single-Family Loan Performance Data
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Company
year: '2013'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://capitalmarkets.fanniemae.com/credit-risk-transfer/single-family-credit-risk-transfer/fannie-mae-single-family-loan-performance-data
- https://www.fanniemae.com/loanperformance
- https://capitalmarkets.fanniemae.com/media/9066/display
- https://capitalmarkets.fanniemae.com/credit-risk-transfer/single-family-credit-risk-transfer/fannie-mae-release-actual-loss-single-family-loan-performance-data
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: Fannie Mae's loan-level origination and monthly performance release since 2000 holds the same loan-period status panel as `mortgage`, at a far larger scale; the label is ours to build from the status and zero-balance fields.
- Source: Fannie Mae, Single-Family Loan Performance Data, first released 2013-04-30: "loans acquired between January 1, 2000 and March 31, 2012" with "monthly performance data as of December 31, 2012", "a subset of Fannie Mae's 30-year, fully amortizing, full documentation, single-family, conventional fixed-rate mortgages", an "Acquisition file" (origination and delivery) and a "Performance" file (monthly) per acquisition quarter (Orrick InfoBytes, 2013-05-06, https://infobytes.orrick.com/2013-05-06/fannie-mae-releases-loan-performance-data/); "over 18 million" loans at that release (Fannie Mae's press release as quoted by a search result; the page itself answers 403). Updated quarterly since, plus an actual-loss release (the fourth link). The current rows (loan-months), columns and file layout were not read: every Fannie Mae page (capitalmarkets.fanniemae.com, fanniemae.com) answers 403 to automated fetches here. Access: registration (the run's note; not checked).
- Use case: a mortgage holder or a credit-risk-transfer investor scoring each active loan each period for default or prepayment (loss reserves, pricing of the risk-sharing deals); fit direct, the use case of `mortgage` (a holder's periodic PD scoring), but Fannie Mae's own purpose statement could not be read (403). Regime temporal by reporting period (as `mortgage`: the last periods as test), the loan as group inside (SPLIT-13).
- Siblings and duplicates: `mortgage` (`Yes`, DF: Yes, BeyondArena; Baesens et al.'s 621,653 loan-quarters 2000-2015 from a consultancy whose site is gone): another source of the same task, so not a duplicate (PROV-4), and the curator decides whether one replaces the other; `freddie_mac_single_family_lgd` and `freddie_mac_single_family_default` (Freddie Mac's loan-level release: another publisher and other tasks, LGD at default and default at origination; the latter lists this release as an alternative); `lgd` (`No`); `hmda_mortgage_application_decision`, `hmda_mortgage_denial` (application decisions, another task). External collections: none found.
- Better data: found as better data for `freddie_mac_single_family_lgd`, `mortgage`; no further search this round.
- Papers and pages: the release pages linked above (403 here); papers that used the data not searched (the session's web search budget ran out).
- Metric: none found (no competition; Fannie Mae publishes data, not a task), so the fallback `log_loss` over default / payoff / active, as `mortgage` declares (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the target is our construction (the next period's status from the delinquency status and the zero-balance codes; the default definition and horizon, as on `mortgage`) (USE-5); the size calls for a sample of whole loans or vintages; loans whose outcome is not yet known at the cutoff (SPLIT-9, SPLIT-10); fields recorded at or after the event (zero-balance date and amounts, foreclosure and disposition dates, loss fields) must go (LEAK); the period's own balance records the event, so lag it as `mortgage` does; the terms of use are a note, not a criterion (EV-4).
- Priority: gap + (multiclass thin), use case 0 (the purpose statement could not be read), source + (Fannie Mae's documented release), shape + (millions of loans, monthly, temporal), risk - (a label of our own construction, a large panel to cut).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `freddie_mac_single_family_lgd`, `mortgage`.
- as published: loan-level origination data plus monthly performance for a subset of Fannie Mae's fully amortizing, full-documentation, conventional fixed-rate single-family mortgages of 30 years or less, acquired ...; target: per active loan and period, the next status: default (serious delinquency or a credit-event zero balance code), payoff (prepaid) or still active, the three ...; access: registration.
- Why: mortgage is the Baesens textbook panel (621,653 loan-quarters, 2000 Q2-2015 Q1, from a consultancy whose site is gone; its assessment says 'No larger source exists'), with origination FICO/LTV/rate and the previous quarter's balance and LTV as features. Fannie Mae's file has the same loan-period panel and the same ...
- Adds: Millions of loans instead of a textbook sample, 26 years (to 2026, through the 2008 crisis and the 2020 forbearance period), monthly periods, a delinquency field the old file lacks, and official documentation. A different source from the already recorded Freddie Mac loan-level dataset. Terms: registration on Data ...

**Assessment (AI, 2026-11-08):** size check for the large-datasets review: one row per loan with a default label over a fixed horizon gives 55,729,394 loans originated 1999-2023 (labels mature by the March 2026 cutoff) x 23 origination inputs; the call stands at priority 4 under the record's loan-period framing, 3 under a per-loan default framing.
- As published: Fannie Mae's primary dataset, one pipe-delimited CSV per acquisition quarter, origination and monthly performance in one file since the October 2020 release (FAQ of 2022-03-08, Q11, https://capitalmarkets.fanniemae.com/sites/g/files/koqyhd216/files/2022-03/sf-loan-performance-dataset-faqs.pdf), 108 columns per loan-month (from a third-party import guide, https://farahat-analytics.github.io/case-mortgage-analytics/data_raw.html; Fannie Mae's file layout answers 403 here). The Statistical Summary Tables of July 2026 (https://capitalmarkets.fanniemae.com/media/20926/display, read through the Wayback copy of 2026-10-11) count 57,864,281 loans acquired from January 2000 to March 2026, by origination year from 160,137 (1999) and 962,090 (2023) up to 5,107,633 (2003) and 4,991,580 (2020). The summary gives serious delinquency (D180) only as a share of origination UPB. Fannie Mae states no loan-month count; the same third-party guide gives "approximately 2.5 billion records" for the July 2023 release (about 55 million loans). First release 2013-04-30 (FAQ Q10: acquisitions 2000-01-01 to 2012-03-31, performance to 2012-12-31). A separate HARP dataset holds about one million refinanced loans with a mapping key. The purpose statement, now read on the archived data page (2026-07-22): the data is provided "to help investors analyze the credit and prepayment performance of loans owned or guaranteed by Fannie Mae".
- The task's table: one row per loan at acquisition, the label built from the performance rows (for example D90 or D180, or a credit-event zero-balance code, within 24 months). Rows: 57,864,281 loans in all, 55,729,394 originated 1999-2023 (computed from the summary's per-year counts; those loans have 24 months of performance by March 2026). Inputs: the third-party list names 26 static fields; without the origination and first-payment dates (kept for the split) and the constant amortization type, 23 remain (channel, seller, rate, UPB, term, LTV, CLTV, number of borrowers, DTI, borrower and co-borrower credit scores, first-time buyer, purpose, property type, units, occupancy, state, MSA, 3-digit zip, MI percentage and type, special eligibility program, relocation flag). The UPB that ever reached D180 is 2.49% of the 1999-2023 origination UPB (computed from the summary, page 2), 13.6% for the 2007 vintage and 1.2% for 2020: a rare positive class with a strong vintage drift. Under the record's own framing (the `mortgage` loan-period panel, the next period's status) the table is the loan-months, about 2.5 billion in 2023, and needs a sample of whole loans.
- Access: free registration on Data Dynamics and acceptance of the terms; "the Data is licensed by Fannie Mae for internal use only" and may not be redistributed without written consent (FAQ Q6), so only a definition built from each user's own download could ship (a note, EV-4). One-click download of all files; single-file downloads are capped at 100 files per hour. Fannie Mae states no total size; a third-party post gives 48.2 GB for the 2000Q1-2023Q2 archive (not opened). Every capitalmarkets.fanniemae.com page and file answers 403 to this machine; the Wayback copies were readable.
- Changes the call: Freddie Mac's release (`freddie_mac_single_family_default`) holds the same task on the other agency's loans, a disjoint population: a second source, so no duplicate (PROV-4); PROV-7 does not apply, since it covers one source with distinct tasks. Neither is better data for the other: 57,864,281 loans acquired 2000 to March 2026 here, about 49.51 million Standard loans originated 1999 to June 2026 there, with origination fields of the same kind. Fannie Mae has 17% more loans and a co-borrower score; Freddie Mac has one more quarter, readable documents, an official random sample of 50,000 loans per vintage, and Relief Refinance loans that Fannie Mae's primary dataset excludes. The curator takes one per framing, as for `ppnn_ecmwf_t2m_postprocessing_germany` against `bias_correction_r_bias_correction_r_2`: one of the two at origination, or Fannie Mae as the periodic panel of `mortgage`'s task and Freddie Mac at origination, which gives two distinct tasks. The use case is now read (the publisher names investors and the analysis of credit and prepayment performance): use case +. The 2026-10-31 factors (gap +, use case 0, source +, shape +, risk -) summed to 3, not the 4 written; with use case + they give 4 under the panel framing (multiclass gap +) and 3 under a per-loan binary framing (no gap). Priority kept at 4.
- Not checked: the 108-column layout and the current loan-month count from Fannie Mae's own files (403); the download size; the default definition and horizon a build would use.

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

CC (2026-11-08, Lennart): framed as the loan-month panel (next month's status), while freddie_mac_single_family_default ships the per-loan task at origination; two distinct tasks on the two agencies' disjoint loans. Open: the shipped `mortgage` (the panel task, 50,000 loans) is to be decided against this one (keep both, or `mortgage` to 2nd Tier as with thailand_road_accident_fatalities_2015).

**Assessment (AI, 2026-11-09):** not built in the large-datasets run of 2026-11-08: Fannie Mae's Data Dynamics needs a free account, which this machine cannot pass. A person has to download the raw files; the build follows in a later round.

CC (2026-11-09, Lennart): later; make this its own task with a human in the loop (the data needs a person to fetch it).
