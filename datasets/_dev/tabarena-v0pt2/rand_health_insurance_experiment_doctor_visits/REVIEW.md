# rand_health_insurance_experiment_doctor_visits

**Outcome:** added. The AI recommends shipping it after the panel's changes, listed below; the forced split is settled
(2026-11-02). The source is Cameron and Trivedi's person-year extract of the RAND Health Insurance Experiment
(1974-1982, six US sites): 14,214 person-years of 5,638 persons. The target is the person's medical spending in the next
study year, in dollars (22.7% zero), the quantity Newhouse et al. (1989) predicted to adjust Medicare's per-enrollee
payment. The split is grouped by rebuilt family and tagged as forced from temporal, and the score is the paper's own
criterion, R2 in dollars. Validity: SEL-2 holds (policy call 1); SEL-1 was not raised, and `black` stays as known at the
prediction point (USE-6), though no payer adjusts for race (domain practitioner); USE-1, USE-2 and USE-5 hold (the
source's own target, so the record's `No Good Target / Scientific Discovery` falls); USE-8 holds now that `fit_reason`
names the missing claims diagnoses and welfare flag; LEAK-10 holds for 29 of 30 features, and `family_income`, whose
timing cannot be checked, is dropped; the target year's eligible fraction stays out (the 37 years cut short by what
happens in them, deaths and exits, average $2,408 against $172), a departure from your fremtpl2 call like frempl's issue
2, and your answer there carries over; SPLIT-24 with SPLIT-4: families can be rebuilt from the data, so the split now
keeps them together (no score change); SPLIT-8 is triggered and tagged, and the split is shipped on your call of
2026-11-02 (forced grouped splits ship; SPLIT-8 amended); PROV-13 and PROV-9 stay open until ICPSR 6439 is read (issue
2). Value: TP-2 and TP-10 hold (R2 0.085 for random forest and 0.083 for ridge on the 9 family folds, near the paper's
9%; carrying this year's spending forward scores -0.43); MET-1, MET-3 and MET-5 hold (`r2` in dollars, the paper's eq.
3; a capitation pays the mean). Quality: the extract's site-mean fills set to missing in three more columns (CLEAN-10);
the notes corrected where the data contradicted them (CLEAN-12); the 37 partial target years kept with a note
(CLEAN-11); the target stays in dollars, unlike the log1p claim-cost tables of australian's issue 5, because R2 scores
the mean a capitation pays (CLEAN-16, MET-3). Weighed: source +, a use case named by the source +, 5,638 persons with a
zero-heavy target +, fold noise - (the largest year, $39,182, holds 41-44% of the sum of squares of each fold it falls
in), 1970s data -, meps_total_healthcare_expenditure carries the task on current data -. Left for Andrej: issues 2 and
3.

Changes made after the review panel (AI, 2026-11-01):

- The split groups on a family id rebuilt from the raw file (runs of person ids with the same site, plan and income:
  2,258 families, at most 10 persons), and `person_id` leaves the table.
- `family_income` is dropped.
- These become missing: the extract's site-mean fills in `chronic_disease_index`, `mental_health_index` and
  `education_of_decision_maker`, and "excellent" self-rated health for the 346 children who were never asked. All
  these data changes together move R2 by less than 0.001.
- The split carries the `ForcedGroupedFromTemporal` tag, and `splits_comment` gives the two study-year windows.
- `fit_reason` names the missing diagnoses and welfare flag. The use case loses its care-manager sentence, since R2
  does not score picking high spenders.
- The notes are corrected where the data contradicted them (the coinsurance coding, the `logc` and `fmde` formulas,
  the missing inpatient charges) and say why the target year's eligible fraction is not a feature and that ICPSR 6439
  has not been read.
- Record, at hand-over (no mark needed): an Assessment line supersedes the screening's `rmse` line and its "Same call
  as `health_insurance`" paragraph, the title says medical spending, and `v2_path` is added. The marker `No Good Target
  / Scientific Discovery`, which you kept on 2026-10-30, stays until your mark: the source's own target refutes it
  (USE-1, USE-2), and the same marker is open on four other `Yes` records of this run (pennsylvania's issue 1).

**Main points:** Can you open
ICPSR 6439 to settle the origin and the year (2)? Rename it to say spending (3)?

**Issues for Andrej:**

2. **Can you download ICPSR 6439 (it needs a login)?** The definition reads Cameron and Trivedi's extract
   (`randdata.dta`) and gives the experiment's public-use files, ICPSR 6439, as the origin, with the year 1995. Nobody
   has read ICPSR 6439: it answered 403 to two panel agents and to the mediator on 2026-11-01. The extract has damage
   of its own: in six columns, missing values were filled with a site mean; its coinsurance code disagrees with the
   file's own derived columns; and its variable labels are cut at 32 characters. PROV-13 (Must) asks to check the
   origin before cleaning around such damage. For SUPPORT2, Lennart downloaded ICPSR 2957 with a login (2026-10-12).
   * What it changes: after the changes above, nothing in the task waits on it. The fills are set to missing from the
     data, and `family_income` (label cut off: "income based on annual income r...") is dropped because nobody can tell
     whether it averages later years (LEAK-10, Must). The codebook would settle that, so the column could come back.
     It would also give the plan and site labels, the coinsurance coding, the price base of the dollars and the year.
   * The year (PROV-9, Must): SUPPORT2 took its extract's year, 2003, because ICPSR "does not hold every value we
     ship" (Lennart, 2026-10-26). If ICPSR 6439 holds the person-year values we ship, 1995 stands. If not, the year is
     the extract's first publication (Cameron and Trivedi's data page for Microeconometrics, 2005, or 2002 if the file
     first came out with Deb and Trivedi's paper), `source_url` is that page, and ICPSR becomes the second citation.
   * The critic holds that the origin counts as unreachable only after your login fails; the advocate accepts a
     note if you cannot log in. Both agree on the year rule above.
   * Implemented: the year 1995 and the ICPSR link are kept until the check, and the notes say ICPSR 6439 has not been
     read. Alternative: if you cannot log in, keep the dataset with that note and take the extract's year, as for
     SUPPORT2. The "repair against cleaning around damage" tension row allows a note when the origin cannot be reached.

   Recommendation: try the login. The codebook and the file list settle the year, the income and the labels in one
   pass. Decision: (a) you download it, or (b) you cannot: keep with the note and take the extract's year?

3. **Rename the dataset to say spending?** The `unique_name`, the folder and the class say "doctor visits", from the
   screening's first target. The dataset predicts next year's medical spending in dollars, and the visit count is only
   a feature, so a user looking for a count task would pick it by mistake. records.md keeps names stable, because a
   rename breaks links and review marks. This dataset has no UUID and no review marks yet, so a rename costs least
   now. Lennart has done both: mic_duplicate was renamed in place, and ames_housing got a new record under its new
   name (2026-10-26).
   * Implemented: the name is kept; the record's title, the task summary and the notes say medical spending.
   * Alternative: rename the record, the folder and the class to `rand_health_insurance_experiment_medical_spending`
     now, and update the claims board, the triage summary and the MEPS record (the working copy's README table has no
     row for it yet).

   * pricing_game_2017_french_mtpl issue 4 asks the same kind of question: a name that misdescribes the target, there
     taken from the source's title ("MTPL"), here from the screening's first target. Answer both the same way unless a
     fact differs; here none of the rename's cost has arisen yet (no UUID, no marks).

   Recommendation: rename now, before a UUID is assigned; the advocate and the critic agree. Decision: rename or keep?

**Review panel:** ship after changes (mediator). Claim audit: 41 claims, 32 hold, 5 refuted and 2 refuted in part (the
notes corrected, the record's marker, metric line and name; the name is issue 3), 1 contested (the missing SPLIT-8 tag,
now added), 1 moot (the record had no Assessment line); 5 more points untested; the split audit refuted "families cannot be held together" (the split now groups on the rebuilt
family). Blind review: would include with changes; its main concern, the heavy-tailed dollar target scored as R2, was
not pressed (MET-3, MET-5: the paper's criterion, and a capitation pays the mean). Debate: agreed on every remedy (the
tag, regrouping, dropping `family_income`, undoing the fills, the text fixes); no remedy disputed; left for the curator:
the forced split against how_much_did_it_rain (issue 1), the ICPSR 6439 login (issue 2) and the rename (issue 3).

<details><summary>Mediator</summary>

**Mediator (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-2 holds (policy call 1); USE-1, USE-2, USE-5 hold (Newhouse et al. 1989's own target: the record's
  `No Good Target / Scientific Discovery` falls); USE-8 fixed (fit_reason names the missing claims diagnoses and
  welfare flag); MET-1 fixed (care-manager clause dropped); LEAK-10 holds for 29 of 30 features, open for
  `family_income`, fixed (dropped); LEAK-30 weak, fixed (site fills set to missing); SPLIT-29 holds against IID;
  SPLIT-24 with SPLIT-4 fixed (grouped on the rebuilt family, cost nil); SPLIT-8 triggered, tagged
  `ForcedGroupedFromTemporal` with the window cost, open against how_much_did_it_rain (issue 1); PROV-13 and PROV-9
  open (ICPSR 6439 needs a login, issue 2).
Value: TP-2, TP-4, TP-10 hold (RF 0.093, linear 0.084, naive last value -0.427); MET-3, MET-5 hold (`r2` in dollars,
  the paper's eq. 3).
Quality: CLEAN-10 fixed (fills, unasked children); CLEAN-12 notes corrected; CLEAN-16 departure from the siblings'
  log1p kept with its stated reason (MET-3: a capitation pays the mean); CLEAN-11: 37 partial target years kept with
  a note.
Weighed: source +, use case named by the source +, shape + (5,638 persons, 22.7% zeros), age -, MEPS sibling -
  (a priority factor, not a duplicate: PROV-7).
For the curator: issue 1, consistency (forced split against how_much_did_it_rain); issue 2, the ICPSR 6439 login
  (PROV-13, PROV-9); issue 3, the rename (records.md).
```

The two briefs end with no remedy in dispute. What is left needs the curator: his own SPLIT-8 call of 2026-10-30,
which no panel role checked against this dataset, a login, and a name.

**Agreed facts**

1. Source: `randdata.dta`, sha256 pinned, 20,190 x 45, 5,912 persons, study years 1-5. The format-110 reader equals
   statsmodels' conversion (10 columns, 20,190 of 20,190 rows) and the blind reviewer's own reader (all 14,214
   shipped rows). The "earlier conversion" the Reading bullet cites was not found (claim audit U5).
2. Task: Newhouse et al. 1989 predict annual spending per person-year to adjust Medicare's capitation (Introduction,
   "Dependent variables"). Target: next-year `meddol`; 14,214 rows, 5,638 persons; 22.7% zero; mean $178, SD $726,
   max $39,182.
3. No feature comes from year t+1. The health columns are baseline. `family_income` is constant per person, its label
   is cut off, it is not the income behind the out-of-pocket cap, and it holds one site-mean fill per site (563
   persons). Its timing cannot be checked. Dropping it moves R2 by 0.0004 at most.
4. IID would be wrong: a feature lookup scores R2 0.372 under random rows. No person sits on both sides of a shipped
   split. Dropping `study_year` moves R2 by 0.0005 at most (SPLIT-9).
5. SPLIT-8: the windows by target study year train on 38.4% (year 3), 76.4% (year 4) and 88.2% (year 5) of the rows.
   RF / ridge: year 4, 0.147 / 0.129 temporal against 0.135 / 0.135 on the person folds; year 5, 0.112 / 0.113
   against 0.098 / 0.103. Training on later study years adds +0.0001 ± 0.0025.
6. Families: consecutive `zper` with identical site, plan and raw income rebuild them (the SPLIT-24 form). The two
   variants nest (2,523 inside 2,422 raw families). `mdeoff` and `pioff`, outside the key, are constant in 99.5-99.8%
   of multi-person families. 75.7% of test rows have a family member in training; the score effect is nil.
7. Value: RF 0.093 and linear 0.084 against the paper's about 9% (62% of a 14.5% maximum); without this year's use
   0.039; prior spending alone 0.038. A six-input ridge equals all 30 features (0.090).
8. Metric: Efron's R2 (eq. 3) is the paper's only criterion. The dummy scores within 0.002 of 0 on every fold. The
   $39,182 row holds 40-56% of its fold's SS_tot; the ridge-against-RF ranking flips on 0 of 9 folds without it.
9. Fills: `disea` 5,604 rows (39.4%), `mhi` 2,494 (17.5%), `educdec` 157; "excellent" self-rated health for 346
   children never asked. Setting them to missing moves R2 by under 0.001.
10. Notes the data contradict: the coinsurance coding (plan 13 coded 0, plans 2-4 coded 100, against the file's own
    `logc` and `fmde`); the DERIVED comments for `logc` and `fmde`; "lacks its charges" (68 of 80 such years record
    some); the 37 partial target years (5.6% of SS_tot) and why the eligible fraction is no feature (it moves with the
    outcome: 19 of the 37 fall before the planned end).
11. The record's marker, its "fallback `rmse`" line and its "doctor visits" name are refuted by the definition.
12. ICPSR 6439 answers 403 without a login (claim auditor, blind reviewer, and my check on the study page, the DSDR
    page and the DOI, 2026-11-01).

My check (two scripts with logs in the run folder), the agreed changes applied together:

| Check | Result |
|---|---|
| Rows set missing | `disea` 5,604, `mhi` 2,494, `educdec` 157; `self_rated_health` 417 rows of the 346 children |
| Coarser family key, shipped rows | 2,258 families; largest 10 persons, 33 rows |
| Data changes, person folds (3 repeats, same seeds) | ridge 0.0794 to 0.0793; RF 0.0821 to 0.0817 |
| Family against person groups, changed frame | ridge 0.0870 against 0.0866 (20 repeats); RF 0.0860 against 0.0889 (6 repeats); SD of repeat means 0.006 |

One 3-repeat draw on family groups gave ridge 0.073 with one fold at -0.016. That is where the largest rows land, as
the tail note says, not an effect of the families.

**Changes to make now (no decision needed)**

Definition:

1. Group on the rebuilt family id: runs in `zper` order with identical site, plan and raw income, built in `_clean`
   before the income column goes. It is a grouping column only (LEAK-33). `person_id` leaves the table (CLEAN-3: an
   id that encodes the site and the family order). Rewrite `task_summary.split` and `grouping.definition`. Rules:
   SPLIT-4, SPLIT-24 (Must); precedent: MEPS groups by household.
2. Drop `family_income` (LEAK-10, Must, second clause: a late value that cannot be located goes unless the curator
   keeps it case by case, and no part of it can be traced). Revisit if ICPSR 6439 shows it is the enrolment income.
3. Set to missing the site fills of `disea`, `mhi` and `educdec` (the column auditor's `FILLS` block) and
   `self_rated_health` for the 346 children under 14 at entry with a filled `physlm` and no flag set. Extend
   Decision 1 (CLEAN-10, Should; LEAK-30 weak; tension row "fix it when we can"; treated like `black` and `physlm`).

Text:

4. Add `ForcedGroupedFromTemporal` and a `splits_comment` (SPLIT-8, Must): the two windows and their scores; study
   years are not calendar years and years 4-5 hold only the 5-year enrollees; a release with calendar years (ICPSR
   6439, the sites' start dates) should get a temporal split.
5. `fit_reason`: no claims diagnoses and no welfare flag (USE-8, Must).
6. `use_case`: drop "An HMO or care manager can use the same prediction to plan for its high spenders" (MET-1, Must:
   `r2` does not score a top-k choice).
7. Notes (CLEAN-12, Should; writing.md): `coinsurance_rate` follows the file's coding and `plan` is the reliable
   identity; correct the `logc` and `fmde` comments; "lacks part of its inpatient charges (68 of the 80 such years
   record some)"; the partial years' share and why the eligible fraction is no feature (the fact that sets this apart
   from fremtpl2); the largest row's 40-56% of its fold's SS_tot; the Anomaly bullet becomes the fills decision;
   `chronic_disease_index` is 100 x count / list length (23 diseases at site 1, 29 elsewhere: one scale, CLEAN-21
   holds); the health indexes change instrument at age 14; the Reading bullet cites the statsmodels comparison
   instead of the conversion that was not found.

Record:

8. Remove `No Good Target / Scientific Discovery` (USE-1, USE-2; the CC of 2026-10-30, "try to find a target", is met
   by the source's own target). Add an Assessment line that supersedes the screening's metric line and the older
   "Same call as `health_insurance`" paragraph (a later stage's measured finding supersedes). Change the title from
   doctor visits to medical spending. `Outdated` stays (weighed).

**Changes that need the curator (ranked)**

1. *Forced split against how_much_did_it_rain (P4, SPLIT-8, Must; consistency).*
   - Problem: the use case is next-year, and the release has no calendar years. SPLIT-8 ships the task grouped and
     tagged. On 2026-10-30 Andrej sent how_much_did_it_rain to `No`: "if the data is temporal but a temporal split is
     not possible, we cannot split the data and reject it". frempl (issue 5) and australian_vehicle_insurance (issue
     1) ask the same question in this run.
   - Effect: models are tested on unseen families, as a formula meets new enrollees, but in the same study years. A
     year-to-year change (mean target $170 in year 2, $209 in year 5) is not tested.
   - What sets it apart (measured): how_much_did_it_rain's `No` named a leak that a random split could not bound.
     Here the split is grouped, its cost is bounded on two windows (fact 5), and the forced split is no more
     optimistic. The other half of the use case is a cold start, which a grouped split tests (USE-10). A split by
     study year would test a change of cohort (only 5-year enrollees reach years 4-5) more than of time.
   - Sides: both accept the tag. Neither brief nor the precedent checker cited how_much_did_it_rain; I add it under
     principles, "Consistent judgement", case 2.
   - Decision: (a) ship as tagged; (b) `No`, like how_much_did_it_rain; (c) amend SPLIT-8. Recommendation: (a),
     decided with frempl and australian. The answer carries over to MEPS.
2. *ICPSR 6439 (P5, PROV-13 and PROV-9, Must).*
   - Problem: the definition cleans around the extract's damage and dates the data 1995 by ICPSR 6439, which nobody
     has read.
   - Effect: nothing in the task waits on it after changes 2 and 3. The codebook settles the income timing (it could
     return), the plan and site labels, the coinsurance coding, the price base and the year.
   - Advocate: the tension row allows a keep with a note when the origin cannot be reached. Critic: unreachable means
     the curator's login failed, not an agent's 403; SUPPORT2 was reached with a login (Lennart, 2026-10-12).
   - Decision: (a) Andrej downloads the codebook and file list; 1995 stands if ICPSR holds the person-year values,
     else the extract's year (Cameron and Trivedi's data page, 2005) as for SUPPORT2 (Lennart, 2026-10-26); (b) no
     login: keep with a note and take 2005. Recommendation: try (a).
3. *Rename (house rule, records.md: names stay).*
   - Problem: `unique_name`, the folder and the class say doctor visits; the target is spending.
   - Effect: a user looking for a count task picks it by mistake.
   - Sides: both support renaming now, while there is no UUID and no review mark (mic_duplicate renamed in place;
     ames_housing got a new record).
   - Decision: rename to `rand_health_insurance_experiment_medical_spending` now, or keep the name with the title
     and text changed. Recommendation: rename now.

**Disputed points**

| Point | Advocate | Critic | Rule and rank | Settled |
|---|---|---|---|---|
| Families | text fix or regroup | regroup | SPLIT-4 and SPLIT-24, both Must (P4) | Regroup. No conflict: SPLIT-24 allows the exact key, and SPLIT-4 lets the use case decide (new enrollees join as family contracts). A note is the lower rung of the ladder, for a definition that cannot be fixed; this one can, at nil cost. The coarser key nests the finer one, and over-merging is harmless. Advocate conceded. |
| `family_income` | costs nothing either way; drop preferred | drop | LEAK-10 second clause (Must; a keep is the curator's case-by-case call) | Drop. "A 'removing it changes no score' test alone is still no reason to keep." Conceded. The critic's site-fill fact is moot after the drop. |
| PROV-13 order | note allowed if agents cannot reach | curator tries the login first | tension row "repair against cleaning around damage" (P5 over P7); SUPPORT2 | Critic's reading: repair comes first, and a login counts as reachable. Advocate conceded. Issue 2. |
| PROV-9 timing | change once ICPSR is answered | extract's year unless ICPSR holds the values | PROV-9, Must | Both agree on the condition. Kept with issue 2 so that the year does not change twice. |
| SPLIT-8 | conceded the tag | tag | SPLIT-8, Must | Tag now. The consistency question is mine (issue 1). |
| Name, use case, fit, record | conceded | text fixes | USE-5, USE-8, MET-1 (Must) | Changes 5, 6 and 8 now; the rename is issue 3. |

Not pressed, and rightly: the log target (MET-3 Must and MET-5 outrank CLEAN-16 Should; the blind reviewer's concern
1); `Outdated` against MEPS (weighed, priority only); `plan` and `site` as int64 (wrong: both are categorical);
annualising or dropping the partial years (CLEAN-11: no source says they are not the task's quantity).

**Consistency with precedent**

- Follows: MEPS (next-year target, survey items, decedents kept, household groups); SUPPORT2 (income dropped, origin
  read before the year); forest_fires and policy call 3 (the source's metric first); sf_permit_time and home_credit
  (fills fixed); ames_housing (CLEAN-11 drop on the source's words); mortgage and onlinenewspopularity (CLEAN-13);
  open_university (SPLIT-8 tag).
- Departs with a fact: fremtpl2 and policy call 3 on exposure (the eligible fraction moves with the outcome; written
  into the notes); the siblings' log1p targets (CLEAN-16 is case by case; R2 in dollars scores the mean a capitation
  pays); the paper's cohort (all ages and non-completers, with a stated reason).
- Flag: how_much_did_it_rain (Andrej, 2026-10-30) is issue 1. The precedent check missed it.
- Distinguished: health_insurance (`No`) had no predictive use; Newhouse et al. supply one (policy call 1).
- No drift and no third exception. The issue 1 answer and the household grouping carry over to MEPS when it is built.

</details>

<details><summary>Claim audit</summary>

**Claim auditor (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Verdict:** the claims about the task hold. Target, prediction point, rows, split and metric survived every test that could have refuted them. Nothing refuted changes the task or its validity. What did not hold:

- one implied split claim that conflicts with the precedents: the dataset carries no forced-temporal tag (P4, SPLIT-8);
- a stale record marker (P3);
- the screening's metric line, now superseded (P6);
- four documentation claims that the data contradict (P7).

The family question, the timing questions and the metric all held under a test that could have failed.

Scripts and outputs are in the run folder. Models are untuned (ridge alpha 10; RF with 200 trees, min_samples_leaf 20), scored on the shipped 3x3 grouped splits unless stated otherwise (EV-8).

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Raw file 20,190 x 45, 5,912 persons, study years 1-5; sha256 pinned | notes ¶1, download | read the file, hash it | holds | sha256 8364cf9e...a628; (20190, 45); 5,912 zper; years 1-5 | PROV |
| 2 | The format-110 patch reads every column correctly | notes "Reading" | compare with an independent conversion (statsmodels `randhie`, 10 columns) | holds | mdvis, idp, lpi, fmde, physlm, disea, hlthg/f/p equal in 20,190/20,190 rows. statsmodels' `lncoins` = log(coins+1) exactly, so its 24% difference from `logc` comes from the file (see 21), not from the reader | EV-2 |
| 3 | `meddol` = out + drugs + supplies + inpatient in 20,188 of 20,190 rows | notes "Prediction point" | recompute | holds | 20,188; the 2 exceptions are rows 6172 and 19895 | USE-5 |
| 4 | The target is the paper's dependent variable: annual spending excluding dental and outpatient mental care, person-year unit, first year never a target | notes, task_summary | read the paper (PMC4192960, "Dependent variables", "Source of data") | holds | quotes verbatim at lines 1006 and 1010 of the paper's text (PMC4192960); the target is year t+1 ≥ 2 by construction | USE-1, USE-5 |
| 5 | 14,266 pairs of 5,639 persons; 273 persons have no consecutive pair | notes "Rows" | rebuild the pairs | holds | 14,266 / 5,639; 269 single-year persons plus 4 whose years only have gaps (12 persons have gaps) | USE-7 |
| 6 | 52 target years have `inpmis`=1; every one had an admission; median $264 over the 80 such years; "the recorded spending lacks its charges" | notes "Dropped rows" | count, and look at `inpdol` | partly refuted (wording) | 52 dropped, 80/80 with `totadm` ≥ 1, median $264.37. But 68 of the 80 have `inpdol` > 0 (median $212), so the spending lacks *part* of the charges ("missing any inpatient charges"). The drop stands | CLEAN-11 |
| 7 | All 45 partial years are a person's last year, never a year t; 37 partial target years | notes "Not features" | count | holds | 45/45 are last years; partial year-t rows in pairs: 0; partial targets: 37 | LEAK-10 |
| 8 | Final frame: 14,214 rows, 5,638 persons, 30 features, `person_id` not a feature | task_summary.row, README | rebuild the container; `feature_columns` | holds | 14,214 x 32; 30 features; `person_id` excluded | |
| 9 | 22.7% zero targets, max $39,182, SD $726 against mean $178 | notes, task_summary | recompute | holds | 0.2274; 39,182.0; 726.1; 178.3 | |
| 10 | 31% of the rows are under 14 | notes | recompute | holds | 0.3143 | |
| 11 | Baseline columns are constant within a person; health is measured at enrolment | grouping, task_summary.known | count values per person; read the file's own variable labels | holds | 17 columns have 0 persons with more than one value (num and xage vary). The dta labels read "mhi ... -- baselin", "disea ... -- ba", "physlm ... -- baselin", "ghindx ... -- baselin". `hlthg/f/p` carry no timing label (constant within person; the paper says self-assessed health was "measured at an initial point", line 1639) | LEAK-10 |
| 12 | Family size and age are "that year" | notes "Features" | count values per person | holds | num varies for 1,119 persons; age steps +1.0 (14,266) or +2.0 (12, the gaps) | |
| 13 | `black`: one fractional value per site for 81 persons (0.511 at site 6); `physlm`: fractional values for 433 persons; both are filled-in means | notes, Decision 1 | count, and compare with the site means | holds (approximately) | 81 and 433. Filled values are close to the site means (site 6 black 0.5112 against an observed row mean of 0.5065), not exactly the means over this extract's rows; the physlm fills sit near child or adult means | CLEAN-10 |
| 14 | `general_health_index` is missing for all of site 1 and for 5-9% elsewhere | notes | count | holds | site 1 100%; other sites 5.2-8.8% | |
| 15 | `disea` is non-integer for 5,400 of 5,912 persons; 13.73 repeats for 642 persons, 74.368 (mhi) for 399; "the extract's documentation does not settle" what the repeats are | notes "Anomaly" | split the repeated values by age and by `tookphys` | **refuted (the data settle it)** | Every child under 14 at enrolment holds one `disea` value per site: 393/393, 395/395, 255/257, 322/322, 282/282, 425/425. Site-1 adults with 13.732: 248 of the 370 without the baseline physical, 1 of the 401 with it. All 393 site-1 children hold mhi 74.368. These values are fill-ins, on 39.4% of shipped rows. The other non-integers come from a weighted index ("both") | CLEAN-10; treat like cases alike (principles) |
| 16 | `disea` and `mhi` fills, "if means over the rows, a weak transductive leak kept on purpose" | notes | effect of setting them to missing | holds (weak, in effect none) | One constant per site, close to the site mean of the measured adults (13.732 against 13.601). Setting the fills to missing: ridge -0.0005 ± 0.0002, RF -0.0007 ± 0.0005 R2 | LEAK-30 |
| 17 | `hlthg/f/p`: at most one set per row; excellent is the omitted category | notes | sum of the flags; R docs | holds | max sum 1 (the code also asserts it); randhealth docs: "omitted category is excellent" | CLEAN-12 |
| 18 | The family key leaves 1,603 persons alone, and 15 keys hold more persons than the family size; families cannot be held together | grouping, split | recount; try zper//10, zper//100 and runs of adjacent ids | holds | 1,603 / 15 recounted. zper//10 is constant on family columns in only 41% of groups; adjacency runs leave 2,523 persons alone. The key matches the family size for only 37% of keys | SPLIT-24, SPLIT-26 |
| 19 | Members of one family on both sides of the split do not matter (builder: coarse proxy changes nothing) | split text, builder | RF with groups that surely hold families together: site,plan,mdeoff (505 groups) and site,plan,mdeoff,pioff (929) | holds | person 0.0859 ± 0.008; 929 keys 0.0897; 505 keys 0.0857 | SPLIT-30 |
| 20 | `lpi` = ln(max(1, pioff)); `fmde` is a function of mdeoff and coins (DERIVED says "0 for the IDP, else ln(max(1, mdeoff/(0.01 coins)))"); `logc` is "coinsurance rate, coded; coins kept"; `linc`, `lfam`, `lnum`, `child`, `fchild`, `binexp`, `lnmeddol`, `xghindx` are copies | DERIVED, notes | recompute every formula | **partly refuted** | linc = log(income+1), lfam, lnum, child (<18), fchild, binexp, lnmeddol and xghindx match in 100% of rows. lpi matches 20,185 (5 rows with pioff NaN). `logc` ≠ log(coins+1) in 4,855 rows (plans 2-4: coins 100, logc 0; plan 13: coins 0, logc = log 96). The `fmde` formula fails in 3,779 plan-13 rows, where fmde = ln(mdeoff/0.95). Both columns are functions of `plan` (and `mdeoff`), which ship, so dropping them loses nothing | CLEAN-1 |
| 21 | The kept `coinsurance_rate` is the enrollee's cost sharing ("a payer knows ... coinsurance") | notes "plan columns" | compare with the file's own `logc` and `fmde` | **contradicted by the file** | Plan 13 (individual deductible, 2,591 shipped rows) has coins 0, but logc and fmde code 95%. Plans 2-4 (785 shipped rows) have coins 100, but logc codes 0. `plan` carries the truth for models | CLEAN-12 |
| 22 | Metric `r2` is the source's metric: Efron's R2, Estimation methods, eq. 3; the share of the maximum ranks models the same | metric | read the paper; check the algebra | holds | Eq. 3 is in "Estimation methods": "We used Efron's R2 because the four-part model is nonlinear". It is the paper's single criterion (a trimmed variant was computed and not presented, line 1011). The share ((R2b - R2a)/(1 - R2a))/maxR2 has derivative 1/((1 - R2a)·maxR2) > 0 on a fixed sample | MET-5, MET-11 |
| 23 | The metric is computable on every fold and means the same as in the source | metric | dummy (train mean) through `data_foundry.v2.metrics.scorer` on all 9 folds; units per fold | holds | Dummy R2 between -0.0019 and -0.00002 on every fold; 1,879-1,880 persons per test fold; dollars on both sides (MET-3). Cohort differs (all ages, non-completers kept), but the quantity is the same | MET-2, MET-3 |
| 24 | "The R2 of a fold moves with its few largest stays" | notes | each fold's SS_tot concentration; ranking with and without the top row | holds (stronger than written) | The single $39,182 row holds 40-56% of its fold's SS_tot; the top 10 rows hold 46-75%, the top 1% 77-90%. Leaving out the top row moves R2 by up to 0.06, but ridge-against-RF ranking flips on 0 of 9 folds | MET-10 |
| 25 | Newhouse estimate a maximum R2 of 14.5% | notes | paper | holds | line 1343 | |
| 26 | Cohort of the paper: aged 14 and over, completers, exit examination | notes, fit_reason | paper | holds | lines 1005, 1006, 1224 | |
| 27 | The prior-use adjusters as quoted | notes | paper | holds | line 1233 (the quote omits "for those with positive expenditures") | |
| 28 | Split: whole persons held out (Medicare calibrates on fee-for-service persons and applies to HMO enrollees) | split, grouping | groups disjoint; read the Introduction | holds | no person on both sides in 9/9 folds; line 965 quoted verbatim | USE-10, SPLIT-24 |
| 29 | Implied: the task is not temporal in nature (no `ForcedGroupedFromTemporal`) | data_tags | precedents; cost of training on later study years | **contested** | fit_reason concedes "the drift between calibrating a formula and using it is not tested". frempl, pricing_game_2017, allstate_1m and spanish_motor_2022_2024 (next-period cost, stacked periods, no usable windows) carry the tag. Measured cost within the experiment: test rows with study_year ≥ 3, model trained on study years ≤ 2 against a random subsample of the same size: ridge -0.0023 ± 0.0042, RF +0.0001 ± 0.0025. Site x study-year means explain 0.33% of target variance | SPLIT-8, SPLIT-3 |
| 30 | Implied: no copies across the split | | leak probe 5 | holds | 0.0% exact copies | LEAK-16 |
| 31 | Implied: every feature is known at the end of year t | | labels, constancy, pairing code | holds, except income (untested, U1) | only meddol and inpmis of t+1 are merged, and both leave the features | LEAK-10 |
| 32 | Not trivial, not a forecast: naive last value -0.427; prior spending alone 0.038; without this year's use 0.039 | builder | recompute the naive forecast and the one-feature linear model | holds | -0.427 (folds -0.195 to -0.725); 0.038 | TP-4, TP-10 |
| 33 | Partial target years | notes "Not features" | their share | holds; consequence unstated | 37 rows: median eligible fraction 0.51, mean target $2,408 (13.5x), 5.6% of SS_tot, 22 with admissions. Kept, as the MEPS precedent keeps persons who die | USE-5 |
| 34 | year 1995 (ICPSR 6439 first release 1995-06-05); public domain | metadata | ICPSR (403 on fetch; search summary of the CoreTrustSeal page); statsmodels COPYRIGHT | holds | "Original release June 5, 1995"; statsmodels: "This is in the public domain." (licence: EV-4, note only) | PROV-9, EV-4 |
| 35 | `Spatial` tag | data_tags | definitions.md | holds | six sites count as regions ("region, store location") | |
| 36 | Record: mdvis 0 for 31.2%, meddol 0 for 22.1%; 9 covariates give 2,760 distinct vectors | record screening | recompute | holds | 0.3124, 0.2206; 2,760 exact | |
| 37 | Record: "Metric: none deliberate found ... fallback rmse" | record screening | paper eq. 3 | **refuted** (superseded by the definition) | see claim 22 | MET-1, MET-5 |
| 38 | Record marker `No Good Target / Scientific Discovery` | record front matter | paper | **refuted** | the Introduction and "Dependent variables" set a prediction for capitation (lines 965, 1010) | USE-1, USE-2 |
| 39 | Record and unique_name: "doctor visits" | record name, unique_name | the shipped target | **refuted** | the target is next-year medical spending; mdvis is only a feature | USE-5 (naming); records.md |
| 40 | Record Assessment lines | brief | read the record | none exist | the record has only screening and CC lines | records.md |
| 41 | The price base is not stated on the data page | notes | the dta label (cut at 32 characters); third-party docs | holds narrowly | Ecdat/randhealth docs: meddol is "annual medical expenditures in constant dollars"; base year not stated | EV-2 |

**Refuted and contested claims, ranked (validity first, Must first)**

1. **P3, USE-1/USE-2: the record's `No Good Target / Scientific Discovery` marker (38).**
   - *What it changes:* the record says there is no target, while Newhouse et al. 1989 define one (prediction for capitation, eq. 3), and the definition ships it.
   - *Mildest remedy:* the curator drops the marker and keeps `Outdated` as a weighed factor. An Assessment line in the record should say this; none exists yet (40).
2. **P4, SPLIT-8 (Must), consistency: the implied "not temporal in nature" (29).**
   - *What it changes:* how the regime is labelled, not the regime. The four insurance precedents with the same facts are tagged `ForcedGroupedFromTemporal`, and the definition's own fit_reason names the untested calibration-to-use drift.
   - *The measured cost is about zero:* training on later study years adds nothing (RF +0.0001 ± 0.0025), and common site-year shocks explain 0.33%.
   - *Mildest remedy:* add the tag with that cost sentence, as in frempl and pricing_game. Or say in splits_comment why SPLIT-8 does not apply: the formula is applied to other persons, and study years are not calendar years. This is a consistency question for the curator.
3. **P6, MET-1/MET-5: the record's screening metric line, "fallback rmse" (37).**
   - *What it changes:* nothing in the definition, which already declares `r2` from eq. 3.
   - *Mildest remedy:* an Assessment line that supersedes it.
4. **P7, CLEAN-10 and treat-like-cases-alike: the `disea`/`mhi` "Anomaly" note (15).**
   - *What it changes:* the data settle what the note leaves open. The repeated values are fill-ins: a site constant for every child under 14 and for the site-1 adults without the baseline physical. That is 39.4% of rows. Decision 1 sets the same kind of fill-in to missing for `black` and `physlm`.
   - It also qualifies task_summary.known ("chronic disease" at enrolment): for children it is a site constant. That fits the paper's reason for leaving out children.
   - *Measured effect of the fix:* nil (ridge -0.0005, RF -0.0007).
   - *Mildest remedy:* rewrite the note with the measured fact. Optionally set the fills to missing so the treatment matches Decision 1.
5. **P7, CLEAN-12: `coinsurance_rate` against the file's own `logc` and `fmde`, and the DERIVED formulas (20, 21).**
   - *What it changes:* documentation only, because `plan` ships and carries the plan identity. The DERIVED comments for `logc` and `fmde` are wrong for plans 2-4 and 13 (4,855 and 3,779 raw rows).
   - The shipped `coinsurance_rate` is 0 for the individual deductible plan, though the file codes 95% there, and 100 for plans 2-4, though logc codes 0. That is 3,376 shipped rows. The note's "a payer knows ... coinsurance" reads that column at face value.
   - *Mildest remedy:* correct the two comments, and add a note that `coinsurance_rate` follows the file's coding (plan 13: 0, plans 2-4: 100) and that `plan` is the reliable identity. This ties in with builder issue 6 (plan labels).
6. **P7, CLEAN-11: "the recorded spending lacks its charges" (6).**
   - *What it changes:* wording only; the drop stands on the source's words.
   - *Mildest remedy:* "lacks part of its inpatient charges (68 of the 80 such years record some)".
7. **House rule, naming: unique_name "doctor_visits" (39).**
   - *What it changes:* a reader expects a visit count.
   - *Mildest remedy:* records.md keeps names stable. A rename is cheapest now, while the dataset is unbuilt and has no UUID; otherwise say it in the record. Curator's call (builder issue 1).

**Untested (cannot verify), ranked**

- **U1, P4, LEAK-10: whether `family_income` contains later years.**
  - *Ruled out:* that income is an average over each person's own years. In proxy families (adjacent ids with the same site, plan, educdec, mdeoff and pioff), 4,031 of 4,053 member pairs share income, including 241 of the 248 pairs whose years on file differ.
  - *Still open:* a family-level average over the family's years, or a baseline value. The dta label is cut off ("income based on annual income r").
  - Alone, income scores R2 -0.033, so any leak would be weak.
  - *What settles it:* the ICPSR 6439 codebook. Until then, keep it with a "Potential leak, kept on purpose:" note if the curator wants caution.
- **U2: when `hlthg/f/p` were measured.** They carry no timing label and are constant within person; the paper's self-assessed health was baseline. Reading: holds by inference.
- **U3: the price base.** Third-party docs say constant dollars, base year unknown. It does not change the task.
- **U4: the record's older probes on the visits target** (AUC 0.69-0.79, R2 0.02-0.27). They are for a different target and superseded; not re-run.
- **U5: the "earlier conversion made in the screening session".** That CSV was not located. The independent statsmodels comparison (claim 2) stands in for it.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Verdict: ship after changes.** No column was recorded after the prediction point, the end of study year t. The
year-t use columns end before the target year starts. The health columns are baseline measures: the Stata labels say
"-- baseline", and Newhouse et al. write "These variables were collected at entry into the study". The target year's
other outcomes and its eligible fraction are left out. Three things need a change or a decision. First, the extract's
site-mean fills are still in three columns, while the definition undoes the same fills in `black` and `physlm`.
Second, the "excellent" level of self-rated health includes children who were never asked. Third, `family_income`
may be an average over later years, though dropping it changes no score.

```text
Verdict: ship after changes.
Validity: LEAK-1/USE-3 hold (prediction point written first); LEAK-10 holds for 29 of 30 features; LEAK-10 open for
`family_income` (weak, unverified; dropping it moves R2 by -0.0002 HGB / +0.0004 RF); LEAK-30 triggered, weak (the
extract's site means in `chronic_disease_index`, `mental_health_index`, `education_of_decision_maker`; restoring them
to missing moves R2 by +0.0009 / -0.0001 / +0.0005); LEAK-33 holds (`person_id` is the group only).
Quality: CLEAN-10 triggered (fills kept in three columns but restored in two; "excellent" stands for "not asked" for
about 346 children); CLEAN-21 optional (the disease index is on two scales); CLEAN-12 questions (plan and site labels,
the coinsurance coding of the deductible plans).
For the curator: problem 1 (family_income, a case-by-case LEAK-10 call), problem 7 (37 partial target years).
```

**How this was read.** There is no codebook in the download, so the "codebook" here is the Stata variable labels of
`randdata.dta` (read with the definition's own `read_stata_110`; each label is cut at 32 characters) plus Newhouse et
al. 1989 (PMC4192960). "Data" means a measurement on the file. Frame: `dataset_io.from_definition`,
14,214 rows, 30 features, 9 shipped grouped splits. Scripts and outputs are in the run folder.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `medical_spending_next_year` (target) | `meddol` of year t+1, "medical exp excl outpatient men[tal]": the paper's dependent variable | target | float64, dollars. 52 years with `inpmis`=1 dropped; all 52 had an admission (4.0% of the 1,294 target years with one). 37 kept years are partial (eligible 0.08 to 0.98): mean $2,408 against $172, 5.6% of SS_tot | fine; question on the 37 partial years (problem 7) | CLEAN-11 |
| `person_id` | `zper`, "person id, leading digit is sit[e]" | group, not a feature | int64 | fine | LEAK-33 |
| `plan` | "hie plan number": 18 codes; plans 1-4 and 8-9 occur at site 1 only | yes: randomised at enrolment, constant per person | category | fine; labels unknown | CLEAN-12 (question; builder issue 6) |
| `site` | "site": the six HIE sites | yes | category | fine. The code-to-place mapping is not in the extract. Data, by inference: site 1 lacks `ghindx`, which matches the paper's Dayton; sites 3-4 and 5-6 share fill values, so they are likely the Massachusetts and South Carolina pairs | CLEAN-12 (question) |
| `coinsurance_rate` | "coinsurance -- medical", percent (0/25/50/95/100) | yes | float64, numeric | fine. But the deductible plans are coded 0 (plan 1), 100 (plans 2-4) and 95 (plan 13) | CLEAN-12 (question, problem 6) |
| `individual_deductible_plan` | `idp`, 0/1 | yes | category (checked: only 0 and 1) | fine | CLEAN-14 |
| `max_dollar_expenditure` | `mdeoff`, "maximum expenditure offer": the out-of-pocket cap in dollars, 0 in the free plan | yes, constant per person | float64 | fine | |
| `participation_incentive` | `pioff`, "participation incentive", dollars | yes, constant per person | float64. `lpi` = ln(max(1, pioff)) to within 3e-7, so dropping `lpi` is right | fine (the fit note is in the comments) | USE-6 |
| `took_baseline_physical` | "took baseline physical": the enrolment exam, not the exit exam | yes | category (0/1) | fine | |
| `study_year` | "study year" t, 1 to 4 | yes | int64 | fine | |
| `age` | `xage`, "age that year" (year t) | yes | float64 | fine | |
| `female` | 0/1 | yes | category | fine | |
| `black` | 0/1. 81 persons held one fractional value per site; these are now missing | yes | category | fine (fix applied) | CLEAN-10 |
| `family_income` | "income based on annual income r…". The value is the same in every year of a person's 3-5 years | **unverified.** It is not the enrolment income that set the cap (problem 1), and it may average the annual reports, target years included | float64. 49 persons at 0 (all at sites 5-6) and 27 at exactly 1.0 (all at sites 1-4) | question (problems 1 and 5) | LEAK-10 (weak), CLEAN-10 |
| `education_of_decision_maker` | "education of decision maker", years | yes, constant per person | float64. **68 persons hold one of five per-site constants** (12.3251, 12.7567, 11.3874, 10.9698, 10.6277), each within 0.07 of its site's observed mean; 157 rows of 62 persons in the frame | cleaning problem: set them to missing (problem 2) | CLEAN-10, LEAK-30 weak |
| `family_size` | `num`, "family size" in that year (it changes over time for 20% of persons) | yes | float64 count | fine | |
| `outpatient_spending` | "outpatient exp. excl. ment and [dental]", year t | yes: year t ends at the prediction point | float64 | fine | LEAK-10 holds |
| `drug_spending` | "drugs purchased, outpatient", year t | yes | float64 | fine | |
| `supplies_spending` | "supplies purchased, outpatient", year t | yes | float64 | fine | |
| `inpatient_spending` | "inpatient exp., facilities & md", year t. Too low when `inpatient_charges_missing`=1 | yes | float64 | fine: the flag marks the 54 years that are too low | |
| `medical_spending` | `meddol` of year t: the sum of the four columns above (20,188 of 20,190 raw rows), i.e. the lagged target | yes | float64. It is a sum, not a copy, so CLEAN-5 does not apply | fine: the paper's prior-use adjusters are built from it | LEAK-34 by analogy; CLEAN-5 |
| `psychotherapy_spending` | "psychotherapy exp., outpatient", year t; not part of the target | yes | float64 | fine | |
| `hospital_admissions` | "number of hosp. admissions", year t | yes | float64 count | fine | |
| `inpatient_charges_missing` | "missing any inpatient charges", year t (54 rows) | yes | category | fine | |
| `psychotherapy_visits` | "number psychotherapy visits", year t | yes | float64 count | fine | |
| `md_visits` | "number face-to-fac[e] md visits", year t | yes | float64 count | fine | |
| `non_md_visits` | "number face-to-face, not-md vis[its]", year t | yes | float64 count | fine | |
| `mental_health_index` | "mental health index -- baseline", 0-100 | yes (enrolment) | float64. **1,133 persons hold one of four site-group constants** (74.3683 site 1; 81.3527 site 2; 83.3914 sites 3-4; 77.4003 sites 5-6); 1,102 of them are children; 2,494 rows (17.5%) in the frame. The other values come from three item sets: adults at sites 2-6 (steps of about 0.5), Dayton adults (about 1.0) and children (1/60) | cleaning problem: set the constants to missing (problem 2); the mix of item sets is a note (problem 8) | CLEAN-10, LEAK-30 weak, CLEAN-21 note |
| `chronic_disease_index` | "count of chronic diseases -- baseline". Data: 100 × count / 29 at sites 2-6 and 100 × count / 23 at site 1; every value that is not a fill lies on one of the two grids | yes (enrolment) | float64. **2,387 persons hold one of four site-group constants** (13.7319, 11.8427, 9.9673, 10.5763): 2,072 of the 2,074 children (the other two are aged 13.9) and 315 adults; 5,604 rows (39.4%) in the frame | cleaning problem: set to missing (problem 2); optional: convert back to a count (problem 4) | CLEAN-10, LEAK-30 weak, CLEAN-21 |
| `physical_limitation` | "physical limitations -- baseline", 0/1. 433 persons held fractional fills; these are now missing | yes | category | fine (fix applied) | CLEAN-10 |
| `general_health_index` | "general health index -- baseline". Missing at site 1 (the paper says GHIOOP was used at Dayton, and the extract does not have it) and for 5-9% of persons elsewhere | yes | float64, missing values kept | fine | |
| `self_rated_health` | `hlthg`/`hlthf`/`hlthp`, coded against "excellent"; baseline, constant per person | yes | category; the merge is lossless (at most one flag set) | cleaning problem: "excellent" also stands for "not asked" for children without the baseline questionnaire (problem 3) | CLEAN-10, CLEAN-13 |

The dropped columns were checked too:
- `time` is 1 in every pair for year t. The target year's eligible fraction comes after the outcome and is rightly
  not a feature.
- The derived copies match their formulas: `linc` = log(income + 1) to within 5e-7, `lpi` as above.
- `xghindx` holds the extract's fills, so dropping it is right on two counts.
- `hlthg/f/p` are merged into `self_rated_health`.

None of the year-t use columns that the screening flagged as outcomes is a leak under the next-year framing: they are
history, the source of the paper's prior-use adjusters.

**Problems, ranked (principles.md: P4 before P7, then by strength, then by effect)**

1. **`family_income` may hold later years (P4, LEAK-10 Must if it is a leak; weak and unverified).**
   - The label is cut off ("income based on annual income r…"), and the value is the same in all of a person's 3-5
     years.
   - RAND ties the cost-sharing cap to family income: "such payments are limited to 5 or 15 percent of the family's
     income". So if `family_income` were the income the cap was set from, cap / income would be one fixed share for
     everyone in a plan.
   - It is not. Test: persons with a cap between $0 and $1,000, outside plan 13 (whose cap is $150 per person). The
     median ratio per plan ranges from 0.043 to 0.186, and only 0-23% of a plan's persons lie within 1% of its
     median. So the column is not the enrolment income behind the cap, at least not in the same units.
   - One reading fits the label: an average of the annual income reports over the person's years, which would
     include the target years. This is circumstantial; the cap may rest on another income concept.
   - Dropping the column on the 9 shipped splits: HGB 0.0737 to 0.0735, RF 0.0819 to 0.0823.
   - Mildest remedy: LEAK-10's second clause covers later values that cannot be located row by row. It allows a keep
     with a note only when the traceable part shows no gain, and here the whole column shows none. So either keep it
     with a `Potential leak, kept on purpose:` note giving these numbers, or drop it, which costs nothing.
   - The ICPSR 6439 codebook would settle it. The decision is the curator's, case by case (builder issue 4).
2. **The extract's mean fills are kept in three columns, while the same fills are undone in two (P4, LEAK-30 weak,
   Should; P7, CLEAN-10).**
   - The anomaly bullet says "a weighted index, filled-in values or both; the extract's documentation does not
     settle it". The data settles it, and EV-2 ranks a measurement on the data above a page.
   - `chronic_disease_index` is a scaled count, 100k/29 or 100k/23 per site. The four values off both grids are one
     constant per site group, held by 2,072 of the 2,074 children (the paper: "our measures of health status are
     different for persons of younger ages") and by 315 adults. Each constant lies 0.03-0.33 from the mean of the
     observed values in its site group.
   - `mental_health_index` has four site-group constants held by 1,133 persons, 1,102 of them children.
     `education_of_decision_maker` has five per-site constants held by 68 persons.
   - This is the mechanism the definition already reverses for `black`: its fills lie within 0.01 of the observed
     site means. The extract's own `xghindx` ("ghi with imputation") shows that its makers filled `ghindx` with
     site-group means too (76.9704, 79.2215, 70.6899).
   - The fills are sample means that include the test persons, which makes them a weak transductive leak.
   - Restoring them to missing moves R2 on the 9 shipped splits by +0.0009 (HGB, higher on 7 of 9 splits), -0.0001
     (ridge) and +0.0005 (RF): no gain either way.
   - Mildest remedy: the same treatment as `black` and `physlm`, one block in `_clean` before the rename. Then extend
     the Decision table and rewrite the anomaly bullet to say what the values are:

   ```python
   # Values the extract filled in with one mean per site or site group (2,072 of 2,074 children for disea).
   FILLS = {
       "disea": {1: 13.7319, 2: 11.8427, 3: 9.9673, 4: 9.9673, 5: 10.5763, 6: 10.5763},
       "mhi": {1: 74.3683, 2: 81.3527, 3: 83.3914, 4: 83.3914, 5: 77.4003, 6: 77.4003},
       "educdec": {1: 12.3251, 2: 12.7567, 3: 11.3874, 5: 10.9698, 6: 10.6277},
   }
   for col, by_site in FILLS.items():
       df[col] = df[col].mask((df[col] - df["site"].map(by_site)).abs() < 1e-3)
   ```

   - The other remedy is to keep the fills with a note that names them as fills (aeolus_rebuilt kept Meteostat's
     model fills with a remark, Lennart, 2026-10-26). Within one definition, though, treating like columns alike
     (principles.md) argues for setting them to missing.
3. **"excellent" includes children who were never asked (P7, CLEAN-10; also CLEAN-13's reference level).**
   - Sites 2-6: 265 children have `ghindx` missing and `physlm` and `mhi` filled. Of these, 258 (97.4%) read
     "excellent", against 66.1% of the 1,367 children without any of these gaps.
   - Site 1: 56 of 57 children with a filled `physlm` read "excellent", against 60% of the other children there.
   - Over all sites, 346 of the 371 children with a filled `physlm` are "excellent" (93% against 64.8%). Many of them
     look like children born during the experiment: 115 of the 371 have no two consecutive years.
   - The cause: all three flags are 0 when there is no rating, so the reference level absorbs "not asked".
   - Mildest remedy: set `self_rated_health` to missing for a child (under 14 in the first year) whose `physlm` was
     filled and who has no flag set. That is 346 persons in the raw file, and the rule reads no label. Otherwise keep
     it with a note. Either way the score effect is negligible: the restored `physlm` gaps already mark these
     children.
4. **The disease index is on two scales (P7, CLEAN-21, Should; optional).**
   - One disease adds 4.35 at site 1 and 3.45 elsewhere. The label says "count of chronic diseases".
   - Remedy: rebuild it as `chronic_disease_count` = `disea` × 23/100 at site 1 and × 29/100 elsewhere (integers once
     the fills are missing), with a note that the two disease lists differ. Otherwise keep it and correct the bullet.
5. **Income 0 against 1.0 (P7, CLEAN-10, question).**
   - 49 persons have exactly 0, all at sites 5-6. 27 have exactly 1.0, all at sites 1-4. No value lies between 1 and
     17.6.
   - This reads like one state ("no income") coded two ways by site, but true zeros would also cluster at the poorest
     sites.
   - Remedy: set 1.0 to 0 only if the codebook confirms; otherwise keep.
6. **Plan, site and coinsurance codes have no labels (P7, CLEAN-12, question; adds to builder issue 6).**
   - The deductible plans carry three coinsurance values: plan 1 (site 1) is coded 0, plans 2-4 (site 1) 100, and
     plan 13 (sites 2-6) 95.
   - If `coins` mixes the inpatient and outpatient rates across the Dayton plans, the same number means different
     plans. `plan` stays as a categorical, so a model can separate them.
   - Remedy: labels from the ICPSR codebook or Manning et al. 1987 if they can be had; otherwise a note.
7. **37 partial target years (P7, CLEAN-11, question; recommend keep).**
   - These are target years with an eligible fraction of 0.08 to 0.98. Their mean is $2,408 against $172, and they
     hold 3.5% of all spending and 5.6% of SS_tot.
   - 19 of them come after study year 1 (so the target is year 2), which is not a scheduled end: they are probably
     deaths and exits during the experiment.
   - CLEAN-11 lets a row leave only when the source names its target as not the task's quantity, and none does. A
     payer bears these costs.
   - Remedy: keep them, and add the numbers to the "Not features" bullet so a reader knows that 37 rows carry 5.6% of
     the variance.
8. **The mental health index comes from three item sets (P7, note).** Adults at sites 2-6 move in steps of about
   0.5, Dayton adults in steps of about 1.0, and children in steps of 1/60. The paper says the 38-item MHI was
   "administered in sites other than Dayton". All three are 0-100 scales, so this needs a sentence, not a fix.

**Comment claims checked on the data (all hold).**
- `black` 81 persons; `physlm` 433 persons.
- `disea` non-integer for 5,400 persons; 13.73 for 642 persons. `mhi` 74.368 for 399 persons.
- `ghindx` missing at site 1 and for 5-9% of persons elsewhere.
- `time` is 1 for every year t; 37 target years are partial.
- All 52 dropped target years had an admission.
- `lpi` and `linc` match their formulas.

**Sources (web, income question only).** Neither source defines the extract's `income` variable.
- [RAND R0965-1, The Health Insurance Study: A Summary](https://www.rand.org/pubs/reports/R0965-1.html): the cap as
  a share of family income.
- [randhealth dataset page](https://r-packages.io/datasets/randhealth): repeats the truncated label.

</details>

<details><summary>Split audit</summary>

**Split audit: rand_health_insurance_experiment_doctor_visits (split-auditor, 2026-11-01)**

**Verdict: right with notes.** Grouping by person is the right regime among those the extract allows, and IID would be
wrong. Two things in the text need fixing. First, the task is temporal by its use case and ships under SPLIT-8
without saying so: the `ForcedGroupedFromTemporal` tag and the cost on the valid windows are missing. Second, the
claim that families cannot be rebuilt is refuted: a family id can be built exactly from the data. Holding families
together changes nothing measurable, so the person split can stay if the text is corrected.

```text
Verdict: right with notes.
Validity: SPLIT-2, SPLIT-23 hold (one prediction = one person-year, context none); SPLIT-29 holds against IID
  (a feature lookup scores R2 0.372 under random rows); SPLIT-9 holds (no measurable shortcut from later years);
  SPLIT-8 triggered, not documented (tag and cost missing; cost measured: none); SPLIT-24/SPLIT-30 family claim
  refuted, effect measured nil.
Value: P6 note: one target of $39,182 carries 20.3% of the total sum of squares and halves its fold's R2.
For the curator: tag ForcedGroupedFromTemporal (issue 1); group on the rebuilt family or correct the text (issue 2).
```

All numbers come from untuned random forest (300 trees, min_samples_leaf 20) and ridge (alpha 10) models, R2 in
dollars. The frame and folds were loaded through `dataset_io.from_definition`, so they are the definition's own 3x3
person folds: 9,436-9,498 train rows, 4,716-4,778 test rows, no person on both sides of any split. On these folds
both models score R2 0.0856, against 0.084 (linear) and 0.093 (random forest) in the builder's task probe. Scripts and
outputs are in the run folder.

**Problem 1 (P4, SPLIT-8 Must with SPLIT-3 and USE-10): the task is temporal by its use case and ships grouped
without the tag or the cost statement.**

* The use case. A payer sets next year's capitation, so the formula is fit on past years and applied to the coming
  year. The definition's own `fit_reason` says "no calendar years, so the drift between calibrating a formula and
  using it is not tested". The `grouping.definition` presents grouping as the natural regime ("calibrated on one
  population and applied to enrollees outside it"). That covers the new-person side of the use case and drops the
  time side.
* What the release allows. `year` is the study year (1-5), not a calendar year. Newhouse et al. 1989, "Source of
  data": the experiment "operated from 1974 to 1982", and families "were randomly assigned to a 3-year or 5-year
  participation period". The sites started at different dates, Dayton first and Georgetown County last, so a study
  year mixes calendar years across sites. This is inference: no calendar date is in the extract, and the mapping from
  site code to city is unverified (builder issue 6).
* Windows by target study year, with train = every earlier target year. Rows per target year: 5,454 (year 2), 5,401
  (year 3), 1,677 (year 4), 1,682 (year 5).
  * Testing on year 5 trains on 88.2% of the rows.
  * Testing on year 4 trains on 76.4%.
  * Testing on year 3 trains on 38.4%, below the 50% floor.
  * So two windows qualify where SPLIT-14 asks for three. Years 4-5 also hold only the 5-year enrollees. This is the
    SPLIT-8 case "too few periods ... stacked and grouped by the entity" (`ForcedGroupedFromTemporal`).
* The cost on the valid windows. The table compares each window with the shipped folds scored on the same
  target-year rows (each repeat covers every row once).

  | test rows | temporal window RF / ridge | shipped person folds RF / ridge | temporal, test persons removed from train RF / ridge |
  |---|---|---|---|
  | target year 4 (1,677) | 0.147 / 0.129 | 0.135 / 0.135 | 0.145 / 0.127 |
  | target year 5 (1,682) | 0.112 / 0.113 | 0.098 / 0.103 | 0.098 / 0.110 |

  The forced grouped split is no more optimistic than the valid windows. Its train sides are smaller: about 67% of
  the rows, against 76-88% for the windows. On those windows, knowing a person's earlier years adds 0.002-0.014.
* Drift the person split cannot test. Mean target by target year: $170, $172, $195, $209. The medians are $32-39 and
  the p99 rises from $2,230 to $2,904. This cannot be separated from ageing, the extract's unstated price base (the
  definition notes this) and the 5-year enrollees' mix. There is no clear end-of-participation effect: at target year
  3, the 3-year enrollees (their last year) spend $18 more than the 5-year enrollees, 95% bootstrap interval -13 to
  49.
* Precedents in this run. Four insurance datasets are tagged `ForcedGroupedFromTemporal` on the same reasoning ("a
  tariff is fit on past years and applied to the next"): `frempl_french_motor_personal_line`,
  `pricing_game_2017_french_mtpl`, `spanish_motor_insurance_coverage_level_2022_2024` and
  `allstate_claim_prediction_challenge_1m`. The Spanish one states its one valid window against the folds in
  `splits_comment`, as asked here.
* Steelman for leaving it untagged. Newhouse et al. ask a cross-sectional question, in-sample R2 of adjusters with no
  holdout ("Estimation methods"). Each row already pairs a year with the next one, so the time order inside a person
  is respected. Against this, the use case as written is a forecast of next year's payment, and the siblings decide
  it the same way.
* Remedy (mildest: text only, no re-split): add `"ForcedGroupedFromTemporal"` to `data_tags` and write a
  `splits_comment`. It should say that the study years give two windows that meet the floor, with the numbers above,
  and that a release with calendar years should get a temporal split. The record's tags may need the same note.

**Problem 2 (P4, SPLIT-24 and SPLIT-30 Must; effect measured nil): "Families cannot be held together" is refuted.**

* The claim, in `grouping.definition` and `task_summary.split`: "the extract has no family id, and the family-level
  columns ... do not rebuild one (1,603 persons would be alone, and 15 keys hold more persons than the family size)".
* The builder's key included `educdec`, and `educdec` is not constant within a family. It takes more than one value
  in 845 of the 1,404 rebuilt multi-person families. This is for the column auditor: "education of the decision
  maker" may be the person's own.
* An exact key exists, of the form SPLIT-24 allows (consecutive blocks with identical values, as in
  in_vehicle_coupon_recommendation): consecutive `zper` values with identical site, plan and family income.
  * The raw file gives 2,523 families for 5,912 persons, and 2,355 families in the shipped rows.
  * 58.8% of families hold exactly the family size and 4 hold more. 1,035 hold fewer, probably members outside the
    extract (unverified).
  * The coarse key alone (site|plan|income, the builder's own key) leaves only 5 persons of
    multi-person families alone.
  * These are families: the correlation of log1p mean spending between members is 0.315, against 0.056 for persons of
    the same site and plan in other families.
* Exposure. 75.7% of the test rows of the shipped folds have a family member on the training side.
* Effect.
  * Grouping on the rebuilt family scores RF 0.0835 and ridge 0.0787, against 0.0821 and 0.0794 for person groups on
    the same seeds (SE about 0.007).
  * An explicit family-target feature (the training family members' mean log spending, leave-person-out) adds
    +0.0002 (RF, SE 0.0003) and 0.0000 (ridge) on the shipped folds.
  * This row's own spending already carries the family effect.
  * The builder's coarse-key test agrees: RF 0.0880 against 0.0893.
* Remedy, for the curator.
  * (a) Mildest: keep the person split. Rewrite the family sentences: a family can be rebuilt (the key above), about
    three quarters of test rows have a family member in training, and holding families together scores the same.
  * (b) Group on the rebuilt family id (a column used only for grouping, never a feature). Under SPLIT-4 the
    use case decides, not the gap. New enrollees arrive as families that are not in the calibration sample, and the
    re-split costs nothing measured.
  * I lean to (b), since it removes a caveat at no cost. The rebuilt key is not checked against a codebook,
    though, which argues for (a).

**Checks that hold**

* IID would be wrong (SPLIT-29, SPLIT-2).
  * 60.3% of rows have their target stored as `medical_spending` in the same person's next row.
  * The person-constant columns give 5,631 distinct keys for 5,638 persons.
  * Under random 3x3 row folds, a lookup from the features alone finds the person's next-year row on the training
    side for 40.1% of the test rows (exact target in 99.9% of hits). Lookup-or-mean scores R2 0.372, against 0.089 (RF)
    and 0.082 (ridge).
  * On the shipped folds the same lookup hits 0.04-0.13% of the test rows: the 7 keys shared by two persons.
  * RF and ridge do not use this lookup (IID 0.089 / 0.082 against person folds 0.086 / 0.086), which is why the
    group probe's gap is small (LightGBM -0.006 against -0.030). Under SPLIT-4 the gap does not decide.
* Group id (SPLIT-24). `zper` is the extract's person id, a true id: its leading digit equals `site` in every row.
* What one prediction is (SPLIT-23). The unit is the person-year, as in Newhouse et al., "Dependent variables": "The
  unit of analysis was the person-year". Hence `prediction_unit="row"` and `labels="per_sample"`.
* Known about a new group. `context="none"` is right: a row carries its own year t, and a test person's other rows
  are not context. A real payer may know more than one prior year. The paper's prior-use adjusters fit one year.
* Training rows labelled after a test row's prediction point (SPLIT-9). Under the person split, the training side
  holds other persons' later study years. Dropping `study_year`, the only column that places a row in time, changes
  R2 by -0.0005 (RF) and +0.0004 (ridge). No shortcut from contemporaneous labels is measurable.
* Source split (SPLIT-19). None: the paper reports in-sample R2 and prescribes no holdout.
* Forecasting (TP-10). Not run by me. The builder's naive last-value forecast scores -0.427.

**Notes (no split change)**

* Heavy tail (P6, for the metric and claim auditors). The largest target ($39,182) carries 20.3% of the total sum of
  squares.
  * The three lowest of the nine fold scores (0.045-0.047 RF) are exactly the three folds that hold it.
  * In repeat 0, its fold scores RF 0.045 with it and 0.085 without that one row.
  * The protocol is standard. The definition's note ("the R2 of a fold moves with its few largest stays") is right
    and could give this number.
* Label delay (cannot verify). The prediction point, "the end of a study year", assumes year t's spending is complete
  then. In practice claims run out over months. Newhouse et al. report claims for "about 90 percent" of physician use,
  which is a completeness figure, not a delay. The extract has annual totals and no claim dates, so no gap can be set
  or measured. At most, one sentence in the notes.

Sources outside the repository: the RAND HIE site order, from a web search that found no site enrolment dates
([ICPSR 6439](https://www.icpsr.umich.edu/web/DSDR/studies/6439/versions/V1),
[arXiv 2205.09736](https://arxiv.org/pdf/2205.09736)). The paper text is PMC4192960.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: rand_health_insurance_experiment_doctor_visits**

Actor: a health-plan actuary (and, behind them, the payer setting a per-enrollee capitation). At the start of a plan year I
forecast each member's expected medical cost for that year from what I hold at the end of the last one. This is the
definition's own use case (Newhouse et al. 1989, the AAPCC adjusters) and the framing of the sibling
`meps_total_healthcare_expenditure` (CC 2026-10-20: "payers setting next year's per-member payments ... care management").

**Fit: approximate (agree with the definition).** This is the source's own question on the source's own data:
next-year dollars from prior use, demographics and health, with persons held out (USE-1, USE-5). But it is a 1974-1982
experiment on people under 65 with randomised cost sharing. It has survey health measures from enrolment where a payer
today has claims diagnoses, and it has no calendar time, so the drift between calibrating a formula and applying it is
untested (USE-8). Nothing in the data offers another use case that would make the fit direct (USE-9): the age of the
data stays a gap under any rewording.

**1. Inputs at the prediction point (USE-3, USE-6)**

- Inputs I have at the end of the year: age, sex, site (the AAPCC's county), family size (the contract), the benefit
  design (coinsurance, individual deductible, out-of-pocket cap), and this year's claims: spending by type, MD and other
  visits, admissions, and the missing-charges flag. A payer gets the year's claims with a lag; CMS-HCC sets provisional
  rates on 6-month-lagged data and final rates by June 30 of the payment year (Pope et al. 2004). Final reconciliation
  therefore uses the whole year, so treating year t as complete is fair.
- Inputs I would not have as a payer: `black` (race is not a payment adjuster), `family_income` (one value per person
  for 100% of persons, so it is a baseline value or an average over the study years, which builder issue 4 leaves
  unverified), `education_of_decision_maker`, `participation_incentive` (a payment the experiment made; its correlation
  with the target is -0.02), `took_baseline_physical` (an assignment flag of the experiment), and the five survey health
  measures. A plan with an enrolment health-risk questionnaire would have something like the survey measures. Newhouse
  et al. call such measures prone to fraud. They are also from enrolment only, so for a year-4 row they are 3-4 years
  old. All of these are known at the prediction point, so USE-6 lets them stay. They make this a research feature set,
  not a payment feature set, and the MEPS sibling was judged the same way ("survey items a payer's claims lack, so for
  payers the task is an approximation").
- Inputs I would always have but the data lacks: diagnoses from claims, the input every prospective formula has used
  since DCG/HCC. CMS-HCC predicts next-year cost from "diagnoses collected in a base year" plus demographics and
  Medicaid status (Pope et al. 2004), and Newhouse et al. had a claims-based diagnosis set too ("AAPCC plus dichotomous
  physiologic health based on claims", 31% of the maximum). The data also lacks a welfare (AFDC or Medicaid) flag, which
  was one of the four AAPCC adjusters in the paper. This is the input gap that matters most, and `fit_reason` does not
  name it.
- What the inputs actually carry: a ridge on six inputs (age, sex, site and this year's total, outpatient and inpatient
  spending) scores R2 0.090 ± 0.037 on the 9 shipped splits, the same as ridge on all 30 features (0.090 ± 0.039) and
  RF on all features (0.085 ± 0.031). So the task
  as shipped is essentially the paper's "AAPCC plus prior-year use" row. The survey, income and plan columns add nothing
  measurable in dollar R2. The columns a payer lacks therefore do not inflate the task, which supports keeping them as
  they are.

**2. The target (USE-5)**

- Next-year medical spending in dollars is what I act on. A capitation pays the expected cost, so I want a number: the
  conditional mean, not a class and not the median. The quantity is the paper's dependent variable ("virtually all
  medical services other than dental and outpatient mental health"). That exclusion is a benefit carve-out, not a
  proxy. Because 22.7% of target years are zero and the median is about $35 against a mean of $178, the mean is the
  functional that counts.
- Small gaps:
  - The price base is not stated. Medians by feature year are flat (31.8, 34.9, 34.2, 39.3 for years 1-4), which is
    consistent with constant dollars.
  - The 37 partial target years are neither annualised nor weighted. CMS calibrates on annualised cost weighted by
    eligible months. At 37 rows this is negligible.
  - The `unique_name` says "doctor_visits" while the target is spending. A practitioner searching for a visits task
    would be misled. I second builder issue 1: rename (e.g. `..._medical_spending`).

**3. One row, one decision; the test data (USE-10)**

- One row is one member-year: one payment or forecast per member per plan year. That is the unit I act on, and the
  metric scores per row (`prediction_unit="row"`), which is right.
- The test persons are new, and each one's previous year is a feature. That mirrors a formula calibrated on one
  population (fee-for-service beneficiaries) and applied to another (the HMO's enrollees), each with a base year,
  which is how CMS-HCC works.
- For an HMO forecasting its own members, the members are known entities and a temporal split would also be right
  (USE-10). The grouped split is the stricter of the two readings and the one the paper's framing asks for.
- What is missing from the test data:
  - Later years: calibration in one period and use in the next is not tested, since the data has only study years and
    sites started at different calendar dates.
  - Whole families: members of one family can sit on both sides of a split. The paper says accounting for family
    correlation "would not greatly affect our estimates", and the builder's family proxy changed RF by 0.001.

**4. Would I use this model?**

- I would not deploy it: 1970s prices and practice, randomised free care for part of the sample, six sites, no
  diagnoses. I would use the dataset to compare methods on the problem I face every year: zero-heavy, heavy-tailed
  annual cost, where 1% of rows hold 30.0% of next-year spending and 5% hold 58.9%, the year-to-year correlation is
  0.19, and the ceiling is low.
- What makes me trust it: it reproduces the paper's levels.
  - Newhouse et al.'s full model explains 62% of a 14.5% maximum, about 9.0%. The builder's RF scores 0.093 and the
    linear model 0.084.
  - Without this year's use, RF scores 0.039, against the paper's 2.8-4.6% for health measures without prior use.
  - The plan effect has the expected direction: next-year mean $191 on free care, $140 at 95% coinsurance.
- What makes me distrust it:
  - Model differences of 0.005-0.01 sit inside a split-to-split spread of 0.04-0.15 per split (RF, builder: 0.036 to
    0.148), driven by a few large hospital stays.
  - Dollar R2 barely punishes a formula that pays nothing at the low end. Ridge's predictive ratio in the lowest decile
    of predictions is -0.007 (it predicts about $0 or less, which no actuary would sign off), against RF's 0.95; in the
    top decile both are 1.10-1.12.
  - Untuned LightGBM scores below the dummy (-0.008). This is a property of the tail, not a defect, but it means the
    benchmark tests robustness to heavy tails as much as signal.

**5. The metric: yes, `r2` in dollars scores my decision**

- A capitation pays the conditional mean, and R2 = 1 - MSE / Var(y_test) ranks models on a fold exactly as MSE does.
  MSE is the scoring function whose best prediction is the mean.
- It is the source's deliberate criterion (MET-5). The paper calls explained variance "the most common metric for
  judging the AAPCC", computes only Efron's R2 (a 98th-percentile trimmed version gave "similar" shares) and ranks
  every specification by it.
- It is also what the field uses at the individual level today: CMS judges CMS-HCC by "the R2 statistic ... for
  individuals" and by predictive ratios for groups (Pope et al. 2004).
- The scale is right (MET-3): dollars, no log, because a capitation pays dollars and a model fit on logs needs a
  retransformation, as the note says.
- MET-6 to MET-9 do not apply: there is no threshold, no k and no cost matrix in the payment decision.
- I would not choose MAE (which the SOA risk-score comparisons also report) as the benchmark metric. It is minimised by
  the median, about $35 here, and a formula built on it would underpay the mean by roughly 80%.
- The metric I would choose is the declared one (MET-1, MET-11 `source` holds).
- Two side readings, neither a change to the metric:
  - The R2 on a trimmed target (top 2% set to the mean of the top 2%, the paper's robustness check) is steadier: 0.128 to
    0.133, with a spread of 0.018-0.026 against 0.031-0.039 for the raw R2. It would be a useful diagnostic, but the
    source ranks on the untrimmed value.
  - Group predictive ratios are what an actuary checks next. They are a report, not a single benchmark number.
- The use case also says "An HMO or care manager can use the same prediction to plan for its high spenders". R2 does
  not score that decision. Picking members for outreach is a top-k choice, scored by the share of spending captured:
  the top 5% of predictions capture 23-24% of next-year spending and recall 25% of the true top 5%. Either drop that
  sentence or accept that the metric scores only the capitation decision. I would drop it.

**Gaps, ranked by how much they change the task**

1. **Era and population** (USE-8; already in `fit_reason`): a 1974-82 experiment on people under 65 with randomised
   plans, inpatient-dominated costs and unstated constant dollars. The form of the task survives (zeros, heavy tail,
   prior-use signal, low ceiling), but no number transfers.
2. **No claims diagnoses or welfare flag; survey items instead** (USE-6, USE-8; not in `fit_reason`): today's payer
   predicts from diagnoses. The shipped task is "AAPCC plus prior use" (a 6-input ridge equals the full model), which
   modern payment formulas deliberately avoid. Pope et al. 2004 wanted "payments to follow what medical problems were
   present as opposed to what services were offered", and Newhouse et al. note that use-based adjustment dilutes the
   incentives of capitation. Prior cost does fit an HMO's own cost forecast, renewal pricing or the paper's research
   question.
3. **No calendar time; families split** (USE-10): calibration-to-use drift is untested, and family members can fall on
   both sides of a split. Measured effect is small (family proxy: 0.001).
4. **Name says visits, target is spending** (USE-5): a labelling gap with no effect on the task, cheap to fix now.
5. **Inputs that change meaning at age 14**: the paper's MHI is 38 items for adults and 12 for children, and
   `general_health_index` is an adult scale yet present for 71% of under-14 rows (31.4% of rows are under 14). Age is a
   feature, so a model can separate the two, but the notes should say it.
6. **37 partial target years kept unweighted**: negligible.

**What a domain expert would change**

- Name the missing claims diagnoses (and the welfare flag) in `fit_reason`, next to "health at enrolment only".
- Rename the dataset to say spending (builder issue 1).
- Make the use case match the inputs. Keep the paper's question ("how much do prior use and health measures add to
  the AAPCC's demographic adjusters") or name the plan's own next-year cost forecast as the actor. Drop the "care
  manager ... high spenders" clause, which `r2` does not score.
- Add one line to the notes that the health indexes switch instrument at age 14.
- Keep the experiment-only columns (`participation_incentive`, `took_baseline_physical`) and the survey columns. They
  are known at the prediction point (USE-6) and carry no measurable dollar-R2 signal, and dropping them would change
  nothing a payer would notice.
- Keep `r2` in dollars, untrimmed, as `Metric.source` (MET-1, MET-3, MET-5).

**Sources**

- Newhouse, Manning, Keeler, Sloss 1989, "Adjusting capitation rates using objective health measures and prior
  utilization", Health Care Financ Rev 10(3):41-54, https://pmc.ncbi.nlm.nih.gov/articles/PMC4192960/ : Introduction, Source of data, Dependent variables, Estimation methods eq. 3, Table 2,
  Discussion.
- Pope et al. 2004, "Risk Adjustment of Medicare Capitation Payments Using the CMS-HCC Model", Health Care Financ Rev
  25(4):119-141, https://pmc.ncbi.nlm.nih.gov/articles/PMC4194896/: prospective timing, inputs, R2 for individuals and
  predictive ratios for groups, the base model's R2 of 1.69% against CMS-HCC's 9.8%.
- SOA, Hileman and Steele 2016, "Accuracy of Claims-Based Risk Scoring Models",
  https://www.soa.org/resources/research-reports/2016/2016-accuracy-claims-based-risk-scoring-models/: confirms that the
  risk-score comparisons report R2 and MAE. The PDF could not be parsed here, so no figures are quoted from it.
- Cameron and Trivedi data page, http://cameron.econ.ucdavis.edu/mmabook/mmadata.html: gives no price base and no
  codebook.
- Sibling record `curation/records/meps_total_healthcare_expenditure.md` (the same actor and the same approximate call
  for survey items).
- My checks (tail shares, ages, income, medians by year, plan means; on the 9 shipped splits raw and trimmed R2,
  predictive ratios, top-5% capture) and the builder's probes are in the run folder.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** The table is a faithful copy of the real RAND Health Insurance Experiment panel. The next-year spending target is built correctly and I found no leakage. But scores on the raw-dollar target depend on a few dozen catastrophic-cost rows per fold. Before this enters a benchmark, the target should be log-transformed (or scored with a deviance metric), the dataset renamed, families kept together in the split, and the leftover source imputations and integer codes cleaned up.

**What the task is**

The table holds one row per person-year from the RAND HIE fee-for-service sample (1974-1982, six US sites, people under 62). This is Cameron & Trivedi's `randdata.dta`, the extract used by Deb & Trivedi (2002). The features describe year t: that year's spending and visit counts by type, the randomly assigned plan (coinsurance 0-100%, individual deductible, maximum-dollar-expenditure offer, participation incentive), demographics, and baseline health indices. The target is the person's `meddol` in year t+1.

The use is real. An insurer or risk-adjustment analyst at the end of a year forecasts next-year cost per member from current claims and baseline health, for premium setting or care management. The setting is dated and stylised, though: a randomised experiment with extreme cost-sharing plans and a 1970s population, which limits how far results carry to a modern use.

**What I checked and found sound**

- *Real data, faithful copy.* I downloaded `randdata.dta` from the Cameron MMA page (20,190 rows, 45 columns) and parsed it with my own reader for the Stata 110 format. Merged on (person, year), all 14,214 prepared rows match the source. Income, age, spending components, visits, MHI, disease index, MDE, education and family size agree 100%.
- *Target construction is correct.* `medical_spending_next_year` equals next-year `meddol` for all 14,214 rows, and only consecutive years are used: the 12 source rows whose next record skips a year were excluded. Exactly 52 further candidate rows were dropped, and all 52 have `inpmis = 1` in the target year (missing inpatient charges). That is a sensible filter, but it is not documented. The row counts add up: 20,190 source rows minus the 5,912 last years, which have no next year, leaves 14,278 candidates = 14,214 kept + 52 dropped + 12 skipped-year rows.
- *No temporal leakage.* Plan, demographics and the health indices are constant within person (0% of persons vary), so they are baseline values. Utilisation, age and family size are year-t values. Nothing comes from year t+1. Grouping by person is the right regime, because a person's year-t+1 spending also appears as `medical_spending` in that person's next row. In practice the leak is small: log-target LightGBM R2 is 0.343 with random rows versus 0.335 with person groups.
- *Signal is present and the task is not trivial.* Spearman correlation between current and next-year spending is 0.51. LightGBM on log1p(target) under 3x3 person-grouped CV gets R2 0.342 +- 0.017. Without the current-year utilisation columns it drops to 0.203.
- *Size is adequate.* 14,214 rows, 5,638 persons, about 4,700 test rows per fold.
- *Duplicates are negligible.* One identical pair of rows (2 rows).

**Concerns, ranked**

1. **On the raw scale the target is so heavy-tailed that RMSE/R2 mostly scores a few dozen rows.**
   - *Evidence on the distribution:* 22.7% of targets are zero, the median is 34, the 99th percentile is 2,390, the 99.9th is 9,566 and the maximum is 39,182.
   - *Evidence on the score:* with a mean prediction, the top 1% of test rows (about 47 rows) produce 75-90% of test SSE (mean 83%).
   - *Model results on raw dollars:* ridge R2 0.085, ranging 0.040-0.135 across the 9 splits. LightGBM Tweedie gets 0.077 and a small L2 LightGBM 0.078. Default LightGBM (400 trees, 31 leaves) gets 0.022. The mean baseline has RMSE 726, against about 700 for the best model.
   - *Why it matters:* the spread between folds (about 0.03) is as large as the gaps between methods. Rankings would mostly reflect how each method treats a handful of hospitalisations, and heavy regularisation wins by default.
   - *Change:* use log1p(target), where R2 is about 0.34 with a fold standard deviation of about 0.017. Otherwise score with Poisson or Tweedie deviance. If raw dollars stay, flag the dataset as high-noise.

2. **The name does not match the target, and the task is the curator's own construction.**
   - *Evidence:* the dataset is called "doctor_visits", and the source's task is the visit count (statsmodels: "mdvis - Number of outpatient visits to an MD"). Here the target is next-year medical spending, made by shifting `meddol` forward one year.
   - *Change:* rename it (e.g. `rand_hie_next_year_medical_spending`). In `task.md`, document the shift, the consecutive-year rule and the `inpmis` filter. Also state the population limits: randomised plans, ages under 62 at enrollment, 1970s dollars. The source says only "constant dollars"; I could not confirm the base year.

3. **The split keeps persons together but not families.**
   - *Evidence:* the 5,638 persons form about 2,782 households. I identified them by matching site, plan, family income, decision-maker education, participation incentive and MDE; IDs are consecutive within these groups. 4,070 persons live in multi-person households. Household members share plan, income and the family-level out-of-pocket cap (MDE), and their spending is correlated.
   - *Measured effect is small:* log-scale R2 is 0.342 with person groups versus 0.329 with household groups. On the raw scale it is 0.022 versus 0.028, which is noise.
   - *Change:* group by household (derived as above, or from the ICPSR family ID). It is cheap and matches the deployment case of a new enrolling household better.

4. **Source imputations are handled inconsistently.**
   - *What was cleaned:* the fractional mean-imputed values of `black` (169 rows) and `physical_limitation` (616 rows) were correctly turned back into NaN.
   - *What was left:* `chronic_disease_index` still carries mean-imputed values for about 39% of persons. There are 14 distinct off-grid values, e.g. 10.576256 (685 persons), 13.731887 (612) and 9.967326 (559); real values lie on a 3.4-step grid. These are mostly children (mean age 14 versus 31). `mental_health_index` has about 18% imputed (6 values, e.g. 74.368256 for 375 persons), and `education_of_decision_maker` about 1% (e.g. 10.627741).
   - *Why it matters:* trees can treat these constants as missing codes, but linear and neural models are misled.
   - *Change:* set them to NaN, or add missing indicators, the same way as for `black` and `physical_limitation`. `general_health_index` is NaN for 26% of rows, which is the source's raw value, so that is fine.

5. **Some column types and roles need fixing.**
   - `plan` (18 nominal codes, 1-19) and `site` (6 codes) are stored as int64. They should be categorical.
   - `person_id` must not be used as a feature: its leading digit is the site and its numbers are consecutive within households. In my test it added nothing (0.343 versus 0.342).
   - Harmless redundancies: `medical_spending` is exactly outpatient + drug + supplies + inpatient (psychotherapy is excluded, as the source defines it). `coinsurance_rate` and `individual_deductible_plan` are fixed by `plan`.

6. **Exposure is not handled.** The source column `time` (fraction of the year eligible) was dropped. For 37 rows the target year is a partial year (`time < 1`), so the target is not annualised there. This is minor: drop those rows or annualise the target.

**What I could not check**

- The ICPSR 6439 codebook (the page returned 403), so I could not confirm the dollar base year or the exact imputation rules behind the off-grid values.
- A true family identifier. Households above are inferred from shared family-level fields.
- Which metric the benchmark will use. Concern 1 matters most if it is RMSE or R2 on raw dollars.
- Hyperparameter-tuned models. My numbers come from a few fixed configurations.

Sources: https://www.statsmodels.org/dev/datasets/generated/randhie.html ; http://cameron.econ.ucdavis.edu/mmabook/mmadata.html (randdata.dta) ; https://rdrr.io/rforge/sampleSelection2/man/RandHIE.html ; https://r-packages.io/datasets/randhealth ; https://www.rand.org/pubs/notes/N2360z1.html

</details>

<details><summary>Precedent check</summary>

**Precedent check (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Verdict:** most choices follow the precedents: the target, the rows, the cleaning, the metric, and the changes to the
markers. Three departures have no stated fact behind them: the missing `ForcedGroupedFromTemporal` tag (SPLIT-8), the
year and source against the SUPPORT2 extract (PROV-9), and cleaning around the extract without checking ICPSR 6439
first (PROV-13, which carries `family_income`, issue 4). Three departures do have a reason: families left ungrouped
(MEPS groups households), the target in dollars (the batch siblings log theirs), and the target year's eligible fraction
left out (fremtpl2 keeps `Exposure`). For the last one the reason is clear from the data but not written down. No drift,
no third exception. None of the register's 14 flags touches this dataset or its rules.

Read: the run's decision register (1,620 decisions), the Cases tables of use_case, splits, metrics, cleaning_features, leak_checks
and provenance, the records of [meps_total_healthcare_expenditure](../../../../curation/records/meps_total_healthcare_expenditure.md),
[health_insurance](../../../../curation/records/health_insurance.md), [fremtpl2](../../../../curation/records/fremtpl2.md)
and [2_month_survival_rate_prediction](../../../../curation/records/2_month_survival_rate_prediction.md) (SUPPORT2), the
policy calls of 2026-10-30 in [two_regime_zero_triage_summary.md](../../../../curation/inputs/two_regime_zero_triage_summary.md),
and this batch's sibling definitions (AI drafts, not decided: they count as like cases, not as precedents).

**Decisions of the definition**

| # | Decision | Rule | Closest precedents | Finding |
|---|---|---|---|---|
| 1 | Target: next-year `meddol` in dollars (changed from the screening's visits) | USE-5, USE-10 | MEPS (CC Andrej 2026-10-20, "Yes, as a prospective task": next-year TOTEXP from the year-1 columns); this record's CC 2026-10-30 ("Try to find a target") | consistent |
| 2 | Rows: year t paired with year t+1, first year never a target, 273 persons out | USE-3 | MEPS (persons in scope in both years); Newhouse et al., "Source of data" | consistent |
| 3 | All ages and non-completers kept, unlike the paper's cohort | USE-1 | MEPS notes keep "the persons who die in year 2" and all ages | departs from the source with a stated reason (a capitation covers children; requiring completion selects on the future); follows MEPS |
| 4 | Target year's eligible fraction not a feature; the 37 partial target years kept | LEAK-10; policy call 3 (exposure) | [fremtpl2](../../../../curation/records/fremtpl2.md) (CC Andrej 2026-10-20: `Exposure` a feature, "the contracted period is known at pricing (a mid-year cancellation also shortens it)"); MEPS (decedents kept) | departs from fremtpl2 for a reason the data shows but the notes do not state (measured below); write it into the bullet |
| 5 | 52 target years with `inpmis` = 1 dropped | CLEAN-11, first clause | ames_housing (Lennart 2026-10-21: De Cock's partial sales dropped with his words) | consistent. Not the same case as #4: here charges are missing; there a shorter year's spending is recorded in full |
| 6 | Grouped by person | SPLIT-3, USE-10, SPLIT-8 | MEPS (grouped, prior-year features as inputs); nba_players_2016_2019 and open_university_learning_analytics_dataset (Lennart 2026-10-21) | the regime is consistent; the tag is missing: **departure 1** |
| 7 | Families not held together | SPLIT-24, SPLIT-25 | MEPS (grouped by household, `DUID`); maternal_health_risk and hazelnut_spread_contaminant_detection (retired: the lost group was the only entity) | departs from MEPS with a stated reason: no family id, SPLIT-24 bars a guessed key, and a family proxy changes R^2 by 0.0013. The reason is only as strong as the proxy (1,603 persons alone), which is for the split auditor |
| 8 | Year t's visits, admissions and spending as features | USE-10, LEAK-10 | MEPS (all `Y1` columns, spending included) | consistent |
| 9 | Plan columns and the participation incentive kept; fit approximate | USE-1, USE-8 | MEPS (survey items a payer lacks kept, so the fit is approximate for payers); policy call 1 (Andrej 2026-10-30) | consistent |
| 10 | Derived copies and the constant `time` dropped | CLEAN-5, CLEAN-22 | none needed | consistent |
| 11 | `hlthg`/`hlthf`/`hlthp` merged with the reference level "excellent" | CLEAN-13 | mortgage, onlinenewspopularity (Lennart 2026-10-22) | consistent |
| 12 | Site-mean fills of `black` and `physlm` set missing; `xghindx` dropped | LEAK-30, CLEAN-2 | tension row "fix it when we can": sf_permit_time and home_credit fixed (Lennart 2026-10-19) | consistent |
| 13 | `disea` and `mhi` kept as shipped (issue 5) | LEAK-30, PROV-13 | bioresponse and the others kept with a note (LEAK-30 cases); SUPPORT2 (origin checked first) | the keep is consistent. The bullet carries `Anomaly:` where the house rule wants `Potential leak, kept on purpose:` (definitions.md, "Recording decisions"; 30 definitions use it), a wording fix. The origin was not checked: **departure 3** |
| 14 | `family_income` kept with no bullet (issue 4) | LEAK-10, PROV-13 | SUPPORT2's edu and income dropped as recorded after the prediction point (Lennart 2026-10-26); LEAK-10's late-pull clause (distribution_transformers: such values go when they may carry a gain; onlinenewspopularity: they stay with a note when the traceable part shows none) | open until the fact is settled (EV-1). Having no bullet departs from definitions.md ("one bullet per ... kept suspect"): **departure 3** |
| 15 | Site and plan codes kept without labels (issue 6) | CLEAN-12 | none needed | consistent as a keep; the labels sit at the origin: **departure 3** |
| 16 | `Metric.source("r2")` from Newhouse et al., eq. 3 | MET-5, MET-11 | forest_fires (the paper's one ranking criterion, 2026-10-21); porto_seguro (a metric equal by identity counts, 2026-10-21); mercedes_benz_greener_manufacturing (`r2`); policy call 3, "the source's metric first" (Andrej 2026-10-30) | consistent; it replaces the screening's fallback `rmse` (a later stage supersedes) |
| 17 | Target shipped in dollars, not logged | CLEAN-16 (Should, case by case), MET-3 | siblings ship log1p under rank or log-scale metrics ([frempl](../frempl_french_motor_personal_line/dataset.py), [wisconsin](../wisconsin_local_government_property_insurance_fund/dataset.py), both Spanish tables) | departs from the siblings with a stated reason: R^2 in dollars scores the mean, and a log fit needs retransformation. CLEAN-16 is case by case, so no exception is due |
| 18 | `year = "1995"`, `source_url` ICPSR 6439 | PROV-8, PROV-9 | SUPPORT2 (Lennart 2026-10-26: the extract's year); airfoil_self_noise and first_principles_tully_fisher (a copy takes the original's year) | departs from SUPPORT2 with no fact stated: **departure 2** |
| 19 | `"Spatial"` tag, domain, `source = "Other"` | definitions.md | many | consistent |
| 20 | `Two-Regime Zeros` (record tag) | policy call 4 (Andrej 2026-10-30) | the call named this record for a check of the count target | settled by the new target: 22.7% exact zeros in a continuous dollar target meet the definition |

Measured for #4: all 45 partial years are a person's last year on file.
The 37 that are targets fall in study year 2 (19), 3 (7), 4 (9) and 5 (2), so most come before the planned end of a 3- or
5-year term. They average $2,408 against $173 for full years: 3.5% of the target dollars and 5.6% of SS_tot from 0.26%
of the rows. The shortened year moves with the outcome, so the eligible fraction cannot be read as a period known when
the payment is set. That fact sets this case apart from fremtpl2.

**The builder's draft recommendations**

| Issue | Recommendation | Precedents | Finding |
|---|---|---|---|
| 1 | Rename (`doctor_visits` → spending) | records.md: "Renaming breaks links and review marks, so names stay"; ames_housing (new record under the new name, the old one keeps its links; Lennart 2026-10-26); mic_duplicate (renamed in place; Lennart 2026-10-26) | departs from the house rule with a reason (no review marks yet). The curator has renamed both ways. Mildest option: change the record's `name` title and keep `unique_name` |
| 2 | Remove `No Good Target / Scientific Discovery`, keep `Outdated`; weighing call against MEPS | policy call 1 (Andrej 2026-10-30: "if a dataset is useful for a predictive application although the data was collected for something else, then this is fine"); P3 informs P2 (Lennart 2026-10-15); health_insurance (`No`, no predictive task); 12 `Yes` records carry `Outdated` (heart_disease_cleveland, 2_month_survival_rate_prediction, ...); adult and census_income are `No` on SEL-3, with Folktables named only for `Outdated` | consistent. What sets this dataset apart from health_insurance is that Newhouse et al. 1989 predict annual spending for capitation. No precedent excludes a dataset only because a modern counterpart exists, so MEPS is a weighing factor |
| 3 | Grouped as it stands, or `ForcedGroupedFromTemporal` | see #6 | **departure 1** |
| 4-6 | `family_income`, `disea`/`mhi`, labels | see #13-15 | **departure 3** |

**Departures without a stated fact (by rank)**

1. **SPLIT-8 (P4, Must): the tag.**

   **Consistency check (AI, 2026-11-01):** the definition ships grouped by person without `ForcedGroupedFromTemporal`.
   Its own `fit_reason` calls the task a next-year prediction whose calibration-to-use drift cannot be tested ("no
   calendar years"). SPLIT-8 covers "a release with no dates at all" and tags such a task. nba_players_2016_2019 and
   open_university_learning_analytics_dataset (Lennart, 2026-10-21) carry the tag for stacked periods of recurring
   entities, and so do three siblings in this batch (frempl_french_motor_personal_line, pricing_game_2017_french_mtpl,
   spanish_motor_insurance_coverage_level_2022_2024). MEPS (Andrej, 2026-10-20) has the same design and has no tag
   decision yet. What sets this dataset apart?
   (a) The use case is a cold start for the model: a formula calibrated on one population is applied to enrollees
   outside it, so the task is grouped by nature and the year-to-year drift is only a fit gap. Recorded as the fact,
   with USE-10's "known entity: the split is temporal" answered in the notes.
   (b) Treat it like the SPLIT-8 cases: add the tag, keep the folds, and say a dated window would test the drift and
   should be recovered (calendar years may follow from the site enrolment dates or from ICPSR 6439).
   (c) Reopen the SPLIT-8 cases to match this one.
   (d) Amend SPLIT-8: no tag when the use case makes the test entities new, even if the prediction is for a later
   period.
   Whichever answer you give, carry it to MEPS when it is built.

2. **PROV-9 (P5, Must): year and source.**

   **Consistency check (AI, 2026-11-01):** `year = "1995"` and `source_url` take ICPSR 6439 as the first publication,
   while every shipped value comes from Cameron and Trivedi's `randdata.dta`. That file has its own site-mean fills,
   derived columns and a non-integer `disea`. For SUPPORT2 (2_month_survival_rate_prediction, Lennart, 2026-10-26)
   the year is the extract's (2003), because "ICPSR 2957 V1 ... holds the study data in another form ..., so it does
   not hold every value we ship". What sets this dataset apart?
   (a) ICPSR 6439's public-use files hold the person-year values we ship: the extract only cut rows and added the
   columns we drop or undo. Then the extract is a copy and 1995 stands. Checking the ICPSR file list or codebook
   settles it.
   (b) Treat it like SUPPORT2: use the year the extract was first published (Cameron and Trivedi's data page, 2005,
   or Deb and Trivedi 2002 if the file came out with that paper), set `source_url` to the data page, and keep ICPSR
   as the second citation.
   (c) Reopen SUPPORT2.
   (d) Amend PROV-9.

3. **PROV-13 (P5, Must), with LEAK-10 for `family_income`: the origin before cleaning around the extract (issues 4-6).**

   **Consistency check (AI, 2026-11-01):** the definition works around the extract's problems on its own reading. It
   undoes the fills, keeps `disea` and `mhi` as possible fills, keeps `family_income` without knowing whether it
   averages later study years (and with no bullet), and keeps site and plan unlabeled. It names ICPSR 6439 as the
   origin but does not say whether anyone checked it. PROV-13 asks for the origin first. For SUPPORT2 the curator
   downloaded ICPSR 2957 with a login (Lennart, 2026-10-12), and the fix took only the placement of values from it.
   What sets this case apart?
   (a) No one can reach the origin in this run (ICPSR login), and the stakes are small: the fills are undone,
   `disea`/`mhi` is a weak LEAK-30 at most, and income is constant per person. Then keep with `Potential leak, kept on
   purpose:` bullets for `disea`/`mhi` and `family_income` and a revisit condition. The tension row allows this only
   when the origin cannot be reached.
   (b) Treat it like SUPPORT2: you fetch ICPSR 6439's codebook (the files if needed). It settles the income timing,
   the `disea`/`mhi` construction and the labels before shipping. If income turns out to include later years, it goes,
   as SUPPORT2's income did.
   (c) Reopen SUPPORT2.
   (d) Amend PROV-13.

**Drift, third exceptions, register**

- Drift: none. Andrej's related calls agree with each other: fremtpl2 and MEPS on 2026-10-20, this record's CC and the
  policy calls on 2026-10-30. The AI's drift (screening `rmse` against builder `r2`; the record's older "Same call as
  `health_insurance`") is an earlier stage superseded by a later reading. The review's Assessment line should say so.
- Third exception: none is due. This definition records no exception. CLEAN-16 is case by case, and #3, #4 and #7
  rest on facts, not on exceptions.
- Register: none of the 14 flags concerns this dataset or the rules above. Tooling note: the register lists CLEAN-11
  and CLEAN-14 as "not defined in the knowledge files". Both exist in cleaning_features.md, but their headers carry
  long amendment notes. As a result the CLEAN-11 precedents used in #5 (ames_housing, mercedes_benz, qsar_tid_11) show
  up only under that heading.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Position: ship after changes.** The dataset ships the task that Newhouse et al. (1989) defined on these data, and
the definition builds it correctly. No evidence agent found a leak, a wrong target or a split that tests the wrong
thing. Every real problem they found is fixed in the definition or its text, and no fix moves the score by more than
0.002 R2. Nothing calls for the last rung of the remedy ladder.

```text
Verdict: ship after changes.
Validity: USE-1, USE-2, USE-5 hold (the source paper's own target); LEAK-10 holds for 29 of 30 features, open and weak
  for `family_income` (dropping it moves R2 by 0.0004 at most); SPLIT-29 holds against IID; SPLIT-8 triggered, fixed by
  the tag and a splits_comment (cost measured: none); SPLIT-24 text refuted, effect nil; PROV-9 a metadata fix;
  PROV-13 origin unreachable in this run, the fills undone from the data.
Value: TP-4 and TP-10 pass; MET-1, MET-3 and MET-5 hold (`r2` in dollars, the paper's eq. 3).
Quality: CLEAN-10 fills left in three columns (cheap fix); several notes to correct.
Weighed: source +, use case + (named by the source), shape +, age -, MEPS sibling -.
```

**1. The task is the source's own prediction, so the record's `No Good Target / Scientific Discovery` falls (P3).**

- Claim: next-year medical spending per person-year is a real payer decision, and the one the source paper made.
- Evidence:
  - Newhouse, Manning, Keeler and Sloss 1989 used the HIE data "to estimate or predict annual expenditures for
    medical care services in constant dollars", with the person-year as the unit, to adjust Medicare's per-enrollee
    payment (claim auditor #4, #38; the paper's text, lines 965, 1006, 1010).
  - The target is `meddol` of year t+1, the paper's dependent variable. It equals the sum of its four parts in 20,188
    of 20,190 rows (#3). As in the paper, the first year is never a target.
  - The blind reviewer, from the table alone, named the same actor: "an insurer or risk-adjustment analyst at the end
    of a year forecasts next-year cost per member". The domain practitioner agrees with `fit="approximate"`.
  - The curator's CC (2026-10-30) set the test: "Try to find a target and if not we can still reject it". The target
    found is the source's, not one we made up.
  - The columns a payer lacks (survey health, income, incentive) do not inflate the task. A ridge on six payer inputs
    scores 0.090, the same as all 30 features (domain practitioner).
- Rule: USE-1, USE-2, USE-5 (Must); USE-6 (Must) keeps every input known at the prediction point.
- Why it outranks the objection: the marker is an AI screening reading, and a later stage's measured finding
  supersedes it (Precedence, Stages). The paper sets this case apart from `health_insurance` (No), and policy call 1
  (Andrej, 2026-10-30) reads SEL-2 the same way.
- Fix that keeps it:
  - drop the marker and add an Assessment line;
  - name the missing claims diagnoses and welfare flag in `fit_reason`;
  - drop the "care manager ... high spenders" clause, which `r2` does not score (MET-1).

**2. No leak: every feature exists at the end of year t, and the one open column costs nothing either way (P4).**

- Evidence:
  - Column auditor: LEAK-10 holds for 29 of 30 features. The health columns read "-- baseline" in the file and
    "collected at entry into the study" in the paper. The target year's other outcomes and its eligible fraction are
    left out.
  - The blind reviewer rebuilt the target with its own reader: all 14,214 rows match, and nothing comes from year t+1.
  - Claim auditor #31: only `meddol` and `inpmis` of t+1 are merged, and both leave the features. #30: no exact
    copies across the split.
  - `family_income` (label cut off, constant per person) is the only open column. Alone it scores R2 -0.033.
    Dropping it moves HGB from 0.0737 to 0.0735 and RF from 0.0819 to 0.0823. An average over the person's own
    years is ruled out: 4,031 of 4,053 family-member pairs share it, 241 of 248 with different years on file.
- Rule: LEAK-10 (Must) with its late-pull clause (case by case); USE-12 (Must): a leak is no reason to reject a task
  whose use case is real.
- Fix that keeps it: the ICPSR 6439 codebook settles it (the repair rung). Without the codebook, drop the column (the
  definition rung): it costs nothing and the doubt goes with it.

**3. The split tests the use case; the two text errors are fixed in the text (P4).**

- Evidence that grouping is right:
  - Under random rows a feature lookup scores R2 0.372, against 0.089 for RF (split auditor).
  - No person sits on both sides in any of the 9 splits.
  - Dropping `study_year` moves R2 by -0.0005 and +0.0004, so there is no SPLIT-9 shortcut.
- Conceded, SPLIT-8: the use case is next-year, and the release has only study years. Only two windows meet the 50%
  floor (target year 3 trains on 38.4%). The forced grouped split is no more optimistic than the valid windows
  (RF / ridge):

  | test rows | temporal window | shipped person folds |
  |---|---|---|
  | target year 4 | 0.147 / 0.129 | 0.135 / 0.135 |
  | target year 5 | 0.112 / 0.113 | 0.098 / 0.103 |

  The facts match frempl, pricing_game_2017, spanish_motor_2022_2024 and allstate_1m in this batch, and nba and
  open_university (Lennart, 2026-10-21). All of them carry the tag.
- Conceded, SPLIT-24 text: a family can be rebuilt exactly (consecutive `zper` with identical site, plan and income;
  2,355 families in the shipped rows). 75.7% of test rows have a family member in training. The effect is nil:
  - family groups RF 0.0835, ridge 0.0787, against person groups 0.0821 and 0.0794 (SE about 0.007);
  - a family-target feature adds +0.0002;
  - the claim auditor's coarse keys agree (0.0857-0.0897 against 0.0859).
- Rule: SPLIT-8 (Must) asks for a tag and a cost statement, not another split. SPLIT-4 and SPLIT-30 (Must): the gap
  never decides. SPLIT-24 (Must) allows the rebuilt key.
- Fix that keeps it:
  - add `ForcedGroupedFromTemporal` and a `splits_comment` with the window numbers, saying that a release with
    calendar years should get a temporal split;
  - then either rewrite the family sentences or group on the rebuilt family id (a grouping column only). Regrouping
    follows SPLIT-4 more closely and costs nothing measured. The text fix alone is enough if the curator distrusts a
    key no codebook confirms.

**4. The data are a faithful copy; the provenance questions are metadata and a codebook check (P5).**

- Evidence:
  - The sha256 is pinned.
  - The format-110 patch equals statsmodels' independent conversion in 20,190 of 20,190 rows (claim auditor #2).
  - The blind reviewer's own reader matched every shipped column in 100% of rows.
  - The dropped columns are true copies, or functions of `plan`, which ships (#20).
- Conceded, PROV-9: like SUPPORT2, the year and `source_url` should be the extract's (Cameron and Trivedi's data page,
  2005, or Deb and Trivedi 2002 if the file came with that paper), with ICPSR 6439 as the second citation. That holds
  unless the ICPSR files turn out to hold the same values. The task does not change.
- PROV-13: ICPSR 6439 returned 403 to two agents. The damage found is site-mean fills. The data identify them, and
  the definition can set them to missing (point 6). Their measured effect is under 0.001. The tension row "repair
  against cleaning around damage" allows a keep with a note when the origin cannot be reached. If the curator can log
  in, as for SUPPORT2, the one codebook settles income, the fills and the plan labels.
- Rule: PROV-9, PROV-13 (Must). Both are met by a field change and a check. Neither leaves an unfixable Must, which is
  the only ground for exclusion (remedy ladder).

**5. Worth benchmarking, scored by the source's metric on the source's scale (P6).**

- Evidence:
  - It reproduces the paper. RF scores 0.093 and linear 0.084, against the paper's about 9% (62% of a 14.5% maximum).
    Without this year's use, RF scores 0.039, against the paper's 2.8-4.6%.
  - It is not trivial: prior spending alone scores 0.038, and the naive last value -0.427 (claim auditor #32).
  - It is large enough: 14,214 rows, 1,879-1,880 persons per test fold, and the dummy within 0.002 of 0 on every fold
    (#23).
  - The metric is the paper's own. Efron's R2 is its single ranking criterion (eq. 3; a trimmed variant was computed
    and not shown), and the paper's share of the maximum rises with R2 (#22).
  - Dollars are the right scale: a capitation pays the conditional mean, which squared error targets. MAE would
    target the median (about $35, against a mean of $178) and underpay by about 80% (domain practitioner). Policy call
    3 (Andrej, 2026-10-30): "the source's metric first".
- Against the blind reviewer's log target: log1p R2 of 0.34 scores a quantity no capitation pays. MET-3 lets a target
  ship as log1p only with the metric still computed in dollars, so a log target would not remove the tail. The tail
  is part of the task: the ridge-against-RF ranking flips on 0 of 9 folds when the largest row is removed (#24).
- Rule: MET-1 and MET-3 (Must) and MET-5 (Should) outrank CLEAN-16 (Should, case by case, P7) and MET-10 (Weigh).
  TP-2: a small real signal is no reason to retire.
- Conceded: the folds vary a lot. One $39,182 row holds 40-56% of its fold's SS_tot, and the three lowest fold scores
  are the three folds that hold it. Fix: put that number in the existing note.

**6. The cleaning gaps are cheap, safe and half done already (P7).**

- Evidence:
  - `disea`, `mhi` and `educdec` hold site-mean fills: 2,072 of the 2,074 children for `disea`, 39.4% of rows. It is
    the mechanism the definition already undoes for `black` and `physlm`.
  - Setting the fills to missing moves R2 by +0.0009, -0.0001 and +0.0005 (column auditor), and by -0.0005 and
    -0.0007 (claim auditor). The column auditor wrote the six-line block.
  - `self_rated_health` = "excellent" absorbs "not asked" for 346 children; those become missing.
- Notes to correct:
  - the `coinsurance_rate` coding (plan 13 is coded 0 and plans 2-4 are coded 100; `plan` ships);
  - the DERIVED comments for `logc` and `fmde`;
  - "lacks part of its inpatient charges";
  - the 37 partial target years, which hold 5.6% of SS_tot;
  - the MHI instrument switch at age 14.
- Rule: CLEAN-10 (Should); LEAK-30 weak (Should); treat like cases alike. Principles step 3: a quality problem is
  fixed when the fix is cheap and safe.
- Why it outranks the objection: P7 never removes a real task (tension row P3 over P7, churn_telco_south_asia).
- Rename: `doctor_visits` is wrong for a spending target. records.md keeps names stable, but this dataset is unbuilt,
  with no UUID and no review marks, so a rename costs least now (mic_duplicate was renamed in place). That is the
  curator's call; the fallback is to change the record's title.

**7. Age and the MEPS sibling are weighing factors, and they do not outweigh what this dataset adds (weighed).**

- Evidence:
  - `Outdated` has no rule behind it (the marker table in selection.md lists "none"). Twelve `Yes` records carry it,
    among them heart_disease_cleveland and 2_month_survival_rate_prediction.
  - No precedent excludes a dataset only because a modern counterpart exists (precedent checker). MEPS is other data,
    so this is no duplicate (PROV-7).
  - What this dataset adds:
    - a published prediction to reproduce, whose levels it matches;
    - randomised cost sharing;
    - a person-year panel with prior spending;
    - 22.7% exact zeros under a heavy tail (`Two-Regime Zeros` under policy call 4).
  - The domain practitioner would use it "to compare methods on the problem I face every year": a year-to-year
    correlation of 0.19 and a low ceiling.
- Rule: Weigh; "no factor decides alone" (principles, Strengths). `fit="approximate"` (USE-8) already names the era.
- Weighed: source + (ICPSR and the paper), use case + (named by the source), shape + (5,638 persons), gap 0
  (medical), age -, sibling -.

</details>

<details><summary>Critic</summary>

**Critic, opening brief (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Position: do not ship as defined. Ship after the changes below.** I ask for no exclusion: no point is a Must that
cannot be fixed. The task is real (Newhouse et al. 1989 predict next-year spending for capitation), the target and
prediction point hold, and no leak was measured. What fails:

- what the dataset says about itself: name, use case, fit and record;
- two Must rules of the split: the SPLIT-8 tag, and a family claim the data refutes;
- one Must leak question left open: `family_income`;
- the origin check, PROV-13 and PROV-9.

Quality comes last and is no reason to hold the task back.

```text
Verdict (critic): ship after changes.
Validity: USE-5, USE-8, MET-1 triggered, text fixes (1); SPLIT-8 triggered, tag + splits_comment (2); SPLIT-24 with
  SPLIT-4: the family claim is refuted, group on families or correct the text (3); LEAK-10 open for family_income:
  settle it or drop the column (4); PROV-13 and PROV-9: origin not checked (5).
Value: TP-2, TP-4, TP-10 and MET-5 hold (not disputed).
Quality: CLEAN-10 with weak LEAK-30: site fills kept in three columns (6); CLEAN-12 and wrong statements in the notes (7).
For the curator: rename (1), SPLIT-8 consistency (2), family grouping (3), an ICPSR login (4, 5).
```

**1. P3, USE-5, USE-8 and MET-1 (Must): the dataset describes another task than the one it ships and scores.**

- *Problem.* There are four mismatches:
  - (a) `unique_name` and the record title say "doctor visits", but the target is next-year medical spending, and
    the visit count is only a feature.
  - (b) The use case adds a second decision: "An HMO or care manager can use the same prediction to plan for its high
    spenders". That is a top-k choice, and `r2` does not score it.
  - (c) `fit_reason` leaves out the largest gap. The data has no claims diagnoses and no welfare flag. Every
    prospective payment formula uses diagnoses (CMS-HCC), and welfare status was one of the AAPCC adjusters in the
    paper.
  - (d) The record still carries `No Good Target / Scientific Discovery` and the screening line "Metric: ... fallback
    `rmse`". Both are refuted.
- *Effect.* A user looking for a count task gets a dollar target. The benchmark claims to score a care-management
  decision that it does not score. The fit reads closer than it is: a ridge on six inputs (age, sex, site and three
  spending columns) scores 0.090 ± 0.037, the same as on all 30 features (0.090 ± 0.039). The task as shipped is the
  paper's "AAPCC plus prior use".
- *Evidence.* Claim audit, rows 37-39; domain practitioner sections 2 and 5 and gap 2; builder issue 1.
- *Rules.* USE-5 (Must): the target as named. MET-1 (Must): the declared metric scores the use case's decision.
  USE-8 (Must): the fit names its known gap. USE-2: the marker.
- *Remedy (text only).*
  - Rename now (e.g. `rand_health_insurance_experiment_medical_spending`), while the dataset is unbuilt and has no
    UUID or review marks. The milder option is to retitle the record and keep `unique_name` (records.md: "names
    stay"; the curator has done both, ames_housing and mic_duplicate).
  - Drop the care-manager sentence.
  - Add "no claims diagnoses or welfare status" to `fit_reason`.
  - Add an Assessment line that drops the marker and supersedes the screening's metric line.

**2. P4, SPLIT-8 (Must; narrows USE-10): the task is temporal by its use case, and it ships grouped without the tag or
the cost.**

- *Problem.* The payer fits the formula on past years and applies it to next year. The definition's own `fit_reason`
  says "the drift between calibrating a formula and using it is not tested". The study years give only two windows
  above the SPLIT-14 floor:

  | test window | share of rows in train |
  |---|---|
  | target year 3 | 38.4% (below the floor) |
  | target year 4 | 76.4% |
  | target year 5 | 88.2% |

  That is SPLIT-8's case "too few periods for three windows ... stacked and grouped by the entity".
- *Effect.* A reader takes the split for a pure cold start. The time side goes unstated. The mean target rises from
  $170 to $209 by target year, and the p99 rises from $2,230 to $2,904; the person split cannot test this.
- *Evidence.*
  - Split audit, problem 1. On target year 4, RF scores 0.147 on the temporal window and 0.135 on the person folds;
    on year 5, 0.112 and 0.098. So the forced split is no more optimistic.
  - Claim audit, row 29: training on later study years adds RF +0.0001 ± 0.0025.
  - Precedent check, departure 1.
- *Precedents.*
  - Four siblings in this batch, on the same reasoning: frempl_french_motor_personal_line,
    pricing_game_2017_french_mtpl, spanish_motor_insurance_coverage_level_2022_2024 and
    allstate_claim_prediction_challenge_1m.
  - nba_players_2016_2019 and open_university_learning_analytics_dataset (Lennart, 2026-10-21).
- *Remedy (no re-split).*
  - Add `ForcedGroupedFromTemporal` to `data_tags`.
  - Write a `splits_comment` with the two windows and their scores.
  - Say that a release with calendar years (ICPSR 6439, or the sites' start dates) should get a temporal split.
  - The only alternative is a recorded fact that sets this case apart (the precedent check's option a). The same
    answer then has to apply to MEPS.

**3. P4, SPLIT-24 (Must) with SPLIT-4 (Must): "families cannot be held together" is refuted.**

- *Problem.* `task_summary.split` and `grouping.definition` say the extract cannot rebuild families. The builder's key
  failed because it included `educdec`, which varies within families. A key of the form SPLIT-24 names (consecutive
  blocks with identical values) does rebuild them: consecutive `zper` with identical site, plan and family income.
  - The split audit counts 2,523 families in the raw file and 2,355 in the shipped rows.
  - My recount in `zper` order finds 2,422 families. 72% of them match the family
    size; 9 exceed it.
  - Income takes 1,703 distinct values over 5,912 persons, so a chance match is unlikely.
- *Effect.*
  - 75.7% of the test rows have a family member on the training side.
  - The correlation of log1p mean spending is 0.315 between family members, against 0.056 between persons of the
    same site and plan in other families.
  - New enrollees join as family contracts, so the test persons are not new in the way the use case says.
  - The measured score effect is nil: RF scores 0.0835 on family groups against 0.0821 on person groups, and a
    family-target feature adds +0.0002.
- *Evidence.* Split audit, problem 2; blind review, concern 3 (a different key finds about 2,782 households).
- *Precedent.* meps_total_healthcare_expenditure groups by household (`DUID`).
- *Rules.* SPLIT-24 allows this key. SPLIT-4: the split follows the application, not the size of the gap. The
  definition states a fact that is false.
- *Remedy.*
  - Group on the rebuilt family id, as a grouping-only column and never a feature. It costs nothing measurable and
    matches MEPS.
  - If the curator distrusts a key that has not been checked against a codebook, the minimum is to rewrite both
    sentences with the measured facts.

**4. P4, LEAK-10 (Must, unverified): `family_income` may average later years, and the definition says nothing about
it.**

- *Evidence.*
  - The value is the same in all of a person's 3-5 years, and the label is cut off ("income based on annual income
    r…").
  - It is not the enrolment income the out-of-pocket cap was set from. The median cap/income ratio per plan ranges
    from 0.043 to 0.186, and only 0-23% of a plan's persons lie within 1% of it (column audit, problem 1).
  - It is set per family, not per person (claim audit, U1). So it may be a family average over the study years, the
    target years included.
  - A payer does not hold it (domain practitioner, section 1).
  - Dropping it moves HGB from 0.0737 to 0.0735 and RF from 0.0819 to 0.0823.
  - The definition has no bullet on it (precedent check, row 14; definitions.md: one bullet per kept suspect).
- *Rule.* LEAK-10 (Must), the late-pull clause. A value whose late cells cannot be located stays with a note only
  when the part that can be traced shows no gain. Here no part can be traced, and "a 'removing it changes no score'
  test alone is still no reason to keep".
- *Precedent.* SUPPORT2's income was dropped as recorded after the prediction point (Lennart, 2026-10-26).
- *Remedy.* Settle it from the ICPSR 6439 codebook (point 5). Until then, drop the column: there is no measured cost,
  and a payer does not have it. If the curator keeps it, add a `Potential leak, kept on purpose:` bullet with these
  numbers.

**5. P5, PROV-13 and PROV-9 (Must): the definition cleans around the extract without checking the origin it names,
and dates the data by that origin.**

- *Problem.* `source_url` and `year = "1995"` name ICPSR 6439, yet every shipped value comes from Cameron and
  Trivedi's `randdata.dta`. That extract has damage of its own:
  - site-mean fills: undone in `black` and `physlm`, dropped with `xghindx`, still shipped in `disea`, `mhi` and
    `educdec`;
  - derived columns;
  - a coinsurance coding that disagrees with its own `logc` and `fmde`;
  - labels cut off at 32 characters.

  No one checked ICPSR (the agents got 403), and the notes do not say so.
- *Effect.* Four questions are open only because the origin was not read: the income timing (point 4), the fill
  rules (point 6), the plan and site labels with the coinsurance coding (point 7), and the price base.
- *Evidence.* Precedent check, departures 2 and 3; claim audit, row 34.
- *Precedent.* SUPPORT2. The curator downloaded ICPSR 2957 with a login (Lennart, 2026-10-12). The year became the
  extract's (2003), because ICPSR "does not hold every value we ship" (Lennart, 2026-10-26). While the
  `disea`/`mhi`/`educdec` fills ship, the same is true here.
- *Tension row.* Repair from the origin first; keep with a note only when the origin cannot be reached.
- *Remedy.* The curator fetches the ICPSR 6439 codebook. Then one of two:
  - the shipped values are in ICPSR: 1995 stands, and the download notes say so;
  - they are not: `year` becomes the extract's first publication, `source_url` its data page, and ICPSR the second
    citation.

  If ICPSR cannot be reached, add one bullet saying the origin was not checked and why.

**6. P7, CLEAN-10 with weak LEAK-30 (Should): the extract's fills are undone in two columns and kept in three, and the
note says the data cannot settle what it does settle.**

- *Evidence.*
  - `disea`: one constant per site group for 2,072 of the 2,074 children, and for 315 adults (mostly site-1 adults
    without the baseline physical). That is 39.4% of the rows.
  - `mhi`: four constants for 1,133 persons, 17.5% of the rows.
  - `educdec`: five per-site constants, 157 rows.
  - Each constant lies within 0.03-0.33 of its site group's observed mean. That is the mechanism Decision 1 undoes
    for `black`.
  - `self_rated_health`: "excellent" also means "not asked". 346 of the 371 children with a filled `physlm` read
    excellent (93%, against 64.8% for the other children).
  - The fix has no effect on the score: R2 moves by +0.0009 (HGB), -0.0001 (ridge) and +0.0005 (RF).
  - Sources: column audit, problems 2 and 3; claim audit, row 15.
- *Rules.* CLEAN-10 (Should). Treat like cases alike within one definition (principles). EV-2: a measurement
  outranks "the documentation does not settle it". LEAK-30 (Should when weak).
- *Remedy.*
  - Add the column auditor's `FILLS` block to `_clean`, extend Decision 1 and rewrite the "Anomaly" bullet with the
    measured fact.
  - Set `self_rated_health` to missing for those 346 children, or note it.
  - The fix is cheap and safe, so it is due (principles, step 3). It is not a reason to hold the task back.

**7. P7, CLEAN-12 and the accuracy of the notes (Should): statements the data contradicts.**

- *Coinsurance.* Plan 13 (the individual deductible plan, 2,591 shipped rows) is coded 0, but the file's own `logc`
  and `fmde` code it 95%. Plans 2-4 (785 rows) are coded 100, but `logc` codes them 0; I confirmed both by plan. The
  note "a payer knows ... coinsurance" takes the column at face value. The DERIVED comments for `logc` and `fmde` are
  wrong for 4,855 and 3,779 raw rows (claim audit, rows 20-21).
- *Missing charges.* "The recorded spending lacks its charges": 68 of the 80 such years have `inpdol` > 0, so it lacks
  part of them (claim audit, row 6).
- *Partial years.* The 37 partial target years carry 5.6% of SS_tot (mean $2,408 against $172), and the notes do not
  say so. The reason the eligible fraction is not a feature is not written either: it moves with the outcome, which
  sets this case apart from fremtpl2 (precedent check, row 4).
- *Heavy tail.* One target ($39,182) holds 40-56% of its fold's SS_tot. The note could give the number.
- *Remedy.* Correct the text, and add a note that `plan` is the reliable plan identity and `coinsurance_rate` follows
  the file's coding.

**Considered and not pressed (no rule or evidence carries them)**

- *Score log R2 or a deviance instead (blind review, concern 1).* This goes against MET-3 (Must: score on the
  task's scale, here dollars) and MET-5 (the source's one criterion). A capitation pays the mean. Ranking ridge
  against RF flips on 0 of 9 folds when the top row is left out (claim audit, row 24).
- *`Outdated` against MEPS.* No rule or precedent excludes a dataset because a modern counterpart exists, and 12 `Yes`
  records carry `Outdated`. The curator said `Yes` knowing MEPS. This is a priority factor only.
- *`plan` and `site` stored as int64 (blind review, concern 5).* Wrong: `_feature_types` declares both categorical,
  and the README shows `category`.
- *Annualise or drop the 37 partial years (blind review).* CLEAN-11 removes a row only when the source says its target
  is not the task's quantity, and a payer bears these costs. A note is enough (point 7).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Position after the critic's brief: ship after changes.** The critic asks for no exclusion and does not dispute
value (TP-2, TP-4, TP-10, MET-5). I concede all seven points. I narrow two of them (1 and 5). On point 3 I ran a
check, and it moves me from "either fix" to the critic's remedy. The two briefs now differ on no remedy.

**1. Name, use case, fit and record (USE-5, USE-8, MET-1): conceded, narrowed.**

- Conceded:
  - (a) The name says visits, while the target is spending.
  - (b) The care-manager clause names a top-k decision that `r2` does not score.
  - (c) `fit_reason` leaves out the missing claims diagnoses and welfare flag.
  - (d) The record's marker and its "fallback `rmse`" line are refuted.
- Narrowed: the task itself is described correctly. `question`, `predicted` and the metric all say next-year
  spending in dollars. The six-input ridge (0.090, the same as all 30 features) shows that the shipped task is "AAPCC
  plus prior use". That is the specification the paper itself tests, so the fit stays approximate (USE-8) and its
  gap gets named. It is no reason to call the fit "None" (USE-2).
- Remedy: as the critic asks. I support renaming now, while the dataset has no UUID and no review marks; that is the
  curator's call under records.md.

**2. SPLIT-8 tag and cost (Must): conceded.** Add `ForcedGroupedFromTemporal` and a `splits_comment` with the two
windows. On target year 4, RF / ridge score 0.147 / 0.129 on the temporal window and 0.135 / 0.135 on the person
folds; on year 5, 0.112 / 0.113 and 0.098 / 0.103. The comment should also say that calendar years would call for a
temporal split. Treat like cases alike: frempl, pricing_game_2017, spanish_motor_2022_2024, allstate_1m, nba and
open_university are all tagged.

**3. Families (SPLIT-24 with SPLIT-4, Must): conceded. Group on the rebuilt family.**

- My check tested whether the key is exact enough to group on.
- It nests persons. Site, plan, income, `mdeoff` and `pioff` take one value per person in all 5,912 persons, so no
  person is split across families.
- Columns outside the key confirm it. Within multi-person families:
  - `mdeoff` is constant in 99.7-99.8% of them;
  - `pioff` in 99.5-99.6%;
  - the first-year family size in 99.2-99.4%.
- The two variants are compatible:
  - The split auditor's key (consecutive ids) gives 2,523 families. The critic's key (runs in `zper` order) gives
    2,422.
  - Every family of the first lies inside one family of the second. They differ only for 358 persons in 92 families.
  - The largest group has 10 or 11 persons.
- What follows:
  - Group on the critic's coarser key, which holds both readings together. The score cost is nil: RF 0.0835 against
    0.0821.
  - Build the key in `_clean` from the raw income before the income column is dropped (point 4). A grouping column is
    not a feature (LEAK-33), so the two fixes do not conflict.
  - Rewrite `task_summary.split` and `grouping.definition` to match.

**4. `family_income` (LEAK-10, Must, unverified): conceded.** The critic reads the late-pull clause correctly. A keep
with a note needs a traceable part that shows no gain, and no part of this column can be traced. "A 'removing it
changes no score' test alone is still no reason to keep." Drop it until the ICPSR codebook settles it. My opening
brief already preferred the drop.

**5. Origin (PROV-13, PROV-9, Must): conceded, narrowed.**

- Conceded: no one read ICPSR 6439, and the notes do not say so. SUPPORT2 is the like case for the year.
- Narrowed: the check needs a login that only the curator has, since two agents got 403. If the curator cannot log
  in, the tension row allows a keep with one bullet saying the origin was not checked and why. Nothing fixed in the
  definition waits on the login.

**6. Fills in `disea`, `mhi` and `educdec`; "excellent" for children never asked (CLEAN-10, LEAK-30 weak): conceded.**
Apply the column auditor's `FILLS` block, extend Decision 1 and rewrite the "Anomaly" bullet with the measured fact.
Set `self_rated_health` to missing for the 346 children. The score effect is under 0.001.

**7. Notes the data contradict (CLEAN-12): conceded.** Correct four things:

- the coinsurance coding note (`plan` is the identity);
- the DERIVED comments for `logc` and `fmde`;
- "lacks part of its inpatient charges";
- the heavy-tail number.

Also write down why the eligible fraction is not a feature. It moves with the outcome: all 45 partial years are a
person's last year on file, and 19 of the 37 partial targets fall before the planned end. That is the fact that sets
this case apart from fremtpl2.

**"Considered and not pressed": agreed on all four.** No log target or deviance (MET-3, MET-5). `Outdated` and MEPS
are a priority factor only. `plan` and `site` are already categorical. The 37 partial years stay, with a note
(CLEAN-11).

**Changes both briefs now ask for (one list for the mediator)**

1. Definition:
   - group on the rebuilt family key (built from the raw income) and drop `family_income` as a feature;
   - set the `disea`, `mhi` and `educdec` fills and the unasked `self_rated_health` values to missing.
2. Text:
   - add the `ForcedGroupedFromTemporal` tag and a `splits_comment` with the window scores;
   - add the diagnoses and welfare gap to `fit_reason`;
   - drop the care-manager clause;
   - correct the notes listed in points 6 and 7;
   - change `year` and `source_url` (or add a bullet) once the ICPSR question is answered.
3. Record: drop `No Good Target / Scientific Discovery` and add an Assessment line that supersedes the screening's
   metric line.
4. For the curator: the rename, the ICPSR login, and the SPLIT-8 consistency answer, which carries over to MEPS.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal (AI, 2026-11-01): rand_health_insurance_experiment_doctor_visits**

**Summary.** The advocate concedes nearly every change I asked for, so most of this rebuttal is concession. Two points
stay open, both narrowed:

- *Families (A3).* Regrouping, not a text fix, is the remedy. A check shows the rebuilt family key is sound.
- *PROV-13 (A4).* The origin counts as unreachable only after the curator tries a login, not after an agent gets a
  403.

One new fact came up during the checks: `family_income` also holds site-mean fills.

```text
Verdict (critic, after rebuttal): ship after changes.
Agreed with the advocate: drop the record marker and add an Assessment line; name the missing diagnoses and welfare
  flag in fit_reason; drop the care-manager clause (USE-8, MET-1); add the ForcedGroupedFromTemporal tag and a
  splits_comment (SPLIT-8); drop family_income unless the codebook clears it (LEAK-10); take the extract's year unless
  ICPSR holds the same values (PROV-9); undo the fills (CLEAN-10); correct the notes; keep r2 in dollars (MET-3,
  MET-5); age and MEPS are weighed only.
Open: group on the rebuilt family id (SPLIT-24 with SPLIT-4); the curator tries the ICPSR login before the PROV-13
  note.
New fact: family_income holds one fill value per site (563 persons, 265 families).
```

**A1. The task is the source's own, and the marker falls (P3): concede.**

- The advocate adopts parts (b), (c) and (d) of my point 1:
  - drop `No Good Target / Scientific Discovery` and add an Assessment line;
  - name the missing claims diagnoses and welfare flag in `fit_reason` (USE-8);
  - drop the care-manager clause (MET-1).
- I never disputed that the task is real; Newhouse et al. 1989 settle it (USE-1, USE-2, USE-5).
- Part (a), the rename, is in A6, and there we agree: it is the curator's call, and the fallback is to retitle the
  record.
- Nothing on P3 remains in dispute.

**A2. No leak; `family_income` is dropped without the codebook (P4): concede, with one new fact.**

- We agree on the remedy for LEAK-10: settle it from the codebook, or drop the column.
- One correction to the reasoning. "An average over the person's own years is ruled out" does not clear the reading
  that matters: a family-level average over the family's study years. Both briefs end at a drop, so this changes no
  remedy.
- *New fact.* `family_income` repeats one value per site across unrelated families: 6,735.32 at
  site 6, 8,665.64 at site 2, 6,674.89 at site 5, 9,542.00 at site 1, 7,910.82 at site 4 and 7,196.79 at site 3.
  Together they cover 563 persons in 265 rebuilt families, across 6-11 plans per site. Each value lies within 2% of
  its site's mean income (site 6: 6,735 against 6,796; site 1: 9,542 against 9,469). This is the site-mean fill
  that Decision 1 undoes for `black`. No evidence agent reported it; the column audit flagged only the 0 against 1.0
  coding.
- If the curator keeps the column against the drop, these values become missing as well (CLEAN-10; weak LEAK-30,
  Should), next to the `Potential leak, kept on purpose:` bullet. The drop makes this moot.

**A3. The split: concede SPLIT-8; narrow the family remedy (P4).**

- *SPLIT-8.* Agreed: add the tag and a `splits_comment` with the two windows (year 4: RF 0.147 temporal against
  0.135 on the person folds; year 5: 0.112 against 0.098). No re-split.
- *Families.* The advocate presents the text fix and regrouping as equal options, with the text fix "enough if the
  curator distrusts a key no codebook confirms". I hold that regrouping is the remedy, and my check removes the
  ground for distrust. Within the 1,404 multi-person families of the split auditor's key (consecutive `zper`,
  identical site, plan and income):
  - the plan offers that are set per family agree: `idp` and `coins` in 100%, `mdeoff` in 99.7% (4 families
    differ), `pioff` in 99.6% (5 differ);
  - household shape is plausible: 1,039 families have two adults, 236 one, 90 three;
  - `educdec` varies in 845 families because each adult keeps their own value (818 families) while children take a
    parent's (97.2%). So the builder's key failed on a column that is set per person, not because families cannot be
    recovered;
  - the few mismatches are adjacent families that share a site fill income (e.g. 9,542.00 at site 1). The key merges
    them, and merging too much is harmless for grouping.
- *Rules.*
  - SPLIT-24 (Must) allows exactly this kind of key.
  - SPLIT-4 (Must): the application decides, not the size of the gap. New enrollees join as family contracts, and
    75.7% of the test rows now have a family member on the training side.
  - MEPS groups by household (`DUID`): treat like cases alike.
  - The measured cost is nil (RF 0.0835 on family groups against 0.0821 on person groups).
- *What remains of the text fix.* It is the fallback only if the curator rejects the key itself.

**A4. Provenance (P5): concede PROV-9 and the faithful reading; narrow PROV-13.**

- I never disputed that the reader is faithful (claim audit, row 2; the blind reviewer's own reader).
- *PROV-9.* Agreed: the extract's year and data page, with ICPSR as the second citation, unless ICPSR holds the same
  values.
- *PROV-13.* "Unreachable in this run" means unreachable to the agents, which got a 403. The tension row "repair
  against cleaning around damage" allows a keep with a note only "when the origin cannot be reached". For SUPPORT2,
  the curator reached ICPSR 2957 with a login (Lennart, 2026-10-12).
  - So the order is: the curator tries ICPSR 6439 first, and the note comes only if that fails.
  - Undoing the fills from the data is cleaning around the damage, which ranks below repair (P5 over P7).
  - The income fills raise to six the number of columns carrying the extract's fills. That strengthens the case for
    reading the codebook, not for exclusion.
- If the login fails, I accept a note.

**A5. Worth benchmarking; `r2` in dollars (P6): concede.**

- I did not press the blind reviewer's log target (MET-3 Must, MET-5).
- We agree on putting the tail number in the existing note: one $39,182 row holds 40-56% of its fold's SS_tot, and
  the ridge-against-RF ranking flips on 0 of 9 folds without it.

**A6. Cleaning (P7): concede, with one addition.**

- Agreed:
  - the `FILLS` block for `disea`, `mhi` and `educdec`;
  - the 346 children's `self_rated_health` set to missing;
  - the note corrections (coinsurance coding, the DERIVED comments, "part of its inpatient charges", the 37 partial
    years, the MHI instrument at age 14);
  - the rename as the curator's call.
- Addition: the income fills (A2), if the column stays.
- I never asked P7 to remove the task (tension row P3 over P7).

**A7. Age and MEPS are weighed only: concede.** My brief already left this unpressed: no rule or precedent excludes a
dataset because a modern counterpart exists, and `Outdated` has no rule behind it.

</details>
