"""Curated dataset definition for `aquatic_toxicity_lunghini_consensus` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from data_foundry.definition import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Smiles,
    Source,
    TaskSummary,
    TimeBasis,
    canonical_smiles,
    scaffold_groups,
)

RAW_FILE = "MergedEndpoints.sdf"
"""The one file of the Zenodo deposit: 3,680 compounds with at least one of the three endpoints, as an MDL SD file
whose data fields carry the canonical SMILES, the CAS-RN, the source databases and the values."""

VALUE_FIELD = "pLC50 - FISH"
"""The fish endpoint as the source publishes it: the 96-hour median lethal concentration as -log10(mmol/L)."""

MG_PER_L_FIELD = "mg/L - FISH"
"""The same value in mg/L. It is the target in another unit, so it does not ship; where the two disagree the
published pLC50 is the one that matches independent values of the same compound (curation_comments)."""

MMOL_TO_MOL = 3.0
"""The published pLC50 is -log10(mmol/L); adding 3 gives -log10(mol/L), the scale qsar_fish_toxicity ships."""

REGISTRY_FORMULA = {
    "275514": "C10H8",
    "3347226": "C14H4N2O2S2",
    "104653341": "C31H23BrO2S",
}
"""The molecular formula the chemical registry gives for the three substances the file draws twice with two different
formulas, by the digits of the CAS-RN: azulene (275-51-4), dithianon (3347-22-6) and difethialone (104653-34-1), read
from PubChem on 2026-11-25. In each pair exactly one drawing carries this formula and is the substance the CAS-RN
names; the other drawing is a different chemical and its row goes."""


class AquaticToxicityLunghiniConsensus(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="How toxic is a chemical to fish, judging from its molecular structure?",
        use_case=(
            "For example, a hazard assessor at a chemical maker or a regulator estimates a substance's acute fish "
            "toxicity from its structure instead of running the 96-hour test, to decide whether it needs testing and "
            "how to classify and label it."
        ),
        row=(
            "One chemical with a 96-hour fish toxicity value in the collection Lunghini et al. 2020 merged from "
            "public toxicity databases and a set of literature values (2,186 chemicals; the Daphnia and algae "
            "endpoints of the same file are other targets on other organisms and other tasks)."
        ),
        predicted=(
            "The concentration that kills half the test fish within 96 hours, as minus the log of moles per litre, so "
            "higher means more toxic. One value per chemical: the median of the guideline measurements the source "
            "kept for it, pooled over the fish species that were tested and over the sources it drew on."
        ),
        known=(
            "The chemical's structure, as a SMILES string. The substance has not been tested on any trophic level at "
            "this moment, so no measured value is known."
        ),
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side. Chemicals "
            "without a ring, and the many built on a bare benzene ring, are held out one by one, so for about three "
            "fifths of the test chemicals the model has seen their ring skeleton on another chemical."
        ),
        changes=(
            "We take the fish endpoint alone, put the target on minus the log of moles per litre, keep one row per "
            "substance where the file draws one chemical twice (the chemical registry decides which of two drawings "
            "is meant), drop the list of source databases and the value in mg/L, and split by chemical series."
        ),
        fit="direct",
        fit_reason=(
            "The structure is all an assessor has for an untested substance, and a held-out series stands for a "
            "family not yet tested. The value names no fish species, so the model learns the collection's pooled "
            "value under the guideline rather than one named test. These rows are the source's public cut, and the "
            "error grows with the distance to the training chemicals (`curation_comments`)."
        ),
    )

    # Dataset
    unique_name = "aquatic_toxicity_lunghini_consensus"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.5281/zenodo.3708082",
            license="CC BY 4.0",
            year="2020",
            files=(RAW_FILE,),
            bibtex=r"""
                @misc{lunghini2020aquatic_data,
                  author={Lunghini, Filippo and Marcou, Gilles and Azam, Philippe and Enrici, Marie-H{\'e}l{\`e}ne and Van Miert, Erik and Varnek, Alexandre},
                  title={Consensus {QSAR} models estimating acute aquatic toxicity for three trophic levels organisms: Algae, Daphnia and Fish},
                  year={2020},
                  publisher={Zenodo},
                  doi={10.5281/zenodo.3708082},
                  howpublished={\url{https://doi.org/10.5281/zenodo.3708082}},
                  note={The collected public data of the companion article; one file, MergedEndpoints.sdf}
                }
                @article{lunghini2020consensus,
                  title={Consensus models estimating acute toxicity to aquatic organisms from different trophic levels: algae, Daphnia and fish},
                  author={Lunghini, Filippo and Marcou, Gilles and Azam, Philippe and Enrici, Marie-H{\'e}l{\`e}ne and Van Miert, Erik and Varnek, Alexandre},
                  journal={SAR and QSAR in Environmental Research},
                  volume={31},
                  number={9},
                  pages={655--675},
                  year={2020},
                  doi={10.1080/1062936X.2020.1797872},
                  publisher={Taylor \& Francis}
                }
            """,
        ),
    )
    special_features = (Smiles(column="SMILES"),)
    download_description = """
        The one file of the authors' Zenodo deposit (source_url), downloaded 2026-11-25.

        mkdir -p local-data-warehouse/aquatic_toxicity_lunghini_consensus && curl -L -o local-data-warehouse/aquatic_toxicity_lunghini_consensus/MergedEndpoints.sdf https://zenodo.org/api/records/3708082/files/MergedEndpoints.sdf/content

        MergedEndpoints.sdf (6,325,348 bytes), sha256
        9ce895c83dbf211468713cd9fa714e596efaf5d7191d2495c09960e11128fc8f, md5 412738140006ff5ad4394fa188885a43 as
        the deposit states.
    """
    curation_comments = """
        We start with MergedEndpoints.sdf from the Zenodo deposit of Lunghini et al. 2020, the public data behind their consensus aquatic-toxicity models: 3,680 compounds, each with at least one of three endpoints.

        - Prediction point: a substance before it is tested, on fish or on any other trophic level. Its structure is known; nothing measured in a toxicity test is. The Daphnia and algae values of the same file are therefore not inputs here, although they would be at a later moment: once a registration dossier is being filled, the 48-hour Daphnia and 72-hour algae tests are the ones a registrant runs before the fish test, and they carry a value for 47.1% and 31.4% of these chemicals.
        - The fish endpoint alone. The file carries three targets on three organisms (fish 96-hour pLC50 on 2,200 compounds, Daphnia 48-hour pEC50 on 2,120, algae 72-hour pEC50 on 1,440), which are three tasks, not three views of one (PROV-7); a curator who wants the other two gets a record and a folder each. 984 of the fish compounds carry the fish value alone, 531 fish and Daphnia, 501 all three, 184 fish and algae.
        - Target: `LC50`, the published `pLC50 - FISH` plus 3, rounded back to the three decimals the file publishes. The deposit defines the field as "the log median lethal concentration measured at 96 hours", and the article states that "LC50 and EC50 values originally expressed in mg/l were transformed to the inverse log of the molar dose (pLC50 and pEC50 in mMol/L)" (p. 658); recomputing the value from the mg/L column as -log10(mg/L / molecular weight) matches the published value with a median absolute difference of 0.0003 over the 2,199 compounds that carry both, while -log10(mol/L) would differ by exactly 3. Adding 3 puts it on -log10(mol/L), the scale qsar_fish_toxicity ships, and leaves RMSE unchanged. The rounding removes the one or two units in the last place of floating-point residue the shift leaves on 307 values: no use to a model, since it is a function of a label it already holds, but a hint about how the file was built.
        - The mg/L column does not ship: it is the target in another unit. Where the two disagree it is the weaker column. They differ by more than 0.3 log on 34 of the 2,199 compounds (at most 1.19); on those 34 the published pLC50 is the closer of the two to an independent value of the same compound in 24 of the 25 cases that qsar_fish_toxicity's fathead-minnow set also holds and in 27 of the 28 that ADORE holds a fathead-minnow 96-hour LC50 for. One fish compound carries no mg/L value at all.
        - Censoring at a reporting limit (LEAK-22): a fish LC50 above the highest tested concentration is often reported as "greater than" a round number, which would pile up in the target. What the check found: 11 compounds sit at exactly 100.000 mg/L, the limit concentration of OECD test guideline 203, against 45 others spread over the band within 10% of it, and 9 of the 11 come from ECHA, NITE or the literature set; the most frequent value in mg/L is 13, tied with 1.4 and 1.5 at 12 compounds each, 1,000 mg/L appears once, and no operator column ships. The source excluded values reported as ranges and compounds above their measured water solubility, but could make the solubility comparison for only 743 of the fish compounds, so a limit value can have survived where the solubility was unknown. The values ship as they are; the pile-up is 0.5% of the rows.
        - The value is pooled over fish species and the file names none (USE-5). Measured against the ADORE release of the EPA's ECOTOX database (96-hour LC50 entries, matched on the CAS-RN, 2026-11-25): where ADORE holds a fathead-minnow value (801 compounds) this value is that value, median absolute difference 0.001 log units, 87.6% within 0.1, r 0.991; where it holds no fathead-minnow value but another fish species (481 compounds) it follows that species, median difference 0.059 and 61.0% within 0.1 over ADORE's fish entries (0.082 with its crustacean and algal entries left in the comparison); and where both are there (325 compounds) it is closer to the fathead minnow's on 263 and to the other species' on 60. The agreement is not circular: on the compounds whose `DB` names neither ECOTOX nor EPAFHM it is as good (86.9% within 0.1, r 0.996). So the target is the fathead minnow's value where that fish was tested and another fish's elsewhere, which is what a classification dossier reports and what a model fitted here predicts. ADORE's own species disagree by about as much as a model errs: fathead minnow against rainbow trout r 0.927, with 67.7% of the shared chemicals within 0.5 log.
        - How several experimental values became one value, from the source's own description of its collection (article p. 658): only measurements made under the conditions of the OECD test guideline were kept - the recommended test organism, mortality read at 96 hours, larval-stage studies discarded, and "the value must be precisely determined (i.e. values reported as ranges were excluded)"; then "In case of multiple values per compound, the median was taken as a representative value. When the ratio between the minimum and the maximum reported value per compound was >10, the entry was discarded"; compounds above their measured water solubility or unstable in water were excluded; and the structures were standardised, with salts and solvents removed, stereochemistry dropped and duplicates removed on the standardised SMILES. So the target is the median of the guideline values a compound had, not an average over everything published, and a compound whose sources spread by more than a factor of ten carries no value at all. 1,328 of the 2,200 fish compounds name two or more source databases, up to eight. The agreement with ADORE's single-species values above is the independent check on the rule: where one species covers a compound, the pooled value is that species' value.
        - The deposit holds more fish compounds than the article models: the paper reports 2,110 fish compounds (p. 658 and its Table 2) against the 2,200 that carry a fish value in the file, while its algae (1,440) and Daphnia (2,120) counts match the file exactly. What the 90 extra compounds are is not stated; they ship like the rest.
        - `DB`, the list of source databases, does not ship. It is not a property of the chemical but a record of how the source filled its table (CLEAN-22), and it is not known for an untested substance, which is the prediction point (LEAK-1). Over the fish compounds it names ten labels, counting each compound's names once, of which one is a collection of articles rather than a database and one is plausibly another name for one already in the list: Literature set 1,299, ECOTOX 980, VEGA 860, ECHA 857, OASIS 619, EPAFHM 389 (the EPA's fathead minnow database), NITE 375, EFSA 64, ECOTOX-EPA 49 (plausibly ECOTOX again) and Aquatic ECETOC 46. On 77 compounds an entry carries a number in brackets (`ECOTOX(76)`, `ECHA(10)`), always 10 or above, which looks like a count of underlying values and is nowhere explained. The deposit's description says only that "Litterature set" means an article, "see the companion article of the dataset for details". Dropping it costs a small and consistent amount: on the shipped splits (3 repeats, untuned LightGBM, 2026-11-25) the ten source flags and their count alone reach RMSE 1.225 against 1.281 for the training mean, and beside the structure 0.713 against 0.717 - 0.005 RMSE, better on 25 of the 30 folds, p 1.5e-5, which is less than the 0.025 spread over folds but not noise. It is dropped regardless, because it is not known for an untested substance.
        - The identifiers and the columns computed from the structure leave: `CdId` (the file's row number), `CASRN` (an identifier, written with and without dashes and leading zeros), `Formula`, `Mol Weight` and `Molecular weight` (the formula and the weight follow from the structure, CLEAN-24), `endpoint` (which endpoints a compound carries, a record of the collection, not of the chemical), and the five value columns the target does not use: the Daphnia and algae values in both units, and the fish value in mg/L.
        - The structure ships as `SMILES` (CLEAN-24), declared in `special_features`, so a benchmark encodes it as a structure and never as text; the recommended encoding is `data_foundry.special.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts). The values are RDKit's canonical form of the published `SMILES_Canonical` field. All 3,680 parse, none holds a `.`, so there are no salts or mixtures to split, and none carries stereochemistry, so no stereoisomer pair has to be decided (LEAK-18).
        - Copies (LEAK-19): the file draws 14 substances twice, 28 of the 2,200 fish rows. A substance is the rows an InChIKey skeleton or a CAS-RN (its digits, leading zeros stripped) ties together; neither key alone finds all 14 (the skeleton finds 8, the CAS-RN 12). The two rows of a pair are the same measurement entered twice: their targets differ by at most 0.151 and by 0.002 in the median (at most 0.014 on the three pairs the registry repairs below). In 11 pairs the two drawings share a molecular formula and are tautomers of one compound (a chlorinated hydroxypyridine drawn as the pyridinone and as the hydroxypyridine; a hydroxyazobenzene as its azo and its hydrazone form), and one row is kept, the one whose `DB` names more sources, ties by the file's order. In 3 pairs the formulas differ, so one of the two drawings is a different chemical: CAS 275-51-4 is drawn as C10H8 and as C10H18, its fully saturated form, CAS 3347-22-6 as C14H4N2O2S2 and C14H6N2O2S2, and CAS 104653-34-1 as C31H23BrO2S and C31H25BrO2S. The registry settles all three, so the pair is repaired rather than dropped: azulene is C10H8, dithianon C14H4N2O2S2 and difethialone C31H23BrO2S (PubChem, read 2026-11-25), and the row carrying that formula is the one that stays (`REGISTRY_FORMULA`). The source count is no substitute for it - it would have kept the wrong drawing in all three pairs, the azulene drawn as C10H18 naming two sources against the right drawing's one, and the difethialone pair tying at two each so that the file's order decided. The kept dithianon row carries no `Molecular weight` and no mg/L value, so the unit cross-check above cannot be made on it. 2,186 compounds remain, no two of them one substance.
        - Split (SPLIT-31): grouped on the Bemis-Murcko scaffold of the structure (`scaffold_groups`); a chemical without a ring, and each chemical of a scaffold holding more than a tenth of the set, is a group of its own. An assessor estimates the toxicity of an untested substance, often of a series not yet measured, so whole series are held out; qsar_fish_toxicity, qsar_bioconcentration, qsar_oral_toxicity and qsar_tid_11 group the same way. The source split at random within its own modelling.
        - Covers qsar_fish_toxicity (908 fathead-minnow chemicals, Cassotti et al. 2015): on the shipped rows this set holds 807 of those 908 (88.9% by canonical SMILES with the stereo set aside, 785 by CAS-RN) at the same values (r 0.995, median absolute difference 0.0009, 570 of the 807 within 0.01) and adds 1,379 chemicals. Another compilation by another group from overlapping public pools, so its own record (PROV-4); qsar_fish_toxicity was retired on 2026-11-26 as a `Duplicate` of this set (PROV-6, Andrej), its chemicals a near-complete cut of the same data at the same values. The Daphnia endpoint of this file is the sibling of qsar_aquatic_toxicity in the same way, and holds 374 of its 546.
        - The file's row order carries no clock: the records are the published SMILES in alphabetical order (only one of the 3,680 is out of that order), so neighbouring rows are near-analogs and the target repeats along the order - that is what the time probe's `order_drift` flags, a lag-1 autocorrelation of 0.33, not a trend with the row number (Spearman -0.03, p 0.18). The order is the leading atom of the structure, bromine first and the aromatic carbons last, not when a value was measured. The base class shuffles the rows regardless.
        - The companion article is open and was read (PROV-17): the publisher's copy is paywalled, but the first author's thesis reproduces it, deposited at https://theses.fr/2020STRAF016/document (the Strasbourg repository serves the PDF), and the journal pages 655-675 are reproduced in it. Pages 658, 660 and 661 give the collection rule, the criterion the authors' search optimises and what they report for the models, all quoted above and in the metric's definition. Unread: Table S5 of the supporting information, which holds the formulas behind the reported r2 and RMSE and which the publisher gates; what it says would settle whether the criterion their search maximises ranks models exactly as rmse does (see the metric).
        - The metric is the source's own (MET-5, MET-11): `rmse` on the shipped scale is the number the article compares models by every time it ranks one against another - its own models against the ECHA ones (p. 668) and against ECOSAR, VEGA and T.E.S.T. (p. 669), and the abstract's headline "RMSE_ext = 0.56-0.78 ... in line with those of state-of-the-art models". For the fish endpoint this record ships, the public consensus model scores RMSE 0.73 with r2 0.67 in fivefold cross-validation repeated ten times and RMSE 0.61 with r2 0.73 on the external test set at 66% data coverage (Tables 4 and 5, p. 666 and p. 668), and the final model merged with the industrial data RMSE 0.69. What the article selects models by is the cross-validated determination coefficient (p. 660), which ranks models exactly as rmse does if it is 1 - MSE/Var(y); that formula sits in the unread Table S5, so the metric's definition states the identity rather than resting on it. Declaring r2 itself would make the numbers depend on each fold's spread - the article shows it, since the ECHA fish model has the lower cross-validated RMSE (0.60 against 0.73) while the public one has the higher r2 (0.67 against 0.64) - and would break the comparison with qsar_fish_toxicity on the same target and scale. No score and no row changes either way.
        - What a model fitted here is good for (USE-8): these rows are the public cut of the authors' collection, which they extended with industrial data and where they report that "industrial data performances were noticeably lower than those on public data", so an inventory of that kind is harder than these folds suggest. The error grows with the distance to the training side: measured over three repeats of the shipped splits, RMSE 0.87 on the 30.5% of scored test rows whose nearest training chemical is below 0.40 Tanimoto, against 0.49 where it is above 0.9. And the label has a floor of its own: the article's Figure 3 puts the agreement between the collected databases on the fish endpoint at RMSE 0.55 to 0.67, against the 0.715 an untuned LightGBM reaches here, so the headroom above today's models is smaller than an R2 of 0.67 suggests.
        - Licence: the deposit states CC BY 4.0.
    """
    split_leaf = "L-FAMILY.key"
    time_basis = TimeBasis(
        "UnseenGroup",
        """
        the use case predicts for substances not tested yet, which whole scaffolds held out stand for. A chemical's
        96-hour fish LC50 is a property of the chemical, and the rows are a 2020 cut of public databases that keep
        growing. The file itself keeps no test date, species or condition, but a parent source dates the entries
        behind it: ECOTOX, through the ADORE release of its mortality tests, holds an entry for 1,444 of the 2,186
        chemicals (66.1%) and dates each one, 1985 to 2022 by the record's own date; the sibling qsar_fish_toxicity
        was dated the same way, 850 of its 908 chemicals. Those dates do not set the split. The authors aim their
        models at chemicals like the ones they collected and benchmark an industrial inventory separately, not at the
        next entries of ECHA or ECOTOX (SPLIT-37, step 3), and the target barely moves with the entry date (Spearman
        -0.03). The split cannot test a chemistry that entered those databases after 2020.
        """,
    )

    # Task
    target = "LC50"
    problem_type = "regression"
    metric = Metric.source(
        "rmse",
        original=(
            "the cross-validated determination coefficient the genetic algorithm maximises; the models are then "
            "reported and compared by r2 and RMSE"
        ),
        reference="https://theses.fr/2020STRAF016/document",
        definition=(
            "sqrt(mean((y - y_hat)**2)) on the shipped scale, minus the log of moles per litre. It is the number the "
            "article compares models by whenever it says one model is better than another: the abstract's "
            '"Reasonable predictive performances were achieved (RMSE_ext = 0.56-0.78) which are in line with those '
            'of state-of-the-art models", "their error (RMSE) is still higher than the ECHA models" (p. 668) and '
            '"ECOSAR is performing significantly worse than any model (RMSE = 1.57-1.94) ... our models are '
            'performing similarly to VEGA and T.E.S.T. tools, with comparable RMSE values" (p. 669). The criterion '
            'the authors deliberately select by, "Cross-validated determination coefficient was selected as fitness '
            "function\" (p. 660) of the genetic algorithm that picks each model's descriptor space and SVM "
            "hyperparameters, ranks every pair of models exactly as rmse does on a fixed test set if it is "
            "1 - MSE/Var(y), and differently if it is a squared Pearson correlation; which of the two the authors "
            "wrote down is in Table S5 of the supporting information, which the publisher gates and which is "
            "therefore unread (checked 2026-11-25). The models themselves are reported with r2 and RMSE side by "
            'side, "the r2 determination coefficient and the RMSE parameters" (p. 661).'
        ),
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the chemicals that share one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit from the structure. A chemical without a ring, or one of a scaffold that holds more than a tenth of the set, is a group of its own (SPLIT-31). A hazard assessor estimates the fish toxicity of an untested substance, often of a series not yet measured, so whole series are held out: the source's own aim is "the chemical space of the current chemical industry" rather than the next entries of the databases it collected (the deposit's description). Each row is one prediction, made from the chemical's structure alone.
        """,
    )

    # Splits
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all chemicals of one series stay on one side, so a model predicts chemicals of a series it has not seen. A chemical without a ring is held out on its own, and so is each chemical of the bare benzene scaffold, which holds more than a tenth of the set; those two carve-outs are 60.6% of the rows, and for them the split holds out nothing but the chemical itself. Chemicals with similar but not identical scaffolds can be on both sides.

        1,764 groups over 2,186 chemicals, 588 groups in each test fold (666 to 816 chemicals), and no group on both sides of any of the 30 splits. 1,654 chemicals are a group of their own: 676 without a ring, 649 of the bare benzene scaffold (29.7% of the set, far above the tenth at which a scaffold is no series) and 329 the only chemical of their scaffold. The other 110 groups are series of 2 to 46 chemicals, 532 chemicals in all.

        What the groups change, measured on three repeats of the shipped splits against three random 3-fold splits of the same rows (2026-11-25): no test chemical's group is in training, against 22.2% at random; but on the actual Bemis-Murcko scaffold, which the carve-outs do not group, 60.7% of the test chemicals still find their scaffold in training, against 82.8% at random. The test chemicals stay about as close to the training side either way: 12.3% have a training chemical at Tanimoto 0.7 or more (Morgan radius 2, 2,048 bits; median nearest 0.486) against 14.3% (0.506) at random.

        Where that two-point difference comes from: on the 861 chemicals the grouping can group, the split removes 57% of the close analogs (8.1% at random to 3.5%); on the 649 bare-benzene chemicals it removes none (14.0% to 14.2%) and on the 676 ring-less ones next to none (22.5% to 21.8%). So this split holds out a chemical series for two fifths of the rows and a single chemical for the rest, and it removes less overlap than the other molecule datasets of this family - qsar_bioconcentration 12.6% to 6.4%, qsar_oral_toxicity 24.7% to 16.3%, qsar_tid_11 79.7% to 59.2%, nci_aids_antiviral_screen 32.4% to 15.3% - while the nearest sibling, qsar_fish_toxicity, removes even less on the same measurement (12.4% against 13.1% at random, Andrej, 2026-11-12).
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return _read_sd_fields(raw_dir / RAW_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # The fish endpoint alone; the Daphnia and algae values of the same file are other tasks (curation_comments)
        df = raw[raw[VALUE_FIELD].notna()].copy()
        # The published value is -log10(mmol/L); +3 puts it on -log10(mol/L), qsar_fish_toxicity's scale. Rounded
        # back to the published 3 decimals, so the shift leaves no float residue that tells how the file was built
        df[self.target] = (df[VALUE_FIELD].astype(float) + MMOL_TO_MOL).round(3)
        # The structure ships as a SMILES column (`special_features`) in RDKit's canonical form; no fragments, no
        # stereochemistry in this file, so there is nothing to strip or to decide
        df["SMILES"] = canonical_smiles(df["SMILES_Canonical"])
        # One row per substance, the rows an InChIKey skeleton or a CAS-RN ties together (LEAK-19): where a substance
        # is drawn with two molecular formulas the registry's formula for its CAS-RN picks the row, the others keep
        # the row whose `DB` names more sources, ties by the file's order
        df = _one_row_per_substance(df)
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring, or a scaffold above a tenth, alone
        return pd.DataFrame(
            {
                "SMILES": df["SMILES"],
                self.target: df[self.target],
                "scaffold": scaffold_groups(df["SMILES"]),
            }
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The SMILES is typed by `special_features`; the target stays numeric
        del df
        return FeatureTypes()

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        fish = raw[raw[VALUE_FIELD].notna()].copy()
        fish[self.target] = (fish[VALUE_FIELD].astype(float) + MMOL_TO_MOL).round(3)
        fish["SMILES"] = canonical_smiles(fish["SMILES_Canonical"])
        fish = fish.assign(substance=_substance_key(fish), order=fish["CdId"].astype(int))
        pairs = fish[fish.groupby("substance")["substance"].transform("size").gt(1)].copy()
        pairs["drawings"] = pairs.groupby("substance")["Formula"].transform("nunique")
        pairs["kept"] = pairs["SMILES"].isin(df["SMILES"]).map({True: "kept", False: "dropped"})
        copies = pairs.sort_values(["drawings", "substance", "order"], kind="stable")[
            ["CASRN", "Formula", "SMILES", self.target, "DB", "kept"]
        ]
        spread = pairs.groupby("substance")[self.target].agg(lambda values: values.max() - values.min()).max()
        copies.index = range(1, len(copies) + 1)

        both = raw[raw[VALUE_FIELD].notna() & raw[MG_PER_L_FIELD].notna()].copy()
        published = both[VALUE_FIELD].astype(float) + MMOL_TO_MOL
        recomputed = -np.log10(both[MG_PER_L_FIELD].astype(float) / both["Molecular weight"].astype(float))
        gap = (recomputed + MMOL_TO_MOL - published).abs()
        units = pd.DataFrame(
            {
                "compounds": [len(both), gap.gt(0.1).sum(), gap.gt(0.3).sum(), gap.gt(1.0).sum()],
                "share": [1.0, *(gap.gt(level).mean().round(4) for level in (0.1, 0.3, 1.0))],
            },
            index=["with both columns", "differ by over 0.1 log", "over 0.3 log", "over 1 log"],
        )
        units.index.name = "the two value columns"
        return [
            Decision(
                "One row per substance where the file draws a chemical twice",
                "The file holds 14 substances twice, under two drawings and two rows, with the same measurement: the "
                f"two targets differ by at most {spread:.3f} log "
                "units. A substance is the rows one InChIKey skeleton or one CAS-RN ties together. Where the two "
                "drawings share a molecular formula they are tautomers of one chemical and the better-sourced row is "
                "kept; where the formulas differ, one drawing is another chemical and the formula the registry gives "
                "for the CAS-RN says which row stays (`REGISTRY_FORMULA`). Without this step the same measurement "
                "could sit on both sides of a split.",
                copies,
            ),
            Decision(
                "The published pLC50 is the target, not the value in mg/L",
                "The file gives the fish endpoint twice, as -log10(mmol/L) and in mg/L, and the two agree on almost "
                "every compound (median absolute difference 0.0003 log units). Where they disagree the published "
                "pLC50 is the one that matches independent values of the same compound: on the 34 compounds that "
                "differ by more than 0.3 log it is the closer of the two to qsar_fish_toxicity's fathead-minnow value "
                "in 24 of the 25 cases that set holds, and to ADORE's fathead-minnow 96-hour LC50 in 27 of 28. The "
                "mg/L column is the target in another unit either way, so it is not a feature.",
                units,
            ),
        ]


def _read_sd_fields(path: Path) -> pd.DataFrame:
    """The data fields of every record of the SD file, one row per record, every value as text.

    The connection tables are not read: the structure ships from the file's own `SMILES_Canonical` field. A record's
    fields follow its connection table as `>  <NAME>` lines, each with its value on the next line; a field a record
    does not carry is missing in that row.
    """
    records = []
    for block in path.read_text(encoding="utf-8").split("$$$$\n"):
        if not block.strip():
            continue
        _, _, fields = block.partition("\n>  <")
        pairs = re.findall(r"<([^>]+)>\n([^\n]*)", ">  <" + fields)
        records.append({name.strip(): value.strip() for name, value in pairs})
    return pd.DataFrame(records)


def _substance_key(df: pd.DataFrame) -> pd.Series:
    """One key per substance: the rows that share an InChIKey skeleton or a CAS-RN, chained through both keys.

    The InChIKey's first block is the connectivity, which merges the tautomer pairs the file draws twice; the CAS-RN
    (its digits, leading zeros stripped) catches the pairs whose two drawings differ beyond a standard InChI
    tautomer rule. Neither key alone finds all of them, so the key is the connected components of the two.
    """
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components

    skeleton = _inchikey_skeletons(df["SMILES"])
    cas = _cas_digits(df["CASRN"])
    # a row without a CAS-RN is tied to no other row by it (none in this file, but the key must not merge them)
    cas = cas.mask(cas.eq(""), "row " + df["CdId"].astype("string"))
    rows, columns, offset = [], [], len(df)
    for key in (skeleton, cas):
        codes, uniques = pd.factorize(key)
        rows.extend(range(len(df)))
        columns.extend(codes + offset)
        offset += len(uniques)
    links = coo_matrix((np.ones(len(rows)), (np.array(rows), np.array(columns))), shape=(offset, offset))
    _, labels = connected_components(links + links.T, directed=False)
    return pd.Series(labels[: len(df)], index=df.index, name="substance")


def _cas_digits(casrn: pd.Series) -> pd.Series:
    """The digits of a CAS-RN, leading zeros stripped: the file writes the same number with and without dashes."""
    return casrn.astype("string").fillna("").str.replace(r"\D", "", regex=True).str.lstrip("0")


def _inchikey_skeletons(smiles: pd.Series) -> pd.Series:
    """The first block of each molecule's standard InChIKey: its connectivity, which merges many tautomers."""
    from rdkit import Chem, RDLogger

    RDLogger.DisableLog("rdApp.*")
    keys = [Chem.MolToInchiKey(Chem.MolFromSmiles(value)).split("-")[0] for value in smiles]
    return pd.Series(keys, index=smiles.index, name="skeleton")


def _source_count(df: pd.DataFrame) -> pd.Series:
    """How many source databases the `DB` field names for each row, counting a name once.

    A few entries carry a number in brackets (`ECOTOX(76)`), and a row can list the same database with and without
    one, so the brackets go before the names are counted.
    """
    names = df["DB"].astype("string").fillna("").str.replace(r"\(\d+\)", "", regex=True).str.split(",")
    return names.apply(lambda parts: len({part.strip() for part in parts if part.strip()}))


def _one_row_per_substance(df: pd.DataFrame) -> pd.DataFrame:
    """One row per substance: where the two drawings differ in their molecular formula the registry says which of
    them is the substance, the others keep the row whose `DB` names more sources (ties by the file's order).
    """
    df = df.assign(substance=_substance_key(df), sources=_source_count(df), order=df["CdId"].astype(int))
    # a substance drawn with two formulas is drawn once as another chemical; the formula the registry gives for its
    # CAS-RN says which drawing is meant, and only a pair the registry does not settle loses both rows
    drawings = df.groupby("substance")["Formula"].transform("nunique")
    registry = _cas_digits(df["CASRN"]).map(REGISTRY_FORMULA)
    df = df[drawings.eq(1) | (registry.notna() & registry.eq(df["Formula"]))]
    kept = df.sort_values(["sources", "order"], ascending=[False, True], kind="stable")
    return df.loc[kept.index[~kept["substance"].duplicated()]]
