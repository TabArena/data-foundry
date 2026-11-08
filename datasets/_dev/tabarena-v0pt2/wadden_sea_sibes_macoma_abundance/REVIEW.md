# wadden_sea_sibes_macoma_abundance

**Outcome:** added. The AI recommends shipping it as implemented: the re-review of 2026-11-06 under the exposure
rules changed wording only, and its one low-ranked call (issue 7) was settled on 2026-11-08: the note only. The data are NIOZ's SIBES survey of the Dutch
Wadden Sea flats (version 6 of 2024-12-21, CC BY-SA 4.0): one row per fauna sample, 59,044 samples at 5,092 stations,
2008-2022. The target is the Baltic tellin (Macoma balthica) per m^2, zero where the sample held none (56.0%), built
by the data descriptor's own join; shipped as log1p and scored after the inverse. Known: the position, tidal basin and
flat, the survey's date, the sediment interpolated from that year's other stations and the elevation from
Rijkswaterstaat's depth surveys (vaklodingen). Whole stations are held out with all their years, so a test station
stands for a place between the stations of a survey already run. The metric is RMSE on the density (fallback),
unweighted, with no sample weight.

Validity:
* SEL-2 holds: Andrej's `Yes` of 2026-10-30, with his answer of the same day to policy question 1 of the
  zero-inflated review (species-abundance mapping is judged per dataset, no new rule).
* USE-1 and USE-5 triggered, fixed: the use case's example, judging food stocks for birds, did not fit a count
  target. The 50 cores above 10,000 per m^2, which set the score, are spat (newly settled juveniles, 36 of them from
  2014): 11.8% of the tellins counted but 1.3% of their biomass. The use case is now the source's: the abundance map
  of a past survey. The fit stays approximate: no named decision (USE-8); the elevation is joined (issue 4).
* USE-3 and LEAK-10 triggered, fixed: the sediment measured at the visit does not exist at an unsampled place, and its
  gain came from the visit itself. It is replaced by the sediment interpolated from the year's other stations, the
  source's own covariate (LEAK-6, LEAK-7, CLEAN-19; issue 5).
* USE-3 holds for the elevation, a survey of the bed separate from the visit, which exists at an unsampled place. Its
  survey stamps are mostly a nominal 1 January, so 19.3% of the samples take a survey stamped 1 January of their own
  year that may have been made after the sample; the bed is not set by the tellins, and the map of a past survey is
  drawn from the whole archive, so the stamps break no prediction point (the notes now say "date stamp").
* LEAK-25 triggered, fixed by default: the 342 samples of 2008 without any fauna record are dropped, located by the
  year; the 427 later ones stay as zeros (issue 2).
* LEAK-41 holds, nothing to remove: the core area is planned by the platform and is neither a feature nor a weight;
  the subsample fraction, which the lab picks after seeing how many animals a sample holds, sits only inside the
  target.
* SPLIT-1: Andrej's pick, grouped by station (issue 1); the leak test across the split finds none, no test row has a
  feature copy in training, and the task gamer found no exploit beyond the noise of a random column.
* PROV-9 holds: a yearly growing release takes the year of the pinned snapshot, 2024.

Value: TP-2 holds (untuned LightGBM R^2 0.373 on log1p at unseen stations, against 0.235 for a linear model, in the
task probe of 2026-11-06 after the elevation fix, on 5 of 9 splits as on 2026-11-02); TP-5 holds (about 1,700 test
stations per fold). MET-5 gives the fallback `rmse` on the density, kept by Andrej's call of 2026-11-02 (the Poisson
deviance went only to nantucket_sound_sea_duck_aerial_survey_counts, whose source names it); MET-2 holds, finite on
all 9 folds. MET-15 and MET-16 hold: the map predicts an
equal-area cell, so the density is scored unweighted with no sample weight, and weighting by the core area changes no
ranking (Kendall tau 1.0 between the unweighted and the area-weighted RMSE, 7 models, 9 of 9 folds). MET-14 holds:
the source ships the rate, and with no count released its rebuild check has nothing to rebuild. The cross-dataset item
X3 in the working copy's REVIEW.md proposes that this check apply only when the source releases the count; this
dataset and boreal_postfire_lichen_biomass release none.

Quality: the 71 samples with unidentified tellinoid spat leave (CLEAN-15); six duplicated sample ids keep one row, and
their conflicting sediment is no source of the interpolation (CLEAN-1). The 117 pairs of a grid and a random sample
taken at one station on one day share every feature; each pair stays in one fold through the station. CLEAN-11 holds
with two notes: the 39 single boat cores stay (issue 6), and so do the 608 positive counts below one tellin per core,
whose cause is unknown (issue 7, kept with the note only on 2026-11-08). EV-8 triggered three times on 2026-11-06, each fixed by rewording: the 608, which the
area and the subsample correction cannot explain; the nominal survey stamps; the row text, which now names the single
boat cores. The check warning `task_target_value_dominant` (56.0% zeros, observed absences) is accepted with Andrej's
reason of 2026-11-03.

Weighed: NIOZ's DOI release with a data descriptor +; a real but soft use case 0; 59,044 rows at 5,092 stations +; a
thin feature set, now with elevation 0; RMSE on the density separates models poorly -.

After the first review panel (AI, 2026-11-01) the definition took the mediator's ten changes: the sediment, the
samples without a fauna record, the Tellinoidea samples and the use case above; the moment of the map in the split
text (issue 1); the date named as the survey's date; the metric note; count slips and two notes. The numbers here and
in issues 1 to 5 were measured again on the changed definition, so some differ from that panel's (default LightGBM
R^2 0.343 on log1p, against the panel's 0.368 with measured sediment; 117 station-days with two samples, not 114; RMSE
879.7 against 847.1 for the Tweedie fit, not 865.8 against 837.2); that panel's reports are in this file's git
history. On 2026-11-06 the elevation join was fixed: under pandas 3, `stack()` keeps the unsurveyed cells, so a
pandas-3 run left 40.66% of the rows without elevation; now 5 rows miss it, as documented, pandas 2.3 and 3.1 give the
same values, and 400 of 400 sampled rows match a re-read of the source tiles. The focused re-review of the same day
(claim auditor, column auditor, task gamer, mediator) found wording only, and its four changes are made (Mediator,
"Changes to make now"). `dataset check`: 0 errors, 0 warnings.

**Main points:** Open: none. Settled: the interpolated sediment (issue 5), the split by station after a clean leak test
(1), the 2008 samples without a fauna record dropped (2), the elevation joined (4) and RMSE on the density kept
(Andrej's call, no issue in this file) on 2026-11-02; the 39 single boat cores kept with a note (6) on 2026-11-06; the
608 counts below one tellin per core kept with the note only (7) on 2026-11-08. Across datasets: X3, whether the check that the density times the core area rebuilds the count applies only
when the source releases the count.

**Issues for Andrej and Lennart:**

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

6. **Keep the 39 single boat cores that the data descriptor does not describe?**

   * **Problem:**
     - 39 samples are one boat core of 0.00866 m2, half the two-core boat sample (0.0173 m2) that the data descriptor
       describes.
     - The source standardised their density for the area, but a core half the size finds no tellin more often: 79.5%
       of them hold none, against 57.4% of the two-core boat samples.
     - Keep them as samples of the survey, or drop them as a protocol the source does not document?
   * **Background:** the descriptor describes two boat cores ("two cores ... combined area of 0.0173 m2") and one core
     on foot ("a single core of 0.0177 m2"), and no single boat core
     ([descriptor](https://doi.org/10.1038/s41597-025-04540-9)). The density folds in the core area (CV 1.4% over the
     shipped rows) and, for samples with many individuals, a subsample fraction chosen after the sample is seen and
     not released, so 9.55% of the positive counts per core are not whole numbers. The task scores the density
     unweighted, as for equal-area map cells[^6a].
   * **Effect on the task:** 39 of 59,044 rows (0.07%): 20 in 2008, 9 in 2010 and 10 in 2009-2019, each at its own
     station. One tellin in such a core is 115.5 per m2, against 57.7 in two cores, so more of their zeros are chance.
   * **Experiments:** 79.5% of them hold no tellin, against 60.6% in the same stations' 452 other samples and 67.2% in
     the two-core boat samples of the same year and basin. Halving the area of a random scatter at those two rates
     gives 77.8% and 82.0% zeros, so the smaller core explains their zeros.
   * **Consistency:** the 2008 samples without any fauna record were dropped because they may never have been entered
     (issue 2)[^6b]; these cores have fauna records, so their zeros are observed, as in every other sample.
   * **Panel:** the column auditor and the domain practitioner counted them (41 in the raw file, 39 shipped) and
     raised nothing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | the 39 stay; the notes name them and the effort the density folds in | real samples of the survey, standardised for the area by the source; no filter to defend | more of their zeros are chance; a protocol the descriptor does not describe |
     | B | Drop them | the 39 rows go, located by the core area | one sampling protocol per platform | drops real samples, 20 of them from 2008; a filter for a gap the core area already explains |

   * **Recommendation:** A: they are unusual, not wrong[^6c], and their extra zeros are what half the area gives by
     chance. **Decision:** A or B?

   [^6a]: **MET-15** (Must, Lennart, 2026-11-06): a rate's realized denominator is the metric's row weight and the
     task's sample weight; when the decision is per unit of an equal-area map, per loan or per contract, the rate is
     scored unweighted and no sample weight is declared.
   [^6b]: **LEAK-25** (Must): "no event" mixed with "not recorded" is a censoring bias; recovered includes unrecorded
     rows located by a rule that does not read the label, and dropped.
   [^6c]: **CLEAN-11** (Should): impossible values become missing, and the row stays; values that are only unusual
     stay; a row leaves only when it is no task row or a copy.

   **Resolved (2026-11-06, Lennart):** A (decision D13 of the exposure study,
   [#51](https://github.com/TabArena/data-foundry/issues/51)): the 39 single boat cores stay, with a note in
   `curation_comments` (79.5% zeros against 60.6% at the same stations' other visits, about the 77.8% that half the
   area gives by chance). The notes also gain the exposure paragraph: the density folds in the core area (CV 1.4%)
   and a subsample correction whose fraction is chosen after the sample is seen and not released, 9.55% of the
   positive counts per core are not whole numbers, and the task scores the density unweighted with no sample weight.
   No earlier call covered these cores. `dataset check`: 0 errors, 0 warnings.

7. **Ask NIOZ why 608 samples hold less than one tellin per core, or keep the note only?**

   * **Problem:**
     - In 608 samples the source's density times the core area gives less than one tellin, mostly 0.5, 0.8 or 0.4,
       which no whole animal in a core can give.
     - The subsample correction divides by a fraction of at most one and so can only raise a count, and the data
       descriptor describes part-animals only for polychaete worms (heads and tails), so their cause is unknown.
     - Ask NIOZ for the cause, or keep the densities as published with the note the definition now carries?
   * **Background:** the source ships only the density of each taxon per m2, "standardized for differences in sampled
     surface area and subsampling", and releases neither the count nor the subsample fraction; "for the species and
     samples that contained many individuals, a subsample was selected and analyzed", and "abundances were corrected
     by dividing the densities with the fraction of the subsample"
     ([descriptor](https://doi.org/10.1038/s41597-025-04540-9)).
   * **Experiments:** on the shipped rows (claim and column auditors, 2026-11-06), the 608 lie on a lattice of tenths
     and occur in every year from 2008 to 2022 (14 to 70 a year). They come from samples poor in fauna: a median of 37
     animals of all species per core, against 51 in samples with exactly one tellin and 107 in those with more; 28.8%
     of them record no Macoma biomass, against 1.3% of all Macoma records.
   * **Effect on the task:** 608 of 59,044 rows (1.0%), all at small densities (median about 29 per m2, where the
     densest spat patches reach 99,780). The RMSE on the density is set by those patches, so these rows hardly move a
     score, and under both options their targets stay as published for now.
   * **Panel:** the column auditor read the values as fragments or subsample corrections; the claim auditor showed that
     the subsample correction cannot give a count below one, and the mediator settled the cause as unknown and
     recommends the note only.
   * **Unknown:** whether these are damaged shells counted in parts or entry errors; only NIOZ can say.
   * **Consistency:** follows spanish_motor_insurance_2015_2018, where the request to the authors was left for a later
     version and the task shipped as it was[^7a]. Repair from the origin comes first when the origin can be
     reached[^7b], which is option B. No repair of our own is offered: rounding or dropping the 608 would guess at a
     cause, and a value that may be right stays[^7c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The note only (implemented) | the 608 densities stay as published; the exposure note says that their cause is unknown | no row or score changes; no repair of our own | the cause stays open |
     | B | Ask NIOZ, ship in the meantime | you ask the SIBES team how a count below one arises; the dataset ships as it is, and the note, or the target if NIOZ corrects it, follows the answer | the cause from the origin; a possible data error reported to the source | needs you to write, an agent cannot send it; effort for 1.0% of the rows, which the score hardly feels |

   * **Recommendation:** A, as the mediator recommends: the score hardly feels these rows, the note documents the
     open cause, and a question can still go with a later version. **Decision:** A or B?

   **Notes for the AI:** on A, nothing: the exposure bullet of `curation_comments` carries the note (2026-11-06). On
   B, draft the message for the curator to send to the SIBES team at NIOZ (data doi:10.25850/nioz/7b.b.ug, the
   descriptor's corresponding author): 608 positive records of Macoma balthica (sibes_id 59) in version 6 whose
   `abundance_m2` times the sample's `total_surface_m2` is below one, on a lattice of tenths (mostly 0.5, 0.8, 0.4), in
   every year 2008-2022; how do they arise, when the subsample correction divides by a fraction? Attach the sample ids
   (positive density times core area below one on the shipped rows). Keep `dataset.py` as it is until the answer; then
   reword the exposure bullet, and change the target only if NIOZ releases corrected values (a new pinned release and
   a CHANGELOG entry).

   [^7a]: spanish_motor_insurance_2015_2018, issue 4 (Andrej, 2026-11-03): "Write a comment that we could do this for
     a future version, but now go with the task as we have it for simplicity."
   [^7b]: **P5** (faithful data, repaired from its origin) and the remedy ladder (principles, "How to decide", step
     5): take the mildest remedy that resolves the problem: repair from the origin; fix the definition; keep it with a
     documented note; exclude the dataset.
   [^7c]: **CLEAN-11** (Should): impossible values become missing, and the row stays; values that are only unusual
     stay. A part-animal may be a real record, so nothing is set missing.

   **Resolved (2026-11-08, Lennart):** A, as implemented. The 608 densities ship as published, and the exposure note
   says their cause is unknown, now with the CC of 2026-11-08; NIOZ is not asked for now. `dataset check`: 0 errors,
   0 warnings.

**Review panel:** ship after changes (mediator). The changes are wording only and are made. Tier focused, a re-review of
2026-11-06 under LEAK-41 and MET-14 to MET-16, after decision D13 and the elevation fix: the claim auditor, the column
auditor, the task gamer and the mediator; no blind reviewer, advocate or critic in this tier. Claims: 25; 22 hold, 2
partly refuted (the 608 counts below one tellin per core, which the area and the subsample correction cannot explain;
"on or before the sample's date" for survey stamps that are mostly a nominal 1 January) and 1 inconsistent with D13 (the
row text), all three fixed by rewording; untested: whether the one-ulp parse differences between pandas 2.3 and 3.1
change the container checksum. Blind review: none in this tier. Task gamer: no exploit beyond the noise of a random
column (five attacks, against an honest raw-scale RMSE of 846.99). Agreed: the elevation fix (5 rows missing instead of
40.66%, 400 of 400 values match the source tiles), D13's numbers, nothing for LEAK-41 to remove (the planned core area
is no feature and no weight, the subsample fraction only inside the target), the unweighted score (tau 1.0 against the
area-weighted RMSE on 9 of 9 folds), the fallback RMSE and its ranking claim. Disputed: the cause of the 608 (the column
auditor: fragments or subsample corrections), settled by arithmetic as unknown, with asking NIOZ left to you (issue 7);
MET-14's rebuild check, which has nothing to rebuild here, goes to the cross-dataset item X3.

<details><summary>Mediator</summary>

The mediator's issue B is issue 7 of this file; its issue A is the cross-dataset item X3 of the working copy's REVIEW.md, which counts two such definitions: noaa_afsc_bottom_trawl_survey_cpue releases its counts and now asserts the rebuild.

**Mediator report: wadden_sea_sibes_macoma_abundance (exposure re-review, focused tier, 2026-11-06)**

With no advocate or critic in this tier, the disputes are between the two auditors and between the notes and the data. I ran no new experiment. Each disputed fact is settled by the measurements already in the reports or by plain arithmetic, shown below.

**1. Recommendation (judgment record)**

Verdict: ship after changes. The changes are wording only.

Validity: USE-3 holds. The elevation is a separate survey of the bed and exists at an unsampled place. Under the moment the use case sets ("a map of a past survey drawn from the whole archive"), a bed survey stamped later than the sample is also available, so the nominal 1-January stamps break no prediction point. LEAK-41 has no column to act on: the core area is planned by the platform, is not a feature, and is not a weight. The subsample fraction, which the outcome does set, sits only inside the target. LEAK-10 holds. SPLIT-1 holds: no test row has a feature copy in training (0.0% of 177,132). The elevation bug fix holds: 5 rows missing instead of 40.66%, 400 of 400 values match an independent re-read of the source tiles, and the result is bit-identical under pandas 2.3 and 3.1.

Value: TP-2 holds. MET-2 holds: the score is finite on all 9 folds. MET-15 and MET-16 hold: scored unweighted with no sample_weight, and the weighting is immaterial by measurement (Kendall tau 1.0 between unweighted and area-weighted RMSE on 9 of 9 folds, 7 models). MET-14 is applied: the source ships the rate. Its rebuild assertion cannot be written because no count is released (change 4).

Quality: CLEAN-11 is kept with a note: the 39 single boat cores (D13) and the 608 positive counts below one tellin per core. The notes need three wording fixes under EV-8 (changes 1 to 3).

Weighed: unchanged from REVIEW.md (source +, soft use case 0, size +, thin features 0, RMSE separates models poorly -).

For the curator: two low-ranked calls, neither blocking. Issue A (a proposed MET-14 amendment) and issue B (optionally ask NIOZ about the 608).

**2. Changes to make now (no decision needed)**

All four go in dataset.py, after which the README is regenerated and the copy's CHANGELOG.md gets a dated entry.

1. The 608 positive counts below one (EV-8; CLEAN-11). The exposure bullet now says the area and the subsample correction explain why "2,480 ... are not whole numbers, and 607 are below one tellin". For the 608 below one, that is arithmetically false.
   - The descriptor corrects for subsampling by dividing the density by the subsample fraction, which is at most 1. A whole count of at least one therefore stays at least one.
   - The 608 sit on a 0.1 lattice (0.5 ×113, 0.8 ×77, 0.4 ×73, ...) and appear in every year from 2008 to 2022.
   - They come from poor samples: median total fauna 37.4 per core, against 50.5 for a count of one and 107 for counts above one. 28.8% of them have zero AFDM, against 1.3% overall.
   - The area and the subsampling explain the 1,897 non-whole values above one, not these 608.
   - Settle the count at 608: the claim auditor and the column auditor both count 608, and so does REVIEW.md. The bullet's 607 depends on the build's rounding tolerance; either name that tolerance or use 608 (absolute tolerance 1e-3).
   - Proposed clause: "the 608 below one tellin per core (on a 0.1 lattice, mostly in poor samples) are not explained by the area or the subsample correction, which can only raise a count; the descriptor documents fractional counts only for polychaete fragments, so their cause is unknown. They are 1.0% of the rows at small densities (median about 29 per m2), which the RMSE on the density does not feel."
   - This settles the auditors' only disagreement. The column auditor read the 608 as "consistent with fragments or subsample corrections". The arithmetic rules out the subsample correction. Fragments stay possible but undocumented, so the note should say "unknown cause", not name a mechanism.

2. The elevation's "on or before" wording (EV-8). It appears in curation_comments (Elevation), the code comment at step 3, and the column meaning.
   - 70,220 of 74,518 station-surveys (94%) carry a stamp on the 1st of a month, 56,581 of them 1 January. The stamps come from Rijkswaterstaat's file names, for example "_20220101_VlieBi_22_12_31.asc".
   - 19.26% of the samples take a survey stamped 1 January of their own year, 157 to 248 days before the sample. The survey itself may have been made after the sample.
   - Reword to: "the latest survey whose date stamp (mostly a nominal 1 January of the survey year, from the source's file names) is on or before the sample's date".
   - Keep the code. This is no leak: the bed is not set by the tellins, and a later survey is part of the archive the map is drawn from (the split already trains on later years, settled issue 2 of 2026-11-02).
   - For the record: the stricter cut (surveys from earlier calendar years only) changes 10,269 rows and costs LightGBM R^2 0.0015 on log1p (lower on 8 of 9 folds). Nothing requires it.

3. task_summary.row (EV-8, consistency with D13).
   - It says "one core on foot, two cores bulked from a boat", but 39 rows are a single boat core.
   - Change to "(one core on foot, two cores bulked from a boat, a single boat core in 39 samples)".

4. MET-14's rebuild assertion (MET-14, Should).
   - MET-14 asks `_clean` to assert that the target times the denominator rebuilds the count. Here there is nothing to rebuild: samples.csv and biota.csv release only abundance_m2, and the subsample fraction is not released.
   - Add half a sentence to the exposure bullet: "no count is released, so the target × area check of MET-14 has nothing to rebuild; the source's density is shipped as it is".
   - No exception record is needed: the assertion has no object here, and the rate MET-14 requires is what the source ships. See issue A for the recurring pattern.

No change for the remaining points: 156 rows below -2 m NAP and 100 rows on surveys older than 20 years (CLEAN-11, unusual not wrong; the next survey differs by a median 0.13 m); the 1-ulp parse difference between pandas 2.3 and 3.1 (51 target values, max relative 2.2e-16; at most a checksum note if the checksum is pinned).

**3. Issues for the curator, ranked**

No issue at P1 to P6 and no Must issue. Both items are low rank.

**A.** Rules maintenance (MET-14, Should): should the rebuild assertion apply only when the source releases the count? Proposed amendment, not urgent.

- Problem: MET-14's assertion cannot be written when the source releases only the rate. This is the third definition shipping a source-folded density without the assertion: boreal_postfire_lichen_biomass (kg/ha, quadrat area folded in), noaa_afsc_bottom_trawl_survey_cpue (CPUE, area swept folded in), and this one.
- Effect: none on any score. Without a clause, the next panel will raise the same point again.
- Evidence for amending: principles.md says the same reason recurring a third time calls for an amendment proposal, and all three cases have the same fact (no count released, the rate is the source's own).
- Evidence against: none raised. An amendment is the curator's deliberate change of a rule.
- Decision: amend MET-14 to add "when the source releases the count; when it ships only the rate, the notes say so", or leave each definition's note as it is.

**B.** The 608 below-one counts: ask NIOZ for the cause? Optional, P5/P7.

- Effect: 1.0% of rows at small densities, which the RMSE cannot feel. The target stays as the source standardised it either way.
- For asking: repairing from the origin is the top of the remedy ladder, and a data error would be worth reporting to the source.
- For not asking: the effect on the score is nil and change 1 already documents the open cause.
- Decision: ask the source, or keep the note only. The panel recommends keeping the note only.

**4. Disputed points, settled**

- Cause of the 608: settled by arithmetic (change 1). The subsample correction is ruled out; the cause is unknown. A note, no target change (CLEAN-11 over any repair we would invent ourselves; P5 keeps the data as published).
- "On or before" against nominal stamps: no rule conflict. USE-3 and LEAK-10 hold under the archive-map moment, so this is wording only (EV-8, change 2). It is not a weighing call: the stricter cut serves no rule.
- task_summary.row against D13: an inconsistency, not a conflict (change 3).
- MET-14 rebuild: the rule's object (the count) is absent, so it is neither a departure nor a failure (change 4 and issue A).

The task gamer's attacks, mapped to rules. The definition carries no `Potential leak, kept on purpose:` note, so none of these is a known accepted leak. Each is either new with no gain or covered by settled text.

| # | Attack | Rule | New or known | Gain over honest raw-scale model (846.99) | Issue? |
|---|---|---|---|---|---|
| 1 | Day-level survey-log counts (stations per day, rows per flat-year, weekday) | LEAK-28/LEAK-29 (aggregates over all rows; label-free); USE-3 | New | +0.22 RMSE, within noise (about ±1.5 to 2) | No: deployable, label-free, no gain |
| 2 | Same-year neighbours' labels (nearest, IDW, share non-zero) | SPLIT-1 / LEAK-10 | Known (splits_comment: the year's other stations are the map's own input; settled issue 1) | -0.6 (worse) | No |
| 3 | Elevation-missing flag (5 rows) | LEAK-25 / LEAK-13-type recording artefact | New | 0.00 (leak probe: R^2 -0.001) | No: missingness follows the survey calendar |
| 4 | Core area or subsample read off the target's lattice | LEAK-41 / MET-15 | Known (exposure note) | Not measurable: no column holds it | No |
| 5 | Format-only features (decimals, sentinels) | LEAK-15 (recording artefacts) | New | -1.4 (alone 889.88, worse than the constant 883.88) | No |
| - | Raw-scale RMSE dominated by 2014 spat (top 10 rows 57% of squared error); proposes RMSLE | MET-10/MET-5 | Known: settled issue 3 (2026-11-02, RMSE on the density kept by the curator); today's changes do not reopen it | n/a | No |
| - | 2017/2018 rows exceed the paper's processed-station counts | LEAK-25 | Covered by settled issue 2 (2008 no-record samples dropped, 427 later ones kept as zeros) and by version 6 being a later release | No block of fake zeros: no flat is 100% zero | No |

Overall: no exploit beats the honest model beyond the noise of a random column.

**5. Agreed facts (both auditors and the task gamer, rebuilt under pandas 3.1.1)**

Frame:

- 59,044 rows, 5,092 stations, 56.0% zeros.
- 8 features. No scoring column, sample_weight None, metric inputs {}.
- total_surface_m2, platform and sampling_type are not features.

Elevation fix:

- The old code under pandas 3.1 left 24,006 shipped rows (40.66%) missing. The fix leaves 5, at stations 2942, 2996, 4008 and 4083, whose first survey is stamped 2010-01-01 or 2011-01-01.
- Where both runs have a value, it is equal (0 differ). Pandas 2.3 and 3.1 give bit-identical results.
- Median survey age 2.70 years; 98.03% of samples within 6 years.
- Elevation gain with the fixed column: LightGBM R^2 0.334 to 0.371 and RMSE 878.4 to 869.9, both better on 9 of 9 folds. Same direction as the note's 0.343 to 0.376; the levels differ with the hyperparameters.

D13:

- 39 single boat cores of 0.008659 m2: 20 in 2008, 3 in 2009, 9 in 2010, 1 in 2013, 2 in 2017, 4 in 2019. Each at its own station, 32 grid and 7 random.
- 79.5% of them are zeros, against 60.6% in the same stations' other samples, 67.2% in two-core boat samples of the same year and basin, and 57.4% in all two-core boat samples.
- The halved-area expectation is 77.8% to 82.0% zeros (per-sample mixture 0.799), which matches.
- Core-area CV is 1.4% (0.52% without the 39).

Non-whole counts:

- 2,480 of 25,974 positive counts are non-whole (9.55%) at the run's tolerance, 2,505 at an absolute tolerance of 1e-3.
- 608 are below one. The subsample fraction is not released.

Metric:

- The fallback RMSE on the density is justified: the paper scores ME and MSE with no single criterion.
- It ranks 7 models exactly as the paper's MSE on the count per core (tau 1.0, 9 of 9 folds).
- Finite on all 9 folds, which have 1,697 to 1,698 test stations each.

**6. Consistency with precedent**

No precedent checker report was supplied to this focused tier, so I checked the closest Cases by hand.

- MET-15 unweighted for a map over equal-area cells: consistent with noaa_afsc_bottom_trawl_survey_cpue (CPUE scored unweighted, effort folded in by the source) and boreal_postfire_lichen_biomass (planned protocol area, no weight, LEAK-41 has nothing to remove). The fact that sets these apart from the insurance Cases (fremtpl2, bemtpl97, australian_vehicle_insurance_2004_2005, frempl, pricing_game_2016, spanish_motor_insurance_coverage_level_2022_2024, where the exposure is the weight): the decision here is per unit of an equal-area map, not a sum over a realized denominator. The planned area also has CV 1.4%, and the weighting does not change a ranking.
- MET-14 without a rebuild assertion: treated like boreal and noaa CPUE. This is the third case, hence issue A.
- MET-10 (raw-scale RMSE): consistent with this dataset's own settled issue 3 (2026-11-02). The task gamer's RMSLE suggestion is not reopened.
- D13 (keep the 39 cores with a note): today's findings support it, and no precedent decides otherwise.

</details>

<details><summary>Claim audit</summary>

**Claim auditor: wadden_sea_sibes_macoma_abundance, exposure re-review of 2026-11-06 (focused tier)**

Container rebuilt from the raw files under pandas 3.1.1: 59,044 rows, features = date, tidal_basin,
tidal_flat, longitude, latitude, 2 interpolated sediment columns, elevation_m_nap; sample_weight None; scoring_columns [].

VERDICT: today's changes hold on the data. The elevation fix works (5 missing; 40.66% missing under the old code on
pandas 3; bit-identical under pandas 2.3 and 3.1). All D13 numbers reproduce. The metric holds under MET-1, MET-11,
MET-14 and MET-15. Measured on our data: RMSE on the density ranks 7 models exactly as the paper's MSE on the count per
core and as an area-weighted RMSE (Kendall tau 1.0 on 9 of 9 folds). Two notes are partly refuted, both Could-level
note accuracy (EV-8): (1) the 608 positive counts below one tellin per core cannot come from the area or the subsample
correction the notes name; (2) the elevation's "latest survey on or before the sample's date" is not guaranteed,
because 94% of the vaklodingen survey dates are nominal 1 January labels. Neither changes validity. One summary field
is now inconsistent with D13 (the task summary's "row" says two boat cores).

**Today's changes (D13, exposure notes, elevation fix)**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| C1 | 39 shipped samples are a single boat core of 0.00866 m2 (41 in raw); 20 in 2008, 9 in 2010, 10 in 2009-2019; each at its own station; 32 grid, 7 random | curation_comments Note (CC 2026-11-06); REVIEW issue 6 | group the rebuilt frame (joined to samples.csv by index) by total_surface_m2 | HOLDS | 39 rows at 0.008659 m2, all platform=boat; years {2008:20, 2009:3, 2010:9, 2013:1, 2017:2, 2019:4}; 39 distinct stations; grid 32 / random 7; 41 in raw samples.csv | CLEAN-11 |
| C2 | 79.5% of them hold no tellin, against 60.6% in the same stations' 452 other samples, 67.2% in two-core boat samples of the same year and basin (57.4% in all two-core boat samples) | same | zero shares on the rebuilt frame | HOLDS | 0.795; 452 others 0.606; 5,694 same year-basin two-core boat 0.672; all two-core boat 0.574 | CLEAN-11, EV-1 |
| C3 | One tellin is 115.5 /m2 in one core, 57.7 in two; halving the area of a random scatter gives 77.8% and 82.0% zeros, so the smaller core explains their zeros | same | sqrt(p0) for the halved Poisson; plus a sharper check: mean exp(-count/2) over the 5,694 same year-basin two-core samples | HOLDS | sqrt(0.606)=0.778, sqrt(0.672)=0.820; per-sample mixture 0.799 against the observed 0.795. Positive densities 46.2-461.9 /m2 (0.4-4 per half core), so the area is not mis-recorded (a true two-core area would give about 61-67% zeros) | EV-1 |
| C4 | Core area CV 1.4% over the shipped rows | Exposure note; CHANGES | std/mean of total_surface_m2 over the shipped rows | HOLDS | 0.0139. Without the 39 single cores 0.0052: the 1.4% is mostly those 39 rows | MET-14 |
| C5 | 2,480 of 25,974 positive counts per core (density x area, 9.55%) are not whole numbers; 607 are below one tellin | Exposure note | count = density x area on the shipped rows | HOLDS (depends on the tolerance) | 25,974 positives; 2,505 non-whole at abs tol 1e-3 (9.64%), 2,480 at the run's tolerance; 608 below one | MET-14 |
| C6 | The density folds in the core area and a subsample fraction the lab picks after seeing the sample and does not release; the non-whole counts are what that gives | Exposure note: "The source folds both into abundance_m2 ... so the target is a density: 2,480 ... are not whole numbers, and 607 are below one tellin" | descriptor (PMC11814293): "abundances were corrected by dividing the densities with the fraction of the subsample", so a subsampled count is count/f >= 1. Then inspect the below-one values | PARTLY REFUTED | Dividing by a fraction <= 1 cannot give a positive count below one. The 608 below-one values sit on a tenths lattice (0.5 x113, 0.8 x77, 0.4 x73, 0.7, 0.6, 0.1 x50, ...) in every year 2008-2022 (14-70 per year). They are poor samples, not rich subsampled ones: median total fauna 37.4 per core against 50.5 for count==1 and 107 for counts >1; mean log1p at the same station in other years 2.12 against 2.44 for count==1. The descriptor names fractional counting only for polychaete heads and tails. The area and subsample explain the non-whole values above one (1,897), not the 608 below one (2.3% of positives, 24% of the non-whole). Two other facts hold: the subsample fraction is unreleased (no column in samples.csv or biota.csv) and the "standardized for ... subsampling" quote is verbatim | EV-8 (Could: note accuracy) |
| C7 | Scored unweighted with no sample weight: the map predicts the density of an equal-area cell; the core area is no feature; a Poisson deviance on non-whole counts is no likelihood | Exposure note; MET-15 footnote | sample_weight(c), scoring_columns, metric inputs; feature_columns. Then score 7 models (mean density, mean log1p, LightGBM L2 on log1p, LightGBM L2 on density, LightGBM Tweedie 1.5, LightGBM without elevation, LightGBM with prior-year elevation) on the 9 shipped folds by unweighted RMSE and by area-weighted RMSE | HOLDS | sample_weight None, scoring_columns [], inputs {}; total_surface_m2, platform and sampling_type absent from the features. Kendall tau (unweighted vs area-weighted RMSE) 1.0 on 9 of 9 folds: under a CV of 1.4% the weighting choice changes no ranking. The core area is planned by the platform, known before the sample, and not set after the prediction point, so LEAK-41 has no column to act on | MET-15, MET-16, LEAK-41 |
| C8 | Bug fix: `stack()` under pandas 3 kept NaN cells, so elevation_m_nap was missing in 40.66% of rows; with `stack().dropna()` 5 samples have no elevation | CHANGES; code comment ("40.7% of the samples") | the run's npz from the old code under pandas 3.1 reindexed to the shipped sample_ids; the shipped frame rebuilt now | HOLDS | old code + pandas 3.1: 24,006 of 59,044 shipped rows missing (40.66%), 24,229 of 59,457 raw samples (40.75%, the comment's 40.7%). Where both are present the values are equal (0 differ). Now: 5 missing | CLEAN-11 (correctness), EV-1 |
| C9 | Bit-identical under pandas 2.3 and 3 | CHANGES | compare_versions.py on elev_pandas2.3.npz vs elev_pandas3.1.npz and vs the pandas-2.3 run of the old code | HOLDS | series (74,518 station-surveys) and per-sample elevation and survey identical in all three; the fixed pandas-3.1 sample elevations equal the frame I rebuilt (array_equal with NaN) | EV-1 |
| C10 | 5 samples have no earlier survey and stay missing | curation_comments (Elevation) | for each missing sample, list its station's surveys | HOLDS | stations 2942 (2008, 2009), 2996, 4008, 4083 (2008): every station has a cell; first surveys are labelled 2010-01-01 or 2011-01-01 | USE-3 |
| C11 | Elevation is from the latest vaklodingen survey on or before the sample's date: median 2.7 years earlier, 98.0% within 6 years | curation_comments (Elevation); task_summary.known | recompute the merge_asof; inspect the survey dates in the netCDF (time attrs, isource flag_meanings) | NUMBERS HOLD; "on or before" PARTLY REFUTED | median 2.70 y, 98.03% within 6 y. But 70,220 of 74,518 station-surveys (94%) are dated the 1st of a month, 56,581 of them 1 January. These are nominal labels from the source file names (KB127_1514: "_20160101_Wadden_2015_16tmp.asc", "_20220101_VlieBi_22_12_31.asc"). 19.26% of the samples take a survey labelled 1 January of their own year, 157-248 days before the sample; the real survey may be later than the fauna sample. Cost of the conservative fix: elevation from an earlier calendar year changes 10,269 rows and LightGBM R^2 on log1p by -0.0015 on average (-0.003 to +0.001, 8 of 9 folds lower) | USE-3 (no validity change: bed elevation is no outcome, and the use case is a map of a past survey drawn from the whole archive) ; EV-8 |
| C12 | Side note: pandas 2.3 parses 8,060 of 449,516 abundance values one ulp off; harmless for scores | CHANGES | target_pandas2.3.npz vs target_pandas3.1.npz | HOLDS | 51 shipped target values (559 densities) differ, max relative 2.2e-16. Not tested: whether the container checksum then depends on the pandas version (a reproducibility point for a build, not a score point) | PROV (Could) |

**The metric (MET-1, MET-11, MET-14, MET-15, MET-2)**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| M1 | Fallback rmse: Lyashevska et al. 2016 score with overall/user's/producer's accuracy (prevalence) and ME and MSE (intensity, unconditional intensity), with no single criterion; the descriptor defines no metric | Metric.fallback reason | looked once more: the paper (PMC4729254, Materials and Methods) and the descriptor (PMC11814293) | HOLDS | paper: "the quality measures were overall accuracy, user's accuracies, and producer's accuracies" / "mean error (ME) and mean squared error (MSE)"; it compares the small and large models measure by measure and names no single criterion. The descriptor has no evaluation section. MET-11's stand-in needs a unique source metric, which is absent, so the origin is fallback; the spec's original/reference are None, as a fallback allows | MET-1, MET-5, MET-11 |
| M2 | RMSE on the density ranks models nearly as the paper's MSE on the unconditional count per core | Metric reason | same 7 models x 9 folds: RMSE on the density vs RMSE on count per core (area x (y - p)) | HOLDS (now measured on our data) | Kendall tau 1.0 on 9 of 9 folds | MET-11, EV-1 |
| M3 | Version 6 does not reproduce the paper's 2010 counts (variance per core 97.5 against 24) | Metric reason | 2010 count per core on the shipped rows | HOLDS | shipped 2010: n 3,965, mean 1.92, variance 96.4 (97.5 is the raw-row figure), 60.9% zeros; the paper has mean 1.39, variance 24, 66% zeros of 3,451 | EV-8 |
| M4 | Computable on every fold (MET-2): unit per row; shipped as log1p and scored on the density after expm1 | target_transform="log1p" | scorer(c) on each of the 9 test folds with constant predictions (training mean density, training mean log1p) and the models | HOLDS | finite on all 9 folds; 19,446-19,955 test rows and 1,697-1,698 test stations per fold; the scorer equals sqrt(mean((expm1 y - expm1 p)^2)) on back-transformed predictions. Training-mean density 883.9; LightGBM log1p 869.9; Tweedie 841.3 (beats LightGBM log1p on 9 of 9 folds) | MET-2, MET-3 |
| M5 | MET-14: a count over a varying amount at risk ships as the rate per unit; the count leaves the frame | Exposure note | columns of the frame | HOLDS (assertion not applicable) | the target is already a density in the source; no count is released, so MET-14's assertion that target x denominator rebuilds the count has nothing to rebuild. The note says why (abundance_m2 folds in area and subsampling) | MET-14 |
| M6 | The metric means on our task what it meant at the source | Metric reason; notes | target: Macoma balthica per m2, all sizes (sibes_id 59), the paper's species; zeros by the descriptor's join | HOLDS, with the settled caveat | RMSE on the density is dominated by spat: 2014 holds 75.5% of the squared deviation, the 10 densest samples 58.0%, max 99,780 /m2. All three reproduce. This is settled issue 3; today's changes do not reopen it | MET-2, MET-10 (settled) |

**Other claims, checked again because today's changes touch the frame**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| O1 | 59,044 rows, 5,092 stations, 56.0% zeros | task_summary, README | rebuilt container | HOLDS | 59,044; 5,092; 0.5601 | EV-8 |
| O2 | 769 samples without any fauna record, 342 in 2008, dropped by year | Decision 1 | raw | HOLDS | 769 / 342 | LEAK-25 |
| O3 | 71 Tellinoidea samples dropped, 29 without Macoma; 12 Tellininae samples without Macoma kept as zeros; 6 duplicated sample ids | notes | raw | HOLDS | 71 / 29 / 12 (sibes_id 389) / 6 | CLEAN-15, CLEAN-1 |
| O4 | 117 station-days hold two samples | Note | groupby(station, date) | HOLDS | 117, none with more than 2 | - |
| O5 | Elevation lifts untuned LightGBM R^2 on log1p 0.343 -> 0.376 (9/9 folds) and lowers RMSE on the density 872.8 -> 863.9 (9/9) | Elevation note | 9 shipped folds, LightGBM 300 trees, lr 0.05, with and without elevation | HOLDS (direction and size) | R^2 0.334 -> 0.371 (+0.037); RMSE 878.4 -> 869.9, lower on 9 of 9. The levels differ from the note because the hyperparameters differ. The note's numbers are dated 2026-11-02; whether they were measured under the pandas-3 bug cannot be told, but the corrected column gives the same gain, so the note stands | EV-1 |
| O6 | No test row has a feature copy in training | splits_comment | leak probe (probes/leak.txt) | HOLDS | 0.0% of 177,132 test rows | SPLIT-24 |
| O7 | One row is one core on foot or two cores bulked from a boat | task_summary.row ("One fauna sample (one core on foot, two cores bulked from a boat)") | the C1 counts | INCONSISTENT WITH D13 | 39 rows are a single boat core; the curation note says so, the summary field does not | EV-8 (Could) |

**Refuted and untested, ranked (validity first, Must first; none is Must or touches validity)**

1. C6, partly refuted (EV-8, Could): the 608 positive counts below one tellin per core.

   Changes: the note implies that the area and the subsample correction explain all non-whole counts. The descriptor's
   correction divides by the fraction, so it can only raise a count. The 608 below-one values (a tenths lattice, in
   poor samples, in every year) come from a mechanism the source does not document, perhaps fractional counts of
   damaged shells, perhaps a data error. They are 1.0% of the rows, at small densities (median 0.5 per core, about
   29 /m2), so the RMSE on the density does not feel them. No change to the target.

   Mildest remedy: one clause in the exposure note, e.g. "...are not whole numbers; the 607 below one tellin per core
   (on a 0.1 lattice) are not explained by the area or the subsample correction, which can only raise a count, and the
   descriptor documents no fractional count of bivalves." Optionally ask NIOZ.

2. C11, partly refuted (EV-8, Could): "the latest vaklodingen survey on or before the sample's date".

   Changes: 94% of the vaklodingen dates are nominal labels on the 1st of a month, mostly 1 January. For 19.3% of the
   samples the chosen survey is labelled 1 January of the sample's own year, and some of those were measured later
   (a file "_20220101_VlieBi_22_12_31"). The feature stays known at the prediction point under the use case: a map of a
   past survey is drawn from the whole archive, and bed elevation is no outcome. Taking only earlier calendar years
   costs R^2 0.0015.

   Mildest remedy: reword to "the latest survey whose date label (often 1 January of the survey year, from
   Rijkswaterstaat's file names) is on or before the sample's date". Keeping the code is fine. The stricter
   alternative, an earlier calendar year (cut = 31 December of the year before), costs 0.0015 R^2.

3. O7, inconsistent (EV-8, Could): task_summary.row says one core on foot or two bulked from a boat; 39 rows are
   one boat core.

   Mildest remedy: "(one core on foot, two cores bulked from a boat, one boat core in 39 samples)".

4. C12, untested part: whether the 1-ulp parse differences between pandas 2.3 and 3.1 (51 target values) change the
   container checksum.

   Changes: nothing for scores; a build under the other pandas may report a different checksum.

   Mildest remedy: none needed now. If the checksum is pinned, note the pandas version it was computed with.

5. C5, depends on the tolerance: 2,480 / 607 is the run's count; abs tolerance 1e-3 gives 2,505 / 608.

   Mildest remedy: none, or name the tolerance.

Everything else listed holds: D13's numbers (C1-C4), the elevation fix (C8-C10), the unweighted scoring with no
sample weight (C7, MET-15, immaterial by measurement), the fallback's reason and its ranking claim (M1-M3, MET-1,
MET-11), computability on all 9 folds (M4, MET-2), MET-14 (M5), and the counts the notes carry (O1-O6).

Sources looked at: Lyashevska et al. 2016, https://pmc.ncbi.nlm.nih.gov/articles/PMC4729254/ ; Bijleveld et al. 2025
(SIBES descriptor), https://pmc.ncbi.nlm.nih.gov/articles/PMC11814293/ ; the vaklodingen netCDF attributes of
tile KB127_1514 (time units, isource flag_meanings).

</details>

<details><summary>Column audit</summary>

**Column auditor: wadden_sea_sibes_macoma_abundance (exposure re-review, 2026-11-06)**

Definition: dataset.py after the elevation fix.
Frame loaded through dataset_io.from_definition under pandas 3.1.1: 59,044 rows, 10 columns, 8 features, no scoring column, no sample weight.

VERDICT: fine. No leak, no cleaning problem that needs a change. The core area is an amount at risk planned by the
protocol, not realized through the outcome; the only effort the abundance sets (the lab's subsample fraction) is
inside the target and in no column. The elevation fix works and the shipped values match an independent re-read of
the source tiles. Two documentation notes (N1, N2) and one question (Q1), all P7 or wording.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| station | SIBES sampling_station_id, a fixed position (500 m grid or random) | yes, the place | category, 5,092 levels; group column, dropped from the features by feature_columns (LEAK-33); one position, one basin, one flat per station (0 exceptions) | fine | LEAK-33, SPLIT-1 |
| date | the day of the sample (survey date; June-October, 2008-07-14 to 2022-09-16) | yes (each area is sampled in the same period each year; a neighbour's day changes R^2 by -0.0003, settled) | datetime64, %Y-%m-%d, no missing | fine | USE-3 (settled) |
| tidal_basin | tidal_basin_name in samples.csv, 12 basins | yes, a fixed name of the place | category, no missing | fine | - |
| tidal_flat | tidal_flat_name, 41 named flats (18 of them span more than one basin, so not nested) | yes | category, no missing | fine | - |
| longitude, latitude | station position, WGS84 degrees (x, y) | yes | float64, constant per station, inside 4.80-7.23 E, 52.90-53.53 N | fine | - |
| interpolated_median_grain_size_um | median grain size (um) at the station, IDW from the 8 nearest other stations of the same survey year | yes: built from other stations' sediment, not from the visit (settled, issue 5) | float64, 0 missing, 22.2-331.2 um | fine | USE-3, LEAK-7, CLEAN-19 (settled) |
| interpolated_mud_percent | mud fraction (%) the same way | yes (same) | float64, 0 missing, 0-80% (measured max 100%, IDW smooths) | fine | same |
| elevation_m_nap | metres above NAP of the station's 20 m vaklodingen cell, latest Rijkswaterstaat survey stamped on or before the sample's date | yes: a separate survey of the bed, exists for an unsampled place | float64, 5 missing (0.0085%), -10.96 to 1.44 m; see the elevation section | fine, notes N1-N2 | USE-3, CLEAN-11 |
| log1p_macoma_per_m2 (target) | log1p of Macoma balthica per m2 (abundance_m2 of sibes_id 59, zero if no row) | the outcome | float64, 0-11.51; RMSE on the density after the inverse; not a deviance, so CLEAN-16's untransformed clause does not apply | fine | MET-5, CLEAN-16 |

Dropped (checked, correctly out): sample_id (an id, no meaning; USE-3), sampling_type (grid/random design label of the visit), platform and total_surface_m2 (the visit's protocol and core area, see the exposure section), median_grain_size and percentage_mud (the visit's own jar; USE-3/LEAK-10, settled), and every other taxon of biota.csv (measured with the target).

Dtype probe (dtype_probes.py, --no-fetch): 0 of 7 columns flagged. Nothing is a code typed numeric or a count typed
categorical; no ordinal scale; no proxy missing codes (no -9/999 sentinels in any numeric column; the netCDF fill
value >1e30 is set missing before the join).

**The sampled area as an amount at risk (MET-14, MET-15, MET-16, LEAK-41)**

Two parts of effort sit behind each density:

1. The core area (total_surface_m2): 0.01732 m2 for 54,855 two-core boat samples, 0.01767 m2 for 4,150 single cores
   on foot, 0.00866 m2 for 39 single boat cores. It is PLANNED by the protocol of the place: the platform follows the
   flat (the features alone predict on foot vs boat at grouped-CV ROC AUC 0.987; elevation alone 0.795), and is fixed
   before the core is taken. Nothing ties it to the outcome: the 39 single boat cores' 79.5% zeros match what half the
   area gives by chance (77.8-82.0%), so the outcome did not set their area. The cause of those 39
   is undocumented (realized deviation of unknown cause), but they are 0.07% of rows, carry no weight and no feature.
   LEAK-41 does not bite: no column encodes a value set or cut after the prediction point. A feature predicting the
   planned area through the place (elevation, position) is USE-6's case, which LEAK-41 keeps.
2. The subsample fraction: chosen by the lab AFTER seeing the sample, for samples with many individuals, so the
   abundance sets it. It is not released and is in no column; the source folds it into abundance_m2. 2,480 of 25,974
   positive counts per core are not whole (9.55%, as the notes say), and the features do not locate them (grouped-CV
   ROC AUC 0.559 among positives). Because this part of the realized effort is set by the outcome, a weight built from
   it would itself be a LEAK-41 column; declaring no weight is the right side of that line.

MET-14: the target ships as the rate per unit (density) and the count leaves the frame (the source releases only the
density). MET-14's "_clean asserts target x denominator rebuilds it" cannot be met because no count is released; the
exposure bullet says why. Not a defect; at most worth a half-sentence (Q1).

MET-15: the decision is per unit of an equal-area map, so the rate is scored unweighted and no sample_weight is
declared. Matches the definition (dataset_io: weight_column None, no scoring columns).

MET-16: no survey or design weight exists in the release; sampling_type (grid/random) is dropped, scored unweighted
(the use case is a map, not a population total). Fine.

**Elevation after today's fix**

- Missing share: 5 of 59,044 (0.0085%), down from 40.66%; the 5 are 2008-2009 samples at stations 2942, 2996, 4008,
  4083, whose first survey is stamped 2010-01-01 or 2011-01-01 (no earlier survey), as documented. Their targets are
  mixed (2 zeros, 3 positives): the missingness is set by the survey calendar, not by the outcome; the leak probe's
  missing indicator alone scores R^2 -0.001.
- Source match: an independent re-read (brute-force nearest cell per tile, no cKDTree, no stack) of 400 random shipped
  rows at 391 stations gives 400 of 400 identical values (max abs diff 0.0). No station falls in two tiles. The
  pandas 2.3 and 3.1 runs agree (74,518 station-survey pairs, 0 NaN, 5 missing samples, median age 2.70 years).
- The panel's probes ran at 15:40-15:49, after the definition's 15:33 edit, so they score the fixed column:
  elevation is the strongest single feature (R^2 0.164 alone; without it 0.265 against 0.294 in the leak probe).
- Not set by the abundance: a Rijkswaterstaat depth survey of the bed, made on its own calendar.

N1 (P7 wording; no leak). "Latest survey on or before the sample's date" is by the netCDF's survey stamp, and 70% of
the stamps in the 40 tiles (91.4% of the stamps matched to a sample) are 1 January. 19.3% of the rows take a survey
stamped 1 January of the sample's own year, which may have been flown or sailed after the June-October sample. This
is no leak (the bed is not set by tellins, and under the archive-map moment a later survey is available too); the
comment could say "stamped" and that the stamps are mostly nominal 1 January. Remedy: one clause in the elevation
bullet, or nothing.

N2 (P7 note; CLEAN-11, unusual not wrong). 156 rows lie below -2 m NAP (35 below -3, minimum -10.96), at 84 stations
mostly in Borndiep, Marsdiep, Lauwers; median survey age 3.6 years, so not stale. These are cells in or at gullies on
flats sampled by boat; 88.5% hold no tellin against 56.0% overall, the signal a habitat model should see. 500 rows
take a survey more than 10 years old (100 rows more than 20 years, 39 stations; max 62.6 years), but the next later
survey differs from it by a median 0.13 m, so the old values are not wrong. Keep both as they are; the existing
"98.0% within 6 years" covers it.

**Columns the abundance may set (searched)**

- Subsample fraction: set by the abundance, but only inside the target (above). No column.
- Interpolated sediment: its sources are other stations' measured sediment. The measured jar is missing slightly more
  often where the core holds no tellin (6.9% against 4.5%), so the source set of the IDW depends weakly on neighbours'
  outcomes; each row has 8 sources and a missing one is replaced by the next neighbour, so no row's value carries its
  own label. Negligible; no remedy.
- Elevation: no (separate survey). Date, basin, flat, position: fixed by the design.
- Row selection: the Tellinoidea drop reads another taxon's record (settled, CLEAN-15); the 2008 no-record drop is
  located by the year (settled, LEAK-25). Neither reopened today.
- The target's precision marks the core area (one tellin = 57.7, 56.6 or 115.5 per m2) but the target is no feature.

**Problems ranked (principles.md)**

No P1-P6 problem. P4 (LEAK-41, MET-15) checked and clear: no realized or outcome-set amount at risk is a feature or a
weight; the planned core area is out of the features by USE-3 (an unsampled place has no visit), and the features that
predict it are known at the prediction point (USE-6).

P7, notes only:

- Q1 (MET-14, question for the curator, mildest remedy: half a sentence or nothing): MET-14 asks _clean to assert that
  target x denominator rebuilds the count; with no count released and an unreleased subsample fraction, the
  assertion cannot be written. The exposure bullet explains the effort but not why the MET-14 assertion is absent.

- N1 (wording): elevation joined by survey stamp; most stamps are nominal 1 January; 19.3% of rows use a survey stamped
  1 January of their own year. Remedy: "stamped on or before".

- N2 (CLEAN-11): 156 rows below -2 m NAP and 100 rows on a survey more than 20 years old; unusual, not wrong. Keep.

Side observation (already in the notes, not new): 608 positive samples hold less than one tellin per core (common
values 0.5, 0.8, 0.4 per core; 28.8% of them have zero AFDM against 1.3% overall), consistent with fragments or
subsample corrections the source standardised; the D13 notes count them (607 by the notes' tolerance). No remedy.

</details>

<details><summary>Task gamer</summary>

**Task gamer: wadden_sea_sibes_macoma_abundance (log1p Macoma density, RMSE on the raw ind/m2 scale, grouped by station)**

Verdict: I found no exploit. Nothing beats the honest model by more than the noise of a random column. The score depends mostly on which of a few 2014 spatfall outliers land in a test fold, not on leaked information.

Scores (mean RMSE over the 9 shipped splits, ind/m2, lower is better)

```text
  constant (train mean)                                883.88
  baseline: untuned LightGBM on the log1p target       862.43  (per split 563.6 - 1077.2)
    + a random column, 3 seeds                         863.91 / 864.01 / 864.22  (noise about +-2)
  honest: LightGBM fitted on the raw density           846.99  (551.2 - 1060.2)
    + a random column, 3 seeds                         849.04 - 849.80 (noise about +-1.5)
  honest + winsorised training target (q 0.999)        840.99  (539.4 - 1057.3)
```

The baseline fits the log, so it predicts something close to a geometric mean. On a raw-scale RMSE that loses. Fitting the raw density, or winsorising it, is a modelling choice and not a flaw of the task. I compare the exploits below with the honest raw-scale model (846.99).

Exploits ranked by gain

| # | Exploit | Script | Honest | Exploited | Gain | Deployed has it? | Fix |
|---|---|---|---|---|---|---|---|
| - | none beyond noise | - | 846.99 | - | - | - | - |

Candidates measured (gain = honest minus exploited; a negative number means worse):

 1. Day-level counts over all rows (number of stations sampled that day, number of rows per flat and year, day of week): 846.77, gain +0.22, within noise. These come from the survey log, and a deployed model has them. Signal, not an exploit.
 2. Labels of the same-year neighbours from training stations (nearest, IDW of the 8 nearest, share of non-zero, within a 500 m grid): 847.61, gain -0.6. IDW alone: 904.2. A mapping model would have the neighbours of the same survey, so this is legitimate kriging, and it does not help here either: a single 0.017 m2 core is too noisy.
 3. Elevation-missing flag (5 rows; 3 of them non-zero): 846.99, gain 0.00. Elevation is not missing because of the outcome.
 4. Sampled area / sampling method. The task has no such column. The grid of target values gives it away: density = count / area, with units of 57.74 (boat, 2 cores, 0.0173 m2, 21,443 non-zero rows), 56.59 (foot, 1 core, 0.0177 m2, 2,454 rows) and multiples from subsampling (28.9, 23.1, 40.4, 5.77...). The paper says boat 0.0173 m2 and foot 0.0177 m2, and foot stations are high and near the shore. In the kit, foot rows have a mean elevation of +0.14 m, against -0.26 m for boat rows. That is why the area is not cleanly recoverable from the features: elevation stands in for it only partly, and elevation is a legitimate feature. No feature encodes the area or the subsample fraction, so I cannot measure a gain from them. If a column for the core type or the subsample were added, it would leak little anyway: it is only identifiable for non-zero rows.
 5. Format-only features (decimal counts of lon/lat, minute fractions, elevation-missing flag, mud == 0 sentinel, decimal count of grain size): alone 889.88, worse than the constant 883.88. Added to the honest model: 848.39, gain -1.4. The classes were not recorded differently.

Flaws that hurt an honest model

None that come from the task construction. Training rows are the same kind of rows as test rows (grouped random split, no time column in the regime). The 117 station-years that appear twice (an identical pair of feature rows with two cores) stay within one group, so they cannot cross the split.

Design note (not an exploit): RMSE on the raw scale is dominated by a handful of rows. The top 10 densities (up to 99,780/m2, nearly all in the 2014 spatfall) carry 57% of the total sum of squares, and the top 50 carry 74%. Per-split RMSE ranges from 551 to 1060 depending on where they fall, and the best honest model is only 4-5% better than the constant. A log-scale metric (RMSLE, i.e. RMSE on the shipped log1p values) would rank models on the bulk of the data. The mildest fix: drop target_transform from the metric, or make the metric RMSE on the log1p scale.

Attacks that found nothing (numbers above or here)

  - Row order: correlation between row position and target 0.006. Next-row agreement on zero vs non-zero 0.508 against 0.507 expected by chance. Station id against target: r = -0.008 (and the station id is not a feature).
  - Copies across the split: coordinates map one-to-one to the station (5,092 coordinate pairs = 5,092 stations), so no test station's coordinates appear in training. The nearest training neighbour's label is attack 2.
  - Train-vs-test classifier (grouped 5-fold, first 3 splits): AUC 0.504-0.521. Train/test mean density 144-151.
  - Last digit of elevation against the target: non-zero share 0.42-0.46 for every digit. 0.04% of elevations have more than 2 decimals.
  - Transforms over all rows: none found. The sediment columns are interpolated per row and per year (about 11.6 distinct values per station), not standardised or ranked.
  - Unprocessed samples recorded as zeros: the paper says only 2,831 (2017) and 2,274 (2018) stations were processed, while the kit has 4,129 and 4,128 rows. But no flat has a 100% zero rate in those years (2017 zero share 0.67, 2018 0.50), so I see no block of fake zeros. A later dataset version probably processed them; I could not confirm this.
  - Lookup in the published source file (NIOZ SIBES dataset, station + date): this would work, as for any public dataset. Not ranked.

What I could not check

  - The raw NIOZ files (biota.csv / samples.csv), to confirm the processing status of 2017/2018 and the subsample fractions per row. Not downloaded.
  - How the "interpolated" sediment values and the elevation were built (which years and which sources). If the interpolation included sediment from later surveys, it would still not touch the target.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC11814293/ (SIBES data descriptor, Sci Data 2025), https://doi.nioz.nl/dataset/sibes-dataset

</details>
