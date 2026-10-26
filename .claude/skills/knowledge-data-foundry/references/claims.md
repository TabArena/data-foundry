# Claims: who works on which dataset

Several curators, each running several agents, work on the same records and folders, and git shows their work only
when it reaches `main`. A claim says "I am working on this dataset now", and every curator and agent sees it within
seconds. A claim covers one dataset: its record `curation/records/<name>.md` and its folder
`datasets/_dev/tabarena-v0pt2/<name>/` with `REVIEW.md`. Shared files (CHANGELOG, the README table, the vocabulary)
are never claimed; their conflicts are resolved when merging.

## How it works

* **The board** is the branch `claims` of the repository's remote. It holds one file `claims/<name>.yaml` per claimed
  dataset (holder, stage, since, until, note) and a `README.md` table. That table is the team's view on GitHub:
  <https://github.com/TabArena/data-foundry/blob/claims/README.md>.
* **A claim is a commit pushed straight to that branch**, with no pull request and no CI. Two claims of the same
  dataset at the same moment cannot both land: git rejects the second push, and the command fetches again, sees the
  claim and skips the dataset. Nothing touches your working tree or your branch.
* **Login is the repository's.** Whoever can push to the repository can claim, and whoever can read it sees the
  board. Nothing else to sign up for or host. The code (`src/data_foundry/curation/claims.py`) works with any git
  remote: `$DATA_FOUNDRY_CLAIMS_REMOTE` (default `origin`) and `$DATA_FOUNDRY_CLAIMS_BRANCH` (default `claims`).
* **Stages:**
  * `triage`: screening, a check, or settling an open verdict;
  * `add`: building the v2 folder;
  * `review`: the curator's review of an added dataset.
* **Expiry.** A claim lasts 7 days unless renewed. After that it shows as expired, and anyone may take it over with
  `--steal`; the board's log names the previous holder.
* **Claims are advisory.** Nothing refuses a write. Warnings appear in three places:
  * `save_record` warns (`ClaimWarning`) when it writes a record another curator holds;
  * the Claude Code hook warns before an agent edits such a file;
  * the dashboard shows the holder.

  A warning means: stop and ask the curator, or the holder.
* **The records mirror the board.** `claimed_by` and the WIP value (`WIP (Triage)` for triage or an open verdict,
  `WIP (DF)` for work on an accepted dataset) are written by `claims claim` and `claims release`. They travel with the
  work branch and reach `main` with the work. The board is the truth: the old rule of pushing the claim to `main` in
  its own PR is gone.

## Setup, once per curator

```bash
git config data-foundry.curator <Name>     # a claimed_by value of curation/vocabularies.yaml
.venv/bin/python -m data_foundry.curation.cli claims list
```

`claims list` works when `git fetch` from the remote works. On a machine whose ssh agent went stale, prefix the
commands with `env SSH_AUTH_SOCK=`. The git calls never prompt: a missing credential fails at once with a hint.

## Commands

`data-foundry-curation claims ...` (or `.venv/bin/python -m data_foundry.curation.cli claims ...`):

| Command | What it does |
|---|---|
| `list [--mine\|--others] [--json] [--offline]` | Fetches and shows the board. |
| `check <names>` | Says per dataset: free, yours, or held by someone (always exit 0). |
| `claim <names> [--stage S] [--note TEXT] [--ttl DAYS] [--steal]` | Claims what is free and skips the rest. Exit 1 when anything was skipped. Stage default: `add` for an accepted record, else `triage`. A name with no record is refused unless `--allow-unknown`. Claiming your own claim again renews it. |
| `release <names> [--force]` | Releases your claims; `--force` releases someone else's (logged). |
| `renew [<names>] [--ttl DAYS]` | Extends your claims (all of them by default). |
| `sync [--check]` | Makes every record's `claimed_by` and WIP value match the board. |
| `import-records` | One-time: moves the claims the records carry onto the board. |
| `init [--pages-dispatch]` | Creates the branch. `--pages-dispatch` adds `.github/workflows/claims-to-pages.yaml` to it, so each claim rebuilds the public dashboard. |

From Python: `claims.claim(...)`, `claims.release(...)`, `claims.load(max_age=30)`, `claims.cached_board()`.

## In the workflows

* **Before working on records** (screening, adding, a re-check, a review round), run `claims claim <names> --note
  "<what>"` once for the whole batch. Work only on the names it claimed. A skipped name belongs to someone else: leave
  it out and report it.
* **For a long job**, `claims renew`.
* **When the work reaches `main`, or is dropped,** `claims release <names>`.
* **Batch filters** use the board (`claims list --json`), not the record's `claimed_by`, which can lag behind.
* **Hand edits:** the dashboard's Claimed by column shows the board. Pick your own name in a cell to claim, empty it to
  release. The 🔒 count in the bar says when the board was fetched.

## The Claude Code hook

`.claude/settings.json` runs `.claude/hooks/claims_hook.py` with the repository's `.venv` at two points:

* **At session start**, it adds the board to the agent's context: the other curators' claims, yours, and yours that
  expire within 2 days.
* **Before each Edit, Write or NotebookEdit** of a claimed dataset's record or folder, it shows a warning when another
  curator holds the dataset.

It never allows or denies a tool call. It re-fetches the board at most once a minute, and it does nothing without the
package, a curator name or the network.

## The public dashboard

The GitHub Pages workflow fetches the board before it builds, so the read-only dashboard's Claimed by column shows
the claims. With `claims init --pages-dispatch`, each push to the board dispatches the Pages workflow on `main`, and
the page follows within a minute or two. Without it, the page updates with the next push to `main`.

## When something is off

* **A record says `claimed_by` but the board does not** (or the reverse): `claims sync --check` lists the drift and
  `claims sync` fixes the records.
* **"The claims branch kept moving"**: five pushes in a row lost a race. Run the command again.
* **The board's log** shows every claim and release: `git log origin/claims`.
