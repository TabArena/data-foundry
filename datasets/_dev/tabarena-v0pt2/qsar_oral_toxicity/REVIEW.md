# qsar_oral_toxicity

**Outcome:** added. The very toxic endpoint (rat oral LD50 of 50 mg/kg or less) of UCI 508 from 1,024 ECFP bits,
binary, IID with the default random splits; copies of a parent structure, vectors with both classes and nine rows
whose parent structure is already present are dropped (8,484 chemicals). A review panel, full tier, ran on
2026-10-20 and recommends shipping it after changes, which are applied; on 2026-10-21 the fit became `approximate`
and the scaffold-grouped variant stays a listed candidate (SPLIT-31). Only the extension is open (issue 3).

**Main points:** Extend the dataset with the package's validation set, add the non-toxic endpoint as a second
dataset, both, or neither? The curator's copy of the package holds both (issue 3).

**Record judgment:** valid. The labels are the very toxic endpoint of the calibration set of the ICCVAM acute oral
toxicity project (CATMoS): the claim audit reproduced the class counts, both block counts and the checksum, and
linked every row to the project's structure file (100% class agreement). The UCI file equals the ECFP_1024_02
training and test blocks of the authors' package bit for bit. Fingerprints are in scope by the qsar_tid_11
precedent.

**Issues for Lennart:**

3. **Extend the dataset with the project's evaluation set and the second endpoint?**
   - Problem: UCI holds only the calibration part of the data. The full very toxic data is 11,886 chemicals.
   - Effect: up to a third more chemicals, and the non-toxic endpoint would be a second, better balanced task on the
     same source (3,848 of 8,981 positive).
   - Evidence: the labels of both are public in the project files (the evaluation set is 2,894 chemicals, 243 very
     toxic), but the fingerprints exist only in the Milano group's download, which needs a form with a name and an
     e-mail address that this machine cannot submit. Not verified: the package was never downloaded.
   - Implemented: UCI only.
   - Alternative: fetch the package by hand and extend. hiva_agnostic (your call of 2026-10-14, add the challenge's
     384 validation compounds) leans that way, but there the further compounds were in a file already fetched.
   - Rule: PROV-6 and PROV-7 (a shared source with a distinct task is not a duplicate); no rule forces the extension.
   - Recommendation: leave it as it is unless you fill in the form; both extensions need the same download.
   - Decision: fetch the package by hand (which enables both), or leave the dataset as it is?

   **Lennart (2026-10-21, discuss):** here is the gdrive link to the data [a copy the curator provided (Google Drive)] can you use that? i can use it without the form
   **Answer (AI, 2026-10-21):** Yes. A copy the curator provided (Google Drive) is the Milano group's package behind
   the form (a RAR of MATLAB code and data; only the data was read). `vt_data.mat` holds the training (6,744), test
   (2,248) and validation (2,894, 243 very toxic) chemicals in both fingerprint variants; its ECFP_1024_02 training
   and test blocks equal the UCI file bit for bit (8,992 of 8,992 rows, classes 100% equal), so UCI uses `_02`.
   With our deduplication (exact copies, vectors with both classes) the very toxic data grows from 8,493 to 11,114
   chemicals (931 very toxic, +31%); 237 validation vectors equal a calibration vector. `nt_data.mat` holds the
   non-toxic endpoint: 11,871 chemicals (5,083 non-toxic, 43%) with ECFP_1024_05 bits and 3,152 fragment counts.
   Each set also carries CASRN, DTXSID, QSAR-ready SMILES, InChIKey and LD50 per chemical, as MATLAB string objects
   that scipy does not decode; the project's structure files give the same by row order. Nothing is changed yet:
   extending means a new raw file whose public route is the form (the package's readme: freeware, cite the paper),
   and redoing the parent-pair linkage for the validation rows. Your call: extend the very toxic dataset with the
   validation set, add the non-toxic endpoint as a second dataset, both, or neither?

**Review panel:** ship after changes (mediator). Claims: 52 checked, 8 refuted (the target threshold, the "never" in
the split text, the reason given for IID-only, two duplicate counts, a citation, the record's "issues closed"), all
fixed; 1 weighing call left open (the fit label). Blind review: include, its main concerns are the optimism of the
random split and the undocumented fingerprint variant. Agreed: no exclusion, no re-split, the deduplication as
implemented, the scope of fingerprints. Disputed: the fit label (issue 6) (issue 1 in the mediator's report is issue
6 here) and whether to build a scaffold variant (issue 2). The mediator's change 8 points at "REVIEW issue 5", a
closed issue this file no longer has; the sibling's domain value was checked and is right, so nothing is open there.
The precedent check's two consistency checks and the column audit's dtype question are filed in the working copy's
cross-dataset review file.

<details><summary>Mediator</summary>

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-1, SEL-3 hold; SEL-12 holds (qsar_tid_11). USE-1, USE-3 hold; USE-5 holds once the target reads
"50 mg/kg or less" (text). USE-8: direct is not supported for the use case as written; approximate recommended,
curator's call under USE-9 (issue 1). LEAK-10, LEAK-27 to LEAK-30 hold; LEAK-31 very weak, no remedy. LEAK-16,
LEAK-19, LEAK-20 hold (text corrected). LEAK-17 triggered by 9 surviving parents, fixed (drop one row of each pair).
SPLIT-1, SPLIT-24, SPLIT-29 hold; IID stays; SPLIT-31 scaffold variant is a candidate (issue 2). PROV-8, PROV-13 hold.
Value: TP clean (RF 0.882, 236+ positives per test fold).
Quality: CLEAN holds; bit dtype convention across siblings is a separate question.
Weighed: gap - (prediction set farther than test rows), use case +, source +, shape +.
For the curator: issue 1 (fit label), issue 2 (scaffold variant), issue 3 (extension, still open).
```

No exclusion, no re-split. One data change (9 rows); the rest is text. The 9-row drop makes a new container: build only
on the curator's ask, with a CHANGELOG entry and the README table updated.

**Changes to make now (no decision needed)**

1. **Drop one row of each parent that survives twice** (LEAK-17, Must; remedy ladder: fix the definition). Decisive
   run on the claim audit's linkage: **9** parents (not 11) keep two rows, 18 rows, by full and by
   skeleton InChIKey. Every pair is a free acid and its salt or tautomer under two CASRNs (e.g. 50-06-6 / 57-30-7,
   phenobarbital and its sodium salt), all "negative". Raw UCI positions: 3238/6358, 3952/7628, 3785/8179, 6671/6689,
   6675/8967, 2900/5706, 4384/4996, 4538/7203, 6672/6690. The bits of a pair differ (Tanimoto 0.19 to 0.93), so the
   pair cannot be found from the file alone; hard-code the 9 positions to drop, citing the linkage. This settles the
   advocate's objection (no reconstruction run in `_clean`): a wrong link would only drop one negative row. A
   wording fix alone leaves a Must broken, and a Must has no exceptions.
2. **Target** (USE-5, Must; EV-2): `predicted` and the Target bullet say "50 mg/kg or less (the top acute oral hazard
   category)"; add that 25% of labels (2,258 rows) come from category data without a point LD50. Same fix in the
   record's 2026-10-07 assessment ("LD50 < 50").
3. **Split wording** (LEAK-17): after change 1, "never" holds by the project's InChIKeys; say it rests on the
   order linkage to `trainingset_171130.txt`.
4. **IID bullet** (EV-1, SPLIT-5): delete "The file holds no structure or identifier, so a scaffold split cannot be
   built." Say IID rests on the use case (a new chemical each time; no entity recurs, SPLIT-29), the structure-blind
   source protocols, and SPLIT-24; the rows can be linked to the project's structures by file order.
5. **Note bullet** (EV-2, SPLIT-31): add the cluster cost (RF 0.882 to 0.842 under Butina clusters at 0.5; scaffold
   3-fold 0.843 against 0.887; ranking unchanged) and drop "It does not come from series a random split lets a model
   memorise"; the near-copy gap is +0.006, but chemotype-level signal carries over.
6. **Duplicates bullet and `_decisions`** (LEAK-16, EV-2): 12 of the 406 repeated vectors are hash collisions of
   different chemicals; by InChIKey the source has 405 repeated keys over 891 rows, and the both-class groups are 11
   keys over 29 rows.
7. **Features bullet** (writing.md): Dragon 7 is cited in Sec. 2.7; state the variant (ECFP_1024_02 or _02R, radius
   2, 2 bits per fragment, the file does not say which); 97 QSAR-ready SMILES keep stereo markers, which the
   fingerprint ignores.
8. **Record and REVIEW.md** (procedure): replace "no known risk" / "issues closed" in the 2026-10-20 assessment with
   the open issues below; reopen REVIEW issue 2 with the linkage facts and the refuted premise "screening lists hold
   many analogs"; in REVIEW issue 5, clock_protein_toxicity is "chemistry & material science", not biology.

**Issues for the curator (ranked)**

1. **Fit label: direct or approximate** (P3; USE-8 Must, USE-9 Should with a weighing).
   * Problem: `use_case` names screening of untested chemicals; the test rows are random members of the tested set.
   * Effect: the shipped AUC is the in-domain number. Untested chemicals of the project's prediction set have half
     the close-analog share (9.3% against 19.7% at Tanimoto >= 0.7; median 0.474 against 0.553), and RF AUC tracks
     that axis (0.68 to 0.96).
   * For direct (practitioner): the project's real external evaluation set matches the IID test (0.545, 21.7%);
     the blind validation scored like the random test (NER 85% / 86%).
   * For approximate (critic; advocate conceded in rebuttal): the actor in the CATMoS paper screens the 48,137-chemical
     prediction set; narrowing the use case to the evaluation design is "a use case rephrased only to excuse a gap".
   * Recommendation: approximate, with the two similarity numbers and the 0.044 scaffold cost in `fit_reason`.
     Ships either way. What would settle it: whether you read the programme's evaluation design as a use case
     practitioners have (USE-9; 5g_energy_consumption was direct on that ground).
2. **Scaffold-grouped variant** (P4; SPLIT-31 Should). IID stays (SPLIT-29 not triggered, SPLIT-24 bars clusters).
   Build a variant on the linked structures? For: costs 0.034 to 0.044 AUC, a real out-of-chemotype test. Against:
   the key is a reconstruction (~96-99% right), not a source field; the tensions table puts our own constructions
   below the source's version (eryhemato). Decision: list as a candidate only, or build it.
3. **Extension with the evaluation set and the NT endpoint** (P5/P6; REVIEW issue 3, unchanged). Labels are public;
   the bits need the Milano download behind a form. hiva_agnostic (Lennart, 2026-10-14) leans towards extending.
   Decision: fetch by hand, or leave as is.

**Agreed facts**

* 8,992 UCI rows = the VT endpoint of the ICCVAM calibration set (741 / 8,251; blocks 556 / 185; boundary 6,744);
  sha256 reproduces; CC BY 4.0.
* Label = LD50 <= 50 mg/kg = regulatory category 1 on all rows; 44 rows at exactly 50 are positive; 25% have no point
  LD50.
* Features: 1,024 structure-derived bits, no post-outcome column; best single bit AUC 0.68, drop-one costs <= 0.001.
* 477 exact copies and 22 both-class rows dropped (8,493 kept, 708 positive), per LEAK-19 / LEAK-20 and wine_quality /
  jm1; 0.0% exact copies across the split.
* Rows link to the project's structures by order (100% class agreement; flag AUC 0.998).
* RF 0.882 IID, 0.842 to 0.848 under structure clusters, ranking unchanged; near-copy gap +0.006.
* Fingerprints in scope (SEL-12): RF 0.883 matches the N3-kind kNN 0.877.
* Disputed fact settled here: 9 parents (18 rows), not 11, survive twice; all negative.

**Consistency with precedent**

* Deduplication follows wine_quality (2026-09-30) and jm1 (2026-10-01); IID follows qsar_tid_11 and the SPLIT-31 cases
  (amazon_employee_access, bank_marketing); scope follows qsar_tid_11. No departure, no prompt on this dataset.
* Approximate (if chosen) matches kick and account_debt_south_africa: a known gap, named. Direct would follow
  5g_energy_consumption only if the evaluation design counts as a practitioners' use case.
* Two prompts belong to siblings, not here (precedent agent): hiva_agnostic keeps 23 same-label copies without a stated
  fact (LEAK-19); qsar_tid_11 has no decision on 870 rows in repeated vectors (LEAK-16 Must).

</details>

<details><summary>Claim audit</summary>

**The decisive new fact (EV-1): the UCI rows can be linked back to their structures**

The UCI file has no identifier, but the project's public calibration file (`trainingset_171130.txt`, downloaded today:
8,994 rows, 741 / 8,251 / 2 blank for the VT endpoint) carries the QSAR-ready SMILES, CASRN, InChIKey and the LD50
value. Both UCI blocks (rows 1-6,744 and 6,745-8,992) are in CASRN order, so the two blocks interleave into the order
of that file. A merge alignment (dynamic programme over the interleaving; cost = class mismatch + |log bit count -
predicted log fragment count| + 26 structural flags predicted from the bits, iterated five times) gives:

* class agreement 100% (8,992 / 8,992), and the block counts 556 / 185 positives reproduced exactly;
* structural flags (halogen, S, P, N, O, aromatic, carbonyl, nitro, ring, ...) predicted from the bits of the linked
  row with mean cross-validated ROC AUC 0.998; only 9 rows contradict two or more flags strongly, 313 contradict one,
  so the linkage is right for at least ~96% and probably ~99% of rows;
* the two rows with exactly two bits set link to the two single-carbon structures, and the vector the comments
  describe (the counter-ion example) links to exactly the three salts named there.

Consequence: structures, scaffolds and exact LD50 values are recoverable for this dataset, which several claims deny.

**Claim table**

| # | Claim (short) | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | question: very toxic when swallowed, from structure alone | task_summary.question | read with 4, 22 | holds | | USE-1 |
| 2 | use case: regulator / maker screens untested chemicals | task_summary.use_case | CATMoS paper (PMC8086800) | holds | "predicting acute oral toxicity without animal testing"; a 48,137-chemical prediction set | USE-1 |
| 3 | row = one calibration chemical; 8,493 kept | task_summary.row | linkage | holds, imprecise | a kept row is a bit vector; 12 of the 406 repeated vectors cover more than one distinct parent (see 26) | USE-1 |
| 4 | target: LD50 **below** 50 mg/kg; 8% positive | task_summary.predicted | label vs LD50 column; CATMoS Methods | **refuted (wording)** | CATMoS Methods: "Very toxic (VT; LD50<=50mg/kg vs. all others)". 44 rows with LD50 exactly 50 are all positive; label == (LD50 <= 50) on 100% of rows with a value, == (LD50 < 50) on 99.3%. Label == regulatory category 1 on all 8,992 rows. 2,258 of 8,992 rows (25%) have no point LD50 at all, so their label comes from category data, not a number. Share 8.34% holds | USE-5, EV-2 |
| 5 | features: bits from the structure, salts, solvents and **stereochemistry removed** | task_summary.known | source structures | holds, one slip | 97 of 8,992 QSAR-ready SMILES still carry stereo markers; the fingerprint ignores them (two stereo pairs share a vector) | USE-3 |
| 6 | split: a test chemical **never** has its parent structure in training | task_summary.split | parent InChIKey over the shipped 3 x 3 splits | **refuted (tiny)** | 11 parents survive in two kept rows each (different vectors: tautomer / SMILES variants of the same compound); 0.15% of test rows per fold share a parent key with train (max 0.21%) | LEAK-17 |
| 7 | changes: drop exact copies and the 22 both-class rows | task_summary.changes | prep counts; code | holds | 477 + 22 | LEAK-19, LEAK-20 |
| 8 | fit = `direct` | task_summary.fit | Tanimoto (Morgan r2, 2048) to a 2/3 calibration subset for: shipped IID test rows, the project's evaluation parents, and untested parents of the project's prediction set (`predset_qsarr_2d.txt`, 48,137 rows) | **refuted (weighing)** | IID test: median nearest-neighbour similarity 0.553, 19.7% at >= 0.7, 5.1% < 0.3. Evaluation set, new parents: 0.545 / 21.7% / 5.5%. Prediction set, untested parents (3,000 sampled): 0.474 / **9.3%** / 8.0%. RF ROC AUC on the shipped repeat 0 runs 0.682 (sim < 0.5) to 0.956 (>= 0.85). Scaffold-grouped 3-fold CV (2 repeats): RF 0.843 +- 0.015 against random 0.887 +- 0.008 | USE-8, SPLIT-1, SPLIT-31 |
| 9 | fit_reason numbers 0.681 / 0.954 | task_summary.fit_reason | RF (500 trees) on shipped repeat 0, binned by nearest training Tanimoto on the bits | holds | 0.682 (n 973, 11.5%) and 0.956 (n 971) | EV-8 |
| 10-13 | year, domain, source/DOI, licence | class attributes | prep | hold | | PROV-8 |
| 14 | donor and sha256 | download_description | prep re-download | sha256 holds; the donor line is not checkable on today's source page | | EV-7 |
| 15 | bibtex (Ballabio 2019, Mansouri 2021) | bibtex | lookup | holds | EHP 129(4) 047013, doi 10.1289/EHP8495 | |
| 16-19 | target name, N_BITS, N_TRAINING_ROWS, 8,992 rows | class / docstrings | linkage, prep | hold | the block boundary at 6,744 is confirmed by the linkage | |
| 20 | VT endpoint of the project's calibration set, bits by Ballabio | opening | source file | holds | 741 / 8,251 (+2 blank) | PROV-8 |
| 21 | prediction point before any animal test | bullet Prediction point | paper 2.1 | holds | the stereo slip of 5 aside | USE-3, LEAK-10 |
| 22 | "below 50 mg/kg (paper, Sec. 2.1)" | bullet Target | as 4 | **refuted (wording)** | as 4 | USE-5 |
| 23 | paper scores NER, we keep ROC AUC | bullet Target | paper Table 3 | holds | | EV-5 |
| 24 | "Dragon 7 (paper, Sec. 2.2)" | bullet Features | paper text | **refuted (citation)** | Dragon 7 appears in Sec. 2.7; the variant (2 bits per pattern) is still unstated | writing.md |
| 25 | no constant and no duplicated bit | bullet Features | prep | holds | | CLEAN |
| 26 | repeated vectors are salt forms, hydrates and stereoisomers of one parent (406 vectors, 894 rows) | bullet Duplicates | parents per repeated vector via the linkage | **holds for 394 of 406** | 12 repeated vectors cover two or more distinct parents: hash collisions of genuinely different structures (isomer pairs, two esters of the same formula, chlorinated isomers). So the deduplication also removes about a dozen distinct chemicals, not only salt forms | LEAK-16 |
| 27 | "the project's training file shows the same 406 repeated parents by InChIKey" | bullet Duplicates | counts in that file | **refuted (number)** | full InChIKey: 405 repeated keys over 891 rows; 14-character skeleton: 406 keys over 893 rows; bit vectors: 406 over 894. The two groupings agree on 394. Both-class: 11 keys over 29 rows against 11 vectors over 22 rows | EV-2 |
| 28-29 | 477 copies, 11 vectors / 22 rows; 8,493 kept, 708 positive | bullet Duplicates | definition | hold | 8,493 x 1,025 | LEAK-19, LEAK-20 |
| 30 | the class can depend on the counter-ion | bullet Note | linkage | holds | the three salts named sit on one vector with the stated labels; the 11 both-class vectors are also free base against salt, stereo forms and isomer mixtures, i.e. real chemistry rather than label noise | |
| 31 | 3 x 3 stratified CV | bullet IID split | definition | holds | | SPLIT-2 |
| 32 | the project split "without supervised sampling ... based on structures" | bullet IID split | CATMoS Methods | holds | "semirandomly by ordering chemicals based on the five end points ... without supervised sampling of the chemicals based on structures ... equivalent distribution of the LD50 values" | SPLIT-5 |
| 33 | the file stores the authors' stratified random sets in order | bullet IID split | linkage | holds | | |
| 34 | "The file holds no structure or identifier, so a scaffold split cannot be built." | bullet IID split | the linkage above | **refuted** | structures recovered for ~96-99% of rows; 2,400 Murcko scaffolds (1,963 rows acyclic); scaffold-grouped RF 0.843 against random 0.887 | EV-1, SPLIT-5 |
| 35 | 0.681 / 0.954 applicability-domain numbers | bullet Note | as 9 | holds | | |
| 36 | "does not come from series a random split lets a model memorise" | bullet Note | scaffold-grouped CV | numbers hold, **conclusion weakened** | the near-copy probe gap is +0.006, but a scaffold split costs 0.044 AUC (3-5 fold SDs): there is chemotype-level signal beyond near copies. Analog density is class-balanced (median nearest similarity 0.697 positive, 0.680 negative) | SPLIT-29, SPLIT-31 |
| 37 | fingerprints in scope, as qsar_tid_11 | bullet Scope | - | untested (a judgment call) | | SEL-12 |
| 38 | repeat 0: RF 0.883, LightGBM 0.869, N3-kind 0.877 | bullet Scope | re-run on shipped repeat 0 | holds | RF 0.883, LightGBM 0.869, similarity-weighted kNN (sim^10) 0.877 (sim^5 0.874, sim^20 0.869) | EV-8 |
| 39-40 | the two `_decisions` | _decisions | as 26, 18 | hold (39 with the caveat of 26) | | |
| 41, 43-47, 49 | record front matter and the 2026-10-07 facts | record | source file, linkage, re-run | hold | the 741 / 8,251 cross-check against the project file is confirmed | |
| 48 | "IID, as in both source splits" | record | CATMoS Methods | holds as a source fact | the use-case question stays (row 8) | SPLIT-5 |
| 51-52 | "no known risk", "issues closed" | record | rows 4, 8, 34 | **refuted** | | |
| - | "screening lists hold many analogs of tested chemicals" | REVIEW_before, issue 2 | prediction-set similarity | **refuted** | untested prediction-set parents have half the share of close analogs of an IID test row (9.3% against 19.7% at >= 0.7) | SPLIT-1 |
| - | 237 of 2,894 evaluation chemicals have their parent in training | REVIEW_before, issue 1 | evaluation file by InChIKey | holds | 236 of 2,895 rows | |

**Refuted, ranked (validity first, Must first)**

1. **The split mirrors the source's evaluation, not the use case's screening list; `fit = direct` is overstated**
   (P3/P4; USE-8 Must, SPLIT-1 Must, SPLIT-31 Should). Untested chemicals of the project's own prediction set have
   half the close-analog share of an IID test row (9.3% against 19.7% at Tanimoto >= 0.7; median nearest similarity
   0.474 against 0.553), and the model's skill tracks exactly that axis (RF 0.682 to 0.956). A scaffold-grouped split
   costs 0.044 AUC. What it changes: the shipped number overstates what the stated actor would get on new chemistry.
   Mildest remedy: keep the IID split (after deduplication no chemical recurs, so SPLIT-29 does not trigger and a
   scaffold is not an entity new data lacks) but set `fit = approximate` and name the gap in `fit_reason` with these
   two numbers, or narrow `use_case` to the project's own evaluation design (USE-9). A scaffold-grouped variant is a
   candidate dataset, not a fix (SPLIT-31). Curator's weighing call.
2. **"The file holds no structure or identifier, so a scaffold split cannot be built"** (P4; EV-1, SPLIT-5). Refuted:
   the public project file plus the file order recovers structures for ~96-99% of rows (100% class agreement,
   structural-flag AUC 0.998). What it changes: the stated reason for IID-only is wrong, and a grouped variant,
   stereochemistry checks and the exact LD50 (a regression target) all become reachable. Mildest remedy: rewrite the
   bullet ("the file has no identifiers, but its rows can be linked to the project's structure file by order"), and
   state that IID rests on the use case, not on impossibility.
3. **The target threshold is `<=`, not `<`** (P3; USE-5 Must, EV-2). Claims 4 and 22 say "below 50 mg/kg"; the project
   defines VT as LD50 <= 50 mg/kg, 44 chemicals sit exactly at 50 and are all positive, and the label matches
   regulatory category 1 on every row. 25% of rows have no point LD50, so the label is a hazard category, not a
   thresholded number. What it changes: the written target is not quite the real-world target. Remedy: "50 mg/kg or
   less (the top regulatory hazard category)" in `predicted` and the Target bullet.
4. **"A test chemical never has its parent structure in training"** (P4; LEAK-17 Must). 11 parents survive twice
   (tautomer / SMILES variants that give different vectors); 0.15% of test rows per fold. What it changes: the
   absolute wording only; the effect on the score is negligible. Remedy: "almost never (11 parents remain in two
   rows each, 0.15% of test rows)", or drop those 11 duplicated parents using the linkage.
5. **The repeated vectors are not all one parent** (P5/P7; LEAK-16). 12 of 406 repeated vectors are hash collisions of
   genuinely different chemicals, so the deduplication silently drops about a dozen distinct compounds. Remedy: one
   clause in the Duplicates bullet.
6. **"The project's training file shows the same 406 repeated parents by InChIKey"** (EV-2). Measured: 405 keys / 891
   rows (full key) or 406 / 893 (skeleton), overlapping the 406 vectors in 394 cases. Remedy: correct the number.
7. **Citation slip** (writing.md): Dragon 7 is named in Sec. 2.7, not 2.2.
8. **"No known risk" / "issues closed"** in the record's 2026-10-20 assessment (procedure): rows 1-3 above are open.

**Untested, and why**

* Whether the 1,024 bits really are ECFP_1024_02 or _02R: the generating software is not available here. The bit
  counts (median 89, max 911) are consistent with a 1,024-bit hashed fingerprint at 2 bits per pattern, and the two
  single-carbon rows set exactly 2 bits.
* The donor line on the source page (`creators: []` today) and the "matches the citation request" phrase.
* Whether a graph model would clearly beat tabular models on the recovered structures (SEL-12): not run; now
  possible via the linkage, and the honest test of the scope claim (37).
* The extension with the evaluation set and the second endpoint: the descriptor package still needs a web form.
  Note that the labels of both are public in the project files downloaded here, so only the bits are missing.

**What held against the hardest tests**

Features are all known at the prediction point (only structure-derived bits exist); real data (no generation flags);
the class share, both source block counts, both decision tables, the applicability-domain numbers and the repeat-0
model comparison all reproduce; copies across the split are gone except for the 11 parents above; the IID score is not
inflated by congeneric series the probes missed in the near-copy sense (gap +0.006) — the cost appears only at the
scaffold level (0.044).

</details>

<details><summary>Column audit</summary>

Inputs: the definition (prediction point: "a chemical without an acute oral toxicity test, before any animal test";
`task_summary.known`: 1,024 fingerprint bits of the QSAR-ready structure), Ballabio et al. 2019 (Sec. 2.1, 2.2, 2.7,
3.1, Table 2), the probes, and the frame rebuilt from the definition.

**Measurements on the cleaned frame**

* 8,493 rows x 1,025 columns: 1,024 `int64` bits, target `category` (No 7,785 / Yes 708). No missing value, no value
  other than 0/1 (raw file too: only 0 and 1 in the bit columns; target only `positive` / `negative`, so the map
  leaves no NaN).
* Bit density: min 0.65% (no bit with fewer than 5 ones), median 4.5%, max 92.0%. No constant bit, no two equal bits,
  no complementary bits; 21 bit pairs with |r| > 0.95 (max 0.981), not copies.
* Bits set per row: min 2 (one row, the single-carbon structure; 2 bits per fragment), median 89, max 911. The count of
  bits set alone gives ROC AUC 0.467 (no size artefact by class).
* No remaining duplicate feature row (0).
* Row order: the frame is shuffled by the pipeline (`order_rows`, seed 42); Spearman of frame position against the raw
  file position 0.004; next-row label agreement 0.848 = chance (0.847). The authors' train/test block order and the
  CASRN-like order inside the blocks do not survive (CLEAN-23 holds).
* `_clean` assigns `df = raw` and renames in place; safe, because the framework passes `_copy(self.raw)` and
  `_decisions` gets the untouched raw frame.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `ecfp_1` ... `ecfp_1024` (all 1,024 bits, one kind) | Presence (1) or absence (0) of the circular fragments hashed to this position of a 1,024-bit binary ECFP computed by Dragon 7 on the QSAR-ready structure (salts, solvents, stereochemistry removed), radius up to 2, 2 bits per fragment (paper Sec. 2.2, 2.7, Table 2; the variant is ECFP_1024_02 or _02R, the file does not say which; 2 bits set on the single-carbon row rules out _05). Which fragments map to a given bit: unknown (hashed, with collisions, Sec. 2.2). | Yes. Computed per molecule from the structure alone, which exists before any test; no label, no assay value, no all-row statistic enters a bit. | `int64` 0/1, no missing, no proxy codes, no impossible values, not constant, no copies; names in file order, as no bit has a documented meaning. | fine | LEAK-10, LEAK-27 to LEAK-30, CLEAN-5, CLEAN-9, CLEAN-14 |
| `ecfp_283` (singled out: best single feature, AUC 0.680; drop-one -0.001) | as above | Yes | as above | fine: an ordinary structural bit, not a near-copy of the label | LEAK-5, LEAK-10 |
| densest bit (92% ones) | as above; most likely a bit hit by a near-universal atom environment (e.g. an sp3 carbon) | Yes | as above; not constant | fine | CLEAN-5 |
| `very_toxic` (target) | "Yes" if the experimental rat oral LD50 < 50 mg/kg ("positive" in the file), else "No"; for several values the median of the lower quantile (paper Sec. 2.1) | target | `category` Yes/No, 741 / 8,251 in the raw file (= Table 1), 708 / 7,785 after deduplication | fine | CLEAN-15, USE-5, LEAK-4 (no change of the target) |
| (absent) identifiers, CASRN, SMILES, InChIKey, counter-ion | not in the UCI file | - | nothing to drop or turn into meaning; no RDKit descriptors can be built (CLEAN-24 not applicable without structures) | fine; see problem 3 | CLEAN-3, CLEAN-24 |

No column is post-outcome, no missingness exists (so none can be caused by the outcome), there is no time window, and
no id encodes the label.

**Problems, ranked by principles.md**

No validity problem (P1-P5) at the column level. Every finding below is P4-weak or P7.

1. **P4, LEAK-31 (Should), very weak, no remedy needed (note optional).** The fingerprint settings (radius 2, 2 bits per
   fragment, with or without SSSR) were picked by the authors' internal cross-validation on their 6,744 training
   molecules (paper Sec. 3.1: "Internal cross validation was performed on the training molecules to ... select the
   best set of molecular descriptors"; VT models used ECFP_1024_02, NB _02R). That is a supervised choice among three
   unsupervised hashings, made with the labels of 79% of our rows; it does not select bits or fit any value, and every
   one of the three alternatives is a standard fingerprint. Not measurable without the other variants, and far below
   LEAK-30's "strong". Mildest remedy: none, or a half sentence in the Features bullet. Not a reason to change anything.

2. **P4, LEAK-20 (Should): the 11 both-class vectors (22 rows) dropped; already settled, consistent.** The class differs
   within a vector because the parent structure strips the counter-ion (comments: sodium / potassium cyanide vs silver
   cyanide). LEAK-20 keeps such rows only when the ambiguity is one "the task has"; in the real use case a screener has
   the full salt structure, so the ambiguity is made by the featurisation, not by the task, and the drop follows the
   rule (jm1 precedent). No change.

3. **P3/P7, known-but-missing input (not a leak), note exists.** The salt form, counter-ion and stereochemistry are known
   at the prediction point but absent from the features (the QSAR-ready step removed them, Sec. 2.1). This weakens the
   signal rather than inflating it; the counter-ion note in `curation_comments` covers it. Nothing to recover: the file
   has no identifiers (CLEAN-24 cannot apply).

4. **P7, CLEAN-14 (Should): dtype of binary bits differs across the fingerprint siblings; question for the curator.**
   Here the bits are `int64` 0/1 (lossless and the natural form for a binary presence flag); `hiva_agnostic` ships its
   binary features as `category`, `qsar_tid_11` as `float64`. Nothing is wrong in this dataset; a single house
   convention for 0/1 fingerprint bits would be cleaner. Mildest remedy: none here; decide the convention once.

5. **Procedure (writing.md): the Features bullet.** It cites "Dragon 7 (paper, Sec. 2.2)"; Dragon 7 is named in Sec. 2.7
   (Sec. 2.2 describes ECFPs). The variant (ECFP_1024_02 or _02R, radius 2, 2 bits per fragment; hashed, so a bit has
   no one-to-one fragment meaning) is not stated, although the earlier REVIEW.md says it is. Remedy: edit the bullet,
   e.g. "binary extended connectivity fingerprints (paper, Sec. 2.2; computed with Dragon 7, Sec. 2.7), radius 2 with 2
   bits per fragment (ECFP_1024_02 or _02R of Table 2; the file does not say which), 1,024 hashed bits ...". No data
   change.

Checked and clean: CLEAN-2 (no encoding, imputation or scaling of ours), CLEAN-3 (no identifier), CLEAN-5 (no
constant or copied column), CLEAN-6/7 (nothing built from labels or all-row statistics), CLEAN-9 (no object column),
CLEAN-10/11 (no proxy or impossible values), CLEAN-12/13 (no one-hot block: rows set 2 to 911 bits), CLEAN-15 (no
missing target), CLEAN-22 (all 1,024 bits kept), CLEAN-23 (rows shuffled; order signal gone), LEAK-16 to LEAK-19
(0 duplicate feature rows remain; 0.0% exact copies across the split per leak probe 5).

</details>

<details><summary>Split audit</summary>

Models: random forest 300 trees, LightGBM 300 x 0.05, logistic C=0.1, similarity-weighted Tanimoto 5-NN; ROC AUC
averaged over 3 folds.

**Verdict: right with notes**

Declared: IID, stratified 3-fold x 3 repeats over 8,493 deduplicated chemicals (5,662 / 2,831 per fold). That is the
regime the use case implies. The note is the measured optimism of a random split over analog chemicals, which is
modest, leaves the model ranking unchanged, and matches the source's own blind validation. No re-split.

**Regime implied by the use case (SPLIT-1, SPLIT-3, USE-10, USE-11)**

* The actor screens a chemical with no animal test: a new entity each time (cold start). There is no history to use,
  so temporal does not apply. After the deduplication each parent structure is one row, so one row per entity: by
  USE-11 this is IID without grouping. Identical parent structure gives an identical bit vector, so the claim "a test
  chemical never has its parent structure in training" holds on every shipped fold (leak probe 5: 0.0% exact copies
  across the split). This holds without the unverified InChIKey cross-check.
* Temporal: no time column, and none implied (SPLIT-7 does not apply). LD50 is a fixed property of a chemical, the
  rows are a compiled database and not a stream, and the project split on the LD50 distribution, not on time.
* The source's splits are both random (SPLIT-5, SPLIT-19 checked): Ballabio Sec. 2.1 says "randomly splitting the
  calibration set ... (stratified splitting)". The project's calibration/validation split was "semi-randomly divided
  ... equivalent coverage with respect to LD50 distribution". The project's blind validation set, embedded in the
  48,137-chemical prediction set, scored like the random test set (N3 NER 85% test / 86% validation; BNN out-of-domain
  27% / 28%, paper Sec. 3.2). So the real external hold-out behaved like an IID hold-out of this pool.

**Measurements**

| Split | RF | LightGBM | logistic | Tanimoto 5-NN | test NN Tanimoto median | test rows with NN < 0.5 |
|---|---|---|---|---|---|---|
| shipped IID, repeat 0 | 0.882 (0.889 / 0.874 / 0.884) | 0.869 | 0.856 | 0.842 | 0.68 | 11.5% |
| authors' split (file blocks, deduplicated; 1 split) | 0.896 | | | | 0.68 | 12.1% |
| raw-order blocks of 50 rows, grouped 3-fold | 0.866 (0.843 / 0.888 / 0.868) | | | | 0.67 | 13.0% |
| connected components at Tanimoto 0.7 (4,878, largest 424), grouped | 0.842 | | | | 0.59 | 17.4% |
| Butina leader clusters at 0.5 (2,302, largest 208), grouped | 0.842 (0.851 / 0.820 / 0.856) | 0.831 | 0.805 | 0.782 | 0.57 | 29.0% |
| Butina leader clusters at 0.4 (1,097, largest 981), grouped | 0.848 | | | | 0.58 | 24.3% |

At 0.5 and 0.4, connected components form a giant component (82.5% and 97.4% of rows), so those cuts cannot be used.

Applicability gradient on shipped repeat 0, by the test row's nearest training similarity: [0, 0.5) 11.5% of test rows,
AUC 0.675; [0.5, 0.7) 43.1%, 0.814; [0.7, 0.85) 34.0%, 0.943; >= 0.85 11.4%, 0.957. This reproduces the notes' 0.681 /
0.954 within seed noise. The positive share is flat across bins (7.3-9.7%).

Raw file order: consecutive rows are far more alike than random pairs (mean Tanimoto 0.246 against 0.168; >= 0.5 for
10.8% against 0.2%). Next-row class agreement is 0.869 against 0.847 by chance. The file order clusters related
chemicals (consistent with CASRN or name order). It is not a time order, and the pipeline shuffles rows before
splitting.

**Problems, ranked (principles.md: all under P4)**

1. **A random split over analog chemicals is mildly optimistic** (SPLIT-31 Should, applied via SPLIT-29/30 and EV-3;
   SPLIT-24 Must bars the clusters as a key).
   * Evidence: holding out structure clusters costs 0.034-0.040 AUC for RF (0.882 to 0.842-0.848) and LightGBM (0.869
     to 0.831). It costs 0.051 for logistic and 0.060 for the memorising Tanimoto 5-NN (0.842 to 0.782). The model
     ranking is unchanged (RF > LightGBM > logistic > 5-NN under both splits). The hidden-group probe has no hit: its
     near-copy gap is +0.006, 11.2% of rows sit in clusters of 2+ at 0.85, the largest has 25 rows, and no column or
     composite key counts.
   * Rule reading: after the deduplication no entity recurs, so SPLIT-29 (a shared entity that new data would not have)
     is not triggered. A similarity cluster is barred as a group key (SPLIT-24), and the file has no structure for a
     scaffold key, so SPLIT-25 does not apply either: the real entities (parents) are already one per row. The source's
     blind external validation scored like its random test. This is the SPLIT-31 case (amazon_employee_access,
     bank_marketing): IID matches the framing, optimistic over related entities, a candidate for a grouped variant.
   * Remedy (mildest): keep the split. Add the cluster-split cost to the "Note" bullet of `curation_comments` (for
     example: "held out by structure clusters (Butina, Tanimoto 0.5) a random forest falls from 0.882 to 0.842,
     ranking unchanged"). Optionally list it as a SPLIT-31 candidate for a scaffold variant if the NTP structures are
     ever linked. Under SPLIT-4 the size of the gap never decides on its own.

2. **The deduplication removes the "salt form of a known parent" case from the test side** (LEAK-16 to LEAK-21 Must,
   satisfied; SPLIT-26 Should, weighed).
   * Evidence: before the drop, 7.6% of the authors' test molecules had an exact bit-vector copy in their training set
     (earlier round). The project's blind validation had 8.2% of chemicals with their parent in the calibration file
     (stated earlier, not re-measured: NTP files absent). After the drop, 0% on every fold.
   * Reading: the shipped test is slightly harder than the project's validation and matches "new parent structure",
     which is the use case (a known parent is read across, not modelled). This is conservative, not a defect. The
     alternative (keep the 8,992 rows, group on the bit vector, SPLIT-24 "identical values in the columns that define
     the entity") would also guarantee new parents. It would keep the 22 conflicting rows and weight parents with many
     salt forms more. The earlier verification closed this in favour of the drop. I see no split reason to reopen it.
   * Remedy: none.

3. **Raw order is structure-clustered, not temporal** (SPLIT-22 Should, SPLIT-7 Must; not triggered).
   * Evidence: consecutive-row similarity above. A grouped split on 50-row blocks of the file order costs 0.016 AUC
     (0.866).
   * Reading: there is no time axis behind the order (LD50 is a fixed property; the order looks like CASRN or name
     order), so it is not a missing timestamp.
   * Remedy: none. The pipeline shuffles before splitting, so the folds do not depend on the order.

**Other checks**

* Fold sizes and class balance: 236+ positives per test fold (task probe). Stratification on `very_toxic` is right for
  8.3% positives. 3 x 3 is the default protocol for this size.
* No `splits_comment` (IID). The `task_summary.split` text is accurate. One wording point: "kept once" is true only
  for same-class copies; copies with both classes are dropped entirely, which `changes` states.
* Grouping, temporal gap, label delay, training history and season windows: not applicable (IID, no time axis).

</details>

<details><summary>Domain practitioner</summary>

I am the computational toxicologist in a regulatory programme (NICEATM/ICCVAM-style) or in the product-stewardship
group of a chemical maker. My job: a list of chemicals with no acute oral study has to be triaged. I decide which ones
get flagged as acute-oral hazard class 1-2 (the "below 50 mg/kg" bin, the "fatal/toxic if swallowed" label), which go
first into testing or further assessment, and which can be set aside. Today I make that call with read-across to
analogues, expert rules and QSAR suites such as OPERA/CATMoS, whose five endpoints are the very-toxic flag, the
non-toxic flag, the EPA category, the GHS category and the LD50 point estimate. Each prediction comes with an
applicability-domain index and the nearest training analogues, and I look at those before I act.

**Verdict**

**Fit: direct** (USE-8). The input is a structure-derived descriptor block that exists before any study is done, the
label is the endpoint the programme itself models, and one row is one chemical, which is one triage decision.

**1. Do I have these inputs at the prediction point?**

Yes, all of them (USE-3, USE-6). The 1,024 bits are a hash of the molecular graph of the QSAR-ready parent structure.
Anything I want to screen I have drawn as a structure first, so there is nothing here recorded after the outcome, and
no field that is blank because a study already happened (LEAK-10 does not bite). No row lacks the input the decision
acts on, so USE-7 is satisfied without dropping anything.

What I would have and the file does not carry: physicochemical descriptors, the structure itself (for read-across and
for showing a case officer *why*), in vitro or related-endpoint data, and the identifier. That is a narrower feature
set than my desk, not a wrong one: USE-6 is about not dropping something I have, and nothing here was dropped to make
the task harder. It does cost me two things in deployment, below.

**2. Is the target what I act on?**

Close. The very-toxic flag is one of the five endpoints of the programme, and 50 mg/kg is a real class boundary, so I
act on this flag directly when I sort a list into "label as acute hazard 1-2" and "not". But most of the time I want
the graded answer: the GHS or EPA category, or the LD50 estimate, because my downstream obligations differ between
categories 1, 2, 3 and 4, and a single binary bin collapses them. The dataset ships only the stricter of the two
binary endpoints, and the better-balanced companion endpoint (the "non-toxic" flag) is not here (USE-5: the target is
the real one, just one slice of it).

I want a **probability**, not a class: my threshold moves with how much testing capacity I have, and with how costly a
miss is for that product line. ROC AUC is a fine benchmark metric for that, with the caveat that the class is 8.3%
positive and what I actually live with is the top of the ranking. I measured that on the shipped rows (random forest,
3-fold stratified): ROC AUC 0.885, average precision 0.623, precision 0.76 and recall 0.46 in the top 5% of the ranked
list, precision 0.55 and recall 0.66 in the top 10%, against a base rate of 8.3%. That is a 6-9x enrichment: a usable
triage list. Nothing in the collection's metric choice misleads me here (EV-5).

**3. One row, one decision; is the test set what I face?**

One row is one chemical, one triage decision. No chemical repeats after the deduplication, so there is no entity with
a history and no cold-start question to answer: USE-10 resolves to "a new entity every time", and USE-11's one-row-per
-entity condition is met by construction rather than by throwing rows away.

The test rows are chemicals of the same curated reference set, drawn at random. The chemicals I actually screen are a
much larger inventory list that is, on average, structurally further from the tested set. So my test error is
optimistic relative to my inventory, which is the applicability-domain gap that `fit_reason` already states (ROC AUC
0.68 for test chemicals with no close analogue against 0.95 for those with a very close one). I accept that it stays
"direct" rather than "approximate": both source protocols split at random, the parent-structure copies were removed,
and the hidden-group probe finds no congeneric series to memorise (gap +0.006). Under USE-9 this is the honest
use case the data mirrors (screen within a reference set), not a use case rephrased to excuse a gap.

**4. Would I use this model, and what would I distrust?**

I would use it as a ranking for triage, not as a labelling decision on its own; that is how I use CATMoS today.

Trust: the endpoint and the threshold are the programme's own; the features cannot leak, by construction; the
deduplication of parent-structure copies means the headline number is not inflated by salt forms sitting on both sides
of the split, which is exactly the mistake I would otherwise make myself.

Distrust, in the order it would bother me:
1. No applicability-domain index and no nearest-analogue list comes with a prediction. For a chemical far from the
   reference set the model is near-useless and I would not know it from the output.
2. The bits are hashed and unnamed, and were computed with commercial software. I cannot explain a flag to a case
   officer from feature 283, and I cannot compute the inputs for a new chemical without that software.
3. The counter-ion is invisible. Salt forms of one acid can differ in this endpoint, and the parent-structure
   descriptors cannot see that.

**Gaps between the dataset and my decision, ranked**

| # | Gap | Why it matters to me | How much it changes the task |
|---|---|---|---|
| 1 | No applicability-domain signal, and the random test set is closer to training than my inventory is | I act on the score only inside the domain; the benchmark number is the in-domain number | Large for deployment, small for the benchmark: it is stated in `fit_reason` and both source protocols are random (USE-8, USE-9, SPLIT-1) |
| 2 | One binary endpoint of five; no graded category, no LD50 estimate, no companion "non-toxic" flag | My duties differ between classes; the binary bin is the coarse version of what I act on | Moderate; the flag is still a real endpoint, so USE-5 holds. The companion endpoint would be a second, better-balanced task |
| 3 | Hashed, vendor-specific bits; no structure, no identifier | I cannot explain, read across, or recompute inputs | Moderate for use, none for the benchmark; it also makes a scaffold split impossible here |
| 4 | Salt forms collapsed and the 11 contradictory vectors dropped (22 rows) | Those are exactly the cases I get wrong in deployment, where the counter-ion drives the class | Small (0.26% of rows); the right call for a split, and the note already says so |
| 5 | Calibration set only; the programme's separate evaluation set is not here | I would want the held-out set as the honest estimate | Small for the benchmark; it is the open extension in the review file |

**What an expert in my field would change**

* Ship a per-prediction similarity-to-training number alongside the score, or at least report the score split by that
  similarity in the README, so a reader sees the in-domain and out-of-domain numbers side by side. (No change to the
  task; the note already has the numbers.)
* Prefer the graded endpoint if a version with it ever becomes available, and add the companion "non-toxic" endpoint
  as a second, better-balanced task from the same chemicals.
* Report a top-of-list number (average precision, or precision at the top 5%) next to ROC AUC for this 8.3% class,
  because triage is a ranking decision.
* Keep the deduplication as implemented. Alone among the alternatives it matches how I would evaluate: a parent
  structure I have already tested must not be sitting in my training set when I claim to predict it.
* Nothing I would change makes the shipped dataset less of a real decision. It is one of the cleaner regulatory
  screening tasks I have seen as a benchmark row.

Sources: Ballabio et al. 2019, Mol. Inf. 38(8-9) 1800124; Mansouri et al. 2021, EHP 129(4) 047013 (CATMoS); NICEATM /
ICCVAM material on CATMoS, its five endpoints and the hazard-category boundaries
(https://ntp.niehs.nih.gov/iccvam/meetings/ascct-2019/mansouri-abstract-508.pdf ,
https://ntp.niehs.nih.gov/ntp/about_ntp/sacatm/2021/session_2b_public_writeup_fd-508.pdf ,
https://www.altex.org/index.php/altex/announcement/view/136 ).

</details>

<details><summary>Blind review</summary>

Review of the dataset as handed over, with the target `very_toxic`, without our notes or rules.

**Verdict**

Include. It is a real, cleanly deduplicated QSAR toxicity task with clear signal and no leakage. I have only minor
notes on documentation and on the split.

**What the task is**

This is the CATMoS / ICCVAM-US EPA acute oral toxicity collaboration (Ballabio, Grisoni, Consonni, Todeschini, Mol.
Inform. 38(8-9), 2019, doi:10.1002/minf.201800124). There are 8,992 chemicals. "Very toxic" means rat oral LD50 < 50
mg/kg, which is the GHS/EPA hazard category. Regulators and chemical or pharma companies screen compounds that have no
animal data, to rank them or replace the animal test. This is a real use. The prediction is made from structure alone,
so no feature can be unknown at prediction time.

**Checks performed**

- Prepared table: 8,493 x 1,024 binary int columns (`ecfp_1..1024`) plus the categorical target (No 7,785 / Yes 708,
  8.3% positive). It has no missing values, no constant columns and no duplicate feature rows.
- Comparison with the original UCI CSV (8,992 rows; 741 positive): 8,504 distinct fingerprints. 406 fingerprints occur
  more than once (one occurs 12 times). Only 11 groups (29 rows) have conflicting labels. 8,504 - 11 = 8,493, so the
  preparer collapsed the exact duplicates and dropped the conflicting groups. Every prepared row matches an original
  fingerprint, and every label agrees with the original. This is correct handling: without it, a random split would put
  copies of the same molecule in train and test.
- Signal (3-fold stratified CV, ROC AUC): logistic regression 0.859, random forest 0.886, LightGBM 0.881. The task is
  not trivial and not saturated.
- Near duplicates: the median Tanimoto similarity to the nearest other row is 0.71. 5.4% of rows have a neighbour with
  similarity >= 0.9. 1-NN label agreement is 92.6% overall but only 55.6% for positives. Analogue series are present,
  as expected for QSAR, but they do not dominate.

**Concerns, most to least serious**

1. **The random IID split is optimistic compared with real use.** In use, new chemicals are often structurally novel;
   the original study validated blind on an external set. The table has no SMILES, so a scaffold or cluster split
   cannot be built from the released data. One option is a Tanimoto-cluster group split on the fingerprints
   themselves, but that is optional. The 5.4% of rows with a close analogue (>= 0.9) is modest, so I would keep IID
   and document it.
2. **Fingerprint provenance is undocumented.** UCI says only "1024 binary attributes (molecular fingerprints)". The
   `ecfp_` names are an assumption, and the radius and settings are not given. One row has 911 of 1,024 bits set,
   which looks like a very large molecule or a hashing artefact. Plausible, but worth a note. I would state in the
   metadata that the fingerprint type is assumed.
3. **Dataset character.** The data is 1,024 sparse binary columns with no other features. This is a high-dimensional,
   homogeneous fingerprint task rather than a typical heterogeneous tabular one. It is useful for diversity, but it
   tests a narrow regime and is wide for some foundation models' feature limits.
4. **Class imbalance (8.3%).** Fine for AUC or log loss. With 3 folds, each test fold has about 236 positives, which
   is enough to score.
5. **Preparation is minor.** The features are int64; bool or uint8 would be lighter. The target is categorical No/Yes,
   which is fine.

**What I could not check**

- The michem.unimib.it page and the full paper returned HTTP 503 or were paywalled. I could not confirm the
  fingerprint type, the exact label threshold beyond the abstract (LD50 < 50 mg/kg), or whether the 8,992 chemicals
  already contained salts or stereoisomer duplicates, which would explain the fingerprint collisions.
- I could not verify whether any of these chemicals overlap with other benchmark datasets (for example, other CATMoS
  endpoints).
- I did not run the exact 3x3 benchmark splits; the baselines use one 3-fold repeat.

Sources: https://archive.ics.uci.edu/dataset/508/qsar+oral+toxicity ; https://boa.unimib.it/handle/10281/213189 ;
https://michem.unimib.it/download/data/acute-oral-systemic-toxicity/ (503)

</details>

<details><summary>Precedent check</summary>

Checked against `principles.md` ("Consistent judgement", "Exceptions and amendments", "Tensions"), `leak_checks.md`
(LEAK-16 to LEAK-21), `splits.md` (SPLIT-24 to SPLIT-31), `selection.md` (SEL-12), `task_probes.md` ("Hidden groups"),
the register and the sibling molecule definitions. Sibling numbers below were measured today by running each sibling's
`_load_raw` and `_clean`.

The register flags for this dataset are only its own open issues filed under LEAK-16, LEAK-21, SPLIT-24 and
"duplicate rows"; none of the four cross-dataset flags (opposite outcomes, drift, third exception) involves it.
Note: the register's LEAK-21 tag on issues 1 and 2 is a keyword artefact (LEAK-21 is reposts, emscad); the rules that
apply are LEAK-19 and LEAK-20.

**Summary**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1a | Drop 477 same-label exact copies (LEAK-19) | consistent with the rule and with wine_quality / audiology; **one sibling decided the other way: hiva_agnostic keeps its 23 same-label copies, with no reason given** | wine_quality (Lennart, 2026-09-30), audiology_diagnosis (case table), hiva_agnostic (AI, 2026-10-14, in the change Lennart asked for that day) |
| 1b | Drop all 22 rows of the 11 both-class vectors (LEAK-20) | consistent with jm1 and drug_induced_autoimmunity_prediction; the "unless genuine label ambiguity" clause is arguable but jm1 dropped real, distinct entities too | jm1 (Lennart, 2026-10-01), drug_induced_autoimmunity_prediction (streptomycin, follows this dataset) |
| 1c | Alternative of issue 1 (keep 8,992 rows, group on the bit vector) | would be a departure from LEAK-19 (Should); a distinguishing fact exists (the entity is the parent structure, not an unknown one) so it is not barred by SPLIT-24's maternal_health_risk case, but it needs to be recorded as an exception | maternal_health_risk (SPLIT-24, hash of the feature vector barred), superconductivity (SPLIT-26, grouped, copies had different targets) |
| 2 | IID split, no scaffold split | consistent | qsar_tid_11 (IID kept, near copies 35%, gap 0.035; calibration 2026-10-12), bioresponse, qsar_biodeg, qsar_bioconcentration, hiva_agnostic (all IID random molecules); emscad (SPLIT-24, similarity cluster barred); amazon_employee_access / bank_marketing (SPLIT-31) |
| 3 | UCI calibration set only; evaluation set and NT endpoint left open | open, curator's call; one curator precedent leans towards extending when the labels and features can be had | hiva_agnostic (CC Lennart 2026-10-14: add the challenge's 384 validation compounds) |
| 4 | Fingerprints in scope (SEL-12) | consistent | qsar_tid_11 (TabArena v0.1, Lennart "tend towards yes"), hiva_agnostic, musk |
| 5 | domain "chemistry & material science" | no rule; the toxicity sets are split between two domains; the earlier review file misnames one sibling | see below |
| - | ROC AUC instead of the paper's NER; no accepted warnings | consistent (collection metric; `dataset check` 0 warnings) | |

No drift and no third exception: Lennart's duplicate decisions run drop (wine_quality 2026-09-30, jm1 2026-10-01),
keep only for natural repeats on few features (sepsis_survival_minimal_clinical_records 2026-10-06, LEAK-18), which is
the rule's own split, not drift.

**1. Parent-structure copies dropped**

**1a, same-label copies (477 rows).** LEAK-19 (Should): "Exact copies with the same label: drop them rather than group
on the duplicate key." Follows wine_quality (CC Lennart 2026-09-30: 1,177 copies dropped, split stays IID) and
audiology_diagnosis (27 copies on different ids). LEAK-17 (Must) is met too: one row per repeated molecule. The source
keeping its rows ("No molecules were removed") does not set the case apart: wine_quality's source also kept its copies.
Consistent.

Sibling decided the other way. Measured today on the shipped definitions:

| dataset | features | rows | exact copies (label included) | rows sharing a feature vector | of them with differing labels | documented |
|---|---|---|---|---|---|---|
| qsar_oral_toxicity | 1,024 ECFP bits | 8,493 (from 8,992) | 0 (477 dropped) | 0 (894 before) | 0 (22 dropped) | yes |
| hiva_agnostic | 1,617 descriptors | 4,229 | 23 | 46 | 0 | "23 compounds repeat another's descriptors, always with the same label (3 of them across training and validation), and stay." No reason given |
| qsar_tid_11 (regression) | 1,024 FCFP bits | 5,741 | 116 | 870 in 387 vectors | 684 (pChEMBL differs; within-vector SD median 0.25 against 1.54 overall) | not mentioned |
| qsar_biodeg | 41 descriptors | 1,055 | 3 | 6 | 0 | not mentioned |
| drug_induced_autoimmunity_prediction | RDKit descriptors | 587 | 0 | 0 | 0 | yes, dropped "as for qsar_oral_toxicity" |
| qsar_bioconcentration | 9 + RDKit descriptors | 776 | 0 | 0 | 0 | yes, repaired with RDKit descriptors from the SMILES (a distinguishing fact: structures available) |

So qsar_oral_toxicity follows the rule and the curator's precedents; the outlier is hiva_agnostic (keep, a departure
from LEAK-19 without a stated fact), and qsar_tid_11 has no recorded decision on 15% of its rows sharing a fingerprint,
which LEAK-16 (Must: "Duplicate rows need a decision every time") requires. qsar_tid_11 is the scope precedent this
dataset cites, so the question "Would I decide the same for its sibling datasets?" lands on it directly.
These are questions on the siblings, not on this dataset's decision.

**1b, both-class vectors (11 vectors, 22 rows).** LEAK-20 (Should): drop every copy, "unless they are genuine label
ambiguity the task has". The definition's own note (sodium and potassium cyanide very toxic, silver cyanide not; the
parent structure does not show the counter-ion) reads like the unless clause: a screener meeting a new salt form sees
the same bits. Steelman of the drop: jm1 (CC Lennart 2026-10-01) dropped 88 conflicting vectors that were also real,
distinct modules with the same metrics, "to be on the safe side", and drug_induced_autoimmunity_prediction dropped both
streptomycin rows on the same reasoning; 22 of 8,515 rows cannot move the score. Consistent with jm1; no prompt. If the
curator reads the unless clause as covering counter-ion chemistry, that would reopen jm1's reasoning as well, so it
would be an amendment of LEAK-20, not a one-off.

**1c, the alternative (keep 8,992 rows, group on the bit vector).** Departs from LEAK-19 (Should, "rather than group").
SPLIT-24 (Must) bars "a hash of the feature vector standing in for an unknown entity" (maternal_health_risk, retired).
The fact that would set this case apart: the entity is known, the QSAR-ready parent structure the bits are computed
from (the record says the NTP training file shows the same 406 repeated parents by InChIKey; prep did not download
that file, so the fact was unverified at the time). SPLIT-26 (Should, "keep the source's rows") is the argument for
it, but it sits in Part 4 and LEAK-19 in Part 3, and superconductivity (grouped, 2026-10-06) differed by having
different targets per composition. Choosing the alternative is a reasonable exception only with the InChIKey match
verified and recorded as `Exception to LEAK-19`.

**2. Random split while the score depends on close analogues**

Consistent. After deduplication no molecule repeats, so SPLIT-29 (Must, a shared entity new data would not have) is
not triggered; the near-copy probe calibration (`task_probes.md`, "Hidden groups", 2026-10-12) lists this dataset at a
gap of 0.006 against qsar_tid_11's 0.035 (IID kept). SPLIT-24 bars a similarity-threshold cluster as a group key
(emscad, TF-IDF cluster barred), and SPLIT-30 says the gap never decides. Every sibling molecule set is IID random
(qsar_tid_11, bioresponse "as no structure is given to group them", qsar_biodeg, qsar_aquatic_toxicity,
qsar_fish_toxicity, qsar_bioconcentration, hiva_agnostic, clock_protein_toxicity). The tension row "The right split
against the score (P4 over P6)" (forest_fires) is respected: the split follows the use case, not the gap. A scaffold
variant would be a SPLIT-31 candidate (a variant, not a fix), as for amazon_employee_access and bank_marketing.

One fact for the claim auditor, not a consistency issue: the "both source protocols are random" premise rests on
Mansouri et al. 2021, which prep did not read, while Ballabio et al. Sec. 2.1 calls the project split "semi-random"
with "equivalent coverage". Semi-random by coverage is still not a structure-grouped split, so the conclusion holds
either way.

**3. Only the calibration part on UCI**

Open, the curator's call; nothing to compare a decision against yet. The closest curator decision: hiva_agnostic,
CC (2026-10-14, Lennart): "Add the 384 validation compounds", when the source's further labelled compounds had the same
features and were in a file already fetched. What sets this case apart: the evaluation set's fingerprints need a
download behind a name-and-e-mail form that this machine cannot reach, and up to 8.2% of those chemicals have their
parent in the training file (more deduplication). The NT endpoint would be a second task on a shared source, which the
tension row "Uniqueness against a distinct task" (PROV-6, PROV-7) allows.

**4. Fingerprints in scope**

Consistent with SEL-12 ("Vectorized ... data is fine where tabular models are competitive", judged per dataset) and
with qsar_tid_11 (1,024 FCFP bits, shipped in TabArena v0.1; Lennart "tend towards yes") and hiva_agnostic. The
per-dataset evidence (random forest 0.883 against a nearest-neighbour model of the paper's kind, 0.877) is what SEL-12
asks; a graph model on structures cannot be run from the file alone.

**5. Domain**

No rule decides `domain`; it is metadata, not a curation decision, so no prompt. For the curator's convenience the
values among molecule toxicity and QSAR sets today:

* chemistry & material science: qsar_oral_toxicity, qsar_tid_11, hiva_agnostic, clock_protein_toxicity,
  qsar_bioconcentration, musk;
* biology & life sciences: qsar_biodeg, qsar_aquatic_toxicity, qsar_fish_toxicity, bioresponse, apistox;
* medical & healthcare: drug_induced_autoimmunity_prediction.

The earlier review file lists clock_protein_toxicity under "biology & life sciences"; its definition and record say
"chemistry & material science". The split is not by endpoint (fish and bee toxicity in biology, rat oral and
clock-protein toxicity in chemistry).

**Consistency prompts**

Every decision on qsar_oral_toxicity follows a rule and a precedent, so it gets no prompt. The one real pair of similar
cases decided differently is with a sibling, and one sibling has no decision on file; one prompt each, to be filed on
the sibling and not here:

**Consistency check (AI, 2026-10-20):** hiva_agnostic keeps its 23 compounds that repeat another's descriptors with
the same label (2026-10-14, written by the AI in the change you asked for that day, no reason given), while
qsar_oral_toxicity drops its 477 (LEAK-19, as wine_quality, Lennart 2026-09-30). Same mechanism: exact copies of a
compound's descriptor vector, one label, binary IID screen. What sets hiva_agnostic apart?
(a) the AI's best guess: the copies are 0.5% of the rows and only 3 cross the challenge's training/validation cut, so
the effect is negligible (a size argument, which LEAK-19 does not name), recorded as an exception; (b) treat
hiva_agnostic like qsar_oral_toxicity and drop its 23 copies; (c) reopen qsar_oral_toxicity to keep its copies;
(d) change LEAK-19 (an amendment, for example a share below which copies may stay).

**Consistency check (AI, 2026-10-20):** qsar_tid_11 has 870 of 5,741 rows (15%) in 387 repeated FCFP vectors (116
exact copies; within a vector the pChEMBL SD is 0.25 against 1.54 overall), with no decision recorded, while
qsar_oral_toxicity, which cites it as its scope precedent, drops its repeated parents under LEAK-17 and LEAK-19.
LEAK-16 (Must) requires a decision. What sets qsar_tid_11 apart?
(a) the AI's best guess: it is a regression on ChEMBL activities where one compound's repeated vector comes from
different ChEMBL records (salt forms or FCFP collisions) with different measured values, so the rows are not copies
with one label and dropping would need averaging (SPLIT-26: a different dataset); the remedy would then be grouping on
the vector, which needs the ChEMBL ID the definition drops to rule out SPLIT-24's bar on feature hashes;
(b) treat qsar_tid_11 like qsar_oral_toxicity (one row per vector, LEAK-19 / LEAK-20 adapted to regression);
(c) reopen qsar_oral_toxicity to keep its copies; (d) change the rule (an amendment saying how repeated vectors with
differing regression targets are handled).

</details>

<details><summary>Advocate</summary>

Position: ship after text changes. Every Must at P1-P5 holds on the measurements. The problems the evidence agents
found are wording, one fit label and one optional variant. None needs a change to the data or the split.

**1. A real regulatory endpoint, and the label is the hazard category itself (P3; USE-1, USE-2, USE-5 Must hold)**

* Evidence: the CATMoS paper names the actor and the moment ("predicting acute oral toxicity without animal testing";
  a 48,137-chemical prediction set; claim audit row 2). The claim audit linked every UCI row to the project file:
  class agreement 8,992 / 8,992, and the label equals regulatory category 1 on all 8,992 rows. The practitioner
  measured a usable triage list: precision 0.76 in the top 5% against a base rate of 8.3%.
* Objection answered: "below 50" is wrong, since the project's definition is LD50 <= 50 (44 chemicals at exactly 50,
  all positive). I concede it. This is a wording error. The data already holds the target the actor acts on, so
  USE-5 is met. Remedy: write "50 mg/kg or less (the top hazard category)" in `predicted` and in the Target bullet.

**2. No leak: every input exists before any test (P4; LEAK-10, LEAK-27 to LEAK-31 hold)**

* Evidence: the only columns are 1,024 bits computed per molecule from the structure (column audit: no
  post-outcome column, no all-row statistic). Leak probe: the best single bit reaches 0.679 against 0.869 for all
  features, and dropping any one bit costs at most 0.001. The label-free distance AUC is 0.510 (EV-9: ordinary data).
* Objection answered: the authors chose the fingerprint variant by internal CV (LEAK-31 Should, very weak). The column
  audit rates it far below "strong" and says it needs no remedy.

**3. Copies of an entity are removed by the rules and their precedents (P4; LEAK-16, LEAK-17 Must; LEAK-19, LEAK-20 Should)**

* Evidence: 477 exact copies and 22 both-class rows are dropped, which leaves 0.0% exact copies across every fold.
  The same rules and precedents apply here as for wine_quality (Lennart, 2026-09-30) and jm1 (Lennart, 2026-10-01).
  The precedent agent found the decision consistent and no prompt on this dataset.
* Objections answered: (a) 11 parents survive in two rows each, as tautomer or SMILES variants. That is 0.15% of test
  rows, so the effect on the score is negligible. Remedy: change "never" to "almost never (11 parents, 0.15% of test
  rows)". (b) 12 of the 406 repeated vectors are hash collisions of different chemicals. Remedy: one clause in the
  Duplicates bullet. (c) The "406 repeated parents by InChIKey" figure is wrong: it is 405 or 406 depending on the key.
  Remedy: correct the number. All three are text fixes at the lowest rung of the remedy ladder.

**4. IID is the split the rules prescribe here; a scaffold split is a variant, not a fix (P4; SPLIT-1, SPLIT-29, SPLIT-30 Must; SPLIT-24 Must; SPLIT-31 Should)**

* Evidence: after deduplication each parent appears once. No entity recurs, so SPLIT-29 does not trigger. SPLIT-24
  bars a similarity cluster as a group key. Both source protocols are random, and the project's split is
  "without supervised sampling of the chemicals based on structures" (claim audit row 32). The project's blind
  validation scored like its random test (N3 NER 85% against 86%; split audit). Holding out clusters costs RF 0.034 to
  0.044 AUC and leaves the model ranking unchanged (split audit; claim audit). That is the SPLIT-31 case
  (amazon_employee_access, bank_marketing), and SPLIT-4 says the size of the gap never decides.
* Objection answered: the claim that "the file holds no structure, so a scaffold split cannot be built" is refuted.
  The linkage recovers structures for about 96-99% of rows (EV-1). I concede the sentence. The linkage only shows
  that a scaffold variant could be built. It does not show that IID is wrong: SPLIT-31 makes the variant a candidate,
  not a fix. A split built on our own inferred merge would also be "a fix of our own invention", which the tensions
  table puts below the source's version (P5 over P6, eryhemato). Remedy: rewrite the bullet so that IID rests on the
  use case and the source protocols, and file the scaffold variant as a SPLIT-31 candidate.

**5. The fit label: a text call, not a reason to hold the dataset (P3; USE-8 Must, USE-9 Should narrows USE-8)**

* Evidence for direct: the project's real external evaluation set has the same analog profile as our IID test rows
  (median nearest-neighbour Tanimoto 0.545 against 0.553; 21.7% against 19.7% at >= 0.7; claim audit row 8). The
  practitioner (the P3 agent) argues for direct under USE-9: the use case is screening within the reference set,
  which is how the programme evaluates its models.
* Concession: the untested chemicals of the prediction set are further away (9.3% at >= 0.7, median 0.474). If
  `use_case` stays "screens chemicals without animal test data", "direct" overstates the fit. Mildest remedy, both
  text only: (a) keep `direct` and narrow `use_case` to the project's evaluation design (USE-9), or (b) set
  `approximate` and put the two numbers (9.3% against 19.7%) in `fit_reason`. Either keeps the dataset and the split.
  USE-8 asks for an honest label, not a perfect match. This is the curator's weighing call.

**6. Worth benchmarking, and in scope (P6; TP-1 to TP-10; P2; SEL-12 Weigh, precedent qsar_tid_11)**

* Evidence: task probes raise no flag. RF reaches 0.882 against a dummy log loss of 0.287, the spread between RF and
  linear is +0.167 (paired SE 0.014), and every test fold has at least 236 positives. RF (0.883) matches a
  nearest-neighbour model of the paper's N3 kind (0.877), so tabular models are competitive. The fingerprint scope
  follows qsar_tid_11 (shipped in v0.1) and hiva_agnostic. The blind reviewer says "Include".
* Objection answered: the critic may ask for a graph-model test on the recovered structures. The claim audit left that
  test untested, and it is a Weigh factor. SEL-12 is satisfied by the per-dataset evidence above.

**7. Faithful and reproducible (P5; PROV-8, PROV-13 to PROV-15)**

* Evidence: the sha256 reproduces. The counts match Table 1 (741 / 8,251; blocks 556 / 185). The independent linkage
  confirms the block boundary at 6,744. The licence is CC BY 4.0. No damage was found.
* Remaining items are procedure fixes: the Dragon 7 citation is in Sec. 2.7, the fingerprint variant goes into the
  Features bullet, and the record's "no known risk" / "issues closed" become "open: fit label, scaffold variant".

Judgment record: Verdict: ship after text changes. Validity: SEL-1, SEL-3 hold; USE-1 and USE-5 hold (target wording
fixed); USE-8 fit label is the curator's call (direct with a narrowed use case, or approximate); LEAK-10, LEAK-16,
LEAK-17, LEAK-19, LEAK-20 hold (wording: "almost never"); SPLIT-1, SPLIT-29, SPLIT-24 hold; SPLIT-31 scaffold variant
is a candidate; PROV holds. Value: TP clean. Quality: CLEAN holds; dtype convention across siblings is a separate
question.

**Rebuttal of the critic**

The critic and I agree on the verdict: ship after text changes, with no exclusion, no re-split and no data change.
What is left is one weighing call and how to word the reopened issue.

1. *Fit label: conceded, set `approximate`.* I offered two options: narrow the use case (USE-9), or set approximate.
   The critic's argument decides between them. The use case as written, screening untested chemicals, is the real one:
   CATMoS was built for the 48,137-chemical prediction set. Narrowing it to "chemicals like the reference set" would
   be the case USE-9 itself warns against, a use case rephrased only to excuse a gap. The measurement outranks the
   practitioner's reading (EV-2). The prediction set has 9.3% of chemicals with a close analog (>= 0.7) against 19.7%
   for our test rows, and a scaffold split costs 0.044 AUC. What follows: set `fit = "approximate"`; put both numbers
   in `fit_reason`; keep IID (SPLIT-31; SPLIT-29 is not triggered; SPLIT-24 bars clusters); list the scaffold variant
   as a candidate. USE-8 asks for an honest label, and approximate still ships (kick,
   account_debt_south_africa).
2. *The false reason for IID-only: conceded, with one limit.* The sentence is false, and the review issue must be
   reopened with the linkage facts (EV-1). I dispute only the implication that the closure rested on that sentence. It
   also rested on three rules that still hold: SPLIT-29 (no entity recurs after deduplication), SPLIT-24 (clusters are
   barred as a group key), SPLIT-5 (both source protocols were structure-blind). The critic's own caveat is that the
   linkage is a reconstruction, not a key. So the reopened issue changes the reason written down, not the outcome.
3. *The written target: conceded.* Write "50 mg/kg or less (the top acute oral hazard category)" in `predicted` and in
   the Target bullet, with the critic's note that 25% of the labels come from category data. Text only (USE-5).
4. *"Never": conceded, with a choice of remedy.* Use the wording fix: "almost never: 11 parents keep two rows, 0.15%
   of test rows". I dispute the alternative of dropping rows through the linkage. It would put a reconstruction of
   about 96-99% accuracy into `_clean` for a 0.15% effect, which the critic's own caveat argues against. The remedy
   ladder takes the mildest fix that resolves the problem.
5. *The duplicate story: conceded.* Correct one clause each in the Duplicates bullet and in `_decisions`: 12 of the
   406 vectors are hash collisions of different chemicals; by InChIKey the source shows 405 repeated keys over 891
   rows, not 406. The decision itself stands (LEAK-19, LEAK-20), and both sides agree it does.
6. *Record and citation: conceded.* Fix the Dragon 7 citation (Sec. 2.7) and add the fingerprint variant to the
   Features bullet. After the curator decides, replace "no known risk" / "issues closed" in the record with the open
   items. Priority 4 can stay: the open items are a fit label and a variant, not a validity failure.

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** I do not ask for exclusion: every Must problem below can be fixed in the
definition text. All of them are P3/P4 statements in `dataset.py` that the phase A measurements refute, plus one
review issue that was closed on a false premise.

**1. `fit = direct` overstates how well the split mirrors the stated use case (P3, USE-8 Must)**

* Problem: `use_case` says a regulator or maker screens untested chemicals. The test rows are random members of the
  tested reference set, and those sit much closer to training than the chemicals the actor actually screens.
* Effect on the real task: the shipped AUC is the in-domain number. For the stated actor the real number is lower, and
  the skill follows exactly this axis: RF AUC is 0.682 below Tanimoto 0.5 to the nearest training chemical and 0.956
  at 0.85 or more.
* Evidence (claim audit row 8): untested parents in the project's own prediction set (`predset_qsarr_2d.txt`, 48,137
  rows, 3,000 sampled) have a median nearest-training similarity of 0.474 and 9.3% of rows at >= 0.7. Shipped IID test
  rows: 0.553 and 19.7%. A scaffold-grouped 3-fold CV gives RF 0.843 +- 0.015, against 0.887 +- 0.008 for the random
  split. The split audit's cluster splits agree: 0.842 to 0.848, against 0.882. This also refutes the earlier review
  issue's premise that screening lists "hold many analogs of tested chemicals".
* Rule: USE-8 (Must) defines "direct" as rows, features *and split* mirroring the use case. Here a known gap exists,
  and approximate is for "a stand-in with a known gap, named as such". SPLIT-31 (Should) keeps the IID split. I do not
  ask for a re-split: no entity recurs after deduplication (SPLIT-29 is not triggered), and SPLIT-24 bars clusters as
  a key.
* Remedy: keep the split. Set `fit = "approximate"` and put the two numbers in `fit_reason` (prediction-set
  similarity, scaffold-split cost). The alternative is USE-9: narrow `use_case` to screening chemicals like the
  reference set, the project's own evaluation design. USE-9 itself weighs that against "a use case rephrased only to
  excuse a gap". The practitioner keeps "direct", but that reading rested on the gap being stated and on "no
  congeneric series" (probe gap +0.006). The 0.044 scaffold cost shows that chemotype-level signal does carry over.

**2. The stated reason for IID-only is factually false, and the earlier review issue was closed on it (P4, EV-1 / EV-2 Must, SPLIT-5)**

* Problem: the curation_comments say "The file holds no structure or identifier, so a scaffold split cannot be
  built". The earlier review issue's alternative says linking "would need Dragon 7's ECFP".
* Effect: the curator decides the split question on an impossibility that does not hold. The same applies to the
  grouped variant, the stereo check and the exact LD50 (a regression target).
* Evidence (claim audit EV-1): both UCI blocks are in CASRN order and interleave into the order of
  `trainingset_171130.txt`. The alignment gives 100% class agreement on 8,992 rows and reproduces the 556 / 185 block
  positives exactly. Structural flags predicted from the linked rows' bits score ROC AUC 0.998, so roughly 96-99% of
  the links are right. The counter-ion vector links to the three salts named in the comments.
* Rule: EV-1 / EV-2 (Must): a measurement outranks the page and the earlier claim. SPLIT-5 (Must): the split rests
  on the task design, not on what the file cannot do.
* Remedy: rewrite the bullet. Say that IID rests on the use case and the source design, and that the structures can be
  recovered by order linkage. Reopen the review issue with these facts. List a scaffold-grouped variant as a SPLIT-31
  candidate. Caveat: the linkage is a reconstruction, not a key, so I do not ask to group on it here.

**3. The written target is not the label (P3, USE-5 Must)**

* Problem: `predicted` and the Target bullet say LD50 "below 50 mg/kg". The project defines VT as LD50 <= 50 mg/kg.
  All 44 chemicals at exactly 50 are positive. The label equals regulatory category 1 on all 8,992 rows, and 25% of
  rows have no point LD50, so their label comes from category data.
* Effect: small on the score, but the target the actor acts on is the hazard category, not a thresholded number.
* Rule: USE-5 (Must): the written target has to be what the actor acts on. EV-2.
* Remedy: text only. Write "50 mg/kg or less (the top acute oral hazard category)" in `predicted` and the Target
  bullet, and note that a quarter of the labels come from category data.

**4. "A test chemical never has its parent structure in training" is false as written (P4, LEAK-17 Must)**

* Evidence (claim audit row 6): 11 parents survive in two kept rows each, as tautomer or SMILES variants with
  different vectors. That is 0.15% of test rows per fold, at most 0.21%.
* Effect: negligible on the score. The absolute claim is wrong.
* Remedy: soften the wording in `task_summary.split` ("almost never: 11 parents keep two rows"), or drop one row of
  each pair through the linkage.

**5. The duplicate story is partly wrong (LEAK-16 Must on documenting the decision; EV-2)**

* Evidence: 12 of the 406 repeated vectors are hash collisions of genuinely different chemicals, not salt forms. The
  claim "the project's training file shows the same 406 repeated parents by InChIKey" is refuted: there are 405 keys
  over 891 rows by full key, the groupings overlap on 394, and the both-class groups are 11 keys over 29 rows, not 22
  rows.
* Effect: about a dozen distinct chemicals are dropped under the label "copies". This does not change the decision
  (LEAK-19 / LEAK-20 still apply to identical feature vectors).
* Remedy: one corrected clause in the Duplicates bullet and in `_decisions`.

**6. Record and citation (procedure, writing.md; quality, not a reason to hold the task)**

* The record's 2026-10-20 assessment ("no known risk", "issues closed", priority 4) is refuted by points 1-3. Update it
  after the curator decides.
* The comments cite "Dragon 7 (paper, Sec. 2.2)", but it is Sec. 2.7. The fingerprint variant (ECFP_1024_02 or _02R,
  2 bits per fragment) is not stated in the bullet, although the earlier review file says it is.

**Not argued**

The column validity (all bits are known at prediction, no leak), the deduplication decision itself (LEAK-19 / LEAK-20,
wine_quality / jm1), fingerprint scope (SEL-12, qsar_tid_11) and the signal (P6) all held against every probe. I raise
nothing there.

**Rebuttal of the advocate**

We now agree on the verdict: ship after text changes, with no change to the data or the split. One point stays in
dispute, which remedy to use for the fit label (point 5).

| Advocate's point | Answer |
|---|---|
| 1. A real endpoint; the label is the hazard category; "below 50" is a wording error | Concede. USE-5 holds once the text says "50 mg/kg or less (the top hazard category)". I keep my request to note that 25% of the labels come from category data, not from a point LD50. |
| 2. No leak | Concede. I raised nothing there. |
| 3. Copies are dropped by rule; "never", collisions and the 406 figure are text fixes | Concede. Same remedies as my points 4 and 5. One correction for the text: by full key the InChIKey figure is 405 keys over 891 rows, and the both-class groups are 11 keys over 29 rows. It is not only "405 or 406". |
| 4. IID stays; the scaffold split is a SPLIT-31 variant; the bullet is rewritten | Concede. I never asked for a re-split, so the eryhemato argument answers a request nobody made. One part stays open: the review issue has to be reopened, because it was closed on the false premise that linking is impossible and that screening lists "hold many analogs". |
| 5. Fit label: (a) direct with a narrowed use case, or (b) approximate | **Dispute (a); (b) is the remedy.** The advocate's evidence for (a) is that the external evaluation set matches the IID test (0.545 against 0.553). That set is the programme's model test, not an actor's decision. Screening within an evaluation design is not "another well-defined use case that practitioners have" (USE-9). The actor named in `use_case` and in the advocate's own point 1, quoted from the CATMoS paper, screens the 48,137-chemical prediction set. Those chemicals sit further away: 9.3% against 19.7% at >= 0.7. Narrowing the use case to the evaluation design would be "a use case rephrased only to excuse a gap", the factor USE-9 weighs against. USE-8 (Must) wins: approximate, with the two numbers and the 0.044 scaffold cost in `fit_reason`. |
| 6. Worth benchmarking, in scope | Concede. I asked for no graph-model test. |
| 7. Faithful; procedure fixes | Concede. The same fixes as my point 6. |

</details>
