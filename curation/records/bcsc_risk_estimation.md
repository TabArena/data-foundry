---
unique_name: bcsc_risk_estimation
name: BCSC Risk Estimation Dataset
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- AI-Filled (Verify)
- New IID
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Fixed Delay'
- Clinical Study
original_source: GOV Website
year: '? (2006)'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.bcsc-research.org/index.php/datasets/rfdataset
- https://www.bcsc-research.org/index.php/datasets/rfdataset/dataset
- https://doi.org/10.1093/jnci/djj331
needs_review:
- ai_unverified
v2_path: datasets/_dev/tabarena-v0pt2/bcsc_risk_estimation/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 2,392,998 BCSC screening mammograms with the one-year breast cancer outcome and 11 risk factors, the data of Barlow et al. 2006's published risk model; a real screening task, shipped as aggregated counts of categorical factors.
- Source: Breast Cancer Surveillance Consortium (NCI-funded), "Risk Estimation Dataset" (https://www.bcsc-research.org/index.php/datasets/rfdataset), the data of Barlow et al., "Prospective breast cancer risk prediction model for women undergoing screening mammography", JNCI 98(17):1204-1214, 2006 (doi 10.1093/jnci/djj331), which users must cite; the file's own release date is not stated (a one-observation-per-woman version was added in August 2012). As published (documentation page): `risk.txt`, 280,660 records ("This reduces the dataset to 280,660 records"), one per combination of risk factors and outcome with a `count` ("The count variable (16) must be used to obtain correct estimates"); menopaus, agegrp (35-84 in 5-year bands), density (BI-RADS 1-4), race, Hispanic, bmi, agefirst, nrelbc, brstproc, lastmamm, surgmeno, hrt; targets `invasive` and `cancer` (invasive or DCIS within one year); a 75/25 `training` flag; code 9 is unknown. Exams 1996-2002, "this dataset is static". "The index mammogram's assessment is not included." Access after a registration form.
- Use case: a screening programme, at a woman's screening visit, estimates her short-term breast cancer risk from self-reported risk factors, breast density and her last mammogram result, to tailor screening and prevention ("Our risk model may be able to identify women at high risk for breast cancer", abstract); fit direct. Regime IID on the one-woman version: the cells carry no woman id, so the version with several exams per woman cannot be grouped (USE-11, as `breast_cancer_prediction`).
- Siblings and duplicates: `breast_cancer_prediction` (`Yes`; the BCSC Digital Mammography Dataset, 2014) is the same consortium but other exams and a later prediction point (at the read, with the BI-RADS assessment, kept as inputs by CC 2026-10-15); this file stops before the read, so a distinct task (PROV-7). `cbis_ddsm` (this run) is an image collection. No other record of this file (grep for bcsc, rfdataset, breast cancer surveillance). External collections: none found.
- Better data: from the run's search, a related task next to `breast_cancer_prediction`; no further search this round.
- Papers and pages: Barlow et al. 2006 (PubMed 16954473); the BCSC dataset and documentation pages (variables, SAS code for the paper's Table 3 and Table 5 models).
- Metric: the c statistic, the paper's one discrimination measure ("Concordance of the predicted with the observed outcomes was assessed by a concordance (c) statistic", abstract; 0.631 premenopausal, 0.624 postmenopausal), so `roc_auc`, which is also the fallback (MET-5, MET-8); inputs: `count`, used to expand the cells into exams (MET-2).
- Risks for /add-dataset: expand by `count` (2.39M exams, 11,638 cancers per the abstract, about 0.5%) and cap the rows; take the one-woman version; `cancer` (the paper's outcome) against `invasive` (USE-5); drop `training`, a prescribed random split (SPLIT-5); density is the radiologist's reading of the index exam, an input under SEL-14 like the readings of `breast_cancer_prediction`; code 9 as missing, not a level (CLEAN); exams of 1996-2002 under an older BI-RADS density definition, which the documentation flags (`Outdated` to weigh).
- Priority: gap 0 (medical and binary classification are not thin), use case + (the paper names the screening decision), source + (a consortium page, a codebook, a JNCI paper), shape 0 (millions of exams, but 11 low-cardinality categorical factors in aggregated cells), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through a related task next to `breast_cancer_prediction`.
- as published: 2,392,998 screening mammograms (1996-2002) aggregated into 280,660 records, one per combination of risk factors and outcome with a count; two versions (multiple exams per woman, one per woman); 12 ...; target: breast cancer diagnosed within one year of the index screening mammogram (cancer: invasive or DCIS; invasive); access: registration.
- Why: same publisher and same outcome as breast_cancer_prediction but a different use case: risk estimation before the read, without the index exam's BI-RADS assessment (deliberately left out of the public file); a strong source with a published model
- Adds: about 60x more screening exams for the same 1-year cancer outcome; caveats: older (1996-2002), aggregated counts (expand by count or use weights), only categorical features

CC (2026-11-27, Andrej): add it. It is the risk task before the mammogram is read, which `breast_cancer_prediction` cannot carry (there the radiologist's read is a feature; its review issue 2).

## Review

**Outcome:** added. The BCSC Risk Estimation Dataset, one exam per woman: 1,007,660 women, 7,319 cancers within a year (0.73%), twelve risk factors known at the screening visit, before the radiologist assesses the mammogram; the risk task `breast_cancer_prediction` cannot carry (its review issue 2, open). The full review panel recommends shipping after changes, all applied: the age band 75-79 restored (it had been set to missing), the fit set to approximate, a "not menopausal" level, and corrected notes.

**Main points:** Keep the forced time tag (1), mark the 1996-2002 exams `Outdated` as a note (2), and add the source page's second citation wording (3)? Values on the shipped folds, after the fixes: logistic regression ROC AUC 0.648, regularised LightGBM 0.658, untuned LightGBM 0.635, age alone 0.610; the methods beat age on 3 of 3 folds. The paper's c statistic (0.631 / 0.624) is per menopausal group; logistic regression gives 0.62-0.63 per group here, 0.649 pooled. Nothing leaks: 91.2% of the test women share their exact profile with training women, and looking up those women's outcomes adds nothing (-0.010, SE 0.004); the blind task gamer found no exploit. Density is read from this mammogram (worth 0.016 ROC AUC), which the fit names. The one-exam-per-woman file is a strict subset of the all-exams file; the all-exams file has no woman id, so random folds would put one woman's exams on both sides, and it is not used. The source's 75/25 flag scores as one random split (0.648 / 0.657) and is dropped for our folds.

**Issues for Andrej:**

1. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - The exams are from 1996-2002 and the file carries no dates, so nothing can be measured over time.
     - The use case scores women decades later.
     - Hormone therapy use, the BI-RADS density scale and the imaging that finds the cancers have all changed since.
   * **Background:** 24.8% of the women were on hormone therapy, before its use fell after the Women's Health Initiative trial[^whi]; density was redefined in the BI-RADS editions of 2003 and 2013; digital mammography and tomosynthesis replaced film. No dated BCSC file has the outcome (the Risk Factors summary of 2005-2017 has none).
   * **For a stationary use case:**
     - the BCSC's current risk models use the same factors.
     - a fixed one-year label window.
   * **Against:**
     - hormone therapy use and the density scale changed after 2002.
     - the imaging that detects the label's cancers changed.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning | Claims only what is known; as `breast_cancer_prediction` and `hepatitis_survival_prediction` | The split stands for later women only as far as the relation holds |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later women | Three known changes after 2002 argue against it |

   * **Recommendation:** A, a known mechanism of change and nothing to measure. Confidence: high (the whole panel). **Decision:** A or B?

   [^whi]: Rossouw JE, Anderson GL, Prentice RL, LaCroix AZ, Kooperberg C, Stefanick ML, Jackson RD, Beresford SA, Howard BV, Johnson KC, Kotchen JM, Ockene J; Writing Group for the Women's Health Initiative Investigators. Risks and benefits of estrogen plus progestin in healthy postmenopausal women: principal results from the Women's Health Initiative randomized controlled trial. JAMA. 2002;288(3):321-333. doi:10.1001/jama.288.3.321. SPLIT-32: the review reasons whether the use case can be taken as stationary; `AssumedStationaryRelation` is set by a person only.

2. **Ship with `Outdated` as a note, or with no marker?**

   * **Problem:**
     - The exams are 24 to 30 years old and the source says the data are static.
     - You kept two old medical cohorts with `Outdated` as a note, for the same kind of change of era.
     - No fact found sets this case apart from them.
   * **Background:** `cirrhosis_patient_survival_prediction` (CC 2026-10-15, 2026-11-05) and `hepatitis_survival_prediction` (CC 2026-11-10, also time lost and forced) ship with the marker; a marker does not leave a dataset out on its own[^sel18], so not adding the dataset for its age alone is not an option.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No marker (implemented) | Ships as is | The task is how the field still estimates this risk | Departs from the two precedents with no fact that sets it apart |
     | B | `Outdated` as a note | The marker and a CC line: the risk-factor relation holds; the era's hormone therapy, density scale and imaging differ | Treats like cases alike | – |

   * **Recommendation:** B. Confidence: high (advocate and critic agree). **Decision:** A or B?

   [^sel18]: **SEL-18** (Should): `Outdated` alone does not exclude a dataset; a `No` that cites it names other reasons.

3. **Add the source page's citation wording beside the acknowledgement you asked for?**

   * **Problem:**
     - The BibTeX note carries the documentation page's acknowledgement, as you asked (NCI-funded BCSC, HHSN261201100031C).
     - The dataset's main page asks downloaders for different wording: funding by the National Cancer Institute (P01CA154292), and "Downloaded xx/xx/xxxx from the Breast Cancer Surveillance Consortium Web site - http://www.bcsc-research.org/".
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the acknowledgement only (implemented) | No change | The wording you chose | The main page's required sentence is missing |
     | B | Add the main page's sentence after it | Both grants and the download line, with our download date (2026-11-27) | Satisfies both pages | One more sentence |
     | C | Replace it with the main page's text | The main page's wording only | One wording | Drops the wording you asked for |

   * **Recommendation:** B. Confidence: medium. **Decision:** A, B or C?

**Review panel:** ship after changes (mediator). Tier full: claim, column and split auditors, domain practitioner, precedent checker, blind reviewer, task gamer, advocate and critic with one rebuttal each, mediator. Claims: 28, 23 hold, 5 refuted (all fixed: the age band, the code-9 wording, the hormone therapy share, the sibling's status, the citation wording, now issue 3). Blind review: include with changes (the age band). Task gamer: no exploit; density worth 0.016 as known signal. Agreed: the split, no leak, the metric, the file version. Settled in the debate: fit approximate, not direct.

<details><summary>Mediator</summary>

Tier: full (claim, column and split auditors, domain practitioner, precedent checker, blind reviewer, task gamer,
advocate and critic with one rebuttal each). No experiment run: no fact is disputed. Numbers are from the rerun after
the age fix (the task and leak probes and the dataset check) and the phase A reports.

## Judgment record

```text
Verdict: ship after changes.
Validity: SEL-14 holds (density is the read of this exam, the assessment withheld by the source); SEL-18 holds, `Outdated`
  as a note recommended (issue 2); USE-1 holds; USE-8 triggered, fixed: fit `approximate`, not `direct` (one-year
  in-situ-or-invasive label, mostly this screen's own detections, and this exam's density, stand in for the longer
  horizon and prior-exam density the named decisions use); USE-9 considered, no direct reading (pre-read triage had no
  moment with radiologist density known and the read not done); LEAK-10, LEAK-37, LEAK-42 hold (profile lookup -0.0097,
  SE 0.0037, 0 of 3 splits above 0); USE-10/USE-11 hold (one exam per woman); SPLIT-5 holds (source 75/25 flag tested
  first: LR 0.648, LightGBM 0.657 against our 0.649 / 0.659); SPLIT-36 holds (L-FORCED.random, `ForcedIIDFromTemporal`),
  the place to be written into `use_case`; PROV-7 holds (distinct from breast_cancer_prediction).
Value: TP-4 step 1 passes (linear 0.648 and regularised LightGBM 0.658 against age alone 0.610, on 3 of 3 folds);
  TP-2 holds (methods spread: linear 0.648, LightGBM untuned 0.635, RF 0.582; no flags); MET-5 `roc_auc` (the source's
  one c statistic), with a note that the published c is per menopause stratum and ours pooled.
Quality: CLEAN-12 triggered, fixed (age band 75-79 restored; already applied); CLEAN-12 mixed level ("not menopausal")
  to fix; relatives level "1" label to fix.
Weighed: source +, size +, use case + (the published model's data), age of data - (note, not exclusion), signal
  modest but real +.
For the curator: issue 1 (time tag, A recommended), issue 2 (`Outdated` note, B recommended), issue 3 (second
  citation wording, B recommended).
```

## Changes to make now (no decision needed)

| # | Change | Rule | Evidence |
|---|---|---|---|
| 1 | Age band 75-79 kept as a level, not missing (done; README: 10 levels, 0 missing) | CLEAN-12, CLEAN-14 | claim R1, column 1, blind 1, gamer, domain: 56,233 women, 1.154% cancers |
| 2 | `fit="approximate"`; `fit_reason` names both gaps: the one-year invasive-or-in-situ label, mostly this screen's own detections, stands in for the 5-year / lifetime invasive risk that prevention and supplemental-screening decisions use; density read from this mammogram stands in for the prior exam's density a visit-time model would take (worth +0.016 ROC AUC: 0.6531 with, 0.6375 without) | USE-8 (Must); USE-9 weighed and declined | domain practitioner; critic 2; advocate rebuttal 2 conceded |
| 3 | `use_case` names the place: the BCSC registries' screening programmes scoring their later women (keeps L-FORCED.random; no group basis) | SPLIT-36 [CLI.meets] | split auditor 2 (A, folds identical either way); both sides agree |
| 4 | `surgical_menopause` and `current_hormone_therapy`: code 9 becomes a level "not menopausal" where `menopausal_status` is premenopausal (280,205 women), missing otherwise | CLEAN-12 (mixed level split by what the data shows) | column 2, claim R2, blind 2; score-neutral (trees read it from `menopausal_status`) |
| 5 | `first_degree_relatives_with_breast_cancer` level "1" labelled "1 (or positive, number unknown)" | CLEAN-12 (codebook words) | column 5, codebook |
| 6 | Curation note: the published c (0.631 / 0.624) is per menopause stratum; per stratum our LR gives 0.62-0.63, pooled 0.649; calibration (absolute risk) matters to a clinical user and AUC does not score it | MET-5, MET-3 | claim 16; domain 5 |
| 7 | Density bullet of the notes gets its measured worth (+0.016, 0.6531 vs 0.6375) | SEL-14, LEAK-37 (known exploit, size now stated) | gamer exploit 1 |
| 8 | Review text: Background of issue 1 says 24.8% on hormone therapy (not 28.6%, the all-exams file) and that HT yes vs no scores AUC 0.510 among postmenopausal women with a known answer (the 0.567 was the premenopausal missing code); the fact the issue rests on (HT use fell after WHI 2002) stands | EV-1, EV-2, EV-6 | claim R3 |
| 9 | Review text: issue 2 must not call `breast_cancer_prediction` retired (its issue 2 is open) | open items stay open | claim R4 |
| 10 | Review text: main points quote the rerun (linear 0.648, LightGBM untuned 0.635, RF 0.582, age alone 0.610; regularised LightGBM 0.658; profile lookup -0.0097, SE 0.0037; 91.2% of test women share a training profile) and say the paper's c is per stratum | EV-1 | the task and leak probes, the advocate's table |
| 11 | Issue 3 of the draft (file version) leaves the issue list and becomes a note: the all-exams file cannot be grouped (no woman id), so option B breaks a Must (USE-10, SPLIT-24: one woman on both sides); the one-exam file is a strict subset of it with the paper's flag carried over (0 cells exceed); the selection rule is undocumented and fits one random exam per woman | USE-10, USE-11, SPLIT-24 | split auditor, claim 6, precedent (breast_cancer_prediction, USE-11) |

## Issues for the curator (ranked)

### 1. Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`? (P4, SPLIT-32; tag set by a person only)

- Problem: exams of 1996-2002, no dates; the use case scores women today.
- Against stationarity: HT use fell after WHI 2002 (24.8% of these women on HT; today a small minority); BI-RADS density
  redefined (4th edition 2003, 5th 2013); film replaced by digital and tomosynthesis (changes what the label detects).
- For: the BCSC's current risk models use the same factors; a fixed one-year label window.
- Nothing can be measured: no dated parent with the outcome (Risk Factors 2005-2017 has none).
- Options: A keep forced (implemented); B `AssumedStationaryRelation` with your reason.
- Recommendation: A, high. All panel members agree; precedent breast_cancer_prediction issue 1 and
  hepatitis_survival_prediction (Andrej, 2026-11-18).

### 2. Ship with `Outdated` as a note, or with no marker? (P2, SEL-18 Should; like cases alike)

- Problem: the draft recommended no marker because "age matters for a deployed model, not for comparing methods"; the
  same reason held for cirrhosis_patient_survival_prediction (CC 2026-10-15, 2026-11-05) and
  hepatitis_survival_prediction (CC 2026-11-10), where you kept `Outdated` as a note.
- Options: A ship, no marker; B ship with `Outdated` as a note, CC line in the cirrhosis style (the risk-factor relation
  holds; the era's HT use, density scale and imaging differ). Option C (do not add for `Outdated`) is not open: SEL-18
  needs other reasons for a `No`, and no panel member found one.
- Recommendation: B, high (advocate and critic agree; precedent). A needs a fact that sets this case apart; none found
  (framingham ships without the marker but no CC line argues it).

### 3. Add the rfdataset page's citation wording beside the acknowledgement you asked for? (P5, PROV citation terms)

- Facts: the BibTeX note carries the documentation page's acknowledgement (NCI-funded BCSC, HHSN261201100031C,
  bcsc-research.org), as you asked. The rfdataset main page asks users for different wording: funded by the NCI
  (P01CA154292), plus "Downloaded xx/xx/xxxx from the Breast Cancer Surveillance Consortium Web site". The claim
  auditor's R5 is not a fault in what is there: both texts are the source's.
- Options: A keep only the acknowledgement (implemented); B add the main page's sentence after it in the note (both
  grants, the download line with our download date); C replace it with the main page's text.
- Recommendation: B, medium: the main page states the required citation for downloaders, and carrying both satisfies
  both pages at the cost of one sentence. Decision: A, B or C?

## Disputed points

None left. The one dispute after the briefs (fit `direct` via a pre-read triage use case, USE-9, against `approximate`,
USE-8) was conceded by the advocate in rebuttal: in 1996-2002 the radiologist recorded density in the same read as the
assessment, so no actor acted with density known and the read not done; today's triage takes density from software,
and Ho et al. 2023 predicts recall, not one-year cancer. Under USE-9 that is a use case rephrased to excuse a gap.
Settled as change 2.

## Task-gamer exploits mapped

| Exploit | Gain | Rule | Definition's notes / warnings | New or known |
|---|---|---|---|---|
| Density from the index mammogram | +0.015 to +0.017 ROC AUC (0.6531 vs 0.6375) | SEL-14, LEAK-37 (known at the moment after the density read, before the assessment); USE-8 fit gap | curation bullet "Density is the radiologist's reading of this mammogram ... the BCSC risk calculator takes it as an input"; no size stated; not a `Potential leak, kept on purpose:` (no leak) | known; add the size (change 7) and name it in `fit_reason` (change 2) |
| Missing flags of non-structural columns | +0.012 over age alone; nothing over the full model (count of missings +0.0025, inside noise) | LEAK-37; LEAK-10's outcome-missingness clause checked, not met | curation bullet "unknown density or last mammogram result: 1.2-1.4 times higher cancer share ... fixed at the visit" | known; size consistent |
| Structural missing pattern (menopause → HT, surgical menopause) | 0.603 alone, ≈ age (0.610) | CLEAN-12 mixed level | curation bullet on code 9 "unknown or not menopausal" | known; fixed by change 4 |
| Exact-cell copies across the split, loose key, rare cells | -0.0018 to +0.0005 | LEAK-42 (link by profile; label does not travel) | accepted warning `dataset_duplicate_rows` | known; matches (no gain) |
| Cell count over train+test | -0.004 | LEAK-30 (transductive) | none needed | new, no gain; no note |
| Row order | none (rates 0.0069-0.0079 by decile) | ORDER step of SPLIT-36; time probe's `order_drift` is the source sort by feature codes | split auditor's walk | known; no effect under random folds |
| 75-79 coded missing | no score effect (LightGBM 0.6551 → 0.6557) | CLEAN-12 | fixed | fixed (change 1) |
| Untuned LightGBM overfits sparse cells | model choice, not task | — | — | not an exploit |

## Agreed facts

- 1,007,660 women (one exam each, `risk_rand.txt`), 7,319 cancers (0.73%), 181,903 cells; risk.txt 2,392,998 exams,
  11,638 cancers (0.49%), no woman id; `invasive` is a subset of `cancer` (0 exceptions).
- The one-exam file is a subset of the all-exams file with the 75/25 `training` flag carried over (0 cells exceed);
  the flag is balanced and scores as one random split.
- Age group 9 is 75-79 (56,233 women, 1.154%); fixed, README shows 10 levels, 0 missing; fix changes no score.
- Density is read from the index exam; the assessment is withheld; invasive share among cancers 80.4% vs 80.6% with
  density known vs unknown; density worth +0.016.
- Code 9 in HT and surgical menopause holds all 280,205 premenopausal women.
- Rerun: 0 errors, linear 0.648, LightGBM untuned 0.635, RF 0.582, age alone 0.610, no flags; smallest test class
  1,444; regularised LightGBM 0.658 leads LR on 3 of 3 folds; both beat age by 0.037-0.053.
- No leak: profile lookup -0.0097 (SE 0.0037); 1-NN agreement at chance; gamer found no exploit.
- Paper c 0.631 / 0.624 per stratum; our per-stratum LR 0.62-0.63, pooled 0.649.
- HT on 24.8% of women in this file; HT yes vs no AUC 0.510 among postmenopausal women with a known answer.
- No newer open BCSC file with the one-year outcome; the licence page names no licence and no teaching-only clause.
- `breast_cancer_prediction` is `Yes`; its retirement issue is open.

## Consistency

Followed:
- Forced time tag: breast_cancer_prediction issue 1, hepatitis_survival_prediction (Andrej, 2026-11-18); framingham's
  `AssumedStationaryRelation` set apart (its stationarity was measured on dated exams; here nothing is dated and a
  mechanism is known).
- `Outdated` as a note (issue 2 B): cirrhosis_patient_survival_prediction, hepatitis_survival_prediction; SEL-18.
- One row per woman, IID: USE-11 case breast_cancer_prediction (Lennart, 2026-10-15).
- Source split tested first and dropped as a prescribed random split: SPLIT-5; fosp_cancer_registry_survival.
- Coarse duplicates accepted: sepsis_survival_minimal_clinical_records' acceptance; set apart from its later `Trivial`
  retirement by the gap over age (+0.04 to +0.05 here against +0.0024 there).
- Registration-gated BCSC data shipped: breast_cancer_prediction (same consortium).
- Fit approximate for a label horizon that stands in for the decision's: USE-8 cases (alfa_battle_2_0_task_2,
  differentiated_thyroid_cancer_recurrence).

Departures: none. New ground: the first definition that expands aggregated cells by a count (MET-2 met; `count` is not
a feature); a Cases row may be added once shipped.

</details>

<details><summary>Claim audit</summary>

## Claims (refuted first)

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| R1 | "9 means unknown in every coded column" / "Unknown (code 9) becomes missing in every coded column" | dataset.py `UNKNOWN` comment, curation_comments, task_summary.changes | Codebook codes per column; raw `agegrp` tally; built frame | **Refuted (Must, a bug)** | `agegrp` has codes 1-10 and **9 = 75-79** (`CODE_LABELS` says so itself). `_clean` replaces 9 in all coded columns, so all **56,233 women aged 75-79 (5.6%) become missing age**; built `age_group` has 9 levels, no "75-79", and exactly 56,233 missing. The row claim "women aged 35 to 84" is then false in the shipped data. Score effect nil (LR 0.6489 both; LightGBM 0.6551 → 0.6557 with the band restored), because NaN is the band's only source, but the column's meaning and ordinal scale are wrong | CLEAN-12, CLEAN-14 |
| R2 | Code 9 is "unknown" in `current_hormone_therapy` and `surgical_menopause` | same | Codebook; raw cross-tab with `menopaus` | **Refuted (wording/semantics)** | Codebook: hrt and surgmeno "9 = unknown or not menopausal (menopaus=0 or menopaus=9)". All 280,205 premenopausal women carry 9 in both (100%); of hrt's 465,837 missing, 280,205 are "not applicable", not unknown. Model can recover it from `menopausal_status`, so a documentation issue, not a leak | CLEAN (missing vs not-applicable) |
| R3 | "28.6% of the exams are of women on hormone therapy; it is the third strongest single feature (ROC AUC 0.567 alone)" | Review issue 1, Background | Tally on risk_rand.txt; OOF single-feature AUC; HT yes/no AUC among postmenopausal women with known HT | **Refuted** | 28.56% is the all-exams file (risk.txt); the shipped file has **24.8%** (39.2% of postmenopausal, 46.2% of known). The 0.567 (my OOF 0.557) is the menopause signal through the structural missing code (missing-indicator alone 0.565 in the leak probe); HT yes vs no among 541,823 postmenopausal women with known HT: **AUC 0.510**. The fact the issue rests on (HT use changed after WHI) still holds; the in-data strength claim does not | EV-6 |
| R4 | "with `breast_cancer_prediction` retired, the screening question altogether" | Review issue 2, option C Con | Read breast_cancer_prediction record | **Refuted (premature)** | That record is `DF: Yes`; its issue 2 (retire, recommendation A) is open, no Resolved line (CC 2026-11-27 only states the problem) | Open items stay open |
| R5 | BibTeX note "funded by ... HHSN261201100031C" as the required citation | dataset.py `bibtex` note | rfdataset page, required citation text | **Refuted (minor)** | The page's required text: "are funded by the National Cancer Institute (P01CA154292)" plus "Downloaded xx/xx/xxxx from the Breast Cancer Surveillance Consortium Web site"; the grant in the note is not the one the page asks for | PROV (licence/citation) |
| 1 | 1,007,660 women, 7,319 cancers (0.73%); 181,903 cells | task_summary, curation, decision | Raw tally | Holds | 181,903 cells, 1,007,660, 7,319 (0.0073) | – |
| 2 | risk.txt: 280,660 cells, 2,392,998 exams, 11,638 cancers (0.49%) | curation, download_description | Raw tally; abstract | Holds | 280,660 / 2,392,998 / 11,638 (0.0049); abstract same | – |
| 3 | `invasive` is part of `cancer` | task_summary.changes, curation | invasive=1 & cancer=0 | Holds | 0 exams (5,894 invasive of 7,319) | USE-5 |
| 4 | `training` is a 75% random sample; 75.0% in this file | curation | Weighted share; cell-level subset test | Holds | 75.01% (rand), 75.02% (all); every risk_rand cell (incl. `training`) has count ≤ its risk.txt cell, 0 excess: consistent with a subset of risk.txt exams with the flag inherited | SPLIT-5 |
| 5 | risk_rand added August 2012; "All population and other characteristics remain the same" | curation | rfdataset page | Holds | Both quoted on the page | – |
| 6 | One exam per woman; selection rule undocumented; higher cancer share because women with cancer leave follow-up | curation, issue 3 | Kept fraction rand/all by stratum | Holds as stated (undocumented; explanation consistent, not proven) | Kept fraction 0.629 for cancer exams vs 0.420 others; higher for younger age groups (0.64 at 35-39 vs 0.37 at 60-74) and for lastmamm unknown (0.585): the pattern of one exam drawn per woman with fewer exams per woman for the young, new and diagnosed. A selection that favours cancer exams would look the same; no id to tell them apart | – |
| 7 | The all-exams file has no woman id | curation, issue 3 | Codebook column list | Holds | 16 columns, none an id; codebook: "do not include any dates, origin of the data, patient identifiers" | SPLIT (grouping) |
| 8 | Index mammogram's read not included; prior mammogram in 5 years; ages 35-84; 1996-2002; "static" | task_summary, curation | Codebook | Holds | All quoted on the codebook page (except the 75-79 band, see R1) | – |
| 9 | Density 9 also covers "different measurement system" | curation | Codebook | Holds | "9 = Unknown or different measurement system" | – |
| 10 | Pure-value warning: premenopausal, ages 35-44, fatty breasts, Native American 99.6-99.7% no cancer | accepted warning | Raw tally | Holds | 99.56%, 99.71%/99.67%, 99.68%, 99.62% | – |
| 11 | Duplicate rows are independent women; a copy in train tells nothing beyond the profile | accepted warning, curation | Leak probe 23 (lookup of training outcome of the same profile) | Holds | 91.2% of test rows share a profile; lookup gain -0.008 (SE 0.0047, above 0 on 0/3 splits) | LEAK |
| 12 | Paper's c statistic 0.631 / 0.624 (fit_reason "0.62-0.63") | task_summary.fit_reason, metric | Abstract | Holds | 0.631 (pre), 0.624 (post) | MET-3 |
| 13 | On the paper's 75/25 split LR reproduces 0.628 / 0.626 | Review, main points | Weighted LR per menopause stratum on risk.txt, training flag, validation c | Holds (approximately) | My LR with all available factors per stratum: 0.621 (pre), 0.625 (post); same order as published. Not the paper's exact spec; the review's 0.628 is plausible, not reproduced exactly | EV-1 |
| 14 | Our 3 folds: LR 0.650, LightGBM 0.656 | Review, main points | One-hot LR and LightGBM (300 trees) on the shipped folds | Holds | LR 0.6489 (0.648/0.646/0.653), LightGBM 0.6551 | – |
| 15 | Untuned probes LR 0.646, LightGBM 0.634, RF 0.578, best single feature age 0.611 | Review | the task probes; my OOF single feature | Holds | Log matches; my age-alone 0.610 (leak probe's 0.622 is another method) | – |
| 16 | Metric `roc_auc` = the source's c statistic | dataset.py metric | Abstract; dummy scored per fold; positives per fold | Holds, with a nuance | c statistic of a binary logistic model = ROC AUC. The paper reports it **per menopause stratum** (separate models); ours is pooled, which adds the between-strata separation (my per-stratum 0.62-0.63 vs pooled 0.649), so the published numbers are not directly the benchmark's scale. Computable: dummy 0.5 on every fold; 2,439-2,440 positives per test fold | MET-2, MET-3 |
| 17 | Split: random folds, every row a different woman | task_summary.split | Subset test + source statement | Holds (as far as the source documents) | No ids; source says one observation per woman | SPLIT |
| 18 | Size: 671,773 train / 335,887 test, under 1M / 500k | curation | README splits table | Holds | 671,773-671,774 / 335,886-335,887 | – |
| 19 | Time basis ForcedIIDFromTemporal: 1996-2002, no dates | time_basis | Codebook | Holds | "do not include any dates" | SPLIT-32 |
| 20 | BI-RADS density categories redefined in 2013 | Review issue 1 | Knowledge + codebook | Holds, incomplete | The 5th edition (2013) changed density to a-d descriptors; the codebook (2006) already warns of "a recent change in the BI-RADS breast density definition", i.e. the 4th edition (2003), which falls inside or right after the collection period | – |
| 21 | No newer BCSC file has the one-year outcome; Risk Factors summary 2005-2017 | Review issue 2 | BCSC Risk Factors page | Holds (as far as checked) | Risk Factors Dataset: 6,788,436 mammograms 2005-2017, risk factors incl. "history of breast cancer", no outcome named; a "Hormone Therapy and Breast Cancer Incidence Data" set exists (aggregate incidence; not checked in depth) | – |
| 22 | Licence: registration, citation required, no licence named, no teaching-only clause | Source.license | rfdataset page | Holds | Page has no licence, no teaching or commercial restriction | PROV |
| 23 | Implicit: every feature known at the screening visit | implied | Codebook | Holds | Density is the reading of the index mammogram (codebook "density" of the index exam); known at the read, before the assessment; the screening block already flags this (SEL-14). Not the assessment | SEL-14 |

## Refuted and untested, ranked

1. **R1, age band 75-79 set to missing (Must, data correctness).** Changes: the shipped `age_group` drops a level and shows 5.6% of women as of unknown age; row and known claims false. Remedy: exclude `age_group` from the 9 → missing replacement (agegrp has no unknown code), rerun `dataset check`. Score unchanged.
2. **R3, HT evidence in issue 1.** Changes: the Background line; HT's in-data strength among postmenopausal women is AUC 0.51 and the 28.6% is the other file (24.8% here). Remedy: restate the background (24.8%; the 0.567 is the premenopausal missing code); the recommendation still rests on the WHI fact.
3. **R2, "not menopausal" coded as missing.** Remedy (mildest): fix the comment and curation bullet to say 9 in hrt/surgmeno also means "not menopausal". Optional: a "not menopausal" level, but CLEAN minimal preprocessing allows leaving it, since `menopausal_status` carries it.
4. **R4, issue 2 option C states `breast_cancer_prediction` as retired.** Remedy: "if `breast_cancer_prediction` is retired (its issue 2)".
5. **R5, BibTeX note grant number.** Remedy: use the page's required text (P01CA154292, downloaded date, web site).
6. Nuance on 16 (pooled vs per-stratum c statistic): say in the metric definition or review that the published 0.631/0.624 are per stratum, so the pooled AUC (about 0.65) is not directly comparable.

Untested: the exact selection rule of risk_rand.txt (no id; not documented); the review's exact 0.628/0.626 spec (mine 0.621/0.625 with a different factor set).

</details>

<details><summary>Column audit</summary>

Inputs: `dataset.py`, generated README (check of the current definition), record, raw `risk_rand.txt` (181,903 cells,
1,007,660 women), BCSC codebook page (rfdataset/dataset), dtype probe (4 of 12 flagged). Tallies are weighted by
`count`. No model fits run (none needed for these findings).

## Files

| File of the release | Read by `_load_raw` | Reason given |
|---|---|---|
| `risk_rand.txt` (risk_dataset_v2.zip), one exam per woman | yes | the file used |
| `risk.txt` (risk_dataset.zip), all exams | no | no woman id in the cells; random folds would put one woman's exams on both sides (curation notes) |

No file left out without a reason.

## Columns

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `age_group` | agegrp 1-10 = 35-39 ... 80-84; **no code for unknown** | yes | ordinal, 10 levels declared; **code 9 = 75-79 is replaced by missing** by the blanket `replace(UNKNOWN, nan)`: 56,233 women (5.58%) lose their age, the level 75-79 never occurs (README: 9 unique, 5.58% missing) | **cleaning bug** | CLEAN-10/CLEAN-12 (a real level turned into missing) |
| `menopausal_status` | 0 premenopausal; 1 postmenopausal **or age >= 55**; 9 unknown | yes, self-report at intake | categorical, words; 9 -> missing (88,739, all aged 35-54) | fine; the label keeps the codebook's "or age 55 or older" | CLEAN-12 |
| `birads_breast_density` | BI-RADS 1-4, read by the radiologist **from the index mammogram**; 9 = unknown or different measurement system | produced at the read of this exam (not before it); not the assessment | ordinal fatty < scattered < heterogeneous < extremely dense, correct order; 9 -> missing (27.4%) correct for a state off the scale | fine as a feature (SEL-14, the BCSC risk model's own input); **wording of the prediction point is wrong** (see problem 3) | USE-3, SEL-14 |
| `race` | 1 white, 2 Asian/PI, 3 black, 4 Native American, 5 other/mixed, 9 unknown | yes | categorical nominal, words; 9 -> missing | fine | CLEAN-12 |
| `hispanic` | 0 no, 1 yes, 9 unknown | yes | categorical flag; 9 -> missing | fine | CLEAN-14 |
| `bmi_group` | 1 10-24.99 ... 4 35 or more, 9 unknown | yes | ordinal, open top end as own level (probe `open_end` answered); 9 -> missing (56.2%) | fine | CLEAN-14 |
| `age_at_first_birth` | 0 <30, 1 >=30, 2 nulliparous, 9 unknown | yes | categorical (probe says `ordinal_like`): nulliparous is a state off the age scale, so unordered is right | fine | CLEAN-14 (state that is a second dimension) |
| `first_degree_relatives_with_breast_cancer` | 0, 1, 2 or more, 9 unknown; codebook: **a positive family history with unknown count is coded 1** | yes | ordinal 0 < 1 < 2 or more, open end correct; label "1" also holds "at least one, number unknown" | fine; label could say so (minor) | CLEAN-12 |
| `prior_breast_procedure` | "Previous breast procedure" 0/1, 9 unknown; self-reported at the index exam | yes | categorical flag | fine | CLEAN-14 |
| `last_mammogram_result` | result of the last mammogram before the index: 0 negative, 1 false positive, 9 unknown | yes (earlier exam) | categorical flag; 9 -> missing (32.4%) | fine; missing is informative (see problem 4) | CLEAN-10 |
| `surgical_menopause` | 0 natural, 1 surgical; **9 = unknown or not menopausal** | yes | categorical; 9 -> missing (56.3%) mixes 280,205 premenopausal (not applicable), 88,739 menopause-unknown, 198,790 postmenopausal-unknown | question: not-applicable level (problem 2) | CLEAN-12 (mixed level), CLEAN-14 |
| `current_hormone_therapy` | 0 no, 1 yes; **9 = unknown or not menopausal** | yes (note: falls after 2002, record issue 1) | categorical; 9 -> missing (46.2%) mixes 280,205 premenopausal, 88,739 menopause-unknown, 96,893 postmenopausal-unknown | question: not-applicable level (problem 2) | CLEAN-12, CLEAN-14 |
| `cancer_within_one_year` (target) | invasive or DCIS within one year of the index mammogram | label | No/Yes, Yes = event | fine | CLEAN-25 |
| `invasive` (dropped) | invasive cancer within one year: part of the target | - | dropped | right | LEAK-10 |
| `training` (dropped) | the paper's 75% development flag | - | dropped | right | SPLIT-5 |
| `count` (consumed) | cell frequency | - | rows repeated by it | right | MET-2 |

## Problems, ranked

1. **`age_group` 75-79 set to missing (cleaning bug, Must-level effect on the data; CLEAN-10/CLEAN-12).**
   `_clean` runs `df[coded].replace(9, nan)` over every column of `CODE_LABELS`, `age_group` included, before
   `decode`. In agegrp, 9 is the band 75-79, not unknown (codebook: codes 1-10 are 35-39 ... 80-84; the raw file has
   no unknown age). Raw: agegrp 9 = 56,233 women; the frame: `age_group` 5.58% missing = 56,233, 9 distinct levels,
   no 75-79. These are the highest-risk women (cancer 1.154%, the highest band; overall 0.73%), so the bug removes
   signal from the strongest single feature. Remedy: exclude `age_group` from the unknown replacement (e.g.
   `coded = [c for c in CODE_LABELS if c != "age_group"]`), re-run check; the record's numbers (age AUC 0.611, LR 0.650,
   LightGBM 0.656, the 91% profile share) were computed on the damaged frame and need re-running.

2. **`surgical_menopause` and `current_hormone_therapy`: code 9 mixes "not applicable" with "unknown" (Should,
   CLEAN-12's mixed-level clause; question for the curator).** Codebook: "9 = unknown or not menopausal (menopaus=0 or
   menopaus=9)". In the data, 9 holds every premenopausal woman (280,205), every menopause-unknown woman (88,739), and
   198,790 / 96,893 postmenopausal women with a truly unknown answer. The split is recoverable from
   `menopausal_status`, so missing loses no information (a tree reads the interaction), but CLEAN-12 asks to split such
   a level by what the data shows. Options: A keep missing (implemented; lossless via `menopausal_status`); B a level
   "not menopausal" for `menopausal_status == premenopausal`, missing for the rest (mirrors the paper, which fits these
   two only in its postmenopausal model). Recommendation: B, low stakes; confidence medium.

3. **The prediction point says density is known "before the mammogram is read"; density is read from this mammogram
   (Should, USE-3 wording).** Codebook: density is judged by the radiologist on the index mammogram; covariates other
   than density and lastmamm are self-reported. So the row is at the read, after the density call and before the
   BI-RADS assessment, which the source withholds. Not an outcome leak (SEL-14; the BCSC risk calculator takes this
   density; the invasive share among cancers is the same with and without density, 80.4% vs 80.6%), but
   `task_summary.question`, `known` and the first curation bullet should say "after the radiologist records breast
   density, before the exam's assessment". Remedy: text only.

4. **Informative missingness in `birads_breast_density` and `last_mammogram_result` (note, no change; LEAK-10's
   "missingness that encodes the outcome" checked and not met).** Within age, cancer is 1.2-1.4x higher when either is
   unknown (age 55+: both known 0.84%, density unknown 1.08%, last mammogram unknown 1.13%, both 1.35%). Both
   missings are fixed at the visit (no earlier exam in the registry, a site with another density system), not set by
   the outcome, so they are legitimate inputs (LEAK-37). Worth one line in the notes: missing is a signal here, the
   reason likely a first exam at the facility (prevalent round) and site.

5. **`first_degree_relatives_with_breast_cancer` level "1" includes "positive history, number unknown" (minor,
   CLEAN-12).** Remedy: label it "1 (or positive, number unknown)" or a note.

Not problems: dtypes (all 12 categorical/ordinal by the codebook's words; probe flags answered above), orders (density,
BMI, age, relatives all lowest first per codebook), `invasive`/`training` dropped, no temporal columns (time lost, no
period missingness to audit).

</details>

<details><summary>Split audit</summary>

**Verdict: right, with notes.** Random 3-fold on one exam per woman is the split the tree gives for a later-women use case with the time lost (L-FORCED.random), and the source's 75/25 `training` flag scores the same as our folds. Two questions for the curator: should the walk take the place step, and is `AssumedStationaryRelation` the tag? Neither changes the folds. One data bug is outside the split but touches every number: the age band 75-79 is set to missing. The column auditor found it too.

## Tree walk (SPLIT-36)

| Question | Answer, from what | 
|---|---|
| Type | Clinical study: registry screening exams with a linked one-year outcome and no date per row. The record tags it `Clinical Study`. |
| [CLI.meets] | The definition's use case is "a screening programme" scoring later women, which gives later patients. But the source is 6 BCSC registries (Carolina, Chicago, KP Washington, New Hampshire, Vermont, San Francisco; documentation footer), and the paper's model is offered for women in general. That is another place as well. See problem 2. |
| [CLI.dated] | No. The documentation says "the data do not include any dates, origin of the data, patient identifiers". |
| [ORDER.order] | No. The order is lost. Both raw files are sorted by the 12 feature codes (`is_monotonic_increasing` True), so the row order is the profile, not arrival. The time probe's `order_drift` (p 4.8e-218, size 0.004) is that sort, not time. → Forced step |
| [FORCED.test] | Nothing can be measured: no dates and no dated parent with the outcome. The BCSC Risk Factors summary for 2005-2017 has no one-year cancer outcome. |
| [FORCED.reason] | The agent answers no. A person may give `AssumedStationaryRelation` (problem 3). |
| [FORCED.risk] | The agent answers no. |
| [FORCED.groups] | No. There is one exam per woman, so no unit repeats. Periods can't be grouped because no order exists. |
| Leaf | **L-FORCED.random, `ForcedIIDFromTemporal`**. This matches `split_leaf`, the shipped regime (iid, 1 repeat x 3 folds, stratified, as SPLIT-33 sets for 1M rows) and the Time basis line. |

## Checks with numbers

- **Units across the split.** `risk_rand.txt` holds one exam per woman, by the source's statement, so no woman sits on both sides (USE-10, SPLIT-24/25 do not apply). The paper's all-exams file would put one woman on both sides with no id to group by. The record's issue 3, recommendation A, is right on split grounds.
- **Shared profiles (probe 23).** 91.2% of test women share their exact 12-feature profile with training women. Looking up those women's outcomes changes AUC by -0.008 (SE 0.005, 0 of 3 splits positive). The nearest-neighbour label agreement is 0.985 against 0.986 by chance. There is no entity leak (LEAK-42: the link is the profile, and the label does not travel with it).
- **The one-exam file is a subsample of the all-exams file with the paper's flag carried over.** For every (profile, outcome, `training`) cell, the count in `risk_rand.txt` is at most the count in `risk.txt`: 0 cells exceed it. With the flag permuted, about 36,000 cells (about 40,000 exams) exceed it in each of 3 runs. So each kept exam keeps its paper assignment. The flag is balanced: 75.01% training, cancer 0.728% (training) against 0.720% (validation), and no feature share differs by more than 0.21 percentage points. That fits a random flag. Whether the paper assigned it by woman or by exam is not documented (the documentation says only "75% random sample"; the paper's full text was not reachable). It does not matter in the one-exam file.
- **Labels in flight.** The target is a fixed one-year window after each exam, closed for every row (`Target: Fixed Delay`), and 1996-2002 is complete. No row has an open outcome.

## Alternatives run

The features are as shipped (age 75-79 missing, see problem 1). Logistic regression is one-hot. LightGBM uses 300 trees, 15 leaves and min_child 200. The test metric is ROC AUC.

| Split | LR | LightGBM | Test rows | Test cancers |
|---|---|---|---|---|
| Ours, fold 0 | 0.648 | 0.656 | 335,887 | 2,440 |
| Ours, fold 1 | 0.646 | 0.656 | 335,887 | 2,440 |
| Ours, fold 2 | 0.653 | 0.664 | 335,886 | 2,439 |
| **Ours, mean** | **0.649** | **0.659** | | |
| Source `training` flag (75/25) | 0.648 | 0.657 | 251,805 | 1,812 |
| Random 75/25, 5 draws (range) | 0.648-0.663 (mean 0.657) | 0.657-0.672 (mean 0.664) | about 251,700 | 1,726-1,850 |

The source's split falls inside the spread of random 75/25 draws, at its low end, and within 0.002 of our 3-fold mean. It is one random split of the same rows, so it adds nothing a random fold lacks, and it gives one split where SPLIT-33 asks for 3 folds. Dropping it was right (SPLIT-5: it is a prescribed random split with no other design behind it). The `changes` line and the curation comment say so. The source split was tested first, and it agrees with ours.

## Problems, ranked

1. **Not a split problem, but it moves every split number: the age band 75-79 is set to missing (CLEAN-10/CLEAN-12; column auditor issue 1).** `_clean` runs `replace(9, nan)` over every coded column, `age_group` included, and in agegrp the code 9 is 75-79. I measured 56,233 raw exams with agegrp 9 and 56,233 missing `age_group` in the frame, with no 75-79 level left. The scores above, and the record's 0.650 / 0.656 / 0.611, were computed with this bug. Mildest remedy: leave `age_group` out of the unknown replacement, then rerun the check and the probes.
2. **Leaf question for the curator: does the use case meet other places too ([CLI.meets])?** The data pools 6 registries with no registry column. A programme outside the BCSC is another place, so the walk's rule ("meets both another place and a later time → place step") would lead to [PLACE.several] = no key, then [PLACE.units] = one row per woman, then **L-PLACE.random (Random · `ForcedIIDFromGrouped`)**. No v0.2 definition reaches that leaf yet, so it goes to a human reviewer. The folds would be identical. Only the tags differ: a Group basis line beside the time basis, naming the registry the data cannot key, with the rows of each registry on both sides.
   - Option A: keep the later-women reading, with the use case as written (implemented).
   - Option B: add `ForcedIIDFromGrouped` with a group basis.
   - My recommendation is A, unless the curator reads the use case as transfer beyond the BCSC. The definition's use case does not name one. Confidence: medium.
3. **Time basis: `ForcedIIDFromTemporal` against `AssumedStationaryRelation` (SPLIT-32; the record's issue 1).** I agree with the draft's recommendation A. The facts against a stationary relation are real and named in SPLIT-32's list of reasons against: changed treatments (hormone therapy after the WHI trial in 2002, 28.6% of exams on therapy), changed coding (BI-RADS density, 5th edition 2013), and changed detection (film to digital and tomosynthesis). Only a person sets the tag. Nothing here can be measured, so the forced tag claims only what is known.
4. **Note: the Time basis line could name what a dated release would test more concretely.** It now says "would test exams later than those used for training". It could add that the BCSC Risk Factors summary (2005-2017) has no outcome, so no dated parent exists. This is wording only. SPLIT-8 asks the line to name the reason, which it does.

## What found nothing

- Recurring women: none, one exam per woman.
- Hidden groups and copies: profiles are shared by construction (aggregated cells), and the lookup gain is -0.008 (SE 0.005).
- Order or batch in the raw file: the file is sorted by profile, and no time order is recoverable.
- Source split against ours: the same score, within the random-split spread.
- Open labels: none, the one-year windows are closed.

</details>

<details><summary>Domain practitioner</summary>

Actor played: a US screening programme's breast-imaging radiologist / high-risk clinic, deciding at a woman's screening
visit about supplemental screening (MRI, ultrasound), referral for risk-reducing medication, or reading priority.

## Fit: approximate (the declared fit `direct` overstates it)

One sentence: the rows, inputs and label are those of a real published research model (Barlow et al. 2006), but no
actor makes a decision on a 1-year in-situ-or-invasive outcome with this exact information set: density is read off
the index mammogram itself while that same read's assessment is withheld, and the deployed tools (BCSC calculator,
Gail, Tyrer-Cuzick) predict 5-year, 10-year or lifetime invasive risk, not the 1-year outcome, most of which is the
index screen's own detections.

A defensible direct reading exists (USE-9): pre-read triage. The images have been taken and density is known (today
from automated density software at acquisition; then from the radiologist), the read is not yet done, and the programme
ranks exams by short-term cancer probability for reading priority, double reading or a same-day diagnostic slot (BCSC
has published exactly this kind of model for recall, Ho et al. 2023). If the dataset's use case were rewritten that
way, I would accept `direct`. As written ("tailor screening and prevention"), the target is a proxy.

## Decisive finding first: age 75-79 is wiped to missing (a cleaning bug)

`_clean` replaces code 9 by NaN in every coded column (`coded = list(CODE_LABELS)`), but in `agegrp` the code 9 is
the level 75-79 (codes 1-10, CODE_LABELS itself says so). The raw file has 56,233 women with `agegrp == 9`, exactly the
README's 56,233 missing `age_group`, and the README's category table has no 75-79 level. These are the highest-risk age
group (1.154% cancer, against 0.73% overall; tally below). An actor always knows the woman's age. Fix: exclude
`age_group` from the code-9 replacement (age has no unknown code in the codebook). The task probes (age_group the best
single feature, ordinal handling in the linear model) ran on the bugged frame and should be re-run after the fix.

## 1. Inputs at the moment of prediction

| input | do I have it at the visit? | note |
|---|---|---|
| age, menopause, surgical menopause, race, Hispanic, BMI, age at first birth, first-degree relatives, prior breast procedure, current HT | yes | self-report at the index mammogram (codebook: "based on self-report at time of the index mammogram") |
| result of last mammogram (negative / false positive) | yes | from the programme's own records, before the visit |
| BI-RADS density | only after the index images are read | codebook: "Breast density (3) is judged by the radiologist from the screening mammogram", i.e. the index exam, not the prior one. A pre-visit risk clinic would use the prior exam's density (what the BCSC calculator asks for). Density changes slowly, so as a stand-in it is close, but the information set is "after the density read, before the assessment", which is a moment only the triage reading has |
| index assessment (BI-RADS 0-5) | yes, if I am deciding after the read | deliberately withheld by the source ("nor the assessment (outcome) of the index screening mammogram"). Any post-read decision (supplemental MRI, ultrasound) is made with it in hand |

Missing that I would always have: exact age (only 5-year bands), number of prior benign biopsies and atypia
(BCSC v2, Tice 2015, uses benign breast disease), prior false positive count, genetic testing / family pedigree (for
Tyrer-Cuzick), for today also polygenic score. Missing values: density unknown 27% (code 9 also covers "different
measurement system", i.e. some sites; cancer rate 0.816% vs 0.73%), HT unknown 46% (code 9 also = "not menopausal", so
its missing indicator re-encodes menopause: fine, but users should know).

## 2. Target

- `cancer` within one year = invasive or DCIS (80.5% invasive in this file). Within one year of a screening exam most
  cancers are found by that very screen (prevalent, screen-detected), the rest are interval cancers. So the label is
  mainly "will this mammogram (and its work-up) find cancer", plus interval cancers.
- For a prevention decision (tamoxifen / raloxifene / aromatase inhibitor) I act on 5-year invasive risk (thresholds
  such as 1.67% or 3% at 5 years), for supplemental MRI on lifetime risk >= 20% (ACS, Saslow 2007), for supplemental
  imaging in dense breasts on interval-cancer risk (Kerlikowske 2015). None of these is a 1-year in-situ-or-invasive
  outcome. The BCSC itself moved on: its deployed models are 5-year invasive (Tice 2008), with benign disease
  (Tice 2015), and 5/10-year with extended factors (Gard 2024).
- For the triage reading above, the 1-year cancer (screen-detected dominated) is the right target, as a probability.
- Keeping `cancer` (not `invasive`) is the paper's choice and the right one for triage; for prevention I would want
  invasive. Dropping `invasive` as a part of the target is correct.

## 3. Row and test data

- One row = one screening exam of one woman (one drawn per woman); one decision per exam: matches.
- Population: women with a mammogram in the past 5 years but not the past 9 months, no prior breast cancer, 35-84.
  That is the returning-screening population I meet; first-time screeners are excluded (a selection the setting
  partly shares).
- Test data: random women of the same 1996-2002 cohort. What I would face is women screened today (see section 6).

## 4. Would I use this model?

Not as is, for a clinical decision. Reasons I would distrust it: (a) c statistic ~0.62-0.65 is the field's ceiling for
risk-factor models and I accept that, but I would only use it with documented calibration (observed/expected overall
and by risk decile), which a decision at an absolute threshold needs; (b) HT exposure, density scale and imaging
modality have all changed since 2002; (c) coarse bands (age, BMI) lose information I have exactly. As a benchmark of
methods on a large, honest, real risk-factor table, it is sound: features known before the outcome, label from
registry/pathology linkage, independent women.

## 5. Metric: partly

- `roc_auc` is the source's one deliberate measure (abstract: "Concordance ... was assessed by a concordance (c)
  statistic"), so MET-5 keeps it as the source metric, and it is also the MET-8 fallback. It scores ranking, which fits
  the triage use (who is read first) and risk stratification.
- It does not score what a prevention or supplemental-screening decision needs: an absolute risk compared with a fixed
  threshold. That needs calibration (Van Calster et al. 2019). In the probes the random forest has a log loss of 0.0558,
  worse than the dummy's 0.0429, while still scoring ROC AUC 0.578: a model a clinician must never use, which AUC
  does not flag as worse than no model.
- I would choose `log_loss` (strictly proper, MET-8) for the actor's decision, or keep `roc_auc` as declared (source
  metric, MET-5) and report log loss / Brier beside it. No source fixes one threshold or cost, so no threshold metric
  (MET-6, MET-7); AUPRC adds nothing here (MET-9: imbalance alone is no reason, no top-k is fixed). On the probes the
  two metrics rank the three methods the same way (linear > LightGBM > RF), so the choice does not change the current
  leaderboard; it changes what a winning model is required to be.

## 6. Does 1996-2002 stand for today's women?

| change since 2002 | effect on the task |
|---|---|
| HT use fell after WHI (Rossouw 2002); BCSC saw incidence fall with it (Kerlikowske 2007) | 24.8% of the women here are on HT (250,182 of 1,007,660); today a small minority. The HT coefficient and the case mix differ |
| film -> digital -> tomosynthesis | higher detection in dense breasts and more DCIS: the label's composition (screen-detected share, in situ share) and the density effect shift |
| BI-RADS density: 3rd/4th edition (percent-based) -> 5th edition 2013 (masking-based); large reader variation (Sprague 2016); automated density software | the density input means something slightly different now |
| screening guidance: USPSTF 2024 biennial 40-74; density notification (FDA MQSA rule, 2024) | a 1-year horizon from an annual screen is less the norm; supplemental screening decisions after density notification are now common |

So the relation is not stationary (supports keeping `ForcedIIDFromTemporal`, issue 1 A). For a methods benchmark on
one fixed relation the age is tolerable (issue 2 A or B); I would mark it `Outdated` as a concern (B) because a user
reading "screening risk model" will assume today's practice.

## Gaps ranked by how much they change the task

1. Age 75-79 set to missing (bug; changes the inputs of 5.6% of women, the oldest/highest-risk band). Fix in `_clean`.
2. Target horizon/composition: a 1-year in-situ-or-invasive outcome, mostly the index screen's own findings, against
   the 5-year/lifetime invasive risk the prevention and supplemental-screening decisions use. Changes the use case,
   not the data: rewrite the use case as pre-read triage (direct), or keep it and set `fit="approximate"`.
3. Density from the index exam, with the index assessment withheld: an information set only the pre-read triage moment
   has. Write it in `known` ("density from this mammogram's read").
4. Era (HT, technology, BI-RADS edition): known gap, already raised as issues 1-2.
5. Metric scores ranking only; calibration matters to the actor.

## What an expert would change

- Fix the age_group code-9 bug.
- `known`: "the breast density read from this mammogram, without its assessment" instead of implying density is known
  before the mammogram; the `question` "before the mammogram is read" is not literally true for density.
- Either rewrite `use_case` to pre-read triage of screening exams (rank exams by short-term cancer probability for
  reading priority / double reading) and keep `direct`, or keep "tailor screening and prevention" and set
  `fit="approximate"` with the reason: a 1-year in-situ-or-invasive outcome stands in for the 5-year invasive risk the
  decision uses.
- Metric: keep `roc_auc` (source) or move to `log_loss`; whichever, name calibration as what a clinical user would check.
- Notes: HT code 9 includes "not menopausal"; density code 9 includes other measurement systems.

## Tallies (raw `risk_rand.txt`, cells weighted by `count`)

| feature | level | women | cancer % |
|---|---|---|---|
| agegrp | 1 (35-39) | 27,391 | 0.288 |
| agegrp | 5 (55-59) | 126,934 | 0.847 |
| agegrp | 9 (75-79; set to NaN by `_clean`) | 56,233 | 1.154 |
| agegrp | 10 (80-84) | 32,061 | 1.092 |
| density | 1 fatty / 2 / 3 / 4 extremely dense | 64,160 / 324,399 / 282,601 / 60,362 | 0.318 / 0.650 / 0.799 / 0.817 |
| density | 9 unknown | 276,138 | 0.816 |
| lastmamm | negative / false positive / unknown | 665,244 / 15,619 / 326,797 | 0.670 / 1.063 / 0.825 |
| hrt | no / yes / unknown or premenopausal | 291,641 / 250,182 / 465,837 | 0.837 / 0.908 / 0.559 |
| nrelbc | 0 / 1 / 2+ | 727,625 / 114,471 / 5,565 | 0.678 / 1.014 / 1.456 |

Invasive share of the cancers: 80.5%. Probe log losses (task.json): dummy 0.0429, linear 0.0420, LightGBM 0.0426,
random forest 0.0558.

## Sources

- BCSC Risk Estimation Dataset documentation, https://www.bcsc-research.org/index.php/datasets/rfdataset/dataset
  (density "judged by the radiologist from the screening mammogram"; assessment of the index exam excluded; 1996-2002;
  inclusion criteria).
- Barlow WE, White E, Ballard-Barbash R, Vacek PM, Titus-Ernstoff L, Carney PA, et al. Prospective breast cancer risk
  prediction model for women undergoing screening mammography. J Natl Cancer Inst. 2006;98(17):1204-1214.
  doi:10.1093/jnci/djj331 (PMID 16954473).
- Tice JA, Cummings SR, Smith-Bindman R, Ichikawa L, Barlow WE, Kerlikowske K. Using clinical factors and mammographic
  breast density to estimate breast cancer risk: development and validation of a new predictive model. Ann Intern Med.
  2008;148(5):337-347. doi:10.7326/0003-4819-148-5-200803040-00004.
- Tice JA, Miglioretti DL, Li CS, Vachon CM, Gard CC, Kerlikowske K. Breast density and benign breast disease: risk
  assessment to identify women at high risk of breast cancer. J Clin Oncol. 2015;33(28):3137-3143.
  doi:10.1200/JCO.2015.60.8869.
- Gard CC, Tice JA, Miglioretti DL, Sprague BL, Bissell MCS, Henderson LM, et al. Extending the Breast Cancer
  Surveillance Consortium model of invasive breast cancer. J Clin Oncol. 2024;42(7):779-789. doi:10.1200/JCO.22.02470.
- Gail MH, Brinton LA, Byar DP, Corle DK, Green SB, Schairer C, et al. Projecting individualized probabilities of
  developing breast cancer for white females who are being examined annually. J Natl Cancer Inst.
  1989;81(24):1879-1886. doi:10.1093/jnci/81.24.1879.
- Tyrer J, Duffy SW, Cuzick J. A breast cancer prediction model incorporating familial and personal risk factors.
  Stat Med. 2004;23(7):1111-1130. doi:10.1002/sim.1668.
- Kerlikowske K, Zhu W, Tosteson AN, Sprague BL, Tice JA, Lehman CD, et al. Identifying women with dense breasts at
  high risk for interval cancer: a cohort study. Ann Intern Med. 2015;162(10):673-681. doi:10.7326/M14-1465.
- Ho TH, Bissell MCS, Lee CI, Lee JM, Sprague BL, Tosteson ANA, et al. Prioritizing screening mammograms for immediate
  interpretation and diagnostic evaluation on the basis of risk for recall. J Am Coll Radiol. 2023;20(3):299-310.
  doi:10.1016/j.jacr.2022.09.030.
- Kerlikowske K, Miglioretti DL, Buist DS, Walker R, Carney PA. Declines in invasive breast cancer and use of
  postmenopausal hormone therapy in a screening mammography population. J Natl Cancer Inst. 2007;99(17):1335-1339.
  doi:10.1093/jnci/djm111.
- Rossouw JE, Anderson GL, Prentice RL, et al. Risks and benefits of estrogen plus progestin in healthy postmenopausal
  women: principal results from the Women's Health Initiative randomized controlled trial. JAMA. 2002;288(3):321-333.
  doi:10.1001/jama.288.3.321 (as cited in the draft review; not re-fetched).
- Sprague BL, Conant EF, Onega T, Garcia MP, Beaber EF, Herschorn SD, et al. Variation in mammographic breast density
  assessments among radiologists in clinical practice: a multicenter observational study. Ann Intern Med.
  2016;165(7):457-464. doi:10.7326/M15-2934.
- Saslow D, Boetes C, Burke W, Harms S, Leach MO, Lehman CD, et al. American Cancer Society guidelines for breast
  screening with MRI as an adjunct to mammography. CA Cancer J Clin. 2007;57(2):75-89. doi:10.3322/canjclin.57.2.75.
- US Preventive Services Task Force; Nicholson WK, Silverstein M, Wong JB, Barry MJ, Chelmow D, et al. Screening for
  breast cancer: US Preventive Services Task Force recommendation statement. JAMA. 2024;331(22):1918-1930.
  doi:10.1001/jama.2024.5534.
- Van Calster B, McLernon DJ, van Smeden M, Wynants L, Steyerberg EW. Calibration: the Achilles heel of predictive
  analytics. BMC Med. 2019;17(1):230. doi:10.1186/s12916-019-1466-7.

All PubMed entries verified via NCBI esummary/efetch on 2026-11-27 except Rossouw 2002 and the BI-RADS 5th edition
atlas (a book, cited by description only). Rules: USE-1, USE-3, USE-5, USE-8, USE-9; MET-5, MET-6, MET-7, MET-8, MET-9.

</details>

<details><summary>Precedents</summary>

Read: the definition, the record with its draft `## Review` (3 issues), claims.md, task.json, register.json (flags:
none on this dataset's rules; no drift flag touches SEL-18, SPLIT-32, USE-11 or SPLIT-5), the sibling
`breast_cancer_prediction`, and the Outdated / forced-tag / duplicate-row / one-row-per-entity precedents below.

## Summary

| Decision | Verdict | Closest precedents |
|---|---|---|
| Issue 1: keep `ForcedIIDFromTemporal` (rec. A) | consistent | breast_cancer_prediction issue 1 (Resolved 2026-11-18, Andrej, A); hepatitis_survival_prediction (Resolved 2026-11-18, Andrej, A: "an old one-time study whose outcome treatment has since transformed"); framingham_heart_study_fhs set apart |
| Issue 2: ship with no marker (rec. A) | **departs without a stated reason** | cirrhosis_patient_survival_prediction (CC 2026-10-15 and 2026-11-05, Andrej: keep + `Outdated`); hepatitis_survival_prediction (CC 2026-11-10, Andrej: `Yes`, `Outdated` kept as a note); 2_month_survival_rate_prediction, heart_disease (kept, `Outdated`); SEL-18 (protein_model_quality_rf_pcp, Lennart 2026-11-05) |
| Issue 2, option C (do not add for `Outdated`) | would break SEL-18 as framed | SEL-18: "A `No` that cites `Outdated` names its other reasons too"; ljubljana_breast_cancer retired `Trivial` + `Outdated` (2026-11-10), never `Outdated` alone; hepatitis_survival issue (option C "retire: outdated task" rejected, "the rule needs the task to be gone") |
| Issue 3: one exam per woman (rec. A) | consistent, with a further fact | USE-11 case breast_cancer_prediction (Lennart 2026-10-15: one exam per woman, IID); corporate_credit_rating |
| Dropping the source's 75/25 `training` flag | consistent | SPLIT-5 (a prescribed split is a claim); fosp_cancer_registry_survival (paper's random 75/25 treated as a claim); SPLIT-33 repeated folds; the source split was tested first (LR 0.628/0.626 vs published 0.631/0.624) |
| Expanding the aggregated cells by `count` | no precedent (first definition that expands cell counts); consistent with MET-2 | MET-2 (`count` is an input, never a feature); noaa_storm_events_damage uses a cell weight for scoring only, a different mechanism |
| Accepting `dataset_duplicate_rows` (coarse categories) | consistent, and set apart from the retirement | sepsis_survival_minimal_clinical_records: duplicates of real patients accepted (CC 2026-10-06, Lennart); retired later (`Trivial` 2026-11-10 Andrej, `Not Representative` 2026-11-12 Lennart) because methods sat within 0.001-0.0024 ROC AUC of age / a clinician's rule |
| Metric `roc_auc` from the source's c statistic | consistent | MET-5, MET-8; sepsis (roc_auc fallback, CC 2026-10-21) |

## Details

### Issue 1: forced tag (consistent)

- Same consortium, same mechanism argument, same options: breast_cancer_prediction issue 1 (BCSC 2005-2008, Time:
  Lost, density coding changed 2013) was resolved A by Andrej on 2026-11-18. The same day hepatitis_survival_prediction
  (1970s, Time: Lost, treatment changed) kept `ForcedIIDFromTemporal` too.
- framingham_heart_study_fhs is the only medical `AssumedStationaryRelation` (Andrej, 2026-11-20). What sets it apart:
  the stationary-relation test could be run on the parent file's three exams (Kumo-Tabular flat once age is matched).
  Here no date and no second period exist, and a known mechanism (hormone therapy after WHI 2002, BI-RADS 2013) is a
  fact against. No departure.
- The tree's person question at FORCED.risk (decline the forced split as too risky, `L-FORCED.too-risky`) is not
  offered as an option; the sibling's issue did not offer it either, so the draft follows precedent. An agent answers
  no there by rule.

### Issue 2: age of the data (departs without a stated reason)

- Precedent: every kept medical dataset whose era is argued as changed carries `Outdated` as a note. Andrej's own
  decisions: cirrhosis (1974-86 cohort; "the relation between the findings and the risk still holds today; the
  absolute risk is that of an earlier treatment era", CC 2026-10-15, restated 2026-11-05, marker kept) and
  hepatitis_survival (CC 2026-11-10, `Yes`, `Outdated` kept as a note; Time: Lost, ForcedIIDFromTemporal, the closest
  structural twin). Also 2_month_survival_rate_prediction (Lennart) and heart_disease. cirrhosis's review counted 11
  records marked `Outdated` that were a plain `Yes` on 2026-10-15.
- The draft recommends A (no marker) with "the age matters for a deployed model, not for comparing methods". That
  reason applies to cirrhosis and hepatitis_survival alike, where the marker was set; it does not set this case apart.
  The draft's own issue 1 names a mechanism change (hormone therapy, density coding, film to digital), the same kind
  of era change cirrhosis's `Outdated` records. Option B's con ("a marker on a shipped dataset is only a note") is
  exactly what SEL-18 makes the marker.
- Counter-case: framingham_heart_study_fhs (cohort from 1948) ships without `Outdated`. No CC line argues it, so it is
  an omission rather than a decision and weighs less than two explicit curator decisions.
- Option C ("Do not add (`Outdated`)") names only `Outdated`; SEL-18 (Should) requires other reasons for a `No`. Its con
  also says "with `breast_cancer_prediction` retired": that record's issue 2 (retire) has no Resolved line yet, so the
  con assumes an open decision.

### Issue 3: one exam per woman (consistent)

- USE-11 says one row per entity only when the use case is that row. breast_cancer_prediction took each woman's
  earliest exam (Lennart 2026-10-15), IID without grouping. Here the source made the choice (`risk_rand.txt`, one exam
  per woman, apparently random), which is closer to "any screening visit" than the earliest exam.
- What strengthens it beyond the sibling: the all-exams file has no woman id, so option B cannot be grouped (SPLIT-24
  forbids inferred groups as the source's key), and the USE-11 cost ("loses rows and signal") buys a split that
  otherwise cannot be built.

### Coarse duplicates and the sepsis precedent (consistent, set apart)

- sepsis_survival_minimal_clinical_records: 110,204 admissions in 975 cells of three fields; kept 2026-10-06 with the
  duplicates as real patients, retired 2026-11-10/12 (TP-4 step 2): TabPFN 3.5 only +0.0024 ROC AUC over age alone,
  +0.0010 over an unfitted clinician's rule, tuned methods within 0.0015 of each other.
- Here: 1,007,660 women in 181,903 cells of twelve fields; best probe 0.646-0.656 against age alone 0.611 (a gap of
  about 0.04, roughly 15-20 times sepsis's), methods spread (LR 0.646, LightGBM 0.634, RF 0.578, untuned), and the
  outcome lookup over shared profiles adds nothing (-0.008, SE 0.005). That gap is the fact that sets it apart from
  the retirement. Not run: TP-4's "rule not fitted on these data" (the BCSC page's published Barlow coefficients are
  fitted on the all-exams file, which holds these women, so they are not a clean unfitted rule; Gail needs inputs the
  file lacks). Information only, no issue proposed: no precedent retired a dataset with a 0.04 gap over its best
  single feature.

### Count expansion and the 75/25 flag

- No earlier definition expands aggregated cells into rows; MET-2 is met (`count` dropped, not a feature; a row is a
  woman, the paper's unit). A Cases row (cleaning or MET-2) may be worth adding once settled; not a review issue.
- The `training` flag is the paper's random 75/25 development/validation split; our folds are the same leaf (random),
  repeated per SPLIT-33, and the source split was tested first and reproduces the paper. Consistent with SPLIT-5 and
  the practice of testing the source's task before our own.

## Reflection prompt (issue 2)

**Mark the 1996-2002 exams `Outdated` as a note, as for cirrhosis and hepatitis_survival, or ship without it?**

* **Problem:**
  - Andrej's own decisions keep old medical cohorts with `Outdated` as a note whose era changed treatment or practice:
    cirrhosis (CC 2026-10-15, 2026-11-05)[^c] and hepatitis_survival (CC 2026-11-10)[^h], the latter also Time: Lost
    and `ForcedIIDFromTemporal`.
  - The draft recommends no marker for a reason (age matters for deployment, not for comparing methods) that held for
    those two as well.
  - The draft's issue 1 names the era change itself: hormone therapy use fell after 2002, density coding changed in
    2013, film was replaced.
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | A fact sets it apart: no marker (the AI's best guess: the BCSC still builds its current risk calculator on data of this kind, so the task's inputs are today's) | Ship, no marker; the CC line names that fact | Keeps the record lean | cirrhosis's Mayo score is also still in use and got the marker, so the fact may not hold as a distinction |
  | b | Follow the precedent: `Outdated` as a note | Ship with `Outdated` (issue 2 B); CC line as for cirrhosis: the relation holds, the era's absolute risk and practice differ | Like cases alike; makes the age visible | One more tag |
  | c | Amend SEL-18: `Outdated` only where the task's inputs are no longer used | Ship, no marker; SEL-18 narrowed, cirrhosis and hepatitis_survival re-read | A sharper marker | Changes two settled decisions |

* **Recommendation:** b, the precedent's facts match and no distinguishing fact is written down. Confidence: medium.

[^c]: SEL-18; cirrhosis_patient_survival_prediction, CC 2026-10-15 and 2026-11-05 (Andrej).
[^h]: SEL-18; hepatitis_survival_prediction, CC 2026-11-10 and Resolved 2026-11-18 (Andrej).

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** It is a real, well-documented screening-risk task with honest features and a large test set. But the preparation turns the 75-79 age group into missing values, and that has to be fixed before the dataset ships.

## Concerns, most to least serious

1. **The 75-79 age group was recoded as missing (preparation bug).**
   - The codebook codes `agegrp` as "1 = 35-39 ... 8 = 70-74; 9 = 75-79; 10 = 80-84", and age has no unknown code. The preparation evidently treated 9 as "unknown", the way it is for every other variable.
   - In the sample, `age_group` has no 75-79 level and 11,076 NaN (5.5%), which fits between 70-74 (15,109) and 80-84 (6,261).
   - All 11,076 NaN-age rows are "postmenopausal or age 55 or older", and their cancer rate is 1.24% (70-74: 1.02%; 80-84: 1.21%). These are 75-79-year-olds, not unknowns.
   - **Change:** map code 9 of `agegrp` to "75-79" and keep `age_group` free of missing values. Since age groups are ordered, consider an ordinal encoding.

2. **Coded 9 merges two meanings in `surgical_menopause` and `current_hormone_therapy` (minor).**
   - Code 9 means "unknown or not menopausal (menopaus=0 or menopaus=9)". In the sample, all 55,920 premenopausal rows and all 17,555 unknown-menopause rows are NaN in `current_hormone_therapy`.
   - A tree model can recover this from the menopause column, so this does not bias the task. A distinct level would still be clearer.
   - **Change (optional):** use a level such as "not applicable (not postmenopausal)" where `menopausal_status` is not postmenopausal, and keep NaN for true unknowns.
   - Code 9 for density also means "Unknown or different measurement system". That is fine as missing.

3. **Signal is modest and mostly from age; headroom between methods is small.** The table below shows 3-fold stratified CV on the 200k sample (1,453 positives, 0.73%).

   | Model | ROC AUC | Log loss |
   |---|---|---|
   | Prior | 0.500 | 0.04302 |
   | Age group only | 0.618 | 0.04238 |
   | Logistic regression, all features one-hot | 0.655 ± 0.008 | 0.04194 |
   | LightGBM | 0.654 ± 0.006 | 0.04204 |

   - This matches the source model's reported discrimination (Barlow et al. 2006, c-statistic around 0.62-0.63). It confirms the data and target are real, not generated, and that the task is not trivial.
   - Every feature is a coarse category, so there are no interactions or nonlinearity for flexible models to exploit. The sample has 53k distinct feature vectors in 200k rows. Expect method rankings to sit within noise on AUC.
   - On the full 1.0M rows (about 7,300 positives) the test folds are large enough to score reliably. The table is valid, but it may separate methods poorly. Keep it, and possibly lean on log loss or calibration.

4. **Version, target choice and unit are not stated in `task.md`.**
   - The source offers version 1 (2,392,998 mammograms, several per woman, aggregated to 280,660 count records) and version 2 ("limits observations to one per woman").
   - It also has two outcomes: `invasive`, and `cancer` (invasive or DCIS).
   - 1,007,660 rows does not match version 1's 2.39M. So this is presumably version 2 expanded by `count`, which would rule out the same woman appearing in train and test. That is good, but I could not verify it.
   - The 0.73% prevalence is consistent with "invasive or DCIS" but I could not confirm it.
   - **Change:** state in the record that this is version 2 expanded by `count`, and that the target is `cancer` (invasive + DCIS).

5. **Identical rows across train and test.**
   - In the sample, 145,585 of 200,000 rows duplicate another row.
   - These are distinct women who share a coarse covariate profile. That follows from the aggregated, de-identified release, not from leakage. With a random IID split, it amounts to estimating cell-wise risk, which is the intended use.
   - Acceptable; no change needed.

6. **Split.**
   - Random IID 3-fold suits a static, one-row-per-woman registry extract (1996-2002, no dates released). The source's own split is a random 75/25 `training` flag. Dropping that flag from the features is correct.
   - A temporal or by-registry split would mirror deployment better, but the release has no dates or site identifiers, so it cannot be done.

## Task and honesty checks

- **Use:** a woman attends screening mammography. The radiology or primary-care team estimates her near-term breast-cancer risk from questionnaire items and BI-RADS density, to guide supplemental imaging, chemoprevention counselling or the screening interval. This is the BCSC risk model's real use.
- **Timing:** every feature is known at the index visit. Density is read from the index mammogram. The leaking item, the index mammogram's assessment, is excluded by the source ("no ... assessment (outcome) of the index screening mammogram"). Women with a prior breast cancer are excluded.
- **Plausibility:** cancer risk rises with age from 0.30% at 35-44 to about 1.2% at 75-84, and menopause, hormone therapy and prior procedure all point the expected way. Women under 45 coded postmenopausal are absent, as the codebook says.
- **Weight:** `task.md` names no weight column. That is correct: rows are already expanded, so `count` must not be applied a second time.
- **Licence:** the site offers a free public-use file after a name/institution/email form, and the reference must be cited. No formal licence text is given, so check whether redistribution is allowed.

## What I could not check

- The full 1,007,660-row table (I had only the 200k sample) and the raw `risk.txt`.
- Which source version and which outcome column were used.
- Whether redistributing the expanded file is permitted.
- The exact c-statistic in the Barlow paper (the paper is behind a paywall; the figure above is from memory).

</details>

<details><summary>Task gamer</summary>

**Verdict:** I could not game this task. Every feature is a coarse self-reported or registry category, the rows are shuffled, and no copy, order, format or test-composition attack beat the honest model. The only questions are about meaning: breast density comes from the reading the prediction point says has not happened yet, and the `75-79` age band was turned into missing values.

All scores are ROC AUC on the 3 shipped folds, using all 1,007,660 rows (no subsampling).

## Exploits

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Breast density read from the index mammogram itself | `attacks.py` | 0.6375 (density dropped) | 0.6531 (baseline, density in) | +0.0150 to +0.0167 | Mostly yes: a density from her previous mammogram (every woman had one in the last 5 years) is close. Strictly no, because the prediction point is "before it is read" | Reword the prediction point to "at the screening visit, once density is assessed". Do not drop the column |

The noise floor for scale: adding a column of random numbers to the default LightGBM moves the mean by -0.002 to -0.004 (0.6493 and 0.6512 against 0.6531). Per split the drop reaches up to 0.0053 (fold 1, 0.6515 to 0.6462).

**1. Density.** The source documentation says density "is judged by the radiologist from the screening mammogram", which is the index exam. Density alone scores 0.541. Age plus density scores 0.632, against 0.610 for age alone. Dropping density costs 0.0156 on average.

- This is the established Barlow/BCSC risk factor, not label leakage. The prior-exam density a deployed model would use is highly correlated with it.
- What I could not rule out: the radiologist who sees a lesion on the index exam might rate density differently, or leave it missing. Density is missing in 27% of rows. Its missing flag on its own adds 0.002 over dropping density (0.6397 against 0.6375), which is inside the noise floor.
- What would decide it: the AUC of density taken from the prior exam, which this release does not include.

## Flaws that hurt an honest model

None in the data. No training rows are mislabelled or out of time; the regime is IID with one row per index mammogram.

The default untuned LightGBM slightly overfits 12 sparse categoricals (71,328 of 134,407 feature combinations are singletons). That is a model choice, not a task flaw:

| Model | Script | fold 0 | fold 1 | fold 2 | mean |
|---|---|---|---|---|---|
| LightGBM default (baseline) | `attacks.py` | 0.6479 | 0.6515 | 0.6599 | 0.6531 |
| LightGBM default, NaN as an explicit level | `attacks.py` | 0.6508 | 0.6529 | 0.6579 | 0.6538 |
| LightGBM regularised (7 leaves, min_child 2000, lr 0.03) | `honest.py` | 0.6557 | 0.6559 | 0.6631 | **0.6582** |
| ... plus a random column | `honest.py` | 0.6543 | 0.6540 | 0.6598 | 0.6560 |
| Logistic regression, one-hot | `honest.py` | 0.6481 | 0.6457 | 0.6530 | 0.6489 |
| Logistic regression, one-hot with menopausal-status interactions (Barlow-style) | `honest.py` | 0.6480 | 0.6483 | 0.6557 | 0.6507 |

For reference, Barlow et al. 2006 report c = 0.631 (premenopausal) and 0.624 (postmenopausal) for separate models. A pooled model gains from age, which differs a lot between the two groups.

## Preparation issues (no score effect)

- **`age_group` has no `75-79` level.** The source codes 1 to 10 (35-39 to 80-84) with no unknown code. The kit has 9 levels plus 56,233 NaN, and the NaN rows have a cancer rate of 1.154% (70-74: 1.094%, 80-84: 1.092%). So NaN here means 75-79. Trees treat NaN as its own level, so this costs nothing, but the meaning is wrong. **Fix:** map NaN back to `75-79`.
- **Size and source version.** The kit's size (1,007,660 rows, 7,319 cancers) matches the "1 million women" of the paper and the one-observation-per-woman second release, not the 2,392,998-mammogram first release. I could not confirm this, because the source file is behind a registration form.

## Attacks that found nothing

| Attack | Result |
|---|---|
| Row order | Cancer rate by position decile ranges 0.0069 to 0.0079, with no trend. Adjacent rows share a feature combination 0.02% of the time. Adjacent positive pairs: 62, against 53 expected by chance |
| Copies across the split (`copies.py`): boost the prediction by the share of training positives in the same exact cell | -0.0002 to -0.0018 (a=0.5 to 5) |
| Same, on a looser key (density, age and last-mammogram result dropped, as they could change between a woman's visits) | +0.0000 to +0.0005. Rare loose cells (at most 3 training rows) contain no positive copy at all, so this is noise, not a same-woman match |
| Positive rate of rare exact cells (at most 3 training rows) that hold a training positive, against those that do not | 0.0094 vs 0.0085 (fold 0), 0.0088 vs 0.0079 (fold 1), 0.0110 vs 0.0090 (fold 2): no usable signal |
| Nearest-row lookup: smoothed target rate of the exact feature combination | 0.5585, far below the model |
| Cell count over train+test as a feature (needs the test rows) | 0.6491, against 0.6531 (-0.004, a noise-level drop) |
| Missing pattern of all 12 columns, alone | 0.603. Almost all of this is structural: menopausal status is missing only for ages 35-54, surgical menopause and HRT only when not postmenopausal, and age only for the hidden 75-79 band. Age alone gives 0.610 |
| Missing flags of the 8 non-structural columns, alone | 0.560; on top of age, +0.012 (0.621 against 0.610). For example, a missing BMI lowers the rate by 0.0007 to 0.002 in most age bands. This likely tracks the registry or questionnaire version, which a deployed model at the same site has: signal, not an exploit |
| Number of missing values, alone | 0.508. Added to the baseline: +0.0025, inside the noise floor |
| Formats and strings | Every column is a categorical with fixed labels. There are no numeric values, decimals, ids or free text to attack |
| Transforms over all rows, and the weight | None present (no scaled columns, no `sample_weight`) |
| Columns from after the outcome | None. The best single feature is age (0.610). No column comes close to the full model |
| Web search | No competition, forum or "leak" thread exists for this dataset. It is distributed after a registration form, so I did not try looking rows up in the published file |

## What I could not check

- Whether density measured on the index exam differs from prior-exam density for women later diagnosed (this would need the full BCSC data).
- Whether the kit is the one-per-woman release. The copy tests found no same-woman leakage, which fits that release.

</details>

<details><summary>Advocate</summary>

Verdict argued: ship as defined. The age band fix is applied; the rest are text fixes or one cheap level. No problem any
agent found is a validity failure that survives its mildest remedy.

New test: the shipped 3 folds, paired per fold.
The built frame the script loaded still held the 75-79 band as missing, but every model here treats missing as its own
level ("NA" one-hot, a category rate, LightGBM's missing bin), so the band is kept intact. The claim auditor measured
the fix's effect at LR 0.6489 -> 0.6489, LightGBM 0.6551 -> 0.6557.

| Model | ROC AUC (folds 0/1/2) | mean | log loss | cancers in top 10% |
|---|---|---|---|---|
| prior | 0.5 | 0.500 | 0.0430 | 10.9% |
| age group alone (train-side rate) | 0.611 / 0.608 / 0.610 | 0.610 | 0.0425 | 15.2% |
| LR one-hot, density dropped | 0.635 / 0.628 / 0.635 | 0.632 | 0.0422 | 19.6% |
| LR one-hot | 0.648 / 0.646 / 0.653 | 0.649 | 0.0420 | 21.2% |
| LightGBM regularised (7 leaves, min_child 2000) | 0.656 / 0.657 / 0.663 | 0.658 | 0.0419 | 21.9% |

Gain over age alone, per fold: LR +0.037 / +0.038 / +0.043; LightGBM +0.044 / +0.049 / +0.053.

## 1. A real use case, on the source made for it (P3: USE-1 Must, USE-8 Must, USE-9 Should; P5: PROV-7 Must)

- Claim: the rows, inputs and label are those of the BCSC's published risk model (Barlow 2006, JNCI). It is the only
  open source of the risk task *before the read*. The source has no teaching-only clause. Its sibling
  `breast_cancer_prediction` is a teaching set, and in that set the label is found through the read (its issue 2).
  PROV-7: a shared consortium with a distinct task is not a duplicate.
- The real problem (domain practitioner): `direct` overstates "tailor screening and prevention". Prevention acts on
  5-year invasive risk. Most of the 1-year in-situ-or-invasive label is what the index screen itself finds.
- Mildest remedy: text only. Under USE-9, rewrite the use case as **pre-read triage**: the images are taken and density
  is recorded, the assessment is not yet made, and the programme ranks exams for reading priority, double reading or a
  same-day diagnostic slot. This is the moment in the data: density in, assessment out. The 1-year, screen-detected
  label is that decision's outcome. BCSC publishes this kind of model (Ho et al. 2023, J Am Coll Radiol). The fit stays
  `direct`, and the data do not change.
- Why it outranks the objection: the weighed factor "a use case rephrased only to excuse a gap" (−) does not apply.
  The triage use case is the one the information set already describes, and the field practises it. A Weigh factor
  cannot override USE-9 (Should). If the curator prefers the prevention wording, the fallback is `fit="approximate"`
  with the horizon named. That is still a ship (USE-8).

## 2. Nothing leaks; density is a legitimate input (P4: LEAK-10 Must, LEAK-37 Must, LEAK-42; P2: SEL-14 Must)

- Density is the radiologist's reading of this mammogram, recorded before the exam's assessment. The source withholds
  the assessment ("The index mammogram's assessment is not included"). The BCSC calculator takes density as an input.
  SEL-14 keeps such readings, and the same consortium's precedent is `breast_cancer_prediction` (Lennart, 2026-10-15).
  The definition now says this.
- Evidence of no leak:
  - The invasive share among cancers is the same with density known and unknown (80.4% vs 80.6%, column auditor).
  - Dropping density costs only 0.016-0.017 AUC (task gamer; my LR 0.649 -> 0.632). It is a risk factor, not the answer.
  - The profile lookup across folds gains -0.008 (SE 0.005; 0 of 3 splits positive).
  - The gamer's order, copy, missing-pattern and format attacks all found nothing.
- Missing density or last-mammogram result raises risk 1.2-1.4x within age. Both values are fixed at the visit (site,
  first exam), so LEAK-37 keeps them as inputs. One line in the notes covers it.

## 3. The split is the tree's split, and the source's split was tested first (P4: SPLIT-36, SPLIT-5, SPLIT-32, USE-11)

- Split auditor: the walk reaches L-FORCED.random and `ForcedIIDFromTemporal`, which matches `split_leaf`.
  - One exam per woman, so no unit crosses the split (USE-11, as `breast_cancer_prediction`).
  - The source's 75/25 flag scores LR 0.648 and LightGBM 0.657, against our 0.649 and 0.659. It is one random split
    of the same rows (SPLIT-5).
  - The one-exam file is a strict subset of the all-exams file with the flag carried over (0 cells exceed it). The
    file version of issue 3 A therefore loses nothing a valid split could use. The all-exams file cannot be grouped:
    it has no woman id.
- Issue 1, A (keep the forced tag) follows the sibling's resolution (Andrej, 2026-11-18) and hepatitis_survival. Only a
  person sets `AssumedStationaryRelation`.
- Correction to the draft (claim auditor R3): the Background line should say 24.8% on hormone therapy, not 28.6%. The
  0.567 is the premenopausal missing code. The recommendation rests on the post-WHI fact, which holds.
- Place branch at [CLI.meets]: the folds are identical either way, and there is no registry key to test. The use case
  scores later women of the same programmes. Keep A as written (split auditor's recommendation). If the curator reads
  the use case as transfer beyond the BCSC, only a tag changes, not the ship.

## 4. Worth benchmarking: a real gain over the best single feature (P6: TP-2 Should, TP-4 Must)

- From the table above:
  - Both methods beat age alone on every fold: LR by +0.037 to +0.043, LightGBM by +0.044 to +0.053. TP-4 step 1
    finds no match.
  - Methods spread by 0.009 between LR and regularised LightGBM. LightGBM is ahead on all 3 folds.
  - Each fold has about 2,440 test cancers.
- Precedent checker: the gap over the best single feature is about 15-20 times sepsis's (+0.0024 over age), the only
  coarse-duplicate retirement. No precedent retired a dataset with a 0.04 gap.
- Under triage, the top 10% of exams by LightGBM hold 21.9% of the cancers, against 15.2% by age and 10.9% at random.
  That change in a reading queue is large enough to matter (TP-2 step 2).

## 5. `roc_auc` is the source's deliberate metric and fits the decision (P6: MET-5 Should, MET-8 Should; the source-metric tension row)

- The abstract names the c statistic as its one measure ("Concordance ... was assessed by a concordance (c)
  statistic"). MET-5 makes it the source metric. It is also MET-8's binary fallback.
- Triage is a ranking decision, so AUC scores exactly what the actor does (point 1). No source fixes a threshold or a
  cost (MET-6, MET-7), so no metric needs absolute risk. The tension row gives the source metric precedence when it is
  one deliberate choice that suits the decision.
- `log_loss` would not change the board. In my run it orders the models the same way: LightGBM 0.0419 < LR 0.0420 <
  age 0.0425 < prior 0.0430. The gamer's regularised model, which tops on AUC, is also best on log loss.
- The domain practitioner's random-forest case (log loss worse than the prior, AUC 0.578) is a model failure that AUC
  already ranks last.
- Mildest remedy for the calibration concern: a note that calibration matters to a clinical user.
- Nuance to document (claim auditor 16): the published 0.631 and 0.624 are per menopause stratum, while ours is pooled
  (about 0.65).

## 6. The age of the data is a note, not a reason to drop (P2: SEL-18 Should)

- SEL-18: `Outdated` alone does not leave a dataset out. The decision still exists: BCSC builds its current models on
  data of this kind. No newer open BCSC file has the outcome (Risk Factors 2005-2017 has none).
- Option C of issue 2 ("do not add, `Outdated`") names no other reason, so it breaks SEL-18 as framed. Its con also
  assumes `breast_cancer_prediction` is retired, but that issue is still open (R4).
- I concede the precedent: cirrhosis (Andrej, 2026-10-15 and 2026-11-05) and hepatitis_survival (Andrej, 2026-11-10)
  ship with `Outdated` as a note for the same kind of era change. Take issue 2 **B**, ship with `Outdated` as a note.
  That is a ship, and it treats like cases alike.

## 7. What is left is cheap P7 cleaning; fix it and ship (P7: CLEAN-12 Should; principles, "a real task against imperfect cleaning")

- Hormone therapy and surgical menopause code 9 includes "not menopausal". CLEAN-12 asks to split a mixed level by what
  the data shows, and `menopausal_status` shows it: all 280,205 premenopausal women carry 9 in both columns.
  - I concede it. Add a "not menopausal" level for premenopausal women and keep missing for the rest.
  - It is lossless today, since trees recover the split from `menopausal_status`, so the scores are unaffected.
- Text fixes that change no data:
  - The BibTeX note's grant: the page asks for P01CA154292 and the download line (R5).
  - The relatives level "1" also holds "positive, number unknown".
  - The draft's 28.6% / 0.567 background (R3).
  - Issue 2 C's "retired" wording (R4).
- None of these changes what the target means. Under step 3 of the principles a real task carries such imperfections
  once they are fixed or written down. This sits on the remedy ladder's "fix the definition" rung, far from exclusion.

Judgment record (proposed): Verdict: ship after small changes.
- Validity: SEL-14 holds; SEL-18 holds (`Outdated` as a note); USE-1 holds; USE-8 holds (direct via USE-9 triage
  wording, else approximate); LEAK-10/37/42 hold; SPLIT-36 holds (L-FORCED.random, `ForcedIIDFromTemporal`); USE-11
  holds; PROV-7 holds.
- Value: TP-4 step 1 passes (+0.04-0.05 over age on 3/3 folds); MET-5 `roc_auc`.
- Quality: CLEAN-12 fixed (age band; "not menopausal" level); text fixes R3-R5.

</details>

<details><summary>Critic</summary>

**Position: ship it only after changes.** It is a real task on faithful data, and the split is honest. No Must
excludes it. But the definition claims a direct fit that its own label and inputs do not support. The record leaves
out the `Outdated` note that the curator's own precedents set. Several facts in the review draft are wrong. Every
remedy below is a text, tag or label change. None asks to retire the dataset or change the folds.

Ordered by principle rank, then strength (principles.md, "What the curator reads first").

## 1. Mark it `Outdated` as a note (issue 2 B, not A). SEL-18 (Should), like cases alike

- **Problem:** the draft recommends shipping with no marker because "the age matters for a deployed model, not for
  comparing methods". The curator decided the opposite on the same facts. In cirrhosis_patient_survival_prediction
  (CC 2026-10-15 and 2026-11-05) and hepatitis_survival_prediction (CC 2026-11-10) the dataset was kept and `Outdated`
  was added as a note. hepatitis_survival is the structural twin: Time: Lost and `ForcedIIDFromTemporal`.
- **Evidence:** precedent checker. The draft's reason applies equally to both precedents, so it does not set this case
  apart. The draft's own issue 1 names three era changes: hormone therapy use fell after the WHI trial in 2002, the
  BI-RADS density definition changed in 2003 and 2013, and digital mammography and tomosynthesis replaced film.
  Domain practitioner: 24.8% of the women here are on hormone therapy, today a small minority. The only counter-case,
  framingham, has no CC line arguing it.
- **Effect:** a user who reads "screening risk model" will assume today's practice.
- **Remedy:** ship with `Outdated` as a note, and a CC line in the cirrhosis style ("the relation of the risk factors
  holds; the era's hormone therapy, density scale and imaging differ"). Keep issue 1 at A (`ForcedIIDFromTemporal`).
  The facts named above are SPLIT-32 reasons against a stationary relation, and I agree with A. Option C as worded
  (`Outdated` alone) would break SEL-18. Rewrite it or drop it.

## 2. The fit is approximate, not direct, as the use case is written. USE-5, USE-8 (Must); USE-9 (Should)

- **Problem:** the use case is "tailor screening and prevention" at the visit, and the record sets `fit="direct"`.
  Two gaps:
  - **Target (USE-5).** The label is invasive or in situ cancer within one year of this mammogram. Most such cancers
    are found by this screen's own work-up: they are detections, not future risk. The decisions the use case names act
    on other horizons and outcomes:
    - chemoprevention: 5-year invasive risk, at thresholds such as 1.67% or 3%;
    - supplemental MRI: lifetime risk of 20% or more;
    - the BCSC's own deployed models: 5-year and 10-year invasive (Tice 2008, Tice 2015, Gard 2024).
  - **Moment (USE-3).** The information set (this exam's density, without its assessment) exists only once the
    radiologist has read the density. A prevention or screening-plan decision at the visit would use the prior exam's
    density.
- **Evidence:**
  - Domain practitioner, with sources, ranks this the largest gap after the age bug.
  - Barlow 2006 abstract: "identify women at high risk ... for preventive interventions or more intensive
    surveillance". That is the paper's aim, but its label is the 1-year screening outcome.
  - The sibling's open issue 2 retires breast_cancer_prediction because its label is "found through" the read's
    decision. Here the read is withheld, so the features are clean. The label is still mostly what this exam's work-up
    finds.
  - Task gamer: density from the index exam is worth +0.0156 ROC AUC (0.6375 without it, 0.6531 with it).
- **Why USE-9 does not rescue `direct`:** the practitioner's direct reading is pre-read triage, which ranks exams for
  reading priority. In 1996-2002 a radiologist read the density, so it was not known before the read. Automated
  density software is today's tool, not this data. A triage rewrite would be "a use case rephrased only to excuse a
  gap" (USE-9's weighed factor against).
- **Remedy (text only):** set `fit="approximate"`. `fit_reason` should say that a 1-year invasive-or-in-situ outcome,
  mostly the index screen's detections, with density read from this exam, stands in for the longer-horizon invasive
  risk that screening and prevention decisions use. If the curator prefers the triage reading, the use case must say
  that density is the radiologist's reading at the start of the read, and the gap still needs naming.

## 3. Decide the place, and write it into the use case. SPLIT-36 [CLI.meets] (Should)

- **Problem:** the data pools 6 BCSC registries with no registry column. The use case says "a screening programme",
  which does not say whether that means a BCSC programme scoring later women or any programme. The BCSC calculator and
  the paper are offered for US women in general. Under "another site" the walk goes to the place step: one unkeyable
  place, one row per woman, so L-PLACE.random (`ForcedIIDFromGrouped`). No v0.2 definition has reached that leaf, so it
  goes to a human reviewer.
- **Evidence:** split auditor, tree walk and problem 2. The folds are identical under either reading.
- **Remedy:** name the actor's place in `use_case`. For "later women at the same programmes", keep the leaf (the split
  auditor's A). For any programme, add a group basis line naming the 6 registries the data cannot key. Either way the
  choice should be written down, not left implicit.

## 4. Split the "not menopausal" code, and label the relatives level honestly. CLEAN-12 (Should)

- **Problem:** in `surgical_menopause` and `current_hormone_therapy`, code 9 means "unknown or not menopausal". It now
  becomes missing for all 280,205 premenopausal women, mixed with true unknowns: 198,790 and 96,893 postmenopausal
  women, plus 88,739 of unknown menopause. CLEAN-12 says a level that mixes a state with "not asked" is split "by what
  the data shows, else missing". Here the data shows it: `menopausal_status`. The definition's comment now says what
  code 9 means, but the column still mixes the two.
- **Evidence:** column auditor (problem 2); claim auditor (R2); blind reviewer (concern 2). Score effect nil: trees
  can read the split from `menopausal_status`.
- **Remedy (cheap and safe, P7):**
  - code 9 becomes "not menopausal" where `menopausal_status` is premenopausal, and stays missing otherwise;
  - `first_degree_relatives_with_breast_cancer` level "1" becomes "1 (or positive, number unknown)", or a note says
    so (codebook).

## 5. Correct the review's facts before the curator decides on them. EV-1, EV-2, EV-6; PROV (citation)

The draft's issues rest partly on wrong numbers.

- **Issue 1, Background.** "28.6% on hormone therapy" is the all-exams file; this file has 24.8%. "Third strongest
  feature, ROC AUC 0.567" is the premenopausal missing code. Among postmenopausal women with a known answer, yes
  against no scores ROC AUC 0.510 (claim auditor, R3). The WHI fact stands; the claim that hormone therapy is strong in
  the data does not.
- **Issue 2, option C Con.** "with `breast_cancer_prediction` retired" states an open decision as done: its issue 2
  has no Resolved line (R4).
- **Main points.** The record compares our pooled ROC AUC of 0.650 to 0.656 with the paper's per-stratum c of 0.631 /
  0.624 as "in line with the field". These are different scales: per stratum we get 0.62-0.63, pooled 0.649 (claim
  auditor, claim 16). Say so. All headline numbers (age alone 0.611, LR 0.650, LightGBM 0.656, 91% shared profiles)
  came from the frame with the age bug and need the rerun's values.
- **BibTeX note.** It cites grant HHSN261201100031C. The source page's required text is "funded by the National
  Cancer Institute (P01CA154292). Downloaded xx/xx/xxxx from the Breast Cancer Surveillance Consortium Web site"
  (checked in rfdataset.html). Use the required text (R5).
- **Remedy:** rewrite those lines; no data change.

## Raised in phase A and dropped (no case)

- **Metric `roc_auc` against log loss.** The abstract names the c statistic as the paper's one measure ("Concordance
  of the predicted with the observed outcomes was assessed by a concordance (c) statistic"). That is a deliberate
  choice under MET-5, and no source fixes a threshold (MET-6, MET-7). A note that calibration matters to a clinical
  user is enough.
- **Selection of the one exam per woman.** The undocumented rule fits a random draw. Cancer exams are kept 0.629 of the
  time, which matches a mean 1/k for women whose cancer ends their follow-up after about 1.6 exams, against 2.37
  exams per woman overall. Issue 3 A stands.
- **Value (TP).**
  - Regularised LightGBM beats one-hot LR on every fold, by 0.008-0.010 (task gamer).
  - Age alone scores about 0.61 against about 0.66 for the best model.
  - No exploit gains (lookup -0.008).
  - It is not trivial, and methods separate.
- **Duplicate rows, the source's 75/25 flag, and the time tag (A):** sound as implemented.

</details>

<details><summary>Advocate rebuttal</summary>

The critic and I now agree on every point except the fit, and I concede the fit too (point 2). Joint position: **ship
after changes**. The changes are text, one tag and one categorical level. The folds, rows and target stay. No new
experiment was needed. The facts below come from the phase A reports and my opening run.

## 1. `Outdated` as a note (issue 2 B): concede

I conceded this in my opening point 6. SEL-18 (Should) and like cases alike point the same way: cirrhosis
(2026-10-15 and 2026-11-05) and hepatitis_survival (2026-11-10) are the precedent, and the draft gives no fact that
sets this case apart.
- What follows: ship with `Outdated` as a note, with a CC line in the cirrhosis style.
- Option C as worded breaks SEL-18. Drop it or give it its other reasons.
- Issue 1 stays at A.

## 2. Fit approximate, not direct: concede (I withdraw the triage rewrite)

My opening argued that USE-9 gives a direct fit through a pre-read triage use case. The critic's objection holds, for
two reasons.

- **The data's moment is not a triage moment.** In 1996-2002 one radiologist recorded density and the assessment in the
  same read. "Density known, assessment not yet made" was not a step at which anyone acted. The source made that cut
  by withholding the assessment.
- **Today's triage uses a different input.** It would take density from automated software at acquisition, not a
  radiologist's BI-RADS call. Ho et al. 2023 also predicts recall, not one-year cancer.

USE-9 asks whether the data *as shipped* mirrors another use case. It does not: the density input is a stand-in in
both readings. A rewrite would therefore be a use case rephrased to excuse a gap, the factor against.

The original use case (tailor screening and prevention, the aim stated in Barlow's abstract) is more honest, with
`fit="approximate"` (USE-8, Must). This still ships: an approximate fit is a named gap, not a None (USE-8; no use-case
rule excludes it).

`fit_reason` should name both gaps:
- the label: a one-year invasive-or-in-situ outcome, mostly this screen's own detections, stands in for the longer
  invasive-risk horizon that screening and prevention decisions use;
- the input: density read from this mammogram stands in for the prior exam's density, which is what a visit-time model
  would use.

The size of the density gap is known. Dropping density costs about 0.016 ROC AUC (task gamer 0.6531 -> 0.6375; my LR
0.649 -> 0.632). With density dropped, the task still clears age alone on every fold: LR without density +0.020 to
+0.025.

The question and `known` already say density comes from this mammogram's read, before its assessment, so only
`fit` and `fit_reason` change.

## 3. Write the place into the use case: concede the write-down, keep leaf A

The folds are identical under either reading (split auditor), so this is a SPLIT-36 documentation step, not a split
change.
- My recommendation stands: the actor is the screening programmes the data comes from (the BCSC registries), scoring
  their later women. This keeps L-FORCED.random and `ForcedIIDFromTemporal` (split auditor's A).
- If the curator means any US programme, add a group basis line naming the 6 registries the data cannot key. That leaf
  goes to a human reviewer.
- Either way the sentence goes into `use_case`.

## 4. CLEAN-12, "not menopausal" level and the relatives label: concede

This is the same as my opening point 7 (CLEAN-12, Should): the data shows the state through `menopausal_status`.
- Code 9 becomes "not menopausal" for premenopausal women and stays missing otherwise.
- The relatives level "1" says "or positive, number unknown".
- Score effect nil. These are cheap, safe P7 fixes.

## 5. Correct the draft's facts: concede, with the rerun values

Agreed on all of them: R3 (24.8% on hormone therapy; 0.567 is the menopause code; HT yes vs no AUC 0.510), R4
(sibling not retired), claim 16 (pooled against per-stratum c statistic) and R5 (P01CA154292 and the "Downloaded"
line). EV-1 and EV-2: a measurement beats the draft's number.

Values for the Main points line after the age fix:

| Quantity | Value |
|---|---|
| age group alone | 0.610 |
| LR one-hot | 0.649 |
| LightGBM, regularised | 0.658 |
| LightGBM, untuned (claim auditor) | 0.6557 |
| test women sharing a training profile | 91.2% |

All are on the shipped folds. My run's frame kept 75-79 as its own level (missing), which every model treats as a
category, so these equal the fixed frame's values. The claim auditor measured the fix's effect directly: LR
0.6489 -> 0.6489. The 91.2% does not move either: the fix renames one level one-to-one, so the profiles stay the same.
Still, the record should quote the rerun check's README once it lands.

Per-stratum wording: "per menopause stratum our LR reaches 0.62-0.63 (claim auditor), the published 0.631 / 0.624;
pooled, 0.649".

## On the critic's dropped points

I agree with all four: metric `roc_auc` (MET-5), issue 3 A, value (TP-2 and TP-4: +0.037 to +0.053 over age on 3 of 3
folds), and duplicates, flag and time tag as implemented. Nothing remains to dispute.

## Joint judgment record (proposed for the mediator)

**Verdict:** ship after changes.

| | Finding |
|---|---|
| Validity | SEL-14 holds. SEL-18: `Outdated` as a note. USE-8: **approximate** (label horizon and index-exam density named). LEAK-10, LEAK-37 and LEAK-42 hold. SPLIT-36 holds: L-FORCED.random, `ForcedIIDFromTemporal`, place written into `use_case`. USE-11 and PROV-7 hold. |
| Value | TP-4 step 1 passes. MET-5: `roc_auc`, with a calibration note. |
| Quality | CLEAN-12 fixed: the age band, the "not menopausal" level and the relatives label. Text fixes R3, R4, R5 and claim 16. |

For the curator: issue 1 A, issue 2 B, issue 3 A; the place sentence (A recommended).

</details>

<details><summary>Critic rebuttal</summary>

We agree on the verdict: ship after changes. We agree on `Outdated` as a note (issue 2 B), the forced tag (issue 1 A),
the file version (issue 3 A), the "not menopausal" level, and the text fixes R3-R5. One dispute is left: whether the
fit is `direct` (advocate's point 1).

## Disputed: point 1, fit `direct` via a pre-read triage use case (USE-8 Must, USE-9 Should)

The advocate concedes the gap: "`direct` overstates 'tailor screening and prevention'". The only question is whether
the triage rewrite makes the fit direct. It does not.

- **The triage moment does not exist in these rows.** In 1996-2002, density was "judged by the radiologist from the
  screening mammogram" (codebook). It was recorded during the read, by the reader, before the assessment. A queue that
  ranks exams for reading priority or double reading acts before anyone reads. In this era, density was not known at
  that moment. It is known pre-read only with automated density software, which this data does not have. USE-8 says
  direct means "the rows, the features, the label's timing ... mirror the use case". The feature timing does not.
- **USE-9's condition fails, and USE-9 itself calls for the weighing.** USE-9 applies "where the features are known and
  the label is not". Here density is not known at the triage moment. USE-9 also says "Weigh it together with the factor
  against it", so the "rephrased only to excuse a gap" factor is part of the rule, not something set against it. A use
  case written after the gap was found, whose moment the data's era did not have, is that factor.
- **Ho et al. 2023 is not this task.** By the domain practitioner's own description, that model prioritises exams "on
  the basis of risk for recall". Its target is the read's decision (recall), not cancer within a year. It shows that
  triage is practised. It does not show that a triage actor acts on a 1-year cancer label with radiologist density.
- **The top-10% capture (21.9% against 15.2% by age) is a value fact, not a fit fact.** It shows the ranking is useful
  (TP-2). It does not change when density is known.

**What I accept:**
- Either wording ships.
- If the curator prefers triage, write it with the gap named: density is the radiologist's reading at the read, where
  today's software reads it before.
- Either way: `fit="approximate"`, with the horizon and density named in `fit_reason`. The advocate offers this as the
  fallback for the prevention wording.
- Under USE-8, approximate is still a ship. The cost is one honest field.

## Conceded

| Advocate's point | Concession |
|---|---|
| 2, no leak; density a legitimate input (SEL-14, LEAK-10/37/42) | Conceded; I never argued a leak. One line in the notes on the informative missingness of density and the last mammogram result (LEAK-37) |
| 3, split (SPLIT-36, SPLIT-5, USE-11) | Conceded, with one condition. The advocate states the use case "scores later women of the same programmes". `use_case` still says only "a screening programme", so write that into it. Then the walk's A stands with no group basis. My point 3 asked for exactly this |
| 4, worth benchmarking (TP-2, TP-4) | Conceded. LightGBM leads LR on all 3 folds, and both beat age by 0.037-0.053 |
| 5, `roc_auc` (MET-5, MET-8) | Conceded; I had dropped it. Add a calibration note. Note also that the published 0.631 / 0.624 are per stratum and ours (about 0.65) is pooled (claim 16) |
| 6, `Outdated` as a note (SEL-18) | Agreed: issue 2 B, and option C rewritten or dropped |
| 7, CLEAN-12 level and text fixes | Agreed, plus the relatives level "1" label |

Caveat on the advocate's table: it was run on the frame with the 75-79 band still missing. The claim auditor measured
the effect of the fix as nil (LightGBM 0.6551 to 0.6557), so the table stands. The record should cite the rerun's
numbers, not these.

## Proposed judgment record

- **Verdict:** ship after changes.
- **Validity:**
  - SEL-14 holds; SEL-18 is a note (`Outdated`, issue 2 B).
  - USE-1 holds; USE-8 approximate, with the horizon and radiologist density named.
  - LEAK-10, LEAK-37 and LEAK-42 hold; USE-11 holds.
  - SPLIT-36 holds (L-FORCED.random, `ForcedIIDFromTemporal`, issue 1 A), with the place written into `use_case`.
- **Value:** TP-4 step 1 passes; MET-5 `roc_auc`.
- **Quality:**
  - CLEAN-12 fixed: the age band, the "not menopausal" level, the relatives label.
  - Text fixes R3-R5 and the pooled against per-stratum note.
- **For the curator:** a weighing call on the fit, `approximate` or `direct` via the triage wording.

</details>
