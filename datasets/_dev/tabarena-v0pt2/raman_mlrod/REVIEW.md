# raman_mlrod

**Outcome:** added. The ML Raman Open Dataset (Berlanga, Williams and Temiquel 2022): which mineral sits at a point of a
rock never measured before, from one Raman spectrum (950 bands of 1 cm-1, 150-1,099 cm-1, 15 classes). 125,244 spectra:
90,387 of 35 reference and powder maps train, and one test fold holds the gabbro slab (18,646) and the granite slab
(16,211), clean and under 50% basalt dust, as in the source's own split; scored by log loss (our default, since the
source reports only accuracy), read per rock too. Built from a third-party mirror of the 41 files (ODR refuses this
machine); three files you downloaded from ODR match it byte for byte. The AI recommends shipping it after the panel's
changes, which are made. The paper you supplied settles two of the three gates the panel set (the slabs were labelled by
hand; the reference maps are separate hand samples), so the record's `TBD` now waits only on issue 1: one more file and
ODR's file list.
Verdict: ship after changes (made); `TBD` until issue 1 is settled; issue 4 after a GPU run.
Validity: SEL-12 open: the source's own spectrum CNN scores 1.00 accuracy on the clean slabs, an untuned logistic
regression 0.934, so whether tabular models are competitive waits for a tuned run (issue 4; SEL-15's default leans
keep). USE-5 holds: the slab labels are a person's calls, checked against the source's CNN (paper, Sec. 4.2; issue 2);
fit approximate, the gap named in `fit_reason` (a lab microscope for a rover instrument, a closed set with no "no call",
labels that name the grain in the gabbro and the spot in the granite). SPLIT-1, SPLIT-4, SPLIT-29 hold: grouped by rock,
IID barred (log loss 0.072 at random against 0.63-1.64 by rock). SPLIT-19 applied: the source's split, train on the
reference maps and test both rocks in one fold (the draft had one fold per rock with the other rock in training, which
let the training rock tell the test rock's class set). SPLIT-24 / LEAK-17: the 46-spectrum gypsum and forsterite-albite
powder map named after the gabbro now trains; the two reference maps that match a slab mineral closely are separate
specimens by the paper's Table 1 and stay (issue 3). LEAK-9: a protocol line (each spectrum predicted on its own) and a
kept-on-purpose note with the task gamer's measured gains. LEAK-13: one reading per band in place of the source's band
minimum, which left a trace of the wavenumber grid by class (comb ROC AUC 0.651 to 0.536). PROV-13: the dusty gabbro's
code 9 repaired to anorthite (holds on every test); the spreadsheet fill-down in one reference spectrum masked (ODR's
own file holds it too); PROV-1: three of four checked files match ODR, the rest is issue 1.
Value: MET-5, MET-6: log loss, the fallback (the source scores accuracy and per-class F1 on the most likely class).
TP-5, TP-8 hold. Few groups weighed − (two test rocks; per-row standard errors understate the noise 4-13x).
Quality: CLEAN-26: the spectrum declared, raw; three damaged reference spectra masked (1,168 cells); wording fixed (the
code's citation, readings per band, saturation counts, the metric's threshold, the dust asymmetry, the rare-class loss
shares, the encodings table on the new grid, the licence note).
Weighed: few groups −, the source's own design +, a real lab and rover task +, a strong spectrum-model incumbent −
(open).
Probes on the final definition (one split): task probes, log loss: linear 0.961 against the class shares' 2.603 (62.7%
lower), LightGBM 2.501 (untuned, it barely beats the class shares: with default settings the trees put near-certain
probability on the wrong mineral of a rock they never saw, and log loss punishes that hard; their accuracy is 0.865 on
the clean slabs, issue 4), random forest 3.102, the best single band 5.498; flags only the small classes
(forsterite-albite mix 3 test rows, gypsum none). Dtype probe: 0 of 950 bands flagged. Leak probes (macro ROC AUC): all
bands 0.910, the best band alone 0.661, a depth-3 tree 0.565, the number format 0.496 (0.537 under the band minimum), no
exact copies across the split. Group probe: LightGBM 1.000 on a random split against 0.905 by rock; across groups
logistic regression 0.675, LightGBM 0.660 (baseline 0.5). On the source's own labels (code 15 kept, code 9 not repaired,
the same split): linear 4.217 against 5.642 for the class shares (21.2% lower): the 4,817 code-15 points have no class
to learn and the 3,540 points labelled microcline are anorthite, which is why the definition drops the one and repairs
the other.
For the curator: issue 1 (one file to compare, ODR's file list and the licence it states), issues 2 and 3 (answered by
the paper; confirm), issue 4 (SEL-12, after the run), issue 5 (design A, only if you want it), issue 6 (the four warning
texts, yes or no).

**Main points:** Issue 1 is the last check before the record leaves `TBD`: download one file from ODR, compare its
sha256, and note ODR's file count and licence. Issues 2 and 3 are answered by the paper you supplied (labelled by hand;
the reference maps are separate hand samples): confirm. Issue 4 waits for a GPU run of the source's CNN against tuned
tabular models. Issue 5 asks nothing unless you want one fold per rock. Issue 6: the four warning texts, yes or no.

**Record judgment:** valid. A documented laboratory deposit (the paper with its sample table, an ODR deposit with a
DOI, the source's code on Zenodo) of measured Raman maps for a named identification task. The screening's open
question, how many physical specimens stand behind each class, is answered by the paper's Table 1: one hand-sample
specimen per mineral, of its own locality, and two slabs. The files come from a mirror; three of them match ODR byte
for byte (issue 1 for the rest).

**Issues for Lennart:**

1. **Does the last file match ODR, and does ODR hold more maps than our 41?**

   * **Problem:**
     - The definition is built from a third-party mirror (the raman-data package's Google Drive zip), because ODR answers this machine with a reCAPTCHA; you compared three of its files with ODR's on 2026-11-09 and all three match byte for byte, the file with the spreadsheet fill-down included[^prov].
     - Still to do in your browser: compare the fourth file, the dusty granite, and read ODR's file list and licence.
     - A match and 41 maps settle the source and lift the record's `TBD`; a mismatch means a rebuild from ODR's files; more maps mean a new scope (option C); a match with 41 maps is option A and nothing in the data changes.
   * **Your request (in a browser):**
     - Download `L_raw_granite50dust_test_015s_10000.csv` from https://odr.io/MLROD (doi:10.48484/PWRB-R137) and compare its sha256 (`shasum -a 256 L_raw_granite50dust_test_015s_10000.csv`) with 04d079761ab987f2d85d721ccc2447acd49e97243174c6527eef10518f90fb91 (163,027,169 bytes). Save it anywhere (it is not kept) and write the sum and 'match' or 'mismatch' into this issue; on a mismatch, keep the file for the rebuild (option B). It is the one file with no `og-idx` header, so the source's own reader fails on it, and it holds the 4,817 code-15 points.
     - Count the map files ODR lists: the mirror has 41 (ODR ids 63245 and 63641-63758); note whether id 63742, missing from that run, is a map, and whether any map beyond the 41 is there (the raman-data card says 4 mixtures, 3 here; NASA AHED's keywords name magnesium sulfates, a sulfide and basaltic glass).
     - Copy the licence text ODR shows (NASA AHED's text says CC BY-NC, its badge links CC BY-NC-ND 4.0); a note for the release checklist, never a reason for the verdict[^lic].
   * **Background:** already checked by you on 2026-11-09, each equal in size and sha256 to the mirror's file (a byte match, as for ai4d):

     | File on ODR | sha256 | bytes | Result |
     |---|---|---|---|
     | `L_raw_gabbro50dust_test_015s_9740.csv` | 1b8b6b592f1a60aca1d65feebee4efc1eeb90c7eaf287be446739b50eda38077 | 105,564,433 | match |
     | `L_raw_granite0dust_test_015s_4084_final.csv` | fc0d5132897101563167511eaba4d64ed672007737ebfce0daea4e07a2be01e0 | 70,455,751 | match |
     | `qtzalb_train_60s_3000.csv` | df16b22e4cb37bd43efb4efe8cb6ef4cce4f7d168e7f58ac2978fceb9022f831 | 32,476,361 | match: ODR's file holds the same fill-down, so it stays masked |

   * **Experiments:** the paper's Table 1 lists about 130,000 spectra (89,121 training, 39,720 test), close to the 130,061 the 41 files hold, so the "500,000+" of the abstract does not point to maps the paper describes.
   * **Consistency:** the three matches follow ai4d (a byte match settles a mirror); ugr16_isp_netflow_intrusion in this batch has the same situation (a mirror for a server that refuses this machine) and is decided alike.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the mirror (implemented) | the definition reads the mirror's zip; ODR named as the origin | three of four checked files match ODR byte for byte; one zip downloads by script | the dusty granite file and the file list still unchecked |
     | B | Rebuild from ODR's files | the download line names ODR's files | the origin's own bytes | ODR needs a browser for every file; nothing gained if the last file matches too |
     | C | Re-scope to ODR's full deposit | new maps added as reference maps or test rocks | the data the deposit holds | a new build and review |

   * **Recommendation:** A on a match and 41 maps, B on a mismatch, C if ODR holds maps the mirror lacks. **Decision:** does the dusty granite file match, and how many maps does ODR list?

   **Notes for the AI:**
   - A: a `CC` line with the date and the results (the three matches of 2026-11-09 and the fourth); `download_description` names the ODR check; the record leaves `TBD` (issue 4 does not hold it).
   - B: put the ODR files under `local-data-warehouse/raman_mlrod/odr/`, point `_load_raw` there, write the sums into `download_description`; the fill mask stays; re-run `dataset check` and the probes.
   - C: a new `/add-dataset` pass on the added maps.
   - Licence: write what ODR states into `license` as a note.

   [^prov]: **PROV-1** (Must): the data comes from its first publisher, or a copy proven equal to it. **PROV-13** (Must): a damaged value is repaired from the origin where it can be, else masked. **PROV-2**: the release as published, in full or the cut stated.
   [^lic]: **EV-4**: a licence is a note for the release checklist, never a verdict reason (Lennart, 2026-09-23).

2. **Were the slab maps labelled by hand or by a classifier?**

   * **Problem:**
     - The panel could not tell whether a person or the source's CNN set the test labels of the two rock slabs; if the CNN had set the granite's, models would be scored against another model's calls and the granite would leave the test[^use5].
     - The paper you supplied answers it: the authors labelled the spectra by hand, and used the CNN only to point at labels to check again.
     - The paper's Sec. 4.2 (quoted in the answer below) settles this for hand labels, so both rocks stay, as implemented: waiting only for your confirmation.
   * **Background:**
     - Signs of model-made labels the panel saw: code 15, the label of 4,817 dusty granite points, is what the source's code gives a prediction below its confidence cut; the dusty granite map is speckled (1,688 one-point runs among 3,691), while the gabbro maps come in whole blocks.
     - Signs of labels that read the spectrum: the dusty granite's feldspars show their own bands; a nearest-centroid check agrees with the labels on 77-100% of the points per class; the 147 dusty granite points labelled forsterite show the dust's iron-rich olivine (817 and 850 cm-1).
   * **Effect on the task:** the labels are a person's calls, but each pass was checked against the CNN, so where a person changed a call after a disagreement the label leans toward that CNN; the source's own 1.00 accuracy on the clean slabs is therefore partly self-confirming (issue 4).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both rocks with the note (implemented) | 34,857 test spectra; the notes quote the paper's labelling | the source's full test set; hand labels | the labels lean toward the source's CNN where a call was changed |
     | B | Filter the granite rows out | the test fold is the gabbro slab only (18,646 spectra) | none left: the plan applied it only to model-made labels | one test rock left; the granite's quartz, albite and micas never tested |

   * **Recommendation:** A: the labels are by hand. **Decision:** confirm A?

   **Notes for the AI:** B (only if you disagree): drop the rows whose `specimen` is `granite slab` from the split, update `task_summary`, `splits_comment` and the notes, re-run `dataset check` and the probes.

   [^use5]: **USE-5** (Must): the target is what the actor acts on; a label another model produced is no ground truth. An undocumented construction is allowed with a note. The remedy for a part that fails is the mildest one that works: filter those rows out, not exclude the dataset.

   **Answer (AI, 2026-11-09):** from the paper (Berlanga et al. 2022, Earth and Space Science 9(10), e2021EA002125, Sec. 4.2 "Labeling Test Models"):
   - "Over 30,000 spectra were manually labeled by the authors over the span of 500 hr and three full passes. These true labels were used to verify the success rate of our classifying models. With each pass, the test set was run through the CNN and the misclassified spectra often identified human mineral classification errors, effectively correcting any manual labeling mistakes."
   - Applied: the slab-labelling bullet of the notes quotes it and names the CNN check; `fit_reason` says "set by hand and checked against the source's CNN". Nothing else changes.
   - Also from the paper: its gabbro test set lists gypsum, and its 8,952 clean gabbro spectra include the 46-spectrum gypsum and forsterite-albite map, so the source tested that map with the gabbro. The definition keeps it in training (a 50/50 forsterite-albite lab powder is no point of a gabbro); the notes say so.

3. **Were the augite and muscovite reference maps measured on the slabs themselves?**

   * **Problem:**
     - The reference map `aug_train_15s_1000` matches the gabbro slab's augite as closely as a map matches itself, and `ms_train_015s_5900` matches the granite's muscovite block the same way; had either been mapped on a slab, that rock's mineral would have been seen in training.
     - The paper's sample table answers it: every reference map comes from a hand-sample specimen of its own locality, not from the slabs[^split24].
     - The paper's Table 1 and Sec. 2 settle this, so both stay reference maps, as implemented: waiting only for your confirmation.
   * **Background:**
     - The paper's Table 1: augite from Trento Province, Italy (6,103 spectra, the two augite maps together); muscovite from Ottawa, Ontario (5,900); the gabbro slab from Madagascar; the granite slab's locality "Unknown"; Sec. 2: "12 hand sample mineral specimens, four of which were mixed into three binary powders".
     - The 1,373-spectrum map `L_raw_granite0dust_test_030s_1373_final` (873 hornblende, 500 muscovite) stays with the granite: the paper's 11,028 clean granite spectra include it, and its granite test set lists hornblende and muscovite.
   * **Experiments:** what was at stake (logistic regression, split auditor): without `aug_train_15s_1000` the gabbro's augite accuracy falls from 0.822 to 0.002 and the gabbro's log loss from 0.784 to 2.551 (class shares 2.898); the gabbro's score leans heavily on one augite specimen from Italy, which the notes record.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both as reference maps (implemented) | they train; the notes cite the paper's localities | separate specimens by the paper; no regrouping on similarity | the gabbro's augite score rests on one specimen's map |
     | B | Join the slab's group | the map moves to that slab's test side | none left: the paper places them on other specimens | removes a separate specimen from training for no reason |

   * **Recommendation:** A: the paper names separate specimens. **Decision:** confirm A?

   [^split24]: **SPLIT-24** (Must): the groups follow the units the data names (a specimen, a map), never a cluster of similar rows. **LEAK-17** (Must): no unit on both sides of a split. **EV-6**: similarity is circumstantial evidence, not proof of a mechanism.

   **Answer (AI, 2026-11-09):** from the paper's Table 1: "Augite, Trento Province, Italy, 6,103 spectra; Muscovite, Ottawa, Ontario, 5,900; Gabbro slab, Madagascar; Granite slab, Unknown"; Sec. 2: "12 hand sample mineral specimens, four of which were mixed into three binary powders". Applied: the specimen bullet of the notes and `splits_comment` cite the localities; the split is unchanged.

4. **Is the source's spectrum CNN clearly better than tuned tabular models?**

   * **Problem:**
     - A spectrum stays in the benchmark only where tabular models are competitive with the models the field uses for it, judged per dataset; here the source's own CNN scores 1.00 accuracy on the clean slabs, untuned tabular models 0.80-0.93[^sel12].
     - A run settles the facts: the source's CNN against tuned tabular models and TabPFN v3.5 on the shipped split, on GPU.
     - "Clearly better" has no numeric line, so the call on that table is yours.
   * **Experiments:** shipped split (trained on the reference maps only), untuned, accuracy of the most likely class on the 19,980 clean slab spectra, the source CNN's exact test set (critic, re-run by the mediator, 2026-11-09):

     | Model | Clean slabs | Clean gabbro | Clean granite |
     |---|---|---|---|
     | source's Spec-CNN (its notebook, its own result) | 1.00 (macro F1 0.98) | | |
     | logistic regression, 100 principal components | 0.934 | 0.975 | 0.902 |
     | logistic regression on the standard normal variate | 0.906 | | |
     | LightGBM | 0.865 | | |
     | random forest | 0.830 | | |
     | k nearest neighbours | 0.801 | | |

     - On the dusty slabs the tabular models score 0.42-0.64; there is no CNN number on our labels.
     - On the earlier draft split (one fold per rock), the untuned trees scored worse than the class shares in log loss (random forest 3.158, LightGBM 2.906, class shares 2.766). On the shipped split, LightGBM is just under them (2.501 against 2.603) and random forest still worse (3.102): confident mistakes on unseen rocks, not a lack of signal (accuracy 0.83-0.87).
     - Task probes on this definition (untuned, one split, log loss): linear 0.961, LightGBM 2.501, random forest 3.102, class shares 2.603.
   * **Consistency:** bacteria_id_raman in this batch was recommended keep with a source gap of CNN 82.2% against logistic regression 75.7% accuracy; here the gap in error rate is larger and the tabular accuracy higher, a pair to decide alike. open_university and heart_disease were kept pending a measured run.
   * **Panel:**
     - Advocate: untuned tabular models already reach 0.93; the field also uses PLS-DA, SVM, random forests and kNN; the burden lies on "clearly better", and the slab labels are by hand but were checked against this CNN (issue 2), so its 1.00 is partly self-confirming: read the gabbro apart.
     - Critic: 6.6% error against 0% is not competitive on its face, and third parties put CNNs 8-10 points ahead (orientation only, not evidence).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep pending the run (implemented) | the dataset ships as defined; the run is a TODO, its table decides | the default leans keep; untuned tabular models already reach 0.93 | a spectrum model may be far ahead |
     | B | Exclude after the run | the record gets `No` (`Wrong Domain / Source Modality`) if the CNN is clearly ahead of the tuned tabular models on both rocks | keeps a spectrum task where tabular models are not the tool out | loses the only mineral Raman task |

   * **Recommendation:** A until the run; then B only if the CNN is clearly ahead of the best tuned tabular model and TabPFN v3.5 on both rocks, clean and dusty. **Decision:** after the run, keep or exclude?

   **Notes for the AI:** the TODO run, on GPU via SkyPilot (never local SLURM or CPU), TabPFN v3.5 (never v2):
   - models: the source's Spec-CNN (`cnnmodel_raw` of Spec-CNN, Zenodo 10.5281/zenodo.7036374, on the 950 bands as its input layer takes them), tuned LightGBM, CatBoost, RealMLP and logistic regression, and TabPFN v3.5;
   - the shipped split (train on the reference and powder maps, test both slabs), the declared log loss and the accuracy of the most likely class;
   - reported apart for the clean slabs, the dusty slabs, the gabbro and the granite;
   - put the table into this issue as `**Answer (AI, <date>):**`, then ask for the call; on B, the record's `suggestion` to `No` with the marker and a `CC` line, and the folder leaves the working copy with a CHANGELOG entry.

   [^sel12]: **SEL-12** (Must): vectorised signals (spectra) stay only where tabular models are competitive with the field's models, judged per dataset. **SEL-15** (weigh): the default leans keep; the burden is on "clearly better". **EV-4**: another paper's or benchmark's scores orient, they are no evidence; the source's own result counts.

5. **Test one rock per fold instead of the source's single split?**

   * **Problem:**
     - The draft tested each rock in its own fold with the other rock in training; the panel switched to the source's split (both rocks tested in one fold, the reference maps train), which is the default unless a fact sets the case apart[^split19].
     - The reason given for one fold per rock, that the other rock lowers the loss on both rocks, does not hold for the shipped spectrum (logistic regression: the gabbro 0.883 to 0.784, but the granite 1.065 to 1.307), and a score per rock is still read from the single fold.
     - Asks nothing unless you want one fold per rock.
   * **Effect on the task:** with one fold per rock, the training rock tells the test rock which minerals it lacks (the two share almost none): scaling those classes down lowers the best honest model's log loss from 0.666 to 0.477 with no test row seen, and an honest untuned LightGBM is worse with the other rock in training (2.757 against 2.410 on the reference maps alone; task gamer).
   * **Experiments:** the two designs rank five untuned models the same (Kendall tau 1.0; split auditor).
   * **Consistency:** heart_disease tests one hospital per fold with the others in training (kept 2026-10-27); every hospital there has both outcomes, while these two rocks share almost no classes, the fact that sets this case apart.
   * **Panel:** the split auditor and the domain practitioner prefer one fold per rock (a lab trains on every labelled rock it has; a score per rock); the advocate conceded to the source's split in rebuttal; the mediator found no fact that survives.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The source's split (implemented) | one fold: the reference maps train, both slabs are tested; scored by rock after the fact | the source's design; the class-set exploit and the confound are gone; costs no ranking | one split only |
     | B | One fold per rock | two folds, the other rock in training; needs a recorded exception | a lab's use of every labelled rock; a fold score per rock | the training rock tells the test rock's class set; an honest model scores worse; needs an exception with a fact the panel did not find |

   * **Recommendation:** A, the source's split. **Decision:** A or B?

   **Notes for the AI:** B: restore the two folds in `_make_splits` (reference maps plus the other rock train), write an "Exception to SPLIT-19" with the fact and the task gamer's exploit in `splits_comment`, re-run `dataset check` and the probes.

   [^split19]: **SPLIT-19** (Should): the source's split is the default; a departure needs a fact that sets the case apart and a higher principle it serves (principles.md, "Exceptions and amendments"). **SPLIT-1** (Must) holds under both: whole rocks are held out. **SPLIT-5**: the test mirrors the source's test.

6. **Accept the four warnings with these texts?**

   * **Problem:**
     - Four checks fire on the shipped definition (the 1x1 split, the two test groups, gypsum missing from the test, the three masked spectra), and each needs a text that says why the task stays as it is.
     - The texts are in the notes below; on yes they are written into `dataset.py` and the checks count as accepted.
   * **Background:** the texts cite the facts measured here: the source's own split, 34,857 spectra scored one by one, the 4-13x noise of a two-rock test, gypsum in neither rock, and the damaged spectra that ODR's own files hold.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept the four texts | written into `dataset.py` on yes | each warning carries its reason; the checks close | none found |
     | B | Leave them unaccepted (implemented) | the four warnings stay open in `dataset check` | none found | the checks stay open with no reason recorded |

   * **Recommendation:** A. **Decision:** accept the four warnings with these texts, yes or no?

   **Notes for the AI:** on yes, write these into `accepted_check_warnings` in `dataset.py` and re-run `dataset check`:

     `splits_dimensions_off_protocol`: "1x1, the source's split (Spec-CNN, Notebook-CNN-Raw_Data): the reference maps
     train and both rock slabs are tested in one fold; with two rocks no other partition keeps every test rock unseen
     without the training rock telling the test rock's class set (splits comment)."
     `groups_test_groups_few`: "The two rock slabs are the task's unit of transfer and the source's test set. Each of the
     34,857 spectra is scored on its own; the smallest tested classes (forsterite-albite mix 3 spectra, forsterite-augite
     mix 44) are 0.13% of the test rows. The signal carries to unseen rocks (task probes: linear log loss 0.961 against
     2.603 for the class shares). Per-row standard errors understate the noise 4 to 13 times, and the gabbro's score rests
     on 12 mineral blocks: read the score per rock."
     `splits_test_class_missing`: "Gypsum has no test rows: neither rock holds it (its 16 points in the powder map named
     after the gabbro are a lab mixture, which trains). Every other class is tested in one rock or both."
     `dataset_spectrum`: "Three reference spectra are damaged (two cut short, one spreadsheet fill-down, which ODR's own
     file holds too); their damaged bands are set missing as for inner positions, the rows train and are never tested."

**Review panel:** ship after changes (mediator). Full panel, on the builder's draft (one fold per rock with the other
rock in training, the band minimum, the 46-spectrum powder map tested with the gabbro): the claim auditor, the column
auditor, the split auditor, the domain practitioner, the blind reviewer, the task gamer and the precedent checker, then
the advocate and the critic with one rebuttal each, and the mediator. In rebuttal the advocate conceded the source's
split and agreed to move the muscovite block to training. The mediator kept the block on the rule against grouping by
similarity, and the paper now confirms it. The critic ended at ship after changes, gated on the browser checks, and kept
the SEL-12 run open. Claims: 43 audited; most hold (the counts, the codes, the metric, the band minimum's identity with
the source's code, the code-9 repair, the code-15 drop); 3 refuted on facts (a spreadsheet fill-down in one reference
row, the rare-class loss shares, the encodings sentence) and 4 in detail (the code's citation, readings per band, the
metric's threshold, "no cosmic-ray removal"), all fixed; 3 untested, now issues 1-3 (issues 2 and 3 now answered by the
paper). Blind review: include with changes; without them it would exclude, as the split let the training rock reveal the
test rock. Task gamer: one fold per rock could be gamed with no test row (log loss 0.666 to 0.477 for the best honest
model), gone with the source's split; test-row smoothing and the like are covered by the protocol line; the augite map
carries most of the gabbro's honest score (a separate specimen by the paper, issue 3). Agreed: grouped by rock, the
code-15 drop, the code-9 repair, log loss, the powder map to training, one reading per band, the protocol line.
Disputed: the split (settled for the source's, issue 5 if you want the other), the hb_ms muscovite block (settled: kept;
the paper places it in the granite test set, issue 3), SEL-12 (issue 4).

<details><summary>Mediator</summary>

```text
Written before the changes; counts here (gabbro 18,692, 90,341 reference spectra) are before the 46-spectrum powder map
moved to training.
MEDIATOR: raman_mlrod (folder datasets/_dev/tabarena-v0pt2/raman_mlrod, df-large), 2026-11-09
Read: principles.md, PANEL_COMMON.md, the builder's report, the seven phase-A reports, both briefs with their
rebuttals, dataset.py, the rule texts cited (SPLIT-1/5/19/24, LEAK-9/13/17, USE-5, SEL-12/15, EV-4). One check run
(below). Nothing edited.

======================================================================================================================
1. RECOMMENDATION (judgment record)
======================================================================================================================

Verdict: ship after changes. The record stays `TBD` until gates G1-G3 (one browser session) are settled. The SEL-12
  run is a TODO re-check (G4); it does not hold the verdict.
Validity:
  - SEL-12 open. The default leans keep (SEL-15). Re-check after the run.
  - USE-5: fit approximate, gap named. Gated on G1: if the source's classifier set the granite labels, the granite
    rows leave the task.
  - SPLIT-1, SPLIT-4, SPLIT-29 hold: grouped by rock.
  - SPLIT-19 (Should): switch to design B, the source's split. No exception is needed.
  - SPLIT-24 / LEAK-17: the 46-row gyp_foalb map moves to training. The hb_ms muscovite block and the augite map are
    gated on G2 (no regrouping on similarity).
  - LEAK-9: a protocol line covers the transductive exploits.
  - LEAK-13: one reading per band. The measured fix costs nothing.
  - PROV-13: the code-9 to code-8 repair holds. The filled row is repaired from ODR or masked. The mirror is checked
    against ODR (G3).
Value:
  - MET-5 and MET-6: log loss, the fallback.
  - TP-5 and TP-8 hold (keep).
  - Few groups (-): the 4-13x noise goes in the reason.
Quality: CLEAN-26 wording fixes; the fill-down row masked if ODR does not repair it.
Weighed: few groups -, the source's design +, a real lab and rover task +, a strong spectrum-model incumbent - (open).
For the curator:
  - issue 1, the browser session (G1 granite labelling, G2 augite and muscovite specimens, G3 ODR checksums, file
    list and licence);
  - issue 2, SEL-12 after the run;
  - issue 3, design A only if the curator records a SPLIT-19 exception with a fact the panel did not find.

======================================================================================================================
2. CHANGES TO MAKE NOW (no decision needed)
======================================================================================================================

C1. Design B (SPLIT-19 Should; SPLIT-5; LEAK-9). One split, 1x1: all 34 reference maps (plus the moved material, C2)
    train, and both slabs are tested in one fold. This is the source's split (Notebook-CNN-Raw_Data:
    fin_path=Single, testin_path=Mixed/Test Set).
    - Why no decision is needed: SPLIT-1 (Must) holds under A and under B. Both hold whole rocks out, cold start, so
      this is no conflict between rules, and SPLIT-19 (Should) sets the default.
    - A departure needs a fact that sets the case apart and serves a higher principle. A's stated fact ("the other
      rock lowers the log loss on both rocks") is refuted for the shipped encoding: logreg on standardised bands goes
      gabbro 0.883 -> 0.784 but granite 1.065 -> 1.307 (claim auditor 34; split auditor: true for SNV-logreg only).
    - The remaining reason for A, a score per rock, serves P6 (value), not a higher principle, so it cannot carry an
      exception to a P4 rule. B still gives a score per rock: score the one test fold by the `specimen` group after
      the fact.
    - Under A, the design itself can be gamed with no test rows (exploit #3: H3 0.666 -> 0.477, baseline 2.757 ->
      1.988). No protocol line can detect that.
    - A also hurts honest models: baseline 2.757 under A against 2.410 trained on the references only. The best honest
      model (H3) trains on the references only.
    - Cost of B: none measured. Kendall tau is 1.0 for five models, A against B (split auditor).
    - Accept `splits_dimensions_off_protocol` (1x1) with the source's split as the reason. Rewrite splits_comment,
      task_summary.split and Decision 3 ("each fold tests one rock").
    - If G1 drops the granite, B becomes reference -> gabbro, still one fold.
C2. The 46-row map L_raw_gabbro0dust_test_015s_46_final goes to every training side as a group of its own
    (SPLIT-24, LEAK-17; USE-10).
    - Exact basis from the data, not similarity:
      - its labels are gypsum and the forsterite-albite powder mixture, and a 50/50 lab powder mixture cannot be a
        point of a rock slab;
      - the source's own row ids read "gyp_foalb_test".
    - Effect: logreg gabbro 0.784 -> 0.786.
    - Fix the class counts: the gabbro holds 6 classes, not 8 (task_summary.predicted, splits_test_class_missing).
      Gypsum then has no test rows; that is TP-8 reading 3.
C3. LEAK-9 protocol line in splits_comment: each spectrum is predicted on its own, with no use of other test rows
    (no neighbour averaging, test-set priors, self-training or train-against-test weighting). Precedents:
    medical_facility_operational_data, sepsis, 5g. It covers exploits #1 (the kNN part), #4, #5, #6 and #7.
C4. One reading per band (LEAK-13 Must, P4): the reading nearest k + 0.5 in place of the band minimum.
    - Measured: the comb AUC goes 0.651 -> 0.536; LR gabbro 1.451 -> 1.253, granite 0.485 -> 0.497 (claim auditor 38).
    - LEAK-13 is a Must that asks to harmonise once the fix is measured. The source's grid (spectra.md under
      CLEAN-26, P7 Should) cannot outrank it.
    - This settles the precedent checker's prompt C1 as option (b). Option (a) read a Must by its purpose, and the free
      fix removes the need.
    - Keep 150-1,099 cm-1 and 1 cm-1 bands. The practitioner needs that resolution.
    - Reword the Spectrum description and curation note: the source's band minimum was a cosmic-ray step; ours takes
      one raw reading per band.
    - Re-run the probes and the encodings table on the new grid.
C5. Filled row qtzalb_train_60s_3000 row 2456 (346 readings exactly k x 4.11843; PROV-13 Must, CLEAN-26/CLEAN-11):
    repair it from ODR's file if that file is clean (G3). Otherwise mask bands 581-1,099 cm-1 of that row. Guard the
    mask count in `_clean`: 3 rows, 649 + 519 cells under the band minimum (re-count under C4). Correct claim 6.
C6. Notes and wording (PROV-16, USE-5, USE-8, CLEAN-26, MET-5/6, TP-8):
    - fit_reason:
      - the closed set (no abstain answer; code 15 dropped);
      - the labels mean different things by rock: the gabbro is labelled by grain in blocks, the granite by what the
        spot shows (147 "Forsterite" points are the dust's olivine);
      - the slab labelling is undocumented in what we could read;
      - the instrument gap: SuperCam/RLS at 6-12 cm-1, not SHERLOC.
    - The dust asymmetry with its numbers: about 610 forsterite and 800 plagioclase points of the dusty gabbro look
      like the granite's code 15 and keep the grain's label.
    - Replace "every test rock stays unseen" with the G2 question and its stake.
    - The README citation goes to `raw_processing` and the (950, 1) input layer; the 5 cm-1 text belongs to the CWT
      path.
    - Bands hold 1-4 readings, not 1-2 (moot after C4; say so).
    - 112 saturated spectra ship (5 of the 117 are dropped code-15 rows); name the 4 near-fully saturated
      hb_train_120s rows.
    - 12 exact grids, 11 within the window; 1,189-3,670 readings.
    - Encodings: SNV beats "as is" for LightGBM on both rocks. "As is" stays by CLEAN-26 (the field's default, not a
      fit on our folds).
    - Rare-class loss shares: Quartz-albite mix 0.81% of rows -> 6.42% of the loss; biotite 1.28% -> 4.51%; gabbro
      calcite 4.3% -> 10.1%.
    - Metric reason: the test report is classification_report on argmax. The "unknown" threshold (dec_pred default
      0.95, 0.5 in the notebook; no 0.98 found in the code) shapes only the validation confusion matrix.
    - Decision 2's evidence: add the in-situ granite microcline (511/474, SNV correlation 0.08 / 0.00) as the
      comparator.
    - Dust-state reason: the cover at the spot is unknown; whether the surface is dusty is known.
    - Licence field: state what the source says, both AHED's text "BY-NC" and its badge "BY-NC-ND 4.0", as a one-line
      note (EV-4). It is a release-checklist item, never a verdict reason (Lennart, 2026-09-23). This corrects both
      briefs' "ND would stop shipping".
C7. Warnings:
    - groups_test_groups_few: under B, one test fold of two rocks. Cite the noise: per-row SE understates it 4-13x;
      the gabbro's score rests on 12 mineral blocks. Add heart_disease-style counts: points scored one by one; the
      smallest tested classes are under 0.2% of the loss.
    - splits_test_class_missing: moot under B. Both rocks together hold every class except gypsum (after C2); state
      gypsum's case.
    - splits_rows_never_tested: word it like bacteria_id_raman's and file one Cases row.
    - dataset_spectrum: as proposed.
C8. TP-7 / LEAK-4 (Must): run the task and leak probes on the source's labels too (code 15 kept, code 9 unrepaired) and
    report them (audiology's case). The precedent checker found them missing.
C9. Write the SEL-12 run as a TODO in the record and REVIEW.md (issue 2 below). Drop "as for bacteria_id_raman" and cite
    the source's CNN result.

======================================================================================================================
3. ISSUES FOR THE CURATOR (ranked: validity first, Must first)
======================================================================================================================

Issue 1 (P3/P4/P5; USE-5, SPLIT-24/LEAK-17, PROV-1/PROV-13 Musts). The browser session. These facts gate `TBD`.
  This is no weighing: each is a fact that a cheap check settles (EV-1), and each changes the definition.
  G1. How the slab maps were labelled (USE-5). Read the paper's methods: open access, the 403 is a bot block.
    - Against model-made labels: the labels follow the spectra (dusty-granite albite and microcline show their own
      bands); nearest-centroid agreement is 77-100%; the 147 forsterite points show an Fe-olivine doublet (817/850),
      so the label reads the spot.
    - For model-made labels: code 15 is exactly dec_pred's output below its threshold; the dusty granite is speckled
      (1,688 one-point runs of 3,691); the gabbro comes in whole blocks.
    - Outcomes:
      - by hand or by phase mapping: approximate fit, with both label semantics named (C6);
      - the source's CNN or another thresholded classifier: the granite rows fail USE-5. Remedy: filter them out
        (rung 2, not exclusion); the task becomes reference -> gabbro.
      - not stated: keep with the note (USE-5 allows an undocumented construction).
  G2. Whether aug_train_15s_1000 (and ms_train_015s_5900) were mapped on the slabs or their hand samples (SPLIT-24,
      LEAK-17). Read the sample list in the paper or the ODR metadata.
    - Stake (split auditor, logreg, gabbro):
      - without that map, gabbro augite accuracy 0.822 -> 0.002 and fold log loss 0.784 -> 2.551 (dummy 2.898);
      - dropping the 5x larger augite map instead changes nothing.
      - Augite is 44% of the gabbro rows.
    - Critic: augite matches at each map's own level (SNV 0.972 against 0.982/0.975; background 1,121 against 1,128
      counts; adversarial AUC 0.91 where other pairs reach 0.99-1.00). It is the outlier of the calibration.
    - Advocate: albite (0.289 -> 0.004) and microcline (0.989 -> 0.126) depend on one map just as much. Similarity
      proves no shared specimen (EV-6).
    - Both sides agree: no regrouping on similarity (SPLIT-24). On a yes, the map joins the gabbro's group (test side
      under B, or dropped). On "not stated", keep it, with the question and stake in splits_comment.
    - The hb_ms muscovite block follows the same check (see disputed point 2).
  G3. ODR sha256 of qtzalb_train_60s_3000, L_raw_granite0dust_test_015s_4084_final, L_raw_granite50dust_test_015s_10000
      and the gabbro 50% dust file; the ODR file list ("500,000+" against 130,061; id 63742 missing); the licence badge
      (a note only).
    - A match: ai4d's pattern (byte match).
    - A mismatch: rebuild from ODR's files (repair from the origin, PROV-13).
    - More maps: re-scope.
    - Decide ugr16_isp_netflow_intrusion alike (the same server-refuses-machine mirror situation).
  Decision needed: run the session. Then apply the outcomes above; none of them needs a weighing.

Issue 2 (P2; SEL-12 Must, SEL-15 weighed). Is a spectrum model clearly better? This is a judgment call: SEL-12 is
  "judged per dataset", and "clearly better" has no numeric line. It stays with the curator after the run.
  - Facts (critic's measurement, re-run here):
    - design B, trained on the references only, untuned, argmax accuracy on the 19,980 clean slab spectra (the source
      CNN's exact test set): logreg PCA100 0.934 (gabbro 0.975, granite 0.902), logreg-SNV 0.906, LightGBM 0.865,
      RF 0.830, kNN 0.801;
    - the source's Spec-CNN: 1.00, macro F1 0.98 (Notebook-CNN-Raw_Data cell 12; the source's own result, which EV-4
      counts);
    - the dusty slabs: 0.42-0.64 (no CNN number on our labels).
  - Advocate: untuned tabular models already reach 0.93; the field's tools include PLS-DA, SVM, RF and kNN; SEL-15
    puts the burden on "clearly better". If the granite labels are CNN-made (G1), the 1.00 is partly circular, so read
    the gabbro (block labels) apart.
  - Critic: 6.6% error against 0% is not competitive on its face. The untuned trees score below the dummy in log loss
    (RF 3.158, LightGBM 2.906, dummy 2.766). Third parties put CNNs 8-10 points ahead (EV-4: orientation only).
  - Pair, not precedent: bacteria_id_raman was judged keep with a source gap of CNN 82.2% against LR 75.7%. Here the
    gap in error rate is larger, the tabular accuracy higher.
  - Precedents for keeping pending a run: open_university, heart_disease (TP-1 practice).
  - TODO run (GPU via SkyPilot, TabPFN v3.5, never v2):
    - Spec-CNN (cnnmodel_raw) against tuned LightGBM/CatBoost/RealMLP/logreg and TabPFN
      v3.5, on design B;
    - log loss (declared) and argmax accuracy;
    - reported on the clean slabs, the dusty slabs, the gabbro and the granite apart.
  - What settles it: the curator's call on that table. If the CNN is clearly ahead of the tuned tabular models on
    both rocks, SEL-12 excludes the dataset (`Wrong Domain / Source Modality`), and nothing ranked above it rescues it.
  Decision needed: after the run, keep or exclude.

Issue 3 (P4; SPLIT-19 Should). Only if the curator wants design A. A needs an "Exception to SPLIT-19" with a fact that
  sets the case apart and a higher principle it serves. The split auditor and the practitioner prefer A ("a lab
  trains on every labelled rock"; a score per rock). The panel found no fact that survives:
  - the measured reason is refuted (C1);
  - the per-rock score is a P6 value and is available under B;
  - exploit #3 and flaw A remain.
  A departs from heart_disease (leave one hospital out, kept 2026-10-27). The fact that sets raman_mlrod apart: the
  two rocks share almost no classes, so the training rock tells the test rock's class set. Every hospital has both
  outcomes. Decision needed: none, unless the curator wants A. Then write the exception, with exploit #3 in it.

======================================================================================================================
4. DISPUTED POINTS, SETTLED
======================================================================================================================

D1. Design B against A. Settled for B (C1).
  - Rules: SPLIT-1 (Must) holds under both, so there is no conflict. SPLIT-19 (Should) is the default. A departure
    needs a fact and a higher principle (principles.md, Strengths); none survives.
  - The advocate conceded in rebuttal.
  - The split auditor's and practitioner's preference for A rests on facts that B keeps (a per-rock score) or that are
    refuted ("lowers on both rocks").
  - Remedy ladder: fix the definition (re-split) over a protocol note that no check can read.
D2. hb_ms muscovite block: move to training (critic; advocate in rebuttal) or keep with a note (column auditor;
    advocate's opening). Settled: keep with a note, gated on G2 like the augite map.
  - SPLIT-24 (Must) bars grouping on similarity.
  - The only exact basis offered is the id "granite0dust_test_hb_ms". It names the minerals of the block. It does not
    say the material is not granite: muscovite and hornblende are granite minerals, and the hornblende block is a
    distinct specimen (0.615 to the reference).
  - That differs from the 46-row map, whose own labels (a lab powder mixture, gypsum) show it is no gabbro (C2).
  - The muscovite match at self level (0.9937 against 0.9938) is the same kind of evidence as the augite case (G2). The
    granite quartz reaches its reference at 0.9968 against 0.9974 and nobody proposes to move it. Treat like cases
    alike.
  - On a yes in G2, move the block to training as its own group.
  - Stake: 500 rows (3.1% of the granite); moving them raises logreg granite 1.079 -> 1.138; the ranking is unchanged.
D3. The gates. G1-G3 hold `TBD`: they are Must questions settled by one cheap fact-finding session (EV-1), and each
    changes the definition. This is not "ship with issues".
  - The licence is no gate (EV-4; release checklist).
  - SEL-12 is no gate. Precedent (open_university, heart_disease) keeps a dataset pending a measured run, and SEL-15's
    default leans keep. The critic's "gate on the run" is a stronger remedy than the precedents use. The run's outcome
    can still exclude the dataset.
D4. SEL-12: not settled by rank. It is a judgment call (issue 2).
D5. LEAK-13. Both sides agree on (b), against the precedent checker's recommendation (a). Settled for (b) by rank:
    P4 Must over P7 Should, the fix measured as free (C4).

======================================================================================================================
5. TASK GAMER'S EXPLOITS MAPPED
======================================================================================================================

The definition has no `Potential leak, kept on purpose:` note and no accepted warning that covers any of them, so all
are new.

| # | Exploit (gain on H3, mean of folds) | Rule | Status after the changes |
|---|---|---|---|
| 1 | split rule + kNN over test rows (0.666 -> 0.431) | SPLIT-19 design + LEAK-9 | split part removed by B (C1); kNN part by the protocol line (C3) |
| 2 | same-rock augite map (r0f0 H1 4.072 -> 1.375 with it) | SPLIT-24 / LEAK-17 (Must) | open: G2 |
| 3 | split rule alone, no test rows (0.666 -> 0.477) | SPLIT-19 / SPLIT-5 (no LEAK rule reads it) | removed by B |
| 4 | kNN smoothing over test rows (0.666 -> 0.593) | LEAK-9 | protocol line (C3) |
| 5 | EM prior of the test rock (unstable) | LEAK-9 | protocol line |
| 6 | self-training on test rows (unstable) | LEAK-9 | protocol line |
| 7 | importance weights from a train-against-test classifier (unstable) | LEAK-9 (reads test features); with #2 | protocol line; G2 |
| A | flaw: one slab in training confounds the slab look with its minerals (2.757 against 2.410) | SPLIT-19 / SPLIT-1 | removed by B |

After the changes, add a `Potential leak, kept on purpose:` note for #4-#7: test rows of one rock cluster by mineral
(nearest test row has the same label 96-97%), blocked by the protocol line only. Record the measured gain (B0 -0.99 to
-1.69; H3 -0.06 to -0.09) so that a later run can compare.

======================================================================================================================
6. AGREED FACTS
======================================================================================================================

- 125,244 rows: 90,341 reference spectra (34 maps), 34,903 slab spectra (gabbro 18,692, granite 16,211); 950 bands;
  15 classes.
- The counts equal Sineesh and Kamsali's ODR download, and the per-class support equals the source notebook's. The
  sha256 against ODR is unchecked.
- The band minimum equals the source's raw_processing exactly (max difference 0.0 on all 41 files).
- IID is barred: logreg 0.072 at random against 0.63-1.64 by rock; LightGBM ROC AUC 1.000 against 0.923. A split by
  map or by dust level leaks grains, so grouping by rock is the only honest partition (SPLIT-29).
- The code-9 to 8 repair holds:
  - correlation 0.977 with the clean gabbro anorthite;
  - correlation 0.08 / 0.00 with the in-situ granite microcline;
  - bands at 507/482 against microcline's 511/473;
  - petrology agrees.
- The code-15 drop: the source's "unknown", in one map only; Sineesh and Kamsali drop it too.
- Log loss, the fallback, is right (MET-5, MET-6, MET-11).
- No exact copies (0 of 130,061). Rows are shuffled. The number format and row order carry nothing.
- The 46-row map is gypsum plus forsterite-albite mix, ids "gyp_foalb_test".
- The hb_ms muscovite matches ms_train_015s_5900 at the self level. Its hornblende does not match the reference.
- aug_train_15s_1000 matches the gabbro augite at the self level. The stake is above (G2).
- Filled row: qtzalb_train_60s_3000 #2456.
- One reading per band removes the comb at no cost.
- The dust asymmetry by rock is real; the slab labelling method is unknown.
- Noise: per-row SE understates a fold's noise 4-13x.
- Untuned scores under design B: logreg 0.955 pooled log loss; argmax accuracy on the clean slabs 0.934 (re-run here
  from the split auditor's predictions: clean gabbro 0.975, clean granite 0.902, dusty 0.590).
- The source's CNN scores 1.00 on the same 19,980 spectra.

======================================================================================================================
7. CONSISTENCY WITH PRECEDENT
======================================================================================================================

- heart_disease (leave one site out): departed from by C1. The fact that sets this case apart is in issue 3 (nearly
  disjoint class sets, so the training rock reveals the test rock's class set; measured exploit #3 and flaw A).
- force_2020 (Basement; class missing by group) and audiology (TP-7): the code-15 drop is consistent. C8 adds the
  probes on the source's labels.
- mortgage, nci_aids (a repair toward the release's own record): the code-9 repair is consistent. The origin check
  is in G3.
- hepatitis_c, gallstone_disease, chicago_traffic_crashes (LEAK-13 harmonised): C4 is consistent. pancreatic's kept
  marker is set apart: no free fix was measured there.
- emscad (SPLIT-24, no similarity cluster): D2 and G2 are consistent.
- medical_facility_operational_data, sepsis, 5g (LEAK-9 protocol lines): C3 is consistent.
- open_university, heart_disease (kept pending tuned results): issue 2 is consistent. bacteria_id_raman is a pair to
  decide alike; the facts that differ are stated in issue 2.
- ugr16 (a mirror for a server that refuses this machine): decide alike in G3.
- lucas_topsoil and EV-4 (a licence is a note): C6 is consistent.
- No drift, and no third exception. Second cases (a library that trains and is never tested; a repair toward the
  release's record; a refusing-server mirror) are listed by the precedent checker. None reaches three.
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDIT: raman_mlrod (folder datasets/_dev/tabarena-v0pt2/raman_mlrod, df-large worktree), 2026-11-09
Claim auditor of the review panel. Read-only; scratch in the run folder.

VERDICT
Most claims hold: the counts, the codes, the splits, the metric, the band minimum's identity with the source's code,
the code-9 repair and the code-15 drop all survive tests that could have refuted them. Nothing refuted breaks validity
on its own, but the record needs these changes:
- 3 written claims are refuted on facts that matter:
  - claim 6: a value did change. One reference row holds a spreadsheet fill.
  - claim 43: two more rare classes carry several times their row share of the loss.
  - claim 39: SNV beats the spectrum as it is for LightGBM on both rocks.
- 1 statement of the builder's draft issue 7 is refuted: there is a cheap fix for the grid texture, and it does not
  smooth.
- 4 claims are refuted in detail: the README citation in claim 13, the readings-per-band count in claim 13, the
  threshold detail in claim 37, and the "raw / no cosmic-ray removal" wording in claim 15.
- 1 measured concern on an implied claim: the two rocks are labelled differently under dust (USE-5).
- 3 claims stay untested:
  - how the slab maps were labelled;
  - whether the 46-row and 1,373-row maps share a specimen with a reference map;
  - whether the mirror equals ODR, and the "500,000+".

How it was done: loaded the definition (load_definition(...).to_container(), 23 s) and scored dummies with the
declared scorer. Re-read all 41 raw CSVs through the definition's own functions. Ported Spec-CNN helper.raw_processing
verbatim and compared it with the definition, file by file. Ran a spreadsheet-fill detector on every raw row. Checked
the Spec-CNN notebooks' outputs, the raman-data loader, Sineesh and Kamsali (2026) and the AHED page. Fitted untuned
logistic regressions (PCA 100). Looked once more for the paper's text.

TABLE (claim | source | test | result | evidence | rule)
Claims are numbered as in claims.md. "probe" means the builder's output under probes/. M = my measurement.

1 | MLROD = Berlanga et al. 2022 + doi:10.48484/PWRB-R137 | source_url, bibtex | AHED page text | holds | AHED names
  both DOIs (and its own, 10.48667/yv5q-2606) | PROV-1
2 | licence CC BY-NC, version not stated | license | AHED, S2 record | holds | AHED "License: BY-NC"; S2 openAccess
  license CCBYNC | EV-4 (note only)
3 | ODR reCAPTCHA; zip 625,358,111 B, sha256 10178a4a...caaf7 | download_description | curl odr.io/MLROD and
  doi.org/10.48484/PWRB-R137; stat + sha256sum | holds | HTTP 403 "Confirm you are human" (2026-11-09);
  size and hash equal; all 41 extracted CSVs match the zip CRCs | PROV-1
4 | mirror = same 41 files and row counts as an ODR download | curation_comments | Sineesh text; per-file checks
  | holds for counts, per-file identity untested | footnote 2 and Sec. 4.1: 90,341 / 8,952 / 9,740 / 11,028 / 10,000
  / 5,183 / 34,903 equal ours. Their majority-class accuracies equal our per-class counts: 53.96% = 5,951/11,028 and
  38.01% = 1,970/5,183. Signs the mirror is not byte-for-byte what the source's code read: see claim 6; the dusty
  granite CSV has an empty first header (no `og-idx`), so the source's own raw_processing
  (read_csv(index_col='og-idx')) raises on it; that file has ODR id 63245, uploaded apart from 63641-63758; one id
  (63742) is missing from the loader's run 63737-63758 | PROV-1, PROV-2
5 | label codes match the notebook's clean-test support | curation_comments | Notebook-CNN-Raw_Data.ipynb cell 12
  output | holds | the support per class, 0-14, equals ours exactly (5,951 ... 30; total 19,980 = 8,952 + 11,028)
  | PROV-1
6 | two files carry Apple Numbers metadata; "whether a value changed is unknown" | curation_comments | decoded the
  __MACOSX quarantine attributes; fill detector (runs of 8 or more readings that are exactly linear or constant)
  on every row | REFUTED (a value changed) | quarantine "q/0082;698f6ca9;Numbers;" (0x698f6ca9 = 2026-02-13, the
  zip's date) on qtzalb_train_60s_3000 and L_raw_granite0dust_test_015s_4084_final. qtzalb_train_60s_3000 row 2456
  (og-idx ...-2456) holds 346 readings, 581.4-858.0 cm-1, exactly k x 4.11843 for k = 1..346 (4.12 to 1,424.98): a
  fill-down. The values stay below 1,500 to 873 cm-1; the row's median elsewhere is about 3,400. In the shipped
  bands, 277 to 293 of the row's 950 bands are fill. qtzalb_60s is the only training CSV whose integers are written
  without ".0", the format of the 7 test CSVs (all others: about 1% of tokens end ".0"). In the 4084 test file: no
  fill found, the format is the test files' own, and the label counts match the notebook. Whether ODR's
  qtzalb_60s has the same fill is unknown | PROV-13, CLEAN-26 (fill -> missing)
7 | paper full text and ODR unreadable | curation_comments | retried | holds | Wiley pdfdirect / full / full-xml /
  pdf: 403. eScholarship dissertation PDF (qt5k39g59z): 403. Unpaywall lists only Wiley. Europe PMC 0 hits; NTRS
  no hit | EV-7
8 | abstract "500,000+" vs 130,061 | curation_comments | S2 abstract; loader card; AHED | holds as "unchecked";
  UNTESTED | abstract: "500,000+ ... (5,000+ spectra/mineral class)". Hints of more data: raman-data's card says
  "4 binary mixtures" (3 here); AHED keywords include magnesium sulfates, sulfide and basaltic glass (none among the
  15 classes); ODR id gap 63742 | PROV-2
9 | Horiba LabRAM HR Evolution, 532 nm, 0.1 um step | curation_comments | raman-data card, Sineesh Sec. 4.1 | holds
  (T) | both third parties name the instrument and laser; the step only the card | EV-2
10 | 41 CSVs: 34 train (90,341), 7 test (39,720); all used | curation_comments, _load_raw | raw counts | holds | M
  90,341 / 39,720; container 125,244 = 130,061 - 4,817 | -
11 | one code per training map | CLASS_NAMES comment | inspect.log + raw | holds | every *_train_* file has a single
  label | -
12 | 11 grids, 1,190-3,671 readings, 52-1,801 cm-1, steps 0.45-0.87 | curation_comments | raw headers | holds
  (trivial off-by-one) | 11 grids (12 if the 4084 header variant counts). Numeric readings 1,189-3,670; range
  52.07-1,800.99; median steps 0.46-0.81, local steps from 0.01 on qtz_train_003s_1148. The range common to every
  grid is 141.02-1,100.46 | -
13a | shipped grid = the source's helper.raw_processing | BANDS, band_minimum | verbatim port of raw_processing vs
  band_minimum on all 41 files | holds | max |difference| = 0.0 on every file; the notebook's input layer is
  (None, 950, 1) | CLEAN-26
13b | ...as in the README "What Happens In Preprocessing", steps 1-3 | curation_comments | read the README | REFUTED
  (citation) | README step 3: "grouped in bands of 5 wave numbers ... all data between 150 and 155 ... the new
  datapoint 150". The 1 cm-1 band is the code's range(150, 1100), not the README | PROV-16
13c | "every grid has 1 or 2 readings per band" | claims.md (M) and the texture note | readings per band per file |
  REFUTED | 13 maps on the 0.487-step grid (3 granite test maps among them) and aug_train_20s_5103 have bands with 3
  readings; qtz_train_003s_1148 has one with 4 | -
14 | RamanBench interpolates to 1,836 positions, 141-1,100 | curation_comments | grid ranges | consistent (T, not
  re-measured) | the common range of all grids is 141.02-1,100.46, matching 141-1,100 | EV-4
15 | state raw: no cosmic-ray removal or other preprocessing; the band minimum is the source's standardisation |
  special_features, curation_comments | README text | PARTLY REFUTED (wording) | the source's README says the band
  minimum "cleans up the noise created by cosmic rays". The shipped values are minima over 1-4 readings, so they are
  de-spiked where a band holds 2 or more. The Spectrum description's "with no cosmic-ray removal" contradicts the
  source's own account of the step it ships | CLEAN-26
16 | 117 spectra reach about 65,535 | curation_comments | count of rows with a band >= 65,000 | holds | 117 of
  130,061. 5 rows have half or more of their bands saturated (4 in hb_train_120s_1225_01, 1 dusty-granite test
  row); 19 test rows touch the ceiling | -
17 | two cut-short spectra (cal 2732 from 938, qtz 1148 from 613), zero bands set missing | _clean step 2 | exact
  zeros in raw | holds | only these 2 rows; both are the files' last rows; zeros run to the end | CLEAN-26
18 | one malformed header 1630.89.1, outside the window | curation_comments | non-numeric columns per file | holds |
  only in 4084, where the header duplicates 1630.89 and ends at 1,800.29 instead of 1,800.99 (above 1,100) | -
19 | no two of the 130,061 spectra equal on the 950 bands | curation_comments | hash of the rows (rounded to 4
  decimals) | holds | 0 duplicates | LEAK-16..21
20 | 15 classes; gabbro 8, granite 9; every class in some test fold | task_summary | container per fold | holds |
  fold 0: 8 classes; fold 1: 9; union 15; every training side holds all 15 | -
21 | class names | CLASS_NAMES | raman-data label_map, Sineesh Sec. 4.1 | holds | label_map 0-14 names agree;
  "binary 1:1 powder mixtures" (Sineesh) | -
22 | code 15 is the source's "unknown"; 15 outputs; bands 506 / 999-1,010 / 629-655 | _clean step 5 | code and
  notebook; median spectrum | holds | dec_pred: pred_lab[i] = 15 below the threshold; dense5 (None, 15); my
  strongest bands for code 15: 506, 999, 641, 655. The mineral reading stays I | USE-5, TP-7
23 | Sineesh and Kamsali also leave the code-15 rows out | curation_comments | footnote 2 | holds | quoted verbatim;
  5,183 = 10,000 - 4,817 | -
24 | dusty gabbro code 9 (3,540 rows, rows 4,600-8,139) is plagioclase -> 8 | GABBRO_DUSTY, Decisions 1-2 | block
  boundaries; SNV-mean correlations with a calibration; peak positions | holds (stronger than written; part of the
  shown evidence is weak) | block rows 4,600-8,139. Correlations: 0.977 with the clean gabbro's code-8 block. With
  the granite slab's own microcline blocks (same slab setup) only 0.082 (clean) and 0.000 (dusty); those blocks
  peak at 511/473 like the reference microcline, while the code-9 block peaks at 508/482 (clean code 8: 507/482). The
  reference correlations shown in Decision 2 are weak evidence: reference albite scores 0.722, above both reference
  anorthite (0.658) and reference microcline (0.615). The same statistic ranks hornblende (0.843) above calcite
  (0.728) for the clean gabbro's calcite block, whose strongest bands are calcite's 1,086 / 711 / 281. A
  reference-trained LR calls all 400 of that block hornblende, so the LR count (1,911; mine 2,129) is weak too |
  PROV-13, EV-9
25 | gabbro maps at 0% and 50% dust: blocks of nearly the same size, "possibly the same spots" (I) | grouping
  definition | the two 400-row calcite blocks: per-point peak height and intensity, aligned vs transposed 20x20 |
  holds, now measured | aligned rho 0.10 / -0.20; read as a transposed 20x20 raster rho 0.35 / 0.35 (null 95%:
  0.11). Likely the same spots, scanned in another order; both sit in one test group | SPLIT-29
26 | gabbro labelled in blocks (6, 4 runs), granite point by point (135-3,691 runs) | curation_comments | runs per
  map | holds (3 of 4 granite maps) | 4084: 417 runs (70 of one point); 5571: 135 (21); dusty granite: 3,691
  (1,688 of one point; code 15 in 1,561 runs); the 1,373-row hb/ms map: 2 runs | -
27 | the 46-row and 1,373-row maps: specimen shared with a reference map unknown | curation_comments | nearest
  reference spectrum against each reference map's own neighbours | UNTESTED (suggestive, not decisive) | 46-row
  gypsum to gyp_train_12s_3320: median 0.9994 against that map's own nearest neighbours 0.9997 (56% above its
  p10). 1,373-row muscovite to ms_train_015s_5900: 0.9937 vs 0.9938 (88%). Fo-alb mix: 0.973 vs 0.985. But the
  1,373-row hornblende is far from every reference hornblende (0.616 vs 0.93-0.99), the gabbro's enstatite and
  forsterite are far (0.83 vs 0.998), and the granite slab's quartz is as close to reference quartz (0.9968 vs
  0.9974). Closeness does not prove a shared specimen | SPLIT-1, PROV-4
28 | use case from the abstract | task_summary.use_case | S2 abstract | holds | quote verbatim | USE-1
29 | integration time would name the class | curation_comments | file names | holds | e.g. 1s only calcite,
  12s only gypsum, 120s only hb/bt | LEAK-10
30 | source design: reference trains, slabs test | curation_comments | notebook paths | holds | fin_path
  'Data/Raw Data/Single/', testin_path 'Data/Raw Data/Mixed/Test Set/' (19,980 clean rows) | SPLIT-5
31 | source validation 80/20 random, 99-100% | curation_comments | helper.splitdata; notebook | holds |
  train_test_split(test_size=0.2); validation diagonal of 1,957 ... 1,028 (18,067 = 20% of 90,341) | SPLIT-29
32 | random third LR 0.072 / 0.984 vs held-out rock | curation_comments | probe; group probe | holds (not re-run) |
  consistent with LightGBM IID ROC AUC 1.000 vs grouped 0.923 | SPLIT-29
33 | two folds; 18,692 / 16,211 test; 90,341 reference rows train in both | splits_comment | container splits |
  holds | train 106,552 = 90,341 + 16,211 and 109,033 = 90,341 + 18,692; no specimen in both sides | SPLIT-1
34 | the other rock in training lowers LR log loss on both rocks | splits_comment (M part) | re-ran A (reference
  only) vs B (reference + other rock) with two LR pipelines | holds for SNV, NOT for the shipped encoding | SNV+PCA100:
  gabbro 1.549 -> 1.451, granite 0.639 -> 0.485. Standardised bands (the "as is" encoding): gabbro 0.883 -> 0.784,
  granite 1.065 -> 1.307 (not converged at 400 iterations). "Lowers on both rocks" depends on the preprocessing; the
  design's reason stays the I-statement | SPLIT-5, EV-8
35 | fit approximate | task_summary.fit | - | holds (I) | - | USE-8
36 | each spectrum one decision, per-row scoring | curation_comments | notebook | holds | classification_report
  over every test point | MET-17
37 | fallback log_loss: the source reports classification_report with a 0.5 / 0.98 threshold | metric.reason |
  notebook cells 4, 5, 12; cnnmodel_raw | holds, detail REFUTED | the test report (cell 12) is
  classification_report on argmax, with no threshold. The thresholds (0.5 notebook, 0.98 raw_cnn_model, 0.95
  dec_pred default) only shape the validation confusion matrix (build_confmat on X_dev). Fallback unchanged | MET-5,
  MET-6, MET-11
38 | grid trace by class (AUC 0.68), no shortcut on the test rocks | curation_comments | (i) a grid "comb" template
  score; (ii) the shipped LR on the band minimum vs one reading per band (nearest k + 0.5) | holds | (i)
  0.487-grid vs rest: AUC 0.651 on the band minimum, 0.536 with one reading per band. (ii) gabbro 1.451 (acc 0.626)
  -> 1.253 (0.735); granite 0.485 -> 0.497. On granite, true quartz / albite / microcline on the coarse map (4084)
  and the fine map (5571) get fine-only or coarse-only predictions in 0-0.3% of rows. Removing the trace does not
  lower the score, so it is no shortcut. Draft issue 7's "no clean fix without smoothing" is REFUTED: one reading
  per band removes the trace at no cost | LEAK-13, EV-3
39 | "no registered candidate beats the spectrum as it is on both rocks for either model" | curation_comments |
  probes/encodings.json | REFUTED for LightGBM | LightGBM SNV: gabbro 1.019 vs 1.987, granite 1.856 vs 3.220. Better
  on both. For the LR no candidate wins on both | CLEAN-26
40 | task probes: linear 0.877 vs dummy 2.766, trees worse than the dummy | curation_comments | task json; scorer
  dummies | holds | as written. Note: the dummy is the training prior. A uniform forecast (log 15 = 2.708) beats it
  on gabbro (2.898) and loses on granite (2.634). RF 3.158 and LightGBM 2.906 are worse than both | TP-1, EV-9
41 | leak probes (0.924, 0.683, 0.55, 0% copies, 0.537, 1-NN 0.633) | curation_comments | probe log | holds |
  values match; my exact-duplicate hash: 0 | LEAK-16..21
42 | group probes (IID 1.000 vs 0.923; 0.676 / 0.651 / 0.653 / 0.647) | curation_comments | probe log | holds |
  values match | SPLIT-29
43 | rare classes carry less than their row share of the loss except Fo-alb mix (3 rows, 0.18%) | curation_comments
  (TP-8) | probes/class_loss_share.json | REFUTED (detail) | granite fold: Quartz-albite mix 0.81% of rows -> 6.42% of
  the loss (8x); biotite 1.28% -> 4.51% (3.5x); gabbro calcite 4.3% -> 10.1%. The TP-8 verdict (keep) stands: far
  from alvin's 51-54% | TP-8
M | declared metric log_loss (fallback) | metric, README "Metric" | source re-read (MET-1); scorer on both folds
  (MET-2) | holds | Source: several threshold metrics (accuracy, per-class P/R/F1, macro and weighted averages),
  no deliberate one; the abstract's "+99% success" is a headline. MET-2: the per-row unit exists; no scoring
  columns are needed; every training side has all 15 classes; the scorer runs on both folds (prior dummy 2.898 /
  2.634, uniform 2.708 / 2.708). Same target and 15 classes as the source's CNN outputs. The source's "unknown"
  decision (dec_pred -> 15) is not scored, and its rows (code 15) are dropped | MET-1, MET-2, MET-5, MET-6, MET-8,
  MET-11
I1 | every feature known at the prediction point | implied | feature_columns(c) | holds | 950 bands; specimen and
  mineral are not features | USE-3
I2 | no row is a copy across the split | implied | hash; nearest neighbours | holds (exact) | 0 exact copies.
  Near copies: see claim 27 | LEAK-16..21
I3 | the split is the one the use case needs | implied | container | holds | whole rocks held out; 2 groups tested |
  SPLIT-1
I4 | the target is the same real-world target on both rocks, under dust too | implied | classifier of code 15 vs the
  rest within the dusty granite (CV ROC AUC 0.947), applied to the other maps | CONCERN | dust-like share: clean
  granite 0.2% (5571) and 2.6% (4084), the control. Dusty-gabbro forsterite block 38.1% (clean gabbro forsterite
  0.7%); repaired plagioclase block 22.5% (clean anorthite 8.7%). Augite and calcite are confounded (the clean
  gabbro already scores 65-100%: basalt dust has gabbro's minerals). The dusty gabbro keeps the grain's label on
  points that look like dust (4 whole blocks); the dusty granite's are coded 15 and dropped | USE-5

REFUTED, CONCERNS AND UNTESTED, RANKED (principles.md: validity first, Must first)
1. [P3, USE-5 Must; implied claim I4] The two rocks are labelled differently under dust (concern).
   - What changes: the gabbro fold scores dust-covered points against the grain under the dust. The granite fold
     scores only the 52% of dusty-granite points the source could assign (4,817 dropped). The two folds test
     different targets under dust, and the granite fold is easier than the use case, where the scientist does not
     know which points are dust.
   - Measured: about 610 forsterite and about 800 plagioclase points of the dusty gabbro look like the granite's
     code-15 points.
   - Mildest remedy: a note in curation_comments and in draft issue 4 (drop code 15 vs keep), stating the asymmetry
     and the numbers. No change to the data.
2. [P3/P5, USE-5 Must] How the slab maps were labelled: UNTESTED.
   - The evidence: code 15 is exactly the code the source's dec_pred gives a low-confidence prediction. The dusty
     granite's labels are speckled (1,688 one-point runs of 3,691), while the gabbro's come in whole blocks.
   - If the granite labels came from a classifier with a threshold, the granite target is a model's output, not a
     reading.
   - What settles it: the paper's methods section (Wiley and eScholarship return 403 here). Curator: read it in a
     browser.
   - Mildest remedy until then: a note that the labelling of the slab maps is not documented in what we could read
     (fit stays approximate).
3. [P4, LEAK-13 Must; draft issue 7] Claim 38 holds (no shortcut), but issue 7's "no clean fix without smoothing" is
   refuted.
   - Taking one reading per band (the one nearest k + 0.5) removes the grid comb (AUC 0.651 -> 0.536).
   - It scores the shipped LR at least as well: gabbro 1.451 -> 1.253, granite 0.485 -> 0.497.
   - LEAK-13 asks to harmonise a class-linked recording convention once the fix is measured. The fix is measured,
     cheap and free.
   - What changes: issue 7 gains option (B) "one reading per band", and issue 6 gains it as an alternative to
     interpolation. It departs from the source's own grid (CLEAN-26), so it is the curator's call.
   - Caveat: one untuned model, 2 folds (EV-3).
4. [P4, SPLIT-5] Claim 34's measured support depends on the preprocessing.
   - With SNV, the other rock in training lowers the LR loss on both rocks.
   - On the encoding the definition recommends (as is), it lowers gabbro (0.883 -> 0.784) and raises granite
     (1.065 -> 1.307).
   - What changes: draft issue 2 should state this, and rest design A on the use-case argument (I), not on "lowers
     on both rocks".
   - Mildest remedy: reword splits_comment and issue 2.
5. [P4/P5, SPLIT-1, PROV-4] UNTESTED: do the 46-row gypsum/Fo-alb map and the 1,373-row map's muscovite share a
   specimen with a reference map?
   - The evidence: their spectra are as close to gyp_train_12s_3320 and ms_train_015s_5900 as those maps' own
     neighbours. Quartz shows the same closeness across specimens, so this is not proof.
   - If shared: 46 rows of the gabbro fold (0.25%) and up to 500 rows of the granite fold (3.1%) are not "a rock
     never measured".
   - Mildest remedy: keep the "not stated" note and add the numbers; dropping them changes little.
6. [P5, PROV-13 Must, CLEAN-26; claim 6] A value changed: claim 6 is refuted.
   - qtzalb_train_60s_3000 row 2456 holds a spreadsheet fill-down: 346 readings, 581-858 cm-1, equal to
     k x 4.11843. That is 277 to 293 of the row's shipped bands.
   - It is one training row of 90,341 (Quartz-albite mix) and is never tested, so the effect on scores is
     negligible. But the definition ships fabricated values without a note.
   - Mildest remedy: in _clean, set that row's filled bands missing (as for the two cut-short rows), or drop the
     row, and note it. Add qtzalb_train_60s_3000 to issue 5's browser checksum against ODR: if ODR's file is clean,
     repair from it.
   - Claim 4 weakens with it: the mirror is not proven equal to ODR file by file, and the dusty-granite file is not
     in the state the source's own reader takes (no og-idx header).
7. [P5, PROV-16 Must; claim 13b] The README citation is wrong.
   - The Spec-CNN README describes 5 cm-1 bands; the 1 cm-1 band is in raw_processing (range(150, 1100)) and in the
     raw CNN's input layer (950, 1).
   - The identity with the code is exact (max difference 0.0 on all 41 files).
   - Mildest remedy: cite the code and the input layer, and say the README's 5 cm-1 text belongs to the CWT path
     (190 features).
8. [P6, TP-8; claim 43] Wrong detail.
   - Quartz-albite mix (0.81% of rows, 6.42% of the loss) and biotite (1.28%, 4.51%) also carry several times their
     row share.
   - The verdict (keep) is unchanged.
   - Mildest remedy: correct the sentence.
9. [P6, MET-5/6; claim 37] Detail of the metric reason.
   - The notebook's test report has no threshold; the thresholds shape only the validation confusion matrix.
   - The fallback holds.
   - Mildest remedy: reword the reason ("classification_report on argmax; a threshold for unknowns only in the
     validation matrix").
10. [P7, CLEAN-26; claim 39] Refuted for LightGBM.
    - SNV beats the spectrum as it is on both rocks.
    - The recommended encoding stays "as is" because CLEAN-26 sets the field's published default, never a choice on
      our folds.
    - Mildest remedy: say that, and drop "no candidate wins on both rocks for either model".
11. [P7, CLEAN-26; claims 13c and 15] Wording.
    - Bands hold 1-3 readings (1-4 on qtz_train_003s_1148), not 1-2.
    - The source's README calls the band minimum a cosmic-ray cleanup, so the Spectrum description's "no
      cosmic-ray removal" should say the band minimum de-spikes where a band holds several readings. "raw" stays
      defensible as the source's state.
    - Mildest remedy: reword both.
12. [P5, PROV-2; claim 8] UNTESTED, still.
    - "500,000+" against 130,061.
    - New hints that the deposit holds more: raman-data's card says 4 mixtures, AHED's keywords name minerals
      outside the 15 classes, and ODR id 63742 is missing.
    - Remedy: issue 5's browser check of the ODR file list.
13. Trivial counts: 1,189-3,670 readings (claim 12), not 1,190-3,671; "granite maps point by point" holds for 3 of
    4 granite maps (claim 26).

Strengthened by new measurements: claim 24 (the granite microcline calibration, 0.08 / 0.00), claim 25 (the same
spots, a transposed raster) and claim 38 (an independent template test plus the harmonisation test).

FILES (all under the run folder)
container_check.py/.json (scorer dummies, folds), raw_checks.py/.json (counts, source raw_processing identity, grids,
zeros), frame.py (analysis frame built through the definition's functions; frame.parquet, single.parquet),
analysis.py/.json (repair calibration, LR by block, texture harmonisation, odd maps, dust-like shares, label runs),
nn_calib.py/.json, design_check.py/.json, comb.py/.json, fill_detect.py/.json, numbers_check.py, dl/ (fetch
attempts).
```

</details>

<details><summary>Column audit</summary>

```text
raman_mlrod: column audit (column-auditor, review panel, 2026-11-09)
=====================================================================

Verdict: no leak in any feature column. Two of the slab test maps are probably not points of a new rock: one certainly,
one in part. One damaged spectrum is missed by the exact-zero rule. The binning, the Spectrum declaration, the label
repair, the code-15 drop, the class names and the excluded columns all check out.

Validity: LEAK-10 holds: only the spectrum ships; the integration time, dust level and og-idx are out.
  LEAK-13 holds as the builder read it, now tested with the exact grid as an oracle (see 3).
  LEAK-17 / USE-7 triggered, weak: the 46-spectrum "gabbro" map is the reference gypsum and Fo-alb material (issue 1).
  PROV-13: the repair is confirmed by an independent check, and no second label swap was found in the granite.
Quality: CLEAN-26 / CLEAN-11 departure, small: one ramp-filled spectrum is left in (issue 4).
Weighed: none.
For the curator: issue 1 (move or drop 46 test rows), issue 2 (the 1373 map's muscovite block).

How it was checked
- The cleaned frame came through dataset_io.from_definition (encode_special=False): 125,244 rows x 952 columns.
- Each shuffled row was traced back to its source file and row by hashing its bands 150-209 cm-1 against the builder's
  binned.parquet: all 125,244 rows matched.
- The frame equals that independent band minimum of the raw files in every cell except the 649 masked zeros.
- The shipped labels equal the source's codes after the 9->8 repair, mapped through CLASS_NAMES, on 100% of rows.
- Grids were read from the 41 file headers.
- dtype probe (re-run): 0 of 950 columns flagged; no codebook.
- Scripts and outputs are in the run folder: align.py, rowmap.py, grids.py (grids.json), values.py,
  oddrows.py, shortcuts.py (shortcuts.json), oddmaps.py, oddmaps2.py, nnwho.py, nnwho_fsp.py, granite_fsp.py and
  dustlike.py.

COLUMN TABLE
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
-------|---------|----------------------|--------------------|---------|-----
raman_150 ... raman_1099 (950) | Raman counts, the lowest reading in the band [k, k+1) cm-1 (Spec-CNN helper.raw_processing) | yes: the spectrum just measured | float64. Band minimum and 150-1,099 trim as in the source's code. 649 NaN in 2 cut-short rows. 1 ramp-filled row missed (issue 4). 112 shipped rows touch the detector ceiling | fine; one cleaning fix | CLEAN-26, CLEAN-11
Spectrum declaration | name raman_spectrum, prefix raman_, unit cm-1, technique raman, state raw | - | right: counts as read, no baseline, no normalisation; the band minimum is the source's own grid step | fine | CLEAN-26
specimen | the group: "gabbro slab", "granite slab" or "reference map <file stem>" (36 levels) | not a feature (feature_columns drops it) | category. Reference levels spell out the mineral and the integration time, harmless while it stays the group | fine | SPLIT-23, CLEAN-3
mineral (target) | the source's code 0-14 decoded into 15 class names | outcome | category with 15 levels in words. Code 15 dropped (4,817 rows). Dusty gabbro's code 9 repaired to 8 (3,540 rows) | fine; repair confirmed | USE-5, PROV-13, CLEAN-25
(excluded) integration time, from the file name | exposure per map, 0.03-120 s | the operator knows it, but it is set per reference map, so it names the class (cal 1 s, gyp 12/15 s, foaug 30/60 s, qtzalb 30/60 s) | not shipped | fine: right to exclude | LEAK-13
(excluded) dust level, 0% or 50% | the experiment's cover | not known on a real target | not shipped | fine | USE-3
(excluded) og-idx | file stem plus row number | an id; on the two small maps it names the minerals ("gyp_foalb", "hb_ms") | dropped as the index | fine: right to drop | LEAK-10 (an id that encodes the label)
(excluded) non-numeric headers ("1630.89.1", label) | a duplicated column of granite 4084, outside 150-1,100 | - | dropped, as in the source | fine | CLEAN-5

COLUMN NOTES (the bands)
- Binning
  - The 41 maps sit on 12 exact grids. They count as 11 within 150-1,099: granite 4084 is the albite grid less one
    reading plus the duplicated 1630.89.
  - All maps share 141.0-1,100.5 cm-1. Keeping more than 150-1,099 would make the bands beyond 1,100 missing by grid,
    and so by class. The source's trim is right and avoids that.
  - Wording fix: "Every band holds one or two readings on every grid" is wrong.
    - The 0.46-0.49 cm-1 grids hold 1 to 3 readings per band (6.9% of bands hold 3).
    - qtz_train_003s_1148 holds up to 4, and aug_train_20s_5103 up to 3.
    - The coarse grids hold 1 or 2 (23% of bands hold 2).
  - The README the definition cites ("What Happens In Preprocessing", step 3) describes 5 cm-1 bands, for its CWT
    pipeline. The 1 cm-1 bands come from helper.raw_processing, and the raw CNN's input is (None, 950, 1). Cite the code.
- Saturation
  - 117 spectra reach 65,000 counts, but 5 of them are dropped code-15 rows, so 112 ship: 98 reference and 14 test rows,
    in 30 maps and 14 classes.
  - The median spectrum has 1 band at the ceiling, 48 have 2-4. These are cosmic-ray spikes that the band minimum keeps
    where a band holds one reading.
  - Rows 197-200 of hb_train_120s_1225_01 are saturated in 518-762 of the 950 bands: no spectral shape is left.
  - Values reach 67,388, so the readings are not clipped at 16 bits.
  - Not class-specific: keep them as readings, and name the 4 near-fully saturated rows in the note.
- Cut-short spectra
  - The two rows are verified: the last row of cal_train_1s_2732 is missing from 938 cm-1 and the last row of
    qtz_train_003s_1148 from 613 cm-1. Each is 0 to the end of its grid, after normal readings (1,380 and 1,045 counts).
  - Setting them missing is right under CLEAN-26: one row each, so not the edge-position clause.
- Missingness is only in these two training rows; the missing-indicator probe scores 0.5.

PROBLEMS, RANKED (principles.md: P4 before P5 before P7; Must before Should)

1. [P4, LEAK-17 / SPLIT-23 and USE-7; weak; question for the curator] The 46-spectrum "gabbro" test map is reference
   material re-measured, not a point of a rock never measured before.
   Evidence:
   - L_raw_gabbro0dust_test_015s_46_final holds 16 gypsum and 30 Fo-alb mix. Gabbro holds neither, and the source's own
     row ids read "gabbro0dust_test_gyp_foalb".
   - Gypsum: correlation of the SNV spectra.
     - Each of the 16 rows has its nearest neighbour in gyp_train_12s_3320: median 0.9994 (q10 0.992).
     - That map's own rows reach 0.9997 to each other.
     - The two reference gypsum maps reach each other at only 0.79-0.97.
     - Levels are close: median 8,040 against 10,389 counts.
   - Fo-alb: all 30 rows have their nearest neighbour in foalb_train_15s_5220, median 0.973. That map's rows reach
     0.984 to each other, and the levels are 1,195 against 1,181 counts.
   - The map shares grid 0 with exactly those reference maps. The class shares of the training rows on its grid score
     log loss 1.37 on these rows, against 3.03 for the fold's class shares.
   - They are easy: the builder's logistic regression gets 0.978 accuracy on them.
   Size: 46 of 18,692 rows of fold 0 (0.25%). They are all of gypsum's test rows and 30 of the 33 Fo-alb test rows.
   Remedy, mildest first:
   - (a) Move the 46 rows to the reference side (train only, a group of their own), keeping the data.
   - (b) Drop them.
   - (c) Keep them with a note.
   I recommend (a). Afterwards gypsum has no test rows, as for any class a rock lacks (TP-8, as accepted for
   splits_test_class_missing).

2. [P4, LEAK-17; open, question for the curator] The muscovite block of L_raw_granite0dust_test_030s_1373_final cannot
   be told apart from the reference muscovite. The hornblende block can.
   Evidence:
   - Row ids "granite0dust_test_hb_ms"; two blocks, 873 hornblende then 500 muscovite. The map shares grid 2 with
     hb_train_015s and ms_train_015s.
   - Muscovite: nearest neighbour in ms_train_015s_5900 at a median of 0.9937. That map's rows reach 0.9941 to each
     other, and the levels are 1,473 against 1,408 counts.
   - Hornblende: only 0.615 to the reference hornblende, against 0.708 to other minerals. Its main band is at 669 cm-1
     (reference 680/669), and its nearest reference map is augite.
   - The hornblende is a different specimen, plausibly the granite's. The muscovite match proves nothing on its own:
     the slab's quartz reaches 0.992 to the reference quartz.
   - Grid shares score 2.12 on this map, against 3.02 for the class shares.
   Size: 500 rows (3.1% of fold 1); the logistic regression gets 500 of 500. Remedy: keep with a note (the name says
   granite), or ask the authors. Do not drop it on this evidence.

3. [P4, LEAK-13; holds; a stronger test than the builder's] The grid and the intensity level are no shortcut to the
   test labels.
   - Exact grid as an oracle (the training rows' class shares on the test row's grid), log loss on the whole fold:
     - gabbro 9.53 against class shares 2.90;
     - granite 7.70 against 2.63.
   - Map level, the log of the median count, alone:
     - gabbro 3.12, granite 3.32;
     - with the spread added: 4.20 and 5.27.
   - Roughness alone: 3.68 and 3.05, which reproduces the builder's numbers.
   - The raw counts do carry part of the excluded integration time: map medians run from 1,054 counts to 10,389 (gyp
     12 s), and 6,402-8,852 for the hb 120 s maps. Even so, a model reading it loses on both folds.
   - The only maps where the grid helps are the two in issues 1 and 2.
   - Keep, with the note extended by these numbers.

4. [P7, CLEAN-26 / CLEAN-11; Should; cleaning problem] A third damaged reference spectrum is missed by the exact-zero
   mask.
   Evidence:
   - Row 2456 of qtzalb_train_60s_3000 reads about 3,245 counts up to 580 cm-1.
   - From 581 cm-1 it falls to 4 counts and climbs as a straight ramp (a median step of 4.1 counts per band) to 2,771
     at 1,099. The file reaches about 3,500 only at 1,205.
   - This is no Raman reading: the 1st percentile of every other shipped row is 1,040 counts or more (the detector
     offset), and this row's is 51.
   - It is the same kind of damage as the two cut-short rows.
   Remedy: set raman_581 to raman_1099 of that row missing (or drop the row). Guard the mask counts in _clean:
   649 + 519 cells, 3 rows. One training row, so the score barely moves.
   Also one cell, raman_539 = 291 in row 3069 of qtz_train_003s_4760, comes right after a spike to 4,857. It is a
   detector undershoot: keep it as a reading.

5. [P3/P5, USE-5; note] The dusty target means different things in the two rocks.
   - The gabbro maps are labelled by block (4 and 6 runs: one grain's mineral for every point of a sub-map), so under
     50% dust its dust-covered points keep the grain's mineral.
   - The granite maps are labelled point by point (3,691 runs in the dusty map): 48.2% of the dusty granite points are
     code 15 (dust) and are dropped.
   - The two cannot be separated from the data. A dust detector trained on the granite's code 15 (5-fold ROC AUC 0.946)
     calls 40% of the clean gabbro "dust" too: basalt dust shares the gabbro's pyroxene and plagioclase.
   - Add one sentence to the slab-labelling bullet. No change to the data.
   - The source scored code 15 through its unknown threshold (dec_pred). Log loss cannot express that, so the drop is the
     mildest workable choice (builder issue 4).

6. [P7, writing; trivial]
   - "117 spectra" counts 5 dropped code-15 rows: 112 ship.
   - "one or two readings per band" and the README citation: see the column notes above.
   - "11 grids": 12 exact grids, 11 within 150-1,099.

CONFIRMED, NO ISSUE
- The code 9 -> 8 repair (PROV-13).
  - The repaired block's nearest reference maps (qtzalb_30s 114, an 73, hb 46, bt 11 of 300 sampled rows) follow the
    clean gabbro anorthite block's (qtzalb_30s 151, an 92, albite 37, foalb 13). No microcline map is among them.
  - Main bands 508/482/497/519 cm-1 for the repaired block, against 507/482/518/496 for the clean gabbro anorthite.
    The reference microcline sits at 511/473 and the reference anorthite at 502/482.
  - The two blocks sit in the same block order in both maps (augite, calcite, then the plagioclase or forsterite block).
- No second swap in the granite: the dusty granite's albite points show albite's bands, and its microcline points show
  microcline's.
  - Albite: 506/477, ratio I473/I479 0.79, correlation 0.968 with the reference albite and 0.60 with microcline.
  - Microcline: 510/473, ratio 1.82, correlation 0.965 with the reference microcline.
- The clean gabbro's calcite block (400 rows) is calcite: main band 1,086 cm-1, with 711 and 281. The logistic
  regression calls it hornblende because the broad background dominates the SNV shape; the label stays.
- The code-15 drop: only in L_raw_granite50dust_test_015s_10000 (4,817 rows); no reference map carries code 15.
- Class names: every *_train_* file holds one code, and the prefix-to-code mapping matches CLASS_NAMES. Shipped labels
  equal the source's codes on all rows.
- Copies: none across the split (leak probe). Missing values only in the 2 (soon 3) damaged training rows.
- dtypes: the bands are counts and float64. The target is a category of words, and specimen a category used only as
  the group.
```

</details>

<details><summary>Split audit</summary>

```text
raman_mlrod: split audit (split-auditor, review panel, 2026-11-09)
=====================================================================

VERDICT: right with notes.
Grouped by rock is the right regime, and the rock is the right group. Design A (one fold per rock, with the
reference maps and the other rock in training) is acceptable over B. It ranks five untuned models exactly as B does,
and it gives a score per rock. Three things need notes or a fix:
(1) specimens may sit on both sides of the split. This is measured for two small side maps and suspected, with a
    large stake, for the gabbro's augite reference map;
(2) the departure from the source's split (SPLIT-19) is not recorded as an exception, and the measured claim behind
    it holds for one model only;
(3) two test rocks make a noisy benchmark. The reasons given for accepting the warnings should cite the noise.

Judgment record
  Validity: SPLIT-1, SPLIT-4, SPLIT-29 hold (grouped by rock, cold start for a new rock).
    SPLIT-24 holds for the slabs. It is triggered for two side maps named after a rock that hold reference material
    (problem 1a).
    SPLIT-24/SPLIT-29 open question for aug_train_15s_1000 against the gabbro (problem 1b, EV-3, EV-6).
    SPLIT-19 departure needs an exception record (problem 2).
  Value: few groups, weighed − (problem 3). TP-8 reading 3 for the missing classes (accept, force_2020).
  Weighed: only a few groups −. The source's own transfer design + (heart_disease precedent).
    IID is not an option: SPLIT-29 is a Must.

Data and method
  - Loaded through dataset_io: the definition's frame and splits, as the column auditor cached them with
    from_definition(encode_special=False). Matched row for row to the builder's binned frame, which keeps the map
    file and the row position. Values, NaN pattern, labels and specimen all agree exactly.
  - Shipped split verified:
    - fold 0 tests the 3 gabbro maps (18,692 rows);
    - fold 1 tests the 4 granite maps (16,211 rows);
    - the 90,341 reference rows train in both folds;
    - train and test do not overlap.
  - Models, all untuned:
    - logistic regression on 100 PCs of the standardised bands ("logreg");
    - the same on SNV spectra ("logreg-SNV");
    - LightGBM (200 trees, 30% of the bands per tree) and a random forest (300 trees), each on 40,000 training rows;
    - kNN (k = 25) on 50 PCs of SNV.
  - Thread caps of 4 on every run. Scratch: the run folder.

---------------------------------------------------------------------
The regime and the group (pass)
---------------------------------------------------------------------
- Use case: "a point of a rock never measured before"; the rover meets a new target. That is a cold start for the
  rock (USE-10), so a grouped split tests it (SPLIT-1, SPLIT-4).
- IID would reward recognising a map (SPLIT-29):
  - logreg-SNV log loss 0.072 at random against 0.63-1.57 by rock (builder; my A runs: logreg 0.784 / 1.079,
    logreg-SNV 1.568 / 0.629);
  - LightGBM ROC AUC 1.000 against 0.923 (group probe).
- Points within one map share far more than the mineral (median SNV correlation r):

  | test map | next point (lag 1) | random same-class point, same map | same class in the reference maps |
  |---|---|---|---|
  | clean gabbro | 0.936 | 0.798 | 0.671 |
  | dusty gabbro | 0.834 | 0.413 | 0.561 |
  | granite 4084 | 0.963 | 0.917 | 0.387 |
  | granite 5571 | 0.995 | 0.994 | 0.607 |
  | dusty granite | 0.958 | 0.930 | 0.309 |

  Each map also has one integration time (0.15 s; 0.30 s for hb_ms), one dust level and one wavenumber grid. All
  maps of a rock are on the test side together, so these traits are what a new rock brings; none of them crosses the
  split.
- The clean and dusty maps of one rock share grains, not points:
  - dusty gabbro anorthite: nearest clean-gabbro anorthite r 0.929, against 0.801 for the nearest reference
    anorthite;
  - augite 0.894 against 0.852;
  - the same row index in the clean and the dusty block correlates no more than a shuffled pair (anorthite 0.676
    against 0.662; augite 0.499 against 0.513);
  - dusty granite quartz and albite: nearest clean-granite r 0.95-0.997.
  So a split by map or by dust level would leak grains. Grouping by rock, built exactly from the file names
  (SPLIT-24), is right, and it is what the grouping definition says.
- What one prediction is: one point, scored per row, no context (SPLIT-23: the source predicts and scores every
  point). Pass.
- Temporal: does not apply (no time axis; the use case is not a stream).

---------------------------------------------------------------------
PROBLEM 1 (P4; SPLIT-24, SPLIT-29): specimens on both sides of the split
---------------------------------------------------------------------
1a. Measured, small. Two "rock" maps are lab material whose spectra match a reference map at that map's own level.
- `L_raw_gabbro0dust_test_015s_46_final`: internal index "gyp_foalb_test"; 16 gypsum and 30 Forsterite-albite mix
  spectra. Gabbro holds neither.
  - Gypsum: nearest r to gyp_train_12s_3320 is 0.999 (raw SNV) and 0.998 (first derivative). The reference map
    against itself (points more than 20 rows away) is 1.000 and 0.998. The other gypsum reference map is far (0.59 to
    0.81).
  - Forsterite-albite mix: 0.973 against foalb_train's own 0.984.
- `L_raw_granite0dust_test_030s_1373_final`: internal index "hb_ms_test".
  - Its 500 muscovite spectra match ms_train_015s_5900 at 0.994 both ways, the same as both maps' own levels (first
    derivative 0.992 / 0.991 against 0.991 / 0.990).
  - Its 873 hornblende spectra are a different specimen (nearest reference hornblende 0.613, own level 0.941). That
    specimen is not the granite either.
- So 546 test rows are, by spectrum, specimens that are in every training side, and 1,419 test rows are not rock.
  This also skews the class counts:
  - the gabbro slab's own maps hold 6 classes, not 8; Gypsum and the Forsterite-albite mix come only from the
    46-row side map;
  - 873 of the granite fold's 901 hornblende rows and 500 of its 504 muscovite rows come from the hb_ms map.
  The "holds 8 of them" claim in task_summary.predicted and the reason given for `splits_test_class_missing` should
  say this.
- Effect is small:
  - logreg A: gabbro 0.784 to 0.786 and granite 1.079 to 1.088 without the side maps in test; 0.786 and 1.138 with
    them moved into training;
  - logreg-SNV granite 0.629 to 0.670;
  - the ranking of the 5 models is unchanged.
- The source counts the 46-row map as clean gabbro (8,952 = 8,906 + 46), so the shipped split follows it. Under
  SPLIT-5 that is a claim to check, and the check says these rows are not "a rock never measured before".
- Mildest remedy, a re-split: put the 46-row gyp_foalb map and the muscovite block of hb_ms in every training side,
  grouped with the reference specimens they match. Keeping the hornblende block (a new specimen) in test is a defensible
  choice; it could also join them. Alternatively keep everything with a note, since these are the source's test rows.

1b. Suspected, large stake: the gabbro's augite reference map may be the gabbro's own augite. This is a question
    (EV-3); similarity cannot prove it (EV-6).
- aug_train_15s_1000 against the clean gabbro augite (8,291 gabbro rows, 44% of the fold), both directions, compared
  with each map's own level:

  | spectra | augite map to gabbro | gabbro to augite map | own levels |
  |---|---|---|---|
  | raw SNV | 0.972 | 0.971 | 0.982 / 0.975 |
  | first derivative | 0.942 | 0.936 | 0.959 / 0.932 |
  | baseline-removed | 0.967 | 0.963 | 0.977 / 0.966 |

  - Every point of the reference map has a gabbro twin as close as its own map neighbours.
  - The other augite reference map (aug_20s_5103) sits at 0.66-0.82 against aug_15s_1000.
  - Absolute level: background (5th percentile) 1,121 against 1,128 counts, peak 1,497 against 1,574. The other augite
    map: 1,193 and 3,177.
- Stake, logreg, fold 0:
  - drop aug_train_15s_1000 from training: gabbro augite accuracy 0.822 to 0.002, augite log loss 0.632 to 4.629,
    fold log loss 0.784 to 2.551 (dummy 2.898);
  - drop the 5x larger aug_train_20s_5103 instead: 0.831 and 0.767, no change.
- Calibration: one reference map carries a test class elsewhere too.

  | test class | dropped from training | accuracy | log loss |
  |---|---|---|---|
  | granite albite | albite 625 + 1100 | 0.289 to 0.004 | 2.76 to 16.9 |
  | granite microcline | mc_3243 | 0.989 to 0.126 | 0.034 to 21.7 |

  But the peak-level match is below the self level there:
  - albite: 0.848 / 0.906 against 0.921 / 0.981;
  - microcline: 0.895 / 0.957 against 0.940 / 0.977.
  That gap is about the same as between the two albite reference maps that look like one specimen (0.939 / 0.931
  against 0.968 / 0.982). Augite at the self level is the outlier.
- If aug_train_15s_1000 (or albite 015s_625/1100, mc_015s_3243) was mapped on the slab or on the hand sample it was cut
  from, the gabbro is not an unseen rock for 44% of its rows. "Every test rock stays unseen" (splits_comment) is then
  not established.
- Decisive check: the source's sample list (the paper's methods; ODR metadata), or the authors.
- Remedy:
  - on a yes, the map joins that slab's group (a re-split: it leaves that fold's training side);
  - until settled, keep the split. State the question and its stake in splits_comment/fit_reason in place of "every
    test rock stays unseen". This is a curator issue.

---------------------------------------------------------------------
PROBLEM 2 (P4; SPLIT-19 Should, SPLIT-5): design A departs from the source's split
---------------------------------------------------------------------
- Source (B): trains on the reference maps only and tests both rocks in one fold. Shipped (A): adds the other rock to
  each training side. Same test rows.
- Measured, log loss per rock (gabbro / granite):

  | model | A | B | the other rock in training |
  |---|---|---|---|
  | logreg | 0.784 / 1.079 | 0.888 / 1.033 | gabbro better, granite worse |
  | logreg-SNV | 1.568 / 0.629 | 1.918 / 0.953 | both better (gabbro accuracy 0.748 to 0.602) |
  | LightGBM | 2.008 / 3.273 | 2.242 / 2.445 | gabbro better, granite worse |
  | random forest | 4.714 / 3.292 | 4.807 / 3.058 | gabbro better, granite worse |
  | kNN | 6.999 / 5.161 | 6.913 / 4.581 | both worse |
  | dummy (training prior) | 2.898 / 2.634 | 2.736 / 2.449 | both worse |

  - The dummy gets worse because the other rock's classes pull the prior away from the test rock's classes.
  - So the claim "the other rock lowers the log loss on both rocks" (claims.md #34; builder issue 2) holds for
    logreg-SNV only. Correct it.
- Rankings by log loss are identical under A and B: Kendall tau 1.0 per rock and for A's mean against B pooled
  (logreg, logreg-SNV, LightGBM, RF, kNN). Pooled B: 0.955, 1.470, 2.336, 3.995, 5.830. Mean of A's folds: 0.931,
  1.098, 2.640, 4.003, 6.080.
- My call on builder issue 2: keep (A).
  - It tests every rock as unseen, as B does.
  - It gives a score per rock with two different training sides. B split into two folds would share one training
    side: one evaluation, not two (the SPLIT-14 logic).
  - It follows a lab that trains on every labelled rock (SPLIT-1).
  - It does not change the ranking.
- Reject (C): the same 34,903 test rows would be scored twice under two training sides. It adds no group and mixes two
  designs in one mean (repeats over the same groups add no evidence).
- Mildest remedy: record "Exception to SPLIT-19" in splits_comment and the record. Fact: two test rocks; one fold per
  rock gives a per-rock score, every other labelled rock trains, rankings unchanged against the source's design
  (tau 1.0). Principle: SPLIT-1.

---------------------------------------------------------------------
PROBLEM 3 (P4 weighed / P6; "only a few groups" −, TP-5, TP-8): two test groups, a noisy benchmark
---------------------------------------------------------------------
- Each fold is one rock. Per-row standard errors understate a fold's noise 4-13 times. Example, logreg minus
  logreg-SNV on the gabbro, difference -0.784:

  | standard error by | value |
  |---|---|
  | rows | 0.019 |
  | 100-point chunks of a map | 0.070 |
  | 1,000-point chunks | 0.139 |
  | the gabbro's 12 mineral blocks | 0.242 |

- The gabbro maps are labelled in 12 whole blocks (6 + 4 + 2), one mineral per block. Three dusty blocks (forsterite,
  augite, plagioclase) carry 81% of the best model's gabbro loss (0.180 + 0.278 + 0.348).
- Across the two rocks:
  - the ranking holds except for the two linear variants (tau 0.8);
  - 8 of 10 model pairs separate on both rocks by 2 SE with 100-point chunks;
  - only 4 of 10 separate on the gabbro by its 12 blocks.
- No alternative partition adds groups:
  - by map or by dust level leaks grains (see the regime section);
  - the reference maps as test groups would be another task (pure specimens), and 5 classes have one reference map;
  - IID is barred (SPLIT-29).
  So this is a weighed factor, not a fix. heart_disease (3 hospitals, the source's transfer design) is the
  precedent for keeping it.
- Warnings:
  - groups_test_groups_few: accept. Cite the noise in the reason, not only the signal: "one rock per fold, the only
    partition; a fold's score rests on 12 mineral blocks (gabbro) or about 1,600 short runs (granite); per-row SE
    understates it 4-13x".
  - splits_dimensions_off_protocol (1x2): accept; repeats would reshuffle nothing.
  - splits_test_class_missing: accept under TP-8 reading 3 (a class lives in one rock; force_2020), with the class
    counts corrected as in 1a. The Forsterite-albite mix has 3 granite rows and carries 0.2% of the loss (TP-8
    reading 4).

---------------------------------------------------------------------
Files (all under the run folder)
---------------------------------------------------------------------
- prep.py: aligns the dataset_io frame with the builder's frame. Outputs meta_rows.parquet and X.npy.
- structure.py, structure.json: label runs, autocorrelation, nearest-neighbour checks, clean against dusty maps.
- same_specimen.py, same_specimen_peaks.py: the side-map and augite twin checks. Outputs same_specimen.csv (raw SNV),
  same_specimen_d1.csv (first derivative), same_specimen_bl.csv (baseline-removed).
- designs_fit.py, designs_eval.py: A against B. Outputs pred_*.npz, designs_scores.csv, fold_noise.csv,
  designs_eval.json, designs_eval.log.
- extra.py, extra.log: side maps moved into training, the augite stake, A against B per gabbro block.
- map_stake.py, map_stake_*.json, class_baselines.log: calibration of the one-map stake for forsterite, calcite,
  albite and microcline.
```

</details>

<details><summary>Domain practitioner</summary>

```text
raman_mlrod: domain practitioner report (2026-11-09)
=====================================================

Seat: a mineralogist who reads Raman point spectra, in a lab (a micro-Raman map of a rock slab or thin section) and
on a 532 nm rover team (SuperCam on Perseverance, RLS on ExoMars Rosalind Franklin). At the prediction point I have
one spectrum from a spot on a rock I have never measured, and a library of reference minerals measured on the same
instrument. I call the mineral at the spot, or I abstain, and from the calls of many spots I name the rock and choose
the next spot, the next target or the sample to take.

VERDICT
- Fit: APPROXIMATE (agree with the definition), with a fuller reason. One sentence: the rows are point spectra of a
  new rock from the same lab micro-Raman as the library, which is the lab task almost exactly, but the slab labels'
  construction is undocumented and differs between the two rocks, the abstain answer the source's decision includes
  is left out, and a rover instrument reads spectra at 6-12 cm-1 resolution (SHERLOC above about 800 cm-1 only), not
  at this 1 cm-1 micro-Raman grid (USE-5, USE-8; USE-9 gives no direct fit, as the label gap holds for the lab actor
  too).
- Metric: YES, keep log_loss (fallback, MET-5, MET-6, MET-8, MET-11). Two reservations, neither a reason to change it
  (see Q5).
- Ship: yes once the open issues settle. I would use this task as a test of mineral ID on a new rock. Nothing I found
  argues against the task. Two of the builder's statements need fixing (findings F5, F6).

-----------------------------------------------------------------------------------------------------------------------
Q1. At the prediction point, do I have each input? Which am I missing that I would always have?
-----------------------------------------------------------------------------------------------------------------------
- The spectrum: yes, the one input I always read (USE-3). Raw counts are what the detector gives me. I would never read
  absolute counts, though: I read peak positions and relative intensities after a baseline and a normalisation (F6).
- Integration time: I set it, so I always know it. Excluding it is right, though: the library maps run from 0.03 s to
  120 s per mineral, so it names the class in training (LEAK-13). In the test it is 0.15 s on 6 of the 7 maps, so it
  carries nothing there anyway.
- Dust state: the definition says "the dust level is unknown on a real target". From my seat that is half right. I
  know whether I am shooting a natural, dust-covered surface or an abraded or brushed patch (rover images, the
  abrasion tool), and in the lab I know whether I dusted the slab. I do not know how much dust covers the micro-spot.
  A binary "surface dusted" flag is known at the prediction point (USE-6). Shipping it would give little: one dusty
  map per training side, and every reference map is clean. So excluding it is defensible, but the stated reason should
  say "the cover at the spot is unknown; whether the surface is dusty is known". Minor.
- Missing inputs I would always have: the context image of the spot, the neighbouring spots of the raster, and on a
  rover the other instruments (SuperCam LIBS chemistry and VISIR, PIXL XRF). They are outside a per-spectrum task.
  The task deliberately keeps to the spectrum, as the source does. This is no gap in the data.
- The window 150-1,099 cm-1 holds the diagnostic bands of all 15 classes, as I read them in the data:
  - quartz 464;
  - feldspars 470-515;
  - olivine doublet 821/853;
  - pyroxene 665 and 1,011;
  - amphibole 669-679;
  - calcite 1,086, 281 and 711.
  It misses the OH-stretch region (about 3,600 cm-1) that I would use for the hydrous classes (micas, amphibole,
  gypsum's water). No file reaches it (the grids end at 1,801 cm-1 at most), so this is no curation choice.

-----------------------------------------------------------------------------------------------------------------------
Q2. Is the target what I act on? Probability, class or number?
-----------------------------------------------------------------------------------------------------------------------
- Yes: the mineral at the spot is what I act on (USE-5). I want a probability vector. I threshold it to abstain (the
  source's own `dec_pred` turns a top probability under 0.95, 0.98 in `raw_cnn_model`, into "unknown"), and I sum it
  over spots into a modal mineralogy with an uncertainty.
- Granularity is the source's. Three points I would note, none a reason to change the target:
  - "Anorthite" in the gabbro is the gabbro's plagioclase, a calcic plagioclase. Its bands (507/482 cm-1, per
    spectrum IQR 506-508 / 481-482) sit between the reference albite (507/479) and the reference anorthite
    (502/482). The definition says so already ("whatever the source calls anorthite").
  - What changes a rock's name is plagioclase against K-feldspar against quartz (the QAPF axes). Albite against
    anorthite matters less. Log loss weighs every confusion alike, and no cost matrix exists in the source (MET-7: do
    not invent one).
  - The three 50/50 powder mixtures stand in for a spot on a grain boundary, which I would call as two minerals
    (multi-label). This is the source's design; keep it.
- The closed set is the real gap of the target (F2): my decision includes "no call" for a spot that shows only dust or
  a mineral outside the library.

-----------------------------------------------------------------------------------------------------------------------
Q3. Does one row match one decision? Is the test what I would face?
-----------------------------------------------------------------------------------------------------------------------
- One row is one spot call, the unit at which the source predicts and scores. Per row is right (the builder's MET-17
  reading holds).
- The test is a rock never measured, a cold start (USE-10). That is the right kind of test (issue 2): reference
  library to rock means grain boundaries, crystal orientation, solid-solution compositions not in the library, low
  signal at 0.15 s, and dust. I believe it as a transfer test.
- I would not believe it as a precise estimate:
  - Two rocks, so the dataset score is the mean of two very different numbers (logistic regression 1.64 and 0.63).
  - Each slab map covers few grains. The clean gabbro map is 6 label blocks and the dusty gabbro 4. The clean granite
    maps hold 135 and 417 label runs over 5,571 and 4,084 points, about one or three boundary crossings per raster
    line. So each fold's score rests on a handful of grains: the gabbro's plagioclase block alone carries 50% of the
    gabbro fold's loss (class_loss_share.json).
  - Gabbro is basalt's plutonic twin (plagioclase, pyroxene, olivine) and the dust is basaltic. On the gabbro, a spot
    that reads the dust and one that reads the rock look alike, so the dusty gabbro cannot separate "seeing through
    dust" from "reading the dust". The granite can.
- Option A (the other rock in training) is how I would work: a lab or a rover team trains on every labelled analogue
  rock it has, and the test rock stays unseen. Keep A. B, the source's library-only design, is a fair alternative, but
  one fold mixing both rocks gives no more information.
- Test against what a rover faces: the instrument is the library's own LabRAM, so the test measures transfer across
  rocks, not across instruments. For the lab actor that is exactly the setting. For the rover it is the largest gap
  (F1).

-----------------------------------------------------------------------------------------------------------------------
Q4. Would I use this model? Trust and distrust
-----------------------------------------------------------------------------------------------------------------------
- In the lab: yes, as a first-pass phase map with an abstain threshold, which I check by eye on the peaks.
- On a rover: not as trained here. I would first degrade the library to the flight instrument's resolution and window.
- What makes me trust a model:
  - its confidence matches its accuracy on a held-out rock;
  - it keeps calls on dust-dominated spots low;
  - its calls agree with the diagnostic band positions;
  - it is robust to intensity scale and to the few-cm-1 shifts of solid solutions.
- What makes me distrust one: the builder's untuned random forest and LightGBM score worse than the dummy in log loss
  (3.16 and 2.91 against 2.77) while their macro AUC is 0.90-0.93. They rank well and are confidently wrong under
  shift, the failure that costs on an autonomous rover.
- SEL-12 (issue 1), from my seat:
  - Today minerals are identified by a library search (a correlation or hit-quality index on baseline-corrected,
    normalised spectra) and an expert's peak reading. PLS-DA, SVM, kNN and RF on spectra are standard chemometric
    tools, and 1D CNNs are the research front.
  - A tabular learner on 950 bands is a tool a lab would try, so the task is in scope under SEL-15 unless a spectrum
    model is clearly better.
  - The domain argument for a CNN here is concrete. The rock-to-library shift is largely band shifts of a few cm-1
    (plagioclase 502-507 against microcline 511) and intensity scale. A CNN is built to absorb both; a tabular model
    sees raman_507 and raman_511 as unrelated columns.
  - Sineesh and Kamsali (EV-4) report RF 69.2% and SVC 70.8% overall accuracy against CNNs at 78-80%.
  - I cannot settle SEL-12 from my seat: the builder's pending tuned and TabPFN v3.5 run is the right test. Keep it
    pending.

-----------------------------------------------------------------------------------------------------------------------
Q5. Does the declared metric score my decision?
-----------------------------------------------------------------------------------------------------------------------
- The source reports scikit-learn's classification_report on argmax predictions: precision, recall and F1 per class,
  and accuracy (Notebook-CNN-Raw_Data, cell 12: 1.00 accuracy on the 19,980 clean test spectra). It also builds a
  confusion matrix with an "unknown" threshold of 0.5 (notebook), 0.95 (`dec_pred` default) or 0.98 (`raw_cnn_model`
  default). The abstract's "+99% success" is a headline.
- That is several threshold metrics, and three thresholds, none argued from a cost. So the source has no unique metric
  (MET-5), no fixed threshold (MET-6, MET-7: a range fixes none), and the fallback, log loss, is right (MET-8; MET-11
  prefers log loss to a multiclass AUC).
- Would I pick a model by it? Yes.
  - My decision acts on a probability: a threshold to abstain, and a sum over spots for the modal mineralogy. Log
    loss is strictly proper, so it rewards exactly the calibration that threshold depends on.
  - It punishes hardest a confident wrong call, the error that sends a rover to the wrong target.
  - Its unit, the spot, is the unit I call.
- Two reservations, both on the task rather than the metric:
  - It cannot score the abstain answer, because the "unknown/dust" truth rows are dropped (F2).
  - It weighs classes by their rows, while on Mars the rare phase (calcite, gypsum: a carbonate or sulfate) is the
    find that changes a sampling decision. Calcite already carries 10% of the gabbro loss on 4.3% of its rows, and no
    source gives a class weighting, so I would not change it.
- The metric I would use: log_loss, as declared. Macro-F1 (Sineesh, RamanBench) would be a benchmark habit (MET-6).

-----------------------------------------------------------------------------------------------------------------------
FINDINGS (ranked by how much they change the task)
-----------------------------------------------------------------------------------------------------------------------
F1. Instrument gap for the Mars actor (USE-8; fit_reason).
- The data are lab micro-Raman: LabRAM HR, 532 nm, grids of 0.45-0.87 cm-1, µm spots on single grains.
- The flight instruments:
  - SuperCam (532 nm): about 12 cm-1 FWHM resolution, remote spots of millimetre scale.
  - RLS (532 nm): 150-3,800 cm-1, 6-8 cm-1 resolution, 50 µm spot on crushed powder.
  - SHERLOC (248.6 nm deep UV): usable only from about 800 to 4,000 cm-1. It cannot see quartz's 464 or the
    feldspars' 470-515 cm-1 bands, which identify about 62% of this task's test spectra (21,525 of 34,903: quartz,
    feldspars, quartz-albite).
- So the Mars use runs through SuperCam or RLS, and only after the library is degraded to their resolution.
- The fit_reason says "a laboratory Raman microscope ... not a rover's instrument". I would add the resolution and
  window difference, and name SuperCam/RLS (532 nm) as the instruments it stands in for. Mars 2020's SHERLOC does not
  fit.

F2. The abstain answer is left out (issue 4: agree with A, drop; USE-5, USE-8).
- Code 15 is the source's "unknown". `dec_pred` gives 15 to a call under its threshold, so on these 4,817 spots (48%
  of the dusty granite map) the source's decision credits a no-call.
- Their median spectrum shows the dust: plagioclase at 506 and pyroxene at 999-1,010 and 659 cm-1, basaltic dust's
  minerals.
- Keeping them as a 16th class breaks the granite fold: the class is absent from its training side, and the dusty
  gabbro labels dust spots by their substrate, so no consistent "dust" class exists to learn. Drop them (A).
- But fit_reason should say the task is closed-set: the no-call on a dust-dominated spot, common on natural Martian
  surfaces, is not tested.

F3. Label construction differs by rock under dust, and is undocumented (USE-5, USE-8: a label definition the sources do
not settle).
- The gabbro maps are labelled in whole blocks, by grain: the substrate mineral.
- The granite maps are labelled point by point, by what the spectrum shows, including the dust's own minerals:
  - 147 dusty-granite spots carry "Forsterite". Their median shows the olivine doublet at 817/850 cm-1, against the
    reference forsterite's 821/853, the downshift of a more Fe-rich olivine.
  - Mg-olivine does not occur in granite (it does not coexist with quartz in an igneous rock), so these spots are the
    basaltic dust's olivine.
  - Where the dust shows plagioclase and pyroxene, the granite gets 15.
- So on the gabbro the label is "what lies under the spot", and on the granite "what the spot shows".
- How the granite's per-point labels were set (by hand, or by a reference fit such as the instrument software's
  phase mapping) is not stated, and the paper could not be read.
- My check of how much this costs on the gabbro (nearest centroid among the clean gabbro's blocks, SNV): 86% of the
  dusty plagioclase block, 89% of the dusty augite block and 60% of the dusty forsterite block read as their own
  block's mineral. So most dusty-gabbro labels are readable. The block labels are no large noise apart from the code-9
  block (F4).
- Name both semantics in the notes and in fit_reason as the label gap. This is a second reason for approximate, and
  it holds for the lab actor too.

F4. The code-9 to 8 repair is right (issue 3: agree with A, repair; PROV-13). Per-spectrum band positions (window
maxima after a rolling-minimum baseline, SNV), median and IQR:

  | block | main band (cm-1) | second band (cm-1) | other bands (cm-1) |
  |---|---|---|---|
  | dusty gabbro, code 9 (3,540) | 507 (506-509) | 482 (480-483) | 517 and 495 shoulders |
  | clean gabbro anorthite, code 8 | 507 (506-508) | 482 (481-482) | 518 and 496 |
  | granite's own in-situ microcline, code 9 (2,166) | 511 (510-511) | 474 (473-475) | K-feldspar 282, 264, 452 |
  | reference microcline | 511 | 473 | |
  | dusty granite's microcline | 510 | 473 | |

- The dusty-gabbro block matches the clean gabbro's plagioclase band for band.
- It misses microcline by 4 cm-1 on the main band and 8 cm-1 on the second, both well outside the IQRs. Telling
  K-feldspar from plagioclase by the main band's position is the standard reading (Freeman et al. 2008 sort feldspars
  into structural types by the position of the strongest band).
- Petrology agrees: a gabbro holds plagioclase and rarely K-feldspar.
- The repair moves a library-only logistic regression's dusty-gabbro accuracy from 0.444 to about 0.64 (1,911 of
  3,540 called anorthite), which fits Sineesh and Kamsali's 40-49% for every model on that map.
- Suggest adding the in-situ granite microcline (511/474) to Decision 2's evidence: a microcline in a rock on the same
  instrument is a stronger comparator than the reference powder or specimen.

F5. A wrong sentence in the encodings bullet of curation_comments. It says "No candidate wins on both rocks for either
model". probes/encodings.json shows SNV alone (vib-snv-r1) beats the spectrum as it is for LightGBM on both rocks:

  | rock | log loss: as is to SNV | accuracy: as is to SNV |
  |---|---|---|
  | gabbro | 1.987 to 1.019 | 0.724 to 0.800 |
  | granite | 3.220 to 1.856 | 0.639 to 0.761 |

- Only the logistic regression has no candidate that wins on both.
- The recommended encoding stays "as it is" by CLEAN-26's own rule (the field's published default, never a tuning on
  our folds), so the outcome stands. The stated reason is false, though, and needs rewording.
- From my seat this is the expected result: raw counts carry the integration time and focus, and a tree that splits
  on absolute counts breaks under shift.

F6. Reading the spectrum: the grid (issue 6: agree with A).
- 1 cm-1 bands are the resolution I need: the species I must tell apart differ by 4-9 cm-1 (microcline 511/473,
  plagioclase 507/482, reference anorthite 502/482), and the per-spectrum IQRs are 1-3 cm-1.
- The source's README says "bands of 5 wave numbers", which would blur 507 against 511. Its code
  (`helper.raw_processing`) and the trained CNN (input shape 950, notebook cell 5) use 1 cm-1. The builder followed
  the code, correctly.
- The band minimum is a crude cosmic-ray filter that biases bands holding two readings low (the grid texture, issue
  7). I would interpolate after a proper cosmic-ray removal. Option B's 1,836 positions oversample an instrument with
  about 1-2 cm-1 resolution and add nothing I would read.
- Keep A, the source's own. The window 150-1,099 cm-1 holds every class's diagnostic bands (Q1).

F7. A check that found no problem: the clean gabbro's "Calcite" block (400), which the logistic regression calls
hornblende 400 of 400, is calcite. It shows bands at 1,086, 281 and 711 cm-1, weak against the reference (corrected
1,086 peak 3.2 against 15.6), with no amphibole 670 band. It is a weak-signal block, not a label error (calcite veins
are a common alteration in gabbro).

F8. The dust-state reason (Q1). It is a minor wording fix to curation_comments' first bullet. Not shipping it is fine.

-----------------------------------------------------------------------------------------------------------------------
What an expert in the domain would change (in order)
-----------------------------------------------------------------------------------------------------------------------
1. fit_reason: name the instrument gap (resolution and window; SuperCam or RLS, not SHERLOC), the closed set without
   the abstain answer, and the label construction that differs by rock (F1-F3). Fit stays approximate.
2. Keep the code-9 repair and add the in-situ granite microcline to Decision 2's evidence (F4).
3. Keep code 15 dropped, with the closed set named (F2).
4. Reword the encodings sentence (F5), and the dust-state reason in the prediction-point bullet (F8).
5. Keep split A, grid A, log loss.
6. Out of scope here, noted for a Mars variant: degrade the library to the flight resolution and test on a basalt.

-----------------------------------------------------------------------------------------------------------------------
Sources used
-----------------------------------------------------------------------------------------------------------------------
- Repository and run files:
  - the definition: $W/datasets/_dev/tabarena-v0pt2/raman_mlrod/dataset.py;
  - the record: $W/curation/records/raman_mlrod.md;
  - the builder's report and its probes: the run folder, probes/encodings.json,
    probes/class_loss_share.json, probes/split_designs_logreg.json, probes/task_probes.log, explore2.log.
- The source's code, Spec-CNN (Zenodo 10.5281/zenodo.7036374, the run folder): README, helper.py
  (`raw_processing`, `dec_pred`), cnnmodel_raw.py, Notebook-CNN-Raw_Data.ipynb (cells 4, 5, 11, 12).
- Sineesh and Kamsali 2026 (arXiv:2601.16107; the run folder): Sec. 4.1, footnote 2,
  Tables 3-4.
- NASA AHED dataset page (https://ahed.nasa.gov/datasets/f5b6051bfeb18c5a7eaef6504582; saved copy at paper/ahed.html).
- The Berlanga et al. 2022 abstract, as summarised by search. The full text is unreachable (eScholarship 403 again,
  2026-11-09).
- SuperCam body unit: Wiens et al. 2021, Space Sci. Rev., https://link.springer.com/article/10.1007/s11214-020-00777-5
  (Raman about 12 cm-1 FWHM).
- SHERLOC's window, about 800-4,000 cm-1:
  - https://link.springer.com/article/10.1007/s11214-022-00907-1;
  - https://an.rsl.wustl.edu/help/Content/About the mission/M20/Instruments/M20 SHERLOC.htm;
  - Asher, Appl. Spectrosc. 2021 (sites.pitt.edu).
- RLS (150-3,800 cm-1, 6-8 cm-1, 50 µm spot on crushed powder):
  - https://meetingorganizer.copernicus.org/EPSC2012/EPSC2012-740.pdf;
  - https://meetingorganizer.copernicus.org/EPSC2013/EPSC2013-935.pdf;
  - https://en.wikipedia.org/wiki/Raman_Laser_Spectrometer.
- Freeman et al. 2008, Can. Mineral. 46:1477, feldspar types by the main band's position
  (https://www.sshade.eu/data/publication/PUBLI_Freeman_2008). Read through a search summary only; the PDF host
  refused the connection.
- My checks: the run folder and peaks.log (band positions per block),
  dust_share.py and dust_share.log (nearest-centroid readability of the dusty gabbro, label runs per map). Both read
  the builder's binned.parquet, the same 1 cm-1 band minimum as the definition.

Rules cited: USE-1, USE-3, USE-5, USE-6, USE-8, USE-9, USE-10; MET-1, MET-5, MET-6, MET-7, MET-8, MET-11, MET-17;
SEL-12, SEL-15; CLEAN-26; LEAK-13; PROV-13; EV-4.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: raman_mlrod (MLROD, Machine Learning Raman Open Dataset)
Reviewer worked only from clean_room/{data.parquet,task.md} and the public web.
Scratch, scripts and raw outputs: the run folder (exp1.py/out, exp2.py/out, exp3.py/out)

VERDICT
Include with changes. The task is real and the data is real, but the split as specified (2 folds grouped by
"specimen") is broken. Without the changes below I would exclude it.

WHAT THE TASK IS
Classify one 532 nm Raman spectrum (950 intensity channels, raman_150 ... raman_1099, one per cm-1, raw CCD counts)
into one of 15 classes: 12 rock-forming minerals (quartz, albite, anorthite, microcline, hornblende, biotite,
muscovite, forsterite, augite, enstatite, calcite, gypsum) and 3 binary 1:1 powder mixtures. Source: Berlanga,
Williams & Temiquel 2022, Earth and Space Science, doi 10.1029/2021EA002125. Abstract: the goal is to identify
minerals "under low signal-to-noise-ratios, Mars-like conditions", for "autonomous rover decision-making on planets
like Mars" (Mars 2020 SuperCam, ExoMars RLS) and to help scientists interpret spectra on Earth. The real use is:
train on a library of reference spectra, then label new spectra from an unseen rock, which may be dusty. This is a
genuine, well-motivated use.
Structure of the 125,244 rows:
  - 34 "reference map ..." groups = 90,341 spectra, each a map of one pure mineral or one mixture.
  - "gabbro slab" (18,692 rows, 8 labels) and "granite slab" (16,211 rows, 9 labels) = 34,903 spectra. These are
    the source's held-out TEST set: rock slabs measured clean (0% dust) and with 50% basaltic dust. The two dust
    conditions are merged into one group per slab, and there is no dust column.
  - The counts match exactly what arXiv 2601.16107 reports after its own cleaning: "the training set ... had 90,341
    spectra" and "34,903 test samples overall", after dropping slab spectra whose label is not among the training
    classes.

CONCERNS, MOST SERIOUS FIRST

1. The 2-fold grouped split makes large parts of the test set unlearnable, so scores mostly reflect which groups
   land in which fold. [Blocking]
   Evidence: there are only 36 groups. Two slabs make up 28% of rows. Anorthite, Enstatite, Muscovite and the
   Forsterite-albite mix each have a single reference map. In every 2-fold grouping I simulated (GroupKFold, and
   StratifiedGroupKFold with seeds 0-4: 6 splits, 12 folds), 9 of 12 folds had 10%-42% of test rows from classes
   with ZERO training rows, and every split had at least one fold with 28% or more:
     GroupKFold fold0: Anorthite, Enstatite, Fo-Aug mix absent from train = 37.6% of test rows
     GroupKFold fold1: Muscovite absent = 10.3%
     SGKF seed0: 21.9% / 41.9%;  seed1: 29.9% / 18.1%;  seed2-4: 0% / 32.7%, 0% / 30.3%, 0% / 28.6%
   Each class has only 1-3 maps, and each map has its own intensity, baseline and calibration. So even the
   learnable part shows the model a new acquisition with almost no within-class variety.
   LightGBM on the raw features (20k train subsample):
     random 50/50 split   acc 0.989   (RamanBench reports macro-F1 0.990 for TabICL v2 on random 80/20 splits)
     GroupKFold fold0     acc 0.035   (predicts "Quartz" for every gabbro and reference spectrum; exp3.out)
     GroupKFold fold1     acc 0.208
     reference -> slabs   acc 0.707   (the source's own split)
   An SNV logistic regression gets 0.38 / 0.75 on the two GroupKFold folds and 0.80 on reference -> slabs.
   With the current split the benchmark would mostly measure fold luck and how badly a model breaks on a new
   acquisition, not mineral identification.
   Change: use the split the source defines and the real use calls for: train on the 34 reference maps and test on
   the slabs. This gives 90,341 / 34,903 rows, and every test class is present in training. For two scored splits,
   use reference -> gabbro and reference -> granite. If a CV-style protocol is required, assign folds by hand so
   every class keeps at least one reference map in train. Do not use 2-fold GroupKFold over these 36 groups.

2. The "specimen" column leaks the label and is mislabelled as a specimen. [Must fix]
   Evidence: its values are acquisition file or map names that contain the mineral code, exposure time and
   spectrum count, e.g. "reference map albite_train_015s_5250", "reference map qtz_train_003s_4760",
   "reference map hb_train_120s_1225_01" / "_02". Every reference-map value determines its class. "gabbro slab" and
   "granite slab" nearly determine the class set: gabbro is anorthite/augite/forsterite, granite is
   quartz/albite/microcline. Any model that reads strings, or any random or target-encoded CV, gets the label for
   free. Under a grouped split it is unseen at test, but it is still noise.
   These are maps, not physical specimens. The "_01"/"_02" pairs and repeated maps per mineral at different
   exposures (bt 015s and 120s, qtz 003s, 005s and 015s) suggest several maps of the same hand sample. The
   abstract says "hand samples/powder mixtures (5,000+ spectra/mineral class)". So "grouped by specimen" probably
   holds out acquisition sessions, not specimens.
   Change: keep it only as a group id. Never expose it as a feature. Rename it (e.g. "acquisition_map"). Fix the
   task.md wording.

3. Raw counts carry strong per-acquisition shortcuts. Rankings would be driven by whether a method normalizes each
   row, not by how well it learns. [Should fix or declare]
   Evidence: median per-row minimum (baseline) differs by up to 5x between maps of the same class (Hornblende 1,280 vs 6,974;
   Gypsum 2,020 vs 6,108; Quartz 1,040-2,058). Four row-level intensity statistics alone (min, p10, median, max)
   give 0.824 accuracy on a random split. A single channel (raman_1000) gives 0.447.
   The fo-albite mix map has its peaks shifted by about +4 cm-1 relative to the pure albite and forsterite maps
   (511/482 vs 507/479; 858/826 vs 853/821), a per-session calibration offset.
   Row normalisation alone lifts LightGBM on reference -> slabs from 0.707 to 0.805 (SNV) and to 0.851 (crude
   baseline removal plus max normalisation).
   Change: either ship the raw counts and declare this a spectral, distribution-shift task, or (my preference)
   also give benchmark users exposure time (it is known at prediction time) and, if the benchmark allows feature
   engineering, recommend row normalisation as the declared encoding.

4. The test labels are not what the source published, and the test has two conditions with no indicator.
   [Document]
   Evidence: the slab rows total 34,903, versus 39,720 test spectra in the source per arXiv 2601.16107. So 4,817
   spectra (12%) were removed because "Several of the spectra in the Granite 50% dust test dataset have a label
   that does not correspond to any of the labels in the training dataset" (arXiv 2601.16107). That is nearly half
   of granite-dusty, which leaves 5,183. Out-of-library spectra are exactly the hard cases a rover meets.
   Clean and 50%-dust spectra share one group each, with no flag, so per-condition results (the point of the
   paper) cannot be reported.
   The slab labels include powder-mixture classes (e.g. "Forsterite-albite mix" 30 + 3, "Quartz-albite mix" 132)
   and "Forsterite" in granite (147). On a rock slab these must mean "spectrum shows two phases", which is not the
   same as the reference class. A crude nearest-centroid check agrees with the slab labels for 77-100% of each
   main class, so the labels match the spectra, but I could not find how they were assigned.
   Change: record the removal in task.md, add a dust_condition column if the raw files allow it (group by slab
   still), and report accuracy or balanced accuracy.

5. Metric choice on the slab test. [Minor]
   Evidence: the slab classes are very imbalanced: Gypsum 16, Fo-alb mix 33, Fo-aug mix 44, Enstatite 132, versus
   Quartz 7,921 and Augite 8,291. Per-slab macro-F1 is about 0.37-0.40 even when accuracy is 0.80-0.89, because
   rare or absent classes dominate the average.
   Change: use accuracy, balanced accuracy or log-loss over all slabs, not per-slab macro-F1.

6. Is it "tabular" enough? [Design choice, declare it]
   950 ordered, highly collinear channels from one 1-D signal. The domain standard is baseline correction plus a
   CNN. RamanBench shows tabular foundation models are competitive, so including it is defensible, but it should
   be flagged as a spectral special-feature task. On a random split it is saturated (0.99), so it only carries
   information under the reference -> slab split. There, the spread is real and useful: 1-NN cosine 0.66, raw
   LightGBM 0.71, SNV logistic 0.80, normalised LightGBM 0.85. The literature reports CNNs at about 0.80 and
   RF at 0.69 (arXiv 2601.16107).

7. Housekeeping. [Minor]
   - 2 rows have truncated spectra with NaN tails: row 9204, calcite, 162 NaN channels from raman_938; row 67485,
     quartz, 487 NaN channels from raman_613. Keep them as NaN or drop them.
   - No exact duplicate feature rows. Rows are shuffled. Target and group are categoricals; all features are
     float64.
   - The values carry 2 decimals and lie on an integer cm-1 grid of 150-1099. RamanBench lists 141-1100 cm-1
     with 1,836 features, so this table was trimmed or resampled from a finer grid. That is acceptable; the
     source code itself trims to [150,1100]. The method is not documented.
   - Size: 125k x 950 float64, about 0.95 GB in memory and a 573 MB parquet. Fine for scoring, but foundation
     models will need subsampling (RamanBench capped training at 10k).
   - License: the paper and code are CC BY-NC. The NASA AHED dataset page says "License: BY-NC", but its badge
     links CC BY-NC-ND 4.0. A "no derivatives" clause would matter for redistributing a reprocessed table, so check
     the ODR licence.

DATA IS WHAT IT CLAIMS
Real laboratory spectra (LabRAM HR Evolution, 532 nm, per arXiv 2601.16107), not generated. The reference maps
show the right peaks: albite 507/479, forsterite doublet 821/853, and the spectrum maximum at 461-465 cm-1 in 880/1000 rows of even the
weakest quartz map. A crude nearest-centroid check puts 93-100% of each reference map's rows in its own class,
except the forsterite-albite mix map (76%). Values are
plausible CCD counts (baseline about 1,040-6,000, max 67,052).

WHAT I COULD NOT CHECK
- The original paper's full text (Wiley returned 403) and the ODR download (odr.io/MLROD returned 403). So I could
  not verify how the slab labels were assigned (by hand, by matching against references, or by a model), which
  maps come from the same physical specimen, or the raw wavenumber grid and resampling.
- The benchmark's actual fold assignment. task.md says only "1 repeats x 2 folds", grouped by specimen. My
  conclusions hold for every 2-fold grouping I tried.
- Which slab rows are 0% and which are 50% dust. Row order is shuffled and no flag exists.
- Process note: while setting up a download folder I noticed pre-existing files in an existing scratchpad
  sub-folder (dey.pdf, msr.pdf, tr.pdf, tse.pdf and .txt). They are not mine. I did not open or use them.

SOURCES
doi 10.1029/2021EA002125 (abstract via Semantic Scholar and Crossref); ahed.nasa.gov/datasets/f5b6051bfeb18c5a7eaef6504582;
github.com/GenTeML/Spec-CNN (README, helper.py); zenodo.org/record/7036374; arxiv.org/abs/2605.02003 (RamanBench:
MLROD 130,061 spectra, 16 classes, 141-1100 cm-1, random 80/20 splits, TabICL v2 macro-F1 0.990);
arxiv.org/html/2601.16107 (MLROD counts, test-label removal, model accuracies on slabs).
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT - raman_mlrod (target mineral, 15 classes, log_loss, grouped by specimen, 1x2 splits)
Kit: participant_kit/ ; scripts and logs in participant_kit/work/ ; all scores from score.py on the shipped splits.

VERDICT
The task can be gamed heavily: each test fold is exactly one rock (r0f0 = gabbro slab, r0f1 = granite slab) and the
training side always holds the other rock, so "down-weight the minerals of the training slab" plus "average each row with
its 50 nearest test rows" cuts the untuned baseline from 2.757 to 0.939 and the best honest model from 0.666 to 0.431,
which equals the ceiling you get from knowing the test rock's true class set (0.431). One reference map
(aug_train_15s_1000) looks like a scan of the gabbro test rock and carries most of the honest fold-0 score.

SPLIT FACTS
 r0f0: test = gabbro slab (18,692 rows: Augite 44%, Anorthite 38%, Forsterite 12%, Calcite 4%, 4 tiny classes);
       train = 33 reference maps (one mineral each) + granite slab.
 r0f1: test = granite slab (16,211 rows: Quartz 49%, Albite 21%, Microcline 18%, Hornblende 6%, Muscovite 3%, ...);
       train = reference maps + gabbro slab.
 The two slabs share only Forsterite and Forsterite-albite mix (both small in one of them). Rows are shuffled.

MODELS (mean of r0f0, r0f1; per split in brackets)
 B0  baseline: untuned LightGBM on features()                                   2.757 [2.447, 3.068]   work/baseline.py raw
     noise: same + 1 random column, 2 seeds                                     [2.438, 3.021], [2.420, 3.033] -> spread up to 0.05
 H1  per-spectrum normalization (subtract own 5th pct, divide by own SD)        1.587 [1.375, 1.799]   work/baseline.py norm
 H2  H1 + temperature fitted on the training slab (model fit on refs only)      0.912 [0.913, 0.911]   work/honest2.py norm
 H3  H1 trained on reference maps only + temperature fitted on training slab    0.666 [0.728, 0.605]   work/honest2.py norm (normrefcal)
 H1-H3 use only each test row's own spectrum and training data: signal, not exploits. H3 is the best honest model.

EXPLOITS, ranked by gain (lower log_loss is better; gain = exploited - honest)
| # | Exploit | Script | Honest score | Exploited score | Gain (per split) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Split rule + test-rock kNN: multiply classes with >=1% share in the training slab by 0.02, then average each test row's probabilities with its 50 nearest test rows (PCA of normalized spectra) | work/exploits.py (splitrule_knn50) | B0 2.757 / H3 0.666 | 0.939 / 0.431 | B0: -1.549, -2.088 ; H3: -0.286, -0.184 | No: it uses the knowledge that the test rock is the other slab and lacks its minerals, plus the other spectra of the same rock (context: none) | Train on reference maps only and test both slabs in one fold (the source design); enforce row-by-row prediction |
| 2 | Same-rock reference map: aug_train_15s_1000 is nearly indistinguishable from the gabbro test rock's augite | work/same_rock.py, same_rock2.py, drop_map.py | H1 r0f0 without the map 4.072 | H1 r0f0 with it 1.375 | r0f0: -2.697 (control: dropping the other augite map costs only 0.293) | No, if the map was measured on the gabbro slab (unverified) | Put that map in the gabbro slab's group (or drop it); check ms_train_015s_5900 vs granite too |
| 3 | Split rule alone (training data only + split design) | work/exploits.py (splitrule) | B0 2.757 / H3 0.666 | 1.988 / 0.477 | B0: -0.822, -0.717 ; H3: -0.259, -0.120 | No (a new rock may hold any mineral) | as #1: no slab in training, both slabs in one test fold |
| 4 | Test-rock kNN smoothing alone (k=50) | work/exploits.py (knn50), work/test_smooth.py | B0 2.757 / H3 0.666 | 1.416 / 0.593 | B0: -0.990, -1.694 ; H3: -0.062, -0.085 (vs calibrated raw B0+T 1.271 -> 1.037: -0.211, -0.256) | No: other spectra of the same rock | enforce row-by-row prediction (no batch context) |
| 5 | EM class prior of the test rock (Saerens 2002) | work/prior_shift.py, exploits.py (em) | B0 2.757 / H3 0.666 | 2.505 / 0.520 | B0: -0.527, +0.022 ; H3: -0.386, +0.094 (unstable: helps gabbro, hurts granite) | No | same as #1 |
| 6 | Self-training on the test rock (pseudo-labels with p>=0.9 from #1+EM on H1, refit) | work/self_train.py | H1 + splitrule+EM+kNN 0.551 | 0.675 | r0f0 -0.071, r0f1 +0.319 (unstable) | No | row-by-row prediction |
| 7 | Importance weights from a train-vs-test classifier (upweights aug_train_15s_1000 x18 in r0f0) | work/adv_weight.py | H1 1.587 | 1.549 | r0f0 -0.168, r0f1 +0.092 (unstable) | No | as #2 |
| - | Ceiling, not an exploit: true class set of the test rock | work/exploits.py (oracle_set) | B0 2.757 / H3 0.666 | 1.457 / 0.431 | B0: -1.434, -1.167 ; H3: -0.300, -0.171 | - | - |
All gains except #6/#7 r0f1 are far beyond the noise spread (0.05). k=50 was the best of k in {5,10,20,50} on the test
folds (mild test tuning); the 0.02 factor and 1% threshold were fixed before scoring.

FLAWS THAT HURT AN HONEST MODEL
| # | What is wrong | Honest choice | Score as shipped | Score with honest choice | Fix |
|---|---|---|---|---|---|
| A | With only two rocks, each fold trains on one slab whose "slab-measured" look is confounded with that rock's mineral set; its plagioclase is the other end member (gabbro anorthite vs granite albite) | Train on reference maps only (the source's own design) | B0 2.757 [2.447, 3.068]; H1 1.587; H2 0.912 [0.913, 0.911] | raw 2.410 [2.283, 2.538]; norm 1.034 [1.075, 0.994]; H3 0.666 [0.728, 0.605] | Drop the slabs from training: one split, train = reference maps, test = both slabs |
Mechanism: in r0f1 the baseline labels granite Albite as Anorthite (Albite accuracy 0.18, mean -log p 8.9, 1.90 of the
3.07 loss) because the only slab-measured feldspar in training is the gabbro's anorthite; trained on references only
(H3) Albite accuracy is 0.44 and its loss contribution 0.45. A deployed model trained on many rocks would not see this
confound; a single training rock makes it. The choice cannot be validated inside a training side that holds one slab.

FINDINGS
1/3/5. Test fold = one rock, training holds the other rock. The two slabs' mineral sets are almost disjoint, so the
   classes that dominate the training slab (r0f0: Quartz, Albite, Microcline, Hornblende, Muscovite, Biotite; r0f1:
   Augite, Anorthite, Forsterite, Calcite) are (nearly) absent from the test rock. Scaling them by 0.02 needs no test
   data and lowers H3 from 0.666 to 0.477 and B0 from 2.757 to 1.988. EM on the test rows estimates the rock's mix
   (gabbro: Augite 0.39/Anorthite 0.32 vs true 0.44/0.38) but mistakes granite albite for anorthite, so it is unstable.
   Mildest fix: no slab in training; test the two slabs together (one fold) so no class set can be negated and the
   test mix is two rocks.
4. Test rows of one rock cluster by mineral: a test row's nearest test row has the same label 96.2% (gabbro) and 97.4%
   (granite) of the time. Averaging over 50 test neighbours removes most of the baseline's overconfidence (B0 is worse
   than the training prior on r0f1: 3.068 vs 2.634) and adds information beyond calibration (calibrated B0 1.271 ->
   1.037; H3 0.666 -> 0.593). With "context: none" this uses group context. Mildest fix: the harness predicts rows one at
   a time (or in random batches mixed across rocks); a split cannot block it.
2. aug_train_15s_1000 vs gabbro-slab augite: median raw spectra differ by 2.7 counts (5th percentile 1124.4 vs 1126.7,
   corr 0.983; the other augite map differs by 131.6, corr 0.67); a classifier separates them with AUC 0.91 (raw) where
   every other map/slab-mineral pair gives 0.99-1.00 (except ms_train_015s_5900 vs granite muscovite, 0.92/0.88). It is
   the nearest training specimen for 84% of gabbro augite rows. Dropping it from training: H1 r0f0 1.375 -> 4.072
   (accuracy 0.765 -> 0.337, augite accuracy 0.84 -> 0.02); dropping the other, 5x larger augite map: -> 1.668. If this
   map is a scan of the gabbro slab, fold 0 tests a rock already measured in training and the honest score is inflated
   by about 2.7. The fact that decides it: the MLROD sample metadata for that map. Fix: give it specimen = gabbro slab
   (held out with it) or drop it; same check for ms_train_015s_5900 (only muscovite map, cannot be ablated in r0f1).
6/7. Self-training and importance weighting each help one fold and hurt the other.

ATTACKS THAT FOUND NOTHING
- Row order: rows are shuffled. Next-row label agreement in the slabs 0.360 vs 0.357 expected (gabbro), 0.317 vs 0.321
  (granite); label shares flat over position quintiles; LightGBM on row position alone 2.915 / 2.647 vs training prior
  2.898 / 2.634.  (work/explore1.py, explore2.py, format_order.py)
- Exact copies: 0 duplicated spectra (full rows and first-50-point prefixes) among 125,244 rows.  (work/explore2.py)
- Formats: values carry 6 significant digits (2 decimals below 10,000, 1 decimal above), so precision follows intensity
  only; trailing-zero share 0.098-0.111 per class except Gypsum 0.25 (its intensities exceed 10,000). Format-only
  LightGBM 2.899 / 2.680 vs prior 2.898 / 2.634.  (work/format_order.py)
- Identifiers: no id column; specimen is excluded; NaN points occur only in 3 reference maps (training side only).
- Transforms over all rows: raw counts (about 1,000-29,000), no table-wide scaling or ranks.
- Train-vs-test classifier: AUC 0.997-0.999 (the test rock is trivially separable, an expected domain shift); its only
  use was locating the same-rock map (#2, #7).  (work/adversarial.py)
- Web: no competition, forum or "magic feature" exists for MLROD. RamanBench (arXiv 2605.02003) uses random 80/20
  splits of 130,061 spectra x 1,836 points (141-1100 cm-1), 16 classes; the kit has 125,244 rows x 950 points on an
  integer 150-1099 cm-1 grid and 15 classes, so preparation dropped 4,817 rows and one class and resampled the axis.
  The source code (GitHub GenTeML/Spec-CNN) trains on reference spectra and keeps a separate labeled test set.
- Looking rows up in the published MLROD files: not tried (odr.io returned 403); not a task flaw either way.

COULD NOT CHECK
- Whether aug_train_15s_1000 / ms_train_015s_5900 were measured on the test slabs (paper and ODR pages blocked: Wiley 403,
  eScholarship 403, odr.io 403).
- How the slab spectra were labeled. 147 "Forsterite" and 3 "Forsterite-albite mix" rows in the granite are geologically
  odd (olivine is not a granite mineral) and hint at model-made labels; if the slab labels are the source CNN's output,
  a model that mimics that CNN would gain, and the labels would not be ground truth.
- Training rows from the future: not applicable (no time column).
- Variance across more splits: only 1 repeat x 2 folds; every number above is per split.

SOURCES
- https://arxiv.org/html/2605.02003 (RamanBench; saved as work/ramanbench.html)
- https://ahed.nasa.gov/datasets/f5b6051bfeb18c5a7eaef6504582 (MLROD landing page)
- https://zenodo.org/record/7036374 and https://github.com/GenTeML/Spec-CNN (source code)
- https://doi.org/10.1029/2021EA002125 (not readable: 403)
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER: raman_mlrod (2026-11-09)

Inputs: the definition and README (W/datasets/_dev/tabarena-v0pt2/raman_mlrod/), the record
(W/curation/records/raman_mlrod.md; its only curator line is CC 2026-11-08, Lennart, accepted for adding), the builder's
report (draft issues 1-8), claims.md, the probe outputs, register.json (5,937 decisions, 34 flags; none names this
dataset), the knowledge files of df-large, the source's code (the run folder, Spec-CNN), Sineesh and Kamsali
2026 (the run folder), and the precedent-checker reports of bacteria_id_raman, milk_nir_composition
and uniform_soybean_tests_yield. No other phase-A report of this panel existed when this was written (work folders
only), so none is cited. The in-batch siblings (bacteria_id_raman, milk_nir_composition, uniform_soybean_tests_yield,
ugr16_isp_netflow_intrusion) carry AI recommendations that no curator has accepted yet. They are cited as pairs to
decide alike, not as precedents.


======================================================================================================================
SUMMARY
======================================================================================================================

  D1 SEL-12 pending a tuned / TabPFN run .......................... consistent; the cited sibling is misread (bacteria
                                                                      was judged keep, not pending) and the source's
                                                                      own CNN result is missing from issue 1
  D2 Two rock folds, reference maps always in training ............ consistent (heart_disease, force_2020, SPLIT-4/29);
                                                                      bacteria's TP-5 reading does not carry over
     Five warnings ................................................. all consistent; two acceptance texts need counts
  D3 Code 9 -> 8 repair ........................................... consistent with mortgage; PROV-13's origin check
                                                                      still open
  D4 Code 15 drop ................................................. consistent (force_2020's Basement, audiology);
                                                                      TP-7's probes on the source's labels not reported
  D5 Third-party mirror, counts matching a paper .................. consistent with PROV-1 and PROV-8; departs from the
                                                                      run brief's mirror bar, with a stated reason that
                                                                      is weaker than any accepted copy; the curator's
                                                                      checksum (issue 5) decides; decide ugr16 alike
  D6 The source's band-minimum grid ............................... consistent (spectra.md: prefer the source's grid)
  D7 Two truncated spectra set missing ............................ consistent (CLEAN-26 as amended, inner branch)
  D8 Grid texture by class, kept with a note ...................... departs from the letter of a Must (LEAK-13), with a
                                                                      stated reason that is the rule's purpose; a Must
                                                                      takes no exception: prompt C1
  D9 Fallback log_loss ............................................ consistent (MET-5, MET-6; gallstone, heart_disease)

Judgment record:
  Validity: SEL-12 open, pending a measured comparison (TP-1 practice); SPLIT-4 and SPLIT-29 hold (heart_disease's
    shape); PROV-1 and PROV-8 hold, but the copy is not checked against the original (issue 5); PROV-13 repair as
    mortgage; USE-5 and TP-7 drop as force_2020's Basement; LEAK-13 kept by a reading of a Must (C1).
  Value: MET-5 and MET-6 hold (fallback); TP-5 not triggered in the scored unit; TP-8 short classes kept (mic).
  Quality: CLEAN-26 grid and missing positions as written.
  No drift, and no reason has reached its third exception. One prompt for the curator (C1).

======================================================================================================================
D1. IS A TABULAR MODEL COMPETITIVE ON A 950-BAND SPECTRUM? (SEL-12 Must, SEL-15 weighed; builder issue 1)
======================================================================================================================

Precedents:
- The SEL-15 weighed factor "A spectrum" (amended 2026-11-02, Lennart; W/.claude/skills/knowledge-curation/references/
  selection.md): "it is in scope unless a spectrum model is clearly better (SEL-12)". So without such evidence a
  spectrum is in scope.
- selection.md Cases holds no SEL-12 case for spectra. The kept spectrum datasets were never measured against a
  spectrum model: pancreatic_cancer_mouse_detection (2026-11-02), micro_mass (2026-10-12) and
  open_soil_spectral_library (ship 2026-11-05), whose field's incumbents are tabular (Cubist, PLS).
- Keeping a dataset pending tuned results follows TP-1 practice: open_university (TP-3, "kept pending tuned
  results", 2026-10-22, Lennart) and heart_disease (TP-1, "re-check with tuned results after the build", 2026-10-27).
- In-batch pair: bacteria_id_raman's builder judged SEL-12 "pass, concern noted ... SEL-12/SEL-15 judged keep"
  (the run folder, checklist P2), and its panel raised no SEL-12 point. Issue 1 here says
  "keep pending that run, as for bacteria_id_raman". That misreads the sibling: bacteria was judged keep, not pending.

Facts that set raman_mlrod apart from bacteria (all are in the data or the source; issue 1 states none of them):
- On our folds the untuned trees score worse than the dummy: random forest 3.158 and LightGBM 2.906, against 2.766.
  In bacteria, untuned LightGBM reaches a patient accuracy of 0.97 to 1.00.
- The source's own CNN, trained on the reference maps only, reaches accuracy 1.00 and macro F1 0.98 on the 19,980
  clean slab spectra (Spec-CNN, Notebook-CNN-Raw_Data.ipynb, cell 12, classification_report on argmax). This is the
  source's own result, which EV-4 counts as a modality signal (the source's own competition or paper is no "other
  benchmark"). Issue 1 cites only Sineesh and Kamsali, which EV-4 rules out as evidence. The source's other notebooks
  print a dense MLP on the raw spectra at accuracy 0.55 (Notebook-MLP-Raw_Data.ipynb, cell 13, on a 7,981-spectrum
  test set, not the same one) and its CWT-image CNN at 0.77 on the same 19,980 (Notebook-CNN-CWT-Data.ipynb, cell 12).
  For bacteria the source's own gap was CNN 82.2% against LR 75.7%.
- For orientation only (EV-4, no evidence), Sineesh and Kamsali, Table 3: grid-searched random forest and SVC reach
  69.2% and 70.8% overall on MLROD, against 78.0% to 80.3% for four of the five CNNs. On bacteria's treatment task
  (Table 5) the gap is 94.1% against 97.1%.

Verdict: consistent. A scope Must held open for a measured comparison follows TP-1 practice, and the stated default
leans to keeping the dataset. Two precision fixes for issue 1:
  (1) Cite the source's own CNN result and drop "as for bacteria_id_raman". If the curator keeps bacteria now and
      holds raman, the facts above are the reason, written down.
  (2) The decisive experiment as written, tuned methods and TabPFN v3.5 on the shipped folds, has no spectrum model
      to compare against. SEL-12 asks whether a spectrum model is clearly better, so either run the source's Spec-CNN
      on the two folds (the code is in the run folder), or run the tuned methods and TabPFN on the source's
      own design (reference maps train, clean slabs test), where the source's CNN scored 1.00.

======================================================================================================================
D2. TWO ROCK FOLDS, REFERENCE MAPS ALWAYS IN TRAINING (SPLIT-1, SPLIT-4, SPLIT-5, SPLIT-29 Must; TP-5, TP-8 Must;
    weighed "only a few groups"; builder issue 2 and the five warnings)
======================================================================================================================

Precedents:
- heart_disease (Lennart, 2026-10-27; splits.md Cases, "Few groups (factor)"; W/datasets/_dev/tabarena-v0pt2/
  heart_disease/dataset.py). Three hospitals, leave one out. The source built its model in Cleveland and applied it
  at the other hospitals; our split tests every hospital in turn, with the others training. Labels are per patient,
  and SPLIT-1, SPLIT-4 and SPLIT-23 outweighed the few-groups factor. Accepted `groups_test_groups_few` ("Each fold
  still scores 199 to 303 patients one by one (smallest class: 51)") and `splits_dimensions_off_protocol` ("Leave one
  hospital out gives exactly three splits. More repeats would split the same three hospitals the same way").
  raman_mlrod has the same shape: one site per fold, labels per row, every rock tested in turn with the other
  training, a widening of the source's one-fold design.
- covertype (3 wilderness areas, IID instead): set apart, because a new row comes from a known area, while a rover's
  target rock is unseen (SPLIT-4). Here IID scores 0.072 against 0.63 to 1.64 held out, the map-recognition gain of
  SPLIT-29.
- spectra.md, "Splits": "hold the group out (... MLROD's map points by specimen)", already written for this source.
- force_2020 (TP-8 case, kept 2026-10-12; accepted `splits_test_class_missing` with counts per fold): a class a
  grouped split leaves out of a fold because few groups hold it is not a small class. raman_mlrod is the same kind:
  every class is tested in some fold and present in every training side (claim auditor's container check:
  train_classes_missing empty on both folds). It differs in extent: 6 or 7 of 15 classes are absent from each fold,
  against 2 of 11 classes missing one of 3 folds.
- bacteria_id_raman's TP-5 reading (its precedent checker, 2026-11-09) counts the unit the score counts, a patient
  under its MET-17 weight. raman_mlrod scores each point (MET-17 does not apply, the definition says why): 18,692 and
  16,211 scored points per fold. The smallest tested classes are the Forsterite-albite mix (3 rows in the granite
  fold), gypsum (16), the Forsterite-albite mix (30) and the Forsterite-augite mix (44) in the gabbro fold. Each
  carries 0.2% of its fold's log loss or less (probes/class_loss_share.json). That is TP-8's mic reading (a rare
  class with its share of the loss stays), not TP-5's parkinsons. The bacteria reading does not carry over, as that
  checker also said, and the two `groups_test_groups_few` texts should not cite each other.
- The weighed factor "Only a few groups" (−) is heavier here than in heart_disease on two facts. There are 2 groups,
  not 3. And within a rock a class sits in one or two contiguous blocks: the gabbro maps are labelled in 6 and 4 runs,
  so a fold's score for a class rests on one or two regions, where heart_disease had 51 or more independent patients
  per class and no class dropping out. This is a weighing for the curator (issue 2), not a departure from a rule.
- SPLIT-5: the source's design was checked (reference maps train, both rocks tested at once). Adding the other rock to
  training is heart_disease's leave-one-out, measured to help on both rocks (gabbro 1.97 to 1.64, granite 0.94 to
  0.63).

The five warnings:
- `splits_rows_never_tested`: consistent with bacteria_id_raman, which has the same design (the source trains on its
  reference library). The two would be the first by-design acceptances; the earlier ones were 500k trims, all dropped
  on 2026-11-08 (bacteria's checker). Word the two alike and file one Cases row.
- `splits_dimensions_off_protocol`: consistent with heart_disease, for the same reason.
- `groups_test_groups_few`: consistent with heart_disease's reading. The proposed text gives the signal but not
  heart_disease's per-class count in the scored unit. Add it ("each fold scores 18,692 and 16,211 points one by one;
  the smallest tested classes are 3 and 16 rows, under 0.2% of the loss") and the TP-8 sentence. Wording point for
  the house rules: definitions.md's check table asks for "more than a handful of groups of each class per fold (else
  `Too Small`)". heart_disease and raman_mlrod read "groups" as the scored unit for per-sample labels. Saying so in
  definitions.md keeps the two from reading as departures later.
- `splits_test_class_missing`: consistent with force_2020. Give the classes per fold, as force_2020's text does.
- `dataset_spectrum`: D7.

Note for the split auditor (not a precedent point): the gabbro fold's gypsum (16) and Forsterite-albite mix (30) come
only from L_raw_gabbro0dust_test_015s_46_final, which holds no gabbro mineral. force_2020's reading assumes the class
belongs to the rock; here it rests on the file name.

Verdict: consistent.

======================================================================================================================
D3. CODE 9 -> 8 IN THE DUSTY GABBRO (PROV-13 Must; TP-6; builder issue 3)
======================================================================================================================

Precedents:
- mortgage (Lennart, 2026-10-22; "Exception to LEAK-20" in W/curation/records/mortgage.md; leak_checks.md LEAK-20).
  For 7 loans, period 51 is doubled with only the status differing. The payoff copy was kept because all 7 loans end
  at period 51, so the active copy is damage to the file: a repair toward what the file itself records, made without
  the origin. The register flags this as an exception to PROV-13, a Must; read closely, the exception is to LEAK-20
  and PROV-13 is its reason. No conflict.
- nci_aids_antiviral_screen (Lennart, 2026-11-02): the source's charge code read as +1 on 690 compounds, a repair from
  the source's own documentation.
- SUPPORT2, ashrae, framingham_heart_study_fhs (PROV-13 and PROV-14 cases): repairs from the origin's files.
- principles.md, Tensions, "Repair against cleaning around damage": repair or rebuild from the origin first; when the
  origin cannot be reached, keep with a note or retire.
- TP-6, "a fix of our own invention ... is not a better version": this is about versions of a task, not about damage.

Comparison: the right code comes from the release itself. The clean gabbro map labels the same rock's plagioclase 8,
in blocks of 3,537 and 3,540 spectra. The measured evidence agrees: a correlation of 0.977 against 0.615, and bands at
507/482 against 511/473 cm-1. That is mortgage's pattern, a repair toward the release's own record. It is weaker than
mortgage in one fact: mortgage's evidence was deterministic, while here a library-trained model calls 1,911 of the
3,540 spectra anorthite (54%). The step PROV-13 names first, checking whether the origin has the clean data, is still
open: ODR in a browser, the paper (Earth and Space Science is open access; the 403 is a bot block) and the authors. The
choice moves the score: anorthite carries 49.9% of the gabbro fold's log loss.

Verdict: consistent with mortgage. Write in the record the fact that sets it apart from "a fix of our own invention":
the release's own code for the same block. Put PROV-13's origin check into issue 5's browser session. Option (c),
keeping code 9, is not reasonable under the ranking, since it keeps a label known to be another mineral (USE-5, P5).
Option (b), the drop, sits one step lower on the remedy ladder than a repair.

======================================================================================================================
D4. CODE 15 ("UNKNOWN") DROPPED (USE-5, TP-7, CLEAN-17; builder issue 4)
======================================================================================================================

Precedents:
- force_2020, Basement (CLEAN-17 case, Lennart, 2026-10-21): "a class that lives in one group cannot be on the train
  and the test side of a split by that group", dropped.
- audiology_diagnosis (TP-7 case, 2026-10-06): the non-hearing-loss diagnoses were dropped when the target was
  redefined.
- rain_in_australia (Lennart, 2026-10-26, USE-5): rows whose label is another quantity were dropped. ames_housing
  (2026-10-26): "as we know from the metadata what data to use to build the real task".
- The established convention TP-7 asks for: Sineesh and Kamsali, Sec. 4.1, footnote 2: "We have ignored these samples
  for the purposes of evaluation".

Comparison: code 15 lives in one group only (the dusty granite map) and names no mineral. That is Basement's
mechanism, plus a USE-5 reason.

Verdict: consistent. Two points:
  (1) The source scores code 15 as an "unknown" through its threshold rule (`dec_pred` sets 15), so our closed-set
      task leaves out the open-set part of the source's design. The task summary or fit_reason should say that the
      test covers points of the 15 minerals only. A rover meets dust points; the score does not.
  (2) TP-7 and LEAK-4 (both Must) ask for the probes on the source's labels too, with code 15 kept and code 9 as
      shipped. The builder's report does not say they ran (audiology's case).

======================================================================================================================
D5. FILES FROM A THIRD-PARTY MIRROR WHOSE COUNTS MATCH A PAPER'S (PROV-1, PROV-2, PROV-8, PROV-16; builder issue 5)
======================================================================================================================

Precedents and pairs:
- uniform_soybean_tests_yield (in-batch, AI panel 2026-11-09): the original was gone for everyone. A course
  participant's CyVerse copy was accepted after a record-for-record match with the authors' own GitHub files.
- ai4d_lab_tanzania_tourism_classification_challenge (Myunghwan, October 2026): a student's GitHub commit, accepted on
  a byte match with the official Zindi archive.
- pricing_game_2017_french_mtpl (definition 2026-11-01, reviewed by Lennart 2026-11-08): the organiser's package,
  pinned with sha256.
- ugr16_isp_netflow_intrusion (in-batch, on hold): a Hugging Face mirror, because the official site refuses this
  machine, checked only against the mirror's own manifest.
- numerai_v5_2 (Lennart, 2026-10-26; the original retired): "search for community mirrors if any exist, otherwise we
  can keep our local versions".
- The run brief (the run folder): "a server that refuses this machine. Do not work around it (no credentials of
  your own, no mirrors of doubtful origin)".

Comparison:
- raman_mlrod is ugr16's situation (the original exists, refuses this machine and is reachable by a person), not
  uniform_soybean's (the original gone).
- Its evidence:
  - The maintainer is identifiable: raman-data, RamanBench's loader.
  - The row counts equal Sineesh and Kamsali's ODR download. Checked in the text: Sec. 4.1, footnote 2, "When we
    downloaded the data from the official website, the training dataset had 90,341 spectra"; test 8,952 / 9,740 /
    11,028 / 10,000.
  - The per-class supports equal the source notebook's output.
- This independent evidence is stronger than ugr16's manifest, but weaker than uniform_soybean's record match and
  ai4d's bytes.
- Against it: Apple Numbers metadata on two files (opened, possibly saved again).
- PROV-1 holds (a known source: the paper and the data DOI), and PROV-8 holds (download_description names the copy
  and says what it copies). PROV-2 is not needed.
- PROV-16: the claims attributed to Sineesh and Kamsali carry the section and a quote. The paper's own claims (the use
  case, "+99% success", "500,000+") come from the abstract, which PROV-16 excludes. Definitions have shipped with a
  "full text 403 / not read" note (garments_worker_productivity's metric reason, aegis_bronchial_airway_lung_cancer),
  so this is practice. The same browser session can fetch the paper (open access).

Verdict: consistent with PROV-1 and PROV-8. The copy departs from the run brief's bar, with a stated reason (an
identifiable maintainer, independent counts). The curator's sha256 of 2-3 files against odr.io/MLROD (issue 5) is the
decisive experiment (EV-1). A match makes it ai4d's pattern; a mismatch leaves it below every accepted copy. Decide
ugr16 alike: both rest on a server that refuses this machine. If one is accepted on weaker evidence than the other, the
record says which fact sets them apart.

======================================================================================================================
D6. THE SOURCE'S BAND-MINIMUM GRID AGAINST AN INTERPOLATION (CLEAN-26 Should; spectra.md; builder issue 6)
======================================================================================================================

Precedents:
- spectra.md, "What ships": "Spectra from instruments with different grids need one grid. Prefer the source's own
  common grid; an interpolation in `_clean` is a decision for the curation notes."
- The band minimum is the source's own (Spec-CNN `helper.raw_processing`). RamanBench's 1,836-point interpolation is
  another collection's version (EV-4: no reference). Sineesh and Kamsali's "standardizing the axis via interpolation
  and trimming" (Sec. 4.1) is third-party prose; the source's code ranks above it (EV-2 order).
- State `raw`: consistent with open_soil_spectral_library (KSSL's averaged export grid declared raw, 2026-11-04) and
  pancreatic (400 ppm bins declared raw, 2026-11-02).

Verdict: consistent. Precision: the source says the band minimum "cleans up the noise created by cosmic rays", while
the Spectrum description and claim 15 say "no cosmic-ray removal". Reword to "no cosmic-ray removal beyond the
source's band minimum".

======================================================================================================================
D7. TWO TRUNCATED SPECTRA SET MISSING (CLEAN-26 as amended 2026-11-05; builder issue 8; `dataset_spectrum`)
======================================================================================================================

Rule text: a fill at a position "is set missing and the column stays (CLEAN-11); when only an edge position holds it,
that position is dropped for every row". The runs of zeros from 938 and from 613 cm-1 to 1,099 cm-1 include inner
positions, so the set-missing branch applies. open_soil_spectral_library (53 spectra, only the 600 cm-1 edge) was the
edge branch and avoided the warning. This would be the first `dataset_spectrum` acceptance.

Verdict: consistent. Dropping the two never-tested rows is the other option: no rule path leads to it and no rule
forbids it, so the rule text decides for set-missing. The processing encodings return these two rows missing
(spectra.md, Pitfalls). Say so in the acceptance text.

======================================================================================================================
D8. GRID TEXTURE BY CLASS, KEPT WITH A NOTE (LEAK-13 Must, P4; builder issue 7)  -> prompt C1
======================================================================================================================

Precedents:
- hepatitis_c_prediction (7 lab columns rounded, `ALP` dropped), gallstone_disease (Andrej, 2026-10-26: measured
  precision restored, with LEAK-39) and chicago_traffic_crashes (Lennart, 2026-11-05: the time coarsened in `_clean`).
  Each harmonised a trace that the test rows carried.
- pancreatic_cancer_mouse_detection (TP-1 case 2026-10-06; spectra.md, SPLIT-30): a file marker that separates
  control spectra at AUC 0.67 was kept with an open question. That marker is present in tested rows too.

Comparison: here the trace follows the class only in the training-only reference maps (grid kind at ROC AUC 0.68). On
the test rocks the grid follows the map, and the roughness alone scores worse than the class shares (3.665 against
2.898 on the gabbro, 3.057 against 2.634 on the granite). So it cannot raise a test score. pancreatic kept a stronger
case.

Where it stands under the ranking: LEAK-13 is a Must and has no training-side scope. A Must takes no exception, and
what the keep serves (the source's grid, CLEAN-26 and spectra.md, a P7 Should) cannot outrank a P4 Must. So the keep is
either an application of LEAK-13 (the rule's purpose, honest evaluation, is not engaged) and filed as such, or the fix
is made. The builder's "no clean fix without smoothing" is not exact: one reading per 1 cm-1 band (the reading nearest
the band's centre) removes the min-of-two effect without smoothing, at the cost of leaving the source's grid. That also
gives LEAK-13's "first measure how much the fix removes" a measurement.

Verdict: departs from the letter of a Must, with a stated reason that is the rule's purpose. Prompt C1.

======================================================================================================================
D9. FALLBACK LOG LOSS AGAINST THE SOURCE'S PRECISION/RECALL/F1 WITH AN "UNKNOWN" THRESHOLD (MET-1 Must; MET-5, MET-6)
======================================================================================================================

Precedents:
- MET-5: gallstone_disease and early_stage_diabetes_risk_prediction (several metrics side by side, so the fallback;
  Lennart, 2026-10-21).
- MET-6: heart_disease and ljubljana_breast_cancer (accuracy with no fixed threshold or costs, so the fallback,
  2026-10-21).
- In-batch: bacteria_id_raman (fallback log loss).
- MET-17 does not apply, since each point is a decision (asp_potassco_classification and
  video_transcoding_time_prediction, kept unweighted).

Facts: the source reports scikit-learn's classification_report (precision, recall, F1, accuracy per class;
tradmodels.py scores the argmax). The unknown threshold is no fixed decision: 0.95 is `dec_pred`'s default (helper.py
line 221, cnnmodel_raw.py line 227), Notebook-CNN-Raw_Data sets 0.5 and Notebook-CNN-CWT-Data sets 0. The code-15 rows
are dropped (D4), so a reject option would have nothing to score. "+99% success" is a headline in the abstract (MET-5:
not by itself a deliberate choice).

Verdict: consistent. Precision: the metric reason and claim 37 say "0.5 or 0.98". I found no 0.98 in the notebooks or
the code; reword to "0.95 by default, 0.5 or 0 in the notebooks". The stale covertype line in MET-6 (bacteria's
checker) does not bear on this dataset.

======================================================================================================================
DRIFT AND AMENDMENT CHECKS
======================================================================================================================

- No drift. Lennart's few-groups calls (covertype IID; heart_disease grouped, 2026-10-27; huesken accepted, 2026-11-04)
  rest on different facts. His PROV-13 calls (mortgage 2026-10-22, nci_aids 2026-11-02) all repair toward a record.
- Second cases, none at three:
  - a reference library that trains and is never tested (bacteria_id_raman, raman_mlrod);
  - a label repaired toward the release's own record (mortgage, raman_mlrod);
  - a mirror for a server that refuses this machine (ugr16, raman_mlrod);
  - a class-linked trace kept where it cannot reach the score (pancreatic's batch marker in kind, raman_mlrod).
- Register flags: none names raman_mlrod.
  - mortgage's "exception_to_must PROV-13" reads the exception's reason as its rule (D3).
  - USE-5 "opposite outcomes" (diabetes_3, xente and others) rests on other facts.
  - The few_minority mechanism (7 keep, 1 exclude: alvin's temporal windows) agrees with keeping the
    Forsterite-albite mix.

======================================================================================================================
PROMPT FOR THE CURATOR (issue shape of review_file_format.md, turns)
======================================================================================================================

C1. **Consistency check (AI, 2026-11-09): Is a recording trace that follows the mineral only in the never-tested
    reference maps a case for harmonising?**

   * **Problem:**
     - In the reference maps each mineral comes on its own wavenumber grid. The band minimum makes fine-grid spectra
       lower and rougher, which tells the grid kind apart at ROC AUC 0.68[^l13].
     - On the two test rocks the grid follows the map, not the mineral, and the roughness alone scores worse than the
       class shares (3.67 against 2.90; 3.06 against 2.63).
     - The rule on class-specific recording is a Must with no training-side scope, and the source's grid cannot
       outrank it, so keeping the trace is either a reading of that rule or a change to it[^rank].
   * **Background:**
     - pancreatic_cancer_mouse_detection kept a file marker that separates control spectra at AUC 0.67, with an open
       question, though the marker sits in tested rows too[^cases].
     - hepatitis_c_prediction, gallstone_disease and chicago_traffic_crashes harmonised traces that the test rows
       carried.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep, filed as an application (implemented) | keep the source's band minimum; a Cases row says a trace that follows the class only in rows never tested, measured as no shortcut on the test side, is not a recording leak | the source's own grid; the measured fact sets it apart from the three harmonised cases; pancreatic kept a stronger case | the rule is read by its purpose, not its letter; models may still learn a texture that misleads them on a new rock |
     | b | One reading per band | take the reading nearest each 1 cm-1 band's centre instead of the minimum, so every grid gives one raw reading per band | no smoothing; removes the min-of-two trace by construction; measures how much the fix changes the scores | leaves the source's own grid, which the spectrum guide prefers; a choice of ours |
     | c | Amend the rule | write into the rule that it covers recording conventions the test rows carry by class | the next case follows a written line | a rule change from one dataset |

   * **Recommendation:** a, with the Cases row; b if a fit on both grids shows the trace changes the ranking of model
     families on the two folds. **Decision:** a, b or c?

   [^l13]: **LEAK-13** (Must; amended 2026-10-26, Andrej, on gallstone_disease): "Class-specific recording conventions
     are harmonised ... First measure how much the fix removes." Cases: hepatitis_c_prediction, gallstone_disease;
     chicago_traffic_crashes (applied, Lennart, 2026-11-05).
   [^rank]: principles.md: "A Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an
     amendment." spectra.md (under CLEAN-26, a Should, P7): "Prefer the source's own common grid".
   [^cases]: task_probes.md Cases, TP-1, pancreatic_cancer_mouse_detection (kept 2026-10-06: "the `t` file suffix is
     an open question in the record"); spectra.md, "Splits": the marker "separates some control spectra at AUC 0.67".

======================================================================================================================
PATHS
======================================================================================================================

Definition: W/datasets/_dev/tabarena-v0pt2/raman_mlrod/dataset.py
Record: W/curation/records/raman_mlrod.md
Builder: the run folder
Source code read: the run folder (helper.py, cnnmodel_raw.py, tradmodels.py,
  Notebook-CNN-Raw_Data.ipynb cell 12, Notebook-CNN-CWT-Data.ipynb)
Sineesh and Kamsali: the run folder (Sec. 4.1 with footnote 2; Tables 3 and 5)
Sibling reports: the run folder,
  the run folder,
  the run folder
Precedent definitions: W/datasets/_dev/tabarena-v0pt2/{heart_disease,force_2020_well_well_log_and_lithofacies_dataset_
  for_machine_learning_competition,huesken_sirna_efficacy,open_soil_spectral_library}/dataset.py
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE: raman_mlrod, opening brief (2026-11-09)
Position: ship, after changes that keep the data and the task. Fit stays approximate. Every Must problem the panel
found has a fix on the remedy ladder below exclusion (principles.md, How to decide 5). None calls for `No`.

1. The task is real and the split tests it. (USE-1, USE-10; SPLIT-1, SPLIT-4, SPLIT-29 Must; TP-5, TP-8 Must)
   - Claim: one point spectrum of a rock never measured, mineral called from a reference library. The source's own
     design is reference maps -> slabs (claim 30). The domain practitioner would use the task ("ship: yes"). Lab fit is
     nearly direct; the rover gap is in fit_reason.
   - Evidence: IID LR 0.072 against 0.63-1.64 held out; group probe ROC AUC 1.000 against 0.923. A split by map or by dust
     level leaks grains (split auditor: dusty against clean anorthite r 0.929 against 0.801 to the reference). So grouping
     by rock is the only honest partition. Every training side holds all 15 classes (claim auditor), and every class is
     tested in some fold.
   - Answers the blind reviewer's "blocking" concern: it simulated GroupKFold over 36 groups (classes with zero
     training rows). That is not the shipped split. The shipped split is the reference->slab design it recommends, one
     fold per rock.
   - Answers "two groups, noise 4-13x the per-row SE": that is the weighed factor "only a few groups" (−). It is no Must.
     TP-5 counts the scored unit: 18,692 and 16,211 points. The smallest classes carry under 0.2% of the loss. Rare
     classes elsewhere carry 3.5-8x their row share, far from alvin's 51-54% (TP-8 keep). A missing class is force_2020's
     kind (TP-8). heart_disease (3 hospitals, leave one out) is the precedent. No other partition adds groups, and IID is
     barred by a P4 Must. Fix: cite the noise and the counts in the `groups_test_groups_few` reason (split auditor's
     text).

2. The task gamer's largest exploits are evaluation-level leaks. A protocol line fixes them, not the data.
   (LEAK-9 Should, amended 2026-11-05)
   - Evidence: exploit #1/#4/#6 average over the 50 nearest TEST rows, or self-train on them. "Context: none", so this
     is transductive. LEAK-9 says such leaks are "fixed ... by a protocol line the benchmark checks, not in the data".
     Cases: medical_facility_operational_data, sepsis, 5g. Fix: add the line to splits_comment ("predict each spectrum
     on its own; no use of other test rows").
   - Exploit #3 (scale down the training slab's classes) lowers H3 from 0.666 to 0.477. It does not use test rows. It
     uses benchmark knowledge that no generic learner has: that the test rock is "the other one". The same protocol
     line can name it ("no prior from the fold design").
   - Concession: a protocol line is weaker than a design that removes the gap. Design B (reference maps train, both
     slabs in one fold) removes #3 and the gamer's flaw A (gabbro anorthite taught as the only slab feldspar). It is
     the source's own split (SPLIT-19 Should), and the split auditor measured the same model ranking under A and B
     (Kendall tau 1.0, five models).
   - So A with the protocol line, or B, both keep the dataset with the same ranking. It is a curator's call between two
     fixes, not a reason to exclude. If the curator keeps A, record it as an exception to SPLIT-19 (split auditor,
     problem 2), and reword claim 34 ("lowers on both rocks" holds for SNV-LR only).

3. aug_train_15s_1000 may be the gabbro's own augite. It is a question to settle, not a regrouping by similarity.
   (SPLIT-24 Must; EV-3, EV-6)
   - Evidence: twin correlations sit at the map's own level (0.972 against 0.982/0.975). The stake is large: gabbro
     augite accuracy 0.82 -> 0.002 without the map.
   - But SPLIT-24, a Must, forbids grouping "on a similarity-threshold cluster". A group needs a true id. EV-6:
     similarity cannot prove a shared specimen.
   - The calibration shows that one reference map carrying a test class is normal here. Albite drops 0.289 -> 0.004
     and microcline 0.989 -> 0.126 when their maps are dropped. Five classes have a single map. Quartz on the granite
     reaches reference quartz at 0.9968 against 0.9974 (claim 27) without any claim of a shared specimen.
   - Fix (keep with a note, one rung above exclusion): replace "every test rock stays unseen" with the question and its
     stake. The curator's browser session (the paper's sample list, ODR metadata) decides. On a yes, the map joins the
     gabbro group: a re-split that still keeps the dataset.
   - The 46-row "gabbro" map (gypsum + Fo-alb, row ids "gyp_foalb") is different: the row ids say it is no gabbro
     material. Fix: move it to the training side as a group of its own (column auditor (a)). Effect 0.784 -> 0.786.
   - Muscovite in hb_ms: keep with a note (column auditor: "do not drop it on this evidence").

4. The labels are the right target. The rock asymmetry under dust is a documented gap, which USE-5 allows.
   (USE-5 Must, PROV-13 Must)
   - Code 9 -> 8 is confirmed by four independent checks:
     - correlation 0.977 with the clean gabbro plagioclase block, 0.08/0.00 with the in-situ granite microcline;
     - main bands 507/482 against microcline's 511/473;
     - the nearest reference maps;
     - petrology.
     It repairs toward the release's own record (mortgage).
   - Code 15 dropped: force_2020's Basement, and Sineesh and Kamsali's own convention (TP-7).
   - Dust asymmetry (gabbro labels by grain, granite by spot): USE-5 itself says a label "whose construction is
     undocumented ... may ship with fit=approximate and a note naming the gap". Fit is already approximate. The
     practitioner measured the gabbro labels as readable: 86%, 89% and 60% of the dusty blocks read as their own
     block's mineral.
   - Fix: the note in fit_reason (closed set, labelling by rock) and in issue 4. No data change.

5. The defects found are cheap, and three of them need no weighing.
   - Fill-down row qtzalb_train_60s_3000 #2456 (346 readings = k x 4.11843): set bands 581-1,099 missing, as for the two
     cut-short rows (CLEAN-26, CLEAN-11; PROV-13 asks for no more because ODR is the check in point 7). It is one
     training row of 90,341 and is never tested.
   - Grid texture (LEAK-13 Must): I concede the letter. A Must takes no exception, and the source's grid (P7 Should)
     cannot outrank it. The claim auditor measured the fix: one reading per band (nearest k+0.5) removes the comb
     (AUC 0.651 -> 0.536) at no cost (LR gabbro 1.451 -> 1.253, granite 0.485 -> 0.497). LEAK-13 says to harmonise
     once the fix is measured. Take it (precedent checker's option b) and keep the 1 cm-1 resolution the practitioner
     needs.
   - Wording fixes:
     - the README citation goes to raw_processing and the (950, 1) input layer;
     - "1-3 readings per band";
     - "no cosmic-ray removal beyond the band minimum";
     - the encodings sentence (SNV wins for LightGBM; as-is stays by CLEAN-26);
     - claim 43's rare-class shares;
     - the metric reason's thresholds;
     - "112 saturated ship".

6. SEL-12 is open, and the defaults lean to keep. (SEL-12 Must; SEL-15 weighed: "a spectrum is in scope unless a
   spectrum model is clearly better")
   - The burden lies on "clearly better". The source's CNN reaches accuracy 1.00 on the clean slabs, an argmax
     accuracy on the source's design. Untuned tabular models on that design already reach 0.80 (SNV LR) and 0.85
     (normalised LightGBM) on all slabs, dusty included (blind reviewer). No tabular model has been tuned yet.
   - The field's tools are library search, PLS-DA, SVM, RF and kNN (practitioner), and a lab would try a tabular
     learner.
   - Fix: keep pending the run (TP-1 practice: open_university, heart_disease). Make it decisive as the precedent
     checker says: tuned + TabPFN v3.5 on the source design against Spec-CNN, or Spec-CNN on our folds. Drop "as for
     bacteria_id_raman" and cite the CNN's 1.00 in issue 1.
   - Concession: if the CNN is clearly better there, SEL-12 excludes the dataset. Nothing ranked above it rescues it.

7. Provenance holds as far as this machine can reach. The decisive check is one browser session. (PROV-1, PROV-8; EV-1)
   - The counts are independent of the mirror:
     - Sineesh and Kamsali's ODR download (90,341 / 8,952 / 9,740 / 11,028 / 10,000);
     - the source notebook's per-class support (exact, 0-14).
     That is stronger evidence than ugr16's manifest.
   - The Numbers metadata now has a known effect: one filled row (point 5).
   - Fix: in issue 5, compare the sha256 of qtzalb_train_60s_3000, the 4084 and the dusty-granite files against ODR.
   - Licence: AHED's text and the S2 record say "BY-NC". The badge links BY-NC-ND 4.0. Read ODR's licence in the same
     session.
   - Concession: under ND, redistributing a reprocessed table is a house-rule question that could stop shipping.
     Until then, "CC BY-NC (version not stated)" stays as written.

Judgment record (advocate's reading)
Verdict: ship after changes.
Validity:
- SPLIT-1/4/29 hold;
- LEAK-9 fixed by a protocol line (or B);
- SPLIT-24 holds (no similarity regroup), augite question noted;
- 46-row map moved to train;
- LEAK-13 fixed (one reading per band);
- USE-5 approximate with the gap named;
- PROV-13 repair holds; ODR check open;
- SEL-12 open, pending the run.
Value: TP-8 keep; few groups − with the noise cited.
Quality: fill-down masked (CLEAN-26); wording fixed.
For the curator: A+protocol or B; the augite sample list, sha256 and licence in one browser session; SEL-12 run.

Rebuttal
========
The critic and I agree on the verdict class: ship after changes, with no exclusion now. The differences are below.

C1 (SEL-12). Concede the remedy: Spec-CNN and tuned tabular models / TabPFN v3.5 on the same split, issue 1 rewritten
   with the source's 1.00, and "as for bacteria" dropped. One qualification, built from facts already on file and not
   a new point:
   - The 1.00 is argmax accuracy on the 19,980 clean slab spectra, against those slabs' labels.
   - The labelling of the slab maps is undocumented (C2).
   - If the granite's labels are a CNN's output, the 1.00 is partly circular.
   So the comparison should be read on the gabbro (block labels) as well as pooled. SEL-12 (Must) then decides; nothing
   ranked above it would rescue a clear CNN win.

C2 (USE-5, granite labels possibly the CNN's). Concede the conditional. If the source's CNN (or any thresholded
   classifier) set the granite labels, the granite target is a model's output, not a reading. USE-5 (Must) then fails
   for that fold, and approximate fit does not cover it: USE-5 allows a gap in an undocumented construction, not a
   label known to be a prediction.
   - Evidence against it, not proof:
     - The labels follow the spectra: dusty-granite albite and microcline show their own bands (column auditor).
     - 77-100% nearest-centroid agreement (blind reviewer).
     - The 147 "Forsterite" points show an Fe-olivine doublet at 817/850, so the label reads what the spot shows (by a
       person or by phase mapping). It does not read what lies under the dust.
     - A label of what the spot shows is still a reading.
   - Remedy on a "CNN-made": a filter, rung 2, not exclusion. The granite slab rows leave the task (no clean truth to
     train or test on). The task ships reference -> gabbro, whose 6+4 block labels by grain are no classifier's
     speckle.
   - Remedy on "hand or phase mapping": approximate fit with both label semantics named.
   - The curator's methods read settles it before ship. I accept that as a condition.

C3 (augite map). Agree: same fact, same remedy. Settle it in the browser session and replace "every test rock stays
   unseen" until then. I dispute only the framing "inflated by about 2.7".
   - That holds only on a "yes".
   - Albite (0.289 -> 0.004) and microcline (0.989 -> 0.126) depend on one map just as much, with no twin claim.
   - So dependence alone is not inflation (EV-6).

C4 (side maps). Concede both moves.
   - The 46-row map: the source's own ids ("gyp_foalb_test") are an exact basis (SPLIT-24).
   - The hb_ms muscovite block moves to training as a group of its own, on its id (`hb_ms_test`). It is not merged
     with ms_train_015s_5900: that would be a similarity group, which SPLIT-24 forbids. The hornblende block stays.
   - Fix the class counts (gabbro 6, not 8) in task_summary and in `splits_test_class_missing`.
   - Cost: logreg granite 1.079 -> 1.138; the ranking is unchanged.

C5 (design B against A plus a protocol line). Concede: ship B with the protocol line.
   - The critic is right that the split-rule exploit (0.666 -> 0.477, baseline 2.757 -> 1.988) uses only knowledge of
     the design. A protocol line can forbid it, but no check reads it from predictions, so it is a weaker fix than a
     design that removes it (remedy ladder: fix the definition before a note).
   - B also removes the gamer's flaw A (granite albite taught as gabbro anorthite).
   - B follows SPLIT-19 (Should) with no exception to record. The best honest model (H3) already trains on references
     only.
   - The split auditor measured an identical ranking of five models under A and B (tau 1.0), so B costs no
     information we used.
   - What B loses is the per-rock score and the second fold. With one test fold made of two rocks, SPLIT-14 says a
     B split into two folds sharing one training side is one evaluation anyway.
   - Accept `splits_dimensions_off_protocol` (1x1) with that reason.
   - Keep the LEAK-9 protocol line for the test-row averaging (#1 kNN, #4, #6). B does not block those.
   - groups_test_groups_few: cite the 4-13x noise, as the critic says.
   - If C2 drops the granite, B becomes reference -> gabbro, one fold.

C6 (LEAK-13). Already conceded in my point 5: one reading per band.

C7 (fill-down, copy, licence). Concede all three:
   - Mask the filled bands, with the mask count guarded, or repair from ODR if its file is clean.
   - sha256 of qtzalb_train_60s_3000, the 4084 file and the dusty-granite file, plus the file list.
   - Read the licence badge in the same session.
   The `license` field states what the source says. An ND licence would stop the dataset from shipping under the
   house rules.

Net: ship after changes.
- Changes needing no decision:
  - one reading per band;
  - the fill-down mask;
  - both side maps to training;
  - design B plus the LEAK-9 line;
  - the wording fixes.
- Before ship, one browser session: the paper's labelling method and sample list (C2, C3), sha256, licence.
- Then the SEL-12 run. Exclusion only if the CNN is clearly better, an ND licence holds, or both rocks' labels prove
  to be model output.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: raman_mlrod (2026-11-09)

Position: do not ship as defined. Ship only after changes 2-7 below and once point 1 is measured. Nothing here asks
for exclusion now: every Must at stake has a fix in the definition or a fact the curator can settle in a browser.

Judgment record
  Validity: SEL-12 open with strong evidence against (1); USE-5 concern, label construction differs by rock and may
    be a model's output (2); SPLIT-24/LEAK-17 open for aug_train_15s_1000 with the whole gabbro fold at stake (3);
    SPLIT-24/LEAK-17 triggered for two side maps (4); split design gameable to the oracle ceiling, SPLIT-19 departure
    not recorded, LEAK-9 no protocol line (5); LEAK-13 Must kept against a measured free fix (6); PROV-13 fabricated
    values shipped, PROV-1 copy unchecked (7).
  Value: TP-5/TP-8 hold; few groups weigh − heavily (noise 4-13x per-row SE), inside point 5.
  Quality: wording items (README citation, "no cosmic-ray removal", 1-2 readings per band, encodings sentence) are
    the auditors' and not counted here.

1. [P2, SEL-12 Must] The source's own spectrum model is far ahead, and the planned check cannot show it.
   - Problem: SEL-12 keeps vectorised spectra only where tabular models are competitive. The source's raw-spectrum
     CNN, trained on the reference maps only, scores accuracy 1.00 (macro F1 0.98) on the 19,980 clean slab spectra
     (Spec-CNN Notebook-CNN-Raw_Data.ipynb cell 12; precedent checker D1). EV-4 counts the source's own result.
   - Against it on our side: untuned RF 3.158 and LightGBM 2.906 log loss, worse than the dummy 2.766 (builder);
     LightGBM reference->slabs accuracy 0.707, 0.85 with row normalisation (blind reviewer); third-party RF/SVC
     69-71% vs CNN 78-80% (Sineesh and Kamsali, EV-4 orientation only).
   - Effect: if the gap holds tuned, the benchmark ranks tabular models on a task where the field's answer is a CNN.
   - Issue 1 misreads the sibling (bacteria_id_raman was judged keep, not pending) and its decisive run (tuned + TabPFN
     v3.5 on our folds) has no spectrum model to compare with.
   - Remedy: hold the ship decision on a run that compares like with like: Spec-CNN (code in the run folder)
     and tuned tabular/TabPFN v3.5 on the same split. Rewrite issue 1 with the source's 1.00. Exclusion only if the
     CNN is clearly better there.

2. [P3, USE-5 Must] The label means different things in the two rocks, and the granite's may be a model's output.
   - Gabbro: whole blocks, 6 and 4 runs per map, the substrate's mineral under dust. Granite: point by point, 3,691
     runs in the dusty map (1,688 one-point runs); code 15 is exactly what the source's dec_pred assigns below its
     threshold; 147 granite points are "Forsterite", which cannot occur with quartz in granite (basalt dust's
     olivine, 817/850 cm-1) (claim auditor I4 and item 2; domain practitioner F3; task gamer).
   - A dust detector trained on granite code 15 calls about 610 forsterite and 800 plagioclase points of the dusty
     gabbro dust; those keep the grain's label (claim auditor I4).
   - Effect: the two folds score different targets under dust; if the granite labels come from a thresholded
     classifier, a model that mimics it gains and the target is not a reading.
   - Remedy: curator reads the paper's methods (open access; 403 only to bots) before ship. If labelled by hand or
     by phase mapping: fit approximate with the two label semantics and the closed set named in fit_reason (USE-5
     allows this). If the source's CNN made them: the granite fold's target fails USE-5 and must be re-targeted or
     dropped.

3. [P4, SPLIT-24/LEAK-17 Must; EV-1] The gabbro's augite may be in training: "every test rock stays unseen" is not
   established.
   - aug_train_15s_1000 matches the gabbro augite at each map's own self level (SNV 0.972 vs 0.982/0.975; background
     1,121 vs 1,128 counts; the other augite map 0.66-0.82); adversarial AUC 0.91 where every other map/slab pair is
     0.99-1.00 (split auditor 1b; task gamer #2).
   - Stake: drop that map and gabbro augite accuracy 0.822 -> 0.002, fold-0 log loss 0.784 -> 2.551 (dummy 2.898);
     drop the 5x larger augite map instead: no change. Augite is 44% of fold 0. ms_train_015s_5900 vs granite
     muscovite shows the same pattern (AUC 0.92/0.88).
   - Effect: fold 0 may test a rock already measured in training; its honest score is then inflated by about 2.7.
   - Remedy: settle the fact before ship (sample list in the paper or ODR metadata; the authors). On yes, the map
     joins the gabbro's group (re-split). Similarity alone cannot set a group (SPLIT-24), so until settled the
     splits_comment must drop "every test rock stays unseen" and name the question and its stake.

4. [P4, SPLIT-24/LEAK-17 Must] Two "rock" test maps are lab material by the source's own ids: move them to training.
   - L_raw_gabbro0dust_test_015s_46_final: source row ids "gyp_foalb_test"; 16 gypsum + 30 Fo-alb mix, neither a
     gabbro mineral; gypsum matches gyp_train_12s_3320 at 0.999 against that map's self level 1.000.
   - L_raw_granite0dust_test_030s_1373_final: ids "hb_ms_test"; its 500 muscovite match ms_train_015s_5900 at 0.994,
     the self level (column auditor 1-2; split auditor 1a).
   - Effect: 546 test rows are specimens present in every training side; gypsum and Fo-alb in the gabbro fold come
     only from this map, so "gabbro holds 8 classes" is wrong (6).
   - Remedy: re-split. These maps are grouped on the source's own ids (exact, SPLIT-24 allows it): the 46-row map and
     the muscovite block go to every training side (their own group); the hornblende block may stay. Fix
     task_summary and the splits_test_class_missing text. Score effect small (logreg granite 1.079 -> 1.138).

5. [P4, SPLIT-19 Should, SPLIT-5 Must, LEAK-9 Should] Design A lets the split itself be gamed to the oracle ceiling.
   - With one rock per fold and the other rock in training, the training slab's minerals are nearly absent from the
     test rock. Scaling those classes by 0.02, with no test data, lowers the best honest model 0.666 -> 0.477 and the
     baseline 2.757 -> 1.988; adding a 50-neighbour average over test rows gives 0.431, equal to the ceiling of
     knowing the test rock's class set (task gamer #1, #3). A protocol line cannot block the first part: it reads only
     the split design.
   - Design A also hurts honest models: the one slab in training confounds "slab look" with its minerals (granite
     albite called anorthite; baseline 2.757 under A vs 2.410 trained on references only; H3, the best honest model,
     trains on references only). The builder's reason, "the other rock lowers log loss on both rocks", holds for
     logreg-SNV only (split auditor, claim auditor 34).
   - SPLIT-19 (Should) says follow the source's split, and the departure is not recorded as an exception.
   - Remedy: the source's design B: reference maps train, both slabs in one test fold (no class set to negate, no
     confound). Add the LEAK-9 protocol line that predictions are made row by row, without other test rows (as
     medical_facility_operational_data). If the curator keeps A, record the SPLIT-19 exception with the gamer's
     numbers, and the protocol line is needed either way. groups_test_groups_few must cite the noise: per-row SE
     understates a fold's noise 4-13x, only 4 of 10 model pairs separate on the gabbro's 12 blocks.

6. [P4, LEAK-13 Must] The class-linked grid texture is kept although a measured fix costs nothing.
   - The band minimum makes fine-grid maps lower and rougher; the grid kind follows the class in the reference maps
     (AUC 0.68). One reading per band (nearest the band centre) removes it (comb AUC 0.651 -> 0.536) and scores the
     shipped logreg at least as well (gabbro 1.451 -> 1.253, granite 0.485 -> 0.497) (claim auditor 38).
   - Draft issue 7's "no clean fix without smoothing" is refuted. LEAK-13 is a Must with no training-side scope; the
     keep rests on the source's grid (spectra.md under CLEAN-26, a P7 Should), which cannot outrank it
     (principles.md; precedent checker D8).
   - Remedy: harmonise with one reading per band (option b of C1). This also answers the source's own account that
     the band minimum is a cosmic-ray step.

7. [P5, PROV-13 Must, PROV-1; CLEAN-26] Fabricated values ship, and the copy is not checked against the origin.
   - qtzalb_train_60s_3000 row 2456 holds a spreadsheet fill-down: 346 readings, 581-858 cm-1, exactly k x 4.11843;
     277-293 shipped bands. The file carries Apple Numbers metadata; claim 6 ("whether a value changed is unknown")
     is refuted (claim auditor 6; column auditor 4).
   - The mirror is not the state the source's reader takes (dusty-granite CSV has no og-idx header); ODR id 63742
     missing; "500,000+" against 130,061 unexplained (claim auditor 4, 8).
   - Licence: AHED text says BY-NC, its badge links CC BY-NC-ND 4.0 (blind reviewer). A note only (EV-4), but the
     `license` field must state what the source says.
   - Remedy: mask the filled bands (as the two cut-short rows, with the mask count guarded), or repair from ODR's
     file if it is clean. Before ship, the curator's browser session: sha256 of 2-3 files including
     qtzalb_train_60s_3000 against odr.io/MLROD, the file list, and the licence badge.

What I do not argue: the grouped regime (SPLIT-29 holds), log loss (MET-5/6), the code-9 repair (PROV-13, mortgage),
the code-15 drop (force_2020's Basement), TP-8 for the short classes.

Rebuttal
========

New fact (measured for this rebuttal, from the split auditor's design-B predictions
with meta_rows.parquet; argmax accuracy, trained on the reference maps only, on the 19,980 clean slab spectra, the
exact test set of the source's CNN): logreg PCA100 0.934, logreg-SNV 0.906, LightGBM 0.865, RF 0.830, kNN 0.801.
Dusty slabs: 0.42-0.64. It bears on advocate point 6 and on my point 1.

A1 (task real, grouped by rock, few groups a weighed factor). Concede. I never contested the regime, TP-5 or TP-8.
   The blind reviewer's GroupKFold is not the shipped split. The noise belongs in the groups_test_groups_few reason.

A2 (gamer's exploits are evaluation leaks; A + protocol line or B). Concede the transductive part (#1 kNN, #4, #6):
   LEAK-9's protocol line is the rule's fix. Dispute that A + a line equals B:
   - Exploit #3 reads no test rows. It is a hand-set prior from the fold design (0.666 -> 0.477). LEAK-9 covers
     "a model can read other test rows"; a prior typed in from the design leaves no trace a benchmark can check.
     Only the design removes it.
   - Flaw A hurts honest models: baseline 2.757 under A against 2.410 trained on references only; the best honest
     model (H3) trains on references only.
   - SPLIT-19 (Should) defaults to the source's split. A departure needs a fact that sets the case apart; A's stated
     fact ("lowers log loss on both rocks") holds for SNV-LR only. Tau 1.0 shows A is not invalid. It does not
     supply the missing fact.
   - So B plus the protocol line. A only as a recorded SPLIT-19 exception, with exploit #3 written into it.

A3 (augite map; SPLIT-24 forbids a similarity group; one map per test class is normal here).
   - Concede SPLIT-24: I asked for no regroup on similarity (my point 3 says so). We agree on the note and on the
     browser check.
   - Dispute "normal". The calibration separates augite from the others. Albite and microcline match their slab
     below their own self level (albite 0.848/0.906 against 0.921/0.981; microcline 0.895/0.957 against
     0.940/0.977), about the gap between two albite maps of one apparent specimen. Augite matches at the self level
     (0.972 against 0.982/0.975), with background 1,121 against 1,128 counts (other augite map 1,193). Adversarial AUC
     is 0.91 against 0.99-1.00 for every other map/slab pair, muscovite excepted (split auditor 1b, task gamer #2).
     "Its class needs its map" is normal; "its map is indistinguishable from the test rock" is the outlier.
   - Where we differ: ship before or after the check. EV-1 (facts first) and SPLIT-1/LEAK-17 (Must): the fact is
     settleable in one browser session, and 44% of fold 0 rides on it (fold log loss 0.784 against 2.551). Gate the
     ship on it. If the source cannot say, keep with the note, as the advocate proposes.
   - Muscovite in hb_ms: dispute "keep". This is grouped on the source's own id "hb_ms_test", an exact id like
     "gyp_foalb_test" (SPLIT-24 allows it), not on similarity. Its hornblende is not the granite either (split
     auditor 1a). Treat like cases alike: move the muscovite block to training with the 46-row map. Concede that the
     hornblende block may stay.

A4 (labels: code 9 -> 8, code 15, dust asymmetry as an approximate note).
   - Concede the repair and the drop. I did not contest them.
   - Concede in part: USE-5 lets an undocumented construction ship as approximate with a note.
   - Dispute: USE-5 also says "a label checked and found to be another quantity still fails". The granite's 147
     "Forsterite" points are the dust's olivine (817/850 cm-1; olivine does not occur with quartz). There the label is
     what the spot shows, not the rock's mineral. The 86/89/60% readability is measured on the gabbro and does not
     address how the granite was labelled. If the source's thresholded CNN set the granite labels (code 15 is its
     dec_pred output), the target is a model's output. My remedy stays: read the paper's methods before shipping,
     approximate with a note if people set the labels.

A5 (fill-down masked; LEAK-13 fixed by one reading per band; wording). Concede: we agree on both fixes. One addition
   from PROV-13: check ODR's qtzalb_train_60s_3000 first and repair from it if it is clean; mask only otherwise.

A6 (SEL-12: untuned tabular already 0.80-0.85; SEL-15 leans keep).
   - Dispute the comparison. The 0.80/0.85 are over all slabs, dusty included, and 0.85 needs a crude baseline
     removal plus max normalisation, not the shipped encoding. The CNN's 1.00 is on the 19,980 clean spectra only.
   - Concede the substance on the like-for-like number. Measured above: untuned logreg reaches 0.934 on the same
     19,980, LightGBM 0.865. This is closer than my brief implied. A 6.6% error rate against 0% is still not
     "competitive" on its face. The untuned trees still sit below the dummy in the declared log loss.
   - Neither side can call "clearly better" yet. The remedy is the one we share: keep pending a run of Spec-CNN and
     tuned tabular / TabPFN v3.5 on the same split and metric (on design B that is the source's own test set). Cite
     0.934 against 1.00 in issue 1.
   - I withdraw nothing else of point 1, and I ask for no exclusion before that run.

A7 (provenance; licence). Concede: counts are independent of the mirror; one browser session settles sha256, the file
   list and the licence. Licence: EV-4 makes it a note, never a verdict reason. Fix the field after reading ODR. A
   house-rule question on ND is the curator's.

Net position after rebuttal: ship after changes, gated on three facts from the curator's browser session (the
granite's labelling method, the augite map's specimen, the ODR checksums) and on the SEL-12 run. Changes: design B with
the LEAK-9 protocol line (or A as a recorded SPLIT-19 exception), both side maps' lab material to training, one
reading per band, the filled row repaired or masked, the notes (closed set, label semantics by rock, the augite
question).
```

</details>
