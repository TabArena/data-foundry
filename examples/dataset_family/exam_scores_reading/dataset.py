"""A child of `exam_scores`: the reading score of students at the known schools (IID)."""

from __future__ import annotations

from data_foundry.v2 import Metric, TaskSummary, import_definition

ExamScores = import_definition("exam_scores")


class ExamScoresReading(ExamScores):
    unique_name = "exam_scores_reading"
    derivation = """
        The reading score as the target, on random students of the six schools (IID); the math score, written at the
        same exam, is dropped.
    """
    task_summary = TaskSummary(
        question="What reading score will this student reach at the end of the year?",
        use_case=(
            "A teacher flags, during the year, the students of their school likely to score low in reading, to plan "
            "extra lessons."
        ),
        row="One student.",
        predicted="The end-of-year reading score, from 0 to 100.",
        known="The student's school, study time, attendance, parents' education and last year's grade.",
        split="Random students of the same schools.",
        fit="approximate",
        fit_reason="Generated scores stand in for real students.",
    )

    target = "reading_score"
    problem_type = "regression"
    metric = Metric.fallback(reason="Generated example data: there is no source metric.")

    def _clean(self, raw):
        return super()._clean(raw).drop(columns=["math_score"])  # the other outcome
