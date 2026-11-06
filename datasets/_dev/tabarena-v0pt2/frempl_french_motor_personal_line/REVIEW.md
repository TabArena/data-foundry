# frempl_french_motor_personal_line

**Outcome:** added. The AI recommends shipping it; the forced split of one year and the `Exposure` fix are settled
(2026-11-02), and the claim cost per year with the realized length as the weight (issue 6, 2026-11-06). A French private
insurer's motor portfolio of 2004 (CASdatasets freMPL5 to freMPL9, 115,155 records, each a policy's period of cover with
fixed rating factors); the target is the period's claim amount per realized year, shipped as log1p and scored on the
amount per year by the exposure-weighted Gini of the ordered Lorenz curve (a context metric), with the realized length
as each record's weight in training and scoring; all records of one policy component stay on one side of the split.
Validity: SEL-1 holds (`Gender` noted); USE-1 holds, fit approximate (USE-8); LEAK-41: the realized length `Exposure` is
the rate's denominator and the weight, never a feature (issue 6; it supersedes the fix of 2026-11-02 under LEAK-10,
which kept the realized length on the continued records); LEAK-10 holds for the other features; LEAK-24 cannot be
verified (issue 3); SPLIT-9 triggered and fixed: under random records, a test record's later records sat in training
and gave its claim away to a model that reads training rows, so the folds are grouped by policy component (issue 1);
LEAK-9: those later records are test rows now, so a protocol line forbids reading other test rows; SPLIT-8 ships the one
year as `ForcedGroupedFromTemporal`, shipped on your call of 2026-11-02 (forced grouped splits ship; SPLIT-8 amended);
PROV-7, PROV-8 and PROV-9 hold. Value: a small real signal (TP-2: claim AUC about 0.67, claim sizes not learnable); an
honest model beats the length to 31 December alone on every split (TP-4: 0.183 against 0.005, 9 of 9 shipped splits);
1/`Exposure` alone scores 0.184, the ceiling a leak would reach. Quality: the negative amounts stay set to 0, with a
corrected reason. Weighed: documented source and size +; low signal, fold noise (SD 0.03 over the 9 splits) and a thin
tariff (no vehicle or cover factors) -; a squared-error fit on the shipped log1p scale is misled by the length to 31
December (issue 7). Left for Lennart: issue 7.

Changes made after the review panel (AI, 2026-11-01): the folds grouped by policy chain, `Exposure` fixed (issue 2), the
valid windows stated in `splits_comment` (SPLIT-8), the metric reason and the negatives text corrected, and the figures
re-measured on the shipped folds. The record's screening lines the data refutes (the year, the chain links, the file
sizes, "near-random slices", the negatives) are corrected at hand-over and need no mark. Changed on 2026-11-06 (issue
6): the target is the claim amount per realized year, `Exposure` the weight and no feature, the length to 31 December
the feature, the metric the Gini per unit of `Exposure`; `exposure_at_start` dropped; `fit_reason` no longer names a
kept leak; a protocol line against reading other test rows.

**Main points:** issues 1, 3 and 4 resolved on 2026-11-03 and issue 6 on 2026-11-06: the amounts stay with their note
(3), the folds are grouped by the cross-file policy component (1), the target is the claim cost per realized year with
the realized length as the weight, scored by the Gini per unit of that length (6, which replaces the base of 4). Open:
keep the length to 31 December as a feature, although it misleads a squared-error fit on the log1p scale (7)? Verdict:
ship (2026-11-03).

**Issues for Andrej:**

3. **Keep the claim amounts although their basis and valuation date are not stated?**

   * **Problem:**
     - The source says "Total claim amount of the guarantee" and no more.
     - It does not say whether the amounts are paid or incurred (paid plus reserves), or when they were valued.
     - Claims late in 2004 may have been valued before they settled: a target cut short in the newest period[^3a].
   * **Effect on the task:** if year-end claims were valued before they settled, the records that run to 31 December
     carry too low an amount in training and test alike, so the benchmark asks for the cost as valued, not the final
     cost an insurer prices; the grouped folds put the same mix on both sides.
   * **Experiments:** circumstantial evidence only[^3b]: claimants whose record runs to the end of the year have lower
     amounts (median 749) than those whose record ended earlier (799 to 1,086 by quarter). That fits immature year-end
     claims, and it also fits claims that end a contract (theft, write-off).
   * **Unknown:** one year of data cannot separate the two readings. The CASdatasets maintainers (Dutang, Charpentier)
     are the people to ask (option B).
   * **Consistency:** the rule on targets cut short is not shown violated[^3a]. A label whose construction the source
     leaves undocumented ships with an approximate fit and a note naming the gap[^3c]. This follows
     blood_tests_drink_prediction and mobile_churn (the quantity known, its recording not), as do the australian and
     spanish drafts.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the note (implemented) | amounts as published; the unknown basis and valuation date named in the fit reason | follows the precedents; ships now | the target may be the cost as valued, not the final cost |
     | B | Ask the maintainers first | shipping waits for Dutang and Charpentier | could settle paid or incurred, and the valuation date | shipping waits on an answer |

   * **Recommendation:** A, keep with the note: one year of data cannot settle the question, and an undocumented label
     ships with a note, as blood_tests_drink_prediction and mobile_churn did. **Decision:** A or B?

   [^3a]: **LEAK-24** (Must): a target right-censored in the newest periods (a duration or a final status cut by the
     download date) is cut where follow-up is complete, or re-sourced from an archive with settled labels.
   [^3b]: **EV-6** (Should): say which evidence is proof (a test that could have refuted the claim) and which is
     circumstantial.
   [^3c]: **USE-5** (Must): a label from a named publication whose construction is undocumented and cannot be checked
     may ship with `fit="approximate"` and a note naming the gap. Cases under this clause: blood_tests_drink_prediction,
     mobile_churn.

   **Resolved (2026-11-03, Andrej):** A, the amounts stay as published with the note on their unknown basis and
   valuation date.

1. **Group the folds by policy chain, or by the cross-file policy component?**

   * **Problem:**
     - The folds are grouped by policy, since a policy's later records give an earlier record's claim away, but the
       release has no policy id.
     - The choice is the key: the exact chain within a file, or a cross-file component that also joins 10,292 records.
   * **Background:** a policy whose contract changed during 2004 has several records:
     34,324 records continue in the next row of their file (same profile, starting the day the previous one ends; 1
     such link by chance with the rows shuffled). A later record's claim counters include the earlier record's claim:
     they rise after 87% of its claims and after 0.9% of its non-claims. Under random folds, about 8,000 training rows
     per fold were later records of a test record. An insurer pricing the test record could not have them: they did
     not exist yet. A shortcut that can be measured is always removed, so the folds are grouped by policy[^1a][^1b].
     The choice left is the key: the chain joins records only within a file (exactly, 1 chance link); the cross-file
     component also joins the 10,292 records that continue in another file.
   * **Experiments:** paired, same test rows, random folds, before the `Exposure` fix. Give a model a lookup that
     finds, among the training rows, the record that looks like the test record's next one (same profile, licence age
     advanced by the record's length) and checks whether its counters rose. It scores a Gini of 0.395 against 0.280
     without the lookup. Drop those later records from training and the gain falls to 0.013 (3/3 folds). LightGBM
     alone scores the same either way, because it reads one row at a time; that is why the split auditor's test found
     no effect. Grouping costs nothing measured (untuned LightGBM on the shipped frame: Gini 0.332 grouped against
     0.329 random, claim AUC 0.673 both).
   * **After the fix:** on the shipped folds (chain key) the lookup now lowers the model's Gini on 8 of 9 splits (by
     0.038 on average): the fix gave many unjoined records the length known at their start, which breaks the lookup's
     match. The lookup ranks those unjoined records' claims at AUC 0.51; a lookup that leaves the length out ranks
     claims at AUC 0.53 and moves the Gini by -0.02 to +0.01 (3 splits). So the unjoined records no longer give claims
     away, and the component would close a path that is no longer measured.
   * **Component key:** before the fix, the lookup's signal was gone under it (lookup alone AUC 0.507 against 0.545 by
     chain), at no measured cost (Gini 0.2785 against 0.2827). After the fix the chain leaves about as little, so the
     gain from the component key is now small.
   * **Consistency:** grouping matches pricing_game_2017_french_mtpl (grouped by client) and
     spanish_motor_insurance_coverage_level_2022_2024 (grouped by policy). A group key must be a true id or one built
     exactly from the data, never a similarity match[^1c]. The chain meets it, built exactly from the raw order as in
     in_vehicle_coupon_recommendation.
   * **Panel:** the advocate and the critic recommend the chain. The split auditor preferred random records; the paired
     test above settles that.
   * **Unknown:** whether in-context models such as TabPFN take the lookup path is untested. Whether the component,
     with its age tolerances and about 1% chance links, counts as built exactly is the reading you decide[^1c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Policy chain (implemented) | one group per chain of consecutive rows in a file, 80,831 groups | exact key, 1 chance link | leaves the 10,292 cross-file continuations unjoined |
     | B | Cross-file policy component | also joins records across files, 68,882 groups | closes the cross-file path, at no measured cost | links rest on equal profiles and dates with age tolerances, about 1% by chance; gain now small |

   * **Recommendation:** A, the chain: it is an exact key, and after the `Exposure` fix the records it leaves unjoined
     no longer give claims away. **Decision:** A or B?

   **Notes for the AI:** the chain is the group column `policy_chain` in `dataset.py`, the regime
   `ForcedGroupedFromTemporal` (SPLIT-8). The splits comment and the Grouping text hold the numbers above.

   [^1a]: **SPLIT-9** (Must): a training row whose label is not yet known at the prediction point must not be in
     train. Its tension row in principles.md: "a shortcut that can be measured is always removed". With **LEAK-5**
     (Must): never argue "not a leak" because models would predict the same; ask whether the stored values depend on
     the test rows.
   [^1b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give valid windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal; here grouped by the entity,
     `ForcedGroupedFromTemporal`.
   [^1c]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data; never on a
     similarity-threshold cluster. Here exactness weighs against coverage. Cases include in_vehicle_coupon_recommendation.

   **Andrej (2026-11-03, discuss):** What is the most conservative option that is the safest to not leak? Also, why
   can't we do a temporal split via a reconstructed time feature?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - The most conservative key is B, the cross-file policy component: it joins every record that may be a later
       record of the same policy, also across the five sample files, so no later record of a test policy stays in
       training.
     - Its chance links (about 1%) only put two unrelated policies into one group, which makes the split stricter,
       never leakier, so the exactness worry of the rule is about cost, and the cost measured is nothing.
     - A temporal split is possible from the record dates, but within one year it trains on few and unusual records.
   * **Why not a temporal split:**
     - The release covers 2004 only, and a record's claim is known when its period ends. Most records run to
       31 December, so at a cutoff inside 2004 the only records with a known label are those that already ended:
       13%, 26% and 39% of the rows at 1 April, 1 July and 1 October.
     - Those are the contracts that ended early, often because of the claim or a change of car, not the book an
       insurer trains on; and the windows fall below the rule that a window trains on at least half the rows[^1d].
     - On the next three months' records they rank claims at AUC 0.55, 0.59 and 0.62, against 0.60, 0.59 and 0.62
       for as many random records, so they test nothing a grouped split does not.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Policy chain (implemented) | one group per chain of consecutive rows in a file, 80,831 groups | exact key | leaves 10,292 cross-file continuations unjoined |
     | B | Cross-file policy component | also joins records across files, 68,882 groups | the most conservative key; closes the cross-file path; costs nothing measured (Gini 0.2785 against 0.2827) | about 1% of the links join unrelated policies, which only makes the split stricter |
     | C | Temporal windows inside 2004 | train on the records ended before a cutoff, test on the next three months | follows time | trains on 13% to 39% of the rows, all early-ended contracts; below the half-the-rows rule |

   * **Recommendation:** B: you ask for the safest key, it is, and it costs nothing measured. **Decision:** A, B or C?

   **Notes for the AI:** on B, build the component in `_clean` from the raw order and dates as the panel did (age
   tolerances as in its script), restate the group counts in the Grouping text and `splits_comment`, re-run
   `dataset check` and the leak probe.

   [^1d]: **SPLIT-14** (Must): a temporal window trains on at least half of the rows.

   **Andrej (2026-11-03, change):** I choose B

   **Resolved (2026-11-03, Andrej):** B. The group column is now `policy_component`: records joined where one may
   continue another, in the next row of its file or in another file (same profile, starting the day the other ends,
   driver's age the same or one more, licence age advanced by the months between the starts within one), 68,857
   components of 1 to 13 records. `dataset check` is clean; the leak probe on the new folds flags nothing (no feature
   alone above 0.025 R^2 on log1p, 0.2% of test rows with an exact feature copy in training).

4. **Keep the row Gini, or score the exposure-weighted Gini on the cost per year, for the whole insurance family?**

   * **Problem:**
     - The declared Gini counts each record once, whatever its length (1 day to 1 year).
     - An actuary compares tariffs by a Gini that sorts by predicted cost per year of cover and counts each record by
       its exposure.
     - Which form scores this table?
   * **Background:** the declared Gini is the form of Allstate's Kaggle competition and sorts the records by predicted
     claim cost. The actuary's form is that of CAS Monograph 5, sec. 7.2.4; Liberty Mutual's competition also
     weighted.
   * **Effect on the task:** the row Gini rewards knowing which records are long nearly as much as which are risky.
   * **Experiments:** on the 9 shipped splits, after the fix of issue 2, sorting the records by length alone already
     scores 0.277 of the model's 0.332 (83%). Under the weighted form, length alone scores about 0, and the fold scores
     vary less (SD 0.027 against 0.069). Both forms rank the model with the length above the one without it (9 of 9
     splits row, 6 of 9 weighted), so the row form still scores the real task and the choice is a weighing[^4a]. The
     critic withdrew its objection on that measurement.
   * **Consistency:** the weighted form needs the same answer for australian_vehicle_insurance_2004_2005 and
     spanish_motor_insurance_coverage_level_2022_2024. pricing_game_2017_french_mtpl is unaffected: every row is a whole
     policy-year, so the two forms coincide (its issue 2); pricing_game_2016_french_fleet is binary, scored by ROC AUC.
   * **Panel:** the domain practitioner and the advocate recommend the weighted form; the critic leaves the form to
     you. The practitioner's metric and the better resolution favour the weighted form; a scoring column counts
     against it.
   * **Not proposed:** capping the losses at 50,000 (the practitioner's other suggestion: fold SD 0.044 to 0.012). It
     changes the recorded target, and unusual values stay, so the 802,620 claim is kept (precedent check,
     qsar_tid_11)[^4c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Row Gini (implemented) | sorts by predicted claim cost, each record counts once; its reason corrected (what the cited sources score, the length's share, the swing of about 0.10 from one claim) | no scoring column | length alone scores 83% of the model's Gini; fold SD 0.069 |
     | B | Exposure-weighted Gini on the cost per year | sorts by predicted cost per year, weights each record by its realised `Exposure`, a scoring column and never a feature[^4b] | the practitioner's metric; length alone scores about 0; fold SD 0.027 | a scoring column; not normalized; asks the same of the australian and spanish tables |

   * **Recommendation:** B, decided once for the family: it is the practitioner's metric, length alone scores about 0
     under it, and its fold scores vary less (SD 0.027 against 0.069). Shipping frempl does not wait for it: the row Gini stays
     until you choose. **Decision:** A or B?

   **Notes for the AI:** B uses `ordered_lorenz_gini` (added on 2026-11-01 for
   wisconsin_local_government_property_insurance_fund): it sorts by prediction / base with the base in the `weight`
   role, here the realised `Exposure`, where `normalized_weighted_gini` sorts by the raw prediction.

   [^4a]: **MET-1** (Must): the declared metric scores the real task, the way a practitioner would choose a model
     for it; the row form passes it. The choice then falls under **MET-11** (Must: every metric has one origin, named
     in the notes) and **MET-10** (Weigh: the factors on a borderline call, among them the source's track record and
     the resolution on our folds).
   [^4b]: **MET-2** (Must): every input the metric needs ships as a column and is never a feature.
   [^4c]: **CLEAN-11** (Should): impossible values become missing; values that are only unusual stay. Precedent check:
     qsar_tid_11.

   **Answer (AI, 2026-11-02):**

   * **Found:** there is no family decision on the metric: you decided case by case while reviewing
     pricing_game_2016_french_fleet, with diversity when in doubt[^4d].
   * **Now:** the question is this table's alone: A or B for frempl, on its own evidence; when in doubt, the form the
     collection has fewer of.

   [^4d]: Andrej, 2026-11-02, on pricing_game_2016_french_fleet: "It is case by case and when in doubt we go for
     diversity"; **MET-10** as amended: the metric is chosen per dataset, never as one call for a family of datasets,
     and when the call stays in doubt, the metric that adds diversity to the collection wins.

   **Andrej (2026-11-03, change):** We go with B. But that you say 'asks the same of the australian and spanish
   tables' as a con is something I don't understand. We don't care about other tables, only what is the best decision
   for this one. Also, please explain why not normalized is a con

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Before applying B I measured it on the shipped splits, and B as written leaks: it divides by the realised
       length, which is not known when a record starts, so even a constant prediction scores 0.184.
     - The fix is a different base, the length known at the start (the feature `Exposure`): then the length alone
       scores 0 and the model 0.137.
     - B is therefore not applied; the row Gini stays until you choose between the options below.
   * **Your two questions:**
     - The other tables: you are right, they are no reason for or against a choice here; that con is removed.
     - Not normalized: it is no real con. The weighted Gini is not divided by the best possible score, so its top
       value differs from fold to fold; models are still ranked the same within a fold, and only the mean over
       folds mixes slightly different scales. I listed it wrongly.
   * **Why B leaks:** a record that ended early, often because of its claim (a write-off, a theft), has a short
     realised length. Dividing any prediction by that length ranks those records high, so the metric itself reads
     the end of the record that the features were cleaned of (issue 2). The panel measured "length alone about 0"
     before that cleaning, when the feature still was the realised length.
   * **Experiments:** untuned LightGBM on the 9 shipped splits:

     | Scoring | Model | Length alone | Constant prediction | Model without the length | Spread of the model (SD) |
     |---|---|---|---|---|---|
     | row Gini (A) | 0.319 | 0.277 | 0 | not measured | 0.067 |
     | weighted, realised length as base (B) | 0.233 | 0.203 | 0.184 | 0.246 | 0.042 |
     | weighted, length known at the start as base (C) | 0.137 | 0.000 | not measured (see Resolved) | 0.170 | 0.036 |

     - Under C a model scores only for ranking the cost per year of cover, which is what an actuary compares
       tariffs by; the length alone earns nothing.
     - C's base is the length known at the start, rounded to whole months in the feature; the scoring column takes it
       unrounded, so no record has a base of 0.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Row Gini (implemented) | sorts by predicted claim cost, each record counts once | no scoring column | the length alone scores 0.277 of the model's 0.319; fold SD 0.067 |
     | B | Weighted, realised length as base | as first proposed | the panel's form | leaks the record's end: a constant prediction scores 0.184 |
     | C | Weighted, length known at the start as base | sorts by prediction / the length known at the start, weights by it; a scoring column, never a feature | the actuary's metric; length alone and a constant score 0; fold SD 0.036 | a scoring column that repeats a feature's value unrounded |

   * **Recommendation:** C: it is the practitioner's metric without the leak. **Decision:** A, B or C?

   **Notes for the AI:** on C, `Metric.from_context("ordered_lorenz_gini", inputs={"weight": "exposure_at_start"})`
   with a `ScoringColumn` `exposure_at_start` (the known-at-start length before the month rounding); the measurement
   script is `frempl/weighted_gini.py` in the run folder of 2026-11-03.

   **Andrej (2026-11-03, change):** I go with your option C

   **Resolved (2026-11-03, Andrej):** C. The metric is `ordered_lorenz_gini` with the scoring column
   `exposure_at_start` as its base. On the shipped component folds untuned LightGBM scores 0.147 (0.052 to 0.179),
   random predictions 0.049 on average (0.015 to 0.104), the same models' row Gini 0.324. A correction to the answer
   above: under C the zero point is a prediction proportional to the length known at the start (the same cost per
   year for every record), not a constant one; a constant total cost per record ranks short records first and was not
   measured. The metric reason says so.
   The base is the feature `Exposure` before its rounding, as measured for C: continued records keep their realised
   length in it, as in the feature (the leak kept on purpose in issue 2), so their ratio stays neutral. Checked on
   2026-11-03: with the known-at-start length for them too, the length alone would score 0.176 of a model's 0.249.

6. **Ship the claim cost per realized year, weighted by the realized length, with the length to 31 December as the
   feature?**

   * **Problem:**
     - The `Exposure` feature of 2026-11-02 held the realized length on the 34,324 records that continue in a later
       record, a length known only when they end, and the length known at the start on the others.
     - The metric of issue 4 took the same mix as its base (`exposure_at_start`), and the target was the period's
       total, which grows with the realized length.
     - The exposure study of 2026-11-05 proposed the cost per realized year as the target, the realized length as the
       weight of the metric and of training, and the length to 31 December, known at the start, as the feature (its
       decision D9)[^6a].
   * **Background:**
     - The 115,155 records form 68,857 policy components: 55,700 records are open at 31 December, 34,324 continue in
       a later record of their file and 25,131 end earlier without a continuation.
     - Claims cut records short: the records that ended alone cost 837 per realized year, the continued ones 407 and
       the open ones 311.
     - An actuary prices the cost per year of cover and compares tariffs by the Gini of the ordered Lorenz curve: the
       records sorted by the predicted cost per year, each counted by its exposure.
   * **Effect on the task:** a model reads no realized length any more, so it ranks the cost per year from what an
     insurer knows when the period starts; each record counts in training and scoring in proportion to its time on
     risk.
   * **Experiments:** on the 9 shipped splits, untuned LightGBM weighted by the realized length, 3 seeds:
     - an honest model scores 0.183 with a Tweedie loss on the cost per year and 0.156 with squared error on the
       log1p scale; the weighted constant scores 0 and random orders 0.003 on average;
     - 1/realized length alone scores 0.184, above the Tweedie model on 4 of 9 splits; the realized length added as a
       feature lifts the Tweedie model to 0.256 (+0.073, higher on 9 of 9);
     - the old hybrid length in place of the length to 31 December scores 0.018 lower with the Tweedie loss (higher on
       1 of 9 splits); its kept part was worth about 0.045 under the metric of issue 4 (the exposure study).
   * **Consistency:** fremtpl2 and bemtpl97 moved to the claims per year insured with the exposure as the weight on the
     same day[^6b]. It departs from Andrej's call of 2026-11-03 (issue 4, option C)[^6c]; what sets the case apart:
     under the rate a constant scores 0, whereas option B scored totals against a realized base, where a constant
     scored 0.184; the leak rule now keeps 1/length out of the features.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Total with the hybrid length | the definition of 2026-11-03: log1p of the period's total; `Exposure` a feature; the Gini on the base known at the start | no training weight | the realized length stays in a feature on 34,324 records; worth about 0.045 under that metric |
     | B | Cost per realized year, weighted (implemented) | log1p of the amount per realized year; `Exposure` the weight and `sample_weight`, never a feature; `length_to_year_end` a feature; the Gini per unit of `Exposure` | the actuary's form; a constant scores 0; no realized length in the features | 1/length alone scores at the honest model's level; learners differ by loss (issue 7) |

   * **Recommendation:** B, the exposure study's D9: no realized length in the features, and the metric scores the cost
     per year by the exposure. **Decision:** A or B?

   [^6a]: **LEAK-41** (Must, 2026-11-06): a column the task uses as a weight or as a rate's denominator whose value is
     set or cut after the prediction point is never a model input, whatever it scores, nor is a column that encodes
     it, such as a length corrected on some rows and realized on others. **MET-14** (Should) and **MET-15** (Must): a
     count or amount over a varying time on risk ships as the rate per unit, and its realized denominator is the
     metric's row weight and the task's `sample_weight`, never a feature.
   [^6b]: fremtpl2 issue 6 and bemtpl97 issue 1, resolved 2026-11-06 (Lennart); the exposure study of 2026-11-05.
   [^6c]: Andrej, 2026-11-03, issue 4: "I go with your option C", the length known at the start as the base; option
     B, the realized base, was set aside because a constant prediction scored 0.184 under it.

   **Resolved (2026-11-06, Lennart):** B, decision D9 of the exposure study of 2026-11-05. The target is
   `log1p_claim_amount_per_year`, log1p of `ClaimAmount` / `Exposure` (the log1p scale kept, CLEAN-16 as amended: a
   rate scored by a Gini keeps the curator's scale). `Exposure`, the realized length (0.001 to 1 year, positive on
   every record, so no row goes under USE-7), is the weight scoring column, the `weight` input of
   `ordered_lorenz_gini` with `per_unit` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15).
   `length_to_year_end`, the length the source gives a record open from the same start day to 31 December, is the
   feature (CLEAN-22, USE-6), unrounded: the month rounding of 2026-11-02 only hid the decimals of the realized
   length, and rounded it would make 2,704 records repeat another record of their policy. `exposure_at_start` is
   dropped. Supersedes Andrej's call of 2026-11-03 (issue 4, option C); his unnormalised CAS form stays. On the shipped
   splits an honest Tweedie LightGBM scores 0.183, squared error on log1p 0.156, the weighted constant 0 and
   1/`Exposure` alone 0.184. A model that reads a test record's next record, a test row too under the grouped split,
   reaches 0.443, so the notes and the splits comment carry a protocol line: no feature or model step may use other
   test rows, and a method that does is called out and not benchmarked (LEAK-9). `dataset check`: 0 errors, 0
   warnings (the warning `task_feature_looks_like_exposure` is gone).

7. **Keep the length to 31 December as a feature, although it misleads a squared-error fit on the log1p scale?**

   * **Problem:**
     - Issue 6 keeps the target on the log1p scale and the length to 31 December as a feature, and a squared-error fit
       on that scale ranks short periods too low when it sees the length.
     - On the shipped splits such a fit scores 0.156 with the length and 0.185 without it, while a Tweedie fit on the
       cost per year scores 0.183 with it and 0.179 without.
     - The rule on log-scale rates asks to drop such a feature or to ship the identity scale[^7a], and the decision of
       issue 6 keeps both the feature and the scale[^7b].
   * **Background:**
     - A squared-error fit on log1p of the cost per year estimates the exposure-weighted mean of log1p(cost per year),
       not the cost per year the Gini orders by.
     - A short period's cost per year is large when it has a claim, but a claim is rarer, so that mean rises with the
       time to 31 December (0.29 up to 3 months, 0.98 to 1.08 from 9 months on) while the cost per realized year stays
       at 394 to 469 and the claims per realized year at 0.20 to 0.22.
     - The length to 31 December equals the realized length on the 55,700 records open at the year end and bounds it
       on the others.
   * **Effect on the task:** most regression learners fit squared error on the target as shipped; with the length they
     lose about 0.03 of Gini for a reason unrelated to the risk, while a learner with a Tweedie loss gains 0.005 from
     it.
   * **Experiments:** untuned LightGBM weighted by the realized length, the 9 shipped splits, 3 seeds:
     - squared error on log1p: 0.156 with the length, 0.185 without (lower with it on 7 of 9 splits, -0.029, SE 0.010);
     - Tweedie on the cost per year: 0.183 with it, 0.179 without (higher with it on 5 of 9, +0.005, SE 0.004);
     - squared error on the cost per year itself: 0.159 with it, 0.163 without, led by the tail (up to 11.6 million
       per year, a claim of 58,087 on a record of under two days);
     - without the length, squared error on log1p scores as the Tweedie fit with it (+0.001, higher on 6 of 9).
   * **Consistency:** the rule's example is spanish_motor_insurance_coverage_level_2022_2024, whose log1p rate shows
     the same rise across exposure bands[^7a]; the length to 31 December is known at the start, and an input known at
     the prediction point is legitimate[^7c].
   * **Unknown:** only LightGBM was measured; other squared-error learners should show the same trend, which sits in
     the target's weighted mean by length.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the length on log1p (implemented) | as issue 6 decided | an input known at the start stays; a Tweedie fit gains 0.005 | squared-error fits on the shipped scale lose 0.029 (7 of 9 splits) |
     | B | Drop the length | `length_to_year_end` leaves the features; target, scale and weight unchanged | squared-error and Tweedie fits score alike (0.185 and 0.179); keeps your scale | drops an input known at the start, worth 0.005 to a Tweedie fit |
     | C | Identity scale | the cost per year ships untransformed; the length stays | a squared-error fit then estimates the cost per year | squared-error fits score 0.159, led by the tail; departs from the curator's scale |

   * **Recommendation:** B: the length is worth +0.005 (SE 0.004) to the loss that suits the metric and costs the
     common loss 0.029, and dropping it keeps the log1p scale. **Decision:** A, B or C?

   **Notes for the AI:** on B, drop `length_to_year_end` in `_clean` (the asserts on the length known at the start
   can stay), rewrite `known` and `changes` in the task summary, the bullets on the length, the learners and the
   ceiling and the metric reason's numbers, then re-run `dataset check`, the leak probes and the measurement of
   2026-11-06; on C, ship `claim_amount_per_year` with `target_transform="identity"` and re-measure.

   [^7a]: **CLEAN-16** (Should; amended 2026-11-06, Lennart): a rate scored by a Gini keeps the scale the curator chose
     for the table, and the notes say what a weighted fit on that scale estimates; a log-scale rate with its
     denominator as a feature misleads squared-error fits (spanish_motor_insurance_coverage_level_2022_2024: the mean
     log1p of the rate rises from 0.085 to 1.074 across exposure bands while the cost per year stays at 221 to 336):
     drop the feature or ship the identity scale.
   [^7b]: Lennart, 2026-11-06, D9: the target on the log1p scale as before, and the length to 31 December, known at
     the record's start, stays a feature.
   [^7c]: **USE-6** (Must): anything known at the prediction point is a legitimate input. **CLEAN-22** (Must):
     columns leave for what they are, never for how many there are.

**Review panel:** ship after changes (mediator). Claim audit: 39 claims, 26 hold, 4 refuted and 3 refuted in part (all
fixed or reworded), 3 refuted in the record only, 3 untested. Blind review: include with changes; its main concerns are
the weak signal, mostly from `Exposure`, and the realised `Exposure`. Settled by the mediator: grouped folds over the
split auditor's random records (the paired lookup test, D1) and the `Exposure` fix over the precedent checker's keep
(LEAK-10 by rank, D2). Agreed: the text fixes. Left to Andrej: the key (issue 1), the `Exposure` fix as a departure from
fremtpl2 (issue 2) and the Gini form for the family (issue 4).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): frempl_french_motor_personal_line**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1 holds (Gender noted); SEL-2 and USE-1 hold, fit approximate (USE-8). SPLIT-9 triggered (with LEAK-5):
  under random records about 8,000 training rows per fold are later records of a test record's policy, and their
  claim counts give the test claim away to a model that reads training rows (+0.09 Gini, 3/3 folds, gone when those
  rows leave train; mediator's paired test); fixed by grouping on the within-file policy chain,
  ForcedGroupedFromTemporal (SPLIT-8, SPLIT-24). LEAK-10 triggered on `Exposure` for the 25,131 records that ended
  early with no continuation; fixed by LEAK-7 (the length known at the start, rounded to months). LEAK-10 holds for
  the other 15 features. LEAK-24 cannot verify (evaluation date of the amounts). PROV-7, PROV-8, PROV-9, PROV-13 hold.
Value: TP-2 a small real signal (keep); TP-4 holds (model 0.339 against the fixed length alone 0.281, 9/9, random
  folds; re-measure on the shipped folds); MET-11 context Gini kept, reason corrected; its form is a family weighing.
Quality: negatives clip kept with a corrected reason (EV-2); file note (EV-5) and record corrections (EV-2).
Weighed: source + (every column documented, version pinned), size +, a real tariff table +; signal - (claim AUC
  0.69, severity unlearnable), fold noise - (one claim moves its fold by about 0.09), a thin tariff - (no vehicle or
  cover factors).
For the curator: issue 1 (chain or component key), issue 2 (the Exposure fix against the fremtpl2 call, a
  consistency check), issue 3 (amount basis and evaluation date, cannot verify), issue 4 (row or exposure-weighted
  Gini, a family weighing).
```

**Agreed facts** (no agent disputes them; EV-8: untuned LightGBM, the builder's settings, unless noted)

- 115,155 records from freMPL5-9 of CASdatasets 1.2-1 (commit 3f5c00c), all ten checksums match; the blind reviewer
  rebuilt the target, log1p(clip(ClaimAmount, 0)), to 1e-10. 45 exact copies over 20 columns dropped (89 in groups).
- 967 negative amounts, all with `ClaimInd` = 0, set to 0. They are not "recoveries on earlier claims": 95.1% of those
  with a next record are followed by a rise of the not-at-fault counter (0.19% for zero records), so they are
  not-at-fault claims of the period whose recourse covered the payment. The clip stays (-2.4% of net cost; the
  pricing_game_2017 definition clips the same way); the text is wrong.
- 90.6% zeros; claim AUC about 0.69; severity not learnable (R^2 at or below 0); 3,540-3,740 claims per test fold.
- 15 of the 16 features hold the state at the record's start: a claim counter rises at the next record after 95.3% of
  claims and 2.3% of other records; `BonusMalus` moves at the anniversary (after 11.6% of claims).
- `Exposure` is the realised length. 51.6% of records end before 31 December; 25,131 (21.8%) end with no continuation
  in their file. Those hold 20.7% of the exposure, 38.9% of the claim cost (837 per exposure-year against 311 for open
  records) and 66 of the 109 largest claims. The exact 3-decimal value tells an ended record from an open one at
  AUC 0.91 (0.61 rounded to months; two agents, model and lookup).
- Policies have several records: 34,324 records continue in the next row of their file (1 by chance), 10,292 more only
  in another file. Under the shipped folds about a fifth of the test rows have a later record of their policy in
  train; its counters rise after 87% of the test record's claims and 0.9% of its non-claims.
- Grouping costs a row-wise model nothing measurable: 0.277 against 0.282 Gini by chain, 0.2785 against 0.2827 by
  component.
- Valid windows inside 2004 train on 13-39% of the rows (only contracts that had ended): claim AUC 0.55 / 0.59 / 0.62
  against 0.60 / 0.59 / 0.62 for as many random records. No window meets SPLIT-14, so SPLIT-8 applies.
- The files differ (claim rate 7.7-10.0%, one-vs-rest AUC 0.57-0.64), but leave-one-file-out scores like random folds
  (AUC 0.690 against 0.687), so stacking without a file column holds. "Near-random slices" and its accuracy evidence
  (EV-5) go.
- After the Exposure fix, the declared row Gini gives the fixed length alone 0.281 of the model's 0.339 (83%), fold SD
  0.052, against 0.019 for the exposure-weighted Gini on the annual rate (3 seeds x 3 random folds). The scorer is
  verified (equal to a hand-computed Gini on the amount).
- Year 2014 (NEWS of 1.0-7), licence GPL (>= 2); freMPL1 (39% of contracts in 5-9), freMPL2-4 and freMPL10 stay out.

**Changes to make now** (no decision needed; dataset.py unless marked)

1. Split (SPLIT-9 Must and its tension row, LEAK-5, SPLIT-8, SPLIT-24): in `_clean`, before `file` and the dates are
   dropped, build the within-file chain id as `_decisions` does and keep it as `policy_chain`; declare
   `grouping = Grouping(on="policy_chain", labels="per_sample", prediction_unit="row", context="none", definition=...)`;
   `data_tags = ("ForcedGroupedFromTemporal",)`. Rewrite decision 3, `task_summary.split` and `splits_comment` (chain
   counts within and across files; the lookup's +0.09 Gini under random records and its loss without the successors;
   the residual across files, issue 1).
2. Valid windows in `splits_comment` (SPLIT-8 Must, "with the cost measured against the valid windows"): 13-39% of the
   rows, only ended contracts, claim AUC 0.55 / 0.59 / 0.62 against 0.60 / 0.59 / 0.62.
3. `Exposure` (LEAK-10 Must, LEAK-7; the curator confirms in issue 2): in `_clean`, before the dates are dropped, give
   the records with `RecordEnd` and no within-file continuation the median `Exposure` of the open records with the
   same `RecordBeg` (fallback for a start day without one: days to 1 January 2005 / 365, floored to 3 decimals, capped
   at 1); then round every `Exposure` to whole months (`(Exposure * 12).round() / 12`). Measured on 3 seeds x 3 random
   folds: Gini 0.288 to 0.339 (9/9), claim AUC 0.689 to 0.675 (9/9); rounding costs nothing (0.338 / 0.674) and takes
   the code that marks a continued record from AUC 0.92 to 0.71. Label the rest `Potential leak, kept on purpose:`
   (continued records keep their realised length: 407 against 311 per exposure-year; revisit if a release gives the
   contracted term or why a record ended). Replace "the family's call of 2026-10-30" with "the AI's suggested call of
   2026-10-30" and cite fremtpl2's CC with the fact that sets this case apart. Update decision 1, the dates bullet ("the
   exact value alone gave the end away, AUC 0.91") and the `fit_reason` clause.
4. Re-measure on the rebuilt folds and restate (EV-8): the TP-4 note (model against the fixed length as a raw score),
   the Gini figures in the notes and the metric reason.
5. Metric reason (MET-1, MET-11, EV-2): Frees, Meyers and Cummings order by the relativity to a premium; Liberty Mutual
   scored a weighted Gini; Allstate's rows were whole vehicle-years. Say the row Gini scores the period's total cost,
   length included (the fixed length alone 0.281 of 0.339), and that the 802,620 claim moves its fold by about 0.09.
6. Negatives (EV-2): "0 = no claim, or a not-at-fault claim whose recourse covered the payment (0.84%)" in `predicted`,
   the negatives bullet, the target bullet, decision 2 and the acceptance reason of `task_target_value_dominant`.
   AIcrowd's game ran in 2020-21 on the 2017 game's portfolio.
7. Files bullet (EV-5, EV-2): the claim rate by file, the per-file AUC and leave-one-file-out instead of the accuracy;
   "samples of one portfolio drawn differently, sharing policies across files".
8. Smaller text (EV-2, USE-5): the counts bullet "a rise after 95% of the claims, 2.3% otherwise" (the 12% counted falls
   out of the 4-year window); `task_summary.known`: `OutUseNb` counts out-of-use periods, not claims; first bullet: 38%
   of records start on 1 January, the calendar cut; `fit_reason`: the amount spans every counted claim type (of claims
   with one counter rise: windscreen 40%, at fault 28%, not at fault 17%, parking 9%, fire-theft 6%), paid or incurred
   and the evaluation date not stated.
9. Record (no mark needed): the screening's empty year (2014), "no record spans all of 2004" (3,805 do), "431 pairs
   against 309, policyholders cannot be traced" (34,324 links, 1 by chance), the file sizes (16,000-32,400 in 1.2-1),
   "near-random slices", and the negatives reading. Record fields: `required_split` and the `Larger IID Data` tag
   (field rows in the review draft).

**Changes that need the curator** (ranked; details in the review draft)

1. P4, SPLIT-24 (Must) with SPLIT-9: group on the within-file chain (implemented) or on the cross-file policy
   component. Chain grouping leaves a lookup-alone AUC of 0.545 (component: 0.507); with the lookup the model gains
   +0.014 Gini on average (one fold +0.037) and loses 0.006 claim AUC. The component key links on exact profile and
   date continuity with age tolerances, with about 1% chance links (465 under a 7-day shift). A weighing of exactness
   against coverage.
2. P4, LEAK-10 (Must): confirm the Exposure fix, which departs from fremtpl2 (CC, Andrej, 2026-10-20). Fact that sets
   frempl apart: the dates locate the early ends row by row, and the shipped value encoded them. Keeping the realised
   length would be an amendment of LEAK-10, not a kept-leak note.
3. P4, LEAK-24 (Must) and USE-5, cannot verify: paid or incurred, and when the amounts were valued. Keep with the note
   or ask the maintainers.
4. P6, MET-1 and MET-11: the row Gini (implemented) or the exposure-weighted Gini on the annual rate, for the whole
   insurance family (australian, spanish, the pricing games).

**Disputed points**

D1. **The split: random records (split auditor) or grouped by policy chain (claim auditor, advocate, critic).** The
two measurements answer different questions, so I ran the test that separates them
(a script in the run folder, not committed). Shipped folds of repeat 0, the same test rows; training
side A drops as many random rows as B drops successors (training rows that are later records of a test record's
chain, 7,852-8,055 per fold). The lookup is the claim auditor's, built from features only.

| training side or split | plain LightGBM: Gini / claim AUC | with the lookup: Gini / claim AUC | lookup alone, AUC |
|---|---|---|---|
| A: shipped, random rows dropped | 0.280 / 0.688 | 0.395 / 0.739 | 0.626 |
| B: shipped, successors dropped | 0.290 / 0.688 | 0.303 / 0.686 | 0.545 |
| folds grouped by within-file chain | 0.275 / 0.688 | 0.288 / 0.682 | 0.545 |
| folds grouped by cross-file component | 0.286 / 0.689 | 0.236 / 0.653 | 0.507 |

Paired A minus B: plain Gini -0.009 (-0.013, -0.017, +0.002), plain AUC +0.000; with the lookup, Gini +0.092 (+0.096,
+0.067, +0.113) and AUC +0.053, 3/3 folds.
- Fact settled: both auditors measured correctly. The information that gives the test claims away sits in the
  successors on the training side. A row-wise model cannot read it, so the split auditor's paired test could not have
  come out the other way (EV-6); a model that reads training rows gains 0.09 Gini from it. Whether TabPFN-class models
  take it stays untested (no in-context model in the environment; EV-7).
- Rules: the split auditor rests on SPLIT-29/SPLIT-30 (re-split only for an entity new data would not have) and USE-10
  (a known policy's history is legitimate). The others rest on SPLIT-9 (Must: a training row whose label is not known
  at the prediction point stays out), its tension row ("a shortcut that can be measured is always removed") and
  SPLIT-8. LEAK-5 (Must, part 3) adds: "models would predict the same" is no argument when the stored values depend on
  the test rows, and the successors' counters depend on the test record's claim.
- No conflict: SPLIT-29/30 and USE-10 cover recognising an entity and its past. A successor is the policy's future: it
  does not exist when the record is priced. Grouping keeps the past, since the counters and `BonusMalus` carry it as
  features. So SPLIT-9 must hold on its own, and the remedy is the second rung (re-split). SPLIT-8 names the regime:
  grouped by the entity when periods are stacked and entities recur, `ForcedGroupedFromTemporal`. Cost: none measured.
- Left open: chain or component key (issue 1).

D2. **`Exposure`: keep as recorded (precedent checker, following fremtpl2; the practitioner does not reopen it) or fix
(column and claim auditors, advocate, critic).**
- For keeping: the curator's fremtpl2 call ("the contracted period is known at pricing (a mid-year cancellation also
  shortens it)"); the precedent checker's test (every record given its start-known length: no consistent Gini gain).
  The strongest case, which no agent made: LEAK-11 (Should, narrows LEAK-10) keeps a late value that weakens the
  signal, and the shipped value lowers the declared Gini (0.288 against 0.339).
- For fixing: LEAK-10 (Must) puts out "a consequence of the target"; the unforeseen ends move with the outcome (2.7
  times the cost per exposure-year, 66 of the 109 largest claims), and they can be located row by row.
- Decision by rank: LEAK-10 (Must) holds. LEAK-6's narrowing covers only late values that cannot be located, which is
  not this case. The precedent checker's test is the "removing it changes no score" test that LEAK-10 rules out, and
  the targeted fix does change the score, 9/9. LEAK-11 does not reach a value that also raises the claim ranking on 9/9
  folds (AUC 0.675 to 0.689), as this one does through the end status. Remedy: LEAK-7 (the start-known value for the
  located rows).
- It departs from a curator precedent, so the curator confirms (issue 2). The fact that sets frempl apart is named.

D3. **The fallback if the curator keeps the realised length: a kept-leak note with month rounding (critic) or an
amendment (advocate).** The advocate is right on the form: a Must has no exceptions, and LEAK-6's narrowing does not
cover located cells, so keeping it changes the rule (principles.md, "Exceptions and amendments"). The critic's rounding
is useful either way. After the fix, the exact value marks the continued records (AUC 0.92); rounding to months takes
that to 0.71 at no cost (a script in the run folder, not committed), so it is part of change 3.

D4. **The metric: a failed MET-1 (critic's opening) or a family reading (advocate).** Settled on the critic's own
post-fix test: the order swap between the two Gini forms came from the leaking `Exposure`. After the fix, both forms
rank the model with length above the one without (9/9 row, 6/9 weighted). So it is no failed Must; which form is the
"clear context" of MET-11 is a weighing, and the curator's (issue 4).

D5. **Recording of the keep (precedent checker: `Note:` instead of `Potential leak, kept on purpose:`, no revisit
condition, an AI suggestion cited as "the family's call").** Agreed by all; mostly moot after change 3. The residual is
labelled, and the attribution is corrected.

**Consistency with precedent**

- fremtpl2 (CC, Andrej, 2026-10-20), `Exposure` kept: departed from, with the fact named (dates locate the early ends;
  the value encoded them). Issue 2 asks the curator.
- spanish_motor_insurance_coverage_level_2022_2024 (draft): reset the cancellations it could locate. Followed.
- australian_vehicle_insurance_2004_2005 (draft): kept with a note because it could not locate them. Different facts.
- Split: pricing_game_2017_french_mtpl (grouped by client, `ForcedGroupedFromTemporal`) and spanish (grouped by policy)
  now agree with frempl. nba_players_2016_2019 and open_university_learning_analytics_dataset are the SPLIT-8 cases
  for this tag. alfa_battle_2_0_task_2 (SPLIT-9: an entity's later rows telling the earlier outcome, removed) has the
  same mechanism. sarcoma (IID kept over a weak group, SPLIT-29) differs: no future rows there.
- Andrej, 2026-10-30, on SPLIT-8: "Forced IID is to be avoided at all costs." Change 1 takes frempl off forced IID. It
  ships forced grouped under SPLIT-8, which stays unchanged, as pricing_game_2017 does. His `No` on
  how_much_did_it_rain rested on a leak that forced IID could not bound; here the measured path is removed and the
  remaining cost is measured (the valid windows).
- Target scale (consistency check B): frempl follows CLEAN-16 and MET-3 (Lennart, 2026-10-21). The question belongs to
  australian, which departs.
- MET-11 context Gini: no curator precedent yet. Once issue 4 is decided, it becomes a MET-11 Cases row for the three
  definitions; the `Exposure` answer becomes a LEAK-10 Cases row (precedent checker).
- `RiskArea` numeric: consistent with CLEAN-14 as amended ("categorical if we know from the context"; the source says
  "possibly ordered"). The column auditor's question is not raised.
- Library, for the working copy's REVIEW.md: `normalized_gini` breaks ties in row order, as the official code does,
  so a constant scores -0.016 to +0.101 depending on the frame order.

</details>

<details><summary>Claim audit</summary>

**Claim audit: frempl_french_motor_personal_line (claim-auditor, 2026-11-01)**

**Verdict: ship after changes.** Most of the counts and the provenance hold. Two validity claims are refuted, both in
P4 and both fixable in the definition at no cost to the declared metric:
1. The random split leaves later records of a test record's policy in train, and their claim counts give the test
   record's outcome away (SPLIT-8, SPLIT-9).
2. `Exposure` is the realised length, which for 51% of the records is known only when the record ends. The length
   known at the start is in the raw data (LEAK-10, LEAK-7).

The metric's reason cites sources that, for rows of unequal exposure, use an exposure-weighted Gini (MET-1, a weighing
call across the family).

Data: the definition's own frame and split plan (`make_splits`, 115,155 rows, 3 x 3 folds, seed 4267). Each shipped
row is mapped back to its raw row (dates, file) by replaying the frame's shuffle. Models are untuned LightGBM with the
builder's parameters (300 trees, lr 0.03, 31 leaves), fit on the log1p target. The Gini is scored on the amount
through `data_foundry.v2.metrics`. Scripts and outputs are in the run folder (not committed).

**Claims**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 115,155 records from freMPL5-9 of 1.2-1; 16 features | task_summary.row, README | rebuilt frame; sha256 of the 5 rda and 5 csv | holds | 115,155 x 17; all 10 checksums match the definition; commit 3f5c00c (2026-04-11, "update freMPL* files by removing duplicated rows") is still the last commit to touch `data/freMPL5.rda` | PROV-8 |
| 2 | 45 exact copies dropped (89 rows in groups; 10 within a file, 35 across) | notes, changes | `duplicated` over the 20 source columns | holds | 89 / 45 / 10 / 35 | LEAK-18 |
| 3 | After the dates are dropped: 29 repeat features and amount, 9 conflict | notes; info checks | duplicates on the shipped frame | holds | 29 exact rows; 9 conflicting groups (18 rows); 13-19 test rows per fold have their feature vector in train (0.03-0.05%) | LEAK-18 |
| 4 | 967 negatives (0.84%, -1,948 to -2), all with `ClaimInd` = 0, set to 0 | notes, decision 2 | counts after dedup | holds | 967 (0.84%), min -1,947.6, max -2.07, all `ClaimInd` 0 | CLEAN, USE-5 |
| 5 | "AIcrowd set negative totals to 0 on the portfolio of its 2017 pricing game" | notes | sibling record `pricing_game_2017_french_mtpl` | holds in substance, wrong wording | AIcrowd's game ran in 2020-21 on the 2017 game's portfolio and set 1,116 negative Year-0 totals to 0. "its 2017 pricing game" is wrong | EV-2 |
| 6 | `ClaimInd` is 1 exactly where the amount is positive | notes | assert on the deduplicated raw | holds | True on every row | LEAK-10 |
| 7 | `Exposure` = (end - start) / 365 within 0.006; 48% of records open at year end | notes | recomputed | holds | max deviation 0.0060; 48.4% open | - |
| 8 | Records that ended early claim more at the same length; Gini 0.251 / 0.273 / 0.294 | notes, decision 1 | builder's experiment1; my 9 shipped splits | holds | table reproduced. On my splits, start-known length + `Exposure` gives 0.302 against 0.283 shipped, the same direction | LEAK-10 |
| 9 | "`Exposure` is a feature ... the period is known when a policy is priced, apart from a contract that ends early" | notes (Note), fit_reason | `Exposure` against the length known at the start (start to year end, from the dropped `RecordBeg`), 9 shipped splits | **refuted in scope** | 51.3% of records ended early. Claim AUC: start-known length 0.633, `Exposure` 0.689 (9/9 splits), no length 0.565, so 45% of the lift from `Exposure` is known only at the end. Of the top 1% of claims, 74% ended early (51% of all records); the largest claim, 802,620, ended its record after 2 months (circumstantial: a claim ending the contract). Declared Gini: start-known length 0.292, shipped 0.283 (shipped wins 4/9, paired SE 0.015), so the fix costs nothing | LEAK-10 (Must), LEAK-7 |
| 10 | `Exposure` follows "the curator's call for fremtpl2 and the family's call of 2026-10-30" | notes | `fremtpl2` record; the records' Assessments of 2026-10-30 | **refuted in part** | The fremtpl2 call is the curator's (CC 2026-10-20). The 2026-10-30 table is the AI's suggestion per record: "The calls are suggested per record". The frempl CC of 2026-10-30 sets only `Yes`, priority 5 | principles, who decides |
| 11 | Raw `Exposure` ranks claims at 0.674 and losses at Gini 0.214; the model reaches 0.282 and wins on every fold (no lookup) | notes | 9 shipped splits | holds | 0.674 / 0.213 against 0.283; the model wins 9/9 | TP-4 |
| 12 | 34,324 records (30%) continue in the next row; 1 by chance; 80,831 chains of 1-6 | notes, splits_comment, decision 3 | `_continues_next` on the deduplicated raw | holds | 34,324; chain sizes sum to 80,831; shuffled control 1 (explore2) | SPLIT-24 |
| 13 | A claim does not make one in the next record likelier (8.3% against 9.2%) | notes | explore3 | holds | 0.083 / 0.092 | SPLIT-29 |
| 14 | "Folds that keep each chain together score like random ones ... so the split stays random"; "a pricing model scores the known policies of its portfolio too" | notes, splits_comment, decision 3 | (a) true links: is the test record's successor in train, and did its counts rise? (b) a lookup on the shipped features only (same profile, `DrivAge` +0/1, `LicAge` + 12 x `Exposure` within 1.5 months), added to LightGBM; (c) the same under chain-grouped folds | **refuted (as justification)** | (a) 19.4-20.0% of test rows have their successor in train. Its counts rose after 87% of claims and 0.9% of non-claims (AUC 0.93 on those rows, 90% precision, 17% of test claims flagged). (b) Shipped splits, repeat 0: Gini 0.282 -> 0.403, claim AUC 0.689 -> 0.741 (3/3 folds). (c) Chain-grouped: lookup AUC 0.54 (0.63 random); the model with the lookup gets AUC 0.680 against 0.689 and Gini 0.300 against 0.277 (one fold +0.065, two within ±0.007). The plain model loses nothing grouped (0.277 against 0.282). LightGBM cannot read other rows, so the builder's random-against-grouped test could not have come out the other way (EV-6). At a record's start its successor does not exist | SPLIT-9, SPLIT-8, LEAK-10 (Must) |
| 15 | "Random records, so the test data stands for other policies' periods in the same year" | task_summary.split | as 14 | **refuted** | 30% of records continue; a fifth of the test rows have a later record of the same policy in train | SPLIT-1 |
| 16 | The claim counts are taken at each record's start, never its own claim (change after 96% of claims, 12% otherwise) | notes; builder's claims | counts rise from k to k+1 depending on whose claim it is | holds | rise after a claim in k: 95.3%; after a claim only in k+1: 2.6%; neither: 3.1%. `BonusMalus` rises after a claim at only 11.6% (updated at the anniversary) | LEAK-10 |
| 17 | 90.6% zeros (89.7% as published plus the negatives) | predicted, notes, warning | counts | holds | 0.9056 shipped; 0.8972 published zeros after dedup | - |
| 18 | Claim AUC 0.69, severity R^2 -0.08 (amount) / -0.01 (log), oracle 9.6% | notes, metric reason | hurdle on the shipped splits, repeat 0 | holds | AUC 0.686-0.692; severity amount -0.154 / -0.002 / -0.206; log -0.007 to -0.023; oracle 0.160 / 0.021 / 0.133 (mean 0.105); hurdle R^2 -0.006 to 0.000 | TP-2 |
| 19 | Files 5-9 "are near-random slices of one portfolio" | notes; record | per-file rates against 200 random relabellings of the file | **refuted** | Claim rate by file 7.67-9.99% (chi2 80, p 2e-16); spread 0.023 against at most 0.0097 under random relabelling. Mean `BonusMalus` 56.3-61.4 (Kruskal p ~0); 1 January starts 30-42%; mean start day 102-127. They are samples drawn differently, not random cuts | PROV-7 (weigh), EV-2 |
| 20 | File sizes are round (16,000-32,400): samples of a chosen size; 1.2-1 removed "around 9995" duplicates per file | notes, download | pre-1.2-1 files (commit ef06f44) | holds, sharpened | Before 1.2-1: 26,000 / 42,400 / 36,600 / 34,000 / 26,200 rows, each with 10,000-10,004 duplicated rows. 1.2-1 removed exactly 10,000 per file, leaving 4 + 4 + 2 within-file copies, the 10 the definition drops | PROV-8 |
| 21 | freMPL1 repeats 39% of its contracts and amounts in 5-9; freMPL10 has another column list | notes (not re-measured by the builder) | freMPL1 and 10 of 1.2-1 matched on the 11 shared columns | holds | 8,041 of 20,566 keys (39.1%); 793 of 815 positive amounts equal; freMPL10 has 21 columns (adds `VehAge`) | PROV-7 |
| 22 | Year 2014: entered CASdatasets 9 Sep 2014 (NEWS of 1.0-7) | notes, `year` | `inst/NEWS` and `DESCRIPTION` at commit c49cbbb | holds | "freMPL1.rda 09/09/2014" ... "freMPL10.rda 09/09/2014" in the "Dataset list with entry date"; DESCRIPTION Version 1.0-7. The current NEWS page lists them only from 1.2-0 | PROV-9 |
| 23 | Licence GPL (>= 2) | `license` | DESCRIPTION at 1.0-7 and master | holds | "License: GPL (>= 2)" both | - |
| 24 | Source names no use; currency not stated; "Unknown French private insurer"; RiskArea "possibly ordered" | task_summary, notes | freMPL page and `man/freMPL.Rd` | holds | page quotes match ("Unkonw risk area between 1 and 13, possibly ordered"); no task or metric named | USE-1 |
| 25 | "the claims of the four preceding years by type" | task_summary.known | codebook | holds, loose wording | `OutUseNb` is "Number of out-of-use in the 4 preceding years", not a claim count | - |
| 26 | 46 CSP codes, 23 under 10 records; 47 licences before 17; top claim 802,620 = 3.6%, next 163,427, top ten 7.6% | notes | counts | holds | 46 / 23; 47; 0.0355, 163,427, 0.0764 | - |
| 27 | Metric computable per row; target_transform log1p scored on the amount | metric, README | scorer per fold with dummies; raw `Exposure` scored through the scorer against a hand-computed Gini | holds | 3,540-3,740 claims per test fold. The scorer gives 0.2627, equal to the Gini on the amount (0.3481 on the log1p values), so the inverse is applied. No scoring column needed | MET-2, MET-3 |
| 28 | "CASdatasets defines no task or metric ... no paper that defines a task on these tables was found" | metric reason | freMPL page, NEWS, one more search | holds | none on the page or in the NEWS. A web search found only freMTPL papers; arXiv 1808.08982 ("Combining Predictions of Auto Insurance Claims") draws a Lorenz curve, but its PDF could not be read, so which data it uses is unverified | MET-1 |
| 29 | Gini of the ordered Lorenz curve (Frees, Meyers, Cummings 2011), "the metric the insurers' own Kaggle competitions chose (Allstate 2011, Liberty Mutual 2014)" | metric reason | sources against the declared unweighted form; the declared metric against an exposure-weighted Gini (order by predicted cost / `Exposure`, x = cumulative exposure, y = cumulative loss) | **refuted in part** | Frees et al. order by the relativity to a premium (abstract and secondary sources; full text not read). Liberty Mutual scored a weighted Gini (`var11`; the sibling declares `normalized_weighted_gini`). Allstate's rows are whole vehicle-years (sibling record: "Exposure: none"). Here exposure runs 0.001-1. Raw `Exposure` gets 0.213 on the declared Gini (75% of the model's 0.283) and -0.05 on the exposure-weighted one, so the declared Gini mostly scores how well periods are ranked by length | MET-1 (Must), MET-11 |
| 30 | (implied) The fold score resolves models | metric | the per-fold Gini with and without the top claim; constant and random predictions | concern | One claim (802,620) moves its fold by about 0.09 (0.216 -> 0.308). SD over 9 splits is 0.044, and 0.018 without it. A constant scores -0.016 to +0.101 (ties broken by the fixed frame order); random predictions -0.094 to +0.036 | MET-10 |
| 31 | Warning `task_target_value_dominant` proposed for acceptance: 0 = no claim | builder | counts | holds | 0 = `ClaimInd` 0 on every row; 90.6% | - |
| 32 | Record screening: "the version that first held the tables was not found ... `year` stays empty" | record, screening | as 22 | **refuted** | NEWS of 1.0-7 lists 09/09/2014 (the definition already uses 2014) | PROV-9 |
| 33 | Record: "no record spans all of 2004"; "chaining ... finds 431 pairs against 309 by chance, so policyholders cannot be traced" | record, recommendation | counts; as 12 | **refuted** | 3,805 records run from 1 January to year end. 34,324 links, 1 by chance | EV-2 |
| 34 | Record: "Every file's row count is a multiple of 100 (20,600 to 38,300)" | record | as 20 | wrong range for 5-9 | 1.2-1: 16,000-32,400 (20,600 is freMPL1) | EV-2 |
| 35 | Record Assessment (2026-10-30): target `ClaimAmount`, `Exposure` a feature, negatives to 0, Gini context, pin 1.2-1, drop `ClaimInd` | record | against the definition | holds (implemented) | all applied; target shipped as log1p, scored on the amount | - |
| 36 | (implied) Every other feature is known at the record's start | - | 16; codebook | holds | ages, licence age, profile; counts start-dated (16); `BonusMalus` at the anniversary | LEAK-10 |
| 37 | (implied) Benchmark models take the shortcut of claim 14 | - | not run | **untested** | needs an in-context model (TabPFN, TabICL) on random against chain-grouped folds. LightGBM and KNN (which reads neighbours' labels, not their features) cannot | EV-7 |
| 38 | Which guarantee; paid or incurred; development date | fit_reason, builder | source | **untested** (cannot verify) | not in the page, the Rd or the NEWS | USE-5, LEAK-24 |
| 39 | freMPL2-4 amounts derived from freMPL1 (0.849 x) | notes (from the record) | not re-run | **untested** | needs freMPL2-4; it changes no decision, since those files stay out anyway | PROV-7 |

Count: 39 claims. 26 hold or hold in substance; 4 refuted (9, 14, 15, 19); 3 refuted in part (10, 29, and 5 in
wording); 3 refuted in the record only (32-34); 3 untested (37-39). Claim 30 is a concern, not a written claim.

**Refuted and untested, ranked (validity first, Must first)**

1. **The split (claims 14, 15; P4, SPLIT-9 and SPLIT-8, Must).**
   - What is wrong: under random records, a fifth of each test fold has the policy's next record in train. That
     record's claim counts rose after 87% of the test record's claims and after 0.9% of its non-claims. A lookup built
     from training features only (no labels, no dates, no file order) lifts the declared Gini from 0.282 to 0.403
     (3/3 folds).
   - SPLIT-8 already names the regime for this case: "grouped by the entity when the periods are stacked and the
     entities recur across them (`ForcedGroupedFromTemporal`)". The principles' SPLIT-9 tension: "a shortcut that can
     be measured is always removed".
   - What it changes: the regime and the tag.
   - Mildest remedy:
     - build the chain id in `_clean`; `_decisions` already computes it;
     - ship it as the group column, not a feature, with `Grouping(on=chain, labels="per_sample", context="none")`;
     - tag `ForcedGroupedFromTemporal`.
   - Cost: none measured (plain LightGBM 0.277 grouped against 0.282 random). Grouped, the lookup's gain is gone
     (AUC 0.680 against 0.689).
   - Residual: chain grouping still leaves a test record's successor in `X_test`. That is an evaluation-level path,
     which standard models do not take (LEAK-9).
   - Untested (claim 37): whether TabPFN-class models take the shortcut. It is no reason to keep the split, since
     the shortcut is measured.
2. **`Exposure` (claims 9, 10; P4, LEAK-10 Must, LEAK-7 Should).**
   - What is wrong: half the records ended early. The realised length carries 45% of what `Exposure` adds to the
     claim AUC (0.633 start-known against 0.689 realised, 9/9). Large claims end their records early more often (74%
     against 51%), circumstantial evidence of the outcome cutting the period short.
   - The length known at the start (start date to year end, equal to `Exposure` for every open record) scores the
     same on the declared Gini (0.292 against 0.283).
   - What sets this case apart from fremtpl2 (CC, kept) and australian (kept, "Revisit if a release gives the
     contracted term"): the start date exists here. Spanish 2022-2024 made the same fix where it could, giving
     cancelled portfolio years their start-known exposure.
   - Mildest remedy: replace `Exposure` by the start-known length, and say so in the notes and the task summary.
   - It departs from the curator's fremtpl2 call, so it is the curator's: a consistency check (a) treat as fremtpl2,
     or (b) the start date as the distinguishing fact.
   - Also correct "the family's call of 2026-10-30" to "the AI's suggested call", since the curator decided only
     the verdict and the priority.
3. **Files as "near-random slices" (claim 19; P5, PROV-7 Weigh).**
   - What is wrong: claim rates differ by file, 7.7-10.0% (p 2e-16, 2.4 times the largest spread of random
     relabelling); bonus-malus and start dates differ too.
   - Stacking without a file column stays reasonable: one schema, one insurer, a file is not known for a new record.
   - Mildest remedy: reword the note ("samples of one portfolio drawn differently, claim rate 7.7-10.0% by file; why
     is undocumented") and the record. The fit reason already says the cuts are undocumented.
4. **The metric's justification (claims 29, 30; P6, MET-1 Must, MET-10 Weigh).**
   - What is wrong: the cited practice supports the unweighted Gini only for rows of equal exposure (Allstate's
     vehicle-years). For unequal exposure, Liberty Mutual weighted, and Frees et al. order by the relativity to a
     premium.
   - On this task the declared Gini gives raw `Exposure` 75% of the model's score, and an exposure-weighted Gini
     gives it -0.05.
   - One claim moves a fold by 0.09.
   - What it changes: what the benchmark rewards (ranking period lengths against ranking risk). The australian and
     Spanish siblings declare the same unweighted Gini, so it is a family-level weighing call for the curator.
   - Mildest remedy: keep `normalized_gini`, and add to the reason that it scores the period's total cost, length
     included.
   - Alternative: an exposure-weighted ordered-Lorenz Gini, with the realised `Exposure` as a scoring column (MET-2:
     a weight is never a feature). That fits the remedy of item 2, where the feature becomes the start-known length.
5. **Record corrections (claims 32-34, 19; EV-2, record only).** Year 2014 from the 1.0-7 NEWS; 3,805 records span
   all of 2004; 34,324 chain links (not "431 against 309"); file sizes 16,000-32,400 in 1.2-1; the files are not
   random slices. The builder's draft issue 5 covers part of this.
6. **Wording (claims 5, 25; quality).** AIcrowd's game was 2020-21 on the 2017 game's portfolio. `OutUseNb` counts
   out-of-use periods, not claims.
7. **Cannot verify (claim 38).** Which guarantee the amount covers, paid or incurred, and the development date
   (USE-5, LEAK-24). The source does not say; it stays in the fit reason.

**Files**
- Scripts and outputs: in the run folder (not committed): the row alignment, the counts, the models, the true
  links, the feature-only lookup (random and chain-grouped folds), the severity, the files, the pre-1.2-1 sizes
  and the freMPL1 overlap.
- Sources: CASdatasets freMPL page (https://dutangc.github.io/CASdatasets/reference/freMPL.html); NEWS
  (https://dutangc.perso.math.cnrs.fr/RRepository/pub/web/NEWS.html); `inst/NEWS` and `DESCRIPTION` at GitHub
  commit c49cbbb; commit 3f5c00c; Frees et al. 2011 abstract
  (https://academicnewsletter.sufe.edu.cn/info/445125).

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): frempl_french_motor_personal_line**

**Verdict: ship after changes.** 15 of the 16 features are fine. One is not: `Exposure` is partly post-outcome, and its late
part can be located row by row. The negative-amount step can stay, but its stated reason is refuted by the data.

Prediction point (first `curation_comments` bullet): the start of a record, a period of cover with fixed rating factors.
Codebook: CASdatasets `man/freMPL.Rd` (master). Frame: `dataset_io.load(..., built=True)`, which gave a rebuild because
there is no build record: 115,155 x 17, shuffled (0.01% of consecutive rows look like a continuation). All numbers below
are mine, from untuned LightGBM (the builder's settings) on random 3-fold CV (6-9 folds), unless they are cited as the
builder's. Scripts: in the run folder (not committed).

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `Exposure` | "The exposure, in years"; (end - start)/365 within 0.006, 3 decimals | partly. Yes for open records (48%, which run to 31 Dec) and probably for continued ones (30%, which end at a renewal: the BM steps -3/-4/-5 at the change). No for the 25,131 records (21.8%) that end before 31 Dec with no continuation. Their end is unforeseen, and the claim drives it | float, (0.001, 1] | **leak (partial), fix** | LEAK-10, LEAK-7 |
| `LicAge` | "driving licence age, in months" | yes: grows by the months elapsed between consecutive records (99.9%) | int, 2-940. 47 records imply a licence before 17 (DrivAge is in whole years), 18 before 16, none before 15 | fine (unusual, kept with the note) | CLEAN-11 |
| `Gender` | Male / Female | yes (profile, fixed per record) | category, 2 levels | fine (ethics note present) | SEL-1, CLEAN-14 |
| `MariStat` | "Alone" / "Other" | yes | category, 2 | fine | CLEAN-14 |
| `SocioCateg` | CSP code, "CSP1" to "CSP99" | yes | category, 46 levels (union of the files), 23 with < 10 records | fine | CLEAN-14, CLEAN-8 |
| `VehUsage` | 4 usages | yes | category, 4 | fine | CLEAN-14 |
| `DrivAge` | driver age in years | yes: +1 at 37% of continuations, so it is the age at the record's start | int, 20-99 | fine | |
| `HasKmLimit` | "1 if there is a km limit for the policy" | yes (contract term) | category {0, 1} | fine (a yes/no flag) | CLEAN-14 |
| `ClaimNbResp`, `ClaimNbNonResp`, `ClaimNbParking`, `ClaimNbFireTheft`, `ClaimNbWindscreen` | claims of each type "in the 4 preceding years" | yes: at least one counter rises at the next record after 95.3% of the claims and after 2.3% of the zero-amount records, so a record's counters never hold its own claim | int counts | fine | LEAK-10 holds, CLEAN-14 |
| `OutUseNb` | "Number of out-of-use in the 4 preceding years"; what an "out-of-use" event is: unknown | yes: rises at the next record after 2.0% of the zero records and 3.2% of the claims, so it is not a claim type of the target | int count | fine | |
| `RiskArea` | "Unknown risk area between 1 and 13, possibly ordered" | yes (profile) | int, kept numeric. Claims per exposure-year are not monotone in the code (0.117 in area 1, 0.251 in area 4, 0.149 in area 12; Spearman 0.25) | fine; minor question | CLEAN-14 |
| `BonusMalus` | 50-350, < 100 bonus | yes: rises at the next record after 11.6% of the claims (2.4% otherwise), so it is the value at the start, updated at renewal | int, 50-195 | fine | |
| `log1p_claim_amount` (target) | `ClaimAmount`, "Total claim amount of the guarantee", negatives clipped to 0, log1p | target | float. 967 negatives set to 0; the stated reason is refuted (problem 2) | cleaning problem (reason only) | EV-2, CLEAN-1 |
| `ClaimInd` (dropped) | claim indicator of the same period | no: same period, 1 exactly where amount > 0 | dropped | fine (correct drop) | LEAK-10 |
| `RecordEnd` (dropped) | end date of the record | no: post-outcome (it carries the termination) | dropped | fine (correct drop) | LEAK-10 |
| `RecordBeg` (dropped) | start date of the record | yes, but with `Exposure` it gives a record's end | dropped. Even after the problem-1 fix it adds nothing (Gini 0.335 with it against 0.340 without, AUC 0.675 both) | fine | CLEAN-22 |
| `file` (dropped) | which sample file | n/a (a storage artefact of near-random slices) | dropped | fine | CLEAN-3 |

**Problems, ranked**

**1. P4, LEAK-10 (Must), fixed by LEAK-7: `Exposure` of records that end early with no continuation is post-outcome,
and those ends can be located.** Severity: strong on the declared metric.
- What the definition says. The `Exposure` note gives the curator's fremtpl2 call ("known when a policy is priced, apart
  from a contract that ends early"). The dates bullet says that only "the start date together with `Exposure`" gives
  the end away.
- What the data shows. The exact 3-decimal value of `Exposure` alone tells a record that ended early from an open one at
  ROC AUC 0.91 (3 folds; rounded to whole months, 0.61). It picks out the unforeseen ends at 0.81 (rounded, 0.56).
  Dropping the dates hides much less than the note says.
- The claim drives the end. Among short records, those with an unforeseen end have far more claims than open or
  continued ones of the same length:

  | length | unforeseen end | open | continued |
  |---|---|---|---|
  | 1-3 days | 2.7% | 0.4% | 0.24% |
  | 4-11 days | 2.65% | 0.34% | 1.0% |
  | 0.03-0.1 years | 4.3% | 1.7% | 2.0% |

  These records hold 20.7% of the exposure but 38.9% of the claim cost (837 per exposure-year, against 311 for open
  records and 407 for continued ones). They also hold 66 of the 109 claims in the top 1%. Large claims (write-offs,
  thefts) end contracts, as the australian sibling found (claims of at least 80% of the vehicle's value: median
  exposure 0.37 against 0.65).
- The decisive test (EV-1). Give these 25,131 records the source's own `Exposure` for a record starting the same day
  and running to 31 Dec, the value known at the start. Every start date has open records and one shared value, so this
  is a lookup that does not read the label.
  - Normalized Gini goes from 0.288 to 0.339: +0.027 to +0.065, higher on 9 of 9 folds. Without the 802,620 claim it goes
    from 0.316 to 0.371.
  - Claim AUC goes from 0.689 to 0.675: -0.013 to -0.016, lower on 9 of 9 folds.
  - So the shipped value inflates the claim ranking and hides the large claims that ended contracts. Either way the
    benchmark measures another task than "price at the start".
  - Giving every record its start-known value instead loses the scheduled renewal ends: Gini 0.293, AUC 0.633.
- Precedents.
  - spanish_motor_insurance_coverage_level_2022_2024 (same run): cancellations it could locate got the exposure known at
    the start (LEAK-10, LEAK-7); the ones it could not locate were kept with a note.
  - australian (same run): kept with a note, because it could not locate them and the late part showed no gain.
  - fremtpl2 (CC, 2026-10-20): kept, also unable to locate them.
  - LEAK-10's second clause: late cells that can be located are fixed.
  - The fact that sets freMPL apart from fremtpl2: its dates locate the early ends row by row. Treating it like spanish is
    the consistent call; keeping it as it is would be a departure from the rule that needs its own reason.
- Mildest remedy. In `_clean`, before the dates are dropped, set `Exposure` for the records with `RecordEnd` and no
  continuation (`_continues_next` already in the file) to the open records' `Exposure` for the same `RecordBeg`. Keep the
  continued records as they are, with a note on the residue: some continuations are claim-driven too (vehicle
  replaced), at a claim cost of 407 against 311 per exposure-year. Rewrite the `Exposure` note and the `fit_reason`
  clause.
- Fallback if the curator keeps the fremtpl2 reading. Use a `Potential leak, kept on purpose:` note with the numbers
  above. Also round `Exposure` to whole months. That removes the end-status code (0.91 to 0.61) at no cost: Gini 0.282
  against 0.283, claim AUC -0.001, and +0.002 for exact values with fine-binned trees on 5 of 6 folds.

**2. P7 with EV-2 (Should): the negative amounts are claims of the period, not "recoveries on earlier claims".**
- Of the 246 negative-amount records that have a continuation, 95.1% are followed by `ClaimNbNonResp` +1 at the next
  record. That happens for 0.19% of zero-amount records and 18.6% of positive claims.
- Their rate grows with the length, like a claim of the period: 0.18% at 0.1 years or less, 1.5% at 0.75-1.
- Their predecessor had a claim no more often than for other records (6.6% against 8.0%).
- So they are not-at-fault claims in the record's own period whose recourse exceeded the payment, presumably the
  IRSA flat rate. `ClaimInd` = 0 there marks "no positive net cost", not "no claim".
- The clip itself can stay. pricing_game_2017 clips the same kind of recourse totals with "a net recovery is no claim
  cost of the year". The effect is small: the negatives are -2.4% of the net claim cost.
- Remedy (text only):
  - Correct the negatives bullet, `predicted` ("0 ... those without a claim"), the target bullet ("90.6% ... no claim"),
    the `Decision` text, and the reason proposed for accepting `task_target_value_dominant`.
  - Suggested wording: 0 = no claim, or a not-at-fault claim recovered in full (0.84%).

**3. P3, USE-5 (positive finding for a note): the amount covers the policy's claims of every counted type.** The source
names no guarantee, but the counter that rises after a positive claim shows which kinds the amount holds. Over the
2,361 claim pairs with exactly one rise:

| counter | share |
|---|---|
| windscreen | 39.6% |
| responsible (at fault) | 28.2% |
| non-responsible (not at fault) | 17.3% |
| parking | 8.9% |
| fire-theft | 5.9% |

So the amount spans liability, own damage, glass and theft/fire claims. This narrows the `fit_reason` gap "the guarantee
behind the amount is not named" and the builder's draft issue 3. The fit stays approximate for its other reasons.

**4. P7, CLEAN-14 (weigh; question for the curator): `RiskArea` numeric or categorical.** It is a fixed set of 13 codes
that the source calls only "possibly ordered", and the claim rate is not monotone in the code (Spearman 0.25).
- Numeric keeps the source's suggested order and matches the definition ("as shipped").
- Categorical follows CLEAN-14's "fixed, finite set". The australian sibling types its `area` categorical, but that one
  is a letter code.
- Either choice is defensible. Low stakes for tree models.

**5. Minor note wording (claim-auditor's territory).**
- The counts bullet's "12% otherwise" counts any change, falls from the 4-year window included. Only 2.3% of zero
  records see a rise, mostly in `OutUseNb`. Say "a rise after 95% of claims, 2.3% otherwise", or name the falls.
- The 47 early licences: 18 imply a licence before 16 even allowing for the whole-year `DrivAge`. They are still not
  provably impossible without the reference dates, so keeping them is right.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-3 holds; LEAK-10 triggered on Exposure (21.8% of records, unforeseen ends located by RecordEnd + no
continuation), fix by LEAK-7 (start-known Exposure, as spanish); ClaimInd/RecordEnd drops hold; counters and
BonusMalus are as of the record's start (LEAK-10 holds).
Value: unchanged by this audit (the fix raises the Gini 0.288 -> 0.339, lowers claim AUC 0.689 -> 0.675).
Quality: negative-amount reason refuted (EV-2), clip kept with corrected text; RiskArea dtype a CLEAN-14 weighing.
For the curator: problem 1 (fix Exposure as spanish, or keep as fremtpl2 with a kept-leak note and month rounding).
```

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): right with notes.** Random 3x3 folds over the 115,155 records, tagged
`ForcedIIDFromTemporal`, are the right split for this release. All numbers come from untuned LightGBM (300 trees, the
builder's settings) on the definition's frame and shipped splits, loaded through `dataset_io` (EV-8). The split stays.
Three statements about it need correcting, and one consistency question goes to the curator.

```text
Verdict: right with notes.
Validity: SPLIT-1, SPLIT-3 hold (temporal by use case, one year released); SPLIT-8 holds for the regime and the tag, but
  the cost against the valid windows was not measured (now measured, issue 1); SPLIT-29, SPLIT-30 hold: a test record's
  policy mates on the training side add nothing (paired, 9 shipped folds); USE-10 (known policies are priced) supports
  keeping them across the split.
Value: not affected by the split. The 802,620 claim decides which fold scores low (note A).
For the curator: consistency with pricing_game_2017_french_mtpl (grouped by client) and
  spanish_motor_insurance_coverage_level_2022_2024 (grouped by policy), issue 2.
```

**What the use case implies.** An insurer prices a period of cover when it starts and fits its tariff on past years
for the next year. The task is therefore temporal (SPLIT-6), and most priced policies are renewals, i.e. known entities
(USE-10). The release holds one year: `RecordBeg` runs from 2004-01-01 to 2004-12-31, 38% of the records start on 1
January, and 48% are open at year end. No next-year window exists, so SPLIT-8 applies. IID is its closest regime,
because the records are segments of one year, not periods stacked across years. One prediction is one record, with no
aggregation. Claims per exposure-year are flat by start quarter (0.216, 0.209, 0.216, 0.204), so there is no seasonal
pattern a window would have to respect.

**Issue 1 (P4, SPLIT-8, Must: "with the cost measured against the valid windows where the data has any").** The
`splits_comment` says windows inside 2004 "would train on records whose period is still running". That is only true of
naive windows. Windows whose training labels are complete do exist: train on the records whose period ended by the
cutoff (SPLIT-9 met), and test on the records that start in the next three months. They fail SPLIT-14's 50% floor, and
their training side holds only contracts that ended early. Their cost was not measured. Measured on the same test rows:

| cutoff | test rows | valid train (ended by cutoff) | claim AUC: valid / random same n / 3-fold OOF | Gini: valid / random same n / 3-fold OOF |
|---|---|---|---|---|
| 1 Apr | 20,237 | 14,752 (12.8%) | 0.549 / 0.601 / 0.621 | 0.136 / 0.170 / 0.162 |
| 1 Jul | 16,822 | 30,933 (26.9%) | 0.592 / 0.595 / 0.604 | 0.106 / 0.155 / 0.162 |
| 1 Oct | 19,417 | 45,077 (39.1%) | 0.624 / 0.622 / 0.638 | 0.172 / 0.153 / 0.191 |

The April window loses the most, because it trains on Q1-ended records (mean `Exposure` 0.15, claim rate 4.4%) and tests
on Q2 starters (mean 0.53, 11.0%). Its predicted claim rate is 0.41 of the observed rate. That loss comes from which
records the window can train on (only contracts that ended early), not from change over time. The two later windows
match random records of the same size on AUC. Training on every record that started before the cutoff, labels still
running, gives AUC 0.624, 0.609 and 0.630. So the windows this release allows test a training side that is selected by
how contracts ended. They cannot replace the forced IID split, but SPLIT-8 asks for the number to be stated.
*Remedy (mildest: text only):* replace the reason in `splits_comment` with the measured windows, e.g. "Windows inside
it can train only on records whose period had ended by the cutoff: 13% to 39% of the rows for 1 April, 1 July and 1
October, below the 50% floor, and only contracts that ended early; on the records starting in the next three months
they reach a claim AUC of 0.55, 0.59 and 0.62 against 0.60, 0.59 and 0.62 for as many random records".

**Issue 2 (P4, SPLIT-29 and SPLIT-30, Must, which hold; a consistency question under principles.md).** The notes
undercount how often one policy has several records. `splits_comment` ("80,831 chains") and the curation note ("34,324
records (30%)") count only continuations in the next row of the same file. Matching every closed record to a record
that starts on its end day, with the same six profile columns and consistent `DrivAge` and `LicAge`, gives:

- 34,683 closed records continue within their file. Another 10,292 continue only in another file, and 1,201 in both.
  Shifting every start date by 7 days, as a chance control, matches 465 closed records.
- The cross-file pairs behave like one policy. The claim-history counts change after 95% of claims (96% within a
  file), and `BonusMalus` moves by 0 to -5 in 89% of the pairs.
- Joining all the links gives about 68,900 policy components. 74% of the records share a component with another record,
  and 10,485 components span two or more files. So the five files are not disjoint policy samples.
- Under the shipped folds, 53% of the test records have a record of their policy on the training side (40% counting
  only the within-file chains).

Does the random split reward recognising the policy? A paired test on the 9 shipped folds answers it. For each fold,
one model trains without the test records' policy mates, and the other drops the same number of random non-mate rows.
Both score the same test rows:

| policy key | Gini, mates kept / removed (diff ± se) | claim AUC, kept / removed | test rows with a mate: Gini, AUC diff |
|---|---|---|---|
| within-file chains | 0.2804 / 0.2821 (-0.0017 ± 0.0018) | 0.6880 / 0.6890 (-0.0009 ± 0.0005) | -0.0005, -0.0007 |
| cross-file components | 0.2790 / 0.2790 (0.0000 ± 0.0029) | 0.6871 / 0.6875 (-0.0004 ± 0.0007) | +0.0028, -0.0002 |

A direct split, 3x3 folds grouped by component, scores Gini 0.2785 and AUC 0.6899, against 0.2827 and 0.6901 on the
shipped folds. The mates do not help. This fits the builder's finding that a claim does not make the next record's claim
likelier (8.3% after a claim, 9.2% otherwise), and it refutes the screening note "policyholders cannot be traced" (431
pairs against 309 by chance). The builder's unpaired numbers (0.266 against 0.251) sit inside the fold noise of note A.
The paired numbers are the ones to cite.

The consistency question: two siblings in this run keep a policyholder's rows together.
`pricing_game_2017_french_mtpl` (one year, the same family) is grouped by `id_client` because "the claims of the
client's other vehicles in that year are not known". `spanish_motor_insurance_coverage_level_2022_2024` is grouped by
`insured_id`. The same reasoning applies here to a policy's later records. What sets this case apart:

- The release has no policy or client id. The components are built from date continuity, with tolerances on the ages,
  so they would be a constructed key that is not exact (SPLIT-24). About 1% of the links match by chance, and 1,767
  closed records have two or more candidate continuations.
- New data keeps the entity: the insurer reprices its known policies. SPLIT-30 re-splits only for an entity that new
  data would not have.
- The measured effect is nil. Under SPLIT-4 the gap never decides alone, but no reward is measurable either.

*Remedy (mildest: text only):* correct the counts in `splits_comment` and in the curation note. Cite the paired test.
Record the distinguishing facts above. Ask the curator to confirm IID over grouping by component. If the curator wants
consistency instead, grouping on the components is possible and costs nothing measurable, but it groups on an inexact
key.

**Issue 3 (P4 support; EV-5, EV-9).** The claim that the files are "near-random slices of one portfolio" underpins
stacking them with no file column. It rests on file accuracy of 31.0% against a 28.1% majority share, and EV-5 bars
accuracy against the majority class as evidence. Measured instead:

- The file log loss is 1.528 against 1.572 for the prior, and the one-vs-rest AUC per file is 0.57 to 0.64 (files 9 and
  5 are the most distinct). So the files are weakly distinct.
- What separates them is the profile mix (`HasKmLimit`, `VehUsage`, `DrivAge`, `BonusMalus`, `SocioCateg`), not time:
  the start-quarter shares are close, and 47% to 49% of each file's records are open at year end.
- File 9's claim rate is 7.7%, against 9.3% to 10.0% for the others.
- Leave-one-file-out scores like the random folds on each file's rows: AUC 0.690 against 0.687, Gini 0.284 against
  0.285.

The conclusion holds: stacking with no file column is fine, and a file split would test nothing new. Policies also
cross files (issue 2). *Remedy:* replace the accuracy figure in the note with these numbers.

**Issue 4 (P3 wording, USE-8).** `task_summary.split` says the test data "stands for other policies' periods in the same
year". Half the test records have their policy on the training side, so it should read "other periods of cover in the
same year, half of them of a policy with another period in training, which a pricing model knows too". *Remedy:*
wording.

**Note A (P6; for the metric and value reviewers, not a split problem).** The largest claim, 802,620, decides the fold
Gini. The fold that holds it scores 0.211 to 0.234, the other folds 0.279 to 0.331 (shipped folds, both mate tests).
Each repeat has exactly one such fold, so repeat means stay comparable, but any single-fold or unpaired comparison of
splits is noisy.

**Note B (LEAK-24, cannot verify).** The claim amounts' evaluation date is not stated. Among claimants, records open at
year end have lower severity (median 749, mean capped at the 99th percentile 1,608) than records that ended earlier
(median 799 to 1,086, capped mean 2,046 to 2,781 by end quarter). This fits immature year-end claims, but also claims
that end a contract (a total loss or a theft), so it is circumstantial. It does not change the IID split.

**Checked with no finding.**

- No exact feature copy in the test folds has a twin on the training side (leak probe: 0.0%).
- Near copies: 0.2% of the rows, the largest cluster 4.
- Hidden-group probe: no hit. Its best composite key, `(all but Exposure, LicAge)` at 49.4%, is the policy chain of
  issue 2, now tested directly.
- No time column survives in the features, and none is needed for an IID task.

**Scripts and outputs** (run folder, not committed): the alignment of the shuffled frame with the raw dates, files
and chains; the paired mate test; the cross-file components; the valid windows; the files; the grouped folds.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (pricing actuary of a French motor insurer), 2026-11-01**

**Verdict.** Fit **approximate**, as declared (USE-8). The rows are the exposure lines of a tariff study and the features are its rating factors. But the amount's guarantee and loss basis are undocumented (USE-5), the vehicle and cover factors every French motor tariff rates on are missing, and random records of 2004 stand in for next year's book. Metric: **partly**. The Gini family is the right one, but the declared form ranks rows, not exposure. It scores the record's length nearly as much as the risk, and one claim moves it by ±0.05 between folds. I would use the exposure-weighted Gini on the predicted annual loss cost (below).

**How the decision is made.** I fit a pure-premium model each year: expected loss per car-year, either frequency × severity or one Tweedie GLM. I fit it on calendar-year experience, one line per period with fixed rating factors, with the earned exposure and the incurred losses of that line. The exposure is an offset or a weight, never a rating factor. CAS Monograph 5 (sec. 2.6) says exposure is "included as a weight, but not as an offset" for frequency, and its offset form for counts is the same thing. Sec. 5.1.1 defines pure premium as "dollars of loss per exposure". The premium of a period is the annual rate times its length, pro rata. I pick between candidate models on a holdout. The tools are quantile plots, double-lift charts against the current tariff, and the Gini index. That Gini sorts by "the model predicted loss cost" and plots "the cumulative percentage of exposures" against "the cumulative percentage of losses" (sec. 7.2.4). I cap large losses before fitting (sec. 5.1.3).

**1. Inputs at the prediction point (USE-3, USE-6).**
- I have these at the start of the period: age, licence age, marital status, CSP, usage, km limit, risk area, the bonus-malus (the French CRM, known at the anniversary), and the claim counts of the four preceding years, taken at the record's start (the builder's check, 96% / 12%). Gender was a lawful factor in 2004. I could not use it today (Test-Achats, noted).
- `Exposure` is not a risk input in my world. It is the volume of experience inside the 2004 window: 38.2% of records start on 1 January, 48.4% run to 31 December, and only 3.3% cover the whole year. When I price a real policy, its planned period is known. The realised length of a record that ends early is not known.
- The early end carries risk. Records that end with no next record cost 837 a year (frequency 0.280, severity 2,985). Records that end and continue in a next record cost 407 (0.211). Open records cost 311 (0.189, severity 1,640). That is 2.7 times the annual cost of open records, presumably cancellations after claims, total losses and thefts.
- `fit_reason` names this gap ("known only at its end when the contract ends early"). The curator's fremtpl2 call and the family call of 2026-10-30 keep `Exposure` as a feature. I do not reopen that call, but it is the reason the metric needs fixing.
- Inputs I would always have and do not: the vehicle (SRA group and class, age, value, power), the cover level (third party or comprehensive), the deductible, tenure with the insurer and a finer zoning. freMPL1-4 hold the vehicle block, but for other samples, and the record measured the union and rejected it. So this is a thin tariff: it ranks driver and claims-history risk only.

**2. Target (USE-5).** I act on a number: the expected cost per car-year. I would never want a class. The shipped total amount of the record is the standard label of a pure-premium model once the length is handled. It is the right quantity, with three caveats. "Total claim amount of the guarantee" names no guarantee; the median claim of 781 and the claim counts by type suggest all covers combined. Paid or incurred is not stated, and neither is the evaluation date. The losses are uncapped: the 802,620 claim is 3.6% of all cost, and the 13 claims above 50,000 hold 8.3%. The log1p shipping with the score taken on the amount is correct (MET-3).

**3. Row and test data (USE-8, USE-10).** One row is one exposure line, the unit I model on, not the unit I decide on. I decide an annual rate per risk. 38% of the record starts are the calendar cut, not a pricing event, so "the start of a record, when the insurer prices it" (the first `curation_comments` bullet) is true only loosely: the factors are the ones in force. Random records of one year are an accepted holdout in practice. The CAS monograph (sec. 4.3.1) allows a random or an out-of-time split and prefers out-of-time. The chain-grouped folds scored like random ones, so the split is a small gap, honestly named (`ForcedIIDFromTemporal`).

**4. Would I use it?** Yes, as a challenger to a GLM on a realistic, if thin, French tariff table. I would trust a model that beats the current tariff on a double-lift chart and on an exposure-weighted Gini out of time, with actual/expected stable by decile and by factor. I would distrust one whose lift comes from the period length, or whose ranking depends on where one 802,620 claim lands.

**5. The metric (MET-1, MET-2, MET-10, MET-11).** `normalized_gini` here is Kaggle's row form: losses cumulated over rows sorted by the predicted total. In Frees, Meyers and Cummings (2011), which the reason cites, rows are sorted by relativity, score / premium, against the cumulative premium. The row form is that curve with every record charged the same premium, whatever its length, and no insurer charges that. With a pro-rata base premium it becomes the CAS construction: sort by predicted loss cost per year, cumulative exposure on the x-axis. Allstate's rows were vehicle-years, so its row Gini was close to an exposure Gini. Here exposure runs from 0.001 to 1 year. Measured with untuned LightGBM on 3×3 random folds (script and output below):

| model | declared row Gini (sd) | exposure Gini on the annual rate | row Gini, losses capped at 50,000 (sd) |
|---|---|---|---|
| LightGBM, all features (log1p) | 0.283 (0.044) | 0.182 | 0.316 (0.012) |
| LightGBM without `Exposure` | 0.191 | 0.203 | 0.187 |
| `Exposure` alone (raw score) | 0.213 | about 0 (constant rate) | - |
| Tweedie GBM, log-exposure offset, no `Exposure` feature | 0.281 | 0.199 | 0.304 |

- Under the declared metric, the record's length alone (0.213) beats a risk model without it (0.191) and makes up 75% of the full model's score.
- Under the actuary's Gini, the length scores nothing and the order of the two LightGBMs reverses.
- The three folds that hold the 802,620 claim score 0.216-0.237, the other six 0.281-0.328. Capping cuts the fold sd from 0.044 to 0.012 and keeps the model order (MET-10, resolution).
- The price-level blind spot the reason names is real and acceptable for ranking (pricing sets the level separately).

The metric I would choose: the normalized Gini of the ordered Lorenz curve on the annual loss cost. Rows are sorted by predicted amount / `Exposure`, with cumulative `Exposure` on the x-axis and cumulative amount on the y-axis. This is `normalized_weighted_gini` with y = amount / `Exposure`, prediction = predicted amount / `Exposure`, weight = `Exposure`. It needs `Exposure` as a metric input, and MET-2 says a metric input is never a feature, so it is the curator's call. The ways to get there are listed below.

**Gaps, ranked by how much they change the task.**
1. What the score measures. With `Exposure` a free feature and a row Gini on the total, about three quarters of the score is the record's length, part of it known only at the record's end (gap above; LEAK-10 kept by the curator's call). The fix is in the metric, not the features.
2. Missing vehicle and cover factors. This is a driver-and-history tariff and cannot be repaired from these files.
3. The undocumented amount: which guarantee, paid or incurred, evaluated when (USE-5, already behind `approximate`).
4. Uncapped large losses. One claim decides a third of the folds (MET-10).
5. One year, random records, one policy's records on both sides. Standard practice, small, named.
6. Gender: lawful then, barred now. Noted, fine for a 2004 task.

**What an expert would change (recommendations; the curator decides).**
- Metric, in order of preference:
  - (a) Keep target and features, and score the exposure-weighted Gini on the annual rate, with `Exposure` also a metric input. This needs the curator to allow a feature as a metric input (MET-2) and a general metric such as `normalized_exposure_gini` (MET-12, MET-13).
  - (b) Ship the annual loss cost with `Exposure` as weight only. This follows the actuarial standard and the AUTOSEG precedent, but goes against the fremtpl2 call ("dividing would inflate short policies' targets"), and models without weights suffer on records of a few days.
  - (c) At the least, keep the row Gini and write in the metric reason that `Exposure` alone scores 0.213 of the model's 0.283, and that one claim moves a fold by about 0.08.
- The same question applies to every table with exposure below a year scored by the row Gini: `australian_vehicle_insurance_2004_2005`, `spanish_motor_insurance_coverage_level_2022_2024`, and the 2015 and 2016 pricing games. It should be one family decision, not this dataset's alone.
- Capping: consider scoring losses capped at a large-loss threshold (50,000: 13 claims), or name the instability. This is a change to the target as recorded, so it is the curator's call.
- Wording:
  - `use_case`: "estimates the expected claim cost per year of cover (the pure premium) from the rating factors; a period's premium is that rate times its length".
  - `fit_reason`: add that the length is mostly the 2004 window, that contracts ending within the year cost 2.7 times as much per year, and that vehicle and cover factors are missing.
  - The first `curation_comments` bullet: name the calendar cut (38% of starts).
- Keep: freMPL5-9 stacked, negatives set to 0, `ClaimInd` and the dates dropped, the log1p shipping, the random split with its tag.

**Probe.** A script in the run folder, not committed (clean-room frame, RepeatedKFold 3×3, seed 4267, the builder's LightGBM settings; the constant-rate Gini over five random tie orders lies between -0.01 and 0.035). The annual costs by record type, the calendar shares and the claim tail were computed inline on the raw freMPL5-9 CSVs with the 45 copies dropped.

**Sources.**
- CASdatasets freMPL page (column definitions, "Total claim amount of the guarantee", "The exposure, in years"): https://dutangc.github.io/CASdatasets/reference/freMPL.html
- Goldburd, Khare and Tevet, CAS Monograph No. 5, Generalized Linear Models for Insurance Rating, read in full: sec. 2.6 exposure offset and weight, 4.3.1 random against out-of-time holdout, 5.1.1 pure premium, 5.1.3 capping large losses, 7.2.4 Gini on cumulative exposures. https://www.casact.org/sites/default/files/2021-01/05-Goldburd-Khare-Tevet.pdf (page: https://www.casact.org/monograph/cas-monograph-no-5)
- Frees, Meyers and Cummings (2011), "Summarizing Insurance Scores Using a Gini Index", JASA 106(495):1085-1098, read from the abstract and the CAS slides (the ordered Lorenz curve by relativity score / premium): https://casact.org/sites/default/files/presentation/spring_2010_handouts_c17-frees.pdf; the 2014 follow-up, https://casact.org/abstract/insurance-ratemaking-and-gini-index
- CAS RPM slides on the Lorenz curve with earned car-years on the x-axis, from search results, not read in full: https://www.casact.org/sites/default/files/presentation/rpm_2014_handouts_paper_3048_handout_1892_0.pdf
- Family call of 2026-10-30: the zero-inflated triage summary (no longer in the repository; each call is in its record's Assessment of 2026-10-30), "Policy calls of 2026-10-30", item 3. The fremtpl2 call on `Exposure`: the fremtpl2 curation record.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The table is a faithful, leak-free preparation of real French motor insurance records (CASdatasets freMPL5 to freMPL9). But very little in it is predictable: most of the explainable variance comes from the mechanical effect of `Exposure`, and well-tuned models tie within noise. The changes are to document how the target was built and to flag the task as low-signal (it tests robustness to noise and does not separate good methods well).

**What the task is**

A French motor insurer in 2004 predicts, for one policy record (a time segment of a policy within the year), the claim cost on "the guarantee", using driver profile, bonus-malus, risk area, usage and claim counts over the previous 4 years. The decision is pricing: an expected cost per policy period, in effect a pure premium. This is a real and central actuarial use. An actuary would normally model frequency and severity separately, or use a Tweedie model on the raw amount, rather than squared error on log1p. Still, log1p regression is a reasonable proxy for a generic benchmark, and it avoids the extreme tail (maximum claim 802,620).

**Provenance check (reproduced from the public source)**

I downloaded the current freMPL5 to freMPL10 `.rda` files from github.com/dutangc/CASdatasets and read them with pyreadr, installed into a scratch folder.
- freMPL5 to 9 have 16,000 + 32,400 + 26,600 + 24,000 + 16,200 = 115,200 rows. The prepared table has 115,155 rows, which is exactly those files minus 45 rows that are duplicates on all 20 source columns (including RecordBeg, RecordEnd and ClaimAmount).
- The target equals `log1p(clip(ClaimAmount, lower=0))` exactly: the sums match to 1e-10, and there are 10,869 positive rows in both the source and the table.
- RecordBeg, RecordEnd and ClaimInd were dropped. ClaimInd is the target indicator, so dropping it was correct.
- freMPL10 was excluded. That is right: it has a different schema (VehAge) and a claim rate of 0.08% against about 9.5% in files 5 to 9.
- The files are from CASdatasets 1.2-1, whose NEWS says: "Remove duplicated rows in `freMPL*.rda` files (around 9995 rows for each file)". So the prepared table already builds on the deduplicated release.

**Concerns, most to least serious**

1. **Weak signal, mostly from Exposure; competent methods cannot be told apart.** All figures below are from 3x3 repeated CV (the same protocol as the task description), scored as R² on the log1p target:
   - tuned LightGBM: 0.0357 ± 0.0018
   - spline + one-hot ridge: 0.0355 ± 0.0015
   - default LightGBM: 0.0319
   - LightGBM on `Exposure` alone: 0.0284

   So about 80% of the explainable variance is the mechanical effect of the record's length: the claim rate rises from 2.1% at Exposure ≤ 0.1 to 19.4% at Exposure = 1. The other 15 features add about 0.007 R².
   - The paired difference between tuned LightGBM and ridge is 0.0002 ± 0.0009, a tie. Tuned versus default LightGBM is 0.0038 ± 0.0006, so the task mainly rewards regularization.
   - Severity among the positive rows is essentially unpredictable (R² 0.012).
   - For the claim indicator, AUC is 0.692 with all features against 0.674 with Exposure alone.

   What I would change: keep it only as a deliberately low-signal or noise-robustness task, and give it low weight or flag it in any analysis that ranks methods. If the benchmark wants tasks where model choice matters, this one adds little.

2. **Exposure is partly known only after the fact.** A record's length is fixed when it ends, by a policy change, a cancellation, or the end of the 2004 observation window. Records that end with no following record (likely cancellations) have 0.282 claims per exposure-year. Records that run to the end of the year have 0.189, and records followed by another record of the same policy have 0.213. So a short exposure partly encodes "the policy lapsed, often after a claim".
   - Using exposure as an offset is standard actuarial practice, and the effect is moderate, so I would not drop `Exposure`. Without it the task loses most of its signal anyway.
   - What I would change: say in the task description that Exposure is the realised duration of the record, not a planned one.

3. **Negative claim amounts were set to zero, undocumented.** 967 source rows (0.84%) have negative ClaimAmount (minimum −1,947.62). All of them have ClaimInd = 0, so they are presumably recoveries rather than claims.
   - Setting them to 0 agrees with the source's own claim indicator and is sensible.
   - What I would change: state it in the task description, together with the 45-row deduplication and the choice of files (freMPL5 to 9 only).

4. **One policy can contribute several rows, and the IID split ignores this.** The source has no policy ID. Policies are split into several records within 2004, and in the source these records sit on consecutive rows.
   - I linked consecutive source rows when the next record starts on the day the previous one ends and gender, socio-category, age and licence age agree. This gave 37,045 links and 78,155 inferred policies; 70,177 rows (61%) belong to policies with two or more records.
   - The effect on scores is negligible: random 3-fold R² is 0.0294 against 0.0287 for GroupKFold on the inferred policies.
   - The claim-history counts do not leak the target. After a record with a claim, the next record's ClaimNbResp rises by 0.26 and ClaimNbWindscreen by 0.38 on average, against −0.02 and −0.03 after records without a claim. So the counts exclude the record's own claim and are known when the record starts.
   - What I would change: nothing is required. Mention it as a known limitation.

5. **Source files overlap, and some duplicates remain.** For 35 of the 45 duplicate rows that were removed, the original copy sits in a different file. Some are whole multi-record chains: source rows 10929 and 10930 in freMPL5 reappear as row 38840 in freMPL6 and row 67520 in freMPL7.
   - After RecordBeg and RecordEnd were dropped, the prepared table still has 29 rows duplicated on all columns and 38 duplicated on the features alone. That is negligible.
   - Overlaps that differ in segmentation cannot be detected. Because the files overlap, other freMPL tables in the benchmark (if any) could share policies with this one.

6. **Pooling five files without a file indicator.** Claim rates differ by file: 7.7% in freMPL9 against 9.3% to 10.0% in the others. Ages and gender mix also differ a little. The claim-amount distributions, including the conventional fixed amounts, look alike across the files, so pooling is defensible. Minor.

7. **Preparation details (fine).**
   - No missing values.
   - Gender, MariStat, SocioCateg and VehUsage are stored as categoricals. SocioCateg has 46 levels, 25 of them with fewer than 30 rows.
   - RiskArea (1 to 13, "possibly ordered") is stored as an integer, which is acceptable.
   - The values are plausible:
     - DrivAge runs from 20 to 99 and BonusMalus from 50 to 195.
     - Only 18 rows have a licence age in years above DrivAge − 16.
     - The positive amounts have mass points at 1,418.61 (427 rows), 102.59 (329) and 4,326.53 (192). These look like the fixed-cost conventions typical of French claims data and support that the data is real, not generated.

**What I could not check**
- True policy identity: there is no ID in the source, so the grouping is inferred.
- Which "guarantee" (coverage) ClaimAmount refers to, the insurer, and the currency or any scaling.
- Whether the 1.2-1 deduplication removed records that were legitimately repeated, such as multi-vehicle insureds with identical driver rows (a few within-file triplicates look like that).
- How the earlier, pre-deduplication release differs from this one.
- Whether other freMPL or CASdatasets tables elsewhere in the benchmark overlap with this one.

I used only the clean-room data and public sources (the CASdatasets docs and NEWS, and the raw `.rda` files on GitHub).

</details>

<details><summary>Precedent check</summary>

**Precedent check (AI, precedent-checker, 2026-11-01): frempl_french_motor_personal_line**

```text
Verdict: consistent with the precedents on 14 of 15 decisions. One departs without a stated reason: how the
`Exposure` keep is recorded (the label, no revisit condition, the late part it could locate left unmeasured, and an
AI suggestion cited as "the family's call"). One pair in this batch is decided two ways and the curator should
settle it once: the target scale (log1p here and in spanish, raw in australian).
Validity: LEAK-10 / LEAK-6 the `Exposure` keep follows fremtpl2 (CC, Andrej, 2026-10-20) and is reasonable (no
consistent Gini gain from the late part, measured below), but it is written as `Note:`, not `Potential leak, kept on
purpose:`, and gives no revisit condition (definitions.md; australian, spanish). SPLIT-8, SPLIT-29/30 consistent (IID,
ForcedIIDFromTemporal). PROV-6/7, PROV-9 consistent.
Value: MET-3 consistent (Lennart's calls of 2026-10-21). MET-11 context Gini: no curator precedent yet; the same reason
is now in three definitions.
Quality: CLEAN-11, CLEAN-14, LEAK-18/19 consistent.
Drift: none. Third exception: none recorded. Two Cases rows are due once the curator confirms: time exposure as a
feature (fremtpl2's call is cited by three definitions and is in no Cases table), and the context Gini for insurance
pricing (MET-11).
For the curator: consistency checks A (Exposure) and B (target scale) below.
```

**How I checked.** For each decision: the same rule ID in the decision register of this run (1,620
decisions, 14 flags, none touching this dataset's decisions), the same mechanism in the Cases tables of the knowledge files, the
records of the insurance family (a search of the curation records for fremtpl, MTPL, CASdatasets, insurance), and the
definitions of the insurance siblings built in this run. Who decided matters (principles.md, "Precedence"). Curator
decisions on this family: fremtpl2 (record) (CC 2026-10-20, Andrej: aggregate claim
amount, `Exposure` a feature capped at 1, `ClaimNb` dropped, temporal by `year_index`). The CCs of 2026-10-30 on
frempl, australian, spanish, pricing_game_2017 and allstate_claim_prediction_challenge set only the verdict and priority.
The insurance table of "Policy calls of 2026-10-30" in
the zero-inflated triage summary (no longer in the repository; each call is in its record's Assessment of 2026-10-30) holds *suggested*
calls (Andrej: "I want you to suggest judgement calls ..."; every record: "the curator has the call"). The sibling
definitions australian_vehicle_insurance_2004_2005 and
spanish_motor_insurance_coverage_level_2022_2024 are
AI drafts of 2026-11-01 waiting for review. They are not precedents with a curator's authority, but the curator will
decide them alongside this one.

**Per decision**

1. **Target: the record's total `ClaimAmount`, freMPL5-9 stacked without a file column, freMPL1-4 and 10 left out.**
   Consistent. It follows fremtpl2 (CC 2026-10-20, aggregate amount per policy), the tension row "versions or cuts
   without a distinct task are duplicates" (PROV-6, PROV-7), the record's recommendation of 2026-10-20 and the Assessment
   of 2026-10-30. Andrej's answer to policy question 5 (no cap on French motor portfolios) leaves no uniqueness question
   against fremtpl2.
2. **Target shipped as log1p, scored on the amount (`target_transform="log1p"`).** Consistent with MET-3 and CLEAN-16,
   and with the curator's calls of 2026-10-21 (Lennart, "ship the target on the modelling scale, score on the original
   scale", given on 15 definitions). Among them are
   allstate_claims_severity (a log insurance loss) and the
   zero-inflated forest_fires (log1p area; MET-3 Cases in
   metrics.md). spanish ships log1p and says why.
   australian ships the raw cost and gives no reason. The builder calls log1p a "departure", but it is not one: MET-3
   leaves the scale to the definition. The split in the family is real, though: consistency check B.
3. **`Exposure` a feature; `RecordBeg` and `RecordEnd` dropped.** The decision follows fremtpl2 (CC 2026-10-20: "The
   contracted period is known at pricing (a mid-year cancellation also shortens it)"). Under the ranking it is a
   reasonable keep: LEAK-6 lets a slight optimism with a known cause stay with a note, and the part known only at the end
   shows no consistent gain in the metric (measured below). How it is recorded **departs without a stated reason** in
   three ways:
   * The bullet is labelled `Note:`. definitions.md ("Recording decisions") wants `Potential leak, kept on purpose:` for
     a suspect kept on purpose, with the mechanism, the numbers, why it stays and when to revisit. The definition itself
     names the suspect (`fit_reason`: "a period's length is known only at its end when the contract ends early").
     australian (`Potential leak, kept on purpose:`, LEAK-6/LEAK-10, revisit "if a release gives the contracted term")
     and spanish (the same label for the part it cannot locate) both use the label.
   * The part known only at the end can be located here (`RecordEnd` is set on 51.6% of the deduplicated records).
     spanish resets the cancellations it can locate to the value known at the start (LEAK-7: exposure 1 and annual
     premiums for portfolio policies, +0.004 to 0.010 Gini when kept). frempl neither resets nor measures this part. It
     measures the dates (Gini 0.251 without, 0.294 with an ended-early flag), not the late part of `Exposure` itself.
   * The note cites "the family's call of 2026-10-30". That call was an AI suggestion that the curator had not yet
     confirmed. australian words it correctly: "the suggested call of 2026-10-30, for the curator to confirm".

   Measured for this check (untuned LightGBM, the builder's settings, 3 random folds; script and output in
   the run folder, not committed): I replaced `Exposure` by the length known
   at a record's start (start to 31 December, capped at 1). The normalized Gini on the amount moves from 0.286 to 0.301
   on a log1p fit (per fold 0.273, 0.297, 0.289 against 0.336, 0.315, 0.253) and from 0.251 to 0.243 on squared error.
   The claim AUC falls from 0.690 to 0.632. The realized length helps rank claims, but it shows no consistent gain in the
   declared metric. That supports the keep under LEAK-6, provided the note says so. A weaker AI precedent points the
   other way: analcatdata_supreme (AI assessment, 2026-10-07) read an exposure shortened by the outcome as a leak. The
   curator retired that dataset on another ground (Lennart, 2026-10-14), so the reading was never decided.
   Consistency check A.
4. **967 negative amounts (all `ClaimInd` = 0) set to 0.** Consistent. It matches the suggested call of 2026-10-30 and
   AIcrowd's practice on the 2017 game's portfolio (an external precedent). The record's own indicator shows they are no
   claim of the period (USE-5). The register holds no curator decision on negative targets either way. The
   pricing_game_2016 and 2017 definitions will meet the same question, so the first confirmation sets the family's
   precedent.
5. **`ClaimInd` dropped.** Consistent with LEAK-10 (a part of the target) and the family: fremtpl2 `ClaimNb` (CC),
   australian `clm`/`numclaims`, spanish's claim counts.
6. **45 exact copies over all 20 columns dropped; 29 and 9 feature repeats kept.** Consistent with LEAK-18 and LEAK-19
   (wine_quality; many columns and an exact match make a collection artefact) and with the source's own repair in 1.2-1
   (PROV-13). australian keeps its 707 copies for a stated distinguishing fact (7 features, two of them rounded), so the
   two cases do not conflict.
7. **Random split, `ForcedIIDFromTemporal`, policy chains not grouped.** Consistent with a stated reason:
   * SPLIT-8: one year with no valid window, as distribution_transformers_at_cauca_department (one label year, IID,
     Lennart, 2026-10-21) and australian.
   * SPLIT-29/30: no id column, and the entity does not carry the label (8.3% claims after a claim against 9.2%).
     sarcoma (IID kept over a weak group, Lennart, 2026-10-26) is the closest curator case.
   * USE-10: the previous record's claim reaches the next record through the claim counts, a known entity's history.

   spanish groups by policy. That is a different set of facts, all evident: a true `insured_id`, policies that recur
   across three calendar years, 69% new business. frempl's chains are reconstructed, sit inside one year, and have no
   id. Two things to fix. The bullet's "so the split stays random" follows the fold comparison (Gini 0.266 against
   0.251), and SPLIT-4/SPLIT-30 say the gap never decides, so lead with the SPLIT-29 condition and cite it. The record's
   screening reason for IID ("policyholders cannot be traced", 431 pairs against 309) is superseded by the builder's
   34,324 chained records and should be corrected (EV-2; a later stage's measurement wins).
8. **Metric: normalized Gini, context (MET-11).** Consistent with the suggested call of 2026-10-30 and with australian
   and spanish (the same reason, nearly word for word). The insurers' own source metrics agree: Allstate 2011 (normalized
   Gini) and liberty_mutual_fire_peril_loss_cost (weighted Gini). porto_seguro (roc_auc for a binary Gini, 2026-10-21)
   is the related case. No curator has yet confirmed a *context* Gini on a regression target. MET-11's context origin
   ("only when the context is clear"; diamonds, Lennart, 2026-10-21) allows it. Once confirmed, it should become a MET-11
   Cases row, so the three definitions rest on one decision.
9. **`year = "2014"`.** Consistent with PROV-9 and melbourne_housing_market (a publication that grew over versions takes
   its first version's year, Lennart, 2026-10-22): freMPL entered CASdatasets on 9 September 2014. Pinning 1.2-1 is the
   copy, not the year. The screening's empty year is superseded (record correction, builder issue 5).
10. **Dtypes.** Consistent with CLEAN-14 as amended (Lennart, 2026-10-21): `HasKmLimit` is a yes/no flag, so
    categorical; `RiskArea` ("possibly ordered") stays a number as shipped, like australian's age bands. Keeping all 46
    CSP codes is allowed (CLEAN-8 permits merging rare codes, never requires it).
11. **The 802,620 claim kept.** Consistent with CLEAN-11 and qsar_tid_11 (Lennart, 2026-10-21: the training-period
    clause does not apply to a random split).
12. **47 licence ages below 17 kept.** Consistent with CLEAN-11 (unusual values stay) and with spanish's threshold,
    which makes missing only what no licence allows (below 15 in Spain). Measured here: 0 records below 15, 18 below 16,
    47 below 17, and 21,136 below 18. The measure (whole-year `DrivAge` minus `LicAge` in months) runs about a year low
    for many records, so nothing is shown impossible.
13. **`Gender` kept with a note (SEL-1).** Consistent: no rule or precedent drops a protected attribute. australian keeps
    `driver_gender`. 2_month_survival_rate_prediction's drop of edu and income (Lennart, 2026-10-26) rested on LEAK-10,
    and its fairness remark was an aside.
14. **Fit `approximate` (USE-5, USE-8: guarantee and development date undocumented).** Consistent with the USE-5 cases
    blood_tests_drink_prediction (the quantity known, its recording not) and mobile_churn, and with australian and
    spanish.
15. **`task_target_value_dominant` proposed for acceptance.** No precedent (no definition accepts this check yet). It
    is consistent within the batch.

**The builder's draft issues against the precedents.** Issue 1 (Exposure): the keep follows fremtpl2. The drop option
(claim AUC 0.690 to 0.565) would depart from the curator's only call on the question, so it needs a fact that sets frempl
apart. The recording needs check A. Issue 2 (chains): consistent (item 7); confirm the tag. Issue 3 (USE-5): consistent
(item 14). Issue 4 (scale): frempl is consistent; the pair goes to check B. Issue 5 (record corrections): add the chain
correction of item 7. Issue 6 (notes): consistent (items 11-13).

**Drift and repeated reasons.** Andrej's decisions on the family are fremtpl2 (2026-10-20) plus verdicts and priorities
(2026-10-30, 2026-11-01): no drift. Lennart's MET-3 calls of 2026-10-21 are uniform. No recorded exception shares a
reason with this dataset, so no third exception. One reason does recur, though: a realized time on risk kept as a feature
although an early end is known only after the prediction point. It appears in fremtpl2 (CC) and the three drafts of this
batch. LEAK-10 is a Must, so this cannot travel as exceptions. It needs one written reading (a LEAK-10 Cases row under
LEAK-6's slight-optimism clause, or an amendment) that the curator confirms once ("Keeping the rules current"). Today
three definitions cite a call that sits only in fremtpl2's record.

**Consistency check A (AI, 2026-11-01):** your call on frempl (`Exposure` kept as recorded, dates dropped, written as a
`Note:`) differs from spanish_motor_insurance_coverage_level_2022_2024 (draft, 2026-11-01: the locatable cancellations
reset to the exposure known at the start, LEAK-7; the rest `Potential leak, kept on purpose:` with a revisit condition)
and australian_vehicle_insurance_2004_2005 (draft, 2026-11-01: `Potential leak, kept on purpose:` with a test that the
late part adds nothing to the Gini). The mechanism is the same: a time on risk cut short after the prediction point,
with early-ended records claiming more at the same length (2.4% against 1.5% at 0.1 years or less). What sets frempl
apart?
(a) The length known at a record's start is only an upper bound (31 December); no contracted term ships, unlike
spanish's portfolio policies, which run from 1 January. So no value known at the start can be restored, as for spanish's
new business. Recorded as `Potential leak, kept on purpose:` with the measurement above (Gini 0.286 against 0.301 on a
log1p fit, claim AUC 0.690 against 0.632) and a revisit condition (a release with the contracted term or why a record
ended), and "the family's call" reworded as the suggested call. (b) Treat frempl like spanish: for the early-ended
records, replace `Exposure` by the length from the start to the year end. (c) Reopen spanish's portfolio fix to match
frempl. (d) Change the rule: a LEAK-10 Cases row or amendment for time exposure in insurance pricing, from fremtpl2's
call.

**Consistency check B (AI, 2026-11-01):** the insurance drafts of this batch ship the claim cost on two scales:
frempl and spanish on log1p, australian raw, all scored by the Gini on the amount (the scale changes only what a model
fits: here log1p LightGBM 0.286, Tweedie 0.275, squared error on the raw amount 0.251). frempl follows CLEAN-16 and
Lennart's MET-3 calls of 2026-10-21. What sets australian apart?
(a) Its source, a GLM textbook (de Jong and Heller 2008), models the raw cost with Tweedie and zero-adjusted models,
while frempl's source names no model. Recorded as an exception to CLEAN-16 on australian. (b) Treat australian like
frempl (log1p). (c) Reopen frempl to the raw scale. (d) Amend CLEAN-16 for zero-inflated insurance costs (the raw,
Tweedie scale).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): frempl_french_motor_personal_line**

**Position: ship after definition fixes. None of them costs the task.** The panel found two real P4 problems: the late
part of `Exposure`, and the successor shortcut under random records. Each has a fix in `dataset.py` that keeps all
115,155 rows and costs nothing measurable on the declared metric. Everything else is notes and wording. Nothing found
goes past the second rung of the remedy ladder ("fix the definition", principles step 5).

**1. A real pricing task on faithful data (P2, P3, P5).**
- Claim: the rows are an insurer's 2004 exposure lines: the rating factors and the claim cost that a tariff study
  uses, exactly as the source publishes them.
- Evidence:
  - All 10 checksums match (claim audit, claim 1).
  - The blind reviewer rebuilt the 115,155 rows from the public `.rda` files without the definition. The target
    equals log1p(clip(ClaimAmount, 0)) to 1e-10.
  - The amounts have mass points at 1,418.61 (427 rows), 102.59 and 4,326.53, which look like French fixed-cost
    claim conventions: real claims, not generated ones.
  - Domain practitioner: "Yes, as a challenger to a GLM on a realistic, if thin, French tariff table."
  - 26 of 39 claims hold, and none of the refuted ones touches scope, ethics or provenance.
- Rules: scope (SEL) holds. SEL-1 holds, with `Gender` noted. USE-1 holds, and USE-8 `approximate` is declared
  honestly. PROV-8 holds (pinned to commit 3f5c00c). PROV-9 holds (2014, verified at 1.0-7). PROV-13 holds (the
  source's own 1.2-1 dedup).
- Answers the undocumented guarantee, loss basis and sample cuts (USE-5, LEAK-24):
  - These already sit behind `approximate`.
  - The column audit narrows the guarantee gap. The counter that rises after a claim shows that the amount spans
    windscreen 40%, at fault 28%, not at fault 17%, parking 9% and fire-theft 6%: the policy's total motor claim cost.
  - Tension row "a real task against imperfect cleaning": keep the task and note the rest. None of these gaps changes
    what the target means.

**2. Fifteen of the sixteen features are known at the prediction point (P4, LEAK-10 Must holds for them).**
- Evidence:
  - The claim counts are taken at the record's start. A counter rises at the next record after 95.3% of the claims
    and after 2.3-3.1% of the other records (claim audit 16, column audit).
  - `BonusMalus` moves after 11.6% of the claims, because it is updated at the anniversary.
  - `ClaimInd` (1 exactly where the amount is positive) and `RecordEnd` are dropped.
  - No test row has an exact feature copy in train (0.0%).
- What it shows: the problem is one column, not the task. Independent failures are not conflicts, so this point does
  not excuse point 3.

**3. `Exposure`: the late part is real, and LEAK-7 fixes it without losing the feature (P4, LEAK-10 Must, LEAK-7
Should).**
- Concession: 25,131 records (21.8%) end before 31 December with no continuation. For them the realised length is a
  consequence of the outcome.
  - They hold 20.7% of the exposure and 38.9% of the claim cost.
  - The 3-decimal `Exposure` alone tells an ended-early record from an open one at AUC 0.91 (column audit).
  - So the note's premise is wrong: dropping the dates does not hide the end.
- Mildest fix (column audit, problem 1):
  - In `_clean`, before the dates are dropped, give those records the `Exposure` of the open records that start on the
    same day. That is the value known at the start.
  - Keep the continued records as they are. Add a `Potential leak, kept on purpose:` note on the residue: continued
    records cost 407 per exposure-year, against 311 for open ones.
  - Measured: the Gini goes from 0.288 to 0.339 and the claim AUC from 0.689 to 0.675, on 9 of 9 folds each way. The
    shipped value inflated the claim AUC and hid the large claims that ended contracts. It did not inflate the
    declared score.
- Why this rather than the alternatives:
  - Dropping `Exposure` (the builder's option, claim AUC 0.565) is a harsher rung.
  - Setting every row to the length from the start to the year end (claim audit: Gini 0.292, AUC 0.633) also throws
    away the renewal ends, which are known at the start.
  - Keeping the value as in fremtpl2 fails LEAK-10's second clause, which fixes late values wherever they can be
    located. "No consistent Gini gain" (precedent check) is the "removing it changes no score" test, which the
    LEAK-7/LEAK-10 case row of 2026-10-21 rules out as a reason to keep.
  - The dates set frempl apart from fremtpl2 (CC, 2026-10-20). So the fix follows the rule without reopening the
    curator's call: a precedent is followed only on the same facts.
  - The curator settles it as consistency check A, option (b).
- Also: reword "the family's call of 2026-10-30" to "the AI's suggested call" (claim audit 10).

**4. The split: group on the chain to remove the measured successor shortcut, at no cost (P4, SPLIT-9 tension row,
SPLIT-8 Must, SPLIT-24 Must).**
- Concession:
  - Under random records, a fifth of each test fold has its policy's next record in train.
  - That record's claim counts rose after 87% of the test record's claims and after 0.9% of its non-claims.
  - A lookup built from training features only lifts the declared Gini from 0.282 to 0.403 (claim audit 14).
  - The successor does not exist when the record is priced. USE-10's "known policy" argument (split audit) covers the
    policy's past, not its future.
  - The tension row settles it: "a shortcut that can be measured is always removed".
- Mildest fix:
  - Ship the chain id that `_decisions` already computes as the group column, not as a feature.
  - Use grouped folds, tagged `ForcedGroupedFromTemporal` (SPLIT-8: grouped by the entity when its periods recur).
  - The key is built exactly from consecutive raw rows with the same profile, each starting on the previous end. The
    shuffled control finds 1 such link by chance. It follows the SPLIT-24 case in_vehicle_coupon_recommendation
    (consecutive blocks in the raw file order).
- Cost: none measured.
  - Plain LightGBM scores 0.277 grouped against 0.282 random (claim audit).
  - Grouped by component, it scores Gini 0.2785 against 0.2827 and AUC 0.6899 against 0.6901 (split audit).
  - Under chain folds the lookup falls to AUC 0.54 and no longer lifts the claim AUC.
- Residual, for the curator:
  - 10,292 records continue only in another file, and one chain fold of three still gains (+0.065).
  - Grouping on the cross-file components (split audit) costs nothing measured either, but that key has about 1% chance
    links: a weighing of exactness (SPLIT-24) against coverage.
  - The successor that stays in the test fold is an evaluation-level path (LEAK-9).
- Why a fix and not an exit: re-splitting is the second rung of the ladder, and the tension row "a real task against a
  leak" fixes the leak and keeps the task.

**5. The metric: the Gini family is right, and the row form is a weighing call for the whole family, not a blocker
(P6, MET-11 Must, MET-1 Must, MET-10 Weigh).**
- Evidence for the Gini:
  - Every agent agrees that RMSE would score the wrong thing. The true claim indicator times the claimants' mean reaches
    only R^2 0.096, and untuned LightGBM -0.04 to 0.00, while the same model ranks claims at AUC 0.69. That is MET-11's
    context case ("the default would score the wrong thing").
  - The scorer is verified (claim audit 27): it returns 0.2627, the Gini computed by hand on the amount, with
    3,540-3,740 claims per test fold.
- Concession: the reason overstates its sources.
  - Liberty Mutual used a weighted Gini, Frees et al. order by the relativity to a premium, and Allstate's rows were
    whole vehicle-years.
  - Here exposure runs from 0.001 to 1, and raw `Exposure` alone scores 0.213 against the model's 0.283 (domain
    practitioner, claim audit 29).
- Mildest fix: keep `normalized_gini` and correct the reason. Say that it scores the period's total cost, length
  included, and give the 0.213 figure and the swing of 0.09 that one claim causes in a fold.
- Why the better metric waits for a family decision:
  - The exposure-weighted Gini on the annual rate (domain practitioner, option a) needs `Exposure` as a scoring column
    (MET-2).
  - It needs a new general metric with a reference implementation (MET-12, MET-13).
  - australian, spanish and the pricing games need the same answer.
  - So it is one decision for the curator, not a reason to hold this dataset alone.
- Fold noise is a factor (MET-10), not a failure. Each repeat holds the 802,620 claim in exactly one fold, so the
  repeat means stay comparable (split audit, note A). Capping changes the target as recorded, which is the curator's
  call.

**6. Worth benchmarking (P6, TP-2 Should, TP-4 Must, TP-5 Must).**
- Evidence:
  - Not trivial: the model beats raw `Exposure` on 9 of 9 folds (0.283 against 0.213; TP-4).
  - The linear model beats the dummy on 5 of 5.
  - 115,155 rows and about 3,600 claims per test fold, far from `Too Small` (TP-5).
  - After the fix in point 3, the Gini rises to 0.339.
- Answers the blind reviewer's "low signal, methods tie" (tuned LightGBM against ridge, 0.0002 ± 0.0009 R^2):
  - TP-2: a small real signal is "no reason to retire".
  - forest_fires (kept, R^2 0.013) has the same zero-inflated shape: only the claim part carries signal.
  - acquire_valued_shoppers_challenge and amex_non_iid_1m were kept with no spread.
  - That tie is R^2 on log1p, not the declared Gini.
  - The blind reviewer's own verdict is include.

**7. The file choice, uniqueness and cleaning hold; the fixes are wording (P5, PROV-7 Must; P7; EV-5).**
- Uniqueness holds:
  - freMPL1 stays out: 39.1% of its contracts are in files 5-9, and 793 of 815 amounts are equal.
  - freMPL2-4 stay out (derived amounts), and so does freMPL10 (another schema, 0.08% claims).
  - fremtpl2 is another portfolio, period and schema (PROV-7).
- Concession on the file note: "near-random slices" is wrong, and its evidence is accuracy against the majority class
  (EV-5). Claim rates run 7.7-10.0% by file.
  - Stacking without a file column still holds. Leave-one-file-out scores like the random folds (AUC 0.690 against
    0.687, Gini 0.284 against 0.285), and a new record has no file.
  - Fix: reword the note with these numbers.
- Concession on the negatives: they are not recoveries on earlier claims. Of those with a continuation, 95.1% are
  followed by a rise in the not-at-fault counter (column audit).
  - The clip stays: the negatives are -2.4% of the net cost, and the pricing_game_2017 definition clips the same way.
  - Fix the text in the notes, in `predicted`, in the Decision and in the acceptance reason for
    `task_target_value_dominant`: "0 = no claim, or a not-at-fault claim recovered in full".
- Smaller wording fixes:
  - AIcrowd's game ran in 2020-21 on the 2017 game's portfolio.
  - `OutUseNb` counts out-of-use periods, not claims.
  - The record's screening lines are superseded (EV-2): the year, "431 against 309", and the file sizes.
- All of these are P7 and record fixes, cheap and safe (principles step 3).

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds (Gender noted, SEL-1); USE-1 holds, USE-8 approximate; LEAK-10 holds for 15 features, triggered
on Exposure (21.8% unforeseen ends, located row by row), fixed by LEAK-7 (the start-known value for those rows);
SPLIT-9 shortcut (successor's counts, Gini 0.282 -> 0.403 with a lookup) fixed by chain-grouped folds,
ForcedGroupedFromTemporal (SPLIT-8, SPLIT-24); PROV-7, PROV-8, PROV-9 hold.
Value: TP-2 small real signal (keep); TP-4 not trivial (9/9); MET-11 context Gini kept, reason corrected.
Quality: negatives clip kept, reason corrected; file note and wording corrected.
Weighed: source + (every column documented, version pinned), size +, use case + (a real tariff table), signal -,
fold noise -.
For the curator: consistency check A (Exposure as spanish, not as fremtpl2); chain against component grouping; the
family's metric form (row Gini against exposure-weighted Gini on the annual rate).
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (2026-11-01): frempl_french_motor_personal_line**

```text
Verdict: do not ship as defined; ship after changes 1-3 (the definition) and 4-6 (text).
Validity: SPLIT-9 triggered (a policy's later records in train tell a test record's claim), fix: group on the policy
  chain (SPLIT-8, ForcedGroupedFromTemporal). LEAK-10 triggered on `Exposure` (unforeseen ends, located row by row),
  fix by LEAK-7. PROV-7 holds, but the evidence given for it breaks EV-5.
Value: MET-1 triggered: the row Gini on the period's total scores the period's length; the exposure-weighted form,
  a family decision.
Quality: the negative amounts are described wrongly (EV-2); note and record corrections (EV-2).
Exclusion: none asked. Every Must here can be fixed in the definition.
```

**1. The random split shows the model a test record's claim through the policy's later records (P4, SPLIT-9 Must, with SPLIT-8 Must).**
- Problem. 30% of records continue in a later record of the same policy: 34,324 links within files, 1 by chance with
  the rows shuffled. More continue across files: 10,292 records continue only in another file, and 53% of test records
  have a record of their policy in train (split auditor). The later record's claim counts rise after 86.8% of the
  earlier record's claims and after 0.9% of its non-claims (claim auditor).
- Effect on the task. At a record's start its successor does not exist: an insurer knows a policy's past, not its
  future. Under the shipped folds, 19.4-20.0% of each test fold has its successor in train. On those rows the
  successor's counts identify the test claim at AUC 0.93.
- Evidence (claim auditor, claim 14). The lookup uses the shipped training features only: same profile, `DrivAge`
  +0/1, `LicAge` advanced by the length. It reads no labels, dates or file order. Added to LightGBM, it lifts the
  declared Gini from 0.282 to 0.403 and the claim AUC from 0.689 to 0.741, on 3/3 folds. Under chain-grouped folds
  the lookup alone drops to AUC 0.54 (0.63 random), and with it the model's claim AUC is lower than without it (0.680
  against 0.689).
- The tests read the other way prove nothing here. The builder's chain-fold comparison and the split auditor's
  paired mate test (-0.0017 ± 0.0018) both used LightGBM. LightGBM reads one row at a time and cannot take a cross-row
  path, whatever the data holds. A test that cannot come out the other way proves nothing (EV-6). Whether in-context
  models (TabPFN, TabICL) take the path is untested (EV-7, cannot verify).
- Rule. The principles' tension row on SPLIT-9: "a shortcut that can be measured is always removed, whatever it costs
  the floor". alfa_battle_2_0_task_2 has the same mechanism: a later row of one client tells the earlier outcome, and
  that client's training rows were dropped. USE-10 makes a known entity's history legitimate, and history is the past.
  Here the past already reaches the record through its claim counts and `BonusMalus`.
- Like cases. pricing_game_2017_french_mtpl (one year, French MTPL, this batch) groups by client because "the claims
  of the client's other vehicles in that year are not known". spanish groups by policy. SPLIT-8 names this regime:
  grouped by the entity, `ForcedGroupedFromTemporal`.
- Cost: none measured. Grouped by component: Gini 0.2785 and AUC 0.6899, against 0.2827 and 0.6901 random (split
  auditor, 3x3). Grouped by chain: Gini 0.277 against 0.282 (claim auditor).
- Remedy (fix the definition).
  - Build the chain id in `_clean`; `_decisions` already computes it. Ship it as the group column, never a feature,
    and tag the split `ForcedGroupedFromTemporal`.
  - Which key: the within-file chain is constructed exactly (consecutive raw rows, exact profile and date continuity),
    as in in_vehicle_coupon_recommendation (SPLIT-24). The split auditor's cross-file component also covers the 10,292
    cross-file continuations, but it links on age tolerances (465 chance links under a 7-day shift). The curator
    decides whether it meets SPLIT-24.
  - Rewrite `task_summary.split`, `splits_comment` and decision 3.
  - Put the measured valid windows in `splits_comment`, as SPLIT-8 asks: 13-39% of the rows, claim AUC 0.55 / 0.59 /
    0.62 against 0.60 / 0.59 / 0.62 for as many random records (split auditor, issue 1).

**2. For records that ended with no successor, the realised `Exposure` is set by the outcome (P4, LEAK-10 Must, fixed by LEAK-7 Should).**
- Problem. 25,131 records (21.8%) end before 31 December with no continuation, an end not foreseen at the start.
  Claims drive these ends (column auditor):
  - they hold 20.7% of the exposure but 38.9% of the claim cost: 837 per exposure-year, against 311 for open records;
  - they hold 66 of the 109 claims in the top 1%;
  - at a length of 1-3 days, 2.7% of them have a claim, against 0.4% of open records.
- Dropping the dates does not hide it. The exact 3-decimal `Exposure` alone tells an ended record from an open one at
  ROC AUC 0.91, and at 0.61 when rounded to months. My second check, a model-free lookup per value, gives 0.914 /
  0.915 / 0.914, and 0.61 rounded (a script in the run folder). So the note's "the start date
  together with `Exposure` gives it away" is refuted: `Exposure` gives it away alone.
- Effect on the task. The decisive test (column auditor, EV-1): give those records the value known at the start, the
  open records' `Exposure` for the same start day, which reads no label. The declared Gini rises from 0.288 to 0.339,
  higher on 9/9 folds. The claim AUC falls from 0.689 to 0.675, lower on 9/9. So the shipped value changes what is
  measured: it inflates the frequency ranking and hides the large claims that ended their contracts.
- Rule. LEAK-10's second clause (2026-10-26, Lennart): late cells that can be located go. Only cells that cannot be
  located row by row stay with a note, and only when the part that can be traced shows no gain. The clause adds: "a
  'removing it changes no score' test alone is still no reason to keep". The precedent checker's LEAK-6 keep rests on
  exactly that test (no consistent Gini gain when every record gets the start-known length), and LEAK-6's narrowing
  covers only cells that cannot be located.
- Precedents. fremtpl2 (CC, 2026-10-20) has other facts: no dates there locate the early ends. spanish (this batch)
  reset the cancellations it could locate. What sets this case apart: `RecordEnd` with `_continues_next` locates the
  early ends row by row.
- Attribution. The note cites "the family's call of 2026-10-30", but that was an AI suggestion. The curator's CC of
  that day set only `Yes` and priority 5 (principles, "Who decides").
- Remedy (fix the definition, LEAK-7).
  - In `_clean`, before the dates are dropped, set `Exposure` of the records with `RecordEnd` and no continuation to
    the open records' `Exposure` for the same `RecordBeg`.
  - Keep the continued records as they are, with a `Potential leak, kept on purpose:` note (407 against 311 per
    exposure-year) and a revisit condition.
  - Rewrite the `Exposure` note, the `fit_reason` clause and the attribution.
  - The change departs from the fremtpl2 call, so it goes to the curator as a consistency check.
  - Fallback if the curator keeps the realised length: round it to whole months, which removes the end-status code
    (AUC 0.91 to 0.61) at no cost (Gini 0.282 against 0.283), and label the bullet `Potential leak, kept on purpose:`
    with these numbers and a revisit condition (definitions.md).

**3. The declared row Gini scores the period's length as much as the risk (P6, MET-1 Must; MET-11; MET-10 Weigh).**
- Problem. `normalized_gini` sorts rows by the predicted total and weighs every record the same, whatever its length
  (0.001 to 1 year). The practice the reason cites does not do this (domain practitioner; claim auditor, claim 29):
  - CAS Monograph 5, sec. 7.2.4, sorts by predicted loss cost against cumulative exposure;
  - Frees, Meyers and Cummings order by the relativity to a premium (read from the abstract and slides, not the full
    text);
  - Liberty Mutual scored a weighted Gini;
  - Allstate's rows were whole vehicle-years.
- Effect on the task. `Exposure` alone scores 0.213, 75% of the full model's 0.283, and it beats a model of all the
  risk factors without `Exposure` (0.191). Under the exposure-weighted Gini on the annual rate, `Exposure` alone scores
  about 0, and the two models swap places: 0.182 with `Exposure`, 0.203 without (9 splits, two auditors). A metric that
  ranks two models the opposite way to the practitioner's metric does not score the task "the way a practitioner would
  have chosen a model" (MET-1).
- Resolution (MET-10). The 802,620 claim moves its fold by about 0.09: the fold SD is 0.044, and 0.018 without that
  claim. A constant prediction scores -0.016 to +0.101, depending on the frame order.
- Remedy (fix the definition; a family decision).
  - Declare the exposure-weighted ordered-Lorenz Gini on the annual loss cost, with the realised exposure as a scoring
    column, never a feature (MET-2). After change 2 the feature and the scoring column are different columns.
  - Ship it as a general library metric (MET-12, MET-13). `normalized_weighted_gini` exists, but it orders by the raw
    prediction. The alternative is to ship the annual rate with `Exposure` as the weight.
  - australian, spanish and the pricing games declare the same row Gini, so the curator decides once for all of them.
  - Keeping the row Gini would be a reading of MET-1 to record, since a Must has no exceptions. The reason must then
    state the 0.213-of-0.283 share and the swap.

**4. "Near-random slices" is refuted, and it was argued from accuracy against the majority class (P5, PROV-7; EV-5 Must).**
- Problem. The note and the record rest the claim on a file accuracy of 31.0% against 28.1%, which EV-5 bars as
  evidence. What was measured instead:
  - claim rates by file run from 7.7% to 10.0% (chi2 p 2e-16), a spread 2.4 times the largest of 200 random
    relabellings (claim auditor);
  - the per-file one-vs-rest AUC is 0.57-0.64 (split auditor);
  - 10,485 policy components span two or more files.
- Effect on the task. None on stacking: leave-one-file-out scores like the random folds (AUC 0.690 against 0.687).
  It matters for change 1, because policies cross files.
- Remedy (text), in the note and the record. Write "samples of one portfolio drawn differently (claim rate 7.7-10.0%
  by file; why is undocumented), sharing policies across files", and give the AUC numbers instead of the accuracy.

**5. The negative amounts are claims of the period, not "no claim" (EV-2 Must; the target's description).**
- Problem. Of the 246 negative-amount records that have a continuation, 95.1% are followed by a `ClaimNbNonResp` +1.
  That happens for 0.19% of zero records and 18.6% of positive claims. Their rate grows with the length, like a claim's
  (column auditor). So they are not-at-fault claims recovered in full, and `ClaimInd` = 0 means "no positive net
  cost", not "no claim".
- Effect on the task. The clip to 0 stays: pricing_game_2017 clips the same way, and the negatives are -2.4% of the net
  cost. The text is wrong: `predicted` ("0 ... those without a claim"), the negatives bullet ("presumably recoveries on
  earlier claims"), the target bullet, decision 2, and the reason proposed for accepting `task_target_value_dominant`.
- Remedy (text). Write "0 = no claim, or a not-at-fault claim recovered in full (0.84%)". Also, AIcrowd's game ran in
  2020-21 on the 2017 game's portfolio; it was not "its 2017 pricing game".

**6. Note and record corrections (EV-2: a later measurement supersedes).**
- `curation_comments`:
  - "12% otherwise" in the counts bullet includes counts falling out of the 4-year window. A rise follows only 2.3% of
    non-claims (column auditor).
  - `OutUseNb` counts out-of-use periods, not claims, so `task_summary.known` should not call it one.
  - The first bullet should say that 38% of the starts are 1 January, the calendar cut, not a pricing event (domain
    practitioner).
- Record:
  - year 2014 (NEWS of 1.0-7), not empty;
  - 3,805 records span all of 2004, not none;
  - 34,324 chain links against 1 by chance, not "431 against 309", so policyholders can be traced;
  - the 1.2-1 file sizes are 16,000-32,400, not 20,600-38,300.
- Remedy: text, in the same change as 1-3.

**Files**
- Second check of the end-status code: a script in the run folder (not committed).
- Evidence cited: claim-auditor.md (claims 9, 14, 19, 29, 30), column-auditor.md (problems 1, 2), split-auditor.md
  (issues 1-3), domain-practitioner.md (metric table), precedent-checker.md (item 3, check A), the panel's reports.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): frempl_french_motor_personal_line**

The critic and I agree on the verdict (ship after changes) and on the remedies for points 1, 2, 4, 5 and 6. Two
disputes are left. One is the framing of the `Exposure` fallback. The other is whether the metric (point 3) fails
MET-1 on this dataset or is a reading for the whole family. One new fact came up: I ran the critic's own metric check,
which the brief does not report.

**1. Split: conceded in full.**
- I accept chain-grouped folds tagged `ForcedGroupedFromTemporal`, with the chain id shipped as the group column.
- I also accept the addition I missed. SPLIT-8 asks for "the cost measured against the valid windows", so the valid
  windows go into `splits_comment`: 13-39% of the rows, claim AUC 0.55 / 0.59 / 0.62 against 0.60 / 0.59 / 0.62 for
  as many random records.
- EV-6 point accepted. LightGBM cannot take a cross-row path, which is why my concession rested on the lookup and not
  on the paired tests.
- Key: the within-file chain by default, because it is built exactly (SPLIT-24). Whether to use the cross-file
  component instead, with about 1% chance links, is the curator's call. We agree on this.

**2. `Exposure`: the fix is conceded. I dispute the fallback.**
- Month rounding is not a remedy for LEAK-10.
  - It removes the 3-decimal code for the end status (AUC 0.91 to 0.61).
  - But the realised length of the 25,131 unforeseen ends stays, so nothing measured changes: Gini 0.282 against
    0.283, the critic's own numbers.
  - The effect the decisive test found (Gini 0.288 to 0.339, claim AUC 0.689 to 0.675) sits in the length, not in the
    decimals.
- Rule:
  - LEAK-10's second clause (Must) removes late cells that can be located, and a Must has no exceptions.
  - So keeping the realised length would be an amendment of LEAK-10, fremtpl2's reading made general. It would not be
    a `Potential leak, kept on purpose:` note (principles, "Exceptions and amendments" and "Consistent judgement",
    case 1).
  - The curator can choose that, but it should be offered as an amendment.

**3. Metric: partly conceded, partly disputed, on a new fact.**
- Conceded:
  - The sources the reason cites do not support the row form when exposure varies.
  - The practitioner's metric is the exposure-weighted Gini on the annual rate (CAS Monograph 5, sec. 7.2.4).
  - "Correct the reason", my fix in the opening brief, does not settle MET-1 by itself.
- New fact. I ran the critic's metric script on the column auditor's aligned
  records (untuned LightGBM, 3 seeds x 3 random folds). Output in the run folder (not committed).

  | model | row Gini (SD) | weighted Gini on the rate (SD) |
  |---|---|---|
  | no length | 0.188 (0.023) | 0.264 (0.045) |
  | shipped `Exposure` | 0.288 (0.049) | 0.195 (0.030) |
  | fixed `Exposure` (change 2) | 0.339 (0.052) | 0.277 (0.019) |
  | fixed `Exposure` alone, as the score | 0.281 (0.057) | - |

- What follows:
  - The critic's MET-1 evidence is that the two metrics "rank two models the opposite way". That swap comes from the
    realised `Exposure`, the LEAK-10 problem of point 2, not from the metric.
  - After change 2, both metrics put the fixed-length model above the no-length one: on the row Gini 9/9 (+0.151), on
    the weighted Gini 6/9 (+0.012). So the row Gini no longer misorders the models that would ship.
- Still conceded:
  - Under the row Gini, the start-known length alone scores 0.281 of the model's 0.339 (83%).
  - The fold SD is 0.052, against 0.019 for the weighted form.
  - Both favour the weighted form: the unit clause of MET-1 (a rate per car-year) and resolution (MET-10).
- Ties: a constant scores -0.016 to +0.101 under the row Gini (claim audit 30). The constant rate scores -0.017 to
  +0.101 under the weighted Gini (domain practitioner's probe, `rate_expo`). Both come from breaking ties by row order,
  so the fix belongs in the library metric (average the ties). It does not decide between the two forms.
- Disputed: that MET-1 blocks this dataset alone. Whether the row form meets MET-1 when exposure varies is one reading
  for australian, spanish, the pricing games and this dataset (the critic agrees: "decide once").
  - If the curator takes the weighted form, adopt it here: realised `Exposure` as a scoring column (MET-2), shipped as
    a library metric (MET-12, MET-13).
  - If the curator keeps the row form, record it as the family's MET-1 reading, with the 83% share and the SD in the
    reason.
  - On this evidence I would recommend the weighted form.

**4. "Near-random slices": conceded.** I add the critic's wording: "sharing policies across files" (10,485 components
span two or more files).

**5. Negative amounts: conceded.** The text becomes "0 = no claim, or a not-at-fault claim recovered in full (0.84%)",
and the AIcrowd date is corrected.

**6. Note and record corrections: conceded.**
- The counts bullet: "a rise after 95% of the claims, 2.3% otherwise". The old "12%" counted falls out of the window.
- `OutUseNb` is not a claim count.
- The 38% of starts on 1 January are the calendar cut, not a pricing event.
- The record lines on the year, the 3,805 full-year records, the chain links and the file sizes.

**Judgment record after the rebuttal**

```text
Verdict: ship after changes 1-2 (definition) and 4-6 (text); change 3 after the family's metric decision.
Validity: SPLIT-9 fixed by chain-grouped folds (SPLIT-8, SPLIT-24), valid windows stated; LEAK-10 fixed by LEAK-7 on
the 25,131 unforeseen ends; keeping the realised length would be an amendment, not a kept-leak note.
Value: after change 2 the row Gini and the weighted Gini rank the candidate models the same way (9/9, 6/9); the row
form still gives the length alone 83% and has 2.7 times the fold SD: the family should pick the weighted form.
Quality: file, negatives and wording corrections conceded.
For the curator: consistency check A; chain or component key; the family's metric (MET-1 reading).
```

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (2026-11-01): frempl_french_motor_personal_line**

The advocate concedes my points 1, 2, 4 and 5 and asks for the same remedies. What remains is the metric (their
point 5, my point 3). I settled that question with a new measurement, and the measurement goes against my opening
point.

**New fact (EV-1).** I repeated the metric comparison on the column that change 2 produces: the records that ended
with no continuation get the open records' `Exposure` for the same start day. Setup: untuned LightGBM with the
builder's settings, log1p target, 3 seeds x 3 random folds. Script in the run folder (not committed). The tie-order caveat of change 1 applies here too.

| features | row Gini (declared) | exposure-weighted Gini on the annual rate |
|---|---|---|
| no length | 0.188 | 0.264 |
| shipped `Exposure` | 0.288 | 0.195 |
| fixed `Exposure` (change 2) | 0.339 | 0.277 (beats no length on 6/9) |
| fixed length alone, as a raw score | 0.281 | (constant rate) |

The order of the two models swapped only because of the shipped `Exposure`, that is, because of the leak. Once the
column is fixed, both forms rank the models the same way. The model also beats the fixed length alone on 9/9 folds
(0.339 against 0.281, a script in the run folder), so TP-4 still holds.

**Point by point**

1. **A real task on faithful data (P2, P3, P5).** I concede it, and I raised nothing against it.
2. **15 of the 16 features known at the prediction point (LEAK-10).** I concede it.
3. **`Exposure` (LEAK-10 Must, LEAK-7).** We agree on the fix, the consistency check A option (b) as spanish did, and
   the rewording of the attribution. I keep one addition. If the curator keeps the realised length instead, round it
   to whole months and label it `Potential leak, kept on purpose:`. The exact value gives away whether a record ended
   early (AUC 0.91, and 0.61 rounded; re-checked by a script in the run folder), and rounding costs nothing (Gini 0.282
   against 0.283).
4. **The split (SPLIT-9 tension row, SPLIT-8, SPLIT-24).** We agree. On which key to group by, the evidence favours
   the advocate's mildest one, the within-file chain:
   - Under chain folds, the lookup lowers the claim AUC on 3/3 folds (0.680, 0.678, 0.681 against 0.687, 0.687,
     0.692; claim auditor). So the frequency shortcut is gone.
   - The one fold with +0.065 Gini has a plain Gini of 0.215, the level of the folds that hold the 802,620 claim
     (0.211-0.237 in the split audit). That is circumstantial; read it as fold noise (MET-10).
   - So I drop my preference for the cross-file component. It stays an option for the curator, with its 1% chance
     links (SPLIT-24).
5. **The metric (MET-1, MET-11, MET-10).** I concede the remedy: keep `normalized_gini`, correct the reason, and send
   the choice of form to the curator as one decision for the whole insurance family.
   - My MET-1 case rested on the swap in model order. The new measurement shows that swap was the leak, which change
     2 removes.
   - The row form still gives the length most of the score: the fixed length alone gets 0.281 of the model's 0.339
     (83%). So the curator still has a real call between the two forms, but it is no longer a failed Must.
   - One condition holds (EV-8): the corrected reason must give the numbers on the shipped, fixed column (0.281 of
     0.339, the 0.09 swing that one claim causes in its fold), not the pre-fix 0.213 of 0.283 the advocate cites.
6. **Worth benchmarking (TP-2, TP-4, TP-5).** I concede it. The TP-4 note in the definition must be re-measured on the
   fixed column: model against raw length, 0.339 against 0.281, model ahead on 9/9.
7. **Files, negatives, wording (PROV-7, EV-5, EV-2).** I concede it. These are the same remedies as my points 4 to 6.
   The record corrections include "no record spans all of 2004" (3,805 do), which the advocate's list leaves out.

**Where this leaves the verdict**

```text
Verdict: ship after changes (changes 1-2 in the definition, the rest text); no dispute left between critic and
  advocate on the remedies.
Validity: SPLIT-9 fixed by within-file chain groups, ForcedGroupedFromTemporal (SPLIT-8, SPLIT-24); LEAK-10 on
  Exposure fixed by LEAK-7 (consistency check A, option b).
Value: MET-11 context row Gini kept, reason corrected with post-fix numbers; the form (row against exposure-weighted)
  a family weighing call. TP-4 holds after the fix (9/9).
Quality: file note (EV-5), negatives text, record corrections (EV-2).
For the curator: check A (Exposure, as spanish); the family's Gini form.
```

</details>
