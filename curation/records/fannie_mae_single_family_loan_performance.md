---
unique_name: fannie_mae_single_family_loan_performance
name: Fannie Mae Single-Family Loan Performance Data
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
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
needs_review:
- ai_unverified
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
