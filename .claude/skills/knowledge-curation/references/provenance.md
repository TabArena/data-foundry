# Sources, duplicates and evidence

Part 5 of the curation rules, under P5 (Faithful, unique data) in [principles.md](principles.md). The rules of earlier
parts win over this file's rules in a conflict; within this file a rule wins over the rules below it of the same
strength. How to weigh, exceptions and amendments: [principles.md](principles.md).

Where a dataset first came from, whether it is a duplicate, how to cite the evidence, and how to tell whether the
data is real. Whether generated data is in scope is decided by SEL-16 in [selection.md](selection.md); how to detect it
is here (PROV-3).

## Rules

### Known and real data

**PROV-1 (Must).** The data comes from a known source, so we can tell what it is. A working download link is not a
known source: when following every link ends at an anonymous re-upload with no documentation and no traceable upstream
(paper, competition, institution, an identifiable first uploader), the origin is unknown. A dataset that still lacks
the information needed to decide after a thorough search is `No`, and that is the curation team's call; only the end
of a search counts ([selection.md](selection.md), "Unknown or unclear source"). PROV-2 keeps, case by case, a sound
upload whose first platform cannot be traced but that has a source to point to (amended 2026-10-21, Lennart). Marker:
`Missing source information`. Cases: water_quality_and_potability, 3d_estimation_using_rssi_of_wlan_dataset_complete_1_target, calendardow.

**PROV-2 (Should; narrows PROV-1).** A source that is plausible but unclear in a detail stays, with a note of what to
clarify. A bare record of a known origin (a link, no description) is no lack of information either. An upload whose
first platform cannot be traced is kept for now, case by case, when the data looks sound (it passes PROV-3) and there
is a source to point to: the first upload, or a named course or teaching platform. The gap is written as an
approximate fit (USE-8) with a note of what is unknown, and the risk is taken knowingly (Lennart, 2026-10-21: "if the
data looks good enough even without a good source but there is a source, we want to keep it for now and risk it";
this widens the amendment of the same day for a named platform). Cases: bad_customer_detection (Lennart, 2026-10-14),
tour_travels_churn, mobile_churn, credit_card_customers, bank_customer_churn.

**PROV-3 (Must).** The data is real: not generated, and not a real table someone reworked (relabelled, columns
renamed, values replaced). A table that looks clean and scores well can still be either. Generated data is `No`; the
scope rule is SEL-16 in [selection.md](selection.md), the detection is the seven tests under Methods, "Is the data
generated?". Marker: `AHDS`, usually with `Missing source information`, and `Data Quality Issue` when a real
table was manipulated. Values the data owner perturbed for privacy (disclosure control on a real cohort) are no
rework when no test under Methods measures damage: the data stays, with a note saying what was checked and what cannot
be (Lennart, 2026-10-21; framingham_heart_study_fhs). Without a source statement or a generator, measured marks are
judged case by case: either calibrated marks from at least two of the tests under Methods, or marks linked to the label
(test 5 or 7), can be strong enough. The marks count on the columns we ship; marks found on the file as published
count when they extend to the shipped version, which is again case by case (amended 2026-10-21, Lennart: "either
might be strong enough; on the columns we ship, and if the marks on the published file leak/extend to the shipped
version (which is again case-by-case)"; prompted by credit_card_customers, stroke_prediction and hepatitis_c_egypt).
Cases: customer_satisfaction_in_airline, ecommerce_shipping, homeq_default_prediction, video_game_fps_prediction,
framingham_heart_study_fhs.

### Duplicates

**PROV-4 (Must).** A dataset enters once: two records that end at the same original source are duplicates, even when
their direct links differ. The reliable signal is the original source, not the data layout: two uploads of one
dataset can look very different (column names, dtypes, row counts, preprocessing), and similar-looking tables can be
different datasets. Test: trace each candidate back to where the data first came from rather than diffing tables
(Methods, "Tracing a duplicate"). Marker: `Duplicate`.

**PROV-5 (Must).** Confirm the source before marking a duplicate. Cases: colleges (Lennart, 2026-10-12).

**PROV-6 (Must).** Different versions or cuts of one underlying dataset are duplicates too when neither adds a
distinct task: a swapped target, another slice of the same cohort, added or dropped rows or columns. Marker:
`Duplicate`. Cases: arsenic_male_lung.

**PROV-7 (Must; narrows PROV-4 and PROV-6).** Records that share a source but give different tasks are not
duplicates. The comments say why they are distinct, ideally each with its own DOI. Cases:
parkinsons_biomedical_voice_measurements, amex_iid.

### The source is the first publication

**PROV-8 (Must).** The source of a dataset is where it was first published: the competition, the paper or its
supplement, the institution's release, the first upload. A Kaggle, OpenML, UCI or Hugging Face re-upload of a
government survey, a paper's repository or a company release takes the original's source. Kaggle is the source only
when the data first appeared there or no other source can be found (Lennart, 2026-10-12). Where we download the files
can differ from the source: the download instructions name the copy, and say which original it copies.

**PROV-9 (Must).** The year is the year of that first publication: a competition's launch, a dataset's release (UCI's
"donated on", a Kaggle dataset's first version), the online date of the paper or supplement that holds the rows, the
first commit that shares them. A figure that shows every measured value holds the rows, together with the columns
the publication's own formulas compute from them: a file digitised from it later is a copy, and takes the figure's
publication as its source and year. Not the collection period, not the year of a paper
that only analysed the data, not the BibTeX year of a later citation, not the date of the copy we download (Lennart,
2026-10-12 and 2026-10-14; figures: Lennart, 2026-10-20, airfoil_self_noise). A source that grows over time (a public
register, a scraped site, a monthly archive) takes the year of the snapshot we pin.

**PROV-10 (Must).** The citation is the work that published the data, not a paper that used it.

**PROV-11 (Must).** A dataset we rebuild from other sources has those as its origin, not the file it replaces. Cases:
corporate_issuer_credit_rating (Lennart, 2026-10-16).

**PROV-12 (Must).** Links to related work (another competition on similar data, a paper that used it) are not
sources; they go into the comments. Cases: nyc_taxi_trip_duration, melbourne_housing_market (moved 2026-10-12).

### Repair or rebuild before keeping damaged data

**PROV-13 (Must).** When a release is damaged (rows of another patient, units mixed across sites, values scaled over
all rows, labels taken from the wrong rating), check whether the origin has the clean data before keeping the damage
or retiring the dataset, and repair or rebuild from the origin when it has them. Scaling over all rows is a weak leak:
LEAK-30 in [leak_checks.md](leak_checks.md). Cases: SUPPORT2, ashrae, coad_colon_adenocarcinoma,
corporate_credit_rating.

**PROV-14 (Must).** A repair stays under its record: the same units and the same features, with the damaged values
restored from the origin (PROV-13), even when the table then differs from the release. Only a rebuild from other
sources (new data, new units or new columns, PROV-11) is a new dataset with its own record (Lennart, 2026-10-21;
framingham_heart_study_fhs). Cases: SUPPORT2 (2_month_survival_rate_prediction), cirrhosis_patient_survival_prediction,
framingham_heart_study_fhs (repairs); corporate_credit_rating, rebuilt as corporate_issuer_credit_rating.

### Problems of third-party copies

**PROV-15 (Must).** Copies on OpenML, Kaggle or in other benchmarks often carry their own errors. Note such a problem
in the record of the dataset it concerns, as a problem of that copy, so it can be reported to the maintainers later.
Raise it as an issue only when it changes one of our decisions. Another collection's version of the data, pretraining
overlap and other benchmarks' scores never do: they are no evidence ([evidence.md](evidence.md), EV-4). Name another
collection's version only for provenance or a duplicate. Cases: OpenML 43838, SUPPORT2, OpenML 46372.

### Citing papers

**PROV-16 (Must).** Any claim attributed to a paper comes with a text reference: the section, table or page, and the
load-bearing sentence quoted, from text you read (not the title, the abstract or a recollection of the field). Write
it as `Sec. 6.1, p. 12: "..."`. A dataset's paper is often the decisive evidence, and the reference lets the next
curator check it in one step. It prevents two real traps: a paper can refute the claim you were about to make, and a
paper's own framing can decide the verdict. Cases: kddcup99, intrusion_detection.

**PROV-17 (Must).** When a paywalled paper turns out to matter and no free copy turns up (Methods, "Finding a paper's
text"), ask the curator for the PDF. If you go on without it, say so and mark the claim as unverified rather than
paraphrasing the abstract as if it were the text.

### Competition pages are claims

**PROV-18 (Must).** A competition or dataset page is a claim about the data; the discussion threads and the public
notebooks are where the problems surface. Before triaging anything from Kaggle or a similar platform, skim both (by
votes), and write what you find with the thread or notebook link. What to look for: Methods, "Reading a
competition's threads and notebooks". Cases: pkdd-15-taxi-trip-time-prediction-ii.

## Weighed factors

* **Clear provenance** (+): clear provenance is a strong sign of a good dataset (PROV-1).

## Patterns

Quick ways to apply the rules; a pattern never overrides a rule, and the dataset at hand wins over the pattern.

* Duplicates can have a very different structure but almost always share the source. A structural diff is weak
  evidence; shared provenance is strong evidence (PROV-4).
* Suspect generated data when there is no traceable first source, a data card names only "a company" or "an airline",
  "where is this from?" threads stay unanswered, the data is course or competition material, scores look too good (F1
  0.97 on a survey), or distributions look too even. Then run the tests under Methods, "Is the data generated?"
  (PROV-3).

## Methods

### Tracing a duplicate

Trace each candidate back to where the data first came from (PROV-4):

* Compare all links of the candidate records: OpenML ids, Kaggle pages, UCI or DOI, GitHub, the paper. Overlap in any
  canonical link is a strong signal.
* Follow each link to its origin. A Kaggle or OpenML page usually references an upstream source (a paper, a UCI
  entry, an earlier uploader); two records that end at the same source are duplicates even when their direct links
  differ.
* Spot-check by name and rough field structure against datasets you know, to recognise a re-upload under a new name
  and to rule out a false match.

### Is the data generated?

The detection for PROV-3. Run these tests, cheapest first, on the earliest version you can find:

1. Trace the uploads and compare every version. Download each upload in the chain, every file of each, match the rows
   by id or by columns that should stay fixed, and list what changed. For changed labels, fit a shallow tree on the
   original features to see whether a rule picked the changed rows. customer_satisfaction_in_airline: one upload holds
   two files with the same 129,880 ids; in the derived file 8 of 14 rating columns sit under the wrong name, distances
   were replaced, and 14,659 labels were flipped one way by a rule (Female, Personal Travel, wifi at most 3, delay at
   most 130 min) that uses a column the shipped file then drops.
2. Look for row-counter patterns. Sort by the id or the file order, cross-tabulate each categorical column against the
   id modulo k for k up to a few hundred, look at run lengths and at the target rate in blocks of ids.
   ecommerce_shipping: `Warehouse_block` is the id modulo 6 and `Mode_of_Shipment` a 137-id cycle, with no exception
   in 10,999 rows; the target is 100% one class for the first 3,135 ids.
3. Look for copied columns: for every pair of columns on one scale, the share of rows with equal values, overall and
   within each segment. More than about 90% agreement between unrelated items is a copy rule (the airline file: wifi
   equals gate location in 95% of one segment's 39,191 rows). A real survey stays well below (the Brazilian airport
   surveys never exceed 68%, even for near-synonyms).
4. Look for marginals that are too even: categories with identical counts (1,833 rows per warehouse block), ratings
   spread evenly over 1-5 inside a "satisfied" class.
5. Look for class-conditional generation: a correlation between two features that differs strongly by class or
   changes sign, a label-free nearest-neighbour distance that predicts the label, number formats that differ by class
   (homeq_default_prediction: near-copy clusters pure in the label, distance alone AUC 0.92).
6. Look for structure the world would show: units that ought to cluster (passengers of one flight), physical
   constraints (arrival delay against departure delay), impossible combinations (children on business trips), known
   reference values. This also shows which parts are real: the airline distances spike on actual route lengths (337 mi
   LAX-SFO, 2,475 mi JFK-LAX), so only the passenger part is synthetic.
7. Look for a deterministic target: a near-perfect fit from a simple formula or lookup is `Trivial` and often `AHDS`
   (video_game_fps_prediction: log FPS = game + CPU + GPU, R^2 0.99998).

Calibrate before concluding: run the same statistic on a real dataset of the same kind, since a selection on the label
also changes correlations. Report which columns look real and which look generated, with the decisive test first.
When you can, write the generator down: that settles it. The automated marks of generated data and their calibration
are in [task_probes.md](task_probes.md), "Generated data".

### Finding a paper's text

When the publisher's copy is paywalled, spend a short search on a free copy (PROV-17): Unpaywall, Europe PMC, arXiv,
Semantic Scholar, the authors' or institution's pages, and a web search for the exact title in quotes plus "pdf" (with
and without the quotes, and with the first author's name). Copies often sit on PDF mirrors (ResearchGate, SciSpace,
oa.mg, CORE, Academia.edu). When nothing turns up or a mirror cannot be fetched, ask the curator for the PDF as soon
as the paper turns out to matter, with the exact query (a Google search for the title plus "pdf" usually finds it).

### Reading a competition's threads and notebooks

Skim the discussion threads and the public notebooks by votes (PROV-18) for leak threads and "hack" baselines (a
trivial rule that scores near the top), disputes about the test set (random or temporal, ground truth recoverable from
a public upstream), duplicated or mislabelled rows, a column that is the target in disguise, and the uploader's answers
about where the data came from.

## Cases

Precedents: how a rule was applied. They never change a rule; an exception is listed with the fact that set it apart.

| Rule | Dataset | Decision (date, curator) | Kind |
|---|---|---|---|
| PROV-1 | water_quality_and_potability, 3d_estimation_using_rssi_of_wlan_dataset_complete_1_target, calendardow | every link ends at an anonymous re-upload: `Missing source information`, `No` ([selection.md](selection.md), "Unknown or unclear source"). water_quality_and_potability was rejected in the v1 workbook for the source alone (the curator then judged its features free of group or time structure), with no PROV-3 test on record; under PROV-2 as amended (2026-10-21) no recorded fact sets it apart from mobile_churn, so it is due a re-check; re-checked 2026-10-21: the first upload (adityakadiwal, 2021) calls itself "Synthetically generated" and TDS is about 50 times the conductivity, so the AI recommends keeping `No` with `AHDS`; open in its record | applied |
| PROV-2 | bad_customer_detection | a plausible source unclear in a detail: kept, with a note of what to clarify (2026-10-14, Lennart) | applied |
| PROV-2 | credit_card_customers, bank_customer_churn | a named first platform (Analyttica's LEAPS teaching case 11, offline; a named data-science course) counts as a known source when the data shows no PROV-3 marks; PROV-2 amended (2026-10-21, Lennart). credit_card_customers stays open on whether its measured marks count (its issue 1) | applied |
| PROV-2 | tour_travels_churn | a bare Kaggle upload with no named origin, kept for now: the data passes PROV-3 and the upload is the source to point to; the gap is in the approximate fit (2026-10-21, Lennart; PROV-2 amended) | applied |
| PROV-2 | mobile_churn | every link ends at an anonymous Kaggle upload (2019, empty description); no PROV-3 flag and the data look like a system export: kept, with the unknown operator and churn rule in the approximate fit (2026-10-21, Lennart; PROV-2 amended) | applied |
| PROV-2 | credit_card_customers, bank_customer_churn | covered by the wider amendment as well (a named platform is a source to point to); credit_card_customers' keep still depends on its PROV-3 question (its issue 1) (2026-10-21, Lennart) | applied |
| PROV-3 | customer_satisfaction_in_airline | tests 1, 3 and 6: a derived file with rating columns under the wrong name, replaced distances and 14,659 labels flipped by a rule; the passenger part is synthetic, the route distances real; retired | applied |
| PROV-3 | ecommerce_shipping | tests 2 and 4: `Warehouse_block` is the id modulo 6, `Mode_of_Shipment` a 137-id cycle, 1,833 rows per warehouse block; retired | applied |
| PROV-3 | homeq_default_prediction | test 5: near-copy clusters pure in the label, distance alone AUC 0.92; retired | applied |
| PROV-3 | video_game_fps_prediction | test 7: log FPS = game + CPU + GPU, R^2 0.99998, `Trivial` and often `AHDS`; retired | applied |
| PROV-3 | framingham_heart_study_fhs | BioLINCC's teaching data, anonymised by undocumented methods ("permutations and/or random visit selection", Nahhas, App. A.6): no test fires (digit preference intact, systolic BP ends in 0 for 22.5% of readings; within-person r 0.90 and 0.71 six years apart; per-sex baseline tables match the documentation); kept with a note of what was checked; PROV-3 amended (2026-10-21, Lennart). stroke_prediction may be a second case (about 1,029 more patients aged 78 to 82 than the trend gives); not decided | applied |
| PROV-4, PROV-5 | colleges (OpenML 42727) | marked a duplicate of college_scorecard only after its named original (a Colleges.txt file, still online) proved to be the College Scorecard file of 2013-14: all 7,804 institution ids in it, and faculty salary, size and admission rate agreeing for 97-99% of the colleges (2026-10-12; Lennart asked for that check) | applied |
| PROV-6 | arsenic_male_lung | the lung-cancer version of the same exposure data as arsenic_male_bladder: a duplicate ([selection.md](selection.md), "Duplicates and versions") | applied |
| PROV-7 | parkinsons_biomedical_voice_measurements, telemonitoring_parkinsons_biomedical_voice_measurements | one source, two tasks: the first detects a disorder, the second tracks its progression ([selection.md](selection.md), "Duplicates and versions") | applied |
| PROV-7 | amex_iid, amex_non_iid | the IID and grouped versions of one competition ([selection.md](selection.md), "Duplicates and versions") | applied |
| PROV-8, PROV-9 | airfoil_self_noise | 1989 and NASA RP-1218, not UCI 2014: the report's Figs. 11-43 show every measured value (the scaled target and the thickness are the report's formulas of them), and UCI's file was digitised from them (Lau, López and Oñate, CIMNE PI-335, Sec. 4.1), so it is a copy; the report's tables do not list the levels (2026-10-20, Lennart; PROV-9 amended) | applied |
| PROV-9 | first_principles_tully_fisher | 1977 and Tully and Fisher (A&A 54), not PMLB: its 18 rows were read off the paper's Fig. 5(a); real measurements, so not `AHDS` (2026-10-20, Lennart) | applied |
| PROV-9 | nikuradse_1, nikuradse_2 | 1933 and Nikuradse's VDI-Forschungsheft 361, not PMLB or the 1950 NACA translation: its Tables 2-8 hold the 362 measurements (2026-10-20, Lennart) | applied |
| PROV-11 | corporate_issuer_credit_rating | a rating history rebuilt from the agencies' SEC Rule 17g-7(b) disclosures and SEC EDGAR has them as its source, not the Kaggle file it replaces (2026-10-16, Lennart) | applied |
| PROV-12 | nyc_taxi_trip_duration | listed the Porto PKDD-15 competition as a source; moved to the comments (2026-10-12) | applied |
| PROV-12 | melbourne_housing_market | listed two Airbnb datasets as sources; moved to the comments (2026-10-12) | applied |
| PROV-13, PROV-15 | SUPPORT2 | the copy's phase II physiology held rows of the wrong patient; restored from the study data (ICPSR 2957) | applied |
| PROV-14 | SUPPORT2 (2_month_survival_rate_prediction), cirrhosis_patient_survival_prediction, framingham_heart_study_fhs | repairs: the same units and features, damaged values restored from the origin, kept under their records (framingham: 4,240 participants matched row for row on 15 features, 249 labels turned from Yes to No, 16 rows dropped); PROV-14 amended (2026-10-21, Lennart) | applied |
| PROV-11, PROV-14 | corporate_credit_rating | a rebuild from other sources (the agencies' rating histories, SEC EDGAR): a new record, corporate_issuer_credit_rating (2026-10-16, Lennart) | applied |
| PROV-13 | ashrae | the readings put in kWh from the data owners' raw files | applied |
| PROV-13 | coad_colon_adenocarcinoma | retired for a rebuild from the GDC's per-sample files | applied |
| PROV-13 | corporate_credit_rating | retired for a rebuild from the agencies' own rating histories | applied |
| PROV-15 | OpenML 43838 (account debt) | the label columns shipped as features: a problem of that copy | applied |
| PROV-15 | OpenML 46372 | a generated table made from the book's 197 rows, posing as real: a problem of that copy | applied |
| PROV-15, EV-4 | TabSTAR's version of a dataset | another collection's columns or labels are no reference for ours; named only for provenance or a duplicate (2026-10-15, Lennart) | applied |
| PROV-15, EV-4 | any dataset | whether a dataset is in some model's pretraining data does not change any decision (2026-10-12, Lennart) | applied |
| PROV-15, EV-4 | scores from TALENT and leaderboards | scores other benchmarks published are no evidence: their random splits are wrong for most of our tasks (2026-10-15, Lennart) | applied |
| PROV-16 | kddcup99 | the simulation-artifact critique (Mahoney & Chan, RAID 2003) looks like it condemns KDD, but Tavallaee et al. (CISDA 2009, Sec. III) state that the artifacts "do not affect the KDD data set since the 41 features used in KDD are not related to any of the weaknesses mentioned": the paper refuted the claim about to be made | applied |
| PROV-16 | intrusion_detection | the BCCC/NTLFlowLyzer paper (Shafi et al., Computers & Security 148:104160, 2025) says in Sec. 6.1 "our focus is on developing a profiling system, not a detection system", so its headline ">99.8%" is profile coverage, and the release ships no target, split or baseline: `No Good Target / Scientific Discovery` | applied |
| PROV-18 | pkdd-15-taxi-trip-time-prediction-ii (Porto, ECML/PKDD 2015) | a public snippet predicting `max((len(POLYLINE) - 1) * 15, 660)` scores well, not because test data leaks but because the test polylines are truncated prefixes of the trips (de Brebisson et al. 2015: "The testing dataset is composed of 320 partial trajectories, which were created from five snapshots taken at different timestamps"), so the elapsed time is a lower bound on the target. The competition predicts the remaining travel time from a partial trajectory, a trajectory task; only the notebooks make that visible | applied |

## In Data Foundry

The record fields for source, year and links, the `_duplicate` naming and how to note a third-party problem:
[records.md](../../knowledge-data-foundry/references/records.md). The definition's `source`, `year`, `source_url`,
`download_description` and `bibtex`: [definitions.md](../../knowledge-data-foundry/references/definitions.md). The
Kaggle command line and other access recipes:
[sources_access.md](../../knowledge-data-foundry/references/sources_access.md).
