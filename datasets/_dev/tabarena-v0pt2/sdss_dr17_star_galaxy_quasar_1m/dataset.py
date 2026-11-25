"""Curated dataset definition for `sdss_dr17_star_galaxy_quasar_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.collections import TABARENA_V0PT2_ROW_BUDGET
from data_foundry.v2 import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Source,
    SplitPlan,
    TaskSummary,
    Temporal,
)
from data_foundry.v2.splits import sample_temporal_splits

# The SkyServer columns under the names of the Kaggle cut `sdss_17` uses, so both definitions read alike.
RENAME = {
    "objid": "obj_ID",
    "ra": "alpha",
    "dec": "delta",
    "run": "run_ID",
    "rerun": "rerun_ID",
    "camcol": "cam_col",
    "field": "field_ID",
    "specobjid": "spec_obj_ID",
    "mjd": "MJD",
    "fiberid": "fiber_ID",
    **{f"psfmag_{band}": f"psfMag_{band}" for band in "ugriz"},
    "type": "photo_type",
}
MAGNITUDES = ["u", "g", "r", "i", "z"]
PSF_MAGNITUDES = [f"psfMag_{band}" for band in MAGNITUDES]
EXTINCTIONS = [f"extinction_{band}" for band in MAGNITUDES]
# The imaging pipeline's object type (`PhotoType` of SkyServer's schema), decoded to its names: 3 extended, 6 point source.
PHOTO_TYPES = {
    0: "UNKNOWN",
    1: "COSMIC_RAY",
    2: "DEFECT",
    3: "GALAXY",
    4: "GHOST",
    5: "KNOWNOBJ",
    6: "STAR",
    7: "TRAIL",
    8: "SKY",
    9: "NOTATYPE",
}
# The test windows (first day, day after the last; None: the end of the data), newest first, one per targeting era
# (2026-11-25, Andrej): 2019 with 2020 (1 January 2019 to 24 March 2020, the end of eBOSS and eFEDS; 2019 and 2020 form
# one window as in `sdss_17`), the calendar year 2016 (eBOSS) and the calendar year 2013 (BOSS).
WINDOWS = (
    (pd.Timestamp("2019-01-01"), None),
    (pd.Timestamp("2016-01-01"), pd.Timestamp("2017-01-01")),
    (pd.Timestamp("2013-01-01"), pd.Timestamp("2014-01-01")),
)


class SdssDr17StarGalaxyQuasar1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a sky object a galaxy, a star or a quasar, judging from its images alone?",
        use_case=(
            "For example, an astronomer classifies objects that have images but no spectrum, to choose targets for "
            "spectroscopy or to build catalogues."
        ),
        row=(
            "One object with a spectrum in the Sloan Digital Sky Survey's Data Release 17: every primary optical "
            "spectrum with a photometric object whose class the survey's pipeline does not flag, 4,249,921 objects "
            "observed from February 2000 to March 2020."
        ),
        predicted=(
            "The class the survey's spectroscopic pipeline assigned: galaxy (61.60%), star (20.73%) or quasar (17.68%)."
        ),
        known=(
            "The sky position, the brightness in five colour bands (u, g, r, i, z) from the survey's images, fitted "
            "to the object's shape and as a point source (PSF magnitudes), the imaging pipeline's call of extended "
            "or point source, the dust extinction in each band and the camera column. The date of the spectrum "
            "orders the split but is no model input: it arrives with the class."
        ),
        split=(
            "Later spectra: three periods, one in each targeting programme, are each predicted by a model trained on "
            "every spectrum taken before it, as the survey's classifier would be refit at a data release and used "
            "on the objects observed next: January 2019 to March 2020 (the end of eBOSS, then eFEDS), the year 2016 "
            "(eBOSS) and the year 2013 (BOSS)."
        ),
        changes=(
            "We drop the redshift, fitted with the class, the plate and fibre, which record how the object was "
            "chosen, and the spectra the pipeline flags as unreliable. We add the PSF magnitudes, the imaging's "
            "object type and the dust extinction. We split by the date of the spectrum, testing on three periods, "
            "2019 and 2020 together, 2016 and 2013."
        ),
        fit="approximate",
        fit_reason=(
            "The features exist before a spectrum, but every row is an object the survey's targeting programmes "
            "already picked by its colours for a spectrum, so the mix of classes and colours is not that of the "
            "objects one would classify without one. Each programme picked its own kind of object, so the class mix "
            "of later years differs (quasars 13-16% of the spectra in 2010-2013, 31-51% from 2014)."
        ),
    )

    # Dataset
    unique_name = "sdss_dr17_star_galaxy_quasar_1m"
    domain = "physics & astronomy"
    sources = (
        Source(
            role="publication",
            platform="Other",  # SDSS Data Release 17, queried from SkyServer's public SQL search
            url="https://www.sdss4.org/dr17/",
            license="Public Domain",  # "All SDSS data released in our public data releases are considered in the public domain"
            year="2021",
            bibtex="""
                @article{accetta2022seventeenth,
                  title={The seventeenth data release of the Sloan Digital Sky Surveys: Complete release of MaNGA, MaStar, and APOGEE-2 data},
                  author={Accetta, Katherine and Aerts, Conny and Aguirre, Victor Silva and Ahumada, Romina and Ajgaonkar, Nikhil and Ak, N Filiz and Alam, Shadab and Prieto, Carlos Allende and Almeida, Andres and Anders, Friedrich and others},
                  journal={The Astrophysical Journal Supplement Series},
                  volume={259},
                  number={2},
                  pages={35},
                  year={2022},
                  publisher={IOP Publishing}
                }
            """,
        ),
        Source(
            role="copy",
            platform="Other",
            url="https://skyserver.sdss.org/dr17/SearchTools/sql",
            license="Public Domain",
            name="SkyServer's SQL search, which we query",
        ),
    )
    download_description = """
        We query SkyServer's public SQL search (no account) for every spectrum of `SpecObj` (DR17's primary spectra,
        `sciencePrimary`) with its photometric object in `PhotoObj`: the query behind the Kaggle cut `sdss_17`,
        without its `TOP 100000`. The service returns at most 500,000 rows per query, so we fetch 11 ranges of
        nights (MJD), each under the limit; every file starts with a `#Table1` line and holds a header and its rows
        (4,618,753 in all, 1,227 MB). The query adds to the Kaggle cut's 18 columns the five PSF magnitudes of
        `PhotoObj`, its object type `type` and Galactic extinction `extinction_u` to `extinction_z`, and the spectrum's
        quality flags `zWarning`.

        mkdir -p local-data-warehouse/sdss_dr17_star_galaxy_quasar && cd local-data-warehouse/sdss_dr17_star_galaxy_quasar && COLS="p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z,p.psfMag_u,p.psfMag_g,p.psfMag_r,p.psfMag_i,p.psfMag_z,p.type,p.extinction_u,p.extinction_g,p.extinction_r,p.extinction_i,p.extinction_z,p.run,p.rerun,p.camcol,p.field,s.specobjid,s.class,s.z AS redshift,s.zWarning,s.plate,s.mjd,s.fiberid" && for range in "51578 52710" "52721 53565" "53566 54573" "54574 55514" "55517 55854" "55855 56073" "56074 56384" "56385 56934" "56935 57712" "57713 58223" "58224 58932"; do set -- $range; sql="SELECT $COLS FROM PhotoObj AS p JOIN SpecObj AS s ON s.bestobjid = p.objid WHERE s.mjd BETWEEN $1 AND $2"; enc=$(python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))" "$sql"); curl -sS -f -m 900 -o "chunk_$1_$2.csv" "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch?cmd=$enc&format=csv"; sleep 5; done && cd ../..
    """
    curation_comments = """
        We start with the 11 CSV files of SkyServer's SQL search for DR17 (`download_description`): 4,618,753
        primary spectra of `SpecObj` joined to their photometric objects in `PhotoObj` on `bestobjid`, the 18 columns
        of the Kaggle cut `sdss_17` (which is this query cut at 100,000 rows in database order; all its 99,999 objects
        are here) and the PSF magnitudes, `type`, the extinctions and `zWarning`. The other 492,959 of DR17's 5,112,724 primary spectra have
        no photometric object (`bestobjid` = 0): almost all are sky fibres and spectra without a target type, nearly
        all flagged by `zWarning`, and they have no features to classify with. The files are the release as published; no other file is read. The nights the ranges leave out
        (MJD 52711 to 52720, 55515 and 55516) hold no spectrum of the join: the row count of every range equals the
        join's count per night.
        - Larger than the row budget: the training sides hold 2,769,428 to 4,197,395 spectra, so the dataset ships as
          the `_1m` version: every window keeps all earlier spectra on its training side, a benchmark draws 1M of
          them before a fit, and each test window holds at most 500,000 spectra (none of the three is cut; 2013,
          the largest, holds 447,141).
        - We renamed the columns to the Kaggle cut's names and the target to "ObjectType".
        - We drop the 368,771 spectra (7.98%) whose class the source flags as unreliable, `zWarning` not 0 (the
          spectroscopic pipeline's own quality bitmask, sdss4.org/dr17/algorithms/bitmasks; Bolton et al. 2012), as
          that flag directs and as SDSS training sets do (2026-11-25, Andrej): 172,453 labelled galaxy, 81,158 star
          and 115,160 quasar, 6.2%, 8.4% and 13.3% of each class. 19,581 of them come from fibres that carried no
          light from the object, a class fitted to no object's light: 18,513 UNPLUGGED, "the fiber was unplugged or
          damaged, and the location of any spectrum is unknown" (17,948 labelled galaxy; median signal-to-noise 0),
          and 1,068 more NODATA, "No data for this fiber, e.g. because spectrograph was broken during this
          exposure", all labelled galaxy. About 91% of the rest are flagged only as SMALL_DELTA_CHI2, the best class
          template barely ahead of the next. A flagged class is unstable: of the same 91,063 spectra of December
          2011 to February 2012, 26.8% of the flagged ones changed class from DR12's pipeline (v5_7_0) to DR17's
          (v5_13_2), against 0.43% of the clean ones. The flagged share grows over time (3.7% of the spectra before
          2012, 15-22% of each test window from 2016), so the drop takes most from the newer windows and from the
          quasars, and it changes which objects are scored: the ones the pipeline could not decide leave. They leave
          before the position dedup, so an object whose flagged spectrum has a clean one at the same position keeps
          the clean one (2 positions). `sdss_17` keeps them only because its Kaggle file has no `zWarning`.
        - We sort the spectra by night, plate and fibre, which name one spectrum: the service returns the rows of a
          query in no fixed order (a second fetch of the newest range held the same rows in another order), and the
          sort keeps the frame, and so the test-window draw, the same from fetch to fetch.
        - We keep one spectrum per sky position ("alpha", "delta"), the earliest: 61 positions carry two spectra of one
          photometric object, taken 0 to 5,509 nights apart (median 2,536), and at 2 of them the two classes differ;
          the later spectrum would be a test row whose object the model saw with a label (4,249,921 objects remain).
        - We dropped the identifiers ("obj_ID", "spec_obj_ID"), the imaging run, rerun (constant) and field, which
          name the image, not the object.
        - We drop "redshift". The SDSS pipeline fits the class and the redshift in the same step, and stars are only
          fitted within +-1200 km/s (Bolton et al. 2012, Sec. 3.1), so a redshift near zero identifies stars almost
          perfectly. The task is photometric: classify an object from its position and u, g, r, i, z magnitudes, as
          in `sdss_17` (2026-11-11, Andrej), and from the PSF magnitudes below.
        - We drop "plate" and "fiber_ID". A plate is one spectroscopic pointing designed for one targeting programme,
          so it encodes how the object was pre-selected from photometry rather than what it is, and a new object has
          no plate before it is targeted; the fibre is a slot on the plate (as `sdss_17`).
        - We add the PSF magnitudes "psfMag_u" to "psfMag_z": the brightness of the object fitted as a point source,
          from the same images and the same catalogue as the model magnitudes, known before any spectrum. The
          difference of PSF and model magnitude is how SDSS separates stars from galaxies (the imaging pipeline's own
          star/galaxy `type` is a cut on it), and every photometric classifier of the literature reads it. `sdss_17`
          has no PSF magnitudes only because the Kaggle file held none; our own query has them, so the feature set
          now goes beyond `sdss_17`'s, for the same task. Measured by two reviewers in four tests on the windows
          (LightGBM, before the flagged spectra were dropped), they lower the log loss by 0.09 to 0.15.
        - We add the imaging pipeline's object type, "photo_type" (`PhotoObj.type`, its codes decoded to the names
          of SkyServer's `PhotoType`: GALAXY, an extended object, 2,635,130; STAR, a point source, 1,614,692;
          UNKNOWN 99), and the Galactic extinction "extinction_u" to "extinction_z", from the same `PhotoObj` row as
          the magnitudes (2026-11-25, Andrej): a practitioner classifying an object without a spectrum reads both from
          the imaging catalogue, which holds them for every imaged object, at training and at prediction time. The
          type is a fixed rule of the imaging pipeline, a point source when the PSF magnitude is at most 0.145
          fainter than the cModel magnitude; no label went into it. It is GALAXY for 97.1% of the galaxies and STAR
          for 94.4% of the quasars and 94.3% of the stars, and the other shipped columns predict it at about 98%
          (LightGBM, the two newest windows). The extinction is the dust map's reddening at the object's position
          times a fixed coefficient per band, so the five columns are one number (correlation 1.000; u, g, i, z at
          1.855, 1.446, 0.743 and 0.553 times r; none missing); the position carries part of it. Measured on the two
          newest windows before they were added (LightGBM, log loss): the type lowered it by 0.004 to 0.005, the
          extinction by nothing; they are added because the practitioner has them, not for the score. Like the
          magnitudes, both are DR17's imaging catalogue, not the version an astronomer had at a window's start.
        - We set the sentinel -9999 to missing: 149 objects carry it in one or more bands of either magnitude (99 to
          135 per band), 99 of them in all five.
        - "u", "g", "r", "i", "z" are the model magnitudes of DR17's imaging catalogue. DR17 adds no imaging ("Data
          Release 17 does not include any new or updated SDSS imaging data", sdss4.org/dr17/imaging), and its
          catalogue magnitudes carry the DR13 recalibration of the zero points ("the DR13 hypercalibration has been
          applied to the catalogs"; Finkbeiner et al. 2016), so the photometry of an object observed in 2003 is as
          recalibrated in 2016, not as an astronomer had it then. The recalibration is of the whole imaging
          catalogue against an external survey, made without the spectra's classes, and it is the photometry a user
          of the catalogue classifies with today.
        - Split by the year of the spectrum instead of at random, as `sdss_17` (2026-11-11, Andrej). Every row is a
          spectrum taken on a dated night (the raw "mjd", now the time column "date") through a plate drilled for
          one targeting programme, and the programmes changed what they observed: quasars are 2-10% of each year's
          spectra in 2000-2009, 13-16% in 2010-2013 and 31-51% from 2014 on. A classifier in use is trained on the
          spectra taken so far and labels objects the survey has not yet observed.
        - We keep "MJD" out of the features and bring it back only as the time column "date": the date orders and
          splits the rows and is no model input (`Temporal(..., time_of="label")`), since the date of an object's
          spectrum arrives with its class (2026-11-12, Andrej).
        - Re-observed objects, kept: 5.6-7.7% of the primary spectra of 2010-2020 (8-14% of the quasars) belong to an
          object that had an earlier spectrum in `SpecObjAll`, eBOSS and TDSS re-observations of known quasars and
          replacements of poorer spectra (counted on SkyServer among all primary spectra, before the flagged ones were
          dropped). The earlier spectrum is not in the data and the object appears once, so no copy crosses the
          split, but these objects were picked for a class the survey already had, unlike the use case's objects without a spectrum (part of the `Selection Bias`).
        - We keep the sky position ("alpha", "delta") as `sdss_17` does: it is known from the images before any
          spectrum. Under the year windows it mostly records which targeting programme's footprint an object lies
          in, and the footprints move from year to year: adding it to the model magnitudes raised LightGBM's log
          loss in every window measured, by 0.013 to 0.066 (mean 0.033, five windows, before the PSF magnitudes
          were added and the flagged spectra dropped); alone it scores worse than the class shares. A method that
          learns to discount it under the drift does better, which is part of the task. "cam_col" changes the log
          loss by at most 0.001.
        - Worth benchmarking, measured in one run (the task probe, the three windows, untuned, log loss): LightGBM
          0.232, random forest 0.252, logistic regression 0.346, the best single feature ("photo_type" in 2 windows,
          `psfMag_u` in the other) 0.520, the class shares 1.130; LightGBM beats the class shares in every window.
        - Potential leak, kept on purpose (LEAK-9, an evaluation leak): features built from the other test rows of a
          window, the unlabelled objects observed in the same year in the same patch of sky, tell a model which
          programme observed the patch and lowered the mean log loss by 0.047 in a reviewer's test (before the flagged
          spectra were dropped). A deployed classifier choosing targets from the images does not know which objects
          get a spectrum that year. Each test object is predicted from the training rows and its own features only;
          no feature or model step may use other test rows, and a method that learns from the test window is called
          out and not benchmarked.
    """

    # Task
    target = "ObjectType"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "SDSS DR17 (Abdurro'uf et al. 2022) is a data release with no prediction task or metric; SkyServer's "
            "documentation defines none either, and the Kaggle cut `sdss_17` of the same query is a dataset page, "
            "not a competition. Our task (photometric classification, redshift, plate and fibre dropped) also "
            "differs from the SDSS pipeline's spectroscopic classification."
        ),
    )

    split_leaf = "L-ORDER.windows"
    # Splits: three windows, one per targeting era, the test sides capped (`_make_splits`)
    temporal = Temporal(
        on="date",
        horizon=1,
        horizon_unit="years",
        time_of="label",  # the date of the spectrum arrives with the class: no model input (2026-11-12, Andrej)
    )
    splits_comment = """
        Three windows, newest first, one per targeting era: 1 January 2019 to 24 March 2020 (the end of eBOSS on 1
        March 2019, then eFEDS), the calendar year 2016 (eBOSS) and the calendar year 2013 (BOSS) (2026-11-25,
        Andrej). Each trains on every spectrum taken before it, as a classifier refit at a yearly data release (DR8,
        January 2011, to DR16, December 2019) would. Three is the target for this size: SPLIT-15 aims the number of
        windows at the splits an IID split would get, SPLIT-33's count for two thirds of the 4,249,921 objects, one
        repeat of 3 folds. The eight yearly windows of `sdss_17` (2012 to 2018, 2019-2020) came from its 100,000 rows,
        whose target is 9. The windows are spread over the eras because the targeting programme sets the class mix:
        BOSS used all the dark time until June 2014, eBOSS half of it until 1 March 2019, and quasars are 15.6% of
        the 2013 spectra, 42.4% of 2016's and 50.3% of 2019-2020's.

        The windows hold 52,526 (2019-2020), 179,009 (2016) and 447,141 (2013) spectra, all scored (a test window
        keeps at most 500,000, drawn at random within the classes). Each train side holds every earlier spectrum:
        4,197,395 (98.8% of the 4,249,921 objects, 2019-2020), 3,564,868 (83.9%, 2016) and 2,769,428 (65.2%, 2013),
        and a benchmark sub-samples it to 1M rows (by default rows drawn at random from the newest year before each
        window, extended back in time until it holds that many rows, `subsample_train`).

        No gap: the user is the survey team, which has its reduced spectra, and so the classes, within days and
        plans the next plates from them. A public user waits for the next release, whose newest spectra are 0.5 to
        3.5 years old at a window's start; a window's length is not that gap. Measured on the eight yearly windows
        before the flagged spectra were dropped (LightGBM, mean log loss): no gap 0.450, a 6-month gap 0.495, 18
        months 0.590, the public release at each window's start 0.635 (release cutoffs from the release papers, not
        checked).

        2020 holds only 8 plates (4,265 spectra kept, 5 nights) of one programme (eFEDS), observed before the
        observatory closed for COVID-19 on 24 March 2020: an atypical newest window, so it is merged with 2019 (48,261
        spectra kept, 72 plates), as in `sdss_17` (2026-11-12, Andrej).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        # 11 files, one per range of nights; each starts with a "#Table1" line. The spectrum id exceeds int64.
        files = sorted(Path(raw_dir).glob("chunk_*.csv"))
        assert len(files) == 11, f"Expected the 11 SkyServer files, found {len(files)}."
        return pd.concat(
            [pd.read_csv(f, skiprows=1, dtype={"specobjid": str, "class": str}) for f in files], ignore_index=True
        )

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # SkyServer writes some headers in mixed case ("psfMag_u", "zWarning"): lower case first, then the Kaggle names.
        df = raw.rename(columns=str.lower).rename(columns=RENAME)
        # Spectra the source flags (zWarning not 0): classes DR17 itself does not stand behind, among them the fibres
        # that carried no light (UNPLUGGED, NODATA). Dropped before the position dedup, so an object whose flagged
        # spectrum has a clean one at the same position keeps the clean one (2026-11-25, Andrej).
        df = df[df["zwarning"].astype("int64") == 0]
        # The imaging pipeline's star/galaxy call, decoded to the schema's names (2026-11-25, Andrej).
        codes = df["photo_type"].astype("int64")
        assert codes.isin(PHOTO_TYPES.keys()).all(), "A `type` code outside SkyServer's PhotoType."
        df["photo_type"] = codes.map(PHOTO_TYPES)
        target_feature = "ObjectType"
        df = df.rename(columns={"class": target_feature})
        df[target_feature] = df[target_feature].str.strip()
        # The night the spectrum was taken, as a date: the split's time column, never a feature (2026-11-11, Andrej).
        df["date"] = pd.to_datetime(df["MJD"], unit="D", origin=pd.Timestamp("1858-11-17"))
        # A fixed row order (the service returns rows in no fixed order); night, plate and fibre name one spectrum.
        df = df.sort_values(["MJD", "plate", "fiber_ID"], kind="stable")
        # One spectrum per sky position, the earliest (61 positions with two spectra of one photometric object).
        df = df.drop_duplicates(subset=["alpha", "delta"]).reset_index(drop=True)
        assert df["obj_ID"].is_unique, "One photometric object per row after the position dedup."
        # The imaging pipeline's sentinel for a magnitude it could not measure.
        df[MAGNITUDES + PSF_MAGNITUDES] = df[MAGNITUDES + PSF_MAGNITUDES].replace(-9999, np.nan)
        df = df.drop(
            columns=[
                "obj_ID",  # photometric object id
                "spec_obj_ID",  # spectrum id
                "run_ID",  # imaging run: names the image, not the object
                "rerun_ID",  # constant (301)
                "field_ID",  # imaging field within the run
                "MJD",  # observation night, now the time column "date"
                "redshift",  # fitted together with the class by the spectroscopic pipeline
                "plate",  # spectroscopic pointing: observation date and targeting programme
                "fiber_ID",  # slot on the plate
                "zwarning",  # the spectroscopic pipeline's quality flags, set with the class
            ]
        )
        return df

    def _make_splits(self, df: pd.DataFrame) -> SplitPlan:
        """The windows of `WINDOWS`, newest first, each training on every spectrum taken before its start, no gap; each
        test window capped at the collection's test budget, a random draw within the classes.
        """
        dates = df["date"]  # the frame arrives sorted by date with a RangeIndex
        positions = np.arange(len(df))
        splits = {}
        for start, end in WINDOWS:
            test = (dates >= start) & (dates < end) if end is not None else dates >= start
            train = dates < start
            splits[len(splits)] = {0: (positions[train.to_numpy()], positions[test.to_numpy()])}
        frame, splits, _ = sample_temporal_splits(
            df,
            splits,
            TABARENA_V0PT2_ROW_BUDGET,
            stratify_on=self.target,
            random_state=self.SPLIT_RANDOM_STATE,
        )
        return SplitPlan(splits=splits, df=frame)

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # cam_col names which of the six camera columns took the image: a code, not a quantity (as `sdss_17`);
        # photo_type is the imaging pipeline's class, a code decoded to its names (the extinctions stay numeric)
        return FeatureTypes(categorical=["cam_col", "photo_type"], datetime=["date"])
