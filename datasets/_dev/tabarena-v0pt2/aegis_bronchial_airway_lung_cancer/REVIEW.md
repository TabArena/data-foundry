# aegis_bronchial_airway_lung_cancer

**Outcome:** added. Bronchial-airway gene expression of 639 smokers with a suspicious lung lesion from the AEGIS-1
and AEGIS-2 trials (Silvestri et al. 2015, GEO GSE66499): lung cancer or not, from 32,641 transcript clusters and
sex, one array per patient, random patient folds, scored by ROC AUC as the source built its classifier. The AI recommends shipping it: valid (no leak, copy or exploit found; the per-cohort normalisation is a weak
leak, measured at no effect, issue 2), worth benchmarking (logistic regression 0.750 against a dummy at 0.500 on
every split checked), clean (no missing values). Weighed: a strong source; 639 rows; only two cohorts, too few groups
for a cohort split. Left for you: the use-case fit (issue 1) and the normalisation exception (issue 2). Changed after
the review: the 102 control clusters (lab spike-ins, which carry the scan batch, and background probes) are dropped.
Together with the 554 clusters that copy another cluster (3 of the 557 copies were control clusters), 32,641 of the
33,297 clusters ship. The notes now name the 227 clusters with no annotated type and the 28 recruiting centres, which
cannot be tested as a group.

**Main points:** How to state the use-case fit (implemented: approximate, with the population gap named), and whether to keep the source's per-cohort normalised values as an exception although the raw files exist
(implemented: kept).

**Record judgment:** valid. Two prospective multicentre trials (NEJM 2015) on GEO; the sibling
`lung_cancer_epithelial_genexp` is another cohort and stays its own dataset. Priority 3: gap 0, use case 0, source +, shape 0, risk -.

**Issues for Lennart:**

1. **State the use-case fit as approximate, or reword the use case to triage before the bronchoscopy's result?**

   * **Problem:**
     - The use case names patients whose bronchoscopy gave no diagnosis, but the rows are all 639 bronchoscopy patients, 76% cancer, also those the bronchoscopy diagnosed.
     - The bronchoscopy's result is not in the release, so the nondiagnostic subgroup cannot be cut.
     - The draft's fit "direct" with this wording overstated the match; the definition now says "approximate"[^u1].
   * **Effect on the task:** the score is on a broader, likely more cancer-heavy and easier population than the decision the use case names.
   * **Experiments:** none possible; the release has three sample characteristics only (tissue, sex, diagnosis).
   * **Consistency:** a use case reworded only to excuse a gap is a weighing factor against it[^u2].
   * **Panel:** the domain practitioner judges the fit approximate today but prefers the reword; the advocate and the critic prefer the reword; the practitioner adds that the commercial test is used only after a nondiagnostic bronchoscopy, so a decision before the result has no shown practice; the mediator recommends B unless that practice exists.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Reword, fit direct | use case "triage at bronchoscopy, before its result", one sentence that the commercial test is used in the nondiagnostic subgroup | rows match the decision named; same target and timing | no shown practice of a pre-result decision; rewording to excuse a gap |
     | B | Fit approximate, gap named (implemented) | use case as the source states it; `fit_reason` names the population gap | honest about the gap; the source's own use case | the score is on a broader population than the decision |

   * **Recommendation:** B, unless you know pulmonologists act on a bronchial classifier before the bronchoscopy's result. **Decision:** A or B?

   **Notes for the AI:** on A, rewrite `use_case` in `dataset.py` to triage at bronchoscopy before its result, add the sentence on the commercial test's subgroup, set `fit="direct"` with a `fit_reason` under 70 words; re-run `dataset check`.

   [^u1]: **USE-8** (Must): write how closely the data mirrors the use case, its fit; direct means the rows, the features,
     the label's timing and the split mirror the use case; approximate is a stand-in with a known gap, named as such.
   [^u2]: **USE-9** (Should): before settling on approximate, ask whether the data mirrors another well-defined use case
     that practitioners have; weigh it against a use case rephrased only to excuse a gap.

2. **Keep the source's per-cohort RMA values as an exception, although the CEL files exist?**

   * **Problem:**
     - The values come from RMA, the standard microarray normalisation that pools all arrays it is run on; the source ran it once per trial cohort, so each test array helped set the values of every training array.
     - The raw scanner files (CEL files) are public, and every earlier dataset with raw values available was rebuilt or fixed[^l2].
     - Normalising each array on its own needs a reference fixed outside the data (fRMA, an R package); we would have to port it to Python.
   * **Effect on the task:** measured nil: fitting RMA on the training arrays alone moves the values by 0.02 to 0.03 log2 and the ROC AUC by -0.0006 for logistic regression (SD 0.0012) and +0.0018 for LightGBM (SD 0.021), with no consistent sign.
   * **Experiments:** the builder's numpy RMA per cohort, 2 repeats of 3-fold CV on the 639 kept arrays; the task gamer found no label signal from the normalisation; only the builder measured this; no panel agent re-ran it (the critic notes this).
   * **Consistency:** this would be the first keep with raw files available; what sets it apart is the external frozen reference the rebuild needs and the nil effect[^l1].
   * **Panel:** all agents agree on A; the critic accepts it only with your explicit word and a Cases line in the rule, so the precedent does not widen silently.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, exception with a Cases line (implemented) | the source's values; the notes state the measured nil effect; a Cases line in the rule | the source's values; no own re-implementation; mildest remedy | first keep with raw files available |
     | B | Rebuild with fRMA | per-sample normalisation against a frozen reference | no transductive step | needs R's frozen vectors ported; our values replace the source's; no measured gain |
     | C | Our numpy RMA per cohort | ship our re-implementation | none found | the same leak as A, with our values instead of the source's |

   * **Recommendation:** A. **Decision:** A, B or C?

   **Notes for the AI:** on A, add to LEAK-30's Cases (knowledge-curation, by the curator's word): "`aegis_bronchial_airway_lung_cancer` (2026-11-09): kept; a rebuild needs an external frozen reference (fRMA), measured nil". On B, port fRMA's vectors for pd.hugene.1.0.st.v1, normalise each array alone, re-run the task and leak probes.

   [^l1]: **LEAK-30** (Should when weak): features the source transformed with statistics over all rows (RMA among them)
     are rebuilt from the unprocessed values when the source has them; otherwise kept with a `Potential leak, kept on
     purpose:` note.
   [^l2]: Precedents: `coad_colon_adenocarcinoma` (retired 2026-10-16 for a rebuild from the GDC), `sarcoma` (rebuild
     from the GDC's per-sample values ordered, Lennart 2026-10-19), `home_credit_default_risk` (fixed 2026-10-19: nothing
     computed over all rows); the sibling `lung_cancer_epithelial_genexp` kept its RMA values with a note (Lennart,
     2026-10-19).

**Review panel:** ship after changes (mediator). Full panel; the rebuttal round was skipped because the advocate's and the critic's briefs converged, so the mediator ran no experiment. The final task probe: linear 0.750, no flag, on 5 of 60 splits. Claim audit: no claim refuted. Column audit: the 57 spike-in control clusters carry the scan batch (ROC AUC 0.621 alone; dropped). Split audit: IID right; the 28 centres untestable. Task gamer: no exploit (best 0.583 against an honest 0.731). The leak probe on the final definition finished late with no flag: 0.0% exact copies over 60 splits, nearest-neighbour distance alone ROC AUC 0.534. Blind review: would benchmark; asked for clinical covariates, which the release does not have (closed). Applied with no decision: the 102 control clusters (spike-ins, background) dropped (32,641 clusters and sex now ship; the reports below give 32,740, the count before this drop), notes on the 227 untyped clusters and the 28 centres, the record's source and metric fixed. Disputed and handed over: the use-case fit (issue 1), the LEAK-30 exception (issue 2).

<details><summary>Mediator: aegis_bronchial_airway_lung_cancer</summary>

```text
Mediator report: aegis_bronchial_airway_lung_cancer (2026-11-09).

Summary: ship after changes. Two changes need no decision. The definition drops the 57 affx spike-in clusters and the 45 bgp background clusters, and the README notes the 227 untyped clusters and the 28 centres. The record gets two field fixes. Two issues go to the curator: issue 1 is how to fix the fit wording (USE-8 Must, USE-9 weighing), and issue 2 is confirming the LEAK-30 exception with a Cases line. The briefs converged, so no rebuttals were written and I ran no experiment: no fact is in dispute.

\## Judgment record
Verdict: ship after changes.
Validity: SEL-1 and SEL-2 hold. USE-8 is triggered: "fit direct" claims the nondiagnostic subgroup, but the rows are all 639 bronchoscopy patients. Fix the wording (issue 1). USE-3 and USE-5 hold. LEAK-17 was triggered and is fixed (first array per patient, USE-11). LEAK-13/LEAK-15 are triggered, weak: the 57 affx spike-in clusters carry the scan batch (ROC AUC 0.621 alone) and are fixed by dropping them. LEAK-30 is triggered, weak, measured nil, and kept with a note; it needs the curator's word as an exception (issue 2). SPLIT-1 holds (IID). PROV-4 holds (the sibling is distinct).
Value: TP-1..5 with no flag (linear 0.750 against dummy 0.500 on 30/30 splits; model spread +0.236). MET-5: the source's metric, `roc_auc`.
Quality: CLEAN-22 holds: the width is kept and the 557 identical clusters are dropped. Notes on the 227 untyped clusters and the 28 centres.
Weighed: source +, size 0 (639 rows), few groups (counts against a cohort split).
For the curator: issue 1, a weighing call on the use-case wording (USE-9 reword or fit approximate). Issue 2, confirm the first LEAK-30 keep while the raw files exist.

\## Changes to make now (no decision needed)
1. **Drop the 57 control->affx and 45 control->bgp clusters** (pd.hugene type), with one bullet in the notes. Rules: LEAK-13 (fix the recording artefact by dropping it, measure first) and CLEAN-22 (a column leaves for what it is: lab reagents and background, not the patient).
   - Measured: affx alone 0.621, the same as scan day alone (0.62). Benign share per scan day runs 6%-65%. bgp alone 0.487.
   - The remedy ladder puts a definition fix above a note. The critic and the column auditor ask for the drop, and the advocate accepts it.
   - Keep the normgene clusters: they measure the sample.
2. **README notes** (writing.md, PROV-3):
   - 227 clusters with no pd.hugene type: their meaning is unknown.
   - 28 recruiting centres: a plausible hidden group (SPLIT-29), but no centre id is in the release, so it cannot be tested. Its nearest proxies (scan day, scan month, cohort) show no drop.
3. **Record fields** (PROV-8/9, MET-5): `original_source` Other -> GOV Website; `Metric:` fallback -> source `roc_auc` (Whitney 2015 select their classifier by CV AUC).
4. **Close the blind reviewer's request to add clinical covariates.** The series matrix has three characteristics only (tissue, gender, cancer_yes_no): no age, smoking or lesion size. Keep the gap as already named in `known` (USE-3). Nothing to add.

\## Issues for the curator (ranked)
**1. USE-8 (Must) / USE-9 (Should, a weighing call): the use case names a population the rows do not have.**
- Problem: the use case reads "when bronchoscopy does not give a diagnosis". The rows are all 639 bronchoscopy patients, 76% cancer, including those the bronchoscopy already diagnosed. The bronchoscopy result is not released, so the subgroup cannot be cut.
- Effect: the score is on a broader population, probably more cancer-heavy and easier, than the decision named.
- That "direct" cannot stay with today's text is not in dispute (USE-8 Must). The open choice is the remedy:
  - (a) Reword to "triage at bronchoscopy, before its result" and keep fit direct (USE-9), adding one sentence that the commercial test is used in the nondiagnostic subgroup.
    - For: the domain practitioner, the advocate and the critic prefer it. The brushing is taken before the result and the target (diagnosis within 12 months) is the same.
    - Against: USE-9's own weighing factor, a use case rephrased only to excuse a gap. The practitioner says the test is used only in nondiagnostic patients, so the pre-result triage reading has no shown practice behind it.
  - (b) Set fit approximate and name the population gap in `fit_reason`.
- What would settle it: evidence that pulmonologists act on a bronchial classifier before the bronchoscopy result is in. Without that evidence, (b) is the more honest fit.
- My recommendation: (b), unless you know that practice exists. Both remedies ship.

**2. LEAK-30 (Should when weak): keep the per-cohort RMA although 680 CEL files exist.**
- Problem: LEAK-30 says rebuild when the source has unprocessed values. Every earlier case with raw values available was rebuilt (coad, sarcoma) or fixed (sf_permit_time, home_credit). This would be the first keep with raw files available.
- Effect: measured nil. Values move 0.02-0.03 log2; ROC AUC changes -0.0006 for logistic regression (SD 0.0012) and +0.0018 for LightGBM (SD 0.021), with no consistent sign. Only the builder measured this; the claim auditor did not re-run it.
- Each side's best evidence:
  - All panel agents agree on (a): keep it as an exception. A per-sample rebuild needs fRMA's frozen vectors from R, ported to numpy. That puts our own re-implementation in place of the source's values (P5) for no gain. Option (a) is the mildest rung of the remedy ladder.
  - The critic's condition: only with your explicit word and a Cases line in LEAK-30, "rebuild needs an external frozen reference; measured nil". Otherwise coad and sarcoma read as unlike cases and the precedent widens silently.
- Decision needed: (a) keep with the exception and the Cases line (recommended); (b) rebuild with fRMA; (c) ship our numpy RMA per cohort (no merit over (a)).

Builder issues already settled, no curator call needed:
- First array per patient: all agree, and it follows the breast_cancer_prediction precedent.
- IID split rather than a cohort split: all agree; the alternative splits score within 0.03 of it. A cohort-transfer variant is optional.
- Both sibling datasets in the benchmark: consistent with freddie_mac and numerai28_6. Retiring the smaller sibling would be a new kind of decision, not a precedented one.
- Blind reviewer's width concern: CLEAN-22 and EV-4 say width is no reason to cut columns.

\## Task gamer's attacks
No exploits found. The honest baseline is logistic regression at 0.731. Mapped to rules and notes:
- Normalisation over all rows: LEAK-30, the known `Potential leak, kept on purpose:` note. The gamer measured no label signal, which agrees with the note's nil effect, so it is not an issue.
- Row order (position alone 0.490; LightGBM on position 0.546): LEAK-39 / probe reading 3. Known: the builder's raw probe found the file order (AEGIS-1, then AEGIS-2). It is no exploit at 0.546 against 0.731.
- Repeat arrays "merged or dropped, not checked": LEAK-17. Known and documented: the first array is kept.
- Principal components and per-row statistics (best 0.583): batch or biology that a deployed model also has. This links to the control-cluster drop above; not new.

\## Agreed facts
- 639 patients, one array each, from 680 arrays; 23 patients had 2-4 arrays (22 benign, all AEGIS-1).
- AEGIS-1 298 (220 Yes / 78 No); AEGIS-2 341 (267 / 74). Yes 487 (76.2%).
- 32,740 clusters + `sex` ship. The 557 identical clusters are dropped. No missing values, no duplicate rows.
- Sex matches chrY expression on 680/680 arrays; sex alone scores 0.517.
- Scores: linear 0.750 against dummy 0.500 (30/30 splits); LightGBM about 0.67; at least 50 benign rows per test fold.
- Split check: random 0.728, grouped by scan day 0.734, by scan month 0.705, forward in scan date 0.782. AEGIS-1 -> AEGIS-2 0.769; AEGIS-2 -> AEGIS-1 0.723.
- Exact copies 0.0% over 60 splits; 1-NN agreement 0.643 against chance 0.637.
- Batch: scan day alone 0.62. Models fitted within scan days are no worse than pooled (logistic regression 0.768 against 0.748), so batch gives no gain overall.
- `roc_auc` is the source's selection criterion; NEJM reports AUC 0.78 / 0.74, with age in the source classifier.
- The series matrix holds no clinical covariates beyond sex.
- The RMA values were computed once per cohort.

\## Consistency with precedent
- Six of the seven precedent checks are consistent: first array (breast_cancer_prediction), IID (forest_fires tension), both siblings (freddie_mac, numerai28_6), metric source, record fields, duplicate-cluster drop.
- One departs with a stated reason: LEAK-30 is kept while the raw files exist. The facts that set it apart from coad and sarcoma: the rebuild needs an external frozen reference (not a simple transform undo or a download), and the effect is measured nil. Issue 2 goes to you for that reason.
- No drift found, and this is not a third exception of its kind.
- The control-cluster drop has no conflicting precedent.
```

</details>

<details><summary>Claim audit: aegis_bronchial_airway_lung_cancer</summary>

```text
Claim auditor: aegis_bronchial_airway_lung_cancer (2026-11-09)
Verdict: no claim refuted; ship as built. Scripts: the run folder, t2.py (definition pipeline).

claim | source | test | result | evidence | rule
680 arrays / 639 patients / 23 multi / 41 extra | notes 12-13, dataset.py | parse raw titles | holds | 680 rows, 639 pat, 23 multi, 41 extra; every patient has an array 1 | LEAK-17
Multi-array patients 22 benign, all AEGIS-1 | notes 13 | crosstab | holds | N 22 / Y 1, A1 23 | LEAK-17
Cohort counts A1 298 (220/78), A2 341 (267/74) | notes 12 | crosstab of first arrays | holds | exact | -
Target Yes 487 (76.2%) | notes 16, task_summary | container | holds | 0.7621 | USE-5
32,740 clusters + sex ship; 557 copies dropped | changes | feature_columns; T.duplicated on shipped | holds | 32,741 features, 0 identical columns left | CLEAN-22
No missing, no duplicate rows | notes 27 | count | holds | 0 NaN, 0 dup rows | LEAK-16
Metric roc_auc is the source's | dataset.py metric, notes 26 | read Whitney 2015 PMC4434538 | holds | CV "gave the best AUC"; AUC among accuracy measures; NEJM AUC 0.78/0.74 | MET-1, MET-5
Metric computable on every fold | MET-2 | scorer on dummy 0.5 proba, 60 folds | holds | all 0.500; min 50 benign per test fold | MET-2
12-month follow-up, 299 AEGIS-1 training patients, age in classifier | notes, splits_comment | Whitney 2015 | holds | quoted: "12 months", 299 (223/76), age coef 0.0623 | USE-5, SPLIT-1
Sex not a shortcut (implied) | implied | AUC of sex alone | holds | 0.517 | LEAK-13
No hidden same-specimen copies across patients (implied) | implied, notes 15 | whole-profile correlation between different patients | untested-decisive (raw correlation not discriminative: max between 0.993 vs replicate min 0.984); builder's 1-NN 0.643 vs chance 0.637 stands | LEAK-17
LEAK-30 nil effect; scan-batch; cohort transfer numbers | notes 23-25 | not re-run (CEL RMA, costly) | untested, builder's logs taken | LEAK-30, LEAK-13
"28 centres", "met the criteria for inclusion" | task_summary row, notes 17 | NEJM paywalled | untested | - | EV-1

Ranked open items (none refuted):
1. LEAK-30 (Should) exception: only the builder measured it; the mildest remedy is the note as written (issue 1 option a).
2. Record fields differ (original_source Other vs GOV Website; Metric fallback vs source): update record on curator's word.
3. NEJM details untested: harmless descriptive text.
```

</details>

<details><summary>Column audit: aegis_bronchial_airway_lung_cancer</summary>

```text
Column auditor: aegis_bronchial_airway_lung_cancer (2026-11-09)
Verdict: ship, with one should-fix question (control clusters). No leak by timing; no cleaning error in dtypes.

Prediction point: the bronchoscopy (brushing before its result and the final diagnosis).

Column table
column | meaning | known at prediction? | dtype and cleaning | verdict | rule
lung_cancer (target) | cancer_yes_no Y/N decoded to Yes/No; diagnosis at bronchoscopy or <=12 months follow-up | outcome | category, words | fine | CLEAN-25
sex | GEO 'gender' characteristic, Male/Female; agrees with chrY on 680/680 | yes | category, no missing | fine | -
28,869 'main' transcript clusters (pd.hugene type main, after the 557-copy drop slightly fewer) | RMA log2 gene-level expression of brushed airway cells | yes (brushed at bronchoscopy) | float; RMA per cohort over all arrays (LEAK-30 weak, measured nil by builder) | fine (LEAK-30 exception noted) | LEAK-30
1,195 normgene->exon + 2,904 normgene->intron clusters | Affymetrix normalisation controls (housekeeping exons, intronic background) | yes | float | fine/question: technical, but measure the sample | CLEAN-22
57 control->affx clusters | Affymetrix hybridisation / poly-A / bacterial spike-in and ERCC controls (exogenous reagents added in the lab) | yes in time, but they measure the processing run, not the patient | float | QUESTION / weak batch leak | LEAK-13/15
45 control->bgp->antigenomic clusters | background probes | yes | float | fine (no signal, AUC 0.49) | -
227 clusters without a type in pd.hugene (featureSet type NULL) | unknown (no annotation) | yes | float | fine, meaning unknown | -
dropped: title, gsm, patient, array, tissue | identifiers / constant | - | dropped | fine (trial label correctly not kept) | LEAK identifiers
dropped: 557 duplicate clusters | exact copies of other clusters | - | dropped | fine (unsupervised, value-identical) | CLEAN-22

Dtype probe: 0 of 32,741 flagged (probes/dtype_probes_a.txt); I agree: all expression values are measured quantities as float, sex the only categorical, no ordinal, no proxy missing codes (no missing values at all).

Problem ranked
1. (P4, weak, should) Exogenous spike-in control clusters carry processing-batch signal. Measurement (work_column_auditor/a.py; first array per patient, 639 rows, L2-LR C=0.01 standardised, 3 repeats of 3-fold out of fold ROC AUC): main clusters 0.757; control->affx (57 clusters) alone 0.621; all 4,201 control clusters 0.635; normgene exon 0.643, intron 0.604; bgp 0.487; unannotated 227: 0.625. The affx spike-ins (bac_spike, polyA spike, ERCC) are reagents added in the lab; their 0.62 equals the builder's scan-day-alone 0.62, i.e. they encode the scan batch, which is label-unbalanced (benign share 6%-65% per day). The builder showed models do not gain from batch overall, so the strength is weak. Mildest remedy: drop the 57 control->affx (and the 45 bgp, signal-free) clusters by their pd.hugene type, a documented non-patient-feature drop; keep the normgene clusters (they measure the sample, their AUC is plausible biology). Alternative: keep and add a sentence to the Potential-leak note. Question for the curator.
2. (P5, info) 227 shipped clusters have no type in pd.hugene.1.0.st.v1 3.14.1: meaning unknown; harmless, mention in notes.
3. Builder issues weighed: issue 1 (LEAK-30 kept) agree; issue 2 (first array) agree, the fix is right at column level (label and sex constant across replicates asserted); issues 3 and 4 not column questions.
No post-outcome field, no outcome-caused missingness, no id encoding the label (trial and patient ids are dropped).
```

</details>

<details><summary>Split audit: aegis_bronchial_airway_lung_cancer</summary>

```text
Split auditor: aegis_bronchial_airway_lung_cancer (2026-11-09)

VERDICT: right with notes. IID over 639 patients (one array each), 20 x 3 folds.

Regime. The use case is a new patient at bronchoscopy; patients do not recur (one specimen each after the
first-array fix), so the cold-start question is about the patient, which a random patient split already holds out.
No time column ships (scan date is only in the CEL headers, not a feature); the label (diagnosis within 12 months)
is known for every row and is not a stream-forecast task, so no gap or late-label issue. Grouping: the true group
(patient) is unique per row after the fix; there is no group to hold out.

Checks run (work_split_auditor/alt.py; first arrays, 5,000 most variable clusters, L2 logistic regression C=0.001,
3 repeats x 3 folds; builder's scratch expr.parquet and CEL headers):
  random patients           ROC AUC 0.728 (SD 0.045)
  grouped by scan day (19)  0.734 (SD 0.023)
  grouped by scan month (6) 0.705 (SD 0.086)
  forward in scan date (first 2/3 -> last 1/3, test from 2013-11-27) 0.782 (one split; benign share 19% vs 26%)
  Builder: AEGIS-1 -> AEGIS-2 0.769, AEGIS-2 -> AEGIS-1 0.723 (LR); hidden-groups probe no candidate, near copies 0%;
  exact copies 0.0% over 60 splits; 1-NN 0.643 vs chance 0.637.
None of the alternatives lowers the score materially: the IID estimate is not inflated by processing batch or cohort.

Notes (ranked, principles.md):
1. P4, SPLIT-1 / SPLIT-19 (note, no change): cohort split (builder issue 3). Agree with IID: two concurrent cohorts
   are two groups (a domain-shift test, few groups), the source did not train on one and test on the other, and the
   transfer costs little (above). Mildest remedy if the curator wants it: a variant, not the default.
2. P4, hidden group (note): the 28 recruiting centres are a plausible hidden group (new centre in deployment), but no
   centre id is in the release; the scan-day and cohort groupings, the nearest proxies, show no drop. Name it in
   the README as untestable; no remedy available.
3. P4, LEAK-17 / SPLIT-26 (builder issue 2): agree with first array per patient; it removes the only recurring
   entity and makes IID correct. Option (b) all arrays grouped by patient would also be right but weights 22 benign
   patients 2-4x; not preferable.
4. P4, LEAK-30 (builder issue 1) is a transform leak, not a split problem; its measured effect (+-0.002 AUC) does not
   change the split verdict.

Smallest class per test fold: about 50 benign (152/3), adequate for ROC AUC.
```

</details>

<details><summary>Domain practitioner: aegis_bronchial_airway_lung_cancer</summary>

```text
Domain practitioner report: aegis_bronchial_airway_lung_cancer (2026-11-09)
Actor: pulmonologist after a bronchoscopy for a suspicious lesion in a current or former smoker.

FIT: approximate (definition says direct). Reason: the use case is the classifier applied when bronchoscopy is
NONDIAGNOSTIC (the definition's own use_case text), but the rows are all 639 bronchoscopy patients, ~57% of whom
already got a diagnosis from the bronchoscopy (76% cancer prevalence overall vs a much lower prevalence in the
nondiagnostic / intermediate-risk group where the test is used; NEJM: NPV 91% in 101 intermediate-risk patients
with nondiagnostic bronchoscopy). The bronchoscopy result is not in the release, so the subset cannot be cut.
Under USE-8's selection paragraph this is a selection the real setting does not share -> approximate.
(The figure "272 of 639 nondiagnostic, ~43%" is from my memory of the NEJM paper, paywalled, not verified.)

1. Inputs at the moment (USE-3): yes, the brushing is taken during the bronchoscopy, before the result; sex known.
   Missing that I always have: age (used by the source classifier itself), pack-years, smoking status, lesion size
   and location, and the bronchoscopy result; my pretest probability (Mayo/clinical judgement) is the frame the test
   is interpreted in. The source classifier estimated smoking status and pack-years from expression, so a model can
   partly recover them; age it cannot. Named in `known`; fine as a gap.
2. Target (USE-5): cancer diagnosis from bronchoscopy or within 12 months follow-up is what I act on (rule out ->
   CT surveillance instead of biopsy/surgery). Good. I want a probability (to combine with pretest probability).
3. Row = one patient, one specimen (first array): matches one decision (USE-11). Test = random new patients of the
   same referral population: right for IID. The cohort split (issue 3) is a processing-batch transfer, not my
   decision; I agree with IID. Issue 2 (first array): agree.
4. Would I use it? Only as a rule-out tool in nondiagnostic, low-intermediate risk patients. I would trust it when it
   holds sensitivity >= ~90% (NPV >= 90%) in that subgroup and is calibrated across centres/batches; scan-batch
   confounding (benign share 6%-65% by scan day) and per-cohort RMA would make me ask for locked-preprocessing
   validation, but the measured effects are nil (LEAK-30 keep, issue 1: agree with (a)).
5. Metric (MET-1, MET-6..9): partly. ROC AUC is the source's development criterion (MET-5) and ranks
   probabilities over every threshold (MET-8), so it is defensible. My actual decision is a high-sensitivity rule-out
   threshold: the source reports sensitivity/NPV at the locked cut-off, but fixes no cost matrix or k usable on our
   folds (MET-7: no single threshold transferable to a new model's scores), so a threshold metric is not warranted.
   AUPRC: no (MET-9, positive class is the 76% majority). I would keep roc_auc; if anything, a partial AUC in the
   high-sensitivity region would score my decision better, but it is not the source's and adds a free parameter.

Gaps ranked by how much they change the task:
 (a) population: all bronchoscopy patients instead of the nondiagnostic subgroup the test is for (prevalence and
     difficulty differ; cases diagnosed by bronchoscopy are likely larger/central and easier) -> set fit approximate
     and name it in fit_reason; or reword use_case to "triage at bronchoscopy, before its result" (USE-9) and keep
     direct. I prefer the USE-9 reword plus a sentence on the nondiagnostic use.
 (b) no age/clinical risk factors (named; moderate).
 (c) per-cohort RMA, scan-batch imbalance (measured nil; minor).
What an expert would change: state the decision population honestly (a), keep IID and first array, keep roc_auc.
Sources: dataset.py, README.md, builder_report.md; Silvestri et al. NEJM 2015 abstract via
https://edrn.cancer.gov/data-and-resources/publications/25981554-2695-a-bronchial-genomic-classifier-for-the-diagnostic-evaluation-of-lung-cancer
and https://www.onclive.com/view/new-genomic-test-will-benefit-patients-being-screened-for-lung-cancer ;
use_case.md USE-1/3/5/8/9/11; metrics.md MET-1/5/6/7/8/9.
```

</details>

<details><summary>Blind review: aegis_bronchial_airway_lung_cancer</summary>

```text
Verdict: include with changes - a real clinical task (bronchial-brushing gene expression to rule out lung cancer in smokers with a suspicious lesion, AEGIS-1/2, Silvestri NEJM 2015, GEO GSE66499) with genuine, moderate signal, but it is extremely wide (639 x 32740) and lacks the clinical covariates the published classifier uses.
Task: at bronchoscopy, when the result is non-diagnostic, predict whether the lesion is cancer to decide between CT follow-up and invasive biopsy. This is a real use: it became the commercial Percepta test.
Checks: 639 rows, 32740 float probe columns (Affymetrix Gene 1.0 ST transcript-cluster IDs 7892501-8180418, log2 RMA-like 3-12) plus sex. No missing values, no duplicate rows or columns. Target is 76.2% Yes. A ridge logistic regression with 5-fold CV gets AUC 0.743, which matches the paper's gene-only performance (about 0.74-0.78). That means the signal is real and not trivial.
Concerns, ranked:
1. Width: 32740 features against about 426 training rows per fold. This mostly tests p>>n handling and feature selection rather than tabular learning, and many tree and foundation models will be slow or capped. Fix: keep it as an explicit high-dimensional task, or reduce it to expressed or variable genes (for example the top 2-5k by variance, chosen inside each fold or on biological grounds).
2. Clinical covariates are missing: age, smoking status, pack-years, and lesion size are in the GEO characteristics and in the published model. Without them the task is gene-only and less realistic. Fix: add them if they were recorded before the procedure.
3. Split: the source has two cohorts (AEGIS-1 about 299 and AEGIS-2 about 341, the latter used as independent validation) and probably several processing batches. A random IID split ignores the cohort and batch shift. Fix: keep a cohort or batch column, or offer a cohort-split variant.
4. Normalization: if RMA was run on all samples together, that leaks a little information across folds. This is a minor risk.
5. Sex is coded as a category, which is fine. Probe IDs are not mapped to gene symbols, which is acceptable.
Could not check: the GEO series matrix (I did not download it to confirm the clinical fields, cohort labels, or how the data were normalized), and whether the patients with diagnostic bronchoscopy were excluded from or kept in the cohort.
```

</details>

<details><summary>Task gamer: aegis_bronchial_airway_lung_cancer</summary>

```text
Task gamer report: aegis_bronchial_airway_lung_cancer (target lung_cancer, ROC AUC)
Script: work/a.py   Output: work/a.log   Scope: 12 of the 60 shipped splits

VERDICT
Nothing found that games this task. No feature carries information from after the
bronchoscopy, and no test row has a copy in training.
gamer_prompt.txt was outside the kit and could not be read; worked from task.md.

DATA
639 rows: sex plus 32,740 gene-expression values per patient.
487 cancer, 152 benign (GEO GSE66499).

HONEST BASELINE (ROC AUC, mean and range over the 12 splits)
- Untuned LightGBM, all features: 0.664 (0.597 to 0.723)
- Logistic regression (C=0.001), 5,000 most variable genes plus sex: 0.731 (0.667 to 0.817)
  -> the better honest model; the reference for any exploit.

EXPLOITS RANKED BY GAIN
None found. No fix needed.

FLAWS THAT HURT AN HONEST MODEL
None found.

ATTACKS THAT FOUND NOTHING
- Row order: row position alone ranks the label at 0.490. A LightGBM on position alone
  scores 0.546 (0.503 to 0.618). Neighbouring rows share a label 66.8% of the time vs
  63.7% by chance. Probably a faint trace of the source file order (one study's
  patients, then the other's); this is a guess. Far below 0.73, so no use.
  The random-number noise control was not run.
  Mildest fix if wanted: shuffle row order.
- Per-row statistics: mean, SD, min and max of each row rank the label at
  0.46, 0.51, 0.45 and 0.49. Rows' sorted values differ slightly (mean SD 0.13), so the
  normalisation did not force one identical distribution, but this does not predict the label.
- Principal components over all rows: each of the top 10 alone ranks the label at
  0.40 to 0.58. Row statistics plus top 5 components: 0.583 (0.552 to 0.634).
  Batch or biology a deployed model also has; not an exploit.
- Copies across the split: none. Closest-row correlation median 0.45, max 0.76.
  GEO lists 680 raw arrays for 639 specimens, so the 41 repeat arrays were merged or
  dropped; how was not checked.
- Normalisation over all rows (RMA in the source): uses no labels; showed no label signal.

NOT CHECKED
- Study membership (A1_/A2_ in GEO sample titles): not in the kit; would add little.
- Forum or leak threads: not searched; no competition exists for this dataset.
- Matching kit rows to GSE66499's per-sample labels: not tested.
```

</details>

<details><summary>Precedent check: aegis_bronchial_airway_lung_cancer</summary>

```text
Precedent checker, aegis_bronchial_airway_lung_cancer (2026-11-09)

1. LEAK-30 (Should when weak), RMA kept although the CEL files exist: DEPARTS WITH A STATED REASON, reasonable, but a first.
   Precedents: lung_cancer_epithelial_genexp (2026-10-19/21, Lennart): RMA kept *because* GSE4115 has no CEL files.
   coad_colon_adenocarcinoma (retired 2026-10-16 for a GDC rebuild) and sarcoma methylation (CC 2026-10-19, Lennart:
   rebuild from the GDC's per-sample betas): rebuilt whenever per-sample values existed. sf_permit_time, home_credit
   (principles.md Tensions): fixed when we could. So the register says: raw available -> rebuild. This is the first
   case kept *with* the raw available. Distinguishing facts (written in the notes): (i) no per-sample published value
   exists; a per-sample rebuild needs fRMA's frozen external vectors (R) re-implemented in numpy, not a cheap
   transform undo like coad's z-scores or a GDC download; (ii) measured effect nil (ROC AUC -0.0006 LR, +0.0018 LGBM,
   no sign). It is a Should yielding to P5 (source's values, no own re-implementation) with a measurement; no Must
   broken (weak leak). Curator must confirm and, if kept, add a Cases line to LEAK-30 naming the distinction
   ("rebuild needs an external frozen reference and the measured effect is nil"), else coad/sarcoma read as unlike.
   Reflection prompt below (issue R1).

2. LEAK-17 / USE-11, first array per patient: CONSISTENT. Precedent breast_cancer_prediction (USE-11 Cases,
   2026-10-15, Lennart: each woman's earliest exam, IID without grouping). Same facts: one prediction per specimen,
   later arrays are re-hybridisations. corporate_credit_rating (USE-11) shows grouping all rows is the alternative
   when the use case covers repeat events; here it does not. Option (c) last array has no precedent; fine as listed.

3. SPLIT-1/SPLIT-19, IID over patients instead of AEGIS-1 -> AEGIS-2: CONSISTENT with the regime-follows-the-
   application tension (principles.md, forest_fires; "split follows what the task does in reality") and the
   few-groups factor. The batch brief's cohort suggestion is not a curator decision, so no departure. The stated
   facts (source's training set not in the deposit; overlapping trial periods; 2 groups) are the reasons. OK.

4. PROV-4 / PROV-6, both siblings: CONSISTENT with freddie_mac_single_family_default (2026-11-08, Lennart: keep,
   other source with disjoint rows) and numerai28_6 (2026-10-22: not a duplicate, different release/features).
   Disjoint patients, other array platform, other cohort -> not a duplicate; unlike nfip/food_stamps/hiva (same
   rows). Retiring the smaller as "superseded" would be a new kind of decision (no precedent retires a disjoint
   cohort); if offered, flag it as such. Recommendation (keep both) follows precedent.

5. MET-5 metric source(roc_auc) vs sibling's fallback(roc_auc): CONSISTENT, a fact sets it apart: Whitney 2015 select
   by CV AUC (stated), Spira 2007 reported accuracy/sens/spec. Same scorer either way. Record's "fallback" line should
   be updated to match.

6. PROV-8/9 source "GOV Website" vs record "Other": definition follows the sibling (GEO, GOV Website, Public Domain);
   CONSISTENT; fix the record field (no decision needed).

7. Dropping 557 identical clusters (CLEAN-22, dataset_duplicate_columns): consistent with the house check; no
   precedent against.

Drift: none found (no curator decided the same rule two ways on the same facts in this set).
Third exception of a kind: no; but item 1 is the first "raw exists, kept" under LEAK-30, so record it as a case.

--- Issue R1 (draft for REVIEW.md) ---
Keep the per-cohort RMA values as published although the CEL files would allow a rebuild?

**Problem:**
- LEAK-30 says rebuild from the unprocessed values when the source has them; every earlier case with raw values
  available was rebuilt (coad_colon_adenocarcinoma, sarcoma methylation, sf_permit_time, home_credit).
- The only RMA case kept (lung_cancer_epithelial_genexp) was kept because it had no CEL files; this one has 680.
- A per-sample rebuild needs fRMA's frozen reference vectors (R) re-implemented in numpy over 2.8 GB of CEL files; the
  measured leak is nil (ROC AUC -0.0006 LR, +0.0018 LightGBM, no consistent sign).

| Option | Pro | Con |
|---|---|---|
| (a) Keep, recorded as an exception: a rebuild that needs an external frozen reference, with a measured nil effect, is not required | the source's own values; no own re-implementation of an R method; effect measured | first case kept with raw available; needs a Cases line so coad/sarcoma stay distinguishable |
| (b) Rebuild with fRMA per sample | follows LEAK-30's rebuild clause literally | R-derived vectors, our numpy port to verify, new raw files; no measurable gain |
| (c) Ship our numpy RMA per cohort | none over (a) | same leak, our code in place of the source's |

**Recommendation:** (a), with the distinguishing fact written into LEAK-30's Cases.

[^1]: LEAK-30, PROV-13, P4 against P5 (principles.md, Tensions; Exceptions and amendments).
```

</details>

<details><summary>Advocate: aegis_bronchial_airway_lung_cancer</summary>

```text
Advocate, aegis_bronchial_airway_lung_cancer (2026-11-09). Ship as defined, with changes that need no decision.

1. No leak, no copies, nothing to game (P4, LEAK-10/16..21, Must). Task gamer: no exploit; honest LR 0.731. Split auditor: random 0.728, grouped by scan day 0.734, scan month 0.705, forward in time 0.782; exact copies 0.0% over 60 splits; 1-NN 0.643 vs chance 0.637. Every validity Must holds; what remains is weak Shoulds and notes.
2. Real, scoped, worth benchmarking (P2/P6, SEL-2, SEL-16, TP-1..5). Sponsor's GEO deposit, sex matches chrY 680/680; linear 0.750 vs dummy 0.500 on 30/30 splits, family spread +0.236 (SE 0.015), >=50 benign per test fold. p>>n with 639 rows is a regime the benchmark lacks, not a flaw (blind reviewer: include).
3. LEAK-30 exception is the mildest remedy (Should, weak). Measured nil: ROC AUC -0.0006 LR, +0.0018 LightGBM, no sign. Rebuild needs fRMA frozen vectors ported from R (P5: source's values over our re-implementation). Precedent checker: departs with a stated reason, no Must broken; keep (a) plus a Cases line in LEAK-30. Rebuilding for zero measured gain is above the mildest rung of the remedy ladder.
4. Split and replicates are right and precedented (SPLIT-1, SPLIT-19, USE-11). First array per patient matches breast_cancer_prediction; IID over two concurrent cohorts follows the few-groups factor; cohort transfer costs little (0.769 vs 0.799). Split, column, domain and precedent agents all agree; a cohort variant is optional, not a block.
5. Fit objection answered by a reword, not a downgrade (USE-9 over USE-8). Domain practitioner prefers "triage at bronchoscopy, before its result" plus a sentence on the nondiagnostic use; the data match that decision exactly (brushing before result, target within 12 months). Missing age/pack-years: named in known (a gap, not a leak); clinical covariates from GEO only if confirmed known before the procedure.
6. Control clusters: real but weak, fix by mildest remedy (LEAK-13/15, weak). affx spike-ins alone 0.621 = scan day alone 0.62, yet models within scan day are no worse than pooled (0.768 vs 0.748). Drop the 57 affx + 45 bgp clusters by pd.hugene type (documented non-patient drop, CLEAN-22) or extend the note; either keeps the dataset. Note the 227 untyped clusters and the untestable 28 centres in the README.
7. Metric and record fields are bookkeeping (MET-5, PROV-8/9). roc_auc is the source's selection criterion (Whitney 2015), the practitioner keeps it; set record Metric to source and original_source to GOV Website. Both siblings in: disjoint patients and platform (PROV-4, freddie_mac precedent).
```

</details>

<details><summary>Critic: aegis_bronchial_airway_lung_cancer</summary>

```text
Critic, aegis_bronchial_airway_lung_cancer (2026-11-09). Opening brief: ship only with changes. No point asks for exclusion.

1. Fit stated "direct" for a population the use case excludes (USE-8 Must; remedy USE-9 Should).
   Problem: use_case says the classifier is used "when bronchoscopy ... does not give a diagnosis", but the rows are
   all 639 bronchoscopy patients, including those the bronchoscopy already diagnosed (76% cancer overall; the test's
   population is the nondiagnostic, intermediate-risk subgroup). The bronchoscopy result is not released, so the
   subgroup cannot be cut. Effect: the benchmark scores a different, likely easier and more cancer-heavy population
   than the decision it names. Evidence: dataset.py lines 26-29 and 48; domain practitioner gap (a).
   Remedy: reword use_case to triage at bronchoscopy, before its result (USE-9), with a sentence that the commercial
   use is the nondiagnostic subgroup; otherwise set fit approximate with that reason. Definition fix, no exclusion.

2. Lab spike-in control clusters ship as patient features and carry scan batch (LEAK-13/LEAK-15 Must; CLEAN-22 Must).
   Problem: 57 control->affx clusters (bacterial/poly-A/ERCC spike-ins added in the lab) measure the processing run,
   not the patient; alone they score ROC AUC 0.621, equal to scan day alone (0.62), on a batch whose benign share runs
   6%-65% by scan day. Effect: a recording artefact correlated with the label sits among the features. Its gain over
   biology is not shown (models within scan day >= pooled, 0.768 vs 0.748), so this is weak, which is why I do not ask
   for LEAK-15's retire. Evidence: column auditor a.py; builder batch_label.json.
   Remedy: drop the 57 affx (and the 45 bgp background, AUC 0.49, no patient content) clusters by pd.hugene type as
   documented non-patient columns (CLEAN-22), one bullet in the notes. Repair, cheap.

3. LEAK-30 departure needs the curator's word and a Cases line (LEAK-30 Should when weak).
   First case kept with the raw files available; every earlier one (coad, sarcoma) was rebuilt (precedent checker).
   The nil effect rests on one measurement by the builder, not re-run (claim auditor: untested). I accept option (a)
   only as an explicit curator decision with the Cases line "rebuild needs an external frozen reference; measured
   nil", so the precedent does not silently widen.

4. Blind reviewer's "clinical covariates in GEO" is false; say so in known, not add (USE-3 / evidence).
   The series matrix has 3 characteristics only (tissue, gender, cancer_yes_no); no age, smoking or lesion size.
   No remedy beyond the existing note; I drop the blind reviewer's add-covariates request.

5. Notes (Should, quality, not reasons to hold): 227 untyped clusters (meaning unknown) and 28 untestable centres
   named in the README; record fields original_source -> GOV Website, Metric -> source (PROV-8/9, MET-5).

Not argued: split (IID right, all alternatives within 0.03), first array (USE-11 precedent), metric, both siblings.
```

</details>
