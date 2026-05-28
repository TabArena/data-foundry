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

### Prereleases (no git tag)

Two flavors, both publish to PyPI without creating a git tag, commit, or
GitHub Release. The version is set only on the CI runner.

**Automatic `.dev` builds on every push to `main`** —
[`.github/workflows/dev-release.yaml`](.github/workflows/dev-release.yaml).
Triggered via `workflow_run` after the `Tests` workflow succeeds. The
version is computed as `<next-patch>.dev<UTC-timestamp>` (e.g.
`0.0.4.dev20260528170102` when `pyproject.toml` is at `0.0.3`). This is
the AutoGluon-style "every commit is on PyPI" pattern — install with:

```bash
pip install --pre data-foundry        # any prerelease
pip install data-foundry==0.0.4.dev*  # a specific dev cycle
```

**Manual `alpha`/`beta`/`rc` from the Actions UI** —
[`.github/workflows/prerelease.yaml`](.github/workflows/prerelease.yaml).
Go to `Actions → Prerelease → Run workflow`, enter a PEP 440 prerelease
version (e.g. `0.0.4a1`, `0.0.4b2`, `0.0.4rc1`), and it publishes that
exact version. Stable `X.Y.Z` inputs are rejected — use the tag-push
release flow for those.

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
