---
unique_name: autotuning_benchmark_hub_gpu_kernel_runtime
name: FAIR Benchmark Hub for Auto-Tuning (brute-forced GPU kernel search spaces)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
source_links:
- https://doi.org/10.5281/zenodo.15364125
- https://github.com/AutoTuningAssociation/benchmark_hub
- https://doi.org/10.1145/3629527.3651429
- https://doi.org/10.5281/zenodo.11617999
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16, with SEL-8): the hub ships "fully brute-forced search spaces" of GPU tuning parameters, every configuration of a designed grid measured per kernel and GPU, as "GPU auto-tuning benchmarking resources"; the same facts as `sgemm_gpu_kernel_performance` (`No`, AHDS: "all possible value combinations are in the dataset").
- Source: Willemsen, van Nieuwpoort, van Werkhoven (Netherlands eScience Center, Leiden University), "FAIR Benchmark Hub for Auto-Tuning", Zenodo doi 10.5281/zenodo.15364125 (v1.0.0b1, 2025-05-08, MIT; GitHub AutoTuningAssociation/benchmark_hub): "This repository is a FAIR-compliant hub for GPU auto-tuning benchmarking resources" that "provides fully brute-forced search spaces (in original and T4 format)"; "24 fully brute-forced search spaces": 4 kernels (GEMM, convolution, hotspot, dedispersion) x 6 GPUs (NVIDIA A100, A4000, A6000; AMD MI250X, W6600, W7800); configurations per space not stated. The kernels come from Lurati, Heldens, Sclocco, van Werkhoven, "Bringing auto-tuning to HIP: Analysis of tuning impact and difficulty on AMD and Nvidia GPUs" (Euro-Par 2024; artifact doi 10.5281/zenodo.11617999), an analysis of tuning, not a prediction task.
- Use case: the source's is benchmarking auto-tuning search on stored spaces (SEL-8). The steelman: predict each configuration's runtime on a GPU not yet measured, learned on the others; the spaces carry no device features, so a held-out GPU is an unseen category, and six GPUs make six groups. Within one GPU every configuration is already measured, so a prediction serves no decision.
- Siblings and duplicates: `sgemm_gpu_kernel_performance` (`No`, AHDS; the CLTune GEMM grid on one GPU); `sat11_hand_algo_runtime` (`Yes`) differs, its rows are real problem instances, not a designed grid. External collections: none found.
- Better data: found as better data for `sgemm_gpu_kernel_performance`; no further search this round.
- Papers and pages: the Zenodo record and the GitHub README; Hozzová, Tørring, van Werkhoven, Strelák, Vuduc, "FAIR Sharing of Data in Autotuning Research (Vision Paper)", ICPE '24 Companion (doi 10.1145/3629527.3651429).
- Metric: none (the source compares tuning methods by the configurations they find, not by predictions).
- Risks for /add-dataset: not applicable.
- Reject check (AI, 2026-10-31): stands. README: 'fully brute-forced search spaces' to 'compare optimization algorithms', usable 'without constant access to the original hardware' (https://github.com/AutoTuningAssociation/benchmark_hub; https://zenodo.org/records/15364125); no prediction, model or transfer use is named. Same facts as sgemm_gpu_kernel_performance (TabArena verdict 'Deterministic'; Lennart: 'not a real predictive task if we know and observe all combinations', and he weighed the special splits too). The unseen-GPU steelman has six GPUs and no device features.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sgemm_gpu_kernel_performance`.
- as published: 24 fully brute-forced search spaces: 4 kernels (GEMM, convolution, hotspot, dedispersion) x 6 GPUs (NVIDIA A100, A4000, A6000; AMD MI250X, W6600, W7800); one row per tuning configuration; ...; target: Measured kernel runtime per configuration of tuning parameters (as in SGEMM's four runs); access: open.
- Why: Same target and features as SGEMM (runtime of a tiled GEMM kernel from its tuning parameters such as work-group and tile sizes, vector widths), measured on current hardware; the kernels follow the Kernel Tuner/CLTune lineage of the UCI data (to check that the GEMM kernel is the CLBlast one)
- Adds: Six GPUs of two vendors and four kernels against one 2012-era GPU and one kernel: a split by GPU (or by kernel) makes the task open-world and answers the record's objection that every combination of the grid is observed. The Deterministic/Trivial concern stays within one GPU (each space is still a full grid); ...
