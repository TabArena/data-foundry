"""Curated dataset definition for `desi_dr1_star_galaxy_quasar_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    decode,
    drop_columns,
)

RAW_FITS = "zall-pix-iron.fits"
PREPARED = "zall_pix_iron_main.parquet"

# The columns we read from the redshift catalogue (136 columns, 787 bytes a row): the target, the filters of the
# release's "useful spectra", the photometry and astrometry the targeting saw, and, for the evidence only, the
# targeting decision and the spectroscopic fit (dropped in `_clean`).
READ_COLUMNS = (
    # identity and the release's quality filters
    "TARGETID", "SURVEY", "PROGRAM", "OBJTYPE", "ZWARN", "ZCAT_PRIMARY", "MAIN_PRIMARY", "HEALPIX",
    # the target and the spectroscopic fit (after the spectrum)
    "SPECTYPE", "Z", "ZERR", "DELTACHI2",
    # the targeting decision (before the spectrum, but it is the pre-selection by class)
    "DESI_TARGET", "BGS_TARGET", "MWS_TARGET", "SCND_TARGET", "PRIORITY_INIT", "NUMOBS_INIT",
    # Legacy Surveys DR9 imaging (Tractor) and Gaia: known before the spectrum
    "TARGET_RA", "TARGET_DEC", "PHOTSYS", "RELEASE", "EBV", "MORPHTYPE",
    "FLUX_G", "FLUX_R", "FLUX_Z", "FLUX_W1", "FLUX_W2",
    "FLUX_IVAR_G", "FLUX_IVAR_R", "FLUX_IVAR_Z", "FLUX_IVAR_W1", "FLUX_IVAR_W2",
    "FIBERFLUX_G", "FIBERFLUX_R", "FIBERFLUX_Z", "FIBERTOTFLUX_G", "FIBERTOTFLUX_R", "FIBERTOTFLUX_Z",
    "MASKBITS", "SERSIC", "SHAPE_R", "SHAPE_E1", "SHAPE_E2",
    "REF_CAT", "REF_EPOCH", "GAIA_PHOT_G_MEAN_MAG", "GAIA_PHOT_BP_MEAN_MAG", "GAIA_PHOT_RP_MEAN_MAG",
    "PARALLAX", "PMRA", "PMDEC",
)  # fmt: skip
LOGICAL_COLUMNS = ("ZCAT_PRIMARY", "MAIN_PRIMARY")
BANDS = ("G", "R", "Z", "W1", "W2")

# Legacy Surveys DR9 MASKBITS (https://www.legacysurvey.org/dr9/bitmasks/), the bits set in at least one row.
MASKBITS = {
    0: "NPRIMARY", 1: "BRIGHT", 2: "SATUR_G", 3: "SATUR_R", 4: "SATUR_Z", 5: "ALLMASK_G", 6: "ALLMASK_R",
    7: "ALLMASK_Z", 8: "WISEM1", 9: "WISEM2", 11: "MEDIUM", 12: "GALAXY", 13: "CLUSTER",
}  # fmt: skip

# Codes in the words of the Legacy Surveys DR9 catalogue page (https://www.legacysurvey.org/dr9/catalogs/).
CODE_LABELS = {
    "PHOTSYS": {"N": "north (BASS g, r; MzLS z)", "S": "south (DECam g, r, z)"},
    "MORPHTYPE": {
        "PSF": "PSF (point source)",
        "REX": "REX (round exponential galaxy)",
        "DEV": "DEV (de Vaucouleurs profile)",
        "EXP": "EXP (exponential profile)",
        "SER": "SER (Sersic profile)",
        "DUP": "DUP (Gaia source fit by an extended source)",
    },
    "REF_CAT": {"": "none", "G2": "Gaia DR2", "L3": "SGA-2020 large galaxy"},
}

_FITS_TYPES = {"K": ">i8", "J": ">i4", "I": ">i2", "E": ">f4", "D": ">f8", "B": "u1", "L": "S1"}


def _fits_table_layout(path: Path) -> tuple[np.dtype, int, int]:
    """The record dtype, the row count and the data offset of the first binary-table extension of a FITS file.

    FITS stores a binary table row by row in big-endian fixed-width records after 2880-byte header blocks, so numpy
    reads it without a FITS library (the catalogue has no scaled or unsigned columns: no TZERO or TSCAL cards).
    """
    cards: dict[str, str] = {}
    headers = 0
    offset = 0
    with open(path, "rb") as f:
        while headers < 2:
            block = f.read(2880)
            if len(block) < 2880:
                raise ValueError(f"{path} ends before its binary-table header")
            offset += 2880
            for i in range(0, 2880, 80):
                card = block[i : i + 80].decode("ascii")
                if card.startswith("END"):
                    headers += 1
                    break
                if headers == 1 and card[8:10] == "= ":
                    cards[card[:8].strip()] = card[10:].split("/")[0].strip().strip("'").strip()
    if cards.get("XTENSION") != "BINTABLE" or any(k.startswith(("TZERO", "TSCAL")) for k in cards):
        raise ValueError(f"{path}: expected a plain binary table")
    fields = []
    for i in range(1, int(cards["TFIELDS"]) + 1):
        repeat, code = re.fullmatch(r"(\d*)([A-Z])", cards[f"TFORM{i}"]).groups()
        repeat = int(repeat or 1)
        if code == "A":
            fields.append((cards[f"TTYPE{i}"], f"S{repeat}"))
        else:
            fields.append((cards[f"TTYPE{i}"], _FITS_TYPES[code] if repeat == 1 else (_FITS_TYPES[code], (repeat,))))
    dtype = np.dtype(fields)
    if dtype.itemsize != int(cards["NAXIS1"]):
        raise ValueError(f"{path}: row size {dtype.itemsize} != NAXIS1 {cards['NAXIS1']}")
    return dtype, int(cards["NAXIS2"]), offset


def _targeting_class(desi_target: pd.Series) -> np.ndarray:
    """The targeting class of each object from the main survey's desi_mask bits (desitarget).

    LRG 0, ELG 1, QSO 2, BGS_ANY 60, MWS_ANY 61; an object in several classes is counted in the last that applies (the
    quasar targets last), the rest are "other".
    """
    bits = desi_target.to_numpy().astype(np.int64)
    tracer = np.full(len(bits), "other (standard stars, secondary)", dtype=object)
    for name, bit in [
        ("Milky Way stars", 61),
        ("bright galaxies", 60),
        ("red galaxies", 0),
        ("emission-line galaxies", 1),
        ("quasars", 2),
    ]:
        tracer[((bits >> bit) & 1) == 1] = name
    return tracer


class DesiDr1StarGalaxyQuasar1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Is an object of an imaging survey's catalogue a galaxy, a star or a quasar, judging from its catalogue "
            "photometry before it has a spectrum?"
        ),
        use_case=(
            "A survey team classifies catalogue objects that have no spectrum, more than 99% of them, to pick "
            "spectroscopic targets such as quasar candidates or to flag stars and galaxies in a catalogue or an "
            "alert stream (DESI's random-forest quasar selection; Liu et al. 2025's star-galaxy model)."
        ),
        row=(
            "One object observed in the first 13 months of DESI's main survey (May 2021 to June 2022) with a "
            "spectroscopic class the pipeline settled (no warning flag) and Legacy Surveys DR9 photometry: 1.5 "
            "million of 16.9 million, drawn at random within each class."
        ),
        predicted=(
            "The class DESI's pipeline (Redrock) fit to the object's spectrum: galaxy (75.4% of the objects), star "
            "(15.6%) or quasar (9.0%)."
        ),
        known=(
            "The sky position; the brightness in three optical and two infrared bands with its uncertainty and as "
            "seen through a fibre; the profile type and shape fit to the images; image-quality flags; the dust "
            "reddening; and Gaia's magnitudes, parallax and proper motion where Gaia measured them."
        ),
        split=(
            "Random objects, so the test data stands for other objects of the same sky area that DESI's programmes "
            "chose for a spectrum in the same way."
        ),
        changes=(
            "We drop the redshift and the other outputs of the spectral fit, and the targeting programme and bits that "
            "record which class DESI was looking for; we keep only objects with Legacy Surveys photometry, which "
            "leaves out the Gaia-only backup targets (98% stars)."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs exist before a spectrum, but the rows are targets picked by colour cuts aimed at one class, "
            "not all catalogue objects, and only spectra whose class the pipeline settled ship (21% of the "
            "emission-line galaxy and 14% of the quasar targets drop out, about 2% of the others). The label is "
            "Redrock's class; DESI's quasar catalogue disagrees on 0.73% of the shipped rows, both ways."
        ),
    )

    # Dataset
    unique_name = "desi_dr1_star_galaxy_quasar_1m"
    version_of = "desi_dr1_star_galaxy_quasar"
    version_comment = """
        We sub-sample the frame (16,930,061 objects) to 1.5M objects, stratified on the class, and use 3-fold cross-validation, so every fold trains on 1M and tests on 500k objects (v2 split protocol).
    """
    year = "2025"
    domain = "physics & astronomy"
    source = "Other"  # the DESI collaboration's data release (data.desi.lbl.gov), not a GOV portal
    source_url = "https://data.desi.lbl.gov/doc/releases/dr1/"
    license = "CC BY 4.0"
    data_tags = ("Spatial",)
    download_description = """
        The DR1 redshift catalogue (22.4 GB; FITS stores a table row by row, so the whole file is needed) and its checksums, from the DESI public data release (CC BY 4.0, https://data.desi.lbl.gov/doc/acknowledgments/).

        mkdir -p local-data-warehouse/desi_dr1_star_galaxy_quasar && cd local-data-warehouse/desi_dr1_star_galaxy_quasar
        wget https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/zcatalog/v1/zall-pix-iron.fits
        wget https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/zcatalog/v1/redux_iron_zcatalog_v1.sha256sum
        grep ' zall-pix-iron.fits' redux_iron_zcatalog_v1.sha256sum | sha256sum -c -

        The LBL server gave 2-9 MB/s per connection on 2026-11-08 (byte ranges in parallel are faster). The European mirror (https://webdav-hdfs.pic.es/data/public/DESI/DR1/spectro/redux/iron/zcatalog/v1/) is faster but served the copy replaced on 2026-07-10, which differs only in the `DESINAME` column (deprecated/README); we do not read that column, so it gives the same data. The first build writes `zall_pix_iron_main.parquet` next to it (`_prepare_raw_files`).
    """
    bibtex = """
        @article{desi2026dr1,
          title = {Data Release 1 of the Dark Energy Spectroscopic Instrument},
          author = {{DESI Collaboration} and Abdul Karim, M. and Adame, A. G. and Aguado, D. and Aguilar, J. and others},
          journal = {The Astronomical Journal},
          volume = {171},
          number = {5},
          pages = {285},
          year = {2026},
          doi = {10.3847/1538-3881/ae4c43},
          eprint = {2503.14745},
          archiveprefix = {arXiv}
        }
    """
    curation_comments = """
        We start with the DR1 redshift catalogue `zall-pix-iron.fits` (Iron production, zcatalog v1) from the DESI public data release.

        - Prediction point: before the object's spectrum. Known then is the imaging catalogue DESI selects its targets from: the Legacy Surveys DR9 Tractor photometry and its Gaia DR2 cross-match, which DESI copies into the redshift catalogue. The class is fit to the spectrum.
        - Rows: the release's "useful spectra" of the main survey (`ZCAT_PRIMARY`, `OBJTYPE` TGT, `ZWARN` 0; DR1 page, footnote 1), 18,659,804 objects, exactly the published counts (13,049,402 galaxies, 1,553,713 quasars, 4,056,689 stars). A spectrum with a `ZWARN` flag has no reliable class, so it has no label to keep (LEAK-22: the release's cohort); such spectra are 10.1% of the primary spectra fit as galaxies, 4.0% of those fit as quasars and 1.6% of those fit as stars. By targeting class the filter is uneven: it drops 20.6% of the emission-line galaxy targets and 13.9% of the quasar targets (53,375 of the 307,534 dropped quasar targets are in DESI's quasar catalogue), against 2.2%, 2.0% and 1.6% of the red galaxy, bright galaxy and Milky Way targets (the first decision below), so the shipped objects are those whose class the spectrum settled (USE-8, named in fit_reason). The Survey Validation and special programmes stay out: they were selected by other rules.
        - Class shares (galaxy / quasar / star) at each step: 71.6 / 8.0 / 20.4% of the 20,256,046 primary spectra, 69.9 / 8.3 / 21.7% of the 18,659,804 useful spectra (the 1,596,242 dropped spectra are 91.8% galaxies), 75.4 / 9.0 / 15.6% of the 16,930,061 objects with Legacy Surveys photometry (the 1,729,743 dropped are 81.5% stars).
        - We drop the 1,729,743 objects without Legacy Surveys photometry (USE-7): 1,212,422 Gaia-only targets of the backup programme for poor observing conditions (`PHOTSYS` G: optical fluxes -99, profile types `GPSF` and `GGAL` of their own, 98.3% stars) and 517,321 secondary targets without a Legacy Surveys match (`PHOTSYS` empty: no profile type, shape, infrared or fibre flux and no flux uncertainty). 16,930,061 objects remain.
        - We drop the outputs of the spectral fit, `Z`, `ZERR` and `DELTACHI2` (LEAK-10): the pipeline fits them with the class from the same spectrum. In LightGBM (600k objects, 3 random folds, early stopping on a tenth of each training side), `Z` alone reaches log loss 0.156 and the photometry with the fit 0.016, against 0.0864 without it.
        - We drop the targeting decision (LEAK-10, the record's screening): the programme (`PROGRAM`, dark or bright), the target bits (`DESI_TARGET`, `BGS_TARGET`, `MWS_TARGET`, `SCND_TARGET`) and `PRIORITY_INIT`, `NUMOBS_INIT`. They exist before the spectrum but record which class DESI was looking for, and the objects the use case classifies have none. Alone they reach log loss 0.163 (class shares 0.720); added to the photometry they change it from 0.0864 to 0.0857 (same folds): the photometry already carries what they say.
        - Note: selection bias, as in sdss_17. Each targeting class is one class almost entirely (bright, red and emission-line galaxy targets 97-98% galaxies, Milky Way targets 99.5% stars); the classes mix among the quasar targets (70.5% quasars, 25.3% galaxies, 4.1% stars). The photometry recovers much of the targeting class, since the cuts are functions of it, but the task is more than that: within the quasar targets an untuned LightGBM scores log loss 0.399 against 0.726 for the targets' own class shares on the shipped splits; within the bright, red and emission-line galaxy targets 0.037, 0.061 and 0.067 against 0.119, 0.149 and 0.116 (the 600k objects above). An unmeasured z or infrared band follows the targeting route too (1,409 of the 1,461 objects without z and 1,446 of the 1,745 without W1 are stars: the Milky Way selection needs neither band); it is known from the imaging, so it stays. The selection gap has a size: trained on the brighter two thirds in r, a LightGBM scores 0.48 on the faintest third against 0.18 under random folds (confounded with the class and programme mix).
        - We keep the Tractor model columns (`MORPHTYPE`, `SHAPE_R`, `SHAPE_E1`, `SHAPE_E2`, `SERSIC`) and the predicted fibre fluxes (`FIBERFLUX_*`, `FIBERTOTFLUX_*`). They are fits to the images, but the table is mostly fluxes measured through an imaging device (SEL-15), not image descriptors (SEL-13): the five profile columns are 5 of 45 inputs, and without them the log loss moves from 0.0864 to 0.0886 (0.0979 without the fibre fluxes too; same folds). This sets the case apart from magic_gamma_telescope, whose table is image descriptors only, and simulated (SEL-16). DESI's own target selection cuts on `MORPHTYPE` and fibre flux.
        - Missing values (CLEAN-10): the Gaia columns are 0 where the object has no Gaia match (all non-Gaia rows), and the parallax and proper motions are 0 for Gaia's two-parameter solutions (14.7% of the Gaia rows). A flux whose inverse variance is 0 was not measured (g 252, r 120, z 1,461, W1 1,745, W2 1,744 objects), nor were that band's fibre fluxes (a fibre total that is not 0 there is the neighbours' light and stays). `SERSIC` is 0 for point sources (`MORPHTYPE` PSF or DUP, 5,514,671 objects), which have no Sersic index; `MORPHTYPE` keeps the information. All set to missing; no score changes.
        - We blank `PARALLAX`, `PMRA` and `PMDEC` for the 17,006 objects (1,529 shipped rows) that carry them without a Gaia DR2 match (`REF_CAT` none or SGA-2020; LEAK-10, weak; CLEAN-21). Which objects have them follows targeting routes: 89.8% are bright-galaxy targets against 44.0% of the other objects without a Gaia match, 36.2% secondary targets against 7.3%, and 60.1% stars against 0.9%; the use case's catalogue object would not have them. The astrometry left is the catalogue's Gaia DR2 match.
        - Note: 88 W1 and 155 W2 fluxes lie below -1000 nanomaggies (down to tens of thousands of sigma, mostly stars, likely forced photometry near bright stars); they are the catalogue's published measurements and stay (CLEAN-11).
        - `MASKBITS` becomes one yes/no column per bit that is set in some row (13 of 16; CLEAN-13). `PHOTSYS`, `MORPHTYPE` and `REF_CAT` are decoded into the words of the Legacy Surveys DR9 documentation.
        - We drop `TARGETID` (unique), `HEALPIX` (the sky pixel, from the position), `RELEASE` (a processing-run code whose camera `PHOTSYS` gives; 9012 marks 1,691 reprocessed bricks), `REF_EPOCH` (2015.5 in every row) and the filter columns.
        - Note: the label is Redrock's template class, the class the release counts (USE-5). DESI's DR1 quasar catalogue (`QSO_cat_iron_cumulative_v0.fits`), which adds the MgII and QuasarNET afterburners on the quasar targets only, disagrees with it both ways (joined on the main-survey row): it calls 53,190 kept objects quasars that Redrock calls galaxies or stars (99.6% of them quasar targets), and it leaves out 68,521 of Redrock's quasars (98.7% of them outside the quasar targets: 34,469 red galaxy, 21,925 bright galaxy and 11,075 emission-line galaxy targets). DESI's all-target AGN and galaxy catalogue flags afterburner quasars among Redrock's galaxies and stars only on quasar targets too (and on 554 objects of a secondary quasar programme), so DESI has no quasar class that does not follow the targeting class; we keep Redrock's, the one class fit the same way for every object. On the shipped rows the two sets are 0.32% and 0.41% of the rows and carry 6.6-7.7% and 14.2-16.6% of a LightGBM's log loss; scored on the catalogue's class instead, the gap between an untuned and a stronger LightGBM grows from 0.0027 to 0.0032 (its additions only) or 0.0046 (both ways), and their order holds. In Survey Validation visual inspection Redrock alone finds about 86% of the quasars, with the afterburners about 94% (Alexander et al. 2023).
        - Copies: `TARGETID` is unique and no two objects share all photometry (0 exact copies). 5,211 pairs of kept objects lie within 1 arcsec of each other: separate Tractor sources of a blend, with different fluxes, kept (LEAK-16); 102 of the shipped rows have such a partner.
        - Note: the same task from another survey as sdss_17 (SDSS DR17, 99,999 objects), not better data for it: SDSS has the u and i bands, DESI adds two infrared bands, Gaia astrometry and image morphology, and the targeting rules differ, so both enter (principles.md, Tensions, "Same task, another source"; PROV-4, PROV-7), with the reason in both records.
        - Note: FITS stores a table row by row, so the whole 22.4 GB file is downloaded; `_prepare_raw_files` reads the 53 columns we use (of 136) for the main survey's 25.4M rows into a Parquet file once, with numpy alone.
    """

    # Task
    target = "SPECTYPE"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "DESI DR1 is a data release (the DR1 paper, the DR1 documentation pages and the redshift catalogue's data "
            "model) with no prediction task or metric. The closest uses, DESI's quasar target selection (Chaussidon "
            "et al. 2023, ApJ 944, 107) and the Legacy Surveys star-galaxy model of Liu et al. (2025, PASP 137, "
            "084501), report purity, completeness and accuracy at thresholds of their own for other label sets, not "
            "one metric for this three-class task. As for sdss_17, the fallback scores the class probabilities."
        )
    )

    # Splits
    row_budget = RowBudget(train=1_000_000, test=500_000)
    splits_comment = """
        Random objects in 3-fold cross-validation on the 1.5M objects sub-sampled within each class (version_comment), so every fold trains on 1M and tests on 500k objects. As for sdss_17, an imaging survey classifies new objects in the same sky area, and the position is a feature, not an entity. Holding out whole sky regions changes nothing: with LightGBM (600k objects, 3 folds each, early stopping) random folds score log loss 0.0864, folds of HEALPix pixels of 0.84 square degrees 0.0861, of 215 square degrees 0.0865 and of the 12 base pixels of about 3,400 square degrees 0.0878; a regularised LightGBM scores 0.0848 on random folds and 0.0850 on 0.84-square-degree pixels. The shipped objects cover about 13,700 square degrees, nearly the whole footprint, so a deployed model classifies objects of sky it was trained on; only one of the deep equatorial DECam areas held out whole costs about 0.03 to 0.05.
    """

    prepared_raw_files = (PREPARED,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        # One pass over the 22 GB FITS table in blocks of rows: keep the main survey's rows and the columns we read.
        import pyarrow as pa
        import pyarrow.parquet as pq

        dtype, n_rows, offset = _fits_table_layout(raw_dir / RAW_FITS)
        table = np.memmap(raw_dir / RAW_FITS, dtype=dtype, mode="r", offset=offset, shape=(n_rows,))
        writer = None
        try:
            for start in range(0, n_rows, 500_000):
                block = np.array(table[start : start + 500_000])
                keep = np.char.strip(block["SURVEY"]) == b"main"
                columns = {}
                for name in READ_COLUMNS:
                    values = block[name][keep]
                    if name in LOGICAL_COLUMNS:  # FITS logicals are one byte, "T" or "F"
                        columns[name] = pa.array(values == b"T")
                    elif values.dtype.kind == "S":
                        columns[name] = pa.array(np.char.strip(values).astype(str))
                    else:
                        columns[name] = pa.array(values.astype(values.dtype.newbyteorder("=")))
                chunk = pa.table(columns)
                if writer is None:
                    writer = pq.ParquetWriter(raw_dir / PREPARED, chunk.schema, compression="zstd")
                writer.write_table(chunk)
        finally:
            if writer is not None:
                writer.close()
            del table

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / PREPARED)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        # 1. The release's "useful spectra" of the main survey (DR1 page, footnote 1): the object's best spectrum
        #    (ZCAT_PRIMARY), a science target (OBJTYPE TGT, not a sky fibre), no known redshift-fitting failure
        #    (ZWARN 0); the main survey has no PROGRAM "other". 18,659,804 rows, the published count.
        useful = df["ZCAT_PRIMARY"] & df["OBJTYPE"].eq("TGT") & df["ZWARN"].eq(0) & df["PROGRAM"].ne("other")
        df = df[useful]
        # 2. Rows without the imaging survey's photometry are no task rows (USE-7): the backup programme's Gaia-only
        #    targets (PHOTSYS "G") and secondary targets without a Legacy Surveys match (PHOTSYS empty).
        df = df[df["PHOTSYS"].isin(["N", "S"])]
        # 3. Proxy missing values (CLEAN-10): Gaia columns are 0 where the object has no Gaia match or no
        #    astrometric solution; a flux whose inverse variance is 0 was not measured, and nor were its fibre
        #    fluxes (a fibre total that is not 0 there is the neighbours' light and stays); a point source has no
        #    Sersic index (0 in the catalogue; MORPHTYPE keeps the information).
        for col in [
            "GAIA_PHOT_G_MEAN_MAG",
            "GAIA_PHOT_BP_MEAN_MAG",
            "GAIA_PHOT_RP_MEAN_MAG",
            "PARALLAX",
            "PMRA",
            "PMDEC",
        ]:
            df[col] = df[col].mask(df[col].eq(0))
        for band in BANDS:
            unmeasured = df[f"FLUX_IVAR_{band}"].eq(0)
            df[f"FLUX_{band}"] = df[f"FLUX_{band}"].mask(unmeasured)
            if band in ("G", "R", "Z"):
                df[f"FIBERFLUX_{band}"] = df[f"FIBERFLUX_{band}"].mask(unmeasured)
                total = f"FIBERTOTFLUX_{band}"
                df[total] = df[total].mask(unmeasured & df[total].eq(0))
        df["SERSIC"] = df["SERSIC"].mask(df["MORPHTYPE"].isin(["PSF", "DUP"]))
        #    Astrometry without a Gaia DR2 match (LEAK-10, CLEAN-21): 17,006 objects carry a parallax and proper
        #    motions with no Gaia match in the imaging catalogue; they follow targeting routes (90% bright-galaxy
        #    targets, 36% secondary targets), so only the catalogue's Gaia DR2 astrometry stays.
        no_gaia_dr2 = df["REF_CAT"].ne("G2")
        for col in ["PARALLAX", "PMRA", "PMDEC"]:
            df[col] = df[col].mask(no_gaia_dr2)
        # 4. The image-quality bitmask as one yes/no column per bit that is ever set (CLEAN-13: flags that can be set
        #    together stay separate columns); bits 10, 14 and 15 are never set in these rows.
        bits = df["MASKBITS"].to_numpy().astype(np.int64)
        for bit, name in MASKBITS.items():
            df[f"MASKBIT_{name}"] = (bits >> bit) & 1
        # 5. Codes into the words of the Legacy Surveys DR9 documentation (CLEAN-12).
        df = decode(df, CODE_LABELS)
        df = drop_columns(
            df,
            [
                # identifiers and the release's filter columns (constant after step 1)
                "TARGETID", "SURVEY", "OBJTYPE", "ZWARN", "ZCAT_PRIMARY", "MAIN_PRIMARY", "HEALPIX",
                # the spectroscopic fit: recorded with the class from the same spectrum (LEAK-10)
                "Z", "ZERR", "DELTACHI2",
                # the targeting decision: which programme picked the object, by its class (LEAK-10)
                "PROGRAM", "DESI_TARGET", "BGS_TARGET", "MWS_TARGET", "SCND_TARGET", "PRIORITY_INIT", "NUMOBS_INIT",
                # a processing-run code (9010 / 9012 south, 9011 north) whose camera PHOTSYS already gives
                "RELEASE",
                # the reference catalogue's epoch: 2015.5 in every row (CLEAN-5)
                "REF_EPOCH",
                # replaced by its bits (step 4)
                "MASKBITS",
            ],
        )  # fmt: skip
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["PHOTSYS", "MORPHTYPE", "REF_CAT", *[f"MASKBIT_{name}" for name in MASKBITS.values()]]
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        primary = raw["ZCAT_PRIMARY"] & raw["OBJTYPE"].eq("TGT") & raw["PROGRAM"].ne("other")
        spectra = raw.loc[primary, ["ZWARN", "DESI_TARGET"]]
        zwarn = (
            pd.DataFrame(
                {"targeted as": _targeting_class(spectra["DESI_TARGET"]), "share dropped": spectra["ZWARN"].ne(0)}
            )
            .groupby("targeted as")["share dropped"]
            .agg(["mean", "size"])
            .round(4)
            .rename(columns={"mean": "share dropped", "size": "primary spectra"})
        )
        useful = primary & raw["ZWARN"].eq(0)
        rows = raw.loc[useful, ["PHOTSYS", "DESI_TARGET", "SPECTYPE"]]
        photometry = pd.crosstab(
            rows["PHOTSYS"]
            .map({"N": "Legacy Surveys north", "S": "Legacy Surveys south", "G": "Gaia only"})
            .fillna("none (secondary targets)"),
            rows["SPECTYPE"],
            margins=True,
        )
        rows = rows[rows["PHOTSYS"].isin(["N", "S"])]
        tracer = _targeting_class(rows["DESI_TARGET"])
        shares = pd.crosstab(
            pd.Series(tracer, index=rows.index, name="targeted as"), rows["SPECTYPE"], normalize="index"
        )
        shares = shares.round(4).assign(objects=pd.Series(tracer).value_counts())
        return [
            Decision(
                "Only spectra whose class the pipeline settled ship (the release's ZWARN filter)",
                "The release's useful spectra are those without a ZWARN flag (DR1 page, footnote 1; LEAK-22: the "
                "release's cohort): a flagged spectrum has no reliable class to keep. The filter drops more "
                "emission-line galaxy and quasar targets than the others, so the shipped objects are those whose "
                "spectrum settled the class (named in fit_reason, USE-8). Share of the main survey's primary spectra "
                "with a ZWARN flag, by targeting class.",
                zwarn,
            ),
            Decision(
                "Objects without Legacy Surveys photometry are dropped",
                "The task classifies objects from the imaging survey's catalogue; the backup programme's Gaia-only "
                "targets and the secondary targets without a Legacy Surveys match have none of its columns (USE-7).",
                photometry,
            ),
            Decision(
                "The targeting class decides most of the class (selection bias, targeting columns dropped)",
                "Each object was targeted by colour cuts aimed at one class, so the target bits nearly give the class "
                "away and are dropped (LEAK-10); the classes mix mostly among the quasar targets. Shares of the "
                "spectroscopic class by targeting class, on the shipped objects before sub-sampling.",
                shares,
            ),
        ]
