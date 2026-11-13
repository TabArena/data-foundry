# github_pull_request_acceptance

**Outcome:** added as `github_pull_request_acceptance_1m`. Zhang et al.'s GHTorrent release (IEEE TSE 2023), 2,666,723 pull requests of 10,017 GitHub projects decided within 180 days, with "merged" as the target and only what is known at the opening as inputs, tested on three monthly windows of autumn 2018 (each train side a random 1M of the earlier rows). The AI recommends shipping it, scored by ROC AUC over all test pull requests until the curator decides whether the score is taken within each project (issue 1).

**Main points:** Score ROC AUC pooled over all test pull requests, as implemented, or within each project, the unit the integrator ranks (a rule amendment shared with smartshark_release_defect_prediction)?

**Record judgment:** valid with an approximate fit. Value: a moderate real signal (ROC AUC about 0.81 pooled, best single column 0.746) on 2.67M pull requests from a peer-reviewed release. Quality: the notes were corrected (the unit of pushed_delta, the base of the known-project share, the row cut from 3.35M to 1.30M). The integrator's triage at the opening is a real task (Gousios et al., ICSE 2015), the temporal split matches it, and after the panel's fixes no column is known only after the opening: `contrib_perc_commit` (it counts the pull request's own commits once merged: above 0 for 64.6% of merged first pull requests of outsiders against 22.8% of unmerged ones; dropping it costs 0.0006-0.0036 ROC AUC) and `integrator_availability` (no published code says when it was measured, and it adds nothing: alone ROC AUC 0.468) were dropped, and a protocol line (each test pull request is scored without the other test rows) closes the task gamer's exploit, which read earlier test outcomes off the history counters of later test rows and lifted ROC AUC from 0.81-0.82 to 0.90-0.92. The model learns who submits more than what changed, since the release holds the code change only after review. Settled without a decision (the panel agreed): the personal attributes stay dropped (no gain, 0.8155 with against 0.8162 without); only pull requests decided within 180 days are kept, as in training; project_id stays as a category; description_length is kept with a note (worth at most +0.0024).

**Issues for the curator:**

1. **Score ROC AUC pooled over all projects, or within each project?**

   * **Problem:**
     - The integrator ranks the open pull requests of one project, but the pooled ROC AUC also rewards telling projects that merge often from those that do not.
     - On the shipped windows the project's merge rate from the training rows alone scores 0.71-0.72 against LightGBM's 0.80-0.81, and within projects the same LightGBM scores only 0.61-0.63.
     - The source names no single metric, so the default for a yes/no target (ROC AUC over all rows) applies; scoring within each project would be the third or fourth exception of this kind, which calls for changing the rule rather than adding another exception[^met5].
   * **Effect on the task:** pooled, a model wins largely by knowing each project's merge rate; within projects, only by ranking one project's pull requests, which is the integrator's decision.
   * **Experiments:** the mediator, LightGBM with 300 trees on a 300k training sample, `contrib_perc_commit` and `integrator_availability` dropped, windows November / October / September 2018:

     | Score | November | October | September |
     |---|---|---|---|
     | project merge rate from the training rows, pooled | 0.720 | 0.708 | 0.709 |
     | `pr_succ_rate_at_open` alone, pooled | 0.753 | 0.750 | 0.733 |
     | LightGBM, pooled | 0.813 | 0.812 | 0.798 |
     | LightGBM, mean ROC AUC within projects with both classes | 0.613 | 0.629 | 0.618 |
     | projects with both classes (share of test rows) | 2,529 (71%) | 2,796 (75%) | 2,383 (71%) |

   * **Consistency:** protein_model_quality_rf_pcp and huesken_sirna_efficacy were scored within groups on a measured gap (2026-11-04), the second recorded as the second exception to the fallback rule[^met5c]; smartshark_release_defect_prediction raises the same question for its projects. The across-datasets item on scoring within groups (from uniform_soybean_tests_yield and genomic_prediction_soy_yield), which you kept for the review page, proposes the rule wording and a measure; this issue follows whatever it settles.
   * **Panel:** the advocate would ship pooled with a README caveat and raise the rule for the batch; the critic and the precedent checker asked to measure first and take a grouped score if the gap is material; the mediator measured it, finds it material, favours a within-project score in principle, and leaves the rule change to you. The ship verdict does not depend on it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Pooled ROC AUC (implemented) | the default ROC AUC over all test pull requests; the README states that the project's merge rate alone scores 0.71-0.72 pooled against 0.80-0.81 for LightGBM | follows the rule as written; scores every test row | most of the score is telling projects apart, not the integrator's ranking |
     | B | Amend the fallback for the batch: score within the unit the actor ranks | a new `mean_group_roc_auc` metric over the projects, checked against a reference, here and in smartshark_release_defect_prediction | scores the decision the use case names; one rule for the family | a rule change and new metric code; 25-29% of test rows sit in projects with one class and go unscored; noisier on small projects |

   * **Recommendation:** A now, and switch to B with smartshark_release_defect_prediction if the across-datasets item amends the rule; the measurements favour B. **Decision:** A or B?

   **Notes for the AI:** on A, nothing more: the note on the score in `curation_comments` carries the table above to the README; drop its last sentence ("Whether to score within each project is open (REVIEW.md, issue 1)."). On B, write `mean_group_roc_auc` in `src/data_foundry/v2/metrics.py` (mean of per-group ROC AUC over groups with both classes, the group from a scoring column `project_id`), check it against a reference implementation, declare it with `Metric.from_context` and the reason (MET-1, the integrator ranks one project's queue), add a Cases row to MET-5, apply the same to smartshark_release_defect_prediction, and re-run `dataset check` and the task probes. Scripts: the mediator's experiment script in the run folder.

   [^met5]: **MET-5**: a source that reports several metrics without naming one leaves the fallback (binary: ROC AUC, **MET-8**); **MET-1** (Must): the metric serves the use case's decision. A third exception to a rule is a reason to amend it (principles, "Exceptions and amendments").
   [^met5c]: The working copy's across-datasets item of 2026-11-04 (resolved by Lennart): huesken_sirna_efficacy is the second grouped-ranking exception to MET-5 after protein_model_quality_rf_pcp; "No MET-5 amendment is due before a third exception."

**Review panel:** ship after changes (mediator). Claim audit: no claim failed; the known-project share is 94-95% of test rows (against the full train side), now stated. Column audit: `contrib_perc_commit` counts the pull request's own commits once merged (64.6% above 0 among merged first pull requests of outsiders against 22.8%, alone ROC AUC 0.718 there), dropped (worth 0.0006-0.0036 ROC AUC in the model); `integrator_availability` dropped as no code, no gain. Split audit: the temporal windows and the one-month gap are right. Blind review: would benchmark; its worry that some counts are dump-time values is answered by the source code (computed as of the opening). Task gamer: the differences of the history counters between consecutive test rows of a project or contributor lift ROC AUC from 0.81-0.82 to 0.90-0.92; closed by a protocol line (LEAK-9). Debate: the advocate's and the critic's opening briefs converged, so the rebuttal round was skipped; agreed: the two drops, the protocol line and the notes; disputed: pooled or within-project scoring (issue 1).

<details><summary>Mediator</summary>

MEDIATOR REPORT: github_pull_request_acceptance (folder github_pull_request_acceptance_1m), 2026-11-09

SUMMARY (15 lines max)
- Recommendation: ship after changes. The task is real and the temporal split is right. One Must leak (contrib_perc_commit) is fixed by dropping it.
- Changes to make now: drop contrib_perc_commit (LEAK-10) and integrator_availability (LEAK-10, recorded as "no code, no gain"); add the LEAK-9 protocol line; add the description_length kept-on-purpose note; fix the notes.
- The one open point is the metric. I measured it. On its own, the project's merge rate from the training rows gives a pooled AUC of 0.708-0.720, and pr_succ_rate_at_open alone gives 0.733-0.753. LightGBM's pooled AUC is 0.798-0.813. Within projects, the same LightGBM scores only 0.613-0.629 (mean AUC over the 2,383-2,796 test projects that have both classes; they hold 71-75% of test rows).
- So the gap is real: most of the pooled score is telling projects apart. This is the measured fact the critic and the precedent checker asked for. Per-project scoring is now an evidenced option. It would be the 3rd/4th exception of its kind (with smartshark), so it becomes a batch amendment of MET-5/MET-1, which is the curator's call (scoring-within-groups stays on the review page).
- Task gamer: both exploits map to LEAK-9. They are new (no existing note), and the protocol line closes them.
- Consistency: every change follows precedent. Per-project AUC would depart from the default only through the amendment.

1. JUDGMENT RECORD
Verdict: ship after changes.
Validity: SEL holds. USE-1 holds with an approximate fit (the model learns who submits, not what changed; there are no code or CI features). USE-5 is met with a note (squash, cherry-pick and command-line merges are labelled No). LEAK-10 triggered and fixed (dropped contrib_perc_commit and integrator_availability). LEAK-10 description_length kept with a note (whole-field worth at most +0.0024 AUC). LEAK-9 triggered and fixed by a protocol line. LEAK-23/24 hold (180-day selection, noted). SPLIT-8 holds (temporal). SPLIT-13/USE-10 hold (project_id is a known entity, kept as a category).
Value: TP holds, a moderate real signal (pooled AUC about 0.81, best single feature 0.746). MET-5 fallback roc_auc is in place; whether to score within projects goes to the curator (issue 1).
Quality: notes corrections (CLEAN, writing).
Weighed: size +, source + (Zhang et al. TSE), fit approximate -, pooled metric scores between-project ranking -.
For the curator: issue 1, metric (pooled vs per project, a batch amendment shared with smartshark).

2. CHANGES TO MAKE NOW (no decision needed)
a. Drop contrib_perc_commit (LEAK-10, Must). Among first PRs of non-core contributors, the share with a value above 0 is 64.6% when merged and 22.8% when not; the column alone gives AUC 0.718 there; no code backs "known at opening". Record the ablation, correct the "known at opening" bullet, and withdraw probe 17's "history" reading for this column.
b. Drop integrator_availability (LEAK-10). Its timing is unknown, there is no code, and alone it scores AUC 0.468 (no gain). Record it as "no code, no gain", not as a measured leak.
c. Add a LEAK-9 protocol line: a model scores each test row without using other test rows. This follows the precedents medical_facility_operational_data, sepsis_prediction and 5g_energy_consumption.
d. Add a `Potential leak, kept on purpose:` note for description_length (LEAK-10/LEAK-6). It holds the latest state, worth at most +0.0024 AUC. Precedents: onlinenewspopularity, medical_facility.
e. Add a label note (USE-5): merged means merged through GitHub, so squash, cherry-pick and command-line merges read as No. Fit stays approximate.
f. Notes fixes (writing/CLEAN):
   - pushed_delta is in seconds.
   - The known-project share is 94-95% and the note must say what it counts against (the full training set).
   - One line on the 3.35M -> 1.30M row cut.
   - One line on the 180-day decided-within selection, shown as a pair with smartshark's 1-year horizon.
   - The blind reviewer's worry that some counts are dump-time values is left out. The column auditor found them computed as of opening (MSR code), and the critic dropped the point. Optionally name the source table in the notes.
g. Optional, no effect measured: filter the 0.27-0.30% of train rows decided after the window starts (SPLIT-9). Measured 0.818/0.819 vs 0.819/0.816. Keeping them is fine.

3. ISSUES FOR THE CURATOR (ranked)
Issue 1 (P6, MET-1/MET-5, Should; a batch rule question): score ROC AUC within each project, or pooled?
- Problem: an integrator ranks the open PRs of one project. Pooled AUC also rewards knowing which projects merge more.
- Effect (measured now, LightGBM with 300 trees on a 300k training sample, contrib_perc_commit and integrator_availability dropped, 3 windows):
  - project merge rate from training rows, pooled AUC: 0.720 / 0.708 / 0.709
  - pr_succ_rate_at_open alone, pooled AUC: 0.753 / 0.750 / 0.733
  - LightGBM pooled AUC: 0.813 / 0.812 / 0.798
  - LightGBM within-project AUC (mean over projects with both classes): 0.613 / 0.629 / 0.618
  - projects with both classes: 2,529 / 2,796 / 2,383, covering 71% / 75% / 71% of test rows; the other projects would go unscored
  - The project rate carries most of the pooled signal; the within-project task is much harder.
- Advocate: pooled roc_auc is implemented and checked. Per-project scoring would be a 3rd/4th exception, so raise it for the batch rather than hold this dataset. Ship pooled with a README caveat.
- Critic and precedent checker: measure first and take a grouped AUC if the gap is material. The gap is now measured and material, in line with protein_model_quality and huesken (2026-11-04, both measured).
- Decision needed:
  (a) amend MET-5/MET-1 for the batch: score within the unit the actor ranks when the source has no unique metric. This needs a new mean_group_roc_auc metric checked against a reference, and covers github and smartshark alike.
  (b) keep pooled roc_auc and state the 0.71-0.75 project-rate figure in the README.
- My reading: the facts favour (a) in principle. It is still a rule change, so it is the curator's call. The ship verdict does not depend on it; ship with (b) now and switch if the amendment passes.

No other disputed points: the opening briefs converged and there were no rebuttals.

4. AGREED FACTS
- The temporal split is right (SPLIT-8). Training rows predate the test window, with a gap of about 100k rows. project_id is a true entity, and 94-95% of test rows come from known projects by design.
- prev_pullreqs and the rebuilt merge rates are computed as of opening. No copies conflict. The number format gives no gain (0.8288 vs 0.8276).
- 85% of rows are merged. The honest LightGBM pooled AUC is 0.81-0.82, and adding a noise column changes it by about 0.001.
- The contrib_perc_commit evidence is as in change 2a. integrator_availability alone scores 0.468.
- description_length worth is at most +0.0024 AUC.
- Late-decided training rows (0.27-0.30%) have no effect.
- Task gamer exploits, mapped to rules:
  - Exploit 1, deltas of the project counters to later test rows: 0.81-0.82 -> 0.90-0.92 AUC.
  - Exploit 2, the same per requester (requester key rebuilt from account_creation_days): +0.08 to +0.11 AUC.
  - Both are LEAK-9 (an evaluation-level leak). Each feature is valid at its own row. Neither is covered by a definition note or an accepted warning, so both are new. Fix: the protocol line (2c). Coarsening counters or account_creation_days is not needed (advocate, critic and precedent agree).
  - No gain from row order, copies, future training rows or recent-only training.

5. CONSISTENCY WITH PRECEDENT
Consistent:
- dropping review/CI/final-state fields and lifetime (heart_failure, hotel, noaa_storm_events)
- rebuilt merge rates (garments, mortgage)
- dropping personal attributes (house_sales, distribution_transformers)
- the description_length note (onlinenewspopularity, medical_facility)
- dropping contrib_perc_commit (online_shoppers PageValues, loan_default)
- dropping integrator_availability (no Case keeps a column with no timing evidence)
- the 180-day window (LEAK-23/24; smartshark took the horizon shape, both allowed)
- project_id as a category (SPLIT-13, EV-4)
- the LEAK-9 protocol line (medical_facility and others)
Departure only under issue 1(a): the fact that sets it apart is now measured (project rate 0.71-0.75 of 0.81 pooled; within-project 0.61-0.63). With smartshark it would be the 3rd/4th MET-5 exception of the same reason, so the rule should be amended, not stretched.

Files:
- experiment script: the mediator's experiment script in the run folder
- data it ran on: (the run folder)

</details>

<details><summary>Claim audit</summary>

Claim auditor report: github_pull_request_acceptance_1m (2026-11-09)
Verdict: no claim refuted. Ship as the builder proposes; the open items stay the curator's calls.
Script: t1.py, logs t1.log and t1b.log. The frame was rebuilt with the definition's _load_raw and _clean. No container was built.

| Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| C2/C19 rows | claims 2, 19; curation notes | count after _clean | holds | raw 3,281,386 x 101; clean 2,666,723 | EV-1 |
| C7 10,017 projects | task_summary.row | nunique(project_id) | holds | 10,017 | - |
| C37 window sizes and share of No | splits_comment | month of created_at | holds | Nov 88,913 at 0.1304; Oct 99,992 at 0.1422; Sep 80,238 at 0.1226 | SPLIT-1 |
| C39 train sides before sampling | version_comment | rows opened before window start minus 1 month | holds | 2,477,818 / 2,397,580 / 2,314,345 | SPLIT-10 |
| C46 known projects | splits_comment | test projects present in the full train side | holds (slightly higher) | 95.0% / 94.1% / 95.0% of test rows; builder says 93.8%, likely measured on the sampled 1M | SPLIT-13 |
| C36 friday_effect | claims 36 | flag against a Friday in UTC | holds | 99.97% on Fridays, 0.004% on other days | - |
| C13 created_at rebuild | curation notes | lifetime_minutes is an integer, so seconds(created_at) equals seconds(close) on 100% of rows | holds; a side note follows | the seconds field of the time column is the close's seconds. No leak of the label, but a model given the datetime gets 1/60-minute noise from the close | LEAK-10 (none) |
| C31 prev_pullreqs/first_pr as of opening | claims 31 | prev_pullreqs minus our own count of the contributor's earlier openings in the release | holds | median 0, negative on 0.12% of rows; first_pr=1 with an earlier PR on 0.009% of rows. Counts never run ahead of the opening, so they are not counted at the dump | LEAK-10 |
| C35 copies | curation notes | duplicates on every shipped column | holds | 25 groups (50 rows), none with conflicting labels | LEAK-18 |
| C43 probe 17 (number format) | curation notes, "not tested further" | the builder's open test: refit LightGBM (400k train, Nov 2018) with the number of decimals of three shares added | holds, now tested | ROC AUC 0.8288 without, 0.8276 with; on rows with >=20 earlier decided PRs, decimals of social_strength alone give 0.559. Recording by class is not supported | LEAK-13 |
| C42 project_id ablation | notes | no-project_id model | consistent | 0.8288 without project_id (builder 0.8283) | EV-4 |
| Rebuilt rates use only earlier closes | Decision 3 | code read: merge_asof backward, allow_exact_matches=False on closed_at < created_at | holds by construction. Builder: polars and pandas implementations agree | LEAK-7 |
| Metric fallback roc_auc | metric reason | TSE paper not re-opened | untested: I did not fetch the paper. Several side-by-side metrics with none primary makes MET-5 plausible | MET-1/MET-5 |
| C32 description_length latest state | notes | cannot be tested on the release | untested (data gives no edit history) | gain 0.002 per builder | LEAK-10 |
| C34 integrator_availability timing | notes | no published code | untested | no gain per builder | LEAK-10 |

Ranked refuted: none.
Ranked untested:
(1) description_length and integrator_availability timing (P4). Remedy: the builder's issue 1. Keep with the note, or drop.
(2) Metric source wording (P6). Remedy: one re-read of the TSE paper's Sec. 2.4.3 at review.
Minor: the 93.8% known-projects figure should state its base (sampled train side). The full train sides give 94-95%.

</details>

<details><summary>Column audit</summary>

Column auditor: github_pull_request_acceptance_1m (record github_pull_request_acceptance), 2026-11-09
Prediction point: the opening of the pull request. Evidence: raw release (3,281,386 rows), dataset.py, builder report, dtype probe.

VERDICT: ship after one fix. One kept column, contrib_perc_commit, shows the signature of a post-outcome count (LEAK-10); everything else is fine or already raised by the builder.

Column table:

| Column | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| created_at | opening time, rebuilt as last_close_time - lifetime_minutes | yes (it is the prediction point) | datetime | fine; split column | SPLIT-1 |
| first_pr | contributor's first PR in the project | yes; consistent: first_pr=1 iff prev_pullreqs=0 (checked on all rows) | 0/1 category | fine (redundant with prev_pullreqs, harmless) | CLEAN-12 |
| core_member | contributor in core team before opening | yes by the MSR code | 0/1 category | fine | LEAK-10 |
| prev_pullreqs | PRs the contributor opened before | yes | int, 0-6127, no sentinel | fine | |
| prior_interaction | contributor's interactions in the project, 3 months before | yes by code | int | fine | |
| social_strength | share of interactions with integrators, 3 months before | yes by code | float 0-1, 238 NaN | fine (probe-17 decimals noted by builder) | LEAK-13 |
| followers | contributor followers before opening | yes by code | int | fine | |
| account_creation_days | account age at opening | yes | int 0-4147 | fine | |
| contrib_perc_commit | contributor's share of the project's commits (TSE addition, no published code) | DOUBTFUL: evidence it counts the PR's own commits after the merge | float 0-1 | LEAK (see P1) | LEAK-10, LEAK-13 |
| project_id | GHTorrent project id | yes | category (10,004 levels; dtype probe numeric_levels answered: id, category right) | fine; keep/drop is builder issue 4 | CLEAN-14, USE-10, EV-4 |
| language | project's main language, 6 levels | yes | category | fine | |
| project_age | months since project creation | yes | int 0-135 | fine | |
| sloc, test_lines_per_kloc, test_cases_per_kloc, asserts_per_kloc | size and test density of the base tree | yes by code | numeric, ~2k NaN | fine | |
| team_size | core team size before opening | yes | int, 25,559 NaN, min 1 | fine | |
| perc_external_contribs | share of external contributions before | yes | float 0-1 | fine | |
| open_issue_num, open_pr_num | open issues / PRs at opening | yes | int | fine | |
| pushed_delta | time from last push to opening (unit seconds by range, max 1.57e8) | yes | int, 20k NaN | fine; unit not stated in notes (minor) | |
| fork_num, stars | counts before opening | yes by code | int | fine | |
| integrator_availability | latest activity of the 2 most active integrators, hours 0-23 (TSE, no code) | unknown | int, 240,547 NaN (7.3%) | question (builder raised); alone AUC 0.468, no gain | LEAK-10 |
| description_length | words of title+description, latest MongoDB state | probably, edits possible | int | question = builder issue 1 | LEAK-10 |
| commits_on_files_touched | commits on the touched files before opening (at_open mode) | yes by code | int | fine | |
| friday_effect | opened on a Friday (UTC) | yes; derivable from created_at | 0/1 category | fine | |
| pr_succ_rate_at_open, project_prs_decided_before | project merge share/count among PRs closed strictly before opening | yes (merge_asof backward, no exact matches) | float with NaN / count | fine | LEAK-7, USE-10 |
| requester_succ_rate_at_open, requester_prs_decided_before | same per (project, contributor) | yes | float with NaN / count | fine | LEAK-7 |
| merged (target) | GitHub merge event | outcome | No/Yes | fine (off-button merges = No, noted) | USE-5 |

PROBLEMS, RANKED
P1 (P4, LEAK-10): contrib_perc_commit likely includes the pull request's own commits once merged.
  The curation notes list it under "known at the opening by the source code", but the builder's own report says it is a
  TSE addition without published code, so its timing was never checked (inconsistency in the notes).
  Test: among first-time pull requests of non-core contributors (no earlier PR in the project, not core; 435,229 raw
  rows) the contributor should have almost no commits in the project. Share with contrib_perc_commit > 0:
  merged 64.6% (median 0.00036, i.e. a handful of commits out of thousands) vs not merged 22.8%; AUC of the column
  alone in this subgroup 0.718. Contributors with a single PR in the release, non-core: 62.5% vs 19.7%. The tiny positive
  values on merged first PRs are exactly what a share counted at the dump, with the merged PR's commits inside, produces;
  closed-unmerged PRs' commits never enter the default branch. Also consistent with probe 17's 0.63 for this column.
  Remedy (mildest that removes it): drop contrib_perc_commit; or, if the TSE paper's definition says "before the PR"
  explicitly, keep only with a refit check (rebuild is impossible: the release has no commit table). Expect a visible
  AUC drop on the windows; record the ablation. Then fix the "Kept, known at the opening by the source code" bullet.
P2 (P4, LEAK-10, question): integrator_availability, timing unknown, no code; alone AUC 0.47, no gain. Builder issue
  accepted; mildest remedy drop (it costs nothing) rather than ship an unverifiable column.
P3 (P4, question): description_length, builder issue 1; agree with keep-with-note.
P4 (P7, minor): pushed_delta unit not stated in the notes (values up to 1.57e8, seconds); add to notes. friday_effect
  is a function of created_at, harmless.
No cleaning problems: no sentinels or negatives in kept columns, 0/1 flags categories, the only dtype-probe flag
(project_id) answered. No ordinal columns.

</details>

<details><summary>Split audit</summary>

Split auditor: github_pull_request_acceptance_1m (2026-11-09)

VERDICT: right with notes.

Regime. Use case = an integrator triaging new PRs of a project they know, as they arrive: a stream over time on known
entities (USE-10, SPLIT-13). Declared: temporal on created_at (opening time = prediction point), 3 monthly windows
Sep-Nov 2018, gap 1 month, projects recur. Matches. created_at is rebuilt as close - lifetime_minutes (source code
`pull_reqs`), so it is the opening, not the close the source split on; correct departure.

Numbers re-measured from the raw CSV (polars, independent of the builder; row counts agree within the 6 dedup rows):
  window   train rows  test rows  train labels after window start  of last train month  test projects unseen
  2018-11  2,477,824   88,913     6,702 (0.27%)                    8.35%                5.05%
  2018-10  2,397,585   99,992     7,150 (0.30%)                    8.59%                5.90%
  2018-09  2,314,350   80,239     6,735 (0.29%)                    8.78%                5.04%

Findings (ranked by principles.md):
1. P4, SPLIT-10 (late labels on the train side), minor. With the one-month gap, 0.27-0.30% of train rows (8.4-8.8% of
   the newest train month) were decided only after the window started, so their label is not known at the prediction
   point. The builder's ablation shows no effect (known-at-start 0.818/0.819 vs gap 0.819/0.816, Nov/Oct). Mildest
   exact remedy if wanted: a train-side filter closed_at < window start; otherwise keep and keep the note (it is in
   splits_comment). No change required.
2. P4, LEAK-24/LEAK-23 (the 180-day selection applies to test rows too), note. Test rows are selected on being decided
   within 180 days, a fact unknown at opening; same rule on both sides and in every month, and 14.3-14.8% of test rows
   are decided after their window ends anyway. This is the builder's issue 2; I agree with (a) as shipped. It means the
   test set misses ~2.5-3.3% slow PRs (merged ~40%), so scores read as "among PRs decided within 180 days" (already in
   fit_reason).
3. Grouping/hidden groups: project_id is a true entity id; 94-95% of test rows come from projects in train, by design
   (known-entity use case). Near copies 1.6%, exact copies 0.0% (builder probe). No grouped split needed; the cold
   start (5-6% new projects) is present naturally. Builder's issue 4 (project_id as 10k-level category) is a feature
   question, not a split one; keep.
4. Training history: Aug 2010 onward, random 1M of 2.3-2.5M rows; no-rate drifts 0.15-0.23 (2015-16) to 0.12-0.14
   (2017+). Legitimate history for a refit; a participant can weight recent rows. No issue.
5. Season: Sep-Nov test windows, no holiday month; three consecutive months, fine for a monthly refit horizon.

Alternative split not run: no doubt about the regime; the builder's gap/no-gap/known-at-start ablation already covers
the only open choice and I reproduced its late-label counts.

</details>

<details><summary>Domain practitioner</summary>

Domain practitioner report: github_pull_request_acceptance_1m (record github_pull_request_acceptance)
Actor: an integrator of one GitHub project, at the moment a pull request is opened, triaging the open queue.

FIT: approximate (agree with the definition). The history inputs are what I see at opening and the target is the
outcome I care about, but I would never judge a pull request without its diff (size, files, tests), which is absent,
and I act within my own project, while one row and the score pool 10,017 projects.

1. Inputs at the prediction point (USE-3, USE-4, USE-6)
 - Have and shipped: contributor history (first_pr, core_member, prev_pullreqs, rebuilt requester merge rate),
   project state (open PRs, team size, stars), description length. The rebuilt as-of-opening rates are correct
   (LEAK-7); the source's own rates would have been a leak.
 - Missing that I always have (largest gap): the change as opened - lines added/removed, files touched, whether tests
   are included, number of commits at opening. The release only holds the final state after review (rightly dropped,
   LEAK-10). The source code has an at_open mode but the release does not ship it. Minutes later I also have the CI
   result. Without these the model is a "who is asking" model, not a "what is asked" model.
 - Missing too: whether the author is a bot (dependabot/renovate); I know it instantly and it changes merge odds
   strongly. Not in the data as a flag (25 same-second bot pairs show bots are present).
 - Would not have: nothing shipped looks unavailable at opening, except the caveats already raised: description_length
   (latest state; small gain 0.0024 AUC, I accept keeping it, builder issue 1 option a) and integrator_availability
   (timing unknown, no gain; dropping it costs nothing and removes a doubt - my mild preference).
2. Target (USE-5): GitHub merge event. A proxy: projects that squash/cherry-pick on the command line read as 0, so for
   those projects "rejected" is wrong. A project-level heuristic merge flag (Gousios) would be closer to what I act
   on; a probability is what I want (rank my queue).
3. Row and test (USE-10): one row = one opened pull request = one triage decision, matches. Test = next month on known
   projects, which is my situation (the project is known; keep project_id, builder issue 4 option a). The 180-day
   window (builder issue 2) is acceptable: at opening I do not know how long it takes, but the selection is the same
   in train and test and drops only 2.5%; option (b) "merged within 180 days" would match my decision slightly better
   (a pull request left to rot is in practice a non-merge to me) but adds the dump-end censoring back; keep (a).
4. Would I use it? As a triage aid, partly. Trust: as-of-opening rates, temporal test, no review-time fields. Distrust:
   it mostly encodes "core member / repeat contributor gets merged" (~87% base merge rate), which I already know; it
   cannot tell a good first-time contribution from a bad one without the diff. Personal attributes (gender, country)
   dropped - I would refuse a tool that used them; agree with issue 3 option (a).
5. Metric (MET-1, MET-8, MET-6, MET-9): PARTLY. ROC AUC is the right family (no source threshold or cost, MET-6/MET-7
   do not apply; probabilities preferred, MET-8; no reason for AUPRC, MET-9). But I rank within my project's queue; a
   pooled AUC over 10k projects rewards separating high-merge projects from low-merge ones, which I never need
   (MET-1, unit the actor acts on). The metric I would choose: ROC AUC computed per project (or per project-week queue)
   and averaged over projects with both classes in the window, or log_loss as a proper rule if a single pooled score
   is required (calibrated probability is what a bot/dashboard would show). Suggest the curator weigh a grouped AUC
   with project_id as the scoring group; otherwise keep pooled roc_auc with this caveat in the README.

Ranked gaps: (1) no diff/CI at opening; (2) pooled metric vs per-project ranking; (3) merge-button label misses
command-line merges; (4) no bot flag; (5) 180-day selection; (6) projects chosen as survivors in 2019.
Expert changes: ship at-open change size (needs the SQL dump/at_open code path), a bot flag from the login, score
per project.
Sources: dataset.py task_summary and curation_comments; builder_report.md draft issues 1-4; use_case.md USE-3..USE-10;
metrics.md MET-1, MET-6..MET-9; Gousios et al. ICSE 2015 integrator survey (prioritisation, via the definition);
Zhang et al. TSE 2023 (Table 2 factors, as cited in the definition). No new web lookups.

</details>

<details><summary>Blind review</summary>

Blind review: github_pull_request_acceptance (target merged, binary; temporal split on created_at)
NOTE: my first handback wrongly said the load returned nothing; it had returned. This report replaces that handback.

TASK: Predict whether a GitHub pull request will be merged, using requester, project and PR features known when the PR is opened (Zhang et al., "Pull Request Decisions Explained", TSE 2022; Zenodo 4837134). Real users would be integrators triaging PRs and bots that rank or route them. The data is real and was mined from GHTorrent and GitHub.

VERDICT: include with changes. There is real but moderate signal (temporal holdout AUC 0.817 with default LightGBM on 200k sample, last 20% by time as test). No single feature leaks: the best univariate AUC is 0.746 for pr_succ_rate_at_open. There are no duplicate feature rows. All 32 columns look sensible.

CONCERNS (most to least serious)
1. Snapshot vs at-open timing (not verifiable here). stars, fork_num, followers, open_issue_num, team_size, sloc and test_* must be measured at PR creation time, not at dump time. If they are dump-time values, later information leaks into earlier rows. The arXiv abstract does not state the timing. The *_at_open / *_decided_before columns look like the preparer recomputed them causally, which is good. Change: confirm from the paper's feature table that every factor is computed at creation time, or drop the ones that cannot be confirmed.
2. Class imbalance and drift. merged=Yes is 85% overall. By year it rises from 0.57 (2010) to 0.71 (2011) to 0.87 (2017-18). Volume is heavily concentrated late: 2018 has 80,888 of the 200k sample rows. Test windows will therefore be about 87% positive. Change: use AUC or log-loss, not accuracy. Check the 3 windows are each large enough, which is fine at this size.
3. Self-merge shortcut. core_member and prior_interaction partly encode "the integrator is the submitter", which the source names the top factor. This is legitimate at open time but makes part of the task easy. Keep it, and note it.
4. Preparation. project_id is int64. It should be treated as categorical or dropped: about 11k projects, and the temporal split means it cannot generalise to unseen projects. requester_succ_rate_at_open is 16.6% NaN, meaning first-time requesters; that is informative missingness and fine. integrator_availability is 6.6% NaN. language is categorical and correct.
5. Size. The full table has 1.30M rows, though the source reports 3.35M PRs (some filtering by the preparer). Large: subsample for benchmark cost.

NOT CHECKED: the paper PDF's per-feature timing; how 3.35M rows were reduced to 1.30M; the full table (I only saw the 200k sample); the exact definitions of the 3 test windows; whether the same PR appears in more than one window.

</details>

<details><summary>Task gamer</summary>

Task gamer report: github_pull_request_acceptance (target merged, ROC AUC, 3 temporal windows)

Verdict: the task can be gamed badly. Each test PR's outcome can be read off the later rows of the same project or the same requester in the test window, which lifts AUC from about 0.82 to about 0.91.

Honest baseline: untuned LightGBM, 300 trees, trained on a random 300k sample of each training set, all features.
  r0f0 0.8247 | r1f0 0.8240 | r2f0 0.8110
  Random-noise column added: 0.8237 | 0.8239 | 0.8116 (noise spread about 0.001)
  Training on the most recent 300k rows instead: 0.8236 | 0.8255 | 0.8108 (no gain, so no flaw that hurts the honest model)

| # | Exploit | Honest | Exploited | Gain | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | The next test rows of the same project: deltas of project_prs_decided_before and pr_succ_rate_at_open*decided give the PRs decided (merged or rejected) between this PR and the next one | 0.811-0.825 | 0.903 / 0.915 / 0.912 | +0.078 / +0.091 / +0.101 | No (uses rows from later in the test window) | Score each test row with only past rows. At minimum, ship the test rows shuffled with no project_id, or coarsen the running counters (e.g. bin them) so deltas between rows are not exact |
| 2 | The same, per requester: the requester is rebuilt as project_id + (created_at date - account_creation_days); deltas of requester_prs_decided_before and requester_succ_rate_at_open across that requester's next PR | same | 0.901 / 0.918 / 0.920 | +0.076 / +0.094 / +0.109 | No | As 1; also round account_creation_days to months, or drop it, so the requester key cannot be rebuilt |

   The simple rule "rejections decided before the project's next PR" alone (no model) gives an AUC of 0.667 / 0.684 / 0.698.

Mechanism: the data is sorted by created_at, and the *_decided_before and *_succ_rate_at_open counters are cumulative snapshots taken at each PR's open time. A test PR is often decided before the next PR in its project (or by its requester) opens. The difference between consecutive snapshots then records whether that PR was merged or rejected. A deployed model scores one PR at a time and cannot see that next row. This is test-set composition leakage, not a column leak: each feature alone is valid at the prediction point.

Attacks that found nothing:
- Global row order: the previous row's label as a feature gives 0.826 / 0.823 / 0.812, within noise.
- Copies: only 6 rows have duplicate features; no gain.
- Training rows from the future: none. Every train row is dated before the test window, and the splits leave a gap of about 100k rows.
- Most recent training rows only: no gain (see above).

Not checked:
- Format and decimal artefacts per class.
- A train-vs-test classifier.
- Web "magic feature" threads (no Kaggle competition is known for this source).
- Looking rows up in the Zenodo file. That should work, but it is not a flaw of the task.

</details>

<details><summary>Precedent check</summary>

Precedent checker: github_pull_request_acceptance_1m (record github_pull_request_acceptance), 2026-11-09
Sources: builder_report.md, column_auditor.report.txt, domain_practitioner.report.txt, register.json flags,
leak_checks.md LEAK-10 Cases (lines 475-497), metrics.md MET Cases (lines 297-342), smartshark builder report issue 4.

VERDICT: the definition's calls follow precedent, except two that need the curator: contrib_perc_commit (consistent
to drop, departs if kept) and the per-project AUC (would be the third exception of its kind: amendment due).

1. Dropped review/CI/closer/final-state fields, lifetime_minutes: CONSISTENT with LEAK-10 (heart_failure `time`,
   hotel BookingChanges; LEAK-10/LEAK-37 noaa_storm_events 2026-11-06 for spans ended by the outcome).
2. Rebuilt merge rates: CONSISTENT with LEAK-10/LEAK-7 rebuild-as-of-prediction (garments incentive lag, mortgage lag).
3. Personal attributes dropped (issue 3a): CONSISTENT with LEAK-10 "looked up after the outcome" (house_sales;
   distribution_transformers 2026-10-21, Lennart: drop, no amendment). Tunisian_fraud (2026-11-05) kept registry fields
   only because no mechanism ties them to the outcome; here the lookup is later AND personal (SEL-1): drop holds.
4. description_length kept with a note (issue 1a): CONSISTENT with LEAK-10/LEAK-6 onlinenewspopularity (2026-10-26)
   and medical_facility_operational_data (2026-11-05, Lennart): late state not locatable, whole-field worth
   (+0.0004 to +0.0024) is an upper bound on the late part and small. Needs the `Potential leak, kept on purpose:`
   note with its worth, as in those cases.
5. contrib_perc_commit (column auditor P1): DROP is CONSISTENT. Closest: LEAK-10/LEAK-7 online_shoppers PageValues
   (an aggregate that may hold the row's own outcome; kept only where it behaves like history), loan_default
   (Andrej, 2026-11-03: drop with the leaking block), onlinenewspopularity rule "drop when a gain may sit on the late
   cells". The auditor's subgroup (first PRs, non-core: AUC 0.718 alone, 62.5% vs 19.7%) shows a gain on exactly the
   cells a self-count would hit, and there is no code to say otherwise. Keeping it would depart without a
   distinguishing fact. Note the shipped builder text calls probe 17 "share denominators (history)": that reading
   should be withdrawn for this column.
6. integrator_availability (timing unknown, alone 0.468, no gain): either call is within precedent. Keep-with-note
   precedent (onlinenewspopularity, medical_facility) needs a traceable part or a bounded worth; here the worth is
   bounded (none) but nothing is traceable and there is no code. Dropping a no-gain column of unknown timing departs
   from nothing (no Case keeps a column with no timing evidence at all). Drop is the conservative, consistent call;
   record it as LEAK-10 with "no code, no gain" so it is not read as a measured leak.
7. 180-day window (issue 2a): CONSISTENT with LEAK-24 (smartshark this batch: one-year window on the label horizon,
   newest releases dropped) and LEAK-23. Smartshark chose a horizon label; here a decided-within selection. The two
   differ: (b) here would be the smartshark shape. Not a departure (LEAK-24 allows both), but the curator should see
   the pair side by side: same batch, same censoring problem, two shapes.
8. project_id kept as a category (issue 4a): CONSISTENT with SPLIT-13/USE-10 known-entity cases and EV-4.
9. Fallback roc_auc, temporal split, gap: CONSISTENT with MET-5/MET-6 fallbacks (gallstone_disease, heart_disease,
   taiwanese_bankruptcy: several metrics side by side -> fallback) and SPLIT-10.

10. Per-project ROC AUC (domain practitioner): DEPARTS from the default; reason stated but not measured.
   Precedents of scoring within the unit the actor ranks, both "exception" under MET-5:
   - protein_model_quality_rf_pcp, mean_group_pearsonr on protein_id (2026-11-04, Lennart): fact = pooled RMSE
     rewards a protein's typical quality; each protein's true mean beats LightGBM (0.134 vs 0.188).
   - huesken_sirna_efficacy, mean_group_pearsonr on target_gene (2026-11-04, Lennart): knowing the gene mean cuts
     RMSE 0.1582 -> 0.1378; recorded as "the second exception of this kind".
   - Related, not exceptions: numerai mean_group_pearsonr per era (source's metric, MET-4); blogfeedback top-k per day
     (MET-2 amended 2026-11-02, Andrej; source's metric).
   - Same batch: smartshark issue 4 asks mean_group_roc_auc per release (pooled 0.783 vs per release 0.811, measured).
   Both earlier exceptions rest on a MEASURED fact that pooled scoring rewards the group's mean. Here no such number
   exists: what does project_id-mean alone (or the per-project merge rate) give in pooled AUC vs within-project AUC?
   Also unmeasured: how many of ~10,000 projects have both classes per monthly test window (per-group AUC drops the
   rest; few_minority in groups). If github and smartshark both take a grouped AUC they are the third and fourth
   exceptions of one kind (rank within the actor's queue, source has no unique metric) -> principles.md says an
   amendment of MET-5/MET-1 is due rather than more exceptions. Kept for the review page as the batch-level question.

Reflection prompt (decision 10), issue shape:

Should the merge prediction be scored by ROC AUC within each project rather than pooled over all projects?

**Problem:**
- The integrator ranks the open pull requests of one project; pooled ROC AUC also rewards telling projects with high
  merge rates from low ones, which no integrator needs.
- Two earlier exceptions (protein_model_quality_rf_pcp, huesken_sirna_efficacy, 2026-11-04) took a per-group metric
  on a measured fact; this case has no measurement yet, and smartshark (same batch) asks the same for releases.
- A third exception of one kind means the rule should be amended, not stretched again.

| Option | Pro | Con |
|---|---|---|
| a) per-project ROC AUC (project_id scoring group), on the fact that the project's merge rate alone carries much of the pooled AUC (to be measured: project-rate-only pooled AUC vs within-project AUC) | matches the integrator's queue; same reasoning as the two MET-5 exceptions | new metric `mean_group_roc_auc` (not in the library); many projects lack both classes per window; third exception -> amendment due |
| b) pooled roc_auc (fallback) with the caveat in the README | standard, already implemented and checked; no new rule | scores a between-project ranking nobody makes |
| c) amend MET-5/MET-1 for the batch: score within the unit the actor ranks when the source has no unique metric, then apply to github and smartshark alike | like cases decided alike; ends the exception chain | a rule change on a batch's evidence; needs the metric code and its check against a reference |

Recommendation: measure the project-rate-only pooled AUC first; if it carries most of the signal, take (c) with
github and smartshark together; otherwise (b).

[1]: MET-1, MET-5, MET-8, MET-11; principles.md "Exceptions and amendments".

</details>

<details><summary>Advocate</summary>

ADVOCATE, github_pull_request_acceptance (folder github_pull_request_acceptance_1m). Verdict: ship, with three
changes that need no decision (drop contrib_perc_commit, drop integrator_availability, LEAK-9 protocol line) and the
builder's four issues answered (a).

1. The core design passed every audit. Claim auditor: nothing refuted (C31 prev_pullreqs as of opening, rebuilt rates
   merge_asof strictly before opening, C35 no conflicting copies, C43 number format no gain 0.8288 vs 0.8276). Split
   auditor: temporal split right (SPLIT-8, Must), late train labels 0.27-0.30% with no measured effect (0.818/0.819 vs
   0.819/0.816), project_id a true entity, 94-95% of test rows known projects by design (SPLIT-13, USE-10). No other
   agent contests the regime. Real, moderate signal: blind AUC 0.817, best single feature 0.746 (no one_feature mark).
2. contrib_perc_commit (column auditor P1) is a real LEAK-10 (Must) problem, conceded: merged first PRs of non-core
   contributors 64.6% >0 vs 22.8%, AUC 0.718 alone. The mildest remedy that resolves it is "fix the definition":
   drop the column, record the ablation, correct the "known at opening" bullet (remedy ladder, principles.md 5). It
   is one column of 32; the task stands without it. Precedent checker calls the drop consistent.
3. integrator_availability: timing unverifiable, alone AUC 0.47, no gain. Drop costs nothing (LEAK-10 doubt + no
   gain); all of builder, column auditor, domain practitioner, precedent checker agree. No decision needed.
4. Task gamer's +0.08-0.10 exploit (deltas of running counters across later test rows of the same project/requester)
   is an evaluation-level leak, not a column leak: each feature is valid at its row's opening (gamer's own words).
   LEAK-9 (Should) and its precedent medical_facility_operational_data (2026-11-04, Lennart) settle the fix: a
   protocol line that a model may not use other test rows, not a data change. Coarsening counters would degrade the
   honest task to block a cheat the benchmark can check for.
5. Blind reviewer's snapshot worry (stars, forks, followers, team_size, sloc at dump time) is a note-level question,
   not a blocker: these are the source's published at-creation factors (Zhang et al. TSE, GHTorrent per-PR
   computation), and the claim auditor found the counts it could test (prev_pullreqs) never run ahead of the
   opening. Remedy: name the source table in the notes (keep with a note), not exclusion. Independent of item 2.
6. Metric: pooled roc_auc is the implemented, checked fallback (MET-5). Per-project AUC is unmeasured (precedent
   checker) and would be a third/fourth exception -> a batch amendment question shared with smartshark. That is a
   reason to raise it on the review page, not to hold this dataset: ship pooled with the README caveat (option b),
   switch if the batch amendment passes. Domain practitioner: ROC AUC is the right family.
7. The rest are notes or settled choices: 180-day selection same on both sides, 2.5% rows (LEAK-23/24, split and
   domain agree on (a)); personal attributes dropped (all agree, 3a); project_id kept (EV-4: model limit is no
   argument); known-project share should state its base (94-95% full train); pushed_delta in seconds; 1.30M vs 3.35M
   cut to explain in notes. Squash/cherry-pick merges labelled No is a source-label note (USE-5).

</details>

<details><summary>Critic</summary>

Critic, opening brief: github_pull_request_acceptance_1m (record github_pull_request_acceptance), 2026-11-09
Position: do not ship as defined; ship after the changes below. The task is real (no exclusion asked).

1. contrib_perc_commit likely counts the PR's own commits once merged (LEAK-10, Must).
   Effect: the model reads the outcome off the feature for exactly the hard rows (new outside contributors).
   Evidence: column auditor P1: first PRs of non-core contributors (435,229 rows) have contrib_perc_commit > 0 in
   64.6% if merged vs 22.8% if not; AUC alone in that subgroup 0.718; single-PR non-core 62.5% vs 19.7%. No
   published code (TSE addition), so the notes' "known at opening by the source code" is unbacked. Precedent checker:
   drop is consistent (online_shoppers PageValues, loan_default, distribution_transformers: no amendment for gain
   sitting on changed rows). Remedy: drop it, record the ablation, fix the notes bullet and withdraw probe 17's
   "history" reading for this column.
2. Test-set composition leak through cumulative counters (LEAK-9, Should).
   Effect: a participant reading later test rows of the same project/requester gets 0.82 -> 0.90-0.92 AUC
   (+0.08 to +0.11); the delta rule alone gives 0.67-0.70. Evidence: task gamer exploits 1 and 2. Remedy: the
   LEAK-9 protocol line (models may not use other test rows; checked by the benchmark), as for
   medical_facility_operational_data, sepsis_prediction, 5g_energy_consumption.
3. integrator_availability: timing unknown, no code, no gain (alone AUC 0.468; LEAK-10, Must).
   Evidence: column auditor P2, domain practitioner, precedent checker 6 (no Case keeps a column with no timing
   evidence). Remedy: drop, recorded as "no code, no gain", not as a measured leak.
4. Pooled ROC AUC scores the wrong unit (MET-1, Should).
   Effect: the integrator ranks within one project; pooled AUC over ~10k projects rewards knowing project merge rates.
   Evidence: domain practitioner 5; precedent checker 10: unmeasured, unlike protein_model_quality/huesken.
   Remedy (mildest): measure project-merge-rate-alone pooled AUC and the count of projects with both classes per
   window; if the gap is material, grouped AUC on project_id (with smartshark, raise the MET-5 amendment);
   otherwise keep pooled roc_auc with a README caveat.
5. Label is a merge-button proxy (USE-5, Must, satisfied by a note): squash/cherry-pick/command-line merges read as
   No. Remedy: state it in the notes with fit approximate (already approximate); no change to the target.
6. description_length is latest state (LEAK-10 keep-with-note precedent): worth <= +0.0024 AUC. Remedy: the
   "Potential leak, kept on purpose:" note with its worth (onlinenewspopularity, medical_facility).
7. Notes accuracy (quality, not a reason to exclude): pushed_delta unit (seconds) unstated; known-project share is
   94-95%, not 93.8% (say what it counts); the 3.35M -> 1.30M row reduction and the 180-day selection need one
   line each (blind reviewer 5, split auditor). Remedy: fix the notes.
Dropped: blind reviewer's dump-time worry on stars/followers/sloc: the column auditor found them as-of-opening by
the MSR code; no evidence left to argue it.

</details>
