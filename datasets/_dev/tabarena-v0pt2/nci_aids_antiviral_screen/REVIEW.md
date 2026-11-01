# nci_aids_antiviral_screen

**Outcome:** added. The NCI DTP AIDS antiviral screen, 41,133 compounds, each one a structure and the screen's own
conclusion (confirmed active 386, confirmed moderately active 1,011, confirmed inactive 39,736), split by chemical
series and scored by log loss. The structure is the only feature, as a SMILES column the benchmark encodes. A full
review panel ran and recommends shipping it; everything the panel settled is already applied, including a repair to
how the source's charge field is read. What is left for you is which framing ships, and whether `hiva_agnostic`,
the 2007 challenge cut of this same screen, retires now.

**Main points:** the target framing (the screen's three conclusions, as now, or the field's binary active/inactive),
and the retirement of `hiva_agnostic`. Two smaller confirmations follow them.

**Issues for Lennart:**

1. **Ship the screen's three conclusions, or the field's binary split?** The screen concludes CA, CM or CI per
   compound, and that is what ships, scored by log loss. Every published use of this file instead merges CA and CM
   into one active class and scores ROC-AUC: MoleculeNet, OGB's `ogbg-molhiv`, the 2007 HIVA challenge and ChemPile.
   This is the one genuine weighing call; no rule decides it, and the panel split on it before converging on "the
   curator decides".

   For the three conclusions: they are a real potency scale, not a labelling quirk. Of the actives where the source
   released both numbers, the selectivity index separates CA from CM at ROC AUC 0.948, and a single threshold
   reproduces 89.7% of the labels; CA compounds reach an EC50 in 84.6% of cases against 40.7% for CM, with median
   log10 EC50 -6.08 against -4.55. A model tells them apart from the structure alone at ROC AUC 0.77. The asymmetry
   decided it for the panel: anyone can merge CA and CM when scoring, but nobody can recover CA from a merged label.
   Keeping them also gives the collection a genuine multiclass molecule task.

   For the binary: it is what the field benchmarks, so results would compare directly with MoleculeNet and OGB; it
   would let the source's own metric apply instead of a fallback; and it keeps 7 compounds that the three-class
   framing drops, because they were concluded differently under different registry numbers. Measured: 41,140
   compounds, 1,404 active, ROC AUC 0.79 to 0.83 over the nine splits.

   Implemented: the three conclusions with `log_loss`. The binary recipe and its numbers stay in the definition's
   notes either way, so switching later costs nothing but a rebuild.

2. **Retire `hiva_agnostic` now that this ships?** You decided on 2026-11-01 to ship this release and retire the cut;
   this issue is here so the two are confirmed together and the working copy never ends up with neither.

   `hiva_agnostic` is the 2007 Agnostic Learning vs. Prior Knowledge challenge's cut of this same screen: 4,229
   labelled compounds given as 1,617 anonymous binary bits from ChemTK 4.1.1, with an IID split. A linking run on
   2026-11-01 recovered the registry number behind each of its rows by matching those bits against structure
   features: 97% of rows with confidence, and every one of its 4,229 labels agrees with the NCI file. Its three
   parts together are 42,678 compounds, which is this screen's structure-bearing set of 42,682 less four. So it adds
   no compound and no label this release lacks; what it adds is one 2006 feature representation that nobody can
   recompute for a new compound.

   Retiring it means: `No (Retired)` with `Duplicate` and `Outdated`, the folder leaves the working copy and
   `v2_path` is cleared, while `DF: Yes`, the collection tags and the shipped BeyondArena and TabArena v0.1
   containers stay, as for `churn` and the three `heart_disease_*` records. The duplicate pointer from `hiv_qsar`
   moves to this record.

   Implemented: nothing yet, pending your verdict here.

   Alternative: keep both, as the anonymised-features version of the same screen. Against it: PROV-6, and its
   features cannot be reproduced. For it: it already ships in TabArena v0.1, so retiring it changes what the two
   collections have in common.

3. **Confirm the fit reads `direct`.** The critic argued `approximate`, because the rule separating the three
   conclusions is nowhere published, and an unverified label definition makes a fit approximate (USE-8, the
   `differentiated_thyroid_cancer_recurrence` precedent). Two findings answered it. The mediator showed the boundary
   is not unverifiable but visible in the source's own released files, at the AUC figures in issue 1. Then you
   supplied Weislow et al. 1989, and it turns out to be the assay paper, not the conclusion rule: it defines the
   soluble-formazan method and one operational threshold, "if a test substance shows at least 30% protection against
   virus-induced cytopathic effects in the host cells, the microculture XTT antiviral assay is repeated", which is
   where the word "confirmed" in the labels comes from. The words "moderately" and "category" do not occur in it.
   So nothing was withheld from us, and the CA/CM line is a DTP reporting convention we can see in the data.

   Implemented: `fit="direct"`, with the NSC-batch dependency of issue 4 named in `fit_reason` as kept on purpose.

   Alternative: `approximate`, on the ground that `qsar_oral_toxicity` reads approximate for a comparable screen.
   The panel distinguished it: there an external set of untested chemicals exists and shows the test rows are closer
   to training than the chemicals a screener meets; here no such set exists, and the label is this screen's own
   conclusion on compounds sent to this screen.

4. **Confirm two things the panel settled that leave visible marks.** Neither needs a decision unless you disagree.

   The first is a repair. The source marks cations with a charge code our reader silently dropped, so 690 shipped
   compounds carried a hydrogen atom that is nowhere in the file: a sodium counter-ion shipped as sodium hydride, a
   phosphonium centre as a neutral five-bonded phosphorus. The file's own usage settles what the code means, since
   it writes that code and the ordinary +1 code on the same motifs. The repair is now applied; it recovered 2
   previously unreadable records and merged a handful of duplicates, which is why the count is 41,133 rather than
   41,136. The measured effect on scores is nil. One consequence worth knowing: MoleculeNet's copy of this screen
   has the identical artefact, so our structures now differ from MoleculeNet's and OGB's on those 690 compounds. Our
   rule says another collection's version is no reference for ours, so the repair stands; tell me if you would
   rather match the reference rendering.

   The second is a disclosed dependency, not a leak. Compounds registered next to each other were submitted together
   and share activity far above chance, and the scaffold split does not separate them. It is disclosed rather than
   split away because the registry number is not shipped, so no model can see it; the only channel is structural
   resemblance, which the scaffold grouping already holds out. Grouping the batches away would cost 0.003 macro AUC,
   inside the spread between folds. The numbers are in `splits_comment`, in the form the rules ask for.
**Review panel:** ship after changes (mediator). Full tier: claim auditor, column auditor, split auditor, domain
practitioner, blind reviewer, precedent checker, advocate and critic with one rebuttal each, mediator, editor.
Claims: every count reproduced; refuted were the fit, the target's typing, and three stale or imprecise sentences.
Blind review: would include with changes; its main concerns were the metric on a 96.6%-one-class target and the
single raw-SMILES feature. Agreed: the split keeps whole series apart, no screen measurement is a feature, the
charge repair, the ordered target, the probe re-run. Disputed and settled on new measurements: the fit (direct) and
the metric reason. Left for you: the target framing (issue 1) and the retirement of `hiva_agnostic` (issue 2).

<details><summary>Mediator</summary>

Verdict: ship after changes. Settled all four disputes with its own experiments.

- **The fit is `direct`.** The dispute was a fact, so it measured one: on the 387 actives where both an EC50 and an
  IC50 were reached, the log selectivity index separates CA from CM at ROC AUC 0.948, one threshold (SI about 12)
  reproduces 89.7% of the labels, and potency alone gives AUC 0.915; only 83 of 42,038 inactive compounds (0.2%)
  reached an EC50 at all. So the boundary is not unverifiable: it is a potency and selectivity boundary visible in
  the source's own released files. The thyroid precedent is distinguished because there a definition exists and the
  sources disagree, and no measurement could settle it.
- **The metric reason was wrong and is corrected.** A macro or one-vs-rest ROC AUC is well defined on three classes;
  what is true is that the source's metric is defined on a different target. It refused the extra clause the critic
  wanted, because on the shipped 1,407-column encoding log loss and macro AUC rank the families identically
  (random forest 0.1449 / 0.837, LightGBM 0.1588 / 0.824, selected linear 0.1818 / 0.768, linear 0.2737 / 0.747), so
  the near-tie both sides quoted is a stale 383-feature artefact.
- **The NSC batches get a note, not a re-split.** SPLIT-30 permits a re-split only when the context says the rows
  share an entity new data would not have; here NSC is not shipped, so no model can recognise a batch, and grouping
  it away costs macro AUC 0.8215 to 0.8184, inside the fold spread. Precedent: sarcoma.
- **The charge code means +1 here, and the repair is reading the source.** The file writes code 3 and code 4 on the
  same motifs (four-bonded phosphorus 81 against 538, bare sodium 25 against 426, bare potassium 11 against 24), and
  it is not strict V2000 (it also writes codes 8, 9 and -1), so code 4 cannot mean a doublet radical. What ships is
  not a misread charge but a hydrogen our reader invented to fill the valence; no such atom is in the file. It
  corrected two expectations: the repair recovers 2 of the 609 unreadable records, not the ~581 the debate assumed,
  and it merges about 6 records under the duplicate key.

</details>

<details><summary>Claim audit</summary>

Tested every statement the definition makes. Reproduced exactly: the join (43,850 conclusions, 42,687 structures,
42,682 joined), the duplicate and salt handling, the class counts, all group and fold counts, and the analog shares
(15.3% against 32.4%, actives 29.3% against 51.2%). Confirmed the metric is computable and meaningful on every fold.
Refuted: the fit (on the evidence then available), the target's unordered typing, the stale encoding description,
and two wording slips ("organic counter-ions stay" — the list also strips acetate, trifluoroacetate, triflate and
common solvents; "the shipped SMILES carries none" — one row keeps stereo marks). Re-ran the three headline numbers
on the current encoding: CA against CM 0.777, active against inactive 0.807, log loss 0.1522 against a prior of
0.1693 — all holding.

</details>

<details><summary>Column audit</summary>

No leak in the shipped frame: the one feature is the structure, which exists before the screen, and every screen
measurement stays out. Verified that the EC50 and IC50 files would leak if joined (the "not reached" flag is 99.8%
of inactive rows against 20.4% of confirmed actives) and that they are not. Found the charge-code defect and
measured that it carries no label signal. Confirmed the group column is excluded from the features, and that NSC and
CAS are correctly dropped (NSC alone scores ROC AUC 0.552, and compounds above NSC 700,000 are 13.7% active against
1.9 to 4.4% elsewhere).

</details>

<details><summary>Split audit</summary>

The scaffold split fits the use case and matches the four sibling datasets; the group id is an exact construction,
and no group crosses any split. Scores under alternatives: random 0.853 macro AUC, the shipped scaffold split 0.822,
a stricter similarity-cluster split 0.801. Found the NSC batch dependency and bounded it with a decisive experiment.
Noted that organic counter-ions in the group key put at most 0.4% of rows near a copy across the split.

</details>

<details><summary>Domain practitioner</summary>

Playing a screening chemist: would sign off `direct` — at the moment of the decision the structure is all they have,
and the label is the call the assay returns. Would use the model as a triage ranker in front of the plates, never as
a gate. Two caveats worth recording: the strongest single feature on most splits is the azo-dye fragment count, so
the model partly detects assay artefacts (the assay's own paper, read later, names non-specific XTT reduction as a
known false-positive mode, which confirms this); and the library is 1990s chemistry, so a prospective hit rate on a
modern deck would be lower. Argued for the binary framing with ROC-AUC on the grounds that it scores the ranking a
screening team acts on.

</details>

<details><summary>Blind review (clean room, no notes and no rules)</summary>

Verdict: include with changes. Confirmed the data is real and the labels agree with MoleculeNet's copy on every
shared compound. Measured active-vs-inactive ROC AUC 0.797 under a scaffold split and 0.827 under a random one, in
line with MoleculeNet's published 0.756 to 0.792. Its concerns: the target is 96.6% one class and stored unordered;
the only feature is a raw SMILES, so results depend entirely on the featurisation; the duplicate rule appeared to
drop actives; and the scaffold split is lenient. The duplicate point was answered by the claim audit (the rule drops
every row of a structure with two conclusions, which falls mostly on retested actives) and the lenience by the Lo-Hi
paper, now cited in the split note.

</details>

<details><summary>Precedent check</summary>

Seven of ten decisions follow precedent. Flagged three that did not and are now settled: the target's typing (fixed),
the dropped unreadable structures (kept, with the reason that the source is not damaged and re-drawing 609 metal
complexes would be our own invention), and the fit (settled by measurement). Confirmed the scaffold split, the
duplicate handling, the metric fallback and the retirement of `hiva_agnostic` all follow established cases.

</details>
