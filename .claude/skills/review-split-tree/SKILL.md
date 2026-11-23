---
name: review-split-tree
description: "Shows the split decision tree (split_tree.md) to a person as a page they can read and review: a pannable node-and-branch tree (questions, answers on the branches, leaves coloured by split family, shared steps as links that open in place, the questions only a person answers marked), the review's issues below it in the dataset review page's shape (problem, options with pros and cons, recommendation, decision, then the turns), with a mark and a note per issue and a note per node saved with the page; then reads the marks back so Claude can answer or apply them. Also draws a draft of a restructured tree beside today's. Use when someone wants to see, review or discuss the split tree, a change to it, or a draft of a new structure, or asks to rebuild or republish such a page."
argument-hint: "[--draft <draft.md>] [--notes <review notes.md>]"
user-invocable: true
---

# Review the split tree

The split tree ([`split_tree.md`](../knowledge-curation/references/split_tree.md)) is the decision tree SPLIT-36
asks every definition to walk: seven collection types that link to five shared steps, about 30 questions and 30
leaves. As nested markdown bullets it is hard to review by reading top to bottom. This skill turns it into a page a
person can read, and turns their review into marks Claude can act on. The page is the same each time; only the inputs
change. The tree is read by `data_foundry.curation.split_tree`, the same reader the tests check the tree's logic with,
so a tree the page draws is a tree the tests accept.

## When

* Someone wants to see the tree, or one collection type's branch of it.
* A change to `split_tree.md` is under review (a PR, a review's findings), or a draft restructures it.
* The page exists and someone asks to rebuild it after the tree or the review notes changed, or to apply their marks.

## Steps

1. **Inputs.** The tree (`split_tree.md` at the commit under review). Optional: a draft in the same grammar (below);
   the review notes, with the issues under a `## Review points` heading in the issue shape (below); an anchors file
   that says which nodes each issue concerns. Keep notes, draft and anchors in the run folder
   (`local-data-warehouse/_runs/<date>_<topic>/`), not in the repository.
2. **Build.** From the repository root:

   ```bash
   .venv/bin/python .claude/skills/review-split-tree/scripts/build_tree_page.py \
       --tree .claude/skills/knowledge-curation/references/split_tree.md --commit "$(git rev-parse --short HEAD)" \
       [--draft <run>/split_tree_draft.md --draft-label "Draft"] \
       [--notes <run>/TREE_IMPROVEMENTS.md --anchors <run>/tree_anchors.json] --out <run>/page
   ```

   The script stops, naming the place, on anything outside the grammar: an answer without an arrow, a question or
   leaf without an ID, a link to a section that does not exist, a leaf without examples or a reach note, an anchor
   that matches no node. Fix the input, not the script; `pytest tests/test_split_tree.py` checks the same tree. It
   prints each issue's state and how many nodes it is pinned to; an issue pinned to nothing shows only in the list
   below the tree.
3. **Publish.** `<run>/page/split_tree_review.html` as an Artifact with `files: {"tree-data.json": <run>/page/...}`
   and `capabilities: {db: {}, user: {scopes: ["profile"]}}` (the marks and notes live in the page's database).
   Republish the same file path to keep the link; on a rebuild only the data file changes.
4. **Look once** before handing over the link: light, dark and a phone width (see "Checking the page" below).
5. **Read the marks back** (`ArtifactData list`, collections `marks` and `notes`) before answering. Each person's
   note goes into the notes file as their turn, `**<Name> (<date>[, <mark>]):** <note, in their words>`; Claude's
   answer follows as `**Answer (AI, <date>):**`. An answer that asks for a choice takes the issue shape again
   (question on the label line, `**Problem:**`, an options table with lowercase letters, `**Recommendation:**`,
   `**Decision:**`); the page shows its options as the new mark buttons. A settled issue ends with
   `**Resolved (<date>, <who>):**`. Then rebuild, republish, and clear or migrate the marks that the new turns
   replace, so a mark never lands on a question it was not given for.

## How the page represents the tree

The aim is that a person can follow any path without reading the markdown, see at once where the tree needs a
person, and find any definition. Keep these when changing the page:

* **A real tree, read left to right.** Each question is a card; its answers are the branches. The answer's words
  sit on the branch, just above the card they lead to (`↳ new items`), so a path reads as question, answer,
  question, answer, leaf. Parents are centred on their children; nothing overlaps; branches fold and unfold
  (`+5` shows how many ends a folded branch hides).
* **One view per part.** An overview (the collection types and their first questions), one view per collection type,
  one per shared step. Views are bookmarkable (`#survey`). The tree is drawn to fit the width on a desktop and kept
  readable on a phone (pan instead of shrinking the text).
* **Leaves by split family, at a glance.** Temporal, Grouped, Random, Retire and Restart each have their own colour;
  the card names the family, the tag and the qualifier, then up to three example definitions. A leaf no definition
  reaches has a dashed border; a definition that departs from its leaf is named on the leaf in red.
* **Shared steps are links, opened where they are used.** A step written once (place, fill-in, order and windows,
  forced, family key) appears as a dashed link card with the time key its link names. "Open here" draws the step's
  tree under the link (the branch into it is dashed), so a path reads end to end; "Go to the step" shows it on its
  own. In the type views the links start open.
* **Who answers.** Each question carries its kind from the annotation (use case, data & docs, measurement); a
  question only a person answers carries a magenta "person decides" chip. Small chips (windows, gap, unit, groups,
  same time, stationarity) name the check of "Checks the steps cite" a question or leaf applies; the node's panel
  shows that check's text.
* **Details on demand, path always visible.** Clicking a node opens a panel over the tree: the path as a breadcrumb,
  the node's ID (`FILL.units`, `L-FILL.unit`; a link's ID is its question's and the answer's number), the full
  question and what it reads, every answer with where it leads, examples, departures, the review points that touch
  it, and a note field.
* **The review is pinned to the tree.** Each issue's chip (`T3`) sits on the nodes it concerns; "Show on the tree"
  rings them and dims the rest. Search finds a definition or a word across the tree.
* **The review below the tree, in the review page's shape.** Grouped by state (your turn, open, with others,
  decided). Each issue: the problem in up to three bullets, the rest in a closed "Details" box, the options table
  (option A is the tree as it is, marked "as is"; the recommended row tagged; your pick highlighted), the
  recommendation and the decision, then the turns, then the mark buttons for the question that is open ("As is",
  "Change to: B C", "other", "Discuss") and a note. Decided issues are folded.

## The markdown grammar the reader takes

`split_tree.md` and a draft use the same grammar; `data_foundry.curation.split_tree` reads it and raises on anything
else. A section (`## <name>`) is a collection type (SPLIT-34's seven, in their order), a shared step when its name
ends in "step", or text. A tree section holds:

* Intro paragraphs (a type's one-line defining condition, a step's "Reached when ..."), shown as the section's intro.
* Its first question, a paragraph: `**<question>?** [<ID>] _(<kind>; reads <what it reads>)_`. The kind is one of
  `use case`, `data and documentation`, `measurement` or `person decides`; the ID is `<CODE>.<slug>`, the code the
  same for every question and leaf of the section (`DB.meets`, `FILL.units`).
* Its answers, one bullet each, `- <answer> → <what follows>`, with the next question's answers as sub-bullets two
  spaces in. What follows is a question (as above), a leaf, or a link.
* A leaf: `**<Random|Grouped|Temporal|Retire> · <tag and qualifier>** [L-<CODE>.<slug>]. <body>. Examples: a, b.`
  (at most three) or `... No v0.2 definition reaches it yet.` A random or grouped leaf names its tag in backticks.
* A link: `**<section name>**`, optionally `(<note>; here: a, b)`: the note names the time key the step works on,
  `here:` the definitions that take this link.
* The text sections are `How to walk it`, `Who answers` (it names every person question by ID; the tests check
  that), `Words`, `Overview` (a mermaid chart, not drawn on the page), `Checks the steps cite` (one bullet per named
  check, `* **The <name>** ...`) and `Definitions that ship another split`, whose table
  `| Definition | Leaf | Ships | Reviewer | Date | Reason |` puts each row on its leaf by ID.

## The issue shape and the anchors

An issue in the notes is `### <ID>. <question>?`, then a line `**Merges:** <finding IDs>. **Status:** <status>.`,
then the bullets of the dataset review page's issue
([review_file_format.md](../review-added-datasets/references/review_file_format.md)): `**Problem:**`, optional
leads (`**Details:**`, `**Background:**`), `**Options:**` with the table `| | Option | What it does | Pro | Con |`
(the tree as it is marked `(implemented)`), and `**Recommendation:** <letter>. **Decision:** <question>`. Turns
follow as described in step 5. A status that starts "with" (`with Andrej (draft PR)`) shows the issue as waiting on
someone else, without mark buttons. Findings the issues merge (`**A1. <title>** (verified). ...` paragraphs and
`## R1. ...` sections) show as each issue's evidence.

The anchors file maps an issue ID to node selectors: `{"T4": [{"id": "EXP.meets"}, {"sec": "EXP", "type": "q",
"contains": "repeated"}]}`. A selector picks by `id` (the tree's IDs, which survive edits of the text), or by
section code (`sec`), node type (`q`, `leaf`, `ref`), text the node contains (`contains`, also matching its examples)
or exact leaf `title`; `"tree": "draft"` selects in the draft.

## The marks

`marks/<issue>.<question>` (e.g. `T6.q2`): `{d: "ok" | "change" | "discuss" | null, pick: <option letter> | null,
note, by, at}`; `ok` is "as is", `change` with no pick is "other" (the note says what). `notes/<node id>`:
`{text, by, at}`. `by` is the viewer's opaque id; resolve names with `ArtifactData profiles`.

## Checking the page

Render the built page once in light, dark and at 400 px before handing over the link (on this machine: playwright's
`chrome-headless-shell` with libnspr4, libnss3 and libgbm1 extracted locally, the page wrapped in the publish
skeleton and served over `http://127.0.0.1` so it can fetch its data file). Look for overlapping cards, labels that
wrap badly, and colours that do not read in one theme. The page's script needs no build; a syntax error shows as an
empty canvas.
