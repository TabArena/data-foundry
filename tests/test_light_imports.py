"""The modules a benchmark imports load nothing of the build side or the curation log."""

from __future__ import annotations

import subprocess
import sys


def test_the_consumer_modules_load_nothing_of_the_build_side() -> None:
    """A benchmark that scores, sub-samples and encodes never imports the definition side or the curation log."""
    code = (
        "import sys; import data_foundry.metrics, data_foundry.sampling, data_foundry.special.chemistry, "
        "data_foundry.special.spectra, data_foundry.encodings, data_foundry.curation_container; "
        "print(' '.join(m for m in sys.modules if m.startswith('data_foundry')))"
    )
    run = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)  # noqa: S603 - fixed code
    loaded = run.stdout.split()
    heavy = [m for m in loaded if m.startswith(("data_foundry.definition", "data_foundry.curation."))]
    assert not heavy
    assert "data_foundry.bundle_checks" not in loaded
