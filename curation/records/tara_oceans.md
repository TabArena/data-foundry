---
unique_name: tara_oceans
name: tara_oceans
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target  / Scientific Discovery
- Needs extensive data wrangling
tags:
- Many features
- AI-Filled (Verify)
collections:
- New (BeyondArena)
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
original_data_state: Database (or multiple to-be-joined tables)
source_row: 863
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

The Tara Oceans marine microbiome dataset (Science 10.1126/science.1261359), assembled by joining companion-website metadata tables (W1/W8) with a 16S OTU abundance table. As with the subseafloor records, this is a metagenomics/microbiome scientific-discovery resource with many features and heavy wrangling; the existence of a clean, deployable tabular target and adequate sample size is uncertain. The OTU/microbiome framing tends toward scientific discovery rather than representative tabular ML. A human must define a target (e.g. ocean region/depth/biome), check post-join sample size, and confirm it is not better treated as discovery.

---

World-wide sampling cruise; metadata source: http://ocean-microbiome.embl.de/companion.html ("Companion Website Tables/Tables W1-W8 (.xlsx)" -- table W1 and W8); otu table source:http://ocean-microbiome.embl.de/companion.html ("16S OTU table (*.tsv.gz)" / miTAG.taxonomic.profiles.release.tsv)

## Reference

10.1126/science.1261359
