# cesnet_quic22_service_classification

**Outcome:** added as `cesnet_quic22_service_classification_1m`. QUIC flow records of four weeks on the CESNET2 backbone (31 October to 27 November 2022), labelled with one of 102 web services from the server name, which is not an input; a fixed 1-in-20 hash sample of the release, tested on three 4-day windows (16 to 27 November) with a random million earlier flows per train side; the AI recommends shipping it after the panel's changes, which are made.

```text
Verdict: ship after changes (made).
Validity: the prediction point is the exported flow record, so the whole-flow counters and histograms are legitimate inputs; the use case now says "label exported flow records" (reporting, accounting, audit), and the notes give the score if the model had only the first 30 packets (log loss 0.260 against 0.220 with whole-flow inputs). The server name and user agent are dropped (the label is mapped from the server name). The closed world of 102 services is named in the fit note. Each split trains on 60-88% of the flows before its window; no gap is needed.
Value: real backbone traffic with headroom: LightGBM log loss 0.20, a lookup of the server address 0.84-0.88, the class shares 3.54.
Quality: negative inter-packet gaps (61 cells) and the reserved network number 65535 are now missing; the packet directions stay +1/-1 numbers as a named exception; the 1-in-20 sample of a temporal frame is recorded as a departure (class shares hold, chi-square p 0.35-0.99).
Weighed: source +, size +, headroom +, the 2022 view of server addresses before Encrypted Client Hello -.
Changed (no decision needed): the use case reworded to labelling exported flow records, with the first-30-packets score in the notes; the closed world named in the fit note; the record corrected to 102 classes and 140.47M service flows (the source's 105 and 153M kept as the source's figures); the metric reason notes that the class mix comes from the source's per-service sampling; the 1-in-20 sample recorded as a departure; split notes on the 31 Oct-1 Nov capture break and the 17-18 Nov holiday and bridge day; negative gaps and dst_asn 65535 set to missing; ppi_dir kept numeric as a named exception; feature count 132 and the 0xfaceb00x versions named as Meta's.
Probes: the final leak-stability run did not finish. Its first lines match the builder's run (all features macro ROC AUC 0.984, shallow tree 0.647 / 0.667), but its later checks (each feature alone, missing indicators, number format, drop-one, exact copies across the split, nearest-neighbour agreement, target by period) were not seen again on the final frame. Until it is re-run, the builder's run is the only evidence for those checks.
For the curator: 1, the server address and network as inputs; 2, the closed world of 102 services; 3, class-weighted log loss; 4, accept the check warning `task_stratify_high_cardinality`.
```

One more drop is decided with `ember2024_malware_detection`, issue 3: the smallest server-side size bin, constant only in the shipped frame (6 of the 7.0M sampled flows, none drawn), is dropped here; ember's issue 3 sets the rule for both.

**Main points:** Keep the server's address and network as inputs or drop them as the source's models do; keep the closed world of 102 services or add an "other" class; score plain or class-weighted log loss; accept the stratify warning.

**Issues for the curator:**

1. **Keep the server's address and network as inputs?**

   * **Problem:**
     - The label comes from the server name, which is dropped; the server address (`dst_ip`) and its network (`dst_asn`) are kept, and much of the score comes from looking up known servers: log loss 0.19-0.20 with them and 0.51-0.54 without, a gain of about 0.32-0.35.
     - The source's own models leave the address out and report a lookup of addresses as a separate baseline (68.68% accuracy).
   * **Effect on the task:** with the address, LightGBM log loss 0.195 and 0.192 (newest and oldest window), without both columns 0.507 and 0.544; the blind reviewer's accuracy / macro F1 0.948 / 0.868 with, 0.869 / 0.654 without.
   * **Experiments:** the address alone as a lookup of each server's earlier services scores 0.84-0.88 log loss and 68-70% accuracy, far from the model; 99.9% of test flows go to a server seen before; 0.2-0.74% of test addresses are unseen; 16.7% of the addresses serve several services and carry 62.9% of the flows.
   * **Consistency:**
     - `ugr16` drops its addresses, but its label was assigned on the addresses; here the label comes from the server name, which sets the case apart.
     - `2_month_survival_rate_prediction` kept the source's comparator out; `breast_cancer_prediction` kept the actor's own input (BI-RADS)[^prec]. The question is which of the two the address is.
   * **Panel:**
     - Advocate (keep): the operator holds and uses lists of server addresses (domain practitioner); the paper names an ensemble with the address as future work.
     - Critic (concern, does not ask to drop): the source's models and CESNET's DataZoo treat the address as an "other field", not a model input, and the address is worth less under Encrypted Client Hello and shared CDN fronts.
     - Mediator: rank does not settle it; the address is known at the prediction point[^use6], so it is a weighing call against precedent[^use10].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | `dst_ip` and `dst_asn` stay as categories; the fact that sets the case apart from `ugr16` (the label comes from the server name, the address is a raw field of the operator's flow record) goes into the Cases table of use_case.md | the operator's own field at the prediction point; the model still beats the lookup by far | much of the score is a lookup of known servers; departs from the source's ML task |
     | B | Drop both | the side-channel task of the source's models | follows the source's models and `ugr16`; tests the traffic features alone | throws away an input the operator has and uses |

   * **Recommendation:** A: the address is a raw field of the flow record, not another predictor's output for the target. **Decision:** A or B?

   **Notes for the AI:** on A, add the row to the Cases table of `.claude/skills/knowledge-curation/references/use_case.md` with the curator's reason. On B, add `dst_ip` and `dst_asn` to the dropped columns in `_clean` and `_feature_types`, rewrite the "Potential shortcut" note and `known`, re-run `dataset check` and the leak and task probes.

   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input, including a number the company itself produces.
   [^use10]: **USE-10** (Must): decide from the use case whether the entity the model predicts for is new or known, before choosing the split; with **SPLIT-13** (Should): look for grouped structure inside a temporal task.
   [^prec]: Precedents from the precedent checker's report: `ugr16` (batch of 2026-11-08), `2_month_survival_rate_prediction` (Lennart, 2026-10-26), `breast_cancer_prediction` (Lennart, 2026-10-15).

2. **Keep the closed world of 102 services, or let the model meet unknown services?**

   * **Problem:**
     - The release's three background classes (`google-background`, `facebook-background`, `default-background`; 8.3% of the release; about 16% of the source's flows by another count, before the per-service sampling) hold flows of services outside the 102 and are left out.
     - So the test never asks the model to reject an unknown service, which a deployed monitor always meets.
   * **Effect on the task:** not measured. An "other" class built from the background flows would be about 8.3% of the release, about as large as the largest service (`google-www`, 7.1-7.9% of a test day), and a mix of many services; tests would then also score how well the model rejects unknown services, which today's numbers do not show. For scale, the input set moves the score by about 0.04 (log loss 0.260 with the first 30 packets only, against 0.220 shipped).
   * **Consistency:** the source's evaluation paper (TMA 2023) trains and scores on the 102 services and names unknown services as a limitation; its data article keeps the background flows "for open-world scenarios".
   * **Panel:**
     - Domain practitioner: an operator always meets unknown services, so prefers 105 classes or an "other" class.
     - Advocate: the source's benchmark task is 102 classes, and the background classes are mixed buckets, not services.
     - Mediator: the fit note now names the closed world[^use8]; the class set is the curator's call[^use5].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 102 services (implemented) | background flows left out; the fit note names the closed world | the source's benchmark task; every class is one service | no test of unknown services |
     | B | One "other" class | the three background classes merged into one, 103 classes | the model must flag what it does not know | a mixed class whose mix is a sampling artefact |
     | C | 105 classes as released | the three background classes kept apart | the release as published | the background classes are buckets by provider, not services |

   * **Recommendation:** A, the source's task, with the gap stated in the fit note. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, change step 1 of `_clean` (map or keep the `-background` classes), the `predicted` and `fit_reason` text and the Decision table, re-run `dataset check` and the task probe.

   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it.
   [^use8]: **USE-8**: the fit is honest; an approximate fit names its gap.

3. **Score plain log loss, or weight the classes equally?**

   * **Problem:**
     - The class mix comes from the source's per-service sampling (the biggest services kept 1 flow in 15, the rarest kept whole), so it is not the network's mix.
     - Plain log loss weighs each class by its share in the release; a class-weighted log loss would weigh the 102 services equally.
   * **Effect on the task:** not measured; the ten rarest services hold 0.08% of a test window and 1.5% of LightGBM's log loss.
   * **Consistency:** the source reports accuracy, macro F1 and macro recall side by side and says only recall does not depend on the sampling; with no single metric chosen by the source, the default is plain log loss on the release's mix[^met5][^met16].
   * **Panel:**
     - Domain practitioner: would pick models by macro recall or a class-balanced log loss, since the mix is a sampling artefact.
     - Advocate: plain log loss scores the probabilities the operator thresholds and adds up.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Plain log loss (implemented) | the fallback on the release's mix | the default; scores the probabilities as used | the mix is the release's sampling, not the network's |
     | B | Class-weighted log loss | each service counts equally | does not depend on the sampling, like the source's macro recall | a new metric choice; the rarest services (15-24 test flows) weigh as much as YouTube |

   * **Recommendation:** A, the default, with the sampling stated in the metric reason. **Decision:** A or B?

   **Notes for the AI:** on B, declare a class-balanced log loss in `metric` (check the library has one, or propose it), re-run `dataset check` and the task probe.

   [^met5]: **MET-5** (Should): a paper's metric is the source's metric only when it is one deliberate choice; several reported ones mean the fallback; with **MET-6** (Should): a threshold metric only with a threshold the source fixes.
   [^met16]: **MET-16** (Should): a survey or design weight is never a feature; the task is scored unweighted.

4. **Accept the stratify warning with this text?**

   * **Problem:**
     - `dataset check` warns that the split is stratified on `service`, which has 102 values.
     - `service` is the target itself, stratified on purpose so each 500k test window and 1M train side keeps its rare services (15-24 test flows of the rarest).
   * **Effect on the task:** none; the draw keeps the class shares of each window, which the check takes for a high-cardinality column other than the target.
   * **Consistency:** keeping every class in each window follows the rare-class rule[^tp8].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept | the text below written into `dataset.py` on yes | the warning is answered with its reason; the rare services stay in every window | none found |
     | B | Do not accept (implemented) | the warning stays open | none | a known, explained warning stays on the dataset |

   * **Recommendation:** A. **Decision:** accept the warning with this text, yes or no?

   **Notes for the AI:** on yes, write `accepted_check_warnings = {"task_stratify_high_cardinality": "service is the target (102 classes); the row budget is stratified on it on purpose so each test window and train side keeps its rare services (15-24 test flows of the rarest)"}` in `dataset.py` and re-run `dataset check`.

   [^tp8]: **TP-8**: rare classes stay; the cut keeps every class in each window.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator; the rebuttal round was skipped, as the advocate's and the critic's briefs converged on ship after changes. The mediator ran no new experiment. Final leak-stability run: did not finish; its first lines match the builder's run (all features 0.984). Claim audit: no claim that bears on validity refuted; negative gaps, the QUIC version attribution and the feature count corrected. Blind review: would benchmark; main concern the server address. Task gamer: the whole-flow columns gain 0.034-0.045 log loss over a first-30-packets point (the use case reworded to exported records, the number in the notes). Debate: agreed on the split, the dropped server name and the export point; disputed: the address (issue 1), the closed world (issue 2), class weighting (issue 3).

<details><summary>Mediator: cesnet_quic22_service_classification</summary>

```text
MEDIATOR REPORT: cesnet_quic22_service_classification (folder cesnet_quic22_service_classification_1m), 2026-11-09
There was no rebuttal round. Both opening briefs reach the same position, "ship after changes", and neither asks for the dataset to be excluded. I ran no new experiment: the reports already agree on every fact that matters, so nothing needed settling by a test.

SUMMARY (15 lines)
1. Verdict: ship after changes. No unfixable Must failure was found; every agent ends at ship with changes or notes.
2. The gamer's only exploit is the 30 whole-flow columns, worth 0.034-0.045 log loss. It is a wording problem, not a leak (USE-3 / LEAK-1). Fix now: the use case becomes "labelling exported flow records" and the columns stay.
3. Changes that need no decision: record corrected (102 classes shipped, 140.47M service flows); closed world named in the fit note (USE-8); class mix from per-service sampling noted (MET-5/6); the sampled temporal frame recorded as a departure; split notes; CLEAN-11 repairs; ppi_dir as a named CLEAN-14 exception; feature count 132; quic_version 0xfaceb00x documented as Meta.
4. Curator issue 1 (USE-6, a Must; a weighing call against precedent): keep or drop dst_ip and dst_asn. Log loss is 0.19-0.20 with them and 0.51-0.54 without. Ranked first.
5. Curator issue 2 (USE-5/USE-8): the closed world of 102 classes, or an "other" class, or 105 classes.
6. Curator issue 3 (MET-5/6, a Should): plain or class-weighted log loss.
7. Across datasets: the 1-in-20 sample of a temporal frame is the 4th case in the batch, so an amendment of definitions.md is due.

JUDGMENT RECORD
Verdict: ship after changes.
Validity: USE-3 / LEAK-1 triggered and fixed by rewording (the prediction point is the exported flow record, so the whole-flow columns are legitimate). LEAK-10 holds (SNI dropped: the label is mapped from it). USE-6 holds for the address; whether to keep it is issue 1. USE-5 / USE-8: the closed world is stated in the fit note; the choice of class set is issue 2. SPLIT-14 holds (4-day windows, 59.7/69.4/87.8% train). SPLIT-10 holds with no gap needed (at most 0.0006% of flows straddle a boundary). SPLIT-20 needs notes added.
Value: real backbone traffic with signal and headroom (LightGBM 0.20 log loss; dummy 3.54; address lookup 0.84-0.88).
Quality: CLEAN-11 repairs (61 negative inter-packet gaps -> missing; dst_asn 65535 -> missing). CLEAN-14 departure kept as a named exception (ppi_dir +1/-1 numeric). The pre-split sample of a temporal frame is recorded as a departure from a Should.
Weighed: source +, size +, headroom +, 2022 pre-ECH view of server addresses -.
For the curator: issue 1 (address as input), issue 2 (closed world), issue 3 (class-weighted log loss).

CHANGES TO MAKE NOW (no decision needed)
1. USE-3 / USE-8 (Must): reword task_summary and use_case to "label exported flow records": reporting, accounting, SNI-less audit. Remove "QoS priorities" and inline enforcement. State in the notes that at the first-30-packets point the score is 0.260 log loss against 0.220 shipped (task gamer).
2. USE-8 (Must): the fit note names the closed world. Background flows (about 16% in the source, 8.3% by another count) are dropped and the test never asks the model to reject an unknown service.
3. Record fields: 105 classes / 153M rows -> 102 classes shipped / 140.47M service flows, keeping the source totals as the source's figures.
4. MET-5 / MET-6 note: the class mix comes from the source's per-service sampling (TMA footnote 2: the mix does not carry over to a network). Put this in the metric comment.
5. definitions.md "Temporal data: the frame is not sampled" (Should): record the fixed 1-in-20 hash sample as a departure. Class shares hold (chi-square p 0.35-0.99).
6. SPLIT-20 notes:
   - 31 Oct-1 Nov is a capture break with a different class mix (instagram 10% against about 4.5%).
   - 17 Nov holiday and a bridge day fall in the oldest test window.
   - Shifts in the sampling rate show as drift.
   - Dropping 31 Oct-1 Nov is optional; the measured gain is 0.007-0.012, near noise, so I do not recommend it.
7. CLEAN-11: negative inter-packet gaps (61 cells) -> missing; dst_asn 65535 -> missing.
8. CLEAN-14: ppi_dir_02 to _30 stay numeric as a named exception (the sign multiplies the packet sizes in the field's sequence models; lossless). Replace "CLEAN-26 by analogy" with that fact. Revisit when the PacketSequence kind lands (precedent checker option c).
9. Feature count: 133 -> 132 in the builder text. Document quic_version 0xfaceb00x as Meta's QUIC stacks.

ISSUES FOR THE CURATOR (ranked: validity first, Must first)

Issue 1. Server address and network (dst_ip, dst_asn) as inputs. Rules: USE-6 (Must) against USE-10 / SPLIT-13 and the precedents.
- This is not a conflict that rank settles. USE-6 allows the columns, because the monitor sees them at the prediction point. No higher Must forbids them. Whether to follow the source's ML task is a weighing against precedent, so it is the curator's call.
- Problem: with the address, much of the score is a server lookup.
- Effect: log loss 0.19-0.20 with both columns, 0.51-0.54 without. Blind reviewer: accuracy / macro-F1 0.948 / 0.868 with, 0.869 / 0.654 without.
- Advocate (keep):
  - The operator holds and uses IP lists (domain practitioner).
  - The address alone as a lookup is far from the model: 0.681 accuracy, 0.84-0.88 log loss.
  - 99.9% of test flows go to a known server, so a recurring server is part of the task.
  - The paper proposes an ensemble with the address as future work.
- Critic (concern, but does not ask to drop):
  - The source's ML models leave the address out and report an "IP baseline" (68.68%) beside them.
  - DataZoo lists DST_IP, DST_ASN and SRC_PORT as "other fields", not model inputs.
  - The address is worth less under ECH and shared CDN fronts.
- Precedents:
  - ugr16 drops its addresses. That label was assigned on the addresses; here it comes from the SNI, so the case is set apart.
  - 2_month_survival_rate_prediction (curator, 2026-10-26) kept the source's comparator out.
  - breast_cancer_prediction (curator, 2026-10-15) kept the actor's own input (BI-RADS).
- What would settle it: the curator's reading of whether the address is the actor's own field (like BI-RADS) or the source's separate comparator (like prg2m).
- Options: (a) keep, and write the fact that sets the case apart into the use_case.md Cases table; (b) drop both, following the source's ML task.
- Lean: (a). The address is a raw field of the flow record, not another predictor's output for the target.

Issue 2. Closed world (USE-5 / USE-8, Must). The fit statement is fixed now; choosing the class set is the curator's call.
- Domain practitioner: an operator always meets unknown services, so prefers 105 classes or an "other" class.
- Advocate: the source's benchmark task is 102 classes, and the background classes are mixed "other X" buckets, not services.
- What would settle it: whether the use case needs open-set rejection. If yes, add an "other" class built from the dropped background flows.

Issue 3. Class-weighted log loss (MET-5 / MET-6, Should; MET-16 is the default).
- Domain practitioner: would select models by macro recall or class-balanced log loss, because the class mix is an artefact of sampling.
- Advocate: plain log loss scores the probabilities the operator thresholds and aggregates.
- Effect: not measured.
- What would settle it: whether the mix of the release should count as the population's mix.

AGREED FACTS
- Release: 1-in-20 hash sample of 140.47M service flows, 102 classes. 3 temporal 4-day windows; each split's training rows end before its test window.
- Leaks: none among the 132 features at the export point. The 30 whole-flow columns exist only at flow end.
- Gamer, on mean log loss across splits (differences under about 0.01 are noise):
  - shipped features: 0.2195
  - first-30-packets point (whole-flow columns and time_first dropped): 0.2599
  - first-30-packets point, trained on the last 8 days: 0.2404
  - Other tested attacks gave no gain beyond noise: row order, copies, test-window context, EM priors, formats, identifiers.
- Address: lookup alone gives 0.84-0.88 log loss and 68-70% accuracy. 0.2-0.74% of test addresses are unseen. dst_ip has 5,702 levels and is typed categorical, consistent with the census_tract precedent.
- SNI dropped under LEAK-10: the label is mapped from the SNI.

TASK GAMER EXPLOITS, MAPPED
1. Whole-flow columns (gain 0.034-0.057). Rules: LEAK-1 / USE-3.
   - Known: the definition's prediction point is the export, and the paper's inputs include these columns.
   - Not covered by a "Potential leak, kept on purpose" note. The gamer measured against a first-30-packets point that only the use_case wording implies.
   - Resolved by change 1 (rewording), with the measured gain written into the notes.
2. H1, old training rows (honest gain 0.028-0.030). Rule: SPLIT-20 notes. The training window is the participant's choice; not an issue.
3. H2, time_first as a feature (gain 0.004-0.013, near noise). Participant's choice; no change.

CONSISTENCY WITH PRECEDENT
- 7 of 10 calls follow precedent.
- The address kept departs from the batch's ugr16 call and from the curator's 2_month call. Facts that may set it apart: the label comes from the SNI, not the address; the address is the operator's own raw field. It goes to the curator as issue 1.
- The pre-split sample of a temporal frame is the 4th case in the batch: an amendment item for the across-datasets list.
- ppi_dir against the fingerprint-bits rows of CLEAN-14 (2026-10-21): departure with a reason that holds, recorded as an exception.
- The QUIC_SNI drop matches tls_os's drop of the HTTP User-Agent OS fields: consistent.
- No drift found.
```

</details>

<details><summary>Claim audit: cesnet_quic22_service_classification</summary>

```text
CLAIM AUDITOR - cesnet_quic22_service_classification_1m (record cesnet_quic22_service_classification), 2026-11-09

Verdict: ship after note changes. No claim that bears on validity is refuted: the prediction point holds (no kept
column comes from the SNI, the user agent or the category), so do the 1-in-20 sample, the UTC-to-Prague shift, the
TIME_LAST drop, the background share, the address numbers (re-tested on the shipped splits with my own code), the
4-day windows against the paper's weeks, the probe re-run, the rare classes and the metric. Refuted or incomplete,
in rank order: (1) P3, the use case names decisions taken during the connection (QoS priorities, enforcing policies),
but the prediction point is the record's export and the features are whole-flow counters; (2) P4 SPLIT-20, the
"first two days" anomaly is a break in what was captured (another class mix), not only a volume dip; (3) P4
SPLIT-20, the oldest test window holds the 17 November national holiday and a bridge day, unmentioned, and they break
claim 38's working-day band; (4) five small number or attribution slips. None moves a score by more than 0.0015 nats.

Sources read: dataset.py and README.md (df-large), the record, claims.md, builder_report.md, the probe outputs; the TMA
2023 paper in full (text extracted to the agent's work foldertma.txt), the Data in Brief article in full
(paper/dib.txt), the zip's stats-dataset.json and the 28 daily stats-*.json; the Zenodo API for 10728760 and 7409924;
the IANA QUIC registry and the quicwg "QUIC Versions" wiki. Rules: principles.md, evidence.md, metrics.md, splits.md,
use_case.md, leak_checks.md, task_probes.md.

Tests run (scripts and outputs in the agent's work folder):
  a1_sample_checks.py -> a1_sample_checks.json: the 1-in-20 sample and the all-flow counts (shares, time zone,
     constants, histograms, addresses, windows, daily counts, window lengths).
  a2_container.py -> a2_container.json: the container through the definition (2,500,000 x 133, peak 15 GB); the
     scorer on a dummy per fold; classes per fold; addresses seen in the shipped train sides.
  a3_address.py -> a3_address_rep0.json, a3_address_rep2.json: LightGBM (the builder's settings, 250 trees,
     min_child_weight 1, 4 threads) on 100k shipped train rows and 100k shipped test rows, with and without
     dst_ip + dst_asn; the paper's IP baseline (majority service per address) on the full shipped sides.
  a4_first_days.py -> a4_first_days.json: the class prior and an address lookup trained with and without
     31 Oct - 1 Nov.
  Inline: the release's per-service sampling ratios (stats-dataset.json) and the daily received/seen/saved counts.

CLAIM TABLE
(claim | where | test | result | evidence | rule)

1 | Zenodo concept 7409923; 7409924 of 2022-12-07, 10728760 of 2024-02-29; same zip; md5 2d52...; CC BY 4.0 | claims 1, download_description | Zenodo API for both records | holds | 10728760: 2024-02-29, cc-by-4.0, conceptrecid 7409923, zip 20,952,008,298 B md5 2d52ad44...; 7409924: 2022-12-07, same size and md5; logs/md5.txt matches | PROV-1, EV-4
2 | servicemap.csv md5 89b5... | claims 2 | Zenodo API | holds | 9,519 B, md5 89b5080480db4be0c31bbbbdedd62451 | PROV-1
3 | 28 daily CSVs, one 30-column header | claims 3, _prepare_raw_files | zip listing; the header check in code | holds | 28 flows-2022*.csv.gz from 20221031 to 20221127; the code raises on any other header | PROV-13
4 | 153,226,273 flows | claims 4, notes | sum of flow_counts; stats-dataset.json | holds | 153,226,273 both | PROV-3
5 | CESNET2, about half a million users, 31 Oct - 27 Nov 2022 | claims 5, row | DiB Specifications and Sect. 3 | holds | "around half a million users"; Table 2 "31.10.2022-27.11.2022" | PROV-16
6 | client addresses Crypto-PAn, server addresses intact | claims 6 | DiB Specifications, 3.5 | holds | "Client IP addresses were anonymized; server IP addresses were left intact" | SEL-1
7 | bibtex DiB 46, 108888 | claims 7 | DiB header | holds | "Data Brief. 2023 Jan 9;46:108888. doi: 10.1016/j.dib.2023.108888" | PROV-10
8 | use case (ISP monitor, QoS, policies, SNI faking, ECH, without handshake decryption) | task_summary.use_case | TMA Sect. I | holds as a quote; PARTLY REFUTED against the prediction point, see R1 | "SNI faking [7], Encrypted Client Hello [8], QoS prioritization, or the enforcement of network-usage policies"; the features are whole-flow counters known only at the export | USE-1, USE-3
9 | fit approximate, gaps named (per-service sampling, background out, one network) | fit_reason | DiB 3.4; stats-dataset.json | holds | "top 5% ... 1:15; the bottom 60% ... not sampled"; measured 42 of 102 services saved at <= 1:1.67, 60 unsampled; release-mix entropy 3.55 nats against 2.95 for the network's (seen) mix | USE-8
10 | prediction point = the record's export, idle 65 s, active 5 min | notes bullet 1 | DiB 3.2; the first packet of every task flow | holds | DiB "active timeout of 5 min and an inactive (idle) timeout of 65 s"; ppi_size_01 >= 1200 B (min 1200, median 1250) and direction +1 on 100% of 7,026,437 task flows: every record starts with the client Initial, so no continuation record of a split connection is in the data | USE-3, LEAK-10
11 | fixed 1-in-20 SplitMix64 sample by ID, 7,663,274 flows, no ID repeats; keeps the shares | version_comment, notes | chi-square of sampled against all-flow counts / 20 | holds | 7,663,274 = 5.0013%; 7,663,274 unique IDs; per class chi2 102.2 on 105 classes (p 0.56, max |z| 3.0, jsdelivr); per hour 666.8 on 673 hours (p 0.56); per hour x class 30,763 on 30,734 cells (p 0.45) | PROV-3, EV-1
12 | three background classes, 12,752,625 flows = 8.3%, leave; the paper's task is 102 services | notes, Decision 2 | counts; TMA appendix and Sect. VI; TMA IV-A4 | holds | 12,752,625 / 153,226,273 = 8.32%, sampled 1:15 (0.0667, stats-dataset.json "backgrounds"); TMA "out_features=102", "standard closed-world classification"; the paper's "first week ... 30 million flows" matches the 30.03M SERVICE flows of week 44 (32.6M with background): the paper dropped the background too | USE-5, MET-2
13 | 7,026,437 task rows in the sample; 2,500,000 shipped | version_comment | a1, a2 | holds | 7,026,437; container 2,500,000 x 133 (132 features) | -
14 | background 1:15; 46 of 102 services have saved < seen, lowest 1/15 | claims 14 | stats-dataset.json | holds in substance, count slip | 46 only at a 0.1% tolerance; strictly 77 have saved < seen (31 lose a handful of flows); 42 are sampled at <= 1:1.67; lowest ratio 1/15.000 | EV-7 (nit)
15 | uber 6,239 in the release; 15-24 of the rarest per shipped test window; the ten rarest 0.08% of rows, 1.5% of the loss | notes, claims 15 | counts; a2 per-fold counts; probes/rare_class_loss_w2.json | holds | uber 6,239; shipped test minima 24 (uber), 23 (uber), 15 (livescore); all 102 classes in every test fold, one class below 20 (oldest); rarest-10 loss share 0.0151 on 0.0008 of the rows (one fit, with the address) | TP-8
16 | each of 36,948 server names maps to one class | notes | group by QUIC_SNI | holds | 36,948 names, 0 with two classes; CATEGORY is a function of APP (1 value per class) | LEAK-10
17 | QUIC_SNI, QUIC_USERAGENT (0.22%), CATEGORY dropped | notes, _clean | the dropped list; feature_columns | holds | none of the three among the 132 features; UA on 0.225% of task flows | LEAK-10
18 | ID, SRC_IP dropped; TIME_LAST = TIME_FIRST + DURATION within 30 us | notes | |TIME_LAST - TIME_FIRST - DURATION| over 7.66M flows | holds | max 30 us, 99.9th percentile 13 us | CLEAN-3, CLEAN-5
19 | constants: PROTOCOL 17, DST_PORT 443, ppi_dir_01 +1, ppi_ipt_01 0, psize_bin1 0; psize_bin1_rev non-zero on 6 | notes | n_unique on task rows | holds | 1 value each; psize_bin1_rev non-zero on 6 of 7,026,437 | CLEAN-5
20 | 88 packet columns; positions past ppi_len missing; 59.2% < 30 packets; sizes 12-1,472; gaps up to 64,999 ms | notes, claims 20 | a1 | holds with an omission | sizes 12-1,472; gaps max 64,999 ms but MIN -4 ms: 57 task flows hold negative gaps (unmentioned); 59.4% of the task flows have < 30 packets (59.5% in the shipped frame), not 59.2% | CLEAN-11 (nit)
21 | 30 histogram columns; size bins sum to the packet count (100%), gap bins to packets - 1 (100% / 99.97%) | notes | sums | holds | 100.000% / 100.000% / 99.99999% / 99.975% | -
22 | end-reason flags exclusive; idle 99.50%, active 0.45%, other 0.04% | notes, _clean | sums | holds | exclusive on 100%; 99.502 / 0.454 / 0.044% | CLEAN-12
23 | QUIC versions 0x1 90.0%, 0xfaceb002 6.6%, 0xff00001d 3.4%, 0xfaceb001 1,289, 0xfaceb00e 3; names "from the IANA registry" | notes, code comment, claims 23 | counts; IANA registry; quicwg wiki | holds, attribution wrong | counts exact; IANA's QUIC Versions registry lists none of 0xfaceb00x or 0xff00001d; the quicwg "QUIC Versions" wiki lists 0xfaceb00[0-f] Facebook mvfst and 0xff000000+ IETF drafts (0x1d = 29), so the code comment's names are right | EV-2 (nit)
24 | dst_ip 8,255 (3.4% IPv6), dst_asn 487; 5,702 / 336 shipped; 16.7% of addresses serve several services, 62.9% of flows; 99.9% seen before | notes | a1, a2 | holds | 8,255; IPv6 is 3.44% of the flows (10.2% of the addresses); 487; multi-service 16.7% / 62.9%; seen in all earlier sampled flows 99.94 / 99.89 / 99.86%, in the shipped 1M train side 99.81 / 99.64 / 99.75% | USE-6
25 | address as a lookup: log loss 0.83-0.86, 68.5-70.3%; paper's IP baseline 68.68% | notes | lookup on the SHIPPED train sides (a4); majority per address (a3); TMA Table I | holds | shipped train sides: log loss 0.855 / 0.874 / 0.836, accuracy 69.3 / 68.3 / 70.3%; majority-per-address 69.3% (newest), 70.2% (oldest); TMA Table I "IP baseline 68.68%" | TP-4
26 | LightGBM log loss 0.507 / 0.544 without address and network, 0.195 / 0.192 with; accuracy 86.1 -> 94.4%, macro recall 60.0 -> 81.5% | notes | own re-fit on the shipped splits (a3), same settings, other rows | holds | newest: 0.507 without, 0.190 with (accuracy 85.95 -> 94.48%, macro recall 59.8 -> 85.0%); oldest: 0.545 without, 0.190 with (85.07 -> 94.63%, 60.8 -> 84.6%) | USE-6, EV-6
27 | release times are UTC: daily files from about 22:55 UTC of the day before; peak 9-12 UTC; DST ended before the first flow; shipped as Prague time | notes, _clean | per-file min, 0.1% quantile, max; date match | holds | every file's min 22:54-22:58 UTC, 0.1% quantile 22:59:56-23:01:43 UTC, max 22:58:43-22:58:54 UTC; the Prague date equals the file's date for 99.89-99.96% of a file's flows, the UTC date for 95.8-98.4%; trough 3 UTC, peak 9-10 UTC; DST ended 30 Oct 01:00 UTC, first flow 30 Oct 22:55 UTC. DiB gives no time zone, so this rests on the measurement | EV-2
28 | the first two days hold about half the flows at every hour, "which the source does not explain" | notes (Anomaly) | daily stats-*.json (received/seen/saved), class mix per day | numbers hold; the reading is INCOMPLETE, see R2 | the source's own counts: total-received 27.9M and 28.2M against 70.2-75.8M on every later Monday and Tuesday; the class mix moves too: Google services 42.7 / 38.8% of seen service flows against 57.5-64.0% on every other day, Meta 35.5 / 36.4% against 13.8-17.1%; the day's mix (release counts) against the 2-27 Nov pool, total variation 0.30 / 0.29 against 0.018-0.113 on every other day; Google's sampling ratio unchanged (seen/saved 9.7 / 9.5 against 9.4-9.6) | SPLIT-20, PROV-3
29 | 29,987 flows over 300 s (max 360.17 s); 8 with PPI_DURATION > DURATION + 1 ms | notes | a1 | holds | 29,987; 360.1656 s; 8 | -
30 | 4-day windows train on 59.7 / 69.4 / 87.8%; weekly 71.2 / 49.2 / 21.4%; 5 days leave the oldest at 47.3% | splits_comment, Decision 1 | train shares from the all-flow counts by Prague day, window lengths 3-7 days | holds | 4 d: 87.77 / 69.43 / 59.68%; 5 d oldest 47.26%; 7 d 71.19 / 49.18 / 21.38%; 3 d 92.8 / 76.6 / 68.1% | SPLIT-14
31 | the paper trains on week 1 (30M) and tests on a 20M subset of weeks 2-4 and per week | splits_comment | TMA IV-A4, V | holds | "trained on the first week ... which consists of 30 million flows"; "tested using a 20 million subset from the remaining three weeks"; Table II per week | SPLIT-19
32 | Google's certificate change drove a drop within the second week | splits_comment | TMA V-A, Fig. 5, Sect. VI | holds (the paper's supported hypothesis) | Fig. 5 "in the second week (7th-13th Nov. 2022). The average recall of Google services dropped from ~92% to ~67%"; Sect. VI "substantial data drift can develop within a single week" | SPLIT-12
33 | no gap: the label is the connection's own server name | splits_comment | DiB 3.2-3.3; the first-packet test of row 10 | holds | the SNI comes from the record's own Initial packet, present in every record | SPLIT-9, SPLIT-10
34 | test pools 684k-1.29M keep 500k; train pools 4.19-6.17M keep 1M; stratified | version_comment | a1, a2 | holds | pools 684,195 / 1,288,936 / 860,292; train pools 4,193,014 / 4,877,209 / 6,166,145; shipped 1,000,000 / 500,000 per split, train ends before test starts, no overlap | SPLIT-14
35 | metric: fallback log loss; the paper reports four metrics side by side; footnote 2; nothing on Zenodo or in DiB; unweighted (MET-16) | metric reason, README Metric | read TMA IV (preamble), IV-A3, IV-B1, V-A, VI and DiB once more; scorer on a dummy per fold | holds (a wording note, see N1) | TMA: "we measure accuracy, macro averaged F1-score, and macro averaged recall" plus provider-level accuracy; "an apparent trade-off when choosing the classifier depending on the preferred metric"; model selection "based on the classification performance on the validation set" (metric not named); abstract "up to 88% accuracy" is a headline (MET-5); DiB defines none. Computable: spec log_loss, origin fallback, no inputs, no scoring columns, no weights; dummy prior 3.539 / 3.522 / 3.567, uniform 4.625 per fold; every fold holds all 102 classes. Same target, same 102 classes, same (release) class mix as the paper's evaluation | MET-1, MET-2, MET-5, MET-6, MET-11, MET-16
36 | task probes (stable LightGBM): dummy 3.542, drift 3.552, linear 0.772, RF 0.677, LightGBM 0.202, best single dst_ip 1.041; stock LightGBM diverged (24.7) | notes | probes/task/*.json, probes/task_default_lgbm/*.json; scratch/leak_probes_stable.py | holds | numbers match to 3 decimals; stock LightGBM 24.742 (macro AUC 0.517), its single-feature fit 21.8; the wrapper only sets min_child_weight 1.0 and learning rate 0.05 by setdefault; evidence.md lists "ran a model that diverged" (force_2020) as a probe-made flag; my own LightGBM (a3) lands at 0.190 on the shipped splits, the same range | EV-3, TP-1
37 | leak probes: 0.984 all, 0.966 without dst_ip, packet sizes alone 0.82-0.86, missing 0.582, format 0.649, no exact copies, 1-NN 0.546 / 0.749 / 0.040 | notes | probes/leak/*.json | holds, one nit | numbers match; over the probed features 1 of 1,500,000 test rows has an exact copy in its train side (same label); over all columns 0; the forced heavy check finds 0 duplicate rows in the frame | LEAK-16 to LEAK-21
38 | YouTube 6.5-7.0% on weekend days, 4.5-5.1% on working days from 2 November | notes (probe 13) | YouTube share per Prague day (all-flow counts) | PARTLY REFUTED, see R3 | weekend days 6.48-6.96%; working days 4.52-5.07% except Thursday 17 November: 6.35%, a weekend-like day (the Czech national holiday) | EV-7

The declared metric (MET-1 to MET-3), tested separately: see row 35. I looked once more for a primary metric: TMA
reports four metrics and names the trade-off; footnote 2 argues only that recall survives the sampling, not that it is
the criterion; DiB and the Zenodo page define none. MET-5 fallback holds; MET-11 (log loss over a macro AUC for a
multiclass task) holds; MET-3 not applicable (classes). Computable on every fold (MET-2).

IMPLIED CLAIMS
I1 | every kept feature exists at the prediction point and none derives from the SNI, UA or category (LEAK-10) | DiB Table 1 and 3.2 field by field; the first-packet test (row 10); SNI->class 1:1 (row 16) | holds | packet sizes/directions/gaps (PSTATS), whole-flow counters and histograms (PHISTS), end reason, version from the clear long header, ports, server address and its ASN (a lookup on the address): none is read from the decrypted ClientHello; dst_asn 36183 -> apple-privaterelay is an address property, not a label copy | LEAK-10, USE-6
I2 | the prediction point fits the use case | task_summary.use_case vs known | PARTLY REFUTED (R1) | bytes, packets, duration, the four whole-flow histograms and the end reason exist only at the export (after 65 s idle or the 5 min timeout); QoS priority and policy enforcement on that connection act before it | USE-1, USE-3
I3 | the split is the one the use case needs | splits_comment | holds, with two unchecked breaks (R2, R3) | temporal, each window trains on all earlier flows, no gap needed (row 33); SPLIT-14 Must over SPLIT-19 Should: weekly windows leave two windows below 50% (row 30) and the paper's design shares one train side (one evaluation) | SPLIT-14, SPLIT-19, SPLIT-20
I4 | the target is the real-world target | predicted | holds | the service from the record's own SNI by the authors' list, 1:1 per name; closed world (issue 2 already drafted) | USE-5
I5 | no row is a copy across the split | notes | holds | 0 over all columns (leak probe, heavy check); 1 of 1.5M over the probed features | LEAK-16
I6 | the record's "105 classes", "153M rows", "fit direct", "train on one week" | record Comments (AI screening) | superseded, not refuted | the definition measured and argued each departure: 102 (background, issue 2), 7.03M sampled task flows -> 2.5M shipped (version_comment), approximate with named gaps, 4-day windows (SPLIT-14); by EV-2 the later measured stage wins; the record has no assessment line saying so yet | EV-2, process

REFUTED OR INCOMPLETE, RANKED (validity first, Must first)

R1 (P3; USE-1 and USE-3, Must; wording) The use case names in-flow decisions at an after-the-flow prediction point.
   Claim: "labels each QUIC connection ... for quality-of-service priorities, usage policies and catching faked
   server names" (task_summary.use_case; TMA Sect. I) with "known: ... the bytes and packets each way, the duration
   and why the record ended; histograms of all packet sizes and gaps" (task_summary.known).
   Test: when do those inputs exist? DiB 3.2: the record is exported after 65 s idle or the 5 min active timeout, and
   "histograms are not limited to the first 30 packets". A QoS priority or a block on that connection is taken while
   it runs, before any of those exist. Catching a faked server name, per-service accounting and auditing usage
   policies can wait for the export. The task is the paper's (TMA IV-A1b uses all FLOWSTATS, the end reason
   included), so the data are right and only the decision named is off.
   Changes: nothing in the data; the use case and fit_reason. Mildest remedy: name the decisions taken at the export
   (per-service traffic reporting and policy auditing, catching faked server names, labelling for later flows of the
   same service), or say that QoS acts on the service's later flows. Not a leak: the column auditor reached the same
   point independently.

R2 (P4; SPLIT-20, Should) The first two days are a break in the collection, not only a volume dip.
   Claim: "the first two days ... hold about half the flows ... at every hour of the day ..., which the source does not
   explain; they are training history only" (notes, Anomaly; claims 28).
   Test: the release's own daily statistics (received, seen and saved per service) and the class mix per day.
   Result: the volume numbers hold, but the source's network-wide count halves too (total-received 27.9M and 28.2M
   against 70.2-75.8M on every later Monday and Tuesday), and the mix of services changes: Google 42.7 / 38.8% of the
   seen service flows against 57.5-64.0% on every other day, Meta 35.5 / 36.4% against 13.8-17.1%; total variation
   against the 2-27 Nov mix 0.30 / 0.29, against at most 0.113 on any other day (weekends 0.09-0.11). The sampling
   ratio of Google's services is unchanged (9.7 / 9.5 against 9.4-9.6), so this is not the sampling: some part of the
   network (a monitoring point or line, by inference) was not captured on 31 October and 1 November.
   Effect: those days are 5.3 / 6.7 / 7.8% of the shipped train sides (newest to oldest); dropping them moves the
   class prior's log loss by at most 0.0015 nats and the address lookup's by at most 0.001 (a4). The paper's week-1
   training included them.
   Changes: the note and the record, not the score. Mildest remedy: rewrite the Anomaly bullet with the source's own
   counts and the mix shift (keep, with the paper's precedent and the measured effect); the alternative, starting the
   history on 2 November, keeps the oldest window at about 57.7% of the service flows (above SPLIT-14's floor).

R3 (P4; SPLIT-20, Should) The oldest test window holds a national holiday and a bridge day.
   Claim: probe 13's "4.5-5.1% on working days from 2 November" (notes; claims 38), and the splits comment's silence
   on atypical days.
   Test: daily received counts and class mix from the release's statistics.
   Result: Thursday 17 November 2022 (Struggle for Freedom and Democracy Day, a Czech public holiday; calendar fact)
   had 23.4M received flows against 62.3-67.2M on the other Thursdays, YouTube 6.35% of service flows, and a
   weekend-like mix (total variation 0.111); Friday 18 November had 31.7M against 47.7-49.2M on the other Fridays.
   These two days are 42.1% of the oldest test window's rows (a3), and the window also holds a Saturday.
   Changes: nothing in the data (holidays recur and the operator meets them; the model trains on four weeks with
   weekends); the notes. Mildest remedy: one sentence in the splits comment and probe 13's bullet ("17 November,
   a public holiday, and 18 November look like weekend days"); the band in claim 38 then holds.

R4 (process and nits; no rule above P7 moved)
   - claims 14: "46 of the 102 services have saved < seen": strictly 77; 46 only at a 0.1% tolerance; 42 are
     sampled at 1:1.67 or more.
   - claims 23: the QUIC version names are not in the IANA registry; the quicwg "QUIC Versions" wiki confirms them.
   - claims 20 / notes: 57 task flows hold negative inter-packet gaps (to -4 ms), unmentioned (CLEAN-11; the column
     auditor proposes the fix); "59.2% under 30 packets" is 59.4% of the task flows.
   - claims 37 / notes "No test flow has an exact copy in its train side": 1 of 1.5M over the probed features
     (same label); 0 over all columns. Write "no copy over all columns".
   - builder report: "133 features" / "133 numeric inputs": 132 features, of which 4 categorical and 1 datetime.
   - record: the AI screening's 105 classes, 153M rows, fit direct and weekly split stand without an assessment
     line pointing at the definition's measured departures (EV-2: the later stage wins; issue 2 covers the classes).

N1 (P6; MET-2, MET-16, weigh; not refuted) The metric reason uses TMA footnote 2 as an argument about accuracy and
   F1, but log loss depends on the class mix just as much: the release's mix (entropy 3.55 nats; google-ads 7.1%)
   differs from the network's seen mix (2.95 nats; google-ads 13.3%). Scoring the release's mix is what the paper
   did (MET-2 holds) and DiB leaves the choice to the user ("whether to use the dataset's service distribution with
   softened imbalances or resample it back"); the fit_reason already names the gap. Mildest remedy: one clause in the
   reason ("log loss, like accuracy, depends on the mix; we score the release's mix as the paper did").

UNTESTED (and why)
   - Why 31 October and 1 November were captured partly: the source is silent; "a monitoring point or line missing"
     is inference (EV-2 rank 5) from the received counts and the mix.
   - That 17 November is a public holiday: a calendar fact, not from the source; the data agree (weekend-like counts
     and mix).
   - The hidden-group probe (the builder stopped it): not re-run; the address recurrence it targets was measured
     directly (row 24).
   - The exact Optuna/early-stopping criteria of the paper (validation "classification performance", metric not
     named): not knowable from the text; it does not change MET-5.
   - Each LightGBM comparison in rows 26 and 36 is one fit per window on 100k rows (mine and the builder's), not the
     tuned benchmark methods (EV-8).

work folder the agent's work folder (a1-a4 scripts and JSON, frame.parquet
and splits.npz: the shipped frame and splits, 0.3 GB, reusable by other panel agents).
```

</details>

<details><summary>Column audit: cesnet_quic22_service_classification</summary>

```text
COLUMN AUDITOR - cesnet_quic22_service_classification_1m (record cesnet_quic22_service_classification), 2026-11-09

Verdict: ship after small changes. No leak among the 132 features at the definition's prediction point (the flow
record's export); one P3 question on the use-case wording against that point; three small P7 cleaning items.

Sources read: dataset.py and README.md (df-large), the record, builder_report.md, the Data in Brief article
(paper/dib.txt, Table 1 and Sect. 2-3), the TMA 2023 paper (the agent's work foldertma.txt, Sect. IV-A1),
principles.md, use_case.md, leak_checks.md, cleaning_features.md. Measurements on the prepared 1-in-20 sample
(flows_sample.parquet, 7,026,437 flows of the 102 services) and the dtype probe (rerun: the agent's work folder: ,
1 of 131 flagged, dst_asn, the same as the builder's). Scripts in the agent's work folder; outputs in
the agent's work folder.

Count: the frame has 133 columns = 132 features + the target (README n_features 132). The builder report's "133
features" and "133 numeric inputs" are off by one and not all numeric (4 categorical, 1 datetime); the prompt
repeated the 133. 132 = 88 packet-sequence + 30 histogram + 8 counters + flow_end_reason + quic_version + src_port +
dst_ip + dst_asn + time_first.

PREDICTION POINT. curation_comments bullet 1: "the flow record is exported (idle 65 s, or 5 minutes of activity)".
At that point every kept column exists. The TMA paper's own inputs are the same (Sect. IV-A1b: "We use all FLOWSTATS
fields ...: bytes and packets in both directions, the duration of flow, and the flow export reason", plus "packet
histograms ... for each direction across the entire flow"), and tls_os_fingerprinting_masaryk_1m uses the same
export point with whole-flow durations (precedent). Against the prompt's "first 30 packets" point, the whole-flow
columns are NOT known: see finding 1.

COLUMN TABLE
(known at export = the definition's prediction point; "first 30" = known once the flow's first 30 packets are seen)

column | meaning (DiB Table 1 / Sect. 2; TMA IV-A1) | known at prediction? | dtype and cleaning | verdict | rule
service (target) | web service from the SNI via servicemap.csv, 102 classes | label, set at connection start | category, source's names | fine | CLEAN-25, USE-5
ppi_size_01 | UDP payload size of packet 1, the client Initial | export yes; first 30 yes | float32 bytes; 11 values in 7.0M flows (1250 87%... 1200, 1357, 1232, 1350, 1252, 1230, 1337, 1330): the client stack's padding target, not the SNI length (see finding 4) | fine | LEAK-10 (checked), USE-6
ppi_size_02..30 (29) | payload sizes of packets 2-30, missing past ppi_len | yes / yes | float32 bytes, 12-1472, no 0; missing = flow shorter (59% < 30 pkts), not the outcome | fine | CLEAN-26 by analogy
ppi_dir_02..30 (29) | direction, +1 client->server, -1 server->client (DiB 2.1, "encoded as +/-1") | yes / yes | float32 +/-1 only, missing past ppi_len | question (P7): a two-valued flag typed numeric; lossless either way | CLEAN-14 flag rule vs CLEAN-26 analogy
ppi_ipt_02..30 (29) | gap to the previous packet in ms (sum/1000 = ppi_duration to 2e-6 s) | yes / yes | float32 ms; 57 sampled flows (61 cells) hold negative gaps down to -4 ms: impossible | cleaning problem (tiny) | CLEAN-11
ppi_len | packets in the sequence, = min(30, packets+packets_rev) in 100% | yes / yes | int | fine | -
ppi_duration | time span of the sequence, s | yes / yes | float | fine | -
ppi_roundtrips | direction changes in the sequence | yes / yes | int | fine | -
duration | flow duration, s, to the export (idle or 300 s active timeout; 0.43% up to 360 s) | export yes; first 30 NO for the 39% of flows > 30 packets | float s | fine at export | LEAK-37
bytes, bytes_rev | bytes each way, whole flow | export yes; first 30 NO | int | fine at export | LEAK-37
packets, packets_rev | packets each way, whole flow (= sum of the direction's size bins, 100%) | export yes; first 30 NO | int | fine at export | LEAK-37
psize_bin2..8, psize_bin2..8_rev (14) | counts of packet sizes in log bins 16-31 ... >1024 B per direction, whole flow ("histograms are not limited to the first 30 packets", DiB 3.2) | export yes; first 30 NO (in flows > 30 pkts the forward histogram counts more packets than the sequence in 97%) | int32 counts, numeric | fine at export | LEAK-37, CLEAN-14
ipt_bin1..8, ipt_bin1..8_rev (16) | counts of gaps in log bins 0-15 ... >1024 ms per direction, whole flow (sum = packets-1, 99.97%+) | export yes; first 30 NO | int32 counts | fine at export | LEAK-37
flow_end_reason | idle timeout / active timeout / other (IANA IPFIX end reason; DiB 2.2) | export yes; first 30 NO | category of 3 from 3 exclusive flags (asserted one per row: CLEAN-13 lossless) | fine at export; depends on the service through connection length (active 0.45% overall, 5.8% chrome-remotedesktop, 5.1% instagram, 4.5% apple-privaterelay), not through the label | LEAK-37, USE-6, CLEAN-12/13
quic_version | version from the clear long header (DiB 2: "extracted handshake fields"), decimal -> hex | yes / yes (header is not encrypted) | category 0x1, 0xfaceb002, 0xff00001d, 0xfaceb001, 0xfaceb00e; no missing | fine | CLEAN-12, CLEAN-14
src_port | client UDP port | yes / yes | numeric; 1-65535 (raw min 7); no port with >= 20 flows maps to one service (0 of 43,741); ranges carry OS/NAT (49152+ for Apple/Windows, 10400-10402 a cluster) | fine | CLEAN-14 (precedent tls_os_fingerprinting_masaryk_1m)
dst_ip | server address, IPv4/IPv6 (3.4% v6), public | yes / yes | category, 5,702 levels in the frame | fine (question noted) | CLEAN-14, USE-6; issue 1 of the builder
dst_asn | server's autonomous system number | yes / yes | category, 336 levels, 53-65535; ASN 65535 (reserved) on 1 sampled flow (snapchat), 0 / 23456 / private none | fine; 65535 a proxy value at most once | CLEAN-14 (probe flag numeric_levels answered: a network code), CLEAN-10
time_first | timestamp of the first packet, release UTC, shipped Prague (UTC+1) naive | yes / yes | datetime; shift verified (finding 6) | fine | CLEAN-14

Dropped, checked: QUIC_SNI (label source, LEAK-10), QUIC_USERAGENT (decrypted Initial, 0.2%), CATEGORY (function
of the label), ID and SRC_IP (CLEAN-3; SRC_IP is also a user identity), TIME_LAST (= time_first + duration to 30 us;
also post-start), PROTOCOL (17) and DST_PORT (443) constant by the authors' filter, ppi_dir_01 (+1) and ppi_ipt_01 (0)
constant, psize_bin1 and psize_bin1_rev (no payload < 16 B; 6 sampled server counts of 1-3, none shipped). All
right; nothing kept that the dropped fields encode (TIME_LAST - TIME_FIRST is duration, kept as a feature by its own
meaning).

PROBLEMS, RANKED (principles.md: validity P3/P4 first, then P7)

1. P3 question for the curator (USE-3, weighing; no leak): the use-case text does not match the prediction point.
   The prediction point is the flow record's export (65 s idle or 300 s active), and at that point every column is
   known (LEAK-37 holds: the spans end at a timeout, not at the label). But task_summary.use_case names
   "quality-of-service priorities, usage policies", which act while the connection runs, so before export. Those
   need the "first 30 packets" point, and there 45 inputs do not exist yet for the 39% of flows longer than 30
   packets: duration, bytes, bytes_rev, packets, packets_rev, flow_end_reason and all 30 histogram bins (the DiB:
   "histograms are not limited to the first 30 packets"; in 97% of flows over 30 packets the forward histogram counts
   more packets than the sequence shows).
   How much it matters (LightGBM, 250 trees, 150k training flows before 24 Nov, 60k test flows 24-27 Nov from the 1-in-20
   sample; the agent's work folder: first30_vs_export.json): with the address, all inputs score log loss 0.162
   (95.3% accuracy) and first-30 inputs 0.191 (94.4%); without the address, 0.441 (87.8%) against 0.514 (85.9%).
   The whole-flow block is worth 0.03 to 0.07 in log loss, with the paper's own inputs (TMA IV-A1b uses FLOWSTATS,
   end reason and histograms included) and the precedent tls_os_fingerprinting_masaryk_1m (same export point).
   Mildest remedy: (a) keep the export point and reword use_case to labelling of exported flow records (reporting,
   capacity planning, policy audits, catching faked server names afterwards), dropping "quality-of-service
   priorities" (a text change only); (b) a first-30-packets framing that drops the 45 whole-flow columns (closer to
   in-line QoS, departs from the paper's inputs). Recommendation (a).

2. P4, checked, no leak (LEAK-10): no column still carries the SNI or the user agent. ppi_size_01, the client Initial
   with the SNI in it, takes only 11 values over 7.0M flows: QUIC pads the Initial to the client stack's target
   (1250 Chrome on version 1, 87%; 1200; 1357; 1232/1252/1230 mvfst; 1350 draft-29). Within google-www (SNI lengths 13
   to 25) and youtube (11 to 33) the median is 1250 at every length; the correlation with SNI length is -0.03 and -0.01.
   Spotify's -0.57 comes from its client mix (app versus web), not from the length. Size_01 identifies the client
   stack, which the monitor sees in the clear (USE-6). The user agent (0.2%) is gone, and its flows share the
   same padded sizes. The server certificate's size (packet ~5, TMA Fig. 2) is a clear-text side channel the paper
   relies on; it is not a leak.
   flow_end_reason depends on the service only through connection length (active timeout 0.45% overall, 5.8%
   chrome-remotedesktop, 5.1% instagram, 4.5% apple-privaterelay). It is known at export and is a paper input, so
   not LEAK-10 or LEAK-37. Every record begins with a client Initial (all ppi_size_01 >= 1200), so no
   active-timeout continuation record sits without its handshake.

3. P7 question (CLEAN-14 flag rule against CLEAN-26 by analogy): ppi_dir_02..30 hold only +1 and -1 (plus missing
   past the length) and ship as float numbers. By CLEAN-14's table a two-valued flag is a category. The source and the
   paper encode it as the number +/-1 (DiB 2.1; TMA IV-A2 "no need to standardize"), and as the channel of a
   sequence it parallels a spectrum's numeric positions. Both forms are lossless. Mildest remedy: keep numeric and
   write it as an exception to CLEAN-14 in the notes (fact: a channel of a published packet sequence, encoded +/-1 by
   the source; serves CLEAN-26 consistency, pending the PacketSequence special kind the builder proposes). The
   current bullet calls it "as published" but does not name the departure.

4. P7 cleaning (CLEAN-11): negative inter-packet times. 57 of 7,026,437 sampled flows (61 cells in ppi_ipt_03..30,
   down to -4 ms; README shows -3 in ppi_ipt_05 and -1 in ppi_ipt_09 of the shipped frame). A gap cannot be
   negative (most likely capture reordering across exporter threads). Remedy: set ipt < 0 to missing (or 0, with
   the source's reason) and add a guard count. About 20 rows in the shipped 2.5M. They lean to Facebook services
   (28 of 57), but the count is too small to matter as a class artefact.

5. P7 small (CLEAN-10): dst_asn 65535 (reserved; most likely a failed lookup) on 1 sampled flow (snapchat); 0, 23456
   and the private range do not occur. Remedy: set to missing, or leave it with no change; negligible.

6. P7 count error in the writing, not the data: the builder report says "133 features" and "133 numeric inputs".
   The frame has 132 features + the target, 5 of them non-numeric (dst_ip, dst_asn, quic_version,
   flow_end_reason, time_first). The README (n_features 132) is right. Remedy: fix the report and REVIEW.md wording.

ANSWERED, NO CHANGE
- dst_ip as a category (5,702 levels in the frame, 8,255 in the sample, 3.4% IPv6), against CLEAN-14's "string for
  high-cardinality values": the string type means text to embed, and an address is a lookup key with no words in it.
  CLEAN-14's table types "a code with no words (an id...)" as a category, and zillow_prize's census_tract (3,030 levels)
  is a precedent. 99.9% of test flows hit a known address. Category is right; the notes could name the departure
  from the "high-cardinality string" wording. Splitting the address into a /24 prefix (CLEAN-12 "ids that encode a
  group") is not needed: dst_asn already gives the network, and the paper found prefix matching weak. Whether the
  address belongs at all is the builder's issue 1 (a weighing call under USE-6, not a leak). I agree it is no label
  construction.
- dst_asn as a category: the dtype probe's numeric_levels flag is answered. An AS number is a network code without
  order (CLEAN-14 code rule).
- src_port numeric: no port with 20 or more flows maps to a single service (0 of 43,741), and its ranges carry
  OS/NAT meaning (49152 is the start of the IANA dynamic range; 10400-10402 is a cluster on Cloudflare-hosted
  services). Matches the tls_os_fingerprinting_masaryk_1m precedent.
- quic_version: the hex codes are right (0x1 = v1, 0xff00001d = draft-29, 0xfaceb001/2/00e = mvfst); none missing.
- UTC to Prague: right. Each daily file holds flows from about 22:55 UTC of the previous day, cut at 23:00 UTC
  (export time) = local midnight CET. Summer time ended 30 Oct 2022 01:00 UTC, before the first flow (30 Oct 22:55
  UTC), so UTC+1 holds for all flows. Note that the files are cut by export time, so the shipped Prague day is by
  first packet, as the windows need.
- Dropped columns: all correct; see the table. TIME_LAST adds nothing beyond duration.
- Histogram bins and counters: numeric counts, consistent (size bins sum to packets in 100%, gap bins to packets-1
  in at least 99.97%); psize_bin1 dropped as a constant, ipt_bin1 kept (it varies).
- ppi_duration exceeds duration by more than 1 ms in only 8 flows (the builder's note); the rest is rounding.
```

</details>

<details><summary>Split audit: cesnet_quic22_service_classification</summary>

```text
SPLIT AUDIT: cesnet_quic22_service_classification (folder cesnet_quic22_service_classification_1m), 2026-11-09

VERDICT: right with notes. Temporal, three 4-day windows (16-19, 20-23, 24-27 Nov 2022), expanding history, no gap,
row budget 1M train / 500k test. The regime, the window length, the gap and the sampling hold up under measurement.
Three notes belong in the definition's text; nothing needs a re-split.

Work: scripts and outputs in the agent's work folder (a1.py: sample fidelity, rare classes, cutoff straddlers,
daily counts; a2.py, a3.py: first two days and sampling ratios; alt.py / alt.json / alt.log: alternative histories).
Data: flows_sample.parquet (the 1-in-20 sample), flow_counts.parquet (all 140.47M service flows per hour), and the
release's per-day stats JSONs (meta/cesnet-quic22/W-*/), which also give the flows received on the network before
labelling and the per-service seen/saved counts.

---------------------------------------------------------------------------------------------------------------
CHECKS THAT HOLD
---------------------------------------------------------------------------------------------------------------
A. Regime (SPLIT-1, SPLIT-13, USE-10): right. A monitor labels new flows to servers it has seen: 99.9% of a window's
   flows go to an address seen before it (builder probe). The recurring server is part of the operator's task, not
   a cold start. A grouped split by server would test a question the use case does not ask.
B. Train shares (SPLIT-14): checked against the all-flow counts: the train sides hold 83.8M, 97.5M and 123.3M of
   140.47M service flows, i.e. 59.7%, 69.4% and 87.8%, which matches splits_comment. Each window has its own
   expanding train side (SPLIT-11).
C. Weekly windows (SPLIT-14 over SPLIT-19): agreed. The paper's weeks give 21.4% / 49.2% / about 71% train
   shares, so only one window is above the floor. The 2026-11-08 amendment (two windows above 50% plus one at 40% or more) does not
   rescue it either. The paper's own design (one model on W-44, tested on W-45 to W-47) shares a train side across
   windows, which SPLIT-14 calls one evaluation. Measured at 60k train flows on the 24-27 Nov window: training on
   W-44 only gives log loss 0.303 (acc 0.916), against 0.225 (acc 0.937) for all earlier flows. Following the paper
   would score a stale model and mostly measure drift.
D. Gap (SPLIT-10): none needed, agreed. The label is the SNI of the flow's own first packet, known at export.
   The only training labels not known at a cutoff come from flows that start before it and are exported after it
   (the active timeout is up to 5-6 min). In the sample that is 27, 12 and 25 flows out of 4.19M, 4.88M and 6.17M
   (at most 0.0006%). A one-day gap would cost a day of history for nothing.
E. Hash sample keeps the class shares per window (asked): the 1-in-20 SplitMix64 sample against the full counts,
   chi-square over 102 classes, gives p = 0.354 / 0.607 / 0.993 on the test windows and 0.49 / 0.32 / 0.55 on the
   train sides (largest |z| 2.9 / 2.2 / 1.9 test, at most 3.65 train). The sample-to-full ratio is 19.992. The
   500k test cap and the 1M train draw are stratified on the service in the protocol, so the shares carry through.
F. Rare classes per window (TP-8): no class is missing from any window's sampled pool (the rarest are livescore
   with 21 of 684k in W1, uber 59 of 1.29M in W2, uber 41 of 860k in W3). Expected counts in the shipped 500k test
   windows: livescore 13.3 (16-19 Nov), uber 20.3 (20-23), uber 24.0 (24-27). All are above TP-8's 5 per fold. The
   probe's few_minority flag comes from its 100k cap. Keep the rare classes, as the builder proposes. Small
   correction: the builder's "about 15" for the oldest window is 13.3 by the full counts.
G. SPLIT-21: the windows were not chosen from a score comparison (they follow from the floor). Fine.

---------------------------------------------------------------------------------------------------------------
NOTES (ranked by principles.md; all P4 honest evaluation, none a Must breach)
---------------------------------------------------------------------------------------------------------------
1. Season-shaped windows: each 4-day window has a different weekday mix, and the oldest one is mostly holiday
   (SPLIT-20 "check whether the newest windows fall in an atypical season"; SPLIT-12).
   Evidence:
   - 17 Nov 2022 (Thursday) is a Czech public holiday (Struggle for Freedom and Democracy Day). Its volume is that
     of a Sunday: 2.47M service flows, against 7.4M on the Thursdays of 10 and 24 Nov. Friday 18 Nov is also low
     (3.31M against 4.97M / 5.08M on the other Fridays), probably bridge days at universities and schools, the
     network's users.
   - Share of a window's flows on weekend, holiday or bridge days: 16-19 Nov 55.9%, 20-23 Nov 9.6%, 24-27 Nov 29.4%,
     against 12.5% in a normal week (7-13 Nov).
   - The class mix of the holiday differs from the following Thursday by TV 0.133. Same-weekday pairs a week apart
     usually differ by 0.02-0.05.
   - The score depends on the day type: per-day log loss at 60k train flows is 0.20-0.21 on 17 and 19 Nov against
     0.23-0.24 on workdays, and 0.18-0.20 on 26-27 Nov against 0.22-0.24 on 24-25 Nov. So the window means move by
     about 0.01 with their day mix. That is small next to the 0.20 vs 0.51 address effect, but no window is a
     typical week.
   Rule: SPLIT-20 (Should), SPLIT-12 (Should). A 7-day window would fix the cycle but fails SPLIT-14 (Must), so
   the 4-day windows stay.
   Mildest remedy: a note in splits_comment naming the holiday (17 Nov) and the low 18 Nov in the oldest window,
   and the weekday mix of the three windows. No re-split: any 4-day tiling has unequal day mixes, and shifting the
   windows by a day still puts the holiday in one of them.

2. The first two days (31 Oct, 1 Nov) are a collection artefact, not a quiet period (asked).
   Evidence:
   - The release's stats count all QUIC flows received on CESNET2 before labelling and sampling: 27.9M and 28.2M on
     those days, against 70.6M and 71.6M on 7 and 8 Nov. By hour, 31 Oct is 0.38-0.62 of 7 Nov at every hour. A
     real holiday would follow a weekend profile instead (31 Oct and 1 Nov are no Czech public holidays).
   - The service mix before sampling also differs: TV 0.263 between 31 Oct and 7 Nov, against 0.014 between 7 and
     14 Nov. After sampling it is 0.31 and 0.29 (Tuesday pair) against 0.02.
   - The largest movers: snapchat seen at 4% of its 7 Nov level, unitygames 10%, kaggle 12%. Instagram and the
     Facebook services go up by 3-5 points of share, the Google services down.
   This matches part of the five monitoring points or peering lines missing, since a single line carries a skewed
   population. The data article says nothing about it.
   Effect: only training history. Removing the two days from the 16-19 Nov window's history changes nothing
   measurable (log loss 0.224 with, 0.226 without, 60k train flows).
   Rule: SPLIT-20 (Should: check the history for a break in the data collection); PROV-3 at most as a note.
   Mildest remedy: keep the rows and reword the curation_comments "Anomaly" bullet. It should state that the flows
   received before labelling are also halved at every hour, and that the class mix is shifted by TV 0.26 (snapchat
   at 4%), i.e. a partial capture. No filter is needed.

3. The class mix shifts across windows partly because of the authors' sampling, not the network.
   Evidence: the data article (Sect. 3.4) updates the per-service sampling ratios every five minutes. 22 of the 102
   services change their daily seen/saved ratio by more than 5% over the month, for example:
   - discord 6 -> 4 and snapchat 4 -> 6 from 7 Nov,
   - openx 3 -> 4 from 14 Nov,
   - facebook-rupload 3 -> about 2 from 21 Nov, which falls inside the test period.
   A model trained on earlier weeks meets these prior shifts as if they were drift. fit_reason already names the
   softened mix, but not that it changes over time.
   Rule: USE-1 and USE-8 gaps (Should), plus the split's honesty (P4).
   Mildest remedy: one sentence in fit_reason or in the metric note. The per-day seen counts ship with the release
   if a curator wants the network's mix instead (MET-16 keeps the unweighted score).

---------------------------------------------------------------------------------------------------------------
FOR INFORMATION (no action)
---------------------------------------------------------------------------------------------------------------
- History length: on the 24-27 Nov window at equal training size (60k), training on the 4 days just before gives
  log loss 0.210, all earlier flows 0.225, and W-44 only 0.303. Recency matters, which a participant may exploit
  through time_first, a shipped datetime feature. SPLIT-21 forbids picking the history from this comparison, and
  the expanding history is what a refit sees (SPLIT-11, SPLIT-20). No change.
- The per-day results above use one LightGBM per design (200 trees, address and network as categories, hour and
  weekday from time_first) and a fixed 100k test draw per window. They are a single fit each, not a tuned score.
```

</details>

<details><summary>Domain practitioner: cesnet_quic22_service_classification</summary>

```text
DOMAIN PRACTITIONER - cesnet_quic22_service_classification_1m (record cesnet_quic22_service_classification)
Actor: the flow-monitoring team of a backbone operator (CESNET's own, or an ISP). The ipfixprobe probes export
bidirectional flow records (65 s idle / 300 s active timeout) to a collector. There I label each QUIC flow with the
service behind it, because the SNI goes away once Encrypted Client Hello arrives and because decrypting the QUIC
Initial packet at 100 Gbps is costly. I use the labels for usage reporting and policy accounting, to spot faked SNI,
and (the paper also names this) for QoS.

VERDICT
Fit: approximate (I agree with the definition). The rows, inputs and SNI labels are what my collector holds when a
flow record arrives. But the test is a closed world of 102 services, scored on a class mix the collection itself
softened, and the whole-flow statistics only exist when the record is exported. So the task fits reporting and SNI
auditing, not inline QoS.
Metric: partly. Log loss (fallback, MET-8) scores the probabilities that both my reject threshold and my per-service
volume estimates need. But it is scored per flow on the softened mix of the release, which the source itself says
does not carry over to the network (TMA footnote 2), and no "unknown" outcome exists to score. I would pick a model
by per-service (macro) recall plus a calibrated probability, in a single number a class-balanced log loss. See Q5.

Q1 INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
- Have, at the first 30 packets: the packet sizes, directions and gaps (ppi_*), ppi_len/duration/roundtrips, the QUIC
  version, the client port, the server IP and ASN, and the start time. All are in the clear on the wire.
- Have only at export (idle 65 s or active 300 s after the flow starts): bytes/packets both ways, duration, the four
  full-flow histograms, and the end reason. My collector classifies exported records anyway, so this is legitimate
  for monitoring, accounting and SNI auditing (USE-3 holds for that moment). But the task_summary also lists
  "quality-of-service priorities". A router that sets a QoS priority acts within the first packets and would not have
  these columns. The TMA paper's models use the same FLOWSTATS (LightGBM leans on them heavily, TMA Fig. 3), so this
  matches the source. Suggest dropping QoS from use_case or naming the moment ("on the exported flow record").
- Server address and ASN (issue 1): yes, I would use them. IP lists are standard operator practice. The paper builds
  its own IP baseline (68.68% accuracy, 98-99% provider accuracy) and names an ensemble as future work (Sect. VII).
  So I back option (a), keep both (USE-6). What makes me distrust a model that leans on the address: CDN-hosted
  services move (alza-www, mentimeter and kiwi-com fell to 0% recall in the IP baseline within the month, TMA
  Table III). Under ECH, many services sit behind shared front IPs (Cloudflare), so the address will be worth less
  than in 2022. The temporal windows catch part of the first effect. The notes should say the second is a 2022 view.
  Option (c) (drop both) is a different and harder benchmark (log loss 0.51-0.54 against 0.19-0.20), the "pure side
  channel" research task. It is not my deployment.
- What I always have and the table lacks: the SNI itself for every non-ECH flow (correctly dropped, LEAK-10; it is
  the label), the client's anonymised prefix (which institution; dropped under CLEAN-3, minor), and the DNS answers
  my resolvers gave the client just before the flow. Operators use DNS correlation heavily, but it is not in the
  release, so this is out of scope. Nothing the table holds is unknowable at export.

Q2 TARGET (USE-5)
- The service from the SNI-to-service map is what I act on (reporting, policy). The map is hand-built (vendor
  docs, Netify, handpicked). That gap is acceptable and named.
- I would want a probability per service. I accept or reject on its maximum (CESNET's own line of work is
  "classification with reject option", Luxemburk & Cejka 2023, cited in the data article), and summed probabilities
  give my per-service volume estimates. A class alone is not enough.
- Errors inside one provider (Google Search vs Google Docs) cost me less than errors across providers. The paper's
  provider-level accuracy measures exactly that. No cost matrix is given, so I would not invent one (MET-7).

Q3 ROW, TEST DATA
- One row = one exported flow record = one labelling decision of mine. Yes.
- The biggest gap is issue 2, background traffic. The 102 services cover 84% of CESNET2's QUIC traffic (data
  article Sect. 3.1). The other 16% (Google background, Facebook background, default background) is in every hour I
  classify. A closed-world model forces each of those flows into one of the 102 services, so the benchmark overstates
  what I would see. The data article's "Value of the data" bullet names exactly this use (OOD / open-world), and
  CESNET DataZoo has an "explicit unknown" option for these classes. My preference: option (b), the three
  background classes as labels (105 classes, as the record first stated). A supervised "other Google / other
  Facebook / other" class is how I would deploy it, and it keeps the provider information. Option (c), one merged
  "other" class, is also fine. Option (a) is defensible only as "the paper's task". Then fit_reason must keep saying
  this, as it does now. Background makes up 8.3% of the release after sampling, which is modest extra size.
- Class mix: the release samples each service at its own rate (top 5% at 1:15, bottom 60% unsampled, background at
  1:15, ratios updated every 5 minutes). The test windows therefore do not show the class mix I face. The release
  ships the pre-sampling counts. Rank 2 gap. It does not change what a model must learn (the posterior up to a prior
  shift), but it changes which errors the score weighs (see Q5).
- Time: three 4-day windows, trained on everything earlier. This is closer to my practice than the paper's design
  (train on week 1, test weeks 2-4). I would refit every few days on SNI-labelled flows, and the paper shows why:
  Google's certificate change drove a 30-point recall drop on Google services within a week (TMA Fig. 5; LightGBM
  week 2 to 3: 87.3% to 77.9% accuracy). One point differs from my practice. The train side is a uniform random 1M
  of all earlier flows, while I would favour recent days (DataZoo supports recency-weighted train dates). That is a
  user's training choice, not a data gap. One network: right for CESNET's own team, and it does not transfer to
  another ISP (named in fit_reason).
- Is a model trained on one week still valid weeks later? Not reliably, as the paper shows. A benchmark whose
  windows refit on all history tests the setting I would actually run. Good.

Q4 WOULD I USE IT
- Yes, as a labeller of exported records for reporting and auditing, with a reject threshold. I would trust it
  given: per-service recall per window (the paper's Table III style), calibration (my volume estimates are sums of
  probabilities), stability across the three windows, and provider-level accuracy above about 98%. I would distrust
  it if: the address carries the whole score (CDN moves), it behaves unknowably on background traffic (it is not in
  the data), or the Google services collapse after a certificate change.

Q5 METRIC (MET-1, MET-6 to MET-9, MET-16)
- Declared: Metric.fallback, log loss, unweighted, on the release's softened mix. The source reports accuracy,
  provider accuracy, macro F1 and macro recall with no threshold or cost (MET-6), so the fallback is consistent with
  the rules (MET-8). Log loss also suits my needs: a reject threshold and summed volume estimates both need
  calibrated probabilities, which a strictly proper rule rewards.
- Where it misses my decision. Per-flow log loss weighs services by their softened share, an artefact of the
  collection: neither one vote per service (what I monitor) nor the network's true mix (what I account for). The
  source itself says only recall carries over to the real network (TMA footnote 2), and the paper's ranking flips by
  metric (LightGBM has higher accuracy, mm-CNN higher macro recall, Sect. V). So a per-flow score on this mix can
  pick a different model than per-service recall would.
- What I would choose. As a proper score, log loss with each service weighted equally (every flow weighted 1 over
  its service's test count). It is invariant to the per-service sampling ratios, as macro recall is, and still
  scores probabilities. The rules do not cover this yet: MET-16 rules out design weights for scoring unless the use
  case is a population estimate, and this is no unit weight (MET-17). So I raise it as a weighing call for the
  curator, not a rule violation. Second choice: keep plain log loss and report macro recall (and provider accuracy)
  next to it in the notes as the source's deployable measure. I would not use multiclass ROC AUC (MET-11 note; it
  saturates at 0.998). I would not use accuracy alone either: it depends on the softened mix (footnote 2) and on an
  argmax with no reject.
- Verdict: partly.

GAPS RANKED BY HOW MUCH THEY CHANGE THE TASK
1. Background flows dropped (closed world of 102), while about 16% of the QUIC traffic I classify is background
   (issue 2; USE-5, USE-8). Prefer (b) 105 classes or (c) one "other". If (a) stays, keep it named in fit_reason
   (it is).
2. The scored class mix is the release's per-service sampling, not the network's (USE-8 gap, named). It interacts
   with the metric (above).
3. The prediction point is the exported record (up to 65-300 s after the flow starts): full-flow stats and end
   reason are not available for inline QoS. Reword use_case or name the moment (USE-3).
4. The server address dominates (log loss 0.19 with it vs 0.51 without). This is legitimate for me (USE-6, issue 1:
   keep (a)), but it is a 2022, pre-ECH, CESNET-specific advantage. Say so in the notes.
5. One network, one month, uniform-random training history. Minor: right actor, and the refit cadence is plausible.

WHAT A DOMAIN EXPERT WOULD CHANGE
- Add the three background classes (or one "other") so the test window holds the traffic the classifier meets.
- Drop "quality-of-service priorities" from use_case, or say the label is set on the exported flow record.
- Report macro recall per window and provider-level accuracy in the notes next to the log loss. Consider equal
  per-service weighting of the log loss.
- Keep dst_ip and dst_asn as categorical keys (not text). Note that the address's value is pre-ECH and shrinks as
  services move behind shared CDN fronts.
- Optional: the per-service sampling ratios (servicemap / stats JSON) as a scoring-only reweighting to the network's
  mix if the curator wants the deployment mix. MET-16 currently says unweighted. Flag only.

SOURCES
- Luxemburk, Hynek, Cejka, "Encrypted traffic classification: the QUIC case", TMA 2023 (run folder paper/tma2023.pdf,
  text in the agent's work foldertma.txt): Sect. I (motivation: SNI faking, ECH, QoS, usage policies), Sect. IV
  (metrics and footnote 2), IV-C (IP baseline), Tables I-III, Fig. 5, Sect. VI (drift within a week).
- Luxemburk et al., "CESNET-QUIC22", Data in Brief 46:108888 (2023) (paper/dib.txt): Value of the data (OOD, background
  classes), Sect. 3.1 (84% coverage, background classes), 3.2 (timeouts), 3.4 (per-service sampling).
- CESNET DataZoo paper, arXiv 2310.19568 (https://ar5iv.labs.arxiv.org/html/2310.19568) and docs
  (https://cesnet.github.io/cesnet-datazoo, https://cesnet.github.io/cesnet-datazoo/datasets_overview): explicit-unknown
  open-world option for QUIC22's background classes, time-aware splits with recency weighting.
- Zenodo record https://zenodo.org/record/7409923.
- Rules: use_case.md USE-1, USE-3, USE-5, USE-6, USE-8; metrics.md MET-1, MET-6, MET-7, MET-8, MET-11, MET-16, MET-17.
```

</details>

<details><summary>Blind review: cesnet_quic22_service_classification</summary>

```text
BLIND REVIEW: cesnet_quic22_service_classification
Inputs used: clean_room/data.parquet, clean_room/task.md, Zenodo record 7409923, Data in Brief article (PMC9851865 mirror; the
Elsevier DOI page returned 403), CESNET DataZoo feature docs (cesnet.github.io/cesnet-datazoo/features). The TMA 2023 PDF
downloaded but could not be text-extracted (no PDF tool), so it was not read.
Incidental: while stopping my own wait loops, `pgrep` listed command lines of other agents' processes (paths of other datasets'
runs). I did not open or use any of them.

VERDICT: Include with changes. It is a real, large, well-known encrypted-traffic task with signal and a sound temporal split, but
the server-address columns turn a large part of it into a lookup of the destination IP, and the class mix is set by the
curators' sampling.

WHAT THE TASK IS
CESNET-QUIC22: QUIC flows captured on the Czech national research network, 31 Oct to 27 Nov 2022 (153M flows in total). Target
`service` is one of 102 web services (google-www, youtube, instagram, ...). The label comes from the SNI domain:
"The created SNI-service mapping was used for assigning labels to the captured flow data." A network operator (ISP or
enterprise) predicts it for monitoring, QoS or policy when the SNI is not visible (ECH or encrypted ClientHello). The features
are flow statistics, the first 30 packets (sizes, directions, inter-packet times), packet-size and IAT histograms, and the
server IP, ASN, client port and QUIC version. This is a real and widely studied use. Prepared: 2.5M rows x 133 columns
(I saw a 200k sample), with 3 temporal test windows on time_first.

CONCERNS, MOST TO LEAST SERIOUS

1. Server address columns (dst_ip, dst_asn, also src_port) are kept as features. The task becomes mainly an IP lookup. [major]
   Evidence: dst_ip is a 2,052-level categorical in the sample. Taking the most frequent service per dst_ip gives 0.697
   row-weighted purity. On my temporal check (train before 2022-11-21, 123,854 rows; test from 2022-11-21, 76,146 rows), only
   0.74% of test rows have a dst_ip not seen in training. A pure train-set IP->majority-service lookup scores 0.681 accuracy on
   the test week. LightGBM (400 trees, lr 0.05) on all columns: acc 0.948 / macro-F1 0.868. Without dst_ip, dst_asn and
   src_port: acc 0.869 / macro-F1 0.654. The CESNET DataZoo docs list DST_IP, DST_ASN, SRC_PORT and QUIC_VERSION under "Other
   fields" (auxiliary, returned only with return_other_fields), not among the flow statistics or packet features used as model
   inputs. Server IPs are a real signal operators use. But with 2,052 levels (more in the 2.5M version) and the test weeks
   reusing nearly the same IPs, the benchmark would mostly reward high-cardinality categorical handling, and the label (from
   the SNI) is nearly a function of the IP for many services. src_port is the client's ephemeral port (1025 to 65535; per-class
   medians 46k to 57k) and should carry no service signal. Any signal it does carry is an OS or client artefact.
   Change: drop dst_ip and src_port. Either drop dst_asn or keep it deliberately and document it. Keep quic_version, since it is
   in the cleartext header (0xfaceb00x appears only on Facebook/Instagram/WhatsApp rows), but say so. Or publish both variants.

2. The class distribution is set by the curators, not by real traffic. [moderate]
   Source: "Each service is sampled at a different ratio, depending on the amount of traffic". Top services were sampled at
   1:15 and the bottom 60% were not sampled at all. The three background classes (Google Background, Default Background, and
   one more) are missing here: 102 classes, all of them named services. So this is a closed-world task with a reweighted
   prior. Accuracy and log-loss do not reflect deployment frequencies. That is acceptable for a benchmark, but document it.
   Rarest classes in the sample: uber 9, fitbit 13, alza-identity 13. In the 2.5M version they have about 12x more rows (my
   extrapolation), so they are scoreable. Report a macro metric alongside accuracy.

3. The time distribution of the subset does not match the source. [moderate, unverified cause]
   Share of rows by ISO week in the sample: W44 14.2%, W45 18.7%, W46 29.0%, W47 38.1%. Source flow totals give 21.3%, 27.8%,
   22.0%, 28.8%. 2022-11-16 alone has 17.6k of the 200k rows, against about 7k on the days around it. Possible causes: removal
   of the background classes, per-class balancing, or uneven sampling of files. task.md does not describe how the 2.5M rows were
   drawn from the 153M. Change: document the subsampling, and check that it does not leak time trends into the label prior
   (for example, later weeks over-represented).

4. Flow-level statistics are only known at the end of the flow. [minor]
   duration (up to 359 s), bytes, packets, flow_end_reason and the histograms are known only after the flow ends. The first-30-
   packet features are known early. This is fine for post-hoc traffic accounting, but it is not early classification. No column
   is computed from the label: the SNI and user agent are correctly excluded, and time_last is absent. Consistency checks pass:
   the non-null PPI count equals ppi_len on 100% of rows, and packets >= ppi_len always.

5. Preparation details. [minor]
   time_first is a datetime column in the table. Make sure the harness uses it only for splitting, not as a feature. 3 rows
   fall on 2022-10-30 (a timezone edge before the 31 Oct start). ppi_ipt_01 and ppi_dir_01 were dropped (constant), and so was
   psize_bin1, which is fine. The PPI missing values (up to 59.5% at position 30) are structural (the flow was shorter), so they
   are informative, which is fine for GBDTs. The ppi_dir_* columns are float ±1 with NaN. They could be int or categorical, but
   it is harmless. The data has 90 near-sequential PPI columns, which favours sequence models. Tabular methods still do well.
   No exact duplicate feature rows in the sample (0).

6. Ceiling and difficulty. [minor]
   Even without the address columns, a default GBDT reaches 0.87 accuracy. Macro-F1 of 0.65 leaves room for better methods,
   so the task is not trivial. With the address columns it is near-saturated on accuracy (0.95).

WHAT I COULD NOT CHECK
- The 2.5M-row prepared table and the exact 3-window split boundaries. I saw only the 200k sample and made my own single cut.
- The TMA 2023 paper text (PDF not extractable here), so I could not confirm the authors' own feature choices or results.
- How the 2.5M rows were drawn, and whether background classes were removed on purpose.
- Whether servicemap.csv maps any SNI domains to several services. I did not download the raw data.
- Model numbers are from a single LightGBM configuration, without tuning or seeds.

Scratch: the agent's work folder: m.py, m2.py (m.py's first lr=0.1 config diverged to acc ~0.10, so I disregarded it).
```

</details>

<details><summary>Task gamer: cesnet_quic22_service_classification</summary>

```text
TASK GAMER REPORT - cesnet_quic22_service_classification (log_loss, lower is better, 102 classes, 3 temporal windows)

Verdict: one real flaw - the shipped features include whole-flow statistics and packet histograms that exist only
after the flow has ended, well past the stated prediction point (first 30 packets); they lower log loss by about
0.04-0.05. Nothing else (row order, copies, test-window statistics, formats, identifiers) gains beyond noise.

Setup. LightGBM multiclass (lr 0.1, 31 leaves, max_bin 63, min_sum_hessian_in_leaf=1 - the default diverges
to log loss ~33 on rare classes), early stopping on the latest 10% of the training sample, 4 threads.
SUBSAMPLED: 150,000 training rows drawn at random from each split's 1,000,000 (full 500,000 test rows scored with
score.py). Noise: refits of the same baseline with other seeds (training subsample + bagging) span
r0 0.193-0.212, r1 0.230-0.234 (range up to 0.018 on one split); random-number column added: r0 0.196-0.207,
r1 0.230-0.236. Treat differences below ~0.01 on the mean as noise.
Scripts: work/common.py (harness), work/baseline.py, work/context.py, work/recent_ctx.py, work/trainfilter.py,
work/prior_em.py, work/calendar_feats.py, work/seeds.py, work/lookup_ip.py, work/eda_dups.py, work/eda_format.py;
logs work/run_*.log.

Honest baseline (features() as shipped):     r0 0.2037  r1 0.2323  r2 0.2224  mean 0.2195
Honest model at the prediction point (drop whole-flow cols, drop time_first):
                                              r0 0.2382  r1 0.2736  r2 0.2677  mean 0.2599
Better honest model (last 8 days of training only), at the prediction point:
                                              r0 0.2213  r1 0.2595  r2 0.2404  mean 0.2404
Same, with whole-flow columns:                r0 0.1757  r1 0.2025  r2 0.1920  mean 0.1900

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Whole-flow columns: duration, bytes, bytes_rev, packets, packets_rev, flow_end_reason, psize_bin*/ipt_bin* (30 cols) | work/baseline.py (all vs pp_notime); work/recent_ctx.py pp vs work/trainfilter.py recent8d | 0.2599 (shipped train) / 0.2404 (recent 8 d) | 0.2195 / 0.1900 | 0.034-0.045 (shipped train); 0.046-0.057 (recent 8 d) | No: known only when the flow ends (idle/active timeout), not after 30 packets | Drop these 30 columns (or restate the prediction point as flow end) |

No other exploit beat the noise; see "found nothing" below.

FLAWS THAT HURT AN HONEST MODEL

| # | What is wrong | Honest choice | Baseline | Honest-choice score | Gain (per split) | Fix |
|---|---|---|---|---|---|---|
| H1 | Training spans all earlier days back to 31 Oct; the oldest rows drift away from the test windows (31 Oct-1 Nov have a visibly different class mix: instagram 10% vs ~4.5%, google-www 4.4% vs ~7.7%) | Train only on the last 8 days before each window (work/trainfilter.py recent8d) | 0.2195 | 0.1900 | 0.028 / 0.030 / 0.030 | Not a leak; a modelling choice a deployed model would make. Optionally drop 30 Oct-1 Nov from the data (dropping only those days: 0.2106, gain 0.007-0.012) |
| H2 | time_first given as a feature in a temporal split (test times lie beyond every training time) | Drop time_first (work/baseline.py pp vs pp_notime) | 0.2680 (pp with time) | 0.2599 | 0.007 / 0.013 / 0.004 | Mild; leave to participants, or drop the raw timestamp from features |

Exploit #1 measured against both: shipped training 0.2599 -> 0.2195; recent-8-day training 0.2404 -> 0.1900.

FINDINGS

1. Whole-flow columns. The CESNET DataZoo feature docs (work/datazoo_features.html) state the flow statistics
   (DURATION, BYTES, PACKETS and _REV, FLOW_ENDREASON) "describe the entire flow" and the packet histograms (PHIST,
   here psize_bin*/ipt_bin*) are "built from all packets of the entire flow"; only ppi_* (incl. ppi_len,
   ppi_duration, ppi_roundtrips) cover the first 30 packets. The task's prediction point is "the first 30 packets
   have been seen". In the data, packets reaches 949,789 and duration 360 s while ppi_len <= 30, and
   flow_end_reason only exists once the flow ends. Adding them cuts log loss from 0.2599 to 0.2195 (gain
   0.034/0.041/0.045 per split, 2-4x the seed spread); against the recent-8-day honest model 0.2404 -> 0.1900.
   Mildest fix: drop the 30 whole-flow columns (keep dst_ip, dst_asn, src_port, quic_version, ppi_*). If the task
   instead means "classify a finished flow", rewrite the prediction point; then these columns are legitimate.

2. (Honest) Old training rows. The first two days have a different class mix (sampling of the source dataset,
   which the Zenodo page says was resampled per service), and the IP-to-service mapping drifts. Training on the
   last 8 days (same 150k rows) gains 0.029 mean, consistent in all three splits. Part of the gain may come from
   a validation slice closer to the test window (more boosting rounds chosen: 152-237 vs 128-150). This is a
   legitimate choice, not a task flaw; dropping 30 Oct-1 Nov from the data is the mild fix if wanted.

ATTACKS THAT FOUND NOTHING (numbers are mean log loss over r0/r1/r2 unless noted)

- Row order: rows are sorted by time_first; label equals next row's label 4.43% vs 4.04% by chance; no ties to
  exploit (3 duplicate timestamps). Train is a random 1M subsample of the earlier rows; test is contiguous.
- Copies across the split (work/eda_dups.py, split r0): 0 exact duplicate rows; ignoring time and src_port only
  0.15% of test rows have an exact training copy (label agrees 98%), ppi-only key 1.9% (73% agree), ppi+dst_ip 1.4%
  (92% agree). These are natural repeats of identical short flows that a tree already fits; not worth a model.
- Training rows that tell the future: none. Every split's training rows end before its test window starts
  (r0 train to 23 Nov 23:59, test 24-27 Nov; r1 to 19 Nov / 20-23 Nov; r2 to 15 Nov / 16-19 Nov).
- Statistics of the test rows / future context (work/context.py, work/recent_ctx.py): counts of flows to the same
  dst_ip (and dst_ip+src_port) in the next 60 s / 600 s and the gap to the next such flow, computed over all rows
  including later test rows: shipped train 0.2213 (all + past + future context) vs 0.2240 (past only) vs 0.2195
  baseline; recent-8-day 0.1993 (with future context) vs 0.1900. No gain. The dst_ip+src_port key is nearly unique
  (no client IP shipped), so there is no client session to rebuild.
- Test-window class composition (work/prior_em.py): EM prior re-estimation over the whole test window, per test
  day, or from the previous day all made it worse (all features: 0.2199 -> 0.2457 / 0.2473 / 0.2383).
- Format artefacts (work/eda_format.py): duration has microsecond precision (86% 6 dp), ppi_duration
  milliseconds, ppi_ipt whole milliseconds, sizes 21-1472, NaN padding equals ppi_len exactly; decimal counts of
  duration carry no class signal beyond duration itself. No sentinels or recoding by class.
- Identifiers: dst_ip (5,702 values) alone as a lookup gives log loss 0.84-0.88, accuracy 68-70%, unseen IPs in
  test 0.2-0.4% (work/lookup_ip.py). The monitor sees the server IP at the first packet: signal, not a leak.
  src_port differs in mean by class (client OS port ranges): also signal. Client IP (SRC_IP) is not shipped.
- Calendar (honest): hour/day-of-week instead of time_first, all features: 0.2139 vs 0.2195 (gain 0.004-0.008,
  within noise).
- Web: no competition, leak or "magic feature" threads exist for CESNET-QUIC22. Published work uses dst_ip/ASN as
  a strong (deployable) feature and treats flow stats as whole-flow. Row lookup in the public Zenodo files would
  work (server IP, ports, timestamps with microseconds are intact) but is not a flaw of the task.

WHAT I COULD NOT CHECK
- Full-size training (1M rows per split) and more seeds: runs were subsampled to 150k training rows on a heavily
  loaded machine; seed spread is from 3 seeds on r0/r1 only.
- The PDF papers (no PDF text tool in the kit environment); the feature semantics come from the DataZoo docs and
  the Zenodo record.
- Whether the source's per-service sampling (counts "before sampling" are published) makes daily class mixes an
  artefact that a deployed model would not see; EM on test composition found no gain, so it is not exploitable here.

Sources: https://zenodo.org/record/7409923 ; https://cesnet.github.io/cesnet-datazoo/features ;
https://tma.ifip.org/2023/wp-content/uploads/sites/12/2023/06/tma2023-final13.pdf ; https://arxiv.org/abs/2310.19568v1
```

</details>

<details><summary>Precedent checker: cesnet_quic22_service_classification</summary>

```text
PRECEDENT CHECKER - cesnet_quic22_service_classification_1m (record cesnet_quic22_service_classification), 2026-11-09

Verdict: the definition's calls follow precedent on 7 of the 10 points checked. One near-precedent the builder did not
cite bears on issue 1 (2_month_survival_rate_prediction: the source's comparator input kept out). Two departures
from the rule text have stated reasons that need recording: the packet directions typed numeric against CLEAN-14's
flag rule, and the fixed 1-in-20 sample before the split, which goes against definitions.md's "Temporal data: the frame
is not sampled". The second is now the fourth case of its kind in this batch, so an amendment is due. No drift: no
curator has decided any of these rules both ways. The register's flags (USE-5 and USE-8 opposite outcomes, SPLIT-14
amendment_due) do not touch this dataset's facts: its windows meet SPLIT-14 without an exception.

Read: principles.md, use_case.md (USE-3, 5, 6, 8, 10 and Cases), splits.md (SPLIT-13, 14, 19 and Cases),
cleaning_features.md (CLEAN-3, 14, 26 and Cases), metrics.md (MET-2, 15, 16, 17), leak_checks.md (LEAK-37), and
knowledge-data-foundry definitions.md ("Larger than the row budget"), all in df-large. Also dataset.py,
builder_report.md, column_auditor.report.txt, domain_practitioner.report.txt and register.json (6,080 decisions, 34
flags). Sibling definitions: tls_os_fingerprinting_masaryk_1m, ugr16_isp_netflow_intrusion_1m. Records:
cesnet_os_fingerprinting_2024, ctu_13, cic_ids2017, unsw_nb15, nsl_kdd, kddcup99, 2_month_survival_rate_prediction,
breast_cancer_prediction, sarcoma, zillow_prize, pricing_game_2017_french_mtpl, uk_mot_test_results,
allstate_claim_prediction_challenge, sorel_20m_malicious_pe, data_fusion_2026_guardian. Paths below are relative to
W=.

Which family precedents are curator decisions: none of the network-traffic family's address or class calls has been
reviewed by a curator. tls_os_fingerprinting_masaryk_1m and ugr16_isp_netflow_intrusion_1m are this batch's AI
calls; ugr16 has one CC (2026-11-08, Lennart: the real classes only). ctu_13 is `No` (CC 2026-10-27, Myunghwan:
shallow two-port rules, too little headroom). cic_ids2017, unsw_nb15, nsl_kdd and kddcup99 are `No` with AHDS (lab
or synthetic traffic). cesnet_os_fingerprinting_2024 is screened only. CESNET-QUIC22 is real backbone traffic and not
trivial (address lookup 0.85 against LightGBM 0.20 log loss), so neither ground for rejection carries over. The binding
precedents therefore come from outside the family; they are named under each point.

-----------------------------------------------------------------------------------------------------------------------
1. Server address and ASN kept as categories (USE-6, USE-10, SPLIT-13; the paper's IP baseline)
   Status: departs from the family's AI calls with stated reasons that hold. It also departs from the closest
   curator precedent on a source's comparator (2_month_survival_rate_prediction), and the builder does not name that
   precedent or the fact that sets this case apart. This belongs in issue 1.

   Family (AI, this batch, not reviewed):
   - ugr16_isp_netflow_intrusion_1m drops both addresses: "identifiers on which the label was assigned (the five
     hosts), so with them the task is a lookup" (dataset.py curation_comments). The fact that sets cesnet apart: its
     label is assigned from the SNI, not from the address. 16.7% of addresses serve several services and carry 62.9%
     of the flows, and the address lookup scores log loss 0.83-0.86 against 0.20 for LightGBM (probes/ip_lookup.json).
     It is no lookup task.
   - tls_os_fingerprinting_masaryk_1m drops dst_ip under CLEAN-3. It is a Crypto-PAn-anonymised opaque id of 138,681
     values (79,163 seen by one session), and it moves log loss by -0.0023 to +0.0023. The fact that sets cesnet
     apart: the address is the public, unanonymised server address, and it moves log loss from 0.51-0.54 to
     0.19-0.20. CLEAN-3 drops uninformative identifiers, and this one is informative.
   - Recurrence: 99.9% of a window's flows go to a known address. That fits USE-10's known entity and SPLIT-13's
     "part of the task" branch. It matches tls_os (16-21% of a window's flows in sessions with earlier flows, kept and
     measured). Consistent.

   Curator precedents on USE-6 (use_case.md Cases):
   - 2_month_survival_rate_prediction (CC 2026-10-26, Lennart, issue 5): the physicians' estimates prg2m/prg6m stay
     out because "the use case is SUPPORT's objective estimate ... set beside the physician's own estimate (the
     physicians were interviewed on day 3 as the comparator)". This is the closest shape: the source's model leaves
     an input out and reports it as a separate comparator. TMA 2023 does the same with the address: its ML models
     leave it out, and the "IP baseline" (68.68% accuracy) is reported beside them.
   - breast_cancer_prediction (CC 2026-10-15, Lennart): the BI-RADS reading is kept as "the actor's own input".
     medical_facility_operational_data (use_case.md Cases, USE-6) adds a field the front desk knows at check-in.
   - The candidate fact that sets cesnet apart from 2_month: the address is a raw field of the flow record that the
     operator's own monitor holds and uses (operators keep IP lists, per the domain practitioner). It is not a second
     predictor's output for the same target. The paper also names an ensemble with the address as future work
     (Sect. VII). That places it with BI-RADS, not with the physician's estimate. The counter-fact: like SUPPORT,
     the source chose to measure its models without the address, and the shipped task is not the paper's ML task
     (0.20 against 0.51 log loss).

   Reflection prompt (draft, for issue 1):

   ### Does the server's address stay an input, although the paper reports it only as a separate baseline, as SUPPORT did with the physicians' estimates?

   **Problem:**
   - The definition keeps `dst_ip` and `dst_asn` (USE-6). In TMA 2023 the ML models leave the address out, and an
     "IP baseline" (68.68% accuracy) is reported beside them.
   - On 2_month_survival_rate_prediction (2026-10-26) the curator kept the physicians' estimates out because the
     source set its model beside them as a comparator. On breast_cancer_prediction (2026-10-15) the BI-RADS reading
     stayed as the actor's own input.
   - With the address LightGBM scores log loss 0.19-0.20; without both columns 0.51-0.54. The address alone, as a
     lookup, scores 0.83-0.86.

   | Option | Pro | Con |
   |---|---|---|
   | (a) keep both and record the fact that sets this case apart: the address is a raw field of the operator's own flow record, not another predictor's output for the target (as BI-RADS, unlike prg2m) | matches the operator's view (USE-6) and the paper's proposed ensemble; the exception text is ready for use_case.md Cases | the shipped task is not the paper's ML task; the address's value is pre-ECH and specific to CESNET |
   | (b) treat it like 2_month: drop both, follow the source's ML task | same as the SUPPORT call; tests the side-channel features the paper studies | drops an input the actor really has; log loss rises from about 0.20 to about 0.52 |
   | (c) keep the network, drop the address | a coarse, stabler attribute; the side channels carry the task | no precedent; a middle path of our own |
   | (d) amend USE-6 to say when a source's comparator input is an input (raw field the actor holds vs a second prediction of the target) | settles the 2_month and BI-RADS line for later cases | a rule change on one dataset |

   Recommendation: (a). Write the fact into curation_comments ("unlike 2_month_survival_rate_prediction's physician
   estimates, the address is a field of the record itself") and add a USE-6 Cases row once the curator decides.

   Footnotes: USE-6, USE-10, SPLIT-13, CLEAN-3, LEAK-37; precedents 2_month_survival_rate_prediction (2026-10-26),
   breast_cancer_prediction (2026-10-15), W/curation/records/2_month_survival_rate_prediction.md line 71.

-----------------------------------------------------------------------------------------------------------------------
2. Background flows dropped: a closed world of 102 services (USE-5, USE-8)
   Status: consistent with sarcoma. The ugr16 and ctu_13 precedents do not carry over; the reason is below.

   - sarcoma (CC 2026-10-21, Lennart; use_case.md USE-8 Cases): a closed set of confirmed types ships with
     fit="approximate" and the gap named. Cesnet does the same: fit approximate, and fit_reason names "flows of
     services outside the 102 are left out, where a deployed model would meet them". Consistent.
   - ugr16 (CC 2026-11-08, Lennart) and ctu_13 (AI review 2026-10-29, under the CC No) also drop classes or background
     rows, but their "background" is unlabelled traffic ("the rest of captured traffic") or classes the authors
     staged. Cesnet's three background classes are labelled from the SNI (google-background, facebook-background,
     default-background), and the data article keeps them "for open-world scenarios". The fact that justified those
     drops (no real label) is absent here, so they are no precedent for dropping. They are no precedent against it
     either.
   - The record's screening (AI, 2026-11-08) said "target APP (105 classes)". It was not a curator decision (the CC
     only accepts for adding), so dropping to 102 departs from no curator call. The source's own evaluation (TMA,
     102 outputs) supports the closed world. USE-5 is a Must ("what the actor would act on"), and the domain
     practitioner's case for (b) is that the actor acts on background flows too. That is a weighing call and stays
     issue 2. No reflection prompt: this is no departure from a rule or a precedent.
   - The 16% background share in the network's traffic (DiB Sect. 3.1: the 102 services cover 84%) is a selection
     its setting does not share. Under USE-8's selection-bias paragraph (Lennart, 2026-10-27) that makes the fit
     approximate, as declared, with the selection named. Consistent.

-----------------------------------------------------------------------------------------------------------------------
3. Prediction point at flow export with whole-flow statistics (USE-3, LEAK-37)
   Status: consistent with tls_os_fingerprinting_masaryk_1m (export at the connection's end or after 5 minutes;
   duration and flow fields as inputs) and with ugr16_isp_netflow_intrusion_1m ("when the border router exports a
   finished flow record"). TMA's own FLOWSTATS are the same columns.
   Not a precedent question, but a USE-3 wording mismatch the other two definitions do not have: task_summary.use_case
   says "for quality-of-service priorities", a decision taken inline within the first packets, before export (the
   column auditor and the domain practitioner raise it too). Name the moment ("on the exported flow record") or drop
   QoS from use_case.

-----------------------------------------------------------------------------------------------------------------------
4. 4-day windows instead of the paper's weekly periods (SPLIT-14 Must over SPLIT-19 Should)
   Status: consistent. A higher-ranked Must decides, so no exception record is needed.
   - tls_os_fingerprinting_masaryk_1m: half-days instead of the paper's "train day 1, test days 2-5", the widest length
     that keeps three windows above the floor. ugr16_isp_netflow_intrusion_1m: 5-day windows. Cesnet: 4 days (59.7,
     69.4 and 87.8% train shares on all 140M service flows; 5 days would leave the oldest at 47.3%). The same rule
     applied the same way.
   - The paper's design also trains one model for three test periods, which SPLIT-14 calls one evaluation, not three.
     So SPLIT-19 yields on two counts.
   - The SPLIT-14 amendment of 2026-11-08 (wisconsin: one older window may train on at least 40% when two windows are
     above the floor) does not open weekly windows. Weekly gives one window above the floor (the week of 14 November
     is at 49.2%, the week of 7 November at 21.4%). Checked, not applicable.
   - Register flag amendment_due SPLIT-14 (five exceptions): this dataset adds none.

-----------------------------------------------------------------------------------------------------------------------
5. The fixed 1-in-20 hash sample before the split
   Status: departs from the stated repository protocol, with a reason (size). It is the fourth case of the same kind
   in this batch, so an amendment of definitions.md is due.
   - The protocol (knowledge-data-foundry definitions.md, "Larger than the row budget"): "Temporal data: the frame is
     not sampled. The windows (at least 3) are built on the full data, then sample_temporal_splits keeps ...".
   - Cesnet samples the release before the split: 1 in 20 by the SplitMix64 hash of the flow's ID, 7.66M of 153M
     flows (version_comment). The reason given: one pass over a 21 GB zip (89 GB unpacked), peak 19.3 GB. The
     safeguards: the window table is built from counts of all flows (flow_counts.parquet), the key does not depend on
     the label, no class share changes in expectation, and every window and train side stays above its budget (684k
     to 1.29M per test window against 500k; 4.19M to 6.17M per train side against 1M). Given those, the draws match
     what a direct draw from all flows would give in distribution.
   - The same kind in this batch: ugr16_isp_netflow_intrusion_1m (1-in-20 hash of the row position, mail flows only),
     sorel_20m_malicious_pe_1m (a sixteenth by SHA-256 prefix), data_fusion_2026_guardian_1m (a uniform random tenth
     "so the frame fits in memory", still TODO(verify)). None is reviewed by a curator. The data_fusion case uses no
     fixed hash, so it is weaker than the others.

   Reflection prompt (draft, cross-dataset: an amendment, not a per-dataset issue):

   ### Should a temporal `_1m` version be allowed to sample its raw rows by a fixed, label-free hash before the split, as four definitions of this batch do?

   **Problem:**
   - definitions.md says a temporal version's frame is not sampled. cesnet_quic22 (1/20), ugr16 (1/20), sorel_20m
     (1/16) and data_fusion_2026_guardian (1/10, random) sample before the split because the full release does not fit
     in memory.
   - Under conditions it changes nothing in distribution: the key does not depend on the label or the time, the
     windows are cut on counts of all rows, and every side stays above its budget. Without them it can shift windows
     or thin rare classes.
   - Four cases of one reason, unreviewed (principles.md: the third exception of the same kind calls for an
     amendment).

   | Option | Pro | Con |
   |---|---|---|
   | (a) amend definitions.md: a pre-split sample is allowed for a release too large to hold, by a fixed hash of a label-free unique key, with the windows cut on the full counts and every side above its budget, stated in version_comment | records what four definitions do; the conditions are checkable | one more protocol path to maintain |
   | (b) keep the rule; each case is an exception with its reason | no protocol change | four exceptions with the same reason, the case the amendment rule is for |
   | (c) require the full-frame path (stream all rows, sample in the split) | one protocol for all | out of reach for 153M x 133 or larger releases on the current memory budget |

   Recommendation: (a), with data_fusion_2026_guardian brought to a fixed hash, or noted as the case without one.

   Footnotes: definitions.md "Larger than the row budget"; principles.md "Exceptions and amendments"; SPLIT-14,
   TP-8.

-----------------------------------------------------------------------------------------------------------------------
6. Fallback log loss, unweighted, on the release's sampled class mix (MET-16; class-weighted log loss as an alternative)
   Status: consistent with the rule as written. The alternative has no rule and no precedent behind it and would
   need an amendment, not an exception.
   - MET-16 (2026-11-06, Lennart): scored unweighted unless the use case is a population estimate. The definition
     follows it and says so in the metric's reason. MET-2's Cases (emscad, taiwanese_bankruptcy_prediction: score the
     class balance the shipped rows hold) and ugr16 (unweighted although the spam share moves from 51-61% to 18-26%)
     are scored the same way. The fallback over the source's four threshold metrics follows the tension row (MET-4 to
     MET-9: gallstone_disease and ljubljana_breast_cancer to the fallback, Lennart, 2026-10-21) and
     hepatitis_c_prediction (CC 2026-10-21: no balanced accuracy the paper did not choose).
   - A class-balanced log loss (the domain practitioner's first choice) is no design weight under MET-16 and no unit
     weight under MET-17, which needs units of repeated rows. No definition in the working copy declares one (grep:
     none). The tension row says "we never invent a cost or threshold the source did not fix". The case for it does
     have a fact behind it: the source itself says the mix is an artefact and that only recall survives it (TMA
     footnote 2). Taking it would amend MET-16 or MET-17 (a per-class weight when the source sampled by class). That
     is the curator's call. If raised, raise it as an amendment question, not as an exception.

-----------------------------------------------------------------------------------------------------------------------
7. Packet sequences as plain columns (CLEAN-26 by analogy; the proposed PacketSequence special-feature kind)
   Status: consistent. The proposed kind is a deliberate amendment, the right channel.
   - CLEAN-26 covers spectra, CLEAN-24 SMILES, and the library knows those two kinds only. Shipping the positions as
     published numeric columns, without scaling or zeroing, follows CLEAN-26's "never processed in the data". It also
     matches uniform_soybean_tests_yield (weather as one column per variable and day, no special kind) and
     huesken_sirna_efficacy (CC 2026-11-04/05, Lennart: the sequence kept as descriptors, SEL-12, Revisit later).
   - A PacketSequence kind would amend CLEAN-26's scope (or add a rule) and change the library. It goes to the main
     session and the curator as a proposal, which is how CLEAN-26 itself came in (Andrej's PR #21, 2026-11-02).
     Not drift.

-----------------------------------------------------------------------------------------------------------------------
8. ppi_dir_02..30 (+1/-1) typed numeric against CLEAN-14's flag rule
   Status: departs with a stated reason ("CLEAN-26 by analogy"), but CLEAN-26 does not cover this column. A spectrum
   position is a measured quantity; a direction is a two-valued code.
   - CLEAN-14 (amended 2026-10-21, Lennart, home_credit_default_risk: "one clear way to treat 0/1 flags"; Cases:
     qsar_oral_toxicity, hiva_agnostic, qsar_tid_11 fingerprint bits categorical; 35 definitions' flags) says a
     two-valued column is categorical when its meaning makes it a yes/no flag, "a fingerprint bit" included. A
     direction is such a code by meaning (client to server, or back). The +/-1 coding does not make it a count.
   - The candidate fact that sets it apart: the direction is one channel of one sequence object whose standard
     readers (the paper's CNN, size x direction features) use the sign as a number. The release codes it +/-1 for
     that reason (DiB 2.1). Typing 29 columns categorical would split the object that the proposed PacketSequence
     kind would declare. The loss is nil either way (the column auditor calls it lossless).

   Reflection prompt (draft):

   ### Do the packet directions stay +1/-1 numbers, against CLEAN-14's rule that a two-valued code is categorical?

   **Problem:**
   - `ppi_dir_02` to `ppi_dir_30` hold only +1 (client to server), -1 and missing past the flow's length. By meaning
     each is a two-valued code, which CLEAN-14 types categorical (fingerprint bits, 2026-10-21).
   - The definition keeps them numeric "by analogy" with CLEAN-26, which covers spectra, measured quantities per
     position.
   - The sign is used as a number by the sequence models of the field (size x direction), and the release codes it
     that way.

   | Option | Pro | Con |
   |---|---|---|
   | (a) keep numeric, recorded as an exception to CLEAN-14: a direction is a channel of a packet sequence whose sign the field's models multiply with the sizes; it moves to the PacketSequence declaration when that kind exists | keeps the sequence whole; as published; serves P7's "as an expert would ship it" | an exception to a rule the curator wanted to have "one clear way" |
   | (b) treat it like the fingerprint bits: categorical | follows CLEAN-14 and its 2026-10-21 Cases | 29 categorical columns inside a numeric sequence; a sequence encoder must cast them back |
   | (c) amend CLEAN-14: positions of a declared special feature keep the source's numeric coding | settles it for every future sequence kind | waits for the PacketSequence kind |

   Recommendation: (a) now, (c) when the PacketSequence kind lands. Replace "CLEAN-26 by analogy" with the stated
   fact in curation_comments.

   Footnotes: CLEAN-14, CLEAN-26, CLEAN-24; Cases rows cleaning_features.md lines 361-362.

-----------------------------------------------------------------------------------------------------------------------
9. dst_ip as a 5,702-level category against CLEAN-14's "string for ... high-cardinality values"
   Status: consistent with the curator's reading of CLEAN-14 in the Cases.
   - Categorical precedents: zillow_prize census_tract (CC 2026-10-26, Lennart: 3,030 levels, median 40 sales, 0.2%
     of test rows unseen; the 55,601-level block dropped as a near-identifier), allstate submodel (2,379 levels),
     uk_mot make (11,191 spellings, 58 cover 99%).
   - String precedents: pricing_game_2017_french_mtpl pol_insee_code (17,794 communes, median 2 policies each, "high-
     cardinality text") and uk_mot model (54,868 values with trim words).
   - The dividing facts are rows per level, unseen levels at test time, and whether the value has text structure.
     dst_ip has 5,702 levels over 2.5M rows (about 440 per level), 99.9% of test flows go to a seen address, and an
     address has no words. That puts it with census_tract, not the communes. dst_asn (336 levels in the frame, a
     network code) is categorical by meaning, as the "codes shipped as numbers as categories" Cases row says (sberbank
     ID_metro). lt_vehicle_loan_default_prediction's pincode stays numeric (CC 2026-11-05) because its masked
     numbering kept a geographic order. ASN numbers carry no such order. Consistent.

-----------------------------------------------------------------------------------------------------------------------
10. Further point in the family (not in the prompt): QUIC_SNI dropped (LEAK-10), although tls_os keeps its SNI (USE-6)
   Status: consistent. The fact that sets it apart is written down: here the label is the SNI mapped by servicemap.csv
   (each of the 36,948 sampled names maps to one class), so the SNI is a function of the label. In tls_os the label is
   the OS from DHCP and the SNI is an input. The user agent drop matches tls_os's drop of the HTTP User-Agent OS
   fields.

-----------------------------------------------------------------------------------------------------------------------
Drift and repeated exceptions
- Drift: none found. No curator has decided USE-6 addresses, CLEAN-14 for addresses, or the network family's class
  sets both ways. The register's drift flags (SEL-16, post-outcome feature, scaling over all rows) do not involve
  this dataset.
- Repeated exceptions: the pre-split sample (point 5) is the fourth of one kind, so an amendment is due. "Paper's
  split replaced for SPLIT-14" recurs (tls_os, ugr16, cesnet), but a Must decides it, so it is no exception and needs
  no amendment.

Footnote rule IDs: USE-3, USE-5, USE-6, USE-8, USE-10, SPLIT-13, SPLIT-14, SPLIT-19, LEAK-10, LEAK-37, MET-2, MET-16,
MET-17, CLEAN-3, CLEAN-14, CLEAN-24, CLEAN-26; definitions.md "Larger than the row budget".
```

</details>

<details><summary>Advocate: cesnet_quic22_service_classification</summary>

```text
ADVOCATE OPENING BRIEF - cesnet_quic22_service_classification_1m (2026-11-09)
Position: ship as defined (102 classes, address kept, export point), with note-only changes that need no decision.

1. The task is real, large and hard, and the evidence agents found no leak. Claim auditor: no validity claim refuted;
   column auditor: no leak among the 132 features at the definition's prediction point (flow export); split auditor:
   "right with notes, nothing needs a re-split"; gamer: nothing but the whole-flow columns beats noise. Real backbone
   traffic, LightGBM 0.20 log loss vs address lookup 0.85, so neither family ground for rejection (lab traffic, too
   little headroom; ctu_13, cic_ids2017) applies. Rules: USE-3/USE-6 (Must) met; precedent checker: 7 of 10 calls follow
   precedent.

2. Server address and ASN stay (issue 1, option a). USE-6 (Must): anything known at the prediction point is a
   legitimate input; the monitor sees dst_ip/dst_asn in the clear. The domain practitioner, the actor, would use them
   ("IP lists are standard operator practice") and the paper builds an IP baseline and proposes the ensemble. The gap
   (0.51 -> 0.19; blind 0.869 -> 0.948 acc) is signal an operator has, not leakage; the lookup alone is 0.681 acc, far
   from the model. The blind reviewer's DataZoo "other fields" argument is a convention of the loader, not a rule; a
   Must outranks a source's default feature list. USE-10/SPLIT-13: 99.9% of test flows go to known servers, so the
   recurring server is the task, not a cold start. Mildest remedy: write the measured gap and CDN drift in the notes.

3. The whole-flow columns are not a leak; the use_case wording is. The definition's point is the exported record
   (column auditor; the TMA paper's own inputs are FLOWSTATS + whole-flow histograms; precedent
   tls_os_fingerprinting_masaryk_1m). The gamer's 0.04-0.05 gain is against a "first 30 packets" point the definition
   never names. Fix with no decision: drop "quality-of-service priorities" from use_case, say "on the exported flow
   record" (USE-3 Must, USE-8 Must fit wording). Rewording outranks dropping 30 columns (remedy ladder: mildest fix).

4. Dropping background flows (issue 2) keeps the source's 102-class closed-world task. USE-5 (Must) predicts what the
   actor acts on; the paper's task and benchmark are 102 classes. The 8.3% background classes are "other X" buckets,
   not services. State the closed world in USE-8 fit; 105 classes is an option for the curator, not a defect. Record
   says 105/153M: fix the record text to 102 classes / 140.47M service flows.

5. Split is sound and measured. 4-day windows meet SPLIT-14 (Must) with 59.7/69.4/87.8% train; no gap needed (at most
   0.0006% straddlers, SPLIT-10); hash sample keeps class shares (chi-square p 0.35-0.99). Notes only: holiday 17 Nov
   in the first window, first two days a capture artefact, sampling-rate shifts as drift. Training-window choice
   (gamer H1) is the participant's, not ours.

6. Metric: log loss (MET-8 Should) scores the probabilities the operator thresholds and aggregates; class-weighted log
   loss is a curator option (domain), not a required change. Unweighted on the release mix follows MET-16.

7. Small cleaning, no decision: negative IPT (61 cells) and dst_asn 65535 -> missing; fix "133 features" to 132;
   document quic_version 0xfaceb00x = Meta. ppi_dir ±1 numeric is a named, lossless CLEAN-14 departure (precedent
   checker: stated reason holds); the 1-in-20 sample of a temporal frame is the 4th case -> amendment to definitions.md
   (cross-dataset item), not a block on this dataset.
```

</details>

<details><summary>Critic: cesnet_quic22_service_classification</summary>

```text
CRITIC OPENING BRIEF - cesnet_quic22_service_classification_1m (record cesnet_quic22_service_classification), 2026-11-09

Position: ship only after the changes below. None is a ground for exclusion: the task is real backbone traffic, has
signal and headroom (log loss 0.20 vs 3.54 dummy), and every phase-A agent ends at "ship with changes/notes".

1. The use case names a moment the features do not fit (USE-3 Must, LEAK-1 Must).
   Problem: task_summary/use_case lists QoS priorities and enforcing policy, decisions taken inside the connection,
   but the prediction point is the exported flow record (idle 65 s / active 300 s) and 30 columns (bytes, packets,
   duration, end reason, the full-flow histograms) only exist then. Effect: a reader takes the score as an inline
   classifier's; at the first-30-packets point it is 0.260 not 0.220 log loss (task gamer, 0.034-0.045 per window).
   Evidence: task_gamer exploit #1; column_auditor finding 1; domain_practitioner Q1; claim_auditor P3 (rank 1).
   Remedy: reword use_case and task_summary to labelling exported flow records (reporting, accounting, SNI audit);
   drop QoS/inline enforcement. Columns stay (source's own inputs, TMA IV-A1b).

2. The server address makes much of the task a lookup, and the source's models leave it out (USE-6 Must vs
   USE-10 / SPLIT-13; precedent ugr16 drops addresses, 2_month_survival_rate keeps a source comparator out).
   Evidence: log loss 0.19-0.20 with dst_ip+dst_asn vs 0.51-0.54 without (builder); acc 0.948/macro-F1 0.868 vs
   0.869/0.654, a train-set IP->majority lookup alone 0.681 acc, 0.74% unseen IPs in test (blind reviewer); DataZoo
   lists DST_IP, DST_ASN, SRC_PORT, QUIC_VERSION as "other fields", not model inputs. USE-6 lets them in, so I do not
   ask to drop them. Remedy: curator call on issue 1 with these numbers; the notes name the precedent that sets this
   case apart (label from SNI, not address), and that under ECH/shared CDN fronts the address is a 2022 view worth
   less (domain practitioner). Document quic_version 0xfaceb00x = Meta stacks.

3. Closed world: background flows (about 16%) dropped, no "other" outcome (USE-5 Must, USE-8 Must).
   Effect: an operator always meets unknown services; the test never asks the model to reject one.
   Evidence: domain_practitioner (prefers 105 classes or an 'other' class); builder issue 2; record says 105 classes.
   Remedy: curator call on issue 2; at minimum the fit statement (USE-8) names the closed world and its share, and
   the record's 105-class/153M-row figures are corrected to the shipped 102 classes / field rows.

4. The class mix is the curators' per-service sampling, scored unweighted (MET-5/MET-6, Should).
   Evidence: release samples top services at different ratios; TMA footnote 2 says the mix does not carry to the
   network; domain practitioner would select by macro recall / class-balanced log loss.
   Remedy: a note in the metric comment; class-weighted log loss left as a named curator call, not a blocker.

5. A temporal frame sampled before the split (definitions.md "Temporal data: the frame is not sampled", Should).
   Evidence: precedent checker: fixed 1-in-20 hash sample, fourth such case in the batch. The split auditor shows
   class shares hold (chi-square p 0.35-0.99), so no harm measured. Remedy: record the departure; amendment of the
   rule is a cross-dataset item, not this dataset's blocker.

6. Split text misses two facts (SPLIT-20 Should).
   Evidence: claim_auditor/split_auditor: 31 Oct-1 Nov are a capture break (other class mix: instagram 10% vs ~4.5%),
   not a volume dip; the oldest test window holds the 17 Nov holiday and a bridge day. Remedy: notes in
   splits_comment; optionally drop 31 Oct-1 Nov (gain 0.007-0.012, task gamer H1). No re-split.

7. Small cleaning and count slips (quality only, never a reason to exclude).
   CLEAN-11: 61 negative inter-packet gaps (to -4 ms) -> missing; dst_asn 65535 -> missing (CLEAN-11 sentinel);
   CLEAN-14: ppi_dir +-1 typed numeric, record as a named exception; builder's "133 numeric features" is 132 mixed
   (column auditor). Remedy: repair in the definition.
```

</details>
