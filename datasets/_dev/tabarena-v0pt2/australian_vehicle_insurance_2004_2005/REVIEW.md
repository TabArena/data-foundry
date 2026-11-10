# australian_vehicle_insurance_2004_2005

**Outcome:** added. The AI recommends shipping it: the re-review panel of 2026-11-06 under the exposure rules found no
validity rule broken in the rows, features, target or split, its text changes are made (below), and its three
questions were settled on 2026-11-08: the cost per year insured stays with MET-14's per-contract clause amended (issue
8), the age bands are ordered categories (issue 9), and `gender` left the features (issue 7), back since 2026-11-09
under the rule that today's law of the data's country decides on sex in insurance pricing (issue 10). Like every container
with a `sample_weight`, it enters no
run before the collection's training-weight gate (`BENCHMARK_CHANGES_TODO.md`, "Training weights", "The gate"). The
"Car" table of de Jong and Heller (2008) from the R package insuranceData (CASdatasets holds the same rows): 67,856
one-year Australian vehicle policies of 2004-2005, target the claim cost per year insured (the cost of the part of the
policy's year the data observed, over that time, in dollars; 0 for 93.2%), six rating factors, the observed time as
each policy's weight in training and scoring, random 3x3 split tagged forced from temporal, scored by the
exposure-weighted normalized Gini as a context metric. Validity: USE-1 holds (pricing a policy at underwriting, "for
example"); LEAK-41 holds: `exposure`, which some claims cut short, is only the weight scoring column, the metric's
weight input and the `sample_weight` (issue 6, Lennart, 2026-11-06); the rating factors predict it only weakly (R^2
0.074, and about 0.08 on the policies without a claim, whose exposure no claim cut), so what they predict is when the
policy started, which is known at the quote (USE-6); probe 22 finds in both arms (an L2 and a weighted Tweedie fit)
that the exposure as a feature gains +0.112 and +0.085 and that no rating factor gains through it above noise
(re-run on 2026-11-09 with `gender`); LEAK-10 holds (`clm`, `numclaims` and `claimcst0`
dropped as parts of the target); SPLIT-8 holds: the forced IID split ships on Andrej's call of 2026-11-02 (issue 1),
and on the rate it shows no drop when later file blocks or whole rating cells are held out; PROV-4 and PROV-16 hold
(the book's Table 1.1, CASdatasets row by row, the book's pages read, issue 3); USE-6 and the Tensions row on rating
factors as amended on 2026-11-09: sex leaves an insurance pricing task only where today's law of the data's country
bars it, and s41 of the Sex Discrimination Act 1984 allows it in Australia, so `gender` stays (issue 10); USE-5 and MET-14 hold: the per-contract clause,
amended on 2026-11-08, needs the data to record each contract to its end, and the extract's window cuts 98.1% of
these policies (issue 8). Value: TP-2, a small real signal: the three families fitted with the weight beat the
weighted constant on 9 of 9 splits (Tweedie GLM 0.133, Tweedie LightGBM 0.062, L2 LightGBM 0.074); the task probe
flags `no_signal`, but the flag reads an R^2-type skill (weighted squared error, best R^2 0.000), while on the
declared metric the probe's linear family scores 0.122 and beats the dummy on all 5 splits it ran (EV-3); re-check
with the first tuned run (TP-1), as for sf_permit_time, heart_disease and
open_university_learning_analytics_dataset; TP-4: the observed time, which alone earned 82% of the
old score, is no input now; MET-11 and MET-13 hold: the exposure-weighted Gini of the cost per year as a context
metric (issues 4 and 6), its scorer equal to a brute-force Lorenz area, its reason now saying that it sees neither the
price level nor the spread of the relativities; MET-15 holds at the definition (the run waits on the gate above).
Quality: the 53 vehicle values of 0 made missing (CLEAN-10, CLEAN-11); the claim costs at 200 kept as recorded, as the
call on fremtpl2's fixed amounts (2026-10-20); dollars kept on Andrej's call of 2026-11-02 (issue 5; CLEAN-16 as
amended 2026-11-06: a rate scored by a Gini keeps the curator's scale); the 7 costs per year of 1M dollars or more
kept, since no row may be selected by the realized weight (LEAK-41); CLEAN-14: the age bands ship as ordered categories
(issue 9, 2026-11-08). Weighed: a documented textbook table +, the standard actuarial formulation (a rate with its
weight) +, six coarse rating factors -, a thin signal (best honest score 0.122 to 0.133) -. For Andrej: Lennart's
decision D8 of 2026-11-06 (issue 6) supersedes his call on issue 2 (`exposure` kept as a feature) and changes the form
of his Gini of issue 4 (unweighted on the cost, now weighted on the rate), and Lennart's stance of 2026-11-08 (issue
7) dropped the `gender` his ship of 2026-11-02 kept, which his rule of 2026-11-09 brings back (issue 10); the newer
curator decision wins. Nothing is left open.

Changes made after the review panel (AI, 2026-11-01), text only (rows, split and metric unchanged): `exposure` is
described as the share of the year observed, cut short after some claims, and named in `fit_reason` as a kept leak;
the split note gives the one observation period and the file-order check; the metric reason cites Ye et al. (2022) and
describes Frees et al. and Allstate as they are; the book's later sections are marked unverified; the duplicates and
200-floor notes give their baselines and precedent; `driver_gender` is renamed `gender`. Changed on 2026-11-06 (issue
6): the target is the cost per year insured, `exposure` the weight and no feature, the metric the weighted Gini on the
rate; `fit_reason` no longer names a kept leak. Changed after the re-review panel (AI, 2026-11-06), text only (rows,
features, target, weight, split and metric unchanged): the metric reason adds that the Gini also ignores the spread of
the relativities (a Tweedie GLM with doubled log-relativities keeps its Gini but loses to the weighted constant on the
weighted Tweedie deviance on 9 of 9 splits) and why that deviance was not chosen (the best honest model gains 0.5% of
it); the split and copies notes give the file-order and grouped splits re-measured on the rate, as issue 1 now does,
the cut at the extract window's edges and the drift of the exposure along the file; the exposure note gives both arms
of probe 22; "spread evenly" and four minor numbers are corrected; the record marks its old statements on `exposure`
and the target superseded.

Changed on Lennart's marks of 2026-11-08 (target, weight, metric and split design unchanged; a build waits for your
ask): `gender` is dropped (issue 7), so five rating factors remain; the notes' target bullet says why MET-14's
per-contract clause, amended the same day, does not apply, and the metric reason why the claim frequency's deviance
was not chosen (issue 8). Dropping a column changes the rows' content order and so the shipped splits; every model
number of the notes, the metric reason and this page was re-measured on the new splits (the probes, the honest and
exposure-fed fits, the grouped, file-order and copy checks).

Changed on Andrej's decision of 2026-11-09 (target, weight, metric and split design unchanged; no container built):
`gender` is back among the rating factors (issue 10), as sex in insurance pricing now follows today's law of the
data's country, and Australian law allows it. Adding the column changes the rows' content order and so the shipped
splits; the model numbers of the notes, the metric reason and this page are re-measured on the new splits (the probes,
the honest and exposure-fed fits, the grouped, file-order and copy checks), except the claim-frequency comparison of
the metric reason, which keeps its date.

**Main points:** nothing open. On 2026-11-09: `gender` ships again, as Australian law allows sex in insurance pricing
today (10, reopening 7, where it was dropped on 2026-11-08 under the family stance). On 2026-11-08: the cost per year
insured kept, with MET-14's per-contract clause amended together with spanish_motor_insurance_2015_2018's issue 7 (8);
the age bands as ordered categories (9). Issues 1 to 6 are resolved (6 supersedes 2 and changes the form of 4).

**Issues for Andrej and Lennart:**

1. **Ship this forced random split, or treat it like how_much_did_it_rain?** An insurer fits its tariff on past
   policies and prices next year's, so the task is temporal by its use case. The release has no dates and no policy
   ids, so the test folds are random policies of the same period. SPLIT-8 (Must) ships such a task as IID with the tag
   "forced from temporal" (`ForcedIIDFromTemporal`). On 2026-10-30 you sent how_much_did_it_rain to `No` ("if the data
   is temporal but a temporal split is not possible, we cannot split the data and reject it") and said "Forced IID is
   to be avoided at all costs"; SPLIT-8 itself was left unchanged. Your `Yes` here was given on a record that read
   "Regime IID"; the split was tagged as forced when the dataset was added.
   * What it does to the task: models are tested on policies of the same observation period, not on a later year. A
     later year's change in the claim level would not move the Gini, which ignores the level; a change in the mix of
     policies or in what drives claims is not tested. The cost cannot be measured: the data covers one period of
     about a year.
   * What may set it apart (measured): each row is a distinct policy; the hidden-group probe finds nothing; no policy
     is split into two rows (116 pairs of identical rating factors sum to 365 days, against 102 on average for other
     sums); a split that keeps identical rating factors together, or identical full rows with the exposure, scores as
     the random one (weighted Gini of the cost per year: LightGBM 0.054 and 0.077, GLM 0.119 and 0.127, against 0.059
     and 0.120 on the shipped splits); the claims show no dependence along the file's order, and training on earlier
     quarters of the file to test on the next shows no drop (LightGBM 0.078 and GLM 0.128 against 0.060 and 0.111 for
     random splits of the same sizes; means of three splits, and whether the file order is time is unknown).
     how_much_did_it_rain's `No` named a leak: hours of the same storm on both sides of a random split. No such
     channel is found here.
   * The advocate reads these facts as setting the case apart; the critic accepts the facts but says only you can say
     whether they meet "at all costs". The precedent check flags the same.
   * Implemented: (a) IID tagged `ForcedIIDFromTemporal`, with the facts above in the notes. Alternatives: (b) `No`,
     like how_much_did_it_rain (frempl_french_motor_personal_line, same run and same tag, would follow); (c) reopen
     how_much_did_it_rain under SPLIT-8 as written; (d) amend SPLIT-8 ("forced IID only where rows share no unit or
     period outcome", or "forced IID is a reject"), which reaches the 17 forced-IID datasets of the working copy.

   Recommendation: (a). Decision: (a), (b), (c) or (d)?

   *Restored on 2026-11-03 from the panel's draft: the issue was removed when settled, before the rule that settled issues stay (2026-11-02).*

   *Numbers re-measured on 2026-11-06 on the cost per year insured, every fit weighted (issue 6); on the cost target of 2026-11-01 they were 0.194 and 0.208 against 0.182 and 0.205 (identical feature rows together, with the exposure a feature) and 0.168, 0.189, 0.208 against 0.127, 0.174, 0.181 (file order, single splits). The conclusion is unchanged.*

   **Resolved (2026-11-02, Andrej):** the forced IID split ships (issue 1 (a)): "Forced group splits should be fine.
   Regarding forced IID, did you make sure there are no leaks? Whenever there are no leaks we can ship." Recorded in
   SPLIT-8 (amended 2026-11-02: a forced grouped split ships; a forced IID split ships only when the leak test across
   the random split finds none).

2. **Keep the time in force (`exposure`) as a feature, now that some claims are known to cut it short?** Every policy
   is a one-year contract. `exposure` is the share of that year the data observed (1 to 365 days, median 163; 1.9%
   are full years), and a policy ends early after some claims, most clearly when the car is written off. The AI's
   suggestion of 2026-10-30 in the record called it "the contracted period, known when the policy is priced"; that
   reading was wrong and is corrected.
   * What it does to the task: at a real quote the time is one year for every policy, so it ranks nothing. In the
     benchmark each test policy comes with its observed time, which alone earns 0.168 of the best Gini, 0.205. The
     part cut short after a claim does not help a model; it lowers the score.
   * Evidence (9 shipped splits): short policies claim more per year (147 more claims than expected at 0.2 years or
     less; the 193 claims of at least 80% of the car's value have a median time of 0.37 years against 0.65). A model
     given the time only as a proportional effect, which cannot use that excess, scores 0.1833 against 0.1824 with
     the time as a free feature (paired SE 0.0059). Giving the written-off policies their uncut time raises the Gini
     from 0.182 to 0.31 (18 of 18 runs).
   * Rule: LEAK-10 (Must) is triggered; LEAK-11 (Should, narrows LEAK-10) keeps a late value that weakens the signal,
     with a note. That sets it apart from heart_failure, whose follow-up `time` (ending at death) was dropped because
     it carried the signal (ROC AUC 0.90 to 0.75 without it). Your fremtpl2 call (2026-10-20) kept `Exposure` as a
     feature, not a divisor, for the same pricing practice; its reason, a contracted period known at pricing, does
     not carry here. The advocate and the critic both keep it.
   * Implemented: kept, with the note rewritten. Alternatives: drop it (best Gini 0.205 to 0.130; it removes the time
     on risk, the core of a claim cost); or predict the cost per policy-year with the time only as the metric's
     weight, as actuaries do, which Data Foundry cannot train for yet (without a training weight one claim on a
     one-day policy counts as up to $5.2M a year) and which belongs with issue 4.

   Recommendation: keep. Decision: keep or drop?

   *Restored on 2026-11-03 from the panel's draft: the issue was removed when settled, before the rule that settled issues stay (2026-11-02).*

   **Resolved (2026-11-02, Andrej):** `exposure` kept as a feature with its note (issue 2); recorded as the LEAK-10
   case for time on risk cut short by the outcome (leak_checks.md, Mechanisms table): the cut is removed or fixed
   where the data locates it, kept with its measured size where it cannot. Here the cut cannot be located (no dates),
   and the traced part lowers the Gini (offset-only 0.1833 against 0.1824 free; uncut write-offs 0.31).

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

5. **Ship the claim cost in dollars or as log1p, decided once for the three insurance tables?** This table ships the
   raw cost; frempl and spanish, from the same run and with the same Gini on dollars, ship log(1 + cost)
   (`target_transform="log1p"`), and no reason for the difference is recorded. The Gini is computed on dollars either
   way; only what a model is trained on changes.
   * Effect (9 splits): log1p lifts squared-error boosting by +0.028 to +0.034 (two probes, better on 7 to 9 of 9),
     from below the time-alone baseline (0.163 against 0.168) to above it. The best model, a Tweedie GLM, is fit on
     dollars (0.205).
   * For dollars: insurers model the cost in dollars with a Tweedie model and a log link (CAS Monograph 5, Sec.
     2.7.3), a scale MET-3 (Must) allows. For log1p: CLEAN-16 (Should) logs a skewed positive target by default, case
     by case, and the family stays aligned. The advocate prefers dollars, the column audit log1p; the critic asks for
     one call for the three.
   * Implemented: dollars. Alternatives: log1p here (one line; the target renamed `log1p_claim_cost`); or frempl and
     spanish reopened to dollars, with the Tweedie practice recorded as the reason.

   Recommendation: one scale for the three; log1p follows the rule's default and the siblings, dollars needs the
   reason recorded. Decision: dollars or log1p?

   *Restored on 2026-11-03 from the panel's draft: the issue was removed when settled, before the rule that settled issues stay (2026-11-02).*

   **Resolved (2026-11-02, Andrej):** the target scale as each file implements it (issue 5): this table ships the
   claim cost in dollars, the log1p tables keep log1p.

6. **Ship the claim cost per year insured, with `exposure` as the weight and no longer a feature?**

   * **Problem:**
     - `exposure` is the realized share of each one-year policy inside the extract (median 163 days, 1.9% full years),
       and some claims cut it short: the 193 likely write-offs have a median exposure of 0.37 against 0.65 for the
       other claims.
     - Your call of 2026-11-02 kept it as a feature[^call], because on the unweighted Gini of each policy's cost the
       part cut short showed no gain (as an offset only 0.1833, as a free feature 0.1824).
     - The exposure study of 2026-11-05 measured it on scores that can see the cut, and the rules adopted on 2026-11-06
       never let a realized weight be a model input[^weight].
   * **Background:** Issue 2 named the actuaries' design (the cost per policy-year, the time only as the metric's
     weight) and set it aside because Data Foundry had no training weight. The API now has one (`sample_weight`):
     every model trains with the weight it is scored by, so one claim on a one-day policy counts by its cost, not as
     5.2 million dollars a year.
   * **Effect on the task:**
     - The target is `claim_cost_per_year` = `claimcst0` / `exposure`, in dollars on the identity scale (issue 5's
       scale); `exposure` leaves the features and becomes the weight scoring column, the metric's `weight` input and
       the task's `sample_weight`; the metric is `normalized_weighted_gini` on the rate, still a context Gini.
     - A weighted fit estimates the cost per year that breaks even (292.90 dollars a year for the portfolio); a learner
       that ignores the weight estimates the mean of cost / exposure (755.26, 2.6 times as much).
     - Every exposure is at least one day, so no row goes. The 7 policies at 1M dollars or more a year (one claim each
       on 1 to 7 days observed, up to 5.24 million, 1.26% of the cost) are kept and listed in the notes; actuaRE's copy
       removes them. They hold 45% of the exposure-weighted sum of squares of the rate, while the Gini counts each by
       its cost.
   * **Experiments:**
     - Exposure study (own 3x3 KFold): on the claim counts, 47% (GLM) to 82% (LightGBM) of a free model's gain over a
       constant rate is leak; at a quote (exposure one year) the free LightGBM is 0.0068 worse in mean deviance than
       the offset model, better on 0 of 9 folds.
     - Same study, on the weighted Gini of the cost per year: a Tweedie GLM that reads the exposure scores 0.238
       against 0.125 for an honest GLM; the rating factors predict the exposure at R^2 0.06 (ROC AUC 0.62 for
       exposures of 0.2 years or less).
     - On the 9 shipped splits of the new definition, every fit with the sample weight: an honest Tweedie LightGBM
       scores 0.059 (SD 0.021), an L2 LightGBM on the identity scale 0.060 and a Tweedie GLM 0.120, against 0 for the
       weighted constant (above it on 9 of 9); with `exposure` added as a feature 0.149 (+0.089, SE 0.010), 0.159
       (+0.099, SE 0.008) and 0.236 (+0.116, SE 0.006), higher on 9 of 9 each. More regularised LightGBM settings:
       0.070 to 0.090 honest, +0.094 to +0.124 with the exposure.
     - 1/exposure alone scores 0.205, above every honest model. The weight-proxy probe: the rating factors predict the
       exposure at R^2 0.07 (Spearman 0.26, mostly through the vehicle value), and no rating factor gains through it
       above noise. Both arms of the probe (added after the decision, 2026-11-06): the exposure as a feature gains
       +0.098 over an honest L2 fit of 0.052 and +0.068 over an honest weighted Tweedie fit of 0.068, and in neither
       arm does a rating factor gain through it above noise.
   * **Consistency:** Follows fremtpl2 and bemtpl97 (2026-11-06: the claims per year insured, the exposure as the
     weight and never a feature)[^cases]. It departs from your call of 2026-11-02 on this table; what sets the case
     apart is a measurement made after it: the deviance on the claim counts shows the leak the slice Gini hid.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Cost per year, weighted Gini (implemented) | `exposure` the weight; Gini on the rate | the actuary's Gini; no exposure leak | fold SD 0.02-0.03 |
     | B | Claim frequency, weighted deviance | `numclaims` / `exposure` | as fremtpl2, bemtpl97; fold SD 0.01 | drops the claim size |
     | C | Keep `exposure` a feature | the call of 2026-11-02 | no training weight | 47-82% of the count gain is leak |

   * **Recommendation:** A (the exposure study's decision D8). **Decision:** A, B or C?

   [^call]: Andrej, 2026-11-02 (issue 2): `exposure` kept as a feature with its note, recorded as the **LEAK-10** case
     for time on risk cut short by the outcome; his Gini of the same day (issue 4) was the unweighted one.
   [^weight]: **LEAK-41** (Must, 2026-11-06): a column the task uses as a weight or a rate's denominator whose value is
     set or cut after the prediction point is never a model input, whatever it scores; **MET-14** (Should) and
     **MET-15** (Must): the rate per unit, its realized denominator the metric's row weight and the `sample_weight`;
     **CLEAN-16** (Should, amended 2026-11-06): a rate scored by a Gini keeps the scale the curator chose.
   [^cases]: fremtpl2 issue 6 and bemtpl97 issue 1, resolved 2026-11-06 (Lennart); the exposure study of 2026-11-05,
     decision D8.

   **Resolved (2026-11-06, Lennart):** A, decision D8 of the exposure study of 2026-11-05. The target is
   `claim_cost_per_year` = `claimcst0` / `exposure` in dollars (identity scale); `exposure` is the weight scoring
   column, the `weight` input of `normalized_weighted_gini` and the task's `sample_weight`, and never a feature
   (LEAK-41, MET-14, MET-15); the metric stays a context Gini, the CAS Gini of the cost per year, normalised; the claim
   frequency with a weighted deviance was not chosen. No exposure is 0 (the shortest is one day), so no row goes; the
   7 rows at 1M dollars or more a year are kept and named in the notes. Supersedes Andrej's call of 2026-11-02 (issue
   2) and changes the form of the Gini of issue 4: the deviance on the counts shows the leak the slice Gini hid. On the
   shipped splits an honest Tweedie LightGBM scores 0.059 and a Tweedie GLM 0.120 against 0 for the weighted constant;
   `exposure` as a feature adds +0.089 and +0.116 (9 of 9); 1/exposure alone scores 0.205. `dataset check`: 0 errors,
   0 warnings (the warning `task_feature_looks_like_exposure` is gone).

7. **What sets `gender` here apart from bemtpl97's `sex`, which was dropped?**

   * **Problem:**
     - On 2026-11-05 bemtpl97 dropped `sex`, because its actor, an EU insurer pricing today, may no longer rate on sex
       since the Test-Achats ruling[^i7-tension].
     - This definition keeps `gender` for "an Australian car insurer" pricing a policy at underwriting and gives no
       reason why that insurer may use it.
     - The likely fact is the jurisdiction, since the panel reads s41 of the Sex Discrimination Act 1984 (Cth) as
       allowing sex-based terms of insurance that rest on actuarial or statistical data it is reasonable to rely on,
       but nobody checked the statute's text in this run.
   * **Effect on the task:** None on the data if an Australian insurer may price on sex; if it may not, one of the six
     rating factors is an input the actor cannot use, and it leaves the features.
   * **Unknown:** Whether s41 says this: the advocate, the critic, the precedent checker and the mediator all cite it
     unverified (the mediator: "That is my reading of the statute too, but I did not check the text in this run"). The
     statute's text settles it.
   * **Consistency:** bemtpl97 (Lennart, 2026-11-05) dropped `sex`; home_credit_default_risk (`CODE_GENDER`) and
     credit_card_clients_default (`SEX`) keep theirs and are not reviewed yet[^i7-tension]. When a precedent with
     similar facts went the other way, the curator is asked what sets the case apart[^i7-check].
   * **Panel:** The advocate's best evidence is the jurisdiction (s41, unverified); the critic's is that the question
     stands whatever decision D8 changed, so it should be settled before the dataset enters a run. Both want the fact
     that sets this case apart written into the notes (B or C).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `gender`, no reason written (implemented) | nothing changes | none found | like cases read unlike; the fact that sets this case apart stays unwritten |
     | B | Keep `gender`, the law named | once s41 is read, the notes name the Australian insurer and the law; this table becomes a case of the rule | the input the actor has at the quote; like cases read alike | rests on a statute not read yet |
     | C | Drop `gender`, as bemtpl97 | five rating factors | the same outcome as bemtpl97 | against the use case if the law permits the factor |
     | D | Reopen bemtpl97 | `sex` back in bemtpl97 | none found | EU law bars the factor there |
     | E | Amend the rule: the actor's jurisdiction decides | the rule asks the definition to name the law; B follows | settles home_credit_default_risk and credit_card_clients_default too | a rule change before the statute is read |

   * **Recommendation:** B: the use case names an Australian insurer pricing today, so Australian law decides, as EU
     law decided for bemtpl97; if s41 turns out not to permit the factor, C. E can wait until home_credit_default_risk
     and credit_card_clients_default are reviewed. **Decision:** A, B, C, D or E?

   **Notes for the AI:** On B: read s41 of the Sex Discrimination Act 1984 (Cth) in its current compilation
   (legislation.gov.au). If it permits sex-based terms of insurance resting on actuarial or statistical data that it
   is reasonable to rely on, add to the notes' renames bullet that the actor is an Australian insurer and that s41
   permits the factor, so `gender` stays (USE-6; the Tensions row on rating factors); record the curator's call as a
   CC line; the main session adds this table to the Tensions row's cases in principles.md. If s41 does not permit it,
   put C to the curator. On C: drop `gender` in `_clean`, take it out of `_feature_types`, the `known` text and the
   notes, and re-run `dataset check` and the leak and task probes. On E: the main session amends the Tensions row in
   principles.md (date, curator, this case).

   **Lennart (2026-11-08, change):** Option C: Drop gender, as bemtpl97.

   **Consistency check (AI, 2026-11-08):** Drop `gender` "as bemtpl97", when bemtpl97's ground was the law that binds
   its actor today and the actor here is an Australian insurer?

   * **Problem:**
     - The rules drop a rating factor the actor knows at the quote only when the actor may no longer use it; bemtpl97's
       `sex` went because EU law bars it (Test-Achats)[^a7a].
     - Section 41 of the Sex Discrimination Act 1984 (Cth) exempts insurance terms that rest on actuarial or statistical
       data it is reasonable to rely on (the panel's reading; the AI could not fetch the statute's text today), so an
       Australian insurer may use the factor.
     - Without a fact of its own, dropping it here departs from the rule on inputs known at the prediction point.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | A stance for the family | the tensions row is amended: sex leaves the rating factors of every insurance pricing task, whatever the law; `gender` dropped here | like cases alike without reading statutes; your C stands | drops an input this actor may use; a rule change |
     | b | Follow the law of the actor | `gender` stays, the notes name s41 (the issue's option B) | the rule as written | differs from bemtpl97 by jurisdiction |
     | c | C as an exception | `gender` dropped with a fact of its own | your mark stands | no such fact found |

   * **Recommendation:** (a) if "as bemtpl97" was meant for the whole insurance family, otherwise (b).
   * **Decision:** (a), (b) or (c)?

   **Notes for the AI:** on (a), amend the tensions row in principles.md (2026-11-08, Lennart, this case) and drop
   `gender` as the issue's option C says; on (b), the issue's option B. Re-run the task probe either way.

   [^a7a]: principles.md, "Tensions" ("A rating factor known at the prediction point against a factor the actor may no
     longer use"; bemtpl97, 2026-11-05); **USE-6** (Must), **USE-1** (Must).


   [^i7-tension]: The Tensions row of principles.md on "a rating factor known at the prediction point against a factor
     the actor may no longer use" (P3 and P4; **USE-1**, **USE-6**): when the use case is today's pricing, the actor's
     legal constraint today decides and the factor leaves the features; a use case set in the data's own time keeps
     it. Cases: bemtpl97, `sex` dropped, the actor an EU insurer pricing today, barred by the Test-Achats ruling (CJEU
     C-236/09, 1 March 2011, in force for new contracts from 21 December 2012; Lennart, 2026-11-05);
     home_credit_default_risk (`CODE_GENDER`) and credit_card_clients_default (`SEX`) keep it, not reviewed yet.
   [^i7-check]: principles.md, "Consistent judgement, the curator's included", case 2: a precedent with similar facts
     was decided the other way; the ways out are the distinguishing fact recorded, the case treated like the
     precedent, the precedent reopened, or the rule amended.

   **Lennart (2026-11-08, change):** Reply (a): A stance for the family; as if we were to simulate the case in europe
   always

   **Resolved (2026-11-08, Lennart):** (a), the issue's C. `gender` leaves the features: sex is no rating factor of any
   insurance pricing task of this collection, whatever the actor's jurisdiction, as under EU law (Test-Achats); the
   Tensions row on rating factors in principles.md is amended so (2026-11-08, Lennart, this case). `known`, `changes`,
   `fit_reason` and the notes say so, and the record's CC line supersedes Andrej's ship of 2026-11-02, which kept
   `gender`. It carried little: the Tweedie GLM scores 0.124 with it and 0.119 without (+0.004, SE 0.002, higher with
   it on 7 of 9 splits), a regularised LightGBM 0.103 either way. Dropping a column changes the rows' content order and
   so the shipped splits; the notes' model numbers are re-measured on the new ones (task probe: linear 0.117 against the
   dummy's 0, 5 of 5 splits). `dataset check`: 0 errors, 0 warnings.

   **Resolved (2026-11-09, Andrej):** reopened and settled again in issue 10: `gender` ships again, under the rule of
   2026-11-09 that sex leaves an insurance pricing task only where today's law of the data's country bars it.

8. **Record the cost per year insured as an exception to the per-contract rule, or amend the rule?**

   * **Problem:**
     - The rule for rates keeps a target per contract when every contract has the same planned term, known at the
       prediction point[^i8-rule], and that holds here (one year at every quote), yet decision D8 ships the claim cost
       per year insured.
     - What sets the case apart is measured and agreed: 98.1% of these policies are observed for only part of their
       year (median 163 days, 1.9% full years), so the recorded cost belongs to the extract's window, not to the
       contract, while spanish_motor_insurance_2015_2018, which kept its target per contract on the same day, has 5.5%
       of its first years cut short.
     - A departure from a rule of this strength needs that fact recorded as an exception, or the rule amended so that
       it says what it meant[^i8-strength].
   * **Effect on the task:** None on the data: the rule and the decision disagree only on paper, so the next curator
     cannot tell which one to follow.
   * **Consistency:** spanish_motor_insurance_2015_2018 issue 7 asks about the same clause from the other side:
     whether its half-yearly payers who stop paying at six months (1,632 of its 2,055 cut first years; the insurer
     collects half the annual premium on them) make that table a rate case, and it recommends amending the clause too.
     The clause is settled once, for both tables. An exception here would be the first on the clause[^i8-cases].
   * **Panel:** The advocate reads the rate as holding under what the clause meant, the critic as a departure that
     needs its exception recorded; both agree on the remedy and differ only in the label.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The rate, nothing recorded (implemented) | nothing changes | none found | a departure without its fact; the next curator cannot tell which to follow |
     | B | The rate, recorded as an exception | an exception line with the 98.1% fact in the record and the notes, and a row in the rule's cases | the decision stands as made; one line | the first exception on this clause |
     | C | The rate, the rule amended | the clause reads "... known at the prediction point and observed in full for most rows" | the rule says what it meant; no exception needed | a rule change, read for spanish_motor_insurance_2015_2018 too |

   * **Recommendation:** C: the clause was written on spanish_motor_insurance_2015_2018, where 94.5% of the terms are
     observed in full, so it assumed a term observed in full; one amendment, written with
     spanish_motor_insurance_2015_2018 issue 7 (B), settles both tables. B if the clause was meant to hold even for
     terms mostly cut short. **Decision:** A, B or C?

   **Notes for the AI:** On B: append to the record, and add to the notes' target bullet, the line "Exception to
   MET-14 (date, curator): every policy has a one-year planned term known at the quote, but 98.1% are observed for
   only part of it (median 163 days, 1.9% full years), so the recorded cost belongs to the extract's window, not to
   the contract; the cost per year insured, weighted by the time observed, is what the insurer prices. Serves P3
   (USE-5)." with its label in bold, as principles.md shows it; the main session adds a row of kind `exception` to
   MET-14's Cases table in metrics.md. On C: the main session amends MET-14's clause in metrics.md (date, curator,
   this case), and the notes' target bullet cites the amended clause. Either way the same call answers
   spanish_motor_insurance_2015_2018 issue 7.

   **Lennart (2026-11-08, discuss):** Reinvestigate the prior decisions, from the original state of the data and its
   context with our current rules, what target would be best?

   **Answer (AI, 2026-11-08):** Keep the claim cost per year insured with the weighted Gini, and add one sentence to the
   per-contract clause so that the rate follows from the rule?

   * **Problem:**
     - You asked which target and metric are best when the earlier calls (Andrej's of 2026-11-02 and decision D8 of
       2026-11-06) are treated as hypotheses and tested against the raw data, the source and the current rules, and
       what that means for the per-contract clause of this issue.
     - The data hold each one-year contract only inside the extract's observation window (98.1% are part-years, 0.47
       of a year per contract on average), so the recorded cost, claim count and claim indicator belong to that window,
       and five targets were fitted on the 9 shipped splits without `exposure` and without `gender`.
     - Only the two targets per year insured give no credit for predicting the window, and of those the cost per year
       under the weighted Gini is the insurer's own quantity and tells the models apart best, so D8 stands and the
       clause needs one sentence on what a per-contract target requires.
   * **Background:**
     - The source: one-year policies taken out in 2004 or 2005 (de Jong and Heller 2008); `exposure` is "0-1" in
       insuranceData and "the number of policy years" in CASdatasets. The book treats it as the time at risk in its
       claim-occurrence model (Sec. 7.3-7.4), models the claim cost with its zeros (Sec. 10.4) and scores no held-out
       prediction[^a8a].
     - What `exposure` measures: among the policies without a claim it is spread almost evenly over the year (12.4% in
       the first tenth, 8.8% in the last), as a one-year window cuts one-year terms that start all through the year;
       1,289 rows (1.9%) run the full year, against about 184 rows for any other day count; some claims cut the rest
       short (the 193 likely write-offs have a median of 0.37 years against 0.65 for other claims).
     - What that does to the recorded outcomes: the chance that a row has a claim rises from 1.3% (7 days or less) to
       12.1% (0.9 years or more), while from 7 days on the claims per year insured fall from 0.23 to 0.14. The book's
       own numbers show it: ROC AUC 0.662 with the exposure in the link, 0.548 without.
   * **Experiments:** 9 shipped splits, five honest models (two GLMs, three LightGBMs), `gender` out, `exposure` only
     as the weight of the targets per year.
     - Predicting the window: a model of the exposure from the five rating factors, used as the score, reaches ROC AUC
       0.539 on the claim indicator (the GLM 0.548) and a Gini of 0.057 on the cost per contract (the GLM 0.119; above
       0 on 8 of 9), but a weighted Gini of -0.034 on the cost per year (below 0 on 8 of 9) and -0.016 on the claims
       per year.
     - Signal over the constant: cost per year, weighted Gini, GLMs 0.117 and 0.125 (SD 0.022 and 0.024, 9 of 9);
       claims per year, weighted Poisson deviance, the best three models 0.47% to 0.49% of the constant's deviance
       (SD 0.13% to 0.16%, 9 of 9); cost per year, weighted Tweedie deviance, GLMs 0.48% and 0.62% (6 and 8 of 9),
       every LightGBM below the constant.
     - Telling models apart: on the cost per year the GLM beats the regularised LightGBM by +0.031 Gini (8 of 9), and
       the Gini puts the five models in the same order as the Tweedie deviance on the same target; on the claims per
       year the GLMs and the regularised LightGBM tie (-0.0001, GLM ahead on 3 of 9). Within one test fold the Gini is
       noisier: bootstrap SE 0.034 on the gap of 0.051 between the GLM and the 300-round LightGBM, against 0.0018 on a
       gap of 0.0048 for the frequency deviance.
     - The claim size: on the claimants a gamma GLM gains nothing over the mean claim (-1.0% of the deviance, above 0
       on 4 of 9), and the frequency GLM's predictions score 0.1145 on the shipped Gini against 0.117 for the cost GLM.
       The six factors order the cost per year through its frequency; the size adds the heavy tail, which is what
       separates the GLM from boosting.
     - Ranking across the 9 splits (Kendall's W of the five models, 1 for the same order on every split): Tweedie
       deviance 0.90, claim occurrence 0.68, cost per contract 0.68, claims per year 0.66, cost per year Gini 0.54; the
       Gini's lower value comes from pairs that are close (the two GLMs, the two slower LightGBMs).
   * **Consistency:**
     - Andrej's `exposure` as a feature (2026-11-02): overturned, as D8 did; alone it scores ROC AUC 0.653 on the claim
       indicator and 0.205 weighted Gini, and a quote never has it[^a8b].
     - Andrej's Gini (2026-11-02): kept as the metric; its first form, unweighted on each row's cost, is overturned,
       since on it a model of the window earns 0.057 of the GLM's 0.119. His dollars (2026-11-02): kept, a Gini does
       not depend on the scale.
     - D8 (2026-11-06): kept in full. Its reason against the claim frequency gets a measured fact: here the claim size
       adds no order, and the frequency score cannot tell the reasonable models apart.
     - spanish_motor_insurance_2015_2018 (your B of 2026-11-08): the same clause, the other way for a stated fact.
       There the contract itself ends (a lapse, priced through the surcharge for paying in instalments) and the data
       record it to that end; here the extract's window ends the record while the contract runs on[^a8c].
     - fremtpl2 and bemtpl97 ship the claims per year because their sources score that; this source scores no
       frequency.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the current target (implemented), the clause amended | cost per year insured, weighted Gini, `exposure` the weight; one sentence added to the per-contract clause in the same change as spanish's | the insurer's own quantity; the window earns nothing (-0.034); separates the GLM from boosting (+0.031, 8 of 9) | sees only the order, so a tariff twice too steep scores the same; noisier within one fold |
     | b | Keep the current target, recorded as an exception | as a, with an exception line in the record, the notes and the rule's cases instead of the sentence | no second change to the clause | the first exception on the clause; the next table with a window needs one too |
     | c | Claims per year insured, weighted Poisson deviance | target `numclaims / exposure`; the cost leaves; as fremtpl2 and bemtpl97 | a score that sees the level and the spread; less noise within a fold; the window earns nothing | drops the claim size the insurer prices; the reasonable models tie; a third task of the same kind |
     | d | Cost per year insured, weighted Tweedie deviance | same target and weight, the metric changes | sees the level and the spread; same model order as the Gini | best gain 0.6% of the constant's; every LightGBM below the constant; a power and a floor to choose |
     | e | Claim cost per contract, unweighted Gini | Andrej's target of 2026-11-02 with `exposure` out and no weight | the clause as it reads; no rule change | the recorded cost is the window's part of the contract; predicting the window earns 0.057 of 0.119 |
     | f | Claim occurrence, ROC AUC | target `clm`, the book's measure | the book's own score (0.548 without the exposure, reproduced) | predicting the window earns 0.539 of 0.548; drops the count and the size; no insurer prices it alone |

   * **Recommendation:** a. The insurer prices the cost per year insured[^a8d]; dividing by the time observed and
     weighting by it removes the window that the per-contract cost and the occurrence reward[^a8b]; and on that
     target the Gini orders the models as the proper deviance does while resolving them better[^a8e]. The added
     sentence says what both tables show: a per-contract target needs the data to record each contract to its end,
     so no exception is needed[^a8c][^a8f]. c is the choice if a score that sees the price level counts for more than
     the claim size. **Decision:** a, b, c, d, e or f?

   **Notes for the AI:**
   - The numbers above are without `gender` (issue 7): the Tweedie GLM scores 0.117 and the Tweedie LightGBM of the
     metric reason (300 rounds) 0.067, where the reason now gives 0.120 and 0.059 with `gender`; update them when
     issue 7 is applied.
   - On a: `dataset.py`'s target, weight, metric and split stay. In `curation_comments`, the target bullet gets: "The
     per-contract clause of MET-14 (amended 2026-11-08) does not apply: the data record each one-year contract only
     inside the extract's window (98.1% part-years, 0.469 of a year per contract on average), so the recorded cost is
     the window's part of the contract's. A model of the exposure from the rating factors, used as the score, scores
     0.057 Gini on the cost per contract (the GLM 0.119) and -0.034 on the cost per year (9 shipped splits,
     2026-11-08)." In the metric reason, the sentence on the frequency becomes: "The alternative, the claim frequency
     with an exposure-weighted Poisson deviance, was not chosen: it drops the claim size the insurer prices, and on
     the shipped splits the GLMs and a regularised LightGBM tie on it (-0.0001, 3 of 9), while the weighted Gini on the
     cost per year separates them (+0.031, 8 of 9) and orders the five models as the weighted Tweedie deviance does."
     The main session amends MET-14's per-contract clause in metrics.md in one change with
     spanish_motor_insurance_2015_2018 issue 7 (B), for example: "A per-contract target stays when the planned term is
     constant and known at the prediction point and the data record each contract to its end; a cut known only at the
     policy's end and priced into the contract (a surcharge for paying in instalments) does not make the target a
     rate, and the notes give the share cut short (spanish_motor_insurance_2015_2018: 2,055 of 37,090). When the data
     observe only part of each term, as an extract window that cuts the policies at its edges, the recorded amount is
     the window's, not the contract's, and the rate ships (australian_vehicle_insurance_2004_2005: 98.1% part-years)."
     Update this table's row in MET-14's Cases (the window fact) and spanish's row; a CC line in the record; the
     resolved turn here and on spanish issue 7; `dataset check`.
   - On b: append to the record and the notes' target bullet, in bold label: "Exception to MET-14 (2026-11-08,
     Lennart): every policy has a one-year planned term known at the quote, but the data record 98.1% of them only
     inside the extract's window (0.469 of a year per contract on average), so the recorded cost is the window's part
     of the contract's; the cost per year insured, weighted by the time observed, is what the insurer prices. Serves
     P3 (USE-5)." The main session adds a row of kind `exception` to MET-14's Cases; spanish's amendment stands alone.
     The metric-reason sentence of a applies too.
   - On c: `_clean` builds `claims_per_year` = `numclaims` / `exposure`, asserts that it times `exposure` gives back
     `numclaims`, and drops `clm`, `claimcst0`, `numclaims` and `X_OBSTAT_`; `metric = Metric.from_context(
     "mean_poisson_deviance", params={"min_prediction": 1e-4}, inputs={"weight": "exposure"}, ...)` with a reason
     (the book fits no held-out frequency, the deviance of the offset model, fremtpl2's floor) and a definition;
     `ScoringColumn.used_by` and `sample_weight` follow; the `task_summary` (question, predicted, changes), the
     target-dominant acceptance (93.2% zero) and the decisions (the 200 floor goes to a note; the 7 rows become 52 to
     365 claims a year) are rewritten; the clause amendment of a; `dataset check`, the task probe and probe 22.
   - On d: `metric = Metric.from_context("mean_tweedie_deviance", params={"power": 1.5, "min_prediction": 1.0},
     inputs={"weight": "exposure"}, ...)`, the reason naming the power and the floor (two orders below the portfolio's
     293 dollars a year); the target stays on the identity scale; the clause amendment of a; `dataset check`.
   - On e: the target is `claimcst0` renamed `claim_cost`, `exposure` dropped (still never a feature), no weight
     scoring column and no `sample_weight`, `normalized_gini` from context; the notes name the window and the 0.057;
     spanish's amendment stands alone.
   - On f: the target is `clm`, binary, `roc_auc` with the book's in-sample AUC named as the original; `exposure`,
     `numclaims` and `claimcst0` dropped; the notes give the 0.539 of the window model.

   [^a8a]: Read by Andrej on 2026-11-02 (printed pages): Sec. 7.3-7.4 (logistic model, exposure in the link), Sec. 7.6
     (ROC AUC 0.662 against 0.548, in-sample), Sec. 8.3 and 10.5 (Tweedie and multiple-claim models, not fitted to this
     table), Sec. 10.4 (zero-adjusted inverse Gaussian model of the claim cost with its zeros, chosen by AIC). Whether
     a chapter fits a claim-count or a claim-size model to this table was not checked.
   [^a8b]: **LEAK-41** (Must): a column the task uses as a weight or a rate's denominator, cut after the prediction
     point, is never a model input, and neither is a column that encodes it; **MET-15** (Must): a realized denominator
     is the metric's row weight and the `sample_weight`.
   [^a8c]: **MET-14** (Should), as it reads: "A per-contract target stays when the planned term is constant and known
     at the prediction point"; amended on 2026-11-08 (Lennart, spanish_motor_insurance_2015_2018 issue 7, B): "a cut
     known only at the policy's end and priced into the contract does not make the target a rate".
   [^a8d]: **USE-5** (Must): predict what the actor acts on, at the resolution they act on it; **MET-1** (Must): the
     metric scores the decision of the use case.
   [^a8e]: **MET-10** (Weigh): the resolution on our folds and diversity; **MET-8** (Should): a proper score is
     preferred for the same goal; **MET-11** (Must): the Gini and the deviances here are all from context.
   [^a8f]: principles.md, "Strengths": a departure from a Should rule needs its fact recorded as an exception;
     "Exceptions and amendments": an amendment replaces the rule's text under the same ID.

   [^i8-rule]: **MET-14** (Should; 2026-11-06, Lennart, on fremtpl2 and bemtpl97): a count or amount accrued over a
     varying amount at risk ships as the rate per unit when the decision prices per unit; "A per-contract target stays
     when the planned term is constant and known at the prediction point; the notes give the share cut short
     (spanish_motor_insurance_2015_2018: 2,055 of 37,090)." **MET-15** (Must) makes a realized denominator the
     metric's row weight and the `sample_weight`, never a feature; it holds here.
   [^i8-strength]: principles.md, "Strengths": a departure from a **Should** rule "needs the fact that sets the case
     apart and the higher principle it serves, and is recorded as an exception"; "Exceptions and amendments": an
     exception goes into the record, the notes and the rule's Cases table, and an amendment replaces the rule's text
     under the same ID. The principle served here is P3 (**USE-5**, Must: predict what the actor acts on).
   [^i8-cases]: MET-14's Cases rows of 2026-11-06 in metrics.md: this table (applied) and
     spanish_motor_insurance_2015_2018 (the per-contract target stays); no exception on the clause is recorded yet.

   **Lennart (2026-11-08, discuss):** Reply (a): Keep the current target, the clause amended

   **Resolved (2026-11-08, Lennart):** (a). The claim cost per year insured stays, with `exposure` as its weight and
   the weighted Gini (D8 kept); MET-14's per-contract clause is amended in one change with
   spanish_motor_insurance_2015_2018's issue 7. The notes' target bullet says why the clause does not apply here, and
   the metric reason why the claim frequency was not chosen, with the numbers on the shipped splits without `gender`,
   which moved with the new splits (issue 7): a model of the window scores 0.056 Gini on the cost per contract (the
   GLM 0.124) and -0.034 on the cost per year; on the claims per year the GLMs and a regularised LightGBM tie (-0.0003,
   GLM ahead on 4 of 9), on the weighted Gini of the cost per year the GLM leads it by +0.016 (8 of 9; +0.031 on the old
   splits); the Tweedie GLM scores 0.119 and the 300-round Tweedie LightGBM 0.075 (0.117 and 0.067 on the old splits,
   as above). The record's CC line keeps D8. `dataset check`: 0 errors, 0 warnings.

9. **Ship the two age bands as numbers or as ordered categories?**

   * **Problem:**
     - `vehicle_age_band` (1 youngest to 4) and `driver_age_band` (1 youngest to 6) ship as integers, "the order of an
       age", and no curator has decided it.
     - Since the rule's amendment of 2026-10-30 (and the marks of 2026-10-31 and 2026-11-01), a scale the source ships
       as numbers is typed by whether the source says in words what each level is, and bands of a quantity become
       ordered categories[^i9-rule].
     - The two copies differ, since insuranceData names one end only ("1 (youngest), 2, 3, 4"), which points to a
       number, while CASdatasets names every level ("youngest cars" to "oldest cars"), and the band of an age is a
       band of a quantity, which points to an ordered category.
   * **Background:** The band limits are published nowhere, so an ordered category keeps the codes as its levels. The
     precedent check of 2026-11-01 read the integers as consistent with the rule as amended on 2026-10-21; the text on
     binned ranges and the test of words per level came later. Decision D8 of 2026-11-06 does not touch the bands.
   * **Effect on the task:** None for tree models. A linear model spaces the bands equally, though their limits are
     unknown (claims per year by driver band: 0.190, 0.158, 0.150, 0.145, 0.119, 0.118).
   * **Panel:** The column auditor and the critic read the bands as an ordinal scale, categorical by default; the
     definition and the advocate read insuranceData's one-ended labels as the numeric branch.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Numbers (implemented) | the bands stay integers; the notes cite insuranceData's labels at one end only | the copy we load; a code keeps its order | CASdatasets names every level; a linear model assumes equal steps |
     | B | Ordered categories | the bands typed as ordered categories, levels 1 to 4 and 1 to 6, youngest first | the rule's default for bands of a quantity; no spacing assumed | the levels stay codes, since the limits are unknown |

   * **Recommendation:** B: an age band is a band of a quantity, which the rule makes an ordered category whatever
     words the labels carry; A holds only if insuranceData's labels, named at one end, count over CASdatasets', which
     name every level. **Decision:** A or B?

   **Notes for the AI:** On B: `_feature_types` returns `FeatureTypes(categorical=[...], ordinal={"vehicle_age_band":
   [1, 2, 3, 4], "driver_age_band": [1, 2, 3, 4, 5, 6]})`, and the notes' bullet "The age bands ... stay numbers, the
   order of an age" says instead that they are ordered categories with their codes as levels, the limits being
   unpublished; re-run `dataset check` and the dtype probe. On A: that bullet cites the branch (insuranceData labels
   one end only), and the curator's call goes into a CC line.

   [^i9-rule]: **CLEAN-14** (Should; amended 2026-10-30, Lennart: "ordinal scales are case-by-case, they could be
     either but generally we know they are not numeric so categorical might be the safer bet"; the marks of 2026-10-31
     and 2026-11-01): an ordinal scale (a grade, a stage, binned ranges) "is decided case by case, categorical by
     default"; "A scale the source ships as numbers is typed by what the source says its levels are", the test being
     "does the source say in words what each level is?"; a score with words only at its two ends is a number; "Bands
     of a quantity ("21-25", "1-10%", "3 or more") are ordered categories with the band labels, decoded where the file
     stores a band's number." open_university_learning_analytics_dataset ships its `age_band` as ordered categories.

   **Resolved (2026-11-08, Lennart):** B. `_feature_types` types `vehicle_age_band` (levels 1 to 4) and
   `driver_age_band` (levels 1 to 6) as ordered categories, youngest first, the codes kept as levels since the band
   limits are unpublished; the notes' bullet says so, with a CC. `dataset check`: 0 errors, 0 warnings; the dtype probe
   flags 0 of 6 columns.

10. **Ship `gender` again, now that today's law of the data's country decides on sex in insurance pricing?**

   * **Problem:**
     - On 2026-11-08 `gender` left the features under the family stance that sex leaves every insurance pricing task,
       whatever the jurisdiction (issue 7)[^i10-old].
     - On 2026-11-09 Andrej replaced that stance: sex leaves an insurance pricing task when the law of the country the
       data come from bars it today, as if the ban had always applied, and stays where that law allows it[^i10-rule].
     - Australian law allows it, so the drop of issue 7 has no ground left and that issue reopens.
   * **Background:**
     - Section 41(1) of the Sex Discrimination Act 1984 (Cth), compilation of 1 November 2025, read on 2026-11-09:
       discrimination on the ground of the client's sex in the terms on which an insurance policy is offered is not
       unlawful when it "is based on actuarial or statistical data from a source on which it is reasonable for the
       insurer to rely" and "is reasonable having regard to the data", the data to be shown to a client who asks in
       writing[^i10-law].
     - The four EU tables keep sex dropped under the same rule, as EU law bars it today: bemtpl97,
       frempl_french_motor_personal_line, pricing_game_2017_french_mtpl and
       spanish_homeowners_motor_insurance_2010_2014.
   * **Effect on the task:** six rating factors instead of five. Adding the column changes the rows' content order and
     so the shipped splits. On the new splits, every fit weighted, the score with `gender` minus without on the same 9
     splits (SE over the splits): a Tweedie GLM 0.133 against 0.130 (+0.004, SE 0.001, higher with it on 7 of 9), the
     300-round Tweedie LightGBM -0.004 (SE 0.004, 3 of 9), the L2 LightGBM -0.007 (SE 0.008, 6 of 9), a regularised
     Tweedie LightGBM over 3 seeds -0.002 (SE 0.001, 2 of 9; seed SD 0.001) and a regularised L2 LightGBM +0.002 (SE
     0.002, 6 of 9). A small gain for the GLM, as on 2026-11-08 (+0.004, 7 of 9), none above noise for boosting.
   * **Experiments:** on the new definition `dataset check` gives 0 errors and 0 warnings. The leak probes find no
     feature alone above an R^2 of 0, and 42.7% of the test rows have an exact copy of the six factors in train (coarse
     rating cells, as before). The weight-proxy probe finds that the factors predict the exposure at R^2 0.074 and that
     none gains through it above noise. The shared-unit lookup adds -0.002 (SE 0.003), the hidden-group probe finds no
     group and the dtype probe flags 0 of 6 columns. The task probe's linear family scores 0.122 on the declared metric
     against the dummy's 0, on 5 of 5 splits (its `no_signal` flag reads the squared-error skill, as before).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Ship `gender` again (implemented) | `gender` back among the rating factors; the notes name s41 and the rule of 2026-11-09 | the input an Australian insurer may use at the quote; follows the rule as amended | the family's inputs differ by country |
     | b | Keep it dropped | five rating factors, as on 2026-11-08 | one input set for the whole family | against the rule of 2026-11-09; withholds an input the actor may use |

   * **Recommendation:** a, as the rule of 2026-11-09 says; the measured effect is small either way. **Decision:** a or
     b?

   **Notes for the AI:** on a (done): `gender` back in `_clean` and `_feature_types`, `known`, `changes` and
   `fit_reason` without the drop, the notes' gender bullet with s41 and the measured effect, a CC bullet, the model
   numbers of the notes and the metric reason re-measured on the new splits, the record's CC line, a CHANGELOG entry;
   the Tensions row in principles.md amended and a USE-6 Cases row in use_case.md.

   **Andrej (2026-11-09, as implemented):** I go with a. (his mark on the cross-dataset item "Keep sex out of every
   insurance pricing task, or decide by each use case's actor?", option a)

   **Resolved (2026-11-09, Andrej):** a. `gender` ships again as a rating factor: sex leaves an insurance pricing task
   when the law of the country the data come from bars it today, as if the ban had always applied, and stays where that
   law allows it, and Australian law allows it (s41 of the Sex Discrimination Act 1984). This reopens issue 7 (Lennart,
   2026-11-08), whose drop rested on the family stance this rule replaces. The Tensions row on rating factors in
   principles.md is amended so. `dataset check`: 0 errors, 0 warnings.

   [^i10-old]: principles.md, "Tensions", the row on "a rating factor known at the prediction point against a factor the
     actor may no longer use", as amended on 2026-11-08 (Lennart, this table's issue 7): "sex leaves the rating factors
     of every insurance pricing task, whatever the actor's jurisdiction, as if the actor priced in the EU".
   [^i10-rule]: The same row, amended 2026-11-09 (Andrej, on the cross-dataset item of the information audit: "If the EU
     bans it today, we treat it as if it also has been banned before. For non-banned countries, we use it."); **USE-6**
     (Must): "Anything known at the prediction point is a legitimate input"; **USE-1** (Must).
   [^i10-law]: Sex Discrimination Act 1984 (Cth), s41(1)(a) to (e),
     https://www.legislation.gov.au/C2004A02868/2025-11-01/2025-11-01/text/original/epub/OEBPS/document_1/document_1.html.
     The EU ban: CJEU C-236/09 (Test-Achats), in force for new contracts from 21 December 2012.


**Review panel:** ship after changes (mediator). Tier full, re-review of 2026-11-06 under LEAK-41, MET-14 to MET-16,
after decision D8 (issue 6): 12 reports. Claims: 39 audited, 34 hold (a few only approximately), 3 refuted in their
wording (the Outcome's "every model family probed beats the weighted constant on 9 of 9", "exposure spread evenly",
the record's old statements that `exposure` is a feature; all fixed), 1 partly tested (CAS Monograph 5 Sec. 7.2.4,
whose PDF did not render), 1 untested (the book's sections, read on 2026-11-02). Blind review: exclude as prepared, on
weighted RMSE and deviances the task does not score; both debaters drop the exclusion, and its point that the Gini
cannot see calibration is now in the metric reason. Task gamer: the six features cannot be gamed; all five exploits
read `exposure`, which `feature_columns()` drops (1/exposure alone 0.205, an honest frequency model divided by the
exposure 0.2275), and all are known. Agreed: ship with text changes only, no change to rows, features, target, weight,
split or metric; the 7 high-rate rows kept; the forced split. Disputed: `gender` against bemtpl97 (issue 7); a hold or
an exception under the per-contract rule (issue 8); the age bands as numbers or ordered categories (issue 9). Settled
by the mediator: the training-weight gate is the collection's, one line in the Outcome, and the probe's `no_signal`
flag is re-checked with the first tuned run. The panel read the L2 arm of probe 22; its weighted Tweedie arm, run
afterwards, agrees. The mediator's issues 1 to 3 are issues 7 to 9 here.

<details><summary>Mediator</summary>

**MEDIATOR REPORT: australian_vehicle_insurance_2004_2005 (exposure re-review, full tier, 2026-11-06)**

I ran no new experiment. No fact was in dispute that needed one: advocate and critic agree on every number, and the one apparent clash (the task gamer's "no feature proxies exposure", corr 0.0003, against probe 22's R² 0.074) is linear correlation against a nonlinear fit. Probe 22 already settles it: R² 0.074, no mediated gain above noise, and the column auditor measured R² 0.080 on no-claim rows, where no claim can have cut the exposure.

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes (text only; rows, features, target, weight, split and metric unchanged).
Validity: SEL holds; USE-1 holds (approximate fit, "for example" actor); LEAK-41 holds (exposure is only the weight
  scoring column, the metric's weight input and sample_weight; probe 22: R² 0.074 from the factors, 0.080 on no-claim
  rows, a start-date cohort kept by timing, USE-6; no mediated gain above noise); LEAK-10 holds (clm, numclaims,
  claimcst0 dropped); SPLIT-8 holds (forced IID, settled 2026-11-02; re-measured on the rate: no drop under file-order
  or rating-cell holdouts); USE-6 / Tensions row: `gender` kept with no stated fact against bemtpl97 (issue 1);
  USE-5 / MET-14: the rate departs from the per-contract clause without the fact recorded (issue 2).
Value: TP-1 flag `no_signal` (MSE skill under a Gini metric) answered by the fitted families on the declared metric
  (linear 0.120 beats the dummy on 100% of the probe's splits), re-check with the first tuned run; TP-2: a small real
  signal, keep; TP-3 not yet applicable (no tuned results); MET-15 holds at the definition (any run waits on the
  collection's training-weight gate); MET-11 / MET-13 hold (the scorer matches a brute-force Lorenz area to 1e-12;
  constant 0, perfect 1, reversed -1 on 9 of 9).
Quality: CLEAN-10/11 hold (53 values of 0 made missing); CLEAN-16 as amended holds; CLEAN-14: age bands as int64,
  open (issue 3).
Weighed: documented textbook table +, standard actuarial formulation (rate plus weight) +, six coarse factors -, thin
  signal (best honest 0.109-0.120) -.
For the curator: issue 1 (gender against bemtpl97, s41), issue 2 (MET-14 exception or amendment), issue 3 (age bands).
```

**2. Changes to make now (no decision needed)**

All are in `dataset.py`, `REVIEW.md` and the record. Then regenerate the README and add a dated CHANGELOG entry (house rule).

1. **REVIEW.md Outcome, Value line (TP-1 Must, TP-2).**
   - The line "every model family probed beats the weighted constant on 9 of 9" is refuted: the probe's untuned RF beats it on 7 of 9 (claim auditor #16).
   - Write instead: "the three families fitted with the weight beat it on 9 of 9 (Tweedie GLM 0.120, Tweedie LightGBM 0.059, L2 LightGBM 0.060)".
   - Add the probe's `no_signal` flag and its reading: MSE-based skill (best R² 0.0002) under a Gini metric. The probe ran on 5 of 9 splits; its linear family scores 0.120 and beats the dummy on all of them.
   - Mark "re-check with the first tuned run". Precedents: sf_permit_time, heart_disease, open_university_learning_analytics_dataset.
2. **REVIEW.md Outcome, the run gate (MET-15).** One line: "Like every container with a sample_weight, it enters no run before the collection's training-weight gate (BENCHMARK_CHANGES_TODO.md, 'The gate')."
   - The same line belongs in the five weighted siblings (fremtpl2, bemtpl97, frempl, pricing_game_2016_french_fleet, spanish coverage), so like cases read alike. None of them has it today.
3. **REVIEW.md Outcome: "Left for Andrej: none" is wrong.** Lennart's D8 of 2026-11-06 supersedes Andrej's issue-2 call and changes the form of his issue-4 call. Say so and tell Andrej. The newer curator decision wins (principles, "Who decides").
4. **Metric reason (MET-11; domain practitioner; both briefs agree).** After "The Gini ignores the price level", add the following.
   - It also ignores the spread of the relativities: any monotone transform scores the same. A GLM with doubled log-relativities keeps 0.120 but is worse than the weighted constant on exposure-weighted Tweedie deviance (p 1.5) on 9 of 9 splits.
   - The untuned Tweedie LightGBM (Gini 0.059) is also worse than the constant on that deviance on 9 of 9.
   - Why the deviance was not chosen: the best honest gain is 0.5% of the constant's deviance (SE 0.2, 8 of 9).
5. **Split bullet and REVIEW issue 1 (EV-2, stale numbers).** Replace the numbers measured on the old cost target with the split auditor's numbers on the rate target, weighted:

   | Check | LightGBM | GLM |
   |---|---|---|
   | Train on earlier quarters of the file, test on the next | 0.078 | 0.128 |
   | Random splits of the same sizes | 0.060 | 0.111 |
   | Grouped by rating cell | 0.054 | 0.119 |
   | Shipped random split | 0.059 | 0.120 |
   | Grouped by full row | 0.077 | 0.127 |

   The conclusion is unchanged.
6. **Split bullet wording (claim auditor E11).** "exposure spread evenly over 1-365 days" is refuted. Write "spread over 1-365 days, about 6,300 per 30 days at the short end falling to about 4,300 at the long end".
7. **The record line (PROV-16, records hygiene).** Add "Assessment (AI, 2026-11-06): supersedes the statements above that `exposure` is a feature known at pricing (2026-10-30 body and assessment), that it stays a feature under LEAK-11 (2026-11-01 assessment), and that the target is `claimcst0`; see the CC of 2026-11-06 (D8)."
8. **Optional, Could (split auditor b, c).**
   - One clause in the split bullet: exposure is also cut at the extract window's edges, and both IID sides share the one window. A future temporal split must re-check the cutoff cut (SPLIT-9, LEAK-41).
   - The exposure drift along the file order (0.42-0.53 per tenth, chance SD 0.0035), next to the 12.2% adjacent-day-count fact.
9. **Optional minor numbers (claim auditor).**
   - "120-125 copies (20 runs)" is an interquartile range; the full range is 98-139.
   - The log-exposure coefficient is "about 0.3" (0.28-0.31 by design).
   - The excess claims: 145 to 147.
   - "1/exposure alone, the ceiling a proxy of it would reach" is loose. A model that reads exposure together with the factors scores more: 0.2275 for the gamer's frequency model divided by exposure, 0.236 for the notes' own GLM. "What the weight alone scores" is exact.
10. **No action: the known framework nit.** Bundle duplicate checks count the weight as a feature: 61 conflicting rows reported, 7,512 on the six real features. It is being fixed; regenerate the README after the fix.

**3. Issues for the curator, ranked (validity first, Must first)**

**Issue 1 (P3, USE-6 and the Tensions row "a rating factor ... the actor may no longer use"; consistency check case 2): what sets `gender` here apart from bemtpl97's `sex`?**
- Problem: bemtpl97 dropped `sex` on 2026-11-05 (an EU insurer pricing today, Test-Achats). This definition keeps `gender` for "an Australian car insurer" and gives no reason.
- Effect: none on the data if the actor may price on sex. One of the six features goes if it may not.
- Advocate's best evidence: the likely fact is jurisdiction. The Sex Discrimination Act 1984 (Cth) s41 allows sex-based terms in insurance when they rest on actuarial or statistical data that it is reasonable to rely on. That is my reading of the statute too, but I did not check the text in this run.
- Critic's best evidence: the rank of this question does not depend on today's change. The precedent went the other way, so principles.md requires the prompt before the dataset runs.
- Options:
  - (a) Verify s41. Write in the notes that the actor is an Australian insurer and the law permits the factor. Add this table as a case of the Tensions row.
  - (b) Drop `gender` like bemtpl97 (against the use case).
  - (c) Reopen bemtpl97 (no reason found).
  - (d) Amend the Tensions row: "the actor's jurisdiction decides, and the definition names the law".
- Recommendation: (a), with (d) when home_credit (`CODE_GENDER`) and credit_card_clients (`SEX`) are reviewed.
- What would settle it: the text of s41.

**Issue 2 (P6, MET-14 Should; principles "Strengths": a Should departure records its fact): exception or amendment for the rate target.**
- Problem: MET-14's clause says "a per-contract target stays when the planned term is constant and known at the prediction point". That holds here (one year at every quote), yet D8 ships the rate. spanish_motor_insurance_2015_2018 kept per contract on the same day.
- The fact that sets this case apart is measured and agreed: 98.1% of these policies are observed only part of the year (median 163 days, 1.9% full years), so the recorded cost belongs to a window, not to the contract. In spanish 2015-2018 only 5.5% are cut short.
- Effect: none on the data. The rule and the decision disagree on paper.
- Both sides agree on the remedy and differ only in the label (hold or exception).
- Options:
  - (a) "Exception to MET-14 (2026-11-06, Lennart)" with that fact, serving P3 and USE-5, plus a Cases row. It is the first exception on this clause.
  - (d) Amend the clause to "... known at the prediction point and observed in full for most rows". The rule then says what it meant, and no exception is needed.
- Recommendation: (d) if the clause assumed a term observed in full (spanish's reasoning suggests it did); otherwise (a).

**Issue 3 (P7, CLEAN-14 Should, case by case): the age bands as int64 or ordered categories.**
- Not caused by today's change and never decided by a curator. The 2026-11-01 precedent check read it as consistent with CLEAN-14 as amended 2026-10-21. The "binned ranges ... categorical by default" text and the 2026-11-01 "words for each level" test came later.
- For ordered categories (column auditor, critic): bands of an age are an ordinal scale, categorical by default. CASdatasets names every level ("youngest cars" to "oldest cars").
- For numbers (definition, advocate): insuranceData names only one end ("1 (youngest), 2, 3, 4"). That points to the numeric branch of the 2026-11-01 test.
- Effect: none for trees. A linear model spaces the bands equally, though their limits are unknown.
- Options:
  - (a) `FeatureTypes(ordinal={"vehicle_age_band": [1, 2, 3, 4], "driver_age_band": [1, 2, 3, 4, 5, 6]})`.
  - (b) A note that the bands stay numbers under the "words at one end only" branch.
- What would settle it: which source's level names count for the test.

**4. Disputed points, settled**

- **D1. Training-weight gate: a dataset condition, or the collection's (MET-15 Must)?**
  - MET-15 binds the definition: the denominator is the metric's row weight and the task's sample_weight, never a feature. It holds (claim auditor #2).
  - The harness gap is real: an unweighted Tweedie GLM scores 0.022 against 0.109 weighted, worse on 9 of 9. But the gate that answers it is already a collection rule covering all six weighted containers, and none of them was held on it. Treat like cases alike.
  - Settled: no dataset-specific hold. One pointer line in the Outcome (change 2). The critic's wording and the advocate's are the same in substance.
- **D2. TP-3 on untuned fits.** The critic is right: TP-3 says "tuned methods", and none exist for this formulation. The keep rests on TP-2 (Should; no concrete reason found in the task), and TP-1 (Must) requires the tuned re-check. Settled: change 1. It is a follow-up mark, not a hold. The advocate accepted it.
- **D3. `gender` "outside today's change".** The critic is right that rank does not depend on today's change. Principles.md's consistency check (case 2) puts it before the curator. The remedy is agreed. Settled: issue 1.
- **D4. Blind reviewer's "exclude" (P6).** Its evidence scores metrics the task does not ship (weighted RMSE, deviance, frequency). On the declared metric the fitted families beat the constant on 9 of 9, and the GLM beats LightGBM by +0.061 (SE 0.007, 9 of 9). TP-2 keeps the task, and both sides drop the exclusion. What survives of it is the blindness to calibration, which goes into the metric reason (change 4).
- **D5. Dropping short exposures from scoring, or capping the rate (blind reviewer, task gamer).**
  - Both select rows by the realized weight, which LEAK-41 (Must, P4) and USE-7 forbid. They serve a P6 preference, so the higher rank wins.
  - The weighted Gini counts each row by its cost: the 7 rows at 1M a year or more hold 1.26% of the cost.
  - Settled: keep, as D8 decided.
- **D6. MET-14 "hold" or "exception".** The two sides differ only in the label. Recording an exception or amending the rule is the curator's: issue 2.

**Task gamer's exploits, mapped.** None is a `Potential leak, kept on purpose:`: the leak is removed, not kept. All five need the scoring column, which feature_columns() drops. All are known. No measured gain contradicts the notes.

| # | Exploit | Score | Rule | Known? | Gain against the notes |
|---|---|---|---|---|---|
| 1 | Honest frequency prediction / exposure | 0.2275 (+0.139) | LEAK-41, USE-3 timing | Known (notes: exposure read with the factors, GLM 0.236) | Within the notes' range; only the "ceiling" wording is loose (change 9) |
| 2 | Exposure as a feature, Poisson frequency | 0.208 (+0.120) | LEAK-41 | Known | Matches +0.089 to +0.124 |
| 3 | 1/exposure alone | 0.2050 | LEAK-41 | Known | Identical to the notes' 0.205 |
| 4 | Exposure as a feature, L2 / Tweedie LightGBM | +0.09 / +0.12 | LEAK-41 | Known | Matches |
| 5 | 1/exposure as a feature | +0.080 | LEAK-41 | Known | Same class |

- The gamer's fixes: "keep exposure from the model" is already the API. "Drop exposure < 0.1 from scoring" breaks LEAK-41 and USE-7 (D5). "Score per planned year" is the MET-14 clause question (issue 2).
- The null attacks hold: row position, vehicle_value format and the NaN flag show nothing (LEAK-13 not triggered).
- The only residual risk is a harness that hands the model scoring.parquet or drops the weight. That is the collection gate (D1).

**5. Agreed facts**

- **Features and weight.** The six features are vehicle_value, vehicle_body, vehicle_age_band, gender, area and driver_age_band. `exposure` is only `ScoringColumn(role="weight")`, the metric's `weight` input and `sample_weight`.
- **Target.**
  - The target is claimcst0 / exposure, rebuilt to 3.6e-12. It is 0 on exactly 63,232 rows (93.2%).
  - The weighted portfolio rate is 292.90 a year, against 755.26 unweighted (2.58x).
  - Exposure runs from 1 to 365 days (median 163); 1.9% are full years and 98.1% part-years.
- **The 7 rows at 1M a year or more.** Each has one claim on 1-7 days, ordinary costs of 8.6k to 25.6k. They hold 1.26% of the cost and 45% of the weighted SS (92% unweighted). Each test fold holds 1-4 of them.
- **Honest scores (weighted, 9 shipped splits).**

  | Model | Weighted Gini |
  |---|---|
  | Tweedie GLM | 0.120 (0.109 in the claim auditor's design), 9 of 9 above the constant |
  | Tweedie LightGBM | 0.059 |
  | L2 LightGBM | 0.060 |
  | Regularised RF | 0.088 |
  | Constant | 0 |

  GLM minus LightGBM is +0.061 (SE 0.007, 9 of 9). Per-fold SD is about 0.02-0.03.
- **With exposure read as a feature.** It adds +0.089 to +0.124 (9 of 9). 1/exposure alone scores 0.205.
- **Probe 22.** The factors predict exposure at R² 0.074 (0.080 on no-claim rows), mostly through vehicle_value. No mediated gain rises above noise.
- **Without the weight.** A Tweedie GLM scores 0.022 against 0.109, worse on 9 of 9.
- **Scorer.** It equals a brute-force Lorenz area (0.456702279408 against ...409). Constant 0, perfect 1, reversed -1.
- **Split.** 3x3 random, disjoint, balanced (test-fold mean exposure 0.465-0.471, KS p 0.095-0.994). 42-43% of test rows have an exact copy of the six factors in train: coarse cells of distinct policies, 1-NN R² -1.2. No drop under rating-cell grouping or file-order holdout.
- **Deviance (practitioner).** On weighted Tweedie deviance only the GLM beats the constant (8 of 9). A GLM with doubled relativities keeps Gini 0.120.
- **Task probe.** `no_signal` (MSE skill), 5 of 9 splits, RF 0.026, LightGBM 0.037, linear 0.120.
- **Record and REVIEW text.** The record's 2026-10-30 and 2026-11-01 text on exposure as a feature is stale and unmarked. "Spread evenly" is wrong. The split numbers are on the old target. "Left for Andrej: none" is wrong.
- **Precedent.** The reversal of Andrej's issue-2 call is required by LEAK-41 (Must). All six siblings were decided alike on 2026-11-06.

**6. Consistency with precedent**

- **D8 itself is consistent.**
  - It reverses Andrej's 2026-11-02 keep under LEAK-10 with a fact measured afterwards (47-82% of the gain on counts is leak; +0.089 to +0.116 on the shipped splits) and a new P4 Must (LEAK-41). Keeping his call would now break that Must.
  - It matches fremtpl2, bemtpl97, frempl, pricing_game_2016 and spanish coverage, all of 2026-11-06. Liberty stays apart, with its reason stated: the weight is a function of the features.
  - Keeping the 7 rows matches fremtpl2's uncapped counts. The register has no flag on this dataset.
- **Reflection prompt 1 (precedent checker), MET-14's per-contract clause against spanish_motor_insurance_2015_2018.** Consistency check (AI, 2026-11-06): the clause, read literally, keeps a per-contract target here too. The distinguishing fact is 98.1% part-year here against 5.5% cut short there; it is measured but not written as what sets the case apart. Options: (a) an exception note; (b) treat like spanish (a window artifact, against USE-5); (c) reopen spanish (no reason); (d) amend the clause to "observed in full for most rows". Recommended: (a) now, or (d). This is issue 2.
- **Reflection prompt 2 (precedent checker), `gender` here against bemtpl97's `sex`.** Consistency check (AI, 2026-11-06): the likely fact is jurisdiction (SDA 1984 (Cth) s41), written nowhere. Options: (a) record it once verified, plus a Tensions-row case; (b) drop `gender`; (c) reopen bemtpl97; (d) amend the Tensions row so the actor's jurisdiction decides. Recommended: (a), then (d) with home_credit and credit_card_clients. This is issue 1.
- **Run gate (D1).** The pointer line belongs in all six weighted siblings or in none (treat like cases alike).
- **The tuned re-check mark (change 1)** follows sf_permit_time, african_credit_scoring_challenge and open_university (TP-1 and TP-3 Cases).
- **A rule-file wording point.** leak_checks.md's probe-22 row cites R² 0.06 (the study's own KFold), while the shipped-split probe gives 0.074. Both are true; the row could name both. No conflict.

**Sources**

- The panel's reports, the four debate files and `probes/task.txt`.
- The definition, `REVIEW.md` and the record.
- The gate: `BENCHMARK_CHANGES_TODO.md` ("Training weights", "The gate").
- Rules: principles.md; metrics.md MET-14, MET-15; task_probes.md TP-1 to TP-3; leak_checks.md LEAK-41; cleaning_features.md CLEAN-14.

</details>

<details><summary>Claim audit</summary>

**CLAIM AUDITOR: australian_vehicle_insurance_2004_2005 (exposure re-review, 2026-11-06, full tier)**

Every test runs on the shipped container (load_definition(...).to_container()), its 9 shipped splits and the shipped
scorer; raw-file facts on the raw dataCar.csv.

VERDICT: today's change (D8) holds. Every validity claim survives a test that could have refuted it: exposure is not
a feature, the sample weight is the metric's row weight (MET-15), the metric scores what it says, and an independent
re-fit gives the claimed scores. Three refuted claims, all about accuracy or reporting, none a Must on validity:
(1) "every model family probed beats the weighted constant on 9 of 9" (REVIEW Outcome) is false for the task probe's
untuned random forest, and the probe's `no_signal` flag goes unreported; (2) "exposure spread evenly over 1-365 days"
overstates (a third fewer policies at the long end); (3) the record keeps 2026-10-30 / 2026-11-01 text saying exposure
is a feature, and nothing marks it superseded. The largest open risk lies outside the definition: a harness that does
not pass `sample_weight` scores about a fifth of a weighted fit (Tweedie GLM 0.022 against 0.109).

TODAY'S CHANGES (D8) FIRST

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | `exposure` is no feature; 6 features remain | CHANGES; task_summary.known; notes "Exposure" | feature_columns(c) | holds | features = vehicle_value, vehicle_body, vehicle_age_band, gender, area, driver_age_band; exposure is only ScoringColumn(role=weight) | LEAK-41, MET-2 |
| 2 | sample_weight is the metric's row weight | dataset.py `sample_weight="exposure"`, `inputs={"weight":"exposure"}` | sample_weight(c); MetricSpec.inputs | holds | sample_weight(c)='exposure'; objective_metric.inputs={'weight':'exposure'}; scoring column used_by=normalized_weighted_gini | MET-15 |
| 3 | target = claimcst0/exposure; _clean rebuilds the cost | notes "Target"; _clean | sorted(y*e) vs sorted(claimcst0) (shipped rows are reordered) | holds | max abs diff 3.6e-12; 67,856 rows | MET-14 |
| 4 | 0 for exactly the 63,232 without a claim (93.2%) | task_summary.predicted; accepted warning | count; clm==0 vs claimcst0==0 | holds | 63,232 (93.19%); equality on every raw row | accepted warning |
| 5 | exposure 1 to 365 days, full year 0.9993, median 163 days, 1.9% full years, no 366-day row; 98.1% part-years | notes; metric reason | days = e*365.25 | holds | min 1.0, max 365.0 (0.99932), median 163, full-year 1.90%, part-years 98.10%, >365.5 days: 0 | - |
| 6 | weighted fit estimates 292.90/yr, unweighted 755.26 (2.6x) | notes "Target"; REVIEW issue 6 | sum(w y)/sum(w); mean(y) | holds | 292.905 and 755.259, ratio 2.58 | MET-15 |
| 7 | 7 policies at >= 1M/yr, 1-7 days, the listed costs, 1.26% of cost; max 5.24M | notes; _decisions | raw rows rate >= 1e6 | holds | days 1,1,2,2,4,4,7; costs 14,343, 8,605, 16,307, 13,819, 20,891, 17,604, 25,594; one claim each; 1.258% of cost; max 5,238,879 | USE-7 |
| 8 | they hold 45% of the exposure-weighted SS of the rate (92% unweighted) | notes; metric reason | e*(y-mu_w)^2 and (y-mean)^2 | holds | 45.3% and 91.5% | MET-2 |
| 9 | actuaRE removes them and body types < 100 exposure-years, 67,566 left | notes | filter on raw | holds | 67,566 (BUS 25.8, CONVT 32.6, MCARA 59.3, RDSTR 11.7 years removed); actuaRE's help page says 67,566 policies | PROV |
| 10 | in the weighted metric each counts by its cost, not its rate | notes; Decision 3 | the metric's L = cumsum(w*y) = cumsum(claimcst0) | holds | by construction, checked in the code (_weighted_gini) | MET-15 |
| 11 | honest Tweedie GLM 0.120, Tweedie LightGBM 0.059, L2 LightGBM 0.060, constant 0; with exposure +0.116/+0.089/+0.099, 9 of 9; 1/exposure 0.205 | CHANGES; notes; metric reason; REVIEW issue 6 | independent re-fit on the 9 shipped splits, all weighted (my own banding of vehicle_value; LightGBM tweedie 300x0.05, 15 leaves) | holds | GLM 0.109 (SD 0.027), 9/9 > 0; LightGBM-Tweedie 0.061 (SD 0.017), 9/9; GLM + log(exposure) 0.230, +0.121, 9/9; 1/exposure 0.2050 (per fold identical to remeasure.txt); constant -0.0 on every fold | LEAK-41, TP-2 |
| 12 | probe 22: factors predict exposure at R^2 0.07, Spearman 0.26, mostly vehicle value; no feature gains through it above noise | notes; CHANGES | probe outputs probe22.txt / probe22_l2.txt | holds | R^2 0.074 / 0.071, Spearman 0.269 / 0.264; vehicle_value 68-70% of gain; every mediated gain within 1 SD | LEAK-41 |
| 13 | 193 claims >= 80% of vehicle value, median exposure 0.37 vs 0.65, MW p < 1e-20 | notes; Decision 2 | raw, share = cost/(veh_value*1e4), finite only | holds | 193 (199 if the 6 claims on a vehicle value of 0 count as inf), 0.370 vs 0.646, p = 4.2e-21 | LEAK-41 |
| 14 | <= 0.2 years: 147 more claims than the longer rate predicts; <= 7 days 0.85/yr without write-offs; 0.14-0.17 above 0.2 years | notes "Exposure" | raw numclaims / exposure | holds (approx.) | 145.4 excess; 0.847/yr; bands 0.171, 0.156, 0.150, 0.140 | - |
| 15 | free log-exposure coefficient 0.29-0.31 in a Tweedie GLM | notes | TweedieRegressor on cost, p 1.5-1.7, + log(exposure) | holds (approx.) | 0.278-0.285 with my design | - |
| 16 | TP-2 "every model family probed beats the weighted constant on 9 of 9 splits" | REVIEW.md Outcome, "Value" | the task probe's untuned families with its settings, weighted, on the 9 splits | REFUTED (wording) | probe-style RF (200 trees, leaf 2, sqrt) 0.031 mean, above 0 on 7 of 9; task probe itself: RF 0.026 (SD 0.026), LightGBM 0.037 on 5 splits, flag `no_signal` (TP-1, TP-2, from weighted-MSE skill: best R^2 0.0002) not reported in REVIEW. The three fitted families (Tweedie GLM, Tweedie and L2 LightGBM) do hold 9/9, and so does a regularised RF (leaf 50: 0.088, 9/9) | TP-2 |
| 17 | 42-43% of test rows have an exact copy of the six factors in train; 34,974 rows (51.5%) share them | notes "copies"; copies.txt | hash of the 6 features over the splits | holds | 34,974 (51.5%); split 0/0 42.9% | LEAK-18 |
| 18 | "Known framework nit: bundle duplicate checks count the weight column as a feature" | CHANGES | conflicting duplicates with and without exposure | holds (nit confirmed) | with exposure 142 rows (bundle reports 61), on the 6 real features 7,512 rows share their factors with a row of another target; the README's INFO line understates it | - |

METRIC (MET-1, MET-2, MET-3, MET-11, MET-13, MET-15)

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| M1 | no source metric for this claim-cost regression; context origin | metric reason | looked once more: insuranceData/CASdatasets/actuaRE pages, web search for a held-out metric on dataCar/ausprivauto0405 | holds | nothing new; actuaRE builds the rate with exposure as weight (no metric); Ye et al. 2022 (unweighted Gini plus others) already named as context | MET-1, MET-11 |
| M2 | CAS Monograph 5 Sec. 7.2.4 sorts by predicted loss cost per exposure, exposure on the x axis | metric reason | fetch the monograph | partly tested | 7.2.4 is "The Gini Index" in the 2019 printing (contents found by search); the PDF did not render here; CAS RPM decks give exactly this construction (sort by predicted pure premium, cumulative earned car-years on x, losses on y). The 2025 second edition may number it differently | MET-11 |
| M3 | the declared definition is what the code computes | definition string; metrics.py _normalized_weighted_gini | brute-force trapezoid Lorenz-area Gini on fold 0/0, random scores without ties | holds | shipped 0.456702279408 vs brute 0.456702279409 vs CAS area form 0.456702279409 | MET-13 |
| M4 | a constant scores 0; ties averaged | definition | constant, perfect and reversed scores on every fold | holds | constant -0.0, perfect 1.0, reversed -1.0 on 9/9 | MET-13 |
| M5 | computable on every test fold | MET-2 | test fold contents | holds | 22,618-22,619 rows, 1,520-1,560 claims, 1-4 of the >= 1M rows per fold; the weight ships in every row and is no feature | MET-2 |
| M6 | identity scale is right for a Gini on the rate | notes; CLEAN-16 amended | the Gini is rank-only on p; target_transform identity | holds | MetricSpec.target_transform = identity; the notes say what a weighted fit estimates (CLEAN-16 asks for that) | MET-3, CLEAN-16 |
| M7 | the weight matters: an unweighted fit estimates the wrong quantity | MET-15 why; notes | same Tweedie GLM fitted with and without sample_weight | holds (strongly) | weighted 0.109, unweighted 0.022 (two folds below 0), weighted better on 9/9 | MET-15 |

EARLIER CLAIMS RE-CHECKED (not changed today, rechecked because they are cheap)

| # | Claim | Source | Result | Evidence | Rule |
|---|---|---|---|---|---|
| E1 | Table 1.1 counts: bands 5,742 to 16,189, youngest 5,742, oldest 6,547; 4,624 with a claim | notes "Source" | holds | agecat 5,742 / 12,875 / 15,767 / 16,189 / 10,736 / 6,547; 4,624 claims | PROV-4 |
| E2 | no cost below 200; 705 of 4,333 single-claim at 200.00 (695 exact); two-claim start at 400 (10 at 400.00, 1 at 400.01); no multi-claim at 200 x k beyond those | notes "Anomaly" | holds | 705 / 695 / 4,333; 271 two-claim, min 400.0, 10 and 1; multi-claim at 200k: 10 (the 400.00 ones, consistent) | - |
| E3 | point masses 353.77 (219), 389.95 (94), 390 (55) | notes | holds | 219, 94, 55 | - |
| E4 | 53 vehicle values of 0 made missing; next lowest 0.18; mostly station wagons, buses, trucks, caravans of the oldest band | notes; task_summary.changes | holds | 53 -> NaN in the shipped data; STNWG 27, BUS 10, TRUCK 8, MCARA 6, MIBUS 1, SEDAN 1; band 4: 41 | CLEAN-10/11 |
| E5 | CASdatasets' unit would make the median car $1,500 | notes | holds | median veh_value 1.5 | - |
| E6 | 707 rows share every column (378 extra), all without a claim; full-year no-claim 1,129 with 152 copies | notes | holds | 707 / 378 / 0 claims; 1,129 / 152 | LEAK-18 |
| E7 | with exposure shuffled among no-claim rows, 120-125 copies remain (20 runs) | notes | holds (range narrow) | my 20 runs: mean 120.5, IQR 117-125, range 98-139 | - |
| E8 | 0.8% of test rows had an exact feature copy in train with exposure a feature | notes | holds | 0.89% on split 0/0 | - |
| E9 | 116 pairs with identical factors sum to 365 days against 102 on average | split note | holds (weakly) | 116 at 365; mean over 330-400 (excluding 365) 104.8, with 362 = 124 and 369 = 132: 365 is no outlier | SPLIT-29 |
| E10 | file order: 12.2% adjacent rows share a day count vs 0.3% permuted; lag-1 claim correlation 0.005 | split note | holds | 12.17% vs 0.30%; 0.0053 | SPLIT-8 |
| E11 | "exposure spread evenly over 1-365 days" | split note | REFUTED (wording) | 30-day bins: 6,377, 6,248, 6,261, 6,437, 5,998, 5,533, 5,330, 5,384, 5,165, 4,449, 4,508, 4,242 (then 1,924 for days 360-365): the counts fall by a third from the first months to the last. That is still consistent with one observation period of about a year (policies ending inside it or cut by claims), so the conclusion stands | SPLIT-8 (Should-level accuracy) |
| E12 | splits: random, 3 x 3, disjoint | task_summary.split | holds | 9 splits, train 45,237-45,238, test 22,618-22,619, no overlap | SPLIT-8 |
| E13 | record, 2026-10-30 assessment: exposure is "a feature ... since the contracted period is known when the policy is priced"; the 2026-10-30 body paragraph says the target is `claimcst0` and lists exposure among the features; the 2026-11-01 assessment says exposure "stays as a feature under LEAK-11" | curation/records/...md | REFUTED (stale) | exposure is realized and cut short by write-offs (E: 0.37 vs 0.65); the shipped definition has neither. The CC of 2026-11-06 supersedes them, but no AI assessment marks the old text, as the 2026-11-02 assessment did for "book not read" | PROV-16, record hygiene |
| E14 | book sections 7.3-7.6, 10.4, 8.3, 10.5; Ye et al. 2022 details; area = residence | notes; metric reason | untested | settled by the earlier claim audit and Andrej's reading of the printed pages (2026-11-02); today's change does not touch them | PROV-16 |

IMPLIED CLAIMS (nobody wrote them; the definition implies them)

- Every feature is known at the prediction point: holds. Vehicle value, body, vehicle age band, gender, area and driver
  age band are rating factors known at the quote. One weak channel: the 53 missing vehicle values have a mean exposure
  of 0.686, against 0.468 for the rest. Probe 22 finds no mediated gain above noise, so nothing to do (LEAK-41, USE-6).
- The split is the one the use case needs: the definition says it is not (it is forced, SPLIT-8, settled 2026-11-02).
  Nothing new.
- The target is the real-world target: holds. The pure premium per year insured, weighted by earned exposure, is the
  actuary's breakeven quantity (MET-14/15). The cost's construction stays undocumented and fit_reason says so.
- No row is a copy across the split: as stated (E6, E8, #17). Rating-cell copies of distinct policies, no outcome
  copies. Holds.
- Training is weighted: the definition declares the weight correctly, but only the harness can honour it. Without the
  weight a Tweedie GLM scores 0.022 instead of 0.109, 9/9 worse. This is not a refutation of the dataset. It is the
  largest lever on benchmark results and should stay visible to whoever runs TabArena on format-2 containers
  (MET-15, Must).

REFUTED AND UNTESTED, RANKED (principles.md: validity first, Must first)

1. (Value / reporting, TP-2) REVIEW Outcome: "every model family probed beats the weighted constant on 9 of 9 splits".
   Refuted. The task probe's untuned random forest beats it on 7 of 9 in my re-run (mean 0.031). The probe itself
   reports RF 0.026 and LightGBM 0.037 and raises `no_signal` (its skill is weighted MSE, best R^2 0.0002), and REVIEW
   does not mention that. Changes: nothing in the data; the "Value" line overstates. Mildest remedy: write "each of the
   three families fitted with the weight (Tweedie GLM 0.120, Tweedie LightGBM 0.059, L2 LightGBM 0.060) beats it on 9
   of 9". Add one line for the probe's `no_signal`: it is MSE-based under a Gini metric, a forest_fires-type flag, and
   the tuned and fitted families answer it.
2. (Record hygiene, PROV-16 Should) The record's 2026-10-30 assessment and body paragraph, and the 2026-11-01
   assessment, still say exposure is a feature, known at pricing or kept under LEAK-11, and that the target is
   `claimcst0`. They are superseded by the CC of 2026-11-06, but nothing marks them. Mildest remedy: one "Assessment
   (AI, 2026-11-06)" line: "supersedes the target and exposure statements of 2026-10-30 and 2026-11-01 above".
3. (Accuracy, split note) "exposure spread evenly over 1-365 days". The counts per 30 days fall from about 6,400 to
   about 4,250. Mildest remedy: "spread over 1-365 days (about 6,300 a month at the short end, 4,300 at the long end)".
   The conclusion (one period of about a year) is unaffected.
4. Untested: the exact wording of CAS Monograph 5 Sec. 7.2.4. The PDF did not render here. The section title and the
   construction are confirmed from the contents and CAS presentations. Remedy: none needed, unless the citation should
   name the edition (2019 printing; the 2025 second edition may renumber it).
5. Minor numbers that hold only approximately, with no remedy needed:
   - excess claims 145 against 147;
   - log-exposure coefficient 0.28-0.29 against 0.29-0.31;
   - shuffled copies: the stated "120-125" is the interquartile range, the full range is 98-139.
6. Framework nit, as known: the bundle's conflicting-duplicates INFO (61 rows) counts exposure as a feature. On the six
   real features 7,512 rows share their factors with a row of another target. Remedy: the fix in progress.

Sources:
- https://www.casact.org/monograph/cas-monograph-no-5
- https://www.casact.org/sites/default/files/presentation/rpm_2014_handouts_paper_3048_handout_1892_0.pdf
- https://rdrr.io/cran/actuaRE/man/dataCar.html
- https://dutangc.github.io/CASdatasets/reference/ausprivauto.html

</details>

<details><summary>Column audit</summary>

**COLUMN AUDIT (column-auditor, 2026-11-06, exposure re-review, full tier): australian_vehicle_insurance_2004_2005**

Verdict: ship as defined. Under the new rules no column is a leak. `exposure` is out of the features. It appears only
as the weight scoring column, the metric's weight input and the task's sample_weight: feature_columns(c) gives the six
rating factors, and the probe frame lists exposure as a scoring column only. The six features are all known when the
policy is priced. Probe 22 finds that the features predict the weight (R^2 0.074). That prediction does not go
through the outcome: it is just as strong on the no-claim rows (R^2 0.080), so it rests on a cohort fixed at the start
and the features stay (LEAK-41 by timing, USE-6). One open quality point remains (P7, CLEAN-14): both age bands ship as
int64. It is a question for the curator, not something today's change caused.

Prediction point used: when the policy is priced at underwriting ("for example"), from the first curation_comments
bullet. Frame: dataset_io.from_definition and to_container(), with the definition as shipped. Size:
67,856 rows x 8 columns, IID, 3 x 3 splits. Dtype probe: 0 of 6 columns flagged. The codebook matched 0 columns because
of the renames, so I checked each column by hand against the insuranceData Rd and the CASdatasets Rd.

COLUMN TABLE

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| claim_cost_per_year (target) | claimcst0 ("claim amount (0 if no claim)", insuranceData; "the sum of claim payments", CAS) / exposure, in dollars per year observed | outcome | float64, identity scale; 0 on 63,232 rows; max 5,238,879 (one claim of 14,343 on 1 day); claimcst0 is checked back to the cent in _clean; weighted mean 292.90 vs unweighted 755.26, both stated in the notes | fine | MET-14, CLEAN-16 (amended: a Gini-scored rate keeps the curator's scale; the notes say what a weighted fit estimates: holds) |
| exposure (weight scoring column, sample_weight) | insuranceData "0-1"; CAS "the number of policy years"; whole days / 365.25, 1 to 365 days, 383 distinct values, median 0.446, 1.90% full years, no 0, no 366 | no (realized at the end of the observation period; some claims cut it short) | float64; never a feature (not in feature_columns; scoring column role=weight; sample_weight = "exposure"); no rows dropped or selected by it | fine as the weight (it was the leak of 2026-11-02, now resolved) | LEAK-41, MET-14, MET-15, USE-7 |
| vehicle_value | "vehicle value, in $10,000s" (insuranceData; CAS's "thousand of AUD" is an error of that copy) | yes (the value insured at the start) | float64; 53 zeros made missing (next lowest 0.18); range 0.18 to 34.56; 1,004 band-1 values ending in $990/$490 (list prices) | fine; predicts the weight through a start-date cohort (below), not through the outcome | CLEAN-10, CLEAN-11; LEAK-41 by timing, USE-6 |
| vehicle_body | 13 body codes with CAS's labels (one to one on every row) | yes | unordered category, 13 levels (27 roadsters to 22,233 sedans) | fine | CLEAN-12, CLEAN-14 |
| vehicle_age_band | "1 (youngest), 2, 3, 4" (insuranceData); CAS: "The vehicle age group", with levels "youngest cars" to "oldest cars" per the 2026-11-01 audit; limits not published | yes | int64 1-4; the median value falls 2.30 to 0.80 across the bands, as an age order would | question: a band of a quantity, so an ordered category under CLEAN-14 as amended 2026-11-01? (problem 1) | CLEAN-14 |
| driver_age_band | "1 (youngest) ... 6" (insuranceData); Table 1.1 "Driver's age category"; CAS "The age of the policyholder"; limits not published | yes | int64 1-6; counts match Table 1.1; claims per year fall from 0.190 to 0.118 | question, as above (problem 1) | CLEAN-14 |
| gender | "a factor with levels F M" (insuranceData); "the gender of the policyholder" (CAS) | yes | unordered category F/M (38,603 / 29,253) | fine | CLEAN-14 |
| area | "a factor with levels A-F" (insuranceData); residence, A-F unexplained (book Table 1.6); absent from CAS | yes | unordered category, 6 levels; claims per year are not monotone in the letter (A 0.143, B 0.153, C 0.147, D 0.130, E 0.139, F 0.161), and no source gives an order, unlike fremtpl2's documented density bands | fine | CLEAN-14 |
| clm, numclaims (dropped) | the claim indicator and the claim count | no (outcome) | dropped; asserted to be > 0 exactly where claimcst0 > 0 | correct drop | LEAK-10 |
| claimcst0 (dropped) | the claim cost | no | the target's numerator; dropped after the rate is built | correct drop | LEAK-10 |
| X_OBSTAT_ (dropped) | constant | n/a | dropped | correct drop | CLEAN-5 |

THE WEIGHT AND THE FEATURES THAT PREDICT IT (LEAK-41, probe 22)

Values of exposure: every value is a whole day count (days*365.25 is an integer to 1e-6), from 1 to 365 days. 1.90%
are full years. The mean is 0.436 in vehicle age band 1 and 0.475-0.478 in bands 2-4. By body type the mean runs from
0.40 (convertible, coupe) to 0.54 (panel van, bus), and full years are 13.6% for panel vans and 6.3% for trucks,
against 1.3-2.2% for the common bodies (the fleet cohort the notes describe). Gender, area and driver age band move the
mean by at most 0.03.

Probe 22 (probe22.txt, identical to probe22_l2.txt): the features predict exposure at R^2 0.074 (Spearman
0.27), with vehicle_value carrying 70% of the gain. The weight as a feature adds +0.098 (SD 0.03) to an honest fit of
0.052. 1/weight alone scores 0.2055. No feature's weight-mediated gain rises above noise. The probe has little power,
though: its SDs (0.019-0.039) are about the size of the honest fit itself. So I tested the path the timing call turns
on directly (vv_exposure.out, shipped splits, repeat 0):

- Where the features learn the weight from. All six: R^2 0.081 (Spearman 0.277). Vehicle value alone: 0.027. All but
  vehicle value: -0.001. All six with the value rounded to $1,000: 0.031. A lookup of each exact value's mean exposure
  in train gives Spearman 0.19. So the signal is the exact vehicle value combined with the other factors: it picks out
  cohorts of near-identical vehicles that started on the same date. Exact (value, day count) pairs repeat on 20,146
  rows, against 18,272 with the day counts shuffled.
- Whether the outcome is in that path. Fitted and scored on the no-claim rows only, where no claim can have cut the
  exposure, the features predict it just as well: R^2 0.080, Spearman 0.274. The proxy therefore carries the start
  date's window, fixed when the policy starts, not the part a claim cuts. Spearman of the value with the exposure:
  0.002 on no-claim rows, 0.066 on claim rows.
- Timing. vehicle_value is the value insured at inception. The cohorts it marks (fleets, same-date entries) exist
  before any claim. LEAK-41 by timing and USE-6 keep it. The window part also carries no claim rate per year in
  itself (the claim rate's excess at short exposures is the cut, which this path does not see), which fits probe 22's
  null mediated gains.

The rest of LEAK-41 holds:
- No column encodes the weight: no earned premium, no sum of exposures, no precision mark. Exposure's own precision is
  whole days on every row, so it carries no correction flag.
- No row is trained or scored by a selection on the weight. Every exposure is at least one day, so USE-7 removes
  nothing.
- 1/weight alone is stated in the notes and the metric reason (0.205).
- The definition reports the L2 and the weighted actuarial gains of `exposure` itself: L2 LightGBM +0.099, Tweedie
  LightGBM +0.089, Tweedie GLM +0.116, 9 of 9 each. Probe 22 names no other suspect column.

PROBLEMS, RANKED (principles.md)

No P1-P6 problem at column level.

1. P7, CLEAN-14 (Should): both age bands ship as int64. This is a question for the curator, not raised by today's
   change.
   - Evidence: the amendment of 2026-11-01 makes "bands of a quantity ('21-25', '1-10%', '3 or more') ... ordered
     categories with the band labels, decoded where the file stores a band's number". open_university_learning_
     analytics_dataset ships age_band that way.
   - This definition says "the age bands ... stay numbers, the order of an age". The mediator of 2026-11-01 read that
     as following CLEAN-14. No curator call is recorded, and the ordinal and dtype sweeps of 2026-10-30 (run before this
     dataset was added) do not cover it.
   - The case for the number: the same amendment's test ("does the source say in words what each level is?")
     reads insuranceData's "1 (youngest), 2, 3, 4" as words at one end only, which points to a number.
   - The case for the ordered category: CAS's level names ("youngest cars" ... "oldest cars", "young people" ...
     "oldest people") name every level, and the column is a band of an age.
   - Effect: none for tree models. For a linear model, a number spaces the bands equally, though their limits are
     unknown. Claims per year by driver band: 0.190, 0.158, 0.150, 0.145, 0.119, 0.118. Cost per year: 500, 337, 288,
     282, 205, 221 (not monotone at the end).
   - Mildest remedy: the curator decides. Either FeatureTypes(ordinal={"vehicle_age_band": [1, 2, 3, 4],
     "driver_age_band": [1, ..., 6]}), the codes kept as levels because the limits are unknown, or a note that the
     bands stay numbers under the "words at one end" branch. Rows, split and metric are unchanged either way.

2. P7, CLEAN-1 (optional, carried over): the mediator's item 11 (round the claim costs to cents) is still not applied.
   The notes keep "695 exactly, the rest float noise". Now that the target is cost / exposure, rounding claimcst0
   before dividing changes the rate by at most $0.005 / exposure. Harmless, so I do not ask for it.

Tested and not a problem: the scoring column's description matches the data (1 to 365 days, realized, cut short by
some claims). The weighted and unweighted portfolio means quoted in the notes (292.90, 755.26) reproduce. The shares of
rows sharing all six rating factors reproduce (51.5%, 34,974 rows): coarse rating cells, LEAK-18, settled. The
framework nit that bundle duplicate checks count the weight as a feature is known and does not touch the frame.

Judgment record
Verdict: ship as defined.
Validity: LEAK-41 holds. exposure is the weight scoring column and sample_weight, never a feature. The features
  predict it at R^2 0.074-0.081, equally on no-claim rows (0.080), through exact vehicle-value cohorts fixed at the
  start; they stay by timing (USE-6). clm, numclaims and claimcst0 are correctly dropped (LEAK-10). No other column
  holds a value from after the outcome.
Quality: CLEAN-10/11 hold (53 vehicle values of 0 made missing); CLEAN-16 as amended holds. CLEAN-14: the age bands as
  int64 against the 2026-11-01 "bands of a quantity" clause is a question for the curator.
For the curator: the age bands, ordered category or number (problem 1).

</details>

<details><summary>Split audit</summary>

**SPLIT AUDITOR - australian_vehicle_insurance_2004_2005 (exposure re-review, 2026-11-06, full tier)**

VERDICT: right with notes. The forced IID split (ForcedIIDFromTemporal, SPLIT-8, settled 2026-11-02, issue 1) still
holds under D8. Nothing in the split needs to change. The notes only need their split numbers re-measured on the new
target, and one sentence on the window edges.

Evidence: split_audit.py and its outputs split_audit.txt and split_audit.csv (run folder).
Every fit is weighted by `exposure`. The models are a Tweedie 1.5 LightGBM (lr 0.05, 15 leaves, min leaf 100, 300 rounds)
and a Tweedie 1.5 log-link GLM (one-hot factors, quadratic in log vehicle value). Every score is the weighted normalized
Gini. My implementation matches the container's scorer on split 0 (0.101931 for both).

1. REGIME (P4, SPLIT-8, USE): unchanged and right as forced.
   The use case prices next year's one-year policies from past policy-years, so it is temporal. The release has no
   dates and no policy ids, and covers one observation period, so no valid window exists. SPLIT-8 ships it IID with
   the forced tag. D8 changes the target and the weight. It does not change the regime.

2. THE SHIPPED SPLITS ARE BALANCED (3 repeats x 3 folds, 45,237-45,238 train / 22,618-22,619 test, disjoint, covering
   all rows).
   - Mean exposure per test fold is 0.4648-0.4708 (train 0.4676-0.4706). KS p for train against test exposure is
     0.095-0.994.
   - The weighted rate per test fold is 269.9-325.7 dollars a year, and the claim share is 0.0672-0.0690.
   - Each test fold holds 1-4 of the 7 rows at 1M dollars a year or more.
   - The honest scores are noisy per fold: LightGBM 0.059 (SD 0.021, 0.023-0.087), GLM 0.120 (SD 0.023, 0.096-0.153).
     Model gaps under about 0.02 are not separable on single folds. They need the paired 9-split comparison.

3. TIME ON RISK CUT AT THE EXTRACT WINDOW'S EDGES (SPLIT-9, LEAK-41; the french_fleet check in the brief)
   - `exposure` is cut at both edges of the one extract window (the window start for policies begun earlier, the
     window end for policies still running) and by some claims.
   - In this IID split the train and test sides come from the same window. No cutoff inside the data admits or
     excludes a training row by its time on risk, and the weight distributions match (item 2). So the temporal failure
     the brief names cannot occur here: later windows that admit only early-ended periods
     (pricing_game_2016_french_fleet).
   - The edge cut stays a property of the target, the part-year rate of whichever months fell inside the window. It is
     the same on both sides, so it is not a split defect.
   - Note (Could, text): if a dated release ever allows the temporal split SPLIT-8 asks to recover, each window's cutoff
     cuts the exposure again, and the train side must be checked for periods ended by the cutoff (SPLIT-9, LEAK-41).
     The split bullet could say so in one clause.

4. HIDDEN GROUPS AND COPIES OF RATING PROFILES ACROSS THE SPLIT (SPLIT-29, SPLIT-24, LEAK-18): no leak.
   - Without exposure, 34,974 rows (51.5%) share their six rating factors with another policy (45,220 distinct
     cells). 42.1-43.3% of test rows have an exact copy in train. These are coarse tariff cells of distinct policies,
     which next year's policies also fall into.
   - The leak probe: among test rows with a copy, 34.6% match only same-label copies and 4.2% only other-label copies.
     1-NN R^2 is -1.2, so a lookup does not pay.
   - Alternative 1, grouping by the rating cell (a stress test, harsher than the use case since new policies do not
     form new cells), 9 splits: LightGBM 0.054 (SD 0.031) against 0.059 shipped; GLM 0.119 (SD 0.026) against 0.120.
     No drop beyond fold noise.
   - Alternative 2, grouping by the full row with exposure (the fleet-cohort proxy: 67,417 groups, 812 rows in groups
     of two or more, all without a claim), 9 splits: LightGBM 0.077 (SD 0.025), GLM 0.127 (SD 0.016). Not lower than
     shipped. The difference is fold noise (unpaired partitions).
   - Neither key is a true group id, and SPLIT-24 bars shipping on them. They were run only to bound the optimism, and
     it is nil. No policy is visibly split into two rows (116 pairs of profiles summing to 365 days against 102 for
     other sums, settled).

5. ORDER DEPENDENCE ON THE NEW TARGET (SPLIT-22, SPLIT-8 leak test). The old numbers were on the cost target; this
   re-measure uses the rate target.
   - I rebuilt the frame in raw file order with the definition's own `_clean`, trained on the first 1-3 quarters of
     the file and tested on the next quarter. Results: LightGBM 0.096, 0.046, 0.093 (mean 0.078); GLM 0.168, 0.084,
     0.132 (mean 0.128). Random splits of the same sizes (3 seeds each): LightGBM mean 0.060, GLM mean 0.111.
   - No drop when holding out later file blocks, so no order-borne leak is hidden by the random split.
   - The file order is not neutral, though:
     - Mean exposure per tenth of the file is 0.484, 0.468, 0.458, 0.459, 0.421, 0.428, 0.446, 0.497, 0.529, 0.496.
       Chance SD is about 0.0035, so the U shape is far beyond chance. It would fit an order by policy start date
       across the window edges, but that is not established.
     - The weighted rate per tenth is 247-349 dollars a year, and the claim share 0.061-0.073.
   - Whether the order is time stays unknown (settled point). Shipping the order as time is not supported (SPLIT-24
     spirit, inferred key). This only refines the note.

PROBLEMS, ranked by principles.md
 a) (Should, P4/EV, text only) The split bullet and REVIEW issue 1 still give the file-order and grouped-split numbers
    "on the earlier cost target" (0.168/0.189/0.208 against 0.127/0.174/0.181; 0.194 against 0.182).
    Mildest remedy: add today's numbers on the rate target with the weight: file order LightGBM 0.078 against 0.060
    random, GLM 0.128 against 0.111; grouped by rating cell 0.054/0.119 against shipped 0.059/0.120; grouped by full
    row 0.077/0.127. The conclusion is unchanged.
 b) (Could, text) Add one clause to the split bullet that the exposure is cut at the extract window's edges as well as
    by claims, and that the IID sides share the one window. Also note that a future temporal split must re-check the
    cutoff cut (SPLIT-9, LEAK-41).
 c) (Could, note) Record the exposure drift along the raw file order (0.42-0.53 per tenth) next to the 12.2%
    adjacent-day-count fact, as more evidence that the order is structured, possibly by start date.
No re-split, gap or filter is called for.

</details>

<details><summary>Domain practitioner</summary>

**australian_vehicle_insurance_2004_2005 -- domain practitioner (pricing actuary, Australian private motor), exposure re-review 2026-11-06, full tier**

VERDICT
Fit: approximate, as declared. Real one-year policies with the rating factors and claim costs of a tariff, now priced
in the unit I price (claim cost per year insured, exposure as weight); what remains short of my decision is the forced
random split of undated policies and the undocumented label (paid or incurred, the $200 floor, the cover), not the
exposure any more (USE-8, USE-5).
Metric: yes for selecting the segmentation of a tariff, partly for the whole pricing decision. The exposure-weighted
normalized Gini of the cost per year is the CAS Monograph 5 Gini I would read; it ignores the level and the spread of
the relativities, which I set and check with a deviance or actual-over-expected by segment. I would keep it for this
table (resolution, below) and say in the reason what it does not score.

What is new against the earlier practitioner block (REVIEW.md, "Domain practitioner"): every recommendation of that
block on the formulation is now adopted (rate target, exposure as metric weight and sample weight, never a feature).
Its two reasons for not proposing an exposure-weighted Tweedie deviance are gone too (the leak, and no training
weight); I re-measured that alternative below and still prefer the Gini for this table.

1. INPUTS AT THE QUOTE (USE-3, USE-6, LEAK-41)
- Vehicle value, body, vehicle age band, driver age band, gender, area: all on the proposal form. I have them.
- exposure: correctly gone from the inputs. At the quote the term is one year for every policy; the shipped column is
  the part of that year the extract observed, cut short by some total losses (an Australian comprehensive policy ends
  on a total-loss settlement with no refund). It is known in my training data as earned exposure, which is exactly how
  I use it: as weight (CAS Monograph 5, Sec. 2, exposure offsets/weights). LEAK-41 and MET-15 match practice.
- Missing inputs I would always have (settled earlier, unchanged): no-claim bonus / rating level, postcode or garaging
  address, make and model, exact age and licence years, excess, cover type and use, new business or renewal. This is a
  thin new-business tariff: it changes the difficulty, not the decision.
- Probe 22 confirms no rating factor's gain travels through exposure above noise (R^2 0.074 for exposure from the
  factors, mostly vehicle value). That is risk selection, which I would want the model to keep (USE-6).

2. THE TARGET (USE-5, MET-14, MET-15)
- I act on a number: the expected claim cost of one policy-year, the pure premium, before expenses and loadings.
  claim_cost_per_year = claimcst0 / exposure, fitted and scored with weight exposure, estimates
  E[cost | x] / E[exposure | x], the pure premium that breaks even (portfolio 292.90 dollars a year against 755.26 for
  an unweighted mean of the ratio). This is the form of CAS Monograph 5 Sec. 2.7.3 and of actuaRE's copy of this
  table. Direct quantity, no longer a proxy.
- The cut-short exposures bias the rate level only negligibly: even if every claim of at least 80% of the vehicle
  value (199 policies in my count, 193 in the notes, which exclude the vehicle values of 0) had run to a full year, the lost exposure would be at most 111.8 of
  31,800.8 policy-years (0.35%). The leak was in using exposure as an input, not in the denominator.
- The 7 rows at 1M dollars a year or more: right to keep. Their costs (8.6k to 25.6k) are ordinary claims, not large
  losses I would cap; they are large only per day observed, and the weight makes each count by its cost (1.26% of the
  claim cost). I would cap claim amounts at a large-loss threshold, never rates; none of these is a large loss.
- Unverifiable label construction (paid or incurred, evaluation date, the $200 floor with 705 single claims at 200.00,
  the point masses at 353.77 and 389.95): unchanged, the reason the fit stays approximate.

3. ONE ROW, ONE DECISION; THE TEST DATA (USE-8, USE-10, SPLIT-8)
- One row is one policy's observed part-year; with the rate and the weight it is one policy's annual premium, each
  counting by its time on risk. That matches the decision now (the earlier gap 2, "unit of the metric", is closed).
- No ids, no history: cold-start new-business pricing (USE-10), legitimate.
- Test data: random policies of the same book. I would price next year's book (out-of-time, CAS Monograph 5 Sec.
  4.3.1 prefers it); the release has no dates, so ForcedIIDFromTemporal and the approximate fit are right. Settled;
  today's change does not reopen it.

4. WOULD I USE IT?
- As a benchmark for fitting a thin new-business tariff: yes, now more readily than before. The scores look like
  pricing experience: an honest Tweedie GLM 0.120 weighted Gini, honest LightGBMs 0.059-0.060, the weighted constant 0
  (9 of 9 splits each, paired SE about 0.007). A GLM beating untuned boosting on six coarse factors is what I would
  expect. The old 0.18-0.21 levels were inflated by exposure; the new levels are believable for six coarse factors.
- What makes me trust it: two independent copies agree row by row; the leak is measured out (with exposure as a
  feature +0.089 to +0.116 on 9 of 9; 1/exposure alone 0.205, above every honest model) and now removed.
- What makes me distrust a score: the signal is small and the Gini does not see calibration. My check on the 9
  shipped splits (dev_check.py and dev_check.txt in the run folder; floor 1 dollar a year):

  ```text
  model                         weighted Gini   weighted Tweedie dev p=1.5   better than constant (dev 1.5)
  constant (weighted mean)      0.000           105.48                         -
  Tweedie GLM                   0.120           104.94                       8 of 9 (+0.54, SE 0.20)
  GLM, log-relativities x 0.5   0.120           104.74                       9 of 9 (+0.73, SE 0.10)
  GLM, log-relativities x 2     0.120           108.39                       0 of 9 (-2.91, SE 0.53)
  GLM x 1.3 (level 30% high)    0.120           105.92                       2 of 9
  Tweedie LightGBM              0.059           110.48                       0 of 9 (-5.00, SE 0.65)
  L2 LightGBM (identity)        0.060           126.83                       0 of 9 (1.4% of predictions at floor)
  ```
  (p = 1.7 gives the same orders.)

  So a tariff whose relativities are twice too steep, or whose level is 30% too high, scores the same Gini as the GLM
  and would misprice the book; the untuned LightGBMs order the risks a little (Gini 0.06) but their relativities are
  too extreme to beat a flat rate on the deviance. Shrinking the GLM's relativities by half improves its deviance:
  the signal is credibility-thin, and only a weak spread is supported.

5. THE METRIC (MET-1, MET-2, MET-8, MET-10, MET-11, MET-14, MET-15)
- Declared: normalized_weighted_gini on the rate, weight exposure: rows sorted by predicted cost per year, x the
  cumulative exposure, y the cumulative claim cost, normalised by the perfect order. That is the CAS Monograph 5 Sec.
  7.2.4 Gini at the unit I act on (the policy-year). MET-2 holds: the weight ships as a scoring column only and is never
  a feature; MET-15 holds: the sample weight is the metric's row weight. The origin `context` is right (MET-11:
  the book selects by AIC in-sample, Ye et al. 2022 report five measures, no unique original, MET-5).
- Do I pick a pricing model by it? I pick the segmentation by a Gini or lift (double lift, quantile plots) and the
  level and the spread by a deviance or by actual over expected per segment. So it scores my ordering decision, not
  the premium itself: partly.
- What I would choose in principle (MET-8): an exposure-weighted Tweedie deviance on the rate (MET-14's convention,
  a required min_prediction floor under MET-13), a proper score that sees level and spread. On this table I would not
  switch to it: its resolution is poor (the best honest model gains 0.5% of the constant's deviance, SE 0.2, 8 of 9
  splits), the choice of power and floor changes the scale, and the Gini separates the honest models cleanly (GLM minus
  LightGBM +0.061, SE 0.007, 9 of 9). The collection already scores the frequency side by weighted Poisson deviance
  (fremtpl2, bemtpl97), so the Gini here adds diversity (MET-10). The curator's rejection of claim frequency (drops the
  claim size I price) I agree with.
- Answer: yes for the ordering, partly overall; keep normalized_weighted_gini; I would not use a different metric
  for this table.

GAPS BETWEEN THE DATASET AND MY DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. The forced random split of undated policies stands in for next year's book (SPLIT-8, USE-8). Unchanged, settled.
2. The metric scores the order of the risks, not the level or the spread of the relativities (MET-1, MET-8): a tariff
   twice too steep scores the same 0.120 as the fitted GLM. New to state; it should be in the reason.
3. The label's construction is undocumented (paid or incurred, the $200 floor, the point masses, the cover) (USE-5).
4. Thin rating factors (no NCD, postcode, make and model, excess, cover): harder task, same decision.
5. The realized exposure is cut short by about 200 total losses: as a denominator it biases the rate level by at most
   0.35% (now negligible; it was the largest gap while exposure was a feature).

WHAT AN EXPERT WOULD CHANGE (recommendations; the curator decides)
- Metric reason (MET-11): next to "The Gini ignores the price level, which pricing sets separately", add that it also
  ignores the spread of the relativities (any monotone transform of the predictions scores the same), and give the
  numbers: on the shipped splits a GLM with log-relativities doubled keeps Gini 0.120 while its exposure-weighted
  Tweedie deviance (p 1.5) is worse than the weighted constant on 9 of 9 splits; the untuned Tweedie LightGBM (Gini
  0.059) is worse than the constant on that deviance on 9 of 9. Say why the deviance was not chosen (resolution: best
  honest gain 0.5% of the constant's deviance, SE 0.2).
- Optional: a sentence in the dataset's notes for benchmark users that the signal is thin (honest GLM 0.120,
  shrinking its relativities by half improves its deviance), so heavy regularisation is expected to win.
- Nothing to change in the inputs, the target, the weight, the 7 high-rate rows or the split. `known`, `predicted` and
  `changes` read correctly for an actuary. fit_reason correctly no longer names exposure as a gap (USE-8: the
  rate-plus-weight form is the standard actuarial formulation, not a large change made to avoid the leak).

SOURCES
- dataset.py, README.md, REVIEW.md (issue 6 and the earlier practitioner block) in the dataset's folder.
- The run's CHANGES.md, task probe, probe 22 and re-measure.
- My check: dev_check.py and dev_check.txt in the run folder.
- de Jong and Heller (2008), Generalized Linear Models for Insurance Data (Sec. 7.3-7.6, 10.4; as read by the curator).
- CAS Monograph 5, Goldburd, Khare, Tevet et al., GLMs for Insurance Rating (Sec. 2 exposure weights and offsets,
  2.7.3 pure premium by Tweedie, 4.3.1 out-of-time holdout, 7.2.4 Gini on loss cost per exposure).
- actuaRE 0.1.5 dataCar (Y = claimcst0 / exposure, weight exposure).
- Ye et al. (2022), Econometrics 10(2):19 (Gini among five measures on this table).
- Frees, Meyers and Cummings (2011), JASA 106:1085-1098 (ordered Lorenz / Gini for insurance scores).
- No new web fetches this pass; the Australian total-loss practice (policy ends, no refund) is carried over from the
  earlier block (NRMA FAQ via a search summary).
Rules cited: USE-3, USE-5, USE-6, USE-8, USE-10; MET-1, MET-2, MET-5, MET-8, MET-10, MET-11, MET-13, MET-14, MET-15;
LEAK-41; SPLIT-8.

</details>

<details><summary>Blind review</summary>

**BLIND REVIEW: australian_vehicle_insurance_2004_2005 (dataCar / ausprivauto0405, de Jong & Heller 2008)**

VERDICT: Exclude as prepared. The exposure weighting is actuarially correct, but the six rating factors barely beat a constant, and the weighted score is driven by a handful of tiny-exposure claims. Method rankings would mostly reflect noise.

TASK
A motor insurer prices one-year private auto policies (2004-05, Australia). The pricing actuary predicts expected claim cost per policy-year (pure premium) from the rating factors at quote time. This is a real and standard use. The target is claimcst0 / exposure; I confirmed this because claim_cost_per_year * exposure gives back amounts with min 200, median 762 and max 55,922 over 4,624 claims, matching the source ("4,624 had at least one claim"). Zero target in 93.2% of rows.

TRAINING WEIGHT: is exposure right? Yes, in principle. For a rate target Y = cost/exposure, weighting by exposure is the textbook Tweedie/Poisson pure-premium setup: the weighted mean (292.9) equals total cost / total exposure, while the unweighted mean (755) is inflated by short-exposure claims. Weighting the test score by exposure is also the right idea. The problem is the loss it is combined with (concern 2).

CONCERNS (most to least serious)
1. Almost no learnable signal, so the task cannot separate methods.
   Evidence: LightGBM fitted with exposure weights, 3x3 random splits.
   - Exposure-weighted RMSE: model 5262 vs constant 5261. Model 3395 vs 3394. Every split shows the model equal to or slightly worse than the constant.
   - Weighted Tweedie(1.5) deviance: model 105.8-113.4 vs constant 102.1-108.0. A conservative model gets 105.78 vs 105.41. The model is never better.
   - Claim frequency, Poisson with exposure: deviance 0.7473 vs 0.7485.
   - Claim AUC: 0.658 from model rate times exposure vs 0.653 from exposure alone.
   - Gini of predicted pure premium: 0.06-0.11.
   The features are 6 coarse rating factors (value, body, vehicle age band, gender, area, driver age band). That matches the textbook, where these effects are significant but small.
   Change: drop it. If an insurance task is wanted, use a larger set with real signal (for example freMTPL2: 678k rows with more covariates).
2. The metric is dominated by a few rows.
   Evidence:
   - With weight w=exposure, the squared error per row is (cost - p*exposure)^2 / exposure, which explodes when exposure is small.
   - Minimum exposure is 0.0027 (one day). 817 rows have exposure < 0.01.
   - The top target is 5.24M (a 14,343 claim divided by 0.0027). The next targets are 3.14M, 2.98M and 2.52M.
   - The top 10 rows hold 56% of the total weighted SSE and the top 100 hold 87%.
   - Test-fold wRMSE swings from 3394 to 5393 depending on which fold the 5.2M row falls into.
   Change: if kept, score with exposure-weighted Tweedie or Poisson deviance (or a Gini/normalised-Gini), not weighted RMSE/R2. Optionally drop policies with exposure under about 0.05 (4,018 rows), or cap the target. I could not see which metric the benchmark applies; task.md says only that the score is exposure-weighted.
3. Target heavy-tailed and zero-inflated (93.2% zeros, q99 = 7,469, max = 5.24M). Models trained with squared-error objectives will do badly by construction, so the benchmark would partly test the choice of loss rather than the learner. Combined with concern 1, this makes the results noise.
4. Minor preparation points. All look fine.
   - vehicle_value has 53 NaN. These are the 53 zero values in the source, recoded as missing, which is reasonable.
   - Units are $10,000s per insuranceData. CASdatasets says "thousands of AUD", which is a documentation inconsistency only.
   - The age bands are kept as ordinal ints and body/gender/area as categoricals, which is sensible.
   - Leaked columns from the source (clm, numclaims) and X_OBSTAT_ (constant) were correctly removed.
   - Area is coded A-F with no documented meaning.
5. Duplicates and split. 378 fully duplicated rows and 439 duplicated feature rows. These are expected from 6 coarse features plus zero targets and are not a leak. There is no date or policy ID, so a random IID split is the only option. Policies from 2004 and 2005 cannot be separated, so a temporal pricing split cannot be checked.

DATA AUTHENTICITY: Real, widely used textbook data. Row count (67,856), body classes (13), bands and claim count all match the source. The 200 minimum claim (703 claims at exactly 200) is plausible as a reporting floor or excess.

COULD NOT CHECK: the exact benchmark metric; whether 2004 and 2005 policies overlap (renewals of the same vehicle); the original source website (acst.mq.edu.au, offline); the meaning of the area codes.

</details>

<details><summary>Task gamer</summary>

**TASK GAMER REPORT - australian_vehicle_insurance_2004_2005 (claim_cost_per_year, normalized_weighted_gini, w = exposure)**

Verdict: the features themselves cannot be gamed. The task can only be gamed through the exposure column (the scoring column and training weight). Exposure is cut short by the outcome, so 1/exposure alone scores 0.205, against 0.047 for the honest baseline and 0.089 for the best honest model.

All scores are means over the 9 shipped splits (3 repeats x 3 folds), computed with score.py. Every model was fitted with sample_weight = exposure.
Honest baseline: untuned LGBM (L2) on features(), mean 0.0474, range 0.0057-0.0783.
Better honest model: a regularised LGBM Poisson on claim frequency (claim indicator / exposure, weight exposure), mean 0.0888, range 0.0496-0.1308.
Noise: adding a random column to the baseline gives 0.048 / 0.059 / 0.059 over 3 seeds. Per-split spread is about +-0.04.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Honest frequency prediction divided by exposure | 0.0888 (0.0474 baseline) | 0.2275 (0.188-0.264) | +0.139 over better honest; +0.180 over baseline | No: realised exposure is only known when the policy ends | Keep exposure hidden from the model; ideally define the target per planned term |
| 2 | Exposure as a feature (Poisson frequency) | 0.0888 | 0.2084 (0.163-0.250) | +0.120 | No | same |
| 3 | 1/exposure alone as the prediction (no model) | 0.0474 | 0.2050 (0.171-0.242) | +0.158 over baseline, +0.116 over better honest | No | same |
| 4 | Exposure as a feature (baseline L2 / tweedie LGBM) | 0.0474 / 0.0746 | 0.137 / 0.193 | +0.09 / +0.12 | No | same |
| 5 | 1/exposure as a feature (baseline L2) | 0.0474 | 0.1273 (0.036-0.230) | +0.080 | No | same |

Finding 1-5 (the weight). The target is claim cost divided by exposure, and the metric weights each row by exposure. In dataCar, short exposures are full of claims. The claim share per exposure decile goes 1.7%, 3.0%, 3.4%, 5.0%, 6.3%, 7.6%, 8.9%, 9.8%, 10.7%, 12.1%, so claims per car-year are about 3x higher in the shortest decile. Cost per car-year is 1747 in the shortest decile against 201 in the longest. A policy that ends early after a claim (total loss, cancellation) gets both a short exposure and a large cost/exposure. Ranking by 1/exposure therefore orders the claimants first, and no rating variable carries that information. None of the features proxies exposure: its correlation with vehicle_value is 0.0003 and with row position -0.001, and its mean is flat across categories (0.40-0.54). So the exploit needs the scoring column itself, which task.md says is never a feature.

A model at underwriting knows the planned term (one year), not the realised exposure. Part of the short exposure may come from the observation window (a policy written late in the period) rather than from the outcome. The fact that would settle this is the policy start/end dates, which the published data lack. The 3x frequency gradient says the outcome-driven part dominates.

Mildest fix: make sure the harness never hands exposure to the model (it already sits in scoring.parquet, so the risk is only for participants who read it). Stronger fix: drop rows whose exposure is very short (for example < 0.1) from scoring, or score total claim cost per planned year. Because exposure is outcome-cut, even the metric's denominator carries outcome information.

Flaws that hurt an honest model: none found that the task should fix.
- Training only on near-full-year rows (exposure > 0.9, "not cut short") made things worse: 0.0383 against 0.0888 for the same Poisson model on all rows.
- The gap between the untuned baseline (0.047) and the Poisson-frequency / regularised tweedie models (0.089 / 0.075) is a modelling choice: the heavy-tailed target (max 5.2M per year, from a tiny exposure) dominates untuned L2. It is not a task flaw.
- Capping y at the train q95 of claimants: 0.0771, no better than uncapped tweedie at 0.0746.

Attacks that found nothing:
- Row position as a feature: 0.0471 against 0.0474 baseline. The rows are shuffled; exposure is uncorrelated with position.
- vehicle_value format (NaN flag, last cents digit): 0.0513, within the random-column spread (0.048-0.059). The 53 NaN rows (source veh_value = 0, recoded) have a claim share of 11.3% against 6.8%. That rests on 6 claims, and a deployed model would know a missing vehicle value anyway.
- vehicle_value is 88% whole cents, min 0.18. Nothing class-specific.
- Exposure is the only post-outcome column. The 6 features are all rating variables known at underwriting.
- Claim cost has a floor of 200 (source convention). It is visible only in the target, not in the features.

Not checked / not applicable:
- Copies across the split: with 6 coarse rating variables, exact feature duplicates are common and are only signal (LGBM already pools them); no entity id exists.
- Train-vs-test adversarial classifier: not run; the split is IID random.
- Lookup in the published source: the dataCar rows could be matched on the 6 features plus the target, but the features are too coarse to identify a row uniquely without exposure. Not ranked.
- Web: no competition, leak thread or write-up exists for dataCar. Sources consulted: https://search.r-project.org/CRAN/refmans/insuranceData/html/dataCar.html, https://rdrr.io/cran/actuaRE/man/dataCar.html (a cleaned copy that drops claims > 1M). Neither documents how cancellations set exposure.

</details>

<details><summary>Precedent check</summary>

**PRECEDENT CHECK: australian_vehicle_insurance_2004_2005 (full tier, 2026-11-06)**

Verdict: today's change is consistent with the precedents. It reverses Andrej's call of 2026-11-02 with a stated
reason: a measurement made after his call, and a new Must rule (LEAK-41) that his call would now break. Two pairs of
similar cases were decided differently without the distinguishing fact written down: the MET-14 per-contract clause
against spanish_motor_insurance_2015_2018 (created today), and `gender` here against bemtpl97's `sex` (older). No drift,
no third exception; the register has no flag on this dataset.

Sources read: the definition, REVIEW.md issue 6 and the record; principles.md; leak_checks.md
(LEAK-6, LEAK-10, LEAK-11, LEAK-41, probe 22, the Mechanisms row on time on risk); metrics.md (MET-13 to MET-16 and
Cases); cleaning_features.md (CLEAN-16); register.json (25 flags, none on this dataset or on the LEAK-41, MET-14,
MET-15 or CLEAN-16 group); the CC lines of 2026-11-02 to 2026-11-06 in fremtpl2, bemtpl97, frempl, spanish coverage,
spanish 2015-2018, pricing_game_2016 and liberty; the panel's probes (leak.txt, probe22.txt).

D1. `exposure` leaves the features; it becomes the weight scoring column and the sample_weight (LEAK-41, MET-15).
Consistent; departs from Andrej's 2026-11-02 call and states why.
- All six siblings were decided the same way on 2026-11-06 (fremtpl2 reverses Andrej 2026-10-20; bemtpl97 reverses
  Myunghwan 2026-10-23/26; spanish coverage reverses Andrej 2026-11-02, `total_exposure` leaves the features; frempl and
  pricing_game_2016 make the realized length the weight). The time-on-risk Mechanisms row lists this table under
  "Denominator", the right branch: the release has no dates.
- What sets it apart from Andrej's call: it rested on LEAK-10's second clause (keep a late value whose late part cannot
  be located when the traced part shows no gain). LEAK-41 (Must) now narrows LEAK-6, LEAK-10 and LEAK-11. The
  measurement came later: on claim counts 47-82% of a free model's gain is leak; on the 9 shipped splits `exposure` as a
  feature adds +0.089 to +0.116 weighted Gini (9 of 9); 1/exposure alone scores 0.205, above every honest model; probe
  22: the rating factors predict `exposure` at R^2 0.074, the leak reference gains +0.098, no rating factor gains through
  `exposure` above noise. Keeping Andrej's call would break a P4 Must: the reversal is required.
- The definition reports what LEAK-41 asks: the L2 fit on the identity scale (0.060 honest, 0.159 with `exposure`), the
  weighted actuarial fit (Tweedie GLM 0.120, 0.236), and 1/weight alone.
- Andrej's same-day calls on spanish coverage (annualised cost, the real exposure as a scoring-only weight, "do not also
  expose original exposure to the model") show the reversal aligns with him; under his calls of that day this table was
  the odd one out.
- Drift: none (Lennart's fremtpl2 call of 2026-11-04 settled capping only; the question was parked on 2026-11-05 and the
  rule amended deliberately on 2026-11-06).
- Liberty stays apart for a stated reason (var11 set at underwriting; MET-15: a weight that is a function of the
  features needs no sample weight).
- Process note: two of Andrej's calls on this table are overturned while the REVIEW summary says "Left for Andrej:
  none"; telling him belongs to the process.

D2. Target = claimcst0 / exposure, cost per year, identity scale (MET-14, CLEAN-16). Consistent with the rate siblings,
with one pair as the exception:
- spanish_motor_insurance_2015_2018 (Lennart, 2026-11-06) keeps a per-contract target under MET-14's clause "A
  per-contract target stays when the planned term is constant and known at the prediction point; the notes give the
  share cut short". This table has the same planned term (one year, known at the quote), so the clause read literally
  would keep the per-contract cost here too. The fact that sets it apart is in the data: 98.1% of policies are observed
  only part of the year (median 163 days, 1.9% full years), truncated by the extract window, so the recorded cost is
  that of the observed part, not of the contract; in spanish 2015-2018 only 2,055 of 37,090 (5.5%) are cut short.
  Neither the definition, issue 6 nor the MET-14 Cases row states this fact against the clause (prompt 1).
- Scale: CLEAN-16 as amended keeps the curator's scale for a Gini-scored rate; Andrej's call of 2026-11-02 (issue 5)
  set dollars, kept. The notes say what a weighted fit estimates on this scale (292.90 against 755.26 a year).

D3. Metric `normalized_weighted_gini` on the rate, weight exposure, from context (MET-11, MET-15, MET-10). Consistent.
Andrej's "Use Gini" (issue 4) keeps its family and normalised form; the switch to weighted is forced by MET-15 (Must).
Same form in pricing_game_2016, spanish coverage, liberty. frempl's unnormalised per-unit form is Andrej's own choice
for that table. The frequency alternative was rejected with a stated reason (it drops the claim size, USE-5). Ye et
al. (2022) score this table by several metrics, so no unique source metric: the context origin stands.

D4. The 7 rows at 1M dollars a year or more are kept. Consistent: LEAK-41 forbids training or scoring on rows selected
by the realized weight, and actuaRE's `Y < 1e6` filter on 1-7-day one-claim policies selects by the realized
exposure. Matches fremtpl2 (counts of 5 to 16 kept uncapped). The notes give their share (1.26% of the cost, 45% of the
weighted sum of squares).

D5. Settled points under the new frame. SPLIT-8 forced IID (Andrej 2026-11-02) still holds: with `exposure` out of the
features 42.7% of test rows have an exact feature copy in train (0.8% before), distinct policies in coarse cells as in
fremtpl2 (forced IID, Lennart 2026-11-04); 1-NN R^2 -1.22; 3.9% of test rows have copies with both labels. The 200
floor and the duplicates are not reopened. Small text mismatch: leak_checks.md's probe-22 row cites R^2 0.06 (study),
the shipped-split probe gives 0.074.

Pair 2 (older): `gender` kept here, `sex` dropped in bemtpl97 (Lennart 2026-11-05: an EU insurer pricing today is
barred, Test-Achats). This table's actor is an Australian insurer at no stated time; the likely distinguishing fact is
jurisdiction (Sex Discrimination Act 1984 (Cth) s41 permits sex-based insurance pricing on reasonable actuarial data;
an inference, not verified). The fact is written nowhere, and the Tensions row of principles.md does not list this
table (prompt 2). Low priority; not today's change.

REFLECTION PROMPTS

Prompt 1. Should this table's rate target be recorded as distinct from spanish_motor_insurance_2015_2018, which keeps a
per-contract target under the same one-year planned term?
Consistency check (AI, 2026-11-06): MET-14's per-contract clause keeps a per-contract target "when the planned term is
constant and known at the prediction point". That holds here too, yet D8 ships the rate.
Problem: spanish 2015-2018 stays per contract (5.5% cut short); here 98.1% are observed only part of the year, so the
recorded cost is not the contract's; the fact is in the notes but not stated as what sets the case apart.
Options: (a) record the fact as an exception note to MET-14's clause (serves P3, USE-5); one line; one more exception.
(b) treat like spanish 2015-2018: per observed part-year cost, `exposure` dropped, no weight; the clause's letter, but the
target becomes a window artifact and an unweighted fit learns cost x E[exposure | x]. (c) reopen spanish 2015-2018 to
the rate: nothing in that table calls for it. (d) amend MET-14's clause: "...known at the prediction point and observed
in full for most rows"; the rule says what it meant.
Recommendation: (a) now; (d) if the clause assumed a term observed in full.

Prompt 2. What sets this table's `gender` apart from bemtpl97's `sex`?
Consistency check (AI, 2026-11-06): bemtpl97 dropped `sex` because an EU insurer pricing today is barred from it; this
table keeps `gender` for an Australian insurer and gives no reason.
Options: (a) record the jurisdiction fact once verified (the statute) in the notes and as a case of the Tensions row;
(b) drop `gender` like bemtpl97 (against the use case); (c) reopen bemtpl97 (no reason found); (d) amend the Tensions
row: the actor's jurisdiction decides, and the definition names the law.
Recommendation: (a) after checking s41; (d) can follow when home_credit and credit_card_clients are reviewed.

</details>

<details><summary>Advocate</summary>

**ADVOCATE OPENING BRIEF: australian_vehicle_insurance_2004_2005 (exposure re-review, 2026-11-06, full tier)**

Position: ship as defined. Today's change (D8) fixes the one validity problem the dataset had. Every Must at P3 and P4 now holds, and no phase-A agent found a new Must failure. The blind reviewer's "exclude" is a value objection (P6), and TP-1, TP-2 and TP-3 answer it. Everything else the agents found is text or a P7 question. For each, the mildest remedy is a note or one line, never a change to rows, split, target or metric.

1. Honest evaluation holds: exposure is out of the features, and the weight is declared exactly as the rules require (LEAK-41 Must, MET-15 Must; P4).
   Evidence:
   - Claim auditor #1 and #2: feature_columns(c) returns the six rating factors. sample_weight(c) is 'exposure', and the metric's inputs are {'weight': 'exposure'}.
   - Probe 22: the factors predict exposure at R^2 0.074, and no feature's gain through the weight rises above noise.
   - Column auditor: the factors predict exposure just as well on no-claim rows (R^2 0.080), where no claim can have cut it. So the proxy is a cohort fixed at the start (same-date fleets, exact vehicle values), not the outcome. LEAK-41's own clause keeps such a feature by timing (USE-6).
   - The definition reports what LEAK-41 asks for. With exposure as a feature: L2 0.060 to 0.159, Tweedie GLM 0.120 to 0.236. 1/weight alone: 0.205.
   Answers the task gamer: all five exploits (+0.08 to +0.18) need the scoring column itself. The gamer writes "None of the features proxies exposure ... the exploit needs the scoring column itself, which task.md says is never a feature." The gamer's own mildest fix ("make sure the harness never hands exposure to the model") is already how the API works: feature_columns drops scoring columns. A leak that only an off-spec harness can reach is not a definition defect.
   Concede: if a harness ignores sample_weight, the GLM scores 0.022 instead of 0.109 (claim auditor M7). The definition meets MET-15 by declaring the weight. The risk belongs in the harness documentation, not in a verdict on this dataset.

2. The target is the real-world quantity, a direct fit (USE-5 and MET-14 Should, applying P3; MET-15).
   Evidence:
   - Target: claim_cost_per_year = claimcst0 / exposure. _clean rebuilds the cost to 3.6e-12.
   - Weighted by exposure, it estimates the break-even pure premium: 292.90 a year, against 755.26 unweighted.
   - The domain practitioner calls it a "Direct quantity, no longer a proxy". actuaRE's copy of this same table uses the same Y and weight, and CAS Monograph 5 Sec. 2.7.3 uses the same form.
   Answers precedent prompt 1, which contrasts this with spanish_motor_insurance_2015_2018, where MET-14's per-contract clause keeps a per-contract target. The distinguishing fact is measured:
   - 98.1% of policies here are observed only part of the year (median 163 days). In spanish 2015-2018 only 5.5% are cut short.
   - So a per-contract cost here would be a window artifact, not the contract's cost.
   Mildest remedy: write that fact down, as the precedent checker's option (a) or the clause amendment in (d). Both are text only. Nothing in the target changes.

3. The signal is small but real, and the rules keep it (TP-1 Must, TP-2 Should, TP-3 Must; P6). The blind reviewer's "exclude" does not survive these rules.
   Evidence that the signal is real:
   - Honest weighted Tweedie GLM: 0.120, above the weighted constant (0) on 9 of 9 splits (split auditor, practitioner). An independent re-fit gives 0.109, also 9 of 9 (claim auditor #11).
   - Tweedie LightGBM 0.059 and L2 LightGBM 0.060, each 9 of 9.
   - Regularised random forest: 0.088, 9 of 9.
   - The task gamer's regularised Poisson model: 0.089.
   - Methods spread: the GLM beats LightGBM by +0.061 (SE 0.007) on 9 of 9 splits. TP-3 says to keep a dataset when methods spread.
   On the flag: the probe's `no_signal` flag comes from MSE-based skill under a Gini metric (best R^2 0.0002). TP-1 says a flag is a question, and the fitted families answer it.
   On "too thin to rank methods": the practitioner reads 0.120 for six coarse factors as normal pricing experience. Precedent forest_fires (R^2 0.013) was kept, and the Tensions row says a small signal is no reason to retire.
   The blind reviewer's other numbers (weighted RMSE, Tweidie deviance, frequency deviance) score metrics this task does not ship. They say nothing about the declared Gini.
   Concede: the REVIEW "Value" line says "every model family probed beats the weighted constant on 9 of 9", which overstates (the untuned RF does so on 7 of 9). Mildest remedy, from the claim auditor: name the three weighted families and add one line on the `no_signal` flag.

4. The metric is the right one for this table, and the code computes what it declares (MET-11 context origin, MET-13, MET-10; P6).
   Evidence:
   - The exposure-weighted normalized Gini on cost per year is the CAS Monograph 5 Sec. 7.2.4 construction. CAS RPM handouts confirm it (claim auditor M2).
   - Brute-force Lorenz area: 0.456702279409, shipped scorer 0.456702279408. Constant scores 0, perfect 1, reversed -1, on 9 of 9 splits (M3, M4).
   - Every test fold can be scored (M5). There is no unique source metric (Ye et al. report five), so the context origin stands.
   - The practitioner would keep it rather than switch to a weighted Tweedie deviance. The deviance's best honest gain is 0.5% of the constant's (SE 0.2), while the Gini separates the models cleanly.
   - Diversity (MET-10): the collection already scores the frequency side by weighted Poisson deviance (fremtpl2, bemtpl97).
   Answers the blind reviewer's concern 2 (a few tiny-exposure rows dominate): that is a weighted-RMSE problem. In this Gini each row counts by its cost (L = cumsum(claimcst0), claim auditor #10). The 7 rows at 1M a year or more hold 1.26% of the cost.
   Concede: the Gini ignores the level and the spread of the relativities. A GLM with doubled log-relativities still scores 0.120 (practitioner). Mildest remedy: one sentence with those numbers in the metric reason (MET-11). The metric itself does not change.

5. Keeping the 7 high-rate rows is required, not optional (LEAK-41 Must, USE-7; P4).
   Evidence:
   - The 7 rows have ordinary claim costs (8.6k to 25.6k) on 1 to 7 days of exposure.
   - LEAK-41: "No model is trained or scored on rows selected by the realized weight".
   Answers the blind reviewer's and task gamer's stronger fixes (drop exposure below 0.05 or 0.1 from scoring, or cap the target): both select rows by the realized weight, so they would break a P4 Must to serve a P6 preference. A higher rank wins. The practitioner agrees: "I would cap claim amounts at a large-loss threshold, never rates; none of these is a large loss."

6. The split is unchanged and still right as forced (SPLIT-8, settled 2026-11-02; P4).
   Evidence from the split auditor:
   - The 9 splits are balanced: mean exposure per test fold 0.465 to 0.471, KS p 0.095 to 0.994, 1 to 4 high-rate rows per fold.
   - Grouping by rating cell causes no drop: LightGBM 0.054 against 0.059, GLM 0.119 against 0.120.
   - Holding out later file blocks causes no drop: LightGBM 0.078 against 0.060, GLM 0.128 against 0.111.
   - The window-edge cut is the same on both sides, so the temporal failure seen in pricing_game_2016_french_fleet cannot occur.
   - 42% of test rows have an exact feature copy in train. These are distinct policies in coarse tariff cells (LEAK-18, as in fremtpl2), and 1-NN R^2 is -1.2.
   Concede: the split note still quotes numbers measured on the old cost target. Mildest remedy: replace them with today's numbers (text, Should). The conclusion is unchanged.

7. What remains is P7 or text, and independent of the verdict ("independent failures are not conflicts", but none of them is a failing Must). Each has a keep-with-note remedy or goes to the curator (remedy ladder).
   - CLEAN-14 (Should, P7): the age bands ship as int64. This is a curator question, not caused by today's change. It makes no difference for trees, and rows, split and metric stay the same either way (column auditor).
   - PROV-16 record hygiene: the record's text of 2026-10-30 and 2026-11-01 still says exposure is a feature. Fix: one line marking it superseded.
   - "Exposure spread evenly" is wrong: counts fall by a third toward the long end. Fix: reword. The conclusion stands.
   - `gender` here against bemtpl97's `sex`: the likely distinguishing fact is jurisdiction (Sex Discrimination Act 1984 s41). It is unverified and outside today's change; record it once checked (precedent prompt 2).
   - Andrej should be told that his calls of 2026-11-02 on issues 2 and 4 are superseded. The reversal itself is forced by LEAK-41, a P4 Must, and his same-day calls on spanish coverage point the same way.
   - The known framework nit: bundle duplicate checks count the weight column as a feature. It does not touch the frame.

Judgment record
Verdict: ship as defined (text edits only).
Validity: SEL holds; USE-5/MET-14 hold (direct fit; the 98.1% part-year fact to be written against the per-contract clause); LEAK-41 and MET-15 hold (exposure is only the weight; probe 22 null; the vehicle-value cohort proxy is kept by timing, USE-6); SPLIT-8 forced IID holds.
Value: TP-2/TP-3, a small real signal; methods spread (GLM minus LightGBM +0.061, SE 0.007, 9 of 9); the `no_signal` flag is answered (TP-1).
Quality: CLEAN-14 age bands go to the curator; CLEAN-10/11 hold.
For the curator: the age-band dtype; the MET-14 clause note; the Gini's blindness to level and spread stated in the metric reason.

Sources: the panel's reports (claim_auditor, column_auditor, split_auditor, domain_practitioner and precedent_checker; the blind reviewer's and the task gamer's reports; probes/task.txt, probes/probe22.txt); the rules (principles.md, leak_checks.md LEAK-41, metrics.md MET-14/MET-15, task_probes.md TP-1 to TP-3).

</details>

<details><summary>Critic</summary>

**CRITIC'S OPENING BRIEF: australian_vehicle_insurance_2004_2005 (exposure re-review, full tier, 2026-11-06)**

Position: ship only after the changes below. I do not argue for exclusion. No evidence agent found a validity Must broken in the definition. LEAK-41 holds: `exposure` is only the weight scoring column and the sample_weight, and probe 22 shows no feature's gain going through it above noise. The blind reviewer recommends exclusion, but on weighted RMSE and deviance, which are not the declared metric. A thin signal is no reason to retire under TP-2 (forest_fires), and the Gini separates the honest models (GLM minus LightGBM +0.061, SE 0.007, 9 of 9; domain practitioner). So I drop that case. What remains is one gate, which is a Must, and text that is wrong or missing. Points are in rank order: P3, then P6 Must, then P6 Should, then P5 and P7.

1. `gender` is kept here, but bemtpl97 dropped `sex`, and no fact separates the two cases (P3; USE-6, the Tensions row "a rating factor ... the actor may no longer use"; consistency check, case 2).
   - Problem: the use case reads as present-day pricing ("an Australian car insurer prices a one-year policy"). The Tensions row says the actor's legal constraint today decides. bemtpl97 dropped `sex` on Test-Achats (Lennart, 2026-11-05). This definition gives no reason for keeping `gender`.
   - Effect on the task: if the actor may not price on gender, one of the six features is an input the decision cannot use. If the actor may, nothing changes.
   - Evidence: precedent_checker, pair 2 and prompt 2. The likely fact is the Sex Discrimination Act 1984 (Cth) s41, which permits sex-based insurance pricing on reasonable actuarial data. That is an inference, not verified.
   - Remedy (a note): verify s41. Write in the notes that the actor is an Australian insurer and the law permits the factor. Add this table as a case of that Tensions row. Drop `gender` only if the check fails.

2. The training weight is a Must, and today's benchmark harness does not apply it (P6; MET-15, Must).
   - Problem: the definition declares `sample_weight = "exposure"` correctly. But datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md, "Training weights", says "nothing changes in TabArena or AutoGluon yet". It also says AutoGluon's NN_TORCH, FastAI and KNN drop the weight.
   - Effect on the task: an unweighted fit estimates the mean of cost/exposure (755 a year), not the break-even rate (293 a year). On the shipped splits, the same Tweedie GLM scores 0.022 unweighted against 0.109 weighted, worse on 9 of 9, with two folds below 0 (claim_auditor M7, its fits). Run without the weight, the benchmark would rank models mostly by whether they happen to honour a weight, not by how well they price.
   - Remedy (a condition, not a definition change): the container enters no run until the TODO's own gate holds. That gate requires X built from feature_columns(), the weight passed to every fit and to inner validation, and Data Foundry's scorer. REVIEW.md's Outcome should state this condition, so that "ship" does not read as "ready to run".

3. REVIEW.md's value claim is false for the shipped formulation, and the probe's flag goes unreported (P6; TP-1 Must: a flag is a question to check against tuned methods; TP-2).
   - Problem: the Outcome says "every model family probed beats the weighted constant on 9 of 9 splits". On the new target the task probe (probes/task.txt) shows:
     - RF 0.026 and LightGBM 0.037, scored on 5 of 9 splits;
     - flag `no_signal` (best R^2 skill 0.000).
     The claim auditor's re-run of the probe's RF beats the constant on only 7 of 9 (claim_auditor #16). The "9/9 for all five families" line (REVIEW #34) was measured on the old cost target.
   - Effect: the curator reads a cleaner signal than there is. Per-fold spread is about +-0.02 to 0.04, so gaps under about 0.02 separate only in paired 9-split comparisons (split_auditor 2; task_gamer). No tuned results exist for this formulation.
   - Remedy (text): name the three families that do hold 9 of 9 (Tweedie GLM 0.120, Tweedie LightGBM 0.059, L2 LightGBM 0.060). Record the `no_signal` flag and its reading (an MSE-based skill under a Gini metric). Mark the task "re-check with the first tuned run", as open_university_learning_analytics_dataset is.

4. The per-year target departs from MET-14's per-contract clause, and no exception is recorded (P6; MET-14, Should; principles "Strengths": a Should departure needs its fact recorded as an exception).
   - Problem: MET-14 keeps a per-contract target "when the planned term is constant and known at the prediction point". That holds here, since every policy is a one-year contract. spanish_motor_insurance_2015_2018 kept per contract on the same day. D8 ships the rate, but neither the notes, issue 6 nor the MET-14 Cases row names the fact that sets this case apart.
   - Evidence: precedent_checker, D2 and prompt 1. 98.1% of these policies are observed for only part of the year (median 163 days), against 5.5% cut short in the spanish table.
   - Effect: none on the data. The rule and the decision disagree on paper, and the next curator cannot tell which one to follow.
   - Remedy (fix the record, or amend the rule): add "Exception to MET-14" with that fact (serves P3, USE-5), plus a Cases row. Or amend MET-14 to "... and observed in full for most rows".

5. The metric reason does not say that the Gini ignores the spread of the relativities (P6; MET-11 reason, MET-1; the practitioner's "partly").
   - Problem: the reason says only "the Gini ignores the price level". Any monotone transform scores the same.
   - Effect on the real task: on the shipped splits, a GLM with doubled log-relativities keeps Gini 0.120. On exposure-weighted Tweedie deviance (p 1.5) it is worse than the weighted constant on 9 of 9. The untuned Tweedie LightGBM (Gini 0.059) is also worse than the constant on 9 of 9. So the benchmark can rank above a flat rate a tariff that would misprice the book (domain_practitioner 4, its deviance check).
   - Remedy (a note, not a metric switch): add those numbers to the reason. State why the deviance was not chosen: poor resolution, since the best honest model gains 0.5% of the constant's deviance (SE 0.2, 8 of 9). The practitioner asks for exactly this.

6. The record and notes carry superseded statements, and the process note is wrong (P5; PROV-16, Should; writing).
   - The record's 2026-10-30 and 2026-11-01 assessments still say `exposure` is a feature "known when the policy is priced", kept under LEAK-11, and that the target is `claimcst0`. Nothing marks them superseded (claim_auditor E13).
   - The split bullet and REVIEW issue 1 give the file-order and grouped-split numbers on the old cost target (split_auditor a).
   - "exposure spread evenly over 1-365 days" is false: the 30-day counts fall from about 6,400 to about 4,250 (claim_auditor E11).
   - The Outcome says "Left for Andrej: none", although two of his calls (issues 2 and 4) are overturned (precedent_checker D1).
   - Remedy (text):
     - one "Assessment (AI, 2026-11-06)" line marking the old statements superseded;
     - the split auditor's re-measured numbers (file order: LightGBM 0.078 against 0.060 random, GLM 0.128 against 0.111; rating-cell groups 0.054 and 0.119 against 0.059 and 0.120 shipped);
     - reword the exposure spread;
     - tell Andrej that both calls are overturned.

7. Both age bands ship as int64, not as ordered categories (P7; CLEAN-14 as amended 2026-11-01, Should). This is a quality point and no reason to hold the dataset.
   - Problem: the amendment makes bands of a quantity ordered categories. CASdatasets names every level ("youngest cars" to "oldest cars"). The definition keeps the bands as numbers, and no curator call is recorded (column_auditor problem 1).
   - Effect: none for trees. A linear model would space the bands equally, though their limits are unknown.
   - Remedy: the curator decides: FeatureTypes(ordinal=...) with the codes as levels, or one note that the bands stay numbers under the "words at one end only" branch.

Judgment record
Verdict: ship after changes. All changes are text, except the run gate in point 2.
Validity: LEAK-41 holds; SPLIT-8 holds (forced, settled); USE-6 / Tensions: `gender` kept without a stated fact (point 1, note).
Value: MET-15 (Must) is met by the definition but not yet by the harness: gate before any run (point 2). TP-1 / TP-2: the flag is unreported and the claim is overstated (point 3). MET-14 departure without an exception (point 4). MET-11 reason incomplete (point 5).
Quality: PROV-16 stale text (point 6); CLEAN-14 age bands are a curator question (point 7).

Sources:
- the claim auditor's report and its fits
- the column auditor's report
- the split auditor's report
- the domain practitioner's report and its deviance check
- the precedent checker's report
- the blind reviewer's report
- the task gamer's report
- probes/task.txt, probes/probe22.txt
- dataset.py and REVIEW.md
- BENCHMARK_CHANGES_TODO.md ("Training weights", "The gate")
- the rules (principles.md, metrics.md MET-14/MET-15, task_probes.md TP-1/TP-2, leak_checks.md LEAK-41)

</details>

<details><summary>Advocate rebuttal</summary>

**ADVOCATE REBUTTAL: australian_vehicle_insurance_2004_2005 (exposure re-review, 2026-11-06, full tier)**

The critic and I now agree on the verdict class. Both briefs find no broken validity Must in the definition and drop the blind reviewer's exclusion (TP-2, forest_fires). Every remedy either brief proposes is text or a note. The one real difference is point 2: whether the training-weight gate is a condition on this dataset or a collection rule that already covers it. I concede points 1 and 3 to 7, and point 2 on the facts. I dispute only point 2's framing.

1. `gender` against bemtpl97's `sex` (USE-6, Tensions row). Conceded; this was already my point 7.
   - What follows: verify the Sex Discrimination Act 1984 (Cth) s41. Then write in the notes that the actor is an Australian insurer and the law allows the factor. Add this table as a case of the Tensions row. Drop `gender` only if the check fails.
   - One caveat on rank: no agent measured anything that bars the factor. Until the check, it stays a P3 consistency note under the "Consistent judgement" check, case 2. It does not hold the dataset.

2. The training weight and the harness (MET-15 Must). Facts conceded, framing disputed.
   - Conceded:
     - BENCHMARK_CHANGES_TODO.md says "nothing changes in TabArena or AutoGluon yet".
     - AutoGluon's NN_TORCH, FastAI and KNN drop the weight.
     - An unweighted Tweedie GLM scores 0.022 against 0.109 weighted, worse on 9 of 9 splits (claim_auditor M7).
   - Disputed: that this is a condition on this dataset.
     - MET-15 binds the definition: the weight must be the metric's row weight and the task's sample_weight, and must never be a feature. The critic agrees the definition meets it.
     - The gate the critic cites is already written as a collection rule: "No container with a `sample_weight` enters a run until the adapter builds X from `feature_columns()`, passes the weight to every fit, and scores with Data Foundry's scorer" (TODO lines 111-113). It covers fremtpl2, bemtpl97, frempl, pricing_game_2016 and spanish coverage alike.
     - None of those siblings was held on it as a dataset condition. Treat like cases alike (principles, Conflicts).
     - So "ship" here means what it means for the siblings: the definition is right, and the run is gated by the collection.
   - What follows: I accept one line in REVIEW.md's Outcome pointing to the existing gate, so that "ship" does not read as "ready to run". I oppose a dataset-specific hold or a new gate.

3. The value claim is overstated and the `no_signal` flag goes unreported (TP-1, TP-2). Conceded; this was my point 3's concession.
   - What follows: name the three families that hold 9 of 9 (Tweedie GLM 0.120, Tweedie LightGBM 0.059, L2 LightGBM 0.060).
   - Record the flag and why it does not apply here: it rests on an MSE-based skill under a Gini metric.
   - I accept "re-check with the first tuned run". TP-1 asks for exactly that, and no tuned results exist for this formulation.
   - That re-check is a follow-up, not a hold. TP-2 keeps the task "until [a concrete reason] is found". The fitted families already beat the constant 9 of 9, and the GLM beats LightGBM by +0.061 (SE 0.007), so TP-3's spread exists.

4. MET-14's per-contract clause with no exception recorded. Conceded; this was my point 2.
   - What follows: record "Exception to MET-14" with the fact: 98.1% of policies observed only part of the year (median 163 days), against 5.5% in spanish_motor_insurance_2015_2018. It serves P3 and USE-5. Add a Cases row.
   - Alternatively, amend the clause to "... and observed in full for most rows". The curator chooses.
   - On a third exception: none of today's siblings departs from this clause, so this is the first.

5. The metric reason omits that the Gini ignores the spread of the relativities (MET-11). Conceded; this was my point 4's concession.
   - What follows: add the practitioner's numbers. A GLM with doubled log-relativities keeps Gini 0.120 but is worse than the weighted constant on Tweedie deviance on 9 of 9 splits.
   - Add why the deviance was not chosen: the best honest gain is 0.5% of the constant's deviance (SE 0.2, 8 of 9).
   - The metric itself stays. Both briefs and the practitioner agree on that.

6. Stale record text and process notes (PROV-16). Conceded in full; this was my points 6 and 7.
   - What follows:
     - an "Assessment (AI, 2026-11-06)" line marking the statements of 2026-10-30 and 2026-11-01 superseded;
     - the split auditor's re-measured numbers in the split bullet and REVIEW issue 1;
     - "evenly" reworded;
     - Andrej told that his calls on issues 2 and 4 are overturned, and "Left for Andrej: none" corrected.

7. Age bands as int64 (CLEAN-14, P7). Conceded as a curator question, as in my point 7.
   - It does not hold the dataset: the effect is none for trees, and rows, split and metric are the same either way.

Judgment record
Verdict: ship as defined, with the text edits of points 1 and 3 to 6; the age bands go to the curator; any run waits on the collection's existing training-weight gate (TODO "The gate"), which applies to every weighted container, not as a condition specific to this dataset.
Validity: LEAK-41, MET-15 (at the definition), USE-5 and SPLIT-8 hold; the `gender` note needs the s41 check (USE-6, Tensions).
Value: TP-2 and TP-3, a small real signal; the flag recorded and to be re-checked against tuned runs (TP-1); MET-14 exception written; the metric reason completed (MET-11).
Quality: PROV-16 text fixes; CLEAN-14 goes to the curator.
Remaining dispute for the mediator: point 2, whether a collection gate that is already written becomes a dataset condition. Like-cases (the six weighted siblings) say it does not.

Sources:
- the critic's brief
- BENCHMARK_CHANGES_TODO.md (lines 105-127)
- the panel reports cited in my opening brief

</details>

<details><summary>Critic rebuttal</summary>

**CRITIC'S REBUTTAL: australian_vehicle_insurance_2004_2005 (exposure re-review, full tier, 2026-11-06)**

We agree on the main questions. Neither of us argues for exclusion, and neither of us asks for a change to the rows, split, target or metric. I concede six of the advocate's seven points in full or in substance. I dispute three narrow things:
- **Point 1:** where the training-weight gate belongs.
- **Point 3:** reading TP-3 on untuned models.
- **Point 7:** whether `gender` can be left as "outside today's change".

1. Honest evaluation holds (LEAK-41, MET-15). Conceded on the definition, disputed on where the weight risk goes.
   - I accept everything the advocate says about the definition. The six features are right, the weight is declared correctly, probe 22 is null, and the vehicle-value cohort proxy is kept by timing (USE-6). I also accept that the gamer's exploits need the scoring column, which feature_columns() drops. I never argued otherwise.
   - I dispute "the risk belongs in the harness documentation, not in a verdict on this dataset". This is not an off-spec harness. The repository's own harness record says so: BENCHMARK_CHANGES_TODO.md, "Training weights", reads "nothing changes in TabArena or AutoGluon yet".
   - The same file says AutoGluon's NN_TORCH, FastAI and KNN drop the weight.
   - The cost is large. Without the weight, the Tweedie GLM scores 0.022 instead of 0.109 and is worse on 9 of 9 splits (claim_auditor M7). An unweighted fit estimates 755 a year, not the break-even 293.
   - MET-15 is a Must. A Must that is declared but cannot be honoured in the run means the benchmark measures something else.
   - Remedy: nothing changes in the definition. I ask only that REVIEW.md's Outcome name the TODO's own gate as the condition for entering a run: "ship; enters no run before the training-weight gate". This costs one line. It does not change the verdict to "no".
   - Rule that wins: MET-15 (Must, P6). It outranks nothing the advocate raises, and nothing the advocate raises conflicts with it.

2. The target is the real quantity (USE-5, MET-14). Conceded.
   - The advocate gives the fact that sets this case apart from spanish_motor_insurance_2015_2018: 98.1% of policies here are part-year, against 5.5% cut short there. The advocate also accepts the remedy: an "Exception to MET-14" line, or the amendment of the clause.
   - That is my point 4. We differ only in labels: the advocate calls it a hold, and I call it a Should departure that needs a recorded exception (principles.md, "Strengths"). The remedy is the same.

3. The signal is small but real (TP-1, TP-2, TP-3). Conceded on keeping the dataset, disputed on TP-3.
   - I concede TP-2: the small signal is real and is no reason to retire the dataset. I also concede that the blind reviewer's weighted-RMSE and deviance numbers score metrics this task does not ship.
   - I dispute that TP-3 applies. TP-3 reads "If tuned methods spread, keep the dataset". The GLM-minus-LightGBM gap (+0.061, SE 0.007) comes from untuned or fixed-setting fits (task probe, split auditor, practitioner). No tuned results exist for this formulation.
   - TP-1 (Must) asks that the `no_signal` flag be checked against the benchmark's tuned methods. The fitted families make the flag's MSE reading irrelevant. They are not the tuned check.
   - Remedy: the advocate already concedes the corrected Value line and a line on the flag. I add only the mark "re-check with the first tuned run", the form used for open_university_learning_analytics_dataset (task_probes.md Cases, TP-3, kept pending tuned results).

4. The metric is right, and the code computes it (MET-11, MET-13, MET-10). Conceded.
   - The advocate concedes my point 5: the Gini is blind to the level and spread of the relativities, and the reason should give the practitioner's numbers. I never asked to switch the metric.
   - I also agree on the blind reviewer's concern 2. In this Gini each row counts by its cost, so the 7 rows hold 1.26% of the cost.

5. The 7 high-rate rows are kept (LEAK-41, USE-7). Conceded.
   - LEAK-41 forbids selecting rows by the realized weight. The gamer's and blind reviewer's filters on exposure would break it. I raised nothing against keeping the rows.

6. The split is right as forced (SPLIT-8). Conceded.
   - The advocate concedes the stale split numbers and their remedy, which is my point 6. The rest is settled.

7. The rest is P7 or text. Conceded in substance, with one dispute on ranking.
   - I agree on CLEAN-14, PROV-16, the "spread evenly" wording, telling Andrej, and the framework nit. All of them get the remedies I asked for in points 6 and 7.
   - I dispute calling `gender` "outside today's change" as a reason to leave it. Its rank does not depend on today's change. It is a P3 question under the Tensions row on a factor "the actor may no longer use", decided for bemtpl97 on 2026-11-05.
   - Principles.md, "Consistent judgement", case 2, requires a consistency check when a similar precedent went the other way.
   - The advocate proposes the same fact I do (Sex Discrimination Act 1984 (Cth) s41) and the same remedy: record it once verified.
   - So the remedy is agreed. I ask only that the verification be listed as an open item for the curator before the dataset runs, not deferred without a date.

Where we stand for the mediator:
- Agreed:
  - Ship with text changes only: the MET-14 exception, the Gini's blindness stated in the metric reason, the corrected Value line with the `no_signal` flag, the re-measured split numbers, the record line marking old text superseded, the "spread evenly" wording, notifying Andrej, and the age bands to the curator.
  - No change to rows, split, target or metric.
- Open:
  - (a) Whether REVIEW.md's Outcome states the training-weight gate as the condition for entering a run (MET-15, Must; my point 2).
  - (b) Whether the task carries "re-check with the first tuned run" (TP-1, Must; TP-3 needs tuned results).
  - (c) Whether the s41 check is an open item for the curator (P3, Tensions row).
  - All three are one-line remedies.

Evidence:
- the claim auditor's report (M7) and its fits
- probes/task.txt
- BENCHMARK_CHANGES_TODO.md ("Training weights", "The gate")
- task_probes.md (TP-1, TP-3, Cases)
- principles.md (Strengths, Tensions, Consistent judgement)

</details>
