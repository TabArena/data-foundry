# alfa_bank_credit_history_default

**Outcome:** added as `alfa_bank_credit_history_default_1m`. Alfa-Bank's credit-bureau default task of Data Fest 2022
(ODS.ai): will a loan applicant default, from the products in their credit-bureau report at application? One row per
application, 418 inputs (417 counts of each code of each of the 59 product fields, as the organisers' boosting baseline
counts them, plus the application id `time_index`), three temporal windows of 500,000 consecutive applications by id
(the id order is stated by the organiser), each trained on a random 1M earlier applications without the window's
repeat clients; ROC AUC, the competition's metric. The AI recommends shipping it, with the competition rules'
"fictitious" read as legal wording for anonymised records.
Verdict: ship after changes (the panel's changes are made: no gap, recorded as an exception rather than as the amended
rule; the frame size of 2,503,777 explained; a note that the counts lose product order and recency; the organiser's
id-order sentence quoted; the library change that would record the row budget is the across-datasets item
**Record row_budget when a definition has its own _make_splits**).
Validity: the source is the organiser's files, and the rules' "fictitious" is open (issue 1, a Must); the bank's
history runs "up to the moment of the application", so no input is recorded after it; no column leaks; the id order is
quoted from the organiser's field description; repeat clients are removed from training; no gap between training and
test, recorded as an exception: a gap would leave the oldest window 42% of the rows, below the 50% floor.
Value: untuned LightGBM 0.73-0.75 ROC AUC per window, 16.4k-19.0k defaults per test window; the task gamer found no
exploit above noise.
Quality: the counts lose the order and recency of the products (0.73 here against 0.783 best private on the
sequences): a note, not a defect.
Weighed: + size, + organiser files with a field description; - the rules forbid passing the data on (in the licence
field); - recency lost in the aggregation.
For the curator: issue 1 (fictitious, Must), issue 2 (`time_index` as an input, weighing).

**Main points:** Read the rules' "fictitious credit histories" as legal wording for anonymised records (recommended,
with the `Anonymized` marker) or exclude (issue 1); keep `time_index` as an input as well as the time column
(implemented, as for california_house_prices_2020) or as the time column only (issue 2). Gap 0 is one case of the
across-datasets item **SPLIT-10 exceptions that serve SPLIT-14 (fifth case)**; decide it there, not here.

**Record judgment:** valid source (Alfa-Bank's files on the competition's data tab, with a field description and a
baseline); the record's fields agree with the definition (binary, temporal, finance, 2022). The `Anonymized` marker
is set, as on alfa_battle_2_0_task_2: every amount and day count is replaced by a randomly numbered interval. No one on the panel disputes the marker.

**Issues for Lennart:**

1. **Read the competition rules' "fictitious credit histories" as legal wording for anonymised records, and keep the dataset?**

   * **Problem:**
     - The competition rules (3.3) describe the input as "данные вымышленных кредитных историй" (data of fictitious credit histories) and the target as the "вероятность дефолта вымышленного клиента" (default probability of a fictitious client).
     - The competition page says the opposite: the task is credit scoring of Alfa-Bank's clients on data that were "тщательно анонимизированы" (carefully anonymised).
     - A generated table is excluded under our rules, and no dataset so far has had a first-party statement on each side[^prov3][^sel16].
   * **Effect on the task:** if the histories are generated, the task is not a real bank's and the dataset goes; if they are anonymised, nothing changes.
   * **Experiments:**
     - All three tests are the builder's; no panel agent re-ran them.
     - Every `is_zero_*`, `pclose_flag` and `fclose_flag` = 1 falls into a single code of the field it summarises (the interval holding zero), as in a real bureau extract (builder).
     - `rn`, which orders the products by opening date, moves `pre_since_opened` one way in 99.53% of the 14.8M changes between consecutive products, against 42% with the pairs shuffled (builder).
     - No row-counter pattern (codes against the id modulo k < 200), and the default rate rises from 2.4% to 5.0% when the newest product was opened recently, a known credit-hunger pattern (builder).
   * **Consistency:**
     - No earlier case: ibm_hr and water_quality went out where the creator stated generation and nothing contradicted it; here a first-party page contradicts the word and the tests pass.
     - The sibling alfa_battle_2_0_task_2 (same bank, Data Fest 2022 re-host) carries `Anonymized` for the same random interval numbers; its competition rules were not read for the same wording.
   * **Panel:** the advocate, the builder, the domain practitioner and the precedent checker read it as legal wording; the critic accepts that reading but asks that it be recorded as a precedent and that the sibling's rules be checked first.
   * **What would settle it:** reading alfa_battle_2_0_task_2's competition rules for "вымышлен" (its definition and record have no such word, and its rules PDF was not read); the same word there with the same anonymised-data page would make this a family reading, its absence would leave this case alone; a statement from the organiser would also settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Legal wording for anonymised records (implemented) | keep the dataset with `Anonymized`; the reading goes into the record as the first case | the organiser's page and the provenance tests agree; a real bank's bureau data at scale | rests on reading a legal text against its words; first case of its kind |
     | B | Exclude | the record goes to `No` | follows the rules' words | loses a real-looking 3M-row credit task against a contradicting first-party page |
     | C | Decide after reading the sibling's rules | the dataset waits; the sibling's rules are read for the same wording | a fact that may settle it | a delay; the sibling's rules may not exist in the same form |

   * **Recommendation:** A: the tests and the competition page outweigh one word in a legal text; the critic accepts A but asks that the sibling's rules be read first (C costs one read). **Decision:** A, B or C?

   **Notes for the AI:** on A, add a CC line to the record with the reading and the reasons, and a case row in
   `provenance.md` (Cases) through the curator. On B, set the record to `No` with `Synthetic` and retire the folder.
   On C, read the sibling alfa_battle_2_0_task_2's competition rules for "вымышлен".

   [^prov3]: **PROV-3** (Must): the data is real, not generated or a real table someone reworked; the curator checks
     a claim of generation with the methods of the rule.
   [^sel16]: **SEL-16**: a generated or simulated table is out unless the generator is the object of study.

2. **Keep `time_index` (the application id) as a model input, or only as the time column?**

   * **Problem:**
     - `time_index` is the application id, the only time the data has; the definition keeps it as the time column and as one of the 418 inputs.
     - Under the temporal split every test value lies beyond the training range, so a tree reads it as "the newest training slice".
   * **Background:** no house rule says whether a time column is also an input; california_house_prices_2020 keeps its id as both[^split22].
   * **Effect on the task:** it never helps an honest model; ROC AUC per window ignores a constant shift of the predictions, so the harm is small: up to 0.003 ROC AUC with a 300k training sample, within noise at 1M.
   * **Experiments:**
     - Task gamer (random 300k training rows, 400 trees): -0.0022, -0.0032 and -0.0032 ROC AUC with it, against noise of a random column up to 0.0015.
     - Split auditor (the full 1M training sides, 300 trees): -0.0004, -0.0006 and +0.0012, noise about 0.0016; the mean prediction moves up by 0.0018-0.0045.
     - The two setups differ in training size: the harm is small and grows when the training sample is thinner.
   * **Consistency:**
     - Keeping it follows california_house_prices_2020; alfa_battle_2_0_task_2 dropped its app id because a month could be rebuilt from it, which does not hold here.
     - Dropping it here would depart from california, on two facts: the id is a fine-grained counter with no coarser time, and there is a measured harm.
   * **Panel:** for keeping, the advocate and the precedent checker (no rule forbids it; the metric is invariant to the shift); for the time column only, the critic, the split auditor, the task gamer and the blind reviewer (an ordering key that extrapolates); the column auditor raised it as a question and would keep it if the house keeps time columns as inputs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Time column and input (implemented) | as now | follows california_house_prices_2020; no rebuild | an input that cannot generalise; small measured harm on smaller training samples |
     | B | Time column only | `time_index` stays the time column and is marked not a feature | removes an extrapolating input | departs from california; the duplicates note changes (2.8k-4.8k test rows then have training copies, harmless) |

   * **Recommendation:** B, lightly: an id that only extrapolates is no input a deployed model would use, and the call is a convention for every dataset whose only time is an id. **Decision:** A or B?

   **Notes for the AI:** on B, mark `time_index` not a feature in `dataset.py` (keep `Temporal(on="time_index")`),
   restate the curation_comments' "Duplicates" note without `time_index` (copies across the split are natural repeats
   of coarse codes), re-run `dataset check` and the leak probe on duplicates; consider a house rule in `splits.md`.

   [^split22]: **SPLIT-22**: a temporal split needs a time column; the definition names it.

**Review panel:** ship after changes (mediator). The rebuttal round was skipped under the budget rule: the opening
briefs converged except on `time_index` as an input and the id-order quote, which the mediator settled from the
source file (description.xlsx, re-read 2026-11-09). Claim audit: no claim refuted. Column audit: no leak in any
column. Split audit: right with notes (no gap, now recorded as an exception). Blind review: include with
changes (its concern about the id order is answered by the quote). Task gamer: no exploit above noise; training on the newest 300k rows instead of a random 300k gains up to 0.0046, a
modelling choice (no change). Disputed:
`time_index` as an input (issue 2); "fictitious" left to the curator (issue 1).

<details><summary>Mediator</summary>

Mediator report: alfa_bank_credit_history_default (folder alfa_bank_credit_history_default_1m), 2026-11-09
Rebuttal round skipped (budget rule); settled on the opening briefs, the seven phase-A reports and the builder's report.

1. RECOMMENDATION (judgment record)
Verdict: ship after changes.
Validity: SEL-1 holds; SEL-16/PROV-3 open for the curator (rules 3.3 say "fictitious"; PROV-3 tests pass; issue 1);
  USE-1 holds (approximate fit: a bureau-only sub-score); LEAK-10 holds (23% recency test, history "до момента подачи
  заявки"); LEAK-16..21 hold (copies only without time_index, short histories, LEAK-18); LEAK-30 kept with its note;
  SPLIT-7/22 hold (id order quoted verbatim below); SPLIT-9 holds (repeat-client filter, 0 shared client_key);
  SPLIT-10 departed from (gap 0) for SPLIT-14: record as exception, not application (change 1); SPLIT-12/14/19 hold.
Value: TP holds (LightGBM 0.73, 16.4k-19.0k positives per test window); MET-2 holds (ROC AUC, source's metric).
Quality: CLEAN-14 holds; CLEAN-19 baseline counts kept (no published top solution) with a note (change 3).
Weighed: size +, source + (organiser files), licence - (rules forbid passing on; noted), recency features lost -.
For the curator: issue 1 (Must, "fictitious"), issue 2 (time_index as input, weighing), issue 3 (row_budget library
  change), issue 4 (SPLIT-10 amendment, cross-dataset), issue 5 (Anonymized marker confirmation).

2. CHANGES TO MAKE NOW (no decision needed)
C1. SPLIT-10 / SPLIT-14 (P4): restate the splits comment's "No gap (SPLIT-10 as amended 2026-11-05)" as an exception
    to SPLIT-10 serving SPLIT-14's floor, like alfa_battle_2_0_task_2 (2026-10-21). None of the amended rule's no-gap
    conditions holds (no label dates, no fixed horizon); the 250k gap would leave the oldest window 42%. Every panel
    agent who spoke to it agrees (advocate concedes, critic, split, domain, precedent). Wording only, no rebuild.
    Record the exception in the record's CC lines.
C2. Reproducibility (builder issue 2, metadata): until the library takes row_budget after a custom _make_splits, keep
    the README sentence on the frame size and make it plain: 3,000,000 source applications -> 2,503,777 rows = union of
    three 500k test windows and three 1M stratified training samples (ids below 1.5M kept at about two thirds); no
    filter by target besides the SPLIT-9 removal. The blind reviewer read the gap as "500k rows dropped unexplained".
C3. CLEAN-19 note (quality, Should): one line in the description that the table is a bag-of-codes aggregation of the
    product sequences (organisers' baseline), losing order and recency, which caps scores (0.73 here vs 0.783 private
    on sequences). The definition already says the construction; add the consequence.
C4. Note in the record that the id-order quote was re-read (below) so SPLIT-7 is no longer "untested".

3. ISSUES FOR THE CURATOR (ranked: validity first, Must first)
Issue 1 (P2/P5, Must; SEL-16, PROV-3): "fictitious" in the competition rules.
  Problem: rules 3.3 say "данные вымышленных кредитных историй" / "вымышленного клиента"; the ODS page says carefully
  anonymised data of Alfa-Bank clients. Effect: if generated, the task is not real (exclude).
  For keeping (advocate, builder, domain, precedent): PROV-3 tests pass: flags fall inside one code of the field they
  summarise; rn keeps opening order in 99.53% of 14.8M changes vs 42% shuffled; no row-counter pattern; newest-product
  recency raises default 2.4% -> 5.0% (a real credit-hunger pattern); first-party page contradicts "fictitious".
  Against (critic): no panel agent re-ran the tests; first case of its kind; the sibling's rules not checked.
  Precedent: none direct; ibm_hr and water_quality excluded where the creator states generation and nothing
  contradicts it. Distinguishing fact here: a conflicting first-party statement plus passing tests.
  What would settle it: the sibling's (alfa_battle_2_0_task_2) competition rules read for the same wording (the grep of
  its definition and record finds no "fictitious"; its rules PDF was not read); or a statement from the organiser.
  Decision: read "fictitious" as legal wording for anonymised records (recommended; write the reading into the record
  as a precedent) or exclude.
Issue 2 (P4, weighing; SPLIT-22, no house rule): time_index (application id) also a model input?
  Facts agreed: every test value lies beyond the training range; it never helps.
  Measured: gamer (random 300k training sample, 400 trees) -0.0022/-0.0032/-0.0032 vs random-column noise up to
    -0.0015; split auditor (full 1M training sides, 300 trees) -0.0004/-0.0006/+0.0012, noise ~0.0016, mean prediction
    shifted up by 0.0018-0.0045. The two setups differ (training size), so the numbers do not contradict each other:
    the harm is small and grows when the training sample is thinner. Not a conflict of rules; no rule decides.
  For keeping (advocate, precedent): california_house_prices_2020 keeps the id as time column and feature; ROC AUC per
    window is invariant to a constant shift; no rule forbids it.
  For dropping from features (critic, column, split, gamer, blind): an ordering key that extrapolates, helps no honest
    model, measured harm at 300k.
  Mildest remedy if dropped: keep it as the time column, mark it not a feature; then restate the duplicates note
    without time_index (2.8k-4.8k test rows have train copies, LEAK-18, harmless). A departure from california would
    name its fact: here the id is a fine-grained per-application counter with no coarser time, and a measured harm.
  What would settle it: the curator's house convention on time columns as inputs (applies across datasets).
Issue 3 (process, not a rule): library change so make_splits applies a declared row_budget after a custom
  _make_splits (builder option a). Supported by split auditor, critic, advocate. A change to
  src/data_foundry/v2, beyond this dataset; C2 covers the gap until then.
Issue 4 (cross-dataset; principles.md "Exceptions and amendments"): this is the fifth SPLIT-10 exception serving
  SPLIT-14 (alfa_battle_2_0_task_2, lending_club, spanish_homeowners_motor_insurance_2010_2014,
  wisconsin_local_government_property_insurance_fund, this); an amendment is due at the third. Proposed (precedent
  checker): "no gap where the needed gap breaks SPLIT-14's floor and SPLIT-9 is met", citing the five cases.
Issue 5 (selection.md marker): confirm the Anonymized marker (every amount and day count replaced by random interval
  numbers; description.xlsx footnotes * and **), as on the sibling. No one disputes it.
Notes only (no decision): LEAK-24 release-end default fall (applicants, measured; kept); EV-4 licence (rules 6.1.5,
  6.1.9; already in the definition's license field; critic's remedy met: cite the organiser files, which the
  definition does). Selection to issued loans only (domain): note.

4. AGREED FACTS
- Source: 3,000,000 applications, target 3.55% (106,442); 418 inputs (417 counts + time_index), no constants, uint8.
- Id order is time, quoted verbatim from description.xlsx (sheet 1, row "id"; re-read by the mediator 2026-11-09):
  "Идентификатор заявки. Заявки пронумерованы так, что более поздним заявкам соответствует более поздняя дата."
  This settles disputed fact (b) and answers the blind reviewer's concern 1 (he had no access to the xlsx). A weak or
  non-monotone label trend by id (AUC 0.495-0.522) does not refute stated order.
- Splits: test ids 2.5-3.0M / 2.0-2.5M / 1.5-2.0M; max train id below test min; 1M/500k sizes; frame 2,503,777.
- SPLIT-9 filter: 13,224 / 10,642 / 7,743 training rows removed; 0 shared client_key after.
- Gap: a 250k gap costs 0.0010-0.0015 AUC (upper bound) and would leave the oldest window at 42%.
- No leak in any column; LEAK-30 interval cuts likely over all rows (weak, noted).
- Task gamer: no exploit above noise (0.0015).
- ROC AUC is the source's metric; best private 0.782805.

Task gamer's exploits mapped:
- Count of identical vectors over train+test: LEAK-30 (transductive), new, gain -0.0013..+0.0010 = none. No issue.
- Training-label lookup of exact copies: LEAK-16..21 / LEAK-18, known (definition's duplicates note), 0.6-1.0% of test
  rows, gain -0.0003..-0.0002; matches the note (natural coarse repeats). No issue.
- time_index as feature: SPLIT-22, known (issue 2), harms. Issue 2.
- Recent 300k training rows +0.0046/+0.0037/+0.0009: SPLIT-14 / modelling choice, new; not a task flaw (a participant
  may weight recent rows). Optional, no change recommended: shrinking training sets to recent rows would change the
  shared random-sample design for all temporal 1M versions.
- Lookup in the public HF copy: known for every public set; not ranked.
No exploit's gain differs from what a note says.

5. CONSISTENCY WITH PRECEDENT
- time_index as time column: follows california_house_prices_2020; sibling dropped app_id because a month was
  rebuildable there (distinguishing fact). Dropping it as an input (issue 2) would depart from california, with the fact
  named above, or as a curator convention.
- Gap 0: C1 brings it in line with alfa_battle_2_0_task_2 and lending_club; as written it departed (application) with
  no amendment condition met.
- SPLIT-9 filter: same as alfa_battle_2_0_task_2.
- "Fictitious": no precedent; whatever the curator decides becomes the first case (add to provenance.md Cases).
- Metric: source's ROC AUC, consistent with the MET-4 tension row (a company's competition).
- Anonymized marker: consistent with the sibling.

</details>

<details><summary>Claim audit</summary>

Claim auditor: alfa_bank_credit_history_default_1m (2026-11-09)
Verdict: no claim refuted. Pipeline run in memory only (_load_raw, _clean, _make_splits on the cached application_features.parquet), nothing built.

claim | source | test | result | evidence | rule
10 target 3.55% | curation_comments, claims 10 | count flag in raw | holds | 106,442 / 3,000,000 = 0.03548 | -
16 418 inputs | claims 16, task_summary.known | count columns after _clean | holds | 418 (417 counts incl. n_products + time_index); no constant column; max count 58 fits uint8 | CLEAN-14
18 drop of 3 codes | _clean asserts | ran asserts | holds | asserts pass on the data | CLEAN
23 windows | splits_comment | ids per split | holds | test 2.5M-3.0M / 2.0M-2.5M / 1.5M-2.0M; max train id below test min; no index overlap | SPLIT-11/12
25 SPLIT-9 filter | splits_comment, decision 1 | client_key of train vs test per split | holds | 0 training applications share a client_key with their test window | SPLIT-9
28 budget and frame | splits_comment, version_comment | sizes, overlap, rates | holds | 1,000,000 / 500,000 each; frame 2,503,777; train pos rate 3.62/3.63/3.57% vs 3.55% overall (stratified); train sides overlap 798k/599k/748k (one shared random order, as stated) | -
P6 worth benchmarking | builder checklist | test positives | holds | 16,407, 17,715, 18,998 | TP
21/32 copies across split | claims 21, 32 | hash of all features without time_index, test vs train | holds | 2,823 / 4,092 / 4,771 test rows have an exact copy in train, none with 5+ products (all short coarse histories, LEAK-18) | LEAK-16..21
12 metric | metric block | ODS page, data tab, FAQ text | holds | "Метрика соревнования - ROC AUC"; leaderboard column ROC AUC; binary per application, no scoring inputs; every window has >16k positives | MET-1..3
13 best private 0.782805 | claims 13 | ods_lb.html | holds | 134 teams, 1st 0.782805 | -
29 / decision 2 release-end fall | decision 2 why | default rate per 100k block | holds | newest 2.61% vs 3.05%-4.15% before (text's 3.1-4.2 is rounding) | LEAK-24
implicit: time_index is a fair feature | definition | AUC of -time_index alone per test window | holds (weak signal, as intended for a temporal task) | 0.522 / 0.519 / 0.505 | SPLIT-22
implicit: horizon / label maturity | fit_reason | untestable: no label dates, one extraction | untested | - | LEAK-24, EV-5
22 id order = time | description.xlsx | not re-read (xlsx quote taken from builder) | untested here | - | SPLIT-7
6 "fictitious" | rules 3.3 | builder's PROV-3 tests not re-run | untested here (no new test cheaper than the builder's) | prov3.log | SEL-16, PROV-3

Minor inconsistency (not a refutation): decision 2's why says the mean prediction drops "from 3.6% to 3.0%", curation_comments says "2.9-3.1%"; same fact, consistent within range.

Ranked refuted: none.
Ranked untested: (1) "fictitious" data, SEL-16/PROV-3 Must, curator issue 1 stands; remedy: curator decision, as drafted. (2) Label maturity at the release end (LEAK-24): no data can settle it; remedy: keep the note. (3) id order = time (SPLIT-7): rests on description.xlsx quote; remedy: a reviewer opens description.xlsx once.
Builder issues weighed: issue 2 (row_budget not recorded) is metadata only, the budget is applied correctly (verified sizes); issue 3 gap 0 consistent with measured small gap cost.

</details>

<details><summary>Column audit</summary>

Column auditor: alfa_bank_credit_history_default_1m (2026-11-09)

Verdict: no leak and no cleaning problem in any column. One question for the curator (time_index as model input), plus two notes.

Checked: application_features.parquet (3,000,000 x 422): no constant column, no count >= 255 (uint8 is safe), 59 fields with 2 to 20 codes each. dtype probe: 0 of 418 flagged ("no codebook": description.xlsx only describes id and flag, and the field meanings come from the ODS data tab, as quoted in curation_comments).

Column table (grouped: the 417 counts share one construction)
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
default (target) | source flag, 1 = default on the issued loan, no horizon | outcome | category No/Yes | fine (horizon gap noted, LEAK-24) | CLEAN-25
time_index | application id, in date order (description.xlsx) | yes, it is the application order | int64, time column, also a model input | question | SPLIT-7/SPLIT-22
n_products | number of bureau products before the application | yes ("до момента подачи заявки"; LEAK-10 recency test, 23%) | uint8 count | fine | CLEAN-14
pre_since_opened/confirmed__k, pre_pterm/fterm__k, pre_till_pclose/fclose__k | day counts to the collection date, as random interval codes | yes, measured to the application moment; the sign of pre_till_* cannot be read (random codes), and fclose_flag sits inside one code | uint8 counts per code, no order assumed | fine | CLEAN-14, LEAK-37 (cannot verify)
pre_loans_credit_limit, next_pay_summ, outstanding, max_overdue_sum, credit_cost_rate __k | amounts as random intervals | yes | counts | fine; max_overdue_sum__0 dropped correctly (it marks the same single product) | CLEAN-14
pre_loans_total_overdue__0/1 | current overdue debt, one code on all products but one | yes | dropped (the __0 count equals n_products) | fine, correct drop | CLEAN-*
pre_loans5/530/3060/6090/90 __k, is_zero_* | late-payment counts by bucket and zero flags | yes | counts | fine | CLEAN-14
pre_util, pre_over2limit, pre_maxover2limit, is_zero_util/over2limit/maxover2limit | utilisation ratios | yes | counts | fine | CLEAN-14
enc_paym_0..24 __k | monthly payment status, last 25 months | yes (at collection) | counts, 4 codes each | fine | CLEAN-14
enc_loans_account_holder_type, credit_status, credit_type, account_cur __k | relation, status, type, currency | yes (status as of the application) | counts | fine | CLEAN-14
pclose_flag, fclose_flag __0/__1 | planned/actual close date is missing | yes | counts | fine | CLEAN-14
id/rn (product level), client_key | ids | - | not in the frame: rn ordered the linking, client_key dropped after the splits | fine |

Problems, ranked
1. (Question, low) time_index is a model input. Under a temporal split its test values are all beyond the training range. A tree treats it as a constant at the edge, but it can still pick up the default-rate drift (3.0-4.5% falling to 2.5-2.9% at the newest end). The mildest remedy is to keep it if the house convention keeps the time column as a feature; otherwise the curator marks it as not a feature. I did not measure its effect.
2. (Note) Each of the 12 two-code fields (the is_zero_*, pclose_flag, fclose_flag, pre_loans_total_overdue already dropped) gives __0 + __1 = n_products, so one count of each pair is redundant. This is lossless, harmless, and the organisers' baseline. Remedy: none.
3. (Note, kept) The interval cuts were most likely made over all rows (LEAK-30, weak). Already stated in the definition.
Builder issues weighed in my role: issue 5 (baseline features only) is acceptable, since no richer published features exist. Issues 1, 2, 3, 4, 6 and 7 do not concern columns.

</details>

<details><summary>Split audit</summary>

Split auditor: alfa_bank_credit_history_default_1m
Verdict: right with notes.

Regime. A bank scores each new application from the client's bureau report and refits on past applications: a stream
over time. Declared temporal on time_index (the application id, stated by description.xlsx to follow the date;
SPLIT-7, SPLIT-22). Three expanding windows of 500,000 (the competition's own test size, SPLIT-12/19); train sides
50/67/83% before sampling (SPLIT-14 met). Measured train/test ranges: [1, 2,499,998] -> [2.5M, 3.0M), [1, 1,999,999]
-> [2.0M, 2.5M), [1, 1,499,999] -> [1.5M, 2.0M); no overlap. Training side sampled to 1M (stratified), test 500k.
Not a grouped task: a new client is not the use case (most applicants are unseen; 3.5% of applications link), so the
SPLIT-9 filter on linked repeat clients is the right handling of the hidden groups, not a grouped split.

Gap and late labels. No label dates, no horizon. Gap 0, defended by the builder's measurement (a 250k gap costs
0.0010-0.0015 AUC, an upper bound; it would put the oldest window at 42%). Same facts as alfa_battle_2_0_task_2,
recorded there as an exception (builder's issue 3). I agree with gap 0; I lean to recording it as an exception
serving SPLIT-14 like the sibling, since "every label final at release / not selected by outcome" (the 11-05
amendment) cannot be shown here without label dates. Rate by training quarter (newest window): 3.20, 3.81, 3.81,
3.63%; test 3.28%. The newest quarter drops less than the release-end window, consistent with drift, not strong
censoring.

Hidden groups. Linked repeat clients (60,048 links) removed from each training side when linked to a test row
(13,224 / 10,642 / 7,743): SPLIT-9 met. Partial (histories under 6 products not linked); the builder measured the
residual effect as small. No copies with time_index; one-product count profiles repeat naturally (LEAK-18).

Finding 1 (P4, low; question raised by the column auditor): time_index as a model input.
Evidence (untuned LightGBM 300 trees, lr 0.05, 63 leaves, shipped splits, 418 features with vs 417 without):
  window 0 (newest): AUC 0.7369 with, 0.7373 without (-0.0004); mean prediction 0.0369 vs 0.0351, test rate 0.0328
  window 1:          AUC 0.7463 with, 0.7469 without (-0.0006); mean prediction 0.0385 vs 0.0340, test rate 0.0354
  window 2:          AUC 0.7481 with, 0.7469 without (+0.0012); mean prediction 0.0357 vs 0.0330, test rate 0.0380
  time_index takes 1.7-2.2% of the gain, yet adds nothing beyond draw noise (two draws differ by ~0.0016).
Every test value lies beyond the training range, so a tree reads it as "the newest training slice" and carries the
recent rate forward; with ROC AUC (rank per window) a constant shift cancels, hence the null effect. It is an
ordering key, not something the bank knows about the applicant besides the date, and it cannot generalise to new ids.
Rule: P4 / SPLIT-22 keep it as the time column; whether the time column is also an input has no house rule.
Mildest remedy: keep it as the time column but mark it not a feature (it costs nothing measurable and removes an
extrapolating input); keeping it is also defensible since the metric is invariant to the shift. Curator decides.

Finding 2 (note): builder's issue 2 (row_budget not recorded because of the custom _make_splits) is metadata only;
the split itself applies the 1M/500k budget correctly. Support option (a).

</details>

<details><summary>Domain practitioner</summary>

Domain practitioner report: alfa_bank_credit_history_default (folder alfa_bank_credit_history_default_1m)
Actor: a retail credit-risk modeller / underwriting decision at Alfa-Bank, scoring a loan application from the credit-bureau (BKI) report.

FIT: approximate (agree with the definition). The bureau report at application is a real input I always have and default on the issued loan is what I act on, but I would also have the application form and the bank's own data, the target has no stated horizon, and only issued loans are labelled.

1. Inputs at the moment of prediction (USE-1, LEAK-10)
- Have: every bureau field per product, as of the application date (organisers: history "up to the moment of the application"); the builder's check that the applied-for loan is not in its own history (23% newest-interval share) satisfies me. No leak from the future in the inputs, apart from the label-free interval cuts over all rows (LEAK-30, weak, kept; I agree).
- Missing that I would always have: application form (amount and term requested, product, income, age, region), the bank's internal history with the client (for existing clients, the strongest block), the bureau's own score. So a model here is a bureau-only sub-score, which is how banks actually build modules (a bureau scorecard combined with an application scorecard), so this is a realistic component, not the whole decision.
- Representation: counts of codes per field (baseline aggregation) drop recency and order (the newest products, the latest 25-month payment string). A real bureau scorecard leans on "worst delinquency in last 12 months", "number of inquiries / new products in last N months". The data supports such features (order recoverable from rn); keeping the organisers' baseline is defensible under CLEAN-19 but caps realism. I would add at least the latest product's codes as an expert; leave as is for the benchmark (builder issue 5: agree, keep).
- Anonymised random interval numbers: no monotone order in amounts; a practitioner loses monotone constraints and reason codes (regulatory explainability). Acceptable for a benchmark; it is the source's state (builder issue 4: confirm the Anonymized marker).

2. Target
- default = "client defaulted", no horizon (in practice usually 90+ DPD within 12 months on book). Proxy close enough; the immature newest labels concern is real but measured (release-end fall explained by applicants, LEAK-24 note: agree).
- Labels exist only for issued loans (selection bias / reject inference). Training and testing both on the accepted population is standard practice for behavioural benchmarks; note only.
- I want a probability (PD): for the cut-off by approval rate and for pricing / IFRS 9 provisioning.

3. Row and test (USE-2, SPLIT-11, SPLIT-9)
- One row = one application = one decision: yes.
- Test = next 500,000 applications after training, refit on all earlier: exactly how a scorecard is redeveloped and deployed (out-of-time validation). Good.
- Repeat-client filter (SPLIT-9): correct and necessary; the earlier application's flag set after the later application is a classic leakage a validator would flag. Gap 0 (builder issue 3): in practice an out-of-time sample is chosen so labels have matured; with no dates the 250k gap costs only 0.001-0.0015 AUC; I accept gap 0 and lean toward recording it as an exception like the sibling, since the reason is the missing horizon, not a measured absence of immaturity.

4. Would I use it? Yes as a bureau module challenger model (gradient boosting vs. logistic scorecard). Trust: out-of-time windows, repeat-client filter, stable 3.5% rate. Distrust: no reason codes on random codes, no horizon, the "fictitious" wording (builder issue 1: I read it as legal anonymisation wording; the measured internal structure, e.g. recency raising default 2.4% -> 5.0%, is what real bureau data shows).

5. Metric: YES. ROC AUC (Gini = 2*AUC-1) is the industry standard for selecting a credit scorecard on discriminatory power, and the source's own metric (MET-2). Per application is the unit I act on (MET-1). No cost matrix or single cut-off is fixed (cut-off is set later by approval-rate policy), so a threshold metric would be wrong (MET-6, MET-7). Imbalance (3.5%) is no reason for PR AUC (MET-9). Only gap: I also need calibrated PDs for pricing/provisioning (MET-8); log loss would score that, but AUC is how I choose the model, calibration is done after. Keep roc_auc.

Gaps ranked by how much they change the task:
 1. Bureau-only inputs: no application form or internal bank data (a module, not the full decision).
 2. Baseline count features lose recency/order of the history (the core of bureau scoring).
 3. No default horizon, newest labels possibly immature (gap 0).
 4. Accepted-only population (no reject inference).
 5. Random interval codes: no monotonicity, no explainability.
What an expert would change: add recency features (latest product, last-12-month delinquency); define a fixed horizon; out-of-time gap; combine with application data. None are possible from the release except recency features.

Builder issues weighed: 1 keep (fictitious = anonymised); 2 no domain view, (a) fine; 3 gap 0, record as exception; 4 confirm Anonymized; 5 keep baseline; 6, 7 notes.

Sources: dataset.py and README.md of the folder; builder_report.md; https://ods.ai/competitions/dl-fintech-bki (as quoted in the definition); https://github.com/SmirnovValeriy/dl-fintech-bki (baseline); general credit-scoring practice (Gini/AUC for scorecard selection, out-of-time validation, 90+ DPD 12-month default definition, Basel/IFRS 9 PD calibration). No web pages fetched in this review beyond the definition's citations.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: alfa_bank_credit_history_default
Verdict: include with changes. The data is real and useful, but the "temporal" split rests on an id whose time ordering no source documents. The features are a fixed hand-made aggregation, and the row count does not match the source.

TASK
Alfa-Bank / ODS competition (dl-fintech-bki). Predict whether a loan applicant will default, using only their credit-bureau history. The bank's credit desk would make this prediction when the application arrives, to approve or price the loan. This is a real use. The competition metric is ROC AUC.
Prepared table: 200k-row sample of 2,503,777 rows, 419 columns. There is 1 int64 time_index, 1 category target (Yes = 3.58%), and 417 uint8 count features. Each feature counts how many of the applicant's credit products fall in each bin of an original encoded field (pre_*, enc_*, is_zero_*, flags), plus n_products (1-54, median 7). Check: summed over each row, the 416 bin counts equal exactly 58 x n_products for every row. So the table is a "bag of bins" aggregation of the sequence data.

CONCERNS (most serious first)
1. The temporal split is not supported by the sources. time_index ranges 1..2,999,982, with one unique value per row, so it is the source's application id. The HF card (mllab/alfa_bki) calls it the "application ID" and does not say whether ids are chronological. The ODS page says the competition split is temporal ("train ... M months, test ... following K months"). That describes the hidden competition test set, not id order inside train. In the sample, the default rate by id decile rises and then falls (0.030, 0.035, 0.040, 0.041, 0.039, ..., 0.035, 0.030), and time_index alone has AUC 0.495. Nothing shows it is time. Change: either find documentation that ids are chronological, or call it a random / iid split and drop the "temporal" claim. Either way, keep time_index out of the features: it is an id.
2. The row count does not match the source. The source train set has 3,000,000 applicants, but the task says 2,503,777, and ids reach 2,999,982. About 500k applicants were dropped, and I could not find why. If the drop was by target or by history length, it biases the task. Change: document the filter.
3. The features are a fixed, lossy aggregation. Order and recency of products are gone (no per-product sequence, no "last product" features). The source invites sequence modelling. The table is still a legitimate tabular task, but the encoding choice decides how well models can do. The counts are also unnormalised, so they scale with n_products. Change: say in the description that this is an aggregation, and consider adding per-client means or the last product's values.
4. The classes are imbalanced (3.6% positive). That is fine with AUC. Scale is fine: 2.5M rows, roughly 90k positives.
5. Duplicates: 447 of 200k sampled rows (0.2%) have identical features. This is expected for applicants with 1-2 products and is not a leakage concern.

SIGNAL / DIFFICULTY
LightGBM (400 trees), trained on the first 80% of the sample by id and tested on the last 20%: AUC 0.714. This is not trivial, and top competition scores were about 0.78-0.79 on sequence models, so there is room to improve. Top features: is_zero_loans530, pre_loans_credit_cost_rate, pre_util, pre_till_pclose. None of them looks like a target proxy.

LEAKAGE
All features describe the bureau history before the application, according to the source. I found no target proxy. I could not verify how the source measures or binarises each bureau field.

COULD NOT CHECK
- The ODS Data tab, which needs a login, so the real meaning of id or whether there is a timestamp.
- The full 2.5M rows; I looked only at the sample.
- Why 500k rows are missing.
- The exact binning that produced the __k columns.

</details>

<details><summary>Task gamer</summary>

Task gamer report: alfa_bank_credit_history_default (roc_auc; 3 temporal windows of 500k test rows each)

Verdict: I found no exploit that beats the honest baseline by more than the noise (about 0.0015 AUC).

Setup: untuned LightGBM (400 trees, lr 0.05, 63 leaves), trained on a random 300k-row sample of each training set and scored on the full test window with score.py. 

Split   honest  +random  +time_index  +dupcount_all  +copylabel  recent300k  nonzero-count only
r0f0    0.7250  0.7252   0.7228       0.7260         0.7247      0.7296      0.522
r1f0    0.7345  0.7330   0.7313       0.7332         0.7343      0.7382      0.529
r2f0    0.7366  0.7357   0.7334       0.7361         0.7362      0.7375      0.532
Noise: adding a random column moves the score by -0.0015 to +0.0002.

Exploits ranked by gain: none clear the noise.
1. Count of identical feature vectors over train and test together (uses test-row statistics): -0.0013 to +0.0010. This is noise. Fix: none needed.
2. Mean training label of exact copies of a test row: copies cover only 0.6-1.0% of test rows; gain -0.0003 to -0.0002. Fix: none needed.
3. time_index (the application id, consecutive within each test window) as a feature: -0.0032 to -0.0022, which hurts. The default rate drifts with the id (3.1% to 4.1% to 3.2%), but a tree cannot extrapolate past the training ids. Fix: keep time_index out of the features, or say plainly that it is an index.

Row order: the label is uncorrelated with the next row's label (r = 0.001). The gaps between ids do not differ by label (mean 1.198 for both classes). ids below 1.5M are subsampled to two thirds; ids above 1.5M are kept whole.
Formats: all features are uint8 bin codes, so decimals and sentinels do not apply. The number of non-zero cells alone gives AUC 0.52-0.53, which is just the history length. That is signal, not an artefact.
Columns from after the prediction point: none seen. The features are binned bureau history known at application, and no single column comes close to the full model (not checked column by column).
Web: nothing public on leaks or magic features for the ODS.ai dl-fintech-bki competition. Looking rows up in the Hugging Face source (mllab/alfa_bki) works as with any public set; not ranked.

Flaw that hurts an honest model (mild): training on the most recent 300k training rows instead of a random 300k gives +0.0046 / +0.0037 / +0.0009, with the default rate drifting over time. An honest deployed model would do the same, so this is a modeling choice, not a task flaw. The likely cause is old rows dominating each training set of 1M rows. Fix (optional): build the training sets from the most recent rows.

Not checked: per-row aggregation from the raw product sequences (the kit ships only aggregates); tuned or full-data models; per-column AUC scans.
Sources: https://huggingface.co/datasets/mllab/alfa_bki ; https://app.alphaneural.io/datasets/mllab/alfa_bki

</details>

<details><summary>Precedent check</summary>

Precedent checker: alfa_bank_credit_history_default (folder alfa_bank_credit_history_default_1m), 2026-11-09
Read-only. Sources: splits.md (SPLIT-7/10/14/22 text and Cases), provenance.md and selection.md Cases, sibling
datasets/_dev/tabarena-v0pt2/alfa_battle_2_0_task_2 (dataset.py, README.md, record), california_house_prices_2020,
lt_vehicle_loan_default_prediction, records grepped for "fictitious/fictional".

VERDICT: consistent on time_index and on the anonymisation reading as far as precedent reaches; ONE real departure
in how gap 0 is labelled (application vs exception) - the domain practitioner is right; and an amendment is overdue.

1. time_index (the application id) as the time column and a feature -- CONSISTENT, with a nuance.
   - SPLIT-7 / SPLIT-22: an id in date order kept as the time column. Precedent: california_house_prices_2020
     ("a higher ID means a later sale ... we name the ID column time_index and use it as a time feature");
     SPLIT-22 cases seismic_bumps, california; bank_marketing (file date order). Same facts here (description.xlsx:
     later ids = later dates). Follows california.
   - Sibling alfa_battle_2_0_task_2 kept the reconstructed issue_month (0-23) as time column and feature and DROPPED
     app_id. Distinguishing fact: there a month could be rebuilt from the week codes, so app_id only re-dated the
     issue at finer grain; here no coarser time exists, so the id IS the time column. Not a departure.
   - Column auditor's worry: a fine-grained id is constant within the test window for trees (extrapolation), and the
     README says no duplicates exist only WITH time_index (LEAK-16..21 read without it). No rule or case makes the
     time column a non-feature; leave as a curator question only if the auditor shows a measured effect.

2. Gap 0 under SPLIT-10 -- DEPARTS in its label, not its outcome.
   - The definition calls gap 0 an application of SPLIT-10 as amended 2026-11-05. The amended text's no-gap
     conditions are: time step longer than the delay (ames, perth), newest period complete on a later read
     (melbourne), or a fixed outcome horizon with every label final (lt_vehicle_loan_default_prediction, 2026-11-05,
     the only "application" for a default task). None holds here: no label dates, no stated horizon, and the falling
     default rate at the release end is explained (applicants) but not measured away as selection.
   - The rule's own last sentence: "Where the gap a case needs breaks SPLIT-14's floor, the departure is an
     exception." A 250k gap leaves the oldest window 42% (< 50% floor). That is exactly the sibling's recorded
     reason: alfa_battle_2_0_task_2, exception 2026-10-21 (Lennart), gap 0 2026-10-26; also lending_club
     (2026-10-21). Same facts (bureau default, no label dates, no horizon, SPLIT-9 met by the repeat-client filter).
   - So: record it as an exception to SPLIT-10 serving SPLIT-14, like the sibling. Builder issue 3 should
     recommend that, not leave it either way.
   - Amendment due: SPLIT-10 exceptions serving SPLIT-14 already number four (alfa_battle_2_0_task_2, lending_club,
     spanish_homeowners_motor_insurance_2010_2014 2026-11-02 Andrej, wisconsin_local_government_property_insurance_fund
     2026-11-08 Lennart); this is the fifth. principles.md asks for an amendment at the third; none is proposed (the
     proposed amendment in the Cases table is the ames/perth one, a different reason).

3. "Fictitious" in rules 3.3 (PROV-3 / SEL-16) -- NO DIRECT PRECEDENT; reading it as anonymised is reasonable.
   - Closest cases: ibm_hr_analytics_... (No, AHDS: "fictional data set created by IBM data scientists") and
     water_quality_and_potability (first upload says "Synthetically generated"): there the creator states
     generation and nothing contradicts it. Here the organiser's own page says Alfa-Bank clients' data, carefully
     anonymised, and the PROV-3 tests pass (flags inside one code, rn order kept in 99.53% vs 42% shuffled, no
     row-counter). Retirements under PROV-3 (credit_card_customers, ecommerce_shipping, homeq...) all rest on failed
     tests; none here. Distinguishing fact: a conflicting first-party statement plus clean tests.
   - Still a Must and a first case of this kind: the curator decides, and the reading should be written into the
     record (and the sibling's rules checked for the same wording, which the builder did not do) so the next case
     follows it. Anonymized marker (issue 4): consistent with the sibling's record ("- Anonymized").

DRAFT ISSUE (for REVIEW.md, the gap label; the one departure without a stated reason)
Should gap 0 be recorded as an exception to SPLIT-10 serving SPLIT-14, as on alfa_battle_2_0_task_2, rather than as an application of the amended rule?
**Problem:**
- The definition calls gap 0 an application of SPLIT-10 (2026-11-05), but none of the amendment's no-gap conditions
  holds: no label dates, no fixed horizon, not every label known final.
- A 250k gap would leave the oldest window 42% (< SPLIT-14's floor), the rule's stated case for an exception.
- The sibling, same bank, same kind of default label, recorded the exception (2026-10-21, gap 0 2026-10-26).

| Option | Pro | Con |
|---|---|---|
| (a) Exception serving SPLIT-14, like the sibling (AI's guess at the fact: the floor, not a measurement, is why no gap) | like cases alike; matches the rule's text | fifth exception of this reason, so the amendment becomes due now |
| (b) Application of the amended rule | no new exception | no amendment condition met; departs from the sibling without a stated fact |
| (c) Amend SPLIT-10 now: "no gap where the needed gap breaks the floor and SPLIT-9 is met", cite the five cases | ends the exception run | a rule change, decided on purpose, beyond this dataset |

Recommendation: (a) for this dataset, and open (c) as a cross-dataset item.
[1]: SPLIT-10, SPLIT-14, SPLIT-9; principles.md "Exceptions and amendments", "Tensions".

</details>

<details><summary>Advocate</summary>

ADVOCATE opening brief: alfa_bank_credit_history_default (folder alfa_bank_credit_history_default_1m). Ship as defined.

1. No leak, no exploit (LEAK-*, CLEAN-*, Must). Column auditor: no leak in any of 418 columns. Task gamer: no attack beats
   the honest baseline by more than noise (0.0015 AUC); copies (0.6-1.0% of test rows) give nothing. The strongest
   failure modes were checked with numbers and none appears. Outranks every softer objection below: these rules rank first.

2. Real task, right metric (P2/SEL, PROV). Domain practitioner: a bank scoring a new application from the bureau report,
   a challenger to a logistic scorecard; "would use it". ROC AUC is the source's metric (claim auditor). "Fictitious"
   (builder issue 1, SEL-16/PROV-3 Must): the data shows real bureau structure (newest-product recency raises default
   2.4% -> 5.0%; flags inside the intervals they summarise); ODS calls it anonymised clients' data. Mildest remedy:
   curator reads it as anonymised, plus the Anonymized marker (builder issue 4), as for the sibling alfa_battle_2_0_task_2.

3. Temporal split is right (SPLIT-7/12/14/19/22). description.xlsx states ids follow the date; precedent
   california_house_prices_2020 (id as time). Three 500k windows = competition test size; pools 83/67/50%. Blind reviewer's
   "AUC 0.495, no trend" does not refute order: SPLIT-7 rests on the stated order, and a weak label trend is expected
   for a stable 3.5% rate. Remedy if doubted: one reviewer opens description.xlsx (claim auditor), not a re-split.

4. Hidden-group shortcut removed (SPLIT-9, Must). 60,048 repeat-client links (later default 89% after an earlier one)
   filtered from training sides (7.7k-13.2k rows per window); same handling as the sibling.

5. Gap 0 (SPLIT-10): concede the label, keep the outcome. A 250k gap costs only 0.0010-0.0015 AUC and would break
   SPLIT-14 (oldest window 42%). Record it as an exception serving SPLIT-14, like alfa_battle_2_0_task_2 (precedent,
   split auditor, domain). A wording change, no rebuild.

6. "~500k rows dropped" (blind 2) is the row budget, not a filter: source 3,000,000 rows; train sides sampled to 1M,
   tests 500k; frame 2,503,777 = union kept (split auditor, claim row 28: holds). Fix = metadata only (builder issue 2:
   library applies row_budget after custom _make_splits, or state it in the README). No selection by target.

7. time_index as an input: harmless, consistent. Measured -0.0004/-0.0006/+0.0012 (noise 0.0016); gamer -0.002/-0.003
   only when exploited deliberately. Precedent california_house_prices_2020 keeps id as time column and feature; no
   rule forbids it. Excluding it is a curator preference, not a defect. Baseline features (CLEAN-19): no published
   top solution, so the organisers' aggregation is the sourced choice; blind 3 is an extension, not a failure.

</details>

<details><summary>Critic</summary>

Critic, opening brief: alfa_bank_credit_history_default (folder alfa_bank_credit_history_default_1m), 2026-11-09
Position: ship only after the changes below. No point asks for exclusion; points 1-2 are Must-level and must be settled first.

1. "Fictitious" source data (validity, SEL-16 / PROV-3, Must). Rules 3.3 call the input "fictitious credit histories" of a "fictitious client". The ODS page says anonymised client data. The builder's PROV-3 tests pass (flags inside one code, rn order 99.53% vs 42% shuffled, recency 2.4% -> 5.0%), but no panel agent re-ran them (claim auditor: untested), and nobody checked whether the sibling's rules use the same words. This is the first case of its kind (precedent checker). Effect: if the data is generated, the task is not real. Remedy: the curator decides, and the reading ("fictitious" = legal wording for anonymised, backed by the PROV-3 results) goes into the record as a precedent. Check the sibling alfa_battle_2_0_task_2's rules for the same wording before deciding.
2. Gap 0 is labelled as an application of SPLIT-10, but none of the amended rule's no-gap conditions holds (SPLIT-10, Must, with SPLIT-14). There are no label dates and no horizon, so labels are not known to be final. A 250k gap costs 0.0010-0.0015 AUC and would push the oldest window to 42%, below the floor. Effect: newest labels may be immature, and the definition hides that this departs from the rule. Precedent, split auditor and domain practitioner all agree. Remedy: fix the definition so it records an exception serving SPLIT-14, as the sibling does (2026-10-21). Open the overdue SPLIT-10 amendment (fifth case) as a cross-dataset item.
3. time_index, the application id, is a model input (P4 / SPLIT-22, Should). Every test value lies outside the training range. Measured effect: gamer -0.0022 to -0.0032 AUC (beyond noise 0.0015); split auditor -0.0004/-0.0006/+0.0012, and the mean prediction shifts by 0.002-0.0045. It is an ordering key that cannot generalise to new ids, and it helps no honest model. Remedy: keep it as the time column but mark it not a feature. The README line "no copies with time_index" must then be restated without it (2.8k-4.8k test rows have train copies; harmless, LEAK-18).
4. The id-is-time claim rests on one quote nobody re-read (SPLIT-7, Must for the temporal regime). The claim auditor marked "id order = time" untested. The blind reviewer, without description.xlsx, saw no trend (time_index AUC 0.495) and doubted the temporal split. Remedy: a reviewer opens description.xlsx once and quotes it verbatim in the README.
5. Row budget missing from the metadata (Should, reproducibility). The custom _make_splits samples by hand, so the container records no splits.row_budget. The blind reviewer read the 2,503,777-row frame against the source's 3,000,000 as "500k rows dropped unexplained". It is in fact the budget sample of ids below 1.5M (gamer: two thirds kept). Remedy: builder option (a), the library change, or at least a README sentence explaining the frame size.
6. Features are the organisers' baseline counts only (quality, CLEAN-19, Should; not a reason to exclude). Order and recency are lost, and recency is the core of bureau scoring (domain). This caps realism: LightGBM reaches 0.73 against 0.78 private. Remedy: a note in the description saying this is a bag-of-codes aggregation, with no recency features.
7. Licence (EV-4, note). Rules 6.1.5 and 6.1.9 forbid passing the data on. The CC BY 4.0 copy's uploader is unknown. Remedy: a note in the README, and a citation to the organiser-hosted files, not the HF copy.

</details>
