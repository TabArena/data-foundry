---
unique_name: bwin_early_high_risk_gambler_detection
name: Using Cross-game Behavioral Markers for Early Identification of High-risk Internet Gamblers (bwin.party, Transparency Project)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
year: '2013'
domain: social science
problem_type: Binary Classification
source_links:
- http://www.thetransparencyproject.org/download_index
- https://doi.org/10.1037/a0032818
- http://www.thetransparencyproject.org/codebooks/CodeBook_for%20Braverman_LaPlante_PAB_2013.pdf
- https://doi.org/10.1037/a0028545
- https://www.openml.org/d/45717
- https://arxiv.org/abs/2505.17451
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 4,056 bwin.party subscribers with about 100 aggregates of their betting in the 31 days after the first deposit, target whether they triggered the operator's Responsible Gambling programme, published by the Division on Addiction for the early identification of high-risk gamblers; a 50:50 case-control sample whose outcome is counted over one calendar year.
- Source: Braverman, LaPlante, Nelson and Shaffer 2013, "Using Cross-game Behavioral Markers for Early Identification of High-risk Internet Gamblers", Psychology of Addictive Behaviors (doi 10.1037/a0032818); data and codebook on the Transparency Project (Division on Addiction, Cambridge Health Alliance, a Harvard Medical School teaching affiliate; sponsor bwin Interactive Entertainment AG). As published (codebook and the analytic file's header read 2026-10-31): the analytic dataset, 4,056 rows (USERID, age, gender, RG_case, ValidationSet, first-active dates per product, sums, active days, standard deviations and averages of stakes and bets per product over 31 days, weekly, weekend and weekday splits) as text, SAS and SPSS files, plus raw tables: demographics (4,134 subscribers), daily aggregates (981,782 rows, 2000-05-01 to 2010-11-10) and RG details (2,068 cases).
- Use case: the operator, a month after a new subscriber's first deposit, decides whether to flag the account for an early responsible-gambling intervention ("behavioral markers that operators can use to predict the development of gambling-related problems among their subscribers", the study's description); fit approximate: the codebook defines cases as the subscribers "who triggered a responsible gambling intervention between November 2008 and November 2009" and controls as those with a first deposit "on the same day as an RG case" who did not, while first deposits run from 2000-05-08 to 2009-11-27, so the time from the first month to the outcome varies by years (SEL-6, see the risks); the classes are 50:50 by design (one class oversampled, no `Selection Bias` marker by that alone); regime temporal by first deposit date with the matched pairs kept together, or IID; the authors' `ValidationSet` is their holdout (SPLIT-5).
- Siblings and duplicates: no record of this study (grep bwin, transparency, gambl). OpenML 45717 `bwin_amlb` and 45711 `doa_bwin` (530 rows, 14 features) come from another bwin cohort of the same research programme (live-action betting over 24 months from February 2005, account closure; no record): a sibling study, not a duplicate (PROV-4). External collections: CLIMB (arXiv 2505.17451) per the Zotero item (which bwin set it carries was not checked).
- Better data: from the curator's Zotero collection (item 1); no further search this round.
- Papers and pages: Braverman et al. 2013 (a CHAID tree on one half, confirmed on the independent validation half; two subgroups in which 90% are RG cases); Gray, LaPlante and Shaffer 2012 (doi 10.1037/a0028545) on the behaviour of subscribers who trigger RG interventions.
- Metric: none ranked: the study reports subgroups of a CHAID tree in which "90% of the members were identified by bwin.party's RG program" (the Transparency Project's summary; the paper's full text not read), with no threshold or cost for a score; so the fallback `roc_auc`, which the 50:50 design does not distort; inputs none.
- Risks for /add-dataset: SEL-6: the label counts one shared calendar year, not a fixed horizon after the first month; restrict the rows to first deposits shortly before or within the window (the first-active dates allow it) or argue the case, before anything else; the codebook says year of birth, country, language and registration date are missing for 167 subscribers, "all controls" (`age` ships in the analytic file), and 21 controls have no betting data, so missingness gives the class away (LEAK-13, `Class-dependent Recording`): drop the column or the rows; the label mixes RG event types (third-party block requests, closures, deposit-limit changes, complaints; Appendix 2); `ValidationSet` and `USERID` are no features.
- Priority: gap + (no gambling task; social science is thin), use case 0 (approximate), source +, shape + (4,056 subscribers, about 100 features), risk - (the SEL-6 window, class-dependent missingness).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 1: "CLIMB: Class-imbalanced Learning Benchmark on Tabular Data".
- as published: Subscribers: analytic dataset 4,056 rows (from 2,068 RG cases + 2,066 controls with the same first-deposit date; minors and subscribers without first-month betting removed). Columns: first-31-day ...; target: RG_case: the subscriber triggered bwin.party's Responsible Gambling program (binary, case vs control); access: open.
- Why: Real operator data, published for exactly this early-detection task with the authors' own validation split. All features are first-31-day aggregates, so they are known at the prediction point.
- Adds: A gambling-harm domain we lack, with 7.6 times the rows of bwin_amlb (OpenML 45717/45711; 530 account closers; no record). Caveats: a 50:50 case-control sample, so the base rate is not real (selection by design); the RG trigger can come years after the first month. The Gray et al. 2012 package (very likely the same ...
