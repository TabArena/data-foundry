# frempl_french_motor_personal_line

**Outcome:** added. The AI recommends shipping it: the re-review panel of 2026-11-06 under the exposure rules found
that a policy's later record could sit on the other side of the split when its contract change also changed one profile
column, and the component is widened to close it on Lennart's mark of 2026-11-08 (issue 8); its text changes are made
(below), and on 2026-11-08 Lennart chose the identity scale with the length to 31 December kept (issue 7) and confirmed
that length unrounded (issue 9). Like every container with a `sample_weight`, it enters no run before the collection's
training-weight gate (`BENCHMARK_CHANGES_TODO.md`, "Training weights", "The gate"). A French private insurer's motor
portfolio of 2004 (CASdatasets freMPL5 to freMPL9, 115,155 records, each a policy's period of cover with fixed rating
factors); the target is the period's claim amount per realized year, shipped untransformed and scored by the
exposure-weighted Gini of the ordered Lorenz curve (a context metric), with the realized length as each record's weight
in training and scoring; all records of one policy component stay on one side of the split. Validity: SEL-1 holds
(`Gender` left the features on 2026-11-08 under the collection's stance on sex in insurance pricing, and stays in
the component's key); USE-1 holds, fit approximate (USE-8); LEAK-41 holds: the realized length `Exposure` is the rate's
denominator, the metric's weight and the `sample_weight`, never a feature (issue 6; it supersedes the fix of 2026-11-02
under LEAK-10, which kept the realized length on the continued records); the feature `length_to_year_end`, the part of
the time on risk known at the start, depends on the start day alone (one value per day), and its gain through the
weight is negative under both fits of probe 22 (-0.051 weighted Tweedie, -0.049 squared error on the cost per year, on
the folds of 2026-11-08, without `Gender`), with no other feature above noise; LEAK-10 holds for the other features; LEAK-24 cannot be
verified (issue 3); SPLIT-9 triggered and fixed for later records with the same profile (issue 1), and triggered again
where a contract change also changes one profile column: the later record fell in another component, could sit in
training and told a test record's claim to a model that reads training rows (+0.020, 9 of 9 splits); the widened
component keeps it on the test record's side (+0.001 on the new folds; issue 8); LEAK-9: a test record's later records
are test rows, and a model that reads them gains +0.26 to +0.44, so a protocol line forbids reading other test rows;
SPLIT-8 ships the one year as `ForcedGroupedFromTemporal` on Andrej's call of 2026-11-02; PROV-7, PROV-8 and PROV-9
hold. Value: TP-2, a small real signal: an honest weighted Tweedie fit scores 0.182, the weighted constant 0 and random
orders -0.001 (per-fold SD 0.035), and the fit beats the length to 31 December alone (0.006) on 9 of 9 splits (TP-4; the
folds of 2026-11-08); the task probe (2026-11-08, the identity scale) flags `no_signal`, but the flag reads an
R^2-type skill (+0.001 on the cost per year, which the tail dominates), while on the declared metric its linear family
scores 0.206 and the dummy 0 (5 of 5 splits; EV-3); MET-1 holds in part: the large claims decide the fold that holds
the largest (a loss cap of 50,000 moves it by 0.021 to 0.075), so the notes ask for paired fold comparisons.
1/`Exposure` alone scores 0.184, as much as the honest model, and `Exposure` as a feature lifts the model to 0.254; the
word "ceiling" that LEAK-41 and probe 22 use for 1/weight alone is cross-dataset item X2 ("From PR #47"). Quality:
CLEAN-16 holds since 2026-11-08 (issue 7): on the identity scale a weighted squared-error fit estimates the cost per
year, which the length to 31 December does not move, and scores 0.153 against 0.182 for Tweedie, led by the tail; on
the log1p scale shipped until then the length misled it (0.154 with it, 0.187 without); the negative amounts stay set
to 0. Weighed: the actuarial convention (a rate weighted by its time on risk) and a faithful, documented source +; an
approximate fit (a thin tariff, no vehicle or cover factors), fold noise and a low signal -. For Andrej: Lennart's D9
(issue 6) supersedes his `Exposure` fix of 2026-11-02 (issue 2 (a)) and his base of issue 4, which Lennart's CC line of
2026-11-08 names, confirming the unrounded length against his month rounding (issue 9); Lennart's mark on issue 8
widens his key of issue 1, in the direction of his call; the stance on sex drops `Gender`, which shipped with his
verdict of 2026-11-03 under an EU-law note. Follow-up, not an issue: a large-loss cap in scoring (each
loss capped at 50,000: on the 9 folds of 2026-11-08 one weighted Tweedie fit moves by 0.021 to 0.075 in the three folds
that hold the largest claim, from 0.238 to 0.163 on fold 1 of the first repeat, and by 0.008 at most in the others),
not offered yet; the metric is unchanged until then. Nothing is left open.

Changes made after the review panel (AI, 2026-11-01): the folds grouped by policy chain, `Exposure` fixed (issue 2), the
valid windows stated in `splits_comment` (SPLIT-8), the metric reason and the negatives text corrected, and the figures
re-measured on the shipped folds. The record's screening lines the data refutes (the year, the chain links, the file
sizes, "near-random slices", the negatives) are corrected at hand-over and need no mark. Changed on 2026-11-06 (issue
6): the target is the claim amount per realized year, `Exposure` the weight and no feature, the length to 31 December
the feature, the metric the Gini per unit of `Exposure`; `exposure_at_start` dropped; `fit_reason` no longer names a
kept leak; a protocol line against reading other test rows. Changed after the re-review panel (AI, 2026-11-06), text
only (rows, features, target, weight, split and metric unchanged): the protocol line gives the gain as +0.26 to +0.44,
depending on what is read, and says that a test record's successor is found without `policy_component`, from the
features and `Exposure`; the metric reason and the notes no longer call 1/`Exposure` alone the ceiling a leak would
reach; the notes ask for paired fold comparisons (random orders' per-fold SD 0.037, up to 0.071; the 802,620 claim
moves the fold that holds it by about 0.06) and say that the start date ships as the length to 31 December, one value
per day; issue 6's resolution marks the unrounded length as the AI's call, pending Lennart's mark (issue 9); issue 7
carries the panel's reading and the precedent checker's question. Changed on 2026-11-08 (issue 8, B): the policy
component also joins the later records that changed one profile column (61,091 groups, the largest 90 records; 68,857
before), so the folds changed, and every score in the notes and the metric reason is re-measured on them. Issues 7
and 9 keep their figures of 2026-11-06; on the new folds, squared error on log1p scores 0.152 with the length to 31
December and 0.184 without (lower with it on 9 of 9 splits; 0.156 and 0.185 before), a Tweedie fit 0.181 and 0.177
(higher with it on 6 of 9; 0.183 and 0.179), squared error on the cost per year 0.149 and 0.152 (0.159 and 0.163); the
month rounding moves a Tweedie fit by -0.005 (higher on 3 of 9; -0.002 before) and squared error on log1p by +0.002
(6 of 9; -0.001), and rounded, 2,714 records would repeat another record of their policy (2,704 before). Changed on
2026-11-08 (issue 7, b; issue 9, B): the target ships as `claim_amount_per_year`, the cost per year untransformed (no
`target_transform`), `length_to_year_end` kept and unrounded; `predicted`, the notes on the dates, the length, the
learners, the stand-ins and the target, and the metric reason carry the scores re-measured on the identity scale (the
same folds; the container orders its rows by their content, the target included, so the rows changed order and each
score moved by up to 0.005); CC lines for both issues. Changed on 2026-11-08 on Lennart's stance of
australian_vehicle_insurance_2004_2005's issue 7, sex is no rating factor of any insurance pricing task of this
collection (rows, target, weight, split and metric unchanged): `Gender` leaves the features after it has built the
policy component, so the partition is the same (61,091 components, the same test records in every split; the rows
changed order); `known`, `changes`, the notes, the metric reason and the splits comment carry the scores re-measured
without it. It carried nothing measurable: a weighted Tweedie fit scores 0.1815 with it and 0.1819 without (-0.0004,
SE 0.002, higher with it on 5 of 9 splits), squared error on the cost per year 0.1519 and 0.1527 (-0.0008, 5 of 9).
Without it 928 records repeat another's features and target (610 with it) and 0.6% of test rows have an exact feature
copy in training (0.4%); the leak probe flags nothing, and the task probe's linear family scores 0.206 on the
declared metric (0.203).

**Main points:** Nothing open. Resolved: 1, 3 and 4 on 2026-11-03, 6 on 2026-11-06, 8, 7 and 9 on 2026-11-08 (the
component widened; the cost per year on the identity scale with the length to 31 December kept; that length unrounded,
with Andrej's two superseded calls named). Verdict: ship (2026-11-03).
Changed on 2026-11-08 without an issue: `Gender` left the features, on Lennart's stance that sex is no rating factor
of any insurance pricing task (australian_vehicle_insurance_2004_2005's issue 7); it still builds the policy
component, whose 61,091 groups are unchanged, and it carried nothing measurable (-0.0004 with a weighted Tweedie fit).

**Issues for Andrej and Lennart:**

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
   feature (CLEAN-22, USE-6). It ships unrounded on the dataset agent's call, which is not part of D9 and is open as
   issue 9. `exposure_at_start` is
   dropped. Supersedes Andrej's call of 2026-11-03 (issue 4, option C); his unnormalised CAS form stays. On the shipped
   splits an honest Tweedie LightGBM scores 0.183, squared error on log1p 0.156, the weighted constant 0 and
   1/`Exposure` alone 0.184. A model that reads a test record's next record, a test row too under the grouped split,
   reaches 0.443, so the notes and the splits comment carry a protocol line: no feature or model step may use other
   test rows, and a method that does is called out and not benchmarked (LEAK-9). `dataset check`: 0 errors, 0
   warnings (the warning `task_feature_looks_like_exposure` is gone).

8. **Widen the policy component to the later records that change one profile column, or filter each fold?**

   * **Problem:**
     - A policy's later record joins its component only when all six profile columns are equal, so a contract change
       that also changes one of them (the risk area, the km limit, the vehicle use, the socio-professional category or
       the marital status) leaves the policy in two components, and its later record can sit in training while the
       earlier one is tested.
     - The later record's claim counters tell the earlier record's claim, so a model that reads training rows gains
       +0.020 on 9 of 9 splits, a shortcut the split has to remove whatever it costs[^8a].
     - The rule leaves you only the form of the fix: widen the component with these links (B), or drop each fold's
       candidate successors from its training side (C).
   * **Background:**
     - The component of issue 1 joins a record to one that starts the day it ends, with the same six profile columns,
       the driver's age the same or one more and the licence age advanced by the months between the starts.
     - The split auditor searched for a record that ends before 31 December and a record that starts that day with
       the same gender, a driver's age 0 to 1 higher, the licence age advanced, every claim and out-of-use counter at
       least as large and exactly one of the other five profile columns different: 9,160 such pairs over 7,120 earlier
       records, none of them in one component.
     - About 3,200 of the pairs are true links: the later record's counters rise after 75.5% of the earlier record's
       claims and after 41.9% of its other periods, while pairs with the end date shifted by one or two months show no
       such contrast (0.63 to 0.67 against 0.62 to 0.65), nor do pairs that differ in two or more columns.
     - By the column that changed, the rise after a claim against the rise otherwise: the km limit 0.939 against 0.073,
       the vehicle use 0.863 against 0.311, the risk area (5,788 pairs) 0.722 against 0.494, the socio-professional
       category 0.68 against 0.47, the marital status 0.72 against 0.46.
   * **Effect on the task:** a model that reads the training rows (nearest neighbours, retrieval, in-context learners)
     learns a test record's claim from its own policy's later record, which an insurer pricing the record at its start
     would not have; a gradient-boosted model that reads one row at a time cannot use it.
   * **Experiments:** the split auditor, the 9 shipped splits, untuned LightGBM with a Tweedie loss weighted by
     `Exposure`, one seed:
     - a lookup computed from the training rows only (the largest counter rise among a test record's candidate
       successors in training; 1,609 to 1,705 test rows per fold, about 4.4%, have one) lifts the honest score from
       0.1742 to 0.1945 (+0.0203, SD 0.0100, higher on 9 of 9 splits);
     - the flag "a candidate exists" alone gives -0.003 (higher on 3 of 9), so the gain is the claim the later record
       tells, not the early end;
     - with the component widened by these links (61,091 groups, the largest 90 records), the lookup's gain falls to
       -0.0045 (SD 0.009, higher on 4 of 9), and the honest score is 0.1686 against 0.1742, an unpaired comparison of
       different folds, inside the fold SD of about 0.03;
     - the filter of C drops about 1,700 to 2,500 training rows per fold (2% to 3%) and leaves the groups as they are.
   * **Consistency:** B applies your choice of issue 1 (the most conservative key, its chance links accepted) to the
     same mechanism[^8b]. The widened key is the current rule with one profile column relaxed, built from the data;
     about two thirds of its new links are chance (about 1% in issue 1's key), and a chance link only joins two
     policies into one group, the stricter side[^8c]. This is the path issue 1 closed for later records with the same profile, at about a fifth of
     its size.
   * **Panel:**
     - The split auditor found the route and recommends B: it fits your call for the most conservative key, at a cost
       inside the noise.
     - The advocate first named C as the mildest fix and then accepted B, since B also moves the successors to the
       test side, where the protocol line against reading other test rows covers them[^8d].
     - The critic asks for B, since both fixes stand on the same rung of the remedy ladder, so the precedent of issue 1
       decides[^8e].
     - The mediator recommends B, since C drops training rows chosen by a contract change that often follows a claim,
       close to the rule against training on rows selected by the realized length[^8f], and has to be repeated at
       every re-split.
   * **Not proposed:** widening only by the km-limit and vehicle-use links (2,049 pairs, the near-exact ones): it
     leaves most of the route open and does not meet the rule.
   * **Cost:** either fix changes the shipped splits, so the container is rebuilt, only on your ask; under B every
     score in the notes, the metric reason and these issues is re-measured on the new folds.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Six-column key (implemented) | the component of issue 1, 68,857 groups | no rebuild | the shortcut stays: +0.020 on 9 of 9 splits for a model that reads training rows |
     | B | Widen the component | also joins a record to a successor that differs in one profile column: 61,091 groups, the largest 90 records | the lookup's gain falls to -0.0045; your most conservative key of issue 1, applied to the same mechanism; the successors become test rows, under the protocol line | about two thirds of the 9,160 new links are chance (about 3,200 true), against about 1% in the key of issue 1; a chance link only joins two policies; groups of up to 90 records; every score re-measured |
     | C | Per-fold filter | drops from each fold's training side the candidate successors of its test rows, about 2% to 3% of the training rows; the groups unchanged | the key of issue 1 stays | training rows dropped for a contract change that often follows a claim; repeated at every re-split; the links among the test rows stay without a group |

   * **Recommendation:** B: it is your choice of issue 1 applied to the same mechanism, it puts the successors on the
     test side, where the protocol line covers them, and its measured cost is inside the fold noise; C if the key of
     issue 1 should stay as it is. **Decision:** B or C?

   **Notes for the AI:** SPLIT-9 is a Must, so A is no outcome; the mediator's issue 1 of the re-review of 2026-11-06.
   On B: extend `_policy_components` with the one-column links as the split auditor built them (a record ending before
   31 December; a record starting that day with the same `Gender`, `DrivAge` 0 to 1 higher, `LicAge` advanced by the
   months between the starts within 1, every claim and out-of-use counter at least as large, and exactly one of
   `MariStat`, `SocioCateg`, `VehUsage`, `HasKmLimit`, `RiskArea` different); restate the counts (61,091 groups, the
   largest 90 records) in the `Grouping` definition, `splits_comment`, the notes and the third `Decision`; add to the
   LEAK-9 bullet that the protocol line also covers the one-column successors, now test rows (the mediator's change 1);
   re-run `dataset check`, the leak and group probes and the lookup test (gain near 0), and re-measure the scores of the
   notes, the metric reason and issues 7 and 9 (the rebuild only on the curator's ask). On C: override `_make_splits`
   to drop from each fold's training indices the candidate successors of its test rows (the same link rule), give the
   dropped counts in `splits_comment`, and re-run the same checks.

   [^8a]: **SPLIT-9** (Must; amended 2026-11-05, Lennart): a training row whose label tells a test row's outcome and
     was not yet known at the prediction point must not be in train, such as a label of the test row's own entity set
     after its prediction point; "The shortcut is measured and removed, whatever it costs". Its Tensions row in
     principles.md: "a shortcut is always removed".
   [^8b]: Andrej, 2026-11-03, issue 1: "What is the most conservative option that is the safest to not leak?", then
     "I choose B", the cross-file policy component, about 1% of its links by chance.
   [^8c]: **SPLIT-24** (Must): group on a true group id, or on one constructed exactly from the data; never on a
     similarity-threshold cluster.
   [^8d]: **LEAK-9** (Should; amended 2026-11-05, Lennart): an evaluation leak, where a model can read other test rows,
     is fixed by a protocol line the benchmark checks, not in the data.
   [^8e]: principles.md, "How to decide", the remedy ladder: repair from the origin; fix the definition (drop, lag,
     filter, re-split, re-target); keep it with a documented note; exclude. A filter and a widened group are both a
     fix of the definition.
   [^8f]: **LEAK-41** (Must; 2026-11-06, Lennart): "No model is trained or scored on rows selected by the realized
     weight (such as full-year rows only)".

   **Resolved (2026-11-08, Lennart):** B, the component widened: it also joins a record to a successor with the same
   gender, starting the day it ends, the driver's age the same or one more, the licence age advanced by the months
   between the starts within one, exactly one of the other five profile columns changed and no counter lower, which
   gives 61,091 groups of 1 to 90 records, the same groups the split auditor measured. On the new folds none of the
   9,160 pairs crosses a split and the lookup gains +0.001 (SD 0.012, higher on 5 of 9; the auditor's own folds gave
   -0.0045), `dataset check` shows 0 errors and 0 warnings, the leak and group probes flag nothing, the notes, the
   metric reason, the Grouping text, `splits_comment` and the third Decision carry the new counts and the re-measured
   scores, and the protocol line names the one-column successors; the container is rebuilt only on your ask.

7. **Keep the log1p scale and the length to 31 December together, although together they mislead a squared-error fit?**

   * **Problem:**
     - Issue 6 keeps the target on the log1p scale and the length to 31 December as a feature, and a squared-error fit
       on that scale ranks short periods too low when it sees the length (0.156 with it, 0.185 without, on the shipped
       splits).
     - The rule on log-scale rates asks to drop such a feature or to ship the identity scale[^7a], while the leak rule
       says that the part of the weight known at the start ships as its own column[^7d], and this length is that part.
     - The leak rule ranks higher, so its sentence is an instruction, not a permission: only the identity scale (C)
       meets both rules as written, and dropping the length (B) needs that sentence amended first[^7e].
   * **Background:**
     - A squared-error fit on log1p of the cost per year estimates the exposure-weighted mean of log1p(cost per year),
       not the cost per year the Gini orders by.
     - A short period's cost per year is large when it has a claim, but a claim is rarer, so that mean rises with the
       time to 31 December (0.29 up to 3 months, 0.98 to 1.08 from 9 months on) while the cost per realized year stays
       at 394 to 469 and the claims per realized year at 0.20 to 0.22.
     - The length to 31 December equals the realized length on the 55,700 records open at the year end and bounds it
       on the others; it depends on the start day alone (one value per day), so it is known when the period
       starts[^7c].
     - Your D9 keeps both the length ("stays a feature") and the log1p scale[^7b]: B reverses the first clause, C the
       second, and the rule D9 cites for the scale names the identity scale as one of its two remedies.
   * **Effect on the task:** most regression learners fit squared error on the target as shipped; with the length they
     lose about 0.03 of Gini for a reason unrelated to the risk, while a learner with a Tweedie loss gains 0.005 from
     it.
   * **Experiments:** untuned LightGBM weighted by the realized length, the 9 shipped splits, 3 seeds:
     - squared error on log1p: 0.156 with the length, 0.185 without (lower with it on 7 of 9 splits, -0.029, SE 0.010);
     - Tweedie on the cost per year: 0.183 with it, 0.179 without (higher with it on 5 of 9, +0.005, SE 0.004);
     - squared error on the cost per year itself: 0.159 with it, 0.163 without, led by the tail (up to 11.6 million
       per year, a claim of 58,087 on a record of under two days);
     - without the length, squared error on log1p scores as the Tweedie fit with it (+0.001, higher on 6 of 9);
     - the blind reviewer, without our notes, found the same mechanism on its own folds: a model of the log target
       ranks claims at AUC 0.627 with the length and 0.560 without, a Poisson rate model at 0.572 and 0.569.
   * **Consistency:**
     - pricing_game_2016_french_fleet, the sibling with the same facts, kept its length to the year end, known at the
       start, and ships the identity scale (Lennart, 2026-11-06)[^7f]; the precedent checker found no fact that sets
       this table apart from it.
     - Dropping a length known at the start for this reason has no applied precedent:
       spanish_motor_insurance_coverage_level_2022_2024 dropped `total_exposure` as a length corrected on some rows and
       realized on others, under the leak rule, and has no start date to build a known part from[^7f].
     - Keeping both (A) needs an exception to the rule on log-scale rates, and no fact sets this table apart from the
       rule or from pricing_game_2016_french_fleet.
   * **Panel:**
     - The advocate and the domain practitioner favour B: the length is a cut made by the extract's calendar year, not
       a rating factor, it is worth +0.005 (SE 0.004) to a Tweedie fit, and the leak rule's own table says the length
       known at the start "may stay a feature", which they read as a permission.
     - The critic favours C: a rule's text outranks a row of its table, so B would break the higher-ranked rule to meet
       the lower one, while C meets both and follows pricing_game_2016_french_fleet.
     - The mediator settles the reading by rank for C and offers B only with the leak rule's sentence amended into a
       permission ("a part known at the start may ship as its own column"), after which B against C is your weighing
       call: the log1p scale and the squared-error learners on it against a legitimate input worth 0.005 and the match
       with the sibling.
   * **Unknown:** only LightGBM was measured; other squared-error learners should show the same trend, which sits in
     the target's weighted mean by length.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the length on log1p (implemented) | as issue 6 decided | an input known at the start stays; a Tweedie fit gains 0.005 | squared-error fits on the shipped scale lose 0.029 (7 of 9 splits); needs an exception that no fact supports |
     | B | Drop the length, with the leak rule amended | `length_to_year_end` leaves the features; target, scale and weight unchanged; the leak rule's sentence first becomes "a part known at the start may ship as its own column" | squared-error and Tweedie fits score alike (0.185 and 0.179); keeps your scale | a rule change first; drops an input known at the start, worth 0.005 to a Tweedie fit; reverses D9's "stays a feature"; no applied precedent |
     | C | Identity scale | the cost per year ships untransformed; the length stays | meets both rules as written; follows pricing_game_2016_french_fleet; a squared-error fit then estimates the cost per year | squared-error fits score 0.159, led by the tail; reverses D9's log1p scale |
     | D | Amend a rule to say which wins | the rule on log-scale rates or the leak rule says which wins for a length known at the start on a log-scale rate; this table then follows it (B or C) | settles this table and the next one alike | a rule change prompted by one case |

   * **Recommendation:** C: it is the only option that meets both rules as written, and it follows
     pricing_game_2016_french_fleet; B only together with the leak rule amended (D), after which B against C is a
     weighing call; A needs an exception that no fact supports. **Decision:** A (then name the fact that sets this
     table apart from the rule and from pricing_game_2016_french_fleet), B, C or D?

   **Notes for the AI:** the mediator's issue 2 of the re-review of 2026-11-06 (CLEAN-16, Should, against LEAK-41's
   "A part known at the start ships as its own column", Must; settled by rank under principles.md, "Conflicts between
   rules"). On C: ship `claim_amount_per_year` with `target_transform="identity"`, rewrite the target, learners and
   stand-in bullets, `predicted` and the metric reason's numbers, record the curator's call in a CC line that names the
   clause of D9 it reverses (the log1p scale), and re-run `dataset check`, the leak and task probes, probe 22 in both
   arms and the measurement of 2026-11-06. On B: the main session first amends LEAK-41's sentence in leak_checks.md
   (date, curator, this case) and the Mechanisms row's case text; then drop `length_to_year_end` in `_clean` (the
   asserts on the length known at the start can stay), rewrite `known` and `changes` in the task summary, the bullets
   on the dates, the length, the learners and the stand-in and the metric reason's numbers, record the CC line (it
   reverses D9's "stays a feature"), and re-run the same checks. On D: the main session amends CLEAN-16 in
   cleaning_features.md or LEAK-41 in leak_checks.md (date, curator, this case); then B or C as the amended rule says.
   On A: an exception line to CLEAN-16 with the fact the curator gives, in the record and the notes, and a row of kind
   `exception` in CLEAN-16's Cases table (the main session).

   **Lennart (2026-11-08, discuss):** In another cases we are already discussing this, so check for
   pricing_game_2016_french_fleet. should the length to X be a feature at all? what should we do here with our rules
   from raw data/state ignoring prior decisions?

   **Answer (AI, 2026-11-08):** Keep the length to 31 December and ship the cost per year on the identity scale, as
   pricing_game_2016_french_fleet does, or keep log1p and drop the length by amending the leak rule?

   * **Problem:**
     - You ask whether the length to 31 December should be a feature at all, worked out from the raw data and the
       rules instead of the calls of 2026-11-02 to 2026-11-06, and alike for pricing_game_2016_french_fleet, which
       ships the same length.
     - In both tables the length is the start day in another unit, 31 December is a cut of the release (here) or of
       the source (there) that no one prices on, and with the cost per year as the target it adds no signal that can
       be measured.
     - It matters only on the log1p scale, where any form of the start day misleads a squared-error fit, so the real
       choice is the scale: the rules as written keep the length and ask for the identity scale, and dropping the
       length needs the leak rule's sentence on a part known at the start amended first.
   * **Background:**
     - What the length is here: one value per start day (366 days, 366 values, in exact reverse order of the day of
       the year), and the start date ships in no other form. 48.4% of the records are still open at 31 December, the
       release's end, where the length equals the realized length; 38.2% start on 1 January, the release's start.
     - What it is in pricing_game_2016_french_fleet: the same formula from `period_start` (and the vehicle count, 2 on
       two periods), and `period_start` ships beside it as a date. Periods are cut at 31 December in every year, in
       the 2014 file too, while contracts start on any day: where a vehicle's next period follows a cut within the
       year, the contract's age class steps up at 19% of those cuts, an anniversary. So 31 December is the source's
       year, not a contract's term.
     - What the actor uses: the insurer prices a year of cover from the policy's anniversary, which the release does
       not give; the fleet insurer charges a rate per vehicle-year, earned pro rata; the game's players had each 2014
       period's vehicle-years in their file. With the cost per realized year as the target, the length is no
       denominator any more: it is a covariate, the start date recoded[^a7a].
     - The length would have a role of its own only under a target per period, where it bounds the period's time on
       risk. pricing_game_2016_french_fleet issue 6 asks about such a target (the weight removed); the answer there is
       to keep the rate, so in both tables the length stays a covariate.
     - Why log1p reacts: a short period rarely has a claim, but its rate is large when it has one. So the mean of
       log1p(rate), weighted by the realized length, rises with the length (here 0.29 up to 3 months, 0.98 to 1.08
       from 9 months on; there 0.15 to 0.52), while the cost per realized year stays flat (here 394 to 469; there 164
       to 200 per vehicle-year). A squared-error fit on log1p learns that rise and ranks short periods too low; on the
       identity scale the same fit estimates the cost per year that breaks even, which the length does not move[^a7b].
     - The rules, read from the raw data: the start date is known when a record starts, so it is a legitimate input,
       and it is nothing that takes a column out of the features[^a7c]; the length is the part of the time on risk
       known at the start (it bounds the realized length and equals it on the open records), which the leak rule
       ships as its own column[^a7d]; the scale rule then asks for the identity scale or the column dropped[^a7b], and only the identity
       scale meets both as written[^a7e]. The exposure study listed the length to 31 December as a planned term; the
       data shows it is a cut of the release, which an amendment could rest on but which does not change what the
       rule asks now.
   * **Experiments:** here, untuned LightGBM weighted by the realized length on the 9 shipped splits (the policy
     component widened by issue 8), 3 seeds; in pricing_game_2016_french_fleet, its regularised LightGBM weighted by
     the vehicle-years on its three windows (5 seeds) and on the 3 x 3 folds by contract of its issue 6.

     | Fit (this table) | With the length | No start information | Start's day of the year instead | Flag "starts on 1 January" instead |
     |---|---|---|---|---|
     | squared error on log1p | 0.152 | 0.184 | 0.152 | 0.185 |
     | squared error on the cost per year | 0.149 | 0.152 | 0.150 | 0.150 |
     | Tweedie on the cost per year | 0.181 | 0.177 | 0.181 | 0.178 |

     - The start information adds nothing beyond noise to the cost per year: Tweedie +0.004 with it (SE 0.004,
       higher on 6 of 9 splits), squared error on the cost per year -0.003 (SE 0.006). On log1p it costs squared
       error 0.032 (SE 0.005, lower with it on 9 of 9).
     - On log1p, the start's day of the year misleads exactly as the length does (0.152 both), so the harm is the
       start day's information, not the column's name. The flag keeps the record type (carried into 2004 or begun in
       it) but no length below a year: it misleads nothing and adds nothing (0.185 against 0.184 without).
     - On the identity scale, squared error scores 0.032 below Tweedie (SE 0.004, 9 of 9) with the length and 0.029
       without, led by the tail of a rate over records as short as a day (up to 11.6 million per year). On log1p
       without the length the two fits score alike (0.184 and 0.177).
     - pricing_game_2016_french_fleet shows the same pattern. On its identity scale the length and the start together
       add 0.006 to Tweedie (SD 0.012, folds by contract; 0.008 on the windows), and dropping the length alone changes
       nothing (+0.001), since the start date carries the same information. On log1p both time columns would cost
       squared error 0.022 (9 of 9 folds by contract), though not on its windows, where each window holds one cohort
       of lengths. Squared error on its identity scale scores 0.002 to 0.010 below Tweedie: its source left out every
       period under 30 days, so its tail stops at 75,929 per vehicle-year.
   * **Consistency:**
     - pricing_game_2016_french_fleet keeps its length and its start date on the identity scale (your D11), so b
       gives the two tables the same scale and the same inputs; c drops its length too, under the same amendment, and
       keeps its start date, the time column of its split.
     - australian_vehicle_insurance_2004_2005 ships its cost per year on the identity scale;
       spanish_motor_insurance_coverage_level_2022_2024 keeps log1p and has no length known at the start (its
       `total_exposure`, realized on some rows, left the features).
     - What sets this table apart from pricing_game_2016_french_fleet is the tail, not the length: records as short as
       a day here, none under 30 days there. It is the fact c would rest on.
   * **Prior calls:** your D9 (target, weight, metric) stands under every option; a keeps both its clauses on the
     length and the scale, b reverses its log1p scale, c reverses "the length stays a feature". Andrej's month
     rounding of 2026-11-02 stays open as issue 9 under a and b and falls away under c. The re-review's reading by
     rank (identity scale unless the leak rule is amended) is what b follows and what c amends.
   * **Issue 9 under each option:** under a or b it stays, recommended B (confirm the unrounded length in one CC line
     that names Andrej's two calls D9 superseded), with its figures re-measured on the widened folds: rounded to
     months, 2,714 records would repeat another record of their policy, and the Tweedie fit loses 0.005 (SE 0.0015);
     under c no length ships, so it closes, and the CC line of c names those two calls.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Log1p with the length (implemented) | as issue 6 decided | an input known at the start stays; nothing changes | squared error on log1p loses 0.032 (9 of 9 splits); needs an exception to the scale rule that no fact supports |
     | b | Identity scale, the length kept | the cost per year ships untransformed; the length stays, unrounded (issue 9); pricing_game_2016_french_fleet unchanged | meets every rule as written; the same scale and inputs as pricing_game_2016_french_fleet; the length then costs no fit anything | squared error scores 0.149, 0.032 below Tweedie, led by the tail; reverses D9's log1p |
     | c | Log1p, the length dropped, the leak rule amended | the sentence on a part known at the start is limited to a term of the cover, so a distance to a cut of the release or the source may go; no start information ships here; pricing_game_2016_french_fleet drops its length and keeps its start date | squared error and Tweedie score alike (0.184 and 0.177); drops a column that is no term and adds nothing measured; keeps D9's scale | a rule change first; the start date goes with it here; reverses D9's "stays a feature"; no applied precedent |

   * **Recommendation:** b: read from the raw data, the rules keep the start information as the length and settle the
     scale rule by the identity scale, which gives this table the scale and inputs of pricing_game_2016_french_fleet,
     and on that scale the length costs no fit anything. c if you weigh squared-error fits on this table's tail above
     the rules as written, as an amendment that reaches pricing_game_2016_french_fleet too. a needs an exception that
     no fact supports. **Decision:** a, b or c?

   **Notes for the AI:**
   - All options: the notes' bullets on the dates and on the length say that 31 December is the release's end (48.4%
     of the records still open there, 38.2% starting on 1 January), not a term of the policy, and give its worth on
     the cost per year (Tweedie +0.004, SE 0.004; squared error on the cost per year -0.003).
   - b: in `dataset.py`, `TARGET = "claim_amount_per_year"`; in `_clean`, `df[TARGET] = df["ClaimAmount"] /
     df["Exposure"]` with the assert that `df[TARGET] * df["Exposure"]` rebuilds `ClaimAmount`; drop
     `target_transform="log1p"` from the metric (identity), keep `params={"per_unit": True}` and the weight
     `Exposure`. Rewrite `task_summary.predicted` (no log1p), the target bullet, the learners bullet (CLEAN-16: on the
     identity scale a weighted squared-error fit estimates the cost per year that breaks even; the tail costs it 0.032
     against Tweedie), the metric reason's numbers, and the CC line in Lennart's name that names D9's log1p clause as
     reversed (CLEAN-16 as amended, LEAK-41's sentence on the part known at the start). Then issue 9's CC line (B).
     Re-run `dataset check`, the leak and task probes, probe 22 in both arms and the measurement of 2026-11-06
     (`final.py`) on the new scale; the rebuild only on the curator's ask. pricing_game_2016_french_fleet: nothing.
   - c: the main session first amends LEAK-41's sentence in leak_checks.md in place (date, curator, this case), for
     example: "A part known at the start that is a term of the cover (a planned term the actor sets) ships as its own
     column (LEAK-7, LEAK-37); the time from the start to a cut the release or the source makes, such as a calendar
     year's end, is an input like any other and may go where it misleads a fit on the shipped scale (CLEAN-16)", and
     the Mechanisms row's "(which may stay a feature)" to match. Then here: `_clean` stops adding
     `length_to_year_end` (`RecordBeg` stays dropped); rewrite `task_summary.known` and `changes`, the bullets on the
     dates, the length and the learners, and the metric reason's numbers; CC line naming D9's clause reversed and
     Andrej's two superseded calls; issue 9 resolved as moot. In pricing_game_2016_french_fleet: `_clean` stops adding
     `exposure_to_year_end` (`period_start` stays); rewrite `known`, `changes`, `predicted` where they name it, the
     Exposure and probe-22 bullets, Decision 1's text; CC line. Re-run the same checks in both.
   - a: an exception line to CLEAN-16 with the fact the curator gives, in the record and the notes, and a row of kind
     `exception` in CLEAN-16's Cases table (the main session).

   **Lennart (2026-11-08, discuss):** Reply (b): Identity scale, the length kept

   **Resolved (2026-11-08, Lennart):** b: the target ships as `claim_amount_per_year`, the claim amount per realized
   year untransformed, and `length_to_year_end` stays a feature, unrounded (issue 9), which reverses D9's log1p scale
   and gives the table the scale and inputs of pricing_game_2016_french_fleet; weight, metric and split are unchanged.
   On the same folds a weighted Tweedie fit scores 0.183 and squared error on the cost per year 0.154 (0.029 lower on 9
   of 9 splits, led by the tail); `dataset check` shows 0 errors and 0 warnings, and the leak probe, probe 22 under
   both fits and the task probe flag nothing new (the task probe's `no_signal` reads an R^2 skill of +0.001, while
   its linear family scores 0.203 on the declared metric against 0 for the dummy).

   [^a7a]: **MET-14** (Should) and **MET-15** (Must), 2026-11-06: an amount over a realized time on risk ships as the
     rate per unit, and the realized time on risk is the metric's row weight and the training weight, never a feature.
   [^a7b]: **CLEAN-16** (Should; amended 2026-11-06, Lennart): "A rate scored by a Gini keeps the scale the curator
     chose for the table, and the notes say what a weighted fit on that scale estimates. A log-scale rate with its
     denominator as a feature misleads L2 fits (...); drop the feature or ship the identity scale."
   [^a7c]: **USE-6** (Must): anything known at the prediction point is a legitimate input; "dropping it changes the
     task". **CLEAN-22** (Must): columns leave for what they are (a leak, an identifier, a copy, the measurement that
     defines the label), never for how many there are.
   [^a7d]: **LEAK-41** (Must; 2026-11-06, amended 2026-11-08 on its last clause): "A part known at the start ships as
     its own column (LEAK-7, LEAK-37)." Its row in the Mechanisms table: "fix it to the length known at the start
     (which may stay a feature) or remove it".
   [^a7e]: principles.md, "Conflicts between rules": a higher part wins over a lower one (LEAK-41 is Part 3, CLEAN-16
     Part 7); "Exceptions and amendments": "A Must has no exceptions: only a higher-ranked Must overrides it, and
     anything else is an amendment."


   [^7a]: **CLEAN-16** (Should; amended 2026-11-06, Lennart): a rate scored by a Gini keeps the scale the curator chose
     for the table, and the notes say what a weighted fit on that scale estimates; a log-scale rate with its
     denominator as a feature misleads squared-error fits (spanish_motor_insurance_coverage_level_2022_2024: the mean
     log1p of the rate rises from 0.085 to 1.074 across exposure bands while the cost per year stays at 221 to 336):
     drop the feature or ship the identity scale.
   [^7b]: Lennart, 2026-11-06, D9: the target on the log1p scale as before, and the length to 31 December, known at
     the record's start, stays a feature.
   [^7c]: **USE-6** (Must): anything known at the prediction point is a legitimate input. **CLEAN-22** (Must):
     columns leave for what they are, never for how many there are.
   [^7d]: **LEAK-41** (Must; 2026-11-06, Lennart): "A part known at the start ships as its own column (LEAK-7,
     LEAK-37)". Its row in the Mechanisms table of leak_checks.md (time on risk cut short by the outcome): "fix it to
     the length known at the start (which may stay a feature) or remove it".
   [^7e]: principles.md, "Conflicts between rules": "Rules win over patterns (quick ways to apply them) and over
     precedents (how they were applied)"; "Exceptions and amendments": "A Must has no exceptions: only a
     higher-ranked Must overrides it, and anything else is an amendment"; "Consistent judgement", case 1: a call that
     would break a Must of a higher rank is offered as an amendment of the rule.
   [^7f]: pricing_game_2016_french_fleet, CC of 2026-11-06 (Lennart, D11): "the length to 31 December stays a feature
     as `exposure_to_year_end` (LEAK-7, LEAK-37)", "the scale stays the identity (CLEAN-16 as amended)";
     spanish_motor_insurance_coverage_level_2022_2024, CC of 2026-11-06 (Lennart, D10): "every premium is annualised
     and `total_exposure` leaves the features (LEAK-41); the log1p target and the weighted Gini stay".

9. **Keep the length to 31 December unrounded, against Andrej's month rounding of 2026-11-02?**

   * **Problem:**
     - The length to 31 December ships unrounded on the dataset agent's call, which undoes Andrej's rounding of every
       length to whole months (issue 2 (a), 2026-11-02), and an AI call does not outrank a curator's until a curator
       marks it[^9a].
     - The CC line of D9 names only Andrej's issue 4 of 2026-11-03 as superseded, though D9 also supersedes his issue 2
       (a), which kept the realized length on the 34,324 continued records.
     - The CC lines of the sibling tables name every call they supersede[^9b], so one line from you would confirm the
       unrounded length and name both calls, unless the rounding should come back.
   * **Background:**
     - The rounding of 2026-11-02 hid the decimals of the realized length, which told a continued record from an open
       one (AUC 0.92, and 0.71 once rounded).
     - The new column depends on the start day alone: it is the length the source gives the records open from that day
       to 31 December, one value per start day (366 values) at the source's precision of three decimals, so its
       decimals carry no end.
     - Rounded, 2,704 records would repeat the features and target of another record of their policy that starts 0 to
       15 days apart (3,445 such repeats in all, against 610), and the score would not move (-0.002 with a weighted
       Tweedie fit, -0.001 with squared error on log1p); these are the dataset agent's figures, which the panel did not
       re-run.
   * **Effect on the task:** none if you confirm, since only the record changes; if the rounding comes back (C), the
     length takes whole months and 2,704 records repeat another record of their policy.
   * **Consistency:** pricing_game_2016_french_fleet ships its length to the year end at the source's precision (0.01
     year) and the start day as a feature, and spanish_motor_insurance_coverage_level_2022_2024 kept the source's
     precision of its premiums; the precedent checker reads the unrounded column as consistent with both, a departure
     from Andrej's rounding with a stated fact[^9c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave as is (implemented) | the length ships unrounded on the AI's call; the CC line of D9 names issue 4 only | nothing to do | an AI call stands against Andrej's; the record misses a superseded call, unlike the siblings |
     | B | Confirm in one CC line | your CC line confirms the unrounded length with its fact and names Andrej's issue 2 (a) of 2026-11-02 and issue 4 of 2026-11-03 as superseded | the record matches the siblings; the call becomes a curator's | none found |
     | C | Restore the rounding | the length to 31 December rounded to whole months, as on 2026-11-02 | follows Andrej's call | 2,704 records repeat another record of their policy; gains nothing, since the column holds no realized decimals |

   * **Recommendation:** B: the column depends on the start day alone, so the rounding hides nothing, and the line only
     records who decided what. **Decision:** A, B or C?

   **Notes for the AI:** the mediator's issue 4 of the re-review of 2026-11-06 ("Who decides", principles.md). On B:
   append through the store API a CC line in Lennart's name, for example "CC (<date>, Lennart): the length to 31
   December ships unrounded (REVIEW.md issue 9 (B)): it depends on the start day alone, one value per day at the
   source's precision, so the month rounding of 2026-11-02 hides nothing (rounded, 2,704 records would repeat another
   of their policy). D9 (issue 6) supersedes Andrej's calls of 2026-11-02 (issue 2 (a): the realized length kept on the
   34,324 continued records, every length rounded to months) and of 2026-11-03 (issue 4, option C)." On C: round
   `length_to_year_end` to whole months in `_clean`, as the feature of 2026-11-02 was, restate the length bullet,
   record the CC line, and re-run `dataset check`, the copies count and the measurements of the notes.

   **Lennart (2026-11-08, change):** See discussion above

   **Answer (AI, 2026-11-08):** This issue follows issue 7, whose answer above waits for your choice.

   * Under issue 7's (a) or (b) the length stays, and this issue's B (a CC line confirming it unrounded, naming Andrej's
     calls of 2026-11-02 and 2026-11-03 as superseded) is still the recommendation; under (c) the length goes and this
     issue closes as moot.
   * The numbers moved with the wider policy component of issue 8: rounded to whole months, 2,714 records would repeat
     another record of their policy (2,704 before), and a Tweedie fit loses 0.005 Gini (SE 0.0015, lower on 6 of 9
     splits), so option C's "gains nothing" now reads as a small loss.
   * The Consistency bullet's second precedent changed on 2026-11-08: spanish_motor_insurance_coverage_level_2022_2024
     now rounds its annualised premiums to the cent (its issue 7), because their decimals marked a cut year; this
     length depends on the start day alone and holds no realized decimals, so that reason for rounding does not
     carry over.

   **Lennart (2026-11-08, change):** Agree.

   **Resolved (2026-11-08, Lennart):** B: a CC line confirms the unrounded length to 31 December with its fact (it
   depends on the start day alone, so rounding hides nothing; rounded to months, 2,714 records would repeat another
   record of their policy and a weighted Tweedie fit would lose 0.003 to 0.005 in two runs on the same folds) and names
   Andrej's calls of 2026-11-02 (issue 2 (a)) and 2026-11-03 (issue 4, option C) as superseded. The code is unchanged;
   the notes' bullet on the length says so.


   [^9a]: principles.md, "Precedence in the process", who decides: "the curator's decision (a `CC` line, a review
     mark) > an AI assessment > an AI draft marked unverified > imported or legacy values. A newer decision of the
     curator beats an older one." Andrej's CC of 2026-11-02 (issue 2 (a)): the records that end early without a
     continuation get the length known at their start, "every `Exposure` rounded to months".
   [^9b]: australian_vehicle_insurance_2004_2005, CC of 2026-11-06 (D8): "Supersedes Andrej's call of 2026-11-02
     (issue 2 ...) and changes the form of his Gini of the same day (issue 4 ...)"; pricing_game_2016_french_fleet,
     CCs of 2026-11-06 (D11): each names the call of Andrej it supersedes (issue 4 on the target, issue 2 (d) on the
     training sides).
   [^9c]: principles.md, "Consistent judgement, the curator's included": a decision that departs from a precedent
     names the fact that sets the case apart. Andrej, 2026-11-02, on spanish_motor_insurance_coverage_level_2022_2024:
     "do not round the premiums".

**Review panel:** ship after changes (mediator). Tier full, re-review of 2026-11-06 under LEAK-41, MET-14 to MET-16,
after decision D9 (issue 6): 12 reports. Claims: 30 audited, 26 hold (one within seed noise, one by reasoning), 1
refuted (the wording "1/`Exposure` alone, the ceiling a leak would reach", reworded in the definition), 1 not
reproduced (1/`Exposure` above the squared-error fit on 6 of 9 splits: 8 of 9 with one seed), 2 untested (the CAS
Monograph 5 section; the rounding figures of issue 9), and issue 7's conflict confirmed. Blind review: include with
changes; its main concern, the log1p rate with the length to 31 December, is issue 7, measured on its own folds (claim
AUC 0.627 with the length, 0.560 without); its call for a deviance or a frequency task is not taken, since a Tweedie
deviance scores worse than a flat rate here. Task gamer: the task can be gamed badly through a test record's later
records among the test rows (0.20 to 0.64), the route the protocol line forbids, whose figure is now restated; its
other exploits read `Exposure`, which `feature_columns()` drops. Agreed: D9's target, weight and metric; the length to
31 December known at the start; the grouped split; that the one-column successors must be fixed; the text changes
(made). Disputed: the fix for those successors, a widened component or a per-fold filter (issue 8; both sides now
prefer widening); dropping the length or the identity scale (issue 7, settled by rank for the identity scale unless
LEAK-41 is amended). Not dataset issues: the word "ceiling" in LEAK-41 and probe 22 (cross-dataset item X2); a
large-loss cap in scoring, to be measured first (the Outcome). The mediator's issues 1, 2 and 4 are issues 8, 7 and 9
here.

<details><summary>Mediator</summary>

**Mediator report: frempl_french_motor_personal_line (exposure re-review, full tier, 2026-11-06)**

The facts are settled. No disputed fact needed a new experiment: the two sides differ on remedies and on how to read the rules, not on any number. One factual correction to both sides is in agreed fact 9: the gamer's "features-only" link used each test row's `Exposure`.

**1. Judgment record**

```text
Verdict: ship after changes.
Validity: SEL and USE hold (USE-8, approximate fit). LEAK-41 holds: Exposure is the weight only. length_to_year_end is
  known at the start; its weight-mediated gain is -0.038 (Tweedie) and -0.060 (L2). USE-6 holds. MET-15 holds.
  PROV-7/8/9 hold. SPLIT-8 holds (forced grouped).
  SPLIT-9 is triggered (finding A: one-column successors cross the split, +0.020 Gini, 9 of 9 splits). The fix is in
  the definition: widen the component (recommended) or a per-fold filter. It reopens issue 1's key, so the curator
  marks it.
  LEAK-9 is an evaluation leak, kept with its protocol line. The line's figure is restated and the link route is named.
Value: TP-2, a small real signal (Tweedie 0.183; weighted constant 0; random orders 0.003, SD 0.037). TP-4 holds
  (the length alone scores 0.005). MET-1 partly: one claim moves a fold by about 0.06; noted, a cap to be measured.
Quality: CLEAN-16 departure open (issue 7). A has no fact that sets it apart. C meets every rule text. B needs LEAK-41's
  start-known sentence amended into a permission first.
Weighed: approximate fit -, fold noise -, actuarial convention and faithful source +.
For the curator: issue 1 (key for finding A), issue 2 (issue 7: B or C, and how LEAK-41 reads),
  issue 3 ("ceiling" amendment, joins X2), issue 4 (CC line), issue 5 (large-loss cap, optional).
```

**2. Changes to make now (no decision needed)**

1. **LEAK-9 protocol note (dataset.py notes line 188; REVIEW; CHANGES).** Rules: EV-2 and LEAK-9.
   - Replace "+0.260" with "+0.26 to +0.44 depending on what is read". The exploited scores are 0.44 to 0.64, against honest scores of 0.18 to 0.20:
     - claim auditor: +0.285;
     - split auditor: +0.355;
     - task gamer: +0.387 without `Exposure` among the inputs, +0.437 with it.
   - Add that the successor can be linked without `policy_component`: `length_to_year_end` minus the row's `Exposure` matches the next record's `length_to_year_end`, and `LicAge` rises by 12×`Exposure` (39% of rows linked, 99.7% of them within one group). This link reads the test rows' scoring column `Exposure`. So write "from the features and `Exposure`", not "from the features alone".
   - Once finding A's key is widened, add that the line also covers the one-column successors.
2. **"Ceiling" in the dataset's own texts** (metric reason line 220, notes line 186, REVIEW summary). Rule: EV-2; claim audit row 13 refutes the word.
   - New wording: "1/`Exposure` alone scores 0.184, as much as the honest model (0.183); `Exposure` as a feature lifts the model to 0.256".
   - This still states the score of 1/weight alone, which LEAK-41 requires. It only drops the refuted bound.
3. **REVIEW.md issue 6, "Resolved (2026-11-06, Lennart)" block.** Mark the "unrounded" clause as the AI's call, pending Lennart's mark. Rule: "Who decides" in principles.md; until a curator marks it, Andrej's rounding of 2026-11-02 outranks it.
4. **Notes, paired comparisons.** Say that models are compared by paired fold differences. Give the fold SD (random orders 0.037, up to 0.071) and the fact that one 802,620 claim moves fold 0 by about 0.06. Rules: TP-2, EV-2.
5. **Notes line 118, start date.** "Dropped the record dates" becomes: the start date ships as `length_to_year_end`, a one-to-one recoding (366 values). Rule: EV-2. This applies under A and C; under B the sentence is true again as written.
6. **Issue 7 in REVIEW.md.** Append the precedent checker's consistency prompt (section 5 below). Rule: principles.md, "Consistent judgement".
7. **Finding A** goes into REVIEW.md as a new issue for the curator's mark (issue 1 below).
8. **Knowledge files, stale number** (LEAK-41 Cases text; evidence.md line 200). Change "the honest model 0.176" to D9's 0.183. The metrics Cases row at line 316 already has it. This is a number update, not a rule change; the word "ceiling" itself is issue 3.

Not a change: the 967 negative amounts set to 0 are already in the notes and the accepted warning (claim audit row 23).

**3. Issues for the curator, ranked**

**Issue 1 (P4, SPLIT-9, Must). Finding A: one-column successors cross the split.**
- **Problem.** The component key joins records only when all six profile columns are equal. A contract change that also changes one of them (RiskArea, HasKmLimit, VehUsage, SocioCateg, MariStat) leaves the policy split across components. The later record can then sit in train, and its claim counters tell the test record's claim.
- **Evidence (split auditor).**
  - 9,160 pairs, about 3,200 true links.
  - The successor's counters rise after 75.5% of claims against 41.9% of non-claims; for HasKmLimit changes, 0.939 against 0.073.
  - A train-only lookup gains +0.0203 (SD 0.010) on 9 of 9 splits.
  - The "a candidate exists" flag alone gives -0.003, so the gain is the claim, not the early end.
- **Effect.** A model that reads training rows (kNN, retrieval, in-context learners) learns a test record's claim from its own policy's later record. Row-wise GBMs cannot use it.
- **Whether to fix: no decision needed.** Every Must has to hold, and nothing ranked above SPLIT-9 excuses it (principles step 4). The SPLIT-9 tension row says a shortcut is always removed. Both sides agree.
- **Decision: which fix.**
  - (ii) Widen the component with all one-column links. 61,091 groups, the largest 90 records. The lookup gain falls to -0.0045 (4 of 9). The honest score is 0.169 against 0.174, an unpaired comparison inside the fold SD of about 0.03.
  - (i) A per-fold filter: drop each fold's training rows that are candidate successors of its test rows (about 2-3% of training rows; groups unchanged).
- **Mediator.** Both are on the same rung of the remedy ladder (fix the definition), so mildness does not decide. Three things favour (ii):
  - Treat like cases alike: it is Andrej's issue-1 choice of 2026-11-03, the more conservative key with chance links accepted, applied to the same mechanism.
  - It encodes the link in the group column, so the successors move to the test side, where the LEAK-9 line covers them.
  - (i) drops training rows chosen by a contract change that follows a claim. That selection sits close to LEAK-41's last clause, and the filter has to be repeated at every re-split.
- **Not an option:** the narrower variant (HasKmLimit and VehUsage only). It leaves most of the route open and does not meet the Must.
- **Cost of (ii).** A rebuild, only on the curator's ask (house rule). Every score in the notes, the metric reason and the issue numbers is re-measured.
- **Recommendation:** (ii).

**Issue 2 (P7, CLEAN-16, Should, against how LEAK-41, a Must, is read). Issue 7: the length on the log1p scale.**
- **Problem.** The definition keeps both the log1p scale and `length_to_year_end`. CLEAN-16 (amended 2026-11-06) asks for one or the other: drop the feature or ship the identity scale.
- **Mechanism, measured.**
  - Weighted mean of log1p by length band: 0.29 to 1.01, while the cost per year stays flat at 394 to 469.
  - L2 on log1p scores 0.156 with the column and 0.185 without (lower on 7 of 9).
  - The blind reviewer found the same thing independently: claim AUC 0.627 with the column against 0.560 without for the log target, and 0.572 against 0.569 for a Poisson rate model.
- **Advocate's best case for B (drop).**
  - L2 and Tweedie score alike after the drop (0.185, 0.179). The only cost is Tweedie's +0.005 (SE 0.004).
  - The practitioner: the length is "a cut made by the extract's calendar year, not a rating factor".
  - LEAK-41's Mechanisms row says the length "may stay a feature".
  - Lennart's same-day CLEAN-16 names "drop the feature" as a remedy.
- **Critic's best case for C (identity scale, column kept).**
  - It meets CLEAN-16, LEAK-41 and USE-6 together.
  - It follows the nearest sibling with the same facts, pricing_game_2016_french_fleet (Lennart, 2026-11-06: identity scale, start-known length kept). The precedent checker found no fact that sets frempl apart.
  - B has no applied precedent: spanish dropped a hybrid under LEAK-41, which is a different reason.
  - Cost of C: L2 scores 0.159, driven by the tail (up to 11.6M per year). Tweedie is unaffected (0.183).
- **Settled by rank: how LEAK-41's sentence reads.**
  - The rule text outranks a Mechanisms or Cases row ("rules win over patterns and precedents").
  - LEAK-41 says "A part known at the start ships as its own column". It sits right after the list of columns that encode the weight, and it says that column's start-known part is shipped, not discarded. `length_to_year_end` is exactly that part (column audit: one value per start day, L >= E on every row).
  - As written, then, the sentence is a directive, and B would break a P4 Must to meet a P7 Should. That is not allowed (principles step 4; a Must has no exceptions).
- **Two more facts neither side raised.**
  - Lennart's own D9 CC says "the length to 31 December stays a feature (CLEAN-22, USE-6)". B reverses that clause.
  - C reverses the CC's scale clause. But CLEAN-16, which the CC cites for the scale, names the identity scale as its own remedy.
- **Option A (keep as is).** It needs an exception to CLEAN-16, and no fact sets frempl apart from the rule or from pricing_game_2016. It fails the test for an exception.
- **Decision.**
  - (c) C. Recommended: the only option that meets every rule text.
  - (b) B, only together with an amendment of LEAK-41's wording ("a part known at the start may ship as its own column"). It is offered as an amendment, not an exception (consistency case 1), so the next table is decided the same way. B against C then becomes a weighing call, with the evidence above.
  - (a) A, with an exception: not supported.
  - (d) Amend CLEAN-16 or LEAK-41 to say which wins for a start-known length on a log-scale rate.
- **What would settle the weighing**, if LEAK-41 is amended: whether the curator values the log1p scale (and L2 learners on it) above keeping a legitimate input worth +0.005 to Tweedie, and above matching pricing_game_2016.

**Issue 3 (P4, LEAK-41, Must, wording; cross-dataset, joins X2). "Ceiling" in LEAK-41, probe 22, evidence.md line 200 and metrics Cases line 316.**
- **Problem.** LEAK-41 asks each definition to state "the score of 1/weight alone as the ceiling a leak would reach". Here that is refuted. `Exposure` as a feature reaches 0.256 to 0.259 (probe22_actuarial: 0.240 against 0.183), about 0.07 past 1/E's 0.184.
- **Effect.** A reviewer would wave through a partial proxy at 0.20 as "below the ceiling".
- **Same gap as X2.** X2 (bemtpl97 and fremtpl2 panels) already shows that under a deviance, 1/weight is no ceiling either. Under a Gini, frempl shows the same.
- **Decision (amendment).**
  - (a) Call 1/weight alone "what the weight alone scores", and call the probe's leak reference (the weight as a feature next to the features) the size a perfect proxy would reach. Under a deviance, "the weight alone" means the weight fitted to the target, as X2 proposes.
  - (b) Keep the word, with a note that it bounds the weight alone only.
  - Mediator: (a), settled together with X2. Both sides agree it goes to the curator, not to the dataset agent.

**Issue 4 (recording; "Who decides"). Lennart's CC line.**
- **Problem.**
  - The unrounded `length_to_year_end` is the dataset agent's call. It supersedes Andrej's month rounding (issue 2 (a), 2026-11-02).
  - D9's CC names only Andrej's issue 4 (2026-11-03) as superseded. It also supersedes issue 2 (a), which kept the realized length on the 34,324 continued records.
  - The sibling CCs (australian D8, pricing_game_2016 D11) name every call they supersede.
- **Evidence for the call.** One value per start day, no realized decimals (column audit). Rounding would create 2,704 within-component repeats. It is consistent with pricing_game_2016 and spanish (precedent checker).
- **Decision.** Confirm with one CC line that names both superseded Andrej calls, or restore the rounding. Mediator: confirm; this is attribution only.

**Issue 5 (P6, MET-1, Weigh; optional, not now). Large-loss cap in scoring.**
- Capping at 50,000 moves fold 0 from 0.210 to 0.147. The 802,620 claim is 3.6% of all cost.
- Both sides want the cap measured on the 9 shipped splits before it is offered. The metric is unchanged until then.
- Decision only after that measurement.

**4. Agreed facts**

1. The target is log1p(ClaimAmount/Exposure); the round trip asserts.
2. `Exposure` is the weight scoring column, the metric's weight and `sample_weight`, and not among the 16 features. `exposure_at_start` is gone.
3. The scorer matches an independent CAS Gini to 4e-12. A weighted constant scores 0 on 9 of 9 splits; random orders score 0.002 to 0.003 (SD 0.037).
4. Scores:
   - Tweedie 0.182 to 0.183; L2 on log1p 0.152 to 0.156;
   - 1/E alone 0.184 (above Tweedie on 4 of 9);
   - `Exposure` as a feature +0.073 to +0.077 (9 of 9);
   - ignoring the weight costs Tweedie 0.023 (9 of 9).
5. `length_to_year_end` is a function of the start day: 0 of 366 days have two values, it falls strictly with the date, L >= E on all rows and L = E on 48.4%.
   - Without it, the tariff predicts `Exposure` at R² 0.003; with it, R² 0.34 (86% from it).
   - Weight-mediated gain: -0.038 (Tweedie), -0.060 (L2). No other feature is above noise.
   - It alone scores 0.005.
6. Issue 7's mechanism is measured: L2 0.156 with the column against 0.185 without (7 of 9); identity-scale L2 0.159; Tweedie gain from the column +0.005 (SE 0.004).
7. Data: 115,200 − 45 copies = 115,155 rows; 10,869 positive claims, as in the source; the target rebuilt with difference 0.
8. Grouped split: no component straddles a split. Test folds hold 38,281 to 38,532 rows and 3,570 to 3,675 claims. An in-year temporal split would train on rows chosen by their realized weight (12.8% of rows by 1 April, cost 1,140 against 311 per year), which LEAK-41 forbids.
9. Successor route within test (LEAK-9): exploited scores +0.26 to +0.44.
   - Linking without the group id reaches 39% of rows, 99.7% of them within one group.
   - The link uses each test row's `Exposure`. Neither brief says so; whether `length_to_year_end` and `LicAge` alone suffice was not measured.
10. Finding A as stated under issue 1. Its widened alternative: 61,091 groups, gain -0.0045, honest score 0.169.
11. Fold noise: one claim moves a fold by 0.06; a random column spreads Tweedie by about 0.04. The Tweedie deviance does worse than a flat rate on 3 of 3 folds.
12. The dataset texts, LEAK-41, probe 22 and evidence.md call 1/weight alone the "ceiling", which the measurement refutes.

**5. Disputed points, settled**

- **Finding A remedy: widen (ii) or filter (i).**
  - No conflict and no departure: SPLIT-9 must hold either way.
  - Same rung of the ladder; precedent (Andrej, issue 1 (B)) and LEAK-41's selection clause favour (ii). Both sides now prefer (ii).
  - The curator marks it, because it reopens issue 1's key.
- **Issue 7, B against C.**
  - A real conflict only if LEAK-41's sentence is a directive. By rank (rule text over the Mechanisms row) it is, and B then breaks a Must.
  - C meets everything, so there is no conflict under C.
  - Recommend C. B needs an amendment, after which the choice is a weighing call for the curator.
- **LEAK-9 figure and the link route.** Agreed in the rebuttals (change 1). Corrected here: the link needs `Exposure`, a scoring column.
- **"Ceiling."** Agreed: reword the dataset texts now (change 2); the rule and probe wording is a cross-dataset amendment (issue 3, with X2). The advocate's worry that dropping the word departs from LEAK-41 does not hold: the Must's operative duty, stating the score of 1/weight alone, is still met.
- **Recording gaps.** Agreed (change 3, issue 4).

**Task gamer exploits, mapped** (the gamer's honest Tweedie is 0.2025, the definition's 0.183, different settings):

| # | Exploit | Rule | Definition note | Gain: measured against noted | Status |
|---|---|---|---|---|---|
| 1, 1b, 1c, 1d, 4 | Successor deltas and the no-model rule | LEAK-9 (protocol line) | "Potential leak, kept on purpose (LEAK-9)", line 188: +0.260 | +0.364 to +0.437 measured | Known, figure understated: an issue, fixed by change 1 |
| 2, 3, 3b, 3c | ends_early flag, `Exposure` as a feature, 1/E rule, -E alone | LEAK-41, MET-15 (`feature_columns` excludes it) | Line 186: +0.073 and 0.184 | +0.082 to +0.088 (within probe 22's SD of 0.017); 3c 0.1837 equals the note | Known, no issue. Reading `scoring.parquet` is a protocol breach for every exposure dataset |
| Flaw | log1p scale hurts L2 (0.141 against 0.203) | CLEAN-16 | Issue 7 | Matches | Known, open: issue 2 |

- The gamer's fix (one row per policy-year) is rejected by both sides. No rule requires it, and the practitioner says the earned-exposure segments are the unit a pricing GLM is fitted on.
- Finding A is not among the gamer's exploits (it is a training-side route); it is new from the split auditor.
- The accepted warning (`task_target_value_dominant`) is not touched.

**6. Consistency with precedent**

- D9 is consistent with fremtpl2, bemtpl97, australian (D8), pricing_game_2016 (D11) and spanish (D10). Its reversal of Andrej's issue 4 names the fact that changed (the constant scored 0.184 then, 0 now). No prompt needed.
- The unrounded length departs from Andrej's 2026-11-02 rounding with a stated fact, and is consistent with pricing_game_2016 and spanish. It needs Lennart's mark (issue 4).
- Widening the key (finding A) follows Andrej's issue 1 (B) of 2026-11-03.
- Issue 7: A has no fact that sets it apart; C follows pricing_game_2016; B has no precedent. The register shows no flags on LEAK-41, MET-14/15/16 or CLEAN-16, no drift, and no third exception.
- Reflection prompt for issue 7 (from the precedent checker, to append):

**Consistency check (AI, 2026-11-06):** Does anything set frempl apart from CLEAN-16's clause on log-scale rates, or should it go like pricing_game_2016_french_fleet (identity scale, start-known length kept)?

| | Option | Pro | Con |
|---|---|---|---|
| a | Exception to CLEAN-16 (keep A) | Keeps a legitimate input and the log1p scale | No fact sets frempl apart; L2 loses 0.029 for a reason unrelated to risk |
| b | Drop the column (B) | L2 and Tweedie score alike (0.185, 0.179); scale kept | Breaks LEAK-41's "a part known at the start ships as its own column" unless amended; reverses D9's "stays a feature" |
| c | Identity scale, column kept (C) | Meets CLEAN-16, LEAK-41 and USE-6; matches pricing_game_2016 | L2 scores 0.159, driven by the tail; changes the per-table scale of 2026-11-02 |
| d | Amend CLEAN-16 or LEAK-41 to say which wins | Settles this table and the next alike | A rule change prompted by one case |

Recommendation: c, or d followed by b if the log1p scale matters more than the sibling match. Decision: a, b, c or d?

</details>

<details><summary>Claim audit</summary>

**Claim audit: frempl_french_motor_personal_line (full tier, exposure re-review 2026-11-06)**

Verdict: ship as is on validity. Every claim of today's change (D9) that I tested holds on the data. One claim is
refuted, a wording claim repeated in five places: "1/Exposure alone, the ceiling a leak would reach". Issue 7
(CLEAN-16) is confirmed as an open Should-level conflict. No Must-level claim is refuted.

Setup: the definition's container (load_definition(...).to_container()), scored with
data_foundry.v2.metrics.scorer, features from feature_columns(c), splits as shipped (3x3). LightGBM ran with the
exposure study's PARAMS (400 trees, lr 0.03, min_child_samples 200, subsample/colsample 0.8), Tweedie power 1.5,
weighted by Exposure, ONE seed (the definition used 3).

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Target = log1p(ClaimAmount/Exposure); _clean rebuilds the amount | dataset.py _clean step 7, notes "Target" bullet, CHANGES | inverted the container's target: expm1(y)*Exposure; re-ran _clean | HOLDS | the assert passes; total 22,586,967; max rate 11,617,306/yr (amount 58,087, Exposure 0.005 = 1.8 days) | MET-14 |
| 2 | Exposure is the weight scoring column, the metric's weight input and the sample_weight, never a feature | dataset.py metric/scoring_columns/sample_weight, CHANGES | task_metadata; sample_weight(c); feature_columns(c) | HOLDS | inputs={'weight':'Exposure'}, sample_weight='Exposure', 16 features, no Exposure, no exposure_at_start, policy_component not a feature | MET-15, MET-2, LEAK-41 |
| 3 | exposure_at_start dropped | CHANGES, notes | columns of the container | HOLDS | not among the 19 columns | LEAK-41 |
| 4 | length_to_year_end is known at the start: one value per start day, >= Exposure, = Exposure on open records, unrounded | _clean step 6, notes, CHANGES | raw files: nunique of open records' Exposure per start day; compare with (2005-01-01 - start)/365 | HOLDS | 0 of 366 start days have two open Exposure values; L >= E on all rows, L = E on 48.4%; max \|L - calendar days/365\| 0.006 (the source's own Exposure precision); 366 values at 3 decimals (the source's precision, not month-rounded) | USE-6, CLEAN-22, LEAK-41 |
| 5 | Every Exposure is positive, 0.001 to 1; no row goes under USE-7 | notes, scoring_columns | min/max | HOLDS | 0.001 to 1.0, none <= 0 | USE-7, MET-2 |
| 6 | The per_unit Gini is the CAS ordered-Lorenz Gini: rows sorted by predicted rate, x = cumulative exposure, y = cumulative loss | metric reason, metrics.py | independent 1 - 2*AUC (sklearn Tweedie-example form, ties grouped) against the scorer on 45 random predictions over the 9 folds; perfect and 1/E predictions | HOLDS | max abs difference 4.1e-12; perfect 0.9630 both; 1/E 0.1837 both; the scorer inverts y_true through target_transform | MET-3, MET-13 |
| 7 | A weighted constant scores exactly 0 | metric reason, CHANGES | constant prediction on 9 folds | HOLDS | 0.0000 on every fold | MET-13 |
| 8 | Random orders score 0.003 on average (SD 0.039) | metric reason | 20 random predictions per fold | HOLDS | mean 0.0024, mean per-fold SD 0.037 (0.020 to 0.071) | EV-2 |
| 9 | MET-2 computable: each test fold holds what the metric reads | (implied) | units per fold | HOLDS | 38,281-38,532 test rows, 3,570-3,675 claims per fold; 0 groups shared between train and test on 9 of 9 splits | MET-2, SPLIT-9 |
| 10 | Honest Tweedie LightGBM scores 0.183 (0.149 to 0.237) | CHANGES, metric reason, notes, REVIEW 6 | refit, 1 seed | HOLDS | 0.182 (0.145 to 0.244) | EV-8 |
| 11 | Squared error on log1p scores 0.156 | same | refit | HOLDS within seed noise | 0.152 | EV-8 |
| 12 | 1/Exposure alone scores 0.184 (0.130 to 0.263), above the Tweedie model on 4 of 9 | same | scorer on log1p(1/E) | HOLDS | 0.1837 (0.1305 to 0.2629), above Tweedie on 4 of 9 | LEAK-41 |
| 13 | 1/Exposure is "the ceiling a leak would reach" / "the ceiling of a proxy" | metric reason, notes "metric rewards any stand-in" bullet, REVIEW summary, CHANGES ("the ceiling"), probe 22 output | Tweedie with Exposure as a feature | REFUTED | with the realized length as a feature: 0.259 (mine, +0.077, 9 of 9), 0.256 (the definition's own number, +0.073), 0.240 against 1/E's 0.183 in probe22_actuarial.txt. A proxy combined with the features goes 0.07 past the "ceiling" | EV-2 (wording); LEAK-41's own phrasing |
| 14 | Exposure as a feature lifts Tweedie by +0.073 on 9 of 9 | CHANGES, notes, REVIEW 6 | refit | HOLDS | +0.077 (SE 0.007), 9 of 9 | LEAK-41 |
| 15 | 1/E above the L2 fit on 6 of 9 splits | notes bullet | per fold | NOT REPRODUCED (seed noise) | 8 of 9 with one seed; the mean claim (0.156 < 0.184) holds | EV-2 |
| 16 | Ignoring the weight costs Tweedie 0.023 (9 of 9) and L2 on log1p nothing | notes "learners" bullet | unweighted refits | HOLDS | Tweedie -0.0225 (SE 0.003), 9 of 9; L2 weighted - unweighted -0.004 (weighted higher on 3 of 9) | MET-15 |
| 17 | Probe 22: features predict Exposure at R^2 0.34, 86% through length_to_year_end; none above noise | CHANGES, notes, probe22*.txt | cross-fitted LightGBM E ~ features on split (0,0), with and without L; mediation of L under Tweedie with and without E on 9 splits | HOLDS | R^2 0.336 with all features, 0.003 without L (the rest of the tariff has no selection proxy of the length); mediated gain of L = -0.035 (SD 0.019), negative on 9 of 9 (L gains MORE when E is present, as L - E marks a cut record: an interaction with the leak, not a proxy of it); probe22_actuarial.txt: -0.038 (SD 0.019) | LEAK-41, USE-6 |
| 18 | Issue 7: L2 on log1p scores 0.156 with L, 0.185 without (lower with it on 7 of 9); Tweedie 0.183 with, 0.179 without | CHANGES, notes, REVIEW 7 | refits | HOLDS | L2 0.152 vs 0.182 (-0.030, SE 0.011, lower with L on 7 of 9); Tweedie 0.182 vs 0.178 (+0.004, SE 0.005, higher on 6 of 9) | CLEAN-16 |
| 19 | The weighted mean of log1p rises with the length to 31 December while the cost per year stays flat | notes "learners" bullet, REVIEW 7 | raw data by L band | HOLDS | weighted mean log1p 0.289 / 0.636 / 0.881 / 1.013 for L in quarters; cost per year 394 / 469 / 451 / 441; claims per year 0.20 to 0.22 | CLEAN-16 |
| 20 | The next record of the policy as an oracle: 0.443 (+0.260) | CHANGES, notes LEAK-9 bullet, REVIEW 6 | Tweedie with has_next, the next record's counter rises and the realized length from the next start | HOLDS | 0.467 (+0.285, 9 of 9; min 0.427) | LEAK-9 |
| 21 | The length to 31 December alone scores 0.005; models beat it by at least 0.11 on 9 of 9 | notes, REVIEW summary | per fold | HOLDS | L alone 0.0052; Tweedie margin min 0.140, 9 of 9 | TP-4 |
| 22 | Records: 55,700 open, 34,324 continued, 25,131 ended alone; ended-alone 20.7% of exposure, 38.9% of cost; 837 / 407 / 311 per exposure-year; 66 of the 109 largest claims | notes "Exposure" bullet, REVIEW 6 | recomputed from raw with _continues_next | HOLDS | exact: 55,700 / 34,324 / 25,131; 20.7% / 38.9%; 836.9 / 407.0 / 310.6; 66 | EV-2 |
| 23 | 45 exact copies dropped, 967 negatives set to 0; 90.6% zeros (89.7% published + 0.84%) | notes, task_summary | raw | HOLDS | 45; 967; 0.9056 and 0.8972 | EV-2 |
| 24 | 15,303 records shorter than a month hold 4.3% of the claim cost | notes | raw | HOLDS | 15,303; 4.32% | EV-2 |
| 25 | 38% of records start on 1 January | notes | raw | HOLDS | 38.2% | EV-2 |
| 26 | MET-1/MET-11: the source names no metric, origin context | metric reason | the CASdatasets freMPL page once more; one web search for a freMPL paper | HOLDS | the page has descriptions and plotting examples only; no paper scoring freMPL found (Gini on ordered Lorenz curves appears on freMTPL/BelgianMTPL, arXiv 2412.14916). The x axis of cumulative exposure with ordering by predicted pure premium matches the CAS validation practice | MET-1, MET-11 |
| 27 | "CAS Monograph 5, sec. 7.2.4" | metric reason | look up the section | UNTESTED | the monograph PDF was not reached in one search; the form itself is confirmed (claim 6) | EV-2 |
| 28 | MET-15 applies: the decision's quantity is a sum over the realized length (premium earned pro rata) | metric reason, notes | reading | HOLDS (reasoning) | a per-year tariff earned pro rata on a cancelled policy; the sample weight equals the metric's weight | MET-15 |
| 29 | "Rounded, 2,704 records would repeat ... (3,445 in all, against 610)", "score would not move (-0.002 / -0.001)" | notes length bullet | not run | UNTESTED | a supporting figure for the unrounded choice; claim 4 already shows the unrounded L is a per-day calendar value with no realized decimals, so the choice is safe whatever these counts are | LEAK-41 |
| 30 | (implied) No row copies across the split | leak.txt | probe output | HOLDS | 0.4% of test rows have an exact feature copy in train; same label 0.3%, another label 0.1% | LEAK-18 |

**Ranked: refuted and untested**

1. (Refuted, wording, EV-2; no validity effect) "1/Exposure alone ... the ceiling a leak would reach". Where:
   metric reason (dataset.py, README Metric block), the notes bullet "The metric rewards any stand-in", the REVIEW
   summary, CHANGES.md, the probe 22 output line "1/weight alone, the ceiling of a proxy", and LEAK-41 /
   probe-22 text in leak_checks.md. Numbers: the realized length as a feature reaches 0.259 (mine), 0.256 (the
   definition's own), 0.240 (probe22_actuarial) against 0.184. The single variable 1/E is a floor for a perfect proxy
   used together with the features, not a ceiling. What it changes: nothing in the decision (LEAK-41 decides by
   timing), but a reader who takes 0.184 as a bound would let a partial proxy that scores 0.20 through as "below the
   leak ceiling". Mildest remedy: reword to "1/Exposure alone scores 0.184, as much as the honest model; with the
   features it reaches 0.256" in the dataset's texts. The rule and probe wording are the curator's (shared with
   australian_vehicle_insurance and others), so flag them and do not edit them here.

2. (Confirmed open conflict, CLEAN-16 Should; issue 7) The shipped state keeps both the log1p scale and
   length_to_year_end, which CLEAN-16 as amended asks against ("drop the feature or ship the identity scale"). Measured:
   -0.030 (SE 0.011) for a weighted L2 fit on log1p, lower on 7 of 9; +0.004 (SE 0.005) for Tweedie. Strictly CLEAN-16
   names the "denominator as a feature". L is not the denominator, but it equals it on 48% of rows and bounds it on
   the rest, and the mechanism (weighted mean of log1p rising with L, flat cost per year) is the one the rule describes.
   What it changes: the most common learner family loses about one random-order SD (0.037) for a reason unrelated to
   risk. Mildest remedy: option B of issue 7 (drop L), which the agent recommends; the data supports it.

3. (Not reproduced, seed noise) "1/E above the L2 fit on 6 of 9": 8 of 9 with one seed. The mean holds. Remedy: none
   needed, or state the count as "6 to 8 of 9 by seed".

4. (Untested) The CAS Monograph 5 section number; the rounding counts 2,704 / 3,445 and the -0.002 / -0.001 deltas.
   Neither changes a decision.

Other observations (not claims the definition makes, for the panel):
- Fold noise: random orders have a per-fold SD of 0.037 (up to 0.071), the Tweedie-L2 gap is 0.030, and 1/E per fold
  ranges 0.13 to 0.26. Model comparisons on this task need paired fold differences. The REVIEW already lists "fold
  noise (SD 0.03)" as a minus.
- The task probe's flag no_signal (TP-1, TP-2) comes from R^2 skill on the log1p scale (+0.014). On the declared metric
  the models beat the constant by 0.18 and the length alone by at least 0.14 on 9 of 9 (TP-4), so the flag measures
  the scale, not the absence of a ranking signal.
- Without length_to_year_end, the tariff predicts the realized length at R^2 0.003: no rating factor carries risk
  selection into the length. The LEAK-41 timing call for L is clean.
- The README guidance "a model fitted without [the weight] targets another quantity" holds in principle. Empirically
  it matters for Tweedie (-0.023, 9 of 9) and not for L2 on log1p (-0.004 the other way).
- The container rows are not in _clean's order. I aligned them through a key merge over every column (the assert on a
  complete match passed, and the oracle's 0.47 confirms the alignment). The probes that read raw order go through
  lineage and are unaffected.

Sources checked: https://dutangc.github.io/CASdatasets/reference/freMPL.html ; https://arxiv.org/pdf/2412.14916 ;
https://open-exam-prep.com/study-guides/cas-pcpa/ch07-validation/gini-roc-auc

</details>

<details><summary>Column audit</summary>

**Column audit (2026-11-06, exposure re-review, full tier): frempl_french_motor_personal_line**

Verdict: ship as defined. No leak and no cleaning problem is new under LEAK-41. `length_to_year_end` is known at the
start and holds no part of the realized length. The only open point is issue 7 (CLEAN-16). Both arms of probe 22
show the feature is worth nothing on the declared metric, and that evidence supports option B, dropping it.

Read: the definition and its REVIEW.md (issues 6, 7; column audit of 2026-11-01),
the change note, leak_checks.md (LEAK-41, probe 22, cases), cleaning_features.md (CLEAN-12, -14, -16, -22), use_case.md
(USE-6, -7). Frame: the definition's own _load_raw/_clean on the warehouse CSVs, 115,155 x 21 (with the raw dates kept
next to it for the checks). dataset_io.load confirms 16 features, weight `Exposure`, scoring column `Exposure`, group
`policy_component`.
Probes read: probe 22 (the L2 arm and the weighted Tweedie arm), the leak, task and group probes.

**1. length_to_year_end: the question asked (LEAK-41 timing, its decimals)**
Known at the start: yes. It depends on the start date alone.
- _clean takes it as the median `Exposure` of the open records (RecordEnd missing) that start on the same day.
  All 366 start days of 2004 have open records. On none of the 366 days do the open records disagree: every day has
  exactly one distinct open `Exposure`, so the median is that value, and the frame holds one value per start day
  (max distinct per day 1; 366 values over 366 days).
- It falls strictly with the start date (0 inversions over the 366 days, 0.001 on 31 Dec to 1.0 on 1 Jan). It is the
  source's own rounding of the time left to 31 December. Neither (days-1)/365 nor days/366 reproduces it exactly
  (50% and 44% of rows match to 3 decimals), so the lookup from the source is the right way to build it, not a formula.
- Since the value is fixed by the start day, it carries no information about the realized length beyond the start date
  itself. Its three decimals are the start date's, not the record's end. It equals `Exposure` on all 55,700 open
  records and is strictly above it on all 59,455 closed records (0 ties). That says the end is at or before 31 Dec,
  which is known at the start. No value is "corrected on some rows and realized on others" (LEAK-41's hybrid), and
  no precision marks the cut. Unrounded is right: the month rounding of 2026-11-02 guarded the old `Exposure`
  feature's decimals, and this column has no such decimals to hide. Rounded, it would only merge known start days.
- The lookup reads the open records' `Exposure` over all rows, test rows included. Every day has one shared value,
  so the lookup is a fixed calendar table and moves no label information. This is not a leak (EV note only).
- Probe 22 (3 splits x 3 seeds, capped at 50k):
  - The features predict `Exposure` at R^2 0.335 (Spearman 0.536), 86% of the gain through length_to_year_end. That
    is expected of a feature that equals the weight on 48% of rows and bounds it on the rest.
  - Its weight-mediated gain is negative in both arms: -0.060 (SD 0.034) under L2 on log1p and -0.038 (SD 0.019)
    under the weighted Tweedie fit. The feature stands in for nothing the weight would add.
  - Its gain without the weight is -0.038 (SD 0.040) under L2 and -0.002 (SD 0.014) under Tweedie.
  - Its gain with the weight present is +0.022 under L2 and +0.036 under Tweedie. That is the open/closed status that
    `Exposure` < length_to_year_end reveals, and it only exists while the weight is a feature, which it is not.
  - The other top features (LicAge, DrivAge, BonusMalus, SocioCateg) are all within one SD of 0 in both arms.
  Verdict: fine under LEAK-41 and LEAK-10 (timing: known at the start, USE-6). LEAK-41's "worse of the two fits" test
  is for suspect columns. This one is not a suspect by timing. Its value question is CLEAN-16 (issue 7, below).
- A small wording point for the definition: length_to_year_end is a one-to-one recoding of RecordBeg (366 values for
  366 days). `changes` says "dropped the record dates", and the `known` field says "the time from the period's start
  to 31 December". Both are true, but a reader should be told that the start date ships in this form. Suggested
  addition to the length bullet: "a one-to-one recoding of the start date (366 values)". The 2026-11-01 audit found
  that RecordBeg adds nothing on top of the corrected length (Gini 0.335 against 0.340), so nothing changes in value.

**2. Exposure (the weight)**
Realized length in years, 0.001 to 1.0, positive on every row (USE-7: none to drop). It is excluded from the features
(confirmed in dataset_io's feature_cols), it is the metric's `weight` input with per_unit, and it is `sample_weight`.
Verdict: correct under LEAK-41, MET-14 and MET-15.
- Leak reference: as a feature it would add +0.079 (SD 0.017) under Tweedie, and 1/Exposure alone scores 0.183
  against the honest Tweedie fit's 0.161 in the probe. Those numbers are the ceiling a leak would reach. Nothing
  shipped reaches it.
- Under L2 on log1p, Exposure as a feature lowers the Gini (0.137 to 0.008). That is the CLEAN-16 mechanism again,
  not reassurance.

**Column table**

| Column | Meaning (codebook, man/freMPL.Rd) | Known at prediction (record start)? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `length_to_year_end` | time from the record's start to 31 Dec 2004 in years, the source's Exposure of open records starting that day | yes: a function of the start date only (one value per day, strictly monotone) | float64, 0.001-1.0, unrounded, no missing | fine (timing); keep or drop is issue 7 | USE-6, LEAK-41 (holds), CLEAN-16 (open) |
| `LicAge` | driving licence age in months | yes (grows by the elapsed months between records) | int, 2-940; 47 implausible early licences kept with a note | fine | CLEAN-11 (settled) |
| `Gender` | Male / Female | yes (profile) | category, 2 | fine (ethics note present) | CLEAN-14 |
| `MariStat` | Alone / Other | yes | category, 2 | fine | CLEAN-14 |
| `SocioCateg` | CSP code (socio-professional category) | yes | category, 46 levels, 23 with < 10 records (several singletons) | fine | CLEAN-14, CLEAN-8 |
| `VehUsage` | 4 vehicle usages | yes | category, 4 | fine | CLEAN-14 |
| `DrivAge` | driver age in years | yes (age at start; +1 at 37% of continuations) | int, 20-99 | fine |  |
| `HasKmLimit` | 1 if the policy has a km limit | yes (contract term) | category {0, 1}, 0/1 only (12,660 ones) | fine | CLEAN-14 (yes/no flag) |
| `ClaimNbResp` | at-fault claims in the 4 preceding years | yes (rises after the record's claim, not before) | int 0-5 | fine | LEAK-10 holds |
| `ClaimNbNonResp` | not-at-fault claims, 4 preceding years | yes | int 0-7 | fine | LEAK-10 holds |
| `ClaimNbParking` | parking claims, 4 preceding years | yes | int 0-5 | fine | LEAK-10 holds |
| `ClaimNbFireTheft` | fire-theft claims, 4 preceding years | yes | int 0-4 | fine | LEAK-10 holds |
| `ClaimNbWindscreen` | windscreen claims, 4 preceding years | yes | int 0-8 | fine | LEAK-10 holds |
| `OutUseNb` | out-of-use periods, 4 preceding years (what one is: unknown) | yes | int 0-5 | fine |  |
| `RiskArea` | "Unknown risk area between 1 and 13, possibly ordered" | yes (profile) | int 1-13 kept numeric; codes have no words, so CLEAN-12 keeps them as shipped | fine (the minor question of 2026-11-01 was not raised by the mediator; not reopened) | CLEAN-12, CLEAN-14 |
| `BonusMalus` | bonus-malus 50-350, < 100 bonus | yes, see below | int 50-195 | fine | LEAK-10 holds (checked again against the fremtpl2 case of 2026-11-05) |
| `Exposure` | realized length in years | no: cut by contract changes and ends, which claims drive | float 0.001-1; weight scoring column and sample_weight, not a feature | fine as wired | LEAK-41, MET-14, MET-15 |
| `policy_component` | group: connected records of one policy | n/a (group column, not a feature) | int32 | fine | SPLIT-9, SPLIT-24 |
| `log1p_claim_amount_per_year` (target) | log1p(ClaimAmount / Exposure), negatives clipped to 0 | target | float 0-16.27 (11.6 M per year at most); round-trip checked in _clean | fine; scale question is issue 7 | MET-14, CLEAN-16 |
| `ClaimAmount`, `ClaimInd` (dropped) | the period's amount and its indicator | no: parts of the target | dropped | fine | LEAK-10 |
| `RecordEnd` (dropped) | end date | no: post-outcome | dropped | fine | LEAK-10, LEAK-41 |
| `RecordBeg` (dropped) | start date | yes | dropped; ships one-to-one as length_to_year_end | fine (note wording, problem 2) | CLEAN-22 |
| `file` (dropped) | sample file | n/a | dropped | fine | (settled) |
| `exposure_at_start` (dropped since 2026-11-06) | the old hybrid base | partly realized | dropped | fine | LEAK-41 |

BonusMalus against the fremtpl2 case (new LEAK-10 Cases row, 2026-11-05). There, BonusMalus was recorded after the
outcome in some ID blocks, with claimants piling up on the first malus step. That pattern is absent here:
- Only 9 of 115,083 records with no at-fault claim in the 4 preceding years carry BM > 100 (7.8e-5), against 8.1%
  of the records with one. A malus therefore follows prior at-fault claims, which places the value at the start.
- The claim rate rises smoothly with BM: 0.086 at 50, 0.11 at 100, 0.12-0.14 at 101-125, 0.16 above 125. Claimants
  do not pile up on a step.
- The 2026-11-01 audit found that BM rises at the next record after 11.6% of the claims (2.4% otherwise).
Kept: the source registers it at the start, as for bemtpl97.

Dtype probe: 0 of 16 columns flagged. There is no codebook file, so
the meanings above come from man/freMPL.Rd as cited in the definition. No count or measured quantity is typed
categorical, and no code is typed numeric except RiskArea, which is deliberate. There is no ordinal column, and no
missing values in any feature.

**Problems, ranked (principles.md)**
1. Issue 7, open (CLEAN-16, Should; value, not validity). Keep length_to_year_end on the log1p scale? New evidence
   from probe 22, 3 splits x 3 seeds, with the weight not a feature:
   - weighted Tweedie arm: the feature's gain is -0.002 (SD 0.014);
   - L2-on-log1p arm: its gain is -0.038 (SD 0.040).
   On the definition's 9 splits it was +0.005 (SE 0.004) under Tweedie and -0.029 (SE 0.010) under L2.
   - No arm shows the feature is worth anything to the loss that suits the metric. Under the common loss it is a
     penalty unrelated to risk: CLEAN-16's mechanism, with the start-known length in the place of the denominator.
   - LEAK-41's "decide on the worse of the two fits" does not formally apply, because the column is not a suspect by
     timing. But the same reading leads to the same answer.
   - Mildest remedy: option B as issue 7 describes it. Drop the feature in _clean, keep the asserts, and update
     known, changes, the length bullet, the learners bullet and the metric reason's numbers. USE-6 makes the column
     legitimate, not obligatory, and CLEAN-16 names dropping it as one of its two remedies.
   - If the curator keeps it (A), the learners bullet already says what an L2 fit estimates. Nothing else is needed.
2. Text only (EV, CLEAN-22): say that length_to_year_end is a one-to-one recoding of the start date (366 values),
   because `changes` reads "dropped the record dates". One clause in the length bullet; moot under issue 7 option B.
No other problem. Settled points (the grouped folds, the negatives, the 45 copies, the LEAK-9 protocol line, the
counters' timing) are not reopened by today's change.

</details>

<details><summary>Split audit</summary>

**Split audit: frempl_french_motor_personal_line (exposure re-review, full tier, 2026-11-06)**
Verdict: RIGHT WITH NOTES. The forced grouped regime and the component key stand. One new finding: a hidden group the
key misses. A contract change that also changes one profile column (a move to another RiskArea, a km limit or vehicle use
changed) leaves the policy split across components, and its later record in training gives a test record's claim away
(+0.020 Gini, 9/9 splits). The LEAK-9 protocol line is right, and the route it guards is larger than its stated number.

Untuned LightGBM, Tweedie
1.5, 300 trees, weighted by Exposure, one seed; scored with scorer(c) on log1p(pred). Rows are mapped to the raw dates
through process(lineage=True) ("traced by the column", target matches).

1. Regime (SPLIT-8): holds, and is now also required by LEAK-41.
   - The use case is a tariff applied at the start of a period to next year's policies, so it is temporal by nature.
     Every record lies inside 2004 (starts 2004-01-01 to 2004-12-31), and 48.4% are open at 31 Dec.
   - An in-year window could only train on records that had already ended by its cutoff:

     | Cutoff | Rows ended by then | Claim rate of those rows | Cost per year, those rows / open records |
     |---|---|---|---|
     | 1 Apr | 12.8% | 4.4% | 1,140 / 311 |
     | 1 Jul | 26.9% | 6.5% | 720 / 311 |
     | 1 Oct | 39.1% | 8.1% | 631 / 311 |

     That training side is chosen by the realized weight. LEAK-41's last clause forbids it, as in the
     pricing_game_2016_french_fleet case, and it is also below the 50% floor.
   - The weight (time on risk) is cut at the release end (31 Dec) for 48.4% of the records. The grouped random folds
     put that cut on both sides alike. ForcedGroupedFromTemporal is right.
   - Not new, and should stay in the notes: held-out policies of the same year cannot test drift to the next tariff
     year (fit=approximate already says so).

2. Group id (SPLIT-24, SPLIT-9): checked.
   - 68,857 components; 1 to 13 records each; 85,124 records in components of two or more.
   - No component straddles any of the 9 splits. Test folds hold 38,281 to 38,532 rows.
   - One prediction = one row, made from that row (context none).
   - The group probe: IID 0.006 vs grouped 0.008, so a row-wise model gains nothing from IID. That probe cannot see a
     lookup route; see finding A.

**Findings, ranked (all P4)**

A. [P4, SPLIT-9 Must, with SPLIT-30/SPLIT-24] Hidden successors that change one profile column fall outside the
   component and cross the split. NEW.
   - What the key requires: all six PROFILE columns equal. But a contract change is often exactly a change of one of
     them.
   - The search: records that end before 31 Dec, matched to a record starting that same day with the same Gender, a
     DrivAge 0 to 1 higher, a LicAge advanced by the months between the starts (within 1), every claim/out-of-use
     counter at least as large, and exactly one of the other five profile columns different.
   - Result: 9,160 such pairs over 7,120 predecessors, none in the same component.
   - Proof that real links are among them (a test that could have refuted it): the successor's counters rise after
     75.5% of the predecessor's claims and after 41.9% of its non-claims.
     - Chance baselines, with the end date shifted by +-1 or 2 months: 0.63-0.67 against 0.62-0.65, no contrast.
     - Pairs with 2 or more profile columns different: no contrast either.
     - By column changed (rise after claims / after non-claims):

       | Changed column | Rise after claims | Rise after non-claims |
       |---|---|---|
       | HasKmLimit | 0.939 | 0.073 (near exact) |
       | VehUsage | 0.863 | 0.311 |
       | RiskArea (5,788 pairs) | 0.722 | 0.494 |
       | SocioCateg | 0.68 | 0.47 |
       | MariStat | 0.72 | 0.46 |

   - Rough count of true links: about 3,200 records (35% of the pairs, from the non-claim rise mixing 0.63 chance
     with 0.025 true).
   - Leak size, on the shipped 9 splits:
     - Setup: a lookup feature, computed only from training rows: the largest counter rise among the test record's
       one-column-changed candidate successors in train. 1,609 to 1,705 test rows per fold (about 4.4%) have such a
       candidate.
     - Result: honest 0.1742 against lookup 0.1945, a gain of +0.0203 (SD 0.0100), better on 9 of 9 splits.
     - Where the gain comes from: the flag "a candidate exists" alone gives -0.003 (3/9). So the gain is the claim
       told by the later record's counters, not the early end.
   - The same alternative under widened groups: the component graph plus these links gives 61,091 groups, the largest
     90 records.
     - The lookup gain falls to -0.0045 (SD 0.009, 4/9).
     - The honest score is 0.1686 (SD 0.020) against 0.1742 on the shipped folds. These folds differ, so the
       comparison is unpaired; the gap is well inside the fold SD of about 0.03.
   - Rule: SPLIT-9 says a training row of the test row's own entity, set after its prediction point, that tells its
     outcome is removed whatever it costs. This is the same path issue 1 closed for exact-profile links, at about 1/5
     of its size (issue 1 measured 0.303 to 0.395 on about 20% of test rows).
   - LightGBM reading one row cannot use it. A model that searches the training rows (kNN, retrieval, in-context
     models conditioning on train) could.
   - Remedies, mildest first:
     (i) A per-fold filter. Drop from each training side the rows that are one-column candidate successors of a test
         row of that fold. About 1,700 to 2,500 training rows per fold (about 2-3%); groups unchanged. The splits
         stay index lists, so this is a split edit only.
     (ii) Widen the component with these links, as Andrej's "most conservative key" asked.
         - Exactness: the rule is the current rule with one profile column relaxed, so it is built exactly from the
           data (SPLIT-24).
         - Precision: about half of the RiskArea links are chance. A chance link only merges two policies, the
           stricter side, as the 1% cross-file chance links were accepted. The largest group grows to 90 records.
         - Narrower variant: restrict the relaxation to HasKmLimit and VehUsage changes (2,049 pairs), the near-exact
           links. This closes only part of the route.
     Recommend (ii) with all one-column links (it fits the 2026-11-03 "most conservative" call and the measured cost
     is within noise). Otherwise use (i). Either needs the curator's mark, since it reopens issue 1's key.

B. [P4, LEAK-9 Should] The protocol line for the successor route: right, and its number should be stated as a floor.
   - Grouping puts a test record's later records in test. 44,999 records have an in-component successor; issue 1 fixed
     that route on the training side.
   - My oracle uses the in-component successor's counter rise plus the days to its start, i.e. the realized length.
     - Result: honest 0.1742 against oracle 0.529, a gain of +0.355 (SD 0.015), 9 of 9.
     - The CHANGES/notes figure (+0.260) uses the next record of the file only. Both say the same thing; the larger
       one is what a method reading other test rows could get, about 3x the honest score.
   - The mildest remedy stays the protocol line: each test record is predicted from the training rows and its own row
     only, and a method that reads other test rows is called out and not benchmarked. Precedents: fremtpl2,
     medical_facility_operational_data, sepsis.
   - The re-split alternative is not milder. Keeping one record per component in test would drop about 15,000 test
     rows per fold and select rows by contract changes, which correlate with claims and with the realized length
     (LEAK-41).
   - Note: models that predict each test row independently given train (GBMs, TabPFN in its usual batch) are not
     affected.
   - Suggested wording: "+0.26 to +0.36 depending on what is read". After finding A's fix, the line also covers the
     one-column successors, which would then be test rows.

C. [P4, SPLIT-8, note] Time on risk cut at the release end: no split problem.
   - The cut is the same on both sides.
   - It enters only through `length_to_year_end`: equal to Exposure on the 48.4% open records, an upper bound on the
     others. That is a feature question (issue 7, CLEAN-16/LEAK-41 timing), not a split one.
   - Every record has Exposure > 0, so every test fold is fully scored.

D. [P4, copies across the split, note] Fine.
   - 0.39% to 0.46% of each test fold has an exact feature copy in train.
   - Leak probe: same label 0.3%, another label 0.1%; 1-NN R^2 is negative. Natural repeats (LEAK-18), already
     documented.

Not re-opened: issue 1 (the component key, apart from finding A), the 45 exact copies, the file stacking.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (2026-11-06, exposure re-review, full tier): frempl_french_motor_personal_line**
Played as: the pricing actuary of a French private motor insurer, building the pure-premium (prime pure) model of a
personal-line tariff from a year of earned-exposure records.

**Verdict**
Fit: approximate (USE-8), unchanged. The rows are the rated exposure segments I fit a tariff on, the target is the
pure premium per earned year and the weight is the earned exposure, but the tariff is thin (no vehicle, cover or
deductible factors), the amount's guarantee and basis are unknown, and held-out policies of the same year stand in
for next year's book.
Metric scores my decision: partly. The exposure-weighted ordered Lorenz Gini on the cost per year is the lift
measure I would use to rank segmentations (Frees, Meyers and Cummings 2011), at my unit (the earned year) with my
weight. It ignores calibration, and one large claim moves it by about 0.06 on a fold. I would keep it (the Tweedie
deviance I would normally add fails here, see Q5) and score it on losses capped at a large-loss threshold.
Issue 7: from the pricing side I support B (drop `length_to_year_end`). It is a cut made by the extract's calendar
year, not a rating factor.

**Q1. Do I have these inputs when a period of cover starts?**
- Driver age, licence age, gender, marital status, socio-professional category, vehicle use, km limit, bonus-malus
  (the French CRM, 50 to 350), risk area, and the claim and out-of-use counts of the four preceding years: yes, all
  on the policy file at the start or amendment of cover (USE-3, USE-6). The counters update at each record's start
  (95% rise after a claim, 2.3% otherwise), so they are history I hold. Gender was a legal rating factor in 2004
  (before the EU Test-Achats ruling of 2012), so it is fine for a 2004 book.
- `length_to_year_end`: I know it, because it follows from the start date. But no French tariff rates on the days
  left to 31 December. That boundary comes from the extract's calendar year: 38% of the records start on 1 January
  because the release cuts there, not because anything is priced there. What it really tells me is the kind of
  record (a policy carried into the year, or one that starts mid-year as new business or an amendment). If I want
  that, I want it as a new business / renewal / mid-term amendment flag and a policy tenure. The data supports this:
  the cost per realized year stays at 394 to 469 across its bands, so it carries nearly no risk signal. Under the
  right loss it is worth +0.005 (SE 0.004, 5 of 9 splits), and it costs a squared-error fit on log1p 0.029 (7 of 9).
  Keeping it is legitimate under USE-6, but CLEAN-16 as amended names exactly this case (drop it or ship the
  identity scale). As a practitioner I would drop it (issue 7, option B).
- The realized `Exposure` is out of the features (LEAK-41, MET-15). That is correct: at the start I know the planned
  term, not when a total loss or a cancellation will end the cover. Probe 22 confirms nothing reaches it above noise
  (features predict it at R^2 0.34, 86% through `length_to_year_end`, and no feature's gain is mediated by it).
- Missing inputs I would always have (the main gap, ranked first below): the vehicle (class or group, age, power,
  value, fuel; the source has them in freMPL1 to freMPL4 but not in freMPL5 to freMPL9), the cover bought and the
  deductible (DeducType exists only in freMPL3-4), policy tenure, the new business / renewal flag, and a zoning finer
  than 13 unknown risk areas.

**Q2. Is the target what I act on?**
- The claim cost per earned year is the pure premium. It is the number I set the premium from (MET-14 applies, and I
  would ship it the same way). I want a number, the expected cost per year on the original scale, not a class.
- Shipping it on log1p is not my scale. A fit of the mean of log1p(cost per year) is not E[cost per year]. Because
  the Gini is rank-based this does not change the score's meaning (y is scored after the inverse, and the order of
  the predictions is unchanged). It does change which learners look good (issue 7), and it leaves predictions I
  could not use as premiums (A/E 0.003 below). The notes say what such a fit estimates (CLEAN-16), so the scale is
  the curator's call. Any premium I file would come from a Tweedie or frequency-severity model on the identity scale.
- The amount: "Total claim amount of the guarantee" (CASdatasets page), with no guarantee named. The counters show
  windscreen, at-fault, not-at-fault, parking and fire-theft claims all inside it. I price each guarantee separately
  (third-party liability, damage, glass, theft-fire), each with its own frequency and severity. A sum over guarantees
  whose purchase I cannot see means a 0 can stand for "covered, no claim" or "not covered". Paid or incurred, and the
  valuation date, are unknown: 2004 bodily-injury liability claims develop for years (LEAK-24 cannot be verified,
  issue 3, settled). These gaps keep the fit approximate (USE-5, USE-8).
- The negative amounts set to 0 (recourse covered the payment) match how I would net recoveries per period. No gap.

**Q3. Does one row match one decision? Is the test data what I face?**
- A row is a period with fixed rating factors, weighted by its earned length. That is exactly the unit of the
  earned-exposure table a pricing GLM is fitted on. The premium is re-rated at an amendment and charged pro rata, so
  the per-unit weighting is my convention (MET-15). A row matches one rated exposure segment, though not always one
  pricing event: the 1 January starts are calendar cuts.
- I would weight by the realized length: yes. Earned exposure is the weight of a rate model (the compound-Poisson
  convention of MET-14). A record cut short after a total loss is real experience at a high cost per earned year,
  and weighting it by its earned days counts it the way my book earns it. The records ending alone cost 837 per
  realized year, against 311 for the open ones. That is risk I must price, not noise.
- Test data: other policies' periods in the same year, grouped by policy component. That is the right protection for
  my use (a later record's counters give a test record's claim away, SPLIT-9). But I apply a tariff to next year's
  book, with claims inflation and portfolio drift, and one year cannot test that (SPLIT-8, ForcedGroupedFromTemporal,
  settled). New against known entity (USE-10): I price renewals as well as new business, and the history I would
  use for a renewal is already in the four-year counters and the CRM. Grouping by policy costs me nothing real.
- The five files are samples of chosen sizes with claim rates of 7.7% to 10.0% and an undocumented draw. I could not
  say what book the test fold represents.

**Q4. Would I use this model? Trust and distrust**
- As a benchmark of how well a learner ranks risk from a thin French personal-line tariff: yes. The signal is small
  but real (claim AUC about 0.67; an honest Tweedie fit 0.183 against 0.005 for the length alone, 9 of 9 splits,
  TP-4). Severities are not learnable (R^2 about 0 on the claimants), which is typical of motor and believable.
- As a tariff: no. Without vehicle and cover factors it is a partial model, and I could file no premium from it.
- I would trust it more with the vehicle and cover factors, a stated guarantee and valuation date, and losses capped
  at a large-loss threshold (the 802,620 claim is 3.6% of all cost, and the ten largest are 7.6%).
- I would distrust any score that moves with which fold drew the largest claims (fold SD about 0.03 over 9 splits).

**Q5. Does the metric score my decision? (MET-1, MET-6 to MET-9)**
- Unit and weight (MET-1, MET-2): yes. The rows are sorted by the predicted cost per year, x is the cumulative
  earned exposure, y the cumulative losses, and there is no base premium (I have none, so the flat rate is the base).
  A flat rate scores exactly 0, random orders score 0.003, and 1/Exposure, the leak's ceiling, scores 0.184 and is
  kept out by LEAK-41. The unnormalised form suits me: normalising by the perfect order would divide by a number the
  largest claims set.
- Threshold metrics (MET-6, MET-7) do not apply: I set a continuous premium, with no cut-off and no top k (MET-9 does
  not apply either).
- What the Gini misses is calibration. It is consistent only among auto-calibrated predictions (Wuthrich 2023,
  European Actuarial Journal 13:469-477): rank-based, so blind to the level and to the shape of the relativities. I
  measured this on repeat 0 (3 folds; LightGBM 300 trees, lr 0.03, seed 0, weighted by Exposure):

| Fold | Tweedie p=1.5 on rate: Gini, A/E | L2 on log1p: Gini, A/E | L2 on log1p, no length: Gini |
|---|---|---|---|
| 0 | 0.210, 0.69 | 0.185, 0.003 | 0.162 |
| 1 | 0.163, 0.82 | 0.154, 0.004 | 0.207 |
| 2 | 0.139, 0.85 | 0.106, 0.004 | 0.182 |

  A/E is predicted cost over actual cost, weighted. The squared-error fit on log1p predicts about 1/250 of the cost
  level, yet scores the same Gini range. A rebasing would fix the level, but not the distorted relativities that a
  log-mean produces.
- The metric I would add normally fails here. Weighted Tweedie deviance (p=1.5) on the cost per year: the Tweedie
  fit is worse than the flat rate on all 3 folds (132.64 vs 132.56, 121.23 vs 120.86, 117.84 vs 117.56). The tail
  rates (up to 11.6 million per year on records of a few days) swamp it. So I would not switch to a deviance (MET-8's
  proper rule is not usable as the single score of this table). The Gini stays the better single choice, and MET-10
  diversity agrees: fremtpl2 and bemtpl97 already carry the Poisson deviance.
- Large claims: capping each record's loss at 50,000 in scoring only (my script) moves the Tweedie fit's fold-0 Gini
  from 0.210 to 0.147. Folds 1 and 2 move by -0.003 and +0.006. One fold's score is decided by its largest claims. A
  pricing actuary models attritional losses and loads large losses separately (ecretement).
- The metric I would choose: the same `ordered_lorenz_gini` (per_unit, weighted by Exposure) on the cost per year
  with each record's loss capped at a stated large-loss threshold. The cap is a target or scoring choice for the
  curator, measured on the shipped splits first. Failing that, I would keep the declared metric as it is. Answer:
  partly.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. A thin tariff: no vehicle, cover, deductible, tenure or fine zoning (present in freMPL1-4, absent in freMPL5-9).
   The model ranks risk from driver and history factors only. This sets the ceiling of the task (USE-8 approximate).
2. The target is a sum over guarantees whose purchase is unseen, with an unknown basis and valuation date. The zeros
   mix "no claim" and "not covered" (USE-5, issue 3 settled as a note).
3. Same-year held-out policies stand in for next year's book (SPLIT-8, settled). Trend and inflation are untested.
4. Large claims are uncapped. The 802,620 claim (3.6% of cost) can decide a fold, about 0.06 of Gini on fold 0.
5. `length_to_year_end` is a calendar-cut artefact, not a rating factor. It is legitimate (USE-6) but misleads L2
   learners on log1p (CLEAN-16). Issue 7: B.
6. The log1p shipping scale is not the premium scale. It is harmless to the Gini, but it invites learners whose
   predictions could not be premiums (A/E 0.003). Noted per CLEAN-16, the curator's choice.
7. The sample draw of the five files is undocumented (claim rates 7.7% to 10.0%).

**What an expert in the domain would change**
- Drop `length_to_year_end` (issue 7, B). If a record-type signal is wanted, derive a mid-year start flag from
  RecordBeg instead. That is a curator decision, not measured here.
- Measure and consider a large-loss cap on the losses the Gini reads (or on the target), stated in the notes. The
  pricing practice is to cap and load.
- Say in the notes, beside the Gini, that it scores the ranking only and not the premium level (Wuthrich 2023). A
  user who wants a premium refits with a Tweedie or frequency-severity loss on the identity scale and rebalances.
- Keep the realized-exposure weight, the per-unit rate and the LEAK-41 exclusion as decided (issue 6). These are the
  actuarial convention.
- Optional, for the fit: a sibling built from freMPL1-4 with the vehicle factors would mirror a real tariff more
  closely, but freMPL1 overlaps 39% with freMPL5-9 (record notes). That is out of scope here.

**Rules cited**
USE-3, USE-5, USE-6, USE-8, USE-10; MET-1, MET-2, MET-6, MET-7, MET-8, MET-9, MET-10, MET-14, MET-15; CLEAN-16;
LEAK-24, LEAK-41; SPLIT-8, SPLIT-9; TP-4.

**Sources**
- Dataset: the definition, its README.md and REVIEW.md, the change note and the probes (probe 22 in its weighted
  Tweedie arm, the leak and task probes).
- CASdatasets freMPL page: https://dutangc.github.io/CASdatasets/reference/freMPL.html (variables by file, "Total
  claim amount of the guarantee", year 2004, unknown insurer, no sampling description).
- Frees, Meyers, Cummings (2011), "Summarizing insurance scores using a Gini index", JASA 106:1085-1098 (as cited in
  the metric reason).
- Wuthrich (2023), "Model selection with Gini indices under auto-calibration", European Actuarial Journal 13:469-477,
  https://arxiv.org/abs/2207.14372.
- My measurement: 3 folds of repeat 0, one seed; indicative, not the 9-split protocol.

</details>

<details><summary>Blind review</summary>

**Blind review: freMPL French motor personal line (clean room task)**

VERDICT: Include with changes. The data is real, cleanly prepared and grouped by policy, but the target log1p(ClaimAmount/Exposure),
fitted and scored with Exposure as the weight, does not stay the same as exposure changes. Most of the little signal it has comes from
exposure leaking in through length_to_year_end. Reformulate the target before benchmarking.

**What the task is**
An insurer pricing a motor policy (the annual pure premium for one guarantee) at the start of a 2004 policy record, using driver,
usage, bonus-malus, area and 4-year claim history. This is a real and common actuarial use. Rows = 115,155 policy-period records,
taken from CASdatasets freMPL5..freMPL9. I verified this: their combined size is 115,200, and the 45 exact duplicates were removed. The 10,869 positive
claims match the number of positive ClaimAmount rows in the source exactly. Target = log1p(max(ClaimAmount,0)/Exposure), which I
reproduced exactly (max abs diff 0.0). length_to_year_end = (2004-12-31 - RecordBeg)/365 (matches to within 0.003), so it is
known at the start of the record.

**Concerns, most serious first**

1. Target/weight design: the "per year" log target is not invariant to exposure, so the Exposure weight does not do its job (serious).
   - For a rate target A/E, weighting by E is standard (Poisson/Tweedie). Taking log1p of the rate breaks that: P(claim) scales with E,
     while log1p(A/E) on a claim grows as E shrinks. The weighted mean target by exposure bin is
     E<=0.1: 0.20, 0.1-0.3: 0.43, 0.3-0.6: 0.76, 0.6-0.99: 1.05, E=1: 1.29. So the target mostly measures how long the record ran.
   - Exposure is withheld as a feature, but length_to_year_end is an upper bound on it (L>=E for 100% of rows, corr 0.49). Models learn
     exposure through L. With LightGBM and grouped 3-fold CV, the claim AUC of the log-target model is 0.627 with L and 0.560 without L.
     For an exposure-invariant Poisson rate model, the AUC barely moves (0.572 with L vs 0.569 without). So L only matters because of the
     target artifact, not because of risk. Weighted R2 drops from 0.0098 to 0.0019 when L is dropped.
   - Annualizing tiny exposures gives absurd values: a max of 11.6M per year from an ~800k claim. Exposure goes down to 0.001, and 84 claims
     have E<0.05.
   - Is the training weight right for the task? Weighting by Exposure is right for a frequency or pure-premium rate under a
     Poisson/Tweedie loss. Under squared error on log1p(rate) it is an ad-hoc fix that leaves the target biased by exposure (see the
     numbers above). Fix, either:
     (a) target = ClaimAmount/Exposure (no log), weight = Exposure, metric = Tweedie/Poisson deviance (the actuarially correct form); or
     (b) a frequency task: ClaimInd (binary) with Exposure as an input feature or offset. That is known at pricing time as the term of
         the contract. Without it, the signal is weak but honest: a Poisson rate model with E as offset reaches AUC 0.69.
     If the benchmark must use RMSE on a log target, keep Exposure as a feature rather than a weight, or restrict to E close to 1.
     Only 3.3% of rows have E==1, so that restriction leaves too little data.

2. Very weak signal / score dominated by noise (serious for benchmarking value).
   - 90.6% of targets are zero, and claim rows carry 88% of the weighted target variance. Weighted R2 in grouped CV: LightGBM 0.007-0.013,
     Ridge on one-hot features 0.011-0.016 (Ridge beats GBM in all 9 folds). Fold spread is about 0.002, comparable to the gaps
     between methods. A ranking of methods would mostly reflect noise and the exposure artifact. Concern 1's reformulation (a
     deviance metric or the frequency task) is the standard way to make it informative.

3. Negative claim amounts clipped to zero without saying so (moderate).
   - The source has 967 rows with ClaimAmount<0 across freMPL5-9: 165/324/220/163/95. All 965 that I matched have target 0.
     They are most likely recoveries or subrogation. Clipping is defensible, but task.md should say so.

4. Which guarantee/portfolio a row comes from was dropped (moderate, could not fully resolve).
   - The source says ClaimAmount is the "Total claim amount of the guarantee" and gives no per-file meaning. 15% of policy_components
     span more than one source file, and about 2,470 cross-file record pairs overlap in time. So the files may be different
     guarantees or covers on the same policies. Claim rates are similar (7.7-10.1%), so maybe not. Either way, a source-file
     indicator would be cheap, and it would be safer to keep it as a feature, or at least to document why it is dropped.

5. policy_component is a reconstructed key (minor).
   - Records link sensibly: LicAge steps track the calendar-time gaps between records (corr 0.83, median deviation about 0 months).
     Gender, SocioCateg, RiskArea, VehUsage, MariStat and HasKmLimit are constant within every component. About 3% of components have
     overlapping records, which hints at some over-merging. Over-merging is conservative for a grouped split.
   - Grouping is needed and correct here. After a claim in one record, the next record's claim-history count rises in 82% of
     cases. A random row split would let a test record's outcome show up in a training record's features. Within a record, the
     history columns look pre-period: the claim rate only climbs from 7.8% to 12.9% across history counts, so there is no leak.

6. Preparation details (minor).
   - Column types are fine: categoricals are categorical, and counts and RiskArea are int. RiskArea 1-13 is described as "possibly
     ordered", so int is acceptable. No missing values. Vehicle variables are absent from freMPL5-9 by source design.
     freMPL10 is excluded, which is reasonable since it has only 18 claims. One near-duplicate is left once the group id is ignored.

**What I could not check**
- Which guarantee each freMPL file represents. The source does not say ("Unknown French private insurer").
- The exact rule that built policy_component (I only inferred it).
- Whether the 45 removed rows were exactly the source duplicates. The counts match: 115,200 - 45 = 115,155. 272 prepared rows
  matched more than one source row, so the row-by-row mapping is only approximate.
- I read the source .rda files from GitHub (dutangc/CASdatasets, current master) with pyreadr installed into a scratch directory.

</details>

<details><summary>Task gamer</summary>

**Task gamer report: frempl_french_motor_personal_line (target log1p_claim_amount_per_year, ordered_lorenz_gini per_unit, weight Exposure, grouped by policy_component, 3x3 splits)**

Verdict: the task can be gamed badly. A record of this table ends when a claim happens, so the record's length (the weight) and the next record of the same policy (which is in the same test fold) both reveal the outcome. Rebuilding the next record from the features alone takes the Gini from 0.20 (best honest model) to 0.64.

Every model is LightGBM with Exposure as the sample weight, scored on all 9 shipped splits. The "baseline" is the brief's untuned LGBM: L2 on the shipped log1p target, 300 trees. The "honest tweedie" is a Tweedie LGBM on expm1(target), the per-year rate (honest2.py).

**Honest scores (mean over the 9 splits)**

```text
baseline (L2 on log1p target)          0.1407  (per split 0.10-0.18)
baseline + random column, 3 seeds      0.148 / 0.153 / 0.153
honest tweedie on the raw rate         0.2025  (per split 0.17-0.25)
tweedie + random column, 3 seeds       0.165 / 0.193 / 0.196  -> the noise spread is about 0.04
The metric is very noisy: it is an unnormalised Gini on heavy-tailed claim amounts.
```

**Exploits, ranked by gain**

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Successor record rebuilt from features: changes in claim counts and BonusMalus to the next record of the same policy, plus Exposure | 0.2025 (tweedie) | 0.6394 | +0.437 (+0.423..+0.448) | No (the next record is created by the outcome) | Collapse the records of a policy-year into one row, or drop the count and BonusMalus columns of any record that follows a cut |
| 1b | Same successor deltas, no Exposure | 0.2025 tweedie / 0.1407 base | 0.5893 / 0.5588 | +0.387 (+0.368..+0.402) / +0.418 (+0.387..+0.475) | No | as above |
| 1c | d_claims alone (rise in the next record's claim counts) | 0.2025 / 0.1407 | 0.5420 / 0.5113 | +0.34 / +0.371 (+0.334..+0.44) | No | as above |
| 1d | Rule with no model: rows with d_claims>0 first, linked rows with no new claim last | 0.1407 | 0.5051 | +0.364 (+0.319..+0.436) | No | as above |
| 2 | ends_early flag (Exposure < length_to_year_end) | 0.2025 | 0.2905 | +0.088 (+0.06..+0.11) | No | Ship the planned term, not the realised exposure; or merge cut records |
| 3 | The weight: Exposure as a feature (Tweedie model) | 0.2025 | 0.2846 | +0.082 (+0.051..+0.104) | No (a claim cuts it short) | as #2 |
| 3b | The weight as a rule: log P(claim) - log Exposure | 0.2025 | 0.2841 | +0.082 (+0.03..+0.12) | No | as #2 |
| 3c | The weight alone: prediction = -Exposure | 0.1407 base | 0.1837 | +0.043; it beats the brief's baseline with no model at all | No | as #2 |
| 4 | d_bm alone (BonusMalus change to the next record) | 0.2025 | 0.2734 | +0.071 | No | as #1 |

Note on Exposure fed to the L2 log1p baseline: the score drops to 0.005, and to 0.023 with E/L and ends_early added. On the log scale the model learns that short rows are mostly zero. The weight only pays off on the rate scale (the Tweedie model or the rule).

**Mechanism**

**#1:** A freMPL row is a record (RecordBeg-RecordEnd) of one policy in one year. When a claim happens, the claim-history columns change, so the record is closed and a new one opens. The next record starts where this one ends: its length_to_year_end equals this row's length_to_year_end minus Exposure (within 0.002), and its LicAge equals this row's LicAge plus 12*Exposure (within 1 month). Its Gender, MariStat, SocioCateg, VehUsage, HasKmLimit and RiskArea are the same. Matching on these, without policy_component, links 39% of the rows, and 99.7% of the links fall in the same group, so the successor is always on the test side with the row. Among linked rows, when the successor's claim counts rose by 1 the row has a claim 87.5% of the time; when they did not rise, 1.4% of the time (base rate 9.4%). The claim frequency per exposure-year is 1.59 for cut rows whose successor gained a claim and 0.036 for cut rows whose successor did not.
Mildest fix: aggregate the records of a policy-year into one row (summed exposure and amount, features at the first record), or keep only each policy-year's first record. Grouping by policy keeps the successor in the same fold, so it does not stop this; it makes it worse.

**#2/#3:** Exposure (the training weight and metric weight) ends at RecordEnd, and a claim moves RecordEnd forward. The loss per exposure-year is 312 for records that run to year end, 1227 for cut records with no successor found, 67 for cut records whose successor shows no new claim, and 3222 for cut records whose successor shows one. The per-year rate is falling in Exposure: about 1200/yr in the shortest decile, 295/yr in the longest. A model given Exposure, or the flag Exposure < length_to_year_end, learns "short record = claim". At the start of cover the insurer knows the start date (length_to_year_end) but not when the record will end.
Fix: same as #1 (one row per policy-year makes the exposure run to the planned term or to cancellation). Keeping Exposure out of the features is already the case. The issue is that it is also the target's divisor and the metric's weight, and a participant can feed it in from scoring.parquet.

**Flaws that hurt an honest model**

| What is wrong | Honest choice | Baseline score | Honest-choice score | Fix to the task |
|---|---|---|---|---|
| The target ships as log1p of a per-year rate, but the metric ranks on the original scale. L2 on log1p ranks the claim indicator, not the expected rate. | Fit the rate expm1(y) with a Tweedie (or Poisson) objective, weighted by Exposure | 0.1407 | 0.2025 (+0.062, per split +0.037..+0.144) | Not strictly a flaw. Ship the raw per-year amount, or say in task.md that the score is on the expm1 scale. |

The record-splitting above also distorts the honest training target: claim-free pieces of a cut policy-year get a tiny rate. I found no honest row filter that undoes this. The fix for #1 removes it.

**Attacks that found nothing**

- Row position: Spearman with the target 0.001. Next-row label agreement 0.8297 vs 0.8290 by chance. Tweedie + row position 0.1945 (vs 0.2025).
- policy_component id as a feature: 0.2009; Spearman with the target -0.012.
- has_prev (a predecessor record exists; past information): 0.2033. has_next alone: 0.2101, within noise.
- Year-end successor (next year's record): the links are spurious (0% same group, no label signal). The data covers one year.
- Exact feature copies across the split: 0.4% of the test rows (split r0f0), and their train labels do not predict (7% vs a 9.4% base rate).
- Format of length_to_year_end (last digit): the positive rate is 0.07-0.11 across digits, with the 0 digit (year-start records) at 0.106. That is the record structure again, not a separate signal.
- Train vs test classifier: AUC 0.54 on three splits, so no usable shift.
- No column is standardised or scaled over all rows. The targets have no sentinels (min 0; source claim amounts can be negative, the kit clips them to 0).

**Could not check / notes**

- I did not compare row by row with the public freMPL5-9 files. A lookup in the published source would work, as for any public dataset, and is not ranked.
- The web turned up no competition forum or leak thread for freMPL. The CASdatasets reference only confirms that the claim-history columns cover "the 4 preceding years" and that records are RecordBeg-RecordEnd.
- That a claim causes the record split is inferred from the data (the claim counts rise in the successor; the loss per year is extreme in cut records). The source documentation does not state it.
- About 14,400 cut records have no successor found (frequency 0.33 per year). These are cancellations after a claim, or links my matcher missed. The policy_component oracle links the same share (39%).
- I did not open any file outside the kit.

Sources: https://dutangc.github.io/CASdatasets/reference/freMPL.html

</details>

<details><summary>Precedent check</summary>

**Precedent check: frempl_french_motor_personal_line (full tier, exposure re-review, 2026-11-06)**

**Verdict in short:**
- **D9 is consistent.** It follows the four sibling calls Lennart made the same day, and where it reverses Andrej's issue-4 call it names the fact that sets the case apart.
- **The unrounded `length_to_year_end` departs from Andrej's call, with a stated reason.** It undoes Andrej's month rounding of 2026-11-02, gives a reason that holds up, and is consistent with pricing_game_2016 and the spanish table. It is still an AI call that needs Lennart's mark.
- **One real departure has no fact that sets it apart: keeping the length on the log1p scale (issue 7, option A).** The reflection prompt for it is at the end. It also shows a conflict between two rule texts that issue 7 does not mention.
- **Two recording gaps** (point 3).

The register's flags (opposite outcomes on LEAK-38, TP-10, USE-5, USE-8, few_minority, one_feature, trivial; amendments due on SPLIT-10, SPLIT-14, CLEAN-19; exceptions to Musts) don't touch this decision. None is on LEAK-41, MET-14, MET-15, MET-16 or CLEAN-16, or on the mechanism "realized weight / time on risk" (19 decisions, no flag). I found no drift: Lennart's CLEAN-16 calls of 2026-11-05 and 2026-11-06 all follow the amended text. No third exception of one kind either, so no amendment is due.

**1. D9: target per realized year, `Exposure` as weight and sample_weight, never a feature; `exposure_at_start` dropped; `ordered_lorenz_gini(per_unit=True)`. Consistent.**

**Follows** (all CC, 2026-11-06, Lennart, under LEAK-41, MET-14 and MET-15):
- **fremtpl2:** ClaimNb / Exposure, Exposure the weight. Metrics Cases row l.313.
- **bemtpl97:** nclaims / expo. Row l.314.
- **australian_vehicle_insurance_2004_2005 (D8):** claimcst0 / exposure, identity scale, `normalized_weighted_gini` on the rate. Row l.315.
- **pricing_game_2016_french_fleet (D11):** charge per vehicle-year, the realized period as weight. Row l.317.
- **spanish_motor_insurance_coverage_level_2022_2024 (D10):** `actual_exposure` as metric weight and sample_weight, the hybrid `total_exposure` dropped.

frempl has the same structure as all of these: a realized time on risk that claims cut short, used as the rate's denominator. All five give the same treatment. Each sibling's CC names the curator call it supersedes and why.

**Where frempl differs, the difference is allowed:**
- **Metric form:** the unnormalised CAS ordered Lorenz Gini here, the normalized weighted Gini on australian and pricing_game_2016. MET-15 fixes the weight, not the metric, and MET-10 chooses the metric per table. Andrej said on 2026-11-02 (pricing_game_2016): "It is case by case and when in doubt we go for diversity". D9 keeps Andrej's own choice of form from 2026-11-03.
- **Scale:** log1p here and on spanish; identity on australian and pricing_game_2016. This follows Andrej's per-file call of 2026-11-02 (australian CC: "this table ships the claim cost in dollars, the log1p tables keep log1p") and CLEAN-16 as amended ("a rate scored by a Gini keeps the scale the curator chose"). This is not a pair of similar cases decided differently: each table keeps its own scale, as the rule says. But pricing_game_2016's notes give a general reason for identity ("a log1p fit transformed back orders by its geometric mean"). That reason would apply here too. It feeds issue 7, not D9.

**Reverses Andrej's call of 2026-11-03 (issue 4, option C over B), with a fact that sets it apart:**
- Andrej turned down B because a constant prediction scored 0.184 when totals were scored against the realized base: the metric itself read the record's end.
- Under D9 the target is the rate, so a weighted constant scores 0. The realized length now acts only through 1/`Exposure` as a would-be feature (0.184, the ceiling), and LEAK-41 (Must, adopted the same day) keeps it out of the features. Probe 22 finds no feature whose gain goes through `Exposure` above noise (length_to_year_end weight-mediated -0.060, SD 0.034).
- So the fact Andrej's call rested on (the constant's score) no longer holds. The change also comes through an adopted rule, not drift, and the two calls are by different curators. Under "Who decides", a newer curator decision with a stated fact wins.
- The record states this fact (CC l.154; REVIEW issue 6, Consistency bullet). No prompt is needed.

**2. Unrounded `length_to_year_end` (dataset agent's call, for Lennart to confirm): departs from Andrej's rounding, with a stated reason; consistent with the siblings**

**Precedent it departs from:** Andrej, 2026-11-02 (CC l.138, issue 2 (a)): "every `Exposure` rounded to months". The reason recorded then was that the three decimals of the *realized* length told a continued record from an open one (AUC 0.92 to 0.71, 0.91 to 0.61), and the rounding cost nothing.

**Fact that sets it apart** (stated in dataset.py l.184 and REVIEW issue 6):
- The column is now a function of the start day alone: the source's own `Exposure` for open records starting that day, one value per day. Its decimals carry no end, so the mark the rounding hid is gone.
- LEAK-41's "a value whose precision marks the cut" does not apply.
- The column auditor reaches the same reading (column_auditor.report.txt l.23-30).
- A second, weaker reason: rounding would make 2,704 records within one component repeat another record's features and target (3,445 repeats against 610, copies.log against copies_unrounded.log). The score would not move (-0.002 / -0.001).

**Siblings:**
- **pricing_game_2016:** `exposure_to_year_end` keeps the source's own precision (0.01 year, the grid of Exposition_au_risque), and `period_start` (to the day) is a feature. So the start day at full precision is already a shipped input in the nearest sibling.
- **spanish:** "do not round the premiums" (Andrej, 2026-11-02): the source's precision kept when rounding bounds no leak.
- The rule both follow: the start-known length at the source's own precision. The unrounded column is consistent.

**Recording gap:** REVIEW.md's "**Resolved (2026-11-06, Lennart):**" block (issue 6) writes "unrounded: ..." as part of Lennart's resolution. Lennart's CC line (record l.154) does not mention the rounding, and CHANGES.md calls it the agent's call for Lennart to confirm. Under "Who decides" (principles.md), an AI call sits below Andrej's CC until a curator marks it. Either Lennart confirms it (one line in the CC, naming Andrej's rounding of 2026-11-02 as superseded and why), or the Resolved block marks the clause as the AI's, pending. This is not a consistency problem, only an attribution one.

**3. Recording gaps (no departure)**

- **D9 also supersedes Andrej's issue-2 call of 2026-11-02, but the CC line names only issue 4.** That call kept the realized length on the 34,324 continued records, as a potential leak kept on purpose, and rounded it to months. The REVIEW header says so ("it supersedes the fix of 2026-11-02 under LEAK-10"). The australian (D8) and pricing_game_2016 (D11) CC lines each name every Andrej call they supersede, so frempl's CC should too, for the record to match its siblings.
- **LEAK-41 Cases text and probe 22's row l.370 are now stale.** They still quote "1/length alone 0.184, the honest model 0.176", the figures under the metric of 2026-11-03. The D9 figures are 0.184 against 0.183 (Tweedie), as the metrics Cases row l.316 has them. This is a wording fix in the knowledge file, not a decision.

**4. Keeping `length_to_year_end` on the log1p scale (D9 as worded = issue 7 option A): departs from CLEAN-16 without a fact that sets it apart**

**The rule:** CLEAN-16 (Should, amended 2026-11-06 by Lennart) says "A log-scale rate with its denominator as a feature misleads L2 fits ...; drop the feature or ship the identity scale". The rule's mechanism is measured here: mean log1p rate 0.29 to 1.08 by length band; L2 on log1p 0.156 with the length and 0.185 without, lower on 7 of 9 splits; probe 22 L2 weight-mediated -0.060.

**The reason D9 gives** ("CLEAN-22, USE-6") does not set the case apart:
- USE-6 makes the input legitimate, not required.
- CLEAN-22 is about width.
- Neither answers a learner being misled by the scale.

**Precedents:**
- **pricing_game_2016 (Lennart, 2026-11-06):** the start-known length kept as a feature, on the identity scale. This is the clause's identity remedy.
- **spanish_motor_insurance_coverage_level_2022_2024 (Lennart, 2026-11-06):** log1p kept with no length feature. But `total_exposure` left under LEAK-41 as a hybrid, and that release has no start date to build a start-known part from. So spanish is not a precedent for dropping a start-known length for the L2 reason. No applied case of that exists.

**Conflict between rule texts that issue 7 leaves out:**
- LEAK-41 (Must) says "A part known at the start ships as its own column (LEAK-7, LEAK-37)".
- The leak Mechanisms row (l.441) says the fixed length "may stay a feature".
- If LEAK-41's sentence is a directive, issue 7's recommended B (drop) breaks a higher-ranked Must to satisfy a Should, and only C meets every rule.
- If it is a permission, B is fine.
- The principles tension row "Width against model limits: ... a model's input cap is never an argument" also leans against dropping a legitimate input because of one family of losses.
- So the precedents and ranks favour C. Issue 7 frames C as a departure from the curator's scale, but CLEAN-16 itself names C as a remedy.

**Reflection prompt** (to append to issue 7 of REVIEW.md, in the review-file shape):

**Consistency check (AI, 2026-11-06):** Does anything set frempl apart from CLEAN-16's clause on log-scale rates, or should it go like pricing_game_2016 (identity scale, length kept)?

* **Problem:**
  - D9 keeps both the log1p scale and `length_to_year_end`. CLEAN-16 asks for one or the other, and it gives no exception[^cc1].
  - The reason D9 gives (USE-6, CLEAN-22) makes the column legitimate but doesn't answer the misled L2 fit (0.156 with the column, 0.185 without, 7 of 9 splits).
  - pricing_game_2016 (Lennart, 2026-11-06) kept its start-known length and shipped the identity scale. spanish dropped `total_exposure` for LEAK-41, not for this clause.
  - Dropping the column (issue 7 B) may conflict with LEAK-41's "a part known at the start ships as its own column"[^cc2].

| | Option | Pro | Con |
|---|---|---|---|
| a | Exception to CLEAN-16 (keep A): the column is known at the start on every record, and LEAK-41 asks for that part as a column; the notes name which losses it misleads | keeps a legitimate input and the curator's scale; serves P4 and USE-6 | first exception to the clause; squared-error learners lose 0.029 for a reason unrelated to risk |
| b | Treat like the clause's letter: drop the column (issue 7 B) | L2 and Tweedie fits score alike (0.185, 0.179); scale kept | may break LEAK-41's start-known sentence (Must over Should); drops an input worth +0.005 (SE 0.004) to Tweedie |
| c | Treat like pricing_game_2016: identity scale, column kept (issue 7 C) | meets CLEAN-16, LEAK-41 and the nearest sibling; L2 then estimates the cost per year | L2 scores 0.159, led by the tail (11.6 million per year); changes the per-file scale of 2026-11-02 |
| d | Amend CLEAN-16 (or LEAK-41) to say which wins for a start-known length on a log-scale rate | settles this table and the next one alike | a rule change for one case so far |

* **Recommendation:** c, or d if the log1p scale matters more to you than the sibling match. c is the only option that meets every rule text and follows pricing_game_2016. b should wait until LEAK-41's sentence is read as a permission. **Decision:** a, b, c or d?

[^cc1]: **CLEAN-16** (Should; amended 2026-11-06, Lennart): a rate scored by a Gini keeps the curator's scale; a log-scale rate with its denominator as a feature misleads L2 fits: drop the feature or ship the identity scale.
[^cc2]: **LEAK-41** (Must; 2026-11-06, Lennart): "A part known at the start ships as its own column (LEAK-7, LEAK-37)"; against it, the Mechanisms row of leak_checks.md: "which may stay a feature". **USE-6** (Must): an input known at the prediction point is legitimate. Precedents: pricing_game_2016_french_fleet CC 2026-11-06 (identity, `exposure_to_year_end` kept); spanish_motor_insurance_coverage_level_2022_2024 CC 2026-11-06 (log1p, `total_exposure` dropped under LEAK-41).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: frempl_french_motor_personal_line (full tier, exposure re-review 2026-11-06)**

Position: ship. Validity holds where today's change touches it. I concede one Must-level split finding (finding A of the split audit). Its fix is a split edit that keeps the dataset. Issue 7 is a P7 call, and I take a side on it below. The panel found no problem that cannot be fixed inside the definition.

1. The target, weight and metric of D9 are the actuarial convention, and the Musts behind them hold. They also answer the blind reviewer's concern 1.
   - Evidence. The claim audit tested the D9 claims, and all of them hold:
     - target = log1p(ClaimAmount/Exposure); the round trip asserts;
     - Exposure is the weight scoring column, the metric's weight and sample_weight, and is not among the 16 features;
     - exposure_at_start is gone;
     - the scorer matches an independent CAS ordered-Lorenz Gini to 4e-12;
     - a weighted constant scores 0.000 on 9 of 9 splits.
   - Precedents. Lennart gave the same treatment the same day to fremtpl2, bemtpl97, australian_vehicle_insurance (D8), pricing_game_2016 (D11) and spanish_motor (D10). The precedent checker calls D9 consistent. Where it reverses Andrej's issue-4 call, it names the fact that changed: the constant scored 0.184 then and scores 0 now.
   - Practitioner: the earned-exposure-weighted pure premium is "the number I set the premium from". A record cut short after a total loss "is risk I must price, not noise" (837 against 311 per exposure-year).
   - Rules: LEAK-41 (Must), MET-15 (Must), MET-14 (Should). Who decides: Lennart's D9 is the newest curator decision.
   - Against the blind reviewer's "the weight does not do its job; switch to Tweedie deviance or a frequency task":
     - The weight works for the loss that suits the metric. Dropping it costs Tweedie -0.023, worse on 9 of 9 splits (claim audit row 16).
     - The proposed deviance metric fails on this table. On 3 of 3 folds the Tweedie fit scores worse than a flat rate (132.64 vs 132.56, 121.23 vs 120.86, 117.84 vs 117.56), because tail rates of up to 11.6M per year swamp it (practitioner, Q5).
     - A frequency-only task changes what the actor acts on (USE-5).
     - The Gini scores on the expm1 scale and is invariant to order, so the log1p scale only matters for training. That is issue 7 (P7), not a validity problem.

2. No realized length reaches the features, and length_to_year_end is known at the start. This answers the claim that "exposure leaks in through L".
   - Evidence. length_to_year_end is a function of the start day alone:
     - one value per day; 0 of 366 days have two different open-record values;
     - strictly monotone in the start date; L >= E on all rows;
     - unrounded decimals are the source's calendar precision, not the record's end (column audit, claim audit row 4).
   - Without L, the tariff predicts Exposure at R² 0.003. No rating factor carries risk selection into the length.
   - Probe 22, both arms: L's weight-mediated gain is negative, -0.038 (SD 0.019) under Tweedie and -0.060 (SD 0.034) under L2, and negative on 9 of 9 splits in the claim audit. No other feature is above noise.
   - Rules: USE-6 (Must), LEAK-41 (Must, a timing call). The blind reviewer's AUC gap from L appears only under the log1p target. That is CLEAN-16's mechanism (P7, issue 7), not a P4 leak.

3. The data is faithful, and the grouped split is right. The blind reviewer confirmed both independently.
   - Evidence from the blind review:
     - 115,200 source rows minus 45 exact copies gives 115,155;
     - the 10,869 positive claims match the source exactly;
     - the target was rebuilt with max abs diff 0.0;
     - the history columns are pre-period; grouping is "needed and correct".
   - Split audit: no component straddles any of the 9 splits; every test fold has 3,570-3,675 claims (MET-2 computable).
   - Rules: PROV-7/8/9 hold, SPLIT-9 (Must, as fixed by issue 1), SPLIT-8 (ForcedGroupedFromTemporal, settled 2026-11-02).
   - The in-year temporal alternative is ruled out. Its training side is selected by the realized weight: 12.8% of rows by 1 April, cost 1,140 against 311 per year (split audit, point 1). LEAK-41's last clause forbids that, and it also falls below the 50% floor.

4. The task is worth benchmarking. TP-2 (Should) and TP-4 (Must) hold; the "weak signal" objection is a weighing factor, not a blocker.
   - Evidence:
     - honest Tweedie 0.183; L alone 0.005; the margin over L alone is at least 0.14 on 9 of 9 splits;
     - weighted constant 0; random orders 0.003 (SD 0.037);
     - claim AUC about 0.67.
   - The probe's no_signal flag comes from R² on the log1p scale. On the declared metric the models beat the constant by about 0.18 (claim audit, other observations).
   - Rank: TP-2 says a small real signal is no reason to retire. The principles' tension row "right split against the score" puts P4 over P6.
   - Fold noise (SD about 0.03) and one large claim moving fold 0 by 0.06 are real minuses. Their remedy is a note: compare models by paired fold differences, and optionally measure a large-loss cap in scoring (practitioner). Neither is an exclusion.

5. The successor-record exploit is the settled LEAK-9 route. A protocol line already covers it. The number in the text needs updating.
   - Evidence. The task gamer reaches 0.639 from 0.203 by rebuilding each test record's successor from other test rows. The split audit's oracle gives +0.355. Both read other test rows of the same fold. LightGBM reading one row cannot use this, and neither can TabPFN in its usual batch.
   - Rule: LEAK-9 (Should, amended 2026-11-05). An evaluation-level leak where "a model can read other test rows" is fixed "by a protocol line the benchmark checks, not in the data". Precedents: fremtpl2, medical_facility_operational_data, sepsis_prediction. Lennart settled it for this dataset in issue 6.
   - Against the gamer's fix (collapse each policy-year into one row): it is not milder. It rebuilds the unit and the weight, and the 1 January starts are calendar cuts, not pricing events. The split audit also shows that keeping one record per component in test drops about 15,000 test rows per fold, selected by contract changes that correlate with claims (LEAK-41).
   - Gamer exploits 2 and 3 (Exposure fed in from scoring.parquet) amount to using the weight as a feature. MET-15 and the shipped feature_columns forbid that for every exposure dataset; nothing here is specific to frempl.
   - Concession (EV-2): restate the protocol line's figure as "+0.26 to +0.44, depending on what is read", instead of +0.260 alone.

6. Concede: the split audit's finding A is a real SPLIT-9 Must problem. It is fixed in the split, and the dataset stays.
   - Evidence. A contract change that also changes one profile column leaves a policy split across components. The later record then sits in train and tells the test record's claim:
     - 9,160 candidate pairs; about 3,200 are true links;
     - the counter rises after 0.939 of claims against 0.073 of non-claims when HasKmLimit changes;
     - a train-only lookup gains +0.020 (SD 0.010), better on 9 of 9 splits.
   - Only models that read training rows (kNN, retrieval, in-context learners) can use it. SPLIT-9 is a Must, so "whatever it costs" applies. Under "independent failures are not conflicts", nothing ranked above it excuses it.
   - Mildest remedy: (i) a per-fold filter that drops the one-column candidate successors of a fold's test rows from its training side (about 2-3% of training rows; groups unchanged; a split edit only). Alternatively (ii), widen the component with these links, which fits Andrej's "most conservative key". Under (ii) the lookup gain falls to -0.0045, and the honest score moves from 0.174 to 0.169, inside the fold SD of 0.03.
   - Either reopens issue 1's key, so the curator must mark it. Neither threatens the dataset.

7. Issue 7 is open: CLEAN-16 (Should) against keeping L on the log1p scale. It is a quality call, and either fix keeps the dataset. The remaining items are text.
   - Concede: shipping A (the definition as it stands) needs a recorded exception, and the precedent checker finds no fact that sets frempl apart.
   - Evidence:
     - L2 on log1p scores 0.156 with L and 0.185 without (lower with L on 7 of 9 splits);
     - Tweedie gains only +0.005 (SE 0.004) from L;
     - the practitioner: "a cut made by the extract's calendar year, not a rating factor".
   - My side: B, drop L, the mildest fix. It keeps the curator's scale and stays inside CLEAN-16's letter. On the precedent checker's worry that B breaks LEAK-41's "a part known at the start ships as its own column": the Mechanisms row says the fixed length "may stay a feature". I read that as a permission, so B does not break the Must. If Lennart reads the sentence as a directive, C (identity scale, as in pricing_game_2016) is the way out. Either way this is P7, fixed when cheap and safe, and it is no reason against shipping (principles, step 3).
   - Text fixes, all cheap (EV-2):
     - reword "1/Exposure alone, the ceiling a leak would reach" (refuted: Exposure as a feature reaches 0.256);
     - say that length_to_year_end is a one-to-one recoding of the start date (moot under B);
     - have Lennart's CC confirm the unrounded length and name Andrej's issue-2 rounding of 2026-11-02 as superseded;
     - state in the notes that the 967 negatives were set to 0 (the blind reviewer asks for this; the claim audit shows it is already counted).

Proposed judgment: ship after changes.
- Validity: LEAK-41, MET-15, USE-6, PROV, SPLIT-8 hold. SPLIT-9 is triggered by finding A and fixed by the per-fold filter or the widened key (curator mark). LEAK-9 is covered by the protocol line, with its figure restated.
- Value: TP-2 small real signal, TP-4 holds.
- Quality: CLEAN-16, issue 7, B (or C).
- For the curator: issue 7, and the key for finding A.

</details>

<details><summary>Critic</summary>

**Critic, opening brief: frempl_french_motor_personal_line (exposure re-review, full tier, 2026-11-06)**

Verdict asked: ship only after changes. Point 1 is a Must under P4 and has to be fixed before the dataset ships. Points 2 to 6 ask for corrected numbers, a curator decision or notes. None of them is a reason to exclude: the task is real (domain practitioner: a pure premium per earned year, weighted by earned exposure, is the actuarial convention), and D9's target, weight and metric hold on the data (claim auditor, claims 1-12 and 14-28).

1. A hidden successor route crosses the split (P4, SPLIT-9 Must; SPLIT-24, SPLIT-30).
- Problem: the policy_component key joins records only when all six PROFILE columns are equal. A contract change that also changes one of them (RiskArea, HasKmLimit, VehUsage, SocioCateg, MariStat) leaves the policy split across components. The later record can then sit in train and give away the test record's claim through its claim counters.
- Evidence (split auditor, finding A):
  - 9,160 one-column-changed pairs over 7,120 predecessors, none in the same component.
  - The pairs are real links, and the test could have refuted it. The successor's counters rise after 75.5% of claims against 41.9% of non-claims. Shifted end dates give no contrast (0.63-0.67 against 0.62-0.65). HasKmLimit changes are near exact (0.939 against 0.073).
  - A training-side lookup gives +0.0203 Gini (SD 0.010), better on 9 of 9 shipped splits (0.1742 to 0.1945). The "a candidate exists" flag alone gives -0.003, so the gain is the claim, not the early end.
  - Under widened groups the gain falls to -0.0045 (4/9). The honest score is 0.1686 against 0.1742, an unpaired comparison inside a fold SD of about 0.03.
- Effect: a model that reads training rows (kNN, retrieval, in-context learners) can learn a test record's outcome from its own policy's later record. This is the path issue 1 closed for exact-profile links, at about 1/5 of the size.
- Rule: SPLIT-9 (Must) says a shortcut of the row's own entity is removed whatever it costs. The tension row in principles.md says a measured shortcut is always removed. Issue 1 sets the precedent that lookup routes count, even though LightGBM cannot use them.
- Remedy (fix the definition): widen the component with the one-column links. This follows Andrej's "most conservative key" call of 2026-11-03; the measured cost is within noise; the largest group is 90 records. Failing that, a per-fold filter that drops the one-column candidate successors of each fold's test rows from training (about 2-3% of training rows). Either reopens issue 1's key and needs the curator's mark.

2. The LEAK-9 protocol line understates the route it guards, and the route needs no group id (P4, LEAK-9 Should).
- Problem: the notes, CHANGES and REVIEW give the successor oracle as +0.260 (0.443 against 0.183). Three agents measured more:
  - claim auditor: 0.467 (+0.285, 9/9);
  - split auditor: 0.529 (+0.355, 9/9), with the in-component successor and the days to its start;
  - task gamer: 0.2025 to 0.6394 (+0.437, range +0.423 to +0.448). It rebuilt the successor from features alone, without policy_component, matching length_to_year_end minus Exposure and LicAge plus 12*Exposure. That links 39% of rows, 99.7% of them within one group. A rule with no model (d_claims > 0 first) scores 0.505.
- Effect: a method that reads other test rows can reach about three times the honest score. The note tells the benchmark operator how much to look for, so an understated size makes a cheating method harder to spot. The grouped split keeps successors on the test side, so the protocol line is the only guard (the gamer: grouping "makes it worse").
- Rule: LEAK-9 (Should, amended 2026-11-05) puts the fix in a protocol line, as for fremtpl2 and medical_facility_operational_data. I do not ask for a re-split: the split auditor shows that one record per component in test would select rows by contract changes, which LEAK-41 forbids. EV-2: a measurement outranks the stated figure.
- Remedy (a note): restate the size as "+0.26 to +0.44 depending on what is read". Say that the successor can be found from the features without the group id (length to 31 December minus Exposure, LicAge advanced). After point 1's fix, the line also covers the one-column successors.

3. Issue 7 rests on two rule texts that disagree, and the recommended option B may break the Must (P4 LEAK-41 Must against P7 CLEAN-16 Should).
- Problem: the definition keeps both the log1p scale and length_to_year_end, which CLEAN-16 (amended 2026-11-06) asks against.
  - Measured: L2 on log1p scores 0.156 with the column and 0.185 without (claim auditor: -0.030, SE 0.011, lower on 7 of 9). Tweedie: +0.004 (SE 0.005).
  - Weighted mean of log1p by band of the length: 0.289 / 0.636 / 0.881 / 1.013, while the cost per year stays flat at 394 / 469 / 451 / 441.
  - The blind reviewer, working without our notes, ranked the same mechanism as the most serious problem: claim AUC 0.627 with the length against 0.560 without for the log target, and 0.572 against 0.569 for a Poisson rate model.
- Effect: the most common learner family loses about one random-order SD (0.037) for a reason unrelated to risk. Rankings between learners change.
- The trap: the agent recommends B (drop the column). LEAK-41 (Must) says "a part known at the start ships as its own column", and the column auditor confirms this column is exactly that part (a function of the start day only, one value per day, L >= E on every row). If that sentence is a directive, B breaks a higher-ranked Must to meet a Should. Option C (identity scale, column kept) meets CLEAN-16, LEAK-41 and the nearest sibling, pricing_game_2016_french_fleet (Lennart, 2026-11-06: identity scale, exposure_to_year_end kept). The precedent checker found no fact that sets frempl apart from it.
- Remedy (fix the definition, the curator's call): C. B only if the curator records that LEAK-41's sentence permits the column rather than requires it. Either way, add the precedent checker's consistency prompt to issue 7. Its cost under C: L2 on the identity scale scores 0.159, led by the tail. Tweedie is unaffected.

4. One claim decides a fold (P6 value; MET-1 "scores the decision", EV-2).
- Evidence:
  - Domain practitioner: capping losses at 50,000 in scoring moves fold 0's Tweedie Gini from 0.210 to 0.147. The 802,620 claim is 3.6% of all cost; the ten largest claims are 7.6%.
  - Random orders: per-fold SD 0.037 (up to 0.071).
  - Task gamer: a random column added to Tweedie spreads it by about 0.04 (0.165 to 0.196).
  - The Tweedie-L2 gap is 0.030, and 1/E per fold ranges 0.13 to 0.26.
  - Annualised tiny exposures reach 11.6 million per year (58,087 over 1.8 days).
- Effect: method gaps below about 0.04 are noise unless they are paired by fold. A pricing actuary caps and loads large losses separately.
- Rule: TP-2 keeps a small real signal, so this is no exclusion. MET-1 asks that the metric score the decision, which the practitioner answers "partly".
- Remedy (a note): state in the notes that comparisons need paired fold differences, with the fold SD. Measure a large-loss cap on the losses the Gini reads on the shipped splits and give the curator the number as an option. Do not change the metric without that measurement.

5. A stated bound is refuted: "1/Exposure alone, the ceiling a leak would reach" (EV-2; the wording of LEAK-41 and probe 22).
- Evidence: with the realized length as a feature the score is 0.259 (claim auditor), 0.256 (the definition's own number) and 0.240 against 0.183 (probe22_actuarial.txt). That is about 0.07 past the "ceiling". 1/E alone is a floor for a perfect proxy combined with the features, not a ceiling. The column auditor's report repeats the wrong reading ("Those numbers are the ceiling a leak would reach").
- Effect: a reviewer would wave through a partial proxy scoring 0.20 as "below the ceiling". The figure appears in five places: the metric reason, the notes bullet, the REVIEW summary, CHANGES and the probe output. LEAK-41's Cases text also still quotes 0.176 for the honest model, where D9 gives 0.183.
- Remedy (a note): reword the dataset's texts to "1/Exposure alone scores 0.184, as much as the honest model; with the features the realized length reaches 0.256". Flag LEAK-41's and probe 22's "ceiling" wording to the curator as an amendment; it is not an edit for the dataset agent.

6. Recording gaps ("Who decides" in principles.md; CLEAN-22, EV).
- The unrounded length_to_year_end is the dataset agent's call (CHANGES: "Lennart to confirm"). REVIEW.md's "Resolved (2026-11-06, Lennart)" block records it as Lennart's resolution, and Lennart's CC line does not mention it. It supersedes Andrej's month rounding of 2026-11-02. Until a curator marks it, Andrej's call ranks above an AI call. The data supports the call (column auditor: one value per start day, no realized decimals), so this is attribution only.
- D9's CC line names only issue 4 as superseded. It also supersedes Andrej's issue-2 call of 2026-11-02. The australian (D8) and pricing_game_2016 (D11) CC lines each name every call they supersede.
- The notes say "dropped the record dates", but length_to_year_end is a one-to-one recoding of RecordBeg (366 values).
- Remedy (notes): ask Lennart for one CC line that confirms the rounding change and names both superseded Andrej calls. Add one clause saying the start date ships as length_to_year_end.

Points I checked and dropped:
- Exposure fed in as a feature, or the ends_early flag (task gamer: +0.082, +0.088). These need the test rows' scoring column as an input, which LEAK-41 and MET-15 already forbid. Nothing shipped reaches it (probe 22: no feature's gain is mediated by Exposure above noise).
- Merging a policy-year's records into one row (task gamer's fix). The domain practitioner shows the earned-exposure segments are the unit a pricing GLM is fitted on, and the protocol line covers the route. I found no rule that requires the merge.
- A source-file or guarantee indicator (blind reviewer). Issue 3 is settled and the files show similar claim rates; I have no evidence that the files are different guarantees.
- The negative amounts set to 0. Already in the notes (967 rows), and the practitioner agrees with it.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: frempl_french_motor_personal_line (exposure re-review, 2026-11-06)**

The critic and I reach the same verdict: ship after changes, with nothing that excludes the dataset. We differ on two things: the remedy for issue 7 (point 3) and where the "ceiling" wording gets fixed (point 5). I concede the rest.

1. Hidden successor route across the split (SPLIT-9, Must): CONCEDE.
- This is my own point 6. The evidence stands: +0.020 Gini (SD 0.010) on 9 of 9 splits, and 0.939 against 0.073 on HasKmLimit changes.
- What follows: it is a Must, so it must be fixed before shipping. Under "independent failures are not conflicts", nothing ranked above it excuses it.
- On the remedy, the critic prefers widening the component and I named the per-fold filter as the narrower option. Both are "fix the definition" on the remedy ladder, and both keep the dataset.
- I accept widening as the first choice, for three reasons:
  - It follows Andrej's "most conservative key" call of 2026-11-03 (treat like cases alike).
  - It also moves the successors into test, where point 2's protocol line covers them.
  - The filter would leave the same links among test rows with no group to hold them.
- The curator marks it, because it reopens issue 1's key.

2. The LEAK-9 protocol line understates the route: CONCEDE.
- I proposed the same wording in my point 5: "+0.26 to +0.44, depending on what is read".
- I also accept the critic's addition: say that the successor can be found from the features without the group id (length_to_year_end minus Exposure, LicAge advanced). It tells the benchmark operator what to look for.
- The remedy stays a note under LEAK-9 (Should). The critic agrees that a re-split would select rows by contract changes (LEAK-41).

3. Issue 7, B against C: PARTLY DISPUTE.
- I concede three things:
  - Keeping A as shipped needs either an exception with a fact that sets frempl apart, or a change. The precedent checker found no such fact.
  - The consistency prompt belongs in issue 7.
  - C is the only option that satisfies every reading of the rule texts.
- I dispute that B "may break the Must". Read in context, LEAK-41's sentence "A part known at the start ships as its own column (LEAK-7, LEAK-37)" keeps the legitimate part from being thrown out with the leak. It does not force every start-known column to stay a feature. Three things support this reading:
  - The rule's own Mechanisms row, which names frempl, says the start-known length "may stay a feature".
  - The same rule says a feature known at the start that predicts the weight "stays (USE-6)". USE-6 makes an input legitimate, not required (column auditor; precedent checker on USE-6).
  - Lennart amended CLEAN-16 the same day, and it names "drop the feature" as a remedy. A reading under which the curator's two same-day texts conflict is the less likely one.
- Rule text outranks a Mechanisms row. If the curator reads the sentence as a directive, C wins and I accept it.
- On the evidence, B costs less:
  - Under C, L2 scores 0.159, "led by the tail" (11.6 million per year).
  - Under C, it overturns Andrej's per-table scale call of 2026-11-02.
  - Under B, L2 and Tweedie score alike (0.185, 0.179), and the only cost is +0.005 (SE 0.004) to Tweedie.
  - The practitioner calls L "a calendar-cut artefact, not a rating factor".
- What follows: this is a curator call on how to read LEAK-41, which is option d of the precedent checker's prompt. I recommend B with one recorded line that the sentence permits the column, and C if Lennart reads it as a directive. Either way it is a definition fix that keeps the dataset.

4. One claim decides a fold (P6): CONCEDE as notes.
- The evidence stands:
  - capping at 50,000 moves fold 0 from 0.210 to 0.147;
  - random orders spread with an SD of 0.037;
  - a random column spreads Tweedie by about 0.04.
- What follows:
  - The notes state that model comparisons need paired fold differences, and give the fold SD.
  - The large-loss cap is measured on the shipped splits and offered to the curator as an option, not applied now.
- Under TP-2 (Should) a small real signal is no reason to retire, and the critic agrees. The metric stays as declared until that measurement exists. The Tweedie deviance alternative already fails here (worse than a flat rate on 3 of 3 folds; practitioner, Q5).

5. "1/Exposure alone, the ceiling a leak would reach" is refuted: CONCEDE the fact, DISPUTE where the fix goes.
- The fact: Exposure as a feature reaches 0.256 to 0.259, about 0.07 above 1/E's 0.184 (claim audit, row 13; EV-2).
- The dataset did not invent the word. LEAK-41 (Must) itself says the definition "states the score of 1/weight alone as the ceiling a leak would reach". If the dataset texts alone drop the word, they depart from the rule's wording while the rule still prescribes it.
- What follows: two changes, both cheap.
  - The dataset's texts keep the 1/E figure and add the measured one: "1/Exposure alone scores 0.184, as much as the honest model; with the features the realized length reaches 0.256".
  - The word "ceiling" in LEAK-41, probe 22 and the LEAK-41 Cases text (0.176, now 0.183) goes to Lennart as an amendment ("Maintenance of the rules: an amendment"). The critic agrees that it is not an edit for the dataset agent.
- Nothing in the decision changes, because LEAK-41 decides by timing.

6. Recording gaps: CONCEDE all three.
- One CC line from Lennart that confirms the unrounded length and names both Andrej calls it supersedes (the issue-2 month rounding of 2026-11-02, and issue 4 of 2026-11-03). Until he marks it, the "Resolved (Lennart)" block must show the rounding clause as the AI's call, pending ("Who decides").
- One clause in the length bullet saying that the start date ships as length_to_year_end (366 values). It is moot under B.
- None of the three affects validity. The column audit shows the unrounded column carries no realized decimals.

On the critic's dropped points: I agree with all four. They match my points 1, 3 and 5:
- Exposure and ends_early as features are already forbidden by LEAK-41 and MET-15.
- No rule requires merging a policy-year into one row.
- The file indicator is covered by settled issue 3.
- The negatives are already noted.

Agreed judgment for the mediator: ship after changes.
- Validity: SPLIT-9 is triggered by finding A; fix it by widening the key (curator mark). LEAK-9 is covered by the protocol line, with the size restated and the feature-only route named. LEAK-41, MET-15, USE-6, PROV-7/8/9 and SPLIT-8 hold.
- Value: TP-2, a small real signal, with notes on fold noise and a cap to measure. TP-4 holds.
- Quality: CLEAN-16, issue 7, B (or C if LEAK-41 is read as a directive), plus the text and CC fixes.
- For the curator: issue 7 and the LEAK-41 reading, the widened key, the "ceiling" amendment, and the CC line.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: frempl_french_motor_personal_line (exposure re-review, full tier, 2026-11-06)**

We agree on the verdict: ship after changes. Two disputes are left, both about which remedy to take: issue 7 (B against C) and the key for finding A. I concede everything else. No new points.

Point by point:

1. D9's target, weight and metric (advocate 1): concede. The claim audit holds on every D9 claim: the round trip, the weight wiring, the scorer within 4e-12 of an independent Gini, and a constant scoring 0. The deviance alternative fails on this table (the practitioner, Q5: worse than a flat rate on 3 of 3 folds). I did not argue otherwise.

2. length_to_year_end is known at the start (advocate 2): concede. One value per start day, R² 0.003 without it, and a negative weight-mediated gain in both arms of probe 22. The open question about this column is issue 7, not P4.

3. Data and grouped split (advocate 3): concede. The blind reviewer independently reproduced the target, the row count and the claim count.

4. Value (advocate 4): concede. This matches my point 4. TP-2 and TP-4 hold. The noise and the large claims call for a note (paired fold differences) and a measured cap offered as an option, not an exclusion.

5. The successor route under LEAK-9 (advocate 5): concede. The advocate accepts the restated figure, "+0.26 to +0.44 depending on what is read", which is all my point 2 asked. I also dropped gamer exploits 2 and 3 and the policy-year merge, for the same reasons. One addition, from the evidence already on file: the protocol line should also say that the successor can be found without the group id (task gamer: 39% of rows linked through the length to 31 December minus Exposure and LicAge plus 12*Exposure, 99.7% of them within one group). An operator checking a model for the route must know that dropping policy_component does not block it.

6. Finding A, SPLIT-9 Must (advocate 6): the problem is conceded on both sides. I dispute the remedy order only.
- The advocate leads with (i), the per-fold filter, as the mildest. On the remedy ladder (principles.md) both options are "fix the definition" (a filter and a re-split stand on the same rung), so mildness does not decide between them.
- "Treat like cases alike" does decide. On 2026-11-03 Andrej resolved issue 1 for the cross-file component over the exact chain: the more conservative key, with about 1% chance links accepted. Widening the key with the one-column links (ii) applies that same choice to the same mechanism.
  - The measured cost is inside the noise: 0.1686 against 0.1742, fold SD about 0.03.
  - The lookup gain falls to -0.0045 (4 of 9).
- (i) leaves the splits with per-fold holes that depend on the test fold and hides the policy link instead of encoding it in the group column. Any later re-split would have to repeat it.
- Remedy asked: (ii). (i) is acceptable if the curator prefers to keep issue 1's key unchanged. Either meets SPLIT-9, and either needs the curator's mark.

7. Issue 7 (advocate 7): disputed. The advocate picks B (drop L), reading LEAK-41's sentence "a part known at the start ships as its own column" as a permission because the Mechanisms row says the length "may stay a feature".
- The rule outranks the table row. Principles.md, "Conflicts between rules": rules win over patterns and precedents. The Mechanisms row is a Cases-table entry, so it cannot narrow the text of LEAK-41 (Must). The rule's sentence is written as a directive ("ships as"). Read as written, B breaks a P4 Must to meet a P7 Should, which principles.md step 4 and the Should definition forbid ("only a higher-ranked Must overrides" a Must).
- C meets every rule text: CLEAN-16 names "ship the identity scale" as its second remedy, and LEAK-41's sentence is kept. C also follows the nearest precedent with the same facts, pricing_game_2016_french_fleet (Lennart, 2026-11-06: identity scale, start-known length kept). The precedent checker found no fact that sets frempl apart.
- B has no applied precedent: spanish dropped `total_exposure` as a hybrid under LEAK-41, not a start-known length under CLEAN-16.
- The advocate's practitioner quote ("not a rating factor") is a weighing argument. USE-6 makes the column a legitimate input, and the precedent checker notes the tension row "a model's input cap is never an argument" for dropping a legitimate input because of one loss family.
- C's cost: L2 on the identity scale scores 0.159, led by the tail (claim audit, issue 7). Tweedie is unaffected (0.183).
- Remedy asked: C. B only if Lennart records that LEAK-41's sentence is a permission, as an amendment of LEAK-41's wording, so the next table is decided the same way (principles.md, "Consistent judgement", case 1: a call that would break a higher Must is offered as an amendment, not an exception). Agreed with the advocate: shipping A as it stands needs a recorded exception, and none is supported.

Text fixes (advocate 7, list): concede, with two corrections.
- The negatives are already noted (claim audit row 23: "967 negatives set to 0" holds in the notes). That item is a check, not a change.
- The advocate's list leaves out the flag to the curator: the "ceiling" wording also sits in LEAK-41's own text and in probe 22's output line, and LEAK-41's Cases text still quotes the honest model at 0.176 (D9: 0.183). Rewording only the dataset's texts leaves the rule stating a refuted bound (claim audit, refuted claim 13: 0.256 to 0.259 with the realized length as a feature, against 1/E's 0.184). Remedy: flag both as an amendment for the curator. The dataset agent does not edit the rule.

Judgment I support:
- Verdict: ship after changes.
- Validity:
  - SPLIT-9 triggered by finding A, fixed by widening the component (ii), or by filter (i), on the curator's mark;
  - LEAK-9 covered by the protocol line, its figure restated to +0.26 to +0.44, plus that the route works without the group id;
  - LEAK-41, MET-15, USE-6 and PROV hold.
- Value: TP-2, TP-4; a note on paired fold comparisons and a measured cap offered as an option.
- Quality: issue 7, C (B only with a LEAK-41 amendment).
- Text: the "ceiling" reworded in the dataset's texts and flagged in the rule; Lennart's CC to confirm the unrounded length and name both superseded calls of Andrej; the start-date recoding stated.

</details>
