---
unique_name: fragile_families_challenge
name: Fragile Families Challenge
checked_by:
- Lennart
data_foundry_status:
- WIP (Triage)
claimed_by: Lennart
suggestion: TBD -> 2nd Tier
priority: 3
decision_markers:
- Available on Request
tags:
- AI-Filled (Verify)
- Many features
original_source: Other
year: '2017'
domain: social science
source_links:
- https://www.pnas.org/doi/10.1073/pnas.1915006117
- https://oprdata.princeton.edu/Archive/FF
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-08):** `TBD -> 2nd Tier`, priority 3: 4,242 families of the Fragile Families study with 12,942 background variables from the child's birth to age 9 and six outcomes at age 15 (GPA, grit, material hardship, eviction, layoff, job training); a wide, documented social-science table, but the source names no decision and warns against using such predictions for one, only half of the families carry outcomes for training, and access needs an application.
- Source: Salganik, Lundberg, Kindel, Ahearn, ... McLanahan et al., "Measuring the predictability of life outcomes with a scientific mass collaboration", PNAS 117(15), 2020 (doi 10.1073/pnas.1915006117, read in full through PMC7165437); the Fragile Families Challenge ran from March to August 2017 on the Fragile Families and Child Wellbeing Study. As published: "The background data included 4,242 families and 12,942 variables about each family", "a version of the wave 1 to 5 (birth to age 9 y) data that we compiled for the Fragile Families Challenge", without genetic and geographic information; "training data that included the six outcomes for half of the families"; the other half split into leaderboard and holdout sets. Access: "currently available to approved researchers from the Princeton University Office of Population Research Data Archive" (oprdata.princeton.edu/Archive/FF: a login and an application).
- The task's table: one outcome per dataset (GPA or material hardship, the two with signal), 2,121 labelled families x 12,942 variables, or 4,242 if the archive now ships the leaderboard and holdout outcomes (to check).
- Use case: none from the source, which measures predictability for science ("The prediction task was not to forecast outcomes in wave 6 ... using only data collected in waves 1 to 5": predict other families' outcomes in the same wave) and writes "Policymakers using predictive models in settings such as criminal justice and child-protective services should be concerned by these results"; a possible one, ours and so approximate, is a social-service programme offering support at age 9 to families at risk of material hardship at 15. Regime IID over families (the challenge's random halves).
- Siblings and duplicates: none (grep: fragile, families, salganik, wellbeing). External collections: none found.
- Better data: none searched (found by the data-scouting run of 2026-11-08).
- Papers and pages: the PNAS paper; Lundberg et al., "Privacy, ethics, and data access: A case study of the Fragile Families Challenge" (Socius 2019, not read); the Socius special collection of 2019 with the participants' papers.
- Metric: "All predictions were evaluated based on a common error metric: mean squared error", reported as R² holdout, the MSE rescaled by that of the training mean (PNAS, Results): the challenge's choice (MET-4), so `rmse`, which ranks every pair of models as the MSE (MET-11), on the chosen outcome; for a binary outcome the MSE is the Brier score; inputs none.
- Risks for /add-dataset: SEL-1 and USE-2 for the curator: predictions about the children and families of a disadvantaged cohort, from a source that warns against decision use; the challenge's ethics review (Lundberg et al.) to read before deciding; access by application (`Available on Request`, no verdict reason); low signal ("R² holdout of about 0.2 for material hardship and GPA and about 0.05 for the other four outcomes"; a small real signal is no reason to retire, TP-2); the background file is the organisers' merge with their own missing-value codes.
- Priority: gap + (social science thin), use case 0 (none from the source), source + (PNAS paper, a documented cohort study), shape + (2,121 to 4,242 families x 12,942 mixed variables), risk - (the ethics question, access by application, a small labelled set).

Found by the data-scouting run of 2026-11-08 for the large-datasets review (wide tables outside biology and medicine, and tables with 2M+ rows).

CC (2026-11-08, Lennart): kept for later (`TBD -> 2nd Tier`, priority 3) in the screening review of the large candidates, round 2.
