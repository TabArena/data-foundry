# Developer Documentation

Maintainer-facing notes for the Data Foundry package. See
[**CONTRIBUTING_DATASETS.md**](CONTRIBUTING_DATASETS.md) for the
dataset-contributor flow and [**AGENTS.md**](AGENTS.md) for the
agent-facing brief on the codebase.

## 🚢 Releasing to PyPI

> [!NOTE]
> Releases are cut by the maintainers. The flow below is what they run.

One command bumps the version, commits, tags, and pushes:

```bash
scripts/release.sh patch        # 0.0.2 -> 0.0.3
scripts/release.sh minor        # 0.0.2 -> 0.1.0
scripts/release.sh major        # 0.0.2 -> 1.0.0
scripts/release.sh 0.1.2        # explicit version
```

What this triggers:

1. Local script checks the working tree is clean and on `main`, bumps the
   version in `pyproject.toml` (via `uv version`), commits, creates an
   annotated `vX.Y.Z` git tag, and pushes both to `origin`.
2. The [`Release` workflow](.github/workflows/release.yaml) fires on the
   pushed `v*` tag and runs `uv build` + `uv publish`, publishing the
   sdist and wheel to PyPI and creating a GitHub Release with the
   artifacts attached.

### One-time setup

* Add a `PYPI_TOKEN` secret in the GitHub `pypi` environment
  (`Settings → Environments → pypi → Add secret`) holding a PyPI API
  token scoped to `data-foundry`. The workflow consumes it via
  `UV_PUBLISH_TOKEN`.
* Once you switch to PyPI trusted publishing, drop the `PYPI_TOKEN` env
  block — the workflow already requests `id-token: write` for OIDC.

### Manual fallback

If the workflow is unavailable, you can still publish locally:

```bash
uv build
uv publish --token "$PYPI_TOKEN"
```
