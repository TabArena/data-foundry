---
unique_name: kddcup99
name: KDDCup99
checked_by:
- Andrej
- Lennart
suggestion: 'No'
decision_markers:
- Outdated
- Time-series (Classification)
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Data Quality Issue
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabSTAR
original_source: Other
year: '1999'
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.openml.org/d/42746
- https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
- https://archive.ics.uci.edu/static/public/130/kdd+cup+1999+data.zip
- https://web.archive.org/web/20110728094556id_/http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz
- https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data
- kaggle more (kavl31/kdd-cup-1999-data, primus11/kdd-99-original-dataset)
source_row: 629
type_adapter_id: curation-record-v1
---

## Comments

[12. August 2026 Notes] We were able to find the original data on re-uploads, but all details point to the data being simulated and full of issues that make it questionable to add to our benchmarks. 




CC: "Subsampled dataset. Detect intrusions. Might be outdated, but might as well be still representative; original data had 7 weeks of training and 2 weeks of test data so this implies a temporal connection"

Likely outdated too

* Tavallaee et al., "A Detailed Analysis of the KDD CUP 99 Data Set", IEEE CISDA 2009 —
  <https://www.ecb.torontomu.ca/~bagheri/papers/cisda.pdf>. Two defects: 78% of train and 75% of test
  rows are exact duplicates (Tables I/II), and the task is saturated — 97.97% / 86.64% of train / test
  rows are labelled correctly by all 21 classifiers they trained (Sec. IV.B). Their fix is [[nsl_kdd]].
* McHugh, "Testing Intrusion Detection Systems: A Critique of the 1998 and 1999 DARPA Intrusion
  Detection System Evaluations as Performed by Lincoln Laboratory", ACM TISSEC 3(4):262-294, 2000 —
  <https://dl.acm.org/doi/10.1145/382912.382923> (free copy:
  <https://sites.cs.ucsb.edu/~kemm/courses/CS595/TestingIDSs/mchugh_ll_critique.pdf.gz>). The
  underlying DARPA'98 simulation was never validated — no validation of the background traffic's
  false-alarm behaviour (Sec. 4.1, p. 269), no attempt to distribute the synthetic attacks
  realistically within it, and an unrealistic attack mix (Sec. 4.2, p. 271).

The artifact critique (Mahoney & Chan, RAID 2003) does *not* transfer here: the artifacts they found
are packet-header fields (TTL, client source IP, TCP window size/options) absent from KDD's 41
features — Tavallaee et al. Sec. III.


"intrusions simulated in a military network environment" "They operated the LAN as if it were a true Air Force environment, but peppered it with multiple attacks."

Is actually a time-series task, but was made tabular

"It is important to note that the test data is not from the same probability distribution as the training data, and it includes specific attack types not in the training data.  This makes the task more realistic.  Some intrusion experts believe that most novel attacks are variants of known attacks and the "signature" of known attacks can be sufficient to catch novel variants.  The datasets contain a total of 24 training attack types, with an additional 14 types in the test data only."
Class shift then, or need to change prediction task?

Only could use the official split, otherwise no temporal information?

## Reference

Cost-based Modeling and Evaluation for Data Mining With Application to Fraud and Intrusion Detection: Results from the JAM Project by Salvatore J. Stolfo, Wei Fan, Wenke Lee, Andreas Prodromidis, and Philip K. Chan.
