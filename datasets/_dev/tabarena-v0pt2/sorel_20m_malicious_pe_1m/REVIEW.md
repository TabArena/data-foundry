# sorel_20m_malicious_pe

**Outcome:** added as `sorel_20m_malicious_pe_1m`. Sophos and ReversingLabs' SOREL-20M Windows executable files (a fixed sixteenth of the release: 1,251,351 files whose SHA-256 begins with 0, first seen from January 2017 to April 2019) with the release's EMBER version 2 vector and the first sighting, tested on three 30-day windows that tile the release's own test set, each training on a random million earlier files; the AI recommends shipping it after the panel's changes, which are made: the sample's description corrected (prefix 0 is 48.9% malicious against 50.5% for the release, about 40,000 extra benign training files from benign batches of July-August 2017 and June-July 2018; the test windows unaffected), the feed rhythm of the first sighting named in `fit_reason`, and the stated 0 and late values of `header_coff_timestamp` noted as kept.

```text
Verdict: ship after changes (made).
Validity: a real static detector at first sighting; every feature comes from the file's bytes; the detection count and 11 behaviour tags are out (known only later). 0 exact copies across the split; the task gamer found no exploit (every trick within +-0.0002 ROC AUC of a noise column). The split tiles the release's test set; no gap, measured.
Value: LightGBM 0.9973, random forest 0.9966, linear 0.9861 ROC AUC; families still spread in log loss (0.053 / 0.078 / 0.134) and in the true positive rate at a 0.1% false positive rate (0.929-0.945).
Quality: the hashed machine, subsystem and PE type decoded into names; 33 all-zero bins dropped; flags categorical; the other hashed blocks plain, as ember2024.
Weighed: source +, shape +, gap 0, use case 0, risk - (unpublished labels, a benign batch ordered by SHA-256 in the oldest training side).
For the curator: 1, the sample prefix; 2, the metric; 3, the first sighting to the minute; 4, the hashed blocks; 5, the sentinel warning.
Record field: original_source `Company` against `Other` in the definition (Sophos's public S3 bucket in the AWS Open Data registry); the record value counts as the schema's Other.
```

**Priority 2:** from screening; the largest public table for static malware detection, but 97% of the vector is hashed bins or histograms, the labels come from undisclosed internal sources, and the task sits near its ceiling (ROC AUC 0.997). Factors: gap 0, use case 0, source +, shape +, risk -.

**Main points:** Five calls: keep the SHA-256 prefix 0 sample with its corrected text or switch to an in-band prefix; ROC AUC or a partial ROC AUC up to a 0.1% false positive rate; the first sighting to the minute or to the day; the hashed blocks as plain columns; and whether to accept the missing-value-sentinel warning with the builder's text.

**Issues for the curator:**

1. **Keep the sample of files whose SHA-256 begins with 0, or switch to a prefix that matches the release?**

   * **Problem:**
     - The release's benign files of July-August 2017 and June-July 2018 came in batches that favour low SHA-256 values, so prefix 0 holds about 40,000 more benign training files than the average prefix (48.9% malicious against 50.5% for the release, 49.9-50.8% for each other prefix; z = 37, far beyond chance).
     - The definition said the sample depended on neither label nor time (stating 49.5% against 51.2%); both are now corrected with these numbers.
     - Prefixes 0 and 1 are the only ones out of the band of the others; a prefix such as 8 is in band every month.
   * **Effect on the task:** about 4% of the oldest train side is a benign batch ordered by hash rather than the month's population; the test windows are unaffected (benign ratio to other prefixes 1.00-1.08); the effect on ROC AUC is likely small and not measured.
   * **Experiments:** the claim auditor counted every prefix of `meta.db` by month (prefix 0 against 8: 4.2x the benign files in July 2017, 1.75x in June 2018, 0.87-1.13x in other months). Not run: a fit on prefix 0 against prefix 8 with the same test windows (part of the 1-2 h re-run of option B).
   * **Consistency:** no precedent for a hash-prefix sample that the release's ordering skews; the size call (a sixteenth for memory) was the builder's draft issue and is folded in here. The claim was refuted by measuring it[^ev1].
   * **Panel:** the critic switches to prefix 8 and re-prepares, so the sample is what it claims; the advocate keeps prefix 0 with the corrected text and leaves a switch to the size call; the mediator leans to prefix 8 if the curator re-prepares anyway.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Prefix 0, corrected text (implemented) | keeps the sample; the version comment states the benign excess | no re-run; the text matches the data | a hash-ordered benign batch stays in the oldest train side |
     | B | Prefix 8 at a sixteenth | `SAMPLE_PREFIX = "8"`, re-prepare, check and probes | in band every month; the sample is what a random sixteenth would be | about 1-2 h; window sizes change |
     | C | An eighth from two in-band prefixes | prefixes 8 and 9 (not 0 and 1, both out of band) | twice the rows; in band | a re-prepare of 1-2 h or more; memory about 2x (50+ GB check, 100+ GB probes); window sizes change |

   * **Recommendation:** A, since the text is now true and no score effect is measured; B if the curator re-prepares for any other reason. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, set `SAMPLE_PREFIX` (C needs the prefix reader to take two prefixes), re-run `_prepare_raw_files`, `dataset check`, the leak, task and group probes, and rewrite the version comment, the row counts in the notes and the splits comment, and claims 17-19.

   [^ev1]: **EV-1** (Must): facts before rules: settle a disputed fact with the decisive experiment before arguing about
     rules or asking the curator.

2. **Keep the ROC AUC, or score only false positive rates up to 0.1%?**

   * **Problem:**
     - Every model family scores a ROC AUC between 0.975 and 0.997 (LightGBM 0.9973), while the true positive rate at a 0.1% false positive rate moves by points (0.929-0.945).
     - The paper asks for performance "at lower false positive rates (1 in 1000 or below)" ([arXiv 2012.07634](https://arxiv.org/abs/2012.07634), Sec. 1), a range and no single bound, and reports several criteria side by side, so the definition declares the fallback ROC AUC[^met5].
   * **Effect on the task:** a partial ROC AUC with `max_fpr=1e-3` scores where a vendor operates, with about 60 false positives per test window, enough for a stable estimate; it also makes the no-gap split optimistic: training up to the window's start adds 1.3-3.0 points of the true positive rate at 0.1% (0.00006-0.0007 ROC AUC), so it needs a gap of about 7 days[^split10].
   * **Experiments:** the split auditor measured the gap effect above; families spread in log loss (0.053 / 0.078 / 0.134). Not run: the rank of several methods under both metrics across the three windows.
   * **Consistency:** ROC AUC matches ember2024_malware_detection (as implemented), naticusdroid, ugr16 and website_phishing. A partial ROC AUC would be the third exception of its kind (after protein_model_quality_rf_pcp and huesken_sirna_efficacy), so it is a proposal to amend the paper-metric rule, not another exception[^p-exc]. It is decided on sorel's own facts, not together with ember2024[^met10]; here the source states a range, where ember's code fixes `max_fpr=5e-3`.
   * **Panel:** the critic and the domain practitioner want the partial ROC AUC at the paper's 1e-3; the advocate and the precedent checker keep the ROC AUC, since a bound picked from a range would be ours.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC (implemented) | the fallback for binary classification | the rule as written; matches ember2024 and three other security datasets; no gap needed | ranks near the ceiling; weights false positive rates no vendor operates at |
     | B | Partial ROC AUC, max_fpr=1e-3 | from context, the bound from the paper's sentence; a new library metric; a gap of about 7 days | scores where the decision is made; the domain practitioner's choice | an amendment of the paper-metric rule; new metric code; the bound is ours from a range; costs a week of training data |

   * **Recommendation:** A; the source gives no single bound, and the ROC AUC still separates families at low false positive rates. **Decision:** A or B?

   **Notes for the AI:** on B, add a partial ROC AUC (`max_fpr`) to the metric library with a reference check against `sklearn.metrics.roc_auc_score(max_fpr=1e-3)` (MET-13), declare it from context, draft the MET-5 amendment for the curator, set a gap of about 7 days in `Temporal`, re-run `dataset check` and the task and split probes, and restate the time feature's effect at 0.1% (-0.57 to +0.80 points) in issue 3.

   [^met5]: **MET-5** (Should): a paper's metric is the source's metric only when it is one deliberate choice; a paper that reports several metrics side by side without naming the one that decides has no unique original: declare the fallback.
   [^met10]: **MET-10** (Weigh): factors on a borderline call between the source's metric and the fallback, among them the ceiling (amended 2026-11-02: no family call).
   [^split10]: **SPLIT-10** (Should): when a label is known only some time after its row, a model refit at a window's
     start knows only the rows whose label had arrived; simulate that with a gap of about the label's delay.
   [^p-exc]: principles.md, Exceptions: a third exception of the same kind asks for an amendment of the rule.

3. **Keep the first sighting to the minute, or floor it to the day?**

   * **Problem:**
     - The hour and weekday of `first_seen` alone separate the classes at ROC AUC 0.605-0.626: ReversingLabs' feed rhythm, not a property of the file.
     - With the vector they add at most 0.0008 ROC AUC (the task gamer measured 0.0001-0.0002, within the noise of a random column), and move the true positive rate at a 0.1% false positive rate by -0.57 to +0.80 points.
   * **Effect on the task:** the time is known when the file arrives, so no rule is breached[^use6]; the rhythm belongs to one vendor's telemetry, now named in `fit_reason`[^use8].
   * **Experiments:** builder and claim auditor (200,000 files, untuned LightGBM, 3 windows); task gamer (hour, minute and weekday features: within noise).
   * **Consistency:** ember2024_malware_detection has the same open question for its submission time (its issue 2, A implemented); this is a linked item decided on sorel's facts, not a joint call.
   * **Panel:** the advocate keeps it (known at arrival, as ember2024's option A); the critic and the domain practitioner floor it to the day (it does not transfer to another vendor). It turns on who the actor is: the telemetry's owner (keep) or any vendor (floor).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep to the minute (implemented) | `first_seen` as recorded; the rhythm named in `fit_reason` | known at arrival; matches ember2024 as implemented | one feed's arrival rhythm stays as signal |
     | B | Floor to the day | the time feature keeps date and weekday | removes the hour; windows unchanged | the weekday rhythm stays; departs from ember2024 unless it floors too |

   * **Recommendation:** A, the time is known at the prediction point and the gain is within a method gap. **Decision:** A or B?

   **Notes for the AI:** on B, floor `first_seen` in `_clean` after the split column is read (the windows must keep their row counts), drop the rhythm sentence from `fit_reason`, re-run `dataset check` and the task probes.

   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^use8]: **USE-8** (Must): write how closely the data mirrors the use case, its fit; an approximate fit names its gap.

4. **Keep the hashed blocks and histograms as plain numeric columns?**

   * **Problem:**
     - Besides the three decoded fields, the header and DLL characteristics, section, import and export names are hashed into bins, and the byte, byte-entropy and character histograms fill hundreds of columns.
     - All panel members agree to keep them; the call is the curator's because the builder raised it.
     - Only the malicious binaries are released, so this vector is the only representation of every file.
   * **Effect on the task:** about 97% of the features are hashed bins or histograms; detectors in the field (the authors' LightGBM and network) read them as columns.
   * **Experiments:** none needed; the authors' LightGBM reproduces its published ROC AUC on our vectors (0.982 against 0.981).
   * **Consistency:** ember2024_malware_detection ships its version 3 vector the same way; the bins are no spectrum (no physical axis)[^clean26].
   * **Panel:** all agree to keep them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Plain columns (implemented) | the authors' vector as published | the field's representation; matches ember2024 | many low-information columns |
     | B | Declare them as feature groups | a grouped special feature | names the structure | no field default to encode them; departs from ember2024 |

   * **Recommendation:** A. **Decision:** A or B?

   [^clean26]: **CLEAN-26** (Should, by analogy): a spectrum ships as the source publishes it, one numeric column per
     position on its axis, and is declared as a special feature; hashed bins have no physical axis.

5. **Accept the missing-value-sentinel warning with this text?**

   * **Problem:**
     - `dataset check` warns that -1 dominates four hashed bins (`imports_library_hash_030` is -1 in 56.1% of files).
     - The -1 is a signed count of EMBER's hashing trick (`user32.dll` hashes to that bin with sign -1), a real value, not a missing code.
   * **Effect on the task:** none; the warning is a process item.
   * **Experiments:** the builder traced the -1 values to the hashed names.
   * **Consistency:** ember2024_malware_detection proposes the same acceptance on the curator's yes[^clean10].
   * **Panel:** uncontested.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept with the builder's text | written into `dataset.py` on yes | the check is clean; the reason is recorded | none found |
     | B | Leave it unaccepted (implemented) | the warning stays in the README | none found | an open warning on a value that is real |

   * **Recommendation:** A. **Decision:** accept the warning with this text, yes or no?

   **Notes for the AI:** on yes, add `accepted_check_warnings = {"dataset_missing_value_sentinel": "the -1 values are signed counts of EMBER's hashing trick (FeatureHasher alternate_sign: user32.dll hashes to imports_library_hash_030 with sign -1), not a missing code"}` to `dataset.py` and re-run `dataset check`.

   [^clean10]: **CLEAN-10** (Should): convert proxy missing values (`-1` among them) to real missing values when the
     encoding can be inferred; keep a code and say why when it means something.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate, critic, mediator; the rebuttal round was skipped under the budget rule, as the advocate's and the critic's briefs agreed on every fact and differed only on the curator's calls. Claim audit: one claim refuted (the sample independent of label and time: prefix 0 is 48.9% malicious against 50.5%; text fixed, the prefix is issue 1); every other tested claim holds. Blind review: would benchmark; main concerns the near-ceiling ROC AUC and the drift of the malicious share. Task gamer: no exploit; every trick within +-0.0002 ROC AUC of a noise column. Debate: agreed on the features, dropping the detection count and the 11 behaviour tags, the split without a gap under ROC AUC and the plain hashed blocks; disputed: the sample prefix (issue 1), the metric (issue 2), the first sighting to the minute (issue 3). Uncontested: the hashed blocks (issue 4) and the sentinel warning (issue 5).

<details><summary>Mediator: sorel_20m_malicious_pe</summary>

```text
Mediator: sorel_20m_malicious_pe (folder sorel_20m_malicious_pe_1m), 2026-11-09
Rebuttal round skipped (budget rule); briefs agree on every fact. No experiment re-run: no fact is disputed.

JUDGMENT RECORD
Verdict: ship after changes.
Validity: SEL-1, SEL-2, SEL-12 hold; USE-1 holds, fit approximate (USE-5 grey zone 2-4 absent, already in fit_reason;
  USE-8 collection-driven class mix); LEAK-10 triggered, fixed (detection count + 11 tags dropped); LEAK-16..20 hold
  (0 exact copies across the split); LEAK-24 not triggered; SPLIT-1/SPLIT-19 hold; SPLIT-10 measured, no gap under
  roc_auc. Sample representativeness (EV-1): claim 17 refuted (prefix 0 is 48.87% malicious vs 49.9-50.8% for 1-f,
  ~40k extra benign train files from Jul-Aug 2017 and Jun-Jul 2018; test windows unaffected, ratio 1.00-1.08).
  Text fixed now; prefix switch is the curator's (issue 1).
Value: TP flag `solved` (LightGBM 0.9973) benign: no leak (gamer: every trick within +-0.0002 of a noise column),
  best raw feature 0.859, families spread in log loss 0.053/0.078/0.134. MET-10 ceiling raised (issue 2).
Quality: CLEAN-12 decoded headers, CLEAN-5 33 constant bins, CLEAN-14 flags; hashed blocks kept plain (as ember2024).
Weighed: source +, shape +, gap 0, use case 0, risk - (unpublished labels, sha-ordered benign batch in train).
For the curator: issues 1-5 below (all weighing calls; none breaks a Must).

CHANGES TO MAKE NOW (no decision needed)
1. version_comment and claim 17: drop "depends on neither the file's label nor its time"; state that the hash is
   independent of the file, but the release's benign selection of Jul-Aug 2017 and Jun-Jul 2018 favoured low SHA-256
   values, so prefix 0 holds ~9.5% more benign training files than the average prefix (48.9% malicious against the
   release's 50.5%); test windows unaffected. Replace the wrong 49.5%/51.2%. (EV-1, EV-2; writing.md: the text must
   match the data.) Needed under either option of issue 1 until the prefix changes.
2. fit_reason: add that the hour and weekday of first_seen carry ReversingLabs' feed rhythm (alone ROC AUC
   0.605-0.626), kept as known at arrival. Precedent: ember2024's recommendation A carries this sentence (USE-8; treat
   like cases alike). Drop it if issue 3 floors to the day.
3. Dtype note: one sentence that header_coff_timestamp's 0 (1.83%) and dates after first_seen (2.6%) are values the
   file states, kept raw (CLEAN-10; column auditor Q1, uncontested).
Not a change: critic point 2 (grey zone in fit_reason) is already met (fit_reason lines 321-322).

WHY THE PREFIX SWITCH IS NOT A NOW-CHANGE
The problem resolved by a now-change is the false statement; change 1 resolves it. The remaining problem (a
sha-ordered benign batch in ~4% of the oldest train side) has no measured effect on any score; its rules are Should/
Weigh (EV-1, USE-8), not a validity Must. Switching costs 1-2 h (re-read 77 GB LMDB, check, probes) and changes
window sizes. Both are cheap and safe, so this is a weighing call (P5/P7 "fix when cheap and safe" vs no measured
harm), folded with the builder's size issue. Mediator leans to switching to "8" if the curator re-prepares anyway.

ISSUES FOR THE CURATOR (ranked)
1. [P5/EV-1 Should; version design] Sample prefix (and size).
   Problem: prefix 0 over-represents a sha-ordered benign batch from four training months; prefixes 0 and 1 are the
   only ones out of band. Effect: ~4% of the oldest train side; test untouched; ROC AUC effect likely small, unmeasured.
   Critic: switch to "8" (in band every month), re-prepare, re-probe: makes the sample what it claims.
   Advocate: reword (change 1), keep 0; switch only as part of the size call.
   Settles it: a fit on prefix 0 vs 8 with the same test windows (part of the 1-2 h re-run).
   Options: (a) keep 0, reworded; (b) "8" at 1/16; (c) 1/8 with two in-band prefixes (not "0"+"1": both out of
   band; e.g. "8"+"9"), memory ~2x (50+ GB check, 100+ GB probes).
2. [P6 MET-11 Must / MET-5 Should / MET-10 Weigh] Metric near ceiling.
   Problem: every family ROC AUC 0.975-0.997; TPR at 0.1% FPR moves by points (0.929-0.945).
   Critic + domain practitioner: partial ROC AUC max_fpr=1e-3 from the paper's "1 in 1000 or below" (Sec. 1); ~60
   FP per window, stable; needs MET-5 amendment (third exception) and new metric code (MET-13).
   Advocate + precedent checker: roc_auc; the source states a range, not one bound, so the bound would be ours
   (MET tension row: never invent a threshold the source did not fix).
   Not a Must failure: MET-11 is met by a fallback the source does not contradict; this is a weighing of the source's
   range against the ceiling. Decide on sorel's own facts (MET-10 amended 2026-11-02), not with ember2024.
   If (b): add a ~7-day gap (SPLIT-10; no-gap optimism +1.3-3.0 TPR points at 0.1% FPR) and restate the time
   feature's 0.1%-FPR effect (-0.57..+0.80 points) in issue 3.
3. [P3/P4 USE-6, USE-8 Should; LEAK-10 not triggered] first_seen to the minute.
   Problem: hour/weekday are one feed's rhythm (alone 0.605-0.626 AUC; +<=0.0008 AUC with the vector; gamer
   +0.0001-0.0002). Advocate: keep (known at arrival; as ember2024 A). Critic + practitioner: floor to the day (does not
   transfer to another vendor). Settled by who the actor is: the telemetry's owner (keep) or any vendor (floor). A
   linked per-dataset item next to ember2024's issue 2, not a joint call.
4. [process, CLEAN-10] Accept dataset_missing_value_sentinel with the builder's reason (-1 = signed hashing counts).
   Uncontested; written on the curator's yes, as ember2024 item 6.
5. [P7 CLEAN-26/24 by analogy] Hashed bins and histograms as plain columns: keep (all agree; as ember2024 item 4).
Record note: original_source Company vs definition Other (PROV-8): one record-vocabulary note with ember2024.

TASK GAMER EXPLOITS -> RULES
- Row position (+0.0001..0.0004): = first_seen order; LEAK-10 not triggered, maps to issue 3. Known (time-feature note).
- first_seen hour/minute/weekday (+0.0001..0.0002): USE-6, issue 3. Known; gain within the builder's stated <=0.0008.
- Duplicate counts, format features: no gain; LEAK-16..20, LEAK-13..15 hold. Known (builder: format 0.955 one vectoriser).
- sha256 lookup in the public release: EV-4/known for any public data; not ranked.
No new exploit; no measured gain differs from the notes. The definition has no `Potential leak, kept on purpose:`
note and needs none.

AGREED FACTS
1,251,351 rows (SHA-256 prefix 0 of 19.39M files with a vector), 2,322 features; check 0 errors, 1 warning; windows
99,209/77,057/89,466 (malicious 0.38/0.30/0.27), train 985,619/1M/1M, tiling the release's test set; 0 exact copies
across the split; grey zone 2-4 absent from all files; claim 17 refuted with the numbers above; LightGBM 0.9973, RF
0.9966, linear 0.9861; TPR at 0.1% FPR 0.929-0.945; time features alone 0.605-0.626, +<=0.0008 with the vector;
no-gap optimism +0.00006-0.0007 AUC, +1.3-3.0 TPR points at 0.1% FPR; authors' LightGBM 0.981 on our windows.

CONSISTENCY
Follows ember2024 on roc_auc (as implemented), time feature kept (A), hashed blocks, sentinel warning, no gap,
LEAK-10 drops. Departures from the builder's draft corrected per the precedent checker: metric and time feature are
decided on sorel's own facts (MET-10 amended 2026-11-02), as linked items. Change 2 closes the fit_reason gap against
ember's A. If partial AUC is chosen for either dataset it is the third MET-5 exception: propose an amendment instead.
```

</details>

<details><summary>Claim audit: sorel_20m_malicious_pe</summary>

```text
Claim auditor: sorel_20m_malicious_pe_1m (2026-11-09)
Verdict: ship after one wording fix (or a one-line prefix change). One claim refuted (claim 17: "the sample is
independent of label and time"); every other claim tested held. No validity Must broken; the test windows are untouched.

Only meta.db and the sha256 column of the prepared parquet were read; no full probe was re-run.

TABLE (claim | source | test | result | evidence | rule)
1 | claim 17, version_comment ("the sample depends on neither the file's label nor its time") | malicious share and count of
  benign files by the first hex digit of sha256, for the whole release (16 prefixes) and by month (prefixes 0, 1, 8) |
  REFUTED | prefix 0: 48.87% malicious against 49.9-50.8% for prefixes 1-f (release 50.51%; z = 37 for n = 1.27M).
  Malicious counts are flat over the prefixes (~537k before the test period, ~85k in test). Benign files before the test
  period: prefix 0 464,596, prefix 1 440,020, prefixes 2-f 423-428k. So prefix 0 holds about 40k extra benign files
  (+9.5%), all in the training period, packed into a few months. Benign files of prefix 0 / prefix 8: 2017-07 9,952 /
  2,370 (4.2x), 2017-08 1.9x, 2018-06 1.75x (45,646 / 26,059), 2018-07 1.17x (prefix 1 also high: 53,549); other months
  0.87-1.13x; test months 1.00-1.08x. Within prefix 0 the excess is spread over all second digits (00-0f: 39-42k
  against 37.9k for 8x), so it follows lexicographic sha order (a selection by sorted SHA-256 in the release's benign
  sampling of those months), not a feature of the files. The claim's own numbers (49.5% against 51.2%) differ from the
  data (48.9% against 50.5%). | SEL / sampling representativeness, EV-1
2 | claims 20-21, splits_comment: window sizes, malicious shares, train sides | recomputed from meta.db joined to the
  parquet keys | HOLDS | test windows 99,209 / 77,057 / 89,466 (oldest first), malicious 0.380 / 0.298 / 0.270; earlier
  files 985,619 / 1,084,828 / 1,161,885 (so 985,619 / 1M / 1M); 0 files after the last window; the cutoff second
  (07:54:00) falls into test, as in config.py (< split = validation) | SPLIT-1, SPLIT-19
3 | claim 9: first_seen to the minute, range 2017-01-01 to 2019-04-11 03:59 | rl_fs_t % 60 | HOLDS | 0 non-whole minutes;
  min 2017-01-01 00:01, max 2019-04-11 03:59 | USE-3
4 | claim 11 / Decision 1: grey zone 2-4 absent, benign 0-1, malicious 5-28 | release_counts.json + sample crosstab |
  HOLDS | no file of either label with 2-4 detections; in the sample benign 0: 355,262, 1: 277,148, malicious >= 5 only |
  LEAK-10, USE-5
5 | claim 15/16: release counts | release_counts.json | HOLDS (consistent: 12.91M train files in meta.db, 12.70M with a
  vector, matching Table 1) | PROV-13
6 | claim 35 / curation note on first_seen | time_feature.json | HOLDS as written (ROC AUC 0.605-0.626; +0.1-0.4 TPR
  points at 1% FPR). Not written: at 0.1% FPR the time moves the TPR by +0.47 / +0.80 / -0.57 points, the same order as
  the "gap" effect (1.3-3.0) and as the families' differences there. This matters only if the curator takes issue 1(b)
  (partial AUC); then it belongs in issue 2 | LEAK-10, USE-6, MET-11
7 | metric: fallback roc_auc (claim 33) | paper.txt lines 41, 57, 71, 171; plot.py; README | HOLDS: the paper names no
  single metric. It speaks of "lower false positive rates (1 in 1000 or below)", a range, so MET-5/MET-7 apply. MET-2:
  every test window holds >= 22,985 of the smaller class; per-row unit; no scoring column | MET-1, MET-2, MET-5, MET-7
8 | builder: "1 warning proposed for acceptance" (dataset_missing_value_sentinel) | grep dataset.py; README front matter |
  OPEN (not refuted): `accepted_check_warnings` is absent from dataset.py and README `accepted: {}`, so the warning is
  still unaccepted. A curator call, not a defect | process
9 | claims 24 (exact copies), 26-29 (layout, decoding, constants), 23 (no gap), 36 (probe 13), 37 (authors' model 0.981) |
  builder probes | UNTESTED by me: no re-run under the memory cap; the builder's numbers in experiments.json,
  time_feature.json and drift_check.json agree with the text where I read them | -
10 | implied: every feature is known at the first sighting | dataset.py drops rl_ls_const_positives, 11 tags, sha256,
  rl_fs_t; the rest is EMBER v2 from the bytes | HOLDS by construction (header_coff_timestamp is stated by the file) | LEAK-10

RANKED (refuted / open)
1. Claim 17 refuted (sample validity, Should-level, not a leak). What it changes: the 1/16 sample is not a random
   sixteenth. Its training side carries ~40k extra benign files from four months (Jul-Aug 2017, Jun-Jul 2018), about 4%
   of the oldest train side. These are batches the release picked by sorted SHA-256, so the training class mix and the
   benign population of those months are those of a sha-ordered slice. The test windows are unaffected (ratio 1.00-1.08).
   Effect on ROC AUC is likely small, but the text claims an independence the data refute.
   Mildest remedy: (a) correct the version_comment and claim 17. Say the hash is independent of the file, but the
   release's benign selection of Jul-Aug 2017 and Jun-Jul 2018 favoured low SHA-256 values, so prefix 0 holds ~9.5%
   more benign training files than the average prefix (48.9% malicious against 50.5%). (b) Better and still cheap: set
   SAMPLE_PREFIX to a digit in the band (e.g. "8": ratio about 1 in every month) and re-run the prepare step (4-40 min).
   Window sizes change slightly and the probes need re-running. Prefixes 0 and 1 are the only ones out of band.
2. Accepted warning still open (item 8): add accepted_check_warnings with the builder's reason if the curator agrees.
3. Time feature at low FPR (item 6): only relevant if issue 1(b) is chosen; then state the 0.1%-FPR effect
   (-0.6 to +0.8 points) in issue 2.

On the builder's draft issues: 1 (metric near its ceiling) and 2 (time feature) stand as framed. 3 (1/16 sample size)
should absorb finding 1: if the prefix changes, decide it together with the size.
```

</details>

<details><summary>Column audit: sorel_20m_malicious_pe</summary>

```text
Column auditor: sorel_20m_malicious_pe (folder sorel_20m_malicious_pe_1m), 2026-11-09
Prediction point: the file's first sighting in ReversingLabs telemetry (rl_fs_t). Codebook: EMBER v2 features.py (layout
in dataset.py's vector_columns), SOREL README/paper. Own run: the first 200,000 rows of the prepared parquet joined to
meta.db (4 threads). Full probes were not re-run; I read the builder's probe outputs instead.

VERDICT: no leak among the shipped columns; no cleaning problem that blocks shipping. One question for the curator (Q1), and
I weigh in on builder issue 2.

COLUMN TABLE (by block; 2,322 features)
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
is_malicious (target) | Sophos label | after (target) | No/Yes category | fine | CLEAN-25
first_seen | time of first sighting, UTC, to the minute | yes, it is the prediction point | datetime | fine; hour-of-day signal is builder issue 2 | LEAK-10 not triggered, USE-6
byte_histogram_000..255 | share of each byte value in the file | yes, from the file's bytes | float, normalised per file | fine | CLEAN-26 not applied (no physical axis)
byte_entropy_histogram_e*_b* (256) | joint histogram of window entropy and byte | yes | float | fine | same
strings_count/mean_length/printables/char_share_20..7f/char_entropy/n_paths/n_urls/n_registry/n_mz | statistics of the printable strings | yes | float; counts held as numbers | fine (strings_n_mz min 1: the file's own MZ) | CLEAN-14
general_size, general_vsize, general_n_exports/imports/symbols | file size, virtual size, counts | yes | float32 (integers above 2^24 rounded at the source) | fine | CLEAN-14
general_has_debug/relocations/resources/signature/tls | 0/1 flags | yes | categorical 0/1 | fine (has_signature: 29% of benign, 9% of malicious files; a real signal) | CLEAN-12 table, CLEAN-14
header_coff_timestamp | compile time the file states (epoch seconds) | yes, written in the file (can be faked) | number | question Q1 | CLEAN-10, CLEAN-14
header_coff_machine, header_optional_subsystem, header_optional_magic | decoded LIEF names; missing for the 119 files LIEF could not parse | yes | category; collisions joined with " / " | fine; restores meaning | CLEAN-12
header_characteristics_hash_*, header_dll_characteristics_hash_* | multi-name flag sets hashed into 10 signed bins | yes | numeric | fine (multi-name fields can't be decoded one-to-one) | CLEAN-13
header_optional_* (11) | image/linker/OS/subsystem versions, sizeof_code/headers/heap_commit | yes | number | fine. The dtype probe flagged sizeof_code (`code_name`): it is a byte count, so numeric is right. The version fields are numeric version numbers (up to 64,986), so numeric is right too | CLEAN-14
section_count, section_n_zero_size/n_empty_name/n_read_execute/n_write | section counts | yes | number | fine | -
section_{size,entropy,vsize}_hash_00..49 | per-section values hashed by section name | yes | numeric | fine | CLEAN-13
section_entry_name_hash_*, section_entry_props_hash_* (21 + 27 kept) | entry section's name and properties, hashed | yes | numeric, signed | fine; the 33 all-zero bins were dropped | CLEAN-5
imports_library_hash_000..255, imports_function_hash_0000..1023, exports_hash_000..127 | imported/exported names, hashed with signs | yes | numeric; -1 is a signed count, not missing | fine; the builder's proposed accepted warning is right | CLEAN-10 not applicable
datadir_*_size / _virtual_address (30) | PE data directories | yes | number | fine | -
Dropped: sha256 (identifier, CLEAN-3); rl_fs_t (now first_seen); rl_ls_const_positives and the 11 tags (post-sighting, define the label: LEAK-10); the 30 hashed one-name blocks (decoded); 33 constant bins. All correct.

PROBLEMS, RANKED
1. (P4, question, weak) first_seen hour of day: AUC 0.605-0.626 on its own, +0.0008 at most with the vector. It is known at
   arrival, so it is not a leak. It is still a property of the feed rather than of the file. I agree with the builder's
   issue 2: decide it together with ember2024. Mildest remedy, if the task should stand for any vendor's detector: floor
   first_seen to the day.
2. Q1 (P7, question, minor) header_coff_timestamp: 1.83% of files have 0 (not set). 2.6% are dated more than a day after
   first_seen, which is impossible for a real compile time: these are faked timestamps or the hashes that reproducible
   builds write there (benign 4.3%, malicious 0.8%). The maximum is 4.29e9 (0xFFFFFFFF). These are values written in the
   file and a static detector reads them as they are, so keeping them raw is defensible (CLEAN-10 keeps a code that
   carries meaning). Do not set them to missing: the class difference is real signal from the file. Mildest remedy: keep,
   and add one sentence to the dtype note that 0 and dates after the sighting are values the file states, not errors.
3. None otherwise. There are no proxy missing codes in the non-hashed columns (no negatives) and no reversed encodings.
   No ordinal columns. All flags are 0/1. The builder's issues 1, 3 and 4 are not column issues; on issue 4 I agree
   with keeping the hashed bins and histograms as plain columns.
```

</details>

<details><summary>Split audit: sorel_20m_malicious_pe</summary>

```text
Split auditor - sorel_20m_malicious_pe (folder sorel_20m_malicious_pe_1m)
Verdict: RIGHT WITH NOTES. No new experiments run (builder's experiments.json already holds the alternative-split fits
at 200k rows; the memory note asked not to repeat the probes).

Regime. Use case: a detector scores each new file on first sighting and is refit monthly on older files. That is a
stream over time; files are unique by SHA-256, so no recurring entity to group on. Declared: temporal on first_seen
(ReversingLabs first-seen time = the prediction point), 3 x 30-day windows newest first, horizon 30 days, no gap.
Matches (SPLIT-1, SPLIT-19). Malware families recur across time as hidden groups, but recurrence is what the deployed
detector meets in a stream, so a family-grouped split would misstate the use case; not recommended.

Windows (experiments.json): starts 2019-01-12 07:54, 02-11, 03-13 (the release's own VALIDATION_TEST_SPLIT), test
99,209 / 77,057 / 89,466 rows, train before 985,619 / 1,084,828 / 1,161,885 (capped at 1M random of earlier rows,
one order for all windows). Three windows tile the source's 88-day test period (90 days declared; the last data week
2019-04-13 is partial, 174k files vs ~340k, so the newest window ends with the data - fine). Malicious share per window
0.38 / 0.30 / 0.27: shift, not season; no season-shaped test window problem with 30-day windows.

Findings, ranked:
1. (P4, note) Gap vs label delay, SPLIT-10. A real refit at a window start would not yet have settled labels for the
   last days/weeks of files (detections accumulate). Shipped split has no gap. Builder's equal-size test (200k,
   2 seeds, 3 windows): training up to start vs 30 days before adds +0.00006 to +0.0006 ROC AUC (seed 0: 0.00006,
   0.00049, 0.00058) but +0.7 to +1.3 TPR points at 1% FPR and +1.3 to +3.0 at 0.1% FPR. Under the ROC AUC metric the
   optimism is negligible: no gap is acceptable. If the curator picks a low-FPR TPR metric (open metric issue,
   shared with ember2024), the optimism is 1-3 points; mildest remedy then: a gap of ~7 days (labels settle within
   days to weeks; release documents no delay figure). Tie this to the metric decision.
2. (P4, note) Training rows whose label was not known at the prediction point: same mechanism as 1 (all labels final
   Dec 2020). Not separable without per-file detection timelines, which the release lacks; covered by 1.
3. (P3, note) Train history composition: train's malicious share swings 74-93% (2017-mid 2018) to 26-40% (Sep 2018+);
   a model sees a prior unlike the test months. A genuine trait of the source's sampling, already in the README's
   anomaly; ROC AUC is prior-insensitive. No change.
4. Near copies across split: 0 / 2 / 1 test rows with an exact earlier vector copy, none malicious; 155 rows in 58
   copy groups overall, no conflicting labels (LEAK-16..20 hold). No filter needed.

Builder's draft issues weighed: issue on first_seen as feature (hour/weekday AUC 0.60-0.63, adds <=0.0008 with the
vector) is not a split problem; agree it is the curator's call with ember2024. Split choice and windows: agree.
```

</details>

<details><summary>Domain practitioner: sorel_20m_malicious_pe</summary>

```text
Domain practitioner report: sorel_20m_malicious_pe_1m (2026-11-09)
Actor: a security vendor's static-detection team (PE classifier at first sighting, refit monthly), per task_summary.
Sources: dataset.py, README.md, builder_report.md and its probes (no new experiments run: the builder's numbers answer
my questions); SOREL-20M paper arXiv 2012.07634 Sec. 1 and the release's plot.py (as cited by the builder).

FIT: approximate. The inputs and the monthly temporal test match a vendor's static detector, but the label drops the
grey zone and the class mix and metric do not reflect the low-FPR operating point the vendor acts on (USE-1, USE-5, USE-8).

1. Inputs at prediction time (USE-3, USE-6): yes for all 2,381 EMBER values; they are computed from the file's bytes.
   Nothing I always have is missing for a purely static detector. In practice I would also have the file's signer and
   certificate validity, its prevalence across customers and the reputation of where it came from. These are outside
   the static scope, so I accept leaving them out. The hour and weekday of `first_seen` describe ReversingLabs' feed
   rhythm (alone 0.61-0.63 AUC). My own telemetry has a different rhythm, so I would not want a model to lean on it.
   I support builder issue 2 option (b), flooring to the day: it adds at most +0.0008 AUC and transfers to no other vendor.
2. Target (USE-5): a proxy. I act on "block or not". The label is >=5 vs <=1 AV detections 20 months later, and the
   2-4 grey zone is removed. Those grey-zone files (PUA/adware, fresh malware with few detections) are exactly the
   hard ones my detector meets at first sighting. Removing them makes the task easier than deployment and explains part of
   the 0.997 ceiling. I want a calibrated probability so I can set my own threshold. Binary is right.
3. Row = one file = one block/allow decision: yes. Test = next 30 days after a training cut: yes, this is my monthly refit
   (SPLIT-1, SPLIT-19). Gap: in deployment the newest labels are not final when I refit. The dataset trains on labels
   that were final 20 months later, so the dataset is optimistic about freshness. The builder measured that the last 30
   days add only 0.0007 AUC, so this gap is small (SPLIT-10).
   Class mix (USE-8): the malicious share is about 25-40% in the test windows. A real endpoint stream is overwhelmingly benign, so any
   precision or alert-volume reading at this mix would mislead. ROC-based scores do not depend on prevalence, which
   helps here.
4. Would I use the model: I would use it as a candidate ranker. I would trust it if its TPR at FPR 1e-3 and 1e-4 holds over
   successive windows. I would distrust a model whose edge comes from the time-of-day feature or from near-duplicate
   variants (the 1-NN agreement of 0.996 in the closest tenth means part of the score is family memorisation, which is real but
   flatters the model).
5. Metric (MET-1, MET-6, MET-7): partly. Full ROC AUC ranks probabilities without regard to prevalence, which is good. But almost
   all of its area lies at FPRs I would never deploy (1-100%). The source names "1 in 1000 or below" (Sec. 1), and
   plot.py reads 1e-5 to 1e-1. Every family scores 0.975-0.997 on ROC AUC, so it hardly separates models in my region,
   while TPR at FPR 0.1% moves by points (0.929-0.945) (MET-10). I would choose the standardized partial ROC AUC with
   max_fpr=1e-3 (roc_auc_score(max_fpr=0.001)), which is the cost-free form of "TPR at 1-in-1000 FPR" (MET-7, MET-9). Over
   ~60k benign test files per window, an FPR of 1e-3 is about 60 false positives, enough for a stable estimate.
   1e-4 is too noisy at this size. I support builder issue 1 option (b), decided together with ember2024.

Gaps ranked by how much they change the task:
 (1) Metric scores the whole ROC curve, not the low-FPR operating point (changes which model wins).
 (2) The grey zone (2-4 detections) is removed from the label, so the hard cases are absent.
 (3) The hour of `first_seen` is a feed artefact of one vendor.
 (4) The class mix follows the collection, not deployment.
 (5) Labels are final before refit (measured negligible).
What a domain expert would change: pAUC at FPR <= 1e-3 as the metric; `first_seen` floored to the day; a note in fit_reason
that the grey zone is absent and test AUC overstates deployment. Keep everything else.
```

</details>

<details><summary>Blind review: sorel_20m_malicious_pe</summary>

```text
Verdict: include with changes - a real, honest temporal malware-detection task, but nearly saturated (AUC ~0.997) and with heavy label-prior drift over time.
Task: Sophos SOREL-20M, EMBER v2 static PE features (2,318 numeric + 3 header categoricals); predict whether a Windows executable is malicious at first sight, as an AV/EDR scanner would. Real use.
Concerns (ranked):
1. Near-trivial: LightGBM 300 trees, train on the oldest 80% of a 200k sample, test on the newest 20%: AUC 0.9973. Gaps between methods will be very small. Reporting log-loss or TPR at low FPR (the paper's metric) would separate methods better than AUC.
2. Label prior shifts with time: malicious share is about 75-90% for 2017 through May 2018, then about 30-45% from June 2018 on (for example 2018-10: 12,341 No vs 4,919 Yes). The temporal test windows therefore measure prior shift as well as concept drift. Say so in the task docs, or rebalance.
3. The 1.25M rows are a subsample of the 20M files. task.md does not say how they were drawn (stratified? by time?). Document the sampling.
4. first_seen is kept as a column. That is fine for splitting, but the docs must say whether it is dropped from the model features. header_coff_timestamp (the compile time) is the top feature. It is legitimate, but it carries time.
5. Minor: 9 duplicate feature rows in 200k; 3 columns have NaNs; categoricals look sane (header_optional_magic has an empty 'unnamed' level). No constant columns.
Not checked: the full 1.25M rows; the builder's probe outputs (not opened, to keep the clean-room rule); the source's label definition (vendor-vote threshold) against the target.
```

</details>

<details><summary>Task gamer: sorel_20m_malicious_pe</summary>

```text
SOREL-20M task gamer report
Verdict: no exploit found; every gain is within the noise of a random-number column (about +-0.0002 AUC).
Setup: 50k random training rows and 25k random test rows per split (215k rows in total). LightGBM with 300 trees, 63 leaves, colsample 0.3, 4 threads. Scored with score.py on the sampled test positions.

AUC per split (r0, r1, r2):
 honest baseline without first_seen        0.99701 0.99673 0.99722
 baseline with first_seen (as shipped)      0.99708 0.99664 0.99731
 + random column (noise check)              0.99692 0.99684 0.99701   spread about +-0.0002
 + row position                             0.99716 0.99686 0.99758   +0.0001..+0.0004; rows are sorted by first_seen, so this is first_seen again
 + first_seen hour/minute/day of week       0.99723 0.99678 0.99745   +0.0001..+0.0002; known at the prediction point, so signal, not an exploit
 + count of identical rows (train+test)     unchanged (no duplicates)
 + format features (zero count, NaNs, share of whole numbers)  0.99714 0.99678 0.99712   noise
 honest: train only on rows from 2018-07 on 0.99636 0.99592 0.99710   worse, so the old training rows do not hurt the model

Findings
- Exact copies across the split: none in the sample (0 of 75k test rows match a training row). SOREL is deduplicated by sha256.
- Label drift: the malicious rate is 0.92 in 2017Q4 training rows, 0.32-0.43 in 2018Q4-2019Q1, and 0.27-0.38 in the test windows. AUC does not depend on base rate, and the honest fix (recent rows only) scores worse.
- Each feature alone on the test rows: first_seen hour has AUC 0.38 in r0 and 0.62 in r2, which is a feed artefact but legitimately available. Every other feature alone is between 0.44 and 0.57.
- Labels in SOREL come from later vendor rescans. That is the target definition, not a leak in the features.
- Web search: no published leak or "magic feature" threads for SOREL-20M. Looking rows up by sha256 in the public release is possible, as for any public dataset; not ranked.
Not checked: full-size training (memory limit); near-duplicate (not exact) copies via nearest neighbours; a train-vs-test adversarial classifier.
```

</details>

<details><summary>Precedent checker: sorel_20m_malicious_pe</summary>

```text
Precedent checker: sorel_20m_malicious_pe (folder sorel_20m_malicious_pe_1m), 2026-11-09
Sources: dataset.py / README.md (df-large), record, builder_report.md, register.json, metrics.md Cases table,
ember2024_malware_detection_1m/REVIEW.md (the sibling, panel of 2026-11-09, still open).

VERDICT: the definition's calls are consistent with precedent. Two of the builder's draft recommendations depart
(issue 1 and, in its framing, issue 2), with no fact to set them apart. One small gap against the sibling's
pending recommendation (fit_reason). No drift found.

1. Metric: fallback roc_auc (MET-5, MET-10, MET-11). The definition is CONSISTENT: ember2024 (A implemented),
   naticusdroid, ugr16 and website_phishing all ship roc_auc.
   The builder's recommendation "(b) as one call for both datasets, decided together with ember2024" DEPARTS
   from MET-10 as amended on 2026-11-02 (Andrej; metrics.md Cases row MET-10: "no family call on the metric,
   each table's metric is decided on its own"). The ember panel already settled this: "decide together with
   sorel is ruled out ... sorel later on its own (its paper says 1e-3)". MET-10 is a Weigh rule and the
   amendment is the curator's own, so no exception without a stated reason.
   - Also: if partial AUC is taken for EITHER dataset, it is a third exception to MET-5 (after
     protein_model_quality_rf_pcp and huesken_sirna_efficacy). That asks for an amendment of MET-5, not another
     exception (principles.md, Exceptions).
   - Sorel's facts differ from ember's: the paper states a range ("1 in 1000 or below", Sec. 1), and plot.py
     reads TPR from 1e-5 to 1e-1. It gives no single bound like thrember's max_fpr=5e-3 selection criterion. So
     a context bound is weaker here than for ember.
   - Reflection prompt, drafted as an issue:
     Keep the ROC AUC for sorel, or score only the low false positive rates, decided on sorel's own facts?
     **Problem:**
     - Every family scores ROC AUC 0.975-0.997 (LightGBM 0.9973). TPR at 0.1% FPR moves by points
       (0.929-0.945).
     - The builder proposes deciding this together with ember2024, which MET-10 (amended 2026-11-02) rules out.
     - SOREL names a range of FPRs, not one bound.
     | | Option | Pro | Con |
     | a | roc_auc, decided alone (implemented). Distinguishing fact: SOREL gives no single FPR bound, so a context bound would be ours | rule as written; matches ember (as implemented) and three other security sets | ranks near the ceiling |
     | b | partial AUC with max_fpr=1e-3, from the paper's "1 in 1000", decided alone | scores where the vendor operates | third MET-5 exception, so an amendment is due; the bound is a reading of a range; new metric code (MET-13) |
     | c | follow ember's outcome as a family call | one rule for the pair | breaks MET-10 as amended |
     Recommendation: a, decided per dataset. If the curator amends MET-5 on ember, re-judge sorel under the
     amended rule, on its own facts.
     [MET-5 Should] [MET-10 Weigh, amended 2026-11-02] [MET-11 Must] [principles.md Exceptions]

2. Time feature first_seen kept to the minute (USE-6, USE-8; LEAK-10 not triggered). The definition is
   CONSISTENT: it matches ember2024 option A (implemented), and the effect is the same size (alone 0.605-0.626
   here, 0.58-0.60 there; with the vector at most +0.0008 AUC).
   - "One call with ember2024" is allowed here only as linked per-dataset items. This is a weighing call, not a
     metric, and the ember REVIEW.md already says that on B/C a matching item goes into sorel's REVIEW.md
     (memory rule: per-dataset choices are their own issue in each REVIEW.md). Draft it that way, not as a
     joint decision.
   - GAP: ember's recommendation A comes with "name the submission rhythm as a kept artefact in fit_reason"
     (USE-8). Sorel's fit_reason does not name the hour-of-arrival signal; it is only in a note. For a like
     decision, add the same sentence to fit_reason.

3. Size (1/16 by SHA-256 prefix): no direct precedent conflict. It is a version design within the 1M/500k
   budgets. CONSISTENT with the _1m convention (ember2024_malware_detection_1m, numerai_v5_2_1m and others).

4. Hashed bins and histograms as plain columns (CLEAN-26/CLEAN-24 not applied): CONSISTENT with ember2024
   (item 7, uncontested, kept).

5. Other calls:
   - Constant columns (CLEAN-5): the 33 bins are judged on the fixed SHA-prefix sample, which is the task's row
     set and is deterministic. So the drop holds under either option of ember's open issue 3 (all task rows vs
     drawn rows). Note: if ember chooses B, nothing changes here.
   - accepted_check_warnings for dataset_missing_value_sentinel: same reason as ember item 6 (CLEAN-10).
     CONSISTENT; write it on the curator's yes, as there.
   - LEAK-10 drop of the detection count and tags: CONSISTENT with the register's LEAK-10 cases (columns that
     define the label).
   - SPLIT-10 no gap: CONSISTENT with ember (measured, stated).
   - source="Other" vs record "Company": the same kind of record/definition mismatch as ember (Other vs
     HuggingFace). Treat both the same way in one record-vocabulary note.

Drift: none. Lennart's 2026-11-08 CC lines decide the pair as "same task, another source, both enter"
(principles.md Tensions), and both definitions follow it. Third exception of a kind: only on the metric, if
partial AUC is chosen (see 1).
```

</details>

<details><summary>Advocate: sorel_20m_malicious_pe</summary>

```text
Advocate opening brief: sorel_20m_malicious_pe (folder sorel_20m_malicious_pe_1m), 2026-11-09
Position: ship as defined, with two changes that need no decision (fix claim 17's wording; record the accepted
sentinel warning). Every open item is a curator weighing call; none breaks a validity Must.

1. Real, defensive use case with a split that matches it. Static PE detector at first sighting, refit monthly; temporal
   split on first_seen, three 30-day windows that tile the release's own test set (99,209 / 77,057 / 89,466 rows,
   train 985,619 / 1M / 1M). Split auditor: RIGHT; domain practitioner: inputs all available at prediction time,
   row = one block/allow decision. Rules: SEL-1/SEL-2 (Must), USE-1, SPLIT-1/SPLIT-19 (Must). Outranks any
   "family-grouped split" or "rebalance" objection: recurrence over time is what the deployed detector meets
   (split auditor), and validity Musts outrank value/quality Weigh calls.
2. No leak, confirmed independently four times. LEAK-10 fixed by construction (detection count + 11 tags dropped);
   task gamer: no exploit, every trick within +-0.0002 AUC of a random column; 0 exact copies across the split
   (0/75k gamer, 0.0% of 265,732 builder); column auditor: no leak among 2,322 columns. Rules LEAK-10, LEAK-16..20
   (Must). The "solved" flag (LightGBM 0.9973) is therefore a ceiling question, not a validity one.
3. Metric: keep roc_auc (MET-5 Should; MET-10 Weigh as amended 2026-11-02, per-dataset). SOREL names a range
   ("1 in 1000 or below") and no single bound, so a partial-AUC bound would be ours and a third MET-5 exception
   (precedent checker). Families still separate in log loss (0.053 / 0.078 / 0.134). Concession: ROC AUC ranks near
   the ceiling; mildest remedy is a REVIEW.md item to re-judge if MET-5 is amended on ember2024, not a block.
4. Time feature: as ember2024 option A (implemented) - PREC consistency. Effect at most +0.0008 AUC with the vector
   (builder, gamer +0.0001..0.0002); hour of day is known at prediction (USE-6, LEAK-10 not triggered). The
   practitioner's day-flooring is a mild, optional change; it is not a reason not to ship.
5. Claim 17 refuted (claim auditor: prefix 0 = 48.9% vs 50.5% malicious, ~40k extra benign train files, ~4% of the
   oldest train side; test windows unaffected, ratio 1.00-1.08). Real; Should-level (SEL/EV-1), not a leak. Mildest
   remedy: correct the version_comment (no decision). Switching SAMPLE_PREFIX to "8" is the next rung, folded into
   builder issue 3 (sample size), the curator's call.
6. Label prior drift (75-90% -> 27-38% malicious) and the dropped 2-4 grey zone are traits of the source, documented
   in the README; ROC AUC is prior-insensitive and "recent rows only" scores worse (gamer 0.9959-0.9971). USE-5/USE-8
   are fit "approximate", which is a Weigh, not a Must; remedy is documentation, already present.
7. Label-delay gap: measured, +0.00006..0.0006 AUC (SPLIT-10); no gap is right under ROC AUC. Only if the metric
   changes to low-FPR does a ~7-day gap follow (split auditor) - tied to point 3, independent of shipping.
```

</details>

<details><summary>Critic: sorel_20m_malicious_pe</summary>

```text
Critic, opening brief: sorel_20m_malicious_pe (folder sorel_20m_malicious_pe_1m), 2026-11-09
Position: ship only after changes 1-4. I do not argue for exclusion: the task is real (SEL-1/2/12, USE-1 hold), no leak was
found (task gamer, column auditor, leak probes), the split matches the use case (split auditor).

1. The sample is not what it says it is (validity of the row set; EV-1, USE-8 Should; claim 17 refuted).
   Problem: version_comment claims the SHA-256 prefix-0 sixteenth "depends on neither the file's label nor its time". The
   claim auditor measured otherwise: prefix 0 is 48.87% malicious against 49.9-50.8% for prefixes 1-f (z = 37); ~40k extra
   benign files (+9.5%) in the training period, packed into Jul-Aug 2017 (4.2x prefix 8 in 2017-07) and Jun-Jul 2018
   (1.75x). The release picked benign files of those months in sorted-SHA order, and prefix 0 is the most exposed slice.
   Effect: the training history (about 4% of the oldest train side) carries a sha-ordered benign batch, not the month's
   population; test windows are unaffected (1.00-1.08x). Small on ROC AUC, but the shipped text states a false fact.
   Remedy (mildest that makes the claim true): SAMPLE_PREFIX = "8" (in band every month), re-run prepare (4-40 min) and the
   probes; fold into builder issue 3. Fallback if refused: correct the comment and claim 17 with the measured numbers.

2. The label drops the hard cases; the shipped text must say so (USE-5, USE-8 Should).
   Problem: the target is >=5 vs <=1 detections 20 months later; the 2-4 grey zone (PUA, fresh low-detection malware) is
   absent from all 19.7M files (claim auditor item 4). The domain practitioner: these are exactly the files a detector
   meets at first sighting; their absence explains part of the 0.997 ceiling.
   Remedy: one sentence in fit_reason (not only the notes) that the grey zone is absent and test scores overstate deployment.

3. The metric does not score the decision the source names (MET-11 Must: metric fits the decision; MET-10 ceiling).
   Problem: every family scores ROC AUC 0.975-0.997 (LightGBM 0.9973 +- 0.001); nearly all the area lies at FPRs a vendor
   never deploys. The source: "1 in 1000 or below" (paper Sec. 1), plot.py reads TPR at 1e-5..1e-1; TPR at 0.1% FPR
   moves by points (0.929-0.945). Practitioner would pick roc_auc_score(max_fpr=1e-3); ~60 FP per window at 1e-3, stable.
   Remedy: decide on sorel's own facts (MET-10 as amended 2026-11-02: no family call with ember2024) for partial ROC AUC,
   max_fpr = 1e-3 (the bound the paper's sentence names). I accept this is a third MET-5 exception and so needs an MET-5
   amendment (principles.md Exceptions); if the curator declines, keep roc_auc and state the ceiling in the notes.

4. The hour of first_seen is one feed's rhythm, not a property of the file (USE-6, USE-8 Should).
   Problem: hour/weekday alone ROC AUC 0.605-0.626; adds <= +0.0008 AUC, but at 0.1% FPR moves TPR -0.57..+0.80 points
   (claim auditor item 6), the order of the families' differences in the region of point 3. Practitioner: transfers to no
   other vendor. Precedent gap: ember's recommendation A requires naming the arrival rhythm in fit_reason; sorel's does not.
   Remedy: floor first_seen to the day in _clean (keeps windows and trend). Minimum if kept: the fit_reason sentence, as
   ember. Decide as a linked per-dataset item, not a joint call.

5. If point 3 is taken, the no-gap split becomes optimistic (SPLIT-10 Should).
   Problem: training up to the window start vs 30 days before: +0.00006-0.0006 AUC but +1.3 to +3.0 TPR points at 0.1% FPR
   (split auditor 1). Labels were final 20 months later; a real refit has unsettled recent labels.
   Remedy: tie to point 3: with a low-FPR metric, a ~7-day gap; with roc_auc, no change.

6. Process: the proposed accepted warning is not written (claim auditor item 8): dataset.py has no
   accepted_check_warnings, README accepted: {}. Remedy: write the builder's reason on the curator's yes (CLEAN-10, as ember).

7. Quality notes (do not block): header_coff_timestamp holds 0 (1.83%) and dates after first_seen (2.6%; benign 4.3%,
   malicious 0.8%); keep raw, one sentence in the dtype note (column auditor Q1, CLEAN-10). Record original_source Company
   vs definition Other: one record-vocabulary note with ember (PROV-8).
```

</details>
