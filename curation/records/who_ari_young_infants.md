---
unique_name: who_ari_young_infants
name: WHO ARI multicentre study of clinical signs in young infants
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Website
year: '? (1998)'
domain: medical & healthcare
problem_type: Multiclass Classification
source_links:
- https://hbiostat.org/data/repo/ari.html
- https://doi.org/10.1002/(SICI)1097-0258(19980430)17:8<909::AID-SIM753>3.0.CO;2-O
- https://hbiostat.org/data/repo/ari.zip
- https://hbiostat.org/data/repo/aridescription
- https://hbiostat.org/data/repo/ari
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the WHO multicentre study of clinical signs in 4,552 sick infants under 3 months in Ethiopia, The Gambia, Papua New Guinea and the Philippines, with an ordinal outcome of three levels (3,551 / 490 / 511) built from sepsis, meningitis, hypoxaemia, pneumonia and death, and about 70 history items, signs and vitals known at presentation; the study's aim was a clinical prediction model, and the lab, X-ray and outcome columns ship in the same table.
- Source: Harrell, Margolis, Gove, Mason, Mulholland, Lehmann, Muhe, Gatchalian, Eichenwald et al. for the WHO/ARI Young Infant Multicentre Study Group, "Development of a clinical prediction model for an ordinal outcome: the World Health Organization Multicentre Study of Clinical Signs and Etiological Agents of Pneumonia, Sepsis and Meningitis in Young Infants", Statistics in Medicine 17(8):909-944 (1998-04-30; metadata through Crossref, the text not read); data in Frank Harrell's Vanderbilt repository (https://hbiostat.org/data/repo/ari.html, https://hbiostat.org/data/repo/ari.zip with files of 2012-03-19, previewed 2026-10-31): ari.csv 4,552 x 97 variables, Y.csv, Y.death.csv and Sc.csv (19 cluster scores); "analyzed in Chapter 14 of Regression Modeling Strategies". Y: 3,551 at 0, 490 at 1, 511 at 2; Y.death: 3,467, 450, 386 and 249 over four levels; countries Papua New Guinea 2,168, Manila 873, Ethiopia 816, Gambia 695. The level definitions are in the 1998 paper.
- Use case: a health worker at a first-level facility decides whether a sick young infant needs referral and treatment for a serious infection, from the history, signs and vitals (the study's stated aim is a clinical prediction model; such signs underlie WHO's young-infant referral rules); fit direct for the clinical columns; regime IID, or grouped by country (4 sites, too few for 5 folds), to decide (SPLIT-3).
- Siblings and duplicates: no record holds this study (grep by hbiostat, ARI multicentre, young infants, pneumonia); the other hbiostat data in the records (such as `bacteremia_vienna`) are other studies. External collections: Harrell's data repository and the Regression Modeling Strategies course.
- Better data: from the curator's Zotero collection (items 79 and 127, data lists); no further search this round.
- Papers and pages: Harrell et al. 1998 (Statistics in Medicine); the study group's 1999 article in the Pediatric Infectious Disease Journal (linked from https://hbiostat.org/data/repo/aridescription, not read); Regression Modeling Strategies, chapter 14 (not read).
- Metric: none found (the hbiostat pages; the paper and the book chapter not read), so the fallback `log_loss` for the three-level target (MET-1, MET-8); inputs none.
- Risks for /add-dataset: drop the outcome and work-up columns: wbco, lpcc, pmcr, bcpc, lp.pos, nxray, s1-s3, pneu, saogp (oxygen saturation defines hypoxaemia), dead, daydth; check clin, impcl, cprot, cdip and weight for values recorded after presentation (LEAK, USE-3); the Sc cluster scores were derived by the authors, possibly fit to Y (do not ship them unless unsupervised, LEAK-27); lab columns are mostly missing (up to 3,673 of 4,552); data of the early 1990s (`Outdated` to weigh); the framing (Y as an ordinal three-class target, Y.death, or any severe outcome as binary) for the curator.
- Priority: gap + (multiclass is thin with 24), use case + (the study's stated aim, a clinical referral decision), source + (Statistics in Medicine paper, a curated repository of the study's data), shape + (4,552 infants, about 70 mixed clinical features, 4 countries), risk - (outcome-defining columns in the table, derived scores).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 127: "Datasets"; the curator's Zotero collection, item 79: "Datasets".
- as published: 4,552 infants under 3 months in Ethiopia, The Gambia, Papua New Guinea and the Philippines x 97 variables (history, clinical signs, vitals; lab and X-ray results for some infants); target: Ordinal severity (sepsis, meningitis, hypoxaemia or pneumonia vs none) or death; access: open.
- Why: A real multi-country clinical study with a published prediction model and a task still done today (IMCI referral signs). | A real multicentre study whose stated aim is a clinical prediction model, with many clinical-sign features known at presentation; country gives a grouped split
- Adds: Paediatric triage in low-income settings, with a country grouping. Caveats: dated and small; the lab and X-ray columns are parts of the outcome (leak risk) and must be dropped. | Paediatric triage in low-resource settings, not in the records. Lab, X-ray and outcome columns must be kept out of the features. Same name ...
