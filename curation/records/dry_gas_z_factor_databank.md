---
unique_name: dry_gas_z_factor_databank
name: Natural gas compressibility factor (dry-gas Z-factor) databank and associated ML codes (ANN, GMDH, GP)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2026'
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.18225906
- https://doi.org/10.3390/su18041742
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 1,079 compressibility factors of dry natural gases with a real engineering use, but two effective inputs (reduced pressure and temperature) on a smooth surface, compiled from literature sources the deposit does not name.
- Source: Faraji, Zenodo 10.5281/zenodo.18225906 (2026-01-12, CC BY 4.0, "The data is under review with a manuscript for publications"), with Bougha, Faraji, Khalili Nejad et al., "Machine Learning-Based Dry Gas Reservoirs Z-Factor Prediction for Sustainable Energy Transitions to Net Zero", Sustainability 18(4):1742 (2026-02-08). As published: one xlsx with P (MPa), T (K), Pc, Tc, Ppr, Tpr and Z, "compiled from multiple literature sources" (not named; the reference list has McCain & Cawley 1991, Ahmed 1986, Gaganis et al. 2019, Kamari et al. 2019) and "Z was obtained/reconciled using standard industry practice" (Zenodo); the paper: "1079 samples where pseudo-reduced pressure (Ppr) and pseudo-reduced temperature (Tpr) served as input and experimentally measured Z-factors as output" (abstract).
- Use case: "The experimental measurements of Z-factor are the most reliable source; however, they are expensive and time-consuming. This makes developing accurate predictive models essential" (abstract): a reservoir engineer estimates Z for a gas without a laboratory PVT measurement, in place of a correlation (DAK, Hall-Yarborough) or an equation of state; fit direct. Regime grouped by gas (a new gas; a pair of Pc and Tc likely marks one) rather than IID over pressure steps of one gas (SPLIT-24, to check on the data).
- Siblings and duplicates: `first_principles_ideal_gas` (`No`, 30 rows generated from the ideal-gas law, PMLB) is the record this was found for; no other Z-factor record (grep: compressibility, z-factor, Standing-Katz). External collections: none found.
- Better data: found as better data for `first_principles_ideal_gas`; no further search this round.
- Papers and pages: Bougha et al. 2026; the Zenodo deposit with the authors' ANN, GMDH and GP code.
- Metric: the paper reports MSE, R² and AARD% side by side (abstract) and names no single criterion, so the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: "obtained/reconciled" may mean some Z values were read from the Standing-Katz chart or a correlation rather than measured (PROV-3: trace the literature sources first; a chart-read table would be `AHDS`); Ppr = P/Pc and Tpr = T/Tc are exact functions of the other columns; a smooth two-input surface may be near-trivial for flexible models (TP-4); the ranges (Ppr 0.2 to 30, Tpr 1.05 to 3) limit the use to dry gases.
- Priority: gap 0 (regression, grouped not thin; the domain is petroleum engineering, left empty), use case + (the paper names the engineering need), source + (paper and deposit), shape 0 (1,079 rows, two effective inputs), risk - (unnamed upstream, "reconciled" values, a smooth low-dimensional surface): 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `first_principles_ideal_gas`.
- as published: Dry natural gases: 1,079 measurements compiled from several literature sources, columns P (MPa), T (K), Pc, Tc, Ppr, Tpr, Z (one 64 kB xlsx); about 0.2 <= Ppr <= 30, 1.05 <= Tpr <= 3; measurement ...; target: Experimentally measured compressibility factor Z = PV/(nRT) (regression); access: open.
- Why: The same physical relation as the ideal-gas record (pressure from temperature and volume per mole), measured on real gases: Z is exactly the deviation from the ideal gas law, so this is the real, measured counterpart of the formula-generated table
- Adds: Real measurements instead of 30 formula-generated rows, about 36 times larger, with a documented engineering use case and a paper benchmarking correlations and EoS against ML. Risks: only two inputs in the paper (Ppr, Tpr; P, T, Pc, Tc are also given), a smooth low-dimensional surface; a compilation whose upstream ...
