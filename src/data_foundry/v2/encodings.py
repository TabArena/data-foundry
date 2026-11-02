"""Recommended encodings for the columns a tabular model cannot take as they are (Lennart, 2026-11-01).

Data Foundry ships such columns as they are, typed by what they hold: a date as ``datetime``, free text as
``string``, a molecule as a SMILES column (a definition's ``smiles_columns``, recorded in the container as a
:class:`~data_foundry.schema.SemanticColumn`). It does not encode them in the data. It recommends how to encode them,
so a benchmark can do it the same way for every method (and cache it), and so this repository's tests of a dataset
see what a model would see. A benchmark may use these encodings, take inspiration from them, or use its own.

========  ========================================  ==========================================================
kind      recommended (:func:`recommended_encodings`)  what it computes
========  ========================================  ==========================================================
smiles    ``rdkit2d-maccs-ecfp4`` (:func:`~data_foundry.v2.chemistry.encode_smiles`)  RDKit's 2D descriptors, the 166
          MACCS keys and the ECFP4 counts, per molecule
datetime  ``skrub-datetime`` (:func:`encode_datetime`)  skrub's ``DatetimeEncoder(add_weekday=True,
          periodic_encoding="circular")``, as BeyondArena and TabArena's ``tabarena_default`` pipeline
text      ``tfidf-svd`` (:func:`encode_text_tfidf`) and ``e5-small-v2`` (:func:`encode_text_e5`): check both
spectrum  by technique and state (:func:`~data_foundry.v2.spectra.spectrum_encoding`): a raw mass spectrum
          ``ms-sqrt-sg21-snip100-tic`` (MALDIquant's steps), any other ``spectrum-as-is``; a vibrational spectrum
          also ``vib-als-snv`` (RamanBench's linear-model default): check both
========  ========================================  ==========================================================

Text has two recommendations because neither wins everywhere: TF-IDF fitted on the training rows reads the words (or
the character n-grams of codes and identifiers) of this dataset, while a sentence embedding reads meaning a small
dataset cannot teach. Compare both on a dataset with text.

Each encoding has an :class:`Encoding` spec whose ``id`` names it, the library release that fixes its values when
there is one, and a revision: a cache of encoded values is keyed by it. The SMILES and e5 encodings give one row per
distinct value (cacheable by value); TF-IDF is fitted on the training rows of each split. The libraries are optional:
RDKit is in the ``build`` extra, skrub and sentence-transformers in the ``encodings`` extra.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(frozen=True)
class Encoding:
    """A fixed encoding of one kind of column into numeric columns, identified by :attr:`id`."""

    kind: str
    """The kind of column it encodes: ``smiles``, ``datetime``, ``text`` or ``spectrum`` (a group of columns)."""
    name: str
    """What it computes, e.g. ``rdkit2d-maccs-ecfp4``."""
    revision: int
    """Bumped for any change that alters the values or the columns."""
    description: str
    """The columns it makes, for the container and a benchmark's cache."""
    library: str | None = None
    """The library release that fixes its values (``rdkit2026.03.6``), when one is pinned."""

    @property
    def id(self) -> str:
        """The spec id, e.g. ``rdkit2d-maccs-ecfp4-rdkit2026.03.6-r1``: a cache of encoded values is keyed by it."""
        return "-".join(part for part in (self.name, self.library, f"r{self.revision}") if part)


DATETIME_ENCODING = Encoding(
    kind="datetime",
    name="skrub-datetime",
    revision=1,
    description=(
        "skrub's DatetimeEncoder(add_weekday=True, periodic_encoding='circular'), as BeyondArena and TabArena's "
        "tabarena_default pipeline: the year and the total seconds, and a circular (sine/cosine) pair for each "
        "periodic part down to the column's resolution (month, day, hour, ...) and for the weekday, named "
        "<column>_<part>_circular_0/1."
    ),
)
"""The recommended encoding of a ``datetime`` column."""

TEXT_COMPONENTS = 16
"""The SVD components :data:`TEXT_TFIDF_ENCODING` keeps per text column."""

ONE_TOKEN_SHARE = 0.9
"""A text column whose values are a single token in at least this share of rows is read by character n-grams."""

TEXT_TFIDF_ENCODING = Encoding(
    kind="text",
    name="tfidf-svd",
    revision=1,
    description=(
        f"TF-IDF fitted on the training rows (words; character 2- to 5-grams when at least {ONE_TOKEN_SHARE:.0%} of "
        f"the values are one token, as codes and identifiers are), reduced to {TEXT_COMPONENTS} components by "
        "truncated SVD: columns tfidf_0 to tfidf_15."
    ),
)
"""One of the two recommended encodings of a text column (``string``): fitted per split."""

E5_MODEL = "intfloat/e5-small-v2"
"""The sentence-transformer of :data:`TEXT_E5_ENCODING` (384 dimensions)."""

TEXT_E5_ENCODING = Encoding(
    kind="text",
    name="e5-small-v2",
    revision=1,
    description=(
        f"{E5_MODEL} sentence embeddings of each value with the 'query: ' prefix, L2-normalised: columns e5_0 to "
        "e5_383, one row per distinct value."
    ),
)
"""One of the two recommended encodings of a text column (``string``): per value, cacheable."""


def recommended_encodings() -> dict[str, tuple[Encoding, ...]]:
    """The recommended encodings by kind of column (``smiles``, ``datetime``, ``text``) or of spectrum
    (``mass_spectrum`` raw, ``processed_spectrum``: a processed mass spectrum or a peak list, ``vibrational_spectrum``:
    Raman, infrared, near-infrared). Text and vibrational spectra have two, check both; the first is the default.
    """
    from data_foundry.v2.chemistry import DEFAULT_SMILES_ENCODING  # noqa: PLC0415 - chemistry imports this module
    from data_foundry.v2.spectra import (  # noqa: PLC0415 - spectra imports this module
        AS_IS_ENCODING,
        MS_RAW_ENCODING,
        VIBRATIONAL_ALS_SNV_ENCODING,
    )

    return {
        "smiles": (DEFAULT_SMILES_ENCODING,),
        "datetime": (DATETIME_ENCODING,),
        "text": (TEXT_TFIDF_ENCODING, TEXT_E5_ENCODING),
        "mass_spectrum": (MS_RAW_ENCODING,),
        "processed_spectrum": (AS_IS_ENCODING,),
        "vibrational_spectrum": (AS_IS_ENCODING, VIBRATIONAL_ALS_SNV_ENCODING),
    }


def _optional(module: str, extra: str = "encodings"):
    """Import ``module``, or say which extra installs it."""
    import importlib  # noqa: PLC0415

    try:
        return importlib.import_module(module)
    except ImportError as exc:
        msg = f"This encoding needs `{module}`: install the `{extra}` extra (`pip install data-foundry[{extra}]`)."
        raise ImportError(msg) from exc


def encode_datetime(values: pd.Series, *, prefix: str | None = None) -> pd.DataFrame:
    """A ``datetime`` column in the recommended encoding (:data:`DATETIME_ENCODING`), on the index of ``values``.

    The columns are skrub's, named ``<column>_<part>``; ``prefix`` replaces the column name in them.
    """
    skrub = _optional("skrub")
    encoder = skrub.DatetimeEncoder(add_weekday=True, periodic_encoding="circular")
    name = values.name if values.name is not None else "datetime"
    out = encoder.fit_transform(values.rename(name))
    out.index = values.index
    if prefix is not None:
        out.columns = [f"{prefix}{c.removeprefix(f'{name}_')}" for c in out.columns]
    return out


def _text_vectorizer(values: pd.Series) -> object:
    """Word TF-IDF for prose; character 2- to 5-grams when most values are one token (codes, identifiers)."""
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415 - scikit-learn is in `build`

    sample = values.head(5_000).astype("string").fillna("")
    one_token = float((~sample.str.strip().str.contains(r"\s")).mean()) if len(sample) else 0.0
    if one_token >= ONE_TOKEN_SHARE:
        return TfidfVectorizer(
            analyzer="char", ngram_range=(2, 5), max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32
        )
    return TfidfVectorizer(max_features=20_000, min_df=2, sublinear_tf=True, dtype=np.float32)


def encode_text_tfidf(
    train: pd.Series, test: pd.Series, *, prefix: str = "tfidf_", components: int = TEXT_COMPONENTS
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """A text column in the TF-IDF encoding (:data:`TEXT_TFIDF_ENCODING`), fitted on ``train`` only.

    Returns the train and the test rows, each on its own index, with columns ``<prefix>0`` onwards (fewer than
    ``components`` when the vocabulary is smaller). Missing values are empty text.
    """
    from sklearn.decomposition import TruncatedSVD  # noqa: PLC0415 - scikit-learn is in `build`

    fit = train.astype("string").fillna("")
    vectorizer = _text_vectorizer(fit)
    matrix = vectorizer.fit_transform(fit.to_numpy())
    n = max(1, min(components, matrix.shape[1] - 1, matrix.shape[0] - 1))
    svd = TruncatedSVD(n_components=n, random_state=0)
    columns = [f"{prefix}{i}" for i in range(n)]
    out_train = pd.DataFrame(svd.fit_transform(matrix), index=train.index, columns=columns)
    test_matrix = vectorizer.transform(test.astype("string").fillna("").to_numpy())
    out_test = pd.DataFrame(svd.transform(test_matrix), index=test.index, columns=columns)
    return out_train, out_test


def encode_text_e5(
    values: pd.Series,
    *,
    prefix: str = "e5_",
    batch_size: int = 64,
    model_factory: Callable[[str], object] | None = None,
) -> pd.DataFrame:
    """A text column in the e5 encoding (:data:`TEXT_E5_ENCODING`): one row per value, each distinct value once.

    Missing values are empty text. ``model_factory`` builds the encoder from :data:`E5_MODEL` (default:
    ``sentence_transformers.SentenceTransformer``; tests pass a stub).
    """
    if model_factory is None:
        model_factory = _optional("sentence_transformers").SentenceTransformer
    text = values.astype("string").fillna("")
    unique = pd.Index(pd.unique(text), dtype="object")
    model = model_factory(E5_MODEL)
    vectors = np.asarray(
        model.encode([f"query: {v}" for v in unique], batch_size=batch_size, normalize_embeddings=True),
        dtype=np.float32,
    )
    table = pd.DataFrame(vectors, index=unique, columns=[f"{prefix}{i}" for i in range(vectors.shape[1])])
    out = table.reindex(text.to_numpy(dtype="object"))
    out.index = values.index
    return out
