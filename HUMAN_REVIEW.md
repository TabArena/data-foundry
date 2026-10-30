# Human review in dataset curation

This is a short guide to the existing workflow. The linked skills define the full
procedure, decision values and file formats; this page adds no review gates.

| Step | Agent work | Curator decision |
|---|---|---|
| [Screen](.claude/skills/screen-candidates/SKILL.md) | Research source, task, likely split, duplicates and risks; draft a record and priority. | None yet: an AI screening recommendation is unverified. |
| [Review screening](.claude/skills/review-screened-candidates/SKILL.md) | Explain the candidate and apply reviewed decisions. | Proceed to actual-data work, keep for later, or reject; settle task constraints when needed. |
| [Add](.claude/skills/add-dataset/SKILL.md) | Implement the definition; run data checks, probes and the independent review panel; fix problems and collect open questions. | Resolve a material task choice if work needs one. The agent panel supplies evidence for human review. |
| [Review the added dataset](.claude/skills/review-added-datasets/SKILL.md) | Present the implemented task, evidence, panel findings and ranked issues; apply the curator's marks. | Ship, request changes, do not ship, or discuss; decide the applicable issues and record-field disagreements. |
| [Build and commit](.claude/skills/knowledge-data-foundry/references/rebuild.md), when requested | Build containers, verify reload/checksums and traced-input reproduction, and update reports and the changelog. | Request the build and authorize commits/publication within the intended scope. |

A review should make the task understandable: what one row represents, the target,
the prediction point and available inputs, the metric and split, what was checked,
the important limitations, and the exact remaining choices with a recommendation.
Source claims, measured results and unresolved facts should remain distinguishable.

Record curator decisions and reasons in the record's `CC` lines, with confirmed
exceptions recorded as the knowledge skills require. Apply settled choices to the
definition and record, regenerate affected reports and rerun affected checks.
Keep remaining questions in `REVIEW.md`; settled issues leave the active review.
A request for changes does not by itself mean final acceptance, and a ship decision
does not itself request a build or publication.

For commands and panel roles, see the [skills overview](.claude/skills/README.md).
For record and artifact authority, see the [pipeline reference](.claude/skills/knowledge-data-foundry/references/pipeline.md).
