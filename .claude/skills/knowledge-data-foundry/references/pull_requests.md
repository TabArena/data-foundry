# Pull requests

How an agent writes, stacks and merges a pull request in this repository. Opening, pushing and merging a PR still need
the curator's ask (the house rules in [SKILL.md](../SKILL.md)). Lennart set these rules on 2026-11-11, after agent PRs
had grown to bodies of 3,000 to 20,000 characters with nothing at the top that said what to review, and after a chain
of ten PRs (#55 to #81) had stacked mostly unrelated retirements on top of each other. They adapt Sentry's
[`pr-writer`](https://github.com/getsentry/skills/blob/main/skills/pr-writer/SKILL.md) and Kiln's
[`open-pr`](https://github.com/Kiln-AI/Kiln/blob/main/.agents/skills/open-pr/SKILL.md) skills, Google's
[CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) and GitHub's
[stacked pull requests](https://docs.github.com/en/pull-requests/get-started/about-stacked-prs).

The style rules of [AGENTS.md](../../../../AGENTS.md#ai-writing-tropes-to-avoid) apply to titles and bodies like any
other prose: no em dashes, no bold-first bullets, no inflated words.

## The title

One line that names what changes, in the curator's words: the datasets, the rule or the API. Keep it under about 70
characters, with no trailing period and no type prefix. "Retire three generated datasets" or "Families of definitions:
tasks derived from a parent" work; "Update records" or "Address review feedback" say nothing. Issue numbers go in the
body.

## The body: a summary on top, the details folded

The reviewer, often a curator rather than a programmer, decides from the top of the body whether and how to review.
The part above the first `<details>` section fits on one screen (about 200 words) and holds, in this order:

1. What changes and why, in one to three sentences of plain prose. Describe the effect on the datasets, the data or
   the package, not the edited files. When the PR applies a curator's decision, name the curator and the date
   (Andrej, 2026-11-10).
2. What the reviewer has to decide or check. List each open question with its options and the recommendation, or
   name the one thing to look at (a changed split, a dropped column, the wording of a new rule). For an open question
   about a dataset, link its `REVIEW.md` instead of copying it. A PR that only applies decisions already taken says
   so: "Nothing to decide: applies Andrej's marks on the review page."
3. What to know before merging, only when there is something: the PR it depends on and why, the merge order, a
   re-check or rebuild that has to follow, every container checksum changing. Say whether any container was built.

Everything else goes below, in folded sections, each with a summary line that names its content:

* the changes, grouped by area (definitions, records, knowledge files, code), one bullet for each change the diff
  does not make obvious;
* the evidence: tables, probe and model scores, the analysis behind a decision;
* the checks that ran (`pytest -q`, ruff on the changed files, `validate`, `dataset check`), one line each;
* the decisions taken in review (who, when, what), and examples or code.

Leave out what the diff or another file already holds: lists of every file, the commit history, command output and
logs, copies of a `REVIEW.md` or of a record's comments. Leave out private data and the names of company code
repositories (house rules).

A small PR (one record, a typo, a one-line fix) is one paragraph with no sections. Fixed headings on every PR teach
the reviewer to skip them. A larger PR follows this shape:

````markdown
<What changes and why, in one to three sentences.>

To decide:
- <the question, its options, the recommendation; or "Nothing to decide: ...">

Before merging: <depends on #N because ...; the re-check that has to follow>. No container built.

<details>
<summary>Changes</summary>

- ...

</details>

<details>
<summary>Evidence: scores on the 9 shipped splits</summary>

| Method | ROC AUC |
|---|---|

</details>

<details>
<summary>Checks</summary>

- `pytest -q`: 2499 passed, 303 skipped.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
````

The body ends with the attribution line the session gives. The repository's template,
[`.github/pull_request_template.md`](../../../../.github/pull_request_template.md), has the same shape; GitHub fills
it in for a PR opened on the web. An agent writes the body to a file in that shape and does not leave the template's
placeholders in it.

### Markdown and `gh` mechanics

* Write the body to a file in the scratchpad and pass it with `--body-file` (`gh pr create`, `gh pr edit`). Shell
  quoting and `\n` escapes then cannot break the markdown.
* GitHub renders markdown inside `<details>` only with a blank line after `</summary>` and before `</details>`.
  Keep the `<summary>` text plain, since markdown inside it does not render reliably (use `<code>` there). Do not
  indent the content by four spaces, or it turns into a code block. A section inside a section works.
* GitHub refuses a body over 65,536 characters. Put longer evidence in a comment on the PR.
* `Closes #N` only when merging the PR settles issue N; otherwise `Refs #N`.
* Open the PR as a draft (`--draft`) while work on it is still running, and mark it ready (`gh pr ready <n>`) once
  the summary is final.

### Keeping the body current

When later commits change what the PR does, rewrite the top part so that it describes the PR as it is now
(`gh pr edit <n> --body-file <file>`). The history of review rounds does not go on top. A decision taken in review goes
into the summary as a decision (who and when), and its details go into a folded "Decided in review" section.

## One change, one PR against `main`

A PR starts from the current `origin/main` and targets `main`. Changes that do not need each other get separate PRs,
each against `main`, even when one session made them on the same day: two retirements, a rule edit and an unrelated
dataset, a fix and a feature. Each can then be reviewed and merged on its own, in any order.

An independent PR is brought up to date when it is about to be merged, not after every merge to `main`:

```bash
git fetch origin
git switch <branch>
git rebase origin/main        # or `git merge origin/main` when someone else also works on the branch
# resolve conflicts, then run pytest -q, ruff on the changed files and data-foundry-curation validate
git push --force-with-lease origin <branch>
```

A conflict in a shared file (`CHANGELOG.md`, the cases table of a knowledge file, a vocabulary) is resolved at that
point by keeping both sides. A shared file is no reason to stack.

In the chain of ten PRs from #55 to #81 (November 2026), most retired unrelated datasets, yet each waited for all the
PRs below it. Reordering the chain merged #60 into its parent branch instead of `main`. GitHub shows it as merged,
but its change never reached `main` and had to be opened again as #79. The same happened to #49, which landed again
as #72.

## Stacked PRs: only for a dependency

Stack a PR on another only when it needs that PR's unmerged change: it calls a function the other adds, edits a file
the other creates, or applies a rule the other introduces. To test it, ask whether this PR's diff against `main`
would be correct and pass the tests without the other PR. If it would, the PR goes against `main`.

Make the stack a GitHub stack, not only a chain of base branches. GitHub then shows the stack map on every PR, and
each PR's diff shows only its own layer. Merging the bottom PR rebases and retargets the ones above. Stacked PRs have
been generally available since 2026-10-06 and need no setup in the repository. The `gh stack` extension drives them
(`gh extension install github/gh-stack`, or `gh extension upgrade stack` to update it). #65 (#63 on top of #64)
was such a stack.

### Creating a stack

Each PR gets its own title and body, so open the PRs with `gh pr create` and then link them into a stack:

```bash
git fetch origin
git switch -c <part-a> origin/main               # commit part A
git push -u origin <part-a>
gh pr create --base main --head <part-a> --title "..." --body-file a.md
git switch -c <part-b> <part-a>                  # commit part B on top of A
git push -u origin <part-b>
gh pr create --base <part-a> --head <part-b> --title "..." --body-file b.md
gh stack link <A> <B>                            # PR numbers, bottom to top: GitHub shows them as one stack
gh stack init <part-a> <part-b>                  # track the same branches locally, for rebase and sync
```

`gh stack submit` can open the PRs too. Without a terminal it gives them generated titles and opens them as drafts,
so their titles and bodies then need `gh pr edit`.

Each PR in a stack says at the top which PR it depends on and why ("Depends on #73: uses its `NonFeature`."). The
stack map shows the order, so the body needs no list of the stack. When a lower layer changes, `gh stack rebase`
rebases the layers above and `gh stack push` pushes them; `gh stack sync` fetches, rebases and pushes in one step.

### Merging a stack

* Merge from the bottom up, in the stack's merge box on GitHub or with `gh stack merge <PR> --squash`. `gh pr merge`
  refuses a PR that is part of a stack. Merging a PR also merges every PR below it, in one step.
* GitHub then rebases the PRs above onto `main` and retargets them. `gh stack sync` brings the local branches along.
* Never merge a PR into its parent branch. The parent then carries the child's commits, and the child shows as
  merged although nothing reached `main` (#60, #49).
* For a chain that is not a GitHub stack (older PRs), link it with `gh stack link` before merging. If you merge it
  by hand instead, merge the bottom PR into `main` and retarget the next one (`gh pr edit <B> --base main`) before
  deleting the bottom branch: deleting it first can close the next PR
  ([cli/cli#14223](https://github.com/cli/cli/issues/14223)). After a squash merge, the next branch still carries the
  bottom PR's original commits; drop them with `git rebase --onto origin/main <old tip of A> <part-b>` and
  `git push --force-with-lease`.

### Moving an independent PR off a stack

A PR stacked on another that it does not need moves to `main`:

```bash
git fetch origin
git rebase --onto origin/main origin/<parent-branch> <branch>   # keep only this PR's own commits
git log --oneline origin/main..<branch>                         # check: only this PR's commits are left
git push --force-with-lease origin <branch>
gh pr edit <n> --base main
```

If the parent branch was rebased after this branch started from it, use the commit this branch started from
(`git merge-base <branch> <old parent tip>`) in place of `origin/<parent-branch>`. Then apply the same dependency
test to each PR that was stacked on the moved one, and rebase it onto the PR it needs, or onto `main`. If the PRs were
in a GitHub stack, unlink them first: `gh stack unstack <stack number>` removes the stack (the PRs stay open), and
`gh stack link` builds it again from the PRs that still depend on each other.
