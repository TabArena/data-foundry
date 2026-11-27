---
unique_name: maize_nam_flowering_time
name: NAM-maize-DTA (Maize Nested Association Mapping Flowering Time)
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- AI-Filled (Verify)
- Many features
- 'Samples: No Time Dimension'
- 'Entities: Recur'
- Experimental Results
- Non-IID (Grouped)
original_source: Other
year: '2009'
collection_period: 2006-2007
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1126/science.1174276
- https://www.panzea.org/phenotypes
- https://cornell.box.com/s/su1vodojjq5g8wg2aw8crimdx6328px6
v2_path: datasets/_dev/tabarena-v0pt2/maize_nam_flowering_time/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public
knowledge of this dataset and from the archive's own files, NOT from a built dataset. A human must verify everything
before relying on it.**

**Screening (AI, 2026-11-26):** `TBD -> Yes`, priority 4: days to anthesis of 4,699 maize recombinant inbred lines
of the 25-family Nested Association Mapping population from 1,106 imputed linkage-map markers, the line value a BLUP
across eight environments; the genomic-selection task of `genomic_prediction_maize_flowering_time` on twelve times
the lines, with the families as a group key and the raw plot data shipped beside the line values.
- Source: Buckler et al., "The genetic architecture of maize flowering time", Science 325:714-718, 2009
  (doi 10.1126/science.1174276; the publisher refuses automated fetches, so the paper's own text is unread in this
  run). The data is Panzea's "Buckler_etal_2009_Science_flowering_time_data-090807.zip", listed on its phenotypes
  page as "Flowering time phenotypes and imputed genotypes of our maize NAM population from Buckler et al. 2009"
  and downloaded 2026-11-26 (3.76 MB, seven files). As published, counted in the files: `markergenotypes062508.txt`
  holds 4,699 lines x 1,106 markers coded 0, 0.5, 1, 1.5 and 2 with no missing cell, 1.44% of cells carrying an
  intermediate imputed dosage, and the three traits in the same table, but no line identifier;
  `NAMSum0607FloweringTraitBLUPsAcross8Envs.txt` holds 5,463 lines with the family (25 `Z` groups of 190 to 200
  lines, and 481 rows that carry none), days to anthesis 58.40 to 121.21 (mean 77.04, sd 4.20), days to silk, and
  the anthesis-silking interval; four per-plot tables of 43,459 and 43,055 rows (days to tassel, days to silk and
  the two raw dates) span 9 location-year-rep rows, the paper's 8 environments, with B73 standing in 1,993 plots as
  the check grown everywhere; `markers061208.txt` holds the 1,106 markers with chromosome and position. Target
  `days2anthesis`.
- Use case: a maize breeder, before the season, ranks unphenotyped lines of the breeding population by predicted
  flowering time and chooses which to advance (genomic selection); fit direct inside the population, approximate
  for other germplasm. Collection: one designed population grown in replicated trials over two summers, the
  genotype fixed before the season and the trait read in the field, a line's value a BLUP over its own plots
  (`Samples: No Time Dimension`, `Entities: Recur`); the plot tables date the trials to 2006 and 2007, the line
  table carries no date. Type `Experimental Results` (a closed set of lines measured by one trial protocol,
  SPLIT-34).
- Split: leaf L-EXP.kind (Grouped · `UnseenGroup`, the family) because [EXP.meets] is a line of a cross the
  training side does not hold and [EXP.kind-key] is yes (the family, 25 groups of 126 to 196 genotyped lines),
  which is the leaf `genomic_prediction_soy_yield` reached on the same shape; open: whether the breeder instead
  meets a new line of a cross already phenotyped, which is L-EXP.random, and the enough-groups check on 25
  families.
- Siblings and duplicates: `genomic_prediction_maize_flowering_time` (`TBD -> 2nd Tier`, priority 2) is the same
  trait of the same species on another population, Azodi et al. 2019's pan-genome cut of 391 lines; this record is
  the better data that screening named, and from another population it is its own record, not a duplicate (PROV-4).
  `genomic_prediction_soy_yield` (`Yes`, a built folder) is the same task shape in another crop, so a distinct task
  (PROV-7), and its decisions on the group key and the metric are the precedent here.
  `genomic_prediction_rice_flowering_time` and `genomic_prediction_switchgrass_height` are the other Azodi cuts.
  External collections: none.
- Better data: none found for this task in this round. The same source holds a far denser genotype of the same
  population (Panzea's ZeaGBS v2.7, 955,690 SNPs over 17,280 public samples, of which the NAM share is not stated
  on the page), which is more markers for the same lines rather than more units, so it is a version question for
  the curator (PROV-6) and not better data.
- Papers and pages: Buckler et al. 2009 (above); https://www.panzea.org/phenotypes; the archive at
  https://cornell.box.com/s/su1vodojjq5g8wg2aw8crimdx6328px6.
- Metric: none found at the source: Buckler et al. is a QTL-mapping paper and the Panzea page defines no task, so
  there is no deliberate choice (MET-5). The nearest named metric for this task is Azodi et al. 2019's pooled
  Pearson's r, which is context from a sibling and not this source's call. On the shipped BLUPs the between-family
  share of the days-to-anthesis variance is 0.472, so MET-18 applies as it does on `genomic_prediction_soy_yield`
  (54.3%): the metric is declared per family, the pooled score is named as the original from context, and the
  declaration reports the share and what a family-mean predictor scores. Inputs: the family, which ships.
- Risks for /add-dataset: the genotype table ships no line identifier, only the family and the three traits, so its
  join to the BLUP table is positional; checked here, every one of the 4,699 trait values matches a BLUP value of
  its own family to two decimals and the first rows align exactly, so the trait doubles as the key, but a build
  states this and asserts it (PROV-13). The genotype table holds 4,699 of the BLUP table's 5,463 lines, and which
  764 it drops is unchecked. The markers are imputed at the source and cannot be checked from the release
  (LEAK-30 at most); 1,106 markers is a coarse linkage map beside what this population now has. Panzea states no
  licence or terms of use on the pages read (EV-4, no verdict reason). The plot tables hold the check B73, which is
  not a NAM line and must not become a row of the line table. Duplicate marker profiles were checked and there are
  none.
- Priority: gap 0 (biology & life sciences has 11 accepted, thin at 6.5 or fewer, and regression 78 is not thin),
  use case + (the breeder and the selection decision are named by the task's own literature), source + (a Science
  paper, a public archive, and the raw plot values beside the line values), shape + (4,699 lines x 1,106 markers),
  no minus: the positional join is measured and settled here, and the unstated licence is no verdict reason.

CC (2026-11-26, Andrej): accepted, go to `/add-dataset`.
- The screening's verdict stands: 4,699 lines over 25 families, 1,106 markers, the target in days, and the raw plot values beside the line values.
- Priority 4 kept. Nothing was built at screening.

## Review

**Outcome:** added as `maize_nam_flowering_time`: 4,699 recombinant inbred lines of the 25-family maize Nested
Association Mapping population, days to anthesis in days from 1,106 imputed linkage-map markers, grouped on the
family, scored by the within-family correlation. The data is the project's own Buckler et al. 2009 release and the
target is the line value it publishes, so no value is computed here. `dataset check` passes with 0 errors and 0
warnings over 28 checks and nothing is built. A full review panel ran and found no leak, no copy across a split, no
artefact in the target and no feature that is unavailable at the prediction point; it corrected a dozen statements
in the notes, and it left one question that decides the dataset (issue 4) and one that decides how it is served
(issue 5). A reading that the task has no signal across its groups was raised by the panel and then refuted:
models chosen for the problem all beat the training mean on unseen families.

**Main points:** whether the headroom is worth a benchmark slot (issue 4) is the decision; after it come the
genotype to ship on, the flowering trait, the split, and the container the benchmark hands a participant.

**Record judgment:** the screening block holds up on the data and its two open risks are closed, but one of them
was closed the wrong way round: the genotype table does carry a line identifier, as its first column, so the
"positional join" the screening worried about never existed and the definition now reads the id. The screening's
between-family share of 0.472 is wrong (0.6933 on what ships); its "27 families" are 25 families plus the IBM
population and a block of inbreds that includes B73 and the founders; and its marker-density risk is refuted, since
a tenth of the markers keeps 92% of the score. The panel's own corrections are in the definition and in the panel
block below.

**Issues for Andrej:**

1. **Ship on the parent-of-origin map, or rebuild on the population's absolute-allele genotype?**

   **Problem:**
   - The 1,106 shipped markers are coded relative to B73, so a 2 names a different founder's segment in each
     family and the features carry no absolute allele at all.
   - That is why the between-family part of the target, 69.3% of its variance, is unreachable by any model here,
     and why a dense SNP release would not be a denser version of this task but a different one.
   - The same population has a public absolute-allele release (955,690 SNPs over 17,280 public samples), whose
     overlap with these 4,699 lines is not measured.

   **Effect on the task:** under B the features change entirely, the family mean becomes partly predictable, and
   the per-family metric of issue 4 would no longer be forced; the rows and the use case are untouched.

   **Experiments:**

   | | measured |
   |---|---|
   | family-by-marker mean calls | all 25 x 1,106 lie in 0.441 to 1.581, none fixed in any family |
   | markers needed for the score | a tenth of them keeps 92% of the declared metric; ~31 markers per haplotype segment |
   | effective width | 77 components carry 90% of the marker variance, participation ratio 42.5 |

   **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Keep the parent-of-origin map (implemented) | 4,699 lines x 1,106 markers, the release's own pairing | genotype and phenotype come from one release and one paper; density is saturated, so nothing is lost to coarseness | the features cannot express the between-family component, which forces the metric of issue 4 |
   | B | Rebuild on the absolute-allele release | the same lines against the dense SNP release | a model could learn founder allele effects, and a pooled score would stop being wrong | a different task, not a better version of this one; another download and join; the overlap with these lines is unmeasured |
   | C | Ship both | A now, B as a second record | the comparison becomes measurable | two datasets of one population, and the curator picks one anyway |

   **Recommendation:** A, and B as its own record if it is ever wanted. The panel's practitioner and its blind
   reviewer agree on the facts and split on the conclusion: density is saturated, so A loses nothing to the map's
   age, while B is the only route to a learnable between-family component. **Decision:** A, B or C?

2. **Which of the three flowering traits is the target?**

   **Problem:**
   - The genotype table carries days to anthesis, days to silk and the interval between them in the same three
     columns, and the definition takes the first and drops the other two.
   - All three are measured on the same plants within days of each other, so none can be a feature for another.
   - Days to silk is the trait a drought breeder reads, and the interval is the one the source's own paper studies
     as a stress indicator.

   **Effect on the task:** the target column changes; the rows, the markers, the grouping and the metric do not.

   **Experiments:**

   | trait | within-family SD | between-family share | ridge, within-family r | within-family r with anthesis |
   |---|---|---|---|---|
   | days to anthesis (implemented) | 1.99 d | 0.693 | 0.372 | — |
   | days to silk | 2.24 d | 0.681 | 0.373 | 0.886 |
   | anthesis-silking interval | 0.79 d | 0.324 | 0.309 | 0.010 |

   **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Days to anthesis (implemented) | one dataset, the pollen-shed date | the trait this population is known for, and the paper's own title names it | the other two columns are discarded |
   | B | Days to silk instead | the silking date | closer to what a drought breeder selects on | the same trait by measurement (within-family r 0.886) and predicted no better, so nothing changes |
   | C | All three as separate datasets | three folders of one population | nothing is discarded | the interval needs managed drought to mean anything, and three cuts of one table are one task |

   **Recommendation:** A. Silk is the same trait days later; the interval is a genuinely different one but these
   are unstressed summer nurseries, where the panel's practitioner says it carries little of what makes it worth
   selecting on. **Decision:** A, B or C?

3. **Is the breeder's next cross a new one, or one already phenotyped?**

   **Problem:**
   - The definition holds out whole families, which is a breeder ranking the progeny of a cross nobody has grown.
   - A breeder who has phenotyped part of a cross and wants the rest ranked is an equally real use case, and that
     is a random split over lines.
   - The choice carries the few-groups warning with it, since 25 families give 8 or 9 per test fold.

   **Effect on the task:** under a random split every test line has full siblings in training; the family then
   becomes a legitimate input and the task is much easier.

   **Experiments:**

   | | whole families held out (shipped) | random over lines | splits |
   |---|---|---|---|
   | untuned ridge, declared metric | 0.164 | 0.188 | 60 |
   | random forest | 0.300 | 0.335 | 60 |
   | LightGBM | 0.265 | 0.301 | 60 |
   | LightGBM with `family` as a feature | not applicable | 0.517 | 15 |
   | pooled R^2, LightGBM | -0.144 | +0.226 | 60 |
   | a model fitted on two thirds of one family's own lines | 0.56 | — | 15 |

   The markers name a line's family on 50.3% of held-out lines against 4.0% by chance, so a random split hands a
   model the between-family component rather than merely adding siblings.

   **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Hold out whole families (implemented), accepting the few-groups warning | 20 x 3 splits over the 25 families, 8 or 9 per test fold | the question genomic selection is bought for; the warning is inherent to it and the signal across families is measured | 25 groups is few and the repeats reuse them, so the honest unit is the family |
   | B | Random split over lines | siblings of a test line are in training | more folds, no few-groups warning | a breeder ranking a new cross does not have its siblings; `family` would have to become a feature, and the score mostly measures family membership |
   | C | Both, as two datasets | A and B as separate folders | both use cases served | two datasets of one table, and the easier one would read as the better result |

   **Recommendation:** A, with the warning accepted as the definition writes it. The split auditor ran the
   alternatives and found none better; the practitioner, playing the breeder, calls A their own decision.
   **Decision:** A, B or C?

4. **Is the headroom this task offers worth a benchmark slot?**

   **Problem:**
   - The panel's blind reviewer, judging without our notes, would not benchmark on it: model families are hard to
     separate on a pooled score, and the effective sample is 25 crosses rather than 4,699 lines.
   - Read on the declared metric the same data separates models cleanly, from 0.05 for the best single marker to
     0.42 for the best honest model, with a dummy at 0.
   - The two readings disagree because a pooled score is mostly a test of predicting an unseen cross's mean, which
     these features cannot carry and which the breeder reads off the parents anyway.

   **Background:** an earlier version of this issue asked whether the dataset has any signal across its groups, on
   the ground that every model scored below the training mean there[^s28]. That premise was tested again with
   models chosen for the problem and does not hold, so there is no Must to answer and the question is the narrower
   one above.

   **Effect on the task:** the whole dataset, but as a judgment of worth rather than of validity.

   **Experiments:** pooled R^2 on unseen families, over 21 of the shipped splits:

   | model | pooled R^2 | folds above 0 | per-family r |
   |---|---|---|---|
   | training mean | 0.0000 | 0 of 21 | undefined |
   | ridge, penalty by inner cross-validation | +0.0445 | 20 of 21 | 0.369 |
   | ridge on markers centred inside each family | +0.0569 | 21 of 21 | 0.424 |
   | shrunk LightGBM | +0.0559 | 19 of 21 | 0.298 |
   | random forest, 300 trees | +0.0468 | 19 of 21 | 0.291 |
   | HistGradientBoosting | +0.0269 | 16 of 21 | 0.260 |
   | PLS, 8 components | -0.0066 | 10 of 21 | 0.342 |
   | an under-regularised ridge, and the group probe's defaults | -0.84 to -0.136 | 0 | 0.164 |

   The field's own GBLUP was attempted and the implementation was mis-scaled, so it is not reported. On the
   declared metric a within-family label permutation null over 200 runs has mean 0.0005 and SD 0.0068, putting the
   observed 53 SDs above it, and the breeder's realised gain is about 1.0 days per cycle at a fifth selected, 40%
   of a perfect ranking, positive in 94% of crosses.

   **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Ship as defined (implemented) | the dataset enters with the per-family metric | signal confirmed on both metrics once the model fits the problem; the metric is realised gain up to a constant; a real decision with a real actor | the pooled headroom is small, and the honest unit is 25 crosses |
   | B | Ship with the family-centred deviation as the target | the task becomes within-family transfer explicitly | every metric then agrees and a leaderboard reads straight | the target stops being the source's published value, which is what keeps this dataset clear of the rule the sibling needed an exception to[^rows] |
   | C | Do not ship | back to 2nd tier | spends no slot on a narrow genomic-prediction task | the outside objection rests on a pooled score the task does not declare, and the blind reviewer did not have the metric in its kit |

   **Recommendation:** A. The blind reviewer's verdict is the one piece of the panel worth weighing against
   shipping, and it was reached without the declared metric, which its own report notes was missing from its kit.
   On the metric the dataset declares, models separate across the full range and the signal survives a permutation
   null by 53 standard deviations. **Decision:** A, B or C?

   [^s28]: the split rule that a regression whose models all score below the mean on unseen groups has no signal
       across groups. Its trigger is not met here once the models are specified for the problem.
   [^rows]: the split rule that a dataset ships the source's own rows; the sibling
       `genomic_prediction_soy_yield` computes its line value from the plots and files an exception for it,
       while this dataset ships the published line value and needs none.

5. **Does the benchmark have to enforce the per-split refit, and record the public lookup?**

   **Problem:**
   - The participant kit ships `days_to_anthesis` for all 4,699 rows, test rows included, and nothing makes a
     participant refit per split, so one model fitted on every row and scored on all 60 splits reaches a perfect
     1.0 against an honest ceiling of 0.421.
   - The source file the task card links is a single unauthenticated download holding the identical 4,699 rows
     with the identical labels, so a join on the genotype vector also reaches 1.0.
   - Neither is a flaw in the task's design: the panel's gamer found no exploit in the features, the label, the row
     order, the split or the metric.

   **Effect on the task:** none on the data. It decides whether a number from this dataset is verifiable.

   **Experiments:** fit once on all rows, score all 60 splits: 1.000 (LightGBM) and 0.636 (ridge at alpha 0.1),
   against an honest 0.421. Marker pre-selection over all rows before fitting on the training side: +0.031, still
   below the honest ceiling. Every other attack returned nothing.

   **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Nothing; the harness already refits per split for our own runs (implemented) | no change | the collection fits its own models, so the exploit is not a route a scored model has, which is the standing decision on public lookups | an outside leaderboard built on this folder reports unverifiable numbers |
   | B | Record both in the definition as a caveat | one bullet naming the two and what they cost | a reader knows what a score here means | a published note tells a participant where to look |
   | C | B, plus ask the framework to hand a model only its training rows | a change to the harness, not to this dataset | closes the one exploit that is ours to close | a framework change for a problem no shipped collection has |

   **Recommendation:** B. The lookup is the same question you settled on 2026-11-26 for a public derived copy, and
   the answer there was that the collection fits its own models; what is new here is the refit, which is cheap to
   state and would be cheap to enforce later. **Decision:** A, B or C?

**Review panel:** full tier, seven evidence roles, run 2026-11-27 on the definition as committed that morning. Two
caveats on how it ran: the roles were not available as registered agent types, so each read its own role definition
instead; and the blind reviewer and the task gamer were sandboxed by instruction rather than by the hook, with both
reporting what did and did not reach them. The blind reviewer disclosed that the repository's `CLAUDE.md` reached
its context through the harness.

<details><summary>Claim auditor</summary>

31 claims tested, 26 held. It confirmed the marker order with a test the definition did not
have, comparing observed recombination fractions against the map's distances in sequence (Spearman 0.936
forward against 0.049 reversed, in all ten chromosomes), and the line-id recovery against the file's own ids
(4,699 of 4,699). It refuted four statements: the genotype table does carry the line id; "ridge" meant an
undisclosed alpha of 1,000 where the probe log in the same folder prints 0.165; the LightGBM figures did not
reproduce; and two probe claims asserted checks that had not run.

</details>

<details><summary>Column auditor</summary>

No column fails its dtype or its availability at the prediction point, no marker encodes
the family (largest between-family share 0.037), and neither sibling trait survives anywhere in the frame. It
found the imputation understated roughly fivefold and the value 1 described as a call, with the ladder across
recombination breakpoints as the evidence, and it identified the IBM population and the inbred block.

</details>

<details><summary>Split auditor</summary>

"Right with notes; nothing needs re-splitting." It walked the tree to the same leaf, ran
the alternatives (random over lines, a founder's half-sib group, a map-keyed split inside families,
leave-one-germplasm-group-out) and found none better, measured the split's cost on both metrics, and raised
the rule collision that is issue 4.

</details>

<details><summary>Domain practitioner</summary>

Fit approximate, metric kept, with the breeder's equation showing the declared metric
is realised gain up to a constant. It measured the founder's own flowering date as the thing a pooled score
would reward (r 0.965 to the family mean), struck the marker-density gap from the fit reason, and showed the
task delivers a ranking rather than a date.

</details>

<details><summary>Blind reviewer</summary>

Would not benchmark on it as prepared: the honest headroom is 2% of pooled RMSE, model
families are statistically indistinguishable while the regularization strength moves the score five times
further, and the effective sample is 25 crosses. It verified the table against the public source, endorsed
the grouped split and the dropped sibling traits, and proposed the family-centred target that is issue 4
option B.

</details>

<details><summary>Task gamer</summary>

No exploit in the features, the label, the row order, the copies, the metric or the field
design; the framing "holds up against everything I could test". Its two findings are the container's, and
are issue 5.

</details>

<details><summary>Precedent checker</summary>

Consistent with the sibling on the per-group metric, on shipping the source's own line
value and on the public second copy; departing on the few-groups evidence, which has since been measured to
the sibling's standard and is in the accepted warning.

</details>
