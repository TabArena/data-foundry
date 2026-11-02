"""Curated dataset definition for `basque_offshore_bivalve_biotoxins` (data-foundry v2). Evidence: README.md."""

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
    Splits,
    TaskSummary,
    Temporal,
    TemporalSplits,
    drop_columns,
)

OA_GROUP = ["OA", "DTX1", "DTX2"]  # okadaic acid and dinophysistoxins, the regulated OA group (Reg. (EU) 2021/1374)
OA_LOQ = 40.0  # the source's code for an okadaic-acid non-detect ("<" with the LOQ as VALUE), both laboratories
EU_LIMIT_OA_GROUP = 160.0  # ug OA eq/kg, Reg. (EC) 853/2004 Annex III, Section VII, Chapter V
SURVEY_WINDOW_DAYS = 14  # the newest survey of the two weeks up to the day it must be known by (sample - turnaround)
TURNAROUND_DAYS = 7  # a laboratory result (toxins, plankton counts) counts as known a week after its sample
CTD_TURNAROUND_DAYS = 0  # the CTD reads in situ: known on the day of the cast
NO_DATA = -999  # "NO DATA is indicated by -999" (Notes sheet of Hydrographic_variables.xlsx)
CTD_LAYER_DBAR = (1, 12)  # the layer the bivalves hang in: "collected at a depth ranging between 3 and 12 m"
# One Ostreopsis record, renamed in 2021 (descriptor Table 1, footnote a); the two columns never overlap.
OSTREOPSIS = ("plankton_ostreopsis_cf_siamensis", "plankton_ostreopsis_spp_siamensis_ovata")
# The test windows: 35 sampling days each, the oldest from the first day whose train side, after the 7-day gap, holds
# half the samples (SPLIT-14 counted in rows, SPLIT-10).
WINDOW_STARTS = (pd.Timestamp("2021-06-07"), pd.Timestamp("2021-11-30"), pd.Timestamp("2022-07-04"))
WINDOW_SAMPLING_DAYS = 35

# Each farm and the water station next to it ("Mendexa-Control ... very close to the AZTI pilot plant"; "Mussel
# Farm-CTD ... to the east of the Mussel Farm site", descriptor Sec. 4.1); the CTD sheet calls the second
# "CTD-Mussel Farm".
PAIRED_PLANKTON = {"AZTI pilot plant": "Mendexa-Control", "Mussel Farm": "Mussel Farm-CTD"}
PAIRED_CTD = {"AZTI pilot plant": "Mendexa-Control", "Mussel Farm": "CTD-Mussel Farm"}
CTD_CHANNELS = {
    "TEMPERATURE (°C)": "ctd_temperature_c",
    "SALINITY": "ctd_salinity_pss78",
    "SIGMA THETA (kg m-3)": "ctd_sigma_theta_kg_m3",
    "LT (%)": "ctd_light_transmission_pct",
    "CHLOROPHYLL-a (µg l-1)": "ctd_chlorophyll_a_ug_l",
    "OXYGEN SATURATION (%)": "ctd_oxygen_saturation_pct",
}


def _taxon_column(name: str) -> str:
    """`Dinophysis acuminata (cells l-1)` -> `plankton_dinophysis_acuminata`."""
    name = name.replace("(cells l-1)", "").replace("<5 μm", "lt5um").replace(">5 μm", "gt5um").replace("μm", "um")
    return "plankton_" + re.sub(r"[^0-9a-z]+", "_", name.lower()).strip("_")


def _latest_before(
    samples: pd.DataFrame, surveys: pd.DataFrame, paired: dict[str, str], turnaround: int
) -> tuple[pd.DataFrame, pd.Series]:
    """For each sample, the newest survey at least `turnaround` days before its date and at most SURVEY_WINDOW_DAYS
    older than that, at either water station; on a day with surveys at both, the station next to the sample's farm.
    Returns survey rows aligned with `samples` (missing where none) and the survey age in days.
    """
    surveys = surveys.reset_index(drop=True)
    positions = []
    for station, date in zip(samples["station"], samples["sample_date"], strict=True):
        known_by = date - pd.Timedelta(days=turnaround)
        window = (surveys["date"] <= known_by) & (surveys["date"] >= known_by - pd.Timedelta(days=SURVEY_WINDOW_DAYS))
        cand = surveys[window]
        cand = cand.assign(paired=(cand["water_station"] == paired[station]).astype(int))
        positions.append(cand.sort_values(["date", "paired"], kind="stable").index[-1] if len(cand) else -1)
    positions = np.asarray(positions)
    picked = surveys.iloc[np.where(positions >= 0, positions, 0)].reset_index(drop=True)
    none = np.repeat((positions < 0)[:, None], picked.shape[1], axis=1)
    picked = picked.mask(none)  # no survey in the window: missing
    picked.index = samples.index
    age = (samples["sample_date"] - picked["date"]).dt.days
    return picked.drop(columns=["date", "water_station"]), age


class BasqueOffshoreBivalveBiotoxins(AbstractCuratedDataset):
    # In brief: the task in plain words, for a reader who has not seen the source (first in the README).
    task_summary = TaskSummary(
        question=(
            "How much okadaic-acid-group toxin (the cause of diarrhetic shellfish poisoning) does a batch of mussels "
            "or oysters from an offshore farm off the Basque coast hold, before the laboratory result is back?"
        ),
        use_case=(
            "For example a shellfish food-safety manager or farm operator, on a sampling day, reads the plankton "
            "counts and toxin results already back from the laboratories and the day's water profile, and decides "
            "whether to stop harvesting as a precaution before the new result arrives. The source names "
            "precautionary closures and early warning of toxic blooms, but builds no model."
        ),
        row=(
            "One pooled bivalve sample (mussels or Pacific oysters) from the AZTI pilot plant or the Mussel Farm "
            "off Mendexa, SE Bay of Biscay, analysed for the okadaic-acid group: 280 samples, April 2016 to June "
            "2023, sampled up to daily during toxic episodes."
        ),
        predicted=(
            "The okadaic-acid-group concentration in micrograms of okadaic-acid equivalent per kg of flesh. "
            "67% of the samples are below the laboratory's quantification limit and carry its code of 40; the EU "
            "limit is 160. Shipped on a log scale, scored on the concentration."
        ),
        known=(
            "The farm, the shellfish species, the analysing laboratory and the date; the water profile of the newest "
            "probe cast of the past two weeks, the same day included; the counts of 41 potentially toxic plankton "
            "taxa from the newest survey 7 to 21 days old; the farm's latest toxin result at least a week old. A "
            "laboratory result counts as known a week after its sample."
        ),
        split=(
            "Test samples come after all training samples, a week later at least, in three windows of 35 sampling "
            "days from June 2021 to June 2023: the end of the spring 2021 episode, the spring 2022 episode (refit "
            "before it) and a quiet year. The oldest window trains on half the samples."
        ),
        changes=(
            "We built the target and the rows from AZTI's long table and joined the plankton and water surveys "
            "by date, rather than use the benchmark copy that pooled 24 toxins in five units."
        ),
        fit="approximate",
        fit_reason=(
            "The source names closures at the regulatory limit and early warning of blooms, but no model. It states "
            'no turnaround for either laboratory: toxin analysis was "initiated within two days of sampling" for '
            'refrigerated samples, and plankton samples were stored "until analysis" and settled before counting. '
            "The week we allow for both results is an assumption on the cautious side, not a stated delay."
        ),
    )

    # Dataset
    unique_name = "basque_offshore_bivalve_biotoxins"
    year = "2025"  # Mendeley Data v1 of 2025-03-26 (PROV-9)
    domain = "environmental science & climate"
    source = "Other"  # AZTI's release on Mendeley Data (PROV-8); the GitHub benchmark of Zhou et al. 2026 is a copy
    source_url = "https://doi.org/10.17632/vyz9zvddz4.2"
    license = "CC BY 4.0"  # stated on the Mendeley Data page (the Data in Brief article itself is CC BY-NC)
    data_tags = ()
    download_description = """
        We download version 2 of AZTI's release from Mendeley Data (doi:10.17632/vyz9zvddz4.2): the three tables, "Biotoxins in bivalves.xlsx" (sha256 b2e49eb1...), "Toxic_phytoplankton_v2.xlsx" (716abd69..., new in v2) and "Hydrographic_variables.xlsx" (d7a00558...).
        mkdir -p local-data-warehouse/basque_offshore_bivalve_biotoxins && cd local-data-warehouse/basque_offshore_bivalve_biotoxins
        B=https://data.mendeley.com/public-files/datasets/vyz9zvddz4/files
        curl -L -o "Biotoxins in bivalves.xlsx" $B/2600377e-de07-466e-9a33-fd270e7f0dbf/file_downloaded
        curl -L -o Toxic_phytoplankton_v2.xlsx $B/65695b2e-734b-4b88-bc2a-326a5a404d3c/file_downloaded
        curl -L -o Hydrographic_variables.xlsx $B/74f2f926-2186-4678-b5c5-4d5e32bbf6f7/file_downloaded
    """
    bibtex = """
        @misc{solaun2025basque,
          title = {Long-term monitoring of potentially toxic phytoplankton, marine biotoxins and hydrographic variables in open waters off the Basque coast ({SE} Bay of Biscay)},
          author = {Solaun, Oihana and Zorita, Izaskun and Revilla, Marta and Gonz{\\'a}lez, Manuel and Larreta, Joana and Cuesta, Luis and Font{\\'a}n, Almudena and Ferrer, Luis and Sagarminaga, Yolanda and Laza, Aitor and Assadi, Carolina and Rodr{\\'i}guez, Jos{\\'e} Germ{\\'a}n},
          year = {2025},
          publisher = {Mendeley Data},
          note = {Version 2. Data descriptor: Solaun et al. (2025), Data in Brief 61:111736, doi:10.1016/j.dib.2025.111736},
          doi = {10.17632/vyz9zvddz4.2},
          howpublished = {\\url{https://doi.org/10.17632/vyz9zvddz4.2}}
        }
    """
    curation_comments = """
        We start with the three tables of AZTI's Mendeley Data release v2 (Solaun et al. 2025): "Biotoxins in bivalves" (5,446 rows in long format, 24 toxin variables, 344 samples of 2013-12 to 2023-06 at the AZTI pilot plant and the Mussel Farm), "Phytoplankton" (531 depth samples of 45 potentially toxic taxa in cells/l, 152 surveys at Mendexa-Control and Mussel Farm-CTD) and "Hydrographic variables" (180 CTD casts).

        - Prediction point: the day a bivalve sample is taken, before its toxin result. Known then: the farm, the species, the laboratory, the date, the newest CTD cast of the past 14 days (the same day included: the probe reads in situ), the newest plankton survey 7 to 21 days old, and the farm's latest toxin result from a sample at least 7 days older. One turnaround for each laboratory result, a week, since the source states none: toxin analysis was "initiated within two days of sampling" when the sample was refrigerated, "otherwise, they were frozen" (Sec. 4.1); plankton samples were "preserved in the dark and cool (4 °C) until analysis", then a 50 ml subsample "was sedimented" (20 to 50 h by the usual Utermöhl protocols) and counted at an outside laboratory (Sec. 4.3), which rules out a count on the sampling day (LEAK-10). Plankton lags of 1, 3 and 7 days score alike (pooled RMSE of tuned LightGBM about 104, 106 and 101 ug/kg). The descriptor: "This will allow food safety managers to ban the sales when the biotoxins exceed the regulatory limits or temporarily close the harvesting areas as a precautionary measure"; its early warning is "for toxic algal blooms" (Value of the Data).
        - Rebuilt from AZTI's release, not from the "biotoxin" table of Zhou et al. 2026 (GitHub zhm12305/marine-ml-benchmark), whose target pools the 24 toxin variables in five units and whose only inputs are the two stations' coordinates (PROV-13, PROV-15).
        - Rows: the 280 samples with the okadaic-acid group analysed (2016-04-15 to 2023-06-22; the lipophilic panel starts in 2016). The 64 samples without it (22 with domoic acid only in 2013-2015, 42 with a partial panel without the okadaic-acid group in 2020-2021) have no target.
        - Target: the okadaic-acid group, OA + DTX1 + DTX2 in ug OA eq/kg (the group the EU limit of 160 covers), from the quantified values; a sample with none quantified takes the source's non-detect code for OA, 40, its limit of quantification at both laboratories (188 of 280, 67.1%). DTX1 is never quantified and DTX2 only three times, next to a quantified OA, so the target is OA plus those three values. Shipped as its natural log (`target_transform="log"`), scored on ug/kg.
        - Why a level and not the exceedance of 160 (USE-5): the level is what the actor reads. Precautionary closures act below the limit (the descriptor's "temporarily close the harvesting areas as a precautionary measure"), the laboratory reports the level, and forecasts of DSP toxins in mussels model the level (Cruz et al. 2022, Portuguese farms, 1 to 4 weeks ahead). 47 of 280 samples exceed 160, in five spring episodes (2017, 2018, 2019, 2021, 2022; the okadaic-acid group was not measured in the 2020 season). An exceedance target would not fix the thin test: the newest window holds no exceedance either.
        - Plankton: per taxon the maximum count over the survey's depths (one to six Niskin depths until 2018-05, three hose layers from 2018-06), from the newest survey 7 to 21 days before the sample, at either water station, the farm's own on a day with both (`_latest_before`); with its age in days and the sampling method. 86 samples have no survey in that window: missing. The two Ostreopsis columns are one record renamed in 2021 (Table 1, footnote a), never both above zero: summed into `plankton_ostreopsis_spp` (CLEAN-12). Taxa never counted in a matched survey are dropped (constant zero): 41 taxa ship.
        - Note: 16 taxa (four Pseudo-nitzschia species, Alexandrium ostenfeldii and the tamarense complex, Azadinium, Pfiesteria, Heterosigma akashiwo, Phaeocystis globosa and six more) are counted only by the 2014-2017 laboratory (UPV/EHU); the later one (Oceansnell, from 2017-12) does not resolve them, so a zero after 2017 means "not resolved", not "absent" (CLEAN-21). They are above zero in 15 training samples and zero in every test sample; none is an okadaic-acid producer, so they stay.
        - Water profile: the mean over 1-12 dbar (the bivalves hang at 3-12 m, descriptor Sec. 4.1) of temperature, salinity, sigma-theta, light transmission, chlorophyll and oxygen saturation from the newest CTD cast within 14 days, the same day included, matched the same way, with its age; -999 to missing. PAR (light at the cast's hour) and dissolved oxygen (derived from the saturation, temperature and salinity, R^2 0.998) left out.
        - Last result: the farm's highest okadaic-acid-group value (non-detects at 40) on its latest sampling day at least 7 days before, with its age in days. The actor reads it; it is the only lag of the target (TP-10).
        - Dropped: coordinates and datum (one value per farm), the species name (a copy of the shellfish type).
        - History: every sample from 2016-04 is kept, across breaks: about monthly sampling at the AZTI pilot plant only in 2016-2018 (with the 2017 and 2018 episodes), plankton sampled by Niskin bottle until 2018-05 and by hose from 2018-06, the Mussel Farm from 2019-06, the toxin laboratory changed in 2020-01 (every test sample is from the second), and the okadaic-acid group not measured in the 2020 season. The 2017-2019 episodes are the only earlier seasons to learn from (SPLIT-20).
        - Note: sampling runs up to daily during toxic episodes (87 samples within 3 days of the farm's previous one: 37 same-day mussel and oyster pairs and 50 taken one to three days later), so episodes weigh more in training and test than quiet weeks; no feature counts the sampling frequency.
        - Note: INTECMAR (to 2019-12) reports one decimal, CECOPESCA-ANFACO (from 2020-01) whole numbers; the LOQs are the same.
        - A tabular task, not forecasting (TP-10), on the three windows (oldest first; RMSE in ug/kg; 95% intervals from a bootstrap over ISO weeks): LightGBM tuned on the training side scores 85 / 164 / 20 and CatBoost 92 / 162 / 19, against the farm's last known result 160 / 189 / 7, its calendar-month mean 115 / 214 / 198 and median 115 / 204 / 106 from training. The gain over the best of these in each window is [-24, 49] / [-10, 90] / [-21, -5]: ahead on point estimates in both toxic windows with no interval clear of 0, and behind the last result (nearly always the code 40) in the quiet window. Pooled over the windows, the gain over the last result is [6, 65]. With all inputs, the plankton and CTD add nothing measurable to an untuned LightGBM on the farm's own series (pooled gain [-18, 23]). The last result is the only lag of the target and the actor reads it (TP-10 as amended 2026-10-26).
        - Note (TP-9): the test rests on few events. The windows hold 6, 7 and 0 exceedances of 160 and 12, 11 and 2 values above the code in 37, 42 and 59 samples; 3 of the 13 test exceedances are onsets (after a last result at or below 160), the other 10 fall while the farm's last result is above it. The 3 or 4 highest samples carry 74-91% of each toxic window's squared error. For the limit, the tuned model's ROC AUC is 0.98 [0.90, 1.00] and 0.87 [0.74, 0.99] and its recall 5 of 6 and 3 of 7 (the last result: 6 of 6 and 4 of 7); no quiet-window prediction crosses 160. No split that keeps half the samples for training avoids a quiet newest window, as the last exceedance is on 2022-05-23; revisit when AZTI publishes seasons after 2023.
        - Note: 188 of 280 targets (67.1%) are the non-detect code 40: left-censored at the LOQ, kept as the low regime (Andrej, 2026-10-30).
    """

    # Task
    target = "log_oa_group_ug_kg"
    problem_type = "regression"
    metric = Metric.fallback(
        reason=(
            "The data descriptor (Solaun et al. 2025, Data in Brief 61:111736) fits no model and the Mendeley page "
            "defines no task. The source team's study of okadaic acid in these mussels (Revilla et al. 2025, "
            "Regional Studies in Marine Science, doi:10.1016/j.rsma.2025.104556) was found by its title; its "
            "methods are unread (neither the publisher's page nor the AZTI repository copy opened). Zhou et al. "
            '2026 (PLOS ONE, Sec. 2.4) rank their benchmark by R^2 "for cross-dataset comparability", on a copy '
            "that pools 24 toxins in five units: a target that does not carry over (MET-2). RMSE on the "
            "concentration in ug OA eq/kg; the ROC AUC and the recall at the EU limit of 160 per window are in the "
            "notes."
        ),
        target_transform="log",
    )
    temporal = Temporal(on="sample_date", horizon=12, horizon_unit="months", gap=TURNAROUND_DAYS, gap_unit="days")
    splits_comment = """
        Three windows of 35 sampling days, each with an expanding train side that ends 7 days before the window starts (SPLIT-10: a toxin result counts as known a week after its sample): 2021-06-07 to 2021-11-24 (37 samples, 12 quantified, 6 above the EU limit; the end of the 2021 episode, which began on 2021-03-10, so a refit in the middle of it, with 17 of its 24 exceedances in training and 1 in the gap), 2021-11-30 to 2022-06-28 (42, 11, 7; a refit before the 2022 episode) and 2022-07-04 to 2023-06-22 (59, 2, 0; a quiet year). The oldest window starts on the first sampling day whose train side, after the gap, holds half the samples: 140 of 280 (50.0%; SPLIT-14 counted in rows). The samples of one day stay on one side. The horizon of 12 months is the newest window's year; the other two span 6 and 7 months.
    """

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "toxins": pd.read_excel(raw_dir / "Biotoxins in bivalves.xlsx", sheet_name="Biotoxins"),
            "plankton": pd.read_excel(raw_dir / "Toxic_phytoplankton_v2.xlsx", sheet_name="Phytoplankton", header=None),
            "ctd": pd.read_excel(raw_dir / "Hydrographic_variables.xlsx", sheet_name="Hydrographic variables"),
        }

    def _samples(self, toxins: pd.DataFrame) -> pd.DataFrame:
        """One row per bivalve sample with the okadaic-acid group analysed, and its target in ug OA eq/kg."""
        tox = toxins.assign(
            station=toxins["STATION"].replace({"Mussel Farm (MF)": "Mussel Farm"}),
            sample_date=pd.to_datetime(toxins["UTC DATE (YYYYMMDD)"].astype(str), format="%Y%m%d"),
        )
        key = ["station", "sample_date", "TYPE OF MOLLUSC"]
        oa = tox[tox["VARIABLE (abbreviation)"].isin(OA_GROUP)]
        quantified = oa["VALUE"].where(oa["<=>"] == "=")
        total = quantified.groupby([oa[k] for k in key]).sum(min_count=1)
        samples = oa.groupby(key, sort=True).agg(laboratory=("LABORATORY", "first")).join(total.rename("oa_group"))
        samples["oa_group"] = samples["oa_group"].fillna(OA_LOQ)  # no analogue quantified: the source's code
        return samples.reset_index().rename(columns={"TYPE OF MOLLUSC": "shellfish"})

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # 1. The rows and the target: samples with the okadaic-acid group analysed.
        df = self._samples(raw["toxins"])

        # 2. Plankton surveys: one row per station and day, each taxon's maximum over the depths; the two Ostreopsis
        #    columns are one record renamed in 2021 (CLEAN-12). Known a turnaround after the survey (LEAK-10).
        pl = raw["plankton"]
        header = pl.iloc[0].tolist()
        pl = pl.iloc[2:].set_axis(header, axis=1)  # row 2 of the sheet names each taxon's toxin group
        taxa = header[8:]
        counts = pl[taxa].apply(pd.to_numeric).set_axis([_taxon_column(t) for t in taxa], axis=1)
        ostreopsis = counts[list(OSTREOPSIS)].sum(axis=1, min_count=1)
        counts = counts.drop(columns=list(OSTREOPSIS)).assign(plankton_ostreopsis_spp=ostreopsis)
        taxon_columns = list(counts.columns)
        counts["water_station"] = pl["STATION"].to_numpy()
        counts["date"] = pd.to_datetime(pl["UTC DATE (YYYYMMDD)"]).to_numpy()
        counts["plankton_sampling_method"] = pl["SAMPLING METHOD"].to_numpy()
        surveys = counts.groupby(["water_station", "date"], sort=True).agg(
            {**dict.fromkeys(taxon_columns, "max"), "plankton_sampling_method": "first"}
        )
        picked, age = _latest_before(df, surveys.reset_index(), PAIRED_PLANKTON, TURNAROUND_DAYS)
        df = pd.concat([df, picked], axis=1)
        df["plankton_survey_age_days"] = age

        # 3. CTD casts: the mean over the bivalves' layer of six channels, -999 to missing.
        ctd = raw["ctd"].rename(columns=CTD_CHANNELS)
        layer = ctd["PRESSURE (dbar)"].between(*CTD_LAYER_DBAR)
        chans = list(CTD_CHANNELS.values())
        ctd[chans] = ctd[chans].mask(ctd[chans] == NO_DATA)
        casts = ctd[layer].groupby(["STATION", "UTC DATE (YYYYMMDD)"], sort=True)[chans].mean().reset_index()
        casts["date"] = pd.to_datetime(casts["UTC DATE (YYYYMMDD)"].astype(str), format="%Y%m%d")
        casts = casts.rename(columns={"STATION": "water_station"}).drop(columns="UTC DATE (YYYYMMDD)")
        picked, age = _latest_before(df, casts, PAIRED_CTD, CTD_TURNAROUND_DAYS)
        df = pd.concat([df, picked], axis=1)
        df["ctd_cast_age_days"] = age

        # 4. The farm's last known result: its highest value on its latest sampling day at least 7 days earlier.
        day_max = df.groupby(["station", "sample_date"], sort=True)["oa_group"].max().reset_index()
        last, last_age = [], []
        for station, date in zip(df["station"], df["sample_date"], strict=True):
            prev = day_max[
                (day_max["station"] == station) & (day_max["sample_date"] <= date - pd.Timedelta(days=TURNAROUND_DAYS))
            ]
            last.append(prev["oa_group"].iloc[-1] if len(prev) else np.nan)
            last_age.append((date - prev["sample_date"].iloc[-1]).days if len(prev) else np.nan)
        df["last_result_oa_group_ug_kg"] = last
        df["last_result_age_days"] = last_age

        # 5. Taxa never counted in a matched survey are constant zero (CLEAN-5).
        plankton_cols = [c for c in df.columns if c.startswith("plankton_") and c != "plankton_sampling_method"]
        never = [c for c in plankton_cols if not (df[c] > 0).any() and c != "plankton_survey_age_days"]

        # 6. The target on the log scale; scored on ug/kg through target_transform="log".
        df[self.target] = np.log(df["oa_group"])
        return drop_columns(df, ["oa_group", *never])

    def _make_splits(self, df: pd.DataFrame) -> Splits:
        """Three windows of 35 sampling days; train keeps the samples taken at least 7 days before a window starts."""
        time_on = self.temporal.on
        dates = df[time_on]
        windows = TemporalSplits(window=WINDOW_SAMPLING_DAYS, unit="unique", cutoffs=WINDOW_STARTS).splits(df, time_on)
        splits: Splits = {}
        for split, folds in windows.items():
            train, test = (np.asarray(side) for side in folds[0])
            known = (dates.iloc[train] <= dates.iloc[test].min() - pd.Timedelta(days=TURNAROUND_DAYS)).to_numpy()
            splits[split] = {0: (train[known].tolist(), test.tolist())}
        assert dates.iloc[splits[0][0][1]].max() == dates.max(), "the newest window must reach the end of the data"
        assert len(splits[len(splits) - 1][0][0]) >= len(df) / 2, "the oldest window must train on half the samples"
        return splits

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=["station", "shellfish", "laboratory", "plankton_sampling_method"],
            datetime={"sample_date": "%Y-%m-%d"},
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        oa_group = np.exp(df[self.target])
        table = (
            pd.DataFrame(
                {
                    "year": df["sample_date"].dt.year,
                    "samples": 1,
                    "quantified": oa_group > OA_LOQ,
                    "above_eu_limit_160": oa_group > EU_LIMIT_OA_GROUP,
                }
            )
            .groupby("year")
            .sum()
        )
        return [
            Decision(
                title="A level, not the exceedance of the EU limit",
                why=(
                    "The level is what the actor reads (USE-5): precautionary closures act below the limit of 160 ug "
                    "OA eq/kg, the laboratory reports the level, and forecasts of DSP toxins in mussels model it "
                    "(Cruz et al. 2022). The exceedances fall in five spring episodes, 6, 7 and 0 of the 47 in the "
                    "three test windows, so an exceedance target would leave the newest window without a positive too."
                ),
                evidence=table,
            )
        ]
