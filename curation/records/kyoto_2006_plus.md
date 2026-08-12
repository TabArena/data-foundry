---
unique_name: kyoto_2006_plus
name: Kyoto 2006+ (Kyoto University Honeypot Traffic)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: 2006-2015
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.takakura.com/Kyoto_data/
- https://www.kaggle.com/datasets/harshwardhanbhangale/kyoto-2006
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

Session-level records extracted with Bro 2.4 from Kyoto University's honeypots and darknet sensors, as daily files covering 2006-11-01 to 2015-12-31. The traffic is genuinely observed, so criterion 4B is not the problem here — the target is.

**The label is another detector's output.** The canonical page describes the current release as "Bro 2.4 based session extraction. Based on new IDS detection result", i.e. rows are labelled by what the deployed IDS/AV flagged, not by verified ground truth, so a model trained on it distils an IDS rather than learning intrusion. Second concern: the page's "Deployed systems" list separates the honeypots from a mail server and a web crawler, so benign vs attack may track which host received the traffic. Both need checking against the format document linked from the page before this moves either way (Song et al., BADGERS 2011, not read).

## Reference

Song, J., Takakura, H., Okabe, Y., Eto, M., Inoue, D., Nakao, K., "Statistical analysis of honeypot data and building of Kyoto2006+ dataset for NIDS evaluation", Proceedings of the First Workshop on Building Analysis Datasets and Gathering Experience Returns for Security (BADGERS), 2011.
