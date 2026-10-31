---
unique_name: sigma_aldrich_safety_data
name: msds
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Multi-target
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Company
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
source_links:
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/msds ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/sigma_aldrich_safety_data ; original: https://www.sigmaaldrich.com (safety data sheets); ChemNLP folder sigma_aldrich_safety_data'
- https://arxiv.org/abs/2505.12534
- '# the table the ChemNLP builder downloads (msds.csv): SMILES plus one boolean per H-statement'
- https://huggingface.co/datasets/chemNLP/msds_sigma_aldrich
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: the ChemPile config is whole safety data sheets as text and out of scope as served, but the table underneath it (a compound's GHS hazard statements from its SMILES) is a real tabular multi-label task; it is kept at the bottom of the queue because the data is an undocumented scrape of a vendor's website.
- Source: the safety data sheets Sigma-Aldrich (Merck) publishes for the products it sells. There is no publication and no release page behind the table: ChemNLP's `meta.yaml` describes it as "H-statements parsed from the safety datasheets (SDS) coming from Sigma-Aldrich. This dataset refers only to pure compounds", gives one link (`https://www.sigmaaldrich.com/DE/de`, "corresponding source for the safety datasheets"), an empty `bibtex: []` and no licence field; the builder downloads `msds.csv` from the Hugging Face dataset `chemNLP/msds_sigma_aldrich` and drops the free-text `h_statements` column. As published there: `num_points: 6420`, one identifier `SMILES` and one boolean target per H-statement (H206 "fire, blast or projection hazard", H208, H211, H220, H221, H224, H225, H226, H228, H240, ... — about a hundred codes). The ChemPile-LIFT `msds` config is something else: 12,892 whole sheets as markdown (checked with the dataset viewer by the scouting run), which is text, not a table.
- Use case: whoever classifies and labels a substance before it is shipped or handled (a supplier's regulatory affairs team, or a lab planning to work with an untested compound) decides which hazard statements apply from the structure, when no test data exists; fit approximate, since the sheets record what the supplier assigned, much of it copied from harmonised classifications rather than predicted; regime grouped on the Bemis-Murcko scaffold, as for every molecule dataset with exact structures (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: no earlier record (checked for sigma, msds, safety data sheet, GHS, H-statement). Other hazard and toxicity candidates are different sources and endpoints (PROV-7): `qsar_oral_toxicity` (`Yes`, the ICCVAM/CATMoS acute oral toxicity set), `ld50_zhu`, `toxvaldb_in_vivo_toxicity_values`, `clock_protein_toxicity`, `tox21`, `flash_point_sun_morgan` (a physical hazard property). External collections: ChemPile-LIFT (`msds`), ChemNLP (`sigma_aldrich_safety_data`).
- Better data: a candidate of the benchmark ChemPile; no new search this run. For the same task a public regulatory inventory (the ECHA C&L inventory, which publishes GHS classifications per substance) would be the documented source; nothing was searched for this run.
- Papers and pages: none. ChemNLP's `meta.yaml` carries no bibliography for this folder, and no paper describing the scrape was found; the only pages are the ChemNLP folder, the Hugging Face copy and the vendor's site.
- Metric: none found (ChemNLP's metadata declares none; there is no challenge and no paper). The fallback per H-code is `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: provenance — an undated scrape of a vendor site, with no record of which products were read, when, or how the H-statements were parsed, so what the table is cannot be checked against the source (PROV-1, PROV-2; the note here is the reason for the low priority, not for a `No`); no licence is stated anywhere for the scraped sheets (a note only, EV-4); which code becomes the target, and the prevalence of each (most of the hundred codes will have very few positives, TP-5, TP-8), or whether several ship at once (`Multi-target`, CLEAN-18); whether the sheet's statement is a harmonised classification that follows a published list for part of the compounds, which would make those rows a lookup rather than a prediction (SEL-5); 6,420 compounds against 12,892 sheets, so the pure- compound filter has to be reproduced; one column as published, so the features come from the shared RDKit descriptor helper (`apistox` precedent).
- Priority: gap 0 (chemistry & material science is not thin), use case 0 (a regulatory document, no stated decision), source 0 (a vendor-site scrape with no publication and no licence), shape + (6,420 compounds), risk - (undocumented provenance and a multi-label target with rare codes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 12,892 safety data sheets in the ChemPile config; 6,420 compounds in the ChemNLP sigma_aldrich_safety_data table; in ChemPile-LIFT 12,892 text prompts over 1 config(s); target: the sheet text; in the ChemNLP table, one boolean per H-statement (H206, H208, ... ).
- Why: Read a material safety data sheet (the ChemPile config is the whole sheet as markdown); the ChemNLP table behind it assigns GHS hazard statements (H-codes) to a pure compound
- Notes: Out of scope as shipped: the config holds whole markdown safety sheets (checked with the dataset viewer: section-by-section text of a Sigma-Aldrich SDS), not a table. The ChemNLP table it was built from (H-codes per compound) would be a tabular multi-label task, but the source is a vendor website without a licence ...
