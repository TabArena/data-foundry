---
unique_name: north_macedonian_wine_varieties
name: North Macedonian Red and White Wine Dataset (Multi-Vintage Physicochemical Differentiation and Machine-Learning Classification of North Macedonian ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- Tiny Data
- AI-Filled (Verify)
original_source: Kaggle
year: '2026'
problem_type: Multiclass Classification
source_links:
- https://www.kaggle.com/datasets/cvetamartinovska/north-macedonian-red-and-white-wine-dataset
- https://doi.org/10.20944/preprints202610.0890.v1
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 1,023 wines analysed by the Skopje university wine laboratory (vintages 2004-2023), grape variety from nine routine physicochemical parameters; a real, non-trivial replacement for the rejected `wine_recognition`, but small and so far only a preprint.
- Source: Kaggle, Cveta Martinovska, "North Macedonian Red and White Wine Dataset", uploaded 2026-10-08, CC BY-NC 4.0: "The analyses were performed at the Laboratory for Wine and Alcoholic Beverages, Institute of Agriculture, Ss. Cyril and Methodius University in Skopje, using internationally standardised OIV methods"; preprint on Preprints.org (doi 10.20944/preprints202610.0890.v1; it returned 403 here, not read). As published (a preview of the two files): DatasetRedWine.csv 614 rows (Vranec 312, Merlot 176, Cabernet 126; the card says 615), DatasetWhiteWine.csv 409 rows (Chardonnay 140, Smedervka 90, Riesling 76, Sauvignon Blanc 52, Temjanika 51; the card says 410); nine parameters (specific gravity, alcohol, total dry extract, reducing sugars, sugar-free extract, total and volatile acidity, total and free SO2) plus vintage year, variety and region (codes 1-7 per the card).
- Use case: a wine control laboratory or regulator, at the routine analysis of a sample, checks whether the declared variety fits its profile (varietal authentication, the preprint's framing per the run, not read here); fit approximate: these parameters mostly reflect winemaking, and authentication in practice uses other markers; regime likely temporal by vintage (a laboratory sees new vintages), otherwise IID as `wine_recognition`.
- Siblings and duplicates: `wine_recognition` (`No`: Outdated, Trivial, Tiny Data; 178 Italian wines, cultivar from 13 constituents); `wine_quality` and the other wine records predict quality, price or rating (other tasks). External collections: none (uploaded three weeks ago).
- Better data: found as better data for `wine_recognition`; no further search this round.
- Papers and pages: the preprint, "Multi-Vintage Physicochemical Differentiation and Machine-Learning Classification of North Macedonian Wine Varieties" (Martinovska Bande et al. 2026); the run notes a Random Forest at 73% accuracy on red and 83% on white (not verified).
- Metric: the preprint's accuracy is a threshold metric without a decision that fixes it (MET-6), so the fallback `log_loss` (MET-8); inputs none.
- Risks for /add-dataset: 25 red and 19 white rows repeat another row's nine measurements exactly (repeat analyses or copies, to check); nine rows are of vintages 2004-2007 although the card says 2008-2023; region code 0 (29 rows) is not in the card's code list; reducing sugars sit at 1 in about two thirds of the rows (a floor), where the sugar-free extract equals the total extract, so that column is partly computed from two others (a CLEAN check); two tables: one task per colour, or one with colour as a feature, the curator decides.
- Priority: gap + (multiclass is thin), use case 0 (the preprint's framing, not verified), source + (a named university laboratory, OIV methods), shape 0 (614 and 409 rows), risk - (repeated rows, small, a preprint only).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `wine_recognition`.
- as published: 614 red and 410 white wine samples (Kaggle page says 615 red), two tables; 9 physicochemical parameters measured by OIV methods (specific gravity, alcohol, total dry extract, reducing sugars, ...; target: Grape variety (classification; region also possible); access: open (CC BY-NC 4.0).
- Why: Same task as wine_recognition (the UCI Wine data of Forina et al.: 178 Italian wines, 13 chemical constituents, class = cultivar): predict the cultivar from a laboratory chemical analysis
- Adds: About 1,024 samples against 178, 16 vintages (2008-2023) against one 1980s study, several varieties and regions; not trivial (the preprint's Random Forest reaches 73% accuracy on red and 83% on white, where UCI Wine is solved almost perfectly), and the vintage allows a temporal split. Caveats: still small; a ...
