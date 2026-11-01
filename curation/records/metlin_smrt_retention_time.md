---
unique_name: metlin_smrt_retention_time
name: METLIN Small Molecule Retention Time (SMRT) dataset
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6084/m9.figshare.8038913
- https://doi.org/10.1038/s41467-019-13680-7
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6925099/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: 80,038 small molecules with a reverse-phase retention time measured on one LC-MS method (METLIN SMRT, Nature Communications 2019), published as training data for retention-time prediction in metabolite annotation; a large measured molecular-property regression.
- Source: Domingo-Almenara, Guijas, Billings, ..., Siuzdak, "The METLIN small molecule dataset for machine learning-based retention time prediction", Nature Communications 10:5811 (December 2019, doi 10.1038/s41467-019-13680-7, PMC6925099); figshare 10.6084/m9.figshare.8038913 (posted 2019-12-19, Apache 2.0). As published: SMRT_dataset.csv (12.6 MB; columns `pubchem`, `rt` in seconds, `inchi`, previewed), SMRT_dataset.sdf (structures), Dragon 7 descriptors (zip, 521 MB), ECFP 1024-bit fingerprints and the paper's DNN; "an experimentally acquired reverse-phase chromatography retention time dataset covering up to 80,038 small molecules" (Abstract), pure standards run on one Agilent 1100/1200 HPLC with a Zorbax Extend-C18 column and one fixed gradient (Methods).
- Use case: an analyst annotating LC-MS features ranks or filters the candidate structures of an accurate-mass search by their predicted retention time on this method ("predicted-experimental projection ranked the correct identity among the top three candidates in up to 70% of cases", Conclusion); fit direct for the METLIN method, approximate for other methods (they need a calibration); regime IID, one row per molecule, as the paper's random 75/25 split; a scaffold split is the harder variant for the curator.
- Siblings and duplicates: `report_retention_times` (RepoRT, unscreened, from the same Zotero item) contains SMRT as its dataset 0186 ("SMRT_METLIN", Domingo-Almenara; raw_data/0186/0186_info.tsv in the RepoRT GitHub, read), so most of RepoRT's rows are these: RepoRT's own task is retention time across chromatographic methods with the method metadata as inputs (distinct, PROV-7, if shipped that way; otherwise a version, PROV-6, and the curator picks one). `mona_spectral_entropy` (`No`, MoNA spectra) is unrelated. External collections: none in our vocabulary; RepoRT carries it.
- Better data: from the curator's Zotero collection (item 13, an error-detection workflow paper applied to SMRT); no further search this round.
- Papers and pages: the Nature Communications paper (read); Khrisanfov, Matyushin and Samokhin, "Finding potentially erroneous entries in METLIN SMRT", J Chromatogr A 1745:465761 (2025; ChemRxiv December 2024), flagging about 1,300 entries (about 1.6%) by 5-fold cross-validated prediction error (abstracts and secondary pages only; ChemRxiv refused the fetch).
- Metric: the paper reports mean and median relative and absolute errors side by side ("mean and median absolute errors of 57 s and 35 s", Results), none named as the criterion (MET-5), so the fallback `rmse` on seconds; inputs none.
- Risks for /add-dataset: the non-retained molecules ("elute before the start of the gradient, typically within the first minute", Results; rows at 79.7 s and 93.5 s in the preview) form a separate cluster the paper leaves out of parts of its analysis: keep them as a real outcome or drop them, a target decision (USE-5); the flagged erroneous entries (repair from the published exclusion list or keep with a note, PROV-13); structures come as InChI and SDF, so the features are pinned RDKit descriptors or fingerprints (CLEAN-24); stereoisomers share 2D descriptors with different retention times; the overlap with RepoRT above (PROV-6).
- Priority: gap 0 (chemistry & material science and regression are not thin), use case + (the paper names candidate filtering in metabolite annotation), source + (a data paper with methods and an open deposit), shape + (80,038 molecules), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 13: "Towards robust databases: an ensemble-based workflow for error detection applied to ...".
- as published: 80,038 small molecules, one row per molecule; SMRT_dataset.csv (12.6 MB: PubChem id + retention time in seconds), SMRT_dataset.sdf (structures), Dragon 7 molecular descriptors (zip, 521 MB) and ...; target: experimental reverse-phase retention time in seconds (regression); access: open.
- Why: real measured chemistry published for prediction (the paper's whole point is ML-based RT prediction), one standardised method, structure-only inputs known before the measurement; same handling as apistox / qsar_bioconcentration (SMILES or SDF to pinned RDKit descriptors, CLEAN-24)
- Adds: a large measured molecular-property regression task (80k rows) that we do not have; unlike molecularproperties (QM9/CHAMPS, DFT-computed, rejected as simulated) every value here is measured
