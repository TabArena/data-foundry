# qsar_oral_toxicity

**Outcome:** added. The very toxic endpoint of the ICCVAM acute oral toxicity project (rat oral LD50, the data behind
CATMoS): 11,116 chemicals with their QSAR-ready structure as a SMILES, grouped on the Bemis-Murcko scaffold (7,481
groups). Opened on 2026-11-11 from the review of how catalogues of fixed properties split: the definition names no
time basis for its scaffold split.

**Main points:** Name the scaffold split `Timeless`, with the project's own untested chemicals as the reference for
how far a test chemical stands from training (issue 1)?

**Issues for Andrej:**

1. **Time basis: name the scaffold split `Timeless`, or date the chemicals first?**

   * **Problem:**
     - The definition splits on the scaffold and names no time basis, while the record carries
       `Samples: No Time Dimension`.
     - Whether a chemical is very toxic when swallowed is a fixed property of the chemical, the case the `Timeless`
       prototype names[^1a].
     - The project that compiled the data also published the chemicals it was built to screen, so how new the test
       chemicals are can be measured against the actor's real population rather than guessed.
   * **Background:** the use case is a chemical without an acute oral test, judged before any animal test; the fit is
     already recorded as approximate, because the test chemicals are members of the tested reference set.
   * **Experiments:** the share of chemicals with a close training analog (Tanimoto 0.7 or more, Morgan radius 2,
     2,048 bits), measured when the scaffold split was adopted:

     | Population | Close analog in training | Median nearest similarity |
     |---|---|---|
     | Test chemicals, random split | 24.7% | |
     | Test chemicals, scaffold groups | 16.3% | 0.519 |
     | The project's 48,137 untested chemicals | 11.0% | 0.486 |

   * **Effect on the task:** the scaffold groups move the test chemicals most of the way toward the untested
     inventory the actor meets, which is what the split is for here; nothing in this task arrives later, since the
     inventory already exists.
   * **Consistency:** on 2026-11-11 the three sibling Milano sets (qsar_biodeg, qsar_fish_toxicity,
     qsar_aquatic_toxicity) were sent to be dated through NITE and ECOTOX before their time basis is named; this
     dataset differs in having its screening population published, so the question it answers is already measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | no change | nothing to write | the definition does not say why a split that is not temporal is safe in time |
     | B | Scaffold split, `Timeless` | the tag and a `Time basis:` line naming the fixed property and the untested inventory as the reference | states the fact the split rests on; the inventory measures what the split cannot reach | the order in which the chemicals were tested stays unmeasured |
     | C | Date the chemicals first | look for a test or registry year per chemical, then decide as the sibling sets will | same route as the three siblings | the use case fills in an existing inventory, where nothing comes later; the ICCVAM compilation pools many databases and registries |

   * **Recommendation:** B: the actor screens an inventory that already exists, and that inventory is published, so
     it is the reference rather than a year. **Decision:** A, B or C?

   **Notes for the AI:** on B, `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`) and a
   `curation_comments` bullet: `- Time basis: Timeless: acute oral toxicity is a property of the chemical, and the
   use case fills in an inventory that already exists. The split holds out whole series: 16.3% of the test chemicals
   have a close training analog, against 24.7% at random and 11.0% for the project's 48,137 untested chemicals, so
   the split stands between a random one and the screening population.` Then `dataset check`, a CHANGELOG entry and a
   record CC line with `Andrej` in `checked_by`.

   [^1a]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows; `Timeless` when the target
     is a fixed property of the item, the same whenever it is measured, and the use case meets items drawn like the
     catalogue's. **SPLIT-34** (Should, proposed): where the actor fills in an inventory that already exists, nothing
     comes later and the family key stands for the less similar items of that inventory; the inventory itself, where
     the source has it, is the reference for how close the test items should be to training.

   **Andrej (2026-11-11, change):** Option C: Date the chemicals first.

