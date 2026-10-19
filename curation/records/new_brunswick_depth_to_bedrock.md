---
unique_name: new_brunswick_depth_to_bedrock
name: New Brunswick depth-to-bedrock (Pennell et al. 2026; provincial borehole, well, drillhole and outcrop points)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Not Available (from Paper))
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
year: '2025'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1016/j.geoderma.2025.117651
- https://doi.org/10.3390/rs13214210
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Depth-to-bedrock (DTB) mapping for New Brunswick with explicit zeros at bedrock outcrops (Pennell, Comeau, Zhang,
Feng and Heung, Geoderma 465:117651, online December 2025). Its points come from public provincial databases
(NBERD boreholes, drillholes and outcrop transects; NBELG well logs via GeoNB; pedons; till site cards), the same
sources as the predecessor compilation of Furze et al. (2021), whose PDF was read: "The result was 398 covariates for
176,658 DTB observations" (Sec. 2.5.3), multi-scale LiDAR terrain derivatives plus bedrock and surficial geology,
for a provincial DTB map with a 70:30 split. One row is an observation point; a spatial (grouped) split fits the
mapping use case, as for `lucas_topsoil` and `wosis_soil_profiles`.

Zero mechanism, from the 2021 paper only: structural, an outcrop has depth 0. In Furze Table 2 outcrops are 126,849
points (77%), all from one programme (NBERD transects), while positive depths come from wells and drillholes, so
zero against positive also tracks the data source and its sampling geography; a model can learn the programme rather
than the soil. The analytical table is not deposited; the workbook says it is "available on request", and the 2026
paper's text (and its data availability statement) could not be read (ScienceDirect 403). Workbook pushback: it calls
the same table both "public" and "available on request". To check: the PDF's data statement (Google the title plus
"pdf"); whether to request the table or rebuild it from GeoNB and the provincial LiDAR. Licence: article CC BY-NC-ND
4.0; the provincial sources are public.

## Reference

Pennell T., Comeau L.-P., Zhang J., Feng C., Heung B. (2026). The importance of zeros in digital soil mapping II: A
case study of depth-to-bedrock mapping in New Brunswick, Canada. Geoderma 465:117651.
doi:10.1016/j.geoderma.2025.117651. Predecessor compilation: Furze S. et al. (2021), Remote Sensing 13:4210,
doi:10.3390/rs13214210.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 1 (New Brunswick depth-to-bedrock).
