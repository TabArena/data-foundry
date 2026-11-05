# duolingo_spaced_repetition_recall

**Outcome:** added as `duolingo_spaced_repetition_recall_1m_clf`; retain the prior approved session-performance task after the current-main focused recheck. Predict the probability of at least 75% correct using numerical session_seen and prior/context, scored by AUROC on the same temporal holdouts. The new measured future-counter shortcut is an evaluation leak addressed by the current train-only, own-row prediction protocol; benchmark method checking remains required.

**Main points:** No new curator decision remains. Preserve the November 3 inclusion and metric choices and the November 5 instruction to reuse past decisions. The target, eight predictors, equal weights, three one-day windows, one-day gap and 1M/111111 caps are unchanged. Each test prediction must use the fixed training-side model and its own covariates only; other test rows cannot enter any feature, learned transform or inference step. Do not interpret a clean dataset build as downstream enforcement.

**Record judgment:** The record and definition agree. IDs 1-5 stay closed historical decisions, with their dated discussion retained in the record; they are not reopened or reused. Issue 6 below preserves final inclusion. Issue 7 records the new protocol repair under the updated general rule, without inventing a new curator mark. The 75% criterion remains curator-selected; conditional realized-N, uncertain clock/label arrival, imperfect source histories, short 2013 coverage and exploratory formulation selection remain explicit limits. Probability of meeting this event is distinct from expected fraction correct.

**Issues for Myunghwan:**

6. **Include the selected conditional session-performance task?**

   - **Problem:** Whether to include the completed conditional >=75% session-performance classifier with its documented limitations.
   - **Background:** The target, AUROC, numerical N, equal record weights and temporal-only protocol were already selected by Myunghwan.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Include as implemented (implemented) | Retain the approved task and documented limitations | Preserves the selected performance-estimation purpose | Approximate logged-process interpretation and short coverage remain |
     | B | Leave out | Exclude this candidate | Avoids its stated limitations | Discards the approved large temporal education task |

   - **Recommendation:** A, following the actual November 3 inclusion decision. **Decision:** already settled.

   **Resolved (2026-11-03, Myunghwan):** Answered exactly "yes" to including the completed task with its limitations; accepted as implemented. The original ship and issue-6 marks remain on their original review identity. The November 5 request carries these choices forward, without assigning a new snapshot to the old marks.

7. **Predict each session without reading later test-session histories?**

   - **Problem:** A later held-out session's history counters reveal an earlier session's result when a model can inspect the test block.
   - **Effect on the task:** Reading future test covariates gives information unavailable at the earlier session's prediction point.
   - **Experiments:** Independent feature-only matching within each full 111111-row test window reconstructs 3.32-5.18% of labels at 99.97-100% precision; adding this to frozen honest predictions increases AUROC by 0.0210-0.0349 across all three windows.
   - **Consistency:** Current policy separates test-block evaluation leakage from valid own-row history and applies a benchmark-checked prediction-access contract, as for the medical-facility and sepsis tasks.[^protocol]
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Fixed training state and current row only (implemented) | Keep eight predictors; prohibit other test rows, future histories, test-block fitting/statistics and cross-split held-out labels | Preserves legitimate prior history and all approved data/splits; follows current policy | Benchmark must audit each method and exclude test-block learning |
     | B | Remove history_correct and requalify | Ship seven predictors and remove derived accuracy-history features | Blocks the demonstrated counter-difference formula | Loses legitimate signal: bounded raw-model AUROC drops 0.0072-0.0131; changes the approved predictor set |

   - **Recommendation:** A, the routine current-policy remedy that retains the approved task. **Decision:** no new human mark is required for this protocol correction; downstream enforcement remains a benchmark obligation.

   **Resolved (2026-11-05, AI):** Applied the current general evaluation-leak rule and its existing precedents: explicit train-only fitting, frozen state and current-row-only prediction in the definition, plus the benchmark method-checking TODO. Batched computation is allowed only when each prediction is invariant to changes in unrelated test rows. This records an agent-owned correction, not new curator acceptance or verified downstream enforcement.

   [^protocol]: LEAK-9 (Should, amended 2026-11-05) fixes evaluation leaks in scoring or a protocol the benchmark checks; LEAK-7 favors the smallest valid repair; LEAK-34 protects legitimate prior history. See the current `medical_facility_operational_data` issue-7 decision and `sepsis_prediction_1m` snapshot contract. No dataset-specific exception or general rule amendment is introduced here.

**Review panel:** ship (mediator; routine protocol correction applied and final native verification passed). Focused current-main recheck: independent claim/precedent audit, column/split audit, participant attack, independent successor refutation, mediator and editor. Historical full and focused panels remain preserved with the prior acceptance evidence; their scores are not fresh experiments. Current data and split identities match the approved package. The participant attack revealed evaluation leakage; the updated general policy settles the routine protocol repair. No unresolved curator choice remains after the correction. Benchmark method enforcement is still required.

<details><summary>Mediator</summary>

**Focused Duolingo mediator judgment**

2026-11-05. Base: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Dataset: `duolingo_spaced_repetition_recall_1m_clf`.

Verdict: ship after changes. The owner has added the explicit per-row inference protocol, demonstrated successor attack and measured size, and Duolingo benchmark-side checking TODO. I inspected those actual updated definition/record/TODO bytes. Finish the small documentation consistency changes below and native verification, then the authorized local build/commit. These are routine corrections under current LEAK-9, not a new scientific choice. Preserve the approved eight predictors, labels, weights, metric and six split arrays. This judgment does not certify downstream benchmark enforcement.

Validity: the newly demonstrated other-test-row attack is an evaluation leak (LEAK-9), requiring the protocol correction below. The evidence does not show that a row's own `history_correct` contains that row's current outcome (LEAK-10); its legitimate prior history remains protected by LEAK-34. The approved approximate conditional task and temporal regime remain intact. Value: the exact approved predictions retain mean AUROC 0.663756, versus 0.596148 for train-only N rates; fresh task probes have no flags. Quality: no new dtype repair is needed; lexical morphology is nominal, counts numerical. Weighed: the previously accepted realized-N, recorded-clock/label-arrival, imperfect-history, short-period and exploratory-selection limitations remain. For the curator: no new weighing call remains under the current general amendment and directly matching precedent.

**Changes to make now**

1. State the operational protocol in `task_summary`, `curation_comments` and `splits_comment`, so it reaches the generated README and built metadata. For each split, fit preprocessing and learned state only on that split's training rows. Freeze that state, then predict each test row from that row's supplied covariates only. No feature construction, preprocessing, model update or prediction step may use other test rows, future session histories, test-block statistics, or held-out labels from another split. Batched computation is permissible only when the prediction for a fixed row is invariant to the other test rows. Same-clock rows do not receive an invented arrival order. This is a snapshot protocol; allowing sequential test-history updates would be a separately defined protocol. Rules: LEAK-1/9, USE-3.
2. Add a `Potential leak, kept on purpose:` evaluation note naming the successor mechanism, full-fold coverage and measured gains below. Distinguish it from the already accepted source-history inconsistencies. The leak is newly found and materially measured; the old note neither disclosed nor accepted it. Rules: LEAK-6/9, EV-2/6/7.
3. Add Duolingo and this concrete mechanism to `datasets/_dev/tabarena-v0pt2/BENCHMARK_CHANGES_TODO.md`, under "Test rows predicted without the other test rows". Retain the requirement to inspect/exclude transductive methods or verify invariance to other test rows. Record this as required benchmark follow-through, not an executed check. Rules: LEAK-9, EV-7.
4. Use an AI assessment for this application of current policy; do not invent a new curator CC or a new acceptance mark. Regenerate/check metadata and README, verify exact values/categories/labels and all six split arrays, and complete the already authorized build/reload/checksum verification and local commit. A metadata checksum change is expected when protocol prose changes; do not describe it as unchanged metadata or silently replace historical identities. Rules: EV-7/8; repository build/record procedures.

Status on inspected updated bytes: the `known` summary, `Evaluation protocol (LEAK-9)` curation bullet, dated November 5 AI assessment and TODO implement the substantive correction and accurately leave downstream enforcement pending. Add the standard `Potential leak, kept on purpose (LEAK-9, an evaluation leak):` prefix to that bullet and a short own-row protocol reminder to `splits_comment`, as the medical-facility precedent does. These are cheap consistency edits; neither opens a scientific choice. Native regeneration and build are still in progress, not reported complete here.

The proposed protocol wording is: "For each split, fit preprocessing and the model only on its training rows and freeze learned state before evaluation. Predict each test session from its own supplied covariates only. No preprocessing, feature or model step may use another test row, future session histories, test-block statistics or held-out labels from another split. Batched prediction must leave each row's prediction unchanged when the other test rows change. Methods that learn from the test block are excluded from this task's benchmark."

**Issues for the curator**

None. This is conditional on implementing the corrections above. A desire to permit transductive/sequential test adaptation, change the feature set instead, or claim that unrestricted bulk predictions are valid would require a different protocol or new decision. None is requested or necessary here.

Missing executed downstream enforcement is real, but is not a new human choice for this local data build. The current amendment delegates checking to the benchmark; its exact motivating precedent already ships a written protocol with the benchmark check left on this repository's TODO. It would be inconsistent to invent an immediate harness-implementation gate for Duolingo while claiming to apply that amendment. Conversely, writing the line does not make an unchecked transductive benchmark result honest: such results remain ineligible under the protocol. Curation/build readiness and execution of compliant future benchmarks are separate factual claims.

The claim auditor's final addendum recommends issue 7 as a human choice between the protocol and dropping `history_correct`. I accept its factual refutation and its warning against inventing downstream enforcement. I do not accept that applying the current general remedy requires a fresh human mark. No distinguishing fact or contradictory current rule is identified; the amendment specifically covers this demonstrated mechanism, its motivating case already accepts the same deferred checking boundary, and LEAK-7 favors preserving valid signal. Dropping the history feature remains an optional changed task, not an equally mandatory unresolved fork. The auditor's request to present alternatives does not itself create a weighing call where current policy and direct precedent select the mildest adequate remedy. Keep the addendum as evidence and record this disagreement/resolution rather than rewriting it as unanimous initial approval.

**Agreed facts and decisive evidence**

I read the current mediator role, full review-panel procedure, principles and applicable leak/evidence rules; the current definition/record; `claim-audit.md`, `column-split-audit.md`, task/leak/dtype/check outputs; the final `participant_kit/work/REPORT.md` and associated evidence; and final independently authored `successor-refutation.md/json`. This is the focused tier: claim/precedent audit, column/split audit, participant gamer, independent attack refutation and mediator; a cold editor follows. There is no full-tier advocate/critic debate to imply.

The participant constructs matches without labels: same learning/UI language and lexical tag; successor clock minus its delta equals the current clock; successor prior exposures equal current prior exposures plus current N; successor correct-count minus current prior correct-count is a feasible current K. The resulting label is `4*K >= 3*N`. Every accepted successor is later than the row being predicted. Same-test-only access suffices; learner ID, future test labels, cross-fold rows and post-window records are unnecessary.

The independent refutation uses every actual 111,111-row test array and frozen, already qualified honest predictions. It rejects inconsistent candidate labels before scoring and confirms:

| Test day | Recovered rows | Coverage | Correct recovered labels | Honest AUROC | Attack AUROC | Gain |
|---|---:|---:|---:|---:|---:|---:|
| March 12 | 5,759 | 5.1831% | 5,758 (99.9826%) | 0.662491 | 0.697404 | +0.034913 |
| March 11 | 3,687 | 3.3183% | 3,687 (100%) | 0.662434 | 0.683475 | +0.021041 |
| March 10 | 3,978 | 3.5802% | 3,977 (99.9749%) | 0.666342 | 0.690257 | +0.023915 |

These are new rescoring experiments, not new model fits. The participant separately fitted 100k-train/50k-test untuned controls and found same-test-only gains of +0.036001/+0.023078/+0.025357 over its stronger honest engineering comparator. Those smaller-sample fits and bootstrap intervals must not be mixed with the full-fold frozen scores. Label recovery includes hundreds of negatives per full fold; a majority-class prediction does not explain it. Source-counter imperfections do not refute this measured route.

The current gap separates training and testing; it cannot prevent a later test row disclosing an earlier test row's outcome. Removing learner recurrence likewise does not directly address the demonstrated within-test-window channel. LEAK-9 applies because the attack reads another test row, while each counter remains prior history at its own row. This is not a conflict in which a Should overrides LEAK-10's Must: the alleged own-row post-outcome feature defect has not been demonstrated. LEAK-6 requires acting on the confirmed attack; LEAK-7 and the remedy ladder favor the valid-signal-preserving protocol fix supplied by LEAK-9.

Dropping `history_correct` blocks the tested exact K subtraction. In the participant's bounded comparison, it costs 0.00723-0.01312 AUROC for the raw control and 0.01539-0.02318 for the engineered control (also removing its derivatives). It changes approved inputs and would need fresh qualification. Under current LEAK-9 it is an optional, more destructive repair, not required. No untested alternative attack is asserted as a reason against it.

Other participant hypotheses did not establish another corrective data finding: full-feature cross-side copies are absent; descriptor lookup, formats, past-neighbor labels and row position do not establish an unavailable-outcome channel. Full-table lexical/cohort statistics gave small gains, but causal controls were not isolated, so this is not a second proven mechanism; the proposed protocol excludes test-block-derived predictors regardless. The owner's fresh raw-order adjacency flag concerns raw order removed by content ordering and actual time sorting; no shipped ordering exploit follows from that flag alone (EV-3). Dropped current fraction/count are expected label ingredients; their strong scores support their exclusion.

Current native checks report 27 passed, zero errors/warnings; fresh task probes show usable signal and no flags. The independent audits verify exact frame values, category state, labels and six split arrays against the approved package; legitimate qualification may be reused for those identical inputs. Those checks did not themselves test other-test-row access. The attack refutation supersedes any earlier broad reading of "no new leak found."

The participant additionally ran `batch_invariance.py`: for its fold-0 honest model on 50,000 fixed test rows, whole-batch versus 1,000-row chunks and 100 single-row predictions have maximum absolute difference zero (`batch_invariance.json`). This verifies that tested model's batch behavior only; it neither screens every benchmark method nor establishes a downstream guard.

**Consistency and execution boundary**

The current `medical_facility_operational_data/dataset.py` notes (lines 109-110 on this base) describe the same direction of information flow: a later row's own legitimate history reveals an earlier row's outcome. It keeps the fields, requires train-plus-own-row prediction, and records the November 5 LEAK-9 amendment and benchmark TODO. This remains accepted despite a much larger measured MAE gain. `fremtpl2/dataset.py` records the same amendment for label-free renewal information read from other rows, separately from its own-row BonusMalus repair. `sepsis_prediction_1m` forbids combining other patient hours under its snapshot task, while retaining patient-hour records; `5g_energy_consumption` explicitly makes station-hour predictions per sample and calls other-row learning transductive. These support the protocol remedy, not feature deletion or an invented learner holdout.

The decisive current implementation contract is the existing final TODO section: Data Foundry ships a protocol line and no per-row scorer; the guarantee sits in the benchmark, which must check models and exclude test-block learning. LEAK-9 is the current general amendment, not merely an old dataset-specific exception requiring renewed human approval every time it applies. The user also explicitly authorized repeating the full cycle with prior choices and local build/commit. Applying this existing remedy changes no settled target or inclusion choice.

Executed evidence here consists of inspection and synthesis of the final reports and actual current rules/definitions. I did not modify canonical source, run downstream enforcement, refit a model, build a container or create human marks. The owner must implement and verify the documentary changes and authorized build; future benchmark method checks remain pending. Preserve these boundaries in REVIEW, the record and final handoff.

</details>

<details><summary>Claim and precedent audit</summary>

**As-of scope:** The initial checksum analysis below used the byte-identical approved definition before the successor-counter finding. It attributes that initial framework-only change to special_features=[]. The final definition additionally records the own-row protocol, intentionally changing metadata again; the final native regeneration and build establish its current checksum. The successor addendum and mediator settle the later evaluation finding.

**Focused independent claim and precedent audit**

2026-11-05 UTC. Current upstream main: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`. Dataset: `duolingo_spaced_repetition_recall_1m_clf`. Roles: claim auditor and precedent checker, in the focused recheck panel. Read-only on canonical source and human decisions; only this run's report/evidence was written. Interpreter: the workflow's dedicated `.venv/bin/python`, explicitly importing the refreshed checkout's `src`, with two-thread caps.

Verdict: the preserved inclusion decision remains consistent. No new human decision or scientific repair is identified by this audit. The current source, frame, categories, labels, metric and six split arrays support reuse of the approved numerical qualification. The changed container checksum is entirely a current-schema metadata change, not a changed task. Final panel synthesis and build verification remain the owner's work; this report creates no new human marks.

Validity: the source and target-construction claims hold; the conditional realized-N, recorded-clock, label-arrival and source-history limitations remain explicit rather than being certified as resolved. Value: the full classifier beats the natural count-only baseline on every window; a current full task-probe run is owned by the main session, with prior exact-data qualification available. Quality: numeric counts, nominal lexical tags and No/Yes target remain consistent with the updated dtype rules. Weighed: a large, traceable education task with an approximate practical fit, short coverage and exploratory formulation-selection limits. For the curator: no reopened question from the facts inspected here.

**Scope, identities and evidence**

I read the current add-dataset panel procedure, claim-auditor and precedent-checker role files, both knowledge skills, principles/evidence and applicable use-case, split, metric, task and cleaning rules; current definition/README/record; the November 3 acceptance and its actual input/marks; the prior focused numerical and precedent audits; and the rule changes from `1964e1b2e4caa41c8a94082e028f65d4cd8b2b6b` to current main. The preserved diff is `claim-rule-changes.diff`. The historical local implementation commit `7c1928bb...` is not present in this refreshed Git object store; I used the available historical instruction commit plus the preserved actual definition/metadata/artifacts, rather than inventing a Git comparison.

The declaration SHA256 is `10e6c681a128763a081ad3ed086f5f54a21b60d77fd7b74d211b382cd1a1a06f`. The old qualification manifest records an earlier pre-approval documentation SHA (`a4298686...`), so those two definition hashes must not be described as identical. The old accepted built dataset metadata and current definition-generated dataset metadata compare exactly; task metadata differ only by the empty field described below. The data Parquet SHA256 remains `b6f104eed4cddf621d169771c84bf61e3cdb2380dd797014e9160433dcf0d596`, identical to the historical presentation frame. All six array comparisons passed independently in `claim_audit.py`, alongside the owner's stricter value/category comparisons.

Fresh independent evidence: `claim-audit-evidence.json`, executable `claim_audit.py`, `claim-source-counts.json`, executable `claim_source_counts.py`, and `claim-metric-stability.json`. The fresh decision register is `claim-register.json` / `claim-register.txt`. The column/split reviewer separately supplied `column-split-numerical.json`; source-to-selected-row lineage and the 81-copy count are inherited from the prior explicitly scoped full-source audits, not falsely presented as a new full-source alignment by this reviewer.

The latest local Bridge selected-sync capture was November 2 23:05:41 UTC, completed 23:06:19 UTC, approximately 72 hours old at this audit. Its current state is changed-since-install with changed summaries and unknown receipt members. Peer inventory is unknown. These limits do not establish the freshness of this independent local Git-main checkout or a remote installation; this audit uses the explicitly observed local identities above.

**Claims and attempted refutations**

Each quoted phrase below identifies a claim in current `dataset.py` task_summary/comments/splits_comment, generated README, or dated record. `Holds` means the stated, bounded claim survived the cited test; it does not mean every conceivable leak was ruled out.

| Claim and source | Refutation test actually run or inspected | Result and evidence | Rule |
|---|---|---|---|
| “One learner-word lesson or practice session”; six-language logs in late February–March 2013 (summary/README) | Reopen original paper grain; inspect fresh frame and source split audit | Holds. Paper section 4.1 describes learner-word session traces; frame has six learning languages; actual selected clocks span February 28 to March 12, newest end 16:14:57 UTC | USE-1/5, EV-2 |
| “At least 75% correct”; “4*K >= 3*N”; “Exact 75% is positive” (predicted/_clean/comments) | Independently stream all raw numeric outcomes and denominators, test integer/boundary formula against published fraction; inspect exact-data historical lineage | Holds. 12,854,226 source rows; zero bad denominators, count bounds, nonintegers or fraction mismatches. 169,363 source rows exactly 75%; zero integer-vs-fraction 75% mismatches. Prior aligned audit verified all 1,429,456 selected labels, including 18,802 exact-75% positives; current frame/labels are identical | TP-7, LEAK-4, CLEAN-1, EV-8 |
| “At N=1,2,3 this criterion equals all-correct; at N=4, 3/4 is positive” (comments) | Numeric stream checks N<=3; inspect exact integer rule for N=4 | Holds, zero N<=3 disagreements. At K=3,N=4 the implemented inequality is equality and positive | USE-5, TP-7 |
| “No rows are removed for having a particular outcome”; dedup precedes coarsening (comments/_clean) | Read actual pipeline; compare present output with approved frame and prior source-copy audit | Holds as implemented. Only source-copy removal precedes the label mapping; no binary-outcome filter or exercise weighting. Current frame has 1,240,113 Yes and 189,343 No (86.75419% Yes) | LEAK-16/19/20, CLEAN-1 |
| “83.886% ... all correct and 58.937% ... one exercise” (source-limit comment) | New full numeric raw stream | Holds: 10,782,942 all-correct / 12,854,226 = 83.88636%; 7,575,913 N=1 / 12,854,226 = 58.93714% | EV-2/7 |
| “Verify MD5 ... and 379004009 bytes” (download description) | Hash and size actual gzip | Holds exactly: MD5 `0a1cae5eb7ad4b0bd9c0de91d74fcced`, 379,004,009 bytes; SHA256 `26cf9b33f2e9b2e8aa9a8f262a017b30699ca2f625c56a12ce699d4ea7076873` matches prior qualification | PROV-8/13, EV-8 |
| “Eight predictors”; no current correct count, fraction or opaque IDs (summary/comments) | Inspect real frame schema and missing/copy counts | Holds: clock, delta, two languages, lexical tag, two history counts, N. No `p_recall`, `session_correct`, `user_id` or `lexeme_id`; no missing cells or full final-row copies | LEAK-10, CLEAN-1/14 |
| “Numerical session_seen remains a conditioning input, not a label by itself” (comments) | Inspect both outcomes within N and independently rebuild every test N-only training-rate probability | Holds. N spans integer 1–20, common N strata contain both labels; N-only baseline is each binary label's training success rate and exactly reproduces saved probabilities. It is not the former mean-fraction baseline | TP-4, LEAK-4, EV-5/9 |
| Lexical tag is nominal morphology, not prose or a severity scale (comments/_feature_types) | Inspect current dtype flag and actual lexical values against source Fig. 2/Appendix semantics | Holds. Fresh `ordinal_like` heuristic flag concerns strings such as lexical/morphology tags, not ordered severity levels. No semantic order is supplied; retain unordered category. Real counts stay numeric under updated CLEAN-14 | CLEAN-12/14/25, EV-3 |
| Three March 12/11/10 one-day windows, one-day gap, 1M/111111 per fold (split text/_make_splits) | Independently inspect six arrays, temporal boundaries, class support and source-code eligibility | Holds. Gaps 86403/86407/86401 seconds; every fold has 1,000,000 train and 111,111 test, with 14,780/14,835/14,806 negatives. Distinct training arrays, expanding eligibility. Separate source audit lower-bounds full-source train fractions at 86.48/78.32/70.80%, all above 50% | SPLIT-2/9/10/11/14, TP-5/9 |
| “Approximately 90/10 after sampling”; not the paper's single cut (summary/version/splits) | Arithmetic caps and primary paper section 4.1 | Holds. 111111/(1000000+111111) is approximately 10%; source uses one first-90%/last-10% split. Current text clearly disclaims literal reproduction | SPLIT-5/19/20, EV-2 |
| “All learners are eligible ... may recur; no learner holdout” (comments/splits) | Inspect actual split code and feature exclusions; compare prior curator input | Holds. Temporal windows receive the full cleaned source; no learner reservation exists. Recurrence is deliberate, not a cold-start claim | USE-10, SPLIT-3/13 |
| Output is P(K/N>=.75|X,N), not E[K/N|X,N]; goal is curator-selected (summary/comments/record) | Compare formulas and actual binary output, exact November 3 task-selection and approval input, and source evaluation | Holds as an approximate conditional session-performance task. The criterion is not asserted to be mastery or a deployed source rule. The two estimands are explicitly distinguished; source target is quantitative session performance | USE-1/3/5/8, TP-6/7 |
| “AUROC ... ranking ... not calibration ... or accuracy at a fixed action threshold” (training comment) | Inspect standard metric declaration, score categorical target on every fold, and current edge cases | Holds. Binary fallback `roc_auc`, no scoring columns/weights/threshold params; constant native AUROC .5 each fold. All-zero/all-one/tied probabilities are finite and permutation invariant; NaN/Inf raise ValueError | MET-2/7/8/11/12/13 |
| “Source ... MAE ... AUC/half-life correlation”; its rounded AUC is not the 75% event (metric reason) | Reopen paper section 4.1 and publisher evaluation.r | Holds. Publisher AUC code uses `round(p)`; no inclusive-75% convention is defined there. New README origin now says “no metric the task would use in practice”, fixing the earlier generic false “no metric” boilerplate | MET-1/2/5/8/11 |
| Equal records; diagnostic binary log loss with AUROC/logloss reporting; benchmark objective is its own (comments/model evidence) | Read executed model protocol; independently re-score all 12 predictions and reconstruct train-only N rates | Holds. Native scorer, independent rank-sum AUROC and manual logloss reproduce all 12 rows, maximum discrepancy 1.11e-16. Mean AUROC constant .500000, N-only .596148, without-N .622571, with-N .663756; full beats N-only in AUROC and logloss on every fold | EV-1/2/5/7/8 |
| Existing numerical qualification can be reused on refreshed main (owner claim) | Exact current frame/splits binding, current native scoring and metadata comparison | Holds for saved predictions and qualification tied to those identical inputs. No new fit was claimed. This is score reproduction, not an independent refit or proof that recorded early-stopping rounds are optimal | EV-7/8 |
| “Final scientific review ... approved inclusion ... no check warnings” (comments/record) | Read preserved exact native approval and application integrity; inspect new checks | Holds. Original snapshot `e8d965ea135d05819d8b441e64ccddb7db7abba1f8229ca7bf2ba5218a9cecd7`, version 0; actual answer “yes”, ship and issue 6 as implemented. Fresh check has 27 checks and zero errors/warnings/info. No new mark is inferred | Principles precedence, EV-7 |
| Source clock semantics, reporting latency and planned-N availability are established | Test whether the source text and code establish these stronger claims | Untested/unverified facts; current definition expressly does not claim them. Keep approximate conditional realized-N and recorded-clock wording. Source lesson adaptation supports preserving caution, not a new demonstrated leak | USE-3/8, LEAK-10, SPLIT-9/10 |
| Historical 98.18% counter consistency, counter decreases, first-90% archive/paper mean discrepancy and deposit chronology (comments) | Check historical reports, source identity and current attribution | Not newly recomputed here. Explicitly scoped as prior full-source verification; identical source identity and unchanged transform give no new contrary evidence. Counter mechanisms and start/completion timing remain unknown | PROV-16/17, EV-7/8 |
| Exploratory formulation selection was separated from inner-only model iteration selection (comments/record/model protocol) | Inspect actual dated choices, saved inner-selection audit and current wording | Holds as provenance. November 3 audit independently checked all six inner memberships/scores. This auditor re-scored primary predictions, not early-stopping traces; already inspected outer dates remain exploratory for task selection | SPLIT-4/21, EV-7/8 |
| No leak is demonstrated by current bounded screens | Inspect fresh leak JSON and supported-input scope | Holds only for tested mechanisms. Seven-feature fitted screen omits datetime; all-column exact-copy test includes the final predictors and finds zero cross-side copies. Reduced-screen matches 0.1662% and shallow depth-3 AUROC .598622 do not establish copies of full events or a label formula. Do not copy the historical reduced-screen 0.006% into the current report | LEAK-4/16, TP-4, EV-3/8 |

No current task claim is refuted. Historical screening claims about direct fit, fraction/RMSE, dropping N, single paper split or learner-disjoint evaluation are preserved history and explicitly superseded by later measured assessments and curator decisions; they must not be presented as current constraints.

**Checksum change, exactly attributed**

The accepted historical build checksum is `v2:18d351606c00ca77ce5f6707c1d477305d0e183492e0e8d05160bf28109285bb`. The current check checksum is `v2:0dadd5dcd69f149d54157ed533c07c1a83a3495446c79d655a7c7992e99b6fda`.

I independently reconstructed both using the current frame's canonical encoding and the saved historical metadata. Historical dataset metadata equal the current definition's generated dataset metadata; saved experiment metadata plus the verified identical six arrays retain the split identity. The only task metadata difference is `special_features`, absent before and now `[]` under the current schema. Hashing with the old dict exactly reconstructs the old checksum; adding only that empty field exactly reconstructs the current checksum. This is a proven metadata representation change. Do not silently edit the stored historical checksum to match it or treat it as a scientific drift requiring another approval.

**Current precedent review**

The new register contains 4,052 entries and 21 candidate flags, none naming Duolingo. The register still does not comprehensively index MET IDs and can parse numbered text in historical panel bodies as issues; absence of a flag is not the consistency finding. I read the actual closest cases and changed rules.

| Decision or changed rule | Actual precedent and current fact comparison | Finding |
|---|---|---|
| Preserve the approved approximate conditional task | `diabetes_3`, CC October 21/26: keep approximate with the undocumented-label gap named. Duolingo's label construction itself is verified; uncertainty is practical prospective interpretation | Consistent. Approval is not proof that source timing or planned N is known. No newly demonstrated availability defect was found |
| Preserve the derived 75% event, binary identity and fallback AUROC | `cirrhosis_patient_survival_prediction`, CC October 14 and November 1: explicit retargeting, binary event, No/Yes and AUROC. `nci_aids_antiviral_screen`, CC November 2: binary framing follows established field usage | Consistent with explicit target choice and metric matching, with an essential distinction: NCI/cirrhosis do not establish an educational 75% convention. Duolingo's bounded user-directed TP-7 departure was already exposed and accepted; it is not a general amendment or a false Must pass |
| TP-7 remains an established-convention Must | Actual unchanged TP-7; November 3 independent precedent report explains the specific higher-priority user instruction selecting inclusive 75% after its convention gap was shown | Preserve the existing bounded override. No third new exception or drift is established by re-running the same approved choice. Do not relabel it as a Should exception or reopen merely because the native snapshot changes |
| MET-4/5/11 changes: source standing, unique tuning criteria and context origin | New `open_soil_spectral_library` case deliberately tunes on log1p RMSE; `protein_model_quality_rf_pcp`/`huesken_sirna_efficacy` score within-group ranking; Imperial College challenge allows an overruled source metric | No opposite like-for-like case. Duolingo is a changed binary session event, not the paper's fraction target or candidate ranking within genes/proteins. Existing explicit fallback reason satisfies amended MET-11; it names the quantitative original and why it does not score this event |
| MET-13 stability tightened November 5 | New metric-library edge-case rule | Current binary AUROC passes finite constant/tied predictions, row-order permutation and invalid-prediction tests. No custom metric repair or new choice needed |
| SPLIT-9/10 now distinguish row-linked future labels from shared-code drift | `lt_vehicle_loan_default_prediction` November 5: no recurring borrower, fixed horizon and measured shared-code effect, gap 0. `alfa_battle_2_0_task_2`: own-client later-set labels filtered | Neither fact pattern demonstrates a Duolingo defect or requests changing its already-approved one-day gap. Duolingo source has recorded prior histories and realized session counts, not a retrospectively assigned borrower default label. Keep timing uncertainty explicit; do not claim a proven label-delay bound |
| SPLIT-14 now explicitly requires each window's own train side | Fresh arrays and full-source train counts | Consistent: three distinct training sides with earlier eligible histories; no frozen single model/train side across windows |
| CLEAN-12/14/25 now decode meaningful codes and preserve counts | Source lexical tags, exact counts, actual unordered No/Yes target; `bank_marketing` counts remain numerical | Consistent. Lexical morphological tags have no ordinal severity interpretation; the dtype heuristic flag is answered, not escalated into a new vote. No numeric rating or censored count was introduced |
| LEAK-9/10/13/39/40 changes: test-block exploitation, window aggregates, class-specific formats and fills | Current definition computes no whole-table covariate transform or class-specific fill; exact frame retained; current leak screen and separate task gamer attack | No new demonstrated contrary mechanism. Conditional realized N remains an explicitly accepted practical limitation; an old acceptance is not a license to conceal a newly proven leak. Task-gamer outcomes are for the separate reviewer/mediator, not pre-certified here |
| Newer curator choice replaces earlier fraction/RMSE or learner-disjoint decisions | Actual Duolingo dated CCs and exact November 3 inclusion | Consistent application of newer explicit decisions, not silent drift. Historical builds/results remain evidence, and newly authored human marks are prohibited |

No real departure without a distinguishing fact, higher-ranked new violation, or third comparable new exception was identified. No reflection prompt is warranted on this evidence. If the ongoing task-gamer or fresh task probe produces a demonstrable new validity issue, the mediator should assess that new evidence; neither a changed checksum nor a regenerated review identity is such an issue.

Primary source reread: [Settles and Meeder 2016, sections 3.3 and 4.1](https://aclanthology.org/P16-1174.pdf), and [publisher evaluation code](https://raw.githubusercontent.com/duolingo/halflife-regression/master/evaluation.r). The paper's deployed strength-display/ranking metrics concern its original quantitative output; the new event remains clearly a curator-designed performance goal. Its copyright/publication and deposit metadata are not a release authorization.

**Addendum: demonstrated successor-counter attack (new evidence, November 5)**

This addendum supersedes the opening **no new decision** conclusion only for the newly demonstrated test-block exposure below. The label, source integrity, exact frame/split identity, score reproduction, checksum explanation and previously settled scientific choices still hold. The earlier audit explicitly left the participant attack pending; its bounded seven-feature leak screens did not test this cross-row recurrence. A new human decision is now needed for issue 7's evaluation constraint or material feature removal. This reviewer changes no canonical file, acceptance mark or scientific setting.

**Mechanism and evidential status**

Read `successor_refutation.py` and `successor-refutation.json`, the owner's independent replication of the participant attack. For each fold, the code first strips the target and works only with that fold's 111,111 test rows. It matches the same learning language, interface language and lexical tag, with

```
t_next - delta_next = t_current
history_seen_next = history_seen_current + session_seen_current
K_inferred = history_correct_next - history_correct_current
```

It requires `t_next > t_current`, feasible `0 <= K_inferred <= session_seen_current`, and agreement of the inclusive-75% label among all feasible candidates for a current row. `actual_y` is attached after matching for measurement; neither actual labels nor source learner IDs nor excluded source correct counts enter the match, feasibility or accepted-prediction rule. The predictor then replaces the frozen approved honest model's probabilities only for accepted rows. Looking at the code confirms that no test label enters the matching or candidate-agreement decision. The supplied independent replication tests the actual shipped folds, not a hypothetical whole-source join.

| Fold (test date) | Reconstructed rows / 111,111 | Coverage | Correct inferred event labels | AUROC: frozen to attacked | Log loss: frozen to attacked |
|---|---:|---:|---:|---:|---:|
| 0 (March 12) | 5,759 | 5.1831% | 5,758 / 5,759 (99.9826%) | 0.662491 to 0.697404 (+0.034913) | 0.372437 to 0.352741 (-0.019696) |
| 1 (March 11) | 3,687 | 3.3183% | 3,687 / 3,687 (100%) | 0.662434 to 0.683475 (+0.021041) | 0.373293 to 0.361263 (-0.012030) |
| 2 (March 10) | 3,978 | 3.5802% | 3,977 / 3,978 (99.9749%) | 0.666342 to 0.690257 (+0.023915) | 0.371544 to 0.357934 (-0.013610) |

These figures and code inspection are strong evidence of the stated future-counter mechanism (EV-1/2/6); near-perfect classification on the linked subset and a gain over the frozen honest predictions distinguish it from ordinary recurrence or an imbalanced constant predictor. They do not establish every source learner match as correct or every counter as continuous: there are two wrong reconstructed event labels across the accepted rows, and ambiguous/infeasible candidates are excluded. A curator need not decide whether unknown counter anomalies are harmless to acknowledge this separately demonstrated evaluation shortcut.

**What this changes, and what remains settled**

The previously accepted 98.18% counter continuity and occasional decreases concerned whether source prior histories were perfectly consistent and whether they proved a current-row outcome leak. At each row's own prediction point, the preceding history remains legitimate under USE-6/10 and **LEAK-34 (Must)**. The new attack instead takes the next row's later history and reads the earlier outcome backward. Its future timestamps are measured, and its gain is measured. Calling it merely an accepted uncertainty would erase the newly demonstrated mechanism; calling every history value an intrinsic current-row leak would erase the prediction point.

The current claim “no current correct count or fraction remains as a predictor” remains literally true **within one row**. A stronger implied claim that unrestricted access to the complete test covariate block cannot disclose a row's outcome is **refuted**. The present definition does not yet state the row-access restriction needed to justify the honest row-wise evaluation. The accepted source-clock and realized-N approximations do not authorize later rows, and the one-day training gap cannot remove a successor inside the same test day. Repeating target, 75% cutoff, numerical N, equal records, dates, caps, learner recurrence or the existing gap question would not decide this mechanism.

**Current rules and closest precedents**

**LEAK-9 (Should, amended November 5)** directly addresses an evaluation leak where a model reads other test rows. It permits repair in scoring or by a protocol line the benchmark checks, instead of deleting otherwise legitimate row features. The closest actual precedent is `medical_facility_operational_data`, CC November 5, issue 7 A: future arrivals' queue features decode the current waiting-time outcome and lower MAE from 13.85 to 6.83 across all nine windows. The curator preserved the history fields with a no-other-test-row protocol and a benchmark-side model check. That mechanism is directly comparable: later rows carry realized outcome increments in otherwise legitimate histories. `sepsis_prediction`, CC October 1, similarly preserves each hour's measurements but requires causal predictions because future stay rows/record length expose the outcome. These precedents support keeping Duolingo's own-row prior counters **with a concrete evaluation restriction**, rather than rejecting the source.

The current amended LEAK-9 allows a benchmark-checked protocol line; it does not require this reviewer to invent a new scorer or certify an enforcement system that has not been demonstrated. Nor does it permit merely calling future-context cheating “out of scope” without stating the contract and how methods will be checked. **USE-3, LEAK-1/10** still forbid future information at the prediction point; **LEAK-34** does not extend its protection from past to future. **LEAK-38** is not the applicable kept-uncertainty rule: the future dates and counter mechanism are measured. **SPLIT-9** concerns unavailable training labels; here the exploit can run entirely within the test block, so increasing the train/test gap is not the demonstrated remedy. **EV-7** requires preserving the fact that honest row-wise model scores reproduce while the unrestricted participant kit permits a stronger illicit calculation.

**Repair choices for an actual curator decision**

| Choice | What it concretely fixes | Cost, validation and limits | Consistency |
|---|---|---|---|
| Preserve the eight approved predictors and require causal/row-independent prediction | Prevent the observed backward read by disallowing later test covariates when predicting an earlier row. A simple explicit contract is `prediction_i = f(training data, x_i)`, with no other test-row inputs, no fitting to the test block and no test labels. The cumulative prior histories already supplied in `x_i` stay valid | Preserve exact data and honest qualification; state the prediction point and restriction in maintained dataset/protocol notes. The benchmark must check the admitted methods for test-context use or enforce per-row access. This report has not verified such benchmark enforcement. A broader causal contract that permits earlier covariates must still prohibit later ones and test labels; it needs its own explicit check, not an assumption from sorted rows | Follows LEAK-9 and the directly comparable medical-facility/sepsis precedents; LEAK-34 protects legitimate histories |
| Drop `history_correct` and requalify the resulting seven-predictor dataset | Removes the correct-count increment used to recover K in the demonstrated attack. Without the two `history_correct` values, the exact numerator-difference identity cannot be computed from that formula | Material loss of genuine prior-success signal. Changes feature set and potentially content-based ordering/sampling, so regenerate/check the exact frame/splits and rerun affected baselines, fits and probes, including the participant attack. No residual equivalent exploit from the retained columns has been demonstrated here; do not reject this choice merely by speculating about other future information | A concrete data remedy under LEAK-7, though more destructive of approved legitimate signal than the LEAK-9 protocol remedy. It does not follow automatically from the old approval |

Recommendation: present both choices in issue 7, with **preserve histories plus an explicit benchmark-checked no-future-test-row contract** as the closest-precedent recommendation. If the curator wants protection against this measured exploit through the released columns themselves, or cannot accept the benchmark protocol obligation, dropping `history_correct` is a concrete alternative to qualify. Do not describe that drop as proven inadequate without a distinct retained-column exploit and measured evidence. Conversely, do not mark it qualified merely because the one observed formula is broken; run the affected qualification on the actual seven-feature package before accepting/building it.

A note saying that the attack is measured but allowing unrestricted future test context is not a repair for this prediction point. The next decision concerns which remedy to carry, not whether to erase the previously accepted scientific formulation. Apply no material feature deletion, changed evaluation guarantee, revised human mark or final build from this addendum alone. Preserve the original November 3 approval on its actual identity and record the new issue/decision separately.

</details>

<details><summary>Column and split audit</summary>

**Focused Duolingo column and split audit**

Verdict: retain the current definition and split, with the already accepted approximate-task limitations. New corrective findings: 0. No new human decision is requested by this audit.

This is an independent column/split contribution to the focused add-dataset recheck on 2026-11-05. It does not replace the claim, task-gamer, mediator or editor reviews. No canonical files were edited and no models were fitted. The definition is `state/duolingo-refresh-20261105/checkout/datasets/_dev/tabarena-v0pt2/duolingo_spaced_repetition_recall_1m_clf/dataset.py`, SHA256 `10e6c681a128763a081ad3ed086f5f54a21b60d77fd7b74d211b382cd1a1a06f`, on the supplied `9048f36a` base.

I read current column-auditor/split-auditor instructions and the applicable knowledge on principles, use cases, leakage, splits, cleaning/dtypes, evidence and checks/probes. The current November 5 amendments to LEAK-9, LEAK-38 and SPLIT-9/10/14 were considered. They do not establish a previously unverified clock or delay bound. The explicit November 3 curator approval remains the authority for this task's inclusive 75% criterion, numerical N, equal record weights, temporal-only evaluation and approximate fit. CLEAN-17/TP-7's usual established-convention requirement is not reasserted as a new unanswered decision: this particular curator-selected event is explicitly authorized and accurately described as such.

**Columns and meaning**

Meanings were checked against the publisher's [data-format README](https://github.com/duolingo/halflife-regression#data-set-and-format), accessed November 5. Its descriptions of prior counters explicitly say "prior to this lesson/practice". The [paper](https://aclanthology.org/P16-1174.pdf), section 3.4 and Table 1, separately describes interaction history and lexical features. Section 2.1 describes within-session learning/feedback; section 4.1 uses historical logs. Neither establishes preassigned exercise counts or the archive's label-arrival bound.

| Column | Meaning | Known at prediction? | Observed dtype / cleaning | Verdict / rules |
|---|---|---|---|---|
| `timestamp` | Recorded session clock | Recorded-clock approximation; start/completion unverified | `datetime64[ns]`, Unix seconds converted before sorting; no coarsening | Retain with accepted timing limit; USE-8, LEAK-10, CLEAN-14/23 |
| `delta` | Seconds since previous practice of the word | Prior interval under recorded-clock assumption | `int64`; positive, not an ordinal code | Retain; USE-6, LEAK-34, CLEAN-14 |
| `learning_language` | Studied language | Context | Unordered category, 6 observed levels | Retain nominal category; CLEAN-14 |
| `ui_language` | Interface language | Context | Unordered category, 4 observed levels | Retain nominal category; CLEAN-14 |
| `lexeme_string` | Lexical/morphological tag | Exercise context | Unordered category, 13,803 observed levels | Retain; not prose or an ordinal scale; CLEAN-14, EV-3 |
| `history_seen` | Prior exposure count | Source describes prior history; imperfect continuity remains known | `int64`; quantity, not a code | Retain with accepted source-counter limit; LEAK-34, CLEAN-11/14 |
| `history_correct` | Prior correct-answer count | Same evidence and limitation as prior exposure | `int64`; never exceeds `history_seen` in the frame | Retain; LEAK-34, CLEAN-11/14 |
| `session_seen` | Realized session exercise count N | Not demonstrated preassigned; supplied conditioning variable in accepted contract | `int64`, observed 1-20; actual count, no documented open-ended top-code | Retain numerical N with accepted conditional-task limitation; USE-8, CLEAN-14 |
| `session_accuracy_at_least_75` | Inclusive event `4*K >= 3*N` | Outcome, never predictor | Unordered categorical `No`/`Yes`; Yes is the event | Correct target representation; CLEAN-25, LEAK-4 |

The current dtype probe was executed independently on the current frame through `dataset_io.from_definition`, using a supplied saved split plan. It flagged only `lexeme_string: ordinal_like` (19 levels match scale-like vocabulary). The publisher defines structured word tags, and there is no source ordering through these tags. This is a lexical false positive, resolved by meaning; an ordered category would invent an order. The four numerical predictors are counts or elapsed seconds, with no scale-code, binary-flag or open-end evidence requiring recoding. The timestamp is correctly datetime. All nine columns are typed, all cells are present, and there are no untyped object columns.

The excluded source fields are handled correctly: learner identity and opaque lexeme ID are not predictors; current `session_correct` and `p_recall` are outcome ingredients and are removed. Deduplication is identity-aware and precedes target coarsening. No fitted aggregate, imputation, whole-table scaling or learned feature is introduced by `_clean` (LEAK-10, LEAK-29, CLEAN-6/7). The current label comes from integer comparison, including exact 75%; no outcome class is filtered out.

**Exact split audit**

The saved current frame has 1,429,456 rows, eight predictors and one binary target. It is sorted by actual timestamp with a RangeIndex. All six actual split arrays were checked for bounds, uniqueness, within-window disjointness, exact requested sizes and timestamp eligibility. Their union uses every stored row. The three training arrays differ, satisfying the updated SPLIT-14 requirement for distinct earlier-history refits.

| Test day (2013) | Train rows | Test rows | Latest train timestamp | Earliest / latest test timestamp | Test Yes / No |
|---|---:|---:|---|---|---:|
| March 12 | 1,000,000 | 111,111 | March 10 23:59:58 | March 12 00:00:01 / 16:14:57 | 96,331 / 14,780 |
| March 11 | 1,000,000 | 111,111 | March 9 23:59:57 | March 11 00:00:04 / 23:59:59 | 96,276 / 14,835 |
| March 10 | 1,000,000 | 111,111 | March 8 23:59:59 | March 10 00:00:00 / 23:59:58 | 96,305 / 14,806 |

Every training clock is strictly before midnight one day before its test window, and every test clock is within the intended calendar day. The sampled train/test proportion is 90.000009% / 9.999991%. Both classes occur in every train and test side. The newest day is partial, as documented; these results do not turn it into a complete daily window.

I independently streamed all 12,854,226 source records and counted full-source training eligibility before the sampling caps: 11,116,716 / 10,067,162 / 9,101,090 rows for the newest-to-oldest windows. Even conservatively placing all 81 previously established source copies on each train side, the post-dedup training shares are at least 86.4829% / 78.3178% / 70.8021%. Thus the oldest window comfortably meets the 50% history floor; the 1M cap does not redefine eligibility (SPLIT-14). Current code constructs expanding calendar windows on full-source history and only then samples/reduces the union.

The regime matches the approved known-learner practice-stream application (USE-10, SPLIT-1/3/13, LEAK-34). Learner recurrence is allowed; no learner reservation is declared. The old learner-temporal-review group-probe output was inspected only as historical evidence: it used another regression framing and mixed learner/date restrictions, so its scores are not evidence requiring a cold-start split here. No alternative model split was run because this recheck found no contradiction in the selected regime.

**Executed checks and remaining limits**

Executed scratch script: `column_split_check.py`; detailed output: `column-split-numerical.json`, both beside this report. It ran with the project `.venv/bin/python`, explicitly imported current checkout `src`, and capped OMP/MKL/OpenBLAS/Polars at two threads. Exit status: 0.

Checks included: current `dataset_io` metadata/feature interpretation; independent current dtype probe; exact pandas comparison of every frame value, dtype, category and index against approved prior `binary75-final/frame.parquet`; exact comparison of all six split arrays; split and class counts/bounds/gap/coverage; raw compressed-file SHA256; full-source denominator positivity, valid current correct counts, fraction/count agreement and history-correct <= history-seen; source eligible-history counts. There are 169,363 exact-75% source rows. The raw SHA256 still matches `26cf9b33f2e9b2e8aa9a8f262a017b30699ca2f625c56a12ce699d4ea7076873`; current frame SHA256 from the parent manifest is `b6f104eed4cddf621d169771c84bf61e3cdb2380dd797014e9160433dcf0d596`.

The parent's current native check reports 0 errors, 0 warnings, 27 passed checks; I inspected that artifact but did not rerun `dataset check`, which would rewrite its README. Fresh leak/task models belong to the parent's probe run; no fresh fitted scores are claimed here. Prior original-label and shallow-rule evidence remains applicable only with the independently verified exact frame/split identities, and is not relabeled as a newly fitted experiment.

Cannot verify: planned rather than realized N; session start/completion semantics; exact label-arrival delay; causes of the historical counter discontinuities; seasonal or modern-population generalization. The one-day gap is an accepted approximation, not proof all labels arrived before each refit. Stable test class shares cannot prove absence of censoring. The formulation was selected after exploratory outer-window inspection, so those dates are not a pristine confirmatory task-selection test. Current rules do not erase these accepted limitations, and no newly contradictory evidence was found.

Bridge startup observation: last successful selected capture November 2 23:05:41 UTC / install 23:06:19 UTC, about 71 hours 37 minutes old at audit startup. Receipt is changed-since-install; relevant curation knowledge/operations and local summaries differ, some selected policy references are missing, and peer edits remain unknown. The current checkout procedures and actual local raw/frame/array bytes, rather than the old sync receipt, support this audit. No transfer or peer-freshness claim is made.

</details>

<details><summary>Participant attack</summary>

**Independent participant attack report**

One confirmed finding: later held-out rows reveal earlier held-out outcomes through cumulative correct-answer counts. No test labels or public target lookup are used to construct this attack.

**Scope and baseline**

Only `task.md`, `task.json`, `data.parquet`, `splits.parquet`, the supplied scoring implementation, and the public source below informed the analysis. All authored scripts and outputs are in `work/`. No parent/project rules, curation notes, other datasets or outside code repositories were inspected. The initial LightGBM import emitted a default matplotlib configuration-path warning and created an incidental temporary cache outside the kit; no outside task/project contents were exposed. Subsequent runs place that cache in `work/mpl`.

All three shipped temporal splits were tested. For each, seed 481 fixes 100,000 sampled training rows and 50,000 sampled test rows. Every comparison uses those exact same rows; saved sample indices permit replay. Models are untuned LightGBM classifiers: 200 trees, 31 leaves, learning rate 0.05, seed 481, two threads. The honest baseline uses all supplied features, converts timestamp to seconds, and preserves categorical features. A stronger honest comparator adds prior accuracy, prior incorrect count, log delta, hour and weekday. These are legitimate predictors available at the stated prediction point. AUROC is computed through `score.py` using original class labels.

**Confirmed finding: successor history reconstructs current correctness**

For current row i and candidate later row j, match identical learning language, UI language and lexeme string, require:

- `timestamp_j - delta_j == timestamp_i`;
- `history_seen_j == history_seen_i + session_seen_i`;
- `timestamp_j > timestamp_i`;
- `K = history_correct_j - history_correct_i` lies between zero and `session_seen_i`.

Retain a row only when exactly one candidate survives these feature-only constraints. Reject ambiguity before reading any target labels. The inferred outcome is `4*K >= 3*session_seen_i`. Future covariates reveal K after the current session has finished, which is unavailable when its correct-answer count has not been observed. No user ID is needed. The [official data dictionary](https://github.com/duolingo/halflife-regression#data-set-and-format) describes delta as elapsed time from prior practice, the history counters as totals before current practice, and session counts as current-practice totals. This supports the reconstruction interpretation; the source was consulted for definitions only.

There are 76,093 uniquely linked rows across the complete table; reconstruction agrees with their labels on 99.982916% (13 errors). Labels are used here only to evaluate an already fixed reconstruction. To eliminate any dependence on excluded or later test windows, the main result below restricts j to the same shipped test window as i. On linked rows replace the honest engineered prediction with 0.999999 or 0.000001 according to inferred outcome; retain original model predictions elsewhere.

| Split | Honest AUC | Engineered honest AUC | Same-test successor attack AUC | Gain vs engineered | Paired bootstrap 95% interval | Linked evaluated test rows | Reconstruction accuracy |
|---|---:|---:|---:|---:|---|---:|---:|
| r0f0 | 0.630206 | 0.640320 | 0.676321 | +0.036001 | [0.033453, 0.038432] | 2,616 (5.232%) | 99.961774% |
| r1f0 | 0.626041 | 0.639688 | 0.662766 | +0.023078 | [0.021549, 0.025202] | 1,654 (3.308%) | 100.000000% |
| r2f0 | 0.630069 | 0.645489 | 0.670845 | +0.025357 | [0.023221, 0.027261] | 1,762 (3.524%) | 99.943246% |

The same-test attack gains versus the raw honest baseline are 0.046115, 0.036725 and 0.040777 respectively. Allowing successor covariates anywhere in the supplied table gives engineered-attack AUROCs 0.676321, 0.668139 and 0.677388. Thus same-test access alone establishes the finding. No successor is in the current split's training set. The gain is conditional on bulk access to future covariates; this attack is unavailable with strictly chronological per-row inference. The row bootstrap (100 replicates for the main comparison) does not account for latent user/session dependence, but the positive effect repeats in all three shipped windows.

**Other tested hypotheses**

- **Row order / IDs:** no ID columns are shipped. Timestamps are globally nondecreasing. Adding row position changes raw-baseline AUC by +0.000626, +0.001246 and -0.000233. Only the second row-bootstrap interval excludes zero. This does not establish an outcome side channel beyond supplied time.
- **Exact cross-side copies:** zero full-feature duplicates between train and evaluated test rows. Omitting timestamp produces 81, 91 and 79 matches to full training sets. Training-label mean lookup on these descriptors changes AUC by -0.000186, +0.000083 and -0.000346; all bootstrap intervals include zero. No demonstrated duplicate exploit.
- **Formats / sentinels:** generic lexeme markers, noun/verb markers, lexeme length and extreme delta flag change AUC by -0.000326, -0.000088 and +0.000682; all intervals include zero. No missing cells or impossible `history_correct > history_seen` records. Extremely long delta occurs in about 0.0096% of rows and has univariate test AUC approximately 0.5. Lexeme morphology itself is legitimate signal.
- **Inferred entities / nearest neighbors:** matching past training predecessors and blending their known label reduced all three honest AUROCs. A fixed ten-neighbor training-only comparator within language/UI/lexeme, using log prior counts, log delta, prior accuracy and exercise count, also reduced AUROC (0.622354, 0.617050, 0.621594). The confirmed attack uses future counters, rather than merely a strong nearest-neighbor predictor.
- **Training rows' futures:** 5,384, 5,518 and 5,670 sampled training rows have a unique successor in the full table. Their later records were not used as extra training labels. Temporal cutoffs have no shared training/test timestamps. The actionable issue remains held-out future counters.
- **Test statistics:** full-table lexeme frequency and same-timestamp cohort counts, added to honest engineering, gain +0.001060, +0.003264 and +0.002976. The first bootstrap interval crosses zero; the latter two do not. These combined covariates have not been isolated against a comparable causal frequency/session-context control, so deployment unavailability and mechanism are unresolved. They are not ranked as a second confirmed exploit.
- **Direct post-outcome inputs:** no `session_correct` or recall proportion is supplied. Historical counts are legitimate for the current row, and `session_seen` is explicitly conditioned on by the task. Their legitimate predictive strength is not itself a defect. The demonstrated violation is looking ahead to the next row's historical count.

**Bounded repair comparison**

Removing `history_correct` from every row prevents the demonstrated exact K-difference formula. This is a measured comparison only, not a task change or a claim that every possible future-information route is closed. For the engineered comparator, also remove prior accuracy and prior incorrect count because both derive from the removed column. All other training settings and sampled rows remain identical.

| Split | Raw model without history_correct AUC | Drop vs raw honest | Engineered model without history_correct AUC | Drop vs engineered honest |
|---|---:|---:|---:|---:|
| r0f0 | 0.622522 | 0.007683 | 0.624932 | 0.015388 |
| r1f0 | 0.612924 | 0.013117 | 0.616506 | 0.023182 |
| r2f0 | 0.622842 | 0.007227 | 0.622783 | 0.022706 |

**Evidence and replay**

Run `work/run_attacks.py`, then `work/additional_checks.py`, then `work/repair_comparison.py` from the kit using the supplied interpreter. All cap compute threads at two. `work/write_report.py` creates this report. Evidence: `work/scores.csv`, `work/evidence.json`, `work/additional_evidence.json`, `work/repair_and_noise_evidence.json`; link audit: `work/future_links.parquet`; exact samples and all predictions: `work/r*f0_samples.npz` and `work/r*f0_predictions.parquet`. Logs retain execution outcomes. Bootstrap intervals are exploratory conditional uncertainty checks, not population-level guarantees. More extensive tuning, hidden user identities and production inference plumbing were not checked.

The fixed r0f0 honest model is batch invariant in a direct implementation check: all 50,000 test predictions are identical between whole-batch and 1,000-row chunks; the first 100 are also identical under one-row inference (maximum absolute difference zero). See `work/batch_invariance.py` and `work/batch_invariance.json`. This establishes the property for this supplied-feature honest implementation, without auditing general benchmark submission enforcement.

</details>

<details><summary>Independent successor refutation</summary>

**Independent successor-row attack refutation**

The same-test-only successor attack replicates. It is a material new evaluation finding: later test covariates reconstruct the earlier binary outcome with 99.97-100% observed label precision on 3.32-5.18% of each full test window, and improve a frozen honest classifier on all three actual splits. The accepted imperfections in source-counter continuity do not cover or refute this future-information channel.

This report supplements and narrows the earlier `column-split-audit.md` conclusion of no newly identified corrective concerns. That audit validated individual column meaning and actual split integrity; it did not test joint access to later test rows. The new evidence does not establish that a row's own prior counter contains its own current outcome. It establishes that a later row's prior counter can disclose an earlier row's outcome to a method permitted to inspect the whole test block.

**Independent test**

Executed `successor_refutation.py`, exit 0; full results are in `successor-refutation.json` beside this report. Project interpreter and all applicable numerical thread caps were set to two. The script is independently authored and did not read the participant attack implementation. It reads only the current saved frame/six split arrays and frozen previously qualified predictions; matching uses each actual 111,111-row test array alone. No row from another split, outside the test window or after its end is used. Learner identity, source correct counts and source fractions are unavailable to the attack.

For current row c, find later row n in the same test array such that:

1. Course, interface language and lexical tag agree.
2. `timestamp_n - delta_n == timestamp_c` exactly.
3. `history_seen_n == history_seen_c + session_seen_c`.
4. `K_inferred = history_correct_n - history_correct_c` is between zero and the current N.

Infer the event by `4*K_inferred >= 3*N_current`. A row is attacked only when every feasible matching successor agrees on this label; inconsistent candidate labels are rejected. None of these selection or inference steps reads a test label. Actual labels are used only afterward to assess precision and scores. No model is trained or tuned for this test.

| Actual fold / test day | Test rows | Accepted recoveries | Coverage | Correct labels | Label precision | Ambiguous-label rows excluded |
|---|---:|---:|---:|---:|---:|---:|
| 0 / March 12 | 111,111 | 5,759 | 5.1831% | 5,758 | 99.9826% | 1 |
| 1 / March 11 | 111,111 | 3,687 | 3.3183% | 3,687 | 100% | 0 |
| 2 / March 10 | 111,111 | 3,978 | 3.5802% | 3,977 | 99.9749% | 0 |

There are 5,761 / 3,688 / 3,979 candidate pairs before feasibility filtering. One pair in each of folds 1 and 2 implies an impossible K and is excluded. Fold 0 has exactly one current row with two candidate successors, differing both in inferred K and label; it is excluded. All accepted rows therefore have a unique candidate. Covered true negative counts are 817 / 485 / 576 and true positive counts 4,942 / 3,202 / 3,402; this is not simply predicting the majority class. There is one erroneous recovered label in folds 0 and 2, respectively, and none in fold 1.

This refutes the proposed defenses that the effect needs cross-fold data, post-window data, a learner ID, a test-label match, materially ambiguous keys, or perfect continuity across all source rows. None is needed. It does not prove exact recovery of source K on every match; binary outcome precision is what was assessed.

**Measured gain**

The control is the saved approved `classifier_with_n` prediction vector, whose current-frame and six-array identity was independently verified in the first audit. Unattacked probabilities remain byte-for-byte the same; attacked rows are replaced by their inferred 0/1 event. No fit or tuning is claimed. The prior-only version uses the current fold's training event rate elsewhere.

| Fold | Frozen honest AUROC | With successor attack | AUROC gain | Honest log loss | With attack |
|---|---:|---:|---:|---:|---:|
| 0 | 0.662491 | 0.697404 | +0.034913 | 0.372437 | 0.352741 |
| 1 | 0.662434 | 0.683475 | +0.021041 | 0.373293 | 0.361263 |
| 2 | 0.666342 | 0.690257 | +0.023915 | 0.371544 | 0.357934 |

Mean AUROC gain is about +0.026623. Even a model using only a training-prior constant plus this attack reaches AUROC 0.551862 / 0.532432 / 0.536417, against 0.5 for the constant. No confidence interval or broad model comparison is claimed by this independent check. Parent/participant confidence estimates, if reported, are separate evidence.

**Timing and remedies**

All accepted successors have a strictly later recorded timestamp than the row being scored. At that earlier row's prediction point, its later successor record has not yet happened. The publisher [data-format documentation](https://github.com/duolingo/halflife-regression#data-set-and-format) defines the counters as prior to each row's own session and delta as time since preceding practice. These semantics permit the demonstrated recurrence. The unknown start/completion meaning and reporting latency remain unknown; neither makes later-session information prospectively available for an earlier session. A one-day train/test gap cannot stop information moving backward between rows within one test window.

This mechanism falls under current **LEAK-9** (November 5 amendment): evaluation leakage when a method can read other test rows, with causal per-entity prediction/scoring or an enforced benchmark protocol as the remedy. **USE-10 / LEAK-34** still support a row's own legitimate practice history. It should not be framed as newly proving current-row `history_correct` is a post-outcome feature.

The mildest remedy is an explicit, enforceable causal inference contract: score each row using the training data and its own available covariates, or allow only previously arrived records under a defined sequential protocol. Deny every row access to later test covariates, test-fitted transformations, order statistics or aggregate state derived from those later records. Rows sharing a clock should also be handled conservatively because within-clock arrival order is unverified. A held-back streaming/per-row evaluator could enforce this; a written line requires the benchmark to actually check compliant methods, as LEAK-9 specifies. This audit has not verified that the downstream evaluator enforces it.

Dropping `history_correct` blocks this particular exact K subtraction, but removes genuine historical signal as well. It is a more destructive dataset change than enforcing causal evaluation and would require requalification of the changed feature set. It is not established as a complete solution to every future-block mechanism. Neither a new learner holdout nor wider train/test gap addresses this same-window route directly. These are analytical remedy comparisons, not a curator approval or an implemented change.

The previously accepted target, numerical realized N, equal records, history anomalies, temporal windows and exploratory formulation-selection limits remain as documented. This new test warrants a concrete evaluation-protocol follow-through; it does not authorize silent source/feature/split edits or a fresh semantic inclusion decision by this auditor.

</details>

<details><summary>Review editor</summary>

**Focused Duolingo cold editor review**

Ready for the curator after the three concrete corrections below. No further semantic issue or new human decision is identified. This is the focused review-editor role; canonical source and human marks were not modified.

I read the current editor role, writing, principles and review-file procedures, then read REVIEW.md cold. I checked its claims against dataset.py, generated README.md, the curation record and the affected BENCHMARK_CHANGES_TODO entry. The README was awaiting final regeneration during the initial inspection; the owner's later final native-check result is separate evidence, not a check executed by this editor.

**Concrete edits**

1. **Make the panel badge a recommendation.** Old: `**Review panel:** focused current-main recheck: independent claim/precedent audit, column/split audit, participant attack, independent successor refutation, mediator and editor.` New: `**Review panel:** ship after the routine protocol correction, now applied (mediator). Focused current-main recheck: independent claim/precedent audit, column/split audit, participant attack, independent successor refutation, mediator and editor.` The page takes the first sentence as the recommendation; the initial sentence was only the tier and role inventory. Keep benchmark enforcement explicitly pending in the remainder.

2. **Normalize the embedded reports to the review format.** Old examples: `# Focused Duolingo mediator judgment`, `## Changes to make now`, `### Mechanism and evidential status`. New examples: `**Focused Duolingo mediator judgment**`, `**Changes to make now**`, `**Mechanism and evidential status**`. Apply this to every report heading after the single dataset title. The current review format prohibits Markdown headings inside the panel; preserve the complete substantive reports and their disagreements while changing heading syntax.

3. **Scope the initial checksum analysis before the protocol correction.** Old unqualified opening in the claim report: `The changed container checksum is entirely a current-schema metadata change, not a changed task.` Preserve that authentic report, but precede it with: `Report scope: the opening audit and its checksum comparison describe the initial current-main refresh before the successor-counter protocol correction. At that stage, the sole task-metadata change was the empty special_features field. The final definition additionally changes protocol text; its current checksum is established by the later final regeneration/build, not by this initial comparison. The addendum records the later attack finding and the auditor's recommendation; the mediator explains the final resolution of that disagreement.` This avoids presenting the initial 0dadd checksum or schema-only explanation as the identity of the final protocol-bearing package. The record already scopes this correctly as the initial framework-only checksum change.

**Scientific and evidence assessment**

The task is intelligible without the earlier chat: predict the probability of the inclusive 75% session-performance event, conditioned on numerical realized N and legitimate prior/context inputs, with equal record weights and the retained temporal windows. It distinguishes that output from expected fraction correct and from source-defined mastery. The full record retains the reason for choosing the coarser performance summary and the fact that regression was not invalidated. Realized rather than proven planned N, uncertain start/completion and label arrival, imperfect historical counters, short 2013 coverage and exploratory formulation selection remain visible limitations.

The new finding is concrete and distinct from the accepted source-counter imperfections. Feature-only matching to a later row in the same test window reconstructs earlier outcomes. Full-window recovery of 3.32-5.18% at 99.97-100% precision and frozen-model AUROC gains of 0.0210-0.0349 are separated from the participant's newly fitted 100k/50k controls and their bootstrap intervals. Exact-data/split verification supports reuse of the approved model predictions; it is not called a new model fit. The initial bounded screens are not allowed to overrule the later independent attack replication.

The report preserves the claim auditor's proposed need for human choice and the mediator's contrary policy resolution. Current LEAK-9 and directly matching precedents support the routine train-only, own-row evaluation contract while retaining genuine history. Issue 7 closes as an AI-owned protocol correction, without attributing a new acceptance, exception or amendment to the curator. The original issue-6 inclusion and mark identity remain historical. No repeated semantic gate is needed for unchanged scientific choices.

The definition and TODO distinguish an applied documentary protocol from future benchmark method checking. Frozen fitting and own-row predictions exclude the demonstrated future-counter route; a dataset check/build does not establish downstream enforcement. The measured batch-invariance example concerns only its tested honest implementation. Neither feature deletion nor a wider gap is misrepresented as an executed or comprehensive repair.

No exposed credential or absolute host-local path was found in the inspected public review. Public source references, current-versus-historical numerical evidence and the closed issue numbering remain intelligible. No additional stylistic or speculative finding is raised.

**Scope and freshness**

This was local read-only inspection of the refreshed checkout and supplied run evidence. No remote request, model fit, controller operation, canonical edit or human mark was performed. Bridge status recorded the last selected capture at 2026-11-02 23:05:41 UTC and completion at 23:06:19 UTC, approximately three days old; selected files have changed and peer inventory remains unknown. The review relies on observed local current-main procedures and current artifacts, not on that sync receipt as scientific revalidation.


**Application (AI, 2026-11-05):** All three requested format and evidence-scope repairs are applied. The current native collector and page builder pass with both issues resolved; no new semantic finding is left.

</details>
