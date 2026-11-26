"""A finding of a check (:class:`CheckResult`) and the report of a check run (:class:`BundleCheckReport`)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

Severity = Literal["error", "warning", "info"]

SEVERITY_ORDER: dict[Severity, int] = {"error": 0, "warning": 1, "info": 2}


class BundleCheckError(RuntimeError):
    """Raised by :meth:`BundleCheckReport.raise_if_errors` when a bundle has errors."""


@dataclass(frozen=True)
class CheckResult:
    """One finding of a check.

    Attributes:
        slug: Stable identifier of the check, listed in :data:`data_foundry.checks.registry.CHECKS` (use it in
            ``ignore=[...]``).
        severity: ``"error"`` (must fix), ``"warning"`` (look at it), or ``"info"``.
        message: What was found, including the offending values.
        hint: Optional "what to do about it" follow-up.
    """

    slug: str
    severity: Severity
    message: str
    hint: str | None = None

    def __str__(self) -> str:
        text = f"[{self.slug}] {self.message}"
        return f"{text}\n    -> {self.hint}" if self.hint else text


def run_guarded(name: str, check: Callable[[], Iterable[CheckResult]]) -> list[CheckResult]:
    """The findings of ``check``, or one ``check_crashed`` error that names it when it raises: a broken check must
    not hide the findings of the others. The bundle's runner and the definition's both go through it.
    """
    try:
        return list(check())
    except Exception as error:  # noqa: BLE001 - a broken check is a finding, not a crash
        return [
            CheckResult(
                "check_crashed",
                "error",
                f"Check `{name}` raised {type(error).__name__}: {error}",
                hint="A bug in the check or an unexpected bundle shape: report it.",
            )
        ]


def merge_same_slug(results: list[CheckResult], slug: str) -> list[CheckResult]:
    """``results`` with the findings of ``slug`` joined into one, at the strongest severity, in the place of the
    first: two check sites that see one cause (a placeholder in the metadata and in ``dataset.py``) report it once.
    """
    found = [r for r in results if r.slug == slug]
    if len(found) < 2:
        return results
    severity = min((r.severity for r in found), key=SEVERITY_ORDER.__getitem__)
    hints = list(dict.fromkeys(r.hint for r in found if r.hint))
    joined = CheckResult(slug, severity, " ".join(r.message for r in found), hint=" ".join(hints) or None)
    first = results.index(found[0])
    return [*(r for r in results[:first]), joined, *(r for r in results[first:] if r.slug != slug)]


@dataclass
class BundleCheckReport:
    """The findings of :func:`run_bundle_checks` for one bundle.

    Print it (``print(report)`` / just evaluate it in a notebook cell) for the
    human-readable report, use :meth:`raise_if_errors` to fail a notebook run, and
    :meth:`to_dict` to persist a machine-readable record of what was checked.
    """

    unique_name: str
    results: list[CheckResult] = field(default_factory=list)
    ignored: tuple[str, ...] = ()
    n_checks_run: int = 0

    def by_severity(self, severity: Severity) -> list[CheckResult]:
        """Return all findings of one severity, in the order they were produced."""
        return [r for r in self.results if r.severity == severity]

    @property
    def errors(self) -> list[CheckResult]:
        """Findings that must be fixed before the bundle is saved/shipped."""
        return self.by_severity("error")

    @property
    def warnings(self) -> list[CheckResult]:
        """Findings that need a human call (often fine, sometimes a real defect)."""
        return self.by_severity("warning")

    @property
    def infos(self) -> list[CheckResult]:
        """Informational findings, including checks skipped for cost reasons."""
        return self.by_severity("info")

    @property
    def ok(self) -> bool:
        """Whether the bundle produced no errors (warnings are allowed)."""
        return not self.errors

    @property
    def slugs(self) -> list[str]:
        """The slugs of all findings, in report order."""
        return [r.slug for r in self.results]

    def raise_if_errors(self) -> BundleCheckReport:
        """Raise :class:`BundleCheckError` if any finding is an error, else return self."""
        if self.ok:
            return self
        details = "\n".join(f"  - {r}" for r in self.errors)
        raise BundleCheckError(
            f"{len(self.errors)} bundle check error(s) for {self.unique_name!r}:\n{details}\n"
            "Fix the bundle, or pass `ignore=[<slug>, ...]` to accept a finding on purpose.",
        )

    def to_dict(self) -> dict:
        """Return a JSON-serializable record of the report."""
        return {
            "unique_name": self.unique_name,
            "n_checks_run": self.n_checks_run,
            "ignored": list(self.ignored),
            "counts": {
                "error": len(self.errors),
                "warning": len(self.warnings),
                "info": len(self.infos),
            },
            "findings": [
                {"slug": r.slug, "severity": r.severity, "message": r.message, "hint": r.hint} for r in self.results
            ],
        }

    def to_json(self, path: Path | str) -> Path:
        """Write :meth:`to_dict` to ``path`` (as an audit trail next to the bundle)."""
        path = Path(path)
        with path.open("w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return path

    def summary(self) -> str:
        """Return the human-readable report (same text as ``str(report)``)."""
        head = (
            f"Bundle checks — {self.unique_name}: "
            f"{len(self.errors)} error(s), {len(self.warnings)} warning(s), {len(self.infos)} info "
            f"({self.n_checks_run} checks run"
            + (f", {len(self.ignored)} ignored: {', '.join(self.ignored)}" if self.ignored else "")
            + ")"
        )
        if not self.results:
            return f"{head}\nAll checks passed. ✓"

        lines = [head]
        for severity, label in (("error", "ERRORS"), ("warning", "WARNINGS"), ("info", "INFO")):
            found = self.by_severity(severity)  # type: ignore[arg-type]
            if not found:
                continue
            lines.append(f"\n{label}")
            lines.extend(f"  {r}" for r in found)
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.summary()

    def __repr__(self) -> str:
        return self.summary()
