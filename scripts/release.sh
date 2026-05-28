#!/usr/bin/env bash
# Bump the data-foundry version, commit, tag, and push.
#
# Usage: scripts/release.sh <bump>
#   <bump> = patch | minor | major | X.Y.Z (explicit)
#
# What it does:
#   1. Verifies a clean working tree on the main branch.
#   2. Bumps the version in pyproject.toml via `uv version`.
#   3. Commits the bump and creates an annotated `v<new-version>` tag.
#   4. Pushes the commit and the tag to `origin`.
#
# After the tag lands on GitHub, .github/workflows/release.yaml builds the
# sdist + wheel and publishes them to PyPI (and creates a GitHub Release).

set -euo pipefail

REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-main}"

usage() {
    sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
}

if [[ $# -ne 1 ]]; then
    usage
fi

BUMP="$1"

# Repo root = parent of this script's directory.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# 1. Sanity checks.
current_branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$current_branch" != "$BRANCH" ]]; then
    echo "error: must be on '$BRANCH' (currently on '$current_branch')" >&2
    exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "error: working tree has uncommitted changes" >&2
    git status --short >&2
    exit 1
fi

echo "Fetching $REMOTE..."
git fetch --tags "$REMOTE"

local_sha="$(git rev-parse HEAD)"
remote_sha="$(git rev-parse "$REMOTE/$BRANCH")"
if [[ "$local_sha" != "$remote_sha" ]]; then
    echo "error: local '$BRANCH' is not in sync with '$REMOTE/$BRANCH'" >&2
    exit 1
fi

old_version="$(uv version --short)"
echo "Current version: $old_version"

# 2. Bump.
case "$BUMP" in
    patch|minor|major)
        uv version --bump "$BUMP" >/dev/null
        ;;
    [0-9]*.[0-9]*.[0-9]*)
        uv version "$BUMP" >/dev/null
        ;;
    *)
        echo "error: <bump> must be patch | minor | major | X.Y.Z (got '$BUMP')" >&2
        exit 1
        ;;
esac

new_version="$(uv version --short)"
tag="v$new_version"
echo "New version: $new_version (tag: $tag)"

if git rev-parse "$tag" >/dev/null 2>&1; then
    echo "error: tag '$tag' already exists locally" >&2
    git checkout -- pyproject.toml uv.lock 2>/dev/null || true
    exit 1
fi

# 3. Commit + tag.
git add pyproject.toml
# Only stage uv.lock if it's already tracked (it's gitignored in this repo).
if git ls-files --error-unmatch uv.lock >/dev/null 2>&1; then
    git add uv.lock
fi
git commit -m "release: $new_version"
git tag -a "$tag" -m "data-foundry $new_version"

# 4. Push. Show the user what we're about to do.
echo
echo "About to push to $REMOTE:"
echo "  - branch '$BRANCH' (commit $(git rev-parse --short HEAD))"
echo "  - tag    '$tag'"
read -r -p "Push now? [y/N] " reply
case "$reply" in
    y|Y|yes|YES)
        git push "$REMOTE" "$BRANCH"
        git push "$REMOTE" "$tag"
        echo
        echo "Pushed. Watch the release workflow at:"
        echo "  https://github.com/$(git remote get-url "$REMOTE" | sed -E 's#.*[:/](.+/.+)\.git#\1#')/actions"
        ;;
    *)
        echo "Skipped push. To complete the release later, run:"
        echo "  git push $REMOTE $BRANCH && git push $REMOTE $tag"
        ;;
esac
