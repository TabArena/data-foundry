# australian_vehicle_insurance_2004_2005

**Outcome:** added. The AI recommends shipping it; the panel's changes to the text are made (below), and the forced
split, `exposure` and the target scale are settled (2026-11-02). The "Car" table of de Jong and Heller (2008) from the R
package insuranceData (CASdatasets holds the same rows): 67,856 one-year Australian vehicle policies of 2004-2005,
target the claim cost of the part of the policy's year the data observed (0 for 93.2%), six rating factors and the
observed time, random 3x3 split tagged forced from temporal, scored by the normalized Gini as a context metric.
Validity: USE-1 holds (pricing a policy at underwriting, "for example"); USE-3 and USE-8 were wrong in the text (the
observed time was called the contracted term and listed as a gap), now reworded; LEAK-10 is triggered by `exposure`,
which some claims cut short, and it is kept on your call of 2026-11-02 (a LEAK-10 case: the cut cannot be located, and
that part lowers the score); SPLIT-8 holds, the split shipped on your call of 2026-11-02 (a forced IID split ships when
the leak test across the random split finds none; SPLIT-8 amended); PROV-4 holds (the book's Table 1.1, CASdatasets row
by row); PROV-16 was broken by claims about the book's later chapters taken from section titles; corrected from
the pages Andrej read (issue 3, resolved). Value: TP-2, a small real signal (every model family beats a
constant on 9 of 9 splits);
TP-4 holds (a GLM beats the observed time alone on 8 of 9); MET-11, the Gini as a context
metric, is open for the insurance tables (issue 4). Quality: the 53 vehicle values of 0 made missing (CLEAN-10,
CLEAN-11); the claim costs at 200 kept as recorded, as fremtpl2's fixed amounts; the target is in dollars while
CLEAN-16's default and most sibling tables use log1p, kept as implemented on your call of 2026-11-02. Weighed: a
documented textbook table +, a real pricing task +, few coarse rating factors -, the observed time alone earns 82% of
the best score -. Left for Andrej: none (issues 3 and 4 resolved 2026-11-02).

Changes made after the review panel (AI, 2026-11-01), text only (rows, split and metric unchanged): `exposure` is
described as the share of the year observed, cut short after some claims, and named in `fit_reason` as a kept leak;
the split note gives the one observation period and the file-order check; the metric reason cites Ye et al. (2022) and
describes Frees et al. and Allstate as they are; the book's later sections are marked unverified; the duplicates and
200-floor notes give their baselines and precedent; `driver_gender` is renamed `gender`.

**Main points:** All issues are resolved: the Gini confirmed for this table (4), the book's claims corrected (3).

**Issues for Andrej:**

3. **Can you get de Jong and Heller (2008)?** Only the book's first chapter and its contents were read; its companion
   website and the Internet Archive were offline on 2026-11-01. The notes' statements on what the book does with this
   table (logistic regression with an exposure correction, Sec. 7.3-7.4; Tweedie and zero-adjusted inverse Gaussian
   models, Sec. 8.3, 10.4-10.5; no held-out score) come from section titles, so they are now marked unverified
   (PROV-16, PROV-17, Must).
   * What the text would settle: whether the book scores held-out predictions by one measure (then the metric's origin
     changes, MET-5, issue 4); how its p. 15 defines `exposure`, the area and the cover (third party per CASdatasets,
     comprehensive per another R package), which bears on issue 2; whether it models the raw cost (issue 5).

   * Implemented: the claims marked unverified (PROV-17). Nothing in the rows or the split rests on them, and the
     metric's context origin also rests on Ye et al. (2022), who report five measures. Alternative: the pages, which
     could change the metric's origin (issue 4) and the reading of `exposure` (issue 2).

   Recommendation: send the pages if you can reach the book; otherwise leave the claims marked unverified. Decision:
   send the PDF (Sec. 7.3-7.4, 8.3, 10.4-10.5 and p. 15), or leave the claims marked unverified?

   **Andrej (2026-11-02, discuss):** Here is a readable copy:
   https://www.scribd.com/doc/66265471/0521879140-Generalized-Linear-Models-for-Insurance-Data

   **Answer (AI, 2026-11-02):** The link does not open for the AI: Scribd builds the page in the browser, a fetch
   returns only its loading error, and a direct download was stopped as getting around the site's bot check. The
   upload is a third party's copy of the Cambridge book, so it does not go into `source_links`; the record keeps the
   publisher's citation (PROV-8). The claims stay marked unverified until the pages are here: paste the text of
   p. 15 and Sec. 7.3-7.4, 8.3 and 10.4-10.5, or save a PDF in the worktree, and the AI checks them against issues 2,
   4 and 5.

   **Andrej (2026-11-02, discuss):** I accessed the extracted text of de Jong and Heller (2008) through this readable
   copy (printed page numbers; OCR damages some equations). pp. 15-16, Table 1.6: confirms 67,856 policies and 4,624
   with claims; area denotes residence, A-F remain unexplained; the table labels age as policyholder age. Sec. 7.3-7.4,
   pp. 99-104: logistic regression for claim occurrence, exposure (time at risk) in a modified link; these passages do
   not establish why individual exposures end early. Sec. 7.6, pp. 108-110: ROC AUC 0.662 with the exposure adjustment
   against 0.548 without, for classification, no held-out split described. Sec. 8.3, pp. 127-128: Tweedie models
   explained, no fitted example for this dataset. Sec. 10.4, pp. 145-148: a zero-adjusted inverse Gaussian model of
   claim amounts including zeros, selected by AIC; log links do not imply a log-transformed target. Sec. 10.5, pp.
   148-149: a multiple-claim model, not fitted here. The passages do not establish normalized Gini as a source metric or
   resolve the $200 floor, paid-versus-incurred costs, or claim-triggered termination. Please correct the earlier book
   claims accordingly. Replace "the book defines no metric" with the narrower statement that no source metric for our
   claim-cost regression benchmark was established. Keep Gini's justification separate from the book's classification
   AUC results.

   **Answer (AI, 2026-11-02):** Corrected in the definition, with your page references: the source note now says what
   the book does with this table (Table 1.6; the logistic model with exposure in the link, Sec. 7.3-7.4; ROC AUC 0.662
   against 0.548 for claim occurrence on the same data, Sec. 7.6; the zero-adjusted inverse Gaussian claim-amount model
   chosen by AIC on the raw amount, Sec. 10.4; Tweedie and multiple-claim models explained without a fit, Sec. 8.3 and
   10.5) and what it leaves open (early exposure ends, paid or incurred costs, the 200 floor). `area` cites Table 1.6
   (residence, A-F unexplained); the age band keeps its name, with Table 1.1's "driver's age category" and Table 1.6's
   policyholder age both noted. The metric reason now reads "no source metric for this claim-cost regression was
   established"; the book's AUC is named only as a classification measure that does not support the Gini, whose case
   rests on Ye et al. (2022) and pricing practice. `dataset check`: 0 errors, 0 warnings. A Cases row is not needed: no
   rule changes.

   **Resolved (2026-11-02, Andrej):** the book was read from the pages you supplied; the claims are corrected, not
   marked unverified. The 200 floor, paid or incurred costs and why exposures end early stay open in the notes.

4. **Confirm the normalized Gini for the four insurance tables that declare it as a context metric, and drop the `rmse`
   fallback?** The normalized Gini scores how well the predictions order the policies by claim cost (1 a perfect order,
   0 a random one); it ignores the price level, which an insurer sets separately. No source metric for this claim-cost
   regression was established (the book selects its claim-amount model by AIC with no held-out score; the R packages
   define none), so it is declared as a context metric, one chosen from the domain's practice because the source
   names none (MET-11, Must); frempl_french_motor_personal_line, spanish_motor_insurance_coverage_level_2022_2024 and
   spanish_motor_insurance_2015_2018 declare the same; pricing_game_2017_french_mtpl declares it as a stand-in, and
   wisconsin_local_government_property_insurance_fund now declares its source's Gini against the fund's premium
   (`ordered_lorenz_gini`, Metric.source). The record still offers `rmse` "if the
   curator prefers the default". No curator has yet confirmed a context ranking metric on a regression target.
   * With `rmse`: the best model explains 0.2% of the variance, the 46 largest claims (0.07% of policies) hold 43% of
     the squared error, and common learners lose to a constant, so it would rank models by how far they shrink toward
     the mean. The blind reviewer, who assumed it, would leave the dataset out.
   * With the Gini: every model family beats a constant on 9 of 9 splits, and the five real models come out in the
     same order as on the pricing actuary's own measure (the Gini of the cost per policy-year, weighted by the observed
     time; mean rank agreement 0.64). Its weak point: the observed time alone (0.168) beats squared-error boosting on
     6 of 9 splits.
   * Support: Ye et al. (2022, Econometrics 10(2):19) scored this table with this Gini on a random split, among five
     measures; Allstate chose it for its claim challenge, on full vehicle-years. The advocate and the critic both keep
     the Gini.
   * Implemented: the normalized Gini (context), its reason rewritten. Alternatives: `rmse`, the fallback; the
     actuary's weighted Gini on the cost per year, which needs a training weight and, with the time as a feature,
     rewards the policies cut short (0.238, above every honest model). Or claim occurrence as a binary target, the
     blind reviewer's proposal (ROC AUC 0.654), which drops the claim size the insurer prices.

   * pricing_game_2017_french_mtpl issue 2 recommends the Tweedie deviance over the Gini for its stand-in, measured
     against the game's simulated profit; the four tables here have no original to measure against.

   Recommendation: confirm the Gini for the four and strike the fallback. Decision: Gini or `rmse`, for the four
   tables?

   **Andrej (2026-11-02, ok):** Use Gini

   **Resolved (2026-11-02, Andrej):** the normalized Gini as a context metric, decided for this table (MET-10 as amended
   2026-11-02: no family call on the metric); the screening's `rmse` fallback is struck in the record. The four tables
   named above decide their own metric.

**Review panel:** ship after changes (mediator). Claim audit: 37 claims, 30 hold, 5 refuted (all fixed in the
text), 2 untested (whether the costs are paid or incurred; the book's later sections). Blind review: exclude as
prepared, assuming RMSE on the raw cost; it proposes claim occurrence as a binary target, or a deviance or a normalized
Gini to keep the regression; the Gini is what ships (issue 4). Debate: agreed on keeping `exposure` with a rewritten note, the Gini and the text
fixes; disputed: whether a fact sets the forced split apart from how_much_did_it_rain (issue 1), and the target scale
(issue 5); settled by the mediator: fremtpl2 counts for the practice (a feature, not a divisor), not as the same facts
(issue 2).

<details><summary>Mediator</summary>

**Mediator (2026-11-01): australian_vehicle_insurance_2004_2005**

**Recommendation**

```text
Verdict: ship after changes (text of dataset.py and the record; rows, split and metric formula unchanged).
Validity: SEL holds (CC Yes, priority 5); USE-1 holds (pricing at underwriting, "for example"); USE-3 broken in the
  text (exposure called the contracted term), fixed by rewording; USE-5/USE-8 fit approximate, gaps renamed (forced
  split, cost of the observed part of the year, undocumented label); LEAK-10 triggered for `exposure` (cut short after
  some claims), kept under LEAK-11 (the traced late part lowers the Gini: 0.182 to 0.31 with counterfactual exposure,
  18 of 18 runs; offset-only 0.1833 against 0.1824 free), note rewritten, curator confirms (issue 2); `clm`,
  `numclaims` dropped (LEAK-10); LEAK-18 holds with a corrected note; LEAK-24 cannot be verified, not blocking;
  SPLIT-8 holds as written, note corrected, consistency check against how_much_did_it_rain open (issue 1); PROV-4
  holds; PROV-16 not met for the book's later sections, marked unverified (PROV-17), book requested (issue 3).
Value: TP-2 small real signal (every family beats the dummy Gini on 9 of 9); TP-4 not trivial (GLM beats exposure
  alone on 8 of 9, +0.038, SE 0.010); MET-11 context Gini kept with its reason rewritten, curator confirms for the
  insurance family (issue 4).
Quality: CLEAN-10/11 hold (53 vehicle values of 0 made missing); 200 floor kept as recorded (fremtpl2's point
  masses); names fixed (`gender`, area code); raw or log1p target open (issue 5, MET-3, CLEAN-16).
Weighed: source + (textbook table, two copies agree row by row), real pricing task +, few coarse rating factors -,
  exposure alone earns 82% of the best score -.
For the curator: issue 1 (forced IID, consistency check), issue 2 (exposure keep), issue 3 (the book), issue 4 (Gini
  for the insurance family), issue 5 (target scale for the family).
```

The advocate and the critic reach the same verdict. No point is a Must that cannot be fixed. Exclusion is possible
only if the curator applies his how_much_did_it_rain standard to this split (issue 1, option b).

**Changes to make now (no decision needed)**

1. Prediction-point bullet and `task_summary.known` (USE-3): every policy is a one-year contract; `exposure` is the
   share of that year observed in the data (1 to 365 days, median 163, 1.9% full years), known at the end of the
   observation period and cut short after some claims. Suggested `known` ending: "and the share of the policy's year
   observed in the data (a full year for 1.9%; it can end early after a claim)".
2. "Potential leak, kept on purpose" bullet and the second Decision's text (LEAK-10, LEAK-11): the column is mostly
   the observation window; the shortening shows in claim occurrence (147 excess claims at 0.2 years or less; 0.85
   claims per policy-year at 7 days or less even without the claims at 80% of the vehicle's value or more; a free
   log-exposure coefficient of 0.29-0.31 where proportional time gives 1) and in size (193 write-offs, median exposure
   0.37 against 0.65). Kept under LEAK-11 because the traced part lowers the score: exposure as an offset only 0.1833
   against 0.1824 as a free feature (paired SE 0.0059, 9 splits), floored at 0.1 years 0.1849; the write-offs given a
   counterfactual exposure lift the Gini from 0.182 to 0.31 (18 of 18 runs). Cite fremtpl2 for the practice (a
   feature, not a divisor), not as the same facts: its reason "the contracted period is known at pricing" does not
   carry. Replace "The claim size adds nothing to the Gini" in the Decision text. Revisit if a release gives the policy
   dates or why a policy ended.
3. `fit_reason` (USE-8; kick, homesite_quote_conversion): name `exposure` as a kept potential leak, not a gap. Gaps: a
   random split of undated policies; the target is the cost of the observed part of the year, not the cost per
   policy-year the insurer prices; the label's construction is undocumented (paid or incurred, the 200 floor, the
   repeated amounts, the cover).
4. Split bullet and `task_summary.split` (SPLIT-8): replace "a split by year would test a model on a later year's
   portfolio and claim level" with: the release looks like one observation period of about a year (exposure spread
   evenly over 1-365 days, 1.9% full years, no 366-day row), so a temporal test needs another year's extract; the raw
   file order is not random (12.2% of adjacent rows share a day count, 0.3% shuffled), but the claim indicator shows no
   serial dependence and a forward holdout over file quarters shows no drop (Tweedie LightGBM 0.168, 0.189, 0.208
   against 0.127, 0.174, 0.181 random; single splits; whether the order is time is unknown). Do not write "shuffled".
   In `split`, "the same portfolio and years" becomes "the same portfolio and period".
5. Metric reason and `changes` (MET-11, PROV-16): cite Ye et al. (2022, Econometrics 10(2):19), who scored this table
   with this unweighted normalized Gini on a random split with exposure among the inputs, next to four other measures
   (so the origin stays context, MET-5), with a section reference from the text read; describe Frees, Meyers and
   Cummings (2011) and CAS Monograph 5 (Sec. 7.2.4) as the premium- or exposure-weighted form on the rate; cite
   Allstate with its difference (full vehicle-years there; 98.1% of rows here are shorter); state the exposure-alone
   baseline (0.168, 9 splits). In `changes`, replace "the insurers' ranking metric" with a plain description.
6. Book claims (PROV-16, PROV-17): mark the statements about Sec. 7.3-7.4, 8.3, 10.4-10.5 and "scores no held-out
   prediction" as unverified (contents only); "5,742 to 6,547 policies per band" becomes "5,742 to 16,189 policies per
   band (5,742 in the youngest, 6,547 in the oldest)".
7. Duplicates bullet (LEAK-18): replace "plausible ... natural" with the chance baseline (378 copies against 120-125
   with exposure shuffled; 152 against 11.6 among the full-year rows, which are rich in trucks and panel vans, likely
   fleet vehicles insured on the same dates), all without a claim; dropping them moves the Gini by +0.0045 and a split
   grouped on the feature vector scores within noise; kept.
8. Names (CLEAN-1): rename `driver_gender` to `gender` (insuranceData: "gender"; CASdatasets: the policyholder's); in
   `known`, "the area of residence" becomes "an area code A-F (its meaning is not documented in the sources read)";
   in `row`, "private car policy" becomes "vehicle policy" (1,750 trucks, 48 buses, 127 motor caravans; the Rd says
   "vehicle insurance policies").
9. 200 floor bullet: drop "for the curator to confirm" and cite fremtpl2, whose fixed IRSA-IDA amounts stay in the
   target as point masses (CC 2026-10-20, Andrej): the same kind of fact, so the precedent is followed.
10. `accepted_check_warnings = {"task_target_value_dominant": ...}` with the reason: zero-inflated by nature, 0 for
    exactly the 63,232 policies without a claim, not a cap or placeholder (claim audit #29 holds).
11. Optional (CLEAN-1, cheap and safe): round `claim_cost` to cents (1,925 positive costs carry float noise up to
    $0.005); the floor then counts 705 exactly and the "695 exactly" wording goes.
12. Record: an `Assessment (AI, 2026-11-01)` line that replaces the 2026-10-30 reading of exposure ("the contracted
    period is known when the policy is priced") and the screening's "Regime IID" with the measured readings. The
    `rmse` fallback stays in the record until issue 4 is decided.

**Issues for the curator, ranked**

1. **Forced IID against how_much_did_it_rain** (P4, SPLIT-8, Must; consistency check cases 2 and 3).
   * Problem: pricing is temporal by its use case; the release has no dates or ids, so SPLIT-8 ships it as IID tagged
     `ForcedIIDFromTemporal`. On 2026-10-30 Andrej sent how_much_did_it_rain to `No` ("if the data is temporal but a
     temporal split is not possible, we cannot split the data and reject it") and said "Forced IID is to be avoided at
     all costs"; SPLIT-8 was left unchanged. His `Yes` here was given on a record that read "Regime IID".
   * Effect: test policies come from the same observation period; a change of mix or relativities in a later year is
     not tested (a level shift would not move the Gini). The cost cannot be measured: one period, no dates.
   * Advocate: the distinguishing fact is measured: distinct policies, hidden-group probe 0 hits, no renewal pairs (116
     at 365 days against a mean of 102), a split grouped on the feature vector within noise (0.194, 0.208 against
     0.182, 0.205), forward file-quarter holdout with no drop. how_much_did_it_rain's `No` named a leak channel
     (storm-correlated hours on both sides) that does not exist here. Rules win over precedents; a reject would be an
     amendment reaching 17 datasets and frempl.
   * Critic: agrees with the facts and the remedy; the `Yes` does not settle the reframed split, so the fact must be
     written and put to Andrej.
   * Decision: (a) record the fact and ship; (b) `No`, like how_much_did_it_rain (frempl would follow); (c) reopen
     how_much_did_it_rain under SPLIT-8; (d) amend SPLIT-8. Recommendation: (a).
2. **Keep `exposure` as a feature on its corrected reading** (P4, LEAK-10 Must, kept under LEAK-11 Should).
   * Problem: the record's suggestion of 2026-10-30, seen by Andrej, called it the contracted period known at
     pricing. It is the observed share of a one-year contract, and some claims cut it short.
   * Effect: at a real quote it is 1 for every policy; here it alone earns 0.168 of the best 0.205. The part cut short
     after a claim lowers the score (change 2 above).
   * Both sides: keep with the rewritten note; the advocate leans on fremtpl2, the critic on LEAK-11 and the
     difference from heart_failure `time`.
   * Alternatives: drop (best Gini 0.205 to 0.130; Tweedie LightGBM 0.182 to 0.089); or the cost per policy-year with
     exposure as the metric's weight, which needs a training weight Data Foundry lacks (one claim on a one-day slice
     is worth up to $5.2M a year unweighted) and is a family item.
   * Decision: keep or drop. Recommendation: keep.
3. **The book** (P5, PROV-16 and PROV-17, Must). Only chapter 1 and the contents of de Jong and Heller (2008) were
   read; the companion site and the Internet Archive are offline. The text would settle whether the book scores
   held-out predictions by one measure (MET-5, issue 4), how p. 15 defines `exposure`, the area and the cover (issue
   2), and whether it models the raw cost (issue 5). Decision: supply the PDF (Sec. 7.3-7.4, 8.3, 10.4-10.5, p. 15),
   or leave the claims marked unverified.
4. **Normalized Gini as a context metric for the insurance family** (P6, MET-11 Must; MET-1, MET-2).
   * Problem: no source metric; the record still offers the `rmse` fallback; first context ranking metric on a
     regression target; frempl and spanish declare the same.
   * Effect: under `rmse` the best R^2 is 0.002 (in-sample ceiling 0.0037), 46 claims hold 43% of the squared error,
     squared-error and Huber LightGBM lose to the mean: it ranks shrinkage (the blind reviewer's "exclude" assumed
     it). Under the Gini every family beats the dummy 9 of 9 and the real models keep the actuary's quote-measure
     order (mean Kendall tau 0.64), but exposure alone (0.168) beats squared-error LightGBM on 6 of 9 splits.
   * Both sides: the Gini, strike `rmse`. The practitioner's exposure-weighted Gini on the rate is not workable here
     (no training weight; with exposure a feature it rewards the cut-short policies, 0.238).
   * Decision: Gini or `rmse`, once for the three tables. Recommendation: the Gini.
5. **Raw dollars or log1p** (P7, CLEAN-16 Should; MET-3 Must allows either; consistency check case 2).
   * Problem: this table ships dollars; frempl and spanish ship log1p with the Gini on the amount; no reason recorded.
   * Effect: the Gini is on dollars either way; log1p lifts squared-error LightGBM by +0.028 to +0.034 (7 to 9 of 9),
     from below the exposure-alone baseline to above it. The best model (Tweedie GLM, 0.205) fits dollars.
   * Advocate: dollars, the actuarial modelling scale (CAS Monograph 5, Sec. 2.7.3: Tweedie on dollars of loss).
     Column auditor: log1p, for the family. Critic: either, decided once for the three with the reason recorded.
   * Decision: one scale for the three. Recommendation: decide it once; log1p follows CLEAN-16's default and the
     siblings, dollars needs the Tweedie practice recorded as the reason.

**Disputed points**

| Point | Advocate | Critic | Rule and rank | Settled |
|---|---|---|---|---|
| Which rule keeps `exposure`; fremtpl2 as a like case | LEAK-10 second clause and LEAK-11; fremtpl2 alike (its second reason carries) | LEAK-11 only; fremtpl2's reason does not carry; heart_failure the closest mechanism | LEAK-11 (Should, narrows LEAK-10, so it wins within its scope). LEAK-10's second clause covers values read at a later pull, not a time on risk cut by the outcome | Critic on the rule and the wording: the note cites LEAK-11 and the fact that sets it apart from heart_failure (the traced part lowers the score). Advocate on the practice: fremtpl2's "dividing would inflate short policies' targets" carries. Not an independent failure: LEAK-10 is met through LEAK-11's narrowing. Remedy: keep with a note (issue 2 to confirm, since the reading the curator saw was wrong) |
| Does the CC `Yes` settle the split and the exposure keep? | yes, it outranks AI readings | no: given on "Regime IID" and the wrong exposure reading | "Stages": a later measured finding supersedes a screening reading; the CC settles what it decided | Critic: the `Yes` settles scope and priority, not the framing (issues 1, 2) |
| Is there a fact that sets the forced split apart? | yes, measured | the facts hold; only the curator can say they meet "at all costs" | SPLIT-8 Must holds; a precedent binds only on the same facts (how_much_did_it_rain's reason was a leak channel) | Not mine to settle: consistency check, issue 1, recommendation (a) |
| Raw file order shuffled? (fact) | withdrew "the cost cannot be measured" | not shuffled | EV-1, decisive experiment | Critic. Raw `dataCar.csv`: 12.2% of adjacent rows share a day count (0.3% shuffled), lag-1 exposure 0.094, claim indicator lag-1 0.005, claim rate per tenth 6.1-7.3%. The pipeline frame (CLEAN-23 shuffles IID rows): 0.29%, lag-1 -0.008. The split auditor measured the pipeline frame |
| PROV-16 holds? | yes (a slip) | no: section claims from titles | PROV-16, Must, P5 | Critic: mark unverified (PROV-17), request the book (issue 3). The advocate is right that the raw scale and the context origin have other support |
| Allstate as support | same metric | full vehicle-years there | MET-11, Must (name the original accurately) | Critic: cite it with the difference |
| Target scale | dollars | one family call | MET-3 permits both; CLEAN-16 Should, case by case | A weighing call: issue 5 |

The script and output of the decisive experiment are in the run folder.

**Agreed facts**

* The copy is faithful: insuranceData `dataCar` matches all 18 cells of the book's Table 1.1; CASdatasets
  `ausprivauto0405` equals it on 67,856 of 67,856 rows (no area); Rdatasets 0 mismatches; both hashes match; GPL-2.
* 67,856 one-year policies; `claim_cost` is 0 on exactly the 63,232 no-claim rows (93.2%); `clm` and `numclaims` are
  parts of the target; `X_OBSTAT_` is constant; vehicle value is in $10,000s, with 53 zeros.
* No cost below 200; 705 single-claim policies at 200.00 to the cent; two-claim policies start at 400; 27.5% of
  claimants sit on 12 repeated amounts. Paid or incurred, and how developed, is undocumented (LEAK-24 untestable).
* `exposure` is days / 365.25, 1 to 365 days, near uniform, median 163, 1.9% full years, no 366-day row: the observed
  share of a one-year contract, cut short after some claims (147 excess claims at 0.2 years or less; write-offs median
  0.37 against 0.65; free log-exposure coefficient 0.29-0.31 Tweedie, 0.73 Poisson).
* The traced late part brings no gain on the declared metric: offset-only 0.1833 against 0.1824 free (SE 0.0059);
  floored 0.1849; counterfactual write-off exposure lifts the Gini from 0.182 to 0.31-0.32 (18 of 18).
* Scores on the 9 shipped splits: Tweedie GLM 0.205, hurdle 0.191, Tweedie LightGBM 0.182, squared-error LightGBM
  0.163 (0.195-0.197 on log1p), exposure alone 0.168 (GLM beats it 8 of 9); best R^2 0.002; top 46 rows hold 43% of
  the sum of squares.
* On the practitioner's quote measure the five real models keep their order (mean Kendall tau 0.64); exposure alone
  scores about 0 there.
* No date or id; hidden-group probe 0 hits; no renewal pairs; split grouped on the feature vector within noise; 378
  exact copies at about three times chance, all without a claim, dropping them moves the Gini by +0.0045.
* The book was read only to chapter 1 and its contents; the companion site and the Internet Archive are offline.
* Ye et al. (2022) scored this table with the unweighted normalized Gini, a random split and exposure as an input,
  among five measures; Frees et al. (2011) and CAS Monograph 5 use a premium- or exposure-weighted form; Allstate's
  rows are full vehicle-years.

**Consistency with precedent**

* `exposure` as a feature: follows the practice of fremtpl2 (CC 2026-10-20, Andrej), frempl and spanish. Departs from
  heart_failure `time` (dropped); the fact that sets it apart is LEAK-11's (south_africa_coronary_heart_disease): the
  traced late part lowers the score, while `time` carried the signal (ROC AUC 0.90 to 0.75 without it). Once confirmed,
  a Cases row under LEAK-10/LEAK-11 for time exposures in insurance would save the next table the argument.
* Forced IID: follows SPLIT-8 and its cases (account_debt_south_africa, mobile_churn) and the sibling frempl; departs
  from how_much_did_it_rain's CC and Andrej's statement of 2026-10-30, so it is issue 1 with the AI's best guess at the
  distinguishing fact.
* 200 floor: follows fremtpl2's IRSA-IDA point masses (CC) and policy question 2.
* Drops, vehicle value 0 to missing, age bands as numbers: follow fremtpl2, churn_telco_south_asia and CLEAN-14 as
  amended.
* Duplicates: LEAK-18 (sepsis_survival_minimal_clinical_records) followed, with the wording corrected to the measured
  excess.
* `fit_reason`: brought in line with kick, homesite_quote_conversion and house_sales (USE-8).
* Metric: no curator precedent for a context ranking metric on a regression target; issue 4 decides it for the
  family. Scale: departs from frempl and spanish; issue 5.
* No `Exception to` line and no third exception of one reason.

</details>

<details><summary>Claim audit</summary>

**Claim audit (claim-auditor, 2026-11-01): australian_vehicle_insurance_2004_2005**

**Verdict:** I tested 37 claims. 30 hold, 5 are refuted and 2 are untested. Untested parts remain in #13, #14 and #24.
The 5 refutations come down to three findings and one slip of wording: the time in force is called known at pricing
(#5 and #14), the support for the metric (#25), the duplicates called natural (#21), and the band counts (#9). None
needs a change to the data or the split. The first and third change the notes. The second is a question for the
curator about what the metric measures (MET-1, MET-2). The exposure keep is backed by a test that could have gone against it, and that test went
further than the notes do: the part of `exposure` recorded after the outcome lowers the Gini, it does not raise it.

All numbers come from the definition's frame and its 9 shipped splits (3 x 3, seed 4267), loaded with
`dataset_io.from_definition` or `to_container()`. The models are untuned: a Tweedie GLM (statsmodels, log link,
power 1.5) and a Tweedie LightGBM (300 trees, 15 leaves). The raw file is insuranceData's `dataCar` exported to CSV.
Scripts and logs are in the run folder.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Question: what the policy costs the insurer in claims while it is in force | task_summary.question | target against the Rd | holds | `claimcst0` "claim amount (0 if no claim)"; observed period up to 365 days | USE-5 |
| 2 | Use case: an insurer prices a one-year policy at underwriting ("for example"); the source names no decision | use_case | Rd, CASdatasets page, book ch. 1 | holds | no decision in any of them; the "time on risk" part is #14 | USE-1 |
| 3 | Row: one one-year policy taken out in 2004 or 2005, observed up to a year, 67,856 policies, unnamed insurer | row | Rd, counts | holds | Rd: "one-year vehicle insurance policies taken out in 2004 or 2005", 67,856. Note: 98.1% are observed for less than a full year, and "private car" includes 1,750 trucks, 48 buses and 127 motor caravans | PROV |
| 4 | Target: 0 for 93.2%, no claim below $200 | predicted | count on the frame | holds | 63,232 zeros (93.19%); lowest positive 200.00 | - |
| 5 | Known at prediction time: the rating factors and "the share of a year the policy was in force" | known | see #14 | refuted in part | the time in force is not the contracted term, and part of it comes after the outcome | USE-3, LEAK-10 |
| 6 | Split: random policies | split | the container's splits | holds | 3 x 3 IID; 22,618-22,619 test rows per fold | SPLIT-8 |
| 7 | Changes: `clm` and `numclaims` dropped, 53 vehicle values of 0 made missing, scored by "the insurers' ranking metric" | changes | asserts in `_clean`, counts | holds; the metric part as in #25 | both asserts pass; 53 zeros | MET-11 |
| 8 | Fit approximate; fit_reason gives the forced split and "the time in force is known only after the period" as the gaps | fit, fit_reason | USE-8 text | holds; wording | approximate is right because of the forced IID split. USE-8 wants a kept leak named "as kept, not as a gap", and the time in force is a kept potential leak | USE-8 |
| 9 | insuranceData matches the book's Table 1.1: "5,742 to 6,547 policies per band, 4,624 with a claim" | notes, Source | crosstab against book p. 8 | refuted (wording) | all 18 cells match (496/932/1,113/1,104/614/365 claim; totals 5,742/12,875/15,767/16,189/10,736/6,547). The bands hold 5,742 to 16,189 policies: 5,742 and 6,547 are only the youngest and oldest bands | PROV-16 |
| 10 | CASdatasets `ausprivauto0405` agrees on every row, without the area | notes, download | row-by-row comparison | holds | Exposure, VehValue, ClaimNb and ClaimAmount equal on 67,856 of 67,856 rows; body labels, gender and both age bands map one to one; no area column | PROV-4 |
| 11 | The book fits logistic regression with exposure (Sec. 7.3-7.4) and Tweedie and ZAIG models (8.3, 10.4-10.5) to this table, and scores no held-out prediction | notes, Source; metric reason | book contents | untested | the contents give 7.3 as "Application of logistic regression to vehicle insurance" and 7.4 as "Correcting for exposure". The titles of 8.3, 10.4 and 10.5 do not name a data set. The book was not read | PROV-16, EV-7 |
| 12 | Target is 0 on exactly the 63,232 no-claim policies; `clm` and `numclaims` > 0 on the same rows; `X_OBSTAT_` constant | notes, Target | asserts, counts | holds | asserts pass; `X_OBSTAT_` has 1 value | LEAK-10 |
| 13 | Floor at 200: 705 of 4,333 single-claim policies at 200.00 to the cent (695 exactly); no multi-claim policy at 200; two-claim policies start at 400 (10 of 271 at 400.00, one at 400.01); point masses 353.77 x 219, 389.95 x 94, 390 x 55 | notes, Anomaly; Decision 1 | recount on raw | holds | every number reproduced exactly. That each claim is recorded at 200 or more is a reading of the data, not a stated rule | - |
| 14 | `exposure` is days / 365.25, a full year 0.9993, mean 0.47; "the period the policy is on risk [is] known" at pricing (notes, Prediction point); "the contracted period is known when the policy is priced" (record, Assessment 2026-10-30) | notes; record | source text; exposure distribution; claim rate per year by exposure decile; GLM with free log(exposure) | first part holds; "contracted period" refuted | day counts are whole numbers on every row, maximum 365 days. But every policy is a one-year contract (Rd), and 98.1% of rows fall short of a full year, almost uniformly (quartiles 0.22, 0.45, 0.71): this is time inside an extract window, not the contract term. Claims per year of exposure are 0.40 and 0.23 in the two shortest tenths against 0.14-0.17 in the rest, and still 0.33 and 0.20 with the write-offs removed. The free coefficient on log(exposure) is 0.29, where a proportional offset would be 1 | USE-3, LEAK-10 |
| 15 | Exposure alone: ROC AUC 0.65 for a claim, 82% of the best Gini (0.168 against the Tweedie GLM's 0.205, which wins on 8 of 9 splits) | notes, Potential leak | container scorer on 9 folds; GLM refit | holds | exposure alone 0.1675 (0.137-0.200), AUC 0.653; GLM 0.2050 | TP-4 |
| 16 | The 193 claims of at least 80% of the vehicle value have median exposure 0.37 against 0.65 (Mann-Whitney p < 1e-20) | notes; Decision 2 | recompute | holds | 0.370 against 0.646, p = 4.2e-21. Six claimants with vehicle value 0 are excluded, as in the Decision table | LEAK-10 |
| 17 | "The claim size adds nothing to the Gini ... so the late part shows no gain in the metric" | notes, Potential leak | (i) exposure as a proportional offset against a free effect; (ii) the write-offs given a counterfactual exposure, never below the observed one, in train and test | holds, and more strongly than the notes say | (i) free minus offset: GLM +0.005 (paired SE 0.007, 6 of 9), LightGBM +0.002 (SE 0.005, 4 of 9). (ii) Gini 0.182 rises to 0.31-0.32 on 18 of 18 runs, and exposure alone rises from 0.168 to 0.30-0.32. The write-offs are 4.2% of claimants and 24.7% of the loss, so their shortened exposure lowers the score. The notes' own test (claim size against claim probability) does not cover the frequency channel | LEAK-6, LEAK-11 |
| 18 | `vehicle_value` is in $10,000s; CASdatasets' "thousands of AUD" is an error of that copy | notes | Rd, CASdatasets page, book p. 9-10, data | holds | Rd: "vehicle value, in $10,000s". CASdatasets: "in thousand of AUD". Book: claim probability peaks "around $40 000". Data: the claim rate peaks at 3.0-4.0 (8.2%) | PROV-15 |
| 19 | 53 zeros, most of them station wagons, buses, trucks or caravans of the oldest band; next lowest value 0.18 | notes | counts | holds | 51 of 53 in those bodies, 41 of 53 in band 4, next value 0.18. A zero does not mark a claim: 6 of 53 claimed (p = 0.17 against 6.8%) | CLEAN-10 |
| 20 | Body codes get CASdatasets' labels | notes; `BODY_LABELS` | mapped against CAS `VehBody` | holds | equal on 100% of rows | CLEAN |
| 21 | 707 rows in duplicate groups (378 extra copies), all without a claim, 36% full-year; "such repeats are plausible ... kept as natural (LEAK-18)"; 0.8% of test rows have an exact copy in train | notes; info check | chance baseline: exposure shuffled across the no-claim rows (also stratified by vehicle age band, body, area and driver age band); full-year subset against random subsets; Gini with the copies dropped | counts hold; "natural repeats" refuted | observed 378 copies; 120 after shuffling (96-134 over 20 runs), 125 stratified (109-159). Among the 1,129 full-year rows there are 152 profile copies; random subsets of that size give 11.6 (at most 18 in 50 draws). The copies sit far apart in the file (median gap 11,146 rows). Dropping them changes the Tweedie LightGBM Gini by +0.0045 (SE 0.001), so they do not inflate the score | LEAK-18, LEAK-19 |
| 22 | Split forced (ForcedIIDFromTemporal): the release does not say which year a policy started | notes; data_tags | the raw file order as a hidden time axis or hidden groups | holds | no date column. The file order has local runs of equal day counts (12.2% of neighbouring rows against 0.31% by chance) but no trend: Spearman of exposure with the row number is 0.04, and the claim rate by tenth of the file is 6.1-7.3%. Neighbours with equal day counts do not share an area (22.4% against 21.5%), so they are not households. Allstate's challenge was split by year (2005-2007 train, 2008 test), which agrees that pricing is temporal | SPLIT-8 |
| 23 | `normalized_gini`, origin context, no scoring columns; computable on every fold | metric | `scorer(container)` on 9 folds with constant, random, oracle and exposure predictions | holds; one caveat | 1,512-1,582 claimants and 223-243 floor policies per test fold; oracle 1.000. A constant prediction scores -0.061 to +0.037, because ties are broken in row order on a shuffled frame. Models with continuous predictions are barely affected | MET-2, MET-13 |
| 24 | Metric reason: insuranceData and CASdatasets define no task; the book scores no held-out prediction | metric reason | Rd; CAS page; one more look at the companion site | packages hold; the book is untested | no task or metric on either page. The Internet Archive was still "Temporarily Offline" on 2026-11-01, and has no snapshot listed for acst.mq.edu.au/GLMsforInsuranceData | MET-1 |
| 25 | Metric reason: "models are compared by the Gini index of the ordered Lorenz curve of losses (Frees, Meyers and Cummings 2011)"; task_summary: "the insurers' ranking metric" | metric reason; changes | Frees' definition, as quoted by Henckaerts et al. (arXiv 1904.10890, Sec. 5.1; the JASA paper is paywalled); both variants scored on the 9 splits | refuted in part | Frees' curve puts the cumulative benchmark premium on the x-axis and orders rows by relativity (competing / benchmark premium). The declared metric puts policy counts on the x-axis and orders by predicted cost. The two agree only when every row has the same premium. With a premium per policy-year (rows run from 0.003 to 1 year), Frees' index is the exposure-weighted Gini of the rate (`normalized_weighted_gini`, weight = exposure). Under it, the rating-factor GLM scores 0.102 (0.200 declared), LightGBM with an exposure offset 0.077, exposure-only ranking -0.206 (+0.168 declared), and ranking the shortest exposures first +0.206 | MET-1, MET-2 |
| 26 | Allstate chose the normalized Gini for "a task of this shape: claim payments per vehicle-year, mostly 0" | metric reason | WPI thesis on the challenge (Sec. 2.0, 4.0) | holds, with a difference | "Each of the 13184290 cases ... contains one year's information for an insured vehicle", and the leaderboard used the normalized Gini. Every Allstate row is a full year; here 98.1% of rows are not | MET-2 |
| 27 | RMSE follows a few large claims: the largest 46 (0.07%) hold 43% of the sum of squares; no family beats the mean by more than R^2 0.002 | metric reason | recompute; probe logs | holds | 0.4296 of SS; 0.068% of rows; linear 0.002, GLM 0.0013 | MET-11 |
| 28 | "The Gini ignores the price level" | metric reason | definition | holds | depends only on the ranking of the predictions | - |
| 29 | Warning `task_target_value_dominant`: zero-inflated by nature, not a cap or placeholder | builder; bundle check | zeros against `clm` | holds | every zero is a no-claim policy | TP |
| 30 | Decision tables (floor by claim count; median exposure by claim / vehicle value) | Decisions 1-2 | recompute | holds | 4,333/271/18/2 policies; 705/10/0/0 at the floor; 3,158/800/270/197/193 claims by band | - |
| 31 | Licence GPL-2; sha256 of the tarball and the CSV | licence; download | DESCRIPTION; sha256sum | holds | "License: GPL-2"; both hashes match | PROV |
| 32 | Record screening: fit direct; metric fallback `rmse`; 695 of 4,624 (15%) exactly 200; untuned LightGBM R^2 -0.02 on raw cost; oracle 0.97 | record | recompute | holds where measured; superseded otherwise | 695 is exact equality (705 to the cent); oracle R^2 on log1p is 0.968; task probe LightGBM -0.023. The definition's later reading replaces "direct" and the `rmse` fallback | EV-2 |
| 33 | Record Assessment: exposure kept as a feature, "as in the fremtpl2 call" | record | fremtpl2 record CC of 2026-10-20 | holds | "keep `Exposure` capped at 1"; frempl did the same | precedent |
| 34 | Builder: every family beats the dummy Gini 9/9; the `no_signal` flag on R^2 read as a small real signal | builder report | probe CSV | holds | yes, 9 of 9 for all five families. The dummy itself moves between -0.06 and +0.04 (#23) | TP-2 |
| 35 | Implied: the six rating factors are known at the prediction point | implied | codebook; vehicle value 0 against claims | holds | all are rating factors at policy start; no post-outcome marker found | LEAK-10 |
| 36 | Implied: no row is a copy of the same policy across the split | implied | pairs with identical rating factors whose day counts add up to a year (one policy cut by two windows) | holds (small) | 116 and 116 pairs at 365 and 366 days, against a median of 102 for other sums from 300 to 430. Copies (#21) are zero rows and do not inflate the score | LEAK-17 |
| 37 | Implied: the target is the settled claim cost | implied | point masses | untested | 27.5% of claimants sit on 12 repeated amounts (200 x 705, 353.77 x 219, 389.95 x 94, 367.73 x 42, ...). These may be standard amounts or initial case reserves. Whether costs are paid or incurred, and how far they had developed, is not documented | USE-5, LEAK-24 |

**Refuted claims, ranked (validity first, Must first)**

1. **The time in force is called the contracted period, known at pricing** (#5, #14; P4, USE-3 and LEAK-10, Must,
   on the wording). It appears in the prediction-point note ("the period the policy is on risk [is] known then"), in
   `known`, and in the record's Assessment ("the contracted period is known when the policy is priced"). Every policy
   is a one-year contract. `exposure` is time inside an extract window: 98.1% of rows fall short of a full year,
   almost uniformly. Its short end carries outcome information beyond the write-offs: claims per year of exposure are
   0.40 and 0.23 in the shortest tenths against 0.14-0.17 elsewhere, and 0.33 and 0.20 without the write-offs.
   `fit_reason` already says the time in force is "known only after the period", so the definition contradicts
   itself. *What it changes:* the notes, not the keep. Under the declared Gini, the outcome-dependent part brings no
   gain (free effect against offset: +0.005 ± 0.007 GLM, +0.002 ± 0.005 LightGBM), and the shortened exposure of the
   write-offs lowers the score (counterfactual +0.13, 18 of 18 runs). That is LEAK-11 (a late value that weakens the
   signal stays with a note) on top of the LEAK-6 narrowing the notes cite. *Mildest remedy:* reword the
   prediction-point bullet, `known` and the Assessment to "the time in force in the extract; a policy that ends early
   (after a write-off) is shorter". Cite LEAK-11 with the counterfactual number. In `fit_reason`, name the time in
   force as a kept potential leak and not as a gap (USE-8).
2. **The metric reason's support** (#25, #26, #7; P6, MET-1 and MET-2, Must). Frees et al. compare models on premium
   share, and Allstate's rows are full vehicle-years. The declared metric weights every row equally, on rows observed
   from 1 to 365 days. On this data it gives 82% of the best score to ranking policies by how long they were observed,
   which no price for a one-year contract depends on. The rating-factor signal, which is what pricing sets, is scored
   by the exposure-weighted Gini on the rate: GLM 0.102, LightGBM with an exposure offset 0.077 (the builder's rate
   model 0.086). *What it changes:* what the benchmark measures. The keep in #1 is tied to the metric: under the
   weighted Gini, exposure as a feature would be a strong late signal (shortest first +0.206, above the rating-factor
   GLM's 0.102), so that framing needs exposure as a scoring column and not as a feature. *Mildest remedy:* keep the
   metric and reword the reason: Kaggle's count-based normalized Gini, chosen by analogy with Allstate's full-year rows.
   Say that exposure alone reaches 82% of the best score, and drop "the ordered Lorenz curve of Frees et al." as its
   support, or describe that curve correctly. *For the curator (builder issues 1 and 3):* the rate per policy-year with
   exposure as the weight (`normalized_weighted_gini`) and not as a feature. frempl uses the same unweighted framing,
   so this is a decision for the whole family.
3. **The duplicates are called natural repeats** (#21; P4, LEAK-18 and LEAK-19, Should). The 378 copies are about three
   times the chance level (120-125), and 13 times among the full-year rows (152 against 11.6). They look like linked
   records, perhaps several vehicles of one holder insured on the same dates. *What it changes:* little. Every copy has
   no claim, and dropping them changes the Gini by +0.0045, so they do not inflate the score. *Mildest remedy:* reword
   the note with the chance baseline and keep. Or drop the copies under LEAK-19 (exact copies with the same label).
4. **"5,742 to 6,547 policies per band"** (#9; P5, PROV-16, wording). The bands hold 5,742 to 16,189 policies, and all
   18 cells match the book. *Remedy:* "5,742 in the youngest band to 6,547 in the oldest, 67,856 in all".
5. **The fit_reason names a kept leak as a gap** (#8; USE-8, wording). This is folded into the remedy of point 1.

**Untested claims, ranked**

1. **Settled or incurred claim cost** (#37; P3 and P4, USE-5 and LEAK-24). 27.5% of claim costs sit on 12 repeated
   amounts, and costs for 2004-2005 policies released in 2008 may not have settled. This cannot be checked: the book's
   page 15 was not read, and the companion site and the Internet Archive are offline. It goes to the curator as a
   question that cannot be verified. It does not block: the Gini ranks losses, and a reserve standard is part of the
   source's data.
2. **What the book does with this table** (#11, #24): Sec. 8.3 and 10.4-10.5, and that it scores no held-out
   prediction. Only the contents were read, so mark these claims unverified in the notes (PROV-16). If the book did
   score held-out predictions, the metric's origin would need a second look (MET-1, MET-5).
3. **The source's definition of `exposure`** (#14): only "0-1" (insuranceData) and "the number of policy years"
   (CASdatasets) are available. The window reading rests on the measured distribution (EV-2, level 1).
4. **The floor's mechanism** (#13): the pattern is reproduced exactly; the per-claim minimum of 200 is an inference.
   The decision to keep it does not depend on the mechanism.

**For the other agents:** the split auditor can use #22 (local runs of equal day counts in the raw order, no global
time axis, no households). The critic and the mediator can use #17 and #25 (the exposure keep holds under the declared
Gini but would not hold under a premium-weighted Gini).

Sources: [Henckaerts et al., arXiv 1904.10890](https://arxiv.org/pdf/1904.10890) (Sec. 5.1, quoting Frees' ordered
Lorenz curve); [WPI thesis on the Allstate Claim Prediction Challenge](https://digital.wpi.edu/downloads/zs25x859f?locale=en);
[CASdatasets ausprivauto](https://dutangc.github.io/CASdatasets/reference/ausprivauto.html);
[Frees, Meyers, Cummings 2011, abstract](https://academicnewsletter.sufe.edu.cn/info/445125); insuranceData 1.0
`man/dataCar.Rd` and `DESCRIPTION` (the CRAN tarball); de Jong and Heller (2008), excerpt pp. 1-10 and contents
(saved in the run folder).

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01)**

**Verdict: ship after small changes.** No column needs to go. `exposure` is partly recorded after the outcome, and
more broadly than the note says: the shortening also shows in claim occurrence, not only in claim size. The part that
can be traced still adds nothing to the Gini, so keeping it with a note still holds (LEAK-10 second clause, LEAK-6;
the fremtpl2 precedent). The note should be rewritten with the right test. The target ships in raw dollars while its
sibling frempl ships log1p under the same family call. That choice moves a default model's Gini by +0.034 (CLEAN-16,
MET-3). It needs the curator.

Prediction point used: when the policy is priced at underwriting ("for example"; the first `curation_comments`
bullet). Frame read through `dataset_io` from the definition (67,856 x 8, IID, 3 x 3 splits).

**Column table**

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `claim_cost` (target; `claimcst0`) | "claim amount (0 if no claim)" (insuranceData); "the sum of claim payments" (CASdatasets) | the outcome | float64, raw dollars. 0 on exactly the 63,232 rows with `clm` = 0. The 200 floor is kept as recorded. 1,925 of the 4,624 positive values are off the cent grid by up to $0.005 (float noise in the source). Paid-to-date or ultimate cost and the extraction date are unknown | fine as a target; open questions: raw scale or log1p (frempl), and rounding to cents | CLEAN-16, MET-3; CLEAN-1; LEAK-24 cannot be tested |
| `exposure` | "0-1" (insuranceData); "the number of policy years" (CAS). Days / 365.25: every value is a whole day count from 1 to 365 | partly. The overlap of the policy with the observed period is fixed when the policy starts. The part cut short after a claim is not known then | float64 as published. No cap needed (max 0.9993) | leak, weak, kept with a note (remedy: rewrite the note) | LEAK-10 (second clause), LEAK-6 |
| `vehicle_value` | "vehicle value, in $10,000s" (insuranceData). The book puts the peak claim probability "around $40 000" (Sec. 1.4), which fits only this scale (the 99.9% quantile is 10.4). CAS's "thousand of AUD" (its page, read 2026-11-01) is an error of that copy | yes (the value when the policy starts). Rounding and spread do not differ between policies with and without a claim (below) | float64. 53 zeros made missing (CAS has the same 53). 97.4% of values lie on a $100 grid. The other 1,771 rows (1,769 of them in vehicle age band 1) end in $990 or $490, which look like new-car list prices | fine | CLEAN-10, CLEAN-11; LEAK-13 not triggered |
| `vehicle_body` | 13 body codes, given CAS's labels; each code has one CAS label on every row (checked) | yes | category, 13 levels (27 roadsters to 22,233 sedans) | fine | CLEAN-12, CLEAN-14 |
| `vehicle_age_band` | "1 (youngest), 2, 3, 4" (insuranceData). CAS's words are "youngest cars" to "oldest cars"; the band limits are not published | yes | int64, ordered. Median vehicle value falls from 2.3 to 0.8 across the bands, as an age order implies | fine (dtype is a weighing point, problem 6) | CLEAN-14 |
| `driver_age_band` | "1 (youngest) ... 6" (insuranceData). The book's Table 1.1 says "Driver's age category"; CAS says "the age of the policyholder" ("youngest people" to "oldest people"). Band limits not published | yes | int64, ordered. Counts match Table 1.1; the claim rate falls from 8.6% to 5.6% | fine | CLEAN-14 |
| `driver_gender` | "gender", F/M (insuranceData); "the gender of the policyholder" (CAS). No source read says "driver" | yes | category | fine; the name claims more than the sources say (problem 3) | CLEAN-1 (naming) |
| `area` | "a factor with levels A-F" (insuranceData); absent from CAS. The task summary's "area of residence" is in no page read (the book's p. 15 description was not read) | yes | category. The claim rate is not monotone in the letter (6.1% to 7.8%), so there is no order to restore | fine; meaning partly unknown (problem 4) | CLEAN-14 |
| `clm` (dropped) | "occurrence of claim" | no (the outcome) | dropped; equals `claim_cost > 0` on every row (asserted in `_clean`) | correct drop | LEAK-10 |
| `numclaims` (dropped) | "number of claims", same period | no | dropped; above 0 on exactly the claim rows | correct drop | LEAK-10 |
| `X_OBSTAT_` (dropped) | the constant "01101 0 0 0" | n/a | dropped | correct drop | CLEAN-5 |

The source has no identifier. Each of the 378 extra exact copies has no claim. That is expected: a copy of a
claimant row would need the same cost to the cent. 56 of the 373 groups of rows with identical features carry
different costs: ordinary noise for a regression target.

**Problems, ranked**

**1. P4, LEAK-10 / LEAK-6: `exposure` is shortened after claims, more broadly than the note says. Keep it, but rewrite the note.**

* Most of the column is the observation window, not the policy term. All rows are one-year policies, but only 1,289
  (1.9%) are in force for 365 days. Across 20 equal bins the counts fall gently from about 4,000 to 2,600, and the last
  bin also holds the full-year pile. The likely reading, which no source states, is that the column measures how much
  of each policy fell in the observed period. That is set when the policy starts, so it is a fair input (it is what a
  GLM offset uses).
* Shortening after a claim, in claim occurrence. Claims per policy-year by exposure:

  | exposure (years) | claims per policy-year |
  |---|---|
  | up to 0.02 (7 days) | 1.27 |
  | 0.02 to 0.04 | 0.53 |
  | 0.04 to 0.06 | 0.44 |
  | 0.06 to 0.08 | 0.30 |
  | 0.08 to 0.10 | 0.22 |
  | above 0.2 | 0.14 to 0.17 |

  The policies above 0.3 years claim 0.150 times per policy-year. At that rate the 15,592 policies of 0.2 years or less
  would have about 232 claims; they have 379, an excess of 147 (3.2% of all claims). A Poisson GLM of the claim count
  on the rating factors gives log(exposure) a coefficient of 0.73 where proportional time on risk would give 1.
* The excess claims look like write-offs. Claims on policies of 0.05 years or less have a median cost of $2,972. Their
  median cost is 0.30 of the vehicle's value, and 23% are at 80% of the value or more. Above 0.5 years the median cost
  is about $750, the median share of value 0.045 to 0.048, and 2.5% are at 80% or more. The link holds inside every
  vehicle-value quintile, so cheap cars do not explain it:

  | vehicle-value quintile | median exposure, claims at 80% of value or more | median exposure, other claims | Mann-Whitney p |
  |---|---|---|---|
  | 1 | 0.40 | 0.62 | 2.6e-8 |
  | 2 | 0.30 | 0.66 | 2.0e-7 |
  | 3 | 0.47 | 0.64 | 0.06 |
  | 4 | 0.38 | 0.67 | 0.03 |
  | 5 | 0.19 | 0.64 | 1.7e-4 |

  With the claims at 80% or more removed, short policies still claim too often: 0.85 claims per policy-year at 0.02
  years or less, 0.40 between 0.02 and 0.06. So the shortening is not limited to the 193 claims the note names. A car
  is often written off below 80% of its value, and other claims may also end a policy.
* The note's test is incomplete. It argues "the claim size adds nothing to the Gini". But the shortening also acts on
  claim occurrence, and the Gini comes mostly from occurrence. The test that fits, on the 9 shipped splits with
  Tweedie LightGBM:

  | exposure enters as | mean Gini | free feature better on | difference, paired SE |
  |---|---|---|---|
  | a free feature (as shipped) | 0.1824 | | |
  | a proportional offset only (log exposure as init score, so the model cannot use the short-policy excess) | 0.1833 | 4 of 9 | -0.0009, SE 0.0059 |
  | a feature floored at 0.1 years | 0.1849 | 3 of 9 | -0.0025, SE 0.0029 |
  | not at all | 0.0893 | | |

  The late part that can be traced shows no gain. So LEAK-10's second clause keeps the column with a note. This
  matches fremtpl2 (CC 2026-10-20: "a mid-year cancellation also shortens it") and frempl.
* **Remedy (mildest): keep `exposure`; rewrite the "Potential leak, kept on purpose" bullet.** It should say three
  things:
  * the column mostly measures how much of the policy fell in the observed period (1.9% full year);
  * the shortening after a claim shows in claim occurrence (147 excess claims at 0.2 years or less), not only in the
    193 claims at 80% of the value;
  * the no-gain evidence is the floor and offset test above, with the hurdle comparison as support.

  `task_summary.known` should say "the share of a year the policy was in force within the observed period". The
  curator confirms the keep, case by case, as the clause requires.

**2. P7, CLEAN-16 with MET-3, consistency: raw-dollar target here, log1p in frempl.**

* frempl ships `log1p_claim_amount` with `target_transform="log1p"` and scores the Gini on the amount. That follows
  the same family call of 2026-10-30. This definition ships raw dollars and records no reason for the difference.
* Effect on the 9 shipped splits: squared-error LightGBM reaches a Gini of 0.163 on the raw target and 0.197 on log1p
  (+0.034, paired SE 0.007, better on 9 of 9). The metric reason quotes a GLM vs LightGBM gap of +0.042; this effect is
  almost as large. The builder raised the same point.
* **Remedy:** ship `log1p_claim_cost` with `target_transform="log1p"`. The Gini still scores the dollar amount.
  Otherwise record the fact that sets this table apart from frempl. This is the curator's call (consistent judgement,
  case 2).

**3. P7, naming: `driver_gender`.**

* CAS: "the gender of the policyholder". insuranceData: "gender". The book's chapter 1 names only the driver's age.
* **Remedy:** rename to `gender`, or say in the notes that the sources differ. In `known`, "the driver's gender"
  becomes "the policyholder's (or driver's) gender". `driver_age_band` can stay: the book's Table 1.1 backs it.

**4. P7, unverified meaning: `area`.**

* "Area of residence" (`task_summary.known`) is in no source read. insuranceData gives only "a factor with levels
  A-F".
* **Remedy:** write "an area code A-F, undocumented", unless the book's p. 15 description confirms residence.

**5. P7, CLEAN-1: float noise in the target.**

* 1,925 of the 4,624 positive costs are off the cent grid by up to $0.005.
* **Remedy:** round to cents. It is cheap and safe, and the 200 floor then counts exactly (705) without the "695
  exactly, the rest float noise" wording. Optional.

**6. P7, CLEAN-14, a weighing point: the age bands as numbers.**

* Numbers keep the order. The band limits are not published, and CAS's words only restate the order. Precedents typed
  bands as categories when they came with labelled limits (expresso `TENURE`, open_university `age_band`).
* No change suggested; listed for consistency only.

**Tested and not a problem**

* `vehicle_value` is not recorded differently for claimants. Within each vehicle age band, policies with and without a
  claim match:

  | vehicle age band | share on a $1,000 grid (claim / no claim) | SD of log value (claim / no claim) |
  |---|---|---|
  | 1 | 0.109 / 0.085 | 0.451 / 0.470 |
  | 2 | 0.092 / 0.107 | 0.409 / 0.408 |
  | 3 | 0.108 / 0.098 | 0.442 / 0.436 |
  | 4 | 0.101 / 0.105 | 0.541 / 0.543 |

  The list-price values in band 1 claim 0.171 times per policy-year against 0.163 for the other band-1 values. Their
  crude rate is higher (8.4% against 6.5%) only because they are in force longer (mean exposure 0.53 against 0.42).
  The zeros made missing have 6 claims in 53 rows (3.6 expected at the base rate), and buses or old station wagons
  account for most of them.
* The raw file order carries no label, though it is not random. 12.1% of adjacent rows share the exact day count,
  against 0.3% by chance. The lag-1 autocorrelation is 0.094 for exposure (0.002 shuffled) and 0.096 for the driver
  age band, but 0.005 for the claim indicator. Neighbouring rows match on claim status 87.4% of the time, against
  87.3% by chance. The order is not a column and the pipeline shuffles it. It is a lead for the split auditor on
  SPLIT-8: the file may have been written in date batches. 2,000-row blocks show no overall trend (mean exposure 0.39
  to 0.56).
* LEAK-24: CAS calls the amount "the sum of claim payments". Whether payments were still developing cannot be checked
  without dates; the builder already lists this as a gap.

**Judgment record**

```text
Verdict: ship after changes.
Validity: LEAK-10 triggered for `exposure` (weak: shortened after claims, in claim occurrence as well as size); kept
  under its second clause, since the traced part shows no Gini gain (floor and offset tests, 9 splits); the note needs
  rewriting. `clm`, `numclaims` dropped under LEAK-10 (hold). No other column holds post-outcome values.
Quality: CLEAN-16 departure with no recorded reason (frempl ships log1p; +0.034 Gini for a default model);
  CLEAN-10/11 vehicle value 0 to missing holds; CLEAN-5 holds; naming of `driver_gender` and `area`; target float noise.
For the curator: the target scale (consistency with frempl); confirm the `exposure` keep with the rewritten note.
```

Scripts and outputs are in the run folder: file order, exposure distribution and rates by exposure, the write-off
link by value quintile, the short-policy claims, vehicle value, labels, target noise, the gain test (exposure as an
offset, per split) and the target scale.

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): australian_vehicle_insurance_2004_2005**

**Verdict: right with notes.** IID 3x3 tagged `ForcedIIDFromTemporal` is the regime SPLIT-8 gives a pricing task whose release has no time axis, and it matches the frempl_french_motor_personal_line precedent (one year, IID, forced). No hidden group or near copy changes the score. The notes need two corrections in wording. The split itself stays as it is.

```text
Verdict: right with notes (no change to the split; two note edits).
Validity: SPLIT-1, SPLIT-8 hold (forced IID, temporal by use case, no dates); SPLIT-8 note partly inaccurate (issue 1)
  and silent on the unmeasurable cost (issue 2); SPLIT-29/30 hold (0 hits; copies change nothing, issue 3);
  USE-10 holds (one policy per row, new-business pricing, issue 4); SPLIT-9 to SPLIT-21 not applicable (no time axis).
Value: every test fold holds 1,512-1,582 claimants, so the Gini can be scored on every fold.
For the curator: issue 1, a reading of the exposure column (one accounting year) that changes what the notes promise
  from "a split by year".
```

Scripts and outputs are in the run folder. Data loaded through dataset_io (`origin=rebuilt`). The shipped splits are 3 repeats x 3 folds, seed 4267, train 45,237-45,238 rows, test 22,618-22,619, no overlap between train and test.

**Regime against the use case (SPLIT-1, SPLIT-8, USE-10): holds.** The use case is pricing a one-year policy at underwriting. A tariff is fit on past policy-years and applied to the next year's, so the task is temporal by its use case. There is no date and no policy id. The test rows stand for "other policies of the same portfolio", which `task_summary.split` and `fit="approximate"` both say. The tag is right: SPLIT-8 covers "a release with no dates at all (one extract)". It also matches frempl (`ForcedIIDFromTemporal`, "the release holds one year").

**Issue 1 (P4, SPLIT-8, Must; the note's accuracy, Should): "a split by year would test a model on a later year's portfolio and claim level" probably does not hold. The release looks like one accounting year.** This is a reading from measurements. The mechanism is inferred (EV-2), and the book's own description of `exposure` (p. 15, Sec. 7.3) was not read.
- `exposure` is days / 365.25 and covers 1 to 365 days, spread almost evenly. Each 30-day bin holds 6.5% to 9.8% of the rows. The median of `exposure` is 0.446, against 0.5 for a uniform spread.
- Only 1.9% of rows (1,289) have a full year. That is 11 times the median count of the neighbouring days, but far below what fully observed one-year policies would show, since most policies run their whole term.
- No row has 366 days, although 2004 was a leap year: a 2004 policy observed over its whole term would sometimes span 29 February.
- These facts fit exposure being the part of each policy inside one 365-day observation period. Calendar 2005 is the simplest fit: the tails of policies "taken out in 2004" and the heads of those taken out in 2005, exactly as the help page says. This is the usual accounting-year extract of insurance data, the same layout as frempl's "records within 2004, an open record ending on 31 December".
- There are weak extra peaks at month-boundary day counts (31, 93, 123, 183, 274-276, 335; 1.25 to 1.6 times their neighbours). They are consistent with that layout but do not pin the window.
- If this reading holds, a split by inception year would separate policy starts within one claim period. It would not test a later year's claim level. A temporal test needs another year's extract.
- Mildest remedy: edit the notes only. In the last `curation_comments` bullet, replace the sentence about a split by year with what the data shows: one observation period of about a year, the evidence above, and "a temporal test needs a later year's extract". In `task_summary.split`, change "the same portfolio and years" to "the same portfolio and period".
- Cross-lane pointer for the leak reviewers: under this reading, most of the variation in `exposure` comes from the extract window, not from each policy's term (every policy is a one-year contract). So the "share of a year the policy was in force" wording, and "revisit if a release gives the contracted term", may need the same correction.

**Issue 2 (P4, SPLIT-8, Must): the notes do not say that the cost of the forced split cannot be measured.** SPLIT-8 asks for the cost "measured against the valid windows where the data has any". There are none, and the data shows it:
- The file order is shuffled:
  - Lag-1 correlations along the rows are -0.008 to 0.005 for the numeric columns.
  - The share of neighbouring rows in the same category equals chance (body 0.248 against 0.249, area 0.214 against 0.213).
  - The claim rate per tenth of the file is 6.1% to 7.4% with no trend; its Spearman correlation with the row index is 0.005.
  - Neighbouring rows are both claimants 300 times, against 315 expected by chance.
- Under the reading of issue 1, a tail and a head with the same number of days look alike, so `exposure` does not reveal the inception year either.
- No row-order time index (SPLIT-22) and no pseudo-window can be built.
- Remedy: add one clause, for example: "the file order is shuffled and no column dates a policy, so the cost of the random split cannot be measured" (as distribution_transformers and mobile_churn state what they could or could not measure).

**Issue 3 (P4, SPLIT-29/30 and LEAK-16 to LEAK-21): hidden groups and copies across the split. None that matters; holds.**
- The hidden-group probe has 2 candidates and 0 hits. `exposure` has gap +0.002 and `vehicle_value` +0.012, both inside their fold SD of 0.018-0.025. The near-copy check was not run (7 columns), so it is no evidence either way.
- Composite-key excess: 12.7% of rows share vehicle value, body, age band, gender and exposure with a row of another area or driver band, against 2.3% if the columns were independent.
  - Most of the excess comes from the full-year cohort: 923 of the 1,289 rows with 365 days are in such keys, against 0.6% of the other rows.
  - That cohort holds more trucks and panel vans (8.5% and 7.9% of its rows, against 2.5% trucks among the other rows), more men and more of the oldest vehicle band. It looks like fleets that start on the window's first day.
  - The key carries no label, though: claim rate 7.1% against 6.8%, s_id -0.20, gap +0.004. It is not an entity that new data would lack and that carries the label, so SPLIT-29 is not triggered.
- Exact copies: 0.85% of test rows have an exact feature copy in train (192 of 22,619 on split 0/0, with 11 to 20 claimants per repeat). This matches the notes' 0.8%.
- Alternative split, fitted (Tweedie LightGBM and Tweedie GLM with log exposure, as in the builder's probe):

| split | Tweedie LightGBM Gini | Tweedie GLM Gini |
|---|---|---|
| shipped IID, 9 folds | 0.182 (SD 0.025) | 0.205 (SD 0.025) |
| shipped, test rows with a train copy removed | 0.183 | 0.206 |
| grouped on the exact 7-feature vector, 3x3 | 0.194 (SD 0.030) | 0.208 (SD 0.024) |

  The copies do not raise the score: the grouped split scores within fold noise of the shipped one, and slightly higher, not lower. This is a sensitivity check, not a proposal. A hash of the feature vector is no group id (SPLIT-24).
- Renewal pairs: none found. Under issue 1's layout, a 2004 policy renewed in 2005 would appear as two rows whose days sum to 365.
  - Among rows identical in all six rating factors, 116 pairs sum to 365 days. Sums of 360 to 370 days give 94 to 132 pairs each, and the mean over sums of 300 to 430 is 102.
  - The key without the vehicle value (which a renewal might revalue) also shows no peak at 365: 6,248 pairs, against 6,208-6,634 for 360-370.
  - So no policy is visibly split into two rows.

**Issue 4 (P3/P4, USE-10): new or known entity. Holds; no change.** Pricing a renewal would use the policyholder's claim history (the no-claim bonus rating). The release has none, and no ids, so the task is pricing on the rating factors alone, effectively new business. Issue 3 finds no entity that recurs. `fit="approximate"` already covers the gap, and nothing else is needed.

**Temporal checks (windows, gap and label delay, training history, a season-shaped window): not applicable.** There is no time axis (issue 2). Whether the claims were paid or incurred, and how developed they were at the extract, cannot be measured (LEAK-24, as the builder says). Claims per policy-year are highest at the shortest exposures: 0.41 under 30 days, 0.13 at a full year. That is the opposite of the drop that unreported late claims would cause, but the write-off ends the builder found mix into it, so it does not prove that the labels matured.

**Claims checked.**
- Confirmed:
  - `task_summary.split` ("random policies ... same portfolio"), apart from "years" (issue 1).
  - The forced-IID tag and its use-case reason.
  - "0.8% of the test rows have an exact feature copy in train" (0.85%).
  - "36% of them in force for a full year" (0.362, builder's explore2).
  - The split sizes in the README.
- Not supported as written: "a split by year would test a model on a later year's portfolio and claim level" (issue 1).
- Consistent with precedents: frempl (one year, forced IID, folds by policy chain score like random ones) and the one-snapshot cases of SPLIT-8.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: a motor insurer's pricing actuary (Australia, private comprehensive car)**

**Verdict.** Fit: **approximate**, as declared. The data are real one-year policies with the rating factors and claim costs a tariff is fit on, but two things fall short of the decision. The shipped `exposure` is the observed part of each policy's year, not the contracted term, which is one year for every row. And a random split of undated policies stands in for next year's book. Metric: **partly**. A normalized Gini is the kind of measure I select pricing models by, and on six probe models it orders the real ones as my own measure does. But it is computed per observed slice and unweighted, so exposure alone earns 80-82% of the best score. P3 (a real use case) is solid: tariff pricing is the core actuarial decision, and this is a real, documented portfolio. It can carry the small cleaning imperfections (the $200 floor, the 53 vehicle values of 0, the 378 duplicates).

**1. My inputs when I price the policy (USE-3, USE-6)**

- Rating factors: vehicle value, body type, vehicle age band, driver age band, gender and area are all on the proposal. I have them.
- `exposure`: I do not have it. The source says every row is a one-year policy ("based on one-year vehicle insurance policies taken out in 2004 or 2005", insuranceData `dataCar`). At the quote I know the term: one year, the same for everyone. The shipped column is something else:
  - its median is 163 days;
  - it is spread almost evenly over the year (rows per tenth of a year: 7,989, 7,603, 7,835, 7,282, 6,681, 6,671, 6,275, 5,704, 5,502, 6,314);
  - only 1,289 rows (1.9%) cover a full 365 days.

  A one-year contract observed for an even share of its year is what you get when an accounting window cuts across policies written over two years (the earned exposure of a period), plus policies that end mid-term. The first curation bullet and `known` say "the period the policy is on risk [is] known then". That holds for the contract, not for this column. The fremtpl2 reason (the contracted period is known at pricing) carries over only to the term, which here is 1 for every row. In training I would use the earned exposure as an offset or a weight (CAS Monograph 5, Sec. 2, "Exposure offsets"). At the quote I would set it to 1.
- Part of the exposure is cut short by the outcome (LEAK-10):
  - Claims of at least 50% of the vehicle's value: 0.107 per policy-year in the shortest tenth of exposure against 0.005 in the longest (21 times).
  - Smaller claims: 0.252 against 0.121 (2 times).
  - Cost per policy-year: $1,592 against $204 (7.8 times).
  - A Tweedie GLM with log exposure as a free covariate gives it a coefficient of 0.31; a pure offset would be 1.

  In Australia, a total-loss settlement ends a comprehensive policy with no premium refund (NRMA's FAQ, read from a search summary because the page refused direct fetches). So a written-off car's exposure stops at its claim. Boucher, Coulibaly and Trufin (2026) report "a marked difference in claims experience" between policies cancelled mid-term and those kept to maturity. They price it as a cancellation penalty, not as a quote input.
- Inputs I would always have and that are missing:
  - the no-claim bonus or rating level (the policyholder's claim history);
  - postcode or garaging address (6 areas here);
  - make, model and year (13 body types and 4 age bands here);
  - exact age and years licensed (6 bands here);
  - the excess chosen, the cover type and the use (private or business);
  - whether the policy is new business or a renewal;
  - the premium charged.

  Their absence makes this a thin new-business tariff. That changes how hard the task is, not the decision.

**2. The target (USE-5)**

- What I act on is a number: the expected claim cost of one policy-year (the pure premium), before expenses and loadings.
- The shipped target is the cost of the observed slice. Dividing it by exposure, with exposure as the weight, gives the pure premium, which is how actuaries model it:
  - CAS Monograph 5, Sec. 2.7.3: "dollars of loss per exposure, using the Tweedie distribution";
  - actuaRE's copy of this very table ships `Y = claimcst0 / exposure` with `w = exposure`.

  So the target is the right quantity in the wrong unit: a close proxy.
- Things about the target I cannot check:
  - incurred or paid, and at what evaluation date (open claims, claims not yet reported);
  - the $200 floor (705 single-claim policies at 200.00) and the point masses at 353.77 (219), 389.95 (94) and 390 (55).

  The point masses look like fixed amounts (a nominal booking, or glass and towing at a set price). They are of the same kind as freMTPL2's IRSA-IDA convention amounts, which the collection keeps. Keeping them as recorded is right: they are what the insurer booked.

**3. One row against one decision, and the test data (USE-10, USE-8, SPLIT-8)**

- One row is one policy's observed slice. My decision is one policy's annual premium. The two match once the slice is put on a per-year basis.
- There are no policy ids and no history, so this is a cold-start tariff for new business, which is legitimate (USE-10).
- Test data: random policies of the same two inception years. CAS Monograph 5, Sec. 4.3.1 accepts a random holdout and prefers an out-of-time one, which shows "how the model will perform on unseen years". `ForcedIIDFromTemporal` and the approximate fit are right; per USE-8's weighed factor, a use case rephrased only to excuse a gap does not count.
- No direct alternative use case (USE-9): monitoring actual against expected on earned exposure uses the tariff's own expected values, not a new prediction.

**4. Would I use it?**

- As a benchmark for methods that fit a new-business tariff on a few coarse factors: yes.
- What makes me trust it:
  - The source is a textbook table, and two independent copies agree row by row.
  - The probes behave as pricing experience says: a Tweedie GLM beats untuned boosting (0.205 against 0.182), and squared-error boosting comes last.
  - The claim indicator and the claim count are dropped. Ye et al. (2022) ran a random holdout of this table, and their analyst "A5" scored a normalized Gini of 0.955. That is the score the builder's oracle, which knows which policies claimed, reaches (0.955). The published top score most likely used the claim indicator, which this dataset rightly drops.
- What makes me distrust it: any score read on its level. Exposure alone scores 0.168 on the declared metric against the best model's 0.209. A method below 0.168 has learned less than the length of the observation window.

**5. The metric (MET-1, MET-2, MET-5, MET-8, MET-11)**

- The declared `normalized_gini` is the Kaggle form: the losses of the observed slices, every row weighted 1, sorted by predicted cost.
- The pricing form sorts by predicted loss cost per exposure and accumulates exposure on the x-axis:
  - CAS Monograph 5, Sec. 7.2.4: "Sort the dataset based on the model predicted loss cost... On the x-axis, plot the cumulative percentage of exposures";
  - Frees, Meyers and Cummings (2011) accumulate premium, which is proportional to exposure under a flat base rate;
  - Brauer and Wüthrich (2025) take the time exposure as the Gini's case weight, with the prediction "on the level of a premium rate".
- The metric reason cites Frees et al. for a form that is not theirs, while MET-11 asks the notes to name the original whenever the declared metric is not exactly it.
- The paper that did score this table this way is Ye et al. (2022, Econometrics 10(2):19):
  - a random split into thirds;
  - `claimcst0` predicted with exposure among the inputs;
  - the unweighted normalized Gini, called "of the most interest", reported next to MAE, RMSE, rebalanced RMSE and the total error.

  It reports five measures and recommends using at least two, so it fixes no single metric (MET-5) and the origin stays `context`. It belongs in the reason all the same.

My check (the nine shipped splits; the script is in the run folder): each model quotes a full year (exposure set to 0.9993). The quote is scored by the exposure-weighted normalized Gini of the realised cost per policy-year: `normalized_weighted_gini` with y = cost / exposure and weight = exposure.

| model | declared Gini | quote Gini (my measure) |
|---|---|---|
| Tweedie GLM on cost per year, exposure as weight | 0.209 | 0.125 |
| Tweedie GLM on cost, log exposure a feature | 0.205 | 0.123 |
| Tweedie LightGBM on cost per year, exposure as weight | 0.185 | 0.086 |
| Tweedie LightGBM on cost, exposure a feature | 0.182 | 0.075 |
| squared-error LightGBM on cost, exposure a feature | 0.163 | 0.053 |
| exposure alone | 0.168 | -0.015 (sd 0.029: noise) |

- The five real models come out in the same mean order under both measures (per-split Kendall tau 0.4 to 1.0, mean 0.64). Here the declared metric picks the model I would pick.
- But it ranks exposure alone above squared-error LightGBM on 6 of 9 splits and above Tweedie LightGBM on 3 of 9, although exposure alone is worth nothing at a quote.
- The free log-exposure coefficient (0.31) gains nothing on either measure (0.205 against 0.209; 0.123 against 0.125). This agrees with the builder's finding that the late part of exposure does not lift the declared score.

Answer: **partly**. The metric I would choose is the exposure-weighted Gini of the cost per policy-year: target `claim_cost / exposure`, exposure as the metric's weight and not a feature. I do not propose it outright, for two reasons:

1. With exposure still a feature it rewards the leak. A GLM's cost prediction made without exposure, divided by exposure, scores 0.238 on it, above every honest quote, because short slices carry 7.8 times the cost per year.
2. Taking exposure out of the features reverses the curator's fremtpl2 call. And Data Foundry has no training weight, so a learner would fit an unweighted cost per year, where one claim on a short slice is worth up to $5.2M a year (99th percentile among claimants: $111k).

MET-8's preference for a proper score points to an exposure-weighted Tweedie deviance. It needs positive predictions (the triage's objection), and with exposure as a feature it rewards the leak too: on the cost per year it picked the GLM with the free log-exposure coefficient on 9 of 9 splits. So for this benchmark the declared metric is the workable choice, once its reason is corrected.

**Gaps between the dataset and my decision, ranked by how much they change the task**

1. `exposure` is the observed slice (median 163 days, 1.9% full years), not the one-year contract. It is known only after the observation window and partly cut short by total-loss claims. It turns the target into the cost of a slice, and it gives 80-82% of the declared score to a variable that is 1 for every quote (USE-3, USE-5, LEAK-10).
2. The metric's unit: an unweighted Gini per slice instead of the exposure-weighted Gini per policy-year. The model order is the same on the probes, but the level is inflated and the exposure-alone baseline sits above a real model (MET-1, MET-2).
3. A forced IID split stands in for next year's book (SPLIT-8, USE-8). A random holdout is accepted practice; out-of-time is preferred.
4. Thin rating factors (no no-claim bonus, postcode, make and model, excess or cover type): the task is harder, the decision the same.
5. Unknown claim maturity and the fixed amounts ($200, $353.77): small. Keep them as recorded.

**What an expert would change (recommendations; the curator decides)**

- First curation bullet and `known` (USE-3): every policy's term is one year and known at pricing. The shipped exposure is the part of that year the data observed, known only at the end of the observation window, and it ends early when a total-loss claim ends the policy. A suggested `known` ending: "...and the share of the policy's year observed in the data (a full year 0.9993; median 0.45)".
- Leak note: add the per-year numbers (large claims at 0.107 against 0.005 per policy-year; free log-exposure coefficient 0.31) and the fact that a total-loss settlement ends the policy.
- `fit_reason` (USE-8): name exposure as kept, not as a gap. The gaps are the forced IID split and the target per observed slice.
- Metric reason (MET-11):
  - cite Ye et al. (2022) for this exact form on this table;
  - say that Frees et al.'s form and the CAS Monograph's form are exposure-weighted, per rate;
  - add the exposure-alone baseline (0.168), so readers know where a useful model starts.
- A family question for the curator, covering fremtpl2, frempl, the pricing games and the Spanish 2022-2024 table: if Data Foundry gets a training-weight role, the actuarial formulation (cost per policy-year, exposure as weight, `normalized_weighted_gini`) scores the pricing decision directly and removes the leak.

**Sources**

- insuranceData `dataCar` help page: https://search.r-project.org/CRAN/refmans/insuranceData/html/dataCar.html (also the Rd file of the CRAN tarball)
- de Jong and Heller (2008), ch. 1 excerpt and contents (Cambridge's excerpt): Table 1.1; Sec. 7.4 "Correcting for exposure" (title only)
- actuaRE `dataCar` (Y = claimcst0 / exposure, w = exposure): https://search.r-project.org/CRAN/refmans/actuaRE/html/dataCar.html
- Ye, Zhang, Han, Yu, Zhao and Yang (2022), "Combining Predictions of Auto Insurance Claims", Econometrics 10(2):19: https://www.mdpi.com/2225-1146/10/2/19 (text read from arXiv 1808.08982)
- Goldburd, Khare, Tevet and Guller, CAS Monograph 5, 2nd ed.: https://www.casact.org/sites/default/files/2021-03/8_GLM.pdf (Sec. 2 exposure offsets, 2.7.3, 4.3.1, 7.2.4)
- Frees, Meyers and Cummings (2011), JASA 106:1085-1098, doi:10.1198/jasa.2011.tm10506 (abstract only)
- Brauer and Wüthrich (2025), "Gini Score under Ties and Case Weights": https://arxiv.org/abs/2511.15446
- Boucher, Coulibaly and Trufin (2026), arXiv 2604.02400: https://arxiv.org/abs/2604.02400 (abstract)
- NRMA FAQ on total loss: https://www.nrma.com.au/faq/what-happens-to-my-car-if-my-claim-is-a-total-loss/155 (via a search summary; direct fetch refused)
- the fremtpl2 record (the curator's exposure call of 2026-10-20); the builder's probe outputs (the hurdle Gini per split, the exposure alternatives)
- My scripts and outputs (the metric view and the quote view, per split): in the run folder

</details>

<details><summary>Blind review</summary>

**Verdict: exclude as prepared.** The table is a faithful, leak-free copy of the de Jong & Heller (2008) Australian car-insurance data. The problem is the target: raw claim cost per policy, scored by RMSE or R², has almost no signal any model can reach. The best out-of-fold R² is about 0.002, smaller than the noise between folds, so the task would rank methods by how far they shrink toward the mean. It becomes usable if recast as claim occurrence (binary).

**What the task is.** An Australian motor insurer's pricing actuary estimates the expected claim cost (pure premium) of a one-year private car policy from rating factors when setting the premium. That is a real and common use. The data have 67,856 policies written in 2004 or 2005 and six rating factors (vehicle value, body type, vehicle age band, driver gender, area, driver age band), plus exposure. The target is the total claim amount, which is 0 when there was no claim.

**Concerns, most to least serious**

1. **Claim cost cannot be scored by squared error (decisive).**
   - Evidence, the target:
     - 93.2% of rows are zero (63,232 of 67,856).
     - The 4,624 positive claims have a median of 762 and a maximum of 55,922. The overall mean is 137 and the standard deviation 1,056.
     - A handful of rows carry the squared error around the mean: the top 46 rows (0.07%) make up 42.5% of it, and the top 100 rows 58%.
   - Evidence, 3x3 repeated CV, the same scheme as the task:

     | Model | R² (mean ± sd) |
     |---|---|
     | Mean predictor | 0 (RMSE 1054.9, fold-to-fold sd 55) |
     | Tweedie GLM | 0.0016 ± 0.0009 |
     | Small, regularised LightGBM (Tweedie loss) | 0.0020 ± 0.0009 |
     | LightGBM, squared-error loss | -0.0018 |
     | LightGBM, Huber loss | -0.0056 |

     - A Tweedie GLM fitted in-sample on the test fold itself reaches only R² = 0.0037, so the ceiling is below 0.4%.
     - Tweedie deviance is no better: 73.8 for the mean against 72.6 for the best model.
     - Methods would differ by about 1 RMSE unit against a fold sd of 55, and well-tuned default learners lose to the constant.
   - Change: switch the target to claim occurrence (`claim_cost > 0`, equal to the source column `clm`).
     - LightGBM reaches AUC 0.654 (folds 0.646–0.662), with 4,624 positives, about 1,540 per test fold. That is enough to tell methods apart.
     - The alternative is to keep the regression only if the benchmark can score it with Poisson or Tweedie deviance or a normalised Gini. Even then the margins are thin: Gini 0.19 against 0.17 for "average rate × exposure".
     - Do not recast it as claim size among claimants: n = 4,624 and R² is about 0.01, so there is no signal.

2. **Most of the signal is exposure, a mechanical quantity that is only known after the fact.**
   - Evidence:
     - `exposure` equals days / 365.25. Every value is an exact multiple of 1/365.25, from 1 to 365 days, median 163 days.
     - The claim rate rises steadily across exposure quintiles: 2.4%, 4.2%, 6.9%, 9.3%, 11.4%.
     - For occurrence, AUC is 0.654 with exposure and 0.542 without it. For cost, normalised Gini is 0.19 with it and 0.09 without.
     - The sources call it "The number of policy years" (CASdatasets) and "period from the date of insured to the investigation, with a maximum of one year" (DLSSM `car.insur`).
     - So it is time observed at risk. Actuaries use it as an offset, which is legitimate. But part of it may only be known afterwards: if a policy is cancelled after a total loss, its exposure is cut short. That would be a reverse leak, and I could not rule it out.
   - Change: keep exposure as a feature (standard practice) and document it as an offset. Expect the six rating factors to add only modest lift: occurrence AUC goes from 0.542 to 0.654 once exposure is included.

3. **There is an undocumented spike at the bottom of the claim-cost distribution.**
   - Evidence:
     - The smallest positive claim is exactly 200.00, and 695 claims (15% of positives) sit at exactly 200.00.
     - Other repeated exact amounts: 353.77 (219 claims), 389.95 (94), 390.00 (55), 367.73 (42).
     - These look like a floor or fixed administrative amounts. None of the sources explains them.
   - Change: none needed if the target becomes occurrence. If the regression is kept, note in the dataset card that the claim amounts include these fixed values.

4. **The cover type and some features are poorly documented.**
   - Evidence:
     - The sources disagree on the cover. The CASdatasets page introduces the data with "Third party insurance is a compulsory insurance for vehicle owners in Australia". DLSSM says "full comprehensive Australian automobile insurance policies". Rating on vehicle value and body type fits comprehensive (own-damage) cover better.
     - `area` A–F is anonymised.
     - The unit of vehicle value is "$10,000" in insuranceData but "thousands of AUD" in CASdatasets. The values (0.18–34.56) fit the $10,000 reading.
   - Change: describe the cover as "private motor, one-year policies (cover type per de Jong & Heller)", and give the vehicle value unit as $10,000.

5. **The random split is acceptable, but repeated policyholders cannot be checked.**
   - Evidence:
     - There is no date or year column (2004 and 2005 are mixed) and no policy ID, so a random IID split is the only option. It matches cross-sectional pricing well enough.
     - There are 378 exact duplicate rows (707 rows involved). All of them have `claim_cost` = 0, so they are coincidences from coarse features, not copied records.
     - I tested whether policies were cut into calendar-year pieces, looking for pairs with identical rating factors whose exposures sum to 365 days. There is no excess: 116 pairs at 365 days against 92–110 at neighbouring sums.
     - A policyholder who renewed from 2004 to 2005 could still appear twice. I cannot check this.
   - Change: none.

6. **Preparation is sound (minor notes only).**
   - The rows match the public insuranceData `dataCar` file exactly (Rdatasets CSV): after mapping codes, 0 mismatches over 67,474 distinct rows.
   - The leaking columns `clm` and `numclaims` were dropped, which is correct; `numclaims` would make the task trivial. The constant `X_OBSTAT_` was dropped.
   - 53 rows with `veh_value` = 0 became NaN. That is sensible: a value of 0 is a placeholder.
   - Body codes were expanded to names (for example `HBACK` to Hatchback). The ordinal age bands are stored as int and the categoricals as category.
   - The data are real. Claim counts by driver-age band (496, 932, 1,113, 1,104, 614, 365, total 4,624) match Table 1.1 of the book excerpt exactly.
   - Minor: this is a well-known teaching dataset (insuranceData, CASdatasets, actuaRE), so methods built on LLMs may have memorised it.

**What I could not check**
- The original Macquarie companion site and the book's full text: the exact definition of exposure, the cover type, and what the 200.00 amounts mean.
- Whether claims cut exposure short through cancellation.
- Whether the same policyholder appears in both years.
- Which metric the benchmark uses. I assumed RMSE or R² for regression.
- Whether the benchmark already contains other zero-inflated claim tables (for example freMTPL2), which would make this one redundant.

**Sources**
- [insuranceData dataCar documentation](https://search.r-project.org/CRAN/refmans/insuranceData/html/dataCar.html)
- [CASdatasets ausprivauto](https://dutangc.github.io/CASdatasets/reference/ausprivauto.html)
- [DLSSM car.insur](https://r-packages.io/datasets/car.insur)
- [actuaRE dataCar](https://search.r-project.org/CRAN/refmans/actuaRE/html/dataCar.html)
- [Cambridge book excerpt](https://assets.cambridge.org/97805218/79149/excerpt/9780521879149_excerpt.pdf)
- [Rdatasets CSV of dataCar](https://vincentarelbundock.github.io/Rdatasets/csv/insuranceData/dataCar.csv)

</details>

<details><summary>Precedent check</summary>

**Precedent check (precedent-checker, 2026-11-01): australian_vehicle_insurance_2004_2005**

**Verdict.** Most of the definition follows its precedents: exposure as a feature (fremtpl2, Andrej), the drops, the cleaning, the 200 floor, the TP readings and the context Gini. Two real departures and one wording slip need the curator:
1. the forced-IID split (SPLIT-8 as written) sits against Andrej's own `No` on how_much_did_it_rain and his statement of the same day, "Forced IID is to be avoided at all costs";
2. the target ships on the raw scale while its two siblings from this run ship log1p, with no reason given here;
3. `fit_reason` names the kept exposure leak as a gap (USE-8, wording only).

The register's 14 flags touch none of the rules this dataset uses (CLEAN-19, SPLIT-9/10/14, PROV-13, TP-10 and the probe-mechanism flags). No formal exception is recorded in this definition.

What the evidence is: the run's decision register, the records of the siblings and precedents, the Cases tables of `leak_checks.md`, `splits.md`, `metrics.md` and `use_case.md`, and the sibling definitions of this run. Two quick probes of my own ran on the shipped splits (untuned LightGBM, 300 trees; scripts in the run folder).

**Per decision**

| Decision (rule) | Standing | Closest precedents | What sets it apart, or not |
|---|---|---|---|
| Use case "for example", fit approximate (USE-1, USE-8) | consistent; `fit_reason` wording departs (no reason given) | USE-1 Methods ("say for example"; diamonds, bank_customer_churn and about 75 definitions of the working copy open their use case with "For example"); account_debt_south_africa (approximate: one snapshot stands in for a forecast, Lennart); kick, homesite_quote_conversion, house_sales (Lennart, 2026-10-21: a kept leak is named in `fit_reason` "as kept, not as a gap") | The split alone makes the fit approximate. But `fit_reason` also lists "the time in force is known only after the period" as a gap, and the notes call that the kept leak ("Potential leak, kept on purpose"). The siblings frempl and spanish word it the same way. Prompt 3. |
| 200 floor kept as recorded (USE-5, CLEAN-11) | consistent (an AI suggestion, still needs a CC) | fremtpl2 CC (Andrej, 2026-10-20): the fixed IRSA-IDA amounts, 42.3% of claims, stay in the target as point masses; policy question 2 (Andrej, 2026-10-30): how a source codes its values is a cleaning choice, no reason for a No; CLEAN-11 (values that are only unusual stay) | Same kind of fact as fremtpl2: a recording convention inside the positive part, kept as published. Labelled correctly as "the suggested call of 2026-10-30, for the curator to confirm". |
| `exposure` kept as a feature, late part noted (LEAK-10 second clause, LEAK-6) | consistent | fremtpl2 CC (Andrej, 2026-10-20): "`Exposure`: a feature, not a divisor. The contracted period is known at pricing (a mid-year cancellation also shortens it)"; onlinenewspopularity (LEAK-10 and LEAK-6 as amended 2026-10-26, Lennart): late values that cannot be located row by row stay when the traced part shows no gain; distribution_transformers_at_cauca_department (Lennart, 2026-10-21): dropped where a gain may sit on the late rows; siblings: spanish (the cancelled portfolio years can be located from `policy_status`, so exposure is reset to 1 there, LEAK-7), frempl (the record dates that locate an early end are dropped, `Exposure` kept) | Follows fremtpl2. The new measured fact (write-offs end policies: median exposure 0.37 against 0.65, p < 1e-20) is handled by LEAK-10's second clause. Apart from cauca: the late part can only be located through the target (claim / vehicle value), and the traced part shows no gain in the declared metric (hurdle 0.191 against 0.195 for claim probability alone). Apart from spanish: no status or end date to locate it. Two caveats. (i) LEAK-10's clauses are "a case-by-case judgment of the curator, never a default", so the fremtpl2 precedent does not settle this keep by itself. Builder issue 1 correctly sends it to the curator. (ii) The "no gain" holds for the Gini only. Exposure does add R^2 +0.019 (9 of 9) to the claim-size stage. If the curator chooses the `rmse` fallback (issue 3), this has to be measured again. The test also differs in form from onlinenewspopularity's (masking the traced cells there; the contribution of a model stage here), since masking by claim size would read the target. |
| Forced IID split, `ForcedIIDFromTemporal` (SPLIT-8, USE-8) | consistent with the rule; departs from the same curator's stated view, no reason given | SPLIT-8 as written (Must; Lennart, 2026-10-12, amended 2026-10-21); account_debt_south_africa, mobile_churn and the churn snapshots (forced IID, Lennart); sibling frempl (`ForcedIIDFromTemporal`, same run). fremtpl2 CC (Andrej, 2026-10-20): temporal on a year index inferred from `IDpol`. how_much_did_it_rain CC (Andrej, 2026-10-30): `No`, "forced IID would introduce leaks for this task ... if the data is temporal but a temporal split is not possible, we cannot split the data and reject it"; in chat on SPLIT-8: "Forced IID is to be avoided at all costs" (SPLIT-8 left unchanged for now) | Apart from fremtpl2: no id and coarse age bands, so no year can be rebuilt by renewal links. Against how_much_did_it_rain: Andrej's `Yes` (2026-10-30) was given on a record that reads "Regime IID: one policy-year per row, no dates, no ids". The builder reframed the split as forced from temporal at /add-dataset, and the definition does not address the curator's statement. A distinguishing fact is evident from the data but not written down. Prompt 1. |
| Drop `clm`, `numclaims` (LEAK-10: parts of the target) and `X_OBSTAT_` (constant) | consistent | fremtpl2 CC (`ClaimNb` dropped, Andrej, 2026-10-20); the claim parts dropped in frempl and spanish | Same fact: the same claims as the target. |
| `veh_value` 0 made missing (CLEAN-10, CLEAN-11) | consistent | churn_telco_south_asia (impossible values made missing; Tensions table); CLEAN-11 as amended 2026-10-21 | A car worth $0 next to a minimum of $1,800 is no value. The row stays. |
| Age bands kept as numbers, body codes labelled (CLEAN-14, CLEAN-12) | consistent | CLEAN-14 as amended 2026-10-21 (Lennart): "keep it a number" when the context says it is ordered; spanish keeps its ages as numbers | Bands are ordered ages. The labels come from CASdatasets for the same rows. |
| 378 exact repeats kept (LEAK-18) | consistent | sepsis_survival_minimal_clinical_records (few features, real units, kept); fremtpl2 (38% of rows repeat a feature vector, kept by the CC); liberty_mutual_fire_peril_loss_cost (exact copies kept, same run) | Seven features, two of them rounded. All repeats are no-claim rows. |
| Target `claim_cost` on the raw dollar scale, no `target_transform` (MET-3) | consistent with the 2026-10-30 suggestion table (`claimcst0`); departs from both sibling drafts, no reason given | frempl_french_motor_personal_line and spanish_motor_insurance_coverage_level_2022_2024: log1p with `target_transform="log1p"` and the Gini on the amount, same run (AI drafts; the spanish notes cite this dataset as the counterexample); MET-3 (Lennart, 2026-10-21: "ship the target on the modelling scale, score on the original scale"); allstate_claims_severity (log), forest_fires (zero-inflated area, log1p, MAE in hectares) | MET-3 allows either scale, so this breaks no rule, but like cases differ. The reason spanish gives holds here too: on the 9 shipped splits, squared-error LightGBM ranks at Gini 0.195 on log1p against 0.167 on the raw cost (+0.028, paired SE 0.009, better on 7 of 9; Tweedie LightGBM on the raw cost 0.180). The builder's Tweedie GLM (0.205, raw) is still best. The Gini does not change under a monotone inverse; only what squared-error models fit changes. Prompt 2. |
| Metric `Metric.from_context("normalized_gini")` (MET-11, MET-13) | consistent; a new kind of precedent | MET-11 context origin (diamonds, Lennart, 2026-10-21); the family suggestions of 2026-10-30 (AI; Andrej asked for calls per dataset); frempl and spanish (same declaration); `normalized_gini` already in `data_foundry.v2.metrics` (Allstate), so MET-13 holds | It replaces the screening's fallback `rmse` (AI, 2026-10-27), as the 2026-10-30 Assessment proposed. The binary-Gini precedents (porto_seguro, kick: roc_auc by identity) do not apply to a regression target. This is the first context call for a ranking metric on a regression target, and no curator has confirmed it yet. Settling it here settles it for frempl and spanish as well. Builder issue 3 is the place: one family decision. |
| Task probe readings (TP-2, TP-4) | consistent | forest_fires (TP-2: a small real signal kept); california_house_prices_2020 and aps_failure (TP-4: a natural core kept, Lennart, 2026-10-06); fitness_club (retired, the raw feature beat the methods, 2026-10-05) | Every family beats the dummy Gini on 9 of 9. Exposure is the natural core of a pure premium. The GLM beats exposure alone on 8 of 9 (+0.038, SE 0.010). |

**Drift and amendments**

* **Andrej's split decisions.** The same day, 2026-10-30, he gave `Yes`, priority 5, here (on a record that read IID), sent how_much_did_it_rain to `No` for forced IID, and said in chat that forced IID is to be avoided at all costs. Earlier, on fremtpl2, he built a temporal split from an inferred order rather than accept IID. These calls point one way and the draft points the other: prompt 1. frempl_french_motor_personal_line, from the same run, is in the same position.
* **Exposure as a feature.** No rule or Cases row in the knowledge files holds this call. It lives in fremtpl2's CC and the AI's suggestions of 2026-10-30. After this run four definitions carry it (fremtpl2, frempl, spanish, australian), and three of them note an exposure cut short by the outcome (write-offs here, early ends in frempl, cancellations in spanish). These apply LEAK-10's second clause rather than depart from it, so no amendment is formally due. Once the curator confirms them, a Cases row under LEAK-10 ("Keeping the rules current" in principles.md) would let the next insurance table follow without arguing it again.
* **Third exception.** None: the definition records no `Exception to` line.

**One fact for the split auditor (it touches SPLIT-8's "cost measured where the data has any")**

The file order is not random: the mean exposure of 20 file blocks varies with an SD of 0.035, against at most 0.007 in 200 permutations. The claim rate does not vary beyond chance (p 0.12). account_debt_south_africa measured its forced-IID cost by a file-block holdout. Done the same way here (train on the first k quarters of the file, test on the next quarter), the Gini shows no drop: Tweedie LightGBM 0.168, 0.189, 0.208 forward against 0.127, 0.174, 0.181 for random splits of the same sizes; log1p 0.191, 0.199, 0.181 against 0.197, 0.198, 0.186. These are single splits, and nobody knows whether the order is time.

**Reflection prompts**

1. **Consistency check (AI, 2026-11-01):** the draft of australian_vehicle_insurance_2004_2005 ships `ForcedIIDFromTemporal` under SPLIT-8 (your `Yes` of 2026-10-30 was given on a record that read "Regime IID"). That differs from how_much_did_it_rain (`No`, 2026-10-30, you: "forced IID would introduce leaks for this task"; in chat: "Forced IID is to be avoided at all costs"). What sets australian apart?
   (a) No serial dependence. Every row is a distinct one-year policy without an id. The hidden-group probe finds no grouping (best gap +0.004), and the 378 repeated rows are all no-claim. So a random split hands no test row a neighbour's outcome the way storm-correlated gauge hours do. Its cost is the year's claim level only, and a file-order forward holdout shows no drop. Recorded as the fact that sets it apart from how_much_did_it_rain.
   (b) Treat it like how_much_did_it_rain: `No` as forced IID, or, if you see it so, a use case that is IID by nature (rating the policies of one portfolio period), written in the task summary.
   (c) Reopen how_much_did_it_rain to SPLIT-8 as written (2nd Tier, the AI's consistency check of 2026-10-30).
   (d) Amend SPLIT-8 (for example: forced IID only where rows share no unit or period outcome; or forced IID is a reject). This is a deliberate change that reaches the 17 forced-IID datasets of the working copy and frempl from this run.
2. **Consistency check (AI, 2026-11-01):** the draft ships `claim_cost` on the raw dollar scale. That differs from frempl_french_motor_personal_line and spanish_motor_insurance_coverage_level_2022_2024 (same run, same Gini on the amount, shipped as log1p with `target_transform="log1p"`). Here too, log1p lifts squared-error LightGBM from Gini 0.167 to 0.195 (7 of 9 splits). What sets australian apart?
   (a) The source's own models are fit to the raw cost with a log link: de Jong and Heller's Tweedie and zero-adjusted inverse Gaussian GLMs, Sec. 8.3 and 10.4-10.5, read from the contents only. That makes the raw cost this dataset's modelling scale (MET-3, "ship the target on the modelling scale"). freMPL and the Spanish table have no source model. Recorded in the notes.
   (b) Treat it like the siblings: log1p with `target_transform="log1p"`.
   (c) Reopen frempl and spanish to the raw amount.
   (d) Add a MET-3 line for the family (zero-inflated amounts scored by a ranking metric ship on one scale).
3. **Consistency check (AI, 2026-11-01):** `fit_reason` names the exposure's late part as a gap ("known only after the period"), while the notes keep it as "Potential leak, kept on purpose". That differs from kick, homesite_quote_conversion and house_sales (USE-8 as amended 2026-10-21, Lennart: a kept leak is named in `fit_reason` as kept, not as a gap). The fit stays approximate on the split alone either way. What sets australian apart?
   (a) The realised time in force stands in for the contracted term the underwriter knows: an input gap, not a leak. The "Potential leak" label would then change to a plain note.
   (b) Treat it like kick: reword `fit_reason` to name the exposure as kept. frempl and spanish use the same wording.
   (c) Reopen the USE-8 amendment's cases.
   (d) Amend USE-8.

**Builder's draft issues against precedent**

1. Exposure kept: consistent (fremtpl2, onlinenewspopularity). It needs the curator's case-by-case call under LEAK-10, and it is tied to the metric of issue 3.
2. Forced IID: consistent with SPLIT-8 but not with Andrej's view of 2026-10-30 (prompt 1).
3. Gini or `rmse`: consistent with MET-11's context origin and with the family. It is the first call of its kind, so decide it once for the three.
4. 200 floor: consistent (fremtpl2's point masses, policy question 2).
5. Cleaning: consistent (CLEAN-10/11/14).

The builder's own note "align the family (MET-3)" holds: prompt 2.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (2026-11-01): australian_vehicle_insurance_2004_2005**

**Position: ship after note changes.** No evidence agent found a validity problem that the notes cannot settle. The
data, the split and the columns stay as defined. What has to change is wording: how `exposure` is described, the
support given for the metric, the split note and the note on duplicates. One call is a weighing call (raw or log1p
target), and the dataset ships either way.

**1. A real pricing task on verified data, which the curator has already accepted (P3 USE-1, Must; P5 PROV-4 and
PROV-16).**
- Evidence:
  - The domain practitioner: "P3 (a real use case) is solid: tariff pricing is the core actuarial decision, and this
    is a real, documented portfolio."
  - The copy matches all 18 cells of the book's Table 1.1 (claim-auditor #9).
  - CASdatasets agrees with it on 67,856 of 67,856 rows (#10), and the blind reviewer found 0 mismatches against
    Rdatasets.
  - Both sha256 hashes match, and the licence is GPL-2 (#31).
  - CC (2026-10-30, Andrej): `Yes`, priority 5.
- Why it outranks the objections: every other objection sits at P4 or below and has a fix in the definition or the
  notes. The Tensions table settles both kinds: "fix the leak and keep the task" (P3 against a leak), and "keep the
  task; fix what is cheap and safe" (P3 against cleaning). Under "Who decides", the curator's CC outranks any AI
  assessment.
- Conceded, cannot be verified: whether the costs are paid or incurred, and how far they had developed (LEAK-24,
  claim-auditor #37). The Gini ranks the losses as the insurer booked them, so this does not block (claim auditor,
  domain practitioner).

**2. `exposure` stays: its late part lowers the score instead of raising it (P4 LEAK-10 second clause, Must,
narrowing LEAK-6; LEAK-11, Should, narrows LEAK-10).**
- Evidence that the traced late part brings no gain:
  - Offset test (column auditor, 9 shipped splits): a free feature against a proportional offset gives -0.0009
    (SE 0.0059, better on 4 of 9). A feature floored at 0.1 years gives -0.0025 (SE 0.0029).
  - Free log-exposure coefficient (domain practitioner): no gain on either measure (0.205 against 0.209).
  - Counterfactual (claim-auditor #17): give the write-offs a counterfactual exposure, and the Gini rises from 0.182
    to 0.31-0.32 on 18 of 18 runs. The late part hurts the score, which is the LEAK-11 case.
- Precedent with the same facts: fremtpl2, CC (2026-10-20, Andrej): "`Exposure`: a feature, not a divisor ... (a
  mid-year cancellation also shortens it); dividing would inflate short policies' targets". freMTPL2's exposure is
  also cut by records and by early ends. Treat like cases alike.
- Conceded: the definition misdescribes the column. The notes, `known` and the record's Assessment call it the
  contracted period, known at pricing. It is the share of the year inside the observed period (1.9% full years), and
  some claims cut it short: 147 excess claims at 0.2 years or less, not only the 193 write-offs (column auditor).
- Mildest remedy: rewrite the "Potential leak, kept on purpose" bullet. It should say that the column is the share
  of the year in the window and that the shortening also acts on claim occurrence. It should give the offset test
  and the LEAK-11 counterfactual as evidence. Fix `known` to match, and name `exposure` in `fit_reason` as kept, not
  as a gap (USE-8, as in kick and homesite).
- Why it outranks "drop it" or "re-target to the rate": on the remedy ladder, the note resolves the problem because
  the traced part shows no gain. Dropping the column cuts the best Gini from 0.205 to 0.130 and removes the natural
  core of a pure premium. The re-target departs from the curator's fremtpl2 call. LEAK-10's clause is the curator's
  case-by-case call: I recommend the keep.

**3. The declared Gini picks the model a pricing actuary would pick, and RMSE cannot score this task (P6 MET-1 and
MET-2, Must; MET-11 context, Must).**
- Evidence for the Gini:
  - On the domain practitioner's own quote measure (exposure-weighted Gini on the cost per policy-year), the five
    real models come out in the same mean order. Kendall tau per split is 0.4 to 1.0, mean 0.64. The practitioner's
    verdict: "for this benchmark the declared metric is the workable choice, once its reason is corrected."
  - Ye et al. (2022, Econometrics 10(2):19) scored this exact table this way: the unweighted normalized Gini, a
    random split, exposure among the inputs, called "of the most interest". Allstate's challenge used the same
    metric.
- Evidence against RMSE: the top 46 rows hold 43% of the sum of squares, and the best R^2 is 0.002 (#27). The blind
  reviewer found that default learners lose to the constant.
- The blind reviewer's "exclude" assumed RMSE ("I assumed RMSE or R² for regression"). It names a normalized Gini as
  the condition for keeping the regression, and that is what ships.
- Conceded: the reason cites Frees et al. (2011) for a form that is not theirs. Theirs is premium- or
  exposure-weighted (claim-auditor #25).
- Mildest remedy: reword the reason (MET-11). Cite Ye et al. (2022) and Allstate, describe Frees et al. correctly,
  and add the exposure-alone baseline of 0.168.
- Why it outranks the exposure-weighted Gini on the rate:
  - Data Foundry has no training weight, so learners would fit an unweighted rate, where one claim on a short slice
    is worth up to $5.2M a year (domain practitioner).
  - With `exposure` a feature, that metric rewards the leak: 0.238, above every honest quote.
  - It reverses the fremtpl2 call ("dividing would inflate short policies' targets").
  - The `rmse` fallback fails MET-1: it scores shrinkage toward the mean.

**4. A small, real signal that separates methods; not trivial (P6 TP-2, Should; TP-4, Must).**
- Evidence:
  - Every model family beats the dummy Gini on 9 of 9 splits (builder, #34).
  - The Tweedie GLM beats squared-error LightGBM by +0.042 (SE 0.007).
  - Each test fold holds 1,512-1,582 claimants (#23).
  - Exposure alone scores 0.168 against the GLM's 0.205, and the GLM wins on 8 of 9 splits (+0.038, SE 0.010).
- Precedents: forest_fires (TP-2), california_house_prices_2020 (TP-4, a natural core kept).
- Why it outranks "exposure earns 82% of the score": TP-4 needs the raw feature to match or beat the methods fold by
  fold, and it does not. Time on risk is the expected core of a claim cost.

**5. The forced IID split is SPLIT-8 as written, and the facts set this case apart from how_much_did_it_rain (P4
SPLIT-8, Must).**
- Evidence:
  - There are no dates and no ids. frempl, from the same run, ships the same tag, as do account_debt_south_africa and
    mobile_churn.
  - The hidden-group probe finds 0 hits.
  - A split grouped on the exact feature vector scores within noise of the shipped one: 0.194 and 0.208 against
    0.182 and 0.205 (split auditor).
  - No renewal pairs: 116 at 365 days against a mean of 102.
  - The release looks like one 365-day observation period (no row has 366 days), so even a split by inception year
    would not test a later claim level (split auditor).
  - CAS Monograph 5, Sec. 4.3.1 accepts a random holdout.
  - Andrej's `Yes` was given on a record that read "Regime IID".
- Conceded: the CC on how_much_did_it_rain ("forced IID would introduce leaks"; in chat, "Forced IID is to be avoided
  at all costs") is a real consistency check (case 2).
- Mildest remedy: record the fact that sets this case apart, the precedent checker's option (a): no measured channel
  by which a random split hands a test row its neighbour's outcome. Make the split auditor's two note edits: replace
  the "split by year" sentence, and add that the cost of the forced split cannot be measured.
- Why it outranks the objection: SPLIT-8 is an unamended Must, and rules win over precedents. Making forced IID a
  reject would be an amendment that reaches 17 datasets and frempl, not a fact about this one.

**6. The cleaning is minimal and matches the expert state; the slips are in wording (P7 CLEAN-10 and CLEAN-11,
Should; LEAK-18 and LEAK-19, Should).**
- Evidence:
  - The asserts confirm that `clm` and `numclaims` are parts of the target.
  - 53 vehicle values of 0 are made missing.
  - The floor at 200 is kept as recorded, as fremtpl2 kept its IRSA-IDA point masses (42.3% of claims, Andrej's CC).
    The domain practitioner agrees: "they are what the insurer booked."
- Conceded:
  - "Natural repeats" is refuted: 378 copies against 120-125 by chance (#21). All are no-claim rows, and dropping
    them moves the Gini by +0.0045.
  - Smaller slips: the band counts (#9), `driver_gender` (the sources say policyholder), "area of residence" (no
    source read says so), and the book sections that were not read.
- Mildest remedy: fix the notes. Dropping the copies under LEAK-19 is also cheap and safe, and the dataset stays
  either way.

**7. The raw-dollar target is the actuary's modelling scale; aligning with the siblings is a weighing call, not a
blocker (P6 MET-3, Must, which allows either scale; P7 CLEAN-16, Should, "case by case").**
- Evidence:
  - CAS Monograph 5, Sec. 2.7.3 models "dollars of loss ... using the Tweedie distribution": a log link on raw
    dollars, not a log1p target.
  - On the raw target the best model is the Tweedie GLM (0.205). log1p helps only squared-error learners: 0.195 to
    0.197.
- Conceded: frempl and spanish ship log1p (consistency check, case 2). On the raw scale, squared-error LightGBM
  (0.163) falls below the exposure-alone baseline (0.168).
- Mildest remedy: record the actuarial modelling scale as the fact that sets this case apart, or align with the
  siblings (one line, `target_transform="log1p"`). Either way the Gini is computed on dollars and the dataset ships.

**Judgment record (advocate)**

```text
Verdict: ship after changes (notes only; target scale a weighing call).
Validity: USE-1 holds (CC Yes p5); PROV-4/16 hold (Table 1.1, CASdatasets row by row); LEAK-10 triggered for
  `exposure`, kept under its second clause with LEAK-11 (offset test -0.0009 SE 0.0059; counterfactual +0.13), note
  rewritten; SPLIT-8 holds (forced IID; the fact that sets it apart from how_much_did_it_rain recorded); LEAK-24
  cannot be verified, not blocking.
Value: TP-2 small real signal (9/9 above the dummy); TP-4 not trivial (GLM beats exposure alone 8/9); MET-1/2 hold
  (same model order as the practitioner's quote Gini), MET-11 reason reworded (Ye et al. 2022, not Frees).
Quality: CLEAN-10/11 hold; LEAK-18 wording refuted, copies harmless (+0.0045); MET-3/CLEAN-16 raw scale defensible.
For the curator: the exposure keep (LEAK-10 clause); the forced-IID consistency check; raw or log1p.
```

</details>

<details><summary>Critic</summary>

**Critic, opening brief (critic, 2026-11-01): australian_vehicle_insurance_2004_2005**

**Verdict: ship only after changes.** No change touches the rows, the split or the metric's formula. All of them are in the definition's text, plus three calls only the curator can make. No point is a Must that cannot be fixed, so I ask for no exclusion. As defined, though, the dataset has three faults. It states a prediction point that its main feature does not meet. It cites a metric source for a form that is not that source's. And it ships a forced-IID split the curator has not ruled on, which by his own statement of 2026-10-30 he would reject unless a fact sets it apart.

**1. `exposure` is called known at pricing, and it is not (P3 USE-3, Must; P4 LEAK-10, Must).**
- Problem: three places describe a contract term. The prediction-point bullet says "the period the policy is on risk [is] known then". `known` says "the share of a year the policy was in force". The record's Assessment says "the contracted period is known when the policy is priced". But every row is a one-year contract (insuranceData Rd). The column is the part of that year inside an observation window, and the outcome cuts it short.
- Evidence:
  - 98.1% of rows fall short of a full year. The day counts are close to uniform, the median is 163 days, and no row has 366 days (claim auditor #14, split auditor issue 1, practitioner sec. 1).
  - Policies of 7 days or less claim 1.27 times per policy-year, against 0.14-0.17 above 0.2 years. That is 147 excess claims at 0.2 years or less. Without the claims at 80% of the vehicle's value or more, the rate is still 0.85 per policy-year at 0.02 years or less (column auditor).
  - A free log-exposure coefficient comes out at 0.29-0.31 in a Tweedie GLM and 0.73 in a Poisson GLM of the count. Proportional time on risk would give 1.
  - The note names only the 193 write-offs, and its test (claim size against claim probability) misses the frequency channel (claim auditor #17).
- Effect on the task: at a real quote, exposure is 1 for every policy. Yet exposure alone earns 0.168 of the best 0.205 on the declared metric (82%), and -0.015 on the practitioner's quote measure. The mechanism matches heart_failure `time` ("follow-up ends at death"), which the LEAK-10 Mechanisms table drops.
- What saves the keep, which the definition does not yet say: the traced late part brings no gain and lowers the score.
  - With exposure as an offset only, the Gini is 0.1833, against 0.1824 as a free feature (SE 0.0059). Floored at 0.1 years it is 0.1849.
  - When the write-offs get a counterfactual exposure, the Gini rises from 0.182 to 0.31 on 18 of 18 runs.

  That is LEAK-11 (Should, narrows LEAK-10), and it is the fact that sets this case apart from heart_failure. The fremtpl2 reason ("the contracted period is known at pricing") does not carry over: here the contracted period is 1 on every row.
- Remedy (fix the definition text):
  - Reword the prediction-point bullet, `known` and the Assessment to "the share of the policy's year observed in the data; a policy ends early after a total loss".
  - Rewrite the leak note with the frequency excess, the offset and floor test and the counterfactual, and cite LEAK-11.
  - LEAK-10's clauses are "a case-by-case judgment of the curator, never a default". So the curator confirms the keep on this evidence; the fremtpl2 precedent does not settle it.

**2. `fit_reason` names the wrong gaps (P3 USE-5 and USE-8, Must).**
- Problem: the target is the cost of the observed slice, not the cost per policy-year the actor prices. The practitioner calls it "the right quantity in the wrong unit", and actuaRE's copy of this table ships `claimcst0 / exposure` with weight `exposure`. How the label was built is also undocumented:
  - paid or incurred, and at what date;
  - the per-claim floor of 200;
  - 27.5% of claimants sit on 12 repeated amounts (claim auditor #37);
  - the sources disagree on the cover: third party on the CASdatasets page, comprehensive in DLSSM (blind reviewer, point 4).

  Meanwhile `fit_reason` lists the kept exposure leak as a gap. USE-8 wants a kept leak named "as kept, not as a gap" (kick, homesite_quote_conversion, house_sales).
- Effect: the fit is rightly approximate, but `fit_reason` gives the reader the wrong reasons.
- Remedy (text): `fit_reason` names three gaps: the forced split, the target per observed slice, and the undocumented label construction (USE-5 lets such a label ship as approximate with a note). It names exposure as a kept potential leak.

**3. The forced-IID split has no curator ruling, and its note is wrong (P4 SPLIT-8, Must; consistent judgement, case 2).**
- Problem: SPLIT-8 allows `ForcedIIDFromTemporal`, but asks the note to say what a dated split would change and to measure the cost where the data allows. The note says "a split by year would test a model on a later year's portfolio and claim level". The data looks like one accounting year: uniform slices, 1.9% full years, no 366-day row although 2004 was a leap year (split auditor issue 1). If so, a split by inception year would test no later claim level. The note gives no cost estimate either.
- New fact, against one proposed fix: the split auditor suggests writing "the file order is shuffled". It measured the pipeline's frame, which is shuffled (its script reads the `dataset_io` frame). On the raw `dataCar.csv`, I measured:
  - a lag-1 autocorrelation of exposure of 0.094 (0.002 shuffled);
  - 12.2% of adjacent rows with the same day count (0.3% shuffled).

  This agrees with the column auditor, the claim auditor and the precedent checker. A forward holdout over file quarters shows no drop in the Gini (Tweedie LightGBM 0.168, 0.189, 0.208, against 0.127, 0.174, 0.181 on random splits; precedent checker). But nobody knows whether the file order is time.
- Consistency: on 2026-10-30 Andrej sent how_much_did_it_rain to `No` for forced IID: "if the data is temporal but a temporal split is not possible, we cannot split the data and reject it", and "Forced IID is to be avoided at all costs". He gave his `Yes` here on a record that read "Regime IID: one policy-year per row". The builder made the split forced-from-temporal afterwards. The definition gives no fact that sets this case apart. Without one, case 2 says to treat it like how_much_did_it_rain.
- Remedy (text, then the curator's call):
  - Rewrite the bullet. The data covers one observation period of about a year, so a temporal test needs another year's extract. The raw order is not random, but it shows no trend in the claim rate, and the file-quarter forward holdout shows no drop. The rows are independent policies with no hidden group (split auditor issue 3). A later year shifts mostly the level, which the Gini ignores.
  - Then put the precedent checker's prompt 1 to the curator. Exclusion only if he applies the how_much_did_it_rain standard.

**4. The duplicates are called natural, but they run at three times chance (P4 LEAK-18, Should).**
- Evidence:
  - 378 copies, against 120-125 when exposure is shuffled among the no-claim rows.
  - 152 copies among the 1,129 full-year rows, against 11.6 (claim auditor #21).
  - The full-year cohort is rich in trucks and panel vans: likely fleets that start on the window's first day (split auditor issue 3).
- Effect: none on the score. Dropping the copies changes the Gini by +0.0045, and a grouped split scores within noise.
- Remedy (note): replace "plausible ... natural" with the chance baseline and the measured lack of effect. Keep the rows; a LEAK-19 drop is optional.

**5. Claims about the book come from its contents page (P5 PROV-16 and PROV-17, Must).**
- Problem: the notes and the metric reason say the book fits Tweedie and ZAIG models to this table (Sec. 8.3, 10.4-10.5) "and scores no held-out prediction". Only chapter 1 and the contents were read, and those section titles name no data set (claim auditor #11). Separately, "5,742 to 6,547 policies per band" is wrong: the bands hold 5,742 to 16,189 (#9).
- Effect: the claim is load-bearing. It is the MET-1 basis for a context metric, and the only fact offered for the raw target scale (precedent checker, prompt 2a).
- Remedy: mark these claims unverified (PROV-17), or ask the curator for the book: Sec. 7.3-7.4, 8.3, 10.4-10.5, and p. 15, which also describes `exposure`, `area` and perhaps the cover. Fix the band wording.

**6. The metric's stated support is not the declared metric (P6 MET-1 and MET-11, Must).**
- Problem: the reason cites Frees, Meyers and Cummings (2011) and Allstate.
  - Frees orders by relativity and accumulates premium, which is exposure-weighted.
  - CAS Monograph 5 (Sec. 7.2.4) sorts by loss cost per exposure and accumulates exposures.
  - Every Allstate row is a full vehicle-year.

  The declared metric is unweighted, on slices of 1 to 365 days (claim auditor #25-26, practitioner sec. 5). `changes` also calls it "the insurers' ranking metric".
- Effect: on the declared metric, exposure alone (0.168) beats squared-error LightGBM on 6 of 9 splits, though it is worth nothing at a quote. Frees' form gives the GLM 0.102 instead of 0.200. The real models still come out in the same order (practitioner, mean Kendall tau 0.64), so the metric can stay.
- The Gini is load-bearing. Under the record's fallback `rmse`, the best R^2 is 0.002 (in-sample ceiling 0.0037), and squared-error and Huber LightGBM lose to the mean (blind reviewer, point 1). The blind reviewer's "exclude as prepared" is exactly that case.
- Remedy (text):
  - Cite Ye et al. (2022, Econometrics 10(2):19). They scored this table with this unweighted Gini, on a random split, with exposure as an input. They report five metrics, so the origin stays context (MET-5).
  - Describe Frees and the CAS Monograph as the weighted per-rate form.
  - State the exposure-alone baseline of 0.168.
  - The curator confirms the Gini and strikes the `rmse` fallback from the record. The weighted per-year form is a family question: Data Foundry has no training-weight role, and with exposure as a feature that form rewards the leak (0.238).

**7. The target scale and two column names depart from the siblings and the sources (P7 CLEAN-16 and MET-3, Should; quality, no reason to exclude).**
- Evidence (column auditor, problems 2-5):
  - This dataset ships raw dollars; frempl and spanish ship log1p under the same family call, and no reason is recorded here. log1p lifts squared-error LightGBM by +0.028 to +0.034 Gini (7 to 9 of 9 splits).
  - CASdatasets calls `driver_gender` the policyholder's gender.
  - "Area of residence" is in no source read.
  - 1,925 positive costs carry float noise.
- Remedy:
  - One family call on the scale, with its reason recorded. Tweedie log-link practice favours raw dollars.
  - Rename `driver_gender` to `gender`, or note that the sources differ.
  - Write "an area code A-F".
  - Round the costs to cents (optional).

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-3 broken in the text (exposure called known at pricing), fixed by rewording; LEAK-10 triggered,
  kept under LEAK-11 (traced part lowers the Gini) pending the curator's case-by-case call; USE-5/USE-8 gaps
  misnamed in fit_reason; SPLIT-8 holds as a rule, its note is inaccurate and the curator's consistency call
  (how_much_did_it_rain) is open; LEAK-18 note refuted, no effect; PROV-16 book claims unverified.
Value: MET-1/MET-11 support misattributed, metric kept with a corrected reason; the rmse fallback has no signal.
Quality: CLEAN-16/MET-3 scale departs from the siblings with no reason; naming of driver_gender and area.
For the curator: the exposure keep (LEAK-10); forced IID against how_much_did_it_rain; Gini and target scale
  for the insurance family.
```

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (2026-11-01): australian_vehicle_insurance_2004_2005**

**Where we stand.** The critic and I reach the same verdict: ship after changes, with no change to the rows, the split
or the metric's formula, and no exclusion. I concede five points in full and two in part. Three narrow disputes
remain: whether the fremtpl2 precedent applies, whether a distinguishing fact for the forced split exists, and whether
the claims about the book are load-bearing.

**Critic 1, `exposure` called known at pricing: conceded, with one dispute.**
- Conceded:
  - the three descriptions (the prediction-point bullet, `known`, the Assessment) are wrong;
  - the leak note misses the frequency channel;
  - LEAK-11 is the rule that keeps the column;
  - the curator confirms the keep case by case (LEAK-10).
  The remedy is the critic's, which is also mine (opening point 2).
- One fix to the critic's wording: "a policy ends early after a total loss" is too narrow. Without the claims at 80%
  of the vehicle's value or more, the shortest policies still claim 0.85 times per policy-year (column auditor). Write
  "after some claims, total losses most clearly".
- Disputed: "the fremtpl2 reason does not carry over."
  - Andrej's fremtpl2 CC gives two reasons. One is "the contracted period is known at pricing (a mid-year cancellation
    also shortens it)". The other is "dividing would inflate short policies' targets".
  - The second reason carries over in full. The domain practitioner measured it here: a claim on a short slice is worth
    up to $5.2M a year.
  - The first reason was given on a column of the same kind. freMTPL2's `Exposure` is also a record's share of a year:
    94% of its repeat groups sum to 1 year or less ("one policy-year split into records"), and its indices 5-6 hold
    "almost no full-year exposures" (fremtpl2 record).
  - So the facts are alike, and the precedent weighs for the keep. It does not replace the curator's call on this case.
- heart_failure `time` is not a like case:
  - There, the whole column is follow-up that ends at the outcome. Dropping it costs AUC 0.90 to 0.75 (LEAK checks,
    probe 1).
  - Here most of the variation comes from the observation window, which is fixed when the policy starts, and the traced
    late part lowers the score: the counterfactual raises the Gini from 0.182 to 0.31.
  - The critic agrees this is the fact that sets the case apart.

**Critic 2, the gaps in `fit_reason`: conceded.**
- USE-8 asks to name `exposure` as kept, not as a gap (kick, homesite). I raised that myself.
- Adding the target per observed slice and the undocumented construction of the label as gaps is right. Those are:
  paid or incurred, the floor at 200, the 12 repeated amounts, and the cover (third party or comprehensive). USE-8
  lists "a label definition the sources do not settle" as an approximate gap, and USE-5 lets such a label ship with a
  note.
- The fit stays approximate. Nothing in this point changes the data.

**Critic 3, the forced IID split: the note conceded, the default disputed.**
- Conceded:
  - The note is wrong about a split by year: the data looks like one observation period.
  - The critic's new fact holds. The split auditor measured the shuffled pipeline frame, so "the file order is
    shuffled" must not go into the notes.
  - I withdraw my opening wording ("the cost cannot be measured") in favour of the critic's rewrite. The raw order is
    not random, but it shows no trend in the claim rate. A forward holdout over file quarters shows no drop (0.168,
    0.189 and 0.208, against 0.127, 0.174 and 0.181), and nobody knows whether that order is time.
  - The curator rules, as consistency check case 2 requires.
- Disputed: "without a fact, case 2 says treat it like how_much_did_it_rain."
  - The fact exists, is measured, and the critic's own rewrite lists it:
    - the rows are independent policies (hidden-group probe: 0 hits);
    - a split grouped on the exact feature vector scores within noise (0.194 and 0.208, against 0.182 and 0.205);
    - there are no renewal pairs (116 at 365 days, against a mean of 102);
    - the forward holdout shows no drop;
    - a later year shifts mostly the level, which the Gini ignores.
  - how_much_did_it_rain's `No` gave a reason specific to that task: "forced IID would introduce leaks for this task".
    No such channel is measured here.
- Rule: SPLIT-8 is an unamended Must, and rules win over precedents (principles, conflicts). Applying "at all costs"
  literally would be an amendment that reaches 17 datasets and frempl. The way to decide it is option (a) or (d) of
  the precedent checker's prompt 1, not a silent default.

**Critic 4, the duplicates: conceded in full.** Replace "natural" with the chance baseline: 378 copies against 120-125,
and 152 against 11.6 among the full-year rows. Add the measured lack of effect: +0.0045 Gini, and the grouped split
within noise. Keep the rows; dropping them under LEAK-19 is optional. This matches my opening point 6.

**Critic 5, the claims about the book: conceded; "load-bearing" disputed in part.**
- Conceded under PROV-16 and PROV-17, both Must:
  - mark the statements about Sec. 8.3 and 10.4-10.5, and "scores no held-out prediction", as unverified, or ask the
    curator for the book (Sec. 7.3-7.4, 8.3, 10.4-10.5, p. 15);
  - fix the band wording to "5,742 to 16,189".
  - If the book does name one held-out metric, MET-5 reopens the origin, as the claim auditor says.
- Disputed: the claims are not the only basis for the raw scale. My opening point 7 rests the scale on actuarial
  practice: CAS Monograph 5, Sec. 2.7.3 models "dollars of loss ... using the Tweedie distribution". The critic's own
  point 7 agrees ("Tweedie log-link practice favours raw dollars"). Nor are they the only basis for a context origin.
  Ye et al. (2022) report five metrics, so MET-5 gives no source metric from that paper either way.

**Critic 6, the support for the metric: conceded in full.** The remedy is the same as mine:
- cite Ye et al. (2022);
- describe Frees and CAS Monograph 5 as the weighted form per rate;
- state the exposure-alone baseline of 0.168;
- change "the insurers' ranking metric" in `changes` to a plain description;
- the curator confirms the Gini and strikes the `rmse` fallback from the record.
We agree the weighted form per year is a family question that Data Foundry cannot serve yet, since it has no training
weight and that form would reward the leak (0.238).

**Critic 7, the target scale and the names: conceded; the scale stays a weighing call.**
- The renames are cheap and safe P7 fixes: `gender`, or a note that the sources differ; "an area code A-F"; costs
  rounded to cents.
- On the scale, both sides agree it is one family call with a recorded reason. My side: raw dollars, as practitioners
  model this cost (Tweedie, log link). The other side: log1p lifts squared-error learners by +0.028 to +0.034 and
  aligns the family.
- MET-3 allows either scale and CLEAN-16 is a Should, so the dataset ships either way.

**What remains for the curator (unchanged by this round):**
1. confirm the `exposure` keep under LEAK-10 and LEAK-11;
2. rule on forced IID against how_much_did_it_rain, option (a) recorded or an amendment of SPLIT-8;
3. one family call on the Gini and on the target scale.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (critic, 2026-11-01): australian_vehicle_insurance_2004_2005**

**Where we stand.** We agree on the verdict, ship after changes, with no change to the rows, the split or the metric's
formula. I concede points 4 and 7 outright and most of points 1, 2, 3 and 6. I dispute five specifics. Each one
changes what the notes may claim, or which call is still open for the curator.

**Point 1, a real task on verified data: conceded, with two disputes.**
- Conceded: USE-1 holds, PROV-4 holds (Table 1.1, CASdatasets row by row, Rdatasets), and LEAK-24 cannot be verified
  but does not block.
- Disputed, "PROV-16 holds". The notes and the metric reason say what the book does with this table (Sec. 8.3,
  10.4-10.5, "scores no held-out prediction"), but only the contents were read. Those section titles name no data set
  (claim auditor #11). The advocate lists this as a slip in point 6, but PROV-16 is a Must at P5. The claim carries
  weight: it is the MET-1 basis for a context origin. Remedy: mark it unverified (PROV-17) or get the book.
- Disputed, "the curator's CC outranks any AI assessment". The `Yes` of 2026-10-30 was given on a record that read
  "Regime IID" and "the contracted period is known when the policy is priced". Both readings have since been measured
  wrong or changed ("Stages": a later measured finding supersedes). So the CC settles scope and priority. It does not
  settle the forced-IID framing or the exposure keep under the corrected description. Both stay open for the curator.

**Point 2, `exposure` stays: the keep and the remedy conceded, the precedent and the clause disputed.**
- Conceded: keep the column, rewrite the note (window share, shortening in claim occurrence, the offset and floor
  test, the counterfactual), fix `known`, and name exposure as kept in `fit_reason` (USE-8).
- Disputed, "fremtpl2 is a precedent with the same facts". The fremtpl2 call rests on "the contracted period is known
  at pricing". Here the contracted period is 1 on every row (Rd). The outcome-shortening is also measured here and
  was not there: 147 excess claims at 0.2 years or less, and a free log-exposure coefficient of 0.29-0.31 against 1.
  The closest mechanism is heart_failure `time` ("follow-up ends at death"), which the LEAK-10 Mechanisms table
  drops. The keep stands on LEAK-11 (Should, narrows LEAK-10): the traced part lowers the Gini (0.182 to 0.31 with
  counterfactual exposure, 18 of 18 runs). LEAK-10's second clause covers "a value read at a later pull", and exposure
  is not one. Remedy: the note cites LEAK-11 and says what sets this case apart from heart_failure. It does not call
  fremtpl2 a precedent with the same facts.

**Point 3, the Gini: conceded, with one dispute and one addition.**
- Conceded: the Gini stays and RMSE fails MET-1. Cite Ye et al. (2022), describe Frees et al. correctly, and add the
  exposure-alone baseline of 0.168. I also concede the reasons against the exposure-weighted rate form.
- Disputed, "Allstate's challenge used the same metric" as support. Every Allstate row is a full vehicle-year, while
  98.1% of the rows here are not (claim auditor #26). Citing it without that difference repeats the fault MET-11 asks
  the notes to avoid. Remedy: cite Allstate with the difference stated.
- Addition, which follows from our agreement: the record's Assessment still offers "Fallback `rmse` if the curator
  prefers the default". Both briefs say rmse scores shrinkage (best R^2 0.002), so the curator should strike that
  option when confirming the Gini.

**Point 4, a small real signal, not trivial: conceded.** I never argued `Trivial` (TP-4). One caveat on the
evidence: the dummy's Gini moves between -0.061 and +0.037 because ties are broken in row order (claim auditor,
claim 23). "Beats the dummy 9 of 9" is therefore weaker than the GLM beating exposure alone (+0.038, SE 0.010, 8 of 9),
which is the evidence TP-4 asks for.

**Point 5, forced IID: the remedy conceded, two supports disputed.**
- Conceded: SPLIT-8 is an unamended Must that allows `ForcedIIDFromTemporal`. The mildest remedy is to record the
  fact that sets this case apart (precedent checker, option a) and put the consistency check to the curator. Making
  forced IID a reject would be an amendment.
- Disputed, the split auditor's note edit "the cost cannot be measured", which rests on "the file order is shuffled".
  The split auditor measured the pipeline's shuffled frame (its script reads the `dataset_io` frame). On the raw
  `dataCar.csv`, the lag-1 autocorrelation of exposure is 0.094 (0.002 shuffled), and 12.2% of adjacent rows share a
  day count (0.3% shuffled). The column auditor, the claim auditor and the precedent checker found the same. A forward
  holdout over file quarters was run and shows no drop (precedent checker). Remedy: the note says the raw order is
  not random and its meaning is unknown, and it gives the forward-holdout result. It must not say the order is
  shuffled.
- Disputed, "Andrej's `Yes` was given on a record that read Regime IID" as support. It cuts the other way: the
  curator never ruled on the forced-from-temporal framing (see point 1). The distinguishing fact has to be written
  and put to him, not inferred from the `Yes`.

**Point 6, the cleaning: conceded,** apart from filing the unread book sections as a slip (see point 1, PROV-16).
The LEAK-19 drop stays optional.

**Point 7, the raw-dollar target: conceded.** It is P7, the scale is defensible (MET-3 allows either), and it is no
blocker. One refinement: the reason to record is the advocate's CAS Monograph 5, Sec. 2.7.3 (Tweedie on dollars),
not the precedent checker's option (a). Option (a) rests on the book's unread sections (PROV-16). If raw is the
actuarial scale here, the same fact applies to frempl and spanish, so the curator decides it once for the family
(consistent judgement, case 2).

**Judgment record after rebuttal**

```text
Verdict: ship after changes (text only).
Validity: USE-3 text fixed; LEAK-10 triggered, kept under LEAK-11 (not on fremtpl2 as same facts), curator confirms;
  USE-8 fit_reason fixed; SPLIT-8 holds, note rewritten without "shuffled", consistency call open; PROV-16 book
  claims marked unverified.
Value: MET-1/MET-11 reason rewritten (Ye et al. 2022; Allstate with its full-year difference); rmse fallback struck
  from the record.
Quality: raw scale kept with the CAS Monograph reason, one family call; notes on duplicates and names.
For the curator: the exposure keep; forced IID against how_much_did_it_rain; Gini and scale for the family.
```

</details>
