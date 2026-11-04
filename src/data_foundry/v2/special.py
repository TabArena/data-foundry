"""Special features: model inputs that need handling beyond their dtype, declared like the target (2026-11-02).

A definition lists them in ``special_features``, next to ``target`` and ``scoring_columns``. Each entry is one special
feature, in one of two layouts:

* a :class:`SpecialColumn`: the feature is one column, e.g. ``Smiles(column="SMILES")``, a molecule's structure;
* a :class:`SpecialColumnGroup`: the feature is a group of columns that hold one object together, in a fixed order,
  and are encoded together, e.g. ``Spectrum(name="serum_ms", prefix="M/Z:", ...)``, one column per position on a
  spectrum's axis.

The build records each entry as a :class:`~data_foundry.schema.SpecialFeature` in the container's
``task_metadata.special_features``: its name, kind, layout, columns, whether its raw values are usable model inputs
(``encoding_required``), the recommended encoding and what the kind adds (a spectrum's axis, technique and state). A
benchmark reads that one list, whatever the kind (:func:`~data_foundry.curation_container.special_features`), and
encodes each feature with :func:`encode_special_feature`.

Each kind is one class here, registered in :func:`special_feature_kind`; it fixes the layout, the dtype the build
casts to, the bundle checks, the candidate encodings (the default first, :func:`encodings_for`) and how they are
computed. The kinds: ``smiles`` (:class:`data_foundry.v2.chemistry.Smiles`) and ``spectrum``
(:class:`data_foundry.v2.spectra.Spectrum`). A new kind (a shipped embedding, a sequence) is a subclass of one of the
two layouts plus its name in :data:`~data_foundry.schema.SpecialFeatureKind`; no definition attribute, container field
or consumer changes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

import pandas as pd

from data_foundry.schema import SpecialFeature, SpectrumDetails

if TYPE_CHECKING:
    from data_foundry.bundle_checks import CheckResult
    from data_foundry.v2.encodings import Encoding


class SpecialFeatureError(TypeError):
    """A special feature's declaration does not fit the frame (re-raised by the build as a definition error)."""


@dataclass(frozen=True, kw_only=True)
class SpecialFeatureSpec(ABC):
    """One entry of a definition's ``special_features``: use :class:`SpecialColumn` or :class:`SpecialColumnGroup`."""

    kind: ClassVar[str]
    """The kind it declares (:data:`~data_foundry.schema.SpecialFeatureKind`)."""
    layout: ClassVar[str]
    """``column`` or ``group``."""
    encoding_required: ClassVar[bool]
    """Whether the raw values are unusable as model inputs (a SMILES string)."""
    dtype: ClassVar[str | None] = None
    """The dtype the build casts the columns to (``string`` for a SMILES); None leaves them as ``_clean`` returns."""

    @property
    @abstractmethod
    def feature_name(self) -> str:
        """The name the container records."""

    @abstractmethod
    def resolve(self, names: Iterable[str]) -> tuple[list[str], SpectrumDetails | None]:
        """The feature's columns among the frame's ``names``, in order, and what the kind adds about them.

        Raises:
            SpecialFeatureError: The columns are not in the frame.
        """

    def describe(self) -> str:
        """What the container says the feature is."""
        return getattr(self, "description", None) or ""

    def record(self, names: Iterable[str]) -> SpecialFeature:
        """The container's record of the feature, for the columns ``names`` of the frame."""
        columns, details = self.resolve(names)
        feature = SpecialFeature(
            name=self.feature_name,
            kind=self.kind,
            layout=self.layout,
            columns=columns,
            description="",
            encoding_required=self.encoding_required,
            details=details,
        )
        default = type(self).encodings(feature)[0]
        return SpecialFeature(
            name=feature.name,
            kind=feature.kind,
            layout=feature.layout,
            columns=feature.columns,
            description=f"{self.describe()} Recommended encoding: {default.description}".strip(),
            encoding_required=feature.encoding_required,
            recommended_encoding=default.id,
            details=details,
        )

    # --- what the kind does with a record (a container's, without the declaration) ----------------------------
    @classmethod
    @abstractmethod
    def encodings(cls, feature: SpecialFeature) -> tuple[Encoding, ...]:
        """The candidate encodings of ``feature``, the recommended one first."""

    @classmethod
    @abstractmethod
    def encode(cls, frame: pd.DataFrame, feature: SpecialFeature, encoding: Encoding) -> pd.DataFrame:
        """``frame`` (the feature's columns, in order) in ``encoding``: the columns that replace them, same index."""

    @classmethod
    def check(cls, df: pd.DataFrame, feature: SpecialFeature) -> Iterator[CheckResult]:
        """The kind's bundle checks of ``feature`` in ``df`` (its columns are present); none by default."""
        del df, feature
        return iter(())


@dataclass(frozen=True, kw_only=True)
class SpecialColumn(SpecialFeatureSpec):
    """A special feature in one column (``layout="column"``), e.g. ``Smiles(column="SMILES")``."""

    layout: ClassVar[str] = "column"
    column: str
    """The column of the frame; the feature's name in the container."""

    @property
    def feature_name(self) -> str:
        """The column."""
        return self.column

    def resolve(self, names: Iterable[str]) -> tuple[list[str], None]:
        """The column, when the frame has it."""
        if self.column not in set(names):
            msg = f"`special_features` names the {self.kind} column {self.column!r}, which `_clean` does not return."
            raise SpecialFeatureError(msg)
        return [self.column], None


@dataclass(frozen=True, kw_only=True)
class SpecialColumnGroup(SpecialFeatureSpec):
    """A special feature in a group of columns (``layout="group"``) that hold one object together, in a fixed order,
    and are encoded together: every column whose name starts with ``prefix``, e.g. ``Spectrum(name="serum_ms",
    prefix="M/Z:", ...)``. A kind orders them (a spectrum by the position in the name); the default is frame order.
    """

    layout: ClassVar[str] = "group"
    name: str
    """The feature's name in the container, e.g. ``serum_ms``."""
    prefix: str
    """The start of every column name of the group, e.g. ``M/Z:`` for ``M/Z:800.32``."""
    description: str
    """What the feature is: the instrument, the range and resolution, what the source did to the values."""

    @property
    def feature_name(self) -> str:
        """The group's name."""
        return self.name

    def matched(self, names: Iterable[str]) -> list[str]:
        """The frame's columns that start with the prefix, in frame order; at least two."""
        matched = [n for n in names if isinstance(n, str) and n.startswith(self.prefix)]
        if len(matched) < 2:
            msg = (
                f"Special feature {self.name!r}: {len(matched)} column(s) start with {self.prefix!r}; a group needs "
                "two."
            )
            raise SpecialFeatureError(msg)
        return matched

    def resolve(self, names: Iterable[str]) -> tuple[list[str], SpectrumDetails | None]:
        """The matching columns in frame order, and no details."""
        return self.matched(names), None


def special_feature_kind(kind: str) -> type[SpecialFeatureSpec]:
    """The class of ``kind`` (``smiles``, ``spectrum``).

    Raises:
        ValueError: An unknown kind.
    """
    from data_foundry.v2.chemistry import Smiles  # noqa: PLC0415 - the kinds import this module
    from data_foundry.v2.spectra import Spectrum  # noqa: PLC0415

    kinds = {cls.kind: cls for cls in (Smiles, Spectrum)}
    if kind not in kinds:
        msg = f"Unknown special feature kind {kind!r}; known: {sorted(kinds)}."
        raise ValueError(msg)
    return kinds[kind]


def encodings_for(feature: SpecialFeature) -> tuple[Encoding, ...]:
    """The candidate encodings of a special feature, the recommended one first (a raw mass spectrum has three
    published candidates, a vibrational spectrum four, a SMILES one).
    """
    return special_feature_kind(feature.kind).encodings(feature)


def encode_special_feature(
    df: pd.DataFrame, feature: SpecialFeature, encoding: Encoding | str | None = None
) -> pd.DataFrame:
    """``df`` with the feature's columns replaced, where they stand, by their encoding: the recommended one, or
    ``encoding`` (an :class:`~data_foundry.v2.encodings.Encoding` among :func:`encodings_for` or its spec id).

    A SMILES column becomes its descriptor and fingerprint columns (``<column>__<name>``); a spectrum keeps its columns
    with new values. Every encoding works per value or per row, so the rows of every split get the same values.

    Raises:
        ValueError: An encoding that is not a candidate of the feature.
    """
    candidates = encodings_for(feature)
    wanted = feature.recommended_encoding if encoding is None else encoding
    wanted_id = wanted if isinstance(wanted, str) or wanted is None else wanted.id
    chosen = next((e for e in candidates if e.id == wanted_id), None) if wanted_id else candidates[0]
    if chosen is None:
        msg = f"{wanted_id!r} is no encoding of {feature.name!r}; candidates: {[e.id for e in candidates]}."
        raise ValueError(msg)
    encoded = special_feature_kind(feature.kind).encode(df[feature.columns], feature, chosen)
    if list(encoded.columns) == list(feature.columns):
        out = df.copy()
        out[feature.columns] = encoded
        return out
    position = df.columns.get_loc(feature.columns[0])
    rest = df.drop(columns=feature.columns)
    return pd.concat([rest.iloc[:, :position], encoded, rest.iloc[:, position:]], axis=1)
