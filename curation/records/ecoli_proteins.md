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
decision_markers:
- Outdated
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Dated'
- Expanding Science Catalogue
collections:
- TabArena Reject
original_source: UCI
year: '1996'
collection_period: 1986-1995
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
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

CC (2026-10-19, Andrej): Keep, with `aac` dropped (stratified 3-fold x 20).

Changed:
- Dropped `aac` (in `dataset.py`): a leak, as in `yeast` (crit. 4D). It is a discriminant-analysis score (linear classifier fitted to the labels) separating outer-membrane from periplasmic proteins, fitted on the authors' database that preceded this dataset (Nakai & Kanehisa 1991). Without it, outer-membrane (`om`) recall falls from 0.90 to 0.02 and TabPFN log loss rises from 0.359 to 0.462.
- Marker `Outdated`: the features are 1996 scores from older sequence programs; today's localisation tools work from the sequence itself.

Noted, no action (not severe):
- Arbitrary labels: `im` vs `imU` (inner membrane without/with an uncleavable signal sequence, a sorting tag at the protein's start) causes over half the errors and log loss; the authors call the split "somewhat arbitrary" (Horton & Nakai 1997). A noise floor shared by all models.
- Without `aac`, no feature identifies `om` (6% of rows), and TabPFN (0.462) beats LR (0.476) on only 68% of splits. A shared floor, and models are still ranked.
- Labels: 283 of 287 proteins keep their location in today's UniProt; 27 of 336 names no longer resolve.
- `lip` is constant in 324 of 327 rows. Kept: a real, if weak, feature.

References: Nakai K, Kanehisa M. Expert system for predicting protein localization sites in gram-negative bacteria. Proteins. 1991;11(2):95-110. doi:10.1002/prot.340110203. Horton P, Nakai K. Better prediction of protein cellular localization sites with the k nearest neighbors classifier. Proc Int Conf Intell Syst Mol Biol. 1997;5:147-152. PMID: 9322029.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Horton & Nakai 1996 report cross-validated accuracy over 8 sites, a field habit without costs, and we keep 5 of the 8 sites (MET-6, MET-2).

CC (2026-11-06, Andrej): time basis `Timeless` (Review issue 1, B): a protein's location is a property of the protein and the scores are computed from its sequence; the 1996 release was taken to hold no date. Replaced on 2026-11-20 by `StationaryRelation` (Review issue 4, D), once the entries were dated.

CC (2026-11-11, Andrej): Review issue 2, A: ecoli_proteins stays without `aac` (327 rows, five sequence scores), and LEAK-27 is amended in place: a feature fit by a supervised transform on the whole labelled set is dropped and the task kept when the other columns still make a real one; `Data Quality Issue`, `No` only when the transform runs through the columns the task needs or the task rests on it (leak_checks.md with its Mechanisms row, the principles.md conflict row, selection.md, verification.md). yeast gets a re-check question on its record.

CC (2026-11-16, Andrej): collection facts `Samples: Over Time` and `Time: Dated` instead of `Samples: No Time Dimension`. The rows are a cut of SWISS-PROT, a sequence database that kept growing, and the raw file's first column, the sequence name the definition drops, is each protein's SWISS-PROT entry name, which UniProt dates (lookup of 2026-11-16 through UniProt's REST API and its entry history, UniSave):

| Entry name in UniProt | Rows | Date used |
|---|---|---|
| Current entry | 153 | the entry's creation date |
| Merged into a new accession in 2005 | 156 | the first Swiss-Prot release of the old accession |
| Renamed since 1996, not resolved | 27 | none |

- The entries span 1986 to 1995; four were re-accessioned after the UCI donation of 31 August 1996. 59 dates fall on release 9.0 of 1 November 1988, the first release UniSave holds, so those entries were in SWISS-PROT by then.
- The location mix moves with the entry date. Of the five locations the definition keeps, the cytoplasm holds 54% of the 152 entries up to 1989 and 34% of the 145 from 1990; the inner membrane rises from 18% to 26% and the periplasm from 11% to 20% (chi-squared p = 0.005).
- The definition's time basis (`Timeless`, which rests on "the release holds no date") is open: it follows from the expanding-catalogue split rule once the record carries that tag.

CC (2026-11-16, Andrej): tag `Expanding Science Catalogue`: the rows are a cut of SWISS-PROT, a sequence database that keeps growing, as splice's windows are a cut of GenBank. The time basis is open in the Review (issue 3).

CC (2026-11-20, Andrej): random folds tagged `StationaryRelation` on the entry years (Review issue 4, D): the relation measures flat across the entry-year periods; the `Timeless` line, false since the entries are dated, is replaced.

CC (2026-11-23, Andrej): 20 x 3 folds grouped by protein family, `UnseenGroup` (Review issue 5, C): entry-year windows would need the 37% exception, so the catalogue's family key decides. `protein_families.csv` maps the 327 proteins to 219 families (UniProt protein family, else Pfam domains, else the protein alone for 18 unresolved entries). Holding out families costs +0.012 to +0.015 log loss for TabPFN and logistic regression, the ranking unchanged. Ecoli leaves the departures table. `dataset check`: 0 errors, 0 warnings (one fold without the outer-membrane location accepted). Not rebuilt.

## Review

**Outcome:** added. UCI's E. coli protein localization data (Horton and Nakai 1996; UCI 39,
https://doi.org/10.24432/C5388M): proteins annotated in SWISS-PROT up to 1996, five scores computed from each sequence,
and the cell location; the five locations with 10 or more proteins are kept (327 proteins); random split, log loss
(fallback). `aac`, a discriminant score fitted to the labels of the authors' earlier database, is dropped and the rule
on fitted scores amended to keep such a task (issue 2). Its SWISS-PROT entry names date the proteins (CC of
2026-11-16), so the split is read again (issue 3).

**Main points:** All issues settled. ecoli is kept without `aac` and LEAK-27 amended (issue 2, A, 2026-11-11; yeast
gets a re-check question on its record). The random split was named `Timeless` (issue 1, B, 2026-11-06); once the
entries were dated, the 20 x 3 random folds stay, tagged `StationaryRelation` on the SWISS-PROT entry years (issue 4,
D, 2026-11-20, which also settles issue 3). Since 2026-11-23: folds grouped by protein family, `UnseenGroup`
(issue 5, C).

**Record judgment:** valid. `Samples: Over Time`, `Time: Dated` and `Expanding Science Catalogue` added on 2026-11-16.
The comment of 2026-10-19 names `aac` "a leak, as in `yeast`" and keeps the dataset; issue 2 closes the gap to the
rule that gave yeast `No` for the same kind of column.

**Issues for Andrej:**

1. **Time basis: name the random split `Timeless`, as a protein's location is a fixed property?**

   * **Problem:**
     - The five kept scores are computed from the amino-acid sequence, which exists before any localisation
       experiment, and the location is a property of the protein, so nothing in a row arrives after another part.
     - The record carried `Samples: No Time Dimension` with no time or target fact, and the definition named no time
       basis, although the proteins were characterised over the decades up to 1996.
     - `Timeless` is the prototype for a target that is a fixed property of the item; what no split here can test is a
       protein of a family the 1996 catalogue did not yet hold[^1a].
   * **Background:**
     - The release has no date: UCI donated it on 31 August 1996, the annotations come from SWISS-PROT, and the only
       per-protein identifier, the accession, is dropped as an identifier.
     - The raw order is one block per location (consecutive rows share the label far above chance, p 3.5e-155), so the
       order is the label and not a collection order.
     - Annotations are revised after a release, not within the task: 283 of the 287 proteins that still resolve keep
       their location in today's UniProt (4 differ, and 27 of 336 names no longer resolve).
   * **Effect on the task:** none on the data, split or score; the line states why a random split over proteins is
     safe in time, and what it cannot test.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time basis (implemented) | as then | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random split, `Timeless` | the tag and a `Time basis:` line naming the sequence-only scores, the fixed location and the 1996 catalogue | states the fact the split rests on; names what the split cannot test | none found; no data, split or score changes |
     | C | Random split, `StationaryRelation` | the tag for a present state read through a relation time does not move, argued from the source | fits a label read off an experiment | the location is a property of the protein, not a state of it |

   * **Recommendation:** B. **Decision:** A, B or C?

   [^1a]: **SPLIT-32** (Should), as worded then: `Timeless`: the target is a fixed property of the item, the same
     whenever it is measured; `StationaryRelation`: the target is a present state read through a relation that time
     does not move, measured on a dated source and argued where the time is lost.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept five more routine `Timeless`
   issues with one mark?" A `Time basis: Timeless:` line, ending with what the split cannot test (a protein of a family
   the 1996 database did not hold, and homologous proteins on both sides of the split); the split unchanged. Replaced
   on 2026-11-20 by issue 4 (D, `StationaryRelation`), once the SWISS-PROT entry names dated the proteins.

2. **Keep ecoli with `aac` dropped, which needs an amendment of the rule on fitted scores, or retire it as the rule is
   written?**

   * **Problem:**
     - Your review of 2026-10-19 dropped `aac`, a score fitted to the labels of the authors' earlier protein database,
       and kept the dataset.
     - The rule on fitted scores, as written, gives a dataset with such a column `No`, which is how Lennart retired
       yeast, the sibling dataset of the same authors, for a score of the same kind[^2a].
     - A strict rule takes no exception, so keeping ecoli needs the rule amended, or ecoli is retired as the rule
       stands[^2b].
   * **Background:** `aac` is the "score of discriminant analysis of the amino acid content of outer membrane and
     periplasmic proteins" (UCI): a linear classifier that Nakai and Kanehisa fitted on "our database", which UCI calls
     the predecessor of this dataset (Nakai K, Kanehisa M. Expert system for predicting protein localization sites in
     gram-negative bacteria. Proteins. 1991;11(2):95-110. doi:10.1002/prot.340110203). It cannot be refitted per split,
     so it carries the labels of test proteins. The rule that a leak is fixed and the task kept names the fitted score
     as its limit[^2c]; but here the score is one column, and dropping it removes it.
   * **Effect on the task:** without `aac`, outer-membrane proteins (6% of rows) are barely recognised, and the score
     rests more on the inner-membrane boundary. The question is consistency: the same leak, two verdicts.
   * **Experiments:** 60 stratified splits (3 folds x 20, the shipped seed), untuned models:

     | Features | TabPFN log loss | Logistic regression log loss | Outer-membrane recall (TabPFN / LR / RF) | TabPFN beats LR |
     |---|---|---|---|---|
     | with `aac` | 0.359 | 0.393 | 0.90 / 0.88 / 0.86 | 83% of splits |
     | without `aac` | 0.462 | 0.476 | 0.02 / 0.04 / 0.17 | 68% of splits (mean gap 0.014) |
     | `aac` alone | | 1.19 | LR 0.71 | |

   * **Kept on purpose:** (your comment of 2026-10-19, "not severe") the inner-membrane classes `im` and `imU` cause
     over half the errors, and the authors call the split "somewhat arbitrary" (Horton P, Nakai K. Better prediction of
     protein cellular localization sites with the k nearest neighbors classifier. Proc Int Conf Intell Syst Mol Biol.
     1997;5:147-152. PMID: 9322029); nothing identifies outer-membrane proteins once `aac` is gone.
   * **Consistency:** departs from yeast (`No`, Lennart, 2026-07-27: "Confirmed leak"). Dropping a column fitted to the
     labels and keeping the task is how qsar_bioconcentration (the authors' 9 descriptors, 2026-10-26) and
     numerai_v5_2_1m (the Faith features) were decided under the rule on feature selection[^2d], and kickstarter
     (`staff_pick`) under the fix-the-leak rule.
   * **Unknown:** how many of the 336 proteins were in the database `aac` was fitted on (the 1991 paper is
     paywalled); whether yeast's other columns make a real task under the amended rule (not re-read).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep without `aac`, amend the rule | 327 rows, 5 scores; the rule says to drop a fitted column and keep the task when the other columns still make a real one; yeast is re-checked under it | follows your keep of 2026-10-19; follows the fix-the-leak rule; in line with the feature-selection cases | one more record (yeast) to look at; outer-membrane proteins barely recognised |
     | B | Retire as the rule is written | record `No (Retired)` with `Data Quality Issue`; folder removed | consistent with yeast without touching the rule | undoes your keep; a valid task leaves for a column it no longer has |

   * **Recommendation:** A. **Decision:** amend the rule and keep ecoli (A), or retire it as the rule is written (B)?

   [^2a]: **LEAK-27** (Must), as worded then: a feature that is the output of a supervised transform fit on the whole
     labelled set (a discriminant score, a target encoding, a model's prediction) is irreversible: `Data Quality
     Issue`, `No`. Case: yeast's discriminant-analysis score.
   [^2b]: principles.md, "Exceptions and amendments": a Must has no exceptions; only a higher-ranked Must overrides
     it, and anything else is an amendment, which replaces the rule's text in place.
   [^2c]: **USE-12** (Must): a leak in the features is no reason to reject a task whose use case is real; the remedy
     is to fix it and keep the task. The principles' table of conflicts named the fitted score (LEAK-27) as its limit.
   [^2d]: **LEAK-31** (Should): supervised feature selection on the full labelled set is measured, kept with a note
     when small and removed when we can.

   **Resolved (2026-11-11, Andrej):** A (`ok`): ecoli ships without `aac`; LEAK-27 is amended in place (drop a single
   fitted column and keep the task when the other columns still make a real one; `No` when the transform runs through
   the columns the task needs) in leak_checks.md, its Mechanisms row, the principles.md conflict row, selection.md and
   verification.md; a re-check question is on yeast's record; the aac bullet in `curation_comments` names the rule.

3. **Which key splits ecoli now that its entries are dated: the entry date, the protein family, or random as now?**

   * **Problem:**
     - The definition names `Timeless` and splits at random because "the release holds no date", but the raw file's
       SWISS-PROT names date 309 of the 336 entries (1986 to 1995), so the catalogue split rule reads the split[^3a].
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

   [^3a]: The expanding-catalogue split rule (SPLIT-37, Should): the item key always holds; the family key is the
     default; the source's purpose sets which items the test set stands for; the entry date replaces the family key
     when the use case predicts for items the catalogue does not hold yet and arrival changes which items are selected
     or the date carries waves.

   **Resolved (2026-11-20, Andrej):** settled by issue 4 (D): the 20 x 3 random folds stay, tagged `StationaryRelation`, as the stationary-relation test on the entry years reads flat (narrowly).

4. **Windows on the entry year, now that the proteins are dated?**

   * **Problem:**
     - Since 2026-11-16, 309 of 336 entries carry their SWISS-PROT entry year (1986-1995), and the mix of locations moves with it (cytoplasm 54% of entries up to 1989 against 34% from 1990, p = 0.005), which the catalogue rule counts as arrival changing which items are taken in[^s37a].
     - Three windows (test 1989-90, 1991-92, 1993-96) train on 37%, 60% and 77% with 76, 56 and 46 test proteins: enough for the three-window floor with your sign-off on the 37% window, not for the 60 splits of your window-count reading.
     - The definition still ships random folds tagged `Timeless` on the line "the release holds no date"; the record's issue 3 asked this and has no mark.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 20 x 3 random folds, `Timeless`, the present line (implemented) | No change | 60 splits | Its line is false; no leaf gives it with dated entries |
     | B | Three windows on the entry year | The 27 undated entries train only; the year no input; the 37% window signed off | Tests proteins entered later, as the use case meets them | 46-76 test proteins per window |
     | C | The same random folds, `Timeless` (no family key), line rewritten | The line names the dating, the shifted intake and the family the use case would hold out | 60 splits | Only open with option B of the window-count item |

   * **Recommendation:** B with option A of the window-count item, C with its option B. **Decision:** A, B or C?

   **Notes for the AI:** this replaces the record's issue 3; tree: ecoli leaves the departures on B or C.

   [^s37a]: **SPLIT-37** step 4 (Should): the entry date replaces the family key when "(a) arrival changes how the target or the features are recorded, or which items are selected ...: descriptors computed by another convention in a later round, a programme that changed which items it takes in".

   **Andrej (2026-11-19, discuss):** Can we measure stationarity?

   **Answer (AI, 2026-11-19):** measured: flat, narrowly. On the entry-year periods, a model trained on earlier entries predicts the location about as well as one trained on the period's own entries; the location mix moves, but the six sequence scores predict it the same way.

   * **The test:** 297 dated proteins (30 left out: 26 renamed and unresolved, 4 dated after the UCI donation), six features, log loss, 5 seeds; periods up to 1988, 1989-90, 1991-92, 1993-96.

     | Test period | Train share | LightGBM gap | Kumo-Tabular gap | Floor | Verdict |
     |---|---|---|---|---|---|
     | 1993-96 (46) | 77% | -0.072 ± 0.033 | +0.004 ± 0.021 | 0.009 | flat |
     | 1991-92 (56) | 60% | +0.095 ± 0.098 | +0.096 ± 0.092 | 0.010 | inconclusive |
     | 1989-90 (76) | 37% | +0.012 ± 0.094 | +0.003 ± 0.033 | 0.011 | flat (Kumo-Tabular) |
     | pooled, all three | | +0.012 ± 0.047 | +0.034 ± 0.033 | | flat |
     | pooled, the two at half or more | | +0.011 ± 0.052 (2 SD 10.8 floors) | +0.050 ± 0.047 (9.8 floors) | | flat (Kumo-Tabular) |

   * The location mix moves (outer membrane 8.4% against 3.6%, factor 2.4, p 0.39; cytoplasm 54% against 34%, under twofold): not a recording change by the rule.
   * **What it means:** three windows exist only with the 1989-90 window at 37% as your exception (B). Without it, two windows are too few, the forced step reads the test, and it reads flat: the random folds tagged `StationaryRelation` on this test (new option D), replacing the false `Timeless` line. The evidence is thin (297 proteins; the two-period pooling passes at 9.8 floors).

   | | Option | Splits | Tag |
   |---|---|---|---|
   | A | 20 x 3 random folds (implemented) | 60 | `Timeless`, line "the release holds no date" (false) |
   | B | Three windows on the entry year, 1989-90 at 37% as your exception | 3 | none (temporal) |
   | D | 20 x 3 random folds | 60 | `StationaryRelation` on this test, the dating in the line |

   **Recommendation:** D: the windows would need a 37% exception and hold 46-76 proteins each, while the relation measures flat. **Decision:** A, B or D?

   **Andrej (2026-11-20, discuss):** Reply (D): 20 x 3 random folds

   **Resolved (2026-11-20, Andrej):** D. The 20 x 3 random folds stay; `data_tags` reads `StationaryRelation` instead of `Timeless`, and the `Time basis:` line gives the SWISS-PROT entry years and the stationary-relation test (flat, narrowly). `dataset check`: 0 errors, 0 warnings. Not rebuilt.

5. **Keep the random folds tagged `StationaryRelation` in a catalogue, where the rules do not reach that tag?**

   * **Problem:**
     - In an expanding catalogue whose arrival changes which items are taken in, the entry date splits, and three windows on it need the 1989-90 window at 37% as your exception[^dep-cat].
     - Without the exception the catalogue goes on to the family key, not to the forced step, so `StationaryRelation` is no outcome of the catalogue's walk[^dep-fam].
     - The split tree lists ecoli as a departure that rests on a flat relation; Lennart asked on 2026-11-23 that you make this call.
   * **Background:** the run of 2026-11-19 (issue 4), log loss, 5 seeds, 297 dated proteins.

     | Test period | Train share | Test proteins | Kumo-Tabular gap | Floor | Verdict |
     |---|---|---|---|---|---|
     | 1993-96 | 77% | 46 | +0.004 ± 0.021 | 0.009 | flat |
     | 1991-92 | 60% | 56 | +0.096 ± 0.092 | 0.010 | inconclusive |
     | 1989-90 | 37% | 76 | +0.003 ± 0.033 | 0.011 | flat |

   * **Effect on the task:** the random folds keep the shifted intake (cytoplasm 54% of entries up to 1989 against 34% from 1990) on both sides, and proteins of one family on both sides as well.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 20 x 3 random folds, `StationaryRelation` (implemented) | No change; the tree's departures table keeps ecoli with your reason | 60 splits; no rebuild | A tag the catalogue's walk does not reach |
     | B | Three windows on the entry year, 1989-90 at 37% as your exception | The 27 undated entries train only; the year is no input | The leaf the tree gives; tests proteins entered later | 46 to 76 test proteins per window; the exception is yours to allow |
     | C | Folds grouped by protein family, `UnseenGroup` | A homology cluster (for example UniRef50) looked up for each resolved entry | The catalogue's default key without the exception; tests families not seen | The 27 unresolved entries need a key; ignores the shifted intake |
     | D | 20 x 3 random folds, `Timeless` (no family key) | The line names the dating, the shifted intake and the family the use case would hold out | The family-key leaf when no key can be computed; 60 splits | Only right if no family key can be computed |

   * **Recommendation:** none from the AI beyond what the rules give as written: B if you allow the 37% window, else C where a family key can be computed and D where it cannot; A stays only as a departure you confirm with its reason. **Decision:** A, B, C or D?

   **Notes for the AI:** B as issue 4's option B. C needs the homology lookup and a `Grouping` on the cluster; D sets `TimeBasis("Timeless", ...)`. A: the reason goes into the departures table of `split_tree.md`. On B, C or D ecoli leaves that table.

   [^dep-cat]: **SPLIT-37** step 4 (Should): the entry date replaces the family key when the use case predicts for items the catalogue does not hold yet and "(a) arrival changes how the target is recorded, or which items are selected". **SPLIT-14** (Must): "A temporal task has at least 3 windows (splits). Every window trains on at least 50% of the data. A window under 50% is the curator's exception for that dataset, down to 30%".
   [^dep-fam]: The split tree, Expanding science catalogue: "Can the order hold at least three test windows of the use case's size? ... no → ① family-key step". **SPLIT-37** step 2 (Should): the family key is a catalogue's default split; without one the split is `Timeless`.

   **Family check (AI, 2026-11-23):** the shipped proteins mapped through UniProt (REST, 2026-11-23) and grouped three ways; 20 x 3 folds, features without `aac`, log loss (mean ± SE; accuracy in brackets).

   | Key | Resolved | Groups | Largest | Logistic regression | TabPFN |
   |---|---|---|---|---|---|
   | random folds | | | | 0.472 ± 0.007 (0.833) | 0.463 ± 0.009 (0.832) |
   | UniRef90 | 309 | 326 | 2 | 0.471 (0.837) | 0.453 (0.831) |
   | UniRef50 | 309 | 319 | 3 | 0.483 (0.830) | 0.464 (0.831) |
   | UniProt family, else Pfam domains | 309 | 219 | 12 | 0.487 ± 0.007 (0.829) | 0.475 ± 0.009 (0.826) |

   Family minus random, paired: logistic regression +0.015 ± 0.004, TabPFN +0.012 ± 0.005; with `aac` logistic regression +0.008 ± 0.005. Under random folds 41% of the test proteins (44 of 109 per fold) have a family member in training and carry 33% of TabPFN's loss (0.376 against 0.523 for unseen families). The 18 unresolved entries count as their own groups.

   **Resolved (2026-11-23, Andrej):** C, folds grouped by protein family. `Grouping(on="protein_family")` from `protein_families.csv` next to the definition (UniProt protein family 270, Pfam domains 39, the protein alone 18; 219 groups), `TimeBasis("UnseenGroup", ...)` with `StationaryRelation` noted as before, splits comment and notes with the check above; `required_split` Grouped; the row leaves the departures table. `dataset check`: 0 errors, 0 warnings (`splits_test_class_missing` accepted: one fold lacks the outer-membrane location, which log loss tolerates). Not rebuilt.

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
