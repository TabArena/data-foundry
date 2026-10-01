"""Curated dataset definition for `video_transcoding_time_prediction` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import AbstractCuratedDataset, FeatureTypes, Grouping


class VideoTranscodingTimePrediction(AbstractCuratedDataset):
    # Dataset
    unique_name = "video_transcoding_time_prediction"
    year = "2015"
    domain = "technology & internet"
    source = "UCI"
    source_url = "https://doi.org/10.24432/C58C9K"
    license = "CC BY 4.0"
    download_description = """
        wget https://archive.ics.uci.edu/static/public/335/online+video+characteristics+and+transcoding+time+dataset.zip && unzip online+video+characteristics+and+transcoding+time+dataset.zip transcoding_mesurment.tsv && rm online+video+characteristics+and+transcoding+time+dataset.zip && mkdir -p local-data-warehouse/video_transcoding_time_prediction && mv transcoding_mesurment.tsv local-data-warehouse/video_transcoding_time_prediction/
    """
    bibtex = """
        @inproceedings{deneke2014video,
          title={Video transcoding time prediction for proactive load balancing},
          author={Deneke, Tewodors and Haile, Habtegebreil and Lafond, S{'e}bastien and Lilius, Johan},
          booktitle={2014 IEEE International Conference on Multimedia and Expo (ICME)},
          pages={1--6},
          year={2014},
          organization={IEEE}
        }
    """
    curation_comments = """
        We use the tabular prediction task from the UCI archive, which is a video transcoding time prediction task. The data is non-IID and grouped by video, with multiple transcoding measurements per video. The target variable is the transcoding time, and the features include various characteristics of the videos and transcoding settings.

        - Some features on the videos (like URL and category) are not part of this dataset as we got it from UCI, but this sounds like a good idea for the task.
        - The data includes several transcoding per video (also with different output target formats), which creates a non-IID setting. We will use the video id as the group label, and we will make sure to split the data such that all transcoding measurements for a given video are in the same split (train/test).
        - We log scale the target variable.
    """

    # Task
    target = "log_transcoding_time"
    problem_type = "regression"
    grouping = Grouping(
        on="video_id",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a video; its rows are transcoding jobs of that video to an output setting (80 videos with the full grid of 841 settings, the rest mostly single jobs). The use case is predicting the transcoding time of new videos to balance requests across a transcoding cluster ("unseen video streams", Deneke et al. 2014), so each job is one prediction, made from its own row.
        """,
    )

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        df = pd.read_csv(raw_dir / "transcoding_mesurment.tsv", sep="\t")
        return df

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw
        df = df.drop(
            columns=[
                # Target colum / leaking
                "umem",
                # Constant
                "b_size",
            ]
        )
        df = df.rename(
            columns={
                "utime": "log_transcoding_time",
                "id": "video_id",
            }
        )
        df["log_transcoding_time"] = np.log(df["log_transcoding_time"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "video_id",
                "codec",
                "o_codec",
            ],
        )
