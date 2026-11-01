---
unique_name: shell_ai_2025_fuel_blend_properties
name: 'Shell.ai Hackathon 2025: fuel blend properties prediction'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Anonymized
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- Multi-target
original_source: Other
year: '2025'
domain: chemistry & material science
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.hackerearth.com/challenges/new/competitive/shellai-hackathon-2025/
- https://github.com/LD-Shell/shell_hackathon_2025
- https://www.kaggle.com/datasets/srisujal/shell-ai-dataset
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: an industrial competition (Shell.ai Hackathon 2025 on HackerEarth) on 2,000 fuel blends with anonymised, standardised properties; in a preview of the training file two of the ten targets are exact linear blends of the inputs, so the targets look computed rather than measured (PROV-3, test 7), and no source says either way.
- Source: Shell.ai Hackathon for Sustainable and Affordable Energy 2025, HackerEarth, 4-23 July 2025 (about 7,000 registrations; the problem statement and data pages need a login and were not read). As published (the Kaggle copy `srisujal/shell-ai-dataset`, uploaded 18 July 2025 with train.csv, test.csv and sample_solution.csv; train.csv previewed): 2,000 training blends x 65 columns: 5 component volume fractions (steps of 0.01, summing to 1), 50 component properties `Component{i}_Property{k}` and 10 targets `BlendProperty1`-`10`; 500 test blends without public labels. Properties and targets are standardised (mean 0, sd 1), and each blend has its own component property values (1,929 distinct values of `Component1_Property1` in 2,000 rows).
- Use case: a refinery or fuel blender predicts the specification properties of a candidate blend from its components and their volume fractions before mixing it, to pick recipes that meet the specification at least cost (Shell describes the task as predicting the final properties of blends from their components and proportions). Fit approximate: the properties are unnamed, so what is predicted cannot be checked. Regime IID (no time or group columns).
- Generated-data check (PROV-3, test 7; on the previewed train.csv, a least-squares fit, nothing built): regressing each target on the five products fraction_i x property_ik plus the five fractions gives R^2 1.000000 for `BlendProperty1` (max absolute residual 6.5e-05) and `BlendProperty6` (8.5e-05), exact linear volume blending at rounding level after standardisation; `BlendProperty10` 0.9993, `2` 0.998, `4` 0.996, `7` to `9` 0.88-0.97, `3` 0.78, `5` 0.40. Measured blend properties carry laboratory error, so an exact fit says these two targets were computed, most likely by a blending model; the near-linear rest fits the same generator with non-linear terms. Not calibrated against a measured blending set (EV-9). Without a statement from Shell this is a mark linked to the label, which PROV-3 (as amended) allows to be strong enough on its own: the curator decides between `No` (`AHDS`, SEL-16) and asking the organisers first.
- Siblings and duplicates: no other record of the hackathon (grep: shell, hackerearth, fuel blend); `raman_fuel_benchtop` (`TBD -> Yes`, gasoline properties from Raman spectra, another task). External collections: none known.
- Better data: from the curator's Zotero collection (item 9); no further search this round.
- Papers and pages: Daramola, Olanrewaju, Trejo, Enebeli, "A target-specific machine learning framework for predicting fuel blend properties", ChemRxiv 2025, https://doi.org/10.26434/chemrxiv-2025-fq1fq (refused to the fetch, not read), with the team's GitHub `LD-Shell/shell_hackathon_2025` (MIT; public leaderboard 95.476 on half the test set; it holds the raw competition files); the ALCHEMIST write-up of another team, https://alchemist-shellai-hackathon-2025.readthedocs.io/en/latest/ (TabPFN for targets 1-4, RealMLP for 5-10); the TabPFN-3 technical report cites the ChemRxiv paper. The ChemRxiv and ALCHEMIST links moved here from source_links as related work (PROV-12).
- Metric: the leaderboard scored a MAPE-based cost (team write-ups; the official formula in the problem statement was not read), a competition metric under MET-4; but MAPE on targets standardised around zero is unstable (ALCHEMIST: "a handful of faulty predictions can lead to astronomically large MAPE scores"), so MET-2 may overrule it. Inputs none.
- Risks for /add-dataset: the generated-data question comes first (PROV-3); features and targets anonymised (`Anonymized`); ten targets (one dataset per target, or `Multi-target`); test labels not public, so only the 2,000 training rows can ship; the Kaggle copy's terms are unknown (a note, EV-4).
- Priority: gap 0 (chemistry and regression covered), use case 0 (approximate, properties unnamed), source 0 (a competition page that does not document the data), shape + (2,000 blends, 55 inputs), risk - (targets that look computed).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 9: "A Target-Specific Machine Learning Framework for Predicting Fuel Blend Properties".
- as published: 2,000 labelled blends (plus 500 test rows without public labels) x 55 inputs (5 component volume fractions, and 10 anonymised properties for each of the 5 components) and 10 blend-property targets; target: BlendProperty1-10 (continuous, anonymised; one task per property, or multi-target); access: registration.
- Why: An industrial competition with a clear blending decision; the top solutions lean heavily on TabPFN.
- Adds: Fuel-chemistry regression, which we lack. Screen PROV-3 first: a second search still found no statement whether the blends were measured or computed with a blending model, and the properties are anonymised. Redistribution terms of the GitHub and Kaggle copies are unknown.
