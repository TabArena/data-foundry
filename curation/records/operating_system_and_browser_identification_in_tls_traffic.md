---
unique_name: operating_system_and_browser_identification_in_tls_traffic
name: operating-system-and-browser-identification-in-tls-traffic
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
domain: technology & internet
required_split:
- Random (IID)
problem_type: Multiclass Classification
source_links:
- https://zindi.africa/competitions/operating-system-and-browser-identification-in-tls-traffic/data
source_row: 970
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

A Zindi competition to identify the operating system and browser from TLS network-traffic features. Network-traffic fingerprinting from extracted handshake/flow features is a standard tabular multiclass classification task with real-world relevance. The split is likely random (IID) unless connections are grouped by host/session. Suggest TBD -> Yes; a human must confirm the features are pre-extracted tabular fields (not raw packet captures), the target cardinality, dataset size, and whether grouping is needed.
