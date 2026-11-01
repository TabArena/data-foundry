---
unique_name: hepatocyte_clearance_astrazeneca
name: clearance_astrazeneca
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Company
year: '2015'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.6019/CHEMBL3301361
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/clearance_astrazeneca ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/clearance_astrazeneca ; original: https://tdcommons.ai/single_pred_tasks/adme/#clearance-astrazeneca (TDC Clearance_Hepatocyte_AZ)'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: one company's in-house hepatocyte clearance measurements, a task a DMPK group runs every week, with a benchmark that fixes the metric and the split; the row set has to be pinned first.
- Source: AstraZeneca's deposition of in-vitro DMPK and physicochemical data in ChEMBL, CHEMBL3301361 (doi 10.6019/CHEMBL3301361; ChemNLP cites Hersey 2015, the TDC page dates it 2016), with Di, Li et al., "Mechanistic insights from comparing intrinsic clearance values between human liver microsomes and hepatocytes to guide drug design", Eur J Med Chem 57:441 (2012) as the assay paper. As published: intrinsic clearance for AZ project compounds in two assay types; TDC splits them, "1,102/1,020 drugs for microsome/hepatocyte clearance", and serves the hepatocyte set as Clearance_Hepatocyte_AZ. The ChemNLP config carries 1,213 points and its description says the set "covers two experiment types: hepatocyte and microsome", so that cut is not TDC's 1,020 hepatocyte rows. Columns: SMILES, ChEMBL id, the clearance value (ChemNLP declares mL/(min g); the TDC page gives no unit).
- Use case: a DMPK scientist ranking project compounds by metabolic stability to decide which to carry into an in-vitro or in-vivo slot; the benchmark that defined the task names the purpose, not the person, so fit approximate; regime grouped on the Bemis-Murcko scaffold (SPLIT-31 as amended; TDC uses a scaffold split for every ADMET benchmark).
- Siblings and duplicates: `astrazeneca_chembl_logd74` and `tdc_lipophilicity_astrazeneca` come from the same deposition but hold logD7.4, a distinct task (PROV-7, not a duplicate); the microsome clearance variant of the same deposition is a sibling task, not in ChemPile-LIFT; `biogen_adme` is a single-lab ADME set with its own clearance endpoints and is the closest competitor; `caco2_permeability_merged`, `drug_half_life_obach`, `vdss_lombardo`, `pampa_ncats` are the other ADME candidates of this run. External collections: ChemPile-LIFT config `clearance_astrazeneca` (arXiv 2505.12534), TDC ADMET Benchmark Group.
- Better data: a candidate of the benchmark ChemPile (this run searched no further).
- Papers and pages: Di et al. 2012 (the assay and the hepatocyte-microsome comparison); the ChEMBL deposition report card CHEMBL3301361; the TDC ADME page and the ADMET Benchmark Group leaderboard.
- Metric: the TDC ADMET Benchmark Group ranks Clearance_Hepatocyte_AZ by Spearman correlation on a scaffold split (tdcommons.ai/benchmark/admet_group/overview; "Spearman's correlation coefficient is used for benchmarks that depend on factors beyond the chemical structure"), the one deliberate criterion of the benchmark that defined this task (MET-1, MET-5); inputs none. The data's own first publication (a ChEMBL deposition) scores nothing.
- Risks for /add-dataset: which rows the build takes (TDC's 1,020 hepatocyte compounds against the ChemNLP cut of 1,213 that mixes hepatocyte and microsome; mixing two assay types changes what the target means, MET-2, PROV-15); clearance values are censored at the assay limits and heavily skewed, so a log scale and the handling of pile-ups at the limit decide the metric (MET-3); features are the SMILES only, so RDKit descriptors as for `apistox`; check the unit against the ChEMBL assay record (uL/min/10^6 cells for hepatocytes against ChemNLP's mL/(min g)).
- Priority: gap 0 (chemistry not thin), use case + (a standing DMPK decision), source + (a named company deposition with a report card, an assay paper and a benchmark), shape + (about 1,000-1,200 compounds, ~200 descriptors once computed), risk - (the row set and the assay-type mix are unresolved).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,213 compounds in ChemNLP; the TDC page lists 1,020 for Clearance_Hepatocyte_AZ; in ChemPile-LIFT 6,065 text prompts over 1 config(s); target: hepatocyte intrinsic clearance (uL/min/10^6 cells).
- Why: Predict intrinsic clearance of a compound in human hepatocytes
- Notes: AstraZeneca deposition in ChEMBL (CHEMBL3301361, 2016), the same deposition the lipophilicity set comes from; the microsome clearance variant (1,102) is not in ChemPile-LIFT. Features: SMILES string only, so a container keeps the string and adds computed descriptors, as the apistox record does. No record.
