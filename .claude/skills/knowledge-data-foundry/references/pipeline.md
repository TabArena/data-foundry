# The curation pipeline

How a candidate dataset moves from a link to a container in this repository: the stages, the commands, the state of the
record after each step, and which file is the truth for what. The human-facing overview of the commands is the
[skills README](../../README.md); how decisions are ranked is
[principles.md](../../knowledge-curation/references/principles.md).

## Stages and commands

| Stage | The AI works | The curator verifies |
|---|---|---|
| 1. Screen: a quick pass from the context | [`/screen-candidates`](../../screen-candidates/SKILL.md) | [`/review-screened-candidates`](../../review-screened-candidates/SKILL.md): the dashboard's Screening queue |
| 2. Add: build, probe and attack | [`/add-dataset`](../../add-dataset/SKILL.md) | [`/review-added-datasets`](../../review-added-datasets/SKILL.md): the review page |

A build ([rebuild.md](rebuild.md)) and a commit happen only when the curator asks. A question about a record ("does X
belong?") needs no command: answer it from knowledge-curation.

## The record after each step

| Step | `suggestion` | `priority` | `checked_by` | Claim | Definition | Comments |
|---|---|---|---|---|---|---|
| New candidate | empty | empty | empty | none | none | none |
| Screened by the AI | `TBD -> Yes`, `TBD -> 2nd Tier` or `No` | 1-5 (none on `No`) | `AI (UNVERIFIED)` | none | none | the disclaimer and a `**Screening (AI, <date>):**` block |
| Verified by the curator | `Yes` (accepted for adding), `TBD -> Yes` (later) or `No` | as the curator leaves it | the curator | none | none | `CC` lines for decisions given in chat |
| Taken for adding | `Yes` | | | on the claims board; `WIP (DF)` and `claimed_by` mirrored | none | |
| Added by the AI | `Yes` | 1-5 again, from what was measured | | kept | `v2_path`, the folder with `REVIEW.md` | `**Assessment (AI, <date>):**` |
| Reviewed by the curator | `Yes`, or `No` / `No (Retired)` when retired | | | kept until the work reaches `main` | issues leave `REVIEW.md` as they settle; a retired folder goes | `CC` lines, `Exception to` lines |
| On `main` | `Yes` | | | `DF: Yes`, claim released | | |
| Built (on request) | | | | | the README's build record, a CHANGELOG entry | |

`AI (UNVERIFIED)` keeps a record in the review queue until a curator verifies it ([records.md](records.md)). The AI
never sets a plain `Yes` while screening; only a curator does.

## The queues

* **To screen:** records without a verdict, or a filter or list the curator names.
* **Screening review:** the dashboard's Screening pill (AI-unverified records whose verdict is not `No`, highest
  priority first); confirmed rejections are found with the status funnel on 🤖 and ✗.
* **To add:** `suggestion` `Yes`, no `DF: Yes`, no claim on the board, not AI-unverified
  (`#hf.suggestion=+Yes&hf.data_foundry_status=-DF: Yes&hf.claimed_by=+∅&hf.checked_by=-AI (UNVERIFIED)`; the
  dashboard's Claimed by column shows the board, [claims.md](claims.md)).
* **To review:** the folders of the working copy that have a `REVIEW.md`, and records with an `**Open issues (AI)**`
  block ([working_copy.md](working_copy.md)); the review page lists them by priority, highest first, and within one
  priority the fewest open decisions first. A record that is `WIP (DF)` with neither is reviewed and waits for the PR
  that brings it to `main`.

## Which file is the truth for what

When two files disagree, the one named here wins for its topic; the other is corrected.

| Topic | The truth | Not the truth |
|---|---|---|
| What the dataset is: data, target, splits, notes | the definition, `dataset.py` | the generated README (rewrite it with `dataset check`), the record's prose |
| The verdict, the status, the claim, the priority | the record's front matter | a review file, a chat message not yet applied |
| The curator's decisions and their reasons | `CC` lines in the record, `Exception to` lines | an AI assessment |
| What is still open | the folder's `REVIEW.md`, or the record's open-issues block | the review page (a snapshot of these files), a run folder |
| The rules | the knowledge skills | memory (pointers and preferences only), an old run report |
| A build | the README's build record and the CHANGELOG | the warehouse folder names |

A record field that disagrees with the definition is listed in `REVIEW.md` for the curator (`update` or `keep`), never
silently changed ([review file format](../../review-added-datasets/references/review_file_format.md)).

## Agents

The custom agents in `.claude/agents/` and the stage that uses them:

| Stage | Agents |
|---|---|
| Screen | `candidate-screener` (a batch of records), `reject-checker` (tries to refute each fast reject) |
| Add | `dataset-builder` (one source unit of a batch) |
| Add: the review panel ([review_panel.md](../../add-dataset/references/review_panel.md)) | `claim-auditor`, `column-auditor`, `split-auditor`, `domain-practitioner`, `blind-reviewer`, `precedent-checker`, then `advocate` and `critic`, then `mediator`, then `review-editor` |
| Both review skills | `precedent-checker`, on the curator's decisions before they are applied |

Subagents do not start subagents: the main session runs every panel. Limits of the machine: [agent_runs.md](agent_runs.md).
