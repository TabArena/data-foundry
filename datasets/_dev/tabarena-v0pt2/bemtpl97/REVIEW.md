# bemtpl97

**Outcome:** added. Verdict: ship after changes (mediator). Validity: USE-3 and USE-5 hold (the source's own claim
count; every feature except `expo` is registered at policy start); LEAK-10 (Must) is triggered by `expo`, whose use
beyond plain exposure carries 16-18% of the model's skill (issue 1); SPLIT-8 holds (one undated year, IID with
`ForcedIIDFromTemporal`, fit approximate); PROV-9 and PROV-10 were triggered by a public copy from 2019 and are fixed
in the metadata. Value: MET-1, MET-5 and MET-13 hold (the source's Eq. 5, floor 1e-6), MET-2 holds for the shipped
metric (claim auditor); TP-2 shows a real signal (4.2-4.4% deviance skill, 9/9 folds; 3.7% with `expo` as an offset
only, so the signal survives the fix in issue 1). Quality: CLEAN-14 holds. Weighed: none decides the verdict; issue 2
is a USE-5 weighing call. Left for Lennart: issue 1, decided for bemtpl97 and fremtpl2 together; issues 2 and 3; then
a rebuild when you ask for it.

**Main points:** Make `expo` a scoring column, as the source uses it, or keep it as a feature under a LEAK-10
amendment, for both MTPL datasets; then two small calls: keep the release's 19 removed policies out, and keep or drop
`sex`.

**Record judgment:** valid; a documented Belgian motor-insurance portfolio and the source's own frequency task. Five
statements in the record are out of date after this panel: the AI line of 2026-11-04 calls exposure an offset (as
shipped it is a free feature); the 2026-10-26 lines call the removal of the 19 policies unverified (it is now verified
row by row); the first CC of 2026-11-04 says the scorer floors at machine epsilon (superseded the same day by
`min_prediction=1e-6`); "the 20 other forced-IID definitions" are 17 in the working copy; "no panel ran" is superseded
by this panel. The year is now 2019 in the definition and the record.

**Issues for Lennart:**

1. **Make `expo` a scoring column instead of a feature?**

   * **Problem:**
     - `expo` is the share of 1997 a policy was insured, and the source gives two reasons for less than a full year:
       the policyholder "started the policy in the course of the year" (known when the premium is quoted) or
       "surrendered the policy before the end of the year" (often after a claim, so known only later)
       ([arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3), Sec. 4.1).
     - The source uses exposure only in proportion, the expected count being `expo` times the annual frequency with
       the slope fixed at 1 (an offset; Eq. 5 and
       [treeML.Rmd L641-657](https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd#L641-L657)),
       but here `expo` is a plain feature, so a model can learn that short policies claim more per insured day.
     - An actuary cannot use that, because at quotation the exposure is set to a full year, and without dates the two
       reasons cannot be told apart.
   * **Background:** A value from the outcome's period stays only when the data shows it does not move with the
     outcome given the covariates[^leak10]; the narrower rule for anonymised fields does not apply here[^leak38].
     Because that rule is a Must, keeping `expo` as a feature needs an amendment of it for exposure as the denominator
     of a count target; an exception is not enough. A scoring column is a column the scorer reads and the model never
     sees. Under it a model does not see `expo` while it trains unless the harness passes it; trained on `nclaims`
     alone, it learns the count per observed period, not the annual frequency the scorer multiplies by `expo`. There
     are two ways to pass it, and they rank every model the same (mediator): (i) the count target with `expo` as an
     offset at fit time, for models that take one; (ii) the target `nclaims / expo` with `expo` as the sample weight,
     for any model that takes weights. Form (ii) changes the shipped target.
   * **Experiments:** Four agents, independently: per insured year, policies insured up to a quarter of the year claim
     0.292 times, full-year ones 0.126. Given all other features and a proportional offset, part-year policies claim
     about 1.4 times what is expected, and the fitted coefficient on log(`expo`), when it is not fixed, is 0.45-0.54; 1
     would mean claims scale exactly with insured time. New business does not explain it: part-year rows at the entry
     bonus-malus level (bm = 11) show 1.39 times, the rest 1.41; existing policyholders (bm other than 11) reach 2.13
     at `expo` up to 0.1.

     | LightGBM-Poisson, 9 folds (claim auditor) | mean deviance | skill over the training mean |
     |---|---|---|
     | `expo` as a free feature (shipped) | 0.5274 | 4.4% |
     | `expo` as an offset only | 0.5314 | 3.7% |
     | no `expo` | 0.5369 | 2.7% |
     | training mean | 0.5517 | 0 |

     The free use gains 0.0036-0.0041 over the offset, 16-18% of the skill; a random column moves the score by
     0.0001-0.0004.
   * **Consistency:** The keep of 2026-10-23 and 2026-10-26 (Myunghwan) and 2026-11-04 (Lennart) rested on the fit on
     log(`expo`) alone (0.5470 against 0.5517), which measures only the proportional part; the conditional test is the
     new fact. fremtpl2 shows the same mechanism (slope 0.62; deviance 0.2428 with the offset, 0.2407 free) and keeps
     Exposure "as in bemtpl97".
   * **Panel:** The mediator and the critic recommend the scoring column, and so does the advocate after its rebuttal.
   * **Unknown:** Policy start and end dates would settle the mechanism; no copy has them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as a feature (implemented) | `expo` is one of the 13 features; the note says "kept on purpose" and now gives both causes and the measured gain; the leak rule is amended for exposure as the denominator of a count target | no change to the features or the metric | a model can use that short policies claim more per insured day, 16-18% of the skill; needs an amendment of a Must, an exception is not enough |
     | B | Scoring column | `expo` leaves the features; the model predicts the annual frequency, and the scorer computes the mean Poisson deviance of `nclaims` against `expo` times the prediction | under form (i) target, rows and metric stay the source's; the proportional part of `expo` stays | it also removes the part from mid-year starts (bm = 11 at `expo` up to 0.1: 3.36 times expected); the scorer needs an exposure input with tests; form (ii) changes the shipped target |

   * **Recommendation:** B, the scoring column (mediator, critic, and the advocate after its rebuttal).
     **Decision:** B (scoring column) or A (keep as a feature under an amendment of the leak rule), for bemtpl97 and
     fremtpl2 together?

   **Notes for the AI:** the decision goes into a CC line that names LEAK-10, for bemtpl97 and fremtpl2 together. On
   B, `_poisson_deviance` in `src/data_foundry/v2/metrics.py` needs an exposure input with tests, and Claude picks the
   form ((i) offset at fit time, or (ii) target `nclaims / expo` with `expo` as sample weight) together with the metric
   change. On A, write the LEAK-10 amendment for exposure as the denominator of a count target.

   [^leak10]: **LEAK-10** (Must): a value from the outcome's period stays only when the data shows it does not move
     with the outcome given the covariates (account_debt_south_africa, 2026-10-26); late values that cannot be located
     row by row go when they may carry a gain (distribution_transformers_at_cauca_department).
   [^leak38]: **LEAK-38** does not apply: `expo` is a named field, and comparing part-year claims with what the other
     features and proportional exposure predict measured the mechanism.

   **Lennart (2026-11-05, discuss):** This is related to the discussion for fremtpl2, compare it and check

   **Answer (AI, 2026-11-05):** It is the same question, with the same facts, so the two should be decided together; see
   fremtpl2 issue 6's answer of today. Here part-year policies claim about 1.4 times what a proportional offset expects,
   and a free `expo` gains 0.0036-0.0041 mean deviance over the offset (16-18% of the skill); in fremtpl2 the free
   `Exposure` gains 0.0033-0.0047 (21-30% of the gain after today's blanking). Neither has dates that tell a mid-year
   start from a cancellation. The open PRs #44 to #47 do not settle it: they add no exposure weight to the Poisson
   deviance and no training-weight declaration, and #44 keeps an unlocated cut with a measured note. So the choice is
   the same in both:
   - (a) A for both: `expo` / `Exposure` becomes a weight scoring column, the target the annual frequency, the metric a
     weighted Poisson deviance, and the benchmark passes the exposure as `sample_weight` (new code in the API, the
     container and the benchmark);
   - (b) B for both: the feature stays, with an amendment of LEAK-10 for exposure as a denominator and the measured size in
     the note.

   Your answer here also answers fremtpl2 issue 6.

   **Lennart (2026-11-05, discuss):** see my comment for fremtpl on this

   **Deferred (2026-11-05):** parked with fremtpl2 issue 6 until the zero-inflated stack (PRs #44-#47) is merged; [#51](https://github.com/TabArena/data-foundry/issues/51)
   holds the context. The declared metric waits with it.

   **Resolved (2026-11-06, Lennart):** B, as the rate with a sample weight (option A of
   [#51](https://github.com/TabArena/data-foundry/issues/51), the exposure study of 2026-11-05). The target is
   `nclaims_per_year` = `nclaims` / `expo`; `expo` is the weight scoring column, the `weight` input of
   `mean_poisson_deviance` and the task's `sample_weight`, and never a feature (LEAK-41, MET-14, MET-15, adopted the same
   day); the floor is 1e-4 claims per year (MET-13). This is the source's offset model (Henckaerts et al., Eq. 5): on
   every shipped fold the weighted rate deviance equals the count deviance of the same predictions times n/sum(expo) of
   the scored rows (1.123 to 1.125). Supersedes Myunghwan's calls of 2026-10-23 and 2026-10-26 (keep `expo` as a
   predictor; do not weight) and the floor of 2026-11-04 (1e-6 on the expected count): the conditional measurement came
   later (+0.0043, 17% of the skill; never better at quotation), and the source itself scores with an offset. The
   low-cardinality acceptance goes (the rate has 559 values); the built container `01a18ad7` is superseded.
   `dataset check`: 0 errors, 0 warnings.

2. **Ship the 163,212 released rows or all 163,231?**

   * **Problem:**
     - The release leaves out the 19 policies whose average claim cost exceeds EUR 81,000, now verified row by row
       against the first public copy of 2019 (all 19 are claimants, 21 claims, 0.1% of all claims; every other row is
       identical and in the same order).
     - A cut by claim cost depends on the outcome, so the test folds miss 19 heavy claimants, too few to matter for a
       frequency task (the domain practitioner: negligible).
     - Whether to keep the cut or undo it is a weighing call[^use5].
   * **Panel:** The mediator, the advocate and the critic agree on keeping 163,212.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep 163,212 rows (implemented) | the release's rows; the note now states the selection as a fact | these are the rows the boosting paper evaluates on (Sec. 4.1); the cut is the source's own preprocessing ("exclusion of very large claims") | the test folds miss 19 heavy claimants |
     | B | Restore all 163,231 | download the 2019 file and ship 163,231 rows | the unselected 2019 copy exists, so the cut can be undone | a new download; rows that differ from the ones the metric's paper used |

   * **Recommendation:** A, keep 163,212 (mediator, advocate and critic agree). **Decision:** A (keep) or B (restore)?

   [^use5]: **USE-5** (Weigh, as the panel weighs it) and **USE-8** (a selection alone does not change the fit).

   **Lennart (2026-11-05, ok):** If this is the official verison, we can stay with it for now instead of moving on

   **Answer (AI, 2026-11-05):** Partly, and I corrected my first reply. The 163,212 rows are what the source's GitHub
   release ships and what its boosting paper evaluates on (Sec. 4.1), with "exclusion of very large claims" as its own
   preprocessing; but the first publication (PROV-8) is the 2019 copy with all 163,231 rows, so the official version
   by our rule is the unselected one. Keeping the release's rows (A) is still a weighing call, and since the cut is by
   claim cost, the fit rule as amended on 2026-10-27 asks `fit_reason` to name it and the record to carry `Selection
   Bias`, as lt and tunisian do.
   - (a) A, with the selection named in `fit_reason` and the `Selection Bias` marker;
   - (b) B, restore the 2019 rows.

   **Lennart (2026-11-05, ok):** Reply (b): B, restore the 2019 rows

   **Resolved (2026-11-05, Lennart):** (b). The 2019 copy (katrienantonio/PE-pricing-analytics, commit of 2019-09-26,
   SHA-256 pinned) ships all 163,231 rows; minus its 19 rows with an average claim above EUR 81,000 it equals the
   release row by row, so the selection by claim cost is gone and no `Selection Bias` marker is needed. The 2019
   repository states no licence (a note). LightGBM-Poisson mean deviance 0.5274 to 0.5279; the free `expo` still gains
   0.0039 over the offset.

3. **Confirm that `sex` stays?**

   * **Problem:**
     - The notes say "sex stays by curator choice, for research on a 1997 tariff", but no curator line in the record
       states that choice; the 2026-10-23 line accepts the 13 predictors without naming it.
     - Gender-based insurance pricing is banned in the EU since 21 December 2012 (CJEU C-236/09, Test-Achats), so a
       tariff today would not use it.
     - The ethics rule is not triggered: no subject or creator objects to this use[^sel1].
   * **Effect on the task:** A model may use a rating factor that a tariff written today cannot.
   * **Consistency:** No other rule covers protected attributes, and no precedent was found.
   * **Unknown:** Its share of the score was not measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `sex` (implemented) | `sex` stays a nominal feature, disclosed as a 1997 rating factor | a rating factor of the 1997 tariff the data describes; the domain practitioner: fine if disclosed | a tariff written today cannot use it |
     | B | Drop it | `sex` leaves the features | no factor a tariff written today cannot use | one fewer rating factor of the 1997 tariff the data describes |

   * **Recommendation:** A, keep it, disclosed as a 1997 rating factor (the domain practitioner: fine if disclosed).
     **Decision:** A (keep) or B (drop)?

   **Notes for the AI:** on A, write Lennart's reason as a CC line.

   [^sel1]: **SEL-1** (ethics, Must): a task with ethical concerns is out, including data whose subjects or creators
     ask that it not be used for ML.

   **Lennart (2026-11-05, change):** Option B: Drop it. I think it is valid to remove it from the data to have models
   that more acucratly track what would be used today

   **Consistency check (AI, 2026-11-05):** dropping `sex` departs from USE-6 (Must: what is known at the prediction
   point is a legitimate input) while the actor prices the 1997 tariff the notes describe, from the kept `CODE_GENDER`
   (home_credit_default_risk) and `SEX` (credit_card_clients_default), and from SEL-18 of today, where "today one would
   use other features" is a note. No rule covers protected attributes. What sets it apart?
   - (a) the actor is an EU insurer pricing today, and the Test-Achats ruling (2012) bars sex as a rating factor:
     `use_case` and `known` move to today's tariff, with a Tensions row;
   - (b) keep it, as the panel said;
   - (c) (a), and review the credit datasets that keep sex too;
   - (d) a new rule on protected attributes.

   Give the letter in the note; nothing is applied until then.

   **Lennart (2026-11-05, change):** Reply (a): the actor is an EU insurer pricing today, and the Test-Achats ruling
   (2012) bars sex as a rating factor: use_… Option B: Drop it. We make this special case here as we would try to
   understand how good such models would be in the current world, and they would not be able to use sex

   **Resolved (2026-11-05, Lennart):** (a). The actor is an EU insurer pricing today; since 21 December 2012 EU law bars
   sex as a rating factor (CJEU C-236/09, Test-Achats), so `sex` leaves the features (it carried 0.00038 deviance, 1.6%
   of the skill). `use_case`, `known` and `fit_reason` are rewritten; a Tensions row in principles.md (the actor's legal
   constraint today wins when the use case is today's pricing; home_credit_default_risk and credit_card_clients_default
   keep sex, not reviewed yet).

**Review panel:** ship after changes (mediator). Tier full, second pass after Lennart's PR #33 review of 2026-11-04. Claims: 21 audited, 14 hold, 4 refuted in whole or in part (the year, the citation, the `known` sentence and the reason the `expo` note gave; all fixed in the notes, the `expo` question stays as issue 1), 1 record wording inconsistent, 2 untested (the build, the licence). Blind review: include with changes; its main concern is `expo` as a plain feature (its RMSE concern is moot, the definition scores by deviance). Task gamer: no real leak; its best exploit is `expo` used freely instead of as an offset, 0.0039 of deviance (0.0032 to 0.0047 per split) against a noise band of 0.0001 to 0.0004, the known kept-on-purpose note. Agreed: the split (SPLIT-8), the metric (MET-1, MET-5, MET-13), the dtypes (CLEAN-14), the copies (LEAK-16) and the provenance fixes (PROV-9, PROV-10). Disputed: only whether the rebuild is a separate gate (EV-7). On LEAK-10 the advocate withdrew the amendment in its rebuttal, so all sides recommend the scoring column; keeping `expo` under an amendment stays open to you (issue 1).

<details><summary>Mediator</summary>

**Recommendation for `bemtpl97`: ship after changes.** One change needs your decision first: `expo` is a free feature, and by LEAK-10 it should become a scoring column. That reverses your own earlier calls (Myunghwan's of 2026-10-23 and 2026-10-26, and Lennart's of 2026-11-04), so it is issue 1. The other changes need no decision.

**Judgment record**

```text
Verdict: ship after changes.
Validity: USE-3, USE-5 hold (the source's own count, every feature except expo known at policy start).
  LEAK-10 triggered by expo: 0.0036-0.0041 of deviance, 16-18% of the skill, comes from using it non-proportionally;
  recommended fix in the definition (LEAK-7): expo as a scoring column (curator decision, issue 1).
  SPLIT-8 holds (IID, ForcedIIDFromTemporal, approximate, disclosed). PROV-9/PROV-10 triggered, fixed in metadata
  (first public copy 2019-09-26).
Value: MET-1, MET-5, MET-11, MET-13 hold (the source's Eq. 5, floor 1e-6); MET-2 holds fully only after issue 1.
  TP-2: real signal, 4.2-4.4% skill with expo free, 3.7% with expo as offset only, 9/9 folds both ways.
Quality: CLEAN-14 holds; the int32 postcode is a panel-kit parquet artifact, not the definition.
Weighed: none decides; restoring the 19 rows is a minor weighing call (issue 3).
For the curator: issue 1, the fix (b) or a LEAK-10 amendment (a), decided for bemtpl97 and fremtpl2 together.
```

**Changes to make now (no decision needed)**

1. **Year and citation (PROV-9, PROV-10, Must).**
   - Set `year = "2019"` in `dataset.py` and in the record's front matter.
   - Add `katrienantonio/PE-pricing-analytics`, commit 0b279c43 of 2019-09-26, file `data/P&Cdata.txt`, to the bibtex and the year note.
   - Keep treeML/CASdatasets as the download (PROV-8).
2. **The 19 removed policies (EV-2, USE-5 note).** Replace "most likely removed" in `fit_reason` and `curation_comments` with the verified fact: the release is the 2019 file minus exactly its 19 rows with an average claim cost above EUR 81,000 (21 claims, 0.1% of claims), the other rows identical and in order. Add a record line saying the 2026-10-26 "unverified" sentence is outdated.
3. **The `known` field is wrong (EV-2).**
   - It says "longer coverage gives more opportunity for claims". Per insured year, part-year policies claim 1.6-2.3x as often as full-year ones (0.292 at expo ≤ 0.25 against 0.126 for a full year).
   - Name both causes the source gives for a part year: a start during the year, or a surrender (arXiv v3, Sec. 4.1, p. 14).
   - The rest of the `expo` wording follows issue 1.
4. **SPLIT-8 note (SPLIT-22, writing).** Add "the raw order is sorted by postcode, so no row-order window exists".
5. **Record corrections (records.md, writing.md).** Append AI lines; do not edit old lines.
   - The 2026-11-04 AI line "Exposure is an offset" was false as shipped.
   - "No panel ran for this dataset" is outdated.
   - The CC "20 other forced-IID definitions" should read 17.
   - "Machine epsilon" is superseded by 1e-6.
6. **Create `datasets/_dev/tabarena-v0pt2/bemtpl97/REVIEW.md` (pipeline).** The record cites "REVIEW.md issue 1", but the file has never existed in git. It should hold issues 1-4 below.
7. **fremtpl2 `dataset.py` line 136.** Change "floors a predicted mean at machine epsilon" to 1e-6, which its params already use.
8. **Bookkeeping.**
   - Add both siblings to the SPLIT-8 Cases table in `splits.md`.
   - Your decision line on issue 1 should carry `LEAK-10`. The register shows no flag only because the `expo` lines have `rule_ids: []`.
9. **After the changes, rebuild on your ask (rebuild.md).** The build is stale and the container is not in the local warehouse. Then check:
   - `postcode` is a category in the container;
   - after issue 1, `expo` is a scoring column and not in `feature_columns`;
   - the dummy re-scores 0.551735, and LightGBM about 0.531 under (b).

**Issues for the curator, ranked**

**1. `expo` as a free feature (P4, LEAK-10 Must; a consistency check of case 1, also for fremtpl2).**
- **Problem.** `expo` is the realized time insured, which falls inside the outcome's period. Conditional on all covariates and a proportional offset, part-year rows claim about 1.4x what is expected (column auditor), and the free log(expo) slope is 0.45-0.54, not 1.
- **Effect.** Using `expo` freely instead of as an offset gains 0.0036-0.0041 of deviance, 16-18% of LightGBM's skill. Four agents measured this independently. The task gamer mapped its exploit #1 to the existing "Potential leak, kept on purpose" note. That makes it a known exploit, but the note states only the proportional signal (log(expo) alone: 0.5470 against 0.5517), not this gain. So it counts as an issue.
- **Can the mechanism be settled?** No. There are no dates in any copy, the 2019 one included.
  - Advocate's best case: new entrants (bm = 11) have O/E 3.36 at expo ≤ 0.1, and a mid-year start is known at quotation.
  - Critic's best case: existing policyholders (bm ≠ 11) still reach O/E 2.13 at expo ≤ 0.1, and over all part-year rows bm = 11 gives 1.39 against 1.41 for the rest.
- **Which rule wins.**
  - LEAK-10's window clause: a value in the outcome's period "still goes". Its late-pull clause: values whose cells "cannot be located row by row… go when they may carry a gain".
  - LEAK-38 does not apply. `expo` is a named field in a research release, not an anonymised competition field, and a conditional test has measured the mechanism.
  - LEAK-11 does not apply, because `expo` strengthens the signal.
  - This is not a conflict: the fix also satisfies MET-1, MET-5 and MET-2 better. By the ladder, fix the definition. Both sides now agree on this, and the advocate withdrew the amendment as the preferred route.
- **The fix.** `expo` becomes a scoring column; the model predicts annual frequency f(x), and the scorer computes deviance(nclaims, expo·f(x)), the source's Eq. 5. Proportional exposure stays (0.5314 against 0.5361 without expo), and the skill stays at 3.7% with 9/9 wins. It needs an exposure input in `_poisson_deviance` with tests, in the same change (MET-13).
- **One fact I measured, which sets the form.** The unweighted mean of d(y, e·g) equals the expo-weighted mean of d(y/e, g) times Σe/n, a constant per fold (ratio 0.5036 = 1/1.9855 on synthetic data). So scoring the target `nclaims/expo` by Poisson deviance weighted by `expo` ranks every model the same.
  - Form (i) keeps the count target but needs models to take an offset.
  - Form (ii) annualizes the target but works with any model that takes a sample weight.
  - Pick the form your harness can pass to models at fit time.
- **Settled in passing:** the advocate's 0.983 is a per-policy rank correlation and says nothing about the leaderboard (critic is right). It does not matter, because a Must does not depend on how much the ranking moves.
- **Your decision:**
  - (b) apply the fix to bemtpl97 and fremtpl2 together. This is recommended; the cost is the part due to mid-year starts, which cannot be separated without dates.
  - (a) keep `expo`, which needs a LEAK-10 amendment (a Must takes no exception), and the note rewritten with both causes, 16-18% of the skill and O/E about 1.4.
- **What would settle the mechanism:** policy start and end dates.

**2. Shipped rows: 163,212 or all 163,231 (P5/P3, USE-5 Weigh; a minor weighing call).**
- **Problem and effect.** The release dropped 19 policies by their claim cost, an outcome. They are all claimants, with 21 claims (0.1%).
- **For keeping 163,212** (both sides): these are the rows the metric's paper evaluated (Sec. 4.1); the removal is the source's preprocessing; under USE-8 a selection alone does not change the fit.
- **For restoring:** the unselected origin exists (the 2019 copy), so the selection can be undone (PROV-13 spirit).
- **Recommendation and decision needed:** keep 163,212 and state the selection as a fact. Your call.

**3. `sex` "stays by curator choice" (no rule covers it; attribution).**
- **Problem.** No CC line in the record states this choice. The definition attributes it to a curator anyway.
- **Effect and evidence.** The domain practitioner notes gender-based pricing is banned in the EU since 2012 (CJEU C-236/09). Keeping it as research on a 1997 tariff is fine if it is disclosed.
- **Decision needed:** confirm in a CC line, or the attribution is marked as an AI draft.

**4. `postcode` with integer categories (P7, CLEAN-14; optional).**
- **Problem.** A plain parquet round trip turns integer categories into integers, which is why the panel kit shows int32. The container restores the categories from `categories.json`.
- **Effect.** A reader without Data Foundry sees numbers.
- **Decision needed:** whether to store the categories as strings (cheap and safe), or leave them.

**Agreed facts**

- **Rows and target.** 163,212 rows, `id` unique. Counts 0-5 (144,936 zeros). `expo` runs from 1/365 to 1, and 77.3% of rows have a full year. 13 features.
- **Folds.** 9 folds of 108,808 train / 54,404 test.
- **Columns.** CASdatasets equals the treeML rds (0 differing cells). Dropping `id`, `claim`, `amount` and `average` is right. Every feature except `expo` is "registered at the start of the policy period". Dtypes are right (CLEAN-14).
- **Metric.** It is the source's mean Poisson deviance (arXiv Eq. 5, Sec. 4.5; treeML.Rmd L641-657). The 1e-6 floor sits about 2.6 orders below the smallest plausible mean.
- **Scores.**

  | model | mean deviance |
  |---|---|
  | dummy | 0.551735 |
  | LightGBM, expo free | 0.5274-0.5285 (9/9 wins) |
  | LightGBM, expo as offset only | 0.5314 |
  | LightGBM, no expo | 0.5361-0.5367 |

  A random column moves the score by 0.0001-0.0004.
- **Split.** No dates in any copy, so IID is forced (SPLIT-8). The raw order is sorted by postcode. Holding out whole municipalities costs at most 0.002 skill. Exact feature twins across the split are 0.12-0.15% of test rows, with label agreement at chance (0.793 against 0.799).
- **Copies.** 133 exact copies and 35 conflicting rows, both INFO.
- **Provenance.** The 2019-09-26 public copy has 163,231 rows. The release equals it minus exactly the 19 rows with an average claim cost above EUR 81,000.
- **The rest of the task gamer's finds** add nothing new:
  - Counts over train and test rows together (LEAK-30) gain 0.0002, inside the noise band.
  - Looking rows up in the public source is not a task flaw.
  - Row order, splits and format features are clean.
  - Nothing hurts an honest model.
- **Settled as moot.** The blind reviewer's RMSE points do not apply: the definition already scores by deviance. Its int32 postcode point was made on the kit artifact.

**Consistency with precedent**

- **Follow precedent:**
  - SPLIT-8 forced IID: the 19 tagged definitions, all approximate.
  - The MET-13 floor, the same as fremtpl2.
  - Kept copies: hiva_agnostic, fremtpl2.
  - Dtypes: house_sales `zipcode`, fremtpl2.
  - The source's metric: the zillow_prize tension row.
- **Departs from precedent, and the fix (b) restores it:** keeping `expo` as a free feature.
  - LEAK-10 window clause: account_debt_south_africa, where values were kept only because the residual AUC was at chance.
  - Unlocatable gain: distribution_transformers_at_cauca_department.
  - A conditional test measured the mechanism, so LEAK-10 and not LEAK-38 applies: kick, expresso_churn_prediction.
  - hotel_booking_demand: `BookingChanges` dropped.
- **What sets this recommendation apart from your earlier keep:** the conditional test is new. The keep rested on the log(expo)-only fit, which measures only the proportional part.
- **Siblings.** fremtpl2 has the same mechanism (slope 0.62; deviance 0.2428 with the offset against 0.2407 free), so decide the two alike (consistency rule 2).
- **Year.** The precedent checker called "2020" consistent with PROV-9 before the 2019 copy was found. A measured fact wins (EV-2), so this departure is explained.

</details>

<details><summary>Claim audit</summary>

**bemtpl97 claim audit (2026-11-04)**

**Focus question:** `focus.md` asks no extra question beyond the standard panel. Its pointers are settled below:
- **(2)** I re-ran the deviance skill with the shipped scorer: dummy 0.551735, LightGBM-Poisson 0.527420, 9/9 wins.
- **(4)** The definition's frame types `postcode` as category. The int32 is in the panel kit and clean room only.
- **(5)** I opened the arXiv paper and the binning manuscript, and all quoted passages hold.
- **(6)** The 2018 SAJ paper did not publish the rows. A 2019 public copy did (refutation R2).

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 3, 34, 35, 36 | 163,212 distinct holders; id unique; expo in [1/365, 1]; counts 0-5; 144,936 zeros | dataset.py, warnings | Loaded raw through `dataset_io.from_definition(raw=True)` | holds | Counts 0:144,936, 1:16,539, 2:1,556, 3:162, 4:17, 5:2. Expo runs 0.00274 to 1; 77.33% full-year. | PROV-13 |
| 17 | CASdatasets rda equals the treeML `mtpl_data.rds` | curation_comments | Downloaded the rds at 2ee8accc and compared all 18 columns | holds | 0 differing cells | PROV-8 |
| 22, 55, D | The metric is the source's mean Poisson deviance of the count against e·f(x), unweighted | metric spec, record | Read the arXiv text (pdfminer) and treeML.Rmd L641-657 | holds | Sec. 3.2 Eq. 5: "f(xi) is replaced by ei·f(xi)". Algorithm 3 tunes on "loss function L". Sec. 4.5: "We evaluate the Poisson deviance … on the holdout test data". Rmd: `dev_poiss(nclaims, .x*expo)`. Fig. 10 range is 0.528-0.538, the same scale as ours (LightGBM 0.5274). Sum versus mean ranks models the same on a fixed fold. | MET-1, MET-3, MET-5, MET-11 |
| D (MET-2) | Computable on every fold; no scoring column needed | task.json | `scorer()` with a train-mean dummy on all 9 folds; counted positives | holds | Dummy 0.5460-0.5557, mean 0.551735. 5,899-6,191 claimants per test fold. The target, classes and balance are the source's. | MET-2 |
| 24 | Floor 1e-6; NaN and inf raise; one day at 3% is about 1e-4 | curation_comments | Called `_poisson_deviance` directly | holds | All-zero prediction scores 3.21 (26.56 on a toy case). NaN and inf raise ValueError. 0.03/365 = 8.2e-5. | MET-13 |
| 54 vs 56 | The first CC on 2026-11-04 says the scorer floors "at machine epsilon" | record | Compared with the spec | inconsistent wording | The spec says 1e-6. The later CC supersedes the earlier one, but the record contradicts itself. | writing.md |
| 18 | Binning manuscript Sec. 2: "registered at the start of the policy period…" | curation_comments | Opened the manuscript | holds | Verbatim match at manuscript line 154 (Sec. 2) | USE-3, LEAK-1 |
| 20 | `expo` can record a later cancellation; it is kept "as the exposure the source puts into the expected count" | curation_comments, fit_reason | Annualised frequency by expo bin; LightGBM-Poisson ×9 folds with expo free, as an offset only, offset plus a full-year flag, and no expo | first half holds; second half **refuted** | See R1 | USE-3, LEAK-10, LEAK-2 |
| 7 | "Longer coverage gives more opportunity for claims" | task_summary.known | Claimant share by expo bin | **partly refuted** | Claimant share by bin: 3.8%, 8.1%, 10.9%, 17.4% (0.75 to <1), 11.5% (full year). Part-year holders claim more per insured year. | USE-3 |
| 21 | log(expo) Poisson scores 0.5470 against the mean's 0.5517 | curation_comments | PoissonRegressor ×9 folds | holds | 0.547002 vs 0.551735; slope on log(expo) is 0.453 | EV-1 |
| 11, 27, 49 | The release "most likely" dropped the 19 policies with average above EUR 81,000 | fit_reason, record | Compared row by row with the 163,231-row 2019 copy | holds, now **certain**; the old "unverified" line is outdated | The release equals the 2019 file minus exactly its 19 rows with AVG > 81,000, in order. All 15 compared columns are identical; only the ids are renumbered. Manuscript p. 11: "For 19 records the average claim cost exceeds this threshold" (18,295 → 18,276). The 19 rows hold 21 claims (17×1, 2×2). Release max average is 80,499.6. | PROV-13, USE-5 |
| 12, 29 | Year 2020 is "the earliest public copy found" | curation_comments, metadata | GitHub commit history; downloaded the copy | **refuted** | See R2 | PROV-8, PROV-9 |
| 16 | The bibtex names the work that published the data | bibtex | Read the SAJ manuscript footnote; looked for the first public release | **refuted (minor)** | The SAJ paper shares no rows (footnote 1 only cites earlier samples). The first publication is the 2019 course repository, which is missing. | PROV-10 |
| 25 | `coverage` ordered TPL < TPL+ < TPL++; `postcode` nominal | curation_comments | Definition frame dtypes; the arXiv appendix | holds | coverage is an ordered category, 95,124 / 45,984 / 22,104. The appendix defines TPL+ as limited and TPL++ as comprehensive damage; the 2019 file codes them TPL/PO/FO. postcode is a category with 583 levels and 583 unique lat/long pairs. The int32 in `participant_kit/` and `clean_room/` comes from the panel tooling, not the definition. | CLEAN-14 |
| 26, 33 | 133 exact duplicate rows, 35 conflicting profiles, all kept | curation_comments | Recounted | holds | 133 / 35; 168 duplicate feature profiles | LEAK-16 |
| 28, 8 | No dates exist, so the split is forced IID | splits | Read the header of the 2019 origin as well | holds | No date column in any copy (18 columns, plus TOWN in 2019) | SPLIT-8 |
| 30, 31 | 3×3 CV, 108,808 train / 54,404 test; municipalities recur | splits_comment | Read `make_splits()` | holds (seed mechanics untested) | 9 splits with these sizes | SPLIT-1 |
| 45, 48, 50 | Builder scores: dummy 0.551735, LightGBM 0.528534, 9/9 wins | record | Independent LightGBM-Poisson run | holds | Dummy exactly 0.551735. My LightGBM scores 0.527420 (4.41% skill), 9/9 wins. | TP-2, EV-8 |
| 37, 39 | CASdatasets page facts; fremtpl2 is a different portfolio; no other Belgian record | record | Raw shape; grep of the records | holds | 18 columns. `eumtpl` lists bemtpl97 as a sibling, not a duplicate. A third derivative exists (maidrr `mtpl_be`, 163,210 rows) but has no record. | PROV-7 |
| 13 | Licence GPL (>= 2), insurer terms unknown | metadata | none | untested | Not a verdict reason | EV-4 |
| 53, 57 | The build reproduces | record | Tried to load the built container | untested | `01a18ad7…/dataset.parquet` is missing from the local warehouse, and the README says `build_stale: true` | EV-7 |

**Implied claims.**
- Every feature except `expo` is known at the start of the policy. This holds: `bm` is "registered at the start" (arXiv App. A), and long/lat follow from postcode.
- Exact copies across the split: 0.1% (probe 5).
- The target is the source's own count, not a proxy.

**Refuted and untested, ranked (validity first, Must first)**

**R1. P4, USE-3 / LEAK-10 (Must, graded by severity). Claim 20, second half, and claim 7.**
- **What the source does:** it puts exposure in proportionally, with the slope fixed at 1. The arXiv paper replaces f(x) by e·f(x), the treeML GBM uses `offset(log(expo))`, and the binning GAM (manuscript line 403) makes the count "proportional to the exposure".
- **What the benchmark does:** it ships `expo` as a free feature.
- **What the data shows:**
  - The fitted slope on log(expo) is 0.45, not 1.
  - Annualised frequency is 0.292 for expo ≤ 0.25, 0.240 for 0.25-0.5, 0.198 for 0.5-0.75, 0.233 for 0.75 to <1, and 0.126 for full-year policies.
- **What the free use is worth:**

  | LightGBM variant (9 folds) | Mean deviance | Skill over dummy |
  |---|---|---|
  | expo as a free feature | 0.527420 | 4.41% |
  | log(expo) as offset only | 0.531395 | 3.69% |
  | no expo at all | 0.536896 | 2.69% |
  | offset plus a full-year flag | 0.527505 | 4.39% |

  - Using expo freely gains 0.0040 deviance over the offset, about 16% of the model's skill.
  - The full-year flag alone recovers almost all of that gain.
- **Why it matters:** this non-proportional excess is the channel a cancellation after a claim would leak through. Without dates I cannot separate surrender after a claim (post-outcome) from mid-year starters (known at quotation).
- **What it changes:** the "kept on purpose" note understates the size, and its justification ("the exposure the source puts into the expected count") is inaccurate.
- **Mildest remedy:** keep the curator's decision but rewrite the note with these numbers. The text "longer coverage gives more opportunity" should say that claims are proportional to exposure within a policy, while part-year holders claim at 1.6-2.3× the annual rate.
- **Stronger option, for the curator:** ship `expo` as a scoring-column offset instead of a feature. This is a weighing call.

**R2. P5, PROV-8 / PROV-9 / PROV-10 (Must). Claims 12, 29 and 16.**
- The full portfolio (163,231 rows, 18,295 claimants, 20,236 claims, mean 0.1239715) has been public since 2019-09-26. It sits at `github.com/katrienantonio/PE-pricing-analytics`, commit 0b279c43, file `data/P&Cdata.txt`, in KU Leuven course material that ships the SAJ 2018 PDF.
- The treeML release (2020-04-30) and CASdatasets (added 2024-05-29, c86358f9) are both its large-claim-filtered cut.
- **What it changes:** the year should be 2019. The citation and source note should name this first public release. The download can stay as it is, since PROV-8 lets the download copy differ from the source.
- **Mildest remedy:** set `year = "2019"`, add the course repository to the notes and the bibtex, and keep the treeML entry as the release that was shipped.

**R3. P5 / P3, USE-5 (Weigh). Not a refutation; claims 11 and 27 are now proven.**
- The 19 policies removed for severity reasons hold real frequency rows: all are claimants, 21 claims in total, 0.1% of claims. The removal conditions on the outcome.
- The unselected origin exists (R2), so the selection is reversible.
- **What it changes:** "most likely" becomes a fact. The record's 2026-10-26 line ("removal of whole policies unverified") is outdated.
- **Mildest remedy:** reword the note. Shipping all 163,231 rows from the 2019 copy is a curator call; it would drop the selection limit but move away from the release the metric paper used.

**R4. Procedure (writing.md).** The first CC of 2026-11-04 says "machine epsilon", while the spec and the later CC say 1e-6. Mildest remedy: leave both, since the newer CC wins, and the next record edit notes the supersession.

**Untested:**
- **Build reproduction (claims 53, 57).** The container files are not in the local warehouse and the build is stale, so the shipped dtypes cannot be compared. This changes nothing until the curator rebuilds.
- **Licence (claim 13).** Never a verdict reason (EV-4).
- **Split-seed mechanics (claim 30).**
- **Deprez et al. 2026 (claim 39).** External and not material.

**Judgment record:**
- **Verdict:** ship after note and metadata changes.
- **Validity:** USE-3 holds and LEAK-10 is a documented potential leak whose stated size and justification are understated (R1). PROV-9 and PROV-10 are triggered and fixable in metadata (R2). SPLIT-8 holds.
- **Value:** MET-1 to MET-3 and MET-5 hold, the metric is the source's, and TP-2 shows real signal (4.4% deviance skill, 9/9 wins).
- **Quality:** CLEAN-14 holds.

Sources:
- [arXiv 1904.10890v3](https://arxiv.org/abs/1904.10890v3)
- [treeML.Rmd L641-657](https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd#L641-L657)
- [Binning manuscript](https://roelverbelen.netlify.app/publication/binning/binning.pdf)
- [katrienantonio/PE-pricing-analytics 2019 page](https://katrienantonio.github.io/PE-pricing-analytics/background/2019_04_APC_Pricing_analytics_in_R.html)
- [maidrr mtpl_be](https://rdrr.io/github/henckr/maidrr/man/mtpl_be.html)

</details>

<details><summary>Column audit</summary>

Focus question: `focus.md` adds no question beyond the standard panel. On its pointers: postcode is not a defect in what ships (#2 below), and I re-ran the Poisson deviance (#1). That re-run found a measured case for the `expo` timing concern. No column needs a new drop or recode for cleaning, but `expo` goes back to the curator with new numbers.

**Column table (cleaned frame: 163,212 rows, 13 features plus the target)**

Meanings are from the CASdatasets help page (fetched). Prediction point: the quote at policy start.

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| nclaims (target) | "claim number" | target | Int32, 0-5 (144,936 / 16,539 / 1,556 / 162 / 17 / 2), no missing | fine | CLEAN-15/16 (count kept raw by curator) |
| expo | "exposure": share of 1997 insured | **partly no**: its length can come from a cancellation during the year | float64, 365 values (days/365), 1/365 to 1, 77.3% equal 1 | **question for curator: measured leak mechanism** (#1) | LEAK-10, LEAK-38, LEAK-7 |
| coverage | TPL / TPL + limited material damage / TPL + comprehensive damage | yes, set at the start | ordered TPL<TPL+<TPL++; this matches the codebook (the coverage adds up). Claims per exposure-year 0.146 / 0.128 / 0.135 (not monotone, which does not matter: the order comes from meaning) | fine | CLEAN-14 |
| ageph | policyholder age | yes | Int32, 18-95, no impossible values | fine | CLEAN-14 |
| sex | female/male | yes | category, 2 levels | fine (kept by curator for research on a 1997 tariff) | SEL-1 weigh |
| bm | level on the Belgian bonus-malus scale, 0-22, higher is worse | yes (level at the start) | Int32, all 23 levels present; a scale with no words per level, so numeric is right | fine | CLEAN-14 |
| power | horsepower in kW | yes | Int32, 10-243; 192 rows under 20 kW are unusual (microcars), not impossible | fine | CLEAN-11 |
| agec | vehicle age in years | yes | Int32, 0-48 | fine | CLEAN-14 |
| fuel | gasoline/diesel | yes | category | fine | |
| use | private/work | yes | category | fine | |
| fleet | "1 or 0", vehicle is part of a fleet | yes | category '0'/'1' | fine (the flag form CLEAN-12's table asks for) | CLEAN-12/14 |
| postcode | policyholder's postal code | yes | category, 583 levels (1000-9990). The dtype probe flags it `numeric_levels`; nominal is right. It maps one-to-one onto (lat, long) pairs, 583 to 583 with 0 conflicts | fine (#2 note) | CLEAN-14, CLEAN-5 weigh |
| long | longitude of the municipality centre | yes | float64, 583 values | fine | |
| lat | latitude of the municipality centre | yes | float64, 583 values | fine | |
| id (dropped) | policy number | n/a | raw probe R2 -0.0006 | dropping is right | CLEAN-3 |
| claim, amount, average (dropped) | outcomes of the same period | no | raw probe R2 about 0.90 each | dropping is right | LEAK-10 |

I re-ran the dtype probe. It flags 1 of 13 columns (postcode); answered above. No proxy missing codes (0 NaN in every column), no impossible values, no reversed encodings.

**Problems, ranked**

**1. P4, `expo`: the timing concern is now measured, not just suspected (LEAK-10 Must against the kept-on-purpose note under LEAK-38; question for the curator).**

The definition's evidence is "log(expo) alone 0.5470 vs mean 0.5517". That only measures the legitimate part, where more insured time means more claims. It does not test cancellation. I tested it conditionally. LightGBM Poisson on the 12 other features, with log(expo) as an offset (claims proportional to exposure, as in the source's models), on the 3 folds of repeat 0:

- Observed/expected claims by exposure band, `(0,.25]`, `(.25,.5]`, `(.5,.75]`, `(.75,.999]`, full year: **1.77-1.86, 1.38-1.61, 1.17-1.34, 1.43-1.47, 0.92-0.93**. Policies with part of a year insured claim about 40% more than their covariates and exposure predict.
- In the raw counts, policies with 0.75-0.999 years insured have a claimant share of **17.4%**, against **11.5%** for full-year policies, despite less time at risk.
- New business (a mid-year start) does not explain it. Proxies for new business have the same excess as the rest. For part-year rows, bm=11 (the entry level) gives O/E 1.39 against 1.41 for the others. bm=0 (long-standing policyholders, so no new start) gives 1.29. Cars up to 1 year old give 1.21 against 1.43. This fits contracts that ended after a claim (a total loss, or a cancellation by the insurer or the policyholder).
- Mean Poisson deviance on the same folds:

| setup | deviance |
|---|---|
| training-mean dummy | 0.5505 / 0.5506 / 0.5541 |
| no expo | 0.5361 / 0.5338 / 0.5388 |
| expo as offset only | 0.5313 / 0.5289 / 0.5333 |
| expo as a free feature (the shipped setup) | 0.5278 / 0.5248 / 0.5292 |

- The gain beyond proportional exposure is **0.0036-0.0041**, about **16-18% of the model's skill** over the dummy (0.0227-0.0249). This gain is where the cancellation signal lives.
- LEAK-38 says that once a conditional test measures the mechanism, LEAK-10 applies. Here it is circumstantial, because the policies carry no dates, and the proportional part of `expo` is legitimate. So this is the curator's call, not an automatic drop.

Remedies, mildest first:
- (a) Keep `expo`, but replace the note's numbers with these: about 16-18% of the skill from non-proportional exposure, O/E about 1.4.
- (b) Recommended, and closer to the source: make `expo` a scoring column, not a feature. The model predicts an annual frequency, and the scorer computes the deviance of nclaims against expo × prediction. This is exactly the source's Eq. 5 and treeML.Rmd L641-657 (frequency times expo). The source's models only ever use exposure as an offset, so they cannot learn the 1.4× excess. The free feature can. The target stays the original nclaims and the metric is unchanged. It needs a library metric that takes an exposure scoring column. It also reverses two things the definition says now: "neither a weight nor a scoring column", and Myunghwan's no-offset choice of 2026-10-23.
- (c) Drop `expo`: this loses the legitimate exposure scaling.

freMTPL2 carries the same note ("about a fifth of the gain"), so treat the two alike (principles.md consistency rule 2).

**2. P7, postcode in the panel kit (no defect in the shipped data; focus pointer 4).** The definition types it as a category; it has integer categories. A plain parquet round trip turns that into an integer (I reproduced this: Categorical[int] read back as int64). That is why `clean_room/data.parquet` and `participant_kit/data.parquet` hold int32. The container restores categories from `categories.json` (`src/data_foundry/curation_container.py:363-388`), so the shipped data stays categorical. Two effects remain:
- A reader without Data Foundry gets numbers. Optional remedy: make the categories strings.
- The kit's blind reviewer and task gamer saw postcode as numeric. This matters little, because it is one-to-one with (lat, long), and under CLEAN-14 the digits of a postcode carry meaning anyway (Belgian postcodes are numbered by area, so close codes are close places).

**3. P7, minor and no action needed.**
- `power` has 192 rows below 20 kW: unusual, so it stays (CLEAN-11).
- `postcode` repeats the information in long/lat. It is not an exact copy, so it stays (CLEAN-5 weigh). The source uses both.

No other column is wrong for the prediction point. bm, coverage, use and fleet are "registered at the start of the policy period" (the binning manuscript, p. 4, as quoted in the definition; I did not open the page myself).

**What I did not verify**
- I ran only repeat 0, so 3 of the 9 folds.
- The arXiv Eq. 5 and the binning manuscript's p. 4 and p. 11 quotes are unopened.
- The built container (`01a18ad7…`) is not in the local warehouse, so the categorical restore of postcode is confirmed from the code, not from the built file.

</details>

<details><summary>Split audit</summary>

**Split audit for `bemtpl97`. Verdict: right, with notes.**

**The question in `focus.md`:** it asks nothing beyond the standard panel. Pointer (1) says no group probes ran because the task is IID, so I ran the grouped alternatives myself. They do not change the regime. The IID split with the `ForcedIIDFromTemporal` tag is the right choice, it matches freMTPL2 (SPLIT-8, Lennart 2026-11-04), and no re-split, gap or filter is needed.

**Regime against the use case (P3/P4, SPLIT-1, SPLIT-8, USE-10/11)**
- The use case is an insurer that fits on past policy years and prices the next year, so the task is temporal by nature. The release is one undated year (1997), so no window can be built. Under SPLIT-8 it ships IID with the tag, the fit is `approximate`, and the notes say what a dated year would change and that it should be recovered. That meets SPLIT-8's documentation requirement.
- The entity question: there is one row per policyholder (`id` is unique, 163,212 rows) and one year. Claim history enters through `bm` (bonus-malus) as a feature, not as an earlier row. So holding out random policyholders is the correct entity regime (USE-11 pattern). The `splits_comment` claim "test customers are unseen, while municipalities may recur" is accurate.
- **The raw order is not time (SPLIT-22), checked.** `id` equals the raw position plus 1 on every row, and `postcode` never decreases in raw order (0 violations). The file is sorted by municipality. Within a municipality the order does not follow the outcome: the mean within-postcode Spearman correlation with position is -0.008 for `nclaims` and +0.006 for `expo`. Over within-postcode quintiles, the claim share runs 0.113, 0.117, 0.111, 0.109, 0.110. The only notable within-postcode trend is `power` at -0.15, which looks like a secondary sort key. So, unlike freMTPL2 (whose blocks stood in for years), no proxy window exists and the SPLIT-8 cost cannot be measured. The definition's statement of this is correct.
- Temporal items (time column meaning, windows, gap against label delay, unmatured training labels, season-shaped window): none apply because there is no time column. One caveat that cannot be measured: claims from late in 1997 may have been reported after the extract (a reporting delay). Without dates this cannot be tested. It belongs to the same "recover a dated release" note, not to a remedy.

**Alternative splits I ran.** Model: LightGBM Poisson, 400 trees, learning rate 0.03, 31 leaves, `min_child_samples=200`, untuned. Each split has 9 folds. Scored by the shipped metric (mean Poisson deviance, predictions floored at 1e-6). Skill is 1 minus model deviance over the train-mean dummy's deviance.

| split | features | model deviance | dummy deviance | skill (min to max) | wins |
|---|---|---|---|---|---|
| shipped IID 3x3 | all 13 | 0.53472 | 0.55173 | 0.0308 (0.0273 to 0.0343) | 9/9 |
| grouped by `postcode`, 3x3 | all 13 | 0.53119 | 0.55174 | 0.0372 (0.0366 to 0.0383) | 9/9 |
| shipped IID 3x3 | without `postcode` | 0.52678 | 0.55173 | 0.0452 (0.0416 to 0.0485) | 9/9 |
| grouped by `postcode`, 3x3 | without `postcode` | 0.52787 | 0.55174 | 0.0432 (0.0403 to 0.0475) | 9/9 |
| leave out first postcode digit (9 regions) | without `postcode` | 0.52562 | 0.54715 | 0.0389 (0.0311 to 0.0569) | 9/9 |

- Holding out whole municipalities costs at most 0.002 skill (0.0452 to 0.0432, with the same features). Holding out whole regions still keeps every fold above the dummy. Location adds no hidden-group optimism. This agrees with the hidden-group probe: `postcode` gap +0.0013 (fold sd 0.0029), `lat` +0.0036, `long` -0.0006, no hit.
- Under SPLIT-4 the municipality is a feature, not a group. All 583 municipalities in the data recur in every fold, and a new policy always has a known municipality. Belgium has about 589, so there is no cold-start municipality to test. No re-split (SPLIT-4, SPLIT-30).

**Hidden groups and near copies (SPLIT-29/30)**
- 335 rows sit in 166 repeated full feature profiles, the largest holding 3 rows. Over 169 within-profile pairs, labels agree at 0.793 against 0.799 by chance. These are coincident coarse profiles, not one entity. Almost all are full-year rows (98.8% have `expo` == 1, against 77.3% overall).
- Test rows with an exact feature twin in the training side: 80, 81 and 64 per fold (0.12% to 0.15%).
- Rows that share every feature except `expo`: 763 (0.47%).
- The probe's near-copy check was not run on 147,308 rows, as `focus.md` notes. The label-concordance test above covers the exact-profile part of that gap and finds nothing.

**Problems, ranked (P4 first, then strength)**

1. **P4, SPLIT-8 / SPLIT-7 (Must, satisfied; a disclosure note, no fix).** The forced-IID cost cannot be measured: there are no dates and the raw order is sorted by postcode. The definition already says so.
   - Mildest remedy: none now. Recover a dated year if a later release has one, as already stated.
   - One wording fix for the `curation_comments` SPLIT-8 bullet: add "the raw order is sorted by postcode, so no row-order window exists". This saves the next auditor from looking for freMTPL2-style blocks.
2. **P4, SPLIT-1 together with LEAK-10 (Should; the leak itself belongs to the leak auditor).** `expo` is realized exposure. Under the true next-year use case it would not be known at quotation, so the IID split and the kept `expo` share one approximation.
   - Measured size: the exposure-only offset baseline (training frequency times `expo`) scores 0.55072 against the dummy's 0.55173, a 0.18% improvement. The definition's log(`expo`) Poisson figure (0.5470 against 0.5517) is consistent with this.
   - Small, already disclosed with a "Potential leak, kept on purpose" note. No split remedy.
3. **Not a split defect, an observation for the column auditor (P6/P7, CLEAN).** With `postcode` as a 583-level nominal feature, untuned LightGBM under the shipped split loses 0.014 skill against dropping the column (0.0308 against 0.0452), because `lat`/`long` already carry the location.
   - The nominal type is correct for a postcode (dtype decided from context, never from model runs), so I propose no change.
   - The same models lose nothing under the grouped split, which shows the drop is overfitting on categories, not a leak or a hidden group.
   - Relevant to the `focus.md` pointer (4): if the kit ships `postcode` as int32, the participant sees a different encoding from the one the README declares.

**What I checked against the record:** 9 folds, each 108,808 train / 54,404 test, with no index overlap. The builder's LightGBM deviance of 0.52853 against the dummy's 0.55173 is in line with my 0.52678 (without `postcode`) and 0.53472 (with it).

</details>

<details><summary>Domain practitioner</summary>

**bemtpl97, domain practitioner (claims frequency actuary at a Belgian MTPL insurer). Verdict: approximate fit, metric scores the decision (yes). The dataset is ready from my side. Gap 1 is a design choice the curator has already settled.**

**Focus question.** `focus.md` asks nothing beyond the standard panel. The direct answer is the standard verdict above. From its "things worth a look" list, I answered three:
- **Item 5:** I opened arXiv Sec. 3.2 Eq. 5, Sec. 4.1 and Sec. 4.5 myself.
- **Item 2:** I re-ran the deviance skill on the kit with the source's deviance.
- **Item 4:** postcode, below.

**Fit: approximate (agree with `fit="approximate"`, USE-8)**

The rows, the label and the metric are the source's own frequency-model validation. The test set is not next year's portfolio (SPLIT-8, disclosed), and realized exposure is offered as a free input, where I would only ever use it as an offset.

**The five questions, as the actuary**

1. **Inputs at prediction time.** coverage, ageph, bm, power, agec, fuel, use, fleet, postcode, long and lat are rating factors "registered at the start of the policy period". I have all of them at quotation. `expo` is different (gap 1).
   - What I would always have but is missing: vehicle make, model and value; new business vs renewal; years with the insurer; the policy start date.
   - What I would not have today: `sex`. EU law has banned gender in pricing since 21 Dec 2012 (CJEU C-236/09, Test-Achats). Keeping it as research on a 1997 tariff is fine and is disclosed.
2. **Target.** I act on the annual claim frequency f(x), which goes into pure premium = E(F)×E(S) (arXiv Sec. 2). `nclaims` scored against e·f(x) is exactly how the source validates that frequency (Eq. 5: "f(x_i) is replaced by e_i·f(x_i)"). I want an expected count, a number. The label is not a proxy. The task covers only the frequency half of the premium, which is the standard separate model an actuary builds (USE-5 holds).
3. **Row and test data.** One row is one policyholder-year, which is one premium I set. That matches. The test set is random policyholders of 1997, while I would face next year's book. The drift cannot be measured, and the gap is disclosed under ForcedIIDFromTemporal. The source itself uses 6 stratified random folds within the year (Sec. 3.3), so the benchmark matches the source's own protocol.
4. **Would I use it?** Yes, as a frequency-model benchmark. I would distrust any winner whose gain comes from bending `expo` non-proportionally (gap 1). When I build the tariff I set e = 1 (or the contract term), so I can't use that part of its score.
5. **Metric: yes.** See below.

**Gaps, ranked by how much they change the task**

**1. `expo` is a free feature, not an offset.** This is the largest gap. It is settled by curator choice (Myunghwan 2026-10-23, Lennart 2026-11-04), consistent with fremtpl2, and named as a kept potential leak under USE-8/USE-12. My own run on the participant kit, repeat 0, 3 folds, no tuning:
- **Claims per policy-year by exposure band.** Full-year policies have a frequency of 0.126.

  | expo band | frequency |
  |---|---|
  | ≤0.25 | 0.292 |
  | 0.25–0.5 | 0.240 |
  | 0.5–0.75 | 0.198 |
  | 0.75–0.999 | 0.233 |

  So 22.7% of rows (expo < 1) claim 1.6 to 2.3 times more often per unit of exposure. Exposure is not proportional.
- **Mean Poisson deviance:**

  | model | deviance |
  |---|---|
  | dummy (training mean) | 0.5517 |
  | exposure-proportional rate | 0.5507 |
  | LightGBM, log(expo) offset | 0.5308 |
  | LightGBM, expo as a free feature | 0.5268 |

  About 0.0041 of 0.0249 skill (16%) comes from using exposure non-proportionally. This matches the record's log(expo)-only 0.5470 and fremtpl2's "about a fifth".
- For short policies (expo < 0.5), the free-feature model predicts 1.58 times the offset model's expected count. The two models' annual-frequency rankings correlate at 0.983.
- **Wording is incomplete (claim 20).** The source gives two causes for short exposure: policyholders "who started the policy in the course of the year or surrendered the policy before the end of the year" (arXiv v3 Sec. 4.1, p. 14). A mid-year start is known at quotation; a surrender (often after a claim) is not. `curation_comments` and `known` cite only the surrender. They should name both, which also explains why the effect can't be split without dates.
- **What an expert would change:** ship `expo` as a scoring column. The model predicts the annual frequency f(x), and the scorer computes the deviance of y against expo·f(x). This is the source's formulation and the quantity the actuary prices (USE-5). It removes the cancellation channel and fits MET-2 ("every input it needs ships as a column and is never a feature"). It reverses a settled decision, so I raise it as the strongest alternative for `REVIEW.md` rather than as a blocker.

**2. Random split within one year instead of next year (SPLIT-8).** Disclosed. It changes what is measured (no frequency drift, no bonus-malus transitions) but not the decision, and it matches the source's own CV.

**3. Missing rating factors** (vehicle make/model/value, new vs renewal, tenure, mileage). These are the release's limits, not curation errors. Small effect; a benchmark only needs consistent inputs.

**4. `sex` is a 1997-only input.** Small. A modern practitioner removes it. Disclosed as the curator's choice.

**5. postcode as a 583-level nominal.** No effect on the task, only on models. LightGBM with postcode as a native category scored 0.5405, against 0.5268 with it dropped. The source smooths over lat/long instead (Sec. 4.1). Nominal is the right type (CLEAN-14, dtype probe). Focus item 4: the kit ships postcode as int32 while the README calls it nominal, so a consumer reading the kit dtype treats it as numeric. Worth one line in `REVIEW.md`.

**6. Release selection: 19 high-cost policies removed.** Negligible for frequency: 19 of 18,295 claimants (0.1%). The paper confirms "exclusion of very large claims" in preprocessing (Sec. 4.1). Disclosed; per USE-8 a selection alone does not change the fit.

**Metric: yes, `mean_poisson_deviance` scores the decision**

- **It is the source's metric.** Henckaerts et al. compare frequency models by out-of-sample Poisson deviance with e·f(x) (Sec. 3.2 Eq. 5; Sec. 4.5, Fig. 10, all checked in the v3 PDF). Unweighted, per policy, which is the unit I price (MET-1, MET-5).
- **It is a proper rule.** Poisson deviance is strictly consistent for the mean count, so it scores the expected count the way MET-8 asks of probabilities. Calibration (premium level) and ranking (differentiation) both count, and a tariff needs both.
- **I would not pick the alternatives for frequency alone.** The paper's managerial measures (loss-ratio lift, double lift, Gini of the ordered Lorenz curve, Sec. 5) work on the pure premium, which needs a severity model. Gini also ranks only and ignores the level. They suit the final tariff, not a frequency benchmark. MET-6/MET-7 (threshold or top-k) don't apply: no hard decision is made per policy.
- **The floor `min_prediction=1e-6` is sound (MET-13).** The note's "3% frequency" is conservative. The portfolio's frequency is 0.139 per year, so one day of exposure gives a smallest plausible mean of about 3.8e-4, roughly 2.6 orders of magnitude above the floor. A practitioner clips the same way.
- **One caveat, from gap 1.** Because `expo` enters as a feature and not through the scorer, the deviance also rewards exposure used non-proportionally. Under the offset formulation I would keep the same metric with expo as a scoring column.

**Sources**

- [Henckaerts, Côté, Antonio, Verbelen, arXiv:1904.10890v3](https://arxiv.org/pdf/1904.10890v3): Sec. 2 p. 4 (offset ln(e), pure premium), Sec. 3.2 Eq. 5, Sec. 3.3 (6 stratified folds), Sec. 4.1 p. 14 (163,212 policyholders; exposure from mid-year starts or surrenders; exclusion of very large claims), Sec. 4.5 Fig. 10, Sec. 5 (lift, Gini).
- CJEU C-236/09 (Test-Achats), from my own knowledge; I did not fetch it.
- Not opened by me: the treeML.Rmd lines 641-657, the binning manuscript p. 4 / p. 11 quotes, and the CASdatasets page.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real and widely used Belgian MTPL claim-frequency dataset with an honest IID setup. But it is a Poisson count task with exposure, and the benchmark currently treats it as plain regression with `expo` as an ordinary feature. That framing needs fixing, and the low signal should be understood, before it goes in.

**What the task is.** A motor insurer pricing third-party liability cover predicts each policyholder's expected yearly claim count from rating factors: age, bonus-malus level, the car, and the region. That prediction feeds the frequency part of the premium. This is the standard actuarial frequency model and a real use. The source describes the data in Denuit & Lang (2004) and Henckaerts et al. (2018, Scand. Act. J.). CASdatasets lists 18 columns and 163,212 policies, which matches the file. The preparation dropped `id`, `claim` (whether any claim was filed, which would leak the target), `amount` and `average` (claim cost, which would also leak). That is correct.

**Concerns, most serious first**

1. **Exposure is used as a feature, not as an offset or weight, and it may carry leakage.**
   - Evidence: CASdatasets defines `expo` as "the fraction of the year the policyholder was at risk of filing a claim." 22.5% of rows have `expo` < 1 (minimum 0.0027).
   - Claim rates by exposure band are not proportional to exposure:

     | `expo` band | Claims per policy |
     |---|---|
     | 0.75 to 0.99 | 0.203 |
     | full year (1.0) | 0.126 |

     Part-year policies claim more per year at risk. This pattern fits policies being cancelled or changed after a claim, and that information only exists after the period ends.
   - `expo` adds real predictive power. With LightGBM (Poisson objective, 3-fold), mean Poisson deviance is 0.5276 with `expo` and 0.5367 without it. The no-skill baseline is 0.5517, so `expo` accounts for about 40% of the gain over the baseline.
   - Change: predict claims per year at risk. Either use the target `nclaims/expo` with sample weight `expo`, or keep `nclaims` and pass `log(expo)` as an offset. If the framework cannot do either, drop `expo` from the features, or at least document it as known only at the end of the period.

2. **The problem type and metric do not fit the target.**
   - The target is a small count: 0 is 88.8%, 1 is 10.1%, 2 is 0.95%, and only 181 rows have 3 to 5.
   - Under RMSE/R² every method lands within a hair of the mean predictor:

     | Model | RMSE | R² |
     |---|---|---|
     | Mean predictor | 0.3675 | 0 |
     | LightGBM, L2 objective | 0.3633 | 0.023 |
     | LightGBM, Poisson objective | 0.3631 | 0.024 |

   - Poisson deviance separates models more clearly (0.552 → 0.530 → 0.528). It is also the metric actuaries and the source paper use.
   - Change: score with Poisson deviance, ideally weighted by exposure. If the benchmark only supports MSE, note that it ranks methods on a very compressed scale. Also consider whether a Poisson or count task type is available.

3. **The signal is low, so ranking noise is a risk.** R² of about 0.02 is normal for claim frequency and is not a defect. Still, the differences between strong methods will be small compared with the variation across folds. With 163k rows and 9 splits the scores should be stable enough, but I did not measure the variance across folds.

4. **The geography columns are redundant and `postcode` is encoded as a number.**
   - `postcode`, `long` and `lat` each have exactly 583 unique values. They look one-to-one, since `long`/`lat` give the municipality centre.
   - `postcode` is stored as int32. Belgian postcodes are only loosely ordered by region (the first digit marks the province), so a numeric code is a crude encoding. As a category it would have 583 levels.
   - Change: keep `long`/`lat` as numeric, and either drop `postcode` or mark it as a high-cardinality categorical. The current choice works but is worth documenting.

5. **The split is an assumption.** A single policy year with no dates and no policyholder ID, so random rows are the only option. In practice a tariff is applied to next year's book, so IID is somewhat optimistic, but nothing better is possible here. There are 168 rows whose features duplicate another row's and 133 fully duplicated rows. Given coarse discrete features, these are plausibly distinct policies, and at 0.1% they don't matter.

6. **Minor type issues.**
   - `fleet` is a category with values 0/1. That is fine, though a boolean would be more natural.
   - `nclaims` uses the pandas nullable Int32 type. It has no missing values, but make sure downstream code casts it to float.
   - No column has any missing values.
   - All value ranges are plausible: `ageph` up to 95, `bm` 0 to 22, `power` up to 243 kW, `agec` up to 48, frequency 0.139 claims per year at risk. Claim rate rises with `bm` level, 0.091 at level 0 to about 0.3 at levels 16 to 18, as expected.

**What I could not check**
- Whether part-year exposure really comes from cancellation after a claim. The documentation does not say why exposure is below 1.
- The exact insurer and year. CASdatasets says "unknown insurer," and 1997 is only implied by the dataset name.
- Whether the benchmark framework supports offsets, sample weights or a Poisson metric.
- Variance across folds and repeats.
- The pinned treeML GitHub commit. I read the CASdatasets page but not the repository or the paper's full text.

</details>

<details><summary>Task gamer</summary>

**Verdict:** I found no real leak. The only gameable point is `expo`, the realised exposure, which is only known once the policy period ends. Used as a free feature it is worth 0.0091 of Poisson deviance over a model without it. 0.0039 of that comes from the fact that short policies claim at 1.5 to 3.4 times the per-year rate, which fits policies being terminated after a claim. Nothing else beats the noise.

Honest baseline: untuned LightGBM, Poisson objective, all 13 features, scored on the 9 shipped splits. Mean 0.52753 (per split 0.52259 to 0.53096). A model predicting only the mean scores 0.55173. Adding a random column moves the mean by +0.00014 to +0.00036, and single splits by up to 0.0008. That is the noise band.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | `expo` (realised exposure) as a free feature, not a proportional offset | 0.53146 (expo as offset log(expo) only) | 0.52753 (baseline, expo free) | 0.0039 (0.0032 to 0.0047) | Unclear. Yes if expo<1 means the policy started mid-year (known at start). No if it means it ended early (cancellation, write-off after a claim). | Use the planned period, or force expo to be an offset. Or score claim frequency weighted by expo, as the source does. |
| 1b | `expo` at all, compared with no exposure | 0.53666 (no expo) | 0.52753 | 0.0091 (0.0079 to 0.0105) | The proportional part (0.0052) matches the source's own design. The rest is #1. | Same as #1 |
| 2 | Counts over train and test rows together (rows per postcode, rows per ageph/sex/postcode/power/agec/fuel/coverage) | 0.52753 | 0.52734 | 0.0002 (-0.0002 to +0.0006) | Yes for postcode density. The gain is within noise anyway. | none |

**Flaws that hurt an honest model:** none found. The best honest model, with log(expo) as offset plus expo as a feature, scores 0.52721. That beats the baseline by 0.0003 (0.00001 to 0.0011), which is about the noise band. So the baseline is not being pulled down.

**Findings**

**1. Exposure.**
- **Mechanism.**
  - Overall the per-year claim rate is 0.227 for expo<1 against 0.126 for expo=1.
  - By exposure band: 0.383 for (0, 0.1], 0.273 for (0.1, 0.25], 0.240 for (0.25, 0.5], 0.198 to 0.241 up to 0.999, then 0.126 at a full year.
  - Against an out-of-fold offset model, actual/expected for existing policyholders (bm≠11) is 2.13 at expo≤0.1, 1.2 to 1.6 for partial years, and 0.93 for full years.
  - So the deviance rewards a model that learns "short realised exposure means more claims per day".
- **Where the excess comes from.** Part of it is new entrants: bm=11 is 10.8% of partial-year rows against 3.4% of full-year rows, and its actual/expected at expo≤0.1 is 3.36. That share is known at the start. The excess among bm≠11 policies fits policies ending at or after a claim, which is only known later. The exposures cluster at month ends (days 31, 90, 120, 151, 181, 273, 334), which fits either a start or an end.
- **What decides it.** Whether expo<1 comes from a late start (known at the start) or an early end (not known). The kit has no start or end dates, so I could not tell.
- **The source.** henckr/treeML uses exposure as an offset (gbm) or in a `cbind(expo, nclaims)` response, and scores predicted frequency × realised expo. Realised exposure is therefore part of the source's own setup; the non-proportional use is what this kit adds by making expo a plain feature.
- **Mildest fix.** Make expo an offset only, or change the target to nclaims/expo with expo as the sample weight. Also state in task.md whether expo is the planned or the realised period.

**Attacks that found nothing**

- **Row order.** Spearman correlation of row position with nclaims is 0.0025 (p=0.31). Claim rate by position decile stays between 0.120 and 0.126. Next-row agreement on claim>0 is 0.8014 against 0.8011 expected by chance. Columns are not sorted (postcode is non-decreasing 50% of the time).
- **Splits.** Folds are disjoint, test sets do not overlap training, and each repeat covers all 163,212 rows. Train and test claim rates match (0.1234 to 0.1245).
- **Copies across the split.** 0.2% of rows share all 13 features with another row. Their label variance (0.132) is about the overall variance (0.135). Only 0.28% to 0.36% of test rows have an exact match (all features but expo) in training, and the matched training label correlates with the true label at 0.18 on 175 rows. No gain is possible.
- **Formats.** expo×365 is a whole number for every row. Postcode, long and lat map one to one (583 values each). A model on format features alone (expo==1, last digits of power and age, power divisible by 5) scores 0.55287, worse than predicting the mean (0.55173).
- **Missing values:** none in any column. **Sentinels:** none seen.
- **Transforms over all rows.** long and lat are real municipality centres, not standardised or rank-transformed. The counts over all rows are covered in table row #2.
- **Train against test classifier:** not run. The split is random by rows and train and test claim rates match, so a classifier would score about chance by design.
- **Columns from after the prediction point.** The source's `claim`, `amount`, `average` and `id` are already dropped from the kit. Apart from expo, every feature is known at policy start.
- **Looking rows up in the source file.** It would work: the public CASdatasets file holds nclaims, and the features are nearly unique per row. Not a flaw of the task; not ranked.

**What I could not check**

- Policy start and end dates, which would settle finding #1.
- Whether the preparation filtered or rounded anything compared with the published file. The kit matches the documented 163,212 rows and column set minus id, claim, amount and average; I did not download the raw file to compare values.
- No competition, forum or "leak" thread exists for this dataset. A 2026 preprint reports that contracts cancelled mid-term claim more per unit of exposure, but it does not confirm that it uses this dataset.

Sources:
- [CASdatasets beMTPL97 reference](https://dutangc.github.io/CASdatasets/reference/beMTPL97.html)
- [henckr/treeML treeML.Rmd](https://github.com/henckr/treeML/blob/2ee8accc6df49168bd865cdf49efa1b7a5c8f4de/treeML.Rmd)
- [arXiv 2604.02400 (mid-term cancellations, higher frequency)](https://arxiv.org/pdf/2604.02400)
- [arXiv 2502.11788 (offset vs ratio-weighted Tweedie, mid-term cancellations)](https://arxiv.org/html/2502.11788v1)

</details>

<details><summary>Precedent check</summary>

The focus file (`focus.md`) asks nothing beyond the standard panel. Its "known and kept on purpose" list is where the precedent question lies. Of its five items, four follow precedent: the IID split under `ForcedIIDFromTemporal`, the floor `min_prediction=1e-6`, the 133 duplicate and 35 conflicting rows, and the release's 19 removed policies. One does not: `expo`. It is kept as a free feature, which departs from LEAK-10, and LEAK-10 is a Must. The data shows `expo` carries more than exposure. The register has no flag on bemtpl97 or fremtpl2. That is because the `expo` decisions carry no rule ID (`rule_ids: []` on the 2026-10-23 curator line), not because the decision is clean.

**1. `expo` kept as a free feature: departs with a stated reason, but not a reasonable exception under the ranking (a Must)**

- **Decision.** Myunghwan's curator line of 2026-10-23: "Retain expo". Lennart's line of 2026-11-04 carries it into the approximate `fit_reason`. The definition records it as "Potential leak, kept on purpose", which is the wording LEAK-30 uses for transductive scaling. The mechanism here is a different one: a value that may record an event after the prediction point (a cancellation later in the year). That is LEAK-10, a Must with no exceptions.
- **Precedents under LEAK-10.**
  - account_debt_south_africa (2026-10-26, Lennart): a window value is kept only when "the data shows it does not move with the outcome given the covariates". There the residual ROC AUC was 0.509 / 0.501 / 0.496.
  - distribution_transformers_at_cauca_department (2026-10-21, Lennart): late values are dropped when they "may carry a gain".
  - onlinenewspopularity: such values stay with a note only when the traceable part shows no gain.
  - hotel_booking_demand: `BookingChanges` was dropped.
- **The stated evidence does not test the mechanism.** The record's Poisson fit on log(expo) alone (0.5470 against the training mean's 0.5517) measures signal, and plain exposure would give that signal too. I ran the account_debt test instead:
  - **Claims per insured year by exposure:** 0.292 at expo ≤ 0.25 (8,625 rows), 0.240, 0.198 and 0.233 for the middle bands, and 0.126 for a full year (126,211 rows).
  - **Poisson GLM with all covariates:** the coefficient on log(expo) is 0.54. Pure exposure would give 1.0. A part-year flag on top of the offset gives a rate of ×1.53.
  - **Deviance on one random third:** dummy 0.5560, covariates alone 0.5427, plus expo as an offset 0.5393, plus log(expo) as a free covariate 0.5364. The part of `expo` that is not proportional adds about as much (0.0029) as the proportional exposure does (0.0034).
- **Sibling fremtpl2 behaves the same.** Claims per year are 0.138 at ≤ 0.25 against 0.055 for a full year; the coefficient is 0.62; deviance is 0.2428 with the offset and 0.2407 with the free covariate. Its definition keeps Exposure "as in bemtpl97". So the two siblings are decided alike; both depart from the LEAK-10 cases.
- **What may set the case apart.** Without dates, a mid-year cancellation cannot be told apart from new business that starts mid-year. The insured period of new business is known at quotation, so that part would be legitimate.
- **Contradiction between record and definition.** The AI line of 2026-11-04 says "Exposure is an offset, not a weight". The definition says "no annualization, cap, weight or offset" and "neither a weight nor a scoring column". As shipped, `expo` is a free feature, not an offset.

**Consistency check (AI, 2026-11-04):** your call on bemtpl97 (and fremtpl2) keeps realized `expo` as a free feature. That departs from LEAK-10, a Must. Under its 2026-10-26 clause (account_debt_south_africa), a value is kept only when the data shows it does not move with the outcome given the covariates. Here claims per insured year are 2.3x higher for policies insured up to a quarter of the year, and the free log(expo) coefficient is 0.54 against 1.0 for pure exposure. What sets this case apart?
(a) `expo` is the length of the target's own window and the source's offset, and part-year rows partly reflect new business known at quotation. Recorded as an amendment of LEAK-10, since a Must takes no exception, covering exposure as the denominator of a count target.
(b) Treat it like distribution_transformers: remove the part that is not proportional by scoring `nclaims` against `expo` × predicted annual frequency, with `expo` as a scoring column and not a feature. This is the source's structure, and it reverses the 2026-10-26 "no offsets" on both siblings.
(c) Reopen account_debt_south_africa to match.
(d) Change LEAK-10 generally (amendment).

**2. Floor `min_prediction=1e-6` (MET-13): consistent**

- MET-13 was amended on 2026-11-04 on this very case. fremtpl2 declares the same parameter.
- The other metrics whose domain is limited match:
  - All 20 `rmsle` definitions ship `log` or `log1p`, so their predictions are always in range.
  - `mape` and `rmspe` are limited on the label side, not on the prediction side.
- Lennart's two lines of the same day ("machine epsilon", then "1e-6") are a refinement that MET-13 reconciles (library default machine epsilon, definition states 1e-6), not drift.
- **Stale text in fremtpl2:** `datasets/_dev/tabarena-v0pt2/fremtpl2/dataset.py` line 136 says "The shared scorer floors a predicted mean at machine epsilon (Lennart, 2026-11-04, on bemtpl97)", while its params (line 166) are 1e-6.

**3. IID split under `ForcedIIDFromTemporal` (SPLIT-8), fit approximate: consistent**

- **Precedents:** account_debt_south_africa (2026-10-12), and mobile_churn, churn_telco_south_asia, bank_customer_churn and tour_travels_churn ("one undated snapshot", 2026-10-21, Lennart).
- All 19 working-copy definitions with this tag are `fit="approximate"`.
- **The real opposite-outcome pair has been settled.** On 2026-10-28 Myunghwan shipped beMTPL97 but held freMTPL2 for "missing timing information"; the same fact applies to both. Lennart's "do (a) and ship both" (2026-11-04) resolved it.
- **Count slip.** "the 20 other forced-IID definitions" in the 2026-11-04 line does not match: the working copy has 19 tagged definitions including both siblings, so 17 others.
- The SPLIT-8 Cases table in `splits.md` lists neither sibling. This is bookkeeping, not a departure.

**4. Dtypes (CLEAN-14): consistent**

- **`coverage` ordered TPL < TPL+ < TPL++:** nested cover is a single line, which follows the CLEAN-14 cases (heart_disease, ames_housing) and fremtpl2's ordered `Area`.
- **Full `postcode` declared nominal:** follows house_sales `zipcode`, melbourne_housing_market `Postcode` and perth_house_prices `POSTCODE`, all categorical. The zip-prefix clause does not apply.
- **`fleet` 0/1 as a category:** follows the 0/1 amendment of 2026-10-21.
- **`bm` numeric:** matches fremtpl2's `BonusMalus`.
- The int32 `postcode` in the panel kit is an artifact issue, not a precedent issue.

**5. Copies kept (LEAK-16, LEAK-19, LEAK-20, both Shoulds): departs with a stated reason, consistent**

- 133 exact and 35 conflicting rows are kept. The stated fact is that every source ID is distinct and the rating cells are coarse.
- This follows hiva_agnostic (distinct NSC numbers, 2026-10-21) and fremtpl2 (warnings accepted by Lennart, 2026-11-04).
- For bemtpl97 the check rates both as INFO, not warning, so nothing needs accepting.

**6. Metric is the source's (MET-4 to MET-9): consistent**

- Henckaerts et al. make one deliberate choice: they tune and test by Poisson deviance. That matches the tension row "source's metric when one deliberate choice" (zillow_prize `mae`).
- Myunghwan's switch from RMSE to deviance on 2026-10-26 applies that rule. fremtpl2 does the same.

**7. Year and citation (PROV-9, PROV-10): consistent**

- **Year 2020:** PROV-9 takes "the first commit that shares them", here treeML's 2020-04-30 commit. That is the same rule fremtpl2 applied with its CASdatasets entry date of 2014.
- **Unverified:** whether CASdatasets shipped beMTPL97 before 2020-04-30. If it did, that earlier year wins.
- **Bibtex without the 2018 SAJ paper:** consistent with PROV-10. That paper analysed 163,231 rows but did not release them. Citing two works is common (25 definitions).

**8. `sex` "stays by curator choice": no departure, missing attribution**

- No rule in knowledge-curation covers protected attributes.
- No curator line in the record states this choice; only the 2026-10-23 acceptance of the 13 predictors. The attribution in `curation_comments` has nothing in the record behind it.

</details>

<details><summary>Advocate</summary>

**Opening brief for bemtpl97 (advocate). My position: ship. The data, split and metric stay as defined. The notes and metadata need corrections. `expo` needs one curator decision, and that decision is not a reason to reject the dataset.**

**1. The task is real, and the metric is the source's own (P3 and P6; USE-3, USE-5, MET-1, MET-2 and MET-5 are all Musts and all hold).**
- **Evidence.**
  - Every feature except `expo` is "registered at the start of the policy period". The claim auditor and the column auditor both confirmed this quote verbatim, in the binning manuscript (Sec. 2) and the arXiv paper (App. A).
  - The label is the source's own count. It is not a proxy.
  - The metric is Eq. 5 of arXiv:1904.10890v3 ("f(xi) is replaced by ei·f(xi)"), the same formula as treeML.Rmd L641-657. The source's Fig. 10 range (0.528-0.538) is on the same scale as ours.
  - The signal is real:
    - The dummy scores 0.551735, reproduced exactly.
    - LightGBM-Poisson scores 0.5274-0.5285, a 4.2-4.4% skill, and wins on 9 of 9 folds in three independent runs.
    - A random column moves the score by 0.0001-0.0004, about 1/60 of the skill.
  - The domain practitioner's verdict: "metric scores the decision (yes)". Poisson deviance is strictly consistent for the mean count.
- **What it answers.** The blind reviewer's point 2 (RMSE compresses the scale) and point 3 (low signal) are about RMSE. The definition already ships deviance (Myunghwan, 2026-10-26), so neither point applies. An R² of about 0.02 is normal for claim frequency (TP-2: small and real, keep).

**2. `expo`: I concede the measurement. The dataset stays either way (USE-12, Must, P3), and the open question is which fix.**
- **What I concede.**
  - Four agents agree. Part-year policies claim 1.6-2.3 times the annual rate. Using `expo` freely gains 0.0036-0.0041 deviance over using it as an offset, which is 16-18% of the skill.
  - The note's evidence ("log(expo) alone 0.5470") measures only the legitimate proportional part.
  - "Longer coverage gives more opportunity" is partly refuted.
  - A Must takes no exception, so "kept on purpose" alone does not satisfy LEAK-10. It needs either an amendment or a fix.
- **Why the measurement does not settle the mechanism.**
  - The source names two causes of short exposure: policies that "started the policy in the course of the year or surrendered" (arXiv Sec. 4.1, p. 14). A mid-year start is known at quotation.
  - New entrants (bm=11) make up 10.8% of part-year rows against 3.4% of full-year rows, with actual/expected 3.36 at expo ≤ 0.1 (task gamer).
  - The column auditor's "not new business" proxies (bm≠11, bm=0) are weak. My inference, which ranks lowest under EV-2: a Belgian policyholder who switches insurer keeps their bonus-malus level, so a mid-year switcher looks like an existing customer.
  - Without dates, LEAK-10's window clause cannot be tested the way it was for account_debt_south_africa. `expo` is also the length of the target's own window: the target is the count "during the observed insured period".
- **Mildest remedy that keeps the definition as it is.** The curator records an amendment of LEAK-10 covering exposure as the denominator of a count target, which is option (a) in the precedent checker's consistency prompt.
  - The note gets rewritten with the measured numbers: 16-18% of the skill, observed/expected about 1.4 for part-year rows, and both causes named.
  - fremtpl2 is decided the same way. Lennart treated the two alike on 2026-11-04 (principles.md, consistency rule 2).
- **If the curator declines the amendment.** The next rung on the ladder is a definition fix that still keeps the dataset: `expo` becomes a scoring column and the scorer computes the deviance of y against expo·f(x). This is the source's exact structure, and the ranking of models barely changes (correlation 0.983). It needs a new library metric: `_poisson_deviance` in `src/data_foundry/v2/metrics.py` has no exposure input today. Dropping `expo` is not the mildest remedy, because it throws away the legitimate scaling (0.0052 of the deviance).

**3. The split follows SPLIT-8 (Must), the precedents and the source (P4).**
- There is one undated year, and the raw order is sorted by postcode, so no proxy for time exists (split auditor; 0 violations of the order).
- All 19 forced-IID definitions in the working copy are `approximate`, fremtpl2 included.
- The source's own protocol is random folds within the year (Sec. 3.3).
- Holding out whole municipalities costs at most 0.002 skill. Holding out whole regions still beats the dummy on 9 of 9 folds.
- Exact feature twins across the split are 0.12-0.15% of test rows, with label agreement at chance (0.793 against 0.799).

**4. Provenance: I concede R2. It is a metadata fix only (P5; PROV-9 and PROV-10, Musts).**
- **What changes.** The 163,231-row portfolio has been public since 2019-09-26 (`katrienantonio/PE-pricing-analytics`, 0b279c43). So:
  - set `year = "2019"`;
  - add that repository to the bibtex and the notes.
- **What stays.** The download can stay as it is (PROV-8 lets the download copy differ from the first publication).
- **The 19 removed policies.** The selection is now proven: exactly the 19 rows with an average claim above EUR 81,000, holding 21 claims (0.1%). I argue against restoring them:
  - The paper evaluated on these 163,212 policyholders (Sec. 4.1), so the shipped rows are the metric source's own rows.
  - The removal is the source's preprocessing, not damage, so PROV-13 does not apply.
  - USE-8: a selection alone does not change the fit.
  - Reword "most likely" as a fact.

**5. Dtypes are right (P7, CLEAN-14).**
- `coverage` is ordered and matches the codebook. `postcode` is nominal (583 levels, one-to-one with lat/long), which follows the house_sales and melbourne precedents. `fleet` and `bm` match fremtpl2.
- The int32 `postcode` came from the panel kit. The column auditor reproduced this as a plain parquet round trip, and the container restores the categories (`curation_container.py:363-388`). The blind reviewer's point 4 was made on that artifact.
- Untuned LightGBM overfitting a 583-level category (0.014 of skill) is a model problem. EV-4 says a model's limits are never an argument, and dtypes are decided from context.
- Optional and cheap: store the categories as strings, so a reader without Data Foundry also gets a category.

**6. Copies and the floor follow precedent (LEAK-16 Should, MET-13).**
- 133 exact copies and 35 conflicting profiles. The check rates them INFO, and they follow hiva_agnostic and fremtpl2.
- `min_prediction=1e-6` is the amended MET-13, set on this case. It sits about 2.6 orders below the smallest plausible mean (practitioner: 3.8e-4).

**7. Procedure fixes, none of which affects the verdict (writing.md).**
- Superseded wording to fix:
  - The record's "machine epsilon" line is superseded by the 1e-6 line.
  - fremtpl2 `dataset.py` line 136 also says "machine epsilon".
  - "20 other forced-IID definitions" should be 17.
- The AI line of 2026-11-04 says "Exposure is an offset". The definition says the opposite. Correct that line.
- "`sex` stays by curator choice" has no CC line behind it. It needs a curator line, or it should be marked as an AI draft.
- The record cites "REVIEW.md issue 1", but no `REVIEW.md` exists in `datasets/_dev/tabarena-v0pt2/bemtpl97/`.
- The README is `build_stale: true` and the container is missing locally. Reproducing the build is untested, but builds happen only when the curator asks, so this is not a verdict reason.

**Judgment record**
```text
Verdict: ship after note and metadata changes.
Validity: USE-3, USE-5 hold; LEAK-10 triggered by expo (16-18% of skill non-proportional; mechanism mixed:
  mid-year start vs surrender, untestable without dates); remedy: amend LEAK-10 for exposure as the target window's
  denominator (keeps the definition), else expo as a scoring column; SPLIT-8 holds; PROV-9/PROV-10 fixed in metadata
  (year 2019, cite the 2019 course repository).
Value: MET-1, MET-2, MET-5 hold (source's Eq. 5); TP-2 real signal, 4.2-4.4%, 9/9.
Quality: CLEAN-14 holds; postcode int32 is a kit artifact.
For the curator: issue 1, expo, an amendment or a scoring-column fix (bemtpl97 and fremtpl2 together).
```

</details>

<details><summary>Critic</summary>

**Opening brief against shipping `bemtpl97` as defined**

My position is that it should ship only after changes, and should not be excluded. The task is real: the source's own frequency model, scored by the source's own Poisson deviance, with 4.4% skill and 9 of 9 fold wins (TP-2). Two Must rules fail, and both can be fixed in the definition.

**1. `expo` is a free feature, but realised exposure carries outcome information beyond exposure. P4, LEAK-10 (Must). Fix the definition.**
- **Problem.** `expo` is the share of 1997 the policy was actually in force. The source cites two causes for a part year: a start during the year, and a surrender before its end (arXiv 1904.10890v3, Sec. 4.1). A surrender, often after a claim, happens after the prediction point. The source only ever uses exposure in proportion to the expected count: e·f(x) in Eq. 5, `offset(log(expo))` in treeML. The definition lets a model bend it freely.
- **Evidence.** Four agents measured this independently and agree:
  - Claims per insured year are 0.292 at expo ≤ 0.25 and 0.126 for a full year.
  - Fitted on log(expo), the slope is 0.45 to 0.54. Pure exposure would give 1.0.
  - Using `expo` freely rather than as an offset gains 0.0036 to 0.0041 deviance (claim-auditor, column-auditor, domain practitioner, task gamer). That is 16 to 18% of the model's skill over the dummy.
  - New business does not explain it. Entry-level bm=11 rows show O/E 1.39 against 1.41 for the rest (column-auditor). Among existing policyholders (bm≠11), O/E is 2.13 at expo ≤ 0.1 (task gamer).
- **Effect on the task.** The score rewards a pattern a pricing actuary cannot use: "at quotation I set e = 1" (domain practitioner).
- **Why the stated reasons do not hold.**
  - LEAK-38 covers anonymised competition fields whose timing cannot be tested. Here a conditional test measured the mechanism, and LEAK-38 itself says LEAK-10 then applies.
  - The "kept on purpose" format comes from LEAK-30 (transductive scaling), which is a different mechanism.
  - LEAK-10's 2026-10-26 clauses go against keeping it. A window value stays only when "the data shows it does not move with the outcome given the covariates" (account_debt_south_africa), which fails here. Values whose late cells cannot be located row by row "go when they may carry a gain" (distribution_transformers), and these carry 0.004.
  - A Must takes no exception. The curator's 2026-10-23 and 2026-10-26 "retain expo" lines give no fact that sets the case apart (principles, consistency case 1).
- **Remedy.** Make `expo` a scoring column, not a feature. The model predicts annual frequency f(x), and the scorer computes the mean Poisson deviance of `nclaims` against expo·f(x).
  - This is exactly the source's Eq. 5 and treeML.Rmd L641-657. The target, the rows and the metric stay the same.
  - It keeps the legitimate proportional part: 0.5313 with expo as an offset against 0.5361 without expo (column-auditor).
  - It also satisfies MET-2 (Must): "every input it needs ships as a column and is never a feature".
  - It needs the deviance scorer to read an exposure scoring column.
  - Apply the same fix to fremtpl2, which carries the same mechanism (slope 0.62) and the same note ("as in bemtpl97").
  - If the curator still wants `expo` as a feature, that is an amendment of LEAK-10 (precedent-checker's option (a)), not an exception.

**2. The note's justification is factually wrong. P4, LEAK-38 note format (Should), and EV-2. Rewrite the note.**
- `curation_comments` says `expo` stays "as the exposure the source puts into the expected count". The source puts it in proportionally; the definition does not.
- `known` says "longer coverage gives more opportunity for claims". The claimant share is 17.4% at expo 0.75 to 0.999 against 11.5% for a full year.
- The evidence cited (log(expo) alone scores 0.5470 against 0.5517) measures signal that plain exposure would also give. It does not test the leak.
- The record's AI line of 2026-11-04 says "Exposure is an offset, not a weight". The definition says "no … offset" and "neither a weight nor a scoring column".
- **Remedy.** If point 1 is fixed, the note goes. If it is not, rewrite the note in LEAK-38's format: both causes (start and surrender), the 16 to 18% share of skill, O/E about 1.4, and when to revisit.

**3. The year and the citation are wrong. P5, PROV-9 and PROV-10 (Must). Fix the metadata.**
- **Problem.** The definition says 2020 is "the earliest public copy found". The claim-auditor found an earlier one: `github.com/katrienantonio/PE-pricing-analytics`, commit 0b279c43 of 2019-09-26, file `data/P&Cdata.txt`. It holds 163,231 rows.
- The shipped release equals that file minus exactly the 19 rows with an average claim cost above EUR 81,000, in the same order. All 15 compared columns are identical; only the ids are renumbered.
- PROV-9 takes "the first commit that shares them". The precedent-checker's "consistent with 2020" predates this finding, and a measurement wins (EV-2).
- **Remedy.**
  - Set `year = "2019"`.
  - Add the course repository to the bibtex and the source note.
  - Keep treeML and CASdatasets as the shipped copy, which PROV-8 allows.

**4. The release's selection is now proven, but the definition still says "most likely". P3, USE-5 (Weigh). A note.**
- The 19 removed policies are all claimants, with 21 claims (0.1% of claims). Their removal depends on the outcome.
- The arXiv paper itself uses the 163,212 rows, so the task stays the source's.
- **Remedy.**
  - Replace "most likely removed" in `fit_reason` and `curation_comments` with the verified fact.
  - Mark the record's 2026-10-26 "unverified" line as outdated.
  - Shipping all 163,231 rows from the 2019 origin is a curator call. I do not ask for it.

**5. The build is stale and was not reproduced. EV-7 (procedure). Rebuild before shipping.**
- The README says `build_stale: true`.
- The container `01a18ad7…/dataset.parquet` is missing from the local warehouse.
- So no agent could check the shipped dtypes or the categories restored from `categories.json`; for `postcode` that restore is confirmed from the code only.
- **Remedy.** Rebuild after points 1 to 4 and check the container. Under the house rules the rebuild happens only when the curator asks.

**6. The record contradicts itself and the definition. writing.md (procedure). Text fixes.**
- The CC of 2026-11-04 says "machine epsilon"; the spec and the later CC say 1e-6. fremtpl2 `dataset.py` line 136 repeats the stale "machine epsilon".
- "20 other forced-IID definitions" should be 17.
- "sex stays by curator choice" has no curator line in the record behind it. Add one, or drop the attribution.
- The AI line "no panel ran for this dataset" is now outdated.
- Add to the SPLIT-8 bullet: "the raw order is sorted by postcode, so no row-order window exists" (split-auditor).

**7. `postcode` is int32 in the panel kit. P7, CLEAN-14. Optional, and not a reason to exclude.**
- The definition types `postcode` correctly as nominal. Integer categories become int64 in a plain parquet round trip, which is why the kit shows int32.
- A reader without Data Foundry gets numbers.
- **Remedy (optional).** Store the categories as strings.

**Judgment record**
- **Verdict:** ship after changes 1, 2, 3, 4 and 6, and after the rebuild in point 5.
- **Validity:**
  - LEAK-10 triggered; the fix is `expo` as a scoring column (point 1).
  - PROV-9 and PROV-10 triggered; the fix is in the metadata (point 3).
  - USE-3 holds.
  - SPLIT-8 holds and is disclosed.
- **Value:** MET-1, MET-2 (after point 1) and MET-5 hold. TP-2 shows a real signal.
- **Quality:** CLEAN-14 holds; point 7 is optional.
- **For the curator:** point 1 reverses the "no offsets" decisions of 2026-10-23 and 2026-10-26 on both siblings. Keeping `expo` as a feature needs a LEAK-10 amendment, not an exception.

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal for bemtpl97 (advocate). The critic and I now agree on the verdict: ship after changes, do not exclude. I concede the critic's point 1 remedy. The one difference left is small: the critic makes the rebuild a gate, and I treat it as part of fixing point 1.**

**Critic 1: `expo` should be a scoring column. Conceded, and I withdraw my amendment as the preferred route.**
- **The rules point to the definition fix.**
  - LEAK-10's own text says: "Fix it in the definition the smallest way (LEAK-7), else drop it."
  - The remedy ladder (principles.md item 5) ranks "fix the definition" above "keep with a documented note".
  - The scoring-column fix resolves the problem without changing the target, the rows or the metric. It is exactly the source's Eq. 5 and treeML.Rmd L641-657. So it is the mildest remedy, and keeping `expo` with a note under an amendment ranks below it.
- **My case for the amendment does not hold up.** It rested on the claim that part-year rows are mostly mid-year starts, which are known at quotation. The data goes against that:
  - New business does not explain the excess. Part-year rows with bm=11 have O/E 1.39, against 1.41 for the rest (column auditor).
  - Existing policyholders (bm≠11) reach O/E 2.13 at expo ≤ 0.1 (task gamer).
  - My point about switchers keeping their bonus-malus level is an inference with no measurement behind it. It ranks lowest under EV-2.
- **Both LEAK-10 clauses go against keeping `expo`.**
  - The window clause keeps a value only when "the data shows it does not move with the outcome given the covariates". Here it moves: the free log(expo) slope is 0.45-0.54, and freeing `expo` gains 0.0036-0.0041 of deviance.
  - The same clause also says a value "that falls in the outcome's period, still goes". `expo` falls in the outcome's period.
  - The late-pull clause covers values whose late cells cannot be located row by row: they go when they "may carry a gain" (distribution_transformers). We cannot locate the surrender cases, and they carry 16-18% of the skill.
- **What follows:**
  - The definition fix: `expo` becomes a scoring column, and the scorer computes deviance(nclaims, expo·f(x)). This needs an exposure input in `_poisson_deviance` (`src/data_foundry/v2/metrics.py`).
  - The fix keeps the legitimate proportional part. With `expo` as an offset LightGBM scores 0.5313, against 0.5361 without `expo`, so the 3.69% skill and the 9/9 wins stay.
  - Model rankings barely move: the free-feature and offset models' annual-frequency rankings correlate at 0.983.
  - fremtpl2 gets the same fix (consistency rule 2; slope 0.62 there).
  - The fix reverses the "no offsets" decisions of 2026-10-23 and 2026-10-26. That needs a curator line. Keeping `expo` as a feature is still open to the curator, but only as a deliberate LEAK-10 amendment (option (d)/(a)). I no longer argue for it.
  - The one real cost: the fix also removes the part that comes from mid-year starts (bm=11 at expo ≤ 0.1 has O/E 3.36). Without dates that part cannot be separated, and LEAK-10 resolves an unlocatable gain by removing it.

**Critic 2: the note is wrong. Conceded.**
- What I conceded in point 2 of my opening applies unchanged.
- Once the critic's point 1 is applied, the "kept on purpose" note goes. In its place, a short note says why `expo` is a scoring column: both causes of a part year (start and surrender), the 16-18% of skill, and O/E about 1.4.
- The text "neither a weight nor a scoring column" and the `known` sentence on opportunity get rewritten.
- The AI line "Exposure is an offset" becomes accurate after the fix, but it should be re-dated, because it was false when written.

**Critic 3: the year and the citation. Conceded.** This is my point 4: set `year = "2019"`, cite `katrienantonio/PE-pricing-analytics` 0b279c43, and keep treeML and CASdatasets as the shipped copy (PROV-8).

**Critic 4: the selection of 19 policies. Agreed.**
- Replace "most likely" with the verified fact, and mark the 2026-10-26 "unverified" line as outdated.
- We both leave restoring the 163,231 rows to the curator. The paper evaluated on the 163,212 rows (Sec. 4.1).

**Critic 5: rebuild before shipping. Conceded in substance, disputed as a separate gate.**
- Once point 1 is conceded, the definition and the metric change, so a rebuild and a check of the container are part of that fix anyway.
- A stale README alone is not a defect of the dataset. Builds happen only when the curator asks (rebuild.md).
- After the rebuild, these checks should run:
  - `postcode` is a category in the container;
  - the scoring column is present and is not in `feature_columns`;
  - the dummy and LightGBM scores are re-run against 0.551735 and about 0.5314.

**Critic 6: the record's text. Conceded, with one addition.**
- The fixes the critic lists:
  - "machine epsilon" is superseded in the record and at fremtpl2 line 136;
  - "20 other forced-IID definitions" should be 17;
  - "`sex` stays by curator choice" needs a curator line or should be marked as an AI draft;
  - "no panel ran" is outdated;
  - the SPLIT-8 bullet gets "raw order sorted by postcode" added.
- I add one more: the record cites "REVIEW.md issue 1", but no `REVIEW.md` exists in the folder.

**Critic 7: `postcode` int32. Agreed.**
- The int32 comes from the panel kit's parquet round trip, not from the definition (CLEAN-14 holds).
- Storing the categories as strings is optional.

**Where we agree on what holds:**
- USE-3, USE-5, MET-1, MET-5 and SPLIT-8 hold.
- TP-2 shows a real signal: 4.2-4.4% skill, 9/9 fold wins, against a noise band of 0.0001-0.0004.
- None of the critic's points argues for exclusion.

**Judgment record (revised)**
```text
Verdict: ship after changes.
Validity: LEAK-10 triggered by expo; fix in the definition (LEAK-7, ladder): expo as a scoring column,
  deviance of nclaims against expo*f(x) (source's Eq. 5); same for fremtpl2; reverses 2026-10-23/26 no-offset lines
  (curator line needed; keeping expo as a feature would need a LEAK-10 amendment). PROV-9/PROV-10: year 2019, cite
  PE-pricing-analytics 0b279c43. SPLIT-8 holds. USE-5: selection of 19 policies stated as fact.
Value: MET-1, MET-2 (after the fix), MET-5 hold; TP-2 real (offset-only skill 3.7%, 9/9).
Quality: CLEAN-14 holds; postcode as strings optional.
For the curator: issue 1, approve the expo scoring-column fix on both siblings (needs an exposure input in
  _poisson_deviance), then rebuild and re-check.
```

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic) on `bemtpl97`**

The advocate and I now agree on most points. We disagree on one thing: what to do about `expo`.

**Advocate 1: the task is real and the metric is the source's (USE-3, USE-5, MET-1, MET-2, MET-5).** I concede this. My opening said the same: a 4.2 to 4.4% skill, 9 of 9 fold wins, and Eq. 5 of the source paper. I add one point. MET-2 holds fully only when the exposure that Eq. 5 needs ships as a scoring column. Today it ships as a feature. See point 2.

**Advocate 2, `expo`: I dispute the remedy.**
- **The ladder does not list an amendment.**
  - `principles.md` says a Must violation "is fixed in the definition when it can be (drop, lag, filter, re-split, re-target)". The remedy ladder runs: repair, fix the definition, keep with a note, exclude.
  - An amendment is not a step on that ladder. It is a deliberate change to the rule, offered when a departure "would break a Must" (consistency case 1). It is not the mildest remedy for a Must that can be fixed.
  - Both sides agree this one can be fixed. The advocate's own fallback is the fix: `expo` as a scoring column, with the deviance of `nclaims` against expo·f(x). So the Must calls for the fix (Must, P4). The amendment is open to the curator only as a deliberate change to LEAK-10.
- **"The mechanism cannot be tested without dates" argues for removal, not for keeping.** LEAK-10 has two clauses, amended on 2026-10-26.
  - A value from the target's window stays only "when the data shows it does not move with the outcome given the covariates". The data shows it does move: the log(expo) slope is 0.45 to 0.54, and O/E is about 1.4.
  - Values whose late cells "cannot be located row by row … go when they may carry a gain". This is the advocate's own premise, and the gain is 0.0036 to 0.0041.
  - The advocate also calls `expo` "the length of the target's own window". That puts it inside LEAK-10's window clause, not outside it.
- **The new-business explanation loses on evidence (EV-2, Must).**
  - New entrants (bm=11) do show an excess, O/E 3.36 at expo ≤ 0.1. But existing policyholders show it too: O/E 2.13 at expo ≤ 0.1 for bm≠11 (task gamer).
  - Over all part-year rows, bm=11 gives 1.39 and the rest give 1.41 (column auditor).
  - The idea that "switchers keep their bm level" is inference. The advocate ranks it lowest, and it cannot outweigh two measurements.
- **I concede this much.** The scoring-column fix also removes the legitimate part from mid-year starts, which is known at quotation. That cost is smaller than keeping a measured post-outcome channel (LEAK-10 clause 2). The source itself never uses that part: it fixes the slope at 1.
- **The advocate's 0.983 does not show what it is used for.** It is the per-policy rank correlation between two models' predicted frequencies (domain practitioner). It says nothing about how the leaderboard would order methods, so it does not show that the fix "barely changes" the ranking.
- **I concede these points.**
  - Do not drop `expo`, since that loses the proportional 0.0052.
  - The fix needs an exposure input in `_poisson_deviance` (`src/data_foundry/v2/metrics.py`).
  - fremtpl2 must be decided the same way (consistency rule 2).

**Advocate 3: the split (SPLIT-8).** I concede. It is IID, `approximate`, disclosed, and matches the source's random folds. Holding out whole municipalities costs at most 0.002 skill. One wording fix remains: the SPLIT-8 note should say the raw order is sorted by postcode.

**Advocate 4: provenance (PROV-9, PROV-10).** I concede, and our remedies match: set `year = "2019"`, cite `katrienantonio/PE-pricing-analytics` 0b279c43, keep the treeML download (PROV-8), and state the 19-row selection as a fact. I agree not to restore the 19 rows (USE-8; the paper's own 163,212 rows).

**Advocate 5: dtypes (CLEAN-14).** I concede. The int32 comes from the panel kit, not the definition. String categories stay optional.

**Advocate 6: copies and the floor (LEAK-16, MET-13).** I concede. Both checks rate the copies as INFO, and the 1e-6 floor sits about 2.6 orders below the smallest plausible mean.

**Advocate 7: procedure.**
- I concede the text fixes and accept a new fact the advocate found: the record cites "REVIEW.md issue 1", but no `REVIEW.md` exists in the folder. Add that to my point 6.
- I partly dispute the build. A stale build is no reason to exclude, but a stale build cannot ship. The rebuild belongs after the definition fixes, when the curator asks for it (EV-7). Then the container's dtypes and `postcode` categories can be checked, which no agent could do here.

**Judgment record**
- **Verdict:** ship after changes. Never exclude.
- **Validity:**
  - LEAK-10 (Must) fails. The fix is `expo` as a scoring column, with a scorer that takes exposure. Apply it to bemtpl97 and fremtpl2 together.
  - An amendment of LEAK-10 is a deliberate rule change for the curator to choose. It is not a milder remedy.
  - PROV-9 and PROV-10 are fixed in the metadata.
  - USE-3 and SPLIT-8 hold.
- **Value:** MET-1 and MET-5 hold. MET-2 holds fully once `expo` is a scoring column. TP-2 shows real signal.
- **Quality:** CLEAN-14 holds. String categories for `postcode` are optional.
- **For the curator:**
  - The one open disagreement is LEAK-10: fix the definition (critic) or amend the rule (advocate). If you choose the amendment, the note is rewritten in LEAK-38's format with both causes, 16 to 18% of the skill and O/E about 1.4.
  - Then: the text fixes (including the missing `REVIEW.md`), and a rebuild when you ask for it.

</details>
