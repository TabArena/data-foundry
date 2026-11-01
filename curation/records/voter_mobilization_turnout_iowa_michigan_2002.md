---
unique_name: voter_mobilization_turnout_iowa_michigan_2002
name: 'Voter mobilization experiment (Arceneaux, Gerber, Green 2006): turnout in the November 2002 election in Iowa and Michigan'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Other
year: '? (2006)'
domain: social science
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.60600/YU/XD0LK8
- https://doi.org/10.1093/pan/mpj001
- https://github.com/gsbDBI/ExperimentData/tree/master/Mobilization
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 2,474,927 registered voters of Iowa and Michigan with turnout in the November 2002 election from the voter files, published with a phone-mobilization experiment; very large and open (CC0), but published for a causal comparison, with a short feature list led by past turnout and treatment columns to remove (the verdict and priority follow `social_pressure_turnout_michigan_2006`, the same kind of data).
- Source: Arceneaux, Gerber, Green, "Comparing Experimental and Matching Methods Using a Large-Scale Voter Mobilization Experiment", Political Analysis 14(1) (2006, https://doi.org/10.1093/pan/mpj001); data in the ISPS Data Archive on Yale Dataverse (https://doi.org/10.60600/YU/XD0LK8, CC0; the current version is dated 2026-01-07, the first archive date was not read). As published (Dataverse API and DDI, 2026-10-31): ArceneauxGerberGreen_PA_2006_IA_MI_merge040504.tab, 2,474,927 cases with persons (voters in household), competiv, vote00, vote98, newreg, pid_maj, age, female (with female2, fem_miss), state, county, st_sen, st_hse, comp_mi, comp_ia, vote02 (target), treatmen, treat_real, treat_pseudo, contact, pseudo_c, pseudo_portion, lc, hc and bad_county ("2002 voter records not provided"); plus matched and exact-matching extracts and Stata and R replication code. Abstract: "60,000 randomly assigned to the treatment group and nearly two million assigned to the control group".
- Use case: a campaign or party, before an election, scores registered voters' likelihood to vote from the voter file to target mobilization; the source poses no prediction (its question is whether matching recovers the experimental effect); fit approximate (the use case is ours); regime IID within one election, with household size and county as possible groupings (no household id in the variable list) (SPLIT-3).
- Siblings and duplicates: `social_pressure_turnout_michigan_2006` (`TBD -> Yes`, 3, screened this run; Gerber, Green, Larimer 2008, 344,084 Michigan voters of the August 2006 primary, the same archive and the same kind of voter-file turnout task): another election and experiment, not a duplicate (PROV-7), though the curator may take only one turnout-from-voter-file task (this one is seven times larger and not restricted to 2004 voters; that one has household ids and four mailings); `ces_validated_turnout` (`TBD -> Yes`, 3): survey respondents with validated turnout, another source; `anes_voting_2026` (accepted): survey-based. External collections: gsbDBI/ExperimentData (https://github.com/gsbDBI/ExperimentData/tree/master/Mobilization, experiments collected for heterogeneous-effect studies).
- Better data: from the curator's Zotero collection (items 132 and 134); no further search this round.
- Papers and pages: Arceneaux, Gerber, Green 2006 (instrumental-variable and matching estimates of the call effect); the Dataverse readme and DDI.
- Metric: none found (the paper estimates treatment effects; the Dataverse page and readme; the ExperimentData README not read), so the fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: contact and pseudo_c are post-assignment and go, the treatment columns are the experiment's design (drop, or keep the control group only) (LEAK, USE-3); rows of counties with bad_county set have no 2002 records and go; vote98 and vote00 may carry most of the signal (TP-10 against a past-turnout profile, TP-4); county and district codes are high-cardinality; 2.47 million rows need a 1M version or a sample.
- Priority: gap + (social science has 1 accepted dataset), use case 0 (ours, approximate), source + (Political Analysis paper, Yale archive with a DDI codebook), shape + (2.47 million voters, categorical and numeric, groupings), risk - (the post-treatment contact columns sit in the table and past turnout may decide the task).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 132: "gsbDBI/ExperimentData"; the curator's Zotero collection, item 134: "Data | Institution for Social and Policy Studies".
- as published: 2,474,927 registered voters x 26 columns (confirmed from the Dataverse DDI of ArceneauxGerberGreen_PA_2006_IA_MI_merge040504.tab), November 2002; target: vote02 (voted in 2002); access: open.
- Why: A very large, open (CC0) administrative turnout table with a published paper. Same hit as item 134 in zotero_25.json. | A very large, open (CC0) administrative turnout table with a published paper.
- Adds: About 2.5M rows, two states. Caveats: thin features dominated by past turnout (TP-10); 'contact' is post-treatment and must go; a sibling of the Michigan 2006 hit (PROV-7), take the stronger one if only one. | About 2.5M rows, two states. Caveats: thin features dominated by past turnout (TP-10, as above); 'contact' ...
