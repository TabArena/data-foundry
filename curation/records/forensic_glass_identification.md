---
unique_name: forensic_glass_identification
name: glass2
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
decision_markers:
- Outdated
tags:
- Tiny Data
- 'Samples: No Time Dimension'
collections:
- TabArena Reject
original_source: UCI
year: '1987'
domain: chemistry & material science
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/glass2/metadata.yaml
- https://doi.org/10.24432/C5WW2P
- https://www.openml.org/d/41
notebook_path: datasets/beyond_iid/new_iid/forensic_glass_identification/forensic_glass_identification.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/forensic_glass_identification/dataset.py
source_row: 755
type_adapter_id: curation-record-v1
---

## Comments

PMLB version has less samples and less classes, so likely filtered (?)

Generally a valid potential task, might be outdated but still valid for the task?

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Tableware (class 6) has 9 rows, 3 in every test fold, and class 5 has 13 (4-5). Together they are 10% of the test rows and 14% of a random forest's log loss (0.70 against 1.51 for the class shares). Too Small is for a task whose scored units are a handful; one rare class of the source's own labels that does not decide the score is part of the task.

CC (2026-10-20, Andrej): Keep; no reason to exclude found, but the use case is dated.

- **Outdated:** 36% of rows are non-float window glass, which float glass (formed on molten tin) had replaced by the mid-1970s; casework today compares fragments by trace elements (LA-ICP-MS, laser mass spectrometry), not glass type by major oxides. Covered by the `Outdated` marker; methods still separate (29 configurations beat the dummy on 19/19 folds, Kendall's W 0.79).
- **Short classes:** the hardest is vehicle float glass (17 rows, 5-6 per test fold): 8% of the rows, 17% of a random forest's log loss; with containers and tableware, 18% of the rows carry 30%. Well below the share at which short classes decide the score (alvin: 51-54%).
- **Row order:** the file is sorted by class and, within a class, in a few blocks that each run roughly from high to low Mg (magnesium oxide; Kendall's tau -0.4 to -0.9); the features predict the Id order (Spearman 0.67-0.90 out of sample). Holding out stretches of Ids therefore holds out Mg ranges, not new objects: an order built from the features alone costs the same (TabPFN log loss 0.85, against 0.55 on random splits). Beyond the sort, fragments of one object sit next to each other (Ids 39-40 identical, 67-69 share the refractive index), but holding out blocks of 3 neighbours adds only 0.01 (TabPFN) to 0.06 (logistic regression) log loss and leaves the ranking unchanged. The random split stays.
- **Provenance:** rows were collected per class, not sampled from casework, so the class shares are arbitrary; the original technical note is unknown (`glass.names`). The creator was the UK Home Office Forensic Science Service (UCI's abstract says "USA"). PMLB glass2 is the 163-row float vs non-float window subset.

Done in `dataset.py`: dropped the exact duplicate (Ids 39 and 40), with a curation note on the row order; origin set to the UK Home Office Forensic Science Service; use-case fit set to approximate (dated features and glass types, class shares of a collection).

References: German B. Glass Identification. UCI Machine Learning Repository; 1987. doi:10.24432/C5WW2P. ASTM E2927-16e1, Standard Test Method for Determination of Trace Elements in Soda-Lime Glass Samples Using Laser Ablation Inductively Coupled Plasma Mass Spectrometry for Forensic Comparisons. ASTM International; 2016.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — the source defines no metric for the 6-class task; its only result (Spiehler's comparison) counts errors on a different, binary target.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 3: gap +, use case - (dated; class shares come from a collection), source +, shape -, risk +.
CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships its class names.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined with the random split and a note: real forensic measurements whose methods spread; near-copies across the random split are real but the ones that look like one object are few file neighbours, and the rest cannot be tied to objects. Priority 2: gap 1, use case 0, source 1, shape 0, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 3, B, through the cross-dataset item on five more routine `Timeless` issues): the glass type belongs to the object and the measurements to the fragment; the casework before 1987 carries no published date. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-12, Andrej): BeyondArena v0.2 review page, forensic_glass_identification: the random split stays as a decision of ours (issue 2, A), and Id 68 is dropped (issue 4, B).
- **Random split, deliberate:** no clean groups govern how the collection was made. Only 7 glass objects (14 rows) are tied together by a link calibrated against chance: identical refractive index, the same type and every oxide within the tolerance of two analyses, 7 pairs where chance gives 1.8. The other near-copies (35% of the rows within 0.16 SD on five columns) are different objects of the same kind of glass, which a reference collection holds. Holding out the 7 objects cost TabPFN 0.009 log loss and left the ranking unchanged. The definition's `splits_comment` states the choice and its reason; the row-order note gives the near-copy shares.
- **Id 68 dropped:** equal to Id 67 in eight of nine values, silicon 72.32 against 72.22; two analyses of one glass do not agree to 0.01 percent in six oxides, so it is one record entered twice. 212 rows; float building windows 69 to 68.
- Sources: Curran JM, Hicks TN, Buckleton JS. Forensic Interpretation of Glass Evidence. CRC Press, Boca Raton; 2000. ISBN 0-8493-0069-2. Lambert JA, Evett IW. The refractive index distribution of control glass samples examined by the forensic science laboratories in the United Kingdom. Forensic Science International 1984;26(1):1-23, https://doi.org/10.1016/0379-0738(84)90207-x.

CC (2026-11-13, Andrej): BeyondArena v0.2 review page, forensic_glass_identification: ship as defined (issue 1, A, closed on the note "This can be closed."; verdict ship, split and metric ok).
- Ships with 212 rows, 9 features, six glass types and the random split, as settled on 2026-11-12.
- Not an exclusion: the dated use case is recorded by the `Outdated` marker and the approximate fit; the short classes carry about their share of the log loss.

## Review

**Outcome:** added. The AI recommends shipping it; the split stays random by your decision of 2026-11-12 (issue 2,
A), and Id 68, a record entered twice, is dropped (issue 4, B).
Reviewed without a review panel, from the gathered evidence (the record, earlier experiments, a model run on the shipped
data); first written 2026-10-27, updated 2026-11-04 with issue 2. The dataset is UCI 42 (German 1987): 213 glass
fragments from the UK Home Office Forensic Science Service, with the refractive index and the weight percents of eight
oxides, and the glass type as one of six classes. Validity: real measurements; the exact duplicate (Ids 39 and 40) is
dropped, and the random split stays on your review of 2026-10-20, as the within-class row order is a sort by magnesium,
not a set of hidden objects. New: our experiments found that looking up near-identical fragments in the training rows
improves an explicit model by 0.03 to 0.045 log loss on random splits, and a check on the v0.2 frame finds a near-copy
for 36% of the fragments, six times a within-class shuffle; the closest copies (8 rows) are file neighbours of the kind
your block test held out, the looser ones mostly not (issue 2). Value: methods spread: 29 configurations beat the dummy
on 19 of 19 folds (Kendall's W 0.79), and the benchmark methods on the shipped data range from 0.552 (TabICLv2) to 1.00
log loss (logistic regression), median 0.638, TabPFN 0.558. Quality: the use case is dated (`Outdated`) and the class
shares come from a collection, not casework (`fit` approximate); the short classes carry about their share of the loss;
the target ships the source's class names since 2026-11-01. Weighed: real forensic measurements, a documented source and
a clear spread +; a dated use case and near-copies across the random split -.

**Main points:** Nothing open: ship (issue 1, A, resolved 2026-11-13; verdict `ship`). Resolved 2026-11-12: the
random split stays, written down as our decision (issue 2, A), and Id 68, Id 67 entered again, is dropped (issue 4, B;
212 rows). The split is named `Timeless` (issue 3, resolved 2026-11-06).

**Record judgment:** valid; the record carries your keep of 2026-10-20 with its reasons and Lennart's of 2026-10-12 on
the short classes. Its `name` `glass2` is PMLB's name for the 163-row float-against-non-float window subset, kept by
your choice. The record fields agree with the definition.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**

   * **Problem:**
     - Your review of 2026-10-20 found no reason to exclude the dataset and made the changes in `dataset.py`: the exact
       duplicate dropped, the origin corrected (UCI's abstract says USA, the names file names the Home Office lab at
       Aldermaston), `fit` set to approximate, and a note on the row order.
     - Lennart's comment of 2026-10-12 keeps the short classes (tableware 9 rows, 3 per test fold; containers 13 rows,
       4 to 5), which together are 10% of the test rows and carry 14% of a random forest's log loss[^1b].
     - Ship as defined, or name what is missing?
   * **Background:** kept on purpose: 36% of the rows are non-float window glass, which float glass (formed on molten
     tin) had replaced by the mid-1970s, and casework today compares fragments by trace elements (laser ablation mass
     spectrometry, ASTM E2927-16e1), not glass type by major oxides, hence the `Outdated` marker; fragments of one
     object sit next to each other in the file, which costs 0.01 (TabPFN) to 0.06 (logistic regression) log loss when
     blocks of 3 are held out (issue 2 takes this further). Since 2026-11-01 the target ships the source's class names
     (Lennart); decoding reshuffled the rows, and the accepted row-order warning (codes against position, rho -0.21,
     reached by 0.4% of random shuffles) comes from that fixed shuffle, not from the source's order.
   * **Experiments:** on the shipped splits, 29 tuned configurations beat the dummy on 19 of 19 folds, and their ranks
     agree across folds (Kendall's W 0.79)[^1a]. The 40 benchmark methods on the shipped data (214 rows):
     0.552 (TabICLv2) to 1.00 (logistic regression, tuned), median 0.638, TabPFN-3 0.558, CatBoost tuned 0.626. Vehicle
     float glass, the hardest class (17 rows, 5 to 6 per test fold), is 8% of the rows and 17% of a random forest's log
     loss; with containers and tableware, 18% of the rows carry 30%.
   * **Consistency:** follows mic (a rare class of 0.7% of the test rows with 4.8% of the log loss, kept); alvin was
     retired when its rarest classes carried 51-54% of a window's log loss.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 213 rows, 9 features, six types, random split | methods spread; the short classes carry about their share; your review found no reason to exclude | a dated use case; class shares of a collection |
     | B | Retire as dated | record `No (Retired)` with `Outdated`; folder removed | no 1987 glass types in the benchmark | `Outdated` records a dated task, not a reason to retire; a spread task leaves |

   * **Recommendation:** A: the measurements are real, the methods spread, and the dated use case is recorded by the
     marker and the fit. **Decision:** ship as defined (A), retire it as dated (B), or name what is missing?

   [^1a]: **TP-3** (Must): if tuned methods spread, keep the dataset; no further discussion is needed (a rule of an
     earlier part still wins).
   [^1b]: **TP-8** (Must): a short class in a multiclass task is a question about that class, not about the task;
     `Too Small` applies when the short classes carry a large share of the score or a test fold holds a handful of
     units in all, and a rare class whose rows carry about their share of the loss stays.

   **Andrej (2026-11-05, discuss):** I go with A, but also look at the other issues.

   **Answer (AI, 2026-11-05):**

   * **Noted:** ship it (A). The one other open question is the split (issue 2). Its answer finds 7 glass objects
     with two or three rows each, all marked by an identical refractive index, and recommends a split grouped on that
     value.
   * **What it changes here:** only the split and the notes that describe it. The rows, features, target and metric
     stay, so A holds whichever way issue 2 goes; with issue 2's B, the split line of the task summary and the
     curation note on the row order change with it.

   **Andrej (2026-11-13, discuss):** This can be closed.

   **Resolved (2026-11-13, Andrej):** A: ship, per your A of 2026-11-05 and this note; verdict `ship`, split and
   metric `ok`. The dataset ships with 212 rows (Id 68 dropped, issue 4), 9 features, six types and the random split
   written down as our decision (issue 2). Text only: nothing in `dataset.py` changes. Record CC line.

2. **Keep the random split, although many fragments have a near-copy on the other side of it?**

   * **Problem:**
     - Our experiments found that looking up near-identical fragments in the training rows improves an explicit model
       by 0.03 to 0.045 log loss on the random splits of the shipped data.
     - On the v0.2 frame, 36% of the fragments have a near-copy within 0.16 standard deviations on the refractive index,
       magnesium, aluminium, potassium and calcium, six times what a within-class shuffle of the columns gives, and
       95% of those copies have the same type.
     - If the copies are fragments of one object, a random split rewards recognising the object, which a lab facing a
       fragment of a new object cannot do[^2c]; your keep of 2026-10-20 rests on a test that held out only file
       neighbours.
   * **Background:** the source has no object id; the names file says only that the fragments were collected in
     forensic work. The closest copies look like fragments of one object: 8 rows have a copy within 0.08 standard
     deviations, all of the same type, 6 of them next to it in the file (Ids within 2), the kind your block test held
     out (Ids 67-69 share the refractive index). The looser copies mostly are not file neighbours (32% within 2 Ids),
     and the exact refractive index does not mark objects either: 67 rows share theirs with another row, but 15 of the
     32 shared values span two types. They read as glass of one product made the same way, which a reference
     collection holds in practice. Grouping on a similarity cluster is no option[^2a]; when the real groups matter and
     cannot be recovered, the dataset retires instead[^2b].
   * **Effect on the task:** a test fragment whose copy is in training is easier than a fragment of a new object. Your
     block test puts this at 0.013 log loss for TabPFN (0.670 with blocks of 3 file neighbours held out, against 0.657
     for blocks of the same size in an order by magnesium) and 0.06 for logistic regression; a lookup
     takes 0.03 to 0.045 from an explicit model, of which the exact copy dropped in v0.2 is about one test row in 71.
   * **Experiments:** a check on the v0.2 frame (job 1344817): near-copies by Euclidean distance on the five columns,
     standardized; within 0.08 SD 8 rows (3.8%, all same type), within 0.16 SD 76 rows (36%, 95% same type), within
     0.25 SD 127 rows (60%, 88% same type); with each column shuffled within its class (200 draws), 0.7, 12 and 45 rows
     (95th percentiles 4, 18 and 56); the shuffle also breaks the correlation between the columns (the refractive
     index follows calcium), so the excess over it is an upper bound. An explicit model (a glass-family hierarchy)
     scored 0.609 and
     0.575 without the lookup and 0.564 and 0.541 with it on 19 splits (0.580 and 0.537 against 0.541 and 0.510 on 41
     held-out splits); the benchmark methods scored 0.552 at best.
   * **Unknown:** whether the looser copies are fragments of one object or of one product; only the collector's list
     of objects would settle it, and none is published.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, with a note (implemented) | the split as now; the curation note gives the near-copy shares and the lookup's gain | follows your keep of 2026-10-20; the copies that look like one object are 8 rows, file neighbours whose hold-out costs TabPFN 0.013; a reference collection holds glass of the same products | random-split scores are optimistic for a model that looks up copies, by up to 0.03-0.045 |
     | B | Retire: the groups matter and cannot be recovered | record `No (Retired)`; folder removed | no score rewards recognising an object | rests on copies that cannot be tied to objects; undoes your keep; a spread task leaves |

   * **Recommendation:** A: the copies that look like one object are few and are the file neighbours your test
     already held out, and the looser ones cannot be tied to objects, so retiring would rest on a guess; the note
     tells users how much a copy lookup gains. **Decision:** keep the random split with a note (A), or retire (B)?

   **Notes for the AI:** on A, extend the row-order bullet of `curation_comments`: "Near-copies: 8 rows have a copy
   within 0.08 SD on RI, Mg, Al, K and Ca (all of the same type, 6 file neighbours), 76 (36%) within 0.16 SD (95% of
   the same type, 32% file neighbours; a within-class shuffle of the columns gives 12); a lookup of such copies gains an
   explicit model 0.03-0.045 log loss on random splits. No object id exists, so the split stays random." Add a
   `CC (<date>, Andrej):` line to the record, re-run `dataset check` and add a CHANGELOG entry (comment text only,
   the data are unchanged). On B: `suggestion: No (Retired)`, folder removed, `v2_path` cleared, a record note that the
   object labels could only come from the collector, CHANGELOG entry.

   [^2a]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data (identical values
     in the columns that define the entity), never on a similarity-threshold cluster.
   [^2b]: **SPLIT-25** (Must): when the real groups matter and cannot be recovered, retire the dataset rather than
     group on a guess, and note that the authors could be asked for the group labels.
   [^2c]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have and
     the entity carries the label, as a random split then rewards recognising the entity; **SPLIT-30** (Must): re-split
     only when the context says the rows share such an entity, or the evidence is very strong; the size of the gap
     never decides.

   **Andrej (2026-11-05, discuss):** Give it your best to uncover whether there are really groups based on studying
   the domain and use case. It might be that this is a real random split task, or a grouped split with recoverable
   groups or a grouped split with not recoverable groups and each would be handled differently.

   **Answer (AI, 2026-11-05):**

   * **Finding:** the second case, recoverable groups, and only a few of them. Rows of one glass object show up as
     rows with the identical refractive index. Among rows of the same type whose eight oxides agree within analytical
     noise, 9 pairs share the refractive index to the fifth decimal where chance gives 2 (p < 0.002), while rows whose
     oxides differ share it as often as chance gives (7 pairs against 7). That makes 7 clear objects with two or three
     rows, 15 rows in all, and perhaps a few more among the other shared values. The other near-copies are different
     objects of the same kind of glass, and a random split over them matches the use.
   * **How the collection was built:**
     - The creator, B. German, worked at the Home Office Central Research Establishment at Aldermaston, which kept the
       Forensic Science Service's database of control glass from casework: one entry per control, the broken object
       of a case, over 9,000 of them (Lambert and Evett 1984; Curran et al. 2000, Table 4.7).
     - Each row is "a single glass fragment" (Ripley's notes to the data), with eight elements measured by scanning
       electron microscope (Evett and Spiehler 1987). No list of objects or cases was published, and no source says
       whether an object gave more than one row.
     - In casework the refractive index of a control is the mean over several of its fragments; fragments of one
       window differ with a standard deviation of about 0.00004, the value the usual range tests assume (Curran et
       al. 2000, Table 2.6). Rows with one refractive index to the fifth decimal and oxides within noise read as one
       object's value written on more than one analysis, or as one record entered twice (Ids 67 and 68, below).
     - The float process made the flat glass of one plant very uniform (Curran et al. 2000, section 1.11), so windows
       of different cases often agree in refractive index and major oxides: that is the near-copy most rows have.
   * **What the use case needs:** a caseworker classifies a fragment recovered from a suspect's clothing, to choose
     the glass it is compared with (window controls or other glass); that need made elemental analysis routine in the
     early 1980s (Curran et al. 2000, section 4.7). The fragment's object is never in the reference collection, so the
     test objects must be new. Its kind of glass usually is there, since the same plants supply the market, so
     near-copies from other objects on the training side belong to the task.
   * **What the data shows** (chance level: each row's refractive index moved at random by up to 0.00005, 2,000
     draws):
     - Copies: Ids 39 and 40 agree in all nine values (40 is dropped in v0.2), Ids 67 and 68 in eight of nine (silicon
       72.22 against 72.32). Two analyses do not agree to 0.01 percent in six oxides, so 68 is 67 entered again. No
       other pair agrees exactly in more than three of the seven columns other than barium and iron (mostly zero).
     - Shared refractive index: rows of different types, certainly different objects, share it 16 times where chance
       gives 17; same-type rows with the oxides far apart 7 times against 7; same-type rows with every oxide within
       analytical noise 9 times against 2.0 (p = 0.0005), and with the oxides within 0.5 standard deviations 7 times
       against 2.4 (p = 0.013).
     - Fragments of one object measured one by one would pile up at refractive indices 0.00001 to 0.00005 apart; the
       oxide-matched pairs there number 14 against 12.6 by chance (moves of up to 0.00015 for this test; p = 0.37).
       So an object's rows carry one value, and the identical value is what marks them.
     - The 76 near-copies of this issue (within 0.16 standard deviations): 45 have their copy more than 0.0001 away
       in refractive index, 2.5 times the spread within one window, and 8 have it at the identical value.
     - The 7 objects: Ids 67-69, 63/65 and 12/15 (float windows), 139/140, 73/82, 77/88 and 91/97 (non-float
       windows). Four sit within 3 Ids of each other in the file, three are 6 to 11 apart, where a test on file
       neighbours misses them.
     - These 15 rows score as known: under a random split TabPFN's log loss on them is 0.11 against 0.60 on the other
       rows, and 0.23 to 0.24 once their object is held out (random forest 0.25, then 0.37).
   * **Key:** the identical refractive index, an exact value from the data[^a2]: 178 groups (146 single rows, 29
     pairs, 3 triples). Besides the 7 objects it joins 25 other sets of rows that share a value. Most share it by
     chance (15 of the 32 shared values span two types), which costs only some freedom in balancing the folds; a few
     may be objects whose oxides differ more than the tolerance used above, and the key holds those out too. A key
     from the oxides would need a tolerance, which is barred[^a2].
   * **Scores** (log loss, repeated stratified 3-fold, mean over repeats; logistic regression, random forest and
     untuned LightGBM 20 repeats, TabPFN 30, 10 on the bound):

     | Split | Logistic regression | Random forest | LightGBM | TabPFN |
     |---|---|---|---|---|
     | Random (as shipped) | 1.013 | 0.667 | 1.117 | 0.562 |
     | Grouped on the identical refractive index | 1.001 | 0.674 | 1.169 | 0.581 |
     | Random groups of the same sizes (control) | 0.993 | 0.657 | 1.092 | 0.561 |
     | Only the 7 objects grouped | 0.997 | 0.675 | 1.139 | 0.571 |
     | Near-copy clusters within 0.16 SD (bound; barred as a key) | 1.080 | 0.776 | 1.235 | 0.642 |
     | Random groups of those sizes (control) | 1.009 | 0.666 | 1.123 | 0.552 |

     - Grouping on the identical value costs TabPFN 0.019 and the random forest 0.007 (standard errors about 0.01),
       and logistic regression nothing, as it does not use the copies; the ranking stays (TabPFN, random forest,
       logistic regression, untuned LightGBM). The cost sits on the rows that share a value: TabPFN's loss on
       the 15 rows doubles, the 52 rows of the other shared values lose 0.03 (TabPFN) and 0.02 (random forest),
       and the single rows do not change. Random groups of the same sizes score as the random split.
     - If every near-copy were an object, which the refractive index rules out for most, holding them out would cost
       0.07 to 0.11. Those clusters chain into one of 28 rows and one of 13, so part of that cost is holding out a
       range of compositions, not objects.
   * **Consistency:** follows superconductivity (grouped on the exact composition, though a random split cost at most
     0.009 R²) and concrete_compressive_strength (a mix from identical values in seven columns). It differs from
     maternal_health_risk, where a hash of the whole feature vector was barred as a stand-in for collection sites the
     file does not hold: here the rows of an object are the rows that share the value. It changes your keep of
     2026-10-20, which held out only file neighbours.
   * **Unknown:** whether each of the 7 is one object analysed more than once or one record entered again; only the
     collector's case records would say, and both go together under the key.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split (implemented) | 213 rows, random 3-fold; the note gives the copies | as shipped; the 15 rows are 7% of the data | 7 objects can sit on both sides, and their rows score as if known; a lab never sees the object of a new fragment |
     | B | Grouped on the identical refractive index | a group column from identical refractive index values (178 groups), grouped 3-fold; the refractive index stays a feature | every test object is new, as in casework; an exact key; costs TabPFN 0.019 and the random forest 0.007, ranking unchanged | also groups 25 other sets of rows with a chance tie (harmless); rests on reading the shared value as the object's |
     | C | Retire | record `No (Retired)`; folder removed | none found | the groups can be recovered, so the rule for lost groups does not apply[^a3]; a task whose methods spread leaves |

   * **Recommendation:** B: the use case is a fragment of a new object, so the test objects must be new even where a
     random split costs little[^a1], and the identical value recovers them exactly. **Decision:** keep the random
     split (A), group on the identical refractive index (B), or retire (C)?
   * **Sources:** Lambert JA, Evett IW. The refractive index distribution of control glass samples examined by the
     forensic science laboratories in the United Kingdom. Forensic Science International 1984;26(1):1-23,
     https://doi.org/10.1016/0379-0738(84)90207-x. Curran JM, Hicks TN, Buckleton JS. Forensic Interpretation of
     Glass Evidence. CRC Press, Boca Raton; 2000. ISBN 0-8493-0069-2. Evett IW, Spiehler EJ. Rule induction in
     forensic science. In: KBS in Government. Online Publications, Pinner; 1987: 107-118 (contents as summarised in
     the genetic programming bibliography, https://gpbib.cs.ucl.ac.uk/gp-html/evett_1987_rifs.html). Ripley BD.
     Pattern Recognition and Neural Networks. Cambridge University Press; 1996; notes to the data,
     https://www.stats.ox.ac.uk/pub/PRNN/README.

   **Notes for the AI:** on B, in `dataset.py`: after `drop_duplicates`, add the group column
   `df["same_ri"] = df.groupby("RI", sort=False).ngroup().map("ri_{:03d}".format)` (178 groups), a
   `grouping = Grouping(on="same_ri", labels="per_sample", prediction_unit="row", context="none", definition=...)`,
   a `splits_comment` and `_feature_types` declaring the column categorical, as in concrete_compressive_strength
   (definition: rows with the identical refractive index; the rows of one object share the value, 7 clear objects
   with 2-3 rows, the other 25 shared values mostly chance ties), `task_summary.split` "Grouped on the identical
   refractive index, so a test fragment's object is never in training", and replace "so the split stays random" at
   the end of the row-order bullet of `curation_comments` with the key and the numbers above. Id 68 stays (the
   group keeps it with 67; the source's rows are kept). Record: `required_split: Grouped (NON-IID)`, a
   `CC (2026-11-05, Andrej):` line with the reason in bullets and the four sources; CHANGELOG entry;
   `dataset check`; not rebuilt. On A: extend the row-order bullet with "7 objects (15 rows) share an identical
   refractive index with oxides within noise; the identical value is not grouped". Tests: chance
   level from jittering the refractive index by up to 3, 5 or 10 steps of 0.00001 (p 0.0015, 0.0005, below 0.0005);
   nominal analytical tolerances for "within noise" in weight percent: Na 0.3, Mg 0.15, Al 0.1, Si 0.4, K 0.08,
   Ca 0.2, Ba 0.1, Fe 0.1.

   [^a1]: **SPLIT-4** (Must): if the deployed model predicts for an entity new data would not contain, the test
     entities must be new, even when a random split costs little; **SPLIT-30** (Must): re-split when the context says
     the rows share an entity new data would not have (the use case predicts for new entities); **LEAK-17** (Must):
     repeated entities in different rows leak the target across the split even when the rows differ, so keep one row
     per entity when the use case is that row, or group.
   [^a2]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data (identical values
     in the columns that define the entity), never on a similarity-threshold cluster or a hash of the feature vector
     standing in for an unknown entity; **SPLIT-26** (Should): take the group key from the source's own data, at the
     resolution the features see, and keep the source's rows.
   [^a3]: **SPLIT-25** (Must): when the real groups matter and cannot be recovered, retire the dataset rather than
     group on a guess.

   **Andrej (2026-11-05, discuss):** This does not feel like a grouped split but rather as something between an IID
   split and a grouped split. Basically, there are no clean groups governing the data generation process, but also
   the test data does not appear random. I believe we need to think deeply whether there are other cases like this
   that we have overseen and how this would be formally called in the literature. It might also make sense to define
   a new split type for that. But we need to brainstorm it first.

   **Answer (AI, 2026-11-06):**

   * **In short:** the literature has names for the parts, not one name for the whole. The data are partially
     clustered: most rows are single units, a few are repeated records of one unit, and the membership is not
     recorded. A random split then puts repeats on both sides, which leakage taxonomies call non-independence between
     training and test samples. A split between random and grouped exists in spatial statistics as nearest-neighbour
     distance matching, which picks the folds so that test rows lie as far from the training rows as new cases will.
     About ten datasets of the working copy are in the same position.
   * **Names in the literature:**
     - Partially clustered data: some units belong to clusters, the rest are singletons (Baldwin et al. 2011). Here
       the membership is latent.
     - Recovering it is record linkage, or entity resolution: pairs are compared field by field, and the match rule
       follows from how often true matches and chance pairs agree (Fellegi and Sunter 1969). The test of 2026-11-05
       on the refractive index did this, with the chance rate from jittered values.
     - What it does to a benchmark is train-test overlap. Duplicates in the data and non-independence between
       training and test samples are two of the leakage types of Kapoor and Narayanan (2023). Near-duplicates
       inflated the scores of code models by up to 100% (Allamanis 2019), and 3.3% of CIFAR-10's and 10% of
       CIFAR-100's test images had one in training (Barz and Denzler 2020). Random splits overrate models in
       general, and several deliberately biased splits estimate better (Søgaard et al. 2021).
     - Splits by similarity: scaffolds and Butina clusters for molecules (Wu et al. 2018; Butina 1999), leave one
       cluster out for materials (Meredig et al. 2018), blocks and buffers for spatial and other structured data
       (Roberts et al. 2017; Le Rest et al. 2014), and DataSAIL, which sets a split as an optimisation that keeps
       similar items apart and separates identity-based from similarity-based splits (Joeres et al. 2025).
     - Between random and grouped: nearest-neighbour distance matching cross-validation (Milà et al. 2022; the
       k-fold version, Linnenbrink et al. 2024) fits the folds so that each test row's distance to its nearest
       training row follows the distances of the cases to be predicted. Random folds are too optimistic when the
       samples cluster, block folds too pessimistic when they do not.
   * **Best fit:** "partially clustered data with latent membership" names what the data are, "train-test overlap"
     what it does, and distance matching the split you describe. In our own words: latent repeats, rows of one unit
     recorded more than once without an id.
   * **Two kinds of closeness:** a latent repeat (one truck, wine, car, glass object, company or policy recorded
     twice) gives the label away and should not cross the split. Distinct units that look alike (one product, postal
     area, survey profile or chemical series) are the population new cases come from, and a random split over them
     matches the use, molecules excepted[^b3]. The glass data has both: the 7 objects of the first kind, the other
     near-copies of the second.
   * **Datasets in the same position** (random split, repeats or near-copies across it, no clean id):

     | Dataset | What repeats | How much | Where it stands |
     |---|---|---|---|
     | aps_failure | a truck read again: rows equal in 140 to 169 of 170 counters | 30% of rows; 21% of test rows | issue 1 open: one row per truck by that match |
     | splice | one 60-base window in overlapping GenBank entries | 7.7% of test rows | issue 1 open: drop or group |
     | wine_quality | one wine listed twice, one value re-entered (10 of 11 values) | 49 pairs; 1.3% of test rows | issue 1 open: drop |
     | fiat_500 | a car listed again (trim, power, age, odd mileage) | 1.2% of test rows escape the key | open; "This should not be IID" (2026-11-04) |
     | forensic_glass_identification | an object's rows share the refractive index | 7 objects, 15 rows | this issue |
     | naticusdroid_android_permissions_dataset | one permission set kept as a benign and a malware row | 96 sets, 2.6% of rows | issue 1 open |
     | labour_inspection_compliance | an organisation inspected again, no organisation id | 52% of rows in near-identical clusters; the random split gains 5.9% of the skill | random kept |
     | fremtpl2 | one policy in consecutive years, linked by driver age plus one | inferred chains | random kept (2026-11-05, Lennart) |
     | polish_companies_bankruptcy | one company in each yearly file, linked by an accounting identity | 97% of the 5year statements | one file used |
     | coil_2000, ai4d_lab_tanzania_tourism_classification_challenge, allstate_claims_severity, huntprohibited_1m | distinct units with one coarse profile, or re-posted ads | 21-22% and 9.9% of test rows; 4.1% of claims; 1.4-4.9% of test ads | random kept; grouping costs at most 7.9% of the skill where measured |

     - The probe for hidden groups misses two known groups with small gaps (cardiotocography, micro_mass), and two
       datasets whose repeats could not be recovered were retired (maternal_health_risk,
       hazelnut_spread_contaminant_detection)[^b4].
   * **What the rules allow now:** grouping takes only exact keys[^b1], while near-exact copies over many columns
     are dropped[^b2]. So the similarity judgment that may drop a row (aps_failure: 140 of 170 counters;
     wine_quality: 10 of 11 values) may not group it. fiat_500's odd against round mileages (Lennart, 2026-10-14) and
     the glass test on the refractive index already calibrate a match against chance.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split with the overlap reported (current practice) | each random-split dataset reports the share of test rows with a copy or near-copy in training, against its chance level | no new machinery; done for labour_inspection_compliance, coil_2000 and others | scores stay optimistic where the copies are repeats; a number, not a fix |
     | B | Exact keys only (current rule) | group or drop on exact keys (glass refractive index, concrete mix, fiat_500 odd mileage) | inside the rules; no threshold to argue | misses repeats that differ in a value or two (aps_failure, wine_quality) |
     | C | Linked keys, calibrated | a key from record linkage (near-exact agreement over many columns, or a rare value), allowed when a chance null shows most linked pairs are real; grouped or deduplicated by the use case | one rule for dropping and grouping; testable; covers aps_failure, wine_quality, fiat_500 and glass | a rule amendment; calibration work per dataset |
     | D | Distance-matched split (a new regime) | folds chosen so that test rows lie as far from training as new cases will | the formal "between random and grouped"; tunable | needs the distances of new cases, which one release seldom gives; new machinery |
     | E | Buffered folds or a purged test | per fold, training rows within a set distance of a test row left out, or test rows with a near-copy dropped | keeps the random test rows; no groups needed | a threshold; smaller training sets; purging test rows changes the test mix |
     | F | Two scores | random and grouped or linked splits both shipped | shows the optimism | two leaderboards; twice the compute |

   * **Recommendation:** C with A: amend the grouping rule so that a calibrated linkage key counts as constructed from
     the data, and report the overlap for every random-split dataset. No new regime is needed: once linked, the split
     is grouped, and a tag can mark the key as linked, as the forced tags mark a split. D stays the reference for the
     name and for later, when new cases can be sampled. For glass, C gives the key of issue 2's B. **Decision:** open
     a cross-dataset item with these datasets and draft the amendment and the tag (C with A), draft a new split type
     (D), or keep the rule and settle each dataset on its own (B)?
   * **Sources:** Allamanis M. The adverse effects of code duplication in machine learning models of code.
     Proceedings of Onward! 2019, ACM, 143-153, https://doi.org/10.1145/3359591.3359735. Baldwin SA, Bauer DJ, Stice
     E, Rohde P. Evaluating models for partially clustered designs. Psychological Methods 2011;16(2):149-165,
     https://doi.org/10.1037/a0023464. Barz B, Denzler J. Do we train on test data? Purging CIFAR of near-duplicates.
     Journal of Imaging 2020;6(6):41, https://doi.org/10.3390/jimaging6060041. Butina D. Unsupervised data base
     clustering based on Daylight's fingerprint and Tanimoto similarity. Journal of Chemical Information and Computer
     Sciences 1999;39(4):747-750, https://doi.org/10.1021/ci9803381. Fellegi IP, Sunter AB. A theory for record
     linkage. Journal of the American Statistical Association 1969;64(328):1183-1210,
     https://doi.org/10.1080/01621459.1969.10501049. Joeres R, Blumenthal DB, Kalinina OV. Data splitting to avoid
     information leakage with DataSAIL. Nature Communications 2025;16:3337,
     https://doi.org/10.1038/s41467-025-58606-8. Kapoor S, Narayanan A. Leakage and the reproducibility crisis in
     machine-learning-based science. Patterns 2023;4(9):100804, https://doi.org/10.1016/j.patter.2023.100804. Le
     Rest K, Pinaud D, Monestiez P, Chadoeuf J, Bretagnolle V. Spatial leave-one-out cross-validation for variable
     selection in the presence of spatial autocorrelation. Global Ecology and Biogeography 2014;23(7):811-820,
     https://doi.org/10.1111/geb.12161. Linnenbrink J, Milà C, Ludwig M, Meyer H. kNNDM CV: k-fold
     nearest-neighbour distance matching cross-validation for map accuracy estimation. Geoscientific Model
     Development 2024;17(15):5897-5912, https://doi.org/10.5194/gmd-17-5897-2024. Meredig B, Antono E, Church C,
     et al. Can machine learning identify the next high-temperature superconductor? Examining extrapolation
     performance for materials discovery. Molecular Systems Design & Engineering 2018;3(5):819-825,
     https://doi.org/10.1039/C8ME00012C. Milà C, Mateu J, Pebesma E, Meyer H. Nearest neighbour distance matching
     leave-one-out cross-validation for map validation. Methods in Ecology and Evolution 2022;13(6):1304-1316,
     https://doi.org/10.1111/2041-210X.13851. Roberts DR, Bahn V, Ciuti S, et al. Cross-validation strategies for
     data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 2017;40(8):913-929,
     https://doi.org/10.1111/ecog.02881. Søgaard A, Ebert S, Bastings J, Filippova K. We need to talk about random
     splits. Proceedings of EACL 2021, 1823-1832, https://doi.org/10.18653/v1/2021.eacl-main.156. Wu Z, Ramsundar
     B, Feinberg EN, et al. MoleculeNet: a benchmark for molecular machine learning. Chemical Science
     2018;9(2):513-530, https://doi.org/10.1039/C7SC02664A.

   **Notes for the AI:** the candidates come from a search of the REVIEW.md and dataset.py of the 96 folders without
   `grouping` or `temporal` for near-copy, duplicate, twin, replicate and hidden-group wording, read one by one; no
   new model runs. On C with A: a cross-dataset item under a "Splits" section of
   `datasets/_dev/tabarena-v0pt2/REVIEW.md` listing the table above; a drafted amendment to the grouping rule (a
   linkage key is allowed when the domain names the unit, the match comes from many columns agreeing exactly or a
   rare value, the threshold comes from measurement repeatability or the record's structure and never from the
   score gap, and a chance null, jitter or a correlation-keeping shuffle, shows most linked pairs are real), with
   the near-copy drop rule pointing to it; a tag for a linked key (name to settle, such as `LinkedGroups`); the
   overlap number from the hidden-group probe's near-copy share and `test_rows_seen`. The coordinator's reference
   "Lazarus et al." could not be found and is left out.

   [^b1]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data, never on a
     similarity-threshold cluster.
   [^b2]: **LEAK-18** (Should): many degrees of freedom and an exact match is a collection artefact, so drop it and
     give the share; **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped on the
     duplicate key.
   [^b3]: **SPLIT-31** (Should): over related entities, a random split can match how a task is framed even when it is
     optimistic; molecules with exact structures are grouped on the Bemis-Murcko scaffold.
   [^b4]: **SPLIT-25** (Must): when the real groups matter and cannot be recovered, retire the dataset rather than
     group on a guess.

   **Andrej (2026-11-06, chat):** On whether a key linked by measured agreement, with its chance rate, may group rows:
   "Yes, but this is a case by case decision depending on how certain we are that the key works." On repeats whose
   units cannot be recovered: drop the copies, and "it should always be a discussion point if the target is still
   representative then."

   **Answer (AI, 2026-11-06):**

   * **What changed:** the rules now name this case entity leakage and let a link calibrated against chance group
     rows, decided case by case by how certain it is[^c1]. That is the middle ground you asked for: group what the
     evidence ties to one object, leave the rest random.
   * **Verdict for this dataset:** two kinds of near-copy, two verdicts[^c2].
     - 7 objects (15 rows): one object recorded more than once, with each row its own measured fragment, so the fix
       is to hold the object out whole.
     - Every other near-copy: different objects of the same float-glass product, the kind of glass a casework
       fragment is compared with, so a random split over them matches the use.
   * **The three tests:**
     - **The link is real:** same-type rows with the identical refractive index and every oxide within the
       tolerance of two analyses of one glass (Na 0.3, Mg 0.15, Al 0.1, Si 0.4, K 0.08, Ca 0.2, Ba 0.1, Fe 0.1
       wt%): 9 pairs where chance gives 2.0 (the index moved at random by up to 0.00005, 2,000 draws; p = 0.0005;
       2.5 and p = 0.0015 at 0.00003). With a doubled tolerance 14 pairs against 7.0, so the looser pairs are mostly
       chance, and the identical index alone joins 25 further sets that tie by chance (15 of the 32 shared values
       span two types).
     - **The label travels:** the 15 rows score as known, TabPFN log loss 0.11 under the random split against
       0.23 to 0.24 with their object held out.
     - **No order:** no dates; the file is sorted by class and by magnesium.
   * **How certain:** strong for the set (9 against 2), weaker pair by pair: about 2 of the 9 links may be chance.
     Only the collector's case records would settle each one.
   * **Cost:** only the 7 objects grouped, TabPFN 0.571 against 0.562 random and 0.581 on the identical index;
     random forest 0.675, 0.667 and 0.674; the ranking stays.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split (implemented) | 213 rows, random 3-fold; the note gives the copies | as shipped; the 15 rows are 7% of the data | 7 objects can sit on both sides, and their rows score as if known |
     | B | Grouped on the identical refractive index | 178 groups, grouped 3-fold | exact, no tolerance | also holds out 25 sets of rows that tie by chance |
     | D | Grouped on the 7 objects | a group column from the calibrated link (identical index, oxides within the tolerance of two analyses, same type); every other row its own group | holds out only what the evidence ties to one object; the near-copies of one product stay as the population a lab compares with | about 2 of the 9 links may be chance; the tolerance is our choice, from the measurement and not from the score |
     | C | Retire | record `No (Retired)`; folder removed | none found | the objects can be recovered, so the rule for lost groups does not apply |

   * **Recommendation:** D: a fragment from a crime scene comes from an object the reference collection does not
     hold, and the link recovers those objects with a chance rate of 2 in 9, while the other near-copies are the
     glass of one product that the collection rightly holds[^c3]. **Decision:** keep the random split (A), group on
     the identical index (B), group the 7 objects on the calibrated link (D), or retire (C)?

   **Notes for the AI:** on D, in `_clean`: a group column `glass_object`, the connected components of the pairs with
   the identical `RI`, the same type and every oxide within the tolerances above (the check's `suspected_objects`); `grouping = Grouping(on="glass_object", labels="per_group",
   prediction_unit="row", context="none", definition=...)` with the use case (a fragment of an object not in the
   collection) and the chance rate; no forced tag (no time); the curation notes give the link, the tolerances, the
   chance rate (9 against 2.0) and the verdict for the other near-copies. Record `required_split` Grouped, `CC` line.
   `dataset check`, the group probes, no rebuild until asked. Issue 4 (Id 68) is separate.

   [^c1]: **SPLIT-24** (Must, amended in draft PR #62): group on a true id or one constructed from the data, exactly
     or by a calibrated link: a match rule from how the data were recorded and a chance rate showing most links are
     real; whether it holds is the curator's call, case by case. **LEAK-43** (Should, draft PR #62): three tests set
     the verdict (is the link above chance, does the label travel with it, is there an order).
   [^c2]: **LEAK-42** (Must, draft PR #62): repeats of a unit the data does not record are natural (distinct
     look-alikes, random split), an entity fix (units recovered: copies dropped, observations grouped), a temporal
     fix, or not recoverable (identifiable copies dropped).
   [^c3]: **SPLIT-23** (Must): the source's use case decides what one prediction is and what is known about a new
     group when predicting.

   **Andrej (2026-11-12, discuss):** Reply (A): Random split, but note that this was a decision we made

   **Resolved (2026-11-12, Andrej):** A: the random split stays, written down as our decision. The definition's
   `splits_comment` now says that the random split is a deliberate choice (2026-11-12, Andrej, review issue 2, A) and
   why: no clean groups govern how the collection was made; only 7 objects (14 rows once Id 68 is dropped, issue 4)
   are tied together by the calibrated link, 7 pairs where chance gives 1.8; the other near-copies are glass of one
   product that a reference collection holds; holding out the 7 objects cost TabPFN 0.009 log loss, ranking unchanged.
   The row-order bullet of `curation_comments` gives the near-copy shares on the 212 rows (6 rows within 0.08 SD, 75
   or 35% within 0.16 SD) and the 7 objects. The issue drafts no `Time basis:` line; issue 3's `Timeless` line stands.
   Record CC line. `dataset check`: 0 errors, 0 warnings; not rebuilt.

3. **Time basis: name the split `Timeless`, as the glass type is a property of the object?**

   * **Problem:**
     - Each row is a reference fragment whose type comes from the object it was broken from, and the refractive index
       and the eight oxides are measured on that fragment, so nothing in a row arrives after the measurement.
     - The record carries `Samples: No Time Dimension` with no time or target fact, and the definition names no time
       basis, although the fragments were collected from casework over unstated years before September 1987.
     - `Timeless` names a target that is a fixed property of the item; whether rows of one object sit on both sides is
       a grouping question, which is issue 2 and not an arrival one[^3a].
   * **Background:**
     - Nothing dates a row: the names file and the UCI page give only the donation (September 1987), and the Id order
       is a sort by class and, within a class, blocks running from high to low magnesium, which the features predict
       at Spearman 0.67 to 0.90.
     - What the collection holds does depend on when it was built: 36% of the fragments are non-float window glass,
       hardly made since the mid-1970s, and today's casework compares trace elements instead of major oxides (the
       `Outdated` marker), a drift no split of this release can test.
     - The class shares are the collection's and not casework's, which is already the approximate fit.
   * **Effect on the task:** none on the data, split or score; the line states why a split that is not temporal is
     safe in time, and what it cannot test. It holds whichever option issue 2 takes, with the split named accordingly.
   * **Experiments:** the time probe on the source file (b1 run, 2026-11-06) flags only the sort by class and the
     dropped `Id`; it finds no date-like column and no column that encodes a period (`Ba` and `Fe` are listed, but
     they are mostly zero).
   * **Consistency:** follows the undated reference catalogues of this review that recommend `Timeless`
     (biogeographical_ancestry_prediction, musk, the QSAR sets); the catalogue-drift question it leaves open is the
     one raised for superconductivity and the QSAR sets, with nothing here to date a fragment.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | `Timeless` | the tag and a `Time basis:` line naming the fixed glass type, the lab measurement and the 1987 collection the split cannot move past | states the fact the split rests on; names what the split cannot test | none found; no data, split or score changes |
     | C | `Samples: Over Time`, `Time: Lost` and a forced tag | the record's fact changed and the split tagged as forced from temporal | reads the collection as casework gathered over years | a fragment's type does not move with the year it was collected, nothing dates a row, and no dated window exists to measure what the tag costs |

   * **Recommendation:** B: the type belongs to the object and the measurements to the fragment, so no row is in the
     future of another; the collection's own date is recorded by the `Outdated` marker and belongs in the line.
     **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `IID`, or the grouped
   tags on issue 2's B) and a curation bullet `- Time basis: Timeless: the glass type is a property of the object the
   fragment came from, and the refractive index and oxides are measured on the fragment, so nothing in a row arrives
   later. The Home Office laboratory gathered the fragments from casework before September 1987 and no date is
   published; the Id order is a sort by class and by magnesium within it. Not tested: glass made since then (36% of
   the rows are non-float window glass, hardly made since the mid-1970s) and today's trace-element casework.`;
   `splits_comment` unchanged; `dataset check`; no rebuild (comment only). On C, the record's `tags` change too.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts and a definition can name the use-case prototype it follows with a `Time basis:` line.
     `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's strength,
     a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by item family.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept five more routine `Timeless`
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (glass made since 1987, and today's trace-element casework); the split and `data_tags` are unchanged. The
   tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

4. **Drop Id 68, which is Id 67 entered again?**

   * **Problem:**
     - Ids 67 and 68 agree in eight of nine values and differ only in silicon (72.22 against 72.32), while two analyses
       of one glass do not agree to 0.01 percent in six oxides, so 68 reads as 67 typed in a second time.
     - A record entered twice is a copy, not a second fragment, and the rules drop copies of one record[^4a].
     - Every drop asks whether the target still stands for the use case; this one moves one row of building windows
       (float) from 69 to 68 of 212 rows.
   * **Background:** the v0.2 definition already drops Id 40, an exact copy of Id 39. Id 69 shares 67's refractive
     index with its oxides within the tolerance of two analyses, so it is a second fragment of the same object (issue 2)
     and stays.
   * **Effect on the task:** under a random split one of 67 and 68 can sit in training and give the other's type away;
     under issue 2's D they are held out together, and the copy then only counts one fragment twice.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep Id 68 (implemented) | 213 rows | nothing to change | one record counted twice |
     | B | Drop Id 68 | 212 rows, as for the copy of Id 39 | one row per record; class shares move by less than 0.2 points | rests on reading a silicon difference of 0.1 as a typing error |

   * **Recommendation:** B: six oxides equal to the hundredth are not two analyses, and the drop leaves the class
     shares as they are. **Decision:** keep (A) or drop (B) Id 68?

   **Notes for the AI:** on B, drop `Id == 68` in `_clean` next to the drop of Id 40, with a curation bullet (the eight
   equal values, silicon 72.22 against 72.32, read as one record entered twice); `CC` line in the record; `dataset
   check`.

   [^4a]: **LEAK-42** (Must, draft PR #62): copies of one record (entered twice, listed again) go down to one row per
     unit, and every drop states what it does to the target. **LEAK-18** (Should): an exact match over many values is
     a collection artefact.

   **Resolved (2026-11-12, Andrej):** B (`ok`): `_clean` drops Id 68 before the Id column goes, with a curation
   bullet (eight values equal to Id 67's, silicon 72.32 against 72.22, one record entered twice); 212 rows, 68 float
   building windows; `task_summary.row` says 212 fragments. The accepted row-order warning no longer fires on the
   212-row shuffle and is removed. Record CC line. `dataset check`: 0 errors, 0 warnings; not rebuilt.

## Reference

@misc{German1987glass,
  author       = {German, B.},
  title        = {{Glass Identification}},
  year         = {1987},
  howpublished = {UCI Machine Learning Repository},
  note         = {{DOI}: https://doi.org/10.24432/C5WW2P}
}
