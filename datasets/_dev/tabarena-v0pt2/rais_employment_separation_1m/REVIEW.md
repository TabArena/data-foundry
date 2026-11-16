# rais_employment_separation

**Outcome:** added as `rais_employment_separation_1m`. The AI recommends shipping it after two more changes it
recommends but has not made (issue 3, private employees only; issue 5, decode the codes); the panel's own changes are
made, and issue 1 confirms what is implemented. The task is ours, built on Brazil's labour census (RAIS, base year 2025,
91.7 million employment links): on 1 February, after the January payroll, will an employee in a formal job resign
before the year ends? A random 1.5 million of the 58.6 million links in post on 1 February (7.3% of the shipped links
quit, 7.15% of all such links), shipped as one year in three random folds of 1M training and 500k test links; fallback
`roc_auc`.
Verdict: ship after changes (made).
Validity: SEL-1 triggered (the worker's sex, race, age, nationality and disability in an employer's retention score,
which Brazilian law bars) and fixed by dropping all five, on the "factor the actor may no longer use" stance extended
to any decision the actor's own law constrains (issue 1 confirms the extension); USE-1 holds, fit approximate, and
USE-8's note now names the pooled public servants and military, the dormant links and the fake layoffs; LEAK-25
triggered for the armed forces (3 separations recorded in 418,633 links in 2025) and fixed by dropping them, not
triggered for the wider dormant links (their outcomes are recorded, measured); LEAK-10 triggered (contract type shows a
later conversion of fixed-term contracts) and fixed by a merge for recent hires; LEAK-10 and LEAK-13 weak (the rebuilt
tenure marked the class) and fixed; SPLIT-8 applied (forced IID, the 2022/2023 series break as the reason, a
2024-trained model 0.006 lower on 3 of 3 folds).
Value: no task-probe flag; untuned LightGBM 0.791 against linear 0.770 and dummy 0.5; five learners keep their order
when the public servants leave; leaving out the dormant links, or keeping only the links paid in January, swaps two
adjacent learners (0.0006-0.0012 apart, 3 of 3 folds).
Quality: CLEAN-12 departure open (issue 5); CLEAN-11 negative January pay set to missing.
Weighed: gap 0 (social science is not thin among the 151 accepted definitions), source + (the ministry's census),
shape + (millions of links, mixed features), use case 0 (ours), the pooled population and the dormant links - (issues
2, 3).
For the curator: issue 1 (confirm the stance), issues 2 and 3 (framing calls), issue 4 (target breadth), issue 5
(codes).

**Main points:** Confirm that the five protected grounds leave under the extended stance (issue 1, implemented,
recommended); keep the dormant links with the note (issue 2, implemented, recommended); keep only the private employees
or keep the public servants and military pooled with the note (issue 3: pooled implemented, private recommended); count
agreements as No (issue 4, implemented, recommended); and keep the national classifications as codes or decode them
into words, alike for sinan_dengue_case_screening_1m (issue 5: codes implemented, decode recommended).

**Record judgment:** valid. The record's fields agree with the definition: the record's `Temporal (NON-IID)` split and
tag are the source regime, which the definition's `ForcedIIDFromTemporal` tag records. The screening's prediction
point of 1 January moved to 1 February (January pay is the first pay known before the outcome), and the screened
"contracted wage" and "establishment size" are not inputs (the 2023+ files carry no contracted wage; the size is that of
31 December).

**Issues for Lennart:**

1. **Keep the five grounds Brazilian law bars an employer from using (sex, race, age, nationality, disability) out of the features, as now, and so extend your insurance-pricing stance to any decision on a person whose factor the actor's own law bars?**

   * **Problem:**
     - The use case is an employer's retention offer, and Brazilian law bars an employer from using sex, origin, race, colour, disability or age in any practice for giving or keeping a job, so the definition now drops all five grounds[^law][^sel1].
     - Your stance that such a factor leaves the features is written for insurance pricing, so applying it to any decision on a person where the actor's own law bars the factor extends it, which needs your confirmation[^row].
     - Age carries nearly all of the 0.006-0.007 ROC AUC the drop costs; the other four carry at most 0.001.
   * **Background:**
     - A retention offer (a raise, a talk, a training plan) is a practice "for the maintenance" of the employment relation, which the law names; a raise is also pay, where the Constitution (art. 7 XXX) bars differences by sex, age and colour.
     - The law was in force in 2025, the data's year, so the stance's exception for a use case set in the data's own time does not apply.
     - Age was no leak (it is read at one fixed date for leavers and stayers); it leaves only because the law lists it.
   * **Effect on the task:**
     - ROC AUC falls by 0.006-0.007, nearly all of it age; sex, race, nationality and disability carry at most 0.001.
     - Exact duplicate rows rise from 0.8% to 4.0% of the data, as profiles get coarser (two thirds of them public servants or state military).
   * **Experiments:**
     - Column auditor, untuned LightGBM, 600k training and 400k test links, 3 seeds: dropping sex and race -0.0006 to -0.0011; the four grounds other than age -0.0001 to -0.0008; all five -0.0059 to -0.0065.
     - Domain practitioner, shipped fold 0: 0.7917 with all features, 0.7916 without the four, 0.7845 without all five.
   * **Consistency:**
     - Follows bemtpl97 and the insurance family, where sex left the features even where the actor's law allowed it; here the actor's own law bars all five, a stronger case.
     - The first case outside pricing: hr_analytics keeps `gender` in a recruiter's decision (never reviewed), and the stance itself marks home_credit_default_risk and credit_card_clients_default (sex kept) "not reviewed yet".
     - wioa_employment_after_exit drops race, ethnicity and sex under 29 CFR 38.6(b) and UIPL 41-94, and asks about age and disability in its issue 1, to be decided after this one; ny_wcb_assembled_claims_1m's reason is claims triage, not pricing. Each is decided in its own REVIEW.md on the stance you confirm here.
   * **Panel:**
     - All agents agree on dropping all five: the critic because the definition can remove the concern and keep the task, the advocate because no fact sets this case apart, the domain practitioner because a legal team would ask for it.
     - The builder had leaned to keeping them with a note or dropping sex and race only; the precedent checker found that the second follows neither the insurance stance (sex only) nor the legal reasoning (every listed ground).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop all five, stance extended to any decision the actor's own law constrains (implemented) | sex, race, age, nationality and disability leave; the stance covers any decision on a person where the actor's own law bars the factor; accepts the duplicate-rows warning (4.0% exact duplicates, two thirds public servants or state military) | follows the stance's own reasoning; the law lists all five; small cost | the first case outside pricing, so the stance's text changes; age is a real signal; duplicates rise to 4.0%; reaches hr_analytics and the two credit tasks when they are reviewed |
     | B | Drop four, keep age as an exception | sex, race, nationality and disability leave; age stays; the stance's amended text names age as allowed to an employer | keeps the one ground with signal (0.006) | the law lists age with the others; no fact yet sets age apart; the size of a gain sets no case apart |
     | C | Keep all five, stance for pricing only | the five stay with a note; the stance's text says pricing only | keeps the data's full signal | no fact sets the case apart from bemtpl97; a fixable ethics concern left open; hr_analytics and the credit tasks stay as they are |

   * **Recommendation:** A, the stance's own reasoning applied to the actor's own law; then wioa_employment_after_exit and ny_wcb_assembled_claims_1m are decided on the extended stance in their own issues. **Decision:** A, B or C?

   **Notes for the AI:**
   - A: write the extension into the Tensions row of `principles.md` (the row "A rating factor known at the prediction point against a factor the actor may no longer use"): its first stance gains "and in any decision on a person, a ground the actor's own law bars for that decision leaves the features (amended <date>, Lennart, on rais_employment_separation: Lei 9.029/1995 art. 1)", and its cases gain "rais_employment_separation: sex, race, age, nationality and disability dropped from an employer's retention score". Record a `CC` line in the record. Accepted-warning text (`dataset_duplicate_rows`): "4.0% exact duplicates: different workers with the same coarse features once the protected grounds left (0.8% before), two thirds public servants or state military; 5.0% of each test fold has a copy in training, 0.1% with another label only." Then raise the issue in the REVIEW.md of wioa_employment_after_exit and ny_wcb_assembled_claims_1m (one issue each), and in hr_analytics' when it is reviewed.
   - B: remove `age` from `PROTECTED_GROUNDS`, add `"age": list(range(14))` back to `PROXY_MISSING`, and write the age carve-out into the Tensions row as part of the amendment (SEL-1 is a Must, which takes no exception: principles.md, 'Exceptions and amendments'); re-run `dataset check`, the leak and task probes.
   - C: restore the five columns (`sex`, `race`, `age`, `nationality`, `disability_type`) with their decodes (sex, race with 9 missing, the layout's nationality and disability-type lists) and `disability` as a copy of the type; write the stance's "pricing only" scope into the Tensions row; re-run the same checks.

   [^law]: Lei 9.029/1995 art. 1, as amended by Lei 13.146/2015: "É proibida a adoção de qualquer prática discriminatória e limitativa para efeito de acesso à relação de trabalho, ou de sua manutenção, por motivo de sexo, origem, raça, cor, estado civil, situação familiar, deficiência, reabilitação profissional, idade, entre outros" (https://www2.camara.leg.br/legin/fed/lei/1995/lei-9029-13-abril-1995-348798-normaatualizada-pl.html).
   [^sel1]: **SEL-1** (Must): a task with ethical concerns is out; a Must the definition can fix is fixed rather than excluded (principles.md, "How to decide", the remedy ladder).
   [^row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; USE-1, USE-6): the actor's legal constraint today; bemtpl97 (Lennart, 2026-11-05: a model "would not be able to use sex"); australian_vehicle_insurance_2004_2005 (Lennart, 2026-11-08: "as if we were to simulate the case in europe always").

2. **Keep the dormant links (paid in no month of the year and on no leave) with a note, as now, or keep only the links paid in January?**

   * **Problem:**
     - 7.7% of the rows were paid in no month of 2025 and had no leave day; 0.9% of them quit against 7.8% of the others, so they are easy negatives worth 0.013 ROC AUC.
     - The panel measured that the source records their outcomes when they come, so they are not rows without a target like the abandoned links or the armed forces, and a rule that reads the year's pay would choose the rows by the future[^l25][^l22].
     - An HR team scoring "its staff after the January payroll" may not count links dormant for over a year; a cohort of links paid in January is known on 1 February but also removes staff on leave and links paid later in the year.
   * **Background:**
     - Of the Norte links in post on 31 December 2024 that were paid in no month and had no leave, a year later 4.2% had separated with a reason, 11.1% were paid again, 83.6% were still dormant and 1.1% carried the source's abandoned flag (a flag that recurs for 98.9% of its links).
     - 79% of the 2025 dormant links in Norte had been dormant all through 2024 too; 21% had been paid in 2024.
     - The definition does not read the pay of February to November; the dormant links were measured on the sample with the monthly pay.
   * **Effect on the task:** with them, part of the score is telling dormant links from working staff, which an HR team's own payroll does at once; without them, the task is the working staff only.
   * **Experiments:** five learners, 3 shipped folds, the panel's agreed state (mediator):

     | Cohort | LightGBM 15 leaves | LightGBM default | LightGBM, codes dropped | logistic | LightGBM 255 leaves |
     |---|---|---|---|---|---|
     | all links (implemented) | 0.7940 | 0.7886 | 0.7785 | 0.7757 | 0.7670 |
     | dormant links out | 0.7814 | 0.7754 | 0.7651 | 0.7657 | 0.7521 |
     | links paid in January only | 0.7794 | 0.7730 | 0.7624 | 0.7636 | 0.7482 |

     - Both filters swap two adjacent learners (codes dropped and logistic, 0.0006 and 0.0012 apart) on 3 of 3 folds; the rest of the order stays.
   * **Consistency:**
     - The abandoned links and the armed forces left because their outcome is not recorded (zero or near-zero separations), as in caracas_cervical_cancer and account_debt_south_africa; the dormant links record 4.2% separations a year later, which sets them apart.
     - Dropping rows by an event after the prediction point selects the cohort on the future, which framingham_heart_study_fhs refused.
     - If issue 3 keeps only the private employees, 46% of the dormant links leave with the public servants (18.3% of the public rows are dormant, 4.9% of the private ones).
   * **Panel:**
     - Keep with the note (advocate, column auditor, mediator's lean): they record outcomes, staff on leave belong to the use case, and the January-pay rule also drops 1.27 million links paid later in the year (6.1% of whom quit).
     - Filter (critic): a working employee unpaid and on no leave for a year is the source's own abandoned pattern without the flag; the critic's rule on the whole year's pay was ruled out by the mediator as selection on the future.
   * **Unknown:** the ministry's rules for flagging a link abandoned, which would say whether these links are on an employer's staff list.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with the note (implemented) | every link in post on 1 February; the notes give the dormant share and its cost | mildest; the source records their outcomes; keeps staff on leave | 7.7% easy negatives in the score (+0.013) |
     | B | Keep only links paid in January | rows with January pay above 0 (known on 1 February); about 11% of the links leave | the payroll the actor scores after; fewer easy negatives | also drops staff on leave and links paid later in the year; one adjacent swap of two learners |

   * **Recommendation:** A, the mildest framing that rests on what the source records; B if you read the actor's staff as the January payroll. If issue 3 keeps only the private employees, 46% of the dormant links leave with the public servants, and this choice weighs less. **Decision:** A or B?

   **Notes for the AI:** B: in `_clean`, keep the rows with `pay_january > 0` after step 1 (a rule known on 1 February, not reading the label); rewrite `task_summary.row`, `changes` and `fit_reason`, the cohort and dormant-link bullets of `curation_comments` and decision 1's text; re-run `dataset check`, the leak and task probes.

   [^l25]: **LEAK-25** (Must): "No event" mixed with "not recorded" is a censoring bias; unrecorded rows located by a rule that does not read the label are dropped (amended 2026-10-21, Lennart, on caracas_cervical_cancer, account_debt_south_africa and fraud_detection_in_electricity_and_gas_consumption_1m).
   [^l22]: **LEAK-22** (Must): a competing event after the prediction point keeps its label; dropping it selects the cohort on the future (framingham_heart_study_fhs, Lennart, 2026-10-22).

3. **Keep the public servants and military pooled with the private employees, as now, or keep only the private employees?**

   * **Problem:**
     - 19.4% of the rows are statutory and other public servants and state military (eSocial worker categories 301-310), of whom 1.3% quit against 8.8% of the private employees (categories 101-111).
     - No private HR team scores tenured servants or soldiers, and a public body does not make individual retention offers, so these rows are a population the named actor does not share[^use1][^use8].
     - Pooled, the untuned score is 0.789 ROC AUC; trained and tested on the private employees only it is 0.746, and the order of five learners stays.
   * **Effect on the task:** about 0.043 of the pooled score is telling civil servants from private staff, a ranking no employer makes; the ranking of models is the same either way.
   * **Experiments:** five learners, 3 shipped folds, the panel's agreed state (mediator):

     | Cohort | LightGBM 15 leaves | LightGBM default | LightGBM, codes dropped | logistic | LightGBM 255 leaves |
     |---|---|---|---|---|---|
     | pooled (implemented) | 0.7940 | 0.7886 | 0.7785 | 0.7757 | 0.7670 |
     | private employees only | 0.7535 | 0.7458 | 0.7381 | 0.7381 | 0.7195 |
     | pooled model, scored on private rows | 0.7539 | 0.7464 | 0.7384 | 0.7373 | 0.7205 |

     - Kendall tau of the order against the pooled one: 1.0, 0.8 and 1.0 by fold, the one swap a tie to four decimals; spread best to worst 0.027 pooled, 0.034 private.
     - The pooled model scores the private rows as well as one trained on them, so the public rows do not distort training.
   * **Consistency:**
     - Keeping a selection the setting does not share, named in the fit, follows superconductivity (approximate fit with a named gap); no precedent decided a population filter of this kind the other way.
     - chile_school_dropout_mineduc_1m (this batch) keeps the source's population over a deployed list's narrower one; there the source paper defines the population, here the use case is ours.
     - The two warnings of `dataset check` on pure feature values (statutory servants, the state executive) are the same fact; under B they would mostly go.
   * **Panel:**
     - Private only (critic, domain practitioner, blind reviewer): no private HR team scores these rows, and 1.2 million or more private links remain.
     - Pooled (advocate): an approximate fit stands when its gap is named, and a payroll vendor's pooled model is a real user.
     - Mediator: no rule forces the filter; it matches the named actor more closely, and it changes the level, not the ranking.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Pooled, with the note (implemented) | every formal link; the fit names the 20% public servants and military and the private-only score; accepts the two pure-feature-value warnings (statutory servants, the state executive) with the career-stability reason | the census population; no new filter | a fifth of easy negatives the actor never scores; two pure-feature warnings to accept |
     | B | Private employees only | keep worker categories 101-111 (about 80% of the links); public servants, military, casual workers, directors and union leaders leave | the named actor's staff; the warnings go; ranking unchanged | a narrower task than the census; leaves public employers' own turnover out |

   * **Recommendation:** B, the population the use case names, at no cost to the ranking of models; A if you keep the census population with the gap named. **Decision:** A or B?

   **Notes for the AI:**
   - A: Accepted-warning text (`dataset_pure_feature_value`): "Statutory civil servants (contract type) and the state executive (legal nature 1023) almost never resign: 0.3-0.4% against 7.3% overall, the career stability of tenured public employment. The attributes are the link's contract and employer, known on 1 February, not recorded after the outcome." (The armed forces, the old reason's legal nature 1015, left under LEAK-25.)
   - B: in `_clean`, keep the rows with `worker_category` 101-111 after step 1 (label-free, known on 1 February); rewrite `task_summary.row`, `fit_reason`, the population note and decision 5's table; the sample keeps about 1.57 million links, above the 1.5 million budget (check it). Re-run `dataset check`, the leak, task and hidden-group probes.

   [^use1]: **USE-1** (Must): a use case is an actor, a moment and a decision; check every column, filter, target and split choice against it.
   [^use8]: **USE-8** (Must): write how closely the data mirrors the use case; approximate is a stand-in with a known gap, named as such. Against it, as a weighed factor: a use case rephrased only to excuse a gap (use_case.md, USE-9).

4. **Count a termination by agreement (code 90) as No, as now, or as a quit?**

   * **Problem:**
     - Since the 2017 labour reform an employer and an employee can end a job by agreement (art. 484-A CLT), with part of the severance; 6,488 links of the sample, 4.5% of the quits if counted as Yes.
     - The domain practitioner says the employee usually asks for it, to leave with 80% of the severance fund, so it is the departure a retention offer targets; but the employer must agree, and the files cannot show who asked.
     - Which separations are the actor's event is a target call the rules leave to the case[^use5].
   * **Effect on the task:** under A, a retention list trained on this target treats an employee who asks for an agreement as a stayer; under B, some exits the employer started count as quits.
   * **Experiments:**
     - Untuned LightGBM trained on quits, 3 shipped folds: it ranks the links ended by agreement above the stayers at ROC AUC 0.66-0.67, dismissals without cause at 0.69, ends of contract at 0.74 and resignations at 0.82; by the features, agreements look like dismissals.
     - Counting 90 as Yes lowers the score by 0.006-0.008 and keeps the order of five learners (Kendall tau 1.0 on 3 of 3 folds).
   * **Consistency:** No precedent decides which separations count as the actor's event.
   * **Panel:** Yes (domain practitioner); No (builder); the mediator found the data cannot settle it.
   * **Unknown:** a source on who initiates the agreements of art. 484-A.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No (implemented) | agreements count with dismissals; Yes is codes 20 and 21 | the employer's consent makes it a joint decision; by the features it looks like a dismissal | some departures a retention offer could prevent count as No |
     | B | Yes | codes 20, 21 and 90 are Yes (+4.5% positives) | the departure the employee usually asks for | mixes in separations the employer chose; lower score, same order |

   * **Recommendation:** A: an agreement needs the employer's consent, so it is not the employee's own exit the target names, and the files cannot show who asked; B if you read the retention offer as aimed at every departure the employee seeks. **Decision:** A or B?

   **Notes for the AI:** B: add 90 to `QUIT_REASONS`. That constant feeds `_prepare_raw_files` (its counts), so the prepared files are rebuilt (one pass over the 23 GB, about 3 minutes and 15 GB of memory); rewrite `task_summary.predicted`, the target bullets and decision 2; re-run `dataset check`, the leak and task probes and the forced-split cost.

   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it; the details are decided case by case (diabetes_3, Lennart, 2026-10-21).

5. **Ship the occupation, sector, legal-nature and municipality codes as codes, as now, or decode them into "words [code]" from the current official tables?**

   * **Problem:**
     - Occupation (CBO 2002, 2,523 levels), sector (CNAE 2.0 subclass and class), legal nature (CONCLA) and municipality (IBGE) ship as zero-padded codes, where your rule decodes a code into the words its codebook gives[^c12].
     - The stated reason is now that the release's codebook, the 2020 layout, is older than the 2025 codes: it lacks 6.4% of the occupation rows, 1.2% of the CNAE subclass rows and 11.8% of the legal-nature rows, and names no CNAE class.
     - The current official tables (the ministry's CBO list, CNAE 2.3 and natureza jurídica 2021 at IBGE, the IBGE municipalities) would decode them all.
   * **Background:** the earlier reason, that the digits carry the classifications' hierarchy, does not hold for a model that reads a category; "words [code]" keeps the digits for a model that parses text.
   * **Effect on the task:** the same information either way for a model that reads categories; a model that reads text gets the words only under B; the codes ship as text either way, so a method that wants the integer parses it in both; the blind reviewer found LightGBM at 0.769 with native categories and 0.797 with the codes as integers (200k rows), so how a method treats these columns weighs on its rank.
   * **Consistency:**
     - sinan_dengue_case_screening_1m (this batch) keeps the same CBO and municipality codes, and wioa_employment_after_exit keeps its occupation, industry and CIP codes; chile_school_dropout_mineduc_1m keeps its communes as codes. A third exception of one reason makes an amendment of the rule due, so decide rais and sinan alike and say whether the rule should change for large national classifications.
     - ny_wcb_assembled_claims_1m decodes NAICS into "words [code]"; credit_g took the corrected code tables (Lennart, 2026-10-31: "we want the right labels in all cases").
   * **Panel:** the advocate and the critic both call it a quality call; the precedent checker recommends decoding, alike for sinan; the column auditor sees the rule and the ny_wcb form favouring the decode.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Codes, with the outdated-codebook reason (implemented) | as now; the note names the coverage gaps | no lookup files; no risk of a mismatched table | a departure from the rule; the words exist in current tables; a third exception of one reason in this batch |
     | B | Decode to "words [code]" from the current tables | four lookup files in the folder, pinned to their versions; every level gets its title | follows the rule and the ny_wcb form; right labels; digits kept | lookup files to source, pin and check |
     | C | Amend the rule for large national classifications | codes stay here, in sinan and wioa; the rule names the case | one decision for the batch | the rule's own example of a code to decode is an occupation, so the amendment goes against its wording |

   * **Recommendation:** B: the current official tables give every level its words, which the rule asks for, at the cost of four pinned lookup files; apply it alike to sinan_dengue_case_screening_1m's occupation codes (its place and unit codes stay codes, as its precedent checker reads them). **Decision:** A, B or C?

   **Notes for the AI:** B: source the CBO 2002 list (MTE), the CNAE 2.3 subclasses and classes and the natureza jurídica 2021 table (IBGE CONCLA) and the IBGE municipality list (the 2020 layout names all but 510183, 32 rows); ship them as small CSV files next to `dataset.py`, decode in `_clean` to "title [code]" (a code without a title raises), update the codes bullet and the `CODE_WIDTHS` docstring; re-run `dataset check`, the dtype and task probes. Raise the same issue's answer in sinan_dengue_case_screening_1m's REVIEW.md. C: write the amendment into CLEAN-12 in `cleaning_features.md` with its case rows.

   [^c12]: **CLEAN-12** (Should; amended 2026-11-01, Lennart): a code whose codebook says in words what it means is decoded into those words, a nominal code (a job, a building type) into a category of the words; when the same reason has produced three exceptions, the next pass proposes an amendment (principles.md, "Exceptions and amendments").

**Review panel:** ship after changes (mediator). Tier full: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator.
Claim audit: 36 claims and the proposed accepted warning tested; four refuted and fixed (the contract type's stability,
the scope of the abandoned-link rule, the tenure rebuild, the armed forces' "never resign"), five numbers corrected,
age's undocumented date traced (no leak), four low-stakes claims untested. Blind review: include with changes; its
main concerns were the undocumented tenure (fixed) and the random split (measured and noted). Task gamer: barely
gameable, no exploit above +0.001 ROC AUC. Debate: agreed on dropping the five protected grounds (issue 1 confirms the
stance), dropping the armed forces, the contract merge, the tenure fix, the split notes and the cleaning fixes;
disputed: the dormant links (LEAK-25, settled by measurement as recorded outcomes; the cohort stays a framing call,
issue 2) and the pooled population (USE-8, issue 3); code 90 (issue 4) and the codes (issue 5) are open calls.

<details><summary>Mediator</summary>

MEDIATOR REPORT: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-09

Read: principles.md; LEAK-6/7/22/25, USE-1 to USE-9 (df-large); dataset.py; builder_report.md; the reports of the
claim auditor (CA), column auditor (CoA), split auditor (SA), domain practitioner (DP), blind reviewer (BR), task
gamer (TG), precedent checker (PC); the advocate's and the critic's briefs and rebuttals.
My runs (thread caps 4): the run's panel folder (m1 the 2M sample rebuilt with Feb-Nov pay, identical to the prepared
sample on all its columns; m2 Norte 2024->2025 linkage; m3 shipped rows traced to the sample; m4 five learners x three
shipped folds x five cohort variants, in the agreed state; m5 summary). Logs and JSON next to the scripts.

**1. JUDGMENT RECORD**
Verdict: ship after changes.
Validity: SEL-1 triggered, fixed (sex, race, age, nationality, disability_type dropped; Tensions row "a factor the
  actor may no longer use" extended to decisions on employees, an amendment the curator confirms, issue 1);
  USE-1 holds (approximate); USE-8: fit_reason must name the pooled public/military 20% and the dormant 8% (fixed in
  the notes; filters are issues 2 and 3); USE-5 open on code 90 (issue 4);
  LEAK-25 triggered for worker category 314, fixed (dropped); NOT triggered for the wider never-paid group (measured:
  its outcomes are recorded; section 3a);
  LEAK-10 triggered (contract type converted after 1 Feb), fixed (merge for tenure <= 3); LEAK-10/LEAK-13 weak (tenure
  of January hires), fixed; age: no leak (one fixed reference date, measured; moot once age leaves);
  SPLIT-8 applied (forced IID, -0.0057 ROC AUC on the shipped folds, 0.004-0.005 of it same-year cell sharing),
  notes corrected (SPLIT-20 series break as the reason).
Value: TP no flags. Agreed state, pooled: LightGBM 15 leaves 0.794, default 0.789, codes dropped 0.779, logistic
  0.776, deep LightGBM 0.767 (spread 0.027, same order on 3 of 3 folds).
Quality: CLEAN-12 departure open (issue 5, decide alike for sinan); CLEAN-11 negative January pay to missing.
Weighed: the cohort (dormant links, issue 2) and the population (public servants and military, issue 3): level -,
  order of models unchanged or one near-tie swap; use case + (actor's staff).
For the curator: issue 1 (confirm the amendment, carry it to wioa and ny_wcb), 2 and 3 (framing calls), 4 (code 90),
  5 (codes).

**2. AGREED FACTS**
- RAIS 2025 link files, 91,710,262 links, sha256 verified; cohort 58,571,381 (in post 1 Feb 2025), quit 7.15%; the
  shipped 1.5M: 3 folds of 1M/500k, ~36,155 positives per test fold (CA 2, 3, 10, 35).
- Target codes 20/21 match the 2020 manual; commissioned exonerations are code 11; no December censoring (CA 12, 17).
- Post-outcome fields are all dropped; none should come back (CoA).
- The five protected grounds: Lei 9.029/1995 art. 1 bars them for "acesso ... ou manutenção" of a job; the four other
  than age carry <= 0.001 ROC AUC, all five 0.006-0.007 (CoA, 3 seeds; DP fold 0). Both sides: drop all five.
- Category 314 (armed forces): 3 separations in 418,633 links in 2025 against 254 of 12,651 sampled links in 2024;
  zero January pay 85.2% vs 3.3%: a recording change (CA AW). Both sides: drop it.
- Contract type is the year's last value: January hires on CLT fixed term (60) 98.9% separated vs 45.5% on 60->10;
  merging 60/65/70/75 into 10/15/20/25 for tenure <= 3 costs January hires 0.0175 ROC AUC (3 of 3), 0.001 overall;
  yearly change among stayers CBO 6.3%, hours 3.2%, contract 2.8% (CA 28). Both sides: merge.
- Tenure rebuild: January hires show 1-2 months only as leavers; the half-month guess is biased (0.34/0.42); gain
  <= 0.0005 (CA 18, CoA C, TG 3, BR 1). Both sides: tenure 0 for January hires, floor or the measured offset,
  normalise -0.0.
- Forced IID is SPLIT-8's regime: shipped-fold cost -0.0057 (3 of 3, SA); 0.004-0.005 of it is the year's quits shared
  within sector x municipality x legal-form cells; five learners keep their order (SA). The reason for one year is the
  2022/2023 eSocial series break (SPLIT-20), not a download count (SA 3, PC D2).
- Never-paid links: 9.6% of the cohort without pay in any month; 8.4% without pay and without leave, quit 0.98%, any
  separation 6.0% vs 27.5%; worth +0.015 ROC AUC as easy negatives (CA 2, CoA D).
- Public/military: 20% of a test fold, quit 1.2% vs 8.6%; pooled 0.792 vs private-CLT 0.747 (DP 3a).
- Number slips (CA 4): code 24 median age 38; hours 0/99 74% general employees; CNAE 95 99999 in 201,575 Norte rows;
  ~36,155 positives per test fold; exact copies agree 99.2-99.4%.
- roc_auc stays (MET-8 fallback) with a MET-1 note that it ranks pooled links; codes are a P7 call (both concede).
- Negative pay_january (1,041 rows) to missing (CLEAN-11; both rebuttals concede).

**3. DISPUTED FACTS, SETTLED BY MEASUREMENT**
3a. LEAK-25: are the never-paid, no-leave links "not recorded"? (critic: drop them; advocate: keep with a note)
  Decisive test: follow the links across years. Norte, 2024 links in post on 31/12/2024 linked to their 2025 rows
  (12 coded fields + tenure, unique matches, the CA c4 method; 1,696,586 of 3,570,779 links matched; m2_link.log):
    2024 state (in post 31/12)      -> 2025: flagged abandoned / never paid, no leave / paid again / separated
    flagged abandoned (28,849)          98.9% / 0.6% / 0.2% / 0.3%
    never paid, no leave (151,082)       1.1% / 83.6% / 11.1% / 4.2% (1.0% Jan, 3.1% Feb-Dec)
    paid (1,489,085)                     0.04% / 2.1% / 69.2% / 28.4%
  The 2025 cohort's never-paid, no-leave links: 78.6% were never paid all of 2024 too (separation 1.4%, quit 0.22%);
  21.3% were paid in 2024 (separation 9.0%, quit 0.87%). Shipped frame: 8.27% of rows, quit 0.85% vs 7.81%,
  separation 5.6% vs 29.5% (m3).
  Reading: the source records these links' outcomes when they happen (4.2% separated with a reason within a year,
  11.1% back on pay), and its own abandoned flag, which is persistent (98.9% re-flagged), reaches only 1.1% of them a
  year later. They are mostly long-dormant links, not unrecorded events. Unlike 314 (no separation recorded at all),
  caracas (0 positives where 11.8 were expected) or account_debt (0 bad debts of 12,167 vs 91.9%), no zero-recording
  is shown.
  Ruling: LEAK-25 (Must) is not triggered for the wider group, so it does not license a filter that reads pay to
  December and the year's leave. That rule would select the cohort on the future for rows that can still have the
  outcome, which LEAK-22 (Must; framingham) bars; the later-date licence of the LEAK-25 cases (fraud_detection) covers
  rows shown unrecorded only. What remains is a cohort framing call under USE-5/USE-8 (issue 2). The critic's rule
  falls; the note is required either way (USE-8).
  Effect in the agreed state (m4): pooled default LightGBM 0.7886; scored without these rows 0.7755 (-0.013); refit
  without them 0.7754. Order of the five learners: one adjacent swap (logistic 0.7657 over codes-dropped LightGBM
  0.7651, 3 of 3 folds; pooled 0.7757 vs 0.7785).

3b. USE-8: does the 20% public/military population need a filter? Does the order of models change?
  m4, agreed state, 3 shipped folds, private categories 101-111 only (train and test) vs pooled:
    learner                      pooled   private only   pooled model on private rows
    LightGBM 15 leaves           0.7940   0.7535         0.7539
    LightGBM default (63)        0.7886   0.7458         0.7464
    LightGBM, codes dropped      0.7785   0.7381         0.7384
    logistic, one-hot            0.7757   0.7381         0.7373
    LightGBM 255 leaves x 1000   0.7670   0.7195         0.7205
  Order unchanged: Kendall tau 1.0 / 0.8 / 1.0; the one swap (fold 1) is the codes-dropped vs logistic near-tie,
  equal to 4 decimals on the mean. Level -0.043; spread 0.027 pooled vs 0.034 private. The pooled model is as good on
  private rows as one trained on them (0.7464 vs 0.7458), so the public rows do not distort training.
  Ruling: no Must forces the filter. USE-8 asks that a selection the setting does not share be named (fit approximate,
  already so); the note is a change now. Filter or keep is a framing weighing (issue 3).

3c. The age reference date. Moot: age leaves under SEL-1. For the record, the fact is settled for the claim auditor:
  age is read at one fixed date (31/12 or year minus birth year) for leavers and stayers.
  - CA linkage: 430,953 leavers +1 year in 96.5-98.1% in every month (a separation-date age gives (12-m)/12 zeros).
  - CoA's own apprentice data reverses its reading (my count, non-disabled, non-end-of-contract leavers): ages 23 /
    24 / 25 / 26 = 7,834 / 1,835 / 67 / 20, a cliff after 24; stayers' tail is smooth (7,089 / 1,158 / 649 / 411).
    Under an age at separation no non-disabled apprentice leaver could be 24 beyond the stayers' rate of violations;
    under 31/12, leavers who left at 23 before their birthday show 24 and none show 25. The 24+/23 ratio of December
    leavers (0.155) equals the stayers' (0.163). CoA's expected "24/1 in January" counted every shown-23 January leaver
    as a true 23; most are true 22s.
  - CoA's +0.0006 came from a "harmonised" age that adds noise under the true reference. If age were ever kept, the
    note gives the measurement (onlinenewspopularity form), not "cannot verify".

3d. Code 90 (agreement, art. 484-A) under USE-5. Measured (m4, default LightGBM, 3 folds): the quit model ranks code-90
  links against stayers at ROC AUC 0.66-0.67 (mean p 0.08), like dismissals without cause (code 11: 0.69, 0.09) and
  below ends of contract (12: 0.74) and resignations (21: 0.82). By the features, agreements look like dismissals.
  Counting 90 as Yes (+4.6% positives) lowers the level by 0.006-0.008 and changes no order (tau 1.0 on 3 folds). The
  data cannot show who initiates. A target-breadth call the rules leave to the case (USE-5, "decide the details case
  by case"): issue 4.

**4. CHANGES TO MAKE NOW (no decision needed)**
C1. Drop sex, race, age, nationality, disability_type; replace the note with the reason (Lei 9.029/1995 art. 1, the
    actor's own law, in force in the data's year); `known` without them. SEL-1 (Must), Tensions row extended to
    decisions on employees (curator confirms the amendment text: issue 1). Cost 0.006-0.007.
C2. Drop worker category 314 with a decision table (2025 vs 2024 separations); rewrite decision 4 ("the abandoned flag
    is not the whole unrecorded pattern: the armed forces' outcomes are not recorded in 2025"). Re-run the check and
    rewrite the accepted-warning reason for legal nature 1015 (no longer the armed forces). LEAK-25 (Must).
C3. Contract type: for tenure_months <= 3, map 60/65/70/75 to 10/15/20/25; rewrite the "rare" note with 6.3/3.2/2.8%.
    LEAK-10 (Must), LEAK-6, LEAK-7. worker_category checked (m5 frame): no conversion signal (January-hire apprentices
    56.8% separated vs 74.7% of older ones; the experience contract sits in category 101 under types 60-75;
    temporaries 98.4% are their contracts' ends): say so in the note, no code change.
C4. Tenure: 0 for January hires (admission_month 1), floor or the measured offset instead of round-half-even,
    normalise -0.0, correct the note. LEAK-10/LEAK-13 (Must, weak; LEAK-6: a confirmed leak goes even when small).
C5. Split note: the 2022/2023 eSocial series break as the reason for one year (SPLIT-20), not COVID nor the download
    count; the shipped-fold cost (0.7971 vs 0.7915, one training year); the cell-sharing measurement (+0.004-0.005,
    memorising learners gain twice as much, order unchanged); "revisit when the post-2023 stretch holds six base years
    or linked microdata appear". SPLIT-8, writing.md.
C6. fit_reason and notes (USE-8, Must): name the 20% statutory servants and military (quit 1.2%) with the private-only
    AUC; name the dormant links (8.3% never paid and no leave, 79% of them dormant since at least January 2024 in the
    Norte linkage, worth -0.013 when left out) unless issue 2 filters them; name fake-layoff agreements (quits filed as
    code 11) as label noise. MET-1 note: roc_auc ranks pooled links, not one employer's staff.
C7. Code 90: cite USE-5, not LEAK-22, whatever the call (PC D4).
C8. CLEAN-12: the stated reason ("the digits carry the hierarchy") goes either way; the new reason or the decode is
    issue 5. CLEAN-11: negative pay_january to missing with a note.
C9. Numbers: the five slips of section 2; re-measure every note after the edits (writing.md).

**5. ISSUES FOR THE CURATOR (ranked)**
1. [P1, SEL-1 Must; Tensions row] Confirm the amendment: the row "a factor the actor may no longer use" covers
   decisions on employees where the actor's own law bars the factor (here all five grounds, age included).
   - Effect: -0.006 to -0.007 ROC AUC; four grounds carry <= 0.001.
   - Advocate (conceded): no fact sets the case apart; the law lists age with the others.
   - Critic: SEL-1 is a Must; a fixable Must is fixed; keeping any ground needs an amendment with a fact.
   - Decision: confirm the amended scope (recommended) or name a fact for keeping age. Then decide
     wioa_employment_after_exit_1m and ny_wcb_assembled_claims_1m (this batch) on the amended row, each in its own
     REVIEW.md issue (per-dataset rule); hr_analytics and the two credit tasks follow when reviewed. PC: wioa has a
     fact of its own (DOL's adjustment model uses the factors; a benefit, not a job decision); ny_wcb's is weaker.

2. [P3/P4, USE-5 and USE-8 Must; LEAK-22] Dormant links in the cohort: keep with a note, or define the cohort as
   links paid in January (pay_january > 0, known on 1 February)?
   - Effect: -0.013 (dormant rows out) or -0.016 (January-pay filter) on the level; one adjacent swap of two learners
     within 0.0006-0.0012, 3 of 3 folds.
   - Advocate: they record outcomes (now measured: 4.2% separate, 11.1% paid again a year later); staff on leave
     belong to the use case; the January-pay rule also drops 1.27M links paid later (quit 6.1%).
   - Critic: an HR team "after the January payroll" does not score links unpaid all year with no leave; the source
     drops the flagged 1.2% for the same pattern.
   - Settled already: the critic's all-year rule is out (section 3a: LEAK-25 not met; it would select on the future).
   - What would settle it: whether the actor's staff list includes links dormant for over a year (the ministry's
     rules for flagging abandoned links). Mediator's lean: keep with the C6 note (mildest; the January-pay filter
     also removes real staff).

3. [P3, USE-8 Must for the note; framing weighed] Public servants and military: restrict to private categories
   101-111, or keep pooled with the note (C6)?
   - Effect: level 0.789 -> 0.746; order of five learners unchanged (section 3b).
   - Critic and DP: no private HR team scores tenured servants or soldiers; the pure-feature-value warning is the
     same fact; rows stay plentiful (398k test rows).
   - Advocate: USE-8 keeps an approximate fit when the gap is named; a payroll vendor's pooled model (DP's second
     actor) is a real user; the filter changes the level, not the ranking (now measured).
   - Rule: neither side has a Must for the filter; USE-9 (vendor reading) against "a use case rephrased to excuse a
     gap" is a weighing. Mediator: no lean beyond the measurement; the filter matches the named actor more closely.

4. [P3, USE-5 Must] Code 90 (agreement, 4.6% of the Yes count if added): Yes or No?
   - DP: usually asked for by an employee who wants to leave (80% of FGTS); the departure retention targets.
   - Measured: by the features, agreements look like dismissals without cause (section 3d); adding them lowers the
     level 0.007 and changes no order.
   - What would settle it: a source on who initiates art. 484-A agreements; RAIS cannot show it. Either way cite USE-5
     and name the choice in the notes.

5. [P7, CLEAN-12 Should] National codes (CBO, CNAE subclass/class, CONCLA legal nature, IBGE municipality): decode to
   "words [code]" from the current official tables, or keep as codes with the exception "the release's 2020 codebook
   lacks 6.4% of the CBO rows and 11.8% of the legal-nature rows".
   - Both sides concede it is a P7 call; decoding the municipality from the 2020 layout is cheap (all but one code).
   - Consistency: decide alike for sinan_dengue_case_screening_1m (same CBO and municipality lists) and
     chile_school_dropout_mineduc_1m; a third exception of one reason means an amendment is due (PC D5); ny_wcb
     decodes NAICS as "words [code]".

**6. THE TASK GAMER'S EXPLOITS, MAPPED**
- #1 key sizes counted over train+test (+0.0009; +0.0005 with train rows only): transductive participant counts,
  LEAK-30 family / SPLIT-8 same-year sharing. New, below seed noise beyond the honest +0.0005; no column ships it.
  Not an issue. (TG's "ship an establishment size band": the only size is the 31/12 one, dropped under LEAK-10.)
- #2 co-workers' residuals (+0.00017): SPLIT-8 same-year sharing. Known (split note), measured by SA at +0.004-0.005
  for a memorising learner; the note gets the number (C5). Not a separate issue.
- #3 tenure artefact (+0.0002, <= +0.0005): LEAK-10/LEAK-13; the note says rounding hides it, refuted; fixed by C4.
- #4 exact copies (+0.00001): LEAK-18, known ("duplicates kept"); gain as noted; label agreement wording fixed (C9).
- Could not check, contract type and worker category as year-end values: LEAK-10, the "Potential leak, kept on
  purpose" note; contract type measured at +0.0175 on January hires, more than the note's "rare" says: fixed by C3;
  worker category checked, no conversion (C3).
- Could not check, January pay declared by 15 February: USE-3/LEAK-10. The actor runs its own payroll before it
  declares it; known to the employer at the prediction point. No action.
- No flaw that hurts an honest model (adversarial AUC 0.499).

**7. CONSISTENCY WITH PRECEDENT (from PC, checked)**
- Protected grounds (PC D1): follows bemtpl97 and the insurance family (the actor's legal constraint today); first
  case outside pricing, hence the amendment (issue 1). The answer must reach wioa_employment_after_exit_1m and
  ny_wcb_assembled_claims_1m in this batch, each as its own issue, decided alike or set apart by a named fact.
- One year, forced IID (D2): follows distribution_transformers_at_cauca_department; set apart from
  chile_school_dropout_mineduc_1m (seven years, temporal) by the 2022/2023 series break, once the note says so (C5).
- Age (D3): settled by fact (3c); moot.
- LEAK-25 (D4): category 314 follows caracas, account_debt, fraud_detection (located, dropped). Keeping the dormant
  links is not a departure: the fact that sets them apart is the measured recording (4.2% separations filed, 11.1%
  paid again, flag reaches 1.1%), where each precedent had zero or near-zero recording. Competing events labelled No
  follow framingham (LEAK-22); the same case bars the critic's future-reading filter.
- Code 90 (D4): no precedent; a first call under USE-5 (issue 4).
- Population (3b): keeping with a named selection follows USE-8 (superconductivity: a selection the setting does not
  share, approximate, named). No precedent decided a filter of this kind the other way.
- Codes (D5): CLEAN-12 departure with a reason that does not set it apart; issue 5, alike for sinan and chile.
- Register flags: drift "post-outcome feature" leans to removal (followed: C3, C4); amendment_due SPLIT-14 not
  touched (ships under SPLIT-8).

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR REPORT: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-08

Verdict: two validity findings (P4, Must) refute what the definition says about itself, plus one smaller leak. None
is fatal, and each has a mild remedy in the definition.
  (1) LEAK-10: contract_type is the year's last value. Experience contracts (CLT fixed term, code 60) that survive
      are converted to open-ended (code 10), so for recent hires the label "fixed term" means "left before
      conversion". This refutes claim 28 ("such changes are rare").
  (2) LEAK-25: 9.6% of the cohort has zero pay in every month of 2025 and almost never separates, so its "No" is
      mostly "not recorded". The armed forces record no separation at all in 2025. These rows add +0.015 ROC AUC as
      easy negatives. The abandoned-link drop (decision 4) catches only a small part of this pattern, and the
      reason given in the accepted warning for legal_nature 1015 is refuted.
  (3) The tenure rebuild marks the class (half-month guess biased, banker's rounding); the model gains about 0.

Scripts and logs: the run's panel folder (a1-a8 sample checks, b1-b5 models on the shipped container
and its folds, c1-c6 scans of the raw 2025 and 2024 .COMT files).

**TABLE (claim | source | test | result | evidence | rule)**
1  RAIS is the mandatory annual report | task_summary.row | not re-read | untested (low stakes) | - | PROV-1
2  Seven 2025 files, sizes, sha256 | download_description | sha256sum raw/2025/*.7z | HOLDS | all 7 prefixes match (0e4459ee.., d9c4e359.., dfd32817.., 4366dda3.., c7deb880.., d19f924d.., c537caaa..) | PROV-10
3  91,710,262 links, no ids | curation_comments | sum of counts csv; header | HOLDS | 91,710,262; no id among the 62 columns | -
4  year 2026 | year | mtime inside the archives | HOLDS loosely | the unpacked files carry 2026-04-28; the FTP posting date was not re-listed | PROV-8
5  CC BY-ND 3.0 (site), FTP none | license | WebFetch of the gov.br page | HOLDS | "Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada"; the page still says ";"-delimited .txt (the 2023+ files are comma .COMT, which the code handles) | PROV-10
6  de-para table not on FTP | download_description | not re-listed | untested | - | PROV-13
7  314 = armed forces | WORKER_CATEGORIES | sample profile | HOLDS | 14,319 links: all contract 30, legal 1015, CBO 0103xx 12,394 / 0102xx 1,916 | CLEAN-12
8  header identical 2024/2025 | HEADER assert | diff of the header lines | HOLDS | 2024 SP header == 2025 Norte header | -
9  no contracted wage | curation_comments | header | HOLDS | no `Vl Salário Contratual` | -
10 cohort 58,571,381; 6.0% hired in January | decision 1 | counts csv; sample | HOLDS | 58,571,381; 5.96% | USE-5
11 Mês Admissão 0 = before the year; Tempo Emprego to 31/12 or to the separation | notes | crosstab; Jan hires | HOLDS | admission_type 0 iff month 0 (1,880,744 rows); January-hire stayers' tenure_end 11.0-12.0 | -
12 Yes = 20, 21; 7.15% / 7.23% | decision 2 | RAIS 2020 manual (gov.br manualrais2020.pdf, F.3) + counts | HOLDS | manual: "20. Rescisão com justa causa por iniciativa do empregado (rescisão indireta)"; "21. Rescisão sem justa causa por iniciativa do empregado ou exoneração de cargo efetivo a pedido do servidor"; exoneration of a commissioned post is code 11, which the data show (category 302: 5,540 code 11 vs 731 code 21), so 21 is not inflated by employer-initiated exonerations; 4,188,474/58,571,381 = 7.151% | USE-5
13 dismissals, ends of contract, transfers, 90, retirements, deaths = No | notes | manual | HOLDS | as above; code 90 is "Desligamento por Acordo" (art. 484-A), an employer-employee agreement, so the call stays the curator's (issue 4) | LEAK-22
14 six undocumented codes, 3,038 links; 24 = CLT, median age 26 | notes | sample | count HOLDS, detail REFUTED | 58+52+34+43+2,684+167 = 3,038; but code 24 has median age 38 in the 2025 sample (42 in 2024): 39 type 10, 12 type 60, 6 apprentices, legal 2062. Codes 70-80 of the 2020 manual (retirements) never occur in 2024-2025, which supports 81/82 as renumbered retirements | writing.md
15 separation month iff reason; active iff neither | asserts | container build | HOLDS | the build passes the asserts | -
16 abandoned 24,481; 100% no pay Jan/Dec vs 14.7%/17.6% | decision 4 | sample | numbers HOLD; the conclusion is REFUTED in scope | the numbers reproduce exactly. But 5,561,852 non-flagged cohort links (9.6%) have zero pay in all 12 months and in December, i.e. the same pay pattern as the flagged links, and are labelled No (finding 2) | LEAK-25
17 quits spread over every month, no end-of-year drop | notes | months x reason, 2025 vs 2024 | HOLDS | quits Dec/Nov 1.03 (2025 private) vs 0.94 (2024). The December fall of non-quit separations in 2025 (code 11: 17,696 vs 27,174; code 12: 5,590 vs 14,034) is only in the public sector: Dec/Nov 4.3 in 2025 vs 9.2 in 2024, the 2024 municipal election year; private Dec/Nov 0.96 vs 0.95. No censoring of 2025's December | LEAK-24
18 tenure rebuilt: half-month guess; rounding hides the class-dependent precision | notes, _clean step 3 | separation day measured from all 2025 files; January hires; parity; model with January hires' tenure set to 0 | REFUTED (small effect) | measured mean separation-day fraction (Feb-Nov) 0.34 for quits, 0.42 for all leavers, 0.57 in December, against the 0.5 assumed. Among January hires, whose true tenure on 1 Feb is < 1 month for all, the rebuilt tenure is 0 for 61.8% of quitters vs 44.0% of others (single-feature AUC 0.590). Even values: quitters 0.573, other leavers 0.595, stayers 0.547 (banker's rounding of the k+0.5 values). Model gain about 0: overall AUC 0.79715 shipped vs 0.79732 with January hires' tenure set to 0; January-hire subset 0.7653 vs 0.7640 | LEAK-10, LEAK-13
19 post-outcome fields dropped; size class Zero = all separated | decision 3 | sample | HOLDS | size class 1: 41,187 links, 100% separated; share falls 0.33 -> 0.15 with size | LEAK-10
20 CNAE 95 is a conversion of CNAE 2.0 | notes ("our reading") | functional dependence, Norte 2025 (5,645,037 rows) | HOLDS | 0 of 1,164 CNAE 2.0 subclasses map to more than one CNAE 95 class; the 99999 rows (201,575 in Norte alone, not "77k") are mostly agriculture classes 01xxx | CLEAN-5
21 three flags are copies | notes | 2M sample | HOLDS | 100.0% agreement for each | CLEAN-5
22 sub-municipal codes all 999997 | notes | probe file | HOLDS | 0 coded values in all 14 files | CLEAN-5
23 proxy missing; hours 0/99 "mostly intermittent" | notes | sample; Norte band check | numbers HOLD, "mostly intermittent" REFUTED | race 9 3.8%, hours 0/99 2.3%, legal 9999 2.5%; Norte band 99 for every 0/99 row and no other; but only 24.5% of the 0/99 rows are intermittent (category 111) and 74.2% are general employees (101) | CLEAN-10, writing.md
24 work_municipality missing 99.6% | notes | sample | HOLDS | 99.6% | -
25 legal 1244, 1333, 4120 present | notes | sample | HOLDS | 192,487 / 19,540 / 7,012 rows | CLEAN-12
26 pay_january 0 for 14.7% of links in post; 11.8% of cohort, 3.0% of quitters | notes | sample | HOLDS (numbers) | 14.74%, 11.80%, 3.01% vs 12.48%; what these rows are: finding 2 | -
27 age: date undocumented, "cannot verify" | notes (potential leak kept) | link Norte 2024 stayers to 2025 leavers on 12 coded fields + tenure window, unique matches only; if age were taken at the separation, a share (12-m)/12 would show 2025 age = 2024 age | REFUTED as "cannot verify"; the leak it fears is ABSENT | 430,953 matched leavers: age(2025) - age(2024) = 1 for 96.5-98.1% in every separation month and 0 for only 0.07-0.16% (83% expected for February separations under the leak). 1,265,633 matched stayers: diff 1 for 98.7%. Age is read at one fixed date for leavers and stayers | LEAK-10, EV-1
28 occupation, contract, category, hours: "such changes are rare" | notes (potential leak kept) | link Norte 2024 Dec to 2025 rows without the job fields in the key; January hires by contract type; model with CLT fixed term merged into open-ended | REFUTED, and a LEAK-10 leak for recent hires | yearly change: CBO 6.3%, hours 3.2%, contract 2.8% of stayers; contract changed for 9.9% of quitters vs 4.7% of other leavers, mostly 60 -> 10 (conversion of the experience contract). Shipped January hires on contract 60: 98.9% separated (96.6% by April), 37.4% quit; on contract 10: 45.5% and 15.7%. Hires of Nov-Dec 2024 on 60: 97.0% separated. Merging 60/65/70/75 into 10/15/20/25: January-hire AUC 0.7666 -> 0.7491 (-0.0175 mean; 3 of 3 folds), overall -0.0011 | LEAK-10 (Must)
29 duplicates natural: soldiers, servants | notes; check info | shipped frame | composition HOLDS; mostly zero-pay rows | 0.78% excess duplicates; duplicate rows are 42.8% armed forces, 26.5% category 306, 11.3% state military, 10.2% category 301; 77.3% have pay_january 0 (11.8% overall). Across folds 0.91-0.94% of test rows have a train copy, label agreement 99.2-99.4% (not "all same label"); 182 rows in conflicting groups | LEAK-18
30 Spatial tag | data_tags | - | not tested | - | -
31 stacking 2024+2025 puts near-copies on both sides | notes (reasoning) | the linkage of 27 | HOLDS, now measured | 48.4% of Norte 2025 stayers admitted before the year match a unique 2024 row exactly on 12 coded fields + tenure - 12 (age +1 in 98.7%) | SPLIT-8, LEAK-17
32 2024: 87,747,220 / 56,388,578 / 7.1% | notes | counts csv | HOLDS | 87,747,220; 56,388,578; 7.10% | -
33 forced-split cost -0.006 (own folds) | notes | re-run on the SHIPPED folds: LightGBM on 1M links of 2024 vs within 2025 | HOLDS | 0.7976/0.7959/0.7985 IID vs 0.7908/0.7904/0.7932 from 2024: -0.0059 mean, lower on 3 of 3. The gap mixes in the 2024 election-year public-sector turnover and the 2025 recording change for the armed forces (finding 2) | SPLIT-8
34 2M uniform draw, 24,481 out, 1.5M stratified, 3 x 1M/500k | version_comment | container | HOLDS | 3 folds of 1,000,000/500,000, no overlap | -
35 metric: fallback roc_auc, no source metric | metric | web search again (RAIS + ML + turnover) | HOLDS | no RAIS quit-prediction study with a stated metric found. MET-2 per fold: 500,000 test rows, 36,155-36,156 positives (the builder's "14,390" is not the shipped fold), constant 0.5, random 0.499-0.504; no scoring columns needed | MET-1, MET-2, MET-8, MET-11
36 Lei 9.029/1995 art. 1 | notes | WebFetch of the Câmara text | HOLDS | text as quoted, including "deficiência, reabilitação profissional, idade, entre outros" | SEL-1
AW accepted warning: legal 1015 (mostly armed forces) "almost never resign: a category effect of tenured public employment" | builder's proposed accepted_check_warnings | 2025 vs 2024 by worker category; all 2025 files | REFUTED for the armed forces | category 314: 0 separations of 14,319 sample links in 2025 vs 254 of 12,651 in 2024; zero January pay 85.2% in 2025 vs 3.3% in 2024; all files 2025: 418,633 links, 3 separations. The armed forces' outcome is not recorded in the 2025 release; it is not a behaviour | LEAK-25, EV-2

**REFUTED AND UNTESTED CLAIMS, RANKED (validity first, Must first)**
1. [P4, LEAK-10 Must] Contract type shows the conversion after the prediction point (claim 28).
   What it changes: CLT links on an experience contract on 1 February that survive it appear as open-ended. The
   label "fixed term" then marks the hires who left before conversion: January hires on 60 are 98.9% separated vs
   45.5% on 10. The leak is worth 0.0175 ROC AUC on January hires (6% of rows, 3 of 3 folds) and 0.001 overall,
   and it affects the hires of November 2024 to January 2025.
   Mildest remedy: for links with tenure_months <= 3, merge the four CLT fixed-term levels into their open-ended
   twins (60->10, 65->15, 70->20, 75->25). For older links the type is stable: on 60, 26% separate vs 21% on 10.
   Simplest alternative: merge them for every row, at a cost of 0.001 overall. Rewrite the "rare" note with the
   measured rates: CBO 6.3%, hours 3.2%, contract 2.8% per year for stayers (Norte linkage, an upper bound with
   linkage noise).

2. [P4, LEAK-25 Must; P3 USE-5] Zero-pay links are labelled No without a recorded outcome (claim 16 in scope,
   claim 29 interpretation, the accepted-warning reason).
   - All 2025 files: 5,561,852 non-abandoned cohort links (9.6%) have no pay in any month or in December. Their
     separation rate is 5.7% vs 30.0% and their quit rate 0.92% vs 7.96%.
   - General CLT employees (101): 2.64M such links, separation 7.2% vs 32.9%, and 75% have no leave days.
   - Municipal temporaries (306): separation 1.7% vs 34%.
   - Armed forces (314): 84% such links, and 0 separations recorded in 2025.
   Every one of these links has pay_january 0, so the model sees them at the prediction point. Scoring only the
   rows with January pay drops ROC AUC from 0.797 to 0.782 (-0.015, 3 of 3 folds); refitting without them gives
   0.7815 / 0.7805 / 0.7825. An HR team scoring "its staff after the January payroll" would not score links that
   are not on that payroll.
   Mildest remedy: a label-free rule known on 1 February: drop links with pay_january == 0 (11.8% of the cohort;
   this also drops 1.27M with later pay, quit 6.1%). Or follow LEAK-25's "located and dropped" with the all-year
   zero-pay rule (9.6%), noting that it reads later pay. At the very least, drop worker category 314 (0.7%;
   outcome not recorded in 2025) and rewrite the accepted-warning reason for legal 1015.
   Either way, rewrite decision 4: the abandoned flag (1.2%) is only part of the unrecorded pattern.

3. [P4, LEAK-10/LEAK-13, weak] Tenure rebuild (claim 18). The half-month guess is off: separations fall at 0.34 of
   the month for quits and 0.42 for all leavers (Feb-Nov). Rounding marks the class among January hires
   (single-feature AUC 0.590) and in parity. The model gains <= 0.001.
   Mildest remedy: set tenure_months to 0 for January hires (exact: < 1 month on 1 February). Use the measured
   offset (about 0.35-0.4 month, 0.57 in December) or floor instead of round-half-even. Correct the note.

4. [writing.md] Factual slips in the notes and the builder's report:
   - code 24's median age is 38, not 26;
   - hours 0/99 are mostly general employees (74%), not intermittent (24.5%);
   - CNAE 95 has 99999 in 201,575 Norte rows, not "77k";
   - the test folds hold 36,155 positives, not 14,390;
   - exact copies across folds agree on the label 99.2-99.4%, not "all".
   Remedy: correct the numbers.

5. [good news, LEAK-10] Age (claim 27) can be verified, and it is not a leak. Age is taken at one fixed date for
   leavers and stayers (2025-2024 age difference 1 for 96.5-98.1% of matched leavers in every month).
   Remedy: replace the "Potential leak, kept on purpose" note with the measurement.

6. Untested: claim 6 (de-para not on the FTP; FTP not re-listed), claim 1 (the decree), claim 30 (Spatial tag),
   claim 4's posting date. All are low stakes.

Holds that matter:
- The target codes match the 2020 manual, and commissioned exonerations are code 11, not 21.
- There is no December censoring in 2025: the 2024 December spike is the public sector in the election year.
- CNAE 95 is a pure function of the CNAE 2.0 subclass.
- Stacking the years would link 48% of rows.
- The forced-split cost re-measured on the shipped folds is -0.0059.
- The metric is computable on every fold.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR REPORT: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-08

Verdict: ship after changes. One confirmed leak to fix (age, LEAK-10), one small artefact to clip (tenure of January
hires), and three calls for the curator: the protected grounds (P1), a population question raised by the January pay
(LEAK-25), and the classification codes (CLEAN-12).

Judgment record:
  Validity: P1/SEL-1 open: the five protected grounds are model inputs in an employer's retention decision, which
    Brazilian law bars; the principles' tension row "a factor the actor may no longer use" points to dropping them
    (issue A). LEAK-10 triggered: `age` is measured at the separation date for leavers and at 31/12 for stayers.
    Measured, not just suspected: +0.0006 ROC AUC, 3 of 3 seeds (issue B). LEAK-10/LEAK-13 triggered, small:
    `tenure_months` = 2 is possible only for January hires who left (issue C). LEAK-25 question: 8.4% of the cohort
    are links that were never paid in any month in post and have no leave (quit rate 1.0%) (issue D). The other
    columns are known on 1 February.
  Value: no column changes the TP reading.
  Quality: CLEAN-12 departure (CBO, CNAE, legal nature, municipality kept as codes): the official tables decode them,
    and the 2020 sheets miss 11.8% of the legal-nature rows and 6.4% of the CBO rows (issue E). CLEAN-11: negative
    January pay (issue F). The other decodes match the 2020 layout.
  For the curator: issues A, D, E.

Sources read: dataset.py and claims.md; builder_report.md; probe outputs (leak, task_v2, hidden, dtype); the RAIS link
layout of 2020, downloaded from the FTP (ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/Layouts/vínculos/
RAIS_vinculos_layout2020.xls, saved to work_column_auditor/layout/), all sheets read; principles.md, use_case.md,
leak_checks.md, cleaning_features.md, selection.md (SEL-1) from the df-large worktree. The dtype probe was re-run into
work_column_auditor/dtype/: it flags the same 6 columns as the builder's run (numeric_levels on the code columns).

Data used: the cleaned frame through dataset_io (1,500,000 rows, 22 features + target); the definition's own `_clean`
run on the full 2,000,000-link prepared sample with the raw columns aligned (1,975,519 rows,
work_column_auditor/clean_full_with_raw.parquet); every 2025 apprentice link from the seven raw files (1,283,548
links, work_column_auditor/apprentices_2025.parquet); a 10% cohort sample from the raw files with the 12 monthly pays
(5,785,126 links, work_column_auditor/cohort_pay_10pct.parquet). Thread caps set on every run.

**COLUMN TABLE (column | meaning, layout 2020 | known on 1 Feb? | dtype and cleaning | verdict | rule)**

sex | SEXO: 1 masculino, 2 feminino, -1 ignorado | yes, a worker attribute | category Male/Female, 0 missing;
  decode matches the layout | fine as data; a protected ground under Lei 9.029/1995 art. 1 and CF art. 7 XXX ->
  issue A | SEL-1, tension row (USE-1, USE-6)

race | RACA_COR: 1 indigena, 2 branca, 4 preta, 6 amarela, 8 parda, 9 nao ident, -1 ignorado | yes | category,
  9 -> missing (3.8%); decode matches; 9 is 4.08% of No and 4.14% of Yes, so the missingness is not linked to the
  outcome | fine as data; protected ground (raca, cor) -> issue A | CLEAN-10 ok; SEL-1

age | IDADE: "Idade do trabalhador"; the reference date is not documented | NO for leavers: measured on the
  separation date for links that end, on 31/12 for the others (test below) | float, <14 -> missing (12 rows:
  ages 0, 11, 13), range 14-100, ok | LEAK (confirmed, weak: +0.0006 ROC AUC full model, +0.0095 age alone);
  also a protected ground (idade) -> issues A and B | LEAK-10 (Must), LEAK-6, LEAK-7

education | GR INSTRUCAO apos 2005: 1 analfabeto ... 11 doutorado, -1 ignorado | yes (the year's declared value;
  a degree completed during the year shows; negligible) | ordinal, 11 levels lowest first; the order matches the
  layout (ANALFABETO to DOUTORADO); no -1 in the data (decode would raise) | fine | CLEAN-12, CLEAN-14

nationality | NACIONALIDAD: 10 brasileira, 20 naturalidade brasileira (naturalised), 21-80 named countries | yes |
  category, 42 levels; 0 -> missing (0 rows in the sample); labels match | fine as data; protected ground
  (origem) -> issue A | SEL-1

disability_type | TP DEFIC: 0 nao defic, 1 fisica, 2 auditiva, 3 visual, 4 mental, 5 multipla, 6 reabilitado |
  yes | category, 7 levels ("mental" written as Intellectual, fine); `Ind Portador Defic` dropped as an exact
  copy of type != None (holds on every row) | fine as data; protected ground (deficiencia, reabilitacao
  profissional) -> issue A | CLEAN-5 ok; SEL-1

occupation_cbo | CBO Ocupacao 2002, 6 digits; 999999 ignorado | mostly: the year's declared value, as of the
  link's end date (a promotion after 1 Feb shows); kept with a note | category of zero-padded text, 2,523
  levels; 999999 -> missing; the 2020 sheet `ocupacao` names 2,577 codes, 203 levels in the data (6.4% of rows,
  e.g. 521140 with 18,563 rows, 111415, 414140, 010310) are not in it | keep; CLEAN-12 departure -> issue E;
  last-value note stays | LEAK-10 note (cannot test: no ids); CLEAN-12, CLEAN-14

contract_type | TP VINCULO: 10 ... 97, -1 ignorado | mostly (the type as of the link's end; a fixed-term contract
  converted to open-ended shows its later type) | category, 19 levels; labels match the layout; 999 -> missing (36
  rows) | fine, last-value note | LEAK-10 note

worker_category | eSocial Tabela 01 (not in the 2020 layout) | mostly, as contract_type | category, 21 levels; the
  intermittent flag dropped as a copy of 111 (holds on every row) | fine | CLEAN-5 ok

admission_type | TIPO ADM: 0 nao admitido ano, 1 primeiro emprego, 2 reemprego, 3/4 transferencia, 6 reintegracao,
  7-14 servants' types | yes (set at admission) | category; non-zero exactly for the January hires (100% of rows),
  so it holds "hired in January" plus the kind; code 5 (undocumented) -> missing (2 rows) | fine | -

weekly_hours | HORAS CONTR: contracted hours per week, format <99> | mostly (last declared value) | float; 0 and
  99 -> missing (947 + 44,329 rows in the 2M sample, 2.3%); 73% of intermittent contracts have 0/99, for which no
  fixed hours exist, so missing is the right state; the missing share does not differ by class (2.07% vs 2.05%);
  range 1-60 after | fine | CLEAN-10 ok

part_time | IND TRAB PARCIAL: "indicador de movimentacao referente a contrato parcial" | yes: it reads as a contract
  attribute, not a separation marker: set for 0.68% of stayers admitted before the year vs 1.04% of their leavers;
  mean hours 23.6 when set vs 41.2 | category No/Yes | fine | CLEAN-14

cnae_subclass | SB CLAS 20: CNAE 2.0 subclass, 7 digits; 9999999 ignorado | yes (the establishment's activity) |
  category text, 1,291 levels; 29 levels (1.2% of rows, e.g. 6201501, 4713004, 8020001) not in the 2020 sheet
  (newer CNAE 2.3 subclasses) | keep; CLEAN-12 departure -> issue E | CLEAN-12

cnae_class | CLAS CNAE 20: CNAE 2.0 class, 5 digits | yes | category text, 665 levels; equals the first 5 digits of
  the subclass in 99.995% of rows: a coarser level of the same hierarchy, not an exact copy | fine (keeping one
  level of the hierarchy is legitimate) | CLEAN-5 not triggered

ibge_subsector | IBGE Subsetor (25 sectors); {n class} ignorado | yes | category, 25 levels in words; 98 -> missing
  (76 rows); set by the CNAE class (median share of the main subsector per class 1.0) | fine | -

legal_nature | NAT JURIDICA (CONCLA 2002 list in the 2020 layout); 9999/-1 ignorado | yes | category text, 72
  levels; 9999 -> missing (2.5%, equal by class 2.65% / 2.64%); 19 codes not in the 2020 list cover 11.8% of the
  rows: 1244 (146,256 rows, the second-largest level), 1333 (14,839), 4120 (5,268), 1236, 1279, 1325, 1260, 3301,
  2321 and more | keep; CLEAN-12 departure, decodable from the current CONCLA table -> issue E | CLEAN-12

establishment_type | Tipo Estabelecimento (layout: 1 CNPJ, 3 CEI, 9 nao identif; the file's own Nome column for 5
  CAEPF and 6 CNO) | yes | category, 3 levels in the data; the CEI flag dropped as a copy of CNO (holds) | fine |
  CLEAN-5 ok

simples | IND SIMPLES: establishment opted into SIMPLES | yes (the year's value; an exclusion during the year shows;
  rare) | category No/Yes | fine | -

municipality | MUNICIPIO: IBGE 6-digit code of the establishment; <UF>9999 and 999999 ignorado | yes | category
  text, 5,571 levels; 109 rows at 999999 -> missing; all but one level (510183, 32 rows) are in the 2020 sheet,
  which names each one ("110001:Ro-Alta Floresta D Oeste") | keep; CLEAN-12 departure -> issue E | CLEAN-12,
  CLEAN-14

work_municipality | MUN TRAB: municipality where the employee works, when the employer gives one | yes | category text,
  99.6% missing; present mostly for workers on loan to another body (44.5%), casual workers (36%), legal nature
  3131 (union entities); quit rate 0.08% when present, a category effect; missing indicator alone 0.502 |
  fine, kept as published | -

pay_january | Vl Rem Janeiro SC: January pay, nominal R$ | yes (after the January payroll, the prediction point) |
  float; 0 for 11.8%, which marks links mostly unpaid all year (issue D); 1,041 negative values in the 1.5M
  (-587,678.75 to -0.01, quit rate 14.6%, 2x the base) (issue F); max 4.68M R$ | keep; issues D and F |
  LEAK-25 (question), CLEAN-11

tenure_months | rebuilt from Tempo Emprego (months to 31/12 or to the separation) | yes after the rebuild, except
  one artefact: for January hires the value 2 occurs only for leavers (1,367 of 1,975,519 rows, 100% separated,
  5% quits); a January hire has at most 1 month on 1 Feb | float, 0-595 | small LEAK, fix by clipping (issue C) |
  LEAK-10, LEAK-13, CLEAN-11

quit_by_year_end (target) | Motivo Desligamento 20 or 21, Feb-Dec | outcome | category No/Yes, 7.23% Yes | fine (the
  codes 20/21 match the layout's words; target scope is the builder's issue 4, not re-audited here) | CLEAN-25

Dropped columns: the drops listed in curation_comments are right. Each one I checked is post-outcome (separation
fields, active 31/12, Tempo Emprego, December pay, leave days, establishment size on 31/12, abandoned), an exact copy
(three flags), or constant (the five sub-municipal codes, Ano Chegada Brasil). Not read: Faixa Etaria (a band of the
same age, so the same leak), the hours and tenure bands, the pay of Feb-Nov, the average pay. None of them should come
back.

**PROBLEMS, RANKED (principles.md: P1 first, then by strength, then by effect)**

A. Protected grounds as inputs of an employer's retention decision (P1, SEL-1; the tension row "a factor the actor may
   no longer use", USE-1/USE-6). Question for the curator; the builder's issue 1.
   Evidence:
   - All five are known on 1 February. Timing is not the issue (age excepted, issue B). The issue is that the actor
     may not use them.
   - Brazilian law bars them for this decision:
     * Lei 9.029/1995 art. 1, as amended by Lei 13.146/2015 (in force 2016-01-03), bars "qualquer pratica
       discriminatoria e limitativa para efeito de acesso a relacao de trabalho, ou de sua manutencao" on the grounds
       of sex, origin, race, colour, marital status, family situation, disability, professional rehabilitation and
       age, among others.
     * The Constitution, art. 7 XXX, bars differences in pay and functions by sex, age, colour or marital status, and
       XXXI bars discrimination in pay against workers with disabilities.
     * Race and health data are sensitive personal data under the LGPD (art. 5 II).
   - The use case's own decision falls under these rules. "Whom to offer a raise, a talk, a training plan" is the
     maintenance of the employment relationship, and a raise is pay.
   - The tension row settles such a factor by "the actor's legal constraint today": the factor leaves the features
     (bemtpl97; the family stance on sex in insurance pricing). The row's exception, "a use case set in the data's
     own time keeps the factor", does not help here: the law was in force in 2025, the data's year.
   - Cost of dropping, measured (LightGBM, 600k train / 400k test from the 2M cohort sample, 3 seeds, ROC AUC):

       variant                                                 seed 0   seed 1   seed 2
       shipped                                                 0.79047  0.78996  0.78929
       drop sex, race                                          -0.0011  -0.0010  -0.0006
       drop sex, race, nationality, disability_type            -0.0001  -0.0008  -0.0001
       drop all five (+ age)                                   -0.0065  -0.0060  -0.0059

     So the four non-age grounds carry under 0.001. Age carries about 0.006, of which 0.0006 is the leak of issue B.
   Precedents to weigh (consistency):
   - hr_analytics keeps `gender` in a candidate job-change task.
   - wioa_employment_after_exit_1m keeps race, sex and disability with a flag to the curator (SEL-1).
   - home_credit_default_risk and credit_card_clients_default keep sex ("not reviewed yet").
   Whatever is decided here should be applied to hr_analytics (an employer decision on a person) the same way.
   Options:
     (a) Keep all five with the note. The data's analytic use. This departs from the tension row without a fact that
         sets the case apart.
     (b) Drop sex, race, nationality and disability_type (cost <= 0.001). Keep age, fixed by issue B.
     (c) Drop all five (cost about 0.006). This also settles issue B. Age is as explicitly barred as the others.
   Column auditor's reading: the rule as written gives (c). (b) is defensible only if age is treated differently for a
   stated reason (it is the strongest real signal, and an HR team plans hiring by age-related retirement). That reason
   would have to be recorded as an exception. Curator's call.

B. `age` is measured on the separation date for leavers (P4, LEAK-10 Must; LEAK-6: "a confirmed leak goes even when
   small"). This replaces the builder's "Potential leak, kept on purpose" note (claim 27): the mechanism is now shown.
   Evidence (decisive test, all 2025 apprentice links without disability, from the raw files):
   - The test: an apprenticeship must end when the apprentice turns 24. If age were measured on 31/12 for everyone,
     an apprentice who left in month m at age 23 would show 24 whenever the birthday fell after the separation. That
     is about (12 - m + 0.5)/12 of them: 96% for January leavers, 4% for December leavers.
   - What the file shows, for leavers other than end of contract, counts of age 24+ against age 23 by separation
     month:

       month       1      2      3      4      5      6      7      8      9      10     11     12
       24+ / 23    0.36   0.32   0.32   0.31   0.25   0.22   0.20   0.22   0.19   0.15   0.14   0.16
       31/12 hypothesis would give 24/1 in January ... 0.04/1 in December

     Leavers are therefore not aged on 31/12. Their age stops at the separation.
   - In the cohort only (admitted before February), separated February to May: 2,955 at 23 against 898 at 24+. The
     31/12 hypothesis needs several times more 24s than 23s.
   - Stayers are aged on 31/12 or later. Cohort apprentices in post on 31/12 number 7,742 at 22 and 3,661 at 23. If
     age were taken on 1 January, 23-year-old stayers would have had to leave before their birthday, and almost none
     would remain.
   - So a leaver in month m looks on average (12 - m + 0.5)/12 years younger than a stayer born the same day, and
     every separation (quits and the No separations alike) carries it.
   Strength (same LightGBM set-up; "harmonised" = the leaver's age moved to the 31/12 reference by a seeded draw with
   probability (12 - m + 0.5)/12, the expected share whose birthday falls after the separation):

       full model, shipped age - harmonised age:   +0.00065 / +0.00072 / +0.00057 (3 of 3 seeds)
       age alone, shipped - harmonised:            +0.0095 / +0.0095 / +0.0095
       harmonised age vs no age (honest worth):    +0.0053 / +0.0053 / +0.0047

   About 11% of age's apparent worth in the full model is the leak. Weak, but measured and confirmed.
   Remedy, mildest first:
     (1) Harmonise in `_clean`: age + 1 with probability (12 - m + 0.5)/12 for links separated in month m, fixed
         seed, before the separation month is dropped. This is the same kind of rebuild as tenure_months (the
         half-month guess) and keeps the honest signal. Note it as a reconstruction.
     (2) Drop `age` (option A(c)).
     Not a fix: 5-year bands. They only move the edge and keep the leak at every band edge.
   The script and its log are in work_column_auditor/age_leak.py, age_leak.log and age_leak.csv.
   Sibling sweep (LEAK-2): the same marker ("as of the link's end date") very likely holds for occupation_cbo,
   contract_type, worker_category, weekly_hours, education and simples. A link ending in month m shows its values in
   month m; a stayer shows them on 31/12. Without worker ids this cannot be tested, so the existing "Potential leak,
   kept on purpose" note stays. Its wording should change from "the year's declared values" to "the values as of the
   link's end (the separation or 31/12), as `age` shows". `Faixa Etaria` must never be read (the same leak).

C. `tenure_months` = 2 for January hires exists only for leavers (P4, LEAK-10 / LEAK-13: the rebuilt value's
   precision marks the class; CLEAN-11 impossible value). Fix in the definition.
   Evidence:
   - January hires in the 2M sample: stayers 20,336 at 0 and 37,270 at 1, none at 2. Leavers 35,408 at 0, 24,871 at
     1 and 1,367 at 2. The 2s are all separated; 68 of them quit (5%, against 15.3% for January hires).
   - A worker hired in January has at most one month on 1 February, so 2 is impossible. It comes from the half-month
     guess on the separation day (leavers' rebuilt value = true + U(-0.5, 0.5)).
   - Effect: tiny (0.07% of rows), but it is a pure separated-not-quit marker.
   Remedy: clip `tenure_months` to [0, 1] where `admission_month` == 1 (before the drop). Optionally, document the
   +-0.5-month noise that only leavers carry. Rounding hides it everywhere else: the fractional parts differ by class
   before rounding (stayers 29% at .0, leavers 16%), and the whole-month value does not show it.
   Also: 609 links admitted before the year have tenure_months 0, an impossible value (the builder's 594 negatives
   clipped to 0, plus a few). They are mostly stayers (7.4% separated, 1.0% quit). Could be missing rather than 0
   (CLEAN-11); minor.

D. Zero January pay marks links that are mostly never paid (P4/P3, LEAK-25 question; the feature itself is known on
   1 February, so it is no LEAK-10). Question for the curator.
   Evidence (10% cohort sample from the raw files with all 12 monthly pays, abandoned links excluded):
   - 82% of the links with 0 January pay have no pay in any month they were in post.
   - Links never paid while in post: 9.7% of the cohort, quit rate 1.0% against 7.9% for the others.
   - Never paid and no leave day in the year: 8.4% of the cohort, quit rate 0.98%, any separation 6.0% (27.5%
     overall).
   - Part of it is how categories report pay: never paid for 84% of the armed forces, 78% of casual workers, 60% of
     intermittent contracts, 41% of fixed-term public servants.
   - Within CLT employees (category 101): 6.0% never paid, of whom 25% have leave days (17% with 300 or more, long
     benefit leave). 4.5% are never paid with no leave at all; their quit rate is 1.1%.
   - These look like the abandoned links the source flags (no pay in January or December, no separation recorded),
     but unflagged: a link nobody works in whose end may never be declared, so a No that may mean "not recorded"
     (LEAK-25).
   - The builder's note ("on leave, or no pay reported") covers the first group but not this one.
   Options:
     (a) Keep with a note giving these numbers (a known gap, fit already approximate).
     (b) Define the cohort as links paid in January (pay_january > 0). This is known at the prediction point and fits
         "after the January payroll, scores its staff". It removes 70% of the suspected dormant links, and also
         removes staff on long leave, who do belong to the use case.
   Not settleable without the ministry's rules for these links. Lean (a), with the numbers.

E. Classification codes shipped as codes (P7, CLEAN-12 Should; the builder's issue 5). Question for the curator.
   Evidence:
   - CLEAN-12 as amended (2026-11-01) says a code whose codebook names it in words is decoded. The 2020 layout names
     every municipality (one exception: 510183, 32 rows) and every CBO and CNAE subclass of 2020.
   - The builder's reason (the digits carry the hierarchy) does not help a model that sees a category: an unordered
     level loses the digits either way.
   - Coverage of the 2020 sheets: CBO misses 6.4% of the rows, CNAE subclass 1.2%, legal nature 11.8% (1244 alone is
     146k rows, the second-largest level). The current official tables cover the newer codes (the CBO list of MTE,
     CNAE 2.3 and natureza juridica 2021 at IBGE CONCLA). A 2020-only decode would leave holes, and "a code without a
     label raises".
   Options:
     (a) Keep the codes with the departure recorded as an exception: the 2020 codebook is out of date for 2025 and
         the current tables are not part of the release.
     (b) Decode from the current official tables (CBO, CNAE 2.3 subclass and class, CONCLA 2021 legal nature, IBGE
         municipalities) into "words [code]", as ny_wcb_assembled_claims_1m does for NAICS ("the codebook's
         description with the code in brackets"). This keeps both the words and the digits.
     (c) Decode only what the layout fully covers (municipality, to "UF-Name [code]"), and keep the rest as codes.
   The CLEAN-12 rule and the ny_wcb precedent favour (b). The cost is lookup files in the folder. A cheap partial step
   whatever the choice: the state (UF) is the municipality's first two digits. The municipality code already holds it,
   but as a category the model cannot read it.

F. Negative January pay (P7, CLEAN-11 Should).
   - 1,041 of the 1.5M rows (1,400 of the 2M; -587,678.75 to -0.01, median -125.82) have negative pay. Remuneration
     cannot be negative; these are probably reversals of an earlier payment.
   - Their quit rate is 14.6%, twice the base. Read that as a signal of something irregular in the link, not a pay
     level.
   - Remedy: set to missing (CLEAN-11) with a note, or keep with a note saying what they are. Weight: tiny.

No finding:
- Every small code set's decode matches the 2020 layout: sex, race, education order, nationality, disability type,
  contract type, admission type, establishment type, IBGE subsector, the SIMPLES and part-time flags.
- No proxy missing value is left in the numeric columns: age < 14, hours 0/99, CBO/CNAE/legal-nature/municipality
  "ignorado" are all handled.
- None of the proxy-missing patterns differs by class: race 9 is 4.08% vs 4.14%, legal nature 9999 2.65% vs 2.64%,
  hours 0/99 2.07% vs 2.05%.
- cnae_class and ibge_subsector are coarser levels of the subclass, not copies.
- work_municipality's presence is a category effect.

**FILES (all in the run's panel folder)**
layout/layout2020.xls, layout/layout_lines.txt   RAIS link layout 2020, downloaded from the FTP, and its main sheet
dtype/                                           re-run of the dtype probe
load.py, clean.parquet                           cleaned frame through dataset_io (1.5M)
clean_full.py, clean_full_with_raw.parquet       `_clean` on the 2M sample with the raw columns aligned
apprentices_full.py, apprentices_2025.parquet    all 2025 apprentice links (age reference-date test)
pay_months.py, cohort_pay_10pct.parquet          10% cohort with the 12 monthly pays (issue D)
age_leak.py, age_leak.log, age_leak.csv          issue B measurement
protected.py, protected.log                      issue A cost of dropping the grounds

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR REPORT: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-08

VERDICT: right with notes. Forced IID on the 2025 cohort (ForcedIIDFromTemporal, SPLIT-8) is the closest regime the
release allows. I reproduced the cost on the shipped folds: a model trained on 2024 scores 0.0057 ROC AUC lower. About
three quarters of that gap (0.004-0.005) comes from the same year's outcomes being shared within establishment-proxy
cells across the random folds. This favours models that memorise the high-cardinality codes but changes the order of
none of the five learners I tested. The grouped alternative on the proxy is barred (SPLIT-24) and underrates the task by
about as much as IID overrates it. The fixes are notes only.

Judgment record (split only):
  Validity: SPLIT-1 / USE-10 hold (the use case is temporal: train on last year's cohort, score this year's);
    SPLIT-14 not met (one valid window), SPLIT-8 applied correctly (forced IID, cost measured on the valid window);
    SPLIT-8 leak test across the split: triggered, small (same-year shared outcomes within establishment-proxy cells,
    +0.004 to +0.005 ROC AUC, no ranking change), keep with the number in the notes;
    SPLIT-29/30 no re-split (no establishment id; SPLIT-24 bars grouping on the feature-built proxy);
    SPLIT-4 holds (CNAE x municipality cells are features new rows keep).
  Notes: the cost figures in curation_comments come from the builder's own folds, not the shipped folds; the "ship yearly
    windows if more years are downloaded" sentence ignores the 2022/2023 series breaks.

All scripts, logs and JSON are in the run's panel folder
(prep.py, keys.py + keys.log, models.py + models.log/json, decomp.py + decomp.log/json, ranking.py + ranking.log/json).
Data: the shipped frame and folds rebuilt from the definition (dataset_io.from_definition; the prepared files' code hash
matches, nothing re-prepared or written to the warehouse). Shipped rows were traced back to the raw sample by hashing the
features and the target (1.5M of 1.5M matched, target 100%); the 0.8% exact duplicates are matched in arbitrary order.
The 2024 cohort sample is the builder's (test_raw_2024/, built by this definition's code) and was cleaned with the same
`_clean`. Model: untuned LightGBM (300 trees, 63 leaves, lr 0.1, as the builder used), n_jobs 4, thread caps set.

**1. THE REGIME (SPLIT-1, SPLIT-3, USE-10, SPLIT-8, SPLIT-14)**
* Use case: on 1 February an HR team scores its staff for quitting by 31 December. A deployed model trains on last
  year's cohort, whose labels closed on 31 December, and scores this year's cohort. That is temporal by use case
  (a stream of yearly cohorts). The entity is the link (worker x establishment). Employers and most workers recur
  across years, but RAIS publishes no worker or employer id, so their history cannot be used and no entity can be
  grouped on. SPLIT-8's forced grouped regime needs a recorded entity that recurs (nba, open_university); none exists
  here.
* Windows: one cohort per year. A cohort-year is the only time unit: the label horizon is the rest of the calendar
  year, and links cannot be followed into the next year's file. With equal-sized yearly cohorts and expanding training
  sides, three windows with every training side >= 50% need N >= 6 years ((N-3)/N >= 0.5). The builder's "about six
  yearly files" is correct.
* The 40% extension of SPLIT-14 (amended 2026-11-08) needs most test entities to recur and be known to the actor.
  Without ids no recurrence can be shown, so it does not apply. With five years the oldest window trains on 40% and
  fails the floor.
* Series breaks (SPLIT-20): according to the MTE as quoted by Fenacon, base years 2022 and 2023 each carry "uma
  importante quebra na série histórica" (the Group 3 migration to eSocial widened coverage), and direct comparison with
  earlier years is advised against. 2023-2025 share one header (builder's assert). The clean stretch is therefore
  2023-2025, which gives exactly one valid window (train 2023+2024, test 2025). Using 2020-2025 for three windows would
  train across two breaks and the COVID years. I did not re-read the MTE's own note; the Fenacon quote and the RAIS 2022
  presentation are the evidence (sources at the end).
* Precedent: distribution_transformers_at_cauca_department (two label years, one window): one year IID,
  ForcedIIDFromTemporal, not stacked. The facts are the same, so the case is decided the same way. Stacking 2024+2025
  would put the continuing jobs of both years into one random split. A link in post all year in 2024 (label No) is the
  same job as a 2025 row, and a random split across the two years would mix both period effects. I did not measure
  this; it is not a candidate.
* Conclusion: forced IID on the newest cohort is the regime SPLIT-8 prescribes. Holds.

**2. COST OF THE FORCED SPLIT ON THE SHIPPED FOLDS (SPLIT-8)**
Shipped folds: 1 repeat x 3 folds, 1,000,000 train / 500,000 test, no overlap. The "train 2024" model is fit on a
random 1,000,000 of the cleaned 2024 sample (equal size) and scored on the same shipped test folds.

  fold   IID within 2025 (AUC / log loss)   trained on 2024 (AUC / log loss)   gap AUC
  0      0.7975 / 0.2200                    0.7919 / 0.2224                    +0.0056
  1      0.7959 / 0.2208                    0.7899 / 0.2232                    +0.0060
  2      0.7980 / 0.2197                    0.7926 / 0.2222                    +0.0054
  mean   0.7971                             0.7915                             +0.0057 (3 of 3 folds)

The builder's numbers (0.7976 vs 0.7918) are from its own StratifiedKFold on a separate 1.5M draw of the 2M sample
(forced_split_cost.py), not from the shipped folds. curation_comments says "on the three test folds of 2025", which a
reader takes to mean the shipped folds. The two agree within 0.0005.

Nominal pay drift is not the cause: with 2024 January pay rescaled by the minimum wage (R$1,412 to R$1,518), the 2024
model scores 0.7921 / 0.7901 / 0.7926 (mean 0.7916, against 0.7915 unscaled).

**3. ESTABLISHMENT-LEVEL CLUSTERING (SPLIT-8 leak test, SPLIT-29, SPLIT-30)**
No establishment id ships, so I used three proxy cells, built from the shipped features plus the raw size class:
  K1 = CNAE subclass x municipality
  K2 = K1 x legal nature x register type x SIMPLES
  K3 = K2 x establishment size class on 31/12. The size class is recorded after the outcome. I used it only as a
       grouping key, never as a feature.

Cell statistics in the shipped 1.5M (keys.log):
                                      K1        K2        K3
  cells                               212,232   287,172   400,267
  median cell size of a row           38        23        11
  rows in a cell of 1                 6.7%      10.2%     15.7%
  test rows whose cell is in train    91.1%     87.0%     80.4%   (every fold)
  test rows whose cell is in 2024     94.2%     90.6%     77.6%
  ANOVA ICC of the quit flag          0.072     0.089     0.125
  cell quit rate, cells >= 20 rows in both years:
    corr 2024 half vs 2025 half       0.451     0.483     0.508
    corr 2025 half vs 2025 half       0.469     0.491     0.519
The quit rate of a cell is largely persistent from year to year. The cross-year correlation reaches 96-98% of the
within-year split-half correlation, so the part of a cell's rate that belongs to one year alone is small but not zero.
K3 cells hold about one establishment for 28% of the rows, 1.5-5 for 28%, 5-50 for 35% and 50 or more for 9%. These
are estimated from the sampling fraction (1.5M / 58.6M) and the midpoint of the size class.

Decomposition on identical test rows (decomp.py). For each of 3 folds grouped by cell, the test is half of the fold's
rows, restricted to cells that also have a row in the other half (190k-217k rows, 13k-15k positives). There are four
training sets of 900k each:
  A = 2025, the test cells shared (the other half of the fold plus other cells)
  B = 2025, the test cells unseen
  C = 2024, random (cells shared from last year)
  D = 2024 without the test cells

                    A (25 shared)  B (25 unseen)  C (24 shared)  D (24 unseen)  same-year cell value  last-year cell value
  K2 fold 0         0.8065         0.7965         0.7985         0.7939         +0.0100               +0.0046
  K2 fold 1         0.8015         0.7932         0.7995         0.7910         +0.0083               +0.0085
  K2 fold 2         0.8036         0.7921         0.7981         0.7929         +0.0115               +0.0052
  K3 fold 0         0.8129         0.8022         0.8048         0.8013         +0.0107               +0.0035
  K3 fold 1         0.8096         0.7986         0.8005         0.7947         +0.0110               +0.0058
  K3 fold 2         0.8104         0.8008         0.8039         0.7968         +0.0096               +0.0071
  Year-specific cell value, (A-B)-(C-D): K2 mean +0.0038 (+0.0054, -0.0002, +0.0063); K3 mean +0.0050
  (+0.0072, +0.0052, +0.0025).
  Drift with no cell shared, B-D: K2 mean +0.0013, K3 mean +0.0029.
  The full 3-fold grouped runs (models.py, ~1M train) agree: grouped 2025 minus 2024-without-test-cells is +0.0016,
  +0.0026, -0.0005 (K2) and +0.0009, +0.0018, +0.0020 (K3).

Reading: of the +0.0057 AUC that the random folds gain over training on last year, about +0.004 to +0.005 is the same
year's outcomes shared within a cell (an establishment, or a local sector shock in one municipality) between train and
test. The remaining +0.001 to +0.003 is plain year-to-year drift. This is the SPLIT-8 "unit's or period's outcome
shared with the other side" leak. It is real but small: 0.5% of the score. The gap does not concentrate in cells of a
single establishment. By K3 bucket (est. establishments per cell) the gap is ~1: +0.0064/+0.0076/+0.0039;
1.5-5: +0.0075/+0.0075/+0.0061; 5-50: +0.0031/+0.0045/+0.0063; 50+: +0.0068/+0.0029/+0.0052. So it is a cell-level
(local sector and workplace) effect more than a single-employer one.

Does it change the ranking? (ranking.py; 5 learners on the shipped folds against the same learner trained on 2024)
  learner                              IID 2025   trained 2024   gap
  LightGBM, 15 leaves                  0.8023     0.7974         +0.0048
  LightGBM, 63 leaves (probe default)  0.7971     0.7915         +0.0057
  LightGBM, high-card codes dropped    0.7926     0.7894         +0.0032   (no CBO, CNAE, legal nature, municipalities)
  logistic, one-hot (min freq 200)     0.7866     0.7837         +0.0029
  LightGBM, 255 leaves x 1000, small   0.7710     0.7606         +0.0103   (memorises rare category levels)
    category groups
The order is the same under both protocols on every fold. The random split does inflate the reward for using and
memorising the high-cardinality codes. Default minus codes-dropped is +0.0045 under IID against +0.0021 trained on
2024, and the memorising learner's gap is twice the default's. The benchmark therefore slightly favours models that
exploit category levels by heart. This is worth stating in the notes, not fixing.

Grouped alternative: grouping on the proxy gives 0.7874 (K2) / 0.7884 (K3), against 0.7914 for the 2024-trained model
on the same grouped test rows. It underrates the realistic score by ~0.003-0.004, about as much as IID overrates it.
It is barred anyway: the proxy is a combination of features, not a recorded entity (SPLIT-24), it holds out feature
combinations a deployed model has seen in last year's data (SPLIT-4), and K3 cells hold several establishments for
~72% of the rows.

Other hidden groups:
* Workers with two jobs: two links of one person both enter the 2.56% sample rarely, so this is negligible.
* Exact copies: 0.9% of test rows (builder, same label).
* Hidden-group probe: no hits; the CBO and CNAE cells are features (SPLIT-4).
I agree with the builder's reading.

**4. TEMPORAL DETAILS UNDER THE FORCED SPLIT**
* No time column ships, which is right for one cohort. The label horizon (February to December) is complete at
  release: the files are final for the base year, and quits are spread over every month (builder: 25,499 in February
  to 6,530 in December).
* Training rows whose label is unknown at the prediction point: under IID every training label (Feb-Dec 2025) falls
  after the test rows' prediction point (1 Feb 2025). This is the period-sharing measured in section 3, about +0.004.
  It is inherent to forcing and is noted, not removed.
* The gap against label delay for a future temporal variant: each base year's files are posted in May of the following
  year (2025 on 2026-05-13). An actor who trains on RAIS itself would, on 1 February of year t, have cohort t-2 as its
  newest training data, which is a one-year planning gap (SPLIT-10). The HR-team actor of the use case trains on its
  own records, closed on 31 December, so it needs no gap. Whichever actor a temporal variant names decides whether it
  needs the gap, and with the gap it needs one more year.
* No season-shaped test window: the test cohort is a whole year.

**5. PROBLEMS, RANKED (principles.md: P4 validity first; all are Should-level notes, none a Must failure)**
1. [P4, SPLIT-8 leak test across a forced split; SPLIT-29/30] The same year's outcomes are shared within
   establishment-proxy cells across the random folds. Evidence: section 3, year-specific cell value +0.0038 (K2) and
   +0.0050 (K3), against a total IID-vs-2024 gap of +0.0057 (3 of 3 folds). It doubles the IID reward for the
   high-cardinality codes (+0.0045 vs +0.0021) but changes no ranking among 5 learners. It cannot be removed: there is
   no establishment id, and SPLIT-24 bars the proxy.
   Mildest remedy: keep, and state the number. In the curation_comments "One year, IID" bullet, replace "anything the
   year's own outcomes share across rows (a wave of resignations at one workplace), which random folds reward" with
   the measurement. Suggested wording: "about 0.004-0.005 of it is the year's own quits shared within a sector x
   municipality x legal-form cell between training and test (a workplace or a local shock): measured by holding the
   test rows' cells out of each year's training; the order of five learners is the same under both protocols, while
   models that memorise the codes gain more from the random split (+0.010 against +0.005)."
   The fit_reason can say the random split is optimistic by about 0.006 ROC AUC.

2. [P4, SPLIT-8 cost statement; EV-2 / writing] The cost numbers are attributed to the shipped folds but come from the
   builder's own folds. Evidence: forced_split_cost.py uses StratifiedKFold(seed 4267) on its own 1.5M draw; on the
   shipped folds the gap is 0.7971 vs 0.7915 (+0.0057; log loss 0.2202 vs 0.2226).
   Mildest remedy: use the shipped-fold numbers in curation_comments (decision text unchanged), or say "on folds of
   our own".

3. [P4, SPLIT-14 / SPLIT-20; the record of the alternative] "Ship yearly windows if more years are downloaded" is not
   a clean path. Older years cross the 2022 and 2023 series breaks (MTE via Fenacon) and the COVID years. The
   post-eSocial stretch 2023-2025 gives one valid window, and the floor needs six post-break years (2023-2028, the
   2028 base year being released around mid-2029). Five years (40% oldest training side) do not qualify for the 40%
   extension without recurring entities.
   Mildest remedy: reword to "revisit when the post-2023 stretch holds six base years, or if identified (linked)
   RAIS microdata become available".

4. [P3/P4, consistency, no action needed] The record's screening field `required_split: Temporal (NON-IID)` against
   the shipped IID split. The ForcedIIDFromTemporal tag records that the source regime is temporal, so the two are
   consistent. task_summary.split ("with one year of data the split is not by time") is accurate. The curator may want
   it to add "a model trained on the year before scores about 0.006 lower" so the reader of the summary sees the
   optimism.

No re-split, gap or filter is needed.

Caveats: the proxy cells are not establishments (multi-establishment cells dilute and single-establishment cells are
estimated), so the year-specific cell value is a lower bound on true workplace sharing. Even so, the whole IID-vs-2024
gap (+0.0057) bounds what any same-year sharing can add on top of drift for this learner. All numbers are untuned
LightGBM or logistic models (TP-1: not leaderboard numbers).

Sources (web): Fenacon, "RAIS 2023 revela estoque de 54,7 milhões de vínculos ativos no Brasil"
(https://fenacon.org.br/noticias/rais-2023-revela-estoque-de-547-milhoes-de-vinculos-ativos-no-brasil/); MTE, RAIS 2022
technical-note presentation
(https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais/rais-2022/apresentacao_rais-2022_nota_tecnica.pdf).

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-08

Actor played: the HR analytics / workforce-planning team of a Brazilian private employer (a retailer with a few
thousand CLT staff over many stores), on 1 February, after the January payroll, scoring each employee for the risk
of resigning before 31 December, to decide whom to offer a retention measure (a talk, a raise, training) and how many
replacements to budget. Second reading: a payroll or HR-software vendor that serves many small employers and needs a
pooled cold-start model (the only actor who would ever train on all employers pooled, as this dataset does).

VERDICT
  Fit: APPROXIMATE (agree with the definition). One sentence: the inputs are ones I hold on 1 February and the
  employee-initiated quit is what I act on, but the rows pool all employers including public servants and the armed
  forces I never score, they lack the workplace and pay history I always have, and the random split within one year
  stands in for "train on last year, score my staff this year".
  Metric scores the decision: PARTLY. ROC AUC ranks, which my retention list needs, but it ranks nationally across
  employers and sectors (pooled 0.792 against about 0.727 within sector x municipality cells and 0.747 within private
  CLT employees), and it is blind to calibration, which my hiring budget needs. I would choose log_loss (MET-8; MET-10
  diversity), not average_precision (MET-9) and not precision_at_k (MET-7: no k is fixed by any source).
  Legal: under Lei 9.029/1995 art. 1 I may NOT use sex, origin (nationality), race/colour, disability or age in a
  score that decides who is offered retention ("manutenção" of the relation). Measured: the four other than age carry
  nothing (ROC AUC 0.7917 -> 0.7916); all five cost 0.007 (0.7917 -> 0.7845). Recommend dropping all five (tension
  row of principles.md, "the actor's legal constraint today").

1. AT THE PREDICTION POINT, DO I HAVE EACH INPUT?

Have on 1 February (every shipped feature):
  - age, sex, race/colour, education, nationality, disability type: yes. My eSocial events (S-2200) hold the birth
    date, sex, raça/cor, education, nationality and deficiency; RAIS is now built from eSocial. But see 4 below: I may
    not use five of them for this decision.
  - occupation (CBO), contract type, eSocial worker category, weekly hours, part-time flag, admission type: yes, from
    the contract. Caveat already in the notes: RAIS keeps the year's declared value, so a mid-year change shows its
    later value (LEAK-10 cannot verify; kept on purpose, USE-8 does not make it a gap).
  - tenure on 1 February: yes, and to the day (admission date). The dataset rebuilds it to whole months from the
    year-end tenure with a half-month guess for leavers; that is coarser than mine but honest.
  - January pay: yes. Note it is a noisy stand-in for what I really use, the contracted wage: 11.8% of the cohort has
    0 in January (leave, no January pay). The 2023+ public files carry no contracted wage column (builder report).
  - sector (CNAE), legal nature, SIMPLES, register type, municipality: yes, but as a single employer these are nearly
    constant across my staff; they only vary across my establishments. They are inputs for the vendor actor.
  Nothing shipped is unavailable to me on 1 February after the builder's drops (separation fields, year-end tenure,
  December pay, leave days, 31/12 establishment size). The undocumented reference date of `Idade` is the one
  remaining doubt (a leaver could look up to a year younger); named in the notes.

Missing that I would always have (ranked by how much they matter for a quit model in practice):
  a. My workplace identity and its history: which store/team/manager, and that unit's quit rate last year. This is
     the strongest quit predictor HR teams use. The public files have no establishment or worker id, so it cannot be
     added; the fit_reason already names "no history of the worker or the workplace".
  b. Pay history and last raise, and the contracted wage (not shipped; January pay is a proxy).
  c. The establishment's headcount on 1 February (I know my own); the file only has the 31/12 size, rightly dropped
     (decision 3: class Zero = 100% separated).
  d. Last year's absences and leave, prior jobs, performance and engagement data: not in RAIS public files.
  None of these is a fixable defect; together they make the task "a base-rate model from contract and demographic
  facts", which is exactly what the vendor actor needs for a new small client and what a large employer would use
  only as a prior or benchmark next to its own HRIS model.

2. IS THE TARGET WHAT I ACT ON?

  - Yes for retention: codes 21 (pedido de demissão / exoneração a pedido) and 20 (rescisão indireta) are
    employee-initiated. Rescisão indireta is a labour-court claim for my fault, not something a raise prevents, but it
    is 1,181 of 142,852 positives in the sample (0.8%): harmless.
  - Code 90 (acordo, CLT art. 484-A, 6,488 links in the sample, about 4.5% of the Yes count) is counted No. In my
    practice an agreement is usually asked for by an employee who wants to leave and keep 80% of the FGTS; it is the
    departure my retention offer targets. I would count it as Yes, or at least name it in the notes as a target call
    the curator made (USE-5). Builder issue 4 raises it; I side with Yes.
  - Unfixable label noise worth naming: "fake layoff agreements" (acordos simulados). Brazilian workers who want to
    leave often ask to be dismissed without cause so they can draw their FGTS and unemployment insurance, and the
    employer records code 11; the PUC-Rio dissertation of Dias de Aquino Nascimento (2026, Narita and Gonzaga) treats
    them as an important margin, citing Camargo (1996), Gonzaga (2003), Carvalho, Corbi and Narita (2018). Some true
    quits therefore sit in No as dismissals. This is a known gap in the label's breadth, which USE-8 already counts
    as approximate; it does not change the fit, but the notes should say it (it caps any model's score).
  - For the hiring-plan half of the use case, I would want every departure not under my control (quits, agreements,
    deaths, retirements); dismissals I decide myself and ends of contract I know from the contract date. The quit
    target fits the retention half better than the planning half; the use case can keep both.
  - Output I want: a calibrated probability per employee. I rank it to fill the few retention talks I can hold, and
    I sum it per store and role to budget replacements.
  - Horizon February to December (11 months) is within the 3 to 12 months HR teams use; fine.

3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST DATA WHAT I FACE?

  - One row = one employment link = one employee in one job: the unit I decide on. Workers with two links (teachers,
    health staff in public posts) are rare and harmless.
  - The test data is not what I face, in three ways:
    a. POPULATION (largest; changes what the benchmark rewards). The cohort pools every formal link in Brazil,
       including statutory civil servants, the armed forces and state military, commissioned posts and public
       fixed-term servants: 100,159 of the 500,000 test rows of fold 0 (20.0%), quit rate 1.2% against 8.6% for
       private CLT employees. No private HR team scores them, and a public body does not run individual retention
       offers for tenured servants (pay follows the career law). Measured on fold 0 (untuned LightGBM, 1M train):
         pooled ROC AUC 0.792
         private "Employee, general" only 0.747 (385,665 rows); CLT contracts only 0.747
         public or military only 0.923 (the few leavers are separable: non-tenured, commissioned)
         within sector-subclass x municipality cells (a stand-in for "my establishment", 2,445 cells, 171,883 rows,
           weighted by positives) 0.727
       So about 0.045 of the pooled AUC comes from telling civil servants from retail clerks, and about 0.065 from
       ranking across employers (the second includes the first), rankings no employer ever makes. The bundle warning dataset_pure_feature_value
       (statutory servants, legal natures 1023 and 1015 at 99.6-100% No) is the same population fact.
    b. TIME. I train on last year and score this year's staff; the folds are random within 2025. Measured by the
       builder: 0.7918 trained on 2024 against 0.7976 within 2025 (-0.006, 3 of 3 folds). Small, named, tagged
       ForcedIIDFromTemporal; I accept it.
    c. WORKPLACE. Random folds put co-workers of the same establishment and year on both sides, so a resignation wave
       at one workplace in 2025 is partly learned from the training rows (via sector x municipality x occupation
       cells), which I would only know a year late. Part of the 0.006 above; cannot be measured further without ids.

4. WOULD I USE THIS MODEL? MAY I?

  Law: Lei 9.029/1995, art. 1 (wording of Lei 13.146/2015), read on the Câmara's updated text: "É proibida a adoção
  de qualquer prática discriminatória e limitativa para efeito de acesso à relação de trabalho, ou de sua
  manutenção, por motivo de sexo, origem, raça, cor, estado civil, situação familiar, deficiência, reabilitação
  profissional, idade, entre outros". Art. 4 gives the employee reinstatement or double pay plus moral damages when a
  relation ends by a discriminatory act. Choosing whom to offer a raise or a retention plan is a practice "for the
  maintenance" of the relation, so a score that uses these grounds exposes me directly. Also relevant (from my
  knowledge, not re-read for this report): Constituição art. 7 XXX and XXXI forbid pay differences by sex, age,
  colour and civil status and any discrimination of a disabled worker, so retention raises steered by such a score
  would show up in my equal-pay report under Lei 14.611/2023; LGPD art. 5 II and 11 make race and health
  (disability) sensitive data, collected by me for eSocial under a legal obligation, not for a retention model, and
  art. 20 gives the employee a right to review of an automated decision. A disability flag does have one lawful
  planning use: the quota of Lei 8.213/1991 art. 93 (2-5% for 100+ employees; a quota worker's dismissal tied to a
  substitute, TST Tema 312 pending), but that is headcount compliance, not an individual retention score.
  So, as the actor: I would not use sex, race, nationality, disability or age in this score. A legal team would ask
  me to drop all five. Measured on fold 0 (same model):
    all features                     ROC AUC 0.7917, log loss 0.2238
    without sex, race, nationality, disability_type        0.7916, 0.2238 (no change)
    without those four and age       ROC AUC 0.7845, log loss 0.2263 (-0.007 AUC)
  The four carry no signal at all; age carries a little (alone 0.674 per the builder's probe, largely shared with
  tenure). Compared with the insurance family, where sex left the features "as if we were to simulate the case in
  europe always" even where it was legal, here the ban is the actor's own law: a stronger case for dropping
  (principles.md tension row "a factor the actor may no longer use", USE-1, USE-6). Builder issue 1 options: I back
  (c), drop all five; (b) sex and race only is not what the law says (it lists origin, disability and age too).
  Only a different actor (a public agency forecasting replacement demand per region and occupation, not acting on
  individuals) could keep them, and that is a rephrase to excuse a gap (weighed factor against USE-9), with a target
  and unit the metric would not score.

  Would I use it? As the vendor with new small clients: yes, as a cold-start base rate by occupation, sector, contract,
  tenure and pay, with the protected grounds removed. As a large employer: only as a prior or benchmark beside my own
  model with workplace and pay history. What would make me trust it: stability across years (0.792 trained on the
  previous year, a good sign), calibration per sector and per store (my quick untuned model predicted 4.7% too few
  quits overall and 15-20% too few in four industrial subsectors while ranking at 0.792; a hiring plan built on it
  would under-budget), and drivers that make sense (tenure first, pay, occupation). What would make me distrust it:
  a headline AUC inflated by civil servants, sex or race among the drivers, and quits hidden as code 11 dismissals.

  Top of the list (fold 0, pooled, illustrative): top 5% precision 0.290 (lift 4.0, recall 0.20), top 10% precision
  0.245 (lift 3.4, recall 0.34). These match what HR vendors call a useful attrition model (production AUC about
  0.65-0.80, top-decile lift 2-4).

5. DOES ROC AUC SCORE MY DECISION? PARTLY.

  - What it gets right: no source fixes a threshold, a cost or a k (RAIS is a census; MET-6, MET-7 rule out a
    threshold metric or precision_at_k), and a threshold-free probability metric is the right family (MET-8). 7.2%
    positives is no reason for average_precision (MET-9), and my action is not only the top few.
  - What it misses (MET-1: "at the unit the actor acts on"): I rank within my own staff, not across Brazil. The unit
    (an employer's staff list) has no id in the data, so a per-employer AUC cannot be computed (MET-2: the unit must
    exist). Pooled AUC rewards between-employer and public-versus-private separation (0.792 pooled vs 0.727 within
    cells). Restricting the cohort to private employees (below) closes most of that gap (0.747).
  - It ignores calibration, which my replacement budget needs (sum of probabilities per unit). Log loss is strictly
    proper (Gneiting and Raftery 2007, cited in MET-8), scores both the ranking and the calibration, and adds metric
    diversity to a collection where roc_auc is the binary default (MET-10).
  - The metric I would choose: log_loss, origin fallback/context (MET-11), reason: the use case's planning half sums
    the probabilities. Keeping roc_auc is defensible (MET-8's binary fallback); then the notes should say it ranks
    pooled links, not an employer's staff.

GAPS BETWEEN THE DATASET AND THE REAL DECISION, RANKED BY HOW MUCH THEY CHANGE THE TASK
  1. Population: 20% public servants and military that no retention model scores; inflate ROC AUC by about 0.045
     (0.792 pooled vs 0.747 private CLT) and cause the pure-feature-value warning. Fixable (filter on worker category).
  2. No workplace or worker history (no ids), no contracted wage or pay history: the model is a base-rate model.
     Not fixable with public files; named in fit_reason.
  3. Protected grounds of Lei 9.029/1995 among the features: illegal for the actor to use; -0.007 AUC to drop all
     five, 0 for four. Fixable.
  4. Label breadth: code 90 agreements counted No (about 4.5% of positives); fake layoffs (quits recorded as
     dismissals) unmeasurable. The first is fixable, the second only nameable.
  5. Ranking unit and calibration: pooled AUC vs within-employer ranking and the budget's sum (metric, above).
  6. Random split within 2025 instead of next-year scoring (-0.006 measured); co-worker outcomes on both sides.
     Named, tagged; acceptable.
  7. Age reference date and year's last declared occupation/hours: kept potential leaks, named; small.

WHAT AN EXPERT IN THE DOMAIN WOULD CHANGE
  a. Restrict the cohort to the population an HR retention model manages: private-sector employees (eSocial
     categories 101-111, i.e. CLT employees incl. apprentices, temporaries, intermittent), dropping statutory and
     non-tenured public servants, commissioned posts, military (301-314), casual workers and directors. Rows remain
     plentiful (category "Employee, general" alone is 77% of the test rows). If the curator prefers to keep everyone, name the population in fit_reason as
     a selection the setting does not share (USE-8) and report the CLT-only AUC in the notes.
  b. Drop sex, race, nationality, disability_type and age (builder issue 1, option c), with Lei 9.029/1995 art. 1 in
     the notes and in `known`; this follows the tension row's "actor's legal constraint today".
  c. Count code 90 (acordo, art. 484-A) as Yes, or name it explicitly as a curator call; add a note on fake layoff
     agreements as known label noise (USE-5, USE-8).
  d. Declare log_loss (or keep roc_auc and say it ranks pooled links); either way no threshold or top-k metric.
  e. Keep: the 1 February prediction point, the rebuilt tenure, the drops of year-end fields, the abandoned-link
     drop, forced IID with the measured cost. These are what I would have done.

RULES CITED
  USE-1, USE-3, USE-5, USE-6, USE-8, USE-9 (and its weighed factor), USE-10; principles.md tension row "a factor
  the actor may no longer use"; LEAK-10; MET-1, MET-2, MET-6, MET-7, MET-8, MET-9, MET-10, MET-11.

MEASUREMENTS (mine)
  Script: practitioner_probe.py in the run's panel folder; output practitioner_probe.json and .log in the same
  folder. Fold 0 of the shipped splits (1M train, 500k test), untuned LightGBM (400 trees, lr 0.08, 127 leaves),
  native categoricals; one fold, one seed: differences of 0.001 are noise, of 0.007 are not.

SOURCES
  - dataset.py and README.md of df-large/datasets/_dev/tabarena-v0pt2/rais_employment_separation_1m/; the record
    curation/records/rais_employment_separation.md; builder_report.md and probes/ of the run folder.
  - Lei 9.029/1995, updated text (Câmara dos Deputados):
    https://www2.camara.leg.br/legin/fed/lei/1995/lei-9029-13-abril-1995-348798-normaatualizada-pl.html
  - Dias de Aquino Nascimento, B. (2026), "Firms' Responses to a Dismissal Tax: Evidence from Brazil", master's
    dissertation, PUC-Rio (advisors R. Narita, G. Gonzaga), on fake layoff agreements:
    https://www.econ.puc-rio.br/api/uploads/adm/trabalhos/files/28_mai_2026_2412634_Completo.pdf
  - Lei 8.213/1991 art. 93 and TST Tema 312 (quota and dismissal of disabled workers), e.g.
    https://www.migalhas.com.br/coluna/migalha-trabalhista/444412/tst-julgara-se-demissao-de-pcd-e-reabilitados-exige-substituto-previo
  - LGPD sensitive data and art. 20 in employment (practitioner commentary):
    https://www.barbieriadvogados.com/dados-sensiveis-na-lgpd/ ;
    https://mpt.mp.br/pgt/publicacoes/doi/livros/o-uso-de-dados-pessoais-e-inteligencia-artificial-na-relacao-de-trabalho/decisoes-automatizadas.pdf
  - Attrition-model practice (vendor guidance, not peer reviewed: AUC 0.65-0.80, top-decile lift, calibration,
    out-of-time validation): https://everworker.ai/blog/ai_turnover_prediction_accuracy_validation_retention ;
    https://hyring.com/free-hr-toolkit/frameworks/predictive-attrition-framework
  - RAIS age reference date: searched, not found (metadata lists `idade` without a date); stays open as in the notes.
  - From my own knowledge, not re-read: Constituição art. 7 XXX-XXXI; Lei 14.611/2023 (equal pay report); CLT art.
    484-A; eSocial S-2200 fields.

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: rais_employment_separation (target quit_by_year_end, binary, 1.5M rows x 23 cols, IID 3-fold)
Inputs used: clean_room/data.parquet (200,000-row sample), clean_room/task.md, the public pages task.md links to
(basedosdados RAIS page, CRAN raisr page, MTE microdata page via search), and web news on the RAIS 2025 release.
No other local files were read. Scratch scripts: lgb.py, lgb2.py in the run's panel folder.

VERDICT: Include with changes. The task is real, has a meaningful signal (AUC about 0.77-0.80), is large, and is not trivial.
But task.md does not document the target, population and reference date. The tenure feature was recomputed in an
undocumented way, and some columns are redundant or nearly empty. These need to be documented or fixed first.

WHAT THE TASK IS (inferred from the data, because task.md does not say)
- Rows are formal employment links from RAIS (Brazil's annual census of formal jobs). The data come from a single base year,
  2025: the 2025 minimum wage of R$1,518 appears 6,098 times in pay_january, against 174 times for the 2024 value of
  R$1,412. The MTE published RAIS 2025 on 13 May 2026.
- The population is links active in January. Feature values are measured in January. 93.9% of rows are "Not admitted in the year".
  All 11,022 rows with "Re-employment" have tenure_months of 0-2, so only January hires are present. RAIS tempo_emprego is
  normally measured at 31 Dec or at separation, so tenure must have been recomputed to a January reference.
- The target is whether the worker quits by 31 Dec. The positive rate is 7.26%. By sector the rate is 1.5% in public administration
  and 11.0% in retail trade, and it is 0.47% for tenured public servants. This pattern fits a worker-initiated resignation, not any separation:
  the any-separation rate would be several times higher.
- Who would use it and why: labour-market researchers or policy analysts studying turnover, and HR attrition
  modelling in general. Predicting in January who will resign during the year is a real, standard question. An
  employer would have richer data than public RAIS, so this is a stylised but legitimate version of the task.

SIGNAL / DIFFICULTY (LightGBM, 3-fold stratified CV on the 200k sample)
- All features with native categoricals: AUC 0.769. Tenure alone: 0.733. Four features (tenure, worker_category, age, pay_january): 0.766.
- Without tenure: 0.738. Dropping the 6 high-cardinality code columns: 0.783. Those codes as plain integers: 0.797.
- One-hot logistic regression: 0.785. Signal is moderate, not saturated, and models differ. The data is big enough:
  about 109k positives in the full 1.5M rows.

CONCERNS, MOST TO LEAST SERIOUS
1. Target, population and feature timing are undocumented, and the way tenure was computed cannot be checked (possible leakage route).
   Evidence: tenure_months is not the raw RAIS value (see above). There are date-arithmetic artifacts:
   - 586 rows have tenure_months = -0.0. Their positive rate is 44% (253/569 among re-employments), against 18% for the
     5,228 rows with +0.0. Median January pay for the -0.0 rows is 270, so these are late-January hires. A negative raw value
     means the hire date falls after the tenure reference date.
   - 118 rows are hired in the year but have tenure 2. This is inconsistent with a January hire.
   Comparison operators treat -0.0 as equal to 0.0, so trees cannot use the sign. Still, it shows tenure comes from a date
   computation whose reference point is not stated. If the reference point depended on the separation month (RAIS
   tempo_emprego minus elapsed months), tenure would carry the label. The monotone, smooth quit-rate-by-tenure curve
   (22% at 1 month, 1-3% beyond 60 months) argues against a gross leak, but I cannot verify it.
   Change: state in task.md the RAIS year, the population filter (active in January?), the label definition
   (which motivo_desligamento codes count as quitting, and how quits in January are treated), and the formula for tenure_months.
   Recompute tenure from the admission date to a fixed date (1 Jan or 31 Jan) only, and normalise -0.0 to 0.0.
2. A random IID split does not match deployment.
   - The data is one cross-section with no establishment identifier. Coworkers of the same employer fall into both train
     and test, so firm-level events leak through high-cardinality codes such as municipality x CNAE subclass x CBO.
     Examples: mass resignations, closures, public fixed-term contracts ending.
   - Real use would score a new year's January cohort.
   - IID is acceptable as a first approximation, but scores will be optimistic. If another RAIS year is available,
     train on year t and test on year t+1. Otherwise, at least state the limitation.
3. Redundant and nearly empty columns.
   - work_municipality is 99.62% missing. When it is present, rows are almost never positive: it is filled in 0.41% of
     negatives and 0.007% of positives. This is a reporting artifact, not a worker attribute, so drop it or explain it.
   - cnae_class equals the first 5 digits of cnae_subclass in 99.994% of rows, so it is a deterministic copy.
     ibge_subsector is a coarse aggregate of the same thing.
   Change: drop work_municipality and cnae_class, or keep the hierarchy deliberately and document it.
4. High-cardinality codes are stored as categoricals: municipality (5,189 levels), occupation_cbo (2,138), cnae_subclass (1,229),
   cnae_class (657) and legal_nature (63).
   - With LightGBM native categoricals, including these columns lowers AUC: 0.769 against 0.783 without them. As
     integer codes they raise it to 0.797, because IBGE and CBO codes are hierarchical (state prefix, occupation family).
   - Benchmark rankings will therefore depend heavily on how each method treats these columns. This is a valid
     challenge, but document it. Consider adding state (first 2 digits of the IBGE code) and CBO family (2-4 digits)
     as columns.
5. pay_january semantics.
   - 23,561 rows (11.8%) are exactly 0, including 8,951 full-time open-ended CLT workers employed since before January.
     These are probably on leave or have unreported pay.
   - 158 values are negative (minimum -5,623) and the maximum is 1,372,324.
   - For January hires the value is a partial-month amount.
   It is not a leak: the quit rate is not extreme in low-pay bins (8-16%). But the meaning of 0 should be documented, or a
   flag added.
6. Missing-value coding.
   - race is NaN in 3.7% of rows, probably "not identified".
   - legal_nature is NaN in 2.45%.
   - weekly_hours is NaN in 2.3% overall and 72% for intermittent contracts.
   - age is NaN in 2 rows.
   These are acceptable, but say whether NaN means "not reported".
7. Population composition.
   - About 18% of rows are public administration, where quits are near zero.
   - Seven worker categories (military, union leaders, casual port workers, ...) have zero positives in the sample.
   These are easy negatives that inflate AUC. This is optional, but a private-sector-only (CLT) version would be a
   cleaner turnover task.
8. Duplicates are minor. 693 rows (0.35%) duplicate another row on all features. They are mostly public administration
   with pay 0, and only 2 duplicate groups have conflicting labels. Public RAIS has no worker ID, so I cannot tell whether
   one person appears with several links.

DATA AUTHENTICITY: The values look like real administrative data, not generated data. There is heaping at the minimum wage,
at 44 and 40 weekly hours, and at even-month tenures. Category frequencies are plausible: Venezuelans and Haitians are the
top foreign nationalities, and Sao Paulo (355030) and Rio (330455) are the top municipalities. Ages run from 14 to 99, with
130 rows over 80.

COULD NOT CHECK
- The preparation code, the label's exact motivo_desligamento codes, and the tenure formula.
- The other 1.3M rows: I worked only on the 200k sample.
- The RAIS 2025 vinculos layout document: the PDF could not be parsed here, and the basedosdados table pages did not render.
- Whether 'vinculos abandonados' (links abandoned but still recorded as active, flagged by MTE since RAIS 2024) were
  removed. These would be silently labelled as non-quits.
- Grouping by establishment or worker, because no IDs are present.

Sources: https://basedosdados.org/dataset/3e7c4d58-96ba-448e-b053-d385a829ef00 ;
https://cran.r-project.org/web/packages/raisr/index.html ;
https://agenciabrasil.ebc.com.br/economia/noticia/2026-05/brasil-fecha-2025-com-aumento-de-5-no-estoque-de-empregos ;
https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/rais/rais-2025/apresentacao-rais-2025.pdf

</details>

<details><summary>Task gamer</summary>

TASK GAMER REPORT: rais_employment_separation (quit_by_year_end, ROC AUC, IID, 1 x 3 folds, 1.5M rows)
Scripts and logs: participant_kit/work/

VERDICT: barely gameable. No exploit I found gains more than +0.001 AUC over an honest model. The largest is
group sizes counted over train+test rows (+0.0009, and +0.0005 of that is plain establishment-size signal).
A tuned honest model gains +0.0035 over the untuned baseline, more than any exploit.

SCORES (mean over the 3 shipped splits; per split in brackets)
  Honest baseline, untuned LightGBM on features()     0.79572 [0.79581 0.79446 0.79687]   work/baseline.py
  Honest A: + code prefixes, pay/hour, pay==0 flag    0.79685 [0.79698 0.79549 0.79808]   work/honest_tuned.py a
  Honest B: same features, slower regularised LGBM    0.79922 [0.79904 0.79840 0.80021]   work/honest_tuned.py b
  Noise check: baseline + one random column           0.79572 / 0.79566 (two seeds); per split up to +-0.0003

EXPLOITS RANKED BY GAIN
| # | Exploit | Script | Honest | Exploited | Gain (per split) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Sizes of rebuilt establishment/cohort keys (municipality x CNAE x legal nature x simples x estab type, +CBO, +pay, +tenure), counted over ALL rows incl. test | work/exploit_copies_counts.py cnt_all | 0.79685 (A) | 0.79771 | +0.0009 (+0.0017 +0.0009 +0.0001) | Mostly yes: the same counts over train rows only give +0.0005 (cnt_train 0.79735), and establishment size is known on 1 Feb. Only the extra ~+0.0004 needs the test rows. | None needed. Optionally ship an establishment-size band column so the count is not needed. |
| 2 | Co-workers' labels from the same year: train residuals in the same cohort (municipality, CNAE, pay_january, tenure) added to the test logit | work/exploit_coworker_resid.py | 0.79685 (A) | 0.79702 | +0.00017 (+0.00015 +0.00015 +0.00019) | No (this year's quits by co-workers happen after 1 Feb), but the gain is about the size of the noise | Group or temporal split (by establishment, or train on year t-1 and test on year t) if establishment ids ever get added. Not needed now. |
| 3 | tenure_months recorded with the outcome (see finding below). Already in the baseline, so it inflates the honest score rather than adding a gain | work/tenure_artifact.py fix_jan / jitter | 0.79551 (fix) | 0.79572 (as shipped) | +0.0002 (+0.0001 +0.0006 -0.0001); upper bound +0.0005 | No: a January hire's tenure on 1 Feb cannot be 1-2 months | Recompute tenure at 1 Feb from the admission date (or year/month), or round it to whole years for rows hired within the last 2 months |
| 4 | Exact copies of test rows in train, blended with their labels | work/exploit_copies_counts.py copies | 0.79685 | 0.79686 | +0.00001 | n/a | None needed |

FINDING 3, TENURE MEASURED AT THE END OF THE LINK: links hired in January (admission_type = Re-employment, 81,840
rows) had less than one month of tenure on 1 February, yet tenure_months is 0, 1 or 2 for them, with quit rates
of 0.212, 0.121 and 0.037. Within this group, tenure alone has an AUC of 0.585. The column seems to be built
back from RAIS 'tempo de emprego' (counted to 31 Dec or to the separation date), minus the months that elapsed.
For leavers the separation day is unknown, which pushes their value down. Setting tenure to 0 for all January
hires costs 0.0002. Adding +-1 month of noise to every row's tenure costs only 0.0005, so tenure at month
resolution (artefact plus real signal) is worth at most 0.0005. Mildest fix: derive tenure from the admission
date on 1 Feb.

FLAWS THAT HURT AN HONEST MODEL: none found. Adversarial train-vs-test AUC is 0.499, and the folds are
stratified (label rate 0.07231 in every fold). I found no training rows that a deployed model would drop or
label differently.

ATTACKS THAT FOUND NOTHING
- Row order: AUC of row position 0.4998, label rate by decile 0.0714-0.0735, lag-1 label correlation 0.0001,
  no column is sorted (share nondecreasing about 0.51), RangeIndex.
- Exact copies: 1.1% of rows are in feature-identical groups, almost all non-quitters (rate 0.006). 0.9% of
  test rows have a train copy. Blending in the copies' labels: +0.00001.
- Co-workers' labels as a target encoding: est key LOO AUC 0.64 alone, but in the model OOF TE scores 0.79425
  (-0.0015 vs the baseline). Residual shrinkage on est / est x CBO keys: -0.0002 to -0.005.
- Formats: age, tenure and hours are whole numbers. pay_january has cents in 75% of rows. A format-only model
  (pay==0, cents==0, last digit, number of digits, missing flags) reaches AUC 0.615, almost all of it from
  pay==0 (11.8% of rows, quit rate 0.018). pay==0 marks categories (military, casual, public fixed-term,
  intermittent) and Jan leave, which a deployed model has. The last cent digit 1-9 does nothing
  (0.077-0.081).
- Missing values: work_municipality is present in 0.4% of rows (quit rate 0.001), but only for casual/port
  workers, workers on loan and directors: a proxy, not a leak. race is missing in 3.8% of rows (rate 0.013,
  and 0.019 vs 0.087 among general employees). Imputing it away costs 0.0002, so whatever it is, it is
  negligible.
- Transforms over all rows: none; values are raw (codes, BRL, months).
- Lookup / shallow rule: none. The strongest single columns are contract_type, worker_category and tenure,
  all plausible at 1 Feb.
- Public "magic features": RAIS is a government register with no competition forum. The web search found no
  leak threads. Rows could not be looked up in the source file (no key; downloading the regional RAIS 2025
  .7z files was not attempted).

WHAT I COULD NOT CHECK
- Whether contract_type, worker_category, occupation_cbo, weekly_hours and age are the values on 31 Dec (or at
  separation) rather than on 1 Feb. RAIS reports the link's state at year end or at separation, so for
  example a fixed-term contract or an apprenticeship converted later in the year would show the later state for
  stayers only. The deciding fact is whether the preparation took these from monthly eSocial events or from the
  annual RAIS row. If from the annual row, the fixed-term (rate 0.29) and apprentice (0.24) categories may be
  partly post-outcome.
- pay_january: January pay is paid and declared in early February (eSocial deadline 15 Feb), so it may not be
  known exactly on 1 Feb. Dropping it costs 0.0037. Whether this counts as a leak depends on whether the
  deployment point is 1 Feb or mid-February.
- The source row-level file (to see exactly how tenure_months and the population filter were built).

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER REPORT: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-09

Read: principles.md (Tensions, Exceptions and amendments, Consistent judgement), selection.md SEL-1, use_case.md USE-1
to USE-9, leak_checks.md LEAK-6, LEAK-10, LEAK-22, LEAK-25 (and the Mechanisms and Cases rows), splits.md SPLIT-8,
SPLIT-14, SPLIT-20 (and Cases), cleaning_features.md CLEAN-12 (and Cases), all from the df-large worktree; the
definition, the record, the builder report, the four phase-A reports, register.json (flags and the decisions behind
them), sibling records and definitions (grep over curation/records and datasets/_dev/tabarena-v0pt2), and the
same-batch builder reports of wioa_employment_after_exit, ny_wcb_assembled_claims, chile_school_dropout_mineduc,
sinan_dengue_case_screening, kumc_inpatient_aki_prediction. Nothing edited, nothing run beyond reading.

SUMMARY
  D1 protected grounds kept as features ........ departs without a reason (the tension row's reasoning gives "drop
                                                  all five"; its scope sentence names pricing only). Prompt below.
  D2 one year, forced IID ...................... consistent (SPLIT-8, distribution_transformers); the reason the
                                                  notes give is the wrong one (download count, not the series break).
  D3 age kept, "cannot verify" ................. superseded: two panel tests traced it with opposite results; the
                                                  precedent outcome follows the fact (EV-1 first).
  D4 target 20 + 21, Feb-Dec ................... consistent (LEAK-22 framingham; USE-5 diabetes_3); code 90 is an
                                                  open call with no precedent; the never-paid links depart from the
                                                  LEAK-25 precedents without a reason. Prompt below.
  D5 CBO, CNAE, CONCLA, IBGE kept as codes ...... departs with a stated reason that does not set it apart; three
                                                  same-batch definitions take the same departure (amendment due if
                                                  all are accepted). Prompt below.
  Register flags touching this case: amendment_due SPLIT-14 (5 datasets) - not touched, this dataset ships under
  SPLIT-8 and takes no SPLIT-14 exception; drift "post-outcome feature" (Lennart keep to 11-05, exclude from 11-08) -
  bears on D3: the newest calls lean to removing traced post-outcome values; opposite_outcomes USE-5 (diabetes_3 keep,
  xente exclude, chicago_traffic_crashes keep) - none is about which separations count, so no pair with D4.

D1. Sex, race, age, nationality and disability as features of an employer's retention score (P1 SEL-1; Tensions row
    "a factor the actor may no longer use"; USE-1, USE-6)
As implemented: all five kept, with a note quoting Lei 9.029/1995 art. 1 and leaving the call to the curator.

Precedents
  * bemtpl97, 2026-11-05, Lennart (curation/records/bemtpl97.md, CC issue 3 (a)): `sex` dropped; "we would try to
    understand how good such models would be in the current world, and they would not be able to use sex". The
    reasoning is the actor's legal constraint today.
  * australian_vehicle_insurance_2004_2005, 2026-11-08, Lennart (issue 7, then (a) of the consistency check): `gender`
    dropped though Australian law may allow it, "a stance for the family; as if we were to simulate the case in europe
    always". The row was amended so: sex leaves every insurance pricing task, whatever the jurisdiction.
  * pricing_game_2017_french_mtpl, frempl_french_motor_personal_line, spanish_homeowners_motor_insurance_2010_2014
    (all 2026-11-08): sex dropped under the family stance, even where legal in the data's year.
  * Insurance never drops age: age is a lawful rating factor under the EU rule the stance imitates. This is no
    precedent for keeping age here, where the actor's own law lists age.
  * home_credit_default_risk (`CODE_GENDER`), credit_card_clients_default (`SEX`): kept, marked "credit not
    insurance, not reviewed yet" in the Tensions row itself.
  * hr_analytics (built 2026-10-14; Lennart's CCs on the build, probes and dtypes): `gender` kept in a recruiter's
    decision on whom to refer to employers; the protected-ground question was never raised. An unreviewed keep, not a
    decision on the point.
  * adult (legacy CC, `No`): "Potential ethical issues from including race as a feature" is one of the reasons given.
    compas_compas_two_years: `No`, `Ethical Issue`. Both lean towards treating protected features in decisions on
    people as an ethics question.
  * Same batch, pending, AI recommendations only: wioa_employment_after_exit_1m (race, sex, disability, ex-offender
    status kept; reason: DOL's own adjustment model uses them, the decision allocates help); ny_wcb_assembled_claims_1m
    (sex kept; reason: claims triage, not pricing). siab_long_term_unemployment (screening): the source paper itself
    leaves gender and nationality out.

Comparison of the facts that matter
  * The row's reasoning (bemtpl97) is "the actor's legal constraint today". Here the bar is the named actor's own law
    (Lei 9.029/1995 art. 1, read on the Câmara text by the builder, the domain practitioner and the claim auditor). It
    covers "manutenção" of the relation, and raises are pay (CF art. 7 XXX). The facts are stronger than in any
    insurance case: australian and pricing_game_2017 dropped sex where it was legal.
  * The row's stop ("a use case set in the data's own time keeps the factor") does not help: the law was in force in
    2025, the data's year, and the use case is set then.
  * The row's scope sentence names insurance pricing. Applying it to an HR decision extends it. Keeping the five
    factors departs from the row's reasoning. So the call is a deliberate change of the row either way: a new row or
    an amended scope (principles.md: "A new decision on a tension not listed becomes a row").
  * Distinguishing facts offered so far, checked:
    - "the use case is ours / approximate": this holds for bemtpl97's 1997 portfolio as well, and Lennart dropped sex
      there. It does not set the case apart.
    - "the decision allocates a benefit, not a denial" (wioa's argument): Lei 9.029 bars the practice for keeping a
      job, which is what a retention offer serves. It does not set RAIS apart.
    - "the agency itself uses the factors" (wioa: DOL's TEGL 26-15 model): a real fact for wioa, absent here. This
      sets wioa apart from RAIS, not RAIS apart from the row.
    - "age is the strongest real signal" (0.006 ROC AUC): the size of a gain is no fact that sets a case apart (the
      LEAK-10 X4 wording, 2026-11-08, by analogy). The law lists age next to the others.
  * Option (b) of the builder (drop sex and race only) follows neither precedent. The insurance stance drops sex only,
    never race. The legal-constraint reasoning drops every listed ground. It would need its own fact.
  * Ranking: SEL-1 is a P1 Must. If the curator reads "a feature the actor is barred from using" as an ethical concern,
    keeping is not a reasonable exception under the ranking: a Must that can be fixed in the definition is fixed (the
    remedy ladder), and only an amendment could keep the factors. Measured cost of the fix: four grounds <= 0.001 ROC
    AUC, all five about 0.006-0.007 (column auditor, 3 seeds; domain practitioner, fold 0).
  * Drift: none. Lennart's calls on sex in pricing are uniform from 2026-11-05 to 2026-11-08. Nothing has been decided
    outside insurance yet.
  * Siblings the answer should reach (decided alike or set apart by a named fact): wioa_employment_after_exit_1m,
    ny_wcb_assembled_claims_1m, hr_analytics, and the two credit tasks the row already marks "not reviewed yet". Per
    the per-dataset rule, each gets its own REVIEW.md issue; the row's amendment carries the stance.

Reflection prompt (issue shape):

   **Consistency check (AI, 2026-11-09):** Do sex, race, age, nationality and disability leave the features, as the insurance stance's reasoning gives, or what sets this retention task apart from bemtpl97?
   - **Problem:**
     - The definition keeps all five, and Brazilian law bars an employer from using any of them in decisions on keeping a job[^d1law].
     - Lennart dropped sex from every insurance pricing task because a model "would not be able to use sex" in the current world, even where the actor's own law allowed it[^d1row].
     - No written fact sets this case apart: the actor's bar is stronger here, and it already held in 2025, the data's year.
   - **Consistency:** australian_vehicle_insurance_2004_2005 and pricing_game_2017_french_mtpl dropped sex where it was legal (2026-11-08); hr_analytics keeps `gender` in a referral decision, never reviewed; wioa and ny_wcb (this batch) recommend keeping, for reasons that do not apply to an employer.
   - **Effect on the task:** dropping sex, race, nationality and disability costs at most 0.001 ROC AUC, and dropping age too costs about 0.006[^d1cost].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Drop all five, recorded as the stance extended to decisions on employees | the five columns leave; the Tensions row covers any decision on a person whose factor the actor's law bars | follows the row's own reasoning; also settles the age reference-date question; small cost | first case outside pricing, so the row is amended; age is a real signal |
     | b | Keep all five, recorded as an amendment that the stance is for insurance pricing only | the note stays; the row says so | keeps the data's analytic signal | no fact sets it apart from bemtpl97; a P1 concern left unfixed when the fix is cheap; hr_analytics and the credit tasks would stay as they are by default |
     | c | Drop sex, race, nationality and disability; keep age as an exception with a stated fact | four leave, age stays | keeps most of the signal | the law lists age with the others; no fact yet names why age differs |
     | d | Drop sex and race only (builder's option b) | two leave | matches the insurance list for sex | follows neither the insurance stance nor the legal reasoning |
     | e (implemented) | Keep all five with the note, no stance recorded | as now | no change | an open departure from the row, with no fact recorded |

   - **Recommendation:** a; then decide wioa_employment_after_exit_1m, ny_wcb_assembled_claims_1m and hr_analytics on the amended row, each in its own issue.
   - **Decision:** a, b, c, d or e?

   [^d1law]: Lei 9.029/1995 art. 1 (as amended by Lei 13.146/2015): "É proibida a adoção de qualquer prática discriminatória e limitativa para efeito de acesso à relação de trabalho, ou de sua manutenção, por motivo de sexo, origem, raça, cor, estado civil, situação familiar, deficiência, reabilitação profissional, idade, entre outros" (https://www2.camara.leg.br/legin/fed/lei/1995/lei-9029-13-abril-1995-348798-normaatualizada-pl.html).
   [^d1row]: principles.md, Tensions, "A rating factor known at the prediction point against a factor the actor may no longer use" (P3 and P4; USE-1, USE-6); bemtpl97 CC 2026-11-05; australian_vehicle_insurance_2004_2005 CC 2026-11-08 ("as if we were to simulate the case in europe always"); SEL-1 (Must): a task with ethical concerns is out.
   [^d1cost]: column_auditor.report.txt issue A (600k/400k, 3 seeds: four grounds -0.0001 to -0.0008, all five -0.0059 to -0.0065); domain_practitioner.report.txt section 4 (fold 0: 0.7917 to 0.7916, then 0.7845).

**D2. One year (2025), forced IID, instead of yearly windows (P4; SPLIT-8, SPLIT-14, SPLIT-20)**
Status: CONSISTENT with SPLIT-8 and its closest case. The reason written in the notes is not the fact that makes it so.

Precedents
  * distribution_transformers_at_cauca_department, 2026-10-21, Lennart (CC: "option (a) of the cross-dataset item on
    tasks with too few periods ... the cost measured against the valid windows", SPLIT-8 amended). Two label years
    give one window; the newer year ships IID, ForcedIIDFromTemporal, and the years are not stacked because the files
    hold near-copies of the same units. RAIS has the same facts: the claim auditor links 48% of Norte stayers across
    2024/2025 on 12 fields plus tenure. The notes give the same reason for not stacking.
  * SPLIT-8 cases: mobile_churn, account_debt_south_africa, open_university_learning_analytics_dataset (all
    2026-10-12/21, Lennart). 24 definitions carry ForcedIIDFromTemporal; being forced never makes a dataset `No`.
  * chile_school_dropout_mineduc_1m (this batch, AI, not yet reviewed): also a ministry's yearly census of a Latin
    American country. Its builder read seven yearly files (2018-2024) and shipped three temporal windows (first train
    side 56%), with the COVID years kept in the history. This is the sibling that looks decided the other way.
  * perth_house_prices (SPLIT-20 row, 2026-10-26, Lennart): COVID months handled by placing the windows, not by
    leaving the data temporal-less.

What sets RAIS apart from chile
  * The fact is the 2022/2023 break in the series: base years 2022 and 2023 moved employers to eSocial, and the
    ministry advises against comparing across the break (split auditor, via Fenacon and the MTE's RAIS 2022 note).
    The header also changed in 2023 (raisr: two formats; the builder asserts 2023-2025 share one). The eSocial worker
    category the definition ships is not in the 2020 layout (column auditor). SPLIT-20 names "a change of rules or of
    the data collection" as a break to keep out of the history. With three post-break years there is one valid window,
    and the 40% extension of SPLIT-14 needs recurring entities, which RAIS cannot show without ids. SPLIT-8 applies.
  * COVID is NOT a distinguishing fact: chile keeps COVID years in its training history. The builder report names
    COVID next to the break; only the break carries the argument.
  * The definition's own text gives the wrong reason. curation_comments says "about six years of files. We downloaded
    two (2024 and 2025)" and "Ship yearly windows if more years are downloaded". A download count is no fact that sets
    a case apart; chile downloaded seven. The break, stated in builder issue 2, is not in the notes. The split auditor
    (problem 3) already proposes the rewording ("revisit when the post-2023 stretch holds six base years, or if linked
    RAIS microdata become available"). I concur: the consistency depends on the notes naming the break.
  * Small point: SPLIT-8 asks for the cost "against the valid windows where the data has any". The valid window is
    train 2023+2024, test 2025. The cost was measured with train 2024 only (2023 not downloaded): -0.0057 on the
    shipped folds (split auditor), -0.0059 (claim auditor). Close enough to stand as the cost. Say in the notes that
    it is a one-year training side.
  * SPLIT-14 amendment_due flag: RAIS takes no exception to SPLIT-14 (it ships under SPLIT-8), so it does not add to
    the five.
No reflection prompt (consistent). A wording fix for the notes: replace the download-count reason with the series break
(SPLIT-20), drop "COVID" as a reason, and give the cost on the shipped folds.

**D3. `age` kept with an undocumented reference date, "Potential leak, kept on purpose" (P4; LEAK-10, LEAK-6)**
Status: the position "cannot verify, kept with a note" was consistent at build time and no longer is. The panel traced
the value. Under precedent the outcome now depends on a fact that two panel members measured with opposite results.

Precedents
  * LEAK-10 second clause (amended 2026-10-26, Lennart): a value read at a later pull stays with a note only when the
    part that can be traced shows no gain: onlinenewspopularity's crawl-time counts, "go with (a)". It goes when a gain
    may sit on it: distribution_transformers_at_cauca_department. LEAK-6: a confirmed leak goes even when small
    (santander `has_*`, +0.003 AUC).
  * Register drift flag, mechanism "post-outcome feature": Lennart's calls lean to removal from 2026-11-08 on.
  * Sibling mechanism in this dataset: the year's last declared values (contract type, occupation, hours). The claim
    auditor measured the contract-type conversion at +0.0175 ROC AUC on January hires and refuted "such changes are
    rare". It is the same "values as of the link's end" family, located by tenure <= 3. Under the same clause, the
    located part is fixed (zillow_prize and melbourne_housing_market blank the located cells, LEAK-7).

The disputed fact (EV-1 first)
  * Column auditor: age is taken at the separation for leavers. Evidence: the 24+/23 ratio of 2025 apprentices by
    separation month. Effect +0.0006 ROC AUC in the full model, 3 of 3 seeds.
  * Claim auditor: age is taken at one fixed date. Evidence: 430,953 leavers linked to their 2024 rows show +1 year in
    96.5-98.1% of cases in every separation month.
  * The two tests cannot both describe a measurement at the separation. One explanation fits both: age computed as
    the base year minus the birth year. That would make the linkage show +1 everywhere, and the apprentice pattern
    would then reflect who leaves when, not when age is read. This is a hypothesis for the mediator, not a finding.
  * Precedent outcome by fact. If confirmed, it is a fix: harmonise in `_clean` (the column auditor's remedy, of the
    tenure-rebuild kind, LEAK-7) or drop. This follows distribution_transformers and santander. If refuted, age stays
    and the note gives the measurement (the onlinenewspopularity form). In neither case does "cannot verify" stay.
  * If D1 goes (a), age leaves and the question is moot.
No consistency prompt: there is no curator-level departure yet; the mediator settles the fact first.

**D4. Target: separation reasons 20 + 21 from 1 February to 31 December (P3, USE-5; LEAK-22, LEAK-25)**
Status: CONSISTENT on the parts with a precedent. One open call has no precedent (code 90). One sub-decision departs from
the LEAK-25 precedents without a reason (the never-paid links).

  * Competing events (dismissals, retirements, deaths after 1 February) labelled No: follows LEAK-22's
    framingham_heart_study_fhs (Lennart, 2026-10-22: 251 deaths stay with their label; dropping them would select on
    the future). Consistent.
  * Our cohort and target, `fit="approximate"`: follows diabetes_3 (Lennart, 2026-10-21: "keep the data and just mark
    it as approximate, and we can case-by-case decide the details"). Consistent.
  * Prediction point moved from the screening's 1 January to 1 February, with the reason that January pay is the
    first pay known before the outcome: a later stage's measured finding supersedes the screening (principles.md,
    Precedence: stages). Consistent.
  * Code 90 (agreement, art. 484-A CLT) counted No: no precedent decides which separations count as the actor's event.
    The reason the notes give, "the risk the employer faces includes them (LEAK-22)", misapplies LEAK-22. LEAK-22 says
    how a competing event is labelled. Whether an agreement is a competing event or the event itself is USE-5's
    question, "what the actor would act on". The builder (issue 4) and the domain practitioner (Yes) leave it open.
    This is a first call, not a departure, so no consistency prompt. Whatever is chosen, cite USE-5 for it, not
    LEAK-22.
  * The abandoned links dropped (decision 4): follows LEAK-25 (amended 2026-10-21, Lennart). Consistent.
  * The never-paid links kept as No: DEPARTS from the same precedents. Two panel members locate a larger unrecorded
    group with a rule that does not read the label: 9.6% of the cohort with no pay in any month, separation 5.7%
    against 30.0% (claim auditor); 8.4% with no pay and no leave (column auditor). The armed forces record no
    separation in 2025. The LEAK-25 cases drop such located rows: account_debt_south_africa (file runs without debt
    data), caracas_cervical_cancer. fraud_detection_in_electricity_and_gas_consumption_1m dropped clients by their last
    invoice date, so a locating rule may read later columns as long as it does not read the label. The definition
    keeps them, with no fact that sets them apart (the builder did not see the group).

Reflection prompt (issue shape):

   **Consistency check (AI, 2026-11-09):** Do the links never paid in 2025 leave the task as unrecorded outcomes, as the abandoned links and the LEAK-25 cases did, or what sets them apart?
   - **Problem:**
     - About 9.6% of the cohort was never paid in any month of 2025 and almost never shows a separation (5.7% against 30.0%), so its No is largely "not recorded"[^d4meas].
     - The definition drops the source's abandoned flag (1.2%) for this reason but keeps the larger group the same rule locates.
     - account_debt_south_africa and fraud_detection_in_electricity_and_gas_consumption_1m dropped rows located this way, the latter by a date read after the prediction point[^d4rule].
   - **Effect on the task:** the never-paid rows are easy negatives worth about +0.015 ROC AUC (0.797 against 0.782 scored without them, 3 of 3 folds).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Drop the links with no pay in any month in post (label-free, reads later pay), recorded with the LEAK-25 cases | about 9.6% of the cohort leaves; the armed forces mostly go with it | follows the precedents; removes outcomes that were never recorded | also drops some staff on long leave, who belong to the use case |
     | b | Drop the links with no January pay (known on 1 February) | 11.8% leaves | a rule known at the prediction point; matches "after the January payroll" | also drops 1.27M links with later pay (quit 6.1%) |
     | c | Drop worker category 314 only (no separation recorded in 2025) | 0.7% leaves | the clearest unrecorded group | leaves most of the group in |
     | d (implemented) | Keep them, with a note giving the numbers | as now | no new filter | departs from the LEAK-25 cases with no fact recorded |

   - **Recommendation:** a, with the leave-days caveat in the note.
   - **Decision:** a, b, c or d?

   [^d4meas]: claim_auditor.report.txt problem 2 (all 2025 files: 5,561,852 links; armed forces 0 separations; -0.015 ROC AUC); column_auditor.report.txt issue D (10% cohort sample: 8.4% never paid and no leave, quit 0.98%).
   [^d4rule]: LEAK-25 (Must; amended 2026-10-21, Lennart): "No event" mixed with "not recorded", the unrecorded rows located by a rule that does not read the label: drop the located rows and ship the rest. Cases: caracas_cervical_cancer, account_debt_south_africa, fraud_detection_in_electricity_and_gas_consumption_1m.

D5. Occupation (CBO), sector (CNAE subclass, class), legal nature (CONCLA) and municipality (IBGE) shipped as codes
    (P7, CLEAN-12)
Status: DEPARTS WITH A STATED REASON, BUT THE REASON AS WRITTEN DOES NOT SET THE CASE APART. A reasonable kind of
departure (a P7 Should, no higher Must at stake), once the right fact is named.

Precedents
  * CLEAN-12 (amended 2026-11-01, Lennart): "a nominal code (a job, a building type, a water source) into a category of
    the words"; "A column that still ships as a number while its source has words for it is a gap to close, not a
    choice". Applied that day to 377 columns in 29 definitions (Cases row).
  * credit_g / south German credit, 2026-10-31, Lennart: switched to the corrected code tables, "we want the right
    labels in all cases". Where the shipped codebook is wrong or old, the remedy is the right table, not keeping the
    codes.
  * zillow_prize census_tract, CC 2026-10-26: the encoding is chosen from the context; the model's score is "a model
    question, not a reason for the encoding". The builder's reason ("the digits carry the hierarchy") is a modelling
    argument. A category does not expose its digits (column auditor E).
  * Same batch, AI, not reviewed:
    - ny_wcb_assembled_claims_1m ships NAICS and WCIO as "words [code]", keeping both the words and the hierarchy.
    - sinan_dengue_case_screening_1m keeps the same CBO and IBGE municipality codes, and CNES units, as codes.
    - chile_school_dropout_mineduc_1m keeps the communes as codes and drops the file's own commune names as "copies of
      codes", which is the reverse of CLEAN-12.
  * No exception to CLEAN-12 is recorded yet. If RAIS, sinan and chile all take the same one ("a national
    classification with thousands of levels kept as codes"), that is three exceptions of one reason, so the next pass
    proposes an amendment (principles.md). Better to decide it once as an amendment or a decision now.

The fact that would set the case apart
  * The fact is that the release's own codebook is five years older than its codes. The 2020 sheets miss 6.4% of the
    CBO rows, 1.2% of the CNAE subclass rows and 11.8% of the legal-nature rows (1244 alone is 146k rows). CNAE 2.0
    class has no words in the layout. A decode from it would fail ("a code without a label raises") or leave holes.
  * Against it, the current official tables exist: the MTE's CBO list, CNAE 2.3 at IBGE CONCLA, natureza jurídica
    2021, IBGE municipalities. The remedy ladder starts with repair from the origin, and the 2020 layout already names
    every municipality but one (510183, 32 rows).
  * The CBO decision here and in sinan_dengue_case_screening_1m concerns the same code list: decide them alike.

Reflection prompt (issue shape):

   **Consistency check (AI, 2026-11-09):** Do the occupation, sector, legal-nature and municipality codes ship as the official tables' words with the code in brackets, or stay codes as an exception whose fact is the outdated codebook?
   - **Problem:**
     - The definition keeps four national classifications as codes because "the digits carry the hierarchy", which a model that reads a category does not see[^d5rule].
     - The fact that could set the case apart is different: the release's 2020 codebook lacks 6.4% of the occupation rows and 11.8% of the legal-nature rows of 2025.
     - sinan_dengue_case_screening_1m (same CBO and municipality codes) and chile_school_dropout_mineduc_1m make the same choice, and ny_wcb_assembled_claims_1m decodes into "words [code]"[^d5batch].
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the codes, recorded as an exception: the release's codebook is older than its codes | as now, with the note naming the coverage gaps | no lookup files; no risk of a wrong label from a mismatched table | a third exception of the same reason in this batch, so an amendment is due; the words exist in the current tables |
     | b | Decode from the current official tables into "words [code]" | lookup files in the folder; words and digits both kept | follows the rule and the ny_wcb form; right labels, as credit_g asked | lookup files to source and check; table versions to pin |
     | c | Decode only the municipality from the 2020 layout ("UF-Name [code]"); keep the others as codes with the exception | partial | cheap; the layout covers it | mixed treatment within one dataset |
     | d | Amend the rule: a national classification with thousands of levels may ship as its code | one rule for RAIS, sinan, chile | settles the batch at once | the curator's 2026-11-01 rule names "a job" among the codes to decode |
     | e (implemented) | Keep the codes with the hierarchy reason | as now | no change | the reason does not set the case apart |

   - **Recommendation:** b, applied alike to sinan_dengue_case_screening_1m's CBO and municipality.
   - **Decision:** a, b, c, d or e?

   [^d5rule]: CLEAN-12 (Should; amended 2026-11-01, Lennart): a code whose codebook says in words what it means is decoded into those words, a nominal code (a job, a building type) into a category of the words; zillow_prize CC 2026-10-26 (an encoding chosen from context, a model's score "not a reason for the encoding"); credit_g 2026-10-31 ("we want the right labels in all cases").
   [^d5batch]: principles.md, Exceptions and amendments: when the same reason has produced three exceptions, the next pass proposes an amendment; column_auditor.report.txt issue E (coverage of the 2020 sheets).

ALSO NOTED (no prompt)
  * The record says `required_split: Temporal (NON-IID)` and the definition ships IID with ForcedIIDFromTemporal. These
    agree: the tag records the source regime (split auditor point 4).
  * The accepted-warning text for legal nature 1015 ("almost never resign") is contradicted by the claim auditor: the
    armed forces record no separation at all. It changes with D4's answer.
  * Code 24 ("median age 26") is refuted (38 in 2025). It does not change any precedent call; it is a writing fix.

Paths
  Precedent records (df-large/curation/records/): bemtpl97.md, australian_vehicle_insurance_2004_2005.md,
  pricing_game_2017_french_mtpl.md, hr_analytics.md, adult.md, compas_compas_two_years.md, wioa_employment_after_exit.md,
  distribution_transformers_at_cauca_department.md, chile_school_dropout_mineduc.md.
  Definitions (df-large/datasets/_dev/tabarena-v0pt2/): wioa_employment_after_exit_1m, ny_wcb_assembled_claims_1m,
  sinan_dengue_case_screening_1m, chile_school_dropout_mineduc_1m, distribution_transformers_at_cauca_department,
  zillow_prize, hr_analytics.

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-09

Position: ship. The task is real and the evaluation is honest at its core. Every problem the panel found has a fix
inside the definition, at most 0.015 ROC AUC, and none needs exclusion (remedy ladder, principles.md "How to decide"
5). Where a fix needs the curator's call, I name the mildest one and do not deny the problem.

1. A real task on real, unique data, worth benchmarking (P2, P3, P5, P6 hold).
   Evidence: RAIS is the mandatory annual filing of every Brazilian employer: 91,710,262 links, sha256 of all 7 files
   verified (claim auditor 2, 3). The blind reviewer, seeing only the data, inferred the task unaided and called it
   "a real, standard question". The domain practitioner agrees the fit is approximate and would use it as a vendor's
   cold-start model. No task-probe flags: dummy 0.5, linear 0.780, LightGBM 0.797, tuned 0.799 (task gamer). Each test
   fold has 36,155 positives (MET-2).
   Rules: SEL-16, PROV-3 (Must, hold); USE-1 (Must, approximate fit stated, USE-8); TP-1 to TP-10; MET-2.
   Why it outranks: the objections below are about features and rows, not about whether the task exists. The Tensions
   row "a real task against a leak" says fix the leak and keep the task.

2. The core is honest: no exploit is worth more than 0.001.
   Evidence: task gamer: best exploit +0.0009 (and +0.0005 of that is honest establishment-size signal); adversarial
   train-vs-test AUC 0.499; row order, formats and copies give nothing. Every post-outcome field is dropped (column
   auditor: "None of them should come back"). Target codes 20/21 match the 2020 manual, and commissioned
   exonerations are code 11, not 21. There is no December censoring: the 2024 December spike is the election-year
   public sector (claim auditor 12, 17).
   Rules: LEAK-10, LEAK-24, LEAK-27 to LEAK-31 (Must, hold).

3. Forced IID is the regime SPLIT-8 prescribes, and its cost is measured and small.
   Evidence: on the shipped folds a 2024-trained model scores 0.7915 against 0.7971 (-0.0057, 3 of 3 folds; split
   auditor). Same-year cell sharing is +0.004 to +0.005 of that, and five learners keep their order under both
   protocols. The 2022/2023 eSocial break leaves 2023-2025 as one valid window (SPLIT-20), which sets RAIS apart from
   chile_school_dropout. Precedent: distribution_transformers_at_cauca_department.
   Rules: SPLIT-8 (Must, applied); SPLIT-14 not reachable; SPLIT-24 bars the proxy grouping.
   Fix (needs no decision): put the series break in the notes instead of the download count, use the shipped-fold
   numbers, and add the cell-sharing number (split auditor 1-3; precedent checker D2).

4. Protected grounds (P1, SEL-1): a real question. Dropping them fixes it and keeps the dataset.
   Concession: Lei 9.029/1995 art. 1 bars an employer from using these grounds to keep a job. The Tensions row's
   reasoning ("the actor's legal constraint today", bemtpl97) points to dropping them. I cannot argue "keep all five"
   without a fact that sets this case apart, and none has been offered.
   What follows: the ethics concern is about the inputs, not the task. Subjects do not object: this is a public,
   de-identified census, and predicting quits harms no one. So SEL-1 is met by fixing the definition, not by
   exclusion. Cost: the four grounds other than age <= 0.001 (3 seeds); all five 0.006-0.007 (column auditor A;
   practitioner). Which option to take (c: drop all five, or a/b) is the curator's stance call (Tensions row
   amendment). Every option ships.

5. The small leaks found are fixed in the definition and need no decision.
   - contract_type conversion (claim auditor 1, LEAK-10 Must): +0.0175 on January hires, +0.001 overall. Fix: for
     tenure_months <= 3, merge CLT fixed-term 60/65/70/75 into 10/15/20/25. Fix the "rare" note with 6.3/3.2/2.8%.
   - tenure artefact (LEAK-10/13): <= 0.0005 (task gamer). Fix: tenure 0 for January hires, or clip them to [0, 1].
   - age: the fact is disputed. The claim auditor's linkage shows +1 year for 96.5-98.1% of 430,953 leavers in every
     month. The column auditor's apprentice test says age is read at the separation. Facts first (EV-1): the mediator
     settles it. Worst case +0.0006: harmonise in `_clean` (LEAK-6, LEAK-7), or age leaves under point 4.
   - Writing slips (code 24 median age 38; hours 0/99 mostly general employees; 36,155 positives; label agreement
     99.2-99.4%): correct the numbers.
   Rule: Tensions row "a real task against a leak": fix the leak and keep the task. None of these is irreversible
   (LEAK-27).

6. Never-paid links (LEAK-25): a clearly unrecorded part exists. The rest is a weighing call, not a Must failure.
   Concession: the armed forces (category 314) record 3 separations in 418,633 links in 2025, against 254 in 12,651
   sampled in 2024. That is "not recorded", the same fact as the abandoned links. Fix without a decision: drop
   category 314 (0.7%), and rewrite the accepted-warning reason for legal nature 1015.
   Dispute for the wider 9.6%: LEAK-25 is about a No that means "never recorded". These links do record outcomes:
   separation 5.7% (claim auditor), 7.2% among CLT employees. 25% of the CLT group have leave days, and staff on long
   benefit leave are people an HR team holds and scores. The column auditor, who measured the same group, leans
   "keep with a note" and says it is "not settleable without the ministry's rules". If the curator wants a filter,
   pay_january > 0 is label-free and known on 1 February (option b): it keeps the dataset.

7. Population, metric and codes are weighing and quality calls, not validity failures.
   - 20% public servants and military (practitioner): the census population, already named in fit_reason as pooled
     (USE-8, approximate fit). Restricting it to CLT employees is a USE-5 framing choice, open to the curator either
     way. It changes the level of the AUC (0.792 to 0.747), not whether the task is honest.
   - Metric: roc_auc is MET-8's binary fallback. The case for log_loss is MET-10 diversity (Weigh), and no source
     metric exists (claim auditor 35).
   - Codes as codes (CLEAN-12, P7 Should): keep them with the right reason, that the release's 2020 codebook lacks
     6.4% of the CBO rows and 11.8% of the legal-nature rows; or decode from the current tables. Rule: Tensions row
     "a real task against imperfect cleaning": keep the task, fix what is cheap. Decoding the municipality
     ("UF-Name [code]") is cheap.

Judgment record (advocate's reading):
  Verdict: ship after changes (points 3, 5 and 6's category 314 need no decision; points 4, 6 and 7 are the curator's
    calls, and the dataset ships under every option).
  Validity: SEL-1 open, fixable by dropping columns; USE-1 holds (approximate); LEAK-10 triggered twice, small, fixed in
    the definition; LEAK-25 partly triggered (314), fixed; SPLIT-8 applied, cost -0.0057.
  Value: TP no flags; spread dummy 0.5 / linear 0.780 / GBM 0.797-0.799.
  Quality: CLEAN-12 departure, reason to be restated; CLEAN-11 negative pay (1,041 rows), set to missing.

</details>

<details><summary>Advocate rebuttal</summary>

ADVOCATE REBUTTAL: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-09

The critic and I agree that nothing here excludes the dataset. We differ on two points: how far the LEAK-25 filter
should reach (critic 2), and whether the pooled population is a Must failure or a call the curator weighs (critic 5).

C1 Protected grounds: CONCEDE. No fact sets this case apart from the Tensions row's reasoning, and the law lists age
   with the others. What follows: drop all five, recorded as an amendment of the row's scope (decisions on employees).
   Keeping age needs a stated fact, and I have none. This also makes the age question moot (C4). Cost 0.006-0.007.

C2 Unrecorded outcomes: CONCEDE category 314 (3 separations in 418,633 links in 2025, 254 of 12,651 sampled in 2024: a
   recording change). Drop it and rewrite decision 4 and the 1015 warning text. DISPUTE that pay_january == 0 is the
   rule LEAK-25 requires.
   - LEAK-25 removes rows whose No means "never recorded". The wider group does record outcomes: separation 5.7% (CA),
     7.2% among CLT employees.
   - 25% of the never-paid CLT links have leave days. A suspended contract on benefit leave is a reason for fewer
     separations, not for unrecorded ones.
   - The January-pay rule also drops 1.27M links that are paid later in the year (quit 6.1%). Those are real staff.
   - The column auditor measured the same group and called it "not settleable without the ministry's rules".
   - The +0.015 is easy negatives. It is a leak only if their No is false, and that is shown only for 314.
   So: 314 out without a decision. Whether to filter the rest (pay_january > 0, or the all-year rule) is the
   curator's call, with the numbers in the note. Remedy ladder: the mildest fix that resolves the shown part.

C3 Contract type: CONCEDE (LEAK-10, LEAK-6). For tenure <= 3, merge 60/65/70/75 into 10/15/20/25, and rewrite the
   note with 6.3/3.2/2.8%. I agree to check worker_category for the same conversion (apprentice, fixed-term) before
   shipping.

C4 Tenure: CONCEDE. Set tenure to 0 for January hires, use floor or the measured offset, normalise -0.0, and correct
   the note. Age: AGREE that the mediator settles the fact (EV-1). It is moot under C1.

C5 Population and target: DISPUTE that this is a Must failure; CONCEDE the writing.
   - USE-8 lets an approximate fit stand when the gap is named. fit_reason already says "employers are pooled".
     Mildest remedy: name the 20% public servants and military there, give the CLT-only AUC (0.747), and say roc_auc
     ranks pooled links (MET-1 note).
   - Pooled data has a real user: the domain practitioner's own second actor, a payroll vendor's pooled cold-start
     model, which would score its clients' whole staff.
   - So restricting to categories 101-111 is a framing choice the curator weighs (USE-5), not a fix that a Must
     forces. It changes the AUC level (0.792 to 0.747); no measurement shows it changes the order of models.
   - Code 90: CONCEDE that the citation is wrong. Cite USE-5, not LEAK-22. The call itself (Yes or No) has no
     precedent and goes to the curator. Name fake-layoff agreements as label noise.

C6 Split notes: CONCEDE, as in my point 3. Use the shipped-fold numbers and the cell-sharing measurement, give the
   series break as the reason, and say "revisit when the post-2023 stretch holds six base years".

C7 Cleaning and slips: CONCEDE.
   - Restate the CLEAN-12 reason as the outdated codebook, or decode to "words [code]", decided alike for sinan.
   - Set negative pay_january to missing (CLEAN-11).
   - Correct the five numbers.

Net: ship after changes.
- Fixes in the definition that need no decision: C3, C4 (tenure), 314 in C2, C6 and C7's numbers.
- Calls for the curator: C1 (I accept dropping all five), the wider filter in C2, the population and code 90 in C5,
  and the CLEAN-12 option in C7.

</details>

<details><summary>Critic</summary>

CRITIC, OPENING BRIEF: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-09

Verdict asked for: ship only after changes. The task is real (USE-1 holds, approximate), so nothing here asks for
exclusion: points 1-4 are Musts that the definition can fix, 5 is a Must on how the fit and target are written, and
6-7 are notes and quality. The definition as it stands ships one P1 concern and three confirmed P4 leaks/biases.

Sources: dataset.py and README.md (df-large), principles.md; panel reports claim_auditor (CA), column_auditor (CoA),
split_auditor (SA), domain_practitioner (DP), blind_reviewer (BR), task_gamer (TG), precedent_checker (PC); builder
report.

1. Protected grounds as inputs of an employer's retention score (P1, SEL-1 Must; Tensions row "a factor the actor may
   no longer use", USE-1/USE-6)
   Problem: sex, race, age, nationality and disability_type are features of a score whose stated use is an HR team
   deciding "whom to offer retention measures (a raise, a talk, a training plan)" (task_summary.use_case).
   Effect on the task: the benchmark rewards a model the named actor may not lawfully deploy. Lei 9.029/1995 art. 1
   (as amended 2015, in force in 2025) bars "qualquer pratica discriminatoria ... para efeito de acesso a relacao de
   trabalho, ou de sua manutencao" by sex, origem, raca, cor, deficiencia, idade (text read on the Camara site by the
   builder, CA claim 36, CoA A, DP 4). The use case is "manutencao", and a raise is pay (CF art. 7 XXX).
   Evidence of cost: four grounds other than age carry <= 0.001 ROC AUC (CoA, 3 seeds: -0.0001 to -0.0008; DP fold 0:
   0.7917 -> 0.7916); all five cost 0.006-0.007 (CoA -0.0059 to -0.0065; DP 0.7917 -> 0.7845).
   Precedent (PC D1): bemtpl97 and four insurance tasks dropped sex on "the actor's legal constraint today", even
   where the actor's law allowed it. Here the actor's own law bars all five, in the data's own year, so the row's
   stop ("a use case set in the data's own time") does not apply. No fact recorded sets this case apart. The builder's
   option (b) (sex and race only) follows neither the insurance stance nor the legal reasoning.
   Remedy (fix the definition): drop all five; record it as the Tensions row extended to decisions on employees
   (an amendment, as the row's scope names pricing). This also settles the disputed age reference date (point 4).
   If the curator keeps age, that is an exception that needs a stated fact; none has been offered.

2. Unrecorded outcomes labelled No (P4, LEAK-25 Must; P3 USE-5)
   Problem: the definition drops the source's abandoned flag (1.2%) as "outcome not recorded" but keeps a far larger
   group with the same pay pattern.
   Evidence: CA, all 2025 files: 5,561,852 non-abandoned cohort links (9.6%) have no pay in any month; separation
   5.7% vs 30.0%, quit 0.92% vs 7.96%. Armed forces (category 314): 418,633 links, 3 separations in all of 2025, vs
   254 of 12,651 sample links in 2024; zero January pay 85.2% in 2025 vs 3.3% in 2024. That is a recording change,
   not behaviour. CoA D: 8.4% never paid and no leave day, quit 0.98%. Effect: these rows are easy negatives worth
   +0.015 ROC AUC (0.797 vs 0.782 scored without them, 3 of 3 folds, CA).
   The proposed accepted warning ("legal 1015 ... almost never resign: a category effect of tenured public
   employment") is refuted for the armed forces (CA AW).
   Rule: LEAK-25 as amended 2026-10-21: unrecorded rows located by a rule that does not read the label are dropped
   (caracas, account_debt_south_africa, fraud_detection_..._1m, which located by a later date). PC D4: keeping them
   departs from those precedents with no fact recorded.
   Remedy (filter): at least drop worker category 314 (0.7%, decisive evidence). Preferred: drop links with
   pay_january == 0 (11.8%), a rule known at the prediction point that matches "after the January payroll, scores its
   staff"; or the all-year zero-pay rule (9.6%). Rewrite decision 4 and the accepted-warning text accordingly.
   The cost (some staff on long leave go too; 25% of never-paid CLT links have leave days, CoA D) goes in the note.

3. Contract type is the year's last value and marks the outcome for recent hires (P4, LEAK-10 Must; LEAK-6 Must)
   Problem: an experience contract (CLT fixed term, 60) that survives is converted to open-ended (10), so "fixed term"
   for a recent hire means "left before conversion".
   Evidence (CA claim 28): January hires on 60 are 98.9% separated (96.6% by April), on 10 45.5%; hires of Nov-Dec
   2024 on 60: 97.0% separated. Contract changed for 9.9% of quitters vs 4.7% of other leavers, mostly 60 -> 10.
   Merging 60/65/70/75 into 10/15/20/25 drops January-hire ROC AUC 0.7666 -> 0.7491 (-0.0175, 3 of 3 folds), -0.0011
   overall. The note "such changes are rare" is refuted (yearly change among stayers: CBO 6.3%, hours 3.2%,
   contract 2.8%).
   Rule: LEAK-10 (a value recorded after the outcome), LEAK-6 ("a confirmed leak goes even when small"; santander
   +0.003). The leak is located (tenure <= 3), so LEAK-7's smallest fix applies, as zillow_prize/melbourne did.
   Remedy (fix the definition): for links with tenure_months <= 3, merge the four CLT fixed-term levels into their
   open-ended twins (or merge everywhere, -0.001 overall). Rewrite the "Potential leak, kept on purpose" note with
   the measured change rates; check worker_category the same way (apprentice, fixed-term categories, TG "could not
   check").

4. Tenure rebuild marks the class for January hires; age's reference date disputed (P4, LEAK-10/LEAK-13 Must, weak;
   LEAK-6; EV-1)
   Tenure evidence: a January hire has < 1 month on 1 February, yet tenure_months = 2 occurs only for leavers (1,367
   of 1,975,519 rows, 100% separated, CoA C; BR 118 in its 200k sample; TG 0/1/2 quit rates 0.212/0.121/0.037,
   single-feature AUC 0.585 within the group; CA 0.590). The half-month guess is biased (measured separation-day
   fraction 0.34 for quits, 0.42 all leavers, CA). Gain small (<= 0.0005, TG; ~0, CA), but it is a pure
   separated-not-quit marker and it is confirmed. BR also found 586 rows with tenure -0.0 (positive rate 44%).
   Remedy: set tenure_months to 0 (or clip to [0, 1]) where admission_month == 1, before the drop; use floor or the
   measured offset instead of round-half-even; normalise -0.0; correct the note.
   Age: CoA's apprentice test says leavers' age stops at the separation (+0.0006 ROC AUC full model, 3 of 3 seeds);
   CA's linkage of 430,953 leavers says one fixed date (diff +1 in 96.5-98.1% every month). Facts first (EV-1): the
   mediator settles it. Either way "cannot verify" cannot stay (PC D3): confirmed -> harmonise or drop; refuted ->
   the note gives the measurement. Moot if point 1 drops age.

5. Population and target written as a fit the use case does not have (P3, USE-5 Must, USE-8 Must; MET-1 Must)
   Population: 20.0% of fold-0 test rows are statutory/public servants and military (quit 1.2% vs 8.6% private CLT),
   whom no private HR retention model scores and public bodies do not offer individual retention (DP 3a; BR 7). They
   inflate the pooled ROC AUC: 0.792 pooled, 0.747 private "Employee, general" or CLT only, 0.727 within
   sector x municipality cells (DP). The pure-feature-value warning is the same fact.
   Target: code 90 (agreement, art. 484-A, 6,488 sample links, ~4.5% of the Yes count) is counted No with LEAK-22 as
   the reason; LEAK-22 says how a competing event is labelled, not whether an agreement is the actor's event (USE-5,
   PC D4). DP (actor): usually employee-initiated, the departure retention targets.
   Remedy: preferred, restrict the cohort to private employee categories 101-111 (rows remain plentiful); mildest,
   name the pooled population in fit_reason as a selection the setting does not share (USE-8) with the CLT-only AUC,
   and say roc_auc ranks pooled links, not an employer's staff (MET-1). Decide code 90 under USE-5 and cite it; name
   fake-layoff agreements (quits recorded as code 11) as known label noise.

6. Split notes misstate the cost and the reason (P4, SPLIT-8, SPLIT-20 Should; writing)
   - The cost is attributed to "the three test folds of 2025" but came from the builder's own StratifiedKFold; on
     the shipped folds it is 0.7971 vs 0.7915 (+0.0057, 3 of 3) (SA 2; CA 33).
   - SA measured that +0.004 to +0.005 of it is the year's own quits shared within sector x municipality x
     legal-form cells across the random folds; memorising learners gain twice as much (+0.010 vs +0.005), no
     ranking change among 5 learners. The note only speculates about it.
   - The reason for one year is a download count ("we downloaded two"; "ship yearly windows if more years are
     downloaded"). The real fact is the 2022/2023 eSocial series break (SPLIT-20; SA 1, PC D2): chile_school_dropout
     downloaded seven years and shipped temporal, so a download count would not set RAIS apart.
   Remedy (notes): shipped-fold numbers, the cell-sharing measurement, the series break as the reason, "revisit when
   the post-2023 stretch holds six base years".

7. Cleaning and factual slips (P7, CLEAN-12 Should, CLEAN-11 Should; writing) -- quality only, no reason to exclude
   - CBO, CNAE subclass/class, legal nature, municipality ship as codes; the stated reason ("digits carry the
     hierarchy") is a modelling argument a categorical model never sees (CoA E; BR 4: native categoricals 0.769 vs
     integers 0.797). Current official tables exist; the 2020 layout names every municipality but one. Remedy: decode
     to "words [code]" (ny_wcb form), or record an exception whose fact is the outdated 2020 codebook, decided alike
     for sinan_dengue's CBO/municipality (PC D5).
   - pay_january negative in 1,041 rows (quit 14.6%, 2x base): set missing or note (CoA F).
   - Numbers to correct (CA 4): code 24 median age 38 not 26; hours 0/99 are 74% general employees, not "mostly
     intermittent"; CNAE 95 99999 in 201,575 Norte rows; test folds hold ~36,155 positives, not 14,390; exact copies
     agree on the label 99.2-99.4%, not "all".

</details>

<details><summary>Critic rebuttal</summary>

CRITIC REBUTTAL: rais_employment_separation (folder rais_employment_separation_1m), 2026-11-09

Against the advocate's opening brief, point by point. We agree on the verdict (ship after changes, no exclusion). Two
disputes remain: which rows the LEAK-25 filter covers (A6) and whether the population is only a matter of wording (A7).

A1 Real, unique, worth benchmarking: CONCEDE. SEL-16, PROV-3 and USE-1 (approximate) hold; no task-probe flags. I
   never argued exclusion.

A2 "The core is honest, no exploit worth more than 0.001": CONCEDE the task gamer's numbers; DISPUTE the reading.
   The exploits measure what a participant can add on top of the shipped features. They do not test leaks already
   inside those features. The contract-type conversion is such a leak: +0.0175 ROC AUC on January hires, 3 of 3
   folds (CA 28), and the gamer listed it as "could not check". So "every post-outcome field is dropped" is not yet
   true. contract_type, and perhaps worker_category, carry values recorded after 1 February. This is fixed in A5, so
   the dispute changes the record, not the verdict.

A3 Forced IID: CONCEDE. SPLIT-8 is applied correctly; the fixes are the notes in my point 6.

A4 Protected grounds: CONCEDE that the remedy is to drop the columns, not to exclude. DISPUTE "every option ships" as
   written. SEL-1 is a P1 Must. A fixable Must is fixed (principles.md, Strengths; remedy ladder), and a Must has no
   exceptions. Options (a) keep all five and (b) drop sex and race only would therefore need an amendment of the rule
   with a stated fact (Consistent judgement, case 1). None has been offered (PC D1). The advocate's own rebuttal
   (C1) accepts dropping all five, so we agree on the outcome.

A5 Small leaks fixed in the definition: CONCEDE on all points. They are Musts (LEAK-10, LEAK-6), not optional
   polish. The worker_category check must happen before shipping, not after (TG flags apprentice 0.24 and
   fixed-term 0.29 quit rates as possibly post-outcome).

A6 Never-paid links: CONCEDE category 314 as decided. CONCEDE in part on the wider group:
   - Staff on leave belong to the use case (25% of never-paid CLT links have leave days).
   - The January-pay rule also drops 1.27M links paid later in the year.
   - A 5.7% separation rate shows that some of these links do record an outcome.
   So I withdraw pay_january == 0 as the required rule. I hold a narrower filter under LEAK-25 (Must):
   - Drop links with no pay in any month in post and no leave day in the year: 8.4% of the cohort, quit 0.98%,
     any separation 6.0% against 27.5% (CoA D). Among general CLT employees this group is 4.5%, quit 1.1% (CoA D).
   - A working employee with no pay and no leave for a whole year is the source's own definition of an abandoned
     link (no pay in January and December, no separation), only without the flag. Decision 4 already drops the
     flagged 1.2% for exactly this reason.
   - The rule reads later pay and leave but not the label. fraud_detection_..._1m located its rows by a later date
     (LEAK-25 Cases), so this is allowed.
   - It keeps both groups the advocate defends: staff on leave and links paid later in the year.
   - Keeping the whole group is a departure from the LEAK-25 precedents with no fact recorded (PC D4). If the curator
     keeps it, the note must say so and give the +0.015.

A7 Population, metric, codes:
   - Population: DISPUTE that fit_reason already names it. It says "employers are pooled", which does not name the
     20% of rows that are statutory servants and military (quit 1.2%), nor their effect on the score (0.792 pooled vs
     0.747 private CLT, DP 3a). USE-8 (Must) asks for the fit to be written, so the note is required. The vendor actor
     does not cover these rows: DP's vendor serves "many small employers", and DP says no private HR team scores
     tenured servants or the armed forces. CONCEDE that no measurement shows a change in model order, and that a
     named gap keeps the fit approximate (USE-8). Filtering to categories 101-111 stays my preferred remedy; the note
     is the minimum.
   - Metric: CONCEDE. roc_auc is MET-8's fallback, kept with the note that it ranks pooled links (MET-1).
   - Codes: CONCEDE that this is a P7 call. Restate the reason as the outdated 2020 codebook, or decode to
     "words [code]", decided the same way for sinan. Decoding the municipality is cheap.

Net: ship after changes.
- Needs no decision: drop the five protected grounds (A4/C1, agreed); drop category 314; contract_type merge for
  tenure <= 3; tenure fix for January hires; check worker_category; split notes; numbers; negative pay to missing.
- For the curator: the never-paid-and-no-leave filter (my ask, LEAK-25) or a recorded departure; restricting to
  private categories or naming the population (USE-8 note at minimum); code 90 under USE-5; the CLEAN-12 option.

</details>
