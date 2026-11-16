# wioa_employment_after_exit

**Outcome:** added. The AI recommends shipping it: the review panel's changes are made. Changed since the panel's draft
(`wioa_employment_after_exit_1m`, all programmes, a 1M-row sample): the folder is now `wioa_employment_after_exit`, with
Title I exits only and every row; the test windows moved back one quarter, to April to December 2024, so January to
March 2025 is out (Texas's incomplete wages, and DOL's first-report labels); `previous_known_outcome` added; race,
Hispanic ethnicity and sex dropped; American Samoa and Palau dropped; the use case lost its cohort-rate clause. The
dataset: 1,023,443 exits of 2022 to 2024 from WIOA Title I adult, dislocated-worker and Dislocated Worker Grant
services, 162 features, three quarterly test windows (April to December 2024) behind a 9-month gap, fallback `roc_auc`.
The task: at a participant's last planned service, will the person be employed in the second quarter after the exit
quarter, so that a case manager or local board can decide whom to keep in services or offer follow-up. Two calls are
left to you: issue 1 confirms that age and disability leave with the items that reveal them (implemented, recommended,
to decide after rais_employment_separation_1m issue 1); issue 2 asks whether the occupation, industry and CIP codes stay
codes or are decoded, alike with rais and sinan.
Verdict: ship after changes (made).
Validity: SEL-1 triggered: race, Hispanic ethnicity and sex dropped (29 CFR 38.6(b), UIPL 41-94; settled); age and
disability dropped with pregnancy, limited English and the youth, VR&E and ESL items that reveal a ground (issue 1,
option A implemented). USE-1 and USE-5 triggered, fixed: Title I exits only, the population whose follow-up WIOA defines
(20 CFR 678.430(c)), one actor and one decision (the cohort-rate clause removed). USE-10 triggered, fixed:
`previous_known_outcome` added, built only from exits at least four quarters back (the code raises if a test row reads
its gap). LEAK-24 triggered twice (Texas's incomplete 2025Q3 wages, strong; the newest quarter's first-report labels),
fixed by moving the test windows back one quarter: January to March 2025 leaves the frame and the newest window is at
its second report. LEAK-39 and LEAK-25 fixed for American Samoa and Palau (dropped); the 1,117 invalid-SSN exits the
label-free rule locates are a mix (0.21 employed) and stay under LEAK-25's 2026-11-02 amendment, with New York's group
noted. LEAK-10 holds after the PIRL 304 mask (1410 and 2516 masked too). SPLIT-9 holds; SPLIT-10 met (the gap now rests
on the state's own wage records, whose one-month reporting lag is an inference, not read in a source); SPLIT-14 holds
(train sides 53.0%, 61.2% and 68.7% of the frame).
Value: TP-2 holds: untuned LightGBM 0.732 ROC AUC (the task probe's model; the mediator's larger model, trained on every
Title I exit before the gap, scores 0.75 to 0.76 in issue 1) against linear 0.716, random forest 0.712, the best single
feature 0.652 and the dummy 0.5, better than the dummy on 3 of 3 windows, no task-probe flag; no leak probe flags a
column (all features 0.710, no single drop moves it by more than 0.003; exact feature copies across the split 0.0% with
the dates). MET-1 and MET-8: `roc_auc` scores the ranking a follow-up list needs; no source fixes a share, a capacity or
a cost.
Quality: CLEAN-10 (codes that only mean unknown, in 7 items with no other blank, set to missing), CLEAN-11 (the tenure
fill), CLEAN-14 (delivery mode ordered) and CLEAN-5 (calculated items that recode one kept item dropped) fixed; CLEAN-12
open (issue 2); SPLIT-20 notes on the release codings, the one-day closures and Montana's blank wages.
Weighed (priority 3): gap 0 (the mediator had +; social science is not thin among the 151 accepted definitions), use
case 0 (the mediator had +; the per-person follow-up decision is ours, fit approximate), source + (DOL's documented file
with SPRA's record layout), shape + (1.0M exits, 162 features of mixed types, temporal), risk 0 (no leak left open; the
issues are an ethics reading and the codes).
For the curator: the bundle check's two warnings are proposed for acceptance (not written into
`accepted_check_warnings`), and your ship verdict accepts them: `dataset_constant_column`,
"pirl913_indian_native_american_programs is 1 or blank: the layout has no code for not served, so the blank is the other
level (217 of 1,023,443 exits)"; `splits_rows_unused`, "By design: the 77,215 exits of January to March 2024 lie in the
9-month gap of every window (the newest window trains on exits to December 2023) and before the oldest test window."

**Main points:** Issue 1: keep age, disability and the items that reveal them out (implemented, recommended; decide
after rais_employment_separation_1m issue 1). Issue 2: codes, or "words [code]" (recommended), with the same letter as
rais issue 5 and sinan issue 4. Your verdict also accepts the two proposed warnings.

**Record fields that disagree with the definition:**

- `year`: record `(none)`, definition `2026`.
- `required_split`: record `(none)`, definition `Temporal (NON-IID)`.
- `tag`: record `(none)`, definition `Non-IID (Temporal)`.

**Record judgment:** valid. The US Department of Labor's own administrative records, with SPRA's record layout, its
cleaning appendices and DOL's disclaimer; the screening's risks were each met (the post-exit items dropped, the
outcome's maturity handled by the choice of files and windows, disclosure control kept with notes, the population
decided). Two readings of the screening are superseded: the population is the Title I exits only (the use case's
follow-up decision exists only for them), and the prediction point is the last planned service, so the service items
count as inputs, not only the 63 entry items. The size check's bound holds: at most 410,644 Title I exits a program
year, 1,023,443 over three years.

**Issues for Lennart:**

1. **Keep age and disability, and the items that reveal them, out of the features, as now?**

   * **Problem:**
     - The actor, a WIOA recipient, may not give a different service on the basis of age or disability, and DOL bars
       both from its own per-person model that allocates reemployment services, so the definition now drops them with
       every item that states or reveals one[^c38][^uipl][^sel1].
     - WIOA also names older individuals and individuals with disabilities as barrier groups the system is to serve, and
       the regulation does not say whether a score that directs more help by these grounds is barred, so this is a
       reading of the law and an extension of your stance on factors the actor may not use, both yours[^wioa][^row].
     - Pregnancy (PIRL 701) and limited English (803) have the same two-sided status, and the youth, VR&E and ESL items
       reveal a ground through the programme or service, so one reading decides them all.
   * **Background:**
     - PIRL and CALC numbers are items of DOL's record layout; VR&E is the VA's Veteran Readiness and Employment
       programme; ESL is English as a second language; DWG is a Dislocated Worker Grant.
     - Dropped as implemented: age (CALC 4039); disability (PIRL 202, 204-209, 939, 940, CALC 4021-4029); the items that
       reveal disability (303 disabled veteran, 602 SSI or SSDI, 917 vocational rehabilitation, the VA VR&E referrals
       1006, 1115 and 3007); pregnant or parenting youth (701); English learner (803) and ESL services (1207); the youth
       funding, status, programme and service items (CALC 4003, PIRL 702, 704, 905, 906, 911, 919, 1402-1416; 12,604
       exits had youth funding or a youth service).
     - Four codes of kept items are merged into a neighbour: other programmes for people with disabilities (922 code 2)
       into other programmes, wounded, ill or injured (1114 code 3) into "Other", and the WIOA Youth work experiences
       (1205 codes 1 and 5) into their general codes; 1,606 exits in all.
     - Kept under every option: ex-offender status (801, 2413, 2414), single parent (806), displaced homemaker (807) and
       cultural barriers (805), WIOA barrier groups that are no ground of the regulation; dropped under every option:
       race, Hispanic ethnicity and sex, which have no barrier-group role and cost nothing measurable.
     - Follow-up eligibility names neither ground (adult and dislocated-worker participants placed in a job), and a
       state gives the barrier groups priority by policy, not through a score[^fu].
   * **Effect on the task:** ROC AUC falls by 0.009 to 0.011 on the Title I exits, mostly age. With the grounds, people
     aged 55 and over make up 32% to 35% of a board's lowest-scored 20% of closures (those a follow-up list would reach
     first) against 16% to 17% of the exits; without them 19% to 21%.
   * **Experiments:**
     - Mediator, untuned LightGBM (400 trees, 127 leaves) trained on every Title I exit before the gap, on the three
       windows as shipped before the shift (January to March 2025, October to December and July to September 2024):
       0.7605, 0.7594 and 0.7577 with age and disability; 0.7498, 0.7482 and 0.7487 without them and their proxies.
     - Domain practitioner, three windows: 74% to 76% of a board's lowest-scored 20% is the same with and without the
       grounds; dropping the disability proxies on top changes ROC AUC by -0.0002 to +0.0003.
     - The cost of the youth, VR&E and ESL items was not measured; each group touches at most 1.2% of the exits.
   * **Consistency:**
     - rais_employment_separation_1m issue 1 (pending; drop the five grounds Brazilian law bars an employer from using,
       and extend the stance) extends your stance to any decision on a person where the actor's own law bars the factor,
       and drops age there; decide this issue after it: rais A leads to A or B here, rais B leaves age to this issue
       (where DOL's own ban in its profiling model is a fact for dropping it anyway), rais C leads to C.
     - acs_food_stamps_2014_2024_1m keeps age and disability because SNAP's own eligibility rules use them; follow-up
       eligibility names neither, which sets this case apart.
     - bemtpl97 and the insurance family dropped sex under the stance; ex-offender status stays here under every option,
       consistent with all of them.
   * **Panel:**
     - Drop (critic, domain practitioner, the advocate's rebuttal): DOL bars age and disability from its own per-person
       model for the same kind of decision, and a gain of 0.01 sets no case apart.
     - Keep (the builder, the advocate's opening brief, the precedent checker's middle option): WIOA names both as
       barrier groups to serve, and DOL's adjustment model must account for disability; after the rebuttals no agent
       argued to keep.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop every item that states or reveals age or disability (implemented) | the items above leave; four codes merged; pregnancy and limited English leave too | one test for every item; the regulation bars criteria by their effect as well as their purpose; DOL's own profiling ban | ROC AUC -0.009 to -0.011; drops programmes WIOA itself directs; the youth, VR&E and ESL cost unmeasured |
     | B | Drop the items that state a ground, keep the programmes and services received | age, the disability items, 303, 701, 702, 704 and 803 leave; 602, 917, 1207, the youth programme and service items, the VR&E referrals and the four codes come back | keeps what the person received | the programmes carry the grounds back in part; two tests where one would do |
     | C | Keep age and disability as WIOA barrier groups | every item above comes back; race, ethnicity and sex stay dropped | WIOA names them as groups to serve; the full signal | the regulation and DOL's profiling ban against it; departs from rais A |

   * **Recommendation:** A: one reading of the regulation for every item, which DOL's ban in its own per-person
     profiling model supports for the same kind of decision; decide it after rais issue 1. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: no change to `dataset.py`; a `CC` line in the record. If rais issue 1 takes A, add to the cases of the Tensions
     row: "wioa_employment_after_exit: race, sex, age, disability and the items that reveal them dropped from a
     follow-up score (29 CFR 38.6(b), UIPL 41-94)".
   - B: in `dataset.py`, `AGE_ITEMS = ("CALC4039", "PIRL702", "PIRL704")`, `DISABILITY_ITEMS` without 602, 917, 1006,
     1115 and 3007, `PREGNANCY_LEP_ITEMS = ("PIRL701", "PIRL803")`, `GROUND_CODES = {}`; restore PIRL 1205 code 2's
     label "Employment opportunity or internship, not only summer"; rewrite the SEL-1 bullet of `curation_comments`,
     `known`, `changes` and the grounds decision; re-run `dataset check` and the leak and task probes.
   - C: empty `AGE_ITEMS`, `DISABILITY_ITEMS`, `PREGNANCY_LEP_ITEMS` and `GROUND_CODES`; add `"PIRL202": [9]` to
     `UNKNOWN_ONLY` (no other blank) and order PIRL 303 (No, Yes, Yes special disabled); restore 1205's label; rewrite
     the same texts; re-run the same checks.

   [^c38]: 29 CFR 38.5 lists the prohibited bases (race, color, religion, sex, national origin, age, disability,
     political affiliation or belief); 38.6(b): a recipient must not, on a prohibited basis, "Provide to an individual
     any aid, benefit, service, or training that is different, or is provided in a different manner"; 38.6(d) bars
     criteria with that purpose or effect; 38.7 (sex includes pregnancy); 38.9 (national origin includes limited English
     proficiency). https://www.law.cornell.edu/cfr/text/29/38.6
   [^uipl]: UIPL 41-94 (Worker Profiling and Reemployment Services): "the following elements may not be used in the
     profiling system: age, race, ethnic group, sex, color, national origin, disability, religion, political affiliation
     and citizenship". https://oui.doleta.gov/dmstree/uipl/uipl94/uipl_4194.htm
   [^sel1]: **SEL-1** (Must): a task with ethical concerns is out; a Must the definition can fix is fixed rather than
     excluded (principles.md, the remedy ladder).
   [^wioa]: 29 USC 3102(24): individuals with barriers to employment include "(D) Individuals with disabilities", "(E)
     Older individuals", "(F) Ex-offenders" (https://www.law.cornell.edu/uscode/text/29/3102); 20 CFR 677.170(c)(2):
     DOL's statistical adjustment model accounts for disability and ex-offender status, on state-quarter aggregates.
   [^row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no
     longer use": bemtpl97 (Lennart, 2026-11-05), the insurance family (Lennart, 2026-11-08); its extension to any
     decision on a person where the actor's own law bars the factor is rais_employment_separation_1m issue 1 (AI,
     2026-11-09, pending).
   [^fu]: 20 CFR 678.430(c) and 680.150(c): follow-up services for adult and dislocated-worker participants "who are
     placed in unsubsidized employment", for up to 12 months.

2. **Ship the occupation, industry and CIP codes as codes, as now, or decode them into "words [code]", with the same letter as rais_employment_separation_1m issue 5 and sinan_dengue_case_screening_1m issue 4?**

   * **Problem:**
     - Eight columns ship as numeric codes (occupation, PIRL 403, 1306, 1311 and 1316; industry, 404-406; the training
       programme's CIP, 1305; 336 to 1,347 levels), though the record layout names their classifications (O*NET-SOC,
       NAICS 2012, CIP) and the official tables give every level its words, which your rule decodes[^c12].
     - Disclosure control coarsens some codes to a parent level that sits beside its children (2.5% of PIRL 404's codes
       and 3.6% of 403's, all programmes), so a decode needs the titles at every level of each hierarchy.
     - rais and sinan keep national classifications as codes too, so a third exception of one reason makes an amendment
       of the rule due[^amend].
   * **Background:** O*NET-SOC is the US occupation classification, NAICS the industry classification, CIP the
     Classification of Instructional Programs (fields of study); each has an official table of titles by code.
   * **Effect on the task:** none for a model that reads categories; a text-aware model gets the words only under B.
   * **Consistency:**
     - ny_wcb_assembled_claims_1m decodes NAICS into "words [code]", and labour_inspection_compliance decodes its
       industry codes from the official table shipped in its folder.
     - rais issue 5 recommends decoding, alike for sinan's occupation codes.
   * **Panel:** decode (the precedent checker: the rule and the two precedents); keep with the coarsening named (the
     claim and column auditors); the advocate and the critic left it to the batch.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Codes, the coarsening named (implemented) | as now; the notes name the three classifications, the coarsening and the industry code 999999 | no lookup files | a departure from the rule; the third exception of one reason in this batch |
     | B | Decode to "words [code]" | pinned O*NET-SOC, NAICS 2012 and CIP tables in the folder; each code gets the title of its own level; 999999 becomes "Wages exist, industry not known [999999]" | follows the rule and both precedents; the code stays in brackets | three lookup files and a decode by level to check |
     | C | Amend the rule for large national classifications | codes stay here, in rais and in sinan; the rule names the case | one decision for the batch | the rule's own example of a code to decode is an occupation, so the amendment goes against its wording |

   * **Recommendation:** B, since the official tables give every level its words, which the rule asks for; take the
     same letter as rais_employment_separation_1m issue 5 and sinan_dengue_case_screening_1m issue 4 (rais recommends B
     too). **Decision:** A, B or C?

   **Notes for the AI:** B: source the O*NET-SOC taxonomy the layout names (O*NET 10.0, codes truncated to six digits),
   NAICS 2012 and the CIP edition of the files; ship them as small CSV files next to `dataset.py`; decode in `_clean` to
   "title [code]" at the code's own level (trailing zeros mark a parent: SOC major and minor groups, NAICS sectors to
   industry groups), a code without a title raising; update the codes bullet of `curation_comments`; re-run `dataset
   check` and the dtype and task probes. C: write the amendment into CLEAN-12 in `cleaning_features.md` with its cases
   (rais, sinan, wioa).

   [^c12]: **CLEAN-12** (Should; amended 2026-11-01, Lennart): a nominal code whose codebook says what it means in words
     is decoded into those words; credit_g (Lennart, 2026-10-31: "we want the right labels in all cases").
   [^amend]: principles.md, "Exceptions and amendments": three exceptions of one reason make an amendment due.
     rais_employment_separation_1m issue 5 and sinan_dengue_case_screening_1m issue 4 (AI, 2026-11-09, pending).

**Review panel:** ship after changes (mediator), as the Title I version without a row budget. Tier full: claim auditor,
column auditor, split auditor, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic
with one rebuttal each, mediator; the reports below were written on the `_1m` version (all programmes, a 2,754,351-row
frame of 7.37M exits, test windows July 2024 to March 2025). Claim audit: 42 claims tested; 7 refuted (Texas's 2025Q1
labels, an incomplete wage quarter; the follow-up use case for the 84% of exits without Title I funding; keeping race,
ethnicity and sex; American Samoa's labels; the gap's stated reason; the ids of Texas and Utah across files; the
README's counts) and 3 partly, all fixed. Column audit: no shipped column recorded after the exit but PIRL 304 (masked
now); the invalid-SSN mechanism and the cleaning points fixed or noted. Split audit: right with notes (the gap's reason,
each window's report stage, the release codings), written now. Blind review: include with changes; its main concern, the
undocumented stitching of three files with an empty quarter and a 3.8x step in rows, was the gap quarter and the row
budget, now documented and the step gone. Task gamer: barely gameable from the kit; its one large exploit, Texas's
2025Q1 labels (+0.027 ROC AUC on the newest window), gone with the window shift, and training on the labels of other
windows (+0.005) is a matter of the harness. Debate: agreed on Title I only, one use case with `roc_auc`, the cuts of
Texas 2025Q1, American Samoa and Palau, dropping race, ethnicity and sex, and the notes; disputed: age and disability
(issue 1), the first-report lag left after the Texas cut (settled by moving the windows back a quarter), the previous
known outcome (settled: added). The mediator's issue 3 is issue 2 here; its issue 2, keeping January to March 2025 by
grading the rule on right-censored labels by severity, is a rule change, proposed as an item across datasets.

<details><summary>Mediator</summary>

MEDIATOR REPORT: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

Tier: full (seven phase-A agents; advocate and critic with one rebuttal each). Read: principles.md, review_panel.md,
the seven phase-A reports, both briefs and rebuttals, the builder's report, dataset.py, the record, and the REVIEW.md of
rais_employment_separation_1m and acs_food_stamps_2014_2024_1m for consistency. Two experiments of my own settle the
facts behind disputes 2 and 3 (section 8).

**1. RECOMMENDATION (judgment record)**
Verdict: ship after changes, as the Title I version `wioa_employment_after_exit` (full, no `_1m`).
Validity: SEL-1 triggered: race, Hispanic ethnicity and sex dropped (fixed); age, disability and where the drop
  stops are issue 1. USE-1 and USE-5 triggered, fixed (Title I adult, dislocated-worker and DWG exits only; one
  decision, the cohort-rate clause removed). USE-10 triggered, fixed (previous known outcome added). LEAK-24 triggered
  twice: Texas 2025Q1 (strong) and the newest window's first-report labels (small, but LEAK-24 has no grade); both
  fixed by moving the test windows back one quarter, which on Title I keeps SPLIT-14 without a new file (issue 2 only
  if you want January-March 2025 kept by an amendment). LEAK-39 and LEAK-25 fixed for American Samoa and Palau
  (dropped); the unlocated Title I mix kept under LEAK-25's 2026-11-02 amendment, with a note. LEAK-10 holds after the
  PIRL 304 mask. SPLIT-9 holds; SPLIT-10 met (its reason reworded); SPLIT-14 holds.
Value: TP-2 holds (Title I LightGBM 0.756-0.765 ROC AUC, 0.748-0.750 without age and disability; linear 0.71; dummy
  0.5); MET-1 and MET-8: roc_auc once the cohort clause leaves.
Quality: CLEAN-10, CLEAN-11, CLEAN-14 fixed or noted; CLEAN-12 (occupation, industry and CIP codes kept as codes) is
  issue 3, decided alike with rais issue 5 and sinan issue 4; SPLIT-20 notes on the release codings.
Weighed: size + (about 1.0M Title I exits, about 200 features, no sub-sampling), source + (an agency file with a
  record layout), gap + (social science), use case + (a real per-person closure decision; fit approximate).
For the curator: issue 1 (SEL-1, a reading of the law tied to rais issue 1); issue 2 (LEAK-24, optional: amend the
  rule to keep 2025Q1); issue 3 (CLEAN-12, P7).

**2. AGREED FACTS (no side disputes them; numbers from the reports named)**
 1. Target: PIRL 1602 = CALC 4013 on every cohort row of all three files; 1 exactly when the quarter's wages are above
    0 (45 exceptions in 2.44M). Youth-only exits are dropped (149,880). (builder, claim auditor)
 2. Follow-up services exist only for adult and dislocated-worker participants placed in employment (20 CFR 678.430(c),
    680.150(c)); 6,199,267 of 7,373,493 exits (84%) have no Title I funding stream, and 0 of 3,065,763 Wagner-Peyser-
    only exits carry a follow-up date. Title I (CALC 4001, 4002 or 4004): 1,098,270 exits, rate 0.717. (claim auditor,
    domain practitioner)
 3. Texas 2025Q1: target 0.398 against 0.623 one quarter earlier for the same exits (+0.226; 99th percentile over 650
    state-quarter cells +0.035); the hole sits on calendar 2025Q3; SPRA's Appendix B writes "not yet available" as 0.
    Title I: 2,586 rows at 0.539 against 0.704-0.816 in other Texas quarters. Without Texas the r0 ROC AUC rises
    0.023-0.027 and the national 2025Q1 rate is 0.669, above 2024Q3/Q4. (claim auditor, task gamer, advocate a2)
 4. American Samoa (120 exits) and Palau (1): all No; Appendix B: "State reported no wages ... All records were '0'".
 5. No shipped column is recorded after the exit except PIRL 304 (2,197 planned separations, no outcome link). No
    feature, copy, row-order or format shortcut (task gamer: 0 exact copies across the split, best column 0.637).
 6. Dropping race, ethnicity and sex costs nothing measurable (-0.001 to +0.005); age and disability carry 0.010-0.015,
    mostly age. Ex-offender status is not a 29 CFR 38 ground and is a WIOA barrier group. (claim auditor, domain
    practitioner)
 7. The newest window's labels are DOL's first report: a quarter's rate rises 0.7-1.1 points by its third report
    (Title I +0.01 to +0.72 points from first to second); the first-report labels cost 0.003-0.004 ROC AUC and reorder
    no model. (split auditor)
 8. 10-13% of each test window's exits are returning persons; their outcome at least 4 quarters back adds +0.007-0.008
    on them (all programmes, paired). Texas ids link 22.1% (PY 2024 Q4 to PY 2025 Q3), Utah 63.7% (PY 2023 Q4 to
    PY 2024 Q4), every other state 92.8% or more. (split auditor, claim auditor)
 9. Invalid SSN with all pre-entry wages blank: 19,556 exits at 0.022 over all programmes, but only 1,240 at 0.204 in
    Title I, where SPRA fills blank wages with 0; New York has 24,774 Title I invalid-SSN exits without a positive
    pre-entry wage at 0.324 against 0.424 for its valid SSNs. (column auditor, advocate a1, critic c1)
10. The 9-month gap is right (SPLIT-9 needs at least 6 months); its reason is the state's own wage records for quarter
    Q-2, not DOL's four-quarter fill (under which 12.3-15.1% of the train sides were unpublished at a window's start).
    (split auditor, claim auditor)
11. The empty 2024Q2 is the gap quarter; the 3.8x step in rows per quarter is the row budget. (split auditor, both
    briefs)
12. Pooled ROC AUC sits 0.008-0.015 above the within-board mean and ranks feature sets the same; no source fixes a
    k, a capacity or a cost (follow-up use runs from 0.2% to 36% of Title I exits by state). (domain practitioner)

New facts from my runs (section 8):
13. Title I train shares after the Texas and AS/PW cuts: shipped windows 57.2 / 64.2 / 71.3%; windows moved back one
    quarter (tests 2024Q2-Q4, data to 2024-12-31) 53.0 / 61.2 / 68.7%, so SPLIT-14 holds with no PY 2022 Q4 file;
    two quarters back 47.0% (below the floor; 51.2% if the gap-only quarter is not counted).
14. The first-report lag on Title I (rows in every report, LightGBM trained on all Title I exits before the gap):
    2024Q3 window 0.7564 / 0.7591 / 0.7593 on its 1st / 2nd / 3rd report labels; 2024Q4 window 0.7624 / 0.7652 on its
    1st / 2nd. A first report costs 0.0029 and 0.0027 (bootstrap SD 0.0004); a second report against the third
    +0.0002, within noise. The order of the four models holds on every label version; the LightGBM-linear spread moves
    by 0.0004 and 0.0017.
15. The previous known outcome on Title I adds +0.002 to +0.007 ROC AUC on the returning persons (10-13% of test
    exits), positive in 9 of 9 runs, and nothing measurable over all test exits (within +-0.001) (M1, section 8).

**3. CHANGES TO MAKE NOW (no decision needed), each with its rule**
 1. Population: Title I exits only (CALC 4001, 4002 or 4004 set), as the full version `wioa_employment_after_exit`
    (folder renamed, `version_of` and the row budget removed, record `v2_path`, CHANGELOG entry). USE-1, USE-5 (Must):
    the use case's decision exists only for these exits. Weighed size cannot override a Must.
 2. use_case: one actor and one decision (a Title I case manager or local board, at the last planned service, whom to
    keep in services or offer follow-up); the cohort-rate clause leaves; roc_auc stays; the fallback reason says why.
    USE-1, MET-1 (Must), MET-8.
 3. Test windows moved back one quarter: 2024Q2, 2024Q3, 2024Q4, with the 9-month gap; January-March 2025 leaves the
    frame (and with it the Texas hole), 2024Q1 becomes the gap quarter. LEAK-24 (Must, part 3) is triggered by a
    measured revision, and this fix keeps every other Must: SPLIT-14 at 53.0% (fact 13), the newest labels at their
    second report, which scored within 0.0002 of the third on 2024Q3 (fact 14). The splits_comment says why the newest
    quarter is out and when it comes back (PY 2025 Q4 brings 2025Q1 to its second report; then the current windows meet
    the same standard, if Texas's 2025Q3 wages are complete there). SPLIT-11 (Should, newest window first) gives way to
    LEAK-24. Settled by rank; issue 2 is the one way to keep 2025Q1 instead. If you take issue 2's amendment, keep the
    Texas cut (exits from 2025-01-01) as a rule on state and date with a Decision table of the 1st- against 2nd-quarter
    rates by state.
 4. Drop American Samoa and Palau (American Samoa's 120 exits are all Title I; Palau has none left after the youth
    filter), with Appendix B's words. LEAK-39, LEAK-25 (located, amended 2026-10-21).
 5. Drop race (PIRL 211-215), Hispanic ethnicity (210) and sex (201); rewrite the SEL-1 note with the reason (29 CFR
    38.6(b), UIPL 41-94) and update `known`. SEL-1 (Must, P1), the Tensions row as rais issue 1 extends it; the
    builder's reason (DOL's adjustment model) belongs to the aggregate decision that leaves with change 2. Keep
    ex-offender status (801, 2413, 2414).
 6. Add `previous_known_outcome` (Yes / No / none / unknown) and the quarters since that exit, built from the dropped id
    over the person's exits at least 4 quarters before the row's exit quarter, from every exit in the prepared files
    (the agency's records, all programmes); "unknown" for Texas and Utah rows with no earlier exit found, since their
    ids do not link across files (a rule on state, not the label); a note gives the link rates and the gain. USE-10
    (Must): the actor knows the person, and a gain is measured on the rows it concerns (facts 8 and 15), which sets it
    apart from milk_nir_composition's "no gain".
 7. LEAK-25 under Title I: the located-row rule finds only a mix (1,240 rows at 0.204), so no drop is required; keep
    them and the rest under the 2026-11-02 amendment with a note giving the state spread of invalid-SSN exits and New
    York's group (24,774 at 0.324 against 0.424). The task keeps signal beyond the state (within-board 0.714-0.722;
    the state alone 0.514-0.545 on Title I). PIRL 935 stays (SSN status at entry). Dropping the 1,240 is allowed but
    not needed.
 8. Mask PIRL 304 after the exit (2,197 rows), and 1410 and 2516 the same way (no rows today). LEAK-10.
 9. Notes (writing.md, SPLIT-20, LEAK-10, LEAK-22, PROV): each window's report stage and the re-source date; PIRL 935
    code 2 (retirement, timing unknown); NAICS 999999 ("wages exist, industry unknown") as a level of its own; Montana's
    blank pre-entry wages from 2023Q4 (Appendix C) and its one-day batch closure of 2024-09-06; local-board and PIRL
    108B coding by release, wages re-drawn per release, 413-423 cross-release copies of one participation at file
    boundaries (training only); the Texas and Utah id breaks; PIRL 923 exclusions as DOL's own denominator.
10. splits_comment: rest the 9-month gap on the state's own wage records for quarter Q-2 (cite the UI reporting rule or
    mark it as inference); say DOL's interstate and supplemental matches flip 0.5-1% of labels later; give what the
    newest training quarter adds at equal training size (gap 9 against 12: +0.002, split auditor e10). SPLIT-9,
    SPLIT-10. The README says why the gap quarter is empty.
11. Prediction point: the last planned service; the exit is recorded 90 days later and dated back (20 CFR 677.150(c)).
    USE-3. The information set does not change.
12. fit_reason: name the placement at exit and the UI claimant status the public file removed, next to the altered
    wages. USE-8.
13. Cleaning, P7 Should, cheap and safe: codes that only mean unknown become missing where the column has no other
    blank (300, 801, 805, 806, 910, 917, 918, 932; 202 if kept), and the "Unknown" level stays with its reason where a
    blank means "not applicable" (908, 909, 911, 914, 916) (CLEAN-10, CLEAN-12 table); PIRL 412's fill 999 to missing,
    the other implausible tenures noted (CLEAN-11); order 1328 and 3004 (and 303 if kept) or say why (CLEAN-14); CALC
    4041 against 4001/4003/4005 made one way or explained (CLEAN-5). README decision tables counted after the
    population filter (writing.md).

**4. ISSUES FOR THE CURATOR, ranked**
Issue 1 (P1, SEL-1 Must). Drop age and disability too, and where does the drop stop?
  Problem: age (CALC 4039) and disability (PIRL 202, 204-209, 939, 940, CALC 4021-4029; proxies 303, 602, 917, 922
    code 2, 1114 code 3) are prohibited bases for the actor (a recipient, 29 CFR 38.4; 38.5), and 38.6(b) bars giving a
    different service on a prohibited basis. WIOA also names older individuals and individuals with disabilities as
    barrier groups (29 USC 3102(24)(D),(E)) and the adjustment model must account for disability (20 CFR
    677.170(c)(2)). The text does not settle whether a score that directs more help by these grounds is barred (claim
    auditor).
  Effect: ROC AUC -0.010 to -0.015 over all programmes, -0.009 to -0.011 on Title I (0.7605 / 0.7594 / 0.7577 to
    0.7498 / 0.7482 / 0.7487, M1), mostly age. The grounds move a quarter of a board's lowest-20% list; people aged
    55+ fall from 35% to 21% of it (domain practitioner).
  For dropping (critic, the advocate's rebuttal, domain practitioner): UIPL 41-94 bars age, disability, race and sex
    from DOL's own per-person model that allocates reemployment services (WPRS): the same agency, the same kind of
    decision, the same list. Follow-up eligibility (678.430(c), 680.150(c)) names neither ground, and a state gives the
    barrier groups priority by policy, not through a score. A gain of 0.013 sets no case apart.
  For keeping (builder; precedent checker's option b; the advocate's opening): WIOA's barrier groups and the
    adjustment model; acs_food_stamps keeps the grounds its programme's eligibility rules use.
  Rule: SEL-1 (Must) and the Tensions row "a factor the actor may no longer use", whose extension to any decision on a
    person is rais issue 1 (pending). Not settled by rank: it is a reading of the law plus a rule extension, both yours.
  The edges need one reading, not one per column. 701 (pregnant or parenting youth; sex includes pregnancy, 38.7;
    2,609 Title I exits) and 803 (English learner; national origin includes limited English, 38.9; 51,931) have the
    same two-sided status as age and disability: a 29 CFR 38 ground and a WIOA barrier group. So they follow age and
    disability whichever way you decide. The Youth funding and youth-service items (13,463 Title I exits), the VR&E
    referrals (1006, 1115, 3007; about 1,000) and ESL services (1207; 8,172) record a programme or service that reveals
    a ground; the panel already drops the disability proxies of that kind (917, 922 code 2, 1114 code 3, at no measured
    cost), so the same test reaches these.
  Options: (a) drop age and disability, with 701, 803 and the items that reveal a ground (recommended: one test, and
    38.6(d) bars criteria by their effect as well as their purpose); (b) drop age and disability and the items that
    state them, keep programmes and services received as named proxies (then 602, 917, 922 and 1114 come back); (c)
    keep age and disability as WIOA barrier groups, and with them 701 and 803.
  What would settle it: your letter on rais issue 1 (rais A leads to a or b; rais B leaves age to this issue, where
    UIPL 41-94 is a fact for dropping it anyway; rais C leads to c) and your reading of 38.6 for a score that directs
    more help. The cost of the Youth, VR&E and ESL edges is unmeasured; it touches at most 1.2% of
    exits each and does not decide.

Issue 2 (P4, LEAK-24 Must; optional). Keep January-March 2025 by amending LEAK-24, instead of change 3?
  Problem: the newest quarter's labels are DOL's first report; LEAK-24 is a Must with no severity grade, so keeping it
    needs a rule change.
  Effect of keeping it: ROC AUC -0.003 on that window (Title I -0.0029 / -0.0027, fact 14), no model reordered; plus
    the Texas cut (2,586 Title I exits) and a note per window's report stage.
  For the amendment (both debaters, split auditor, domain practitioner): a measured revision that reorders nothing;
    the labels are not final even at the third report, so any reading of "complete" uses a tolerance. Both debaters
    chose it over a shift because the shift seemed to need PY 2022 Q4 (pandemic-tail outcomes) and to break the 50%
    floor; on Title I it needs neither (fact 13).
  For change 3 (precedent checker; the rule as written): a fix in the definition exists, and a Must takes no
    exception; tunisian's 2018 was cut, 2017 kept only where no censoring was measured; an amendment from one case.
  Decision: none needed to ship. Take the amendment only if you want the newest quarter back now; it becomes an
    across-datasets rule item (LEAK-24 graded by its measured effect on the evaluation), with this case as its first.

Issue 3 (P7, CLEAN-12 Should). Occupation (PIRL 403, 1306, 1311, 1316), industry (404-406) and CIP (1305) codes.
  Problem: shipped as codes, though the layout names O*NET-SOC 10.0, NAICS 2012 and CIP, whose tables give words; the
    notes give no reason. Disclosure control coarsens some codes (a parent sits beside its children).
  Effect: none for a categorical model; meaning for a text-aware model.
  Sides: decode to "words [code]" at the code's own level (precedent checker: the rule, ny_wcb_assembled_claims_1m,
    labour_inspection_compliance); keep the codes with the coarsening named (claim and column auditors). The debaters
    left it to the batch.
  Rule: CLEAN-12 (Should, amended 2026-11-01). With rais issue 5 and sinan issue 4 this is a third exception of one
    reason, so an amendment is due if all three keep codes.
  Decision: the same letter as rais issue 5 and sinan issue 4.

**5. THE DISPUTED POINTS, settled**
Dispute 1, age and disability. Both sides now say drop; the rules do not settle it (a reading of 38.6 and the pending
   rais extension). To the curator as issue 1, recommendation (a).
Dispute 2, the remaining first-report lag. Both sides asked for an amendment, on the premise that a shift needs PY 2022
   Q4 and breaks the floor. My measurement refutes the premise for Title I (fact 13: 53.0% with a one-quarter shift;
   fact 14: the second report is within 0.0002 of the third). By rank: LEAK-24 is a Must with a fix in the definition
   that keeps SPLIT-14 and SPLIT-9, so the fix wins (change 3). The amendment stays open as issue 2.
Dispute 3, the previous known outcome. Both sides now say add; USE-10 is a Must and nothing ranked above it conflicts;
   the construction reads no gap or test label. Settled: change 6. Re-measured on Title I (M1): +0.002 to +0.007 on the
   returning persons in every run, less than over all programmes, nothing measurable overall. USE-10 does not make the
   feature depend on its gain.

**6. THE TASK GAMER'S EXPLOITS, mapped**
The definition has no "Potential leak, kept on purpose:" note and no accepted warning (one, pirl913 constant, is
proposed by the builder), so no exploit is known by a note.
 1. Texas 2025Q1 push-down: +0.027 on r0 (+0.009 on the mean). LEAK-24 (strong) and LEAK-25 by its mechanism. New:
    the definition's newest-window note speaks of 0.9 points of first-report lag and calls the end mostly drift; the
    measured gain differs. Fixed by change 3 (or the Texas cut under issue 2).
 2. Training on the other test windows' labels in data.parquet: +0.004 to +0.006 per split. SPLIT-9 as the split
    protocol enforces it: a participant trains on each split's train indices only (the house protocol: iterate the
    splits, never re-split). Not a defect of this definition and the same for every temporal dataset; no change here.
    If you want it closed, it is a harness item across datasets (hand a model only its train side), not an issue of
    this REVIEW.md.
 3. Re-linking persons from rare dates and demographics: +0.0001, noise. LEAK-17 / LEAK-19, USE-10. Nothing found;
    change 6 ships the honest part (the agency's own history).
 Flaw B, Montana's blank pre-entry wages (Appendix C): +0.003 on r2 if Montana is dropped. SPLIT-20, LEAK-25 by
    reporting unit; new, a note (change 9). Under Title I SPRA fills blank adult and DW wages with 0, so the effect may
    differ (unmeasured).
 Flaw C, the absolute exit date as an input: honest feature engineering (+0.0036); SPLIT-10's remark on time as a
    number. No change.
 Unranked, source lookup (matching rows to the published file that holds PIRL 1602): a property of every public
    source; no change.

**7. CONSISTENCY WITH PRECEDENT (precedent checker's report, with the changes above)**
 - SEL-1 (precedent checker D1): dropping race, ethnicity and sex follows rais issue 1's recommendation A and
   acs's outreach reading (7 CFR 272.6). The builder's distinguishing fact is refuted as setting the case apart: DOL's
   model decides on state aggregates, and that decision leaves with change 2. Age and disability: (a) follows rais A
   (age dropped there at 0.006). The fact that sets wioa apart from acs: the follow-up decision allocates a service
   among people already eligible, and its eligibility rule names neither ground, while acs kept what SNAP's own
   eligibility uses. If you take rais B (keep age), wioa has a fact for dropping age anyway (UIPL 41-94 names it for
   the same agency's per-person service allocation); if rais C (pricing only), change 5 then rests on 38.6(b)'s own
   text, a law that names this decision, not on the stance: say so in the note. Ex-offender kept: consistent under
   every option.
 - Population (precedent checker D2): Title I follows rais issue 3's recommendation (the named actor's population,
   pending). The builder's reason for all programmes was the cohort clause, which leaves.
 - LEAK-24 (precedent checker D3): change 3 follows sf_permit_time and tunisian's 2018 cut (cut where follow-up is
   complete). Issue 2's amendment would be the first severity grade of LEAK-24.
 - USE-10 (precedent checker D6): adding follows tunisian_fraud_detection_challenge (Lennart, 2026-11-05).
   milk_nir_composition (pending) kept "no gain, not added"; wioa differs by a measured gain on the rows the feature
   concerns. The precedent checker's point stands for milk: if "no gain" is accepted there, write it into USE-10.
 - LEAK-25: the all-programmes rule would have followed caracas_cervical_cancer, account_debt_south_africa and
   fraud_detection (drop located rows); under Title I the rule locates a mix, so noaa_storm_events_damage's amendment
   (keep with a note) applies. Consistent.
 - CLEAN-12 (precedent checker D4): issue 3, decided alike with rais 5 and sinan 4; a third exception makes an
   amendment due.
 - CLEAN-10: the CLEAN-12 table (codes that only mean unknown become missing; ANES, 2026-11-01).
 - LEAK-10 (precedent checker D5): consistent.
 - No drift and no third exception other than CLEAN-12.

**8. EXPERIMENTS RUN (in the run's panel folder; LightGBM 400 trees, 127 leaves, 4 threads)**
M2 (m2_title1_lag_and_floor.py, .json, m2.log): facts 13 and 14 above.
M1 (m1_prev_outcome_title1.py, .json, m1.log): Title I exits, Texas 2025Q1 and AS/PW cut, every Title I exit before
  the gap as training, every Title I exit of the window as test; B1 = all features but race, ethnicity and sex; B2 = B1
  without age, disability and the disability proxies. Previous known outcome from all exits (any programme; youth-only
  exits excluded as in the definition), "unknown" for Texas and Utah rows with none found.
  Windows 2025Q1 / 2024Q4 / 2024Q3 (as shipped now; not re-run on the shifted windows of change 3):
  test exits 72,121 / 75,283 / 79,202; returning persons 12.6 / 11.0 / 9.8%; employment rate after an employed
    earlier exit 0.772 / 0.755 / 0.774, after one without 0.522 / 0.520 / 0.534; Texas and Utah test rows set to
    "unknown" 301 / 3,106 / 4,264.
  ROC AUC on the returning persons, without -> with the feature (bootstrap SD of each difference 0.0015-0.0020):
    2025Q1  B1 seed 0 0.7552 -> 0.7619 (+0.0067); seed 1 0.7551 -> 0.7618 (+0.0066); B2 +0.0061
    2024Q4  B1 seed 0 0.7420 -> 0.7475 (+0.0055); seed 1 0.7447 -> 0.7466 (+0.0019); B2 +0.0038
    2024Q3  B1 seed 0 0.7393 -> 0.7453 (+0.0060); seed 1 0.7409 -> 0.7441 (+0.0033); B2 +0.0064
  All test exits: +0.0013 / +0.0008, +0.0009 / -0.0007, +0.0003 / -0.0002 (B2 +0.0007, +0.0007, +0.0004); new persons
    -0.0010 to +0.0004.
  Base scores, B1 0.7605 / 0.7594 / 0.7577; B2 0.7498 / 0.7482 / 0.7487 (issue 1's cost on Title I).
  Reading: positive on the returning persons in 9 of 9 runs, mean about +0.005, smaller than the +0.007-0.008 over
    all programmes; the seed moves a paired difference by up to 0.004, so one paired run is less steady than the
    split auditor's report says.

</details>

<details><summary>Claim audit</summary>

**CLAIM AUDITOR REPORT: wioa_employment_after_exit_1m (record wioa_employment_after_exit), 2026-11-09**

Verdict: ship after changes. One validity Must is broken and not on the builder's list (LEAK-24: Texas's labels in
the newest test window are an incomplete wage quarter, not employment). SEL-1 (issue 1) is refuted in the builder's
recommended direction. Issue 2 moves toward Title I only, because the use case's follow-up decision does not exist
for 84% of the rows.

Validity: SEL-1 / Tensions row "a factor the actor may no longer use" (batch extension, rais_employment_separation):
  REFUTED for "keep" (29 CFR 38.6(b), (d)(2) bar race, national origin and sex as criteria for who gets a WIOA
  service; dropping them costs nothing measurable). LEAK-24 (Must): REFUTED, strong in window r0 (Texas 2025Q1
  labels 0.398 against a 1st-quarter rate of 0.623; ROC AUC 0.707 -> 0.734 without Texas). USE-1/USE-8:
  follow-up decision REFUTED for Wagner-Peyser-only rows (20 CFR 678.430(c)). LEAK-39/USE-5: American Samoa and
  Palau labels are a recording artefact, confirmed by SPRA's Appendix B (121 rows). SPLIT-10: the stated reasoning
  for the 9-month gap does not follow from its own premise (Should; wording plus an exception). LEAK-10: PIRL 304
  after exit (2,197 rows, no signal) and PIRL 935 code 2 (1,871 rows, timing unknown): small.
Value: MET-1/MET-2 hold (fallback roc_auc; looked once more; dummy 0.5 on every fold; 170k+ of each class per fold).
Quality: CLEAN-12 for SOC/NAICS/CIP/board codes is a batch-wide curator call; README counts disagree with the notes.

Data used: the prepared file wioa_exiters_q2_employment.parquet (7,523,373 rows; the definition's own filter rebuilt:
7,373,493 exits), the three raw files (PY 2023 Q4 CSV, PY 2024 Q4 and PY 2025 Q3 parquet) for items the definition
does not read (PIRL 1600, 1604, 1606, 1704, the ids), and the participant kit (the shipped 2,754,351-row frame and
splits) for models and the scorer. Models: untuned LightGBM (400 trees, 127 leaves), one seed per run, on the full
1M train side of each shipped split. Scripts and JSON outputs: a1..a9 in the run's panel folder.

**TABLE: claim | source | test | result | evidence | rule**
1 | Three files, report quarters 2024-06-30 / 2025-06-30 / 2026-03-31 | claims 1, notes | none needed beyond the builder's REPORT_QUARTER check; file sizes match the page (PY25Q3 parquet 565,496,159 B = 539 MiB, page "539 MB") | holds | a7: maturity ranges per file as stated | PROV-1
2 | PY 2025 Q3 on the national page; PY24Q4/PY23Q4 on the archive page | claims 2 | national page fetched 2026-11-09 | holds (archive page not reopened) | page lists PY 2025 Q1, Q2, Q3 only; no Q4 file yet | PROV-8
3 | PY23Q4 ".csv" link serves 5.4 GB CSV | claims 3 | file on disk | holds | 5,396,414,277 B | -
5 | year 2026, pinned PY 2025 Q3 snapshot | claims 5 | - | holds | - | PROV-9
7 | Cohort = CALC 4013 not blank; 1602 = 4013; PIRL 923 = 0; CALC 4006 = 0 | claims 7, notes | recomputed on all three files (was PY25Q3 only) | holds | 1602 != 4013 in 0 / 1 / 0 cohort rows (PY23Q4 / PY24Q4 / PY25Q3); 923 = 0 and 4006 = 0 on every cohort row of every file | USE-5, LEAK-22
8 | Youth-only exits dropped (149,880), DOL's Youth indicator differs | claims 8, notes | rebuilt the filter | holds | 149,880 dropped, 7,373,493 kept | USE-5
9 | 7,373,493 exits, rate 0.679; programme counts; "Wagner-Peyser only 6,199,267 (84%)" | claims 9, notes, issue 2 | recount | holds except one label | all counts reproduce exactly; 6,199,267 is "no Title I funding stream" and still includes 94,272 exits served by a veterans' programme (PIRL 914 = 1/2); WP only without veterans' programmes = 6,104,995 (82.8%). Title I (adult, DW, DWG) 1,098,270, rate 0.717; Title I train sides 626,898-780,674, test windows 74,729-79,207 (issue 2's numbers hold) | -
10 | Each file fills exits up to report quarter minus 4; code 9 after | claims 10, notes | per file, filled share and code 9 by exit quarter | holds | filled 0.998-0.999 in the matured quarters, code 9 on 100% after, in all three files | -
11 | No exit taken twice | claims 11, notes | ranges do not overlap; looked for the same participation moved across a file boundary (same state, id and entry date, exit 2023Q3 in PY24Q4 and 2023Q4 in PY25Q3) | holds, nearly | 413 such pairs (404 of them Texas), all inside the training period; Texas's ids mostly do not link (see 23), so its count is a lower bound | LEAK-16
12 | Overlap PY24Q4 vs PY25Q3: 1,782,908 vs 1,800,946 rows, 1,642,717 matched, 13,986 labels changed | claims 12, notes | recomputed | holds (numbers) | identical numbers; but 136,434 of the 140,191 unmatched PY24Q4 rows are Texas (see 23), so the "label revision" figure leaves out the state with the largest revision | -
13 | Target = 1602 = 1, set when the quarter's wages > 0 | claims 13, notes | Texas, 1602 against wages > 0 (PIRL 1704) by exit quarter in both parquet files | holds | the share with 1602 = 1 equals the share with wages > 0 in every Texas quarter (e.g. 2025Q1 0.3977 both); the builder's 45 exceptions of 2.44M stand | USE-5
15 | Prediction point = the day of exit | claims 15, notes ("Prediction point") | TEGL 10-16 Change 2 (read, text extracted from the PDF) | holds in substance, wording wrong | "The date of exit cannot be determined until 90 days have elapsed since the participant last received services ... At that point, the date of exit is applied retroactively to the last date of service." The decision is made at least 90 days after the date the notes call the prediction point. No kept feature is known only after that later point (the masked dates already go; the pre-entry wages are on file by then); the target quarter has not started at exit + 90 days | USE-3
16 | Post-exit outcome items not read | claims 16, notes | RAW_COLUMNS against the list | holds | none of 1600-1618, 1703-1706, 1800-1805, 1814, 1900, 1901, 1406, 1412, 1503, 2002, CALC 4014-4019 is read | LEAK-10
17 | 1002, 1007, 1100, 1101, 1103 dropped | claims 17 | RAW_COLUMNS | holds | not read | LEAK-10
18 | Dates masked when after the exit, counts | claims 18 | recount on all three files | holds | 1000: 12,322 + 24,416 + 21,510 = 58,248; 1409 2,751; 1806 1,629; 1807 2,587; 1808 1,651; 1809 6,963; 1810 24,472 (exact) | LEAK-10
19 | Every other kept date never after the exit (PY25Q3), except 304 (994) and 2414 (1) | claims 19 | all 69 kept date items, all three files, shipped population | holds except PIRL 304 | 0 rows after exit for every kept date item but the masked ones and PIRL 304: 365 / 992 / 840 = 2,197 rows. The layout calls it "Date of Actual Military Separation" ("the date on which the participant separated"); "known at entry as planned" is an inference; median 83 days, p90 437 days after exit; rate 0.607 against 0.617 for all veterans (no outcome link) | LEAK-10 (small)
20 | Split counts and shares | claims 20, splits_comment | recount | holds | 4,927,593 / 4,323,409 / 3,757,391 (66.8 / 58.6 / 51.0%); tests 632,327 / 593,923 / 625,797 | SPLIT-14
21 | The 9-month gap: "DOL's own files fill it four quarters after the exit quarter. So a model refit when a window starts knows the outcomes of the exits up to the quarter that ended nine months before" | splits_comment, claims 21 | follow DOL's own timing (claim 10) | refuted as reasoning; holds on another premise | under DOL's timing an exit of quarter Q-4 is first filled in report quarter Q, i.e. at the END of the test window (and submitted about 45 days later); at the window's start DOL's newest file fills exits up to about Q-6. A 12-month gap would follow from the stated premise, and it breaks the floor: oldest window's train side 43.3% (3,191,161 rows). The 9-month gap holds only if the state's own in-state wage records for quarter Q-2 are in hand when quarter Q starts, which is plausible but not stated or checked | SPLIT-10 (Should), SPLIT-14
22 | Returning persons: 9.9-12.6% of each test window | claims 22, notes | linkability of the ids (see 23) | holds as a lower bound | Texas ids link for 22% of its rows between PY24Q4 and PY25Q3 and Utah's for 64% between PY23Q4 and PY24Q4, so returning persons in those states are under-counted; no feature carries an earlier outcome; prev-outcome feature +0.001 (builder) | SPLIT-13
23 | Encrypted ids are consistent across PY24Q4 and PY25Q3 | claims 23, notes ("the ids match across the two parquet files") | match rate per state on (state, id, exit date), and on id alone | REFUTED for Texas | Texas: 175,203 rows (PY24Q4, exits 2023Q4-2024Q2) against 193,103 (PY25Q3; +10% rows), 38,769 match on id and exit date (22.1%), 43,166 on id alone; RI 81.7%, MP 74.8%; all other states 92.8% or more. PY23Q4 -> PY24Q4: UT 63.7%, TX 80.2%, OK 0% | PROV (a fact about the source)
24 | Codes decoded into the layout's words | claims 24, notes | spot check of 16 items against the layout text (1303, 602, 1115, 3007, 1205, 907, 911, 207-209, 3005, 3006, 2004, 939, 808, 413) | holds | words match; 939's 0 = "Neither" is in the layout ("Record 0 or leave blank if neither condition applies") | CLEAN-12
25 | Undocumented codes set to missing as invalid | claims 25, notes | layout PDF parsed directly (the text copy lost columns) | holds as "undocumented"; "invalid" untested | the PY 2025 Q3 Appendix A has no "2025 Code Value" column although the overview points to one, and the national page lists no other Appendix A. The items with these codes (301, 302, 303, 316, 402, 1114) are exactly the ones the overview names as changed in the PIRL 2025 schema, so they are probably new-schema values SPRA could not map, not typing errors; missing is still the right default | CLEAN-11
26 | PIRL 931 holds 4 for most rows, 1-3 otherwise | claims 26 | counts and rates by code and file | holds | code 4 1.2-1.3M rows per file; code 1 (2,561-3,476 rows per file) employed 0.87-0.88 against 0.68-0.69 | CLEAN-11
29 | Small local areas left out | claims 29, notes | PIRL 108A = 00000 ("Record removed ... fewer than 50 participants") in the cohort | holds | 0 rows with 108A = 0 in any file | PROV-3
30 | Oklahoma only in 2022 (8,923) | claims 30, notes | cohort rows by quarter | holds | OK in PY23Q4 only (17,956 rows 2022Q1-2023Q2, of which the 2022 part is taken); none in PY24Q4 or PY25Q3 | -
31 | Metric: fallback roc_auc; no per-person metric at the source | metric reason, claims 31 | MET-1 looked once more: TEGL 26-15 Att. II (read: fixed effects on state-quarter aggregates, p. 2), DOL's PY 2024-2025 model-selection page (state-level models with state fixed effects, compared on state outcomes), one web search for a per-person paper (found only a slide deck on unemployment one year after exit, another target) | holds | no per-person metric found | MET-1, MET-11
31b | Metric computable on every fold | MET-2 | data_foundry.v2.metrics.scorer on a class-share dummy, per shipped fold; class counts | holds | dummy 0.5 on r0/r1/r2; positives 319,798 / 329,059 / 328,488, negatives 180,202 / 170,941 / 171,512 per test fold; the scorer equals sklearn's ROC AUC on a LightGBM prediction (0.70706) | MET-2
31c | The metric scores the use case's decision | MET-1 ("at the unit the actor acts on") | read against the two decisions in use_case | partly | ROC AUC scores the per-person ranking (whom to offer follow-up); it does not score "the employment rate expected of its exit cohort", an aggregate whose error is a calibration question. The scored decision is the per-person one, which is the one 29 CFR 38 constrains (row SEL-1) | MET-1
32 | Use case: a state agency at exit decides whom to offer follow-up services and sets the expected rate | task_summary.use_case, claims 32 | the regulation and the layout's program columns | REFUTED for 84% of the rows | 20 CFR 678.430(c): follow-up services are "for participants in adult or dislocated worker workforce investment activities who are placed in unsubsidized employment", "for up to 12 months after the first day of employment"; the layout marks PIRL 1503 (follow-up) required for Adult, DW and DWG only, not Wagner-Peyser or JVSG. So for the 6.2M exits without a Title I stream no follow-up service exists to allocate; only the aggregate cohort-rate decision is left for them | USE-1, USE-8
33 | American Samoa's 120 exits all not employed, "maybe because its wage records are not matched" | notes, claims 33 | SPRA's Appendix B (PY25Q3 xlsx) | the "maybe" is confirmed; the keep conflicts with LEAK-39/USE-5 | Appendix B, PIRL 1704, states AS and PW: "State reported no wages in the 2nd quarter after exit quarter ... All records were '0'." The label of these rows records that the territory sends no wages, not employment; the state feature (AS) gives it away; 120 AS + 1 PW cohort rows (23 AS rows in the 2025Q1 window) | LEAK-39, USE-5
34 | Newest window: "January-March 2025 (0.640) may read about 0.9 points higher in a later file"; "most of it drift (0.718 in 2022Q1 to 0.656 in 2024Q3)"; probe 13's rising No rate read as drift plus a little immaturity; issue 3 rated "weak" | notes ("Anomaly"), claims 34, builder issue 3 | per (state, exit quarter): 1st-quarter-after-exit employment (PIRL 1600) against the target; the same calendar quarter seen through PIRL 1604 and 1606; the national rate with and without Texas; LightGBM on the shipped windows with and without Texas | REFUTED; strong | see Finding 2 below: Texas 2025Q1 target 0.398 against 1st-quarter 0.623 (gap +0.226; the 99th percentile of the gap over 650 state-quarter cells is +0.035, the next largest +0.06); calendar 2025Q3 reads 0.385 / 0.393 / 0.398 for Texas's 2024Q3 / 2024Q4 / 2025Q1 exits against 0.65-0.70 for every other Texas quarter; national 2025Q1 rate without Texas 0.669 (with 0.640), above 2024Q3/Q4 (0.652 / 0.658): the release-end rise of No is Texas alone, not drift. ROC AUC r0 0.707 -> 0.734 without Texas (Texas alone 0.578); r1 0.725 -> 0.729, r2 0.722 -> 0.726 | LEAK-24 (Must)
35 | Post-exit date flags score ROC AUC 0.499-0.500 | claims 35 | - | holds (builder's numbers; EV-2: a single-column score does not decide timing, and the drop is for timing anyway) | - | LEAK-10
36 | 408, 409, 1812 ship unordered | claims 36 | layout codes | holds | 1-3 are not ranked among themselves; CLEAN-14 allows categorical by default for an ordinal scale | CLEAN-14
37 | Local board 99999 = liable state record | claims 37 | layout PIRL 108-A | holds | "If participant record is a liable state record, record 99999." | -
38 | DOL's adjustment model lists female, age bands, Hispanic, race, disability, offender, ... (Att. II Table 1) | notes, claims 38 | read Att. II text | holds as a fact; does not carry the conclusion drawn from it | Table 1 lists them, "on exiters aggregated to the State level on a quarterly basis" (p. 2); the statute's list for that model (20 CFR 677.170(c)(2)) names disability status and ex-offender status but not race, sex or ethnicity. The model sets state targets; it allocates no service to a person | SEL-1 (see below)
39 | Task probes: LightGBM 0.713, 3 of 3 windows | claims 39 | own untuned LightGBM on the full 1M train sides | holds | 0.707 / 0.725 / 0.722 (mean 0.718) | TP-2
SEL | Protected grounds kept (race, ethnicity, sex, disability, ex-offender, age); builder recommends keep | notes ("Note: race, ethnicity..."), issue 1 | 29 CFR part 38 read (38.2, 38.4, 38.6), 20 CFR 677.170 and 678.430 read; LightGBM with and without the grounds on the three shipped windows | REFUTED for race, ethnicity and sex; age and disability a curator call; ex-offender holds | see Finding 1 below | SEL-1, Tensions row (factor the actor may no longer use), USE-6
P304 | (implied) every kept date is known at the exit | - | see row 19 | 2,197 rows of PIRL 304 after the exit | see 19 | LEAK-10 (small)
P935 | (implied) PIRL 935 is known at the exit | - | rate by code; the layout's definition | untested (timing not documented) | code 2 "Retirement" ("Record 2 if the participant retired from employment"), 1,871 rows, employed 0.31 against 0.68; an "Accountability Exit Status" may be set at or after the exit; code 1 (invalid or undisclosed SSN, 446k rows) is known at entry | LEAK-10 (maybe; tiny)
COPY | (implied) no row is a copy across the split | - | entity logic plus the builder's probe 5 | holds | test windows sit 9 months after train; a person's exits are distinct participations at least 9 months apart; exact copies 0.0% with the dates | LEAK-16, LEAK-17
NAICS | (implied) codes without words stay as codes (CLEAN-12) | notes ("Kept as codes") | the layout's code definitions; counts | open (batch question) | see Finding 7 | CLEAN-12
README | Notes match the generated decisions | README | compare | refuted (minor) | the decision tables count on all 7,523,373 prepared rows (youth-only included), the notes on 7,373,493: PIRL 301 code 9 11,565 (table) against 10,285 (notes); PIRL 1000 58,729 against 58,248; PIRL 402 645 against 634 | writing.md

Not tested: 4 (access, by the builder's curl), 6 (the disclaimer's words, read by the builder), 14 (that 1602 keeps its
0/1 meaning beyond row 13's identity with wages), 27 (constant and copy drops, by the bundle checks), 28 ("NA"
provider names).

**REFUTED AND UNTESTED CLAIMS, RANKED (principles.md: P1 first, then Must first, then size)**

Finding 1 (P1/P3, SEL-1 and the Tensions row "a factor the actor may no longer use", as extended by the
rais_employment_separation panel to any decision where the actor's own law bars the factor; Must): race,
ethnicity and sex stay as inputs to a decision the actor's own law bars them from. (Ranked first as P1 when read as
SEL-1, as the builder files it; the Tensions row itself sits under P3/P4. Finding 2 is the measured break the
builder's list does not have.)
  Claim refuted: notes "Note: race, ethnicity, sex, disability and ex-offender status are inputs ... DOL's own
  statistical adjustment model explains the same outcome with them"; builder issue 1, recommendation "keep".
  Law, read:
  - The actor is a state workforce agency, a "recipient" under 29 CFR 38.4(zz) ("(2) State Workforce Agencies").
    The part covers recipients and "Programs and activities that are part of the one-stop delivery system" operated
    by the WIOA sec. 121(b) partners (38.2(a)); 29 U.S.C. 3151(b)(1)(B) names "(ii) programs authorized under the
    Wagner-Peyser Act" and "(viii) activities authorized under chapter 41 of title 38" (the veterans' programmes).
  - Prohibited bases (38.4): "race, color, religion, sex, national origin, age, disability, or political
    affiliation or belief", plus citizenship and participation for beneficiaries. Ex-offender status is not among them.
  - 38.6(b): "A recipient must not, directly or through contractual, licensing, or other arrangements, on a
    prohibited basis: (1) Deny an individual any aid, benefit, service, or training; (2) Provide to an individual any
    aid, benefit, service, or training that is different ..."; 38.6(d) bars "standards, procedures, criteria, or
    administrative methods" with that purpose or effect in deciding "(ii) The class of individuals to whom such aid,
    benefit, service, training, or facilities will be provided".
  - So a per-person score that uses race, Hispanic ethnicity (national origin) or sex to decide who is offered
    follow-up help is a criterion on a prohibited basis: barred.
  - Age and disability are prohibited bases too, but WIOA itself directs services by them: the Youth programme is
    defined by age, an "individual with a barrier to employment" includes "(D) Individuals with disabilities",
    "(E) Older individuals" and "(F) Ex-offenders" (29 U.S.C. 3102(24), read), 38.6(g) exempts programmes limited by statute to
    certain classes, and the statute's adjustment model must account for "Disability status" and "Ex-offender
    status" (20 CFR 677.170(c)(2), read; the list names neither race nor sex nor ethnicity). Whether using them to
    direct more help counts as a barred criterion is not settled by the text: a curator call.
  - One nuance for race: the same list names "(C) Indians, Alaska Natives, and Native Hawaiians" as a barrier
    group (and section 166 funds programmes for them), so PIRL 211 and 214 overlap a statutory target group. The PIRL
    items record self-identified race, not eligibility for those programmes, and the other race items, Hispanic
    ethnicity and sex have no such carve-out.
  - The builder's reason does not carry: DOL's adjustment model uses female, race and Hispanic to set state targets
    on state-quarter aggregates (Att. II p. 2). It decides no individual's service. The shipped task is scored per
    person with ROC AUC, i.e. the per-person ranking (follow-up), which is the decision 38.6 constrains.
  What dropping costs (untuned LightGBM, full 1M train side, ROC AUC on all test rows / without Texas):
                                         r0 (2025Q1)       r1 (2024Q4)       r2 (2024Q3)
    all features                         0.7013 / 0.7306   0.7257 / 0.7297   0.7219 / 0.7251
    without race, ethnicity, sex         0.7065 / 0.7344   0.7252 / 0.7293   0.7208 / 0.7238
      ... and without age                0.6938 / 0.7199   0.7108 / 0.7143   -
      ... and without disability items   0.7015 / 0.7298   0.7240 / 0.7275   -
      ... and without age and disability 0.6928 / 0.7167   0.7097 / 0.7128   0.7049 / 0.7072
      ... and without ex-offender too    0.6918 / 0.7163   0.7108 / 0.7142   0.7059 / 0.7080
  Seed-to-seed spread is about 0.005 (r0 "all": 0.7071 and 0.7013 with two seeds). Dropping race, ethnicity and sex
  changes nothing measurable (-0.001 to +0.005); age carries 0.013-0.015; the disability items 0.001-0.005;
  ex-offender status nothing.
  Mildest remedy: drop PIRL 201 (sex), 210 (Hispanic/Latino) and 211-215 (race) under the batch stance; put age
  (CALC 4039) and the disability items (202, 204-209, 939, 940, CALC 4021-4029; 303 and 602 carry disability too) to
  the curator as their own question, with the WIOA targeting carve-out on the keep side; keep ex-offender status
  (801, 2413, 2414), not a section 188 ground and a named barrier. Alternatively re-frame the use case to the
  aggregate cohort expectation only (DOL's own use of these variables), but then ROC AUC no longer scores the
  decision (row 31c). The note should name age, which the current note omits.

Finding 2 (P4, LEAK-24, Must; strong): Texas's labels in the newest window record an incomplete wage quarter.
  Claim refuted: notes "Anomaly: the newest test window's labels ... may read about 0.9 points higher in a later
  file ... most of it drift", builder issue 3 ("weak"), claims 34.
  Evidence (measurement on the source files):
  - PY 2025 Q3, Texas, exits 2025Q1 (68,625 cohort rows): employed in the 1st quarter after exit 0.623, in the 2nd
    (the target) 0.398. In every other Texas quarter the two are within 0.03 (2024Q4: 0.653 / 0.656).
  - The hole sits on calendar quarter 2025Q3, whichever exit cohort measures it: Texas's 2024Q3 exits read 0.385 in
    their 4th quarter after exit, its 2024Q4 exits 0.393 in their 3rd, its 2025Q1 exits 0.398 in their 2nd (the
    target); every other Texas cell is 0.65-0.70. CA, FL and NY show nothing of the kind.
  - Over all 650 (state, exit quarter) cells with 500+ exits that the definition ships, the 1st-quarter rate exceeds
    the 2nd by at most +0.035 at the 99th percentile; Texas 2025Q1 is +0.226, the next largest +0.06.
  - SPRA's Appendix B: "Changed blank to '0' (no) for those who have exited", "Changed code '9' (information not yet
    available) to '0' (no) when complete data are expected", and quarter-two items blanked only "for exit dates on or
    after 4/01/2025". So Texas's missing matches for 2025Q3 were written as "not employed".
  - National 2025Q1 rate 0.640 with Texas, 0.669 without (2024Q3 0.652, 2024Q4 0.658 without): the release-end
    rise of the No rate that leak probe 13 flags (z +2.2 to +2.9) is Texas alone, not drift.
  - Texas's first reports also lag elsewhere (2024Q2: 0.679 in PY24Q4, 0.704 in PY25Q3) and its ids changed between
    the two parquet files (Finding 5), so its reporting changed around 2025.
  What it changes: window r0 (Jan-Mar 2025) scores a recording artefact for 10.9% of its shipped rows (54,315 of
  500,000). Untuned LightGBM ROC AUC on r0: 0.707 with Texas, 0.734 without; Texas alone 0.578 (0.689 / 0.691 on
  r1 / r2). Removing Texas moves r1 and r2 by +0.004 each. A second seed gives the same picture (0.701 -> 0.731).
  The newest window looks hardest only because of this hole.
  The builder's remedy ("take that quarter from the PY 2025 Q4 file when it is out") is not available: the national
  page lists PY 2025 Q1-Q3 only (fetched 2026-11-09).
  Mildest remedy: drop Texas's 2025Q1 exits from the frame (68,625 rows), with a Decision table of the
  1st-quarter against 2nd-quarter rates by state for 2025Q1 as the evidence, a note, and a revisit when PY 2025 Q4
  is out (take 2025Q1 from it if Texas's 2025Q3 wages are complete there). Alternative: the builder's option (b),
  windows one quarter earlier with the PY 2022 Q4 file added for the 50% floor. Also drop American Samoa and Palau
  (121 rows; Finding 3b), the same mechanism.

Finding 3 (P3, USE-1/USE-8, Must on the written use case; issue 2): the follow-up decision does not exist for the
Wagner-Peyser-only rows.
  Claim refuted: use_case "to decide whom to offer follow-up services", for 84% of the rows.
  Evidence: 20 CFR 678.430(c) (read): follow-up services are "for participants in adult or dislocated worker
  workforce investment activities who are placed in unsubsidized employment", "for up to 12 months after the first
  day of employment". The record layout's program columns mark PIRL 1503 (follow-up) required for Adult, DW and DWG
  only; PIRL 1412 for Youth only. Of the 7,373,493 exits, 6,199,267 have no Title I funding stream (6,104,995 also no
  veterans' programme). For them only the second decision of the use case remains (the expected rate of the exit
  cohort), which is DOL's aggregate decision (fit approximate already).
  Also: follow-up is triggered by placement in a job, so the per-person decision is "whom among the placed to keep
  in contact with", not "whom predicted unemployed to help" (the domain practitioner's report measures the same).
  What it changes: issue 2 tilts toward the builder's option (b), Title I only (1,098,270 exits, rate 0.717, no
  sub-sampling, train sides 627k-781k, test windows 75k-79k), or the use case must be rewritten for the Wagner-Peyser
  rows (the cohort-rate decision), and the SEL-1 reading then follows that decision.
  Mildest remedy: a curator call between (a) Title I only as the full version, with the follow-up use case, and (b)
  all programmes with a use case that names a decision Wagner-Peyser exits have (and the matching metric reading).

Finding 3b (P3/P4, LEAK-39 and USE-5, Must; tiny): American Samoa and Palau labels are not employment.
  Claim refuted: notes "maybe because its wage records are not matched (a recording artefact ... kept)".
  Evidence: Appendix B (PY25Q3), PIRL 1704, states AS and PW: "State reported no wages in the 2nd quarter after exit
  quarter ... All records were '0'." 120 AS and 1 PW cohort rows, all labelled No; the state feature identifies them
  (probe 4 found AS pure). Mildest remedy: drop the AS and PW rows (121) with that quote.

Finding 4 (P4, SPLIT-10, Should): the 9-month gap's stated reason does not follow from its premise.
  Claim refuted (as reasoning): splits_comment and claims 21.
  Evidence: by the definition's own measurement (claim 10) DOL fills exit quarter E in report quarter E+4, so the
  labels of the newest training quarter (Q-4) appear in a DOL file only at the end of the test window. DOL's timing
  would need a 12-month gap, which puts the oldest window's train side at 43.3% (SPLIT-14 Must breaks). The 9-month
  gap can rest on the state's own wage records for quarter Q-2 being in hand when Q starts (plausible for in-state
  wages; not shown).
  Mildest remedy: reword the splits comment to that premise, record the departure from DOL's timing as the
  Tensions-row exception (unmatured training labels against the floor), and give what the newest training quarter
  adds at equal training size (SPLIT-10's last sentence).

Finding 5 (P5, a source fact; minor for validity): Texas's (and partly Utah's, Rhode Island's, Northern Mariana
Islands') encrypted ids do not link across files.
  Claim refuted: claims 23, notes ("the ids match across the two parquet files").
  Evidence: Texas 22.1% match (PY24Q4 -> PY25Q3), 175,203 against 193,103 rows for the same exit quarters; UT 63.7%
  (PY23Q4 -> PY24Q4); RI 81.7%, MP 74.8%.
  What it changes: the repeated-person shares (9.9-12.6%) are lower bounds; the label-revision count (13,986) leaves
  out Texas, the largest reviser; up to 413+ participations may be counted twice at the 2023-10-01 file boundary
  (inside training only). No validity change (the id is not shipped; the gap keeps earlier labels before the
  window). Mildest remedy: correct the notes' sentence.

Finding 6 (P4, LEAK-10; small): two kept items may be recorded after the exit.
  - PIRL 304 "Date of Actual Military Separation": 2,197 rows after the exit date (median 83 days, p90 437); the
    "known at entry as planned" reason is an inference against the layout's word "actual". No outcome link (0.607
    against 0.617 for veterans). Mildest remedy: add PIRL 304 to MASK_AFTER_EXIT, as for the other dates.
  - PIRL 935 code 2 "Retirement" (1,871 rows, employed 0.31 against 0.68): untested timing ("Accountability Exit
    Status"; the layout gives no date). Mildest remedy: set code 2 to missing, or a "maybe a leak" note (EV-6).

Finding 7 (P7, CLEAN-12, Should; the batch's open question): SOC, NAICS, CIP and local board codes have words only in
external tables.
  Facts for the call: the layout names the tables ("cross walked to the O*Net 10.0 code"; "cross walked to the 2012
  NAICS industry codes"; CIP with a link to NCES; the national page points to the WIPS "WDB Reporting Codes" for
  boards). Distinct codes on the shipped population: PIRL 403 980, 404 1,322, 1305 1,373, 1306 791. Disclosure control
  truncates to group levels with trailing zeros (3.6% of 403's and 1.3% of 404's filled values end in 000), so a
  decoding needs every level of each hierarchy. NAICS 999999 means "Wages 1st Quarter Prior ... exist and NAICS Code
  is not known" (375,521 exits, rate 0.641), a sentinel the notes do not mention. A 1:1 relabelling changes nothing
  for a categorical model; it adds meaning for text-aware models and loses the code's prefix unless written as
  "code - title".
  Mildest remedy: keep the codes as now (consistent with whatever the batch decides for rais and sinan's CBO),
  name the three taxonomies and their versions and the 999999 sentinel in the notes; if decoded, "code - title".

Finding 8 (P7, writing; minor): the README's decision tables (counted on all prepared rows, youth-only included)
disagree with the notes' numbers (counted after the youth filter): PIRL 301 code 9 11,565 against 10,285, PIRL 1000
58,729 against 58,248, PIRL 402 645 against 634. Mildest remedy: count the decisions on `df` (after the filter) or
say "before the youth filter" in the titles. Also "Wagner-Peyser only 6,199,267" should read "no Title I funding
stream" (94,272 of them had a veterans' programme).

Untested, ranked:
  - PIRL 935 code 2 timing (Finding 6): needs the PIRL 2021 specification's instruction for element 935.
  - Whether the 2025-schema codes of 301/302/303/316/402/1114 carry meaning (row 25): needs the PIRL 2025 layout
    (ETAPerformanceReporting@dol.gov per the overview); missing stays the right default.
  - Whether the 9-month gap matches state wage-record timing (Finding 4): needs a state's wage-record schedule.
  - The first-report revision outside Texas in the 2025Q1 window (weak LEAK-24 part): 2024Q2 rose 0.665 -> 0.674
    between files, 46% of the matched 0 -> 1 changes in MI, AZ and NJ, Texas 31% of the rise; about 0.6 points expected in r0 after
    Texas is dropped; keep with the note and re-check against PY 2025 Q4.

Files (scratch, all in the run's panel folder): a1_population.{py,json} (counts, dates after exit on all
files, PIRL 935), a2_maturity.{py,json} (2024Q2 by state in two files, state year-on-year), a3_texas.{py,json},
a4_q1q2_scan.{py,json} (650 state-quarter cells), a5_eval.{py,json,log} (scorer dummy and LightGBM with/without
Texas), a6_protected.{py,json,log} (protected grounds), a7_files.{py,json} (claims 7, 10, 23, 29, 30 on all files),
a8_tx_ids.{py,json}, a9_age_vs_disability.{py,json,log} (age and disability apart).

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

**VERDICT**
Ship after changes. No shipped column was recorded after the exit. There is one P4 problem and one P1 call for the
curator.
 1. P1, SEL-1 (question for the curator, Must). The protected grounds kept are more than the definition's note names.
    The use-case actor may not use several of them for this decision: 29 CFR 38.5 and 38.6(b)(2) under WIOA sec. 188
    bar giving a different service on the basis of race, sex (pregnancy included, 38.7), national origin (limited
    English proficiency included, 38.9), age or disability. WIOA sec. 3(24) itself lists disability, age 55+, ex-offender
    status, English learners, AIAN/NH and single pregnant women as barriers to serve. It does not list sex or the other
    race and ethnicity groups.
 2. P4, LEAK-25 (Must). The source mixes "not employed" with "not recorded", and a label-free rule locates part of the
    "not recorded" rows. These are exits with an invalid or undisclosed SSN (PIRL 935 = 1) and no pre-entry wage record
    (PIRL 1700-1702 all blank): 19,556 exits, 2.2% employed (0.0% in NJ, 0.1% in AR and ID). Invalid SSNs with a
    pre-entry wage record are employed at 66.3% (73.3% with a positive wage), and valid SSNs without one at 41.7%.
    LightGBM finds them through PIRL 935 (predicted 0.05 to 0.08 against 0.34 to 0.38 without PIRL 935). They add
    +0.0014, +0.0014 and +0.0021 ROC AUC on the three windows. American Samoa's 120 exits (all No, wage records not
    matched) are the same mechanism. Mildest remedy: drop the located rows (LEAK-25 "recovered"). The alternative is
    to keep them under USE-5 with a note, if the curator reads the target as DOL's measured indicator, which counts
    them as not employed.
 3. P4, LEAK-10 (weak). PIRL 935 code 2 "Retirement" has no time attached: 1,871 exits, 31.0% employed, median age
    63. A note is enough.
 4. P7, cleaning (Should). The definition does not say why it keeps codes that only mean unknown as levels (CLEAN-10,
    CLEAN-12 table). This affects 21 items, about 30 million cells. PIRL 412 has 156 impossible tenures (CLEAN-11).
    The "undocumented" codes may be documented in the PIRL 2025 schema (CLEAN-11). SOC, NAICS and CIP codes are not
    decoded and their disclosure-coarsened parents sit beside their children (CLEAN-12). PIRL 303, 1328 and 3004 are
    ordinal candidates (CLEAN-14). CLEAN-5 is applied inconsistently to the CALC recodes.
The dtype probe (re-run, same 18 flags as the builder's) is answered below: all 18 typings are right.

**WHAT I READ AND RAN**
Read: dataset.py; builder_report.md; claims.md; the probe outputs; the PY 2025 Q3 record layout (layout.txt, Appendix
A, element by element for every shipped item); Appendices B and C (every all-state cleaning action, and the rows for
PIRL 207, 208, 931, 935, 1110, 1111, 1221, 1222, 1410, 2516); principles.md, use_case.md, leak_checks.md,
cleaning_features.md and SEL-1 (the batch branch's copies); 29 CFR 38.5, 38.6, 38.7 and 38.9 (LII); 29 USC 3102(24) (LII).
Ran (in the run's panel folder):
  load_clean.py: the definition's own _load_raw and _clean on all 7,373,493 exits (clean_full.parquet), with no
    row budget, so every count below is on the full cohort unless stated.
  profile.py: profile.csv, one row per column. It gives the dtype, levels, blank share, the employment rate when blank
    and when present, and for each date the count after the exit, before the entry and equal to the exit.
  located_effect.py: located_effect.csv. LightGBM (300 trees, 63 leaves) is fit on 400k random exits before each
    window's 9-month gap and scored on the whole quarter of the window. Variants: all features, and without PIRL 935.
    AUC is scored on all test rows and without the located rows.
  dtype_probes.py wioa_employment_after_exit_1m --no-fetch: dtype_probe/ (18 of 145 non-date columns flagged, the
    same 18 as probes/flagged.csv).
  One read of WIOAPUDFPY25Q3.parquet for PIRL 923, 1602 and CALC 4013 (the cohort's exclusions).

**COLUMN TABLE**
Prediction point: the exit (PIRL 901). That is the last service that is not self-service, information-only or
follow-up. The exit is dated back once 90 days pass without a service (20 CFR 677.150(c)). "Known" means known at that
point. Rates are the share employed in quarter 2 (base 0.679), written as present / blank. "After exit" counts dates
later than PIRL 901 in the shipped frame. All 71 date columns were checked: none has a value after the exit except PIRL
304 (2,197 planned separations).

column | meaning (layout) | known at exit? | dtype and cleaning | verdict | rule
--- identifiers, places
pirl105/106/107_special_project_id_1/2/3 | DOL special-project or grant id (107 also the pay-for-performance provider
  id); blank when fewer than 3 participants a year | yes, set at enrolment or funding | category, 139/43/46 levels,
  99.7-99.98% blank | fine | CLEAN-14
pirl108a/b/c_local_board_1st/2nd/3rd | ETA local board code; 99999 = liable state record | yes | category 589/367/138
  levels | fine (60005 = American Samoa, see problem 2) | CLEAN-14
state (CALC 4000) | state postal code from the WIPS file id | yes | category, 56 levels | fine (AS 120 exits, all No:
  problem 2) | CLEAN-14
--- demographics (Section A, recorded at entry, not updated)
pirl201_sex | 1 male, 2 female, 9 did not self-identify (SPRA filled blanks with 9) | yes | category, "Did not
  self-identify" 111,762 kept as a level with no other blank | SEL-1 question; cleaning minor | SEL-1, CLEAN-10
pirl202_disability | ADA disability, Yes/No/did not self-identify (894,088) | yes | category | SEL-1; CLEAN-10 minor |
  SEL-1, CLEAN-10
pirl204/205/206_disability_*_services | SDDA, LSMHA and Medicaid HCBS services (disabled only) | yes | 0/1 category,
  94.1% blank (not disabled) | SEL-1 (disability) | SEL-1, CLEAN-14
pirl207_disability_work_setting | work setting of a person with a disability (CIE, supported, sheltered, not employed)
  | yes, Section A. The element says "is working" with no time. Measured against PIRL 400: CIE with unemployed at entry
  4,326 rows, rate 0.611; not employed with unemployed at entry 0.537; CIE with employed at entry 0.800. No sign of
  an update after the exit | category, unordered (nominal) | fine; SEL-1 | LEAK-10 (checked), SEL-1
pirl208_disability_customized_employment_services | CES type received "to attain most recent or current employment";
  code 4 "secured employment ... with extended support" | yes, a service during participation. Code 4 (about 450
  rows) has a rate of 0.565, not an outcome's | category | fine; SEL-1 | LEAK-10 (checked), SEL-1
pirl209_disability_financial_capability_services | benefit planning or asset services | yes | category | fine; SEL-1
  | SEL-1
pirl210..215 (hispanic_latino, american_indian_alaska_native, asian, black_african_american,
  native_hawaiian_pacific_islander, white) | self-identified ethnicity and races, Yes/No/did not self-identify
  (931,131 to 1,636,018 per item) | yes | category; the unknown level has no other blank | SEL-1 question; CLEAN-10
  minor | SEL-1, CLEAN-10
pirl939_disability_iep, pirl940_disability_section_504_plan | current or previous IEP; Section 504 plan (youth with a
  disability; 939's blank also means "neither") | yes | category | SEL-1 (disability) | SEL-1
calc4021..calc4029 (no_disability, the 7 types, type_not_disclosed) | flags spelled out from PIRL 203 | yes |
  0/1 category. CALC 4021 = 1 exactly when PIRL 202 = No, a recode | SEL-1; CLEAN-5 consistency (problem 8) |
  SEL-1, CLEAN-5
age_at_entry (CALC 4039) | integer age from birth date and entry date | yes | float, 13-99. 282 exits at 13, 6,596
  under 16 (rate 0.240), 8 at 99. Plausible for Wagner-Peyser; no change | SEL-1 (age) | SEL-1
--- veterans (recorded at entry; veterans have priority of service under WIOA, a legitimate input)
pirl300_veteran | 1/0/9 "status not known" (189,484; SPRA filled blanks with 9) | yes | category; unknown level kept
  | fine; CLEAN-10 minor | CLEAN-10
pirl301_eligible_veteran_status | <=180 days / eligible veteran / other eligible person / no | yes | category. Code 9
  (11,565) set missing: 11,563 of them have PIRL 300 = No, so nothing is lost | fine | CLEAN-11
pirl302_campaign_veteran; pirl305_transitioning_service_member; pirl307_tap_workshop_prior_3_years;
  pirl309_hvrp_participant; pirl315_other_significant_barrier; pirl316_active_duty_military_spouse | 0/1 flags (302 9
  and 316 2 set missing, 8 and 108 rows) | yes | 0/1 category | fine | CLEAN-14, CLEAN-11 (problem 9)
pirl303_disabled_veteran | No / Yes (any rating) / Yes, special disabled (30%+ or 10-20% with a serious employment
  handicap) | yes | category, unordered. The layout ranks the levels by severity: an ordinal candidate | fine; CLEAN-14
  minor; SEL-1 (disability) | CLEAN-14, SEL-1
pirl304_date_military_separation | separation date; 2,197 after the exit (TSMs' planned separation) | yes, as a
  planned date at entry | datetime | fine | LEAK-10 (checked)
pirl306_date_covered_person_entry | first contact with the workforce system | yes (never after the exit) | datetime |
  fine |
pirl310_hvrp_grantee_1, pirl311_hvrp_grantee_2 | first 5 digits of the HVRP grant number. 310 holds 103 zeros and
  841 short values (fills) | yes | category | fine | CLEAN-14
pirl312/314_hvrp_reason_grantee_2/3 | why a 2nd or 3rd HVRP grantee serves the person | yes | category, 132 and 102
  rows. 314 is set on 93 rows whose 2nd grantee (311) is blank, and the 3rd grantee (313) was dropped as near-empty:
  a data inconsistency, harmless | fine | CLEAN-5
pirl1005, 1213..1222 (the DVOP service dates), pirl1006_date_referred_va_vre | last DVOP services, referrals and
  entered federal (contractor) jobs; VA VR&E referral | yes, 0 after the exit | datetime | fine (1221/1222: see 1110)
  | LEAK-10 (checked)
pirl1114_referred_to_jvsg, pirl1115_referred_to_va_services, pirl3005_tsm_warm_handover, pirl3006_tsm_housing_plan,
  pirl3007_referred_from_va | JVSG and VA referral codes; TSM items (1114 code 5 set missing, 695 rows) | yes |
  category | fine (1115 and 3007 VR&E levels are disability proxies) | CLEAN-12, CLEAN-11 (problem 9)
--- employment and education at entry
pirl400_employment_status_at_entry | employed / employed with notice / not in labor force / unemployed | yes | category,
  nominal | fine | CLEAN-14
pirl402_long_term_unemployed_at_entry | 27+ weeks unemployed (code 2 set missing, 634) | yes | 0/1 category | fine |
  CLEAN-11
pirl403_occupation_prior_employment | O*NET-SOC of the last job before entry, coarsened to 3 or 2 digits for
  disclosure (3.6% of codes) | yes | category, 980 codes, 65% blank. The SOC titles are not decoded | fine; CLEAN-12
  question (problem 7) | CLEAN-12, CLEAN-14
pirl404/405/406_industry_1st/2nd/3rd_quarter_prior | NAICS of employment in the 1st-3rd quarter before entry; 999999 =
  wages exist, NAICS unknown (375,521 in 404); blank = no wages (SPRA); coarsened for disclosure (2.5% of 404's codes
  at 4 digits or coarser; 223 parent codes sit beside their own children) | yes (quarters before entry) | category
  1,322-1,324 codes. The blank is the natural "no prior employment" (rate 0.743 present / 0.526 blank) | fine; CLEAN-12
  question (problem 7) | CLEAN-12, LEAK-10 (checked)
pirl407_highest_school_grade_at_entry | grades completed 0-12 (SPRA filled 12 from PIRL 408 and 409) | yes | float,
  0-12 | fine | CLEAN-14
pirl408_highest_education_level_at_entry | 9 levels | yes | category, unordered. A partial order (diploma,
  equivalency and IEP certificate not ranked; 4 and 5 not ranked); the note names why | fine | CLEAN-14
pirl409_school_status_at_entry | 6 states mixing attendance and attainment | yes | category, unordered (two
  dimensions, noted) | fine | CLEAN-14
pirl410_date_actual_dislocation | last day at the dislocation job (SPRA blanked dates after the exit) | yes | datetime,
  0 after the exit | fine |
pirl412_tenure_months_at_separation | months with the employer of record | yes | float 0-999. 156 tenures are longer
  than (age - 14) years, impossible; the 16 at 999 (a fill) are among them | cleaning problem (problem 6) | CLEAN-11
pirl413_msfw_designation, pirl808_eligible_msfw_status | farmworker designations | yes | category | fine | CLEAN-12
--- public assistance and barriers (at entry)
pirl600_tanf, 603_snap, 604_other_public_assistance, 702_youth_needs_additional_assistance, 704_foster_care_youth,
  800_homeless_at_entry, 802_low_income_at_entry, 804_basic_skills_deficient, 807_displaced_homemaker,
  2413_incarcerated_at_entry | 0/1 flags | yes | 0/1 category | fine | CLEAN-14
pirl601_exhausting_tanf_within_2_years | Yes/No/"Not applicable" (2,958,049; a state of its own, kept rightly) | yes
  | category | fine | CLEAN-10
pirl602_ssi_ssdi | SSI, SSDI and ticket-holder combinations | yes | category, nominal | fine; disability proxy
  (SEL-1) | SEL-1
pirl701_pregnant_or_parenting_youth | pregnant or parenting youth | yes | 0/1 category | SEL-1: sex includes
  pregnancy under 29 CFR 38.7. Not in the definition's note | SEL-1
pirl801_ex_offender_at_entry | Yes/No/did not disclose (1,465,331) | yes | category | SEL-1 (named in the note;
  a WIOA barrier, not a 29 CFR 38 ground); CLEAN-10 minor | SEL-1, CLEAN-10
pirl803_english_language_learner | ELL at entry | yes | 0/1 category | SEL-1: national origin includes limited English
  proficiency under 29 CFR 38.9 (also a WIOA barrier). Not in the note | SEL-1
pirl805_cultural_barriers, pirl806_single_parent | Yes/No/did not self-identify (2,268,489; 1,824,179) | yes |
  category | fine; CLEAN-10 minor | CLEAN-10
pirl2414_date_released_from_incarceration | release date; blank while still incarcerated at exit | yes (38 values, 0
  after the exit) | datetime | fine (criminal record proxy, SEL-1 note) |
--- programme participation and funding
pirl900_date_program_entry, pirl901_date_program_exit | entry; exit (the split's time column, also an input) | yes |
  datetime | fine. The span entry-to-exit ends at the prediction point. Its end is set by the last service, which a job
  found before the exit can bring forward: that is information held at the exit. There is no weight, so LEAK-41 does
  not apply | LEAK-10 third clause (checked), LEAK-41 (n/a)
pirl903/904/905 (wioa_adult, wioa_dislocated_worker, wioa_youth) | local, statewide or both funding | yes, funding
  over the participation | category | fine | CLEAN-12
calc4001/4002/4003/4004/4005 (funding stream flags) | DOL recodes of 903, 904 or 909, 905, 2003 (a grant number) and
  918 (= 1) | yes | 0/1 category. 4001, 4003 and 4005 are exact coarsenings, checked | fine; CLEAN-5 consistency
  (problem 8) | CLEAN-5
pirl906_date_first_youth_service, pirl933_date_first_dwg_service, pirl2001_date_completion_dwg_services | first youth
  or DWG service; last DWG service | yes, 0 after the exit | datetime | fine |
pirl907_incumbent_worker_training | funding of incumbent worker training (code 7 set missing, 32) | yes | category |
  fine | CLEAN-11
pirl908, 909, 910, 911, 914, 916, 917, 918, 932 (rapid response, RR additional assistance, adult education, Job Corps,
  veterans' programmes, vocational education, vocational rehabilitation, Wagner-Peyser, national DWG) | co-enrolment
  codes with 9 = "grantee is unable to track enrollment" | yes | category. "Unknown" kept as a level: 538,071 /
  5,210 / 4,440,188 (60%) / 61,304 / 7,490 / 579,532 / 5,486,208 (74%) / 27,357 / 3,277,756 (44%) | fine for 908, 909,
  911, 914 and 916, whose blank means "not applicable" (keep the level, say why); CLEAN-10 for 910, 917, 918 and 932
  (no other blank: missing is lossless) (problem 5). 917 is a disability proxy | CLEAN-10, CLEAN-12
pirl912_nfjp_grant, pirl919_youthbuild_grant, pirl936_reentry_employment_adult_grant, pirl938_h1b_grant,
  pirl2003_dwg_grant, pirl934_rapid_response_event | grant or event numbers; all-9 = grant unknown (a served-but-unknown
  level, kept rightly) | yes | category (16/20/3/8/195/3,905 levels) | fine (936: criminal record proxy) | CLEAN-14
pirl913_indian_native_american_programs | 1 or blank (blank = not served) | yes | 0/1 category, constant on non-blank
  (286 rows); the builder proposes accepting the warning | fine | CLEAN-5
pirl921_snap_employment_training, pirl930_pay_for_performance | 0/1 flags | yes | 0/1 category | fine | CLEAN-14
pirl922_other_programs | other programmes; code 2 = I/DD, MH or disability programmes (51) | yes | category | fine |
pirl931_registered_apprenticeship | entered a registered apprenticeship during participation, or an apprentice at entry
  (layout 1/0/9). The files hold 1 (11,424, rate 0.871), 2 (206, 0.825), 3 (3,677, 0.718), 4 (5,323,858, 0.670), and
  blank for whole states (NY, MI, TX, NJ, MS, KY, WV: 2,034,328) | yes by its definition (within participation) |
  category, undocumented codes kept with a note | fine | CLEAN-12
pirl935_accountability_exit_status | 1 invalid or undisclosed SSN (446,315, rate 0.635), 2 retirement (1,871,
  0.310), 0 none | code 1: yes (SSN status, entry). Code 2: an exit status with no time stated | category | code 1 is the
  key to the LEAK-25 shortcut (problem 2); code 2 is a weak LEAK-10 question (problem 3) | LEAK-25, LEAK-10
--- services and their dates (Section C)
pirl1000_date_first_self_service | first self-service date; later than the exit set missing (58,248) | yes after the
  mask (masked-missing flag ROC AUC 0.5003, builder) | datetime | fine | LEAK-10, LEAK-7
pirl1001, 1003, 1004, 1102, 1104, 1105, 1106, 1107, 1108, 1109, 1113, 1116 (first and last staff-assisted basic and
  career services, referrals, placement in federal training) | yes, 0 after the exit | datetime | fine | LEAK-10
  (checked)
pirl1110/1111_date_last_entered_federal_job/contractor_job (and DVOP 1221/1222) | the person entered a federal or
  federal-contractor job. This is an employment event, not a service, so it does not set the exit | yes as shipped: 0
  after the exit in all three files. 1110 is set for 49.8% of TX and 34.5% of GA exits, 407,498 of 496k equal to the
  exit date. Its rate with/without within TX is 0.670/0.644 and pooled 0.679/0.679: a state recording practice, not an
  outcome | datetime | fine. A job entered before the exit is known (USE-6). Revisit if a later file shows dates after
  the exit | LEAK-10 (checked), USE-6
pirl1200, 1201, 1202, 1203, 1206, 1207, 1210 (individualized services, employment plan, work experience, financial
  literacy, ESL, pre-vocational) | yes, 0 after the exit (SPRA blanked 1200 after the exit) | datetime | fine (1207
  ESL is an LEP proxy) | LEAK-10
pirl1205_type_of_work_experience, pirl1211_transitional_job, pirl3004_individualized_services_virtual | type of work
  experience; transitional job; delivery mode | yes | category / 0/1 / category. 3004 (in-person < mix < virtual) is an
  ordinal candidate | fine; CLEAN-14 minor | CLEAN-14
pirl1300..1333 (received_training; provider name; entry dates, types, SOC codes, completion flags and dates of
  trainings 1-3; ITA; Pell; virtual; postsecondary during programme; private-sector training) | training during
  participation | yes, every date 0 after the exit (1308 equals the exit for 145,388) | 1301 string (14,783 names; "NA"
  and "n/a" blanked); 1303/1310/1315 category; 1305 CIP and 1306/1311/1316 SOC category (85 CIP values below 10000,
  leading zeros lost, harmless as a category); 1307/1312/1317/1319/1320/1332/1333 0/1 category; 1328 category (ordinal
  candidate) | fine; CLEAN-12 and CLEAN-14 minor | LEAK-10, CLEAN-12, CLEAN-14
calc4030..4038 (study toward ...) | DOL flags from PIRL 1304, the programme of study | yes | 0/1 category | fine |
pirl1401, 1402, 1403, 1405, 1407, 1408, 1411, 1413, 1414, 1415, 1416 (youth services) | yes, 0 after the exit (SPRA set
  1416 to the exit when later) | datetime / 0/1 | fine | LEAK-10
pirl1409_date_last_supportive_services | later than the exit set missing (2,751) | yes after the mask | datetime |
  fine | LEAK-10, LEAK-7
pirl1410_date_last_adult_mentoring | the layout says mentoring "may occur both during and after program participation";
  0 after the exit in the data | yes as shipped | datetime | fine; mask it like 1409 for robustness (no cost) | LEAK-10
pirl1500_needs_related_payments, pirl1501_date_last_rapid_response_services | yes, 0 after the exit | 0/1 / datetime |
  fine |
pirl1806..1810 (skill gains) | later than the exit set missing (1,629 / 2,587 / 1,651 / 6,963 / 24,472) | yes after
  the mask | datetime | fine | LEAK-10, LEAK-7
pirl1811/1813_date_enrolled/completed_credential_program | enrolled or completed during participation | yes, 0 after
  the exit | datetime | fine | LEAK-10
pirl1812_school_status_at_exit | school status at exit | yes (at the exit) | category, unordered (two dimensions) |
  fine | CLEAN-14
pirl2004_disaster_recovery_dwg | disaster DWG service mix | yes | category | fine |
pirl2516_date_postsecondary_placement | placement into postsecondary education or training. An outcome-like event
  (counts for the Youth indicator) | yes as shipped: 0 after the exit, 99 equal to it, 36k set (rate 0.831) | datetime
  | fine; mask it like 1409 for robustness | LEAK-10
--- wages before entry
pirl1700/1701/1702_wages_3rd/2nd/1st_quarter_before_entry | UI wage-record earnings of the quarters before the entry
  quarter, rounded and randomly altered. SPRA set blank to 0 for adult and DW exiters and set values >= 999999 to
  blank | yes. The quarter before entry may reach the wage records after a same-day exit (51% of exits have entry =
  exit) but before the 90-day exit determination. No outcome link | float. No sentinel cluster (3-6 values above
  990k); 0 for 1.03-1.14M. Blank 8.1-8.8% (rate 0.456-0.504 blank against 0.70 present): blank marks "no wage-record
  match", which shares its cause with an unmatched outcome (problem 2) | fine as a column; the shortcut is problem 2 |
  LEAK-25, PROV-3
--- target
employed_2nd_quarter_after_exit (CALC 4013 = PIRL 1602) | wages > 0 in quarter 2 after the exit quarter, else 0;
  unmatched and "not yet available" codes set to 0 by SPRA once data are due | the outcome | category No/Yes ("Yes"
  the event) | problem 2 for the unmatched part | LEAK-25, USE-5, CLEAN-25
Dropped by the definition, checked: PIRL 100 (id), 1600-1618, 1703-1706, 1800-1805, 1814, 1900, 1901, 1406, 1412, 1503,
2002, CALC 4014-4019 (outcomes after the exit), 1002, 1007, 1100, 1101, 1103 (contact dates past the exit), 203, 313, 920,
923, 937, CALC 4006-4012, 4020, 4040, 4041 (copies or constants). None of the CALC items kept is computed from data after
the exit: 4000 from the file id, 4001-4005 from funding items, 4021-4029 from PIRL 203, 4030-4038 from PIRL 1304, and
4039 from birth and entry dates.

**DTYPE PROBE FLAGS (re-run; 18 of 145 non-date columns, identical to the builder's probes/flagged.csv)**
  ordinal_like: pirl408 (partial order, kept unordered with the reason in the notes: right), pirl409 and pirl1812
    (attendance and attainment mixed: two dimensions, unordered is right). pirl207 (work settings are nominal; the
    "open_end" flag on "Two or more settings" is a combination level, not a cut count: right as is).
  numeric_levels: pirl108a/b/c (board codes), pirl310/311 (grant numbers), pirl403 and pirl1306/1311/1316 (SOC),
    pirl404-406 (NAICS), pirl1305 (CIP), pirl931 (undocumented codes): codes, so category is right. A NAICS or SOC
    prefix carries the sector; see problem 7 for the hierarchy, not the dtype.
  Not flagged but checked: every 0/1 column is a yes/no flag in the layout (no count among them); pirl407, 412,
  1700-1702 and age are quantities, numeric; all 71 dates are datetimes; the target is No/Yes.

**PROBLEMS, RANKED BY principles.md (P1 first, then Must before Should, then size)**
1. P1, SEL-1 (Must; question for the curator). Protected grounds as inputs to a decision about whom to help.
   Evidence:
   * The use case names the actor and the decision: "a state workforce agency ... to decide whom to offer follow-up
     services". WIOA sec. 188's rules, 29 CFR 38.5, bar a WIOA Title I-financially assisted programme from
     discriminating on race, color, religion, sex, national origin, age, disability or political affiliation or
     belief. 38.6(b)(2) bars providing "any aid, benefit, service, or training that is different, or is provided in a
     different manner" on those bases. 38.7(a): sex "includes ... pregnancy, childbirth, and related medical
     conditions". 38.9: national origin includes limited English proficiency.
   * WIOA sec. 3(24) (29 USC 3102(24)) lists the "individuals with barriers to employment" the system is to serve:
     displaced homemakers, low income, Indians, Alaska Natives and Native Hawaiians, people with disabilities, people
     aged 55+, ex-offenders, the homeless, foster youth, English learners and people facing cultural barriers,
     farmworkers, people near TANF exhaustion, single parents including single pregnant women, and the long-term
     unemployed. Sex and the other race and ethnicity groups (Hispanic, Asian, Black, White) are not on it.
   * The definition's note names race, ethnicity, sex, disability and ex-offender status, and age appears in the
     builder's issue. The shipped grounds and proxies are more:
       race and ethnicity: pirl210-215;
       sex: pirl201, plus pregnancy in pirl701;
       national origin / LEP: pirl803, and pirl1207 (ESL services);
       age: age_at_entry, plus the youth items (pirl905, calc4003, 906, 701-704, 1401-1416), which run by age;
       disability: pirl202, 204-209, 939, 940, calc4021-4029, plus the proxies pirl303 (disabled veteran), 602
       (SSI/SSDI), 917 (VR), 922 code 2, 1006/1115/3007 (VR&E);
       criminal record (a WIOA barrier, not a 29 CFR 38 ground): pirl801, 2413, 2414, 936.
     Veteran status is used for priority of service under WIOA, so it is a legitimate input.
   * Precedent: the tension row "a rating factor ... the actor may no longer use" (bemtpl97 and the insurance family
     drop sex) decides by the actor's legal constraint. DOL's statistical adjustment model (TEGL 26-15 Att. II) uses
     these variables to set state targets on aggregates, which is another decision.
   Options, mildest first:
     (a) keep, with the note completed to list every column above (the builder's recommendation);
     (b) drop race and ethnicity (pirl210, 212, 213, 215; and 211 and 214 unless kept as WIOA's AIAN/NH barrier
         group) and sex (pirl201). These are grounds the actor may not use and WIOA does not name as barriers. Keep the
         barrier grounds (disability, age, ex-offender, LEP; pregnant or parenting youth is also a WIOA youth
         eligibility category) that WIOA directs services to;
     (c) drop every 29 CFR 38 ground (race, sex with 701, LEP 803, age, disability items) and keep ex-offender.
   Whichever is chosen, the note in curation_comments should list every column it covers. The domain practitioner's
   report measures the cost of (c)-like drops (ROC AUC -0.010 to -0.015, mostly age). I did not re-measure it.

2. P4, LEAK-25 (Must; fix in the definition, or a USE-5 call). "Not employed" is mixed with "not recorded", and a
   label-free rule locates part of the unrecorded rows.
   Evidence:
   * Appendix B (all states): PIRL 1602 is set to 0 "for those who have exited" when the person "is not found in the
     wage records ... unless non UI verification". A person without a usable SSN cannot be found.
   * Exits with PIRL 935 = "Invalid or undisclosed SSN" and all three pre-entry wages blank number 19,556 (0.27%), with
     2.2% employed: NJ 2,265 at 0.000, AR 1,789 at 0.001, ID 1,178 at 0.001, KS 1,003 at 0.002, MT 1,816 at 0.004,
     OR 3,648 at 0.027, TX 3,399 at 0.040. For comparison:
       invalid SSN with a positive pre-entry wage: 367,310 at 0.733;
       invalid SSN with all-zero wages: 59,428 at 0.234 (SPRA's blank-to-0 fill for adult and DW exiters makes some of
       these the same unmatched case, not locatable);
       valid SSN without any pre-entry wage: 402,439 at 0.417 (a mix, not locatable).
   * Test windows: 1,188, 1,091 and 1,707 such exits (2025Q1, 2024Q4, 2024Q3), at 2.2%, 2.2% and 1.1% employed.
     LightGBM, 400k training exits, predicts them at 0.048, 0.055 and 0.081, but at 0.37, 0.34 and 0.38 without PIRL
     935. With them the ROC AUC is 0.7181, 0.7314 and 0.7272; without them 0.7167, 0.7300 and 0.7250 (+0.0014,
     +0.0014, +0.0021 on the same predictions). Without PIRL 935 they still add +0.0012, +0.0011 and +0.0016, since
     the blank wages alone place them low. Dropping PIRL 935 costs 0.0015, 0.0018 and 0.0013 on all rows, and 0.0013,
     0.0015 and 0.0007 on the rows without them: code 1 with a wage record (rate 0.663 against 0.682) carries some
     honest signal too. One untuned fit per window. The paired differences come from the same predictions, so they have
     no seed noise.
   * American Samoa (state AS, board 60005): 120 exits, 0 employed. The definition already notes it as "maybe because
     its wage records are not matched": the same mechanism, located by state.
   Mildest remedy under LEAK-25: drop the located rows (PIRL 935 = 1 and PIRL 1700-1702 all blank; and state AS),
   with the counts in a decision table. Precedents: caracas_cervical_cancer, account_debt_south_africa,
   fraud_detection_in_electricity_and_gas_consumption_1m, where unrecorded rows located by a label-free rule were
   dropped. PIRL 935 then stays as an honest input (SSN status at entry). Name the unlocatable rest in the notes (the
   402k valid-SSN exits without a pre-entry wage record at 0.417; the 59k invalid-SSN zero-wage exits at 0.234).
   Alternative (the curator's call, USE-5): the target is DOL's measured indicator, which counts them as not employed,
   and the state is scored on it. Then keep with a note, and fit approximate already says the per-person decision is
   ours. The task_summary's `predicted` ("whether the person had unsubsidized employment") argues for the drop.

3. P4, LEAK-10 (weak, about 0.03% of rows; a note). PIRL 935 code 2 "Retirement" is an "Accountability Exit Status"
   with no time stated. If states record a retirement learned after the exit, it is a post-exit value. 1,871 exits,
   rate 0.310 (base 0.679), median age 63 (NY 524, NJ 252, CA 176). Remedy: a one-line note. Blanking code 2 is
   possible too, at no measurable cost.

4. P4, LEAK-22 (cohort, a note; outside the columns, found through the dropped PIRL 923). DOL's cohort (CALC 4013 not
   blank) leaves out the PIRL 923 exits (institutionalised, medical, deceased, called to active duty, and so on): 5,705
   of 3,686,872 exits in the PY 2025 Q3 range (0.15%). Their PIRL 1602 rates are 0.26 (institutionalised), 0.35
   (medical) and 0.12 (deceased). If a state codes 923 after the exit (a death during follow-up), the cohort is
   selected on the future: LEAK-22's framingham note keeps such rows with their No. The share is tiny and it is DOL's
   own denominator (USE-5). A note is enough.

5. P7, CLEAN-10 and the CLEAN-12 table (Should; no reason given). Codes that only mean unknown are kept as levels.
   "Did not self-identify" or "did not disclose" in pirl201, 202, 210-215, 801, 805 and 806, "status not known" in 300,
   and "Unknown" (the grantee cannot track enrollment) in 908, 909, 910, 911, 914, 916, 917, 918 and 932: 21 items,
   about 30 million cells on 7.37M exits. SPRA itself filled the blanks of 201 and 300 with 9. The CLEAN-12 precedent
   (ANES, 2026-11-01) set unknown codes missing in unordered codes too. Remedy, item by item:
     set to missing where the column has no other blank, so missing is lossless: 201, 202, 210-215, 300, 801, 805,
     806, 910, 917, 918, 932;
     keep the level with a note where the blank means "not applicable to this stream": 908, 909, 911, 914, 916.
   Or keep all with a note saying why (a refusal can be informative). The definition says nothing today.

6. P7, CLEAN-11 (Should). pirl412_tenure_months_at_separation has 156 of 61,253 tenures longer than (age - 14) years,
   the 16 values of 999 (83 years, a fill) among them. Remedy: set them to missing. The floor of 14 is my assumption;
   with 16 the count is 211.

7. P7, CLEAN-12 and CLEAN-14 (Should; open across datasets). SOC (403, 1306, 1311, 1316), NAICS (404-406) and CIP (1305)
   ship as codes, though their classifications give words. The disclosure coarsening (trailing zeros) makes a parent
   code an unrelated level beside its children: 223 NAICS parents in 404 co-occur with their own children, and 2.5%
   of 404's codes and 3.6% of 403's are coarsened. Mildest remedy: keep the codes, with a note naming the
   coarsening. Add the 2-digit sector or SOC major group as a column (CLEAN-12's "split ids that encode a group") only
   if the curator wants it across the batch. The precedent checker raised the same as D4 (rais 5, sinan 4); decide
   alike.

8. P7, CLEAN-5 consistency (minor). CALC 4041 is dropped as a copy of PIRL 914 (codes 1 or 2), while CALC 4001,
   4003 and 4005 are exact coarsenings of PIRL 903, 905 and 918 (checked: no disagreement) and stay, as does CALC 4021
   (= PIRL 202 "No"). Either is defensible (CLEAN-5 names exact copies only). Make it one way, or say why 4041
   differs.

9. P7, CLEAN-11 (minor). The codes set missing as "undocumented" (PIRL 301 9, 302 9, 303 9, 316 2, 402 2, 1114 5;
   11,825 values) belong to exactly the items the layout's overview lists with a "2025 Code Value" column (PIRL 2025
   schema: 301, 302, 303, 316, 402, 914, 1114, 1115, ...). That column is lost in layout.txt. Read it in the PDF before
   calling the codes invalid. 301's code 9 sits on non-veterans (11,563 of 11,565), so missing loses nothing there. The
   other counts are small.

10. P7, CLEAN-14 (minor). Ordinal candidates shipped unordered: pirl303 (No < Yes < Yes, special disabled: the
    layout's severity line) and pirl1328/3004 (In-person only < Mix < Virtual or online). Remedy: order them, or say
    why not.

Not problems (checked, no change):
  * No date column holds a value after the exit except PIRL 304's planned separations.
  * The masks of 1000, 1409 and 1806-1810 work.
  * 1110/1111/1221/1222 ("entered a federal job") and 2516 (postsecondary placement) are never after the exit. 1410
    (mentoring, "during and after") is never after it either. Masking 1410 and 2516 like 1409 would guard a future
    file at no cost.
  * pirl207 shows no post-exit update.
  * The decoded labels match the layout's codes for every item in CODE_LABELS. No reversed encodings: 201, 207, 301,
    303, 400, 408, 409, 602, 808, 907, 917, 935, 1114, 1115, 1205, 1303, 2004, 3005, 3006 and 3007 were read one by
    one.
  * The 0/1 flags are all flags; the counts and amounts are numeric.
  * The ids are dropped and no feature encodes the label or the person's earlier outcome.

Files, in the run's panel folder: (load_clean.py, profile.py, profile.csv, located_effect.py, located_effect.csv,
dtype_probe/) under this panel folder.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: wioa_employment_after_exit_1m (record wioa_employment_after_exit), 2026-11-09

VERDICT: right with notes.
The regime (temporal by exit date), the three quarterly windows, the 9-month gap and the train sides fit the use case
(a state agency deciding at a person's exit whom to offer follow-up). Nothing needs a re-split. The notes concern the
newest windows' labels being DOL's first or second report (weak LEAK-24, measured: it changes no comparison), the
gap's wording, the previous outcome of returning persons (USE-10, a call for the curator), and codings that differ
between the three source files.

Judgment record
  Validity: SPLIT-1/2/3 hold (temporal; persons and states are known entities, USE-10); SPLIT-14 holds (train sides
    66.8 / 58.6 / 51.0% of 7,373,493 exits); SPLIT-9 holds and needs at least a 6-month gap, SPLIT-10 met by the
    9-month gap; LEAK-24 triggered, weak (the newest window's labels are about 1 point low; ROC AUC -0.003 to -0.004;
    no model order changes): keep with a corrected note; SPLIT-13 / USE-10: the previous known outcome is legitimate
    and not shipped (+0.007 to +0.008 ROC AUC on returning persons, +0.001 overall): for the curator.
  Quality: SPLIT-20 note: the train sides mix three releases whose local-board coding differs (boards add <= 0.001).
  Title I only (issue 2): changes nothing about the split.

How it was checked (all numbers mine unless marked "builder")
  * Shipped splits read from the panel's participant kit (the _1m frame, 2,754,351 rows, and its splits): 3 repeats
    x 1 fold; train 1,000,000 / test 500,000 each. Train ends 2024-03-31, 2023-12-31 and 2023-09-30, test windows
    2025Q1, 2024Q4, 2024Q3, 275-276 days from the last train exit to the first test exit, no row on both sides. The
    minority class has 170,941-180,202 rows per shipped test window.
  * The full frame came from the prepared file, with the definition's youth-only filter (7,373,493 exits). Model runs
    use a float frame of the definition's columns: dates as days before the exit, masks as in the definition. All
    models are untuned LightGBM (400 trees, 127 leaves), with 1M random training rows and every exit of the window
    as test. Rerunning the same setting on another 1M sample moves ROC AUC by up to 0.004 (0.7214-0.7252 on
    2025Q1). Comparisons on one sample (a column added, labels swapped) are paired and much steadier.
  * Two more DOL files were downloaded to measure label maturity: PY 2025 Q1 and PY 2025 Q2 (parquet, from the
    national results page; PY 2025 Q4 is not published yet, checked 2026-11-09).
  * Scripts and outputs: the run's panel folder (scripts/e0..e10b, e*.json, e*.log).
  * Not run: the hidden-group probe. This is a temporal task, and the entity overlap is measured directly
    (findings 1 and 3).

FINDINGS, in rank order

1. (P3/P4; USE-10 Must, SPLIT-13 Should) Persons exit more than once. The use case treats them as known entities. The
   split is right; the history the actor has is not shipped.
   Evidence: 6,605,362 persons hold the 7,373,493 exits (state + encrypted id), and 768,131 exits have an earlier one.
   The ids are the same across all three files. On the 2023H1 exits that both the PY 2023 Q4 CSV and PY 2024 Q4 hold,
   96.5% match on state, id and exit date. Of the 2023H1 persons, 8.9% (CSV ids) and 8.8% (parquet ids) have a 2022
   exit. The builder's check was parquet-only.
   Per test window, the share of exits whose person's most recent earlier exit is 1, 2 or 3 quarters back (inside
   the gap) is 1.5-1.9%, 2.3-3.0% and 2.0-2.3%. The share 4 or more quarters back (on the train side) is
   8.3-10.4%.
   The earlier label is telling, and more so the closer it is:
     lag 1: employment rate 0.84-0.90 after an employed earlier exit, 0.19-0.24 after a non-employed one;
     lag 4 or more: 0.74-0.75 and 0.43-0.44.
   The person's "previous known outcome" is the label of the latest earlier exit at least 4 quarters back. That is
   what a state knows at the exit, and it never reaches a gap or test label. As a feature it gives (2025Q1 / 2024Q3
   windows):
     overall: ROC AUC 0.7252 -> 0.7260 / 0.7321 -> 0.7334;
     returning persons (79,936 / 62,258 test exits): 0.7575 -> 0.7645 / 0.7574 -> 0.7657;
     new persons: unchanged (-0.0008 / +0.0004).
   The builder's +0.001 holds overall, but it hides +0.007 to +0.008 on the 10-13% of test rows it concerns.
   Rule: USE-10 says that for a known entity the history is legitimate and the previous outcome is a feature
   (precedent tunisian_fraud_detection_challenge: built from the dropped id over strictly earlier periods). The split
   meets SPLIT-13 as it is.
   Mildest remedy, for the curator:
     (a) add `previous_known_outcome` (Yes / No / none) and the quarters since that exit, built from the dropped id
         and taken only from exits at least 4 quarters before the row's own exit quarter (no gap or test label can
         enter);
     (b) keep without it, with the subset gain in the person note.
   I lean to (a): the decision is per person, and the agency has this history. The decision is the curator's.

2. (P4; LEAK-24 Must, graded weak by measurement; the builder's issue 3) The test windows' labels are at different
   DOL report stages: 2025Q1 at its first report, 2024Q4 at its second, 2024Q3 at its third. The definition's note
   names only the newest window.
   Evidence: four releases (PY 2024 Q4, PY 2025 Q1, Q2, Q3), exits with a filled CALC 4013, youth-only exits removed.

   Employment rate of each exit quarter, by report (report number in brackets):
     2024Q2: 0.6647 (1st), 0.6688 (2nd), 0.6719 (3rd), 0.6739 (4th)
     2024Q3: 0.6463 (1st), 0.6519 (2nd), 0.6570 (3rd)
     2024Q4: 0.6528 (1st), 0.6581 (2nd)
     2025Q1: 0.6396 (1st)

   Label flips on rows matched on state, id and exit date:
     1st -> 2nd report, net +0.41 to +0.50 points:
       2024Q2: 2,574 No->Yes, 153 Yes->No (of 593,097)
       2024Q3: 2,735 No->Yes, 110 Yes->No (of 616,737)
       2024Q4: 3,473 No->Yes, 822 Yes->No (of 532,704)
     2nd -> 3rd report, net +0.06 to +0.32 points;
     3rd -> 4th report, net -0.04 to +0.03 points (2023Q4: +0.27).
   The CSV against PY 2024 Q4 for 2023H1 (1st/2nd report against the 4th/5th) shows the same pattern: 15,442
   No->Yes and 3,311 Yes->No, rate 0.683 -> 0.693 (youth-only exits not removed in this comparison).
   Over all rows the rate rises 0.7-1.1 points from the first report to the third (2024Q2 +0.92 by its
   fourth), and 0.5 points from the second report on. Part of that comes from the rows each release
   adds or re-keys: about 9-10% of a quarter's keys differ between PY 2025 Q2 and Q3. So 2025Q1 reads about 1 point
   low and 2024Q4 about 0.5 points low.

   Does it change the evaluation? Same training recipe, rows held in every report, labels swapped:
     2024Q3 window (562,872 rows): LightGBM 0.7312 / 0.7334 / 0.7341 on its 1st / 2nd / 3rd report labels, a
       change of -0.0029 for the 1st report (bootstrap SD 0.0002);
     2024Q4 window (532,706 rows): 0.7366 / 0.7410 on its 1st / 2nd report labels (-0.0043);
     on every label version the four models keep their order (LightGBM > 4-leaf LightGBM > linear > the wage alone);
     the LightGBM - linear gap moves by 0.0003 and 0.0010.
   The relabelled rows are ones the model already scores like employed persons: mean prediction 0.67-0.71 against
   0.70-0.72 for stayed-employed and 0.53-0.55 for stayed-not-employed.
   Reading: the outcome is slightly right-censored at the release end. It lowers the newest window's absolute score
   by about 0.003-0.004 and the second window's by about 0.001, and changes no comparison. Probe 13's rising "No"
   rate at the end is mostly drift (2023Q1 0.702, 2024Q1 0.685, 2025Q1 0.640), with about 1 point of immaturity.

   Rule and remedy:
     (a) Keep, with the note corrected (mildest; recommended). It should name all three windows' report stages and
         the numbers above. It should also say that PY 2025 Q4 brings 2025Q1 only to its second report (still
         about 0.5 points of rate to come, 0.06-0.32 points of it as flips on the same rows). Labels settle at
         about the third report, which is PY 2026 Q1. Re-source the windows' labels from that file (LEAK-24's own
         remedy) when it is out.
     (b) The builder's shift back one quarter (windows 2024Q2-2024Q4). This still leaves the newest window at its
         second report (about -0.001 against its third, as measured on 2024Q3). Without 2021 exits its oldest
         window trains on 47.3% of the rows, below the SPLIT-14 floor. Settling every window needs a shift of two
         quarters (windows 2024Q1-Q3; 42.4% without 2021). Either shift needs the PY 2022 Q4 file, whose 2021 exits
         have their outcomes in 2021Q3-2022Q2, the pandemic's tail (SPLIT-20; not measured). I would not take (b)
         for a 0.003 shift that reorders nothing.
   If the curator reads LEAK-24 as a Must whatever its size, the full fix is the two-quarter shift plus PY 2022 Q4.

3. (P4; SPLIT-9 Must holds, SPLIT-10 Should met) The 9-month gap is right. The splits_comment argues for it from a
   fact that would imply a longer one.
   Evidence:
   * SPLIT-9 needs at least 6 months. With a 3-month gap, 2.3-3.0% of the test exits would have their own person's
     exit from two quarters earlier on the train side. That label measures employment in the test quarter itself,
     after the test row's prediction point (rates 0.77-0.82 against 0.34-0.37). With no gap, the lag-1 labels measure
     the quarter after it (0.84-0.90 against 0.19-0.24).
   * With 9 months, the newest training exits are those of quarter Q-4. Their outcome quarter Q-2 ended 3 months
     before each window. The state's UI wage records for that quarter are due about a month after it ends
     (inference: the general UI reporting rule, not read in a source here), so a state agency has these labels at the
     window's start. A 6-month gap would admit outcome quarter Q-1, which ends on the window's first day, before
     its wage records arrive.
   * DOL's own first report of quarter Q-4 is the report of quarter Q, which comes after the window starts. So
     12.3%, 13.1% and 15.1% of the three train sides are exits DOL had not yet published at the window start. A
     12-month gap, matching DOL's fill, gives train shares 58.6 / 51.0 / 43.3%, and the oldest window would fall
     below the floor (Title I only: 64.1 / 57.1 / 49.4%).
   * What the gap costs, at equal training size (1M), LightGBM on all of the 2025Q1 window:
       without the exit date as an input: gap 0 0.7267, 3 0.7251, 6 0.7249, 9 0.7250, 12 0.7226 (all within the
         0.004 run-to-run spread);
       with the exit date as an input: gap 0 0.7299, 3 0.7154, 6 0.7200, 9 0.7229, 12 0.7209;
       2024Q3 window, with the exit date: gap 0 0.7361, 9 0.7330, 12 0.7293.
     So the labels a refit could not have had are worth up to +0.007, through the time feature. With the exit date
     as an input, which training quarter is newest makes scores move. Under the shipped gap the newest training
     quarters (2024Q1, 2023Q4, 2023Q3) hold no one-day batch closure (finding 5). That is a fact about the time
     feature, not about the split.
   * The outcome has a fixed horizon (the 2nd quarter after the exit quarter), so the gap selects no rows by their
     outcome. What sets this case apart from lt_vehicle_loan_default_prediction (gap 0) is that persons recur.
   Rule: SPLIT-9 (the test row's own person's labels set after its prediction point must not be in train) and
   SPLIT-10 (a gap of about the label's delay).
   Remedy, a wording fix with no change to the split: the splits_comment says "DOL's own files fill it four quarters
   after the exit quarter. So a model refit ... knows the outcomes ... up to the quarter that ended nine months
   before". Replace that with the state's wage-record timing. Add that DOL waits four quarters for interstate and
   supplemental matches, which turn about 0.5-1% of labels to employed later (finding 2), and that the gap also keeps
   every recurring person's later-measured label out of training. "No training label measures a quarter after the
   window's start" holds for a 6-month gap too, so it does not justify 9.

4. (P4; SPLIT-20 Should / quality) The train sides mix three releases, and some codings differ by release. The test
   windows all come from PY 2025 Q3.
   Evidence:
   * Train sides by file:
       2025Q1 window: 2.03M CSV, 1.73M PY 2024 Q4, 1.17M PY 2025 Q3;
       2024Q3 window: no PY 2025 Q3 row.
   * Local board (PIRL 108A): on rows matched across files, the same exit carries the same code in 68.6% (CSV vs PY
     2024 Q4), 85.3% (PY 2024 Q4 vs PY 2025 Q3) and 98.8% (PY 2025 Q1 vs Q3) of rows. The disagreements are a
     statewide code (ss903) against a local board, for example NV 32903 against 32005 / 32010, or NY 36015 against
     36903. The share of ss903 codes is 13-17% in the 2022 exits (CSV), 43-45% in 2023Q1-Q3 (PY 2024 Q4) and
     31-36% from 2023Q4 (PY 2025 Q3).
   * PIRL 108B is missing in 19%, 36% and 24% of rows in the same three blocks.
   * The altered wages before entry (PIRL 1700-1702) are re-drawn per release: equal on only 12-21% of matched rows,
     but Spearman 0.976-0.991 and median relative difference 0.45-0.5%. That is the same disclosure process,
     harmless.
   * Missing shares by quarter: only PIRL 108B, 108C, 931 and 301 (+2.7 points) step at a file boundary by more
     than twice their largest step elsewhere.
   * What it costs: the three local-board columns add +0.0006 (2025Q1) and +0.0011 (2024Q3) ROC AUC to LightGBM,
     within the run-to-run spread (another training sample than the other runs); as categoricals they lower it
     (0.7202 and 0.7263 against 0.7241 and 0.7313). So the drift in coding moves nothing measurable.
   * Also 423 pairs of exits of one person less than 90 days apart come from two different files (337 of them with
     the same entry date). DOL's file combines such records within a release. They are cross-release copies of one
     participation, all on train sides near the file boundaries (0.006% of rows): negligible.
   Remedy: a note under "Files" that local-board codes follow each release's statewide or board coding, and
   PIRL 108B's reporting too. No change needed.

5. (Outside the split, for the column auditor and the curator: USE-3 / PROV) One-day batch closures.
   Evidence:
   * Montana closed 10,122 exits on 2024-09-06, 316 times its median day. This is 1.6% of the 2024Q3 test window.
     99.9% of these exits are Wagner-Peyser only, with a median of 290 days since the last career service (0 for all
     exits; 28% over 365 days). Their employment rate is 0.624. Montana had only 102-609 exits a quarter in
     2023Q3-2024Q1, so this looks like a backlog closed at once.
   * The training data has the same kind: UT 2022-03-29 (11,337), TX 2022-08-31 (9,342), UT 2022-09-16 (2,963).
   * Across all rows, 0.24% have their last career service more than 365 days before the exit date. By PIRL 901 the
     exit is the last service date.
   Reading: the "prediction at exit" is nominal for these rows, but they are few and on both sides. Not a split
   problem.
   Mildest remedy: a note, or a filter on exits dated more than 90 days after the last service (decided on
   inputs, not the label).

6. (Issue 2, the alternative population) Title I only (adult, dislocated-worker or DWG funding: 1,098,270 exits)
   does not change the split's reading.
   Evidence:
   * Same windows and gap. Title I train sides are 71.1 / 64.1 / 57.1% of the Title I exits (floor met), and the
     test windows 74,729 / 75,286 / 79,207 exits (rates 0.687-0.694).
   * First-report revisions are of about the same size (Title I rate, 1st -> 2nd report: 2024Q2 +0.31, 2024Q3
     +0.72, 2024Q4 +0.01 points, against +0.41, +0.56 and +0.53 for all programmes).
   * Scores on the Title I test exits (2025Q1 / 2024Q4 / 2024Q3):
       LightGBM trained on Title I only: 0.7523 / 0.7605 / 0.7584;
       LightGBM trained on all programmes: 0.7461 / 0.7561 / 0.7531;
       all programmes on all exits: 0.7214 / 0.7368 / 0.7305;
       Wagner-Peyser-only exits: 0.7174 / 0.7337 / 0.7268;
       linear: 0.693-0.711 (Title I) against 0.660-0.678 (all).
   * The choice is about the population (USE-1, USE-8), not the split. Either way the same temporal split with the
     9-month gap is right.

CHECKS THAT PASSED
  * Regime: temporal by exit date (SPLIT-1, SPLIT-3). The actor decides at exit for the person in front of them, and
    states and local boards are known: all 55 test states are on every train side; Oklahoma is only in 2022, so on
    train sides only. 99.7-100% of test rows have their local board on the train side (one of 520 boards unseen in
    2024Q3). State and board are features, not groups (SPLIT-4).
  * Windows: three adjacent quarters (Jul 2024 to Mar 2025) of 593,923-632,327 exits each, 500k sampled for the
    shipped test. Each window has its own expanding train side; the shipped train samples overlap 76-88% through the
    shared random order. Train shares are 66.8 / 58.6 / 51.0%, so the floor holds, by one point for the oldest window
    (SPLIT-14). The train shares match the builder's.
  * Season: the windows cover Q3, Q4 and Q1. The rate shows a Q1 bump (+1.1 to +1.6 points over the neighbouring
    quarters) on a downward drift (0.718 in 2022Q1 to 0.657 in 2024Q3), and no window falls in an atypical season.
    Every train side holds at least 7 quarters, more than one full year (SPLIT-20).
  * COVID: the data starts with 2022Q1 exits, whose outcomes start in 2022Q3, so no pandemic quarter is in it. State
    mix drifts between train and test: NY -1.7, CA -1.7 and GA -1.5 points of share; MI +1.8 and CO +1.1. GA's exits
    halve from 2023Q3 and CO's double from 2023Q1. A temporal split carries this drift.
  * No training weight or time-on-risk.
  * No row is on both sides. Leak probe 5's exact feature copies across the split are 0.3% (builder).

FILES
  Work: the run's panel folder (scripts/, e0-e10b outputs, features.parquet 361 MB, dl_py25q1q2/ with the two
  downloaded DOL files, 1.1 GB; both can be deleted after the panel)

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

Actor played: a WIOA Title I case manager at an American Job Center (adult and dislocated-worker caseload), at case
closure: the last service is given and no more are planned. I decide whom to keep in services or to offer the follow-up
that 20 CFR 680.150(c) and 678.430(c) require to be "made available ... for a minimum of 12 months following the first
day of employment, to participants who are placed in unsubsidized employment". Second reading, as the use case words
it: a state workforce agency setting the employment rate expected of an exit cohort, as DOL's statistical adjustment
model does (20 CFR 677.170(c)). I checked both against the shipped frame and splits (participant kit) and the PY 2025
Q3 raw file.

**VERDICT**
Fit: APPROXIMATE (I agree with the definition). One sentence: for Title I exits the rows, the label's timing and the
  9-month-gap split mirror my case-closure and follow-up decision, but 84% of the rows are Wagner-Peyser job-service
  contacts where nobody makes that decision, the per-person use is ours (DOL decides on state aggregates), and inputs I
  always hold (whether I placed the person in a job, UI claimant status, true wages) are missing or altered in the
  public file.
Metric scores my decision: PARTLY. ROC AUC ranks, which my follow-up list needs, and the pooled score stays close to
  the score inside each local board (0.008 to 0.015 lower, same order of feature sets). It cannot see calibration,
  and calibration is the whole decision in the use case's second clause (the cohort's expected rate). There the model
  over-predicts the 2025Q1 cohort by 5.4 points while its AUC looks normal. Keep roc_auc if the use case is narrowed
  to my decision (recommended). Switch to log_loss if the cohort clause stays (MET-8).
Issue 1 (SEL-1, protected grounds): DROP sex, race/ethnicity, age and the disability items, KEEP ex-offender status.
  My own law bars the five grounds for this decision: WIOA sec. 188 and 29 CFR 38.5. DOL's own per-person model for
  allocating reemployment services bars exactly these elements (UIPL 41-94). Measured cost: ROC AUC -0.010 to -0.015
  pooled and -0.011 to -0.012 on Title I rows, mostly age by gain share (6.7-7.1% against 0.9-1.1% for the
  disability items; not dropped one at a time). Sex and race carry <= 0.0012.
Issue 2 (population): TITLE I (adult, dislocated worker, DWG) only, as the full version. Follow-up is a Title I
  obligation, and Wagner-Peyser-only exits are mostly one-day staff contacts with no case manager at closure. A model
  trained on Title I alone scores better on Title I test rows (+0.003 to +0.005 ROC AUC) from 158k-167k training rows
  against a 300k all-programme sample.
Issue 3 (LEAK-24, newest window): agree with the builder (keep with the note, refresh 2025Q1 from PY 2025 Q4). It
  does not touch my ranking. It adds to the cohort-rate miss that only matters to the target-setter.

Measurement setup (all numbers below unless stated otherwise): the shipped frame and splits of the participant kit
(3 windows: 2025Q1 = w0, 2024Q4 = w1, 2024Q3 = w2). Untuned LightGBM (500 trees, lr 0.05, 127 leaves) on a random
300k of each 1M train side. Dates enter as days before the exit, plus the exit month. Every test row of a window is
scored. Scripts and JSON are in the run's panel folder.

**1. AT THE MOMENT OF THE PREDICTION, DO I HAVE EACH INPUT?**
The moment. The definition says "the day a participant exits". In my system the exit is not an event on that day. It is
recorded once 90 days pass with no service and none planned, and then it is dated back to the last service (20 CFR
677.150(c)(1): the exit date "cannot be determined until at least 90 days have elapsed since the participant last
received services"). Layout PIRL 901 agrees: the "last date ... of services that are not self-service,
information-only, or follow up services ... only if there are no future services ... planned". So the real moment of my
decision is the last planned service (closure). The information set "everything up to the exit date" is exactly what I
hold then, so the shipped features are right. Only the wording should change (see 7, item 4).

Inputs I have at closure (every shipped feature, after the builder's drops):
  - Entry items: demographics, barriers, education, employment status at entry, prior occupation and industry, prior
    wages, veteran items. I have the TRUE prior wages from the UI wage records. The file's are "randomly altered", and
    they are the strongest inputs (gain share of PIRL 1702 + 1701 + 1700 = 0.119 + 0.077 + 0.052 = 25% in the w0 model).
    A model trained on altered wages and fed true ones in production may shift. This cannot be fixed and is already
    named in fit_reason.
  - Programmes, funding streams, local board, grants and project ids, the services and their dates up to closure,
    training type and completion, and school status at exit. All of these are known at closure.
  - Nothing shipped is unknown at closure. Small item for the column auditor: PIRL 935 code 2 "Retirement" (684
    shipped rows, rate 0.325) is an accountability exit status that may be recorded after the exit. It is negligible.

Inputs I always have that the dataset lacks, ranked by how much they matter for this decision:
  a. Whether I placed the person in a job at closure. Under 680.150(c) this is the trigger of follow-up, and in
     practice it is the main reason for a closure. PIRL has no employment-at-exit item for Title I; PIRL 2002 exists
     for DWGs only and is rightly dropped, being counted over the exit quarter. The raw file shows the gap's weight.
     On the PY 2025 Q3 cohort, the 6.4% of Title I exits with a follow-up date (PIRL 1503) were employed in Q1 after
     exit at 0.836 against 0.668 without, and in Q2 at 0.828 against 0.688. Follow-up goes to people already placed,
     as the rule says. This cannot be fixed. Name it in fit_reason.
  b. UI claimant status and the WPRS/RESEA profiling result. The layout (p. 3) says PIRL 401 "UC Eligible Status" and
     PIRL 1112 (UI claim assistance) "have been removed from the file entirely". This cannot be fixed. Name it.
  c. Residence (county, ZIP; also removed) and the local labour market at closure. DOL's own model uses the
     unemployment rate and industry job changes (677.170(c)(1)). BLS LAUS publishes the state unemployment rate by
     month, about a month late, so the curator could join it on state and exit month. This is optional (see 7). It
     bears on the drift of the rate from 0.718 (2022Q1) to 0.640 (2025Q1).
  d. The person's earlier exits and outcomes (USE-10). The builder measured +0.001 ROC AUC (prev_outcome_experiment),
     so this is not a gap in practice.

**2. IS THE TARGET WHAT I ACT ON?**
  - Yes, as the measured form. "Employed in the 2nd quarter after the exit quarter" (PIRL 1602, any UI wages in the
    quarter) is the primary indicator my local area is negotiated on and held to (WIOA sec. 116). Follow-up and
    case-closure decisions are made with it in view. What I care about underneath is job retention for those I placed
    and re-employment for those I did not. Q2-after-exit is the official version of both. It is not a proxy I would
    reject (USE-5 holds).
  - The youth-only drop is right (USE-5). For youth the Youth indicator counts education too, and youth follow-up is
    mandatory for all (20 CFR 681.580), so there is no choice of whom.
  - I want a probability: to rank my closures (who to keep or follow up) and, for the target-setter, to sum over a
    cohort. A class or a hard label is no use. No threshold or capacity is fixed anywhere. Follow-up use runs from 0.2%
    (25th percentile of states) to 4.7% (median) to 36.1% (90th percentile) of Title I exits (PY 2025 Q3, PIRL 1503).

**3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST DATA WHAT I FACE?**
  - Title I exits: yes. One exit is one closure and follow-up decision.
  - Wagner-Peyser-only exits: no decision of mine. They are 6,199,267 of 7,373,493 exits (84%), 2,308,756 of the
    2,754,351 shipped rows (83.8%), and 85.1% to 86.4% of each 500k test window. Title I rows are 58,862, 63,379 and
    63,306 per window (11.8-12.7%). Measured on the shipped frame:
      wp_only:  58.1% entry date = exit date (one-day participation), median 0 days, p90 65 days; 47.7% any
                individualized-service date; 28.4% an employment plan; 0.23% training; rate 0.664.
      title_I:  16.1% one-day, median 81 days, p90 375 days; 84.0% individualized; 54.0% a plan; 28.8% training;
                rate 0.709.
    Correction to the framing in the brief and builder issue 2 ("mostly self-service"): 100.0% of Wagner-Peyser-only
    exits have a staff-assisted service date (PIRL 1001), and 88.0% also self-served. Self-service-only users are
    reportable individuals, not participants (20 CFR 677.150(a)(3)(ii)), and the cohort excludes them. What these rows
    are is mostly a single staff contact (job search help, a referral) at a job-service office. No case manager closes
    a case, and 678.430(c) puts follow-up under "adult or dislocated worker workforce investment activities" only. In
    the raw file no Wagner-Peyser-only exit carries a follow-up date (0 of 3,065,763). Part of that is reporting design,
    since PIRL 1503 is required for Title I only.
  - The test data is what I face: next quarter's closures in my state, scored by a model refit on the outcomes known
    then. The 9-month gap matches when DOL's files fill the outcome (four quarters after the exit quarter). That is
    right (SPLIT-9).
  - The target-setter's unit is different: a programme's cohort per state or local area and program year, negotiated
    per programme (Adult, DW, Youth, WP separately). Pooling the programmes in one table does not stop that use, since
    predictions can be averaged over any cohort. But that actor decides at the cohort's resolution, not the row's
    (USE-5).

**4. WOULD I USE THIS MODEL? WHAT WOULD MAKE ME TRUST OR DISTRUST IT?**
I would use it as a triage aid for closures, ranking my Title I caseload by risk of no Q2 employment, under three
conditions.
  (i) It must not use sex, race, age or disability. I cannot defend a follow-up list built on them (section 4 below,
      issue 1).
  (ii) It must be trained on cases like mine. Trained on all programmes, it learns mostly from one-day job-service
       contacts. Trained on Title I alone it is better on my cases: 0.7428, 0.7502, 0.7523 against 0.7376, 0.7474,
       0.7486 ROC AUC on Title I test rows, with 158k-167k training rows against 300k.
  (iii) It must rank within my board, not only nationally. It does: within-board mean ROC AUC (V0, all rows; 281 to
        293 boards with >= 300 test rows) is 0.7135, 0.7174, 0.7222 against pooled 0.7215, 0.7326, 0.7302. The state
        alone, as its training rate, scores 0.578, 0.564, 0.545 pooled and 0.545, 0.523, 0.514 on Title I rows.
What makes it useful: on Title I rows, the 20% of each board's closures with the lowest predicted probability hold
  57.5%, 57.1%, 57.9% not employed in Q2 against 31.3%, 31.1%, 30.6% overall. Without the protected grounds it is
  55.5%, 54.5%, 55.4%: a lift of about 1.8 times either way.
What makes me distrust it: it does not know whom I placed (gap 1a); it learned on altered wages; and "state" is its
  3rd strongest input (gain share 0.079), which partly reflects how each state matches wage records (American Samoa's
  120 exits are all 0).

**5. DOES THE DECLARED METRIC SCORE MY DECISION? (roc_auc, fallback)**
  - For my decision (a ranked closure and follow-up list), a threshold-free ranking is right. No source fixes a k, a
    capacity or a cost: follow-up shares run from 0.2% to 36% across states, so MET-7 forbids inventing one, and a
    threshold metric is ruled out (MET-6). ROC AUC (MET-8) fits. AUPRC has no case: the minority class, not employed,
    is 31-36% of rows, and imbalance alone is no reason (MET-9).
  - The unit (MET-1). I rank within my local board, and the declared score pools all states. Measured, the pooled
    score is only 0.008-0.015 above the within-board mean, and the four feature sets I compared rank the same under
    both. So the pooled ROC AUC is an acceptable stand-in, and a grouped AUC (a new library metric, MET-13) is not
    worth adding.
  - The cohort clause of the use case ("to set the employment rate expected of its exit cohort") is a calibration
    decision: the sum of the probabilities must hit the realised rate. ROC AUC is blind to it. The V0 model's mean
    prediction is 0.694, 0.674, 0.673 against realised 0.640, 0.658, 0.657 (5.4, 1.6, 1.6 points over), with log
    loss 0.585, 0.560, 0.562 against 0.660, 0.645, 0.646 for the training rate. A proper rule (log_loss) would score
    this; ROC AUC cannot (MET-8; Gneiting & Raftery).
  - Verdict PARTLY. My choice: narrow the use case to the per-person decision and keep roc_auc. The cohort target is an
    aggregate actor's decision at another resolution (USE-5, 677.170: state-quarter aggregates). It is also the one
    decision where the protected grounds are lawful inputs, so keeping it in the same task conflicts with issue 1. If
    the curator keeps the clause, declare log_loss (MET-8, MET-11 fallback reason updated).

**6. THE BUILDER'S ISSUES, FROM THE ACTOR'S SIDE**
Issue 1, protected grounds (SEL-1, P1; the Tensions row "a factor the actor may no longer use", as the rais panel
extended it to decisions where the actor's own law bars the factor).
  - My law. WIOA sec. 188 and 29 CFR 38.5 forbid discrimination "on the basis of race, color, religion, sex, national
    origin, age, disability, or political affiliation or belief", and citizenship for "beneficiaries, applicants, and
    participants", in "any WIOA Title I-financially assisted program or activity". 38.2(a)(2) adds the one-stop
    partners' programmes run in the one-stop system. Follow-up and continued services are benefits of exactly that
    programme. So the precedent checker's distinguishing fact ("a benefit, not a job decision") does not set WIOA
    apart: the rule is written for benefits.
  - The closest precedent in my own field. For the per-person statistical model that picks which UI claimants get
    reemployment services (WPRS), DOL's UIPL 41-94 says "the following elements may not be used in the profiling
    system: age, race, ethnic group, sex, color, national origin, disability, religion, political affiliation and
    citizenship". That is the same agency, the same kind of decision (a person-level score allocating reemployment
    help) and the same list.
  - Why DOL's adjustment model may use them. It is a different decision at a different resolution: state-quarter
    aggregates, built to "adjust performance goals for States serving harder-to-serve populations" (DOL statistical
    model summary 2018; TEGL 26-15 Att. II). It protects a state that serves these groups. It does not rank persons.
    Its use does not carry over to my list.
  - Measured (ROC AUC per window w0, w1, w2; Title I rows in brackets):
      all features (V0)                       0.7215 0.7326 0.7302   [0.7376 0.7474 0.7486]
      minus sex and race/ethnicity (V1)       0.7215 0.7320 0.7290   [0.7366 0.7483 0.7482]
      minus also age and disability (V2)      0.7112 0.7175 0.7149   [0.7265 0.7354 0.7366]
      V2 minus ex-offender items (V3)         0.7119 0.7176 0.7154   [0.7268 0.7354 0.7370]
      V2 minus disability proxies (V4)        0.7115 0.7173 0.7150   [0.7262 0.7347 0.7361]
    The V0 gain shares are sex and race 2.0-2.1%, age 6.7-7.1%, disability 0.9-1.1%, ex-offender 0.3%.
  - What the grounds do to my list (Title I rows, lowest 20% per board): with V0, aged 55+ make up 35.3%, 33.5%,
    31.8% of the list against 17.1%, 16.6%, 16.0% of exits; with V2, 21.1%, 19.1%, 18.8%. Disability: V0 14.9%,
    14.0%, 14.4%, V2 12.0%, 10.7%, 11.2%, against 8.1%, 7.6%, 7.8% of exits. Black participants: V0 28.1%, 27.5%,
    27.5%, V2 30.1%, 30.0%, 28.3%, against 29.5%, 30.5%, 30.1%. 74-76% of the list is the same under V0 and V2. So the
    grounds move a quarter of my list, mostly by age, and that is a decision "on the basis of age". Older individuals
    and people with disabilities are WIOA barrier groups (29 USC 3102(24)(D),(E)), but a state gives them priority by
    policy, not through a score.
  - Recommendation (P1 wins, Tensions row "ethics against anything"): drop PIRL 201, PIRL 210-215, CALC 4039
    (age_at_entry), PIRL 202, PIRL 204-209, PIRL 939, PIRL 940 and CALC 4021-4029.
      * Drop the disability proxies too, at no measured cost (V4 against V2: -0.0002 to +0.0003). They are PIRL 602
        SSI/SSDI (SSDI is a disability benefit), PIRL 917 VR, PIRL 303 disabled veteran, PIRL 922 code 2 (I/DD and
        mental-health programmes) and PIRL 1114 code 3 (wounded, ill or injured). The alternative is to recode 922
        and 1114 so the disability codes go.
      * Keep PIRL 801, 2413 and 2414 (ex-offender, incarcerated, release date). Ex-offender status is not a section
        188 or 38.5 ground and is not in UIPL 41-94's list. It is a WIOA barrier group (3102(24)(F)) and one of the
        characteristics the adjustment model must account for (677.170(c)(2)(ix)). Dropping it moves ROC AUC by
        +0.0001 to +0.0007.
      * Rewrite the curation note that says DOL's model uses these characteristics so that it gives the reason they
        left (sec. 188, 29 CFR 38.5, UIPL 41-94). Update `known`.
      * Leave English-language learner and cultural barriers (PIRL 803, 805; national-origin proxies) in. They are
        statutory barriers the programme is told to serve (3102(24)(I)), and nothing bars them as such.
Issue 2, population. Choose Title I: CALC 4001, 4002 or 4004 set, 1,098,270 exits, rate 0.717, which fits without
  sub-sampling as the full version `wioa_employment_after_exit`. Reasons: the follow-up decision exists only there
  (678.430(c), 680.150(c)); one-day job-service contacts (58% of the Wagner-Peyser-only rows) are no closure anyone
  decides on; Title I training gives the better model for Title I cases; and the table is still large (above 1M rows,
  216 features). The builder's argument for all programmes ("DOL's indicator and targets cover Wagner-Peyser too")
  belongs to the target-setting actor, who works on aggregates (USE-5, USE-8). I found no per-person Wagner-Peyser
  decision at exit. RESEA targeting happens at the UI claim, with UI data the file removed. So the Wagner-Peyser rows
  should not become a second dataset without a named actor (USE-1, USE-2).
Issue 3, newest window. Agree with the builder's recommendation. For a ranking metric it is invisible. For the cohort
  clause it is part of the 5.4-point over-prediction in 2025Q1 (1.6 in the other windows). That is one more reason to
  drop the clause rather than to shift the windows.

**7. WHAT AN EXPERT IN THE DOMAIN WOULD CHANGE (ranked)**
1. Population: Title I adult, dislocated-worker and DWG exits (issue 2), as the full version.
2. Inputs: drop the section 188 grounds and the disability proxies, and keep ex-offender (issue 1).
3. use_case: one actor and one decision. Suggested text: "For example, a WIOA Title I case manager or local workforce
   board, when a participant's last planned service is given, estimates the chance of employment in the second
   quarter after exit, to decide whom to keep in services or offer the twelve months of follow-up." Remove "and to set
   the employment rate expected of its exit cohort" (or keep it and declare log_loss).
4. Prediction-point wording (curation_comments first bullet, `known`): the exit is recorded 90 days after the last
   service and dated back to it (20 CFR 677.150(c)(1)), so the moment is the last planned service. The information set
   does not change.
5. fit_reason: name the missing placement status at exit and the UI claimant status (PIRL 401) that the public file
   removed, next to the altered wages already named.
6. Optional input: the state's unemployment rate for the exit month (BLS LAUS, published about a month later). It is
   the economic variable of DOL's own model (677.170(c)(1)) and speaks to the drift. It is an external join, so the
   curator decides.
7. Fix the "mostly self-service" description wherever it appears. Wagner-Peyser participants all had a staff-assisted
   service.

**8. GAPS BETWEEN THE DATASET AND THE REAL DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK**
1. 84% of the rows (85-86% of each test window) are exits with no decision of the actor (issue 2). It decides what the
   benchmark mostly measures. Fixable.
2. Inputs the actor's law bars: -0.010 to -0.015 ROC AUC, and a quarter of the follow-up list moves (issue 1). Fixable.
3. Two actors in one use case, with different resolutions, legal input sets and metrics (ranking against
   calibration). Fixable in the text, or with the metric.
4. Missing inputs the actor always has: placement at exit, UI claimant status, residence, and the local labour
   market. Only the last can be added (LAUS). The rest stay in fit_reason.
5. Altered prior wages and coarsened codes (disclosure control, PROV-3): the strongest inputs are perturbed. Already
   named.
6. Prediction-point wording (90-day dated-back exit). Text only.
7. Label maturity of the newest window (LEAK-24, weak): matters only to the cohort clause.

**9. RULES CITED**
use_case.md:
  USE-1, USE-2: one actor and decision; no WP-only actor found.
  USE-3: the prediction point is the last planned service; the information set holds.
  USE-5: Q2 employment is what the case manager acts on; the cohort target acts on aggregates; youth drop right.
  USE-8: approximate; the Title I change does not make it direct, because of the missing placement and UI status
  and the altered wages.
  USE-9: no other per-person actor mirrors the data directly.
  USE-10: repeat persons: history carries +0.001, no gap.
metrics.md:
  MET-1: unit; the pooled score is close to within-board.
  MET-6, MET-7: no fixed k or cost.
  MET-8: roc_auc for the ranking, log_loss if the cohort clause stays.
  MET-9: no AUPRC.
  MET-11: fallback reason to update if the metric changes.
  MET-13: no grouped AUC needed.
selection.md and principles.md:
  SEL-1, P1: the Tensions rows "ethics against anything" and "a factor the actor may no longer use", the latter as
  extended by the rais panel (decisions where the actor's own law bars the factor).

**10. SOURCES**
- 20 CFR 680.150(c): https://www.law.cornell.edu/cfr/text/20/680.150 (follow-up "for a minimum of 12 months ... to
  participants who are placed in unsubsidized employment").
- 20 CFR 678.430(c): https://www.law.cornell.edu/cfr/text/20/678.430 (follow-up for "adult or dislocated worker"
  participants placed in unsubsidized employment).
- 20 CFR 677.150(a)(3) and (c)(1): https://www.law.cornell.edu/cfr/text/20/677.150 (self-service-only users are not
  participants; exit dated back after 90 days without services).
- 20 CFR 677.170(c): https://www.law.cornell.edu/cfr/text/20/677.170 (adjustment model: economic conditions and
  participant characteristics including disability and ex-offender status).
- 29 CFR 38.5 and 38.2: https://www.law.cornell.edu/cfr/text/29/38.5 and https://www.law.cornell.edu/cfr/text/29/38.2
  (prohibited bases, covered programmes).
- 29 USC 3102(24): https://www.law.cornell.edu/uscode/text/29/3102 (individuals with barriers to employment).
- UIPL 41-94 (WPRS): https://oui.doleta.gov/dmstree/uipl/uipl94/uipl_4194.htm ("may not be used in the profiling
  system: age, race, ethnic group, sex, color, national origin, disability, religion, political affiliation and
  citizenship").
- DOL statistical adjustment model summary (2018):
  https://www.dol.gov/sites/dolgov/files/ETA/Performance/pdfs/Statistical-Model-Summary-2-16-18.docx (Table 1:
  female, age bands, Hispanic, race, disability; aggregated to state-quarters; purpose: "States serving
  harder-to-serve populations").
- TEGL 26-15 Attachment II (the builder's text copy in the run folder).
- PY 2025 Q3 record layout (the builder's text copy in the run folder): p. 3 removed items
  (PIRL 401, 1112, residence); PIRL 901 exit; PIRL 1503 follow-up; PIRL 935.
- State policies seen in search results, not relied on: West Virginia ADW FLW 24 (follow-up does not extend the exit),
  Wisconsin DWD WIOA policy 8.7 and 8.8.

**11. FILES (in the run's panel folder)**
dp1_describe.py, dp1_describe.json   populations on the shipped frame (Title I against Wagner-Peyser-only, test windows)
dp2_models.py, dp2_w{0,1,2}.json     variants V0-V3, Title I training, pooled / per-state / per-board AUC,
                                     calibration, follow-up list composition
dp3_followup_today.py, .json         who receives follow-up today (PIRL 1503, PY 2025 Q3 raw file)
dp4_proxies.py, dp4_w{0,1,2}.json    V2 against V2 minus the disability proxies

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: wioa_employment_after_exit
Inputs used: the clean room's data.parquet (200,000-row sample of 2,754,351), its task.md, and the public sources
(DOL ETA national performance page, PY2023Q4 PUF record layout, TEGL 26-15 Attachment II), plus the PY2025Q3 PUF
record layout linked from the national page. I opened no other files on this machine.
Scratch scripts: model.py, era.py in the run's panel folder.

VERDICT
Include with changes: it is a real, policy-relevant prediction task with moderate signal (temporal AUC about 0.72)
and no leak that I could find. But the table combines two source regimes it does not document: one exit quarter is
missing and row volume steps up 3.8x right after it. Also, the temporal split ignores how long the label takes to
become available, and the column types need cleanup.

WHAT THE TASK IS
Each row is one person's period of participation in US public workforce programs (WIOA Title I Adult/DW/Youth,
Title III Wagner-Peyser (96% of rows), Veterans programs) in the WIOA Performance Records Public Use File (PIRL).
Features describe the person at entry (demographics, barriers, education, pre-entry UI wages for 3 quarters,
prior industry/occupation) and the services received up to exit (dates of service types, training, credentials in
progress). The target is whether the person is in unsubsidized employment in the 2nd quarter after the exit
quarter (a WIOA primary performance indicator; 67.1% Yes).
Real use: DOL and states predict exactly this outcome from exiter characteristics when they negotiate performance
targets. TEGL 26-15 Att. II: "A properly specified statistical model will appropriately adjust performance goals for
States serving harder-to-serve populations". It uses Q2 employment and many of these same variables (female, age bands,
education, employed at participation, pre-program earnings, WP receipt, low income, homeless, offender, training,
ITA, Pell...). DOL's model is aggregated to state-quarter level. At the individual level, a state agency or case
manager would score people at exit to target follow-up services. The prediction point is program exit, and every
feature is meant to be known by then. That is a sound framing.

CONCERNS, MOST TO LEAST SERIOUS

1. The source is stitched together without documentation: a whole quarter is missing and volume steps up 3.8x.
   Evidence (sample counts by exit quarter): 2022Q1-2024Q1 hold about 8.9k-11.4k rows per quarter (target rate 0.68-0.72).
   2024Q2 (Apr-Jun 2024) has 0 rows. 2024Q3, 2024Q4 and 2025Q1 hold 36.4k, 36.3k and 36.3k (rate 0.66, 0.66, 0.64). By
   month: 2,828 exits in 2024-03, then nothing until 12,171 in 2024-07. The step appears in almost every state (new/old
   ratio 2.0x for GA up to 9.9x for MT; TX 3.9x, CA 2.8x, NY 2.9x), so it reflects how rows were selected, not real
   program growth. Scaled to the full table, that is about 130k exits per quarter before the gap and about 500k after.
   No single public release explains this. The PY2025Q3 layout says the file holds "individuals who were served by
   these programs between October 1, 2023, and March 31, 2026", so it cannot contain the 2022 exits. The PY2023Q4
   layout (the one task.md links) covers service between Jan 2022 and Jun 2024. Its Q2 outcomes could not exist for
   2024Q1 exits ("Set to blank outcomes when it was too soon to report complete data"). The national page now
   hosts only PY2025 Q1-Q3 files. So the table must combine several releases and select the older part in some way
   nobody has stated.
   Mitigating evidence: the populations look alike. A classifier separating 2023Q4+2024Q1 from 2024Q3+2024Q4 on
   non-date features reaches AUC 0.61, mostly from state (0.60 without state/board). The target-by-pre-wage pattern
   is stable (employed when Q1-pre wage > 0: 0.80 in 2022Q1, drifting to 0.71 in 2025Q1).
   Effect on the benchmark: all three test windows fall in the high-volume regime, while about 45% of the training
   rows come from the older, thinner regime. The train-to-test gap is 3 months for the first window and zero for
   the others. Other state coverage also shifts: OK appears only up to 2022Q4, and MT jumps to 763 rows in 2024Q3
   from about 150.
   Change: document which releases were used and how rows were chosen per quarter. Prefer one consistent source
   with a contiguous exit window, e.g. one recent release or releases deduplicated on (state, encrypted ID, exit
   date) if the ID encryption is stable across releases. At minimum, state that 2024Q2 is absent and why.

2. The temporal split takes no account of when the label becomes available.
   Employment in the 2nd quarter after the exit quarter comes from UI wage records, which arrive with a lag. For an exit in
   quarter t, the label exists only about 3-4 quarters later (the layout: "Due to the lags in availability of wage
   records, outcome data on the data file is missing for many exiters"). Expanding windows that train up to the
   quarter just before the test window use labels a real user would not yet have.
   Measured on 2025Q1: training on all earlier exits gives AUC 0.7156. Training only on exits up to 2024Q1, which
   respects the embargo, gives 0.7043. Training on 2024Q3-Q4 only gives 0.7095. So the optimism is about 0.01 AUC,
   though it is mixed up with the regime change in item 1.
   Change: put an embargo of about 3 quarters between the end of training and the start of each test window, or
   document that the split ignores label latency.

3. The target's source column and the population filters are not stated.
   The target sits in the column order where CALC4013 ("WIOA Employment rate (quarter 2)") would be, between
   calc4005 and calc4021. It could also be PIRL 1602 with code 9 ("Information not yet available") dropped. task.md
   says neither. The population still includes 43 "Retirement" exits (PIRL 935=2) and 11,403 rows (5.7%) with
   "Invalid or undisclosed SSN". The SSN rows have a 61.5% Yes rate and cannot be wage-matched, so their label rests on
   supplemental data. It also includes 1,266 rows flagged Wagner-Peyser "Reportable individual". PIRL 923 (other
   reasons for exit: institutionalized, deceased...) is absent, so I cannot tell whether those exclusions were
   applied. The latest window is slightly lower (2025Q1 Yes rate 0.640 vs 0.659; wage=0 group 0.414 vs about 0.47),
   which could mean some wage records were still incomplete when the file was cut.
   Change: name the source column, list the row filters, and apply the indicator's exclusions consistently
   (retirement, PIRL 923 exits). Consider dropping the most recent exit quarter if its wage records are incomplete.

4. Column types and encodings need cleanup.
   a) 103 datetime64 columns, including the split column, are stored as absolute timestamps. Most are more than 95% null.
      A harness will either crash or treat them as epoch numbers. Convert them to days-before-exit plus received/not
      flags, and keep the absolute exit date only as the time index. No service date falls after the exit date in any
      column (checked all 68 date columns: 0 cases, apart from 40 military separation dates). So those dates carry
      no post-exit leakage.
   b) Nominal codes are stored as float64: local board codes (pirl108a, 588 values), SOC occupation (pirl403, 913),
      NAICS industry (pirl404/405/406, about 1,273 each), CIP (pirl1305, 465), training SOC codes (pirl1306/1311/1316),
      HVRP grantee IDs (pirl310/311), and pirl931 apprenticeship (codes 1-4, 147k rows = 4). Make them categorical, with
      2-digit prefix features where that helps.
   c) Sentinels: pirl412 tenure has 999. Grant fields carry '99999999999999' for "unknown". The source uses 0-padded
      truncated codes, e.g. "Trailing zeros have been added to display 6-digits".
   d) Dead columns: pirl314 (0 non-null), pirl913 and pirl938 are constant, and 23 columns have 200 or fewer
      non-null values in 200k rows. Drop them.
   e) pirl1301_training_provider_name is free text (2,763 unique values in the sample, 97% null). Drop it or bucket it.
   f) Many binary flags are float with NaN meaning "not applicable". That is correct per the source ("Blanks should
      not be treated as zero or 'no'"), but say so in the task notes.

5. Repeated persons cannot be detected (minor).
   The source keys records on (state, encrypted ID, exit date), and the same person can re-enter after more than
   90 days. The ID is not in the table, so I cannot check whether repeat participants straddle train and test.
   Duplicates within the sample are negligible: 2 exact duplicate rows and 3 feature-duplicate pairs, 1 of them with
   conflicting labels. Under a temporal split, returning participants are realistic, so this is low risk.

6. The source adds noise on purpose (minor, acceptable).
   The layout says pre-entry wages are "rounded to the nearest whole dollar and randomly altered", and that the
   post-exit employment codes "have been modified to avoid disclosing the data source". The values stay plausible:
   median pre-entry quarterly wage about $8k, 99th percentile about $63k, max about $986k; age 13-97 with median 40;
   14.6% have zero wages in the 3rd quarter before entry.

WHAT IS GOOD
- Real administrative data with a meaningful target. The base rate of 67% Yes gives balanced enough classes.
- The signal is moderate and not trivial. LightGBM with dates turned into days-before-exit reaches AUC
  0.7165 / 0.7250 / 0.7156 on the 2024Q3 / 2024Q4 / 2025Q1 windows (log loss 0.578 / 0.565 / 0.583, against 0.645 /
  0.643 / 0.657 for the prior rate). A random 80/20 split gives 0.741. Seven basic features (pre-wages, employment
  status, age, state, education) give 0.684, and wages alone give 0.642, so the richer feature set matters.
- Top gain: Q1-pre-entry wage 16%, state 9%, age 8%, Q2-pre wage 6%, prior industry 5%. No single feature
  dominates, so I saw no sign of leakage.
- Post-exit fields (PIRL 1600-1617, 1703-1706, credentials, calc4007-4019 except the target) and follow-up
  service dates (PIRL 1412, 1503) are absent.
- At 2.75M rows it is large. A benchmark will subsample, which is fine.

WHAT I COULD NOT CHECK
- The full 2.75M rows. I saw only the 200k sample, though it is a uniform random draw.
- Which PUF releases were used, why 2024Q2 is empty, and the row selection for 2022Q1-2024Q1. The older releases
  are no longer linked from the national page.
- Whether the target is CALC4013 or PIRL 1602, and which exclusions were applied. I did not read the official
  indicator definition (TEGL 10-16) or Appendix B/C on data cleaning.
- Repeat participants across splits, since the ID was removed.
- The exact boundaries of the 3 test windows. task.md gives only "3 test windows", so I assumed the last three
  exit quarters as expanding windows.

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: wioa_employment_after_exit (target employed_2nd_quarter_after_exit, ROC AUC, 3 temporal test windows)
Kit: the participant kit; scripts, logs and web sources in its work folder.

VERDICT
You can't game this task much from the features or the shipped training rows. There are no post-exit columns, no copies across the split and no row-order signal.
There is one large flaw: a label artefact in the 2025Q1 test window. Texas holds 10.9% of that window, and its label rate collapses to 0.40
(every other quarter is 0.64-0.70). This costs every honest model about 0.023 AUC on r0f0. Anyone who knows about it from outside the kit gains
+0.027 on r0f0 (+0.009 on the mean). The only other gain, +0.005 on the mean, comes from training on the labelled rows of the other test windows.
data.parquet ships those labels, but a model deployed at the exit date would not have them.

SCORES (ROC AUC on the shipped splits, scored with score.py)
  Untuned LightGBM baseline (features() as given, dates as day numbers, 100 trees)   r0 0.71436  r1 0.72686  r2 0.72377  mean 0.72166   work/baseline.py
  Honest, dates made relative to the exit date, plus day of quarter, no absolute exit date   r0 0.71801  r1 0.73118  r2 0.72648  mean 0.72522   work/honest.py
  Honest strong (the same features, 500 trees, lr 0.05, 127 leaves)                           r0 0.72583  r1 0.73824  r2 0.73514  mean 0.73307   work/final.py
  Noise: the baseline refit with a random column (3 seeds) spreads by 0.0000 / 0.0000 / 0.0003 per split. With 500k test rows the sampling SE of the AUC is about 0.0008.

EXPLOITS RANKED BY GAIN
| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Push down the Texas rows of the 2025Q1 window (shift their logits so their mean is 0.40) | work/exploit_tx.py, work/final.py | strong 0.73307 (r0 0.72583); baseline 0.72166 (r0 0.71436) | strong 0.74193 (r0 0.75241); baseline 0.73146 (r0 0.74376) | r0 +0.0266 (strong) / +0.0294 (baseline); r1, r2 0 (the rule only touches exits from 2025-01-01) | No. The shipped training rows cannot teach it, and the features of TX 2025Q1 rows look like TX 2024Q4 (adversarial AUC 0.55, below the 0.58 of a CA control) | Drop the TX rows of 2025Q1 from the test window, or the whole TX 2025Q1 state-quarter, or rebuild from a later release where TX outcomes are complete |
| 2 | Train on the labelled rows of the other two test windows (2024Q3, 2024Q4, 2025Q1, without TX 2025Q1) | work/exploit_windows.py, work/final.py | strong 0.73307 | strong 0.73782 | r0 +0.0037, r1 +0.0059, r2 +0.0046 | No. At exit, the outcome of an exit less than about 3 quarters old is unknown (Q2 after exit plus the wage-record lag), and later windows are the future | Hand a model only the training side of each split. Do not ship labels of rows outside the training side in data.parquet (or score in a harness that hides them) |
| 1+2 | Both together | work/final.py | strong 0.73307 | strong 0.74660 | r0 +0.0301, r1 +0.0059, r2 +0.0046 | No | As above |
| 3 | Rebuild a person from rare dates (military separation date, dislocation date) plus demographics, with age-consistent links. Features: the other period's label, and a later period's employment status and wages at entry | work/exploit_link.py | honest 0.72522 | 0.72533 | r0 -0.0002, r1 0.0000, r2 +0.0006 (noise) | Partly. A deployed system has the person ID (PIRL 100, dropped here) and past outcomes, but not later periods | None needed. Only 0.1-0.6% of test rows link |

FLAWS THAT HURT AN HONEST MODEL
| # | What is wrong | Honest choice that avoids it | Score with flaw | Score without | Fix to the task |
|---|---|---|---|---|---|
| A | TX labels in the 2025Q1 window: rate 0.398 (54,315 rows) against 0.64-0.70 in every TX quarter from 2022Q1 to 2024Q4. The step happens exactly at 2025-01-01 and is the same in all 28 TX local boards | None from inside the kit (a deployed model cannot know). Scoring r0 without TX shows the cost | r0 strong 0.72583 / untuned honest 0.71801 | r0 without TX: 0.74864 / 0.74115 | Drop TX 2025Q1 rows from the test window. The source documentation says outcomes that are "not yet available" should be 9 (blank), not 0 |
| B | Montana pre-entry wages (PIRL 1700-1702) are blank for 88-100% of rows from 2023Q4 on, against 24-41% earlier. The source appendix C confirms "blank for 95-99%". Missing wages in training mean label rate ~0.48; MT test rows have 0.62 | Nothing simple | r2 0.72648 | r2 without MT 0.72928 | Small (+0.003 on r2 if MT is dropped). Flag it, or drop the MT wage columns |
| C | Absolute exit date as a feature: test windows lie past every training date | Dates relative to exit plus day of quarter (honest feature engineering, not a flaw) | 0.72166 | 0.72522 (+0.0036) | none |

FINDINGS

1. Texas 2025Q1 label collapse (exploit 1, flaw A).
   Mechanism. In the 2025Q1 test window the TX label rate is 0.398, against 0.657 (2024Q4), 0.693 (2024Q3) and 0.66-0.70 in all earlier quarters.
   By exit month: 2024-12 0.642, 2025-01 0.406, 2025-02 0.396, 2025-03 0.391. Within 2025Q1 the rate is flat by week (0.38-0.43).
   All 28 TX boards drop by 0.2-0.35, and every subgroup drops (Employed at entry 0.77 -> 0.45, Unemployed 0.66 -> 0.39). The within-TX AUC of the honest model falls from 0.70 to 0.59.
   This looks like a reporting artefact: about 40% of true "Yes" outcomes recorded as "No", for example because the wage file for 2025Q3 was incomplete and unknowns were coded 0 instead of 9 (PIRL 1602: 9 = information not yet available).
   No other state-window comes close. The next-largest residual is PR at -0.11 to -0.17, and it is present in every window.
   Dropping TX raises r0 by 0.023 (strong 0.7258 -> 0.7486); dropping any other state changes it by at most 0.0007.
   The exploit needs outside knowledge of the window's TX outcome rate (the source file, or a state performance report). The features give no hint.
   Mildest fix: drop TX rows with exit >= 2025-01-01, or drop every state-quarter whose outcomes were incomplete at the release date.
   This is about 54k of the 500k test rows of r0f0.

2. Labels of the other test windows (exploit 2).
   data.parquet holds every row with its label, including the 1.5M rows of the three test windows.
   For r0 (test 2025Q1) the 2024Q3 and 2024Q4 exits are "past", but their Q2-after-exit outcome only exists from mid/late 2025. For r1 and r2 the later windows are the future.
   Adding them, minus TX 2025Q1, gives +0.0037 / +0.0059 / +0.0046 on the strong model.
   Adding them with TX 2025Q1 included hurts r1 and r2 (untuned honest: r1 0.73118 -> 0.71744, r2 0.72648 -> 0.71947), because the TX artefact poisons TX predictions. With the exit date kept as a feature, r2 gains +0.003 instead.
   Fix: give models only the training side of each split, which the split files already define. Do not ship the labels of other windows to participants who are trusted to ignore them.

3. Person re-linking (exploit 3).
   Keys: state + sex + race/ethnicity flags + veteran + military separation date (5% of rows) or dislocation date (33% of rows), keeping pairs whose age difference matches the entry-date difference.
   Linked pairs agree on the label 0.71 / 0.70 of the time, against 0.56 by chance. So they are often the same person.
   But only 618 / 1,727 / 3,054 test rows have a later linked period and 5,283 / 3,742 / 2,944 an earlier one. Gain: +0.0001 on the mean, noise.
   A later period's pre-entry wages could reveal the earlier outcome only if re-entry fell 3 quarters after exit. The data stop at 2025-03-31, so that cannot happen for any test row.

ATTACKS THAT FOUND NOTHING (number = result)
 - Row order: rows are sorted by exit date, with random order within a day. AUC of the position within the day is 0.4996 / 0.4986 / 0.4995. Next-row label agreement equals chance (r0 0.5396 vs 0.5390; training pool 0.5739 vs 0.5730). The row index carries only the date.
 - Exact copies: 0 test rows have an exact copy in training (all features, or all but the exit date). The whole file holds 1,217 duplicated rows in 517 groups, none across the split. The source also merged duplicate periods less than 90 days apart.
 - Columns from after the prediction point: all 68 date columns are on or before the exit date. The one exception is the military separation date (703 rows after exit, unrelated to the outcome).
   Post-exit outcome fields (PIRL 1600-1617, 1703-1706) and the encrypted ID (PIRL 100) are not in the kit.
   The best single feature is pre-entry wages, AUC 0.637 on r0 (work/univariate.py). The top 25 are all pre-entry or program facts.
   PIRL 935 "Invalid SSN" (rate 0.58 vs 0.66) is known at registration: signal, not a leak.
 - Formats: wages are integers (the source rounds them and perturbs them at random). The last digit is flat by class (0.0993 vs 0.1000). Round hundreds are just the zero-wage share.
   A format-only model (missing indicators plus last digit and trailing zeros) scores 0.678 mean. All of it is zero wages and program-specific missingness (which services and programs were recorded), which a deployed model has.
   Provider-name string formats (length, case, double spaces, digits) have AUC 0.497-0.503.
 - Statistics over the test rows (co-exiter counts per state, board and date, state-window zero-wage share, computed over each window including the test rows): 0.72539 vs 0.72522 (+0.0002, noise).
 - Train-vs-test classifier without dates: AUC 0.847. It is driven by state mix (GA, OK, MT, CO) and coding drift (second local board, rapid response, apprenticeship), not by the label.
 - Transforms over all rows: none. No standardized, ranked or binned columns. Age is an integer and wages are raw.
 - Lookup / shallow rule: nothing near the model; the best single column is 0.637.
 - Honest training-row choices:
     dropping training state-quarters with outlying label rates (DE 2023Q4 at 0.45, KY 2022Q4, ME 2022Q1): 0.72554 vs 0.72522, +0.0003
     training only on the last 4 quarters: 0.72502, -0.0002
     adding the 254k / 131k pool rows dated before the cutoff but left out of the shipped training sets: 0.72505, -0.0002
   None of these is a real flaw.
 - Training rows that tell the future: none in the shipped splits. Each split's training ends 3 quarters before its test window (2024Q1 / 2023Q4 / 2023Q3), which matches the label lag. 2024Q2 is absent from the file.
 - Web: there is no competition, Kaggle set or "magic feature" thread for this source. Sources read: the DOL national results page, the PUF record layout PY2023Q4 (PIRL 1602 coding, wage perturbation, confidentiality edits) and the PUF Appendix C for PY2025 Q1-Q3 (state cleaning notes; nothing on TX outcomes; the MT wage blanking is documented).
 - Source lookup: the published PUF (PY2025 Q1-Q3, about 5.5 GB each, not downloaded) holds PIRL 1602 and the encrypted ID. Kit rows could likely be matched on exact dates plus the published perturbed wages. Not tried, not ranked.

COULD NOT CHECK
 - Whether the TX 2025Q1 "No" labels are 0s in the source, or 9s ("not yet available") recoded by the preparation. Either way they are wrong for the task. Deciding it needs PIRL 1602 for TX 2025Q1 in the source file.
 - Whether the 500k-row test windows and the ~130k-rows-per-quarter training pool were drawn at random from the source, and from which releases. The pool looks like an older release, where MT and GA rows thin out in 2023Q3-2024Q1.
 - Whether training labels in the most recent pool quarters (2023Q4, 2024Q1) were complete when that release was cut. Their rates (0.672, 0.685) look normal.

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER REPORT: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

Read: principles.md (Tensions, Exceptions and amendments, Consistent judgement), SEL-1, USE-1/5/8/10, LEAK-10/19/24/34,
SPLIT-9/13/14, CLEAN-12 and their Cases tables (the batch branch's copies); dataset.py; builder_report.md; the record; register.json
(5,226 decisions, 34 flags: none on SEL-1, CLEAN-12, LEAK-24 or USE-10 for this dataset; the USE-8 opposite-outcome
flag is general and has no pair with these facts); the REVIEW.md files of rais_employment_separation_1m,
enem_entrance_exam_scores_1m, acs_food_stamps_2014_2024_1m, sinan_dengue_case_screening_1m,
kumc_inpatient_aki_prediction, milk_nir_composition and tunisian_fraud_detection_challenge; ny_wcb_assembled_claims_1m
and labour_inspection_compliance dataset.py; records adult, law_school_admission_bianry, hr_analytics.
One measurement of my own (prepared file): the PY 2023 Q4 CSV's encrypted ids link to the parquet files too (8.5% of
the 2023 Q1-Q3 exits have a 2022 exit of the same state+id in the CSV; 6.6% of the 2023Q4-2024Q2 exits have one in
PY 2024 Q4), so the builder's repeated-person and previous-outcome measurements cover 2022.
None of the batch precedents is decided yet: rais issues 1/3/5, sinan issue 4, enem issue 1, acs D2 and milk are AI
recommendations of 2026-11-09 awaiting Lennart.

SUMMARY
 D1 SEL-1, protected grounds kept ............ DEPARTS, the stated reason does not meet the batch's test (prompt 1)
 D2 Population, all programmes ............... departs from rais issue 3's recommendation WITH a stated reason; a note
                                               to add (USE-8), no prompt
 D3 LEAK-24, newest window at first report ... DEPARTS from a Must; not reasonable as an exception (prompt 2)
 D4 CLEAN-12, SOC/NAICS/CIP kept as codes .... DEPARTS without a reason; decide alike with rais 5 and sinan 4 (prompt 3)
 D5 LEAK-10, post-exit fields dropped ........ consistent (one small note)
 D6 SPLIT-13 / LEAK-19 / USE-10, returners ... consistent with SPLIT-13 and LEAK-19; USE-10 departs from tunisian with
                                               stated facts, alike milk (pending); no prompt
 Drift: none found (no curator decision on SEL-1 outside insurance; no LEAK-24 or CLEAN-12 reversal).
 Third exception: CLEAN-12 (rais, sinan, wioa; chile's communes) if all keep codes -> amendment due (already raised in
 rais issue 5). Selection Bias marker: consistent to leave it off (below, D2).

D1. SEL-1: race and ethnicity (PIRL 210-215), sex (201), disability (202, 204-209, CALC 4021-4029), ex-offender
status (801) and age (CALC 4039) kept as inputs; builder recommends keep.

Precedents
 * bemtpl97 (CC 2026-11-05, Lennart): sex dropped, the actor's legal constraint today (Test-Achats). Insurance family
   (2026-11-08, Lennart; australian_vehicle_insurance_2004_2005, pricing_game_2017_french_mtpl, frempl, spanish
   homeowners): sex dropped under the stance. principles.md Tensions row "a factor the actor may no longer use".
 * rais_employment_separation_1m issue 1 (AI, 2026-11-09, pending): extend the row to any decision on a person where
   the actor's own law bars the factor; drop all five grounds (Lei 9.029/1995 art. 1). Its Consistency bullet names
   wioa's fact ("DOL's adjustment model uses the factors, and the decision allocates help, not a job") and says wioa is
   decided "on the stance you confirm here".
 * acs_food_stamps_2014_2024_1m (AI, 2026-11-09, pending): under the outreach framing a state SNAP agency is barred by
   7 CFR 272.6(a) -> drop sex, race, origin, place of birth; age, disability and citizenship kept because SNAP's own
   eligibility rules use them; under the imputer framing all kept (no law binds the Census Bureau). Its precedent
   checker (D2) already names the wioa pair: "wioa keeps race and sex for a public programme bound by its own
   nondiscrimination rule (WIOA section 188 ...). The distinguishing fact wioa names ... is about DOL's
   performance-target adjustment, not the service decision the use case models."
 * enem_entrance_exam_scores_1m issue 1 (AI, 2026-11-09, pending) and chile_school_dropout_mineduc_1m (AI note): keep
   race, sex, income for a support offer, because NO law bars them for that actor ("support, not a decision against
   the student").
 * hr_analytics keeps gender (never reviewed); adult `No` (Lennart CC: "Potential ethical issues from including race
   as a feature", but excluded on the task); law_school_admission_bianry `No` with `Ethical Issue` (AI counter
   2026-10-22). home_credit_default_risk, credit_card_clients_default keep sex, "not reviewed yet" (the row).
Comparison
 * wioa's stated reasons: (1) DOL's adjustment model uses the same variables (TEGL 26-15 Att. II Table 1, read);
   (2) the decision allocates help, not a price or a denial. Reason (2) is chile's and enem's, and both rest on the
   absence of a law barring the ground; reason (1) is about DOL setting state targets, which IS the use case's second
   decision ("to set the employment rate expected of its exit cohort") but not its first ("whom to offer follow-up
   services").
 * The batch's test (rais, acs, enem all apply it): does the actor's own law bar the factor for the decision modelled?
   The builder did not apply it. The state workforce agency's own law is WIOA section 188 / 29 CFR part 38 (general
   knowledge, NOT read here, as on acs): no individual "denied the benefits of" a WIOA-assisted programme because of
   race, color, religion, sex, national origin, age, disability or political affiliation; one-stop partners such as
   Wagner-Peyser included. On the same knowledge, WIOA itself names "individuals with disabilities", "older
   individuals", "ex-offenders" and "Indians, Alaska Natives and Native Hawaiians" among its "individuals with barriers
   to employment" (sec. 3(24)) and sec. 116(b)(3)(A)(viii) requires the adjustment model to account for "disability
   status ... ex-offender status" -- the same kind of fact acs uses to keep age and disability.
 * So: ex-offender status is not a section 188 ground and is a named barrier (keeping it is consistent under any
   option); disability and age follow acs's "the programme's own rules use them"; race, ethnicity and sex have no such
   role for the follow-up decision, so keeping them departs from rais/acs under the extension, unless the use case is
   narrowed to the cohort-rate decision DOL's own model makes with them.
 * Smaller: the definition's SEL-1 note names race, ethnicity, sex, disability and ex-offender status but not age,
   which is a ground in rais's five and in section 188 (acs added age to its list on the claim audit, claim 31). Sex
   partly survives in pregnant or parenting youth (701), single parent (806), displaced homemaker (807);
   ex-offender status in incarcerated at entry (2413) and release date (2414): completeness of a drop has no precedent
   (acs column auditor raised it; "a new question, not a departure").

Prompt 1 (draft, issue shape)

1. **Keep race, ethnicity, sex, disability, ex-offender status and age as inputs, as now, when rais_employment_separation_1m's issue 1 drops the grounds the actor's own law bars and the state agency's own law (WIOA section 188) lists most of them?**

   * **Problem:**
     - The definition keeps six protected grounds as inputs to a state agency's choice of whom to offer follow-up services, and its reason is that DOL's adjustment model uses them and that the decision gives help rather than denies it[^pc-sel1].
     - Three calls of this batch decide the grounds by one test, whether the actor's own law bars them for the decision (rais drops five, acs drops the ones 7 CFR 272.6 lists, enem keeps because no law bars them), and the builder did not apply it here[^pc-row].
     - WIOA section 188 bars denying a programme's benefits because of race, sex, national origin, age or disability (read from general knowledge, not checked), while WIOA itself names disability, older age and ex-offender status as barriers the programmes serve and the adjustment model accounts for[^pc-wioa].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all; narrow the use case to the cohort's expected employment rate | the follow-up decision leaves `use_case`; the fact recorded: DOL's own adjustment model makes this decision with these factors (TEGL 26-15 Att. II, Table 1) | a documented fact of the actor's own regulator; no signal lost | the per-person decision the use case leads with goes; DOL's model works on state-quarter aggregates, so the per-person use stays ours |
     | b | Keep disability, age and ex-offender status; drop race, ethnicity and sex | PIRL 201 and 210-215 leave; a note names WIOA's barrier list as the reason for the rest | the acs split (grounds the programme's own rules use stay); rais's test | section 188 lists age and disability too; DOL's model uses sex and race; the law must be read first |
     | c | Drop all six, as rais | the six grounds leave | the strictest reading of section 188 | drops grounds WIOA tells the actor to serve and adjust for |
     | d | Keep all, the stance limited to pricing (rais option C) | no change here | the full signal | rais and acs (outreach) then keep too; unlike the reasoning of bemtpl97 |

   * **Recommendation:** decide rais issue 1 first; under its extension, b once section 188 and sec. 3(24) are read from the statute, or a if you prefer to keep only the cohort-rate decision. **Decision:** a, b, c or d?

   [^pc-sel1]: **SEL-1** (Must): a task with ethical concerns is out; a Must the definition can fix is fixed (principles.md, the remedy ladder).
   [^pc-row]: principles.md, Tensions, "a factor the actor may no longer use": bemtpl97 (Lennart, 2026-11-05), the insurance family (Lennart, 2026-11-08); the extension proposed in rais_employment_separation_1m issue 1; acs_food_stamps_2014_2024_1m (7 CFR 272.6(a)); enem_entrance_exam_scores_1m issue 1.
   [^pc-wioa]: WIOA sec. 188(a)(2) (29 U.S.C. 3248), 29 CFR 38.5; sec. 3(24) "individual with a barrier to employment"; sec. 116(b)(3)(A)(viii). Not read in this run.

D2. Population: all programmes (84% Wagner-Peyser-only exits, 6,199,267) against Title I only; builder recommends
all programmes.

Precedents
 * rais_employment_separation_1m issue 3 (AI, 2026-11-09, pending): recommends B, keep only the population the named
   actor decides for (private employees), since "no private HR team scores" public servants; the mediator required
   fit_reason to name the pooled 20% whichever is chosen (done there).
 * chile_school_dropout_mineduc_1m (this batch): keeps the source's population over a narrower deployed list.
 * USE-8 cases: superconductivity, eryhemato (a selection the setting does not share -> approximate, named);
   lt_vehicle_loan_default_prediction (Selection Bias when the release holds less than the actor wants).
Comparison
 * What sets wioa apart from rais: the use case names Wagner-Peyser exits, and its second decision (the cohort's
   expected rate) is the one DOL negotiates per programme, Wagner-Peyser included (TEGL 26-15); rais's public servants
   are in no decision of its actor. That is a stated fact, so keeping all programmes is a reasoned departure from the
   rais recommendation, not an unreasoned one.
 * But the builder's own issue 2 calls Title I "the population whose follow-up services WIOA defines", so for the
   first decision 84% of the rows are outside it. As rais's mediator asked (USE-8), fit_reason should name that share
   either way; it now names only the state aggregates, disclosure control and small areas.
 * Selection Bias: none needed, consistently: the exit cohort with a measured outcome is how the label exists (the
   marker's "no marker when" clause); the small local areas left out by disclosure control and Oklahoma's absence from
   the two parquet files are named in fit_reason and the notes. Different from enem, kumc and sinan, which carry the
   marker for selections the setting does not share (absence by income, a creatinine cohort, lab-closed cases).
 * Decide alike: if Lennart takes rais 3 B on "the named actor's population", ask whether the wioa actor's follow-up
   decision reaches Wagner-Peyser-only exits; if he narrows the use case under D1 option a, all programmes fit it.

D3. LEAK-24: the newest test window (January-March 2025) at DOL's first complete report; builder recommends keep with
a note and re-source from PY 2025 Q4 later.

Precedents
 * LEAK-24 (Must, no severity grade): cut where follow-up is complete or re-source settled labels; compare two
   downloads first. Cases: sf_permit_time (cut), consumer_complaints (re-sourced).
 * tunisian_fraud_detection_challenge (CC 2026-11-04, Lennart: "do the change"): fiscal 2018 cut (probe 13 median z
   -6.7, adjustments 3 times smaller); 2017 kept because four agents measured it in band (p = 0.36), i.e. kept only
   when no censoring was measured.
 * kumc_inpatient_aki_prediction ("whole stays, no censoring by the download date") and sinan_dengue_case_screening_1m
   (final SINAN files, 2021 closed long ago): both test on settled labels, so neither is a keep-with-note precedent.
 * Tensions row "unmatured training labels" (SPLIT-10, Should) covers training labels, not test labels.
Comparison
 * The builder did the comparison the rule asks for and it measured a revision: April-June 2024 read 0.663 at first
   report and 0.672 two quarters later; older quarters +0.3 points; probe 13 rate of No z +2.2 to +2.9. So the newest
   window is between tunisian's 2017 (in band, kept) and 2018 (out of band, cut): censoring measured, small.
 * "Weak" is a size argument; LEAK-24 has no severity grade and a Must takes no exception (principles.md). The three
   windows are also at different report ages in PY 2025 Q3 (Jul-Sep 2024 at its 3rd report, Oct-Dec at its 2nd,
   Jan-Mar 2025 at its 1st), so they are not scored on equally settled labels.
 * Not reasonable as an exception under the ranking; a fix exists (the builder's option b), or an amendment.

Prompt 2 (draft, issue shape)

2. **Keep January to March 2025 at DOL's first report with a note, as now, when LEAK-24 (a Must) cuts or re-sources a newest period whose labels are measured to rise later, as your tunisian 2018 cut did?**

   * **Problem:**
     - The newest window's labels are DOL's first complete report, and the two files show a quarter's employment rate rising from 0.663 to 0.672 two quarters later (0.3 points for older quarters), so January to March 2025 (0.640) likely reads about 0.9 points low[^pc-l24].
     - LEAK-24 has no severity grade, and your tunisian call cut 2018 while 2017 stayed only because it measured in band; here the comparison found a revision, so "weak" is no exception to a Must[^pc-tun].
     - The three windows sit at their 3rd, 2nd and 1st report in the PY 2025 Q3 file, so they are not scored on equally settled labels.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep with the note: the first complete report is the label DOL's performance reports count | recorded as the fact that the rule is not triggered (AI's guess, not verified) | no change; the label the actor is scored on (USE-5) | unverified; if wrong, a known 0.9-point shortfall stays in a Must |
     | b | Shift the windows back one quarter and add PY 2022 Q4 for the 2021 exits | test windows April-December 2024, each at its 2nd report or later; the 50% floor kept | follows sf_permit_time and tunisian | a fourth file to read; the newest quarter goes |
     | c | Re-source January-March 2025 from PY 2025 Q4 when it is out | as now until then | follows consumer_complaints; keeps the newest window | the file is not out yet; ships with the gap meanwhile |
     | d | Amend LEAK-24 to grade it by severity | a measured revision of about 1 point or less kept with a note | one rule for small revisions | a general change from one case |

   * **Recommendation:** b, the fix the rule asks for that is available today; c later if you prefer the newest quarter. **Decision:** a, b, c or d?

   [^pc-l24]: **LEAK-24** (Must): a target right-censored in the newest periods is cut where follow-up is complete, or re-sourced from an archive with settled labels; compare two downloads first (probe 13). Cases: sf_permit_time, consumer_complaints.
   [^pc-tun]: tunisian_fraud_detection_challenge, CC 2026-11-04 (Lennart): 2018 cut (median z -6.7); 2017 kept, measured in band (p = 0.36). principles.md, "Exceptions and amendments": a Must has no exceptions.

D4. CLEAN-12: occupation (PIRL 403, 1306, 1311, 1316), industry (404-406) and CIP (1305) shipped as codes.

Precedents
 * CLEAN-12 (Should, amended 2026-11-01, Lennart): a nominal code whose codebook gives words is decoded; the rule's
   own example is "a job". Cases: 377 columns in 29 definitions (2026-11-01); credit_g (2026-10-31, Lennart: "we want
   the right labels in all cases").
 * ny_wcb_assembled_claims_1m (this batch): NAICS ships as "words [code]". labour_inspection_compliance: industry codes
   decoded from the official KLASS table shipped in the folder (klass-version-30-codes.csv).
 * rais_employment_separation_1m issue 5 (CBO, CNAE, legal nature, municipality) and sinan_dengue_case_screening_1m
   issue 4 (CBO): both keep codes now, both recommend decoding to "words [code]", both ask that rais, sinan and wioa
   be decided alike; rais notes that a third exception of one reason makes an amendment due.
Comparison
 * wioa gives no reason in the notes ("Kept as codes: ... occupation, industry and CIP codes"); the builder's dtype
   review called them "codes without words", which the layout contradicts: it names O*NET (10.0, truncated to 6
   digits), NAICS 2012 and CIP, all with official titles.
 * Facts of its own, either way: codes coarsened to minor/major groups with trailing zeros (16,244 to 22,568 rows per
   industry/occupation column end in 0000; a decode needs titles at each level); NAICS 999999 ("Wages ... exist and
   NAICS Code is not known") is the most frequent level of PIRL 404-406 (375,521 / 389,050 / 384,835 rows), a layout
   code with words, neither decoded nor named in the notes (the local board's 99999 is named; 999999 is not a pure
   unknown since it also says wages exist, so a level of its own rather than missing under CLEAN-10).
 * Departs without a reason; the coarsening is the best guess at a distinguishing fact, and it is weak (the tables
   have titles at every level).

Prompt 3 (draft, issue shape)

3. **Ship the occupation, industry and CIP codes as codes, as now, or as "words [code]" from the official tables, decided alike with rais_employment_separation_1m's issue 5 and sinan_dengue_case_screening_1m's issue 4?**

   * **Problem:**
     - Eight columns ship as numeric codes (281 to 1,324 levels) whose classifications the record layout names (O*NET-SOC, NAICS 2012, CIP), and their official tables give every level its words, which your rule decodes[^pc-c12].
     - The notes give no reason, and rais and sinan keep national classifications as codes too, so a third exception of one reason would make an amendment due[^pc-batch].
     - The industry code 999999 ("wages exist, industry not known") is the most frequent level of PIRL 404-406 (about 380,000 rows each) and is named nowhere in the notes.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Codes, with the coarsening as the reason | an exception: codes shown at 2-, 3- or 6-digit levels with trailing zeros, so a flat lookup would mislabel them; 999999 named in the notes | no lookup files | the tables have titles at every level; the third exception of one reason with rais and sinan |
     | b | Decode to "words [code]" | pinned O*NET-SOC, NAICS 2012 and CIP tables in the folder, the title at the code's own level; 999999 as "Wages, industry not known" | follows the rule, ny_wcb and labour_inspection_compliance | three lookup files and a level-aware decode |
     | c | Amend CLEAN-12 for large national classifications | codes stay here, in rais and in sinan | one decision for the batch | the rule's own example of a code to decode is a job |

   * **Recommendation:** b, the same letter as rais issue 5 and sinan issue 4. **Decision:** a, b or c?

   [^pc-c12]: **CLEAN-12** (Should; amended 2026-11-01, Lennart): a nominal code whose codebook says what it means in words is decoded into those words; credit_g (Lennart, 2026-10-31: "we want the right labels in all cases").
   [^pc-batch]: rais_employment_separation_1m issue 5 and sinan_dengue_case_screening_1m issue 4 (AI, 2026-11-09, pending); ny_wcb_assembled_claims_1m (NAICS as "words [code]"); principles.md, "Exceptions and amendments": three exceptions of one reason make an amendment due.

D5. LEAK-10: post-exit items dropped (PIRL 1600-1618, 1703-1706, 1800-1805, 1814, 1900, 1901, 1406, 1412, 1503,
2002, CALC 4014-4019); the five "most recent" self-service / information / contact dates dropped; seven dates
(1000, 1409, 1806-1810) blanked when after the exit.
 * Consistent with LEAK-10 and kickstarter (`staff_pick`, a post-outcome item dropped once the prediction point was
   set); the blanking follows LEAK-10's second clause (zillow_prize, melbourne_housing_market, aeolus_1m).
 * Dropping rather than blanking 1002, 1007, 1100, 1101, 1103 departs from the blanking precedents WITH a stated fact:
   a blank would mark a return after the exit (missingness that encodes a post-exit event, LEAK-10's list), at
   173k-699k rows each, flags at ROC AUC 0.499-0.500.
 * Small note, no prompt: 1409 and 1806-1810 are also "last" dates, so the same reason applies to their blanks
   (1,648 to 12,438 rows each; employment 0.47-0.83 among them against 0.66; flags 0.500). The notes could say why
   these are blanked (counts small) rather than dropped. 1000 is a "first" date, where the blank is exact.

D6. A returning person's earlier rows (SPLIT-13, LEAK-19, USE-10, LEAK-34).
 * SPLIT-13: holds. The person is a known entity to the state agency (its own records); 9.9-12.6% of each test
   window's exits have an earlier exit of the same person in training; the 9-month gap keeps those training labels
   known before the window (SPLIT-9). Like noaa_storm_events_damage and ppnn (temporal over known entities).
 * LEAK-19: not triggered: 0.3% exact feature copies across the split (0.0% with dates); repeats are distinct exits.
 * USE-10 (Must: "the previous outcome is a feature"): the id is dropped and no previous outcome ships.
   - tunisian_fraud_detection_challenge (CC 2026-11-05, Lennart, issue 1 B): previous_target added (skill 0.150 ->
     0.226; 64-75% of test rows known).
   - milk_nir_composition (AI, 2026-11-09, pending): the cow's last lab fat not added, "measured no gain ... not a
     departure" (ridge 0.0984 -> 0.0986).
   - wioa: +0.001 / -0.001 / +0.001 ROC AUC with the previous known outcome; 10-13% of test exits known. Departs from
     tunisian with stated facts (no gain, low recurrence), alike milk's reading. My check above confirms the CSV ids
     link, so the measurement covers 2022.
   - Note for the curator: USE-10 is a Must, so if "no measured gain, not added" is accepted for milk and wioa, write
     it into USE-10 (an amendment) rather than as exceptions.

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

Position: ship after definition fixes, in its strongest honest framing: the WIOA Title I exits (adult, dislocated
worker, DWG; 1,098,270 exits) as the full version `wioa_employment_after_exit`, with one use case (the per-person
follow-up decision) and roc_auc. Every problem the panel found has a fix in the definition; none needs exclusion
(principles step 5, the remedy ladder). I concede the Texas cut, the race/ethnicity/sex drop, the located
invalid-SSN rows and the Title I population. What is left after them is a valid, large task with no leak.

Judgment record (as proposed)
  Verdict: ship after changes.
  Validity: SEL-1 triggered, fixed (race, Hispanic ethnicity and sex dropped; age and disability are the curator's
    call); USE-1/USE-5 fixed (Title I only, one decision); LEAK-24 triggered, fixed for Texas 2025Q1 (cut), the rest
    in band (note); LEAK-39 fixed (AS, PW cut); LEAK-25 fixed (located rows dropped, the rest under the 2026-11-02
    amendment); LEAK-10, SPLIT-9, SPLIT-14 hold; USE-10 holds (known entity, temporal split), previous outcome not
    added (point 7).
  Value: TP-2 holds (LightGBM 0.72 all programmes, 0.75-0.76 Title I, dummy 0.5); MET-1/MET-8 roc_auc.
  Quality: CLEAN-10/11/12/14 items are Should: noted, or decided alike with rais 5 / sinan 4 (CLEAN-12).
  Weighed: size + (1.1M rows, 216 features, no sub-sampling), source +, gap + (social science), use case + after the
    narrowing.

New measurement (a1, a2 in the run's panel folder, on the column auditor's clean_full.parquet, all 7,373,493 exits):
  Title I rows of Texas 2025Q1: 2,586, rate 0.539 against 0.704-0.816 in every other Texas quarter (the same hole);
  Title I without Texas: 0.691 / 0.686 / 0.692 for 2024Q3 / 2024Q4 / 2025Q1 (no fall at the release end).
  American Samoa's 120 exits (all No) are all Title I. The LEAK-25 rule (invalid SSN, pre-entry wages all blank)
  finds only 1,240 Title I rows (rate 0.204), against 19,556 overall (0.022), because SPRA fills blank pre-entry
  wages with 0 for adult and DW exiters.

POINTS, strongest first

1. The task is real, has no leak and has headroom; no agent found a reason to exclude it.
   Evidence: no shipped column is recorded after the exit (column auditor: all 71 dates checked; only PIRL 304's
   2,197 planned separations, no outcome link). The task gamer found no feature, copy, row-order or format shortcut
   ("You can't game this task much from the features"; 0 exact copies across the split; best single column 0.637).
   Untuned LightGBM scores 0.707-0.725 against dummy 0.5 and linear 0.686 (spread +0.053, paired SE 0.003), on 3 of 3
   windows, with 170k+ of each class per test fold. Split auditor: "Nothing needs a re-split". All seven verdicts are
   ship or include after changes, or right with notes. The blind reviewer's split concerns are answered by the
   definition. The empty 2024Q2 is the 9-month gap. The 3.8x volume step is the row budget (at most 500k per test
   quarter against a 1M sample of 2022-2024; the full data hold about 200k exits a month throughout). The embargo it
   asks for (train to 2024Q1 for the 2025Q1 window) is what ships. The clean room did not have the notes that say so.
   Rules: LEAK-10, SPLIT-9, SPLIT-14 (Musts) hold; TP-2, TP-3, MET-2 hold.
   Why it outranks: the objections below are independent failures, each with a fix by dropping, filtering or
   re-targeting. Exclusion is only for a Must that cannot be fixed, and none of them is one.

2. Texas January-March 2025, American Samoa and Palau: concede. Cut the located cells; the rest of the newest window
   is in band.
   Evidence: Texas 2025Q1 target 0.398 against its 1st-quarter-after-exit rate 0.623 (+0.226; p99 over 650
   state-quarter cells +0.035, next largest +0.06). SPRA Appendix B changed code 9 to 0 "when complete data are
   expected". For AS/PW: "State reported no wages ... All records were '0'". Cut the Texas exits from 2025-01-01
   (68,625; 2,586 in Title I) and AS/PW (121; 120 in Title I). The rule picks rows by state and exit date, not by the
   label. r0 ROC AUC moves 0.707 -> 0.734 (claim auditor) and 0.726 -> 0.749 (task gamer). After the cut the
   release end shows no fall: the national 2025Q1 rate without Texas is 0.669, against 0.652 / 0.658 for 2024Q3/Q4
   (probe 13's z +2.2 to +2.9 was Texas alone); Title I without Texas 0.692 against 0.686 / 0.691. The remaining
   first-report revision (about 0.5-0.6 points, mostly rows a model already scores as employed) moves ROC AUC by
   -0.003 / -0.004 and reorders no model (split auditor).
   Rules: LEAK-24 (Must); LEAK-39 / USE-5 (Must). Precedent: tunisian, where 2018 was cut (out of band) and 2017 kept
   (measured in band).
   Why it outranks the window shift (precedent checker, option b): the measurement locates the incomplete follow-up
   in one state-quarter, and LEAK-24's remedy cuts where it is incomplete. A one-quarter shift puts the oldest train
   side at 47.3% (two quarters 42.4%) unless PY 2022 Q4 is added, whose outcomes fall in the pandemic's tail
   (SPLIT-14, SPLIT-20). It still leaves the newest window at its 2nd report. Keep with a note naming each window's
   report stage, and re-source from PY 2026 Q1 when it is out. If the curator reads LEAK-24 as binary whatever the
   size, the two-quarter shift plus PY 2022 Q4 still keeps the dataset.

3. Population: concede Title I only, and ship it as the full version.
   Evidence: follow-up is "for participants in adult or dislocated worker workforce investment activities who are
   placed in unsubsidized employment" (20 CFR 678.430(c)). No Wagner-Peyser-only exit carries a follow-up date (0 of
   3,065,763 in PY 2025 Q3; partly reporting design, since PIRL 1503 is required for Title I only). 58.1% of
   Wagner-Peyser-only exits are one-day contacts, and Montana's 10,122-exit batch closure is 99.9% Wagner-Peyser only.
   Title I: 1,098,270 exits, rate 0.717, no sub-sampling. Train sides are 627k-781k (71.1 / 64.1 / 57.1%), test
   windows 74,729-79,207 with about 23k-25k not employed each. LightGBM trained on Title I scores 0.752 / 0.761 /
   0.758 on Title I test rows, against 0.746 / 0.756 / 0.753 trained on all programmes (split auditor). The split
   and the gap are unchanged.
   Rules: USE-1 and USE-5 (Musts: one actor and decision, at its resolution); USE-8 (fit stays approximate, with no
   placement at exit, no UI status and altered wages, all named in fit_reason).
   Why it outranks "keep all programmes": USE-1 is a P3 Must for every row, and no per-person Wagner-Peyser decision
   at exit was found (domain practitioner). Size is a Weigh factor and cannot override a Must. The batch goal still
   holds: 1.1M rows and 216 features.

4. Invalid-SSN exits with no pre-entry wage record: concede, and drop the located rows. Keep the rest with a note.
   Evidence: all programmes: 19,556 exits (0.27%), 2.2% employed (0.0% in NJ), worth +0.0014 to +0.0021 ROC AUC. The
   rule reads PIRL 935 and 1700-1702, not the label. In Title I the rule finds 1,240 rows (0.204), because blank
   wages are filled with 0 there. Drop them too: cheap and consistent. The unlocated rest (no wage-record match)
   follows each state's matching, and the state ships as a feature. The task keeps signal beyond it: within-board
   ROC AUC 0.714-0.722; the state alone scores 0.545-0.578, and only 0.514-0.545 on Title I rows (domain practitioner).
   The label is DOL's own indicator, which counts an unmatched exit as not employed and scores states on it
   (Appendix B; USE-5).
   Rules: LEAK-25 (Must). Amended 2026-10-21 (Lennart): located rows are dropped (caracas_cervical_cancer,
   account_debt_south_africa, fraud_detection_..._1m). Amended 2026-11-02 (Andrej): a mix that follows a shipped
   reporting unit is kept with a note when signal remains beyond it (noaa_storm_events_damage).
   Why it outranks retirement: the amended rule names this exact path.

5. Metric: roc_auc, with the use case narrowed to the per-person follow-up decision.
   Evidence: follow-up use runs from 0.2% to 36.1% of Title I exits across states, so no k, capacity or cost is
   fixed. The pooled ROC AUC sits 0.008-0.015 above the within-board mean and ranks feature sets the same way
   (domain practitioner). The cohort-rate clause is an aggregate decision on state-quarters (20 CFR 677.170; TEGL
   26-15 Att. II p. 2). It is also the one decision for which the protected grounds are lawful inputs, so keeping
   it in the same task contradicts point 6.
   Rules: MET-1 (Must), MET-7, MET-8 (Should), USE-5 (resolution).
   Why it outranks log_loss: MET-8's fallback for binary tasks is roc_auc. log_loss is right only for the clause I
   propose to drop. Concede: if the curator keeps the clause, declare log_loss.

6. Protected grounds: concede race, Hispanic ethnicity and sex. Age and disability are a curator call, and the
   dataset ships either way.
   Evidence: 29 CFR 38.6(b) bars a recipient (a state workforce agency, 38.4) from providing a different service on
   the basis of race, national origin or sex. Dropping PIRL 201 and 210-215 costs nothing measurable (-0.001 to
   +0.005, claim auditor; at most 0.0012, domain practitioner). Age and disability: WIOA names older individuals and
   individuals with disabilities as barrier groups (29 USC 3102(24)(D),(E)), and the adjustment model must account
   for disability (20 CFR 677.170(c)(2)). acs_food_stamps (pending) kept the grounds the programme's own rules use.
   Against: UIPL 41-94 bars age and disability from DOL's own per-person reemployment profiling. It is the closest
   precedent, and I cannot rebut it. Dropping them as well costs 0.010-0.015 (pooled 0.711-0.718, Title I
   0.727-0.737), still far above the dummy and the best single feature. Ex-offender status stays: it is not a 38.4
   ground, and WIOA names it as a barrier.
   Rules: SEL-1 (Must, P1); the Tensions row "a factor the actor may no longer use" (the batch extension pending in
   rais issue 1).
   Why the dataset survives P1: the remedy ladder makes the drop the fix. No evidence says the task is harmful once
   the barred inputs are gone. The note must list every column a drop covers: 701 (pregnancy), 803 (LEP), and the
   disability proxies 303, 602, 917, 922 code 2, 1114 code 3 and 1115/3007 (VR&E).

7. The previous known outcome: ship without it, as defined.
   Evidence: it adds +0.001 overall (builder +0.001 / -0.001 / +0.001; split auditor 0.7252 -> 0.7260 and 0.7321 ->
   0.7334), and +0.007-0.008 on the 10-13% of rows that are returning persons. The encrypted ids do not link across
   files for Texas (22.1%, PY 2024 Q4 to PY 2025 Q3) or Utah (63.7%, PY 2023 Q4 to PY 2024 Q4) (claim auditor). In
   those states the feature would record the file boundary as much as the person's history. SPLIT-9 and SPLIT-13
   hold without it.
   Rules: USE-10 (Must). The decision it requires (known entity, temporal split) is made, and the rule makes the
   history legitimate. Precedents: tunisian (added, skill 0.150 -> 0.226); milk (not added, no gain; pending).
   Why it outranks adding: the overall gain is within run-to-run spread, and the id fact sets the case apart from
   tunisian. Concede: if the curator reads USE-10 as requiring the feature, the split auditor's construction is
   safe (exits at least 4 quarters before, from the dropped id). Add it with the Texas/Utah linkage in the note. The
   dataset ships either way.

CHANGES THAT NEED NO DECISION (the reports agree)
  - splits_comment: rest the 9-month gap on the state's own wage records for quarter Q-2, not on DOL's four-quarter
    fill (claim auditor F4, split auditor 3). SPLIT-9 needs at least 6 months; 9 holds.
  - Prediction-point wording: the exit is dated back after 90 days without service (20 CFR 677.150(c)). The
    information set does not change.
  - Add PIRL 304 to MASK_AFTER_EXIT (2,197 rows, no signal). Mask 1410 and 2516 the same way for robustness. Add a
    note on PIRL 935 code 2 (1,871 rows).
  - Notes to add or fix: each window's report stage; the Texas and Utah ids do not link across files; "Wagner-Peyser
    only" becomes "no Title I funding stream"; the NAICS 999999 sentinel; local-board coding differs by release
    (boards add at most 0.001); the full SEL-1 column list; README decision counts after the youth filter;
    fit_reason names the placement at exit and the UI status that the public file removed.
  - P7 Should items (CLEAN-10 unknown levels; CLEAN-11 tenure longer than age minus 14; CLEAN-14 ordinals 303, 1328
    and 3004; CLEAN-12 SOC/NAICS/CIP, decided alike with rais 5 and sinan 4): fixed where cheap, otherwise noted.
    None touches validity.

CONCEDED: the Texas 2025Q1 and AS/PW cut (LEAK-24, LEAK-39); race, ethnicity and sex dropped (SEL-1); the Title I
population (USE-1); the located invalid-SSN rows dropped (LEAK-25); log_loss if the cohort clause stays (MET-8).

Files: a1_title1_located.{py,log}, a2_tx_title1.{py,log} in the run's panel folder.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

The critic and I agree on the verdict ("ship after changes", nothing excludes the dataset), on Title I only (its 2),
on the Texas and AS/PW cut (its 4), on dropping the located rows (its 5), on removing the cohort clause (its 6) and on
the notes (its 7). On its 1 and 3 I now concede. On its 4 I concede that the remaining lag needs an explicit decision,
and I argue which one.

Critic 1, protected grounds: CONCEDE, including age and disability.
  I had kept age and disability open on the strength of WIOA's barrier groups and the acs precedent. That analogy
  fails. acs keeps the grounds that SNAP's own eligibility rules use. The follow-up decision is not eligibility: it
  allocates a service among people who are already eligible, which is exactly the kind of decision WPRS makes. UIPL
  41-94 bars age and disability from that per-person score (same agency, same kind of decision, same list), and I have
  no rebuttal to it. The domain practitioner also notes that a state gives the barrier groups priority by policy, not
  through a score. The critic is right that a gain of 0.013 sets no case apart.
  What follows: drop PIRL 201, 210-215, CALC 4039, PIRL 202, 204-209, 939, 940, CALC 4021-4029 and the disability
  proxies (303, 602, 917, 922 code 2, 1114 code 3). Keep ex-offender status (801, 2413, 2414). Cost: ROC AUC -0.010
  to -0.015; pooled 0.711-0.718 and Title I 0.727-0.737 remain far above the dummy (0.5) and the best single
  feature (0.637). The edges of the drop are the curator's call, and the note names them whichever way it goes:
  701 (pregnancy, 38.7), 803 (LEP, 38.9), and the Youth-programme items. Youth is a programme limited by statute to
  an age class (38.6(g), per the claim auditor).
  Rule: SEL-1 (Must, P1); the Tensions row, decided alike with rais issue 1.

Critic 2, population: AGREE (my point 3). One addition from my measurement: AS's 120 exits are all Title I, so the
  AS/PW cut is still needed under Title I. Texas 2025Q1 is 2,586 Title I rows (0.539 against 0.704-0.816 in other
  Texas quarters).

Critic 3, previous known outcome (USE-10): CONCEDE.
  My two reasons do not carry against a Must.
  (a) "+0.001 overall" is the wrong measure. The feature concerns the 10-13% of rows that are returning persons,
  and on them the paired comparison gives +0.007 / +0.008 (0.7575 -> 0.7645, 0.7574 -> 0.7657; split auditor, same
  training sample, so no seed noise). milk's "no gain" does not apply.
  (b) The Texas/Utah id breaks make the feature noisier in those states. They do not make it wrong. A failed link
  reads "none" in both training and test for the same file boundaries, and no label can cross into the gap or the
  test window, because the construction only reads exits at least 4 quarters before the row's own exit quarter.
  That is the training side of every split (train ends at Q-4 under the 9-month gap). Noise is not a fact that sets
  the case apart from tunisian.
  What follows: add `previous_known_outcome` (Yes / No / none) and the quarters since that exit, built from the
  dropped id, and add a note on the linkage rates (TX 22.1%, UT 63.7%). The split does not change. The alternative
  is the curator's amendment of USE-10, which I no longer argue for.
  Rule: USE-10 (Must); precedent tunisian (Lennart, 2026-11-05).

Critic 4, Texas and the remaining first-report lag:
  Texas 2025Q1: AGREE (my point 2). The critic's LEAK-25 reading of the mechanism is also right; the same cut fixes
  both.
  The remaining lag: CONCEDE that it needs an explicit decision. DISPUTE which one.
  - My opening called it "in band", like tunisian 2017. That rested on probe 13, whose flag disappears without
    Texas (national 2025Q1 0.669 against 0.652 / 0.658). But LEAK-24 says "compare two downloads first", and that
    comparison measures a revision: about 0.6 points after Texas (claim auditor), +0.31 / +0.72 / +0.01 points from
    the 1st to the 2nd report in Title I (split auditor). LEAK-24 has no severity grade, and a Must takes no
    exception. So "in band" does not settle it.
  - Which decision: I argue for an amendment of LEAK-24 that grades it by severity. principles.md allows this ("a
    leak that is a Must when strong and a Should when weak"). This would be its first case: a measured revision
    under about 1 point that moves ROC AUC by -0.003 / -0.004 and reorders no model (four models, three label
    versions; split auditor). Add a note naming each window's report stage, and re-source from PY 2026 Q1 when it
    is out.
  - Why the amendment over the shift: the two-quarter shift needs a fourth file (PY 2022 Q4), whose 2021 exits have
    outcomes in 2021Q3-2022Q2, the pandemic's tail (SPLIT-20, not measured). Without that file the oldest train
    side falls to 42.4% (SPLIT-14, Must). And labels are not final even at the 3rd report (+0.06 to +0.32 points
    to the 4th). So the shift buys a 0.003 correction with a larger, unmeasured drift.
  - If the curator declines the amendment, the shift plus PY 2022 Q4 still keeps the dataset. Either way the
    dataset ships.
  Rule: LEAK-24 (Must, part 3) and the amendment route in principles.md ("Exceptions and amendments").

Critic 5, located unmatched rows: AGREE, drop them (19,556 + 121). One fact for the Title I framing: there the rule
  finds only 1,240 rows (rate 0.204, not 0.022), because SPRA fills blank pre-entry wages with 0 for adult and DW
  exiters. So in Title I most unmatched exits cannot be located. They stay under LEAK-25's 2026-11-02 amendment: the
  state ships as a feature, and the task keeps signal beyond it (within-board ROC AUC 0.714-0.722; the state alone
  0.514-0.545 on Title I rows). I accept the critic's point that `predicted` argues against a USE-5 keep for the
  rows the rule does locate.

Critic 6, metric: AGREE (my point 5). Remove the clause and keep roc_auc. With Title I and the protected grounds
  gone, nothing is left that needs log_loss.

Critic 7, stitching and wording: AGREE (my point 1 and the no-decision list). Montana's blank wages (+0.003 on r2
  when it is dropped) are a documented reporting-unit pattern (Appendix C). A note is enough; I did not measure
  whether the Title I fill to 0 changes it.

Revised judgment record
  Verdict: ship after changes, as Title I only (`wioa_employment_after_exit`, full version).
  Validity: SEL-1 fixed (race, ethnicity, sex, age and disability items dropped; ex-offender kept); USE-1/USE-5
    fixed (Title I, one decision); USE-10 fixed (previous_known_outcome added); LEAK-24 fixed for Texas 2025Q1
    (cut), the remaining lag a curator call (amend LEAK-24 by severity, recommended; or the two-quarter shift plus
    PY 2022 Q4); LEAK-25 and LEAK-39 fixed (located rows, AS/PW cut); LEAK-10, SPLIT-9, SPLIT-14 hold.
  Value: TP-2 holds (Title I about 0.73 without the grounds, dummy 0.5); MET-1 roc_auc.
  Quality: SPLIT-10 rewording, SPLIT-20 notes, the PIRL 304 mask; CLEAN items noted or batch-decided.
  For the curator: the LEAK-24 amendment or shift; the edges of the SEL-1 drop (701, 803, the Youth items).

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: wioa_employment_after_exit_1m (record wioa_employment_after_exit), 2026-11-09

Position: ship only after changes. None of the points below asks for exclusion: every Must has a fix in the
definition. Point 1 is the most fundamental. Point 4 (Texas 2025Q1) is the largest measured break, and the builder
graded it weak.

Judgment record, as I argue it:
  Verdict: ship after changes.
  Validity: SEL-1 and the Tensions row "a factor the actor may no longer use" are triggered: drop race, ethnicity
    and sex; age and disability too (I argue for dropping them; the curator decides). USE-1, USE-5 and USE-8 are
    triggered: take Title I only, or rewrite the use case. USE-10 is departed from: add the previous outcome, or
    amend the rule. LEAK-24 is triggered and strong for Texas 2025Q1: drop those rows. The first-report immaturity
    left after that is a Must, so it needs an explicit call. LEAK-25 is triggered and small: drop the located rows.
  Value: MET-1 is triggered while the cohort-rate clause stays: remove the clause, or declare log_loss.
  Quality: SPLIT-20 and SPLIT-10 need notes and rewording, and PIRL 304 needs a mask. None of these is a reason to
    hold the dataset.

1. Protected grounds are inputs to a decision the actor's own law bars them from.
   Rule: P1 SEL-1 (Must) and the Tensions row "a factor the actor may no longer use" (P3/P4, USE-1, USE-6). Its
   extension to any decision on a person is pending as rais_employment_separation_1m issue 1, so this dataset is
   decided alike with rais.
   Problem: the features include race (PIRL 211-215), Hispanic ethnicity (210), sex (201), age (CALC 4039) and
   disability (202, 204-209, 939, 940, CALC 4021-4029; proxies 303, 602, 917, 922 code 2, 1114 code 3). The use
   case's per-person decision is "whom to offer follow-up services".
   Effect: the benchmark rewards a model the actor could not lawfully deploy. On the domain practitioner's Title I
   list (the lowest 20% per board), the grounds move a quarter of the list, mostly by age. People aged 55+ are
   35.3 / 33.5 / 31.8% of the list with the grounds and 21.1 / 19.1 / 18.8% without them, against 17.1 / 16.6 /
   16.0% of exits.
   Evidence:
   - The claim auditor and the column auditor read the regulation. The actor is a recipient (29 CFR 38.4(zz)).
     38.6(b) and (d) say it must not, on a prohibited basis, deny an aid, benefit, service or training, or provide
     it differently. Nor may it use criteria on such a basis to set "the class of individuals to whom such aid ...
     will be provided". The prohibited bases are race, sex, national origin, age and disability (38.5). Sex
     includes pregnancy (38.7), and national origin includes limited English proficiency (38.9).
   - DOL's own per-person model for allocating reemployment services is WPRS. Under UIPL 41-94, "the following
     elements may not be used in the profiling system: age, race, ethnic group, sex, color, national origin,
     disability ..." (read by the domain practitioner). It is the same agency, the same kind of score and the same
     list.
   - The builder's reason does not carry. TEGL 26-15 Att. II is a fixed-effects model on state-quarter aggregates
     that sets state targets (p. 2). It ranks no person.
   - Cost of dropping race, ethnicity and sex: -0.001 to +0.005 ROC AUC, within the seed spread of about 0.005
     (claim auditor). Dropping age and disability as well costs -0.010 to -0.015, mostly age (claim auditor,
     domain practitioner).
   Remedy:
   - Drop PIRL 201 and 210-215. This costs nothing and has no WIOA carve-out.
   - Drop age and the disability items with their proxies too. UIPL 41-94 names both, and the 0.013 that age
     carries is a size of gain, which sets no case apart.
   - The curator's alternative for age and disability is WIOA's barrier groups (29 U.S.C. 3102(24)(D),(E);
     20 CFR 677.170(c)(2)), the way acs keeps its programme's own eligibility grounds.
   - Keep ex-offender status (801, 2413, 2414): it is not a section 188 ground.
   - Rewrite the SEL-1 note to say why the grounds left, and update `known`.

2. The use case's per-person decision does not exist for 84% of the rows.
   Rule: P3 USE-1, USE-5 and USE-8 (Must); the builder's issue 2.
   Problem: follow-up is a Title I adult and dislocated-worker service for participants placed in employment
   (20 CFR 678.430(c) and 680.150(c), read). 6,199,267 of the 7,373,493 exits (84%, and 85-86% of each test
   window) have no Title I funding stream. In PY 2025 Q3, 0 of 3,065,763 Wagner-Peyser-only exits carry a
   follow-up date (domain practitioner).
   Effect: the benchmark mostly measures one-day job-service contacts that no case manager decides on (58% have
   entry = exit; 0.23% had training). A model trained on Title I alone scores better on the Title I test rows:
   0.7523 / 0.7605 / 0.7584 against 0.7461 / 0.7561 / 0.7531 (split auditor).
   Why the builder's reason does not hold: the reason given for all programmes ("DOL's targets cover
   Wagner-Peyser") belongs to the aggregate target-setter, whom USE-5 places at another resolution. The issue's
   "mostly self-service" is also wrong: 100% of these exits had a staff-assisted service.
   Remedy:
   - Ship Title I only (CALC 4001, 4002 or 4004 set) as the full version `wioa_employment_after_exit`:
     1,098,270 exits, rate 0.717, no sub-sampling.
   - The split is unchanged: train sides are 71.1 / 64.1 / 57.1% of the rows (the floor holds), and the test
     windows hold 74,729 to 79,207 exits.
   - This is the rais issue 3 reasoning: the population the named actor decides for.
   - If all programmes stay, fit_reason must name the 84%, and the use case must name a decision these exits have.
     The only one left is the cohort rate (point 6).

3. A returning person's previous known outcome is not shipped.
   Rule: P3 USE-10 (Must: "for a known entity ... the previous outcome is a feature"). SPLIT-13 holds.
   Problem: the state agency knows the person. 9.9-12.6% of each test window's exits have an earlier exit of the
   same person on the train side. The builder left the feature out because it adds only +0.001 overall.
   Evidence (split auditor): the outcome of the latest earlier exit at least 4 quarters back raises ROC AUC on
   returning persons from 0.7575 to 0.7645 (2025Q1) and from 0.7574 to 0.7657 (2024Q3). New persons are unchanged.
   The employment rate is 0.74-0.75 after an employed earlier exit and 0.43-0.44 after one without employment.
   Precedents: tunisian_fraud_detection_challenge added previous_target (Lennart, 2026-11-05).
   milk_nir_composition's "no gain" (pending) does not fit this case, because here a gain is measured on the rows
   the feature concerns. A Must takes no exception (precedent checker D6).
   Remedy:
   - Add `previous_known_outcome` (Yes, No or none) and the quarters since that exit. Build them from the dropped
     id over exits at least 4 quarters before the row's exit quarter, so no gap or test label can enter.
   - Note that the ids link only partly across files: Texas 22.1% from PY 2024 Q4 to PY 2025 Q3, Utah 63.7% from
     PY 2023 Q4 to PY 2024 Q4 (claim auditor).
   - Otherwise the curator amends USE-10 for a negligible gain, as a deliberate change.

4. Texas's labels in the newest test window record an incomplete wage quarter.
   Rule: P4 LEAK-24 (Must), strong. By its mechanism it is also LEAK-25: "not recorded" was written as "No".
   Problem: Texas exits of January to March 2025 (68,625 rows) read 0.398 employed. Every other Texas quarter reads
   0.65-0.70, and the same exits read 0.623 in their 1st quarter after exit.
   Evidence:
   - The hole sits on calendar quarter 2025Q3. Texas's 2024Q3 exits read 0.385 there (their 4th quarter after
     exit) and its 2024Q4 exits 0.393 (their 3rd).
   - Over 650 state-quarter cells, the 1st-quarter rate exceeds the 2nd by at most +0.035 at the 99th percentile.
     Texas 2025Q1 is +0.226; the next largest is +0.06.
   - SPRA's Appendix B: a missing or "not yet available" code is set to 0 once complete data are expected.
   - The task gamer found the same independently.
   Effect: 10.9% of the newest window's test rows (54,315 of 500,000) score a recording artefact.
   - Every honest model loses about 0.023-0.027 ROC AUC on that window: 0.707 -> 0.734 without Texas (claim
     auditor), 0.726 -> 0.749 (task gamer). On Texas alone the score is 0.578.
   - Anyone who reads the public source file can push those rows down and gain +0.027 (task gamer, exploit 1).
   - The newest window looks hardest only because of this.
   Why the builder's reading is refuted: the builder called it "weak, most of it drift". The national 2025Q1 rate
   without Texas is 0.669, above 2024Q3 and 2024Q4 (0.652, 0.658), so the release-end rise in "No" that probe 13
   flags is Texas alone. The split auditor's "weak" grade measured the general first-report revision, not Texas.
   The builder's remedy (take the quarter from PY 2025 Q4) is not available: the national page lists PY 2025 Q1-Q3
   only (checked 2026-11-09 by two agents).
   Remedy:
   - Drop Texas exits dated from 2025-01-01 (68,625 rows; a rule on state and date that does not read the label).
   - Add a Decision table of the 1st- against the 2nd-quarter rate by state for 2025Q1.
   - Revisit when PY 2025 Q4 is out.
   What remains outside Texas: the three windows sit at their 1st, 2nd and 3rd DOL report. A quarter's rate rises
   0.7-1.1 points by its third report, which costs about 0.003-0.004 ROC AUC and reorders no model (split auditor).
   LEAK-24 has no severity grade, and a Must takes no exception (tunisian 2018 was cut). So the note must name all
   three report stages, and keeping them needs the curator to either amend LEAK-24 for a small measured revision or
   shift the windows (two quarters, plus the PY 2022 Q4 file). Calling it "weak" is not enough.

5. "Not employed" is mixed with "not recorded" for exits that cannot be wage-matched.
   Rule: P4 LEAK-25 (Must), small.
   Problem: SPRA codes 0 when a person "is not found in the wage records", and a person without a usable SSN cannot
   be found. A rule that does not read the label, PIRL 935 = 1 (invalid or undisclosed SSN) with PIRL 1700-1702
   all blank, locates 19,556 exits.
   Evidence:
   - These exits are 2.2% employed (NJ 0.000, AR 0.001, ID 0.001). Invalid SSNs with a positive pre-entry wage are
     0.733 employed, and valid SSNs without a pre-entry wage 0.417 (column auditor).
   - American Samoa and Palau (121 rows, all "No"): Appendix B says "State reported no wages in the 2nd quarter
     after exit quarter ... All records were '0'" (claim auditor).
   Effect: LightGBM finds these rows through PIRL 935 (predictions of 0.05-0.08), and they add +0.0014 to +0.0021
   ROC AUC per window. The model is rewarded for knowing whom the state cannot match, not who works. The state
   feature gives American Samoa away.
   Remedy:
   - Drop the located rows (19,556 + 121), with their counts in a Decision table. PIRL 935 stays as an honest input.
   - This follows the LEAK-25 amendment of 2026-10-21 (caracas_cervical_cancer, account_debt_south_africa,
     fraud_detection_in_electricity_and_gas_consumption_1m).
   - The task_summary's `predicted` is "whether the person had unsubsidized employment". That argues against a
     USE-5 keep on the ground that "DOL counts them as not employed".

6. The declared metric does not score the use case's second decision.
   Rule: P6 MET-1 (Must) and MET-8; also USE-1 (one decision per use case).
   Problem: the use case names two decisions. One is whom to offer follow-up, a ranking. The other is "to set the
   employment rate expected of its exit cohort", a calibration. ROC AUC is blind to the second.
   Evidence (domain practitioner): an untuned LightGBM's mean prediction is 0.694 / 0.674 / 0.673 against realised
   rates of 0.640 / 0.658 / 0.657, i.e. 5.4, 1.6 and 1.6 points too high, while its ROC AUC looks normal. The
   cohort decision is DOL's aggregate decision (state-quarters). It is also the one decision where the protected
   grounds are lawful, so keeping it in the same task contradicts point 1.
   Remedy:
   - Remove the clause from `use_case`. This is the mildest fix: it keeps roc_auc and fits points 1 and 2.
   - If the clause stays, or all programmes are kept on its strength (point 2), declare log_loss and update the
     fallback reason (MET-8, MET-11).

7. The release stitching and some wording: quality only.
   Rule: P4 SPLIT-20 (Should), SPLIT-10 (Should), USE-3 (wording), writing.md.
   Most of what the blind reviewer saw is by design:
   - 2024Q2 is empty because it lies in the 9-month gap of all three windows, so no split uses it and the frame
     leaves it out.
   - The roughly 3.8x step in rows per quarter is the row budget. Each train side is a random 1M of 3.8-4.9M exits,
     while each test window keeps 500k of 594k-632k. The full data hold about 600k exits a quarter throughout.
   - The README does not say any of this, so a user reads two regimes.
   What is real (split auditor, task gamer):
   - Codings differ by release. Local-board codes agree on only 68.6% of matched exits between the PY 2023 Q4 CSV
     and PY 2024 Q4 (statewide code against local board). PIRL 108B is missing in 19, 36 and 24% of the rows of the
     three files.
   - Montana's pre-entry wages are blank for 88-100% of its exits from 2023Q4 on (Appendix C).
   - The altered wages are re-drawn in each release.
   - 413-423 participations appear twice across releases, at the file boundary and in training only.
   - Measured cost: up to 0.001 ROC AUC, except Montana (+0.003 on r2 when it is dropped).
   Wording:
   - The splits comment derives the 9-month gap from DOL's four-quarter fill, which would imply 12 months: 12.3-15.1%
     of the train sides are exits DOL had not published when the window starts. The gap holds on the state's own
     wage-record timing; say that.
   - The prediction point is the last planned service. The exit is recorded after 90 days without service and
     dated back to it (20 CFR 677.150(c)). The information set does not change.
   Small fixes:
   - Mask PIRL 304 when it is after the exit (2,197 rows), like the other dates.
   - Add a note on PIRL 935 code 2 ("Retirement"; its timing is unknown; 1,871 rows).
   - Count the README's decision tables on the shipped population (PIRL 301 code 9: 11,565 in the table against
     10,285 in the notes).
   Remedy: notes, the rewording and the PIRL 304 mask. Nothing here is a reason to hold the dataset back.

Not argued:
- Decoding the SOC, NAICS and CIP codes (CLEAN-12) is a batch call; decide it alike with rais issue 5 and sinan
  issue 4.
- The unknown levels kept as codes (CLEAN-10) are quality only.
- The labels of other test windows inside data.parquet (task gamer, exploit 2) are a harness matter for every
  temporal dataset, not for this definition.

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: wioa_employment_after_exit (folder wioa_employment_after_exit_1m), 2026-11-09

The advocate argues for the same shape I ask for: Title I only, one use case, roc_auc, Texas 2025Q1 and AS/PW cut,
and race, ethnicity and sex dropped. Three disputes are left: age and disability, the first-report revision that
remains after the Texas cut, and the previous outcome. One new measurement of mine changes my point 5 for Title I.

A1 (the task is real, has no leak and has headroom). Conceded. I never asked for exclusion. I also agree that the
   empty 2024Q2 and the 3.8x step come from the gap and the row budget. One correction: "no leak" holds only after
   the cuts the advocate concedes in A2 and A4, because those labels are LEAK-24 and LEAK-25 problems. The README
   must say why 2024Q2 is missing and why the density steps (writing.md), since the blind reviewer read both as two
   regimes.

A2 (Texas, AS and PW cut; the rest of the newest window "in band"). The cut is conceded by both sides. I dispute
   "in band", because tunisian's 2017 does not fit.
   - Tunisian kept 2017 because no censoring was measured there (p = 0.36).
   - Here a revision is measured on the same rows. Between the 1st and 2nd report, 2,574-3,473 exits per quarter
     flip from No to Yes. The rate rises 0.7-1.1 points by the 3rd report (split auditor), and the Title I rate
     rises too (+0.31 / +0.72 / +0.01 points from the 1st report to the 2nd).
   - LEAK-24 is a Must with no severity grade, and a Must takes no exception (principles.md).
   Keeping the rest with a note therefore needs the curator to amend LEAK-24, grading it by size (about -0.003
   ROC AUC, no model reordered). I support that amendment rather than the window shift. A note alone does not
   settle a Must.

A3 (Title I only). Agreed; there is nothing to rebut. The Texas cut still applies in Title I: 2,586 rows at 0.539,
   against 0.704-0.816 in other Texas quarters (advocate a2).

A4 (invalid SSN: the rule finds only 1,240 Title I rows because blank wages are filled with 0 there). Conceded for
   Title I, on a new measurement (c1_t1_invalid_ssn.{py,log} in the run's panel folder, the column auditor's clean_full.parquet).
   The zero fill does hide the unmatched exits. Among Title I exits with no positive pre-entry wage:
   - with an invalid SSN: 26,500 exits, 0.316 employed;
   - with a valid SSN: 198,387 exits, 0.554 employed;
   - 24,774 of the 26,500 are in New York, at 0.324 against 0.424 for New York's valid SSNs;
   - no state with 100 or more such exits is at or below 0.05.
   So in Title I no rule that ignores the label locates a near-zero "not recorded" set, the way the all-programmes
   rule did (19,556 exits at 0.022). The 1,240 rows at 0.204 are a mix too.
   Remedy, now milder: drop AS and PW (all No, confirmed by Appendix B). Drop or keep the 1,240 rows; dropping is
   cheap. Keep the rest with a note naming New York's invalid-SSN group (0.324 against 0.424). That is LEAK-25 as
   amended 2026-11-02, with the state shipped as a feature. If the curator keeps all programmes, my point 5 stands
   in full: drop the 19,556.

A5 (metric). Agreed: roc_auc once the cohort-rate clause is removed, log_loss if it stays (MET-1, MET-8).

A6 (protected grounds; age and disability left to the curator). The drop of race, ethnicity and sex is agreed. On
   age and disability I keep my position. The advocate concedes UIPL 41-94 and cannot rebut it. Its two reasons for
   keeping them do not carry:
   - The barrier-group lists (29 U.S.C. 3102(24)(D),(E)) decide who the programmes serve and who gets priority, by
     policy. They do not make age a criterion inside a follow-up score. Follow-up eligibility (20 CFR 678.430(c),
     680.150(c)) names neither age nor disability.
   - That also sets acs apart: SNAP's own eligibility determination uses age and disability, and this decision's
     rules do not.
   - 20 CFR 677.170(c)(2) covers the aggregate adjustment model. That model also uses race and sex (Att. II, Table
     1), so it licenses no per-person use of age and disability, any more than of race and sex.
   On 701 (pregnancy) and 803 (limited English): the advocate lists them in the drop's note. They are WIOA barrier
   groups too, so they should be decided with age and disability under one reading, not separately.

A7 (previous outcome: ship without it, because Texas ids link for only 22.1% across files). Disputed.
   - The id fact is real but bounded. Every other state links at 92.8% or better (claim auditor), and the split
     auditor matched 96.5% across the CSV and PY 2024 Q4.
   - Texas and Utah are about 12% of a test window, and returning persons about 10% of those, so roughly 1% of test
     rows are affected. After the Texas 2025Q1 cut, Texas rows remain in the 2024Q3 and 2024Q4 windows, and their
     look-back crosses the PY 2024 Q4 to PY 2025 Q3 boundary.
   - A link that fails turns a returner into "none". That is a gap in coverage that does not depend on the class,
     like any person the state cannot link. It is not a label leak.
   - The overall gain (+0.0008 / +0.0013) is a paired difference on one training sample. The split auditor says
     such comparisons are "much steadier" than the 0.004 spread between samples, so the run-to-run spread is the
     wrong yardstick. On the returners the feature concerns, the gain is +0.007 to +0.008.
   - USE-10 is a Must, and the coverage gap is a fact for a note, not for leaving the feature out of the 88% of rows
     whose ids link.
   Remedy, mildest:
   - Add the feature as the split auditor built it.
   - Set it to "unknown" rather than "none" for Texas and Utah rows whose look-back crosses a file boundary where
     the ids do not link (a rule on state and date, not on the label), and say so in a note.
   - Re-measure the gain on the Title I population, which nobody has measured.
   The alternative remains the one I named: the curator amends USE-10 for a negligible gain, as a deliberate change,
   not an unrecorded departure.

"Changes that need no decision": agreed, all of them.

Where we still differ, for the mediator:
- Age and disability: drop (UIPL 41-94) or keep (WIOA barrier groups). This is the curator's call on SEL-1 and the
  Tensions row; the dataset ships either way.
- The first-report revision outside Texas: an amendment of LEAK-24 is needed to keep it with a note.
- USE-10: add the feature with "unknown" for the links that fail, or amend the rule.

</details>
