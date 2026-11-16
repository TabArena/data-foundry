"""Curated dataset definition for `milk_nir_composition` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    Spectrum,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

N_PIXELS = 256


def _block(name: str) -> list[str]:
    return [f"Trans_{name}_{i}" for i in range(1, N_PIXELS + 1)]


# The source's four spectral blocks: the sample's raw counts, the instrument's dark and white reference readings of the
# same milking, and the normalised transmittance the deposit computed from them (`Trans_Tot`, with the week's mean
# dark and white; see the notes).
SAMPLE, DARK, WHITE, SOURCE_SPECTRUM = (_block(b) for b in ("Sample", "Dark", "White", "Tot"))
# The source's nominal axis: 256 pixels "across a wavelength range of 960 nm to 1690 nm, at a resolution of 2.86 nm per
# pixel" (data paper, Table 1 note b), pixel 1 at the short-wavelength end. No per-pixel calibration is published.
NOMINAL_NM = [960 + 2.86 * (p - 1) for p in range(1, N_PIXELS + 1)]
PREFIX = "nir_"
SPECTRUM = [f"{PREFIX}{nm:.2f}" for nm in NOMINAL_NM]
# The weeks the deposit holds whole (its count equals the data paper's Table 2): there the deposit's `Trans_Tot` is the
# week-mean referencing to machine precision; in weeks 1, 4, 5 and 6 the 46 samples without a reference were in the
# source's mean but are not in the deposit.
WHOLE_WEEKS = (2, 3, 7, 8)
# Laboratory reference values measured on the same milk sample as the target: not known when the sensor reads.
OTHER_LAB_VALUES = ["Prot", "Lact", "SCC", "Urea"]
# The sensor's own timestamps, 39 to 144 seconds after the end of milking, and the trial's week number.
SENSOR_BOOKKEEPING = ["Time_Dark", "Time_Sample", "Time_White", "SET"]
RENAME = {
    "Cow_ID": "cow_id",
    "Fat": "fat_percent",
    "Milk_yield": "milk_yield_liters",
    "Milk_Interv": "milking_interval_seconds",
    "Time_Milk": "milking_end",
    "Time_PrevMilk": "previous_milking",
}
# The farm's wall clock: every sample falls in Belgian summer time (CEST, UTC+2).
FARM_TZ = "Europe/Brussels"
# The four cows that calved during the trial and the one cow under five days in milk at its start, whose 59 samples
# the related research article removed as colostrum (Diaz-Olivares et al. 2020); without them the deposit gives the
# article's Table 3 exactly (see `_decisions`). Kept in the data.
FRESH_COWS = (55391, 55392, 55393, 55394, 59137)


def _own_pair_spectrum(raw: pd.DataFrame) -> np.ndarray:
    """(sample - dark) / (white - dark) per pixel, with the milking's own dark and white readings."""
    sample, dark, white = (raw[cols].to_numpy(dtype="float64") for cols in (SAMPLE, DARK, WHITE))
    return (sample - dark) / (white - dark)


def _week_mean_spectrum(raw: pd.DataFrame) -> np.ndarray:
    """The deposit's referencing: (sample - the week's mean dark) / (the week's mean white - the week's mean dark)."""
    sample, dark, white = (raw[cols].to_numpy(dtype="float64") for cols in (SAMPLE, DARK, WHITE))
    out = np.empty_like(sample)
    for week in raw["SET"].unique():
        rows = (raw["SET"] == week).to_numpy()
        mean_dark, mean_white = dark[rows].mean(axis=0), white[rows].mean(axis=0)
        out[rows] = (sample[rows] - mean_dark) / (mean_white - mean_dark)
    return out


class MilkNirComposition(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What is the fat content of a cow's milk from one milking, read by an on-farm near-infrared sensor on a "
            "milking robot, in the weeks after the sensor was calibrated?"
        ),
        use_case=(
            "A dairy farm's milking robot reads each milking with a near-infrared sensor and predicts its fat content "
            "at once, to monitor each cow's health and milk quality without waiting for a laboratory; the calibration "
            "is updated as new laboratory references arrive."
        ),
        row=(
            "One milking of one of 41 Holstein cows on the Hooibeekhoeve experimental farm (Geel, Belgium), May to "
            "July 2017, sampled when a feeding trial took a laboratory sample (22% of the milkings)."
        ),
        predicted="The milk's fat content in percent by weight, from the laboratory's mid-infrared reference analysis.",
        known=(
            "At the end of the sensor's cycle, up to 144 seconds after the milking: the milk sample's near-infrared "
            "transmittance spectrum (256 pixels, nominally 960 to 1690 nm) referenced with that milking's own dark and "
            "white readings, the cow, the milk yield, the time since the previous milking, and the times of this and "
            "the previous milking."
        ),
        split=(
            "Each test window is one later week of measurements (four windows, the last four of the eight weeks); the "
            "model trains on every earlier week, as a calibration maintained with the references received so far."
        ),
        changes=(
            "We rebuild the spectrum from the sensor's raw counts with each milking's own references, as the deposit's "
            "normalised spectrum used the whole week's readings, later milkings included. We leave out the raw "
            "instrument readings themselves and the other laboratory values of the same sample."
        ),
        fit="direct",
        fit_reason=(
            "The rows are the sensor's own readings on a working farm in time order, with the cows the robot knows, "
            "and the test weeks follow the calibration weeks. The trial gave about 160 laboratory references a week, "
            "a farm about one per cow every 4 to 6 weeks; days in milk and parity, which a farm knows, are not in the "
            "deposit. One farm, one instrument, eight weeks."
        ),
    )

    # Dataset
    unique_name = "milk_nir_composition"
    year = "2023"
    domain = "chemistry & material science"
    source = "Other"
    source_url = "https://doi.org/10.5281/zenodo.8263430"
    license = "CC BY 4.0"
    data_tags = ()
    download_description = """
        mkdir -p local-data-warehouse/milk_nir_composition
        wget -O local-data-warehouse/milk_nir_composition/data_table.csv \\
          "https://zenodo.org/records/8263430/files/data_table.csv?download=1"
        md5sum local-data-warehouse/milk_nir_composition/data_table.csv  # 7cd61315ad73fbdc6461ad85f59b6f90
    """
    bibtex = r"""
        @dataset{diazolivares2023milknir,
          author = {Diaz-Olivares, Jose A. and van Nuenen, Arnout and Gote, Martin J. and Fonseca Diaz, Valeria and
                    Saeys, Wouter and Adriaens, Ines and Aernouts, Ben},
          title = {Near-infrared spectra dataset of milk composition in transmittance mode},
          year = {2023},
          version = {0.0.1},
          publisher = {Zenodo},
          doi = {10.5281/zenodo.8263430},
          url = {https://doi.org/10.5281/zenodo.8263430}
        }
    """
    curation_comments = """
        We start with `data_table.csv` (Zenodo record 8263430, version 0.0.1, 2023-08-18, md5 7cd61315...; 1,224 rows x 1,038 columns), described in the data paper Diaz-Olivares et al., Data in Brief 51 (2023) 109767 (doi 10.1016/j.dib.2023.109767).

        - Prediction point: the end of the sensor's cycle after a milking on the robot. The sensor reads the milk sample 39 to 107 seconds after the end of milking and that milking's dark and white references after it (54 to 122 and 71 to 144 seconds; the data paper says before), so every reading of a milking exists 144 seconds after it ends; the laboratory reference of that sample is still days away ("within no more than three days", data paper section 3.1). Known then: the spectrum, the cow, the milk yield, the interval since the previous milking and the clock times (USE-3, USE-6).
        - Target: `Fat` (milk fat, % w/w; MCC Vlaanderen, CombiFoss FT+, ISO 9622), renamed `fat_percent`, unchanged. One target per task: protein and lactose, also published, are other framings of the same spectra (CLEAN-18) and not built. The screening read 402 fat values in the NIR benchmark of Reiter et al. 2026 (arXiv 2605.21544); the deposit has a fat value on all 1,224 rows, and no missing value in any column.
        - The other laboratory values of the same sample (`Prot`, `Lact`, `SCC`, `Urea`) are dropped: they come from the same reference analysis as the target and are not known when the sensor reads (LEAK-10).
        - The spectrum, rebuilt from the deposit's raw counts: per pixel, (`Trans_Sample` - `Trans_Dark`) / (`Trans_White` - `Trans_Dark`) with the milking's own dark and white readings, the referencing against a Spectralon white and a black dark standard that the data paper describes for each sample ("with its corresponding white and dark reference") and the preprint names as the default ("a pair ... every time a milk sample spectrum was recorded"). The ratio is positive on every cell (0.0011 to 8.01; white - dark at least 185 counts), so nothing is clipped. The source reads these values as percent transmittance (Table 1's "%"; its absorbance of 4 to 5 at 1450 nm is log10(100/T)), so an absorbance taken from them is lower by a constant 2. State `raw`: referencing only, no smoothing, baseline, scatter correction or derivative. Declared as a spectrum (`special_features`, CLEAN-26).
        - The axis: the columns are `nir_<nm>` on the source's nominal axis 960 + 2.86 (p - 1) nm for pixel p, from the data paper (Table 1 note b: 256 pixels of a Carl Zeiss 1.7-256 plane grating spectrometer with a cooled InGaAs array, "distributed across a wavelength range of 960 nm to 1690 nm, at a resolution of 2.86 nm per pixel"), pixel 1 at the short-wavelength end. The source publishes no per-pixel calibration of the array, so the axis is nominal; it puts the window the source removed for its very low transmittance (1360 to 1500 nm, the preprint's Methods) at the pixels whose median transmittance is below 0.03, 1360 to 1492 nm, within about one pixel.
        - Not shipped: the deposit's `Trans_Tot`, "Normalized sample transmittance spectra" (Table 1). It is (sample - the week's mean dark) / (the week's mean white - the week's mean dark): to 5e-15 in weeks 2, 3, 7 and 8, and within 2.1e-3 in weeks 1, 4, 5 and 6, whose 46 samples without a reference were in the mean but are not in the deposit (`_decisions`). The data paper describes a pair at the start of each session and every 0.5 h, the preprint a pair with every sample; the deposit follows neither (PROV-13). Each test window is one week, so with `Trans_Tot` a test milking's spectrum depends on the other milkings of its window and on readings up to 45 hours later (85 hours in week 1), which the robot does not have when it predicts (LEAK-30). The references carry no label: ridge on a milking's dark, white or white - dark alone scores as the train mean (0.719 to 0.867 against 0.720 to 0.872). The rebuild's cost on the four windows (absorbance, mean RMSE in % fat): ridge 0.0983 to 0.0996, PLS with 15 components 0.1095 to 0.1125, PLS with 30 components on the Savitzky-Golay first derivative 0.0977 to 0.1017 (2.7 standard errors of a bootstrap over cows). Two other causal rebuilds score alike and were not taken, being constructions of ours, not the source's: the mean of the pairs of the past 30 minutes (0.0997, 0.1097, 0.1028; a free window length, and the 46 missing samples' pairs are not in the deposit) and a hold of one pair per 0.5 h of a session, the documented procedure (0.0982, 0.1123, 0.1001; needs session boundaries we infer).
        - Dropped as features: the raw instrument blocks `Trans_Dark`, `Trans_White` and `Trans_Sample` (768 columns in digital counts). They are known at the prediction point, and the shipped spectrum is built from each milking's own blocks; alone they predict no better than the train mean. Shipping them would let a method choose its own referencing (how often to take references, how to average them), which the data paper names as a research use; the source's on-farm models read the normalised spectrum. A choice for the curator.
        - Dropped: `SET`, the trial's week number (1 to 8), which follows from the milking time, and the sensor's timestamps `Time_Dark`, `Time_Sample` and `Time_White` (39 to 144 seconds after the end of milking): their offset from the milking's end tracks the milk yield, which is shipped (r 0.83 for the sample's reading), and adds little beyond it (partial correlation with fat given the yield -0.08).
        - Kept as features: `cow_id` (the robot identifies every cow; categorical, 41 cows), `milk_yield_liters`, `milking_interval_seconds` ("Time difference since the last milking", kept as published; it is 245 to 1,118 seconds shorter than the difference of the two milking timestamps, about one milking's duration), `milking_end` (`Time_Milk`, "end of milking process") and `previous_milking` (`Time_PrevMilk`). The two times are Unix seconds, converted to the farm's wall clock (Europe/Brussels, CEST, UTC+2 for every row) and stored without a time zone.
        - Note: 59 samples of five cows (55391, 55392, 55393, 55394, 59137) stay in the data. The related research article (Diaz-Olivares et al. 2020, bioRxiv 10.1101/2020.06.02.129742) removed "Fifty-nine of them [that] originated from four dairy cows that calved during the trial and from one individual animal that was less than five days in milk at the beginning of the experiment. To avoid the inclusion of colostrum samples", leaving 1,165 samples from 36 cows; the data paper releases all 1,224 and names only the 46 samples without a reference as removed. The deposit has no days in milk; without these five cows it gives the article's Table 3 exactly (week 1: 308 samples, weeks 2 to 8: 857), which identifies them. Their milk is not colostrum: its protein reaches at most 3.88% (colostrum's is far above 10%) and its lactose is normal (4.77% on average against 4.70%), so the article's removal also took the transition milk of the weeks after calving. They are the early-lactation milkings health monitoring is for: a fat-to-protein ratio above 1.4, a sign of ketosis, in 11.9% of their samples against 2.0% of the others; and they hold the largest fat value (7.6%, cow 55394, week 8; the article's range ends at 6.25%). As training rows they change nothing measurable (PLS 0.1053 trained with them against 0.1055 without, on the same test rows of the other cows); as test rows they hold 30% of week 8's squared error under ridge (four-window mean 0.0996 with them, 0.0985 without).
        - Note: a window's score hinges on a few milkings. Cow 50435's milking of 2017-07-11 21:38 has a laboratory fat of 2.59%, against 4.3 to 5.5% for the cow's neighbouring milkings; it is 67% of week 7's squared error under ridge (four-window mean 0.0996 with it, 0.0838 without), very likely the preprint's fat test error of -1.573, a sample or laboratory mix-up. It stays, as the source kept it (CLEAN-11, PROV-13). The ranking of model families holds on every window.
        - No duplicate rows and no duplicate spectra; no missing values.
        - Metric: RMSE of fat in % w/w, the source's RMSEP. The related research article (Diaz-Olivares et al. 2020, Computers and Electronics in Agriculture 178:105734) selects its PLS models by the RMSE of cross-validation, reports the RMSEP of the test set (with R2 beside it), and judges the sensor against ICAR's accuracy limits for on-farm and laboratory milk analysers, stated in RMSEP (MET-5: one deliberate criterion). Its real-time models, trained on week 1 and tested on weeks 2 to 8 of the 1,165 samples it kept, reached RMSEP 0.0826% for fat, after removing the 1360 to 1500 nm window, preprocessing and selecting wavelengths (the preprint, Table 4; the journal version was not reachable here). On that protocol (308 and 857 samples) ridge on this spectrum scores 0.101; on the shipped windows 0.0996 (absorbance, mean of the four windows). The protocols differ, so neither number is a target for the other. Training on week 1 only, instead of on every earlier week, raises ridge's four-window mean to 0.121: the calibration maintenance the windows test.
        - Encodings (2026-11-09, on the rebuilt spectrum and the four shipped windows, untuned: LightGBM with 500 trees, learning rate 0.03, 15 leaves and 30% of the bins per tree; ridge with alpha by GCV on standardised bins; PLS with 15 components; the spectrum alone, mean RMSE in % fat): as it is, LightGBM 0.276, ridge 0.107, PLS 0.107; with ALS and SNV 0.219, 0.095, 0.097; with SNV 0.224, 0.095, 0.097; with the Savitzky-Golay first derivative 0.141, 0.105, 0.104. The derivative lowers LightGBM's error on 4 of 4 windows, SNV ridge's on 3 of 4). The recommended encoding stays the spectrum as it is (CLEAN-26); the benchmark compares the candidates on every vibrational dataset. The train-mean dummy scores 0.798, and the cow's training mean alone 0.575.
    """

    # Task
    target = "fat_percent"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original="RMSEP, the root-mean-square error of prediction of fat in % w/w on the test samples",
        reference="https://doi.org/10.1016/j.compag.2020.105734",
        definition=(
            "sqrt(mean((y - y_hat)**2)) over the test milkings, fat in % w/w. The source selects PLS models by RMSECV "
            "and reports RMSEP, judged against ICAR's RMSEP limits for milk analysers (0.1% for laboratory systems)."
        ),
    )
    temporal = Temporal(
        on="milking_end",
        splits=TemporalSplits(
            window=3,
            unit="days",
            cutoffs=("2017-06-13", "2017-06-27", "2017-07-11", "2017-07-25"),
            gap=3,
        ),
    )
    splits_comment = """
        Four test windows, each one measurement week of the trial: weeks 8 (from 2017-07-25), 7 (from 2017-07-11), 6 (from 2017-06-27) and 5 (from 2017-06-13), each window three days from its start, which holds all of that week's samples, taken over 1 to 3 days (162, 168, 84 and 166 milkings). Each trains on every earlier week (1,062, 894, 810 and 644 milkings, 53% of the rows for the oldest window), the calibration maintenance the source asks for ("how to maintain them in time", data paper section 1; the research article: "By adding new samples to the calibration set ... the models can be made robust"). The test weeks are two weeks apart, so the calibration is refitted every fortnight; on a farm the references come from milk recording every 4 to 6 weeks. A three-day gap stands for the laboratory's delay ("within no more than three days"); each test week starts 4 to 13 days after the last milking of the week before it, so the gap removes no row. The source's real-time evaluation trained once on week 1 and tested on weeks 2 to 8 (Diaz-Olivares et al. 2020); week 4 and earlier need not be test windows here, as four windows with more than half of the rows on their train side exist (week 4's would hold 47.8%; SPLIT-14). The cows recur across the windows, as on a farm: 98.1% of a window's test milkings on average (98.8% pooled) are of a cow seen in training; four cows that calved during the trial appear only in weeks 6 to 8 and are new to the model in their first test window.
    """
    special_features = (
        Spectrum(
            name="nir_transmittance",
            prefix=PREFIX,
            unit="nm",
            technique="near_infrared",
            state="raw",
            description=(
                "The milk sample's long-wave near-infrared transmittance from the on-farm sensor (Carl Zeiss 1.7-256 "
                "plane grating spectrometer, cooled 256-pixel InGaAs array; 2 mm borosilicate cuvette; 100 scans of "
                "100 ms averaged): (sample - dark) / (white - dark) with the milking's own Spectralon white and black "
                "dark readings, rebuilt from the deposit's raw counts. The axis is the source's nominal linear one, "
                "960 + 2.86 nm per pixel (no per-pixel calibration is published); it matches the source's "
                "low-transmittance window of 1360 to 1500 nm within one pixel. The source reads the values as percent "
                "transmittance. No smoothing, baseline, scatter correction or derivative."
            ),
        ),
    )
    accepted_check_warnings = {}

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        raw = pd.read_csv(raw_dir / "data_table.csv")
        assert raw.shape == (1224, 1038), "The deposit's table changed"
        return raw

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1. The spectrum, rebuilt with each milking's own dark and white readings (the deposit's `Trans_Tot` used the
        #    week's mean readings, later milkings and test rows included: LEAK-30, PROV-13).
        spectrum = _own_pair_spectrum(raw)
        assert np.isfinite(spectrum).all(), "A ratio is not finite: the counts changed"
        assert (spectrum > 0).all(), "A ratio is not positive: the counts changed"
        # The formula and the blocks are the source's: its week-mean referencing gives `Trans_Tot` exactly in the weeks
        # the deposit holds whole.
        whole = raw["SET"].isin(WHOLE_WEEKS).to_numpy()
        deposit = raw[SOURCE_SPECTRUM].to_numpy(dtype="float64")
        assert np.abs(_week_mean_spectrum(raw)[whole] - deposit[whole]).max() < 1e-12, "Trans_Tot is not rebuilt"
        # 2. Keep the target and the robot's own fields; drop the other laboratory values of the sample (LEAK-10), the
        #    deposit's spectrum, the instrument's reference and raw-count blocks, and the sensor's bookkeeping.
        df = raw.drop(columns=[*OTHER_LAB_VALUES, *SOURCE_SPECTRUM, *SAMPLE, *DARK, *WHITE, *SENSOR_BOOKKEEPING])
        df = df.rename(columns=RENAME)
        assert list(df.columns) == list(RENAME.values())
        df = pd.concat([df, pd.DataFrame(spectrum, columns=SPECTRUM, index=df.index)], axis=1)
        # 3. The cow as a category (the robot knows it), never a number.
        df["cow_id"] = df["cow_id"].astype(str)
        # 4. Unix seconds to the farm's wall clock (CEST for every row), without a time zone.
        for col in ("milking_end", "previous_milking"):
            df[col] = pd.to_datetime(df[col], unit="s", utc=True).dt.tz_convert(FARM_TZ).dt.tz_localize(None)
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["cow_id"], datetime=["milking_end", "previous_milking"])

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        deposit = raw[SOURCE_SPECTRUM].to_numpy(dtype="float64")
        week_mean = np.abs(_week_mean_spectrum(raw) - deposit).max(axis=1)
        own_pair = np.abs(_own_pair_spectrum(raw) - deposit).max(axis=1)
        referencing = (
            pd.DataFrame({"week": raw["SET"], "week_mean": week_mean, "own_pair": own_pair})
            .groupby("week")
            .agg(
                milkings=("week_mean", "size"),
                max_diff_week_mean_reference=("week_mean", "max"),
                max_diff_own_pair=("own_pair", "max"),
            )
        )
        per_cow = raw.assign(fpr_above_1_4=raw["Fat"] / raw["Prot"] > 1.4).groupby("Cow_ID")
        per_cow = per_cow.agg(
            samples=("Fat", "size"),
            weeks=("SET", lambda s: ",".join(str(w) for w in sorted(set(s)))),
            fat_mean=("Fat", "mean"),
            fat_max=("Fat", "max"),
            protein_max=("Prot", "max"),
            fpr_above_1_4=("fpr_above_1_4", "sum"),
        )
        fresh = per_cow.loc[list(FRESH_COWS)].round(2)
        return [
            Decision(
                "Spectrum rebuilt with each milking's own references",
                "The deposit's Trans_Tot is the week-mean referencing (to machine precision in the weeks it holds "
                "whole), so a test milking's spectrum would depend on later readings of its window; the shipped "
                "spectrum uses the milking's own dark and white. Largest absolute difference to Trans_Tot per week:",
                referencing,
            ),
            Decision(
                "Samples of fresh cows kept",
                "The research article removed 59 samples of four cows that calved during the trial and one under five "
                "days in milk; the data paper releases them, their milk is not colostrum (protein at most 3.88%) and "
                "they are the early-lactation milkings health monitoring is for, so they stay. Without these five "
                f"cows ({int(fresh['samples'].sum())} samples here) the deposit gives the article's Table 3 exactly.",
                fresh,
            ),
        ]
