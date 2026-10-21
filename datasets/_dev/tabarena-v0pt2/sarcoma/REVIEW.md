# sarcoma

**Outcome:** added. TCGA sarcoma from the multi-omic benchmark of Rappoport & Shamir (2018): 201 patients, 25,910
expression, methylation and miRNA features, the type confirmed by TCGA's expert pathology review as a five-class
target, IID over patients. Verdict: ship after the changes now made (review panel, mediator). Validity: SEL-4 holds
(a pathology diagnosis, not a cluster label); SEL-5 not triggered (the 12q15 copy number that defines dedifferentiated
liposarcoma is not shipped, and the best single feature has a skill, the share of the prior's log loss a model removes, of 0.05 over 30 splits, 0.075 in the panel's run); USE-1 holds (molecular sarcoma typing,
Koelsche et al. 2021); USE-8 triggered, fixed (fit set to approximate: five confirmed types stand in for every
referred sarcoma); USE-5 holds for the reviewed label and is open on the MFS/UPS resolution (issue 3); LEAK-30 weak,
kept by the curator's decision of 2026-10-19 until the rebuild from GDC values, now written as a kept potential leak;
SPLIT-4 holds for IID by patient, open after the site finding (issue 4). Value: TP-8, synovial sarcoma (10 rows) kept by the curator's decision of 2026-10-12. Quality: CLEAN-3 triggered, fixed (61 SNP genotype probes dropped). Weighed: gap + (wide omics, multiclass), source + (pinned GDC label), use case + (published molecular sarcoma typing), size -. For the curator: issues 3 and 4.

**Main points:** Merge myxofibrosarcoma and undifferentiated pleomorphic sarcoma into one class (issue 3)? Keep the
random split by patient although one hospital gives half the rows (issue 4)?

**Record fields that disagree with the definition:**

- `problem_type`: record `Binary Classification`, definition `Multiclass Classification`.

**Record judgment:** valid. The label is TCGA's reviewed pathology diagnosis and the task a published diagnostic
practice; the record's assessment of 2026-10-20 calls the use case invented, which the panel refuted (Koelsche et al. 2021); the record's assessment of the panel run (2026-10-20) says so.

**Issues for Lennart:**

3. **Merge myxofibrosarcoma (MFS) and undifferentiated pleomorphic sarcoma (UPS) into one class?** Two of the five
   classes are diagnoses that the TCGA study, which supplies the label, finds "largely indistinguishable across
   multiple platforms" and analyses "as a single spectrum of disease". The DNA-methylation classifier used in
   diagnostics (Koelsche et al. 2021) also has one class for both. Pathologists tell them apart from the slide (the
   look of the tissue under the microscope), which this table does not hold.

   Effect on the task: a model cannot learn the distinction from these inputs, so a large share of the benchmark score
   measures a guess. Evidence: within the pair, ROC AUC 0.60-0.66 over three runs; a five-class random forest predicts MFS for none of the 51 MFS test rows (17 patients over three repeats); the pair is 30% of
   the rows and carries 51.5% of the forest's log loss; merged, the log loss falls from 0.650 to 0.461.

   Implemented: five classes, as the reviewed label (`short_histo`) has them, with the reason now written in the
   notes (the two leiomyosarcoma sites are merged because a lab knows before profiling whether the tumour sits in the
   uterus). Cost: about half the score rewards calibration on a near-chance pair. Alternative: one `UPS/MFS` class (61
   rows), the study's and the diagnostic classifier's convention; the probes are re-run. Cost: the task drops a
   distinction pathologists do make.

   Rule: USE-5 (Must, predict at the resolution the actor acts on) against TP-6 (Must, a valid task stays). The critic
   reads a USE-5 breach: the actor who uses molecular profiles acts on one class, and since the definition already
   builds the target (leiomyosarcoma merge, MPNST drop), TP-7 applies and the merge is a version the source defines.
   The advocate reads a weighing call: two distinct values of the reviewed field, and difficulty is no reason to change
   a task. The mediator: valid either way; the call turns on who the actor is. No precedent for merging two diagnoses that the label's source groups; audiology_diagnosis (2026-10-06) is the nearest TP-7 case, where our own merge was replaced by a field convention.

   Recommendation: merge, since the use case's actor is the lab running a molecular classifier and the facts lean
   that way (mediator). Decision: five classes, or four with MFS and UPS merged?

4. **Keep the random split by patient now that the hospital is weakly visible in the data?** TCGA collected the
   tumours at 31 hospitals ("tissue source sites"). One, Memorial Sloan Kettering, gave 101 of the 201 rows and 40 of
   the 50 dedifferentiated liposarcomas. In a random split by patient, test patients come from the same hospitals as
   the training patients, so a model can use a hospital's fingerprint in the measurements (from how it handled the
   tissue) as a hint at the type, because the type mix differs by hospital.

   Effect on the task: scores are optimistic for a lab whose patients come from other hospitals. Evidence: the
   mediator re-ran the check with the site codes matched to the right rows (the split audit's contrary result used mismatched codes and is void). That hospital against the rest, from the features: ROC AUC
   0.70-0.75 overall; 0.69-0.73 within dedifferentiated liposarcoma (95% of shuffled-label runs stay below 0.65);
   0.66-0.67 within soft-tissue leiomyosarcoma, at the edge; 0.61 within UPS, no signal. Holding whole sites out
   raises a random forest's log loss from 0.64 to 0.77 (mean of three seeds); ROC AUC 0.96 against 0.95.

   Implemented: IID by patient, stratified on the type, with a `splits_comment` that argues from the use case (a lab
   types new patients, one row each) and states the hospital's share as a known optimism. Cost: for a lab at a new hospital, scores read better than they would be (log loss 0.64 here against 0.77 with sites held out). Alternative: split by
   site. Cost: one site is half the rows, so the folds come close to a two-way test (that hospital against the rest)
   with unbalanced folds (1 to 161 rows).

   Rule: SPLIT-29 (Must: IID is wrong when many rows share an entity new data would not have and the entity carries
   the label) against SPLIT-4 (the split follows the application) and SPLIT-31 (an IID framing over related entities
   is a candidate for a grouped variant, not a fix). Precedent: glioma_grading kept IID because holding sites out
   changed nothing; that fact does not hold here, so the reason rests on the use case.

   Recommendation: keep IID with the comment (advocate, critic and mediator agree). Decision: IID by patient, or
   grouped by site?

**Review panel:** ship after changes (mediator). Claim audit: refuted the fit `direct`, "made from the tissue" for
the DDLPS label, "as in TabPFN-Wide ... histological type", the earlier MFS/UPS AUC of 0.73 and two record statements
(`problem_type`, "use case is invented"); the rest held (counts, checksums, the 20 relabels, MDM2 AUC 1.000). Blind
review: include with changes; main concern the undocumented label source (now documented). Agreed and applied: drop
the 61 `Methy_rs*` genotype probes, fit approximate, the label, leak and split notes, the MFS/UPS and leiomyosarcoma
reasons, the TabPFN-Wide citation. Settled by the mediator: the site is weakly visible within a type (the split
audit's site result was void and re-run). The precedent check's four consistency questions are answered: LEAK-30 wording (a, applied), DDLPS against coad's copy-number drop (a, the SEL-5 reason is written in the notes), MFS/UPS (issue 3), the site against glioma_grading (issue 4). To the curator: MFS/UPS (the mediator's issue 1, here issue 3) and the
split (the mediator's issue 2, here issue 4); the fit labels of other kept LEAK-30 datasets (the mediator's issue 3)
go to the working copy's REVIEW.md.

<details><summary>Mediator</summary>

Inputs: the phase-A reports, both briefs and rebuttals, `dataset.py`, README, record, the earlier REVIEW.md. One
experiment of my own.

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1 question closed by dropping the 61 Methy_rs* genotype columns; SEL-4 holds (histopathology label,
  not a cluster); SEL-5 not triggered (the 12q15 copy number that defines DDLPS is not shipped; best single-feature
  skill 0.075); USE-1 holds (published practice: Koelsche et al. 2021); USE-5 holds for the reviewed label,
  open on MFS/UPS resolution (issue 1); USE-8 triggered, fit -> approximate; LEAK-30 weak, kept by CC 2026-10-19
  with a `Potential leak, kept on purpose:` note (LEAK-5: "but no label" goes); SPLIT-4/SPLIT-29: IID by patient
  kept, site weakly visible within class (issue 2).
Value: TP-8 keep (CC 2026-10-12: SS 5% of test rows, 6.2-6.5% of RF log loss); TP-4 not met (skill +0.59).
Quality: CLEAN-3 drop 61 Methy_rs*; constant/duplicate drop fine (CLEAN-5).
Weighed: gap + (201 x 25,971 wide omics), source + (pinned GDC label), use case + (molecular sarcoma typing),
  size -.
For the curator: issue 1, MFS/UPS merge (USE-5 by the critic, a framing weigh by the advocate);
  issue 2, the split after the site fact; issue 3, fit precedents (consistency).
```

**Changes to make now (no decision needed)**

1. Drop the 61 `Methy_rs*` columns in `_clean` (germline SNP control probes, no class signal: best one-vs-rest AUC
   0.77 among 305 tests on 10 rows); say so in the Features bullet and carry it into the GDC rebuild. CLEAN-3; closes
   the SEL-1 question. Both sides agree.
2. `fit="approximate"`, reason: a closed set of five expert-confirmed types (the review's 80%, no desmoid, MPNST or
   uncertain case) on three omics stands in for a classifier facing all referred sarcomas; plus the kept LEAK-30.
   USE-8 (its text lists "a potential leak kept on purpose"; `fit_reason` already names two gaps). Both agree; see
   issue 3 for the precedents.
3. Rewrite the preprocessing bullet as `Potential leak, kept on purpose:` the source's >20%-missing filter and kNN
   imputation over all patients on every omic, and the 5,000 highest-variance methylation probes over all 269
   samples; kept per CC 2026-10-19 until the GDC rebuild, which should cover every block the imputation touched;
   drop "but no label". LEAK-30, LEAK-5; precedent lung_cancer_epithelial_genexp. Both agree.
4. Rewrite the Prediction-point and Label bullets: the review required 12q15 copy-number gain for every DDLPS (Cell
   2017 Methods; all 8 relabels in or out of DDLPS follow MDM2), the copy number is not shipped, `mRNA_MDM2` is its
   readout; replace "made from the tissue" and state the SEL-5 reason that sets it apart from coad. USE-5
   (documentation), SEL-5. Both agree.
5. Add a `splits_comment`: IID by patient, one row each, argued from the use case (new patients), not from "only" a
   small gap; site DX holds 101 of 201 rows and 40 of 50 DDLPS; the site is weakly visible within class (numbers
   below); site-grouped RF log loss 0.64 -> 0.77, a known optimism for a new lab. SPLIT-4, SPLIT-31. Both agree on
   the form; the wording follows issue 2 if the curator changes the regime.
6. Write why STLMS+ULMS are merged (uterine or soft-tissue origin is known before profiling, nobody predicts it;
   the clinical file's convention) and that MFS vs UPS is near chance from these inputs (AUC 0.60-0.66). TP-7, USE-5.
   Needed whichever way issue 1 goes.
7. Corrections (writing.md, EV-2, EV-7): REVIEW's "AUC about 0.73" -> 0.60-0.66 (three runs); "as in TabPFN-Wide"
   -> "subtype classification (Sec. 5, Table A1)", the paper does not name the column; record `problem_type` ->
   Multiclass Classification; the next record assessment drops "its use case is invented" (refuted, Koelsche 2021);
   optionally name that practice in `use_case` instead of "For example".

**Issues for the curator**

**1. P3, USE-5 (Must) against TP-6 (Must, P6): merge MFS and UPS into one `UPS/MFS` class (61 rows)?**
* Problem and effect: within the pair, RF 0.597-0.624, L2 logistic 0.663; the 5-class RF predicts MFS for 0 of 51
  MFS test rows; MFS+UPS carry 51.5% of the RF log loss with 30% of the rows; merged, log loss 0.650 -> 0.461.
* Critic: USE-5 asks for the resolution the actor acts on; the actor here uses molecular profiles, the DKFZ
  methylation classifier has one class for both, the label's own source analyses them "as a single spectrum"; the
  definition already builds the target (LMS merge, MPNST drop), so TP-7 applies and the merge is a version the
  source defines (TP-6).
* Advocate: MFS and UPS are distinct values of the reviewed field `short_histo`; pathologists name them apart; a
  weak real signal is difficulty, not invalidity (the score never decides, "right split against the score"); MFS's
  share of the loss (21% for 8.5% of rows) sits within kept TP-8 cases.
* My reading: not a conflict the ranking settles. Whether USE-5 is breached turns on who the actor is (the molecular
  classifier user, who acts on one class, or the pathologist, who names two from morphology the table lacks): a
  framing call. The task is valid either way; the critic's facts lean toward the merge.
* Decision: five classes (with change 6 as the written reason) or four (merge, re-run the probes, TP-7). What would
  settle it: whether the use case's actor acts on MFS vs UPS from a molecular result.

**2. P4, SPLIT-1/SPLIT-29 (Must): IID by patient now that the site is shown to be weakly visible.**
* Fact settled (below): the split audit's "site not visible" (AUC 0.46-0.52) came from site codes misaligned with
  the shuffled frame (1 of 201 rows right); its cross-site table is void too. Correctly aligned, DX vs rest is
  learnable overall (RF 0.70, logistic 0.75, null 0.53) and weakly within type (DDLPS 0.69-0.73 against a null 95%
  of 0.65; STLMS 0.66-0.67, at the null's edge; UPS 0.61, null). The claim audit's LMS 0.773 is mostly uterine vs
  soft tissue (DX has none of the 27 ULMS). The site also carries the class mix (DDLPS 40% of DX rows, 10% elsewhere).
* Both sides: keep IID with a `splits_comment` (SPLIT-31 candidate for a grouped variant); the patient is the unit,
  a lab types new patients; one site is half the rows, so a grouped split is close to a two-domain test (splits.md
  "Only a few groups").
* Against: SPLIT-29 needs an entity new data would not have that carries the label; a TCGA model used at a new
  hospital meets a new site. Measured cost: RF log loss 0.64 IID vs 0.77 mean site-grouped (0.91 DX vs rest), AUC
  0.96 vs 0.95.
* Decision: (a) IID with the comment (recommended default, both sides); (b) site-grouped. It departs from
  glioma_grading's reason (there holding sites out changed nothing), so the comment must rest on the use case.

**3. Consistency, USE-8: fit labels of kept LEAK-30 datasets.** Change 2 follows USE-8's text, but
lung_cancer_epithelial_genexp, bioresponse and other LEAK-30 keeps are `direct`, and glioma_grading and ljubljana are
`direct` with a named gap; only kick applied "a potential leak kept on purpose = approximate". One of the two is wrong:
(a) keep sarcoma approximate and reopen those labels; (b) amend USE-8 to say a weak LEAK-30 keep does not by itself
make a fit approximate (sarcoma would then still be approximate on the closed five-type set).
*Answered by rule (2026-10-21, Lennart):* USE-8 amended as (b): a kept potential leak does not by itself make a fit
approximate. Sarcoma stays approximate on the closed five-type set; `fit_reason` no longer counts the kept
preprocessing as a reason for the fit.

**Agreed facts**

* 201 patients, one primary tumour (type 01) each; 25,971 features (20,154 mRNA, 5,000 Methy incl. 61 `rs` SNP
  probes, 817 miRNA); classes 80/50/44/17/10; every class in every test fold (SS 3-4).
* Label: TCGA 2017 reviewed `short_histo` from the pinned GDC file (md5 re-measured); 20 reclassified; MPNST (5)
  dropped; STLMS+ULMS merged. Source zips re-downloaded, md5s match.
* Task is real (molecular sarcoma typing, Koelsche 2021); not an SEL-4 cluster label.
* DDLPS: `mRNA_MDM2` alone AUC 1.000; the review required 12q15 copy-number gain; copy number not shipped; best
  single-feature skill for the task 0.075. SEL-5 not triggered; wording needs fixing.
* Source preprocessing over all patients (kNN imputation, >20%-missing filter, methylation variance filter):
  weak LEAK-30, kept by CC 2026-10-19 pending the GDC rebuild. mRNA (RSEM UQ) and miRNA (RPM) are per-sample.
* No copies across the split, no hidden groups, no leak flag; RF log loss 0.65 against 1.41 for the prior, logistic
  0.50, LightGBM 0.54.
* MFS vs UPS 0.60-0.66 within the pair; "0.73" not reproduced.
* fit should read approximate; record `problem_type` and "use case is invented" are wrong.
* Width and raw scale are no reasons to change anything (CLEAN-22, coad 2026-10-15).

Disputed fact settled (EV-1): is the site visible within class? Re-run with barcodes matched to the split frame on
feature values (the split audit's positional mapping matched 1 of 201 rows, DX had 29
DDLPS instead of the true 40). DX vs rest, 5-fold CV, 3 seeds, log1p on mRNA/miRNA:

| Rows | n (DX) | RF AUC | L2 logistic AUC | permuted null |
|---|---|---|---|---|
| all | 201 (101) | 0.700 | 0.749 | RF 0.533 |
| LMS (STLMS+ULMS) | 80 (23) | 0.715 | 0.726 | RF 0.492 |
| STLMS only | 53 (23) | 0.656 | 0.671 | LR mean 0.483, 95% 0.663 |
| DDLPS | 50 (40) | 0.692 | 0.733 | LR mean 0.485, 95% 0.647 |
| UPS | 44 (20) | 0.611 | 0.611 | LR mean 0.497, 95% 0.634 |

Answer: weakly, yes (DDLPS clearly, STLMS borderline, UPS not). Neither audit's numbers stand as written.

**Consistency with precedent (precedents.md)**

| Item | Recommendation | Precedent |
|---|---|---|
| SS keep (TP-8) | keep | follows ljubljana, mic, forensic_glass; unlike alvin (51-54% of loss) |
| LEAK-30 note | reword | follows lung_cancer_epithelial_genexp; coad retirement predates the 2026-10-19 amendment |
| Reviewed label (USE-5) | keep | follows corporate_credit_rating, consumer_complaints |
| DDLPS (SEL-5) | keep, reason written | departs from coad's copy-number drop; fact: the defining measurement is absent (as coad's MSI) and the task is no rule |
| MPNST drop | keep | follows ljubljana, ecoli_proteins (<10) |
| MFS/UPS vs STLMS/ULMS | issue 1, change 6 | no precedent; audiology_diagnosis for TP-7 |
| IID with a dominant site | issue 2 | follows glioma_grading in form; the fact that set glioma apart (site invisible) does not hold here |
| fit approximate | change 2, issue 3 | follows kick and USE-8's text; departs from lung_cancer, bioresponse, glioma_grading, ljubljana |
| Not SEL-4 | keep | distinct from brca/gbm/ov (cluster labels) |

</details>

<details><summary>Claim audit</summary>

Definition `datasets/_dev/tabarena-v0pt2/sarcoma/dataset.py` (D), record `curation/records/sarcoma.md` (R), claims list
the panel's claims list (numbers below). Data loaded through the definition's own `_load_raw`/`_clean` and its
splits (shipped split frame mapped back to patients: 201/201 rows matched, values identical).

Sources read as text: Rappoport & Shamir 2018 (NAR, full text via Europe PMC) and its Supplementary File 1 (OUP
archive); `benchmark.R` of Shamir-Lab/Multi-Omics-Cancer-Benchmark; TCGA Cell 2017 (PMC5693358, Pathology review,
Results); TabPFN-Wide arXiv 2510.06162v1 (HTML); Crossref for both DOIs; the benchmark download page; Koelsche et al.
2021 (Nat Commun 12:498, bibliographic record only).

**Table**

| # | Claim (where) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1 | question: type of soft-tissue sarcoma from molecular profiles (D task_summary) | read features and target | holds | 3 omic blocks, 5 histotypes | USE-1 |
| 2 | use_case: a molecular pathology lab types a sarcoma from expression + methylation profiles (D) | look for the practice outside TabPFN-Wide | holds (refutes R's "use case is invented", claim 62) | Koelsche et al. 2021, "Sarcoma classification by DNA methylation profiling", Nat Commun 12:498: a methylation classifier for diagnostic sarcoma typing (bibliographic record; text not read, EV-2 rank 2-4) | USE-1, USE-9 |
| 3 | TabPFN-Wide uses the task as a benchmark (D) | read arXiv 2510.06162v1 | holds, imprecise | Sec. 5: "BRCA, SARC and GBM by Rappoport & Shamir (2018)", "cancer subtype classification"; Table A1: SARC 259 patients, all 26,577 features (not our 201 x 25,971); label column not named in the text | EV-2 |
| 4 | row: primary tumour of one patient whose type experts confirmed (D) | sample-type codes, master table join | holds | only type 01 kept; 206 of 206 master patients are among the 257 with all omics; one row per patient (asserted, 0 duplicate rows) | LEAK-16 |
| 5 | 201 patients; period not stated (D) | count | holds | 201 rows | - |
| 6 | 5 classes, LMS 40%, SS 5% (D) | value_counts | holds | 80/50/44/17/10 = 39.8% ... 5.0% | - |
| 7 | 25,971 measurements (D) | shape | holds | 20,154 mRNA + 5,000 Methy + 817 miRNA | - |
| 8 | split: random patients stand for new patients' tumours (D) | site hold-out (claim 39) | holds with a note | see 39 | SPLIT-4, USE-10 |
| 9, 25 | source is a clustering benchmark without a label (D) | NAR text, benchmark.R | holds | the benchmark scores clusterings by survival and clinical enrichment; no label shipped in `sarcoma.zip` (exp, methy, mirna, survival) | PROV-1 |
| 10, 27 | reviewed type replaces the submitted diagnosis (D) | code + master table | holds | `short_histo` from the pinned GDC file (md5 42146699371fd1582f8f04c05a03f8f5, re-measured) | USE-5 |
| 11, 31, 44 | 5 MPNST dropped; STLMS+ULMS -> LMS (D) | crosstab | holds | MPNST 5; STLMS 53 + ULMS 27 = 80, all submitted as "Leiomyosarcoma (LMS)" | TP-5 |
| 12 | fit = "direct" (D) | USE-8 against fit_reason's own text | **refuted (contested)** | fit_reason names two known gaps ("test tumours are cleaner than a lab's", "few labs measure all three profiles"), and D keeps a transductive preprocessing (claim 36); USE-8: "Approximate: a stand-in with a known gap, named as such ... a potential leak kept on purpose". Precedents split: lung_cancer_epithelial_genexp (RMA, kept) and bioresponse (scaling, kept) are `direct`; kick is `approximate` | USE-8 (Must) |
| 13 | the profiles exist before the typing (D fit_reason) | Cell 2017 STAR Methods, Pathology review | holds in time, **misleading in substance** | the reviewed typing was done after profiling and used the study's molecular data: "All cases diagnosed as DDLPS were required to have evidence of increased chromosome 12q15 copy number", "confirmed by copy number analysis"; reclassification on "focal chromosome 12q~15 amplification" | USE-3, USE-5 |
| 14, 23 | label is the reviewed pathology diagnosis, "made from the tissue" (D) | relabelled cases against MDM2 mRNA | **refuted in part** | the 8 review relabels into or out of DDLPS follow MDM2 exactly: 4 into DDLPS at MDM2 16,691-57,949, 4 DDLPS->UPS at 597-3,813; every reviewed DDLPS >= 9,095, every other class <= 4,541; under the submitted label the same feature gives 0.936. The DDLPS label is the study's copy-number rule, not histology alone | USE-5, SEL-5 (not triggered: the rule's input, copy number, is not shipped) |
| 15 | study left out uncertain cases (D) | Cell 2017 | holds | "After review, 31 of the 237 cases were excluded"; "Five cases were excluded as not being sarcoma, including 3 probable melanomas" | - |
| 16 | few labs measure all three profiles (D) | none cheap | untested | inference (EV-2 rank 5) | - |
| 17 | year 2018, domain, source "Other" (D) | page, files | holds | zips Last-Modified 16 Jul 2018; NAR 2018 | PROV-8 |
| 18 | licence string (D) | page | holds | footer "© All rights reserved"; GDC open-tier terms not re-read (licence is never evidence, EV-4) | EV-4 |
| 19 | md5s, dates, commands (D download_description) | re-download both zips | holds | md5 sarcoma.zip caa80f17..., clinical.zip bf06f12b... match; the unzipped exp/methy/mirna/clinical match the local raw files byte for byte; Last-Modified 2018-07-16 12:24 / 12:34 GMT | PROV-9 |
| 20 | bibtex (D) | Crossref | holds | both DOIs resolve to the stated title, volume, issue, pages, year | EV-7 |
| 21, 26 | target, multiclass, log loss (D) | metadata | holds | - | EV-5 |
| 22 | inputs: exp, methy (450k), mirna, clinical, master table (D) | files | holds | methy probe ids are `cg...` 450k ids | - |
| 24, 37 | "as in TabPFN-Wide (Sec. 5)": histological type, IID (D; R claim 54) | paper text | **partly unverified** | the text says "cancer subtype classification" and "3-fold cross-validation repeated 3 or 10 times"; `histological_type` is not named (the record cites their download instructions, not read) | EV-2, EV-7 |
| 28 | review confirmed 206, excluded others, reclassified 20 (D) | crosstab submitted x reviewed over the 206 | holds | 4 into DDLPS, 5 into MFS, 11 into UPS = 20; paper: "20 were reclassified" | - |
| 29, 30 | 257 patients with all three omics; restricted to 206 (D) | intersection | holds | 257; 206 of them reviewed, 51 not | - |
| 32 | class counts, SS 3-4 per test fold (D) | splits | holds | every test fold holds every class; minimum 3 | TP-5, TP-8 |
| 33 | study: MFS and UPS "largely indistinguishable across multiple platforms"; kept apart as pathologists do (D) | quote; separability | quote holds; **the earlier REVIEW.md's "separates them at about AUC 0.73" not reproduced** | MFS vs UPS within the pair, 5 x 3-fold CV: RF 0.624, L2 logistic 0.663; 5-class RF (3 shipped repeats) predicts MFS for 0 of 51 MFS test rows (44 as UPS); MFS carries 21.0% of the log loss with 8.5% of the rows, MFS+UPS 51.5% with 30.4% | TP-7, USE-5 (weighing) |
| 34 | prefixes, `make.names`, values as shipped (D) | columns, value checks | holds | `mRNA_X..100130426`; mRNA per-sample upper quartile of non-zero values = 1,000 (5-95%: 999.2-1,000; RSEM normalised per sample), miRNA per-sample sums = 1e6 (RPM), Methy in [0.006, 0.995] (beta): per-row transforms, fine under LEAK-30 | LEAK-30 |
| 35, 48 | constant and duplicated columns dropped (D) | counts | holds | 26,577 -> 25,971 (606 dropped) | CLEAN |
| 36 | benchmark preprocessing over all patients, label-free (D) | Supplementary File 1, benchmark.R | holds; **note form departs from LEAK-30** | Suppl. File 1 "Early Preprocessing": "patients and features with more than 20% missing values were removed, and missing values were imputed using k nearest neighbor imputation ... For methylation data, we selected the 5000 features with maximal variance in each dataset" (methy file: exactly 5,000 rows over 269 samples incl. normals and metastases). `benchmark.R` applies its own log/z-score only at run time, not in the files. D writes it as a plain "Note:", not as `Potential leak, kept on purpose:` with the curator's keep (CC 2026-10-19), as LEAK-30 and the precedents (lung_cancer_epithelial_genexp, bioresponse) do. Share of imputed values: untested (no raw values) | LEAK-30 (Should, weak), LEAK-29 n/a |
| 38 | one site holds 101 of 201 (D) | barcode TSS | holds | DX (MSKCC) 101; 31 sites; DX holds 40 of 50 DDLPS and 13 of 17 MFS | SPLIT-30 |
| 39 | site hold-out: RF 0.954 -> 0.947 AUC, log loss 0.66 -> 0.76 (D) | RF 500 trees, shipped IID (5 repeats) vs StratifiedGroupKFold on TSS (3 seeds), DX vs rest | holds approximately | IID 0.960 / 0.643; site-grouped 0.942 / 0.854, 0.957 / 0.675, 0.951 / 0.779 (mean 0.950 / 0.769); train on non-DX, test DX and back: 0.927 / 0.910. Site is learnable within class (RF CV AUC DX vs other: LMS 0.773, DDLPS 0.706; MFS, UPS, SS <= 0.5). "only" is a reading: log loss +20% | SPLIT-4, SPLIT-30, USE-10 |
| 40-43 | rule leaves of DDLPS; review typed by 12q~15 amplification; MDM2 alone AUC 1.000; kept (D) | AUC; Cell quote | holds | AUC 1.000 re-measured; Results: "MDM2 amplification was present in all DDLPS by definition" | PROV-3 reading 2, SEL-5 |
| 45, 46 | barcode parsing, asserts (D) | run | holds | asserts pass; patients with 02/06/11 samples (6/8/4) correctly reduced to 01 | - |
| 47 | decision table pairs both labels for the 257 (D) | rerun | holds | as above | - |
| 49 | IID default, no splits_comment (D) | metadata | holds | 20 x 3 | - |
| 50 | 0 errors, 0 warnings (checklist) | not re-run | untested here (verifier ran it) | - | EV-7 |
| 51 | R `problem_type: Binary Classification` | compare | **refuted** (record wrong) | definition and data: 5 classes | writing.md |
| 52-56 | R comments and 2026-10-07 assessment | as 11, 24, 28 | hold, except 54 (column name unverified in the paper text) | - | - |
| 57 | UPS/MFS one spectrum (R) | Cell | holds | "Taking UPS/MFS as a single spectrum of disease" | - |
| 58 | CC 2026-10-12: SS 6.5% of RF log loss (R) | per-class log loss shares | holds | 6.2% (3 repeats, 500 trees) | TP-8 |
| 60 | CC 2026-10-19: rebuild methylation from GDC beta values later (R) | - | not a claim to test; consistent with 36 | - | PROV-13 |
| 62 | R: "its use case is invented" | as 2 | **refuted** | a published diagnostic practice exists (Koelsche 2021) | USE-1 |

Unwritten claims the definition implies:

| Implied claim | Test | Result | Rule |
|---|---|---|---|
| Every feature is known at the prediction point | prediction point = tumour profiled; label rule | holds for the features (all three omics are measured on the tumour); the label, not a feature, carries molecular information (row 14) | LEAK-10, USE-3 |
| No row is a copy across the split | duplicates, one row per patient | holds: 0 duplicate rows, asserted unique patients, probe: 0% near-copy clusters | LEAK-16 to LEAK-21 |
| The split is the one the use case needs | site hold-out | holds as a reading; a lab is a new site, and site-grouped scores lose 0.01 AUC and +0.13 log loss; DX confounds DDLPS and MFS | USE-10, SPLIT-30 |
| The target is the real-world target | review rule; MFS/UPS | partly: DDLPS = the copy-number rule (clinical practice uses MDM2 amplification too); MFS vs UPS barely separable (0.62-0.66) and half the log loss | USE-5, TP-7 |
| No transform uses the test rows | Suppl. File 1 | refuted, weak: kNN imputation and the methylation variance filter over all 269 samples (claim 36) | LEAK-30 |

**Refuted and untested, ranked (validity first, Must first)**

1. **P3, USE-5 (Must) / USE-3: the label is partly the study's copy-number rule, not "made from the tissue" (claims
   14, 23; implied by 13).** The review required 12q15 copy-number evidence for DDLPS; all 8 relabels in or out of
   DDLPS follow MDM2 mRNA (gap 4,541 to 9,095). Changes: no feature has to go (SEL-5 is not triggered: copy number is
   not shipped), but the definition's wording and the "direct" reading rest on it, and MDM2 expression is a near
   proxy of the label rule. The real-world target survives because diagnostic practice also uses MDM2
   amplification. Mildest remedy: rewrite the Prediction-point and Label bullets ("the reviewed type, by histology,
   immunophenotype and, for DDLPS, the study's 12q15 copy number, which is not shipped") and keep; a curator note,
   not a fix.
2. **P3, USE-8 (Must): fit "direct" against fit_reason's own named gaps and a kept transductive preprocessing
   (claim 12).** Changes: the fit field. Mildest remedy: `fit="approximate"` with the gaps as the stand-in; or, if the
   curator follows the lung_cancer_epithelial_genexp / bioresponse precedent (direct with a kept LEAK-30 note), say
   so in the record as the consistency answer. Weighing call for the curator.
3. **P4, LEAK-30 (Should, weak): the kept all-row preprocessing lacks the `Potential leak, kept on purpose:` note
   (claim 36).** The fact holds (Suppl. File 1 quoted above). Changes: documentation only. Mildest remedy: turn the
   Note bullet into `Potential leak, kept on purpose: ... Kept (Lennart, 2026-10-19) until the GDC rebuild`. The size
   of the kNN imputation is untested (needs the GDC per-sample values, the deferred rebuild).
4. **P3/P6, USE-5 / TP-7 (weighing): MFS vs UPS (claim 33; the earlier REVIEW.md, issue 3's "AUC 0.73" not reproduced).**
   Measured 0.624 (RF) and 0.663 (L2 logistic) within the pair; the 5-class RF never predicts MFS; MFS+UPS carry 51.5%
   of the RF log loss with 30% of the rows. Changes: the issue's number. Mildest remedy: correct the number in
   REVIEW.md; the merge stays the curator's call (classes are the source's, so TP-7 does not force it).
5. **Procedure, EV-2/EV-7: "as in TabPFN-Wide ... histological type" (claims 24, 54) unverified in the paper text**,
   which says "cancer subtype classification" on 259 patients and 26,577 features. Remedy: cite "subtype
   classification (Sec. 5, Table A1)" or the source of `histological_type` (their download instructions).
6. **Procedure: record `problem_type: Binary Classification` (claim 51)** is wrong; set to Multiclass.
7. **Record: "its use case is invented" (claim 62)** is refuted by a published diagnostic practice (Koelsche et al.
   2021); remove or soften in the next assessment.
8. **Untested:** claim 16 (few labs measure all three profiles; inference), the share of kNN-imputed values (claim
   36), GDC open-tier licence wording (claim 18; EV-4, never decisive), `dataset check` (claim 50; run by the
   verifier, not here).

Held under attack (selected): counts and class shares, md5s and dates (re-downloaded), reclassified 20, site claim
(0.950 / 0.769 mean over three site-grouped seeds against the stated 0.947 / 0.76), MDM2 AUC 1.000, per-sample
normalisation of the shipped mRNA and miRNA, no copies across the split.

</details>

<details><summary>Column audit</summary>

Frame: `dataset_io.load("sarcoma", ..., built=True)` (origin `rebuilt`), 201 rows x 25,972 columns: 25,971 float64
features (mRNA 20,154; Methy 5,000; miRNA 817), target `histological_type` (category, 80/50/44/17/10). No missing
values.

Prediction point (curation_comments bullet 1): a primary soft-tissue sarcoma has been profiled on the three platforms;
the model assigns the histological type. Every feature is a measurement of the primary-tumour sample (TCGA type 01),
taken from the resected tissue before the typing. No clinical, site, plate or barcode column is in the frame.

Codebook: none per column. The source (Rappoport & Shamir 2018) ships TCGA level-3 matrices; meanings below are from
the TCGA formats and measured on the frame.

**Column table**

| Column (group) | Meaning | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `mRNA_<symbol>.<Entrez>` (20,154) | TCGA RNA-seq RSEM gene expression, upper-quartile normalised per sample (row UQ 709-897, i.e. the per-sample UQ=1000 scaling over all genes; row sums 1.7e7-3.2e7); 0 to 3.2e6, 14% zeros, not logged | yes, tumour measurement | float64, values as shipped; per-row normalisation is fine; no transform needed (pipeline's job) | fine | LEAK-30 (per-row: fine), CLEAN-2 |
| `mRNA_X..<Entrez>` (26) | genes TCGA lists with symbol `?`, which R's `make.names` turned into `X.`; meaning = the Entrez id | yes | float64; the name is ugly, the column is fine | fine (cosmetic) | CLEAN-3 n/a |
| `mRNA_SLC35E2.9906`, `mRNA_SLC35E2.728661` | two Entrez genes with one symbol | yes | not copies (duplicate-column drop kept both) | fine | CLEAN-5 |
| `mRNA_MDM2.4193` | MDM2 expression | yes | float64 | fine, but see problem 3: one-vs-rest ROC AUC 1.000 for DDLPS (re-measured); CDK4 0.950, FRS2 0.971 | LEAK-37, CLEAN-22 |
| `mRNA_TLE1.7088`, `mRNA_CUX2`, `mRNA_LHX3`, `mRNA_NEU4`, `mRNA_TMEM59L` ... | synovial-sarcoma expression program (TLE1 is the diagnostic IHC marker) | yes | float64 | fine; 117 features have AUC >= 0.99 for SS (10 rows), 1,181 >= 0.95; not singled out by any probe | TP (note) |
| `mRNA_RBPMS.11030` (top single feature, leak probe) and the other top-300 singles | smooth-muscle and other lineage genes (MYLK, SYNPO2, CNN1, ACTG2, MYOCD) | yes | float64 | fine: best single 0.824, a lineage signal, not a give-away | LEAK-10 holds |
| `Methy_cg<id>` (4,939) | Illumina 450k beta value of one CpG (0.006-0.995) | yes | float64; the source kept the 5,000 probes of highest variance over all sarcoma patients and kNN-imputed over all patients (label-free) | leak, weak (transductive): keep with a `Potential leak, kept on purpose:` note; rebuild from GDC betas (CC 2026-10-19, deferred) | LEAK-30 (Should, weak) |
| `Methy_rs<id>` (61) | the 450k array's SNP genotyping control probes: germline genotype of the patient, not methylation (values tri-modal, about 1/3 each near 0, 0.5, 1); they entered via the variance filter | yes | float64; an identifier-like patient fingerprint, no tumour-type meaning; max one-vs-rest AUC 0.61-0.77 over 305 tests (noise level, SS 0.768 on 10 rows); pairwise genotype concordance max 0.64 (no repeated patient) | cleaning problem + question (P1): drop the 61 columns | CLEAN-3; SEL-1 question |
| `miRNA_hsa.<name>` (817) | TCGA miRNA-seq reads per million per precursor (row sums exactly 1e6), 45% zeros | yes | float64; per-row RPM is fine | fine | LEAK-30 (per-row: fine) |
| sparse columns (146 mRNA, 58 miRNA nonzero in <= 2 rows) | genes/miRNAs almost never expressed | yes | not constant over the 201 rows, so CLEAN-5 keeps them | fine | CLEAN-5, CLEAN-22 |
| dropped: constant and duplicated columns | zero-only genes/miRNAs, exact copies | n/a | dropped over the 201 shipped rows; a column choice by the whole table is ordinary cleaning | fine | CLEAN-5, CLEAN-8 |
| `histological_type` (target) | TCGA 2017 expert-review `short_histo`, STLMS+ULMS merged, MPNST dropped | label | category, 5 levels, no missing | fine; see problem 3 on how the DDLPS label was made | USE-5, CLEAN-15, CLEAN-17 |
| barcode, clinical columns | patient id; submitted histology | n/a | not in the frame (index dropped; clinical only for the decision table) | fine | CLEAN-3, LEAK-10 |

**Problems, ranked (principles.md order)**

1. **P1/P7: `Methy_rs*` are 61 germline SNP genotypes, not methylation (CLEAN-3 Should; SEL-1 question).**
   Evidence: 61 of the 5,000 raw `methy` rows are `rs` ids (the 450k's genotyping controls, used for sample
   identity QC); values cluster at 0 / 0.5 / 1 like genotype calls; they carry no class signal (best one-vs-rest AUC
   0.77 on the 10 SS rows among 305 tests). They identify the person, not the tumour; with one row per patient they
   do not leak across the split (no pair of rows shares a genotype). Question for the curator: germline genotype is
   TCGA's controlled-access category, even though the level-3 450k files carried these probes openly. Mildest remedy:
   drop the 61 columns in `_clean` (no loss of signal) and say so in the Features bullet; do the same in the planned
   GDC rebuild (GDC betas also include `rs` probes).

2. **P4: the methylation block's variance filter and kNN imputation used all patients (LEAK-30, Should, weak).**
   Evidence: claim 36; CC 2026-10-19 defers the rebuild; leak_checks.md's LEAK-30 Cases already list "sarcoma's
   methylation (next pass)". The definition says "uses all patients but no label" but lacks the
   `Potential leak, kept on purpose:` note LEAK-30 asks for (grep of the folder and record: none). Imputation over all
   rows also touches the mRNA/miRNA blocks (the benchmark's >20%-missing filter and kNN step ran on every omic).
   Remedy: reword the Note bullet as a `Potential leak, kept on purpose:` note until the GDC rebuild; no data change.

3. **P3/P4 question (already open, the earlier REVIEW.md, issue 2): the DDLPS label was made with TCGA's own copy-number data
   of the same tumour.** Evidence: Cell 2017 Methods: "All cases diagnosed as DDLPS were required to have evidence of
   increased chromosome 12q15 copy number ... confirmed by copy number analysis"; reclassification used "presence or
   absence of focal chromosome 12q~15 amplification". `mRNA_MDM2.4193` is downstream of that amplicon (AUC 1.000).
   Not a leak: the defining measurement (copy number) is not a feature, so CLEAN-22's "measurement that defines the
   label" does not reach the mRNA column, and a lab has MDM2 FISH/expression at the typing (LEAK-37). Remedy: none for
   the columns; sharpen the curation_comments note from "typed these tumours by" to "required 12q15 copy-number gain"
   so the curator sees the label is partly molecular. Related, not a leak: synovial sarcoma is separated perfectly by
   117 single genes (TLE1 and the SS18-SSX program), so two of five classes are near-deterministic and the task's
   difficulty sits in LMS/UPS/MFS (feeds the MFS/UPS question, the earlier REVIEW.md, issue 3).

4. **P7, cosmetic: 26 `mRNA_X..<Entrez>` names** come from TCGA's `?` symbol through `make.names`. Fine as is; a
   rename to `mRNA_unknown.<Entrez>` is optional.

No post-outcome column, no outcome-caused missingness, no id encoding the label, no copies across the split, no
proxy-missing or impossible values (mRNA >= 0, miRNA RPM rows sum to 1e6, betas in (0, 1)). Dtypes are right.

Sources: Cell 2017 TCGA SARC Methods, https://pmc.ncbi.nlm.nih.gov/articles/PMC5693358/

</details>

<details><summary>Split audit</summary>

Note: the mediator found this report's site-visibility runs and its cross-site table void (site codes matched to the wrong rows) and re-ran them; see the Mediator section.

Definition `datasets/_dev/tabarena-v0pt2/sarcoma/dataset.py`; IID, 20 repeats x 3 folds, stratified on the target
(134 train / 67 test; every class in every test fold, synovial sarcoma 3-4).
Frame loaded through the definition, barcodes from `_clean`.

**Verdict: right with notes**

**Regime the use case implies**

* One prediction = one patient's primary tumour, typed once from its omic profiles (prediction point stated in
  `curation_comments`). The deployed model types tumours of *new patients*; each patient is one row (asserted in
  code), so a split by patient is the grouped split at the true entity and IID by row is the same thing (SPLIT-1,
  SPLIT-23).
* Not temporal: no time column, and a tumour-typing classifier is not a stream; the TCGA cohort is a cross-section
  collected 2000s-2015 with no ordering meaning for the label (SPLIT-6/7 do not apply; no label delay).
* Hidden groups: probe clean (0 candidates, no composite key, 0.0% rows in near-copy clusters at 0.7-0.9); exact copies
  across the split 0.0% (leak probe). SPLIT-29/30 not triggered.

**The one candidate group: tissue source site (TSS, barcode chars 6-7)**

31 sites; DX (Memorial Sloan Kettering) holds 101 of 201 rows, 3B 16, the other 29 sites 1-8 each.
Class mix differs mildly (DX: LMS 34%, DDLPS 29%, UPS 22%, MFS 9%, SS 7%; other 29 sites: LMS 49%, DDLPS 21%, UPS
21%, MFS 6%, SS 2%).

Re-run (random forest, 500 trees, raw features):

| Split | macro ROC AUC | log loss |
|---|---|---|
| Shipped IID, first 9 splits (134 train) | 0.963 | 0.638 |
| Random 101 train / 100 test (5 draws, size-matched) | 0.954 | 0.695 |
| Train DX (101) -> test the 30 other sites (100) | 0.959 | 0.644 |
| Train the other sites (100) -> test DX (101) | 0.966 | 0.719 |
| StratifiedGroupKFold by site, 3x3 (pooled LL; folds unbalanced 1-161 rows) | n/a | 0.734 |

Is the site visible in the features? RF predicting DX vs the rest from the 25,971 omic features, 5-fold CV: AUC
0.458 overall, 0.520 within LMS, 0.474 within DDLPS, 0.381 within UPS, i.e. no site batch signature after the
benchmark's preprocessing. A model cannot recognise the site, so an IID split cannot reward site recognition
(SPLIT-29's condition "the entity carries the label" fails in the only way that matters). The size-matched cross-site
scores equal the random ones. The claim in `curation_comments` (RF 0.954 -> 0.947, LL 0.66 -> 0.76) is consistent
with this in direction and size; not reproduced to the digit (different fold construction). With one site holding half
the rows a site-grouped split is a two-domain shift test (splits.md "Only a few groups"), not a better mirror of the
use case.

**Problems, ranked (principles.md)**

1. **P4, note (SPLIT-1, USE-10; definitions.md "set `splits_comment` only when there is something to say").** The
   site analysis that justifies keeping IID sits in `curation_comments`; the class has no `splits_comment`, so the
   README's split section reads "Default splits." while there is something to say (DX = half the rows). Remedy:
   mildest, a `splits_comment` of one or two sentences restating "IID over patients (one row each); one site holds
   101 of 201 rows, its rows are not distinguishable from the features (RF AUC 0.46) and cross-site scores match
   random ones". No re-split.
2. **P4, note (LEAK-27 to LEAK-31; touches the split).** The source's kNN imputation and 5,000-probe variance
   selection used all 201+ patients, test rows included, label-free. This is the weak transductive kind; it does not
   change which rows are in which fold, and the curator deferred the rebuild (CC 2026-10-19). The leak auditor owns
   it; for the split it only means the test rows are not fully out-of-sample in feature construction. Remedy: as
   decided, the GDC beta-value rebuild; meanwhile a `Potential leak, kept on purpose:` phrasing per principles.md.
3. **P3/P4, note (USE-2, not a split fault).** The test population is the TCGA-reviewed, uncertain-cases-removed
   cohort, cleaner than a lab's intake (fit_reason says so). No split can fix this; it belongs to the fit label
   (`approximate` question raised by the checklist), not to the split.

No problem with the regime, the stratification, copies across folds, or the repeats (repeats draw different test
sets: checked repeat 0 vs 1).

</details>

<details><summary>Domain practitioner</summary>

Actor taken: a molecular pathologist at a sarcoma reference centre who runs a molecular classifier on a soft-tissue
sarcoma after the H&E/IHC work-up, to support or overturn a hard diagnosis (the use case in `task_summary`).
Own runs: random forest, 500
trees, 3-fold stratified CV, 3 seeds; same features and rows as `_clean`).

**Fit: approximate (not the declared direct)**

The decision is real (typing a sarcoma from molecular profiles, label = expert pathology diagnosis, one tumour per
row, unseen patients), but the data stand in for it with named gaps: a closed set of five types over the cleanest
80% of cases, at a resolution (MFS vs UPS) that the molecular tools in use do not resolve. `fit_reason` already
names two gaps, which under USE-8 is the definition of approximate; USE-9 offers no other use case that removes
them without rephrasing only to excuse the gap (weighed factor).

**The four questions, as the actor**

1. **Inputs at the prediction point (USE-3, USE-6).** I have a methylation array of the tumour (450k/EPIC, the whole
   array, usually from FFPE), sometimes RNA-seq; I almost never have miRNA. I would not have *these* 5,000 probes
   chosen by variance over the TCGA cohort, but a fixed list is reproducible, so this is not a leak. What I always
   have and the data lack: the patient's age, the tumour site (uterus, retroperitoneum, extremity), the morphology and
   IHC, and the referring pathologist's diagnosis. Classifiers in use (DKFZ sarcoma classifier) are deliberately
   blind to histology, so leaving those out is a coherent "blind classifier" task, not a gap that changes it much.
   Three omics vs one costs little: methylation alone gives macro AUC 0.945 / log loss 0.673, mRNA alone 0.953 /
   0.675, miRNA alone 0.945 / 0.724, all three 0.956 / 0.650.
2. **Target (USE-5).** The expert-reviewed type is what I act on, but at the wrong resolution for MFS vs UPS. The
   TCGA study calls them "largely indistinguishable across multiple platforms" and analyses them as one spectrum; the
   DKFZ classifier has one methylation class ("undifferentiated sarcoma") holding UPS, myxofibrosarcoma and part of
   pleomorphic liposarcoma. The distinction is morphological (myxoid stroma, curvilinear vessels) and the pathologist
   settles it from the slide; no molecular output is acted on to split them. In the data: the random forest gets
   0 of 17 MFS right (15 called UPS); UPS vs MFS alone ROC AUC 0.597; merging them takes log loss from 0.650 to 0.461
   (macro AUC 0.956 to 0.982). So about 30% of the benchmark's log loss rides on a split the inputs do not carry.
   Output form: I want calibrated class probabilities with a "no match" when the top score is low (DKFZ calls a class
   only at calibrated score >= 0.9; 322 of 428 validation cases reached it). Log loss rewards calibration, which fits.
3. **Row and test data (USE-10, USE-11).** One row = one patient's primary tumour = one case I type: matches. IID over
   new patients matches "unseen patients" (no recurring entity). What I would face but the test does not hold: the
   51 of 257 omics patients the review excluded (desmoids, probable melanomas, uncertain types, QC failures) and the
   dozens of other sarcoma types (MPNST, pleomorphic liposarcoma, myxoid liposarcoma...). These are exactly the hard
   cases a lab sends for profiling. Also frozen TCGA tissue against my FFPE, and one site contributing 101 of 201 rows
   (holding out sites raised log loss 0.66 to 0.76 in the definition's own check).
4. **Would I use it?** Not as trained: a closed five-class model would force a desmoid or an MPNST into one of five
   bins. I would trust it for the clear calls (37% of cases get a top probability >= 0.7, 98.7% correct there;
   overall accuracy 84.6%) and for DDLPS, which MDM2 expression alone separates (the very test I would run anyway,
   MDM2 FISH). I would distrust any MFS-vs-UPS output.

**Gaps, ranked by how much they change the task**

1. **MFS vs UPS kept apart (USE-5).** Largest effect on the score (log loss 0.650 vs 0.461 merged); the molecular
   actor acts on one class. Fix: merge into "UPS/MFS" (61 rows), the TCGA study's and the DKFZ classifier's own
   convention. Pathologists name them apart, but from morphology, not from these inputs.
2. **Closed world over reviewed cases (USE-8).** Test tumours are cleaner than a lab's and every one belongs to one
   of five types; no "other/no match". Not fixable from this source (the excluded cases have no reviewed label);
   name it in the fit.
3. **Inputs mix (USE-3).** Three omics incl. miRNA, frozen tissue, variance-selected probes; practice is one
   methylation array on FFPE. Small effect on difficulty (per-block results above); name it.
4. **Site concentration.** One site holds half the rows; IID is defensible for "new patients" but optimistic for a
   different lab.

**What a domain expert would change**

* Merge MFS and UPS (or, if kept apart, say in `curation_comments` that the split is morphological and near chance
  from the inputs).
* Set `fit="approximate"` with the reason "a closed five-type set over expert-confirmed cases and three omics stands
  in for a methylation classifier facing all referred sarcomas" (USE-8). This also resolves the contradiction with the
  record's 2026-10-20 assessment ("its use case is invented"): the use case is real (DKFZ classifier, NCT MASTER
  profiling), the data are a stand-in.
* Cite the real practice in `use_case` (methylation-based sarcoma classification) instead of "for example".
* Keep the reviewed label over the submitted one (the review reclassified 20 cases; that is the label a lab trusts).
* Keep DDLPS as defined by MDM2: that is how pathologists define it too (USE-5 satisfied).
* Optional (USE-6): age and tumour site are always known and would be legitimate inputs, but they are not in this
  source and the blind-classifier framing is coherent without them.

**Sources**

* Definition and record: `datasets/_dev/tabarena-v0pt2/sarcoma/dataset.py`, `curation/records/sarcoma.md`.
* Rules: `.claude/skills/knowledge-curation/references/use_case.md` (USE-3, USE-5, USE-6, USE-8, USE-9, USE-10,
  USE-11).
* TCGA Research Network, Cell 171(4), 2017 (UPS/MFS "largely indistinguishable", single spectrum; quoted in the
  definition).
* Koelsche et al., Sarcoma classification by DNA methylation profiling, Nat Commun 12:498, 2021,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7819999/ (cut-off 0.9; 322/428 classified; FFPE/frozen, 450k/EPIC;
  "undifferentiated sarcoma" class holds UPS and myxofibrosarcoma).
* Search summary of follow-up validation (55% classified in a 986-tumour cohort; Charité report refining 47% of 107
  diagnoses): https://pmc.ncbi.nlm.nih.gov/articles/PMC8185366 (not read in full).

</details>

<details><summary>Blind review</summary>

**Verdict**
Include with changes: the data are real TCGA omics, there is one primary tumour per patient, and the labels look like curated pathology-review diagnoses. The task has clear signal without being trivial. But the label provenance is undocumented and does not match the linked source, and the table (201 x 25,971) is an extreme p >> n omics problem that sits at the edge of "tabular benchmark" scope.

**What I checked**
- data.parquet: 201 rows x 25,972 cols, all float64 plus a categorical target. No missing values, no duplicate rows, no duplicate or constant columns.
  Blocks: 20,154 mRNA (RSEM-like, 0 to 3.2e6, 14% zeros), 5,000 methylation beta values (0.006 to 0.995), 817 miRNA (0 to 8.2e5, 45% zeros).
- Class counts: LMS 80, DDLPS 50, UPS 44, MFS 17, SS 10.
- Source (acgt.cs.tau.ac.il multi_omic_benchmark, Rappoport & Shamir, NAR 2018, doi 10.1093/nar/gky889): I downloaded sarcoma.zip and clinical.zip.
  - The source has exp 20,531 x 265, methy 5,000 x 269 (the 5,000 probes were already preselected by the source) and mirna 1,046 x 263. 261 samples are in all three.
  - I matched each parquet row to a source sample on its methylation values: all 201 matched. All are sample type "01" (primary tumour), and there are 201 distinct patients. So there are no normal/recurrent/metastatic duplicates and no patient overlap.
  - The dropped features are the ones constant across samples (310 mRNA, ~207 miRNA). This is unsupervised and harmless.
- Baselines (3-fold x 3 repeats, stratified):

  | Model | acc | bal-acc | AUC-ovr | logloss |
  |---|---|---|---|---|
  | Prior | 0.40 | 0.20 | 0.50 | 1.41 |
  | L2 logreg, log1p + std | 0.82 | 0.75 | 0.955 | 0.50 |
  | LightGBM | 0.86 | 0.78 | 0.961 | 0.54 |

  Each omic alone gives about 0.79 to 0.81 accuracy. The signal is real and has headroom, and the confusion is the biologically expected one (UPS / MFS / DDLPS).

**Concerns (most to least serious)**

1. **The target does not come from the linked source, and its provenance is undocumented.**
   - The `histological_type` in the source clinical file disagrees with the parquet target for 20 of 201 rows (10%). For example, the parquet UPS class contains 4 source-DDLPS, 4 source-LMS, 2 source-MFS and 1 source-MPNST. The parquet MFS class contains 4 source "Pleomorphic MFH/UPS".
   - The class set and counts (80/50/44/17/10 = the 206 cases of the TCGA SARC Cell 2017 paper minus its 5 MPNST) strongly suggest the labels are the pathology-review consensus diagnoses from Cell 2017 (doi 10.1016/j.cell.2017.10.014).
   - That is a better label, but task.md only links the NAR benchmark.
   - Change: document the label source (TCGA SARC 2017 supplementary / TCGAbiolinks subtype table), the merging of synovial subtypes, and the dropping of MPNST (n=5) and of the ~60 samples not in the 206-case cohort.

2. **Scope and shape: 25,971 features on 201 rows.**
   - This is a high-dimensional genomics problem, not a typical tabular one. Many tabular methods (in-context models with feature limits, wide-feature NN/GBDT tuning budgets) will be dominated by feature handling rather than modelling skill. It will also be costly in a 60-split protocol.
   - Change: either keep it deliberately as a "wide omics" task and flag it so, or reduce dimensionality reproducibly. One option is to keep the methylation block (5,000) or the top-variance genes. Another is to select per fold, never on all rows using the target.

3. **The small minority classes make the scores noisy.**
   - SS has 10 cases and MFS 17, so about 3 SS and about 6 MFS per test fold. Balanced accuracy and per-class metrics will swing by tens of points between repeats. Log-loss / AUC are steadier.
   - Change: 20x3 repeated stratified CV is right. Keep stratification, and prefer log-loss or AUC as the main metric.

4. **Raw-scale expression values.**
   - mRNA goes up to 3.2e6 and miRNA up to 8.2e5, with heavy right skew. The standard practice is log2(x+1). Trees don't care, but NNs/kNN/linear models will be penalised for preprocessing rather than learning.
   - Change: apply log2(1+x) to the mRNA and miRNA blocks (a fixed, label-free transform), or document that it is left to the methods.

5. **Real-world use is moderate.**
   - Histological type is set by a pathologist from the H&E/IHC before any omics are run. A molecular classifier would serve as decision support in ambiguous cases, and methylation-based sarcoma classifiers (e.g. DKFZ sarcoma classifier) are a real clinical tool.
   - The IID split is sensible: the cohort is multi-centre, and there is no time ordering. A source-site (TSS) grouped split would test cross-centre generalisation better and could be considered.
   - Leakage: no column is post-diagnosis or label-derived. All features are tumour molecular profiles.

**Could not check**
- I could not confirm the exact label table: I did not download the Cell 2017 supplement. The inference rests on the matching class counts.
- How the source chose its 5,000 methylation probes (it is not stated on the download page; presumably unsupervised).
- Batch/plate effects by tissue source site, and whether a TSS-grouped split would change scores.

</details>

<details><summary>Precedent check</summary>

Precedent checker. Folder `datasets/_dev/tabarena-v0pt2/sarcoma/`, record `curation/records/sarcoma.md`. Sources:
`register.txt`/`register.json` of this run, the Cases tables of `leak_checks.md`, `task_probes.md`, `use_case.md`,
`selection.md`, `splits.md`, `provenance.md`, and the sibling records `brca_breast_cancer`, `glioblastoma`,
`ov_ovarian_cancer`, `lgg_low_grade_glioma`, `coad_colon_adenocarcinoma`, `tcga_coad_molecular_subtype` (all
`curation/records/`), plus the definitions of `glioma_grading_clinical_and_mutation_features`,
`lung_cancer_epithelial_genexp`, `ljubljana_primary_tumor`. One measurement of my own (EV-1, to settle a fact the
split decision rests on): class mix by TCGA tissue source site from the pinned master table.

**Summary**

| # | Decision | Who / date | Verdict |
|---|---|---|---|
| 1 | Keep despite `few_minority` (synovial sarcoma 10 rows, 3-4 per fold) | CC Lennart 2026-10-12 | consistent (TP-8) |
| 2 | Methylation all-row preprocessing: rebuild next pass, kept as is | CC Lennart 2026-10-19 | consistent with LEAK-30 / PROV-13 as amended; the definition's note departs from LEAK-30's form and LEAK-5 (no stated reason) |
| 3 | Label: TCGA's expert-reviewed `short_histo` instead of the submitted diagnosis (the earlier REVIEW.md, issue 1) | definition (AI) | consistent (USE-5, TP-6, LEAK-22) |
| 4 | DDLPS kept although `mRNA_MDM2` alone gives AUC 1.000 (issue 2) | definition (AI) | departs from the coad copy-number precedent (SEL-5) with a reason that answers another question (provenance, not SEL-5) |
| 5 | MFS and UPS kept apart, while STLMS and ULMS are merged (issue 3) | definition (AI) | two like questions decided by two different conventions; no distinguishing fact written (TP-7, USE-5) |
| 6 | MPNST (5 patients) dropped, fewer than 10 | definition (AI) | consistent (ljubljana_primary_tumor, ecoli_proteins) |
| 7 | IID split by patient despite one site holding 101 of 201 rows | definition (AI) | follows glioma_grading in form, but a fact sets sarcoma apart (site carries the label mix); argued from the gap size, which SPLIT-4 bars |
| 8 | `fit="direct"` | definition (AI) | consistent with glioma_grading and ljubljana; contradicts the record's own AI Assessment ("use case is invented") |
| 9 | Not an SEL-4 unsupervised label | definition (AI) | consistent: distinct from brca/gbm/ov |
| 10 | Record `problem_type: Binary Classification` | record (imported) | procedural mismatch, not a decision |

No curator drift found on TP-8 or LEAK-30. No third exception of one kind is pending from this dataset.

**1. Few-minority keep (TP-8): consistent**

Rule: TP-8 (Must; narrows TP-5): a rare class of the source's own labels that carries about its share of the loss stays;
`Too Small` when the short classes carry a large share (alvin) or a fold holds a handful of units in all (parkinsons).

Precedents, all Lennart 2026-10-12, one batch (`task_probes.md` Cases row "forensic_glass_identification,
ljubljana_primary_tumor, mic, sarcoma"): mic 0.7% of test rows / 4.8% of RF log loss; forensic_glass 10% / 14%;
ljubljana 13% / 22% (prostate 10 rows, 3-4 per fold, the exact count sarcoma has). Sarcoma: 5% / 6.5%. Counter-precedent
alvin_smart_money_management_classification_challenge (`No`, Too Small, 2026-10-12): 8 rows carrying 51-54% of a
window's log loss, 5-12 users per window. Sarcoma's facts sit with the kept group. The register's `opposite_outcomes`
flag (alvin against seven keeps) is explained by that share; not a real pair. The 2026-10-20 task probe (3 SS rows in
the smallest fold) matches what was decided. Consistent.

**2. All-row preprocessing of the source (LEAK-30, PROV-13, LEAK-5)**

Rule: LEAK-30 (Must when strong, Should when weak; amended Lennart 2026-10-19): rebuild from unprocessed values when the
source has them (PROV-13); otherwise keep with a `Potential leak, kept on purpose:` note; `No` only for a strong
suspected leak. A variance filter and statistics over all rows are named; "labels or not". LEAK-5 (Must): never argue
"not a leak" from the absence of labels (coad lesson, 2026-10-16).

Precedents:
- coad_colon_adenocarcinoma, CC Lennart 2026-10-16: retired and removed from the working copy for a rebuild
  (`tcga_coad_molecular_subtype`), z-scores over all 260 patients.
- LEAK-30 Cases row (2026-10-19): "rebuilt: coad ..., sarcoma's methylation (next pass). Kept with a note: bioresponse,
  taiwanese_bankruptcy_prediction, credit_card_customers, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m,
  lung_cancer_epithelial_genexp (RMA), home_credit_default_risk's building columns".
- lung_cancer_epithelial_genexp (closest omics keep, Lennart 2026-10-19): the definition carries a bullet starting
  `Potential leak, kept on purpose:` that names the mechanism, the size, why it is kept, and when to revisit.

Comparison. The curator's CC 2026-10-19 (rebuild next pass, keep until then) follows the amended rule: the GDC has the
per-sample beta values, so a rebuild is due, and keeping in the meantime matches the weak-leak reading. The coad pair
(retired 2026-10-16 vs sarcoma kept 2026-10-19) is explained by the amendment in between (the newer decision wins);
not drift.

Departures in the definition (AI, not the curator), no reason stated:
- The `curation_comments` bullet reads "Note: the benchmark's own preprocessing ... uses all patients but no label." It
  lacks the `Potential leak, kept on purpose:` prefix that LEAK-30 prescribes and lung_cancer uses, does not mention the
  CC 2026-10-19 rebuild, and "but no label" is the very argument LEAK-5 and the coad case (EV-6 row) retired.
- Scope: the CC names only the methylation block, but per claim 36 the >20% missing filter and the kNN imputation of the
  benchmark apply to every omic (mRNA, miRNA too). Fact to settle (EV-1): the share of imputed cells per block, from
  the published preprocessing; if mRNA/miRNA cells were imputed over all patients, the planned rebuild should cover
  them too.

**Consistency check (AI, 2026-10-20):** the definition records sarcoma's all-row preprocessing as a plain "Note ... but
no label", while LEAK-30 and lung_cancer_epithelial_genexp (Lennart, 2026-10-19) use a `Potential leak, kept on
purpose:` bullet, and your CC of 2026-10-19 plans a rebuild of the methylation block only. What sets sarcoma apart?
(a) nothing: reword the bullet as `Potential leak, kept on purpose:` (variance filter and kNN imputation over all
patients; rebuild from the GDC beta values planned, CC 2026-10-19) and drop "but no label", and extend the rebuild to
any block the kNN imputation touched; (b) keep as written; (c) reopen lung_cancer's wording to match; (d) change
LEAK-30's note form (an amendment).

**3. Label from TCGA's expert review (USE-5, TP-6, LEAK-22): consistent**

Rule: USE-5 (Must): predict what the actor acts on; check how the source built its label. TP-6: a better version the
source itself defines replaces ours. LEAK-22: follow the paper's cohort.

Precedents: corporate_credit_rating (retired 2026-10-16 for a rebuild from the agencies' own histories, USE-5);
consumer_complaints (settled labels re-sourced, LEAK-7/LEAK-24); diabetes_130_us (the paper's cohort, LEAK-22);
cirrhosis_patient_survival_prediction (USE-5 re-target).

The reviewed `short_histo` is the label the data's own origin (the TCGA study) defines, pinned by GDC file id and md5,
and the cohort is the study's reviewed 206. The submitted-label alternative was probed (RF macro AUC 0.940, LEAK-4
satisfied). Follows corporate_credit_rating and consumer_complaints. The cost (test tumours cleaner than a lab's) is
written in `fit_reason`. Consistent; no prompt.

**4. DDLPS, a one-feature class (SEL-5, TP-4; coad precedent)**

Rule: SEL-5 (Must): a label the source computes with a published, deterministic rule from the columns: drop the rule's
inputs when the rest still makes a real task. TP-4: `Trivial` needs proof; the natural core of a task is expected to
dominate. evidence.md reading 2 of the generated-data marks: a label legitimately defined by thresholds.

Precedents:
- coad_colon_adenocarcinoma, CC Lennart 2026-10-12: the copy-number block dropped because copy-number changes define CIN
  against GS ("a lab that has them computes the subtype by the published procedure"); MSI kept although tumour mutation
  burden (not shipped) separates it at AUC 1.000, because "no rule on the shipped blocks reproduces" it.
- brca_breast_cancer, glioblastoma, ov_ovarian_cancer (Lennart 2026-10-12, SEL-4): labels assigned by a rule on the same
  expression: `No`.
- TP-4 keeps: sepsis_survival, california_house_prices_2020, aps_failure, expresso_churn (the dominant feature is the
  natural core and does not beat the methods).

Comparison. The review typed DDLPS by 12q13-15 amplification (MDM2), a DNA copy-number call that does not ship (the
Rappoport files have no copy-number block). `mRNA_MDM2.4193` is the amplicon's expression readout and separates DDLPS at
ROC AUC 1.000 (probe re-measured 2026-10-20). Under the coad logic this sits between the two coad calls: the defining
measurement is absent (like MSI's mutation burden), but a shipped feature does reproduce the class (unlike MSI). For the
task as a whole SEL-5 and TP-4 are not met: the best single feature skill is 0.075 and DDLPS is one of five classes
(25% of rows). The definition's stated reason ("the class is defined by the amplification and the data are TCGA
measurements, so we keep it") answers the generated-data question (reading 1 vs 2), not the SEL-5 / coad question.
Departs from the coad copy-number precedent with a reason that does not address it.

**Consistency check (AI, 2026-10-20):** the definition keeps DDLPS, which `mRNA_MDM2` alone reproduces (AUC 1.000),
while for coad_colon_adenocarcinoma (2026-10-12) you dropped the block whose values define the class (copy number for CIN
against GS). What sets sarcoma apart? (a) the defining measurement (12q amplification) does not ship; MDM2 expression is
its downstream readout, and DDLPS is one of five classes, so the task is no rule (best single feature skill 0.075):
recorded as the reason under SEL-5 and TP-4; (b) treat it like coad: drop the 12q amplicon genes (MDM2, CDK4, and
neighbours) from the expression block; (c) reopen coad's copy-number drop to match; (d) amend SEL-5 to say whether a
downstream readout of the defining measurement counts as a rule input.

**5. Class granularity: MFS/UPS apart, STLMS/ULMS merged (TP-7, USE-5, TP-6)**

Rule: TP-7 (Must): when the definition builds the target (merged or dropped classes), use an established convention.
USE-5: the resolution the actor acts on. TP-6: a better version the source itself defines replaces ours; a merge of our
own invention is not one.

Precedents: audiology_diagnosis (TP-7, 2026-10-06: our own 3-class merge replaced by a field convention). No precedent
of a source-endorsed merge of two diagnoses.

Comparison. The definition answers two like questions (merge two reviewed diagnoses or not) by two different
conventions:
- STLMS + ULMS merged "as in the clinical file" (the submitted label's convention), although the reviewed label the task
  uses keeps them apart.
- MFS and UPS kept apart "as the pathologists do", although the TCGA study, the label's own source, analyses them "as a
  single spectrum of disease" and finds them "largely indistinguishable across multiple platforms" (here about AUC 0.73).
A reading in which both are right exists but is not written: uterine against soft-tissue origin is an anatomic fact the
lab knows before profiling (nobody predicts it, USE-5), while MFS against UPS is a diagnostic call a pathologist makes.
TP-6 cuts the other way for MFS/UPS: the one-class grouping is a version the source defines, not one of our invention.
Departs without a stated reason (the contrast between the two choices).

**Consistency check (AI, 2026-10-20):** the definition merges STLMS and ULMS (the clinical file's convention) but keeps
MFS and UPS apart (the pathologists' convention), although the TCGA study itself treats MFS/UPS as one spectrum. What
sets the two pairs apart? (a) leiomyosarcoma's uterine or soft-tissue origin is known to the lab before profiling, so it
is no prediction (USE-5), while MFS against UPS is a diagnosis pathologists make: write this as the reason for both
choices; (b) treat them alike: merge MFS/UPS as the study does (61 rows, TP-6, TP-7); (c) treat them alike the other
way: keep STLMS and ULMS apart as the review does; (d) change TP-7 to say which source's convention wins when the label
source and its analysis differ.

**6. MPNST dropped (5 < 10): consistent**

Precedents: ljubljana_primary_tumor ("We drop the primary sites with fewer than 10 patients", kept 2026-10-12);
ecoli_proteins (classes with fewer than 10 proteins dropped). Same threshold, same reason. Consistent.

**7. IID split by patient with a dominant site (SPLIT-4, SPLIT-29, SPLIT-31)**

Rule: SPLIT-4 (Must): the split follows what the task does in reality, not the size of the gap. SPLIT-29: IID is wrong
when many rows share an entity new data would not have and the entity carries the label. SPLIT-31: IID can match the
framing over related entities; such a task is a candidate for a grouped variant, not a fix.

Precedent: glioma_grading_clinical_and_mutation_features (TCGA, kept IID): "the features do not carry the site, since
holding out whole sites scores like a random split (logistic regression ROC AUC 0.919 against 0.918)"; the site
barcode, which gave the label, was dropped.

Measured today from the pinned master table (`TCGA_barcode` characters 6-7, the 201 shipped patients): site `DX` holds
101 rows, including 40 of the 50 DDLPS, 13 of 17 MFS and none of the 23 ULMS; DDLPS is 40% of `DX` rows and 10% of the
others. The site carries the label mix, and holding sites out moves the scored metric (log loss) from 0.66 to 0.76
(+15%), against no change for glioma. So sarcoma follows glioma in form but a fact sets it apart. Both definitions
argue from the gap size, which SPLIT-4 says never decides; sarcoma's text adds "the unit of the use case", which is
the right argument (a lab types tumours of new patients, mostly from its own referral stream). Not a departure from a
Must as written, but the stated reason leans on the gap.

**Consistency check (AI, 2026-10-20):** you kept glioma_grading IID because holding out sites changed nothing; for
sarcoma one site holds half the rows and 80% of the DDLPS, and holding sites out raises the log loss by 15%. What
decides the split? (a) the use case: a lab types new patients, and the referral mix of a site is part of what a lab
meets, so IID by patient stays (SPLIT-4, SPLIT-31), recorded with the site share as a known optimism; (b) treat it as a
grouped task by tissue source site (SPLIT-29); (c) revisit glioma's reasoning to the same use-case argument; (d) add a
rule on dominant collection sites in medical cohorts.

**8. fit = "direct" (USE-8, USE-9): consistent with precedents, contradicts the record**

Precedents: glioma_grading (direct; "as a check on the tissue diagnosis"; gap named: WHO 2021 regrading);
ljubljana_primary_tumor (direct; gap named: rare sites left out); lung_cancer_epithelial_genexp (direct, with a LEAK-30
note). USE-8 Cases for approximate: kick (a potential leak kept on purpose), coffee_rating_prediction, account_debt.
LEAK-30 keeps are mostly `direct` (bioresponse, cooking_time_1m, delivery_eta_1m, maps_router_eta_1m, lung_cancer), so
kick's "potential leak kept on purpose = approximate" has not been applied to LEAK-30 cases; sarcoma follows the
majority.

Sarcoma's use case ("support or check a hard diagnosis") and gaps mirror glioma_grading. Consistent with the precedents.
The record's AI Assessment (2026-10-20) says "its use case is invented", which contradicts the definition's `direct`;
both are AI text, no curator decision is involved, so this is for the panel's use-case reviewer (USE-9's weighed factor
"a use case rephrased only to excuse a gap"), not a consistency prompt.

**9. Not an SEL-4 label: consistent**

brca_breast_cancer, glioblastoma, ov_ovarian_cancer were retired (SEL-4, Lennart 2026-10-12) because their labels are
clustering subtypes assigned from the same expression. Sarcoma's label is the histopathological diagnosis, confirmed by
expert review of the tissue, not a cluster. The sibling records' facts differ on exactly the fact SEL-4 tests.
Uniqueness (PROV-6, PROV-7): the other Rappoport/MLOmics TCGA records are other cancers; glioma_grading overlaps GBM
patients, not sarcoma. Unique.

**10. Record `problem_type`**

The record still reads `Binary Classification` (imported; the AI Assessment of 2026-10-07 already said multiclass). Same
leftover on brca/gbm/ov/lgg (retired); coad's record was corrected to Multiclass. Procedural: set it to Multiclass
Classification when the curator's decisions are applied. No prompt.

</details>

<details><summary>Advocate</summary>

Position: ship, after documentation fixes and one small column drop. No phase-A finding is a validity failure that
the definition cannot fix; every real problem has a remedy below exclusion on the ladder.

**1. A real task with the target the actor acts on (P3: USE-1, USE-5 Must; SEL-4)**

- Claim: typing a soft-tissue sarcoma from its molecular profiles is a published diagnostic practice, and the label
  is the expert pathology diagnosis, not a computed cluster.
- Evidence: Koelsche et al. 2021 (Nat Commun 12:498), a methylation classifier for diagnostic sarcoma typing (claim
  audit row 2; practitioner: DKFZ classifier, 322 of 428 validation cases called). The label is TCGA's reviewed
  `short_histo` from the pinned GDC file (md5 re-measured), which reclassified 20 submitted diagnoses (crosstab
  4 + 5 + 11 = 20, matches the paper). The blind reviewer inferred the same label source from the class counts alone.
- Answers: the record's "its use case is invented" (refuted, claim 62) and the SEL-4 siblings brca/gbm/ov (retired
  for clustering labels; precedents item 9: this label is histopathology). USE-5 is met better than with the
  submitted label (precedent corporate_credit_rating, consumer_complaints: re-source to the label of record).

**2. The split mirrors the use case (P4: SPLIT-4, SPLIT-29, SPLIT-31)**

- Claim: IID by patient is the right regime; the dominant site DX (101 of 201) does not make it wrong.
- Evidence: one row per patient (asserted), 0 exact or near copies, hidden-group probe 0 candidates. Split audit:
  RF predicting DX vs rest from the features, AUC 0.458 overall; train DX -> test other sites 0.959 AUC / 0.644 LL,
  against 0.954 / 0.695 for a size-matched random split. A lab types new patients, mostly from its own referral
  stream; the patient is the unit.
- Rule: SPLIT-29 needs an entity that new data would not have *and* that carries the label in a way a model can
  recognise; the site is not recognisable overall. SPLIT-4 bars arguing from the +15-20% log-loss gap (claim audit
  0.769 mean, own +20%). At most SPLIT-31 (Should): a candidate for a grouped variant, not a fix.
- Concede: the claim audit finds site learnable within LMS (0.773) and DDLPS (0.706), against the split audit's
  0.520 / 0.474: the two runs disagree, and EV-1 says the fact is settled by one decisive run, not by me. Either way
  the remedy is mild: a `splits_comment` naming DX's share and the site hold-out numbers as a known optimism
  (split audit problem 1, precedents option 7a).

**3. DDLPS is not a rule-made label (SEL-5 Must; TP-4)**

- Claim: `mRNA_MDM2.4193` at AUC 1.000 for DDLPS does not trigger SEL-5 or Trivial.
- Evidence: the review's defining input is 12q15 copy number, which is not shipped (claim audit row 14, column
  audit problem 3: "not a leak"). MDM2 amplification "was present in all DDLPS by definition" (Cell 2017): it is the
  entity, and a lab has MDM2 FISH at typing (LEAK-37; practitioner: "the very test I would run anyway"). The task as
  a whole is no rule: best single-feature skill 0.075, prior log loss 1.41 against 0.50-0.65 for models, accuracy
  0.82-0.86 (blind review) with the hard confusions elsewhere.
- Against the coad precedent: coad dropped a shipped block that computes the class; here the defining block is
  absent, as for coad's MSI (kept although mutation burden separates it at 1.000). Precedents option 4a.
- Remedy (concede the wording): rewrite the Label bullet to say the DDLPS label required 12q15 copy-number gain from
  the study's own data (not shipped), replacing "made from the tissue". Documentation only.

**4. The transductive preprocessing is a weak leak the curator already kept (P4: LEAK-30 Should when weak)**

- Evidence: kNN imputation and the 5,000-probe variance filter over all 269 samples, label-free (Suppl. File 1).
  mRNA and miRNA values are per-sample RSEM/RPM (per-row, fine under LEAK-30). CC 2026-10-19: rebuild methylation
  from GDC betas next pass, "kept as is until then"; LEAK-30 lists "sarcoma's methylation (next pass)".
- Concede: the definition's "uses all patients but no label" is the form LEAK-5 retired and lacks the `Potential
  leak, kept on purpose:` prefix (lung_cancer_epithelial_genexp precedent). Remedy: reword the bullet, name the
  rebuild, and note that the kNN step touched every block (scope of the rebuild for the curator). No data change.

**5. Worth benchmarking, and in a regime the collection lacks (P6: TP-8 Must, TP-5; CLEAN-22, EV-4)**

- Evidence: every class in every test fold, SS 3-4; SS is 5% of test rows and 6.2-6.5% of RF log loss, the same
  facts as the kept batch (ljubljana prostate: 10 rows, 3-4 per fold; mic; forensic_glass) and unlike alvin (51-54%).
  Real headroom: prior 1.41, LR 0.50, LightGBM 0.54, RF 0.64.
- 201 x 25,971 is the wide-omics regime (record: "gap +"). Width is never a reason to drop features or the dataset
  (Tensions row "Width against model limits", coad 2026-10-15), which answers the blind reviewer's concern 2. Raw
  scale (concern 4) is the pipeline's job (column audit CLEAN-2).

**6. MFS vs UPS is a weighing call, not a failure (USE-5, TP-6, TP-7)**

- Concede the facts: the earlier REVIEW.md's "AUC 0.73" is wrong; measured 0.62-0.66 (RF, L2 logistic), 0.597
  (practitioner); RF predicts MFS for 0 of 51 test rows; MFS+UPS carry about half the log loss. Correct the number.
- Argue: both versions are valid tasks, so TP-6 keeps the shipped one unless the source defines a better one. The
  five classes are the reviewed label's own (`short_histo`); a hard pair of real classes is difficulty, not
  invalidity (TP-4 needs proof of triviality, nothing asks for proof of separability). The merge is the TCGA
  analysis's and DKFZ's convention, so it is also legitimate under TP-7. Either choice ships; the curator decides
  (principles: a weighing call goes to the curator).
- Mild fix either way: write why STLMS+ULMS are merged (uterine vs soft-tissue origin is known to the lab before
  profiling, so not a prediction under USE-5) while MFS/UPS stay apart (precedents option 5a), or merge MFS/UPS.

**7. The remaining findings are documentation and one cheap drop (P7, USE-8, procedure)**

- `Methy_rs*`, 61 germline SNP control probes (column audit problem 1): concede. Drop them in `_clean`; no signal
  lost (best AUC 0.77 on 10 rows among 305 tests, noise), removes a patient fingerprint and the SEL-1 question.
  CLEAN-3 (Should), the mildest remedy is the fix itself.
- `fit="direct"` (USE-8 Must): concede it should read `approximate`. fit_reason itself names two gaps (cleaner test
  tumours than a lab's intake, a closed set of five types), and the practitioner agrees. This changes a field, not
  the verdict; USE-8 None would be the only failing value.
- Record `problem_type: Binary Classification` -> Multiclass; "as in TabPFN-Wide ... histological type" -> cite
  "subtype classification (Sec. 5, Table A1)"; drop "use case is invented". Procedure only.

**Judgment record (proposed)**

```text
Verdict: ship after changes.
Validity: SEL-4 holds (histopathology label); SEL-5 not triggered (copy number not shipped); USE-1, USE-5 hold
  (reviewed diagnosis, published practice); USE-8 fit -> approximate; LEAK-30 weak, kept with a note until the
  GDC rebuild (CC 2026-10-19); SPLIT-4/29 hold, IID by patient with a splits_comment.
Value: TP-8 keep (SS 5% of rows, ~6% of log loss); real headroom.
Quality: CLEAN-3 drop 61 Methy_rs* SNP probes; wording fixes (Label bullet, LEAK-30 note).
Weighed: gap + (wide tiny omics), source +, use case + (Koelsche 2021), size -.
For the curator: MFS/UPS merge (weighing call); site within-class learnability (settle the two runs, EV-1).
```

**Rebuttal**

The critic and I agree on the verdict ("ship after changes"), on keeping the reviewed label, on TP-8, and on width.
Only one point is still in dispute: whether the MFS/UPS merge is required (critic point 2).

**1. `Methy_rs*` genotype columns: concede**

Drop the 61 columns in `_clean` and in the planned GDC rebuild. This is my point 7. Nothing is lost (best AUC 0.77 on
10 rows among 305 tests), and the SEL-1 question goes away.

**2. MFS against UPS: concede the facts and the documentation; dispute that the merge is forced**

- Concede: within the pair, AUC is 0.60-0.66 across three runs. "AUC 0.73" is wrong and gets corrected. The RF never
  predicts MFS. The definition must write why STLMS+ULMS are merged and MFS/UPS are not, and say that MFS vs UPS is
  weak from these inputs.
- Dispute "USE-5/TP-7 triggered, merge":
  - TP-7 governs targets the definition builds. Our merge of STLMS+ULMS falls under it; keeping MFS and UPS apart
    does not. They are two distinct values of the label source's own field (`short_histo`).
  - TP-6 says "a valid task stays". The single spectrum is how the study grouped them for analysis. The label table
    the study published keeps them apart, so both versions come from the source and neither is invalid.
  - "Near chance" overstates it. 0.60-0.66 is a weak real signal, not chance. MFS carries 21% of the log loss with
    8.5% of the rows, which is within the kept TP-8 range (ljubljana: 13% of rows, 22% of the loss).
  - Under the "right split against the score" tension, difficulty is no reason to change a task.
- Concede that USE-5's "resolution the actor acts on" weighs toward the merge. The DKFZ classifier uses one class,
  and the practitioner says no molecular output is used to split MFS from UPS.
- What follows: both forms are valid. This is a weighing call for the curator, which the critic's own judgment
  record also says. It is not a Must the definition fails.

**3. fit "direct": concede**

Set `fit="approximate"` with the critic's reason. It names a closed set of five confirmed types and a kept LEAK-30.
This was already my point 7.

**4. DDLPS label wording: concede the wording; no data change**

The critic agrees that SEL-5 is not triggered and that the task is no rule (skill 0.075). Rewrite the
Prediction-point and Label bullets. Record the SEL-5 reason that sets sarcoma apart from coad: the defining
measurement (copy number) is not shipped, and DDLPS is one of five classes.

**5. LEAK-5 / LEAK-30 wording and rebuild scope: concede**

- Change the note to `Potential leak, kept on purpose:` and drop "but no label".
- The scope fact (kNN imputation on every omic) comes from Suppl. File 1, which both of us cite. The rebuild should
  therefore cover every block the imputation touched.
- This is a note and the curator's rebuild plan, not a data change now.

**6. Split reasoning: concede**

The `splits_comment` argues from the use case (new patients, one row each) and states DX's share as a known
optimism. It drops the "only" and the gap-size argument (SPLIT-4). The within-class site disagreement (0.773/0.706
against 0.520/0.474) gets settled before the comment's wording on site visibility is fixed (EV-1). Either result
leaves IID in place: at most SPLIT-31, a grouped variant.

**7. Procedure: concede all four**

problem_type becomes Multiclass. Remove "use case is invented". Correct the 0.73. Cite TabPFN-Wide as "subtype
classification (Sec. 5, Table A1)".

**Net**

Ship after changes:
- drop `Methy_rs*`
- set fit to approximate
- reword the label and LEAK-30 notes
- add the splits_comment
- correct the record fields

One weighing call goes to the curator: whether to merge MFS and UPS (a written reason if kept).

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** The task is real (molecular sarcoma typing exists: Koelsche et al. 2021, DKFZ
classifier; claim audit 2, practitioner) and I do not ask for exclusion. But the definition ships a personal
genotype block, scores half its log loss on a class split its own label source calls indistinguishable, labels its
fit "direct" against its own named gaps, and words the label and the all-row preprocessing in ways the rules retired.

D = the folder's `dataset.py`.

**1. P1: 61 columns are the patient's germline genotype, not methylation (SEL-1 Must, as a question; CLEAN-3 Should)**

* Problem: 61 of the 5,000 `Methy_` columns are `Methy_rs<id>`, the 450k array's SNP genotyping control probes.
  Values cluster at 0 / 0.5 / 1 (genotype calls); they entered only through the source's variance filter.
* Effect on the task: none useful. Best one-vs-rest AUC 0.61-0.77 over 305 tests (noise; 0.77 on the 10 SS rows);
  they identify the person, not the tumour. Germline genotype is TCGA's controlled-access category, even though the
  level-3 450k files carried these probes openly.
* Evidence: column audit, row `Methy_rs<id>` and problem 1.
* Remedy (fix the definition): drop the 61 `Methy_rs*` columns in `_clean`, say so in the Features bullet, and do
  the same in the planned GDC rebuild (GDC betas carry the `rs` probes too). No signal is lost, so the SEL-1 question
  never has to be argued.

**2. P3: MFS against UPS is scored at a resolution the label's source and the molecular actor do not use (USE-5 Must, TP-7 Must, TP-6)**

* Problem: the TCGA study that supplies the label finds MFS and UPS "largely indistinguishable across multiple
  platforms" and analyses them "as a single spectrum of disease"; the DKFZ methylation classifier puts both in one
  class. The definition keeps them apart "as the pathologists do", but pathologists split them from morphology, an
  input this table does not have. Meanwhile it merges STLMS and ULMS by the clinical file's convention: two like
  questions, two conventions, no distinguishing fact written (precedents.md 5).
* Effect: within the pair, RF 0.624 / L2 logistic 0.663 / RF 0.597 (three independent runs); the 5-class RF predicts
  MFS for 0 of 51 MFS test rows. MFS+UPS carry 51.5% of the RF log loss with 30% of the rows; merging them moves log
  loss 0.650 -> 0.461. A large share of the benchmark score measures a distinction the inputs do not carry.
* Evidence: claim audit claim 33; practitioner target question and gap 1; precedent check 5. the earlier REVIEW.md
  issue 3's "AUC about 0.73" was not reproduced by anyone and must be corrected.
* Remedy (fix the definition): merge MFS and UPS into one `UPS/MFS` class (61 rows), the convention of the label's own
  source (TP-6: a version the source defines, not one of our invention; TP-7: an established convention). If the
  curator keeps five classes, the mildest acceptable form is a written reason for both granularity choices and a
  note that MFS vs UPS is near chance from these inputs.

**3. P3: fit is "direct" while `fit_reason` names two gaps (USE-8 Must)**

* Problem: USE-8 defines approximate as "a stand-in with a known gap, named as such ... a potential leak kept on
  purpose". `fit_reason` itself names two gaps (test tumours cleaner than a lab's; few labs measure all three
  profiles); the test set is a closed world of five types over the 80% of cases the review kept (no desmoid, MPNST,
  probable melanoma); and the definition keeps an all-row preprocessing on purpose (point 5; kick precedent).
* Effect: the fit field tells users the test data mirror a lab's intake; they do not. The practitioner, as the
  actor, would not use the closed five-class model on referred cases as trained.
* Evidence: D `fit_reason`; practitioner "Fit: approximate"; claim audit claim 12; split audit
  problem 3; checklist P3 row.
* Remedy (fix the definition): `fit="approximate"`, reason "a closed set of five expert-confirmed types profiled on
  three omics stands in for a classifier facing all referred sarcomas". If the curator follows the
  lung_cancer_epithelial_genexp / bioresponse precedent (direct with a kept LEAK-30 note), the two named gaps beyond
  the leak still need an answer; write it in the record.

**4. P3: the DDLPS label is partly the study's copy-number rule, but the definition says "made from the tissue" (USE-5 Must; SEL-5 consistency)**

* Problem: the review required "evidence of increased chromosome 12q15 copy number" for every DDLPS and reclassified
  by "focal chromosome 12q~15 amplification" (Cell 2017 Methods). All 8 relabels into or out of DDLPS follow MDM2
  mRNA exactly (every reviewed DDLPS >= 9,095, every other class <= 4,541); `mRNA_MDM2.4193` alone gives AUC 1.000.
  D says "the label is the expert pathology diagnosis, made from the tissue" and "the profiles exist before the
  typing"; the second is true in time but hides that the typing used molecular data of the same tumour.
* Effect: one of five classes is a near-rule on a shipped proxy. Not a leak (copy number is not shipped, SEL-5 not
  triggered as written; best single-feature skill 0.075 for the task), and practice also uses MDM2. But D's stated
  reason answers the generated-data question, not the coad precedent (copy-number block dropped because it defines
  the class).
* Evidence: claim audit claims 13, 14, 23; column audit problem 3; precedent check 4.
* Remedy (a note, no data change): rewrite the Prediction-point and Label bullets ("for DDLPS, the study required
  12q15 copy-number gain, which is not shipped; MDM2 expression is its readout") and record the SEL-5 reason that
  sets sarcoma apart from coad (defining measurement absent, task not a rule).

**5. P4: the all-row preprocessing is argued with the retired "no label" reasoning, and the rebuild scope is too narrow (LEAK-5 Must, LEAK-30 Should when weak)**

* Problem: Suppl. File 1 of the source: features and patients with over 20% missing removed and kNN imputation over
  all patients, on every omic, plus the 5,000 highest-variance methylation probes over all 269 samples. D writes this
  as "Note: ... uses all patients but no label". LEAK-5 forbids "not a leak" from the absence of labels (coad,
  2026-10-16); LEAK-30 asks for a `Potential leak, kept on purpose:` note; the closest kept omics case
  (lung_cancer_epithelial_genexp) uses that form. The CC of 2026-10-19 plans a rebuild of the methylation block only.
* Effect: a weak transductive leak, kept by the curator's decision; I do not dispute keeping it. The wording
  understates it, and the mRNA and miRNA blocks may carry kNN-imputed cells too (share untested).
* Evidence: claim audit claim 36; precedent check 2 (consistency check); column audit problem 2.
* Remedy (a note): reword as `Potential leak, kept on purpose:` (mechanism, all omics, kept per CC 2026-10-19 until
  the GDC rebuild), drop "but no label", and extend the planned rebuild to every block the imputation touched.

**6. P4: the split's justification rests on the gap size, and the site concentration is not stated where users read it (SPLIT-4 Must, as a reasoning fix; SPLIT-30 note)**

* Problem: site DX (MSKCC) holds 101 of 201 rows, 40 of 50 DDLPS and 13 of 17 MFS. Site-grouped splits raise RF log
  loss by about 15-20% (0.64 -> 0.77 mean over three seeds; 0.66 -> 0.76 in D). D keeps IID partly because the AUC
  moves "only" a little; SPLIT-4 says the gap size never decides. The README's split section says "Default splits."
* Evidence: claim audit claims 38-39; split audit; precedent check 7. The two audits disagree on whether
  the site is visible within class (claim audit: RF AUC 0.773 in LMS, 0.706 in DDLPS; split audit: 0.52 / 0.47); the
  fact should be settled before the reason is written (EV-1).
* Remedy (a note, no re-split): a `splits_comment` that argues from the use case (new patients, one row each) and
  states the site share as a known optimism for a new lab; drop the gap-size argument.

**7. Procedure: four statements that are wrong or unverified (writing.md, EV-2, EV-7)**

* Record `problem_type: Binary Classification`; the data are 5-class (claim 51).
* Record Assessment 2026-10-20 "its use case is invented": refuted (Koelsche et al. 2021; claim 62).
* REVIEW issue 3's "AUC about 0.73" for MFS vs UPS: not reproduced (0.60-0.66; point 2).
* "as in TabPFN-Wide ... histological type": the paper says "cancer subtype classification" on 259 patients and
  26,577 features, and does not name the column (claims 24, 54).
* Remedy: correct each in the record, REVIEW.md and `curation_comments`.

**Not argued**

Clean room's width (25,971 x 201) and raw-scale expression: width is no reason to drop features (CLEAN-22, coad
2026-10-15) and a log is the pipeline's job. Few-minority SS: decided by CC 2026-10-12 (TP-8), consistent with
precedents. Label from the TCGA review instead of the submitted diagnosis: right (USE-5).

Judgment record (critic's ask):

```text
Verdict: ship after changes.
Validity: SEL-1 question, fixed by dropping 61 Methy_rs* columns; USE-5/TP-7 triggered, merge MFS+UPS (or write the
  reason); USE-8 triggered, fit approximate; USE-5 DDLPS label wording; LEAK-5/LEAK-30 note reworded, rebuild scope
  widened; SPLIT-4 reasoning restated in splits_comment.
Value: TP-8 keep (CC 2026-10-12).
Quality: none raised.
For the curator: the MFS/UPS merge and the fit label are weighing calls the curator owns.
```

**Rebuttal**

We agree on the verdict (ship after changes) and on most of the remedies. One point is still disputed: MFS/UPS
(advocate 6). It is the one change that affects the score.

| Advocate point | Response |
|---|---|
| 1. Real task, reviewed label (USE-1, USE-5, SEL-4) | **Concede.** I never disputed it; my point 7 also asks to remove "use case is invented". |
| 2. IID by patient (SPLIT-4, SPLIT-29, SPLIT-31) | **Concede the regime**: I asked for no re-split. Two conditions stay: the `splits_comment` argues from the use case (new patients) and not from "only" a small gap (SPLIT-4), and the within-class conflict between the two runs (0.773 / 0.706 against 0.520 / 0.474) is settled by one run before the comment is written (EV-1). The advocate agrees to both. |
| 3. DDLPS is not a rule-made label (SEL-5, TP-4) | **Concede** that SEL-5 is not triggered and that the remedy is wording. I still ask that the record give the reason that sets sarcoma apart from coad (the defining copy number is not shipped, like MSI; the task is no rule, best single-feature skill 0.075). That is precedents option 4a. Without it, the coad copy-number drop and this keep look like drift. |
| 4. Weak transductive leak, already kept (LEAK-30) | **Concede.** Both sides want the same remedy: a `Potential leak, kept on purpose:` bullet, no "but no label" (LEAK-5), and a rebuild that covers every block the kNN step touched. |
| 5. Worth benchmarking; width (TP-8, CLEAN-22) | **Concede.** I raised neither point (see "Not argued" in my brief). |
| 6. MFS vs UPS is a weighing call | **Dispute.** USE-5 is a Must about *resolution*: "at the resolution they act on it". The actor here uses molecular profiles only, and no molecular tool acts on MFS against UPS. The DKFZ classifier has one class for both, and the label's own source analyses them "as a single spectrum" (practitioner, target question). The data agree: within the pair 0.597-0.663, MFS predicted for 0 of 51 MFS test rows, and the pair carries 51.5% of the log loss with 30% of the rows. That is not "a hard pair of real classes". About half the score measures a distinction the inputs do not carry. TP-6 does not protect the five classes. The definition built this target itself (it merges STLMS and ULMS and drops MPNST), so TP-7 applies, and the one-class version is "a version the source itself defines", not one of our invention. In TP-6's terms, merging is the better version. The rule that wins: USE-5 (Must, P3), which outranks the advocate's appeal to difficulty under TP-4 (P6). My remedy stands: merge into `UPS/MFS` (61 rows). If the curator keeps five classes, that is an exception to a Must. It cannot be recorded as an exception (a Must has none), so it needs the distinguishing fact written down and the STLMS/ULMS contrast explained (option 5a). |
| 7. `Methy_rs*` drop, fit approximate, record fixes | **Concede**, with one note on rank. The 61 SNP columns are a germline genotype, which raises the P1 question (SEL-1). They are more than CLEAN-3 identifier hygiene. The remedy is the same drop, so the label does not change the outcome. |

Judgment record (critic, after rebuttal):

```text
Verdict: ship after changes.
Validity: SEL-1 question closed by dropping 61 Methy_rs*; USE-5 triggered on MFS/UPS, merge (disputed: advocate
  calls it weighing); USE-8 fit approximate (agreed); SEL-5 not triggered, reason vs coad written (agreed wording);
  LEAK-5/LEAK-30 note reworded, rebuild scope all imputed blocks (agreed); SPLIT-4 holds, splits_comment from the
  use case after settling the within-class site run (agreed).
Value: TP-8 keep.
For the curator: MFS/UPS, a USE-5 question by the critic's reading, a weighing call by the advocate's.
```

</details>

