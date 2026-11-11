# nci_aids_antiviral_screen

**Outcome:** added. The NCI Developmental Therapeutics Program's AIDS antiviral screen: the screen's conclusion for
41,140 compounds from the structure alone, grouped on the Bemis-Murcko scaffold (20,774 groups). Opened on
2026-11-11 from the review of how catalogues of fixed properties split: the compounds carry a registration number,
and whether that number is a usable time index was never tested. The AI recommends keeping the scaffold split and
correcting one collection fact.

**Main points:** Keep the scaffold split, now that a split by registration order has been measured (issue 1), and
correct the record's `Time: Dated`, since the NSC number is an order without a calendar (issue 2)?

**Issues for Andrej:**

1. **Keep the scaffold split, or split by registration order (NSC) instead?**

   * **Problem:**
     - The compounds carry the NCI's registration number, and the definition's notes already show that neighbouring
       numbers are usually analogs submitted together.
     - The use case screens compounds that have not been tested, which reads like a forward use case, so the
       registration order is a candidate time index[^1a].
     - The numbers run from 48 to 706,805, and about a quarter of the compounds sit below 609,000, registered into
       the NCI repository long before the screen began, so the order is not the order of entry into the screen.
   * **Experiments:** four test windows of about 5,140 compounds from the highest numbers down, each trained on every
     lower number (training sides 50.0%, 62.5%, 75.0%, 87.5%; 184 to 257 actives per window); on the same test
     compounds, T forward, S scaffold-disjoint at T's size drawn from all other numbers, and R random at T's size;
     untuned LightGBM and random forest on the recommended encoding; means over the four windows, with the
     shipped-like scaffold folds over all rows for reference; Slurm jobs 1377593 and 1377598:

     | Scheme | Log loss, LightGBM / RF | ROC AUC, LightGBM / RF | Close training analog | Test scaffold seen in training |
     |---|---|---|---|---|
     | T, by registration order | 0.241 / 0.241 | 0.749 / 0.774 | 8.4% | 32.5% |
     | S, scaffold-disjoint | 0.262 / 0.251 | 0.717 / 0.739 | 4.3% | 0 |
     | R, random | 0.217 / 0.226 | 0.762 / 0.770 | 9.8% | 34.9% |
     | Shipped scaffold folds, all rows | 0.187 / 0.187 | 0.786 / 0.796 | 15.4% | 0 |

     - A forward training side still holds a third of the test compounds' scaffolds, because a series was often
       registered across a wide range of numbers.
     - The newest window cannot be compared: nothing is registered after it, so its S and R pools are T's own rows.
   * **Effect on the task:** a forward split on this order leaves a third of the test compounds a training compound
     of their own series, so it does not hold out what the use case says the screener lacks, and the order it follows
     is not one the screen ever ran in.
   * **Unknown:** what calendar year each range of numbers corresponds to; no public table maps NSC numbers to
     registration dates, and PubChem's DTP records give deposit dates, not registration dates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the scaffold split (implemented) | no change; the measurement goes in the notes | holds out whole series, which the use case asks for; the registration order holds out less | the order of submission stays untested as a split |
     | B | Split by registration order | four windows on the NSC rank, the scaffold grouping dropped | follows the one order the file carries | the order is not the order of entry into the screen; it leaves a third of test scaffolds in training and scores near random |

   * **Recommendation:** A: the registration number is not an arrival time for this screen, and holding out series is
     what a screening use case needs. **Decision:** A or B?

   **Notes for the AI:** on A, add a `curation_comments` bullet with the table above next to the existing note on
   neighbouring NSC numbers, and a CC line in the record with `Andrej` in `checked_by`; scripts and results are in
   `~/claude_jobs/catalogue_splits/nci/`. On B, a `nsc_rank` column and a temporal declaration on it, the `scaffold`
   column and the grouping removed, and the windows checked against the floor that every training side holds at
   least half the rows.

   [^1a]: **SPLIT-34** (Should, proposed): in a catalogue of items with a fixed property, the item, its family and
     when it entered the catalogue hold out different things; where the actor predicts for items found later and the
     source dates them, a family key still trains on later families and on siblings of the same batch. The key
     follows the application, never the size of the gap.

2. **Correct the record's `Time: Dated` to `Time: Inferred`?**

   * **Problem:**
     - The record carries `Samples: Over Time` and `Time: Dated`, but no date ships: the only order is the NSC
       number.
     - A release that keeps only an order that tracks time, with no calendar, is `Time: Inferred` rather than
       `Time: Dated`[^2a].
     - Issue 1 also found that this particular order does not track entry into the screen for about a quarter of the
       compounds.
   * **Effect on the task:** none on the split; the fact is what a later curator would check a forward split against,
     and `Dated` invites a split that issue 1 measured and advises against.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Time: Dated` (implemented) | no change | nothing to write | no date ships; the next reader looks for one |
     | B | `Time: Inferred`, with the limit named | the fact corrected, and a CC line saying the NSC order is registration, not entry into the screen | matches what the release carries; records what issue 1 measured | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, in `curation/records/nci_aids_antiviral_screen.md` replace the `Time: Dated` tag with
   `Time: Inferred` and add the CC line with `Andrej` in `checked_by`; `Samples: Over Time` stays.

   [^2a]: **SPLIT-32** (Should): `Time: Dated` when the release or a parent source keeps the date; `Time: Inferred`
     when only an order that tracks time survives, with no calendar (an id, a case number, a file position).

   **Andrej (2026-11-11, change):** Option B: Time: Inferred, with the limit named.

