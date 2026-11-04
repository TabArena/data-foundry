# fremtpl2

**Outcome:** added. A French motor third-party liability portfolio (677,991 policy records, about 2011-2013): the
number of claims with a recorded cost in the insured part of the year, scored by the source's mean Poisson deviance on
random folds. Verdict: ship after changes, not as defined (second-pass panel, after Lennart's PR #33 review of
2026-11-04). Validity: USE-5 and PROV-13 hold (the 2022 counts equal the claims table); LEAK-10 is triggered, likely,
by `BonusMalus` in blocks 0-4 (issue 5) and, with the mechanism measured, by realised `Exposure` (issue 6); LEAK-17 and SPLIT-8's text are triggered by the policy chains across the random split (issue 7);
SPLIT-14 cannot be met, so SPLIT-8 applies. Value: MET-5 holds; the signal is real and small (LightGBM 0.2326, Poisson
GLM 0.2397, exposure baseline 0.2534). Quality: CLEAN-11 (no cap, exposures above a year kept) holds; CLEAN-10 is open
for `DrivAge` 99 (issue 9). Weighed: the label-free renewal signal, kept with a note (issue 8).

**Main points:** Blank `BonusMalus` in blocks 0-4 (issue 5)? Take realised `Exposure` out of the features and score
with it as an offset (issue 6)? Group the split on the inferred policy chains (issue 7)? Keep the label-free renewal
signal with a note (issue 8)? Set `DrivAge` 99 to missing (issue 9)?

**Record fields that disagree with the definition:**

- `year`: record `(empty)`, definition `2014`.

**Issues for Lennart:**

5. **Blank `BonusMalus` in blocks 0-4, where it looks recorded after the row's own claims?**

   * **Problem:**
     - `BonusMalus` is the French bonus-malus coefficient (50 to 350), which falls by 5% after each claim-free year and
       rises by 25% per at-fault claim.
     - If a row's value was read after that row's claims, it carries the target, which the insurer does not know when
       quoting.
     - It looks recorded after them in blocks 0-4 (597,998 rows, 88%) and like a value taken at the start of the year
       in blocks 5-6.
   * **Background:** The blocks are the million-wide `IDpol` ranges, read as periods of three sub-portfolios (0-1, 2-3,
     4-5-6).
   * **Experiments:** column auditor; the frozen values confirmed by the claim and split auditors.
     - In blocks 4-6, where consecutive records of one policy can be compared, it behaves like a value taken at the
       start of the year: it falls in 92-94% of claim-free pairs and rises after a claim in 35-37%; it moves with the
       previous year's claims, hardly with its own row's.
     - In blocks 0-3 it is frozen across the two years (94.5% unchanged from block 0 to 1) and moves with its own
       row's claims as strongly as with the other year's.
     - The footprint is the first malus step from the floor, 62-63 (50 x 1.25), among drivers 30 and older:

     | rows | share at 62-63, with a claim | without a claim |
     |---|---|---|
     | blocks 0-3 | 5.3-6.8% | 1.5-1.7% |
     | block 4, no next-year row | 7.8% | 1.3% |
     | block 4 with a next-year row, and blocks 5-6 | 1.1-2.2% | 1.4-1.6% |

   * **Effect on the task:** `BonusMalus` carries 42% of LightGBM's gain over the mean count (0.0112 of 0.0269).
     Removing it worsens the deviance by 0.0131 in blocks 0-3 and changes it by -0.0005 (SE 0.0003, within noise) in
     blocks 5-6. It also carries most of the split leak of issue 7 (0.0021 with it, 0.0002 without).
   * **Unknown:** Not shown, likely[^likely]: no source statement says when the value was recorded (the panel's search
     of the source found none[^source-first]), and the whole freMTPL2 literature uses it as its main rating factor.
   * **Consistency:** Blanking follows zillow_prize and melbourne_housing_market (the second clause of the rule against
     features recorded after the outcome[^after-outcome]); none went the other way. Keeping it as is needs an amendment
     of that rule, not an exception.
   * **Panel:** The critic's narrower mask (blocks 0-3 plus the block-4 rows without a next-year row) was rejected by
     the mediator: there a missing value would mean "not renewed", and those rows claim 0.141 against 0.070 per year,
     missingness that encodes the outcome[^after-outcome].
   * **Option details:**
     - B: blank it in blocks 0-4 (597,998 rows, 88%), the form of online_shoppers ("keep only the period where it
       behaves like history").
     - C: drop the column, equivalent in effect; it adds nothing measurable in blocks 5-6.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | in all rows | the main rating factor | likely holds the target; a rule amendment |
     | B | Blank blocks 0-4 | 88% of rows missing | as online_shoppers; smallest fix[^smallest] | gone in 88% of rows |
     | C | Drop the column | removed | same effect; nothing lost in blocks 5-6 | also gone where it is history |

   * **Recommendation:** B, blank blocks 0-4. **Decision:** A (keep as is, an amendment of the rule), B (blank blocks
     0-4) or C (drop the column)?

   [^after-outcome]: **LEAK-10** (Must). Blanking follows its second clause (zillow_prize, melbourne_housing_market);
     keeping the column as is needs an amendment of LEAK-10, not an exception.
   [^likely]: **EV-6**: "likely", not shown.
   [^source-first]: **LEAK-3** (Should): read the source first.
   [^smallest]: **LEAK-7**: the smallest fix.

6. **Take realised `Exposure` out of the features and score with it as an offset?**

   * **Problem:**
     - `Exposure` is the share of the year the policy was insured, known at the end of the period.
     - A policy cancelled after a claim gets a short exposure, so the column carries part of the outcome.
     - At quotation the insurer knows the planned term, not a later cancellation.
   * **Background:** Now `Exposure` is a free feature under "Potential leak, kept on purpose", as in
     bemtpl97[^bemtpl97]; the note now gives the sizes below.
   * **Experiments:** claim auditor, column auditor, domain practitioner, task gamer.
     - Among rows with a previous-year record (renewals, no new business), rows with exposure of 0.1 years or less
       claim 0.255 a year against 0.056 for a full year.
     - Within each exposure band, a claim lowers the chance of a next-year record (0.19 against 0.27, up to 0.47
       against 0.53).
     - A Poisson GLM on the rating factors gives log(`Exposure`) a free coefficient of 0.641, where a pure offset would
       be 1.
     - Size of the kept leak: used as a free feature beyond a log(`Exposure`) offset it is worth 0.0039-0.0045 mean
       deviance, 14-19% of LightGBM's gain (three agents). The proportional, legitimate part is 0.0061 (0.2595 to
       0.2534). Part of the excess is renewals during the year recorded as two records (Wüthrich and Merz 2023,
       [Sec. 13.1](https://link.springer.com/chapter/10.1007/978-3-031-12409-9_13)), so the leak is mixed but not
       absent.
   * **Consistency:** No exception of the rule against features recorded after the outcome covers it[^no-exception]. A
     follows kick `WheelType` (2026-10-22) and heart_failure_followup_survival `time` (2026-09-30), both dropped once
     the mechanism was measured; it departs from bemtpl97, where the mechanism had not been measured.
   * **Panel:** Disputed: the advocate argued the exception for a planned term[^no-exception] and conceded that a note
     does not resolve a Must[^after-outcome]; the critic asks for A.
   * **Option details:**
     - A: `Exposure` becomes a scoring column and the score is the Poisson deviance of the predicted rate x
       `Exposure`, the offset form of Noll, Salzmann and Wüthrich. It costs a new metric in
       `src/data_foundry/v2/metrics.py` and reopening bemtpl97 to match.
     - B: keep it and amend the rule[^after-outcome] for exposure denominators, recording 0.0039-0.0045 as the leak's
       size.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Offset in the score | `Exposure` scores only | removes the leak; as kick | new metric; reopen bemtpl97 |
     | B | Keep, amend the rule (implemented) | free feature, noted | as bemtpl97 | leak of 14-19% of the gain |

   * **Recommendation:** A (mediator). **Decision:** A or B, with bemtpl97 following the same call?

   [^after-outcome]: **LEAK-10** (Must).
   [^no-exception]: **LEAK-37** covers a planned term, and none ships; **LEAK-11** needs a value that weakens the
     signal, and this one strengthens it; **LEAK-38** sends a measured mechanism back to **LEAK-10**. The advocate
     argued LEAK-37.
   [^bemtpl97]: Myunghwan, 2026-10-23 and 2026-10-26 (bemtpl97).

7. **Group the split on the inferred policy chains (`ForcedGroupedFromTemporal`) instead of IID?**

   * **Problem:**
     - The release has no dates, but `next_year_rows` links 161,883 pairs of records across consecutive `IDpol` blocks
       (same car and region, the driver one year older), against 16 to 75 under shuffled or shifted controls (a chance
       rate of 0.02-0.05%).
     - Under the random split, 16% of test rows have the same policy's next-year record on the training side, and a
       model that reads other rows (a nearest-neighbour or in-context model, or a participant's lookup feature) can
       find it from the shipped columns alone: the true partner is the only candidate for 54.6% of linked rows.
     - That record holds information about this year's claims that an insurer pricing a renewal never has, because it
       comes from the future.
   * **Background:** The definition is IID with `ForcedIIDFromTemporal`, your call of 2026-11-04[^call]. The first
     pass recommended IID, and "follow the recommendation" took that advice; this pass measured the next-year channel
     and recommends grouping.
   * **Experiments:**
     - The next-year record's claim count and exposure lower mean deviance by 0.0021 with `BonusMalus`, 0.0002 without
       it (3 of 3 folds), and by nothing under grouped folds (mediator). The previous-year record, legitimate history,
       is worth 0.00015.
     - Relinked from shipped columns only, a stacked GLM gains 0.0057 skill (the share of the exposure baseline's
       deviance a model removes) on 3 of 3 folds; grouping on the chains halves it to 0.0024 (domain practitioner).
     - For models that score one row at a time, grouping costs nothing: LightGBM mean deviance 0.23265 shipped against
       0.23238-0.23245 grouped (three seeds), a difference of 0.0002-0.0003 (SE 0.0002), about the 0.0002 by which two
       random seeds differ.
     - The entity carries little of the label itself: pair correlation of claims 0.017.
   * **Consistency:** Grouping follows nba_players_2016_2019 and open_university_learning_analytics_dataset
     (2026-10-21, grouped on a key the release gives). The rules ask for a split by the entity when the periods are
     stacked and the entities recur across them[^entity], and bar the size of the gap as a reason[^gap].
   * **Panel:** Disputed: the critic and the mediator ask for A; the advocate holds that grouping does not remove the
     label-free renewal signal (issue 8) and that the rule on constructed keys[^key] does not clearly admit a
     rule-built key.
   * **Option details:**
     - A: `ForcedGroupedFromTemporal` on the `next_year_rows` chains, with the rule also searching IDpol offsets -1 to
       -9 (another 26,851 matches between rows the forward search leaves unpaired). It needs a ruling that a key built
       by this exact rule counts as "constructed exactly from the data"[^key], and it changes the split; row-wise scores
       do not move.
     - B: keep IID and record the facts that set the case apart: the links are inferred between inferred years, the
       entity carries almost none of the label (pair correlation 0.017, so the rule on entities that carry the label
       does not fire[^label-entity]), and pricing serves renewals, which are known policies[^renewals]. After issue 5
       the label channel left is 0.0002, a size and not a reason.
     - C and D are the consistency check's (c) and (d) below.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Group on the chains | `ForcedGroupedFromTemporal` | as nba, open_university | a ruling on the key |
     | B | IID, facts recorded (implemented) | notes give the facts | row-wise scores same | departs from the text |
     | C | A year per sub-portfolio | 353,887 rows | as distribution_transformers_at_cauca_department | fewer rows |
     | D | Amend the rule | IID for inferred entities | IID the closest regime | a rule change |

   * **Recommendation:** A (mediator). **Decision:** A, B, C or D (the consistency check's (a) to (d) below)?

   [^entity]: **LEAK-17** (Must) and **SPLIT-8**'s text ("grouped by the entity when the periods are stacked and the
     entities recur across them"), against **SPLIT-13** (Should).
   [^gap]: **SPLIT-4** and **SPLIT-30** bar the size of the gap as a reason.
   [^key]: **SPLIT-24**: a key "constructed exactly from the data".
   [^label-entity]: **SPLIT-29**.
   [^renewals]: **SPLIT-13**, **USE-10**.
   [^call]: Lennart, 2026-11-04: "follow the recommendation"; the links "are not the source's key and change the score
     by nothing".

   **Consistency check (AI, 2026-11-04):** your call on fremtpl2 (IID on stacked periods with recurring policies,
   2026-11-04) departs from SPLIT-8's text and differs from nba_players_2016_2019 and open_university (grouped,
   2026-10-21). Its stated reason, "change the score by nothing", is one SPLIT-4 and SPLIT-30 do not count, and the
   next-year channel (0.0021) was not measured then. What sets fremtpl2 apart?

   - (a) No fact sets it apart: group on the chains, as nba and open_university were.
   - (b) The links are inferred between blocks whose years are themselves inferred, the entity carries almost none of
     the label (correlation 0.017, SPLIT-29 does not fire), and pricing serves renewals (SPLIT-13): recorded in the
     notes in place of "change the score by nothing".
   - (c) Keep one inferred year per sub-portfolio, as distribution_transformers_at_cauca_department (blocks 0, 2 and 4:
     353,887 rows).
   - (d) Amend SPLIT-8: when entities are only inferred and carry little of the label, the closest regime is IID.

8. **Keep the label-free renewal and record-structure signal with a note?**

   * **Problem:**
     - Whether a policy has a later or a sibling record can be read from the test features themselves.
     - A policy with a later record was renewed rather than ended, and renewed policies claim about half as often
       (0.070 against 0.141 claims per year in block 0).
     - A model that computes these signals from the test rows learns whether the policy was renewed, which the insurer
       does not know when quoting.
   * **Background:** Statistics over train and test rows of the records identical except `Exposure` (their number and
     summed exposure) carry the same early-termination effect. Now kept; the notes do not name it.
   * **Experiments:** the renewal signal is worth 0.0017 mean deviance with `BonusMalus` (split auditor) and
     0.0009-0.0010 without it (mediator), under random and grouped folds alike; the task gamer's record-structure
     statistics gain 0.0006-0.0007.
   * **Consistency:** none for record existence. The rule on transductive leaks covers scaling only, so this is a
     weighing call[^transductive].
   * **Option details:** none removes it. No split does, and merging records into one row per policy-year needs a key
     the source does not give, so the only other way is a `No`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | a note and a tension row | the data as published | a weak leak stays |
     | B | `No` | the dataset does not ship | no such leak | loses the dataset |

   * **Recommendation:** A, keep with the note. **Decision:** A (keep with the note; the tension row follows) or B
     (`No`)?

   **Notes for the AI:** on A, add a `Potential leak, kept on purpose:` note with these numbers, and a new row under
   the tension "a weak transductive leak against the data as published" (today it lists only the scaling cases
   sf_permit_time and home_credit), written in the same change.

   [^transductive]: **LEAK-10** (the mechanism, transductive); **LEAK-30** covers scaling only.

9. **Set `DrivAge` 99 to missing in block 0, as `VehAge` 99/100 is?**

   * **Problem:**
     - 70 rows have a driver aged 99, against 5 at 98 and 3 at 100; 66 of them are in block 0, after 1 row at 96 and
       none at 97-98, none of the 66 has a next-year record (62.7% of block 0 has one), and block 1 has no driver
       older than 97.
     - That is the default-code pattern for which the definition sets `VehAge` 99 and 100 to missing.
     - Kept, a model reads 66 unknown ages as 99-year-old drivers; the effect is limited to those rows.
   * **Background:** Now kept "as possible".
   * **Consistency:** `VehAge` in the same definition[^default].
   * **Panel:** Both the advocate and the critic conceded the change.
   * **Option details:**
     - A: keep 99 and record that it is a top code (a real age of 99 or more).
     - B: set the 66 block-0 values to missing, a cleaning change, so left to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 99 a top code (implemented) | kept, reason recorded | no cleaning change | 66 unknown ages as 99 |
     | B | Set to missing | the 66 block-0 values missing | as `VehAge` | a cleaning change, so left to you |

   * **Recommendation:** B, set the 66 values to missing. **Decision:** B (missing) or A (a recorded top-code reason)?

   [^default]: **CLEAN-10** (Should).

**Review panel:** ship after changes, not as defined (mediator). Tier full, second pass after Lennart's PR #33 review of
2026-11-04. Claims: 21; 14 hold, 1 holds in part ("consecutive years"), 5 refuted (the Exposure share, "changes
nothing", machine epsilon, "21 of 23", the 28,768 copies; all corrected in the notes this pass), 1 untested (the
Wüthrich and Merz page numbers and Eq. 5.28; their quotes were verified by the advocate). Blind review: include with
changes; its main concerns were the extreme counts under squared error (moot under the declared Poisson deviance), the
`Exposure` framing and near-duplicate rows. Task gamer: the best exploit is realised `Exposure` (0.0045, about 2% of
the score); record-structure statistics over train and test gain 0.0006-0.0007; sibling labels add nothing. Agreed:
the target, the metric, no cap, exposures above a year kept, `DrivAge` 99 to missing, the wording fixes, and that
`BonusMalus` as shipped likely breaks a Must. Disputed: the split (LEAK-17, SPLIT-8, SPLIT-24; issue 7), `Exposure`
(LEAK-10 against LEAK-37; issue 6), and the `BonusMalus` mask (LEAK-10; settled by the mediator for blocks 0-4,
issue 5).

<details><summary>Mediator</summary>

**fremtpl2: mediator report (second-pass panel, 2026-11-04)**

**Recommendation (judgment record)**

```text
Verdict: ship after changes (not as defined).
Validity: USE-5 holds (ClaimNb, direct fit); PROV-13 holds (2022 counts equal the claims table);
  LEAK-10 BonusMalus triggered, likely (blank blocks 0-4 or drop; curator, issue 1);
  LEAK-10 Exposure triggered, measured (offset scoring column or a LEAK-10 amendment; curator, issue 2);
  LEAK-17 / SPLIT-8 triggered (recommend ForcedGroupedFromTemporal on the chains; Lennart's IID call of 2026-11-04 needs a fact the rules count; issue 3);
  SPLIT-14 cannot be met, so SPLIT-8 applies.
Value: MET-5 holds (the source's Poisson deviance, min_prediction 1e-6); real small signal: LightGBM 0.2326, GLM 0.2397, exposure baseline 0.2534.
Quality: CLEAN-10 DrivAge 99 fixed (change below); CLEAN-11 no cap holds; wording fixes.
Weighed: the label-free renewal signal kept with a note (issue 4).
For the curator: issues 1-3 (Must), issue 4 (a new tension row).
```

The mediator's issues 1-4 are issues 5-8 of this file; its change 6 (`DrivAge` 99) changes the data and is issue 9.

Neither side asks for exclusion. The critic's "don't ship as defined" stands, because the advocate conceded that BonusMalus and Exposure each break a Must that a note does not resolve.

**Decisive experiment run in this pass**

Disputed point: does the cross-split label leak survive once BonusMalus is out? I ran LightGBM (Poisson) without BonusMalus and report mean Poisson deviance over 3 folds.

| Added to the no-BM model | Shipped folds | Grouped on chains |
|---|---|---|
| none (deviance) | 0.24351 | 0.24349 |
| true next-year row's ClaimNb and Exposure (via IDpol) | −0.00023 (−0.00011 to −0.00041, 3/3 folds) | +0.00005 (nothing) |
| count of feature-matched later candidates (label-free) | −0.00086 | −0.00098 |
| plus the candidates' labels | another −0.00019 (3/3 folds) | +0.00004 (nothing) |

What this settles:
- With BonusMalus in, the next-year channel is worth −0.0021. Without it, −0.0002. So most of the split leak runs through BonusMalus and is fixed by issue 1.
- The small remainder still exists under IID and is gone under grouping.
- The renewal signal (about −0.0009 to −0.0010) survives any split.

**Changes to make now (no decision needed)**

1. Metric bullet: change "machine epsilon" to `min_prediction` 1e-6. Rule: MET-13, and Lennart's later CC on bemtpl97.
2. VehAge: the notes and the `DEFAULT_VEHICLE_AGE` docstring say "21 of the 23 aged 99 are 100 a year later". The shipped rule pairs 14 of the 23, and all 14 are 100 a year later. Rule: EV-7.
3. "Copies kept" bullet. Rules: EV-7, SPLIT-4, SPLIT-30.
   - Say 28,768 rows copy an earlier row, and 40,903 rows sit in groups of equal rows.
   - Name the links behind the 430,298 groups.
   - Say the 48-60% link shares are lower bounds (±30 gives up to 75.3%).
   - Remove "changes nothing" as a reason and give the measured channels instead.
4. "Split forced IID" bullet. Rule: SPLIT-8.
   - Report the cost on the same rows: +0.00049 deviance (SE 0.00016), so IID is slightly optimistic.
   - Qualify the blocks. From 0→1 and 2→3 the BonusMalus is frozen (94.5% unchanged in 0→1). In blocks 4-6, 0.2% of linked rows cover a full year and 63-66% of pairs sum to at most 1.01, so they look like split contract years.
5. Exposure note: replace "about a fifth of the gain". The proportional part is 0.0061. The size of the kept leak is the part beyond the offset: 0.0039-0.0045 (14-19% of the gain), with a free GLM coefficient of 0.641. Write these numbers whatever issue 2 decides. Rule: EV-7.
6. DrivAge 99: set the 66 block-0 rows to missing, as VehAge is. They follow an empty band, none has a next-year row (62.7% of block 0 does), and block 1 has no driver older than 97. Both sides conceded, and no curator ruling exists to depart from. Rule: CLEAN-10.
7. Year note: cite `pkg/inst/NEWS` at CASdatasets commit 324c15c999. The pinned NEWS.md does not list the tables. Rule: EV-7.
8. Citations. Rule: EV-7. The two Wüthrich and Merz quotes are verified word for word (Appendix B, pp. 553-575, saved chapter). Still to do, verify or cut:
   - the 553/554 page split;
   - Eq. 5.28;
   - the 9,942 old claims;
   - the LightGBM figure of 292.6.

Applied in this pass: changes 1-5, 7 and 8 in part (the page numbers cut in favour of Sec. 13.1, which the saved chapter shows; the 9,942 old claims recomputed from the 2017 copy: 9,387 policies, 9,942 claims). Change 6 is issue 9.

**Issues for the curator, ranked**

**1. BonusMalus is likely recorded after the row's claims in blocks 0-4 (P4, LEAK-10 Must; EV-6 "likely"; LEAK-3).**
- Problem: in blocks 0-3 the value is frozen across years and tied to the row's own claims as strongly as to the other year's (×4.3-5.9 vs ×4.8-6.2).
  - Claimants pile onto the first malus step, 62-63: 5.3-6.8% of claimants against 1.5-1.7% of other rows.
  - Block-4 rows without a next-year row show the same pile (7.8% vs 1.3%). Continuing block-4 rows and blocks 5-6 do not (1.1-2.2% vs 1.4-1.6%).
- Effect: BonusMalus carries 42% of the gain (0.0112 of 0.0269). Removing it costs 0.0131 in blocks 0-3 and gains 0.0005 in blocks 5-6. It also carries most of the split leak (experiment above).
- Each side's best evidence:
  - Critic: the 62-63 footprint, which better risk selection would not produce.
  - Advocate: no source statement exists, and the whole literature uses BonusMalus as its main factor.
- Settled sub-dispute, the mask. The critic would blank blocks 0-3 plus the block-4 rows without a next-year row. Under that mask, missing would mean "not renewed", and non-renewed rows claim 0.141 against 0.070 per year. That is "missingness that encodes the outcome", which LEAK-10 bars. Blanking all of blocks 0-4 covers the same rows without this problem, so the advocate's mask wins under the same Must.
- Decision needed:
  - accept the leak reading, since the panel's source search (LEAK-3) found nothing;
  - then blank blocks 0-4 (LEAK-7, the smallest fix; the online_shoppers form) or drop the column. They are equivalent in effect.
  - Keeping it as is needs an amendment of LEAK-10.

**2. Exposure as a free feature (P4, LEAK-10 Must). This is an independent failure, not a conflict.**
- No exception rule applies:
  - LEAK-37 covers a planned term, and no planned term ships.
  - LEAK-11 needs a value that weakens the signal, and this one strengthens it.
  - LEAK-38 covers anonymised competition fields, and its own clause sends a measured mechanism back to LEAK-10.
- The mechanism is measured conditionally:
  - within each exposure bin, a claim lowers the chance of a next-year row (0.19 vs 0.27 up to 0.47 vs 0.53);
  - among rows with a prior-year record (no new business), rows with exposure ≤0.1 claim 0.255 a year against 0.056 at a full year.
- Advocate's best point: Wüthrich and Merz say renewals during the year are split into two records, so the leak is mixed. That makes it smaller, not absent.
- Decision needed, one of:
  - (a) Exposure becomes a scoring column, scored by Poisson deviance of the predicted rate × Exposure (the source's offset form). This needs a new metric in `src/data_foundry/v2/metrics.py` and reopening bemtpl97.
  - (b) Amend LEAK-10 for exposure denominators, recording 0.0039-0.0045 as the leak's size.

  I recommend (a).

**3. The split: IID or ForcedGroupedFromTemporal (P4; LEAK-17 Must and SPLIT-8's text against SPLIT-13, a Should, and USE-10).**
- Ruling by rank: LEAK-17 (Must) outranks SPLIT-13 (Should).
  - "Changes the score by nothing" is barred as a reason by SPLIT-4 and SPLIT-30.
  - "Not the source's key" does not bar grouping either. SPLIT-24 allows a key constructed exactly from the data. The chains come from an exact rule whose chance rate is 0.02-0.05% (161,883 matches against 16-75 under the controls). SPLIT-25 does not apply.
  - The renewal argument cuts against IID: IID hands the model the policy's future year (−0.0021, or −0.0002 without BonusMalus), while past years are worth −0.00015.
- What grouping costs: nothing measurable. Skill is 0.0825 vs 0.0813, and deviance 0.23265 vs 0.23238-0.23245.
- Decision needed. Lennart's CC of 2026-11-04 kept IID for reasons the rules do not count, and new evidence has come in since. Choose one:
  - (a) ForcedGroupedFromTemporal on the `next_year_rows` chains, with a SPLIT-24 ruling that this key counts as constructed exactly. This is my recommendation.
  - (b) Keep IID, recording a fact the rules accept. After issue 1 the residual leak is 0.0002 on 3 of 3 folds.

**4. The label-free renewal and record-structure signal (P4; LEAK-10 mechanism, transductive; a weighing call).**
- What it is: whether a later or sibling record exists can be read from the test features themselves.
- Size:
  - renewal signal: 0.0009-0.0010 without BonusMalus; 0.0017 with it (split auditor);
  - the gamer's record-structure statistics: 0.0006-0.0007.
- No split removes it. Merging records needs a key the source does not give.
- The principles' tension row on weak transductive leaks lists only scaling cases.
- Decision needed: keep with a `Potential leak, kept on purpose:` note giving these numbers, and add a tension row.

Minor, no change unless the source speaks: VehPower 15 may be a top band (CLEAN-14).

Task-gamer exploits mapped:

| Exploit | Rule | Status | Is it an issue? |
|---|---|---|---|
| Realised Exposure, 0.0045 | LEAK-10 | known (the Exposure note) | yes: the measured gain differs from the note (issue 2) |
| Statistics over train and test records, 0.0006-0.0007 | LEAK-10, transductive | new | issue 4 |
| Sibling labels, 0.00007 | LEAK-17 | known (Copies kept; accepted warnings `dataset_duplicate_rows`, `dataset_conflicting_duplicate_rows`) | no: within noise, as noted |
| Lookup in the published file | PROV | inherent to any public dataset | not ranked |

The blind reviewer's cap and RMSE concerns do not apply: the metric is Poisson deviance, and capping training counts makes the score worse (0.233173 vs 0.233023).

**Agreed facts**

- **Size and counts:** 677,991 rows and 26,444 claims; every count equals the claims table (2022 CASdatasets version). 96.32% of rows have no claim. Seed 4267; train sides of 451,994 rows.
- **Metric:** the declared metric equals the source's (FreMTPL_1b line 35, 100 × the mean deviance), with `min_prediction` 1e-6.
- **Links:** `next_year_rows` gives 161,883 pairs: 48.7%, 48.3%, 49.2% and 60.3% of blocks 1, 3, 5 and 6. The chance rate is 0.02-0.05%, and 99.9% of pairs have the driver exactly +1.
- **Kit:** row order does not reveal IDpol (Spearman −0.0003), and the kit has no IDpol.
- **Next-year row on the train side:** 16% of test rows. Rebuilt from the shipped columns alone, the true partner is the only candidate for 54.6% of linked rows.
- **Grouped vs random:** within fold noise for honest models. The pair correlation of claims is 0.017.
- **BonusMalus:** frozen from 0→1 and 2→3; follows the French CRM rule in 4→5→6.
- **Exposure:**
  - beyond-offset gain 0.0039-0.0045; free coefficient 0.641;
  - 0 of the 1,224 rows above one year are linked;
  - exposure below one year predicts a missing next-year row.
- **Extreme counts:** the 19 rows with 5-16 claims carry 0.00126 of the deviance; capping makes the score worse.
- **DrivAge 99:** 66 of the 70 rows are in block 0, and none has a next-year row.
- **Sources:** OpenML 41214 has 678,013 rows; the help page quotes hold.

**Consistency with precedent**

The register has no flag on fremtpl2. The precedent checker's report:

- **Following precedent:** the 2022 counts, no cap and exposures above one year kept (qsar_tid_11, bemtpl97), the metric and floor, fit "approximate", the hold turned into Yes, the copies kept, the Spatial tag and screening eumtpl later.
- **Issue 1 (BonusMalus):** blanking follows the second clause of LEAK-10 as applied to zillow_prize and melbourne_housing_market, and the online_shoppers form. No precedent goes the other way.
- **Issue 2 (Exposure):** recommendation (a) follows kick `WheelType` and heart_failure `time`, both dropped once the mechanism was measured. It departs from bemtpl97 (Myunghwan, CCs of 2026-10-23 and 2026-10-26: expo retained "not verified as quotation-time information"). What sets this pass apart: the conditional test now measures the mechanism. bemtpl97 has to be reopened to match, or LEAK-10 amended.
- **Issue 3 (split):** grouping follows open_university and nba (stacked periods, recurring entities). It departs from Lennart's own CC of 2026-11-04. What sets it apart: the link to the next year carries label information that was not measured then (−0.0021), and SPLIT-24 admits an exactly built key. It differs from distribution_transformers, which held the same units with identical attributes in one non-stacked year. The precedent checker's consistency prompt (options a-d) stands.
- **DrivAge:** setting it to missing makes it consistent with VehAge in the same definition.

</details>

<details><summary>Claim audit</summary>

**Verdict:** fremtpl2 holds up for ordinary models, but four statements are wrong and the split question needs the curator. The links between IDpol blocks are real. Grouping on them changes nothing for models that score one row at a time. But the split does leak: a test row's next-year record often sits on the training side, and any model that reads other training rows can find it from the shipped columns alone. The definition also understates how much of the gain Exposure carries. Nothing was edited, built or committed.

**Answer to focus.md**

- **Are the links real?** Yes. Offsets +1..+9 give 238,273 matches. Offsets 101-109 give 62 and 1001-1009 give 107, so the links are about 1,000 times chance. The driver's age is +1 in nearly every match (only 39 matches at +0 and 34 at +2).
- **Do the blocks look like consecutive years?** Blocks 4-5-6 do: the bonus-malus moves the way the French system does. Of policies with a malus above 50 and no claim, 93.5% (4→5) and 92.1% (5→6) go down. After a claim, 35-37% go up, against 2.5% without one.
  - In 0→1 and 2→3 the bonus-malus barely moves: 5.2% and 20.5% go down, 94.5% stay the same in 0→1. So those blocks are not clean yearly renewals.
  - Blocks 5 and 6 have no full-year rows (0.2% and 0%).
- **Is "changes the score by nothing" true?** Only for models that look at one row at a time. LightGBM (Poisson objective) skill is:
  - 0.0825 on the shipped random folds;
  - 0.0813 grouped by the chains of `next_year_rows` (516,108 groups);
  - 0.0829 grouped by chains plus identical neighbours (430,379 groups, close to the notes' 430,298).
  - The fold-to-fold spread is 0.0008-0.0036. A Poisson GLM gives 0.0426, 0.0426 and 0.0425.
- **Does the pair structure leak across the 3-fold split?** Yes.
  - In every test fold, 16.0% of rows have their next-year row on the train side (36,200, 35,828 and 36,096 of 225,997), and 16% have their previous-year row there.
  - Features taken from the next-year row (via IDpol) lower LightGBM's mean deviance from 0.2325 to 0.2305 (-0.0021). That is about 10% of the model's gain over the exposure baseline. On the linked test rows alone it is -0.008 to -0.010.
  - Features from the previous-year row are worth only -0.00015. So the signal is future information, not history an insurer would have.
  - The shipped columns alone recover the next-year row. Matching on brand, fuel, region, density, power and area, with driver age +1, finds 161,897 candidate pairs, which include the true partner of every one of the 161,883 rule pairs. The true partner is the only candidate for 54.6% of linked rows. Features built this way lower deviance by 0.0041, of which about 0.0014 comes from the true partners.
  - Row order does not reveal IDpol (rank correlation -0.0003), and the participant kit has no IDpol.
- **Is IID with the ForcedIIDFromTemporal tag still right?** It is defensible, since three temporal windows cannot be built (SPLIT-14). But SPLIT-8's own text names grouping by the entity, tagged ForcedGroupedFromTemporal, for exactly this case: stacked periods with recurring entities. That is how open_university and nba were shipped. Grouping on the chains costs row-wise models nothing (0.0813 vs 0.0825). This conflicts with those precedents, so it is a question for the curator, not something I would override.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 23, 48 | Grouping on the inferred links changes nothing | notes; record, CC of 2026-11-04 | grouped vs shipped folds; features from the linked row (via IDpol, and via shipped columns only) | **refuted in part** | holds for row-wise models (0.0825 / 0.0813 / 0.0829); the next-year row is worth -0.0021 deviance and can be found without IDpol for 55% of linked rows | SPLIT-8, LEAK-17, SPLIT-29 |
| 17 | Exposure "carries about a fifth of the gain" | notes | LightGBM without Exposure; with log(Exposure) as an offset but not as a feature | **refuted** | without Exposure 0.2448 vs 0.2325, so 45% of the 0.0270 gain over the mean count; beyond the offset Exposure is still worth 0.0040 (15%); block 0 rows with exposure ≤0.25 that do not continue claim 0.258 a year, against 0.117 for those that continue | LEAK-10, LEAK-11 |
| 24 | Blocks 0-1, 2-3, 4-6 look like consecutive years; held-out skill 0.0847 vs 0.0820 | notes | bonus-malus change in pairs; blocks 1, 3, 6 held out vs 3 random draws of the same size | **numbers hold, "years" weakened** | 0.0849 vs 0.0812±0.0001; bonus-malus frozen in 0→1 and 2→3 (see above) | SPLIT-8, SPLIT-14 |
| 22, 29, 47 | About half (48-60%) of blocks 1, 3, 5, 6 repeat a row of the block before | notes; decision table | widen the offset to ±30 | holds, but only as a lower bound | rule gives 48.7/48.3/49.2/60.3%; ±30 gives 50.8/49.0/55.5/75.3%; offsets -9..-1 find 80,406 matches, 26,851 between rows the rule leaves unpaired | EV-6 |
| 18 | The scorer floors the prediction at machine epsilon | notes | read the declared metric | **refuted** (wording) | the declared `min_prediction` is 1e-6, and that is what the scorer uses | MET-11 |
| Metric | `mean_poisson_deviance` is the source's metric, on counts against expected counts | `Metric.source` in dataset.py | read the pinned reference file; score dummies on each fold | holds | line 35 defines Poisson.Deviance as 200/n × the deviance sum, i.e. 100 × the mean; each test fold has 8,160-8,465 rows with a claim (max 9-16); a mean-count prediction scores 0.2568-0.2622; all-zero predictions are floored and score 0.99-1.02; an RMSE-trained LightGBM has 1.2-1.3% of predictions floored and scores 0.2348 | MET-1, 2, 3, 5 |
| Metric | Meaning survives without the source's caps | MET-2 | deviance carried by the extreme rows | holds, with a note | the 19-row profile carries 0.00126 of 0.2534; the 16-claim row alone adds about 0.0007 to fold 0, the size of some model gaps | MET-2 |
| 14, 16 | 1,224 rows with exposure above one year, two IDpol ranges, no links to other years | notes | count, ranges, links | holds | 1.01-2.01, median 1.04; 961 rows at IDpol 1,179,653-1,199,005 and 263 at 2,214,197-2,286,947; 0 links; capping raises their rate by 11.4% | CLEAN-11 |
| 12 | First 9,387 policies (IDpol up to 24,951): 293 with claims now | notes | count | holds | 307 claims on 293 policies; the old 9,942 and the 292.6 LightGBM figure were not recomputed | PROV-13 |
| 13, 15 | 8 policies with 5-16 claims; one profile with 72 claims over 3.63 years | notes | count | holds | 7 of the 8 share the profile; its 19 rows hold 72 claims over 3.63 years | CLEAN |
| 20 | VehAge 99/100: 48 rows; 21 of the 23 aged 99 are 100 a year later | notes | `next_year_rows` | 48 holds; 21 not reproduced | the rule pairs 14 of the 23, and all 14 are 100 a year later | CLEAN-10 |
| 21 | Driver age 99: 70 rows against 5 at 98 | notes | count | holds | 70 vs 5 | CLEAN |
| 22 | 28,768 rows equal another | notes | duplicate count | wording | 28,768 rows copy an earlier row; 40,903 rows sit in groups of equal rows | writing |
| 34 | 390 rows share every factor but differ in claim count | accepted warnings | the check's formula | holds | 390 is the check's count; 1,507 rows sit in groups with more than one label | LEAK-20 |
| 4, 9, 11, 35 | 677,991 policies, 26,444 claims, 96.3% zeros, counts equal the claims table | task summary; notes | count | holds | 96.32%; claims sum to 26,444; CASdatasets commit 531aa236fc of 2022-06-23 (claims.md's "22 June" is a typo; the definition is right) | PROV |
| 25 | Tables entered CASdatasets on 14 October 2014 | notes | read NEWS | holds | `pkg/inst/NEWS` at commit 324c15c999 lists freMTPL2freq.rda 14/10/2014; the pinned NEWS.md does not | PROV |
| 26 | OpenML 41214 is the older 678,013-row copy | download description | OpenML API | holds | 678,013 rows, uploaded 2018-11-05 | PROV-8 |
| 3, 37 | Help page quotes | record | read the page | holds | "observed mostly on one year", "approximately 2011-2013", "Unknown private insurer" | EV-2 |
| 30 | Train side 451,994 rows, seed 4267 | splits comment | splits | holds | 3 × 451,994 / 225,997 | SPLIT |
| implied | Bonus-malus is known at quotation | none written | does the bonus-malus rise with the same row's claims? | holds | 4→5: 4.0% with a claim vs 3.1% without; 5→6: 2.9% vs 3.05% | LEAK-10 |
| 18, 11 | Wüthrich and Merz quotes (pp. 553-554; Eq. 5.28) | notes | none | untested | book not opened | EV-7 |

**Refuted and untested claims, ranked**

1. **The split leaks future information (P4; SPLIT-8, a Must; LEAK-17, a Must).** "Changes nothing" holds only for row-wise models. Models that read other training rows can find a test row's next-year record from the shipped columns and gain up to about 10% of the model's gain.
   - What it changes: rankings between such models and gradient-boosted trees can shift by about 0.001-0.002 deviance.
   - Mildest remedy: ship ForcedGroupedFromTemporal, grouped on the chains from `next_year_rows` with the offsets made symmetric. Row-wise scores do not move. Otherwise, keep IID and rewrite the notes to say "no effect for row-wise models; a policy's next year can be recovered from the features". The curator decides (consistency check, case 2).
2. **Exposure's share of the gain is understated (P4; LEAK-10, a Must, against LEAK-11).** Exposure carries 45% of the gain, not a fifth. The part beyond pure time insured, which a later cancellation could create, is 0.0040 (15%).
   - Mildest remedy: correct the note with these numbers. The curator re-confirms the keep with the right numbers; this sits on the "weak vs strong suspected leak" tension in principles.md.
3. **"Consecutive years" is uncertain for blocks 0-1 and 2-3 (P4; SPLIT-8).** The bonus-malus is frozen there.
   - Mildest remedy: a note that says this, and that the link counts are lower bounds.
4. **Wording (P6 and procedure).**
   - "Machine epsilon" should read 1e-6 (MET-11).
   - 28,768 copies of an earlier row (40,903 rows in groups of equal rows).
   - Say which links the 430,298 groups use.
   - "21 of 23" is not reproduced by the shipped rule.
5. **Untested.**
   - The Wüthrich and Merz page quotes.
   - The old count of 9,942 and the 292.6 LightGBM figure.
   - Whether `eumtpl` duplicates this dataset (PROV-6/7, still open).

</details>

<details><summary>Column audit</summary>

**fremtpl2 column audit (column-auditor, 2026-11-04)**

**Focus question: direct answer**

- **The 48-60% claim is true.** `next_year_rows` gives exactly the same counts: 54,571 / 63,800 / 20,924 / 22,577 rows, which is 48.7%, 48.3%, 49.2% and 60.3% of blocks 1, 3, 5 and 6.
  - Chance is far lower. Shuffling row contents within each block gives 16 pairs. Using IDpol offsets of 1,001-1,009 instead of 1-9 gives 75. The real count is 161,883.
  - Dropping the driver-age condition gives 162,019 pairs, and 99.9% of them still have the driver exactly one year older. These are the same policies in consecutive years.
- **"Changes the score by nothing" holds for the shipped features.** LightGBM Poisson deviance is 0.23269 on the shipped random folds (fold SE 0.0015) and 0.23224 when split by pair chain (516,108 groups, SE 0.0007).
- **Leak across the 3-fold split: real but small.**
  - 31% of test rows have a linked row on the train side.
  - Adding that row's ClaimNb and Exposure as features lowers deviance by 0.0004 (0.0003-0.0005 on each fold). Most of it comes from the later-year row (0.0003); the earlier-year row gives 0.0001.
  - Removing IDpol does not hide the links: 52.5% of later rows have exactly one candidate predecessor in the shipped features (median 1, p90 3).
  - The participant kit and row order are clean: no IDpol, and Spearman correlation of row position with IDpol is -0.0003.
- **Keep IID with ForcedIIDFromTemporal** (SPLIT-8, SPLIT-31; SPLIT-25 rules out grouping on inferred links).
  - One consistency note: SPLIT-8's text points to ForcedGroupedFromTemporal "when the periods are stacked and the entities recur". The difference here is that the entity is inferred and grouping makes no measurable difference.
  - The splits_comment should add the 0.0004 lookup gain and the link reconstructability.
- **Exposure below 1 does predict a missing next-year row** (focus item 4). Share of rows with a next-year row: 26% at exposure ≤0.25, 93.5% at a full year. Within each exposure bin a claim lowers it (0.19 vs 0.27, 0.28 vs 0.35, 0.44 vs 0.51, 0.47 vs 0.53).
- **The 1,224 rows with exposure above 1 have no links** (claim 16 confirmed): 0 of 263 in block 2 have a next-year row, and none of the 961 in block 1 has an earlier-year row.
- **The pairs reveal two column problems that matter more than the split:** BonusMalus and Exposure. Both are ranked below.

**Column table**

| column | meaning (CASdatasets help page) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| ClaimNb (target) | claims during the exposure period | outcome | int64, 0-16, matches freMTPL2sev | fine | USE-5, LEAK-26 |
| Exposure | period of exposure, years | **partly no**: a short exposure can record a cancellation after a claim | float64, 1 day to 2.01 | leak, kept on purpose by the curator; the note misstates its size | LEAK-10 |
| VehPower | "power of the car (ordered values)" | yes | int64, 4-15; 2,926 rows at 15 against 2,350 at 14 | fine; a question whether 15 means "15 or more" (the source does not say) | CLEAN-14 |
| VehAge | vehicle age, years | yes | float64; the 48 rows at 99 or 100 set to missing; 68-85 kept as unusual | fine | CLEAN-10, CLEAN-11 |
| DrivAge | driver age, years | yes | int64, 18-100; **70 rows at 99 against 5 at 98 and 3 at 100** | cleaning problem | CLEAN-10 |
| BonusMalus | French bonus-malus coefficient, 50-350 | **likely no in blocks 0-4**: recorded after the row's own claims | int64, 50-230; numeric is correct | **leak (likely)** | LEAK-10 |
| VehBrand | brand ("unknown categories") B1-B14 | yes | category, 11 levels | fine | CLEAN-14 |
| VehGas | Diesel or Regular | yes | category | fine | CLEAN-14 |
| Area | A (rural) to F (urban centre) | yes | ordered A<…<F, correct order; exactly log-density bands with cuts at 50, 100, 500, 2,000 and 10,000 (3 boundary values fall in two areas) | fine (a coarse copy of Density, published by the source) | CLEAN-14, CLEAN-5 n/a |
| Density | inhabitants per km² | yes | int64; 27,000 is the most common value (10,514 rows, all Ile-de-France, likely Paris rounded) | fine | CLEAN-11 |
| Region | 22 regions before 2016 | yes | category | fine | CLEAN-14 |
| IDpol (dropped) | policy id; its block is the inferred year | encodes the period | dropped | fine | CLEAN-3, LEAK-10 |
| sev_claims (dropped) | the target's source | outcome | dropped | fine | — |

My run of the dtype probe flags 0 of 10 columns but reads no codebook: CASdatasets is neither UCI nor OpenML, so I read the help page by hand.

**Problems, ranked**

**1. BonusMalus is likely recorded after the claims in blocks 0-4 (P4, LEAK-10 Must; likely, not shown; EV-6).**

Blocks 4-6 serve as the control: there BonusMalus behaves like a value taken at the start of the year.
- From year to year it follows the French bonus-malus rule. Among rows with no claim and a coefficient above 50, 92-94% are lower in the next row. A claim raises it in 35-37%.
- In 4→5 and 5→6 pairs (drivers 30+, coefficient ≥100), it is linked to the claims of the year before (×8.3 and ×5.7), not much to its own row's claims (×1.4 and ×1.9).

In blocks 0-3 it looks like one value per policy, recorded after the claims:
- It is frozen across the two years. Among claim-free rows above 50 it drops in only 2-6% of pairs, and a claim raises it in only 1-4%.
- It is linked to its own row's claims as strongly as to the other year's (×4.3-5.9 against ×4.8-6.2).

The decisive footprint is the first malus step from the floor, 62-63 (50 × 1.25), among drivers 30+:

| rows | share at 62-63, with a claim | share at 62-63, without |
|---|---|---|
| blocks 0-3 | 5.3-6.8% | 1.5-1.7% |
| block 4, no next-year row | 7.8% | 1.3% |
| block 4 with a next-year row, and blocks 5-6 | 1.1-2.2% | 1.4-1.6% |

Choosing riskier drivers would not pile claimants onto exactly one malus step.

Size of the effect (LightGBM with log(Exposure) as an offset, shipped folds):
- Removing BonusMalus costs 0.0131 deviance in blocks 0-3 and 0.0110 in block 4, but **gains 0.0005 (SE 0.0003) in blocks 5-6**.
- Over all rows, BonusMalus carries 0.0112 of the 0.0269 total gain over the mean count (42%), the largest of any feature.
- The affected rows are blocks 0-3 plus block 4's rows without a next-year row: about 577k rows (85%).

Remedy, mildest first; the call is the curator's:
- (a) Look for a source statement first (LEAK-3). My search found none.
- (b) Blank BonusMalus in the rows where the late value can be located (LEAK-10 second clause, as for zillow and melbourne). Those rows are found only through the inferred IDpol blocks.
- (c) Drop BonusMalus. In blocks 5-6 it adds nothing measurable.
- Keeping it with a note departs from a Must, so it needs an amendment, not an exception.

The whole freMTPL2 literature uses BonusMalus as its main factor. That weighs for (a) before acting.

**2. Exposure: the mechanism is measured, and the note gives the wrong number (P4, LEAK-10; kept by the curator, as in bemtpl97, a consistent precedent).**

- Rows with an earlier-year row, so started before the year, claim at 0.255 a year when exposure is ≤0.1, against 0.056 at a full year (4.5×). Within each exposure bin a claim also lowers the chance of a next-year row (above).
- Exposure as a free feature against the source's form (exposure as an offset, Noll et al.): 0.23269 vs 0.23654. That is 0.0039 better on every fold (0.0033-0.0044), or 14% of the gain. 42% of that 0.0039 comes from rows with exposure ≤0.1.
- The notes' "about a fifth of the gain" (0.2534 vs 0.2595) is the proportional, legitimate time-at-risk part. The part that can carry the leak is the 0.0039, and the notes do not give it.

Remedy: correct the note's number (the mildest). Alternatively, score the rate times Exposure, with Exposure as a scoring column. That is the source's own form, but it needs a new metric in `src/data_foundry/v2/metrics.py`. Curator's call.

**3. Pair structure across the split (P4, SPLIT-8, SPLIT-31).** A lookup gains 0.0004, and 52.5% of the links can be rebuilt without IDpol. Keep IID and add a sentence to splits_comment.

**4. DrivAge 99 is a default (P7, CLEAN-10 Should).**
- 66 of the 70 rows are in block 0.
- None of those 66 has a next-year row, even with the driver-age condition dropped. 62.7% of block 0 does.
- Their claim frequency is 0.081.

The notes keep 99 "as possible" without giving a reason. The cheap fix is missing for the 66 rows, the same treatment as VehAge 99.

**5. VehPower 15 may be a top band (P7, CLEAN-14).** A question, no change unless the source says so.

**6. Wording (writing.md).** The metric bullet says "machine epsilon" but the Metric declares 1e-6, as the checklist already noted.

Sources:
- [CASdatasets freMTPL help page](https://dutangc.github.io/CASdatasets/reference/freMTPL.html)
- Searched for a statement on BonusMalus timing and found none. Closest result: [burning-cost, causal inference on freMTPL2 BonusMalus](https://burning-cost.github.io/2026/03/28/causal-inference-fremtpl2-bonusmalus-dml), which argues BonusMalus builds up from past claims and uses log(Exposure) as an offset, without addressing timing.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The IID split with `ForcedIIDFromTemporal` is still the right choice. I found nothing that needs a re-split. Three things need a note or a wording fix. One of them is a small leak of the dataset itself, not of the split: it is just as large under a grouped split.

**Direct answer to focus.md**

- **The links are real.** `next_year_rows` gives 161,883 pairs, and 99.5% of them have an IDpol offset of +1. Three checks show they are not chance:
  - Shuffling IDpol within each block leaves 28 matches.
  - Requiring a driver age change of 0, +2 or −1 instead of +1 leaves 25, 21 and 19 matches.
  - So the chance rate is about 0.02%, and the pairs are one policy in two consecutive periods.
  - Rows that reappear one block later: block 1 48.7%, block 3 48.3%, block 5 49.2%, block 6 60.3%. Links run 0→1, 2→3 and 4→5→6.
  - Separately, 96,476 pairs of adjacent IDpols share all rating factors, and in 99.9% of them the two exposures add up to at most one year. These look like one policy split into two records within a period.
  - 61% of rows are in a linked group of two or more. 66.8% of the cross-year pairs and 66.5% of the same-period pairs are cut by the shipped folds.
- **"Changes the score by nothing" holds for ordinary models.** I scored by Poisson deviance (lower is better), comparing each row's score under the shipped folds with its score under folds grouped by the links, using a cluster bootstrap:

  | Model | Shipped | Grouped by chain (3 seeds) | Shipped minus grouped |
  |---|---|---|---|
  | LightGBM | 0.23265 | 0.23238–0.23245 | +0.0002 to +0.0003 (SE 0.0002); the random split is not optimistic |
  | Poisson GLM | 0.23970 | 0.23976 | −0.00007 (SE 0.00003) |
  | Over-flexible LightGBM, linked rows only | | | −0.0003 (SE 0.0003) |

  - Two random seeds differ from each other by up to 0.0002.
  - The LightGBM–GLM gap is 0.0071, so the ranking is the same under every split.
  - Chains plus same-period neighbours give 430,379 groups. That agrees with the 430,298 in the notes, and the skill matches too: 0.0820 shipped against 0.0825 grouped.
- **The links do leak, but through the dataset, not across the split.** Whether a policy has a later-period record can be found from the shipped features alone (same brand, fuel, region, density and power; driver one year older). A later record means the policy was renewed rather than ended, and renewed policies claim far less: in block 0, 0.070 claims per year against 0.141.
  - Using only that fact, with no labels, lowers the deviance by 0.00170 on the shipped folds (−0.00134 to −0.00206 per fold).
  - Under the grouped folds it lowers it by 0.00181. Grouping does not remove it.
  - Control: the same feature built from rows five years older gives +0.00003, so the gain is the policy's own later record.
  - The earlier period's claim count, which is legitimate history for a renewal, is worth only −0.00016.
  - It is the same mechanism as the Exposure/cancellation note in the record (claim 17).
- **Is IID with the forced tag still right?** Yes, under SPLIT-8.
  - The calendar years of the blocks are unknown, and each sub-portfolio has only 2–3 periods. That gives one later window, not the three that SPLIT-14 asks for.
  - The "blocks are years" reading is also uncertain for blocks 4–6. Block 4's full-year rows almost never continue (0.1%), and blocks 5 and 6 have 73 and 0 full-year rows.
- **The kit does not reveal IDpol.** IDpol is not in the kit, and the kit's row order is unrelated to it (Spearman −0.0003).
- **Exposure above one year:** none of the 1,224 rows has a link in either direction (961 in block 1, 263 in block 2), so claim 16 is right.
- **Exposure below one year predicts no next-period link:** link rate 0.436 against 0.982 in block 0, 0.272 against 0.001 in block 4, 0.530 against 0.863 in block 5. This fits the cancellation mechanism.

**Problems, ranked**

**1. P4, LEAK-10 / LEAK-17 (weak, Should-strength): a renewal can be seen from the policy's later record.**
- Evidence: as above, −0.0017/−0.0018 deviance under random and grouped folds alike. That is 0.7% of the deviance and about 6% of LightGBM's gain over the mean-count baseline (0.2595 → 0.2326).
  - A participant who matches only against training rows gains −0.0012 on the shipped folds and −0.0004 on grouped folds. The renewal fact without labels already accounts for −0.00094 of that.
  - The over-flexible LightGBM run shows no such gain, so models that do not build the feature on purpose do not seem to pick it up.
  - Not checked: whether in-context models (TabPFN) find it. That needs a GPU run.
- Rule: LEAK-17 says to group, but grouping does not fix it here (EV-1 measurement). Only holding out the latest period removes it, and that gives a single window (fails SPLIT-14). The tension "weak leak against the data as published" applies: keep it with a note.
- Mildest remedy: add to the "Potential leak, kept on purpose" bullet. "A policy's next-period record, findable from the features, marks a renewed policy; continuing rows claim at half the rate; matching on it gains 0.0017 deviance under random and grouped folds alike."

**2. P4, SPLIT-8 (Must: the cost has to be measured): the cost in the notes has the wrong sign.**
- Evidence: "skill 0.0847 against 0.0820 for random rows of that size" compares different rows. On the same rows (blocks 1, 3 and 6, with training on blocks 0, 2, 4 and 5, 58% of the data):
  - LightGBM: 0.23316 against 0.23267 under the shipped folds, +0.00049 (SE 0.00016); skill 0.0843 against 0.0863.
  - GLM: +0.00009 (SE 0.00005).
  - So the forced IID split is slightly optimistic, by 0.2%, and the ranking is unchanged.
- Remedy: a wording fix in the "Split forced IID" bullet. Report the deviance on the same rows. No re-split.

**3. P4, SPLIT-8 letter and consistency: why IID and not `ForcedGroupedFromTemporal`.**
- Evidence: SPLIT-8 names the grouped regime when periods are stacked and entities recur across them, which is the case here. The precedents nba_players_2016_2019 and open_university_learning_analytics_dataset were grouped, but they had an entity id in the release.
- What sets this case apart:
  - There is no key in the release. The entity can only be rebuilt from the dropped IDpol by an inferred rule; SPLIT-24 would still allow grouping on it, given the 0.02% chance rate.
  - Grouping changes nothing (problem 1 and the table above), and it does not remove the renewal signal.
  - Most policies priced are renewals, which are known entities (USE-10), so a cold-start grouped split mirrors the use case no better.
- Remedy: one sentence in `splits_comment` or in the Decision text, recorded as Lennart's reason. Optionally a consistency-check line against those two precedents.

**4. Quality / wording (EV-6, EV-8).**
- The notes and the decision text say the pairs "look like" one policy. With the measured null (161,883 against 28) this can be stated as a fact.
- The same-period neighbour pairs, with exposures summing to at most one year, support `splits_comment`'s "another record of the same year".
- Remedy: a wording edit.

**Pointer for the leak auditor (not a split issue):** BonusMalus barely changes between linked records in blocks 0→1 and 2→3, but it moves normally in 4→5→6.

| | Blocks 0→1 | Blocks 2→3 | Blocks 4→5→6 |
|---|---|---|---|
| BonusMalus falls after a claim-free period (start above 50) | 5% | 21% | 93% / 92% |
| BonusMalus rises after a claim | 1% | 4% | 35% / 37% |

So in blocks 0–3 the BonusMalus value may be one reading copied to both records. If that reading was taken after the earlier record's period, it falls under LEAK-10. I did not settle this.

**Judgment record**

Validity: SPLIT-1/SPLIT-8 hold (forced IID; the one block window costs +0.0005 deviance); SPLIT-29/30 not triggered (grouped ≈ random); LEAK-17/LEAK-10 triggered weakly through the renewal record, keep with a note. Not applicable: SPLIT-9/10, gap and season (no dates).
For the curator: the wording of problem 2, and the note for problem 1.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (pricing actuary, French motor TPL): fremtpl2**

**Fit: approximate.** The rating factors, the claim counts and the policy-year unit match how a French insurer prices claim frequency, but there are no dates, so the next year cannot be held out. Realised Exposure is a free feature, and part of it is known only after the quote (USE-8, SPLIT-8).

**Metric scores the decision: yes.** Mean Poisson deviance of the counts against the expected counts.

**Focus question, answered directly**

**1. Are the links real? Yes, but "consecutive years" only holds well for blocks 0→1 and 2→3.**
- The `next_year_rows` rule finds 161,883 pairs.
- The same rule at wrong offsets finds almost nothing: 62 matches at 101-109 and 90 at 501-509. The chance rate is about 0.05%.
- The bonus-malus moves the way the French legal bonus-malus coefficient (CRM, Code des assurances A121-1) predicts: ×0.95 per claim-free year, ×1.25 per at-fault claim.
  - Earlier BM above 50 and no claim: the later BM falls in 37% of pairs (10th percentile of the ratio 0.941). It rises in 2.0%.
  - Earlier row with a claim: the later BM rises in 10.4%.
- In block 0, rows insured the full year have a next-year row 98.2% of the time, against 43.6% for rows with Exposure below 1. That is renewal versus termination.
- None of the 1,224 rows with Exposure above 1 is linked. Claim 16 is confirmed.
- Blocks 4-5-6 behave differently:
  - Only 0.2% of their linked rows are full-year records.
  - In 63-66% of the 4→5 and 5→6 pairs, the two exposures add up to at most 1.01.
  - So these look like one contract year split across two accounting years, not two full years. The notes' "consecutive years of three sub-portfolios" overstates this.

**2. "Changes the score by nothing": true for an honest model.**
- Setup: LightGBM Poisson with Lorentzen and Mayer's parameters, the declared metric, skill measured against Exposure × the portfolio frequency.

| Folds | Skill (SD) | Deviance |
|---|---|---|
| Shipped | 0.0797 (0.0002) | 0.2332 |
| Grouped by the literature's 9-factor key | 0.0791 (0.0025) | 0.2334 |
| Grouped by key plus inferred links (378,542 groups) | 0.0794 (0.0012) | 0.2333 |

- All three are within one fold SD of each other.
- Last year's claim as a feature (the legitimate history of a known policy, USE-10) adds +0.00001 deviance, i.e. nothing. The BM already carries it, as the CRM is designed to.

**3. Does the pair structure leak across the random split? Yes, through one backward channel, and only if a participant goes looking for it.**
- When a test row's next-year row sits on the training side, a rise in that row's BM reveals this year's claim: P(claim) is 0.238 against a base of 0.037.
- I stacked a Poisson GLM on the honest out-of-fold predictions:
  - Using the IDpol links: skill 0.0797 → 0.0843 (+0.0046).
  - Without IDpol, linking from shipped columns only (same brand, fuel, region, density, power and area; driver one year older; car the same age or one older; BM at least 1.2× higher): 0.0854 (+0.0057), on 3 of 3 folds (+0.0053, +0.0064, +0.0056).
- That is about 10× the gap between random and grouped folds.
- Grouping by the inferred chain halves it (0.0794 → 0.0818, +0.0024).
- Grouping by car-and-commune cell (88,849 cells, largest 940 rows) closes it by construction. Honest skill there is 0.0774 (SD 0.0025), but part of that drop is a change of task (unseen cells).

**4. Is IID with `ForcedIIDFromTemporal` still right? Defensible, and I would keep it.**
- Out of time is not harder. Training on blocks 0, 2, 4 and 5 and testing on 1, 3, 6 gives skill 0.0824 (actual/expected 1.014), against 0.0754 for random rows of the same size. This agrees with the notes' 0.0847 vs 0.0820.
- SPLIT-8 applies: no dates, at most 3 inferred periods per sub-portfolio, and a key the source never states.
- SPLIT-8's literal condition for `ForcedGroupedFromTemporal` ("periods stacked, entities recur") is met only through inferred keys.
- So for the curator: keep IID, but name the BM channel and its size in `splits_comment` and in the decision. Or group by the inferred chain, which costs no measurable skill and halves the channel.

**Q1-Q5 from the actuary's seat**

1. **Inputs.**
   - Every rating factor is known when I quote. The BM is the CRM at renewal.
   - Realised Exposure is not fully known. At quote I know the contract term and start date, not a later cancellation.
   - Missing inputs I would always have: new business vs renewal (tenure), start date, a product or sub-portfolio code (blocks 4-6 are almost all part-year records), vehicle value or model group, cover or deductible, number of drivers.
2. **Target.** The expected claim count, i.e. frequency λ(x) × term, is exactly what I price with; severity is a separate model. I want a positive mean, not a class. Claims with a recorded cost (the 2022 counts) are fine.
3. **Unit and test data.**
   - One row is a policy × accounting-year slice, the unit of a frequency model's data.
   - The test I really face is next year's renewals plus new business. Random rows stand in for that. The cost measured above is nil, but test rows get backward information (point 3).
4. **Would I use it?** Yes, as a model-selection benchmark. I would trust it more if Exposure entered as an offset. I would distrust gains from very flexible models that use Exposure non-proportionally (gap 1).
5. **Metric.** Yes, see the last section.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **Exposure as a free feature: the largest effect.**
   - LightGBM with log(Exposure) as an offset (Exposure not a feature): skill 0.0644 (deviance 0.2371). With Exposure as a feature: 0.0797 (0.2332).
   - So 19% of the skill (0.0039 deviance) comes from using realised exposure non-proportionally.
   - Claims per year fall from 0.172 at Exposure ≤ 0.1 to 0.055 at a full year.
   - In block 0, short rows with no next-year row claim 0.144 per year, against 0.095 for short rows with one. That fits terminations that follow claims, which is information from after the quote.
   - Under USE-8 a kept leak does not change the fit. But the notes' "about a fifth of the gain" (0.2595 → 0.2534) measures the proportional, legitimate use. The size of the kept potential leak is the separate 0.0039 (LEAK-30 wording).
2. **No year (SPLIT-8).** The measured cost is nil or negative (0.0824 vs 0.0754).
3. **The backward BM channel.** +0.0046 to +0.0057 skill for a participant who exploits it; none for a standard model.
4. **Missing standard tariff inputs and a mixed portfolio** without a product code. The frequency level differs by block, from 0.0863 to 0.0586 claims per year.

**What an expert would change (no file edited)**
- **"Potential leak" bullet:** report the non-proportional share (0.2371 → 0.2332, offset vs feature) as the size of the kept leak.
- **`splits_comment` and the decision:** add the backward BM channel and its size (+0.0057 relinked from shipped columns, +0.0024 under chain grouping). Optionally group by the chain, the `ForcedGroupedFromTemporal` variant of SPLIT-8.
- **Decision text:** qualify blocks 4-5-6 as split contract years.
- **Metric bullet:** it says "machine epsilon", but the definition declares `min_prediction` 1e-6 (MET-13). The prep report already flagged this.

**Metric: yes (MET-1, MET-5, MET-8)**
- Poisson deviance is the criterion the source chose deliberately: Noll et al. and Wüthrich and Merz Eq. 5.28.
- Lorentzen and Mayer's exposure-weighted deviance of frequencies ranks models the same way, since d(N, μ) = v·d(N/v, μ/v).
- It is strictly consistent for the mean, so it rewards honest expected counts. It scores the unit I price (a policy-year).
- No threshold or top-k applies (MET-6, MET-7, MET-9 not applicable). Exposure enters through the prediction, as in bemtpl97 (MET-2).
- What I would choose: the same deviance on λ̂(x)·Exposure with log Exposure as an offset. A generic benchmark cannot enforce that, so the declared metric stays. Actual/expected and Gini are checks a practitioner adds, not the score.

**Sources**
- [CASdatasets freMTPL help page](https://dutangc.github.io/CASdatasets/reference/freMTPL.html)
- Lorentzen and Mayer, Responsible ML material:
  - [Introduction](https://lorentzenchr.github.io/responsible_ml_material/xai_1_introduction.html): the group_id is rows with identical risk factors, "We assume that rows in such a group represent the same policy, even if their IDpol varies".
  - [Explaining models](https://lorentzenchr.github.io/responsible_ml_material/xai_2_explaining_models.html): LightGBM pseudo-R² is 6.0% on a random split vs 5.0% grouped, on the old OpenML counts (41214). That gap does not reproduce on the 2022 counts.
- [Légifrance, Code des assurances A121-1](https://www.legifrance.gouv.fr/codes/id/LEGIARTI000036754143/2018-04-01/) and [UFC-Que Choisir on the CRM](https://ain.ufcquechoisir.fr/wp-content/uploads/sites/81/2020/06/Coefficient-de-Réduction-Majoration.pdf): premium = reference premium × CRM, +25% per at-fault claim.
- Noll, Salzmann and Wüthrich 2018 (SSRN 3164764), as cited in the definition.
- Search hits I looked at but did not use: [OpenML 41214](https://api.openml.org/d/41214), [Hugging Face mirror](https://huggingface.co/datasets/mabilton/fremtpl2/blob/main/README.md).

</details>

<details><summary>Blind review</summary>

**Verdict:** include with changes. This is the standard real-world claim-frequency dataset and has real signal, but as prepared a handful of extreme, near-duplicate claim counts and an unweighted squared-error framing can decide the ranking.

**Concerns, most serious first**

1. **A few extreme counts from one entity dominate squared error, and a random split rewards memorising them.**
   - In the sample, ClaimNb runs 0 (192,574), 1 (6,997), 2 (402), 3 (20), then 4, 4, 5, 5, 6, 9, 11.
   - The 5, 6, 9 and 11 all share one risk profile: VehPower 4, VehAge 12/13, DrivAge 52/53, BonusMalus 50, B1, Regular, Area D, Density 824, Languedoc-Roussillon. Three of them have Exposure 0.08. This is almost certainly one policyholder or fleet split into many short records.
   - In 3-fold random CV, LightGBM learns the profile from the sibling rows in train. It predicts 1.23 claims for test rows of this cluster, against a population mean of 0.04. It also predicts 2.87 for a sibling row with 0 claims.
   - These 8 rows (0.004% of the sample) carry 2.6% of the model's squared error. Dropping them moves RMSE from 0.2065 to 0.2038. That shift is larger than the whole gap between GBM and linear regression (0.0012, bootstrap SD 0.0003).
   - The full 678k table probably holds more rows of this cluster. Older versions have ClaimNb up to 16.
   - **Change:** cap ClaimNb at 4, as is common in the actuarial literature (from memory; I did not confirm a citation). Better still, also score with Poisson deviance (see 2) and/or use a grouped split (see 3).

2. **The framing is not how the prediction is used.**
   - The real use: an insurer's pricing team predicts expected claim frequency at policy inception to set the premium. The source treats Exposure as the observation period: "The period of exposure for a policy, in years".
   - Practice models ClaimNb/Exposure with Exposure as a weight, or uses Poisson with a log(Exposure) offset, and scores with Poisson deviance. scikit-learn's reference example does this: "model the frequency y = ClaimNb / Exposure … use Exposure as sample_weight".
   - Here Exposure is a plain feature and the target is a raw count. Exposure alone gives R² 0.008. All features give R² 0.033 (L2) or 0.036 (Poisson objective), with Poisson D² about 0.09–0.10.
   - Realised exposure is partly known only after the fact (mid-year cancellations, possibly triggered by a claim). Claim rate is not monotone in exposure: 6.7% for exposure 0.75–0.99 against 5.5% for exactly 1.0. This is accepted actuarial practice when exposure is an offset, but as a free feature the model can learn post-hoc effects.
   - **Change:** declare Poisson deviance as the metric if the harness allows it. If it is RMSE-only, keep the count target but cap it. Document Exposure as an exposure measure, not a risk factor.

3. **Near-duplicate rows: grouped versus random split.**
   - The literature warns about this for this exact dataset. Lorentzen's material uses grouped splitting on a group_id of identical risk factors: "all their risk factors identical … their 'IDpol' values are very similar … their exposures and claim frequencies are identical". Ignoring the groups raised LightGBM test pseudo-R² "6.0% vs. 5.0%" on the older 678,013-row version.
   - In this sample, 31,353 rows (15.7%) share all nine risk factors with another row, and 7,578 rows also share Exposure (6,816 of them at Exposure 0.08).
   - In this version, though, claims mostly do not repeat within groups. If a row has a claim, the chance that a group sibling does too is 1.0%, versus 1.9% when the row has none. Grouped and random 3-fold CV gave the same score (R² 0.0333 vs 0.0330).
   - So outside the extreme cluster in item 1, I measured little leakage on the 200k sample.
   - **Change:** prefer GroupKFold on the risk-factor tuple. It is cheap and also contains the cluster in item 1. At minimum, document that the IID split is optimistic for memorising models.

4. **Version and provenance are unclear.**
   - The 677,991 rows match the current CASdatasets reference ("dim(freMTPL2freq)" gives 677991 × 12). The CASdatasets NEWS only records a new freMTPL2freq.rda file dated 2024/09/17. OpenML 41214, the Hugging Face copy and older versions have 678,013 rows. The Hugging Face copy documents 9,117 ClaimNb mismatches with the severity file.
   - What changed in the 2024 update (22 rows removed, ClaimNb corrections?) is undocumented in what I could read.
   - VehAge has 14 NaN in the sample. Older versions have none; my best guess is about 47 in the full table, but I cannot say where they come from. Region uses full names rather than R-codes.
   - The first-listed source is a Kaggle mirror whose content I could not read.
   - Row order shows no drift in claim rate (3.2–4.2% across 40 position bins). The ordered high-claim block of the old version is therefore absent, which is consistent with a corrected or re-sorted release.
   - **Change:** cite CASdatasets 1.2-x as the source, record the version, and note the VehAge NaNs.

5. **Signal is low and model differences are small.**
   - R² is about 3%. GBM beats linear regression by 0.0012 RMSE, and GBM-Poisson beats GBM-L2 by 0.0003 (SD 0.0003, not significant) on a 67k-row test fold.
   - With 226k test rows per fold on the full data it is scoreable, but it will separate model classes rather than close competitors.
   - This is realistic for insurance frequency and the task is not trivial, but it amplifies items 1 and 2.

6. **Preparation is mostly fine (minor).**
   - IDpol is dropped, which is correct.
   - The categoricals are typed as category.
   - Values are plausible: DrivAge 18–100, BonusMalus 50–228 (source range 50–350), Density 1–27,000.
   - Area is a deterministic binning of Density (A ≤ 50, B 50–100, C 100–500, D 500–1993, E 2001–9850, F ≥ 10008). It is redundant and ordinal but stored as an unordered category. That is harmless; just note it.
   - VehPower is an ordinal int, which is fine.

**What I could not check**
- Only the 200k sample was available. The size of the extreme cluster, the duplicate rate and the grouped-versus-random gap on the full 677,991 rows are extrapolated.
- I could not read the Kaggle page (it renders with JavaScript).
- I could not read the CASdatasets manual PDF (no PDF tools were available) or the SSRN case study. So I could not confirm what changed in the 2024 release, where the VehAge NaNs come from, or the exact capping convention in the original paper.
- Without IDpol I could not link to the severity file or confirm the groups by consecutive policy IDs.
- task.md does not state the evaluation metric.

Sources:
- [CASdatasets freMTPL reference](https://dutangc.github.io/CASdatasets/reference/freMTPL.html)
- [CASdatasets NEWS](https://github.com/dutangc/CASdatasets/blob/master/NEWS.md)
- [Lorentzen, Responsible ML – XAI](https://lorentzenchr.github.io/responsible_ml_material/xai_2_explaining_models.html)
- [Hugging Face mabilton/fremtpl2 README](https://huggingface.co/datasets/mabilton/fremtpl2/blob/main/README.md)
- [scikit-learn Poisson regression example](https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html)
- [OpenML 41214](https://api.openml.org/d/41214)

</details>

<details><summary>Task gamer</summary>

**Verdict:** the task can be gamed only slightly. Statistics over all rows (train and test) of the records that share a policy's features gain about 0.0006 on a score of about 0.2326, which is 0.2–0.3%. A larger flaw is already inside every honest model: the realised `Exposure` carries outcome information, worth 0.0045 (about 2%). Sibling labels across the split add nothing.

Honest baselines (mean Poisson deviance over 3 folds, lower is better):
- Default LightGBM with a Poisson objective: **0.233023** (folds 0.233246 / 0.230466 / 0.235358).
- Tuned LightGBM (early stopping inside train): **0.232631** (0.232679 / 0.230103 / 0.235110).
- Noise from adding a random column: ±0.0002 per split on the default model (means 0.233036 to 0.233238); +0.00007 on the tuned model.
- For reference: constant prediction 0.2595; exposure × training frequency 0.2534.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Realised `Exposure` used as a free feature instead of a pure time-at-risk offset | 0.237547 (offset only) | 0.233023 (default baseline) | 0.0045 (0.0039 to 0.0052) | Unsure. Only if the record's end date is fixed when the policy is quoted. | Merge records into one row per policy-year, or restate the prediction point as "period at risk known" |
| 2 | Record-structure statistics over train+test: number of records with identical features except `Exposure` (`gsize_all`), and their summed exposure (`gexp_all`) | 0.233023 / tuned 0.232631 | 0.232316 / tuned 0.232082 | default 0.00071 (0.00019 to 0.00108); tuned 0.00055 (0.00012 to 0.00080) | No. It uses the policy's other records in the same year, including later ones and their realised exposure. | Merge feature-identical records into one policy-year row (summed `Exposure` and `ClaimNb`) |
| 3 | Labels of training siblings (same features except `Exposure`) | 0.233023 | 0.232953 (credibility rule, `a` chosen inside train); 0.232583 (LightGBM with out-of-fold sibling features) | 0.00007, within noise; the LightGBM gain of 0.00044 comes entirely from the label-free part of #2 (#2 + labels 0.232321 vs #2 alone 0.232316) | Partly: past records of the policy would be known (experience rating) | None needed beyond #2 |

**Flaws that hurt an honest model:** none found. Every training-row choice I tried stayed within noise or made the score worse:

| Honest choice | Default model | Tuned model |
|---|---|---|
| Cap training `ClaimNb` at 4 | 0.233173 (worse) | 0.232735 (worse) |
| Drop training rows with `ClaimNb` > 5 (as Wüthrich–Merz do) | 0.233405 (worse) | not run |
| Drop training rows with `Exposure` > 1 | 0.232968 | 0.232682 |
| Drop the policy-ID ≤ 24500 block from training (only possible with the source file) | 0.232958 | not run |

Capping or dropping the extreme counts hurts because the test folds keep them.

**Findings**

**1. Realised `Exposure`.** Claims per year at risk fall steeply with the length of the record:
- 1.03 for records of 0.01 years or less;
- 0.24 for 0.01 to 0.05 years;
- 0.12 for 0.1 to 0.25 years;
- 0.055 for full years.

Against an offset-only model:
- Records of 0.25 years or less have 3,436 claims where the offset predicts 2,295.
- Records of 0.01 years or less have 104 claims where it predicts 9.
- Full-year records have 9,216 claims where it predicts 12,013.

6,877 records last 1 to 3 days (stored at day precision as k/365 or k/366). They have a frequency of 1.27 per year.

Records that end early carry the claims, which fits contracts cancelled or split after a claim. Wüthrich–Merz write that "policy renewals during the year account for two separate records". arXiv 2604.02400 reports higher frequency for contracts cancelled mid-term. So `Exposure` is partly set by events after the quote, while the task's prediction point is the quote.

What would decide it: whether a record's end date is known when the policy is quoted (mid-year new business) or set during the year (cancellation, vehicle change, record split). The mildest fix is one row per policy-year. If that is impossible, restate the prediction point so it says the period at risk is known.

**2. Record-structure statistics.** 38% of rows sit in groups with identical features except `Exposure`. The median summed exposure of a group is 0.85, which looks like one policy split into several records within the year. 28.7% of test rows have a training sibling.

Claims per year by the group's summed exposure:
- 0.21 to 0.32 when the sum is below 0.2;
- 0.054 when the sum is about 1.

This is the same early-termination effect seen at policy level. It needs the test rows and the policy's future records, so a deployed model would not have it. Fix: merge the records. A grouped split alone would not stop the statistic being computed inside the test fold.

**3. Sibling labels.** Rows whose siblings had claims have a frequency of 0.11 against 0.067, but a credibility rule on top of the baseline gains only 0.00007. The kit's target counts claims from the severity file (`freMTPL2sev`), which attributes each claim to a single record, so labels hardly carry across records.

The one extreme group (same driver, 15 records, claims 16/9/8/6/5/3/1) helps only on the fold where it splits favourably: test rows with `ClaimNb` ≥ 4 cost 0.0013 → 0.0011 of the fold score.

**Attacks that found nothing**
- **Row order and ids:**
  - Claim rate by row decile is flat (0.038–0.041).
  - Kit position vs the source policy ID: Spearman 0.003.
  - Adjacent rows never share a group (0 of 677,990 pairs).
  - Next-row claim agreement 0.00141 against 0.00135 by chance.
- **Exposure format:** flags for k/365 vs k/366 (which hint at the year): 0.233013 against 0.233023.
- **Missing values:** `VehAge` is missing in 48 rows (99/100 in the source), with 1 claim among them. Nothing.
- **Train vs test:** a classifier separating the two sides, label included, scores AUC 0.502.
- **Policy-ID ≤ 24500 block:** 9,139 rows that all have claims in the frequency file (`freMTPL2freq`) but carry label 0 in 97% of cases. Features find the block (AUC 0.85), but its label rate (3.2%) is close to the rest (3.7%). Dropping it from training is within noise.
- **Transforms over all rows:** none; columns are raw integers and categories.
- **Lookup in the published file:** works. Every kit row matches an OpenML `freMTPL2freq` row, and its label equals the number of `freMTPL2sev` records for that policy ID. Not ranked.

**What the preparation changed:**
- `ClaimNb` was replaced by the severity-file count: 26,444 claims against 36,102 in the frequency file.
- 22 rows were dropped, all with frequency-file `ClaimNb` = 1 and no severity record.
- `VehAge` 99/100 became missing.
- The policy ID was dropped, Region codes became names, and rows were shuffled.
- `Exposure` and `ClaimNb` were not capped.

**Could not check**
- Record dates and why records are split, which would settle #1 and #2.
- Whether `BonusMalus` is the value at the start of the year or after this year's claims.
- Kaggle discussion threads (not fetched).
- Whether identical-feature groups are always one policy rather than different policyholders who happen to match.

Sources: [Wüthrich & Merz, ch. 13](https://link.springer.com/chapter/10.1007/978-3-031-12409-9_13), [arXiv 2604.02400](https://arxiv.org/pdf/2604.02400), [R-bloggers: Exposure as a possible explanatory variable](https://www.r-bloggers.com/exposure-as-a-possible-explanatory-variable/), [OpenML 41214](https://api.openml.org/d/41214) and the `freMTPL2sev` dataset (41215), [Wüthrich/Schelldorfer data-loading script](https://github.com/JSchelldorfer/ActuarialDataScience/blob/3f761ef830d28c14dda5443d504d192069a64ca3/1%20-%20French%20Motor%20Third-Party%20Liability%20Claims/Tools/FreMTPL_1b%20load%20data.r).

</details>

<details><summary>Precedent check</summary>

**Precedent check: fremtpl2 (second pass, 2026-11-04)**

The register has no flag on fremtpl2. Of the ten decisions checked, seven follow precedent. Three need the curator: the split (1), Exposure (2) and DrivAge 99 (3).

**Focus question: are the links real, is IID with ForcedIIDFromTemporal right, and do the pairs leak across the split?**

- **The links are real, and the shares are right.** Running `next_year_rows` again gives 161,883 pairs covering 310,517 of 677,991 rows. The share of rows with an earlier-year row is 0.487 in block 1, 0.483 in block 3, 0.492 in block 5 and 0.603 in block 6, and about 0 elsewhere, so "48-60%" holds. In the twins table, 99.9% of pairs have DrivAge exactly +1. They are inferred links, not a key the source states.
- **"Changes the score by nothing" holds within noise.** Skill is 0.0821 on random folds and 0.0819 on folds grouped by the inferred chains. The difference (0.0002) is far below the fold spread (SD about 0.003 random, 0.002 grouped). The label crosses years only weakly: a claim the next year follows a claim at 0.066 against 0.0385 after no claim, and the pair correlation is 0.017.
- **The pairs do cross the split.** 47.6% of test rows have their inferred policy group on the train side. Under IID that includes a policy's *later* year in train.
- **SPLIT-8 applies.** If the blocks are years {0,2,4}, {1,3,5}, {6}, only two windows exist, and SPLIT-14 needs three. So shipping with a Forced tag is right, and the cost was measured as SPLIT-8 asks: 0.0847 on later years against 0.0820 random, so IID is not optimistic here.
- **The choice of IID over grouped is where precedent splits.** See decision 1.

**Decisions, ranked**

**1. The split stays IID with ForcedIIDFromTemporal on stacked inferred years (CC 2026-11-04, Lennart)**
**Verdict: departs from precedent; the reason is stated only in part.**

- **Precedents:**
  - SPLIT-8 as amended 2026-10-21: "grouped by the entity when the periods are stacked and the entities recur across them".
  - nba_players_2016_2019 and open_university_learning_analytics_dataset (2026-10-21, Lennart): stacked periods grouped by a true key, ForcedGroupedFromTemporal.
  - distribution_transformers_at_cauca_department (2026-10-21, Lennart): one year shipped IID, "not stacked, as the two files hold the same units".
  - account_debt_south_africa (2026-10-12) and bemtpl97 (2026-11-04): Forced IID.
- **Against nba and open_university, the record's reason does set this case apart.** There is no source key, and SPLIT-24 and SPLIT-25 bar grouping on a guess.
- **Against distribution_transformers, the distinguishing facts are visible in the data but not written down:**
  - the features change between years (driver age +1, car age +0/+1, BonusMalus);
  - about 46% of rows are in a pair, not 100%;
  - which block is which year is itself inferred.
- **Part of the stated reason does not count under the rules.** "Change the score by nothing" cites the size of the gap, and SPLIT-4 and SPLIT-30 say the gap never decides. The same number does count if it is put as SPLIT-29's condition that the entity carries the label (pair correlation 0.017).
- **SPLIT-13 and USE-10 give a further reason.** In pricing, renewals are known entities.
- **The decision is new territory.** It is the first Forced IID definition that stacks periods with recurring entities, so no amendment is due yet. SPLIT-8 is a Must, so the departure needs a fact, not an exception.

Consistency check (AI, 2026-11-04): your call on fremtpl2 (all inferred years stacked, random split, a departure from SPLIT-8's stacked-and-recurring clause) differs from distribution_transformers_at_cauca_department (one year kept, IID, not stacked, 2026-10-21: the same units in both years). What sets fremtpl2 apart?
(a) The links are inferred, with changed attributes (driver +1, car +0/+1, BonusMalus), between blocks whose years are themselves inferred. The entity carries almost none of the label (correlation 0.017; grouping moves skill by 0.0002, fold SD 0.003, so SPLIT-29 does not fire). Pricing serves renewals (SPLIT-13). Recorded in the notes in place of "change the score by nothing".
(b) Treat it like distribution_transformers: keep one inferred year per sub-portfolio (blocks 0, 2, 4: 353,887 rows, 52%).
(c) Treat it like nba and open_university: ForcedGroupedFromTemporal on the 430,298 inferred chains. This needs a SPLIT-24 ruling on the rule-built key.
(d) Amend SPLIT-8: when entities are only inferred and carry little of the label, the closest regime is IID.

**2. Exposure stays a free feature, "Potential leak, kept on purpose" (bemtpl97 CC 2026-10-23, Myunghwan; followed here)**
**Verdict: consistent with bemtpl97, but neither definition names a rule that lets it stay, and it may break LEAK-10 (Must).**

- **No exception rule covers it.** LEAK-30 is for transductive scaling, and LEAK-38 is for anonymised competition fields whose timing cannot be tested. Lennart has not ruled on Exposure himself: on 2026-11-04 he ruled "treated alike" on the split and the fit only.
- **New measurement on the raw table:**
  - claims per year by exposure band: 0.172 at 0.1 years or less, 0.123 at 0.1-0.25, 0.097 at 0.25-0.5, 0.055 at a full year;
  - in a Poisson GLM on the rating factors, log(Exposure) gets a free coefficient of 0.641, where a pure offset would be 1.
- **Short policies claim about three times more per year.** That fits the cancellation-after-claim mechanism, but it is confounded with new business.
- **Precedents decided the other way:**
  - heart_failure_followup_survival `time` (2026-09-30, Lennart): a duration ended by the outcome, dropped.
  - kick `WheelType` (2026-10-22, Lennart): dropped once a conditional test measured the mechanism.
- **The literature uses exposure differently.** Noll et al. and Wüthrich and Merz treat exposure as an offset (coefficient fixed at 1), not a feature.

Consistency check (AI, 2026-11-04): your call on fremtpl2 and bemtpl97 (Exposure kept as a free feature, a departure from LEAK-10) differs from heart_failure_followup_survival (`time` dropped, 2026-09-30) and kick (`WheelType` dropped after a conditional test, 2026-10-22). The same mechanism, a value cut short after the outcome, is now measurable here (coefficient 0.641 against 1). What sets it apart?
(a) The planned period is known at quotation (LEAK-37), the premium is pro-rated on it, and the source's metric is built on it. The excess at short exposure is mostly new business. Recorded with the GLM number.
(b) Treat it like kick: keep Exposure out of the features and only as an offset in the scorer (a scoring column), as the source's GLM does.
(c) Reopen bemtpl97 to match whichever you choose.
(d) Amend LEAK-10 for exposure denominators.

A third count dataset scored by exposure (ausprivauto0405 and eumtpl are screened) would make this the third case with the same reason, and an amendment would be due.

**3. DrivAge 99 kept "as possible", VehAge 99/100 set to missing (same definition, CLEAN-10)**
**Verdict: like cases decided differently, with no reason given.**

- **VehAge:** set to missing as a default date: no car is 86-98, and 21 of 23 cars aged 99 are 100 a year later.
- **DrivAge, block 0** (66 of the 70 rows at 99): 1 row at 96, none at 97-98, 66 at 99.
- **The 66 never reappear.** Block 1 (block 0's next year) has no driver older than 97, and none of the 66 has a next-year row even when any driver age is allowed. 62.7% of block 0 has one. They match the default-code pattern of VehAge.
- **The definition's evidence is coarser.** Its "70 against 5 at 98" counts across all blocks.

Consistency check (AI, 2026-11-04): your call on DrivAge 99 (kept) differs from VehAge 99/100 in the same definition (missing, CLEAN-10). Both are a spike at 99 after an empty band, concentrated in block 0. What sets DrivAge apart?
(a) Driver age may be top-coded at 99 (a real age of at least 99), not a default date, recorded as such; (b) set the 66 block-0 values to missing like VehAge; (c) reopen VehAge to keep both; (d) amend CLEAN-10.

**4. The 2022 CASdatasets counts ("use the newer version")**
**Verdict: consistent.** The data owner repaired the counts to match its own claims table (PROV-13, PROV-14). This matches the tension row "a version the source defines replaces ours" (eryhemato). The year stays 2014, the first publication (PROV-9). OpenML 41214/41215 are noted as an older copy (PROV-15).

**5. Exposure above one year kept, counts of 5-16 not capped (CC 2026-11-04)**
**Verdict: consistent.** CLEAN-11 keeps values that are only unusual. Its "single extreme target in the training period" clause does not apply to a random split (qsar_tid_11, 2026-10-21). This matches bemtpl97's "no clip" (2026-10-23).

**6. Metric: mean Poisson deviance with `min_prediction=1e-6` (MET-5, MET-13)**
**Verdict: consistent with bemtpl97 (2026-11-04), with one stale text.** The Metric bullet in `curation_comments` still says the scorer "floors a predicted mean at machine epsilon". The params and bemtpl97's notes say 1e-6.

**7. Fit "approximate"**
**Verdict: consistent.** All 20 ForcedIIDFromTemporal definitions in the working copy are approximate. `fit_reason` names Exposure as kept, as USE-8 requires.

**8. The hold (Myunghwan, 2026-10-28) turned into Yes (Lennart, 2026-11-04)**
**Verdict: consistent.** The newer curator decision wins, and it applies SPLIT-8. It also removes an inconsistency: Myunghwan had shipped bemtpl97 on 2026-10-28 with the same missing timing.

**9. Copies and conflicting copies kept, check warnings accepted**
**Verdict: consistent.** LEAK-18 (few coarse features, plausible repeats), LEAK-20's clause for genuine label ambiguity, bemtpl97, hiva_agnostic.

**10. `Spatial` tag (regions) and eumtpl screened later**
**Verdict: consistent.** The tag follows definitions.md. eumtpl follows selection.md: an old record keeps the verdict its own data earns (hepatitis_c_egypt, 2026-10-26).

**Drift and amendments**
- No drift by one curator on SPLIT-8, CLEAN-11 or MET-13.
- No third exception on any rule this dataset touches.
- The bemtpl97 CC says "the 20 other forced-IID definitions". There are 20 in total including both MTPL sets.

</details>

<details><summary>Advocate</summary>

**Opening brief (advocate), fremtpl2**

Verdict sought: ship after wording changes. Four of the five agents who looked at the split find IID with `ForcedIIDFromTemporal` defensible or right. Two problems are real: the Exposure note gives the wrong size, and the timing of BonusMalus is in doubt. Each has a fix that keeps the dataset.

**1. The task, the target and the metric are what the source defines (P3, P5, P6; USE-5, PROV-13, MET-5). Nobody disputed this.**
- Evidence: 677,991 policies and 26,444 claims. Every count equals the claims table, because the data owner repaired the counts in 2022. The metric is the case study's own Poisson deviance (FreMTPL_1b line 35, 100 times the mean), confirmed by the claim auditor and the practitioner.
- There is real signal and every fold can be scored: each test fold has 8,160-8,465 rows with a claim. Mean count scores 0.2595, exposure times frequency 0.2534, a Poisson GLM 0.2397 and LightGBM 0.2326. The LightGBM-GLM gap of 0.0071 is far above the seed noise of 0.0002.
- The practitioner, a pricing actuary, says: "Yes, as a model-selection benchmark."
- Why this matters for the critic: every point below is a fix inside the definition. None reaches exclusion on the remedy ladder.

**2. IID with `ForcedIIDFromTemporal` is the closest regime SPLIT-8 allows (SPLIT-8, SPLIT-14, both Must; Lennart's CC of 2026-11-04).**
- The temporal split cannot be built. There are no dates, and each sub-portfolio has two or three inferred periods, so SPLIT-14 cannot be met.
- The measured cost is small and its sign is mixed:
  - Notes: 0.0847 vs 0.0820.
  - Practitioner: 0.0824 vs 0.0754.
  - Split auditor, on the same rows: +0.00049 deviance (0.2%), ranking unchanged.
- Grouping on the chains changes nothing. Three agents measured it:
  - 0.0825 / 0.0813 / 0.0829 skill
  - 0.23265 vs 0.23238-0.23245 deviance
  - 0.0797 / 0.0791 / 0.0794 skill
  - Fold SD is 0.0008-0.003.
- SPLIT-29 does not fire, because the entity carries almost none of the label: pair correlation 0.017, and last year's claim as a feature adds +0.00001.
- I concede the cross-row signal is real. It is worth 0.0004 (column auditor) to 0.0021 (claim auditor, via IDpol) deviance, and about 0.0014 for the practitioner's BonusMalus channel. That is 0.2-0.9% of the score. It needs a participant who deliberately matches rows: the over-flexible LightGBM picks up nothing, and sibling labels add 0.00007.
- Grouping does not remove it: −0.0017 random against −0.0018 grouped (split auditor). The signal sits in the data itself, so it falls under the tension "a weak transductive leak against the data as published": keep it with a note.
- On LEAK-17, a fix that does not remove the leak is not the remedy the rule asks for. The mildest remedy is a sentence in `splits_comment` with the numbers.
- I concede SPLIT-8's text names `ForcedGroupedFromTemporal` for stacked periods with recurring entities, so a consistency check against open_university and distribution_transformers is due (principles case 2). The facts that set this case apart:
  - there is no source key;
  - the links are inferred, and the attributes change between years;
  - grouping changes nothing and leaves the renewal signal in place;
  - pricing serves renewals, which are known entities (USE-10, SPLIT-13).
- If the curator prefers grouping on the chains, that also keeps the dataset at no cost.

**3. Not capping the counts and keeping exposures above one year is right (CLEAN-11, Should; precedents bemtpl97 and qsar_tid_11).**
- The 19 extreme rows carry 0.00126 of 0.2534. Each claim has a recorded cost.
- The task gamer measured that capping training counts at 4 makes scores worse (0.233173 vs 0.233023), and so does dropping counts above 5 (0.233405).
- The blind reviewer's cap and RMSE concerns assume an RMSE metric. The declared metric is Poisson deviance, so those concerns do not apply.
- The 1,224 rows with exposure above one year have zero links, as three agents confirmed. They are unusual, not impossible.

**4. Exposure stays as a feature, but the note's number must be corrected (LEAK-37 against LEAK-10; precedent bemtpl97).**
- The planned term and the accounting-year cut are known at quotation. The source's model and metric are built on exposure, and the dataset cannot predict a count without it.
- I concede the note is wrong. "A fifth of the gain" measures the legitimate, proportional part. The part that can carry a later cancellation is 0.0039-0.0045 (14-19% of the gain), and the free GLM coefficient is 0.641.
- Part of that excess is new business and records split within a year: groups of identical rows sum to a median of 0.85 years, and blocks 4-6 look like split contract years. So the cancellation share is likely, not shown (EV-6).
- Mildest remedy: rewrite the note with these numbers and put the consistency check against heart_failure and kick to the curator.
- If the curator rules it a Must breach, the next rung is the definition fix, not exclusion: Exposure as an offset scoring column. That needs a new metric.

**5. BonusMalus timing is the strongest open problem. I concede it is likely, and argue for the fix that keeps the dataset (LEAK-10, Must; LEAK-3, Should; precedent online_shoppers).**
- Evidence: from block 0 to 1 and block 2 to 3, BonusMalus is frozen (it falls after a claim-free year in only 5-21% of pairs, against 92-94% in blocks 4-6). Claimants pile onto the first malus step (5.3-6.8% vs 1.5-1.7%). This points to a value recorded after the claims in blocks 0-4, about 85% of rows.
- What is not shown: no source statement exists, and every paper on freMTPL2 uses BonusMalus as its main factor. That is why LEAK-3 (read the source first) comes before acting.
- Remedies, mildest first:
  - (a) check the source;
  - (b) blank BonusMalus where it fails to behave like history, keep it in blocks 4-6. This follows the online_shoppers precedent ("keep only the period where it behaves like history"), and the rows can be located from IDpol in `_clean`;
  - (c) drop it. In blocks 5-6 it adds nothing measurable.
- The dataset survives every option. Only "keep as is without a source" departs from a Must.

**6. DrivAge 99: concede, cheap fix (CLEAN-10, Should, P7).**
- 66 of the 70 rows are in block 0 and never continue to a next year, which is the pattern that made VehAge 99 missing.
- Set them to missing, or write down the top-coding reason. Under principles step 3 this is a quality issue, not a reason to hold.

**7. Wording fixes (writing.md; MET-11).**
- "Machine epsilon" should be 1e-6.
- "21 of 23" should be 14 of 14 by the shipped rule.
- "28,768 rows equal another" should be 28,768 copies (40,903 rows in groups).
- Name the links behind the 430,298 groups.
- Qualify "consecutive years": the BonusMalus is frozen from block 0 to 1 and 2 to 3, and blocks 4-6 look like split contract years.
- Report the IID cost on the same rows (+0.00049).
- The link counts are lower bounds.

**Judgment record**
- Validity: P3 and P5 hold. SPLIT-8 holds (forced IID, with a consistency check against the SPLIT-8 precedents). LEAK-17 is triggered weakly and not fixed by grouping, so it is kept with a note. LEAK-10 Exposure: the note is corrected, and the curator re-rules. LEAK-10 BonusMalus: likely; LEAK-3 first, then blank by block.
- Value: real, small signal; MET-5 holds.
- Quality: CLEAN-10 DrivAge fix; wording.
- For the curator: the BonusMalus ruling, the Exposure re-confirmation, and IID vs grouped on the chains.

</details>

<details><summary>Critic</summary>

**Verdict: do not ship fremtpl2 as defined. It can ship after changes.** Two features break a Must under P4: BonusMalus and Exposure. The split also leaks the label through the policy's next-year record. Points 4 to 7 can be fixed by editing the text or with a cheap cleaning step.

**1. BonusMalus looks like it was recorded after the row's own claims in blocks 0-4 (P4, LEAK-10 Must).**
- **Problem.** In blocks 4-6, where the 4→5 and 5→6 pairs give a check, BonusMalus behaves like a value read at the start of the year. It follows the French CRM rule: among claim-free rows above 50, 92-94% fall the next year. It is tied to the previous year's claims (×8.3 and ×5.7) and hardly to its own row's claims (×1.4 and ×1.9). In blocks 0-3 it is frozen across the two years: 94.5% are unchanged in 0→1. There it is tied to its own row's claims as strongly as to the other year's (×4.3-5.9).
- **Where the data points.** The first malus step from the floor (62-63) holds 5.3-6.8% of claimants in blocks 0-3, against 1.5-1.7% of rows without a claim. The same pattern shows inside block 4, among rows that have no next-year row: 7.8% against 1.3%. Block 4 rows that do continue, and blocks 5-6, show 1.1-2.2% against 1.4-1.6%. A riskier set of drivers would not put the claimants on exactly one malus step. (Column auditor; the frozen values are confirmed by the claim and split auditors.)
- **Effect on the task.** BonusMalus carries 42% of the model's gain (0.0112 of 0.0269). Removing it costs 0.0131 deviance in blocks 0-3 but gains 0.0005 in blocks 5-6. So most of what the main feature contributes comes from rows where it may encode the target.
- **The other side.** The column auditor labels this "likely, not shown". The actuary reads BonusMalus as the CRM at renewal.
- **Remedy.**
  - First look for a source statement on when BonusMalus was recorded (LEAK-3).
  - If none is found, blank it where the late values can be located: blocks 0-3 plus the block-4 rows without a next-year row, about 577k rows. That is the second clause of LEAK-10, applied as in zillow_prize and melbourne_housing_market.
  - Keeping it with a note departs from a Must, so it needs an amendment, not an exception.

**2. Exposure as a free feature carries post-quote information, and no rule allows keeping it (P4, LEAK-10 Must).**
- **The mechanism is measured.**
  - Records of 0.01 years or less have 104 claims where an exposure offset predicts 9 (task gamer).
  - In block 0, short rows that do not continue claim 0.258 a year, against 0.117 for those that continue (claim auditor). The actuary's numbers are 0.144 against 0.095.
  - In a GLM, log(Exposure) gets a free coefficient of 0.641, where a pure offset would be 1.
- **Size.** Using Exposure beyond the offset is worth 0.0039-0.0045 deviance, which is 14-19% of the skill. Three agents measured this independently.
- **The note gives the wrong number.** Its "about a fifth" (0.2595 → 0.2534) is the legitimate proportional part, not the kept leak.
- **No exception covers it.** LEAK-11 is for values that weaken the signal, and this one strengthens it. LEAK-38 does not cover it either. Lennart ruled on the split and the fit on 2026-11-04, not on Exposure. Precedents went the other way: heart_failure `time` and kick `WheelType` were dropped.
- **Remedy (fix the definition).** Take Exposure out of the features and keep it as a scoring column. Score with Poisson deviance against prediction × Exposure, which is the source's offset form (Noll et al.). This needs a metric in `src/data_foundry/v2/metrics.py`, and bemtpl97 should be reopened to match. If the curator keeps the current form, that is an amendment of LEAK-10, recorded with 0.0039-0.0045 as the leak's size.

**3. The split leaks the label through the next-year record (P4, LEAK-17 Must; SPLIT-8's wording).**
- **What leaks.** In every test fold, 16% of rows have their next-year row on the training side. Built from the shipped columns alone, the true partner is the only candidate for 54.6% of linked rows.
  - The actuary's stacked GLM, linking without IDpol, gains +0.0057 skill on 3 of 3 folds.
  - In the claim auditor's lookup, the true partners alone are worth about 0.0014 deviance, and the information is future, not history: the next-year row is worth 0.0021 when linked through IDpol, the previous-year row 0.00015.
- **"Changes the score by nothing" is not a reason under the rules.** SPLIT-4 and SPLIT-30 say the size of the gap never decides.
- **The links can be grouped on.** SPLIT-24 allows a key "constructed exactly from the data", and the chance rate of these links is 0.02-0.05% (161,883 matches against 16-75 under the controls). So SPLIT-25's bar on grouping on a guess does not apply.
- **SPLIT-8's text names this case.** Its regime for stacked periods with recurring entities is `ForcedGroupedFromTemporal`, as nba and open_university were shipped.
- **Remedy (re-split).** Group on the `next_year_rows` chains, with the offsets made symmetric. Row-wise models lose nothing (skill 0.0825 shipped, 0.0813 grouped), and the actuary's channel is halved (+0.0057 → +0.0024).
- **The renewal signal remains under any split** (-0.0017 deviance). It gets a "Potential leak, kept on purpose" note (LEAK-30 tension).

**4. The cost of the forced split is misreported (P4, SPLIT-8 Must: the cost has to be measured).** "0.0847 against 0.0820" compares different rows. On the same rows, the IID split is slightly optimistic: +0.00049 deviance (SE 0.00016). "Consecutive years of three sub-portfolios" is also weak at both ends:
- in 0→1 and 2→3, BonusMalus is frozen;
- in blocks 4-6 almost no linked row covers a full year (0.2%), and 63-66% of the pairs' exposures add up to at most 1.01. These look like split contract years.

Remedy: rewrite the "Split forced IID" bullet with the same-rows number, and qualify which blocks are years.

**5. Wrong statements in the notes (EV-7 Must, MET-11).**
- "Machine epsilon" should read 1e-6.
- "21 of the 23 cars aged 99 are 100 a year later": the shipped rule pairs only 14 of the 23, all 14 aged 100 the next year. This also sits in the `DEFAULT_VEHICLE_AGE` docstring.
- "28,768 rows equal another" should say they copy an earlier row; 40,903 rows sit in groups of equal rows.
- The 48-60% link shares are lower bounds: widening the offset to ±30 gives up to 75.3% in block 6.

Remedy: edit the text.

**6. DrivAge 99 is treated differently from VehAge 99 (P7, CLEAN-10 Should).** 66 of the 70 rows are in block 0. None of them has a next-year row, against 62.7% of block 0, and block 1 has no driver older than 97. This is the same default-code pattern as VehAge, which the definition sets to missing. Remedy: set those values to missing. This is a quality issue, not a reason to exclude.

**7. Citations nobody checked (EV-7 Must).** No agent opened the Wüthrich and Merz quotes (pp. 553-554, Eq. 5.28), and nobody recomputed the 9,942 claims and the LightGBM figure of 292.6. Remedy: verify them or remove them.

**What I concede.**
- The use case is real, and the metric is right (MET-1, MET-5).
- Keeping the uncapped counts and the exposures above one year is consistent with CLEAN-11 and the precedents.
- The leaks in points 1-3 change scores by 0.001-0.013 deviance. None of them makes the task unfixable, so none of them is grounds for exclusion.

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal (advocate), fremtpl2**

Verdict sought: ship after changes. The critic now asks for the same verdict ("it can ship after changes"). We still disagree on three remedies: which BonusMalus rows to blank, whether Exposure can stay with a note, and whether a re-split fixes the split leak. I concede the critic's points 1, 2, 4, 5 and 6 on substance. I dispute point 3, and I answer point 7 with a check I made in this round.

**New fact (critic point 7, EV-7).** I opened the task gamer's saved Wüthrich and Merz chapter. It is "Appendix B: Data and Examples", pp. 553-575.
- Both quotes in the definition appear word for word:
  - "do not seem to be correct because these claims do not have claim severity counterparts";
  - "policies with more than 5 claims may be data error because they all seem to belong to the same driver (and they have very short exposures)".
- The exact page split 553/554 and Eq. 5.28 (chapter 5) remain unchecked. The 9,942 count and the 292.6 figure were not recomputed.
- The same page says: "policy renewals during the year account for two separate records in the data set. Of course, such split policies should be merged ... we do not have the necessary information". This bears on points 2 and 4 below.

**1. BonusMalus (LEAK-10 Must): concede the Must. I dispute only which rows to blank.**
- I concede the evidence:
  - The first malus step holds 5.3-6.8% of claimants against 1.5-1.7% of other rows in blocks 0-3.
  - BonusMalus carries 42% of the gain.
  - Removing it costs 0.0131 deviance in blocks 0-3 and gains 0.0005 in blocks 5-6.
- I concede that keeping it with a note needs an amendment, not an exception. LEAK-3 (Should) comes first: the chapter above describes BonusMalus but says nothing about when it was recorded, so the source check is still open.
- I dispute part of the critic's mask. Blanking "block-4 rows without a next-year row" makes the missing flag mean "this policy was not renewed". Non-renewed rows claim about twice as often (0.141 vs 0.070 per year in block 0, split auditor). That is "missingness that encodes the outcome", a LEAK-10 clause, so this fix would create a new leak.
  - Mildest remedy that resolves it: blank by block, all of blocks 0-4, which every row shows without a link. This follows the online_shoppers precedent (the period where the value behaves like history).
  - Or drop BonusMalus (option c). It costs nothing measurable in blocks 5-6.
- What follows for point 3: either fix also closes most of the actuary's backward channel, which reads this year's claim from a rise in next year's BonusMalus. With blocks 0-4 blanked, only the 5→6 pairs can carry it. Dropping the column closes it fully.

**2. Exposure (LEAK-10 Must): concede that a note does not resolve it. The offset scoring column is the rung to take.**
- I concede three things:
  - LEAK-11 does not apply, because Exposure strengthens the signal.
  - Lennart's 2026-11-04 marks ruled on the split and the fit, not on Exposure.
  - Under the remedy ladder (principles step 5), a note does not resolve a Must, so my opening's "rewrite the note" is not enough on its own.
- Evidence the critic did not use: Wüthrich and Merz say mid-year renewals are split into two records. So part of the 0.0039-0.0045 excess is record splitting, not cancellation. That fits the median group sum of 0.85 years (task gamer). The leak is mixed. It is not refuted: in block 0, short rows that do not continue claim 0.258 a year against 0.117 for those that continue.
- Why this keeps the dataset: the heart_failure precedent dropped `time`, but here Exposure is the source's own denominator. The matching definition fix is the one the critic names: Exposure as a scoring column, with Poisson deviance on prediction × Exposure (Noll et al.'s offset form).
  - It removes the free 0.641 coefficient.
  - It costs a metric in `src/data_foundry/v2/metrics.py` and reopening bemtpl97 (consistency).
  - Ship after that change, or after an explicit LEAK-10 amendment by the curator that records 0.0039-0.0045 as the leak's size. The curator chooses.
- Residual: the gamer's record-count statistic (0.0006) survives either way. It falls under LEAK-30 (weak) and gets a note.

**3. The split leak (LEAK-17, SPLIT-8): dispute. A re-split does not resolve it.**
- I concede three things:
  - The leak is real. 16% of test rows have their next-year row on the train side. The true partner can be recovered from shipped columns for 54.6% of linked rows.
  - SPLIT-4 and SPLIT-30 bar "the gap is small" as a reason, so I withdraw that wording.
  - SPLIT-8's letter names `ForcedGroupedFromTemporal` for stacked periods with recurring entities.
- Why grouping does not resolve it: a participant sees test features, so the next-year row stays visible inside the test fold. Measured:
  - The renewal signal is −0.0017 under random folds and −0.0018 under grouped folds (split auditor).
  - The actuary's channel shrinks from +0.0057 only to +0.0024.
  - LEAK-17 grouping is a remedy because it separates the entity. Here it does not, so it is not the remedy that resolves the problem (principles step 5).
- What does resolve most of it: the label-carrying part runs through BonusMalus rises, and the point 1 fix removes it.
  - Without labels, the renewal fact is a weak leak in the data as published. The principles' tension table says to keep it with a "Potential leak, kept on purpose" note.
- SPLIT-29 does not fire. It needs an entity "that new data would not have" which "carries the label". Pricing serves renewals, which are known policies (USE-10, SPLIT-13), and the pair correlation is 0.017.
- SPLIT-24 is open, not settled for the critic. The chains come from a matching rule (IDpol offset 1-9, driver age +1), not from identical values. The precedent checker says this "needs a SPLIT-24 ruling".
- Net: IID with the forced tag, plus a note with the numbers, holds SPLIT-8 by its "closest regime" clause. Grouping on the chains is also acceptable at no cost (0.0825 vs 0.0813). The consistency check against nba, open_university and distribution_transformers goes to the curator.

**4. The cost of the forced split: concede.** The same-row figure is +0.00049 deviance (SE 0.00016): IID is slightly optimistic and the ranking is unchanged. Rewrite the "Split forced IID" bullet. Qualify blocks 0→1 and 2→3 (BonusMalus frozen) and blocks 4-6 (split contract years, now backed by the book's sentence above).

**5. Wrong statements: concede all four** (EV-7, MET-11): 1e-6 not machine epsilon; 14 of 14 not 21 of 23, also in the `DEFAULT_VEHICLE_AGE` docstring; 28,768 copies and 40,903 rows in groups; link shares are lower bounds (up to 75.3% at ±30).

**6. DrivAge 99: concede** (CLEAN-10, P7). 66 of the 70 rows are in block 0 and none continues to a next year. Set them to missing, as VehAge 99 is.

**7. Citations: partly resolved** (see the new fact above). The quoted text is verified. The pages, Eq. 5.28, 9,942 and 292.6 are still open: verify them or cut them.

**Judgment record (revised)**
- Verdict: ship after changes.
- Validity:
  - P3 and P5 hold.
  - LEAK-10 BonusMalus: LEAK-3 first, then blank blocks 0-4 or drop (not the renewal-status mask).
  - LEAK-10 Exposure: offset scoring column, or a curator amendment that records 0.0039-0.0045.
  - SPLIT-8 holds with forced IID, or grouping at no cost if the curator chooses. SPLIT-29 does not fire.
  - LEAK-17: kept with a note, because grouping does not remove it.
- Value: MET-5 holds; the signal is real and small.
- Quality: CLEAN-10 DrivAge; the wording fixes; EV-7 open items.
- For the curator:
  - the BonusMalus remedy;
  - Exposure: offset or amendment, with bemtpl97 matched;
  - IID vs grouped on the chains (SPLIT-24 ruling).

</details>

<details><summary>Critic rebuttal</summary>

**Rebuttal (critic), fremtpl2**

**Verdict: unchanged. Do not ship fremtpl2 as defined; it can ship after changes.** The advocate wants to ship after wording changes. Their own points 4 and 5 contradict that. They agree that keeping BonusMalus without a source statement departs from a Must. They also agree that the next step for Exposure, if it breaks a Must, is to change the definition. Neither is a wording fix.

**Advocate 1 (task, target, metric): concede.** P3, P5, P6, MET-1 and MET-5 hold. The measured signal is clear: the LightGBM-GLM gap is 0.0071 against seed noise of 0.0002. None of my points asks for exclusion.

**Advocate 2 (IID with `ForcedIIDFromTemporal`): dispute.**
- **Two channels are mixed up.** The figures "-0.0017 random against -0.0018 grouped" measure the label-free renewal signal: whether a later record exists. My opening already accepts that signal with a note. The label channel is a different thing, and grouping does cut it:
  - The actuary's BonusMalus-rise channel falls from +0.0057 to +0.0024 skill.
  - The split auditor's matching against training rows falls from -0.0012 to -0.0004 deviance.
  - The advocate's rule that "a fix that does not remove the leak is not the remedy" therefore fails on the split auditor's and the actuary's own numbers.
- **LEAK-17 is a Must with no weak tier.** LEAK-30 is the rule that reads "Must when strong, Should when weak", and it covers scaling over all rows. The tension row in principles.md that the advocate cites ("weak transductive leak") lists only scaling cases (sf_permit_time, home_credit). Repeated entities fall under LEAK-17, and its remedy is "keep one row per entity … or group". Neither the split auditor's "Should-strength" label nor the advocate's "triggered weakly" has a basis in the rule text.
- **"Needs a participant who deliberately matches rows."** That is the case LEAK-17 guards against. The task gamer and the actuary both rebuilt the links from the shipped columns alone: 54.6% of linked rows have the true partner as the only candidate, and the gain held on 3 of 3 folds.
- **"Grouping changes nothing" cannot be a reason.** SPLIT-4 and SPLIT-30 say "the size of the gap never decides". The advocate's other distinguishing facts:
  - *No source key.* SPLIT-24 allows a key "constructed exactly from the data", and its cases include "consecutive blocks … in the raw file order" (in_vehicle_coupon) and a mix rebuilt from its ingredients (concrete). An IDpol offset of +1..+9, equal factors and driver age +1 is the same kind of exact rule, with a chance rate of 0.02-0.05%. SPLIT-25 covers groups that "cannot be recovered", and these can. The column auditor's appeal to SPLIT-25 does not apply.
  - *Attributes change between years.* They change by a fixed rule (driver age exactly +1 in 99.9% of pairs). That is not a similarity threshold.
  - *Renewals are known entities (USE-10, SPLIT-13).* This is the advocate's best argument, and it argues against IID. Renewal pricing gets the policy's past. IID gives it the future: the next-year row is worth 0.0021 deviance, the previous-year row 0.00015, and last year's claim +0.00001. Grouping removes the future and costs nothing legitimate.
- **Concede:** grouping is a call for the curator through the consistency check. The advocate agrees that SPLIT-8's text names `ForcedGroupedFromTemporal` for stacked periods with recurring entities. If the curator keeps IID, that departs from the letter of a Must and needs a recorded fact or an amendment (option (d) of the precedent checker), not a sentence in `splits_comment`. A count of four of five agents is not evidence. Two of those agents (claim auditor, actuary) also offered grouping, and the precedent checker found that IID departs from precedent.

**Advocate 3 (no cap, exposures above one year kept): concede.** This follows CLEAN-11, qsar_tid_11 and bemtpl97. The task gamer measured that capping makes the score worse (0.233173 capped against 0.233023). The blind reviewer's concern about the cap assumed an RMSE metric.

**Advocate 4 (Exposure stays as a feature under LEAK-37): dispute.**
- **LEAK-37 covers "an input the actor knows at the prediction point."** The advocate names the planned term, but the shipped column is realised exposure. The actuary says: "At quote I know the contract term and start date, not a later cancellation." LEAK-37 would cover a planned-term column, and none is shipped.
- **"Mostly new business, likely not shown (EV-6)" is refuted by the conditional test.**
  - The column auditor looked only at rows that have an earlier-year row, so no new business. Even there, rows with exposure ≤0.1 claim 0.255 a year against 0.056 for full-year rows (4.5×).
  - Within each exposure bin, a claim lowers the chance of a next-year row (0.19 vs 0.27, 0.28 vs 0.35, 0.44 vs 0.51, 0.47 vs 0.53).
  - In block 0, short rows that stop claim 0.258 a year against 0.117 for those that continue (claim auditor).
  - This is the standard that kick `WheelType` was dropped on, on 2026-10-22: the conditional test measured the mechanism. heart_failure `time` was dropped for the same mechanism, a duration cut short by the outcome.
- **Records split within a year do not save it.** A record ended mid-year after a claim, for example by a change of vehicle, is also a post-outcome event. The groups of identical rows with a median summed exposure of 0.85 are the task gamer's exploit #2, which "a deployed model would not have".
- **LEAK-11 does not apply,** because the value strengthens the signal (free coefficient 0.641 where a pure offset would be 1; 0.0039-0.0045 deviance, 14-19% of the skill).
- **Concede:** the advocate offers the offset scoring column as the next step. Given the facts above, that step is the one that applies: Exposure becomes a scoring column, with a new metric in `src/data_foundry/v2/metrics.py`, and bemtpl97 is reopened. A note alone keeps a Must breach without an amendment.

**Advocate 5 (BonusMalus): largely concede; one dispute.**
- We agree on the order: LEAK-3 first, then blank by block, then drop.
- **Dispute:** the advocate's option (b) keeps all of blocks 4-6. But block-4 rows without a next-year row show the same footprint: 7.8% of claimants at the first malus step against 1.3% of rows without a claim. Block-4 rows that continue show 1.1-2.2% against 1.4-1.6%. The blanking has to cover those rows too, about 577k in total. This is the zillow / melbourne form, "blank … for those rows", and online_shoppers' "keep only the period where it behaves like history" leads to the same cut.
- "Every paper uses BonusMalus" is not a timing statement. LEAK-3 asks for the source, not for common practice.
- Since both sides agree that shipping BonusMalus as it is departs from a Must, the dataset cannot ship "after wording changes" until this is resolved.

**Advocate 6 (DrivAge 99): concede.** This is CLEAN-10, a Should and a quality issue, fixed by setting the 66 block-0 values to missing.

**Advocate 7 (wording): concede the list, with one addition.** The advocate leaves out my point 7 (EV-7, a Must). No agent opened the Wüthrich and Merz quotes (pp. 553-554, Eq. 5.28), and nobody recomputed the 9,942 claims or the LightGBM figure of 292.6. They need to be verified or removed. The "21 of 23" fix also applies to the `DEFAULT_VEHICLE_AGE` docstring.

**Changes I still ask for before shipping, mildest that works:**
1. BonusMalus: the LEAK-3 source search, then blank blocks 0-3 plus the block-4 rows without a next-year row (LEAK-10, Must).
2. Exposure: make it an offset scoring column with a new metric, and reopen bemtpl97. Otherwise the curator amends LEAK-10, recording 0.0039-0.0045 as the leak's size (LEAK-10, Must).
3. Split: `ForcedGroupedFromTemporal` on the `next_year_rows` chains. Otherwise a recorded departure from SPLIT-8 and LEAK-17, with the label-channel numbers above. The renewal signal gets a "Potential leak, kept on purpose" note.
4. Wording fixes, including the IID cost on the same rows (+0.00049), and the EV-7 citations.

Neither side asks for exclusion.

</details>
