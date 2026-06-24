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

The well-known OpenML SpeedDating dataset (Fisman et al. mate-selection experiment) predicting whether a match occurs. It is already in the TabArena Reject collection: data came from a designed multi-wave experiment, the target is influenced by the study design, several features are questionable/leaky ('samerace', 'met'), and it reads as an interpretability/social-science study rather than a deployable predictive task. The grouped/wave structure further complicates honest evaluation. Recommend reject, consistent with prior curation.

---

CC: "Data was collected in multiple waves with a predefined study design influencing the target. Likely this is rather an interpretability task. If not accounting for the special data collection process, tree-based models are superior to other approaches; some questionable preprocessed features ("samerace"); "met" feature has time relationship due to multiple waves "

## Reference

Raymond Fisman; Sheena S. Iyengar; Emir Kamenica; Itamar Simonson.
Gender Differences in Mate Selection: Evidence From a Speed Dating Experiment.
The Quarterly Journal of Economics, Volume 121, Issue 2, 1 May 2006, Pages 673–697,
https://doi.org/10.1162/qjec.2006.121.2.673
