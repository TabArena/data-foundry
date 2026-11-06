# geoai_ground_level_no2_estimation_challenge

**Outcome:** added. Recommend shipping the previously accepted retrospective unseen-station task. The focused recheck found unchanged source values, target, inputs, whole-station folds and source RMSE; no new validity issue was identified. Historical probes still support useful predictive signal, and minimal cleaning preserves the released measurements and missing inputs. Source and dataset size support inclusion; ground-label processing, regional coverage and product timing remain documented limits. No new curator decision is needed; the requested new build remains pending.

**Main points:** No new decision. Myunghwan's 2026-10-30 acceptance and resolved issue 1 remain in force under the repeated instruction to use the past decisions.

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

**Review panel:** ship (independent mediator). The internal-skill refresh uses a focused claim audit, precedent check, mediator and editor; earlier full and focused panels remain dated evidence. Independent comparisons establish unchanged task, data, metadata, folds and checksum. Issue 1 remains resolved under the explicit reuse instruction; no new curator decision. The editor's presentation repairs are applied; the requested new build is pending. Earlier completed-build reports below remain history.



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

<details><summary>Completion of verification (2026-11-05)</summary>

The current full group probe completed over 82,051 rows, 79 stations and all nine folds. IID versus grouped LightGBM R2 is 0.788 versus 0.636 (gap 0.152). Across-group R2 is ridge 0.396, random forest 0.631, LightGBM 0.634 and kNN 0.554, matching the historical printed results. These are indicative utility diagnostics with full-frame median preprocessing, not benchmark rankings. A group-label permutation test does not apply to per-sample labels.

The requested build completed from clean definition commit `2687a3ae2ebd33135af563cf9605e3adbc2897b6`: format 2, UUID `01a1adf0-eb77-7e00-8228-2b3c1bc263db`, checksum `v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`. All 27 checks passed with zero errors or warnings. Saved-container reload verified; a check with only the traced Train.csv (10,000,397 bytes) reproduced the checksum. Rows, nine splits and raw-input selection are unchanged from the October build. The raw-input backup passed ZIP CRC and source SHA-256 checks. The October container is retained because the preserved historical checkout still names it as its current build; no obsolete unreferenced container was deleted.

The source panel reports above retain their original timing and qualifications. Their requested documentation repairs were applied and the current collector rendered one resolved issue, zero open issues, no cross-dataset items and the explicitly reused metric acknowledgement. No new scientific decision is required; the original acceptance and limitations remain in force.

</details>

<details><summary>Internal-skill refresh: mediator</summary>

**Independent mediator — internal skill/runtime refresh, 2026-11-06 UTC**

**Verdict: ship.** Retain the previously accepted scientific definition and complete the authorized current-cycle review and build. This recommendation does not claim that the new build has completed. No new curator decision or scientific change is needed.

Validity: SEL-15, USE-1/3/5/8, SPLIT-1/3/24 and PROV-1 remain supported for retrospective, same-period estimation at withheld stations; unknown daily ground-label aggregation/QC and regional/observed-day coverage remain explicitly limited. No new Must violation is demonstrated. Value: retain source RMSE on the original concentration scale (MET-1/2/3/4); exact fold/scorer identity supports the historical utility evidence under EV-8. Quality: preserve faithful values, missingness and minimal date/identifier cleaning (CLEAN-2/3/11/12/15). Weighed: source and shape positive; approximate use case, no measured thin-category bonus and no newly demonstrated material defect; priority remains 3. For the curator: none.

**Changes and completion work requiring no new decision**

- Preserve the October 30 acceptance and resolved issue 1. Record this cycle as reuse under the explicit repeat-cycle instruction, without inventing a new human mark or rebinding old session fingerprints. This follows the principles' decision precedence and the review-history procedure.
- Clearly distinguish current measured checks from historical model/probe evidence (EV-7/8). The previous November artifact, rather than the October artifact, is the current comparison baseline. Its checksum already matches the fresh in-memory result. The older serialization/context-note checksum change must remain historical.
- Complete editor review and the requested build, saved-container reload and traced-input reproduction, then record their actual results. Until they finish, completion statements are pending (EV-7). The parent corrected the draft verification wording to keep editor/final completion pending; preserve that distinction through handoff.
- Preserve all existing scientific limitations and the query-row-only held-out-station context. No feature, target, metric, cleaning or split edit is warranted.

**Issues for the curator**

None. The fresh claim and precedent reports agree; there is no new disputed fact or weighing call. Acceptance is not being used to waive a Must. It applies because no contrary evidence or changed scientific condition was identified. Daily label QC/aggregation, precise product-release latency, station representativeness, authenticated current download availability and exhaustive duplicate coverage remain unverified; fresh mechanical checks do not establish those facts (USE-8, EV-7).

**Agreed facts and scope of evidence**

This is a focused recheck. Fresh roles are claim auditor, precedent checker and mediator, with editor review still required at this report's completion. The focused-panel procedure calls for a task gamer when features, target or split change; none changed. No new blind review, advocate/critic debate, column/split panel or gamer run is represented as having occurred. Prior full and focused panels remain historical evidence.

The claim auditor's fresh comparison establishes exact equality of every dataframe value, dtype, category metadata, row/column order, missing value, model input, all nine train/test index arrays and all three metadata objects against the previous November container. The checksum is unchanged. Independently parsed raw data retain 82,051 of 86,584 station-days after excluding 4,533 missing targets, with 79 stations and eleven model inputs. All folds have zero station, coordinate and complete-feature overlap, positive target variance, and identical manual/current-scorer RMSE. Their 1,096 shared dates are intentional under the retrospective task. These are measurements relevant to EV-1/2, SPLIT-1/3/24, LEAK-16 and MET-2/3, not a proof of all possible scientific claims.

The source-identity audit and reconciliation agree that all 32 selected procedures and 168 tracked source files match the preceding cycle. The upstream source is the same `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`; previous final head is `5eb90020ef7fad05bdf6f2f60bbca31ae0eb5b81`. Recorded core package versions match, including LightGBM 4.6.0. This supports reuse under unchanged measured conditions, without asserting binary-identical environments or a complete historical transitive-dependency inventory.

Current verification reports 27 bundle checks with zero errors/warnings, zero dtype flags, passing definition imports and dataset lint/format, and 2,017 tests passed: 1,999 initially plus the exact 18 loopback-restricted cases on approved retry; 286 skipped. These are the parent's execution results inspected through the supplied verification evidence, not tests independently rerun by this mediator.

The prior completed group, task, leak, raw-state, column and participant evidence is identified in reused-evidence.json. The completed November group log supersedes the old mediator's then-pending learnability note. The full heavy probe and participant sweeps were not rerun in this cycle. Full-frame median preprocessing limits the historical group diagnostics; fold-safe supplements and finite one-seed participant tests retain their own scope and selection optimism. Exact data, folds, metadata, source and scorer equality makes this reuse adequate for this unchanged-task refresh (EV-8); it does not turn the old numbers into fresh fits.

A supplementary fresh numerical checkpoint, runtime-model-check.json, reproduces all 27,659 predictions of the previous r0f0 LightGBM participant baseline exactly: maximum absolute difference 0.0, RMSE 10.740054356570974. This is one fold, not a new full participant or utility sweep. The initial kit comparison exposed a Parquet station-ID category-label dtype difference (str versus object); exact station strings, model-feature/target dtypes and values, and fold indices were then checked. ID is excluded from model inputs, and the separate direct-container comparison remains exact. This serialization detail does not change the scientific conclusion.

**Historical gamer findings mapped to the current contract**

The prior gamer is reused, not newly run. Its calendar improvement of mean nine-fold RMSE from 10.3701 to 10.0299 uses legitimate query-row information (USE-3/6, LEAK-10). Same-day training-station target blending is legitimate under the complete other-station training archive; its reported gains do not show access to held-out labels (SPLIT-1/3/24). Exact-copy attacks found no matches, consistent with the fresh zero-overlap check (LEAK-16). Nearby correlated stations were not identical target series.

Held-out-station archive aggregates and forward filling were outside `context="none"`; their historical mean RMSE worsened by 0.0887 and 0.1674 respectively. The previous cycle already clarified the row-only contract, so there is no remaining new ambiguity or task expansion (SPLIT-24/26, USE-3/6). Row-order, prohibited identifier and format/missingness probes showed no mean benefit; training-row/station removal also worsened scores. These bounded negative tests are not exhaustive proof (EV-3/6/7). The definition has no accepted-check-warning or `Potential leak, kept on purpose:` exception to reconcile; no measured new exploit requires adding one.

**Consistency with precedent**

The independent precedent report identifies no GeoAI-specific conflict or new drift. Physical quantities follow SEL-15, consistent with infrared thermography temperatures. Same-period station holdout follows the application, consistent with the missing-station use case of 5g_energy_consumption (SPLIT-1/3/24). Approximate named-source labels with explicit construction gaps remain consistent with USE-5/8 and the differentiated_thyroid_cancer_recurrence precedent. Source RMSE remains consistent with MET-4 and the source-metric precedent; no measured pathological incentive justifies replacement. The eight newly extracted register entries are previous-cycle history, including resolved text, rather than eight new decisions. No exception, amendment or reopened curator issue is required.

This mediator inspected the supplied reports, JSON evidence, current definition/README/record/review, relevant procedures and historical mediator/gamer reports. It did not independently rerun models, access remote sources or alter repository files. The scientific ship recommendation is complete; current-cycle editor/build verification remains separate pending work.

</details>

<details><summary>Internal-skill refresh: claim audit</summary>

**GeoAI focused claim audit — internal skill/runtime refresh**

Observed 2026-11-06 UTC. Recommendation: retain the prior scientific acceptance and complete the authorized review/build. **No new curator input is needed.** No refuted current scientific claim was found. This focused audit does not claim that every possible exploit or external duplicate has been excluded.

Validity: exact raw reconstruction, station-disjoint folds and unchanged retrospective query-row contract satisfy the checks relevant to USE-1/8, SPLIT-1/3/23/24, PROV-1 and LEAK-16. Value: source RMSE remains appropriate on the unchanged physical target and is freshly computable on all nine folds (MET-1/2/3/4). Quality: dates, missing-target removal and faithful input/target preservation remain unchanged (CLEAN-2/12/15). Previously accepted limits remain limits.

**What was freshly tested**

`claim_audit_current.py` was adapted into this new panel directory and run through the dedicated capped runtime. It rebuilt the current definition in memory and loaded the previous **November 5** container `01a1adf0-eb77-7e00-8228-2b3c1bc263db`. It did not overwrite that artifact or prior evidence. Assertions passed for exact dataframe values, dtypes, category metadata, column and row order, missingness, eleven model inputs, all nine train/test index arrays, and all three metadata objects. The saved checksum, its fresh recomputation, and the new in-memory checksum are all:

`v2:79bbb806dd322f6c3586bb61f7d86fa3d4315d8e2de3c5f1bdb0015e24596f20`

There is **no new checksum or scientific change** in this cycle. The older October-to-November schema/comment explanation remains historical; it must not be presented as a new difference from the November artifact.

`source_identity_audit.py` independently compared all 32 procedure hashes with the previous instruction manifest. It also compared 168 tracked files selected by `git ls-files src .claude tests pyproject.toml curation/vocabularies.yaml` against both upstream `9048f36a1bcf7da3687fde04b18ef79cd7a1201e` and the previous final commit `5eb90020ef7fad05bdf6f2f60bbca31ae0eb5b81`. All match the current files. This includes model/feature-preparation code, group/task/leak/dtype probes, scorer, container/schema code, role instructions and tests; per-file hashes are in `source-identity-audit.json`. The definition also matches the previous review fingerprint. No new workflow semantics were inferred merely from the integration-pin change.

**Claims and refutation tests**

| Claim (where written) | Test that could refute it | Result and evidence | Rule |
|---|---|---|---|
| “82,051 rows” from “79” stations, 2019–2021 (`task_summary.row`) | Independently parse and count raw and prepared rows/groups | Fresh: 86,584 raw; 4,533 missing targets removed; 82,051 retained; 79 stations; 1,096 raw dates/station and one-day gaps. | CLEAN-12/15, EV-1 |
| “Drop only the 4,533 missing targets” and preserve measurements/NaNs (`curation_comments`) | Compare complete retained raw/prepared frames keyed by independently parsed station/date | Fresh: every retained value and NaN equal; no imputation, filtering by score, smoothing or target-derived stored feature. | CLEAN-2/6/7/15 |
| “ID is a station grouping key and is excluded from model features”; ID_Zindi dropped (comments) | Inspect feature API, full dataframe and duplicate keys | Fresh: eleven inputs, no target or station/submission identifier; zero duplicate station-days; two repeated submission keys remain separate real station-days. | CLEAN-3, LEAK-16 |
| “Whole stations are held out across all dates” (`task_summary.split`, `grouping`) | Compare every fold and intersect stations, coordinates and full-feature row hashes | Fresh: all nine exact memberships match; zero station, coordinate or full-feature hash overlap; 26–27 test stations and 26,637–27,875 test rows/fold. | SPLIT-1/23/24, LEAK-16 |
| Test dates overlap training intentionally (`splits_comment`) | Count date intersections per fold | Fresh: 1,096 shared dates in every fold. Consistent with retrospective same-period spatial task; no forecast claim. | SPLIT-1/3, USE-8 |
| Six original unlabeled stations differ from training (comments) | Parse Test.csv and intersect station/coordinate sets | Fresh: six test stations; zero overlapping IDs or coordinates. Test.csv contributes no container rows. | SPLIT-1, CLEAN-12 |
| Labeled coverage 298–1,093 days; seven zeros, maximum 188.2333333 (comments) | Count coverage and target extremes; exact raw comparison | Fresh: all named counts/extrema match. This does not verify sensor QC or representativeness. | CLEAN-11/15, USE-8 |
| Negative satellite retrievals and cloud excess are retained (comments) | Exact raw equality and fresh extrema | Fresh: negative values unchanged, no NO2 minimum below -0.001 mol/m²; CloudFraction maximum 1.000000044. Product-document explanation is reused from prior audit. | CLEAN-11, EV-2/8 |
| “Root Mean Squared Error (RMSE)” is original metric (`Metric.source`, README) | Inspect current metric metadata and previous source reading | Holds as reused source evidence: previous auditor opened official challenge Evaluation section on November 5 and recorded explicit RMSE, distinct from jury correlation/MAE. No new page access is claimed. | MET-1/4/11, EV-7/8 |
| RMSE scores original ground concentration per row (metric/target) | Score a training-mean prediction with current scorer and previous container, compare manual RMSE on every fold | Fresh: all three exactly equal on all nine folds; each fold has positive target variance. No extra scoring columns required. Target values/scales unchanged. | MET-2/3 |
| Every feature is available at declared prediction point (`task_summary.known`, comments) | Inspect prediction-point wording and original source evidence | Supported for after-products-available retrospective estimation. Exact release latency is still unverified; real-time or as-of-day availability is not established. | USE-3/8, LEAK-1/10, EV-7 |
| “Each prediction uses only the query row” at held-out station; training archive remains available (comments/context) | Read current enum and clarification, compare metadata and old participant findings | Fresh metadata/text inspection: context remains `none`; old held-out archive aggregation variants remain outside contract. Training-station same-day signal is allowed. No new fitting performed. | SPLIT-24/26, EV-8 |
| Raw autocorrelation indicates leakage (possible reading of prior raw probe) | Freshly test raw adjacency and inspect prior decisive test | Fresh: zero adjacent rows share a station; 85,488 adjacent pairs share a date. Prior raw-order reconciliation explains same-day spatial dependence. This flag alone does not refute station holdout. | EV-1/3, SPLIT-1/3 |
| Empty accepted warnings and passing current checks (definition/check log) | Read current check output | Current parent-run check: 27 checks, zero errors/warnings/infos. It is mechanical evidence, not universal scientific assurance. | EV-3/7 |
| Historical model results still apply (record/review completion) | Exact inputs/folds/scorer/source and runtime core-version comparison | Reusable historical diagnostics under unchanged measured conditions; no fresh heavy-model rerun claimed. See below. | EV-8 |
| Original source/citation/year and atmospheric-vs-ground quantities (metadata/comments) | Inspect prior primary-source audit and unchanged raw/definition identity | Reused historical source evidence; no new source publication or raw change is identified. Ground-label aggregation/QC remains undocumented. | PROV-1/8, USE-5, EV-7/8 |

**Evidence reuse and limits**

Current pandas 3.1.0, numpy 2.5.4, scikit-learn 1.7.2 and LightGBM 4.6.0 match the explicitly recorded previous runtime. Build metadata also records the same Python, pyarrow and polars versions. This is package-version evidence, not a claim of identical installed binaries or a complete old transitive dependency inventory.

The November 5 full group log completes the earlier mediator's pending condition: IID/grouped LightGBM R² 0.788/0.636, gap 0.152; grouped ridge 0.396, random forest 0.631, LightGBM 0.634, kNN 0.554. These remain **historical untuned diagnostics** with full-frame median preprocessing; they are neither fresh fits nor tuned benchmark rankings. The prior fold-safe supplements and participant experiments also remain historical, with finite one-seed search and selected-gain optimism preserved. Current source and exact input identity support their reuse; they do not erase those methodological limits. Prior source/scorer/probe files are now hashed and compared against both relevant commits. Prior run files have fresh identifying hashes, without pretending that every old experiment-time byte had a cryptographic attestation.

The prior full panel, focused panel, original-source metric reading and accepted issue history remain applicable. Human acceptance is the October 30 decision, reused under the explicit repeat-cycle instruction; this audit does not create a new human mark or rebind old session fingerprints. Issue 1 remains resolved. A change of target, metric, split, query context or operational scope would need new review; this cycle made none.

**Unsupported or untested claims, ranked**

- P3/P4/P5: actual daily label aggregation/QC, exact product-release latency and station representativeness remain cannot-verify. The mildest remedy is the existing explicit limitations; no demonstrated new invalid-label mechanism requires reopening accepted issue 1.
- P5: a fresh authenticated redownload and exhaustive external duplicate search were not performed. Preserved Train.csv SHA-256 freshly matches `fdee673ab76a4589cf118e10bcb6250ac6c58f132cec76d52ffc6f8b7d104446`; the loader verifies it. This establishes local input identity, not present-day remote download availability or exhaustive uniqueness.
- P6: no claim is made that all historical model experiments were rerun, that every dependency binary is identical, or that the finite gamer search excludes all shortcuts. Preserve their measured, dated scope.

No new concrete curator choice follows from these unchanged accepted limits. The parent still owns the new cycle's final review/build verification and completion record. This reviewer made no repository edits and no transfers.

</details>

<details><summary>Internal-skill refresh: precedent consistency</summary>

**GeoAI precedent consistency — internal skill refresh**

Verdict: **consistent; reuse the existing acceptance, source RMSE, priority 3 and row-only `context="none"` contract. No concrete new human decision is needed.** This is an independent consistency assessment, not a fresh curator mark or a new scientific acceptance. The current instruction explicitly repeats add → review → build while reusing past decisions.

**Scope and evidence identity**

Read the current precedent-checker role, review-added-datasets procedure, principles and applicable use-case, metric, priority and grouping rules; inspected the current definition, REVIEW and record, the October 30 decision session, previous decision-reuse receipt and previous precedent report. Current upstream pin is `9048f36a1bcf7da3687fde04b18ef79cd7a1201e`, the same upstream source already used in the previous cycle, whose final head is `5eb90020ef7fad05bdf6f2f60bbca31ae0eb5b81`.

Reconciliation records all 32 selected procedure hashes equal and zero differences among 168 tracked source files. Runtime resolves Data Foundry to this checkout; the lock adds `lightgbm==4.6.0` and removes nothing. That installation change does not itself change a scientific decision. Fresh runtime checks remain the parent cycle's responsibility.

I independently hashed `dataset.py`, `README.md`, `REVIEW.md` and the curation record: all four match the final snapshot in the previous decision-reuse receipt. No new dataset, source, metric, feature, grouping or review-history modification was identified in this round. The earlier October-to-November checksum change was already reconciled as empty `special_features` serialization plus explanatory row-only context prose; it is not a new change in this refresh.

**Current register, including apparent open issues**

The new register contains **4,038 entries**, against **4,030** in the previous register: **+8, −0**. Both define **176 rule IDs** and contain **21 collection-wide flags**. The complete flag arrays are equal, and **zero flags name GeoAI**. All eight added entries concern GeoAI's completed previous cycle: one metric-reuse CC line, one focused-panel assessment and six lines mechanically classified as `open_issue` from retained REVIEW text. Those six include resolved issue 1 and historical mediator completion instructions. Current REVIEW closes issue 1 and has a completion addendum reporting the finished group probe and build; these register labels are not evidence of six new unresolved decisions. Register flags and extracted lines are navigation candidates, not semantic findings (precedent-checker instructions and principles).

The unchanged `CLEAN-19` amendment-due flag concerns amex and electricity/gas invoice aggregation exceptions, not GeoAI. The unchanged metric exception flags concern within-group ranking/correlation tasks. Neither is a same-facts conflict with per-station-day concentration estimation. Temporal label-maturity flags concern prospective issued-loan outcomes; GeoAI deliberately uses complete other-station archives for retrospective same-period estimation. No new drift or third exception by this curator was identified.

**Per-decision consistency**

| Decision | Classification and rule basis | Closest precedent and distinguishing facts |
|---|---|---|
| Preserve October 30 acceptance with unknown daily ground-label QC/aggregation | **Consistent.** USE-5 expressly permits named-source labels with unverified construction to ship case by case with approximate fit and a named gap; USE-8 and EV-7 require honest limits. CLEAN-11/15 support retaining unproven extremes and excluding missing targets. | `differentiated_thyroid_cancer_recurrence`, Lennart 2026-10-21, is approximate because label breadth/horizon remains unverified (use-case Cases). GeoAI has a defined physical concentration target and source attribution; no evidence now establishes a different or corrupted target. Its curator accepted exactly the remaining uncertainty on 2026-10-30. |
| Retain regional same-period whole-station transfer and observed-label coverage limits | **Consistent.** USE-1/3/8/9/10 and SPLIT-1/3/24 align the split to unseen stations, not an advance forecast. | `5g_energy_consumption`, Lennart 2026-10-14, uses within-period station holdout for missing-station estimation; grouped `airfoil_self_noise` likewise matches the real query entity. GeoAI's complete 2019–2021 archive is intentionally available at other stations. Its 82,051 observed station-days at 79 stations do not establish future-year, distant-region or missing-monitor-day performance. No new measured selection mechanism changes the already approximate fit. |
| Keep physical satellite/weather measurements as tabular inputs | **Consistent.** SEL-15 follows physical measurement semantics. | `infrared_thermography_temperature`, Lennart 2026-10-21, keeps physical temperatures measured with a camera. GeoAI's atmospheric columns and weather measurements are named physical quantities; no new raster-descriptor block appeared. |
| Keep `Metric.source("rmse")` on original concentration scale | **Consistent.** MET-1/2/3/4/11 support a declared source metric at the station-day unit and physical target scale. | `zillow_prize`, Lennart 2026-10-21, keeps source MAE. The MET-4 amendment of 2026-11-05 permits case-specific replacement of weaker competition choices on evidence; it does not require replacement. Unlike `loan_default_prediction_imperial_college` or `african_credit_scoring_challenge`, no measured pathological metric incentive or wrong-use-case evidence is supplied here. RMSE requires no extra scoring column. The existing CC explicitly describes reuse, not a newly supplied metric mark. |
| Keep priority 3 | **Consistent.** The Priority procedure in selection.md starts at 1 and weighs factors; it is not itself a validity rule. PROV-1/8 support source +1; USE-1/8 do not earn a direct-use-case point for an inferred actor. | The measured October 30 and November 5 GeoAI assessments agree: 1 + source 1 + shape 1 + gap 0 + direct-use-case 0 − demonstrated-risk 0 = **3**. The earlier screening's conjectured thin grouped regime was superseded by accepted-definition counts. Nothing in this same-source, unchanged-record refresh supplies a new coverage or risk fact. QC uncertainty remains disclosed; it has not become a demonstrated unclear quantity or damaged target. |
| Preserve the row-only explanation of `context="none"` | **Consistent clarification, not an exception or task expansion.** The maintained definitions guidance says `none` means each row stands alone. USE-3/6/10, SPLIT-3 and LEAK-10 constrain information to the declared task. | The enum already was `none`; the previous mediator clarified it on November 5. Other rows of a held-out station cannot be used for its aggregates/filling. Complete labeled archives at other training stations remain legitimate. The CLEAN-19 `rain_in_australia` case (Lennart 2026-10-26) permits legitimate cross-location information available at prediction time; it does not authorize a global target-derived column or extra held-out-station context. The previous task-gamer results do not change this contract. |

Rules outrank precedents and Must violations cannot be waived just because the curator once accepted a task. Here no newly identified Must violation or unexplained departure was found. Therefore no reflection prompt or manufactured additional approval is appropriate.

**Decision provenance and handoff**

The preserved historical session records Myunghwan's October 30 ship verdict and issue-1 `ok`: “thse limits are fine”. The previous reuse receipt records the November 5 request and completed application. The current authorization again directs the same cycle using past decisions after the internal skill update. These establish reuse authority, not new issue/metric marks. Do not rebind old browser marks to new fingerprints. Keep issue 1 resolved and reserve number 2 or above for an actually new finding. The current review-added-datasets procedure also applies ship when issues, field disagreements and metric are settled; it does not require repeated acceptance of unchanged limits.

The old REVIEW contains historical unfinished-work statements with a later completion addendum. Preserve that chronology. New runtime/build verification must be reported as new execution evidence, not silently substituted for the historical result. This report does not independently rerun models or authenticate a new source download. Ground-label aggregation/QC, operational product latency/versioning, regional representativeness and exhaustive external duplicate coverage remain incompletely established. The historical full-frame median preprocessing limitation in group diagnostics remains; finite participant attacks are not an exhaustive leak proof.


</details>

<details><summary>Internal-skill refresh: review editor</summary>

**Independent review editor, 2026-11-06 UTC**

Verdict: ready for completion after the small presentation edits below. No new scientific issue or curator decision is warranted. The requested new build remains pending at this read; this report is neither a build-verification result nor a new human acceptance.

I read the current editor role, writing guidance, principles and review-file format, then the complete REVIEW, current definition, generated README, curation record and new changelog entry. I checked the fresh claim, precedent and mediator reports against the summary. This was a cold editorial consistency check; I did not rerun experiments or authenticate external sources.

**Concrete edits, in priority order**

1. Make the opening judgment describe this repeat cycle and include its decisive validity, value and quality findings. The current outcome still leads with "after current-main verification" and ends "This clarifies the existing context contract without changing it", which can make the previous cycle's clarification sound newly applied. Replace the whole outcome paragraph with:

   > **Outcome:** added. Recommend shipping the previously accepted retrospective unseen-station task. The focused recheck found unchanged source values, target, inputs, whole-station folds and source RMSE; no new validity issue was identified. Historical probes still support useful predictive signal, and minimal cleaning preserves the released measurements and missing inputs. Source and dataset size support inclusion; ground-label processing, regional coverage and product timing remain documented limits. No new curator decision is needed; the requested new build remains pending.

   Once the new build is actually verified, remove the final pending clause and append its dated completion evidence separately. Do not change the dated earlier reports' pending statements.

2. Keep the main-points line about the curator's decision. Replace:

   > **Main points:** Myunghwan accepted the implemented task and its documented limits on 2026-10-30 and explicitly requested reuse of those decisions on 2026-11-05. Issue 1 is preserved as resolved; any new issue must use number 2 or higher.

   with:

   > **Main points:** No new decision. Myunghwan's 2026-10-30 acceptance and resolved issue 1 remain in force under the repeated instruction to use the past decisions.

   The issue-numbering instruction belongs in the working notes. Preserve the exact original acceptance and subsequent reuse CC entries already present in the record.

3. The newly embedded precedent report ends with "Workspace Bridge's last recorded selected sync finished ..." through "No remote access, transfer, control-plane operation, historical-session rewrite or repository edit was performed." This host-status paragraph is process evidence unrelated to the curator's decision. Keep it in the standalone run report and omit it from the embedded panel copy; no replacement is needed. The REVIEW format keeps run-process details in the run. Existing historical role reports need no rewrite.

**Evidence and scope checks**

- Issue 1 has the required problem, options and recommendation, one implemented row, original quoted answer and explicit resolution. Its rule references are in a footnote. No unresolved record-field disagreement or separate metric choice was identified.
- The metric CC explicitly acknowledges source RMSE by reuse of the accepted implementation, without inventing a new metric mark. The current audit distinguishes the previous official-source reading from fresh scorer checks.
- The fresh reports support exact comparison with the November container: data, dtypes, metadata, inputs, nine fold memberships and checksum. The older October-to-November serialization/context explanation is clearly historical in the fresh reports. The historical full-frame preprocessing limitation, finite participant search and selected-gain optimism remain disclosed. The fresh one-fold LightGBM reproduction is not presented as a new nine-fold sweep.
- The mediator supplies validity, value, quality, weighed factors and the absence of a new decision. Accepted uncertainty is not treated as proof of label quality, real-time availability, broad regional transfer or exhaustive absence of shortcuts.
- The panel is last, uses one summary and closed, nonnested details sections. Public evidence links in REVIEW are portable; no absolute filesystem link or integration-specific link was found there. The new changelog entry has no link-scope problem. Its pending editor/build sentence must be replaced by actual completion evidence only after completion.
- README currently names the previous November build, consistent with the pending new build. Its generated generic description that REVIEW is "removed once they are settled" conflicts with the maintained history-retention procedure, but is an existing generator wording defect. Preserve REVIEW and its resolved issue; this dataset-only repeat cycle need not expand into a shared-generator change or a scientific issue.

The scientific recommendation remains unchanged. Complete the already authorized build and validation, record actual completion, and preserve the distinction between reused human decisions, current measurements and historical evidence.

Application: the opening outcome and main points were rewritten as requested, and the local host-status paragraph was removed only from the newly embedded precedent report. The complete original report remains in the local evidence. No scientific definition changed.

</details>
