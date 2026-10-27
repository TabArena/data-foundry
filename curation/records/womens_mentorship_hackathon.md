---
unique_name: womens_mentorship_hackathon
name: womens-mentorship-hackathon
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: social science
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://zindi.africa/competitions/womens-hackathon
- https://zindi.africa/competitions/womens-mentorship-hackathon
- https://zindi.africa/competitions/she-solves-hackathon-womens-hack-for-safety
source_row: 1003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: whether a South African woman experienced a crime in the last five years, from survey answers; real and large enough, but the label likely comes from the same interview as the features (SEL-7) and no decision is named.
- Source: first publication Zindi "Women's Hack for Safety", a one-day women-only hackathon on 10 April 2021 by the Agence Française de Développement, with DataFirst (UCT) and Stats SA named as partners (https://zindi.africa/competitions/womens-hackathon, read through Zindi's API). This record's "Women's Mentorship #1: Hack for Safety" (14 May to 19 July 2021) and "She Solves Hackathon - Women's Hack for Safety" (Feb to Mar 2022) are Zindi children of it with byte-identical files (Train.csv 2,495,328 bytes, Test.csv 1,063,766, VariableDefinitions.csv 948). As published: "The train set contains ~7700 individuals with various information including if they have experienced a crime in the last 5 years or not"; the test set "has ~3300 individuals" without labels. The survey wave is not named; Stats SA's Victims of Crime Survey (on DataFirst) is the likely origin, not confirmed. Columns not read (login).
- Use case: "build a machine learning model that predicts a woman's level of risk of being victimized by a crime given basic information about her and her life" (Description); no actor or decision is named (a safety programme that targets women at risk would be ours). Fit approximate at best. Regime IID (one survey cross-section), unless households or areas group the respondents.
- Siblings and duplicates: no other record; the three Zindi pages are one dataset and this record stands for the family (links reordered, first publication first, the repeated link dropped). External collections: none found.
- Papers and pages: none beyond the competition pages.
- Metric: AUC ("The error metric for this competition is Area Under the Curve", Evaluation page): roc_auc, a competition's leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: SEL-7, a label the respondent already knows, asked in the same interview as the features: check that the features are "basic information" (age, place, household) and not answers that follow a crime (feeling unsafe, avoidance, reporting) (LEAK); the survey wave and its weights. The old `Ethical Issue` marker is dropped: the source states no objection to ML use and the task as stated is not harmful (SEL-1), though the curator may weigh the sensitivity; the old `Too Small` is refuted by ~7,700 labelled rows.
- Priority: gap + (social science, thin), use case 0 (no decision named), source 0 (a competition page, survey not named), shape + (~7,700 respondents), risk - (SEL-7 and post-crime answers).

This Zindi women's mentorship hackathon asks to predict which women are at highest risk of being made a victim of a crime in South Africa. It is plausibly a genuine tabular classification task, but predicting individual crime-victimization risk for women raises clear ethical sensitivity, and hackathon datasets are usually small. There is almost no detail in the record (no size, features, target definition, or split regime). A human must inspect dataset size, the exact target, and weigh the ethical concern; provisionally 2nd Tier.

---

Predict which women are at highest risk of being made a victim of a crime in South Africa
