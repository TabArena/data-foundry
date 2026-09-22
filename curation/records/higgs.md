---
unique_name: higgs
name: Higgs
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Not Representative
tags:
- Review Prio 1 (Atlas)
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '2014'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5V312
- https://www.openml.org/d/42769
- https://arxiv.org/abs/1402.4735
- https://www.openml.org/d/45570
- https://archive.ics.uci.edu/dataset/280/higgs
source_row: 592
type_adapter_id: curation-record-v1
---

## Comments

CC: "Used in many benchmarks, Monte Carlo simulated but relevant task. In the challenge a special evaluation with postprocessing was required. Subsampled/preprocessed; includes feature engineering already"

CC (2026-09-22, Lennart): No. What it is (Baldi, Sadowski & Whiteson, Nat. Commun. 5:4308, 2014; arXiv 1402.4735): 11M fully simulated 8 TeV pp events (MadGraph5 + Pythia + Delphes fast detector sim). The signal is a *hypothetical* exotic process, not the observed 125 GeV Higgs: "gg -> H0 -> W H+- -> W W h0 -> W W b bbar" with "mH0 = 425 GeV and mH+- = 325 GeV" (p. 2); background is t tbar -> W W b bbar. 21 low-level kinematics + 7 invariant masses; label = MC truth; 53% signal by construction (p. 10) where real S/B is ~1e-3; test set drawn from the same simulation (p. 6).

Reason for No: how the HEP community treats it. Training on simulation is the real workflow (HiggsML write-up, Adam-Bourdarios et al. JMLR W&CP 42, Sec. 2.2 p. 5: "labeled examples of actual signal events in the real data are not available. Rather, events are simulated"), but this benchmark scores simulation-vs-simulation separability with AUC on balanced classes, which is not the physics objective: same paper, p. 6, "classification accuracy is a very poor measure of success in this case", and Sec. 7.1.1, the real analysis accepts only tiny selection regions because background systematics are ~10% of b. Baldi et al. call it "a semi-realistic case" (Discussion, p. 9) and note sensitivity is set "not only by the discriminating power of the selection, but by the uncertainties in the background model itself" (p. 7). The field's own benchmarks encode exactly what this one omits: HiggsML 2014 (ATLAS full sim, event weights, AMS; CERN Open Data record 328) and FAIR Universe HiggsML Uncertainty 2024-25 (280M events, target = CI on signal strength under 6 nuisance parameters; arXiv 2410.02867). The HEP-ML living review cites the 2014 paper only under "BSM particles and models"; its Datasets section lists FAIR Universe, the FAIR Higgs decay set and the LHC Olympics, not UCI HIGGS. So: simulated physics with dedicated benchmarks (criterion 4B), a machine-learning benchmark rather than a representative tabular application (`Not Representative`), consistent with cern_electron_collision_data / cern_proton_collision_dataset.

Standardization (paper p. 10, features "standardized over the entire train/test set") is indeed baked into the UCI/OpenML files (checked on 400k rows: angles mean 0 / std 1, phi range +-1.743, b-tag in {0, 1.0865, 2.173}); judged a harmless label-free affine rescale, not leakage, and not a factor in the verdict.

Copies: OpenML 4532/23512 (98k), 42769 (1M; the linked one), 43975/44077/44092/44129 (940k, Grinsztajn cut), 45570 (full 11M); TFDS `higgs`; Kaggle re-uploads. Same-paper siblings have their own records: `susy`, `hepmass`, `higgs_tautau`; related: `higgsml_2014`, `fair_universe_higgsml_uncertainty`. The old comment's "challenge with special evaluation/postprocessing" describes the Kaggle HiggsML (H -> tau tau, AMS), a different dataset.
