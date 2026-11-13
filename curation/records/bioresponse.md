---
unique_name: bioresponse
name: Bioresponse
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 1
decision_markers:
- Anonymized
tags:
- 'Samples: No Time Dimension'
original_source: Kaggle
year: '2012'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=4134
- https://www.kaggle.com/c/bioresponse
notebook_path: datasets/beyond_iid/old_iid/bioresponse/bioresponse.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/bioresponse/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict a biological response of molecules from their chemical properties. Data already normalized. Otherwise a great dataset (by Boehringer Ingelheim)

Potential issue: maybe the preprocessing

Lennart: no objection

Andrej: Fits criteria

CC (2026-10-19, Lennart): the descriptors are min-max scaled over Kaggle's train and test molecules; kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `log_loss`, the competition's metric (Kaggle API: "Log Loss"; was the default ROC AUC). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 834 descriptors that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Reverted: the 834 anonymized descriptors (D1...) that hold only 0 and 1 stay numeric (no semantic context).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source log_loss — Log Loss, the competition's evaluation metric (kaggle.com/c/bioresponse).

CC (2026-10-27, Lennart): marker Anonymized, from the AI review of PR #17: the 1,776 descriptors D1 to D1776 come with hidden names (Kaggle: calculated properties such as size, shape or elemental constitution, normalized), and the response and its assay are not named, so which descriptor measures what cannot be checked. Data tag Anonymized added to the definition.

CC (2026-11-11, Andrej): the use-case fit reads `approximate` (Review issue 1); the random split stays as it is while Review issue 3 is open.

- Fit: `fit="approximate"` in the definition, `fit_reason` naming the unnamed response and assay and the chemical series a random split cannot hold out. No change to the rows, the descriptors, the split, the target or the metric; the summary is not stored in the container, so no rebuild.
- Kaggle's own split: the competition says nowhere how its 2,501 test molecules were drawn - not on the description, the data description or the rules page, and in none of the 20 forum topics; the organisers' write-up (Bentzien et al., Drug Discovery Today 18 (2013) 472-478, https://doi.org/10.1016/j.drudis.2013.01.002) is subscription-only and its abstract is silent on it. The released files are indistinguishable from a random draw: a model telling Kaggle's test molecules from the training ones reaches ROC AUC 0.485, against 0.484 to 0.497 for a random third of training told from the rest.
- Close analogues under the shipped split: 3.6% of test rows have a training molecule within 0.5 of them, 42% within 3; the closest tenth scores log loss 0.331 and ROC AUC 0.932 against 0.586 and 0.822 for the farthest, and holding out every neighbour within 3 costs 0.03 log loss in all. Answered in Review issue 3: the task stands for filling in a collection that is already partly measured, so those neighbours are what the actor really has; the answer recommends keeping the random split with the overlap named.
- Time basis: the `Timeless` tag and its `Time basis:` bullet (Review issue 2, resolved 2026-11-06, to enter once the time-basis rule was in the working copy) are now in the definition; the bundle check asked for them here and passes with them.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: Boehringer Ingelheim's own Kaggle competition, methods separate clearly (1 - AUC 0.117 to 0.211); only the fit label should become approximate because the response and assay are unnamed. Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on five more routine `Timeless` issues): the response is a property of the molecule and every descriptor is computed from its structure; no date, structure or compound id is published, so nothing could date the rows. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-10, Andrej): review page issue 1, option B: use-case fit approximate; `fit_reason` names the unnamed response and assay and the chemical series a random split cannot hold out. No data, split or score change.

CC (2026-11-11, Andrej): record field set from the definition (review page field mark): `year` 2012 (was 2011).

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, issue 3 "Reply (a): Random, overlap named": the random split stays. The notes name the analogue overlap (no two molecules share all descriptors, the nearest pair differs in 16; close analogues share the label and cross the split, as no structure or compound id is published), Kaggle's own test set as a random-looking draw (a model tells it from train at ROC AUC 0.485) and the lead-optimisation use case. No data change.

## Review

**Outcome:** added. Boehringer Ingelheim's Kaggle competition "Predicting a Biological Response" (2012,
https://www.kaggle.com/c/bioresponse): 3,751 molecules, each described by 1,776 descriptors computed from its structure
(names hidden, values min-max scaled), and whether it elicited a biological response the source does not name (54%
did); scored by log loss, the competition's metric, on random splits. The AI recommends shipping it with the use-case
fit set to approximate (issue 1). Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record, the
CHANGELOG, model runs on the shipped data and on TabArena v0.1's copy). Validity: a company's own competition
on its own assay; the descriptors come from the structure alone, so they are known before a molecule is made; the
scaling over Kaggle's train and test molecules is a weak leak kept with a note (Lennart, 2026-10-19); no structures
or identifiers are published, so no chemical series can be held out (CHANGELOG 2026-11-01); model runs found
no leak, and all 3,751 rows are distinct. Value: on the shipped data (the same 3,751 rows and random splits, scored
there by ROC AUC) the 40 benchmark methods spread from 1 - ROC AUC 0.117 (TabFM) to 0.211 (default logistic regression),
median 0.129, so the methods separate. Quality: the label definition cannot be checked (issue 1); close analogues share
the label (nearest-neighbour agreement 92% in the closest tenth of distances against 64% in the farthest), which the
random split rewards, as `fit_reason` already says. Weighed: a pharma company's own screening data and competition +,
clear separation of methods +, an unnamed response and anonymous scaled descriptors -, no way to hold out a series -.

**Main points:** The random split stays with the analogue overlap named (issue 3, resolved 2026-11-11); the use-case
fit is approximate (issue 1, resolved 2026-11-10); the random split is named `Timeless` (issue 2, resolved 2026-11-06).

**Record judgment:** valid. The record's workbook notes ("data already normalized", "maybe the preprocessing") are
settled by Lennart's CC of 2026-10-19 (the scaling is kept with a note); the `Anonymized` marker fits.

**Issues for Andrej:**

1. **Set the use-case fit to approximate, since the response and its assay are not named?**

   * **Problem:**
     - The definition reads `fit="direct"`, but the source names neither the biological response nor the assay
       behind the label, so what a positive molecule means cannot be checked.
     - The curation rules make a fit approximate when the label definition is not settled, and the anonymized
       competitions with an unnamed target read approximate (santander_customer_transaction_prediction,
       kdd_cup_09_appetency).
     - Set approximate with the gap named in `fit_reason`, or keep direct?
   * **Background:** the competition page describes the label only as an experimental biological response the
     molecule did or did not show, and the columns as calculated descriptors of size, shape or elemental make-up,
     normalized (the record's CC of 2026-10-27). The use case in the definition ("for example, a medicinal chemist
     ... decides which to synthesize") is the curation's, not the source's. A fit is the closeness of the data to the
     use case; a kept weak leak does not change it[^1a], an unverified label definition does[^1b].
   * **Effect on the task:** none on the data, split or score; the label `fit` tells a benchmark user how far the
     scores stand for a named screening decision.
   * **Experiments:** in model runs on the shipped data, a molecule's nearest neighbour carries its label
     92% of the time in the closest tenth of distances and 64% in the farthest, so the random split rewards analogue
     look-up; the definition's `fit_reason` already names that gap.
   * **Consistency:** follows santander_customer_transaction_prediction ("the source names neither the transaction
     nor the time frame": approximate) and kdd_cup_09_appetency (approximate). clock_protein_toxicity and musk read
     direct; their labels are named.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Direct (implemented) | `fit="direct"`, `fit_reason` as now | the descriptors are known before synthesis | reads as if the label were checked; departs from the anonymized precedents |
     | B | Approximate | `fit="approximate"`; `fit_reason` names the unnamed response and the series that a random split cannot hold out | follows the rule and the precedents | none found; no data, split or score changes |

   * **Recommendation:** B: the label's meaning is not stated anywhere, and the sibling competitions with an unnamed
     target read approximate. **Decision:** direct (A) or approximate (B)?

   **Notes for the AI:** on B, `fit="approximate"` and `fit_reason=("The source names neither the response nor its
   assay, so what a positive means cannot be checked; without structures the split cannot hold out a chemical series,
   so scores may be higher than on a new series.")`; `dataset check`; the summary is not stored in the container, so
   no rebuild. Record: an Assessment line and `year` per the record-field row.

   [^1a]: **USE-8** (Must): a potential leak kept on purpose does not by itself make a fit approximate; the fit is that
     of the task without the leak.
   [^1b]: **USE-8** (Must): an unverified label definition is a known gap and makes the fit approximate (Lennart,
     2026-10-21, differentiated_thyroid_cancer_recurrence). **USE-5** (Must): a label from a named publication whose
     construction is undocumented may ship with `fit="approximate"` and a note naming the gap.

   **Resolved (2026-11-10, Andrej):** B: `fit="approximate"` with the drafted `fit_reason` (the unnamed response and
   assay, the chemical series a random split cannot hold out). No data, split or score changes; a CC line in the record.

   **Andrej (2026-11-11, change):** Option B: Approximate.

   **Resolved (2026-11-11, Andrej):** B, applied to the definition, which still read `fit="direct"` here. The use-case
   fit is now `approximate` and `fit_reason` reads "The source names neither the response nor its assay, so what a
   positive means cannot be checked; without structures the split cannot hold out a chemical series, so scores may be
   higher than on a new series." Nothing else changed: the rows, the descriptors, the random split, the target and the
   metric are as before, and the summary is not stored in the container, so no rebuild. A `CC (2026-11-11, Andrej):`
   line records it. The record-field row the notes point to is not in this review, so `year` (record `2011`, the
   competition and the definition `2012`) was left as it stands.

2. **Time basis: name the random split `Timeless`, as the response is a property of the molecule?**

   * **Problem:**
     - All 1,776 descriptors are computed from the structure, which exists before the molecule is made, and the assay
       result is a property of that structure, so no part of a row arrives after another part.
     - The record carries `Samples: No Time Dimension` with no time or target fact, and the definition names no time
       basis, although the company made and tested these molecules over an unstated period.
     - `Timeless` is the prototype for a target that is a fixed property of the item; what no split here can test is a
       new chemical series, since neither structures nor compound ids are published[^2a].
   * **Background:**
     - Nothing dates a row: the release has no date, no compound id and no structure, and the response, the assay and
       the testing dates were never published, so no parent source can date the molecules as ChEMBL dates
       qsar_tid_11's compounds.
     - The shipped file order carries almost nothing: the positive share runs 0.57-0.59 over the first deciles against
       0.50-0.51 over the last (Spearman of the label with the row position -0.04, p 0.016) while 200 descriptors
       show no trend along it (largest |rho| 0.039), so whether the order follows the assay order is unknown and it is
       no usable time axis.
     - The min-max scaling over Kaggle's 6,252 train and test molecules is a transform applied at release, not
       information arriving later; it is kept on purpose with a note (Lennart, 2026-10-19).
   * **Effect on the task:** none on the data, split or score; the line states why a random split over molecules is
     safe in time, and what it cannot test.
   * **Experiments:** on the shipped data a molecule's nearest neighbour carries its label 92% of the time in the
     closest tenth of distances against 64% in the farthest, the series effect the random split rewards and
     `fit_reason` already names; the time probe could not run (the Kaggle file is not in the warehouse).
   * **Consistency:** follows the undated property catalogues of this review (musk, superconductivity, the QSAR sets),
     which recommend `Timeless`; it differs from qsar_tid_11 and sdss_17, where a parent source dates the items and a
     forward split was measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time basis (implemented) | as now | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random split, `Timeless` | as now; the tag and a `Time basis:` line naming the structure-only descriptors, the unknown testing dates and the series the split cannot hold out | states the fact the split rests on; names what the split cannot test | none found; no data, split or score changes |
     | C | `Samples: Over Time`, `Time: Lost` and a forced tag | the record's fact changed and the split tagged as forced from temporal | reads the company's set as a catalogue that grew over years | nothing is dated or recoverable and the response does not move with time, so the tag would say nothing a dated release could settle |

   * **Recommendation:** B: the descriptors and the response belong to the structure, and nothing in or behind the
     release dates a row. **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Anonymized", "Timeless")` (the class adds `IID`) and
   a curation bullet `- Time basis: Timeless: the response is a property of the molecule and every descriptor is
   computed from its structure, so nothing in a row arrives later. Boehringer Ingelheim tested the molecules over an
   unstated period and published no date, structure or compound id, so no forward split is possible; the label drifts
   only weakly along the file order (positive share 0.57-0.59 in the first deciles against 0.50-0.51 in the last,
   Spearman -0.04) and the order is not known to follow the assays. Not tested: a new chemical series, as close
   analogues cannot be grouped (nearest-neighbour label agreement 92% in the closest tenth of distances against 64%
   in the farthest).`; `splits_comment` unchanged; `dataset check`; the comment is not stored in the container, so no
   rebuild. On C, the record's `tags` change too.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts and a definition can name the use-case prototype it follows with a `Time basis:` line.
     `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's strength,
     a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by item family.
     **SPLIT-31** (Should), as amended 2026-10-26 (Lennart): a molecule dataset whose rows carry exact structures
     groups on the Bemis-Murcko scaffold, which this release cannot do, as it ships no structures.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept five more routine `Timeless`
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (a new chemical series); the split and `data_tags` are unchanged. The tag `Timeless` enters `data_tags`
   once PR #50 is in the working copy.

3. **Keep the random split with the analogue overlap named, as no molecule is a copy and the series are lost?**

   * **Problem:**
     - No two of the 3,751 molecules share all 1,776 descriptors, and no pair comes within 10 descriptors of each other, so there is no copy to drop; what crosses a random split is close analogues of one chemical series, which share the label (in model runs on the shipped data, nearest-neighbour agreement 92% in the closest tenth of distances against 64% in the farthest).
     - Without structures or compound ids the series cannot be recovered, and grouping on a similarity cluster is barred, so the new rules for repeats of a unit the data does not record give the verdict "not recoverable": drop the copies that can be identified (none here) and keep the random split with the overlap named[^3a].
     - Keep the random split with the overlap named, or retire because the split still rewards recognising a series nobody recorded[^3b]?
   * **Experiments** (2026-11-06, the 3,751 rows of the Kaggle training file, as shipped):
     - **No link to test:** counting the descriptors in which two molecules differ, each molecule's nearest other
       molecule differs in at least 16 of them (median 106); 9 pairs differ in at most 25 and 149 in at most 50. Under
       random 3-fold splits (20 repeats) no test molecule has a training molecule within 10 descriptors, and 0.3%
       within 25.
     - **The label follows similarity, not identity:** the 9 closest pairs share the label 8 times, the 149 pairs
       within 50 descriptors 87% of the time, against 50% from the class shares; by this count the nearest
       neighbour shares the label 82% of the time in the closest tenth and 70% in the farthest. This is the
       structure-activity relation of a series of distinct molecules, each with its own measured response.
     - **No order:** no date, compound id or structure; the file order carries almost nothing (issue 2).
     - The 834 binary descriptors alone repeat (228 molecules share another's binary part): distinct molecules with
       the same substructure flags, told apart by the other 942.
   * **Consistency:** distinct compounds that the descriptors cannot tell apart stay (hiva_agnostic, qsar_tid_11)[^3c],
     and molecules with structures are grouped on their scaffold, which this release cannot do (issue 2).
     maternal_health_risk and hazelnut_spread_contaminant_detection were retired because their rows are repeats of
     one unit that could not be recovered; here every row is a distinct molecule.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, overlap named (implemented) | 3,751 molecules; `fit_reason` already names the series; the notes gain the verdict and the numbers above | no copy exists to drop; analogues of tested molecules are what a chemist optimising a series designs next | scores are higher than on a new series, which no split here can test |
     | B | Retire | record `No (Retired)`; folder removed | no task that rewards recognising an unrecorded series | the rule for lost groups is written for repeats of one unit; a pharma company's own assay and competition leaves |

   * **Recommendation:** A: every row is a distinct molecule with its own response, no pair is a copy, and the
     analogue overlap is the series a medicinal chemist works within, already named in `fit_reason`.
     **Decision:** keep the random split with the overlap named (A) or retire (B)?

   **Notes for the AI:** on A, once PR #62 is in, a curation bullet "- Entity leakage, not recoverable (2026-11-06): no
   two molecules share all 1,776 descriptors and the nearest pair differs in 16, so no copy is dropped; close analogues
   of one series share the label (nearest-neighbour agreement 92% in the closest tenth of distances against 64% in the
   farthest) and cross the random split, as no structure or compound id is published to group them."; no data
   change, no rebuild. On B, `suggestion: No (Retired)`, folder removed, `v2_path` cleared, a `CC (<date>, Andrej):`
   line. The raw Kaggle file is not in the warehouse; the checks used OpenML 46912 (TabArena's copy of the same
   3,751 rows).

   [^3a]: **LEAK-42** (Must, draft PR #62): repeats of a unit the data does not record get one verdict; not
     recoverable when neither the units nor their order can be recovered with enough confidence: the copies that can
     be identified are dropped, and the random split stays with the remaining overlap in the notes. **SPLIT-24**
     (Must): never group on a similarity-threshold cluster.
   [^3b]: **SPLIT-25** (Must): when the real groups matter and cannot be recovered, never group on a guess; drop the
     repeats that can be identified, and retire when they cannot be identified or what stays still rewards
     recognising an unrecorded group (maternal_health_risk, hazelnut_spread_contaminant_detection).
   [^3c]: **LEAK-19** (Should): copies of one compound go; distinct compounds that the descriptors cannot tell apart
     stay, with the reason in the notes (hiva_agnostic, qsar_tid_11; Lennart, 2026-10-21).

   **Andrej (2026-11-10, discuss):** Check the original Bioresponse competition - was the split random too? Also, can we
   argue that for this dataset the goal could also be to test similar samples with a similar compound in test as in
   train?

   **Answer (AI, 2026-11-10):** yes, Kaggle's own split looks random. The 2,501 test molecules cannot be told from the
   3,751 training molecules, and they sit as close to them as a random third of train does.

   | Check (Kaggle `train.csv` against `test.csv`) | Kaggle test against train | Random third of train against the rest |
   |---|---|---|
   | Model telling the two apart (LightGBM, ROC AUC) | 0.485 | 0.484 to 0.497 |
   | Nearest of 2,500 training molecules, median Euclidean distance | 3.76 to 3.78 | 3.73 to 3.79 |
   | Same, median number of descriptors that differ | 115 to 118 | 113 to 116 |
   | Share within 50 descriptors | 3.5% to 4.1% | 3.9% to 4.9% |

   * Kaggle states neither how the test set was drawn nor the public/private share, and the test labels were never
     released, so the public/private split cannot be measured.
     Posted pairs of the same submission score better in private: LightGBM 0.449 public against 0.378 private, oblique
     forests 0.472 against 0.408 and 0.483 against 0.425. The winner has 0.374 private.
   * A forum post of April 2012 claimed that test molecules lie farther from training than training molecules lie from
     each other. The released files do not show this (table).
   * **Use case:** yes. Scoring new analogues of series already in testing is how a project spends most of its assays
     (lead optimisation), and the competition framed it the same way.
     A random split tests exactly this.
   * **Rules:** molecules with exact structures are grouped on their scaffold, because a new chemical often comes from
     an unmeasured series[^3d]. This release has no structures, so that exception cannot apply.
     Over related entities, a random split can match how the task is framed[^3e], as here.
   * So A holds, with the analogue use case and Kaggle's random split named; `fit_reason` already names the series.
   * Raw Kaggle files re-downloaded today.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Random, overlap named (implemented) | option A, and the notes add that Kaggle's test set is a random draw (numbers above) and that the use case is screening analogues of tested series | matches the competition and a real use case | no new series is tested |
   | b | Retire | option B | none beyond the issue | a random split fits the framing |

   * **Recommendation:** a. **Decision:** a or b?

   [^3d]: **SPLIT-31** (Should; amended 2026-10-26, Lennart): molecules with exact structures group on the scaffold.
   [^3e]: **SPLIT-31** (Should): over related entities, IID can match how a task is framed, even when optimistic.

   **Andrej (2026-11-11, discuss):** Check the original Bioresponse competition - was the split random too?

   **Andrej (2026-11-11, discuss):** Reply (a): Random, overlap named

   Also, can we argue that for this dataset the goal could also be to test similar samples with a similar compound in
   test as in train?

   **Answer (AI, 2026-11-11):** Kaggle never wrote down how it drew the test set, but nothing in the released files
   distinguishes it from a random draw; and the analogue overlap is this task's use case, not a defect, so the random
   split stands with what it leaves on the training side now measured.

   * **Problem:**
     - No page of the competition, and no organiser post in its forum, says how the 2,501 test molecules were
       chosen; the write-up the host promised is subscription-only and its abstract is silent on the split.
     - What can be measured says the draw was random: a model cannot tell Kaggle's test molecules from the training
       ones, and they sit as close to training as a random third of training does.
     - Whether the close analogues crossing the split are a flaw or the task itself turns on which actor the dataset
       stands for, and this release can compute neither a family key nor an entry date.
   * **What the sources say** (the competition's own pages and its full forum, read again 2026-11-11):

     | Source | What it says about the split |
     |---|---|
     | Description and data description | each row is a molecule, d1 to d1776 are calculated properties, "the descriptor matrix has been normalized"; nothing on the split |
     | Rules | the host may modify the training and/or testing dataset during the competition; nothing on how they were drawn |
     | Forum, 20 topics, 2012 to 2022 | no organiser post on the draw; a participant calls the test data "an exactly comparable random sample (which this one was however)"; another plots "public 25 % dataset" against "private 75 % dataset" |
     | Organiser post, 2012-06-16 | promises to publish the descriptors and "point you to structures"; the release carries neither, and no later release was found |
     | Bentzien et al., Drug Discovery Today 18 (2013) 472-478 | the write-up that promise became; subscription-only, and its abstract names only that the complete structure of the dataset is disclosed |
     | A participant, 2012-04-20 | "the distances between testset and training set don't go below 6 units"; the files contradict it (nearest training molecule of a test molecule: 0.03 at the closest, 3.4 at the median) |

     So the source leaves it unstated; the turn of 2026-11-10 measured the released files and found Kaggle's test set
     indistinguishable from a random third of training (model telling them apart, ROC AUC 0.485 against 0.484 to
     0.497; the same nearest-neighbour distances).
   * **Experiments** (the 3,751 shipped rows, LightGBM, 10-fold, 3 seeds; Euclidean distance on the 1,776 scaled
     descriptors): under the shipped split log loss 0.487 and ROC AUC 0.883, and a test molecule's nearest training
     molecule is this close:

     | Nearest training molecule within | Share of test rows |
     |---|---|
     | 0.5 | 3.6% |
     | 1.0 | 6.5% |
     | 2.0 | 24.6% |
     | 3.0 | 42.3% |

     The score does depend on that distance, and so does the label of the neighbour:

     | Decile of the distance | Median distance | Log loss | ROC AUC | Neighbour has the same label | Positives |
     |---|---|---|---|---|---|
     | 1 (closest) | 0.68 | 0.331 | 0.932 | 86% | 65% |
     | 2 | 1.46 | 0.436 | 0.907 | 78% | 57% |
     | 3 | 2.02 | 0.417 | 0.912 | 77% | 53% |
     | 5 | 3.13 | 0.500 | 0.877 | 78% | 54% |
     | 8 | 5.57 | 0.658 | 0.806 | 67% | 55% |
     | 10 (farthest) | 10.65 | 0.586 | 0.822 | 65% | 45% |

     A family key cannot be computed here, but its effect can be bounded by holding out each test molecule's whole
     neighbourhood (single-linkage components of the descriptor graph, grouped folds, the same 3,751 rows scored):

     | Held out | Groups | Largest group | Log loss | ROC AUC | Test rows with a neighbour within 3 |
     |---|---|---|---|---|---|
     | nothing (random, implemented) | - | - | 0.487 | 0.883 | 42% |
     | neighbours within 0.5 | 3,670 | 6 | 0.485 | 0.883 | 42% |
     | neighbours within 1.0 | 3,601 | 9 | 0.493 | 0.880 | 41% |
     | neighbours within 2.0 | 3,074 | 31 | 0.485 | 0.880 | 31% |
     | neighbours within 3.0 | 2,506 | 77 | 0.517 | 0.866 | 0% |

     So the near neighbours are worth about 0.03 log loss and 0.02 ROC AUC in all: they help the few rows that have
     them a lot and the rest not at all.
   * **Which situation the rule on catalogue keys describes:** a company's compound collection that already existed
     and was assayed in part, so this is the inventory an actor fills in, not a catalogue whose items arrive over
     time[^3f]. In that situation the family key stands for the less similar compounds of the same inventory, and the
     inventory is the reference for how close the test compounds should be; here neither is available, as the release
     publishes no structure, no identifier and no date, and the inventory itself was never published. The key follows
     the application and never the size of the gap, so the 0.03 above argues for nothing on its own.
   * **The use case Andrej asks about:** yes, it is the one this release stands for. A company that has measured part
     of its collection and wants the rest filled in meets exactly these neighbours; so does lead optimisation, where
     the next compounds are analogues of the ones already in the assay. The use case that near neighbours would
     flatter, screening a series nobody has tested, is the one no split of this release can build, and `fit_reason`
     says so.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random, the overlap and the use case named (implemented) | option A of this issue; the curation notes gain that Kaggle's own test set is indistinguishable from a random draw and that the task stands for filling in a collection that is partly measured | matches what the source did, as far as it can be measured; matches an actor who really has these neighbours; the numbers above say what it leaves on the training side | a series nobody has tested is not tested, and 3.6% of test rows have a neighbour within 0.5 |
     | b | Group on descriptor-distance clusters | folds grouped by single-linkage components at a cutoff | removes the close neighbours | the cutoff is a guess, grouping on a similarity cluster is ruled out, and it would test an actor this release cannot describe[^3a] |
     | c | Retire | option B of this issue | no task that rewards recognising an unrecorded series | every row is a distinct molecule with its own measured response, and the overlap is the use case |

   * **Recommendation:** a, and nothing in the definition changes but the notes. **Decision:** a, b or c?

   [^3f]: **SPLIT-34** (Should): in a catalogue of items whose target is a fixed property, the item, its family and
     when it entered the catalogue are three keys, each testing something else; which one stands for the use case is
     information from the use case and the source, and where the actor fills in an inventory that already exists,
     nothing comes later and the family key stands for the less similar items of that inventory. The key follows the
     application, never the size of the gap.

   **Resolved (2026-11-11, Andrej):** a: the random split stays; a curation bullet names the analogue overlap (no copy,
   nearest pair 16 descriptors apart), Kaggle's random-looking test draw (ROC AUC 0.485) and the lead-optimisation use
   case; no data change. The bullet cites no rule ID until PR #62 (LEAK-42) is in the working copy.

## Reference

https://www.kaggle.com/c/bioresponse
