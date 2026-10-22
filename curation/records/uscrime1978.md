---
unique_name: uscrime1978
name: USCrime1978
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
year: '1978'
domain: social science
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=1089
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** recommend `No` with `Too Small` (TP-5) and `No Good Target  / Scientific Discovery` (SEL-3), as the workbook's "Tiny data" and both curators' "too small" say; the `TBD -> 2nd Tier` came from an AI "policy" update, not from a curator, and the current rules keep `Too Small` as a reason for `No`. The curator has the call.
- Source: Vandaele, W. (1978), "Participation in illegitimate activities: Ehrlich revisited", in Blumstein, Cohen and Nagin (eds.), Deterrence and Incapacitation, National Academy of Sciences, 270-335; reprinted in DASL (USCrime) and Hand et al. (1994), A Handbook of Small Data Sets; on OpenML as 1089 `USCrime` (uploaded 2014 from TunedIT); as published: 47 US states in 1960 x 14 numeric columns, the crime rate `R` and 13 demographic, labour and police-spending variables; OpenML's default target is `X` ("The number of families per 1000 earning below 1/2 the median income"), not the crime rate.
- Use case: none; the data were "collected from the FBI's Uniform Crime Report and other government agencies to determine how the variable crime rate depends on the other variables measured in the study" (OpenML description, from DASL): an explanatory study of deterrence, one row per state in one year; nobody predicts a state's crime rate from these at a decision point (SEL-3).
- Siblings and duplicates: no other record of this data; it also ships as `UScrime` in R's MASS package. External collections: none found.
- Metric: none found (OpenML and DASL descriptions), so the fallback `rmse`.
- Risks: 47 rows, about 16 per test fold under 3-fold CV (TP-5); OpenML's target is a covariate of the study.
- Priority: 1 (gap + for social science, use case 0, source 0, shape - (47 rows), risk - (no real target)); set only because the verdict is not `No`.

The classic US crime dataset (OpenML id 1089) with only 47 samples. Both the TabArena curation verdict and reviewers (Lennart, Andrej) mark it as too small, which is too few for reliable 3-fold CV evaluation. It fails the adequate-size criterion and should be rejected as Too Small; no further verification needed.

**Update (policy):** "Too Small" is no longer a rejection reason — dataset size is assessed *after* Data Foundry processing. Re-classified off No to TBD -> 2nd Tier pending that post-DF size check.

---

Imported from the TabArena curation workbook.

TabArena curation verdict: Tiny data.

47 samples,  too small with 3-fold CV.

Lennart: too small

Andrej: too small
