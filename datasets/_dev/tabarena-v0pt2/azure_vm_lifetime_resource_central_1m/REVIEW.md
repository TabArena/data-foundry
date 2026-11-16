# azure_vm_lifetime_resource_central

**Outcome:** added as `azure_vm_lifetime_resource_central_1m`. The AI recommends shipping it: the review panel's changes are made, and two calls are left to you, and the AI recommends what is implemented in both: issue 1 confirms the deployment's count of the previous 5 minutes in place of its same-slot count; issue 2 is a weighing call on the window length. Changes made, needing no decision: the subscription's count of VMs created in the same 5 minutes is dropped; a protocol line forbids reading other test rows, since a participant who links a deployment's later test rows lowers log loss by 0.115 to 0.203 per window; the subscription's 24-hour creation count is missing on the first day where VMs ran before the trace; the trace's day of week ships as a number; and the notes now say that the trace's deployment is a subscription's VMs of one day, not one request, that the scheduler can ask for the class (the paper envisions it, Azure later built it), how unequal the groups of VMs one deployment creates in one 5-minute slot are (they share every feature) and how far counting each group once reorders models; and the first draft's false reason for 3-day windows (that nothing longer keeps half the rows for training) is replaced by the true one (issue 2). The task follows Resource Central (Cortez et al., SOSP 2017) on Microsoft's public Azure VM trace (V2, 2019, one region, 30 days): when a VM is created, will it live up to 15 minutes, 15 to 60 minutes, 1 to 24 hours or longer, given its size class, the time and its deployment's and subscription's history to that moment? 2,409,604 VMs (1,801,766 shipped after sampling the train sides), 17 features; three 3-day test windows (234,507 to 281,121 VMs, at least 11,847 per class), each training on a random 1M of the VMs created at least 24 h 10 min earlier; fallback `log_loss`.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2, SEL-16 hold; USE-1 holds, fit direct ("asks" corrected to "can ask": the paper envisions the use in Sec. 4.1, and Barbalho et al., MLSys 2023, built it); LEAK-10 holds for the 12 history features (the trace cut at a slot gives every row of that slot the same features, 0 mismatches, also without the slot's other VMs), triggered by the same-slot counts and fixed by dropping `subscription_vms_in_slot` and lagging the deployment's count (issue 1, LEAK-10 clause 2); LEAK-24 holds (rows cut by creation time, no label censored); LEAK-9 triggered (a chain through the cumulative counts) and fixed by a protocol line and a kept-on-purpose note; SPLIT-9, SPLIT-10, SPLIT-13, SPLIT-14 hold; SPLIT-12's stated reason was false and is corrected (the length is issue 2); PROV-13 holds.
Value: TP-1 to TP-9 no flag (random forest 0.925 against the dummy's 1.231, better in 3 of 3 windows); MET-5 fallback `log_loss` holds; MET-17 note added (scored per VM, with the group sizes and the ranking under one vote per group).
Quality: CLEAN-14 (`trace_day_of_week` a number) and CLEAN-1 / CLEAN-19 (`subscription_vms_created_24h` missing on day 0) fixed.
Weighed (priority 5): gap + (multiclass classification is thin among the accepted definitions); use case + (the paper names the scheduler and its placement decision, fit direct); source + (Microsoft's documented first-party trace with its SOSP paper, CC BY 4.0); shape + (2.4M VMs, 17 features, temporal); risk 0 (the look-ahead is lagged out, the chain through later test rows is covered by the protocol line, and the window length changes no row or label). The missing inputs (exact size, operating system, service) and at most 29 days of history make the task harder, not different.
For the curator: issue 1 (the deployment's same-slot count: lag, drop or keep; the lag is implemented and recommended); issue 2 (window length: 3 days as an exception, implemented and recommended, or 4 or 4.5 days; a weighing call). The bundle check's two warnings are proposed for acceptance (not written into `accepted_check_warnings`), and your ship verdict accepts them: `dataset_duplicate_rows`, "The VMs of one deployment created in one 5-minute slot share every feature (up to 918 VMs; a deployment is a subscription's VMs in the region that day), so 62.7% of the rows copy another. They are distinct VMs, scored per VM as in the paper, and the rows of one slot are always on one side of a split (0.0% of test rows have a copy in train)."; `dataset_conflicting_duplicate_rows`, "VMs of one deployment-slot group that live for different times (41.7% of the groups with several VMs mix classes; 5.7% of the rows): variation within a group that the features cannot resolve, not recording noise."

**Main points:** Confirm that the deployment's VMs of the previous 5 minutes replace its same-slot count, which may include VMs that arrive later (issue 1, implemented, recommended); keep 3-day test windows as an exception to the source's horizon or lengthen them to 4 or 4.5 days (issue 2, 3 days implemented, a weighing call); your verdict also accepts the two duplicate-row warnings.

**Record fields that disagree with the definition:**

- `original_source`: record `Company`, definition `GitHub`.
- `year`: record `(none)`, definition `2019`.

**Record judgment:** valid. Microsoft's first-party Azure VM trace (V2, 2019) with the Resource Central paper; the screening's counts and risks hold, and the build met each risk it named. Two readings of the screening are corrected: the paper's scheduler change uses the utilisation prediction (Sec. 5), while the lifetime use is envisioned (Sec. 4.1) and was built later (Barbalho et al., MLSys 2023), so the fit stays direct; and the trace's deployment id is the paper's regrouping of a subscription's VMs in one day, not a request.

**Issues for Lennart:**

1. **Count the deployment's VMs of the previous 5 minutes instead of the same 5 minutes, drop the count, or keep the same-slot count?**

   * **Problem:**
     - The first draft's `deployment_vms_in_slot` counted the deployment's VMs created in the same 5-minute slot as the row's VM, and the trace cannot tell which of them came after it, so the count may include VMs that arrive up to 5 minutes later.
     - The trace's deployment is not the request being placed but all of a subscription's VMs in the region that day, which arrive slot after slot (78% of rows), and the deployment's VMs of the next 5 minutes, which also arrive after this VM but can be counted apart, lower log loss when added as a feature, so the same-slot VMs that arrive after this one may help a model too[^l10].
     - The definition now counts the deployment's VMs of the previous slot instead (`deployment_vms_prev_slot`, known at creation), and whether to keep that, drop the count or keep the same-slot count with a note is a case-by-case call the rule leaves to you.
   * **Background:**
     - The paper lists "deployment size" among the inputs the scheduler passes in[^rc4], but redefines a deployment as "the set of VMs from each subscription that are deployed to a region during a day"[^rc34]; the trace's day boundary (trace second 80,700) is crossed by none of its 28,208 deployments, so the deployment is known at creation.
     - No outcome sits in the count: if failed VMs were replaced within the slot, groups of two VMs created together would, more often than chance, hold exactly one VM that lived a single 5-minute reading, and they hold one less often (7,852 groups against about 11,400 expected if the two lived independently).
     - The subscription's same-slot count (equal to this one on 98.2% of rows, the rest other deployments' VMs of the same 5 minutes) is dropped; the panel agreed on that.
   * **Effect on the task:** with the same-slot count, a model reads part of the deployment's next few minutes, which the scheduler placing this VM does not know; the lag removes that and changes the honest score by nothing measurable.
   * **Experiments:** mediator, LightGBM (300 trees, 63 leaves), 3 seeds per window, each with its own random 1M of the train side; change in log loss against keeping the same-slot count (negative: lower, better), the mean of the 3 seeds, windows newest first:

     | Variant | Window 0 | Window 1 | Window 2 | Over the 9 fits |
     |---|---|---|---|---|
     | Drop the count | +0.013 | -0.023 | +0.018 | +0.003 (SD 0.020) |
     | Control: add a random column | +0.001 | -0.001 | +0.004 | +0.0015 (SD 0.0095) |
     | Add the next slot's arrivals (pure look-ahead) | -0.011 | -0.026 | -0.001 | -0.013 (lower in 8 of 9) |
     | Lag: the previous slot's count instead (implemented) | +0.001 | -0.024 | +0.014 | -0.003 (SD 0.022, lower in 4 of 9) |

   * **Consistency:**
     - The lag follows distribution_transformers_at_cauca_department, whose looked-up values went because a gain might sit on the part that came late[^dt].
     - Keeping the same-slot count would follow medical_facility_operational_data in kind, whose counts that include later bookings stayed with a note, but there the part that could be traced showed no gain and here it shows one (-0.013, 8 of 9 fits): the fact that sets the two apart[^mf].
   * **Panel:**
     - Keep (advocate): the paper names deployment size as a scheduler input, there is no outcome mechanism, and the whole field's worth sits within about two noise SDs, as in medical_facility.
     - Measure, keep within noise, else drop (critic, and the advocate in the rebuttals): both sides agreed that a 3-seed test of the count alone would decide, and it came out within about two noise SDs in each window, so on that test alone the count stays; the rule counts such a no-change test alone as no reason to keep[^l10].
     - Lag (mediator): the whole field's test says keep, but the rule's own test on the part that can be traced shows a gain, and the lag, the mildest fix in the definition, costs nothing measured[^ladder].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Lag (implemented) | `deployment_vms_prev_slot`, the deployment's VMs created in the previous 5-minute slot, replaces the same-slot count | no look-ahead; scores as keeping does (0.003 lower log loss, within noise); an assert checks that it is known at creation | a feature of ours, not the paper's deployment size |
     | B | Drop | no count of the deployment's recent arrivals; its counts to date stay | the simplest; no look-ahead | drops a count of recent arrivals the scheduler has at creation; scores as keeping does (0.003 higher log loss, within noise) |
     | C | Keep the same-slot count with a note | `deployment_vms_in_slot` back, with the numbers above in the notes | nearest the paper's deployment size input; follows medical_facility in kind | reads up to 5 minutes of later arrivals, whose measurable twin carries a gain; departs from distribution_transformers without a fact that sets it apart; an exception to a Must rule |

   * **Recommendation:** A: the deployment's VMs of the next 5 minutes, the measurable stand-in for the VMs counted after this one, lower log loss, so the same-slot count goes; the lag keeps a count the scheduler has and costs nothing measured, while dropping scores the same but loses that count. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: nothing to change.
   - B: in `_history_features`, remove `prev_slot`, its join, the assert and `deployment_vms_prev_slot` from the select; rewrite the deployment sentence of the features bullet, the LEAK-9 note's link (the chain then links through `deployment_vms_before` and the size classes alone), `task_summary.known` and `task_summary.changes`; re-run `dataset check`, the leak and task probes.
   - C: put back the same-slot count (`vm.group_by(["deployment_id", "created"]).len()` joined on `t`, this VM included) as `deployment_vms_in_slot` in place of `deployment_vms_prev_slot`; replace the features bullet's lag sentence by a "Potential leak, kept on purpose" note with the experiments above; record `**Exception to LEAK-10 (<date>, Lennart):**` with the fact that sets it apart and a Cases row in leak_checks.md; the same re-runs. The mediator's scripts are `ablate_dep_slot.py`, `trace_late_part.py`, `random_col_control.py` and `lag_variant.py` in the run folder.

   [^l10]: **LEAK-10** (Must), second clause (amended 2026-10-26 and 2026-11-08, Lennart): a value whose late part cannot be located row by row goes when it may carry a gain, and stays with a note only when the part that can be traced shows none; a case-by-case judgment of the curator, never a default; 'a "removing it changes no score" test alone is still no reason to keep' (2026-10-21).
   [^rc4]: Cortez et al., SOSP 2017, Sec. 4: "Examples of client inputs are subscription id, VM type and size, and deployment size"; **USE-6**: an input the actor has at the prediction point is a feature.
   [^rc34]: Cortez et al., SOSP 2017, Sec. 3.4 (https://doi.org/10.1145/3132747.3132772); the V2 page (https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md): "we define a 'deployment' differently than Azure in our paper".
   [^dt]: leak_checks.md, Mechanisms, LEAK-10 (decision, Lennart, 2026-10-21): distribution_transformers_at_cauca_department, `power_kva` and `installation_type` dropped, "no amendment for a gain that may sit on the changed rows".
   [^mf]: medical_facility_operational_data (Lennart, 2026-11-05): schedule counts that include later bookings kept with a note, "the whole-field worth is an upper bound on the late part, and it sits within about two seed SDs".
   [^ladder]: principles.md, the remedy ladder: repair from the origin; fix the definition (drop, lag, filter, re-split, re-target); keep it with a documented note; exclude the dataset.

2. **Keep 3-day test windows as an exception to the source's horizon, or lengthen them to 4 or 4.5 days?**

   * **Problem:**
     - The paper trains on two months and tests on the next month, which a 30-day trace cannot hold, so the test windows have to be shorter than the source's horizon[^s12].
     - The first draft's reason for 3 days, that nothing longer keeps every train side above half the rows[^s14], was false: the oldest window's train side holds 59.9% of the rows at 3.5 days, 55.2% at 4 days and 50.8% at 4.5 days.
     - Keeping 3 days (implemented) is an exception resting on one fact, train sides of 65% or more, while 4 or 4.5 days come as near the source's month as the rule of at least half the rows on every train side allows, as the precedents do.
   * **Background:**
     - Each day added to the windows takes about 10 points from the oldest train side (65.2% at 3 days, 55.2% at 4), since the three windows grow together.
     - Within a 3-day window, log loss shows no decay with the distance to the refit (by day, the newest window 1.043 / 0.941 / 0.908, the middle one 0.777 / 0.978 / 0.864, the oldest 0.868 / 0.922 / 0.842); the swings come from the days.
     - The paper gives no refit cadence; Azure's later production model is retrained weekly[^barb].
   * **Effect on the task:** longer windows test each model on more days after its refit, nearer the paper's month; shorter windows train each model on more of the past, nearer the paper's two months of training; the rows, features and labels stay the same.
   * **Experiments:** the oldest train side holds 65.2% of the 2,409,604 kept VMs at 3 days, 59.9% at 3.5, 55.2% at 4 and 50.8% at 4.5 (precedent checker); the day-wise log loss above is one untuned LightGBM fit per window (split auditor). No score decides the length[^s21].
   * **Consistency:** medical_facility_operational_data moved to its source's 14 days, and the house-price datasets each keep their own source's horizon[^s12c]; keeping 3 days needs an exception with its fact[^exc].
   * **Panel:**
     - 3 days (advocate): train sides of 65 / 76 / 85% are larger and more like the application, and no decay shows within a window.
     - Toward 4 days (critic): the rule's default is the source's horizon and the precedents follow theirs as far as they can; no decay within a window means a longer window costs no staleness, so that fact points to 4 days, and a weekly retraining is nearer 4 days than 3.
     - Mediator: nothing ranked higher settles it; a weighing call.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 days, an exception (implemented) | windows of 864 five-minute slots over the last 9 days; train sides 84.7 / 76.2 / 65.2% | the largest train sides, nearer the paper's two months of training; no rebuild | shorter than the 4 to 4.5 days the half-the-rows floor allows; an exception to the source's horizon that rests on one fact |
     | B | 4 days | windows of 1,152 slots over the last 12 days; the oldest train side 55.2% | nearer the paper's month and a weekly retraining; no exception; as medical_facility | the oldest train side near half the rows; a rebuild and new probes |
     | C | 4.5 days | windows of 1,296 slots over the last 13.5 days; the oldest train side 50.8% | the nearest to the paper's month the floor allows | within a point of the floor; a rebuild and new probes |

   * **Recommendation:** A, recorded as an exception (the AI's lean; the mediator leaves it open): in a 30-day trace each day added to the windows takes about 10% of all rows from the oldest train side, and the length changes no row, feature or label; B if you weigh the source's horizon higher, as for medical_facility, and read the missing decay as the critic does (a longer window costs no staleness). A weighing call. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: add to the record `**Exception to SPLIT-12 (<date>, Lennart):** 3-day test windows, shorter than the 4 to 4.5 days a 30-day trace allows above the SPLIT-14 floor: every train side holds 65% or more of the rows (84.7 / 76.2 / 65.2%), where 4-day windows leave the oldest 55.2%. Serves P4: train sides nearer the paper's two months of training per month tested.` and the row of kind `exception` in the Cases table of splits.md; `splits_comment` already says it.
   - B: `WINDOW_SLOTS = 1152`; update `splits_comment` (the windows, the train shares, the low-volume days per window), `task_summary.split` and `version_comment`; check that no test window passes 500k rows (3-day windows hold 234,507 to 281,121); re-run `dataset check`, the leak, task and hidden-group probes.
   - C: as B with `WINDOW_SLOTS = 1296`.

   [^s12]: **SPLIT-12** (Should): "The horizon is a human judgment from the source: how far ahead the actor predicts ..., the competition's own test window, the refit cadence. Choose the test windows to match it and write the reasoning down." The paper trains on two months and tests on the next (Cortez et al. 2017, Sec. 6.1).
   [^s14]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50% of the data; "a smaller train side is too unlike the real application".
   [^barb]: Barbalho et al., "Virtual Machine Allocation with Lifetime Predictions", MLSys 2023 (https://proceedings.mlsys.org/paper_files/paper/2023/hash/48eb2c79643df5cb7d125945238bd7d0-Abstract-mlsys2023.html), as read by the domain practitioner.
   [^s21]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test windows.
   [^s12c]: splits.md Cases: SPLIT-12 / SPLIT-19, medical_facility_operational_data, nine 14-day windows as the source tests (Lennart, 2026-11-05); SPLIT-12, the house-price family, each with its own source's horizon (Lennart, 2026-10-21).
   [^exc]: principles.md, "Exceptions and amendments": an exception departs from a Should rule for one dataset and names the fact that sets the case apart and the higher principle it serves.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. The panel worked on the definition before the changes (1,801,772 rows shipped; 13 history features with both same-slot counts; the cut-trace test on 16,222 rows at 55 slots); the final definition ships 1,801,766 rows and 12 history features, and its cut-trace test covers 23,436 rows at 63 slots, 0 mismatches. Claim audit: 35 claims; no validity claim refuted, and the history features hold under the trace cut at 55 slots (16,222 rows, 0 mismatches) and a re-implementation on 3,700 rows; refuted and fixed: "the scheduler asks" (the paper envisions it), the day-0 meaning of `subscription_vms_created_24h`, the README's "kept" count, and the missing fact that a trace deployment is a subscription's VMs of one day. Column audit: no leak; `trace_day_of_week` typed as a number and the day-0 count fixed; the subscription's same-slot count dropped. Split audit: right with notes; the 24 h 10 min gap is needed (without it the model scores worse than the dummy in two windows). Domain practitioner: fit direct; keep `log_loss` per VM, with the group sizes and the core-time caveat in the notes (done). Precedent check: four departures, three fixed (day of week, MET-17 note, subscription count) and one now issue 2. Blind review: include with changes; its main concerns were the duplicates from batch creation (scored per VM, with a note) and `created` (kept: the gap makes it harmless). Task gamer: a chain through the cumulative counts reads a deployment's later test rows (0.115 to 0.203 lower log loss per window); a protocol line now. Debate: agreed on the history features, the drops, the gap, the LEAK-9 line and the fixes; disputed: the window length (issue 2); on the deployment's same-slot count both sides agreed a 3-seed test would settle it; the mediator's test put its worth within noise but found a gain on the next slot's arrivals, so the mediator recommends the lag (issue 1). The mediator's third point, a Tensions row for a known entity's history against label-based counts, is a rule change, proposed as an item across datasets.

<details><summary>Mediator</summary>

MEDIATOR REPORT: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09
Inputs: every panel report (claim, column, split auditors, domain practitioner, blind reviewer, task gamer,
precedent checker, advocate and critic briefs with rebuttals), builder_report.md, dataset.py, principles.md,
LEAK-9 / LEAK-10 (leak_checks.md), SPLIT-12 / SPLIT-14 (splits.md), MET-17 (metrics.md).
My runs: the run's work files (ablate_dep_slot.py, trace_late_part.py, random_col_control.py, lag_variant.py,
attribute_w0.py, with their .log/.json). All on the split auditor's full frame (dataset.py's own _history_features,
2,409,604 rows), shipped windows, the agreed fixes applied.

**1. RECOMMENDATION (judgment record)**
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds (direct fit; "asks" -> "can ask", MLSys 2023); LEAK-10 holds for the 13
  history features (censored-trace test on dataset.py, 16,222 rows x 13 features, 0 mismatches); LEAK-10 clause 2
  triggered by the same-slot counts: subscription_vms_in_slot dropped (agreed), deployment_vms_in_slot: lag it
  (issue 1, the curator's call under the clause); LEAK-9 triggered (chain exploit, -0.12 to -0.20 log loss), fixed by
  a protocol line and a "Potential leak, kept on purpose" note; LEAK-24 holds; SPLIT-9, SPLIT-10, SPLIT-13, SPLIT-14
  hold; SPLIT-12 reason false, corrected (length: issue 2); PROV-13 holds.
Value: TP-1 to TP-9 pass (random forest 0.920 vs dummy 1.231, 3/3 windows; smallest class per test fold 11,847);
  MET-5 fallback log_loss holds; MET-17 note added.
Quality: CLEAN-14 (trace_day_of_week numeric) and CLEAN-1/CLEAN-19 (subscription_vms_created_24h on day 0) fixed.
Weighed: source + (first-party production trace, CC BY 4.0), fit + (direct), gap - (missing inputs, 29-day history),
  size +.
For the curator: issue 1 (deployment_vms_in_slot: lag, drop or keep; LEAK-10, Must, clause 2 is a case-by-case
  call); issue 2 (window length, 3 d with an exception or 4 d; SPLIT-12, a weighing call); issue 3 (a Tensions row
  for known-entity history vs CLEAN-6; rule maintenance).

**2. THE DECISIVE MEASUREMENT (deployment_vms_in_slot)**
Settings as the split auditor's noise run (noise.py): LightGBM 300 trees, lr 0.05, 63 leaves, subsample 0.8,
colsample 0.8, seeds 1/2/3, each seed its own random 1M of the train pool; shipped windows (gap 87,000 s);
subscription_vms_in_slot dropped; trace_day_of_week numeric; subscription_vms_created_24h missing before 86,400 s in
subscriptions with pre-trace VMs (87,870 rows). Each comparison is paired (same sample and seed). Log loss, w0/w1/w2.

  agreed feature set (keep)          1.0111 1.0002 1.0131 / 0.8661 0.8844 0.8681 / 0.8528 0.8507 0.8507
  A. drop deployment_vms_in_slot     change +0.019 +0.004 +0.017 / -0.015 -0.022 -0.031 / +0.015 +0.016 +0.024
                                     per window +0.013 / -0.023 / +0.018; over 9 fits +0.003 (SD 0.020)
  B. control: add a random column    change +0.009 +0.000 -0.005 / +0.010 -0.018 +0.006 / -0.006 +0.007 +0.010
                                     over 9 fits +0.0015, SD 0.0095 (the noise of changing the column set)
  C. add the deployment's arrivals   change -0.019 -0.004 -0.010 / -0.041 -0.022 -0.016 / -0.006 -0.004 +0.008
     in the NEXT 5-min slot          per window -0.011 / -0.026 / -0.001; over 9 fits -0.013 (8 of 9 lower)
     (pure look-ahead)
  D. lag: replace it by the          change +0.002 -0.013 +0.012 / -0.002 -0.049 -0.020 / +0.013 +0.021 +0.009
     deployment's VMs created in     per window +0.001 / -0.024 / +0.014; over 9 fits -0.003
     the previous slot (known at t)
  Fact: 77.8% of rows sit in a deployment that also creates VMs in the next slot (78.2% in the previous one).

Reading.
- A (the agreed test): the whole-field worth is mixed in sign and within about two noise SDs in each window
  (0.013 and 0.018 against 0.0095; window 1 is better without it). On medical_facility's footing alone, that is a keep.
- C traces the part that A cannot locate: arrivals of the same deployment shortly after the VM. They lower log loss by
  0.013 on average (8 of 9 fits, up to 0.041), against +0.0015 for a random column. The within-slot late part is the
  same kind of value (arrivals 0-5 min later), and in this trace it is common: deployments are subscription-day groups
  that create VMs slot after slot (78%), not single requests.
- LEAK-10 clause 2 keeps an unlocatable late part with a note "only when the part that can be traced shows none"; here
  it shows a gain. That is the fact that sets this case apart from medical_facility (whose late part showed none) and
  puts it with distribution_transformers.
- D: the lag removes the look-ahead and keeps the field's worth (over 9 fits -0.003 against keeping; 0.006 better than
  dropping). Lag is the "fix the definition" rung, below "keep with a note" on the ladder, and costs nothing measured.
Recommendation: replace deployment_vms_in_slot by deployment_vms_prev_slot (the deployment's VMs created in the
previous 5-minute slot). The clause makes it the curator's case-by-case call, so it is issue 1, not a change made
without a decision.

Side measurement (attribute_w0.py, window 0, seed 1): the split auditor's 0.952 becomes 0.979 after dropping
subscription_vms_in_slot, 1.019 with trace_day_of_week numeric as well, 1.011 with all three agreed fixes. Single seed,
an untuned model whose single splits move by up to 0.13 (task gamer). Not a reason against the fixes: dtypes are set
from context (CLEAN-14), and a drop under LEAK-10 is not undone by a score.

**3. CHANGES TO MAKE NOW (no decision needed)**
 1. Drop subscription_vms_in_slot. LEAK-10 clause 2, CLEAN-5 (equal to deployment_vms_in_slot on 98.2% of rows; its
    extra part is other deployments' arrivals in the same 5 minutes); precedent distribution_transformers.
 2. Fix the "one request" wording everywhere: the curation_comments feature bullet ("taken as one request"), the
    duplicates bullet ("one request"), task_summary.known ("how many VMs its request ... create at once"), and the
    accepted-warning texts. Say: the trace's deployment is a subscription's VMs deployed to the region in one day (V2
    page: "we define a 'deployment' differently than Azure"; paper Sec. 3.4), assigned by a fixed daily boundary at
    trace second 80,700 (0 of 28,208 deployments cross it), so the counts are known at creation. writing.md; USE-1.
 3. Add accepted_check_warnings for dataset_duplicate_rows and dataset_conflicting_duplicate_rows with the builder's
    texts, reworded as in 2 ("VMs of one deployment created in one 5-minute slot", up to 918; 62.7% duplicate rows;
    0.0% of test rows have a copy in train; 41.7% of multi-VM slot groups mix classes). LEAK-16 to LEAK-21.
 4. LEAK-9 protocol line and note (agreed; counts not rounded): "- Potential leak, kept on purpose (LEAK-9, an
    evaluation leak): deployment_vms_before is cumulative, so a deployment's later test rows link to its earlier ones
    (the next slot's before = before + in-slot count, matched on the size buckets; 90% of rows link), and along the
    chain the deaths (before - running) and the subscription's per-class counts (share x known count, an integer on
    100% of rows) reveal the current cohort's lifetimes up to 24 h ahead. A participant who reads the later test rows
    lowers log loss from 0.866 to 0.730 (regularised LightGBM; -0.169 / -0.125 / -0.115 per window) and from 0.920
    to 0.741 (untuned; -0.155 / -0.203 / -0.180), a lower bound. Each test VM is predicted from the training rows and
    its own features only; no feature or model step may use other test rows, and a method that does is called out
    and not benchmarked (LEAK-9 as amended 2026-11-05, as for medical_facility_operational_data)." List the
    benchmark-side check in BENCHMARK_CHANGES_TODO.md. If issue 1 ends in the lag, the chain still links (before =
    previous before + previous-slot count, read backwards), so the line stays; say the numbers were measured with
    the same-slot counts. Rule mapping and novelty: section 5.
 5. Use case: "can ask" for "asks", in task_summary.use_case and in the prediction-point bullet ("the scheduler asks
    for its lifetime class"), citing Cortez et al. 2017 (Sec. 4.1) and "as Azure's allocator later did (Barbalho et
    al., MLSys 2023)". USE-1 (fit stays direct); writing.md.
 6. README decision 1 table: "kept" = 2,409,604 from the row filter (2,695,548 - 227,316 - 58,628), plus a row
    "shipped after sampling the train sides: 1,801,772". writing.md.
 7. MET-17 note: per VM stays (the scheduler places each VM; RC Table 4 counts per VM). Give: about 4 VMs per
    deployment-slot group in the test windows (64,568 / 57,640 / 58,788 groups); rows in groups over 100 VMs 4.8 /
    12.3 / 5.1%; over 24 h is 5.5 / 5.1 / 5.9% of VMs but 8.9 / 8.2 / 8.4% of groups; one vote per group reorders four
    feature-set variants at Kendall tau 0.00 / 0.33 / 1.00 (indicative: four variants of one learner); per-VM log loss
    weighs the short classes (42.5% of VMs, 0.7% of core-time) over the long one (5.7%, 79.9%), and no source fixes a
    resource weight (MET-7). Call the unit a deployment-slot group, not a request (change 2). MET-17.
 8. subscription_vms_created_24h: missing for t < 86,400 in subscriptions with pre-trace VMs (87,870 rows, 3.65%,
    training sides only), and the note says so. CLEAN-1, CLEAN-19; precedent g_research_crypto_forecasting_1m.
 9. trace_day_of_week as int 0..6: drop .astype(str) and the categorical entry; update the bullet. CLEAN-14 cycle
    rule; precedent rossmann_store_sales.
10. Smallest class per test fold 11,847 (not 10,077) wherever written. writing.md.
11. Horizon: remove the false reason ("the 30-day trace allows windows of 3 days"; builder: "nothing longer under
    SPLIT-14"). The replacement text follows issue 2. SPLIT-12; writing.md.
12. Smaller fixes raised by one auditor, not disputed (writing.md): the deployment table's size is "the most VMs the
    deployment ran at once" (86.7%), not a whole-trace count; "12-13%" -> "11.9-13.4%" for the top subscription; the
    verification sentence cites the censored-trace test on dataset.py (16,222 rows x 13 features at 55 slots, 0
    mismatches; 3,700-row re-implementation incl. subscription_mean_p95_max_cpu and subscription_vms_class_known),
    not the 300-row check on the prototype; one splits_comment sentence that the newest window holds no low-volume
    day and the three together hold one of each kind (SPLIT-20, split auditor N2); one sentence that `created` is a
    trend counter kept harmless by the gap (no-gap fit 1.331 with it, 0.938 without; split auditor N4).

**4. ISSUES FOR THE CURATOR (ranked: validity first, Must first)**
Issue 1 (P4, LEAK-10 Must, clause 2: case-by-case curator judgment). deployment_vms_in_slot: lag, drop or keep?
  Problem: it counts the deployment's VMs created in the same 5-minute slot, so it may include VMs that arrive after
    this one; the trace cannot order them. The trace's deployment is a subscription-day group, not one request.
  Effect: the field is worth +0.013 / -0.023 / +0.018 log loss (3 seeds each); its traceable twin, arrivals in the
    next slot, is worth -0.013 on average (8 of 9 fits). See section 2.
  Advocate's best evidence (keep): the paper lists "deployment size" as a client input (Sec. 4, USE-6); no outcome
    mechanism (one-zero-life pairs 7,852 against ~11.4k expected); the whole-field worth is within about two noise
    SDs, medical_facility's footing; the critic agreed in advance to keep if within noise.
  Critic's best evidence (measure, drop if it carries a gain): distribution_transformers (dropped when a gain may sit
    on the late part); medical_facility kept only because the late part showed none.
  Mediator: the agreed test (A) says keep; the clause's own test (C) says the traceable part carries a gain. The trace
    has no request id: 78% of rows sit in deployments that create VMs in the next slot, so the column is a binned
    arrival count, not the client's request size.
  Options: (a) lag: replace it by deployment_vms_prev_slot (recommended; -0.003 against keeping, no look-ahead);
    (b) drop it (+0.003 against keeping); (c) keep with a note giving the numbers of section 2, departing from
    distribution_transformers (needs a fact that sets it apart).
  Decision needed: (a), (b) or (c).

Issue 2 (P4, SPLIT-12 Should, a weighing call). Window length: 3 days with a true reason, or 4 days?
  Problem: the paper tests on a month; the 30-day trace cannot hold it. The stated reason for 3 days is false: the
    oldest train side is 59.9% at 3.5 d, 55.2% at 4 d, 50.8% at 4.5 d (precedent checker), all above SPLIT-14's 50%.
  Advocate's best evidence (3 d): train sides 65 / 76 / 85%, larger and more like the application (SPLIT-14's why);
    no decay within a window (day-wise log loss shows none); the three windows together hold one of each kind of
    low-volume day.
  Critic's best evidence (toward 4 d): SPLIT-12's default is the source's horizon, and the precedents follow theirs as
    far as they can (medical_facility moved to the source's 14 days; house-price family); no decay within 3 days means
    a longer window costs no staleness, so that fact points to 4 d, not 3 d. Also: Azure's production retrains weekly
    (Barbalho et al., per the domain practitioner), and 4 d is nearer that cadence than 3 d.
  Rule: SPLIT-12 is a Should; keeping 3 d is an exception that names its fact (train sides of 65% or more) and serves
    P4; 4 d follows the rule with no exception. Nothing ranks above to settle it.
  What would settle it: the curator's weighing; scores do not (SPLIT-4: the split follows the application).
  Options: (a) 3 d, recorded as an exception to SPLIT-12 (fact: train sides >= 65%); (b) 4 d (1,152 slots; oldest
    train side 55.2%; rebuild); (c) 4.5 d (50.8%, within a point of the floor).
  Decision needed: (a), (b) or (c).

Issue 3 (rule maintenance, low). A Tensions row for known-entity history against label-based counts.
  The subscription's class shares are label-based counts (CLEAN-6, Must, P7) that USE-10/LEAK-34 (Musts, P3/P4) keep
  as a known entity's dated history; no Tensions row or CLEAN-6 narrowing says so (precedent checker). Proposed row:
  the history wins, as of the time each label is known; cases tunisian_fraud_detection_challenge (2026-11-05) and this
  dataset. Decision needed: add the row, or not.

**5. THE TASK GAMER'S EXPLOITS, MAPPED**
- Exploit 1 / 1a (chain through cumulative counts, -0.115 to -0.203 per split; naive link -0.072 to -0.114): LEAK-9
  (Should, amended 2026-11-05), "a model can read other test rows". Not LEAK-10: each row passes the censored-trace
  test, and the exploit needs rows created up to 3 days after the prediction point. NEW: the definition has no
  "Potential leak, kept on purpose" note and no accepted warning about it. Remedy: change 4 (protocol line and note,
  as medical_facility, frempl, ppnn, bank_marketing). The gamer's rounding fix is not taken: LEAK-9 fixes evaluation
  leaks in the scoring, not the data, and it leaves 0.015 of gain.
- Same-slot counts (gamer: "signal"): LEAK-10 clause 2, issue 1 and change 1.
- Missing shares for new subscriptions, row order, formats, copies across the split: no finding (consistent with the
  split and column auditors).
- Lookup of the public vmtable: the usual lookup any public dataset allows; not ranked (as elsewhere).

**6. AGREED FACTS**
- Source: Azure Public Dataset V2 vmtable, 2,695,548 VMs, 6,687 subscriptions, 30 days, one region, 2019; CC BY 4.0;
  cite SOSP'17. Kept 2,409,604 (227,316 pre-trace and 58,628 late VMs dropped); shipped frame 1,801,772.
- Target: Table 3 classes, 42.3 / 27.3 / 24.7 / 5.6% shipped; no label censored (assert; 0 violations).
- History features as of creation: builder 300 rows, column auditor 300 rows, claim auditor 16,222 rows x 13 features
  (censored trace, dataset.py's code) and 3,700 rows independently: 0 mismatches. Blind reviewer: over-24-h share is
  exactly 0 in the first 24 h.
- Dropped outcome columns correct: vm_category (Unknown for 100% of the three shorter classes), CPU statistics,
  whole-life deployment size (max concurrent VMs, 86.7%), whole-trace subscription count, ids, deleted.
- Split: temporal, 3 x 864 slots, gap 87,000 s; training labels 100% known at each start; without the gap 1.331 /
  1.124 / 1.386 (worse than the dummy in two windows); train pools 65.2 / 76.2 / 84.7%; deployments never straddle
  (max span 23.92 h); 99.49-99.72% of test rows from subscriptions seen in training (RC's serving case).
- Duplicates: 62.7% exact duplicate rows, all within one deployment and slot; 0.0% of test rows have a copy in train.
- Metric: fallback log_loss (Table 4 reports several metrics side by side; the 0.6 cutoff is abstention, not a cost).
- Value: random forest 0.920 vs dummy 1.231 (+25%, 3/3); smallest class per test fold 11,847.
- Agreed changes (caller and both sides): changes 1-11 of section 3.
- subscription_vms_created_24h counts pre-trace VMs on day 0: 87,870 rows (3.65%), training only, not a leak.
- The trace's deployment is a subscription-day group (boundary at trace second 80,700; 0 of 28,208 cross).
- Mediator measurements: section 2.

**7. CONSISTENCY WITH PRECEDENT**
- Consistent (precedent checker): history features as of creation (tunisian, alfa_battle, g_research); dropped outcome
  columns (mutual_funds_india, kickstarter); per-VM rows kept (hiva_agnostic, hotel_booking_demand,
  brazilian_ecommerce); warm-up rows kept (airqo, g_research); gap (maps_router_eta_1m, nyc_taxi, brazilian_ecommerce);
  fallback log_loss on an ordered target (cardiotocography, chicago_traffic_crashes); ids dropped (CLEAN-3).
- Fixed by the changes: trace_day_of_week (rossmann, CLEAN-14); MET-17 note (video_transcoding, asp_potassco);
  subscription_vms_in_slot (distribution_transformers); LEAK-9 line and note (medical_facility, frempl, ppnn,
  bank_marketing); day-0 window count (g_research).
- Departure, named: issue 1's recommendation departs from medical_facility's keep. The fact that sets it apart: here
  the traceable twin of the late part carries a gain (-0.013, 8 of 9 fits) and deployments stream across slots (78%);
  in medical_facility the late part showed none. That matches distribution_transformers.
- Open: issue 2 (horizon) follows medical_facility and the house-price family if 4 d; 3 d needs an exception to
  SPLIT-12 with its fact. No drift by one curator; no third exception of one kind (register: 34 flags, none here).

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: azure_vm_lifetime_resource_central_1m (record azure_vm_lifetime_resource_central), 2026-11-09
Scratch: the run's work files (t1_asof.py, t2_brute.py, t3_claims.py, t4_deploy.py, t5_depday.py, t6_metric.py and their .out files)

VERDICT
No validity claim refuted. The central claim (every history feature is as of the creation slot) holds under a stronger
test than the builder's: the trace censored at slot tau (what was observable at tau) gives the same features as the full
trace for every row created at tau, on the definition's own code (16,222 rows at 55 slots, 13 features, 0 mismatches),
and an independent re-implementation on 3,700 rows (incl. the two features the builder's check skipped) also agrees
(0 mismatches). Label never censored, gap, split sizes, duplicates within one request, vm_category, whole-trace counts
and the metric all hold. Refuted: four statements of fact in the notes or summary (wording, one feature's description,
one generated table, one missing source fact), none of which changes the task.

TABLE (claim | source | test | result | evidence | rule)

1 | V2 = 30-day trace, one region, 2019, 2,695,548 VMs, 6,687 subs | claims.md 1; curation_comments | count raw vmtable; read V2 page | holds | 2,695,548 rows, 6,687 subs, 33,205 deployments; V2 page: "one geographical region", 30 days | PROV-13
2 | V2 page first committed 2019-07-18 | claims 2 | GitHub commits API on AzurePublicDatasetV2.md | holds | oldest commit 2019-07-18T18:17:34Z | PROV-8
3 | Microsoft asks to cite SOSP'17 | claims 3 | repo README | holds | README l.37 "please make sure to cite our SOSP'17 paper" | PROV-10
4 | CC BY 4.0 | claims 4; license | GitHub licence API | holds | spdx CC-BY-4.0, LICENSE | EV-4
5 | files from release dataset-v2, tag re-created 2026-06-02 | claims 5; download_description | release API | holds | created 2026-06-02T16:35:44Z; vmtable asset 437,594,496 B = local file size | PROV-13
6 | BibTeX (authors, pp. 153-167, doi) | claims 6; bibtex | Crossref | holds | 6 authors match, pages 153-167 | PROV-10
7 | Azure's VM scheduler ASKS RC for a new VM's lifetime class at placement | claims 7; task_summary.use_case | read SOSP'17 Sec. 1, 3.5, 4, 4.1, 5 | REFUTED (wording), use case itself holds | Sec. 1: "RC's models and feature data are currently in production, being used manually by engineers ... The changes to the systems that will leverage RC are still being productized"; Sec. 4.1 "We envision many uses"; "the VM scheduler CAN use the lifetime predictions to co-locate VMs"; the one scheduler change built (Sec. 5) uses P95 utilisation, not lifetime. The use is real later: Barbalho et al., "Virtual Machine Allocation with Lifetime Predictions" (MLSys 2023, Microsoft incl. Cortez) deployed lifetime-aware placement in Azure | USE-1, writing
8 | classes = Table 3 | claims 8 | read Table 3 | holds | "<=15 mins, >15 & <=60 mins, >1 & <=24 hs, >24 hs" | USE-5
9 | top attribute = per-subscription bucket shares to date | claims 9 | Sec. 6.1 | holds | quoted verbatim (Sec. 6.1); probe: subscription_share_up_to_15min best single feature (0.746 macro AUC) | USE-6
10 | RC uses features existing in all subscriptions, not the id | claims 10 | Sec. 6.1 | holds | quoted verbatim; note RC still passes the subscription id as a client input to fetch feature data (Sec. 4) | USE-6
11 | trace lacks service name, OS, exact size | claims 11 | schema.csv | holds | 11 vmtable columns; sizes only as buckets | USE-8
12 | created/deleted all multiples of 300 | claims 12 | modulo on raw | holds | 100% / 100% | -
13 | lifetime = max(deleted-created, 300) as in the notebook | claims 13 | notebook cell 2 | holds | "np.maximum((vmdeleted - vmcreated),300)" | -
14 | 227,316 VMs with created == 0 dropped | claims 14 | count | holds | 227,316 | LEAK-23
15 | 58,628 created after 2,504,700 dropped; every kept VM running at the end lived > 24 h | claims 15; assert in _clean | count; kept rows with deleted == T and class < over 24 h | holds | 58,628; T - 86,700 = 2,504,700; 0 violations (true by arithmetic: created <= T-86,700) | LEAK-24
16 | dropped late VMs still running: 535 / 1,011 / 7,314 | claims 16; decision 2 | crosstab | holds | identical | LEAK-24
17 | kept 2,409,604; shares 42.3/27.3/24.7/5.6 (shipped) | claims 17 | filter + shares | holds | kept 2,409,604; full kept 42.5/27.3/24.5/5.7; shipped 42.3/27.3/24.7/5.6 | -
17b | README decision 1 table "kept 1,801,772" | generated README, Decisions 1 | arithmetic | REFUTED (generated table) | 2,695,548 - 227,316 - 58,628 = 2,409,604; the table's "kept" is len(df) after the 1M sampling, so its rows do not add up | writing
18 | a class is known at most 87,000 s after creation | claims 18; CLASS_KNOWN_WITHIN | reasoning on the 300 s grid + censored test (t1) | holds (conservative by one slot) | over 24 h needs deleted >= created+86,700, seen one slot later | SPLIT-9
19 | vm_category Unknown for 100% of the three shorter classes | claims 19; decision 4 | crosstab on raw | holds | 1,051,770 / 672,509 / 619,717 all Unknown; non-Unknown min observed life 431,100 s (5 days); within kept over-24h rows still 73.6% Unknown, so it also separates long lives | LEAK-10
20 | max/avg/p95 CPU summarise the whole life | claims 20 | schema + paper Sec. 3.2 | holds | per-VM aggregates of the 5-min readings | LEAK-10
21 | deployment size and subscription count are whole-trace aggregates; size = VM count for 50% | claims 21 | join tables | holds, sharpened | size == count 50.3%, size < count 49.7%, never above; size == the deployment's max concurrent VMs for 86.7% (the paper's "maximum deployment size", itself an RC target in Tables 1, 3, 4) | LEAK-10
22 | subscription first-VM time and count equal the vmtable's | claims 22 | join | holds | 100% / 100% | -
23 | every history feature as of the creation slot (builder: 300 rows) | claims 23; curation_comments | (a) t1: censor the trace at tau (keep created <= tau, deleted := min(deleted, tau)), rebuild with dataset.py's own _history_features, compare rows created at tau; 55 slots (40 random, 13 edges incl. 300-900 s, 86,100-87,600 s, 2,504,700, 5 biggest-request slots); (b) t2: own pandas semantics on 3,700 rows (3,000 random, 300 at 86,400-87,600 s, 300 in the first hour, 100 biggest requests) | holds | (a) 16,222 rows x 13 features, 0 mismatches; (b) 0 mismatches incl. subscription_mean_p95_max_cpu and subscription_vms_class_known, which the builder's verify_feats.py did not check (it also ran on the prototype feats.py, not dataset.py) | LEAK-10
23b | subscription_vms_created_24h = "created in the 24 h before t" | curation_comments (Features) | count first-day rows whose subscription has pre-trace VMs | REFUTED (description) | for t < 86,400 the count includes the VMs running at the trace start (created == 0, true creation unknown): 87,870 rows (3.65% of kept; all on training sides), median 207 such VMs per row. Not a leak (they exist at t) | CLEAN / writing
24 | same-slot counts: arrivals only, up to 5 min look-ahead | claims 24 | censored test includes VMs created at tau (arrivals) and nothing later; paper Sec. 4 lists "deployment size" as a client input | holds (design); within-slot order untestable | t1 0 mismatches; but see 28b: the trace's deployment is the paper's subscription-day regrouping, so deployment_vms_in_slot is the subscription's creations in the slot (99.1% of subscription-slots hold one deployment), not one Azure request | LEAK-10, USE-6
25 | every 5-min slot has a creation (8,638/8,638); 864 slots = 3 days | claims 25 | unique created > 0 | holds | 8,638 of 8,638; kept rows cover 8,349 of 8,349 slots; each test window 864 unique slots | SPLIT-12
26 | weekly dips days 1-2, 8-9, 15-16, 22-23, 29; hourly min at trace hour 3; no clock time | claims 26 | daily/hourly creation counts | holds | days 1-2 72k/65k, 8-9 72k/73k, 15-16 63k/73k, 22-23 58k/53k, 29 58k vs 80-98k; hour 3 = 87,129 (min). Note: deployments reveal a daily boundary at trace second 80,700 (28b), so trace_day_of_week is offset 1 h 35 min from the platform's day | CLEAN-25
27 | bucket edges not defined by the release | claims 27 | schema + links file + release assets | holds | definition files named in schema.csv, absent from links and release; the release's cores summary lists a bucket 12 (0.1%) absent from vmtable | -
28 | deployments span <= 23.9 h, one subscription | claims 28 | per-deployment span | holds | max 23.92 h, 1 subscription each | -
28b | (implied) deployment id is assignable at creation | unwritten; underlies deployment_* features | t5: find a fixed daily offset no deployment crosses | holds, fact missing from notes | 0 of 28,208 in-trace deployments cross a boundary at trace second 80,700 (next best offsets: 2,176 and 2,319 cross); V2 page: "we define a 'deployment' differently than Azure in our paper"; paper Sec. 3.4: "the set of VMs from each subscription that are deployed to a region during a day". The id is set by a fixed day boundary, known at creation, so no look-ahead | LEAK-10, PROV
29 | 3 windows x 864 slots, gap 289 slots, all training labels known at window start | claims 29; splits_comment | shipped splits (participant kit) + full frame | holds | gap 87,000 s in all 3; 864 unique test slots; known at start 100.00% x3 | SPLIT-9, SPLIT-10
30 | without the gap: 99.4-99.7% of <=15 min known, 0% of >24 h | claims 30; decision 3 | code review of _decisions (generated from raw) | holds | logic correct; over-24h VMs cannot be known within 87,000 s by definition | SPLIT-10
31 | full train 1,570,928/1,836,014/2,040,583 (65/76/85%); tests 241,863/234,507/281,121 | claims 31 | recompute | holds | identical | SPLIT-14
32 | 99.5-99.7% of test rows in subscriptions seen in training | claims 32 | recompute on full train sides | holds | 99.49 / 99.72 / 99.64% | SPLIT-13
33 | top subscription 14.9% overall, 11.9-13.4% per window | claims 33 | recompute | holds | 14.92%; 13.4 / 12.4 / 11.9% | -
34 | 62.7% exact duplicates, all within one request; 87.9% in multi-VM requests (595,296); one slot never straddles | claims 34 | shipped frame + full frame grouped by features vs deployment | holds | 62.74% dup rows; 595,296 (deployment, slot) groups, 87.85% of rows in multi-VM ones, max 918; only 0.009% of rows sit in feature-identical groups spanning >1 deployment; split by created, so a slot is never split. 41.7% of multi-VM requests mix classes (conflicting duplicates are real within-request variation). Requests >= 500 VMs hold 4.5% of window 1's test rows (0% in the others) | LEAK-16 to LEAK-21
35 | fallback log_loss; Table 4 gives several metrics side by side | claims 35; Metric block | read Sec. 6.1/Table 4; score dummies with data_foundry.v2.metrics.scorer | holds | Table 4: Acc, per-bucket %/P/R, P_theta/R_theta at a 0.6 no-prediction cutoff; no criterion named; 0.6 is an abstention cutoff for reporting, not a cost or treatment threshold (MET-7 n/a). Scorer per fold: train-prior dummy 1.2377 / 1.2241 / 1.2309 (array = DataFrame = sklearn), uniform 1.3863 = ln 4; every class in every test fold (smallest 11,847; builder report says 10,077, a typo-level slip). Class balance differs from the paper's (29/32/32/7% vs 42.5/27.3/24.5/5.7%), immaterial for a fallback | MET-1, MET-2, MET-5, MET-6, MET-8, MET-11

REFUTED, RANKED (all below the validity line; no Must broken)
1. Claim 7 / task_summary.use_case (P3, writing). The SOSP'17 paper presents the scheduler's use of lifetime predictions as
   envisioned ("can use", "We envision", systems "being productized"); the scheduler change it built uses P95 utilisation.
   Changes: nothing in the data; the use case is attested by MLSys 2023 (lifetime-aware VM allocation deployed in Azure).
   Mildest remedy: reword to "can ask ... (Cortez et al. 2017, Sec. 4.1), as Azure later did (Barbalho et al., MLSys 2023)",
   or soften to "asks" -> "can ask". Fit `direct` stays.
2. Feature description of subscription_vms_created_24h (P7/writing, could be P4-flavoured only if misread: it is not a leak).
   For rows created in the first 24 h it counts the pre-trace VMs (87,870 rows, 3.65%, training only; median 207).
   Mildest remedy: exclude created == 0 from the `created_events` used for this one count (e.g. a separate event frame),
   or add "(VMs running at the trace start counted as created at 0)" to the note.
3. Generated README, decision 1 table (writing). "kept 1,801,772" sits beside full-trace counts and does not add up
   (2,409,604 kept, 1,801,772 shipped after sampling). Mildest remedy: in _decisions, compute "kept" from the row filter on
   raw and add a row "shipped (train sides sampled to 1M)".
4. Missing source fact (P5 documentation; supports, not weakens, validity). The trace's deployment is the paper's
   subscription-day regrouping with a fixed daily boundary at trace second 80,700 (0 of 28,208 deployments cross it);
   the deployment table's size is the max concurrent VMs (86.7%), an RC prediction target. Mildest remedy: one sentence in
   the notes: deployment = VMs of a subscription in one day (V2 page, Sec. 3.4), assigned by a fixed day boundary, so
   the deployment counts are known at creation, and deployment_vms_in_slot is the subscription's creations in the slot
   rather than one Azure request. Optional (Weigh, P7): align trace_day_of_week / trace_hour_of_day to that boundary.

UNTESTED (and why)
- Order of creations within a 5-minute slot (claim 24's look-ahead): the trace has 300 s resolution; the builder's
  ablation (-0.024 to +0.018 log loss) bounds its weight. A platform re-creation of a VM that failed inside the same slot
  would make the count partly an outcome; it cannot be seen in the data.
- Whether core/memory buckets can change after creation (resize): the trace gives one value per VM ("maximum"
  allocations per the paper's dataset description).
- Whether Microsoft's "representative subset" sampling of VMs depends on lifetime: not documented.
- Identity of the 2026 release files with the 2019 blob files: only counts and the vmtable byte size agree.

Sources: SOSP'17 text (the paper's text); https://github.com/Azure/AzurePublicDataset (README, AzurePublicDatasetV2.md,
AzurePublicDatasetLinksV2.txt, release dataset-v2, licence API); Crossref 10.1145/3132747.3132772;
https://proceedings.mlsys.org/paper_files/paper/2023/hash/48eb2c79643df5cb7d125945238bd7d0-Abstract-mlsys2023.html and
https://www.microsoft.com/en-us/research/publication/virtual-machine-allocation-with-lifetime-predictions/ (search result
summary only, full text not read).

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR: azure_vm_lifetime_resource_central_1m (record azure_vm_lifetime_resource_central), 2026-11-09

Verdict: ship after two small changes. No leak found. Every history feature uses only what the scheduler knows at the
VM's creation slot. I checked this with my own brute-force run of dataset.py's _history_features on 300 rows (200 from
the test period, 100 from days 0-2). It reproduced every count, share and mean, including
subscription_mean_p95_max_cpu, which the builder's check did not cover. The builder's check ran on feats.py,
not on dataset.py.
Two cleaning problems (P7). (1) subscription_vms_created_24h counts the 227,316 VMs running at the trace start as
"created in the last 24 h" on every day-0 row. (2) trace_day_of_week is typed as an unordered category, but under
CLEAN-14's cycle rule a weekday is a number. One weak question (P4): the subscription-level same-slot count.

Judgment record
  Validity: LEAK-10 holds for all 18 features. The dropped columns (vm_category, max/avg/p95 CPU, the deployment
    table's size, the subscription table's count, the ids) are dropped correctly. USE-6: deployment_vms_in_slot kept
    as the request size, which the paper calls a client input. subscription_vms_in_slot is a weak LEAK-10 question
    (1.8% of rows).
  Quality: CLEAN-14 departure (trace_day_of_week); a definition error in subscription_vms_created_24h on day 0
    (CLEAN-1/CLEAN-19, 3.7% of rows, training only).
  For the curator: issue C (subscription_vms_in_slot: keep with a note, or drop).

Inputs read: dataset.py and builder_report.md, claims.md, the paper's text (Cortez et al. SOSP'17), schema.csv, the
azure2019_data_*.txt summary files. Rules: principles.md, leak_checks.md (LEAK-10, LEAK-41), use_case.md (USE-6),
cleaning_features.md (CLEAN-12 table, CLEAN-14 incl. the cycle rule, CLEAN-25). The participant-kit frame
(1,801,772 rows, 19 columns) is the shipped frame. My scripts are in a1.py to a4.py.

**COLUMN TABLE (shipped frame; t = the VM's creation slot, the prediction point)**
column | meaning | known at prediction? | dtype and cleaning | verdict | rule

created | the VM's creation time, in seconds since the trace start (the first 5-min reading; source schema "timestamp vm
  created") | yes, it is t | int64, 300..2,504,700, on a 300 s grid; the time column is also a feature (house
  convention); the builder's ablation without it: -0.014/0.000/+0.003 log loss | fine | USE-6

core_bucket | the source's class of virtual cores (2, 4, 8, 24, >24); the edge files are not in the release | yes, the
  requested VM size (the paper's "VM type and size" are client inputs, Sec. 4) | ordered category
  2<4<8<24<>24, which matches the source's order (azure2019_data_cores.txt also lists a "12" bucket at 0.1%, but
  vmtable has none: the raw values are 2/4/8/24/>24); open top level kept as its own level; 0 missing | fine
  (dtype-probe flag open_end answered) | CLEAN-14

memory_bucket | the source's memory class in GB (2, 4, 8, 32, 64, >64) | yes, VM size | ordered category
  2<4<8<32<64<>64, which matches azure2019_data_memory.txt; the raw data has only 10 core x memory pairs (fixed SKUs:
  >24 cores always with >64 GB, 10,923 VMs) | fine (open_end answered) | CLEAN-14

lifetime_class (target) | max(deleted-created, 300) s cut at 15 min / 1 h / 24 h (Table 3) | outcome | ordered
  category, shortest first, in the words of Table 3; 5.8% of kept VMs have a single reading (deleted==created, so
  300 s, up to 15 min) | fine | CLEAN-25, LEAK-24 (cut by creation time; assert holds)

deployment_vms_in_slot | VMs of this deployment with created == t, this one included | mostly: the size of the
  request (the paper, Sec. 4: "client inputs ... deployment size"); but within one 5-min slot it may include VMs of
  a later request of the same deployment (it cannot be ordered) | uint32, 1..918 | fine, with the existing note.
  No outcome mechanism seen: if failed VMs were replaced in the same slot, 2-VM groups would show one zero-life VM
  more often than chance, and they show it less (7,852 observed against ~11.4k expected under independence;
  3,835 with both zero-life, which is correlation within a request). Ablation of both same-slot columns:
  +0.015/-0.024/+0.018 | USE-6, LEAK-10 (weak at most)

deployment_vms_before | VMs of the deployment created in earlier slots (VMs running at the trace start included) |
  yes (a created event counts from created+300) | int32 | fine | LEAK-10 holds

deployment_vms_running | deployment VMs created before t with deleted >= t | yes (an ended event counts from
  deleted+300) | int32 | fine | LEAK-10 holds

subscription_vms_in_slot | VMs of the subscription with created == t | partly: it equals deployment_vms_in_slot on
  98.2% of rows (98.1% in the test period). On the other 1.8% it adds other deployments' VMs created in the same
  slot, which can be requests that come after this VM within 5 minutes | uint32 | question for the curator (issue C) |
  LEAK-10 (weak), CLEAN-5 (near-copy)

subscription_vms_running | subscription VMs created before t, deleted >= t | yes | int32 | fine | LEAK-10 holds

subscription_vms_created_24h | meant: subscription VMs created in the 24 h before t | yes in timing, but WRONG on
  day 0: the created event of a VM running at the trace start falls at 300 s and its "aged" event at 86,400 s, so
  every one of the subscription's 227,316 pre-trace VMs counts as created in the last 24 h for each row of day 0,
  whether it is still running or not. 87,870 of 89,906 day-0 rows are affected (3.7% of kept rows); the pre-trace
  VMs make up a median of 25% (mean 36%) of the value; mean value on day 0 is 1,951 against 1,597 without them. All
  affected rows are training-only (the test windows are days 20-28) | int32 | cleaning problem (issue A) | CLEAN-1,
  CLEAN-19 (definition-accuracy)

subscription_vms_class_known | count of the subscription's VMs whose lifetime class was known at t (ended by
  deleted+300 <= t, or running at t >= created + 87,000, so over 24 h; pre-trace VMs as over 24 h from 87,000 s if
  still running at 86,700) | yes; own VM excluded (its class is known at >= t+300). Matches my independent
  rule on 300/300 rows | int64 | fine | LEAK-10 holds (no aggregate includes the row's own outcome)

subscription_share_up_to_15min, _15_to_60min, _1_to_24h, _over_24h | the shares of the 4 classes among those known
  VMs (the paper's top attribute, Sec. 6.1) | yes, as above; missing when no class is known (0.56% of rows: new
  subscriptions, first day), so the missingness reflects the history, not the outcome (missing-indicator probe
  0.50) | float64 | fine | LEAK-10, CLEAN-2 (no imputation)

subscription_mean_avg_cpu | mean of the whole-life avg_cpu over the subscription's VMs with deleted+300 <= t | yes:
  an ended VM's average is final when it ends; the row's own CPU is never included | float64, missing 0.57% | fine |
  LEAK-10 holds

subscription_mean_p95_max_cpu | the same for p95_max_cpu | yes (my check covered this column too; the builder's
  check did not) | float64 | fine | LEAK-10 holds

trace_hour_of_day | (created mod 86,400) // 3600; the trace's clock offset is unknown | yes | int64 0..23, numeric,
  as the cycle rule asks | fine | CLEAN-14

trace_day_of_week | (created // 86,400) mod 7 as a string "0".."6", a weekday stand-in (creations dip on days 1-2,
  8-9, ...) | yes | unordered category of numeric codes. CLEAN-14's cycle rule (and the CLEAN-12 table row "an hour
  or weekday of a cycle -> a number") says a weekday computed as a number ships as a number; rossmann's DayOfWeek
  was moved from an unordered category to a number (Cases row, 2026-11-01). Its sibling trace_hour_of_day is a
  number | cleaning problem (issue B) | CLEAN-14

Dropped columns
vm_category | Delay-insensitive / Interactive / Unknown, inferred by FFT from at least 3 days of CPU readings (Sec. 3.6)
  | no, it is set from the VM's later life; it is Unknown for 100% of the three shorter classes | dropped, correct |
  LEAK-10 (strong)
max_cpu, avg_cpu, p95_max_cpu | statistics of the VM's whole-life CPU readings | no | dropped as row values, correct;
  they enter only as as-of means over ended VMs (max_cpu not used; a design choice) | LEAK-10
deployment table "deployment size" | my measurement: it equals the deployment's maximum number of VMs running at once
  for 86.7% of the 33,205 deployments (its total VM count for 50.3%, its first-slot count for 22.7%), so it is the
  paper's "maximum deployment size" (Sec. 3.4, Fig. 4), a whole-life maximum | no | dropped, correct. The notes'
  wording "counted over the whole trace" could say "the most VMs it ran at once" (a writing nit) | LEAK-10
subscription table (first-VM time, VM count) | whole-trace count; first-VM time is redundant (100% equal to the
  earliest created) | count no; time redundant | dropped, correct | LEAK-10, CLEAN-5
vm_id, subscription_id, deployment_id | encrypted ids | the subscription is known at prediction (the paper: "we always
  know the subscription"), but RC builds its models on features that exist in every subscription (Sec. 6.1) | dropped
  after the features are built; it follows the source. Keeping subscription_id would be a defensible alternative
  (CLEAN-3, a group id with meaning; the test rows' subscriptions were 99.5-99.7% seen in training), but this is not
  a problem | fine | CLEAN-3, USE-6
deleted | the VM's last reading | no, it gives the outcome | dropped, correct | LEAK-10

**PROBLEMS, ranked (principles.md: P4 before P7; Must before Should)**

C. (P4, LEAK-10 weak / USE-6; question for the curator) subscription_vms_in_slot and the builder's issue 1.
   Evidence: deployment_vms_in_slot is the request's size, which the paper names as a client input (Sec. 4), so it
   stays (USE-6). The trace cannot order VMs within one slot, but I found no outcome mechanism (no same-slot
   replacement of failed VMs; see the table). subscription_vms_in_slot is identical to it on 98.2% of rows. On the
   other 1.8% it adds VMs of other deployments created in the same 5 minutes, possibly after this VM: not known to
   the scheduler, though they are arrivals, not outcomes. The builder's ablation removed both columns together:
   +0.015/-0.024/+0.018 log loss.
   Mildest remedy: (a) drop subscription_vms_in_slot (a near-copy whose only extra part is the part that may come
   later) and keep deployment_vms_in_slot with the current note. Or (b) keep both, with the note naming the 1.8%.
   My lean is (a). Both are cheap; the effect is small either way.

A. (P7, CLEAN-1 / CLEAN-19, Should; cheap and safe) subscription_vms_created_24h is wrong on day 0.
   Evidence: in _history_features, created_events puts each pre-trace VM (created == 0) at t=300 and aged_events at
   t=86,400. So for 300 <= t < 86,400 every pre-trace VM of the subscription counts as "created in the 24 h before
   t", including those already ended. This affects 87,870 rows (3.7% of the kept 2,409,604). It inflates the value
   by a median 25%, and the series drops when day 1 starts. Training rows only (the test windows are days 20-28),
   and it does not leak the outcome. The notes ("created in the 24 h before t") and the docstring ("VMs running when
   the trace starts count as running") do not describe this. The builder's verify_feats.py uses the same
   definition, so it could not catch it. Mildest remedy: build the 24-h count from in-trace creations only (filter
   created > 0 in the events of that count) and make it missing for t < 86,400 in subscriptions with pre-trace
   VMs, whose true creation times are unknown. The simpler version, in-trace creations only plus one sentence in
   the notes, is also acceptable. One line in _history_features.

B. (P7, CLEAN-14 cycle rule, Should; cheap and safe) trace_day_of_week is typed categorical.
   Evidence: the dtype probe flags numeric_levels. The builder answered "a weekday stand-in and so a category". But
   CLEAN-14 says a cycle of time computed or shipped as a number stays a number ("there is weekday 1.5 which is
   between monday and tuesday", Lennart, 2026-11-01). Rossmann's DayOfWeek was changed from an unordered category to
   a number under that rule, and this dataset's own trace_hour_of_day is a number. Day 0 is the trace's first day,
   not Monday, but that only shifts where the week starts, which the rule allows ("whatever its unit").
   Remedy: drop .astype(str) and take the column out of FeatureTypes.categorical (int64 0..6). Update the notes'
   bullet.

Not problems (checked and passed)
- Label timing in the shares: a class counts as known from min(deleted+300, created+87,000). That is exact for the
  >24 h class (the reading at created+86,700 is known one slot later). The trace end's truncated lifetimes become
  known only at T+300 or after every kept row's t. The own VM is never in its own history.
- Missingness: shares and means are missing when there is no history (0.56% and 0.57%). That comes from the age of
  the subscription, not from the outcome.
- Impossible and proxy values: deleted < created never happens; no proxy codes. The core "12" bucket of the summary
  file does not occur in vmtable.
- Ordinal orders: core, memory and the target are all ascending, as the source gives them.
- No column encodes the label through an id (the ids are dropped; the only quasi-identifying columns are history
  counts, a known-entity signal the use case expects, SPLIT-13).

</details>

<details><summary>Split audit</summary>

SPLIT AUDIT: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09
Role: split-auditor. Read-only; scratch and scripts in the run's work files (stats.txt, warm.txt, alt.txt,
fresh.txt, noise.txt; full.parquet = the definition's own _history_features on all 2,409,604 rows, with ids).

VERDICT: RIGHT WITH NOTES. The regime (temporal, known subscriptions), the windows and the 24 h 10 min gap mirror
Resource Central's use. The gap is necessary, not just cautious: without it the model scores worse than the dummy.
Nothing needs to change in the split. Four notes for the README / REVIEW.md, ranked below.

**1. WHAT WAS CHECKED (all numbers measured here)**
Shipped split (container rebuilt from dataset.py, 1,801,772 rows):
  window  test days (trace)   test rows  train pool (share)   train used  last train slot -> first test slot
  0       25.993-28.993       281,121    2,040,583 (84.7%)    1,000,000   2,158,800 -> 2,245,800 s (87,000 s)
  1       22.993-25.993       234,507    1,836,014 (76.2%)    1,000,000   1,899,600 -> 1,986,600 s (87,000 s)
  2       19.993-22.993       241,863    1,570,928 (65.2%)    1,000,000   1,640,400 -> 1,727,400 s (87,000 s)
  - Every 5-minute slot has a creation (8,349 of 8,349), so unit="unique" with 864 slots is exactly 3 days.
  - Train and test never overlap; test windows are not cut (largest 281k < 500k); train is a uniform 1M of the
    pool (train class mix 0.429-0.434 / 0.268-0.273 / 0.236-0.243 / 0.057-0.058 in each window).
  - SPLIT-14: 3 windows, each with its own train side, the smallest at 65.2% (floor 50%). Pass.
  - SPLIT-11: expanding train side from the trace start. Pass.

Regime (USE-10, SPLIT-13). The paper (Sec. 4, "Cache management") returns no prediction for a recently created
subscription and predicts from "feature data from the input VMs' subscription" (Sec. 6.1): the actor predicts for
known subscriptions, so temporal is right and grouped-by-subscription would test a cold start RC does not serve.
  - Test rows from subscriptions seen in train: 99.64% / 99.72% / 99.49%.
  - Test rows whose subscription had no known class at creation: 0.11% / 0.10% / 0.06%.
  No grouped fit run: the use case rules it out, and the unseen-subscription rows are 0.3-0.5%.

Label delay and training labels (SPLIT-9, SPLIT-10). A class is known at min(deleted + 300, created + 87,000).
  - Training labels known at the window start, on the full pools (not only the 1M samples): 100.0% in all 3 windows.
  - In the 24 h 10 min before each start (57,962 to 87,900 VMs), the share known at the start, by class:
    up to 15 min 99.4-99.7%, 15-60 min 96.5-98.2%, 1-24 h 66.9-73.7%, over 24 h 0.0%. A "known at start" filter
    without a gap would add rows that are 47-52% up-to-15-min and 0% over-24-h (base rate 42% and 5.6%).
  - Deployments never span more than 23.92 h (27,560 deployments, max span 23.92 h), so with the 24 h 10 min gap no
    test row's deployment has a training row (0.0% in all windows). Rows of one request (deployment, 5-min slot)
    are on one side by construction. The gap also removes the same-deployment shortcut (SPLIT-9: a label of the test
    row's own entity set after its prediction point) that a no-gap split would allow.

Alternatives fitted (untuned LightGBM, 300 trees, lr 0.05, 63 leaves, 1M train per window, same random order;
log loss per window 0 / 1 / 2; dummy 1.238 / 1.224 / 1.231):
  shipped (gap 24 h 10 min)                         0.966 / 0.890 / 0.882
  noise floor, shipped, 3 other samples and seeds   0.952-0.966 / 0.855-0.899 / 0.843-0.856
  no gap, rows whose label is known at the start    1.331 / 1.124 / 1.386   (worse than dummy in windows 0 and 2)
    same, window 0, without the `created` feature   0.938
  no gap, final labels (an oracle, not valid)       0.904 / 0.866 / 0.828   (the delay's honest cost: 0.06/0.02/0.05)
  shipped, no training rows from day 0              0.973 / 0.892 / 0.868
  shipped, no training rows from days 0-2           0.946 / 0.840 / 0.866
  shipped, last 14 days of training only            0.956 / 0.853 / 0.873
How to read these. The no-gap failure is SPLIT-10's case exactly: the newest training rows are the short-lived
ones, and a model that sees the time (`created`) as a number learns "recent means short". With `created` dropped,
the no-gap fit is 0.938, so the gap is what keeps `created` harmless. The shipped gap equals the longest delay
(24 h 10 min); nothing shorter covers the over-24-h class.

Horizon and refit (SPLIT-12). The paper says RC "periodically produces new models and feature data" (Sec. 4) and
evaluates on 2 months of training data and a 1-month test (Sec. 6.1); it gives no refit cadence. Within each
3-day window, log loss by day since the window start shows no decay:
  window 0: 1.043 / 0.941 / 0.908;  window 1: 0.777 / 0.978 / 0.864;  window 2: 0.868 / 0.922 / 0.842.
Day-to-day swings (up to 0.2) come from the days (for example day 24 and day 26 have 35-38% of 15-60 min VMs
against a usual 23-30%), not from the distance to the refit. A daily refit would not change the picture; 3-day
windows are the longest the 30-day trace allows under SPLIT-14. Pass, as the builder's issue 4 says.

Feature freshness (asked: refit daily?). The features are as of the creation slot, while RC pushes feature data
periodically. I recomputed the subscription's class shares, known count and CPU means as of a daily push (window
start plus whole days, for train and test) and as of the window start for test. Log loss:
  fresh (shipped) 0.966 / 0.890 / 0.882; daily push 0.945 / 0.929 / 0.861; test frozen at start 0.945 / 0.929 / 0.855.
There is no consistent direction, and the differences are within the noise floor. The real-time history does not
inflate the score. This is not a split problem; it is noted for the column and leak auditors.

**2. FINDINGS, RANKED (all P4; none blocks)**
N1. History warm-up in the first days (P4, SPLIT-20; builder's issue 3). Rule: Should, weighed.
  Evidence: day-0 rows (89,906 VMs; 4.4% / 4.9% / 5.7% of the three train pools) have subscription_share_over_24h
  = 0 for every row (mean 0.000), because no over-24-h class is known before 24 h 10 min. Their
  subscription_share_up_to_15min averages 0.557 against an actual 0.453 that day. From day 1 on, the shares track
  the class rates (day 1: 0.477 vs 0.493; day 3: 0.439 vs 0.435). The median known count grows from 286 (day 0) to
  about 15-20k (days 20-28). So day-0 features mean something else than later features.
  Measured cost of keeping the rows: dropping day 0 changes nothing (+0.008 / +0.002 / -0.013). Dropping days 0-2
  is better in all three windows (-0.019 / -0.050 / -0.016), but within the seed spread for window 1 (0.044).
  SPLIT-21 forbids picking the history from such a comparison.
  Remedy: none required. Keep option (a), and put the numbers above in the README (the comment already says early
  rows know less). If the curator wants a filter, the mildest is "day 0 only as history": drop training rows
  created before 87,000 s, whose over-24-h share is 0 by construction, not by the data. Measured gain: none.

N2. Weekly cycle in the test windows (P4, SPLIT-20, season-shaped window). Rule: Should; note only.
  Evidence: the trace's low-volume days (day mod 7 = 1, 2: days 1-2, 8-9, 15-16, 22-23, 29) hold 22.0% of all rows.
  The test windows hold 0.0% / 22.8% / 23.7% of their rows on such days (14.6% across the three). Window 0, the
  newest and the one with the most training data, has only weekdays (trace days 26-28). A 3-day window cannot hold
  a week, and 7-day windows would put the oldest train side near 25%, below SPLIT-14's floor.
  Remedy: keep the windows. Add one sentence to splits_comment: the newest window holds no low-volume day, and the
  three together hold one of each kind of low day.

N3. One subscription weighs on every window (P4/P6, SPLIT-13, TP; builder's issue 2). Note only.
  Evidence: the top subscription (the same one in train, 15.5-15.9% of each pool) holds 11.9% / 12.4% / 13.4% of
  the test windows (top 5: 22.7 / 28.2 / 25.0%; top 10: 30.7 / 37.6 / 34.4%, across 1,323-1,503 subscriptions).
  Its rows score 1.068 / 1.109 / 1.151, close to the dummy (1.22-1.24). Without it, the window score improves by
  0.014 / 0.031 / 0.041. Large requests weigh too: request-weighted log loss (each deployment-slot weighted
  1/size) is 0.927 / 0.800 / 0.882 against 0.966 / 0.890 / 0.882 per VM. This is the workload's real
  concentration, and the paper scores per VM. It should not be split away (SPLIT-1, USE-10).
  Remedy: none. Correct the builder's "12-13%" to "12-13% (11.9% in the newest window)" and keep the note under
  the duplicates decision.

N4. `created` is a bare trend counter whose test values lie beyond every training value (P4, SPLIT-10; for the
  column auditor). Evidence: under the shipped gap it is harmless (builder's ablation without `created`: 0.996 /
  0.895 / 0.857 against 1.010 / 0.895 / 0.854). It is the mechanism of the no-gap failure (1.331 with it, 0.938
  without it, window 0). It is an input only because the gap holds.
  Remedy: none for the split. The column auditor may weigh whether a trace offset with no calendar meaning is worth
  a feature. If it stays, the README should say that the gap is what keeps it safe.

Confirmed, no finding:
  - SPLIT-9 / SPLIT-10 gap: right, and needed (above). Training labels 100% known at each start.
  - SPLIT-14 floor, SPLIT-11 expanding train, SPLIT-15 windows rolled back from the newest: pass.
  - SPLIT-12 horizon: 3 days, no decay measured; the paper's month is out of reach of a 30-day trace.
  - Duplicates within a request: on one side by construction. Deployments never straddle the split (0.0%).
  - Right-censoring at the end: rows cut by creation time at 24 h 5 min before the end; the newest window's labels
    are final (the builder's assert; 87,000 s after the last test slot is past the trace end only by the grid
    step, and a VM still running there is over 24 h).
  - Hidden groups / near copies: the probe's near-copy clusters put 2.0-2.6% of test rows next to a train cluster.
    That is consistent with known subscriptions, which are part of the task (SPLIT-13).

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m)
Date: 2026-11-09. I play the actor: Azure's VM allocator (the per-cluster scheduler) and the operator who owns its
lifetime-aware placement rules. When a request for N VMs arrives, I call the lifetime predictor, then place the VMs:
co-locate VMs that should end together, keep long-lived VMs off hosts due for maintenance, and pack.

VERDICT
- Fit: DIRECT (agree with the builder). The moment (VM creation), the decision (placement), the classes (RC Table 3)
  and the main inputs (the subscription's class shares to date, the request size, the size class, the time) are the
  ones Resource Central (SOSP'17) and Azure's production lifetime predictor (Barbalho et al., MLSys 2023) use; the gaps
  are missing inputs and a short history, which make the task harder, not different (USE-8).
- Metric (log_loss, fallback): PARTLY. It is the right declaration under the rules (MET-5: RC Table 4 reports
  accuracy, per-class P/R and P/R at a 0.6 abstention cutoff side by side; MET-6/MET-7: no cost or decision threshold
  is fixed; MET-8: the client consumes a probability). As a score of my packing decision it has two blind spots, ranked
  below as gaps 2 and 3; neither can be fixed by the rules without inventing costs (MET-7). Keep log_loss.
- No blocking issue. Two notes to add (MET-17 numbers for the unit; the resource-weight caveat).

HOW THE DECISION IS MADE TODAY (sources)
- RC (Cortez et al. 2017, Sec. 4.1-4.2, 6.1): the scheduler calls the client DLL with "client inputs" ("subscription
  id, VM type and size, and deployment size") plus feature data fetched from a store ("percentage of short-lived and
  long-lived VMs to date" for the subscription). Feature data are pushed periodically, and a recently created
  subscription gets a no-prediction. The result is a bucket plus a confidence score; "the client may choose to
  ignore a prediction when the confidence score is too low" (the 0.6 cutoff of Table 4). Uses of the lifetime: schedule
  maintenance, co-locate VMs that end at about the same time (Sec. 3.5, 4.1). Sec. 5 actually wires only the P95-CPU
  prediction into the scheduler; lifetime use is described, not evaluated end to end.
- Azure production (Barbalho et al., MLSys 2023, "Virtual Machine Allocation with Lifetime Predictions"): LightGBM in
  the allocator's hot path (<30 ms); deployed V1 is a binary short/long cut at 2 h; multi-class (<10 min, 10 min-2 h,
  2 h-1 d, >1 d) examined in App. B.3, with the remark that finer classes among VMs up to 15 min do not change packing
  density "because those VMs would exit the system very soon". Small feature set: allocation hour and day, the
  customer's counts of all and of long-lived VMs in the past two months, requested size, location; large set adds
  customer lifetime percentiles, cores, memory, OS disk type, extensions, resource group, scale-set setting. Customer
  features are "updated daily via MapReduce"; models retrained weekly. Metrics: AP, F-1, AUC (binary).
- Google LAVA (arXiv 2412.09840, 2024): predicts lifetime distributions and re-predicts as VMs age; argues one-shot
  creation-time predictions are not enough. The dataset is the one-shot creation-time task, which is what RC and
  Barbalho et al. deploy.

Q1. INPUTS AT THE MOMENT OF THE PREDICTION
Have, and in the data:
- Request size: deployment_vms_in_slot / subscription_vms_in_slot stand in for the request's VM count, which RC lists as
  a client input. Builder's issue 1 (a later scale-out of the same deployment within the 5-minute slot gets folded in):
  from my chair this is a fair proxy; the scheduler knows the request it is placing, and the measured effect is
  +0.015 / -0.024 / +0.018 log loss. Keep option (a) (USE-6).
- Subscription history to date (class shares, known count, CPU means of ended VMs, running counts): exactly RC's top
  attribute. All computed as of the creation slot (brute-force verified by the builder).
- Hour and day (trace-relative): both production systems use allocation hour/day. The offset from the unknown clock
  start is harmless for a model that learns the cycle.
- Core and memory class: I have the exact SKU; the buckets are a coarsening (gap below).
Have, but fresher than I would: the history is as of the 5-minute slot; RC pushes feature data periodically and Azure
  production updates customer features daily. I measured it (practitioner_exp.py, untuned
  LightGBM 300 trees, 1M train per window as the builder's ablation): with the subscription's shares, known count and
  CPU means lagged to 1 h / 24 h before creation (request and running counts left current, which the allocator does
  know live), log loss per window (w0/w1/w2):
    fresh  1.0104 / 0.8945 / 0.8535
    1 h    1.0154 / 0.8656 / 0.8703
    24 h   1.0036 / 0.9746 / 0.8545
    dummy  1.2378 / 1.2241 / 1.2310
  The 24 h lag costs +0.025 on average (-0.007 / +0.080 / +0.001), within the run-to-run swing of this untuned model
  in two of three windows. Freshness gives no material edge: not a gap that changes the task, and no change asked
  (USE-6: every value is known at t; it is only more current than Azure's pipeline).
Would always have, missing here (gap 1): exact VM size/SKU, OS (image, disk type), service name for first-party
  subscriptions, the production/non-production annotation (RC Sec. 5's Algorithm 1 input), resource group, scale-set
  setting, VM priority, extensions, cluster/location; and history over 2-3 months instead of at most 29 days. Already
  named in fit_reason; correctly not reconstructable from the release.
Correctly withheld: vm_category (3-day FFT of the VM's own CPU), the VM's own CPU statistics, whole-trace deployment
  size and subscription VM count (LEAK-10, USE-3). I would not have any of them at placement.

Q2. IS THE TARGET WHAT I ACT ON?
- Yes. I act on a lifetime class and its confidence. RC's four classes are the source's convention (USE-5); Azure's
  later production chose other edges (2 h binary; 10 min / 2 h / 1 d), so the edges are a convention, not the only
  real one. No change: the definition follows the paper it cites.
- I want a probability vector, not a hard class: the RC client abstains below a 0.6 top score, and a robust
  lifetime-aware packer (Barbalho's LA) uses the predicted class and tolerates errors. The target is ordered
  (declared ordinal), and an error from "over 24 h" to "up to 15 min" costs me far more than to "1 to 24 h".
- Labels are final: the late-creation cut by creation time and the 24 h 10 min gap mean every training label was
  knowable at the window start (builder decision 3). This is how I would retrain.

Q3. ONE ROW = ONE DECISION? TEST DATA = WHAT I FACE?
- The scheduler places each VM, and RC Table 4 counts per VM, so per-VM rows are right (MET-17: "the score stays per
  row when each row is a decision of its own (... a job a scheduler places)"). But I query once per request, and all
  VMs of a request get the same features and so the same prediction. MET-17 then asks the notes to say how unequal
  the units are and how far one vote per unit moves the ranking. Measured on the test windows (request = deployment x
  creation slot):
    test VMs 281,121 / 234,507 / 241,863 in 64,568 / 57,640 / 58,788 requests (about 4 VMs per request);
    rows in requests of over 100 VMs: 4.8% / 12.3% / 5.1%;
    class mix per VM vs per request: over 24 h 5.5 / 5.1 / 5.9% of VMs but 8.9 / 8.2 / 8.4% of requests.
  One vote per request (weight 1/request size) reorders the four feature-set variants above: Kendall tau 0.00 / 0.33 /
  1.00 per window against per-VM log loss (w0: the variant best per VM, history-only with no request or running
  counts, 0.989, is the worst per request, 0.963). Indicative only (four variants of one learner), but it shows the
  unit matters. Finding F1 (MET-17, Should): keep per VM (builder's option 2a) and add these numbers to the notes,
  which today say only that the rows of one request share features.
- Test data: the next 3 days, from known subscriptions (99.5-99.7% of test rows); RC itself returns no prediction for a
  new subscription. That is what I face (USE-10, SPLIT-13). 3-day windows after a refit match a weekly retraining
  cadence better than the paper's one month.

Q4. WOULD I USE THIS MODEL?
- What a model reaches here (untuned LightGBM, all features): accuracy 0.57 / 0.61 / 0.63 against RC's 0.79; at the
  0.6 cutoff 47-55% of VMs get a prediction and 0.65-0.78 of those are right (RC: P_theta 0.85, R_theta 0.80). Recall of
  "over 24 h" 0.42-0.48. The gap to RC is the missing inputs, the 29-day history and a shorter-lived class mix (42% up
  to 15 min here vs 29% in RC). For a benchmark that ranks methods this is fine: there is room (dummy 1.23 vs 0.85-1.01).
- I would trust it for packing with a robust algorithm, not alone for maintenance. What I would check before trusting:
  calibration of the top probability (it decides abstention), recall of the long class per subscription, stability
  across days, and behaviour on huge requests (a single wrong call on a 918-VM request mis-places 918 VMs; production
  adds a safeguard that falls back to "short" when too many requests are called long).

Q5. DOES LOG LOSS SCORE MY DECISION?  PARTLY.
- For: the declaration follows MET-5 (several metrics side by side, no stated criterion), MET-6 (accuracy without a
  fixed cost; the 0.6 is an abstention level, not a cost or treatment threshold), MET-7 (no cost matrix, none to
  invent), MET-8 (the client consumes probabilities and their calibration decides abstention; log loss is strictly
  proper). Per VM is RC's unit (MET-1, MET-17).
- Blind spot A, resource weight (gap 2): over 24 h is 5.7% of the kept VMs but 79.9% of their core-time (core bucket x
  lifetime, lifetime cut at the trace end, so understated); up to 15 min is 42.5% of VMs and 0.7% of core-time. RC says
  the long-running VMs "account for >95% of the total core hours", and Barbalho et al. say finer short classes do not
  change packing. A per-VM score is dominated by the short classes whose placement I barely care about. No source fixes
  a weight, so MET-7 forbids inventing one; I would add one sentence to the notes and not change the metric.
- Blind spot B, order (gap 3): log loss ignores that the classes are ordered. The metric I would choose if the library
  had it is the ranked probability score (strictly proper and distance-aware on an ordered target). It is not in
  data_foundry.v2.metrics, no source uses it, and MET-8 names log_loss for multiclass; so keep log_loss.
- My choice: log_loss, per VM, unweighted, as declared. Not a hard-label metric: none of the reported hard metrics
  fixes my cost.

GAPS BETWEEN THE DATASET AND THE REAL DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Missing inputs and short history (exact size, OS, service name, production flag, resource group, scale set,
   priority; 29 days vs 2-3 months). Lowers attainable accuracy (0.57-0.63 vs 0.79); same task. Named in fit_reason.
2. Per-VM count weighting vs where the cost lies (80% of core-time in the 5.7% long class). Changes which model I would
   prefer; not fixable without invented costs (MET-7). Note only.
3. Ordered classes scored by an order-blind rule. Small; note only.
4. Unit: per VM with requests of up to 918 VMs; one vote per request reorders variants (tau 0 / 0.33 / 1). Keep per VM,
   add the MET-17 numbers (F1).
5. History fresher than production (5 min vs daily): measured +0.025 mean log loss for a 24 h lag, mostly one window;
   immaterial.
6. Same-slot request counts may fold in a second request of the same deployment: +-0.02; immaterial (builder issue 1a).
7. Class edges are RC's 2017 convention; Azure production later moved to a 2 h cut. Source's convention; no change.
8. One-shot prediction vs re-prediction (LAVA). The task is the creation-time call, as deployed by RC and Barbalho.

WHAT AN EXPERT WOULD CHANGE
- Nothing in the rows, target or split. On the builder's draft issues: 1 (a) keep the same-slot counts; 2 (a) keep per
  VM, with the MET-17 numbers above added to the notes; 3 (a) keep the warm-up rows; 4 information only.
- Add to the notes: (i) one vote per request moves the ranking (numbers above, MET-17); (ii) per-VM scoring weighs the
  short classes that matter least for packing (core-time shares above), and no source fixes a resource weight.
- Not proposed: a core-time-weighted metric or a cost matrix (MET-7), RPS (not in the library; MET-8), a binary 2 h
  sibling (RC's classes are the cited source's task; a 2 h binary sibling from Barbalho et al. would be a different
  source's convention and adds little).

SOURCES
- RC paper text: the paper's text (Sec. 3.5, 4.1, 4.2, 5, 6.1, Tables 1-4).
- Barbalho et al., MLSys 2023: https://www.microsoft.com/en-us/research/uploads/prod/2023/05/MLSYS_Lifetime_final.pdf
  (Sec. 2.4, 3.2, 4.1.1, 5.1, App. B.1, B.3); abstract
  https://proceedings.mlsys.org/paper_files/paper/2023/hash/48eb2c79643df5cb7d125945238bd7d0-Abstract-mlsys2023.html
- LAVA (Google, 2024): https://arxiv.org/abs/2412.09840 (abstract).
- Azure Public Dataset V2 page: https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md
  (first-party subset, one region, 30 days; no task or metric).
- Builder report, ablation (ablation_lightgbm.txt), cached frames feats.parquet, vmtable.parquet.
- My script and outputs: practitioner_exp.py, practitioner_exp.json, practitioner_exp.log
 .
Rules cited: USE-1, USE-3, USE-5, USE-6, USE-8, USE-10; MET-1, MET-5, MET-6, MET-7, MET-8, MET-17; LEAK-10; SPLIT-13.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: azure_vm_lifetime_resource_central
Inputs: data.parquet (200,000-row sample of 1,801,772), task.md, and public sources (AzurePublicDataset README, the V2 trace page, and search results about the Resource Central SOSP'17 paper). I did not open any other local file.
Scratch script: model.py

VERDICT: Include with changes. It is a real, leak-free task with point-in-time history features, done the Resource Central way. Before scoring, drop the raw `created` timestamp from the features and handle the heavy within-batch duplication.

WHAT THE TASK IS
Azure's VM scheduler predicts a new VM's lifetime class at the moment the VM is created. The four classes are <=15 min, 15-60 min, 1-24 h and >24 h, the same buckets Resource Central uses. The scheduler uses the prediction for placement, oversubscription and defragmentation decisions. This is a real production use: see Resource Central (SOSP'17) and the later Azure paper "VM Allocation with Lifetime Predictions". The rows come from the public Azure V2 trace (2019, one region, 2.7M VMs, 30 days). The features are:
- VM size buckets.
- Deployment and subscription activity at creation time (VMs in the same 5-minute slot, VMs created earlier, VMs running).
- The subscription's past class shares and mean CPU, computed only from VMs whose class was already known at creation time.
- Hour and day index within the trace.
Class mix in the sample: 42.3% <=15 min, 27.2% 15-60 min, 24.7% 1-24 h, 5.7% >24 h.

CHECKS THAT PASSED (evidence)
- History features are point-in-time. In the first 24 trace hours, subscription_share_over_24h is exactly 0.000 in every hour. It becomes non-zero from hour 24 on, which is when a >24 h class can first be known. subscription_share_1_to_24h is about 0 in hour 1. The shares are NaN exactly when subscription_vms_class_known == 0, with 0 exceptions either way. So the shares do not use future outcomes.
- Right-censoring is handled. The latest `created` is 2,504,700 s (28.99 days) in a 30-day trace, so every kept VM had at least 24 h in which to show the >24 h class. The >24 h rate on the last day is 5.8%, close to 5-9% on earlier days, so there is no collapse. VMs that existed at trace start (created = 0) are gone; the minimum `created` is 300.
- The VM category field from the trace is not used. That is correct, because the trace derives it from the VM's own CPU time series, which would leak.
- Values are plausible:
  - Timestamps are all on the 5-minute grid.
  - trace_hour_of_day and trace_day_of_week match `created` exactly.
  - deployment_vms_running <= deployment_vms_before in all rows.
  - The class shares sum to 1.
- There is real signal. I trained LightGBM on the earlier rows and scored three later windows (the last 30% of the sample in time, split into 10% slices). Log-loss was 0.86 / 0.97 / 0.88, against 1.23 for the class prior. Accuracy was 0.58-0.60 against 0.39-0.42 for the majority class.

CONCERNS, MOST TO LEAST SERIOUS

1. Many near-identical rows from batch creation; the effective sample size is much smaller than the row count.
   Evidence: in the 200k sample, 29.4% of rows exactly duplicate another row (features and label), and 35.3% duplicate another row's features. 49.8% of rows sit in a group of rows with identical features. The majority label covers 91.9% of rows within such groups. deployment_vms_in_slot is >=10 for 49% of rows and >=100 for 7.6%, with a maximum of 918. In the full 1.8M rows this clustering is about 9x denser.
   Effect: the temporal split keeps copies out of the test set except at window edges. However, the scores are dominated by a few large batch creations, and per-row metrics overstate how much evidence there is. With subsampling or random CV the copies would leak.
   Change: keep the temporal split, never use random CV. Consider grouping by (created, deployment) or capping/deduplicating within a slot. If you keep the rows as they are, at least document the clustering.

2. The raw absolute timestamp `created` is in the feature set.
   Evidence: with the temporal split, test values of `created` are always larger than any training value, so a tree model can only extrapolate them. Removing the column improves LightGBM log-loss in all three windows: 0.900 -> 0.857, 0.988 -> 0.972, 0.897 -> 0.876. It is the 8th most important feature by gain (3.6%).
   Change: use `created` only as the split/time index and drop it from the model inputs. trace_hour_of_day and trace_day_of_week already carry the cyclic information.

3. Headroom over a one-line rule is small; the benchmark mainly tests calibration.
   Evidence: predicting the argmax of the subscription's past class shares gives accuracy 0.602 / 0.561 / 0.577. LightGBM gives 0.596 / 0.579 / 0.604 (without `created`). Most of the model's gain is in log-loss, not accuracy. Resource Central reports about 79-90% accuracy across its metrics, but it uses subscription identity and the full Azure data. I could not compare per-metric numbers.
   Change: score with log-loss (or another proper scoring rule), not accuracy. Optionally add the subscription's previous-VM class or recency-weighted shares, which the paper's approach suggests.

4. Classes shift over time (non-stationarity).
   Evidence: the daily 15-60 min share jumps to 0.381 on day 24 and 0.349 on day 26, against about 0.23-0.29 on the days around them. The <=15 min share is 0.562 on day 16. The three test windows fall in the bursty last days.
   This matches real use and is acceptable, but expect high variance between windows. Report results per window.

5. Slight look-ahead in the "in slot" counts, and two near-duplicate columns.
   Evidence: deployment_vms_in_slot counts all of the deployment's VMs created in the same 5-minute slot, including ones created after this VM, so it reaches up to 5 minutes into the future. A batch request size would usually be known, so the risk is small. deployment_vms_in_slot equals subscription_vms_in_slot in 98.1% of rows.
   Change: say this in the documentation; optionally drop one of the two columns.

6. Small preparation issues.
   - trace_day_of_week is a string category '0'..'6'. It is the trace-relative day index, not a real weekday, because the trace hides the calendar. Likewise, trace_hour_of_day is relative to trace start (unknown time zone/offset). The names are honest, but the documentation should say so.
   - core_bucket ('2','4','8','24','>24') and memory_bucket ('2','4','8','32','64','>64') are ordered quantities stored as unordered categories. Ordinal or numeric encoding would be more natural.
   - About 0.6% of rows have NaN history features (cold-start subscriptions), and the first trace day is mostly cold start: 65% NaN in hour 0. That is fine, but it is worth noting.

WHAT I COULD NOT CHECK
- The raw trace: I did not download the 235 GB V2 trace, so I could not independently recompute the labels or features. In particular I could not check:
  - the exact class boundaries (for example, whether 15 min falls in the <=15 min class), given the 5-minute timestamp granularity;
  - how VMs still running at trace end are assigned a deleted time.
- The rows removed from the 2.70M trace. About 0.9M are not in the 1,801,772; I assume they are the VMs present at trace start and those created in the last day, but I could not confirm it.
- Copies across train and test in the full data: no subscription or deployment IDs are kept, so I could only check this for the 200k sample. Per-window evaluation there showed no problems.
- The exact test-window boundaries used by the benchmark: task.md only says "3 test windows". I used the 70/80/90% quantiles of `created`.
- The full Resource Central PDF: I did not read it, so I could not do a like-for-like accuracy comparison.

Sources: https://github.com/Azure/AzurePublicDataset ; https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md ; https://doi.org/10.1145/3132747.3132772 ; https://www.microsoft.com/en-us/research/publication/resource-central-understanding-predicting-workloads-improved-resource-management-large-cloud-platforms/ ; https://www.microsoft.com/en-us/research/publication/virtual-machine-allocation-with-lifetime-predictions/

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: azure_vm_lifetime_resource_central (lifetime_class, 4 classes, log_loss, 3 temporal windows)

Verdict: the task can be gamed heavily. Later test rows of the same deployment carry its exact cumulative
counts, so each deployment's chain of slots can be rebuilt and read forward. That cuts log loss by 0.12 to 0.20
per split, far more than any honest change I tried.

Scores are log_loss (lower is better), per split r0f0 / r1f0 / r2f0, then the mean.
  Untuned honest baseline (LightGBM, lr 0.1, 63 leaves, 200 rounds, all features):  0.9477 / 0.8919 / 0.9216  mean 0.9204
  Better honest model (regularised LightGBM, lr 0.05, 31 leaves, min_data_in_leaf 2000,
     bagging, L2 10, 300 rounds, created dropped):                               0.9418 / 0.8219 / 0.8345  mean 0.8661
  Noise around the untuned baseline: refits with a random column (2 seeds) or a different
  bagging seed (2 seeds) give means from 0.902 to 0.958, and single splits move by up to
  0.13 (r1f0: 0.883 to 1.019). The untuned model is unstable under this temporal drift, so
  the regularised model is the honest reference.

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Rebuild each deployment's chain of slots from future rows (next slot has deployment_vms_before = before + in_slot), then read later deaths (before - running) and the subscription's per-class count increments (share x class_known) 15 min, 60 min and 24 h ahead | future_chain2.py (features), honest_reg.py chain | 0.8661 (reg) / 0.9204 (untuned) | 0.7297 (reg) / 0.7409 (untuned) | reg: 0.169 / 0.125 / 0.115; untuned: 0.155 / 0.203 / 0.180 | No. It reads rows created up to 3 days after the prediction point | Round deployment_vms_before, deployment_vms_running and subscription_vms_class_known to 2 significant digits and the shares to 2 decimals (tested), or give each test window's rows only through a slot-by-slot feed |
| 1a | The same chain with a naive link (first later slot with a matching before, no consistency checks) | future_chain.py | 0.9204 (untuned) | 0.8244 | 0.072 / 0.114 / 0.102 | No | as above |

Finding 1, the mechanism. deployment_vms_before is a cumulative count. A deployment's next slot therefore has
before' = before + in_slot exactly, and it can be found with a forward as-of join on (before + in_slot,
core_bucket, memory_bucket). I keep a link only if deaths never go negative, running' <= running + in_slot,
and the subscription's class_known and per-class counts never fall. The per-class counts are exact:
share x class_known is an integer in 100% of rows. With these checks, 90% of rows link (99% without them).
Along the chain, (before - running) at a later slot minus (before - running) now counts the deployment's VMs
that died in between. The rise in the subscription's per-class counts counts VMs whose class became known.
Both are the outcome of the current cohort, seen up to 24 h later. Example: rows whose deployment loses at
least as many VMs within 15 min as the cohort has are "up to 15 min" in 57% of cases; with no deaths it is 28%.
Fix tested in fix_test_reg.py: round the three cumulative counts to 2 significant digits and the four
shares to 2 decimals. The share of rows that link falls from 90% to 29%. The regularised honest model barely
moves (0.8661 -> 0.8686, +0.003). The exploit's gain shrinks from 0.136 to 0.015 (0.9436 / 0.8195 / 0.8429 ->
0.9299 / 0.8073 / 0.8246). A small remainder survives, so coarser bins (1 significant digit or log2 bins) or a
slot-by-slot evaluation would close it fully. With the untuned model under the fix, the chain features hurt
(0.890 -> 0.946).

What is NOT an exploit (checked):
- The subscription class shares and the CPU means are point-in-time. The first non-zero values come at
  created = 600 s (up to 15 min), 1800 s (15-60 min), 4800 s (1-24 h) and 87000 s (over 24 h). That is one
  slot after the earliest moment each class can be known, so the current slot's VMs are not counted. The CPU
  mean appears only where the deployment or subscription has ended VMs.
- deployment_vms_in_slot / subscription_vms_in_slot count VMs created later in the same 5-min slot. task.md
  declares the slot known at the prediction point, so this is signal.
- NaN shares (no history) strongly indicate "over 24 h" (64% vs 5.5% base). This is signal: a new
  subscription has no history.
- The 24.2 h gap between train end and test start (87000 s) means every training label, "over 24 h"
  included, is known at test start. The test windows end 87300 s before the end of the trace, so no
  right-censored labels.

FLAWS THAT HURT AN HONEST MODEL
None that I could measure. The fold-0 and fold-1 training sets are 1,000,000-row subsamples (70% and 81% of
eligible rows). The sampling is label-independent (kept rate 0.693 to 0.701 across classes) but uneven in time:
the recent high-volume days 20-24 keep about 49% of rows, older days about 77%. Training only on the last 7 or
14 days did not help: untuned 0.932 and 0.919 vs 0.920, both inside the noise. The untuned model's instability
is a property of the model, not a flaw of the task. Regularising it gains 0.054 honestly.

ATTACKS THAT FOUND NOTHING
- Row order. The position of a row within its identical-feature group and within its slot: Spearman of
  position vs centred label = -0.033. As features (order_noise_honest.py order): 0.9387 vs 0.9204,
  worse and inside the noise. Next-row label agreement across group boundaries is 0.310, against 0.318 by
  chance.
- Copies across the split. Identical rows share a slot and so always fall on the same side. The 24 h gap
  keeps the same deployment's slots out of the test window. Linking backwards to training labels of the same
  deployment would be honest history: task.md says the deployment's history is known.
- Formats. Shares are exact fractions of class_known (100% integer counts). This is a format artefact, but it
  only matters as part of exploit 1. created is always a multiple of 300. trace_hour_of_day and
  trace_day_of_week match created exactly (100%). No sentinel values. running <= before,
  sub_running >= dep_running and sub_slot >= dep_slot hold everywhere.
- Training rows. The label rate of kept vs dropped training rows is equal across classes. No training rows
  are dated at or after the test window.
- Dropping created (honest choice): untuned 0.9047, regularised 0.8661 vs 0.8710. Small, honest.
- Web. There is no competition, forum or "magic feature" for this trace. The sources are the Azure Public
  Dataset V2 docs and the Resource Central SOSP'17 paper. Looking rows up in the published vmtable.csv
  (vmcreated, vmdeleted) would give the labels. That is the usual lookup any public dataset allows; I did
  not try it and do not rank it. The kit dropped vmid, subscription id, deployment id and vmdeleted. The
  chain exploit recovers deployment identity from the cumulative counts that remain.

COULD NOT CHECK
- Without ids I could not measure how accurate the chain link is. The negative deaths in the naive link show
  some mislinks; the checks remove the inconsistent ones, not all of them.
- The exploit was not pushed further (per-VM lifetime decoding, subscription-level chains built from
  class_known). The 0.73 shown is a lower bound on what is reachable.
- Whether the fold-0/1 subsample was meant to be uneven in time.

Scripts and logs: common.py, baseline.py, future_chain.py, future_chain2.py, honest_reg.py,
order_noise_honest.py, fix_test.py, fix_test_reg.py, fix_test_helpers.py, explore1-3.py, chain_crosstab.py;
logs *.log.
Sources: https://github.com/Azure/AzurePublicDataset/blob/master/AzurePublicDatasetV2.md ,
https://www.microsoft.com/en-us/research/publication/resource-central-understanding-predicting-workloads-improved-resource-management-large-cloud-platforms/

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09

Verdict: most calls follow precedent. Four depart from a rule or its closest precedent without a fact that holds:
(1) trace_day_of_week typed categorical, against the cycle rule;
(2) per-VM scoring without the MET-17 note and measurement;
(3) the horizon reason ("nothing longer fits") is false: 4 to 4.5-day windows keep the 50% floor;
(4) keeping subscription_vms_in_slot. Its late part may carry a gain, it was not measured, and the
    medical_facility precedent that would allow keeping it rests on a measurement.
No drift by one curator. No third exception of one kind. Nothing breaks a higher-ranked Must.

Inputs: dataset.py and the record, builder_report.md, column_auditor and blind_reviewer reports,
register.json (34 flags, none on this dataset's calls), the knowledge files of the worktree (principles, leak_checks,
splits, metrics, use_case, cleaning_features), the sibling definitions of the working copy. Scratch:
windows.py (train fractions for longer windows, on the builder's feats.parquet).

**PER DECISION**

A. History features built as of creation from the same log (17 features, incl. the subscription's class shares)
   CONSISTENT.
   - The previous outcome of a known entity is a feature: USE-10/LEAK-34 (Musts, P3/P4).
     Precedents:
     - tunisian_fraud_detection_challenge: the taxpayer's previous adjustment, built from the dropped id over strictly
       earlier years (Lennart, 2026-11-05; use_case.md Cases).
     - corporate_credit_rating: the previous rating (USE-10 Cases).
     - ieee_fraud_detection: `uid` (LEAK-34 Cases).
     - ghanas_indigenous_intel: reporter history (EV-6 Cases).
   - Building a per-row history from a log: CLEAN-19 bullet 3. Precedents:
     - alfa_battle_2_0_task_2 (Lennart, 2026-10-13, reason 2026-10-21).
     - g_research_crypto_forecasting_1m (Lennart, 2026-10-22). It computes the history on the full grid before
       dropping rows, and dropped rows still enter the history, as azure's pre-trace and late VMs do.
   - The features are the paper's own top attribute (Sec. 6.1: "percentage of VMs classified into each bucket to date
     in the subscription"), so CLEAN-19's "take the source's / top solution's features" holds.
   - Label timing is dated (`class_known_at`) and brute-force verified twice (builder; column auditor on dataset.py).
     That is stricter than tunisian, whose audit dates are absent.
   - Same batch, AI draft, not a precedent: data_fusion_2026_guardian_1m declines label-history features because
     the label's arrival is undated (LEAK-12). Azure dates it, so the two are told apart by a stated fact.
   - Note for the mediator (no prompt):
     - CLEAN-6 (Must, P7) bars "label-based counts". In practice USE-10/LEAK-34 (higher-ranked Musts) override it
       for a known entity's history.
     - No Tensions row or CLEAN-6 narrowing says so yet.
     - Azure goes one step beyond tunisian: shares over many sibling entities (VMs) of a group (the subscription),
       not the row entity's own previous label.
     - principles.md asks that a new tension become a row. Propose one at the curator's decision. Tension:
       known-entity history (USE-10, LEAK-34) against label-based counts (CLEAN-6). Winner: the history, as of the
       time each label is known. Cases: tunisian_fraud_detection_challenge (2026-11-05) and this dataset.
   - Event-log siblings named in the brief:
     - delivery_eta_1m and maps_router_eta_1m ship the host's features.
     - nyc_taxi, pkdd_15 and chicago_taxi have no entity key.
     - chicago_traffic_crashes builds no history.
     - sepsis_prediction_1m predicts from the current hour only, by design: a grouped split for new patients, so
       USE-10 sends it to the cold start.
     None of these is a like case decided the other way.

B. Same-slot request counts (deployment_vms_in_slot, subscription_vms_in_slot): builder issue 1, recommends keeping both
   PARTLY CONSISTENT. deployment_vms_in_slot: keep, consistent. subscription_vms_in_slot: keep departs without a
   reason.
   - deployment_vms_in_slot:
     - The paper names "deployment size" among the client inputs the scheduler passes in. the paper's text:
       "Examples of client inputs are subscription id, VM type and size, and deployment size".
     - So it is an input known at the prediction point (USE-6, LEAK-37; brazilian_ecommerce, the input-not-leak
       case).
     - Its possibly-late part (later requests of the same deployment inside one 5-minute slot) cannot be located
       row by row. The closest precedent is medical_facility_operational_data (Lennart, 2026-11-05; LEAK-10/LEAK-6
       Mechanisms row): schedule counts that include later bookings were kept with a note. The reason there: "the
       whole-field worth is an upper bound on the late part, and it sits within about two seed SDs".
     - Azure measured the worth of both columns together, one seed: +0.015 / -0.024 / +0.018 log loss. No seed SD.
     - Keeping deployment_vms_in_slot with the note follows medical_facility in kind; the measurement that made it a
       keep there is missing here.
   - subscription_vms_in_slot:
     - It equals deployment_vms_in_slot on 98.2% of rows (column auditor).
     - Its only extra content is other deployments' VMs in the same slot. These are not a client input, may come
       after this VM, and cannot be located.
     - LEAK-10 clause 2 says such values "go when they may carry a gain"
       (distribution_transformers_at_cauca_department, Lennart, 2026-10-21). They stay with a note only when the
       traced part shows none (onlinenewspopularity, medical_facility).
     - No measurement isolates it. Keeping it departs from distribution_transformers without a fact that sets it
       apart.
     - Dropping it (the column auditor's (a)) is the consistent call and the mildest remedy: the earlier-slot counts
       stay.
   -> Prompt 4 below.

C. One row per VM, 62.7% exact duplicates within one request (builder issue 2)
   KEEP ROWS: CONSISTENT. PER-ROW SCORE: CONSISTENT IN KIND, BUT THE MET-17 NOTE AND MEASUREMENT ARE MISSING (departs
   without a reason).
   - Keeping the copies follows the precedents where distinct units share inputs the features cannot tell apart:
     - LEAK-19 Cases: hiva_agnostic and qsar_tid_11 (Lennart, 2026-10-21).
     - LEAK-18: ai4d_lab_tanzania (Lennart, 2026-11-05).
     - hotel_booking_demand, accepted warning: "several rooms of one group".
     - brazilian_ecommerce: "orders that share every feature ... we keep them as distinct orders".
     The conflicting copies are genuine label ambiguity within a request, the LEAK-20 carve-out (not jm1's drop).
     No copy straddles a split (probe 5: 0.0%).
   - Is a request a unit under MET-17 (Lennart, 2026-11-08)?
     - The rule keeps the per-row score "when each row is a decision of its own (... a job a scheduler places)". The
       scheduler places each VM on a server, so per VM matches:
       - video_transcoding_time_prediction: per job, a scheduler's decision.
       - asp_potassco_classification: per instance.
       Both are metrics.md Cases of 2026-11-08.
     - The same clause requires "the notes then say how unequal the units are and how far one vote per unit moves
       the ranking". Both precedents give it: tau 0.90, and tau 0.86 with the best model changing on 13 of 30.
     - Azure's notes say only "they are distinct VMs and stay". The builder report has the inequality (87.9% of rows
       in multi-VM requests, up to 918 per slot; the top subscription holds 12-13% of each window), but there is no
       ranking measurement and no figure in the notes.
     - A weight per request (options b/c) would follow dementia_prediction, superconductivity and
       pancreatic_cancer_mouse_detection. There the actor decides once per unit, which is not the case here.
   -> Prompt 2 below.

D. History warm-up rows kept (builder issue 3; SPLIT-20, Should)
   CONSISTENT.
   - SPLIT-20 asks that what the train side holds be decided from the use case, with the reason stated. The notes
     state it.
   - Closest precedents:
     - airqo_low_cost_air_quality_monitor_calibration_challenge (Lennart, 2026-11-05): "Nakawa enters October with 63
       hours of history, noted under USE-10". The short-history rows stayed, with a note.
     - g_research (2026-10-22): rows whose trailing window reaches before the series start are kept, with the
       feature missing.
   - chicago_traffic_crashes cut its early history for a break in collection; azure has no break (one 30-day
     trace).
   - g_research backed its SPLIT-20 call with a measurement (all history vs a recent cut). A keep-vs-drop-days-0-2
     ablation would put azure on the same footing. It is optional; no prompt.
   - Related consistency point, not a separate decision: subscription_vms_created_24h on day 0 (column auditor
     issue A).
     - The day-0 count includes pre-trace VMs whose creation time is unknown.
     - The g_research precedent makes a window that reaches before the start missing. So the auditor's first remedy
       is the consistent one: missing for t < 86,400 in subscriptions with pre-trace VMs.
     - "In-trace creations only" would undercount silently.

E. No calendar date: the time axis as 5-minute steps; hour and day mod 7 as features
   AXIS: CONSISTENT. DTYPE OF trace_day_of_week: DEPARTS WITHOUT A REASON.
   - Using the order of a release without dates as the time axis is consistent with:
     - alfa_battle_2_0_task_2 (issue month rebuilt from the transactions);
     - alfa_bank_credit_history_default_1m (application order);
     - medical_facility_operational_data (arrival rank as the time column, day key built in _clean).
     Not inventing a calendar date matches CLEAN-14's "reconstruct ... as far as the information allows".
   - `created` stays a feature: as nyc_taxi `pickup_datetime` and the other temporal tasks. The blind reviewer's
     drop suggestion has no rule behind it (the builder's ablation without it: -0.014 / 0.000 / +0.003).
   - trace_day_of_week:
     - It is built as a number 0..6, then cast to a string category.
     - The CLEAN-14 cycle rule (Lennart, 2026-11-01) says a weekday shipped as a number "stays a number, whatever its
       unit". rossmann_store_sales' DayOfWeek was moved from an unordered category to a number under it. The CLEAN-14
       Cases row lists 5g_energy_consumption, miami_housing, mobile_churn and others typed the same way.
     - The dataset's own trace_hour_of_day is a number.
     - The builder's reason ("a weekday stand-in and so a category") is the reading the rule rejects. The unknown
       start day only moves where the week wraps, as for any 0-6 coding.
   -> Prompt 1 below.
   - core_bucket and memory_bucket as ordered categories with an open top level: consistent with CLEAN-14 (binned
     ranges are ordinal, categorical by default) and the PR #37 typing.

F. Gap of 24 h 10 min (289 slots; SPLIT-10)
   CONSISTENT.
   - The gap equals the longest label delay (a class is known by creation + 87,000 s), and 100% of the training labels
     are known at each window start (measured). Without it: 99.4-99.7% of short VMs known against 0% of long ones, a
     selection by the outcome. That is exactly what the 2026-11-04/05 amendment of SPLIT-10 says calls for a gap.
   - Precedents (SPLIT-9/10 Cases): maps_router_eta_1m, nyc_taxi, pkdd_15 and cooking_time, one-day gaps where a
     trip ends after the window start (Lennart, 2026-10-21); brazilian_ecommerce (2026-10-15); sf_permit_time.
   - The gap costs no floor: train sides are 65 / 76 / 85% (reproduced: 0.652 / 0.762 / 0.847), so this is no
     SPLIT-14 exception and adds nothing to the SPLIT-10 amendment-due flag in the register.
   - Horizon (builder issue 4; SPLIT-12): the paper's month cannot fit, so a departure from the source horizon is
     unavoidable. But the stated reason is false. "The 30-day trace allows nothing longer under SPLIT-14" is
     contradicted by my run on the shipped rows:

       window   oldest train side
       3.5 d    59.9%
       4.0 d    55.2%
       4.5 d    50.8%

     All keep SPLIT-14's floor. SPLIT-12 (Should) asks for the source's horizon. The precedents follow theirs:
     - medical_facility_operational_data moved to the source's 14 days (2026-11-05);
     - the house-price family "each keeps the horizon of its own source" (2026-10-21).
     -> Prompt 3 below (a reason that does not hold).

G. Fallback log loss for a 4-class ordered target (MET-5, MET-6, MET-8)
   CONSISTENT.
   - The paper reports accuracy and per-class precision and recall, with and without a 0.6 confidence cutoff, side by
     side (Table 4). That is the multi-metric case MET-5 sends to the fallback, as gallstone_disease and
     early_stage_diabetes (Tensions row, Lennart, 2026-10-21).
   - The 0.6 cutoff is an abstain threshold reported next to the no-cutoff numbers, not a single treatment threshold
     with costs. So MET-7 does not apply (taiwanese_bankruptcy: no single matrix).
   - Ordered multiclass targets on the fallback log_loss in the working copy: cardiotocography (normal < suspect <
     pathologic), hepatitis_c_prediction, chicago_traffic_crashes (five injury levels), ny_wcb_assembled_claims_1m.
     CLEAN-25 (PR #37, Lennart, 2026-11-01/05): the order is type information only. No precedent declares an ordinal
     metric (no QWK or RPS anywhere in the working copy's metrics).

H. Dropped vm_category and the whole-trace counts (LEAK-10)
   CONSISTENT.
   - vm_category is inferred from at least 3 days of the VM's own CPU series and is Unknown for 100% of the three
     shorter classes. That is "a feature computed from the window that defines the target" and "another encoding of
     the target". Precedents (Mechanisms rows): mutual_funds_india `rating`; heart_failure `time`.
   - The CPU statistics describe the VM's life after creation (kickstarter `staff_pick`, hotel `AssignedRoomType`:
     recorded after the prediction point).
   - The deployment table's size is the most VMs the deployment ran at once over its life (column auditor: 86.7% of
     deployments). The subscription table's VM count is counted over the whole trace.
   - Replacing them with counts to date is the smallest fix of LEAK-7. Precedents:
     - zillow_prize and melbourne_housing_market: late values blanked;
     - garments `incentive`: lagged;
     - github_pull_request_acceptance_1m, same batch, AI: the source's merge rates rebuilt as of the opening.
   - LEAK-10's window-sum clause, keep when the data shows no movement with the outcome (account_debt_south_africa),
     was not claimed and does not fit a count that grows with the deployment's life.
   - The cohort cuts follow LEAK-24 (sf_permit_time: cut where follow-up is complete, by creation time, not by
     outcome): pre-trace VMs dropped, VMs of the last 24 h 5 min dropped.

I. Ids dropped after the features are built (CLEAN-3)
   CONSISTENT, with a stated reason.
   - CLEAN-3 keeps a meaningful id "and process[es] it into that meaning". The subscription id is processed into its
     history features, and the source's models do not use the id (Sec. 6.1).
   - ieee_fraud_detection kept `uid` as a feature (LEAK-34 Cases) because the top solutions did. Different source
     practice; no prompt.

**REFLECTION PROMPTS (issue shape, one per departure)**

1. Consistency check: Ship trace_day_of_week as a number, like trace_hour_of_day and every weekday of the working copy?
   - **Problem:**
     - The day of the trace modulo 7 is built as a number 0..6 and then cast to an unordered category.
     - Since 1 November a weekday or month shipped as a number stays a number[c14], and rossmann's DayOfWeek was changed from a category to a number for that reason[ross].
     - The stated reason (a weekday stand-in, so a category) does not set this case apart: the unknown start day only moves where the week wraps.
   - **Consistency:** this dataset's own trace_hour_of_day is a number; the column auditor raises the same point (issue B).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the category, as an exception | Records that the day index has no known weekday, so its order is arbitrary | The model cannot read a false distance between, say, day 6 and day 0 | The same holds for every 0-6 weekday; a third such exception would call for an amendment |
     | b | Ship it as a number | Drops `.astype(str)` and the categorical entry | Same as the cycle rule and the sibling hour column; no new exception | A tree must learn the wrap itself, as for every numeric weekday |
     | c | Change the cycle rule | Weekdays without a known start become categories | Settles all such cases at once | Reopens rossmann and the rest of the CLEAN-14 cases |
     | d | (implemented) as (a), without a recorded exception | The current definition | None | A departure with no stated fact |

   - **Recommendation:** (b), as the column auditor proposes.
   - **Decision:** number or category?

   [c14]: CLEAN-14 (Should), cycle rule, Lennart 2026-11-01: "Shipped as numbers it stays a number, whatever its unit (a weekday 0-6 or 1-7 ...)".
   [ross]: cleaning_features.md Cases, CLEAN-14 row: rossmann_store_sales `DayOfWeek`, "an unordered category before".

2. Consistency check: Add the request sizes and the ranking under one vote per request to the notes, as for the other scheduler task?
   - **Problem:**
     - VMs are scored one per row, which fits a scheduler that places each VM[m17]; the per-row rule also asks the notes to say how unequal the units are and how far one vote per unit moves the ranking.
     - The two precedents give both (video_transcoding_time_prediction tau 0.90; asp_potassco_classification tau 0.86, the best model changing on 13 of 30)[m17c].
     - Here the notes only say the copies are distinct VMs; 87.9% of rows sit in multi-VM requests of up to 918 VMs, and nothing measures the ranking.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Per VM, plus the note and a tau measurement | Kendall tau of a few untuned models per split, per row against one vote per (deployment, slot); the sizes and the tau in the notes | Follows video_transcoding and asp_potassco; the choice stays and is documented | One more probe run |
     | b | One vote per request as the unit weight | Weight 1 / request size for scoring only, declared as the unit weight | Large requests stop dominating a window | The scheduler places each VM, so the actor does not decide once per request (the dementia and superconductivity cases) |
     | c | (implemented) Per VM, no note | The current definition | No work | Departs from the rule's per-row clause without a reason |

   - **Recommendation:** (a).
   - **Decision:** measure and note, or weight by request?

   [m17]: MET-17 (Should; Lennart, 2026-11-08): "The score stays per row when each row is a decision of its own (... a job a scheduler places); the notes then say how unequal the units are and how far one vote per unit moves the ranking."
   [m17c]: metrics.md Cases, MET-1/MET-17 rows of 2026-11-08: asp_potassco_classification, video_transcoding_time_prediction.

3. Consistency check: Keep 3-day test windows when 4 to 4.5-day windows also keep every train side above half the rows?
   - **Problem:**
     - The paper tests on a month, which the 30-day trace cannot hold, so the horizon has to be shortened[s12].
     - The stated reason, that nothing longer than 3 days keeps the 50% floor[s14], is false on the shipped rows: the oldest window's train side is 59.9% at 3.5 days, 55.2% at 4 days and 50.8% at 4.5 days.
     - The precedents follow the source's horizon as far as they can (medical_facility moved to the source's 14 days)[s12c].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | (implemented) 3 days, with a corrected reason | A recorded fact sets it apart (AI's best guess: each window's train side stays at 65% or more, nearer the paper's two months of training per month tested) | Larger train sides; no rebuild | Shorter than the horizon the floor allows; the reason has to be rewritten |
     | b | 4 days (1,152 slots) | The longest window with a margin above the floor (55.2%) | Nearer the source's horizon, as the precedents do | Rebuild; the oldest train side is 55% |
     | c | 4.5 days (1,296 slots) | The longest window that keeps the floor (50.8%) | Nearest the source | Within a point of the floor |

   - **Recommendation:** (a) only with the corrected reason, otherwise (b); this is a weighing call.
   - **Decision:** which window length?

   [s12]: SPLIT-12 (Should): "The horizon is a human judgment from the source ... Choose the test windows to match it and write the reasoning down."
   [s14]: SPLIT-14 (Must): at least 3 windows, no train side under 50% of the data.
   [s12c]: splits.md Cases: SPLIT-12/SPLIT-19 medical_facility_operational_data (2026-11-05, Lennart); SPLIT-12 house-price family (2026-10-21, Lennart). Measurement: windows.py on feats.parquet.

4. Consistency check: Drop subscription_vms_in_slot and keep deployment_vms_in_slot with its note, as earlier counts that include later events were judged?
   - **Problem:**
     - Both columns count VMs created in the same 5-minute slot, and the trace cannot tell which came after this VM.
     - The deployment count is the request size, which the paper names as a scheduler input; the subscription count equals it on 98.2% of rows and adds only other requests of the same 5 minutes.
     - Counts with an unlocatable late part were dropped when they might carry a gain (distribution_transformers) and kept only when a measurement put their worth within seed noise (medical_facility)[l10]; here neither column was measured on its own and no seed spread is known.
   - **Experiments:** both columns together, one seed: removing them changes log loss by +0.015, -0.024 and +0.018 in the three windows.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Drop subscription_vms_in_slot; keep deployment_vms_in_slot with the note | Removes the part that is not a scheduler input | Matches distribution_transformers for the late part and the scheduler-input precedents for the request size; the column auditor's choice | Loses the 1.8% of rows where the two differ |
     | b | (implemented) Keep both with a note | The current definition | No change | Departs from distribution_transformers with no measurement; medical_facility kept only after one |
     | c | Keep both, after measuring each against seed noise | Ablate each column over 3+ seeds per window | Follows medical_facility if the worth stays within noise | More probe runs; drop anyway if it does not |

   - **Recommendation:** (a); a seed-noise measurement of deployment_vms_in_slot alone would make its note match medical_facility's.
   - **Decision:** drop the subscription count?

   [l10]: LEAK-10 (Must), second clause, and the Mechanisms rows: distribution_transformers_at_cauca_department (Lennart, 2026-10-21, dropped); medical_facility_operational_data (Lennart, 2026-11-05, kept: "the whole-field worth is an upper bound on the late part, and it sits within about two seed SDs"). USE-6/LEAK-37 for the request size as a client input (paper Sec. 4).

**REGISTER FLAGS**
- None of the 34 flags is on this dataset.
- The relevant ones:
  - SPLIT-10 amendment due (10 datasets): azure is no exception, it sets the gap.
  - SPLIT-14 exceptions: azure keeps the floor.
  - CLEAN-19 amendment due (per-entity history kept as rows): azure aggregates to one row per prediction, an
    application of bullet 3, not an exception.
  - LEAK-10 exception_to_must (loan_default_prediction_imperial_college): unrelated.
- Drift: none found for these rules.

</details>

<details><summary>Advocate</summary>

ADVOCATE, OPENING BRIEF: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09

Position: ship as defined, with changes that need no decision (a LEAK-9 protocol line, notes, two one-line cleaning
fixes). No validity Must fails; the one large finding (the task gamer's chain) is an evaluation-level leak whose
rule-given remedy keeps the data as it is.

1. A real, direct use case on first-party production data (P1-P3; SEL-1, SEL-2, SEL-16, USE-1 Must, USE-5, USE-8).
   Evidence: Resource Central (Cortez et al., SOSP'17) predicts exactly these four lifetime classes (Table 3) at VM
   creation; Azure later deployed lifetime-aware placement (Barbalho et al., MLSys 2023: LightGBM in the allocator).
   The domain practitioner rates the fit DIRECT: same moment, decision, classes and top inputs; the gaps (exact SKU,
   OS, 29 days of history) make it harder, not different (USE-8). CC BY 4.0, ids encrypted by Microsoft; counts
   match the V2 page (2,695,548 VMs, 6,687 subscriptions; PROV-13).
   Real problem conceded: the use_case text says the scheduler "asks" RC; the paper says it "can use" it (claim
   auditor, claim 7). Mildest remedy: reword to "can ask ... (Cortez et al. 2017), as Azure later did (Barbalho et
   al. 2023)". Wording, not validity: the fit stays direct.

2. Every row holds only what existed at its creation slot (P4; LEAK-10 Must holds).
   Evidence: claim auditor censored the trace at tau and rebuilt with dataset.py's own code: 16,222 rows x 13
   features at 55 slots, 0 mismatches; an independent re-implementation on 3,700 rows, 0 mismatches (incl. the two
   features the builder's check skipped); column auditor's own 300-row brute force agrees. Blind reviewer, without
   our files: subscription_share_over_24h is exactly 0 in the first 24 h. The outcome columns are dropped:
   vm_category (Unknown for 100% of the three shorter classes), whole-life CPU statistics, whole-trace deployment
   size and subscription count. The class shares are the paper's own top attribute (Sec. 6.1), a known entity's
   dated history (USE-10, LEAK-34 Musts; precedent tunisian_fraud_detection_challenge, 2026-11-05).
   Labels are never censored: rows cut by creation time 24 h 5 min before the end (LEAK-24; assert in _clean).

3. The split mirrors the application, and its gap is necessary (P4; SPLIT-9 Must, SPLIT-10, SPLIT-13, SPLIT-14 Must).
   Evidence: temporal, 3 x 3-day windows, gap 24 h 10 min = the longest label delay; 100.0% of training labels known
   at each window start. Without the gap the split auditor measures 1.331 / 1.124 / 1.386 log loss, worse than the
   dummy in two windows: the gap removes a real selection by the outcome. 99.5-99.7% of test rows come from
   subscriptions seen in training, which is RC's serving case (no prediction for new subscriptions, Sec. 4).
   Train sides 65 / 76 / 85% (floor 50%). Exact copies across the split 0.0%; deployments never straddle (max span
   23.92 h < gap). Precedents: maps_router_eta_1m, nyc_taxi, brazilian_ecommerce (one-day gaps).

4. The task gamer's chain is an evaluation-level leak, fixed by a protocol line, not in the data (P4; LEAK-9 Should,
   amended 2026-11-05 on medical_facility_operational_data).
   Evidence (conceded, it is real and large): linking a deployment's later test rows through its cumulative counts
   (before' = before + in_slot) reads deaths and class increments up to 24 h ahead: -0.12 to -0.20 log loss. But it
   works only by reading rows created up to 3 days AFTER the prediction point, inside the test block; each row on its
   own passes the censored-trace test (point 2). LEAK-9 says exactly this case, "a model can read other test rows",
   "is fixed in the scoring ... or by a protocol line the benchmark checks, not in the data"; medical_facility (queue
   fields = history at each row's arrival, a method reading the block sees the future) is the like case and got the
   protocol line. Mildest remedy: add the same protocol line and list the check in BENCHMARK_CHANGES_TODO.md.
   Why not the gamer's rounding: it alters faithful counts (P7, against LEAK-9's "not in the data"), leaves a residual
   (0.015 gain), and is unnecessary once the protocol holds. The curator may still choose it as an extra guard.

5. Worth benchmarking, scored the way the source reports (P6; TP-1 to TP-9, MET-5, MET-6, MET-8).
   Evidence: random forest 0.920 vs dummy 1.231 (+25%, wins 3/3, SE 0.014); smallest class per test fold >= 10,077
   rows; untuned LightGBM accuracy 0.57-0.63 vs RC's 0.79, so headroom remains. Table 4 reports accuracy and
   per-class P/R with and without a 0.6 abstention cutoff side by side, no criterion: the MET-5 fallback (log_loss;
   precedents gallstone_disease, and cardiotocography / chicago_traffic_crashes for ordered targets on log_loss).
   The practitioner keeps log_loss; RPS or a core-time weight would be invented (MET-7).

6. One row per VM is the right unit; duplicates are distinct VMs (P4/P6; LEAK-16 to LEAK-21, LEAK-20 carve-out,
   MET-17 Should).
   Evidence: MET-17's own example of a per-row unit is "a job a scheduler places"; the scheduler places each VM and
   RC Table 4 counts per VM. 62.7% exact duplicates all sit within one (deployment, slot); 0.0% of test rows have a
   copy in train. Precedents: hiva_agnostic, hotel_booking_demand, brazilian_ecommerce (kept);
   video_transcoding_time_prediction, asp_potassco_classification (per row, MET-17).
   Real gap conceded (precedent checker prompt 2): the MET-17 note is missing. The numbers already exist (domain
   practitioner: ~4 VMs per request, 4.8-12.3% of test rows in requests >100 VMs, one vote per request moves the
   ranking, Kendall tau 0.00 / 0.33 / 1.00 on four variants). Mildest remedy: write them into the notes, accept the
   two duplicate-row warnings with the builder's texts.

7. The rest are cheap fixes or notes, not reasons against shipping (P7 below P4; "a very real task carries cleaning
   imperfections when they are written down"; remedy ladder).
   - subscription_vms_created_24h counts pre-trace VMs on day 0 (87,870 rows, 3.7%, training only, no leak): make it
     missing for t < 86,400 in subscriptions with pre-trace VMs (g_research precedent). CLEAN-1/CLEAN-19.
   - trace_day_of_week: ship as a number 0..6 (CLEAN-14 cycle rule, rossmann; its sibling hour is numeric).
   - subscription_vms_in_slot: equals deployment_vms_in_slot on 98.2% of rows; its extra 1.8% may hold later
     arrivals. Dropping it is the mildest, consistent call (LEAK-10 clause 2, distribution_transformers), keeps the
     request size (a client input, Sec. 4; USE-6). I accept the drop.
   - Horizon (SPLIT-12 Should): conceded, "nothing longer fits" is false (4 d keeps 55.2%). 3 d stays defensible by a
     true fact: train sides >= 65%, nearer the paper's 2 months of training per month tested, and no decay within a
     window (split auditor: day-wise log loss shows none). Correct the reason; the length is the curator's weighing call.
   - `created` stays (blind reviewer would drop it): no rule asks it, ablation -0.014 / 0.000 / +0.003, and the gap
     keeps it harmless (split auditor); house convention, as nyc_taxi pickup_datetime.
   - Writing: README decision 1 "kept 1,801,772" (should be 2,409,604 kept, 1,801,772 shipped), "12-13%" -> 11.9-13.4%,
     deployment = subscription-day regrouping with a fixed boundary at trace second 80,700 (claim auditor 28b).

Judgment record
Verdict: ship after changes that need no new rule (protocol line, notes, two cleaning fixes, one column dropped).
Validity: SEL-1, SEL-2 hold; USE-1 holds (direct; wording fixed); LEAK-10 holds per row; LEAK-9 triggered, fixed by a
  protocol line; SPLIT-9/10/13/14 hold; PROV-13 holds.
Value: TP pass (+25% over dummy, 3/3 windows); MET-5 fallback log_loss; MET-17 note to add.
Quality: CLEAN-14 (day of week) and CLEAN-19 (day-0 count) fixed; SPLIT-12 reason corrected.
For the curator: window length (3 d vs 4 d), a weighing call.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE, REBUTTAL: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09

The critic and I agree on the verdict (ship after changes, no exclusion) and on six of its seven points. The one
open dispute is how much of point 1 is left to settle.

1. Same-slot counts (LEAK-10 Must, clause 2). Partly conceded.
   - Conceded: drop subscription_vms_in_slot. It is a near copy (98.2% equal), and its only extra part is other
     deployments' later arrivals (my point 7 already accepted this). Also conceded: the "one request" wording is
     wrong. The trace's deployment is the paper's subscription-day group (claim auditor 28b), so the note must say
     so.
   - Disputed: that deployment_vms_in_slot is "kept without a measurement" and is open at Must level.
     a) Its id is set by a fixed day boundary (0 of 28,208 deployments cross trace second 80,700), so the group is
        known at creation. Within the 5-minute slot, the late part is later arrivals, not outcomes. The column
        auditor tested for an outcome mechanism (failed VMs replaced in the same slot) and found none: one-zero-life
        pairs 7,852 against ~11.4k expected under independence.
     b) A measurement exists: removing both columns together, which bounds the late part from above, gives +0.015 /
        -0.024 / +0.018 log loss. The signs are mixed. The split auditor's spread over 3 samples and seeds is 0.014 /
        0.044 / 0.013 per window. So the whole-field worth sits at about one spread, which is medical_facility's
        footing ("within about two seed SDs").
   - Caveat I accept: the ablation and the noise run used different LightGBM settings, so this is indicative. A
     3-seed ablation of deployment_vms_in_slot alone is a probe run, not a decision: run it and write its number into
     the note. The rule then decides on its own (drop if the worth exceeds the spread). This is not grounds to hold
     the dataset.

2. LEAK-9 protocol line and note. Conceded. It is my point 4. We agree that the counts are not rounded and that the
   precedents (medical_facility, frempl, ppnn) carry both the line and a "Potential leak, kept on purpose (LEAK-9)"
   note with the gamer's numbers.

3. Horizon reason false (SPLIT-12). Conceded. The fix is a true reason or 4-day windows: the curator's weighing call.

4. MET-17 note. Conceded, including the core-time caveat (42.5% of VMs but 0.7% of core-time, against 5.7% and
   79.9%). No weight is invented (MET-7).

5. Refuted statements of fact (a "asks", b "one request", c "kept 1,801,772"). Conceded. These are wording fixes in
   the definition and _decisions.

6. subscription_vms_created_24h on day 0. Conceded. Make it missing for t < 86,400 where the subscription has
   pre-trace VMs (the g_research precedent).

7. trace_day_of_week. Conceded. Ship it as a number (CLEAN-14).

Net result: no remaining disagreement on rank or rule. All changes are mechanical except two:
- the window length (the curator's weighing call);
- deployment_vms_in_slot, which the 3-seed measurement settles under LEAK-10 without a further decision.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09

Position: ship only after changes. The task is real (USE-1 holds, fit direct), the history features are as of
creation (verified three times, 0 mismatches), the gap and the cohort cuts are right. I do not argue for exclusion.
No point below is a Must that cannot be fixed. But the definition ships one Must-level question open, one measured
evaluation leak without the note and protocol line that every precedent carries, and several stated reasons that
the panel refuted. Ordered: P4 Must, P4 Should, P6, then writing and P7.

1. Same-slot counts: a late part that cannot be located, kept without the measurement the precedent requires
   (P4, LEAK-10 Must, second clause).
   Problem: subscription_vms_in_slot and deployment_vms_in_slot count VMs created in the same 5-minute slot, which
   may come after this VM. The notes justify them as "one request" and the paper's client input "deployment size".
   Evidence: claim auditor 28b: the trace's deployment is not an Azure request but the paper's regrouping of a
   subscription's VMs deployed to a region in one day (V2 page: "we define a 'deployment' differently than Azure";
   Sec. 3.4), fixed day boundary at trace second 80,700, 99.1% of subscription-slots hold one deployment. So
   deployment_vms_in_slot is the subscription's creations in the slot, not the request the scheduler is placing.
   subscription_vms_in_slot equals it on 98.2% of rows; its only extra is other deployments' VMs of the same 5
   minutes (column auditor, issue C). Worth measured only for both columns together, one seed: +0.015 / -0.024 /
   +0.018 log loss. Precedents: distribution_transformers (dropped when a gain may sit on the late part);
   medical_facility (kept only on a measurement that put the whole-field worth within about two seed SDs).
   Effect: a model may read up to 5 minutes of later arrivals the scheduler does not have; the size is unmeasured.
   Remedy (mildest): drop subscription_vms_in_slot (near copy, CLEAN-5; loses 1.8% of rows' extra); measure
   deployment_vms_in_slot alone over 3+ seeds per window and keep it with a note that gives that worth and says the
   trace's deployment is a subscription-day group, not one request. Drop it too if its worth exceeds the seed spread.

2. Measured evaluation leak with no note and no protocol line (P4, LEAK-9 Should).
   Problem: deployment_vms_before is cumulative, so later test rows of the same deployment link to earlier ones
   (next slot's before = before + in_slot, matched on size buckets); along the chain, before - running and the
   subscription's per-class known counts (share x class_known, integer on 100% of rows) reveal how many of the
   current cohort died within 15 min, 1 h, 24 h.
   Evidence: task gamer, exploit 1: log loss 0.866 -> 0.730 (regularised) and 0.920 -> 0.741 (untuned), gains
   0.115-0.203 per split, 90% of rows linked; a lower bound. That is about 40% of the honest skill over the dummy
   (1.23 -> 0.87). A deployed model cannot have it (reads rows up to 3 days later).
   Rule and precedents: LEAK-9 fixes such a leak by a protocol line the benchmark checks and a "Potential leak, kept
   on purpose (LEAK-9)" note: medical_facility_operational_data, frempl_french_motor_personal_line,
   ppnn_ecmwf_t2m_postprocessing_germany_1m all carry both. This definition carries neither.
   Remedy: add the note with the gamer's numbers and the line "each test row is predicted from the training rows and
   its own features only; no feature or model step may use other test rows". Rounding the counts (gamer's fix) is not
   asked: LEAK-9 fixes evaluation leaks in the scoring, not the data.

3. The horizon's stated reason is false (P4, SPLIT-12 Should; SPLIT-14 Must cited wrongly).
   Problem: splits_comment says "the 30-day trace allows windows of 3 days"; the builder report says nothing longer
   fits SPLIT-14. The paper tests on a month (Sec. 6.1).
   Evidence: precedent checker, on the shipped rows: oldest train side 59.9% at 3.5 d, 55.2% at 4 d, 50.8% at 4.5 d,
   all above the 50% floor. Precedents follow the source's horizon as far as they can (medical_facility moved to
   14 days; house-price family).
   Remedy: either 4-day windows (1,152 slots), or keep 3 days with a true reason recorded as an exception (larger
   train sides). A weighing call for the curator; the false reason cannot stay.

4. Per-VM scoring without the MET-17 note and measurement (P6, MET-17 Should).
   Problem: 87.9% of rows sit in multi-VM groups (up to 918 VMs, one feature vector, one prediction). MET-17 keeps the
   per-row score for a scheduler but requires the notes to say how unequal the units are and how far one vote per
   unit moves the ranking. The notes say only "distinct VMs and stay".
   Evidence: domain practitioner: Kendall tau 0.00 / 0.33 / 1.00 between per-VM and one-vote-per-request rankings of
   four feature-set variants; rows in requests over 100 VMs 4.8 / 12.3 / 5.1%; over-24-h is 5.5% of VMs but 8.9% of
   requests. Precedents video_transcoding (tau 0.90) and asp_potassco (tau 0.86) give the figures.
   Remedy: keep per VM; put these numbers (or a tau over a few untuned models) in the notes. Add the practitioner's
   one-sentence caveat that per-VM log loss weighs the short classes (42.5% of VMs, 0.7% of core-time) over the long
   one (5.7% of VMs, 79.9% of core-time); no weight is invented (MET-7).

5. Statements of fact in the shipped text that the panel refuted (P3 / P5 documentation, writing.md).
   a) use_case: "Azure's VM scheduler asks Resource Central ...". SOSP'17 presents it as envisioned ("can use", "We
      envision", "being productized"; Sec. 5 wires only P95 CPU). Claim auditor 7. Remedy: "can ask ... as Azure
      later did (Barbalho et al., MLSys 2023)". Fit stays direct (USE-1).
   b) the "one request" wording of the duplicates and features notes (see point 1, claim auditor 28b).
   c) generated README decision 1: "kept 1,801,772" beside full-trace counts; true kept 2,409,604 (claim auditor 17b).
      Remedy: compute kept from the row filter, add a "shipped after sampling" row.

6. subscription_vms_created_24h is wrong on day 0 (P7, CLEAN-1 / CLEAN-19 Should).
   Evidence: the 227,316 pre-trace VMs count as "created in the last 24 h" on every day-0 row of their subscription:
   87,870 rows (3.65%), median +25% of the value, training sides only (column auditor A; claim auditor 23b). Not a
   leak. Remedy (cheap, safe): missing for t < 86,400 in subscriptions with pre-trace VMs (g_research precedent for a
   window that reaches before the series start), or in-trace creations only with a note.

7. trace_day_of_week typed as an unordered category (P7, CLEAN-14 Should, cycle rule).
   Evidence: built as 0..6 then .astype(str); CLEAN-14 (Lennart, 2026-11-01): a weekday shipped as a number stays a
   number "whatever its unit"; rossmann DayOfWeek moved for this; the sibling trace_hour_of_day is numeric. The
   unknown start day only moves the wrap. Column auditor B, precedent checker prompt 1. Remedy: drop .astype(str)
   and the categorical entry.

Dropped (no rule or evidence behind them): the blind reviewer's "drop `created`" (house convention; ablation
-0.014 / 0.000 / +0.003, within noise); deduplicating or weighting per request (the scheduler places each VM, MET-17);
the history warm-up rows (SPLIT-20; dropping day 0 changes nothing measurable).

Judgment record
Verdict: ship after changes.
Validity: USE-1 holds (wording fix); LEAK-10 open on the same-slot counts (drop one, measure the other);
  LEAK-9 triggered, note and protocol line missing; SPLIT-9/10/13/14 hold; SPLIT-12 reason false.
Value: TP holds; MET-5/8 fallback holds; MET-17 note and measurement missing.
Quality: CLEAN-1/19 (created_24h day 0), CLEAN-14 (day of week): cheap fixes.
For the curator: point 3 (window length) is a weighing call.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC, REBUTTAL: azure_vm_lifetime_resource_central (folder azure_vm_lifetime_resource_central_1m), 2026-11-09

We agree on the verdict (ship after changes, no exclusion). Point by point on the advocate's opening brief:

1. Real, direct use case (USE-1). Conceded, with the "asks" -> "can ask ... as Azure later did (MLSys 2023)" rewording
   the advocate also accepts.

2. Every row holds only what existed at creation (LEAK-10). Conceded for the 13 history features, the dropped outcome
   columns and the cohort cuts (three independent checks, 0 mismatches). Partly disputed for the same-slot counts:
   - The advocate concedes dropping subscription_vms_in_slot and the "one request" wording. Settled.
   - deployment_vms_in_slot: I concede it is not a reason to hold the dataset. The outcome-mechanism test (7,852 vs
     ~11.4k one-zero-life pairs) and the fixed day boundary (0 of 28,208 deployments cross) support a keep. But the
     existing number does not yet meet the medical_facility standard. The builder's ablation (+0.015 / -0.024 /
     +0.018) and the split auditor's spread (0.014 / 0.044 / 0.013, a range over 4 runs, not an SD) come from different
     LightGBM settings. In windows 0 and 2 the ablation is larger than that range. The advocate accepts the 3-seed
     ablation of this column alone. With that, the note and LEAK-10 decide (keep within noise, else drop). No dispute left.

3. Split mirrors the application (SPLIT-9, -10, -13, -14). Conceded: the gap is needed (no-gap 1.331 / 1.124 / 1.386),
   training labels are 100% known, and test rows come 99.5-99.7% from known subscriptions.

4. The task gamer's chain is a LEAK-9 evaluation leak: protocol line, no rounding. Conceded. It is my point 2, and we
   agree on the note with the gamer's numbers and on the precedents (medical_facility, frempl, ppnn).

5. Worth benchmarking, fallback log_loss (TP, MET-5/6/8). Conceded. Small correction: the smallest class per test fold
   is 11,847, not 10,077 (claim auditor 35). It does not matter.

6. One row per VM; duplicates kept (LEAK-16 to -21, MET-17). Conceded, with the MET-17 note the advocate also concedes.
   Disputed detail: the advocate would accept the duplicate-row warnings "with the builder's texts". Those texts say
   "one request of up to 918 VMs". That is the same refuted wording: a trace deployment is a subscription-day group
   (claim auditor 28b, V2 page). Rewrite the warning texts too (writing.md), not only the notes.

7. Cheap fixes and notes. Conceded for created_24h (missing on day 0), trace_day_of_week as a number, dropping
   subscription_vms_in_slot, keeping `created`, and the writing fixes.
   Disputed on the horizon (SPLIT-12, Should): one of the advocate's "true facts" for 3 days points the other way.
   The split auditor finds no decay within a 3-day window (day-wise log loss shows none). That means a longer window
   costs no staleness, so it supports moving toward the source's month (4 d keeps 55.2%). It does not support
   staying at 3 d. Only "train sides >= 65%" sets 3 d apart. If the curator keeps 3 d, the exception must rest on that
   fact alone, recorded as an exception to SPLIT-12. Still the curator's weighing call.

Net: no open dispute on rank or rule. Two items wait on a measurement or a decision: the 3-seed ablation of
deployment_vms_in_slot, and the window length (curator). One wording fix the advocate's brief misses: the
accepted_check_warnings texts.

</details>
