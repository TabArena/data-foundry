"""The smallest benchmark adapter: load a container, fit on every fold, score by its metric.

``python examples/minimal_adapter.py [container folder]`` (default: the format-2 toy shipped with the package). The
task view does the protocol: the folds within the row budget, the inputs (``task.X`` leaves out a SMILES, which needs
an encoding), the training weight, the scorer and the error. A model that stops early or tunes on an inner validation
split takes it from ``task.validation_split(fold.train)``, which follows the regime. ``benchmark_container.py`` adds
the recommended encodings of dates, text and special features.
"""

from __future__ import annotations

import sys

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor

from data_foundry.curation_container import CuratedContainer
from data_foundry.examples import get_toy_container_path


def inputs(x: pd.DataFrame) -> pd.DataFrame:
    """An ordered category by its order, as a number; the other columns as they are."""
    ordinal = [c for c in x.columns if isinstance(x[c].dtype, pd.CategoricalDtype) and x[c].cat.ordered]
    return x.assign(**{c: x[c].cat.codes.where(x[c].notna()) for c in ordinal})


def main(path: str | None = None) -> list[float]:
    """Fit and score every fold of the container at ``path``; return the errors (lower is better, 0 at the best)."""
    task = CuratedContainer.load(path or get_toy_container_path(format_version=2)).task()
    model_class = HistGradientBoostingRegressor if task.classes is None else HistGradientBoostingClassifier
    errors = []
    for fold in task.folds():
        model = model_class(categorical_features="from_dtype", random_state=0)
        model.fit(inputs(task.X(fold.train)), task.y(fold.train), sample_weight=task.train_weight(fold.train))
        x_test = inputs(task.X(fold.test))
        if task.metric.prediction == "proba":  # columns named by class; a class the fold did not train on gets 0
            y_pred = pd.DataFrame(model.predict_proba(x_test), columns=model.classes_)
            y_pred = y_pred.reindex(columns=list(task.classes), fill_value=0.0)
        else:
            y_pred = model.predict(x_test)
        score = task.score(task.y(fold.test), y_pred, fold.test)
        errors.append(task.error(score))
        print(f"{task.name} r{fold.repeat}/f{fold.fold}: {task.metric.name}={score:.4f}, error {errors[-1]:.4f}")
    return errors


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
