"""Curated dataset definition for `sat11_hand_algo_runtime` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import arff
import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Grouping,
    Metric,
    ScoringColumn,
    Source,
    TaskSummary,
    TimeBasis,
    anonymize_ids,
)

# The problem family is the generator an instance comes from, read off its path
# (./SAT<yy>/<track>/<submitter>/<generator>/.../<file>.cnf). Some generators are split over several folders, by
# satisfiability or by a parameter; those folders are merged, so the 48 folders of the kept instances give 32 families.
FAMILY_MERGES = (
    (r"^SAT03/handmade/anton/(SAT|UNSAT)$", "SAT03/handmade/anton"),
    (r"^SAT11/crafted/kullmann/VanDerWaerden/", "SAT11/crafted/kullmann/VanDerWaerden"),
    (r"^SAT09/CRAFTED/rbsat/", "SAT09/CRAFTED/rbsat"),
    (r"^SAT05/crafted/jarvisalo05/", "SAT05/crafted/jarvisalo05"),
    (r"^SAT05/crafted/sorge05/QG", "SAT05/crafted/sorge05/QG"),
    (r"^SAT02/handmade/pehoushek/", "SAT02/handmade/pehoushek"),
    (r"^SAT09/CRAFTED/edgematching/", "SAT09/CRAFTED/edgematching"),
    (r"^SAT04/handmade/anton/l\dk\d$", "SAT04/handmade/anton/lksat"),
    (r"^SAT04/handmade/kexu/frb", "SAT04/handmade/kexu/frb"),
    (r"^SAT04/handmade/connamacher/", "SAT04/handmade/connamacher"),
)


def problem_family(instance_path: str) -> str:
    """The generator family of an instance: its folder, with the folders of one generator merged."""
    folder = "/".join(instance_path.split("/")[1:-1])
    for pattern, family in FAMILY_MERGES:
        if re.search(pattern, folder):
            return family
    return folder


class Sat11HandAlgoRuntime(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How long will each of ten SAT solvers take on a problem instance from a family not seen before?",
        use_case=(
            "Algorithm selection: given a new satisfiability problem, a portfolio predicts the runtime of each of its"
            " ten solvers and runs the one predicted fastest (ASlib, Bischl et al. 2016); here from a problem family"
            " not seen before, as the instances new at the 2011 competition were."
        ),
        row=(
            "One run of one of 10 SAT solvers on one handcrafted instance of the 2011 SAT competition, stopped at "
            "5,000 seconds (184 instances, 1,840 runs)."
        ),
        predicted=(
            "The run's time in seconds, on a log scale; a run stopped at the 5,000-second limit counts as 5,000 (666 "
            "runs)."
        ),
        known=(
            "Statistics of the instance's formula (size, clause and variable structure, graph measures, results of "
            "short probing runs) and of the solver's source code (size, complexity, code-graph measures); not the "
            "solver's name."
        ),
        split=(
            "Whole problem families (the instances of one generator, 32 families) are held out with all their runs, so"
            " the test data stands for a kind of problem not seen in training, as at a later competition."
        ),
        changes=(
            "We drop the 112 of 296 instances on which every solver hits the limit: their labels are only lower "
            "bounds and leave the choice open. One model covers all solvers, with the solver described by its "
            "features. We hold out whole problem families where ASlib splits the instances at random."
        ),
        fit="direct",
        fit_reason=(
            "The features are known before any solver runs, and a held-out family is a new kind of problem, as every"
            " instance new in 2011 was. Counting a timeout as the limit keeps the order of the solvers within an"
            " instance, which is what the selection needs."
        ),
    )

    # Dataset
    unique_name = "sat11_hand_algo_runtime"
    domain = "technology & internet"
    sources = (
        Source(
            role="publication",
            platform="ASlib",
            url="https://github.com/coseal/aslib_data/tree/master/SAT11-HAND-ALGO",
            license="GPLv3",
            year="2011",
            bibtex="""
                @inproceedings{xu-sat12a,
                  author    = {L. Xu and F. Hutter and H. Hoos and K. Leyton-Brown},
                  title     = {Evaluating Component Solver Contributions to Portfolio-Based Algorithm Selectors},
                  pages     = {228-241},
                  crossref  = {sat12}
                }
                @Proceedings{sat12,
                  editor =         {A. Cimatti and R. Sebastiani},
                  title =         {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
                  booktitle = {Proceedings of the Fifteenth International Conference on Theory and Applications of Satisfiability Testing (SAT'12)},
                  publisher =         springer,
                  series =         lncs,
                  volume =         7317,
                  year =         2012
                }
                @article{bischl_aslib_2016,
                	title = {{ASlib}: {A} {Benchmark} {Library} for {Algorithm} {Selection}},
                	number = {237},
                	journal = {Artificial Intelligence Journal (AIJ)},
                	author = {Bischl, Bernd and Kerschke, Pascal and Kotthoff, Lars and Lindauer, Marius and Malitsky, Yuri and Fréchette, Alexandre and Hoos, Holger H. and Hutter, Frank and Leyton-Brown, Kevin and Tierney, Kevin and Vanschoren, Joaquin},
                	year = {2016},
                	pages = {41--58}
                }
            """,
        ),
    )
    download_description = """
        wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/SAT11-HAND-ALGO/feature_values.arff && wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/SAT11-HAND-ALGO/algorithm_feature_values.arff && wget https://raw.githubusercontent.com/coseal/aslib_data/refs/heads/master/SAT11-HAND-ALGO/algorithm_runs.arff && mkdir -p local-data-warehouse/sat11_hand_algo_runtime && mv feature_values.arff algorithm_feature_values.arff algorithm_runs.arff local-data-warehouse/sat11_hand_algo_runtime/
    """
    curation_comments = """
        We get the data from ASlib and merge them into one file.

        - Algorithm selection can be solved with many methods (pairwise classification, hierarchical regression, multi-label, ...). We follow the concept from Pulatov et al. (https://proceedings.mlr.press/v188/pulatov22a.html) and learn one single, unified regression model that goes from (instance_features, algorithm_features) -> runtime.
        - The description says 'If features are "?", the instance was solved during feature computation.' but from the status file we can see that no task was presovled. So it is unclear what this is referring to. We believe that in all cases we have nan values for features, it is a case of the feature running into a memout, timeout, or crash as stated by the description.
        - The runtimes are right-censored: every run was stopped at the cutoff of 5,000 s, and a timeout is stored as a runtime of 5,000 s (the slowest finished run took 4,996 s, so `runtime == log(5000)` marks a timeout). A regression model and RMSE take that cutoff as the exact runtime, which biases predictions down (Hutter et al. 2014, section 9). We drop the 112 of 296 instances on which all 10 algorithms time out (1,120 rows): their labels are only lower bounds, and they cannot change which algorithm is selected (every choice costs the same; the single-best to virtual-best PAR10 gap is the same with or without them). We keep the 666 timeouts of the other 184 instances at the cutoff: selecting the fastest algorithm needs every algorithm's outcome, and the cutoff keeps the order within an instance (every finished run is faster) and is enough to compute PAR10.
        - A survival task type (a censoring indicator, a censoring-aware loss and metric) could use every run, including the 112 dropped instances, as survival-based algorithm selectors do (for example Run2Survive, Tornede et al. 2020). The raw files keep them; TabArena has no such task type yet.
        - Timeouts stay at the recorded 5,000 s in the target (Andrej, 2026-11-06): it is the value ASlib records, and how to
          treat a censored run is part of what a model has to work out; the scoring, ASlib's PAR10, charges a timeout ten
          times the limit. Counting timeouts at that charge (50,000 s) in the target made LightGBM, a random forest,
          linear models and TabPFN pick 17-19% better on the 60 splits, but it would replace the recorded value.
        - We log scale the target.
        - We drop duplicated columns and remove features that leak the target or are not relevant for the predictive task.
        - Split (Andrej, 2026-11-18): whole problem families are held out. A family is the
          generator an instance comes from, read off its path before the id is hashed (`problem_family`); folders that
          split one generator by satisfiability or a parameter are merged (Anton's 2003 SAT/UNSAT, rbsat's four
          forced/unforced folders, QG6/7/7a/8, two Van der Waerden folders and six more), so the 48 folders give 32
          families, 11 of them a single instance, the largest 21. Generators of a shared problem stay apart (model RB in
          2004 and 2009, subgraph isomorphism in 2003 and 2011). The use case decides: in this data a portfolio built on
          the instances of 2002-2009 meets 88 new instances in 2011 from 7 generators no earlier competition used, so
          a new member of a family it already has does not occur; holding out single instances (ASlib's random folds,
          and this definition until 2026-11-18) put 91% of the test instances' families in training. The anonymised
          instance ships as a scoring column only (`instance_id`): PAR10 picks per instance the solver with the lowest
          predicted runtime. Never a feature.
    """
    split_leaf = "L-EXP.kind"
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        whole problem families held out. Every solver ran on every instance in one campaign
        of the 2011 SAT competition with a 5,000 s cutoff; the features exist before any full run, and no run is
        dated. The competition that first used an instance gives one window with half of the rows in training (2011,
        52%; 2009 trains on 38%), so no split by competition (SPLIT-14). Not tested: newer solvers.
        """,
    )

    # Task
    target = "runtime"
    problem_type = "regression"
    metric = Metric.source(
        "par_k",
        original=(
            "PAR10 (penalized average runtime, factor 10) of the selected algorithm; also reported as the "
            "fraction of the single-best to virtual-best gap closed"
        ),
        reference=(
            "Bischl et al. 2016, ASlib: A benchmark library for algorithm selection, Artificial Intelligence "
            "237:41-58; Pulatov et al. 2022 (PMLR v188)"
        ),
        definition=(
            "per instance select the algorithm with the lowest predicted runtime; its true runtime in seconds"
            " (exp of the log target), a timeout (runtime >= 5,000 x (1 - 1e-4)) counted as 50,000 s; mean "
            "over instances"
        ),
        params={"cutoff": 5000, "k": 10, "timeout_rel_tol": 0.0001},
        inputs={"group": "instance_id"},
        target_transform="log",
    )
    scoring_columns = (
        ScoringColumn(
            column="instance_id",
            role="group",
            used_by="par_k",
            description=(
                "the anonymised instance (10 rows each, one per solver); the metric picks per instance the solver with "
                "the lowest predicted runtime and averages the picks' true runtimes."
            ),
        ),
    )
    grouping = Grouping(
        on="problem_family",
        labels="per_sample",
        prediction_unit="row",
        context="all_rows",
        definition="""
            One group is a problem family: the instances of one generator (32 families with 1 to 21 instances), each instance with the runs of the 10 candidate algorithms on it, described by instance and algorithm features, with the log runtime as the target. The use case is algorithm selection: predict every algorithm's runtime on a new instance and run the one predicted fastest (ASlib, Bischl et al. 2016; one model for all algorithms as in Pulatov et al. 2022), scored per instance by the selected algorithm's true runtime (PAR10, or the share of the gap between the single best and the virtual best solver that is closed) through the instance id, a scoring column. ASlib's folds hold out instances at random; holding out whole families is our choice (Andrej, 2026-11-18): the instances new at the 2011 competition all came from generators no earlier competition used.
        """,
    )
    accepted_check_warnings = {
        "groups_test_groups_few": (
            "Accepted (Andrej, 2026-11-23): a group is a problem family, the instances of one generator, and the use "
            "case is a family not seen in training (the 88 instances new in 2011 all came from new generators), so "
            "the 32 families give 10 or 11 per test fold. The signal across families is real: on 3 x 3 family folds "
            "(group_probes.py, R^2 on the log runtime) random forest reaches 0.345, LightGBM 0.291 and kNN 0.242 "
            "against a baseline of 0. The spread is wide (LightGBM 0.041 +- 0.269 per fold, against 0.875 +- 0.031 on "
            "instance folds), which the 20 x 3 splits average over; repeats reuse the same families, so the spread "
            "across repeats is descriptive, not 60 independent experiments."
        ),
    }

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        def load_arff(path) -> pd.DataFrame:
            with open(path, encoding="utf-8") as f:
                data = arff.load(f)
            df = pd.DataFrame(data["data"], columns=[a[0] for a in data["attributes"]])
            return df

        df_features = load_arff(raw_dir / "feature_values.arff")
        df_algo_features = load_arff(raw_dir / "algorithm_feature_values.arff")
        df_algo_runs = load_arff(raw_dir / "algorithm_runs.arff")
        return {"df_features": df_features, "df_algo_features": df_algo_features, "df_algo_runs": df_algo_runs}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df_features, df_algo_features, df_algo_runs = raw["df_features"], raw["df_algo_features"], raw["df_algo_runs"]
        # Drop algorithms that for which we do not have features
        df_algo_runs = df_algo_runs[df_algo_runs["algorithm"].isin(df_algo_features["algorithm"].unique())]
        # Drop instances that no algorithm solves: all their runtimes are the censored cutoff
        solved = df_algo_runs.loc[df_algo_runs["runstatus"] == "ok", "instance_id"].unique()
        df_algo_runs = df_algo_runs[df_algo_runs["instance_id"].isin(solved)]
        # Merge
        df = df_algo_runs.merge(df_features, on="instance_id", how="left").merge(
            df_algo_features, on="algorithm", how="left"
        )
        # The problem family, read off the instance path before the path is hashed (the split's group)
        df["problem_family"] = anonymize_ids(df["instance_id"].map(problem_family))
        # stable anonymous ids (random uuid4 ids changed the data on every run)
        df["instance_id"] = anonymize_ids(df["instance_id"])
        # Drop features
        df = df.drop(
            columns=[
                # Data has no repetitions
                "repetition_x",
                "repetition_y",
                "repetition",
                # We want to only rely on algorithm meta features not names.
                "algorithm",
                # Leaks target
                "runstatus",
                # Duplicated columns
                "clustering_min",
                "edge_ta",
                "edge_to",
                "edge_tl",
                "edge_da",
                "edge_do",
                "edge_dl",
                "edge_as",
                "edge_aa",
                "edge_ao",
                "edge_al",
                "edge_ot",
                "edge_oa",
                "edge_ol",
                "edge_lt",
                "edge_la",
                "edge_ll",
                "degree_min",
                "path_min",
                "VCG_VAR_mean",
                "edge_at",
            ]
        )
        df["runtime"] = np.log(df["runtime"])
        return df

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "problem_family",  # the split's group, never a feature
                "instance_id",  # scoring column only, never a feature
            ],
        )
