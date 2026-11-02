"""Tests of the live claims board: a local bare repository plays the remote, two clones play two curators."""

from __future__ import annotations

import datetime as dt
import http.client
import json
import os
import subprocess
import sys
import threading
import warnings
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
import yaml
from data_foundry.curation import claims
from data_foundry.curation._paths import DATA_FOUNDRY_CURATION_ENV
from data_foundry.curation.app import CurationHandler
from data_foundry.curation.cli import main as cli_main
from data_foundry.curation.record import CurationRecord
from data_foundry.curation.store import load_record, save_record

HOOK = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "claims_hook.py"


def git(repo: Path, *args: str) -> str:
    """Run git in ``repo`` and return its output."""
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True)  # noqa: S603, S607
    return out.stdout.strip()


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    """A bare remote, two clones (Lennart's and Andrej's) and a curation root inside Lennart's clone."""
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "gitconfig"))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for key in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
        monkeypatch.setenv(key, "Tester")
    for key in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
        monkeypatch.setenv(key, "tester@example.org")
    for key in (claims.CURATOR_ENV, claims.CLAIMS_REMOTE_ENV, claims.CLAIMS_BRANCH_ENV):
        monkeypatch.delenv(key, raising=False)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)  # noqa: S603, S607
    repos = {}
    for who in ("lennart", "andrej"):
        repo = tmp_path / who
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "remote", "add", "origin", str(remote))
        repos[who] = repo
    root = repos["lennart"] / "curation"
    (root / "records").mkdir(parents=True)
    (root / "vocabularies.yaml").write_text(yaml.safe_dump({"claimed_by": ["Lennart", "Andrej"]}))
    monkeypatch.setenv(DATA_FOUNDRY_CURATION_ENV, str(root))
    claims._CACHE_MEMO.clear()
    return {"remote": remote, "root": root, **repos}


def _record(root: Path, name: str, **fields: object) -> None:
    save_record(CurationRecord(unique_name=name, name=name, **fields), root / "records")


def test_claim_list_release_round_trip(env: dict[str, Path]) -> None:
    """A claim lands on the branch with its file and README row; a release removes it."""
    out = claims.claim(["a", "b"], stage="add", note="batch 1", holder="Lennart", repo=env["lennart"])
    assert out.changed == ["a", "b"]
    assert not out.skipped
    board = claims.fetch(env["andrej"])
    assert set(board.claims) == {"a", "b"}
    assert board.claims["a"].holder == "Lennart"
    assert board.claims["a"].note == "batch 1"
    readme = git(env["remote"], "show", "claims:README.md")
    assert "## Lennart" in readme
    assert "| `a` | add |" in readme
    assert "batch 1" in readme
    assert claims.release(["a"], holder="Lennart", repo=env["lennart"]).changed == ["a"]
    assert set(claims.fetch(env["andrej"]).claims) == {"b"}
    assert "release: a (Lennart)" in git(env["remote"], "log", "-1", "--format=%s", "claims")


def test_claim_held_by_another_is_skipped_and_release_needs_force(env: dict[str, Path]) -> None:
    """Another curator's claim is skipped, and released only with force (logged)."""
    claims.claim(["a"], stage="triage", holder="Andrej", repo=env["andrej"])
    out = claims.claim(["a", "b"], stage="add", holder="Lennart", repo=env["lennart"])
    assert out.changed == ["b"]
    assert "Andrej (triage)" in out.skipped["a"]
    assert claims.release(["a"], holder="Lennart", repo=env["lennart"]).changed == []
    forced = claims.release(["a"], force=True, holder="Lennart", repo=env["lennart"])
    assert forced.changed == ["a"]
    assert "forced: a of Andrej" in git(env["remote"], "log", "-1", "--format=%s", "claims")


def test_renewing_keeps_since_and_note(env: dict[str, Path]) -> None:
    """Claiming again renews: the start date and note stay, stage and expiry move."""
    claims.claim(["a"], stage="add", note="first", ttl_days=1, holder="Lennart", repo=env["lennart"])
    before = claims.fetch(env["lennart"]).claims["a"]
    claims.claim(["a"], stage="review", ttl_days=10, holder="Lennart", repo=env["lennart"])
    after = claims.fetch(env["lennart"]).claims["a"]
    assert after.claimed_at == before.claimed_at
    assert after.note == "first"
    assert after.stage == "review"
    assert after.expires_at > before.expires_at
    renewed = claims.renew(ttl_days=20, holder="Lennart", repo=env["lennart"])
    assert renewed.changed == ["a"]


def test_expired_claim_is_taken_only_with_steal(env: dict[str, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """An expired claim of another curator is taken over only with steal, and the log names them."""
    claims.claim(["a"], stage="add", ttl_days=1, holder="Andrej", repo=env["andrej"])
    later = claims._utcnow() + dt.timedelta(days=2)
    monkeypatch.setattr(claims, "_utcnow", lambda: later)
    refused = claims.claim(["a"], stage="add", holder="Lennart", repo=env["lennart"])
    assert refused.changed == []
    assert "--steal" in refused.skipped["a"]
    taken = claims.claim(["a"], stage="add", steal=True, holder="Lennart", repo=env["lennart"])
    assert taken.changed == ["a"]
    assert claims.fetch(env["andrej"]).claims["a"].holder == "Lennart"
    assert "taken over: a from Andrej" in git(env["remote"], "log", "-1", "--format=%s", "claims")


def test_race_on_the_same_dataset_has_one_winner(env: dict[str, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """Both curators read the same tip; Andrej's push lands first, Lennart's is rejected and sees the claim."""
    real_fetch = claims.fetch
    raced = []

    def racing_fetch(repo: Path | None = None) -> claims.Board:
        board = real_fetch(repo)
        if Path(repo) == env["lennart"] and not raced:
            raced.append(True)
            claims.claim(["x"], stage="add", holder="Andrej", repo=env["andrej"])
        return board  # Lennart decides on the stale board

    monkeypatch.setattr(claims, "fetch", racing_fetch)
    out = claims.claim(["x"], stage="add", holder="Lennart", repo=env["lennart"])
    assert out.changed == []
    assert "Andrej" in out.skipped["x"]
    assert real_fetch(env["andrej"]).claims["x"].holder == "Andrej"


def test_race_on_different_datasets_both_land(env: dict[str, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """A push that lost the race to a claim on another dataset retries and lands."""
    real_fetch = claims.fetch
    raced = []

    def racing_fetch(repo: Path | None = None) -> claims.Board:
        board = real_fetch(repo)
        if Path(repo) == env["lennart"] and not raced:
            raced.append(True)
            claims.claim(["x"], stage="add", holder="Andrej", repo=env["andrej"])
        return board

    monkeypatch.setattr(claims, "fetch", racing_fetch)
    out = claims.claim(["y"], stage="add", holder="Lennart", repo=env["lennart"])
    assert out.changed == ["y"]
    board = real_fetch(env["andrej"])
    assert {n: c.holder for n, c in board.claims.items()} == {"x": "Andrej", "y": "Lennart"}


def test_board_is_cached_and_offline_reads_need_no_remote(env: dict[str, Path]) -> None:
    """Each fetch caches the board in the git directory; nothing touches the working tree."""
    claims.claim(["a"], stage="add", holder="Lennart", repo=env["lennart"])
    assert claims.cached_board(env["lennart"]).claims["a"].holder == "Lennart"
    assert claims.cached_board(env["andrej"]) is None  # Andrej has not fetched yet
    assert claims.load(env["andrej"], max_age=60).claims["a"].holder == "Lennart"
    assert claims.cached_board(env["andrej"]) is not None
    cache = json.loads((env["lennart"] / ".git" / claims.CACHE_NAME).read_text())
    assert cache["branch"] == "claims"
    # The working tree and the checked-out branch are never touched.
    assert git(env["lennart"], "status", "--porcelain") == "?? curation/"


def test_missing_branch_is_an_empty_board_and_init_creates_it(env: dict[str, Path]) -> None:
    """No branch reads as an empty board; init creates it, and its extra files survive later commits."""
    assert claims.fetch(env["lennart"]).tip is None
    claims.init_branch(env["lennart"])
    assert claims.fetch(env["andrej"]).tip is not None
    claims.init_branch(env["lennart"], pages_dispatch=True)
    workflow = git(env["remote"], "show", f"claims:{claims.PAGES_DISPATCH_PATH}")
    assert "gh workflow run pages.yaml" in workflow
    claims.claim(["a"], stage="add", holder="Lennart", repo=env["lennart"])
    assert git(env["remote"], "show", f"claims:{claims.PAGES_DISPATCH_PATH}") == workflow  # kept by later commits


def test_current_curator_needs_a_known_name(env: dict[str, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """The curator name comes from git config or the environment and must be in the vocabulary."""
    with pytest.raises(claims.ClaimsError, match="Name yourself"):
        claims.current_curator(env["lennart"])
    git(env["lennart"], "config", claims.CURATOR_GIT_KEY, "Lennart")
    assert claims.current_curator(env["lennart"]) == "Lennart"
    monkeypatch.setenv(claims.CURATOR_ENV, "Mallory")
    with pytest.raises(claims.ClaimsError, match="not in vocabularies"):
        claims.current_curator(env["lennart"])


def test_mirror_sets_and_clears_the_records_claims(env: dict[str, Path]) -> None:
    """The records' claimed_by and WIP value follow the board, both ways."""
    root = env["root"]
    _record(root, "a", suggestion="Yes")
    _record(root, "b", suggestion="TBD -> Yes")
    _record(root, "c", suggestion="Yes", claimed_by="Andrej", data_foundry_status=["WIP (DF)", "BeyondArena"])
    claims.claim(["a", "b"], stage="add", holder="Lennart", repo=env["lennart"])
    board = claims.fetch(env["lennart"])
    assert set(claims.mirror_to_records(board, write=False)) == {"a", "b", "c"}
    changed = claims.mirror_to_records(board)
    assert changed == {"a": (None, "Lennart"), "b": (None, "Lennart"), "c": ("Andrej", None)}
    a, b, c = (load_record(root / "records" / f"{n}.md") for n in "abc")
    assert (a.claimed_by, a.data_foundry_status) == ("Lennart", ["WIP (DF)"])
    assert b.data_foundry_status == ["WIP (Triage)"]  # work on a record whose verdict is still open
    assert (c.claimed_by, c.data_foundry_status) == (None, ["BeyondArena"])
    assert not {"wip_unclaimed", "claim_without_wip"} & set(a.needs_review + c.needs_review)
    assert claims.mirror_to_records(board) == {}


def test_import_from_records(env: dict[str, Path]) -> None:
    """The records' claims move onto the board in their holders' names, once."""
    root = env["root"]
    _record(root, "a", suggestion="Yes", claimed_by="Lennart", data_foundry_status=["WIP (DF)"])
    _record(root, "b", suggestion="TBD -> Yes", claimed_by="Andrej", data_foundry_status=["WIP (Triage)"])
    out = claims.import_from_records(repo=env["lennart"])
    assert out.changed == ["a", "b"]
    board = claims.fetch(env["andrej"])
    assert (board.claims["a"].holder, board.claims["a"].stage) == ("Lennart", "add")
    assert (board.claims["b"].holder, board.claims["b"].stage) == ("Andrej", "triage")
    assert claims.import_from_records(repo=env["lennart"]).changed == []


def test_save_record_warns_only_on_another_curators_claim(
    env: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """save_record warns on another curator's claim, writes anyway, and is silent otherwise."""
    root = env["root"]
    claims.claim(["a"], stage="add", holder="Andrej", repo=env["lennart"])
    claims.claim(["b"], stage="add", holder="Lennart", repo=env["lennart"])
    monkeypatch.setenv(claims.CURATOR_ENV, "Lennart")
    with pytest.warns(claims.ClaimWarning, match="a is claimed by Andrej"):
        _record(root, "a")
    with warnings.catch_warnings():
        warnings.simplefilter("error", claims.ClaimWarning)
        _record(root, "b")  # mine
        _record(root, "c")  # free
        save_record(CurationRecord(unique_name="a", name="a"), env["andrej"])  # not the records directory
    assert (root / "records" / "a.md").exists()  # advisory: the write happened


def _hook(payload: dict[str, object]) -> dict[str, object] | None:
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
        env=os.environ,
    )
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def test_hook_warns_before_editing_a_dataset_someone_else_holds(
    env: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The hook warns (never decides) on another curator's dataset and lists the board at session start."""
    repo = env["lennart"]
    claims.claim(["a"], stage="add", holder="Andrej", repo=repo)
    claims.claim(["b"], stage="add", holder="Lennart", repo=repo)
    monkeypatch.setenv(claims.CURATOR_ENV, "Lennart")

    def edit(path: str) -> dict[str, object] | None:
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Edit", "cwd": str(repo)}
        return _hook({**payload, "tool_input": {"file_path": str(repo / path)}})

    out = edit("curation/records/a.md")
    assert "claimed by Andrej" in out["systemMessage"]
    assert "permissionDecision" not in out["hookSpecificOutput"]  # warn only, never allow or deny
    assert "claimed by Andrej" in out["hookSpecificOutput"]["additionalContext"]
    assert "Andrej" in edit("datasets/_dev/tabarena-v0pt2/a/dataset.py")["systemMessage"]
    assert edit("curation/records/b.md") is None
    assert edit("datasets/_dev/tabarena-v0pt2/c/REVIEW.md") is None
    assert edit("src/data_foundry/curation/claims.py") is None

    start = _hook({"hook_event_name": "SessionStart", "cwd": str(repo)})
    context = start["hookSpecificOutput"]["additionalContext"]
    assert "Andrej (1): a" in context
    assert "Yours (1): b" in context


def test_hook_fails_open(tmp_path: Path) -> None:
    """Without a board or a known event the hook prints nothing."""
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Edit", "cwd": str(tmp_path)}
    assert _hook({**payload, "tool_input": {"file_path": str(tmp_path / "curation/records/a.md")}}) is None
    assert _hook({"hook_event_name": "Nonsense"}) is None


def test_cli_claim_check_and_sync(
    env: dict[str, Path], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The CLI claims, checks, syncs and releases, and turns a missing name into one error line."""
    root, repo = env["root"], env["lennart"]
    _record(root, "a", suggestion="Yes")
    monkeypatch.setenv(claims.CURATOR_ENV, "Lennart")
    monkeypatch.setattr(claims, "repo_root", lambda: repo)
    assert cli_main(["claims", "claim", "a", "--note", "testing"]) == 0
    assert load_record(root / "records" / "a.md").claimed_by == "Lennart"
    assert cli_main(["claims", "claim", "nope"]) == 2  # no record
    assert cli_main(["claims", "check", "a", "z"]) == 0
    out = capsys.readouterr().out
    assert "a: yours" in out
    assert "z: free" in out
    assert cli_main(["claims", "sync", "--check"]) == 0
    assert cli_main(["claims", "release", "a"]) == 0
    assert load_record(root / "records" / "a.md").claimed_by is None
    monkeypatch.delenv(claims.CURATOR_ENV)
    assert cli_main(["claims", "claim", "a"]) == 2  # no curator name: one error line, no traceback
    assert "Name yourself" in capsys.readouterr().err


def test_dashboard_claims_and_releases_through_the_board(env: dict[str, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """The dashboard shows the board's holder, claims and releases through it, and refuses another's dataset."""
    root, repo = env["root"], env["lennart"]
    _record(root, "a", suggestion="Yes")
    _record(root, "b", suggestion="TBD -> Yes")
    claims.claim(["b"], stage="triage", holder="Andrej", repo=env["andrej"])
    claims.fetch(repo)
    monkeypatch.setenv(claims.CURATOR_ENV, "Lennart")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(CurationHandler, directory=root / "records"))
    threading.Thread(target=server.serve_forever, daemon=True).start()

    def call(method: str, path: str, body: dict[str, object] | None = None) -> tuple[int, object]:
        conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=30)
        conn.request(method, path, body=json.dumps(body) if body is not None else None)
        res = conn.getresponse()
        return res.status, json.loads(res.read())

    try:
        rows = {r["unique_name"]: r for r in call("GET", "/api/records")[1]}
        assert rows["b"]["claimed_by"] == "Andrej"  # from the board, not the record
        assert rows["b"]["live_claim"]["stage"] == "triage"
        assert rows["a"]["claimed_by"] is None
        assert call("GET", "/api/claims")[1]["me"] == "Lennart"
        status, row = call("POST", "/api/claims/a", {"action": "claim"})
        assert status == 200
        assert (row["claimed_by"], row["live_claim"]["stage"]) == ("Lennart", "add")
        assert load_record(root / "records" / "a.md").data_foundry_status == ["WIP (DF)"]
        assert claims.fetch(env["andrej"]).claims["a"].holder == "Lennart"
        status, err = call("POST", "/api/claims/b", {"action": "claim"})
        assert status == 409
        assert "Andrej" in err["error"]
        assert call("POST", "/api/claims/a", {"action": "release"})[1]["claimed_by"] is None
        assert load_record(root / "records" / "a.md").claimed_by is None
    finally:
        server.shutdown()
