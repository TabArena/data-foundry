# desi_dr1_star_galaxy_quasar

**Outcome:** added as `desi_dr1_star_galaxy_quasar_1m`. The task: the first data release of DESI (the Dark Energy Spectroscopic Instrument), one object of its main survey with a settled spectroscopic class, classified as galaxy, star or quasar from the imaging catalogue it was targeted from (Legacy Surveys DR9 photometry and its Gaia DR2 match), before it has a spectrum; 16,930,061 objects, of which 1.5M are sampled with the class shares kept, 45 features, 3 random folds of 1M training and 500k test objects, scored by log loss (a fallback: the release has no task or metric). The AI recommends shipping it: the panel's changes are made, and one call is left, issue 1 (the label; A implemented and recommended).
Verdict: ship after changes (made).
Validity: SEL-13 not triggered (the profile type, shape and Sersic index are 5 of 45 inputs, worth 0.0022 log loss; the rest are measurements through an imaging device, SEL-15); USE-5 holds (the release's own class; DESI's quasar catalogue disagrees with it on 0.73% of the shipped rows, both ways: issue 1); USE-7 holds (objects without Legacy Surveys photometry dropped, 81.5% of them stars); USE-8 approximate, fit_reason names the target selection, the ZWARN cohort and the label gap; LEAK-10 triggered, fixed (the spectral fit and the targeting columns dropped; astrometry without a Gaia DR2 match blanked); LEAK-16 holds (0 exact copies); LEAK-22 holds (the release's cohort); SPLIT-1 and SPLIT-4 hold (IID; sky-region holdouts score 0.0861 to 0.0878 against 0.0864); PROV-4 and PROV-7 hold under "Same task, another source" (both enter, reworded).
Value: TP-3, the families spread (task probes on the final definition: LightGBM 0.089, random forest 0.103, linear 0.164, dummy 0.719); TP-4 holds (0.399 against 0.726 within the quasar targets, shipped splits); MET-8 fallback log_loss.
Quality: CLEAN-10 masks (fibre fluxes of unmeasured bands, SERSIC of point sources); CLEAN-11 extreme negative infrared fluxes kept as published, with a note.
Weighed (priority 3): gap + (physics & astronomy and multiclass are thin), use case 0 (ours; the fit is approximate), source + (the DESI collaboration's release, data model and paper), shape + (16.9M objects, mixed types), risk - (the label at the galaxy/quasar boundary is open, issue 1).
For the curator: issue 1 (which label, a weighing: A implemented and recommended).
Changes made, no decision needed:

- (a) the fit reason names the release's quality filter: it drops 20.6% of the emission-line galaxy targets and 13.9% of the quasar targets, against about 2% of the others;
- (b) the fit reason and the notes name the label's disagreement with DESI's quasar catalogue, both ways;
- (c) the fibre fluxes of a band that was not measured are set missing;
- (d) the Sersic index of point sources is set missing (c and d change no score);
- (e) the Gaia parallax and proper motions are blanked for 17,006 objects without a Gaia DR2 match (1,529 shipped rows), since which objects carry them follows the targeting route;
- (f) every LightGBM number in the notes is re-run with early stopping on the final definition (the photometry scores 0.0864; the targeting columns add 0.0007, not 0.013; holding out sky regions changes nothing);
- (g) the image-model columns are kept with the fact that sets them apart from magic_gamma_telescope (5 of 45 inputs, worth 0.0022; magic is all descriptors, and simulated);
- (h) sdss_17 is called the same task from another survey, not better data, with the reason in both records;
- (i) the copies are given as 5,211 pairs within 1 arcsec, not 1,872 objects in a grid cell;
- (j) every masked band is listed in the notes;
- (k) the extreme negative infrared fluxes are kept as published, with a note;
- (l) the notes say that an unmeasured z or infrared band follows the targeting route, and that it stays;
- (m) the notes size the selection gap (log loss 0.48 on the faintest third against 0.18 under random folds);
- (n) the notes give the class shares at each filter step and the README a table of the quality filter's drop by targeting class; the builder's report is corrected the same way, and its checklist names the measured label disagreement.

**Main points:** Confirm Redrock's class with the note that names DESI's quasar catalogue's disagreement in both directions, or take the catalogue's class one way or both ways, or add a quasar-targets version later (issue 1, A implemented).

**Record judgment:** valid. DESI's DR1 redshift catalogue (Iron, CC BY 4.0), whose useful spectra of the main survey reproduce the release's counts exactly (18,659,804 objects); the build met each risk the screening named (the target bits and the spectral fit dropped, `Selection Bias` as for sdss_17, a sub-sample of the 16.9M objects). One reading of the screening is corrected: this is the same task from another survey as sdss_17, not better data for it, since the bands, the other inputs and the targeting rules differ, so both enter.

**Issues for Lennart:**

1. **Which label: the pipeline's class (Redrock), or DESI's quasar catalogue?**

   * **Problem:**
     - The label is the class DESI's pipeline (Redrock) fits to each spectrum, the class the release counts, but DESI's own DR1 quasar catalogue, which adds two quasar classifiers on the quasar targets, disagrees with it both ways: it calls 53,190 kept galaxies and stars quasars (99.6% of them quasar targets, the objects DESI's targeting picked as quasar candidates) and leaves out 68,521 of Redrock's quasars (98.7% of them outside the quasar targets)[^use5].
     - The definition keeps Redrock's class and names both disagreements in the fit reason and the notes (implemented)[^use8]; the alternatives take the catalogue's class only where it adds quasars, take it both ways, or add a later quasar-targets version labelled by the catalogue.
     - Which label to ship is a call on what the actor acts on at the galaxy/quasar boundary, because DESI publishes no quasar class that does not depend on which programme targeted the object[^tp6].
   * **Background:**
     - Redrock fits templates of galaxies, quasars and stars to each spectrum; the catalogue adds a fit of the MgII line and a neural network (QuasarNET), the "afterburners", and is about 99% pure in visual inspection, where Redrock alone finds about 86% of the confirmed quasars and Redrock with the afterburners about 94% (Alexander et al. 2023, https://arxiv.org/abs/2208.08517).
     - The catalogue's additions come from the afterburners, not from another spectrum: its own Redrock class is galaxy or star for 51,944 of the 53,190.
     - DESI's all-target AGN/galaxy catalogue (agngal v1.0, "galaxies and quasars from all targets") flags MgII and QuasarNET quasars only on quasar targets, and 65,810 of Redrock's quasars outside the quasar targets carry no quasar flag at all, so the catalogue's quasar class follows the targeting class, the column the definition drops as a leak[^leak10].
     - An object missing from the catalogue is "not in the quasar sample", not "a galaxy": giving the left-outs the galaxy class (option C) is our inference.
     - Catalogue: https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/QSO/iron/ (`QSO_cat_iron_cumulative_v0.fits`, 816 MB, the same CC BY 4.0 release), joined on the object's main-survey row.
   * **Effect on the task:**
     - If the catalogue is right, a model that calls these objects quasars, as DESI's quasar science would, is scored as wrong, so the benchmark rewards reproducing Redrock's misses at the galaxy/quasar boundary, which is where models differ.
     - The catalogue's additions are 4,757 shipped rows (0.32%) and carry 6.6% and 7.7% of the log loss of an untuned and a stronger LightGBM (3 shipped folds); the models already call 76-83% of them quasars.
     - The left-outs are 6,156 shipped rows (0.41%) and carry 14.2% and 16.6% of the log loss of the same two models; they call 84-86% of them galaxies (mean probability of a quasar 0.18-0.20).
     - The quasar targets are 11% of the rows and carry 51% of the loss, so the disagreement sits where models differ.
   * **Experiments:**
     - The task gamer's out-of-fold predictions on the shipped splits, an untuned LightGBM and a stronger one, both trained on Redrock's class, scored against three labels: Redrock's 0.08713 and 0.08444 (gap 0.0027); the catalogue's additions only 0.08279 and 0.07959 (gap 0.0032); the catalogue both ways 0.07166 and 0.06707 (gap 0.0046).
     - A shift both models share does not reorder them: what matters is the gap between the two models, and if the catalogue's class is the truth, Redrock's label hides 16% of it (B's label) or 41% (C's label); the ranking of the two models flips under no label, and the noise between them is 0.0001-0.0003.
     - On the rows the catalogue adds, the stronger model loses more than the baseline (mean loss 2.05 against 1.81).
     - Both models learned Redrock's class, so these numbers are bounds; three or more model families trained on each label were not run.
   * **Consistency:**
     - A keeps the pipeline's class as sdss_17 does[^sdss]; naming the gap follows diabetes_3, differentiated_thyroid_cancer_recurrence and sarcoma, which name the gaps of their labels or cohorts[^use8].
     - A label fails only when it is shown to be another quantity (chicago_traffic_crashes)[^use5]; here it is the same quantity, the spectroscopic class, under two classifiers.
     - Under B or C, like cases alike: sdss_17 gets an issue to measure its class against SDSS's own quasar catalogue (DR16Q) before its label is decided; its verdict stays until then.
   * **Panel:**
     - For a repair (the critic; the advocate after the rebuttal; both settled on B): repair from the source ranks above a note[^ladder], the catalogue is the quasar class DESI's quasar science uses, from the same release, and B makes no row's label worse.
     - For the note (the advocate's opening, the precedent checker, the mediator): Redrock's class is the one class the release fits the same way for every target, while the catalogue's depends on the targeting programme, which a new catalogue object does not have; B joins two source rules by a rule of ours and keeps the left-outs, which carry twice the loss of the additions, as quasars.
     - After the rebuttals the mediator checked two things: DESI's all-target AGN/galaxy catalogue flags afterburner quasars only on quasar targets, so the catalogue's class follows the targeting programme, and B keeps the 68,521 left-outs as quasars; these two facts moved the recommendation from B to A, neither debater has answered them, and a second rebuttal round on this point is still possible.
   * **Unknown:** visual-inspection truth for both disputed sets would settle it (DESI's Survey Validation visual-inspection catalogues; how far they overlap the main survey is unknown).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Redrock's class, with the note (implemented) | the label as the release counts it; the fit reason and the notes name both directions of the disagreement | one class fit the same way for every target; follows sdss_17; no rebuild | models learn Redrock's missed quasars as galaxies; the label hides 16-41% of the gap between two models |
     | B | The catalogue's additions only | quasar where the object's main-survey row is in the catalogue, Redrock's class otherwise, within the shipped cohort; 4,757 shipped rows change | the source's own quasar class where it adds quasars; no row's label gets worse; both debaters' final position | takes the catalogue one way only, so its 68,521 left-outs stay quasars; the additions fall almost only on quasar targets; sdss_17 gets a matching issue |
     | C | The catalogue both ways | quasar if and only if the object is in the catalogue, the left-outs become galaxies; 10,913 shipped rows change | one rule for the quasar class; the largest gap between the two models (0.0046) | the left-outs' galaxy class is our inference; the catalogue's quasar class follows the targeting programme; sdss_17 gets a matching issue |
     | D | A quasar-targets version later, next to A | a second dataset of the 1.9M quasar targets, labelled by the catalogue, as a later /add-dataset run | inside the quasar targets the catalogue is one rule (Redrock, MgII or QuasarNET) and covers 99.9% of Redrock's quasars; the decision DESI's own quasar selection makes | a second dataset to build and review; a narrower use case (choosing among quasar candidates) |

   * **Recommendation:** A, against the debaters' final position (both ended on B). After the rebuttals the mediator found two facts: DESI publishes no quasar class that does not follow the targeting programme, and B keeps the 68,521 left-outs as quasars, which carry twice the loss of the additions. So a relabel would build our own rule into the label, while Redrock's class is fit the same way for every object. D can follow for the quasar-target use case, where the catalogue is one rule. **Decision:** A, B, C or D (D can be added to A)?

   **Notes for the AI:**
   - A: nothing to change.
   - B: download `QSO_cat_iron_cumulative_v0.fits` from https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/QSO/iron/ into the dataset's raw folder (add it and its checksum to `download_description`); keep `TARGETID` until the join; in `_clean` after step 1, set `SPECTYPE` to `QSO` where the object's `TARGETID` has a catalogue row with `SURVEY` main; re-admit no ZWARN-flagged rows (53,375 dropped quasar targets are in the catalogue). Rewrite the label bullet of `curation_comments`, `predicted` and `fit_reason` (the catalogue covers the quasar targets; its 68,521 left-outs stay quasars). Re-run `dataset check`, all probes and a focused panel (claim auditor, task gamer, mediator, editor); a CHANGELOG entry; a `CC` line in the record; open an issue for sdss_17 to measure its class against DR16Q.
   - C: as B, and set `SPECTYPE` to `GALAXY` for Redrock quasars without a main-survey catalogue row; say in the notes that this class is ours.
   - D: a new record for the quasar-targets version (`version_of` this record or its own name), added later with /add-dataset; nothing changes here. Add a `CC` line naming it.

   [^use5]: **USE-5** (Must): predict what the actor would act on; "A target the source defined badly can often be redefined into the real one"; "A label checked and found to be another quantity than the one the actor acts on still fails" (Lennart, 2026-10-21, diabetes_3). chicago_traffic_crashes (CC 2026-11-05, Lennart): "USE-5 fails only when the label is shown to be another quantity".
   [^use8]: **USE-8** (Must): an approximate fit names its known gaps; "a label definition the sources do not settle" is one, and of a selection, "Either way `fit_reason` names the selection" (Lennart, 2026-10-27). diabetes_3 (an undocumented response, CC 2026-10-21), differentiated_thyroid_cancer_recurrence (2026-10-21) and sarcoma (the excluded uncertain cases) name theirs in `fit_reason`.
   [^tp6]: **TP-6** (Must): "A better version the source itself defines ... replaces the current one"; "A fix of our own invention ... is not a better version." principles.md, Tensions: "A better version against our own fix" (eryhemato) and "The real-world target against a convenient label" (corporate_credit_rating).
   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; targeting or pointing ids that encode the pre-selection are dropped (sdss_17's `plate` and `fiber_ID`, CC 2026-10-01, Lennart).
   [^ladder]: principles.md, "How to decide", 5: the remedy ladder: repair from the origin; fix the definition; keep with a documented note; exclude.
   [^sdss]: sdss_17 (CC 2026-10-01, Lennart): the v2 photometric task ships the SDSS pipeline's class, the redshift and the targeting ids dropped, `Selection Bias`, fit approximate.

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. The panel worked on the draft definition, before the masks, the blanked astrometry and the re-run numbers; the masks change no row and no label, so its counts hold for the final definition. In the reports, 0.100 → 0.087, the sky holdouts 0.100 / 0.099 / 0.088, `Z` alone 0.156, the spectral fit 0.020 and the quasar-target 0.400 are the draft notes' overfit numbers (400 trees, no early stopping). The claim auditor's early-stopped re-runs on the draft (photometry 0.0866, targeting columns +0.0006, profile columns 0.0016) are replaced in the final notes by 0.0864, +0.0007 and 0.0022. The column and split auditors' own runs use the draft's 400-tree setting unless marked regularised. The task gamer's 0.08713 and 0.08444 are on the shipped splits. The reports before the mediator's number the builder's draft issues (1 the framing, 2 the image-model columns, 3 the row filters, 4 the download), which the panel settled without an issue; the mediator's issue 1 is this file's. Claim audit: 32 claims (the builder's 27 and 5 implied ones); refuted and fixed: every LightGBM number of the notes (an overfit model: the targeting columns add 0.0007 in the final re-run, not 0.013, and the sky holdouts change nothing), the builder's use of a probe's removed rows, mostly rows the sub-sampling dropped, as evidence that the filters keep the class mix (now replaced by the class shares at each filter step), the copies count (5,211 pairs within 1 arcsec, not 1,872 objects in a grid cell); partly refuted: that the label is the real-world class (DESI's quasar catalogue disagrees, issue 1); untested: the journal details, the mirror copy's sameness, a model of the targeting class alone. Column audit: no leak; the fibre fluxes of unmeasured bands and the Sersic index of point sources (now missing), astrometry without a Gaia match (now blanked), extreme negative infrared fluxes (kept with a note). Split audit: right with notes; IID holds, and the notes' sky-holdout differences were seed noise (now re-run). Domain practitioner: fit approximate; name the label gap (done); would use the model to rank quasar candidates, not to label a whole catalogue. Blind review: include with changes; its concerns were the label's missing quasars (issue 1), the undocumented filters (in the notes, which it did not see), the targeted population (named in the fit reason) and thin headroom. Task gamer: nothing games the task (the largest gain, -0.0003, is calibration a deployed model has too). Precedent check: 9 of 12 calls follow precedent; three departed without a written fact (the unnamed label and filter gaps, the scope reason that would have kept magic_gamma_telescope, "better data for sdss_17"), and all three are now written. Debate: agreed on the leak drops, the split, the scope fact, the ZWARN filter with a fit_reason clause, the masks, the astrometry and the rewording; disputed the label. The debaters count 53,298 additions and 4,764 shipped relabels, from a join on any survey; the issue uses the mediator's join on the main-survey row: 53,190 and 4,757. The critic asks for a repair from DESI's quasar catalogue and the advocate joined it after the rebuttal (the catalogue's additions only), while the mediator's later facts (the catalogue follows the targeting class; it leaves out 68,521 of Redrock's quasars) went unanswered, so the call is yours (issue 1).

<details><summary>Mediator</summary>

MEDIATOR REPORT: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

Read: principles.md (df-large), use_case.md (USE-4 to USE-8), leak_checks.md (LEAK-10, LEAK-22, LEAK-39),
selection.md (SEL-13 to SEL-15), task_probes.md (TP-6), cleaning_features.md (CLEAN-10, CLEAN-11, CLEAN-21),
provenance.md (PROV-6, PROV-7), review_panel.md; dataset.py, the record, builder_report.md; the seven phase-A reports;
both briefs with their rebuttals; the critic's logs.
My checks (read-only, 4 threads; scripts and logs in the run's work files):
  qsocat_routes.py/.log      which route the DR1 QSO catalogue's upgrades take, and which targets it covers
  agngal_check.py/.log       DESI DR1's all-target AGN/Galaxy Classification VAC (agngal v1.0; its AGNCAT table,
                             17,995,599 rows, fetched by byte range into the run's work files, 4.4 GB, scratch)
  both_directions.py/.log    the other direction of the label disagreement, scored on the task gamer's predictions
  astrometry_rows.py/.log    which targets carry Gaia astrometry without a Gaia DR2 match

**1. RECOMMENDATION (judgment record)**
Verdict: ship after changes.
Validity: SEL-13 not triggered (5 of 45 inputs are image-model fits, worth 0.0016 log loss; the rest are measurements,
  SEL-15), note rewritten; USE-5 holds (the release's own class; DESI's quasar catalogue disagrees with it on 0.73% of
  shipped rows, in both directions), the gap named under USE-8; USE-7 holds; USE-8 approximate, fit_reason names the
  target selection, the ZWARN cohort and the label gap; LEAK-10 triggered, fixed (spectral fit and targeting columns
  dropped; astrometry outside the Gaia DR2 match blanked); LEAK-16 holds; LEAK-22 holds (the release's cohort);
  SPLIT-1, SPLIT-4 hold; PROV-6/PROV-7 hold under the row "Same task, another source" (reworded).
Value: TP-3, the families spread (LightGBM 0.089, forest 0.103, linear 0.164, dummy 0.719); TP-4 holds (0.399 against
  0.726 within quasar targets, shipped splits); MET-8 fallback log_loss.
Quality: CLEAN-10 masks (fibre fluxes of unmeasured bands, SERSIC of point sources); CLEAN-11 WISE outliers kept with
  a note.
Weighed: source +, size +, the label at the galaxy/quasar boundary - (issue 1).
For the curator: issue 1, the label. Recommended: keep the release's class with the note (a); a relabel from DESI's
  quasar catalogue is a target redefinition, the curator's call, and the one-way version both sides settled on (b)
  takes the catalogue's class in one direction only.

**2. CHANGES TO MAKE NOW (no decision needed)**
Text (definition, builder report, records):
 C1  fit_reason and curation_comments: name the label gap in both directions (USE-8 Must; USE-5's note clause). The class
     is Redrock's template class, the release's own. DESI's DR1 quasar catalogue, which adds the MgII and QuasarNET
     afterburners on quasar targets only, calls 53,190 kept objects quasars that Redrock calls galaxy or star (99.6% of
     them quasar targets). It also leaves out 68,521 Redrock quasars (98.7% of them outside quasar targets). On the
     shipped rows these are 0.32% and 0.41% of the rows and carry about 7% and 14-17% of a LightGBM's log loss.
     Whatever issue 1 decides, this clause stays, adapted to the label shipped.
 C2  fit_reason: the ZWARN clause (USE-8 Must; LEAK-22). Only spectra whose class Redrock settled ship. The filter drops
     20.6% of ELG targets and 13.9% of quasar targets, against about 2% of the other targets.
 C3  Builder report and draft issue 3: replace the probe-19 line with the class shares at each filter step (EV-1:
     probe 19's removed set is mostly the sub-sampling).
 C4  Re-run decisive_experiments.py with early stopping and replace every LightGBM number in curation_comments (the
     LEAK-10 bullets, the selection-bias bullet) and splits_comment (EV-1). Use the split auditor's wording for the
     split. Cite 0.399 against 0.726 within quasar targets from the shipped splits (TP-4). Correct builder draft issue
     1 option c: the targeting columns add 0.0006, not 0.013.
 C5  Replace the SEL-14 sentence with the fact that sets the case apart from magic_gamma_telescope (SEL-13, SEL-15).
     The table is mostly fluxes measured through an imaging device. The five profile columns carry 0.0016 (0.0866 ->
     0.0882). magic is descriptors only, and simulated (SEL-16). No amendment.
 C6  Uniqueness wording (tension row "Same task, another source"): call this "the same task from another survey", not
     "better data for sdss_17". Record the reason in this definition and in both records: SDSS has u and i; DESI has
     W1/W2, Gaia astrometry and morphology; the targeting rules differ.
 C7  Copies sentence: 0 exact copies; 5,211 pairs within 1 arcsec, separate Tractor sources (LEAK-16; replaces "1,872
     objects in a 1-arcsec cell").
 C8  Selection-bias bullet: an unmeasured z or WISE band follows the targeting route (1,409 of 1,461 objects without z
     are stars). It is known from the imaging, so it stays (USE-8 note; column auditor 3).
 C9  Missing-values bullet: list every band the code masks (g 252, r 120, z 1,461, W1 1,745, W2 1,744 objects), so the
     notes match the code (writing.md).
 C10 Builder checklist: replace "cannot verify the Redrock class error rate" with the measured disagreement (C1).
 C11 Optional (USE-8): one clause sizing the selection gap. Trained on the brighter two thirds, a model scores 0.48 on
     the faintest third, against 0.18 under random folds. This is confounded with the class and programme mix.
Data (step 3 of _clean; needs a rebuild on the curator's ask and a CHANGELOG entry):
 C12 CLEAN-10: set FIBERFLUX_b missing where FLUX_IVAR_b == 0 (21/11/138 shipped rows), and FIBERTOTFLUX_b where it is
     0 in those rows. Set SERSIC missing for PSF and DUP (488,603 shipped rows): 0 is no Sersic index, and MORPHTYPE keeps the
     information. Measured: no score change. Both sides accept the SERSIC mask; CLEAN-10's default settles it.
 C13 LEAK-10 (weak), CLEAN-21: blank PMRA, PMDEC and PARALLAX where REF_CAT is not Gaia DR2 (17,006 kept objects;
     1,529 shipped rows). Both sides agreed to blank them if the values come from the targeting step. My check shows
     that their presence follows targeting routes:
       - 89.8% are BGS targets, against 44.0% of the other non-Gaia rows;
       - 36.2% are secondary targets, against 7.3% (mostly secondary bits 43-48, in matched triples);
       - none are Milky Way targets;
       - 60.1% are stars, against 0.9%.
     Blanking also makes the column what the notes say it is, the DR9 catalogue's Gaia DR2 astrometry. At most a weak
     signal on 0.10% of rows is lost (P7), against a weak targeting leak (P4), so the higher rank decides. Tracing
     the exact file the values come from (desitarget's secondary-target inputs?) only changes the note's wording.
 C14 CLEAN-11: keep the extreme negative WISE fluxes as published (88 W1, 155 W2 below -1000 nanomaggies, mostly
     stars), with a sentence.
Builder draft issues 1 (framing), 2 (SEL-13/14), 3 (filters) and 4 (download) get no REVIEW issue. All panel members
agree on them, and the precedents agree. The quasar-target version of draft issue 1 becomes option d of issue 1.

**3. ISSUES FOR THE CURATOR (ranked)**
Issue 1 (P3; USE-5 Must, USE-8 Must, TP-6 Must; tension rows "The real-world target against a convenient label" and
"A better version against our own fix"). The label: Redrock's class, or DESI's quasar catalogue?

Problem: SPECTYPE is Redrock's template class, the class the release counts. DESI's DR1 quasar catalogue disagrees
  with it in two directions:
  - upgrades: 53,190 kept galaxies or stars are catalogue quasars (52,997 of them quasar targets);
  - left-outs: 68,521 kept Redrock quasars are not in the catalogue (860 quasar targets; 34,469 LRG, 21,925 BGS,
    11,075 ELG, 192 MWS targets).
  (Joined on the main-survey row. The claim auditor's any-survey join gives 53,298 upgrades, 53,066 among quasar
  targets, and 856 quasar-target left-outs.)
Effect, on the shipped rows, with the task gamer's out-of-fold predictions (models trained on Redrock labels, so the
  numbers are bounds):

    rows (share of the 1.5M)          loss share, baseline / strong   models' view
    upgrades 4,757 (0.32%)            6.6% / 7.7%                     argmax QSO 76-83%
    left-outs 6,156 (0.41%)           14.2% / 16.6%                   argmax GALAXY 84-86%, mean P(QSO) 0.18-0.20

    label scored                                baseline   strong    gap
    Redrock (shipped)                           0.08713    0.08444   0.0027
    upgrades only (option b)                    0.08279    0.07959   0.0032
    catalogue both ways (left-outs as GALAXY)   0.07166    0.06707   0.0046

  A shift both models share does not reorder them. What matters is the gap. Redrock's label hides 16% of the gap under
  option b and 41% under option c. The ranking of these two models does not flip under any label, and the noise
  between them is 0.0001-0.0003.
New facts (mine, after the rebuttals; neither side has answered them):
  M1 The upgrades come from the afterburners, not from a different coadd. The catalogue's own Redrock class is
     GALAXY or STAR for 51,944 of the 53,190 upgrades. Their bits are MgII and QuasarNET.
  M2 DESI publishes no afterburner class that is independent of the target class. I checked its all-target AGN/Galaxy
     VAC (agngal v1.0; "galaxies and quasars from all targets").
     - Among kept Redrock galaxies and stars, its MgII flags (31,587) and QuasarNET flags (37,315) fall only on
       quasar targets.
     - Outside quasar targets the only upgrade flag is QN_VAR_WISE, on 554 rows of a secondary quasar programme.
     - Its Redrock-QSO bit is set for 100% of the quasar targets' Redrock quasars and for 0% elsewhere.
     - 65,810 Redrock quasars outside quasar targets carry no quasar flag at all.
     So DESI's quasar class follows the targeting class, the column we drop under LEAK-10.
  M3 Option b keeps all 68,521 left-outs as QSO. It takes the catalogue's class where it adds quasars and ignores it
     where it leaves Redrock quasars out. The left-outs carry twice the loss of the upgrades.

Options:
  a  Keep Redrock's class, with C1's note naming both directions (recommended).
  b  Upgrades only (both sides' final position): QSO where the object's main-survey row is in the catalogue,
     Redrock's class otherwise. Applies only within the ZWARN 0 cohort.
  c  The catalogue both ways: QSO if and only if the object is in the catalogue. The left-outs become GALAXY, which is
     our inference: the catalogue says "not in the quasar sample", not "galaxy".
  d  A quasar-target version (1.9M objects) labelled by the catalogue, later, next to a. Inside quasar targets the
     catalogue's rule is one rule (Redrock, MgII or QuasarNET), and it covers 99.9% of the Redrock quasars. It is the
     decision DESI's random forest makes (builder option b).

For a repair (critic; the advocate after the rebuttal):
  - The remedy ladder puts repair above a note. USE-5: "a target the source defined badly can often be redefined into
    the real one".
  - The catalogue is the class DESI's quasar science and its target-selection validation use. About 99% of it is pure
    in visual inspection (Alexander et al. 2023).
  - It comes from the same CC BY 4.0 release: one 816 MB file and a TARGETID join.
  - Option b makes no row's label worse than today.
  - The error sits where models differ. Quasar targets are 11% of the rows and carry 51% of the loss. Upgraded rows
    cost the better model more (mean loss 2.05 against 1.81).
For the note (the advocate's opening, the precedent checker, M2 and M3):
  - USE-5 holds without a repair: the label is the same quantity, the spectroscopic class (chicago_traffic_crashes,
    2026-11-05; diabetes_3). The note meets USE-8.
  - Redrock's class is the one class the release publishes for every target, fit the same way for each.
  - DESI's quasar class depends on which programme targeted the object (M2). A new catalogue object has no programme.
  - Option b is a union of two source rules that we chose. Under TP-6 that is "a fix of our own invention", not a
    better version. Option c's galaxy class for 68,521 objects is ours too.
  - sdss_17 ships its pipeline's class.
Is the repair a change that needs no decision? No. It redefines the target, and no Must requires it.
  - USE-5 holds, and C1 meets USE-8.
  - TP-6 makes the source's better version replace ours only when the source defines one. For all targets it defines
    none (M2).
  - So which label to ship is a framing call (Weigh), for the curator.
Decision needed: a, b, c, or d (d can be added to a).
What would settle it:
  - The curator's reading of which class the actor acts on at the galaxy/quasar boundary: a quasar for DESI's quasar
    sample, which depends on the targeting class, or Redrock's template class.
  - Visual-inspection truth for both sets of disputed rows (DESI's SV visual-inspection catalogues; how much they
    overlap with the main survey is unknown).
  - Training three or more model families on each label, to see whether their rankings change, not only one pair's
    gap.
  M2 and M3 are new facts, so review_panel.md allows a second rebuttal round on this one point if the main session
  wants the sides to answer them.
Consistency: option a follows sdss_17. Naming the gap departs from sdss_17's silence. The fact that sets this case
  apart: the disagreement is measured here against the source's own catalogue, and it was never raised for sdss_17.
  Under b or c, treat like cases alike: give sdss_17 an issue to measure its class against SDSS's own quasar catalogue
  (DR16Q) before deciding. Its verdict stays until then. The row "Same task, another source" (PROV-4, PROV-7) is not
  affected: both enter either way, and a relabel would only add "other labels".

No other point is still disputed after the rebuttals. The critic's reading of the loss tail ("part of it is label
error") against the advocate's ("calibration") is settled by the measurement above: the two disagreement sets carry
21-24% of the loss. It feeds issue 1 and is not a separate decision.

**4. AGREED FACTS**
Source and rows
 1. Source: zall-pix-iron.fits (Iron, zcatalog v1), 28,425,963 rows, CC BY 4.0. The release's useful spectra reproduce
    the DR1 counts exactly: 18,659,804 = 13,049,402 galaxies + 1,553,713 quasars + 4,056,689 stars.
 2. Kept: 16,930,061 objects (75.4/15.6/9.0%). Shipped: 1.5M drawn within each class, 3 folds of 1M/500k. Test folds
    hold 44,800 quasars each.
 3. Filters:
    - The ZWARN filter drops 20.6% of ELG targets, 13.9% of quasar targets and about 2% of the others. 53,375 of the
      307,534 dropped quasar targets are catalogue quasars.
    - The Gaia-only drop removes 1,212,422 objects, 98.3% of them stars (USE-7).
Leaks and copies
 4. The features are LS DR9 (released 2021-01-13) and Gaia DR2, both older than the first main-survey spectrum (May
    2021). The LEAK-10 drops are complete: all 136 columns were checked.
 5. 0 exact copies.
 6. The task gamer found nothing that games the task. Baseline 0.08713, strong model 0.08444, noise about 0.0001
    (0.0003 per split).
Numbers in the notes
 7. The notes' LightGBM numbers come from an overfit model. With early stopping:
    - photometry 0.0866; with the targeting columns 0.0860 (+0.0006);
    - sky holdouts 0.0866 / 0.0869 / 0.0877;
    - regularised, random folds 0.0848 against HEALPix nside-64 folds 0.0850. IID stays (SPLIT-4).
 8. TP-4: 0.399 against 0.726 within quasar targets.
 9. The five profile columns carry 0.0016. Without the fibre fluxes too, the score is 0.0981.
Label and Gaia astrometry
 10. The label is Redrock's SPECTYPE. The catalogue counts are under issue 1, with M1-M3.
 11. 17,006 kept objects (1,529 shipped rows) have astrometry without a Gaia DR2 match.

**5. TASK GAMER: EXPLOITS MAPPED (the definition has no "Potential leak, kept on purpose:" notes or accepted warnings)**
  1 prior matching, -0.0003 | MET (calibration; weights from another fold gain the same, so the stratified folds
    leak no test composition) | new | no issue
  2 sky kNN label features, +0.0000 to +0.0006 | LEAK-17, SPLIT-29 (near copies, hidden groups) | new, no gain |
    no issue
  3 sky density over train+test, within noise | LEAK-30 (transductive) | new, no gain | no issue
  4 sky density over training rows, -0.00015 | a legitimate feature (USE-6) | new | no issue
  5 row position, within noise | probe 10 (row order) | known (builder: the base class shuffles) | no issue
  6 format features, within noise | LEAK-13, LEAK-39 (probe 17) | known (builder: MORPHTYPE plus missingness) | no
    issue
  Not checked by the gamer: a lookup of full-precision RA/Dec in the public DESI catalogue. That is outside the
  benchmark's threat model, as for sdss_17's coordinates. The ZWARN filter is LEAK-22/USE-8, known and named by C2.
  The absent targeting bits are LEAK-10, known.

**6. CONSISTENCY WITH PRECEDENT (the precedent checker's report)**
Followed:
  - sdss_17: framing, targeting ids dropped, IID after a grouped test, fallback log_loss, Selection Bias, approximate.
  - diabetes_3, differentiated_thyroid_cancer_recurrence and sarcoma: the label and selection gaps are named once C1
    and C2 are in.
  - diabetes_130_us (LEAK-22): the release's cohort. framingham is apart: a ZWARN spectrum has no valid label to keep.
  - chicago_traffic_crashes: USE-5 holds for the same quantity.
Departures, with the fact that sets this case apart:
  - magic_gamma_telescope: the image-model columns are 5 of 45 inputs and worth 0.0016, and the rest are measurements
    (SEL-15). magic is descriptors only, and simulated (C5).
  - The row "Same task, another source": the features and the targeting differ, so both enter (C6).
  - sdss_17's label: see issue 1. If b or c is chosen, sdss_17 gets a parity issue.
No drift and no third exception (precedent checker). SEL-14's wording does not cover automated catalogue fits. The keep
rests on SEL-13's own proportion clause and SEL-15, so no amendment is needed now. One could be proposed if more survey
catalogues come.

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

Verdict: validity holds where it matters most. The kept columns are known before the spectrum (LS DR9 was
released 2021-01-13, and the main survey ran May 2021 to June 2022). The LEAK-10 drops are right. IID shows
no gap under a sky-region holdout. The metric can be computed on every fold. Three findings for the curator:
  F1 (P3, USE-5 Must, weigh): the target is Redrock's SPECTYPE. DESI's own quasar class, from the DR1 QSO
     catalogue that adds the QuasarNET and MgII afterburners, disagrees on 53,922 of the 1,900,008 kept quasar
     targets (2.8%). 52,534 of them are shipped as GALAXY, which is 10.9% of the "galaxy" share of quasar
     targets. That is the stratum where the classes mix. Survey Validation visual inspection: the standard
     pipeline finds about 86% of quasars, against about 94% with the afterburners (arXiv 2208.08517). Neither the
     notes nor fit_reason mention this, and the builder marked it "cannot verify".
  F2 (P4/P6, numbers refuted, decisions unchanged): every LightGBM number in the curation notes and
     splits_comment comes from an overfit model: 400 trees at learning rate 0.1, no early stopping. With early
     stopping on the same kind of sample, the photometry scores 0.0866, not 0.100. Adding the targeting columns
     gives 0.0860, not 0.087. So "0.100 -> 0.087" is an artefact. The sky-holdout numbers become 0.0866 / 0.0869
     / 0.0877: no gap, but also not the "0.088 better than random" the comment reports.
  F3 (P3, USE-7/USE-8, should): the ZWARN==0 "useful spectra" filter selects on the outcome's difficulty by
     targeting class. It removes 20.6% of emission-line-galaxy (ELG) targets and 13.9% of quasar targets, against
     about 2% of the others. 53,375 of the 307,534 dropped quasar targets are quasars in DESI's QSO catalogue.
     fit_reason names only the colour-cut selection.

Scripts t1-t6 with their logs are in the run's work files (the DR1 QSO catalogue was downloaded there, 816 MB, scratch only).

**TABLE: claim | source | test | result | evidence | rule**
C1  Source: zall-pix-iron.fits, Iron zcatalog v1, year 2025 | claims.md 1, dataset.py source_url/year | the DR1 page
    and the files in the warehouse | HOLDS | 25,431,495 main-survey rows read from the file; DR1 page footnote 1
    quoted below | PROV-8/9
C2  CC BY 4.0, citation and acknowledgement required | claims 2, license | read data.desi.lbl.gov/doc/acknowledgments
    | HOLDS | "licensed under the Creative Commons Attribution 4.0 International License" | PROV-10
C3  Citation AJ 171(5), 285 (2026) | claims 3, bibtex | not re-fetched (the ADS link is in the record) | UNTESTED
    (low stakes) | - | EV-4
C4/C5 22.4 GB, mirror is the deprecated copy, DESINAME only | claims 4-5 | file size in the warehouse | size HOLDS
    (22,371,272,640 B). "Same data" is not compared (the builder says so too) | - | PROV-13
C6  53 of 136 columns, 25,431,495 main rows | claims 6 | t1 | HOLDS | 25,431,495 rows | -
C7  useful spectra = 18,659,804 = 13,049,402 / 1,553,713 / 4,056,689 | claims 7, notes | t1 recount from the
    Parquet; the DR1 page footnote | HOLDS exactly | footnote: "ZCAT_PRIMARY==True, OBJTYPE=='TGT', and
    ZWARN==0 ... The Main Survey additionally excludes PROGRAM=='other'" | EV-2
C8  ZWARN!=0 share 10.1% gal / 4.0% QSO / 1.6% star | claims 8 | t1 | HOLDS (0.1009 / 0.0402 / 0.0161). By
    targeting class it is larger and uneven: ELG 20.6%, QSO 13.9%, LRG 2.2%, BGS 2.0%, MWS 1.6% (see F3) |
    USE-7/8
C9  1,729,743 without LS photometry: 1,212,422 G (98.3% stars, GPSF/GGAL), 517,321 empty (all ivar 0) | claims 9 |
    t1 | HOLDS | G: 0.9833 stars, GPSF 1,193,764 / GGAL 18,658; empty: MORPHTYPE '' in all rows, g/r/z ivar 0 in
    100% | USE-7
C10 16,930,061 kept: 75.4 / 15.6 / 9.0% | claims 10 | t1 | HOLDS | 12,765,505 / 2,647,605 / 1,516,951 | -
C11 TARGETID unique; no photometry copies; 1,872 objects share a 1-arcsec cell, separate sources | claims 11, notes
    | t1, t3 (KD-tree on the 16.9M kept objects), t3b | HOLDS in substance. The count is a grid-cell artefact: by
    radius there are 5,211 pairs (10,353 objects) within 1 arcsec. Their r fluxes differ (median relative
    difference 0.96; 14 pairs within 1%). 138 pairs lie within 0.05 arcsec: consecutive TARGETIDs, both PSF,
    different fluxes, same class in 100%. These are Tractor splits of one blended star. About 1 such pair is
    expected in the 1.5M sample. The shipped frame has 0 exact feature copies, and 0 copies without the
    position. | LEAK-16/17
C12 Z, ZERR, DELTACHI2 are post-spectrum and dropped | claims 12, notes | the logic (Redrock fits the class and z
    together); useful rows all have DELTACHI2 >= 9.0 (t1) | DROP HOLDS (LEAK-10: "a value fitted from the same
    measurement that gives the label"). The numbers (0.156 / 0.020 / 0.100) come from the overfit model, see F2 |
    LEAK-10
C13 Targeting columns dropped. "Added to the photometry 0.100 -> 0.087" | claims 13, notes | t5: early-stopped
    LightGBM on the same 600k design (seed 11, 3 stratified folds) | DROP HOLDS (LEAK-10: "targeting or pointing ids
    that encode pre-selection"). The NUMBER IS REFUTED: 0.0866 -> 0.0860 (+0.0006). The gain the notes report is
    the overfit baseline (0.100), not information. | LEAK-10, EV-1
C14 Tractor model columns and fibre fluxes kept (SEL-14 over SEL-13). DESI cuts on MORPHTYPE and fibre flux; Liu
    et al. 2025 read the morphology | claims 14, notes | (a) timing: LS DR9 released 2021-01-13, before the main
    survey's first spectrum (May 2021); (b) ablation t5; (c) Liu et al. 2025 abstract | HOLDS: not
    spectrum-informed. Ablation: all 0.0866; without MORPHTYPE/SHAPE/SERSIC 0.0882; also without fibre fluxes
    0.0981; fluxes + position + masks only 0.1056. The image-model columns carry about 0.011 log loss (12%), and
    the task stands without them, so the SEL-13/14 choice does not decide validity. Liu et al. 2025 (PASP 137,
    084501; arXiv 2505.17174) is a resolved/unresolved model trained on HST COSMOS labels and evaluated on DESI DR1.
    The use_case's "star-galaxy model" wording fits. | SEL-13, SEL-14, LEAK-10
C15 Gaia columns 0 iff no Gaia match; parallax/pm 0 for 14.7% of Gaia rows | claims 15 | t1 | HOLDS | G==0 in 100% of
    non-G2 rows and 0% of G2 rows; parallax==0 in 0.1467 of G2 rows, always together with PMRA==0 | CLEAN-10
C16 ivar 0 in 1,745 (W1) and 1,461 (z) objects | claims 16 | t1 | HOLDS (the notes leave out g 252, r 120, W2 1,744,
    which the code also masks) | CLEAN-10
C17 MASKBITS bits 10, 14, 15 never set | claims 17 | t1 | HOLDS | bit counts 10: 0, 14: 0, 15: 0 | CLEAN-13
C18 Codes decoded | claims 18 | the README's categorical table | HOLDS | -
C19 RELEASE 9010/9012 south, 9011 north; REF_EPOCH 2015.5 everywhere | claims 19 | t1 | HOLDS | RELEASE x PHOTSYS:
    N 9011 3,768,012; S 9010 13,066,856, 9012 95,193. REF_EPOCH 2015.5 in all 16,930,061 rows | CLEAN-5
C20 Fluxes in nanomaggies, negatives kept | claims 20 | the README's numeric table (FLUX_W1 min -726) | HOLDS | -
C21 Target SPECTYPE = Redrock class | claims 21 | t4: join with DESI DR1's QSO catalogue
    (survey/catalogs/dr1/QSO/iron/QSO_cat_iron_cumulative_v0.fits) | HOLDS literally. The IMPLIED claim that this
    is the real-world class is PARTLY REFUTED (F1). Kept quasar targets: Redrock GALAXY but catalogue quasar
    52,534; Redrock STAR but catalogue quasar 532; Redrock QSO but rejected by the catalogue 856. In all, 53,922
    of 1,900,008 (2.84%). Of the catalogue's 1,501,766 quasars among kept objects, 53,298 (3.5%) are shipped as
    GALAXY or STAR. | USE-5
C22 Use case cited (Chaussidon et al. 2023 RF quasar selection; Liu et al. 2025 evaluated on DESI DR1) | claims 22 |
    the Liu et al. abstract (arXiv 2505.17174, PASP 137, 084501 confirmed) | HOLDS. Chaussidon 2023 not re-read |
    USE-1
C23 Fit approximate, Selection Bias as in sdss_17 | claims 23, record decision_markers | sdss_17 record: Selection
    Bias; sdss_17 fit approximate | HOLDS. fit_reason leaves out two known gaps: F1 (label) and F3 (ZWARN filter).
    USE-8 says an unsettled label definition is a known gap that must be named | USE-8
C24 Within targeting classes: shares hold (t1 Decision table; 70.5/25.3/4.1 for QSO targets). Model numbers
    (QSO 0.400 vs 0.726; ELG 0.124 "worse than the shares") | claims 24 | t6 (tracer-recovery baseline) | shares
    HOLD. The model numbers come from the overfit model (F2): direction plausible, values not reproduced. ELG
    "worse than the shares" is likely the overfit itself | TP-4
C25 Metric fallback log_loss: no task or metric at the source | claims 25, metric reason | looked once more: DR1
    page, Liu et al. 2025 (binary resolved/unresolved, no three-class metric), Chaussidon 2023 (target density and
    efficiency for one class) | HOLDS (MET-1). Computable (MET-2): unit is the row; no scoring columns needed. Test
    folds hold 377,007 GALAXY / 78,192-78,193 STAR / 44,800-44,801 QSO. The class-prior dummy scores 0.7192 on each
    fold and uniform 1.0986, through the participant kit's score.py, the benchmark's metric code. Train/test
    overlap 0. Class shares of the sample equal the 16.9M frame (75.40 / 15.64 / 8.96) | MET-1, MET-2, MET-8
C26 IID: a sky-region holdout changes nothing (0.100 / 0.099 / 0.088) | claims 26, splits_comment | t2: early-stopped
    LightGBM, same 600k rows, random vs GroupKFold on HEALPix nside 4 (215 deg2) and nside 1 (12 regions of about
    3,400 deg2), with and without RA/Dec | CONCLUSION HOLDS, NUMBERS REFUTED: random 0.0866; nside 4 0.0869; nside 1
    0.0877 (per fold 0.079-0.098, from the regions' class mix); without position 0.0866 vs 0.0875. The comment's
    "0.088 with 215 deg2 held out" (better than random) is the overfit model. SPLIT-4: the position is a feature,
    and new objects of the footprint keep having it, so IID is right whatever the gap | SPLIT-1, SPLIT-4
C27 Better data for sdss_17, separate surveys | claims 27 | the record and the sdss_17 definition | HOLDS
    (different instrument and objects, PROV-6) | PROV-6
B1  Builder report: "removed rows' class shares within 0.022 of the kept ones" (probe 19) | builder_report.md
    raw probes | probe 19's "removed" set is 23.9M rows. Most of them are rows the sub-sampling dropped, so it
    cannot test the filters | NOT EVIDENCE for the filters. Measured directly (t1): the filters do change the class
    mix. Useful spectra are 21.7% stars, kept rows 15.6%, because the Gaia-only rows are 98.3% stars. The ZWARN
    filter is uneven by targeting class (C8) | LEAK probe 19
I1  Implied: every kept feature is known before the spectrum | dataset.py READ_COLUMNS minus the drops | timing of
    LS DR9 and Gaia DR2 (both before May 2021). Tractor in DR9 fixes the shapes of SGA-2020 large galaxies (REF_CAT
    L3, 92,858 objects, 99.0% GALAXY) and of Gaia sources. These come from earlier catalogues, not from the DESI
    spectrum | HOLDS | LEAK-10, LEAK-37
I2  Implied: no copy across the split | t3 | HOLDS (C11) | LEAK-16
I3  Implied: sub-sampling is random within class | t3 shares | HOLDS | -
I4  Implied: the task is more than recovering the targeting programme | t6 tracer-recovery baseline (photometry ->
    targeting class -> its class shares) | UNTESTED: the 6-class tracer model ran over 60 min on about one core and was stopped (t2, t6 logs). The
    builder's within-tracer test (QSO targets 0.400 vs 0.726 for their shares) supports the claim, though it comes
    from the overfit model | TP-4

**REFUTED AND UNTESTED, RANKED (principles.md: validity first, Must first)**
1. F1, the target is not quite the real-world class (P3, USE-5 Must). It fails partly, on the implied claim of C21.
   DESI's own quasar classification for the DR1 quasar targets (the QSO catalogue with the QuasarNET and MgII
   afterburners, the one DESI's quasar science and its target-selection validation use) disagrees with SPECTYPE on
   2.84% of kept quasar targets. Almost all of them are quasars shipped as GALAXY. The disagreements sit where the
   task is hard (quasar targets: 70.5/25.3/4.1), so they shape the hardest part of the score, and a model is
   partly rewarded for reproducing Redrock's misses. In all rows it is 0.32% (53,922 / 16.93M).
   Changes: the label definition is a known gap that is not named (USE-8: "a label definition the sources do not
   settle" -> approximate; the fit is already approximate, so the verdict stays).
   Mildest remedy: name it in curation_comments and fit_reason ("the class is Redrock's; DESI's quasar catalogue
   with afterburners calls 52,534 of the 481,259 Redrock galaxies among quasar targets quasars; about 86% vs 94%
   quasar completeness in SV visual inspection"), and drop "cannot verify" from the checklist.
   Stronger option (curator): relabel the quasar targets from the DR1 QSO catalogue (one 816 MB file, a TARGETID
   join). That is a target redefinition, so a decision, not a fix.
2. F2, the LightGBM numbers in the notes and splits_comment are refuted (P4 evidence, EV-1). This touches C12, C13,
   C24, C26. The decisions they support still hold (LEAK-10 needs no gain; SPLIT-4 needs no gap). But "+targeting
   0.100 -> 0.087" overstates the targeting columns 20-fold (measured +0.0006). Builder draft issue 1, option 3,
   cites that gain as a reason, so the curator would be weighing an artefact. The sky-holdout line reads "holding
   out makes it easier".
   Mildest remedy: re-run decisive_experiments.py with early stopping (or a fixed n_estimators chosen on a
   validation split) and replace the numbers in curation_comments, splits_comment and draft issue 1. Measured here:
   photometry 0.0866; +targeting 0.0860; random 0.0866 / nside 4 0.0869 / nside 1 0.0877.
3. F3, the ZWARN==0 filter selects on the outcome's difficulty (P3, USE-7/USE-8, should). C8 holds as written. But
   the filter drops 20.6% of ELG targets and 13.9% of quasar targets, against about 2% of the bright-galaxy,
   red-galaxy and Milky Way targets. 53,375 dropped quasar targets are catalogue quasars (17.4% of the dropped
   quasar targets). The benchmark's objects are the ones whose spectrum settled the class. A deployed classifier
   also meets the ones it would not.
   Changes: nothing in the code. Dropping unlabelled rows is the only option, and it is the release's own
   definition. The gap belongs in fit_reason next to the colour-cut selection.
   Mildest remedy: add a fit_reason clause.
4. B1, probe 19 cited as evidence about the filters (procedure). It is not, because the sub-sampling dominates the
   removed rows. Remedy: cite the per-step class shares instead (t1: Gaia-only rows 98.3% stars; ZWARN by class).
5. C11 count (1,872): a grid-cell count, not a radius count (5,211 pairs within 1 arcsec). The conclusion holds.
   Remedy: optional rewording.
6. UNTESTED: C3 (journal details; low stakes), C5's "same data" between the mirror and LBL copies (not comparable now
   that the mirror copy was replaced; rests on the source's README), Chaussidon 2023 not re-read (C22).

Not refuted, the user's focus points:
* Target from photometry only: holds. No spectral or targeting column survives (READ_COLUMNS minus drops = 45
  features; none post-spectrum).
* Dropped spectral fit and targeting decision (LEAK-10): right. Both clauses apply word for word.
* Tractor photometry fit with knowledge of the spectrum (SEL-13/14): no. DR9 predates the spectra. The Tractor
  model columns are a scope weighing worth 0.011 log loss, not a leak.
* Row filters: the main-survey, ZCAT_PRIMARY, TGT and PROGRAM!='other' filters do not depend on the outcome. ZWARN
  is a label-availability filter with an uneven, class-related effect (F3). The PHOTSYS filter removes a 98%-star
  population on an input criterion (USE-7 holds).
* Selection Bias marker as in sdss_17: holds.
* IID with no gap under a sky-region holdout: holds (0.0866 vs 0.0869 / 0.0877), with corrected numbers.

Sources looked at: https://data.desi.lbl.gov/doc/releases/dr1/ (footnote 1),
https://data.desi.lbl.gov/doc/acknowledgments/, https://arxiv.org/abs/2505.17174 (Liu et al. 2025, PASP 137 084501),
https://arxiv.org/abs/2208.08517 (DESI SV quasar visual inspection: standard pipeline about 86%, with afterburners
about 94% of VI quasars), https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/QSO/iron/ (DR1 QSO catalogue),
https://www.legacysurvey.org/dr9/catalogs/ (fibre flux "predicted"),
https://newscenter.lbl.gov/2021/01/13/building-a-giant-2d-map-of-the-universe-to-prepare-for-the-largest-3d-map/
(DR9 released 2021-01-13).

ADDENDUM (2026-11-09): I stopped I4 (the tracer-recovery baseline) and the photometry model's predictions on the
ZWARN!=0 objects after more than 60 minutes on about one core per process. This audit leaves both untested. F3
rests on the counts (t1, t4), not on a model. Add I4 to the untested list, item 6.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR - desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

Verdict: ship. No column is a leak at the prediction point (before the spectrum, from the imaging/targeting catalogue).
The LEAK-10 drops are right and complete. Two small cleaning gaps (P7) and one question for the curator (P4, weak,
1,529 rows). None of them changes a score.

Read: dataset.py, README.md, builder_report.md, probes (leak, dtype, decisive), the FITS header of zall-pix-iron.fits
(all 136 columns), the Legacy Surveys DR9 catalogue and bitmask pages as cited in the definition, principles.md,
use_case.md, leak_checks.md, selection.md (SEL-13/14), cleaning_features.md.
Data: the shipped 1.5M frame (the participant kit's data, same frame and splits as the container) and the
prepared raw Parquet restricted to the 16,930,061 kept rows (filters of _clean steps 1-2).
Script and log: the run's work files: pos_and_fixes.py, pos_and_fixes.log (LightGBM 400 trees, 300k train /
150k test per shipped fold, 3 folds).
Dtype probe: 0 of 45 flagged (the dtype probe). I agree: every measured quantity is numeric, every code and flag
categorical.

COLUMN TABLE (45 features + target)
column | meaning (DR9 catalogue / DESI zcatalog data model) | known at prediction? | dtype and cleaning | verdict | rule
SPECTYPE (target) | Redrock spectral class GALAXY/QSO/STAR | outcome | category, source words | fine | CLEAN-25
TARGET_RA, TARGET_DEC | target position (deg) from the targeting catalogue | yes (imaging) | float64 | fine; position adds nothing beyond photometry (log loss 0.0857/0.0875/0.0873 with, 0.0858/0.0874/0.0871 without; alone 0.69 vs dummy 0.72), so it does not carry the programmes' sky coverage | LEAK-10 checked, USE-6
PHOTSYS | imaging system N (BASS/MzLS) or S (DECam) | yes | category, decoded to words | fine | CLEAN-12
EBV | SFD E(B-V) at the position | yes (dust map) | float32, >0 everywhere | fine | -
MORPHTYPE | Tractor profile PSF/REX/DEV/EXP/SER/DUP | yes (image fit) | category, decoded; DUP 1 row | fine; image-model fit kept as catalogue input | SEL-14 over SEL-13
FLUX_G/R/Z | Tractor model flux, nanomaggies | yes | float32; NaN where FLUX_IVAR=0 (21/11/139 rows); negatives kept (1,262 g) | fine | CLEAN-10, CLEAN-11
FLUX_W1/W2 | unWISE forced flux, nanomaggies | yes | float32; NaN where ivar 0 (136); 88 W1 and 155 W2 values below -1000 nmgy in the full table, -52 to -30,000 sigma, mostly stars | fine (weigh, see 5) | CLEAN-11
FLUX_IVAR_G/R/Z/W1/W2 | inverse variance of the flux | yes | float32; 0 = band not measured, kept as 0 (a true "no information" value; flux already NaN) | fine | -
FIBERFLUX_G/R/Z | predicted flux of this source in a 1.5" fibre (model, imaging) | yes | float32; 0 kept where the band was not measured (see 2) | cleaning gap | CLEAN-10
FIBERTOTFLUX_G/R/Z | same incl. neighbours' flux | yes | float32; 0 in 13/5/123 of the ivar-0 rows | cleaning gap (same fix) | CLEAN-10
SERSIC | Sersic index; fitted for SER, fixed 1 (REX, EXP), 4 (DEV); 0 for PSF and DUP | yes | float32; 0 in all 488,603 PSF rows is a placeholder (see 4) | weigh | CLEAN-10
SHAPE_R | half-light radius (arcsec); 0 for PSF | yes | float32; 0 = point source, a true value of the model | fine | SEL-14
SHAPE_E1, SHAPE_E2 | ellipticity; 0 for PSF, REX | yes | float32; 0 = round, true value | fine | -
REF_CAT | reference catalogue: none, Gaia DR2 (G2), SGA-2020 (L3) | yes | category, decoded; "none" a real level | fine | CLEAN-12
GAIA_PHOT_G/BP/RP_MEAN_MAG | Gaia DR2 photometry of the match | yes | float32; 0 -> NaN: G is 0 in exactly the non-G2 rows; BP/RP 0 in 143,083 G2 rows | fine | CLEAN-10
PARALLAX, PMRA, PMDEC | Gaia astrometry (mas, mas/yr) | yes (targeting) | float32; 0 -> NaN; the three are 0 together in exactly 521,164 G2 rows (two-parameter solutions); 17,006 non-G2 rows carry values (see 1) | question | LEAK-10/LEAK-39 (weak), CLEAN-21
MASKBIT_* (13: NPRIMARY, BRIGHT, SATUR_G/R/Z, ALLMASK_G/R/Z, WISEM1/2, MEDIUM, GALAXY, CLUSTER) | DR9 MASKBITS bits 0-9, 11-13 (names match the DR9 bitmask page; 10 BAILOUT and 14/15 i-band never set) | yes (imaging masks from external star/galaxy/cluster lists) | 0/1, categorical in the container (int64 in the participant kit's parquet only); flags can co-occur, so one column each | fine | CLEAN-13, CLEAN-14

DROPPED or NEVER READ (checked against all 136 header columns):
- Spectroscopic fit, after the spectrum: Z, ZERR, DELTACHI2 (dropped); SUBTYPE, CHI2, COEFF, NPIXELS, NCOEFF,
  COADD_FIBERSTATUS, COADD_NUMEXP/EXPTIME/NUMNIGHT/NUMTILE, TSNR2_* (30), MIN/MAX/MEAN_MJD, MEAN/RMS_DELTA_X/Y,
  MEAN_PSF_TO_FIBER_SPECFLUX, MEAN/STD_FIBER_RA/DEC, MAIN_NSPEC, SV_NSPEC, ZCAT_NSPEC (never read). Correct: LEAK-10.
  Note COADD_NUMEXP / MAIN_NSPEC (number of spectroscopic exposures/spectra) would leak through the quasar targets'
  extra passes; the "number of exposures" of the imaging (NOBS_*) is not in this catalogue, so nothing is lost.
- Targeting decision: PROGRAM, DESI/BGS/MWS/SCND_TARGET, PRIORITY_INIT, NUMOBS_INIT (dropped); OBSCONDITIONS, FA_TARGET,
  FA_TYPE, SUBPRIORITY, CMX/SV1-3 bits, PLATE_RA/DEC (never read). Correct: LEAK-10 (targeting ids encode pre-selection).
- Identifiers: TARGETID (encodes release/brick/objid and target-source flags), HEALPIX, BRICKNAME, BRICKID, BRICK_OBJID,
  REF_ID, DESINAME, SPGRPVAL. Correct: CLEAN-3.
- RELEASE (9010/9012 south, 9011 north; 9012 = 95,193 reprocessed-brick rows): PHOTSYS carries the camera; fine.
- REF_EPOCH: 2015.5 in all 16,930,061 kept rows, Gaia or not: constant, CLEAN-5. Fine.
- Filters ZWARN, ZCAT_PRIMARY, MAIN_PRIMARY, OBJTYPE, SURVEY: constant after the filter. Fine.
No imaging column of the catalogue is left out (CLEAN-22 holds): the zcatalog has no NOBS, depth, PSF size, W3/W4,
FRACFLUX or Gaia error columns.

**PROBLEMS, ranked (principles.md: rank, then strength, then size)**
1. P4, question for the curator (weak; LEAK-10 pre-selection clause / LEAK-39 route; CLEAN-21 if it is another Gaia
   release). Astrometry without a Gaia match. 17,006 kept objects (1,529 shipped rows, 0.10%) have PMRA, PMDEC and
   PARALLAX filled while their Gaia magnitudes are 0 and REF_CAT is none (11,382) or SGA (5,624). In the DR9 catalogue the
   Gaia columns come with a G2 reference, so these values have another origin that the definition does not name. They
   are 59% stars in the shipped rows (900 of 1,529; 60% of 17,006), against 0.9% stars in the other rows without Gaia.
   86% are in the bright programme and 90% are BGS targets. The fibre map is written before observation, so this is no
   timing leak. But the values seem to come from a route tied to the programme (perhaps an astrometry update at fibre
   assignment; a search found fiberassign's PMCORR keyword, not this), and the use case's catalogue object would not
   have them. Size: at most 1,529 rows of 1.5M; I did not measure a separate gain. Mildest remedy: trace the origin in the
   fiberassign / desitarget data model. If it is the targeting route, blank PMRA/PMDEC/PARALLAX where REF_CAT is not G2
   (one line in step 3). Otherwise add one sentence to the Gaia bullet.

2. P7, cleaning gap (CLEAN-10, Should; cheap and safe). Fibre fluxes of a band that was not measured stay 0. The
   definition sets FLUX_b to missing where FLUX_IVAR_b = 0, but leaves FIBERFLUX_b at 0 in those rows: 21 of 21 (g),
   11 of 11 (r), 138 of 139 (z) shipped rows. FIBERTOTFLUX_b is also 0 in 13/5/123 of them. Those are the same proxy
   values, and 135 of the 139 z rows are stars (see 3). Remedy: in step 3, mask FIBERFLUX_b where FLUX_IVAR_b == 0, and
   mask FIBERTOTFLUX_b where it is 0 in those rows (a non-zero value there is neighbours' light, so keep it); add a
   clause to the missing-values bullet. Measured: no change (0.0857/0.0877/0.0871 against
   0.0857/0.0875/0.0873). Separate case, keep: FIBERFLUX_G = 0 in 1,262 rows whose FLUX_G is negative is Tractor's floor
   on a negative model flux, a published value, not a missing value.

3. P4, note only (selection, already named in fit_reason). An unmeasured band follows the targeting route. Of the
   1,461 kept objects with FLUX_IVAR_Z = 0, 1,409 are stars and 1,429 are Milky Way targets. W1/W2 not measured: 1,446
   of 1,745 are stars. The MWS selection needs no z or WISE band, and the galaxy and quasar cuts do. So missingness
   brings the targeting class back for 0.01% of the rows. It is known from the imaging, so it stays. Remedy: one clause
   in the selection-bias bullet; no change to the data.

4. P7, weigh (CLEAN-10; lossless either way). SERSIC = 0 in all 488,603 PSF rows (and the one DUP row). A point
   source has no Sersic index. The fixed profiles' 1 (REX, EXP) and 4 (DEV) are real values of their models, but 0 is
   no point on the Sersic scale (n -> 0 is not a point source), so it is a placeholder. MORPHTYPE already says PSF, so
   no information is lost either way, and the score does not move (included in the fix of 2). Options: set SERSIC
   missing for PSF/DUP, or keep it with a sentence ("0 for point sources") in the notes. SHAPE_R = 0 (no size) and
   SHAPE_E1/E2 = 0 (round) are true values of the model: keep them.

5. P7, weigh (CLEAN-11). Extreme negative WISE fluxes: 88 (W1) and 155 (W2) values below -1000 nanomaggies, down to
   -224,146 and -2,704,847, at -52 to -30,000 sigma. 69 and 117 of them are stars, probably forced photometry near
   bright stars. They are the catalogue's published measurements, so the actor's model sees them. Keep them as
   published (unusual, not impossible as a measurement), or blank values below about -50 sigma as failed fits. I
   lean to keep; 0.002% of rows.

Agreements with the builder (no action):
- LEAK-10 drops (spectral fit; targeting columns and programme) are right; the never-read columns above also hold
  nothing usable at the prediction point.
- SEL-14 over SEL-13 for MORPHTYPE, SHAPE_*, SERSIC and the fibre fluxes: the whole dataset is catalogue photometry
  read by tabular classifiers (sdss_17 precedent); dropping one of them alone changes nothing (0.991 macro AUC).
- Gaia sentinels: the G mag is 0 in exactly the non-G2 rows; PARALLAX, PMRA and PMDEC are 0 together (521,164 rows,
  14.7% of the G2 rows, two-parameter solutions). The masking is exact. The missingness differs by class (78.9% of G2
  galaxies have no parallax, 0.8% of G2 stars), but it is a property of the source known at imaging, not of the
  outcome.
- Number-format probe 17 (0.940) is MORPHTYPE's fixed parameters plus the Gaia match, as the builder found.
- Row filter ZWARN = 0 is a cohort choice (builder issue 3), not a feature. It changes no column.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

VERDICT: right with notes. Random 3-fold over objects (IID) is the regime the use case implies. No sky-region,
imaging-system or hidden-group structure moves the score once model noise is controlled. Two notes for the curator, both
about writing (no re-split, gap or filter): the splits_comment's numbers read as noise, and the cost the selection gap
would add (fainter objects, another programme's mix) could be stated with a number.

Judgment record
  Validity: USE-10 holds (a new object each time, no recurring entity with history); SPLIT-1/SPLIT-2 hold (IID);
  SPLIT-3/SPLIT-7 n/a (no time axis: one fixed imaging catalogue (LS DR9) for every row, and the class does not
  change over the 13 months); SPLIT-4 holds (the sky position is a feature every new object has, not an entity);
  SPLIT-29/SPLIT-30 hold (no hidden group: probe no hits, near-copy gap +0.000, sky-pixel gap 0 under a calibrated
  model); USE-8 approximate + `Selection Bias` already declared and confirmed by the measurements below.
  For the curator: issue 1 (wording of splits_comment), issue 2 (optional sentence sizing the selection gap).

HOW I MEASURED
  Builder's sample re-drawn: the 16,930,061 shipped objects (same filters as _clean, read from
  zall_pix_iron_main.parquet), 600,000 drawn with default_rng(0), cleaned with the definition's own _clean; LightGBM
  with the builder's settings (400 trees, lr 0.1, 63 leaves) unless marked "regularised" (300 trees, lr 0.05,
  min_child_samples 100). Sky groups from HEALPIX (nside 64, nested), coarser levels by integer division; group folds
  assigned to whole pixels at random (interleaved patches). Every alternative is compared with the random-fold
  out-of-fold predictions on the same rows.
  Scripts and logs: the run's work files.

1. THE REGIME THE USE CASE IMPLIES
  - Who uses it: a survey team classifying catalogue objects with no spectrum (DESI's quasar random forest; Liu et al.
    2025). Each prediction is about a new object, and the object never comes back with history: IID unless the
    deployment objects sit in sky, depth or a selection the training objects do not cover.
  - Sky coverage: the shipped objects fill 16,363 nside-64 pixels, about 13,733 deg2: nearly the whole Legacy
    Surveys / DESI footprint (DR1 tiles: 9,739 deg2 bright, 9,528 deg2 dark per the DR1 page; the survey's planned
    footprint 14,000 deg2, later extended). The Tractor photometry exists only inside that footprint. So later DESI
    years, and any user of these catalogue columns, classify objects in sky the training data already covers (more
    passes and the remaining tiles). "Elsewhere on the sky" means interleaved patches inside the footprint, not a new
    hemisphere.
  - Time: none to split on. The features come from one imaging release (DR9, before every spectrum). The
    label is the class of a static object. DR1's 13 months are an observing order, not a drift in what is predicted.

2. SKY-REGION (HEALPIX) SPLITS: NO GAP; THE BUILDER'S DIFFERENCES ARE MODEL NOISE
  Pooled out-of-fold log loss, 600k objects, 3 folds:
    random, StratifiedKFold seeds 0 / 1 / 2       0.1059 / 0.1013 / 0.0909   (accuracy 0.9697-0.9703)
    HEALPix nside 64 (0.84 deg2), seeds 1 / 2     0.0875 / 0.1046
    nside 8 (54 deg2)                              0.0873
    nside 4 (215 deg2), seeds 1 / 2                0.0890 / 0.0877
    nside 2 (860 deg2, 31 groups)                  0.0882
    regularised: random 0.0848, nside 64 0.0850   (difference +0.0002)
    clipped at 1e-3: random 0.0872-0.0907, nside 64 0.0864-0.0904
  With the builder's settings, 0.3% of the rows (1,786-2,144 rows with a loss above 5) carry 22-35% of the log
  loss, so a seed or fold change moves the pooled score by +-0.008. The per-row paired SE (about 0.001) hides
  this, because the variance is between models. Under the regularised model the random and sky-grouped splits agree
  to 0.0002. The splits_comment cites "0.100 random, 0.099 nside 64, 0.088 nside 4", which reads as if holding out sky
  makes the task easier. It does not: those numbers fall inside the seed spread.
  Position as a feature: dropping TARGET_RA/TARGET_DEC under nside-4 holdout gives 0.0876 against 0.0890 with them
  (paired -0.0014, SE 0.00025). The model gains nothing from the position in unseen patches. Shared imaging depth
  and calibration between neighbours carry no label shortcut a random split would reward (SPLIT-29 not met).

3. A WHOLE SKY AREA HELD OUT (leave one nside-1 base pixel out, ~3,400 deg2; same rows' random OOF from seed 0,
   itself about 0.01 high)
    base 0 (RA 34, Dec +22)  0.118 vs 0.132     base 6 (RA 178, Dec 0)  0.078 vs 0.110
    base 1 (RA 129, Dec +38) 0.086 vs 0.101     base 7 (RA 253, Dec +10) 0.120 vs 0.113
    base 2 (RA 227, Dec +34) 0.078 vs 0.092     base 8 (RA 47, Dec -11) 0.114 vs 0.119
    base 3 (RA 317, Dec +27) 0.083 vs 0.096     base 9 (RA 136, Dec -5) 0.087 vs 0.145
    base 4 (RA 41, Dec +3)   0.143 vs 0.110     base 5 (RA 69, Dec -3)  0.147 vs 0.103
  Only bases 4 and 5 lose (+0.033, +0.044 against a noisy baseline, so about +0.05 against a typical one). They are
  the equatorial south-galactic-cap area with the deepest DECam z imaging (median FLUX_IVAR_Z 62 against 34-47
  elsewhere, 100% PHOTSYS S) and a higher quasar share (12.0% in base 4). This is a depth domain shift for a region
  the model has never seen. It is not the deployment case: DR1 already has training objects in that region (2.7M
  and 0.9M shipped objects). No change. It is at most a candidate variant (SPLIT-31) for "a new imaging
  depth", which no use case we cite asks for.

4. IMAGING SYSTEM (PHOTSYS) HELD OUT (two groups only: a domain-shift test, weighed factor "only a few groups")
    train S, test N (133,510): 0.081 vs random 0.087;  train N (133k), test S (466,490): 0.127 vs 0.112.
  The second loses mostly through the 3.5x smaller training side. A deployed model trains on both systems. No
  change.

5. TARGETING PROGRAMME HELD OUT (covariate and prior shift, USE-8 `Selection Bias`)
  Sample mix: dark 304,500 (79.3% galaxy, 16.9% quasar, 3.8% star), bright 295,500 (71.3% / 0.7% / 28.0%). No
  backup-programme row survives the Legacy Surveys filter.
    train bright, test dark: log loss 1.185, accuracy 79.6%, against 0.172 / 94.9% on the same rows under random folds
    train dark, test bright: 0.069 / 98.3% against 0.038 / 99.1%
  This is not a realistic split. The bright programme holds almost no quasars, so the first line measures a model
  that never saw the class. A survey's classifier trains on all its spectroscopic programmes, and the programme
  is dropped as a feature (LEAK-10). The test's programme mix equals training's (random objects), as the split
  sentence says ("chose for a spectrum in the same way"). The use case's population, objects without a spectrum,
  differs from the training mix. That is the selection gap the approximate fit and the marker already name. It is
  not a split error, since no labelled objects outside the selection exist.

6. FAINTER OBJECTS (the use case's "more than 99%" are mostly fainter or outside the colour cuts)
  Train on the brighter two thirds in FLUX_R, test on the faintest third (200,000): 0.482 against 0.178 on the same
  rows under random folds (2.7x). This is confounded with the class and programme mix (the faint third is dark-time
  heavy), but it gives the size of the extrapolation the use case's fainter objects would meet. It cannot be a split:
  the release has no labelled objects outside the targeting cuts. It supports the approximate fit. See issue 2.

7. NEAR COPIES AND THE 1,872 OBJECTS IN A SHARED 1-ARCSEC CELL (SPLIT-29, LEAK-16 to LEAK-21)
  1,855 cells hold 3,727 objects (builder's explore2b.log): 1,609 SS, 228 NN, 14 SSS, 3 NNN, 1 NS. 1,786 cells
  (96.3%) share one class. DESI fibres are 1.5 arcsec, so two fibres 1 arcsec apart see much of the same light, and
  the label is close to shared. But the 1.5M sub-sample keeps both members of a cell with probability about
  (1.5/16.93)^2 = 0.8%: about 15 pairs expected in the shipped table, about 10 of them across train and test in a
  fold. Negligible. Keep them, no filter. The hidden-group probe agrees: near-copy clusters at 0.85 hold 8.0% of
  rows, gap +0.000. SERSIC and SHAPE_R candidates have negative gaps (-0.038, -0.015). There are 0 exact copies.

8. OTHER SPLIT FACTS CHECKED
  - Shipped split: 3 folds of 1M train / 500k test over a class-stratified 1.5M sub-sample (check2.log: 3 of 3
    splits; smallest class in a test fold 17,841 rows). Consistent with splits_comment and version_comment.
  - No group or time column is declared, and none should be: HEALPIX and TARGETID are dropped, and RA/Dec stay as
    features, as in sdss_17.
  - Precedent: sdss_17 (same task, another survey) ships IID, kept after a plate-grouping test (record, CC
    2026-10-01). These measurements give no fact that sets DESI apart from it.

ISSUES (rank order, principles.md)
  1. P4, evidence (EV-1, EV-3; SPLIT-4). splits_comment states "0.100 random, 0.099 nside 64, 0.088 nside 4",
     differences inside the model's seed spread (0.091-0.106 on random folds alone), and it implies sky holdout
     helps. The conclusion (IID) stands. Mildest remedy: reword. For example: "Holding out whole sky regions
     changes nothing: with a regularised LightGBM (600k objects, 3 folds) random folds score log loss 0.0848 and
     folds of HEALPix pixels of 0.84 deg2 0.0850; at 54 to 860 deg2 the pooled scores (0.087-0.089) fall inside the
     random folds' seed spread (0.091-0.106 with 400 unregularised trees, whose log loss 0.3% of the rows dominate).
     Only a whole ~3,400 deg2 area never seen, the deep equatorial DECam sky, costs about 0.04, and the shipped
     objects cover 13,700 deg2, nearly the whole footprint." Strength: Should-level wording fix; no re-split.
  2. P3 (USE-8, `Selection Bias`, weigh). fit_reason names the selection but not its size. Optional: add one clause
     with the measurement. A model trained on the brighter two thirds scores 0.48 on the faintest third against
     0.18 under random folds, and the bright programme alone cannot classify dark-time quasars (1.19 against 0.17).
     This shows how far scores on targets may sit from the non-targets the use case classifies. Note only.
  3. (aside for the metric/task reviewers, P6, not a split issue) LightGBM's log loss here is driven by a few
     confidently wrong rows: 22-35% of the loss comes from 0.3% of the rows. Comparisons between models on this
     dataset will be sensitive to calibration and regularisation. No change proposed.

  No re-split, gap or filter is needed.

Sources: DESI DR1 page https://data.desi.lbl.gov/doc/releases/dr1/ (tile areas); DR1 paper arXiv:2503.14745
(identical bright and dark footprints); DESI news release, 2026-04-15 (14,000 deg2 planned, extending to 17,000).

</details>

<details><summary>Domain practitioner</summary>

Domain practitioner report: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09
Actor: an astronomer who classifies imaging-survey sources as star, galaxy or quasar from photometry alone, either
(a) to select spectroscopic targets (quasar candidates for a DESI-like survey) or (b) to label a photometric catalogue
or alert stream where no spectra exist (>99% of Legacy Surveys sources).

VERDICT
Fit: approximate (agree with the definition). One sentence: the inputs are exactly what I have before a spectrum and
one row is one object I classify, but the rows are DESI's colour-selected targets (bright Gaia stars and pre-selected
galaxy and quasar candidates, not the sources I classify) and the label is Redrock's pipeline class, which misses
about one quasar in seven that DESI's own quasar catalogue recovers with its afterburners.
Metric scores the decision: partly. log_loss is the metric I would pick too (MET-8: no source fixes a threshold or
density for this three-class task, MET-6/MET-7 do not apply; MET-9 rules out average precision for imbalance alone);
what it averages over is the target mix, not my catalogue's mix, and that is the population gap, not a metric fault.
No change proposed to the metric.

MY ANSWERS AS THE ACTOR
1. Inputs at the prediction point (USE-3, USE-6). I have every shipped input when I classify: Legacy Surveys DR9
   Tractor fluxes g, r, z, W1, W2 with inverse variances, fibre fluxes, MORPHTYPE/shape/Sersic, MASKBITS, EBV, Gaia DR2
   magnitudes, parallax and proper motions, position. Nothing shipped comes after the spectrum: Z/ZERR/DELTACHI2 and
   the targeting bits are dropped (LEAK-10). Position is a legitimate input for me (Galactic latitude is the star
   prior; depth varies by region). Inputs I would always have and that are missing, because the redshift catalogue
   does not copy them from the Legacy Surveys sweeps: DCHISQ (chi-square differences between the PSF, REX, DEV, EXP,
   SER fits; the standard star-galaxy input), NOBS / PSFDEPTH / PSFSIZE / GALDEPTH, FRACFLUX / FRACMASKED / FRACIN,
   WISE W3/W4, and WISE light-curve variability (used for eBOSS quasar selection). The zall file keeps RELEASE,
   BRICKID, BRICK_OBJID, so a rebuild could join them from the DR9 sweeps. A gap of a few features, not of the task.
2. Target (USE-5). I act on the object's true class. SPECTYPE is Redrock's class: a close proxy for stars and
   galaxies, a weaker one for quasars. DESI's survey-validation visual inspection found the standard pipeline recovers
   about 86% of visually confirmed quasars, the pipeline plus the MgII and QuasarNET afterburners about 94%, at about
   99% purity (Alexander et al. 2023); the misses are mostly quasars Redrock calls GALAXY. On the shipped rows
   (my measurement, prepared Parquet, same filters as _clean, 16,930,061 objects): the 1,900,008 quasar targets are
   70.53% QSO / 25.33% GALAXY / 4.14% STAR, against 71% quasars / 16% galaxies / 6% stars / 7% inconclusive by visual
   inspection in Chaussidon et al. (2023) (76/17/6.5 among the conclusive). So roughly 8 points of the quasar targets,
   on the order of 150k objects (about 1/3 of their GALAXY labels, about 0.9% of all rows), are likely quasars labelled
   GALAXY (different samples: SV deep exposures against main-survey nominal depth, so an order of magnitude, not a
   count). Consistent with it: all QSO-target GALAXY labels are PSF sources, 44.3% of them at Redrock z > 1.0, median
   z 0.94. The noise sits in exactly the subset that carries the task's non-trivial signal (within quasar targets the
   photometry model scores 0.400 log loss against 0.726 for the shares; elsewhere it is near the prior). I want class
   probabilities (I threshold them per class or rank quasar candidates at a fixed density), so a probabilistic
   three-class target is right.
3. Rows and test data (USE-8, USE-10). One row is one object, one classification: matches. The test fold is other
   DESI targets of the same sky area. For use (a) "which of my quasar candidates are real" the test matches the
   quasar-target subset; for use (b) it does not: the rows are what DESI's cuts let through. Measured on the shipped
   rows: 92.1% of the stars are Milky Way Survey targets, 95% of stars have a Gaia match, star median r 18.0, 95% of
   stars brighter than r 19.85; only 121,466 stars (0.72% of rows) are fainter than r 20, where faint stars are the
   main contaminant of quasar samples (r 20-23 bins: 2.8%, 3.3%, 0.5% stars). The galaxies are BGS (r < 19.5), LRG
   and ELG colour boxes; a real catalogue to r about 24 is dominated by faint galaxies and faint stars outside those
   boxes. The class shares (75.4/15.6/9.0) are those of the targets, not of any catalogue. A new-object IID split is
   right for the same footprint; the sky-region holdout shows no gap (0.099/0.088 vs 0.100), so new sky is not a gap.
4. Would I use it? For use (a), ranking quasar candidates within DESI-like cuts: yes, it is close to the random-forest
   step DESI runs (Chaussidon et al. 2023 uses g, r, z, W1, W2 and r; morphology PSF), after recalibrating to my
   prior. For use (b), a full photometric catalogue: no, not without a representative validation set: Liu et al.
   (2025, PASP 137, 084501) train their Legacy Surveys resolved/unresolved model on HST COSMOS morphology and only
   evaluate on DESI DR1 spectra, and note spectra exist for under 1% of the sources. What would make me trust it:
   purity and completeness per class in magnitude bins, especially quasars against faint stars at r 20-23, and labels
   corrected by the afterburners. What makes me distrust it: easy bright Gaia stars inflate the star score, and the
   model learns Redrock's quasar misses as "galaxy".
5. Metric (MET-1, MET-6 to MET-9). My decision is a per-class threshold (catalogue purity and completeness) or a
   quasar target density per square degree. Chaussidon et al. fix a density (310 per sq. deg.), but that density is
   over all Legacy Surveys objects in the footprint and cannot be computed on targets only, so no threshold metric is
   fixed for this task (MET-6, MET-7). A strictly proper score of the class probabilities serves any threshold I pick
   later (MET-8): log_loss is what I would choose. A one-vs-rest quasar ROC AUC or average precision would score only
   one of my two uses and MET-9 does not allow AP for imbalance alone. The unit is right (one object = one decision,
   no weight needed, MET-17 not engaged). The "partly" is that the score averages over the target mix, 75% galaxies
   that are mostly trivially separated, so the differences between models come from the ~11% quasar targets; that is
   the population gap (finding 1), and no metric repairs it.

GAPS BETWEEN THE DATASET AND THE REAL DECISION, ranked by how much they change the task
1. Population (USE-8 selection judged against the setting; marker Selection Bias, as sdss_17). The setting of use (b)
   does not share DESI's target selection: stars are 92% bright MWS targets, faint stars are 0.7% of rows, galaxies
   sit in four colour boxes. Already named in fit_reason; fit approximate is right. For use (a) on quasar targets the
   setting does share it (builder's issue 1, quasar-target version, would be closer to direct).
2. Label is Redrock-only SPECTYPE (USE-5, label a known gap under USE-8). About 14% of quasars missed by the
   standard pipeline in VI; roughly a third of the quasar targets' GALAXY labels are likely quasars. Not named
   anywhere in the definition: fit_reason and curation_comments say only "the class DESI's pipeline fit". This is a
   second known gap for the approximate fit and should be named.
3. ZWARN 0 filter (USE-7 territory, builder's issue 3): the shipped objects are those whose spectrum settled the
   class; the ambiguous ones (10.1% of galaxy-fitted, 4.0% of quasar-fitted spectra) are exactly objects I would face
   photometrically. Acceptable as a label-quality filter (the release's own "useful spectra"); a small gap.
4. Missing standard inputs (DCHISQ, depth/PSF size, FRACFLUX, W3/W4, variability): a small change to the task; the
   features present (MORPHTYPE, SHAPE_R, SERSIC, Gaia) carry most of what DCHISQ would.
5. Prior: probabilities are calibrated to the target mix; any catalogue use needs a prior shift. A note, not a fix.

WHAT AN EXPERT WOULD CHANGE
- Name the label gap in fit_reason and the notes: "SPECTYPE is Redrock's class alone; DESI's quasar catalogue adds
  the MgII and QuasarNET afterburners, which recover about 8% more of the visually confirmed quasars (86% to 94%,
  Alexander et al. 2023), most of them labelled GALAXY here, among the quasar targets". Severity: should (USE-5/USE-8).
- Better, if the curator wants a rebuild: relabel with the afterburner-corrected class (the DR1 QSO selection used
  for the LSS QSO sample, or the DR1 AGN/Galaxy Classification VAC listed on the DR1 page, "AGN and QSO identification
  for galaxies from all target classes"). I did not verify those files' columns; a weigh item for the curator.
- Optional: join DCHISQ and depth columns from the DR9 sweeps by BRICKID/BRICK_OBJID (could, not needed for validity).
- Keep the sdss_17 framing, the IID split, log_loss, the LEAK-10 drops and the Tractor columns (SEL-14: every
  practitioner's catalogue classifier reads them; DESI's own QSO cut requires MORPHTYPE PSF).
- The quasar-target version (builder's issue 1) is the use case a DESI astronomer actually runs and the one where the
  label noise matters most; if it ships, the label gap there is the main one.

NUMBERS I MEASURED (scripts and logs in the run's work files: label_check.py/.log, star_check.py/.log;
read-only on the prepared Parquet, filters identical to _clean steps 1-2)
- Quasar targets: 1,900,008 (11.2% of rows); SPECTYPE 70.53% QSO, 25.33% GALAXY, 4.14% STAR.
- Their GALAXY labels: 100% MORPHTYPE PSF; Redrock z quantiles 0.24/0.64/0.94/1.23/1.45 (10/25/50/75/90%); 44.3% at
  z > 1.0, 2.8% at z > 1.6; 12.9% with DELTACHI2 < 25.
- Stars: 92.1% MWS targets, 3.1% BGS, 3.0% QSO, 1.3% LRG; 95.0% Gaia-matched; r quantiles 16.35/18.04/19.85
  (5/50/95%); 121,466 stars at r > 20.
- Class mix by r: r<18 65% stars; 19-20 91% galaxies; 21-22 34% quasars; 23+ 97% galaxies.
- MORPHTYPE PSF: 91.4% of quasars, 98.2% of stars, 12.0% of galaxies.

SOURCES
- DESI DR1 page, footnote on useful spectra; VAC list incl. AGN/Galaxy Classification Catalog:
  https://data.desi.lbl.gov/doc/releases/dr1/
- Alexander et al. 2023, DESI SV visual inspection of quasar spectra (pipeline ~86% vs ~94% with afterburners, ~99%
  purity): https://arxiv.org/abs/2208.08517
- Chaussidon et al. 2023, target selection and validation of DESI quasars (RF on g, r, z, W1, W2; 16.5<r<23; 310 per
  sq. deg.; VI 71% quasars, 16% galaxies, 6% stars, 7% inconclusive): https://arxiv.org/abs/2208.08511
- Farr et al. 2020, optimal strategies for identifying quasars in DESI (afterburners): https://arxiv.org/abs/2007.10348
- Liu et al. 2025, PASP 137, 084501, resolved/unresolved XGBoost on Legacy Surveys, trained on HST COSMOS labels,
  evaluated on DESI DR1: https://arxiv.org/abs/2505.17174
- Rules: use_case.md USE-3, USE-5, USE-6, USE-7, USE-8, USE-9, USE-10; metrics.md MET-1, MET-6, MET-7, MET-8,
  MET-9, MET-17; leak_checks LEAK-10; selection SEL-14.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: desi_dr1_star_galaxy_quasar (target SPECTYPE, 3-class, 1.5M rows x 45 features, IID 3-fold)
Inputs used: the clean room's data (200k-row sample) and task description, the public DESI DR1 pages, and web search results on the DR1 paper and the DESI QSO pipeline. I opened no other local file.
Scratch script: the run's work files: lgb.py

VERDICT: Include with changes. The data is real, comes from imaging taken before the spectrum, and is useful, but the provenance and filtering need to be written down, the label's known QSO incompleteness needs to be stated (or the label fixed), and models will be separated only within the last ~3% of error.

WHAT THE TASK IS
Each row is a DESI DR1 spectroscopic target. The features are its Legacy Surveys DR9 Tractor photometry (g/r/z/W1/W2 fluxes and inverse variances, fiber fluxes, morphology/shape, maskbits split into 0/1 columns, EBV) plus Gaia DR2 magnitudes and astrometry. The target is the Redrock spectral class (GALAXY/QSO/STAR) measured from the DESI spectrum. Use case: classify sources from imaging alone before any spectroscopy. People who would do this: spectroscopic survey planners (target selection and fiber prioritisation for DESI-II or 4MOST) and anyone building a photometric quasar or star catalogue. This is a real and common astronomy task, with SDSS star/galaxy/QSO as the classic version. All features exist before the spectrum is taken. The table has no spectroscopic columns (Z, ZWARN, DELTACHI2, targeting bits), so I found no leakage.

EVIDENCE SUMMARY
- Classes: GALAXY 75.3%, STAR 15.7%, QSO 9.0% (150,620 / 31,371 / 18,009 in the 200k sample).
- LightGBM, 3-fold CV on the 200k sample (500 trees, lr 0.05, 127 leaves): accuracy 0.9697, balanced accuracy 0.935, log loss 0.108. Majority-class accuracy is 0.753. Log loss of the class priors is about 0.72.
- Confusion matrix (rows = true G/Q/S): [[148105, 2194, 321], [2659, 15256, 94], [325, 471, 30575]]. Nearly all errors are GALAXY<->QSO.
- Ablations: MORPHTYPE+REF_CAT alone 0.898 acc; the 5 raw fluxes alone 0.955; dropping RA/Dec 0.9693 (no change); RA/Dec alone 0.752, which is the majority rate. Position therefore carries no signal and I see no spatial leakage.
- Duplicates: 0 exact rows, 0 duplicated (RA, Dec) at 1e-4 deg, 0 duplicated feature vectors.
- Values are plausible. Median r is 20.3 for galaxies, 21.4 for QSOs and 18.1 for stars. 94.6% of stars have Gaia proper motions, against 0.9% of galaxies. FIBERFLUX <= FIBERTOTFLUX <= FLUX holds in every row. SERSIC is 0/1/4/6 exactly for PSF/EXP/REX/DEV models, which is the Tractor convention. Dec runs from -19.4 to 79.1, which fits the DR1 footprint. The class mix is the same in every row-order decile.

CONCERNS (most to least serious)

1. The label is Redrock SPECTYPE, which is known to miss roughly 10-20% of real quasars, and the errors left for models to fight over sit exactly there.
   Evidence: DESI's own documentation says "DESI employs two quasar-specific classifiers, 'afterburners', to enhance the completeness of the quasar sample by ~10%", and the DESI QSO target-selection paper (arXiv:2208.08511) puts Redrock's QSO class alone at an efficiency "of the order of 80%". In my CV, 2,659 of 18,009 QSOs (14.8%) are predicted GALAXY and 2,194 GALAXY are predicted QSO. These ~4.9k GALAXY<->QSO swaps make up ~80% of all errors. Some of them are probably correct predictions scored against a wrong label: low-z AGN and Mg II quasars that Redrock called GALAXY.
   Change: take the QSO class from the DR1 QSO catalogue or the AGN/Galaxy VAC (Redrock + Mg II + QuasarNET), or at minimum record that the label is pipeline-Redrock with known QSO incompleteness. Report log loss as well as accuracy, so that differences in the noisy last few percent are not overread.

2. Provenance and filtering are not documented, and the class mix does not match the published DR1 numbers.
   Evidence: task.md gives 1.5M rows but not which catalogue they come from (zpix or ztile, main-only or SV + special), nor which cuts were applied (ZWARN==0, ZCAT_PRIMARY, OBJTYPE=='TGT', a Tractor-match requirement). The DR1 docs list 13,049,402 galaxies, 1,553,713 quasars and 4,056,689 stars among main-survey "useful spectra" (70% / 8.3% / 21.7%). This sample is 75.3% / 9.0% / 15.7%, so stars are under-represented by about a quarter. That points to an unstated selection, for example dropping backup-program or Gaia-only targets without Tractor photometry, or sampling by program. The DR1 page defines "useful spectra" as OBJTYPE=='TGT', ZWARN==0, ZCAT_PRIMARY. If ZWARN==0 was applied, the faint objects with failed redshifts (the hardest ones) are gone, which flatters scores. If ZCAT_PRIMARY was not applied, the same target can appear twice (SV + main), possibly across train and test. I found no positional duplicates in the 200k sample, but the sample is only 13% of the rows.
   Change: write down the source file, the cuts, how the 1.5M were sampled from ~20M, and the TARGETID dedup. Check (RA, Dec) duplicates on the full 1.5M.

3. The population is "objects DESI chose to observe", not "all imaging sources".
   Evidence: DESI targets are chosen by colour/magnitude/morphology cuts on these same features (BGS, LRG, ELG, QSO, MWS). Morphology and Gaia match alone give 0.898 accuracy, and 5 fluxes give 0.955. The task is valid and IID-honest for "classify a DESI-like target before spectroscopy", but it partly re-learns the targeting algorithm. Scores will not carry over to a flux-limited sample.
   Change: say so in the task description. Optionally add the targeting class as context, or keep it out on purpose and say that it is out.

4. The task is not trivial, but headroom is thin.
   Evidence: one untuned GBDT reaches 0.970 accuracy, and 5 fluxes reach 0.955. Strong methods will probably fall within ~0.3-0.5 percentage points of each other, and part of what is left is label noise (concern 1). With ~500k test rows per fold, those gaps are statistically resolvable but may not mean much scientifically.
   Change: use log loss or balanced accuracy / macro-F1 as the main metric. The QSO class is where the methods differ.

5. Smaller preparation points.
   - FLUX_R/Z/W1/W2 are set to NaN in 1/17/20/20 rows, apparently where FLUX_IVAR is 0 (counts match for R and Z). That is a sensible encoding, but it is undocumented.
   - Gaia columns are NaN in 79% of rows. The missingness is fully explained by REF_CAT and is itself informative. PARALLAX/PM is non-null in 159 rows with REF_CAT 'none' and null in 6,146 Gaia rows (2-parameter solutions). That is plausible, but worth a note.
   - FIBERTOTFLUX_* equal FIBERFLUX_* in most rows (near-duplicate columns). Harmless.
   - Structural zeros: SHAPE_R/E1/E2/SERSIC are exactly 0 for PSF sources. Correct Tractor convention, and fine as it is.
   - The 13 MASKBIT_* binaries are very sparse (NPRIMARY 0.01%, CLUSTER 0.005%). Harmless.
   - TARGET_RA/TARGET_DEC add nothing (see ablation). Keeping them is harmless, but dropping them avoids position-based shortcuts in other subsets.
   - Category levels carry long text labels (e.g. "PSF (point source)"). Fine.
   Dtypes are otherwise sensible (category for PHOTSYS/MORPHTYPE/REF_CAT/target, float32 photometry).

WHAT I COULD NOT CHECK
- The full 1.5M rows, and so whether train/test duplicates exist at full size. I had only the 200k sample.
- The exact source file, cuts and TARGETID dedup. The DR1 docs page does not list the columns, and the data-model page I tried returned 404 or did not define them.
- The ADS abstract (HTTP 405). I confirmed the paper (DESI DR1, AJ 171, 285, arXiv:2503.14745) through search results only.
- Whether the label includes afterburner corrections. It looks like plain Redrock, but I cannot confirm that without the source catalogue.
- How much of the 3% residual error is label noise rather than model error. That would need VI truth tables.

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: desi_dr1_star_galaxy_quasar (SPECTYPE, 3-class, log_loss, IID 1x3 folds, 1.5M rows)

Verdict: none of the attacks I ran games this task. Every exploit stays within the noise of the honest models (spread from a random column: about 0.0001 on the mean, 0.0003 per split). The only gain I measured (-0.0003, from prior-matching the test probabilities) is plain calibration that a deployed model can also apply.

Honest models (scripts in ; log_loss, lower is better; per split r0f0/r0f1/r0f2)
- Baseline, untuned LightGBM on features():     0.08713  [0.08622, 0.08761, 0.08758]   baseline.py
- Stronger honest LightGBM (colours, S/N, fibre fractions, Galactic latitude, 1500 trees, lr 0.05, 127 leaves):
                                                 0.08444  [0.0833, 0.08504, 0.08497]    strong.py strong
- Baseline + one random-number column, 3 seeds:  0.08709 / 0.08712 / 0.08701 (noise spread about +-0.0001 on the mean, up to 0.0003 per split)

Exploits ranked by gain
| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Reweight each test fold's class probabilities so their mean equals the exactly known (stratified) prior | prior_match.py, prior_cross.py | strong 0.08444 | 0.08416 | -0.00030/-0.00027/-0.00024 | Yes. Weights fitted on another fold's test rows give the same 0.08417, so this is calibration of an overconfident model, not test-composition information | none needed |
| 2 | Sky kNN label features (class shares among the 5/20/50 nearest training rows, nearest label and separation) | attacks1.py knn, strong.py strong_knn | 0.08713 / 0.08444 | 0.08721 / 0.08494 | +0.0000 to +0.0006 (worse) | Partly (labels of earlier spectra nearby) | none needed |
| 3 | Sky density computed over train+test rows (counts within 30"/60"/120"/300", 1st and 10th neighbour distances) | attacks1.py density, strong.py strong_density | 0.08713 / 0.08444 | 0.08729 / 0.08472 | -0.0001 to +0.0004 (none) | No (needs the observed test set) | none needed |
| 4 | Sky density over training rows only | attacks1.py density | 0.08713 | 0.08707 | -0.00015/-0.00002/-0.00002 | Yes | none needed |
| 5 | Row position as a feature | attacks1.py rowpos | 0.08713 | 0.08709 | within noise | No | none needed |
| 6 | Format features (float32 mantissa trailing zeros, RA/Dec repr digit counts and last digit) added to the baseline | formats.py | 0.08713 | 0.08718 | within noise | n/a | none needed |

Flaws that hurt an honest model: none found. There is no time column, the folds are random and stratified (each test fold has the class shares 0.754/0.0896/0.1564 exactly), and nothing I found in training is mislabelled or filtered by its outcome in a way that the test fold is not.

Findings in detail
1. Prior matching. The 1500-tree model is overconfident on GALAXY. Its mean test prediction is GALAXY 0.7562 against a prior of 0.7540, and the fitted class weights are about [0.92, 1.05, 1.45]. Reweighting to the training prior gains 0.00028 on the mean. Weights taken from a different fold give the same gain, so the stratified folds leak no usable test composition. The gain is calibration, which any deployed model can apply. The untuned baseline is already calibrated (gain 0.000002).
2. Sky neighbours and density. The data are a 1.5M-row sample of DR1's roughly 18.7M spectra, so neighbours are sparse: only 0.43% of rows have another row within 10 arcsec. Label agreement with the nearest row rises from the base rate of 0.60 to 0.96, but only for the 102 rows that have a partner within 1 arcsec. These are distinct blended objects in the same photometric system, not copies. kNN label and density features do not help either model, with or without the test rows.

Attacks that found nothing (numbers)
- Row order. Class shares in 10 consecutive blocks of 150k rows are flat (GALAXY 0.752 to 0.757). Next-row label agreement is 0.6007 against 0.6010 expected by chance. The test folds are spread evenly over row position.
- Exact copies. No duplicated (TARGET_RA, TARGET_DEC) pairs and no duplicated full feature rows. No duplicates on (FLUX_G, FLUX_R, FLUX_Z), on (FLUX_W1, FLUX_W2) or on (Gaia G, parallax). FLUX_R alone repeats for 33k rows: these are float32 coincidences, and their labels agree at about the base rate.
- Near copies. Only 102 rows have a partner within 1" and 306 within 2". These are different objects with different fluxes, never a north/south re-observation.
- Formats. With only format features (mantissa zeros, RA/Dec digits), log_loss is 0.709 against 0.719 for the prior. The small signal is RA magnitude, i.e. position. The feature set that reaches 0.249 also includes the Gaia NaN flags and zeros in SERSIC/SHAPE (PSF morphology), which are physics, not formats. FLUX_x is NaN exactly when FLUX_IVAR_x == 0, which the preparation probably introduced. It affects only 11 to 139 rows per band and carries the same information as ivar = 0.
- Columns from after the prediction point. On r0f0 with a 300k training subsample, the best single feature is PMDEC at 0.336, then Gaia G at 0.337, against 0.087 for the full model. No single column comes close. All columns are Legacy Surveys DR9 or Gaia DR2 imaging and astrometry, known when a target is selected.
- Transforms over all rows. Every column is in raw physical units, with no z-scored or min-max columns and no ranks.
- Test-set composition. The folds are random and stratified, so a train-versus-test classifier has nothing to find (class and PHOTSYS shares are identical across folds). Prior matching gains nothing beyond calibration (finding 1).
- Training rows from the future. Not applicable: the split is IID with no time column.
- Web. I found no competition, leak thread or "magic feature" for this dataset. DESI's documentation describes the "useful spectra" selection (ZCAT_PRIMARY, OBJTYPE=='TGT', ZWARN==0), and Redrock is sometimes overconfident (ZWARN=0 on wrong fits) and labels many backup-program stars as GALAXY. That is label noise shared by train and test, not an exploit.

Could not check
- Looking rows up in the public DESI DR1 zpix catalogue. The NOIRLab Data Lab query service refused anonymous queries, and the full catalogue is several GB. TARGET_RA/TARGET_DEC are kept at full float64 precision, so a lookup would very likely succeed (by the instructions, this is not a task flaw).
- Whether the rows were filtered to ZWARN==0 (outcome-dependent selection: failed spectra are absent from both train and test). This would make the task easier for everyone, not exploitable. A deployed model would face the failures too. The fact that decides it is the preparation's row filter.
- The DESI targeting bits (DESI_TARGET, BGS_TARGET, MWS_TARGET, SCND_TARGET) are known at the prediction point and are absent from the kit. Their absence costs honest models signal but is not a leak.

Sources: https://data.desi.lbl.gov/doc/releases/dr1/ ; https://data.desi.lbl.gov/doc/releases/dr1/known-issues ; https://arxiv.org/pdf/2505.17230 ; https://datalab.noirlab.edu/desi/

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

Verdict: 9 of 12 calls follow precedent. 3 depart without a written fact that sets them apart, one prompt each below:
  P1 the Redrock-only label (and the ZWARN 0 filter) is not named as a gap,
  P2 the Tractor morphology is kept on SEL-14's reason, and that reason would also have kept magic_gamma_telescope,
  P3 "better data for sdss_17" with both shipped, against the tension row of 2026-11-08.
No drift and no third exception. Of the register's flags, only USE-5 (opposite outcomes) touches this dataset, and
facts separate its pairs (below).

Read: principles.md (Consistent judgement, Exceptions and amendments, Tensions); use_case.md (USE-5 to USE-10 with
their Cases); selection.md (SEL-13 to SEL-15, Selection bias, Cases); leak_checks.md (LEAK-10, LEAK-22, Mechanisms);
provenance.md (PROV-4 to PROV-9); metrics.md (MET-8); the definition and README; the record; builder_report.md; the
panel reports so far (domain_practitioner, blind_reviewer, column_auditor) and the claim auditor's working logs
(t4_qsocat.log, t5_ablations.log; its report is not written yet); register.json (5,160 decisions,
34 flags); the records and definitions of sdss_17, magic_gamma_telescope, desi_bgs_photometric_redshift,
happy_teddy_sdss_photo_z, sarcoma, cns_tumor_methylation_classification, chicago_traffic_crashes, xente,
corporate_credit_rating, cesnet_os / kronodroid / ujiindoorloc_wifi.

Closest precedent: sdss_17 (Yes, TabArena v0.1; Selection Bias; CC 2026-10-01 Lennart: v2 definition, a photometric
task, `redshift` dropped as fitted with the class, `plate` and `fiber_ID` dropped as targeting ids, IID kept after a
plate-grouped test; Assessment 2026-10-21: fallback log_loss; CC 2026-10-31: cam_col a category). Its definition
ships the SDSS pipeline's class as the label, approximate fit, fit_reason naming the colour-cut targeting.

**PER DECISION**

1. Framing: all DESI targets, approximate fit, Selection Bias (builder's issue 1). CONSISTENT.
   - Follows sdss_17 (all targets of an imaging survey, classes from the spectrum, approximate, Selection Bias;
     2026-10-01). selection.md, "Selection bias", names sdss_17 as its example (Andrej, 2026-10-20). USE-8 (amended
     2026-10-27, Lennart) also holds: the use-case settings (choosing targets from the whole catalogue, flagging
     catalogue objects) do not share DESI's targeting cuts, so approximate, as for superconductivity and eryhemato.
   - What sets DESI apart from sdss_17: the target bits ship with the catalogue, so a quasar-targets-only version
     (1.9M objects, 70.5/25.3/4.1%) can be cut. sdss_17's Kaggle file had no such bits. This fact opens builder
     option b. It does not oblige it: USE-9 (Should) asks whether the data AS SHIPPED mirrors a direct use case, and
     a cut to 11% of the rows is a framing choice (Weigh), not USE-9's reading. chicago_traffic_crashes (2026-11-05)
     kept every row under a better actor rather than cutting to the direct subset. Keeping option b as a version
     follows both.
   - Option c (all targets with the targeting bits as inputs) departs from sdss_17's `plate`/`fiber_ID` drop
     (leak_checks Mechanisms row "Targeting or pointing ids ... drop them"; 2026-10-01). It would need a named actor
     who holds the bits, has no spectrum yet, and still decides on the class. The builder names none. As drafted it
     is a version at most. Flag it if the curator picks it.

2. Label: Redrock SPECTYPE without the visual-inspection or afterburner corrections (USE-5). KEEP CONSISTENT; NOT
   NAMING THE GAP DEPARTS WITHOUT A REASON -> P1.
   - Not a USE-5 failure by precedent. chicago_traffic_crashes (CC 2026-11-05, Lennart): "USE-5 fails only when the
     label is shown to be another quantity". corporate_credit_rating (2026-10-16): 17% of the checkable labels were
     another rating, retired. xente (2026-11-04): a 0 meant "not reviewed" as much as "not fraud", because a review
     step on a shipped input decided which rows got a label at all. Here the label is the same quantity (the
     spectroscopic class) with a published pipeline error. Measured against DESI's own DR1 QSO catalogue (Redrock +
     MgII + QuasarNET; claim auditor t4): 52,766 GALAXY and 532 STAR labels are catalogue quasars, 0.31% of the
     16,930,061 kept objects. 52,534 of them are quasar targets: 2.8% of the quasar targets and 10.9% of their GALAXY
     labels. The domain practitioner's VI-based order of magnitude is about 150k. No label goes missing by design, so
     the xente mechanism is absent. sdss_17 ships the SDSS pipeline's class the same way, so the keep follows it.
   - The departure is the silence. USE-5 as amended on diabetes_3 (2026-10-21) asks for "a note naming the gap".
     USE-8 counts a known label gap toward an approximate fit and names it in fit_reason
     (differentiated_thyroid_cancer_recurrence, 2026-10-21; blood_tests_drink_prediction). sarcoma's fit_reason
     names the excluded uncertain cases. This definition's fit_reason and notes say only "the class DESI's pipeline
     fit". The domain practitioner and the blind reviewer both raise this gap independently. sdss_17 is just as
     silent, but nobody raised the point there, so it sets no precedent on this fact.
   - The remedy ladder (repair > fix > note) puts relabelling from the source's own QSO catalogue above a note. The
     tension row "A better version against our own fix" limits that: a version the source defines replaces ours, a
     fix of our own invention does not. The catalogue covers only part of the non-quasar targets: 68,483 Redrock QSO
     labels are not in it, 67,627 of them outside the quasar targets. So "Redrock class unless the catalogue says
     QSO" would be a combined rule of ours, though DESI's clustering samples use it.

3. Row filter ZWARN 0 (builder's issue 3; does it select on the outcome? LEAK-22). CONSISTENT; ONE OMISSION, FOLDED
   INTO P1.
   - LEAK-22 says "follow the paper's cohort" (diabetes_130_us). The filter is the release's own "useful spectra"
     definition (DR1 page, footnote 1), and it reproduces the published counts exactly. sarcoma (2026-10-21) shipped
     the expert-confirmed cases only, uncertain ones left out, approximate.
   - What sets it apart from framingham_heart_study_fhs (2026-10-22: dropping competing deaths "selects the cohort on
     the future", so those rows stay with label No): a framingham death keeps a valid label, while a ZWARN spectrum
     has no reliable class to keep. The filter does rest on a post-spectrum quantity (unlike nyc_taxi/pkdd, "the cut
     rests on the inputs"), and it differs by class: 10.1% of galaxy, 4.0% of quasar and 1.6% of star spectra. The
     builder's probe-19 summary ("removed rows' class shares within 0.022") pools this filter with the
     photometry filter, which removes mostly stars, so the pooled shares hide the class dependence. The claim
     auditor's t4 counts 307,534 ZWARN-flagged quasar targets, 53,375 of them in DESI's QSO catalogue.
   - Omission: USE-8 (2026-10-27) says "Either way fit_reason names the selection", and sarcoma's fit_reason names its
     uncertain-case exclusion. Here the filter is only in curation_comments. Fold it into P1 option a.

4. Row filter: Legacy Surveys photometry required (USE-7). CONSISTENT.
   - USE-7 cases: bias_correction (days without the forecast dropped), nyc_taxi/pkdd (2026-10-26: "the cut rests on
     the inputs, not on the travel time"). PHOTSYS is an input-side fact known before the spectrum. The 98.3% star
     share of the dropped Gaia-only targets is a consequence, not the criterion.

5. LEAK-10: Z, ZERR, DELTACHI2 dropped. CONSISTENT. Same mechanism as sdss_17 `redshift` (Mechanisms row "Fitted from
   the same measurement that gives the label"; 2026-10-01). desi_bgs_photometric_redshift's screening drops the same
   spectral outputs.

6. LEAK-10: programme, target bits, PRIORITY_INIT, NUMOBS_INIT dropped. CONSISTENT. Same as sdss_17 `plate` and
   `fiber_ID` (row "Targeting or pointing ids (they encode pre-selection ...)": drop; 2026-10-01) and on the same
   reasoning ("a new object has no plate before it is targeted" / "the objects the use case classifies have none").
   The bits are worth more here (alone 0.164 against the 0.720 prior), which strengthens the case.

7. Tractor morphology and fibre fluxes kept (SEL-13 against SEL-14; builder's issue 2). DEPARTS FROM A PRECEDENT; THE
   STATED REASON DOES NOT SEPARATE IT -> P2.
   - The precedent: magic_gamma_telescope, `No` with `Image` (Lennart, TabArena v0.1 triage, record comment "Image
     Data"). selection.md also lists it under SEL-13 ("`magic_gamma_telescope` shower geometry"). Its Hillas
     parameters (length, width, size, concentration, asymmetry, alpha) are geometric descriptors fit to a camera
     image. The field's standard gamma/hadron classifier is a tabular model on them (MAGIC's random forest), so the
     builder's SEL-14 reason ("catalogue measurements that tabular classifiers of the field take as inputs") would
     have kept magic too. SEL-13 lists "morphological, geometric ... descriptors from an image-analysis pipeline",
     and MORPHTYPE, SHAPE_R, SHAPE_E1/E2 and SERSIC are that.
   - SEL-14's text covers a human reading ("the established clinical or operational result"; breast_cancer_prediction,
     heart_disease). Tractor's are automated fits. Keeping them under SEL-14 extends a Must's wording, and a Must
     takes no exceptions (principles.md), so it should be written down as a reading or an amendment, not left implicit.
   - The data separates the cases, but the definition does not say so. The image-model columns are 5 of 45 inputs
     (11 with the fibre fluxes, which are model-predicted fluxes). Dropping the five costs 0.0016 log loss (0.0866 to
     0.0882, claim auditor t5, 600k objects, 3 folds), and dropping them with the fibre fluxes costs 0.0115. In magic
     the descriptors are the whole table, and its rows are Monte Carlo simulated (a second reason, SEL-16). The bulk
     here is broadband flux, the kind sdss_17's magnitudes established as in scope, and SEL-15 reads it as a
     measurement through an imaging device. SEL-13's own clause ("descriptors stay image-derived when mixed with a few
     non-visual columns") is the opposite proportion.
   - Agreeing panel members: the column auditor (SEL-14 over SEL-13) and the domain practitioner (DESI's QSO cut
     requires MORPHTYPE PSF).

8. Split IID. CONSISTENT. sdss_17 kept IID after a plate-grouped test changed nothing (2026-10-01). Here HEALPix
   holdouts at nside 64 and 4 give 0.099 and 0.088 against 0.100 random, and the column auditor's no-position runs
   agree. The tension row "The right split against the score" (forest_fires) holds because the regime follows the use
   case (new objects in the same footprint), not the gap.

9. Metric: fallback log_loss (MET-8). CONSISTENT. sdss_17's fallback log_loss (Assessment 2026-10-21), on the same
   reason (a data release with no task or metric). Chaussidon et al.'s 310 per square degree cannot be computed on
   targets alone (domain practitioner), so MET-6/MET-7 do not engage. Tension row "The source's metric against a
   better metric": no source metric, no cost invented.

10. Year 2025 (PROV-9). CONSISTENT. The first publication is the public DR1 release with arXiv:2503.14745, both March
    2025. AJ 171, 285 (2026) is the "BibTeX year of a later citation" that PROV-9 excludes. sdss_17 likewise carries
    the DR17 release year (2021), not its 2022 ApJS paper.

11. Marker Selection Bias kept and fit approximate. CONSISTENT. See 1. The "No marker when" cases do not apply: the
    selection is not how the label comes to exist (SDSS and DESI both pick by colour), and it is not an oversample
    from the same population.

12. Uniqueness: "better data for sdss_17", both datasets ship (builder's checklist PROV-6; the curation_comments note).
    DEPARTS FROM THE TENSION ROW OF 2026-11-08 WITHOUT THE RECORDED REASON -> P3.
    - Tension row "Same task, another source" (Lennart, 2026-11-08): both enter when neither is better data (other
      years, labels, features or framings), with the reason recorded in each record. When one is better data (larger
      or newer, same target and features), it enters and the other stays `TBD -> Yes` for later (tls_os over
      cesnet_os, mh_1m over kronodroid, uji_long_term over ujiindoorloc). Read literally, the definition's own words
      "better data for sdss_17" call for sdss_17 to step back.
    - Facts that may set the pair apart, none of them written as the reason: (i) sdss_17 already ships (TabArena v0.1,
      BeyondArena, DF: Yes), while all three cases of the row were unshipped candidates. (ii) The features differ:
      SDSS has u and i, DESI lacks them and adds W1/W2, Gaia astrometry and morphology. (iii) The targeting rules
      differ, so the populations differ. Per the row, (ii) and (iii) make "neither is better data, both enter", and
      then the phrase "better data" is the error. The sdss_17 record carries only the AI's "better data" assessment
      (2026-10-31) and no reason.
    - desi_bgs_photometric_redshift (screening 2026-10-31, TBD -> 2nd Tier): a different task from the same survey
      (photo-z regression, PROV-7). Not affected here. Its own PROV-6 question against DR1 is its record's.

Drift and amendments:
- Lennart on targeting ids (sdss_17 2026-10-01; here), on Selection Bias with an approximate fit (sdss_17, the USE-8
  amendment of 2026-10-27, lt_vehicle 2026-11-05) and on USE-5 (corporate 10-16 exclude, diabetes_3 10-21 keep,
  xente 11-04 exclude, chicago 11-05 keep): the outcomes differ with the facts (another quantity / undocumented /
  label set by a review step / drift), not over time. No drift.
- SEL-14 would get its third application here (breast_cancer_prediction, heart_disease) and its first on automated
  fits. That is no third exception, but the wording no longer covers the case (P2 option d).

**REFLECTION PROMPTS (issue shape, for the review editor; one per departing decision)**

P1 (decision 2, with the omission of decision 3)

**Consistency check (AI, 2026-11-09):** Should the definition name the Redrock-only label and the ZWARN 0 filter as gaps, as diabetes_3, differentiated_thyroid_cancer_recurrence and sarcoma name theirs?

- **Problem:**
  - The label is the pipeline's class alone: 52,766 GALAXY and 532 STAR labels are quasars in DESI's own DR1 quasar catalogue (0.31% of the objects, 10.9% of the quasar targets' GALAXY labels), and neither the fit reason nor the notes say so.
  - The release's quality filter keeps only spectra whose class was settled (it drops 10.1% of galaxy, 4.0% of quasar and 1.6% of star spectra), and the fit reason names only the colour-cut targeting.
  - Earlier calls named such gaps: a label with an unverified definition, an excluded set of uncertain cases.
- **Consistency:** keeping the label follows sdss_17 and the reading of 2026-11-05 that a label fails only when it is shown to be another quantity[use5]; not naming it departs from the note the amendment of 2026-10-21 asks for[use5][use8].
- **Panel:** the domain practitioner (about 150k likely quasars labelled GALAXY, by visual inspection rates) and the blind reviewer raise the label independently; the claim auditor measured the catalogue overlap.
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Name both gaps | adds to the fit reason and the notes that the class is Redrock's alone (with the catalogue numbers) and that only settled spectra ship | follows diabetes_3, thyroid and sarcoma; no rebuild; the label stays the release's | the model still learns the pipeline's quasar misses as galaxies |
  | b | Relabel quasars from DESI's quasar catalogue, and name the filter | the class becomes QSO where the DR1 quasar catalogue lists the object | repair from the source's own product, ranked above a note[ladder]; the noise sits where models differ | the catalogue covers only part of the non-quasar targets (68,483 pipeline quasars are not in it), so the combined label is a rule of ours[tension]; sdss_17 would then be reopened for parity |
  | c | Leave as is (implemented) | the definition stays silent, as sdss_17 is | no change | an approximate fit with a known gap left unnamed |

- **Recommendation:** a; b only as a separate version if the curator wants the quasar-target framing, where the noise matters most.
- **Decision:** a, b or c?

[use5]: USE-5 (Must, amended 2026-10-21 on diabetes_3): a label whose construction cannot be checked "may ship with fit approximate and a note naming the gap"; "A label checked and found to be another quantity ... still fails". chicago_traffic_crashes, CC 2026-11-05 (Lennart): "USE-5 fails only when the label is shown to be another quantity".
[use8]: USE-8 (Must): an unverified label definition is a known gap and makes the fit approximate (differentiated_thyroid_cancer_recurrence, 2026-10-21); of a selection, "Either way fit_reason names the selection" (2026-10-27); sarcoma's fit_reason: "the review left out uncertain cases".
[ladder]: principles.md, "How to decide", 5: repair from the origin; fix the definition; keep with a note; exclude.
[tension]: principles.md, Tensions, "A better version against our own fix": a version the source defines replaces ours; a fix of our own invention does not (eryhemato).

P2 (decision 7)

**Consistency check (AI, 2026-11-09):** What sets the kept Tractor profile type, shape and Sersic index apart from magic_gamma_telescope's shower geometry, which was rejected as image data?

- **Problem:**
  - Both are geometric descriptors fit to an image, and the field's standard classifiers are tabular models on them in both cases.
  - The reason in the notes, that the field's tabular classifiers take them as inputs, would have kept magic_gamma_telescope too.
  - The rule that keeps such readings is worded for a human reading of an image, and these are automated fits.
- **Background:** the five columns are 5 of 45 inputs; without them LightGBM's log loss moves from 0.0866 to 0.0882, and to 0.0981 without the fibre fluxes too (600k objects, 3 folds); in magic the descriptors are the whole table, and its rows are simulated.
- **Consistency:** magic_gamma_telescope, `No` with `Image` (Lennart, TabArena v0.1), listed under the image rule[sel13]; breast_cancer_prediction and heart_disease kept human readings[sel14]; sdss_17 shipped catalogue magnitudes, measurements through an imaging device[sel15].
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep, and record the fact that sets it apart (implemented, without the fact) | writes in the notes and the record that the image-model columns are a small part of a catalogue of fluxes and carry 0.0016 of the log loss, unlike magic's all-descriptor, simulated table | follows the data; the task stands without them | a reading of a Must's wording that the next case will cite |
  | b | Drop the five profile columns | ships fluxes, fibre fluxes, Gaia and masks only | literal image rule; matches magic | drops inputs every catalogue classifier reads, DESI's own quasar cut among them |
  | c | Reopen magic_gamma_telescope to match | re-reviews magic under the same reading | like cases alike | magic is simulated, a reason of its own, so it would likely stay out |
  | d | Amend the rule that keeps readings | extends it to automated catalogue measurements that the field's tabular models use, with magic's proportion and simulation as the boundary | a deliberate rule for the next survey catalogue | a rule change on one case |

- **Recommendation:** a, with d if the curator expects more survey catalogues.
- **Decision:** a, b, c or d?

[sel13]: SEL-13 (Must): "morphological, geometric or spectral descriptors from an image-analysis pipeline" are a vision task; "descriptors ... stay image-derived when mixed with a few non-visual columns". selection.md, Patterns: "`magic_gamma_telescope` shower geometry".
[sel14]: SEL-14 (Must; narrows SEL-13): "when the human reading is the established clinical or operational result that tabular models are used on in practice, the task is tabular". principles.md, Tensions: "A real task against a scope pattern": the use case decides (Lennart, 2026-10-15).
[sel15]: SEL-15 (Must, amended 2026-10-21): a physical quantity measured through an imaging device and used by the field as the instrument's reading is a measurement; counter-cases satimage and wilt, which recognise image content.

P3 (decision 12)

**Consistency check (AI, 2026-11-09):** Do sdss_17 and this dataset both ship as the same task from two surveys, or does the "better data" call of 2026-11-08 move sdss_17 back to later?

- **Problem:**
  - The definition calls this dataset better data for sdss_17 and keeps sdss_17 shipped.
  - Under the call of 2026-11-08, better data enters and the other dataset stays for later; both enter only when neither is better, with the reason in each record.
  - Neither record states the reason.
- **Background:** the features differ (SDSS u and i; DESI two infrared bands, Gaia astrometry and morphology), the targeting rules differ, and sdss_17 already ships in TabArena v0.1, while the three earlier pairs were all unshipped candidates.
- **Consistency:** tls_os over cesnet_os, mh_1m over kronodroid, uji_long_term over ujiindoorloc (2026-11-08)[same].
- **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Both ship, as neither is better data (implemented, without the reason) | rewords "better data" to "the same task from another survey" and records the other bands, inputs and targeting in both records | matches the row's "other features or framings"; keeps a shipped dataset | two astronomy tasks of one kind in the benchmark |
  | b | This one enters, sdss_17 steps back | sets sdss_17 to later and removes it from the working copy | applies the row literally; the larger, newer data | retires a v0.1 dataset whose inputs DESI lacks (u, i) |
  | c | Amend the row | says how it treats a pair whose older member already ships | settles the next such pair | a rule change on one case |

- **Recommendation:** a.
- **Decision:** a, b or c?

[same]: principles.md, Tensions, "Same task, another source (P5 and P6; PROV-4, PROV-7)": "both enter when neither is better data (other years, labels, features or framings), the reason recorded in each record"; "when one is better data for the task (larger or newer with the same target and features), it enters and the other stays `TBD -> Yes` for later" (Lennart, 2026-11-08).

Record fields: none disagree (record `Website` counts as the schema's `Other`; year 2025, Random (IID) and Multiclass
Classification match).

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

Position: ship as defined, after changes that need no decision. Two known gaps go into fit_reason and the notes. The
overfit LightGBM numbers get replaced. Two stated reasons get rewritten. One cheap mask gets added. Every Must holds.
Each real problem the panel found (claim auditor F1, F2, F3; precedent checker P1, P2, P3; the column auditor's
CLEAN-10 gap) is resolved by the mildest remedy on the ladder that resolves it.

1. Honest evaluation holds: nothing shipped comes after the spectrum, and nothing can be gamed.
   (P4; LEAK-10 Must, LEAK-16 Must)
   Evidence:
   - The features are Legacy Surveys DR9 (released 2021-01-13) and Gaia DR2. Both predate the main survey's first
     spectrum (May 2021) (claim auditor I1, C14).
   - The column auditor checked all 136 header columns. The spectral fit is out: Z, ZERR, DELTACHI2, plus the
     never-read spectroscopic columns. So is the targeting decision: PROGRAM, the four target-bit columns,
     PRIORITY_INIT, NUMOBS_INIT. No imaging column of the catalogue is left out.
   - The task gamer ran six attacks. The largest gain, -0.0003, is calibration that a deployed model also has. The
     best single column scores 0.336, against 0.087 for the full model.
   - There are 0 exact copies (task gamer, blind reviewer, claim auditor t3). The blind reviewer, without our notes,
     found no leak.
   Why it decides: a real task can carry imperfect cleaning but not a leak (principles, How to decide 3). Four agents
   tested this independently and agree.

2. F1, the Redrock-only label. USE-5 holds; the gap must be named, and a note is the remedy that resolves it.
   (P3; USE-5 Must, USE-8 Must)
   Concede:
   - The label is Redrock's SPECTYPE without the afterburners, and neither fit_reason nor the notes say so.
   - Measured: 53,922 of the 1,900,008 quasar targets (2.84%) disagree with DESI's DR1 QSO catalogue. 52,534 of them
     ship as GALAXY, which is 10.9% of the quasar targets' GALAXY labels and 0.32% of all 16.93M rows.
   Why it does not fail USE-5:
   - USE-5 fails when a label is "checked and found to be another quantity" (diabetes_3, 2026-10-21). On
     chicago_traffic_crashes (CC 2026-11-05) the curator wrote "USE-5 fails only when the label is shown to be another
     quantity".
   - Here the label is the same quantity, the spectroscopic class, with a published pipeline error on 0.32% of rows.
     corporate_credit_rating failed with 17% of its labels another rating.
   - sdss_17 ships its own pipeline's class the same way.
   Mildest remedy:
   - Add to fit_reason and the notes: "the class is Redrock's alone; DESI's DR1 quasar catalogue, with the MgII and
     QuasarNET afterburners, calls 52,534 of the quasar targets' Redrock galaxies quasars".
   - Rules: USE-5 as amended asks for "a note naming the gap", and USE-8 counts an unsettled label as a known gap of an
     approximate fit. The fit is already approximate, so the verdict stays.
   Why not relabel (repair sits above a note on the ladder):
   - The catalogue's corrections fall almost only on quasar targets: 53,066 of the 53,298 relabels.
   - The catalogue leaves out 67,627 Redrock quasars outside the quasar targets.
   - So "Redrock unless the catalogue says QSO" would correct the label by a rule that follows the targeting bit we
     drop under LEAK-10. That is a fix of our own invention. The tension row "A better version against our own fix"
     says such a fix does not replace the source's class.
   - A quasar-target version with the catalogue label can come later (builder issue 1, option b).
   - The domain practitioner's figure of about 150k is an inference from visual-inspection rates on another sample.
     The measured join on the shipped rows outranks it (EV-2).

3. F3, the ZWARN 0 filter: it is the release's own cohort, the dropped rows have no label to keep, and fit_reason
   should name it. (P3; USE-8 Must; LEAK-22 Must, as the precedent checker reads it)
   Concede:
   - The filter acts unevenly by targeting class. It drops 20.6% of ELG targets and 13.9% of quasar targets, against
     about 2% of the others.
   - 53,375 of the 307,534 dropped quasar targets are quasars in DESI's QSO catalogue.
   - fit_reason names only the colour cuts.
   Why the rows stay out:
   - A ZWARN spectrum has no reliable class, so keeping these rows means shipping labels the source flags as failed.
   - The filter is the release's "useful spectra" definition (DR1 page, footnote 1). It reproduces the published
     18,659,804 = 13,049,402 + 1,553,713 + 4,056,689 exactly.
   - Precedents: sarcoma (2026-10-21) shipped only the expert-confirmed cases, approximate, with the exclusion named.
     framingham differs: there a competing death keeps a valid label.
   - The claim auditor agrees: "nothing in the code. Dropping unlabelled rows is the only option."
   Mildest remedy: one clause in fit_reason, as USE-8 asks ("Either way fit_reason names the selection"): only
   spectra whose class Redrock settled ship, and the filter drops 20.6% of ELG and 13.9% of quasar targets against
   about 2% of the others.
   The blind reviewer's concern 2 comes from the clean room, which has no notes. It said the cuts were undocumented
   and stars were about a quarter short of the published mix. The notes give the file, the four cuts and the counts.
   The star deficit is the Gaia-only drop: 1,212,422 rows, 98.3% stars (USE-7).

4. F2 and the split: the numbers were wrong, but the decisions they support are not. (P4; SPLIT-1, SPLIT-4; EV-1)
   Concede:
   - 400 trees at learning rate 0.1 with no early stopping overfit. Every LightGBM number in curation_comments and
     splits_comment is therefore off.
   - Photometry scores 0.0866, not 0.100. Adding the targeting columns gives 0.0860, not 0.087. The sky holdouts
     score 0.0866 / 0.0869 / 0.0877, not 0.100 / 0.099 / 0.088.
   Why nothing else changes:
   - The LEAK-10 drops rest on the mechanism, not on a gain: "fitted from the same measurement that gives the label"
     and "targeting ids that encode pre-selection".
   - The split follows the application (tension row "The right split against the score", forest_fires). Under
     SPLIT-4 the position is a feature every new object has, not an entity.
   - With a regularised model, random folds score 0.0848 and HEALPix nside-64 folds 0.0850 (split auditor). The
     position adds nothing in unseen patches (0.0876 without it, 0.0890 with it).
   - The shipped objects cover 13,733 deg2, nearly the whole footprint. Only a never-seen area of about 3,400 deg2 of
     deep equatorial sky costs about 0.04, and no cited use case asks for that.
   - sdss_17 kept IID after a plate-grouped test.
   The corrected numbers favour the framing as defined:
   - The targeting columns add 0.0006, not 0.013, so builder option c (ship the bits) loses its reason.
   - The within-tracer numbers (quasar targets 0.400 against 0.726) came from the same overfit model. Overfitting
     raises a log loss, so they likely understate the margin. They still need re-measuring (I4 is untested).
   Mildest remedy: re-run decisive_experiments.py with early stopping. Replace the numbers in curation_comments and
   splits_comment (the split auditor drafted the wording). No re-split.

5. Scope: the Tractor profile columns do not make this an image task. (P2; SEL-13 Must, SEL-14 Must, SEL-15 Must;
   P3 informs P2)
   Concede (precedent checker P2): the notes' reason, "tabular classifiers of the field take them as inputs", would
   also have kept magic_gamma_telescope. So it is not the fact that sets the cases apart.
   The fact that does:
   - SEL-13 catches image descriptors "mixed with a few non-visual columns". Here the proportion is the reverse.
   - Most of the 45 inputs are physical quantities measured through an imaging device and used as the instrument's
     reading (SEL-15, amended 2026-10-21; sdss_17's magnitudes): fluxes in five bands with their inverse variances,
     fibre fluxes, Gaia photometry and astrometry, masks and dust.
   - The five profile columns (MORPHTYPE, SHAPE_R, SHAPE_E1/E2, SERSIC) carry 0.0016 log loss (0.0866 -> 0.0882,
     claim auditor t5). Even without the fibre fluxes as well, the task scores 0.0981, against 0.719 for the prior.
   - magic is all descriptors, and simulated (SEL-16).
   - DESI's own quasar cut requires MORPHTYPE PSF (domain practitioner), so the use case decides (P3 informs P2,
     breast_cancer_prediction).
   Mildest remedy: replace the SEL-14 sentence in the notes with this fact (precedent checker option a). No data
   change and no amendment.

6. Value: worth benchmarking, with the fallback metric the actor would pick. (P6; TP-3 Must, TP-2 Should, MET-8)
   Evidence:
   - The model families spread in the task probes: LightGBM 0.089, random forest 0.103, linear 0.164, best single
     feature 0.380, dummy 0.719.
   - A stronger honest LightGBM beats the baseline by 0.0027 (0.0844 against 0.0871), against a noise spread of
     0.0001-0.0003 (task gamer).
   - The smallest class in a test fold has 17,841 rows.
   - TP-3: "If tuned methods spread, keep the dataset."
   - log_loss is the fallback sdss_17 uses, and the domain practitioner would pick it. No source fixes a threshold,
     so MET-6 and MET-7 do not apply.
   Answers:
   - The blind reviewer's "thin headroom": TP-2 says a small real signal is no reason to retire, and the metric is
     log loss, not accuracy.
   - The split auditor's note that 0.3% of the rows carry 22-35% of an unregularised model's loss: this is a
     difference in calibration between models, which the score should measure.

7. Uniqueness and cleaning: a wording fix and one cheap mask. (P5 PROV-6 and the tension row "Same task, another
   source"; P7 CLEAN-10 Should)
   - "Better data for sdss_17" is the wrong phrase, not the wrong call. The tension row lets both datasets enter when
     they differ in "features or framings", and these do. SDSS has u and i. DESI has W1, W2, Gaia astrometry and
     morphology, and other targeting cuts.
     Remedy: reword to "the same task from another survey" and record that reason in both records (precedent checker
     option a). sdss_17 keeps its verdict.
   - CLEAN-10: mask FIBERFLUX_b where FLUX_IVAR_b = 0 (21/11/138 shipped rows), and FIBERTOTFLUX_b where it is 0 in
     those rows. The fix is cheap and safe, and the measured score does not change (0.0857/0.0877/0.0871 against
     0.0857/0.0875/0.0873). Add notes on SERSIC = 0 for point sources and on the extreme negative WISE fluxes, kept as
     published (CLEAN-11).
   - Astrometry without a Gaia match: 17,006 objects, 1,529 shipped rows (0.10%), a weak question. The values were
     written before the observation, so there is no timing leak. Add a note now. If their origin is traced to the
     targeting route, blank them with one line in step 3.
   - Optional: reword the copies count as 5,211 pairs within 1 arcsec, not 1,872 objects in a grid cell. The
     conclusion holds.

Judgment record
Verdict: ship after changes (none needs a curator's decision).
Validity: SEL-13 not triggered (most inputs are measurements, SEL-15; the profile columns carry 0.0016), note
  rewritten; USE-5 holds (same quantity, 0.32% pipeline error), gap named; USE-7 holds; USE-8 approximate, fit_reason
  names the label gap and the ZWARN selection; LEAK-10 triggered, fixed; LEAK-16 holds; SPLIT-1/SPLIT-4 hold;
  PROV-6 holds (both enter, reworded).
Value: TP-3, the families spread, keep; MET-8 fallback log_loss.
Quality: CLEAN-10 fibre-flux mask applied; notes on SERSIC and the WISE outliers.
Evidence: decisive experiments re-run with early stopping (EV-1); numbers in the notes replaced.
For the curator: nothing required. Optional later version: the quasar-target framing with the catalogue label
  (builder issue 1, option b).

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09, to the critic's opening brief; the critic's new measurement is in the run's work files (label_noise_loss.log)

Critic 1, P2 SEL-13 against SEL-14: concede. We agree on the fact and the remedy: keep the columns, and replace the
notes' SEL-14 reason with the proportion. Most inputs are flux measurements (SEL-15). The five profile columns carry
0.0016, and magic is descriptors only and simulated. What follows: the keep rests on SEL-13 not being triggered by
its own proportion clause. It is not an exception to a Must, so no amendment is needed now. That stays optional, the
curator's call, as the critic says.

Critic 2, P3 USE-5, the label: concede the remedy. I dispute only how the numbers are compared.
- On its own numbers: rescoring the same predictions moves both models by about the same amount (-0.00434 and
  -0.00484). A shift that both models share does not change a ranking. So the 0.0043-0.0048 does not answer whether
  the benchmark mis-ranks models. The gap between the models does, and it moves from 0.0027 to 0.0032. The label
  error hides about 16% of the real difference (0.0005), and it costs the better model more. On the relabelled rows
  the strong model's mean loss is 2.05 against 1.81, and these rows hold 281 of the strong model's loss>5 rows
  against 23 of the baseline's. The ranking does not flip (0.0796 against 0.0828), but the noise shrinks the
  difference the benchmark exists to measure, and in the stratum (quasar targets, 51% of the loss) where models
  differ. Both models were trained on Redrock labels, so 16% is a bound, not the full effect.
- What follows: a note names that gap but does not fix it. The remedy ladder takes the mildest remedy that resolves
  the problem, so the note is no longer enough. Repair from the source's own catalogue resolves it at little cost:
  one 816 MB file from the same CC BY 4.0 release, and a TARGETID join. I withdraw my opening point 2's "why not
  relabel". The repair keeps the dataset. It is a target redefinition, so it is the curator's call, with the note
  as the floor.
- Does "only upgrades labels within the cohort" answer my targeting-bit point? Not as worded. The upgrades still fall
  almost only on quasar targets: 53,066 of the 53,298 in all kept rows, and the shipped catalogue quasars labelled
  GALAXY or STAR sit mostly among quasar targets (4,738 of 4,764 shipped relabels). So the label's correction rate
  still follows a column we drop. But it answers the substance, and my point falls:
  - An upgrade moves a label toward the class the actor acts on (the catalogue is about 99% pure in visual
    inspection) and never away from it.
  - Every other stratum keeps today's Redrock label: no worse, and no new shortcut beyond what the photometry already
    carries about the targeting class.
  - The rule is DESI's own quasar sample for the stratum the catalogue covers, so it is "a version the source
    defines" (tension row, eryhemato), not a fix of ours.
  - One residual to write down: under "only upgrades", the 856 kept quasar targets the catalogue rejects (77 shipped
    rows) stay QSO, a small departure from the catalogue. Name it in the notes. Do not re-admit ZWARN != 0 rows.

Critic 3, P3 USE-8: concede. This is my opening point 3: the ZWARN clause and, if the repair is declined, the label
clause go in fit_reason. The probe-19 line is in the builder's report and draft issue, not in the definition. Replace
it there with the per-step class shares. The optional faint-third sizing (0.48 against 0.18) can go in, but with the
split auditor's caveat: it is confounded with the class and programme mix.

Critic 4, P4 Gaia astrometry without a Gaia match: concede. Same remedy as my point 7: trace the origin; blank the
values if it is the targeting route, otherwise add one sentence. At most 0.10% of rows, weak.

Critic 5, P5 wording: concede. Same remedy as my point 7. The alternative of amending the row is not needed: the
features differ, so the row's "both enter" branch applies as written.

Critic 6, EV-1, the overfit numbers: concede. This is my opening point 4. New fact in the dataset's favour: on the
shipped splits the untuned kit LightGBM scores 0.399 on quasar targets, against 0.726 for their class shares. So the
non-triviality claim (TP-4) now rests on a sound model.

Critic 7, P7 CLEAN-10: concede the fibre-flux mask (my point 7). SERSIC = 0 for PSF: both options lose nothing,
because MORPHTYPE carries it. Making it missing fits CLEAN-10, so I do not oppose it.

Updated judgment record (advocate)
Verdict: ship after changes.
Validity: SEL-13 not triggered (note rewritten); USE-5 holds, label repaired from DESI's DR1 QSO catalogue (only
  upgrades; the curator's call, with the note as the floor); USE-8 approximate, fit_reason names the ZWARN selection
  and whichever label is shipped; LEAK-10 fixed, the astrometry question traced; SPLIT-1/SPLIT-4 hold; PROV-6
  reworded.
Value: TP-3 and TP-4 hold (0.399 against 0.726 within quasar targets, sound model).
Quality: CLEAN-10 masks. Evidence: numbers re-run with early stopping (EV-1).
For the curator: point 2, repair the label (the critic and I now both prefer it) or keep Redrock's class with the note.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

Verdict asked for: ship only after changes. Nothing here is a Must that cannot be fixed, so I do not ask for
exclusion. The changes: repair the label from DESI's own quasar catalogue (or, at the least, name the gap), name the
ZWARN selection in fit_reason, replace the overfit numbers, and fix four write-ups and one cheap cleaning gap.

Read: dataset.py, README.md, the record (CC 2026-11-08), builder_report.md, principles.md, use_case.md (USE-5, USE-8),
selection.md (SEL-13 to SEL-15), leak_checks.md (LEAK-10, LEAK-22), evidence.md (EV-1 to EV-3), the seven phase-A
reports. One new measurement of my own (point 2): the run's work files: label_noise_loss.py and .log. It joins the shipped
1.5M rows to TARGETID by (TARGET_RA, TARGET_DEC): 1,500,000 matched, 0 duplicate matches, labels 100% equal. It then
joins the DR1 QSO catalogue the claim auditor downloaded and rescores the task gamer's out-of-fold predictions
(oof_baseline: untuned LightGBM, 0.08713; oof_strong: 0.08444; the shipped splits).

Points in rank order (principles.md: P2 before P3 before P4 before P5; procedure; P7 last).

1. P2, SEL-13 against SEL-14 (both Must). The Tractor morphology is kept for a reason that would have kept
   magic_gamma_telescope.
   Problem: the notes keep MORPHTYPE, SHAPE_R, SHAPE_E1/E2 and SERSIC "so SEL-14 keeps them", on the grounds that the
   field's tabular classifiers take them as inputs. SEL-14 is worded for a human reading ("the established clinical or
   operational result"). These are automated geometric fits to images, which SEL-13 names word for word
   ("morphological, geometric ... descriptors from an image-analysis pipeline"). magic_gamma_telescope is `No` with
   `Image` and listed under SEL-13 (selection.md:222), yet its Hillas parameters also feed the field's standard
   tabular classifier. A Must takes no exceptions (principles.md), so a keep on a reason that does not separate the
   case stretches the rule silently. The next survey catalogue will cite it.
   Effect on the task: small. The five columns are 5 of 45 inputs. Without them log loss goes from 0.0866 to 0.0882,
   and to 0.0981 without the fibre fluxes too (claim auditor t5). The scope verdict probably holds, but on the wrong
   rule.
   Remedy (fix the definition's text, no data change): keep the columns and write down the fact that sets the case
   apart. The table is mostly flux measurements through an imaging device (SEL-15), with a few image-model columns
   that carry 0.0016 of the log loss. SEL-13's own clause covers the opposite proportion (descriptors with "a few
   non-visual columns"), and magic's table is descriptors only, and simulated (SEL-16). If the curator expects more
   survey catalogues, an amendment of SEL-14 (precedent checker P2, option d).

2. P3, USE-5 (Must), and the tension row "The real-world target against a convenient label". The label is
   Redrock's raw class, not DESI's quasar classification, and the error sits where the benchmark separates models.
   Problem: SPECTYPE is the Redrock template class. DESI's own DR1 QSO catalogue adds the MgII and QuasarNET
   afterburners. DESI's quasar science and its target-selection validation use that catalogue as the quasar class,
   and USE-5 says to predict what the actor acts on. In Survey Validation visual inspection, Redrock alone recovers
   about 86% of quasars and Redrock with the afterburners about 94% (arXiv 2208.08517; domain practitioner, claim
   auditor). The blind reviewer also raised it without knowing the source.
   Evidence (measurements on the source's files):
   - Claim auditor t4: 53,922 of the 1,900,008 kept quasar targets disagree with the catalogue (2.84%). 52,534 of the
     481,259 GALAXY labels among quasar targets (10.9%) are catalogue quasars.
   - Mine, on the shipped 1.5M rows: 4,764 rows (0.32%) are catalogue quasars shipped as GALAXY (4,719) or STAR (45).
     The photometry model already calls most of them quasars: argmax QSO for 83.1% (untuned) and 76.0% (strong), mean
     P(QSO) 0.71 and 0.70. These 0.32% of rows carry 6.6% (untuned) and 7.7% (strong) of the total log loss, and 8.9%
     and 8.7% of all misclassifications.
   - The same predictions scored with the catalogue's class: 0.08713 -> 0.08280 (-0.0043) for the untuned model and
     0.08444 -> 0.07960 (-0.0048) for the strong one. The whole gap between the untuned and the strong model is
     0.0027 (0.0032 under the catalogue's class). The label error moves the score by more than the model difference
     the benchmark is there to measure, and it penalises the better model more: the strong model's mean loss on these
     rows is 2.05 against 1.81.
   - The quasar targets are 11.2% of rows and carry 51% of the loss. That is the stratum where models differ, and
     where the label noise sits.
   Caveats: the models were trained on Redrock labels, so this rescoring only bounds the effect. The catalogue is
   about 99% pure in visual inspection, not perfect. This is no USE-5 failure by precedent: it is the same quantity
   with a published pipeline error (chicago_traffic_crashes, 2026-11-05), so exclusion is not asked for.
   Remedy (repair from the origin, which ranks above a note; principles.md, remedy ladder): within the shipped cohort,
   the class is QSO where the object's main-survey row is in DESI's DR1 QSO catalogue, and Redrock's class otherwise.
   This is one 816 MB file and a TARGETID join (keep TARGETID until the join). It is DESI's own rule for its quasar
   sample (Redrock plus the afterburners), so it is "a version the source defines" (tension row, eryhemato), not a
   fix of ours. It only upgrades labels, so the 68,483 Redrock quasars outside the catalogue keep their class.
   Re-admit no ZWARN != 0 rows: that would select rows by their label. If the curator declines the repair, the floor
   is point 3's note.

3. P3, USE-8 (Must). fit_reason names neither known gap: the label, and the ZWARN filter's selection by class.
   Problem: USE-8 asks that an approximate fit name its known gaps, and of a selection that "fit_reason names the
   selection" (2026-10-27). fit_reason names only the colour-cut targeting. The ZWARN==0 "useful spectra" filter is
   the release's cohort, so LEAK-22 holds and no row changes. But it drops 20.6% of emission-line-galaxy targets and
   13.9% of quasar targets, against about 2% of the bright-galaxy, red-galaxy and Milky Way targets (claim auditor
   C8). 53,375 of the 307,534 dropped quasar targets are catalogue quasars (t4). The shipped objects are the ones
   whose spectrum settled the class, and a deployed classifier meets the others too. The builder's probe-19 line
   ("removed rows' class shares within 0.022") is not evidence about the filters: its removed set is mostly rows the
   sub-sampling dropped (claim auditor B1; precedent checker 3).
   Precedents: diabetes_3 (the note USE-5 asks for), differentiated_thyroid_cancer_recurrence, sarcoma (its
   fit_reason names the excluded uncertain cases).
   Remedy (a note): add to fit_reason and curation_comments (a) the label clause, if point 2 is not taken, with the
   numbers above, and (b) the ZWARN clause, with the per-class drop rates. Replace the probe-19 citation with the
   per-step class shares. Optionally size the selection gap: trained on the brighter two thirds, the faintest third
   scores 0.48 against 0.18 under random folds (split auditor 6).

4. P4, LEAK-10 (pre-selection clause), weak. Gaia astrometry on objects without a Gaia match, from an unnamed source.
   Problem: 17,006 kept objects (1,529 shipped rows) have PMRA, PMDEC and PARALLAX filled while their Gaia magnitudes
   are 0 and REF_CAT is none or SGA. In DR9 the Gaia columns come with a G2 reference, so these values come from
   another route the definition does not name. Of these rows 59% are stars, against 0.9% of the other rows without
   Gaia; 86% are in the bright programme and 90% are BGS targets (column auditor 1). If the values come from the
   targeting step, the use case's catalogue object would not have them.
   Effect: at most 0.10% of rows. No separate gain measured.
   Remedy: trace the origin in the desitarget / fiberassign data model. If it is the targeting route, blank
   PMRA/PMDEC/PARALLAX where REF_CAT is not Gaia (one line in step 3). Otherwise add one sentence to the Gaia bullet.

5. P5, PROV-4/PROV-7, the tension row "Same task, another source" (Lennart, 2026-11-08). The notes call this
   dataset "better data for sdss_17" and ship both.
   Problem: under the row, the better data enters and the other dataset stays `TBD -> Yes`. Both enter only when
   neither is better data, "the reason recorded in each record". The definition says "better data" and records no
   reason, and sdss_17's record carries only the AI's "better data" assessment (precedent checker 12).
   Remedy (wording): say "the same task from another survey", with the reason (SDSS has u and i; DESI has W1/W2, Gaia
   astrometry and morphology; the targeting rules differ), in both records. Or, as the curator's call, amend the row
   for pairs whose older member already ships.

6. Procedure, EV-1 (Must). The notes and the splits_comment report numbers from an overfit model, and one of them
   feeds a curator option.
   Problem: every LightGBM number in curation_comments and splits_comment comes from 400 trees at learning rate 0.1
   with no early stopping. With early stopping: photometry 0.0866, not 0.100. Adding the targeting columns gives
   0.0860, so a gain of 0.0006, not "0.100 -> 0.087" (about 20 times less). Sky holdout: random 0.0866, 215 deg2 pixels
   0.0869, 3,400 deg2 regions 0.0877 (claim auditor F2, C13, C26). Under a regularised model random and sky-grouped
   folds agree to 0.0002 (0.0848 / 0.0850), and the builder's settings spread 0.091-0.106 over seeds alone (split
   auditor 2). The splits_comment's "0.088 with pixels of 215 square degrees" reads as if holding out sky made the
   task easier. Builder's draft issue 1 option c cites the 0.100 -> 0.087 gain as a reason, so the curator would be
   weighing an artefact.
   Effect: no decision changes (LEAK-10 needs no gain, SPLIT-4 no gap). The task's non-triviality (TP-4) also
   survives on a sound model: on the shipped splits the untuned kit LightGBM scores 0.399 on quasar targets, against
   0.726 for their class shares (my run).
   Remedy: re-run decisive_experiments.py with early stopping, and replace the numbers in curation_comments,
   splits_comment and draft issue 1. The corrected values are above.

7. P7, CLEAN-10 (Should). The fibre fluxes of an unmeasured band stay 0 while the band's flux is set missing.
   Problem: step 3 masks FLUX_b where FLUX_IVAR_b == 0 but leaves FIBERFLUX_b at 0 in those rows: 21 of 21 (g), 11 of
   11 (r) and 138 of 139 (z) shipped rows. FIBERTOTFLUX_b is also 0 in 13/5/123 of them. SERSIC = 0 for the 488,603
   PSF rows is a placeholder too (column auditor 2, 4).
   Effect: none on the score (measured 0.0857/0.0877/0.0871 against 0.0857/0.0875/0.0873). A quality point, no reason
   to hold the dataset.
   Remedy (cheap and safe): in step 3, mask FIBERFLUX_b where FLUX_IVAR_b == 0, and FIBERTOTFLUX_b where it is 0 in
   those rows. Add a clause to the missing-values bullet. SERSIC: set it missing for PSF/DUP, or add one sentence.

Judgment record (critic's side)
Verdict: ship after changes.
Validity: SEL-13/SEL-14 holds on a reason that needs writing down (1); USE-5 triggered, repair from DESI's QSO catalogue
(2); USE-8 gaps unnamed, fixed by a note (3); LEAK-10 weak question on 1,529 rows (4); PROV tension row wording (5).
Value: TP-4 holds (0.399 vs 0.726 within quasar targets); the label error (point 2) is larger than the gap between
the untuned and the strong model.
Procedure: EV-1, the overfit numbers replaced (6).
Quality: CLEAN-10, cheap fix (7).
For the curator: point 2 is the weighing call. Repair the label (preferred), or keep Redrock's class with the note.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: desi_dr1_star_galaxy_quasar (folder desi_dr1_star_galaxy_quasar_1m), 2026-11-09

The advocate's brief agrees with mine on six of its seven points. The real dispute is point 2: whether a note is
enough for the label. One check is new, made for this rebuttal to answer the advocate's targeting-bit argument:
the run's work files: relabel_asymmetry.py and .log, on the same out-of-fold predictions as before.

1. Honest evaluation (LEAK-10, LEAK-16). CONCEDE. Four agents tested it and found nothing. The Gaia astrometry on
   objects without a Gaia match (my point 4) is a weak question, and the advocate's point 7 accepts my remedy: a note
   now, and blank the values if their origin traces to the targeting route.

2. The Redrock-only label. DISPUTE. I still ask for the repair. The curator should decide it, not find it marked
   "nothing required".
   What I concede:
   - The counts hold: 53,066 of the 53,298 relabels fall on quasar targets, and the catalogue gives no afterburner
     correction outside them. So the repaired label would be more complete inside the quasar targets than outside.
   - That makes the label a combination: DESI's catalogue class where it exists, Redrock's otherwise.
   Why that does not make it "a fix of our own invention":
   - (a) LEAK-10 governs features: "a feature holds only what existed at the prediction point". The target bit stays
     out of the inputs either way. Which spectra DESI ran its afterburners on is part of how the source built its
     label. It is not an input the model sees.
   - (b) Every repaired row takes a class DESI itself published for that object. Nothing is inferred by us. It is
     DESI's rule for its own quasar sample (Redrock QSO plus QuasarNET and MgII).
   - (c) The repair is one-way. It upgrades 4,764 shipped rows to the source's own better class and makes no row's
     label worse. The part it leaves uncorrected is the same as today, not new error.
   The remainder outside the quasar targets is small (new check):
   - Among the 1,088,303 shipped GALAXY rows outside quasar targets, the models give P(QSO) > 0.9 to only 121
     (untuned) and 231 (strong), and 10 and 21 of those are point sources.
   - Within the quasar targets, the repair fixes 1,146 and 1,658 rows at the same confidence.
   - The catalogue is also no echo of the photometry. It leaves 9,648-10,636 quasar-target GALAXY rows that the
     model calls QSO at P > 0.5 alone. It follows the spectrum's afterburners, not the colours.
   - So the asymmetry the advocate raises is an order of magnitude smaller than the error the repair removes.
   USE-5 and the note:
   - The amended note clause of USE-5 covers a label whose construction "is undocumented ... and cannot be checked".
     This label was checked (claim auditor t4), and the source publishes the correction.
   - The clause that applies is USE-5's first: "A target the source defined badly can often be redefined into the
     real one." The remedy ladder puts repair above a note (principles.md, How to decide 5).
   - The chicago_traffic_crashes reading decides that USE-5 does not fail. That is why I do not ask for exclusion. It
     does not decide that a note is enough when the source publishes the repair.
   - The advocate's brief does not answer my measurement. On the shipped splits the label error moves log loss by
     0.0043-0.0048. The whole gap between the untuned and the strong model is 0.0027. The error also hits the better
     model harder (mean loss 2.05 against 1.81 on these rows). A note names that distortion but leaves the ranking it
     produces in place.
   sdss_17:
   - Like cases are treated alike only when the facts are the same (principles.md, Conflicts).
   - sdss_17's label question was never raised or tested (precedent checker 2: "sets no precedent on this fact"), and
     no DESI-style correction catalogue was joined to it.
   - If the repair is taken, sdss_17 is the one to reopen for parity, as the precedent checker notes. It is not a
     reason to keep the known error here.
   What I ask:
   - Repair as in my point 2, with a note that the afterburner correction covers DESI's quasar targets only.
   - If the curator prefers a single-source label, keep Redrock's class with the note. That is a curator's weighing
     call, and I ask that it be put to the curator.

3. The ZWARN filter (USE-8, LEAK-22). CONCEDE. The rows stay out, with a clause in fit_reason. One condition holds for
   my point 2: the repair must not re-admit ZWARN != 0 rows the catalogue calls quasars (53,375), since that would
   select rows by their label.

4. F2 and the split (EV-1, SPLIT-4). CONCEDE, with two corrections.
   - The advocate's remedy leaves out builder draft issue 1 (option c cites the false 0.100 -> 0.087 gain). It should
     be corrected too.
   - I4 is no longer untested. On the shipped splits the untuned kit LightGBM scores 0.399 on quasar targets against
     0.726 for their class shares (my opening, point 6). The notes can cite that.

5. Scope (SEL-13, SEL-14, SEL-15). CONCEDE. The fact the advocate writes down is the one I asked for: most inputs are
   measurements (SEL-15), the profile columns carry 0.0016, and magic is all descriptors and simulated. Option a, no
   amendment needed.

6. Value (TP-3, MET-8). CONCEDE the verdict: the model families spread and log_loss is right. DISPUTE one reading.
   The advocate reads the heavy tail of the loss as "a difference in calibration between models, which the score
   should measure". Part of it is label error:
   - Catalogue quasars shipped as GALAXY or STAR are 0.32% of rows. They are 10.9% of the strong model's top-1% loss
     rows, about 34 times their base rate.
   - They carry 7.7% of its total loss.
   - The model comparison the advocate cites as proof of value (0.0027) is the one the label error shrinks by about
     16% (0.0032 under the catalogue's class).
   This supports point 2. It is not a reason against value.

7. Uniqueness and cleaning (PROV tension row, CLEAN-10). CONCEDE. The rewording "the same task from another survey",
   with the reason in both records; the fibre-flux mask; and notes on SERSIC and the WISE outliers.

Judgment record (critic, after the rebuttal)
Verdict: ship after changes.
Agreed with the advocate: the points 1 and 3 to 7 remedies (notes, the corrected numbers including draft issue 1, the
SEL-15 fact, the PROV rewording, the CLEAN-10 mask).
Disputed: point 2. Repair from DESI's QSO catalogue (USE-5's redefinition clause; the remedy ladder; the label error
is 0.0043-0.0048 against a model gap of 0.0027) against a note only (USE-5 holds; the label is uneven by targeting
class). The curator's weighing call.

</details>
