---
unique_name: ready_biodegradability_mansouri_external
name: Ready biodegradability external validation set (Mansouri et al. 2013)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Other
year: '2013'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- '# The paper the set is published with; the data is sheet `External validation` of its supporting information `ci4000213_si_001.xlsx`'
- https://doi.org/10.1021/ci4000213
- https://pubs.acs.org/doi/suppl/10.1021/ci4000213/suppl_file/ci4000213_si_001.xlsx
- '# The chemicals'' own sources, per Chakravarti and Alla 2018 (arXiv 1808.04456)'
- https://doi.org/10.1021/ci200622d
- https://www.canada.ca/en/environment-climate-change/services/canadian-environmental-protection-act-registry/substances-list/domestic.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-02):** `TBD -> 2nd Tier`, priority 2: the 670-chemical external validation set
published with `qsar_biodeg`'s paper, the same task on chemicals from different sources, 657 of them new to that
dataset; worth having, but a 2022 compilation nine times its size already has a record. Screened on the curator's
ask after `qsar_biodeg`'s run of 2026-11-01 noted it.
- Source: Mansouri, Ringsted, Ballabio, Todeschini and Consonni, "Quantitative Structure-Activity Relationship Models
  for Ready Biodegradability of Chemicals", J. Chem. Inf. Model. 53(4):867-878, 2013 (doi 10.1021/ci4000213), the
  `External validation` sheet of the supporting information `ci4000213_si_001.xlsx`. The chemicals are not the
  paper's own collection: "The training/validation dataset was curated from MITI. The test set was constructed from
  two data sources, Cheng et al. and the Canadian DSL database" (Chakravarti and Alla, arXiv 1808.04456, Table 1,
  read 2026-11-02; its counts, 356/699 and 191/479, match the sheets exactly). As published: 670 rows x 44 columns -
  CAS-RN, SMILES, the class, and the same 41 Dragon descriptors as the 1,055-chemical sheet; one table.
- Use case: a regulator or a chemical manufacturer screens a chemical's structure to decide whether it needs a
  ready-biodegradability test, or to rank candidates before one; the same actor and moment as `qsar_biodeg`, which
  the curator accepted. Fit direct: the structure is all that is known before the test, and the label is the test's
  outcome. Regime grouped on the Bemis-Murcko scaffold (SPLIT-31), because a screener meets chemicals of series not
  yet tested, as all five sibling molecule datasets are split.
- Siblings and duplicates: `qsar_biodeg` (`Yes`, TabArena v0.1; Mansouri's other sheet, 1,055 chemicals from
  NITE/MITI), `qsar_biodegradation` (`No`, `Duplicate`: the UCI copy of that), `ready_biodegradability_huang_zhang`
  (`TBD -> Yes`, priority 2; about 6,139 chemicals from REACH). Not a duplicate of `qsar_biodeg` under PROV-4: the
  publication is the same but the chemicals come from other sources, and the overlap is small - 13 of 670 CAS
  numbers and 8 of 670 canonical structures, one of the 8 carrying the opposite class (measured 2026-11-02 on the
  workbook already in the warehouse). External collections: none found.
- Better data: `ready_biodegradability_huang_zhang`, the same target and use case on about 6,139 chemicals from
  REACH dossiers (2022), nine times this set and newer; it already has a record, found as better data for
  `qsar_biodeg` on 2026-10-31. Koerner et al. 2024 (doi 10.1039/d4em00431k) publish a label-noise-curated version of
  that one. No further search this round.
- Papers and pages: the 2013 paper above; Chakravarti and Alla 2018 (arXiv 1808.04456) and the OPERA R-Biodeg QMRF
  use this set as the external test set. The curated sibling literature is on `ready_biodegradability_huang_zhang`.
- Metric: the paper reports the error rate and the non-error rate with sensitivity and specificity, the Milano
  group's house measure, with no decision threshold and no costs (MET-6), so the fallback `roc_auc` (MET-8), as
  `qsar_biodeg` declares. Inputs none.
- Risks for /add-dataset: 670 chemicals and one feature once the Dragon descriptors leave (CLEAN-24), below the
  "good shape" guess of about 1,000 units, though above `qsar_bioconcentration`'s 776; the 8 structures shared with
  `qsar_biodeg` and the one class disagreement need a decision if both ever ship (LEAK-19, PROV-15); 4 CAS numbers
  occur twice; the labels come from two compilations, and Koerner et al. document label noise across exactly this
  literature. The ACS supporting information states no licence and was taken from the Internet Archive, as
  `qsar_biodeg`'s was.
- Priority: gap 0 (chemistry, binary and grouped are all common among the 172 accepted records), use case +, source
  +, shape 0 (670 chemicals, one feature), risk - (better data found).

**Assessment (AI, 2026-11-02):** one framing the curator may prefer to a dataset of its own. This set is what
`qsar_oral_toxicity`'s review called an external set: chemicals for the same task, collected by other people, which
measures how optimistic our scaffold split is on `qsar_biodeg`. `qsar_oral_toxicity` is `approximate` for exactly
that reason, and `qsar_biodeg` has no such check today. Shipping it as its own small dataset and using it as that
check are not exclusive, but if only one happens, the check is the more useful. Merging the two into one 1,725-row
dataset is the option to avoid: the labels come from different compilations, which is the label noise Koerner et al.
document.
