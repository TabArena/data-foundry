---
unique_name: qsar_aquatic_toxicity
name: qsar_aquatic_toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
collections:
- TabArena Reject
original_source: UCI
year: '2014'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5SG7H
notebook_path: datasets/beyond_iid/new_iid/qsar_aquatic_toxicity/qsar_aquatic_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_aquatic_toxicity/dataset.py
source_row: 3
type_adapter_id: curation-record-v1
---

## Comments

CC: "546 samples, too small for 3-fold CV. 

Same data source / type of study as for QSAR_fish_toxicity (10.24432/C5JG7B)

predict acute aquatic toxicity towards the fish Pimephales promelas (fathead minnow) on a set of 908 chemicals."

Check if any of the qsar fish datasets are used in tabaren already

Other version in TabArena "QSAR_fish_toxicity"

Generally fine to add, but we need to decide whether we allow two datasets that similar in the benchmark

**Assessment (AI, 2026-10-14):** the quoted sentence about the fathead minnow and 908 chemicals is UCI's summary of QSAR fish toxicity (UCI 504), pasted by mistake into the summary of this dataset (UCI 505). This dataset is 546 chemicals with the 48-hour LC50 for Daphnia magna, a regression target (UCI 505 abstract; Cassotti et al. 2014).

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit set to `direct`; the authors' selection of the eight descriptors by their fit to the toxicity is named in `fit_reason` as a kept potential leak.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Cassotti et al. (2014) report Q2 with RMSE, no single task metric; r2 and rmse rank models the same within a fold.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the folder's `REVIEW.md` (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 2: gap -, use case +, source +, shape -, risk - (a near-copy of qsar_fish_toxicity; a kept selection leak).
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `adore_aquatic_toxicity` (TBD -> Yes, priority 3), `aquatic_toxicity_lunghini_consensus` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): go ahead for the structure-recoverable datasets: ship the SMILES only, as for qsar_tid_11. The authors' descriptors are one modelling choice; the benchmark encodes the structure.

**Assessment (AI, 2026-11-01):** the structures are recoverable and the link is exact. The authors' own workbook (Milano Chemometrics, `toxicity_data.xlsx`) holds the same 546 rows in the same order as the UCI file, with CAS-RN, SMILES, their train/test split, LC50 and the same 8 descriptors; all 8 and LC50 are identical on every row. The 8 descriptors leave, which settles the kept potential leak the record named: a genetic algorithm chose them by their fit to the measured toxicity of chemicals in our test folds (LEAK-31), and no such selection reaches the features now. `SMILES` is the one feature; the split is scaffold-grouped (463 groups). Task probes, 30 splits: LightGBM R^2 0.573, random forest 0.548, no flags.

CC (2026-11-02, Lennart): on how the Milano workbook the structures come from was downloaded ("freeware with proper
reference", fetched through a public link rather than the authors' notification form): "that is okay for now, we can
note it but it is not blocking us here". Noted here; regularise before this ships outside the group.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Keep with a note on its overlap with qsar_fish_toxicity: a different task (species, exposure time) of the same Milano design, now shipping the recovered structures with a scaffold split, so the old selection leak is gone; Andrej's redundancy dispute (issue 1) is the open call. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): keep both, note the overlap (BeyondArena v0.2 review page, issue 1, B; disagreement settled, `Yes`): a sibling of qsar_fish_toxicity from the same group, databases and pipeline, but another species (Daphnia magna, not the fathead minnow) and exposure time (48 h, not 96 h), so a different task (PROV-7). The overlap is in `curation_comments`: about 145 to 165 shared chemicals, estimated from matching MLOGP values, LC50s correlated at r = 0.75 on 89 one-to-one matches. The count by structure waits for the two authors' workbooks, which are not on this machine.

## Reference

@article{cassotti2014prediction,
  title={Prediction of acute aquatic toxicity toward daphnia magna by using the ga-k nn method},
  author={Cassotti, Matteo and Ballabio, Davide and Consonni, Viviana and Mauri, Andrea and Tetko, Igor V and Todeschini, Roberto},
  journal={Alternatives to Laboratory Animals},
  volume={42},
  number={1},
  pages={31--41},
  year={2014},
  publisher={SAGE Publications Sage UK: London, England}
}

CC (2026-11-11, Andrej): kept next to `qsar_fish_toxicity` with the overlap written into both definitions (review issue 1, B).
- Counted by structure, from the two authors' workbooks rather than the earlier MLOGP estimate of 145 to 165: 237 chemicals are in both, 43.4% of this set and 26.1% of the fish set, 225 of them under the same CAS-RN.
- Their LC50s correlate at r = 0.81 (Spearman 0.82), the Daphnia values 0.37 log units more toxic on average.
- The species, the exposure time and the endpoint differ (Daphnia magna 48 h against the fathead minnow 96 h), so the two are different tasks of one study design, not duplicates; the notes of both now say so, since a method that suits the design gains on both.
