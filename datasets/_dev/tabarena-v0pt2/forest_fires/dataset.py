"""Curated dataset definition for `forest_fires` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Metric, TaskSummary


class ForestFires(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How large an area will a forest fire burn?",
        use_case=(
            "When a fire breaks out in the Montesinho natural park, the fire service estimates from the weather how "
            "large it will grow, to decide where to send air tankers and ground crews (the paper's stated use)."
        ),
        row=("One forest fire in the Montesinho natural park in northeast Portugal, 2000-2003 (517 fires)."),
        predicted="The burned area in hectares; 48% of the fires burned 0 ha.",
        known=(
            "The fire's square on a grid map of the park, the month and weekday, four components of the Canadian fire"
            " weather index, and the temperature, humidity, wind and rain."
        ),
        split=("Random fires, so the test data stands for other fires of the same years; the year is not in the data."),
        fit="approximate",
        fit_reason=(
            "Fires from several years are split at random because the data holds only month and weekday, so a split "
            "by time is impossible. When the weather values were read relative to the fire is not stated. The signal "
            "is small."
        ),
    )

    # Dataset
    unique_name = "forest_fires"
    year = "2008"
    domain = "environmental science & climate"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C5D88D"
    license = "CC BY 4.0"
    data_tags = ("Spatial", "ForcedIIDFromTemporal")
    download_description = """
        We get the data from UCI.

        wget https://archive.ics.uci.edu/static/public/162/forest+fires.zip && unzip forest+fires.zip && rm forest+fires.zip forestfires.names
        mkdir -p local-data-warehouse/forest_fires && mv forestfires.csv local-data-warehouse/forest_fires/
    """
    bibtex = r"""
        @article{cortez2007data,
          title={A data mining approach to predict forest fires using meteorological data},
          author={Cortez, Paulo and Morais, An{\'\i}bal de Jesus Raimundo},
          year={2007},
          publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
        }
    """
    curation_comments = """
        We start with the data from UCI.

        - The original paper used a IID split. The tasks sounds like it requires a temporal split. However, the data does not contain the original time indices (or order of samples) and just month and weekday over four years (January 2000 to December 2003, Cortez and Morais 2007, Sec. 2). Furthermore, the authors made sure to only use time-invariant features as it seems they wanted to develop a time-invaraint model for deployment and analysis of the data. In other words, this task can be handled by IID splits. Furthermore, the task in the paper was about using algorithms also for feature selection (so scientific discovery).
        - We ship the burned area in hectares, as the authors scored it: they fit on log1p(area) and computed MAD and RMSE on the raw area after back-transforming the predictions (Cortez and Morais 2007, Sec. 3-4).
        - The data contains naturally occurring duplicates.
    """

    # Task
    target = "area"
    problem_type = "regression"
    metric = Metric.source(
        "mae",
        original="MAD (mean absolute deviation) of the burned area; RMSE also reported, models ranked by MAD",
        reference="Cortez & Morais 2007, A data mining approach to predict forest fires using meteorological data (EPIA 2007), Sec. 3-4; UCI forestfires.names",
        definition="mean absolute error of the burned area in hectares, on the raw scale",
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "forestfires.csv")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        return raw

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "month",
                "day",
            ],
        )
