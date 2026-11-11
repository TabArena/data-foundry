---
unique_name: apistox
name: ApisTox
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
collections:
- New (BeyondArena)
original_source: Other
year: '2024'
domain: chemistry & material science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.11062076
v2_path: datasets/_dev/tabarena-v0pt2/apistox/dataset.py
source_row: 717
type_adapter_id: curation-record-v1
---

## Comments

Contains SMILES. Authors provide custom splits: maximum diversity (MaxMin) split and a novel approximation of time split using PubChem literature data

Unclear what to do with SMILES. To correctly use this dataset, we would need to better understand the domain

**Assessment (AI, 2026-10-07):** Valid; curated as a temporal task on the first publication year (four ten-year windows), dropping `ppdb_level`, `toxicity_type` and `source` (derived from the measured LD50 or the label's database). Open question: the benchmark's default pipeline lowercases a string column and embeds it with Qwen3-Embedding-8B at 32 dimensions, which gets almost none of the structure out of a SMILES. On the four windows that embedding with the agrochemical flags and the year reaches ROC AUC 0.78-0.81, no better than the flags and the year alone (0.70-0.82), while ECFP4 bits or character n-grams reach 0.83-0.85. So either a pinned fingerprint ships with the data or the benchmark needs a SMILES encoder. The source is Zenodo, not UCI.

**Assessment (AI, 2026-10-14):** the original source is the Zenodo record (concept DOI 10.5281/zenodo.11062076); UCI 995 holds no file and links to it, so `original_source` is Other. The reference is now the published data descriptor (Scientific Data 12:5, 2025), which the definition's BibTeX cites. Licence: CC BY-NC 4.0 in the current Zenodo version, CC BY 4.0 in v1 (noted only; the licence is no verdict reason). The question "what to do with SMILES" is answered in the definition: the SMILES stays a string feature and RDKit's 2D descriptors of it are added (since 2026-10-12).

CC (2026-10-14, Lennart): Ship (review of the 2026-10-07 run).

CC (2026-10-14, Lennart): Drop the SMILES as a feature, as in every SMILES dataset; the structure ships as RDKit's 2D descriptors from one shared helper, the same tooling for all (review page, issue 1).

**Assessment (AI, 2026-10-14):** Next to the descriptors the SMILES as character n-grams adds 0.010 ROC AUC to LightGBM over the 4 windows (standard error 0.023). The definition now drops it and keeps the 199 descriptors, computed by `data_foundry.v2.rdkit_descriptors` (CHANGELOG, 2026-10-14).

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: herbicide, fungicide, insecticide, other_agrochemical and the 14 RDKit fragment counts that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: herbicide, fungicide, insecticide, other_agrochemical. Reverted: the 14 RDKit fragment counts that hold only 0 and 1 stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Adamczyk et al. 2025 (ApisTox, Scientific Data) recommend reporting AUROC and MCC together; no single deciding metric (MET-5). MCC needs a threshold the source does not fix. roc_auc is the binary fallback and the paper's threshold-free metric.

CC (2026-11-01, Lennart): SMILES ship as a typed structure column, not pre-encoded and never as text (path C of the discussion doc "SMILES Handling in Data Foundry and TabArena v0.2" (https://claude.ai/artifact/6r49WpR9Uard5ogo7qK4rB)): the benchmark encodes it; the recommended encoding in Data Foundry is RDKit's 2D descriptors with the MACCS keys.

**Assessment (AI, 2026-11-01):** the definition now ships `SMILES` (RDKit's canonical form; 17 strings change) in `smiles_columns` and no longer RDKit's 199 descriptors. The 141 salts and complexes stay as published: the largest fragment would make 86 rows copies of another, among them triclopyr and picloram triethylammonium, which both reduce to triethylamine. MACCS keys next to the descriptors: -0.006 (LightGBM) / +0.004 (random forest) ROC AUC over the 4 windows. The decade windows already keep series apart about as a scaffold split would (test compounds with a training analog at Tanimoto >= 0.7: 10-24%, against 14-19% for scaffold groups and 17-30% at random), so the temporal split stays.

## Review

**Outcome:** added. ApisTox (Zenodo 13350981): whether an agrochemical is acutely toxic to honey bees, from its
structure, its pesticide-type flags and the year it enters the literature; 1,035 compounds, four ten-year windows on
`first_publication_year`, as the authors' own time split. Opened on 2026-11-11 from the review of how catalogues of
fixed properties split: the definition splits by year while the record says the compounds have no time dimension.

**Main points:** Correct the record's collection facts, which contradict the split the definition measured and chose
(issue 1)?

**Issues for Andrej:**

1. **Correct the record's collection facts to `Samples: Over Time`, `Time: Dated` and `Target: Varying Delay`?**

   * **Problem:**
     - The record carries `Samples: No Time Dimension` and no time or target fact, while the definition splits the
       compounds into ten-year windows by the year each first appears in the literature.
     - The collection facts describe the source whatever split a definition chooses, so a catalogue whose items enter
       in eras arose over time even where each item's own value is fixed[^1a].
     - The definition's notes say bee tests of old compounds were often published decades later, so a training label
       is not always known at its window's cutoff.
   * **Background:** `first_publication_year` is the year of the earliest article PubChem links to the compound's
     CID, else the PubChem record's creation date; the four windows hold 54, 106, 118 and 173 compounds, and their
     training sides 95%, 85%, 73% and 56% of the set.
   * **Effect on the task:** none on the split, which already follows the year; the facts are what a reader checks a
     split against, and here they say the opposite of what the definition does.
   * **Consistency:** qsar_tid_11 and superconductivity were both found to be catalogues that drift and had the same
     facts questioned; this one already ships the forward split, so only the record is behind.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the facts (implemented) | no change | nothing to write | the record contradicts the definition's split |
     | B | `Samples: Over Time`, `Time: Dated` | the two facts the year column supports | matches the definition and the source's own column | the label's delay stays unrecorded |
     | C | B and `Target: Varying Delay` | also records that a bee test can follow its compound by decades | records what the notes already measured; asks for the usual check of every feature against the prediction point | a reader may read it as a censoring problem, which the windows do not show |

   * **Recommendation:** C: all three are facts of the source, and the delay is one the definition already writes
     about. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, edit `curation/records/apistox.md`: replace the `Samples: No Time Dimension` tag
   under `tags:` with `Samples: Over Time` and `Time: Dated` (and `Target: Varying Delay` on C), add a CC line with
   the reason and `Andrej` in `checked_by`. The definition needs no change: a temporal split carries no time-basis
   tag. Then `dataset check` and a CHANGELOG entry.

   [^1a]: **SPLIT-32** (Should): the curation record describes the source by collection facts, true whatever task is
     built on it; `Samples: Over Time` when the samples arose over a period, `Time: Dated` when the release or a
     parent source keeps the date, `Target: Varying Delay` when the target arrives after a delay that differs
     between samples. A catalogue whose items enter in eras arose over time even when each item's value is fixed.

   **Andrej (2026-11-11, change):** Option C: B and Target: Varying Delay.

## Reference

ApisTox: a new benchmark dataset for the classification of small molecules toxicity on honey bees
By Jakub Adamczyk, Jakub Poziemski, Paweł Siedlecki. 2024

Published in Scientific Data 12:5 (2025), doi 10.1038/s41597-024-04232-w; preprint on arXiv (2024).

CC (2026-11-11, Andrej): collection facts corrected to `Samples: Over Time`, `Time: Dated` and `Target: Varying Delay` (review issue 1, C), so that the record says what the definition's split already does.
- The definition splits the compounds into four ten-year windows by `first_publication_year`, the year the compound first appears in the literature, as the authors' own time split; the record still carried `Samples: No Time Dimension`.
- The collection facts describe the source whatever task is built on it, and a catalogue whose items enter in eras arose over time even where each item's own property is fixed.
- `Target: Varying Delay`: the curation notes record that bee tests of old compounds were often published decades later, so a label is not always known at its window's cutoff.
- The definition is unchanged: a temporal split carries no time-basis tag.
