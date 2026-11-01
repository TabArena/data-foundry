---
unique_name: record_linkage_comparison_patterns
name: Record Linkage Comparison Patterns
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: UCI
year: '2011'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C51K6B
- https://archive.ics.uci.edu/dataset/210/record+linkage+comparison+patterns
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: 5.7 million record pairs of a registry with nine field-comparison scores and a match label from manual review, the deduplication task of `nomao` on far more pairs; real and documented, but matches are rare and the comparison patterns may make it near trivial, and `nomao` stays `2nd Tier` on the same kind of features.
- Source: UCI Machine Learning Repository 210, "Record Linkage Comparison Patterns", donated 2011-03-09, cited as Schmidtmann, Hammer, Sariyar, Gerhold-Ay (2009), doi 10.24432/C51K6B, CC BY 4.0. As published: 5,749,132 record pairs (20,931 matches, 0.36%) from "a sample of 100.000 records dating from 2005 to 2008", split into 10 blocks of about equal size and match ratio; columns id_1, id_2, cmp_fname_c1, cmp_fname_c2, cmp_lname_c1, cmp_lname_c2 (string similarities from 0 to 1), cmp_sex, cmp_bd, cmp_bm, cmp_by, cmp_plz (agreement 0/1), is_match; missing values present; a `frequencies.csv` for Fellegi-Sunter u-probabilities. Labels: pairs "classified as 'match' or 'non-match' during an extensive manual review" by several documentarists, used to assess the registry's own linkage. The UCI page does not name the registry and lists no paper.
- Use case: the registry's linkage step decides, when a new report arrives, whether it belongs to a person already registered, or sends the pair to clerical review; the UCI page states the decision ("whether the underlying records belong to one person"), fit direct. Regime IID over pairs, with records repeated across pairs (id_1, id_2) as a group question (LEAK-17); the 10 blocks are random partitions, not a design.
- Siblings and duplicates: `nomao` (`TBD -> 2nd Tier`, `Wrong Domain / Source Modality`, `NLP (Text)`; the curator's CC: comparisons of text fields, "likely already filtered for obvious cases", "very low errors for all models; task sounds not like a predictive task?"), the same task on places instead of people; no copy of this dataset among the records. External collections: not checked (web search budget used up).
- Better data: found as better data for `nomao`; no further search this round.
- Papers and pages: the UCI page. Papers that used it (Sariyar and colleagues on record-linkage error rates) were not read.
- Metric: none found on the UCI page; no paper read, so the fallback `roc_auc` (MET-1, MET-8); with 0.36% matches a hard-label metric would need the source's threshold, which it does not give (MET-6); inputs none.
- Risks for /add-dataset: near separability (`Trivial`, TP-4): exact agreement on name, birth date and postal code may decide almost every match, which TP-4 would measure; the modality objection of `nomao` (scores computed from text fields), though here only four of nine columns are string similarities and the raw names are not published; pairs share records, so a record's other pairs carry its label (LEAK-17, a grouped split by record to consider); 5.7 million rows need the 1M cap.
- Priority: gap 0 (binary and IID are not thin; the domain, a population registry, is not stated), use case + (the page states the linkage decision), source + (a documented UCI donation by four named donors, with a DOI), shape + (5.7 million pairs, nine features of two kinds), risk - (a likely near-trivial task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nomao`.
- as published: 5,749,132 record pairs, 12 columns (two record ids, comparison scores of first and family name, agreement of sex, birth day/month/year and postal code, the match label), from a sample of 100,000 ...; target: is_match: both records belong to the same person (binary); access: open.
- Why: The same task as nomao (decide from field-wise similarity features whether two database records describe the same entity, to deduplicate the database), with features of the same kind.
- Adds: About 167 times the pairs (5.7 million against 34,465), labels from an extensive manual review. Not newer (records 2005-2008). Caveats: matches are rare (about 0.4%) and known to be nearly separable (Trivial risk), and the modality objection that rejected nomao (features derived from text fields) applies here too.
