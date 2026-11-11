# apistox

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

