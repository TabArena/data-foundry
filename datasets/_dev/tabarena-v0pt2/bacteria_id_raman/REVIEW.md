# bacteria_id_raman

**Outcome:** added. The AI recommends shipping it. The task is the source's own clinical task (Ho et al. 2019, Nature
Communications): from the Raman spectra of a new patient's bacterial isolate, which of the source's eight empiric
antibiotic groups does it call for? 50 patients (25 from Palo Alto 2018 with 400 spectra each, 25 from Stanford 2019
with 100 each) carry five of the groups, 10 patients each; whole patients are held out, and the 66,000 spectra of the
30 reference isolates train in every split and are never tested, as the source pre-trains on them. The spectrum
(1,000 positions) is the only input; fallback `log_loss`. The panel's three calls are implemented as recommended and
wait for your mark: one prediction per patient from its spectra (issue 1), 2 folds x 30 repeats so a test fold holds 5
patients per group (issue 2), and the 5 library-only reference isolates kept with a note (issue 3). The changes that
needed no decision are made: four fit gaps named (the Gram stain, MALDI-TOF or PCR at this culture stage, a fixed drug
per species, the pooled years), six wording repairs, a near-copy note on the look-alike pair 2018-24/21
(piperacillin-tazobactam; the claim audit called it daptomycin), the patients numbered at random, a protocol line
against reading other test patients or the fold's make-up, and the library note. The panel counted 6 library-only
isolates and 13,200 rows; the label files hold 5 and 11,000, and the file uses 5. Two changes nobody asked for, so you
can object: the weight columns `isolate_weight` and `unit_weight` are removed. Under one prediction per patient, the
scorer reads a weight at each patient's first row, so a 2019 patient would count four times a 2018 patient. The schema
also refuses a unit weight that the metric does not use. The mediator asked to keep `unit_weight`, but it cannot stay.
Verdict: ship after changes (made).
Validity: a real clinical decision the source names, with an approximate fit, now with its four gaps named; the target
is the treatment group of a new patient's isolate, not the 30 lab strains[^v1]. No leak in the data: the spectrum is the
only input, processed one row at a time, with no exact copies in 78,500 rows. Patients are held out whole, and each
patient's rows come from the source's row blocks (the block offset fits in 10 of 10 checks); the look-alike pair is kept
with a note[^v2]. One prediction is now one patient, as the source identifies a patient (issue 1). Two ways to read other
test rows (a neighbour rebuild, the fold's make-up by year) are closed by that unit and a protocol line; the patient ids
were renumbered so they no longer follow the label[^v3].
Value: 3-4 patients per group per test fold was below the size rule's 5, now 5 with 2 folds (issue 2)[^v4]. The final
task probe at the shipped design (2 folds, one prediction per patient) had not finished when this file was written. In
its place, the builder's probe on the first draft (one prediction per spectrum, 5 of 60 3-fold splits): LightGBM best,
skill +0.807 (SE 0.023) over the class shares on 5 of 5 splits. At the declared unit, three untuned models score 0.120
to 0.251 per patient, against 1.975 for the class shares, on 20 of 60 splits. The group probe is too coarse to add to
this: its row cap of 20,000 keeps 18 patients, and with 10 permutations its smallest possible p is 0.091. The source
reports accuracy only, with no costs, so the fallback log loss holds; one prediction per patient counts each patient
once without a weight[^v5].
Quality: the spectrum ships as published, declared `processed`.
Weighed: source + (Nature Communications, the authors' repository; the source's own clinical task), gap + (spectra,
multiclass), size - (50 patients), fit - (five species from cultured colonies, MALDI-TOF the routine comparator).
For the curator: issues 1-3, each implemented as recommended; issue 4, three check warnings to accept with the texts
proposed there. `groups_test_groups_few` no longer fires (25 patients per fold).

[^v1]: SEL holds; **USE-1** holds, fit approximate; **USE-5** decided the target; **USE-8** met once the four gaps were named.
[^v2]: **SPLIT-4** and **SPLIT-29** hold; **SPLIT-24** holds (offset 0 best in 10 of 10 file-and-group pairs); **SPLIT-30**: the pair kept with a note.
[^v3]: **SPLIT-23** triggered and fixed; **LEAK-9** triggered twice, closed by the unit and a protocol line; **LEAK-33** holds, the ids renumbered as hardening.
[^v4]: **TP-5** triggered, fixed by 2 folds; TP-1 to TP-3 hold on the builder's probe.
[^v5]: **MET-6** and **MET-8**: the fallback log loss; **MET-17** met by the patient unit; **CLEAN-26** holds.

**Main points:** Issues 1-3 are implemented as recommended and wait for your mark; issue 4 is a yes/no on three warning
texts.

**Record judgment:** valid. The record's fields agree with the definition. Two screening statements no longer hold and
the notes say why: the size check's priority 3 assumed the large 30-isolate framing (the task is the 50-patient one),
and the covertype precedent the screening cites for keeping a paper's accuracy is stale (covertype went to the fallback
log loss on 2026-10-21). Priority 4 becomes 3 (the fit is approximate).

**Issues for Lennart:**

1. **One prediction per patient, from all of its spectra, as now, or one per spectrum?**

   * **Problem:**
     - The source identifies a patient's treatment group by a majority vote over 10 of that patient's spectra, and the lab has all 100 to 400 of them[^u23].
     - The first draft made each spectrum one prediction from that spectrum alone, with a weight so each patient counted once; its reason was that per patient the score saturates, which holds for accuracy (0.96-1.00) but not for log loss (0.10-0.22 per patient).
     - The definition now scores one prediction per patient, the mean of its spectra's class probabilities, and a model may use all of the patient's spectra.
   * **Effect on the task:**
     - The unit reorders the models: between the per-spectrum score and the per-patient one, four untuned models rank at Kendall tau 0.48 on average (lowest -0.33), and the best model differs on 36 of 60 splits.
     - A logistic regression with C=1 beats one with C=0.01 per patient on 59 of 60 splits, per spectrum on 17 of 60.
     - Per spectrum, a participant who averages each test spectrum with its nearest test spectra (mostly the same patient's) lowers the loss by 32% on 60 of 60 splits; per patient, that trick gains no more than sharpening each spectrum's prediction on its own.
   * **Experiments:** (3-fold splits of the first draft, untuned models, probe numbers)

     | Unit | PCA-100 logistic | Logistic C=0.01 | kNN on PCA-30 |
     |---|---|---|---|
     | Per spectrum, each patient weighted once (first draft) | 0.228 | 0.214 | 0.585 |
     | Per patient, mean of 10 spectra (the source's 10) | 0.104 | 0.128 | 0.220 |
     | Per patient, mean of all its spectra (implemented) | 0.100 | 0.124 | 0.213 |

     - The source's own score, a vote over 10 spectra, ties on 241 of 360 model pairs, and all four models are perfect on 27 of 60 splits; on the 119 pairs it separates, the per-spectrum score agrees with it 107 times, the per-patient mean 88 times and a per-patient mean of log probabilities 97 times.
   * **Consistency:** the context follows the use case, not the gain, as you set for huesken_sirna_efficacy and the protein task; musk and fraud_detection_in_electricity_and_gas_consumption_1m score one prediction per group from all its rows. micro_mass, pancreatic_cancer_mouse_detection and raman_mlrod predict per row, but there the source's prediction is one spectrum or one sample[^u23c].
   * **Panel:**
     - One patient (critic, claim auditor, mediator): the cited protocol is one identification per patient from several of its spectra, so the rule decides it; the advocate's ranking numbers are a score argument, which cannot decide what one prediction is.
     - One spectrum (advocate; the precedent checker before the claim audit): the per-spectrum score orders the models as the source's vote does on the coarse pairs, and the culture-free aim of few spectra has one spectrum as its limit; the mediator found no statement of the source that a decision is made from one spectrum.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One spectrum | each spectrum one prediction from itself alone; each patient weighted once; a protocol line bars the patient's other spectra; a new reason in the grouping | 50 times more scored predictions; orders the coarse model pairs as the source's vote does | not the source's prediction; bars the spectra the lab has; needs a reason the source does not give; the patient trick stays a live exploit |
     | B | One patient, from all its spectra (implemented) | one prediction per patient, the mean of its spectra's probabilities; all of its spectra usable; no weight | the source's unit; the lab's information; each patient counts once without a weight; closes the neighbour trick | 25 scored predictions per fold; the mean favours models sharp per spectrum, so a method may return its own patient prediction |

   * **Recommendation:** B: the source's cited protocol identifies a patient from its spectra, and nothing in the source makes one spectrum the decision. **Decision:** A or B?

   **Notes for the AI:** A: `Grouping(prediction_unit="row", context="none")`; restore the scoring column `isolate_weight` (1 over the isolate's spectra), `Metric.fallback(..., inputs={"weight": "isolate_weight"})` and `UnitWeight(column="isolate_weight", unit="isolate")`; add to splits_comment's protocol line "each spectrum is predicted from itself and the training rows only, never from the patient's other spectra"; write the use-case reason for one spectrum into `grouping.definition`; rewrite `task_summary` (question, known, split, changes) and the unit bullet of curation_comments; re-run `dataset check` and the task probe. The mediator asked to keep `unit_weight` under B; the schema refuses a unit weight that is not the metric's weight input, and the weight input would be read at each patient's first row (a 2019 patient would count four times a 2018 patient), so B has none.

   [^u23]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is and what a model may know about the group. Ho et al. 2019, Results: "We then use 10 randomly sampled spectra from each patient isolate in the test set ... The most common class out of the 10 spectral classifications is then chosen as the identification." principles.md, Tensions, "The right split against the score": a score argument does not decide a rule ranked above it.
   [^u23c]: SPLIT-23 Cases: huesken_sirna_efficacy and the protein task, "the context follows the use case, not the gain" (Lennart, 2026-11-05); musk (group, any, all_rows); fraud_detection_in_electricity_and_gas_consumption_1m (group, mean, all_rows). **MET-17** (Should): the weight changes how much a prediction counts, never what one prediction is.

2. **Two folds of 25 patients, as now, or three folds with a written amendment of the size rule?**

   * **Problem:**
     - There are 10 patients per treatment group; three folds put 3 or 4 of each group in a test fold (16 or 17 patients), below the 5 the probe asks for[^t5].
     - Two folds x 30 repeats put 5 of each group in a test fold (25 patients) and clear both checks; training keeps 5 patients per group plus the library.
     - Keeping three folds needs your rule to say that 3 or 4 units per class with stable scores is more than a handful, a change that holds for every dataset.
   * **Effect on the task:**
     - With two folds one patient carries 13% to 34% of a fold's loss, and the patient-bootstrap standard error of one fold's score is 0.032 on a mean of 0.120 (logistic regression on 100 principal components, first 20 shipped splits).
     - With three folds one patient carried 16-51% of a fold's loss, and the patient-bootstrap standard error was 0.050 on 0.242 per spectrum, 18 times the standard error across repeats; gaps below about 0.03-0.05 do not carry to new patients.
     - The source's own leave-one-patient-out fine-tuning trains on 4 patients per group.
   * **Experiments:** the final task probe on 2 folds had not finished; the first draft's task probe (3 folds, per spectrum) gave LightGBM a skill of 0.77 to 0.84 on each of 5 probed splits. On the first 20 shipped 2-fold splits a logistic regression on 100 principal components scores 0.076 to 0.324 per patient per fold (mean 0.120), and C=1 beats C=0.01 on 19 of 20; the group probe is too coarse to add to this: its row cap of 20,000 keeps 18 patients, and with 10 permutations its smallest possible p is 0.091, so it cannot show significance at 0.05. The first draft's probe in full: LightGBM 0.401 against 1.959 for the class shares (linear 0.693, random forest 1.089), LightGBM ahead of the random forest by 0.349 (paired SE 0.009).
   * **Consistency:** parkinsons was retired at 2 or 3 healthy people per fold (10-11 per fold, unstable scores); micro_mass and sarcoma were kept at 3 or 4 units of a class per fold inside large folds; musk at 13 per fold. Two folds follow the rules as written[^t5c].
   * **Panel:** the advocate argued for three folds (stable skill 0.77-0.84 on 5 of 5 probed splits, no short class, 16-17 patients per fold against parkinsons' 10-11) and accepts two as the fallback; the critic and the precedent checker ask for two (3-4 is below the probe's 5, a Must takes no exception); nobody asks for Too Small.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 2 folds x 30 repeats (implemented) | 25 test patients per fold, 5 per group | meets the probe's 5 without a rule change; both checks clear; both sides accept it | 25 training patients instead of 33-34; 5 per group is still few |
     | B | 3 folds x 20 repeats, with the size-rule amendment[^t5] | 16-17 test patients per fold, 3-4 per group; the line goes into the size rule for every dataset (text in Notes for the AI) | more training patients; the protocol's dimensions | changes how a Must reads for all datasets; 3-4 is below the probe's threshold |
     | C | Too Small | retired with the `Too Small` marker | the strictest reading | drops the source's real task with stable scores; nobody asks for it |

   * **Recommendation:** A: the mildest remedy that follows the rule as written. **Decision:** A, B or C?

   **Notes for the AI:** B: in `_make_splits`, `n_repeats, n_folds = protocol.recommended_dimensions(clinical, group_on="isolate", group_labels="per_group")` (3 x 20); rewrite splits_comment, `task_summary.split` and the few-patients bullet; propose `groups_test_groups_few` for acceptance; add the amendment to the across-datasets REVIEW.md (text below) and, once you agree, to TP-5. Amendment text: "TP-5 amendment (proposed, bacteria_id_raman): a class at 3 or more units per test fold is not a handful when no class is short, a test fold holds 15 or more units, and the score is stable across splits (best family's skill within a narrow band on every probed split); below that, fewer and larger folds first, then Too Small." C: `suggestion` `No`, marker `Too Small`. Re-run `dataset check` and the task probe on B.

   [^t5]: **TP-5** (Must): `Too Small` means a handful of units of a class, per test fold and in total, counted in the unit the task is scored on. evidence.md: the `few_minority` flag fires below 5 units of a class per test fold. principles.md, How to decide 4: a very real task with a handful of units per class per test fold is still `Too Small`. definitions.md: accept `groups_test_groups_few` only with real signal and more than a handful of groups of each class per fold.
   [^t5c]: task_probes.md Cases: parkinsons_biomedical_voice_measurements retired 2026-10-05; musk kept 2026-10-06; micro_mass, sarcoma and ljubljana_primary_tumor kept 2026-10-12 (Lennart). The remedy ladder fixes the definition before it changes a rule.

3. **Keep the 5 reference isolates of the three library-only groups, with a note, as now, or drop them?**

   * **Problem:**
     - Ciprofloxacin, ceftriaxone and caspofungin occur only in 5 reference isolates (two Candida strains, one Salmonella and two pneumococci; 11,000 spectra), which are never tested, so a model's probability on these groups is always penalised and never rewarded.
     - The source pre-trains on all eight groups, and a lab's library holds such species[^t6].
     - Dropping them makes training and test hold the same five groups and clears one check warning.
   * **Effect on the task:** renormalising each spectrum's probabilities over the five patient groups, an upper bound for the drop without a refit, lowers the per-patient loss by 19% (logistic regression on 100 principal components, 0.120 to 0.097), 18% (C=0.01) and 10% (kNN) on the first 20 shipped splits; the three models keep their order on 20 of 20 splits, so it is mostly a level shift.
   * **Experiments:**
     - A refit without them (column auditor, per spectrum, first draft): -0.007 to -0.049; the panel counted 6 isolates and 13,200 rows, the label files hold 5 and 11,000.
     - The spectrum tells the library from the patients at ROC AUC 0.932 within the shared groups too, so it marks the subset, not a class.
   * **Consistency:** raman_mlrod (this batch) trains on its reference library in every fold and never tests it, as its source does; no definition has dropped a source's training-only classes.
   * **Panel:** keep (advocate, mediator): the source's version, and dropping is a fix of our own that only removes a level; drop (critic): the test never rewards that mass, and "which of five" then holds on both sides. Both keep the library itself.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, with the library note (implemented) | all 30 reference isolates train in every split | the source's 8-group pre-training; what a lab's library holds; no filter of our own | a level of the score is the open-set cost of three groups never tested; one check warning to accept |
     | B | Drop the 5 isolates | 11,000 rows leave; training and test hold the same five groups | the score holds only the tested groups; the check warning clears | a filter of our own; the source's version changes; mostly a level shift |

   * **Recommendation:** A: the source pre-trains on all eight groups, and dropping them mostly shifts the level. **Decision:** A or B?

   **Notes for the AI:** B: in `_clean`, drop the reference rows whose group is ciprofloxacin, ceftriaxone or caspofungin (`REFERENCE_ISOLATES` 0, 1, 19, 23 and 24: groups 7, 1 and 4); update the row counts in `task_summary.row`, the library bullet and splits_comment; drop the `splits_test_class_missing` acceptance; re-run `dataset check` and the task probe. Either way, the across-datasets item on a reference library that trains and is never tested gets one Cases row with raman_mlrod.

   [^t6]: **TP-6** (Must): a valid task stays, and a version of our own is no better version of the source's task. **LEAK-14** (Must) is not triggered: its mechanism, a tested class recognised by its source, is absent, as no spectrum of the three groups is ever scored.

4. **Accept the 3 warnings with these texts?**

   * **Problem:**
     - `dataset check` gives 0 errors and 3 warnings, each a consequence of the design: the library never tested, three groups no test fold holds, and 2 folds instead of the protocol's 3[^w1].
     - The texts are not in `dataset.py` yet; row A is what ships on your yes.
   * **Effect on the task:** none on the data or the score; the warnings stop showing as open findings.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept the 3 | the three texts in the notes below, written into `dataset.py` on yes | the design reasons recorded next to the warnings | none found |
     | B | Leave them unaccepted (implemented) | the warnings stay open | none found | the bundle shows 3 open warnings |

   * **Recommendation:** A, if you settle issues 2 and 3 as recommended; a change there changes the texts. **Decision:** accept the 3 warnings with these texts, yes or no?

   **Notes for the AI:** on yes, add to `dataset.py` `accepted_check_warnings = {"splits_rows_never_tested": "By design: the 66,000 spectra of the 30 reference isolates train in every split and are never tested, as the source pre-trains its clinical model on them; the test units are the 50 patients (splits_comment).", "splits_test_class_missing": "By design: ciprofloxacin, ceftriaxone and caspofungin occur only in 5 reference isolates, which are never tested; every test fold holds all five patient groups, 5 patients each. The class-share dummy pays for the library's prior (1.975 against ln 5 = 1.609; curation_comments).", "splits_dimensions_off_protocol": "2 x 30 instead of the protocol's 3 x 20, so that a test fold holds 5 patients of each treatment group (TP-5; 3 folds left 3 or 4; splits_comment)."}`; re-run `dataset check`. The 1.975 is curation_comments' number on the shipped 2-fold splits; the mediator's 1.953 was the first draft's 3-fold splits. Drop the `splits_test_class_missing` text if issue 3 goes to B, and the `splits_dimensions_off_protocol` text if issue 2 goes to B.

   [^w1]: definitions.md, the check table: a warning that is correct for the dataset is accepted with its reason; the curator fills `accepted_check_warnings`. The two library warnings would be the first by-design acceptances of their kind, alike for raman_mlrod.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. The
panel worked on the first draft: one prediction per spectrum with a per-patient weight, grouped 3-fold x 20 repeats
(16 or 17 test patients per fold, 3 or 4 per group), the patients numbered in file order. The final definition scores
one prediction per patient (the mean of its spectra), drops the weight, uses 2 folds x 30 repeats and numbers the
patients at random, so the reports' patient ids are the old ones: 2018-22/23 is now 2018-24/21, 2018-16 is now 2018-07,
2019-20 is now 2019-02, 2018-25 is now 2018-11, 2019-21 is unchanged. The claim audit names the look-alike pair
2018-22/23 as daptomycin; the label files put it in piperacillin-tazobactam, as the mediator says. Claim audit: 32
claims and 5 implied, most hold; refuted: the per-spectrum unit's reason (per patient the log loss does not saturate),
the attribution of 74.0% against 93.1% to the culture (mostly the measurement session), the 45 x 45 map for the
patients, and the wording of the source's 2019 protocol; now fixed. Column audit: the spectrum is the only input and is
processed per row; the source's 25-spectra filter, the block order and the crop guess fixed in the notes; the patient
ids followed the label blocks (now random). Split audit: grouping by patient is right; a split over spectra lowers the
loss by 26-69%; the noise from the sample of patients is 18 times the noise across repeats. Domain practitioner: fit approximate; four gaps unnamed
(Gram stain, MALDI-TOF or PCR, a fixed drug per species, pooled years), now in the notes. Blind review: include with changes; its split
concerns came from a split of its own over the reference isolates, and its preferred fix is the shipped design (whole
patients held out, the library in training). Task gamer: a neighbour rebuild from other
test rows (-32% per spectrum) and the per-year make-up of a test fold (-0.014 and -0.033 per patient), both now barred
by a protocol line. Precedent check: framing, library, metric and spectrum consistent; 3-4 patients per class per fold
needs 2 folds or an amendment; MET-6's covertype line is stale. Debate, one rebuttal each: the advocate kept one prediction per spectrum after the rebuttal, and the mediator settled
it by the rule, since no statement of the source makes one spectrum the decision; the advocate accepted 2 folds as the
fallback and the critic held to 2 folds; both kept the library in training and disagreed only on the 5 library-only
isolates (issue 3; the reports say 6 isolates and 13,200 rows, the label files hold 5 and 11,000); agreed: the framing,
the notes and the protocol line.

<details><summary>bacteria_id_raman: mediator</summary>

bacteria_id_raman: mediator report (mediator, 2026-11-09)

Tier: full (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent checker;
advocate and critic with one rebuttal each). Read: principles.md (df-large), dataset.py, README.md, the record,
builder_report.md, the seven phase-A reports, both briefs and both rebuttals.
My checks: a re-count of the advocate's unit_ranking.csv, and renorm_unit.py (.log) on the
split auditor's stored predictions (4 untuned models, all 60 shipped splits). Probe numbers, not leaderboard numbers
(EV-8).

**1. RECOMMENDATION**

Verdict: ship after changes.
Validity: SEL holds. USE-1 holds, fit approximate. USE-5 decided the target: the treatment group of a new patient's
  isolate, not the 30 lab strains. USE-8 is met once four gaps are named (change 1). No leak in the data: the spectrum
  is the only feature, it is processed one row at a time, and there are 0 exact copies in 78,500 rows. SPLIT-4 and
  SPLIT-29 hold (whole patients held out). SPLIT-24 holds (row blocks; offset 0 is best in 10 of 10 file-and-group
  pairs). SPLIT-30: the TZP pair 2018-22/23 is kept with a note. SPLIT-23 triggered: the source identifies each
  patient from its spectra, so one prediction is one patient (issue 1). LEAK-9 triggered twice (the gamer's
  neighbour rebuild and the fold make-up per year): fixed by the unit and a protocol line. LEAK-33 holds; the ids are
  renumbered as cheap hardening.
Value: TP-5 triggered: 3-4 patients per class per test fold, below the probe's 5. Fixed by 2 folds (issue 2). TP-3:
  the model families spread at both units. MET-6 and MET-8: the fallback log loss holds. MET-17: met by the patient
  unit, with the weight input removed.
Quality: CLEAN-26 holds; writing repairs (change 2).
Weighed: source + (Nat Commun; the source's own clinical task), gap + (spectra, multiclass), size - (50 patients),
  fit - (five species from cultured colonies).
For the curator:
  - issue 1: the unit. SPLIT-23 settles it as one patient; please confirm.
  - issue 2: 2 folds, or keep 3 folds and amend TP-5.
  - issue 3: the 6 library-only isolates, kept with a note or dropped. A weighing call; I recommend keep.

**2. AGREED FACTS**

The task and the data:
- The task is the source's clinical task (USE-5, SPLIT-4, SPLIT-29):
  - the target: "Each patient is classified into one of 8 treatment classes" (Fig. 4);
  - the split: patients are held out whole (the notebook: "spectra from the same patient do not appear in both");
  - the library: the source pre-trains on it for the eight groups (Methods).
- The rows and labels hold:
  - all 78,500 rows match the source arrays (blind reviewer);
  - the labels match config.py on 30 of 30 isolates;
  - no reference row is in any of the 60 test folds.
- The patient blocks hold:
  - the nearest-centroid accuracy is highest at offset 0 in 10 of 10 file-and-group pairs;
  - the correlation between adjacent rows drops at the block edges in 10 of 10.

Leaks and look-alike patients:
- There is no leak in the data. The format exploit is within noise (+0.001 and -0.003, against a noise band of
  +-0.012).
- The patients 2018-22/23 (TZP) are a look-alike pair:
  - each one's log loss drops by 0.21 and 0.14 when the other trains;
  - that is about 0.007 of 0.242 on the mean;
  - the other look-alike pairs fall inside the band of ordinary pairs.
  The pair gets a note and no re-split (SPLIT-24 bars grouping on similarity; SPLIT-30).
- The patient ids follow the label blocks. They are renumbered at random.

The metric and the unit:
- The metric is the fallback log loss: the source reports accuracy only, with no costs or threshold (MET-6, MET-8).
  Draft issue 4's covertype citation is stale (covertype went to the fallback on 2026-10-21).
- The builder's saturation reason for the row unit is withdrawn. Per patient, the log loss is 0.10-0.22 and not
  saturated; only accuracy saturates. A P6 reason cannot decide a P4 Must.
- Measured, and accepted by both sides:
  - Kendall tau between the declared score and the patient-mean score: 0.48 (lowest -0.33);
  - the best model differs between those two on 36 of 60 splits;
  - LR C=0.01 with its rows squared (t=2) beats LR C=1 at the patient mean on 52 of 60 splits;
  - at the patient unit, the neighbour rebuild gains no more than sharpening each row on its own.
- In both forms of the unit, a LEAK-9 protocol line bars other test patients' rows and the fold's make-up.
- Under the group unit:
  - the context is all_rows;
  - the weight input goes: metrics._aggregate reads the inputs at each group's first row, so a 2019 patient would
    count 4 times a 2018 patient (tau 0.89, lowest 0.33, with the weight against without);
  - unit_weight stays.
- fit_reason and the notes name four gaps:
  - the Gram stain: 45-52% of the errors cross the Gram line;
  - MALDI-TOF or PCR, which give the species at this culture stage;
  - a fixed drug per species: resistance plays no part, and the paper's MRSA/MSSA accuracy is 65.4%;
  - the pooled years: the forward test gives 0.368 against 0.229 pooled.

Few patients and the library:
- The counts:
  - 10 patients per class, 3-4 per class in every test fold, 16-17 per fold;
  - one patient carries 16-51% of a fold's loss;
  - the patient-bootstrap SE is 0.050 on 0.242, 18 times the SE across repeats;
  - gaps below about 0.03-0.05 do not generalise.
  Both sides accept 2 folds as the fallback, and neither asks for Too Small.
- The reference library stays in training (the source's pre-training; raman_mlrod has the same design).

Set aside:
- The blind reviewer's split concerns 1-2 came from its own split over the reference isolates. Its preferred fix is
  the shipped design.
- A year column and a year-wise split are not wanted.

**3. CHANGES TO MAKE NOW (no decision needed)**

C1. USE-8 (Must). Add the four gaps, with their numbers, to fit_reason and curation_comments:
    - the Gram stain;
    - the MALDI-TOF or PCR comparator at the culture stage;
    - a fixed drug per species;
    - the pooled years.
    The fit stays approximate.
C2. writing.md and EV-2, the repairs:
    a. The 74.0% against 93.1% sentence (curation_comments, draft issue 1, claims.md 21). Most of that gap is the file
       or session: 92.6% within the reference file, against 45.2% and 43.6% on the 2 s files of the same strains. A
       new culture costs about 5-14 points (77.5 against 72.1; 90.6 against 76.5).
    b. "A 45 x 45 map" holds for the reference isolates only. Say the patients' map size is not stated (the 2018 rows
       repeat at a lag of 20).
    c. splits_comment: the source tests the 2019 patients in their own one-per-group loop, after fine-tuning on the
       other 2019 patients, with 10 spectra per training patient.
    d. The CLINICAL_FILES comment: the blocks run 0, 6, 5, 3, 2 in 2018 and 0, 5, 6, 3, 2 in 2019, not in code order.
    e. The anomaly bullet: drop "before a crop" (the minima sit at inner positions).
    f. Add the source's row filter: the 25 highest-intensity spectra of each map were discarded.
    g. Add the presumed species of the five patient groups from config.py's comments, marked as inferred.
    h. Optional: say the grid is uneven (1.20-1.56 cm-1).
    i. In the measurement-settings bullet, add that the year can be read from the spectrum at ROC AUC 0.994. A batch
       by class within a year would be read just as easily, and it cannot be tested without dates.
C3. SPLIT-30 and SPLIT-24: a "Potential near-copy, kept on purpose" note naming 2018-22/23 (TZP), with its numbers.
C4. LEAK-33: number the patients in a seeded random order within each year.
C5. LEAK-9 (Should): a protocol line. A test patient is predicted from its own spectra and the training rows only:
    - no rows of other test patients;
    - no preprocessing fitted on test rows;
    - no class counts of the test fold from outside the training data.
    Document exploit 2 and its gain beside the line (section 5).
C6. MET-1: the metric's reason records that the notebook's early stopping selects models on validation accuracy.
C7. The check acceptances (definitions.md, check table):
    - splits_rows_never_tested: by design.
    - splits_test_class_missing: the three groups only the library holds are never tested. Cite this as its own
      fact, not as TP-8's force_2020 reading.
    - In the notes:
      - the class-share dummy pays 0.34 nats for the library's prior (1.953 against ln 5 = 1.609), so the skill
        against ln 5 is about 0.75;
      - the patient-bootstrap SE and the concentration numbers;
      - "the splits recombine the same 50 patients".
    - groups_test_groups_few follows issue 2: 2 folds clear it (25 patients per fold, at least the 20 the check
      asks for).
C8. A library note, whatever issue 3 decides:
    - the library's class shares and its three never-tested groups are part of what the log loss scores: 16-19% of
      a linear model's loss at either unit (section 4, issue 3);
    - its gain over training on the patients only rests on two vancomycin patients (2018-16, 2019-20).
C9. Knowledge files, outside this folder:
    - flag MET-6's covertype case as stale;
    - after the curator's call, add one Cases row with raman_mlrod: a reference library that trains in every fold
      and is never tested, as the source trains on it.
C10. After issues 1 and 2:
    - re-run the task probe and the library comparison at the declared unit and fold count;
    - update the notes' numbers (the notes must match the code).

**4. CHANGES THAT NEED THE CURATOR: THE DISPUTED POINTS, RANKED**

ISSUE 1. The prediction unit (P4; SPLIT-23, Must). Settled by rank as (b), one patient. Please confirm.

Problem. The grouping makes each spectrum one prediction, from that spectrum alone (prediction_unit="row",
context="none"). The source identifies a patient from its spectra.

Effect.
- The unit reorders the models: tau 0.48 between the declared and the patient score, and the best model differs on
  36 of 60 splits.
- The row unit leaves a live exploit (-32%, 60 of 60 splits). Part of the information it uses is the lab's own: the
  patient's other spectra.

Each side's best evidence.
(a) One spectrum (advocate):
- The declared score orders the 4 models as the source's 10-spectrum vote does: per-split tau 0.62, against 0.37 for
  the patient mean.
- The C=1 against C=0.01 flip is sharpness, not knowledge.
- Under all_rows the order turns on each method's pooling (tau 0.57 between mean and log-prob pooling).
My re-count of that evidence (unit_ranking.csv):
- The vote ties on 241 of 360 model pairs, and all four models are perfect on 27 of 60 splits. So both taus rest on
  32 splits.
- On the 119 pairs the vote separates:
  - the declared score agrees with the vote 107 times;
  - the patient arithmetic mean agrees 88 times;
  - log-prob pooling per patient agrees 97 times.
- The contested pair, LR C=1 against C=0.01, ties on 54 of 60 splits, so the vote cannot referee it.
- The advocate's fact holds, but only on the coarse pairs: library against patients-only, and LR against kNN.
(b) One patient (critic):
- The source's prediction is per patient: "We then use 10 randomly sampled spectra from each patient isolate ... The
  most common class out of the 10 spectral classifications is then chosen as the identification" (Results).
- The lab has the patient's own 100-400 spectra. The advocate agrees.
- SPLIT-23 also decides what is known about a new group.
- Under the row unit, the neighbour rebuild gains -0.049 (LR-PCA) and -0.125 (LightGBM).
- At the patient unit with all_rows, an allowed pooling over the patient's own spectra scores 0.037 and 0.179. That
  beats the neighbour trick (0.069 and 0.222).

Rule and settlement.
- SPLIT-23 (Must, P4) names what decides: "the source's use case, cited". The cited protocol is one identification
  per patient from several of that patient's spectra.
- The reading "the culture-free aim has one spectrum as its limit" (the precedent checker's C2) is our inference, the
  lowest rank of evidence (EV-2). The source chose 10 spectra and calls 10 "not many".
- The advocate's numbers are about how the scores rank, a P6 matter. They cannot decide a P4 Must (Tensions, "The
  right split against the score"; SPLIT-23 Cases, huesken: "the context follows the use case, not the gain").
- Form (a) also fails SPLIT-23's second clause. Context "none", and its protocol line, would bar the patient's own
  spectra, which the source's actor uses.
- So this is not a weighing call: (b). The ladder's remedy is to fix the definition.

The change under (b):
- Grouping(prediction_unit="group", aggregation="mean", context="all_rows").
- Remove inputs={"weight": "isolate_weight"}, and the scoring column's use by the log loss if the API requires it.
  Keep unit_weight.
- Rewrite grouping.definition and task_summary (question, split: one identification per patient from its spectra),
  and the metric reason (each patient counts once by the unit).
- Notes:
  - the source votes over 10 spectra, while all_rows gives all 100-400; 10 against all differ by 0.004 (claim
    auditor);
  - the ranking depends on how each method pools its rows, and the scorer's default mean rewards sharp row models, so
    a method should return its own patient prediction (the schema allows it; the harness decides).

What would settle it the other way: a statement of the source's that its clinical decision is made from a single
spectrum. None was found.

ISSUE 2. Few patients (P6; TP-5, Must). Recommend 2 folds; 3 folds needs an amendment.

Problem. There are 10 patients per class: 3 or 4 per class in every test fold, counted in the scored unit, and 16-17
per fold. Two checks fire:
- few_minority, below 5 units of a class per fold (evidence.md);
- groups_test_groups_few, below 20 groups per fold.

Effect.
- One patient carries 16-51% of a fold's loss.
- The patient-bootstrap SE is 0.050 on 0.242.
- LR C=1 against C=0.01 is not resolved ([-0.009, +0.051]).

Each side's best evidence.
- Keep 3 folds (advocate):
  - the scores are stable: skill 0.77-0.84 on 5 of 5 probed splits, and the real fit beats all 60 permuted fits;
  - no class is short;
  - 16-17 patients per fold, against parkinsons' 10-11;
  - micro_mass was kept at 3-4 strains of a typical species per fold.
- 2 folds (critic):
  - 3-4 is below the probe's 5;
  - "How to decide" 4 bars strong signal as a rescue;
  - parkinsons was retired at 2-3 per fold;
  - micro_mass and sarcoma had large folds;
  - a Must takes no exception.

Rule.
- TP-5 does not put a number on "a handful". The only written number is the probe's 5.
- TP-8 is not triggered: no class is short, and a fold holds more than a handful in all.
- The remedy ladder fixes the definition before it changes a rule. 2 grouped folds x 30 repeats give 5 per class and
  25 per fold, which clears both checks. Training keeps 5 patients per class plus the library; the source's LOOCV
  trains on 4.

Decision:
(a) 2 folds (recommended; follows the rules as written, and both sides accept it);
(b) 3 folds, with the line written into TP-5 as an amendment that applies across datasets: for example, 3 or more
    units per class per fold, no short class, 15 or more units per fold, stable scores;
(c) Too Small (nobody asks for it).
Nothing measurable settles it; it rests on the curator's reading of "a handful".

ISSUE 3. The 6 library-only reference isolates (a weighing call; no Must triggered). Recommend keep, with the note C8.

Problem. Ciprofloxacin, ceftriaxone and caspofungin occur only in 6 reference isolates (13,200 rows). No test fold
holds them, so any probability a model puts on them is penalised and never rewarded.

Effect (mine: renormalising each row over the five patient groups, an upper bound without a refit):
- The loss of a linear model drops by 16-19% at every unit:
  - per spectrum, 0.242 to 0.197;
  - patient mean, 0.105 to 0.086;
  - patient log-prob pooling, 0.013 to 0.011.
- It is mostly a level shift. Among the three models trained on the same data, the full order stays the same on:
  - 59 of 60 splits at the patient mean;
  - 52 of 60 per spectrum;
  - 49 of 60 with log-prob pooling.
- A refit without the 6 isolates (column auditor, per spectrum): -0.007 to -0.049.

Why no Must:
- LEAK-14's mechanism, a tested class recognised by its source, is absent: no row of the three groups is ever scored.
- The spectrum tells the library from the patients at AUC 0.932 within the shared groups too, so it marks the subset,
  not a class.
- What remains is a prior that the training patients reveal (the gamer's honest restrict5: -0.005).

Each side's best evidence.
- Keep (advocate):
  - TP-6 (Must): a valid task stays, and a fix of our own is not a better version;
  - the source pre-trains on all eight groups;
  - a lab's library holds Candida, and patients do carry it;
  - renormalising barely reorders the models (tau 0.94).
- Drop (critic):
  - the test never rewards that mass, and it is 3-26% of the loss;
  - training and test would then hold the same five groups, matching "which of five";
  - the drop clears splits_test_class_missing;
  - the library's measured worth turns with the unit (41 of 60 splits per spectrum, 24 of 60 per patient; 31 of 60
    after renormalising, mine).
  That last point is about the whole library against patients only. Both sides keep the library, and every benchmark
  method gets the same training data.

Mediator: TP-6 leans keep, and the source's 8-group pre-training is the fact behind it. The drop is our own filter
and only removes a level. Decision: keep with a note (recommended) or drop.
What would settle it: whether the score should carry the open-set cost of a library's extra classes. Or a refit at the
chosen unit that shows the drop reorders the leading models; the renormalisation proxy says it mostly does not.

**5. THE TASK GAMER'S EXPLOITS, MAPPED**

The definition has no "Potential leak, kept on purpose:" note and no accepted warning, so every exploit is new.

Exploit 1 Neighbour rebuild from the test rows. Rule: LEAK-9 (an evaluation leak: a model reads other test rows). New.
  - Per spectrum: LR-PCA 0.153 to 0.104 (-0.049), LightGBM 0.386 to 0.261 (-0.125), lower on 60 of 60 splits.
  - 75-86% of a row's 10 neighbours are its own isolate, and 14-25% are other patients.
  - Under issue 1 (b), the own-patient part becomes the declared context. At the patient unit the trick (0.069 and
    0.222) loses to the allowed pooling over the patient's own spectra (0.037 and 0.179). Sharpening each row on its
    own matches it (0.072 and 0.221 at t=2), so it carries no information from other test rows.
  - The protocol line C5 bars the rest.
Exploit 2 Per-year make-up of the test fold. Rule: LEAK-9. New.
  - It uses the fold's composition from outside the training data: the paper's 5 patients per class per year, with the
    year read from one spectrum at AUC 0.993.
  - Gain per spectrum: -0.017 (better on 73% of splits) and -0.043 (80%). At the patient unit: -0.014 (53 of 60) and
    -0.033 (51 of 60).
  - It survives either unit and any random grouped split. Stratifying on treatment x year would still leave the
    complement known (by construction; untested).
  - Fix: the protocol line C5, with the gain written beside it.
  - The gamer's own fix, holding out whole years, is not taken: it leaves one pair of splits, a site transfer the
    source does not use as its task (both sides agree).
Exploit 3 PCA fitted on all rows. Rule: LEAK-9 (preprocessing that sees the test rows). New, and small (-0.004). Covered by
  C5.
Format (the raw count range): within noise. LEAK-39 reading: benign (the builder's probe 17 reading holds).
Future rows (2019 patients in training when 2018 patients are tested: -0.0085, mixed): not a leak. It is the
  pooled-years fit gap, named in C1.

**6. CONSISTENCY WITH PRECEDENT (precedent checker's report)**

- Framing: follows these precedents:
  - corporate_credit_rating and nba_players_2016_2019 (USE-5);
  - superconductivity (SPLIT-4);
  - micro_mass and pancreatic_cancer_mouse_detection (grouped by entity, SPLIT-29).
- Unit (b):
  - Follows musk (group, any, all_rows) and fraud_detection_in_electricity_and_gas_consumption_1m (group, mean,
    all_rows), and SPLIT-23's protein and huesken cases ("the context follows the use case, not the gain").
  - Departs from micro_mass, pancreatic_cancer_mouse_detection and raman_mlrod, which predict per row. What sets this
    case apart: in those, the use case is one spectrum or one sample. micro_mass identifies a colony from one spectrum
    (Mahé 2014). Each pancreatic bleed is its own serum test. raman_mlrod labels each point. This source identifies a
    patient by a vote over 10 spectra of one map, measured together.
  - Departs from the precedent checker's C2 (keep the row unit, with a use-case reason). C2 rests on an inferred
    one-spectrum limit, and it was written before the claim audit and the gamer's exploit existed.
  - The MET-17 cases stand: "the weight changes how much a prediction counts, never what one prediction is".
- Few patients:
  - parkinsons was retired at 2-3 per fold;
  - micro_mass and sarcoma were kept at 3-4 per class, inside large folds;
  - musk was kept at 13 per fold.
  2 folds follow the rules as written. 3 folds need an amendment (the precedent checker's C1). No drift.
- Library:
  - raman_mlrod has the same design.
  - These two would be the first by-design splits_rows_never_tested acceptances. Word them alike and add one Cases
    row (C9).
  - splits_test_class_missing is its own fact, not force_2020's.
- Metric: follows heart_disease, ljubljana_breast_cancer, gallstone_disease and covertype as applied (the fallback).
  MET-6's covertype line contradicts the record: flag it, do not follow it (C9).
- Protocol lines (LEAK-9): follows medical_facility_operational_data, sepsis_prediction_1m, 5g_energy_consumption,
  fremtpl2 and bank_marketing.
- A question to ask yourself, if you choose (a) in issue 1: what fact of this source makes one spectrum the
  prediction, when micro_mass's source identifies from one spectrum and this source votes over ten?

</details>

<details><summary>bacteria_id_raman: claim audit</summary>

bacteria_id_raman: claim audit (claim-auditor, 2026-11-09)

Verdict: the framing holds on the source and on the data; two claims fall and change what the curator reads.
(1) The reason given for scoring one spectrum at a time ("per patient it would saturate") is wrong for log loss: per
patient the log loss is 0.075-0.30, not near 0, and the model ranking changes with the unit. This is a SPLIT-23 (Must)
question about what one prediction is. (2) The 74.0% vs 93.1% numbers measure mostly the measurement session (the
reference file against the later 2 s files), not the culture. The framing decision (USE-5) does not rest on them.
Everything else I tested holds or is a wording fix. Scratch, scripts and outputs: the run's work files.

Inputs read: dataset.py, README.md, the record (screening, size check, CC 2026-11-08), claims.md (32 claims),
builder_report.md (issues 1-4), the probe outputs, the source's config.py, README and 3_clinical notebook (run
folder src/), the paper on PMC (PMC6960993: Results, Methods "Dataset", the Fig. 4 caption, data availability), and
principles.md, evidence.md, metrics.md, splits.md, task_probes.md, use_case.md, spectra.md from the df-large worktree.
Models: untuned, CPU, thread-capped (PCA-100 logistic regression, logistic regression C=0.01, kNN on PCA-30), on the
shipped splits from the definition's container (built in 13 s) or on the raw .npy files. These are probe numbers, not
leaderboard numbers (EV-8).

**A. The six points the main session asked for**

A1. The framing (USE-5, SPLIT-4, SPLIT-29): HOLDS on the source. The clinical task is the source's own: "Each patient
    is classified into one of 8 treatment classes where each species corresponds to a different treatment class"
    (Fig. 4 caption). The source holds out whole patients: "We use a leave-one-patient-out cross-validation (LOOCV)
    strategy for fine-tuning, where we assign 1 patient in each class to the test set" (Results). It pre-trains on the
    reference isolates' treatment labels: "For the clinical isolates, we start by pre-training a CNN on the empiric
    treatment labels for the 30 reference isolates" (Methods); "We augment our reference dataset with this clinical
    dataset" (Results). The use-case quote is verbatim (Results). The paper also scores the 8 treatment groups on the
    30-isolate test file (CNN 97.0%, LR 93.3%, SVM 92.2%). So the treatment group of a new patient, grouped by patient,
    follows the source's clinical extension. SPLIT-4 holds: a patient is an entity new data does not contain.
    One point does not follow the source: what one prediction is (A1b, refuted below).

A1b. The prediction unit: REFUTED (the reason given). grouping says prediction_unit="row", "Each spectrum is one
    prediction made from that spectrum alone (the source votes over 10 spectra per patient)"; builder issue 4 gives the
    reason: "patient accuracy is 0.96-1.00 for every family, so it would saturate". The source's unit is the patient:
    "We then use 10 randomly sampled spectra from each patient isolate in the test set" and "The most common class out
    of the 10 spectral classifications is then chosen as the identification" (Results); the notebook says this is "to
    simulate a culture-free clinical setting where not many bacterial spectra may be available". Test
    (t6b_unitrank.py and .json, repeats 0-1, 6 folds, 3 models): accuracy saturates, but log loss
    does not, and the ranking changes:
        unit                                   PCA-100 LR   LR C=0.01   kNN-PCA30   best per fold
        per spectrum, patient-weighted (ships)   0.228        0.214       0.585     LR C=0.01 5 of 6
        patient, mean prob. of 10 spectra        0.104        0.128       0.220     PCA-100 LR 6 of 6
        patient, mean prob. of all its spectra   0.100        0.124       0.213     PCA-100 LR 6 of 6
    The two logistic regressions swap places on 5 of 6 folds. Patient accuracy is 0.977-1.000 (vote over 10) and
    1.000 (all spectra) in all 12 fits (t6_units.json), so accuracy saturates, but the declared metric is log loss.
    Rule: SPLIT-23 (Must; P4): the source's use case, cited, decides what one prediction is. A P6 argument (a score
    that saturates) does not decide a P4 rule (principles.md, "The right split against the score").
    Mildest remedy: Grouping(prediction_unit="group", aggregation="mean"), the API's closest form of the source's
    patient identification (all of a patient's spectra averaged; 10 vs all spectra differ by 0.004 here). Or keep "row"
    and state in grouping.definition why the use case's prediction is one spectrum. Either way it is a curator's call
    with these numbers; builder issue 4 should carry them.

A2. 74.0% on the cultured test file vs 93.1% at random (claim 21; curation_comments framing bullet: "a split over
    spectra mostly rewards knowing the culture"): numbers HOLD, attribution REFUTED. The 3,000 random hold-out comes
    from reference + fine-tuning (95% from the reference file). The reference file is a different measurement session
    from the 2 s files: "were increased from 1 s to 2 s in order to keep SNR consistent across datasets", after a
    "degradation in optical system efficiency" (Methods). Test (t9_framing.py/.json, PCA-100 LR, 30 isolates):
        train 57,000 of the reference file -> 3,000 held out of the same file      92.6%
        train 57,000 of the reference file -> fine-tuning file (2 s, same strains)  45.2%
        train 57,000 of the reference file -> test file (2 s, new cultures)         43.6%
        train reference + half the fine-tuning file -> its other half (same culture) 76.8%
        train reference + half the fine-tuning file -> test file (new culture)       70.9%
    Most of the 19-point gap is the session or file (93% -> 45% for the same strains). A new culture adds about 6
    points. SPLIT-29 still holds, and more strongly: a random split over spectra rewards the map and session. The
    framing decision rests on USE-5 (lab strains are not what the physician acts on) and stands. Remedy: reword the
    bullet (numbers above).

A3. Patients per group and per test fold (TP-5, TP-8): the counts HOLD; the weighing is the curator's. Container, all
    60 splits (t5_container.py): every fold holds 16 or 17 patients (40 folds with 17, 20 with 16), 3 or 4 per group,
    and every fold has at least three groups with only 3 test patients; 10 patients per group in all; 2018 patients per
    fold 4-11, 2019 patients 5-13 (the folds are stratified by group, not by year). New numbers for the weighing
    (t6_units.json, PCA-100 LR and LR C=0.01, 6 folds): one patient carries 16-51% of a fold's patient-weighted log
    loss and three patients carry 43-83%. The same few patients top every repeat: 2018-16 (log loss 1.35-2.00, 42-51%
    of folds r0f2 and r1f2), 2018-25, 2019-21. Precedents: parkinsons retired (8 healthy people, 2-3 per fold), musk
    kept (13 musk per fold), huesken kept (10 test genes per fold, regression, signal measured). Here there are 10 per
    class and 3-4 per fold, closer to parkinsons by count. Unlike parkinsons there is no `unstable` or `no_spread` flag
    (LightGBM beats the dummy on 5 of 5 splits, spread +0.349, paired SE 0.009). The builder's rank list is consistent:
    on 9 splits the top two of four models swap on 2 and the bottom two on 3 (shipped_compare.json). Not refuted.
    Builder issue 2 should carry the concentration numbers: the score of a fold depends heavily on 1-3 atypical
    patients.

A4. The 66,000 reference spectra (labels, never tested): HOLD.
    - Labels: REFERENCE_ISOLATES matches config.py's STRAINS and ATCC_GROUPINGS on all 30 isolates (t1_basic.py; 0
      mismatches).
    - The clinical codes are in the same code space as ATCC_GROUPINGS. A model trained on the reference library alone
      (ATCC groups) predicts the patients' codes on the diagonal: per spectrum 75.0% (2018) and 67.9% (2019), per patient
      0.96 and 0.76, with every code's diagonal 0.35-0.99 (t2b_refonly.json). A permuted code space would put the
      diagonal near 0.
    - Never tested and no isolate on both sides: asserted on all 60 splits.
    - Cost of the three training-only classes: on average a test spectrum puts 1.1-3.3% of its probability on them
      (t6_units.json), which is small.
    - The prior shift is not small. The training class shares, which the reference rows dominate, score 1.906-2.009 as a
      dummy, against ln 5 = 1.609 for uniform over the five tested groups. So the task probe's "class shares" dummy is
      handicapped by 0.34 nats: LightGBM's skill is about 0.75 against ln 5, not 0.81 (claim 32 holds as worded).
    - New measured fact for claim 17. A reference-only model fits the 2018 patients far better than the 2019 ones
      (0.96 vs 0.76 per patient). Adding the 2 s fine-tuning and test files flips this (0.80 vs 0.96). So the 2018 file
      looks like the reference file's session and 2019 like the 2 s files. The SNR (median absolute second difference
      on the 0-1 scale) is about equal: 0.157-0.163 in the three reference files, 0.179 in 2018, 0.165 in 2019. This
      fits "to keep SNR consistent".

A5. The spectrum declaration (special_features, spectra.md): HOLDS, except the map size.
    - Axis orientation. On the declared axis (columns high to low, named from wavenumbers.npy) the S. aureus minus
      others difference peaks at 1524.9 and 1161.7 cm-1, staphyloxanthin's carotenoid bands. The mean spectrum peaks at
      1003.1 (phenylalanine), 1451.3 (CH2) and 1659.3 (amide I). Reversed, the carotenoid peaks would fall at 694.6 and
      1081.5 (t2_axis.py).
    - The 1,000 names are unique. The grid is monotone with 1.2-1.56 cm-1 spacing. feature_columns is exactly the
      1,000 raman_ columns (isolate and isolate_weight excluded). The recommended encoding is spectrum-as-is-r1 and the
      state is processed.
    - Min-max scaling: 4.6-8.0% of spectra do not reach 0 and 0.9-2.5% do not reach 1 (claim 15 exact).
    - 1 s vs 2 s: the wording holds against the Methods. See A4 for the data side.
    - "One spot of a 45 x 45 map" (special_features.description; claim 16): partly refuted.
      - Reference file: the rows of an isolate correlate at lags 44-45 (0.054-0.058, against 0.025 at lag 30), a
        45-wide raster scan. Holds there.
      - 2018 file: rows correlate at lags 19-21 (0.009-0.013) and 38-41 (0.005-0.007), near 0 between. That is a
        20-wide raster, as a 20 x 20 map of 400 spots would give (t7_species_map.py, t7b_lags.py).
      - Paper: "400 spectra are measured across a sample from each patient isolate".
      Remedy: say 45 x 45 for the reference isolates and "map size not stated" for the patients. The 2018 rows look like
      a 20 x 20 map.

A6. Can one patient's spectra leak across the split?
    - The block boundaries HOLD, and the evidence is stronger than Decision 2's.
      - Offset scan: the nearest-centroid accuracy within a group is highest at offset 0 in 10 of 10 file-and-group
        pairs (t3_blocks.py/.json).
      - Adjacent-row correlation drops at the block edges in 10 of 10 (inside 0.36-0.60, at the edges -0.06-0.35). The
        rows are map spots in scan order, and the order breaks exactly at 400 and 100.
      - The container shuffles the rows, so row order cannot leak.
    - Exact copies: 0 of 78,500 over all five files (md5 of each row).
    - Maybe near-copy patients (EV-6: circumstantial).
      - 7 of 100 within-group patient pairs are as alike as two random halves of one patient's spectra (t4b_pairauc.json):
        2018-12/13 (cross-validated AUC 0.570), 2018-07/10 (0.571), 2018-06/07 (0.580), 2018-22/23 (0.606), 2019-06/08
        (0.520), 2019-06/09 (0.537), 2019-06/07 (0.562).
      - References: halves of one block have median AUC 0.48 and max 0.69 (2018) / 0.61 (2019). Distinct patients of a
        group have median 0.946 / 0.987. Two cultures of one reference strain have median 0.81 and minimum 0.51.
      - So these pairs could be one isolate measured twice or clonal strains of one species. The data cannot tell them
        apart, and the source lists no species or patient ids.
      - The pairs sit in adjacent blocks (06/07, 12/13, 22/23), which fits either reading.
    - Does a near-copy in training help (t8_twins.py, t8b_twins_control.py, t8b_pairs.csv; PCA-100 LR on all 60
      splits)? Each patient's log loss is compared with its partner in training and with its partner in test, for the
      near-copy pairs and for all 166 ordinary same-group, same-year pairs:
      - ordinary pairs: mean gain 0.016, median 0.001;
      - near-copy pairs: mean gain 0.037, median 0.008.
      Five of the seven pairs sit at the 17th to 84th percentile of the ordinary pairs, so no special effect. The
      exception is 2018-22/23 (daptomycin, E. faecium): each one's log loss drops by 0.210 and 0.136 when the other
      trains (98th and 93rd percentile; 0.48 -> 0.27 and 0.24 -> 0.10). Per fold that is about 0.01 nats, the size of
      the LightGBM-RF paired SE (0.009) and far below the family spread (0.35).
    - Verdict: maybe one near-copy pair (2018-22/23), a small effect. No patient-level leak otherwise.

A7. The metric (claim 26; dataset.py `metric = Metric.fallback(...)`, README "Metric"; MET-1 to MET-17): HOLDS.
    - Does the source name a metric? I looked again. The paper reports accuracy only:
      - isolate-level accuracy on the 30-isolate test file;
      - treatment-group accuracy on that file;
      - per-patient identification by majority vote over 10 spectra ("99.7±1.1%" for 2019; species "89.0±3.6% to
        99.0±1.9%" for 2018);
      - for the binary MRSA/MSSA sub-task, accuracy 89.1% and AUC 0.953.
    - No threshold or cost matrix is fixed for the treatment groups. The paper only says that the MRSA/MSSA binary
      decision "can be tuned for higher sensitivity", and both of those are the vancomycin group here.
    - One point the reason does not record (MET-1, "record where you looked"): the notebook's early stopping selects
      models by validation accuracy (`if acc_val > best_val`), so accuracy is also the source's selection criterion
      (MET-5). The fallback still holds under MET-6 and MET-8: accuracy at equal costs, while a wrong empiric antibiotic
      costs differently by pair. This follows the accuracy-only precedents (ljubljana, gallstone).
    - Form: a fallback with a weight input matches the unit-weighted precedents (boreal_postfire_lichen_biomass,
      dementia_prediction and pancreatic_cancer_mouse_detection all declare Metric.fallback with the weight). MET-17's
      "declared from context" wording is not followed by them either.
    - Computable on our data (MET-2):
      - The unit exists. isolate_weight sums to 1.000000 per isolate (80 of 80).
      - The input ships as a scoring column, not a feature. feature_columns has 1,000 raman_ columns only, and
        sample_weight is None.
      - Every test fold holds 16-17 patients with all five tested groups.
      - The scorer ran on all 60 folds with dummy predictions. Training row shares: 1.906-2.009 (mean 1.953).
        Training isolate shares: 1.713-1.750. Uniform over the 5 tested groups: 1.609. Uniform over 8: 2.079.
    - Same meaning as on the source (MET-2, third point): same target (treatment group), same classes (8 output, 5
      tested), same balance (5 patients per group per year, as in the source's LOOCV).
    - The weight follows the source's per-patient view. Kendall tau between the weighted and per-row log loss, recomputed
      from shipped_compare.json: 0.911 mean, 0.60 lowest over 18 runs. The 18 runs include the patients-only variant; on
      the shipped variant alone it is 0.933 and 0.60.
    - The metric's unit is A1b's question, not this one.

**B. Table: every claim of claims.md plus the implied ones**
claim | source | test | result | evidence | rule

1 first published with Ho 2019 via github, MIT | source, license, bibtex | data availability statement on PMC; gh api; LICENSE | holds | "All data needed to replicate these results are available at https://github.com/csho33/bacteria-ID"; repo license MIT | PROV-1, EV-4
2 zip 628,639,018 bytes, sha256 05f0978e...074f | download_description | sha256sum, stat | holds | identical | PROV-8
3 year 2019 | year | gh api created_at | holds | 2019-06-12; paper 2019 | -
4 all five files, 78,500 rows | curation_comments | row counts; container | holds | 60,000+3,000+3,000+10,000+2,500 | -
5 30 isolates x 2,000/100/100 | curation_comments | label counts | holds | each code 2,000/100/100 | -
6 2018 25x400, 2019 25x100; Methods 30 | curation_comments, row | counts; PMC | holds | Methods: "30 patient isolates ... 400 spectra per isolate"; Results 25 | PROV-13
7 VA Palo Alto 2018, Stanford Feb-Mar 2019 | row | PMC | holds | quoted | -
8 patient from row order | grouping.definition, Decision 2 | offset scan; adjacent-row correlation at the edges | holds (stronger) | offset 0 best in 10/10; edge drop in 10/10 | SPLIT-24
9 no two spectra equal | curation_comments | md5 of every row | holds | 0 of 78,500 | LEAK-16
10 target from config.py | TREATMENTS, REFERENCE_ISOLATES | parse config.py against dataset.py | holds | 0 of 30 mismatches | USE-5
11 clinical codes are treatment codes | predicted | reference-only model predicting the patients | holds | diagonal 0.35-0.99 per code; 0.96/0.76 per patient | USE-5, TP-7
12 each clinical species one group | fit_reason | nearest reference species per patient | holds (circumstantial) | vancomycin 10/10 S. aureus; penicillin 10/10 E. faecalis; daptomycin 10/10 E. faecium; meropenem 10/10 Enterobacterales; TZP 6/10 P. aeruginosa | EV-6
13 three groups only in the reference | curation_comments | counts | holds | - | TP-8
14 spectrum the only feature, axis, names | special_features, known | feature_columns; band positions | holds | carotenoid 1161.7/1524.9, phenylalanine 1003.1 on the declared axis | CLEAN-26
15 processed, 0-1 per spectrum, anomaly | special_features | min/max per spectrum | holds | 4.6-8.0% min != 0; 0.9-2.5% max != 1 | CLEAN-26
16 one spot of a 45 x 45 map | special_features.description | row-lag correlations | partly refuted | reference: lag 44-45 peak; 2018: lags 19-21 and 38-41 (20-wide) | PROV-13 (description), writing.md
17 1 s / 2 s; 2018 not stated | curation_comments | PMC; SNR by file; reference-only fit by year | holds as worded | 2018 behaves like the reference file's session (0.96 vs 0.76 per patient) | EV-2
18 test file separately cultured | curation_comments | per-isolate AUC fine-tuning vs test | holds (circumstantial) | median 0.81, min 0.51 | EV-6
19 use-case quote | use_case | PMC | holds | verbatim | USE-1
20 fit approximate | fit_reason | read | holds | - | USE-8
21 30-isolate task set aside; 74.0% vs 93.1% "mostly rewards knowing the culture" | curation_comments | random hold-out by file | numbers hold, attribution refuted | 92.6% same file vs 45.2%/43.6% on the 2 s files of the same strains; culture alone about 6 points (76.8 vs 70.9) | SPLIT-29, EV-1
22 splits 16-17 patients, 3-4 per group, reference never tested | splits_comment | all 60 splits | holds | 100 group-folds with 4, 200 with 3 | SPLIT-4
23 source: one patient per group out, five folds over 2018; 2019 tested after training on 2018 | splits_comment | notebook + PMC | partly refuted (wording) | 2019 is tested in its own 3/1/1 loop after further fine-tuning on the other 2019 patients; the source fine-tunes on 10 spectra per training patient | SPLIT-5
24 source pre-trains on the reference for 8 groups | grouping.definition | notebook + Methods | holds | "pre-training a CNN on the empiric treatment labels for the 30 reference isolates" | -
25 reference library worth mixed | curation_comments | recount from shipped_compare.json | holds | 5/9, 4/9, 4/9, 1/9 | TP-6
26 metric fallback, weighted per patient | metric, scoring_columns, unit_weight | source reread; scorer on 60 folds; weight sums | holds | see A7 | MET-1, MET-2, MET-6, MET-8, MET-17
27 tau 0.91 mean, 0.60 lowest | curation_comments | recomputed | holds | 0.911/0.60 (shipped variant 0.933/0.60) | MET-17
28 leak probes | builder report | exact copies recounted; the rest read only | holds (copies); rest untested here | 0 copies | LEAK-16 to LEAK-21
29 number-format probe = exact 0.0 and 1.0 | builder report | 2,000 spectra of 2018 | holds | 0.20% of values have <= 3 decimals, 91.7% of those are 0 or 1 (claim: 95.6%) | LEAK-39
30 permutation signal | builder report | read script + JSON | holds | real 0.19-0.27 vs permuted >= 1.66 (labels permuted across all 80 isolates) | SPLIT-27
31 encodings | curation_comments | JSON read, not re-run | untested (re-run) | numbers match the JSON | CLEAN-26
32 task probe | builder report | JSON read; dummy recomputed | holds as worded | the class-share dummy is 0.34 nats worse than ln 5 (reference prior); skill about 0.75 against ln 5 | TP-1, EV-9
I1 (implied) every feature known at the prediction point | known | feature list | holds | spectrum only | USE-3, LEAK-10
I2 (implied) the target is the actor's target | predicted | PMC Fig. 4 | holds | treatment group per patient | USE-5
I3 (implied) one prediction is one spectrum | grouping prediction_unit="row"; builder issue 4 | per-patient log loss, three units | refuted (the reason) | patient log loss 0.10-0.22 (not saturated); the two LR models swap on 5 of 6 folds | SPLIT-23 (Must)
I4 (implied) no patient copy across the split | - | pairwise AUC within groups; twin effect | holds for exact copies; maybe near-copies | 7 of 100 pairs as alike as halves of one block | LEAK-17, EV-6, SPLIT-24
I5 (implied) TP-5 borderline but keep | builder issue 2 | counts; loss concentration | counts hold; weighing open | 1 patient = 16-51% of a fold's loss, 3 = 43-83% | TP-5, TP-8

**C. Refuted and untested claims, ranked (validity first, Must first)**

1. P4, SPLIT-23 (Must): one prediction per spectrum (I3; builder issue 4's reason). REFUTED.
   - What it changes: the unit decides which methods win. At the source's unit (the patient), PCA-100 LR beats
     LR C=0.01 on 6 of 6 folds (0.104 vs 0.128). Per spectrum, LR C=0.01 wins 5 of 6 (0.214 vs 0.228). kNN's gap to
     the best shrinks from +0.37 to +0.12. The "it would saturate" reason holds for accuracy only, and the metric is
     log loss.
   - Mildest remedy: a curator's call between two options.
     - (a) Grouping(prediction_unit="group", aggregation="mean"): the patient from its spectra, the source's
       identification unit, 16-17 units per fold.
     - (b) Keep "row" and write the use-case reason why one spectrum is the decision, as an exception the curator
       names. Note that a Must takes no exception, so (b) needs an argument that the use case itself predicts per
       spectrum, e.g. a culture-free reading where each cell is measured once.
   - Builder issue 4 should be re-filed under P4 with these numbers.

2. P4, LEAK-17 / SPLIT-24 (maybe): near-copy patients across the split (I4). Maybe; a question, not a refutation.
   - What it changes: a fold holding one of 2018-22/23 in test with the other in training scores about 0.01 nats
     better. That effect is weak (LEAK-17 graded "weak"). The other six pairs act like ordinary patients of a species.
   - Mildest remedy: keep, with a "Potential near-copy, kept on purpose" note naming 2018-22/23 and the numbers. Do not
     merge them into one group: SPLIT-24 forbids grouping on similarity. Note that the authors could be asked for
     patient ids (SPLIT-25).

3. P3/P4, SPLIT-29 evidence (claim 21): "a split over spectra mostly rewards knowing the culture". REFUTED as an
   attribution.
   - What it changes: nothing in the framing, which rests on USE-5. The evidence sentence in curation_comments and
     builder issue 1 is wrong.
   - Mildest remedy: reword. A random split over spectra rewards the map and session: 92.6% within the reference file
     vs 45.2%/43.6% on the 2 s fine-tuning and test files of the same strains. Within the 2 s session a new culture
     costs about 6 points (76.8% vs 70.9%).

4. P5, the description of the spectrum (claim 16): "one spot of a 45 x 45 map". PARTLY REFUTED: holds for the
   reference isolates; the 2018 patients' rows repeat at a 20-row lag (a 20 x 20 map of 400).
   - What it changes: one sentence of special_features.description.
   - Remedy: reword ("45 x 45 for the reference isolates; the patients' map size is not stated").

5. P5, the source's protocol (claim 23): "tests the 2019 patients after training on 2018". PARTLY REFUTED.
   - The 2019 patients are tested in their own one-patient-per-group-out loop after further fine-tuning on the other
     2019 patients. The source fine-tunes on 10 spectra per training patient.
   - Remedy: reword splits_comment.

6. P6, TP-5 / TP-8 (builder issue 2): not refuted; new numbers for the curator's weighing.
   - One patient carries 16-51% of a fold's log loss and three carry 43-83%. The same three patients (2018-16,
     2018-25, 2019-21) lead in every repeat.
   - 10 patients per class, 3-4 per fold: by count this is between parkinsons (retired: 8, 2-3) and musk (kept:
     13 per fold).
   - Remedy: add the numbers to issue 2.

7. P6, the dummy (claim 32): holds as worded. The class-share dummy pays 0.34 nats for the reference library's prior
   (1.953 against ln 5 = 1.609), so skill against the class shares overstates skill against a sensible prior: about 0.75
   instead of 0.81 for LightGBM. Remedy: a clause in the accepted `groups_test_groups_few` text and in issue 3 (the
   reference library shifts the prior as well as the spectra).

Untested here, and why:
- Claims 28 (leak probe numbers other than copies) and 31 (encodings): read from the run's JSON, not re-run. They are
  untuned probe outputs, and re-running them is the builder's probe, not a refutation test.
- A within-year measurement-day batch by species (builder's concern): not testable without dates. The 2018 -> 2019
  transfer (90.1% per spectrum) and the patient-level fit of a reference-only model (0.96 on 2018) bound it but do not
  exclude it.
- The patients' species and ids (needed to settle item 2): Supplementary Table 2 was not read here either.

What the curator gets from this audit:
- The framing is the source's own clinical task and holds.
- A SPLIT-23 question about what one prediction is, with numbers.
- A maybe on near-copy patients, with its measured effect.
- Three wording fixes (claims 16, 21, 23).
- Two sets of numbers for issues 2 and 3.

</details>

<details><summary>bacteria_id_raman: column audit</summary>

bacteria_id_raman: column audit (column-auditor, review panel, 2026-11-09)

Verdict: no leak, and no column that should not be there. The spectrum is the only feature. It is known at the
prediction point, the source processed it one spectrum at a time, and it is declared correctly. The reference labels
match the source's ATCC_GROUPINGS for all 30 isolates, and no reference row is ever in a test fold. There is one
question for the curator (P4, weighing, part of builder issue 3): the three treatment groups that only the reference
library holds can be ruled out on patient spectra because the spectrum shows which file it came from. Doing so is worth
0.007-0.049 of weighted log loss. There is also one note to strengthen (a measurement batch the spectrum carries
strongly) and four writing fixes.

Read: dataset.py, README.md, builder_report.md, claims.md; principles.md, use_case.md, leak_checks.md,
cleaning_features.md, spectra.md (worktree df-large); the source's config.py, 3_clinical_finetuning.ipynb, README and
datasets.py (github.com/csho33/bacteria-ID, fetched 2026-11-09; config.py is identical to the builder's copy); the
paper's Methods and Results (PMC6960993 full text via Europe PMC).
Code and logs:  (raw_checks, label_checks, frame_checks, domain_checks, absent_classes, year_batch;
dtype probe output in dtype/).

**Column table**
column | meaning | known at prediction? | dtype and cleaning | verdict | rule

raman_1792.4 ... raman_381.98 (1,000 columns; one block, `special_features` raman_spectrum) |
  The intensity at each Raman shift of one spectrum from one spot of the isolate's dried monolayer. It is
  background-corrected (a 5th-order polynomial, subbackmod) and scaled to 0-1 one spectrum at a time "within this
  spectral range" (Methods) |
  yes: measured on the isolate before identification. The source's processing uses that spectrum alone (background,
  min-max). The only row filter is the removal of the 25 highest-intensity spectra of each map, which is within one
  sample (one isolate, so within one group) and can be repeated for a new patient |
  float64, 0 NaN, 0 negative, 0 above 1. No constant or duplicate column. Axis = wavenumbers.npy exactly, in file
  order (high to low). The container lists the columns from 381.98 to 1,792.4 cm-1, state `processed`, encoding
  spectrum-as-is-r1. Axis direction checked on the data: the phenylalanine band peaks at 1003.1 cm-1 (prominence
  0.224 over +-4 positions; 0.018 if the axis were reversed), with carotenoid bands at 1157.5 and 1523.6, CH2 at
  1450.0 and amide I at 1659.3. The grid is uneven (1.20-1.56 cm-1 apart: detector pixels, not interpolated). No
  all-row scaling: column means 0.19-0.79, SD 0.11-0.19. 534 columns hold both an exact 0 and an exact 1, which comes
  from the per-row scaling (92-95% of rows reach 0, 97.5-99% reach 1). No edge fill: an exact 0 in the first or last
  column in 0.00-0.08% of spectra. Format is the same in all five files: full float64; the only short values are
  each spectrum's 0.0 and 1.0 (0.20-0.21% of the values of every file) |
  fine | CLEAN-26, LEAK-30 (not triggered), LEAK-13/16 (no format difference)

isolate | the group: a patient's isolate (50, recovered from 400-row blocks in 2018 and 100-row blocks in 2019, as
  the source's notebook indexes them), or one of the 30 reference isolates ("reference <strain>") |
  not a feature: metadata. `feature_columns` gives exactly the 1,000 spectrum columns; README: "metadata, never a
  feature" |
  category, 80 levels, one label per isolate (assert in _clean, checked). The id encodes the label: the patient
  numbers follow the file blocks (2018-01..05 meropenem, 06-10 daptomycin, 11-15 penicillin, 16-20 vancomycin, 21-25
  TZP; 2019-06..10 penicillin, 11-15 daptomycin), and a reference name spells the species |
  fine, with optional hardening (finding 3) | LEAK-33, SPLIT-24

empiric_treatment (target) | the source's empiric treatment group (config.py `antibiotics`). For reference rows it
  comes from ATCC_GROUPINGS of the isolate code; for patients it is the label file's code ({0,2,3,5,6}; the
  notebook trains these with n_classes = 8, "the 8 empiric groupings") |
  target |
  category, 8 levels in words, unordered (nominal: correct). REFERENCE_ISOLATES vs config.py STRAINS + ATCC_GROUPINGS:
  0 mismatches of 30. TREATMENTS vs `antibiotics`: same codes, TZP written out as Piperacillin-tazobactam (correct).
  Reference codes 0-29, 2,000/100/100 rows each. Clinical: one label per block in both files |
  fine | CLEAN-25, USE-5

isolate_weight | 1 over the isolate's rows (0.0025 for a 2018 patient, 0.01 for 2019, 1/2,200 for a reference
  isolate) |
  not a feature: scoring column (role weight) and the unit weight. Its value names the file, which is why it must
  never be an input |
  float64. Sums to 1.000000 for every isolate. Not a sample_weight (sample_weight None). Excluded by
  `feature_columns` and dataset_io |
  fine | MET-17, LEAK-41 (not applicable: no training weight)

Not shipped, checked against the source:
  measurement time (1 s / 2 s): no column. The Methods give 2 s for the fine-tuning, test and 2019 files; the 2018
    time is unstated (implied 1 s), and such a column would mark the reference rows, the only rows of three groups.
    Leaving it out is right.
  source file: no column, since no new patient comes with one. Right.
  map spot / day / culture batch: not in the release.

Dtype probe (dtype_probes.py bacteria_id_raman --no-fetch): 0 of 1,000 columns flagged. The spectrum columns are
measured intensities, numeric: correct. The target, group and scoring column are excluded by the probe and checked
above.

**Problems, ranked (principles.md: rank, then strength, then effect)**

1. P4, question for the curator (weighing; part of builder issue 3). The spectrum shows which file it comes from, and
   the file decides which classes are possible.
   Rules: closest LEAK-14 (classes from a separate source or measurement series), USE-8 (fit), TP-8. This is not a
   Must violation, since none of the three classes is ever tested.
   Mechanism: ciprofloxacin, ceftriaxone and caspofungin exist only in the reference library (a separate measurement
   series: lab strains, a 1 s / 2 s regime, other cultures). The spectrum separates the reference library from the
   patients within the five shared groups at ROC AUC 0.932 (PCA-50 logistic regression, grouped 5-fold by isolate).
   The training patients show that patients never carry those three groups, so a model that learns "clinical-looking
   spectrum, not one of the three" scores better. In use, a patient may carry Candida, Salmonella or S. pneumoniae.
   Evidence (repeat 0, three shipped folds, PCA-100 features, untuned; absent_classes.log):
     probability on the three groups for test patients, patient-weighted: trained on the reference library alone,
     LR 0.065-0.096 and LightGBM 0.046-0.058; as shipped, LR 0.015-0.029 and LightGBM 0.003-0.018.
     weighted log loss as shipped vs. without the 6 reference isolates of the three groups (13,200 rows):
     LR 0.188/0.179/0.251 vs 0.139/0.164/0.232 (-0.049/-0.015/-0.019);
     LightGBM 0.203/0.124/0.369 vs 0.170/0.117/0.354 (-0.033/-0.007/-0.014).
     So 3-26% of the loss is about ruling out classes the test never holds.
   Remedies, mildest first: (a) keep, and name it in the notes and in issue 3: the eight-group output space is the
   source's, and the cost above is part of what a model is scored on. (b) Drop the 6 reference isolates of the three
   training-only groups, so training and test hold the same five groups. This also clears
   `splits_test_class_missing`, and it matches fit_reason's "which of five". (c) Builder issue 3 option B (patients
   only). It is a weighing call. Facts for it: (a) follows the source's 8-group pre-training; (b) removes a reward for
   recognising the domain that would not carry over to practice.

2. P4, note to strengthen (LEAK-13/15/39 reading: no evidence of a batch by class; cannot be ruled out). The spectrum
   carries its measurement batch strongly: 2018 against 2019 patients at ROC AUC 0.994 grouped by patient (0.920-1.000
   within each treatment group; domain_checks.log). The year does not give the label away: 5 patients per group in each
   year. But a batch by class within a year (measurement days), if it exists, would be read just as easily. The files
   hold no dates. The source rules out batch effects from sample preparation only ("prepared separately for each
   patient"). Measured (patients only, PCA-50 LR; year_batch.log): within-year grouped 5-fold accuracy 0.943 (2018) and
   0.907 (2019), against 0.882 (2018 -> 2019) and 0.841 (2019 -> 2018) across years; patient accuracy across years
   0.96 and 0.92. The 5-7 point drop fits the year shift alone, and the species signal carries across site and year.
   This is consistent with the builder's "concern, cannot verify". Remedy: keep. Add the year-separability number to
   the measurement-settings bullet, so the curator sees how strong a batch would be.

3. P4, low (LEAK-33 holds): `isolate` encodes the label. The patient number follows the file's label blocks, and a
   reference name spells the species. It is never a feature, so the benchmark is safe. Anyone who reads the raw frame
   without `feature_columns` would see the label. Optional hardening at no cost: number the patients within each year
   in a seeded random order, so the id no longer follows the label.

4. P7 / writing (four fixes in dataset.py; no data change):
   a. The comment on CLINICAL_FILES says "five patients per treatment group, the groups in code order". The files are
      not in code order: 2018 blocks run 0, 6, 5, 3, 2 (meropenem, daptomycin, penicillin, vancomycin, TZP), and 2019
      runs 0, 5, 6, 3, 2. The code does not depend on the order (labels come from the y files, and the assert holds),
      so only the comment is wrong.
   b. The anomaly bullet guesses "as if scaled before a crop or a step we do not know". The data do not support the
      crop. Among spectra that do not reach exactly 0, the minimum sits at an inner position: at the first or last
      five positions in 0.3-0.7% of them, as for the spectra that reach 0 (0.1-0.5%). The argmax pattern is similar.
      Suggest "after a step we do not know". The rate of not reaching 0 varies a little by class among patients
      (3.4-12.2%, with no consistent order across the two years), worth at most about 0.53 ROC AUC as a flag: no
      artefact by class.
   c. The notes leave out the source's row filter: "discarding the 25 spectra with highest intensity" per map (45 x
      45 = 2,025 - 25 = 2,000 per reference isolate). It is within one sample, so not an all-row statistic (LEAK-30
      not triggered), but it belongs in the account of the source's processing next to the background and scaling.
   d. Optional: say in the Spectrum description that the grid is uneven (1.20-1.56 cm-1 between positions). The
      Savitzky-Golay candidate differentiates by position, not by cm-1.

Checked and fine, for the record:
  * Reference labels: 30 of 30 isolates map to config.py's STRAINS and ATCC_GROUPINGS. Reference rows are never
    tested: 0 reference rows in any test fold of the 60 splits, and no isolate on both sides.
  * Clinical labels are treatment codes, not isolates (the notebook trains them as 8 treatment groupings). Each 400- or
    100-row block holds one label, and there are 5 patients per group per year.
  * Frame: 78,500 x 1,003, rows shuffled (CLEAN-23), features = the 1,000 spectrum columns only.
  * Probe 17 (number format alone, 0.712): consistent with the per-row 0.0 / 1.0 (all files full float64 otherwise);
    no recording difference between files or classes by format.

</details>

<details><summary>bacteria_id_raman: split audit</summary>

SPLIT AUDITOR REPORT: bacteria_id_raman (2026-11-09)
Folder: df-large datasets/_dev/tabarena-v0pt2/bacteria_id_raman/dataset.py (read-only). Scripts, logs and outputs:
panel/ (s0_cache.py, s1_structure.py, s2_models.py, s3_isolate_task.py, s4_noise.py,
s5_iid_and_reference_twins.py; s4_fold_scores.csv, s4_patient_scores.csv, s3_isolate_task.json, s5_iid_twins.json).
Models: untuned. "LR" = StandardScaler + PCA-100 + logistic regression (C=1). The 60 shipped splits, metric as
declared (log loss weighted by isolate_weight), 4 threads per process.

VERDICT: right with notes.

Judgment record
  Validity: USE-10 / SPLIT-4 / SPLIT-23 / SPLIT-29 hold (a new patient's isolate, grouped by patient; an IID split
    flatters the score by a quarter to two thirds and reverses the ranking in issue 3); SPLIT-24 holds (blocks of
    the source's own row indexing, one code per block in 50 of 50); SPLIT-30: one look-alike patient pair
    (2018-22/23) helps itself across the split, kept (no shared entity that new data would lack); no patient
    found to be a reference strain.
  Value: TP-5 / TP-8 borderline keep. Stratification holds on all 60 splits. The noise from the patient sample is
    18x the noise across repeats.
  For the curator: issue 2 (few patients) and issue 3 (library) remain weighing calls; the numbers below add to
    both. The comparison of 74.0% against 93.1% in issue 1 overstates the culture effect (reword it).

**FINDINGS, in rank order (principles.md)**

1. P3/P4: REGIME. Grouped by patient is right. (USE-10 Must, SPLIT-4 Must, SPLIT-23 Must, SPLIT-29 Must)
   A physician's new patient brings a strain never measured. That is a cold start, and a grouped split tests it.
   The source holds patients out too ("spectra from the same patient do not appear in both training and
   validation/test"). Measured with an IID split over the patients' spectra (3 stratified folds, reference library
   in training):
     LR with library:  IID 0.163 / 0.150 / 0.181 (mean 0.165); grouped repeat 0: 0.216 / 0.189 / 0.267 (mean
                       0.224); all 60 grouped folds: 0.242.
     LR patients only: IID 0.091 / 0.104 / 0.100 (mean 0.099); grouped repeat 0: 0.215 / 0.106 / 0.424 (mean
                       0.248); all 60 grouped folds: 0.321.
   The IID split lowers the loss by 26-69%, and it reverses the issue-3 ranking: under IID the model without the
   library wins (0.099 against 0.165); under grouped folds the model with it wins (0.242 against 0.321). Patients
   carry signal of their own, which a split over spectra would reward. The builder's macro-AUC split gap (0.997
   against 0.992) hides this.
   The use case also sets the unit: one spectrum per prediction, each patient counted once. The source votes over
   10 spectra per patient, but a per-patient score would saturate here: the patient accuracy from the mean
   probability is 1.000 for both LR variants with the library, on every patient in every split (kNN 0.967,
   patients only 0.975). SPLIT-23 holds as declared (prediction_unit row, context none).
   Remedy: none.

2. P4: THE GROUP UNIT AND HIDDEN GROUPS ACROSS PATIENTS. (SPLIT-24 Must, SPLIT-30 Must)
   - The patient is built exactly from the source's own indexing (SPLIT-24's "consecutive blocks in the raw file
     order"). Every 400-row block (2018) and 100-row block (2019) holds one treatment code (50 of 50).
   - Small inaccuracy in the comments, no effect on the split: the groups are not stored in code order (2018 file:
     codes 0,6,5,3,2; 2019 file: 0,5,6,3,2), although the comment in _clean and the README say "the groups in code
     order". The split only uses the blocks.
   - Look-alike pairs (the claim auditor's pairwise AUC below 0.65): 2019-06/07/08/09 (penicillin, AUC
     0.52-0.69), 2018-06/07 and 2018-07/10 (daptomycin), 2018-12/13 (penicillin), 2018-22/23 (TZP). Measured
     effect: over the 20 repeats, I compared each patient's LR loss when its look-alike trains with its loss when
     the look-alike sits in the same test fold. Across all 448 same-class pairs this difference lies between
     -0.104 and +0.076 (5-95%).
       All look-alike pairs fall inside that band (-0.042 to +0.008) except 2018-22/23 (TZP): 0.483 -> 0.273 and
       0.236 -> 0.099 (-0.21 and -0.14). Patients only: the same, -0.21 and -0.13.
     Reading (SPLIT-30): the source describes 25 distinct patients per file, one isolate each. Two patients
     carrying one hospital strain (clonal spread of P. aeruginosa) is something new patients do have, so the
     context gives no shared entity that new data would lack. Effect on the mean: about 0.007 of 0.242 (the pair
     shares a test fold in 4 of 20 repeats).
   Remedy: none. A note in the group definition is optional.

3. P4: IS A PATIENT'S ISOLATE A REFERENCE STRAIN? No evidence that one is.
   - Provenance: the reference set is the source's library of 30 isolates (config ATCC_GROUPINGS; "over 94% of
     the infections at Stanford Hospital 2016-17"). The patients come from Palo Alto VA (2018) and Stanford
     (Feb-Mar 2019). The 2019 patients postdate the reference study's preprint (arXiv 1901.07666, January 2019).
     Supplementary Table 1 (strain sources) was not readable: its tables are images.
   - Data: I compared each patient with every reference isolate of its treatment group (fine-tuning + test files,
     2 s), using a PCA-20 logistic regression with 100 spectra per side. For each patient the closest reference
     isolate separates at ROC AUC 0.83-1.00 (median 0.998). As calibration, two cultures of one reference strain
     separate at median 0.81 (min 0.51). No patient falls below that median. The closest two, 2019-09 (0.830)
     and 2019-10 (0.847), both against E. faecalis 2, lie inside the two-culture range, so a shared strain cannot
     be ruled out for them.
   - The library is never tested. A shared strain would therefore mean a test patient whose strain the lab's
     library holds, which is realistic and not a leak across the split.
   Remedy: none.

4. P4/P6: THE REFERENCE LIBRARY IN TRAINING (builder's issue 3). The test is unchanged; what the score rewards
   changes. (SPLIT-1; issue 3 is a weighing call, TP-6 / USE-1)
   - Unchanged: every test row is a patient, the same 50 patients either way, so the split still measures a new
     patient's isolate. The library is identical in all 60 training sides, so all fold-to-fold variation comes
     from the patients.
   - (a) Prior shift and classes never tested. The library is 88-90% of each training side. It sets an 8-class
     prior: daptomycin 3.3% and TZP 6.7% of the library rows, against 20% of the test patients each. It also
     adds three groups no test fold holds.
       LR with library puts 2.0% of the weighted probability on the three untested groups.
       Renormalising its probabilities over the five patient groups lowers the loss from 0.242 to 0.197 (lower
       on 60/60 folds, 50/50 patients).
       A Bayes prior correction to the patients' training shares lowers it to 0.186 (57/60 folds).
     About a fifth of the score with the library is therefore how a model handles the library's class shares and
     the untested groups. A model can learn this from training (clinical spectra are recognisable and their
     class shares are visible). The effect is larger than the gap between two good models (LR C=1 against
     C=0.01: 0.017).
   - (b) The gain from the library rests on two patients. With against without: 0.242 against 0.321, lower on
     41/60 folds and 20/20 repeats. But only 23/50 patients score better with it, and the 95% interval of the
     patient bootstrap is [-0.249, +0.054]. Two vancomycin patients give 144% of the net gain: 2018-16 (5.45 ->
     1.97) and 2019-20 (2.97 -> 0.81). Without them the library hurts on balance. Same pattern for LR C=0.01:
     0.225 against 0.321, 22/50 patients, interval [-0.291, +0.048].
   Remedy: none required from the split. If (A) stays, the mildest step is a sentence in the notes: the
   library's class shares and its three untested groups are part of what the log loss scores (about 0.05 of
   0.24 for a linear model), and its benefit comes from a few atypical patients. (B), patients only, removes the
   prior shift but loses those patients. Both test the same thing, so the call stays the curator's.

5. P6: FEW PATIENTS, NOISE ACROSS FOLDS AND SEEDS. (TP-5 Must, TP-8 Must; warning groups_test_groups_few)
   - Structure, all 60 splits: 16-17 test patients per fold, 3 or 4 of each of the five groups (every fold),
     2,900-5,000 test rows. Every patient is tested once per repeat. No isolate is on both sides. The 66,000
     library rows are in every training side and never tested. Patient training rows: 7,500-9,600 per split.
   - Noise (LR with library, 60 folds): mean 0.242, fold SD 0.076, range 0.090-0.418.
       SE of the mean over the 20 repeat means: 0.003.
       SE from the 50-patient sample (bootstrap over patients, stratified by group): 0.050, 18x larger.
     The repeats reshuffle the same 50 patients and add no evidence about new patients (task_probes.md, "A
     grouped task"). Same for the other models: C=0.01 0.002 against 0.040; kNN 0.012 against 0.212; patients
     only 0.010 against 0.114.
   - Concentration: one patient (2018-16, vancomycin) has a mean loss of 1.97, eight times the average. The
     worst patient carries a median 28% (max 65%) of a fold's loss, and 3 of 17 patients carry half of it. The
     worst 5 of 50 carry 45% of the total. 9 of 50 patients have a mean loss above 0.5.
   - Model gaps:
       LR against kNN (0.37): resolved (bootstrap 95% [-0.77, -0.12]; 60/60 folds).
       LR C=1 against C=0.01 (0.017): the same order on 20/20 repeats, but [-0.009, +0.051] under patient
       resampling (29/50 patients).
       With against without the library (0.079): see finding 4.
     The benchmark will therefore rank close models consistently on these 50 patients (a small repeat SE), but
     differences below about 0.03-0.05 do not show generalisation to new patients.
   - Reading against the precedents:
       TP-8: no short class (10 patients per group).
       16-17 test patients per fold, more than parkinsons (10-11 per fold, 2-3 of a class, retired) and huesken
       (10 genes per fold, kept).
       The signal across patients is clear: the builder's permutation test, and the class shares at 1.9 against
       0.24.
     Not Too Small by the precedents, but borderline (3-4 units per group per fold, 10 in total).
   Remedy: none in the split; it cannot add patients, and more folds or repeats add no evidence. Accept
   groups_test_groups_few with the patient-bootstrap SE (0.05 on 0.24) added to the builder's evidence. Issue 2
   stays a weighing call.

6. P4, minor: STRATIFICATION BY TREATMENT GROUP holds; YEAR is not stratified. (SPLIT-1)
   - 3 or 4 patients of every group in every test fold (60/60).
   - Not stratified by year: 4-13 of a fold's patients come from 2019, and a group's 3-4 test patients include 0-4
     from 2019. 2019 patients score worse (mean patient loss 0.288 against 0.198), but a fold's number of 2019
     patients barely moves its score (r = 0.19 with LR's fold loss, r^2 0.04).
   - Pooling the two years matches the source's second stage: the notebook continues fine-tuning on 2019 patients
     with 2019 patients held out. The splits_comment's "tests the 2019 patients after training on 2018" leaves
     that stage out. The harder transfer from 2018 to 2019 (builder: 90.1% per spectrum, log loss 0.51) is a
     variant, not the use case: the same lab measures both.
   Remedy: optional, stratify on treatment x year inside _make_splits (a key built on the clinical frame, no new
   shipped column). Not needed.

7. P4 EVIDENCE (EV-2; SPLIT-4): the comparison of 74.0% against 93.1% for the 30-isolate task (option B)
   overstates the culture effect.
   - The 93.1% hold-out drew about 95% of its spectra from the reference file: 1 s, and the culture of the
     60,000 training rows. It mixes "same culture" with "same file and measurement setting".
   - Hold-outs of the test file's own setting (2 s, fine-tuning file, 3 stratified folds of a third each),
     scored by the same model as the separately cultured test file:
       Reference + 2/3 of fine-tuning: held-out fine-tuning 77.5%, test file 72.1% (+5.4 points).
       2/3 of fine-tuning only: 90.6% against 76.5% (+14.1).
       Reference minus 3,000 + fine-tuning: reference hold-out 93.8%, test file 74.3% (+19.5).
       Reference alone: test file 43.2%, fine-tuning file 45.5%. The 1 s -> 2 s file shift is large.
   - So the culture is worth about 5-14 points, and most of the rest of the 19-point gap is the file.
   - The framing (A) still stands. It rests on USE-5 and SPLIT-4: a new patient is a new strain, while the
     source's test file holds new cultures of the same 30 strains (a known entity), and the size of a gap never
     decides (SPLIT-4).
   - What is wrong is the sentence "so a split over spectra mostly rewards knowing the culture" in
     curation_comments, in issue 1 and in claim 21.
   Remedy: reword it with the numbers from the test file's own setting (77.5% against 72.1% for the same model;
   90.6% against 76.5% trained on the fine-tuning file alone).

NOT FOUND / NOT CHECKED
- No temporal component to audit: no time column. The two collection years enter only as finding 6.
- Not checked: whether 2018 is a 1 s or 2 s file, and how many measurement days lie behind each species. A
  within-year day batch by species would be shared by the training and test patients of one group (the
  builder's caveat). The 2018 -> 2019 transfer bounds it.
- Not run: LightGBM or tuned models over all 60 splits. The noise figures come from three linear and
  neighbour models.

</details>

<details><summary>bacteria_id_raman: domain practitioner</summary>

bacteria_id_raman: domain practitioner report (2026-11-09)

Role played: the clinical microbiology laboratory that measures Raman spectra of a patient's isolate, and the
physician who picks the empiric antibiotic from what the lab reports, before culture-based identification and
susceptibility testing are back.

VERDICT
-------
Fit: approximate, as declared (USE-8). One-sentence reason: the 50 patients' spectra come from cultured colonies of five
species, one per treatment group, so the test asks a lab to tell five known species apart with a fixed drug per species
at a stage where culture has already happened, not to pick a drug for any pathogen without culture.
Metric: partly scores my decision, and is the best declarable choice. Keep the patient-weighted log loss (issue 4,
option A). It is a proper rule on the probability (MET-8) and counts each patient once (MET-17). It ranks four untuned
models like my patient decisions (Kendall tau 0.94 against the 10-spectrum vote accuracy, 0.91 against the rate of
patients whose drug would not cover the pathogen). It scores one spectrum, not my per-patient decision, and it cannot
weigh the unequal costs of a wrong drug, because no source fixes them (MET-7).
Issues: 1 option A (treatment group); 2 keep, with a note on how few patients drive the score; 3 option A (the library
is what a lab has); 4 option A. No change to the definition's code is needed. Notes and fit_reason should name three
gaps they do not name yet (below, "What an expert would change").

HOW THE DECISION IS MADE TODAY (domain)
* A patient with a suspected bloodstream infection gets empiric antibiotics when cultures are drawn, chosen from the
  syndrome, the patient's risk factors and the local antibiogram. Inappropriate empiric therapy roughly doubles
  mortality in bacteraemia (pooled OR 2.06, 198 studies, 89,962 adults; Hung et al. 2022).
* When a blood culture flags positive, the lab does a Gram stain within 1-2 h. The physician then narrows or widens the
  therapy by the Gram result, then by the species, then by the susceptibility. Species come from a multiplex PCR panel
  (FilmArray BCID: Gram stain to identification in 1.3 h against 22.3 h in the control arm of a randomised trial; the
  panel also reports mecA, vanA/B and carbapenemase genes) or from MALDI-TOF on the broth or on a colony. MALDI-TOF on
  a colony gives the species in minutes: 98.2% correct over 2,263 clinical isolates of 61 species in the Bruker 510(k)
  study. Susceptibility takes another 16-48 h.
* Raman's promise (Ho et al. 2019) is identification without culture, from a few cells, within hours. The data do not
  reach that moment. The clinical isolates "were cultured on blood agar plates" and the "biomass from a single colony"
  was dried on a gold substrate (Methods). The source simulates few cells by voting over 10 spectra.

Q1. INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
* What ships: one spectrum, background-corrected and scaled per spectrum. I have it at the prediction point. No shipped
  input is one I would lack, and no file, year or site marker ships (correct: a new patient comes with none).
* Inputs I would always have that are missing (none can be added from this source):
  - The Gram stain. Whenever a culture bottle flags, it is known before any identification. By my reading of the
    classes (Meropenem, piperacillin-tazobactam: Gram-negative; vancomycin, penicillin, daptomycin: Gram-positive),
    45-52% of the per-spectrum errors of four untuned models cross the Gram line (mean per model, 6 shipped splits).
    Examples: Vancomycin (Staph) read as piperacillin-tazobactam, and Meropenem (E. coli) read as penicillin. A lab
    would never make those errors, because the stain rules them out.
  - Several spectra per isolate (at least 10 in the source's culture-free simulation, 100-400 as measured). The task
    predicts each spectrum alone. That is right for the building block, and the weight makes each patient count once.
  - The specimen type, prior MRSA or ESBL colonisation, and hospital or community onset. These choose the drug within
    a species. They are not in the label (Q2), so their absence does not bias the task as defined.

Q2. THE TARGET (issue 1; USE-5)
* What I act on: as the lab, the species, with resistance markers when I have them. As the physician, a drug that
  surely covers the pathogen and is no broader than needed. The 30 reference isolates are of no use to me: "E. coli 1"
  against "E. coli 2", or MSSA 1/2/3, changes nothing I do. Option B fails USE-5.
* The treatment group is the closest of the three labels to my decision, so option A. For the 50 test patients it
  equals the species: "each species corresponds to a different treatment class" (Fig. 4). `config.py` comments the
  groups as Meropenem # E. coli, TZP # PSA, Vancomycin # Staph, Penicillin # Strep + E. faecalis, Daptomycin
  # E. faecium. So the test is a 5-species identification under a drug name. A species label would test exactly the
  same thing. The group label matters only for how the reference isolates are pooled in training.
* It is still a proxy. The drug is a fixed lookup per species, while in practice the resistance within a species
  decides it. Every S. aureus maps to vancomycin, and the paper itself calls vancomycin "not considered optimal" for
  MSSA. Its clinical MRSA/MSSA classifier reaches only 65.4 +- 6.3%, so Raman does not settle that decision here. For
  E. coli, ESBL status decides between ceftriaxone and a carbapenem. This gap belongs in fit_reason.
* What I want back is a probability over the groups, not a class. "70% Enterobacterales, 25% Pseudomonas" makes me
  pick the agent that covers both. That supports a proper score on probabilities (MET-8).

Q3. ONE ROW, ONE DECISION; THE TEST DATA (USE-10, SPLIT-4, SPLIT-23)
* One row is one spectrum, while I decide once per patient. The isolate weight makes each patient count once, which
  is right (MET-17). Predicting per spectrum, with the patient-level vote left to the user, matches the source's
  culture-free premise of a few cells.
* New patients are held out whole, which is right: a patient brings a strain never measured (USE-10, cold start;
  SPLIT-4).
* The test data differ from what I would face in three ways:
  (a) The case mix is closed and balanced: exactly 5 species, 10 patients each. Real isolates are open-set and skewed:
      E. coli and S. aureus dominate, and Klebsiella, coagulase-negative staph (often contaminants), Candida and mixed
      cultures also occur. fit_reason names this ("a real patient may carry any pathogen").
  (b) Years and sites are pooled. A 2018 Palo Alto VA patient is tested with 2019 Stanford patients in training. A lab
      goes forward, from its library and earlier patients to the next patients. Measured with PCA-100 logistic
      regression, the library and the 2018 patients trained:
        forward 2018 -> 2019 (25 patients): weighted log loss 0.368, per-spectrum accuracy 0.900, patient accuracy
                                            25/25
        pooled grouped CV (6 shipped splits): weighted log loss 0.229 (0.148-0.312)
      So the shipped split is about 1.6x more optimistic per spectrum, with the same patient decisions. The source
      itself fine-tunes within each year, so I would only note this, not change the split.
  (c) Cultured colonies rather than direct specimens (fit_reason names it). At this stage MALDI-TOF is the comparator.

Q3b. WOULD I HAVE THE REFERENCE LIBRARY? (issue 3)
Yes. Every identification system starts from a library of reference strains (the MALDI-TOF databases do), and the
source pre-trains its clinical model on exactly this library. A library measured under other settings (1 s against
2 s, after "optical efficiency" degraded) is ordinary instrument drift that a real lab lives with. So option A: the
library in training, never tested.
Measured (my probe, untuned): the library alone does not carry a lab. Trained on the 66,000 library spectra only and
tested on all 50 patients:
  PCA-100 logistic regression: per-spectrum accuracy 0.786, 10-spectrum vote 0.842, weighted log loss 0.883
  LightGBM:                    per-spectrum accuracy 0.712, 10-spectrum vote 0.788, weighted log loss 1.019
  Patient drug decisions that would miss the pathogen: 6.9% and 15.3%
The source's pre-trained CNN reached 89.0% before fine-tuning on patients and 99.0% after. Local patients are needed,
as in practice (labs add local strains to their libraries), so the task tests how a method combines a shifted library
with a few local patients. That is a real problem.
Side effect: the three groups only the library holds (caspofungin, ceftriaxone, ciprofloxacin) get 1-5% of the
probability on patient spectra in CV (10.6-12.0% with the library alone). Renormalising over the five tested groups
lowers the declared score by 2-40% (mean 6% kNN, 14% LightGBM, 17-19% linear) and swapped the order of the two linear
models on 1 of 6 splits (tau 0.94 with the declared). This is a real open-set cost (Candida, Salmonella and
S. pneumoniae do occur in patients), so I would keep it and name it in the notes.

Q4. WOULD I USE THIS MODEL? (issue 2; TP-5)
* Not as a clinical identifier at the colony stage: MALDI-TOF does that in minutes, over hundreds of species. I would
  not trust any clinical claim from 10 patients per species and 5 species. A cleared identification system is
  validated on thousands of isolates: 2,263 isolates of 61 species for one Bruker claim, 4,399 isolates in the
  follow-up study.
* As a benchmark of how methods identify the class of a new patient's spectrum, I would trust the ranking of model
  families. The gaps are large: weighted log loss linear 0.21-0.23, LightGBM 0.34, kNN 0.59. Builder: LightGBM - random
  forest +0.349 (paired SE 0.009). I would not trust its absolute numbers or small gaps.
* Measured: a fold's score rests on one or two patients. The worst single patient carries 16-78% of a fold's declared
  score (per-model ranges: LightGBM 16-32%, linear 16-51%, kNN 32-78%), and the worst two carry 30-85%. One kNN
  patient averaged a log loss of 5.3 per spectrum. The hard patients recur (2018-16 Vancomycin 1.89; 2019-21
  piperacillin-tazobactam 0.96; 2019-14 Daptomycin 0.81, PCA-100 LR), and the 20 repeats reshuffle the same 50
  patients. So the dataset-level score is largely "who gets those few patients right".
* This is not `Too Small` under TP-5. Each group has 10 patients in all and 3-4 per fold, against parkinsons' 2-3 per
  fold, and the signal across patients is strong. Keep, but the notes or the accepted `groups_test_groups_few`
  warning should carry the worst-patient share, so a user reads small score gaps with caution.
* What would make me trust it more: a forward test on a later cohort from another site (the 2018 -> 2019 numbers
  above), more species including Candida and contaminants, and the Gram stain as a given input.

Q5. DOES THE DECLARED METRIC SCORE MY DECISION? (issue 4; MET-1, MET-6 to MET-10, MET-17)
Declared: log loss over spectra, each weighted 1 over its patient's spectra (fallback, origin named). Compared on 6
shipped splits (repeats 0-1) for 4 untuned models (PCA-100 LR, LR C=0.01, kNN on 30 PCs, LightGBM). Taus are against
the declared ranking, mean over splits.

| Candidate | Mean per model | Tau | Reading |
|---|---|---|---|
| Accuracy per spectrum (patient-weighted) | 0.879-0.929 | 0.56 | A threshold metric with no threshold or costs fixed (MET-6). It ranks the four models least like my patient decisions, and treats a Staph read as Pseudomonas like a Pseudomonas read as E. coli. Reject. |
| Accuracy per patient, majority vote over 10 random spectra (the source's score) | 0.960-0.993 | 0.94 | It ranks like the declared metric but sits at its ceiling. One patient is 6% of a fold, and the two linear models differ by 0.001-0.007 (MET-10: resolution and ceiling). It would need a per-patient prediction protocol the scorer does not have. Reject as declared; worth naming as the original. |
| Patient log loss of the mean probability over 10 spectra | 0.103-0.233 | 0.61 | Closer to my decision unit. It ranks the two linear models opposite to the declared metric on 6 of 6 splits (PCA-100 LR better by 0.018-0.033), but also opposite to the vote and the coverage rate, which side with the declared metric. A mean of probabilities rewards sharper single-spectrum models; it is no cleaner. |
| Expected cost of a wrong drug | — | — | What I really want. My coverage reading (illustrative, not a source matrix): a drug that does not cover the pathogen (penicillin for E. faecium, vancomycin for Pseudomonas) costs far more than one that is broader than needed (vancomycin for MSSA, daptomycin for E. faecalis). As the share of patients whose 10-spectrum decision would leave the pathogen uncovered: 0.3% (LR C=0.01), 0.6% (PCA-100 LR), 2.3% (LightGBM), 3.2% (kNN), tau 0.91 with the declared. The paper only says MRSA-as-MSSA is "more severe" than the reverse and fixes no matrix, so MET-7 forbids declaring one. |

So the declared metric is the right family (a proper rule, MET-8; one vote per patient, MET-17) and ranks like my
decisions, with far more resolution than the vote. It scores the single-spectrum probability rather than my
per-patient choice, and it cannot express the asymmetric cost of an uncovered pathogen, which no source fixes.
"Partly", and keep it.
If the curator wanted the decision itself: a cost matrix from a published guideline mapping (an uncovered pathogen
against a broader-than-needed drug), scored on the patient's aggregated probability. Only a source that fixes those
costs would allow it (MET-7). I found none.

GAPS BETWEEN THE DATASET AND THE REAL DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Cultured colonies, not direct specimens. The moment the data support is after culture, where MALDI-TOF or a PCR
   panel already gives the species. Named in fit_reason; the comparator is not.
2. A closed, balanced set of 5 species, one per group. The real case mix is open-set and skewed. Named in fit_reason.
3. The label is a fixed drug per species: resistance (MRSA/MSSA, ESBL, VRE), which decides the drug within a species,
   is outside it (the paper's clinical MRSA/MSSA accuracy is 65%). Not named.
4. The Gram stain, which a lab always has, is missing. It would remove 45-52% of the per-spectrum errors. Not named.
5. Pooled years and sites against a forward deployment: log loss 0.229 pooled against 0.368 forward (PCA-100 LR), the
   same patient decisions. Not named.
6. Per-spectrum prediction against a per-patient decision: handled by the weight; the declared metric ranks like
   patient decisions (tau 0.91-0.94).
7. Probability on the three groups only the library holds: 2-40% of the declared score. A real open-set cost; not named.

WHAT AN EXPERT IN THE DOMAIN WOULD CHANGE (no code change needed)
* fit_reason: add that the drug is a fixed lookup per species without resistance, and that at the culture stage of
  the data, MALDI-TOF or PCR panels give the species in minutes to an hour.
* curation_comments: add the missing Gram stain (with the cross-Gram share of errors), the forward 2018 -> 2019 number,
  the worst-patient share of a fold's score, and the mass on the three groups only the library holds.
* Record the presumed species of the five patient groups from `config.py`'s comments (E. coli, P. aeruginosa, Staph,
  Strep or E. faecalis, E. faecium), marked as inferred until Supplementary Table 2 is read. The current notes say the
  species are not listed.
* Keep the framing (issue 1 A), the library in training (issue 3 A), the patients (issue 2, keep) and the metric
  (issue 4 A).

RULES CITED
USE-1, USE-3, USE-5, USE-6, USE-8, USE-9 (no other use case is mirrored directly: Raman identification of a colony
still meets a closed 5-species test), USE-10; SPLIT-4, SPLIT-23; TP-5, TP-8; MET-1, MET-6, MET-7, MET-8, MET-10,
MET-11, MET-17.

SOURCES
-------
* Ho et al. 2019, Nat Commun 10:4927, PMC copy https://pmc.ncbi.nlm.nih.gov/articles/PMC6960993/ and arXiv
  https://ar5iv.labs.arxiv.org/html/1901.07666. Methods (culture, colony biomass, 1 s / 2 s), Results ("the priority
  for physicians", Fig. 2 "misclassifications are mostly within antibiotic groupings", Fig. 4, MRSA/MSSA 65.4%,
  pre-trained 89.0% -> 99.0%).
* The source repository's `config.py` and `3_clinical_finetuning.ipynb`, local copies in
  the run folder (the group comments, the 10-spectrum vote, n_classes = 8).
* Hung, Lee, Ko 2022, Front Med 9:869822, inappropriate empirical antibiotics and mortality in bacteraemia:
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9197423/
* Banerjee et al. 2015, randomised trial of rapid multiplex PCR identification of positive blood cultures:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4560903 ; UCSF rapid diagnostic test guideline:
  https://idmp.ucsf.edu/sites/g/files/tkssra4251/f/Antibiotic%20Treatment%20RDT%20Guideline%202020%20Web.pdf ;
  MALDI-TOF and rapid AST in sepsis: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4881997/
* Bruker MALDI Biotyper CA multicenter evaluation (2,263 Gram-negative isolates, 98.2% to species):
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4631355/
* Builder's report and probes: the run folder, probes/shipped_compare.json.

MY PROBES (scratch, read-only on the repository)
dp_probe.py (-> dp_probe.json, dp_probe.log): 6 shipped splits x 4 untuned models, plus
  the library alone -> 50 patients. The arrays were read from the claim auditor's cache
  (X.npy, meta.pkl), built from the container.
dp_summary.py (-> dp_summary.log): means, rankings, taus.
dp_confusion.py (-> dp_confusion.log): patient-weighted confusion, worst patients, forward
  2018 -> 2019.
The coverage table in dp_probe.py is my clinical reading, for illustration only. It is not proposed as a metric.

</details>

<details><summary>bacteria_id_raman: blind review</summary>

BLIND REVIEW: bacteria_id_raman (target: empiric_treatment, 8-class, grouped by isolate, 20x3 folds)
Reviewer worked only from clean_room/ (data.parquet, task.md) and the public sources linked there
(Nature Comms paper via PMC, github.com/csho33/bacteria-ID incl. config.py, notebooks and the Dropbox
data linked in its README, the RamanBench arXiv paper, the raman-data PyPI page). No other local file was opened.
Scratch:  (baselines.py, res_*.csv, src_npy/ with the downloaded source arrays).

VERDICT
Include with changes: the spectra and labels are real and match the source one-to-one, and the clinical
question is real. But the isolate-grouped 3-fold split leaves 3 of the 8 classes (14% of rows) with no
usable training signal, and it does not match how the model would be used. The split has to be redesigned
before the scores mean anything.

WHAT THE TASK IS
Ho et al. 2019 (Nat Commun 10:4927). Spontaneous Raman spectra (633 nm, monolayers of cultured colonies,
1000 points over 381.98-1792.4 cm^-1, 5th-order polynomial background removed, each spectrum min-max
normalised). Each row is one spectrum from one isolate:
  - 30 reference isolates x 2200 spectra (2000 training + 100 fine-tune + 100 test spectra; the test
    spectra come from "separately cultured samples").
  - 25 patient isolates from 2018 x 400 spectra (Palo Alto VA).
  - 25 patient isolates from 2019 x 100 spectra (Stanford, Feb-Mar 2019).
The target maps species to the recommended empiric antibiotic, using the source's config.py ATCC_GROUPINGS.
The use case: a microbiology lab, hours after a colony grows, picks the first antibiotic before culture
identification and susceptibility results arrive. In the paper's words, "the priority for physicians is
choosing the correct antibiotic". This is a real decision, shown in a proof-of-concept study. The paper
predicts per patient by majority vote over 10 spectra; this table predicts each spectrum on its own,
which is a fair unit for a benchmark.

PROVENANCE CHECK (passed)
I downloaded the source .npy files and matched every row by value. All 78,500 parquet rows match exactly
one source row (60000 reference + 3000 fine-tune + 3000 test + 10000 from 2018 + 2500 from 2019), with no
row missing or repeated. The isolate and target labels agree 100% with config.py (STRAINS, ATCC_GROUPINGS,
antibiotics). The column names agree with wavenumbers.npy.
The patient IDs are not in the source. They come from contiguous row blocks (400 or 100 rows), which is
the authors' own convention in notebook 3: "start_idx = 5 * 400 * group_idx + 400 * patient". Two checks
support it:
  - Within each treatment group, the blocks are distinguishable. Patient-ID accuracy is 0.56-0.98 against
    a chance of 0.20 (0.29 for the 2019 Penicillin group). With shuffled IDs it is 0.18-0.24.
  - A classifier trained on reference isolates assigns the patients to the right species: Meropenem to
    Enterobacterales, Daptomycin to E. faecium (0.90-0.99), Penicillin to E. faecalis, Vancomycin to
    S. aureus, TZP to P. aeruginosa.
There are no exact duplicate spectra, no missing values and no constant columns. All values lie in [0, 1].
The data are real and the labels are right.

BASELINES (PCA60+logistic regression and LightGBM, 300 trees; training subsampled to <=400 spectra per isolate)
  split                                        row acc LR / LGBM       isolate-vote acc LR / LGBM
  task's grouped 3-fold (SGKF, 2 repeats)      0.76 (0.66-0.85) / 0.70 (0.60-0.79)   0.91 / 0.87
  random rows (leaky, for contrast)            0.97 / 0.91                           1.00 / 0.96
  references always in train, patients grouped 3-fold x3   0.94 (0.87-0.98) / n.a.   0.99 / n.a.
  paper-style: reference + 2018 -> 2019         0.90 / 0.81                           1.00 / 0.92
  reference only -> all patients                0.73 / 0.62                           0.82 / 0.62
There is real signal, the task is not trivial, and grouping by isolate matters (0.97 vs 0.76).

CONCERNS, MOST TO LEAST SERIOUS

1. Under isolate-grouped CV, three classes cannot be learned. This alone makes the current split unfit.
   Number of isolates per class: Ciprofloxacin 1 (S. enterica), Caspofungin 2 (C. albicans, C. glabrata),
   Ceftriaxone 2 (S. pneumoniae 1/2). The others have 11-18.
   - Ciprofloxacin: a single isolate can never be in train and test at the same time. It is in test in
     20 of 20 repeats and is then absent from train, so its recall is 0 by construction (2200 rows).
   - Caspofungin: StratifiedGroupKFold put both Candida isolates in the same test fold in both repeats I
     ran (r0 fold 1, r1 fold 1). Holding out one isolate at a time, C. albicans to C. glabrata transfer
     is only 0.25.
   - Ceftriaxone: even with the other S. pneumoniae in train, recall is 0.07 / 0.12 (leave one isolate out).
   Mean recall under the grouped split, LR / LGBM: Ciprofloxacin 0.00 / 0.00, Caspofungin 0.00 / 0.00,
   Ceftriaxone 0.15 / 0.00.
   I simulated the 20x3 splits. In about 45% of the 60 splits the test fold has rows whose class is
   missing from train. In the worst split that is 24% (SGKF) or 31% (plain GroupKFold) of the test fold.
   Any macro metric (balanced accuracy, macro-F1, multiclass AUC) loses 3/8 of its range to noise from
   which fold an isolate lands in.
   Fix: see concern 2. If the split must stay "grouped by isolate", drop the classes with 2 or fewer
   isolates (S. enterica, both Candida, both S. pneumoniae: 11,000 rows). That leaves 5 classes and 75 groups.

2. The split does not match the use case. In the paper (and in any deployment), the reference library
   covers every target species, and the new unit is a new patient's isolate of a known species. Holding
   out whole reference isolates often holds out a whole species: 14 of the 30 reference isolates are the
   only isolate of their species. The model then has to infer a prescribing convention for a species it
   has never seen. For example, S. enterica is labelled Ciprofloxacin while every other Enterobacterales
   species is Meropenem, and E. faecium is Daptomycin while E. faecalis is Penicillin. Spectra cannot
   carry that convention.
   Fix (preferred): keep all 30 reference isolates in train in every fold and run grouped k-fold over the
   50 patient isolates (LR row acc 0.94, isolate vote 0.99). Alternatively, use the paper's protocol:
   reference + 2018 to train, 2019 to test (0.90 / 0.81).

3. Very unequal weights across isolates. There are 80 independent units, but a reference isolate has 2200
   rows, a 2018 patient 400 and a 2019 patient 100. The 30 reference isolates make up 84% of rows and of
   the average test fold, and test folds range from 15,400 to 38,000 rows. A row-level metric therefore
   weights one reference isolate 22 times as much as one 2019 patient, and the score swings 0.60-0.85
   between folds for the same model.
   Fix: cap each isolate at about 100-400 spectra (the spectra within an isolate are near-replicates, so
   little is lost), or weight rows as 1/(rows of their isolate). This also cuts the table from
   78,500 x 1000 (785 MB) to about 10-25k rows, which matters for row-limited tabular foundation models.

4. The group column leaks the target if any method reads it.
   - Reference names contain the species, which fixes the label ("reference S. enterica" is Ciprofloxacin;
     "reference C. albicans" is Caspofungin).
   - Patient IDs are numbered in class blocks. 2018-01..05 are Meropenem, 06..10 Daptomycin, 11..15
     Penicillin, 16..20 Vancomycin, 21..25 TZP; 2019 follows a different block order.
   With grouped splits the ID itself is unseen at test time. But a text-aware or LLM-based tabular method,
   or a pipeline that parses the numbers, could read the label off it.
   Fix: replace the isolate values with opaque random IDs, and make sure the harness never passes the
   group column as a feature.

5. The table drops useful provenance. The source says which subset each reference spectrum came from:
   2000 training spectra measured at 1 s, versus 100 fine-tune and 100 test spectra from separately
   cultured samples. The paper notes that "measurement times for the reference fine-tuning and test and
   second clinical datasets were increased from 1 s to 2 s". The parquet has no column for subset,
   measurement time or year (the year survives only in the ID string). So the paper's own test protocol
   cannot be rebuilt from the table, and a split by time or batch is impossible without the ID string.
   I found no noise difference between the subsets (second-difference roughness 0.181 / 0.181 / 0.180),
   so this is minor for the grouped regime.
   Fix: keep a source_subset / collection_year column as metadata, not as a feature.

6. The target is a convention, not a measured outcome. The 8 groups follow one centre's 2019 empiric
   regimen, which is a deterministic function of species. Antibiotic resistance is ignored: MSSA and MRSA
   both map to Vancomycin. The paper itself says vancomycin "is also effective on MSSA but is not
   considered optimal treatment". That is acceptable as a benchmark label, but it should be described as
   "species group" rather than as a treatment outcome.

7. Minor points.
   - 7.1% of rows are not exactly min-max scaled (max < 1 or min > 0). This was probably scaled before
     cropping, it is present in the source, and it is harmless.
   - The 1000 columns are a highly collinear spectrum. Tree models on the raw columns trail a simple
     PCA + logistic regression (0.70 vs 0.76 grouped), so this dataset mostly tests how a method handles
     spectral features. Declare it as a spectral (special-feature) dataset.
   - The raman-data PyPI page calls this dataset "60,000 SERS spectra", but it is spontaneous Raman, not
     SERS.
   - RamanBench lists it as "Pathogenic Bacteria (30 classes, N=78,500)", which conflicts with how the
     5 clinical classes would be labelled. That is their issue, not this table's, but do not compare
     scores with RamanBench.
   Column types are fine: 1000 float64 columns, and isolate and target are categorical.

WHAT I COULD NOT CHECK
- The benchmark harness: whether it drops `isolate` from the features and whether it uses
  StratifiedGroupKFold or plain GroupKFold. I simulated both.
- The real patient-to-row assignment. It is inferred from the authors' notebook convention and a
  separability check, not from published per-patient metadata.
- Which 5 clinical species were used (in the paper's Supplementary Table 2, which I did not read). They are
  inferred from labels and spectra as E. coli, E. faecium, E. faecalis, S. aureus and P. aeruginosa.
- The full 20x3 run and stronger models (CNN, TabPFN, tuned GBDT). I ran 2 repeats with 2 simple models
  and subsampled training spectra.
- Whether the 2018 and 2019 clinical spectra used identical preprocessing to the reference set (the paper
  says they did).

</details>

<details><summary>bacteria_id_raman: task gamer</summary>

TASK GAMER REPORT: bacteria_id_raman (target empiric_treatment, 8 classes, isolate-weighted log loss, 60 grouped splits)

Verdict: there is no leaked column, identifier, row order or copy, but the task can be gamed by a lot through its test
rows. Rebuilding each held-out isolate from its unlabeled neighbours among the test rows, and adding the per-year class
make-up of the test fold, cuts the honest log loss by 36-40% (LR-PCA 0.153 -> 0.098, LightGBM 0.386 -> 0.231). Every
one of the 60 splits gets better.

Setup facts that matter
- 78,500 spectra: 30 reference strains x 2,200, 25 patient isolates from 2018 x 400, 25 from 2019 x 100. Every
  isolate counts the same in the metric (isolate_weight = 1/rows).
- Each test fold holds only patient isolates (16-17, which is 3-4 per class). All 30 reference strains are always in
  training, so every class is always in training. Patient isolates cover only 5 classes; Caspofungin, Ceftriaxone and
  Ciprofloxacin are reference-only.
- Honest baseline (work/baseline.py): untuned LightGBM on the 1,000 Raman columns. For speed, training rows are capped
  at 200 per isolate; every test row is predicted. Score 0.3857 (60 splits, per split 0.201-0.614).
  Random-column refit (work/baseline.py noise): 0.3870, per-split spread of the difference -0.012 to +0.013.
- Better honest model (work/lr_pca.py): Savitzky-Golay smoothing, then PCA-60 fitted on the split's training rows,
  then multinomial logistic regression. Each isolate is weighted equally and patient isolates x5. Score 0.1531
  (0.056-0.265). Random-column refit: 0.1531, spread -0.0009 to +0.0012.

Exploits ranked by gain

| # | Exploit | Script | Honest score | Exploited score | Gain (mean; per-split range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Rebuild the isolate from the test rows: average log-probs over each test row's 10 nearest test rows (PCA-20) | work/transductive2.py (geo10x1) | LR-PCA 0.1531 / LGBM 0.3857 | 0.1042 / 0.2606 | -0.049 [-0.088, -0.016] / -0.125 [-0.185, -0.086]; 60/60 splits better | No. The task gives group context 'none'. Other patients' rows are never available. | Score per isolate (prediction_unit=group, mean), or give group context to everyone |
| 2 | Test-fold make-up per collection year: test isolates per (class, year) = 5 minus the training isolates; year read off the spectrum | work/transductive.py (restrict5+yearcomp) | 0.1478 / 0.3818 (honest 5-class restriction) | 0.1311 / 0.3385 | -0.017 [-0.113, +0.027], 73% of splits / -0.043 [-0.183, +0.029], 80% | No. It needs the test fold's composition. | Hold out whole years (train ref+2018, test 2019, and the reverse) |
| 1+2 | Both together | work/transductive2.py (geo10x1+yearcomp) | 0.1531 / 0.3857 | 0.0977 / 0.2314 | -0.055 [-0.129, -0.008] / -0.154 [-0.301, -0.056]; 60/60 | No | Both fixes |
| 3 | PCA fitted on all rows, test rows included | work/lr_pca.py lrpca_pcaall all | 0.1531 | 0.1489 | -0.0042 [-0.0185, +0.0059], 68% (noise +-0.001) | No (it sees the test spectra) | None needed: small |
| - | Format: raw count range recovered from the value grid | work/quantum.py, make_format_feats.py | 0.1531 / 0.3857 | 0.1543 / 0.3824 | +0.0011 / -0.0033 [-0.023, +0.015] (inside noise +-0.012) | Yes (raw counts), but it carries session, not biology | Round spectra to 4 decimals (removes the grid) |

Upper bound on any isolate rebuild (true isolate, not allowed; work/oracle_group.py): geometric mean over the isolate
gives LR-PCA 0.0368 (0.0310 with #2) and LightGBM 0.179 (0.151). The row-level framing therefore leaves about 0.12
log loss on the table for anyone who can regroup the test rows.

Flaws that hurt an honest model
None found that a deployed model would avoid. The training set is dominated by reference rows (66k of 78.5k), which
include 3 classes that never occur in the test population, and 2018 isolates have 4x the rows of 2019 isolates. These
cost an honest model something, but a careful participant handles them with honest choices learned from the training
rows. Those choices, measured:
- Restrict to the classes seen among the patient training rows (work/transductive.py restrict5): LR-PCA
  0.1531 -> 0.1478 (-0.005, 60/60); LightGBM 0.3857 -> 0.3818 (-0.004, 60/60).
- Weight isolates equally and patient isolates x5: LR-PCA unweighted 0.1671 -> weighted 0.1531.
  LightGBM (work/honest_variants.py isow): 0.3857 -> 0.3544 (-0.031, per split -0.160 to +0.072, better in 75%).
- Train on patient rows only: worse (LR-PCA 0.1701, LightGBM 0.4506).
Exploits #1 and #2 are measured against both the plain and the restricted honest models above.

One flaw in the other direction: training rows from the future flatter the score. In a grouped random split, the 2019
isolates (collected Feb-Mar 2019 at another hospital) are in training when 2018 isolates are tested. Using them helps
a little (work/future_rows.py, 15 splits, 2018 test rows only): LR-PCA 0.1303 with the 2019 rows vs 0.1388 without
(-0.0085, per split -0.043 to +0.022). This is small and mixed. A year-wise split (fix to #2) removes it too.

Findings
1. Isolate rebuild from the test rows.
   The spectra are very noisy (SNR about 4). A single-spectrum model is right on most rows of an isolate but noisy on
   each one. The test rows of one isolate still sit together: in PCA-20 of the smoothed spectra, 75-86% of a test
   row's 10 nearest test rows come from the same isolate, and 94-97% share its label (work/iso_cluster.py,
   work/iso_space.py). Averaging log-probabilities over those 10 neighbours denoises each row's prediction. Every split
   improves, for both models. The kNN choice (k=10, one pass) is the best of 8 variants tried on the same splits, so
   the figure is slightly optimistic. k=5 and k=20 give -0.043 and -0.048 on LR-PCA, so the gain is robust.
   Clustering instead of kNN (KMeans, Ward; ARI 0.44-0.83) is worse (work/transductive3.py).
   In the source paper, the clinical protocol does aggregate 10 spectra per patient isolate, so same-isolate spectra
   are realistic at deployment. Other patients' spectra are not, and the task's own context is 'none'.
   Mildest fix: declare the prediction unit the isolate (mean aggregation in the scorer). That makes the aggregation
   everyone's baseline instead of a hidden trick. Subsampling test rows per isolate would only weaken the exploit.
2. Test-fold make-up per year.
   The paper and the data have exactly 5 isolates per class per year. A test fold is the complement of training, so a
   participant knows exactly how many test isolates of each class come from each year. The year can be read from one
   spectrum: a logistic model on training patients gives row-level AUC 0.993, accuracy 0.956 (work/year_clf.py).
   Multiplying the predictions by the per-year complement prior fixes many confidently wrong isolates. The same
   complement without the year gives nothing (LR-PCA +0.0006, LightGBM -0.007, mixed). With more folds the exploit
   grows: in leave-one-isolate-out it gives the answer outright.
   Mildest fix: hold out whole collection years. The test make-up is then the uniform 5 x 5 that the training
   patients already show, so nothing is left to infer.
3. PCA on all rows: a small transductive gain (-0.004, beyond the +-0.001 noise spread). It is not worth a fix, but
   preprocessing should be fitted on training rows.

Attacks that found nothing (numbers on all 60 splits unless stated)
- Row order: rows are shuffled. Next-row label agreement is 0.1886 vs 0.1879 expected at random, next-row same
  isolate 0.024, and class counts are flat over position deciles (work/order_flags.py).
- Identifiers: none. The index is a RangeIndex 0..78499 and no metadata comes with the parquet. 'isolate' is excluded
  by features(). Column names are wavenumbers. isolate_weight would reveal the year (1/400 vs 1/100), but it is a
  scoring column only.
- Exact copies: 0 duplicate spectra, also after rounding to 3 or 4 decimals.
- Near copies: a patient spectrum's nearest row lies in its own isolate only 8.7% of the time. Nearest own-isolate vs
  other-isolate distance (median) is 4.42 vs 4.20. The nearest other-isolate row has the same label 52% of the time,
  so a 1-NN label lookup is weak (work/nn_scan.py). Isolate means: every patient isolate's nearest isolates are of
  the same class and mostly the same year (work/iso_means.py). That is the signal the honest model uses (see "could
  not check").
- Formats: the values are integer counts divided by each spectrum's own count range (median 99.3% of a row's values
  lie on the 1/range grid). This recovers the raw intensity span per spectrum (38k to 37M), which differs by session;
  for example, 4 of the 5 2019 Piperacillin-tazobactam isolates sit at 105-235k (10th-90th percentile) while the
  other 2019 isolates reach 430-580k
  (work/quantum.py). Format-only features fitted on patient rows score 1.595 vs a random column 1.647 and uniform-5
  1.609 (work/fmt_patient.py). Added to the spectra they give LR-PCA +0.0011 (range only) / +0.0009 (7 format
  features) and LightGBM -0.0033 [-0.023, +0.015] vs a random-column spread of [-0.012, +0.013]: noise.
  2-5% of rows break the paper's [0,1] normalisation (max<1 or min>0). Their rates differ a little by class, but they
  are part of the format set above: no gain.
- Transforms over all rows: normalisation is per spectrum (uses only the row). No column is standardised over the
  table.
- Composition without the year (test prior = 10 minus training isolates per class): no gain (see finding 2).
- Train vs test: the test rows are always patient isolates and reference rows are always in training. That is a
  design choice, and the honest model can learn the patient-only class set from training rows (restrict5 above).
- Web: no competition, forum, "leak" or "magic feature" thread exists for this dataset. Ho et al. 2019 (Nat Commun)
  and RamanBench (arXiv 2605.02003) report no leak. The paper documents the per-spectrum min-max normalisation and the
  5-per-class-per-year clinical design that finding 2 uses.
- Source lookup: the kit keeps the published float64 values, so matching rows to the public arrays would recover the
  labels. That is true of any public dataset and is not ranked. It was not run: the Dropbox folder returns HTML to
  curl.

Could not check
- Whether the patient isolates of one class were measured in the same session. Same-class, same-year isolates are
  each other's nearest neighbours (e.g. 2018-06/07/10 Daptomycin at 0.32-0.44 vs median 2.2 over all isolate pairs), and
  the count range differs by class within 2019. This could be biology (same species) or session batch. If it is
  session, the honest score is inflated and the year-wise split would show it. Deciding fact: measurement date per
  isolate, or the species per patient isolate (paper Supplementary Table 2, not in the HTML).
- The source arrays, to see what the preparation changed (Dropbox download failed).
- LightGBM runs used at most 200 training rows per isolate (about 11k rows) for runtime. LR-PCA used reference
  rows capped at 200 per isolate plus all patient rows.

Scripts and outputs: work/ (common.py loaders; pred_*.npz per-split test predictions; transductive*_*.csv per-split
scores; log_*.txt run logs).

</details>

<details><summary>bacteria_id_raman: precedent check</summary>

Precedent check: bacteria_id_raman (precedent-checker, 2026-11-09)

Inputs read: the definition and README (df-large/datasets/_dev/tabarena-v0pt2/bacteria_id_raman/), the record
(df-large/curation/records/bacteria_id_raman.md), the builder report with draft issues 1-4, claims.md, the probe
outputs, the source's clinical notebook (src/3_clinical.ipynb), register.json (5,226 decisions, 34 flags), the
knowledge files of df-large, and the run folders of raman_mlrod and milk_nir_composition. No other phase-A report
existed when this was written (only work folders), so none is cited.

W = the worktree of the batch

**SUMMARY**

1. Framing (treatment group of a new patient's isolate, grouped by patient): CONSISTENT.
2. Few patients (3-4 per class per test fold, `groups_test_groups_few` accepted): DEPARTS, with a stated reason the
   rules do not accept (strong signal). A fact that does set it apart from parkinsons is in the data but not stated
   (stable scores). TP-5 is a Must, so a keep is an amendment of what "a handful" means, not an exception.
   Consistency prompt C1 below. The task probe's few_minority reading misses that, counted in the patient unit the
   score uses, every tested class is below the probe's own threshold of 5.
3. Reference spectra in every training side, never tested: CONSISTENT (the source's pre-training; same design as
   raman_mlrod). A new kind of `splits_rows_never_tested` acceptance (every earlier one was a 500k-cap trim, all
   dropped). One precision fix: the three never-tested classes are not force_2020's reading.
4. Metric (fallback log loss, each patient once): CONSISTENT with heart_disease, ljubljana_breast_cancer, covertype
   as applied, and with pancreatic_cancer_mouse_detection and dementia_prediction (MET-17). The "covertype deliberate
   accuracy" precedent behind draft issue 4 option (B) is STALE: Lennart set covertype to the fallback log loss on
   2026-10-21; MET-6's text still lists it as kept. Side point: the prediction unit (each spectrum, while the source
   votes over 10 spectra per patient) is justified in the draft by score saturation, a reason the 2026-11-05
   huesken/protein stance does not accept; the use case gives a better one. Prompt C2.
5. Spectrum declaration and preprocessing state: CONSISTENT (CLEAN-26, spectra.md; open_soil, milk_nir, raman_mlrod).

No drift found on TP-5, MET-17 or CLEAN-26. No third exception of one kind. The register's flags do not touch this
dataset except the few_minority mechanism (7 keep and 1 exclude; read below, consistent) and USE-5 (other datasets).

**1. THE FRAMING: CONSISTENT**

Decision: the target is the empiric treatment group (8 groups, 5 on the patients); whole patients are held out; the
source's 30-isolate task on its fixed test file is set aside.

- USE-5 (Must), resolution the actor acts on. Follows corporate_credit_rating (retired 2026-10-16, rebuilt as the
  issuer rating: the label the agency acts on) and nba_players_2016_2019 (No 2026-10-26, Lennart: the score ranked the
  whole ballot where the actor acts on 2-3 starters). Here the 30 classes include strains of one species with one
  treatment (E. coli 1 and 2, MSSA 1-3), which no physician tells apart. Same principle, same direction.
- SPLIT-4 (Must), new entity held out whatever the gap. Follows superconductivity (grouped by composition though a
  random split costs at most 0.009 R^2, 2026-10-06). Here the group-probe gap is only 0.005 macro AUC (IID 0.997,
  grouped 0.992), and the definition still holds patients out: the gap did not decide, as the rule says.
- SPLIT-29 and spectra.md ("Replicate spectra of one specimen, strain, mouse or patient are one group"). Follows
  pancreatic_cancer_mouse_detection (by mouse), micro_mass (by strain; the closest sibling: a bacterial species from
  one spectrum of a new isolate, kept 2026-10-12), raman_mlrod (by rock, this batch, undecided) and the screening of
  raman_rruff_mineral_raw (by specimen, AI 2026-10-31, not built). The 30-isolate task's 74.0% on the cultured test
  file against 93.1% at random is the SPLIT-29 mechanism measured.
- TP-6 (Must): the patient task is one the source itself defines (Fig. 4; 3_clinical_finetuning.ipynb), so this is
  the source's version, not a fix of our own; the 30-isolate task is set aside on USE-5 and SPLIT-4, not on its score.
- milk_nir_composition (this batch) keeps the cow known (temporal, the robot's own herd): another use case (USE-10),
  not a conflicting precedent.
- The curator's acceptance (CC 2026-11-08) came after the size check that named both framings and the 50 patients, so
  shipping the 50-patient task does not depart from what was accepted; the priority 3 assumed the large framing.
- One choice of our own, stated in splits_comment: the 2018 and 2019 patients are pooled into one grouped CV, where
  the source holds one patient per group out within 2018 and tests 2019 after 2018. heart_disease kept the source's
  site transfer (3 hospitals, 2026-10-27) with 51+ of each class per fold; here a 2018-to-2019 split would be one
  split of 25 patients (5 per group). Not a departure that needs a prompt; the 2018-to-2019 probe (90.1% per spectrum)
  is the evidence that the pooling hides no site effect that decides the score.

**2. FEW PATIENTS: DEPARTS, REASON STATED BUT NOT THE ONE THE RULE ACCEPTS**

Facts (claims.md 22, measured on all 60 splits): 50 patients, 10 per treatment group, 3 or 4 per group in every test
fold, 16-17 patients per fold. The score counts each patient once (MET-17 weight), so the patient is the unit TP-5
counts in. Task probe (5 of 60 splits): LightGBM best skill 0.839 / 0.789 / 0.813 / 0.775 / 0.817 per split; spread
LightGBM - random forest +0.349, paired SE 0.009; own permutation test 60 of 60 real fits below every permuted fit.

Precedents, closest first:
- parkinsons_biomedical_voice_measurements: retired Too Small (2026-10-05, Lennart). Same structure: one label per
  person, replicate recordings, scored per person, grouped by person. 8 healthy, 2-3 per fold, 10-11 people per fold.
  The CC names the instability: best AUC 0.58 to 1.0 across folds, Kendall's W 0.18, "the 60 folds recombine the same
  8". W/curation/records/parkinsons_biomedical_voice_measurements.md; task_probes.md Cases (TP-5).
- micro_mass: kept (2026-10-12, Lennart). Same structure (species per strain, replicate spectra). 20 species of 7-20
  strains, median 10, so about 3-4 strains of a typical species per fold, as here; but about 71 strains per fold in
  all. CC: "Too Small is for a task whose scored units are a handful".
- sarcoma, ljubljana_primary_tumor: kept (2026-10-12, Lennart). One class of 10 rows, 3-4 per fold, 5-13% of the test
  rows; the other classes large.
- musk: kept (2026-10-06, Lennart). 13 musk and 21 non-musk molecules per fold (34 in all).
- huesken_sirna_efficacy: `groups_test_groups_few` accepted (Myunghwan 2026-10-26; reworded by Lennart 2026-11-04: "a
  group is a large set of observations over which we want to generalize, so from the context a few groups suffice").
  Does not carry over: each gene holds 81 siRNAs with a label each (regression), while a patient holds one label over
  100-400 replicate spectra that MET-17's weight itself counts once.
- raman_mlrod (this batch, undecided): one rock per fold, but labels per point (about 16,000-19,000 scored points per
  rock). That is the few-groups domain-shift factor (covertype, heart_disease), not a TP-5 count. The two
  `groups_test_groups_few` acceptances of this batch rest on different rules and should not be cited for each other.

Rules as written:
- TP-5 (Must): Too Small is "a handful of units of a class, per test fold and in total, counted in the unit the task is
  scored on".
- principles.md, "How to decide" 4: "A very real task with a handful of units per class per test fold is still `Too
  Small`".
- The Tensions row "Tiny but real": `Too Small` when a class has a handful of units per test fold.
- definitions.md, check table: accept `groups_test_groups_few` only with real signal across groups "and more than a
  handful of groups of each class per fold (else `Too Small`)".
- evidence.md: the few_minority flag fires below 5 units of a class per test fold, counted in groups for a task scored
  per group. The probe counted rows (unit row), so it flagged only the three training-only classes. Counted in the
  patient unit, every one of the five tested classes is at 3-4, below 5. The builder's issue 2 gives the 3-4, but its
  reading of the flag (TP-8 reading 3 only) leaves this out.

Where it stands:
- On the count, bacteria sits one patient per class above parkinsons (3-4 against 2-3; 10 against 8 in total; 16-17
  against 10-11 per fold). Per class it equals micro_mass's typical species and sarcoma's rare class, but those two
  had large folds.
- The draft's reason ("signal across patients is strong ... and models spread") is the kind principles 4 rules out:
  independent failures are not conflicts.
- What does set it apart from parkinsons, measured but not stated, is the stability parkinsons lacked: skill 0.77-0.84
  on every probed split against an AUC of 0.58-1.0. Also, no single class is short (all five equal), and the fold
  holds 16-17 units.
- TP-5 is a Must: it takes no exception, so a keep at 3 folds is a reading of "a handful" that has to be written into
  TP-5 (an amendment). Otherwise take the milder remedy first: fewer, larger folds. definitions.md names it for
  undefined folds, and SPLIT-17 names it for temporal windows.
- Wording, if kept: the proposed acceptance should say, as huesken's and parkinsons' texts do, that the 60 splits
  recombine the same 50 patients, so their spread is descriptive.

C1, drafted as a turn:

Consistency check: Is three or four patients per class in a test fold more than a handful, when
parkinsons was retired at two or three?

- **Problem:**
  - Every tested class has 10 patients, 3 or 4 per test fold and 16 or 17 patients per fold, counted in the unit the
    score counts once[tp5].
  - parkinsons was retired at 2 or 3 healthy people per fold, while micro_mass and sarcoma were kept with about 3 or 4
    units of a class per fold inside much larger folds[cases].
  - The draft keeps it because the signal is strong, which the rules say does not rescue a fold that is too
    small[p4].
- **Background:** parkinsons' retirement named unstable scores (best AUC 0.58 to 1.0 across folds, Kendall's W 0.18);
  here LightGBM's skill is 0.77 to 0.84 on all 5 probed splits, and its lead over the random forest is +0.349 with a
  paired SE of 0.009.
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep 3 folds, the line written down (implemented) | accept the few-groups warning and write into the size rule that a class at 3 or more units per fold, with no single short class, 15 or more units per fold and stable scores, is not a handful | uses all 50 patients in 60 splits; the fact that sets it apart from parkinsons is measured; the next case follows a written line | changes how a Must reads; 3 or 4 per class is below the probe's own threshold of 5 |
  | b | Two folds | 30 repeats of 2 grouped folds: 5 patients per class and 25 per fold | meets the probe's threshold of 5; the mildest fix before retiring; training keeps 5 patients per class plus the library, more than the source's 3 | 5 per class is still few; 25 training patients instead of 33 or 34 |
  | c | Too Small, like parkinsons | retire with the `Too Small` marker | the rule as written today | drops a real task whose scores are stable, the fact parkinsons lacked |

- **Recommendation:** b, the mildest remedy that meets the threshold without changing a Must; a if you hold that 3 or
  4 units with stable scores is not a handful, and then the line goes into the rule. **Decision:** a, b or c?

[tp5]: **TP-5** (Must): `Too Small` means a handful of units of a class, per test fold and in total, counted in the
  unit the task is scored on (parkinsons: 8 healthy people, 2-3 per fold; retired). **TP-8** (Must; narrows TP-5):
  also when a test fold holds only a handful of units in all (parkinsons). **MET-17**: each patient counts once.
[cases]: task_probes.md Cases: parkinsons_biomedical_voice_measurements retired 2026-10-05; musk kept 2026-10-06;
  micro_mass, sarcoma, ljubljana_primary_tumor kept 2026-10-12 (Lennart). huesken_sirna_efficacy's few-genes
  acceptance (2026-10-26, Myunghwan; 2026-11-04, Lennart) rests on a label per siRNA, not per gene.
[p4]: principles.md, How to decide 4: "A very real task with a handful of units per class per test fold is still
  `Too Small`, because nothing ranked above it makes the fold scorable." definitions.md: accept
  `groups_test_groups_few` only with real signal and "more than a handful of groups of each class per fold (else `Too
  Small`)". evidence.md: `few_minority` below 5 units of a class per test fold.

Smaller point (house rule, not precedent): definitions.md asks for `group_probes.py` evidence before accepting
`groups_test_groups_few`. Its learnability table and permutation test did not finish (stopped after 2.5 h). The
builder's own permutation test used one family on three folds, with the task probe's four families against the class
shares beside it. That covers SPLIT-27 in substance; say so in the acceptance text.

**3. REFERENCE SPECTRA: CONSISTENT**

Decision: the 66,000 spectra of the 30 reference isolates, labelled by `ATCC_GROUPINGS`, are in every training side
and never tested (84% of the rows).

- TP-6 (Must) and USE-1 (Must): the source pre-trains its clinical model on the reference library for the eight
  groups (notebook: "pre-trained for the 8 class antibiotic treatment groupings task on the reference dataset"; claims
  24), and a lab has such a library. Option (A) is therefore the source's own version. Option (B), patients only, is
  not a better version the source defines. That the measured worth is mixed (PCA-LR better on 5 of 9, LightGBM and kNN
  on 4 of 9) does not decide: "a valid task stays".
- raman_mlrod (this batch) has the same design: 90,341 reference-map spectra train in every fold and are never
  tested, "as in the source". The two are consistent with each other.
- `splits_rows_never_tested` precedents: every earlier acceptance was a trim by the 500k test cap, 0.02-0.2% of the
  rows. They were amex_non_iid_1m and sepsis_prediction_1m (2026-10-01), fraud_detection_in_electricity_and_gas_
  consumption_1m (2026-10-20) and allstate_claim_prediction_challenge_1m. All of them were dropped once the row budget
  was recorded (W/datasets/_dev/tabarena-v0pt2/CHANGELOG.md, 2026-11-08 entries); no definition in df-large carries
  one now. So bacteria_id_raman and raman_mlrod would be the first by-design acceptances, two in one batch. This is
  not a departure. Once the curator decides, word the two alike and file one Cases row (a reference library that
  trains and is never tested, when the source trains on it), so a third case follows it.
- Precision fix, `splits_test_class_missing`: the builder reads the three reference-only groups (ciprofloxacin,
  ceftriaxone, caspofungin) as evidence.md few_minority reading 3 / TP-8's force_2020 case. That case is a class a
  grouped split leaves out of one fold and tests in others. In raman_mlrod too, every class occurs in some test fold.
  Here the three classes are in no test fold at all: 3 of the 8 target classes are never scored and act only as
  training-side distractors. The proposed acceptance text says this correctly; only the cited reading is off. File it
  as its own fact, not under force_2020.

**4. THE METRIC: CONSISTENT; ONE STALE PRECEDENT; ONE REASON TO REPLACE**

Decision: `Metric.fallback` log loss, weighted by `isolate_weight` (1/400 for a 2018 patient, 1/100 for a 2019
patient), declared as the task's `unit_weight`, scoring only.

- MET-5, MET-6, MET-8 (Should): the paper reports accuracy only, at two units (per spectrum on the isolates; per
  patient by a vote over 10 spectra), with no threshold or costs, while a wrong empiric antibiotic costs differently
  by pair. metrics.md's summary row: "A paper's accuracy, no threshold, no costs | the fallback, unless the use case
  acts on hard labels at equal costs". Follows heart_disease (fallback, 2026-10-21, Lennart; checked 2026-10-27),
  ljubljana_breast_cancer and credit_approval (fallback, proposed) and gallstone_disease (MET-5).
- Stale precedent (a finding for the knowledge file, not for this dataset): metrics.md MET-6 still lists "covertype (a
  single deliberate accuracy, hard labels per map cell: kept, proposed)". The curator decided the other way: "CC
  (2026-10-21, Lennart): Fallback log loss, not the paper's accuracy." (W/curation/records/covertype.md). The
  definition declares `Metric.fallback(... "MET-6, MET-8; Lennart, 2026-10-21")`
  (W/datasets/_dev/tabarena-v0pt2/covertype/dataset.py). This record's screening (2026-10-31) and draft issue 4 option
  (B) cite the stale line. As applied, covertype supports option (A), and no precedent is left for keeping a paper's
  habitual accuracy without costs (hiva_agnostic's balanced accuracy is a competition's, MET-4). Under "a precedent that
  contradicts a rule is flagged, not followed", MET-6's case list should say covertype went to the fallback; option (B)
  should drop the covertype reference or cite it as the opposite.
- MET-17 (Should; 2026-11-08): follows pancreatic_cancer_mouse_detection (fallback roc_auc weighted by mouse_weight)
  and dementia_prediction (fallback log_loss weighted by person_weight), both 2026-11-08, Lennart. In all three the
  labels are per unit, the unit's rows are repeats of the protocol (bleeds, visits, map spots; 400 against 100 here),
  the actor decides once per unit, the weight is for scoring only and is declared as `unit_weight`. Unlike
  asp_potassco_classification and video_transcoding_time_prediction (each row a decision, kept unweighted). Kendall
  tau 0.91 (lowest 0.60) against the per-row score, within the six cases' range.
- Side point, the prediction unit (SPLIT-23, Must): the definition makes each spectrum one prediction. The source
  predicts a patient's group by the mode over 10 random spectra, "to simulate a culture-free clinical setting where not
  many bacterial spectra may be available" (3_clinical_finetuning.ipynb). The builder report's reason for not taking
  the patient unit is that patient accuracy (0.96-1.00) would saturate, a score reason. For huesken and protein the
  curator set what one prediction sees by the use case, "not the gain" (2026-11-05, Lennart; SPLIT-23 Cases), and
  SPLIT-4 says the same of the split. The use case gives a reason that holds: its culture-free aim of few spectra per
  patient has one spectrum as its limit. The grouping definition states the departure ("the source votes over 10
  spectra per patient") but gives no reason. Only the note changes, not the design.

C2, drafted as a turn:

Consistency check: Should the notes justify scoring each spectrum alone by the use case rather
than by the saturated per-patient score?

- **Problem:**
  - The source predicts a patient's group by a vote over 10 random spectra, to simulate a culture-free setting with few
    spectra[unit].
  - The draft scores each spectrum alone because a per-patient score would saturate at 0.96 to 1.00 accuracy.
  - For huesken and protein the curator set what one prediction sees by the use case, not by the gain[stance].
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Each spectrum, the use case as reason (implemented) | keep the unit; the grouping definition says the source's culture-free aim, few spectra per patient, has one spectrum as its limit, and the weight counts each patient once | follows the 2026-11-05 stance; no rebuild | stricter than the source's own 10-spectrum vote |
  | b | The source's vote | one prediction per patient from 10 sampled spectra | the source's own unit | 16 or 17 predictions per fold, near-perfect accuracy, a log loss over a few units |

- **Recommendation:** a, a change to the notes only. **Decision:** a or b?

[unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is. **MET-17**: the weight
  changes how much a prediction counts, never what one prediction is.
[stance]: SPLIT-23 Cases: huesken_sirna_efficacy, `context="all_rows"` though it adds nothing measurable, "the context
  follows the use case, not the gain" (2026-11-05, Lennart); SPLIT-4: "the split follows what the task does in
  reality, not the size of the gap".

**5. THE SPECTRUM: CONSISTENT**

- CLEAN-26 (Should) and spectra.md: declared `Spectrum(name="raman_spectrum", prefix="raman_", unit="cm-1",
  technique="raman", state="processed")`, the whole 1,000-position range, columns named from the source's
  `wavenumbers.npy`, no value changed. `processed` matches spectra.md's definition ("a baseline removed, a
  normalisation or a derivative applied by the source"): a polynomial baseline of order 5 and 0-1 scaling, each per
  spectrum. That makes it a per-row step, not a statistic over rows (LEAK-30 not triggered). Compare
  pancreatic_cancer_mouse_detection (`raw`) and micro_mass (`peaks`), both declared by what the source did (2026-11-02,
  Lennart).
- Recommended encoding: the spectrum as it is, the default for processed and for vibrational spectra. The candidates
  were compared (SNV lower on 3 of 3 folds for both the linear model and LightGBM) and the default kept: "one dataset is
  a case". The same holds for open_soil_spectral_library (LightGBM gains from every candidate, default kept,
  2026-11-04), milk_nir_composition (SG first derivative 4 of 4 for LightGBM, default kept, this batch) and raman_mlrod
  (no candidate wins on both rocks, this batch).
- The 0-1 scaling anomaly (4.6-8.0% of spectra never reach 0) is kept as published. It is no fill value, so
  open_soil's edge-fill amendment of CLEAN-26 does not apply.
- For the benchmark, not a rule change: three of the four vibrational datasets now show some candidate beating the
  spectrum as it is for a tree model (open_soil, milk_nir, bacteria; not mlrod). spectra.md's evidence table holds only
  open_soil. The comparison is planned in BENCHMARK_CHANGES_TODO.md, "Spectra", by a rule fixed in advance; these cases
  feed it and change no default by themselves.

**DRIFT AND AMENDMENT CHECKS**

- TP-5 / TP-8 (Lennart): parkinsons retired 2026-10-05, musk kept 2026-10-06, micro_mass / sarcoma / ljubljana kept
  2026-10-12, huesken accepted 2026-11-04. The facts differ, so this is not drift. The register's `few_minority`
  pair (alvin_smart_money_management retired against seven keeps) is a temporal-window case against rare classes,
  consistent.
- MET-17: applied the same way on all six cases of 2026-11-08 and here; no drift.
- By-design `splits_rows_never_tested`: two cases (this one and raman_mlrod), no earlier one. Not three yet; file a
  Cases row with the curator's decision.
- MET-1 amendment_due flag (huesken, protein, superconductivity): does not involve this dataset (fallback, MET-17 as
  written).

</details>

<details><summary>bacteria_id_raman: advocate</summary>

ADVOCATE: OPENING BRIEF, bacteria_id_raman (2026-11-09)

Position: ship. Keep the definition as it is (treatment group of a new patient's isolate, grouped by patient, library
in training, patient-weighted fallback log loss). Make the wording fixes and add one protocol line; none of these needs
a decision. Two calls stay with the curator: the prediction unit (point 3) and the fold count (point 4). Neither
outcome excludes the dataset.

New measurement (EV-1). It settles the question the main session asked about the task gamer's exploit. I re-scored
the gamer's saved predictions for all 60 splits at the patient unit. Scripts and CSVs are in 
(unit_exploit.py, sharpen.py). Each patient counts once and gets the API's aggregation="mean" (mean of its rows'
probabilities):
                                                    LR-PCA      LightGBM
  honest model, per patient                         0.101-0.104 0.274-0.276
  + neighbour rebuild from test rows (exploit 1)    0.069       0.222      (60/60 lower)
  each row sharpened alone, p^t, no test rows, t=2  0.072       0.221      (60/60 lower than honest)
                                              t=3   0.067       0.211
  true isolate, geometric mean (context all_rows)   0.042       0.184
  year make-up prior alone (exploit 2)              -0.014      -0.033     (53/60, 51/60 lower)
At the patient unit, exploit 1 gains nothing beyond what a fixed sharpening of each row does. Exploit 2 survives the
change of unit.

1. The task is valid and it is the source's own clinical task. A blind reviewer arrived at the same design on its own.
   Evidence:
   - The source's own words: "Each patient is classified into one of 8 treatment classes" (Fig. 4); "we start by
     pre-training a CNN on the empiric treatment labels for the 30 reference isolates" (Methods). Claim auditor A1:
     holds.
   - IID over the patients' spectra lowers the loss by 26-69% and reverses the library ranking (split auditor 1).
     A new patient is a new strain.
   - The blind reviewer's top concerns (three classes unlearnable; whole reference isolates held out) came from a
     split it simulated over the reference isolates. Its clean room did not say those rows are training-only. Its
     "preferred fix" is the shipped design: "keep all 30 reference isolates in train in every fold and run grouped
     k-fold over the 50 patient isolates" (row accuracy 0.94, vote 0.99). Its fix for unequal isolates is the shipped
     weight: "weight rows as 1/(rows of their isolate)". The data match the source arrays row for row (78,500 of
     78,500), and the labels match config.py 30 of 30.
   Rules: USE-5 (Must), SPLIT-4 (Must), SPLIT-29 (Must), TP-6 (Must: the source's version; a valid task stays).
   Precedents: corporate_credit_rating, micro_mass, pancreatic_cancer_mouse_detection.
   Against the objection: the 74.0% vs 93.1% sentence is wrong as an attribution. I concede it (claim auditor A2,
   split auditor 7: that gap is mostly the file or session; the culture is worth 5-14 points). The framing never
   rested on it, because SPLIT-4 says the size of a gap never decides. Fix, no decision: reword with the auditors'
   numbers (77.5% vs 72.1% in the test file's own setting; 92.6% within the reference file vs 45.2% / 43.6% on the
   2 s files).

2. No leak in the data. The look-alike TZP pair stays.
   Evidence:
   - The spectrum is the only feature. It is processed one row at a time (LEAK-30 not triggered).
   - 0 exact copies in 78,500 rows. No reference row in any of the 60 test folds.
   - The gamer found no leaked column, id, row order or format. Format features give +0.001 / -0.003, inside noise.
   - The look-alike pair 2018-22/23 is TZP (blocks 21-25), not daptomycin as the claim auditor wrote. It moves the
     mean by about 0.007 of 0.242, and only in the 4 of 20 repeats where it straddles the split. The other look-alike
     pairs sit inside the band of ordinary pairs.
   Rules: SPLIT-30 (Must) re-splits only when the rows share an entity that new data would lack. Two patients
   carrying one hospital strain is something new patients do have. SPLIT-24 (Must) bars grouping on similarity.
   LEAK-17 (Must) needs a repeated entity, and the pair is not shown to be one (EV-6, circumstantial).
   Fix, no decision: a "Potential near-copy, kept on purpose" note naming the pair and its numbers. Also renumber the
   patients in a seeded random order: the id is never a feature, but its number follows the label blocks (column
   auditor 3, blind reviewer 4).

3. The gamer's exploit is an evaluation-level leak. It is fixed in the protocol or the scoring, not in the data.
   Is it the lab's own information once the unit is the patient? Partly:
   - The lab has its own patient's spectra: one monolayer, 100-400 spots mapped, and the source decides from 10.
   - It has neither other patients' rows nor the fold's make-up. Exploit 1 reads the 10 nearest test rows, and 14-25%
     of them belong to other patients. Exploit 2 needs the full count (5 per class per year), which comes from the
     paper and not from the training data.
   Rule: LEAK-9 (Should, amended 2026-11-05): "a model can read other test rows" is "fixed in the scoring ... or by a
   protocol line the benchmark checks, not in the data". Lennart: a method that learns from the test block "we can
   call out and not benchmark". Precedents: medical_facility_operational_data, sepsis_prediction_1m,
   5g_energy_consumption.
   Two forms that ship:
   (a) As defined (my recommendation). The unit stays the spectrum, and a LEAK-9 protocol line says each test row is
       predicted from that row and the training rows alone, with no fold composition from outside. Rewrite the reason
       for the unit, which is a fix of the notes (precedent checker C2): the source's own classifier predicts one
       spectrum at a time ("the most common class out of the 10 spectral classifications"), and its culture-free aim
       ("not many bacterial spectra may be available") has one spectrum as its limit. The weight counts each patient
       once.
       Under (a) the declared score ranks the four models like the physician's patient decisions: tau 0.94 with the
       10-spectrum vote, 0.91 with the uncovered-pathogen rate (domain practitioner). The patient-mean log loss ranks
       them at tau 0.61, and on the two linear models it orders them against both the vote and the coverage. So the
       ranking change the claim auditor found moves away from the decision.
       Log loss is proper for the row that is predicted (MET-8).
   (b) The source's patient call under SPLIT-23. Use prediction_unit="group", aggregation="mean", context="all_rows"
       (the lab's own spectra). Three conditions:
       - context="all_rows" is required. With context "none" the scorer's mean rewards sharpening each row (table
         above: t=3 lowers LR 0.104 -> 0.067).
       - Remove inputs={"weight": "isolate_weight"}. metrics._aggregate reads input columns at each group's
         representative row, so a 2019 patient (1/100) would count 4 times a 2018 patient (1/400).
       - Randomise the patient ids, since the model then sees the group.
   In both forms exploit 2 needs the protocol line. Stratifying on treatment x year (split auditor 6, optional) would
   narrow it; that is untested.
   Why this does not exclude: the tension row "a real task against a leak: fix the leak and keep the task" (P3/P4).
   The remedy ladder puts a protocol or scoring fix before exclusion. SPLIT-23 is met by either reading, and the
   choice is the curator's.

4. Few patients (TP-5, Must). Keep 3 folds. If the curator reads 3-4 as a handful, take the ladder's re-split, not
   Too Small.
   Evidence:
   - 10 patients per group. Every test fold holds 3-4 per group and 16-17 in all.
   - parkinsons was retired at 2-3 per class and 10-11 per fold, with unstable ranks: best AUC 0.58-1.0, Kendall's W
     0.18.
   - Here LightGBM beats the dummy on 5 of 5 splits (skill 0.77-0.84) and all 60 permuted fits score worse than
     the real one. LR vs kNN stays resolved under the patient bootstrap ([-0.77, -0.12]).
   - micro_mass (the closest sibling: species from spectra of strains, about 3-4 strains of a typical species per
     fold) and sarcoma (one class at 3-4 per fold) were kept.
   Rule: TP-8 (Must, narrows TP-5) applies Too Small when a short class carries the score or a fold holds "only a
   handful of units in all (parkinsons)". No class is short (all five have 10), and 16-17 per fold is above
   parkinsons' 10-11.
   Concession: the score is concentrated. One patient carries 16-51% of a fold's loss, and the patient-bootstrap SE
   (0.05 on 0.24) is 18 times the SE across repeats. Gaps below about 0.03-0.05 do not generalise. That goes into the
   accepted groups_test_groups_few text, with "the 60 splits recombine the same 50 patients".
   Mildest fix if needed: 2 folds x 30 repeats, 5 per class and 25 per fold (precedent checker C1 b). Under
   principles 5, a re-split comes before exclusion.

5. Reference library in training (issue 3). Keep it, with a note.
   Evidence:
   - The source pre-trains on these 66,000 spectra for all eight groups.
   - Every identification system starts from a library, and the probability on the three library-only groups is a
     real open-set cost: Candida, Salmonella and S. pneumoniae do occur in patients (domain practitioner).
   - Ruling those groups out is worth 0.007-0.049 (3-26%) per the column auditor. A model can learn it from the
     training patients: the gamer's honest restrict5 gives -0.005.
   - raman_mlrod in this batch has the same design.
   Rule: TP-6 (Must): "a valid task stays". Dropping the 6 isolates, or the whole library, is a fix of our own and not
   a better version the source defines.
   Against the objection: the column auditor files it as a weighing call, with no Must at stake. The library's mixed
   worth (its gain rests on two vancomycin patients, split auditor 4b) is a finding for the notes, not a reason to cut
   it.
   Fixes, no decision:
   - Say in the notes that about 0.05 of 0.24 is how a model handles the library's class shares and its three
     untested groups.
   - Cite the three never-tested groups as their own fact, not as force_2020's case.
   - File one Cases row with raman_mlrod.

6. The metric holds: fallback log loss, each patient once.
   Evidence:
   - The source reports accuracy only, with no costs or threshold (claim auditor A7).
   - The precedents are heart_disease, ljubljana_breast_cancer, gallstone_disease, and covertype as it was applied:
     fallback, Lennart 2026-10-21. MET-6's case list still calls covertype a kept accuracy. That is stale, so option
     B has no precedent left. For the unit weight: pancreatic_cancer_mouse_detection and dementia_prediction.
   - Per-spectrum accuracy ranks the models least like the patient decisions (tau 0.56).
   Rules: MET-6, MET-8 and MET-17 (all Should, followed, no departure).
   Fixes, no decision:
   - Correct MET-6's covertype entry (a knowledge-file fix).
   - Add to the metric reason that the source's early stopping selects on validation accuracy (MET-1, "where you
     looked").

7. The rest is wording and fit notes. The fit is already declared approximate.
   - The Gram stain (45-52% of errors cross the Gram line), the fixed drug per species (no resistance), MALDI-TOF as
     the comparator at the culture stage, and the forward 2018 -> 2019 test (0.368 vs 0.229 pooled, the same patient
     decisions) go into fit_reason and the notes.
   - The Gram stain cannot ship. It is not in the source, and on this closed five-species set it is a function of the
     label (2 Gram-negative groups against 3 Gram-positive).
   - Further fixes: the patients' map is about 20 wide, not 45 x 45. Correct splits_comment on the 2019 protocol and
     the "code order" comment. Drop the crop guess. Add the 25-brightest filter, the uneven grid, and the presumed
     species from config.py's comments (marked inferred). Count few_minority in patients.
   Rules: USE-8 (Must) is met: the fit is written as approximate, with the gap named. Tension row "a real task
   against imperfect cleaning" (P3 over P7): name the gaps, keep the task.

Judgment record (as I argue it)
Verdict: ship after changes.
Validity: SEL holds; USE-5, SPLIT-4, SPLIT-29 hold (grouped by patient); SPLIT-24 holds (blocks confirmed 10/10);
  SPLIT-30 kept with a note (2018-22/23); SPLIT-23 the curator's reading, (a) or (b), both valid; LEAK-9 triggered,
  fixed by a protocol line (and by the scoring in (b)).
Value: TP-5/TP-8 borderline keep with stable signal; fallback 2 folds if the curator draws the line at 5. MET-6, MET-8,
  MET-17 hold.
Quality: CLEAN-26 holds; wording fixes as listed.
For the curator: the unit (3a or 3b) and the folds (3 or 2).

</details>

<details><summary>bacteria_id_raman: advocate rebuttal</summary>

ADVOCATE, REBUTTAL: bacteria_id_raman (2026-11-09)

New fact (EV-1). I re-scored the critic's four models (the split auditor's stored predictions, all 60 shipped splits)
against the source's own patient call: a majority vote over 10 random spectra per patient. Script and CSV:
unit_ranking.py and unit_ranking.csv.
                         declared  patient mean  patient mean,  patient, log-prob   vote over 10,
                                                 rows ^2        pooling            error
  LR C=0.01 + library    0.225     0.130         0.097          0.028              0.003
  LR C=1 + library       0.242     0.105         0.090          0.013              0.005
  LR patients only       0.321     0.096         0.093          0.066              0.028
  kNN + library          0.612     0.224         0.170          0.192              0.031
Per-split Kendall tau with the vote: declared 0.62, patient mean 0.37 (lowest -0.71).
Caveat: the vote sits near its ceiling and ties often, so it is a coarse check.

Critic 1, USE-8, four unnamed gaps: CONCEDE. This is my point 7. Add (a)-(d) with their numbers to fit_reason and the
  notes. The fit stays approximate. No code change.

Critic 2, SPLIT-23 (Must), the unit:
  - CONCEDE: the saturation reason is a P6 reason and cannot decide a P4 Must. It goes.
  - DISPUTE: that tau 0.48 and "best differs on 36 of 60" show the row unit is wrong. The patient-mean score departs
    from the source's own patient score more than the declared score does.
    - The declared score orders the four models exactly as the vote does (means above). The patient mean puts the
      patients-only model first, although its vote error is 9 times that of LR C=0.01.
    - The C=1 against C=0.01 flip (59 of 60) is temperature, not knowledge. Raise the same C=0.01 rows to the power 2
      and it beats C=1 at the patient mean on 52 of 60 splits (power 3: 58 of 60). The vote prefers C=0.01: C=1 wins
      only 2 of 60.
    - Under the critic's remedy (context all_rows) the order depends on each method's pooling. Mean against log-prob
      pooling gives tau 0.57, with the same best on 43 of 60. A strictly proper row score has no such free knob
      (MET-8).
  - The source's own unit: the source classifies one spectrum at a time and calls the patient from "the 10 spectral
    classifications" by a vote. The declared score is the proper score of that spectral classification, with each
    patient counted once (MET-17).
  - The exploit is not "the lab's own information": 14-25% of its 10 neighbours are other patients' rows. LEAK-9
    (Should) fixes reading the test block by a protocol line the benchmark checks. Precedents:
    medical_facility_operational_data and sepsis_prediction_1m.
  - Residual exploit 2: agreed, keep it named. I would cite LEAK-9 (a protocol line), not LEAK-30, which is about the
    source's transforms. The outcome is the same.
  - Net: the curator reads SPLIT-23. I hold (a), row, on the evidence above. If (b) is chosen, it needs all_rows, no
    weight input and random ids (critic 6), plus a note that its ranking turns on pooling and temperature.

Critic 3, drop the 6 library-only isolates: DISPUTE. Keep, with a note; it is a weighing call either way.
  - LEAK-14 does not fit. Its mechanism is a tested class that its source gives away: biogeographical's Turkey rows
    were separated at AUC 0.96-0.98 by an assay artefact. Here no row of the three groups is ever tested, so no
    tested score is inflated. No Must is triggered, so the ladder's "fix the definition first" does not bind.
  - What remains is a level offset that the training data teach: the training patients show their five-group set
    (gamer's honest restrict5: -0.005).
  - It barely moves the ranking. Renormalising over the five groups gives tau 0.94 with the declared score, with one
    swap in 6 splits (domain practitioner). The critic's reason, that it exceeds the 0.017 LR gap, shows a level, not
    a reorder.
  - TP-6 (Must): "a valid task stays". The source pre-trains on all eight groups, and a lab's library holds Candida.
    Dropping is our own filter.
  - If the curator weighs it the other way, the drop is mild and still ships: training rows only, the test unchanged.

Critic 4, SPLIT-30 and LEAK-33: AGREE. These are my point 2: a near-copy note naming the TZP pair, and random patient
  ids.

Critic 5, TP-5 (Must): CONCEDE IN PART.
  - A keep at 3 folds needs the line written into TP-5 (an amendment), because a Must takes no exception.
  - I hold that the facts support that line: micro_mass, the closest sibling, was kept at about 3-4 strains of a
    typical species per fold; the scores are stable, which parkinsons' were not; no class is short; and a fold holds
    16-17 patients.
  - Otherwise use 2 folds. Agreed: Too Small only if neither. The accepted warning carries the patient-bootstrap SE and
    the concentration numbers.

Critic 6, the weight input under the group unit: CONCEDE. My point 3b says the same from metrics._aggregate. The
  critic's tau of 0.89 (lowest 0.33) with the weight kept against without it adds the size of the effect. Remove
  inputs={"weight": ...} with the unit change. unit_weight stays for validation. Under (a) nothing changes. The stale
  covertype citation and the MET-1 note: agreed (my point 6).

Critic 7, five wrong statements: CONCEDE all five, plus the presumed species. These are the same wording repairs as
  my points 1 and 7, and none needs a decision.

Critic's dropped list: AGREE on all four. The blind reviewer's concerns 1-2 rest on its own simulated split. Year
  columns and a year-wise split are not wanted. The format exploit is noise.

</details>

<details><summary>bacteria_id_raman: critic</summary>

bacteria_id_raman: critic's opening brief (critic, 2026-11-09)

Verdict asked for: ship only after changes. The task is real and holding out whole patients is right. But the
definition predicts the wrong unit. The score also carries a part that the test can only penalise. And the folds keep
3-4 patients per class without the amendment TP-5 would need. No point asks for exclusion: every Must here can be
fixed.

Judgment record, as I argue it:
  Validity: USE-8 met in kind, but four known gaps are unnamed (note). SPLIT-23 triggered (fix the definition: the
    patient is the unit, context all_rows). LEAK-14 is the closest rule for the three groups only the library holds
    (drop 6 isolates; a weighing call). SPLIT-30 holds for one look-alike pair (note). LEAK-33 holds (cheap hardening).
  Value: TP-5 triggered at 3-4 patients per class per fold (2 folds, or the curator amends TP-5). The fallback log loss
    holds, but its weight input has to go with the unit change.
  Quality / procedure: five statements in the notes are wrong or unsupported (repair).

My own measurements (no refit; they use stored per-row probabilities on all 60 shipped splits: the split auditor's 4
untuned models and the task gamer's 2 models; EV-8: probe numbers, not leaderboard numbers):
  unit.py and unit.log, exploit_unit.py and exploit_unit.log
  (P = the run's panel folder)

**1. P3, USE-8 (Must): fit_reason names two gaps and leaves out four that change what the score means.**
Problem. fit_reason names two gaps: cultured monolayers against culture-free, and five species. It does not name:
  (a) The Gram stain. A lab always has it when a culture flags, before any identification. 45-52% of the per-spectrum
      errors of four untuned models cross the Gram line (domain practitioner, 6 shipped splits), for example a Staph
      spectrum read as piperacillin-tazobactam.
  (b) The comparator. At the culture stage where these data stand, MALDI-TOF or a PCR panel gives the species in
      minutes to an hour. The choice is not between Raman and waiting days.
  (c) The label. It is one fixed drug per species, and resistance plays no part (the paper's clinical MRSA/MSSA accuracy
      is 65.4%).
  (d) The years. Sites and years are pooled, where a lab moves forward in time. Going forward from 2018 to 2019 gives a
      log loss of 0.368, against 0.229 for the pooled split with the same model (PCA-100 LR, domain practitioner).
Effect. A reader takes the score as Raman's gain for an empiric choice made before culture. What it measures is the
identification of five species from cultured colonies, without the Gram stain.
Remedy (a note): add (a)-(d) and their numbers to fit_reason and curation_comments. The fit stays approximate. No code
changes.

**2. P4, SPLIT-23 (Must): one spectrum is not the source's prediction, and the row unit cannot be held.**
Problem. The grouping says prediction_unit="row", context="none". The source identifies a patient by a majority vote
over 10 random spectra, "to simulate a culture-free clinical setting where not many bacterial spectra may be available"
(3_clinical_finetuning.ipynb; Results). The definition gives no use-case reason for using one spectrum. The builder's
reason (issue 4) is that patient accuracy saturates. That is a P6 reason, and it cannot decide a P4 Must (principles.md,
Tensions: "The right split against the score"; SPLIT-23 Cases huesken and protein: "the context follows the use case,
not the gain").
Evidence that it matters:
  - The row unit cannot be enforced, because a patient's test rows arrive together. The task gamer averaged each row's
    prediction over its 10 nearest test rows, which rebuilds the patient. That lowers the score on 60 of 60 splits, by
    32% (LR-PCA, 0.153 -> 0.104) and by 32% (LightGBM, 0.386 -> 0.261). The information it uses, the other spectra of
    the same isolate, is what the lab itself has: it measures 100-400 spectra per isolate, and the source votes over 10.
    The trick is the deployed lab's own information, hidden behind a unit the source did not use.
  - The unit changes the ranking (mine, 4 models, 60 splits). Compared: the declared score, and a patient score (the
    mean probability, each patient counted once).
      Kendall tau between the two, per split: 0.48 on average, lowest -0.33.
      The best model differs on 36 of 60 splits.
      LR C=1 beats LR C=0.01 on 17 of 60 splits by the declared score, and on 59 of 60 per patient.
      kNN's gap to the best model: 0.406 against 0.143.
    The claim auditor found the same: the two logistic regressions swap places on 5 of 6 folds.
  - Per patient, the log loss is not saturated: 0.10-0.22 (claim auditor) and 0.096-0.224 (mine). Accuracy
    saturates; the declared metric is log loss.
  - The precedents point the same way. musk (a molecule's conformations: "group", "any") and
    fraud_detection_in_electricity_and_gas_consumption_1m ("every invoice is one observation of" the client's label:
    "group", "mean"). The schema itself describes mean as "replicate measurements, one shared label".
  - Against the precedent checker's C2 (the culture-free aim has one spectrum as its limit): one spectrum is our
    extrapolation, not the source's use case. The source chose 10 and calls 10 "not many". And the data are cultured
    colonies, so the culture-free premise is already outside them (fit_reason).
Remedy (fix the definition). Set Grouping(prediction_unit="group", aggregation="mean", context="all_rows"). Change
grouping.definition and task_summary.split to "one identification per patient from its spectra". With all_rows, the
exploit is no longer hidden. Pooling a patient's own spectra (an average of log-probabilities) is an allowed method,
and it scores 0.037 (LR-PCA) and 0.179 (LightGBM) per patient. The kNN trick at the same unit scores 0.069 and 0.222.
So the trick becomes a worse version of an allowed method (mine, exploit_unit.log). Re-run the task probe and the
issue-3 comparison at this unit (point 3). For the metric weight, see point 6.
Residual, kept with a note. The gamer's exploit 2 is the test fold's class make-up per collection year: 5 patients per
class per year, and the year can be read from one spectrum at AUC 0.993. It survives any random grouped fold. It gains
-0.017 for LR-PCA (better on 73% of splits) and -0.043 for LightGBM (80%), and it needs the paper's design. Keep it
with a "Potential leak, kept on purpose" note (the weak transductive row of the Tensions table, LEAK-30).

3. P4, the three groups only the library holds. Closest rule LEAK-14 (Must), applied by analogy; as it stands, a
   weighing call.
Problem. Ciprofloxacin, ceftriaxone and caspofungin occur only among 6 reference isolates (13,200 rows), a separate
measurement series (1 s against 2 s, Methods). Within the five shared groups, the spectrum tells a library row from a
patient row at ROC AUC 0.932 (column auditor). The test never holds the three groups, so probability put on them is
always penalised and never rewarded. The score therefore rewards learning that a spectrum that looks like a patient's
is not one of the three. That is a fact of the closed five-species sample, not of biology. The domain practitioner
argues that this is a real open-set cost. An open-set test would need patients of those groups, and there are none.
Evidence:
  - Dropping the 6 isolates lowers the weighted log loss by 0.007-0.049 (LR and LightGBM, 3 folds), 3-26% of the loss
    (column auditor).
  - Renormalising LR over the five groups lowers it from 0.242 to 0.197 on 60 of 60 folds (split auditor). That is more
    than the gap between two good models (0.017).
  - The class-share dummy pays 0.34 nats for the library's prior (claim auditor).
  - The library's worth turns with the unit. With the library, the model beats the patients-only model on 41 of 60
    splits per spectrum, but on 24 of 60 per patient (mine; untuned).
  - The per-spectrum gain rests on two vancomycin patients, 144% of the net gain (split auditor).
Remedy. Drop the 6 reference isolates of the three groups in _clean. Training and test then hold the same five groups,
which clears splits_test_class_missing and matches fit_reason's "which of five". The test task is unchanged: this
filters training rows and is not a new version (TP-6). The milder option, if the curator takes it: keep, with a note
carrying these numbers. Either way, re-measure issue 3 at the unit of point 2.

**4. P4, SPLIT-30 (Must) and LEAK-33 (Must): both hold; one note and one free hardening.**
- 2018-22/23 are a look-alike pair: they are as alike as two halves of one patient. Each one's loss drops by 0.21 and
  0.14 when the other is in training, about 0.007 of 0.242 on the mean (split auditor). By the block order the pair is
  piperacillin-tazobactam; the claim auditor's "daptomycin" is a slip. SPLIT-24 forbids grouping on similarity, and
  clonal spread among patients is real. So no re-split, but add a "Potential near-copy, kept on purpose" note that
  names the pair.
- `isolate` encodes the label. Patients are numbered in label blocks (2018-01..05 are meropenem, and so on), and the
  reference names spell the species. It is never a feature, so LEAK-33 holds. Number the patients in a seeded random
  order within each year (column auditor, blind reviewer): cheap and safe.

**5. P6, TP-5 (Must) and TP-8: 3-4 patients per class per test fold, below the flag's own threshold.**
Problem. Each class has 10 patients: 3 or 4 in every test fold, 16-17 patients per fold. TP-5 counts in the unit the
score counts once: the patient (MET-17 now, the group unit after point 2). The few_minority flag fires below 5 units of
a class per fold, counted in groups for a task scored per group (evidence.md). The builder's probe counted rows and
missed this. parkinsons was retired at 2-3 per fold (TP-5 Cases). The draft keeps the dataset because the signal is
strong and the models spread, which is the reason principles.md "How to decide" 4 rules out.
Evidence:
  - One patient carries 16-51% of a fold's loss, and three carry 43-83% (claim auditor).
  - Patient-bootstrap SE 0.050 on a mean of 0.242. That is 18 times the SE over repeats (0.003): the 60 splits
    reshuffle the same 50 patients.
  - LR C=1 against C=0.01 is not resolved under patient resampling ([-0.009, +0.051]). Gaps below 0.03-0.05 do not
    generalise (split auditor).
  - Per patient (mine), the worst patient carries 30% of a fold's loss on average (max 56%) with the library, and 49%
    (max 89%) for patients only.
What sets it apart from parkinsons (precedent checker): skill 0.77-0.84 on all 5 probed splits, no single short class,
16-17 patients per fold. That argues for amending TP-5's "handful". It is not an exception, since a Must takes none.
Remedy, mildest first:
  - Use 2 grouped folds: 5 patients per class and 25 per fold. Training keeps 5 per class plus the library, more than
    the source's 4 per class in its leave-one-patient-out loop over 2018.
  - Or the curator writes the line into TP-5 (an amendment).
  - `Too Small` only if neither.
In every case, the accepted groups_test_groups_few text should give the patient-bootstrap SE and the concentration
numbers, and say that the splits recombine the same 50 patients.

6. P6, MET-17 / MET-6 (Should): the metric stands, but its weight must go with point 2, and issue 4 cites a stale
   precedent.
- The fallback log loss holds (MET-6, MET-8): the source reports accuracy only, with no threshold and no costs.
- With prediction_unit="group", the scorer already counts each patient once. It reads the weight input from each
  group's first row (metrics.py: score_rows reads the inputs at the rows that _aggregate returns, rows[pick]). If
  isolate_weight stays, a 2019 patient (1/100) counts four times as much as a 2018 patient (1/400). Between the patient
  score with and without the weight, Kendall tau is 0.89 on average and 0.33 at the lowest (mine).
  Remedy: remove inputs={"weight": "isolate_weight"} together with the unit change. unit_weight can stay, for
  validation.
- Draft issue 4, option B rests on "covertype, a single deliberate accuracy". On 2026-10-21 the curator set covertype
  to the fallback log loss (curation/records/covertype.md, and its dataset.py), so MET-6's list of cases is stale
  (precedent checker). Remedy: remove the citation from option B and flag the MET-6 line. Also record in the metric
  reason that the notebook selects models by validation accuracy (MET-1, claim auditor).

**7. Procedure (writing.md, EV-2): five statements in the notes are wrong or unsupported (repair).**
- "74.0% against 93.1% ... a split over spectra mostly rewards knowing the culture". The numbers hold; the attribution
  does not. 92.6% on held-out spectra of the reference file against 45.2% and 43.6% on the 2 s files of the same
  strains. Within the 2 s setting, a new culture costs about 5-14 points (77.5 against 72.1; 90.6 against 76.5;
  claim and split auditors). Reword it in curation_comments, in issue 1 and in claims.md 21. The framing still stands
  on USE-5 and SPLIT-4.
- "one spot of a 45 x 45 map": true for the library. The 2018 rows repeat at a lag of 20 rows, which fits a 20 x 20 map
  of 400. Say that the patients' map size is not stated.
- splits_comment, "tests the 2019 patients after training on 2018": the source tests the 2019 patients in their own
  one-per-group loop, after fine-tuning on the other 2019 patients, with 10 spectra per training patient.
- The CLINICAL_FILES comment, "the groups in code order": the 2018 blocks run 0, 6, 5, 3, 2 and the 2019 blocks 0, 5, 6,
  3, 2.
- The anomaly bullet's "as if scaled before a crop": not supported, since the minima sit at inner positions. The notes
  also leave out the source's row filter: the 25 highest-intensity spectra of each map were discarded.
Also: record the presumed species of the five patient groups, from config.py's comments, marked as inferred.

**Dropped (no backing on the shipped definition)**
- Blind reviewer, concerns 1-2: three groups cannot be learned, and reference isolates are held out. It simulated a
  split over the reference isolates, but the shipped splits keep all 30 in training: 0 reference rows are tested on
  any of the 60 splits.
- Blind reviewer, concern 5 (add subset and year columns): leaving them out is right, as no new patient comes with one
  (column auditor).
- `Too Small` outright: a fix exists (point 5) and the scores are stable.
- A year-wise split: it would remove exploit 2, but it turns the task into a transfer between two sites with one pair
  of splits. I do not ask for it.
- The format exploit (raw count range): within the noise. A measurement-day batch by species cannot be tested without
  dates, and the transfer across years bounds it (0.88 and 0.84 accuracy).

</details>

<details><summary>bacteria_id_raman: critic rebuttal</summary>

CRITIC, REBUTTAL: bacteria_id_raman (2026-11-09), point by point against the advocate's opening brief

No new points. One concession changes a remedy of mine: exploit 2 needs a LEAK-9 protocol line, not a note (point 3
below).

Advocate 1, the task is valid and is the source's own; the blind reviewer converges on the shipped design: CONCEDE.
  The patient task, the grouping by patient and the library used for training only hold, as my brief says. The
  74.0 / 93.1 rewording is agreed.

Advocate 2, no leak; the TZP pair stays with a note; renumber the patients: CONCEDE. It is my point 4, word for word.

Advocate 3, the unit: DISPUTE form (a), SUPPORT form (b) with all three of its conditions.
  (i) "The source's model classifies spectrum by spectrum." That is true, and it does not decide the unit. The source's
      prediction is the identification: "The most common class out of the 10 spectral classifications is then chosen
      as the identification" (Results). Its clinical results are reported per patient. The two group-unit precedents
      work the same way: musk classifies each conformation and decides per molecule, and fraud_detection_..._1m scores
      each invoice and decides per client. In this API, a per-row model with an aggregation is exactly what
      prediction_unit="group" means. SPLIT-23 (Must) also decides "what is known about a new group when predicting".
      The lab knows the other spectra of its own patient, so context="none" departs from the source too.
  (ii) "The declared score ranks like the patient decisions (tau 0.94 vote, 0.91 coverage)." Those taus come from
      LightGBM and kNN, which are worse on every measure. The only contested pair, the two linear models, cannot be
      ordered by the vote or the coverage rate: both are at their ceiling. The per-split differences are -0.001 to
      +0.007 in vote accuracy and -0.006 to 0 in the uncovered rate (dp_summary.log). One patient is about 0.06 of a
      fold, so these orderings rest on a tenth of a patient or less. The patient log loss separates the pair by 0.018 to
      0.033 on 6 of 6 splits. The "ranking change that moves away from the decision" therefore rests on noise, while the
      ranking change itself is large: tau 0.48 on 60 splits, and the best model differs on 36 of 60 (critic's probe).
      MET-10 (resolution and ceiling) is the advocate's own reason for rejecting the vote as a metric. The same reason
      bars using it to referee the unit.
  (iii) "The culture-free aim has one spectrum as its limit" (precedent checker C2). SPLIT-23 asks for the source's use
      case, cited. The source chose 10 spectra and calls 10 "not many". One spectrum is our extrapolation, and the
      culture-free premise lies outside these cultured data anyway (fit_reason).
  (iv) The LEAK-9 protocol line of form (a). LEAK-9 (Should) fixes an evaluation leak once the unit is settled. It does
      not choose the unit, and SPLIT-23 is a Must. Every LEAK-9 case bars information the actor would not have: future
      rows of a queue in medical_facility_operational_data, trajectories that end at the outcome in sepsis. The line in
      (a) would also bar the patient's own spectra, which the source's actor uses. A protocol line may not make the task
      blinder than its use case.
  (v) The new measurement (each row sharpened alone matches the neighbour rebuild at the patient unit). I accept the
      numbers (sharpen.py re-read: each row raised to the power t, no test rows used). They support (b). At the patient
      unit the neighbour rebuild gains nothing that a fixed transform of each row, with no test rows, does not also
      gain. So once the unit is the patient, exploit 1 carries no information from other test rows. What sharpening
      shows is that the scorer's arithmetic mean is under-confident when replicates agree. That is why context="all_rows"
      is needed. With it a method returns its own patient prediction (the geometric mean over the true isolate: 0.042 and
      0.184 by the advocate's numbers, 0.037 and 0.179 by mine), and log loss on that prediction is proper (MET-8). Under
      the row unit, by contrast, the rebuild's -32% comes from other test rows, so form (a) keeps a live exploit behind
      a rule the harness has to enforce.
  Concessions. All three conditions of (b) are right, and they match my points 2 and 6: context all_rows, the weight
  input removed, the ids randomised. In both forms, a LEAK-9 protocol line is still needed: no rows of other test
  patients, and no fold composition from outside the training data (exploit 2: -0.014 / -0.033 at the patient unit).
  I withdraw "note" for exploit 2 and ask for that line.
  Rule that wins: SPLIT-23 (Must, P4) decides the unit and the context. LEAK-9 (Should) supplies the protocol line
  within that.

Advocate 4, keep 3 folds: DISPUTE, narrowly.
  TP-8 narrows TP-5 for a short class among larger ones. Here every tested class is at 3-4 per fold, so the case is
  TP-5's own: "a handful of units of a class, per test fold and in total". The few_minority threshold is 5 groups.
  The closest kept precedents had large folds: micro_mass about 71 strains per fold, and sarcoma with one rare class.
  The LR-against-kNN gap does stay resolved, which I concede, but LR C=1 against C=0.01 does not ([-0.009, +0.051]),
  and the benchmark ranks close models.
  The advocate's own fallback is mine (2 folds x 30 repeats). Keeping 3 folds needs the line written into TP-5 (an
  amendment), because principles 4 bars "strong signal" as a reason and a Must takes no exception. Neither of us asks
  for Too Small. The concentration text the advocate concedes is agreed.

Advocate 5, keep the library with a note: PARTLY CONCEDE.
  Keeping the library is agreed; I never asked to cut it. The drop of the 6 isolates is a weighing call, not a Must,
  and the note is an acceptable milder remedy if the curator weighs the source's 8-group pre-training higher.
  I dispute two parts:
  - TP-6. Dropping training rows leaves the test task unchanged: the same 50 patients and the same five scored groups.
    That is a filter on the remedy ladder, not a new version.
  - "A model learns it: restrict5 gives -0.005." That figure holds for the gamer's model, which already weights
    patients x5. For standard models the component is 0.242 -> 0.197 on 60 of 60 folds (split auditor), and the cost
    is one-sided: a test without those groups never rewards mass on them.
  Not answered by the advocate: the library's measured worth flips with the unit (it beats patients-only on 41 of 60
  splits per spectrum, 24 of 60 per patient). Issue 3 must be re-measured at the unit the curator chooses.

Advocate 6, the metric holds: CONCEDE. The weight removal under (b) is agreed (my point 6). So are the stale covertype
  line and the MET-1 note.

Advocate 7, wording and fit notes: CONCEDE. My point 1 asks for exactly these notes. USE-8 is met once they are
  written. The Gram stain cannot ship as a feature: agreed.

Where we differ, for the mediator:
  (1) The unit and the context. SPLIT-23 against the advocate's (a). I hold that SPLIT-23 (Must) decides it for (b).
  (2) Folds. 2, or 3 with a TP-5 amendment: the curator's call; neither of us asks for Too Small.
  (3) The 6 library isolates: drop, or keep with a note. A weighing call.

</details>
