---
unique_name: raman_fuel_benchtop
name: Gasoline Properties (Benchtop)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Tiny Data
- Multi-target
- Many features
- Spectral Data
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
collections:
- RamanBench
original_source: Other
year: '2025'
collection_period: Unknown
problem_type: Regression
original_data_state: One Table
source_links:
- https://arxiv.org/abs/2605.02003
- https://huggingface.co/datasets/chlange/FuelRamanSpectraBenchtop
- https://huggingface.co/datasets/HTW-KI-Werkstatt/FuelRamanSpectraHandheld
- https://doi.org/10.1016/j.fuel.2018.09.006
- https://doi.org/10.1021/acs.energyfuels.9b02944
v2_path: datasets/_dev/tabarena-v0pt2/raman_fuel_benchtop/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 179 commercial gasolines with engine-measured octane numbers and additive contents and Raman spectra from a benchtop and a handheld spectrometer, for octane testing without the CFR engine; small, raw spectral bins.
- Source: the spectra were first released by the data owners on Hugging Face (chlange/FuelRamanSpectraBenchtop, created 2025-12-12; HTW-KI-Werkstatt/FuelRamanSpectraHandheld, 2025-12-16; CC BY 4.0; RamanBench Table 16 marks both new), from the studies Voigt, Legner, Haefner, Friesen, Wirtz and Jaeger, Fuel 236:829-835, 2019 (https://doi.org/10.1016/j.fuel.2018.09.006), and Legner et al., Energy & Fuels 34(1), online 2019-12-04 (https://doi.org/10.1021/acs.energyfuels.9b02944); year 2025 (PROV-9). As published (parquet schemas by range request): 179 rows x 961 bins (98-3801 cm-1; NXR FT-Raman, 1,064 nm) and 179 x 1,901 bins (400-2300 cm-1; IDRaman mini 2.0, 785 nm), 12 targets: RON for all 179, MON for 22, the other ten (ethanol, ETBE, MTBE, density, water, oxygenates, oxygen, olefins, aromatics, benzene) for 164. The samples: "130 refinery samples spanning RON 95-102.2 ... together with additional samples from petrol stations" (RamanBench A.17.7); RON by CFR engine (ASTM D2699), MON by ASTM D2885.
- Use case: a fuel inspector or laboratory rates a gasoline's octane near the pump with a fieldable spectrometer instead of an engine test (Voigt 2019 abstract: "the feasibility of fast and simple near-pump RON determination"); fit direct for RON. Regime IID over fuel samples; the refinery or station origin, the paper's train-then-apply design, does not ship, and raman-data finds repeated target tuples that may be repeat measurements (check, SPLIT-24).
- Siblings and duplicates: no duplicate (grep for the DOIs, "octane", "gasoline"). The record merges the benchtop and handheld spectra of the same 179 samples (PROV-6: one dataset, one instrument or both as columns). External collections: RamanBench (Tables 25, 26).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Voigt et al. 2019 (PCA, support vector regression; handheld Raman and 1H NMR at 80 MHz against benchtop NIR); Legner et al. 2019 (data fusion, additives; abstract only); the HF cards; RamanBench A.17.7.
- Metric: Voigt 2019: "The goodness of the method is expressed both in terms of computational residual mean squared errors and the common experimental reproducibility and repeatability limits", "40-50% of the samples are predicted within 0.2 and 80-90% with 0.7 RON" (abstract): two criteria, so the fallback `rmse` on RON, which is the paper's computational one (MET-5); the share within the ASTM limits would be a custom metric the source does not name as its one criterion; inputs none.
- Risks for /add-dataset: the sample origin (refinery or station) and a sample id are missing (PROV-2; ask the owners); MON for 22 of 179: ship RON (CLEAN-18); two instruments on the same samples (PROV-6); raw spectral bins (SEL-15, weighed against); 179 rows (Tiny Data).
- Priority: gap 0 (regression, IID not thin; domain unset), use case + (the source names near-pump testing against the CFR engine), source + (two papers and the owners' release), shape 0 (179 samples, one feature type), risk - (origin missing, spectral bins).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 179 spectra x 961 wavenumber features; 12 target(s) (raman-data id: fuel_benchtop); target: RON, MON, ethanol, oxygenates (MTBE, ETBE), benzene and other properties (12 targets).
- Why: Predict octane numbers and additive contents of commercial gasoline from Raman spectra (Benchtop FT-Raman, 1064 nm) | Predict octane numbers and additive contents of commercial gasoline from Raman spectra (Handheld Raman, 785 nm)
- Notes: Raw Raman spectral bins (961 wavenumber points, 98-3801 cm-1) as features; SEL-15 judges such signals case by case. New with RamanBench; studies Voigt et al. 2019 (https://doi.org/10.1016/j.fuel.2018.09.006) and Legner et al. 2019 (https://doi.org/10.1021/acs.energyfuels.9b02944). Same 179 samples as the other ...

## Review

**Outcome:** added. Voigt et al. (2019) and Legner et al. (2019) commercial gasolines: the research octane number from
a Raman spectrum, so a sample can be rated near the pump instead of on a CFR engine. 179 samples, each with a benchtop
and a handheld spectrum (961 and 1,900 bands), the eleven other laboratory properties dropped because none is known
when the spectrum is taken. `dataset check` gives 0 errors and 0 warnings. The probes find no exact copy across any
split and real signal. What is left for you is whether a dataset that barely separates model families belongs in the
benchmark, and whether the ten properties measured on 164 of the samples are worth a companion view.
Validity: USE-1 and USE-5 hold, fit direct: the source's own question on the source's own samples. LEAK-10 holds, the
spectrum is the only input. SPLIT-24 triggered and fixed: rows 42 and 96 are one fuel measured twice and share a
group[^f24].
Value: real signal, a random forest beats the class-share dummy on 100% of the splits (RMSE 0.904 against 2.471). TP-3
is the open question: the families sit within 0.028 of each other[^f3].
Quality: the spectra ship as published and are declared, state `raw`; one constant handheld band dropped (CLEAN-26).
Weighed: source + (two papers, the owners' release), use case + (near-pump octane against the engine test), gap 0,
shape - (179 samples, TP-9), risk - (the families barely separate).
For the curator: issue 1 (TP-3, the one that decides whether it ships), issue 2 (the other properties).

**Main points:** Issue 1 is the real question: a random forest and a linear model are 0.028 apart, so the dataset may
not tell methods apart. Issue 2 asks whether the ten properties on 164 samples ship as a companion.

**Record judgment:** valid. The record's screening said 179 samples, two instruments on the same samples, and RON for
all of them against MON for 22; the data confirms each. The screening's SPLIT-24 risk ("raman-data finds repeated
target tuples that may be repeat measurements") is confirmed and fixed.

**Issues for Andrej:**

1. **Does a dataset whose model families sit within 0.028 of each other belong in the benchmark?**

   * **Problem:**
     - The task probe raises `no_spread`: the best family and the next are too close to tell apart[^f3].
     - A random forest scores skill 0.861, LightGBM 0.853, a linear model 0.837, and the paired standard error of the gap is 0.016.
     - The signal itself is not in doubt: every family beats the dummy on 100% of the splits.
   * **Effect on the task:** a benchmark that cannot order methods adds rows without adding information; the dataset would measure that Raman predicts octane, which the source already showed, rather than which model reads a spectrum best.
   * **Experiments:** 30 of 60 splits, untuned. Dummy RMSE 2.471; linear 0.991, selected linear 0.996, random forest 0.904, LightGBM 0.937, the best single band 1.449. Spread random forest minus selected linear +0.028 (paired SE 0.016). A single band alone reaches r2 0.645, so most of the octane signal sits in a few bands around 1,050 to 1,070 cm-1.
   * **Consistency:** a `no_spread` flag is a weighing call, not a Must; the rules ask for a reason either way.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 179 samples, both spectra, RON | a real use case with real signal; spectra are thin in the benchmark; tuning may separate what untuned models do not | the untuned families are 0.028 apart, so it may not rank methods |
     | B | Ship only if a tuned run separates the families | the decision waits for a tuned comparison on the shipped splits | decides on the evidence the flag asks for | a run to schedule; the answer may still be no |
     | C | Don't ship, marker `Trivial` | the record returns to `2nd Tier` | the strictest reading of the flag | the task is not trivial, only narrow: no model is near perfect, RMSE 0.904 on a 15-point range |

   * **Recommendation:** B, and A if the tuned run separates them. The flag is about ranking methods, and only a tuned run answers it; C misreads a narrow task as a trivial one. **Decision:** A, B or C?

   **Notes for the AI:** on B, run the tuned comparison on the shipped splits and record the spread in the review before the verdict; on C, `suggestion` `No`, marker and a CC line.

   [^f3]: **TP-3**: a dataset that does not separate model families adds little to a benchmark; the flag is weighed, not decisive.
   [^f24]: **SPLIT-24**: a unit measured twice is one group. Rows 42 and 96 agree on all twelve properties and their benchtop spectra differ by at most 0.125 across 961 bands, where two random gasolines differ by 5.94.

2. **Do the ten properties measured on 164 samples ship as a companion view?**

   * **Problem:**
     - The release carries ethanol, ETBE, MTBE, density, water, oxygenates, oxygen, olefins, aromatics and benzene on 164 of the 179 samples, and the motor octane number on 22.
     - None of them is an input, because each is a laboratory measurement of the same sample; the question is whether any is a second target.
     - The definition ships the research octane number alone, which is measured on all 179.
   * **Effect on the task:** none on what ships today. A companion view would name a second task on the same rows for a later round, not change this one.
   * **Experiments:** none run; the counts are from the release (179 / 164 / 22).
   * **Consistency:** the rule on several targets ships one and names the others[^f18]; a companion view is how other records keep a second task visible.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Name none (implemented) | the notes list the dropped columns | the simplest record | a second real task stays invisible |
     | B | Name ethanol content as a companion | one line in the notes | ethanol is the property a field instrument is most often asked for, on 164 samples | a promise nobody may pick up |

   * **Recommendation:** B, as a note only. **Decision:** A or B?

   [^f18]: **CLEAN-18**: a release with several targets ships one and names the rest.

   **Notes for the AI:** on B, one bullet in `curation_comments` naming the companion and its row count; no change to the data.
