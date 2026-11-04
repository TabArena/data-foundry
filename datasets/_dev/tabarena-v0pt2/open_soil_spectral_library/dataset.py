"""KSSL MIR calibration against archived laboratory-reference organic carbon."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, Spectrum, TaskSummary

KEY = ["dataset.code_ascii_txt", "id.layer_uuid_txt"]
TARGET_SOURCE = "oc_usda.c729_w.pct"
WAVENUMBERS = range(600, 4001, 2)
SOURCE_BINS = [f"scan_mir.{n}_abs" for n in WAVENUMBERS]
PREFIX = "mir_"
RENAMED = [f"{PREFIX}{n}" for n in WAVENUMBERS]
# The 600 cm-1 edge holds a fill value (an exact 0 beside a 602 cm-1 reading of 1.27-1.86) in 53 spectra: the bin
# leaves for every row (Lennart, 2026-11-04), so the shipped spectrum runs from 602 to 4,000 cm-1.
DROPPED_EDGE = f"{PREFIX}600"
BINS = [b for b in RENAMED if b != DROPPED_EDGE]


class OpenSoilSpectralLibrary(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the laboratory-reference organic-carbon weight percent of a prepared soil sample from its mid-infrared scan?",
        use_case="A soil spectroscopy laboratory estimates a prepared sample's organic carbon from its mid-infrared scan instead of running the wet chemistry, as the OSSL Engine does for an uploaded scan. Evaluation holds out whole soil profiles and predicts each layer separately.",
        row="One archived KSSL soil layer with its averaged mid-infrared spectrum and laboratory-reference label, from the July 2022 source snapshot released in OSSL v1.2.",
        predicted="Organic carbon in weight percent, estimated analytically from total carbon, with the archived S-preparation reference preferred over N preparation when both exist. It ships as log1p, the scale the source models it on, and is scored in weight percent.",
        known="The sample's mid-infrared absorbance spectrum, 1,700 positions from 602 to 4,000 cm-1 every 2 cm-1, declared as a spectrum. Other laboratory outcomes, identifiers and field metadata are not inputs to the source's scan-upload task.",
        split="Whole KSSL soil profiles (the pedon key lims.pedon.id, whose layers are the rows) are held out, so each test layer comes from a profile not seen in training, scanned by the same laboratory and instrument.",
        changes="We restrict OSSL to KSSL mid-infrared samples, ship the reference as log1p as the source models it and hold out KSSL profiles. Rows without a spectrum or reference label cannot form this prediction task.",
        fit="approximate",
        fit_reason="The task is the source's own calibration within one laboratory and one instrument. A laboratory using the OSSL models scans on its own instrument, and that transfer, where the source's independent evaluation finds the errors grow, is not tested.",
    )
    unique_name = "open_soil_spectral_library"
    year = "2023"
    domain = "environmental science & climate"
    source = "Other"
    source_url = "https://zenodo.org/records/7599269"
    license = "CC BY 4.0"
    download_description = "Recreate the lossless raw inputs with Python 3, R 4.3 or later and qs 0.27.3.\nThe following complete Python script downloads the four immutable Zenodo v1.2 files,\nchecks their published MD5 values and decodes them without fitting or cleaning.\nSave it as prepare_raw.py, then run:\n\n```sh\npython3 prepare_raw.py --raw-dir local-data-warehouse/open_soil_spectral_library\n```\n\nUse --existing-only when source files were fetched through a download gateway.\nNo model is fitted. The archived QS originals remain beside the exports.\nA network failure is an access limitation, never evidence against the dataset.\n\n```python\n# Standalone raw-input preparation; no fitting or curation decisions.\nimport argparse,hashlib,subprocess,urllib.request\nfrom pathlib import Path\nFILES={\n 'ossl_soillab_L0_v1.2.qs':'6817a47891b2281545917e543bf3b7f0',\n 'ossl_soillab_L1_v1.2.qs':'652f7bf633d969d6d45cf21007c91a31',\n 'ossl_soilsite_L0_v1.2.qs':'232fb5bef505a8b5bfa4fe2120c913d9',\n 'ossl_mir_L0_v1.2.qs':'de56ed6d11ea9ca8c54475a674586b00'}\na=argparse.ArgumentParser();a.add_argument('--raw-dir',type=Path,required=True);a.add_argument('--rscript',default='Rscript');a.add_argument('--existing-only',action='store_true');args=a.parse_args();d=args.raw_dir;d.mkdir(parents=True,exist_ok=True)\nfor name,expected in FILES.items():\n f=d/name\n if not f.exists():\n  if args.existing_only:raise SystemExit('Missing '+str(f))\n  urllib.request.urlretrieve('https://zenodo.org/records/7599269/files/'+name+'?download=1',f)\n h=hashlib.md5()\n with f.open('rb') as s:\n  for block in iter(lambda:s.read(8*1024*1024),b''):h.update(block)\n if h.hexdigest()!=expected:raise SystemExit('Checksum mismatch '+name)\nLAB_R=\"args <- commandArgs(trailingOnly=TRUE)\\nlibrary(qs)\\noptions(digits=17)\\nfor (path in args) {\\n cat('\\\\nFILE ', basename(path), '\\\\n', sep='')\\n x <- qread(path, nthreads=2)\\n cat('CLASS ', paste(class(x),collapse=','), ' DIM ', paste(dim(x),collapse=' x '), '\\\\n', sep='')\\n cat('COLUMNS\\\\n'); cat(paste(names(x),collapse='\\\\n'),'\\\\n')\\n if ('dataset.code_ascii_txt' %in% names(x)) {cat('DATASET_COUNTS\\\\n'); print(table(x[['dataset.code_ascii_txt']],useNA='always'))}\\n cols <- grep('(^oc_|^c.tot_|^caco3_|^id[.]|^layer[.]|^scan)',names(x),value=TRUE)\\n write.csv(data.frame(column=names(x),type=sapply(x,function(z)paste(class(z),collapse=':'))), paste0(path,'.schema.csv'),row.names=FALSE)\\n # Export all lab/site columns for exact source-key qualification. Decimal strings preserve 17 significant digits.\\n y <- as.data.frame(x)\\n for (n in names(y)) if(is.numeric(y[[n]])) y[[n]] <- ifelse(is.na(y[[n]]),NA,format(y[[n]],digits=17,scientific=TRUE,trim=TRUE))\\n write.csv(y,gzfile(paste0(path,'.csv.gz')),row.names=FALSE,na='')\\n cat('EXPORTED ',nrow(y),' ROWS\\\\n',sep='')\\n}\\n\"\nMIR_R=\"args <- commandArgs(trailingOnly=TRUE)\\nlibrary(qs)\\nx <- qread(args[1],nthreads=2)\\ncat('DIM ',paste(dim(x),collapse=' x '),'\\\\n');cat('DATASET_COUNTS\\\\n');print(table(x[['dataset.code_ascii_txt']],useNA='always'))\\nbins <- grep('^scan_mir[.]',names(x),value=TRUE)\\ncat('BIN_COUNT ',length(bins),'\\\\n');cat('NONBIN_COLUMNS\\\\n');cat(paste(setdiff(names(x),bins),collapse='\\\\n'),'\\\\n')\\nk <- x[x[['dataset.code_ascii_txt']]=='KSSL.SSL',,drop=FALSE]\\ncat('KSSL_ROWS ',nrow(k),'\\\\n');writeLines(bins,paste0(args[2],'.bins.txt'))\\n# R columns are written sequentially; Python reconstructs with Fortran order.\\nwriteBin(as.double(as.matrix(k[,bins])),paste0(args[2],'.float64.bin'),size=8,endian='little')\\nm <- as.data.frame(k[,setdiff(names(k),bins)])\\nfor(n in names(m))if(is.numeric(m[[n]]))m[[n]]<-ifelse(is.na(m[[n]]),NA,format(m[[n]],digits=17,scientific=TRUE,trim=TRUE))\\nwrite.csv(m,gzfile(paste0(args[2],'.metadata.csv.gz')),row.names=FALSE,na='')\\nwrite.csv(data.frame(column=names(x),type=sapply(x,function(z)paste(class(z),collapse=':'))),paste0(args[2],'.schema.csv'),row.names=FALSE)\\n\"\nlab=d/'decode-lab.R';mir=d/'decode-mir.R';lab.write_text(LAB_R);mir.write_text(MIR_R)\nsubprocess.run([args.rscript,str(lab),*[str(d/n) for n in FILES if 'mir_L0' not in n]],check=True)\nsubprocess.run([args.rscript,str(mir),str(d/'ossl_mir_L0_v1.2.qs'),str(d/'kssl_mir')],check=True)\nprint('Verified source checksums and prepared lossless inputs in',d)\n```\n"
    bibtex = r"""
        @dataset{safanelli2023ossl,
          author={Safanelli, Jose L. and Hengl, Tomislav and Sanderman, Jonathan and Parente, Leandro},
          title={Open Soil Spectral Library (training data and calibration models)},
          year={2023}, version={v1.2}, publisher={Zenodo}, doi={10.5281/zenodo.7599269}
        }
    """
    curation_comments = """
        We start with the lab L1, site L0 and MIR L0 tables of Zenodo record 7599269, v1.2, with archived L0 lab references retained for auditing.

        - Prediction point: a prepared scan is available, a new chemical reference is not. Keep 1,700 raw spectral bins (602 to 4,000 cm-1; the 600 cm-1 edge is dropped). The source scan-upload service does not require field metadata; other chemistry outcomes and carbon equivalents never enter its inputs (USE-3, LEAK-10).
        - The metric is the source's cross-validation metric, RMSE on log1p, which is `rmsle` on the percent (Lennart, 2026-11-04: "follow the recommendation, following the source").
        - The spectrum ships as KSSL exported it and OSSL v1.2 published it, and is declared as one (`special_features`, CLEAN-26; Lennart, 2026-11-04): the absorbance of the finely ground sample on KSSL's Bruker Vertex 70 with the HTS-XT accessory, replicate scans averaged, on KSSL's 2 cm-1 grid from 600 to 4,000 cm-1, stored to 5 decimals. OSSL applies the standard normal variate inside its models, not in the table, so the state is `raw`. The bins are renamed from `scan_mir.<wavenumber>_abs` to `mir_<wavenumber>` so the build reads the axis from the names; no value changes.
        - The 600 cm-1 edge: 53 spectra read exactly 0 at 600 cm-1 while their 602 cm-1 value is 1.27 to 1.86 (50 of them scanned in 2011, 42 on two days), a fill at the edge of the range. The bin is dropped for every row (Lennart, 2026-11-04: "do (b)"), so each spectrum stays whole, 602 to 4,000 cm-1. The other 32 exact zeros are sign changes of a near-zero absorbance above 2,000 cm-1. The 600 cm-1 bin's distinct-value count (27,193) is ordinary: the counts run from about 23,000 to 55,000 along the whole axis, and the bins to 606 cm-1 have as few.
        - Encodings (2026-11-04, the three folds of repeat 0, untuned settings, RMSE in percent): LightGBM falls from 1.74 on the spectrum as it is to 1.33 with the registered ALS baseline and SNV, 1.39 with SNV alone and 1.24 with a Savitzky-Golay first derivative (11 points, order 2; both registered on 2026-11-04 as `vib-snv-r1` and `vib-sg11-d1-r1`), lower on every fold. Ridge is best as it is (1.84 against 2.05 to 2.17 processed); PLS with 30 components gains 0.14 to 0.16 from ALS and SNV or the derivative. Fitted on the shipped log1p and scored in percent, every model is worse in percent (LightGBM 1.85 as it is, 1.43 with ALS and SNV) and better on the log scale. Layers above 12% organic carbon (16% of rows) carry 79 to 95% of the squared error, and an unclipped linear fit on log1p put one layer at 118,759% (ridge with SNV, one fold: RMSE 745, and 1.86 with the predictions clipped to the training range).
        - Restrict the source code to KSSL.SSL. Join on dataset.code_ascii_txt and id.layer_uuid_txt with one-to-one validation, never by row position or rounded coordinates. The native KSSL pedon key lims.pedon.id (renamed id.dataset.site_ascii_txt by the 2023-01-09 importer) is the group, never a model feature.
        - The L1 organic-carbon label is an analytical estimate, not a spectroscopy prediction. Archived KSSL L0 S-preparation values take precedence over N preparation; the row-wise coalescence reproduces every KSSL L1 value and missingness mask. The upstream importer had already converted negative laboratory references to missing; this cannot recover their pre-import count.
        - Drop rows without any spectrum, and rows with a missing target. Do not clip the reference, discard zero endpoints, average repeated entities or fit a spectral transform over all rows. Raw reference values and source identities remain in the warehouse.
        - Hold out whole KSSL profiles: a group is one pedon key, a sampled soil profile whose layers are the rows, and holding it out tests a new sample from the same laboratory and instrument. Each layer is predicted and scored separately. Myunghwan chose the key over coordinates on 2026-10-27 ("group id is slightly better. stick to group id").
        - Ship the reference as log1p(weight percent) and score RMSE in weight percent after the inverse (MET-3; Lennart, 2026-11-04: "Follow the source metric and scale"). The source fits organic carbon on log1p (`log1p()` for every property but clay, silt, sand and the two pH values) and back-transforms with `expm1()` for its independent evaluation. Myunghwan's 2026-10-27 choice of the original target compared percent with a fraction, not with log1p.
        - Metric provenance: the source tunes Cubist by RMSE on log1p (inner 5-fold CV on 2,000 samples), reports its 10-fold CV on log1p (S2 Table; for KSSL MIR organic carbon, n = 75,929 as here, RMSE 0.114 and CCC 0.995), reports its independent evaluation in percent after back-transformation (Table 5, S3 Table) and ranks its models by Lin's CCC with an RPIQ cut-off of 2 (Fig 5). The declared RMSE in percent is on the independent evaluation's scale.
        - Version note: this growing-source snapshot was created on Zenodo in February 2023 and uses July 2022 KSSL inputs; the landing page also displays a 2021 publication date. The current record and definition use the 2023 snapshot convention; the historical 2021 landing-page date remains disclosed.
        - Source overlap: WoSIS documents USDA-NCSS ancestry, and KSSL contains ISRIC-labelled projects. The tasks differ from this MIR calibration; physical aliquot overlap is unmeasured. All 76,813 complete KSSL spectra compared with 8,871 complete other-library spectra show no exact full-grid copies; rescans and partial-grid records remain outside that claim.
        - Preparation audit: 55,855 usable XS scans use S references; 20,043 XN scans use N references; 31 XS scans use the source N fallback. Preserve all usable scan/reference rows and source coalescence; identity harmonization is not an analytical-equivalence claim.

        - Curator-requested few-band diagnostics on three fixed grouped samples found two-band OLS RMSE 5.98 and five-band OLS 4.01 percentage points, versus 1.96 for retained full-spectrum Ridge. Ten training-fitted PCs retained 98.6% of input variance; PCA10 Ridge RMSE was 4.55 and PCA10 LightGBM 2.77, versus full-spectrum LightGBM 2.43. These are bounded, untuned comparisons on identical 5,000-row train/test samples per fold, not full-data rankings or deployed preprocessing. All 1,701 measured predictors remain.
    """
    target = "organic_carbon_weight_percent"
    problem_type = "regression"
    metric = Metric.source(
        "rmsle",
        original="RMSE of log1p organic carbon in the source's 10-fold cross-validation and model tuning",
        reference="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0296545",
        definition=(
            "sqrt(mean((log1p(y) - log1p(y_hat))**2)) per layer on weight percent, after expm1 of the shipped log1p "
            "values and of the predictions: the RMSE of the shipped values. The paper's 10-fold CV and its tuning use "
            'RMSE on log1p (S2: "reported in the natural logarithm space"); its independent sets report RMSE in '
            "percent, and it ranks model types by Lin's CCC with RPIQ."
        ),
        target_transform="log1p",
    )
    special_features = (
        Spectrum(
            name="mir_spectrum",
            prefix=PREFIX,
            unit="cm-1",
            technique="infrared",
            state="raw",
            description=(
                "The sample's mid-infrared absorbance from KSSL's Bruker Vertex 70 with the HTS-XT accessory, finely "
                "ground (<80 mesh): replicate scans averaged and exported by KSSL on a 2 cm-1 grid from 600 to 4,000 "
                "cm-1 (1,701 positions; the 600 cm-1 edge, a fill in 53 spectra, is dropped), stored to 5 decimals, with no baseline correction, normalisation or "
                "derivative."
            ),
        ),
    )
    grouping = Grouping(
        on="pedon_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="The KSSL pedon key lims.pedon.id (archived as id.dataset.site_ascii_txt): a sampled soil profile, whose layers are the rows; a few large keys hold archive campaigns or bulk standards. Holding a profile out tests a new sample from the same laboratory and instrument. Each layer is predicted and scored on its own, with no group context.",
    )
    splits_comment = "Whole KSSL profiles (pedon keys) held out, three repeats of three folds with seed 4267: a test layer's profile is never in training, and the laboratory and instrument are the same in training and test."
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        meta = pd.read_csv(raw_dir / "kssl_mir.metadata.csv.gz", dtype=str, keep_default_na=False)
        bins = (raw_dir / "kssl_mir.bins.txt").read_text().splitlines()
        assert bins == SOURCE_BINS, "Source spectral grid changed"
        matrix = np.fromfile(raw_dir / "kssl_mir.float64.bin", dtype="<f8")
        assert matrix.size == len(meta) * len(bins), "Spectra and key metadata do not align"
        frame = pd.concat(
            [
                meta[KEY].reset_index(drop=True),
                pd.DataFrame(matrix.reshape((len(meta), len(bins)), order="F"), columns=bins),
            ],
            axis=1,
        )
        assert meta[KEY[0]].eq("KSSL.SSL").all()
        lab = pd.read_csv(raw_dir / "ossl_soillab_L1_v1.2.qs.csv.gz", dtype=str, keep_default_na=False)
        site = pd.read_csv(raw_dir / "ossl_soilsite_L0_v1.2.qs.csv.gz", dtype=str, keep_default_na=False)
        lab = lab.loc[lab[KEY[0]].eq("KSSL.SSL"), KEY + [TARGET_SOURCE]]
        site = site.loc[site[KEY[0]].eq("KSSL.SSL"), KEY + ["id.dataset.site_ascii_txt"]]
        assert not frame.duplicated(KEY).any()
        assert not lab.duplicated(KEY).any()
        assert not site.duplicated(KEY).any()
        frame = frame.merge(lab, on=KEY, how="left", validate="one_to_one", indicator="lab_join")
        assert frame["lab_join"].eq("both").all(), "Unmatched reference row"
        frame = frame.merge(site, on=KEY, how="left", validate="one_to_one", indicator="site_join")
        assert frame["site_join"].eq("both").all(), "Unmatched site row"
        frame[self.target] = pd.to_numeric(frame[TARGET_SOURCE].replace("", np.nan), errors="raise")
        frame["pedon_id"] = frame["id.dataset.site_ascii_txt"]
        assert frame["pedon_id"].ne("").all(), "Missing native pedon"
        return frame

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        spectra = raw[SOURCE_BINS]
        has_spectrum = spectra.notna().any(axis=1)
        # The archive has complete or entirely absent KSSL spectra, no partial spectra.
        assert spectra.loc[has_spectrum].notna().all().all()
        valid = has_spectrum & raw[self.target].notna()
        result = raw.loc[valid, [*SOURCE_BINS, "pedon_id", self.target]].copy()
        result = result.rename(columns=dict(zip(SOURCE_BINS, RENAMED, strict=True))).drop(columns=DROPPED_EDGE)
        assert np.isfinite(result[BINS].to_numpy()).all()
        assert result[self.target].between(0, 100).all(), "Investigate unexpected reference bounds; never clip"
        # The source fits organic carbon on log1p and back-transforms for its independent evaluation (MET-3).
        result[self.target] = np.log1p(result[self.target])
        return result

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["pedon_id"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        has_spectrum = raw[SOURCE_BINS].notna().any(axis=1)
        counts = pd.Series(
            {
                "KSSL source rows": len(raw),
                "rows without MIR": int((~has_spectrum).sum()),
                "missing OC references": int(raw[self.target].isna().sum()),
                "usable MIR and OC": len(df),
                "native KSSL source keys": df["pedon_id"].nunique(),
                "zero OC endpoints retained": int(df[self.target].eq(0).sum()),
                "spectra with a 0 at 600 cm-1 (bin dropped)": int(
                    raw.loc[has_spectrum & raw[self.target].notna(), SOURCE_BINS[0]].eq(0).sum()
                ),
            }
        )
        return [
            Decision(
                "Source support and missing inputs",
                "An absent scan is not this task's input; a missing reference cannot be scored (USE-7, CLEAN-15).",
                counts,
            ),
            Decision(
                "Reference scale",
                "Organic carbon in weight percent ships as log1p, the scale the source fits and tunes on; RMSE is scored in weight percent after the inverse (MET-3).",
                pd.DataFrame(
                    {
                        "weight percent": np.expm1(df[self.target]).describe(percentiles=[0.01, 0.5, 0.99]),
                        "shipped log1p": df[self.target].describe(percentiles=[0.01, 0.5, 0.99]),
                    }
                ),
            ),
        ]
