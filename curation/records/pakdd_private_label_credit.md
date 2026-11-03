---
unique_name: pakdd_private_label_credit
name: PAKDD 2009/2010 credit risk on a Brazilian private-label credit card
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Website
domain: finance
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/JLZml/Credit-Scoring-Data-Sets/tree/master/2.%20PAKDD%202009%20Data%20Mining%20Competition
- http://web.archive.org/web/20170930175832/http://sede.neurotech.com.br:80/PAKDD2009/
- http://web.archive.org/web/20180208103708/http://sede.neurotech.com.br:80/PAKDD2010/
- https://pakdd.org/archive/pakdd2009/front/show/competition.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: PAKDD 2010's labelled modelling set, about 50,000 private-label credit card clients of a Brazilian credit company captured in 2006 with a 60-day delinquency label (26% bad), from NeuroTech's competition; a real application-scoring task with a competition metric, but only the modelling year has public labels and the 2009 release was not found.
- Source: the PAKDD 2009 and 2010 data mining competitions, co-organised by NeuroTech Ltd. and the Center for Informatics of the Federal University of Pernambuco (sites on the Wayback Machine). 2009, "Credit Risk Assessment on a Private Label Credit Card Application": data "from the private label credit card operation of a major Brazilian retail chain, along stable inflation condition (2003-2008)", a labelled modelling set of one year and unlabelled leaderboard and prediction sets one and three years later. 2010, "Re-Calibration of a Credit Risk Assessment System Based on Biased Data" (Problem characterization): "The competition labeled data set available for modeling comprises the companies' clients who have been captured during one year (2006) and the test data set comprises applicants who have been captured during one year (2008)"; the prediction set holds rejected applicants who were granted credit anyway; "The delinquency of the modeling data set is 26% according to 60 days delay in any payment of the bills contracted along the first year after the credit has been granted". The mirror (github.com/JLZml/Credit-Scoring-Data-Sets, 2019; its folder says 2009) holds only `PAKDD 2010.zip`: `PAKDD2010_Modeling_Data.txt` (tab-separated, no header, 54 fields ending in the label; 8.4 MB, about 50,000 rows by its size, not counted; previewed), the leaderboard and prediction sets, and `PAKDD2010_VariablesList.XLS`.
- Use case: the card issuer scores an applicant at application time to grant or refuse credit (2009: "The offer of credit for potential clients"; 2010: a "binary decision support system" whose score is thresholded); fit direct on approved clients, since only granted credit has a repayment outcome (no `Selection Bias` marker, selection.md, "Selection bias"). Regime IID within the 2006 modelling year when no application date ships (none seen in the preview; SPLIT-7 if one turns up); the competition's drift design needs the later sets' labels, not found.
- Siblings and duplicates: no other PAKDD or NeuroTech record (grep: pakdd, neurotech, private label); the credit-scoring siblings `credit_g`, `sbtic_xente_credit_scoring_challenge` and `sfc_paygo_solar_credit_repayment_competition` are other lenders. External collections: none found.
- Better data: from the curator's Zotero collection, item 87; no new search this run.
- Papers and pages: the archived 2009 overview and the 2010 overview, Problem characterization and Evaluation and Awards pages; the pakdd.org archive page was not read.
- Metric: ROC AUC, the official metric of both competitions (2010, Evaluation and Awards: "Entries will be ranked in terms of the Area Under the Receiver Operating Characteristic Curve (ROC_AUC)", max KS as the tie-break; 2009: "The official performance metrics will be the area under the ROC curve"), so `roc_auc` (MET-4); inputs none.
- Risks for /add-dataset: only the modelling set is labelled in the mirror (check whether NeuroTech released the leaderboard or prediction labels; without them the temporal design is lost, SPLIT-5); the 2009 retail-chain release is a separate dataset not found online; name the 54 fields from the variables list (CLEAN-12) and check the id and the free-text city and district fields; provenance through a third-party mirror (PROV-8, PROV-15). The record's `year` is left empty until the curator picks the release (2010 is the one available).
- Priority: gap 0 (finance and binary are not thin), use case + (the organiser names the issuer's credit decision), source + (competition pages with problem, label and metric definitions), shape + (about 50,000 rows, 53 mixed-type features), risk - (later-year labels missing, 2009 data not found, mirror-only access).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 87: "JLZml/Credit-Scoring-Data-Sets".
- as published: one row per credit-card application; 2009: retail chain, 2003-2008; 2010: credit company and partner shops, 2006-2009; labelled modelling set of one year, unlabelled leaderboard and prediction sets ...; target: bad payer (default) on the private-label card; access: open.
- Why: Real application scoring with a temporal shift, from the issuer's own data.
- Adds: Credit application scoring from Brazil with a drift task. Caveats: the original sites are dead, so provenance runs through Wayback pages and mirrors; the later sets may lack labels; the repo folder for 2009 holds the 2010 zip.
