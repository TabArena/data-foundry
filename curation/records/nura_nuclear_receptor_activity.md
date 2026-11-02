---
unique_name: nura_nuclear_receptor_activity
name: 'NURA: NUclear Receptor Activity dataset'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2020'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.3999420
- https://doi.org/10.1016/j.taap.2020.115244
- https://michem.unimib.it/download/data/nura/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: a curated set of 15,247 molecules with active, weakly active, inconclusive or inactive calls on 33 endpoints (agonism, antagonism and binding on 11 nuclear receptors), merged from Tox21, ChEMBL, NR-DBIND and BindingDB; a real endocrine-activity screen, but one endpoint has to be chosen and its Tox21 part overlaps the `tox21` records.
- Source: Valsecchi, Grisoni, Motta, Bonati and Ballabio, "NURA: A curated dataset of nuclear receptor modulators", Toxicol. Appl. Pharmacol. 407:115244 (2020, doi 10.1016/j.taap.2020.115244, PMID 32961130); data on Zenodo (doi 10.5281/zenodo.3999420, v1.0.1, published 2020-08-19, CC BY 4.0; the paper cites doi 10.5281/zenodo.3991561). As published (file preview): `NURA_v1.0.0.csv` (3.8 MB), one row per molecule with `NURA_ID`, `Canonical SMILES`, 33 label columns `AGO_<NR>`, `ANT_<NR>`, `BIN_<NR>` for PR, PXR, RXR, GR, AR, ERA, ERB, FXR, PPARD, PPARG and PPARA, each `act.`, `w.act.`, `inc.`, `inact.` or `n.a.`, and `SOURCES`; `NURA_v1.0.0_details.csv` (27.7 MB) holds the underlying records, and the KNIME curation pipeline ships too. Abstract: "bioactivity annotations for 15,247 molecules and 11 selected NRs", meant to support decision-making in pharmacology and toxicology and machine learning.
- Use case: a regulatory toxicologist or a medicinal chemist screens a new chemical for agonism or antagonism on a nuclear receptor (endocrine disruption, off-target activity) before testing it in vitro; fit approximate, since the calls merge in-vitro assays of four sources and the paper names decision-making only in general. Regime grouped on the Bemis-Murcko scaffold, because the rows are exact structures (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: `tox21` (`TBD -> Yes`, priority 3) and its cuts `tox21_challenge`, `tox21_challenge_2014`, `tox21_nr_ahr`, `tox21_sr_mmp` hold the Tox21 qHTS calls, one of NURA's four sources. NURA's harmonised labels, its eight receptors outside the Tox21 panel (PR, PXR, RXR, GR, ERB, FXR, PPARD, PPARA) and its agonist, antagonist and binder modes make it a distinct task (PROV-7), but an endpoint shared with Tox21 (AR, ERA or PPARG agonism) would overlap in compounds. `chembl206_estrogen_receptor` (`TBD -> 2nd Tier`) is a ChEMBL potency regression on ER alpha. The run's note that NURA subsumes the group's CoMPARA androgen receptor set (UCI 509) was not checked; no record holds that set. External collections: none found.
- Better data: from the curator's Zotero collection, item 137; no new search this run.
- Papers and pages: the TAAP paper (abstract read, full text paywalled); Valsecchi et al., "Predicting molecular activity on nuclear receptors by multitask neural networks", J. Chemometrics 36(2), 2022 (doi 10.1002/cem.3325), which modelled 30 binary tasks on 14,963 NURA molecules (not read: the accepted manuscript returned 403); the michem.unimib.it pages returned 503.
- Metric: none found (the Zenodo record and the PubMed abstract; the 2022 modelling paper not read), so the fallback `roc_auc` on one binary endpoint (MET-1, MET-8); inputs none.
- Risks for /add-dataset: choose one endpoint (or a few as separate tasks; `Multi-target` only if shipped together, CLEAN-18) and how `w.act.` and `inc.` map to the label (USE-5); many `n.a.` cells per endpoint, so count the labelled molecules and the actives per scaffold-grouped fold (TP-5); compounds shared with the Tox21 records for an overlapping endpoint (PROV-6); salts and repeated structures across the four sources (LEAK-19); the SMILES ship as RDKit descriptors (CLEAN-24).
- Priority: gap 0 (chemistry & material science, binary and grouped are not thin), use case 0 (the decision is named only in general, approximate fit), source + (a peer-reviewed data paper, Zenodo with the curation pipeline), shape + (15,247 molecules, exact structures), risk - (an endpoint to choose and the Tox21 overlap).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 137: "Data".
- as published: molecules, 15,247 rows (SMILES) x 11 nuclear receptors, agonist/antagonist/binder annotations from Tox21, ChEMBL, NR-DBIND, BindingDB; target: active vs inactive per receptor and mode (e.g. AR antagonist, ER agonist), classification; access: open.
- Why: curated, CC BY, large; SMILES go to RDKit descriptors as in CLEAN-24
- Adds: endocrine-disruption task; subsumes the group's smaller AR CoMPARA set (UCI 509, 1,687). Needs one receptor/mode chosen as the task; many labels missing per receptor
