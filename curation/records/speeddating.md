---
unique_name: speeddating
name: SpeedDating
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Not Representative
tags:
- 2nd Tier / Scientfic Discovery
- Non-IID (Grouped)
- AI-Filled (Verify)
collections:
- TabArena Reject
- TabSTAR
year: '2004'
domain: social science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/d/40536
- Columbia Business School  -> https://sites.stat.columbia.edu/gelman/arm/examples/speed.dating/  -> https://statmodeling.stat.columbia.edu/2008/01/21/the_speeddating_1/ -> ?
source_row: 842
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line, TabArena Reject) stands; the research agrees on the target and adds the leak in the rating columns.
- Source: Fisman, Iyengar, Kamenica, Simonson, "Gender Differences in Mate Selection: Evidence From a Speed Dating Experiment", QJE 121(2), 2006 (see Reference); experiments run with Columbia University students in several waves (2002-2004 by the public codebook, not re-checked); the public copy is Gelman's page at Columbia (https://sites.stat.columbia.edu/gelman/arm/examples/speed.dating/) and OpenML 40536 (8,378 date pairs x about 120 columns, target `match`).
- Use case: none fits. The paper is an economics study of stated and revealed preferences; `match` means both partners said yes at the same event, and the ratings of the partner (`attractive_partner`, `like`, `guess_prob_liked` and the like) are filled in on the same scorecard as the decision, so they are not known before it (LEAK, USE-4). A dating service predicting a match before the date would have only the pre-event survey, which is a different, much weaker task that the source did not define.
- Regime: grouped by participant and wave, as the CC says (each person rates 10 to 20 partners); an IID split repeats the same people.
- Siblings and duplicates: none among the records. External collections: TabSTAR; OpenML 40536.
- Metric: none in the paper (it reports regressions, no prediction score), so the fallback `roc_auc` had it shipped.
- No counter-argument: the CC's "interpretability task" matches the paper's aim, which is to estimate gender differences in mate selection, not to predict matches.

The well-known OpenML SpeedDating dataset (Fisman et al. mate-selection experiment) predicting whether a match occurs. It is already in the TabArena Reject collection: data came from a designed multi-wave experiment, the target is influenced by the study design, several features are questionable/leaky ('samerace', 'met'), and it reads as an interpretability/social-science study rather than a deployable predictive task. The grouped/wave structure further complicates honest evaluation. Recommend reject, consistent with prior curation.

---

CC: "Data was collected in multiple waves with a predefined study design influencing the target. Likely this is rather an interpretability task. If not accounting for the special data collection process, tree-based models are superior to other approaches; some questionable preprocessed features ("samerace"); "met" feature has time relationship due to multiple waves "

## Reference

Raymond Fisman; Sheena S. Iyengar; Emir Kamenica; Itamar Simonson.
Gender Differences in Mate Selection: Evidence From a Speed Dating Experiment.
The Quarterly Journal of Economics, Volume 121, Issue 2, 1 May 2006, Pages 673–697,
https://doi.org/10.1162/qjec.2006.121.2.673
