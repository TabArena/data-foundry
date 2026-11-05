# geoai_ground_level_no2_estimation_challenge

**Outcome:** added. Recommend shipping the previously accepted retrospective unseen-station task after current-main verification. The independent audits found no changed data, target, features, split or metric and no new scientific issue. Each prediction uses only its query row from a held-out station; the complete labeled training archive at other stations remains available. This clarifies the existing context contract without changing it.

**Main points:** Myunghwan accepted the implemented task and its documented limits on 2026-10-30 and explicitly requested reuse of those decisions on 2026-11-05. Issue 1 is preserved as resolved; any new issue must use number 2 or higher.

**Record judgment:** source, year, regression target and grouped regime agree with the definition. Priority 3: source and shape positive; use case approximate; no thin accepted domain or regime and no demonstrated material leak.

**Issues for Myunghwan:**

1. **Retain the source labels while daily aggregation and quality control remain undocumented?**

   - **Problem:** The source codebook identifies ground-station NO2 measurements but does not document the daily aggregation or quality-control procedure.
   - **Effect on the task:** Scores measure agreement with observed released labels; they cannot establish performance on missing monitor days or verify every zero or extreme against sensor flags.
   - **Experiments:** Original-source comparisons preserved all observed target values, including seven zeros and the maximum; only 4,533 rows without targets were removed. No specific invalid-label mechanism was demonstrated.
   - **Consistency:** Preserve faithful source measurements and disclose unverified processing rather than inventing repairs.[^geoai-labels]
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Retain with caveats (implemented) | Keep observed source labels and documented limits | Faithful to the published estimation task | Daily label processing remains unverified |
     | B | Defer for owner clarification | Wait for source aggregation and QC details | May resolve the source uncertainty | Delays the task without demonstrated label corruption |

   - **Recommendation:** A. **Decision:** retained under Myunghwan's recorded acceptance.

**Myunghwan (2026-10-30, ok):** "thse limits are fine".

**Resolved (2026-10-30, Myunghwan):** Accepted as implemented with undocumented daily label aggregation/quality control, regional same-period station transfer and uneven observed-label coverage explicitly retained. On 2026-11-05 Myunghwan requested the updated-main cycle "using our past decision"; this preserves the historical acceptance, not a new answer to a new scientific issue.

[^geoai-labels]: USE-8 and EV-7 require honest scope and uncertainty; CLEAN-11/15 retain unproven extremes and omit missing targets. [Original challenge and data description](https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge/data).

**Review panel:** ship (independent mediator). Focused recheck of the accepted definition against updated main: claim/split audit, column audit, precedent consistency, an isolated participant task gamer, mediator and editor. The prior full panel remains historical evidence. No new curator question was identified; issue 1 stays resolved. The current group learnability rerun and build verification are still pending at this draft.



<details><summary>Current checksum reconciliation</summary>

**Current checksum reconciliation:** The final clarified definition has checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. Two metadata changes explain it completely: the new empty `special_features` field and the added curation-comment clarification of existing row-only context. Before that clarification, current serialization gave `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`; the October artifact stored `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. The earlier audit/mediator paragraphs below describe their preclarification snapshot; the claim audit's final documentation follow-up establishes exact equality of the final data, dtypes, features, target, folds and scorer. No scientific transformation changed.

</details>

<details><summary>Mediator (2026-11-05)</summary>

**GeoAI focused refresh — independent mediator**

Date: 2026-11-05. Current upstream: `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`.

**Judgment record**

**Recommendation: ship the scientifically unchanged, previously accepted definition after the current build and verification finish. No new curator decision is needed.** This is an agent recommendation, not a new curator judgment or build authorization. The curator accepted the implemented limitations on October 30 (“thse limits are fine”) and explicitly requested this refresh using the past decisions on November 5. That instruction supports reusing the recorded acceptance; it does not turn new agent findings into human approvals.

The prior complete panel remains historical evidence. This focused panel addresses changes in upstream rules and serialization and tests whether those changes or fresh evidence undermine that accepted task. I read the current principles, applicable task/metric/cleaning and grouping guidance, focused review-panel contract, definition and REVIEW, claim-auditor, column-auditor, precedent-checker, and the participant task-gamer report. I assessed their evidence and inspected the context contract; I did not independently rerun every reported fit.

- **Validity:** the retained 82,051 labeled station-days, target, 11 model features, dtypes, missingness, and all nine whole-station fold assignments match the accepted version. Independent raw comparisons support the reconstruction. Complete training archives from other stations, including observations later than a particular query day, are intentional for retrospective spatial estimation. This is not an advance forecast or a claim of distant-region transfer.
- **Value:** fresh gamer results show useful, legitimate spatial and calendar signal. A calendar model improves mean RMSE from 10.3701 to 10.0299 across the nine existing folds. Same-day training-station target blends also improve performance modestly. Neither is evidence that the evaluation leaks held-out station labels. The completed historical grouped learnability results and the fresh split-gap result support retaining the station split. They do not establish broad operational deployment performance.
- **Quality:** the minimal reconstruction remains appropriate. Dropping missing targets, parsing Date and excluding row/station identifiers from model inputs have clear roles. No evidence justifies imputation, target transformations, station exclusions, new engineered columns, or altered folds. The column audit found no newly applicable ordinal/categorical recoding requirement.
- **Uncertainty:** the actor interpretation is approximate; source QC, daily aggregation details, product timing/versioning and regional station representativeness remain incompletely established. The source archive was not freshly authenticated and redownloaded. These are preserved limits, not newly verified facts. The curator already accepted this scope.

**Findings resolved by this review**

**Updated rules and checksum**

The new metric guidance permits justified case-specific metric choices; it does not require replacing the original RMSE here. Ground-level NO2 has a meaningful physical scale, and the source competition RMSE is consistent with this accepted task. No measured pathology in the current evidence requires a new metric decision. The precedent check identifies no GeoAI-specific adverse collection decision or new selection rule that changes this conclusion.

The checksum changed because current serialization emits `special_features: []`, which the historical metadata omitted. The claim audit reproduced the historical checksum by removing that one newly serialized empty field, and compared the actual tables and folds. Treat the old UUID and its verification as historical, and build/verify a new artifact with current code. Do not describe old serialized checksum compatibility as unchanged.

**Raw target autocorrelation**

The raw table is date-major, not station-major: each date has the 79 stations and adjacent rows never share a station. The target autocorrelation warning is therefore consistent with same-day cross-station signal. Whole-station splitting addresses station memorization. This raw-order flag alone does not justify temporal folds, row reordering as a scientific fix, or dropping observations.

**Participant context and gamer evidence**

The schema defines `Grouping.context='none'` as **the row only**, and the maintained definition guidance says each row stands alone. For a held-out station, this excludes borrowing its other unlabeled rows for group-level summaries or forward filling. It does not restrict the complete labeled training archive at other stations. A query's own Date, coordinates and supplied daily atmospheric/weather measurements remain available.

Accordingly, training-station same-day averages and nearest-training-station target blends are legitimate modeling strategies under the accepted retrospective task. No exact full-feature cross-fold copies were found. The very correlated nearby station pair does not have identical labels and is evidence of spatial dependence, not a demonstrated duplicate entity.

The gamer's `test_archive_stats` and `archive_ffill` variants require additional rows from the held-out station and are outside the row-only contract. Both worsened RMSE in these tests. Their inclusion in the probe is useful for identifying wording ambiguity, not grounds to broaden the declared context or to add those transformations. The participant kit's original broader archive wording should be preserved as historical probe input, accompanied by an explicit correction. The parent reports adding the clarification to curation comments and REVIEW and recording it in `participant-contract-clarification.md`, without changing features, folds or the context enum. That is the appropriate repair and clarifies the existing contract rather than introducing a new scientific task.

The gamer explored a finite collection of one-seed model variants and public suggestions, not all possible attacks or modeling approaches. Selecting improvements on these same folds gives optimistic estimates of the selected gains. Public write-up approximations are not exact reproductions of unpublished competition pipelines, and coefficients tuned to withheld labels are not legitimized by this review.

**Completion conditions and repairs**

1. Preserve the October 30 human decision and mark this as a November 5 refresh under the explicit reuse instruction. Do not reopen issue 1 or create a fictitious new curator response.
2. Keep the row-only held-out-station clarification in the definition notes and REVIEW; preserve the original gamer kit and its provenance with the separate clarification. This repair is reported applied by the parent.
3. Distinguish fresh checks from retained historical evidence. Fresh checks reported 27 passes and zero warnings; the full suite reports 2,016 passes and 286 skips after the 18 loopback-restricted cases passed in their sandbox-exception retry. Existing repository-wide lint/format failures are baseline findings, not GeoAI regressions.
4. At this report's completion, the current group rerun has produced IID R² 0.788 ± 0.001 versus grouped R² 0.636 ± 0.042 (gap 0.152), but the remaining learnability section is still running. The historical full run remains available, and old/current group feature matrices were verified identical. Record the eventual fresh result or explicitly retain the prior result as historical; do not label unfinished work complete. Full-frame median imputation in this diagnostic limits its quantitative interpretation and does not alter the stored definition.
5. Complete the newly authorized current-code build and artifact verification and record its new UUID/checksum. This mechanical completion is distinct from the scientific ship recommendation.

**New curator questions: none.** A future change to permit all held-out-station rows, change the target/metric/split, broaden operational claims, or introduce target-derived feature construction would require its own explicit scientific review. This refresh does not make any of those changes.

</details>

<details><summary>Claim and split audit (2026-11-05)</summary>

**GeoAI focused claim and split audit, 2026-11-05**

Verdict: ship as previously accepted, subject to the remaining current-cycle probes and reviewer synthesis. This audit found no new scientific choice for Myunghwan. Validity: the source task, retained values, retrospective prediction point, group identity and all nine folds remain consistent with USE-1/8, SPLIT-1/3/23/24 and PROV-1/8. Value: source RMSE remains appropriate and computable on every fold (MET-1/2/3/4/11); previously measured nontrivial signal remains applicable under verified identical inputs. Quality: unchanged source values and missingness, exact date restoration and missing-target removal satisfy CLEAN-2/12/15. The already accepted regional, label-processing and observed-day coverage limits remain explicit rather than upgraded to verified facts.

The audit independently ran `claim_audit_current.py` against the current-main checkout at `9048f36a` and the accepted format-2 container `01a18eeb-f85e-72fe-90a9-e5ae0e7817e7`. Its results are in `claim-audit-current.json`; `checksum-cause.json` isolates the schema-related checksum change and `evidence-reuse.json` records a reproduced model check. No definition or curation record was edited.

**Decisive comparison**

All 82,051 rows, thirteen stored columns, column order, dtypes, category metadata, target values, input missingness and eleven model inputs are exactly equal to the accepted container. Every train/test index in all nine folds is equal. The three metadata objects are equal after loading through the current schema. Independent normalized-separator parsing and key-based comparison also reproduce every retained source value. The current bundle check ran 27 checks with zero errors or warnings.

The checksum changes solely because the current schema serializes the new empty `task_metadata.special_features: []` field. The saved October task JSON omitted it. Recomputing the old container with the current reader gives the new checksum `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`. Removing only that empty list from the canonical encoding recovers the old stored checksum `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. This is a schema compatibility difference, not a changed scientific dataset. Preserve the old artifact and its old-runtime verification evidence; the requested current-code build must establish a new UUID and checksum.

**Claims tested**

| Claim and source within the definition/record | Refutation test | Result and evidence | Rule |
|---|---|---|---|
| Question/use case: estimate daily surface NO2 at stations absent from training | Reopen official challenge and test fold station intersections | Holds; source describes withheld-station estimation; zero shared stations on all nine folds. Analyst/exposure-mapping role is explicitly an interpretation. | USE-1, SPLIT-1 |
| Row: 82,051 station-days, 79 stations, 2019–2021 | Count source rows, target availability, groups and independently parsed dates | Holds: 86,584 raw, 4,533 missing targets, 82,051 retained, 79 groups, 1,096 dates per raw station. | CLEAN-15, EV-1 |
| Target: daily ground NO2, micrograms per cubic metre | Read preserved original codebook Table 1 and compare target values exactly | Holds: codebook identifies ARPA and daily ground-level measurements; every retained target equals raw. | USE-5, MET-3 |
| Known inputs: date, coordinates and eight physical predictors | Compare model input API and original codebook | Holds: exactly eleven inputs; no group ID or target among features. Physical satellite column densities are distinct from the surface concentration. | LEAK-2, CLEAN-22 |
| Inputs and training archive are available at the prediction point | Read declared retrospective point and original source metadata | Supported only for the declared retrospective after-products-available point. Exact publication latency remains unverified; no claim of real-time availability is made. | USE-3/8, LEAK-1/10, EV-7 |
| Train/test dates overlap, but stations and coordinates do not | Check each exact shipped split | Holds: 1,096 shared dates, zero station overlap and zero coordinate overlap in all nine folds. | SPLIT-1/3/24 |
| Preparation only omits missing targets, removes ID_Zindi and restores Date | Independently normalize date separators and compare raw/prepared frames keyed by ID/date | Holds exactly for every retained value and NaN. | CLEAN-2/12/15 |
| Approximate fit acknowledges monitoring-site coverage and undocumented label processing | Read original codebook, current task description and accepted record | Holds as a limitation; representativeness and daily QC are not proven. Existing acceptance does not claim otherwise. | USE-8, EV-7 |
| Labeled coverage is 298–1,093 days and two stations lose about 72% | Fresh per-station counts; reuse exact-identical source audit for per-station breakdown | Holds. Scores concern observed labels, not missing-monitor days. | USE-8, CLEAN-15 |
| Seven zero targets and maximum 188.2333333 are retained | Count prepared values and compare all source values | Holds: seven zeros; exact maximum retained. No new proof of invalid measurements. | CLEAN-11/15 |
| Atmospheric columns and station target are different quantities | Read original codebook units/source rows | Holds: TROPOMI mol/m² versus ARPA micrograms/m³. No direct target-copy relationship is asserted. | USE-5, LEAK-2 |
| Daily aggregation/QC details were not supplied | Inspect original one-page codebook and historical source audit | Still cannot verify actual procedure; the codebook gives resolution and units, not its construction algorithm. | EV-7, PROV-2 |
| Raw training calendar is complete and day-first | Independent parse after normalizing slash/dash separators; within-ID day differences | Holds: 1,096 dates/station and one-day raw gaps. Cleaned labeled calendars have missing days, correctly distinguished. | CLEAN-12 |
| Test dates are month-first and Test.csv is excluded | Independently parse Test; inspect loader and compare exact retained data | Holds. Test is preserved for evidence and contributes no rows to the container. | EV-1, CLEAN-12 |
| ID is group-only; ID_Zindi is removed | Feature list and frame-column inspection | Holds; only category is ID and it is excluded from model inputs. | CLEAN-3, SPLIT-24 |
| Two submission identifiers repeat without duplicate station-days | Count raw ID_Zindi duplicates and station/date duplicates | Holds: ID_LMYYAX and ID_ZHFIGQ recur; zero duplicate station/day keys. | LEAK-16, CLEAN-3 |
| No imputation, smoothing, neighboring-target construction or performance-based station filter | Full raw/prepared equality and code inspection | Holds; all 79 stations retained and raw input NaNs preserved. | CLEAN-2/6/7 |
| Small negative satellite retrievals and negligible cloud excess are retained | Exact equality to the old accepted data/raw; inspect prior primary-product audit | Unchanged. Prior primary documentation supports retaining ordinary negative retrieval noise; no new release or value change invalidates that evidence. | CLEAN-11, EV-2/8 |
| Leaderboard metric is RMSE, distinct from jury assessment | Reopen official evaluation page | Holds: current page explicitly names Root Mean Squared Error; jury also considers correlation and MAE. | MET-1/4/11 |
| RMSE scores original concentration per row, on every fold | Current scorer against direct square-root mean error and historical old-runtime results | Exact equality on all nine folds; dummy RMSE ranges 15.9425–19.0181. Every test fold has positive target variance. | MET-2/3 |
| Six competition test stations differ from the 79 training stations | Fresh Test.csv station and coordinate intersections | Holds: six test stations, zero overlapping IDs and coordinate pairs. | SPLIT-1, EV-1 |
| Groups are real stations with unique coordinates | Exact split overlaps and prior verified source identity; all values unchanged | Holds. The grouped protocol preserves all days for each station on one side. | SPLIT-23/24/26 |
| Splits are 3 repeats × 3 folds, without future-year or distant-region claims | Compare exact memberships with accepted artifact and read scope wording | Holds: 26–27 test stations, 26,637–27,875 test rows. | SPLIT-1/3, USE-8 |
| Empty accepted-warning set; current check passes | Read current check output | Holds: 27 checks, zero errors/warnings/infos. No semantic completeness is inferred from the check count. | EV-3/7 |
| Source/year/citation/licence identify the original challenge | Reopen official page and inspect corrected BibTeX | Holds: ITU-hosted 2024 challenge; ITU AI for Good attribution; CC BY-SA 4.0 stated. Earlier unsupported research-group attribution was already corrected. | PROV-8/9/10 |
| Download recipe identifies the exact accepted source | Fresh SHA-256 and inspect loader | Holds for preserved input: Train.csv SHA-256 fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446. Fresh authenticated redownload remains untested. | PROV-1, EV-7 |
| Earlier screening's temporal/image concerns remain unresolved | Compare dated screening hypothesis with original codebook, accepted definition and current measurements | Refuted as a current claim: those are preserved historical hypotheses, superseded by the accepted physical-measurement spatial task. | EV-2, SEL-15, SPLIT-1 |
| Related paper/sibling candidates establish exhaustive uniqueness | Inspect historical record and prior audit | Not established as exhaustive; historical related-work notes are not scientific evidence of every possible duplicate. No new duplicate evidence found in this focused task. | PROV-4/7/16, EV-7 |
| Accepted model results remain relevant to this dataset | Exact data/fold/scorer comparison, same library versions and fresh one-fold rerun | Holds as historical results under unchanged conditions, with original diagnostic limitations retained. See next section. | EV-8 |

**Reuse of runtime evidence**

The environment remains pandas 3.1.0, numpy 2.5.4, scikit-learn 1.7.2 and LightGBM 4.6.0. The prior fold-safe supplement uses deterministic Date-to-integer-days conversion, native missing handling, 300 LightGBM trees, learning rate 0.05, random_state 0 and two threads. I reproduced its first exact shipped fold and obtained RMSE **10.64631402974271**, bit-for-bit equal to the stored result. Together with exhaustive data/fold/scorer identity, this supports reusing its remaining historical diagnostics; it is not a claim that all 36 ablations or all model families were rerun today.

The only change to the group probe's feature preparation changes missing categorical codes. I separately executed the old and current `features` functions on GeoAI and asserted exact matrix equality: ID is excluded, leaving only numbers and dates. The old group probe's all-row median imputation remains a diagnostic limitation, not a transformation in the shipped data. Prefer the fold-safe supplements when interpreting model quality. New leak and raw-state probes cover additional questions and should still run in the parent cycle.

**New rules and remaining limits**

The updated temporal-gap rules (SPLIT-9/10/14) do not change this accepted retrospective spatial application: it does not claim prospective prediction, and no station label is shared across train/test. The updated metric rules continue to support source RMSE on an unchanged continuous measurement scale; no costs, threshold, ranking-only use case or contradictory metric experiment has arisen. New dtype requirements are consistent with numeric measurements, datetime Date and group-only categorical ID; the independent column audit/probe should confirm this. Spectrum/molecule encoding rules do not apply. The new review-retention procedure requires restoring the resolved issue history, not reopening its accepted uncertainty automatically.

No new curator input is required by this audit. The mildest follow-through is documentation of the checksum cause, preservation of historical acceptance and completion of the remaining new mechanical probes. Ground-label daily aggregation/QC, exact product release latency, station representativeness, fresh authenticated redownload and exhaustive external duplicate search remain unverified at their previously stated scope.

Primary page reopened on 2026-11-05: [Zindi GeoAI challenge](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge), Evaluation section and challenge description. The short exact metric label is “Root Mean Squared Error.” The remaining source claims above are paraphrases. Original DataDescription.pdf Table 1 was read from the curator-supplied release; its preserved text is in the earlier source audit.


**Raw row-order flag: independently reconciled**

The current raw probe flags lag-one target autocorrelation near 0.603, with row-index Spearman -0.066. A fresh structural test in `raw-order-reconciliation.json` rejects the hypothesis that the file is ordered station by station: **zero adjacent rows share a station**. Instead, each of the 1,096 dates lists all 79 stations in the same order. Of 86,583 adjacent row pairs, 85,488 are within one date and only 1,095 cross to the next date. Among finite target pairs, same-day lag-one correlation is 0.60744 (all adjacent finite pairs 0.60411; the probe's preprocessing yields a slightly different 0.603).

Thus the flag primarily detects same-day dependence across nearby-region stations. This is expected structure in the accepted retrospective same-period spatial task, not evidence that the row order exposes a test station's labels. The model sees the actual Date and coordinates, all nine train/test station sets are disjoint, and adjacent station measurements at the same date are available in the declared historical training archive. There is no future-year claim to invalidate. The raw probe also finds zero raw copies; the dropped submission identifier has R² -0.0105, and all 4,533 removed rows lack the target. These observations do not justify removing date, changing the station split or dropping additional rows (SPLIT-1/3/4, LEAK-1/10/16, EV-1/3). They also do not prove every possible exploit harmless: the participant-style reviewer and expanded leak probes retain their own scope.


**Final documentation clarification: independent follow-up**

After mediator review, the definition gained one `curation_comments` bullet spelling out the already declared `grouping.context="none"`: each held-out-station prediction receives the query row only, with no other rows from that station for aggregation/filling; the complete training archive from other stations remains available. I independently compared the final definition with the accepted artifact again. `final-documentation-audit.json` enumerates the full changed metadata values and all nine fold results.

All data values, dtypes, category metadata, feature names/order, target and exact train/test indices remain equal. All nine fresh training-mean RMSE calculations equal both the accepted artifact and direct computation. After current-schema loading, **only `dataset_metadata.curation_comments` differs**; task metadata and experiment metadata have no differences. Its text diff contains exactly the one added context clarification bullet.

The final checksum is `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. Substituting only the earlier curation comments in the checksum encoding recovers the preclarification checksum `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`. Additionally omitting only the newly serialized empty `special_features` list recovers the original accepted checksum `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. These two changes fully explain the checksum difference. No model was rerun for this documentation follow-up; no new scientific choice or invalidation of reusable model evidence was found.

</details>

<details><summary>Column audit (2026-11-05)</summary>

**GeoAI current-main column audit**

Verdict: retain all implemented columns and cleaning. No new curator input is required by this audit. This is a focused recheck against main `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`; the existing acceptance of label-QC uncertainty, same-region same-period transfer and observed-day coverage remains in force.

I read the current column-auditor instructions, principles, use-case rules, cleaning/dtype rules, leakage rules, provenance and metric changes; the current definition; the original DataDescription.pdf text; and the previous column and acceptance reports. I ran current `dtype_probes.py --no-fetch`, then independently loaded the current definition and compared all stored values to the raw release by station/date. Outputs are `dtype/geoai_ground_level_no2_estimation_challenge.json`, `panel/column_audit.py` and `panel/column-measurements.json` in this run.

The current dtype probe examined ten numeric model columns and raised zero flags. Its automatic codebook lookup was intentionally disabled and matched zero codebook columns; this is not a codebook-coverage claim. The manual table below covers every stored column, including the date, station key and target. The source codebook supplies eight physical measurements and the target; station/date/coordinates are read from the actual release and independently checked.

| Column | Meaning and unit | Known at accepted prediction point? | Dtype, cleaning and fresh measured evidence | Verdict and rule |
|---|---|---|---|---|
| Date | Observation day | Yes: the day being retrospectively mapped | `datetime64[ns]`, 1,096 dates from 2019-01-01 to 2021-12-31. Independent separator-normalized day-first parsing agrees for every station/day. | Keep; CLEAN-12/14, USE-3. |
| ID | Ground monitoring station | Identifies the held-out entity; not supplied as a model input | Unordered category, 79 values, no missing. Excluded by `feature_columns`. No words or ordered levels are supplied to decode. | Keep for grouping only; CLEAN-3/12/14, USE-10. |
| LAT | Latitude, degrees | Yes, query location | `float64`, 44.92469405 to 45.88973369; no missing. | Keep measured numeric quantity; CLEAN-14, USE-6. |
| LON | Longitude, degrees | Yes, query location | `float64`, 8.736496578 to 12.59068235; no missing. | Keep measured numeric quantity; CLEAN-14, USE-6. |
| Precipitation | CHIRPS daily precipitation, mm/day | Yes after the relevant daily products are available | `float64`, 0 to 135.3968048; 65,219 zeros, no missing or negative values. Zero is dry weather, not a code. | Keep; CLEAN-10/11/14. |
| LST | NOAA daily land-surface temperature, K | Yes after daily retrieval is available | `float64`, 253.2 to 327.84; 37,594 missing. Surface temperature is distinct from air temperature. | Keep values and missingness; CLEAN-2/11/14. |
| AAI | TROPOMI aerosol index at 354/388 nm, dimensionless | Yes after retrieval is available | `float64`, -5.196266174 to 2.143020488; 12,118 missing, 66,275 negatives. It is a signed index, not an ordered response scale. | Keep numeric; CLEAN-10/11/14. |
| CloudFraction | TROPOMI effective cloud fraction | Yes after retrieval is available | `float64`, 0 to 1.000000044; 12,118 missing. Three microscopic overshoots of one remain as already accepted numerical precision. | Keep; CLEAN-11/14. |
| NO2_strat | Stratospheric vertical NO2 column, mol/m2 | Yes after satellite retrieval is available | `float64`, 1.34e-5 to 7.28e-5; 12,118 missing. Atmospheric column is physically different from ground concentration. | Keep; LEAK-2/10, CLEAN-14. |
| NO2_total | Total vertical NO2 column, mol/m2 | Yes after satellite retrieval is available | `float64`, -1.19e-5 to 0.002047452; 12,118 missing, six negatives. | Keep ordinary retrieval negatives; CLEAN-11/14, LEAK-2/10. |
| NO2_trop | Tropospheric vertical NO2 column, mol/m2 | Yes after satellite retrieval is available | `float64`, -2.53e-5 to 0.000985; 33,429 missing, six negatives. | Keep ordinary retrieval negatives and missingness; CLEAN-2/11/14. |
| TropopausePressure | TROPOMI tropopause pressure, Pa | Yes after retrieval is available | `float64`, 8,614.349685 to 24,449.00715; 12,118 missing. | Keep physical scale; CLEAN-14/21. |
| GT_NO2 | ARPA daily ground-level NO2, micrograms/m3 | Target unknown at the queried location | `float64`, 0 to 188.2333333; seven zeros; 4,533 missing-label raw rows omitted. Every retained value equals the source. | Keep original scale, zeros and extremes; CLEAN-11/15, USE-5, MET-3. |
| ID_Zindi (removed) | Submission identifier | Supplies no scientific quantity | Excluded from current frame; no label/feature reconstruction is based on it. | Drop; CLEAN-3. |

Fresh audit: 82,051 rows, 13 stored columns, exactly 11 features, zero station/day duplicates, zero numeric infinities, and no tested numeric sentinel among -999, -9999, 9999 and 99999. Each stored value and NaN equals the independently transformed source after alignment by station/date. The file SHA-256 is `fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446`. An initial positional comparison differed because the framework shuffles grouped rows; the corrected semantic-key comparison is the evidence, and it passes.

The amended CLEAN-12/14/25 rules require no recoding here: there are no measured values masquerading as categories, no coded response scales with source labels, no yes/no feature flags, and no classification target. The opaque station identifier correctly remains categorical. The date is restored from its actual encoding; no handcrafted seasonal feature is needed. The source table already represents station-days, so CLEAN-19 does not require turning it into an aggregated log or adding label-neighbour features.

The existing source-product and ground-label processing limits remain unverified. The codebook identifies daily physical quantities and their sources but does not establish operational release latency, complete extraction versions or ground-label daily QC. The accepted prediction point is after products are available and uses the historical archive; this audit makes no forecast or real-time claim. Negative satellite retrieval justification reuses the prior documented primary-catalog review; I did not independently refresh that website in this column pass.

No fresh data mechanism supports clipping the seven zero labels, removing extreme targets, deleting sparse-label stations, imputing predictors, or changing the source RMSE. A public competitor's improved score after deleting towns remains insufficient evidence of invalid rows under CLEAN-1/11/20. None of the new dtype rules contradicts the previous acceptance.

</details>

<details><summary>Precedent consistency (2026-11-05)</summary>

**GeoAI current-main precedent and decision consistency**

Verdict: the October 30 scientific acceptance and source-RMSE choice can be reused under current main. No rule exception or repeated human decision is required by this consistency review. This is a bounded focused check, not a new scientific verdict by the agent.

I generated the current decision register before selecting precedents: 4,030 entries, 176 defined rule IDs and 21 collection-wide flags. None of the flags names GeoAI. `register.json`, `register.log` and `panel/precedent-selection.json` retain the inspected evidence. I compared applicable rule changes from `1964e1b2` to `9048f36a`, then read the rule text and relevant case/record lines. Register entries are navigation summaries; rules and attributed curator lines decide.

| Question | Relevant precedent / current rule | Applicability and conclusion |
|---|---|---|
| Keep documented ground-label construction uncertainty? | differentiated_thyroid_cancer_recurrence, Lennart 2026-10-21; USE-5/8 | The current rules still allow a named-source label with unresolved construction detail, case by case, with approximate fit and the actual gap named. GeoAI already names the daily-QC/aggregation uncertainty and Myunghwan accepted it on October 30. No evidence has converted uncertainty into a demonstrated wrong target. Reuse the decision. |
| Are physical satellite quantities excluded as image-derived descriptors? | infrared_thermography_temperature, 2026-10-21; SEL-15 | Its camera-derived temperatures are physical measurements. GeoAI's retrieved atmospheric columns, precipitation, pressure and temperature similarly have named physical units. The codebook and actual schema support the prior scope decision; no raster/image feature block appeared. |
| Does shared historical time imply a temporal forecast instead of station holdout? | 5g_energy_consumption, USE-9 case, 2026-10-14; airfoil_self_noise grouped setup, 2026-10-20 | The first precedent permits same-period spatial estimation at unmeasured stations; the second supports grouping at the real query entity. GeoAI explicitly estimates unseen stations using the observed archive. New as-of forecasting restrictions do not transform its accepted task into advance forecasting. Keep the station holdout and its limited transfer claim. |
| Replace RMSE because current MET-4 permits overruling some competition metrics? | zillow_prize (source MAE retained); african_credit_scoring_challenge (F1 overruled on specific gaming/probability evidence); loan_default_prediction_imperial_college (2026-11-05 amendment) | The amendment allows reasoned case-specific replacement; it does not require replacing valid leaderboard metrics. GeoAI predicts continuous concentration on its original scale, and source RMSE directly measures concentration error. No measured wrong-metric or gaming evidence was introduced in this review. Keep `Metric.source(rmse)`; no new scoring-only input is required under amended MET-2. |
| Recode every number after the new ordinal/label rules? | CLEAN-12/14 amended October 30-November 1; CLEAN-25 | These rules follow semantics. GeoAI has continuous physical measurements, coordinates, a true date, a grouping ID and a regression target. No source-labelled ordinal or nominal numeric levels were found. The ID has no label mapping to recover. Zero dtype flags and the full manual column audit support leaving the representation unchanged. |
| Does a selection marker force a new acceptance decision? | USE-8 and selection-bias guidance; lt_vehicle_loan_default_prediction, November 5 | Selection marker guidance is case-specific and does not itself reject a dataset. GeoAI's monitoring-site/observed-day coverage limits were explicitly accepted and remain named. This pass found no new measured outcome-dependent sampling or class-mix evidence comparable to the loan-approval selection. Do not manufacture a new scientific question from a changed example alone. Keep scope limited to the represented region and observed days; a future source showing preferential station selection by outcome would be new evidence. |
| Add neighbouring ground labels as new features? | CLEAN-19 expansion; rain_in_australia, October 26 | It permits practitioner aggregates when valid at prediction time; it does not authorize a global target-derived neighbour column. GeoAI's existing source table is usable directly, and an unseen test station provides no measured target. The accepted remote-sensing-feature task stays. Any participant finding of a specific legitimate or leaking cross-row mechanism should be judged on its own measured evidence by the mediator. |

Decision provenance is exact: Myunghwan's October 30 statement, "thse limits are fine", accepted the then-implemented task and its identified limits; the November 5 instruction explicitly asks to reuse past decisions while repeating the cycle against updated main. That authorizes preservation after checks, not relabelling the historical marks as newly made decisions. No old browser marks should receive a new fingerprint. Current review history should cite the original decision and the new reuse instruction, retain resolved issue 1, and reserve issue 2 for any genuinely new issue.

The current review workflow also adds an explicit metric acknowledgement and keeps resolved review files. The accepted implementation already declared source RMSE, and the newest instruction preserves that decision. Record its reuse transparently with the original date/context; do not fabricate a new verbatim "metric ok" quote or treat the panel as the curator. Resolved-history formatting and current runtime/probe checks are follow-through work, not grounds to reask accepted scientific limitations.

Limits: this report does not substitute for the separate fresh claim/split audit, current leak/task probes or task-gamer findings. A concrete new mechanism from those checks can reopen an affected decision. None was established by this column/precedent review.

</details>

<details><summary>Participant task gamer (2026-11-05)</summary>

**Independent participant task-gamer report**

**Verdict**

No demonstrated benchmark-breaking exploit in this bounded audit. The held-out-station regime is respected in all nine shipped splits. Best measured improvement is ordinary calendar engineering; nearest-station label blending also improves mean RMSE, but other-station labels are explicitly available at the stated retrospective prediction point. Neither is target leakage. Do not reinterpret this result as a prospective forecasting result or as prediction in a geographically isolated region.

An interface clarification is useful: `grouping.context=none` says no group context, while the prediction point grants the complete satellite/meteorological archive. Coordinates identify stations exactly. Full-archive feature aggregates and forward filling were tested as an aggressive diagnostic; both worsen mean RMSE here. State explicitly whether external archive retrieval at each prediction coordinate is allowed versus accessing other held-out rows. No measured gain establishes an exploit from this ambiguity.

**Reproducibility and baseline**

Only the supplied participant kit and public web sources were inspected. Baseline uses every feature returned by `score.features()` (11 columns), excludes ID and GT_NO2, converts Date to integer days since 2019-01-01, and keeps native numeric missing values. LightGBM is untuned: `LGBMRegressor(n_jobs=2, random_state=0, verbosity=-1)` (100 estimators, default remaining hyperparameters). All scores use the shipped `score()`; no test-label fitting, tuning, early stopping, per-town coefficients, or public raw-label lookup is used. Test labels are used only for scoring and post-hoc duplicate diagnostics.

Environment: Python 3.12.3, LightGBM 4.6.0, pandas 3.1.0, numpy 2.5.4. OMP_NUM_THREADS=2 and OPENBLAS_NUM_THREADS=2. Models are sequential and n_jobs=2. Mean scores below are arithmetic means of nine fold RMSEs, not pooled RMSE. Baseline mean RMSE **10.370071**.

Run `work/probe.py`, `work/copy_diagnostics.py`, `work/supplement.py`, then `work/report.py` with the supplied Python interpreter from the kit directory. Set MPLCONFIGDIR to `$PWD/work/mpl`. Scripts, baseline predictions, diagnostics and CSVs are saved in `work/`.

**Ranked tests against the same baseline**

Positive gain = baseline RMSE minus method RMSE. Ordering includes legitimate improvements and unsuccessful attacks, not just alleged exploits.

| Method | Baseline | Method RMSE | Gain | Wins/9 | Deployment availability and fix |
|---|---:|---:|---:|---:|---|
| calendar | 10.3701 | 10.0299 | +0.3402 | 9/9 | Legitimate row features. Month/day-of-week/day-of-year; no fix. |
| near_blend_half | 10.3701 | 10.1301 | +0.2400 | 7/9 | Legitimate other-station labels. Fixed half blend with nearest same-day training-station label; no fix for stated task. |
| date_label_mean_weight_0.5 | 10.3701 | 10.1434 | +0.2266 | 7/9 | Legitimate other-station labels. Half blend baseline with all training-station labels on date; no fix. |
| near_copy_1 | 10.3701 | 10.3623 | +0.0078 | 2/9 | Legitimate other-station labels. Copy nearest training station if <1 km; no fix. |
| exact_copy | 10.3701 | 10.3701 | +0.0000 | 0/9 | No matches. All permitted features including location and date; no fix. |
| row_order | 10.3701 | 10.3720 | -0.0019 | 6/9 | Artifact unavailable in deployment. Added positional row number; no gain; preserve shuffling. |
| total_minus_strat | 10.3701 | 10.3978 | -0.0278 | 2/9 | Available row covariates. Add total-stratospheric NO2 and use difference to fill trop; no fix. |
| satellite_date_copy | 10.3701 | 10.4307 | -0.0607 | 2/9 | Available training-label lookup. Exact date+non-coordinate predictors with baseline fallback; shared/missing weather is not duplicated target. |
| test_archive_stats | 10.3701 | 10.4587 | -0.0887 | 4/9 | Archive available; batch contract ambiguous. Coordinate-group covariate means/missing rates across full archive; clarify context:none vs complete archive. |
| drop_three_anomalous | 10.3701 | 10.5250 | -0.1549 | 4/9 | Training-only filtering. Remove 3 stations with largest monthly-profile squared distance from training median; no evidence to remove. |
| archive_ffill | 10.3701 | 10.5375 | -0.1674 | 1/9 | Archive available; batch contract ambiguous. Chronological coordinate-group satellite forward fill; clarify archive access. |
| id_diagnostic | 10.3701 | 10.7902 | -0.4201 | 1/9 | Prohibited diagnostic. Numeric suffix and categorical prefix of ID, excluded by task; keep excluded. |
| near_copy_5 | 10.3701 | 10.9743 | -0.6042 | 0/9 | Legitimate other-station labels. Copy nearest training station if <5 km; no fix. |
| format_missing | 10.3701 | 11.0030 | -0.6330 | 1/9 | Available row covariates. Added missingness flags and rounded fractional part of 1000*x; no gain. |
| drop_missing_satellite | 10.3701 | 11.0147 | -0.6446 | 0/9 | Training-only filtering. Exclude rows with NO2_total missing; worsens all folds, retain these rows. |
| near_copy_20 | 10.3701 | 11.6644 | -1.2943 | 0/9 | Legitimate other-station labels. Copy nearest training station if <20 km; no fix. |
| date_label_mean_weight_1 | 10.3701 | 11.8393 | -1.4693 | 0/9 | Legitimate other-station labels. Predict mean of all training-station labels on date; no fix. |
| near_copy_inf | 10.3701 | 12.4661 | -2.0960 | 0/9 | Legitimate other-station labels. Unrestricted same-day nearest station; no fix. |

**Per-fold measured results**

| Fold | Baseline RMSE | Calendar RMSE | Calendar gain | Nearby half-blend RMSE | Blend gain |
|---|---:|---:|---:|---:|---:|
| r0f0 | 10.7401 | 10.4592 | +0.2809 | 11.1616 | -0.4216 |
| r0f1 | 10.6016 | 10.1883 | +0.4134 | 10.1652 | +0.4365 |
| r0f2 | 9.4560 | 9.0169 | +0.4391 | 9.2127 | +0.2433 |
| r1f0 | 10.7462 | 10.3092 | +0.4370 | 10.4238 | +0.3224 |
| r1f1 | 10.7765 | 10.6041 | +0.1724 | 10.3822 | +0.3943 |
| r1f2 | 9.3598 | 9.0645 | +0.2952 | 9.2241 | +0.1357 |
| r2f0 | 10.9788 | 10.7631 | +0.2157 | 11.4314 | -0.4526 |
| r2f1 | 10.0876 | 9.7261 | +0.3615 | 9.2249 | +0.8627 |
| r2f2 | 10.5839 | 10.1375 | +0.4464 | 9.9451 | +0.6389 |

Every method has all nine RMSEs in `per_fold_rmse.csv`, all nine paired gains in `per_fold_gains.csv`, and row-level baseline predictions in `r*f*_baseline.npz`. Full attack gains are also included below.

| Method | r0f0 | r0f1 | r0f2 | r1f0 | r1f1 | r1f2 | r2f0 | r2f1 | r2f2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| calendar | +0.2809 | +0.4134 | +0.4391 | +0.4370 | +0.1724 | +0.2952 | +0.2157 | +0.3615 | +0.4464 |
| near_blend_half | -0.4216 | +0.4365 | +0.2433 | +0.3224 | +0.3943 | +0.1357 | -0.4526 | +0.8627 | +0.6389 |
| date_label_mean_weight_0.5 | -0.8944 | +1.3117 | +0.1226 | +0.2198 | +0.0477 | +0.1417 | +0.8809 | -0.3338 | +0.5434 |
| near_copy_1 | +0.0000 | +0.0581 | +0.0122 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| exact_copy | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| row_order | +0.0072 | +0.0133 | -0.0159 | -0.0353 | +0.0291 | +0.0257 | +0.0089 | -0.0564 | +0.0064 |
| total_minus_strat | -0.0819 | +0.1609 | -0.0542 | -0.0094 | -0.0375 | -0.0995 | -0.2073 | -0.1962 | +0.2753 |
| satellite_date_copy | -0.1423 | +0.0902 | -0.0344 | -0.0549 | -0.0471 | -0.2246 | +0.0215 | -0.1142 | -0.0403 |
| test_archive_stats | -0.4297 | +0.2879 | -0.3750 | -0.0867 | +0.2682 | -0.8205 | +0.2768 | -0.1193 | +0.2004 |
| drop_three_anomalous | -1.4711 | +0.1063 | +0.1011 | -0.4421 | +0.0739 | -0.0181 | +0.4407 | -0.0772 | -0.1078 |
| archive_ffill | -0.3231 | +0.1076 | -0.1808 | -0.1609 | -0.1608 | -0.2645 | -0.2335 | -0.1482 | -0.1429 |
| id_diagnostic | -1.2389 | +0.1292 | -0.2219 | -0.6385 | -0.3191 | -0.2615 | -0.6173 | -0.1314 | -0.4816 |
| near_copy_5 | -0.9670 | -0.0049 | -0.3795 | -0.5666 | -0.1863 | -1.4618 | -1.2298 | -0.3397 | -0.3025 |
| format_missing | -1.7495 | +0.2393 | -0.3733 | -0.6376 | -0.2831 | -1.4785 | -0.2886 | -0.3690 | -0.7564 |
| drop_missing_satellite | -0.9829 | -0.3600 | -0.7170 | -0.6710 | -0.8036 | -0.7273 | -0.4503 | -0.6388 | -0.4507 |
| near_copy_20 | -1.8982 | -0.3087 | -1.5394 | -1.2549 | -0.6777 | -2.2650 | -2.3347 | -0.6212 | -0.7490 |
| date_label_mean_weight_1 | -3.1350 | -0.1548 | -1.3315 | -1.2714 | -1.8284 | -1.4995 | -0.5220 | -2.0367 | -1.4441 |
| near_copy_inf | -3.4236 | -2.0178 | -1.8525 | -1.4875 | -2.3811 | -2.2941 | -3.9292 | -0.6482 | -0.8299 |

**Public-source findings and reproduction limits**

The [official data description](https://zindi.africa/competitions/geoai-ground-level-no2-estimation-challenge/data) identifies ground monitoring stations in Lombardy/Veneto and satellite/meteorological sources, and permits derived features and elevation. It does not establish that any feature contains the withheld station label. No public raw-label retrieval was attempted.

The participant-authored [unofficial third-place account](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge/discussions/23436) describes nearby-town copying, per-town and pre/post-2020 coefficients, removal of three anomalous towns, and forward fill. Reproduced applicable ideas as nearest same-day station copying at fixed 1/5/20 km thresholds, a fixed 50% blend, chronological covariate forward fill, and a training-only monthly-profile rule removing three stations. Pure copying mostly worsens; blending helps on 7/9 folds. The exact excluded towns, coefficients, notebook and selection method are not published in that account, so the anomaly rule is a transparent approximation, not an exact reproduction. Test-town coefficients calibrated from withheld labels would be inaccessible and impermissible here; no result based on such coefficients is claimed.

The [public time-series discussion](https://zindi.world/competitions/geoai-ground-level-no2-estimation-challenge/discussions/21633) reports mixed generalization from date-derived features. This audit measures calendar features directly on the shipped station splits; they improve every fold. Searches for winner code, leakage and papers did not yield a reproducible, more specific magic feature within the bounded search. Elevation retrieval, land-use data and remote-sensing reprocessing were not attempted.

**Negative tests and observations**

- 82,051 rows, 79 station IDs and 79 distinct coordinate pairs. No station ID overlaps train/test in any split. Zero duplicate station/date rows and zero duplicate complete feature rows. Location coordinates are legitimate input for a new station, even though they identify station membership.
- Exact covariate copying matched zero test rows in all nine folds. Omitting coordinates gives 7.49–9.38% date/weather collisions; their labels differ (matched-subset RMSE 11.96–14.98). Full-fold copying results are recorded above, so collision counts alone are not treated as leakage.
- Pairwise aligned-date analysis flags nearby/highly correlated stations. Highest correlation is X5607/X10452, 0.96763 across 1,067 days and about 7.02 km; exact-label equality is 0.094%, with interstation RMSE 4.8898. This is evidence of available spatial signal, not a repeated target series. All flagged pairs are in near_pairs.csv; no near-perfect duplicate sensor labels were found.
- Row order adds essentially no mean benefit. ID numeric suffix/prefix (a deliberately prohibited diagnostic) worsens mean RMSE. Missingness and numerical fractional-format features also worsen. These are bounded probes, not a proof that every possible encoding is harmless.
- Removing the three most anomalous training stations worsens mean RMSE by 0.1549; excluding satellite-missing rows worsens by 0.6446 and hurts every fold. No evidence supports declaring those training rows unjustified. Seven zero targets exist but are not, by themselves, invalid measurements, and were retained.
- Full-archive means/missing rates and forward fill use no held-out labels; both perform worse on average. Total-minus-stratospheric reconstruction likewise fails to improve mean RMSE.

**Uncertainty and skipped scope**

These are cheap fixed experiments with one model seed; no neural models, broad hyperparameter search, external labels, original hidden competition test set, exact winning-code reproduction, geospatial raster download, or prospective temporal split was attempted. Multiple probes share the same nine repeated folds, so selection optimism and dependence apply; tiny differences are not statistically established. The source write-up alone cannot establish leakage, duplicated labels, or invalid training stations. Conclusions are specific to this prediction point and these supplied station splits.

**Artifact fingerprints**

- `task.md` SHA256 `ce7b241415cd1ef41a41054958962c41fe0fe32a75b32ab0a370f99eb0324b4d`
- `task.json` SHA256 `ce21beddbe4ded2dfb45ced54ccfb7320c14a9fb3e07d1bc0c883219fed6090c`
- `score.py` SHA256 `c16f6f7bfd37ff8ff3e9d9fc3e9a34f4113b07cf54fe0e52c5db9f597ca72067`
- `data.parquet` SHA256 `c870ad27a5d172968efe0ab19a39521319cd7c9fb7f15e8f0910bfa4639263d0`
- `splits.parquet` SHA256 `44f2786dabd2efa8e7347afb167623711bfdd41cc9974a8d623a5592d96fa3b9`
- `work/probe.py` SHA256 `8e74a176cb5baffbfedcdaf6394285cdbc25a7722b8b47d32c2c91b340f3a85b`
- `work/supplement.py` SHA256 `bdaf6a068107ab75399439d3406e7367daddb152f17df418f9bb8c9db2ffae36`
- `work/copy_diagnostics.py` SHA256 `568cf1e1ddaffff329c10c9adde19c1c94ef78765a527ad95972c9babfd21692`

</details>


<details><summary>Review editor (2026-11-05)</summary>

**Independent review editor, 2026-11-05**

Recommendation: retain the previous scientific acceptance and finish the authorized cycle after the documentation repairs below and pending verification. No new curator issue is warranted by this cold read. I read the current review-file format, writing and principles references, then REVIEW.md, dataset.py, the generated README and the curation record. This is an editorial/content consistency check; I did not rerun scientific experiments or verify the eventual build.

**Actionable documentation repairs**

- The embedded panel contains 25 Markdown headings beginning with `#`, including report titles and subsections. The current review-file contract expressly disallows headings inside the panel and requires bold text. Convert these headings to bold text while preserving the complete reports and their dated evidence limitations. Keep the dataset's single title. Run the current collector/page validation afterward; do not remove panel evidence merely to make parsing pass.
- The mediator's checksum paragraph and the first claim-audit checksum paragraph describe only the new empty `special_features` field. The later independent follow-up now correctly explains both changes, including the added context clarification in `curation_comments`, and matches the generated README checksum. Preserve the initial audit as historical, but preface it and the mediator report with an explicit statement that their initial checksum explanation predates that clarification; point to the final reconciliation. This avoids a reader mistaking the earlier word “solely” for a statement about the final artifact. No recomputation by this editor is claimed.

The final reconciliation already embedded during this review states the complete chain: final `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`; restoring the old curation comments gives `v2:9fec1067df2a277947357c9caa37944fca3597725746ef0bf01771fb7e46975d`; additionally omitting the newly serialized empty field restores accepted `v2:1a1a2473ac3dd7b97c3b979d5bed4eb5cc1957b861a2272fa7e0ae3ed84d0319`. The independent auditor reports exact unchanged data, features and folds. This is sufficient explanation once the earlier scope is explicit.

**Decision provenance and task meaning**

The record and resolved issue preserve Myunghwan's actual October 30 words, “thse limits are fine”, and distinguish the November 5 instruction to repeat the updated-main cycle using past decisions. The metric CC line explicitly records reuse of the accepted source RMSE rather than inventing a new metric mark or quotation. Issue 1 remains resolved and no issue 2 has been fabricated. Earlier acceptance of limited regional transfer, observed-label coverage and unverified daily QC remains visible. I found no contradictory new scientific evidence that would require asking for these decisions again.

The definition and generated README now clearly separate held-out-station access from the training archive: a prediction may use its own query row, and may use the complete labeled archive at other training stations; it may not aggregate or fill from other rows at the held-out station. The mediator explains why the gamer's two broader archive variants fall outside this context contract. Their measured failures are retained as bounded diagnostics, with the original participant input preserved. Legitimate same-day training-station label blends are not misclassified as held-out target leakage. The definition's instruction not to add neighbouring target values describes curation of the stored feature table, consistent with leaving model strategies to participants.

**Evidence and completion boundaries**

Validity: the content consistently describes retrospective station transfer and an approximate use-case fit, without claiming verified daily label processing or future/distant-region prediction. Value: source RMSE and useful signal remain supported by the dated audits and explicit diagnostic limits. Quality: the documentation describes minimal unchanged source cleaning and states the new context clarification. The evidence does not support inventing a new exception, target filter or feature change.

At this read, REVIEW states that the full current group learnability rerun and build remain pending, and the README says not built. The mediator distinguishes a completed fresh split-gap result from the unfinished learnability section, and identifies prior complete results as historical with verified identical feature preparation. These are honest draft limitations. The parent must append actual completion results and update the current summary before presenting the whole cycle as finished; the dated panel reports should retain their original limitations. Build/commit is already authorized by the November 5 request and requires no repeated scientific confirmation absent a new material finding.

The generated README still describes REVIEW as “removed once they are settled”, contrary to the current retained-history rule. This is inherited generator prose, not a reason to delete REVIEW or hand-edit a generated file. Preserve REVIEW; any generator correction belongs to separate tooling scope. This does not change the dataset decision.

**Read identities**

At the final cold-read fingerprint, REVIEW.md SHA256 was `cf12ca8ae6019fe5b117480320f0a16c2513e86f1e8fea3b08b4bd2107bac27a`; dataset.py was `6c65a8a167e27fe433e216125cd81ce3d42eb4097704f02e5fd0221fb13f722a`; README.md was `a64396876ace985236ab19400347645089cfaa4afe43433b41626c5f4620fe75`; the record was `dc3215efc399f261980d7ad47196c3fd20402f4c9106cc1bee179379bc816d0f`. The parent is actively finalizing these artifacts, so these hashes identify the review inputs rather than asserting final build freshness. No project source file was edited by this reviewer.

**Repair verification, 2026-11-05**

I reread the parent's revision, REVIEW SHA256 `9b3733429ce5709321e21e53ed3c6b6d593ee002e8eaad0a4205217f6a3f899a`. The 25 panel headings have all been converted to bold, and the new current checksum reconciliation explicitly explains both metadata changes and scopes the older paragraphs to their preclarification snapshots. Both substantive repairs are satisfied.

One placement fix remained in that revision: the new reconciliation paragraph sits outside a details section after the panel summary. The format requires only details sections after the first summary paragraph. Wrap the reconciliation in its own details section or put it inside the mediator section, then validate collection/rendering. This is a mechanical format repair with no scientific effect. No further actionable content issue was found; the fresh group run and build remain explicitly pending.


**Application:** All three formatting/content fixes were applied: embedded headings use bold text; the two checksum causes are explicitly distinguished; the checksum reconciliation is enclosed in a details section. The generated collector/parser verifies the final structure.

</details>
