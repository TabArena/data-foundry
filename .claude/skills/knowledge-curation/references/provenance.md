# Sources, duplicates and evidence

Where a dataset first came from, whether it is a duplicate, how to cite the evidence, and how to tell whether the
data is real. Criterion 1 of [selection.md](selection.md) rests on this file.

## The source is the first publication

The source of a dataset is where it was first published: the competition, the paper or its supplement, the
institution's release, the first upload. A Kaggle, OpenML, UCI or Hugging Face re-upload of a government survey, a
paper's repository or a company release takes the original's source. Kaggle is the source only when the data first
appeared there or no other source can be found (Lennart, 2026-10-12). Where we download the files can differ from the
source: the download instructions name the copy, and say which original it copies.

* The year is the year of that first publication: a competition's launch, a dataset's release (UCI's "donated on", a
  Kaggle dataset's first version), the online date of the paper or supplement that holds the rows, the first commit
  that shares them. Not the collection period, not the year of a paper that only analysed the data, not the BibTeX
  year of a later citation, not the date of the copy we download (Lennart, 2026-10-12 and 2026-10-14). A source that
  grows over time (a public register, a scraped site, a monthly archive) takes the year of the snapshot we pin.
* The citation is the work that published the data, not a paper that used it.
* A dataset we rebuild from other sources has those as its origin: a rating history rebuilt from the agencies' SEC
  Rule 17g-7(b) disclosures and SEC EDGAR has them as its source, not the Kaggle file it replaces
  (corporate_issuer_credit_rating; Lennart, 2026-10-16).
* Links to related work (another competition on similar data, a paper that used it) are not sources; they go into
  the comments (nyc_taxi_trip_duration listed the Porto PKDD-15 competition, melbourne_housing_market two Airbnb
  datasets; moved 2026-10-12).

A working download link is not a known source. When following every link ends at an anonymous re-upload with no
documentation and no traceable upstream, the origin is unknown ([selection.md](selection.md), "Unknown or unclear
source"). Clear provenance is a strong sign of a good dataset.

## Checking for duplicates

The reliable signal is the original source, not the data layout. Two uploads of one dataset can look very different
(column names, dtypes, row counts, preprocessing), and similar-looking tables can be different datasets. So trace each
candidate back to where the data first came from rather than diffing tables:

* Compare all links of the candidate records: OpenML ids, Kaggle pages, UCI or DOI, GitHub, the paper. Overlap in any
  canonical link is a strong signal.
* Follow each link to its origin. A Kaggle or OpenML page usually references an upstream source (a paper, a UCI
  entry, an earlier uploader); two records that end at the same source are duplicates even when their direct links
  differ.
* Spot-check by name and rough field structure against datasets you know, to recognise a re-upload under a new name
  and to rule out a false match.
* Rule of thumb: duplicates can have a very different structure but almost always share the source. A structural diff
  is weak evidence; shared provenance is strong evidence.
* Confirm the source before marking a duplicate. colleges (OpenML 42727) was marked a duplicate of college_scorecard
  only after its named original (a Colleges.txt file, still online) proved to be the College Scorecard file of
  2013-14: all 7,804 institution ids in it, and faculty salary, size and admission rate agreeing for 97-99% of the
  colleges (Lennart asked for that check, 2026-10-12).

Different versions or cuts of one underlying dataset are duplicates too when neither adds a distinct task: a swapped
target, another slice of the same cohort, added or dropped rows or columns. When two records share a source but give
different tasks, the comments say why they are distinct, ideally each with its own DOI.

## Problems of third-party copies

Copies on OpenML, Kaggle or in other benchmarks often carry their own errors: the label columns shipped as features
(OpenML 43838, account debt), rows of the wrong patient (SUPPORT2's phase II physiology, fixed from ICPSR 2957), a
generated table posing as real (OpenML 46372 from the book's 197 rows). Note such a problem in the record of the
dataset it concerns, as a problem of that copy, so it can be reported to the maintainers later. Raise it as an issue
only when it changes one of our decisions:

* another collection's version of the data (TabSTAR's columns or labels) is no reference for ours; name it only for
  provenance or a duplicate (Lennart, 2026-10-15);
* whether a dataset is in some model's pretraining data does not change any decision (Lennart, 2026-10-12);
* scores other benchmarks published (TALENT, leaderboards) are no evidence: their random splits are wrong for most of
  our tasks (Lennart, 2026-10-15).

## Repair or rebuild before keeping damaged data

When a release is damaged (rows of another patient, units mixed across sites, values scaled over all rows, labels
taken from the wrong rating), check whether the origin has the clean data before keeping the damage or retiring the
dataset. SUPPORT2's phase II physiology was restored from the study data (ICPSR 2957); ashrae's readings were put in
kWh from the data owners' raw files; coad_colon_adenocarcinoma was retired for a rebuild from the GDC's per-sample
files, and corporate_credit_rating for one from the agencies' own rating histories. A rebuild that would not match
the release exactly is a new dataset with its own record.

## Citing papers

A dataset's paper is often the decisive evidence, so any claim attributed to one comes with a text reference: the
section, table or page, and the load-bearing sentence quoted, from text you read (not the title, the abstract or a
recollection of the field). Write it as `Sec. 6.1, p. 12: "..."`, so the next curator can check it in one step. Two
traps this prevents, both real:

* A paper can refute the claim you were about to make. kddcup99: the simulation-artifact critique (Mahoney & Chan,
  RAID 2003) looks like it condemns KDD, but Tavallaee et al. (CISDA 2009, Sec. III) state that the artifacts "do not
  affect the KDD data set since the 41 features used in KDD are not related to any of the weaknesses mentioned".
* A paper's own framing can decide the verdict. intrusion_detection: the BCCC/NTLFlowLyzer paper (Shafi et al.,
  Computers & Security 148:104160, 2025) says in Sec. 6.1 "our focus is on developing a profiling system, not a
  detection system", so its headline ">99.8%" is profile coverage, and the release ships no target, split or
  baseline: `No Good Target / Scientific Discovery`.

When the publisher's copy is paywalled, spend a short search on a free copy: Unpaywall, Europe PMC, arXiv, Semantic
Scholar, the authors' or institution's pages, and a web search for the exact title in quotes plus "pdf" (with and
without the quotes, and with the first author's name). Copies often sit on PDF mirrors (ResearchGate, SciSpace,
oa.mg, CORE, Academia.edu). When nothing turns up or a mirror cannot be fetched, ask the curator for the PDF as soon
as the paper turns out to matter, with the exact query (a Google search for the title plus "pdf" usually finds it).
If you go on without it, say so and mark the claim as unverified rather than paraphrasing the abstract as if it were
the text.

## Competition pages are claims

A competition or dataset page is a claim about the data; the discussion threads and the public notebooks are where the
problems surface. Before triaging anything from Kaggle or a similar platform, skim both (by votes) for leak threads
and "hack" baselines (a trivial rule that scores near the top), disputes about the test set (random or temporal,
ground truth recoverable from a public upstream), duplicated or mislabelled rows, a column that is the target in
disguise, and the uploader's answers about where the data came from. Write what you find with the thread or notebook
link.

pkdd-15-taxi-trip-time-prediction-ii (Porto, ECML/PKDD 2015): a public snippet predicting
`max((len(POLYLINE) - 1) * 15, 660)` scores well, not because test data leaks but because the test polylines are
truncated prefixes of the trips (de Brebisson et al. 2015: "The testing dataset is composed of 320 partial
trajectories, which were created from five snapshots taken at different timestamps"), so the elapsed time is a lower
bound on the target. The competition predicts the remaining travel time from a partial trajectory, a trajectory task;
only the notebooks make that visible.

## Is the data generated?

A table that looks clean and scores well can still be synthetic, or a real table someone reworked (relabelled,
columns renamed, values replaced). Generated data is `No` with `AHDS`, usually with `Missing source information`, and
`Data Quality Issue` when a real table was manipulated.

Suspect it when there is no traceable first source, a data card names only "a company" or "an airline", "where is this
from?" threads stay unanswered, the data is course or competition material, scores look too good (F1 0.97 on a
survey), or distributions look too even. Then run these tests, cheapest first, on the earliest version you can find:

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

## In Data Foundry

The record fields for source, year and links, the `_duplicate` naming and how to note a third-party problem:
[records.md](../../knowledge-data-foundry/references/records.md). The definition's `source`, `year`, `source_url`,
`download_description` and `bibtex`: [definitions.md](../../knowledge-data-foundry/references/definitions.md). The
Kaggle command line and other access recipes:
[sources_access.md](../../knowledge-data-foundry/references/sources_access.md).
