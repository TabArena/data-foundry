---
unique_name: dilist_drug_induced_liver_injury
name: 'DILIst: Drug-induced liver injury severity and toxicity, binary classification of 1,279 drugs by human hepatotoxicity'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: GOV Website
year: '2020'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.drudis.2019.09.022
- https://www.fda.gov/science-research/liver-toxicity-knowledge-base-ltkb/drug-induced-liver-injury-severity-and-toxicity-dilist-dataset
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the FDA's list of 1,279 drugs labelled for human liver injury, a regulator-curated safety endpoint; the structures have to be mapped from the drug names.
- Source: Thakkar, Li, Liu, Wu, Roberts & Tong (FDA NCTR), "Drug-induced liver injury severity and toxicity (DILIst): binary classification of 1279 drugs by human hepatotoxicity", Drug Discovery Today 25(1):201-208 (2020, PMID 31669330); download on the FDA Liver Toxicity Knowledge Base page ("DILIst Supplementary Table"; the page asks users to notify NCTR bioinformatics support). As published: 1,279 drugs, "768 were DILI positives ... whereas 511 were DILI negatives" (abstract); columns `DILIST_ID`, compound name, `DILIst Classification` (0/1), routes of administration (FDA page); no structures. Labels: "We augmented the DILIrank data set [annotated using US Food and Drug Administration (FDA) drug labeling)] with four literature datasets (N >350 drugs)" (abstract).
- Use case: DILI "is of significant concern to drug development and regulatory review because of the limited success with existing preclinical models. For developing alternative methods, a large drug list is needed" (abstract): a safety team judges a candidate's liver-injury risk from its structure before clinical exposure; fit direct. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31), as the other molecule records.
- Siblings and duplicates: `dili_xu` (`TBD -> 2nd Tier`, Xu et al. 2015, 475 drugs, TDC's DILI) has the same endpoint and is likely one of the four literature sets DILIst pooled: a version question (PROV-6) where DILIst is the larger and later list; `clintox` and `drug_induced_autoimmunity_prediction` (`Yes`) are other adverse effects (PROV-7). External collections: none found for DILIst (TDC and ChemPile carry `dili_xu`).
- Better data: found as a related task next to `drug_induced_autoimmunity_prediction`; no further search this round.
- Papers and pages: Thakkar et al. 2020; DILIrank (Chen et al. 2016, Drug Discovery Today, the labelled base); the FDA LTKB page.
- Metric: none found (the abstract and the FDA page; a list paper without a model); fallback `roc_auc` (MET-1, MET-8); inputs none.
- Risks for /add-dataset: name-to-structure mapping through PubChem by us (salts, mixtures and biologics without a SMILES drop out) and descriptors computed by us (CLEAN-24); labels pooled from five sources with different criteria, and how DILIrank's ambiguous drugs were handled is to check; overlap and conflicting labels with `dili_xu` (PROV-6); the route of administration is known at design time and stays.
- Priority: gap 0 (medical & healthcare, binary, grouped not thin), use case + (drug development and regulatory review named), source + (FDA page and paper), shape + (1,279 drugs, descriptors and route), risk - (structures mapped by us, pooled labels): 3.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `drug_induced_autoimmunity_prediction`.
- as published: 1,279 drugs: 768 DILI positive, 511 DILI negative (FDA page). Columns: DILIST_ID, compound name, classification, routes of administration. No structures, so the SMILES must be mapped from PubChem by ...; target: DILI positive or negative in humans (FDA labels and DILIrank, extended with four literature sets); access: open.
- Why: The same kind of task as drug_induced_autoimmunity_prediction: a drug-level human adverse-effect label predicted from chemical structure (RDKit descriptors), under a scaffold-grouped split. It comes from a regulator's curated list.
- Adds: 1,279 drugs against 587, with a regulator-curated label. A different adverse effect (hepatotoxicity), so it is its own record, not a better version of the autoimmunity one. Build risk: name-to-structure mapping and descriptors computed by us, where InterDIA shipped its own.
