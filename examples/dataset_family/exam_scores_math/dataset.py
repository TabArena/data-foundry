"""A child of `exam_scores`: the math score of a student at a school the model has not seen (grouped by school)."""

from __future__ import annotations

from data_foundry.v2 import Grouping, Metric, TaskSummary, import_definition

ExamScores = import_definition("exam_scores")


class ExamScoresMath(ExamScores):
    unique_name = "exam_scores_math"
    derivation = """
        The math score as the target, with whole schools held out; the reading score, written at the same exam, is
        dropped.
    """
    task_summary = TaskSummary(
        question="What math score will this student reach at the end of the year?",
        use_case=(
            "A school that joins a support programme flags, during the year, the students likely to score low in "
            "math, from a model trained on other schools."
        ),
        row="One student.",
        predicted="The end-of-year math score, from 0 to 100.",
        known="The student's school, study time, attendance, parents' education and last year's grade.",
        split="Whole schools: the test data stands for schools the model has not seen.",
        fit="approximate",
        fit_reason="Generated scores stand in for real students.",
    )

    target = "math_score"
    problem_type = "regression"
    metric = Metric.fallback(reason="Generated example data: there is no source metric.")
    grouping = Grouping(
        on="school",
        labels="per_sample",
        definition="""
            One group is one school. Whole schools are held out, as the model is meant for schools whose students it
            has not seen.
        """,
    )
