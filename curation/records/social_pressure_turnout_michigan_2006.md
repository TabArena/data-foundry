---
unique_name: social_pressure_turnout_michigan_2006
name: 'Social Pressure and Voter Turnout (Gerber, Green, Larimer 2008): turnout in the Michigan August 2006 primary'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '2008'
domain: social science
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.60600/YU/CGMWNW
- https://doi.org/10.1017/S000305540808009X
- https://github.com/gsbDBI/ExperimentData/tree/master/Social
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 344,084 registered Michigan voters of a randomised mailing experiment, with turnout in the August 2006 primary, their turnout history and household; real administrative turnout at scale, but published to estimate treatment effects, with few features and a sample restricted by the experimenters.
- Source: Gerber, Green, Larimer, "Social Pressure and Voter Turnout: Evidence from a Large-Scale Field Experiment", APSR 102(1), 2008, doi 10.1017/S000305540808009X; replication data from the ISPS Data Archive, now Yale Dataverse doi 10.60600/YU/CGMWNW (CC0; Dataverse publication 9 January 2026; the Stata file is dated 30 June 2010; record and file list read through the Dataverse API). As published (`GerberGreenLarimer_APSR_2008_social_pressure.tab`; the header and first 50,000 rows previewed): 16 columns `sex`, `yob`, `g2000`, `g2002`, `g2004`, `p2000`, `p2002`, `p2004`, `treatment` (0 control, 1-4 the four mailings: civic duty, Hawthorne, self, neighbours), `cluster`, `voted`, `hh_id`, `hh_size`, `numberofnames`, `p2004_mean`, `g2004_mean`; 344,084 rows (the run's count from the DDI). In the preview `g2004` is 1 on every row (only voters of the 2004 general election are in the sample), `voted` is 1 on 34% and `treatment` 0 on 56%.
- Use case: a campaign before a primary decides which registered voters to contact, from the voter file's turnout history, age, sex and household (a turnout model), and here which mailing they got. Fit approximate: the source estimates treatment effects and builds no predictive model (SEL-8, read with SEL-2), and the sample is restricted. Regime IID or grouped by household (`hh_id`; the experiment randomised households), to decide.
- Siblings and duplicates: `voter_mobilization_turnout_iowa_michigan_2002` (unscreened; Arceneaux, Gerber, Green 2006, 2.47M voters, November 2002; another experiment and election, PROV-4; the curator may want only one of the two), `ces_validated_turnout` (`TBD -> Yes`, a survey with validated turnout), `anes_voting_2026` (`Yes`, survey turnout); the precedent for a randomised arm as a feature is `hillstrom_email_campaign` (`TBD -> Yes`, priority 3, approximate fit). External collections: the `ExperimentData` repository of Stanford GSB's gsbDBI lab (folder `Social`, a collection of experiments).
- Better data: from the curator's Zotero collection (items 132 and 134); no further search this round.
- Papers and pages: the APSR paper (only the abstract on the Dataverse record read); the Dataverse record with the Stata and R replication code and the mailings; the gsbDBI README.
- Metric: none: the paper estimates treatment effects on turnout, so the fallback `roc_auc` (MET-1, MET-8); an uplift metric would need the arm as a scoring column (MET-2), the curator's call. Inputs none for the fallback.
- Risks for /add-dataset: `g2004` is constant (drop); `p2004_mean` and `g2004_mean` are cluster-level means over a wider population (`g2004_mean` is 0.857 on rows where every `g2004` is 1), so check what they average over and whether they hold the row itself (LEAK); `hh_id` and `cluster` are ids, never features; most inputs are lagged turnout, so TP-10 decides whether a model beats the turnout-history profile; `yob` fixes the age in 2006.
- Priority: gap + (social science thin, one accepted dataset), use case 0 (approximate; the source names no predictive decision), source + (APSR and the ISPS archive with codebook and code), shape + (344,084 voters, household structure), risk - (a causal experiment's restricted sample, few features dominated by turnout history).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 132: "gsbDBI/ExperimentData"; the curator's Zotero collection, item 134: "Data | Institution for Social and Policy Studies".
- as published: 344,084 registered Michigan voters x 16 columns (confirmed from the Dataverse DDI of GerberGreenLarimer_APSR_2008_social_pressure.tab), 180,002 households, August 2006 primary; target: voted (turnout in the August 2006 primary); access: open.
- Why: Real administrative turnout records at scale, open under CC0, first published in the ISPS archive with the APSR paper. Same hit as item 134 in zotero_25.json. | Real administrative turnout records at scale, open under CC0, first published in the ISPS archive with the APSR paper.
- Adds: Administrative turnout (anes_voting_2026 is survey-based). Caveats: few features, six of them lagged turnout (TP-10 decides whether a model beats the turnout-history profile); the neighbours-mailer columns exist only for one arm. | Administrative turnout (anes_voting_2026 is survey-based). Caveats: few features, six ...
