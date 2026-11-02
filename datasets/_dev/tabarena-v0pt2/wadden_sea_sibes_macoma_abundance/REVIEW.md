# wadden_sea_sibes_macoma_abundance

**Outcome:** added. The AI recommends shipping it with the changes made after the review panel (summarised at the
end of this block). The data are NIOZ's SIBES survey of the Dutch Wadden Sea flats (version 6 of 2024-12-21,
CC BY-SA 4.0): one row per fauna sample, 59,044 samples at 5,092 stations, 2008-2022. The target is the Baltic tellin
(Macoma balthica) per m^2, zero where the sample held none (56.0%), built by the data descriptor's own join; shipped
as log1p and scored after the inverse. Known: the position, tidal basin and flat, the survey's date, the sediment
interpolated from that year's other stations and, since 2026-11-02, the elevation from Rijkswaterstaat's depth surveys
(vaklodingen). Whole stations are held out with all their years, so a test station
stands for a place between the stations of a survey already run. The metric is RMSE on the density (fallback).

Validity:
* SEL-2 holds: your `Yes` of 2026-10-30, with your answer of the same day to policy question 1 of the
  zero-inflated review (species-abundance mapping is judged per dataset, no new rule).
* USE-1 and USE-5 triggered, fixed: the use case's example, judging food stocks for birds, did not fit a count
  target. The 50 cores above 10,000 per m^2, which set the score, are spat (newly settled juveniles, 36 of them from
  2014): 11.8% of the tellins counted but 1.3% of their biomass. The use case is now the source's: the abundance map
  of a past survey. The fit stays approximate: no named decision (USE-8); the elevation is joined (issue 4).
* USE-3 and LEAK-10 triggered, fixed: the sediment measured at the visit does not exist at an unsampled place, and its
  gain came from the visit itself. It is replaced by the sediment interpolated from the year's other stations, the
  source's own covariate (LEAK-6, LEAK-7, CLEAN-19; issue 5).
* LEAK-25 triggered, fixed by default: the 342 samples of 2008 without any fauna record are dropped, located by the
  year; the 427 later ones stay as zeros (issue 2).
* SPLIT-1: your pick, grouped by station (issue 1); the leak test across the split finds none.
* PROV-9 holds: a yearly growing release takes the year of the pinned snapshot, 2024.

Value: TP-2 holds (untuned LightGBM R^2 0.373 on log1p at unseen stations with the interpolated sediment and the
elevation, against 0.235 for a linear model, task probes of 2026-11-02, 5 of 9 splits); TP-5 holds (about 1,700
test stations per fold). MET-5 gives the fallback `rmse` on the density, kept by your call of 2026-11-02 (the Poisson
deviance went to nantucket alone).

Quality: the 71 samples with unidentified tellinoid spat leave (CLEAN-15); six duplicated sample ids keep one row,
and their conflicting sediment is no source of the interpolation (CLEAN-1). The 117 pairs of a grid and a random
sample taken at one station on one day now share every feature; each pair stays in one fold through the station.
The one check warning, `task_target_value_dominant` (56.0% zeros, observed absences), waits for your acceptance
reason (add-dataset step 6).

Weighed: NIOZ's DOI release with a data descriptor +; a real but soft use case 0; 59,044 rows at 5,092 stations +; a
thin feature set, now with elevation 0; RMSE on the density separates models poorly -. All issues settled on
2026-11-02.

After the review panel (AI, 2026-11-01) the definition took the mediator's ten changes: the sediment, the samples
without a fauna record, the Tellinoidea samples and the use case above; the moment of the map in the split text
(issue 1); the date named as the survey's date; the metric note; count slips and two notes. The numbers
here and in the issues were measured again on the changed definition, so some differ from the panel's (default
LightGBM R^2 0.343 on log1p, against the panel's 0.368 with measured sediment; 117 station-days with two samples,
not 114; RMSE 879.7 against 847.1 for the Tweedie fit, not 865.8 against 837.2).

**Main points:** Nothing left to decide; all settled on 2026-11-02: the interpolated sediment stays (issue 5), the
split by station stays after a clean leak test (1), the 2008 samples without a fauna record go (2), the elevation is
joined (4), RMSE on the density stays (3).

**Issues for Andrej:**

5. **Keep the sediment interpolated from the year's other stations in place of the values measured at the visit?**
   The grain size and mud content were measured in a jar taken at the same visit as the fauna core. A place on the
   map has no visit, so after the panel both columns were replaced by values interpolated (inverse squared distance)
   from the 8 nearest other stations of the same survey year, as the source maps them.
   * What it changes: with the measured values a test station gets a reading from its own visit. R^2 on log1p was
     0.012-0.018 higher with them in three model families (9 of 9 folds), and the station's sediment from its other
     years recovers only 0.003 of that (0.352 against 0.349 with no sediment), so the gain belongs to the visit. RMSE
     on the density does not separate the variants.
   * For replacing: USE-3 and LEAK-10 (Must) make a value that did not exist at the prediction point a leak, and
     LEAK-6 removes a confirmed leak even when small. The critic and the split auditor; the advocate conceded in
     rebuttal; the mediator settled it so.
   * For keeping them with a note: LEAK-6's first clause ("a slight optimism with a known cause can stay with a
     note"); the opening of the advocate, claim auditor, domain practitioner and blind reviewer.
   * Like case: noaa_afsc_bottom_trawl_survey_cpue (same run, undecided) keeps the temperatures measured during the
     haul, which carry no gain there (R^2 0.652 with, 0.651 without, its panel). No Tensions row covers a covariate
     measured with the target against the map used at deployment; your call here and on AFSC becomes that row.
   * Rule: USE-3, LEAK-10, LEAK-6 (Must); LEAK-7 (Should) for interpolated over none; CLEAN-19, as rain_in_australia.
   * Implemented: interpolated sediment; it also fills 2008, when sediment was taken on a 1000 m grid. Cost: the
     default LightGBM scores 0.343 with it against 0.349 with no sediment.
   * Alternative (a): no sediment. Cost: smooth models lose the source's covariate (spline ridge -0.035).
   * Alternative (b): the measured values kept as a named potential leak. Cost: a test station sees its own visit
     (default LightGBM 0.361).

   Recommendation: as implemented, with the Tensions row "a covariate measured with the target is replaced by the
   deployed map's value when it carries a measured gain over it, and kept with a note when it carries none".
   Decision: as implemented, (a) or (b)?

   **Andrej (2026-11-02, ok):** My recommendation is to keep the interpolated sediment for this mapping task. It
   approximates information available at unsampled locations and preserves potentially useful habitat inputs.

   **Answer (AI, 2026-11-02):** Kept as implemented: `interpolated_median_grain_size_um` and
   `interpolated_mud_percent` from the 8 nearest other stations of the survey year; the measured values stay out. With
   the elevation joined (issue 4) the interpolated mud still adds R^2 0.006 (leak probe "without" 0.288 against 0.294
   for all features). The Tensions row is not written here; it is a knowledge-file change for a later pass.

   **Resolved (2026-11-02, Andrej):** the interpolated sediment stays, as implemented.

1. **Confirm the split by station over a split by survey year?** SPLIT-1 leaves the regime to you. Your CC of
   2026-10-30 records only `Yes`, priority 3; the screening named grouped by station, with temporal by year as the
   alternative.
   * What it changes: grouped by station tests a place between the stations of a survey already run, with that
     year's neighbouring stations (median 500 m away) and the other years in training. Temporal would test next
     year's survey.
   * For grouped: Lyashevska et al. 2016 use their model "to make predictions for sites where only environmental
     data are available" and validate it by leave-one-out over the stations of one survey
     ([paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4729254/)). Holding a station out in all its years is
     stricter than that: R^2 0.343, against 0.378 when its other years stay in training.
   * For temporal: neither the paper nor the data descriptor forecasts a later survey. Expanding yearly windows score
     R^2 0.16-0.33 (mean 0.25).
   * The whole panel prefers grouped.
   * Rule: SPLIT-1 and SPLIT-3 (Must): one regime, the one the use case implies. Precedent: 5g_energy_consumption
     (Lennart, 2026-10-14), a split by station that fills the gap between stations.
     noaa_afsc_bottom_trawl_survey_cpue (same run) is temporal because each of its maps stands for five future years.
   * Implemented: grouped by station, 3 repeats of 3 folds. Cost: later surveys train the early years, as for a map
     drawn from the whole archive (R^2 0.343 against 0.316 when each test year trains only on the years up to it,
     mostly 2008-2012); the split text says so.
   * Alternative: temporal by survey year. Cost: it tests a forecast of next year's survey, which neither source
     makes.

   Recommendation: grouped. Decision: grouped or temporal?

   **Andrej (2026-11-02, discuss):** Make sure there are no temporal or spatiotemporal leaks when using grouped

   **Answer (AI, 2026-11-02):** No leak found; the split by station stays. Untuned LightGBM on log1p, the shipped 3x3
   folds, with the elevation joined (shipped R^2 0.376):

   * Shared rows or units: no test row has a feature copy in training; no station is on both sides. No two stations
     lie within 10 m (279 within 50 m, the design's random stations).
   * Nearby places in the same year (spatiotemporal): merging every station within 50, 100 or 250 m of another into
     one group moves R^2 by +0.000, -0.002 and -0.006 (3x3 folds), so no nearby station acts as a copy. 3.0% of the
     test rows have a training sample of their year within 50 m and 6.8% within 100 m, against 14.5% of map pixels
     (split audit); those score higher (0.45 against 0.37 at 400-600 m), as an interpolation should. The
     nearest-neighbour correlation of log1p is 0.55 within 100 m, as for two cores taken at one station on one day
     (0.53).
   * The training side's outcome of the same survey year (the wisconsin test): removing the test year's training
     rows costs R^2 0.085 pooled and 0.089 within a year, as many random rows 0.002 (9 of 9 splits); without its year
     the model misses the year's level by up to 1.0 log unit (2017-2019). The score does lean on the same survey. Here
     that is the use case's input, not a leak: the map of year Y is drawn from year Y's survey, after it was run, as
     the source's leave-one-out over one year's stations. In wisconsin the year's claims are not known when the
     year is priced.
   * Later surveys (temporal): trained only on the years up to its own, a test year scores R^2 0.317, against 0.299
     on as many random training rows (repeat 0; 2008-2012 +0.043, 2013-2021 +0.005). The later years add rows, not
     the test year's outcome.
   * Features from other rows' outcomes: none. The sediment is interpolated from other stations' sediment, the
     elevation comes from a separate depth survey, the basin and flat are fixed names.

   Changed: `splits_comment` holds these numbers; the earlier sentence on "0.343 against 0.316 up to the test year"
   is replaced by the sample-size comparison. The split is the use case's, not forced, so SPLIT-8's Cases row is not
   extended.

   **Resolved (2026-11-02, Andrej):** grouped by station, kept; the leak test across the split finds none.

2. **Which samples without any fauna record to drop?** 769 samples are in the sample list but have no fauna record at
   all, not even of another species. By the descriptor's zero-fill recipe they would be tellin zeros. But an empty
   record can be an empty core or a sample whose fauna was never entered.
   * What it changes: a missing record kept as a zero teaches the model that tellins are absent where nobody looked;
     a true empty core dropped removes a real absence. The disputed 427 are 0.7% of the rows (zero share 55.2-56.0%
     across the options).
   * 2008: 342 of them, 9.0% of that year against 0.2-1.5% in each later year, spread over all basins and 50 of the
     53 sampling days. The recorded 2008 samples hold tellins as often as the same stations in 2009 (30.5% against
     29.9%), but fewer species (5.8 against 7.4).
   * 2009-2022, 427 samples, for real empty cores: the descriptor's Table 1 counts them among the processed samples
     in every year, and it says a sample that could not be processed "did not lead to an entry in the database"
     ([descriptor](https://doi.org/10.1038/s41597-025-04540-9)). Their stations are empty on 3.3% of their other
     visits from 2009 (0.77% for all samples) and hold fewer species on them (5.1 against 7.6).
   * Against, pointing to missing records (circumstantial): they lie in mud (median 22.6% mud against 4.7% for
     recorded cores without tellins). Their share rises with mud much faster than the share of species-poor recorded
     cores (at most 2 taxa), which real empty cores would track: 0.3% against 3.6-4.9% at 2-10% mud, 1.0% against 3.8%
     at 20-40%. They cluster in basins of average richness (Borndiep 1.5%, Eilanderbalg 1.8%) and are rare in the
     poorest one (Dollard 0.6%), where real empty cores would be commonest.
   * The advocate and the critic agree on the implemented version; the blind reviewer would drop all 769.
   * Rule: LEAK-25 (Must, amended 2026-10-21): data that mix "no event" with "not recorded" are recovered when the
     unrecorded rows are located by a rule that does not read the label, and dropped. The year is such a rule for
     2008. "No species recorded" is the outcome "an empty core" itself.
   * Precedents: account_debt_south_africa (whole file runs without data),
     fraud_detection_in_electricity_and_gas_consumption (folder `_1m`; "never by the label") and
     caracas_cervical_cancer drop only rows located by another fact.
   * Implemented: drop the 342 of 2008 and keep the 427 as zeros (59,044 rows).
   * Alternative (a): drop the whole 2008 survey (3,792 samples), a rule that never reads the core (55,594 rows).
     Cost: the 3,450 recorded samples of the first survey go.
   * Alternative (b): drop all 769, as first built, with the mud and basin pattern recorded as the fact that sets the
     427 apart from the precedents (58,617 rows). Cost: if the source's Table 1 is right, it drops true empty cores
     at the barest places, by a rule that reads the outcome.

   Recommendation: as implemented. The source's own counts treat the later samples as processed, and the pattern
   against them is circumstantial. Decision: as implemented, (a) or (b)?

   **Answer (AI, 2026-11-02):** Kept as implemented: the 342 samples of 2008 without a fauna record are dropped, the
   427 of 2009-2022 stay as zeros (59,044 rows).

   **Resolved (2026-11-02, Andrej):** as implemented.

4. **Join elevation from Rijkswaterstaat's depth surveys?** Elevation, which sets how long a flat is under water, is
   the paper's third covariate and, with mud, one of the main factors of tellin habitat. The SIBES release has none. A
   map maker has it for any place from Rijkswaterstaat's bathymetry (vaklodingen).
   * What it changes: the model maps from position, basin, flat, date and interpolated sediment only. Elevation adds
     the input every practitioner uses; its gain here is unmeasured.
   * Rule: CLEAN-19 (Should) allows building an input the actor has but does not require it, so not joining is no
     departure. Precedents where such a gap was closed: mortgage (FRED rates joined, 2026-10-22),
     qsar_bioconcentration (logKOW added, 2026-10-26).
   * Implemented: not joined; `fit_reason` names it as the main input gap.
   * Alternative: join the elevation at each station from the vaklodingen grids. Needs their licence checked and a
     build step.

   Recommendation: ship without it now; the join can follow if you want it. Decision: join or not?

   **Andrej (2026-11-02, change):** Join it if it is available.

   **Answer (AI, 2026-11-02):** Joined. Rijkswaterstaat's vaklodingen are public on Deltares' OpenEarth server
   without a login
   ([catalog](https://opendap.deltares.nl/thredds/catalog/opendap/rijkswaterstaat/vaklodingen/catalog.html)):
   40 netCDF tiles of 20 m cells hold all 5,092 stations (release `vaklodingen_release20260303`, 2.9 GB).
   `elevation_m_nap` is the height above NAP of the station's cell in the latest survey on or before the sample's
   date (median 2.7 years earlier, 98.0% within 6 years; 5 samples have no earlier survey and stay missing). It is a
   survey of the bed, separate from the visit, so it exists at an unsampled place (USE-3).
   * Gain on the 9 shipped folds: untuned LightGBM R^2 on log1p 0.343 to 0.376 (+0.033, 9 of 9), a spline ridge
     0.210 to 0.293, RMSE on the density 872.8 to 863.9 (lower in 9 of 9). It is the strongest single feature
     (task probe, 5 of 5 splits; R^2 0.164 alone).
   * Licence: the netCDF files say "can be used freely for research purposes provided that the following source is
     acknowledged: Rijkswaterstaat"; data.overheid.nl lists Rijkswaterstaat's 20 m bathymetry under CC0 1.0
     ([page](https://data.overheid.nl/dataset/61446-bathymetrie-nederland---kust-en-vaklodingen-20-mtr)). The
     definition cites Rijkswaterstaat in its bibtex and `download_description`; `fit_reason` no longer names the gap.
   * The download needs a rebuild to reach a container (2.9 GB more raw data).

   **Resolved (2026-11-02, Andrej):** elevation joined from the vaklodingen.

**Review panel:** ship after changes (mediator). Claim audit: 41 claims, 30 hold, 6 refuted or partly refuted (the
use-case example, the no-record framing, the station-day counts and the Kendall tau note fixed in the definition; the
metric's meaning is issue 3; the record's year is a field row), 5 untested or contested. Blind review: would include
with changes; its main concerns were `station` as a feature (the API drops the group column) and the raw datetime (the
house format). Debate: agreed on the verdict, the use-case wording, the archive-map moment, keeping the 427 later
samples without a record and `rmse` with a corrected note as the least the metric needs; disputed the measured
sediment (settled for the critic: interpolated; issue 5) and the coarse tellin classes (settled: all 71 Tellinoidea
samples dropped, the Tellininae zeros kept); which samples without a record to drop (issue 2) and the metric (issue 3)
go to you.

<details><summary>Mediator</summary>

**Mediator: wadden_sea_sibes_macoma_abundance (mediator, 2026-11-01)**

**Recommendation**

```text
Verdict: ship after changes.
Validity: SEL-2 holds (CC Yes 2026-10-30; policy call 1). USE-1/USE-5 triggered, fixed (use case reworded to the
  source's map of a surveyed year; food-stock example dropped). USE-3/LEAK-10 triggered, fixed (sediment measured at
  the visit replaced by sediment interpolated from the year's other stations; LEAK-6, LEAK-7, CLEAN-19). LEAK-25
  triggered, fixed by default (342 samples of 2008 without a record dropped, 427 later ones kept; issue 2). LEAK-33
  holds (station is the group column). SPLIT-3, SPLIT-24 hold; SPLIT-1 regime for the curator (issue 1). PROV-9
  holds (2024).
Value: TP-2 a real signal (LightGBM skill 0.355 on log1p as built, 0.349 with interpolated sediment; +0.193 over
  linear); TP-5 holds (1,693 test stations per fold). MET-5 fallback rmse and MET-3 hold; MET-10 resolution
  weighed (issue 3).
Quality: CLEAN-15 triggered, fixed (all 71 samples with Tellinoidea dropped); CLEAN-1 holds (six duplicated ids);
  notes the data refutes corrected (EV-8).
Weighed: source + (NIOZ DOI release, Scientific Data descriptor); use case 0 (real but soft, approximate); size +;
  thin inputs, no elevation -; density RMSE resolves models poorly -.
For the curator: issue 1 (confirm grouped), issue 2 (which samples without a record to drop), issue 3 (rmse or
  Poisson deviance, a weighing call), issue 4 (elevation join, a weighing call).
```

The advocate and the critic agree on the verdict and on every change below except the two disputes the main session
named; both are settled here by a check (sediment: by rule, with an experiment on the remedy; coarse tellin classes:
by species.csv and rule). Scripts and outputs are in the run folder (not committed): m1_sediment_families, m2_records,
m3_later_empty, m4_counts.

**Agreed facts**

* Source: NIOZ SIBES dataset version 6 (2024-12-21), CC BY-SA 4.0; sha256 and portal sizes match. The blind
  reviewer rebuilt all 58,688 shipped rows exactly from the raw files.
* 59,463 samples at 5,105 stations, 2008-2022. Target Macoma balthica (sibes_id 59) per m2, zero-filled by the
  descriptor's Table 4 recipe; 55.67% zeros as shipped.
* Group: `sampling_station_id`, coordinates constant within each id; no station on both sides in any of the 9 folds;
  1,693-1,694 test stations and 19,400-19,702 rows per fold. `station` is dropped from the inputs by
  `feature_columns` (LEAK-33).
* Signal (untuned LightGBM, R^2 on log1p): grouped by station 0.368, station-year groups 0.391, IID 0.389;
  expanding temporal windows mean 0.249. Training only on years up to the test year: 0.345; the gap sits in
  2008-2011.
* Sediment (6-9 folds): measured 0.368, the station's own sediment from its other years 0.358, none 0.355-0.356,
  interpolated (IDW, 8 nearest other stations of the year) 0.349. Density RMSE 862.1-864.1 for every variant against
  875.6 for the dummy. No source names an actor who has sediment measured where no fauna sample is taken.
* 769 samples have no fauna record of any taxon: 342 in 2008 (9.0%), 0.17-1.53% in each later year. Descriptor
  Table 1 "processed" counts equal the samples.csv rows in each year (2017-18 backlog aside).
* Tellinoidea (sibes_id 339, "below 3 mm ... Includes ... Macoma balthica") occurs in 71 samples, 29 of them without
  a Macoma row. These rows hold 0.07% of the squared deviation of density.
* Metric: 2014 holds 75.4% of the squared deviation of density, the 10 densest cores 58%. The note's "Kendall tau
  0.71-0.79" is wrong (0.62-0.71 on the seven log1p models; 0.17-0.56 with mean-targeting fits). V6 does not
  reproduce the paper's 2010 counts (variance 97.5 against 24). A back-transformed log1p model puts basin-year means
  at 0.20 of the observed and scores 3% behind a Tweedie fit (865.8 against 837.2); the Tweedie fit wins 6/6 folds
  (gap 28.7, SE 3.4). RMSE on log1p is out (MET-3, Must).
* The dropped visit columns carry nothing (0.367 against 0.368); the day of year adds 0.002-0.003 and a neighbour's
  day in its place changes R^2 by -0.0003. 142 near-twin station pairs (11-48 m); grouping them moves R^2 by
  +0.0016 (SE 0.0047), and SPLIT-24 forbids distance grouping.
* Slips in the notes: 114 station-days with two samples, correlation 0.536 (not 123, 117, 0.55); later years
  "0.2-1.5%"; base rates 7.6 taxa and 0.77% missing beside 5.8 and 2.8%; a boat sample is two cores bulked; random
  stations sit on gridlines; the first Lyashevska quote describes earlier studies.

Facts settled by the mediator's checks:

* Sediment remedy (m1; 9 shipped folds, R^2 on log1p, untuned):

  | model | measured | interpolated | none | interpolated minus none |
  |---|---|---|---|---|
  | ridge on splines | 0.252 | 0.241 | 0.204 | +0.037 (SE 0.001), 9/9 |
  | LightGBM, 15 leaves, 200 per leaf | 0.344 | 0.328 | 0.325 | +0.004 (SE 0.001), 9/9 |
  | LightGBM, 63 leaves | 0.368 | 0.349 | 0.355 | -0.006 (SE 0.001), 0/9 |
  | random forest (3 folds) | 0.354 | 0.337 | 0.354 | -0.017, 0/3 |
  | kNN, 25 | 0.280 | 0.286 | 0.330 | -0.044, 0/9 (extra dimensions dilute the spatial distance) |

  The measured values beat the interpolated ones by +0.011 to +0.019 in every family but kNN, 9/9 folds. The
  interpolated sediment carries a real signal that smooth and regularised models use (correlation with the measured
  values 0.82 for mud, 0.88 for grain size) and that flexible trees partly overfit. Density RMSE moves by at most 3
  between variants.
* Tellininae (sibes_id 389) remark in species.csv: "Tellininae between 3 and 5 mm are classified on the subfamily
  level. So far, only Macomangulus tenuis and Fabulina fabula were found." Its 12 cores without Macoma (2018) hide no
  tellin; their stations' Macoma history (54%) is habitat, not taxonomy.
* 2008 (m2): the recorded 2008 samples hold Macoma as often as the same stations in 2009 (0.305 against 0.299), but
  fewer taxa (5.8 against 7.4).
* The 427 later samples without a record (m2, m3): median mud 22.6% against 4.7% for recorded cores without Macoma
  and 10.6% with it. Their share rises with mud faster than the share of poor recorded cores (at most 2 taxa):
  0.30-0.33% against 3.6-4.9% at 2-10% mud, 0.99% against 3.8% at 20-40%, 2.05% against 10.5% above 40%. They are
  most frequent in Eilanderbalg (1.8%) and Borndiep (1.5%, 125 of the 427), basins of average richness, and rare in
  the poorest, Dollard (0.6%, 5.2 taxa). Circumstantial (EV-6): it points to missing records, while the source's
  Table 1 points to processed empty cores.
* Rows after the changes (m4): 59,044 at 5,092 stations, 56.0% zeros (42.3-69.6% by year). Whole 2008 dropped
  instead: 55,594 rows, 55.2%. All 769 dropped instead: 58,617.

**Changes to make now (no decision needed)**

1. Replace `median_grain_size_um` and `mud_percent` with the sediment interpolated from the other stations of the
   same survey year (USE-3 and LEAK-10, Must; LEAK-6: a confirmed leak goes even when small; remedy LEAK-7 and
   CLEAN-19, bullets 1 and 4, as rain_in_australia). Construction as in the split auditor's s4: per year, the 8
   nearest other stations with measured sediment, weights 1/max(d, 50 m)^2, the station itself excluded, the six
   conflicting duplicated ids excluded as sources. It fills 2008 from the 1000-m sediment grid, so the missing-sediment
   bullet goes. Rename the columns after what they hold. Rewrite comment 1, `known` and `fit_reason`: the sediment
   gap leaves `fit_reason`; elevation and the unnamed decision keep the fit approximate (USE-8).
2. Keep the 427 samples of 2009-2022 without a fauna record as zeros (Table 4 recipe); drop only the 342 of 2008
   (LEAK-25; the default of issue 2). Rewrite comment 3 and the Decision with the Table 1 match and the base rates,
   and remove "not on the tellin count".
3. Drop all 71 samples with Tellinoidea present: in each the Macoma count is a lower bound, as Macoma below 3 mm is
   counted there (CLEAN-15, Must), and the rule reads another taxon's record, not the label (LEAK-25). Keep the 12
   Tellininae-only cores as zeros. Add a note.
4. Reword `use_case` to the source's objective: an abundance map of a survey year already run, between its stations,
   for habitat-directive, quality-status and impact assessments; drop the food-stock example; add a note on why
   numbers and not biomass (the paper's quantity; the release has no size classes) (USE-1, USE-5, Must).
5. Name the moment in `task_summary.split` and `splits_comment`: a map of a past survey drawn from the whole archive
   (0.368 against 0.345 with only the years up to the test year; the gap falls on 2008-2011), and that the split is
   somewhat strict for a map (test stations a median 500 m from the nearest training station of the year; map
   pixels 192 m) (USE-3, SPLIT-1).
6. Call `date` the survey's date in `known` and comment 1 (USE-3; a neighbour's day changes R^2 by -0.0003).
7. Metric note and `Metric.fallback` reason: drop the tau claim; add 2014's 75.4% share and the 0.20 basin-mean ratio
   of a back-transformed log1p model; say "ranks as the paper's MSE" only by construction (density = count / core
   area) and that V6 does not reproduce the paper's 2010 counts (MET-11, EV-8).
8. Fix the slips listed under the agreed facts (EV-8), and update every count the changes move (rows, stations, zero
   share, the proposed `task_target_value_dominant` text).
9. Notes: the 2017-18 samples were processed late (descriptor); Bivalvia sp. ("parts of individuals", 874 samples) is
   kept, as no species list ties it to Macoma (CLEAN-1).
10. Record: an Assessment line with the panel's outcome; the record's year to 2024 is a field row for the curator.

**Changes that need the curator (issues, ranked)**

1. Confirm grouped by station over temporal (P4; SPLIT-1, Must: the curator picks the regime; SPLIT-3). Effect: the
   test measures a place between the stations of a surveyed year, not next year's survey. For grouped: the paper
   predicts "for sites where only environmental data are available" and validates by leave-one-out over the stations
   of one survey; holding a station out in all years is stricter than the paper (0.368 against 0.391). For temporal:
   nothing in either source; windows score 0.25. The whole panel prefers grouped. Decision: grouped or temporal.
2. Which samples without any fauna record to drop (P4; LEAK-25, Must). Effect: 0.7% of rows; zero share 55.7-56.0%.
   For the default (drop 342 of 2008, keep 427): the year locates the 2008 rows as a fact about the recording; the
   source's Table 1 counts the later rows as processed and says unprocessed samples leave no entry; their stations
   are empty on 2.8-3.3% of other visits (0.77% overall). For (a), drop the whole 2008 survey: the only rule that
   never reads the core; 2008's recorded samples hold fewer taxa (5.8 against 7.4), though as many tellins. For (b),
   drop all 769: the mud and basin pattern above (the blind reviewer would drop them). Advocate and critic: default.
   Decision: default, (a) or (b).
3. Keep `rmse` on the density or take `mean_poisson_deviance` on the density (P6; MET-10, Weigh; MET-11 context,
   MET-12, MET-13). For rmse: consistent for the mean a manager sums; the ranking survives removing each fold's five
   densest rows (tau 0.79-1.00); the Tweedie fit beats the biased model 6/6. For the deviance: stable ranks (Tweedie
   first 6/6, the 5x-biased model 7th-8th in every fold), the source model's loss; costs a library metric with tests
   and a floor on predictions. What would settle it: a family call with nantucket, pennsylvania and basque biotoxins.
   Advocate: rmse is enough; critic: rmse is the floor, the deviance the curator's call. Decision: which metric.
4. Join elevation from Rijkswaterstaat bathymetry (P7; CLEAN-19, Should, allows, does not require). The paper's
   third covariate and the domain practitioner's biggest input gap; gain unmeasured; licence and yearly grids to
   check. Precedents where the gap was closed: mortgage (FRED), qsar_bioconcentration (logKOW). Decision: join or not.

**Disputed points**

1. Measured sediment: keep with a note, or replace (P3/P4). Opening: the advocate, claim auditor, domain practitioner
   and blind reviewer would keep it as a small named gap (LEAK-6, first clause: "a slight optimism with a known cause
   can stay with a note"); the critic and, leaning, the split auditor would replace it (USE-3, LEAK-10, LEAK-6 second
   clause). The advocate's rebuttal concedes; the critic's rebuttal still argues against the opening.
   * Rule: USE-3 (Must, P3) says a value that did not exist at the prediction point is a leak. The prediction point
     is a place without a sample; the jar is taken just before the core, at the same visit, and no actor has one
     without the other (advocate's search). The gain is measured (+0.011 to +0.019 over the interpolated values, four
     families, 9/9 folds) and belongs to the visit (the station's own other-year sediment recovers 0.002 of the
     0.012; the critic's within-station check, mud z = 11). That is a confirmed leak, so LEAK-6's second clause
     applies; its first clause is for an optimism whose cause is not a value absent at the prediction point. Not a
     conflict between rules: one Must, classified by the facts.
   * "No change on the declared metric" is no reason to keep (LEAK-10 amendment, zillow_prize row: a "removing it
     changes no score" test alone is no reason); density RMSE does not resolve these variants at all.
   * Rewording to "given the sediment measured there" fails USE-9's weighed factor (a use case rephrased only to
     excuse a gap; no source describes the practice).
   * Remedy ladder: fix the definition. Interpolated against none: LEAK-7 (Should) prefers the smallest fix that keeps
     a valid signal, and m1 shows the interpolated sediment keeps one (+0.037 for a spline ridge, +0.004 for a
     regularised GBM, 9/9 folds), while the default LightGBM loses 0.006 with it. Settled: interpolated (change 1).
2. Coarse tellin classes: the critic's 41 rows (29 Tellinoidea plus 12 Tellininae cores without Macoma, CLEAN-15)
   against the advocate's 71 Tellinoidea samples (a rule that does not read the label).
   * Fact: species.csv says Tellininae 3-5 mm are "so far, only Macomangulus tenuis and Fabulina fabula" (and Macoma
     sits outside that subfamily), so the 12 Tellininae cores are observed tellin zeros. Tellinoidea below 3 mm
     includes Macoma, so in all 71 samples the Macoma count is a lower bound (42 samples hold 8,051 tellinoid spat
     per m2 beside 21,543 Macoma), not only in the 29 zeros.
   * Rule: CLEAN-15 (Must, P7) covers all 71. Dropping only the zeros selects on the label, which LEAK-25 (Must, P4)
     excludes as a way to locate unrecorded rows; the critic's own point 3 rests on that reading. Dropping all 71
     meets both, so there is no conflict to rank; the 41-row version fails LEAK-25 on its own. Cost: 0.12% of rows,
     yearly zero shares move by at most 0.001. Settled: drop the 71, keep the 12 (change 3).
3. The 427 later samples without a record: agreed by advocate and critic (keep), but the blind reviewer would drop
   them and the mediator's checks add facts on each side. Neither remedy meets LEAK-25's recovery clause in full
   (keeping may hold missing records; dropping by "no species recorded" reads the outcome), and the effect is 0.5% of
   rows, so this is a reading the rules leave open: issue 2.
4. The metric: agreed floor (rmse with notes corrected); whether the deviance is worth a family change is a weighing
   call under MET-10: issue 3.
5. Year 2023 or 2024 (claim auditor): PROV-9's clause for a source that grows over time (a monitoring programme that
   says it releases yearly) gives the pinned snapshot's year, 2024; the clause for a Kaggle upload that grew over
   versions (melbourne_housing_market) does not fit. Settled: 2024; the record field is a field row.
6. `station` as a feature and the raw datetime (blind reviewer): LEAK-33 holds (`feature_columns` drops the group
   column) and datetime is the house format. No change.
7. Mirroring the V6 files (builder): no rule; the working copy's growing sources pin by checksum and date. No issue;
   the download description already names the V6 checksums.

**Consistency with precedent**

* LEAK-25: the 2008 drop follows account_debt_south_africa (a recording fact) and mortgage (a null outcome set apart
  by another fact). Keeping the 427 follows caracas_cervical_cancer, account_debt_south_africa and
  fraud_detection_in_electricity_and_gas_consumption ("never by the label"). This answers the precedent checker's
  consistency check with its option (b); its option (a), with the mud and basin pattern as the distinguishing fact,
  is issue 2's alternative (b).
* Sediment: follows rain_in_australia (CLEAN-19, an input built from other rows of the same release). It departs
  from the same-run draft noaa_afsc_bottom_trawl_survey_cpue, which keeps haul temperatures under a place-year
  prediction point. The fact that sets this case apart: here the visit's value carries a measured gain over what a
  map gives (+0.011 to +0.019, 9/9 folds, and it belongs to the visit), while AFSC's temperatures carry none (0.652
  against 0.651). Not a precedent either way (both undecided); the AFSC mediator's line "wadden_sea keeps
  station-measured sediment on the same reading" is now stale and should be updated. The curator's call on both is
  the Tensions row the precedent checker proposed (a covariate measured with the target against the map used at
  deployment).
* Tellinoidea: the label-blind reading of LEAK-25 (fraud CC).
* Metric: forest_fires and gallstone_disease (MET-5); RMSE on log1p as an exception is not open (MET-3 is a Must).
  Decide with nantucket, pennsylvania and basque biotoxins. The insurance Gini suggestion of 2026-10-30 rests on that
  domain's standard metric and does not carry over.
* Grouped: 5g_energy_consumption (Lennart, 2026-10-14); AFSC's temporal split is set apart by its five-year maps.
* Duplicated ids: mortgage issue 15. Year: kickstarter, sf_permit_time; melbourne_housing_market set apart.
* No drift and no third exception; no exception is recorded by these changes.

</details>

<details><summary>Claim audit</summary>

**Claim audit: wadden_sea_sibes_macoma_abundance (claim-auditor, 2026-11-01)**

**Verdict:** the definition mostly holds. 41 claims tested: 30 hold, 6 refuted or partly refuted (none breaks the task), 5 untested or contested. Everything that bears on validity holds as written: the split, the copies, the features at the prediction point, the target count and the zero filling. What fails is three numbers or framings in the notes and one use-case example. The biggest new facts are about the metric: on our data, RMSE on density is mostly a score of the 2014 spat fall and of the back-transform. The fallback's origin and the fact that it can be computed both hold.

How the tests ran: the definition's frame and its shipped splits (`definition(...).to_container()`, 3 x 3, seed 4267) and the scorer `data_foundry.v2.metrics.scorer`. Raw files are the NIOZ V6 copy, with sha256 values that match the download description. Models are untuned LightGBM, RF, ridge and kNN, with thread caps. Scripts and outputs are in the run folder (not committed): a1_counts, a2_pairs, a3_metric, a4_paper, a5_rank, a6_features.

**Claim table**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | Unsampled place in a survey year, predicted from place, date and sediment | task_summary.question | Is any station on both sides of a split? | holds | 0 shared stations in 9 folds; 1,693-1,694 test stations per fold | SPLIT-3, USE-3 |
| 2 | Use case: map the density "to judge food stocks for birds or the habitat state" | task_summary.use_case | Do density and biomass (`afdm_m2`, in biota.csv) agree? Which rows drive the target? | **partly refuted** | Spearman density vs AFDM among positives is 0.32. The 50 rows above 10,000/m2 (36 from 2014) have a median of 0.84 mg AFDM per individual against 9.3 mg for all positives (spat). They hold 11.8% of the individuals but 1.3% of Macoma biomass. The abundance-map half holds (Lyashevska: "map the abundance") | USE-5, USE-1 |
| 3 | One core sample per station-day, June-October 2008-2022, 58,688 samples at 5,081 stations, most sampled in 13-15 of 15 years | task_summary.row | Count | holds (wording nit) | 58,688 / 5,081; months 6-10; 64.8% of stations in 13-15 years. Nit: a boat sample (92%) is two cores bulked (descriptor, Field sampling), so "one core" is loose | USE-8 |
| 4 | 55.7% zeros; ships as log1p, scored on the density | task_summary.predicted, `target_transform` | Count; scorer against a hand-computed RMSE | holds | 55.67%; scorer 887.361 = manual RMSE on density 887.361 (repeat 0) | MET-3 |
| 5 | Known: position, basin, flat, date, measured sediment | task_summary.known | Shipped splits, repeat 0: full date against year only | holds | R^2 log1p 0.368 with the date, 0.365 with year only: day of year adds 0.003 | USE-3 |
| 6 | Whole stations held out; neighbours "a few hundred metres away" in training | task_summary.split, splits_comment | Nearest other station | holds (nuance) | Median 500 m, 25th percentile 211 m. 142 pairs (279 stations, 5.5%) lie 11-48 m apart, mostly a grid and a random station, and 139 of them were sampled in the same years. Their same-year log1p correlation is 0.54, against 0.41 at 450-520 m. These are distinct stations, and SPLIT-24 forbids grouping them by a distance threshold | SPLIT-24 |
| 7 | Changes: zeros built, 1.3% dropped, sampling columns left out | task_summary.changes | Count | holds | 769 of 59,457 unique ids = 1.29% | |
| 8 | Fit approximate: R^2 0.365 with measured sediment against 0.349 with sediment interpolated from 8 stations | fit_reason; comment 1 | Re-run on the shipped splits with IDW from the 8 nearest other stations of the same year | holds | 0.368 measured, 0.348 IDW, 0.355 with no sediment at all. Interpolated sediment scores below none, so measured sediment's edge is +0.013 to +0.020 R^2 | USE-3, USE-8 |
| 9 | Year 2024, the pinned snapshot of a yearly release | `year`, download_description | Landing page and CKAN API | **contested** | Deposit and distribution date 2023-12-06; V6 published 2024-12-21; the files are unchanged on 2026-11-01 (same resource ids and byte sizes), so no yearly release in 22 months. The record says "`year` stays empty". PROV-9's "grows over time" clause gives 2024; its "one publication with versions takes the first version's year" clause (melbourne_housing_market) gives 2023 | PROV-9 |
| 10 | Licence CC BY-SA 4.0 | `license` | Landing page | holds | "Creative Commons Attribution Share-Alike 4.0" | |
| 11 | Version 6 and its checksums | download_description | sha256; portal resource sizes | holds | 2d5faefe / 8d762310 / 067bcbf2 match; portal sizes 5,837,616 / 12,301,618 / 17,344 equal the local files | PROV-9 |
| 12 | 59,463 samples at 5,105 stations, 2008-2022 | curation_comments intro | Count | holds | 59,463 rows, 5,105 stations | |
| 13 | Paper quote "covariate must be known everywhere"; elevation not in the release | comment 1 | Read the paper's text; samples.csv columns | holds | Quote verbatim in Materials and Methods (sediment interpolated by IDW in ArcGIS); samples.csv has 12 columns and no altitude | PROV-16 |
| 14 | Target is Macoma balthica (sibes_id 59), the paper's species; zero filling per Table 4 | comment 2 | species.csv; descriptor text | holds | One sibes_id; the quote sits in the Table 4 note. Untested caveat: coarse taxa that may include unidentified tellins (row 38) | USE-5 |
| 15 | 769 dropped, all Macoma zeros; 342 from 2008 (9.0%), 0.1-1.5% in later years; their stations average 5.8 taxa and are empty in 2.8% of visits from 2009 | comment 3, `_decisions` | Count | holds (numbers) | 769, 0 with Macoma, 342 = 9.02%. Later years 0.17-1.53% ("0.2-1.5%" would be exact). 5.78 taxa and 2.76% are in the builder's output. The note leaves out the base rates: 7.6 taxa and 0.77% empty for all stations from 2009 | LEAK-25, EV-9 |
| 16 | Descriptor: an unprocessed sample "did not lead to an entry in the database", "which these rows contradict for 2008" | comment 3 | Compare descriptor Table 1's "processed" count with the samples.csv rows per year | **partly refuted** (framing) | Table 1 "processed" equals the samples.csv count within 4 in every year from 2008 to 2021 except the 2017-18 backlog (2008: 3,792 against 3,792, which counts the 342 rows without records). For 2017 and 2018, Table 1 lists 2,831 and 2,274 against 4,139 and 4,140 rows in V6, so rows enter samples.csv once a sample is processed. NIOZ thus counts all 769 as processed samples. For the 427 rows of 2009-2022 (0.2-1.5% a year) that makes genuine empty cores the likelier reading. The 9% of 2008 is still implausible | LEAK-25, EV-6 |
| 17 | Six 2022 ids appear twice with conflicting sediment (149.8 against 47.2 um in one) and one fauna record | comment 4 | Count | holds | 6 ids, all 2022; 149.80 against 47.21; one set of biota rows each | |
| 18 | Sampling columns dropped; R^2 0.365 with and without them | comment 5 | Merged platform, sampling_type and surface back; shipped splits | holds | 0.368 without, 0.367 with (merge matched 58,688 of 58,688) | USE-3 |
| 19 | Sediment missing in 2,703 of the 3,450 kept 2008 samples and 1.2% later; quote on the 1000-m grid | comment 6 | Count; descriptor | holds | 2,703 / 3,450; 1.15% later; quote verbatim | |
| 20 | 123 station-days hold two samples, 117 of them grid+random; log1p correlation 0.55 | comment 7 | Count on the shipped rows | **refuted (numbers)** | Shipped rows have 114 station-days with two samples, all grid+random, correlation 0.536. The 123 counted raw rows, including the 6 duplicated ids (4 grid/grid, 2 random/random) and 3 days whose second sample was dropped | EV-8 |
| 21 | Metric note: 4-5 of about 19,500 test samples hold half the squared error; best of seven untuned models 876.6 against 887.4 for the training mean; zero/non-zero oracle R^2 0.04 on density, 0.93 on log1p | comment 8 | Recomputed on the shipped splits | holds | LightGBM: 4, 6 and 2 rows per fold. Training mean 887.36; RF 876.6 from the builder's CSV. Oracle values from exp_hurdle | MET-10 |
| 22 | "The two scales rank the seven models alike (Kendall tau 0.71-0.79)" | comment 8 | Recompute tau on exactly the seven models; then add density-aware variants | **refuted** | Builder's CSV, seven models: tau 0.62, 0.71, 0.62. The 0.71-0.79 included the constant `mean_log1p`, worst on both scales. Over nine fits (adding smearing, a Poisson model on density and the density mean), tau(density, log1p) is 0.28, 0.56 and 0.17 | MET-3, MET-10, EV-6 |
| 23 | Quote: "possible to encounter no animals in the core" | comment 9 | the paper's text | holds | Verbatim, Introduction | |
| 24 | Fallback origin: the paper reports several measures, no single criterion | `Metric.fallback` reason | Read Lyashevska Methods, Cross-validation, and Results | holds | Overall, user's and producer's accuracy at a 0.5 threshold, plus ME and MSE for μ and π·μ. The Abstract says "small performed slightly better"; Results "model large should be preferred" (from the CV of realizations). No criterion decides | MET-5, MET-11 |
| 25 | The SIBES descriptor and the data page define no metric | reason | Search the descriptor and the page | holds | The only error criteria are the 2012 design simulation's ("mean prediction error"), about sampling design, not this task | MET-1 |
| 26 | "RMSE on the density per m2 ranks models as the paper's MSE on the unconditional count per core" | reason | Area per sample; our 2010 against the paper's 2010 | holds by construction; **untested in substance** | Area is 0.01732 or 0.01767 m2 in 99.9% of samples, so density is count/area to within 2%. The paper's counts are not reproduced by V6: our 2010 has 60.5% zeros against 66%, mean count 1.94 against 1.39, variance 97.5 against 24, max 455 against 84. So whether the paper's count is `abundance_m2` x area is unverified | MET-3, EV-2 |
| 27 | Computable on every fold (implied) | metric | Scorer on 9 folds; units per fold | holds | Every fold scores. Test folds hold 19,400-19,702 rows, 1,693-1,694 stations, 8,422-8,955 positives and 14-20 rows above 10,000/m2 (repeat 0). No scoring columns needed. Training-mean RMSE per fold ranges 596-1,174 | MET-2 |
| 28 | Means on our task what the paper's MSE meant (implied) | metric | Spread of the squared deviation by year; resolution | **refuted (meaning)** | 2014 holds 75.4% of the squared deviation of density; the top 10 rows hold 58%. LightGBM on log1p gets R^2 0.030 on density over the training mean, and 2 of 7 untuned models lose to it. One smearing factor (x3.79) lifts R^2 to 0.070, more than LightGBM gains over the constant. The paper's unconditional MSE of 17.5 against a variance of 24 is about 0.27. Not noise, though: dropping the 50 dense rows keeps the ranking (tau 0.78-1.0) | MET-2, MET-10 |
| 29 | 5,081 stations, most sampled 13-15 times | grouping.definition | Count | holds | 64.8% in 13-15 years; rows per station median 13, max 28 | SPLIT-24 |
| 30 | Station = a grid node or "a random station placed off it" | grouping.definition | Descriptor | holds (wording) | Random stations are "placed on gridlines" at random distances from grid stations | |
| 31 | Paper quotes on predicting at unsampled sites | grouping.definition | the paper's text | holds (attribution nit) | Both quotes are verbatim. The first describes the generic habitat-suitability workflow of earlier studies (Introduction); the Abstract's sentence carries the claim | PROV-16 |
| 32 | Grouped rather than temporal (SPLIT-3) | splits_comment; record | Record CC lines | **untested as the curator's pick** | The screening said "SPLIT-3: one, the curator's pick"; the CC line gives only `Yes`, priority 3 and names no regime | SPLIT-3 |
| 33 | No row is a copy across the split (implied) | definition | Coordinates shared across station ids; feature-identical rows | holds | 0 coordinate pairs held by two station ids; 2 feature-identical rows, both in one station | LEAK, SPLIT-24 |
| 34 | Proposed warning acceptance: zero-inflated, 42-70% by year, presence AUC 0.81, R^2 0.32 on log1p among positives | builder report | Decisions table; shipped splits | holds (positives R^2 not re-run) | 41.9-69.5% by year; AUC of the log1p regressor for presence 0.813 | TP |
| 35 | 56.2% zeros (42-72% by year) before the drop | record, screening | Count on raw | holds | 33,445 / 59,463; 42.3-72.3% | |
| 36 | R^2 0.36 grouped, AUC 0.81, 0.28 temporal on 2021-22 | record, Comments | Shipped splits; train up to 2020, test 2021-22 | holds | 0.368; 0.813; 0.29 | EV-8 |
| 37 | Sediment missing in 3,687 samples; 171 taxa; no table released by the paper; CC BY-SA, 3-year embargo | record | Count; paper supplement; page | holds | 3,687 raw; 171 rows; the supplement is Table S1, "A list of key terms"; page text | |
| 38 | Every year is processed the same way and Macoma is counted at species level (implied) | definition | Coarse taxa by year; descriptor on the 2017-18 backlog | **untested** | Bivalvia sp. in 874 samples (242 in 2015, 261 in 2016, 177 in 2022), Tellinoidea in 71, Tellininae (added 2023) in 57, 55 of them from 2018. The 2017-18 backlog was processed late (descriptor: "will be finished in 2025"). Bivalve presence share is 0.53 in 2017 and 0.79 in 2018, against 0.62-0.68 in the years around them. No test separates a processing effect from real variation | PROV-13, USE-5 |
| 39 | "'3,451' is the number of 2010 grid stations, not of counts" | record | Paper; our 2010 | untested | The Abstract says "66% of the 3451 counts"; Methods gives 3,451 grid points plus 578 others (4,029). Our 2010 has 3,534 grid samples kept | EV-2 |
| 40 | mud = 0 is real sand: 1,534 rows, median grain 204 um | builder checklist | Count on shipped rows | holds (number off) | 1,506 rows on the shipped frame (1,534 likely raw); median 204 um | CLEAN |
| 41 | Record: "the year of the pinned snapshot (PROV-9), so `year` stays empty" | record, screening | Compare with the definition | **refuted (inconsistent)** | The definition sets 2024 under the same rule; record and definition disagree | PROV-9 |

**Refuted and untested claims, ranked (principles.md: validity first, Must first)**

1. **The use case's food-stock example against a density target (P3, USE-5 Must; row 2, partly refuted).** Density and biomass barely agree (Spearman 0.32 among positives). The rows that set the density metric are 2014 spat: 1.3% of Macoma biomass, but the top 10 rows hold 58% of the squared deviation. A manager judging bird food stocks would act on harvestable biomass, not spat counts. The abundance-mapping half of the use case is the paper's own objective and holds. *Changes:* which actor the task claims to serve. *Mildest remedy:* reword `use_case` to the abundance or distribution map ("habitat state") and drop the food-stock example. Retargeting to `afdm_m2` would be the curator's call, not needed for validity.
2. **Dropping the 769 samples without any record: the descriptor reading (P4, LEAK-25 Must; row 16, framing partly refuted).** The descriptor's own "processed" counts include these rows in every year, and the 2017-18 backlog shows samples.csv rows appear once a sample is processed. So NIOZ counts them as processed, and for 2009-2022 (427 rows at 0.2-1.5% a year, at stations empty on 2.8% of other visits against 0.77% overall) genuine empty cores are the likelier reading. 2008's 9% remains an anomaly. *Changes:* nothing measurable in scores (0.7% of rows, all zeros), but it bears on which rows LEAK-25 should remove. *Mildest remedy:* keep the drop or drop only the 2008 rows (curator's call, as in the builder's draft issue 1). Either way, rewrite comment 3 with the Table 1 match and the base rates (7.6 taxa, 0.77%).
3. **Year 2024 (P5, PROV-9 Must; rows 9 and 41, contested).** First distribution was 2023-12-06, with no new version in 22 months; the record says "empty", the definition 2024. *Changes:* a metadata field. *Mildest remedy:* the curator picks 2023 (first version, the melbourne_housing_market reading) or 2024 (the pinned snapshot) and the record is aligned. Also soften "with each yearly release" to "with each release".
4. **Processing and taxonomy across years (P5; row 38, untested).** Coarse bivalve and tellinid taxa in about 1,000 samples (1.7%) and the late-processed 2017-18 backlog could hide Macoma as false zeros. *Changes:* at most a few hundred target values. *Mildest remedy:* a note in the curation comments, or a question to NIOZ (Bijleveld) on how 2017-18 were processed and whether Tellininae or Tellinoidea can be Macoma.
5. **The metric's meaning on our data (P6, MET-2 Must and MET-10 Weigh; row 28, refuted in meaning; row 26 untested).** The origin and the computability hold (rows 24, 25, 27). But RMSE on density here scores mostly the 2014 spat fall (75.4% of the squared deviation) and the back-transform: smearing x3.79 gains more than LightGBM does over the constant. The best untuned R^2 on density is 0.03, against about 0.27 implied by the paper's 2010 MSE. The paper's counts are not reproduced by V6 (2010 variance 97.5 against 24, max 455 against 84), so "ranks as the paper's MSE" rests on an unverified count definition. In fairness to the declaration, the ranking survives dropping the dense rows (tau 0.78-1.0). *Changes:* what a leaderboard on this dataset rewards. *Mildest remedy:* keep `rmse` on density with the note corrected and these numbers added, and let the curator settle the scale question (MET-3) that the record leaves open. The alternative with a precedent is `Metric.from_context("rmsle", target_transform="log1p")`, as in blood_tests_drink_prediction (a skewed count whose error matters relative to the amount). It stays on the source's density scale and is exactly RMSE on the shipped values.
6. **Kendall tau 0.71-0.79 (P6; row 22, refuted).** On the seven models it is 0.62-0.71; with density-aware fits it is 0.17-0.56. The scales reward different things: log1p rewards the shape, density the calibrated mean. *Changes:* the note's support for "the two scales rank models alike". *Mildest remedy:* correct the numbers and drop "alike".
7. **The regime as the curator's pick (P4, SPLIT-3; row 32, untested).** The grouped split is well argued (map a surveyed year between stations; temporal R^2 is 0.29), but no CC line records the curator choosing it over the temporal alternative the screening raised. *Mildest remedy:* ask in REVIEW.md, one line.
8. **Count and wording slips (writing; rows 3, 15, 20, 30, 31, 40).** 114 station-days and correlation 0.536 (not 123, 117 and 0.55); "0.2-1.5%"; a boat sample is two cores bulked; random stations sit on gridlines; the first Lyashevska quote describes earlier studies; 1,506 rows with mud = 0. *Mildest remedy:* edit the notes; no rebuild of any decision.

**Held and worth saying (tested in both directions):** measured sediment at the station is a small, honest gap. It is worth +0.013 R^2 over no sediment, and the paper's IDW approach scores below no sediment (0.348 against 0.355), so `fit="approximate"` is right and no USE-3 fix would buy realism at a cost worth paying. The 142 station pairs 11-48 m apart are distinct stations (SPLIT-24 forbids threshold clustering), and their same-year correlation (0.54) is near that of 500 m neighbours (0.41). No feature-identical row crosses the split. The dropped sampling columns carry nothing (0.367 against 0.368), and the date adds 0.003 R^2 over the year.

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): wadden_sea_sibes_macoma_abundance**

```text
Verdict: ship after changes: two notes need rewording, and the curator decides one call on the sediment.
Validity: USE-3 / LEAK-10 against LEAK-6 on the measured sediment: a question for the curator (it adds R^2 +0.012,
  almost all of it from the visit's own measurement); LEAK-25: the drop of the 769 empty samples reads the record,
  label included (every dropped row is a tellin zero), so the note "not on the tellin count" is wrong; LEAK-33 holds
  (station is the group, not a feature); LEAK-10 holds for every other column.
Value: none raised by the columns.
Quality: CLEAN-3, CLEAN-9, CLEAN-10, CLEAN-11, CLEAN-14 hold; a target note to add (Tellinoidea spat, USE-5).
For the curator: issue 1 (keep the measured sediment with corrected numbers, or replace it with interpolated sediment).
```

Sources read: dataset.py, the record, the builder report and probes, the SIBES descriptor (Bijleveld et al. 2025,
Tables 1-4, Field sampling, Laboratory analysis, Data validation), Lyashevska et al. 2016 (Materials and Methods),
species.csv. Frame loaded through dataset_io.from_definition: 58,688 rows x 9 columns, regime grouped_non_iid on
`station`. Scripts and outputs are in the run folder (not committed): raw_checks, frame_checks, ablations,
coords, twins, place_groups, tellinoidea. The model numbers come from untuned LightGBM (400 trees, 63
leaves) with R^2 on log1p, over the shipped splits, repeats 0-1 (6 folds), unless a builder number is quoted.

**Column table**

| column | meaning (codebook) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `station` | `sampling_station_id`: "unique identifier of sampling station ... repeatedly visited between years" (Table 2); 4,261 grid, 830 random, 14 both | an id, not an input | category (5,081 levels), cast from int via str; the group column, which `feature_columns` drops | fine; one note on near-twin ids (problem 4) | LEAK-33, LEAK-17 |
| `date` | `date`: "sampling date" (Table 2); June-October; "the aim is to sample each area during the same period each year" (Field sampling) | the year: yes, it is the survey being mapped. The day: a nominal date per area follows from the fixed schedule | datetime64, `%Y-%m-%d`, no missing | fine: the day of year adds only 0.002-0.003 beyond the year (year only -0.0022; the station's median day instead -0.0032); the year carries 0.077 (no date: 0.290 against 0.368) | USE-3, CLEAN-14 |
| `tidal_basin` | `tidal_basin_name`: "name of the tidal basin" (12) | yes: a chart lookup of the position | category; constant per station (0 stations with two values) | fine | CLEAN-14 |
| `tidal_flat` | `tidal_flat_name`: "name of the flat as used on Rijkswaterstaat charts" (41); 18 flats span 2-3 basins (two partitions, not nested) | yes: a chart lookup | category; constant per station | fine (the best single feature, R^2 0.125, as a place attribute should be) | CLEAN-14 |
| `longitude` | `x`: "longitude (decimal degrees east, wgs84)" | yes | float64; one value per station; no two station ids share a coordinate | fine | CLEAN-14 |
| `latitude` | `y`: "latitude (decimal degrees north, wgs84)" | yes | float64; one value per station | fine | CLEAN-14 |
| `median_grain_size_um` | "median grain size of the sediment in µm"; a 33 mm jar, 4 cm deep, taken just before the fauna core at the same visit, laser diffraction (Field sampling, Laboratory analysis) | **not as measured**: a place without a sample has only an interpolated sediment map (Lyashevska: "the covariate must be known everywhere"; IDW) | float64; range 6.66-389.3, nothing impossible; 3,344 missing (2,703 of them in 2008 by design, "a 1000-m grid"; 641 later), kept missing; the 6 conflicting duplicate ids set missing (reasonable) | question for the curator (problem 1) | USE-3, LEAK-10 vs LEAK-6, USE-8 |
| `mud_percent` | "percentage of the sediment sample with grain size < 63 µm" (volume %), same jar | as above | float64; 0-100; 0 means sand (1,534 rows, median grain 150-308 µm), 100 means mud (2 rows, 6.7-11.7 µm); consistent with the grain size in every row (none above 50% mud with a median grain over 63 µm, and none the other way); missing in the same rows as grain size | as above | as above |
| `log1p_macoma_per_m2` (target) | Macoma balthica (`sibes_id` 59) `abundance_m2`, standardised for core area and subsampling (Table 4), zero-filled by the join the descriptor names | the outcome | float64, log1p, named after the transform; 26,016 Macoma rows, none ≤ 0 or NaN, no repeated (sample, taxon) pairs, so every zero is the absence of a row; max 99,780 per m2 (2014 spat, "extreme abundances ... double checked", kept) | fine as built; a note to add (problem 3); the 769 dropped rows are problem 2 | CLEAN-16, USE-5, LEAK-25 |
| dropped `sample_id` | "unique identifier of sample" | no meaning | dropped | fine | CLEAN-3 |
| dropped `sampling_type` | "grid or random sampling station" | no: a place between stations is neither | dropped | fine | USE-3 |
| dropped `platform` | boat or walk; "stations close to shore were often accessed by foot, as these relatively elevated sites could not be easily reached by boat" (Field sampling): a rough stand-in for elevation, but it changes between years at 908 stations | no: it is a property of the visit | dropped; R^2 0.365 with and without it (builder, holds in exp_features.csv) | fine | USE-3 |
| dropped `total_surface_m2` | the core area (0.0173 boat, 0.0177 walk, 0.0087 for 41 half cores) | no: a property of the visit | dropped; the target is per m2 already | fine | USE-3 |
| not shipped: the other taxa and AFDM of biota.csv | measured in the same core as the target | no | not shipped | fine | LEAK-10 |
| absent: elevation | the paper's third covariate (Rijkswaterstaat altitude) | yes, from a bathymetry map | not in the release; a join would be ours (CLEAN-19, as mortgage's FRED join) | open in the builder's issue 2; I did not test it | CLEAN-19 |

**Problems, ranked (principles.md: rank, then strength, then size)**

**1. The measured sediment is a value from the visit, which the prediction point excludes (P3/P4; USE-3 and LEAK-10,
Must, against LEAK-6's "a slight optimism with a known cause can stay with a note"; USE-8 for how it is named).** A
question for the curator. The two sediment columns come from a jar taken a moment before the fauna core at the same
spot. The task question is "a place ... that was not sampled", but `known` says "measured at the station".
Evidence (6 shipped folds):

| feature set | R^2 log1p | against shipped | folds below shipped |
|---|---|---|---|
| shipped (place, date, measured sediment) | 0.368 | | |
| the station's own sediment from its other years instead | 0.358 | -0.010 (SE 0.002) | 6/6 |
| no sediment | 0.356 | -0.012 (SE 0.002) | 6/6 |
| sediment interpolated from the 8 nearest other stations of the year (builder, its own 6 folds) | 0.349 | -0.016 | 6/6; and below "no sediment" in 6/6 (-0.004) |

So the sediment's whole contribution is the visit's own value. The interpolated map is worth nothing beyond the
coordinates, and even the place's persistent sediment (its own other years, more than a map could know) recovers
only 0.002 of the 0.012. Bullet 1 and `fit_reason` give the gap as "0.365 against 0.349", against a feature that does
worse than no sediment at all, so they hide that the measured value is the only reason the sediment helps. The
mechanism is circumstantial (EV-6), and three readings cannot be told apart: the jar and the core share a patch; the
spot changed since last year; or the fauna changed the top 4 cm. The effect is small (3% of the score) either way.
On each side: Lyashevska et al. 2016 calibrate on the stations and map with IDW-interpolated sediment, and an IDW
surface passes through its data points, so the paper's own leave-one-out probably saw near-measured values too (not
shown). The sibling noaa_afsc_bottom_trawl_survey_cpue ships the bottom temperature measured during the haul, because
its source trains on covariates "collected in association with the catch". There, though, the question names the
measured values ("given ... the depth and temperatures measured there").

The mildest remedy: keep the columns. Restate bullet 1 and `fit_reason` with all three numbers (0.365 measured, 0.353
none, 0.349 interpolated; or this table's 0.368, 0.356, 0.358), saying the gain comes from the visit's own
measurement. Then align the question with `known`, for example "at a place where no fauna sample was taken,
given the sediment measured there", the way noaa_afsc words it. If the curator reads USE-3 strictly, replace the
columns with the sediment interpolated from the other stations of the same year (CLEAN-19, fourth bullet; the
paper's own covariate), at a cost of about 0.016 R^2, or drop them (-0.012). A third framing (USE-9) is left for the
curator to weigh: a place whose sediment was analysed but whose fauna sample was not. NIOZ's 2017-2018 samples were
"sampled but not processed in the laboratory" for lack of funding, and sediment analysis is the cheap step. That
would make the measured sediment known, but the station's own history would then be known too.

**2. The drop of the 769 samples without any fauna record removes only zeros (P4; LEAK-25, Must; LEAK-22's logic).**
This is the builder's issue 1, and I add two facts. (a) The rule is not "a rule on the recording, not on the tellin
count", as bullet 3 and the decision text say. It reads the whole record, tellin included: a sample with one tellin
would have been kept, and all 769 dropped rows are tellin zeros. LEAK-25's amendment recovers rows "located by a rule
that does not read the label". The 2008 part is still well located by year (9.0% against 0.1-1.5%). (b) Table 1's
"processed" counts equal the samples.csv rows year by year: 2008 3,792 = 3,792; 2009-2016 and 2019-2021 within 4;
2017-2018 were processed later. By the descriptor's own numbers, then, these samples were processed, and the
"2-3%" that "did not lead to an entry" are the 40-140 per year missing from samples.csv. For 2009-2022 (427 rows)
that supports genuine empty cores. Their stations are poorer than average too, with 5.1 taxa on their other visits
against 7.6 (builder's explore2). Dropping those rows deletes true zeros at the barest places. The size is small:
the zero share moves from 56.2% to 55.7%. The remedy is a weighing call: keep the drop, but reword the claim in the
note and the Decision; or drop only 2008 and keep the 427 later empty cores as zeros. Both are milder than any change
to the target.

**3. Unidentified tellinoid spat can hide tellins (P3; USE-5, a target note).** species.csv `sibes_id` 339,
Tellinoidea: "Tellinoidea below 3 mm are classified on the superfamily level. Includes ... Macoma balthica." It occurs
in 71 samples (2015-2022). In 29 of them there is no Macoma row, so they ship as zeros, with 12,553 tellinoid spat
per m2 between them. One of them, sample 113998 (2016, station 3959), holds 9,507 per m2, the size of the 155
densest Macoma samples (≥ 5,000), and under RMSE on the density those few samples weigh most. The descriptor also
says extreme abundances were "corrected or deleted if the mistake was unclear", and a deleted Macoma record turns
into a zero. That cannot be measured. The mildest remedy is a note under the target bullet. An option is to drop the
29 rows as having an unknown target (CLEAN-15), by a rule on another taxon's record, 0.05% of the rows.

**4. Near-twin stations under different ids (P4; LEAK-17 / SPLIT-24, minor; for the split auditor).** 142 pairs of
station ids lie 11-48 m apart, mostly a grid station and its random companion (134 grid-random pairs), sampled in the
same years (139 pairs). Their same-year log1p correlation is 0.54, like the 117 grid-random pairs that share one
station id (0.55). They cover 279 stations and 3,134 rows (5.3%), and the grouped split can put one twin in training
and the other in test. Grouping by place instead (stations under 50 m merged, 4,940 groups) changes R^2 by
+0.0016 (SE 0.0047, 9 folds). On the twin rows it is 0.384 against 0.369. This is defensible under the use case, since
a map node 30 m from a sampled station does know that station's fauna, but it is not consistent with the 117 pairs
held in one station. Remedy: a sentence in the note on station-days; no change to the split.

**Checked and fine (no action)**

- Missing sediment after 2008 does not encode the outcome. Presence is 0.510 where it is missing against 0.451 where it
  is present (n = 641); within a station, +0.032 against its other visits, about 1.6 SE. The missing indicator alone
  gives R^2 0.003 (leak probe). In 2008 the missingness follows the 1000-m sediment grid (the design).
- `date` against the dropped visit columns: the definition drops `platform` and `sampling_type` as properties of the
  visit (USE-3) but keeps the visit's date. That is consistent enough, because the year is the survey being mapped
  and the day within the year is worth 0.002-0.003. No change.
- No proxy missing codes (CLEAN-10), no impossible values (CLEAN-11), no object columns (CLEAN-9), dtypes by meaning
  (CLEAN-14). Coordinates, basin and flat are constant within a station, and no id encodes the label.
- The 1 exact duplicate and the 2 conflicting rows of the bundle checks are grid-random cores of one station-day, so
  they always land in one fold (LEAK-16 decided: replicate cores, kept and noted).

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): wadden_sea_sibes_macoma_abundance**

**Verdict: right with notes.** The use case and the source both call for grouping by station, and the station id is a true group id. Against the map the use case draws, the split errs on the strict side. There are two notes on the definition, both P4: what a new place knows about its sediment, and the moment of the map (later surveys sit in the training side). A third point goes to the metric auditor. No re-split is needed.

```text
Validity: USE-10 / SPLIT-3 hold (a new place, grouped; the source's map is within surveyed years); SPLIT-24 holds
(the source's sampling_station_id, fixed coordinates); SPLIT-23 concern (measured sediment at the held-out station,
issue 1); the moment of the map is unnamed, later surveys train the early years (issue 2); SPLIT-29 holds.
Value: SPLIT-28 holds (every family above the mean on unseen stations; all 9 folds beat the dummy on density too).
For the curator: issue 1 (interpolated or measured sediment), issue 2 (archive map or map after each survey).
```

**Where the numbers come from (EV-8).** I rebuilt the definition's frame and its shipped 3x3 station-grouped splits from the V6 raw files with `dataset_io.from_definition`: 58,688 rows, 5,081 stations. The model is an untuned LightGBM (400 trees, learning rate 0.05, 63 leaves) on the shipped features, with the date read as year plus day of year. R^2 is on log1p, as in the probes; RMSE is on the density, the shipped metric. The 9 shipped folds are used unless stated otherwise. The alternative splits use 3 folds and one repeat. The year experiment uses repeat 0. Scripts and outputs are in the run folder (not committed): s1-s6.

**What I checked, with numbers**

- **Regime (USE-10, SPLIT-3): grouped is right.** Lyashevska et al. 2016 use the model "to make predictions for sites where only environmental data are available" (Abstract) and judge it by leave-one-out over the locations of one survey. That is a new place in a surveyed year, not a future year. I measured the alternatives:
  - Expanding temporal windows (train on the years before, test one year) score R^2 0.139 (2019), 0.276 (2021) and 0.332 (2022), mean 0.249. This matches the record's 0.28 on 2021-22.
  - A known-station framing (the station's previous-year mean as a feature) adds nothing: 0.224.
  - So no warm-start use case is being given up. The family precedent `nantucket_sound_sea_duck_aerial_survey_counts` (grouped by segment, "a map of the surveyed days") made the same call.
- **Group id (SPLIT-24, SPLIT-26): true.** The group is `sampling_station_id` from samples.csv.
  - Coordinates are constant within every id (SD 0 m at the 100th percentile).
  - No two ids lie within 10 m. 279 ids have another within 50 m: these are the design's random stations, "placed at random distances from grid sampling stations" (descriptor), median 130 m from their nearest station.
  - No station is on both sides in any of the 9 folds. Each fold holds 1,693-1,694 test stations and 19,400-19,702 test rows.
- **What one prediction is (SPLIT-23).** A row (a core), `context="none"`, labels per sample. This matches the paper's per-location leave-one-out.
  - The 117 grid-plus-random pairs at the same coordinates and day share one station id, so each pair stays in one fold.
  - 64.8% of the stations are sampled in 13-15 of the 15 years, so "most" holds.
- **Hidden groups and near copies (SPLIT-29, SPLIT-30).** The tests that would apply to an IID split:
  - IID rows: 0.389. Station-year groups, where the station's own other years are in training: 0.391. Shipped: 0.368.
  - The station's own record is worth 0.023, and the split removes it. This supports the definition's "holding a station out in every year is stricter".
  - The builder's probe gave 0.371 against 0.353 (a gap of 0.018).
- **Distance: the test set against the map.** For a test row, I took the distance to the nearest training station sampled in the same year. For the map, I took uniform points in the 500 m cells of each year's stations, with every station in training.

  | | 10% | 25% | median | 75% | 90% |
  |---|---|---|---|---|---|
  | shipped test row to nearest training station of its year (m) | 146 | 482 | 500 | 511 | 523 |
  | the paper's leave-one-out, station to nearest other station (m) | 100 | 289 | 500 | 500 | 511 |
  | map pixel to nearest station (m) | 82 | 133 | 192 | 239 | 273 |

  - Error by distance (repeat 0): R^2 0.41 below 100 m (7.3% of test rows), 0.42 at 100-250 m, 0.41 at 250-400 m, 0.36 at 400-600 m (72%) and 0.28 beyond 600 m (6.4%).
  - Reweighted to the map's distance mix, the score is about 0.42 against 0.37. So the station split is somewhat strict for a map drawn between stations, and about as strict as the paper's leave-one-out.
  - The random stations do not make it easy. 7.0% of the test rows have a training station of the same year within 100 m, against 14.5% of map pixels.
- **Alternative groupings, for the record.** Spatial blocks would test maps of areas the survey never covers, which is not this use case. Under them, R^2 falls with the distance to training data:

  | split | R^2 (log1p) | RMSE density (dummy) |
  |---|---|---|
  | shipped: station | 0.368 | 863.0 (875.6) |
  | 1 km blocks (1,509) | 0.338 | 862.9 (872.6) |
  | 2 km blocks (505) | 0.302 | 875.1 (881.0) |
  | 5 km blocks (121) | 0.192 | 847.6 (847.2) |
  | a new tidal flat (flat not a feature) | 0.096 | 871.6 (869.2) |

  The score is mostly spatial interpolation from neighbours 500 m away, which is what the map does.
- **The date: known for a new place.** The notes drop `platform` and `sampling_type` because "an unsampled place has no visit", yet they keep the visit's date. I measured whether that matters:
  - Replacing each test row's day with the day of the nearest training station sampled that year changes R^2 by -0.0003 (SE 0.0001).
  - Keeping the year only: -0.002. No date at all: -0.077.
  - So the date carries the survey year and the survey's route, both known for a map pixel. A clause in the prediction-point bullet would remove the apparent inconsistency.

**Issues, in rank order**

**Issue 1 (P4; USE-3 and SPLIT-23, Must, a weak instance): a held-out station keeps its measured sediment, which a place without a sample would not have.** Lyashevska et al. interpolate it for exactly this reason ("To be used as a predictor in mapping, the covariate must be known everywhere in the study area. Therefore, the mass fraction of silt and median grain size were interpolated using by inverse distance weighting", Materials and Methods). On the shipped folds, using inverse-distance-weighted (IDW) sediment from the 8 nearest other stations of the year:

| sediment input | R^2 (log1p) | change | paired SE | RMSE density |
|---|---|---|---|---|
| measured, as shipped | 0.368 | | | 863.0 |
| no sediment | 0.355 | -0.013 | 0.001 | 863.7 |
| IDW in train and test | 0.349 | -0.019 | 0.001 | 863.4 |
| measured in train, IDW at the test station (a model fit on stations, applied to the map) | 0.338 | -0.030 | 0.001 | 862.1 |

- At a real unsampled place, the sediment map adds nothing over position: 0.349 and 0.338, against 0.355 without sediment. So the measured sediment's whole gain (+0.013 to +0.030) comes from a value the use case lacks.
- The notes report only the smallest comparison (0.365 against 0.349).
- On the density metric the difference does not show (862-864 against a dummy of 875.6).
- The builder raised this as draft issue 2 and recommends keeping the measured sediment.
- Mildest remedy, the curator's call:
  - (a) Ship the sediment interpolated from the other stations of the year, the source's own covariate. It uses no label, so it is not a transductive leak.
  - (b) Keep the measured sediment. Rewrite the prediction-point bullet with all three numbers and as a kept potential leak, and name it in `fit_reason` as kept, not as a gap (USE-8).
  - I lean to (a), because P4 outranks the small loss of signal and the source does the same. But the effect is small, so (b) is defensible.

**Issue 2 (P4; the moment of the prediction point, USE-1 and USE-3; SPLIT-9's wording if the map is made right after each survey): the training side holds the surveys after the test year.** A held-out station of year Y learns from its neighbours in every year, up to 14 years later. Repeat 0, training on:
- all years (shipped): 0.368;
- years up to Y: 0.345;
- year Y only (the paper's single-survey design): 0.250.

The gain is concentrated in the early years: 2008 0.377 against 0.262, 2009 0.322 against 0.225, 2010 0.323 against 0.273, 2011 0.347 against 0.313. From 2017 on it is at most 0.006.
- For an archive map of a past survey (the source's use; Lyashevska mapped 2010 years later), the later surveys are known and the split is right.
- For the example decision in `use_case`, "to judge food stocks for birds" right after a survey, they are not known.
- Mildest remedy: name the moment as a map of a past survey drawn from the whole archive, in `task_summary.split` and `splits_comment`, with the 0.368 against 0.345 cost and the years it falls on.
- A fold-level fix within one grouped regime does not exist (SPLIT-3). Restricting the data to 2017-2022, where the effect vanishes, would cost about 60% of the rows. I do not recommend it.

**Issue 3 (P4 note; SPLIT-1, the comment's accuracy): the split is strict for the map, and the comment could say so.** "Neighbours a few hundred metres away" holds: the nearest training station of the same year is at a median of 500 m. But map pixels lie at a median of 192 m (90% within 273 m), and near test rows score higher. The score therefore errs low for the map (about 0.42 against 0.37 reweighted). Remedy: one sentence in `splits_comment`. No re-split, and spatial blocks would answer another question.

**Issue 4 (P6, for the metric auditor; MET-3 and MET-10): the folds score the 2014 spat patches.**
- All eight densest samples (28,116-99,780 per m2) are from 2014. Station 4341 (99,780 per m2) lands in a different fold in each repeat.
- Per-fold density RMSE ranges from 580 to 1,165, and density skill per fold from 0.015 to 0.051.
- The temporal windows, which lack such a year, have RMSE of about 230.
- The density metric does not separate the sediment variants of issue 1 (862.1-864.1).
- The folds themselves are balanced. This is a metric-scale question, not a split one.

**Claims checked**
- `task_summary.split`: holds (no station overlap in 9 folds; neighbours at a median of 500 m).
- `Grouping.definition`: holds. 5,081 stations; 64.8% sampled 13-15 times; the per-year leave-one-out analogue is stricter here, at 0.368 against 0.391 with the station's own years.
- `splits_comment`: holds. It lacks the later-surveys point (issue 2) and the pessimism point (issue 3).
- The `curation_comments` note on 123 station-days ("both kept, in one fold through the station"): holds.
- The prediction-point bullet, R^2 "0.365 against 0.349": reproduced at 0.368 against 0.349, but not the realistic comparison (issue 1).
- The builder's group probe, IID 0.371 against grouped 0.353: the gap is consistent at 0.021 with a larger model.
- The record's "0.28 on 2021-22 as a temporal test": consistent (0.276 for 2021, 0.332 for 2022).

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner (actor: a benthic ecologist or Wadden Sea manager mapping Baltic tellin densities between SIBES stations in a surveyed year)**

**Fit: approximate (agree with `fit="approximate"`).** This is the paper's own task: predict the tellin density at a place between the stations of a survey year that has already been run. The held-out stations, with that year's other stations in training, stand in for that place. Three gaps keep it from direct: sediment measured at the station rather than read from a map, no elevation (which every mapper uses), and no named decision taken on the map (USE-1, USE-8). USE-9 does not apply: the gaps are in the inputs, so no rewording of the use case would remove them.

**How the job is done today.** SIBES samples a 500 m grid plus random stations once a year, June to September. Maps between stations are geostatistical: kriging with an external drift on silt, grain size and altitude in Lyashevska et al. 2016, and interpolation of biomass using the spatial autocorrelation in the descriptor's Fig. 4. Population sizes and trends come from the station means, and the effects of gas extraction are judged on the stations themselves (de la Barra et al. 2024). The maps feed studies of shorebird food (prey "landscapes" for red knots), habitat-directive and quality-status assessments, and EIAs. No source names an operational decision taken on the map. The use is real but soft, enough to carry the small cleaning imperfections (the 769 dropped samples, the six duplicated ids).

**1. Inputs at the moment of prediction**
- Position, tidal basin, tidal flat: I have them for any place (GIS).
- Survey year: yes. Day of year: no. A place on the map has no visit date, just as it has no platform or core area, which the builder dropped under USE-3 for exactly that reason. It carries no signal: a Poisson LightGBM with and without day of year scored RMSE on density 866.8 against 869.9, Poisson deviance 355.1 against 357.5 and RMSLE 2.999 against 2.997, all within fold noise. Consistency would mean shipping the year, or naming the date as a visit property kept on purpose.
- Sediment: at a real unsampled place I would read it off an interpolated sediment map, as Lyashevska et al. did with IDW. Here it is measured at the station. The builder measured the cost: R^2 on log1p 0.365 measured against 0.349 interpolated. Small, and named in `fit_reason`.
- Missing, and I would always have it: elevation or inundation time from Rijkswaterstaat bathymetry. It is the paper's third covariate and, with silt, one of the "most important determinants of habitat structure". Its coefficient in model "small" is 0.55 against 0.82 for silt in the Bernoulli part (0.28 against 0.59 in the Poisson part). Its gain on top of the coordinates is not measured. Sediment adds only 0.012 R^2 beyond position (0.365 against 0.353), so the gain may be modest, but this is the biggest input gap. Hydrodynamics and ecotope maps are second-order.
- That year's counts at the neighbouring stations: I would use them directly (kriging). The model sees them only as training rows, so it has to learn a surface for each year from latitude, longitude and year. That is inherent to a tabular task, not a fix to make.

**2. The target.** The number of tellins per m^2, with zeros built from the sample list. It is the paper's quantity, and the population and habitat monitoring use it. For a food-stock decision I would rather map biomass (AFDM g/m^2, ideally the size classes a knot can take). Numbers swing with spatfall. 2014 averages 530 per m^2 against 38-284 in the other years, 12 of the 15 densest cores are from 2014, and the densest holds 1,728 tellins in 0.0173 m^2. Per sample, Macoma numbers and AFDM correlate 0.73 on log1p but only 0.36 raw. The release holds total AFDM per taxon and sample but no sizes, so the harvestable fraction cannot be built. Numbers are an acceptable proxy, but the notes should say why biomass was not used (USE-5, a choice, not a fail). I want a number: the expected density (the paper's "unconditional intensity"), which I can sum to totals for each basin.

**3. Row and test data.** One core is one location in one year, which is the paper's leave-one-out unit. My decision acts on areas: a pixel or a basin in a year. Scoring per core is the only option and matches the source. The test data matches what I would face: whole stations held out in every year, with that year's other stations in training (SPLIT-3, USE-10: a place with no history). It is somewhat harder than a real map. A test core lies a median 498 m from the nearest training core of the same year (10th to 90th percentile 148-521 m), and only 17% have one within 300 m. On the 500 m grid, no pixel is more than 354 m from a station. Measured with station-grouped 3-fold splits; the task_summary's "a few hundred metres" would read better as "about 500 m". The alternatives are rightly not the task. Forecasting next year is research, given swings like 2014. Filling in the stations missed in 2020 (grid at 1000 m) would be a known-entity task with the station's history as a feature.

**4. Would I use the model?** As a first map for a year, yes, if it reproduces the means for each basin and year and the known unimodal response to mud (optimum around 30% silt). A model fit on the shipped log1p target and back-transformed would make me distrust it. Over 141 basin-year cells with at least 100 test cores, it predicts a median 0.20 of the observed mean density (overall 27.7 against 148.9 per m^2), so the food stock comes out five times too small. A Tweedie LightGBM on the density predicts 0.90 (123.4 overall). Under the declared metric the two differ by only 3% (865.8 against 837.2). I would also want per-pixel uncertainty, which the paper reports as a coefficient of variation.

**5. Does the metric score my decision? Partly.** `rmse` after inverting log1p, i.e. on the density, measures the right quantity at the right unit. It ranks models like the paper's MSE on the unconditional count per core (exactly so if the core area were constant; it is 0.0173 m^2 by boat, 0.0177 on foot and 0.0087 in 39 cores). MSE is consistent for the mean, which is what I sum (MET-1, MET-3). The fallback is the right origin under MET-5, because the paper reports accuracies, ME and MSE side by side with no single criterion. MET-6, MET-7 and MET-9 do not apply: there is no threshold, cost or top k, and the paper's prevalence accuracies at 0.5 are habit. The problem is resolution (MET-10). I ran six station-grouped folds (2 repeats x 3) on eight untuned LightGBM variants (log1p fits, back-transformed, with and without smearing; density fits with L2, Poisson and Tweedie objectives), plus the training mean. Results (scripts in the run folder (not committed)):
- RMSE on density: the fold standard deviation is about 236, against 837-907 between models. Three of the seven models rank anywhere from 1st to 8th across the six folds. The training mean beats 3-4 models in 2 of the 6 folds.
- Kendall tau of the per-fold model rankings: between RMSE on density and RMSE on log1p, -0.52 to 0.52 across the six folds; between RMSE on density and Poisson deviance, 0.05 to 0.81.
- The builder's note "The two scales rank the seven models alike (Kendall tau 0.71-0.79)" holds only for models all fit on log1p. Once models that target the mean are in the set, the two scales disagree. That note should be corrected.
- Mean Poisson deviance on density: the ranks are nearly fixed (Tweedie 1st in 6 of 6 folds, Poisson 2nd in 5 of 6). The back-transformed log1p model, the one that gets the means five times too small, comes 7th or 8th of 8 in every fold.
- RMSE on log1p (`rmsle`): ranks that same model 1st in 6 of 6 folds. It would pick the map that understates the food stock fivefold. I would not use it, because it moves the score off the scale the task means (MET-3).

The metric I would choose: `mean_poisson_deviance` on the density. It is consistent for the mean like MSE, so it scores the same expected density. It is the loss of the source's Poisson model, it ranks stably on these folds, and squared error on single spatfall cores does not dominate it. Declaring it would be a context origin (MET-11). It needs a standard scikit-learn metric added to the library with its tests (MET-12, MET-13). It also needs a floor on predictions, since a method that predicts 0 after inverting log1p scores infinity on a positive core. If the curator keeps `rmse` (sibling noaa_afsc keeps RMSE on density, though there it is the source's own metric), the note should name the resolution numbers and the totals bias above.

**Gaps between the dataset and the real decision, ranked by how much they change the task**
1. The metric resolves models poorly on the right scale, and the log scale ranks the wrong model first (P6; MET-10, MET-3). It changes which model wins, not the task.
2. No elevation or inundation input (USE-3, USE-8). Its size is unmeasured; it is the paper's covariate and an input I would always have.
3. Numbers rather than biomass for a food-stock use (USE-5). This is a choice that follows the paper, and the release cannot give harvestable sizes.
4. Sediment measured rather than mapped (USE-3): 0.016 R^2, already named.
5. Day of year kept although a map has no visit (USE-3): no measurable signal, but inconsistent with dropping the platform.
6. Test stations are about 500 m from training cores, against at most 354 m for a real pixel: the test is slightly pessimistic, which is acceptable.

**What an expert in the domain would change**
- Score with mean Poisson deviance on density, or keep `rmse` with a corrected note: the Kendall tau claim limited to models fit on log1p, plus the 0.20 ratio of predicted to observed basin-year means.
- Consider joining Rijkswaterstaat bathymetry (vaklodingen) for elevation, the paper's covariate. If it is not joined, lead `fit_reason` with it rather than with the 0.016 sediment gap.
- Replace `date` with the survey year, or name the date as kept.
- Say in the notes why numbers were taken over AFDM, and that 2014's spatfall dominates numbers (12 of the 15 densest cores).

**Sources**
- Lyashevska, Brus & van der Meer 2016, Ecology and Evolution 6:532-543, https://pmc.ncbi.nlm.nih.gov/articles/PMC4729254/ (Introduction, Materials and Methods, Table 1, Cross-validation, Table 4). Read in full (a text copy in the run folder).
- Bijleveld et al. 2025, SIBES data descriptor, Scientific Data 12:239, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11814293/ (design, Table 1, management uses, Fig. 4 interpolation, the three objectives). Read from a text copy in the run folder.
- de la Barra, Aarts & Bijleveld 2024, J. Appl. Ecol. 61:390-405, https://marineinfo.org/doc/publication/381168 (gas-extraction effects judged on SIBES stations, subsidence and elevation).
- Bijleveld et al. 2018, Sci. Rep. 8:3039, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5813040/ (occupancy does not stand in for abundance or biomass).
- Oudman et al. 2018, Movement Ecology 6:24, https://movementecologyjournal.biomedcentral.com/articles/10.1186/s40462-018-0142-4 (prey maps from benthic grids for red knots).
- My probes on the shipped definition, via `workbench`, untuned LightGBM, station-grouped GroupKFold, seeds 100-101. Scripts and output are in the run folder (not committed): metric_actor, totals, nn, look.
- Builder's probes: exp_metric_scale, exp_features, exp_hurdle and group_probes (in the run folder).

</details>

<details><summary>Blind review</summary>

**Dataset:** `wadden_sea_sibes_macoma_abundance`. Target: `log1p_macoma_per_m2`. Regression, 58,688 rows, grouped by `station`, 3x3 folds.

**Verdict: include with changes.** The data is real and the target is reconstructed exactly from the public source. I found no leakage, and there is real signal well below the noise ceiling. Two preparation fixes are needed: take `station` out of the feature set (keep it only as the group key), and turn the raw `datetime` column into numeric year and day-of-year. The undocumented row drops should also be written down.

**What the task is**

The task is to predict the density of the Baltic tellin (*Macoma/Limecola balthica*, a key bivalve prey of shorebirds) in one SIBES core. The inputs are location, tidal basin and flat, sampling date, and sediment grain size and mud content. The survey is NIOZ's annual synoptic survey of about 4,100 intertidal stations on a 500 m grid plus random stations. It is funded by NIOZ, Rijkswaterstaat and NAM (the gas company). The data paper lists "mapping species distributions" as a design objective, and says "Estimating spatial autocorrelation allows for mapping the distribution of benthic invertebrates." It names uses such as "studying the effects of gas extraction, assessing the European habitat directive … environmental impact assessments."

The station-grouped split matches that use: interpolating density at places that were not sampled, within surveyed years. This is a real, if academic, prediction setting. It is not a forecast, because the model sees same-year neighbours in training.

**Checks that passed**

- **Target reconstruction.** I rebuilt the table from the NIOZ files (`samples.csv` and `biota.csv`; `sibes_id` 59 = *Macoma balthica*; absent species filled with 0). All 58,688 rows matched exactly on station, date and target. The source has 59,463 samples. 769 samples with no fauna record at all were dropped, plus 6 rows with duplicated `sample_id` (see concern 4).
- **Plausible values.** 55.7% of rows are zeros, and the paper reports occupancy 43.8%. One individual per core gives log1p(57.7) = 4.07 for boat samples (0.0173 m²) and 4.05 for walk samples (0.0177 m²). The maximum, 99,780/m² (1,728 animals in a core, Groninger Wad, July 2014), is a plausible spat event in a strong recruitment year: 2013–14 occupancy is 0.58 against 0.30 in 2008.
- **Leakage.** None found. Every column is known at the sampling visit. Sediment comes from a separate 33 mm core taken at the same visit. A station's coordinates, tidal flat and basin never change across years.
- **Copies.** One exact duplicate row. 117 station-date pairs are a grid and a random sample sharing one station ID and identical coordinates. Because the split groups by station, these pairs always land in the same fold.

**Signal (LightGBM, GroupKFold by station, 3 folds, sd(y) = 2.58)**

| Setup | R² |
|---|---|
| All features (year and day-of-year derived, no station ID) | 0.369 (RMSE 2.05) |
| Same, plus `station` as a categorical feature | 0.296 |
| lon/lat/year/day-of-year only | 0.353 |
| lon/lat only | 0.269 |
| sediment only | 0.075 |
| Same-year inverse-distance kNN baseline | 0.32 |
| Whole tidal basin held out | 0.13 ± 0.08 |
| Whole year held out | 0.29 |
| Train 2008–2018, test 2019–2022 | 0.22 |

The noise ceiling comes from the 114 same-station, same-date replicate pairs. Their correlation is 0.54, so explainable variance is roughly 0.5 or less. The task is not trivial and still has headroom.

**Concerns, most serious first**

1. **`station` is in the table as a 5,081-level categorical and will be used as a feature unless excluded.** Under a station-grouped split every test station is unseen, so the column carries no usable information. It cost LightGBM 0.07 R² (0.369 → 0.296), and any one-hot or target encoding wastes effort on it. *Change:* keep `station` only as the group key and drop it from the features.

2. **`date` is a raw `datetime64` column.** Many tabular pipelines drop or mishandle datetimes. Year matters a lot here: Macoma recruitment varies strongly between years (occupancy ranges from 0.30 to 0.58), and adding year and day-of-year raises R² from 0.269 to 0.353. Day-of-year also carries growth stage within the June–October season. *Change:* replace `date` with integer `year` and `day_of_year`.

3. **What the split measures should be stated.** Holding out stations leaves same-year neighbours 500 m away in training. Random stations are closer still: 12.8% of stations have another station within 100 m (minimum 11 m) and 29% within 250 m. So the score measures spatio-temporal interpolation, and a same-year kNN alone gets 0.32. That is honest for the mapping use the survey was designed for. It is much easier than transfer to a new area (0.13) or a new year (0.22–0.29). *Change:* none required, but describe the task as "interpolation within surveyed years". Do not present it as forecasting.

4. **Rows were dropped without documentation.**
   - 769 samples with no fauna records were removed: 1.3% overall, 9% of 2008. The R package's `sibes_merge` would keep them as zeros. Dropping them is probably right: their median mud content is 17.6% against 6.4% for non-empty samples, and muddy sites are rarely azoic, so these look like unprocessed or lost samples rather than true zeros. The paper also notes "sometimes a sample could not be processed".
   - In the 2022 source, 6 `sample_id`s appear twice with conflicting sediment. For example, sample 154828 has 149.8 µm / 4.86% mud on one row and 47.21 µm / 55.6% mud on the other. One row of each pair was kept arbitrarily.

   *Change:* document both filters. For the 6 conflicting samples, set sediment to NaN or drop them.

5. **The target is noisy and has an odd shape.**
   - It is log1p of density for a single core. That gives a spike at 0, then a gap up to 4.05–4.07 for one animal.
   - 2.3% of non-zero samples (608) are below one individual per core, for example 5.77/m² (0.1 animal). This looks like a source-side subsampling-correction quirk.
   - The two platforms map the same count to slightly different values (4.053 vs 4.073).

   None of this is disqualifying on a log scale, but RMSE is dominated by the zero / non-zero split. *Change:* optionally note it, or use log1p(count) instead of density. Otherwise leave as is.

6. **Sediment is measured at the test station during the same visit.** A real map of unsampled locations would need interpolated sediment instead. The effect is small: sediment adds only about 0.016 R² over location and time. It is a standard habitat covariate, so keep it.

7. **Missing values are structural.** Sediment is NaN in 5.7% of rows, mostly 2008 (2,703 of 3,450 rows), because "In 2008 … sediment samples were collected on a 1000-m grid". Leaving NaN is correct. Dropping `platform` (boat/walk) and `sampling_type` loses nothing: adding them changes R² by 0.001. The feature set is thin, with only two environmental covariates and no elevation or inundation time. Expect coordinates to dominate.

**What I could not check**

- The Ecology and Evolution paper (doi 10.1002/ece3.1880) returned HTTP 403, so I did not read it.
- The supplementary material of the data paper.
- Whether the 769 empty samples really are unprocessed rather than azoic. The source does not say.
- Whether the 2017–2018 samples, processed late, followed the same lab protocol.
- The preparation script itself; I inferred the filters by reconstruction.
- I used the current NIOZ download (it covers 2008–2022 and matches the row count exactly).

**Sources**

- https://doi.nioz.nl/dataset/sibes-dataset
- Bijleveld et al. 2025, Scientific Data 12:239 (PMC11814293)
- https://github.com/allertbijleveld/sibes

</details>

<details><summary>Precedent check</summary>

**Precedent check: wadden_sea_sibes_macoma_abundance (precedent-checker, 2026-11-01)**

**Verdict.** The definition follows its precedents on eight of the nine decisions checked. One departs with no fact that
sets it apart: the drop of the 427 samples from 2009-2022 that have no fauna record (LEAK-25 as amended 2026-10-21; P4,
Must). One draft alternative in the builder's issue 3, RMSE on log1p "as an exception", would not be a reasonable
exception under the ranking, because MET-3 is a Must. I found no drift and no third exception.

What I read: the register (1,620 decisions; it holds no MET decisions, so I used the Cases table of metrics.md instead),
the Cases tables of leak_checks, use_case, splits, metrics, provenance and cleaning_features, the records behind the
precedents, the policy calls of 2026-10-30 in the triage summary, and seven sibling definitions of this batch
(noaa_afsc_bottom_trawl_survey_cpue, nantucket_sound_sea_duck_aerial_survey_counts, cape_floristic_region_family_cover,
boreal_postfire_lichen_biomass, pennsylvania_oak_hickory_regeneration_experiment, crms_phragmites_cover,
basque_offshore_bivalve_biotoxins). The siblings are AI drafts the curator has not decided. They show what the batch
does, not precedent, and I name them so like cases get decided together. Checks of my own (samples.csv, biota.csv) are
in the run folder (not committed).

| # | Decision | Rules | Result | Closest precedents |
|---|---|---|---|---|
| 1 | Target: Macoma per m2, zero-filled, shipped as log1p | USE-5, CLEAN-16, MET-3 | consistent | the lead paper's species; forest_fires (2026-10-21); siblings scored on the original scale |
| 2a | Drop the 342 samples of 2008 with no fauna record | LEAK-25 (amended) | consistent | account_debt_south_africa (2026-10-26), mortgage (shipped 2026-10-26) |
| 2b | Drop the 427 samples of 2009-2022 with no fauna record | LEAK-25 (amended) | **departs, no fact given** | fraud_detection_in_electricity_and_gas_consumption ("never by the label", 2026-10-26), mortgage, caracas_cervical_cancer |
| 3 | Drop platform, total_surface_m2, sampling_type, sample_id | USE-3, CLEAN-22, CLEAN-3 | consistent | the exposure reasoning of 2026-10-30 (call 3); AFSC draft |
| 4 | Sediment measured at the station as an input, fit approximate | USE-3, USE-8 | consistent; the stated reason is weak | USE-8 stand-in; no curator precedent; AFSC draft makes the same choice |
| 5 | Grouped by station, all years held out together | SPLIT-3, SPLIT-4, SPLIT-24 | consistent | 5g_energy_consumption (2026-10-14); SPLIT-3 (2026-10-12) |
| 6 | Fallback rmse on the density | MET-5, MET-3, MET-8 | consistent | gallstone_disease, early_stage_diabetes_risk_prediction; forest_fires |
| 7 | Six duplicated sample ids: one row kept, conflicting sediment set missing | CLEAN-1 | consistent | mortgage issue 15 (2026-10-22) |
| 8 | `year = "2024"` | PROV-9 | consistent; the record field needs filling | kickstarter, sf_permit_time; melbourne_housing_market is set apart |
| - | Builder issue 3, the alternative: RMSE on log1p as an exception | MET-3, MET-10 | **not reasonable under the ranking** | - |

Two more choices are also consistent: missing sediment stays missing (USE-7, CLEAN-2), and the 123 station-days with two
samples are kept (SPLIT-26, superconductivity: keep the source's rows).

**1. Target and scale.** Macoma balthica is the lead paper's species (Lyashevska et al. 2016). That is the firmest basis
for a species in the batch; AFSC picked rex sole by probing 22 species. The zeros come from the source's own recipe
(descriptor, Table 4), just as AFSC's come from gap_products and nantucket's from the authors' scripts. Shipping log1p and
scoring the density is MET-3 as Lennart put it on 2026-10-21 ("ship the target on the modelling scale, score on the
original scale"). Precedent: forest_fires (MAE in hectares, shipped as log1p). Every sibling with a transform also
scores on the original scale: nantucket (count), AFSC (numbers per km2), pennsylvania (count), basque biotoxins (ug/kg).
Scoring density rather than count per core changes nothing: the core is 0.01731 m2 by boat and 0.01767 m2 on foot, so
the density is the count times 56.6-57.8 (checked).

**2. Samples with no fauna record (LEAK-25, Must).** Since the amendment (Lennart, 2026-10-21), a dataset counts as
recovered when the unrecorded rows are "located by a rule that does not read the label" and dropped. The precedents:

* caracas_cervical_cancer (shipped 2026-10-15): the patients who skipped a question; 0 positives where 11.8 were
  expected.
* account_debt_south_africa (CC 2026-10-26, Lennart): eight file runs without debt data, dropped as whole runs.
* fraud_detection_in_electricity_and_gas_consumption (CC 2026-10-26, Lennart): the clients "dropped by their last
  invoice date, never by the label".
* mortgage (AI assessment 2026-10-20, shipped by Lennart 2026-10-26): the last rows of 501 loans that leave early
  without an event. The codebook says such exits are censored refinances, so none of the dropped rows is an observed
  "active".
* ghanas_indigenous_intel (retired 2026-10-01): the unrecorded rows could not be located.

In every one of these, the dropped rows were shown to be unrecorded by a fact other than their outcome: a skipped
question, a run without data, an exit date, or a codebook rule for exits.

*2a. The 342 samples of 2008: consistent.* They are 9.0% of that year, against 0.17-1.53% in each later year. They are
spread over all ten basins (3.6-16.0%) and 50 of the 53 sampling days (my check), at stations that average 5.8 taxa. The
year is the recording fact, as account_debt's runs were. A version that never reads the label would drop the whole 2008
survey: 3,792 samples, and only 747 of its 3,450 recorded samples have sediment.

*2b. The 427 samples of 2009-2022: departs, and no fact is given.* Nothing shows that these are unrecorded:

* The descriptor says a sample that could not be processed "did not lead to an entry in the database" (note to Table
  1). By the source's account, then, a sample row without a fauna row is a processed empty core, and the zero-fill
  recipe of Table 4 keeps it.
* The builder's own evidence points the same way: these stations are empty again on 3.3% of their other visits,
  against 0.77% overall.
* The rule that drops them, "no taxon recorded", is the outcome "an empty core", not a fact about the recording. Every
  dropped row is a target zero by construction, so the rule reads the label in the sense of the fraud CC.
* The definition's stated reason ("an empty record cannot be told from an empty core") restates LEAK-25's premise. It
  is not a fact that sets these rows apart.
* What separates this from mortgage: there, an exit without an event cannot be an observed outcome. Here, an empty
  core can.

The effect is small: keeping them gives 59,115 rows with 55.99% zeros, against 58,688 rows with 55.67%. What is at
stake is how the rule is read, not the score. The reflection prompt is at the end.

On the builder's issue 1: its three options match these readings. "Ask NIOZ" is the repair rung (PROV-13, the remedy
ladder). No precedent waited for the source to answer when the rows could be located and dropped (account_debt, fraud,
caracas), and Andrej sent no requests on 2026-10-30 (call 8). Shipping now and keeping the request as a later repair is
therefore consistent.

**3. Dropped columns: consistent.** The target is per m2, so the core area is its exposure. The family's exposure
reasoning of 2026-10-30 says "a target that is already a ratio ... holds its exposure". That reasoning is the AI's
suggestion for insurance under Andrej's call 3, not a rule. Nantucket keeps `transect_km` because its target is a raw
count. The AFSC draft drops gear, effort and vessel for its per-km2 target in the same way. `platform` and
`sampling_type` describe the visit, not the place (USE-3), and the builder's R^2 is 0.365 with them and without them.
They leave for what they are (CLEAN-22). Whether `platform` stands in for inundation, the elevation the release lacks,
is the column auditor's question; the equal R^2 shows it carries no signal we can measure.

**4. Measured sediment as an input: consistent, but the stated reason is weak.** USE-8 names this pattern: "a stand-in
with a known gap, named as such". The definition names the gap in `fit_reason` and keeps the fit approximate. No curator
decision covers a covariate measured with the target standing in for a map layer. The nearest cases:

* AFSC (a draft in this batch) keeps the depth and temperatures measured during the haul, while its source maps from
  rasters. It is the same choice, so decide the two together.
* The stated reason rests on the size of the gap (R^2 0.365 against 0.349). In the curator's decisions the size of a gap
  is not a reason on its own: see the zillow_prize / melbourne_housing_market row (LEAK-7, LEAK-10, Lennart, 2026-10-21:
  "a lookup is not kept merely because removing it changes no score") and SPLIT-4 ("not the size of the gap"). That
  row's mechanism, a value looked up after the outcome, is not this one: the sediment is a habitat property measured
  together with the fauna, not after it.
* If the curator wants a distinguishing fact on record: the paper interpolated by inverse distance weighting, which
  returns the measured value at a sampled station. Its calibration and leave-one-out validation therefore most likely
  used each station's own measurement too. This is my inference; the paper does not say which values it fitted on.
* The alternatives have precedents in which the curator added the input the actor has. For sediment interpolated from
  the same year's neighbours: rain_in_australia (CLEAN-19 amended 2026-10-26, other stations' readings of the same
  morning, taken from other rows of the same release). For an elevation join (the paper's third covariate): mortgage
  (FRED rate joined from outside, 2026-10-22, "this sounds like a good way to make the data better") and
  qsar_bioconcentration (logKOW added, 2026-10-26). CLEAN-19 allows building such inputs but does not require it, so not
  building them is no departure. Still, in those three cases the curator closed the gap rather than noting it, so the
  elevation join is worth offering as an option. The licence of the Rijkswaterstaat bathymetry still needs checking.

No row of the Tensions table covers this case (a covariate measured with the target against the map used at deployment).
The curator's call here and on AFSC becomes that row.

**5. Grouped by station: consistent.** SPLIT-3 (Lennart, 2026-10-12): one regime, the one the use case implies. The
paper maps one survey year between stations and validates by leaving one location out. The decided analogue is
5g_energy_consumption (USE-9, Lennart, 2026-10-14): a split by station fills the gap for stations without measurements.
The station id is the source's own (SPLIT-24).

The AFSC draft is temporal because its source's maps stand for the years until the next review, and that source
assessed forecasting accuracy. SIBES's source maps the surveyed year, and both definitions write down that difference.
Nantucket, cape_floristic, boreal and pennsylvania (all drafts) also group on place. cape_floristic groups on a coarser
block because its test site stands for an unsurveyed cell. Here the neighbouring stations are surveyed when the map is
made (it fills between grid nodes 500 m apart), so the station is the right unit.

One open point, not a departure: the record left the regime as "the curator's pick", and the CC of 2026-10-30 set only
the verdict and the priority. Grouped is still the AI's pick and needs the curator to confirm it.

**6. Fallback rmse on the density: consistent.** Under MET-5, the paper reports overall, user's and producer's accuracy,
ME and MSE, and names no criterion; in its Table 4 the two models even swap rank between conditional and unconditional
intensity. This matches gallstone_disease (proposed) and early_stage_diabetes_risk_prediction. forest_fires differs
because its paper ranks by one criterion (MAD). The density scale is MET-3. A small signal on the scored scale is no
reason to change the scale: forest_fires was kept with R^2 0.013 (TP-2, 2026-10-06), and there the mean predictor
scores the best RMSE.

On the builder's issue 3: keeping the density is consistent. Its alternative, "RMSE on log1p as an exception", is not
reasonable under the ranking:

* MET-3 is a Must, and an exception can only depart from a Should. MET-10, which the issue weighs against it, is a
  Weigh factor and never overrides a Must.
* A log scale for this family would be an amendment of MET-3. It would reopen nantucket, pennsylvania and basque
  biotoxins, which are drafts with the same heavy tail (in nantucket, 1-2 of about 2,600 test rows hold half the squared
  deviation). AFSC would keep RMSE on numbers as its source's metric (MET-4, MET-5).
* The source's own MSE is on counts, so a context metric on the log scale (MET-11) has no basis either.
* The insurance suggestion of 2026-10-30 (the Gini instead of RMSE on raw amounts, for the same heavy-tail problem)
  rests on that domain's standard metric. These abundance-mapping sources have none, and that is the fact that sets the
  two families apart.

**7. Duplicated sample ids: consistent.** One row is kept and the conflicting values are set missing, as in mortgage
issue 15 (Lennart, 2026-10-22: "make ... the conflicting balances missing").

**8. Year: consistent; the record needs updating.** PROV-9 says a source that grows over time takes the year of the
snapshot we pin, and the descriptor says SIBES "will be updated, and data will be made available online yearly". This
matches kickstarter and sf_permit_time (in the working copy) and the crms_phragmites_cover draft.
melbourne_housing_market (Lennart, 2026-10-22) is different: a single Kaggle upload that grew over its versions, which
takes its first version's year. SIBES is an ongoing monitoring programme. House rule: the record has no `year` field,
and its screening line "so `year` stays empty" contradicts PROV-9. Set the record to 2024, as in the definition.

On the builder's issue 4 (mirror the V6 files): no rule or precedent covers it. The growing sources in the working copy
pin by date and do not mirror. This is a house question for the curator, not a consistency one.

**Drift and third exceptions.** None found.

* Andrej's decisions that touch these rules are the CC of 2026-10-30 and policy calls 1, 3 and 8. He has no earlier
  decision on LEAK-25, MET-3 or USE-3 to drift from.
* Lennart's path on LEAK-25 (retire 2026-10-01, amend 2026-10-21, apply 2026-10-26) is a deliberate amendment, not
  drift.
* No rule here has a second exception of the same kind. These decisions do not touch the register's CLEAN-19
  "amendment due" flag: building the interpolated sediment would apply bullet 4, not depart from it.

**Like cases to decide together (batch).**

* Co-measured covariates: SIBES's sediment and AFSC's haul depth and temperatures (item 4).
* Metric scale for heavy-tailed abundance: SIBES, nantucket, pennsylvania and basque biotoxins (item 6).
* The zero-fill check: AFSC and nantucket zero-fill from presence-only tables by their sources' recipes without testing
  for units that have no record of any species (AFSC fetched only rex sole's CATCH). SIBES ran that test and found 2008.
  The same test on those two would keep the batch consistent.
* australian_vehicle_insurance_2004_2005 already fills `accepted_check_warnings` (task_target_value_dominant), which
  add-dataset step 6 leaves to the curator. SIBES leaves it empty, as the step says, and its proposed reason has the same
  form. Check the Australian one.

**Consistency check (AI, 2026-11-01):** the definition drops all 769 samples with no fauna record (LEAK-25 as amended).
For the 427 samples of 2009-2022, this differs from caracas_cervical_cancer (shipped 2026-10-15), account_debt_south_africa
and fraud_detection_in_electricity_and_gas_consumption (CC 2026-10-26, "never by the label") and mortgage (shipped
2026-10-26). There, the dropped rows were shown to be unrecorded by a fact other than their outcome. Here, the rule "no
taxon recorded" is the outcome "an empty core"; the descriptor says unprocessed samples leave no entry; and these
stations are empty on 3.3% of their other visits against 0.77% overall. What sets these 427 apart?
(a) The descriptor's account is shown wrong for 2008, so it vouches for no year. 2009 and 2017 (1.5% each) sit above
the latest years (0.2-0.5%), so the recording is recovered for no year. The rule reads the whole core (171 taxa), not
the tellin count, and it costs 0.3 points of zero share. Recorded as the distinguishing fact under LEAK-25.
(b) Treat them like the precedents: keep the 427 as observed empty cores (the recipe of Table 4) and drop only by a
fact about the recording. That means either the 342 samples of 2008, or the whole 2008 survey for a rule that never
reads the label (3,792 samples; 747 of the recorded ones have sediment).
(c) No precedent to reopen: the label-blind rules of the precedents would drop nothing more under (a).
(d) Amend LEAK-25 to say when a rule that locates unrecorded rows may depend on the outcome being null.

**Files.** The definition and the record of this dataset; the precedent records of mortgage,
account_debt_south_africa, fraud_detection_in_electricity_and_gas_consumption, caracas_cervical_cancer,
melbourne_housing_market, 5g_energy_consumption and rain_in_australia; the rules and Cases in leak_checks.md
(LEAK-25 and its Mechanisms rows), metrics.md (MET-3, MET-5, Cases), use_case.md (USE-8, USE-9), splits.md,
provenance.md (PROV-9) and cleaning_features.md (CLEAN-19); the family policy calls ("Policy calls of
2026-10-30" in the two-regime zero triage summary); my checks in the run folder (check1: no-record share by year
and core area by platform; check2: 2008 by basin and day; check3: zero share under the LEAK-25 variants).

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: wadden_sea_sibes_macoma_abundance (advocate, 2026-11-01)**

**Position: ship after changes.** The task, the split and the inputs are valid. The real problems the panel found are
in one drop, the framing of one input and the notes. Each has a fix on rung 2 or 3 of the remedy ladder (fix the
definition, or keep with a note), and none needs exclusion.

```text
Verdict: ship after changes.
Validity: SEL-2 holds (CC Yes, 2026-10-30); USE-1 holds, USE-8 approximate (soft decision, no elevation); USE-5
  example reworded; USE-3/LEAK-10 measured sediment kept as a named potential leak, or swapped for IDW (curator);
  LEAK-25 fixed (the 427 later empty cores kept); SPLIT-3, SPLIT-24, USE-10 hold; PROV-9 holds.
Value: TP-2 a real signal (skill 0.355 on log1p); MET-5 fallback and MET-3 hold; MET-10 weighed, notes corrected.
Quality: CLEAN-1 holds; count slips corrected.
```

**1. A real task, the source's own, with the fit already declared approximate (P2, P3; SEL-2, USE-1 and USE-8, Must).**
- Evidence. Lyashevska et al. 2016 say "The model is used for prediction and mapping the abundance of a benthic
  invertebrate" and was "used to make predictions for sites where only environmental data are available". The SIBES
  descriptor names habitat-directive, quality-status and EIA uses. The curator set `Yes`, priority 3 (CC 2026-10-30),
  after deciding that the family's policy question is settled dataset by dataset. The domain practitioner agrees the
  fit is `approximate` and calls the use "real but soft, enough to carry the small cleaning imperfections".
- Against "no decision is named": USE-2 excludes only a task that no decision fits. A soft decision is a known gap
  under USE-8, and `fit_reason` names it.
- Conceded: the food-stock example does not fit a density target (USE-5). Among the positives, density and AFDM agree
  at Spearman 0.32, and the 2014 spat that drive the density hold 1.3% of the biomass. The mildest fix: reword
  `use_case` to the abundance map and the habitat state (the paper's objective), and add a note on why numbers and
  not AFDM (the release has no size classes; the practitioner calls numbers "an acceptable proxy"). The target stays.

**2. The split mirrors the application and errs on the strict side (P4; SPLIT-3, SPLIT-4, SPLIT-24, USE-10, Must).**
- Evidence. The group is the source's own `sampling_station_id`, its coordinates constant within each id, and no
  station falls on both sides in any of the 9 folds. Holding a station out in all years costs 0.023 R^2 against
  station-year groups (0.368 against 0.391). Reweighted to the distances of real map pixels, the score would be
  about 0.42 against 0.37 (split auditor). Temporal windows (mean 0.25) test forecasting, which the source does not
  do. Precedent: 5g_energy_consumption (Lennart, 2026-10-14), a split by station that fills the gap between stations.
- Against "later surveys train the early years" (split auditor, issue 2): the source's map is an archive map
  (Lyashevska mapped the 2010 survey years later), and for an archive map the later surveys are known. The mildest
  fix: name that moment in `task_summary.split` and `splits_comment`, with the cost (0.368 against 0.345) and the
  years it falls on (2008-2011).
- Against the 142 near-twin station pairs: SPLIT-24 forbids grouping by a distance threshold, and merging them moves
  R^2 by +0.0016 (SE 0.0047). No re-split. The regime still needs the curator's one-line confirmation, because the
  CC line names none.

**3. No leak among the inputs. The measured sediment is a small optimism with a known cause, settled by a note or a
cheap swap (P4; LEAK-10, LEAK-6 and USE-8, Must).**
- Evidence that nothing else leaks. The leak probe gives R^2 0.290 for all features, 0.125 for the best single one,
  and 0% exact copies. The dropped visit columns carry nothing (0.367 against 0.368). Replacing a test row's day with
  a neighbour's changes R^2 by -0.0003. `station` is the group column, which `feature_columns` drops (column
  auditor, LEAK-33), so the API already handles the blind reviewer's concern 1. Datetime features are allowed by the
  house format, which answers its concern 2.
- The sediment. It adds +0.012 to +0.030 R^2 on log1p over what a map would give. On the declared metric the
  difference does not show: density RMSE is 862.1-864.1 for every sediment variant, against 875.6 for the dummy
  (split auditor). The sediment is a property of the place, measured with the fauna, not a value recorded after the
  outcome. The paper's IDW surface passes through each station's own measurement, so the paper's calibration very
  likely saw station values too (precedent checker; an inference). The size of the gap is not my reason
  (zillow_prize row, SPLIT-4); the reason is the kind of value it is.
- Conceded: the notes hide that interpolated sediment scores below no sediment (0.349 against 0.355), so the whole
  gain comes from the visit's own value. The mildest fix: keep the columns, restate bullet 1 and `fit_reason` with
  all three numbers as a kept potential leak (USE-8: named as kept, not as a gap), and align the question with
  `known`, as noaa_afsc does. If the curator reads USE-3 strictly, IDW sediment from the same year's other stations
  is a definition fix (CLEAN-19, rain_in_australia), not exclusion.
- Why this outranks a removal: LEAK-6 lets a slight optimism with a known cause stay with a note. The mechanism is
  circumstantial (EV-6: three readings cannot be told apart), and the ladder takes the mildest remedy that works.

**4. Worth benchmarking (P6; TP-2 Should, TP-5 Must, MET-2 Must on computability).**
- 58,688 samples at 5,081 stations. Each test fold holds 1,693-1,694 stations, 19,400-19,702 rows and 8,422-8,955
  positives, and every fold scores.
- LightGBM skill is 0.355 on log1p. It beats the dummy 5/5 and is +0.193 over linear (SE 0.005). The families spread:
  ridge 0.162, kNN 0.215, RF 0.336, LightGBM 0.354.
- Both hurdle stages can be learned (presence AUC 0.81, R^2 0.32 on the positives), unlike forest_fires.
- Replicate pairs correlate at 0.54, which puts the ceiling near 0.5 and leaves headroom (blind reviewer). All 9
  folds beat the dummy on density too (split auditor). Nothing comes near `Too Small` or `Trivial`.

**5. The declared metric is the one the rules give (P6; MET-5 Should, MET-3 Must, MET-8 Should).**
- Evidence. The paper reports overall, user's and producer's accuracy, ME and MSE side by side, and its two models
  swap rank between conditional and unconditional intensity. With no single criterion, the fallback applies
  (gallstone_disease, early_stage_diabetes_risk_prediction). The density is the scale the task means, and MSE is
  consistent for the mean that a practitioner sums to basin totals (domain practitioner).
- Against the resolution objection (MET-10): MET-10 is a Weigh factor and decides nothing alone. The density ranking
  survives dropping the 50 densest rows (tau 0.78-1.0, claim auditor), so it is not just noise. A small signal on
  the scored scale is no reason to change the scale (TP-2; forest_fires was kept at R^2 0.013, where the mean had
  the best RMSE).
- RMSE on log1p as an exception is out. MET-3 is a Must (precedent checker), and that scale ranks first the model
  that understates basin-year means fivefold (ratio 0.20, domain practitioner).
- Conceded: the note's "Kendall tau 0.71-0.79, alike" is wrong. It is 0.62-0.71 on the seven log1p fits and
  0.17-0.56 once density fits are added. Correct it, and add 2014's 75.4% share of the squared deviation and the
  back-transform bias.
- Mean Poisson deviance on density is a fair weighing call for the curator: a context origin that needs a new
  library metric (MET-11 to MET-13), best decided together with the like cases (nantucket, pennsylvania, basque
  biotoxins). No Must requires it, and MET-11 keeps the fallback when the context is not clear.

**6. Faithful data from the first publication, rebuilt exactly (P5; PROV-9 Must; PROV-13 not triggered; CLEAN-1).**
- The source is NIOZ's DOI release (V6) with its Scientific Data descriptor, under CC BY-SA 4.0. The sha256 sums and
  portal byte sizes match.
- The blind reviewer rebuilt all 58,688 rows exactly from the raw files. The zeros follow the descriptor's own
  recipe (Table 4). The six conflicting duplicated ids are handled as in mortgage issue 15.
- Year 2024 follows PROV-9 for a growing source (descriptor: "data will be made available online yearly";
  kickstarter, sf_permit_time). melbourne_housing_market, a single upload, is set apart.
- Fixes: set the record's year to match. Add notes on the 29 cores with unidentified tellinoid spat and on the
  late-processed 2017-18 samples (at most a few hundred values; CLEAN-15 allows dropping the 29 if the curator
  prefers).

**7. The no-record drop: keep 2008's, give back the later 427 (P4; LEAK-25 Must, as amended 2026-10-21).**
- Conceded on the evidence, for 2009-2022:
  - the descriptor's Table 1 "processed" counts include these rows;
  - their stations are empty on 2.8-3.3% of their other visits, against 0.77% overall;
  - "no taxon recorded" is the outcome "an empty core", so the drop reads the label, against the fraud CC ("never by
    the label").
- The 342 rows of 2008 are located by a fact about the recording, the year (9.0% against 0.17-1.53%), as
  account_debt's runs were (precedent checker: consistent).
- The mildest fix: keep the 427 as zeros by the Table 4 recipe and drop only the 2008 samples without a record. That
  gives 59,115 rows and 55.99% zeros; nothing else changes. If the curator wants a rule that reads nothing about the
  core, dropping the whole 2008 survey (3,792 samples, 6.5%) still ships the dataset. Either way, correct the note's
  "not on the tellin count".

**Changes this brief accepts (all notes or small definition edits; no new source needed):** reword `use_case` and
add the numbers-over-AFDM note; name the archive-map moment in the split text; restate the sediment with all three
numbers as a kept potential leak (or swap to IDW, the curator's call); correct the metric note; keep the 427 later
empty cores; align the record's year; fix the count slips (114 station-days, correlation 0.536, "0.2-1.5%", 1,506 rows
with mud = 0, a boat sample is two cores bulked); add the Tellinoidea and 2017-18 notes; have the curator confirm the
grouped regime.

</details>

<details><summary>Critic</summary>

**Critic, opening brief: wadden_sea_sibes_macoma_abundance (critic, 2026-11-01)**

**Verdict: do not ship as defined. Ship after the changes below.** The task is real. It is the source's own
abundance map, and the curator marked it `Yes` on 2026-10-30. Nothing here calls for exclusion. But the definition
breaks three Must rules as written, and each can be fixed in the definition:

* The use case names an example and a moment that the target and the split contradict (USE-1, USE-5).
* The held-out "unsampled place" keeps a measurement it could not have (USE-3, LEAK-10).
* 427 observed zeros are dropped by a rule that reads the outcome (LEAK-25).

The metric is a weighing call, and several notes state things the data refutes.

```text
Verdict: ship after changes.
Validity: USE-1/USE-5 triggered, fix the wording (point 1); USE-3/LEAK-10 triggered, fix by interpolated sediment
  (point 2); LEAK-25 triggered for 2009-2022, fix by keeping the 427 zeros (point 3); SPLIT-3, SPLIT-24 hold.
Value: MET-1/MET-2 against the fallback rmse, a weighing call (point 4); TP-2 keep.
Quality: notes refuted by the data (point 5); CLEAN-15 on 29 tellinoid-spat rows (point 6).
For the curator: point 4 (metric), point 7 (record).
```

**1. The use case names no decision. Its one example contradicts both the target and the split (P3; USE-1 Must,
USE-5 Must, USE-3 Must for the moment).**
- *Problem.* `use_case` gives "to judge food stocks for birds" as the example and says no source names the decision.
  That example implies two things: a map made right after a survey, and a quantity birds eat.
  - The target is numbers, not food. Among positives, Spearman density against AFDM is 0.32. The 50 cores above
    10,000/m2 (36 of them from 2014) are spat: median 0.84 mg AFDM per individual, against 9.3 mg for all positives.
    They hold 11.8% of the individuals but 1.3% of Macoma biomass, and they set the density metric (claim-auditor
    row 2; the domain practitioner would map biomass for this use).
  - The training side holds the later surveys. A test station of year Y learns from neighbours up to 14 years
    later. R^2 is 0.368 with all years, 0.345 with the years up to Y and 0.250 with year Y alone. The gap sits in the
    early years: 2008 0.377 against 0.262, 2009 0.322 against 0.225, and at most 0.006 from 2017 on (split-auditor
    issue 2).
- *Effect.* The benchmark scores an archive map of a past survey, drawn with up to 14 later surveys. It does not
  score the post-survey food-stock map the use case names.
- *Remedy (fix the definition, wording only).*
  - Write the use case as the source's objective: "map the abundance" of a past surveyed year from the whole
    archive, for habitat-directive or quality-status assessment (descriptor; Lyashevska et al. 2016, Introduction).
  - Drop the food-stock example.
  - Name the moment in `task_summary.split` and `splits_comment`, with the 0.368 against 0.345 cost.
  - No re-split. With that wording, density is the quantity the actor maps, and USE-5 holds.

**2. The held-out place keeps its own measured sediment, which a place without a sample cannot have (P3/P4; USE-3
Must, LEAK-10 Must, LEAK-6 Must "a confirmed leak goes even when small"; USE-8 Must for `fit_reason`).**
- *Problem.* The question is "a place ... that was not sampled". The two sediment columns come from a jar taken just
  before the fauna core, at the same visit. The source interpolates sediment for exactly this reason: "To be used as
  a predictor in mapping, the covariate must be known everywhere in the study area" (Lyashevska, Materials and
  Methods; IDW).
- *Evidence.* All of the sediment's gain comes from the visit's own value. Column auditor, 6 shipped folds:

  | sediment input | R^2 |
  |---|---|
  | measured (as shipped) | 0.368 |
  | the station's own sediment from its other years | 0.358 |
  | none | 0.356 |
  | IDW from the 8 nearest other stations of the year | 0.349 |

  Each comparison is 6/6 folds. A model fit on measured sediment and applied to IDW sediment at the test station
  scores 0.338 (split auditor, -0.030, SE 0.001).
- *Not disclosed.* Bullet 1 and `fit_reason` report only 0.365 against 0.349. They hide that interpolated sediment
  scores below no sediment at all, so the measured value is the whole reason sediment helps.
- *Effect.* R^2 is 0.013 to 0.030 too optimistic, from an input that does not exist at the prediction point.
  `fit_reason` calls this a gap, but USE-8 says a kept leak is named as kept.
- *Remedy (fix the definition).*
  - Replace both columns with the sediment interpolated from the other stations of the same year. That is the
    source's own covariate. It reads no label, and it is built from other rows of the same release (CLEAN-19, as in
    rain_in_australia). It costs about 0.016-0.019 R^2.
  - Only if the curator keeps the measured values: reword the question to "given the sediment measured there", as
    noaa_afsc does. Then write it in the notes and `fit_reason` as a potential leak kept on purpose, with all three
    numbers.
  - Rewording only to excuse a gap counts against it (USE-9). Decide together with noaa_afsc's haul covariates.

**3. 427 observed empty cores from 2009-2022 are dropped by a rule that reads the outcome (P4; LEAK-25 Must as
amended 2026-10-21).**
- *Problem.* The definition drops all 769 samples that have no fauna record. Bullet 3 and the Decision say this is
  "by a rule on the recording, not on the tellin count". But every dropped row is a Macoma zero, and "no taxon
  recorded" is the outcome "an empty core".
- *Evidence.*
  - Descriptor Table 1's "processed" counts equal the samples.csv rows in every year (2008: 3,792 = 3,792; the
    others within 4; 2017-18 were processed later). Its note says an unprocessed sample "did not lead to an entry in
    the database" (checked in the descriptor's text). So NIOZ counts these rows as processed samples (claim-auditor
    row 16, column-auditor problem 2).
  - Their stations are empty on 2.8-3.3% of their other visits, against 0.77% overall. They hold 5.1-5.8 taxa
    against 7.6. These are the barest places, where empty cores are expected.
  - In every precedent the dropped rows were shown to be unrecorded by a fact other than the outcome:
    caracas_cervical_cancer, account_debt_south_africa, fraud_detection_in_electricity_and_gas_consumption ("never by
    the label") and mortgage (precedent checker, item 2b: departs, no fact given). For 2008, the year is such a fact:
    9.0% of samples have no record that year, against 0.17-1.53% in each later year.
- *Effect.* True zeros are removed at the barest stations, a selection on the outcome. The zero share would be
  55.99% with them and is 55.67% without. The score barely moves; what is at stake is the rule.
- *Remedy (fix the definition).*
  - Keep the 427 samples of 2009-2022 as zeros (the Table 4 recipe).
  - Drop only the 342 samples of 2008, located by year. If the curator wants a rule that never reads the core, drop
    the whole 2008 survey instead (3,792 samples; only 747 of its recorded samples have sediment).
  - Rewrite bullet 3 and the Decision with the Table 1 match and the base rates.

**4. RMSE on density scores the 2014 spatfall and the back-transform more than the map (P6; MET-1 Must and MET-2
Must, third bullet; MET-10 Weigh). Not a reason to exclude (TP-2, forest_fires).**
- *Evidence.*
  - 2014 holds 75.4% of the squared deviation, and the top 10 rows hold 58%.
  - LightGBM on log1p reaches R^2 0.030 on density, and 2 of 7 untuned models lose to the training mean. A single
    smearing factor (x3.79) lifts R^2 to 0.070 (claim-auditor row 28).
  - The fold SD is about 236, against 837-907 between models. Three of seven models rank anywhere from 1st to 8th
    across folds.
  - A back-transformed log1p model predicts basin-year means at 0.20 of the observed (food stock five times too
    small), yet scores only 3% worse than a Tweedie fit (865.8 against 837.2) (domain practitioner).
  - "Ranks as the paper's MSE" is untested. V6 does not reproduce the paper's 2010 counts: variance 97.5 against 24,
    maximum 455 against 84 (row 26).
  - The note's "Kendall tau 0.71-0.79" is false. It is 0.62-0.71 on the seven models and 0.17-0.56 once fits that
    target the mean are added (row 22).
- *Effect.* The leaderboard rewards calibrating the mean on a few spat cores more than drawing the map.
- *Remedy (a weighing call for the curator).*
  - The floor is (b): keep `rmse` and correct the note. Drop the tau claim. Add the resolution and basin-total
    numbers. Say "ranks as the paper's MSE" only by construction.
  - The alternative is (a): `mean_poisson_deviance` on density as a context origin (MET-11). It stays on the scale
    MET-3 requires, it is consistent for the mean, and it is the loss of the source's Poisson model. It ranks
    stably: Tweedie 1st in 6/6 folds, and the 5x-biased model 7th-8th in every fold. It needs a library metric with
    tests (MET-12, MET-13) and a floor on predictions.
  - Not RMSE on log1p. MET-3 is a Must, and RMSE on log1p ranks the biased model 1st in 6/6 folds.
  - Decide with nantucket, pennsylvania and basque biotoxins.

**5. Several notes say what the data refutes (writing; EV-6, EV-8, EV-9 Should).**
Points 2, 3 and 4 each carry one: the selective sediment comparison, "not on the tellin count" and the tau claim.
Further:
- On the shipped rows, 114 station-days hold two samples, all grid and random, with correlation 0.536. The note's
  123, 117 and 0.55 counted raw rows.
- The later years run "0.2-1.5%", not 0.1-1.5%.
- The 5.8 taxa and 2.8% have no base rates beside them (7.6 taxa, 0.77%).
- A boat sample is two cores bulked, not "one core".
- Random stations sit on gridlines.
- `known` keeps the visit's date while visit properties are dropped under USE-3. The day of year adds 0.002-0.003,
  and the day of the nearest training station of that year changes R^2 by -0.0003. So one clause ("the survey's
  date") settles it.

*Remedy:* edit the notes. This is a quality problem and no reason to hold the task back.

**6. Unidentified tellinoid spat ship as Macoma zeros where the metric is most sensitive (P7, CLEAN-15 Must; PROV-13
Must for the repair rung; a USE-5 note).**
- *Evidence.*
  - species.csv `sibes_id` 339 says: "Tellinoidea below 3 mm are classified on the superfamily level. Includes ...
    Macoma balthica" (checked).
  - It occurs in 71 samples. In 29 of them there is no Macoma row, so they ship as zeros, with 12,553 tellinoid
    spat/m2 between them. One (sample 113998) holds 9,507/m2, the size of the 155 densest Macoma cores.
  - Tellininae (added in 2023) appears in 57 samples, 55 of them from 2018. The late-processed 2017-18 backlog shows
    bivalve presence of 0.53 and 0.79, against 0.62-0.68 in the years around it (column-auditor problem 3,
    claim-auditor row 38).
- *Effect.* A few dozen rows, but the false zeros sit in the tail that RMSE on density weighs most.
- *Remedy.*
  - Drop the 29 rows with Tellinoidea present and no Macoma as rows with an unknown target (0.05%).
  - Add a note on Tellininae and the 2017-18 backlog.
  - Keep a question to NIOZ as the later repair.

**7. The record does not carry two decisions the definition relies on (house; SPLIT-3 Must, PROV-9 Must).**
- The screening left the regime as "the curator's pick", and the CC of 2026-10-30 set only `Yes` and priority 3.
  Grouped is still the AI's choice. It is well argued: the temporal splits score 0.249-0.29, and the source maps
  surveyed years.
- The record says "`year` stays empty", while the definition sets 2024. 2024 follows PROV-9 for a growing source.
- *Remedy:* one REVIEW.md line asking the curator to confirm grouped, and align the record's year line.

**What I do not argue, and why.**
- `station` as a feature (blind reviewer): `feature_columns` drops the group column, so LEAK-33 holds.
- The 142 near-twin station pairs: SPLIT-24 forbids grouping by distance, and grouping them changes R^2 by +0.0016
  (SE 0.0047).
- The grouped regime itself.
- Size and signal (TP-2).
- The missing elevation input: CLEAN-19 allows building it but does not require it.
- Year 2024.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: wadden_sea_sibes_macoma_abundance (advocate, 2026-11-01)**

**Where we stand.** The critic and I agree on the verdict: ship after changes, with no exclusion. On points 1, 3, 5 and 7
I concede. On point 2 I now concede the critic's fix, because a check found no actor that has measured sediment at an
unsampled place. On point 4 I dispute the stated effect: a check shows that the density ranking does not come from the
spat cores. On point 6 I narrow the remedy to a rule that does not read the label, and I drop the Tellininae part.
Scripts and outputs are in the run folder (not committed): r1_metric_pairs, r2_metric_tau, r3_tellinoidea.

**1. Use case, example and moment (USE-1, USE-5, USE-3): concede.** This matches my opening points 1 and 2. The fix
changes wording only:
- write the use case as the source's map of a past surveyed year, for habitat-directive and quality-status
  assessment;
- drop the food-stock example;
- name the archive-map moment in `task_summary.split` and `splits_comment`, with 0.368 against 0.345 and the years
  2008-2011.

With that wording, density is the quantity the actor maps and USE-5 holds. No re-split.

**2. Measured sediment (USE-3, LEAK-10, LEAK-6): concede, and take the interpolated sediment.** I argued for keeping it
as a named potential leak. The check that would have backed that fails:
- I searched the descriptor and the paper for an actor who has sediment measured at a place without a fauna sample.
  I found none. Sediment is always taken just before the fauna core at the same visit ("First, a sediment sample was
  taken"), and in 2008 sediment covered fewer stations than fauna, not more.
- So "given the sediment measured there" would be a use case reworded only to excuse a gap, which counts against it
  under USE-9.
- The column auditor's table settles the mechanism as far as it matters. The station's own sediment from its other
  years recovers 0.002 of the 0.012 gain, so the gain belongs to the visit, not the place.
- The fix is cheap and safe. On the declared metric every sediment variant lands at 862.1-864.1 against 875.6 for
  the dummy (split auditor). IDW from the same year's other stations reads no label (CLEAN-19, rain_in_australia).

What follows:
- swap both columns for the IDW values;
- rewrite bullet 1 and `fit_reason`. The sediment gap leaves `fit_reason`; elevation and the unnamed decision keep
  the fit approximate (USE-8).

One point for the curator: dropping the sediment loses slightly less on the log scale (0.356 against 0.349, untuned).
IDW is still the better mirror of the source's map, which reads its sediment from an IDW surface.

**3. The 427 later empty cores (LEAK-25): concede.** This is my opening point 7:
- keep the 427 as zeros by the Table 4 recipe;
- drop the 2008 samples that have no record, located by year, or the whole 2008 survey if the curator wants a rule
  that never reads the core;
- rewrite bullet 3 and the Decision with the Table 1 match and the base rates.

**4. The metric (MET-1, MET-2, MET-10): dispute the effect, keep (b), and leave (a) to the curator.**
- Concede the note fixes:
  - drop the tau claim;
  - say "ranks as the paper's MSE" only by construction (the paper's 2010 counts do not match V6);
  - add 2014's 75.4% share of the squared deviation and the basin-total bias.
- Dispute "rewards calibrating the mean on a few spat cores more than drawing the map". I ran this on the domain
  practitioner's eight fits over 6 folds:
  - Remove each fold's five densest test rows (3-5 of them from 2014) and the RMSE ranking of the eight fits barely
    moves: Kendall tau 0.79-1.00 per fold. The spat cores set the size of the error, not the order of the models.
  - The contrast that matters for the actor is resolved in every fold. The Tweedie fit beats the five-times-biased
    back-transformed log1p fit in 6/6 folds (gap 28.7, SE 3.4). Smearing beats no smearing in 6/6 (14.8, SE 2.2).
    The Tweedie fit ranks 1st in 5 of 6 folds. The "only 3%" gap is a gap of eight standard errors.
  - What jumps between ranks 1 and 8 is three Poisson variants of nearly equal skill. That is the expected noise
    among near-ties, not a metric that cannot see the map.
- MET-2's third bullet asks whether a source's metric keeps its meaning on a task we changed. Here we declare the
  fallback, not the source's metric, so that bullet does not apply. MET-1 holds: MSE is consistent for the mean that
  the actor sums to basin totals (domain practitioner).
- So (b), `rmse` with corrected notes, is enough on its own and not merely a floor. (a), mean Poisson deviance, ranks
  more stably, but it disagrees with RMSE only among the near-ties (tau 0.07-0.71 per fold). It also needs a new
  library metric and a floor on predictions (MET-12, MET-13). It is a fair weighing call (MET-10, Weigh), best decided
  with nantucket, pennsylvania and basque biotoxins. No Must requires it.

**5. Notes the data refutes (EV-6, EV-8, EV-9): concede all.** The fixes:
- 114 station-days with correlation 0.536;
- "0.2-1.5%";
- base rates beside the 5.8 taxa and 2.8% (7.6 taxa, 0.77%);
- a boat sample is two cores bulked;
- random stations sit on gridlines;
- one clause calling the date "the survey's date" (it is worth -0.0003 when replaced by a neighbour's day).

**6. Tellinoid spat (CLEAN-15, LEAK-25): narrow.**
- Drop the Tellininae part. species.csv says Tellininae of 3-5 mm are "so far, only Macomangulus tenuis and Fabulina
  fabula", so those 57 samples hide no Macoma.
- Dispute "where the metric is most sensitive". The 71 Tellinoidea samples hold 0.07% of the squared deviation of
  density (r3).
- Narrow the remedy. Dropping only the 29 rows with no Macoma selects on the label, which is the very reading the
  critic rejects in point 3 (LEAK-25 as amended: "a rule that does not read the label"). In the 42 rows with Macoma
  the count may be short too: 8,051 tellinoid spat/m2 sit beside 21,543 Macoma/m2. The rule that does not read the
  label drops all 71 samples with Tellinoidea present (0.12% of rows). It moves each affected year's zero share by at
  most 0.001 and its mean density by at most 2.4/m2.
- What follows: a note alone, or the drop of all 71 rows. P7 says fix when cheap and safe, so I accept the drop.

**7. Regime and year in the record (SPLIT-3, PROV-9): concede.** One REVIEW.md line asks the curator to confirm the
grouped regime, and the record's year is aligned to 2024.

**Net.** Ship after changes. The changes are:
- wording of the use case and the split moment;
- IDW sediment;
- keep the 427 zeros;
- drop the 71 Tellinoidea samples;
- correct the notes.

The metric stays `rmse` on density unless the curator takes the Poisson deviance as a family call.

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: wadden_sea_sibes_macoma_abundance (critic, 2026-11-01)**

**Where we stand.** We agree on the verdict: ship after changes. The advocate concedes my points 1, 3, 5 and 7 with
the remedies I asked for. Two disputes remain:

* The measured sediment, which the advocate would keep with a note. I hold that USE-3 and LEAK-6 ask for the
  interpolated swap.
* The coarse tellin classes, which the advocate would only note. A new check widens this from 29 rows to 41 and
  supports dropping them under CLEAN-15.

The metric is the curator's weighing call. We now agree on its floor.

I ran two new checks, in the run folder (visit_sediment and coarse_tellins, not committed):

* Within a station, does the visit's sediment track the visit's tellins? I took each station-year's deviation from
  the station's other years and compared it with the previous visit's deviation and with a within-station shuffle of
  the years (200 draws).
* Cores where a coarse class that includes Macoma is present but Macoma is not: how often does the same station hold
  Macoma on its other visits?

**A1. A real task with an approximate fit; the food-stock example reworded: concede.**
- USE-2 excludes only a task that no decision fits. A soft decision is a USE-8 gap, and `fit_reason` names it.
- The joint remedy settles my point 1: reword `use_case` to the abundance map of a past survey, drop the food-stock
  example, and add the numbers-over-AFDM note.

**A2. The split mirrors the application: concede.**
- The advocate names the archive-map moment with its cost (0.368 against 0.345, falling on 2008-2011). That was my
  remaining ask under point 1.
- The near-twin stations and the regime confirmation: agreed.

**A3. Measured sediment kept with a note: contest. USE-3 (P3, Must) and LEAK-6's second clause decide.**

- **"A property of the place, not recorded after the outcome."**
  - USE-3 asks whether a value existed at the prediction point, not whether it came after the outcome. The
    definition's prediction point is a place without a sample, and no jar exists there.
  - The model does not use the place's persistent sediment. The station's own sediment from its other years
    recovers only 0.002 of the 0.012 (column auditor, 6/6 folds).
  - My check, mud: the visit's deviation tracks that visit's tellin deviation at Spearman 0.046, against 0.020 for
    the previous visit's mud. The null is 0.000 with SD 0.004 (z = 11).
  - My check, grain size: same visit -0.029, previous visit -0.028. That is a persistent drift at the station.
  - Part of the measured value is about this visit, and the rest is the station's own drift. An IDW map from the
    neighbours knows neither.
- **"It does not show on the declared metric (862.1-864.1)."**
  - The advocate's own zillow_prize row says a value is not kept "merely because removing it changes no score".
  - Density RMSE also puts a model that understates basin means fivefold only 3% behind the best (point 4). Its
    silence here is the metric's resolution, not evidence of no leak.
  - On log1p, the scale the models are fit on, the gain shows in 6/6 folds (SE 0.001-0.002).
- **"The paper's IDW passes through station values."**
  - This is an inference (the precedent checker says so).
  - Even if true, it concerns the paper's leave-one-out. The paper's map at unsampled places, the deployment the use
    case names, used interpolated sediment ("the covariate must be known everywhere").
- **"LEAK-6: a slight optimism with a known cause; the mechanism is circumstantial (EV-6)."**
  - What is circumstantial is why the jar helps.
  - That the jar does not exist at the named prediction point is a fact of the design, and its gain is measured
    (6/6 folds). That is a confirmed leak, and LEAK-6 says it "goes even when small" (santander, +0.003 AUC).
  - A note does not resolve a confirmed leak, so a note is not the mildest remedy that works. The swap is: one
    definition edit, label-free, the source's own covariate, built from the same release (CLEAN-19,
    rain_in_australia), at -0.016 to -0.019 R^2.
- **The reword path ("given the sediment measured there").** It moves the prediction point to a place with a sediment
  sample but no fauna sample.
  - No source describes that practice.
  - The one real instance is the 2017-18 backlog, "sampled but not processed". Those are surveyed stations with a
    known history, a known-entity task (USE-10) that the station-grouped split does not mirror.
  - USE-9 weighs against a use case rephrased only to excuse a gap.
- **Narrowed.** The effect is small. If the curator still keeps the columns, the minimum is the advocate's
  restatement: all three numbers in the notes, and "kept" rather than "gap" in `fit_reason` (USE-8). The question
  stays as it is.

**A4. Worth benchmarking: concede.** I raised no value objection. TP-2 and TP-3 hold, and every fold scores.

**A5. The declared metric: concede, narrowed.**
- No Must forces `mean_poisson_deviance`. MET-10 is a Weigh factor, the MET-5 fallback holds, and RMSE on log1p is
  out (MET-3). So (b), `rmse` with the note corrected, is the floor, and (a) is the curator's call, decided with the
  like cases.
- Two narrowings:
  - "The ranking survives dropping the 50 densest rows (tau 0.78-1.0)" holds among the log1p fits. Once fits that
    target the mean are in the set, three of seven models rank anywhere from 1st to 8th across folds, and the 5x-biased
    model is 3% behind (domain practitioner). That is what the curator weighs.
  - The metric reason's "ranks models as the paper's MSE on the unconditional count" must be qualified as well as the
    note (MET-11: the reason says where we looked). V6 does not reproduce the paper's 2010 counts: variance 97.5
    against 24, maximum 455 against 84 (claim-auditor row 26). The advocate's list fixes the note but not the reason.

**A6. Faithful data: concede on provenance; contest on the coarse tellin classes (CLEAN-15, Must).**
- Conceded:
  - The DOI release and checksums.
  - The exact rebuild.
  - Year 2024 under PROV-9, with the record aligned.
  - Mortgage issue 15 for the duplicated ids.
- Contested, with a new fact.
  - species.csv has two coarse classes that include Macoma balthica: Tellinoidea (below 3 mm, `year_added` 2020) and
    Tellininae (3-5 mm, `year_added` 2023).
  - Cores where one is present and Macoma is not ship as Macoma zeros. There are 29 Tellinoidea cores (2015-2018 and
    2022) and 12 Tellininae cores (all 2018, the late-processed backlog).
  - Their stations hold Macoma on 48% and 54% of their other visits, against 28% for the shipped zero cores in
    general.
  - The 9,507/m2 Tellinoidea core (sample 113998) sits at a station with Macoma on 79% of its other visits. That core
    falls in the tail RMSE on density weighs most.
  - For these 41 rows the Macoma count is unknown (somewhere between 0 and the coarse count), not zero. CLEAN-15
    (Must): drop rows with a missing target. That is 0.07% of rows, a one-line filter, no rebuild of any other
    decision.
  - The classes were added in 2020 and 2023, so this happens only in samples processed late. A note on that belongs
    with the drop. This is quality, and no reason to hold the task back.

**A7. The no-record drop: concede, agreed.** Keep the 427 samples of 2009-2022 as zeros. Drop the 342 of 2008, or the
whole 2008 survey if the curator wants a strictly label-blind rule. Correct "not on the tellin count".

**For the mediator, by rank.**
1. Sediment (P3/P4). The Must side asks for the IDW swap; the advocate asks for a kept note. The new check shows part
   of the gain is visit-specific.
2. The 41 coarse-tellin rows (P7). CLEAN-15 asks for the drop; the advocate asks for a note.
3. Metric (P6). A weighing call for the curator. Agreed floor: `rmse`, with the note and the reason corrected.

</details>
