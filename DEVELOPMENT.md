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
   annotated `vX.Y.Z` git tag, and pushes both the commit and the tag.
2. **Pushing the tag is what fires the release.** The
   [`Release` workflow](.github/workflows/release.yaml) listens for
   `push: tags: ['v*']`, so any `vX.Y.Z` tag that reaches GitHub kicks
   off `uv build` + `uv publish` and creates a GitHub Release with the
   sdist + wheel attached. The branch push on its own does nothing.

### Re-triggering or releasing without the script

Because the trigger is the tag push, you can drive the workflow by hand
in two situations:

* **Re-run a failed release** (e.g. PyPI auth blew up): go to
  `Actions → Release → <failed run> → Re-run failed jobs`. No new tag,
  no new commit — the workflow re-checks out the same tagged commit.
* **Release without the script:** bump `pyproject.toml` manually, commit
  on `main`, then:
  ```bash
  git tag -a vX.Y.Z -m "data-foundry X.Y.Z"
  git push <remote> main
  git push <remote> vX.Y.Z   # <- this line is what triggers the workflow
  ```
  The workflow's first step refuses to publish if the tag name doesn't
  match the version in `pyproject.toml`, so the bump and the tag must
  agree.

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
