"""Tests for the hidden-group probe (``curation_probes.hidden_groups``) and its command-line wrapper."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("lightgbm")

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".claude" / "skills" / "knowledge-data-foundry" / "scripts"


@pytest.fixture(scope="module")
def cli():
    """hidden_groups.py, imported as a module (it puts the probe library on the path)."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("hidden_groups_cli", SCRIPTS / "hidden_groups.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def probe(cli):
    """curation_probes.hidden_groups."""
    return cli.hidden


def test_float_column_with_few_values_is_a_candidate(probe):
    """A float column whose values repeat is a candidate, whole numbers or not."""
    rng = np.random.default_rng(0)
    per_run = rng.normal(size=50).round(6)  # one computed value per run, not whole numbers
    assert probe.is_candidate(pd.Series(np.repeat(per_run, 4)))
    assert probe.is_candidate(pd.Series(np.repeat(np.arange(50.0), 4)))  # whole numbers, as before
    assert not probe.is_candidate(pd.Series(rng.normal(size=200)))  # every value once
    assert not probe.is_candidate(pd.Series(np.repeat(per_run, 4)).astype(bool))


def test_float_entity_column_reaches_the_scored_candidates(probe):
    """A per-run float value (a boundary-layer thickness) is scored as an entity column."""
    rng = np.random.default_rng(1)
    runs, per_run = 60, 5
    thickness = rng.uniform(0.001, 0.05, size=runs)
    effect = rng.normal(size=runs)
    frame = pd.DataFrame(
        {
            "thickness": np.repeat(thickness, per_run),
            "frequency": np.tile(np.arange(per_run) * 1000.0, runs),
            "noise": rng.normal(size=runs * per_run),
        }
    )
    frame["y"] = np.repeat(effect, per_run) + 0.1 * rng.normal(size=len(frame))
    result = probe.run(frame, "y", "regression", n_jobs=1)
    scored = {c["column"]: c for c in result["scored"]}
    assert "thickness" in scored
    assert scored["thickness"]["dtype"] == "float64"
    assert scored["thickness"]["s_id"] > 0.8


def test_near_copies_not_run_on_a_narrow_table(probe, cli):
    """No row reaches the token floor: the near-copy check reports not run, not 0%."""
    rng = np.random.default_rng(2)
    frame = pd.DataFrame({"a": rng.normal(size=300), "b": rng.integers(0, 5, size=300), "y": rng.integers(0, 2, 300)})
    result = probe.run(frame, "y", "binary", n_jobs=1)
    copies = result["near_copies"]
    assert copies["run"] is False
    assert math.isnan(copies["repeated_share"])
    assert math.isnan(copies["s_id"])
    assert not copies["eligible"]
    assert not copies["testable"]
    assert copies["ladder"] == []
    assert "(near copies): not run" in cli.render(result | {"name": "narrow", "regime": "iid"})
    assert "(near copies) not run" in cli._summary_row(result | {"name": "narrow", "regime": "iid"})


def test_near_copies_run_on_a_wide_table(probe):
    """A wide table with every row twice: the check runs and finds the copies."""
    rng = np.random.default_rng(3)
    base = rng.integers(0, 4, size=(100, 20))
    rows = np.vstack([base, base])  # every row twice
    frame = pd.DataFrame(rows, columns=[f"c{i}" for i in range(20)])
    frame["y"] = np.tile(rng.integers(0, 2, 100), 2)
    copies = probe.run(frame, "y", "binary", n_jobs=1)["near_copies"]
    assert copies["run"] is True
    assert copies["repeated_share"] == 1.0


def test_text_columns_and_normalisation(probe):
    """Only prose columns get a text key; case, punctuation and spacing do not count."""
    frame = pd.DataFrame(
        {
            "description": ["A bright flat with two rooms", "Old car, runs well, one owner", None, "big garden"],
            "code": ["AB12", "CD34", "EF56", "GH78"],
            "number": [1, 2, 3, 4],
        }
    )
    assert probe.text_columns(frame, list(frame.columns)) == ["description"]
    texts = pd.Series(["Great flat, 2 rooms!", "great   flat 2 rooms", "GREAT FLAT \u2013 2 ROOMS", "", None, "other"])
    normal = probe.normalise_text(texts)
    assert normal.iloc[0] == normal.iloc[1] == normal.iloc[2] == "great flat 2 rooms"
    assert normal.iloc[3:5].isna().all()


def _ads(rng: np.random.Generator, n: int = 600) -> pd.DataFrame:
    """Ads with a text and four numeric columns; 100 of them posted again with other capitals and punctuation, and
    50 rows with one boilerplate text.
    """
    words = np.array(
        ["flat", "house", "car", "bike", "sofa", "table", "lamp", "phone", "garden", "kitchen", "new", "old", "cheap"]
    )
    texts = [" ".join(rng.choice(words, 8)) + f" {i}" for i in range(n)]
    label = rng.integers(0, 2, n)
    reposts = rng.choice(n - 50, 100, replace=False)
    for i in range(n - 50, n):
        texts[i] = "Contact us for details"
    frame = pd.DataFrame({"text": texts, "y": label})
    for k in range(4):
        frame[f"x{k}"] = rng.normal(size=n)
    again = frame.iloc[reposts].copy()
    again["text"] = again["text"].str.upper() + "!!"
    return pd.concat([frame, again], ignore_index=True)


def test_text_key_finds_edited_reposts(probe, cli, monkeypatch):
    """Reposts with other capitals and punctuation share a text key; boilerplate is left single."""
    monkeypatch.setattr(probe, "COPY_MAX_CLUSTER", 40)  # the 50 boilerplate rows count as a large key
    frame = _ads(np.random.default_rng(4))
    result = probe.run(frame, "y", "binary", n_jobs=1)
    (key,) = result["text_keys"]
    assert key["column"] == "(text: text)"
    assert key["source_column"] == "text"
    assert key["repeated_share"] == pytest.approx(200 / len(frame), abs=1e-3)
    assert key["rows_in_large_keys"] == 50
    assert key["cluster_sizes"]["2"] == 100
    assert key["s_id"] == pytest.approx(1.0)  # a repost keeps its label
    assert key["eligible"]
    assert key["testable"]
    assert "gap" in key
    named = result | {"name": "ads", "regime": "iid"}
    assert "(text: text): 600 texts" in cli.render(named)
    assert "(text: text) gap" in cli._summary_row(named)


def test_text_key_recurrence_on_a_temporal_task(probe):
    """On a temporal task the text key reports the test rows whose text is on the training side."""
    frame = _ads(np.random.default_rng(5))
    frame["day"] = np.arange(len(frame))
    reposts = np.arange(len(frame) - 100, len(frame))
    train = np.setdiff1d(np.arange(len(frame)), reposts)
    result = probe.run(frame, "y", "binary", time_on="day", splits=[(train, reposts)], n_jobs=1)
    (key,) = result["text_keys"]
    assert key["test_rows_seen"] == 1.0  # every repost's text is on the training side
    assert "gap" not in key
    assert not result["hits"]


def test_a_column_with_few_repeated_values_is_no_candidate(probe):
    """A sparse spectrum bin: one repeated value (0) and the rest unique is no candidate (it has no groups to hold
    out).
    """
    rng = np.random.default_rng(6)
    values = np.r_[np.zeros(280), rng.normal(size=300)]
    assert not probe.is_candidate(pd.Series(values))


def test_a_column_of_repeated_texts_gets_no_text_key(probe):
    """A string column that is a candidate of its own (a school name) is left to the column check."""
    schools = [f"Lincoln Elementary School {i}" for i in range(30)]
    frame = pd.DataFrame({"school": np.repeat(schools, 4), "notes": [f"note number {i} here" for i in range(120)]})
    assert probe.text_columns(frame, ["school", "notes"]) == ["notes"]
