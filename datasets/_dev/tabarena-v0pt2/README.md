# TabArena-v0.2  Curation Overview

Working setup towards TabArena-v0.2

- **Every change is logged** in [`CHANGELOG.md`](CHANGELOG.md): edits, added or removed files, re-runs that change a container.
- The leak audit of September-October 2026 (removed and changed datasets, with severity) is summarised in [`LEAK_AUDIT.md`](LEAK_AUDIT.md).
- Changes the benchmark harness (TabArena) needs for these datasets, for example scoring grouped tasks per group, are in [`BENCHMARK_CHANGES_TODO.md`](BENCHMARK_CHANGES_TODO.md).
- The design plan for grouped data (use cases, new metadata, recommended scoring, checks, dataset review) is in [`GROUPED_DATA_PLAN.md`](GROUPED_DATA_PLAN.md).
- Each dataset folder has a `README.md` that `data-foundry-curation dataset check` generates from its `dataset.py`: the folder's files, links to the curation record and the source, how to rebuild, the evidence and the build record. Folders still holding their v1 notebook get one when their migration is checked ([`TODO.md`](TODO.md)).
