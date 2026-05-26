# Developer Documentation

Maintainer-facing notes for the Data Foundry package. See
[**CONTRIBUTING_DATASETS.md**](CONTRIBUTING_DATASETS.md) for the
dataset-contributor flow and [**AGENTS.md**](AGENTS.md) for the
agent-facing brief on the codebase.

## 🚢 Releasing to PyPI

> [!NOTE]
> Releases are cut by the maintainers. The flow below is what they run.

```bash
# 1. Bump the version in pyproject.toml.
# 2. Build sdist + wheel.
uv build

# 3. (Optional) sanity-check against TestPyPI first.
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TESTPYPI_TOKEN"
pip install --index-url https://test.pypi.org/simple/ data-foundry==<version>

# 4. Publish.
uv publish --token "$PYPI_TOKEN"
```

CI provenance and trusted-publishing via OIDC are tracked in
[`.github/workflows/`](.github/workflows) when the workflow lands.
