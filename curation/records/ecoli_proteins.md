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

CC (2026-11-16, Andrej): tag `Expanding Science Catalogue`: the rows are a cut of SWISS-PROT, a sequence database that keeps growing, as splice's windows are a cut of GenBank. The time basis is open in the Review (issue 1).

## Review

**Outcome:** added. UCI's E. coli protein localization data (Horton and Nakai 1996; UCI 39,
https://doi.org/10.24432/C5388M): proteins annotated in SWISS-PROT up to 1996, five scores computed from each sequence,
and the cell location; the five locations with 10 or more proteins are kept (327 proteins); random split, log loss
(fallback). Its SWISS-PROT entry names date the proteins (CC of 2026-11-16), so the split is read again (issue 1).

**Main points:** Open: which key splits the proteins now that their entries are dated (issue 1).

**Record judgment:** valid. `Samples: Over Time`, `Time: Dated` and `Expanding Science Catalogue` added on 2026-11-16.

**Issues for Andrej:**

1. **Which key splits ecoli now that its entries are dated: the entry date, the protein family, or random as now?**

   * **Problem:**
     - The definition names `Timeless` and splits at random because "the release holds no date", but the raw file's
       SWISS-PROT names date 309 of the 336 entries (1986 to 1995), so the catalogue split rule reads the split[^1a].
     - The use case predicts the location of a newly sequenced protein, and the source names no narrower scope: the
       test set stands for proteins the catalogue did not hold yet.
     - The rule's default is a family key (a protein family the actor has not met); the entry date replaces it when
       arrival changes which items the catalogue takes in, or when the date carries waves.
   * **Experiments:** the UniProt lookup of 2026-11-16 (record CC); the location mix of the five kept locations moves
     with the entry date (chi-squared p = 0.005):

     | Entered SWISS-PROT | Proteins | Cytoplasm | Inner membrane | Periplasm | Inner membrane, uncleavable signal | Outer membrane |
     |---|---|---|---|---|---|---|
     | up to 1989 | 152 | 54% | 18% | 11% | 9% | 8% |
     | 1990 to 1996 | 145 | 34% | 26% | 20% | 14% | 6% |

   * **Effect on the task:** a random split trains on proteins entered after the test proteins, and the later entries
     hold more membrane and periplasmic proteins than the earlier ones.
   * **Unknown:** the date of the 27 entries renamed since 1996 (they existed by then); 59 entries are dated only "by
     November 1988", UniSave's first release; the share of close training neighbours under each key (the rule's
     measurement), which needs the sequences from UniProt.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, `Timeless` (implemented) | keeps the split; the `Time basis:` line names the dates | no change | `Timeless` is for a catalogue no source dates, which this one is not |
     | B | Protein family, `UnseenGroup` | groups by a homology cluster (for example UniRef50) looked up for each entry | the rule's default; tests families not seen | ignores the move in the location mix |
     | C | Entry date | yearly windows on the SWISS-PROT entry date, the 27 undated entries in training only | tests the proteins that entered later; the mix moves with the date, the rule's case for the date | 327 proteins over 1986-1995 make few, small windows |

   * **Recommendation:** C: the use case reaches later proteins, and the location mix moving with the entry date is
     the rule's case for the date; the windows are checked against the minimum test size before the change.
     **Decision:** A, B or C?

   **Notes for the AI:** on C, add the entry dates as a raw helper file with its lookup (UniProt creation date, UniSave
   first release of a merged accession), a `Temporal(feature=False)` split on the entry year, and a `Time basis:` line;
   on B, look up a UniRef50 cluster per accession and group on it, time basis `UnseenGroup`; on A, rewrite the
   `Time basis:` line. `dataset check` after each; rebuild only on ask.

   [^1a]: The expanding-catalogue split rule (SPLIT-34, Should): the item key always holds; the family key is the
     default; the source's purpose sets which items the test set stands for; the entry date replaces the family key
     when the use case predicts for items the catalogue does not hold yet and arrival changes which items are selected
     or the date carries waves.

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
