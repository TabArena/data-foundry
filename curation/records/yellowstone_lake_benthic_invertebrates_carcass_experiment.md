---
unique_name: yellowstone_lake_benthic_invertebrates_carcass_experiment
name: Fish carcass / Yellowstone Lake benthic invertebrates (lake trout carcass treatment, BACI experiment)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Too Small
tags:
- Two-Regime Zeros
original_source: Other
year: '2022'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.c866t1g9m
- https://doi.org/10.1002/aff2.72
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3): a before-after-control-impact
field experiment at four sites, published to test a treatment effect; its inputs are the design.
- Source: Briggs et al., Dryad doi:10.5061/dryad.c866t1g9m (2022-09-21, CC0): invertebrate abundance and biomass
  workbooks by sample and taxon, plus four dissolved-oxygen logger workbooks and a README (file list from Dryad's
  metadata API, 2026-10-27; not downloaded, Dryad refuses automated downloads); paper Briggs et al. 2022, Aquaculture,
  Fish and Fisheries 2:470-483 (read in the accepted PDF on montana.edu).
- Use case: none. Dryad abstract: "We conducted a field experiment during one ice-free season at four sites in
  Yellowstone Lake to investigate the non-target effects of carcass treatment on benthic invertebrates"; paper,
  Introduction (last paragraph): "to determine how carcass treatment to suppress lake trout embryos affects
  invertebrate communities"; Sec. 2.4: "To determine if invertebrate density and biomass changed in response to carcass
  treatment, we assessed the interaction between time ... and treatment", tested at alpha 0.1 "because of variation
  expected from such a large-scale experiment with low replication". Two treated sites (Flat Mountain Hump, Snipe
  Point) and two controls, triplicate samples on three monthly and four biweekly dates (Sec. 2.3): the inputs are
  site, date, treatment and period, fixed by the design, and the oxygen loggers record the treatment's own mechanism.
  As in `mice_protein_trisomy_discriminant` (retired, Lennart, 2026-10-01: the classes are the experimental design and
  the sources test group differences), no decision is made from a prediction per sample; the Park Service decides on
  carcass treatment from the effect estimate.
- Siblings and duplicates: none (grep Yellowstone, lake trout, carcass). External collections: none.
- Metric: none (no task).
- `Too Small` stays as a concern: about 84 samples from four sites, though with no task there are no splits to count
  (TP-5).
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). The source calls it "a field experiment during one ice-free
  season at four sites", two treated and two controls in triplicate, analysed for a treatment effect
  (https://datadryad.org/dataset/doi:10.5061/dryad.c866t1g9m).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

Benthic invertebrate density and biomass around lake trout carcass deposits in Yellowstone Lake (Briggs et al. 2022).
A before-after-control-impact experiment at 4 sites (2 carcass, 2 control), triplicate samples on 3 monthly
pre-treatment and 4 biweekly post-treatment dates, about 84 samples by taxa (Dryad methods; files of 23-29 KB, not
downloaded because Dryad blocks automated downloads). Data analysis: "To determine if invertebrate density and
biomass changed in response to carcass treatment, we assessed the interaction between time ... and treatment", in
what the authors call "a large-scale experiment with low replication".

Zero mechanism, from the paper only: a taxon absent from a 0.25 m2 suction sample; zero-inflated models were used
for EPT and Sphaeriidae because they "had many zeros". Workbook pushback: it is a manipulated experiment, not
observational data, with 4 independent sites. Licence: CC0.

## Reference

Briggs M.A., Albertson L.K., Lujan D.R., Tronstad L.M., Glassic H.C., Guy C.S., Koel T.M. (2022). Fish carcass
deposition to suppress invasive lake trout through hypoxia causes limited, non-target effects on benthic
invertebrates in Yellowstone Lake. Aquaculture, Fish and Fisheries 2:470-483. doi:10.1002/aff2.72. Data:
doi:10.5061/dryad.c866t1g9m.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 39 (Fish carcass / Yellowstone Lake benthic
invertebrates).
