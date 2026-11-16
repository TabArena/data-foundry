---
unique_name: ecoli_proteins
name: ecoli
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Dated'
- Expanding Science Catalogue
collections:
- TabArena Reject
original_source: UCI
year: '1996'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/ecoli/metadata.yaml
- https://doi.org/10.24432/C5388M
notebook_path: datasets/beyond_iid/new_iid/ecoli_proteins/ecoli_proteins.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ecoli_proteins/dataset.py
source_row: 754
type_adapter_id: curation-record-v1
---

## Comments

Has some minor classes that might not be dropped for proper validation setup. Might be outdated, otherwise seems to be still an okay task from the time

need to check sequence names again

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Horton & Nakai 1996 report cross-validated accuracy over 8 sites, a field habit without costs, and we keep 5 of the 8 sites (MET-6, MET-2).

CC (2026-11-16, Andrej): collection facts `Samples: Over Time` and `Time: Dated` instead of `Samples: No Time Dimension`. The rows are a cut of SWISS-PROT, a sequence database that kept growing, and the raw file's first column, the sequence name the definition drops, is each protein's SWISS-PROT entry name, which UniProt dates (lookup of 2026-11-16 through UniProt's REST API and its entry history, UniSave):

| Entry name in UniProt | Rows | Date used |
|---|---|---|
| Current entry | 153 | the entry's creation date |
| Merged into a new accession in 2005 | 156 | the first Swiss-Prot release of the old accession |
| Renamed since 1996, not resolved | 27 | none |

- The entries span 1986 to 1995; four were re-accessioned after the UCI donation of 31 August 1996. 59 dates fall on release 9.0 of 1 November 1988, the first release UniSave holds, so those entries were in SWISS-PROT by then.
- The location mix moves with the entry date. Of the five locations the definition keeps, the cytoplasm holds 54% of the 152 entries up to 1989 and 34% of the 145 from 1990; the inner membrane rises from 18% to 26% and the periplasm from 11% to 20% (chi-squared p = 0.005).
- The definition's time basis (`Timeless`, which rests on "the release holds no date") is open: it follows from the expanding-catalogue split rule once the record carries that tag.

## Reference

@inproceedings{horton1996probabilistic,
  title={A probabilistic classification system for predicting the cellular localization sites of proteins.},
  author={Horton, Paul and Nakai, Kenta},
  booktitle={Ismb},
  volume={4},
  pages={109--115},
  year={1996},
  organization={St. Louis, Missouri, USA}
}
