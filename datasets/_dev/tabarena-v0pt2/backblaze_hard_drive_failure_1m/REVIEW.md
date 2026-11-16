# backblaze_hard_drive_failure

**Outcome:** added as `backblaze_hard_drive_failure_1m`. The AI recommends shipping it: the review panel's changes are
made, and two calls are left to you, the first a confirmation of what is implemented. Changes made, needing no decision: the servers' boot drives are left out (67,620 rows; no boot-drive failure has been recorded since December 2024, so their 'not failed' meant 'not recorded'), and so are the data drives without a pod slot on the cut day (6,353 rows, 369 of them failing; an empty slot marks a drive already taken out of service for replacement). The year is now 2026, and a protocol line in the split notes forbids reading later months. The task is ours, built on
Backblaze's daily drive logs (Drive Stats, Q1 2025 to Q2 2026): on the first of a month, will a data drive in
Backblaze's fleet be replaced as failed within the next 30 days, given that day's SMART readings and its place in the
data centre? 17 monthly cuts, 5.48 million drive-months, 0.10% positives; the three newest cuts (March to May 2026)
are the test windows, each with all its drives (336,654 to 345,340 rows, 294 to 460 positives) and a random 1M of the
earlier drive-months for training; fallback `roc_auc`.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-16 hold; USE-5 holds, fit approximate (the label is Backblaze's replacement record, 53% proactive
pulls in Q3 2024; the five-counter rule ranks below a model, so no review step on an input as in xente); LEAK-25
triggered for the boot drives (no failure record since December 2024) and fixed by dropping them, and for the
scattered drives that vanish without a record, dropped; LEAK-10 triggered (an empty pod slot marks a drive already out
of service) and fixed by dropping those rows, a rule that reads no label; LEAK-22 triggered by the builder's drop of
the vault migrations and fixed by keeping them as No (issue 1 confirms); LEAK-9 triggered (the next month's snapshot
gives a test window's labels away, ROC AUC 0.993-0.996) and fixed by a protocol line; SPLIT-1, 3, 9, 10, 12, 13, 14
hold; PROV-9 triggered and fixed (year 2026).
Value: TP-1 to TP-9 no flag; 294 to 460 test positives per window; MET-11 fallback stands (no source fixes a share
of the fleet to act on, MET-7).
Quality: CLEAN-10/11 sentinels set to missing; CLEAN-14 fact for `pod_slot_num` written; CLEAN-19 a weighing call
(issue 2).
Weighed: the operator's own fleet logs and a real fleet review (the monthly cadence is ours) +; size and test positives +; the label partly the
operator's own pulls -; a model well above the operator's rule +.
For the curator: issue 1 (confirm the removal rule, settled by rank); issue 2 (change features, a weighing call). A metric on the top of the ranking (asked for by the critic and the domain practitioner) is not an issue: no source fixes the share, so it would need a change to the rule against invented thresholds.
The bundle check's one warning, `meta_time_horizon_mismatch`, is proposed for acceptance (not written into
`accepted_check_warnings`): "each one-month test window holds one cut day (the first of the month); the horizon of 1
month is the refit cadence, and the label's horizon is 30 days after the cut", as accepted for perth_house_prices,
zillow_prize and tunisian_fraud_detection_challenge.

**Main points:** Confirm that drives leaving in whole-vault migrations stay as not failed while drives that vanish
alone are dropped (issue 1, implemented, recommended); keep the snapshot only or add the change of the error counters
over the 30 days before the cut (issue 2, snapshot implemented, a weighing call); your verdict also accepts the one check warning (each monthly test window holds a single cut day).

**Record judgment:** valid. The record's fields agree with the definition (`Company` counts as `Other`); the record's links to SurvSet, frailtySurv and awesome-public-datasets point to a small, old survival extract, not this data, and now sit in the discovery note. The screening's "fit direct" is approximate: half the failures are Backblaze's
own proactive pulls.

**Issues for Lennart:**

1. **Keep drives that leave in a whole-vault migration as not failed, and drop only the drives that vanish alone?**

   * **Problem:**
     - 8,541 data-drive rows leave the files within 30 days of their cut without a failure record: 8,356 in blocks of 20 or more drives of one vault after one cut (migrations) and 185 single drives scattered over the cuts.
     - The builder dropped all of them as "outcome unknown"; the panel's ruling keeps the migrated drives as No, because dropping an exit that happens after the prediction point chooses the rows by the future, and drops only the scattered drives, which look like failures without a record[^l22][^l25].
     - The builder dropped them all, and the advocate and the critic both asked to keep that drop and fix only its notes, so the mediator's reversal needs your confirmation.
   * **Background:**
     - Backblaze counts drives removed for other reasons as not failed[^klein], so the source's own label for a migrated drive is No.
     - One of the five error counters Backblaze watches (SMART 5, 187, 188, 197, 198) is above zero on 42.7% of the scattered drives, 12.4% of the migrated ones, 7.7% of the kept No rows and 69.8% of the Yes rows (counted before the slot rule, on 206 scattered and 8,361 migrated drives).
     - The migrated drives' share is below the 22.3% of kept No rows of the same age and for ST8000DM002, the model of most young migrated drives, it is 31.9% among the migrated and the kept drives alike, so they show no sign of unrecorded failures; the scattered drives do.
     - The block rule reads no label, and every block is complete by the cut plus 30 days, so it is known at each window's refit.
   * **Effect on the task:**
     - The test windows of March, April and May 2026 hold 1,054, 900 and 120 migrated drives as No; the oldest of them (HGST 8 TB drives in March) rank high among the test negatives, so keeping them makes the test a little harder.
     - The choice moves the test ROC AUC by at most 0.0006 either way.
   * **Experiments:** split auditor, a regularised LightGBM per shipped train side, one seed, the removed drives added to the test as No (counts before the boot and slot rules):

     | Test window | Removed drives | ROC AUC without them | ROC AUC with them as No | Their median percentile among the test negatives |
     |---|---|---|---|---|
     | 2026-05-01 | 151 | 0.9127 | 0.9127 | 71st |
     | 2026-04-01 | 940 | 0.9123 | 0.9124 | 16th |
     | 2026-03-01 | 1,102 | 0.8876 | 0.8870 | 96th |

   * **Consistency:**
     - Keeping the migrated drives follows framingham_heart_study_fhs, which keeps its 251 deaths from other causes as No and drops only the 16 lost to follow-up.
     - Dropping the scattered drives follows mortgage, fraud_detection_in_electricity_and_gas_consumption_1m and rais_employment_separation_1m, which drop exits whose outcome the source left unrecorded, by a rule that reads no label; a migration's outcome is recorded (No), which sets it apart from them.
   * **Panel:**
     - Drop the migrations too (builder, advocate, domain practitioner): 95.7% of the removals are whole-vault blocks, planned migrations the operator knows at the cut and would not score.
     - Keep them as No (split auditor, mediator; the critic made the same rule argument but asked for no change to the rows unless you take this option): "planned before the cut" is an inference the release does not record[^ev2], and the drop uses the realised removal, which the rule on competing exits forbids[^l22].
     - Keep every removal as No (split auditor's simplest option): the mediator ruled it out because it labels likely failures No.
   * **Unknown:** whether Backblaze schedules a vault migration more than 30 days ahead; a Backblaze statement or record of that would let option B rest on what the operator knows at the cut instead of on the realised removal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Migrations kept as No, scattered drives dropped (implemented) | 8,356 rows stay as No; 185 leave | the source's own label for a migrated drive; no choice of rows by the future; follows framingham | the test holds old drives about to be migrated, which an operator may not score |
     | B | Drop every removal (the builder's first version) | 8,356 more rows leave | matches an operator who does not score drives it plans to move | the plan is not in the release, so the drop reads the realised removal; departs from framingham without a recorded fact |
     | C | Keep every removal as No | 185 more rows stay as No | the simplest rule | labels likely unrecorded failures No (42.7% carry an error counter) |

   * **Recommendation:** A: a migrated drive's outcome is recorded (not failed), so its row stays; a drive that vanishes alone may be an unrecorded failure, so its row goes; B needs a Backblaze record that migrations are scheduled more than 30 days ahead, which we do not have. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: nothing to change.
   - B: in `_label_cut`, set `keep = eligible & ~pl.col("removed_in_horizon")`; write the fact that migrations are planned before the cut, with its Backblaze link, into the "Kept as No" bullet (renamed into the rows left out) as a scope call under USE-7, not an exception to LEAK-22; update `task_summary.changes`, the decision's text and the test-window counts in `splits_comment` and `version_comment`; re-run `dataset check`, the leak and task probes.
   - C: set `keep = eligible`; replace the scattered-drive bullet with a note that 185 likely unrecorded failures stay as No; the same updates and re-runs.

   [^l22]: **LEAK-22** (Must): a competing event after the prediction point keeps the label it had, No; dropping it selects the cohort on the future (framingham_heart_study_fhs, 251 deaths, Lennart, 2026-10-22).
   [^l25]: **LEAK-25** (Must; amended 2026-10-21, Lennart): "no event" mixed with "not recorded" is a censoring bias; unrecorded rows located by a rule that does not read the label are dropped (caracas_cervical_cancer, account_debt_south_africa, fraud_detection_in_electricity_and_gas_consumption_1m).
   [^klein]: Backblaze, "What SMART Stats Indicate Hard Drive Failures" (Andy Klein, 2016-10-06): "Drives which have failed are marked as such and their data is no longer logged"; drives removed for other reasons are not counted as failures (https://www.backblaze.com/blog/what-smart-stats-indicate-hard-drive-failures/).
   [^ev2]: **EV-2** (Must): evidence ranks; a measurement on the data first, an inference (a plausible reading of the source) last.

2. **Keep the cut day's SMART snapshot only, as now, or add the change of the error counters over the 7 and 30 days before the cut?**

   * **Problem:**
     - The rows carry the cut day's readings only; the SMART error counters are cumulative, so a drive's history shows as a level, not as how fast it is rising now.
     - Backblaze names new uncorrectable read errors as its main reason to replace a drive, and published practice on this data and the PAKDD 2020 challenge builds windowed changes of the counters, which a fleet team would read too[^c19].
     - The measured gain is small and mixed, so whether a data scientist would build them is a weighing call.
   * **Background:**
     - Building them reads the daily files of the 30 days before each cut (`data_Q4_2024.zip` for the January 2025 cut, already downloaded).
     - The changes of the usage counters (power-on hours, head-flying hours, sectors read and written) carry the out-of-service state that the slot rule now removes (a drive that stops reading), so only the error counters would be built (SMART 1, 5, 7, 184, 187, 188, 189, 197, 198, 199, 200).
   * **Effect on the task:** a model sees a drive with 50 reallocated sectors the same whether they appeared last week or two years ago, while a fleet team sees the difference, so the benchmark cannot reward a method for reading the recent rate; the measured cost is at most about 0.01 ROC AUC.
   * **Experiments:**
     - Builder, a regularised LightGBM, one seed, one random 1M training sample per window, the 7- and 30-day changes of all raw counters, on the rows before the boot, slot and vault-block rules: ROC AUC 0.899, 0.918 and 0.902 on March, April and May 2026, against 0.890, 0.911 and 0.904 without (+0.010, +0.007, -0.002); this run also took the changes of the usage counters and still held the drives without a slot, so part of the gain may be the out-of-service signal the slot rule now removes.
     - Task gamer, monthly lags of a drive's earlier snapshots rebuilt from the training rows (deltas of 15 SMART counters), three seeds: 0.9056 mean against 0.9015 (+0.004, above the seed range of 0.9010-0.9022).
   * **Consistency:**
     - Not building is consistent with the earlier cases: rain_in_australia (better in 8 of 9 windows, a paired standard error of 0.0045) and alfa_battle_2_0_task_2 (3 of 3 windows, the top solutions' features) built a history feature only on firmer evidence than one seed.
     - In this batch, data_fusion_2026_guardian_1m and azure_vm_lifetime_resource_central_1m build the history features their source papers use; Backblaze has no source baseline.
   * **Panel:**
     - Snapshot only (builder, advocate): one seed with a mixed sign, and the cumulative counters already carry the history.
     - Add the error-counter changes (column auditor, domain practitioner): the recent rate is what a fleet team and every published tool read; the level does not show it.
   * **Unknown:** what would settle it: three seeds with a paired standard error on the three windows, with the error-counter changes only, on the shipped rows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Snapshot only (implemented) | the cut day's readings, as now | the daily files used as they are; no feature of ours | leaves out the recent rate a fleet team reads |
     | B | Add the 7- and 30-day changes of the 11 error counters | about 22 columns more, built from the daily files before each cut | what practice builds; Backblaze's own replacement indicator | the gain is measured on one seed only, mixed in sign; reads one more quarter of files |

   * **Recommendation:** A, as implemented: the one measured gain is one seed, mixed in sign and partly from columns B would not build; if you lean to B, mark B and the AI runs the three-seed check first (Notes) and builds the columns only if the gain holds in all three windows. A weighing call. **Decision:** A or B?

   **Notes for the AI:**
   - B: in `_prepare_raw_files`, also read `data_Q4_2024.zip` for history only, and keep the readings of the 11 error counters (raw) of every drive on the days 7 and 30 before each cut; in `_clean`, add `<column>_d7` and `<column>_d30` as the cut day's value minus the value then (missing when the drive has no reading that day); update `download_description`, the "Not built" bullet and the README; re-run `dataset check`, the leak probes (a change can carry the out-of-service state: check the missing indicators) and the task probes. The builder's construction is in the run folder's `scripts/change_features.py`.
   - To settle it first: the builder's script with three seeds and the error counters only, on the shipped rows; report the paired difference and its standard error per window.

   [^c19]: **CLEAN-19** (Should): a feature is built when it is what a data scientist on this task would build because the raw data cannot be used as it is, such as a history aggregated to one row per prediction (rain_in_australia, 2026-10-26; alfa_battle_2_0_task_2, 2026-10-13).

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator.
Claim audit: 26 written and 6 implied claims; every count reproduced; refuted and fixed: the boot-drive keep (no boot
failure record since December 2024) and "about half proactive" as a suggestion (it is a count, 47.0% / 53.0%); partly
refuted and fixed: "the removals are vault migrations" (95.7% are) and the December dip (partly unrecorded failures);
untested: whether later downloads revise failure flags. Column audit: an empty pod slot marks a drive already out of
service (dropped) and the boot drives cannot be positive (dropped); sentinels set to missing. Blind review: include
with changes; its main concerns were the training subsample (documented) and a label look-ahead across the boundary (closed by the 29-day gap); it also asked to drop the boot drives (done). Task gamer:
nothing beats an honest model inside a split; the next month's snapshot gives two of three windows away (a protocol
line now). Debate: agreed on the boot drives, the slotless drives, year 2026 and the notes; disputed: where the protocol line goes (in the definition, mediator), the removed drives (settled by rank, issue 1 confirms), the `last_seen` look-ahead (a note), a context
metric (no source fixes a share, so `roc_auc` stays), and the change features (issue 2).

<details><summary>Mediator</summary>

MEDIATOR REPORT: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Read: principles.md, leak_checks.md (LEAK-7/9/10/22/23/25), splits.md (SPLIT-9/10), metrics.md
(MET-6 to MET-11), use_case.md (USE-7); all nine panel reports and both rebuttals; builder_report.md; dataset.py; the
record. Own runs (thread caps 4, under 13 GB): (the run's work files).

**1. JUDGMENT RECORD**

Verdict: ship after changes.
Validity: SEL-1, SEL-16 hold. USE-5 holds, fit approximate (label = replacement record, 47.0% reactive / 53.0%
  proactive; the five-counter rule ranks below a model). LEAK-25 triggered, fixed: boot drives dropped (no failure
  record since Dec 2024) and the 206 scattered data-drive removals stay dropped. LEAK-10 triggered, fixed: data-drive
  rows with no pod slot at the cut dropped. LEAK-22 triggered by dropping the 8,361 vault-block exits, fixed: keep them
  as No (issue 1, confirm). LEAK-9 triggered (cross-fold, AUC 0.993-0.996), fixed by a protocol line. SPLIT-1, 3, 10,
  12, 13, 14 hold; SPLIT-9 holds (the `last_seen` look-ahead is no shortcut: about 50-169 No rows per train side, a
  note). PROV-9 triggered, fixed: year 2026.
Value: TP-1 to TP-9 no flag; 327-505 test positives per window (about 1,147 of 1,262 after the slot drop). MET-11
  fallback roc_auc stands; no context metric (MET-7: no source fixes a k or an FPR cap).
Quality: CLEAN-10/11 sentinels to missing; CLEAN-14 fact for pod_slot_num written; CLEAN-19 a weighing call.
Weighed: the operator's own fleet logs and a real monthly review +; size and test positives +; label partly the
  operator's own pulls -; model well above the operator's rule +.
For the curator: issue 1, confirm the removal filter settled by rank (LEAK-22 for vault exits, LEAK-25 for the rest);
  issue 2, change features (CLEAN-19, weighing call).

**2. CHANGES TO MAKE NOW (no decision needed), rank order**

a. [P4, LEAK-25 Must] Drop boot drives, capacity_bytes <= 2.2e12 (builder issue 5, option B). Note: 32 boot failure
   records in Q4 2024, none Jan 2025-Jun 2026; Backblaze reports boot drives apart. The SSD-only columns and the
   smart_245 copy then fall to the existing empty/constant drop.
b. [P4, LEAK-10 Must; LEAK-7 smallest fix; USE-7] Drop data-drive rows whose pod_slot_num is empty at the cut
   (label-free; 2,653 shipped rows, 169 positives; 1,510 test rows, 115 test positives). Note that the reading is
   ours (Backblaze does not document an empty slot) and that it makes the cohort match the drives already left out for
   being absent on the cut day.
c. [P4, LEAK-9 Should] Protocol line in splits_comment (the README is generated from it), naming the mechanism: "A
   method sees only its split's train rows and test window. Rows dated after a test window reveal its labels: a drive
   is recognised across months by model, place (datacenter, cluster, vault, pod, slot), capacity and power-on hours,
   and a drive missing from the next month's snapshot has usually failed (ROC AUC 0.993-0.996 on the March and April
   windows). A method that uses them is called out and not benchmarked."
d. [P4, SPLIT-9/SPLIT-10 note] One sentence with the measured look-ahead of the removal filter (section 4, point 3).
e. [P5, PROV-9 Must; PROV-8] Year 2026 in the definition, the bibtex and the record; keep "published since February
   2015" in the comments. Move the record's SurvSet, arXiv 2203.03094, frailtySurv and apd-core links out of
   source_links into the discovery comment.
f. [P3, USE-5/USE-8 notes; LEAK-25 note clause; EV-2] curation_comments and fit_reason: the Q3 2024 count (640
   reactive, 721 proactive, 47.0% / 53.0%) instead of "a suggestion"; the proactive share by server type (Dell 73.5%,
   Storage Pod 6.0 44.6%) and datacenter (AMS 68.1%, SAC2 47.5%); the fact that sets this case apart from xente (every
   drive monitored, a dead drive always recorded, no review step on an input: the rule scores 0.83-0.87 against
   0.89-0.90); the test cohort leaves out 187 of 1,449 failing drives absent on the cut day (13%; 119 in April);
   the December dip is partly drives that vanish without a record; the removal counts by kind (section 5) with
   LEAK-22 / LEAK-25 cited instead of LEAK-23; the boot sentence "which the operator replaces too" removed.
g. [P6, MET-11 fallback reason] README/metric note: the operator acts on the top 0.1-1% of the fleet; on the test
   windows recall at the top 0.5% and ROC AUC order models differently by a few drives per window (practitioner's
   topk.json); no source fixes the k, so roc_auc stays.
h. [P7, CLEAN-10/11] smart_9_raw 0 (137 shipped rows of drives years old) and 65535 (10), smart_240_raw 65535 (6) to
   missing.
i. [P7, CLEAN-14] Write the fact for the pair: pod_slot_num is a physical position in one chassis (nearby numbers,
   nearby slots; per-slot failure rates flat), pod_id one of a vault's 20 servers with no adjacency. Precedent
   checker R3 option a.
j. [P7, CLEAN-12/CLEAN-1 notes] Seagate raw 1/7/188/195 are bit-packed as shipped; "WUH721816ALE6L4" and
   "WDC WUH721816ALE6L4" kept apart (they report different attributes); cluster_id "not always correct" (Backblaze).
k. [proc.] Accept meta_time_horizon_mismatch with the builder's reason (as perth_house_prices, zillow_prize,
   tunisian_fraud_detection_challenge). At the rebuild, update the counts, the decision table and the probe numbers
   in the notes.

**3. ISSUES FOR THE CURATOR, ranked**

Issue 1 [P4, Must: LEAK-22 against LEAK-25] Drives removed without failure: which are dropped, which stay No?
  Settled by rank; it reverses the builder's implemented option A and both briefs' wording, so confirm.
  Problem: 8,873 rows are dropped because the drive leaves the files within 30 days with no failure record. They are
    three kinds (my count, boot first): 306 boot drives, 206 scattered data drives, 8,361 data drives in blocks of
    20 or more of one vault on one cut.
  Effect: at most 0.0006 test ROC AUC either way (split auditor e1). Test windows Mar/Apr/May: vault blocks 1,059 /
    900 / 120 rows, scattered 19 / 11 / 12, boot 24 / 29 / 19.
  Facts (removed_blocks.log, removed_age.log, removed_young.log): one of the five error counters above zero on 42.7%
    of scattered drives, 12.4% of vault-block drives, 7.7% of kept No and 69.8% of Yes. The vault-block share is below
    its age-matched kept-No expectation (22.3%) and equals its model's: ST8000DM002, 2,763 of the young block rows,
    31.9% in the blocks against 31.9% of its kept No. So the vault blocks show no sign of unrecorded failures; the
    scattered drives do.
  Advocate's best evidence: 95.7% of removals are whole-vault blocks, planned migrations the operator knows at the
    cut, so not a decision at the review; mortgage, STEG and rais drop administrative exits by a label-free rule.
  Critic's best evidence: a vault exit after the prediction point is LEAK-22's competing event (framingham keeps 251
    deaths as No); "planned before the cut" is not in the release, and the drop uses the realised removal.
  Ruling: the two Musts do not conflict; each covers its own rows. LEAK-25 covers the scattered drives (located
    unrecorded failures: drop). LEAK-22 covers the vault blocks: an exit after the prediction point whose label is
    known (Backblaze: drives removed for other reasons are not failures), so the row stays No; dropping it selects on
    the future. The precedents that drop (mortgage, STEG) had labels the source left unknown, which is not the case
    here. The "planned" fact is an inference (EV-2, lowest), and LEAK-22 is a Must with no exceptions.
  Remedy (fix the definition): keep as No the removals that fall in a block of 20 or more drives of one vault on one
    cut; drop the other removals (the boot ones leave with change a). A label-free rule; every block is complete by
    cut + 30 days, so it is known at each window's refit.
  Decision: (A) as above, recommended; (B) keep all removals as No (split auditor; labels 206 probable failures No,
    against LEAK-25); (C) keep the drop, which needs the plan shown known at the cut. What would settle C: a Backblaze
    statement or record that vault migrations are scheduled more than 30 days ahead; then the drop rests on USE-7
    scope (P3) and is written with that fact, not as an exception.

Issue 2 [P7, CLEAN-19 Should, a weighing call] Change features over the 7 and 30 days before the cut (builder
  issue 3; the curator keeps it).
  Builder / advocate (A, snapshot only): one seed, +0.010 / +0.007 / -0.002; the counters are cumulative; precedents
    that built history features had firmer evidence (rain_in_australia 8 of 9 windows).
  Column auditor / practitioner (B): Backblaze's main replacement indicator is new uncorrectable errors, a rate the
    level does not show; published practice and PAKDD 2020 build windowed changes. Caveat: build changes of the error
    counters only, since the usage counters' changes carry the out-of-service state of change b.
  What would settle it: three seeds with a paired SE on the three windows, error-counter changes only.

No other issue needs a decision. Builder issues 1 (fit approximate) and 2 (30 days, monthly) are agreed by every
agent; issue 5 becomes change a; issue 6 becomes change e.

**4. DISPUTED POINTS, SETTLED**

(1) LEAK-9 protocol line. Critic: a protocol line in splits_comment naming how a drive is recognised. Advocate: a
    README sentence. Both rest on LEAK-9 (Should); no conflict on the data. LEAK-9's text and its Cases row
    (medical_facility_operational_data: "a protocol line in the definition ... and the benchmark checks models for
    it") settle it for the critic: the line goes in the definition (splits_comment), which also puts it in the
    generated README. Change c.
    Task gamer's exploit mapped: LEAK-9, evaluation-level leak (other folds' later rows read). The definition has no
    `Potential leak, kept on purpose:` note and no accepted warning on it: NEW. Measured gain: flag alone 0.9934
    (April) and 0.9958 (March), +0.09 to +0.115 over the stable model; the May window is immune. Inside one split
    nothing beat the honest model. Not fixable in the data with one shipped table, so the protocol line is the
    remedy LEAK-9 names.
(2) Removed drives: issue 1 above (LEAK-22 for vault blocks, LEAK-25 for the rest; effect <= 0.0006).
(3) SPLIT-9, `last_seen` beyond the refit (claim auditor I5). Decisive count (split9_lastseen.log,
    split9_vaults.log): training rows kept as No only because the drive reappears after the window's test cut, while a
    refit-time view would call it removed:
      window       rows in eligible pool   share      expected in the 1M side   positives   in vault-wide gaps
      2026-03-01   210                     0.005%     about 50                  0           57% (median gap 82 days)
      2026-04-01   821                     0.017%     about 169                 0           81% (11 days)
      2026-05-01   695                     0.013%     about 134                 0           87% (4 days)
    Every one is absent on its window's test cut day, so none is a test row of that window, and its label (No) is
    correct. No link to a test row's outcome: not a SPLIT-9 shortcut. The diffuse rest falls under SPLIT-10 (Should):
    no gap change, a note with these counts (change d).
(4) MET-11 context metric. The critic and the practitioner would offer recall at the top 0.5% or partial AUC to FPR
    1% as a curator option; the advocate says no. MET-7 (Should): never invent a k or a threshold; a source that gives
    a range fixes none (the literature reports several false-alarm rates, the practitioner's k "moves with technician
    capacity"). MET-11's context branch needs the context to make one metric clear, which the varying k denies, so
    the fallback applies; the tension row agrees ("we never invent a cost or threshold the source did not fix"). The
    measured disagreement is a few drives per window, a direction, not proof. Not a curator option under the rules;
    the README note (change g) documents the gap. Changing this would be an amendment of MET-7, not a per-dataset call.

**5. AGREED FACTS**

- 17 monthly cuts (Jan 2025-May 2026), 5,547,634 kept rows, 5,827 positives (0.105%); 198 cut-day failures and 8,873
  removed-without-failure rows dropped; counts reproduce exactly (claim auditor).
- Split: temporal, three one-month windows (Mar/Apr/May 2026), gap 29 days, train shares 75.3 / 87.5 / 93.7%; 1M
  random train side per window; test windows 339,651-350,349 rows with 327 / 505 / 430 positives; 98.2-98.8% of test
  drives known (split and claim auditors, task gamer).
- The five-counter rule 0.832 / 0.872 / 0.838 against a model 0.887 / 0.903 / 0.904; 21-28% of positives have all
  five counters at zero; 7-day failures ranked like 8-30-day ones.
- Q3 2024: 640 reactive, 721 proactive (47.0% / 53.0%).
- Boot drives: 67,314 rows, 0 positives; 32 boot failure records in Q4 2024, none since; +0.0014 to +0.0019 AUC for
  ranking them last.
- Empty pod slot on data drives: 6,184 rows, 369 positives (5.97% against 0.100%); slot empty on 69% of failure-record
  days; AUC moves -0.002 to +0.003, average precision +0.017 to +0.020.
- Removals: 306 boot, 206 scattered data (42.7% with an error counter), 8,361 vault-block data drives (12.4%, as their
  models' kept No); keeping all as No moves AUC <= 0.0006.
- 187 of 1,449 failing drives over the three windows are absent on the cut day and outside the test (no leak).
- Cross-fold exploit: 0.9934 / 0.9958 on the April / March windows; none inside a split.
- No leak in any probe; no task-probe flag. Year should be 2026 (PROV-9).

**6. CONSISTENCY WITH PRECEDENT**

- Boot drives dropped: follows caracas_cervical_cancer, account_debt_south_africa, STEG _1m (LEAK-25 located and
  dropped); ends the precedent checker's departure 5.
- Year 2026: follows the eleven growing sources (PROV-9); ends departure 8.
- Fit approximate: follows diabetes_3, STEG, chicago_traffic_crashes; set apart from xente by the written fact
  (change f).
- Removal filter (issue 1): keeping vault exits as No follows framingham_heart_study_fhs (LEAK-22); dropping the
  scattered drives follows mortgage and STEG (LEAK-25, labels not recorded). The builder's drop-all departed from
  framingham with no recorded fact; the recommended remedy removes the departure.
- Protocol line: follows medical_facility_operational_data, sepsis_prediction_1m, bank_marketing (LEAK-9).
- Fallback roc_auc: follows ljubljana_breast_cancer, heart_disease (MET-6), sepsis_survival_minimal_clinical_records
  (MET-9); no context metric, as no source fixes a k (MET-7).
- 30-day horizon, monthly windows, accepted horizon warning: follows framingham / cirrhosis (field horizon) and the
  house family (refit cadence).
- CLEAN-19 not built: consistent; not the amendment_due kind (raw history rows).
- pod_slot_num numeric: consistent with lt_vehicle_loan_default_prediction once the fact is written (change i).
- No drift and no third exception found (precedent checker).

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Verdict: ship after changes. Of 26 written claims and 6 implied ones, 2 are refuted, 2 are partly refuted, 2 are left
untested, and the rest hold.
- Refuted: the boot-drive keep (draft issue 5). Boot drives have no failure record after December 2024.
- Refuted, documentation only: claim 10's "a suggestion, not a count".
- Partly refuted: issue 4's rationale (not all removals are vault migrations), and the explanation of the December dip.
- Every count in the notes reproduces exactly. The split, the gap and the metric hold.

Scratch and logs: (the run's work files).
How the data was read:
- The label was rebuilt with the definition's own `_label_cut` and `CUT_DATES`, on the warehouse's
  snapshots/failures/drive_last_seen parquets.
- The splits and the frame are the participant kit's (data.parquet, splits.parquet).
- Scoring used data_foundry.v2.metrics.scorer, with the definition's Metric resolved to binary_classification.
- Failure records per model, capacity and day come from presence.parquet (Q4 2024 to Q2 2026).

**TABLE  (claim | source | test | result | evidence | rule)**

1 | One row per drive per day; a daily snapshot | claims 1; data page |
  WebFetch of the data page; snapshot duplicates | HOLDS |
  The page: "The daily snapshot of one drive is one record". 0 duplicate (date, serial) among 5,556,705 snapshot rows. | PROV-3
2 | year = 2015, first publication | claims 2; dataset.py year |
  Web search | HOLDS |
  The blog "Reliability Data Set for 41,000 Hard Drives Now Open-source" is by Brian Beach, 4 Feb 2015. The data page
  says "Since 2013 ... collected, curated, and published" without a date. The record says 2013: draft issue 6 stands. | PROV-8
3 | Licence: cite Backblaze, the data may not be sold | claims 3; license | data page | HOLDS |
  "Cite Backblaze as the source"; "You can not sell the data itself to anyone; it is free"; derivative works may be
  sold. | PROV-10
5 | Six zips, 7.76 GB; Q4 2024 not read | claims 5; download_description |
  Local file sizes; `QUARTERS` | HOLDS |
  1,020,483,699 + 1,067,562,257 + 1,111,587,745 + 1,157,851,346 + 1,312,921,361 + 2,092,757,685 = 7.763 GB.
  `QUARTERS` does not list Q4 2024. | EV-4
6/7 | 17 monthly cuts; May 2026 is the last complete one | claims 6-7; CUT_DATES |
  Code and dates | HOLDS |
  1 May + 30 days = 31 May <= 30 June. 1 June + 30 days = 1 July, outside the release. | LEAK-24
8 | 5,827 Yes of 5,547,634 kept (0.105%); 124 to 505 per cut | claims 8; notes; decision table |
  Recomputed from the parquets | HOLDS |
  5,547,634 kept, 5,827 positives, 0.1050%. Per-cut rows match the README table exactly (124 Dec 2025, 505 Apr 2026). | EV-1
9 | failure=1 on the last day in service; Backblaze's definition | claims 9; notes |
  WebFetch of the Q3 2025 and 2016 posts; reappearance | HOLDS |
  Q3 2025: a failure is "when a drive vanishes out of the reporting population", and the drive's serial is the
  primary serial of a replacement ticket. Clone-target and temporary tickets do not count, and neither does a drive
  that logged on the quarter's last day. 2016: "Drives which have failed are marked as such and their data is no
  longer logged". In our cuts 35 kept positives are seen again after their failure record. | USE-5
10 | About half proactive, "stated as a suggestion, not a count" | claims 10; notes; fit_reason |
  WebFetch of the Q3 2024 post, asked for verbatim numbers | PARTLY REFUTED (wording) |
  The post has a table: "Q3 2024 failed drives | 640 | 721 | 1,361 | 47.0% | 53.0%" (reactive, proactive). By
  server type: Dell 73.5% proactive, Supermicro 64.5%, Storage Pod 6.0 44.6%. By datacenter: AMS 68.1%, SAC2 47.5%.
  "About half" holds, and it is a count, not a suggestion. The proactive share differs by datacenter and server type,
  which are inputs. | USE-5, EV-2
11 | 30-day horizon from PAKDD 2020 | claims 11; HORIZON_DAYS | WebFetch of the dcbrain diskdata README | HOLDS |
  "predicting whether each disk will fail or not within the next 30 days"; "k as 30 days in our competition". | SPLIT-12
12 | 198 cut-day failures; 8,873 removed (0.16%); 4,264 / 2,143 / 1,102 / 940 on the vault-migration cuts |
  claims 12; notes | Recomputed | COUNTS HOLD |
  fails_on_cut 198; removed 8,873 (0.160% of snapshot rows); March 2025 4,264, January 2026 2,143, March 2026 1,102,
  April 2026 940. | EV-1
12b | "Whole vaults were migrated"; issue 4: "The removals are operator migrations of whole vaults, not a risk the drive
  faced" | notes; builder issue 4 | Removed rows grouped by (cut, vault_id), with error counters and capacity |
  PARTLY REFUTED |
  8,489 of 8,873 (95.7%) are in blocks of >= 20 drives of one vault on one cut. The largest blocks are 1,217 (Mar
  2025), 1,156 (Jan 2026), 1,077 (Mar 2026) and 920 (Apr 2026); May 2026 has vaults 1043 (61) and 1002 (60). The
  other 384 are scattered:
  - 178 are boot drives (see 16b).
  - 206 are data drives. 42.7% of them have one of SMART 5/187/188/197/198 above zero, against 7.7% of the kept No
    rows and 69.8% of the Yes rows.
  - They peak in the November and December 2025 cuts (43 and 52), the months when failure records dip; 16 of these 95
    are the retiring HGST HUH728080ALE600.
  - In the test windows: 19 (Mar), 11 (Apr) and 12 (May 2026), against 327, 505 and 430 positives.
  Some of the scattered removals look like failures without a record. | LEAK-22, LEAK-23, USE-5
13 | 19 serials with >1 failure; 81 seen again after a failure | claims 13; analyse_presence.log |
  Log, plus a count on the splits | HOLDS, now counted |
  Each test window holds 20 drives with a positive label in an eligible training cut (full train side, before
  sampling). Their test label is No in all 3 windows. | SPLIT-9
14 | Columns dropped: serial, failure, is_legacy_format, 58 empty or constant SMART columns, smart_23_normalized |
  claims 14 | Column count; shipped frame | HOLDS |
  197 - 11 id/meta - 58 - 1 = 127 SMART columns, and the frame has 127 + 8 + target = 136. serial_number, failure,
  is_legacy_format and date are absent. No SMART column is constant on the shipped 2.1M frame. Four are nearly
  empty there: smart_252_raw (5 values), smart_175_raw (12), smart_82_* (35), smart_211/212_raw (23). | CLEAN-5
15/17 | 85 models (74 to 81 per cut), 6 datacenters, 7 clusters, 257 vaults, 20 pods | claims 15, 17 |
  Recomputed | HOLDS | 85 models; 74 to 81 per cut. | -
16 | Boot drives are 1.2% of rows (capacity <= 2.1 TB) | claims 16; notes | Capacity on the kept rows | HOLDS |
  1.213%, 67,314 rows. The models are all boot types: BarraCuda/MX500/WD SSDs, DELLBOSS VD, 500 GB 2.5" disks. About
  3,874 to 4,042 per cut, matching Backblaze's 3,881 boot drives in Q2 2026. | -
16b | Boot drives kept "which the operator replaces too" | notes; builder issue 5 (A) |
  Positives among boot rows; boot failure records by month; boot drives that vanish | REFUTED |
  - 0 of 67,314 boot rows are positive.
  - presence.parquet holds 32 boot-drive failure records: 10, 10 and 12 in Oct, Nov and Dec 2024, and none in the 18
    months from January 2025 to June 2026.
  - Boot drives still vanish at about the old failure rate: 7 to 68 per cut. 306 boot rows were dropped as "removed
    without failure", 178 of them outside the vault blocks.
  From 2025 on, a boot drive's failure shows up only as a vanishing. Our filter then drops exactly the boot drives
  that failed, so the 67,314 kept boot rows are No by construction. Effect on the test windows: a ranker that puts
  boot rows last gains ROC AUC +0.0017, +0.0014 and +0.0019. | USE-5, LEAK-22
18 | Change features: 0.899/0.918/0.902 against 0.890/0.911/0.904 | claims 18; notes | probes/change_features.json |
  HOLDS (rounding) |
  Mar 0.8993 (d7+d30) against 0.8897; Apr 0.9182 against 0.9108; May 0.9016-0.9022 against 0.9042. | CLEAN-19
19 | Rule 0.832/0.872/0.838; model 0.887/0.903/0.904; 28.4/21.2/27.4% rule-zero; within those 0.689/0.672/0.729;
  Backblaze 2016 23.3% | claims 19; notes | Rule AUC re-scored with the scorer on the shipped test windows; json; 2016 post |
  HOLDS |
  The rule with the shipped scorer: 0.8316 / 0.8717 / 0.8380, identical to sklearn and to the probe. The 2016 post:
  "23.3% of failed drives showed no warning from the SMART stats we record". | TP-4
19c | Within 7 days ranked as well as 8 to 30 days | notes | json; my days-to-failure distribution | HOLDS |
  9.7% of positives fail within 3 days (10.0% if uniform) and 22.8% within 7 days (23.3%): no pile-up of drives
  already dead at the cut. Positives with every SMART value missing: 0.38%, against 0.13% of negatives (weak). | LEAK-10
20 | MG08ACA16TEY: 64 to 76 a month July to September 2025, 2 to 21 otherwise; "cosmetic"; training only |
  claims 20; notes | fail_months.log; Q3 2025 post | HOLDS |
  64/75/76 in Jul/Aug/Sep, 46 in Oct, 9/18/21 in the test months. The Q3 2025 post names MG08ACA16TEY, "'cosmetic'
  failures" after firmware updates. Not stated: the post gives no count. | USE-5
21 | December 2025 dip from holidays; April 2026 505; Q2 2026 AFR 1.73% "highest in years" |
  claims 21; notes | Daily failure records; Q2 2026 post | HOLDS, with a qualification |
  - Failure records per day fall to 1-5 from 16 Dec to 4 Jan, against about 8-15 otherwise.
  - The post says "The quarterly AFR is 1.73%, the highest it's been in quite a while". "In years" is the press's
    wording.
  - Qualification: the November and December 2025 cuts also lose 95 scattered data drives (12b) that vanish without
    a record, about half with error counters. The dip is partly unrecorded failures, not only slow replacements.
  | USE-5
22 | Temporal; three windows; train cut < test cut - 29 days; Feb left out of the March window |
  claims 22; splits_comment | Kit splits: train cut dates, gap, overlap | HOLDS |
  - r0 May: 16 cuts, last 2026-04-01.
  - r1 Apr: 15 cuts, last 2026-03-01.
  - r2 Mar: 13 cuts, last 2026-01-01 (February left out).
  Train max cut + 30 days <= test cut in all 3, and train and test share no row. Boundary: r0's April-cut labels read
  failure records of 1 May, the test day's own file. | SPLIT-9, SPLIT-10
23 | Oldest window 13 of 17 cuts (75.3%); 4.2M to 5.2M full train; tests 339,651 to 350,349 with 327 to 505 positives;
  a random 1M | claims 23 | Kit splits plus the full counts | HOLDS |
  Full train shares 0.937, 0.875 and 0.753 (5,197,285 / 4,852,501 / 4,175,253). Tests 350,349/430, 344,784/505,
  339,651/327. Train side 1,000,000 each, with per-cut shares within 0.0005 of the full train side: a uniform random
  sample. The frame holds 2,104,715 rows, every one used by a split. | SPLIT-14
24 | Test drives are known drives: vault 99.2%, model 100% | claims 24 | hidden_groups.txt; serial join |
  HOLDS | 98.2% to 98.7% of test drives have a row in an eligible training cut. | SPLIT-13, USE-10
25 | Metric: fallback roc_auc; Backblaze defines none; PAKDD's windowed F1 belongs to another source and fixes no
  threshold | dataset.py metric; README Metric block |
  Looked again: data page, Q3 2024/Q3 2025/Q2 2026 posts, the 2016 post, dcbrain README. Scorer on each fold. |
  HOLDS |
  - Backblaze names only AFR (per model, quarterly, annual, lifetime) and no prediction task.
  - PAKDD 2020 scores precision over a sliding 30-day P-window and recall over a fixed R-window, F1 "classical", and
    states no threshold: MET-6 to fallback is right.
  - MET-2: per-row unit; no scoring columns are needed; both classes in every fold (327 to 505 positives).
  - The scorer runs: constant 0.5000 in all folds, random 0.4916 / 0.5091 / 0.4922.
  - Same target and classes as the use case. Balance about 0.1%; imbalance alone is no reason for PR AUC (MET-9).
  | MET-1, MET-2, MET-6, MET-8, MET-9, MET-11
26 | Fit approximate: label = replacement record, about half proactive, plus firmware pulls | claims 26; fit_reason |
  As claims 10, 19, 20 | HOLDS | Supported. Add the Q3 2024 counts and the per-server-type spread. | USE-5, USE-8
19b | Bundle checks 0 errors, 1 warning, 2 infos | claims 19b; README | README front matter | HOLDS | as stated. | -

Implied claims (not written, attacked anyway)
I1 | Every feature is known at the prediction point | code; frame |
  Code reads the cut-day file only; frame columns; days-to-failure; all-missing rows | HOLDS |
  Only the cut-day snapshot. No serial, failure flag or date. Cut-day failures are dropped. No pile-up of failures in
  the first days, and the all-missing SMART rate is only weakly higher among positives (0.38% against 0.13%). | LEAK-10, LEAK-12
I2 | No row is a copy across the split | leak_probes | Probe 5 read | HOLDS |
  0.1% of test rows have an exact feature copy in training without cut_date, all with the same label; 0.0% with
  cut_date. A drive's own earlier rows are its history (SPLIT-13). | LEAK-16..21
I3 | The split is the one the use case needs (monthly refit, score the fleet on the 1st) | splits | as claim 22 |
  HOLDS | The 1M random training sample is a budget choice, not the operator's. | SPLIT-12, SPLIT-14
I4 | The target is the real-world target for every row | label | Boot drives; scattered removals | PARTLY REFUTED |
  For boot drives (1.2% of rows) the target is not recorded in 2025-26 (16b). For data drives it is the replacement
  record (claim 26). | USE-5
I5 | The removal filter uses only what was known when the label matured | _label_cut | Not run | UNTESTED |
  `last_seen` is the maximum over the whole release. A training row whose drive is absent at its horizon end but
  reappears later stays as No, where a refit-time view would call it removed. Likely a handful of rows: 117,970
  serials have absent days, median 1 day. | SPLIT-9
I6 | Later downloads give the same failure flags | notes, builder | Needs a second download | UNTESTED |
  Q3 2024: "the Drive Stats dataset is updated accordingly" when a drive is later found healthy. Q3 2025: a drive
  "stays failed until it reappears". Probe 13 shows no fall at the end. | LEAK-24

**REFUTED AND UNTESTED, RANKED (validity first, Must first)**

1. [P3/P4, Must: USE-5, LEAK-22] Boot drives have no recorded failures in 2025-26, so keeping them (draft issue 5,
   option A) keeps a class whose label is No by construction. The "removed" filter drops the boot drives that did
   fail: 306 rows, at about the 2024 failure rate.
   - What it changes: 1.2% of rows are trivially No, and the reason given for option A ("the operator replaces them
     too") does not reach the label. ROC AUC lift for a model that learns boot = No is +0.0014 to +0.0019 per window:
     small, but the task is wrong for that class.
   - Mildest remedy: take option B of draft issue 5. Filter boot drives out, by capacity <= 2.1 TB or the boot model
     list (every model at or below that capacity is an SSD, a DELLBOSS VD or a 2.5" 500 GB disk). Backblaze leaves
     them out of its failure statistics too. Write a note with the 32 boot failure records of Q4 2024 against none
     after.
   - Recommendation to the curator: change issue 5's recommendation from A to B.
2. [P4, Should-level selection; LEAK-22/LEAK-23] Draft issue 4's rationale, "the removals are operator migrations of
   whole vaults", holds for 8,489 of 8,873 rows (95.7%). The other 384 are 178 boot drives (item 1) and 206 scattered
   data drives. 42.7% of those data drives have an error counter above zero (kept No 7.7%, Yes 69.8%), and they
   cluster in the November and December 2025 cuts (95).
   - What it changes: some unrecorded failures are dropped rather than labelled. In the test windows that is 42 data
     drives against 1,262 positives (at most about 3% of positives); in training it is mostly the holiday months.
   - Mildest remedy: keep the drop (the outcome is not recorded, and we must not invent a label). Correct the note and
     issue 4: "8,489 in vault-migration blocks; 384 scattered (178 boot drives, 206 data drives with error counters 5x
     as often as kept negatives, partly failures without a record)". If boot drives are filtered (item 1), the 178
     go with them.
3. [P3, documentation; USE-5] The December 2025 dip: "replacements slow over the holidays" is only part of it. The
   Nov/Dec cuts also lose 95 scattered data drives that vanish without a failure record (16 of a retiring 8 TB HGST
   model).
   - Mildest remedy: one clause in the anomaly bullet. Training cuts only.
4. [P3, documentation; EV-2] Claim 10: "about half proactive" is a count, not a suggestion. Q3 2024 reports 640
   reactive and 721 proactive (47.0% / 53.0%), and the proactive share varies with server type (Dell 73.5%) and
   datacenter (AMS 68.1%), both partly inputs.
   - Mildest remedy: cite the count in the notes and fit_reason. It strengthens issue 1 and does not change its
     recommendation (A, approximate).
5. Untested, I6 [LEAK-24]: Backblaze revises failure flags. A second download of one quarter compared row for row
   would settle it; the reproducibility concern in the builder's checklist already names it.
6. Untested, I5 [SPLIT-9]: the train-side removal filter reads `last_seen` from beyond the test date. The expected
   size is a handful of rows, so no change is proposed. Counting it would need presence.parquet per training horizon
   end.

Minor (P7, not a claim): smart_252_raw, smart_175_raw, smart_82_*, smart_211_raw and smart_212_raw have 5 to 35
values in the shipped 2.1M rows, and none on a positive. They are not constant, so CLEAN-5 does not force a drop.

Sources: Backblaze data page (backblaze.com/cloud-storage/resources/hard-drive-test-data); Drive Stats Q3 2024,
Q3 2025 and Q2 2026 posts; "What SMART Stats Indicate Hard Drive Failures" (2016); "Reliability Data Set for 41,000
Hard Drives Now Open-source" (2015-02-04); github.com/alibaba-edu/dcbrain/tree/master/diskdata.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Verdict: ship after changes. Two P4 findings the probes did not flag: a field the replacement process empties
(pod_slot_num's missingness, LEAK-10), and boot drives that cannot be positive in this release (LEAK-25 / LEAK-22,
which changes the builder's issue 5). The rest is P7 cleaning (small) and the CLEAN-19 weighing call of issue 3.

Validity: LEAK-10 triggered (pod_slot_num empty on drives already taken out of service before their failure record;
  fix by dropping those rows, or the column); LEAK-25/LEAK-22 triggered (boot drives: 0 failure records from
  2025-01-01 to 2026-06-30, so 24,845 shipped rows are No by recording; drop them); every SMART value, power-on hours,
  model, capacity and location field is known at the cut (LEAK-10 holds for them; LEAK-37).
Quality: CLEAN-5 (smart_245 normalised == raw), CLEAN-10/11 (a few sentinels and impossible zero power-on hours),
  CLEAN-14 (dtypes hold), CLEAN-19 (issue 3, a weighing call), CLEAN-12 (Seagate bit-packed raws kept, note).
For the curator: issue A (pod_slot_num) and issue B (boot drives) are new; issue 3 gets a caveat.

How I worked
- Frame: the shipped frame, read from the participant kit's data file (2,104,715 rows x 136 columns, the rows the
  splits use; built by the panel prep from the definition) instead of a second full rebuild (28 GB). Timing checks on
  the builder's full labelled frame labelled_explore.parquet (5,547,634 rows, with serial_number and failure date),
  and on the daily files of Q4 2025 to Q2 2026 for 6,265 tracked drives (the run's work files).
  Thread caps set.
- Codebook: Backblaze publishes no field definitions on the data page; Drive_Stats_Schema_Current.csv lists names only.
  Field meanings from the Q2 2023 and Q3 2023 Drive Stats posts (vault_id, pod_id, datacenter, cluster_id,
  pod_slot_num) and the standard SMART attribute table; vendor-specific attributes are marked as such.
- Dtype probe (probes/dtype_probes.txt): flags cluster_id, pod_id, vault_id as numeric_levels. Answer: codes of
  physical units (a cluster, a vault numbered from 1000 in build order, one of the 20 servers of a vault), category
  is right (CLEAN-14). No count or measured quantity is typed categorical; no code is typed numeric except
  pod_slot_num (judgement call, see the table).
- Scripts and logs: (the run's work files).

**COLUMN TABLE (column | meaning | known at prediction? | dtype and cleaning | verdict | rule)**

Non-SMART columns
cut_date | the snapshot day, first of a month (prediction point and time column) | yes | datetime, 17 values | fine | CLEAN-14
model | the model string the drive reports (85 levels) | yes | category | fine; note: "WUH721816ALE6L4" (3,806 rows, 7 pos) and "WDC WUH721816ALE6L4" (447,848) are one product; no serial carries both names, the unprefixed set grows 81 -> 487 drives a cut over 94 vaults and is the only one reporting smart_82, so it marks a firmware/batch: keep, add a note | CLEAN-1 (keep)
capacity_bytes | drive capacity in bytes (20 values) | yes | float, one value per model, no -1 sentinel in the frame (the raw Q4 2024 files have capacity -1 rows; none reach the frame) | fine | CLEAN-14
datacenter | Backblaze data centre (ams5, iad1, phx1, sac0, sac2, yyz1) | yes | category, no missing (Backblaze writes it blank when a vault is busy; none in the cuts) | fine | CLEAN-14
cluster_id | logical group of storage servers (7 codes) | yes | category (probe: numeric_levels; a code, kept categorical) | fine; note Backblaze's caveat (Q3 2023 post: "the cluster_id is not always correct") | CLEAN-14
vault_id | Backblaze Vault, 20 servers, numbered from 1000 (257 levels) | yes | category (probe: numeric_levels) | fine | CLEAN-14
pod_id | which of the vault's 20 storage servers (0-19) | yes | category (probe: numeric_levels) | fine | CLEAN-14
pod_slot_num | physical slot of the drive in its server (0-59 in the frame; the numbering depends on the server type: 26, 45 or 60 drives) | value yes; its MISSINGNESS is written by the replacement process | float; position as a number is a defensible judgement (nearby slots are nearby in the chassis; per-slot failure rates are flat, 0.0006-0.0015) | LEAK (missingness encodes the outcome process; Must; weak under roc_auc, clear under precision at the top). Remedy: drop the rows of data drives without a slot at the cut, else drop the column | LEAK-10, LEAK-7
fails_within_30_days (target) | a failure record on one of the 30 days after the cut | label | category No/Yes, Yes the event | fine | CLEAN-25
Dropped by the definition: serial_number (id; CLEAN-3; the drive's history stays through recurring rows, LEAK-34), failure (0 on kept rows), is_legacy_format (one value), 58 empty/constant SMART columns, smart_23_normalized (one non-100 value) | fine | CLEAN-3, CLEAN-5

SMART columns (127). All are read by the drive on the cut day, before the 30-day window (cut-day failures are
dropped), so all are known at the prediction point; Backblaze's replacement rule reading some of them makes them the
inputs the operator reads, not a leak (USE-6). All are float numbers: counters, measured quantities or vendor-scaled
health scores without words per level, so a number is right (CLEAN-14). Missing = the model does not report the
attribute (model-driven; missing indicators reach 0.55 in leak probe 4). "norm" = vendor-normalised health value
(1-253, scales 100 / 200 / 253 by vendor, higher = healthier), "raw" = the vendor's raw counter or bit field.

attr | meaning | columns | dtype and cleaning | verdict | rule
1 | Read Error Rate (Seagate: bit-packed rate counter) | norm, raw | 2^32-1 sentinel on 10 boot-SSD rows | fine (sentinel -> missing optional) | CLEAN-10
2 | Throughput Performance (HGST/Toshiba) | norm, raw | norm 252 on 407 boot-HDD rows (ST500LM012 HN: "no value") | fine; 252 -> missing optional | CLEAN-10
3 | Spin-Up Time | norm, raw | HGST norm 253 on 251 rows (vendor initial value) | fine | CLEAN-14
4 | Start/Stop Count (counter) | norm, raw | ok | fine | CLEAN-14
5 | Reallocated Sectors Count (counter; Backblaze rule) | norm, raw | ok; norm 252 on boot HDDs | fine | USE-6
7 | Seek Error Rate (Seagate: errors in the upper 16 bits, seeks in the lower 32) | norm, raw | packed field kept as shipped | fine, note | CLEAN-12
8 | Seek Time Performance | norm, raw | ok | fine | CLEAN-14
9 | Power-On Hours (drive age at the cut) | norm, raw | per-model maxima plausible (0.02 to 13 years, no unit mix); raw 0 on 137 shipped rows (282 in the full frame, 1 pos) of drives that are years old, and 65535 on 10 ST8000NM0055 rows: impossible / sentinel | fine as a feature (read at the cut, not a span set by the outcome); 0 and 65535 -> missing | LEAK-37 holds; CLEAN-11
10 | Spin Retry Count (counter) | norm, raw | raw 2.1e10 outliers (packed) | fine | CLEAN-14
11 | Calibration Retry Count | norm, raw | 966 non-missing, boot HDDs only, 0 pos | fine (would empty if boot drives go) | CLEAN-22
12 | Power Cycle Count (counter) | norm, raw | ok | fine | CLEAN-14
13 | Soft Read Error Rate (SSD) | norm, raw | 549 rows, boot SSDs; raw 2^48-1 on 1 row | fine | CLEAN-10
16, 17 | vendor-specific (Seagate boot SSDs; spare-block counts by the values) | raw | 11,630 rows, boot only | fine; meaning unknown | -
22 | Current Helium Level (HGST/WDC helium drives) | norm, raw | raw 100 normal, packed outliers to 6.5e6 | fine | CLEAN-14
24 | vendor-specific (WDC/HGST helium drives) | norm | ok | fine; meaning unknown | -
27 | vendor-specific | norm, raw | ok | fine; meaning unknown | -
82 | vendor-specific, only on the unprefixed WUH721816ALE6L4 | norm, raw | 35 rows | fine | -
90 | vendor-specific (WDC) | raw | values near 2^48 on some rows | fine; meaning unknown | -
165-169 | WD SSD vendor counters (boot SSDs) | raw | 1,939 rows, boot only | fine | -
170 | Available Reserved Space (SSD) | norm, raw | boot only | fine | -
171, 172 | SSD Program / Erase Fail Count | raw; 172 norm too | boot only | fine | -
173 | SSD Wear Leveling Count | norm, raw | norm 0/252-255 on 158 CT250MX500SSD1 rows (vendor codes) | fine | CLEAN-10
174 | Unexpected Power Loss Count | raw | boot only | fine | -
175 | Power Loss Protection Failure (SSD) | raw | 12 rows | fine | -
177 | Wear Range Delta (SSD) | norm, raw | boot only | fine | -
179, 181 | Used Reserved Block Count / Program Fail Count Total (SSD) | 179 norm, raw; 181 raw | 588 rows | fine | -
180 | Unused Reserved Block Count (SSD) | norm, raw | boot only | fine | -
183 | Runtime Bad Block / SATA downshift count | norm, raw | boot only | fine | -
184 | End-to-End Error | norm, raw | ok | fine | -
187 | Reported Uncorrectable Errors (counter; Backblaze rule) | norm, raw | raw 65535 on 27 Seagate rows = a saturated 16-bit counter (real, at least 65535): keep | fine | USE-6
188 | Command Timeout (Seagate: three 16-bit counters packed; Backblaze rule) | norm, raw | packed field as shipped | fine, note | CLEAN-12
189 | High Fly Writes | norm, raw | ok | fine | -
190 | Airflow Temperature | norm, raw | norm == 100 - raw on every row (a copy under a fixed transform) | fine; drop of norm optional | CLEAN-5 (exact copies only)
191 | G-Sense Error Rate | norm, raw | ok | fine | -
192 | Power-off Retract Count | norm, raw | ok | fine | -
193 | Load Cycle Count | norm, raw | ok | fine | -
194 | Temperature (Celsius, 15-59) | norm, raw | HGST norm 253 on 2,453 rows (vendor scale) | fine | CLEAN-14
195 | Hardware ECC Recovered (Seagate packed) | norm, raw | packed as shipped | fine, note | CLEAN-12
196 | Reallocation Event Count | norm, raw | ok | fine | -
197 | Current Pending Sector Count (counter; Backblaze rule) | norm, raw | ok | fine | USE-6
198 | Offline Uncorrectable (counter; Backblaze rule) | norm, raw | ok | fine | USE-6
199 | UltraDMA CRC Error Count | norm, raw | ok | fine | -
200 | Multi-Zone / Write Error Rate | raw | ok | fine | -
201 | Soft Read Error Rate / TA counter (SSD) | norm, raw | 549 rows, boot | fine | -
202 | Data Address Mark errors / SSD life used (Micron) | norm, raw | boot only | fine | -
206, 210, 211, 212, 218 | SSD vendor-specific (Micron, Seagate SSD) | raw | boot only (23 to 11,630 rows) | fine | -
220 | Disk Shift (Toshiba) | norm, raw | ok | fine | -
222 | Loaded Hours (Toshiba) | norm, raw | ok | fine | -
223 | Load/Unload Retry Count (Toshiba) | norm, raw | ok | fine | -
225 | Load/Unload Cycle Count (older Samsung-made HDD) | norm, raw | 407 rows, boot | fine | -
226 | Load-in Time (Toshiba) | raw | ok | fine | -
230 | SSD media wear / life status (WD SSD) | norm, raw | boot only | fine | -
231 | SSD Life Left / temperature (vendor) | raw | ok | fine | -
232, 233, 234, 235 | SSD endurance / media wear / vendor counters | 232 and 235 norm, raw; 233, 234 raw | boot only | fine | -
240 | Head Flying Hours (Seagate) | norm, raw | 65535 on 6 ST8000NM0055 rows (same drives as smart_9 = 65535): sentinel | fine; -> missing optional | CLEAN-10
241 | Total LBAs Written | norm, raw | norm 253 on boot WD SSDs | fine | -
242 | Total LBAs Read | norm, raw | norm 253 on boot WD SSDs | fine | -
244 | SSD vendor-specific | norm | 1,939 rows, boot | fine | -
245 | SSD vendor-specific (Micron/Intel boot SSDs) | norm, raw | norm == raw on all 549 rows: exact copy | CLEANING: drop one (vanishes with boot drives) | CLEAN-5
246, 247, 248 | Micron SSD host/FTL write counters | raw | boot only | fine | -
252 | vendor-specific (Samsung SSD) | raw | 5 rows | fine | -
254 | Free Fall Protection | norm | boot HDDs only | fine | -

**PROBLEMS, RANKED (principles.md: P4 before P7, Must before Should, then effect size)**

A. P4, LEAK-10 (Must), new. pod_slot_num goes empty when the replacement process takes the drive out of service.
   Evidence.
   - Data drives (capacity > 2.2 TB) without a slot at the cut: 6,184 rows of the full frame, 369 positives
     (5.97%, against 0.100% with a slot: 60 times the rate). Shipped frame: 2,653 rows, 169 positives; the three test
     windows: 1,510 rows, 115 of the 1,262 test positives (9.1%); 24% and 39% of such rows are positive in March and
     April 2026.
   - The slot is lost right before the failure record: of the 369 positive rows, 349 drives have an earlier cut, 302
     of them had a slot then, all 349 in the same vault. Daily files Q4 2025 to Q2 2026, 3,438 failed drives that ever
     had a slot: the slot is empty on 69% of failure-record days, 14.5% one day before, 10.4% at 5 days, 8.5% at 10,
     5.3% at 20, 3.5% at 30 and 40 days. The last day with a slot is 0 or 1 day before the record for 75% of drives;
     about 20% lose it 2 to 30 days before.
   - On slot-empty days the drive is idle, out of the data path: median LBAs read per day 0.04M (drives that do not
     fail) and 0.17M (drives that fail) against 340M to 460M with a slot; 9% of the failing drives' slot-empty days
     have no SMART at all. So the empty slot marks a drive already taken out of service, mostly as the first step of
     its replacement (the label's own event). Not every empty slot is the outcome: whole vaults lose their slots for a
     cut or two (iad1 vault 1040, 20 pods x 120 rows, 0 positives), which is a label-free reporting gap.
   - Worth, regularised LightGBM as in rule_vs_model.py, 1M training rows, May / April / March 2026:
     ROC AUC with pod_slot_num 0.9041 / 0.9047 / 0.8882, without 0.9059 / 0.9020 / 0.8877 (-0.002, +0.003, +0.001);
     average precision 0.129 / 0.151 / 0.105 against 0.109 / 0.134 / 0.088 (+0.017 to +0.020, 15-20% relative).
     The indicator alone scores ROC AUC 0.541 to 0.550 (below the leak probe's 0.55 flag, so no probe saw it).
   - The 27 data-drive rows with every SMART value missing (15 positive) are the same state: 26 of them have no slot.
   Strength: weak under the declared roc_auc, clear at the top of the ranking. LEAK-5: the score is no argument; the
   field is a consequence of the target's process, which LEAK-10 puts out.
   Remedy (mildest first, LEAK-7):
   (a, recommended) Drop the rows of data drives whose pod_slot_num is empty at the cut: a label-free rule; these
       drives are already out of service, so the monthly review has no decision to make on them (USE-1, USE-7). It
       keeps pod_slot_num as a position, takes the 26 SMART-less rows with it, and removes the whole-vault gaps too
       (outcome-free, a small cost). 2,653 shipped rows, 169 positives; the counts in the notes and the decision table
       change.
   (b) Drop pod_slot_num. Cheaper, loses a feature of no measured worth (flat per-slot rates), but leaves the
       already-out-of-service rows in, unmarked except the 26 SMART-less ones.
   Either way, add a bullet (Backblaze does not document an empty slot; the reading is ours, from the daily files).

B. P4, LEAK-25 / LEAK-22 (Must), new; changes the builder's issue 5. Boot drives cannot be positive in this release.
   Evidence: boot drives (capacity <= 2.2 TB: SSDs and 250-500 GB disks) have 31 failure records in Q4 2024 and none
   from 2025-01-01 to 2026-06-30 (presence.parquet: every drive-day; 32 small-capacity failure records in all, the
   other one a capacity -1 data drive). In the full frame 67,314 boot rows, 0 positives; shipped 24,845 rows (1.2%),
   11,671 of them in the test windows (3.4% of test rows), all No. 388 of 4,296 boot drives leave the files before
   June 2026 without any failure record, so they are replaced or removed, but no longer recorded as failures. The
   definition's "boot drives ..., which the operator replaces too" holds, but the label cannot see it: their No is
   "not recorded", and model, capacity and the empty pod_slot_num identify them for free.
   Remedy: drop the boot drives by a label-free rule (capacity_bytes <= 2.2e12, or the model list), the builder's
   option 5B. This also empties most SSD-only SMART columns (11, 13, 16, 17, 165-183, 201-218, 225, 230-235, 244-254),
   which the definition's constant/empty check then drops. Update the README's row count, the 1.2% note and issue 5.

C. P7, CLEAN-19 (Should, a weighing call), builder's issue 3: change features over the 30 days before the cut.
   My reading: this is the rule's third case, a daily log aggregated to one row per prediction, and the published
   practice on this data and on the PAKDD 2020 challenge builds windowed changes of the SMART counters. The notes'
   argument "the counters are cumulative, so the snapshot already carries the drive's history" holds for the level,
   not for the recent rate (new reallocations this month), which is what a fleet team reads. The measured gain is
   small and mixed (+0.007, +0.010, -0.002, one seed) and is no reason either way (decide from context).
   Caveat if built: the usage counters (smart_9, 240, 241, 242) can carry the same out-of-service state as finding A;
   measured weak here (smart_242 7-day change below 1e8: 17,194 rows, 69 positives, 0.40% against 0.12% base), so
   build changes of the error counters (1, 5, 7, 184, 187, 188, 189, 197, 198, 199, 200, ...) or blank the usage
   counters' changes on rows whose slot is empty. Curator's call; I lean to B (build them), with that caveat.

D. P7, CLEAN-5 (Should). smart_245_normalized equals smart_245_raw on all 549 non-missing rows (boot SSDs): drop one.
   Goes away with B. smart_190_normalized = 100 - smart_190_raw on every row: a copy under a fixed transform, not an
   exact copy; keeping it is fine, dropping it is harmless.

E. P7, CLEAN-11 / CLEAN-10 (Should), cheap. Impossible and sentinel values, all tiny:
   - smart_9_raw = 0 on 137 shipped rows (282 full, 1 positive) of drives years old; smart_9_raw = 65535 on 10 and
     smart_240_raw = 65535 on 6 ST8000NM0055 rows: set to missing.
   - smart_1_raw = 2^32-1 (10 rows) and smart_13_raw = 2^48-1 (1 row), boot SSDs: missing (moot after B).
   - Normalised 252 on every attribute of ST500LM012 HN / ST1000LM024 HN (407 rows, boot): "no value", moot after B.
     HGST normalised 253 on smart_3 (251 rows) and smart_194 (2,453 rows) is the vendor's scale: keep.
   - smart_187_raw = 65535 (27 Seagate rows) is a saturated counter, a real value: keep.

F. P7, CLEAN-12 / CLEAN-1 (Weigh, note only). Seagate's raw smart_1, 7, 188, 195 (and 240-242 on some models) are
   bit-packed fields (smart_188: three 16-bit counters; smart_7 and smart_1: error count in the upper 16 bits over an
   operation count). Backblaze's own analyses and the five-counter rule read them as shipped, and > 0 is unchanged by
   the packing. Keep as shipped; a sentence in the notes would help a reader.

G. Questions for the curator (no change proposed).
   - model: "WUH721816ALE6L4" against "WDC WUH721816ALE6L4" (see table): keep both, they differ in what they report.
   - pod_slot_num as a number while pod_id is a category: defensible (a slot is a physical position, nearby numbers
     nearby slots; a pod is one of 20 servers with no adjacency). The slot numbering depends on the server type
     (Backblaze 45/60, Dell 26, Supermicro 60); the frame holds 0-59 only. Moot under remedy A(b).
   - cluster_id: Backblaze says it "is not always correct"; worth a note.

Not problems (checked)
- Every SMART value, model, capacity, datacenter, cluster, vault and pod is the cut day's reading, before the 30-day
  window; cut-day failures are dropped. No field other than pod_slot_num's missingness (and the 26 SMART-less rows
  that share it) is written by the replacement process: the builder's 1-7 day against 8-30 day split (0.900-0.904
  against 0.883-0.904) shows no extra signal close to the record, and the idle signature lives in daily changes,
  which the snapshot does not ship.
- Power-on hours (smart_9_raw) at the cut is the drive's age, read before the outcome, not a span the outcome ends
  (LEAK-10 span clause does not apply; LEAK-37). No unit mix across models.
- Normalised SMART values are each vendor's per-drive scale, not statistics over rows (LEAK-29, LEAK-30 hold).
- No training weight, so LEAK-41 / probe 22 do not apply.
- Very sparse SSD-only columns (5 to 18,021 non-missing rows) stay under CLEAN-22; most leave with B anyway.

Sources: Backblaze Drive Stats for Q3 2023 (https://www.backblaze.com/blog/backblaze-drive-stats-for-q3-2023/;
field definitions, cluster_id caveat, server types); Q2 2023 post (vault_id, pod_id); Q3 2024 post (proactive and
reactive failures, failures revised after testing); the data page and Drive_Stats_Schema_Current.csv (names only).

</details>

<details><summary>Split audit</summary>

Split auditor report: backblaze_hard_drive_failure_1m (record backblaze_hard_drive_failure), 2026-11-09

VERDICT: right with notes.
Temporal, monthly, known drives: this matches the use case, an operator scoring its own fleet on the first of each
month (USE-10, SPLIT-3, SPLIT-13). The windows, the train shares, the gap against the 30-day label and the history all
hold, checked against the shipped splits (the participant kit's splits) and against the daily files. Two notes go to
the curator. Neither changes the regime.
  (1) Builder issue 4. Dropping the drives removed without failure is selection on the future. LEAK-22 (the
      framingham precedent) keeps such rows as No. Measured, the choice moves the test ROC AUC by at most 0.0006.
  (2) A new finding. The cohort "reporting on the cut day" leaves out 187 drives across the three test windows that
      were in service in the week before the cut and failed within 30 days. That is 119 of them in April 2026, against
      505 positives kept. The cohort is known at the cut, so this is no leak. It changes what the test stands for,
      and it should be said in the notes.

Judgment record
Validity: SPLIT-1, SPLIT-2, SPLIT-3 hold (temporal, known entity); SPLIT-9 / LEAK-12 hold (no training label
unknown at the refit, no shortcut through a test drive's own label); SPLIT-10 holds (gap 29 days = the 30-day
label); SPLIT-11, SPLIT-14, SPLIT-15 hold (expanding, 3 windows, 75.3% / 87.5% / 93.7%); SPLIT-12 holds (refit
cadence 1 month + PAKDD 30-day horizon); SPLIT-13 / LEAK-34 hold (98.2-98.8% of test drives known, serial dropped);
SPLIT-20 holds (15-16 months of history, the atypical months in training); LEAK-22 triggered by the drop of removed
drives (effect <= 0.0006 AUC), curator's call.
Value: unaffected (327-505 test positives per window, about 1,000 per train side).
For the curator: issue 4 (keep removed drives as No, or record an exception); a note on drives missing from the
cut-day file.

**1. Regime (SPLIT-1, SPLIT-3, USE-10, SPLIT-13)**

Use case: a data-centre team reviews its fleet on the first of each month. These are known drives in a stream over
time, so the split is temporal, with the drive's own history allowed.
Measured on the kept rows (labelled_explore.parquet, the shipped 5,547,634 rows with serials; e2_recur.log):
  window      test drives with earlier rows   (positives)   mean earlier rows   new drives (pos, rate)
  2026-05-01  98.26%                          (99.53%)      14.7                6,111 (2, 0.033%) vs known 0.124%
  2026-04-01  98.15%                          (99.41%)      14.0                6,368 (3, 0.047%) vs known 0.148%
  2026-03-01  98.75%                          (98.78%)      12.2                4,258 (4, 0.094%) vs known 0.096%
- A grouped split by drive would test a cold start that the operator never faces. Only 1-2% of each month's drives
  are new, and they fail less often. Temporal is the right regime. I did not fit a grouped alternative: the use case
  rules it out (SPLIT-4: the size of the gap never decides).
- LEAK-34: the serial is dropped, so no model can look up a drive's earlier labels. A failure ends a drive's rows, so
  a test drive's earlier training rows are all No, except 20 test rows per window whose drive had an earlier positive
  row. These are among the 81 serials seen again after a failure record. None of the 20 is positive in its test month.
  No label is carried across the cut.
- Slot history (a proxy for a drive id: datacenter, cluster, vault, pod, slot) is no shortcut either. A test drive
  in a slot whose earlier occupant failed fails at 0.249% / 0.115% / 0.077% against 0.121% / 0.147% / 0.096% for the
  other drives (May / April / March). The sign is inconsistent, and the operator has this history anyway.

**2. Time column, windows, train side (SPLIT-11, SPLIT-12, SPLIT-14, SPLIT-15)**

- `cut_date` is the snapshot day, which is the prediction point. Features are that day's readings only. The label
  covers (cut, cut+30 days]. Each test window is one calendar month holding one cut day.
- Shipped splits (verified; same numbers as the claim auditor's t2_splits.log):
  window      test rows  test pos  train rows  train pos  train cuts  last train cut  full eligible pool (share)
  2026-05-01  350,349    430       1,000,000   1,038      16          2026-04-01      5,197,285 (93.7%)
  2026-04-01  344,784    505       1,000,000   1,008      15          2026-03-01      4,852,501 (87.5%)
  2026-03-01  339,651    327       1,000,000   1,024      13          2026-01-01      4,175,253 (75.3%)
  No train/test overlap. The 1M sample keeps every cut in proportion: the largest deviation in a cut's share is
  0.0005. Expanding: SPLIT-11 holds. Three windows, all above the 50% floor: SPLIT-14 and SPLIT-15 hold.
- Horizon (builder issue 2). One month is the refit cadence, and 30 days is the PAKDD 2020 horizon. SPLIT-12 is met.
  The 90-day option needs quarterly cuts and an 89-day gap. With six cuts in the download, it cannot give three
  windows above the floor. Option A stands.
  A mild alternative, not needed: define the label as "fails before the next review" (28 to 31 days). Every window,
  March included, could then train on the month before it. Today the March window loses February: Feb 1 + 30 days =
  Mar 3, after the cut. This is the correct simulation of a fixed 30-day label, not a defect.
- Spacing and season (SPLIT-20; SPLIT-21 respected, so no window choice from scores). The three newest months
  (March to May 2026) hold 0.096%, 0.146% and 0.123% positives: the 8th, 1st and 3rd highest of the 17 cuts. The
  months whose labels are odd are all in training. These are the firmware pulls of July to September 2025 and the
  holiday dip of December 2025 (124 positives, 0.037%). Drive failures have no strong seasonal cycle, and the odd
  months come from how drives were handled, not from the season. So the newest windows are not an atypical season.
  Spacing the windows (step=3: May 2026, February 2026, November 2025) would train on 93.7%, 75.3% and 57.1%. It is
  a possible variant covering winter, not required. With step=4, the oldest window falls below the floor (45.2%).

**3. Gap against the 30-day label (SPLIT-9, SPLIT-10, LEAK-12)**

- The declared gap is 29 days. Training cuts lie strictly before the test cut minus 29 days, so every training cut
  plus 30 days falls on or before the test cut. Checked on the shipped splits (gap_ok on all three). Every training
  label, and the removed-without-failure flag of every training row (last seen before cut+30), is known at the refit.
- Edge: the last training cut of the April and May windows has its label window end on the test cut day itself. A
  failure record on that day is in the same daily file the test features come from. That drive is also dropped from
  the test window (`fails_on_cut`: 14 rows in April, 31 in May), so no test row's own outcome is in training.
- No shortcut (SPLIT-9): no training label of a test drive was set after the test cut (see section 1).

**4. Drives removed without failure (builder issue 4; LEAK-22 against LEAK-23)          [P4, Must; effect negligible]**

Evidence (e1_removed.log). A regularised LightGBM fit on each shipped train side: 800 trees, 15 leaves, min_child
500, colsample 0.3, lambda 5, cut_date not used. The rows dropped as "removed in the horizon" were rebuilt from
snapshots.parquet and added to the test as No:
  window      removed  AUC shipped  AUC with removed as No  removed: median percentile among test negatives
  2026-05-01  151      0.9127       0.9127                  71st  (6.6% in the top 1%, negatives 0.9%)
  2026-04-01  940      0.9123       0.9124                  16th  (836 are ST8000DM002, 19 vaults)
  2026-03-01  1,102    0.8876       0.8870                  96th  (804 HGST HUH728080ALE600 + 172 HMS5C4040BLE640)
Reading:
- The rule. The builder cites LEAK-23, which covers follow-up cut by one date (the release end). That is not this
  case: here follow-up ends by an event, removal from service, after the prediction point. LEAK-22 covers this case.
  A competing event after the prediction point keeps its row with the label No. The reason given: "dropping it
  selects the cohort on the future" (framingham_heart_study_fhs, Lennart, 2026-10-22).
- Backblaze's own definition backs label No: drives removed for other reasons are not failures (Klein, 2016). The
  drop applies to negatives only.
- Old drives retired in vault migrations rank high (March: 96th percentile). Keeping them as No is the harder test,
  but the score moves by at most 0.0006.
- A fact that could set this case apart: a vault migration is planned before the cut, so the operator knows at the
  cut which drives will leave. The release does not record that plan. Dropping on the realised removal therefore
  stands in for it with future information.
Mildest remedy: (B) keep them as No. This is a one-line change to the filter in `_clean` and `_decisions`; the test
rows grow by 151 / 940 / 1,102. Or keep (A) and record an exception to LEAK-22 that names the planned migration as
the fact and gives the measured effect (<= 0.0006 AUC). Either way the ranking cannot move. This is a consistency
call for the curator.

**5. New: drives in service but missing from the cut-day file (cohort of the test windows)      [P3/P4 note, no leak]**

A row exists only for a drive with a reading on the cut day. Drives in service in the week before the cut, missing
on the cut day, and not failed before it fail at a very high rate (e3_absent.log, all 17 cuts). Among those back
within 7 days, 0.6% to 45% fail in 30 days, against a 0.1% base rate. April 2026 is the extreme month: 111 of 375
returning drives fail.
Evidence (e4_absent_scored.log). Each missing drive was given its last reading in the 7 days before the cut, labelled
like the shipped rows (removed-without-failure dropped), and scored by the same model:
  window      missing drives  their positives  kept positives  AUC shipped  AUC with them added  AUC within them
  2026-05-01  587             43               430             0.9127       0.9204 (+0.008)      0.966
  2026-04-01  550             119              505             0.9123       0.9271 (+0.015)      0.905
  2026-03-01  621             25               327             0.8876       0.8952 (+0.008)      0.935
The missing positives rank at the very top: median 100th percentile among the test negatives, against 99.1-99.4%
for the kept positives. 187 of 1,449 failing drives over the three windows (13%) are outside the test, and 19% in
April.
Reading:
- This is no leak and no split error. Whether a drive reports on the cut day is known at the cut, and train and test
  use the same cohort. These are most likely drives that drive sentinel has already cut off, or that are under
  service ("their data is no longer logged" for failed drives).
- The operator already acts on these drives without a model, so leaving them out can be argued from the use case:
  the review ranks the drives still working. But it should be said. The test score omits the most obvious failures,
  and the share omitted swings between months (25 to 119).
Mildest remedy: a sentence in `curation_comments` and the notes with these counts. The alternative is an as-of row
(the last reading in the 7 days before the cut, plus the days since it). That is a change of the row definition, the
curator's call. It is not needed for an honest split.

**6. History start (SPLIT-20)**

- Training starts January 2025. That gives 13 to 16 monthly cuts, at least one full year before each window. The
  months with odd labels (firmware pulls Q3 2025, holiday dip December 2025, vault migrations March 2025 and January
  2026) all fall in training, where they are label noise as published (documented).
- Data back to 2013 exists. The 1M budget already takes only 19% to 24% of the eligible drive-months, so a longer
  history would mostly thin out the recent months the refit relies on. The model mix (85 models, 74 to 81 per cut)
  is stable over the span. No change is needed.

Files: (the run's work files).
All runs used thread caps of 4, and stayed under 30 GB. One model per window, one seed: the
deltas are indicative.

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Actor: a reliability engineer of a cloud-storage operator. At each monthly cut I rank every drive in the fleet by its
risk of being replaced as failed in the next 30 days, and I take the top of the list for proactive cloning/migration
and spare/technician planning. My budget is a number of drives per month, not a threshold.

VERDICT
- Fit: APPROXIMATE (agree with the builder). One-sentence reason: rows, inputs, the cut and the monthly test window
  mirror my fleet review, but the label is Backblaze's replacement ticket, about half of which are the operator's own
  proactive pulls on an unpublished error threshold, and one sub-population (boot drives) can never be positive.
- Metric: PARTLY scores my decision. A ranking metric is right (my k moves with technician capacity, so no single
  threshold, MET-6, MET-7), but ROC AUC weighs the 99% of the ranking I never act on. Measured: ROC AUC and the
  top-of-list metrics pick different models (below). I would choose recall of next month's failures in the top 0.5% of
  the fleet (or TPR at a false-alarm rate of at most 1%, the disk-failure literature's operating point); under MET-7
  and MET-9 no k is fixed by the source, so roc_auc stays rule-consistent unless the curator takes a MET-11 `context`
  metric.
- New finding (rank 2 below): boot drives are structural negatives. 0 of 6,879 failure records in Q1 2025 to Q2 2026
  fall on a boot-drive serial; 67,620 boot drive-months (1.2%) carry 0 positives, while 306 of them (0.45%, three times
  the data drives' 0.16%) leave the files without a failure record and are dropped as censored. Draft issue 5's reason
  ("the operator replaces them too") does not hold for this label. Recommend option B (drop boot drives).

1. INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
Have them all at the cut: model, capacity, datacenter/cluster/vault/pod/slot, and the cut day's SMART raw and
normalised values; cut-day failures are removed and nothing after the cut is used. No input I would NOT have.
Missing inputs I would always have:
- The drive's recent trend (new pending/uncorrectable sectors this week, the 7/30-day change of each counter).
  Backblaze's "main indicator ... if a drive should be replaced" is new uncorrectable medium errors on reads (Q3 2025
  post); a cumulative snapshot shows them only as a level. The builder measured +0.007, +0.010, -0.002 ROC AUC
  (draft issue 3); small and mixed, so option A is defensible for a benchmark, but every fleet tool I know looks at
  the trend. Weak preference for B; not a blocker.
- Drive sentinel's read/write error counts and the file-system checks that trigger the proactive pulls: internal to
  Backblaze, not published, cannot be added. This is why the label is only partly explained by SMART (21-28% of
  positives have all five counters at zero).
- Pod-level history (recent failures in the same pod/chassis, earlier repairs of the drive). Derivable from earlier
  labels, not built; the location IDs stand in. Lu et al. (FAST 2020) found location helps; here a model without the
  location columns scored ROC AUC 0.905/0.914/0.896 vs 0.904/0.904/0.887 with them, so the IDs as categories add
  nothing at this size. No change needed.

2. TARGET (USE-5, USE-8)
- What I act on is "this drive will need a replacement ticket soon" (for spares and technician time) and, behind it,
  "this drive will lose data" (durability). The label is the first exactly: Backblaze counts a failure when the serial
  is the primary serial of a drive-replacement Jira ticket (Q3 2025 post). Replacement as ground truth is the field's
  standard (Schroeder & Gibson, Pinheiro et al., Botezatu et al. all use replacement logs). For durability it is a
  proxy: a proactive pull on day 3 is a positive whether or not the drive would have died.
- The circular part: about half the positives follow Backblaze's own threshold on errors that partly show in SMART
  187/197/198. The model partly learns the operator's own trigger, but it ranks 1-7-day failures no better than
  8-30-day ones (0.90 vs 0.88-0.90), so it is not just reading drives already past the trigger. I agree with draft
  issue 1, option A, approximate.
- Label noise I would also see in production: the Toshiba MG08ACA16TEY "cosmetic" firmware pulls (training only) and
  the December holiday dip. A policy change at the operator changes the label; that is the main reason I would
  re-validate the model every month.
- I want a probability/score to rank drives (a class at 0.5 is useless at 0.1% prevalence). Binary target fits.

3. ONE ROW = ONE DECISION; TEST = WHAT I FACE (USE-10, SPLIT-12/13)
- One row = one drive at one monthly review: yes. One test window = one cut of the whole fleet: exactly my review.
- Test drives are known drives with history in training (99.2% vault, 100% model seen): yes, I score my own fleet.
- 30-day horizon: fits a monthly planning cycle (PAKDD 2020 also used 30 days). Day-to-day proactive cloning runs on
  shorter horizons (Lu et al. FAST 2020: 10 days), but a monthly review with 30 days is a real cadence. Draft issue 2
  option A: agree.
- Removed without failure (draft issue 4): 8,361 of the 8,568 data-drive removals fall in vault blocks of 20+ drives
  on the same cut, i.e. planned migrations I would know at the cut and would not score. Dropping them (A) matches
  what I do. The 207 isolated removals could be pulls later found healthy ("considered failed until it shows up
  again"); too few to matter.
- Boot drives (draft issue 5): see the verdict. Backblaze itself reports them apart (Q3 2025: 3,970 boot drives,
  328,348 data drives) and does not record their failures as failures in these files: 0 failure records in 18
  months, where an AFR near 1% would give dozens. Their failures leave as removals and are dropped. Keeping them adds
  67,620 easy negatives (identified by model/capacity) and slightly inflates ROC AUC; it also states a claim the data
  contradicts. Drop by model/capacity (option B), or keep and rewrite the reason as "kept as structural negatives".

4. WOULD I USE IT?
Yes, as a ranked watch list. Measured (one 1M random training sample per window, regularised LightGBM, as the
builder's probe): flagging the top 0.5% of the fleet (~1,700 drives) catches 39-43% of next month's failures vs
15-19% for Backblaze's five-counter rule; the top 0.1% (~350 drives) catches 18-20% (precision about 24% in May) vs
6-9%. That is worth a proactive cloning programme. Trust would come from stable recall at my budget across months and
on the zero-counter drives (model AUC only 0.67-0.73 there). Distrust: the label follows replacement policy, so a new
firmware campaign or sentinel threshold shifts it.

5. METRIC (MET-1, MET-6 to MET-9)
Declared: roc_auc, fallback. My decision: a fixed number of drives per month (top k of the ranking).
Measured on the three test windows (the run's work files), four candidate
models plus the rule:
  model                ROC AUC (May/Apr/Mar, mean)        recall top 0.5% (May/Apr/Mar, mean)
  lgbm 1500 trees      0.904 / 0.904 / 0.887  0.898       0.421 / 0.434 / 0.394  0.416
  lgbm 300 trees       0.910 / 0.914 / 0.886  0.903       0.395 / 0.432 / 0.349  0.392
  lgbm no location     0.905 / 0.914 / 0.896  0.905       0.402 / 0.422 / 0.398  0.407
  lgbm five+model      0.894 / 0.906 / 0.886  0.895       0.356 / 0.384 / 0.346  0.362
  five-counter rule    0.840 / 0.876 / 0.825              0.188 / 0.186 / 0.153
- ROC AUC ranks the 1500-tree model third of four; recall at the top 0.5%, recall at the top 0.1% (0.198/0.184/0.183
  vs 0.177/0.176/0.174 for 300 trees) and average precision (0.127/0.151/0.105 vs 0.113/0.146/0.088) rank it first
  in every window. In March the five-counter model ties the full model on ROC AUC (0.886 vs 0.887) but catches 18 fewer
  of 327 failures at the top 0.5%. Log loss follows ROC AUC here (0.00648 vs 0.00657 in May).
- The differences are a few drives per window (one positive = 0.002-0.003 recall), so this is a direction, not proof;
  but the direction is consistent: ROC AUC rewards ordering the 99% of healthy drives I never touch.
- What I would choose: recall (detection rate) in the top 0.5% of each cut's fleet, a k scaled to the fold as
  coil_2000 does (MET-2), or TPR at a false-alarm rate of at most 1% / partial ROC AUC up to FPR 1%. Disk-failure
  prediction has reported detection at a fixed low false-alarm rate since Hughes et al. 2002 (0.2% FAR) and Murray et
  al. 2005. Against it: Backblaze fixes no k (MET-7 forbids inventing one), and MET-9 rules out PR AUC on imbalance
  alone. So: roc_auc is rule-consistent; a `context` metric (MET-11) on the operating range is the curator's call.
  Answer: PARTLY.

WHAT AN EXPERT WOULD CHANGE (ranked by how much it changes the task)
1. Drop boot drives (structural negatives, failures recorded as removals). Draft issue 5 -> B, or rewrite the reason.
2. Name the metric gap in the README: the actor acts on the top ~0.1-1% of the fleet; offer the curator a `context`
   metric (recall at top 0.5% per cut, or partial AUC to FPR 1%) with the numbers above; keep roc_auc otherwise.
3. (Optional) Add the 7/30-day change of the raw error counters (draft issue 3, B): what every operator looks at,
   though the measured gain is small.
4. Keep: 30-day horizon with monthly cuts, removals dropped, label as published with fit approximate (draft issues
   1, 2, 4 -> A).

RULES CITED: USE-3, USE-5, USE-6, USE-8, USE-10, SPLIT-12, SPLIT-13, LEAK-23, MET-1, MET-2, MET-6, MET-7, MET-8,
MET-9, MET-11.

SOURCES
- Backblaze, Hard Drive Data and Stats: https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data
- Backblaze Drive Stats Q3 2025 (failure = primary serial of a drive-replacement Jira ticket; "considered failed until
  it shows up again"; uncorrectable medium errors as the main replacement indicator; drive sentinel thresholds;
  cosmetic firmware failures; 3,970 boot vs 328,348 data drives):
  https://www.backblaze.com/blog/backblaze-drive-stats-for-q3-2025/
- Backblaze Drive Stats Q3 2024 (reactive vs proactive, about half each), via the record:
  https://www.backblaze.com/blog/backblaze-drive-stats-for-q3-2024/
- Backblaze, Using Machine Learning to Predict Hard Drive Failures (Backblaze "doesn't need it to be" perfect;
  30/60/90-day horizons tested): https://www.backblaze.com/blog/using-machine-learning-to-predict-hard-drive-failures/
- Lu et al., Making Disk Failure Predictions SMARTer!, FAST 2020 (380k drives, location/workload, 10-day horizon):
  https://www.usenix.org/conference/fast20/presentation/lu
- Murray, Hughes, Kreutz-Delgado, JMLR 6 (2005): https://jmlr.org/papers/v6/murray05a.html ; Hughes et al. 2002,
  Improved disk-drive failure warnings (detection at 0.2% false-alarm rate).
- PAKDD 2020 Alibaba AI Ops challenge (30-day horizon), via the record and dataset.py.
- Own measurements: (the run's work files), run on the warehouse's snapshots/failures/last_seen parquet files.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: backblaze_hard_drive_failure (target fails_within_30_days, binary, temporal on cut_date)
Inputs used: clean_room/data.parquet (200k-row sample of 2,104,715), clean_room/task.md, public web. No other local files opened.
Scratch script: (the run's work files).

VERDICT: Include with changes. It is a real, well-known fleet-operations task with real data and clear non-trivial signal, but the
train/test months are built from different sampling rates without saying so, the label horizon runs past the train/test boundary,
and the column set needs cleaning.

WHAT THE TASK IS
On the 1st of each month, take one SMART snapshot per drive in Backblaze's fleet (model, capacity, location, and about 120 SMART
normalized/raw attributes). Predict whether the drive will be logged as failed in the next 30 days. A storage operator would use this
to schedule proactive replacement, data migration, or spares. This is a real use, and it is the textbook use of the Backblaze Drive Stats data.
cut_date has 17 monthly values, 2025-01-01 to 2026-05-01, all on day 1. Backblaze currently publishes data through Q2 2026, so the
30-day labels for the 2026-05-01 cut can be computed.
Positive rate is 0.10% (209 of 200,000 in the sample, so about 2,000 in the full data). The monthly rate ranges from 0.013% to 0.19%.

SIGNAL CHECK (sample only; LightGBM, 300 trees; trained on all earlier months, tested on each of the last 3 months)
  test 2026-03: AUC 0.817, AP 0.043 (base rate 0.0009, 29 positives)
  test 2026-04: AUC 0.868, AP 0.092 (base rate 0.0012, 41 positives)
  test 2026-05: AUC 0.818, AP 0.082 (base rate 0.0014, 45 positives)
For comparison, the sum of the five Backblaze "critical" SMART raw counts (5, 187, 188, 197, 198) gets AUC 0.78-0.89 but AP only 0.009-0.020.
So the model adds real ranking value over the rule. The task is not trivial and not hopeless.

CONCERNS, MOST TO LEAST SERIOUS

1. The sampling rate changes between train and test months, and nothing documents it.
   Rows per month in the sample: 6,629-7,806 for 2025-01..2026-02, then 32,149 / 32,856 / 32,908 for 2026-03/04/05.
   Scaled to the full data, that is about 73k drives per month versus about 340k. Backblaze reports a fleet of about 333k drives
   (Q3 2025 post: "fleet total of 332,915"). So the last three months are the whole fleet, and the earlier months are about a 22% subsample.
   The datacenter, cluster and model mix is the same before and after the change (for example phx1 is 31.8% vs 31.7%).
   So it looks like an undisclosed subsample of the training months. task.md does not mention it.
   It is not leakage. But the test windows hold about half of all rows, and it is unclear whether the subsample was drawn per drive or per row.
   A per-drive draw would put the same roughly 22% of drives in every training month.
   Change: document the scheme, or subsample every month the same way. If kept, state that train months are a random 22% of drives.

2. The label horizon crosses the train/test boundary, so an embargo is needed.
   The label for cut 2026-02-01 covers failures up to 2026-03-03, which is after the 2026-03-01 test cut.
   A drive that fails on Mar 1-3 is positive in both a training row and a test row, and that training label could not be known on Mar 1.
   The effect is small (about 2 of 30 days of one month's positives), but it is a real look-ahead.
   Change: train each test window only on rows with cut_date + 30 days <= the test cut_date. That means dropping the immediately preceding month.

3. Part of the label is defined by the features (circularity). This is acceptable but should be stated.
   Backblaze counts a drive as failed when it is pulled and replaced, including proactive pulls. Its Q3 2025 post says the main replacement
   trigger is "uncorrectable read errors, reported through SMART attributes such as Current_Pending_Sector". The older SMART post lists
   SMART 5, 187, 188, 197 and 198 as the attributes used.
   In the data, 66.5% of positives have a nonzero value in one of those five attributes, against 7.9% of negatives.
   Using that flag alone gives AUC 0.79 on the pooled sample.
   So the task is partly "predict Backblaze's own replacement rule". That is still what an operator wants to forecast, and AP shows room
   above the rule. Benchmark users should know about it.

4. The label is noisy and censored.
   The same Q3 2025 post says Toshiba drives pulled for a firmware issue were counted as failed: "we had an abnormal number of 'failed'
   drives in this population", and these failures were not mechanical.
   A failure is a drive "vanishing" plus a replacement ticket. Drives that are migrated or decommissioned inside the window are presumably
   labelled No, but I could not verify this.
   In the sample, 35/65 Toshiba positives (54%) vs 101/144 others (70%) have nonzero critical SMART counts, which fits some
   non-SMART pulls. This is noise, not a fatal problem.

5. Each drive appears many times, and there is no drive ID.
   Each operating drive appears once per month, up to 17 times, with no serial number.
   Training rows are therefore heavily correlated, and test drives are mostly the same physical drives already seen in training (as negatives).
   Under a forward-in-time split, the drive's own past is legitimate knowledge, so this is not leakage. It does mean the effective sample
   is much smaller than 2.1M.
   There are also no history features (deltas, 7- or 30-day trends), which a real deployment would use. The snapshot-only framing is
   acceptable for a benchmark.

6. Positives are scarce, and the score metric matters.
   There are about 2,000 positives in total. Per test window, the full data should have roughly 300-450.
   ROC AUC alone saturates differences. Use log-loss and/or average precision, and expect high variance between windows.
   The positive rate also drifts (Jan 2026 sample: 1 of 7,806; May 2026: 45 of 32,908).

7. Column preparation.
   - 11 columns are constant or entirely NaN in the sample: smart_10_raw, 13_norm, 27_norm, 82_norm/raw, 175_raw, 179_norm, 183_norm,
     211_raw, 212_raw, 252_raw. About 40 more are more than 99% missing.
     These are vendor-specific attributes; missing means "not reported by this model", so the missing pattern encodes the drive model.
     Drop the constant ones and consider dropping the more-than-99.5%-missing ones.
   - Boot and OS devices are mixed in with storage drives, and Backblaze reports them separately.
     In the sample: DELLBOSS VD, Seagate BarraCuda SSD, CT250MX500SSD1, and so on, about 1,800 rows with 0 positives; 2,403 rows have
     capacity below 1 TB. The 61 exact duplicate rows (ignoring cut_date) are all DELLBOSS VD rows with no SMART data at all.
     Change: drop boot drives (DELLBOSS, SSD models), or at least drop the rows with no SMART data.
   - vault_id is a 257-level category and is the top LightGBM feature (12% of gain); pod_slot_num is third (8%).
     The location IDs probably capture batch, chassis, or migration effects. That is legitimate, but it invites memorisation.
     Keep them as categories, but be aware of this.
   - Types are otherwise sensible: model, datacenter, cluster_id, vault_id and pod_id are categories; SMART values and capacity are floats;
     the target is a Yes/No category.
   - capacity_bytes is effectively categorical (19 values) and redundant with model. That is harmless.

8. Several source links have nothing to do with this data.
   task.md links SurvSet, arXiv 2203.03094 and the CRAN package frailtySurv. As far as I know, frailtySurv ships an old (circa 2013-2015)
   Backblaze "hdfail" survival subset, and SurvSet re-packages survival datasets. Neither can be the source of 2025-2026 snapshots that
   include datacenter, vault and pod columns. The real source is Backblaze Drive Stats.
   Change: cite Backblaze (their terms ask users to "Cite Backblaze as the source"), and drop or explain the other links.

PLAUSIBILITY: The values look real, not generated.
  - Power-on hours (smart_9_raw) have a median of about 30k hours (about 3.5 years) and a maximum of 113k hours.
  - Model names, capacities (8-26 TB) and datacenters (ams5, iad1, phx1, sac0, sac2, yyz1) match Backblaze.
  - The SMART normalized values sit near 100 or 200, as expected.
  - smart_241 and 242 (LBAs written/read) are in the 1e11 range.

WHAT I COULD NOT CHECK
- Whether the snapshot is taken on cut_date itself, and whether a failure on cut_date (day 0) counts as positive. If it does, the
  feature row would be the drive's last record, the failure day itself. The snapshots are all dated the 1st, and there is no serial,
  so I could not test this.
- How the about-22% subsample of 2025-2026-02 was drawn (per drive or per row), and why.
- Exactly which months the 3 test windows are. I assumed the last three months (2026-03, 04, 05), which matches the jump in row counts.
- How drives that leave the fleet without failing (migration or decommission) inside a window are labelled.
- Full-data numbers: all results above come from the 200k sample (209 positives), so the AUC/AP estimates are noisy.
- I did not read the arXiv paper's text.

Sources:
- https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data
- https://www.backblaze.com/blog/backblaze-drive-stats-for-q3-2025/
- https://www.backblaze.com/blog/hard-drive-smart-stats/
- https://github.com/awesomedata/apd-core/tree/master/core//TimeSeries/Hard-Drive-Failure-Rates.yml (empty metadata stub)

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: backblaze_hard_drive_failure (fails_within_30_days, ROC AUC, 3 monthly temporal test windows)
Scripts and logs: (the run's work files).

VERDICT
Inside one split (train rows + test features) the task cannot be gamed: no exploit beat the honest model. Two folds of three can be
solved almost perfectly (AUC 0.993-0.999) from data.parquet alone, because the next month's snapshot of the same drives sits in the
file as a later fold's test rows: a drive missing from the next month is a drive that failed. A harness that gives each method only
its own split's rows is safe; anything that sees the whole table (the kit, transductive use, a pooled feature-engineering pass) is not.

HONEST MODELS (same shipped splits; score.py)
  Splits: r0f0 test 2026-05-01 (350,349 rows), r1f0 test 2026-04-01 (344,784), r2f0 test 2026-03-01 (339,651); train 1,000,000 rows each,
  ending 2026-04-01 / 2026-03-01 / 2026-01-01 (r2f0 leaves 2026-02 out, whose 30-day window runs past 03-01: correct).
  - Untuned LightGBM (300 trees, lr 0.05, cut_date dropped)          r0 0.7821  r1 0.7978  r2 0.7890  mean 0.7896
    + one random-noise column, 2 seeds: mean 0.8083 / 0.8069, per split 0.780-0.841 -> the untuned model is unstable (+-0.02 noise)
    + month index as a feature: mean 0.7766 (worse)
  - Stable LightGBM (600 trees, lr 0.02, 15 leaves, min_child 200, bagging 0.5, colsample 0.5, lambda 5), 3 seeds
                                                                    r0 0.9130  r1 0.9090  r2 0.8824  mean 0.9015  (seed range 0.9010-0.9022)
  - Stable + drive-history lag features built only from the split's own training rows (drive re-identified by
    model+datacenter+cluster+vault+pod+slot+capacity and power-on hours consistent with the date gap; deltas of SMART 5/187/188/197/198/
    199/1/7/12/192/193/184/241/242/194), 3 seeds                     r0 0.9148  r1 0.9130  r2 0.8888  mean 0.9056  (0.9052-0.9061)
    -> +0.004 over stable, above seed noise. This is signal: a deployed model has the drive's past snapshots.
  - Same lag features from every earlier row in data.parquet (the full monthly snapshots, not the ~20% kept in training), 2 seeds
                                                                    r0 0.9151  r1 0.9153  r2 0.8871  mean 0.9058
    -> no gain over split-only history; the 1M-row training cap costs nothing here.
  Reference for exploits below: stable model (0.9015), and the untuned baseline (0.7896).

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Drive absent from the NEXT month's snapshot (rows of a later test window in data.parquet) | (the run's work files) | stable r1 0.9083, r2 0.8838 (untuned 0.7978, 0.7890) | rule alone r1 0.9934, r2 0.9958; rule + stable r1 0.9990, r2 0.9984 | +0.09 to +0.115 over stable (+0.20 over untuned) on r1f0, r2f0; r0f0 not reachable (no later month) | No: the next month's snapshot exists only after the 30-day window has passed | Give each method only its split's rows (train + that test window); if the full table must ship, drop from it every row dated after the split's test month, or shuffle/strip the slot columns |

No other exploit gained anything (see "found nothing").

FINDING 1: the next month's snapshot gives the label away (cross-fold, outside the split)
Mechanism: rows carry no serial number, but (model, datacenter, cluster_id, vault_id, pod_id, pod_slot_num, capacity_bytes) is unique
per date (5-7 collisions out of ~340k, all on missing pod_slot_num), and power-on hours (smart_9_raw) advancing by at most the date gap
confirms the same drive. The three test months 2026-03/04/05 hold the full fleet (~340k drives each), so 99.1% of 2026-03 drives and
99.3% of 2026-04 drives are found again a month later. Failed drives are pulled, so they are not: in 2026-03, 3,164 drives (0.93%)
are missing in 2026-04 and they hold 100% of the 327 positives (rate 0.103 vs 0.00000 among drives found again); in 2026-04, 2,309
missing drives hold 99.2% of the 505 positives (rate 0.217 vs 0.00001). The flag alone scores AUC 0.9934 (r1f0) and 0.9958 (r2f0);
added to the stable model 0.9990 / 0.9984. It uses only features (no labels) of rows that, under the shipped splits, belong to the
test side of another fold. r0f0 (2026-05, the last month) is immune.
Mildest fix: the harness should hand a method only its own split's train and test rows (it already must, for the test labels); the kit
itself should not be the input to a method. If the whole table must be visible, cut it per fold at the test month.

FLAWS THAT HURT AN HONEST MODEL
None found that the task causes.
  - December 2025 (2025-12-01) has a label rate of 0.00036, a third of every other month (0.0008-0.0015). Dropping it from training:
    mean 0.9011 vs 0.9015 (seed range 0.8993-0.9032): no effect.
  - Older months are subsampled (~22% of drives per month, rows sampled at random: label rate of the kept rows matches the month).
    Rebuilding history from the full earlier snapshots instead of the kept rows: 0.9058 vs 0.9056: no effect.
  - The untuned baseline's weakness (0.79 vs 0.90) is the model (300 trees at lr 0.05 on a 0.1% positive rate is unstable), not the task.

ATTACKS THAT FOUND NOTHING
  - Row order: test rows are shuffled within the month; AUC of row position 0.504 / 0.493 / 0.506; next-row label agreement among
    positives 0.2-0.6%; no column is monotone in position (|spearman| <= 0.004). Data is sorted by cut_date only.
  - Same-slot duplicates on one date (a failed drive and its replacement): duplicates exist only among rows with missing pod_slot_num;
    none among slotted rows. Nothing.
  - Label-window overlap between the last training month and the test month: 65,655 (r0) / 68,972 (r1) training rows link to a test
    drive; 1 / 0 of them are training positives, and that one is negative in test. Nothing.
  - Training labels vs date: subsample label rates equal the full-month rates; no row is in training because of its label; train ends
    at or before test month - 1 and every training label window closes before the test date. Nothing.
  - Formats: every numeric column is whole-number in both classes (no non-integer values anywhere); no decimals/precision artefact.
  - Missingness: count of missing columns alone AUC 0.515. Pockets with higher rates exist (82 missing columns: 601 rows, rate 0.080;
    all 128 SMART columns missing: 2,747 rows, rate 0.0055; missing pod_slot_num: 27,498 rows, rate 0.0061 vs 0.0010, in every month).
    These are in the day-1 snapshot a deployed model reads (a drive that returns no SMART or has no slot assigned): signal, and the
    tree models already use them. What would decide otherwise: whether Backblaze blanks the slot field only once a drive is
    scheduled for removal (then it is a maintenance decision recorded before the outcome, still known at prediction time).
  - SMART column coverage by month: stable (only smart_27 grows 2% -> 9%, a new model). Nothing.
  - Test-set composition: count of test rows per vault / pod / model, AUC 0.43 / 0.51 / 0.39 (these only proxy the model identity a
    model already has). Nothing.
  - Transforms over all rows: no standardised/min-max/rank columns; raw SMART values. Nothing.
  - Time column: adding the month index hurts (0.7766 vs 0.7896 untuned); it cannot extrapolate.
  - Web: no competition, leaderboard or "magic feature" thread exists for this monthly framing. Public write-ups note that Backblaze's
    "failure" means the drive was pulled from its pod (sometimes before it actually fails), and that same-drive rows across train/test
    leak in random splits; the temporal split here avoids the latter. Looking rows up in the published Backblaze daily CSVs would work
    (model + slot columns + power-on hours identify the serial, whose failure flag is public) - not a flaw of the task, not ranked.

NOT CHECKED
  - Whether the benchmark harness passes a method anything beyond its own split (decides whether Finding 1 is live outside the kit).
  - Whether the December-2025 dip comes from the source (fewer removals over holidays) or from the label build (e.g. missing daily
    files); it does not move the score.
  - A downloaded comparison of the kit with the raw Backblaze daily files (multi-GB); the preparation's rounding/filtering was inferred
    from the kit only (monthly first-day snapshots, older months subsampled to fit a 1M-row training cap, serial number dropped).

Sources: https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data ; https://www.backblaze.com/blog/backblaze-drive-stats-for-2025/ ;
https://arxiv.org/pdf/2102.06509 ; https://old.operate-first.cloud/data-science/ceph-drive-failure/docs/blog/hard-drive-failure-prediction-blog.md

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER REPORT: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Verdict: five of the eight calls follow precedent. Two depart from a Must without a fact that sets the case apart:
the boot-drive keep (draft issue 5; LEAK-25) and the year (draft issue 6; PROV-9). One departs only within the
definition: `pod_slot_num` as a number while `pod_id`, also a position, is a category (CLEAN-14, P7). No drift was
found in the curators' rulings on these rules. This case adds no third exception of any kind. The CLEAN-19
amendment_due flag (amex_non_iid, and fraud_detection_in_electricity_and_gas_consumption with its _1m copy) is about
keeping raw history rows, and option A here is not of that kind.

Read: principles.md; use_case.md, leak_checks.md, splits.md, cleaning_features.md, provenance.md, metrics.md and
selection.md (rules and Cases tables); register.json (the USE-5 and CLEAN-19 flags, the
LEAK-22/23/25 and SPLIT-12 groups); the definitions and records named below; builder_report.md; claim_auditor.report.txt.
Own check: on the builder's labelled_explore.parquet (5,547,634 kept rows), 0 of 67,314 rows with capacity <= 2.1 TB
are positive, against 5,827 of 5,480,320 others. This matches the claim auditor's count.

**PER DECISION**

1. Label partly follows Backblaze's own replacement decisions; keep, fit approximate (draft issue 1, A; USE-5, USE-8,
   SEL-5, TP-4)
   CONSISTENT.
   - Follows:
     - fraud_detection_in_electricity_and_gas_consumption_1m: the label is STEG's own inspection findings, and a 0 is
       "no fraud found". Kept with fit approximate (CC 2026-10-26, Lennart, verdict ship).
     - ieee_fraud_detection: a chargeback rule labels every transaction. Kept, fit direct. The xente ruling of
       2026-11-04 names it as the counter-case.
     - chicago_traffic_crashes: "USE-5 fails only when the label is shown to be another quantity" (CC 2026-11-05,
       Lennart).
     - diabetes_3: keep and mark approximate (2026-10-21, Lennart; USE-5 amended).
     - USE-8's own list: "a label definition the sources do not settle (no stated horizon ...)" is approximate.
       Backblaze states no horizon.
   - The closest precedent the other way: xente_fraud_detection_challenge, `No` with `Data Quality Issue` under USE-5
     (CC 2026-11-04, Lennart).
     - Xente's fact: a review applied above about 500k UGX on a shipped input. 109 of 110 rows at 500k-1M are fraud,
       against 16 of 149 at 100k-490k, so a 0 below the step means "not reviewed".
     - What sets Backblaze apart, evident from the data and the source:
       - Every drive in service is monitored, and a drive that dies is recorded wherever it sits. 47.0% of failures
         are reactive (640 of 1,361 in Q3 2024, the claim auditor's reading of the post).
       - The TP-4 probe finds no step on an input. The five-counter rule scores ROC AUC 0.832 / 0.872 / 0.838,
         against 0.887 / 0.903 / 0.904 for a model. 21% to 28% of positives have all five counters at zero.
       - So a No here is not "not reviewed".
   - SEL-5 does not apply, as the builder says. Its precedents (account_debt_south_africa; the NEWS2 case,
     central_international_medical_college_and_hospital_health_risk_prediction) are labels set by a published rule.
     Backblaze's rule is not published, and the rule alone is below a model.
   - Two notes for the curator, not departures:
     a. The proactive share varies by server type and datacenter: Dell 73.5%, Storage Pod 6.0 44.6%, AMS 68.1% (the
        claim auditor's Q3 2024 reading). The datacenter is an input. This is the part of the mechanism closest to
        Xente's. LEAK-25 as amended (noaa_storm_events_damage, 2026-11-02, Andrej) asks, for a recording that follows
        a unit shipped as a feature, that the notes give the unit's spread. Write the spread into the notes and
        `fit_reason`.
     b. Record the fact that sets this case apart from xente in the notes, as the xente ruling recorded its own fact
        against ieee. Suggested text: "every drive is monitored and a dead drive is always recorded; the five-counter
        rule ranks below a model, so no review step on an input".
   - Same batch, for the mediator: data_fusion_2026_guardian_1m (draft) reads fit `direct` for a label that exists
     only for operations the bank's system held. That differs from Backblaze's approximate. The fact that sets them
     apart is that the contest defines its label and task, while Backblaze defines none (USE-8). This is not a
     finding on this dataset.

2. 30-day horizon, monthly cuts, one-month test windows (draft issue 2, A; SPLIT-12)
   CONSISTENT.
   - SPLIT-12 asks for a horizon from human judgement, with the reasoning written down. The source gives none. The
     definition names its reasons in HORIZON_DAYS and splits_comment: the PAKDD 2020 30-day horizon, the monthly
     refit and the base rate. It keeps PAKDD out of the sources (PROV-12).
   - A field's standard horizon where the source states none:
     - framingham_heart_study_fhs: 10 years, the pooled cohort equations' outcome (2026-10-22).
     - cirrhosis_patient_survival_prediction: 5 years (2026-10-14).
   - Test windows at the refit cadence: the house family case (house_sales, perth_house_prices, ames_housing,
     zillow_prize, melbourne_housing_market): "each keeps the horizon of its own source or refit cadence" (SPLIT-12,
     2026-10-21, Lennart).
   - The warning `meta_time_horizon_mismatch` was accepted for the same reason (one cut date per monthly window) on
     perth_house_prices, zillow_prize and tunisian_fraud_detection_challenge. The proposed acceptance follows them.
   - Caveat, written down already: the monthly cadence is ours. Backblaze's own cadences are daily (monitoring) and
     quarterly (reports). Option B, the quarterly one, is ruled out by SPLIT-14's floor on the downloaded span, not by
     preference.

3. No change features over the 30 days before the cut (draft issue 3, A; CLEAN-19)
   CONSISTENT, a weighing call. It is not an exception.
   - CLEAN-19 builds a history feature when the raw data cannot be used as it is. The SMART counters are cumulative,
     so the cut-day snapshot already carries the history.
   - The precedents that built a feature had firmer evidence:
     - rain_in_australia: better in 8 of 9 windows, paired SE 0.0045 (2026-10-26).
     - alfa_battle_2_0_task_2: better in 3 of 3 windows, the top solutions' features (2026-10-13).
     - african_credit_scoring_challenge: the count alone scores ROC AUC 0.72, and a placed solution built a variant
       (2026-10-26).
     - In this batch, data_fusion_2026_guardian_1m and azure_vm_lifetime_resource_central_1m build the history
       features their source papers use.
   - Backblaze has no source baseline, and the measured gain is +0.010 / +0.007 / -0.002 on one seed. Not building
     follows the rule. The curator should know the evidence is one seed without an SE, below rain's standard.
   - Whether practice builds 7- and 30-day deltas on SMART data is the domain practitioner's question.

4. Drives removed without failure within the 30 days are dropped (draft issue 4, A; cited LEAK-22 against LEAK-23)
   CONSISTENT in the outcome. The rule citation differs from the precedents.
   - Follows: precedents drop units whose exit is administrative and whose outcome is unknown, never by the label.
     - framingham_heart_study_fhs: 16 lost to follow-up dropped, while the 251 competing deaths stay No (LEAK-22,
       2026-10-22, Lennart).
     - cirrhosis_patient_survival_prediction: 5 lost to follow-up dropped (LEAK-23, 2026-10-14).
     - mortgage: 501 exits censored at refinance dropped, 98 of them in test windows (LEAK-25 and CLEAN-15,
       2026-10-20).
     - fraud_detection_in_electricity_and_gas_consumption_1m: clients who left dropped "by their last invoice date,
       never by the label" (LEAK-25 as amended, CC 2026-10-26).
     - Same batch: rais_employment_separation_1m drops the abandoned links (LEAK-25 and CLEAN-15).
   - Against framingham's competing death: a vault migration (8,489 of 8,873 rows, 95.7%, in blocks of 20 or more
     drives of one vault) is the operator's exit, not a risk the drive faces. Dropping it does not select on the
     future the way dropping a death would.
   - The 206 scattered data drives look partly like failures without a record: 42.7% have an error counter above
     zero, against 7.7% of the kept No rows. Dropping them by `last_seen`, a rule that does not read the label, is
     LEAK-25's remedy for unrecorded outcomes, as with STEG's leavers (4.7% fraud against 7.8%).
   - Documentation only:
     - Cite LEAK-25 (amended 2026-10-21) and CLEAN-15, as mortgage, STEG and rais do, plus LEAK-22 for why
       migrations are no competing event. LEAK-23 is the right-truncation rule for event-only targets and does not
       describe this mechanism.
     - Correct the "whole vaults" rationale with the claim auditor's split: 8,489 / 178 boot / 206 data drives.

5. Boot drives kept (draft issue 5, A)
   NOT REASONABLE UNDER THE RANKING. It departs from LEAK-25 (Must, P4), and the fact given for the keep is refuted.
   - The fact given: "the operator replaces them too". The data:
     - 0 of 67,314 boot rows are positive (my count above).
     - Boot drives have 32 failure records in Q4 2024 and none from January 2025 to June 2026 (claim auditor).
     - Boot drives still vanish, 7 to 68 per cut. The removal filter drops those 306 rows, so the kept boot rows are
       No by construction: "no event" mixed with "not recorded".
   - The boot rows are located by a rule that does not read the label (capacity <= 2.1 TB, or the boot model list).
     This is the case of LEAK-25 as amended 2026-10-21 (Lennart), where the located rows are dropped:
     - caracas_cervical_cancer (2026-10-15): 108 patients, 0 positive results where 11.8 were expected.
     - account_debt_south_africa: 28,124 rows, none of their 12,167 billed never-payers a bad debt, against 91.9%
       elsewhere.
     - fraud_detection_in_electricity_and_gas_consumption_1m: the clients who left, dropped by last invoice date.
   - The keep-with-a-note branch (noaa_storm_events_damage, 2026-11-02, Andrej) needs a measured signal within the
     unit. Boot drives have none.
   - It is also USE-5 by the chicago criterion: for these rows the label is shown to be another quantity
     ("not recorded").
   - Effect: a ranker that puts boot rows last gains ROC AUC +0.0014 to +0.0019 per window (claim auditor).
   - A Must has no exceptions, so keeping them needs an amendment, not an exception. Reflection prompt R1 below.

6. `pod_slot_num` as a number; `cluster_id`, `vault_id`, `pod_id` as categories (CLEAN-14)
   DEPARTS WITHIN THE DEFINITION, with no fact written down. P7, small.
   - A number for a physical position with an order is in line with CLEAN-14's "numeric for everything else" and
     with lt_vehicle_loan_default_prediction: `Current_pincode_ID` stays a number because its order carries
     geography, +0.0049 ROC AUC on 9 of 9 windows (2026-11-05, Lennart).
   - The pair to answer is inside this definition:
     - `pod_id` is described as "the pod's place in" the vault, numbered 0-19, and typed categorical.
     - `pod_slot_num`, "a position in the chassis", is typed numeric.
     - Both are positions. The definition does not say why one is ordered and the other is not.
   - A likely fact, from Backblaze's descriptions of its vaults and not verified here: the 20 pods of a vault are
     shards in different cabinets (an index with no physical order), while a slot has a physical place in one
     chassis.
   - Against the number: slot numbering differs between chassis types (Storage Pods of 60 slots against Dell and
     Supermicro servers). The same number can then be another place, which reads like a code.
   - The column auditor is measuring this column. Reflection prompt R3 below, to settle the pair either way.

7. Metric: fallback roc_auc (MET-6, MET-8, MET-9, MET-11)
   CONSISTENT.
   - Backblaze defines no task.
   - PAKDD 2020's windowed F1 belongs to another source and fixes no threshold, so it does not carry over (MET-6):
     ljubljana_breast_cancer, heart_disease, credit_approval.
   - Imbalance alone is no reason for PR AUC (MET-9; sepsis_survival_minimal_clinical_records).
   - The reason names where we looked (MET-11 fallback).
   - Taking PAKDD's horizon but not its metric is no inconsistency. The horizon fills a gap in the label's
     definition that USE-5 requires us to close, while MET-6 bars a threshold metric whose threshold no source fixed.

8. Year: definition 2015, record 2013, builder proposes setting the record to 2015 (draft issue 6; PROV-8, PROV-9)
   DEPARTS, with no fact that sets the case apart. Both values break PROV-9 (Must).
   - PROV-9: "A source that grows over time (a public register, a scraped site, a monthly archive) takes the year of
     the snapshot we pin." Backblaze's page is a quarterly archive with a new zip each quarter, and the definition
     reads only Q1 2025 to Q2 2026. None of its rows are in the February 2015 release.
   - Precedents: every growing source in the working copy carries the year of its pinned snapshot.
     - chicago_traffic_crashes, sf_permit_time, consumer_complaints_1m, kickstarter, college_scorecard and
       noaa_storm_events_damage: 2026.
     - wadden_sea_sibes_macoma_abundance: 2024, its pinned version.
     - The same batch (2026-11-08): fpa_fod_wildfire_cause_1m ("the edition we pin ... the first edition is of 2013"),
       ny_wcb_assembled_claims_1m ("reposted quarterly"), chile_school_dropout_mineduc_1m,
       chicago_taxi_trip_duration_1m and aeolus_rebuilt_1m, all 2026.
   - The one precedent for a first-release year, melbourne_housing_market (2017), is one Kaggle upload that grew over
     its versions, which PROV-9 names separately. Backblaze is an archive of separate files, not one upload's
     versions.
   - The bibtex year (2015) and its note "published since February 2015" should follow the year chosen. The
     2015-02-04 announcement can stay in the comments as the series' start.
   - Reflection prompt R2 below.

Not asked, checked in passing, consistent:
- Cut-day failures dropped (198): the snapshot is the failure record (LEAK-10, USE-3).
- The 29-day gap removes unmatured training labels (SPLIT-9). It is no SPLIT-14 exception: the oldest window trains on
  75% of the rows.
- Test drives are known drives (SPLIT-13, USE-10): the operator scores its own fleet, the setting of
  tunisian_fraud_detection_challenge (2026-11-05).

Drift: none found.
- Lennart's USE-5 rulings keep a label set by a process the actor runs or a source left undocumented: diabetes_3
  (2026-10-21), STEG (2026-10-26), chicago_traffic_crashes (2026-11-05). The one exclusion, xente (2026-11-04),
  records its measured step as the fact that sets it apart.
- LEAK-25's located-and-dropped remedy has been applied the same way since 2026-10-21.
- PROV-9's pinned-snapshot year has been applied the same way since 2026-10-12, by both curators and in this batch.

**REFLECTION PROMPTS (issue shape, for REVIEW.md)**

R1. **Drop the boot drives, whose failures are no longer recorded?**

   * **Problem:**
     * None of the 67,314 boot-drive rows is a positive, and the files hold no boot-drive failure record after
       December 2024 (32 in Q4 2024)[^r1a].
     * The 306 boot rows that vanish within 30 days are dropped as "removed", so the kept boot rows are No by
       construction[^r1b].
     * caracas_cervical_cancer and account_debt_south_africa dropped a subgroup located this way (0 positives where
       many were expected)[^r1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep as an exception: the fleet team scores every drive in service, boot drives included | 1.2% of rows stay, with a note | the rows mirror the fleet | LEAK-25 is a Must and has no exceptions; for these rows the label means "not recorded"; +0.0014 to +0.0019 ROC AUC for learning boot = No |
     | b | Drop boot drives by capacity <= 2.1 TB or the boot model list (implemented: no) | 67,314 rows leave; a note gives the 32 failure records of Q4 2024 against none since | follows caracas and account_debt; the label means one thing on every row; Backblaze leaves them out of its own statistics | the fleet model no longer scores boot drives |
     | c | Treat a boot drive's vanishing as a failure | relabel the 306 rows | keeps boot drives | invents a label the source does not give (USE-5); migrations cannot be told apart |
     | d | Amend LEAK-25 to keep a located subgroup with no recorded outcome | a rule change | none found | the remedy of three precedents is reversed |

   * **Recommendation:** b. **Decision:** a, b, c or d?

   [^r1a]: **USE-5** (Must): predict what the actor acts on; a label checked and shown to be another quantity fails
     (chicago_traffic_crashes, 2026-11-05, Lennart).
   [^r1b]: **LEAK-25** (Must; amended 2026-10-21, Lennart): "no event" mixed with "not recorded"; unrecorded rows
     located by a rule that does not read the label are dropped (caracas_cervical_cancer, account_debt_south_africa,
     fraud_detection_in_electricity_and_gas_consumption_1m). The keep branch (amended 2026-11-02, Andrej,
     noaa_storm_events_damage) needs a measured signal within the unit, and boot drives have none.

R2. **Set the year to 2026, the archive snapshot we pin, in the definition and the record?**

   * **Problem:**
     * The definition says 2015 (the first raw-data release) and the record says 2013, but the rows come only from
       the 2025-26 quarterly files[^r2a].
     * Every other growing source carries its pinned snapshot's year, including five of this batch[^r2a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep 2015 as an exception: Drive Stats is one series announced in February 2015, like a Kaggle upload that grew (melbourne_housing_market) | the definition stays; the record goes to 2015 | names the series' start | PROV-9 is a Must; none of our rows were in that release; fpa_fod_wildfire_cause_1m had a 2013 first edition and took 2026 |
     | b | 2026 in the definition (year and bibtex) and the record; the 2015 announcement in the comments | follows PROV-9 and the eleven precedents | one reading for all growing sources | the year no longer shows how old the series is |
     | c | 2013 (the record's value, the first year of data) | the definition changes | none found | the collection period, which PROV-9 excludes |
     | d | Amend PROV-9 so that an operator's continuous series takes its first release | a rule change | none found | reopens the growing sources dated 2026 |

   * **Recommendation:** b. **Decision:** a, b, c or d?

   [^r2a]: **PROV-9** (Must): a source that grows over time (a public register, a scraped site, a monthly archive)
     takes the year of the snapshot we pin (chicago_traffic_crashes, sf_permit_time, consumer_complaints_1m,
     kickstarter, college_scorecard, noaa_storm_events_damage; in this batch fpa_fod_wildfire_cause_1m,
     ny_wcb_assembled_claims_1m, chile_school_dropout_mineduc_1m, chicago_taxi_trip_duration_1m, aeolus_rebuilt_1m).
     **PROV-8** (Must): the source is the first publication, which here stays the Backblaze data page.

R3. **What sets `pod_slot_num` (a number) apart from `pod_id` (a category), both positions in Backblaze's racks?**

   * **Problem:**
     * The definition types the drive's slot in its pod as a number and the pod's place in its vault (0-19) as a
       category, without saying why one is ordered and the other is not[^r3].
     * The slot numbering differs between chassis types (60-slot Storage Pods, Dell and Supermicro servers), so one
       number can mean other places[^r3].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep both, with the fact written: a vault's pods are shards in different cabinets (an index without order), while a slot is a physical place in one chassis | one comment line | the order is physical, as lt_vehicle's pincode order is geographic | numbering differs by chassis type; the fact is not verified on the data |
     | b | Type `pod_slot_num` as a category | 1 line in `_feature_types` | the same reading as `pod_id`; safe across chassis types | loses the order within a chassis |
     | c | Type `pod_id` as a number too | 1 line | both positions read alike | a shard index has no order |

   * **Recommendation:** a if the column auditor finds the slot's order meaningful within a chassis type, otherwise
     b. **Decision:** a, b or c?

   [^r3]: **CLEAN-14** (Should; amended 2026-10-21, Lennart): categorical when the context says the values are a
     fixed set; numeric otherwise; the meaning decides. Case: lt_vehicle_loan_default_prediction,
     `Current_pincode_ID` kept as a number for its geographic order (2026-11-05, Lennart).

**Files**

Definition: datasets/_dev/tabarena-v0pt2/backblaze_hard_drive_failure_1m/dataset.py
Record: curation/records/backblaze_hard_drive_failure.md
Precedent records: xente_fraud_detection_challenge.md, fraud_detection_in_electricity_and_gas_consumption*.md,
chicago_traffic_crashes.md, mortgage.md, framingham_heart_study_fhs.md (same records folder).

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Position: ship. The task, the label, the split and the metric hold under every audit. Three findings are real, and
each one is fixed by a filter or a field edit inside the definition (remedy ladder, step 2). None of them is a reason
to retire. Where an agent found a real problem I concede it below and name the mildest fix.

1. A real fleet task, and the label is the quantity the actor acts on. Fit approximate is the right call.
   [P3: USE-1, USE-5 (Must), USE-8, USE-10; P6: TP-1 to TP-9]
   - All seven agents call it a real task. The blind reviewer, with no context, says "the textbook use of the
     Backblaze Drive Stats data". The practitioner says "one test window = one cut of the whole fleet: exactly my
     review". Replacement logs are the field's standard ground truth (Schroeder & Gibson, Pinheiro, Botezatu).
   - It is not the operator's rule. The five-counter rule scores 0.832 / 0.872 / 0.838, a model 0.887 / 0.903 /
     0.904, and 21-28% of positives have all five counters at zero (the claim auditor reproduced these with the
     shipped scorer). Failures within 7 days rank no better than those in 8-30 days. At the top 0.5% of the fleet a
     model catches 39-43% of next month's failures, against 15-19% for the rule (practitioner).
   - Precedent: label kept, fit approximate, in diabetes_3, STEG _1m and chicago_traffic_crashes. "USE-5 fails only
     when the label is shown to be another quantity" (Lennart, 2026-11-05). xente is set apart by a fact: 47.0% of
     failures are reactive (640 of 1,361 in Q3 2024), and no step was found on any input (precedent checker). SEL-5
     does not apply, because the rule is unpublished and ranks below a model.
   - Value: 327-505 test positives per window, no probe flags, random forest beats the dummy 3/3.
   - Outranks the circularity objection: the measurements (EV-2) show a label that is wider than the rule.
     Documentation only: replace "a suggestion, not a count" with the 47.0% / 53.0% count, and add the spread by
     server type and datacenter to fit_reason (claim auditor, precedent checker).

2. The split is honest and matches the use case. [P4: SPLIT-1, SPLIT-3, SPLIT-9, SPLIT-10, SPLIT-12, SPLIT-13,
   SPLIT-14, LEAK-12, all checked on the shipped splits]
   - Temporal and monthly. Gap 29 days, so train cut + 30 days <= test cut in every window. Training shares are
     75.3% / 87.5% / 93.7%. 98.2-98.8% of test drives are known drives. Two auditors verified it (split, claim).
   - The blind reviewer's look-ahead concern (the Feb cut's label runs into March) is already handled: February is
     left out of the March window. The blind reviewer's "undocumented subsample" is a clean-room artefact: the random
     1M is stated in splits_comment and version_comment. Kept rows have the same label rate as the full month, and
     history built from the full months gains nothing (0.9058 vs 0.9056, task gamer).
   - A 90-day horizon would fail SPLIT-14's floor, so option A of issue 2 is forced, not preferred.

3. The features carry no leak except one narrow field, and that one is fixed in the definition.
   [P4: LEAK-10 (Must), LEAK-7 remedy; tension row "a real task against a leak: fix the leak and keep the task"]
   - Clean: every leak probe; every in-split exploit of the task gamer ("no exploit beat the honest model"); no
     pile-up of failures in days 1-3 (9.7% vs 10.0% expected if uniform); exact copies across the split 0.1%, all
     with the same label.
   - CONCEDE: pod_slot_num going empty marks a drive already taken out of service, mostly the first step of its
     replacement (column auditor). Slotless data drives fail at 5.97% vs 0.100%. Effect: ROC AUC moves by -0.002 to
     +0.003, but average precision rises 15-20% at the top of the ranking.
   - Mildest fix: the column auditor's (a). Drop data-drive rows with no slot at the cut, by a label-free rule:
     2,653 shipped rows, 169 positives. These drives are no longer a decision at the review (USE-7). The fix keeps the
     column and also removes the 26 SMART-less rows. Fallback (b): drop the column.

4. The boot drives are a fixable subgroup and no threat to the dataset. [P4: LEAK-25 (Must, amended 2026-10-21);
   P3: USE-5]
   - CONCEDE: 0 of 67,314 boot rows are positive. There is no boot failure record from January 2025 to June 2026,
     and the removal filter drops the boot drives that vanish. So "the operator replaces them too" does not reach the
     label. Three agents agree (claim, column, practitioner) and the precedent checker shows a departure from a Must.
   - Mildest fix: option B of issue 5. Drop by capacity_bytes <= 2.2e12 (or the boot model list), a label-free rule,
     as in caracas_cervical_cancer, account_debt_south_africa and STEG _1m. Backblaze also reports boot drives apart.
     This keeps 98.8% of rows. It also clears the SSD-only columns, the smart_245 exact copy and 178 of the 384
     scattered removals. Effect of the bug: +0.0014 to +0.0019 ROC AUC. That is small, and a filter removes it
     completely.

5. The cross-fold "next month" exploit (AUC 0.993-0.999) is a property of how the table is handed out, not a flaw of
   the definition. [P4: SPLIT-9 and LEAK-12 hold inside every split; the container contract hands a method train_idx
   and test_idx only]
   - The task gamer: "Inside one split ... the task cannot be gamed", and "a harness that gives each method only its
     own split's rows is safe". It needs the rows of another fold's test window. The newest window is immune.
   - Mildest fix: a README sentence ("a method sees only its own split's rows"). No change to the data is needed.
     Independent failures are not conflicts, but this one is not a failure of this dataset.

6. The censoring drop and the cohort are consistent with precedent and move nothing. [P4: LEAK-25, CLEAN-15, LEAK-22]
   - Issue 4: 95.7% of removals are vault blocks of 20 or more drives, which are planned migrations the operator
     knows at the cut (practitioner). Keeping them as No moves test AUC by at most 0.0006 (split auditor). Precedent:
     mortgage, STEG, rais and framingham's lost-to-follow-up drop administrative exits by a label-free rule
     (precedent checker: "CONSISTENT in the outcome").
   - Documentation only: cite LEAK-25 and CLEAN-15 instead of LEAK-23, and write the 8,489 / 178 / 206 split.
   - Drives missing on the cut day (split auditor's 187): known at the cut, "no leak and no split error". Add a note
     with the counts.

7. The metric, the cleaning and the metadata need notes and cheap edits, no redefinition. [P6: MET-6, MET-7, MET-9,
   MET-11; P7: CLEAN-5, CLEAN-10, CLEAN-11, CLEAN-19; P5: PROV-9]
   - roc_auc is the rule-consistent fallback. The practitioner's top-k needs a k that no source fixes (MET-7), and
     imbalance is no reason for PR AUC (MET-9). The precedent checker and the practitioner both conclude
     "rule-consistent". A MET-11 context metric is optional and is the curator's call.
   - Change features: CLEAN-19 is a weighing call, with a mixed gain on one seed (+0.010 / +0.007 / -0.002). Not
     building them follows precedent (precedent checker).
   - Cheap P7 edits: smart_9_raw 0 and 65535 and smart_240_raw 65535 to missing (about 150 rows); the smart_245 copy
     leaves with the boot drives.
   - CONCEDE the year. PROV-9 (Must) gives 2026, the pinned snapshot, in the definition, the bibtex and the record.
     That matches eleven precedents, including five in this batch. 2015 stays in the comments as the series' start.
   - Notes to correct: the December dip (partly unrecorded failures), the WUH721816ALE6L4 naming, and cluster_id's
     "not always correct".

Judgment record
Verdict: ship after changes.
Validity:
- SEL-1 and SEL-16 hold.
- USE-5 holds (fit approximate, precedent diabetes_3 / STEG / chicago).
- LEAK-10 triggered: fix by dropping slotless data-drive rows.
- LEAK-25 triggered: fix by dropping boot drives.
- SPLIT-1, SPLIT-9, SPLIT-10, SPLIT-12, SPLIT-13 and SPLIT-14 hold.
- PROV-9 triggered: fix by setting the year to 2026.
Value: TP-1 to TP-9 clean; 327-505 test positives per window.
Quality: CLEAN-10 and CLEAN-11 fixed cheaply; CLEAN-19 a weighing call (A).
For the curator: issue 3 (change features, weighing call); optional MET-11 context metric.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

The critic and I reach the same verdict, "ship after changes", and argue for the same fixes. No point of the critic
asks for exclusion. I concede five points in full and two in part. The two partial ones disagree only on the strength
of a remedy.

C1. Boot drives (LEAK-25). CONCEDE, as in my point 4.
    - Fix: drop boot drives by capacity_bytes <= 2.2e12 (issue 5, option B).
    - Add a note: 32 boot failure records in Q4 2024, none since.
    - The critic's count of 11,671 boot test rows with 0 positives matches the column auditor's.
    - Result: 98.8% of the rows stay, and the label means one thing on every row.

C2. Empty pod_slot_num (LEAK-10, USE-7). CONCEDE, as in my point 3. The critic adds an argument that strengthens
    remedy (a) over (b).
    - The definition already leaves out drives absent from the cut-day file: 187 of 1,449 failing drives. Slot-empty
      data drives are in the same out-of-service state.
    - Dropping their rows makes the cohort consistent: drives in the data path on the cut day.
    - Remedy (b), dropping the column, would leave those rows in with nothing to mark them.
    - So (a) is the right fix: 1,510 test rows and 115 positives leave, and 1,147 test positives stay.

C3. Removed without failure. CONCEDE on the documentation. DISPUTE any change to the rows.
    - Documentation: the notes and issue 4 get the 8,489 / 178 / 206 split, cite LEAK-25 and CLEAN-15 instead of
      LEAK-23, and the December dip gets its clause.
    - Rows: keep the drop (option A).
      - 42.7% of the 206 scattered data drives carry error counters. That makes them partly unrecorded failures, which
        is LEAK-25's case: drop by a label-free rule. LEAK-22 is the wrong rule for them, because keeping them as No
        would label probable failures No.
      - The vault blocks are migrations planned before the cut. That fact sets them apart from framingham's competing
        death (precedent checker 4).
      - Either way the effect is at most 0.0006 AUC (split auditor). So the record needs its rule fixed, and the rows
        need no change.

C4. Cross-fold exploit (LEAK-9, Should). CONCEDE the remedy, the protocol line in splits_comment and the README.
    - The critic agrees there is no effect when a harness hands out one split's rows, and LEAK-9 puts this kind of
      leak in the protocol, not in the data.
    - Nothing in the rows changes.

C5. Year and source links (PROV-9 Must, PROV-8). CONCEDE.
    - Year: 2026 in the definition, the bibtex and the record (as in my point 7).
    - Links: the record's source_links (lines 24-26: SurvSet, arXiv 2203.03094, frailtySurv) are where the scout found
      the record, not this data. Move them to the discovery comment (line 38 already says "a small survival
      extract").
    - This is a field repair, the top step of the remedy ladder.

C6. ROC AUC vs the operator's top of list (MET-11). CONCEDE the README note. DISPUTE that a context metric should be
    offered as an open issue.
    - The critic grants that roc_auc meets the rules (MET-6, MET-7, MET-9) and that the evidence "shows a direction,
      not proof": one positive is worth 0.002-0.003 recall.
    - MET-11 `context` needs a metric the task makes obvious. Here every candidate needs a k or an FPR cap that no
      source fixes. Recall at the top 0.5% and pAUC to FPR 1% are both our inventions, which MET-7 bars ("we never
      invent a cost or threshold the source did not fix").
    - So the fallback stays. Name the gap in the README. If the curator wants a context metric, it is their weighing
      call, not a defect of this definition.

C7. Notes and sentinels (USE-5/USE-8 documentation, CLEAN-10/11). CONCEDE.
    - Notes: the 47.0% / 53.0% count, the spread of the proactive share by server type and datacenter, the fact that
      sets this case apart from xente, and the cut-day-absent cohort, in curation_comments and fit_reason.
    - Sentinels: smart_9_raw 0 and 65535, and smart_240_raw 65535, become missing.

Agreed fix list (all inside the definition, none needs exclusion):
- Drop boot drives (issue 5 B).
- Drop slot-empty data-drive rows (new issue, remedy a).
- Make the sentinels missing.
- Year 2026; move the source links.
- Protocol line and metric note in the README.
- Correct the notes and rule citations on issues 1 and 4.
Open for the curator: issue 3 (change features, CLEAN-19 weighing) and, if they want it, a MET-11 context metric.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

Position: ship only after changes. The task is real (a fleet team ranking its drives at a monthly review) and none of
the points below calls for exclusion. But two Must rules are broken in the definition as written (points 1 and 2), and
both can be fixed with a filter that does not read the label. Until they are fixed, part of the test score measures how
Backblaze records failures, not which drives will fail.

Own check (the participant kit's data, the three test windows, 1,262 positives in all):
  boot drives (capacity <= 2.2 TB)       11,671 rows      0 positives
  data drives with an empty slot          1,510 rows    115 positives (7.6%)
  data drives with a slot             1,021,603 rows  1,147 positives (0.11%)
These match the column auditor's counts.

1. Boot drives are No because their failures are not recorded.   [P3/P4; LEAK-25 Must, USE-5 Must]
   Problem: the files hold no boot-drive failure record from January 2025 to June 2026. There were 32 in Q4 2024 and
     none after. Boot drives still leave the files (7 to 68 per cut, 306 rows), and the removal filter drops exactly
     those. So all 67,314 kept boot rows are No by construction: "no event" mixed with "not recorded".
   Effect on the task: 3.4% of the test rows (11,671) are free negatives, and model and capacity identify them. A ranker
     that puts them last gains +0.0014 to +0.0019 ROC AUC per window. For these rows the label is a different quantity.
     The stated reason, "which the operator replaces too", is refuted: the label cannot see those replacements.
   Evidence: claim auditor 16b; column auditor B; domain practitioner (0 of 6,879 failure records on a boot serial);
     precedent checker 5; my count above.
   Rule: LEAK-25 (Must; amended 2026-10-21) says to drop unrecorded rows found by a rule that does not read the label
     (caracas_cervical_cancer, account_debt_south_africa, STEG _1m). The keep branch (noaa_storm_events_damage) needs a
     measured signal within the unit, and boot drives have none. A Must has no exceptions.
   Remedy: fix the definition by dropping boot drives (capacity_bytes <= 2.2e12, or the boot model list), which is draft
     issue 5 option B. Add a note with the 32 failure records of Q4 2024 against none since. Update the counts. The
     boot-only SMART columns then fall to the existing empty/constant drop.

2. An empty pod_slot_num marks a drive already in its replacement.   [P4; LEAK-10 Must, "missingness that encodes the
   outcome"; USE-7 Must]
   Problem: on data drives, the slot goes empty when the drive is taken out of the data path, usually as the first step
     of the replacement that writes the failure record. In the daily files the slot is empty on 69% of failure-record
     days and on 14.5% of drives one day before the record. On slot-empty days the drive reads about 0.1M LBAs a day,
     against 340M to 460M. In the full frame, 6,184 data-drive rows are slot-empty and 369 of them are positive (5.97%
     against 0.100%).
   Effect on the task: 9.1% of the test positives (115 of 1,262) sit in 0.4% of the test rows. ROC AUC hardly moves
     (+/-0.003), but average precision rises by 0.017 to 0.020 (15-20% relative), which is the top of the list the
     operator acts on. These drives are no longer a prediction: the operator has already pulled them.
   Inconsistent cohort: the definition already leaves out drives missing from the cut-day file, which is 13% of failing
     drives (187 of 1,449), the most obvious failures (split auditor, finding 5). Slot-empty drives are in the same
     out-of-service state, but they are kept.
   Evidence: column auditor A (the run's work files); the task gamer's missingness pocket
     (missing pod_slot_num: rate 0.0061 against 0.0010 in every month); my count above.
   Rule: LEAK-10 (Must) excludes missingness that encodes the outcome, with the smallest fix taken first (LEAK-7).
     USE-7 (Must): a row without the input the decision acts on is no task row.
   Remedy: fix the definition by dropping the data-drive rows whose pod_slot_num is empty at the cut. This filter does
     not read the label, and the rows have no decision left. It also takes the 26 SMART-less rows and the label-free
     whole-vault slot gaps. If that is refused, drop the column (the column auditor's b). Add a note in either case:
     the reading is ours, and Backblaze does not document an empty slot.

3. Drives removed without failure: the rationale is wrong and the rule cited is wrong.   [P4; LEAK-22 Must against
   LEAK-25 Must]
   Problem: the notes say these are "whole vaults ... migrated". That holds for 8,489 of 8,873 rows. The other 384 are
     178 boot drives (point 1) and 206 scattered data drives. 42.7% of those 206 have one of the five error counters
     above zero (kept No 7.7%, Yes 69.8%), and they bunch in November and December 2025, so they are partly failures
     without a record. The definition cites LEAK-23, which covers follow-up cut on one date and not this case.
     LEAK-22 keeps a competing exit after the prediction point as No (framingham); LEAK-25 drops located unrecorded
     outcomes.
   Effect on the task: small. Keeping the removed rows as No moves test ROC AUC by at most 0.0006 (split auditor). The
     rule record and the notes are what is wrong.
   Evidence: claim auditor 12b and 21; split auditor 4; precedent checker 4.
   Remedy: a note and the rule record, with no change to the rows unless the curator takes the split auditor's option
     B. Correct the notes and issue 4 with the split (8,489 in vault blocks / 178 boot / 206 scattered). Cite LEAK-25
     for the scattered rows and LEAK-22 for why a planned vault migration is or is not a competing event. Name the fact
     that sets this case apart from framingham: the migration is planned before the cut. The December-dip note gets
     one clause: part of the dip is drives that vanish without a record.

4. The shipped table gives two of three test folds away to a method that sees all of it.   [P4; LEAK-9 Should]
   Problem: rows carry no serial, but model, place, slot and power-on hours re-identify a drive across months. The
     March and April test windows hold the whole fleet, and the next month's snapshot is in the same file as a later
     fold's test rows. A drive missing a month later is a drive that failed: the flag alone scores ROC AUC 0.9934
     (April) and 0.9958 (March), against 0.90 for an honest model.
   Effect on the task: none for a harness that hands each method only its split's rows. Any pooled feature step, any
     transductive use, or the kit itself as an input breaks folds r1 and r2.
   Evidence: task gamer, finding 1 (the run's work files).
   Rule: LEAK-9 (Should) puts an evaluation-level leak in a protocol line the benchmark checks, not in the data.
   Remedy: a note, as a protocol line in splits_comment and the README: "a method sees only its split's train rows and
     test window; rows dated after the test window reveal its labels".

5. The year breaks PROV-9, and the record's source links are not this data.   [P5; PROV-9 Must, PROV-8]
   Problem: the definition says 2015 (the first release) and the record says 2013. PROV-9 says a growing monthly or
     quarterly archive "takes the year of the snapshot we pin". We read only Q1 2025 to Q2 2026, and the five growing
     sources of this batch took 2026. The record also lists SurvSet, arXiv 2203.03094 and frailtySurv as sources. These
     are a small, old survival extract (the blind reviewer was misled by them, concern 8).
   Effect on the task: none on the score; the provenance fields are wrong.
   Evidence: precedent checker 8 (R2); blind reviewer 8; record source_links.
   Remedy: repair the field. Set year 2026 in the definition (and the bibtex) and in the record, and keep the 2015
     announcement in the comments. Move the SurvSet and frailtySurv links out of source_links, or mark them as a
     different extract.

6. ROC AUC weighs the part of the ranking the operator never acts on.   [P6; MET-11, MET-6/7/9]
   Problem: the operator acts on the top 0.1% to 1% of the fleet. On the test windows, ROC AUC ranks a 1500-tree model
     third of four, while recall at the top 0.5%, recall at the top 0.1% and average precision rank it first in every
     window. In March a five-counter model ties the full model on ROC AUC (0.886 against 0.887) but catches 18 fewer
     failures in the top 0.5%. The disk-failure literature reports detection at a fixed low false-alarm rate (Hughes et
     al. 2002, Murray et al. 2005).
   Effect on the task: the declared metric can rank models in a different order than the operator's decision would.
     The gaps are a few drives per window, so this shows a direction, not proof.
   Evidence: domain practitioner 5 (the run's work files).
   Rule: the fallback roc_auc is consistent with the rules, because no source fixes a k (MET-6, MET-7) and imbalance
     alone is no reason for PR AUC (MET-9). MET-11 `context` allows the metric the task makes obvious.
   Remedy: a note in the README naming the gap. Put a `context` metric (partial ROC AUC to FPR 1%, or recall in the top
     0.5% per cut) to the curator as a weighing call. I do not ask for the metric to change.

7. Notes understate the label and omit the test cohort.   [P3 documentation; USE-5, USE-8, LEAK-25 note clause, EV-2;
   P7 CLEAN-10/11]
   Problem: "about half proactive" is a count, not a suggestion: Q3 2024 had 640 reactive and 721 proactive failures.
     The proactive share varies with inputs: Dell 73.5%, Storage Pod 6.0 44.6%, AMS 68.1%. The notes do not say that
     the test cohort leaves out drives absent on the cut day (13% of failing drives, 19% in April 2026). They also do
     not record the fact that sets the case apart from xente: no review step on an input; the five-counter rule scores
     0.83 to 0.87 against 0.89 to 0.90 for a model.
   Cheap cleaning: smart_9_raw = 0 on drives that are years old (137 shipped rows); 65535 sentinels in smart_9_raw and
     smart_240_raw (10 and 6 rows). Set them to missing.
   Effect on the task: the fit stays approximate; a reader gets the label right.
   Evidence: claim auditor 10 and 26; precedent checker 1a and 1b; split auditor 5; column auditor E.
   Remedy: notes in curation_comments and fit_reason, plus the sentinel fix. None of this is a reason to hold the
     dataset.

Not argued (checked and dropped):
- The blind reviewer's "label horizon crosses the train/test boundary": refuted. The gap is 29 days and February is
  left out of the March window (claim auditor 22, split auditor 3).
- The blind reviewer's "undocumented subsample": it is documented in version_comment and splits_comment.
- Change features (draft issue 3, CLEAN-19): a P7 weighing call with a mixed gain on one seed. It is no reason against
  shipping.

Judgment record
Verdict: ship after changes.
Validity: LEAK-25 triggered, fix by dropping boot drives. LEAK-10 triggered, fix by dropping slot-empty data-drive rows
  (or the column). LEAK-22/25 rationale corrected, with an effect of 0.0006 or less. LEAK-9 needs a protocol line.
  PROV-9 triggered, year 2026. SPLIT-1/9/10/12/13/14 hold. USE-5 approximate, with notes completed.
Value: TP-4 holds, the rule is below a model. The MET-11 context metric is a curator's weighing call.
Quality: CLEAN-10/11 sentinels; CLEAN-19 is a weighing call.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: backblaze_hard_drive_failure (folder backblaze_hard_drive_failure_1m), 2026-11-09

The advocate concedes my points 1, 2 and 5 with the remedies I asked for: drop the boot drives (LEAK-25), drop the
data-drive rows with an empty slot (LEAK-10), and set the year to 2026 (PROV-9). The two briefs now differ only on how
two notes are worded. Both ask for "ship after changes", with the same changes to the definition.

A1 (a real task; the label is fit approximate). CONCEDE. USE-5 holds with fit approximate. The rule scores 0.83 to
   0.87 against 0.89 to 0.90 for a model, and 21% to 28% of positives have all five counters at zero. My point 7 asked
   only for notes: the 47.0% / 53.0% count, the spread by server type and datacenter, and the fact that sets this case
   apart from xente. The advocate asks for the same.
A2 (the split is honest). CONCEDE. I had already dropped the blind reviewer's look-ahead and subsample concerns. One
   residue, not a new point: the claim auditor left I5 untested (SPLIT-9). On training rows the removal filter reads
   `last_seen` over the whole release, beyond the refit. The likely size is a handful of rows, so a sentence will do.
A3 (pod_slot_num). Agreed; it is conceded as my point 2. I add one thing. The fix also makes the cohort consistent:
   drives absent on the cut day are already left out, and slot-empty drives are in the same out-of-service state. The
   note on the 187 absent failing drives (13%) should say so.
A4 (boot drives). Agreed; it is conceded as my point 1.
A5 (cross-fold exploit "not a flaw of the definition"). PARTLY DISPUTE. I agree the data does not change. But LEAK-9
   (Should) asks for "a protocol line the benchmark checks", not only a README sentence. The shipped container is the
   whole table, and two of three folds score 0.993 to 0.996 from it. The line belongs in splits_comment, where a
   harness and a reader see it. It should name the mechanism: rows dated after a test window reveal its labels through
   the re-identified drive. Then a method that pools the table can be called out, as LEAK-9's cases are.
A6 (the drop of removed drives is consistent and moves nothing). CONCEDE the outcome: the effect is 0.0006 AUC or less,
   and I ask for no change to the rows. DISPUTE the citation. The advocate would cite LEAK-25 and CLEAN-15 only. LEAK-25
   covers the 206 scattered drives, which may be unrecorded failures. It does not cover the 8,489 vault-block exits:
   they are an exit after the prediction point, and LEAK-22 (Must) covers that case (framingham keeps such rows as No).
   "Planned, so known at the cut" is the fact that would set this case apart, but the release does not record the
   plan, and the drop uses the realised removal (split auditor 4). The rule record must name LEAK-22 and that fact, or
   the curator takes option B (keep them as No, a one-line change). That choice is the curator's.
A7 (metric, cleaning, metadata). CONCEDE. roc_auc is rule-consistent. My point 6 asked only for a README note, with a
   MET-11 context metric left as the curator's weighing call. The sentinel fixes and the year are the same in both
   briefs.

Settled with the advocate: the boot-drive drop, the slot-empty drop, year 2026, the notes on the label and the cohort,
and the sentinels set to missing. Left for the curator: the wording of the LEAK-9 protocol line, whether the vault-block
removals are recorded under LEAK-22 or kept as No (option B), the MET-11 context metric, and change features
(CLEAN-19).

</details>
