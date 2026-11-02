---
unique_name: report_retention_times
name: 'RepoRT: community repository of small-molecule retention times with chromatographic method metadata'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: Github
domain: chemistry & material science
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/michaelwitting/RepoRT
- https://doi.org/10.1038/s41592-023-02143-z
- https://doi.org/10.5281/zenodo.16267767
- https://doi.org/10.5281/zenodo.22305395
- https://rrt.boeckerlab.uni-jena.de/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: RepoRT, a maintained repository of measured LC retention times from 435 contributed datasets, each with standardised structures and full chromatographic method metadata, published as training data for retention-time prediction in metabolite identification; it contains the METLIN SMRT set, so it overlaps `metlin_smrt_retention_time`.
- Source: Kretschmer, Harrieder, Hoffmann, Böcker, Witting, "RepoRT: a comprehensive repository for small molecule retention times", Nat Methods 21(2):153-155, 2024 (doi 10.1038/s41592-023-02143-z); github.com/michaelwitting/RepoRT (created 2020-01-31, last pushed 2026-10-26; CC BY-SA 4.0; release v1.0 on Zenodo, doi 10.5281/zenodo.16267767, 2025-07-21). README: "a repository dedicated to the collection of training data for the development of new retention time prediction models for the identification of small molecules". As published (repository read 2026-10-31): `processed_data/studies.tsv` lists 435 datasets (343 reversed-phase, 71 HILIC, 5 other, 16 unset), each tied to its publication or contributor (PredRet, the Phenome Centre, papers). Per dataset: `rtdata_*_success.tsv` (id, name, formula, `rt` in minutes, standardised SMILES, InChI, ClassyFire classes), `metadata.tsv` (column name, USP code, length, inner diameter, particle size, temperature, flow rate, t0, eluents A to D with additives), `gradient.tsv` (time steps of the eluent shares and flow), and rcdk descriptors and fingerprints. The retention times were not summed here. ChromaGRT (Zenodo doi 10.5281/zenodo.22305395, 2026-09-04, CC BY 4.0) is a curated reversed-phase cut of RepoRT: "37,627 retention-time records corresponding to 13,357 unique standardized molecular structures measured under 151 distinct chromatographic conditions", with random, scaffold and condition splits.
- Use case: the source's: a metabolomics analyst, after a non-targeted LC-MS run, ranks the candidate structures for a feature by how well their predicted retention time on the lab's method matches the measured one; fit direct, for a method seen in training and for a new method described by its metadata. Regime grouped: by chromatographic method (a new lab method, ChromaGRT's condition split) or by molecular scaffold; molecules recur across methods.
- Siblings and duplicates: `metlin_smrt_retention_time` (a candidate of this run, 80,038 molecules on one METLIN method) is inside RepoRT twice (dataset 0186 `SMRT_METLIN`, from Domingo-Almenara et al., and 0209 `SMRT`, through PredRet). RepoRT adds the method as an input and many more methods, a distinct task (PROV-7), but its SMRT rows are the same measurements (PROV-6), so they enter once. ChromaGRT is a processing variant of RepoRT and stays under this record (PROV-6). External collections: the ChromaGRT benchmark splits.
- Better data: from the curator's Zotero collection (item 13, "Towards robust databases: an ensemble-based workflow for error detection ..."); no further search this round.
- Papers and pages: the Nat Methods paper (not read beyond its citation); the README and DataDescription; the ChromaGRT deposit.
- Metric: none found (the README and both Zenodo records name none; the ChromaGRT paper was not read), so the fallback `rmse` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: the gradient is a variable-length program to encode as fixed features, and some datasets lack method fields (`missing information` in studies.tsv); retention time scales with column length, flow and t0, so a raw or normalised target is a choice (USE-5); a molecule repeats within and across datasets, and SMRT's 80,038 rows would dominate (decide together with `metlin_smrt_retention_time`); the repository grows, so pin a commit (PROV-9); structures to descriptors (CLEAN-24).
- Priority: gap 0 (chemistry, regression and grouped are not thin), use case + (the source names the identification use), source + (Nat Methods paper, maintained repository, a publication per dataset), shape + (hundreds of methods and tens of thousands of retention times, molecule and method features), risk - (the gradient encoding and hundreds of tables to assemble; the SMRT overlap).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 13: "Towards robust databases: an ensemble-based workflow for error detection applied to ...".
- as published: hundreds of contributed LC datasets with standardised structures, rcdk fingerprints/descriptors and full method metadata (column, dimensions, flow rate, gradient, eluents); the curated ChromaGRT ...; target: absolute retention time given the molecule and the chromatographic method (regression); access: open.
- Why: real measured data, traceable to each contributing publication, published explicitly as training data for RT prediction; the method metadata gives a natural grouped/held-out-method split
- Adds: multi-method generalisation over SMRT's single method, and a maintained source that keeps growing; the ChromaGRT record already ships condition-aware splits
