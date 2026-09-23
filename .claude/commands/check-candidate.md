Check one candidate dataset the curator is looking at: trace what the data really is, find what the
record misses, and report a second opinion with citations. Companion to `/triage-candidates`, which
holds the selection criteria this check applies.

**Input:** a record `unique_name` (a display name or a source link is fine; resolve it to the record first).

$ARGUMENTS

## When to invoke

* The curator is triaging a record in the dashboard and wants an independent check run in parallel:
  "check X", "dive into X", "what did I miss on X", "your thoughts on X".
* A record's `## Comments` contain open questions ("need to check duplicates", "licence unclear",
  "maybe not a real predictive task") and someone should go answer them.
* A verdict looks inconsistent with a sibling record and needs the evidence laid out.

If `/triage-candidates` has not been invoked in this session, invoke it first: its guidelines are the
rubric. `/verify-dataset` is for a filled-in notebook, not for a backlog record.

## Protocol

Do every step; skip only when an earlier step settles the verdict and say so.

1. **Reload the record from disk** and read `## Comments` for what they *mean*. Write down every open
   question they contain: those are the things to answer, not a report of everything you find.
2. **Siblings.** List records with a similar name, the same source, or the same external collection
   (`grep -il` over `curation/records/`). Read their verdicts and comments: the team's precedent
   decides consistency (`hypertension` and `public_health_ins` for TableShift re-cuts, `higgs` for
   simulated physics, the `Image` list for descriptors computed from pictures).
3. **Trace the original source.** Follow every link to where the data first came from: the competition,
   the paper, the repository, the agency. Read the paper's *text*, not the abstract: the organisers'
   write-up, the data descriptor, the appendix that defines the task. Cite by section with the
   load-bearing sentence quoted. A Kaggle page is a claim; the discussions and notebooks are where
   problems surface, and they cannot be fetched here, so say when that check was skipped and ask the
   human to paste a thread if it matters.
4. **Answer the criteria with evidence.** What the data physically is (measured, computed, simulated,
   derived from an image or a signal); the original task and what solved it (the model families at the
   top of the leaderboard are a modality signal, and a strong gradient-boosting baseline's rank is the
   tabular-competitiveness number); the split the task design requires, not the one the paper used;
   size after cleaning; how the target was constructed (composite, computed, a supervised transform);
   ethics; duplicates by provenance, not by table shape. Licence and redistribution terms are recorded
   as a one-line note and never used as the reason for a verdict or a marker.
5. **Write into the record only substance.** Add the source links you verified. Add one dated comment
   with what the data is, the decisive facts, and the recommended verdict and markers. Fill empty
   optional metadata only where the evidence is clear. Reload immediately before saving: the human edits
   the same file in the dashboard.
   * The human stated the verdict (in chat or already in the record): apply it and head the comment
     `CC (YYYY-MM-DD, Name):`.
   * The human has not: leave `suggestion` and `decision_markers` alone and head the comment
     `**Assessment (AI, YYYY-MM-DD):** recommend ...; the human has the call.` Do not use the
     `AI (UNVERIFIED)` reviewer convention here; it is for provisional triage of untriaged records.
6. **Leave the tree clean.** `git add` any new file under `curation/`, then run
   `data-foundry-curation validate` and `pytest -q tests/test_records_integrity.py`.

## Report back

Lead with the recommended verdict and markers in one sentence. Then, as bullets with their citations,
what the record missed or got wrong, what it had right, and what could not be checked. Then what you
changed in which files, and whether anything is uncommitted. Counts and scores go in a short table, not
in the prose. Do not restate the record.
