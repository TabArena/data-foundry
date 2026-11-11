"""Curated dataset definition for `superconductivity` (data-foundry v2). Evidence: README.md."""

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
    ScoringColumn,
    Source,
    SplitPlan,
    Splits,
    TaskSummary,
    Temporal,
    UnitWeight,
)

MDR_FILE = "20240322_MDR_OAndM.txt"
"""The MDR SuperCon Datasheet Ver.240322 (NIMS, CC BY 4.0, doi:10.48505/nims.4487), one row per SuperCon entry."""

SHARE_TOLERANCE = 0.003
"""How far a datasheet entry's element shares may lie from a composition's (L1) to count as the same material."""

WINDOWS = ((1996, 2002), (2002, 2009), (2009, 2020))
"""The test windows as `[first year, last year + 1)`: the eras 1996-2001, 2002-2008 and 2009-2019."""

_ELEMENT_SYMBOLS = (
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb "
    "Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au "
    "Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr"
)

ELEMENTS = frozenset(_ELEMENT_SYMBOLS.split())
"""The chemical symbols a SuperCon formula may use."""

_AMOUNT = re.compile(r"^[0-9]*\.?[0-9]+")
_VARIABLE_OXYGEN = re.compile(r"O([0-9.]+[-+=]+[A-Za-z]?|[XZxyzd])(?=[A-Z]|$)")


def composition_labels(elements: pd.DataFrame) -> pd.Series:
    """One label per composition, for the rows of ``unique_m.csv`` (its element counts and formulas).

    A composition is the share of each element in the formula; the 81 features are computed from these shares, so
    rows with the same shares are the same input. The shares are compared at 6 decimals, which only removes
    floating-point noise (5 to 8 decimals give the same 15,164 compositions). This joins formulas that write one
    composition differently: in another element order (`Dy1Ir2Rh2B4`, `Dy1Rh2Ir2B4`) or scaled (`V2Zr1`,
    `V66.6Zr33.3`). A composition is labelled by its most frequent formula (ties: the first in sort order).
    """
    counts = elements.drop(columns=["critical_temp", "material"])
    shares = counts.div(counts.sum(axis=1), axis=0).round(6)
    key = pd.Series(pd.util.hash_pandas_object(shares, index=False).to_numpy(), index=elements.index)
    label = {}
    for value, formulas in elements["material"].groupby(key, sort=False):
        frequency = formulas.value_counts()
        label[value] = min(frequency.index, key=lambda formula: (-frequency[formula], formula))
    return key.map(label)


def parse_formula(formula: str) -> dict[str, float] | None:
    """The amount of each element in a SuperCon formula (the datasheet's `element` column), or None if unreadable.

    An amount is the leading number of the token after the symbol, so a variable part keeps its number (`O7-z` is 7,
    `O4+d` is 4) and a bare variable or nothing counts as 1 (`Cu3Oz` is one oxygen, as UCI writes it). `X` and `Z`
    are never element symbols in this file; they are variables.
    """
    text = str(formula).strip().replace(" ", "")
    text = re.sub(r"[XZ](?![a-z])", "z", text)
    text = re.sub(r"(?<=[0-9.])[-+=]+[A-Za-z]?(?=[A-Z]|$)", "", text)
    amounts: dict[str, float] = {}
    position, length = 0, len(text)
    while position < length:
        if not text[position].isupper():
            return None
        if position + 1 < length and text[position + 1].islower() and text[position : position + 2] in ELEMENTS:
            symbol, position = text[position : position + 2], position + 2
        elif text[position] in ELEMENTS:
            symbol, position = text[position], position + 1
        else:
            return None
        end = position
        while end < length and not text[end].isupper():
            end += 1
        token, position = text[position:end], end
        number = _AMOUNT.match(token)
        if number:
            amount = float(number.group(0))
        elif token == "" or token[0].isalpha():  # `Cu3O`, `Cu3Oz`: one oxygen
            amount = 1.0
        else:
            return None
        if amount > 0:
            amounts[symbol] = amounts.get(symbol, 0.0) + amount
    return amounts or None


def _shares(amounts: list[dict[str, float]], elements: list[str]) -> tuple[np.ndarray, list[str]]:
    """The element shares of each formula (rows summing to 1) and its element set, as a key in column order."""
    matrix = np.array([[a.get(element, 0.0) for element in elements] for a in amounts], dtype=float)
    matrix = matrix / matrix.sum(axis=1, keepdims=True)
    keys = ["".join(element for element in elements if a.get(element, 0.0) > 0) for a in amounts]
    return matrix, keys


def first_report_year(unique_m: pd.DataFrame, composition: pd.Series, mdr_path: Path) -> pd.Series:
    """The year each composition was first reported, from the MDR SuperCon Datasheet (``mdr_path``).

    The datasheet is the parent of UCI 464's rows and gives every entry the publication year of its reference, which
    the UCI release drops. A datasheet entry belongs to a composition when it holds exactly the same elements and its
    element shares lie within :data:`SHARE_TOLERANCE` (L1) of the composition's, which joins the same material
    written at another scale or with a variable oxygen. Formulas with a variable oxygen are matched twice, once with
    its number (`O7-z` as 7) and once with a single oxygen, because UCI writes some cuprates as `...Cu3O`.

    Returns:
        The earliest year per composition label, for the compositions the datasheet holds.
    """
    elements = [c for c in unique_m.columns if c not in ("critical_temp", "material")]
    mdr = pd.read_csv(mdr_path, sep="\t", skiprows=[0], dtype=str, keep_default_na=False, usecols=["element", "year"])
    years = pd.to_numeric(mdr["year"], errors="coerce").to_numpy()

    parsed: list[dict[str, float]] = []
    entry: list[int] = []
    for i, formula in enumerate(mdr["element"]):
        amounts = parse_formula(formula)
        if amounts is None or set(amounts) - set(elements):
            continue
        parsed.append(amounts)
        entry.append(i)
        if amounts.get("O", 1.0) != 1.0 and _VARIABLE_OXYGEN.search(str(formula)):
            parsed.append({**amounts, "O": 1.0})
            entry.append(i)
    entry_shares, entry_keys = _shares(parsed, elements)
    entry_year = years[np.array(entry)]
    by_element_set: dict[str, list[int]] = {}
    for j, key in enumerate(entry_keys):
        by_element_set.setdefault(key, []).append(j)

    one_row = unique_m[elements].groupby(composition.to_numpy(), sort=False).first()
    comp_shares, comp_keys = _shares([row.to_dict() for _, row in one_row.iterrows()], elements)
    first: dict[object, float] = {}
    for c, key in enumerate(comp_keys):
        candidates = by_element_set.get(key)
        if not candidates:
            continue
        candidates = np.asarray(candidates)
        distance = np.abs(entry_shares[candidates] - comp_shares[c]).sum(axis=1)
        matched = entry_year[candidates[distance <= SHARE_TOLERANCE]]
        matched = matched[~np.isnan(matched)]
        if len(matched):
            first[one_row.index[c]] = float(matched.min())
    return pd.Series(first, dtype="float64")


class Superconductivity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=("Below what temperature does a material with this chemical composition become superconducting?"),
        use_case=("A materials scientist screens candidate compositions and decides which to synthesize and measure."),
        row="One measured entry of the SuperCon database; a composition can have several entries.",
        predicted="The critical temperature, in kelvin.",
        known=(
            "81 numbers computed from the chemical formula alone (statistics of the elements' atomic properties, "
            "weighted by their shares), and the year the composition was first reported, which orders the split."
        ),
        split=(
            "The test data is every composition first reported in a later era (1996-2001, 2002-2008, 2009-2019); "
            "training is every entry of an earlier year, so a model meets families that were not yet known."
        ),
        changes=(
            "We join each composition's first report year from the NIMS SuperCon datasheet and split by it; the 100 "
            "entries (0.5%) it does not date leave. With random rows, 35% of the test rows had an identical row in "
            "training. Each composition counts once in the score, where the source counts each entry."
        ),
        fit="approximate",
        fit_reason=(
            "The features come from the formula, which is all a scientist has before synthesis, and a window of "
            "later-reported compositions is what a screen meets. But every row is a known superconductor (all "
            "critical temperatures above 0 K), while most candidates do not superconduct, so a model trained here "
            "gives every candidate a critical temperature."
        ),
    )

    # Dataset
    unique_name = "superconductivity"
    domain = "physics & astronomy"
    sources = (
        Source(
            role="publication",
            platform="UCI",
            url="https://doi.org/10.24432/C53P47",
            license="CC BY 4.0",
            year="2018",
            bibtex="""
                @article{hamidieh2018data,
                  title={A data-driven statistical model for predicting the critical temperature of a superconductor},
                  author={Hamidieh, Kam},
                  journal={Computational Materials Science},
                  volume={154},
                  pages={346--354},
                  year={2018},
                  publisher={Elsevier}
                }
            """,
        ),
    )
    download_description = """
        We download the data from the UCI repository and uzip it to a predefined folder.

        mkdir -p local-data-warehouse/superconductivity/ && wget -P local-data-warehouse/superconductivity/ https://archive.ics.uci.edu/static/public/464/superconductivty+data.zip && unzip local-data-warehouse/superconductivity/superconductivty+data.zip -d local-data-warehouse/superconductivity/ && rm local-data-warehouse/superconductivity/superconductivty+data.zip

        The year of each composition's first report comes from the parent database's own export, the MDR SuperCon
        Datasheet Ver.240322 (National Institute for Materials Science, doi:10.48505/nims.4487), which is published
        under CC BY 4.0 and asks to be cited when it is used:

        wget -O local-data-warehouse/superconductivity/20240322_MDR_OAndM.txt https://mdr.nims.go.jp/filesets/2347b413-9c15-43b7-90e6-41fe9243b1a5/download
    """
    curation_comments = """
        - The 81 features are computed from the element shares of the chemical formula alone. `unique_m.csv` (row-aligned with `train.csv`, same critical temperatures) has each row's element counts and formula; from it we build the composition key (see `composition_labels`): 15,164 compositions, 2,422 of them with 2 to 110 SuperCon entries (6,099 repeated rows). Their temperatures differ by a median standard deviation of 1.3 K, by more than 30 K for 132 compositions (other samples, phases or pressures, which the release does not record). Since 2026-11-11 the key no longer groups the split (the year does), but it stays in the frame as the unit the score counts: metadata the model never sees (`unit_weight`), not a feature.
        - Every entry is kept (SPLIT-26), and each composition counts once in the score (Lennart, 2026-11-08, review issue 3, issue 1 of that round): the RMSE weights an entry by 1 over its composition's number of entries (`composition_weight`), a scoring column for the metric only, no feature and no training weight. All 81 inputs are fixed by the composition (equal within 2,416 of the 2,422 compositions with several entries; in the other 6, formulas written at another scale such as `Au30Pd3.3Te66.6` and `Au0.3Pd0.033Te0.666`, they differ by floating-point noise, at most 3e-15 relative), so a model predicts one value per composition, and the materials scientist decides per composition which to synthesize (MET-1, MET-17). Unweighted, YBa2Cu3O7 (110 entries) counted 110 times a composition measured once, and the 2,422 compositions with several entries held 40% of the rows; weighted, the 12,742 compositions with one entry carry 84% of the weight. On the 9 splits of the composition-grouped protocol the weighted RMSE ranked 8 untuned predictors (random forest, extra trees, two LightGBM, two ridge, kNN, the training mean) like the per-entry RMSE at Kendall tau 0.98 per split on average (lowest 0.93) and 0.93 for the ranking by the mean over the splits, the same best model on 9 of 9. Not deduplicated: Stanev et al. (2018) average the entries of a material instead (standard deviation below 5 K) and drop the rest; we keep the release's rows, and the weight gives each composition the one vote their averaging gives it.
        - Time basis: samples over time, dated from the parent source. Each row is one report of a superconductor, read out of the literature of 1913 to 2019; the catalogue grew in waves of families (the cuprates from 1986, MgB2 in 2001, the iron-based superconductors from 2008), so the population and the typical critical temperature move with the year. The UCI release drops the reference, but the parent database's own export dates the entries (next bullet), so the split follows the year and `Timeless`, `StationaryRelation` and a split forced from temporal are all ruled out.
        - Dated through the MDR SuperCon Datasheet Ver.240322 (NIMS, doi:10.48505/nims.4487, CC BY 4.0, cite it when the year is used; 33,458 entries, 33,302 with the publication year of their reference, 1913 to 2023), the parent of Hamidieh's extract. A datasheet entry belongs to a composition when it holds the same elements and its element shares lie within 0.003 (L1) of the composition's; a formula's variable part keeps its number (`O7-z` is 7 oxygens) and is matched a second time as a single oxygen, because UCI writes some cuprates as `...Cu3O` (`first_report_year`). The earliest year of a composition's matched entries is its `first_year`.
        - The dating is checked three ways: it dates 21,163 of the 21,263 rows (99.5%) and 15,065 of the 15,164 compositions; 99.9% of the dated rows have a matched entry whose critical temperature is within 0.01 K of their own, so the match finds the row's own entry, against 0.9% when the compositions are shuffled; and taking only entries whose temperature is above 0 K, or only the entries without the oxygen variant, changes the year of 2.7% and 0.9% of the rows. The 100 undated rows (63 cuprates, median critical temperature 22.1 K) leave the data, which also drops 99 compositions.
        - Split by the first report year (2026-11-11, Andrej, review issue 2, option a), in place of the grouped split on the composition: three expanding windows, the eras 1996-2001, 2002-2008 and 2009-2019, each trained on every entry first reported before the window. All entries of a composition carry the composition's first year, so a composition is never split; the identical feature rows a random split put on both sides stay on one side, and the composition stays whole for the score's weight too. The split costs much more than the composition split it replaces, which is the point: the window's families are new.

          Untuned LightGBM, the RMSE on a random half of each window's compositions, 3 seeds, each composition counted once (random forest within 0.6 K; Slurm job 1377613), against training on as many rows from all other years with no test composition (the earlier split) or no test element set:

          | Test window | Train rows | Test rows | Trained on earlier years | No test composition, all years | No test element set, all years | Test compositions whose element set is in training |
          |---|---|---|---|---|---|---|
          | 1996-2001 | 13,180 (62%) | 3,308 | 18.2 K | 14.2 K | 18.0 K | 51% by year, 86% by composition |
          | 2002-2008 | 16,488 (78%) | 2,166 | 14.9 K | 10.0 K | 14.6 K | 42% / 84% |
          | 2009-2019 | 18,654 (88%) | 2,509 | 12.6 K | 8.6 K | 11.6 K | 23% / 79% |

          What the older split bought was other dopings of the test composition's own element set (79-86% of the test compositions had one; the split by year leaves 23-51%). Holding out the iron-based family of every year is harder still (20.1 K on the iron-based compositions after 2008, against 12.8 K by year). Grouping by the element set instead of the year was weighed and declined (review issue 2, option e): it is about as hard (18.0, 14.6 and 11.6 K above), but it never tests another doping of a known system, the case a screen meets most often.
        - `first_year` is the time column and therefore one of the model's inputs. It is no help inside a test window: every value there lies after the newest training year, so it tells a model only that the row is new. The 81 features are unchanged, computed from the formula alone.
    """

    # Task
    target = "critical_temp"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmse",
        reason=(
            "Original: the out-of-sample RMSE of Hamidieh 2018 (Computational Materials Science 154:346-354, "
            "doi:10.1016/j.commatsci.2018.07.052; about 9.5 K for XGBoost, R2 about 0.92 alongside), which counts "
            "each SuperCon entry. Overruled on the unit (Lennart, 2026-11-08): every input is fixed by the "
            "composition and the materials scientist decides per composition, so the RMSE of the critical "
            "temperature in K weights an entry by 1 over its composition's number of entries "
            "(`composition_weight`) and each composition counts once, as Stanev et al. (2018) count each material "
            "once. Unweighted, YBa2Cu3O7 (110 entries) would count 110 times a composition measured once."
        ),
        inputs={"weight": "composition_weight"},
    )
    scoring_columns = (
        ScoringColumn(
            column="composition_weight",
            role="weight",
            used_by="rmse",
            description=(
                "1 over the number of SuperCon entries of the row's composition (from 1/110 to 1), so that each "
                "composition counts once in the RMSE; for scoring only, never a feature or a training weight"
            ),
        ),
    )
    unit_weight = UnitWeight(column="composition_weight", unit="composition")

    # Splits
    temporal = Temporal(on="first_year", horizon=7, horizon_unit="years")
    splits_comment = """
        Expanding windows by `first_year`, the year the composition was first reported in the literature (the parent database's datasheet; the UCI release has no year). The three test windows are the eras of the catalogue: 2009-2019 (split 0), 2002-2008 and 1996-2001, each trained on every entry first reported before its window (18,654, 16,488 and 13,180 of the 21,163 rows, 88%, 78% and 62%). The windows are 6, 7 and 11 calendar years long, and the horizon is declared as the middle one; the newest window holds the reports of 2009 to 2016 and one of 2019. Every entry of a composition carries that composition's first year, so a composition stays on one side of the split, and so do the identical feature rows its repeated entries make; the composition is also the unit the score counts once, which the windows therefore keep whole. A test window stands for the materials reported in the years after the model was trained: compositions of families the training data may lack (the iron-based superconductors after 2008), not only other doping levels of known ones.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(f"{raw_dir}/train.csv")
        elements = pd.read_csv(f"{raw_dir}/unique_m.csv")
        if len(elements) != len(df) or not elements["critical_temp"].equals(df["critical_temp"]):
            msg = "unique_m.csv is no longer row-aligned with train.csv"
            raise ValueError(msg)
        composition = composition_labels(elements)
        df["composition"] = composition
        df["first_year"] = composition.map(first_report_year(elements, composition, Path(raw_dir) / MDR_FILE))
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # The entries the datasheet does not date leave: there is no window to put them in (curation_comments).
        df = raw[raw["first_year"].notna()].reset_index(drop=True)
        assert df.groupby("composition")["first_year"].nunique().max() == 1, "a composition has two first years"
        df["first_year"] = df["first_year"].astype(int)
        # Each composition counts once in the score: 1 over its number of entries among the rows that ship. The
        # composition key stays in the frame as the unit of that weight, metadata and never a model input.
        df["composition_weight"] = 1.0 / df.groupby("composition")["composition"].transform("size")
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(categorical=["composition"])

    def _make_splits(self, df: pd.DataFrame) -> Splits | SplitPlan:
        """Expanding windows by first report year, newest first; the windows are eras, so their lengths differ."""
        year = df["first_year"].to_numpy()
        splits: Splits = {}
        for i, (start, end) in enumerate(reversed(WINDOWS)):
            train = np.flatnonzero(year < start).tolist()
            test = np.flatnonzero((year >= start) & (year < end)).tolist()
            splits[i] = {0: (train, test)}
        return splits

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        dated = raw["first_year"].notna()
        composition = raw["composition"]
        windows = {}
        for start, end in WINDOWS:
            rows = (raw["first_year"] >= start) & (raw["first_year"] < end)
            name = f"window {start}-{end - 1}"
            windows[f"{name}: train rows"] = int((df["first_year"] < start).sum())
            windows[f"{name}: test rows"] = int(rows.sum())
            windows[f"{name}: test compositions"] = int(composition[rows].nunique())
        per_composition = raw.groupby(composition, observed=True)["critical_temp"].agg(["count", "std", "min", "max"])
        repeated = per_composition[per_composition["count"] > 1]
        spread = repeated["max"] - repeated["min"]
        entries = pd.Series(
            {
                "rows": len(raw),
                "compositions": len(per_composition),
                "compositions with more than one entry": len(repeated),
                "rows of those compositions": int(repeated["count"].sum()),
                "median std of their critical temperature (K)": round(float(repeated["std"].median()), 2),
                "of those, max - min above 10 K": int((spread > 10).sum()),
                "of those, max - min above 30 K": int((spread > 30).sum()),
                "smallest weight of an entry in the score": round(float(df["composition_weight"].min()), 5),
            },
            name="value",
        )
        dating = pd.Series(
            {
                "rows": len(raw),
                "rows dated by the datasheet": int(dated.sum()),
                "undated rows dropped": int((~dated).sum()),
                "compositions": int(composition.nunique()),
                "compositions dated": int(composition[dated].nunique()),
                "first year, earliest": int(df["first_year"].min()),
                "first year, latest": int(df["first_year"].max()),
                **windows,
            },
            name="value",
        )
        return [
            Decision(
                "Split by the year the composition was first reported",
                "The catalogue grew in waves of families, so a screen meets materials of families the training data "
                "lacks. The MDR SuperCon datasheet dates 99.5% of the rows; the undated ones leave. The windows are "
                "the eras 1996-2001, 2002-2008 and 2009-2019, each trained on every earlier entry.",
                dating,
            ),
            Decision(
                "Every SuperCon entry kept, each composition counted once in the score",
                "The entries of one composition are identical feature rows with their own measured temperature. They "
                "all carry the composition's first year, so they stay on one side of the split; none is dropped or "
                "averaged, and the RMSE weights each by 1 over its composition's entries.",
                entries,
            ),
        ]
