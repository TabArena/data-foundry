"""Live dataset claims: who works on which dataset right now, shared through one git branch.

A claim says that one curator is working on one dataset: its curation record and its v2 folder (with ``REVIEW.md``).
Claims do not travel with the work. They live on a branch of their own (``claims`` on ``origin`` by default): one
small YAML file per claimed dataset under ``claims/``, and a generated ``README.md`` table that GitHub shows as the
team's board. A claim is pushed straight to that branch, with no pull request, so the other curators and their agents
see it within seconds.

Atomicity comes from git. Every change is a commit on top of the tip just fetched, and the remote rejects a push that
is not a fast-forward. When two curators change the board at the same moment, one push lands; the other fetches
again, checks again (the dataset may now be taken) and retries. Nothing here touches the working tree, the index or
the checked-out branch: the commits are built with git plumbing in a temporary index.

Login is the remote's own: whoever can push to the repository can claim, whoever can read it sees the board. Any git
remote works; ``$DATA_FOUNDRY_CLAIMS_REMOTE`` and ``$DATA_FOUNDRY_CLAIMS_BRANCH`` pick another remote or branch.

The curator is named by ``$DATA_FOUNDRY_CURATOR`` or ``git config data-foundry.curator`` and must be one of the
``claimed_by`` values of ``vocabularies.yaml``. Each fetch caches the board in the git directory
(``data-foundry-claims.json``), so the warnings (``save_record``, the Claude Code hook, the dashboard) need no network.

Claims are advisory: nothing refuses a write. A claim expires after ``ttl_days`` (7 by default) unless renewed; an
expired claim can be taken over with ``steal``. The records keep ``claimed_by`` and the WIP value as a mirror of the
board (:func:`mirror_to_records`), written in the work branch and merged with the work.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import tempfile
import time
import warnings
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, replace
from functools import cache
from pathlib import Path

import yaml

from data_foundry.curation._paths import records_dir, resolve_curation_root

CLAIMS_REMOTE_ENV = "DATA_FOUNDRY_CLAIMS_REMOTE"
CLAIMS_BRANCH_ENV = "DATA_FOUNDRY_CLAIMS_BRANCH"
CURATOR_ENV = "DATA_FOUNDRY_CURATOR"
CURATOR_GIT_KEY = "data-foundry.curator"
DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "claims"
LOCAL_REF = "refs/data-foundry/claims"
"""Where the fetched board is kept locally: a private ref, never a branch anyone checks out."""
CACHE_NAME = "data-foundry-claims.json"
CLAIMS_DIR = "claims"
STAGES: tuple[str, ...] = ("triage", "add", "review")
"""``triage``: the verdict is open (screening, a check); ``add``: the v2 folder is being built; ``review``: the
curator's review of an added dataset."""
DEFAULT_TTL_DAYS = 7
MAX_ATTEMPTS = 5

PAGES_DISPATCH_PATH = ".github/workflows/claims-to-pages.yaml"
PAGES_DISPATCH_WORKFLOW = """\
# Lives on the claims branch only: every push of a claim asks the Pages workflow on main to rebuild the
# read-only dashboard, so its Claimed by column follows the board. Written by `data-foundry-curation claims init`.
name: Claims to Pages
on:
  push:
    branches: [claims]
permissions:
  actions: write
jobs:
  dispatch:
    runs-on: ubuntu-latest
    steps:
      - run: gh workflow run pages.yaml --repo "$GITHUB_REPOSITORY" --ref main
        env:
          GH_TOKEN: ${{ github.token }}
"""


class ClaimsError(RuntimeError):
    """A claims operation could not be done (no curator name, no access to the remote, a busy branch)."""


class ClaimWarning(UserWarning):
    """A dataset is being changed while another curator holds its claim."""


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def _iso(when: dt.datetime) -> str:
    return when.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_time(value: object) -> dt.datetime:
    if isinstance(value, dt.datetime):  # YAML read an unquoted timestamp
        return value if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)
    return dt.datetime.strptime(str(value), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


@dataclass(frozen=True)
class Claim:
    """One curator's claim on one dataset."""

    name: str
    """The dataset's ``unique_name`` (the record's file stem and the v2 folder name)."""
    holder: str
    """The curator, a ``claimed_by`` value of the vocabulary."""
    stage: str
    """One of :data:`STAGES`."""
    claimed_at: str
    """UTC, ``YYYY-MM-DDTHH:MM:SSZ``; kept when the holder renews."""
    expires_at: str
    """UTC; after it, anyone may take the claim over (``steal``)."""
    note: str = ""
    """Free text: what is being done, e.g. "add-dataset batch 3"."""

    def expired(self, now: dt.datetime | None = None) -> bool:
        """Whether the claim is past its expiry."""
        return self.seconds_left(now) <= 0

    def seconds_left(self, now: dt.datetime | None = None) -> float:
        """Seconds until the claim expires (negative once it has)."""
        return (_parse_time(self.expires_at) - (now or _utcnow())).total_seconds()

    def describe(self) -> str:
        """One line for messages: holder, stage, dates and note."""
        state = "expired" if self.expired() else "until"
        text = f"{self.holder} ({self.stage}) since {self.claimed_at[:10]}, {state} {self.expires_at[:10]}"
        return f"{text}: {self.note}" if self.note else text

    def to_yaml(self) -> str:
        """The file stored on the claims branch."""
        return yaml.safe_dump(asdict(self), sort_keys=False, allow_unicode=True, width=4096)

    @classmethod
    def from_mapping(cls, data: dict[str, object]) -> Claim:
        """Read a claim from a parsed YAML file or the cache, tolerating timestamps YAML parsed itself."""
        return cls(
            name=str(data["name"]),
            holder=str(data["holder"]),
            stage=str(data.get("stage") or "triage"),
            claimed_at=_iso(_parse_time(data["claimed_at"])),
            expires_at=_iso(_parse_time(data["expires_at"])),
            note=str(data.get("note") or ""),
        )


@dataclass(frozen=True)
class Board:
    """Every claim on the claims branch at one commit."""

    claims: dict[str, Claim]
    tip: str | None
    """The branch's commit, or ``None`` when the branch does not exist yet."""
    fetched_at: float
    """When the board was read from the remote (epoch seconds)."""
    remote: str
    branch: str

    def age(self) -> float:
        """Seconds since the board was fetched."""
        return time.time() - self.fetched_at

    def held_by_other(self, name: str, me: str | None) -> Claim | None:
        """The live claim on ``name`` when someone other than ``me`` holds it, else ``None``."""
        claim = self.claims.get(name)
        if claim is None or claim.holder == me or claim.expired():
            return None
        return claim

    def by_holder(self) -> dict[str, list[Claim]]:
        """The claims grouped by holder, holders and names sorted."""
        out: dict[str, list[Claim]] = {}
        for claim in sorted(self.claims.values(), key=lambda c: (c.holder, c.name)):
            out.setdefault(claim.holder, []).append(claim)
        return out


@dataclass(frozen=True)
class Outcome:
    """What a change of the board did."""

    changed: list[str]
    """The datasets written: claimed, renewed or released."""
    skipped: dict[str, str]
    """The datasets left alone, each with the reason."""
    board: Board
    """The board after the change."""


# -- git ------------------------------------------------------------------------------------------------------------


def repo_root() -> Path:
    """The repository the claims are read from and pushed through: the parent of the curation root."""
    return resolve_curation_root().parent


def claims_remote() -> str:
    """The remote that holds the claims branch (``$DATA_FOUNDRY_CLAIMS_REMOTE``, default ``origin``)."""
    return os.environ.get(CLAIMS_REMOTE_ENV) or DEFAULT_REMOTE


def claims_branch() -> str:
    """The claims branch (``$DATA_FOUNDRY_CLAIMS_BRANCH``, default ``claims``)."""
    return os.environ.get(CLAIMS_BRANCH_ENV) or DEFAULT_BRANCH


def _run_git(
    repo: Path, *args: str, stdin: str | bytes | None = None, env: dict[str, str] | None = None, binary: bool = False
) -> subprocess.CompletedProcess:
    """Run git without a terminal: a credential or passphrase prompt fails at once instead of hanging a hook."""
    env = {**(env if env is not None else os.environ), "GIT_TERMINAL_PROMPT": "0"}
    feed = {"input": stdin} if stdin is not None else {"stdin": subprocess.DEVNULL}
    try:
        return subprocess.run(  # noqa: S603 - fixed git subcommands; names are passed as data, never to a shell
            ["git", "-C", str(repo), *args],  # noqa: S607 - git from PATH
            **feed,
            capture_output=True,
            text=not binary,
            encoding=None if binary else "utf-8",
            env=env,
            timeout=60,
            start_new_session=True,  # no controlling terminal, so ssh cannot stop to ask for a passphrase
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ClaimsError(f"git {args[0]} failed: {exc}") from exc


def _git(repo: Path, *args: str, stdin: str | None = None, env: dict[str, str] | None = None) -> str:
    proc = _run_git(repo, *args, stdin=stdin, env=env)
    if proc.returncode:
        raise ClaimsError(f"git {' '.join(args[:2])} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


_AUTH_HINT = (
    "The claims use the same remote and credentials as `git push`; check that `git ls-remote {remote}` works here "
    "(an ssh agent that went stale can be bypassed with `env SSH_AUTH_SOCK= <command>`)."
)


def _remote_error(action: str, stderr: str, remote: str) -> ClaimsError:
    return ClaimsError(f"{action} on '{remote}' failed: {stderr.strip()}\n{_AUTH_HINT.format(remote=remote)}")


@cache
def _git_dir(repo: str) -> Path | None:
    """The repository's common git directory (shared by its worktrees), or ``None`` outside a git repository."""
    try:
        proc = _run_git(Path(repo), "rev-parse", "--git-common-dir")
    except ClaimsError:
        return None
    if proc.returncode:
        return None
    path = Path(proc.stdout.strip())
    return path if path.is_absolute() else (Path(repo) / path).resolve()


# -- reading the board ------------------------------------------------------------------------------------------------


def _read_tree(repo: Path, tip: str) -> dict[str, Claim]:
    listing = _run_git(repo, "ls-tree", "-r", "-z", tip, "--", f"{CLAIMS_DIR}/", binary=True)
    if listing.returncode:
        raise ClaimsError(f"git ls-tree failed: {listing.stderr.decode(errors='replace').strip()}")
    shas = []
    for entry in listing.stdout.split(b"\0"):
        if not entry:
            continue
        meta, _, path = entry.partition(b"\t")
        if path.endswith(b".yaml"):
            shas.append(meta.split()[2])
    if not shas:
        return {}
    batch = _run_git(repo, "cat-file", "--batch", stdin=b"\n".join(shas) + b"\n", binary=True)
    if batch.returncode:
        raise ClaimsError(f"git cat-file failed: {batch.stderr.decode(errors='replace').strip()}")
    out, data, pos = {}, batch.stdout, 0
    for _ in shas:
        header_end = data.index(b"\n", pos)
        size = int(data[pos:header_end].split()[2])
        body = data[header_end + 1 : header_end + 1 + size]
        pos = header_end + 1 + size + 1
        claim = Claim.from_mapping(yaml.safe_load(body.decode("utf-8")) or {})
        out[claim.name] = claim
    return out


def fetch(repo: str | Path | None = None) -> Board:
    """Fetch the claims branch from the remote, cache it and return the board (an empty one when there is no branch).

    Raises:
        ClaimsError: the remote cannot be reached or read.
    """
    repo = Path(repo) if repo is not None else repo_root()
    remote, branch = claims_remote(), claims_branch()
    proc = _run_git(
        repo, "fetch", "--quiet", "--no-tags", "--no-write-fetch-head", remote, f"+refs/heads/{branch}:{LOCAL_REF}"
    )
    if proc.returncode:
        if "couldn't find remote ref" not in proc.stderr:
            raise _remote_error("Fetching the claims", proc.stderr, remote)
        _run_git(repo, "update-ref", "-d", LOCAL_REF)  # the branch is gone (or was never made): an empty board
        board = Board({}, None, time.time(), remote, branch)
    else:
        tip = _git(repo, "rev-parse", LOCAL_REF)
        board = Board(_read_tree(repo, tip), tip, time.time(), remote, branch)
    _write_cache(repo, board)
    return board


def _cache_path(repo: Path) -> Path | None:
    git_dir = _git_dir(str(Path(repo).resolve()))
    return git_dir / CACHE_NAME if git_dir is not None else None


def _write_cache(repo: Path, board: Board) -> None:
    path = _cache_path(repo)
    if path is None:
        return
    payload = {
        "remote": board.remote,
        "branch": board.branch,
        "tip": board.tip,
        "fetched_at": board.fetched_at,
        "claims": [asdict(c) for c in board.claims.values()],
    }
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False) as tmp:
        json.dump(payload, tmp, ensure_ascii=False, indent=1)
    Path(tmp.name).replace(path)  # atomic: a reader never sees half a file


_CACHE_MEMO: dict[Path, tuple[int, Board]] = {}


def cached_board(repo: str | Path | None = None) -> Board | None:
    """The board of the last fetch, from the cache; ``None`` when there is none (never touches the network)."""
    try:
        path = _cache_path(Path(repo) if repo is not None else repo_root())
        if path is None or not path.exists():
            return None
        mtime = path.stat().st_mtime_ns
        memo = _CACHE_MEMO.get(path)
        if memo is not None and memo[0] == mtime:
            board = memo[1]
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            claims = {c["name"]: Claim.from_mapping(c) for c in data.get("claims", [])}
            board = Board(claims, data.get("tip"), float(data["fetched_at"]), data["remote"], data["branch"])
            _CACHE_MEMO[path] = (mtime, board)
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if (board.remote, board.branch) != (claims_remote(), claims_branch()):
        return None
    return board


def load(repo: str | Path | None = None, max_age: float = 30.0) -> Board:
    """The cached board when it is at most ``max_age`` seconds old, else a fresh :func:`fetch`."""
    board = cached_board(repo)
    if board is not None and board.age() <= max_age:
        return board
    return fetch(repo)


# -- who am I ---------------------------------------------------------------------------------------------------------


def configured_curator(repo: str | Path | None = None) -> str | None:
    """The curator name from ``$DATA_FOUNDRY_CURATOR`` or ``git config data-foundry.curator``, unchecked."""
    name = os.environ.get(CURATOR_ENV)
    if name:
        return name.strip()
    try:
        proc = _run_git(Path(repo) if repo is not None else repo_root(), "config", "--get", CURATOR_GIT_KEY)
    except ClaimsError:
        return None
    if proc.returncode:
        return None
    return proc.stdout.strip() or None


def current_curator(repo: str | Path | None = None) -> str:
    """The configured curator name, checked against the ``claimed_by`` vocabulary.

    Raises:
        ClaimsError: no name is configured, or it is not in the vocabulary.
    """
    from data_foundry.curation.record import load_vocabularies  # noqa: PLC0415 - record imports nothing from here

    allowed = load_vocabularies().get("claimed_by", [])
    name = configured_curator(repo)
    hint = f"one of: {', '.join(allowed)}" if allowed else "a name from vocabularies.yaml (claimed_by)"
    if not name:
        raise ClaimsError(f"Name yourself first: `git config {CURATOR_GIT_KEY} <Name>` (or ${CURATOR_ENV}), {hint}.")
    if allowed and name not in allowed:
        raise ClaimsError(f"Curator '{name}' is not in vocabularies.yaml (claimed_by); use {hint}.")
    return name


# -- changing the board -----------------------------------------------------------------------------------------------


def render_readme(claims: dict[str, Claim], now: dt.datetime | None = None) -> str:
    """The board as the markdown table GitHub shows on the claims branch, one section per holder."""
    now = now or _utcnow()
    groups: dict[str, list[Claim]] = {}
    for claim in sorted(claims.values(), key=lambda c: (c.holder, c.name)):
        groups.setdefault(claim.holder, []).append(claim)
    counts = ", ".join(f"{holder} {len(items)}" for holder, items in groups.items())
    lines = [
        "# Dataset claims",
        "",
        "Who is working on which dataset right now. A claim covers the dataset's curation record and its dataset "
        "folder. One file per claim under `claims/`, written by `data-foundry-curation claims` (claim, release, "
        "renew); do not edit by hand. An expired claim can be taken over.",
        "",
        f"As of {now.strftime('%Y-%m-%d %H:%M')} UTC: {len(claims)} claim(s)" + (f" ({counts})." if counts else "."),
    ]
    for holder, items in groups.items():
        lines += ["", f"## {holder}", "", "| Dataset | Stage | Since | Until | Note |", "|---|---|---|---|---|"]
        for c in items:
            until = c.expires_at[:10] + (" (expired)" if c.expired(now) else "")
            note = c.note.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| `{c.name}` | {c.stage} | {c.claimed_at[:10]} | {until} | {note} |")
    return "\n".join(lines) + "\n"


def _commit(
    repo: Path,
    tip: str | None,
    changes: dict[str, Claim | None],
    claims: dict[str, Claim],
    message: str,
    extra: dict[str, str] | None = None,
) -> str:
    """A commit on ``tip`` that writes ``changes`` (``None`` removes a claim) and the README, built off the worktree."""
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        _git(repo, "read-tree", *([tip] if tip else ["--empty"]), env=env)
        files: dict[str, str | None] = {
            f"{CLAIMS_DIR}/{n}.yaml": (c.to_yaml() if c else None) for n, c in changes.items()
        }
        files["README.md"] = render_readme(claims)
        files.update(extra or {})
        for path, text in files.items():
            if text is None:
                _git(repo, "update-index", "--force-remove", "--", path, env=env)
            else:
                blob = _git(repo, "hash-object", "-w", "--stdin", stdin=text)
                _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env=env)
        tree = _git(repo, "write-tree", env=env)
    return _git(repo, "commit-tree", tree, "-m", message, *(["-p", tip] if tip else []))


def _rejected(stderr: str) -> bool:
    """Whether a push failed because the branch moved (retry), not because of access or the network."""
    return any(s in stderr for s in ("[rejected]", "non-fast-forward", "fetch first", "cannot lock ref"))


Decision = tuple[dict[str, "Claim | None"], dict[str, str], str]


def _update(
    repo: str | Path | None, decide: Callable[[Board], Decision], extra: dict[str, str] | None = None
) -> Outcome:
    """Fetch, decide, commit and push; when the push loses a race, do it all again on the new tip."""
    repo = Path(repo) if repo is not None else repo_root()
    remote, branch = claims_remote(), claims_branch()
    for _ in range(MAX_ATTEMPTS):
        board = fetch(repo)
        changes, skipped, message = decide(board)
        if not changes and extra is None:
            return Outcome([], skipped, board)
        claims = dict(board.claims)
        for name, claim in changes.items():
            if claim is None:
                claims.pop(name, None)
            else:
                claims[name] = claim
        commit = _commit(repo, board.tip, changes, claims, message, extra)
        push = _run_git(repo, "push", "--quiet", remote, f"{commit}:refs/heads/{branch}")
        if push.returncode == 0:
            _git(repo, "update-ref", LOCAL_REF, commit)
            new = Board(claims, commit, time.time(), remote, branch)
            _write_cache(repo, new)
            return Outcome(sorted(changes), skipped, new)
        if not _rejected(push.stderr):
            raise _remote_error("Pushing the claims", push.stderr, remote)
    raise ClaimsError(f"The claims branch kept moving ({MAX_ATTEMPTS} attempts); run the command again.")


def _names(names: Iterable[str]) -> list[str]:
    out = list(dict.fromkeys(n.strip() for n in names if n and n.strip()))
    for name in out:
        if "/" in name or name.startswith("."):
            raise ClaimsError(f"Not a dataset name: {name!r}")
    return out


def _list_for_message(names: Iterable[str], limit: int = 8) -> str:
    names = list(names)
    head = ", ".join(names[:limit])
    return head + (f" and {len(names) - limit} more" if len(names) > limit else "")


def claim(
    names: Iterable[str],
    *,
    stage: str,
    note: str = "",
    ttl_days: float = DEFAULT_TTL_DAYS,
    steal: bool = False,
    holder: str | None = None,
    repo: str | Path | None = None,
) -> Outcome:
    """Claim datasets for the current curator; renew the ones they already hold.

    A dataset someone else holds is skipped with the reason; an expired one is taken over only with ``steal`` (the
    commit message names the previous holder). Renewing keeps ``claimed_at`` and, without a new ``note``, the note.

    Args:
        names: The datasets' unique names.
        stage: One of :data:`STAGES`.
        note: What is being done (optional).
        ttl_days: Days until the claim expires.
        steal: Take over expired claims of others.
        holder: Claim in this curator's name (only for importing the records' claims); defaults to the current
            curator.
        repo: The repository (defaults to the one of the curation root).

    Returns:
        The datasets claimed, the ones skipped with the reason, and the new board.
    """
    if stage not in STAGES:
        raise ClaimsError(f"Unknown stage {stage!r}; use one of {', '.join(STAGES)}.")
    me = holder or current_curator(repo)
    wanted = _names(names)

    def decide(board: Board) -> Decision:
        now = _utcnow()
        expires = _iso(now + dt.timedelta(days=ttl_days))
        changes: dict[str, Claim | None] = {}
        skipped: dict[str, str] = {}
        taken: list[str] = []
        for name in wanted:
            old = board.claims.get(name)
            mine = old is not None and old.holder == me
            if old is not None and not mine:
                if not old.expired(now):
                    skipped[name] = f"held by {old.describe()}"
                    continue
                if not steal:
                    skipped[name] = f"held by {old.describe()}; take it over with --steal"
                    continue
                taken.append(f"{name} from {old.holder}")
            changes[name] = Claim(
                name=name,
                holder=me,
                stage=stage,
                claimed_at=old.claimed_at if mine else _iso(now),
                expires_at=expires,
                note=note or (old.note if mine else ""),
            )
        message = f"claim: {_list_for_message(changes)} ({me}, {stage})"
        if taken:
            message += f"; taken over: {', '.join(taken)}"
        return changes, skipped, message

    return _update(repo, decide)


def release(
    names: Iterable[str], *, force: bool = False, holder: str | None = None, repo: str | Path | None = None
) -> Outcome:
    """Release datasets the current curator holds; another curator's claim only with ``force`` (named in the log)."""
    me = holder or current_curator(repo)
    wanted = _names(names)

    def decide(board: Board) -> Decision:
        changes: dict[str, Claim | None] = {}
        skipped: dict[str, str] = {}
        forced: list[str] = []
        for name in wanted:
            old = board.claims.get(name)
            if old is None:
                skipped[name] = "not claimed"
            elif old.holder != me and not force:
                skipped[name] = f"held by {old.describe()}; release another curator's claim with --force"
            else:
                changes[name] = None
                if old.holder != me:
                    forced.append(f"{name} of {old.holder}")
        message = f"release: {_list_for_message(changes)} ({me})"
        if forced:
            message += f"; forced: {', '.join(forced)}"
        return changes, skipped, message

    return _update(repo, decide)


def renew(
    names: Iterable[str] | None = None,
    *,
    ttl_days: float = DEFAULT_TTL_DAYS,
    holder: str | None = None,
    repo: str | Path | None = None,
) -> Outcome:
    """Push the expiry of the current curator's claims (all of them, or ``names``) ``ttl_days`` from now."""
    me = holder or current_curator(repo)
    wanted = _names(names) if names is not None else None

    def decide(board: Board) -> Decision:
        expires = _iso(_utcnow() + dt.timedelta(days=ttl_days))
        targets = wanted if wanted is not None else [c.name for c in board.claims.values() if c.holder == me]
        changes: dict[str, Claim | None] = {}
        skipped: dict[str, str] = {}
        for name in targets:
            old = board.claims.get(name)
            if old is None or old.holder != me:
                skipped[name] = "not yours" if old else "not claimed"
            else:
                changes[name] = replace(old, expires_at=expires)
        return changes, skipped, f"renew: {_list_for_message(changes)} ({me}, until {expires[:10]})"

    return _update(repo, decide)


def init_branch(repo: str | Path | None = None, *, pages_dispatch: bool = False) -> Outcome:
    """Create the claims branch when it is missing (README only), optionally with the Pages dispatch workflow.

    The workflow (:data:`PAGES_DISPATCH_WORKFLOW`) runs on GitHub on every push to the claims branch and asks the
    ``pages.yaml`` workflow of ``main`` to rebuild the read-only dashboard, so its Claimed by column follows the board.
    """
    if not pages_dispatch:
        board = fetch(repo)
        if board.tip is not None:
            return Outcome([], {}, board)

    def decide(_board: Board) -> Decision:
        return {}, {}, "init: the claims board" + (" and the Pages dispatch" if pages_dispatch else "")

    return _update(repo, decide, {PAGES_DISPATCH_PATH: PAGES_DISPATCH_WORKFLOW} if pages_dispatch else {})


# -- the records' mirror ----------------------------------------------------------------------------------------------


def wip_status(stage: str, suggestion: str | None) -> str:
    """The record's WIP value for a claim: ``WIP (DF)`` for work on an accepted dataset, else ``WIP (Triage)``."""
    from data_foundry.curation.record import ACCEPTED_SUGGESTIONS  # noqa: PLC0415

    return "WIP (DF)" if stage != "triage" and suggestion in ACCEPTED_SUGGESTIONS else "WIP (Triage)"


def mirror_to_records(
    board: Board,
    names: Iterable[str] | None = None,
    directory: str | Path | None = None,
    *,
    write: bool = True,
) -> dict[str, tuple[str | None, str | None]]:
    """Make the records' ``claimed_by`` and WIP value match the board.

    A record with a live or expired claim gets the holder and the WIP value of :func:`wip_status`; a record that
    carries a claim or a WIP value the board does not have loses both. Records are reloaded right before each write.

    Args:
        board: The board to mirror.
        names: Only these records (default: every record).
        directory: The records directory (defaults to the standard one).
        write: ``False`` only reports what would change.

    Returns:
        ``{name: (claimed_by before, claimed_by after)}`` for every record that differs (or differed).
    """
    from data_foundry.curation.record import WIP_STATUSES, load_vocabularies  # noqa: PLC0415
    from data_foundry.curation.store import load_record, save_record  # noqa: PLC0415 - store imports this module

    target = Path(directory) if directory is not None else records_dir()
    if names is None:
        paths = [p for p in sorted(target.glob("*.md")) if not p.name.startswith("_")]
    else:
        paths = [target / f"{n}.md" for n in _names(names)]
    vocab = load_vocabularies() if write else {}
    changed: dict[str, tuple[str | None, str | None]] = {}
    for path in paths:
        if not path.exists():
            continue
        record = load_record(path)
        claim = board.claims.get(record.unique_name)
        status = list(record.data_foundry_status or [])
        has_wip = any(s in WIP_STATUSES for s in status)
        if claim is None and not record.claimed_by and not has_wip:
            continue
        kept = [s for s in status if s not in WIP_STATUSES]
        if claim is None:
            want_status, want_holder = kept, None
        else:
            wip = wip_status(claim.stage, record.suggestion)
            at = next((i for i, s in enumerate(status) if s in WIP_STATUSES), len(kept))
            want_status, want_holder = [*kept[:at], wip, *kept[at:]], claim.holder
        if want_status == status and want_holder == record.claimed_by:
            continue
        changed[record.unique_name] = (record.claimed_by, want_holder)
        if write:
            record.data_foundry_status = want_status
            record.claimed_by = want_holder
            record.needs_review = record.review_reasons(vocab)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ClaimWarning)
                save_record(record, target)
    return changed


def import_from_records(
    directory: str | Path | None = None,
    *,
    ttl_days: float = DEFAULT_TTL_DAYS,
    repo: str | Path | None = None,
) -> Outcome:
    """Put every claim the records carry (``claimed_by``) on the board, in its holder's name; existing ones stay."""
    from data_foundry.curation.store import load_all  # noqa: PLC0415

    held = [r for r in load_all(directory) if r.claimed_by]

    def decide(board: Board) -> Decision:
        now = _utcnow()
        expires = _iso(now + dt.timedelta(days=ttl_days))
        changes: dict[str, Claim | None] = {}
        skipped: dict[str, str] = {}
        for record in held:
            old = board.claims.get(record.unique_name)
            if old is not None:
                skipped[record.unique_name] = f"already on the board: {old.describe()}"
                continue
            stage = "triage" if "WIP (Triage)" in (record.data_foundry_status or []) else "add"
            changes[record.unique_name] = Claim(record.unique_name, record.claimed_by, stage, _iso(now), expires, "")
        holders = sorted({c.holder for c in changes.values() if c})
        return changes, skipped, f"import: {len(changes)} claim(s) from the records ({', '.join(holders)})"

    return _update(repo, decide)


# -- warnings ---------------------------------------------------------------------------------------------------------


def warn_if_claimed(name: str, repo: str | Path | None = None) -> Claim | None:
    """Warn (:class:`ClaimWarning`) when the cached board shows ``name`` held by another curator.

    Reads only the cache of the last fetch, never the network, and stays silent when there is no cache or no curator
    name. Returns the other curator's claim, if any.
    """
    try:
        board = cached_board(repo)
        claim = board.claims.get(name) if board is not None else None
        if claim is None or claim.expired():
            return None
        me = configured_curator(repo)
        if me is None or claim.holder == me:
            return None
    except Exception:  # noqa: BLE001 - a warning must never break a write
        return None
    warnings.warn(
        ClaimWarning(f"{name} is claimed by {claim.describe()}; leave it to them or talk to them first."),
        stacklevel=3,
    )
    return claim
