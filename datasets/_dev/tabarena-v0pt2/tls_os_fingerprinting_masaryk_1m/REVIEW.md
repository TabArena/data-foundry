# tls_os_fingerprinting_masaryk

**Outcome:** added as `tls_os_fingerprinting_masaryk_1m`. The AI recommends shipping it as defined; open are whether the
score counts each Wi-Fi session or each flow and whether the session weight may also train (issue 1), and a
confirmation that the destination address stays dropped (issue 2). Five days of real flow records from Masaryk
University's campus Wi-Fi (NOMS 2020, Zenodo, CC BY 4.0), 13.3M flows with the TCP SYN fields, of which this version
samples 2.5M; the target is the device's operating system from the DHCP host name, five classes, scored by
session-weighted log loss on three half-day windows.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-2 hold; USE-1 holds (the use case names the per-session decision; issue 1); USE-5 holds (closed set
of five, DHCP labels, named); USE-8 holds, fit approximate (the test devices are already DHCP-labelled, the unit is a
session, no OS version: now in `fit_reason`); LEAK-10 triggered, fixed (the four User-Agent OS fields dropped); LEAK-34:
recurring sessions kept (removing them changes the score by 0.001 to 0.002); SPLIT-1, SPLIT-3, SPLIT-10 (no gap),
SPLIT-14 hold; SPLIT-19 departure forced by SPLIT-14 (a Must); PROV-1, PROV-3, PROV-7 hold.
Value: TP-4 holds, not trivial (best single feature 0.282 against 0.133 for a random forest; the baseline with each
session counted once, 1.08); MET-5, MET-6, MET-11 fallback log loss holds; MET-17 weighted branch taken for a unit whose
rows are its own traffic, not protocol repeats (an amendment under A, issue 1); MET-15 holds under the implemented
option, but its premise for unit weights fails here (training with the weight moves the score by 0.008 worse to 0.12
better, by model).
Quality: CLEAN-10, CLEAN-11, CLEAN-14 triggered, fixed (`dst_port` and `tls_extension_types` categorical, `syn_size`
below 40 and the filler `tls_sni_length` to missing); CLEAN-3 departure for the destination address (issue 2);
`period` kept with a note (CLEAN-19); CLEAN-22 SSH fields kept.
Weighed: gap + (multiclass, list-valued TLS fields), source + (NOMS 2020, Zenodo; chosen over cesnet_os), size +,
risk - (DHCP labels, closed set, 2019 fingerprints).
For the curator: issue 1, a weighing call (A: per session with the weight for scoring only, B: per session with the
weight also for training, C: per flow unweighted); issue 2, a confirmation (the destination address stays dropped).

**Main points:** Issue 1: count each Wi-Fi session once with the weight for scoring only (A, implemented), also for
training (B, a rule amendment and a library change), or each flow (C); issue 2: confirm the destination address stays
dropped.

**Record judgment:** valid. A peer-reviewed release (Laštovička et al., NOMS 2020) with its data on Zenodo under CC BY
4.0; the 18,708,983 flows and 45,602 sessions match the paper; the release has five classes, without the paper's 1.5%
Linux and other. The screening's "about 12 to 13 million task rows" is 13,309,494 flows with the SYN fields.

**Issues for Lennart:**

1. **Count each Wi-Fi session once (its weight for scoring only, or also for training), or each flow?**

   * **Problem:**
     - The score can count each Wi-Fi session once, as the security team's inventory would (implemented: each flow
       weighs 1 over its session's flows in the half-day, so a session counts the same however many flows it has), or
       count each flow, as the paper does; Windows has 39.5% of the flows but 7.0% of the sessions, so the two scores
       rank close models differently.
     - Under the implemented score the weight is for scoring only: no model receives it when training (it is neither a
       feature nor a training weight), so a model learns the flows' class mix (much Windows) while the score counts
       sessions (little Windows); training with the weight instead changes the loss by between 0.008 worse and 0.12
       better, depending on the model, far more than the rules assumed when they kept such weights out of
       training[^m15].
     - Our rule counts a unit once when its extra rows are repeats a measurement protocol made (a mouse bled five
       times), and per row when each row is a decision of its own; a session's flows are neither, they are the device's
       own traffic[^m17].
   * **Background:**
     - A session is one Wi-Fi connection of a device (RADIUS), one label each; the weight's unit is the session in a
       half-day (`session_window`, an opaque id kept as metadata, never a feature), and the paper counts 45,602
       sessions of 11,962 devices, so a device can count more than once.
     - One Windows session holds 578,764 flows (4.3%), the ten largest 12.0%; in the test windows Windows is 23-38% of
       the flows but 6-8% of the weight, and Android 55-56% of the weight.
     - "Scoring only" means models train unweighted; a pipeline may still weight its validation loss or recalibrate
       with the weight (`validation_weight` returns it), which the README now says.
   * **Effect on the task:**
     - Per session, a model that learns the flows' class mix (much Windows) carries the wrong class prior for the
       score; the benchmark then partly ranks how a pipeline handles a few giant sessions rather than how well it reads
       a fingerprint.
     - Per flow, a few busy Windows sessions dominate each window's score, and the inventory use case, one reason this
       source was preferred over cesnet_os (its sessions), goes unused.
   * **Experiments:** session-weighted log loss on the 3 shipped windows unless stated.
     - The weight moves the order of close models: among 9 to 10 competitive LightGBM fits per window, 17 of 36, 19 of
       45 and 19 of 36 pairs swap order between the per-flow and the per-session score, and the best per-flow fit is
       never the best per session (3 of 3 windows).
     - One feature set without the time columns, mean of the 3 windows: untuned LightGBM 0.204 unweighted, 0.197 with
       its class probabilities rescaled to the class shares of the training sessions (Windows about 7% instead of
       40%), 0.096 trained with the weight; a regularised LightGBM (31 leaves, at least 500 rows per leaf) 0.139, 0.131
       and 0.095; per window 0.099 / 0.101 / 0.217 unweighted against 0.096 / 0.087 / 0.101 trained with the weight, so
       for this model almost all of the gain is in one window.
     - On another feature preparation (the claim auditor's), the same regularised model trained with the weight is
       worse than unweighted on 2 of 3 windows (+0.008, +0.003), and its rescaled probabilities give the best fits of
       that set (0.101, 0.096, 0.101): training with the weight changes the loss by between 0.008 worse and 0.12
       better by model and preparation, and a recalibration that keeps the weight out of training closes 0.006 to
       0.014 of it.
     - A model that always predicts the class shares of the training flows scores 1.43; one that predicts the shares
       with each session counted once scores 1.08, the baseline for this score.
     - The weight uses no future information: each training row's weight counts its own session's flows in its own
       half-day, and every cutoff is a half-day boundary.
   * **Consistency:**
     - Counting each session once with the weight for scoring only follows the five weighted unit cases
       (boreal_postfire_lichen_biomass, superconductivity, pancreatic_cancer_mouse_detection, dementia_prediction,
       bacteria_id_raman), each with `unit_weight` declared, but there the further rows were protocol repeats, and the
       measured training effect was small (dementia -0.004 log loss, pancreatic -0.015 AUC)[^m15][^m17].
     - Here the unit's rows are traffic the unit itself generated: the first such case of the weighted branch, so A
       widens the rule's wording.
     - Per flow follows asp_potassco_classification and video_transcoding_time_prediction (per row, the imbalance
       named in the notes); the weight also for training departs from every unit-weight case and from the scoring-only
       clause, a rule of the highest strength, so it is an amendment of the rule, not an exception.
   * **Panel:**
     - For A (advocate): counting each session is the use case of the paper's abstract, and the rule as written keeps
       the unit weight for scoring, as in the five cases.
     - For B or C (critic): the training effect is many times the bound the rule assumed, so either train with the
       weight or score per flow; the mediator's run found each side right for some models.
     - The domain practitioner decides per device, roughly per session; the split auditor and the claim auditor raise
       the training mismatch; the task gamer found no exploit beyond it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per session, weight for scoring only (implemented) | session-weighted log loss; `unit_weight` declared on `session_window`; models train unweighted; the README says the class balance is per session and `validation_weight` gives it; the unit rule's wording widened to rows a unit's own activity generated (an amendment, this dataset its case) | the actor's decision; follows the scoring-only rule and the five unit cases; no library change | training with the weight would score 0.008 worse to 0.12 better, by model, which recalibration closes only in part; the benchmark partly ranks how pipelines handle unweighted giant sessions |
     | B | Per session, weight also for training | every model trains with the session weight; the unit-weight declaration removed until the library allows both | removes the mismatch; no future information enters a weight | amends the scoring-only rule; needs a library change for the declaration; departs from every unit-weight case |
     | C | Per flow, unweighted | plain log loss; the session weight and its unit dropped; the notes name the imbalance and the ranking effect | the paper's unit; no mismatch; no rule or library change | a few busy Windows sessions dominate each window's score; the inventory use case, one reason this source was preferred over cesnet_os (its sessions), goes unused |

   * **Recommendation:** A: the inventory decides per session, the rule as written keeps the weight out of training as
     in the five earlier cases, and the README tells pipelines the score's class balance so they can weight their
     validation or recalibrate; take B only if a training effect this large should change the rule for every unit
     weight, with this dataset as its case. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: nothing to change in `dataset.py`. Amend MET-17's wording in metrics.md (the weighted branch also covers rows
     a unit's own activity generated, not only repeats the source's protocol made), with this dataset as its Cases row;
     a CC line in the record.
   - B: amend MET-15's unit-weight clause in metrics.md (a unit weight may also be the training weight when the
     measured training effect exceeds the bound; this dataset's 0.008 worse to 0.12 better as its fact) and lift the
     schema's refusal (schema.py `UnitWeight` docstring and the check that refuses a unit weight equal to the sample
     weight; needs a library change and a test). Then `sample_weight = "session_weight"`, drop `unit_weight` until the
     schema allows both, rewrite the metric reason, the ScoringColumn description ("for scoring and validation only,
     never a training weight") and the session anomaly note; re-run `dataset check` and the task probes (they then fit
     with the weight).
   - C: `metric = Metric.fallback(...)` without `inputs`; drop `scoring_columns`, `unit_weight`, `session_weight` and
     `session_window` in `_clean`; rewrite `use_case`, `question` and `split` per connection ("labels each connection
     with the OS of the device behind it"), the metric reason (the imbalance, the ranking effect from the claim
     auditor's 17/36, 19/45, 19/36), Decision 2's title and text; re-run `dataset check`, the task and leak probes.

   [^m15]: **MET-15** (Must): "A unit weight that gives each unit one vote (MET-17) is for scoring only also when the
     inputs differ within the unit ... it moves the best prediction only as far as a unit's number of rows tells about
     the target given the inputs (a fit with the weight: dementia -0.004 log loss, SE 0.003; pancreatic -0.015 AUC)."
     The schema: "a unit weight is for scoring and validation only, never a training weight".
   [^m17]: **MET-17** (Should): the score counts each unit once "if the actor decides once per unit and the unit's
     further rows are repeats the source's protocol made"; it "stays per row when each row is a decision of its own",
     the notes then saying how unequal the units are and how far one vote per unit moves the ranking. **USE-1**
     (Must): a use case is an actor, a moment and a decision; the use case and question now name the per-session
     decision (option A).

2. **Keep the destination address dropped?**

   * **Problem:**
     - The server's address is known at the prediction point, but the release hides it under Crypto-PAn, so it is an
       opaque id of 138,681 values, and the definition drops it.
     - The house rule drops only identifiers that carry no information, and three earlier datasets kept a shared-entity
       code, so the drop is a departure to record, with the fact that sets this case apart[^c3].
   * **Effect on the task:** dropping it costs nothing measurable on flows with a server name; on the 22.4% without one
     the effect is unknown.
   * **Experiments:**
     - Next to the server names (SNI and HTTP host) the address adds nothing consistent: as a category it moves a
       LightGBM's session-weighted log loss by -0.0023, -0.0009 and +0.0023 on the three windows (31 leaves; -0.0011,
       -0.0001, -0.0016 with 4 leaves).
     - The builder's gain (0.176 to 0.163) was measured without the names, and the names alone take that model from
       0.176 to 0.151.
     - 79,163 of the addresses are seen by one session only (the device's own peers); 22.4% of the task flows carry
       neither server name.
   * **Consistency:** lt_vehicle_loan_default_prediction, kick and amazon_employee_access kept shared-entity codes that
     carried signal; the fact here is the measured redundancy next to the server names[^prec].
   * **Unknown:** the gain on the 22.4% of flows without a server name alone was not measured; a clear gain there
     would reopen the question.
   * **Panel:** the builder, the column auditor, the advocate and the critic all recommend keeping it dropped; the
     precedent checker's open point (measured without the names) is answered by the column auditor's run.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Dropped (implemented) | no address column; the exception recorded in the notes | no measured gain next to the names; an opaque id of the device's own peers | departs from three datasets that kept shared-entity codes |
     | B | Ship it as a category | `dst_ip` kept, categorical | every input known at the prediction point ships | 138,681 levels, no consistent gain |
     | C | Ship its /16 prefix | the first two octets as a category | coarser, fewer levels | a feature of our construction; no measured gain |

   * **Recommendation:** A, recorded as an exception to the identifier rule with the measured redundancy as its fact.
     **Decision:** A, B or C?

   **Notes for the AI:**
   - A: add to the destination-address bullet of `curation_comments`: "Exception to CLEAN-3 (<date>, Lennart): the
     address is dropped although known at the prediction point: next to the server names it adds nothing consistent
     (mean -0.0003, its sign flips across windows), and 79,163 of its 138,681 values are one session's own peers."
     A CC line in the record, a Cases row under CLEAN-3.
   - B: remove `"dst_ip"` from the `drop_columns` of step 2 and add it to the categorical types; C: a `dst_prefix16`
     column built from the address's first two octets. Either way re-run `dataset check` and the leak probes.

   [^c3]: **CLEAN-3** (Should): "Drop uninformative identifiers (row ids, storage artefacts). Keep an identifier that
     carries meaning (a time index, a group id) and process it into that meaning." **USE-6** (Must): inputs known at
     the prediction point are legitimate.
   [^prec]: The precedent checker's comparison: lt_vehicle_loan_default_prediction (`branch_id`, `supplier_id`,
     `Employee_code_ID` kept, 2026-10-23 and 2026-11-05, Lennart), kick (`BYRNO`, `VNZIP1` as categories) and
     amazon_employee_access (`RESOURCE`, manager and role ids); no precedent drops an informative shared-entity id for
     being opaque. ugr16_isp_netflow_intrusion_1m dropped its addresses because the label was assigned on them, which
     does not hold here (the label comes from DHCP).

**Review panel:** ship after changes (mediator). Tier full: the claim, column and split auditors, the domain
practitioner, the blind reviewer, the task gamer and the precedent checker, then the advocate and the critic with one
rebuttal each, and the mediator, who ran the decisive experiment on training with the session weight. Claims: 41 and
the metric and 4 implied; every count, decoding and provenance claim holds; refuted and now fixed: the weight moves
"levels, not the order" (it reorders close models), "each session counts once" (only before sampling), and the use
case's per-connection decision against the metric's per-device one; untested: devices behind sessions (no MAC in the
release). Blind review: include with changes; its main concerns are the time columns and the near-empty SSH fields.
Task gamer: no exploit beats an honest model beyond noise; what costs honest models is the absolute time columns and
training without the weight. Agreed: the User-Agent fields dropped, the half-day windows, no gap, recurring sessions
kept, the unit weight declared, the cleaning fixes and the note corrections. Disputed: the decision unit and the
training weight (issue 1); the destination address is a confirmation, no side disputes the drop (issue 2).

<details><summary>Mediator</summary>

```text
MEDIATOR: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-09

Panel: full tier (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent
checker; advocate and critic with one rebuttal each). Both sides: ship after changes. One issue for the curator.
Decisive experiment run by me: compliant_route.py and regularised.py (+ .log).

========================================================================================================================
1. JUDGMENT RECORD
========================================================================================================================
Verdict: ship after changes.
Validity: SEL-1, SEL-2 hold; USE-1 holds once use_case and question name the one decision the metric scores (default:
  per device, issue 1); USE-5 holds (closed set, DHCP labels, named); USE-8 holds, fit approximate, once fit_reason
  also names the DHCP-labelled test population, session-not-device units and no OS version; LEAK-10 triggered, fixed
  (four User-Agent OS fields dropped); LEAK-34 recurring sessions kept (+0.0014); SPLIT-1, SPLIT-3, SPLIT-10 (no gap),
  SPLIT-14 hold; SPLIT-19 departure forced by SPLIT-14 (a Must); PROV-1, PROV-3, PROV-7 hold.
Value: TP-4 not met (single feature 0.270 against 0.131; honest null 1.08, not 1.42); MET-5, MET-6, MET-11 fallback
  log loss holds; MET-17 weighted branch taken for a unit whose rows are its own traffic, not protocol repeats (a first
  case); MET-15 holds under option (a), but its unit-weight clause's premise fails here: training with the weight
  moves the score by -0.008 to +0.12 depending on the model (measured below).
Quality: CLEAN-10, CLEAN-11, CLEAN-14 fixes applied; CLEAN-3 exception for the destination address (no consistent
  gain next to the server names); `period` kept with a note (CLEAN-19, CLEAN-5 spirit); CLEAN-22 SSH fields kept.
Weighed: gap + (multiclass, list-valued TLS fields), source + (NOMS 2020, Zenodo, chosen over cesnet_os), size +,
  risk - (DHCP labels, closed set, 2019 fingerprints).
For the curator: issue 1 (decision unit and training weight: a / a' / b; a' needs an amendment of MET-15 and of the
  schema); issue 2 (confirm the CLEAN-3 exception, no dispute).

========================================================================================================================
2. AGREED FACTS (no side disputes them)
========================================================================================================================
- Counts and provenance: 18,708,983 flows as in the paper; 13,309,494 task flows with SYN fields; five classes;
  45,602 sessions, one label each; md5, CC BY 4.0 (claim auditor, 41 claims, none refuted on P1-P5).
- LEAK-10: the UA OS code names the label's majority class on 96.5% of the 4.1% of flows that carry it; dropped.
  No other leak (missing indicators 0.532, no host-name patterns in SNI or HTTP host).
- Split: train shares 61.7 / 77.2 / 85.3%; paper's day-1 split 18.8%. Recurring sessions add 0.0014 (split auditor
  B-A); grouped-by-session split scores the same (0.1109 vs 0.1116); IID 0.010 optimistic.
- Task gamer: no exploit beats an honest model by more than noise (about +-0.003); oracle test prior gains 0.0003.
- Claim 38 refuted: close fits swap order in about half their pairs between per-flow and per-session scores; the best
  per-flow fit is never the best per-session (3/3). Builder issue 1's "moves levels, not the order" is false.
- Weighted test class shares: Android 55-56%, Windows 6-8% (34-38% of flows). Session-weighted prior null 1.08.
- Time columns cost a naive model 0.015 (split auditor) to 0.018 (task gamer, weighted); unweighted untuned 1.252.
- Destination address next to the server names: medium LightGBM -0.0023 / -0.0009 / +0.0023, shallow -0.0011 /
  -0.0001 / -0.0016 (column auditor); 22.4% of task flows have neither SNI nor HTTP host; 79,163 of 138,681 addresses
  seen by one session only.
- Cleaning facts: dst_port top 10 = 96.9% of rows; 328 task flows (87 shipped) with syn_size 2-34; tls_sni_length 0
  as filler on 3,829 task flows (888 shipped); tls_extension_types string while the cipher list is categorical.
- TTL anomaly: 137 of the 141 TTL-64 "Windows" sessions have the Windows SYN 52 / window 64240 pair, 103 carry UA
  code 68: they look like real Windows hosts (practitioner).
- unit_weight: with the row-budget check relaxed (now in the worktree, src/data_foundry/bundle_checks.py, with a
  test), the shipped frame passes: 43,948 (session, half-day) units, none above 1.0, none on both sides of a split.

Disputed fact settled by experiment (EV-1): can a pipeline that obeys "scoring only" recover what training with the
weight gains? Same features (task gamer's encoding, no time columns), 3 shipped windows, session-weighted log loss:

  model                          unweighted   + prior shift to train-side   + class bias fit on the   trained with
                                              session-weighted shares        newest train half-day     session_weight
  untuned LightGBM, 100 rounds   0.204        0.197                          0.200                     0.096 (gamer)
  31 leaves, min_child 500, 150  0.139        0.131                          -                         0.095
     per window                  0.099/0.101/0.217  0.098/0.091/0.205                                  0.096/0.087/0.101

And on the claim auditor's encoding (all_models.csv), the same regularised configuration trained
with the weight is worse than unweighted on 2 of 3 windows (+0.008, +0.003; -0.0003 on the third), while its prior
shift gives the best fits of that set (0.101 / 0.096 / 0.101). Reading: the effect of the weight on training is
model- and encoding-dependent, from -0.008 to +0.12; a compliant recalibration closes only 0.006-0.014 of it. MET-15's
stated bound for unit weights (dementia -0.004 log loss, pancreatic -0.015 AUC) does not hold here; the critic's fact
stands, and the advocate's "the honest route works" holds for some pipelines only.

Correction of the task gamer (flaw B): the weight is not computed over "the whole source session, test-window flows
included". `_clean` counts flows per (session, half-day) on all task rows; every cutoff is a half-day boundary, so a
training row's weight uses only its own past half-day (including flows the sample left out). No future information
would enter a training weight under (a').

========================================================================================================================
3. CHANGES TO MAKE NOW (no decision needed)
========================================================================================================================
Under the implemented default (a); items marked [a] are undone or reworded if the curator picks (a') or (b).
1. Issue 1's evidence: replace "moves levels, not the order" with claim 38's numbers and the measured training effect
   above (EV-1, EV-2, writing.md).
2. TP baseline: quote the session-weighted null 1.08 next to the flow-prior 1.42 (TP-4, EV-2).
3. fit_reason: add that the test devices are DHCP-labelled ones standing in for the unlabelled devices the model
   would serve (the release cannot contain them), that the unit is a session per half-day, not a device (45,602
   sessions for 11,962 MACs), and that the label has no OS version (USE-8, USE-5). Fit stays approximate.
4. [a] use_case and question: the team records each device's OS per Wi-Fi session from its connections; drop "fields
   that stay readable when the traffic is encrypted" (the HTTP host is plain text) (USE-1, MET-17).
5. [a] Keep an opaque (session, half-day) id as metadata, never a feature; declare UnitWeight(column="session_weight",
   unit=<that id>) (MET-17 declaration clause; boreal call 2026-11-08).
6. [a] README Metric block and metric reason: the score's class balance is per session (Windows 6-8% of the weight),
   validation_weight returns it, and how far the weight moves the ranking (claim 38), as every MET-17 case states it.
   Accept `task_metric_weight_without_sample_weight` with the measured effect as its reason, not the MET-15 premise.
7. task_summary.split and the ScoringColumn: "each session carries the same weight in a window's score (before the
   window is sampled to 500k flows)" instead of "counts once" (claim auditor I2; writing).
8. `period`: a note that it is only the split key, adds nothing beyond flow_start, costs a naive model 0.015-0.018;
   drop it when TemporalSplits gains an hours unit (CLEAN-19, CLEAN-5 spirit; library gap 1). flow_start stays.
9. Cleaning: dst_port categorical (CLEAN-14); syn_size below 40 to missing, rows kept (CLEAN-11); tls_sni_length to
   missing where no ClientHello was parsed (CLEAN-10); tls_extension_types categorical (CLEAN-14). Notes lines: TLS 1.3
   clients exported as TLSv1.2 (49% of shipped TLSv1.2 rows carry 0x002b); SNI cut at 64 bytes.
10. Destination address bullet: replace the 0.176 -> 0.163 figure (measured without the names) and the reason "the
    server's name is in the clear" with the numbers measured next to the names, the 22.4% without names and the
    79,163 single-session addresses (EV-2); the exception line follows issue 2.
11. TTL anomaly bullet: replace the guess about misleading host names with the practitioner's evidence (EV-2).
12. splits_comment: the recurring-session effect (+0.0014; +0.006 to +0.012 on their own rows); optionally the open
    flows at the cutoff (at most 0.05%) and the gap to the paper's protocol (0.136 against 0.112) (SPLIT-13, SPLIT-19).
13. Library gaps 1 and 2 named in the definition's notes and REVIEW.md, not only the run log (writing).

========================================================================================================================
4. ISSUES FOR THE CURATOR (rank order)
========================================================================================================================
Issue 1 (P3 and P6; USE-1 Must, MET-17 Should, MET-15 Must): which decision is scored, and may the session weight
also train?
- Problem: the actor can decide per device (inventory; paper abstract "asset identification", coverage per session in
  Sect. VI.A) or per flow (tagging each flow or alert; the paper's scoring unit, Sect. VI.B). The weighted score and
  the unweighted one rank close models differently (claim 38). Under the weighted score, a pipeline that obeys
  "scoring only" may lose up to 0.12 against one that trains with the weight, depending on the model.
- Why the rules do not settle it: neither branch of MET-17 fits literally. A session's flows are not "repeats the
  source's protocol made" (weighted branch) and not each "a decision of its own" of the inventory (per-row branch);
  which framing ships is a weighing (principles.md, Weigh). (a') departs from a Must, so it is an amendment, not an
  exception.
- Options:
  (a) per device, weight for scoring only, unit_weight declared, README note (implemented; advocate). Pro: follows
      MET-15 as written and the five MET-17 cases; the actor's decision. Con: a model-dependent training mismatch
      (-0.008 to +0.12) that recalibration closes only 0.006-0.014; the benchmark partly ranks how pipelines handle
      unweighted giant sessions.
  (a') per device, session_weight also the sample_weight (critic's preferred if per device). Pro: removes the
      mismatch; no future information (see correction). Con: amends MET-15's unit-weight clause (a Must), and the
      schema forbids a unit weight that is also the sample weight (schema.py: "a unit weight is for scoring and
      validation only, never a training weight"), so change 5 and the boreal-call declaration cannot ship with it
      without a library change too.
  (b) per flow, unweighted, with MET-17's note on the imbalance (one session 4.3% of flows; Windows 39.5% of flows,
      7.0% of sessions) and the ranking effect (critic's alternative; asp_potassco, video_transcoding shape). Pro: the
      paper's unit; no mismatch; no library change. Con: a few busy Windows sessions dominate each window's score; the
      inventory use case and the curator's reason for choosing this source over cesnet_os (sessions) go unused.
- Each side's best evidence: advocate, per device is the use case of the abstract and MET-15 as written keeps the
  weight for scoring; critic, the training effect (0.012-0.034, 0.09 untuned) far exceeds MET-15's stated bound.
  Mediator's run: both are right in part (effect -0.008 to +0.12, model-dependent).
- What would settle it: the curator's choice of the actor's decision (device or flow). If device, whether MET-15's
  unit-weight clause should allow the unit weight as the training weight when the measured training effect exceeds
  the dementia/pancreatic bound (an amendment, this case its fact, plus the schema check).
- Decision: a, a' or b.
- The use_case wording (change 4), the unit_weight declaration (change 5) and the README note (change 6) follow this
  call.

Issue 2 (P7; CLEAN-3 Should; confirmation, no dispute): record the destination address drop as
`Exception to CLEAN-3 (2026-11-09, <curator>)`: the fact that sets it apart from lt_vehicle, kick and
amazon_employee_access is the measured redundancy next to the server names (mean -0.0003, sign flips across windows),
plus the 79,163 single-session addresses naming the device's own peers. Advocate, critic, builder and column auditor
all recommend keeping it dropped; the precedent checker's open point (not measured with the names) is now answered.
Not measured: the gain on the 22.4% of flows without a server name alone; a clear gain there would reopen it.
Decision: confirm (a), or ship it as a category / the /16 prefix.

========================================================================================================================
5. DISPUTED POINTS AND HOW THEY WERE SETTLED
========================================================================================================================
D1. Training weight (critic C2 / advocate A4). Facts settled by experiment above. Rule: MET-15 (Must, P6) keeps the
    unit weight scoring-only; no higher-ranked Must requires a training weight (MET-2 holds: the metric matches the
    per-device decision, every fold is scorable). Not a conflict but a rule whose premise fails here: a weighing plus
    an amendment option, so it goes to the curator as issue 1. Not settled by the mediator.
D2. fit_reason gaps (critic C3 / advocate rebuttal C3). Both concede the sentence. The residual dispute ("largest
    gap") changes no decision: USE-8 (Must) asks that known gaps be named, not ranked. Settled: change 3.
D3. "No decision needed" for the use_case wording (critic A4). The critic is right: the wording follows issue 1.
    Settled: change 4 marked [a].
D4. unit_weight (critic A5 / advocate 5). Agreed: declare it (change 5). Added by the mediator: it is incompatible
    with (a') under the current schema.
D5. Practitioner's aggregated per-session score: both sides agree SPLIT-23 (Must) and MET-17's last sentence bar it
    without a cited per-device use case of the source. Not raised.

Task gamer's exploits, mapped (the definition has no `Potential leak, kept on purpose:` note; accepted warning:
task_metric_weight_without_sample_weight):
| # | Exploit | Rule | Known? | Measured gain | Issue? |
| 1 | source-port chains, causal count | LEAK-34 / SPLIT-13 (entity history) | known (splits comment: devices recur) | -0.0012, noise | no |
| 2 | pool predictions over test-window chains (later flows) | SPLIT-23, MET-17 (prediction unit) | new | 0.0000 | no |
| 3 | whole-chain count incl. later flows | LEAK-37 spirit (span set after the point) | new | +0.0004 | no |
| 4 | session_weight as a feature | MET-2 (scoring column never a feature) | known (README, ScoringColumn) | +0.001 (worse) | no |
| 5 | test-window prior EM | LEAK-30 spirit (transductive) | new | worse; oracle 0.0003 | no |
| A | time columns as raw numbers | CLEAN-19 / CLEAN-5 spirit (P7) | new; agreed note (change 8) | 0.018 weighted | note only |
| B | training without the weight | MET-15, MET-17 | known (accepted warning) | -0.008 to +0.12 | issue 1 |
| C | train side a 1M sample of the history | SPLIT-26, row budget | known (version_comment) | 0.003 mean, near noise | no |
Lookup of rows in the public source file: untested (EV-6), the same for every public release; not an issue.
Blind reviewer's points not covered above: SSH fields kept (CLEAN-22), SYN filter and per-window caps already in the
notes and version_comment (its task card did not show them), the 9,263 flows of 11 July already noted. None raised.

========================================================================================================================
6. CONSISTENCY WITH PRECEDENT
========================================================================================================================
Followed: LEAK-10 drop (2_month_survival, sdss_17, kickstarter); src address and session id dropped (ugr16,
data_fusion_2026_guardian); SPLIT-14 over SPLIT-19 (california_house_prices_2020); closed set approximate
(sarcoma, diabetes_3); no relabelling (eryhemato tension row); tls_os over cesnet_os (CC 2026-11-08); unit_weight
declared (boreal call; dementia, pancreatic, superconductivity, bacteria_id_raman) under (a).
Departures, each with its fact:
- MET-17 weighted branch for rows the unit's own activity generated, not protocol repeats. Fact: class-linked
  imbalance (Windows 39.5% of flows, 7.0% of sessions). Reflection question for the curator: should MET-17 read
  "repeats the protocol made, or rows the unit's own activity generated"? (first case; an amendment, not an exception)
- Destination address dropped against the kept shared-entity codes of lt_vehicle, kick, amazon. Fact: measured
  redundancy next to the server names (issue 2).
- (a'), if chosen, departs from every MET-17 case and from MET-15 (Must) and the schema: an amendment with this case's
  measured training effect (-0.008 to +0.12, against -0.004 / -0.015 AUC in dementia / pancreatic) as its fact.
No drift by one curator, no third exception of one kind.
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR - tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-08

Verdict: ship after a metric weighing. 41 claims plus the metric and 4 implied claims were tested on the data (the
shipped frame rebuilt through the definition with row lineage; it equals the participant kit's data and
scoring.parquet exactly), on the paper (paper/paper.txt) and on the Zenodo record (API, re-read). Every count,
share, decoding and provenance claim holds. One claim is refuted: claim 38, that the session weight moves the level
of the score but not the order of models. The premise behind claim 39 (a unit weight for scoring only moves the best
prediction little, MET-15) also fails here. Three statements are refuted on wording or are incomplete: the split
text says "each session counts once" although sampling breaks it; the use case says each connection is labelled while
the metric reason says the decision is per device; and unit_weight is not declared (MET-17). Nothing refuted on
validity (P1 to P5).


========================================================================================================================
TABLE (claim | source | test | result | evidence | rule)
========================================================================================================================
1  | Zenodo 3461771, zip 700,767,981 B, md5 ebb0..7f, CC BY 4.0 | claims 1; download_description; license | Zenodo API re-read | HOLDS | size, md5 'ebb0f2c0117193e43d9089d613748c7f', license cc-by-4.0, date 2019-09-26; page defines no metric | PROV-1, EV-4
2  | 120 hourly CSVs, 29 columns | claims 2 | listed the zip; raw frame shape | HOLDS | 120 CSVs, 2019-07-12-00 to 2019-07-16-23; raw (18,708,983 x 29) | PROV-3
3  | 18,708,983 flows = paper Sect. IV | claims 3 | counted | HOLDS | 18,708,983; paper "18 708 983 enriched flows" | PROV-3
4  | Eduroam devices, 12-16 July 2019, Crypto-PAn | claims 4 | paper Sect. IV, Zenodo page | HOLDS | both say so | PROV-1
5  | label from DHCP host name; Windows editable | claims 5; fit_reason; notes | paper V.C | HOLDS | quoted text matches lines 389-402 | USE-5
6  | year, source, bibtex | claims 6 | page | HOLDS | 2019, Zenodo DOI | PROV-10
7  | wget URL returns 200 with the zip's size | claims 7 | curl -IL today | HOLDS | HTTP 200, content-length 700767981 | -
8  | use case: inventory of OSes from encrypted fields | claims 8; task_summary.use_case | paper abstract, Sect. I | HOLDS as a source fact; see implied claim I3 for wording | abstract "Asset identification..." | USE-1
9  | fit approximate, gaps named | claims 9; fit_reason | read against data | HOLDS | gaps confirmed: 141 Windows sessions on TTL 64, no Linux class, rows are flows | USE-1, USE-8
10 | export at end or 5 min; duration 0..300 s | claims 10; notes | recomputed on task rows | HOLDS | min 0.0, max 300.0 s (0.017% at exactly 300) | LEAK-37
11 | 13,309,494 task flows (71.1%) with SYN fields | claims 11; notes | counted | HOLDS | 13,309,494 = 71.14%; paper "over 71 % ... used TCP" | USE-7
12 | all but 1,662 of 9,515,666 TLS flows in task | claims 12 | counted | HOLDS | 9,515,666 TLS, 1,662 outside | USE-7
13 | five classes, counts | claims 13 | counted | HOLDS | Windows 5,258,018; Android 4,800,530; iOS 2,243,622; Mac OS 976,915; Windows Phone 30,409 | -
14 | no Linux; Fig. 4 shares are not the flow shares | claims 14; notes (Anomaly) | flow, session and address shares by vendor | HOLDS | flows: Microsoft 39.93, Google 37.95, Apple 22.12; sessions: Google 54.06, Apple 37.98, Microsoft 7.96; addresses: 55.3/36.0/8.7. None matches Fig. 4 (39.93/30.03/28.49), so "the paper does not say what they count" stands. Note: the release's Microsoft flow share equals Fig. 4's Google figure (39.93) to two decimals, perhaps a coincidence | PROV-3, USE-5
15 | 141/3,154 Windows sessions mostly TTL 64; 24 Mac OS, 7 Android mostly 128 | claims 15; notes | recomputed (TTL rounded up to 64/128/255, majority per session) | HOLDS | Windows 141 sessions, 260,552 flows (4.96%); Mac OS 24; Android 7; iOS 0; Windows Phone 0 on 64 | USE-5, LEAK-24
16 | 45,602 sessions, 1 label, 1 address each | claims 16 | grouped all flows | HOLDS | 45,602; 0 with two labels; 0 with two addresses (the paper's 8,071 IPv4 addresses against 6,165 source addresses in the release: not a claim, unexplained) | -
17 | UA OS fields dropped: 4.1% named, 96.5% majority | claims 17; notes; decision 1 | crosstab on task flows | HOLDS | named 4.09%, majority agreement 96.54%; code 3 -> Android 278,290 of 282,347 | LEAK-10
18 | src address: 1,724 of 6,165 with several labels | claims 18; notes | grouped | HOLDS | 1,724 / 6,165. AUC 0.921 not re-run | CLEAN-3
19 | dst address: 138,681 values; LightGBM 0.176 -> 0.163 | claims 19; notes | distinct count | HOLDS (count); model gain not re-run | 138,681 | CLEAN-3, USE-6
20 | session id leaves after the weight | claims 20 | shipped columns | HOLDS | not in data.parquet; 21 features | CLEAN-3
21 | duration, flow_start, period as inputs | claims 21 | feature_columns | HOLDS | flow_start and period in the 21 features; period is constant and unseen in each test window (harmless for trees) | -
22 | TLS lists: fixed-width LE 16-bit, padding at the end | claims 22; notes | hex lengths; decode | HOLDS | every extension value 112 hex (28 fields), ciphers and groups 32 hex (8); the longest decoded extension list has 20 entries (the paper says the exporter keeps the first 23), so no list reaches either cap; 8,692,829 cipher lists have 8 entries (the paper's truncation to 8) | CLEAN-12
23 | GREASE named: ext types 8,243 -> 469, ciphers 402 -> 311 | claims 23 | recounted | HOLDS | 8,243 -> 469; 402 -> 312 incl. the empty list (311 non-empty) | CLEAN-12
24 | point formats: 4294967295 = none, 764,225 flows, none with 0x000b | claims 24 | recounted | HOLDS | 768,054 all-filler, 764,225 with a version, 0 with 000b; 3 flows have formats but no 000b | CLEAN-12
25 | empty lists none vs missing | claims 25 | builder's heavy_checks.log; version counts | HOLDS (consistent) | SSLv2 94 flows = the 94 empty cipher lists | CLEAN-12
26 | ssh_client_version constant; 4 others on 186/187 | claims 26 | counted | HOLDS | version 187 flows, 1 value; application 187; encryption, MAC, compression 186 | CLEAN-5, CLEAN-22
27 | dtypes | claims 27 | shipped dtypes | HOLDS | as declared; strings SNI 44,911, host 10,659, ext types 428, ext lengths 11,601 distinct | CLEAN-14
28 | SNI and host stay | claims 28; notes | paper Table III | HOLDS (source fact); AUCs not re-run | specific domains 0.8659 | USE-6
29 | copies 0.7%, 84 duplicates (9 other label) | claims 29; notes | hashed inputs per split | HOLDS | input copies 0.24%, 0.24%, 1.55% of test rows (mean 0.68%), conflicting 0.00%; with strings and times 0.000%; 84 duplicates over features + label, 9 feature-duplicate groups with two labels | LEAK-16, LEAK-18
30 | 9,263 flows from 11 July | claims 30 | counted | HOLDS | 9,263, earliest 2019-07-11 23:50:08 | -
31 | largest session 578,764 (4.3%), top 10 12.0%, Windows 39.5% of flows / 7.0% of sessions | claims 31; notes | counted | HOLDS | 578,764 (4.35%); top 10 12.04%, all Windows; 39.51% / 7.02% of 44,925 task sessions | MET-17
32 | windows 15 Jul 12:00, 16 Jul 00:00, 16 Jul 12:00, newest first | claims 32 | splits | HOLDS | split 0 = 16 Jul 12:00 ... split 2 = 15 Jul 12:00; train strictly earlier (max period below the window on 3/3) | SPLIT-1
33 | 61.7 / 77.2 / 85.3%; daily 35.6%; paper day 1 18.8% | claims 33; splits_comment | recomputed | HOLDS | 61.74 / 77.23 / 85.34; 35.56; 18.84 | SPLIT-14, SPLIT-19
34 | no gap: label known at connection | claims 34 | paper Sect. IV | HOLDS (reasoning) | the label comes from the DHCP REQUEST that opens the session | SPLIT-10
35 | 16-21% of flows, 6-12% of sessions seen before | claims 35 | recomputed | HOLDS | flows 21.4 / 15.6 / 21.4%; sessions 12.4 / 5.6 / 12.3%. Accuracy on recurring-session flows differs from new ones by -0.1 to +0.7 points, so no memorisation gain worth a flag | SPLIT-13
36 | 500k test, 1M train, stratified, 2.5M frame | claims 36 | splits | HOLDS | 1,000,000 / 500,000 x3; train class shares equal the earlier population's to 0.01 points (e.g. 40.39/35.83/16.52/7.05/0.21) | SPLIT-26
37 | fallback log_loss weighted by session_weight; paper reports 4 micro-averaged metrics | claims 37; metric; README Metric | paper VI.B, Table III; Zenodo | HOLDS | the paper lists accuracy, precision, recall, F-score, micro-averaged, none named; page defines none. Fallback right (MET-5, MET-6); log loss for multiclass (MET-11) | MET-1, MET-5, MET-6, MET-11
38 | the weight changes the level, not the order (tau 1.0, six families) | claims 38; builder issue 1 | 13 LightGBM fits per window (configurations, session-weighted training, a class-prior shift), each scored per flow and per session | REFUTED | among the 9-10 competitive fits (session loss < 0.14) 17/36, 19/45 and 19/36 pairs swap order (tau about 0.0 to 0.16); the best fit per flow is never the best per session (3/3 windows). The builder's tau 1.0 compared feature subsets 0.05 to 1.2 apart | MET-17, EV-1
39 | session_weight for scoring only, never a training weight | claims 39; ScoringColumn description | the training rule holds by declaration (feature_columns drops it; sample_weight None). Its premise was tested | PREMISE REFUTED | weighted test class shares: Android 55-56%, iOS 30-32%, Windows 6.0-8.0%, Mac OS 4.8-5.5%, WP 0.9-1.3%, against 34-38% Windows per flow. An unweighted model's own class prior is wrong for the score: re-weighting its probabilities to the train side's session-weighted class shares lowers the declared loss on 6/6 fits (0.1234 -> 0.1155, 0.1283 -> 0.1197, 0.1320 -> 0.1176; 0.1076 -> 0.1013, 0.1023 -> 0.0960, 0.1128 -> 0.1010), 5 to 11%, and raises the per-flow loss. Session-weighted training helps a small LightGBM on 3/3 (by 0.012 to 0.034). That is larger than the probes' random-forest and LightGBM gap (0.002) | MET-15, MET-17, MET-2
40 | dummy 1.421, RF 0.131, LGBM 0.133, single feature 0.270 | claims 40 | flow-prior dummy rescored with the scorer | HOLDS | 1.388 / 1.440 / 1.436 (mean 1.4215). Note: the train side's session-weighted prior scores 1.094 / 1.066 / 1.086, the honest null for this metric; the RF's relative gain is 0.88, not 0.91; not trivial either way | TP-4
41 | no Anonymized tag | claims 41 | shipped columns | HOLDS | both addresses dropped; every shipped feature in the clear | -
M1 | metric computable on every fold (MET-2) | dataset.py metric, scoring_columns | scorer on a dummy per fold; units and classes per fold | HOLDS | scored 3/3; test sessions 7,676 / 5,975 / 7,222; every class present (WP 1,601 / 1,875 / 1,363 rows); session_weight not among the features | MET-2
M2 | unit weight valid under the budget (the fixed check) | brief; library | per-(session, half-day) weight sums | HOLDS (would pass) | full task frame: 49,854 units, sums 1.0 (+/-1e-16). Shipped frame: 43,948 units, 0 above 1, max 1.0. 0 units on both sides of any split (the unit carries its half-day) | MET-17
I1 | every feature known at the prediction point | implied | feature list against the export moment | HOLDS | duration ends at the export; no label proxy left (UA fields gone); session_weight not a feature | LEAK-10, LEAK-37
I2 | each Wi-Fi session counts once per window in the score | task_summary.split; ScoringColumn "before the window is sampled" | per-session weight sums in the shipped test windows | REFUTED (wording) | sums range 0.03 to 1.0, mean 0.279 / 0.481 / 0.263; 80 / 171 / 62 sessions count fully; single-flow sessions carry 6 to 11% of the weight. Equal only in expectation (uniform, stratified sampling) | MET-17, writing
I3 | the decision is per device (metric reason, fit_reason) | task_summary.use_case: "labels each connection with the operating system" | read the text against MET-17 | INCONSISTENT | MET-17 keeps the per-row score "when each row is a decision of its own"; the use case says each connection is labelled, while the reason for the weight says "the inventory decides per device" | USE-1, MET-17
I4 | the session is the actor's unit (MET-1) | metric reason | devices against sessions | UNTESTED | no MAC in the release; the paper gives 45,602 sessions for 11,962 MACs over 5 days, so a device can have several sessions in a half-day and count more than once | MET-1
I5 | no row is a copy across the split | implied | claim 29 | HOLDS | 0.000% with every input; 0.68% fingerprint copies, all same label | LEAK-16

Not re-run (the builder's probes, consistent with what was checked): the source-address AUC 0.921, the destination-address
LightGBM gain, SNI/host AUCs (18, 19, 28).

========================================================================================================================
REFUTED AND UNTESTED, RANKED (principles.md: validity first, Must first; nothing hits P1-P5)
========================================================================================================================
1. P6, MET-2 / MET-15 / MET-17 (Must via MET-2): claims 38 and 39's premise. The session weight changes which
   prediction is best. Windows is 34-38% of a window's flows but 6-8% of its weight, so a model trained on flows
   carries the wrong class prior for the score. A post-hoc prior shift alone gains 5-11% of the loss on 6/6 fits. Close
   models swap order between the two scores in about half their pairs. As shipped, the benchmark partly measures
   whether a pipeline learns the session-level class prior. It can do so only through session_weight (validation
   weighting or calibration), and the README forbids it as a training weight. Builder issue 1 says "the call moves
   levels, not the order", so it understates the call.
   Changes: issue 1's evidence and its weighing; the TP baseline (honest dummy 1.08, not 1.42).
   Mildest remedy: correct issue 1 with these numbers (keep option (a) or (b) for the curator). Under (a), say in the
   README Metric block that the score's class balance is per session and that `validation_weight` gives it. Under (b),
   the per-flow log loss has no such mismatch. A third option for the curator: ship session_weight as the sample_weight.
   That is an exception to MET-17's "scoring only", and the schema then forbids also declaring it as unit_weight.

2. P6, MET-17 (Should): unit_weight not declared. Declaring it needs the unit's column, which `_clean` drops with the
   session id. Under the fixed check it would pass: shipped sums are at most 1.0, and no unit spans train and test
   (M2).
   Mildest remedy: keep an opaque `session_window` id (the (session, period) pair factorised in a random order, so it
   encodes neither time nor session), declare `unit_weight = UnitWeight(column="session_weight",
   unit="session_window")`. feature_columns then drops it, and validation_weight users group by it.

3. Writing / P3 (USE-1, MET-17): I3. The use case's decision is per connection, the metric's is per device.
   Mildest remedy: reword use_case so the team records each device's OS per Wi-Fi session from its connections. Then
   the weight follows (MET-17), and "labels each connection" no longer argues for the per-row score.

4. Writing (MET-17): I2. Replace "Each Wi-Fi session counts once per window in the score" in task_summary.split with
   "each Wi-Fi session carries the same weight in a window's score (once before the window is sampled to 500k flows)".

5. Untested, MET-1: I4. The unit is a session per half-day, not a device. A device with several sessions in a half-day
   counts several times. This cannot be measured without the MAC addresses. Name it in fit_reason's "rows are flows
   while the inventory decides per device" (sessions, not devices).

Small notes, no change needed: claim 23's cipher count is 312 with the empty list, 311 without. The paper's exporter
keeps "the first 23 extensions", while the field has 28 slots and at most 20 are used (claim 22 holds). The paper has
8,071 IPv4 addresses, the release 6,165 source addresses (not a claim).
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-08

Verdict: ship after small changes. The audit found no leak. The drop of the User-Agent OS fields is right (LEAK-10,
"another encoding of the target"). The destination address stays a weighing call: next to the server names it adds
nothing consistent (-0.0003 session-weighted log loss, medium LightGBM, 3 windows), so I side with the builder's (a).
Five P7 cleaning points, each cheap and safe.

Sources read: dataset.py; the builder's report, claims and probe outputs; the paper (paper.txt, Sect. III-VI); the
Zenodo record page (field list: "SYN size: the size in bytes of the initial TCP SYN packet", Session ID "matches flows
from the same device", addresses under Crypto-PAn; it gives no SSH fields and no UA OS codes); the rules principles.md,
use_case.md, leak_checks.md and cleaning_features.md from the df-large worktree.
Measured on: the definition's frame rebuilt with dataset_io.from_definition (2,500,000 rows x 22 columns; 21 model inputs,
`period` among them), and the builder's all-string copy of the release for the dropped columns
(all_str.parquet, 13,309,494 task flows).
Dtype probe (re-run, --no-fetch): 0 of 15 columns flagged; with no codebook it cannot see a code typed as a number. My
reading flags `dst_port` (finding 3).

PREDICTION POINT (first curation_comments bullet): a flow record is exported, at the connection's end or after 300 s.
Inputs: what the monitor reads in the clear (the SYN, the ClientHello, a plain-text HTTP host, an SSH banner). The
device's identity (address, session) is not an input. Every kept column below exists by then. The label (DHCP host
name) is set at the session's start. No column is filled or emptied by the label.

======================================================================================================================
COLUMN TABLE
column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule
----------------------------------------------------------------------------------------------------------------------
flow_start | time of the flow's first packet, on the probe's clock (Zenodo "Date flow start") | yes, it is before the export | datetime, no missing values | fine | USE-6
src_port | the client's ephemeral L4 port (Zenodo "sPort") | yes (SYN) | numeric, 1025-65535. The range follows the stack: 63.7% of Android flows fall in [32768, 49152), 0.1% of Windows flows. Port 4001: 8,327 shipped flows, 8,287 of them Windows (one application) | fine. A number is right: the range is the signal | CLEAN-14
dst_port | the server's L4 port, i.e. the service (Zenodo "dPort") | yes (SYN) | numeric, 13,767 values. The top 10 cover 96.9% of rows (443, 80, 993, 5228, 5223, 5222, 110, 3091, 55, 7275) and 96 values have >=100 rows. Ports 55 and 3091 are 100% iOS, 7275 is 99.8% Android, 110 is 95.8% Android | cleaning problem: a service code typed as a number | CLEAN-14 (last bullet), finding 3
syn_size | "the size in bytes of the initial TCP SYN packet" (Zenodo): the IP total length, since 52/60/64 = a 20-byte IP header plus a 32/40/44-byte TCP header | yes | numeric, 31 values. 328 task flows (87 shipped; 300 and 82 of them Windows) hold 2 to 34 bytes, below the 40-byte minimum of an IPv4 TCP SYN. The 230-248-byte SYNs (1,084 Windows flows, port 443) are SYNs that carry data (TCP Fast Open) and are real | cleaning problem (impossible values), small | CLEAN-11, finding 4
tcp_window | the SYN's TCP window value (Zenodo "TCP win") | yes | numeric, 7300-65535, no 0 or proxy value | fine | CLEAN-14
syn_ttl | the TTL observed at the probe (the stack's initial TTL minus the hops; paper Sect. V.A) | yes | numeric, 8 values (62 and 126 dominate). The paper rounds up to a power of two; the definition leaves that to the models, which is right (CLEAN-2) | fine | CLEAN-2, CLEAN-14
tls_sni | Server Name Indication from the ClientHello (paper Sect. III) | yes: in the clear in the 2019 ClientHello | string, 44,911 values, missing for non-TLS flows and for TLS without SNI. The release cuts the name at 64 bytes (5,998 task flows have tls_sni_length > the string's length). No DHCP host-name pattern (android-<hex>, DESKTOP-/LAPTOP-<id>, a device's own name) appears in the SNI or the HTTP host, so the label's source does not leak through the server names. The 200 shipped IP literals are public server addresses (none private or 147.251.*) | fine | USE-6, LEAK-37
tls_sni_length | the SNI's length in bytes (Zenodo) | yes | numeric, 0-82. It is no copy of tls_sni: it keeps the full length where the name is cut. 0 on 89,696 TLS flows without SNI is a real value. On the 3,829 task flows (888 shipped) where no ClientHello was parsed (version missing, every list filler), 0 is the probe's filler; the definition sets every list to missing there but leaves this 0 | cleaning problem (proxy value), small | CLEAN-10, finding 5
tls_client_version | the ClientHello's legacy version field (paper Sect. III) | yes | category, 5 levels (SSLv2.0 ... TLSv1.2). Per the paper, the probe exports TLS 1.3 clients as TLSv1.2. 911,966 of the 1,854,291 shipped TLSv1.2 rows (49%) carry supported_versions (0x002b), i.e. are TLS 1.3 clients. The notes do not say so | fine; one line for the notes | CLEAN-12 (meaning), writing
tls_cipher_suites | the first 8 offered cipher-suite IDs, in the client's order of preference (paper Sect. III) | yes | category, 276 shipped levels (311 over the task flows). The decoding checks out: Chrome 75's list (GREASE,1301,1302,1303,c02b,c02f,c02c,c030) and Apple's (1303,1301,1302,c02c,...). GREASE is named. The SSLv2 empty lists are missing | fine | CLEAN-12
tls_extension_types | the extension IDs in ClientHello order (28 slots; no shipped list fills them) | yes | string, 428 shipped values (469 over the task flows). The decoding checks out: Chrome's exact order with GREASE first and before padding 0x0015, and Apple's 0x3374 (NPN). 'none' is used for 545 parsed hellos without extensions | cleaning problem: typed string while the cipher lists, the same kind of column with a similar number of levels (276), are categorical, and the paper encodes every TLS list as categorical | CLEAN-14, finding 6
tls_extension_lengths | the length of each extension, decimal | yes | string, 11,601 values. The many values come from per-connection lengths (SNI+5, padding, ALPN). The decoding checks out on Apple's list: key_share 38, supported_versions 9, padding 165 | fine (string is right at this many values) | CLEAN-14
tls_elliptic_curves | the first 8 supported groups (paper Sect. III) | yes | category, 28 levels; GREASE named; 0x001d=x25519 etc. check out | fine | CLEAN-12
tls_ec_point_formats | the EC point formats list, decoded from a 4-byte number | yes | category: '0', '0,1,2', '0,1', 'none'. Consistent with the extension list: 'none' never comes with 0x000b, and '0' comes without 0x000b once | fine | CLEAN-12
http_host | the Host header of a plain-text HTTP request (Zenodo) | yes (clear text) | string, 10,659 values, 93% missing (non-HTTP flows). It is not a statement of the OS. It holds service names (connectivitycheck.gstatic.com, init-p01st.push.apple.com) as in the paper's "specific domains" method | fine. Writing nit: the use_case says "fields that stay readable when the traffic is encrypted", while the host comes from unencrypted HTTP (6.8% of task flows) | USE-6
ssh_client_application | the SSH client's software from its banner (not on the Zenodo page; read from the values: OpenSSH_7.9, PuTTY_Release_0.70, ...) | yes (clear text) | category, 6 levels on 52 shipped rows (187 task flows) | fine | CLEAN-22
ssh_client_encryption | the client's first offered cipher (inferred from values) | yes | category, 3 levels | fine | CLEAN-22
ssh_client_mac | the client's first offered MAC; '<implicit>' = an AEAD cipher | yes | category, 4 levels; '<implicit>' is a real value, not a missing code | fine | CLEAN-10, CLEAN-22
ssh_client_compression | the client's first offered compression | yes | category, 2 levels | fine | CLEAN-22
flow_duration_s | end minus start (seconds), 0-300 | yes at the export (the prediction point). The span ends at the connection's end or at the 300 s active timeout, never at the label | numeric; 0.69% of rows >= 299 s; continuation records of cut flows have no SYN and leave with USE-7 | fine | LEAK-37, LEAK-10 (span clause holds)
period | flow_start floored to 12 h: the split's time key | yes | datetime. It is a model input (feature_columns keeps the time key; the README counts it among the 21 features). It is a coarser copy of flow_start, constant within each test window and never seen in the train side | cleaning note: a redundant input | CLEAN-5 (spirit), finding 7
os | target: OS from the DHCP host name (paper Sect. V.C) | n/a | category, 5 classes | fine (label noise in the notes) | USE-5
session_weight | scoring column: 1 / the session's flows in the half-day | not a feature | float, excluded by feature_columns | fine | MET-17

DROPPED COLUMNS
http_ua_os, _major, _minor, _build | the OS (and version) the probe parses from a plain-text User-Agent | known at the prediction point, in the same flow | dropped | agree: LEAK-10, "another encoding of the target". The UA is the device's own statement of its OS, the label is its DHCP host name: two self-reports of one quantity. The paper uses the UA as the training label of its ML methods (Sect. V.B). Where the code names an OS (4.1% of task flows; 65535 = unknown on 14.0%) it agrees 96.5% with the label. LEAK-37/USE-6 does not save it, because it encodes the target. LEAK-2 sweep: no other UA-derived field is in the release. http_host stays: a server name, not an OS statement. Strong but narrow: 4.1% of rows. Remedy: the drop, as done.
src_ip | the device's Crypto-PAn address (prefix-preserving) | known | dropped | agree: an identifier of the device (CLEAN-3; the stated prediction point), reused across devices and sessions. All task flows share one /16 (151.27) in 40 /24 Eduroam pools. The pool's flow mix varies (Windows 11% to 80% of a pool's flows), but by sessions the pools are much alike, and a /24 would be our own construction (CLEAN-19). Measured: the /24 as a category, next to the server names, makes the session-weighted log loss worse on average (medium LightGBM 0.1091 to 0.1115, shallow 0.1515 to 0.1521; 3 windows). The drop is confirmed
dst_ip | the server's Crypto-PAn address, 138,681 values; never equal to a source address (no device-to-device link) | known, in every flow, in the clear | dropped (builder's draft issue 2, option a) | weighing call, finding 2. Measured next to the server names: no consistent gain (medium LightGBM, session-weighted -0.0023, -0.0009, +0.0023 over the 3 windows; shallow -0.0011, -0.0001, -0.0016). See problem 1
session_id | the RADIUS session of the device (Zenodo: "matches flows from the same device") | not an input under the framing | dropped | agree that it is not a feature (LEAK-33, CLEAN-3). But it is the score's unit: once library gap 2 is closed it should ship as UnitWeight.unit, metadata that is never a feature. That lets a model's inner validation keep a session's flows on one side, as the UnitWeight docstring intends. Finding 8
ssh_client_version | the SSH protocol version | known | dropped | agree: constant 2.0 on all 187 task flows that have it (CLEAN-5)
flow_end | the flow's last-packet time | known at the export | turned into flow_duration_s | agree: lossless with flow_start

======================================================================================================================
PROBLEMS, RANKED (principles.md: rank, then strength, then effect)

1. (P3/P4 framing against P7; weighing) The destination address is dropped although it is known at the prediction point.
   This is the builder's draft issue 2. The builder's numbers left the server names out (0.176 to 0.163). Measured
   with them in (the builder's windows and draw, seed 0; SNI and HTTP host as categories of the top 5,000 train
   values; the duration added; LightGBM; dst_ip_with_names.json):
   variant (mean of 3 windows)     shallow (4 leaves, 50 trees)   medium (31 leaves, 300 trees)
                                   session-wtd   per flow         session-wtd   per flow
   names (SNI, host), no address   0.1515        0.1441           0.1091        0.1049
   names + dst_ip                  0.1506        0.1419           0.1088        0.1031
   names + src /24 (finding: src)  0.1521        0.1458           0.1115        0.1077
   Per window, session-weighted, dst_ip minus none: shallow -0.0011, -0.0001, -0.0016; medium -0.0023, -0.0009,
   +0.0023. The builder's gain without the names (0.176 to 0.163, -7%) mostly repeats what the names carry: the names
   alone take the shallow model from 0.176 to 0.151. Next to them the address adds 0.6% (shallow) or nothing
   consistent (medium, the sign flips). The builder's "smaller or equal" now has a number.
   Steelman of shipping it (b): USE-6 (Must) makes any input known at the prediction point legitimate. The address is
   the server, an attribute of the flow like the SNI (or a merchant id), not the identity of the row or the device.
   It never equals a device address, and the 22% of task flows with neither SNI nor host (2.89M) have no other server
   identity. A small score is no reason to drop a column (CLEAN-22, LEAK-10's 2026-10-21 note).
   For keeping it dropped (a): CLEAN-3 drops an identifier that is uninformative. Crypto-PAn leaves only the identity
   of a server whose name the task already reads, and the decisive experiment (EV-1) shows next to no information
   beyond the names. Shipped as a string (CLEAN-14: 138,681 values), it would reach only the models that read
   strings, which are the models that already have the names. The ugr16_isp_netflow_intrusion_1m precedent (addresses
   dropped because the label was assigned on them) does not decide this case: here the label comes from DHCP.
   Recommendation: (a), keep it dropped, and replace the 0.176/0.163 sentence in the notes with the numbers measured
   next to the names. The question stays with the curator as a weighing call (issue 2). (b), as a string, is the
   alternative if the curator puts USE-6 first. Not (c), the /16 prefix: our construction.

2. No leak found (P4). LEAK-10 holds: the UA drop is right, flow_duration_s is a span the label never sets, and no
   column's missingness depends on the label (the builder's missing-indicator probe: 0.532). The server names carry no
   device host names, the label's source (checked by pattern on the shipped rows: no android-<hex>, DESKTOP-/LAPTOP-<id>,
   <name>-iphone or .local host; the only hits are service names such as laptop-updates.brave.com). Entity recurrence through src_port (some stacks allocate ports in sequence), rare TTLs (60, 61, 63, 125, each
   held by one class) and SNIs is a known entity's history under a temporal split. LEAK-34 makes it legitimate, and the
   splits comment states it (16-21% of a window's flows).

3. (P7, CLEAN-14 Should) `dst_port` is a service code typed as a number. CLEAN-14's last bullet: "A code the source
   ships as a number (an id, a type code, a detector column) is a category, unless its digits carry meaning a model
   can use". The definition's own reason is that the destination port "names the service". The range does mean
   something (well-known, registered, dynamic), but 93-96% of every class sits below 1024, and the services are
   point values (5222/5223/5228: XMPP, Apple push, Google push). The ugr16 precedent keeps ports numeric because one
   end is always 25 and the other ephemeral, so it does not carry over. src_port stays numeric, as its range is the
   signal. Remedy: type dst_port categorical (codes as shipped, no decoding to names).

4. (P7, CLEAN-11 Should) `syn_size` holds impossible values: 328 task flows (87 shipped, 82 Windows) of 2-34 bytes,
   below the 40-byte minimum of an IPv4 TCP SYN (Zenodo: "the size in bytes of the initial TCP SYN packet"). Remedy:
   set to missing where syn_size < 40 and keep the rows (their other SYN fields are plausible: window 65535, TTL 126).
   Say so in the notes. Note: the task filter `syn_size.notna()` runs before this, so these rows stay task rows.

5. (P7, CLEAN-10 Should) `tls_sni_length` is 0 on the 3,829 task flows (888 shipped) with no parsed ClientHello. That
   0 is the probe's filler, by the definition's own reading ("the probe parsed no ClientHello: missing"), which it
   applies to every list but not to this column. Remedy: set tls_sni_length to missing where tls_client_version is
   missing. If the curator wants the trace "a TLS record the probe could not parse" kept, keep it with a note instead.

6. (P7, CLEAN-14 Should) `tls_extension_types` is typed string (428 shipped levels, 469 over the task) while
   `tls_cipher_suites` (276, 311) is categorical. Both are short ordered ID lists of a finite registry, and the paper
   encodes every TLS list as categorical (Sect. V.A). The builder's split ("the long extension lists are strings")
   rests on string length, not on what the column is. The type matters here: the probes' "all features" score (0.972)
   leaves string columns out, and the column alone as text scores 0.915, the strongest TLS field. A pipeline that
   embeds or drops strings handles it unlike its sibling. Remedy: categorical, like the cipher list.
   `tls_extension_lengths` (11,601 values) stays a string.

7. (P7, CLEAN-5 spirit; library gap 1) `period` is a model input and a coarser copy of `flow_start`. Within each test
   window it is one value that never occurs in training. It adds nothing a model can use beyond flow_start and may
   invite extrapolation on an unseen level. Remedy, mildest first: keep with a note naming it the split key (it is
   there only because TemporalSplits has no hours unit), or close library gap 1 and split on flow_start directly,
   dropping `period`.

8. (P7 / metric support) `session_id` is dropped instead of shipped as the score's unit (UnitWeight.unit, metadata,
   never a feature). That blocks unit_weight and lets a model's inner validation spread a session over train and
   validation. Remedy: ship it as UnitWeight.unit once library gap 2 is closed. Until then, a note.

9. (Writing) Add a line each: tls_client_version is the ClientHello's legacy version, so TLS 1.3 clients show as
   TLSv1.2 (49% of the shipped TLSv1.2 rows carry 0x002b; paper Sect. III); the release cuts the SNI at 64 bytes
   (5,998 task flows), and tls_sni_length keeps the full length; the use_case wording "readable when the traffic is
   encrypted" leaves out the plain-text HTTP host it keeps.

Optional, not a finding: tls_client_version could be an ordered category (SSLv2.0 < SSLv3.0 < TLSv1.0 < TLSv1.1 <
TLSv1.2). The paper calls it an identifier whose number has no meaning, and CLEAN-14 leaves ordinal scales case by
case. Unordered is acceptable.
```

</details>

<details><summary>Split audit</summary>

```text
Split audit: tls_os_fingerprinting_masaryk_1m (record tls_os_fingerprinting_masaryk), split-auditor, 2026-11-08

VERDICT: right with notes. Temporal is the regime the use case implies. The three half-day windows meet SPLIT-14, and the
train sides are what a refit at each cutoff would see. "No gap" holds. Recurring sessions add 0.0014 to the declared
score. A split grouped by session scores the same as the shipped temporal split on the same half-days, and IID is
optimistic by about 0.010. None of the findings needs a re-split. Findings 1-3 ask for a sentence each in
`splits_comment`.

Judgment record
  Validity: SPLIT-1, SPLIT-2, SPLIT-3 hold (temporal); USE-10 known population, LEAK-34 (entity history legitimate),
    effect measured; SPLIT-9 holds (no label of a test row's own session set after its prediction point); SPLIT-10
    holds without a gap (measured); SPLIT-11 holds (expanding); SPLIT-14 holds (61.7/77.2/85.3%); SPLIT-19 departure
    justified by SPLIT-14 (a Must over a Should), with its cost measured; SPLIT-24/25 do not apply (temporal).
  Weighed: horizon 12 h is ours (SPLIT-12); the whole release is one summer week (July break), so no window is more
    atypical than its training side (SPLIT-20).

How it was measured (EV-8)
  - Data: the definition's `_clean` run on `flows_all.parquet` (13,309,494 task flows), with the session id, the flow
    end and the raw position re-attached by raw index. The shipped split plan comes from `make_splits()`, and its rows
    were traced to raw positions through `dataset_io.from_definition(raw=True)` ("traced by the column"). Train and test
    indices were taken as shipped, never re-split.
  - Model: one untuned LightGBM per split (300 rounds, lr 0.05, 63 leaves, 4 threads, train 1M, test 500k). The 21
    shipped features: lists of up to 62 levels as categories, the other list and server-name columns as their
    training-frequency rank among the top 3,000 values. Times as numbers, or dropped ("no time").
  - Score: the declared metric, log loss weighted by `session_weight` (wLL). Bagging seed noise is 0.0005 on the
    mean (seed 0 against seed 1).

Facts checked (all measured on the task flows)
  - Train shares: 61.74%, 77.23% and 85.34% for the windows at 15 Jul 12:00, 16 Jul 00:00 and 16 Jul 12:00. Daily
    windows would train the third newest day (14 Jul) on 35.56%. The paper's day 1 holds 18.84%. All as claimed.
  - Half-day sizes: AM windows 0.55M to 1.07M flows, PM 1.50M to 2.06M (hourly trough at 04:00, peak at 13:00). The
    test windows are Mon PM, Tue AM and Tue PM. Every train side holds Fri 12 Jul, the weekend and Monday, as a random
    1M drawn in proportion to the pool. For example, the 15 Jul 12:00 train side has Fri 121k + 182k, Sat 67k + 204k,
    Sun 79k + 215k and Mon AM 131k, plus 1.1k from the 11 Jul tail. Train strictly before test: asserted on all 3.
  - Sessions: 44,925 task sessions. 40,240 (89.6%) lie in one half-day, 4,509 in two, and 176 in 3 to 10. Flows of
    sessions spanning more than 12 h: 8.0%. Test rows (shipped samples) whose session has an earlier flow: 21.5%,
    15.6% and 21.4%. This is mostly sessions that straddle the cutoff (connected before noon or midnight).
  - Devices: the paper counts 11,962 MAC addresses over 45,602 sessions (3.8 sessions per device in 5 days). The
    release has no device key: the source address is per session and reused across devices. A session is not a
    device.

Alternatives run (wLL on each test window; windows newest first; mean in brackets)
  A  shipped temporal, no time features           0.1078 0.1098 0.1173  [0.1116]  (seed 1: [0.1121])
  A' shipped temporal, times as numbers            0.1132 0.1286 0.1379  [0.1266]
  B  shipped windows, test window's sessions
     removed from train, no time                   0.1093 0.1108 0.1190  [0.1130]
  C  paper's history: 1M of day 1 (12 Jul),
     same test windows, no time                    0.1318 0.1385 0.1388  [0.1364]  (times as numbers: [0.181])
  D  grouped by session, 3 folds over all 5 days
     (times as numbers), rows of the last 3
     half-days in each test fold                   0.1085 0.1104 0.1137  [0.1109]  (all rows: [0.118])
  E  IID random rows, 3 folds (times as numbers),
     same restriction                              0.1011 0.1043 0.0987  [0.1014]  (all rows: [0.102])

Findings, in rank order (all under P4; none is a Must violation)

1. P4, USE-10 / SPLIT-13 / LEAK-34 (Should, a note). Sessions recur across the cutoff, and the regime is temporal, not
   grouped.
   Evidence: B against A. Dropping every session of the test window from the training side (3-5% of its rows) moves
   the window score by +0.0015, +0.0010 and +0.0017 (mean +0.0014, about 3 times the seed noise). On the
   recurring-session rows the change is +0.0097, +0.0058 and +0.0120. On the new-session rows it is +0.0003, +0.0006
   and +0.0002. So the model does recognise a straddling session a little. That is worth about 0.001 of the declared
   score, because those sessions are only 6-12% of a window's session weight. The recurring rows are easier in every
   variant, including C, which never saw those sessions (0.075-0.15 against 0.11-0.19): they are easier rows, not
   memorised ones.
   Regime: the inventory faces a recurring campus population (3.8 sessions per device). The model gets no device or
   session key. The paper's own design is a time split over the same population. A refit at noon has the morning
   flows of sessions still connected, and their labels were known at connection, so this is legitimate entity
   history (LEAK-34), not a SPLIT-9 shortcut. A split grouped by session (D) would not test new devices either,
   because sessions of one MAC would sit on both sides. It also scores the same as the temporal split on the same
   half-days (0.1109 against 0.1116). Temporal stays (SPLIT-3, USE-10).
   Remedy (mildest): none to the split. Add the measured effect to `splits_comment` next to the shares it already
   gives. A suggested sentence: "the test window's sessions in training improve the window score by 0.001-0.002 (0.006
   to 0.012 on their own rows)".
   Open for the curator (a P3 question, not a split defect): the "no gap" reasoning says the label is known when the
   device connects. A deployed system would then already know the OS of every labelled session, so the model's real
   use is for devices without an informative host name. Those devices are absent from the release, and no split here
   can simulate them. The `fit_reason` already names approximate; it could add this.

2. P4, SPLIT-10 / SPLIT-9 (Should, a note). No gap is needed, and the reason should be stated.
   Evidence: the label (the OS from the DHCP host name) is set at the session's start, before any of its flows (paper
   Sect. IV), so no training label is delayed. What is late is the flow record itself: it is exported at the
   connection's end or after 5 minutes. 3,850, 1,656 and 3,896 pool flows start before the cutoff and end at or after
   it (0.047%, 0.016% and 0.034% of each training pool, about 160 to 470 rows of each 1M sample). A refit at the
   cutoff would not have them yet.
   Rule: this is not a selection by the outcome (the label is the OS, not the duration), so the trip-time precedents
   (nyc_taxi_trip_duration_1m and siblings: a one-day gap wherever a training trip ended after the window start) do
   not apply. There the late quantity was the label. Under SPLIT-10 as amended, the measurements decide, and they
   show neither a shortcut nor a selection.
   Remedy: none. Optionally add one clause to `splits_comment` ("training flows still open at the cutoff, at most
   0.05%, are kept: their label was known at connection and their duration is a feature, not the outcome"). A
   training filter on `flow_end < cutoff` would be cleaner, but the shipped frame has no `flow_end`, and the effect is
   too small to need it.

3. P4, SPLIT-19 / SPLIT-12 (Should, the departure is justified; give its size).
   Evidence: the paper trains once on day 1 (18.84%) and tests on 4 days, with one training side for all of them.
   That is one evaluation under SPLIT-14, and it is below the 50% floor (a Must). The half-day windows are the
   closest design above the floor. Trained on 1M flows of day 1 and tested on the same three windows (C), LightGBM
   scores 0.136 against 0.112 for the expanding train side. With times as numbers it is 0.181 against 0.127. The
   shipped task is therefore easier than the paper's protocol, by drift over the days. The 12-hour horizon (a refit
   twice a day) is our choice, not the source's (SPLIT-12). The `splits_comment` says so ("a plausible cadence").
   Remedy: none to the split. Optionally give the measured gap to the paper's protocol in the notes, so a reader
   comparing against Table III knows the protocols differ.

4. P4 / P7 boundary (a note for the column auditor; not a split defect). The time columns are model inputs.
   Evidence: `period` (the split key, `flow_start` floored to 12 h) and `flow_start` ship as datetime features. In
   every test window both lie beyond the training range, and `period` is constant within a window. Read as plain
   numbers, they cost LightGBM 0.015 wLL on the shipped windows (A' 0.1266 against A 0.1116) and 0.045 under the
   day-1 history. `period` adds nothing that `flow_start` does not carry. It exists only because `TemporalSplits` has
   no hours unit (the builder's library gap 1). Shipping the time key as a feature is the house convention, and how a
   model encodes a date is the model's job (the `encodings` module). So this is not a defect. The 0.015 is the price
   a naive model pays.
   Remedy (mildest): keep it. If the library gains an hours unit, key the windows on `flow_start` and drop the derived
   `period`.

5. P4, SPLIT-29 (no finding; reported because the prompt asked). Hidden groups and the IID alternative.
   Evidence: the hidden-group probe has no hits (temporal regime). IID folds (E) score 0.101 on the same half-days,
   against 0.111-0.112 for both temporal and grouped by session. That is about 0.010 of optimism: rows of one session
   on both sides, plus interpolation in time. IID would be the wrong split, and it is not the one shipped.

Checked, no finding
  - Windows: three, each with its own expanding train side (SPLIT-11, SPLIT-14). Every window is far above SPLIT-17's
    50 rows (500k test rows each; smallest class 550+ rows, per the task probe). An AM and a PM window both test,
    and all three are weekdays after a weekend-heavy history: the real future of a Monday refit, not an atypical
    season (SPLIT-20). The release is a single July week, so no longer history exists to check for breaks.
  - The sampling to 500k per test window and 1M per train side is random and stratified by the OS. The session weight
    is computed before the sampling, so a window's weighted log loss stays an unbiased per-session score.
  - The train sides never hold a row at or after their cutoff (asserted). The 9,263 flows from 11 Jul (period 11 Jul
    12:00) sit in every train side, never in a test window.

Not checked
  - Whether model families rank the same under the session-grouped split. Only LightGBM was run there. The scores
    under the temporal and grouped splits agree within 0.001 on the same rows, so a reversal is unlikely, but it was
    not tested.
  - Recurrence at the device level (MAC addresses are not released). Its effect beyond the session-level 0.0014 cannot
    be measured.
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER REPORT: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-08

Actor played: the network security / asset-inventory team of a university, running flow monitoring (Flowmon-style
IPFIX probes) on its campus Wi-Fi, that labels devices with their OS from passive flow records to find unmanaged or
outdated devices.

VERDICT
Fit: APPROXIMATE (agree with the definition). The inputs are what my flow monitor exports for each flow and the
session weight counts my unit, but on this network I already have the label (the DHCP host name) when the device
connects. So the model stands in for devices I cannot label that way, and three things fall short of my decision:
the five-class closed set leaves out the Linux and "other" devices I hunt, there is no OS version (so nothing on
"outdated"), and I make my decision by combining a device's flows, not one flow at a time (USE-5, USE-8).
Metric scores my decision: PARTLY. A session-weighted log loss is a proper rule (MET-8), it is the right fallback
(MET-5, MET-6), and it counts my unit (MET-17). But it scores a session's average flow, not the verdict I build from
all of the session's flows, and on my probe the two rank model families differently (Kendall tau 0.6 to 0.8).

ANSWERS IN THE ACTOR'S VOICE

1. Inputs at the prediction point (USE-3, USE-6)
   - Each shipped input exists when the flow record is exported: the SYN size, window and TTL, the ports, the start
     time and the duration (capped at the 300 s active timeout), the TLS ClientHello fields, the SNI, a plain-text HTTP
     host and the SSH banner. Dropping the User-Agent OS fields is right for the encrypted-traffic task (LEAK-10).
   - Inputs I always have that the rows lack:
     (a) The device's other flows. My collector keys on the source IP, so every flow comes with the device's history
         in the same lease. The definition drops the source IP and the session id as identities (CLEAN-3; the
         address alone scores macro ROC AUC 0.921). That is correct for a per-flow fingerprint, because the address
         names the device and not its stack. In my deployment, though, the history is how I decide (gap 1).
     (b) On this network, the DHCP request itself: the host name, which is the label, and the option-55
         parameter-request list. NAC and IPAM tools use option 55 for OS profiling (Fingerbank, Cisco ISE,
         Infoblox). Shipping these would hand over the label. I mention them because they explain why I would only
         need this model where no DHCP signal reaches me (gap 4).
     (c) The MAC OUI (vendor). It is not in the release.
   - Inputs I would not have: none found. The flow start is the probe's clock, and the time of day is legitimate.

2. Target (USE-5)
   - What I act on is the OS of a device, at the level of "is it a supported, managed system". The label is the OS
     name only. The paper's Table II says the ground truth has no version ("vendor, name"; major version only in
     part), so the "outdated device" question cannot be answered from this target. For an OS-family inventory it is
     the right target.
   - I would want a probability per device. It lets me flag low-confidence or contradictory devices: a host name
     that claims Windows on a stack that does not look like Windows is exactly the spoofed or unmanaged device a
     security team looks for. A probability serves that, and log loss rewards it (MET-8).
   - The closed set: Android, iOS, Mac OS, Windows and Windows Phone. Linux and "other" (BlackBerry, IoT) are
     missing, although the paper's Fig. 4 gives them 1.48% and 0.07%. For a security team those are the interesting
     devices: unmanaged Linux machines, appliances, IoT. A model trained on five classes will confidently call a
     Linux laptop "Android", since the two share a kernel TCP stack, and it cannot say "unknown". Windows Phone
     (1.0% of task sessions, support ending December 2019) is a class I would merge or drop today, but it is real
     for July 2019. This is a closed-set gap like sarcoma's (USE-8 cases).
   - Label quality, checked by me (ttl64_windows.py). The definition's anomaly bullet
     suggests the 141 Windows-labelled sessions with a 64-TTL stack are "maybe devices whose host names misled the
     labelling". The data says otherwise. Their SYNs are the Windows stack's: SYN size 52 with window 64240 on
     205,630 of their 260,552 flows, the modal Windows pair (4.38M flows of all Windows). Their plain-text
     User-Agent, where present, carries code 68, the Windows majority code, in 103 of the 141 sessions. And 137 of
     the 141 never send a SYN with a TTL above 64. So these are Windows hosts whose TTL arrives at 64 or less (a host
     TTL setting or a TTL-rewriting hop), most likely labelled correctly, and the TTL is the odd field. NAT,
     tethering or VMs that mix stacks within a session are rare: 12 Windows and 18 Android sessions with 5-95% of
     their SYNs above TTL 64 (63k flows). For the claim auditor: the bullet's guess should name this evidence.

3. Does one row match one decision? Is the test what I face? (USE-10, SPLIT)
   - A row is one flow. My decision is one per device, roughly one per session per half-day. The weight gives each
     session one vote, which fixes the count. But I build a device's verdict from all its flows, and the rows are
     scored one by one (gap 1). Per-flow labelling is a real use case too (USE-9): tagging each flow or alert with
     the OS in the SIEM. For that use the unweighted per-flow score is the right one, and it is the paper's unit
     (Sect. VI.B). The definition chose the inventory, so the session weight goes with it.
   - Test data: the next half-day of the same network, with a model refit on everything earlier. As an operator who
     refits twice a day, that is a plausible deployment. But the test devices are DHCP-labelled devices whose label
     I already hold. The devices I would actually run the model on are those without a usable host name (edited
     Windows names, newer phones that send randomised or no host names, other segments), and those are a different
     population. Devices recur more than the session counts show: 44,925 task sessions from 6,160 addresses, and
     11,962 MACs in the paper. Fingerprints belong to stacks, not devices, so the recurrence matters less than for
     user identity. The SNI and HTTP host do carry a user's own app domains.
   - Five days in July 2019, during the summer holidays, before iOS 13 and Android 10 changed their TLS and DHCP
     behaviour. A model trained here would need retraining on every OS release. Half-day windows cannot test that.

4. Would I use it? Trust and distrust
   - I would use it as one signal in the inventory, aggregated per device. It would sit next to the DHCP option-55
     fingerprint, the MAC OUI and the plain-text User-Agent when it appears, much as the paper's Fig. 2 coverage
     argument runs per session.
   - What builds trust: the TCP/IP triple alone gives 0.93 session accuracy (shipped score 0.231 against 1.385 for
     the class shares), and the errors are mostly Mac OS against iOS, as the paper reports.
   - What breaks trust: no "other or unknown" output; a closed set that cannot raise the anomalies I care about;
     2019 fingerprints. Today Chrome shuffles the ClientHello extension order on every connection (since about
     Chrome 110, 2023), which is why JA4 sorts the list. Encrypted Client Hello also hides the SNI. The ordered
     extension string, shipped as a string feature, would not carry over to current traffic. For 2019 data it is
     faithful.

5. The metric (MET-1, MET-5 to MET-9, MET-17)
   - The declared metric is the fallback log_loss, weighted by session_weight = 1 / (the session's task flows in
     the half-day). The fallback is right: the paper reports accuracy, precision, recall and F1 side by side,
     micro-averaged, with no criterion and no costs (MET-5, MET-6, MET-7). Probabilities are what I want (MET-8).
   - The unit is right. Each session counts once, not by its traffic: one Windows session holds 578,764 flows, and
     sessions are 54% Android while flows are 39.5% Windows (MET-17).
   - The aggregation is not mine. MET-17's premise is that a unit's further rows are "repeats the source's protocol
     made". A session's flows are not repeats: they are independent evidence that I combine. My probe
     (session_decision.py, newest half-day 2019-07-16 12:00, own draw: train a random 1M
     earlier task flows, test all 1,951,652 task flows of the window in 8,348 sessions, untuned LightGBM, raw TLS
     fields as categories) gives:
       family        shipped(session-wtd)  session LL, mean log-p  session LL, mean p  session acc (mean p)
       class_shares        1.385                1.385                    1.385              0.079
       tcpip_only          0.231                0.228                    0.228              0.933
       tls_only            0.673                0.228                    0.489              0.888
       all                 0.268                0.165                    0.152              0.964
       all_shallow         0.175                0.144                    0.158              0.962
     Kendall tau against the shipped score: 1.0 for the unweighted per-flow score (as in the builder's probe), 0.8
     for the session verdict from the mean log-probability, and 0.6 from the mean probability. The shipped score
     punishes TLS-only models for the flows that carry no ClientHello. In my combined verdict those flows simply add
     nothing, so per session TLS-only ties TCP/IP. Likewise the untuned full model is third under the shipped score
     but best or second at the session level. Caveat: one window, five families, untuned models.
   - The metric I would choose is the log loss of each session's combined prediction (the mean of its flows'
     probabilities, one row per session and window, all sessions equal), with the session id as a scoring column
     and never a feature (MET-2), as a custom group metric with a reference implementation (MET-13), in the style of
     the mean_group_* metrics. If the library or the protocol cannot take that, the shipped session-weighted log
     loss is the closest row-level score. Its metric reason should then say that the actor aggregates flows and that
     the per-flow score ranks families differently from the per-device verdict.

GAPS, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Scored per flow while I decide per device from all its flows. The model ranking moves (tau 0.6 to 0.8; TLS-only
   0.673 shipped against 0.228 aggregated). Metric gap, MET-17 / MET-1.
2. Closed set without Linux, other or unknown. The devices a security team hunts are absent, and the model cannot
   abstain. USE-5, USE-8.
3. No OS version in the label, so the "outdated" part of the decision is out of reach. USE-5; the paper's Table II.
4. The label is already known on this network at connection (DHCP host name). The test devices stand in for
   unlabelled ones, a population that differs. USE-8, USE-9.
5. One network, five summer days in 2019. Fingerprints have changed since (Chrome extension shuffling, ECH, newer
   OS stacks). An era gap of the kind that alone stays direct (USE-8 cases); named for completeness.
6. The label-anomaly bullet's guess about the 141 Windows sessions with TTL 64 or less is contradicted by their SYN
   size, window and User-Agent (they look like real Windows hosts). This is a notes fix, not a task change.

WHAT A DOMAIN EXPERT WOULD CHANGE
- Score per device-window. Ship the session id as a scoring column with an aggregated log loss, or at least name
  the aggregation gap in the metric reason (gap 1).
- Correct the TTL anomaly bullet: 137 of 141 sessions are pure TTL 64 or less, with the Windows SYN 52 / window
  64240 pair and User-Agent code 68. The likely cause is a TTL changed on the host or the path, not a misleading
  host name.
- Optionally add an order-free view of the TLS lists (a sorted extension set, as in JA4), which modern
  fingerprinting uses. A feature-engineering choice, not required for the 2019 data.
- Name in fit_reason that no OS version is in the label (gap 3). It names the other gaps already.
- Not a change: keep the source IP and session id out of the features. Keep the SNI and HTTP host (they are in the
  clear at export, USE-6).

SOURCES
- Laštovička, Špaček, Velan, Čeleda, NOMS 2020:
  Sect. I (asset identification, unmanaged networks), IV (dataset), V.B (training on day 1, scoring per flow), V.C
  (DHCP host-name ground truth, caveat on Windows and Linux), VI.A (coverage per session), VI.B and Table III
  (micro-averaged accuracy, precision, recall, F1), Fig. 4 (Linux 1.48%, other 0.07%), Table II (no version in the
  ground truth).
- Zenodo 10.5281/zenodo.3461771; the group's later survey "Passive Operating System Fingerprinting Revisited",
  Computer Networks 2023 (https://www.ics.muni.cz/en/research/publications/2276417) and its flow dataset
  (https://zenodo.org/records/7635138).
- DHCP option-55 profiling in NAC and IPAM: https://blogs.manageengine.com/?p=100300,
  https://infoblox-docs.atlassian.net/wiki/x/1IpTAQ, https://tools.netsa.cert.org/yaf/yafdhcp.html
- Chrome extension-order shuffling and JA4: https://stamus-networks.com/blog/ja3-fingerprints-fade-browsers-embrace-tls-extension-randomization,
  https://www.peakhour.io/blog/overview-of-ja4-network-fingerprinting/
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: tls_os_fingerprinting_masaryk (target `os`, 5-class, temporal on `period`, 3 test windows)

VERDICT: Include with changes. The task is real and the data is genuine, the target is clean of leaks and the
temporal split is honest. But accuracy is close to the ceiling, the prepared table carries columns that should not
be features (flow_start, period, four near-empty SSH columns), and the per-window row budget and SYN-only filter
should be stated.

WHAT THE TASK IS
Passive OS fingerprinting. A network operator (here, Masaryk University's campus Eduroam) watches flow records
(IPFIX with TCP SYN and TLS ClientHello fields) and labels the OS of each client device. They use it for asset
inventory, BYOD policy, and spotting outdated or unexpected devices, without installing anything on the device.
The prediction is made per flow, once the flow record is exported. This is a real, published use case (NOMS 2020,
Lastovicka et al.). Source: Zenodo 10.5281/zenodo.3461771, CC BY 4.0, flows from 2019-07-12 to 2019-07-16. Per the
record, the label was "derived from DHCP logs" via the RADIUS session.

WHAT I DID
- Read data.parquet (200k-row sample), task.md, and the Zenodo record. The paper and slide PDFs at is.muni.cz were
  behind a JS bot wall, so I could not read the paper text.
- Downloaded the public raw archive (flows_dataset_anonymized.zip, 120 hourly CSVs, 18,709,103 lines) and compared
  it with the prepared sample.
- Ran a LightGBM model on the expanding-window temporal split, plus two lookup-table baselines.

CONCERNS, MOST TO LEAST SERIOUS

1. Accuracy is near the ceiling, so the useful spread lies in a few small classes.
   On the 200k sample (train on all earlier periods, test on each of the last three windows):
     window      n_test  majority  lookup(ttl,syn_size,win)  lookup(+TLS fp)  LightGBM acc / bal.acc / logloss
     07-15 12h   40,029  0.375     0.912                     0.937            0.957 / 0.782 / 0.148
     07-16 00h   39,905  0.233     0.905                     0.935            0.961 / 0.813 / 0.125
     07-16 12h   40,059  0.376     0.896                     0.927            0.957 / 0.836 / 0.126
   - syn_ttl alone nearly separates Windows: 126 gives 68,989 Windows, 150 Mac OS, 525 Windows Phone and 0 others.
   - syn_size 60 vs 64 separates Android from Apple (75,001 Android at 60; 15,329 Mac OS and 34,363 iOS at 64).
   - Nearly all remaining errors are iOS vs Mac OS (1,004 Mac OS predicted as iOS, 340 iOS predicted as Mac OS) and
     Windows Phone (0.26% of rows, 67 of 123 right).
   - With 2.5M rows, plain accuracy will saturate and models will barely separate.
   Change: score with log loss or balanced accuracy / macro-F1, not plain accuracy. Expect small gaps between models
   and say so.

2. The label comes from a DHCP-based OS heuristic, not from the device. It is a closed set of 5 classes and is
   somewhat noisy.
   - Zenodo says only: "operating system ... as derived from DHCP logs". It does not explain how.
   - Only Windows, Android, iOS, Mac OS and Windows Phone exist. There is no Linux, ChromeOS or other class anywhere
     in the raw data (13,309,494 SYN rows), yet a real deployment would see them.
   - Signs of label noise:
     - the only OpenSSH Ubuntu SSH flow is labelled Windows;
     - 3,568 "Windows" rows have TTL 62, which looks like Linux/Apple;
     - 253 "Android" rows have TTL 125 and 229 have window 64240, a Windows-like stack.
   - 2.6% of fingerprint groups (all fields except src_port and duration) carry more than one label.
   - Each session has exactly one label (checked on the raw data), so the noise sits at device level.
   This sets a floor of a few percent of error that no model can remove. It is acceptable but should be documented.
   Change: note in the task card that the label is DHCP-derived and the class set is closed.

3. Rows are flows, heavily clustered by device/session. This does not leak across the split, but the effective
   sample size is much smaller than the row count.
   - The raw data has 44,925 RADIUS sessions with a median of 38 flows each. The top 1% of sessions hold 32% of the
     SYN flows.
   - In the sample, 77% of rows repeat an earlier (fingerprint, label) combination.
   - Session IDs and IPs were removed, which is good: they would be identity leaks.
   - Overlap with training data: only 12-21% of test-window rows (6-12% of test sessions) come from a RADIUS session
     already seen in training. Devices can get new sessions, though, so overlap by device is probably higher, and I
     could not measure it (IPs are Crypto-PAn anonymised and dropped here).
   For a campus deploying a fingerprinting model, seeing the same devices again is realistic, so I would keep the
   temporal split.
   Exact copies (all columns except flow_start) are only 0.25% of rows.

4. Columns that should not be features, or are useless.
   - flow_start (raw datetime) and period are both in the table. Under a temporal split, flow_start can only
     extrapolate, and hour of day carries class-prior shift: Windows share is 0.14 at 06h and 0.56 at 21h.
     Drop both from the features, or at most derive hour/weekday deliberately.
   - The ssh_client_application, ssh_client_encryption, ssh_client_mac and ssh_client_compression columns are 4
     non-null values out of 200,000. Drop them.
   - tls_sni_length duplicates information in tls_sni. That is harmless.
   - http_host is 93% missing. That is fine, since it is structural (only port-80 flows have it).
   - flow_duration_s and the flow end are only known when the flow ends. That is fine for exported flow records,
     but it is not a "first packet" fingerprint. Fine as is.

5. The row budget distorts the time profile, and one stray period exists.
   - The prepared 2.5M rows sample the three test windows at about 500k each: 40,029, 39,905 and 40,059 in the 200k
     sample, i.e. 24%, 46% and 26% of the raw SYN rows. The eight training periods get about 1.0M rows (about 12%).
   - Within a window the sampling is uniform (hour-of-day ratios between sample and raw are 0.87-1.08), so the
     conditional distribution is not biased. But the train/test balance does not follow raw traffic, and the
     07-16 00h night window is oversampled about 4x relative to 07-15 00h.
   - Period 2019-07-11 12:00 has 88 rows (raw 9,263): flows from 23:51 onward, padding before the official start.
     Drop it or merge it into the next period.
   - The test windows have different class priors: Windows is 37%, 23% and 34% across the three windows, and
     40-60% on weekend evenings in training.
   Change: document the per-window caps. Consider sampling the test windows at the same rate as training.

6. Undocumented row filter.
   - The raw data has 18.7M flows. Only 13.31M have SYN fields (the rest started before capture or have no
     handshake). All 2.5M prepared rows have syn_size, so the preparer kept SYN-bearing flows only.
   - This is sensible because the TCP features need it, but task.md does not say so.
   - All raw SYN rows are labelled.
   Change: state the filter.

7. Encoding of list-valued TLS fields.
   - The TLS fields are comma-separated hex lists. The preparer decoded the byte-swapped raw hex correctly: I checked
     cipher suites against the raw values, and EC point formats 16777215 maps to "none" and 66303 to "0,1,2".
   - The raw cipher-suite field is truncated at 8 suites; that limit comes from the source exporter. Extension
     types and lengths go up to 19 entries.
   - The dtypes are inconsistent: tls_cipher_suites and tls_elliptic_curves are category, while
     tls_extension_types and tls_extension_lengths are string. tls_extension_lengths has 6,265 levels in 200k rows
     and includes SNI-length/padding values that act as quasi-identifiers.
   As a single high-cardinality categorical this is fine for a benchmark (it is how JA3-style fingerprints are
   used). Making all list fields the same dtype would be cleaner.

WHAT IS FINE
- The target is right: the raw "Ground Truth OS" column, with the same five classes and the same proportions.
- The User-Agent OS columns (HTTP UA OS / MAJ / MIN / BLD), which would be partial label leaks, are correctly
  removed, and so are Session ID and IPs.
- The values are plausible: TTL 62/126 are 64/128 minus two hops; windows 65535/64240/14600; real SNIs; ephemeral
  src_port ranges per OS.
- The data is real measured traffic, not synthetic.
- The test set is large enough for stable scores.

WHAT I COULD NOT CHECK
- The paper's full text (is.muni.cz bot wall), so I do not know exactly how the DHCP-derived label was made or its
  measured error rate.
- Device identity across periods (IPs dropped/anonymised; sessions are not devices), so the true device overlap
  between train and test is unknown.
- Behaviour at the full 2.5M-row scale (I only trained on the 200k sample).
- Whether the preparer's per-window sampling is exactly random. It looks uniform by hour, but the seed and code are
  not available to me.
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT - tls_os_fingerprinting_masaryk (target os, 5 classes, weighted log_loss with session_weight, 3 temporal 12 h test windows)

Verdict: no exploit beat the honest model by more than the seed/noise spread (about +-0.003). The flaws that matter work against honest models: the absolute time columns, and training that ignores the session weighting.

LightGBM was untuned (100 rounds, 4 threads), fit on all 1M training rows per split. Nothing was subsampled.

HONEST MODELS (weighted log loss, r0 / r1 / r2, mean)
- Specified baseline, untuned LightGBM on features() including flow_start and period (baseline.py): 0.641 / 0.324 / 2.792, mean 1.252
- Same model with flow_start and period dropped (baseline.py): 0.159 / 0.192 / 0.207, mean 0.186. A rerun gave 0.159 / 0.192 / 0.262, so one split moves by 0.05 from LightGBM thread nondeterminism alone.
- No time columns, trained with session_weight as the sample weight (honest2.py, "notime_sw"): 0.0984 / 0.0886 / 0.1021, mean 0.0963. This is the reference for the exploits below.
- Noise for notime_sw, from three extra fits with a random column (noise_and_more.py noise): r0 0.0984-0.1007, r1 0.0886-0.0934, r2 0.1012-0.1036, mean 0.0963-0.0981.

EXPLOITS RANKED BY GAIN (against notime_sw, mean 0.0963)
| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Rebuild devices by source-port chains (same TTL, next port within 16, within 30 s). Feed the chain's flow count up to this flow as a feature. | chainfeat.py causal | 0.0963 | 0.0951 | -0.002 / -0.001 / -0.0005 | Yes, roughly: a live probe sees earlier flows | none needed (noise) |
| 2 | Pool the honest predictions over each test-window chain, later flows included (half log-prob mix) | smooth.py | 0.0963 | 0.0963 | -0.002 / +0.004 / -0.002 | No (uses later flows) | none needed (noise) |
| 3 | Same chain, but the whole chain's flow count as a feature (later flows included) | chainfeat.py full | 0.0963 | 0.0967 | -0.001 / +0.003 / -0.001 | No | none needed |
| 4 | session_weight (scoring column) as a feature: -log w = session flow count | noise_and_more.py swfeat | 0.0963 | 0.0972 | +0.002 / +0.001 / -0.000 | No | keep test-row weights hidden (no gain anyway) |
| 5 | Re-estimate class priors on the test window (Saerens EM) | prior_em.py | 0.0963 | 0.1194 | worse on all splits | No | none needed |
Even the oracle test prior gives 0.0960, a gain of only 0.0003, so the class mix gives nothing away.

FLAWS THAT HURT AN HONEST MODEL
| # | What is wrong | Honest choice | Score as shipped | Honest score | Fix |
|---|---|---|---|---|---|
| A | flow_start and period are in features(). Trees split on absolute time, which memorises when devices were present, and every test time lies past the training range. | Drop both columns | 1.252 (0.641 / 0.324 / 2.792) unweighted; 0.114 (0.106 / 0.115 / 0.120) session-weighted | 0.186 unweighted; 0.0963 weighted | Drop flow_start and period from the features; keep period only as the split key. An hour-of-day feature hurt too: 0.275 vs 0.186 (honest2.py notime_hour). |
| B | The metric weights each RADIUS session equally (w = 1/session flow count). The table is dominated by huge sessions, mostly Windows, while the loss sits in small Apple and Android sessions. An unweighted fit optimises the wrong mix. | Train with session_weight as the sample weight | 0.186 | 0.0963 (-0.06 / -0.10 / -0.10) | Declare session_weight as the training sample weight (task.json sample_weight is null now), computed from training-period flows only. The count n currently covers the whole source session, test-window flows included. A mild piece of future information, used here only to weight training rows. |
| C | The shipped training sets drop part of the past: r0 trains on 1M of the 2M earlier rows, r1 on 1M of 1.5M. | Train on every row before the test window (train_rows.py allpast) | 0.0963 | 0.0930 (-0.005 / -0.005 / 0) | Near the noise edge. Either ship the full history or say the subsample is deliberate. |
Training on only the last 24 h is worse: 0.115 (train_rows.py recent24h).

MECHANISMS
A. The test windows are the three newest 12 h periods (500k rows each, capped). With flow_start as a feature, every test row lands in the leaf for the latest training times. In r2 that collapses the log loss to 2.79. Dropping the two time columns cuts the mean from 1.25 to 0.19. Session weighting softens the damage (0.114 with time vs 0.096 without) but does not remove it.
B. Session size and class go together. Sessions with 1-5 flows are about 50% Android and about 40% iOS; sessions with more than 1000 flows are 58% Windows. 79% of the test weight comes from sessions with 100 or more rows in the window, yet each one counts once. Per-class weighted loss for r0 is Mac OS 0.050, iOS 0.036, Windows Phone 0.007, Android 0.005, Windows 0.0015, so Apple-vs-Apple confusion carries the remaining loss.
C. The shipped training sets are subsamples of the earlier rows. The full history gives about 0.005 on r0 and r1 and nothing on r2, where the training set already holds every earlier row.

ATTACKS THAT FOUND NOTHING
- Row order. Rows are sorted by period and shuffled within each period: flow_start against position correlates at about 0.00. Next-row label agreement is 0.3359 against 0.3361 expected. Class rates are flat across the position quintiles of each period.
- Formats. A model on format-only features (ms digits, duration digits, whole-number durations, port parity, missing count) scores 1.066, against 1.082 for the prior alone (noise_and_more.py format). The small gain is protocol missingness: no TLS, no HTTP, mostly Windows. That is real signal. Odd duration last digits for Windows (0.114 vs 0.085) and trailing-dot SNIs for Mac OS (2%) are client or exporter behaviour, not preparation artefacts. 18,010 rows have tls_sni_length 0 with tls_sni missing, and 1,165 SNIs do not match their stated length; both are in the source.
- Exact copies across the split (copies.py). 6.4% of r0 test rows (5.3% of r1) have an identical training row once the time columns are ignored. The copy's majority label matches only 93% of the time, below the model's accuracy. Matching on ports and TCP fields only finds a copy for 86% of rows, with 88% agreement. Nothing is gained either way.
- Continuation records of long connections (300 s active timeout; same ports, next record starting at start + duration): about 4,300 pairs in the whole table, label agreement 0.81-0.93 (explore4.py). The 2.5M kit rows are a subsample of a source of about 18.7M flows, which breaks the chains.
- Port chains reaching back into training: only 0.3% of test rows join a chain that holds training rows (chain_check.py). Chains are short (largest about 500-3,600 flows), and label purity is 0.987 at DP=16/DT=30 and 0.962 at DP=32/DT=60. Even an exploit that may use later flows cannot recover the device behind a test flow.
- Train-vs-test classifier (adversarial.py, r0): AUC 0.68, driven by flow_duration_s, SNI, extension lengths and dst_port. That is the weekend traffic mix (13-14 July: short Windows-heavy flows), not a leak.
- No public competition, leak thread or "magic feature" exists for this dataset. It is a Zenodo release with the NOMS 2020 paper; an arXiv paper (2502.09084) applies tabular transformers to it.
- Looking up rows in the published source file: it holds the session ID, the anonymised source IP and user-agent OS fields, so matching on flow_start and ports would very likely recover them. I did not download the 700 MB archive to check. Not ranked.

COULD NOT CHECK
- The NOMS paper PDF sits behind a bot-check page on is.muni.cz, so I could not read the authors' exact labelling and filtering.
- Device identity across 12 h cannot be rebuilt from the kit's columns (no IP, no session ID). 94% of the test weight comes from sessions also present in training, so a leaked device key would be worth a great deal. No such key is in the kit.
- To diagnose the loss (lossdiag.py, explore3.py), I grouped sessions by (round(1/session_weight), os). That uses the label and the scoring column, so it was never used as a feature.

Sources: https://zenodo.org/records/3461771 ; https://doi.org/10.1109/NOMS47738.2020.9110319 ; https://arxiv.org/abs/2502.09084
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER REPORT: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-08

Read: principles.md, metrics.md (MET-14 to MET-17 and Cases), splits.md (SPLIT-13, -14, -19, -21, -23, -26, Cases),
leak_checks.md (LEAK-10, Mechanisms), use_case.md (USE-5 to USE-8, Cases), cleaning_features.md (CLEAN-3), provenance.md
(PROV-4), definitions.md (UnitWeight); the definition, the record, builder_report.md, the probes, the domain
practitioner's report and register.json (5,159 decisions, 34 flags). All rule files from the df-large worktree.
New measurement: dst_ip_specificity.py (.log), on the 13,309,494 task flows of the raw parquet.

SUMMARY
| # | Decision | Verdict |
|---|---|---|
| 1 | Session weight in the score (MET-17) | consistent with the weighted MET-17 cases (pancreatic, dementia, bacteria_id_raman); the rule's wording ("repeats the source's protocol made") does not cover rows the device's own traffic generates, a reason is stated (the inventory decides per device) |
| 1b | No `unit_weight`, session key dropped | departs from MET-17's declaration clause and the curator's boreal call of 2026-11-08; the reason (a library gap with a row budget) is only in the builder report, not in the definition -> prompt A |
| 2 | User-Agent OS fields dropped (LEAK-10) | consistent (2_month_survival_rate_prediction, sdss_17 `redshift`, kickstarter `staff_pick`) |
| 3 | Source address and session id dropped (CLEAN-3) | consistent (ugr16 addresses, data_fusion_2026_guardian ids) |
| 4 | Destination address dropped (CLEAN-3, a Should) | departs from the kept shared-entity codes (lt_vehicle, kick, amazon_employee_access); the stated reason holds for 77.6% of the task flows only -> prompt B |
| 5 | Half-day windows against the paper's day-1 split | consistent: SPLIT-14 (Must) over SPLIT-19 (Should); california_house_prices_2020, wisconsin amendment does not reach |
| 6 | Network precedents (cesnet_os, ctu_13, ugr16) | consistent |
| 7 | No Linux / other class (USE-5) | consistent (sarcoma closed set, diabetes_3), approximate fit with the gap named |
No drift by the same curator and no third exception of one kind is created by this definition.

----------------------------------------------------------------------------------------------------------------------
1. SESSION WEIGHT IN THE SCORE (MET-17, Should; MET-15; MET-11)

What the definition does: fallback log loss weighted by `session_weight` = 1 / (task flows of the session in the
half-day), scoring only, no sample_weight; the reason is in the metric's reason ("the inventory decides per device").

Precedents (all Lennart, 2026-11-08; metrics.md Cases rows 354-359; records under curation/records/):
- Weighted, rows read one by one, label the unit's: pancreatic_cancer_mouse_detection (`mouse_weight`, 1-6 samples
  per mouse, "each sample is still read on its own"), dementia_prediction (`person_weight`, 1-5 visits, "follow-up
  visits stay scored as if each were a first visit"; first visits only rejected, tau 0.87), bacteria_id_raman
  (`isolate_weight`, 100 or 400 spectra; same batch), boreal_postfire_lichen_biomass, superconductivity.
- Unweighted, each row a decision: asp_potassco_classification (an instance per selector run), 
  video_transcoding_time_prediction (a job per scheduler placement).

Comparison:
- Which branch. MET-17 weights when "the actor decides once per unit and the unit's further rows are repeats the
  source's protocol made"; it scores per row "when each row is a decision of its own". A session's flows are neither:
  their number is set by the device's own traffic (1 to 578,764 task flows; Windows 39.5% of flows, 7.0% of sessions),
  not by a protocol. The definition's actor (an inventory) decides per device, so it takes the weighted branch. The
  rule's Why ("a unit ... would otherwise count five times in a decision the actor makes once") applies with more force
  here than in the protocol cases, and the class-linked imbalance is the fact that sets it apart from asp_potassco and
  video_transcoding. Verdict: consistent with the weighted cases; the curator may want MET-17's condition to read
  "repeats the protocol made, or rows the unit's own activity generated" (an amendment, not an exception: a first
  case, no third exception).
- Wording inside the definition: `use_case` says the team "labels each connection with the operating system" and
  `question` asks per connection; read literally that is the per-row branch (each flow a labelling decision, the
  asp_potassco / video_transcoding shape, and the domain practitioner's SIEM tagging, USE-9). Only `fit_reason` and the
  metric reason say the inventory decides per device. Whichever branch the curator takes, `use_case` should name that
  decision; now the text supports both.
- The domain practitioner's alternative (score each session's combined prediction, one row per session and window)
  changes what one prediction is. SPLIT-23 (Must) lets the source's use case, cited, decide that; the paper scores per
  flow (Sect. VI.B) and only counts coverage per session (Sect. VI.A). The precedents with the same structure kept
  the row as the prediction and weighted it (pancreatic, dementia), and MET-17 says "The weight changes how much a
  prediction counts, never what one prediction is". An aggregated per-session score would depart from both
  precedents and needs a cited per-device use case of the source; the practitioner's measured fact (tau 0.6 to 0.8
  against the session verdict, one window, untuned) is a ranking difference, which no precedent has used to change
  the prediction unit (protein_model_quality_rf_pcp and huesken changed it on the source's use case, SPLIT-23).
- Notes: every weighted MET-17 case records in its notes how far the weight moves the ranking (dementia tau 0.94,
  pancreatic 0.66, bacteria 0.91, superconductivity 0.98). The builder measured tau 1.0 on all 3 windows
  (weight_ranking.json) but `curation_comments` does not state it. Small notes gap; add it.

1b. UNIT WEIGHT NOT DECLARED, UNIT COLUMN DROPPED (MET-17 declaration clause; definitions.md "unit_weight")
- MET-17: "the task declares it as its `unit_weight` (the weight column and the unit's column), so downstream tools
  weight their validation loss alike". definitions.md: "the unit is a column `_clean` keeps ..., metadata, never a
  feature". The definition drops `session_id` and declares no `UnitWeight`.
- Every weighted MET-17 case declares it: boreal (curator call 2026-11-08: "make sure to somehow add it to the metadata
  that this kind of group type ... exists and can be read by downstream tools"; `plot` kept as metadata), dementia
  (`UnitWeight(column="person_weight", unit="Subject ID")`), pancreatic, superconductivity, bacteria_id_raman.
- Reason given: builder_report.md, library gap 2 (with a row budget the test window keeps a sample, the weights of a
  unit sum below 1 and `task_unit_weight_not_one_per_unit` errors on 43,523 of 43,906 units). That fact is real and
  sets the case apart from the five precedents (none has a row budget), but it is in the run log, not in the
  definition or a REVIEW.md, and it would not explain dropping the unit column: with the unit declared, the unit
  would be the (session, half-day) pair, which never crosses a window (test = one half-day, train = earlier ones).
- Effect: `validation_weight(container)` still returns `session_weight` (it reads the metric's weight), but a
  downstream tool cannot keep a session's flows on one side of its validation split, the reason MET-17 asks for the
  unit (the curator's boreal call). Verdict: departs, reason stated outside the definition. Prompt A below.

----------------------------------------------------------------------------------------------------------------------
2. USER-AGENT OS FIELDS DROPPED (LEAK-10, Must)
- Fact: the probe's code parsed from a plain-text User-Agent names the label's majority class for 96.5% of the 4.1% of
  task flows where it names an OS; the paper's User-Agent method scores 0.9764 (Table III) and its ML methods use the
  User-Agent as their training label (Sect. V.B).
- Precedents: 2_month_survival_rate_prediction (USE-6 case, 2026-10-26, Lennart): the physicians' estimates are not
  inputs because the source's task is an estimate set beside them as its comparator; sdss_17 `redshift` (LEAK-10:
  dropped "for the task we frame"); kickstarter `staff_pick` (tension row: dropped once the task was "predict at
  launch"). The counter-precedent is breast_cancer_prediction (the radiologist's BI-RADS reading is the actor's own
  input); the domain practitioner says an operator would use a User-Agent where it appears, which points that way,
  but the source's task places the User-Agent as comparator and label, the fact that decided 2_month_survival.
- Verdict: consistent. One wording point: the notes justify the drop by "the OS from encrypted traffic", but the HTTP
  host, also readable only in plain-text HTTP, stays (`use_case`: "from fields that stay readable when the traffic is
  encrypted"). The drop rests on "another encoding of the target / the source's comparator and training label", which
  the HTTP host is not (alone 0.533 macro ROC AUC); the use_case sentence should not claim encrypted-only fields while
  the HTTP host ships.

----------------------------------------------------------------------------------------------------------------------
3. SOURCE ADDRESS AND SESSION ID DROPPED (CLEAN-3, Should)
- Facts: the source address names the device (alone 0.921 macro ROC AUC), is reused across sessions and devices (1,724
  of 6,165 addresses carry several OS labels), and is the key through which the authors joined the DHCP label (address
  and time to the lease's host name, Sect. IV).
- Precedents: ugr16_isp_netflow_intrusion_1m (same batch, curator CC 2026-11-08 on its classes; the definition drops
  both addresses because the label was assigned on them); data_fusion_2026_guardian_1m (same batch: `customer_id`,
  `session_id` dropped as identifiers); ieee_fraud_detection `TransactionID` (CLEAN-3 case, 2026-10-31).
- Verdict: consistent. The session id then serves only the weight (see 1b on keeping it as metadata).

----------------------------------------------------------------------------------------------------------------------
4. DESTINATION ADDRESS DROPPED (CLEAN-3, Should; USE-6, Must, in the background)
- CLEAN-3 drops "uninformative identifiers" and keeps "an identifier that carries meaning". The destination is a
  shared entity (138,681 servers), informative (builder probe: session-weighted log loss 0.1757 without, 0.1630 with it
  as a category, 0.1675 with its /16 prefix; shallow LightGBM, one draw, no string columns), and a monitor reads it in
  the clear at the prediction point (USE-6: "Anything known at the prediction point is a legitimate input").
- Precedents for opaque codes of shared entities kept as categories: lt_vehicle_loan_default_prediction (`branch_id`,
  `supplier_id`, `Employee_code_ID`; CLEAN-3 assessment 2026-10-23, the codes' kept rates in the SPLIT-9 case of
  2026-11-05, Lennart), kick (`BYRNO`, `VNZIP1` as categories), amazon_employee_access (`RESOURCE`, manager and role
  ids). No precedent drops an informative shared-entity id for being opaque.
- The stated reasons and what the data says (new measurement, dst_ip_specificity.log):
  * "the server's name is in the clear in the SNI or HTTP host": 2,983,583 task flows (22.4%) have neither, so for them
    the address is the only identity of the server (3,795,490, 28.5%, have no parsed ClientHello).
  * "an opaque id under Crypto-PAn": Crypto-PAn is prefix-preserving, so the /16 prefix keeps network structure (the
    builder's option (c)); lt_vehicle's codes are as opaque.
  * A fact that could set it apart: 79,163 of the 138,681 addresses are reached by one session only (3.1% of the task
    flows; 5.3% go to an address of at most 3 sessions; 8.3% of the flows without a server name). Those addresses name
    the device's own peers (a home server, a VPN endpoint), the reason the source address goes. The other 96.9% of the
    flows go to shared servers.
  * Width (138,681 values) is no reason (CLEAN-22; tension row "Width against model limits", coad).
- Verdict: departs, with a stated reason that holds for 77.6% of the flows and an untested redundancy (the gain was
  measured without the SNI and host). Not a Must question either way. Prompt B below; the builder's draft issue 2
  covers the same call and can take it as its Consistency bullet.

----------------------------------------------------------------------------------------------------------------------
5. HALF-DAY WINDOWS AGAINST THE PAPER'S DAY-1 SPLIT (SPLIT-14 Must; SPLIT-19 Should; SPLIT-12, SPLIT-21)
- The paper trains on day 1 and tests on days 2-5 (18.8% of the task flows in training), below SPLIT-14's 50% floor;
  daily windows give 35.6% for the third newest day, below even the 40% that the 2026-11-08 amendment allows for one
  older window (wisconsin_local_government_property_insurance_fund). Half-days give 61.7 / 77.2 / 85.3%.
- Ranking: SPLIT-14 is a Must and SPLIT-19 a Should in the same part, so the Must wins (principles.md, "Conflicts").
  Precedents: california_house_prices_2020 (SPLIT-14 case, 2026-10-21: the 25% window replaced, windows on 50/67/83%);
  medical_facility_operational_data (SPLIT-12/19 case, 2026-11-05: the source's horizon followed where the floor
  allows it; here it does not).
- SPLIT-21: the windows were set from training shares, not from scores. The refit cadence ("twice a day is a
  plausible cadence") is an assumption, as ugr16's "refit every few days" is; SPLIT-12's family call (2026-10-21)
  lets each task keep its own cadence.
- Verdict: consistent. Not an exception to SPLIT-19: the departure is forced by a Must and the notes say so.

----------------------------------------------------------------------------------------------------------------------
6. NETWORK TRAFFIC PRECEDENTS
- cesnet_os_fingerprinting_2024: CC 2026-11-08 (Lennart) "kept for later (`TBD -> Yes`, priority 3) ...;
  tls_os_fingerprinting_masaryk, the same task with sessions, times and DHCP labels, is accepted"; principles.md
  tension row "Same task, another source" (tls_os over cesnet_os, one enters). The definition uses the three facts the
  curator chose it for (times: the temporal split; sessions: the weight; DHCP labels: the target). Consistent. Using
  the session only as a weight (not as a group) also matches the record's screening ("the session ID as a group,
  never a feature"), with the temporal regime chosen over grouping (SPLIT-3, one regime; SPLIT-13, devices recur as
  for the monitor).
- ctu_13 and ctu_sme_11: `No`, AHDS (SEL-16), 2026-11-04 (Lennart): staged infections of the lab's VMs, labels by host,
  and a shallow two-port rule at ROC AUC 0.852 against LightGBM's 0.858 (Myunghwan, 2026-10-27). ugr16: `Yes` with the
  real classes only, 2026-11-08 (Lennart: "no staged traffic in the target"). This dataset: real users' devices on
  campus Wi-Fi, labels from the DHCP logs, nothing staged: SEL-16 holds by the fact that set ugr16 apart. Headroom:
  the best single feature (`syn_size`) scores 0.270 against 0.131 for a random forest and 1.421 for the class shares
  (TP-4 not met), unlike ctu_13's rule. Consistent. The register's SEL-16 drift flag (exclude 2026-11-04, keep
  2026-11-08) is explained by ugr16's CC line itself; this dataset adds nothing to it.

----------------------------------------------------------------------------------------------------------------------
7. NO LINUX OR OTHER CLASS (USE-5 Must; USE-8)
- Facts: five classes; the paper's Fig. 4 gives Linux 1.48% and other 0.07%, and its class shares do not match the
  release's flow shares; the authors do not say why. `fit="approximate"` names "no Linux or other systems".
- Precedents: sarcoma (USE-8 case, 2026-10-21, Lennart: approximate for a closed set of types); diabetes_3 (USE-5,
  amended 2026-10-21: an undocumented label construction ships approximate with a note). The register's USE-5 flag
  (diabetes_3 and chicago_traffic_crashes kept, xente_fraud_detection_challenge out) separates on whether the label is
  another quantity or follows a rule on a shipped input: here the label is set from the DHCP log at connection,
  independent of every shipped input, so the keep side applies; corporate_credit_rating (17% of checkable labels
  wrong) has no counterpart here.
- Label noise kept as labelled (141 Windows sessions with a 64-TTL stack): follows the tension row "A better version
  against our own fix" (eryhemato): a relabelling of our own does not replace the source's label. The domain
  practitioner's evidence (SYN 52 / window 64240 and User-Agent code 68 in 103 of the 141) contradicts the notes' guess
  that host names misled the labelling; a notes fix for the claim auditor, not a precedent question.
- Verdict: consistent.

Also checked, consistent: USE-7 row filter (flows without SYN fields dropped; bias_correction, nyc/pkdd 2026-10-26);
CLEAN-5 (`ssh_client_version` constant); CLEAN-22 (four SSH fields kept on 186-187 flows); LEAK-18 (0.7% exact copies
across the split, same labels, kept).

======================================================================================================================
DRAFTED TURNS FOR THE CURATOR (issue shape of review_file_format.md)

PROMPT A (for the builder's issue 1, or as its own issue)

**Consistency check (AI, 2026-11-08):** Should the session key stay in the frame as metadata and the session weight
be declared as the task's unit weight, as for every other one-vote-per-unit score?
- **Problem:**
  - The score counts each session once per half-day, but the definition declares no unit weight and drops the session
    id, so a downstream tool cannot tell which flows form one unit.
  - On boreal_postfire_lichen_biomass you asked that "this kind of group type ... exists and can be read by downstream
    tools", and dementia, pancreatic, superconductivity and bacteria_id_raman declare it.
  - The reason here, a row budget that samples each test window so a unit's weights no longer sum to 1, is written only
    in the run's builder report.
- **Consistency:** the five precedents have no row budget, so the sampling is a real distinguishing fact for the
  check, but not for dropping the unit column; with the unit taken as the session within its half-day, no unit spans
  a window[^met17][^bor].
- **Options:**

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Declare it once the library takes a row budget | keep a session-and-half-day key as metadata, declare the unit weight, and relax the sum-to-1 check for sampled windows (the builder's proposed change) | like every other unit-weighted task; downstream validation keeps a session on one side | a small library change before this ships |
| b | Ship as is, with a note (implemented) | weight in the score only, no unit declared, the library gap named in the notes | no library change now | the only unit-weighted task whose unit downstream tools cannot read; departs from the boreal call |
| c | Keep the key, declare nothing yet | keep the key as metadata and name it in the weight's description until the library is fixed | the information ships now | a second convention for the same thing |

- **Recommendation:** (a): the fact that sets this case apart concerns a check, not the declaration.
- **Decision:** a, b or c?

[^met17]: MET-17 (Should; 2026-11-08, Lennart): "the task declares it as its `unit_weight` (the weight column and the
  unit's column), so downstream tools weight their validation loss alike"; definitions.md, `unit_weight`: "the unit
  is a column `_clean` keeps ..., metadata, never a feature".
[^bor]: boreal_postfire_lichen_biomass, CC (2026-11-08, Lennart), curation/records/boreal_postfire_lichen_biomass.md;
  dementia_prediction, pancreatic_cancer_mouse_detection, superconductivity, bacteria_id_raman definitions.

PROMPT B (for the builder's issue 2)

**Consistency check (AI, 2026-11-08):** What sets the destination address apart from the branch, supplier, buyer and
resource codes that other datasets keep as categories?
- **Problem:**
  - The destination address is dropped as an opaque id whose server name the SNI or HTTP host already carries, but
    22.4% of the task flows (2,983,583) have neither, so for them it is the only trace of the server.
  - Other datasets keep opaque codes of shared entities as categories (lt_vehicle_loan_default_prediction's branch,
    supplier and employee codes; kick's buyer and ZIP; amazon_employee_access's resource), and a monitor reads the
    address in the clear when it labels a flow.
  - A fact that could set it apart: 79,163 of the 138,681 addresses are reached by a single session (3.1% of the
    flows); they name the device's own peers, as the dropped source address names the device.
- **Experiments:** shallow LightGBM, session-weighted log loss on one draw of the shipped windows without the string
  columns: 0.1757 without the address, 0.1630 with it, 0.1675 with its /16 prefix (Crypto-PAn keeps prefixes); not
  yet measured with the SNI and host present[^c3].
- **Options:**

| | Option | What it does | Pro | Con |
|---|---|---|---|---|
| a | Drop it, recorded as an exception (implemented) | the address stays out; the exception names the single-session addresses as device identity and the redundancy on 77.6% of the flows | no device trace through rare peers; nothing to rebuild | departs from the kept shared-entity codes; loses the only server trace on 22.4% of the flows |
| b | Treat it like the other shared-entity codes | ship the address as a category, the addresses of a single session merged into one level | follows lt_vehicle, kick and amazon; what a monitor sees | 59,518 levels remain; a stable server id from five days that will not carry to another network |
| c | Ship the /16 prefix | the Crypto-PAn prefix as a category, the full address dropped | keeps the network (provider, CDN), most of the measured gain; few levels | a construction of ours |
| d | Change the rule | amend CLEAN-3 so an anonymised network address leaves as an identifier | one rule for every flow dataset (ugr16 drops both) | ugr16 dropped its addresses for another reason (the label was assigned on them) |

- **Recommendation:** (c), measured first with the SNI and host in the features; (a) if the gain then vanishes, with
  the exception written down.
- **Decision:** a, b, c or d?

[^c3]: CLEAN-3 (Should): "Drop uninformative identifiers ... Keep an identifier that carries meaning"; USE-6 (Must):
  "Anything known at the prediction point is a legitimate input"; lt_vehicle_loan_default_prediction (CLEAN-3
  assessment 2026-10-23; SPLIT-9 case 2026-11-05, Lennart).
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE, OPENING BRIEF: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-09

Position: ship as defined. The changes below need no decision (text, typing, notes). The two weighing calls stay with
the curator: the score's unit (issue 1) and the destination address (issue 2). Neither is a reason to hold the dataset.
Sources: the seven phase-A reports in this folder, builder_report.md, dataset.py, principles.md, metrics.md (MET-15,
MET-17).

1. Validity holds on every Must, P1 to P5, and was tested hard (rank P1-P5, Must).
   Evidence: the claim auditor tested 41 claims plus the metric and 4 implied claims. Every count, decoding and
   provenance claim holds: 18,708,983 flows as in the paper, md5 and CC BY 4.0 from Zenodo, and no refutation on
   P1-P5. The leak is fixed (LEAK-10, Must). The User-Agent OS fields agree with the label on 96.5% of the 4.1% of
   flows that carry them, so they are dropped. This follows 2_month_survival, sdss_17 and kickstarter (precedent
   checker). The column auditor found no other leak. No host-name pattern appears in the SNI or HTTP host, and the
   missing indicators score 0.532. The split is honest. SPLIT-14 (Must) beats SPLIT-19 (Should): half-days train on
   61.7/77.2/85.3%, against 18.8% for the paper's day-1 split. Recurring sessions add 0.0014 to the score (split
   auditor B-A), and a split grouped by session scores the same (0.1109 against 0.1116). The task gamer found no
   exploit that beats an honest model by more than noise (+-0.003; even the oracle test prior gains 0.0003).
   Against: nothing on validity was raised by any agent. Every remaining point is P3 wording, P6 or P7.

2. Worth benchmarking (P6; TP-1 to TP-9).
   Evidence: dummy 1.421 (the honest session-prior dummy is 1.08, claim auditor), single feature (syn_size) 0.270,
   random forest 0.131, LightGBM 0.133. The best single feature loses twice the best family's loss, so TP-4 is not
   met. The smallest class has 550+ rows per test fold (1,363 to 1,875 Windows Phone rows by the claim auditor).
   Against the blind reviewer's "accuracy near the ceiling" (0.957): the declared metric is log loss (MET-8, MET-11),
   which still spreads the models: notime_sw 0.096, untuned unweighted 0.186, linear 0.212. The remaining errors sit
   in Mac OS against iOS and Windows Phone, a real and hard part of the task. Precedent: unlike ctu_13 (a two-port
   rule at 0.852 against 0.858), this task has headroom (precedent checker 6).

3. The use case is real and the fit approximate is honest (P3; USE-1, USE-5, USE-8).
   Evidence: NOMS 2020 builds and scores exactly these classifiers. The curator chose this source over
   cesnet_os_fingerprinting_2024 for its sessions, times and DHCP labels (CC 2026-11-08; tension row "Same task,
   another source"). The domain practitioner, playing the actor, agrees the fit is approximate. The gaps (closed set
   without Linux, label from DHCP host names, per-device decision) are named in fit_reason, as for sarcoma (closed
   set) and diabetes_3 (label construction) (USE-8 and USE-5 cases). The label is cleaner than the notes suggest:
   137 of the 141 TTL-64 "Windows" sessions have the Windows SYN 52 / window 64240 stack, and 103 have User-Agent
   code 68 (practitioner). Under "A better version against our own fix" (eryhemato), we do not relabel.
   Fix, no decision needed: rewrite the TTL anomaly bullet with that evidence, and name in fit_reason that the label
   has no OS version.

4. The session-weighted log loss is the right branch of MET-17. The builder's evidence for it was wrong, and it must
   be corrected (P6; MET-17 Should, MET-11, MET-5/MET-6).
   Conceded: claim 38 is refuted. Close LightGBM fits swap order in about half their pairs between the per-flow and
   per-session scores. The best fit per flow is never the best per session. A prior shift alone gains 5-11% (claim
   auditor). Training with the session weight takes an untuned model from 0.186 to 0.096 (task gamer). So issue 1's
   line "moves levels, not the order" must go.
   Why it still ships: a ranking change is what MET-17 exists for (its Why: tau 0.66 to 0.98 on its six cases). The
   actor decides per device. Windows holds 39.5% of flows but 7.0% of sessions, and one session holds 578,764 flows.
   The precedent checker finds the weighted branch consistent with pancreatic, dementia and bacteria_id_raman. The
   fallback to log loss is right (MET-5, MET-6: the paper reports four micro-averaged metrics).
   MET-15 (Must) keeps a unit weight for scoring only. The weight reaches a pipeline through validation_weight(), so
   learning the session-level prior is a fair modelling choice, not a hidden trap.
   Mildest fixes, no decision needed: replace issue 1's evidence with the claim auditor's numbers and the honest dummy
   (1.08). In the README Metric block, say that the score's class balance is per session. Reword use_case to say the
   team records each device's OS per Wi-Fi session (claim auditor I3). Reword "each session counts once" to "carries
   equal weight before sampling" (I2). Per-flow scoring (option b) stays the curator's weighing call. The
   practitioner's aggregated per-session score would change what one prediction is: SPLIT-23 (Must) and MET-17's
   last sentence bar that without a cited per-device use case of the source.

5. The undeclared unit_weight is a library gap with a ready fix, not a dataset defect (P6; MET-17 Should).
   Evidence: claim auditor M2. With the builder's three-line change to the check (sampling only removes rows), the
   shipped frame passes: 43,948 units, none above 1.0, and no unit on both sides of a split.
   Mildest fix: keep an opaque (session, half-day) id as metadata and declare UnitWeight once the check is relaxed.
   This is the precedent checker's prompt A (a), and it matches the curator's boreal call. Until then, keep the
   library gap in the notes (option b). Either way the score is unchanged.

6. The time columns are a P7 note, not a validity problem (P7 under P4; CLEAN-5 spirit, house convention).
   Evidence: flow_start and period are known at the prediction point. Shipping the time key as a feature is the house
   convention, and encoding dates is the model's job (data_foundry.v2.encodings; split auditor finding 4). Read as raw
   numbers, they cost a naive model 0.015 (split auditor) or 0.018 (task gamer, 0.114 against 0.096 weighted). The
   task gamer's 1.252 is the unweighted, untuned run, not the declared score.
   Mildest fix: a note that period is only the split key. Drop period when TemporalSplits gains an hours unit
   (library gap 1). A temporal benchmark that punishes naive date extrapolation measures something real.

7. The cleaning findings are cheap and safe, so apply them. The destination address stays dropped (P7; CLEAN-3,
   CLEAN-10, CLEAN-11, CLEAN-14, all Should).
   Apply without a decision (column auditor findings 3 to 6):
   - type dst_port as categorical, since it names a service;
   - set syn_size below 40 to missing (87 shipped rows);
   - set tls_sni_length to missing where no ClientHello was parsed (888 shipped rows);
   - type tls_extension_types as categorical, like the cipher list;
   - add the notes lines on TLS 1.3 being exported as TLSv1.2, the 64-byte SNI cut, and the HTTP host being
     plain text.
   Destination address (issue 2): the decisive experiment (EV-1) was run with the server names present. It gives no
   consistent gain: medium LightGBM -0.0003 on average, with the sign flipping across windows; shallow -0.0009. This
   answers the precedent checker's open point ("not yet measured with the SNI and host"). It also sets the case apart
   from lt_vehicle, kick and amazon, whose codes carried meaning. Keep (a), recorded as an exception to CLEAN-3 with
   the measured redundancy and the 79,163 single-session peer addresses as the stated fact.

Judgment record (proposed):
Verdict: ship after changes (none needing a decision), two weighing calls for the curator.
Validity: SEL-1, SEL-2 hold; USE-1 holds (approximate, gaps named); LEAK-10 triggered, fixed; SPLIT-1, SPLIT-14 hold,
  SPLIT-19 departure forced by a Must; PROV-1 holds.
Value: TP holds (0.270 single feature against 0.131); MET-17 weighted branch, evidence corrected.
Quality: CLEAN-10, -11, -14 fixes applied; CLEAN-3 exception for dst_ip (measured redundancy); time key kept with a note.
For the curator: issue 1 (per-session against per-flow), issue 2 (dst_ip, recommend a), prompt A (unit_weight, a).

========================================================================================================================
Rebuttal (2026-11-09, to the critic's opening brief)
========================================================================================================================
The critic and I agree on the verdict: ship after changes, no exclusion, no validity failure. Most of its points are
my own fixes (my points 3 to 7). What remains in dispute is how point 2 is remedied, and whether point 3 is the largest
gap.

C1 (the use case and the metric name different decisions; USE-1, MET-17). CONCEDE. The text supports both branches
   (claim auditor I3). What follows: the curator picks the decision, and the text is aligned with it. I recommend per
   device. Three facts support it: the paper's coverage is counted per session (Sect. VI.A), the inventory is the
   use case of the abstract ("asset identification"), and the weighted MET-17 precedents (pancreatic, dementia,
   bacteria_id_raman) have the same shape. Under that choice, use_case and question become "records each device's OS
   per Wi-Fi session". Per-flow SIEM tagging (USE-9) is the real alternative, and it is option (b) of issue 1.
   Either way this is a wording fix to the definition (the remedy ladder's second rung).

C2 (the scoring-only weight moves the best prediction; MET-2, MET-15). CONCEDE the facts, and that issue 1 and the
   TP baseline (1.08, not 1.42) must be corrected before the curator decides. DISPUTE the preferred remedy and the
   word "undeclared".
   - Declaring session_weight as the sample_weight contradicts MET-15's unit-weight clause, a Must. A Must has no
     exceptions (principles.md), so the remedy would be an amendment. That is a rule change for the curator, not a
     fix for this dataset.
   - The class prior is not undeclared. It is the metric's declared weight column, and validation_weight(container)
     returns it (precedent checker 1b). A pipeline that weights its validation loss, or calibrates on it, recovers the
     prior. The task gamer's 0.0963 shows the honest route works.
   - MET-15's "only as far as..." clause gives the reason the weight stays scoring-only. It does not set a size limit.
     A larger effect here means MET-17 matters more, not that MET-2 fails: every fold is still scorable, and the score
     matches the decision (MET-2 holds).
   What follows: the mild remedy. Under (a), the README Metric block says the score's class balance is per session
   and that validation_weight gives it. Whether MET-15 should be amended is a separate question the curator can take
   up, with this case as its fact. Under (b), the mismatch is gone.

C3 (fit_reason leaves out that the test devices already have the label, and that the unit is a session, not a
   device; USE-8). CONCEDE as a note. Both facts are measured or cited (split auditor 1, practitioner gap 4, claim
   auditor I4), and both belong in fit_reason. DISPUTE "largest gap". Every gap the critic lists keeps the fit
   approximate, which it already is. USE-8 asks that gaps be named, not ranked. The label being known at connection
   is what makes "no gap" right (SPLIT-10), and the precedent tension "a better version against our own fix" keeps
   the source's labelled population. The remedy is a sentence, as the critic says.

C4 (no unit_weight, the unit's column dropped; MET-17 Should). CONCEDE; this is my point 5. The (session, half-day)
   id goes in as metadata, the builder's check change is applied, and UnitWeight is declared (prompt A, option a).
   Until the library change lands, the gap goes into the definition's notes and REVIEW.md, not only the run log.

C5 (period ships as a model input; CLEAN-19 and CLEAN-5 in spirit). CONCEDE the remedy, with one correction of
   scale. The 1.252 and the r2 2.79 are untuned, unweighted fits on flow_start and period together, and the critic
   keeps flow_start. On the declared score, both time columns together cost 0.015 (split auditor) to 0.018 (task
   gamer, 0.114 against 0.096). This is P7, not P4. Drop period once TemporalSplits has an hours unit. Until then,
   keep it with the note.

C6 (four cheap cleaning fixes; CLEAN-10, CLEAN-11, CLEAN-14). CONCEDE all four. They are my point 7: dst_port and
   tls_extension_types as categorical, syn_size below 40 and the filler tls_sni_length set to missing, the rows kept.

C7 (notes the evidence contradicts; EV-2). CONCEDE every bullet: the TTL anomaly, "each session counts once", the
   destination-address numbers, "readable when encrypted" against http_host, TLS 1.3 exported as TLSv1.2, and the
   weight's ranking effect. One limit on the destination address: the 22.4% of flows without a server name weakens
   the stated reason. It does not change the measurement, which was taken over all flows with the names present and
   shows no consistent gain (column auditor). The recommendation (a) therefore stands, recorded as a CLEAN-3
   exception that cites those numbers and the 79,163 single-session peer addresses. The keep-or-drop call stays the
   curator's (issue 2).

Net: the remaining disagreement is one call for the curator, the remedy under C2: a README note and validation_weight
(my position, consistent with MET-15 as written) against a sample_weight that needs MET-15 amended. Every other point
is an edit both sides accept.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-09

Verdict: ship only after changes. Not exclusion: the task is real (P1, P2, P5 hold; no leak, LEAK-10 handled; the
temporal split is right, SPLIT-14 over SPLIT-19). But the definition does not say which decision it scores, its metric
rests on a refuted claim, and the fit leaves out its largest gap. Points in rank order. Sources: the seven phase-A
reports in this folder, builder_report.md, dataset.py, README.md, principles.md, metrics.md, use_case.md,
cleaning_features.md (df-large worktree).

1. P3, USE-1 (Must) feeding MET-17 (Should): the use case and the metric name different decisions.
   Problem: `question` and `use_case` say the team "labels each connection with the operating system". Only the
   metric reason and `fit_reason` say "the inventory decides per device". MET-17 weights rows only "if the actor
   decides once per unit". It keeps the per-row score "when each row is a decision of its own". As written, the
   definition supports both branches and so it backs neither.
   Effect: the session weight, the dataset's most important scoring choice, has no use case in the text that ships.
   Evidence: claim auditor I3 (INCONSISTENT); precedent checker 1 ("the text supports both"). The domain practitioner
   names per-flow tagging (an OS on each flow or SIEM alert) as a real use case (USE-9) whose score is the unweighted
   per-flow one, the paper's unit (Sect. VI.B).
   Remedy (fix the definition): the curator picks the decision. Per device: rewrite use_case and question so the
   team records each device's OS per Wi-Fi session, and keep the weight. Per flow: say so and score unweighted, with
   MET-17's note on how unequal the sessions are.

2. P6, MET-2 (Must), with the premise of MET-15's unit-weight clause (Must) refuted: the scoring-only weight moves
   the best prediction, and honest pipelines may not train on it.
   Problem: MET-15 keeps a unit weight scoring-only because "it moves the best prediction only as far as a unit's
   number of rows tells about the target" (dementia -0.004 log loss, pancreatic -0.015 AUC). Here the session size is
   strongly tied to the class. Windows is 34-38% of a window's flows but 6.0-8.0% of its weight, and Android is
   55-56% of the weight. So a model fit on flows carries the wrong class prior for the score. The README forbids the
   one remedy ("never a feature or a training weight").
   Evidence: claim auditor claim 38 REFUTED. Among the competitive LightGBM fits, 17/36, 19/45 and 19/36 pairs swap
   order between the per-flow and the per-session score, and the best fit per flow is never the best per session
   (3/3 windows). The builder's tau 1.0 compared feature subsets 0.05 to 1.2 apart. Claim 39's premise REFUTED: a
   post-hoc shift to the session-weighted class prior lowers the declared loss on 6/6 fits by 5-11% (e.g. 0.1320 ->
   0.1176). Session-weighted training helps by 0.012-0.034. Task gamer flaw B: an untuned LightGBM gets 0.186
   unweighted against 0.0963 trained with session_weight. Both are many times the MET-15 bounds. The honest null is
   the session-weighted prior, 1.08 (claim auditor 40), not the 1.42 the TP baseline quotes.
   Effect: as shipped, the benchmark partly ranks pipelines by whether they recover an undeclared class prior.
   Builder issue 1 tells the curator "the call moves levels, not the order", which is false.
   Remedy: correct issue 1 with these numbers before the curator decides. If per device (point 1): declare
   session_weight as the sample_weight too. That contradicts MET-15's clause, a Must with no exceptions, so it is an
   amendment for the curator with this case as its fact. Or name in the README Metric block that the score's class
   balance is per session and that validation_weight gives it (weaker). If per flow: score unweighted, and the
   mismatch is gone. Fix the TP baseline to 1.08.

3. P3, USE-8 (Must): fit_reason leaves out the largest gap. The test devices already have the label.
   Problem: the label is the DHCP host name, known when the device connects (the splits comment uses that fact for
   "no gap"). On this network the actor already holds the OS of every device in the test windows. The model is
   needed for devices without an informative host name (edited Windows names, phones that send random or no names),
   and the release cannot contain them. The unit is also a session, not a device. The paper counts 45,602 sessions for
   11,962 MACs, so a device can count several times in a window.
   Evidence: split auditor finding 1 ("open for the curator ... no split here can simulate them"); domain
   practitioner gap 4; claim auditor I4 (UNTESTED, no MAC). fit_reason names labels, flows against devices, one
   network and no Linux, but not this.
   Remedy (a note): add both to fit_reason: the test devices are DHCP-labelled devices, standing in for the
   unlabelled ones the model serves, and the unit is a session per half-day, not a device. Fit stays approximate.

4. P6, MET-17 declaration clause (Should): no unit_weight, and the unit's column is dropped.
   Problem: MET-17 says "the task declares it as its unit_weight (the weight column and the unit's column)". The
   curator's boreal call (2026-11-08) asks that the group type "can be read by downstream tools". Five precedents
   declare it (boreal, dementia, pancreatic, superconductivity, bacteria_id_raman). Here `_clean` drops session_id.
   The reason (library gap 2: the row budget breaks the sum-to-1 check) is only in the run's builder report.
   Effect: downstream validation cannot keep a session's flows on one side, and a model's inner validation spreads
   sessions over train and validation.
   Evidence: precedent checker 1b / prompt A; claim auditor M2: under the builder's relaxed check the shipped frame
   passes (43,948 units, every sum <= 1.0, no unit on both sides of a split).
   Remedy (fix the definition after a small library change): keep an opaque (session, half-day) id as metadata, never
   a feature. Declare UnitWeight(column="session_weight", unit=<that id>). Apply the builder's check change. Until
   then, at least state the gap in the definition's notes and REVIEW.md.

5. P7, CLEAN-19 and CLEAN-5 in spirit (Should): `period`, our split key, ships as a model input.
   Problem: `period` is flow_start floored to 12 h. We built it only because TemporalSplits has no hours unit. None
   of CLEAN-19's reasons for building a feature holds. In each test window it is one value never seen in training.
   Effect: time inputs that lie past the training range hurt models. Task gamer flaw A: untuned LightGBM with the
   time columns 1.252 against 0.186 without (window r2 2.79, worse than the 1.42 dummy). Split auditor: 0.127
   against 0.112. Both measured flow_start and period together. flow_start is the source's own time, kept by house
   convention (CLEAN-2 nyc_taxi case), and I do not argue against it.
   Remedy (fix the definition): split on flow_start with an hours unit (library gap 1) and drop period. If the
   library change cannot come first, keep it with a note that names it as the split key with no information beyond
   flow_start.

6. P7, cheap and safe cleaning (Should each), measured by the column auditor:
   - dst_port is a service code typed as a number (CLEAN-14, last bullet). The top 10 values cover 96.9% of rows,
     ports 55/3091 are 100% iOS and 7275 is 99.8% Android. The definition's own reason is that it "names the
     service". Remedy: categorical.
   - syn_size holds impossible values: 328 task flows (87 shipped) of 2-34 bytes, below the 40-byte minimum of an
     IPv4 TCP SYN (CLEAN-11). Remedy: missing, rows kept, a note.
   - tls_sni_length is 0 as the probe's filler on 3,829 task flows (888 shipped) with no parsed ClientHello, where
     every list is already set missing (CLEAN-10). Remedy: missing there.
   - tls_extension_types is a string (428 shipped levels) while its sibling tls_cipher_suites (276) is categorical.
     The paper encodes every TLS list as categorical, and the column alone scores 0.915, the strongest TLS field
     (CLEAN-14). Remedy: categorical.
   None of these is a reason to exclude (principles.md, "a real task against imperfect cleaning").

7. Writing and EV-2: notes that the evidence contradicts. The notes must match what was measured.
   - TTL anomaly: the notes guess "devices whose host names misled the labelling". In fact 137 of the 141 sessions
     send only TTL <= 64, with the modal Windows SYN pair (52 / 64240) on 205,630 of their 260,552 flows and
     User-Agent code 68 in 103 of the 141 (domain practitioner). They look like real Windows hosts.
   - "Each Wi-Fi session counts once per window in the score" (task_summary.split). After sampling, the per-session
     sums run 0.03-1.0 (mean 0.26-0.48). It holds only in expectation (claim auditor I2).
   - The destination address: the stated reason ("the server's name is in the clear in the SNI or HTTP host") fails
     for 22.4% of task flows (2,983,583) that have neither (precedent checker). The cited 0.176 -> 0.163 was measured
     without the names. Next to them the gain is -0.0011 (shallow) and has no stable sign (medium) (column auditor).
     The keep-or-drop call stays the curator's (builder issue 2), but the notes must carry these numbers.
   - use_case says the inputs are "fields that stay readable when the traffic is encrypted", but http_host is plain
     HTTP. Also missing: the TLSv1.2 value includes TLS 1.3 clients (49% of shipped TLSv1.2 rows carry 0x002b), and
     the weight's ranking effect is not stated, as every MET-17 case states it.
   Remedy: rewrite these notes.

Asked of the curator before shipping: decide point 1, and with it point 2, on corrected evidence. Points 3, 4 and 7 are
edits to the definition, and 5 and 6 are cheap fixes in `_clean` and `_feature_types`.

========================================================================================================================
Rebuttal (critic, 2026-11-09), point by point against the advocate's opening brief

Where we now stand: we agree on most remedies. Two disputes remain. The fit reason needs one more gap named (USE-8,
Must). Issue 1 is a decision that needs the sample-weight option, not "no decision needed".

A1 (validity holds). Concede on P1, P2, P4 and P5: no leak, and the split is right. Dispute "nothing on validity
   was raised by any agent". Two agents raised a P3 question: split auditor finding 1 ("open for the curator") and
   domain practitioner gap 4. On this network every test device already carries its label when it connects. The
   devices the model would serve, those without an informative host name, are not in the release. Claim auditor I4
   adds that the unit is a session, not a device (45,602 sessions for 11,962 MACs). USE-8 (Must) asks for every known
   gap to be named, and the advocate's fit_reason fix (point 3) adds only "no OS version". My point 3 stands as a
   note, not exclusion.

A2 (worth benchmarking). Concede. TP-4 is not met (0.270 against 0.131), and log loss spreads the models. The TP
   baseline in the notes and issue 1 should quote the session-prior null, 1.08, which the advocate also cites.

A3 (real use case, approximate fit). Concede the use case, the closed-set precedents (sarcoma, diabetes_3), no
   relabelling (eryhemato) and the TTL bullet rewrite. Dispute only the gap list, as under A1.

A4 (session-weighted log loss is the right branch). The advocate concedes the evidence: claim 38 is refuted, and the
   prior shift (5-11%) and weighted training (0.186 to 0.096) are large. I dispute two things.
   (i) "A ranking change is what MET-17 exists for" answers the wrong question. My point is not that the ranking
   moves. It is that the best prediction moves. MET-15 (Must) keeps a unit weight scoring-only on the stated premise
   that the weight "moves the best prediction only as far as a unit's number of rows tells about the target", with
   bounds of -0.004 (dementia) and -0.015 AUC (pancreatic). Here weighted training gains 0.012-0.034 (claim auditor)
   and 0.09 untuned (task gamer). EV-1/EV-2 say a measurement outranks a stated reason, so the curator must see that
   the clause's premise fails here.
   (ii) "The weight reaches a pipeline through validation_weight(), so it is a fair modelling choice." Its docstring
   offers it for "model selection, early stopping and tuning on a validation split" and says to "keep a unit's rows
   on one side of the validation split". The README forbids it as a training weight ("never a feature or a training
   weight"). So a compliant pipeline can at most recalibrate on validation data. It cannot take the measured
   weighted-training gain, and without the unit column (A5) it cannot keep sessions apart in validation either. The
   trap stays.
   "No decision needed" is also wrong for the use_case rewording. If the curator picks per flow under issue 1, "labels
   each connection" is the right text. The wording follows issue 1, it does not come before it (USE-1, Must).
   Remedy, unchanged: issue 1 goes to the curator with three options. (a) Per device, scoring only, with the README
   note (the advocate's choice). (a') Per device with session_weight also the sample_weight (an amendment of MET-15's
   clause, with this case as its fact). (b) Per flow, unweighted. Concede: the practitioner's aggregated per-session
   score is barred by SPLIT-23 and MET-17's last sentence without a cited per-device use case. I did not ask for it.

A5 (unit_weight). Concede the remedy: prompt A (a), an opaque (session, half-day) id as metadata plus UnitWeight,
   once the check is relaxed (claim auditor M2). Dispute "either way the score is unchanged" as a reason to accept
   (b). The score is unchanged, but A4(ii) rests on validation_weight, which needs the unit to work as documented.
   Ship with (a). If the library change cannot come first, ship (c), the key kept as metadata, not (b).

A6 (time columns). Concede. The task gamer's 1.252 is the unweighted untuned run. On the declared footing the cost
   is 0.015-0.018 (split auditor; task gamer 0.114 against 0.096), and flow_start stays by house convention (CLEAN-2
   nyc_taxi case). The advocate's remedy is my fallback: a note that period is only the split key, and drop period
   when TemporalSplits gains an hours unit (CLEAN-19, Should).

A7 (cleaning, destination address). Concede the four cleaning fixes and the notes lines. On the destination
   address, concede keep-dropped as an exception to CLEAN-3. The column auditor's experiment with the names present
   (shallow -0.0009, medium -0.0003 with a flipping sign) is the distinguishing fact from lt_vehicle, kick and amazon.
   The condition is my point 7: the notes' current reason ("the server's name is in the clear in the SNI or HTTP
   host") and its 0.176 to 0.163 figure must be replaced. The reason fails for 22.4% of task flows (precedent
   checker), and the figure was measured without the names.

Judgment record. I accept the advocate's version with two edits:
- "Validity: USE-8 holds once fit_reason names the DHCP-labelled test population and session-not-device units."
- "For the curator: issue 1 with options a / a' / b on corrected evidence; use_case wording follows that call."
```

</details>

<details><summary>Review editor</summary>

```text
REVIEW EDITOR: tls_os_fingerprinting_masaryk (folder tls_os_fingerprinting_masaryk_1m), 2026-11-09

1. Issue 1, Problem (all three sub-bullets), replace with: (i) "The score can count each Wi-Fi session once, as the security team's inventory would (implemented: each flow weighs 1 over its session's flows in the half-day, so a session counts the same however many flows it has), or count each flow, as the paper does; Windows has 39.5% of the flows but 7.0% of the sessions, so the two scores rank close models differently." (ii) "Under the implemented score the weight is for scoring only: no model receives it when training (it is neither a feature nor a training weight), so a model learns the flows' class mix (much Windows) while the score counts sessions (little Windows); training with the weight instead changes the loss by between 0.008 worse and 0.12 better, depending on the model, far more than the rules assumed when they kept such weights out of training[^m15]." (iii) "Our rule counts a unit once when its extra rows are repeats a measurement protocol made (a mouse bled five times), and per row when each row is a decision of its own; a session's flows are neither, they are the device's own traffic[^m17]."
2. Rename the options a, a', b to A, B, C everywhere (title, table, Recommendation, Panel bullet, Notes for the AI, Outcome, Main points); issue 2's a, b, c to A, B, C too.
3. "per device" -> "per session" in issue 1 (title, Problem, Effect, Options, Recommendation, Main points, Outcome). New title: "Count each Wi-Fi session once (its weight for scoring only, or also for training), or each flow?"
4. Issue 1, Consistency bullet 2: remove the "question for reflection" (should the rule read "repeats the protocol made, or rows the unit's own activity generated"?) and put it into option A's "What it does" as "...; the unit rule's wording widened to rows a unit's own activity generated (an amendment, this dataset its case)", so the issue carries one decision; update the Notes for the AI accordingly.
5. Issue 1, Recommendation, new: "A: the inventory decides per session, the rule as written keeps the weight out of training as in the five earlier cases, and the README tells pipelines the score's class balance so they can weight their validation or recalibrate; take B only if a training effect this large should change the rule for every unit weight, with this dataset as its case. **Decision:** A, B or C?"
6. Signs: in Experiments bullet 3 use "between 0.008 worse and 0.12 better"; Options row A Con: "training with the weight would score 0.008 worse to 0.12 better, by model"; Outcome Value line: "moves the score by 0.008 worse to 0.12 better, by model".
7. Experiments bullet 2: after "a regularised LightGBM (31 leaves, at least 500 rows per leaf) 0.139, 0.131 and 0.095" add "; per window 0.099 / 0.101 / 0.217 unweighted against 0.096 / 0.087 / 0.101 trained with the weight, so for this model almost all of the gain is in one window" (verify against the mediator's table); "The mediator's decisive run (same features, no time columns):" -> "One feature set without the time columns, mean of the 3 windows:".
8. Experiments bullet 1: delete "; the builder's 'levels, not the order' (Kendall tau 1.0) compared feature subsets 0.05 to 1.2 apart and is withdrawn".
9. Experiments: "Honest nulls: the train side's flow prior scores 1.43, its session prior 1.08 (the null for this score)" -> "A model that always predicts the class shares of the training flows scores 1.43; one that predicts the shares with each session counted once scores 1.08, the baseline for this score."; bullet 2 "with its probabilities shifted to the train side's session-weighted class shares" -> "with its class probabilities rescaled to the class shares of the training sessions (Windows about 7% instead of 40%)".
10. Options row B, What it does: "every model trains with the session weight; the unit-weight declaration removed until the library allows both" (code stays in Notes for the AI).
11. Outcome opening, new: "The AI recommends shipping it as defined; open are whether the score counts each Wi-Fi session or each flow and whether the session weight may also train (issue 1), and a confirmation that the destination address stays dropped (issue 2)."
12. Outcome: remove the lines from "The panel's changes are in `dataset.py`: ..." through "(a tooling gap, worked around for these runs)." (the probe tooling gap is fixed in the worktree's dataset_io.py now).
13. Outcome Value line: "TP-4 not met (best single feature 0.282 ...)" -> "TP-4 holds, not trivial (best single feature 0.282 ...; the baseline with each session counted once, 1.08)".
14. Outcome Validity line: "USE-1 holds once the use case names the decision the score counts (now per device, issue 1)" -> "USE-1 holds (the use case names the per-session decision; issue 1)"; "LEAK-34 recurring sessions kept (+0.0014)" -> "LEAK-34: recurring sessions kept (removing them changes the score by 0.001 to 0.002)".
15. Outcome Value line: "(a first case, issue 1)" after the MET-17 phrase -> "(an amendment under A, issue 1)".
16. Main points, one line: "Issue 1: count each Wi-Fi session once with the weight for scoring only (A, implemented), also for training (B, a rule amendment and a library change), or each flow (C); issue 2: confirm the destination address stays dropped."
17. Record judgment: "the 18,708,983 flows, 45,602 sessions and five classes match the paper" -> "the 18,708,983 flows and 45,602 sessions match the paper; the release has five classes, without the paper's 1.5% Linux and other".
18. Issue 1, Effect bullet 2 and Options row C Con: "the inventory use case (the reason this source was chosen over cesnet_os, which has no sessions) goes unused" -> "the inventory use case, one reason this source was preferred over cesnet_os (its sessions), goes unused".
19. Issue 1, Panel bullet 2: "the mediator measured both sides right in part (the effect depends on the model)" -> "the mediator's run found each side right for some models".
20. Issue 1, Experiments bullet 3: "On another encoding (the claim auditor's)" -> "On another feature preparation (the claim auditor's)".
21. Issue 2 (optional): add "**Effect on the task:** dropping it costs nothing measurable on flows with a server name; on the 22.4% without one the effect is unknown."
22. dataset.py metric reason: "a model fitted with it scores -0.008 to +0.12 better than one fitted without it" -> "between 0.008 worse and 0.12 better".
```

</details>
