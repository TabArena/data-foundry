"""KSSL MIR calibration against archived laboratory-reference organic carbon."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, Decision, FeatureTypes, Grouping, Metric, TaskSummary

KEY = ["dataset.code_ascii_txt", "id.layer_uuid_txt"]
TARGET_SOURCE = "oc_usda.c729_w.pct"
BINS = [f"scan_mir.{n}_abs" for n in range(600, 4001, 2)]


class OpenSoilSpectralLibrary(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="What is the laboratory-reference organic-carbon weight percent of a prepared soil sample from its mid-infrared scan?",
        use_case="A soil spectroscopy laboratory estimates an archived organic-carbon reference from a prepared sample's scan. Evaluation holds out source-ID groups treated as experiment or measurement batches, predicting each sample separately.",
        row="One archived KSSL soil layer with its averaged mid-infrared spectrum and laboratory-reference label, from the July 2022 source snapshot released in OSSL v1.2.",
        predicted="Organic carbon in weight percent, estimated analytically from total carbon, with the archived S-preparation reference preferred over N preparation when both exist.",
        known="Absorbance in 1,701 spectral bins from 600 to 4,000 inverse centimetres at intervals of two. Other laboratory outcomes, identifiers and field metadata are not inputs to the source's scan-upload task.",
        split="Whole native KSSL LIMS source-ID groups are held out, with each group treated as an experiment or measurement batch for this benchmark scenario. Some IDs include campaigns or standards. Actual one-to-one batch or physical-profile identity is unverified; the evaluation establishes unseen source-ID groups within this archive.",
        changes="We restrict OSSL to KSSL mid-infrared samples, retain the archived reference scale and hold out native KSSL LIMS keys. Rows without a spectrum or reference label cannot form this prediction task.",
        fit="approximate",
        fit_reason="The accepted target is the archived total-C-based analytical reference. Source-ID groups approximate measurement batches for evaluation, without verified one-to-one experimental-batch or physical-profile identity. Preparation equivalence, agreement with a future assay, and broader instrument, laboratory or geographic transfer remain unverified.",
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
    curation_comments = "\n        We start with the lab L1, site L0 and MIR L0 tables of Zenodo record 7599269, v1.2, with archived L0 lab references retained for auditing.\n\n        - Prediction point: a prepared scan is available, a new chemical reference is not. Keep all 1,701 raw spectral bins. The source scan-upload service does not require field metadata; other chemistry outcomes and carbon equivalents never enter its inputs (USE-3, LEAK-10).\n        - Restrict the source code to KSSL.SSL. Join on dataset.code_ascii_txt and id.layer_uuid_txt with one-to-one validation, never by row position or rounded coordinates. Native lims.pedon.id supplies the source-key group, never a model feature (historical KSSL importer, Site information, rename block). Source-key lineage is verified; unique physical-profile identity is not established for all keys, including archive campaigns and bulk standards. No conflicting nonempty coordinate/taxonomy pairs were found; collision is not demonstrated. The source importer kept the first taxonomy per native key before joining, so taxonomy agreement is weak negative evidence of physical uniqueness; missing coordinates further limit that screen.\n        - The L1 organic-carbon label is an analytical estimate, not a spectroscopy prediction. Archived KSSL L0 S-preparation values take precedence over N preparation; the row-wise coalescence reproduces every KSSL L1 value and missingness mask. The upstream importer had already converted negative laboratory references to missing; this cannot recover their pre-import count.\n        - Drop rows without any spectrum, and rows with a missing target. Do not clip, scale or nonlinearly transform the reference, discard zero endpoints, average repeated entities or fit a spectral transform over all rows. Raw reference values and source identities remain in the warehouse.\n        - Hold out native KSSL LIMS source-ID groups for within-archive evaluation, treating each group as an experiment/measurement batch as approved by Myunghwan. Preserve all usable scan/reference rows and score each sample separately; actual experimental batch boundaries are not authenticated by this interpretation. Do not describe every block as a distinct physical profile, or library provenance as proof of physical country of origin. The source-ID grouping is a confirmed task choice; it does not certify physical-profile separation. The benchmark base class supplies deterministic row order and splits.\n        - Keep the archived reference in raw weight percent and score per-row RMSE, as confirmed by Myunghwan. Dividing by 100 would not add submission flexibility: a method emitting a bounded fraction can convert its output back to percent. The paired check found no material aggregate scaling benefit, but this was not the sole rationale. Preserve zeros and avoid clipping or a nonlinear target transform.\n        - Version note: this growing-source snapshot was created on Zenodo in February 2023 and uses July 2022 KSSL inputs; the landing page also displays a 2021 publication date. The current record and definition use the 2023 snapshot convention; the historical 2021 landing-page date remains disclosed.\n    \n        - Metric provenance: the source deliberately tunes inner RMSE with OC in log1p space, and reports original-unit external RMSE. The accepted source-origin raw-percent RMSE cites the external evaluation and keeps these scales distinct; no nonlinear target transform is applied.\n        - Source overlap: WoSIS documents USDA-NCSS ancestry, and KSSL contains ISRIC-labelled projects. The tasks differ from this MIR calibration; physical aliquot overlap is unmeasured. All 76,813 complete KSSL spectra compared with 8,871 complete other-library spectra show no exact full-grid copies; rescans and partial-grid records remain outside that claim.\n        - Preparation audit: 55,855 usable XS scans use S references; 20,043 XN scans use N references; 31 XS scans use the source N fallback. Preserve all usable scan/reference rows and source coalescence; identity harmonization is not an analytical-equivalence claim.\n\n        - Curator-requested few-band diagnostics on three fixed grouped samples found two-band OLS RMSE 5.98 and five-band OLS 4.01 percentage points, versus 1.96 for retained full-spectrum Ridge. Ten training-fitted PCs retained 98.6% of input variance; PCA10 Ridge RMSE was 4.55 and PCA10 LightGBM 2.77, versus full-spectrum LightGBM 2.43. These are bounded, untuned comparisons on identical 5,000-row train/test samples per fold, not full-data rankings or deployed preprocessing. All 1,701 measured predictors remain.\n"
    target = "organic_carbon_weight_percent"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSE of organic carbon in original weight-percent units (external independent evaluation)",
        reference="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0296545",
        definition="sqrt(mean((y - y_hat)**2)), per layer in weight-percentage points. Source-origin metric follows the paper's original-unit external evaluation (Table 5 and supporting S3). Source inner model selection deliberately used RMSE with OC in log1p space; that objective is distinct. Raw references and identity target transform remain unchanged. Myunghwan confirmed the raw weight-percent target and per-row RMSE.",
        target_transform="identity",
    )
    grouping = Grouping(
        on="pedon_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="A group is the archived native KSSL lims.pedon.id, renamed id.dataset.site_ascii_txt in the 2023-01-09 importer. The code is authenticated source metadata, never a predictor, coordinate cluster or similarity hash. Some large keys contain archive campaigns or bulk standards; unique physical-profile identity is not established for every key. No conflicting nonempty coordinate/taxonomy pairs were found; erroneous collisions are not demonstrated. Taxonomy was aggregated to the first value per native key before joining, so its agreement is weak negative evidence; missing coordinates also limit the screen. Myunghwan treats each exact source-ID block as an experiment/measurement batch for evaluation; this is a benchmark interpretation, not verified one-to-one experimental-batch provenance. The task evaluates unseen source-ID blocks within the archive; physical-profile cold start would require original relational/field mappings or source clarification. Prediction and scoring remain per layer/reference, with no group context.",
    )
    splits_comment = "Curator-approved native KSSL LIMS source-ID grouped splits, with seed 4267 and three repeats of three folds. Each source ID is kept intact and treated as an experiment/measurement batch in the benchmark scenario; each row is predicted and scored separately. This interpretation does not authenticate actual experimental-batch boundaries or certify unseen physical profiles, geographic regions or instruments. No numerical membership changed when the task choices were confirmed."
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        meta = pd.read_csv(raw_dir / "kssl_mir.metadata.csv.gz", dtype=str, keep_default_na=False)
        bins = (raw_dir / "kssl_mir.bins.txt").read_text().splitlines()
        assert bins == BINS, "Source spectral grid changed"
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
        spectra = raw[BINS]
        has_spectrum = spectra.notna().any(axis=1)
        # The archive has complete or entirely absent KSSL spectra, no partial spectra.
        assert spectra.loc[has_spectrum].notna().all().all()
        valid = has_spectrum & raw[self.target].notna()
        result = raw.loc[valid, [*BINS, "pedon_id", self.target]].copy()
        assert np.isfinite(result[BINS].to_numpy()).all()
        assert result[self.target].between(0, 100).all(), "Investigate unexpected reference bounds; never clip"
        return result

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["pedon_id"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        has_spectrum = raw[BINS].notna().any(axis=1)
        counts = pd.Series(
            {
                "KSSL source rows": len(raw),
                "rows without MIR": int((~has_spectrum).sum()),
                "missing OC references": int(raw[self.target].isna().sum()),
                "usable MIR and OC": len(df),
                "native KSSL source keys": df["pedon_id"].nunique(),
                "zero OC endpoints retained": int(df[self.target].eq(0).sum()),
            }
        )
        return [
            Decision(
                "Source support and missing inputs",
                "An absent scan is not this task's input; a missing reference cannot be scored (USE-7, CLEAN-15).",
                counts,
            ),
            Decision(
                "Raw reference scale",
                "Weight percent remains unchanged. Fixed division by 100 is separately assessed in identical rows and folds with inverse conversion before physical-unit scoring.",
                df[self.target].describe(percentiles=[0.01, 0.5, 0.99]),
            ),
        ]
