<!--
Rules: .claude/skills/knowledge-data-foundry/references/pull_requests.md

Above the first <details>, about 200 words a curator reads first:
* What changes and why, in one to three sentences. Name the curator and the date when the PR applies a decision.
* To decide: each open question with its options and a recommendation, or "Nothing to decide: ...".
* Before merging, only when there is something: the PR this depends on and why, a re-check or rebuild that has to
  follow, whether a container was built.
Everything else goes into the folded sections. A small PR is one paragraph: delete the sections, keep the checklist.
Checklist: tick an item once it holds, and tick one that does not apply with "n/a" after it. Why each item is there:
pull_requests.md, "Checklist".
Independent changes go against main; stack a PR only when it needs another unmerged PR (gh stack link).
-->

<What changes and why.>

To decide:
-

Before merging:

<details>
<summary>Changes</summary>

-

</details>

<details>
<summary>Evidence</summary>

</details>

<details>
<summary>Checks</summary>

- `pytest -q`:

</details>

Checklist:

- [ ] Reviews are in the records' `## Review`, none in a dataset folder (`move_reviews_to_records.py --check` is clean).
- [ ] Each settled issue has its `**Resolved (<date>, <who>):**` turn and its CC line in the record.
- [ ] A change to the working copy has its dated `CHANGELOG.md` entry.
- [ ] A decision that departs from a rule is written as an exception or an amendment.
- [ ] `pytest -q`, `uvx ruff@0.15.15` on the changed Python and `data-foundry-curation validate` pass.
- [ ] No local path (a run folder, a home folder) in the committed text or the body.
- [ ] Datasets another curator holds are listed in the body.
