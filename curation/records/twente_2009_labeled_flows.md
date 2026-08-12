---
unique_name: twente_2009_labeled_flows
name: Twente 2009 Labeled Flow-based IDS Data Set
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Website
year: '2009'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://link.springer.com/chapter/10.1007/978-3-642-04968-2_4
- https://www.simpleweb.org/wiki/index.php/Traces
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: triaged by an AI (2026-08-12), no human has verified it. Check the verdict and the fields before relying on them.

Labelled NetFlow data from a honeypot run at the University of Twente (Sperotto et al., IPOM 2009) — real observed traffic, so criterion 4B is fine, but it carries the same honeypot-labelling concern as [[kyoto_2006_plus]]: traffic reaching a honeypot is unsolicited by construction, so check whether the label is anything more than "arrived at the honeypot".

**Source needs recovering first.** simpleweb.org, the distribution point, did not respond at all from here (repeated connection failures, not a 404), so availability must be re-established — try Wayback or the authors — before anyone plans work on it. The paper is paywalled at Springer and was not read; everything above about the labelling is a hypothesis to test, not a finding. Attack variety and volume are also reported as limited by the NTLFlowLyzer survey (Shafi et al., Computers & Security 148:104160, 2025, Sec. 5.1, p. 10).

## Reference

Sperotto, A., Sadre, R., van Vliet, F., Pras, A., "A Labeled Data Set for Flow-Based Intrusion Detection", IP Operations and Management (IPOM), LNCS 5843, pp. 39-50, 2009.
