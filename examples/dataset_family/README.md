# A family of dataset definitions

Some data supports more than one task. A table of students' exam results can predict the math score or the reading
score; it can be split by random students or by whole schools; a later variant may filter rows or derive new columns.
Each of these is its own dataset with its own container (one task per container), but they all read the same files
and clean them the same way. Instead of copying that code into every `dataset.py`, the tasks form a **family**: one
parent holds what they share, and each task is a small subclass of it.

## The idea

**The parent** is a definition without a `target`. It says where the data comes from (`sources`,
`download_description`), reads and cleans the raw files once (`_load_raw`, `_clean`, `_feature_types`), and
describes the data independent of any task (`data_summary = DataSummary(...)`). It keeps every outcome in its frame
and declares which columns are never features (`non_features`): the outcomes, and where each row comes from. A parent
is never built; `dataset check` checks it as data: its frame, a checksum of it, its columns, its raw files and its
children.

**A child** is a task. It subclasses the parent, which it imports from the folder next to it:

```python
ExamScores = import_definition("exam_scores")


class ExamScoresMath(ExamScores):
    unique_name = "exam_scores_math"            # <parent>_<variant>
    derivation = "The math score as the target, with whole schools held out; the reading score is dropped."
    task_summary = TaskSummary(...)
    target = "math_score"
    problem_type = "regression"
    metric = Metric.fallback(reason=...)
    grouping = Grouping(on="school", ...)
```

It inherits everything it does not declare: the metadata, the raw files, the cleaning, the column types, the data
summary and the non-features. It drops every declared non-feature it does not use: the reading score (an outcome it
does not predict) and the provenance columns; the math score stays as its target. It may override any hook and call
`super()`. Its container records where it comes from
(`dataset_metadata.derived_from` and `derivation`), so a benchmark can tell which tasks share their data.

## This example

| File | What it is |
|---|---|
| [`exam_scores/dataset.py`](exam_scores/dataset.py) | The parent: one CSV per school, stacked with `read_files` (which records each row's file, row number and id), the school taken from the file name. Declares both scores as outcomes and the provenance columns as `non_features`; its source names the files, which the containers list with their hashes (`raw_files`). |
| [`exam_scores_math/dataset.py`](exam_scores_math/dataset.py) | A task: the math score of students at a school the model has not seen (grouped by school). The reading score and the provenance columns are dropped. |
| [`exam_scores_reading/dataset.py`](exam_scores_reading/dataset.py) | A task: the reading score of random students of the same schools (IID). The math score and the provenance columns are dropped. |
| [`run_family.py`](run_family.py) | Generates the raw files, checks the parent and both tasks, and tries a third task from a class written in the script. |

The data is generated (six schools, 40 students each), so the example needs no download. From the repository root:

```bash
python examples/dataset_family/run_family.py
```

It lists the family (the parent and its two tasks), prints the parent's frame, its never-features, data checksum and
raw files, then each task's target, split, columns, the columns it dropped, and the parent and raw files its
container names. Nothing is built and no file in the repository is
written.

## The rules in short

* A child is named `<parent>_<variant>` after what differs (`_math`, `_grouped`, `_clf`) and declares a
  `derivation`; a row budget's suffix comes last (`<parent>_<variant>_1m`).
* Every member reads the raw files of the definition that says how to download them, the parent here. A child does
  not redeclare `download_description` or the step that prepares the raw files.
* An outcome measured with the target (here the other exam score) is not known when predicting. The parent declares
  it once in `non_features`, with the provenance columns, and every task drops what it does not use.
* A source that names its files (`Source(files=("*.csv",))`) gets them listed with their hashes in each container
  (`raw_files`); a changed file is reported on the next check.
* A child inherits the parent's `data_summary`, shown above its own `task_summary` in its README. It may not inherit
  a `task_summary` written for another target or split.
* To try a task before giving it a folder, write the class in a notebook or script (`class Try(ExamScores): ...`):
  `check()` runs, writes no README, and `build()` refuses it. `run_family.py` does this at the end.
* `dataset new <parent>_<variant> --parent <parent>` scaffolds a child, and `dataset list` shows each definition
  with its kind and parent.

The full reference is the "Families" section of
[`definitions.md`](../../.claude/skills/knowledge-data-foundry/references/definitions.md).
