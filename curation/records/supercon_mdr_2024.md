---
unique_name: supercon_mdr_2024
name: 'MDR SuperCon Datasheet (NIMS): superconductor compositions and critical temperatures'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Website
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.48505/nims.4487
- https://mdr.nims.go.jp/datasets/650c4826-f0ca-42e8-8dd9-94025a5307ce
- https://mdr.nims.go.jp/collections/4c428a0c-d209-4990-ad1f-656d05d1cfe2
- https://doi.org/10.48505/nims.4488
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: NIMS's maintained, re-edited SuperCon datasheet (Ver.240322, CC BY 4.0), the database the shipped `superconductivity` set was drawn from, with later entries and with non-superconducting observations the UCI cut lacks; the composition features must be rebuilt, and the curator decides which version enters (PROV-6).
- Source: National Institute for Materials Science (NIMS), Center for Basic Research on Materials, "MDR SuperCon Datasheet Ver.240322" on the Materials Data Repository (doi 10.48505/nims.4487, posted 2024-05-14), "a datasheet re-edited from SuperCon, which was originally published as the MatNavi database" ("A doi is issued each time the datasheet is revised", collection page; the collection also holds Ver.220808). Files: `20240322_MDR_OAndM.txt` (19 MB, oxides and metallic), `240322_MDR_Organic.txt` (257 KB), a JSON and a YAML schema, `data.zip` (2.9 MB), `figure.zip` (51 MB). Readme Ver.2.0 (doi 10.48505/nims.4488): an English readme that maps the datasheet to the MatNavi fields, and `primary.tsv` (1.9 MB) with recommended Tc values for the oxide and metallic data. Counts are not on the NIMS pages; a third-party record (Leonforte, Zenodo 22771914, 2026) counts "33,458 measurements against 7,254 distinct source references", and another (Zenodo 22772787) 3,130 formulas listed only as non-superconducting in Ver.240322. Files not opened.
- Use case: a materials scientist screens candidate compositions for a high critical temperature before synthesis, as for the shipped sibling (Hamidieh 2018; fit approximate there with `Selection Bias`, since UCI holds only superconductors). NIMS names no decision. The non-observations ("no transition down to X K") could give the negative class the UCI cut lacks, as a classification or a censored target; fit approximate. Regime grouped by composition, as for the sibling (CC 2026-10-06).
- Siblings and duplicates: `superconductivity` (`Yes`, shipped; UCI, Hamidieh 2018, 21,263 rows with 81 derived features, grouped by composition) and `superconductivity_duplicate` (`No`): the same database in an earlier extract, so this is a newer release of the same source (PROV-6) and the curator decides which one enters (a replacement that closes the selection gap is one reading, USE-8). `experimental_band_gap_zhuo` (unscreened) and `systematically_verified_thermoelectric_zt` are other properties. External collections: 3DSC, a SuperCon-derived set matched to crystal structures, which the third-party note analyses; not checked here.
- Better data: found as better data for `superconductivity`, and from the curator's Zotero collection (items 99 and 191, "blaiszik/awesome-matchem-datasets"); no further search this round.
- Papers and pages: the NIMS MDR dataset, readme and collection pages; Hamidieh, "A data-driven statistical model for predicting the critical temperature of a superconductor", Computational Materials Science, 2018 (the sibling's paper); Leonforte's two Zenodo records (doi 10.5281/zenodo.22771914 and 10.5281/zenodo.22772787, 2026), third-party analyses rather than the data, moved here from the links (PROV-12).
- Metric: none from NIMS (a database); the sibling declares `rmse` from Hamidieh's out-of-sample RMSE of Tc. So `rmse` on Tc for a regression on superconductors (MET-1); a classification with the non-observations would take the fallback; inputs none.
- Risks for /add-dataset: the 81 composition features of the UCI version must be rebuilt from the formula (for example matminer's Magpie set), a featurisation of ours to document (PROV-11); non-observations sit in the Tc field as statements with a floor, not as Tc = 0 (USE-5); several measurements per composition that disagree (the sibling found a spread above 30 K for 132 compositions: other samples or pressures); retracted sources (nine found by the third-party note); which file is the task (oxides and metallic, organic, or `primary.tsv`).
- Priority: gap 0 (chemistry & material science has 12 accepted datasets; regression and grouped not thin), use case 0 (NIMS names no decision; the sibling's fit is approximate), source + (NIMS with schema and readme), shape + (about 33,000 measurements by the third-party count), risk - (features to rebuild, non-observations in the target field, a second version of a shipped dataset).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `superconductivity`; the curator's Zotero collection, item 191: "blaiszik/awesome-matchem-datasets"; the curator's Zotero collection, item 99: "blaiszik/awesome-matchem-datasets".
- as published: Ver.240322: 33,458 Tc measurements against 7,254 source references, per a third-party Zenodo record (22771914, 2026-09-15); not counted. Files: 20240322_MDR_OAndM.txt (oxide and metallic), ...; target: Critical temperature Tc (K), regression, as in superconductivity; access: open.
- Why: The maintained current release of the NIMS SuperCon database, the source of the UCI superconductivity set (Hamidieh 2018, 21,263 rows) that TabArena ships. | the database Hamidieh (2018) drew the 21,263 rows from, in a maintained, re-edited and versioned release; the same target, and the same kind of features ...
- Adds: About 1.5 times the rows and later entries, under CC BY 4.0. Caveats: the 81 composition-derived features of the UCI version must be rebuilt (e.g. matminer Magpie). The note in Zenodo 22772787 (the current version of the first pass's 22235399) warns that 'no transition down to X K' non-observations sit in the Tc ...
- A newer release of the same source as the record(s) named above (PROV-6): the curator decides which one enters.
