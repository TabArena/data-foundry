---
unique_name: finscope_tanzania_2023
name: FinScope Tanzania 2023 (fifth wave of the FinScope Tanzania demand-side survey)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
year: '2023'
domain: finance
problem_type: Multiclass Classification
source_links:
- https://www.fsdt.or.tz/finscope/
- https://www.fsdt.or.tz/wp-content/uploads/2023/07/FinScope-Tanzania-2023-Launch-Presentation.pdf
- https://www.fsdt.or.tz/wp-content/uploads/2023/05/FinScope-Tanzania-2017-Data-2.zip
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: the 2023 wave of the survey the Zindi Tanzania challenge was cut from, with FinScope's own access strand as a possible target; usage and demographics come from one interview, and the files sit behind a request form.
- Source: Financial Sector Deepening Trust (FSDT) Tanzania, FinScope Tanzania 2023: fieldwork 1 March to 19 April 2023, 22 teams, tablets synchronised to the National Bureau of Statistics (NBS) server; "n=9,915 SAMPLE ACHIEVED" (individual questionnaire), adults 16+; "the data was cleaned, coded and weighted by NBS" (launch presentation, slides 5-10, https://www.fsdt.or.tz/wp-content/uploads/2023/07/FinScope-Tanzania-2023-Launch-Presentation.pdf). As published: the 2023 datasets and full report behind a form (name, organisation, email) on https://www.fsdt.or.tz/finscope/; the waves 2006, 2009, 2013 and 2017 are direct downloads, 2017 with a user guide and the questionnaire. Columns not read.
- Target: the parent's classes (no financial services, other only, mobile money only, mobile money plus) are Zindi's construction from the usage questions; FinScope's own classification is the Financial Access Strand (banked, other formal non-bank, informal only, excluded; slide "The Financial Access Strand Explained"), a rule over the same questions, changed in 2023: "CMGs were previously classified as informal but in 2023 are classified as non-bank formal".
- Use case: as on the parent, a mobile-money provider or bank targeting new clients from demographics and location; fit approximate, since the features and the label come from one interview (SEL-7 to weigh: the respondent knows the label, the provider does not). Regime IID within the wave (enumeration areas as a possible group), or across the 2017 and 2023 waves (questionnaire and strand changed).
- Siblings and duplicates: `mobile_money_and_financial_inclusion_in_tanzania_challenge` (AI `TBD -> Yes`, priority 2; Zindi's extract of FinScope Tanzania 2017): the same survey series, a newer wave with other respondents (PROV-6, the curator decides which enters); `financial_inclusion_in_africa_for_botswana` (AI `TBD -> Yes`; pooled FinScope/FinAccess, target bank account); `dataorg_financial_health_prediction_challenge` (FinScope MSME, `No`; CC 2026-10-22: "Too risky a dataset ... and it is survey data"); `global_findex_2025` (another survey, a run candidate). External collections: none found.
- Better data: found as better data for `mobile_money_and_financial_inclusion_in_tanzania_challenge`; no further search this round.
- Papers and pages: FSDT's FinScope page and the 2023 launch presentation (links above); the NBS key-insights page the run linked answered 404 on 2026-10-31 and was taken out of the links.
- Metric: none found for this wave (FinScope reports shares, no task); the parent's Zindi challenge scored multiclass log loss on its four classes (MET-4 there). So `log_loss`: the source's metric if the Zindi classes are rebuilt, the fallback otherwise (MET-1, MET-8); inputs none; the NBS weights are never a feature.
- Risks for /add-dataset: the usage questions that define the class must go (SEL-5, LEAK); SEL-7 (label and features from one interview); survey weights and clusters; the class rule changed between waves; the request form is a note, not a criterion (EV-4).
- Priority: gap + (multiclass thin), use case 0 (approximate, named by Zindi for the parent, not by FSDT), source + (FSDT and NBS, a documented survey), shape + (9,915 adults, mixed), risk - (the label rule and the same-interview doubt).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mobile_money_and_financial_inclusion_in_tanzania_challenge`.
- as published: 9,915 adults aged 16+ interviewed (launch presentation 'n=9,915 sample achieved'), one adult per household, 15 households per cluster, 2022 census frame; columns not read (files behind a request ...; target: the adult's financial-service usage group (no financial services / other only / mobile money only / mobile money plus other), built from the usage questions ...; access: request.
- Why: the same survey series and questionnaire family as the record's data (Zindi extracted it from FSDT FinScope Tanzania 2017), the same population and the same kind of demographic and location features; the four classes can be rebuilt from the same usage questions.
- Adds: Six years newer (2023 against 2017) on a 2022 census frame; with the open 2017 wave it allows a split across waves and ships the original codebook rather than a competition extract. Not larger (9,915 against about 10,000). Same SEL-7 doubt as the record (features and label from one interview).
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
