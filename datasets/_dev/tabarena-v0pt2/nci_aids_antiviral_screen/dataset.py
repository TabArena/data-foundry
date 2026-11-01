"""Curated dataset definition for `nci_aids_antiviral_screen` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    TaskSummary,
    canonical_smiles,
    scaffold_groups,
)
from data_foundry.v2.chemistry import RDKIT_VERSION

CONCLUSION_FILE = "aids_conc_may04.txt"
"""The screen's conclusion per compound (May 2004 release): NSC number and CA, CM or CI."""

EC50_FILE = "aids_ec50_may04.txt"
"""Averaged log10 EC50 per compound and highest tested concentration (May 2004); only the decision tables read it."""

IC50_FILE = "aids_ic50_may04.txt"
"""Averaged log10 IC50 on uninfected cells, as the EC50 file; only the decision tables read it."""

SD_FILE = "AIDO99SD.sdf"
"""The structures of October 1999 as an MDL SD file (AIDO99SD.BIN, uncompressed): NSC and CAS RN per record."""

PREPARED_FILE = "aido99sd_smiles.csv"
"""`_prepare_raw_files` writes one row per SD record: NSC, CAS RN, the SMILES as published without stereochemistry (the
file's charge code 4 read as +1), the SMILES without common salts and solvents (`compound`) and RDKit's error for a
record it cannot read."""

CONCLUSIONS = {
    "CA": "confirmed active",
    "CM": "confirmed moderately active",
    "CI": "confirmed inactive",
}
"""The screen's three conclusions, named as on the DTP page."""


class NciAidsAntiviralScreen(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "Does a compound protect human cells from HIV in the US National Cancer Institute's antiviral screen, and "
            "how strongly: confirmed active, moderately active or inactive, judged from its structure alone?"
        ),
        use_case=(
            "For example, a medicinal chemistry team ranks compounds it has not tested by their predicted anti-HIV "
            "activity and decides which to send to a cell-based antiviral screen such as the NCI's."
        ),
        row=(
            "One compound of the NCI's AIDS antiviral screen with a public structure and the screen's conclusion (May "
            "2004 release): 41,133 compounds, salt forms of one compound counted once, without the compounds tested "
            "with different conclusions."
        ),
        predicted=(
            "The screen's conclusion, read by trained staff from the compound's dose-response curves in infected "
            "cells: confirmed active (0.9%), confirmed moderately active (2.5%) or confirmed inactive (96.6%)."
        ),
        known=(
            "The compound's two-dimensional structure as tested, counter-ions included, without stereochemistry (the "
            "source has none), as a SMILES string that the benchmark encodes. Nothing measured in the screen."
        ),
        split=(
            "Whole chemical series are held out: compounds that share a ring skeleton stay on one side, so a test "
            "compound belongs to a series the model has not seen. Compounds without a ring are held out one by one."
        ),
        changes=(
            "We keep the screen's three conclusions, where other benchmarks merge the two active ones; join them to "
            "the structures by the NCI's compound number; read the structure file's charge code 4 as the +1 it means; "
            "drop structures RDKit cannot read and the stereochemistry "
            "the source did not draw; keep one row per compound (salt forms merged) and drop compounds tested with "
            "different conclusions; and split by series."
        ),
        fit="direct",
        fit_reason=(
            "The structure is known before a compound is screened, the label is the screen's own conclusion, and a "
            "held-out series stands for a series not yet tested: 15.3% of the test compounds have a close analog in "
            "training (Tanimoto 0.7 or more), against 32.4% under a random split. Compounds submitted together "
            "(consecutive NSC numbers) are not held out, a dependency kept on purpose that the splits comment "
            "measures."
        ),
    )

    # Dataset
    unique_name = "nci_aids_antiviral_screen"
    year = "2004"
    domain = "chemistry & material science"
    source = "GOV Website"
    source_url = "https://wiki.nci.nih.gov/display/NCIDTPdata/AIDS+Antiviral+Screen+Data"
    license = "Not stated (the DTP page names no terms; a release of the US National Cancer Institute)"
    download_description = """
        The files are the attachments of the NCI Developmental Therapeutics Program's "AIDS Antiviral Screen Data" page on the NCI wiki (source_url; attachments dated 2013-09-09): the screening results of May 2004 and the structures of October 1999. dtp.cancer.gov, whose bulk-data page lists the same files, served a certificate that expired on 2026-10-29. Downloaded 2026-11-01.

        mkdir -p local-data-warehouse/nci_aids_antiviral_screen && for f in aids_conc_may04.txt aids_ec50_may04.txt aids_ic50_may04.txt AIDO99SD.BIN; do wget -O local-data-warehouse/nci_aids_antiviral_screen/$f "https://wiki.nci.nih.gov/download/attachments/158204006/$f?version=1&modificationDate=1378736563000&api=v2"; done

        AIDO99SD.BIN is Unix `compress` (.Z) data, as the page says; gzip reads the format. Uncompress it into the SD file the definition reads:

        gzip -dc < local-data-warehouse/nci_aids_antiviral_screen/AIDO99SD.BIN > local-data-warehouse/nci_aids_antiviral_screen/AIDO99SD.sdf

        sha256 of aids_conc_may04.txt: a652638eefa255964a6ea8c0dc2dd2c71a8ad634def1d05877bc524619342410
        sha256 of aids_ec50_may04.txt: 1957694f7628e8b771ca98a2f7a29a7443b110bf0b417e82ae794f2d086b0bb4
        sha256 of aids_ic50_may04.txt: b0fe4562bc0a6bdf6293ba7ad1e1e28c1416c826555f5765d6b1f239c600e691
        sha256 of AIDO99SD.BIN: 823daad2fab43a5e37b1037fbd874f57556bf4932145b45ec20671ba5f36b9b7
        sha256 of AIDO99SD.sdf: db3a96d3540663551be8d376d8ef8318a2329f9698510f53a990ef0ef0d06ff2

        On first use, `_prepare_raw_files` reads the SD file with RDKit into aido99sd_smiles.csv: per record the NSC, the CAS RN, the SMILES as published without stereochemistry (the file's charge code 4 read as +1), and the SMILES without common salts and solvents.
    """
    bibtex = """
        @misc{nci_dtp_aids_antiviral_screen_2004,
          author={{National Cancer Institute, Developmental Therapeutics Program}},
          title={{AIDS} Antiviral Screen Data},
          year={2004},
          howpublished={\\url{https://wiki.nci.nih.gov/display/NCIDTPdata/AIDS+Antiviral+Screen+Data}},
          note={Screening results of May 2004 (aids\\_conc\\_may04.txt) and structures of October 1999 (AIDO99SD)}
        }
        @article{weislow1989new,
          title={New Soluble-Formazan Assay for {HIV-1} Cytopathic Effects: Application to High-Flux Screening of Synthetic and Natural Products for {AIDS}-Antiviral Activity},
          author={Weislow, Owen S. and Kiser, Rebecca and Fine, Donald L. and Bader, John and Shoemaker, Robert H. and Boyd, Michael R.},
          journal={Journal of the National Cancer Institute},
          volume={81},
          number={8},
          pages={577--586},
          year={1989},
          doi={10.1093/jnci/81.8.577}
        }
    """
    curation_comments = """
        We start with aids_conc_may04.txt (the screen's conclusion for 43,850 compounds, May 2004) and AIDO99SD (42,687 structures as an SD file, October 1999) from the NCI Developmental Therapeutics Program's AIDS Antiviral Screen page, joined by NSC number, the NCI's compound id.

        - Prediction point: a compound before it is screened. Its structure is known; the EC50 and IC50 of the screen, measured in the dose-response experiments the conclusion is read from, are not, so neither file is joined (only the decision tables read them).
        - Target: `screen_conclusion`, the screen's three conclusions (confirmed active, confirmed moderately active, confirmed inactive), "determined by inspection of individual dose response curves and is an overall judgment by trained personnel" (DTP page). The page states no thresholds, and the assay paper (Weislow et al. 1989) defines the assay, not the conclusions: it gives the primary screen's protocol ("we have implemented, as our high-flux primary anti-HIV-1 screen, the cell-free virus protocol ... using the HIV-1 (RF) virus with the CEM-SS host cell") and the rule the word "confirmed" comes from ("If a test substance shows at least 30% protection against virus-induced cytopathic effects in the host cells, the microculture XTT antiviral assay is repeated"), while the words "moderately" and "category" do not occur in it. The boundary between the two active classes is a DTP reporting convention that no publication we found states; what can be checked is that it tracks the source's own released numbers: on the 387 actives for which both an EC50 and an IC50 were reached (178 CA, 209 CM), the log10 selectivity index (IC50 over EC50) separates CA from CM at ROC AUC 0.948 and one threshold on it (1.07, a selectivity index of about 12) reproduces 89.7% of the labels; potency alone (the EC50) gives 0.915; and only 83 of the 42,038 CI compounds (0.2%) reached an EC50 at all. Kept as three classes (CLEAN-17), typed as an ordered category inactive < moderately active < active (CLEAN-25): the two active classes differ in potency (decision table: the EC50 was reached for 84.6% of CA and 40.7% of CM compounds, median log10 EC50 -6.08 and -4.55 M), and models tell them apart from the structure (ROC AUC 0.77 for CA against CM among the actives, 0.73 to 0.82 over the 9 shipped splits; untuned LightGBM on the recommended encoding, 1,407 columns, after the charge repair). MoleculeNet, OGB and HIVA merge CA and CM: as a binary task the same recipe gives 41,140 compounds, 1,404 active (3.4%), and the shipped compounds score ROC AUC 0.81 (0.79 to 0.83) for active against inactive on the same splits and encoding.
        - What the conclusion is a judgment about: the XTT assay reads protection of the host cells from the virus, and its paper names its false-positive modes, "nonspecific reduction of XTT by test compounds", "poorly understood drug-cell-XTT interactions" and "human error", with the rare "restoration of XTT formazan production (protection against viral cytopathic effects) without suppression of virus replication" (Weislow et al. 1989). Some actives can therefore be artefacts of the assay rather than antivirals, and a model fitted here predicts this screen, artefacts included. The task probes are a hint of it: the best single feature is RDKit's azide count on 3 of the 9 splits and its azo count on 2, two redox-active groups; whether they mark real actives or the assay's non-specific reduction of XTT is not settled here. No single feature is a shortcut to the task (skill 0.019 against the best family's 0.166).
        - Not a regression on the EC50: the page calls the EC50 and IC50 "computer generated averages and don't necessarily capture everything that was considered when making the judgement", and the EC50 was not reached in 38,048 of the 39,365 rows (censored at the highest concentration).
        - The join: 42,682 of the 43,850 conclusions have a structure (5 structures have no conclusion). The 1,168 without one are 26.5% active (3.5% of those with one): 254 were registered after the structure release (NSC above 706,805), and PubChem's DTP/NCI records of 25 sampled active ones hold no structure either (aurintricarboxylic acid polymer fractions, polyoxometalates, interferon-alpha, an oligonucleotide), substances without the small-molecule structure the task reads.
        - Reading the structures: the records lack the `M  END` line that closes an SD connection table; `_read_structures` adds it. The charge column has to be read as the file writes it: code 4, which V2000 defines as a doublet radical, sits on the motifs the file also writes code 3 (+1) on, four-bonded phosphorus (538 atoms against 81 with code 3), bare sodium (426 against 25) and bare potassium (24 against 11); and the file writes codes 8, 9 and -1 as well, which V2000 does not define, so its charge column is not the strict format. Read as V2000, those atoms come out neutral and RDKit fills the free valence with hydrogens the file does not draw (`[NaH]`, `[PH](c1ccccc1)(c1ccccc1)c1ccccc1`), so code 4 is read as +1 before the block is sanitized (`_plus_one_charge_codes`, PROV-13). It changes 723 records, 690 of the shipped compounds (50 CA, 66 CM, 554 CI), and makes 2 unreadable ones readable. RDKit still rejects the valences of 607 records (513 hold a metal, 69 more boron; a charged chlorine or oxygen bonded to it), which are dropped (1 CA, 15 CM, 591 CI). The 1,455 readable structures with a metal stay as the source draws them (coordination bonds as charged bonds, such as a copper -3 with three oxygens +1).
        - The repaired records are not charge-balanced: 631 of the 723 read net +1 and 42 net +2, because the source draws the partner anion protonated (a sodium phosphonate as the free acid beside `[Na+]`, NSC 224131) or draws no counter-ion at all (a phosphonium without its halide, NSC 4763). Deprotonating to balance them would be a fix of our own invention, not the source's drawing, so the drawing stays as published (P5 over P6).
        - Stereochemistry removed: "No stereochemical information was used in the build" of the 3D coordinates (DTP page), so the stereo RDKit reads from them (25,366 of 42,080 structures) is arbitrary; the shipped SMILES carries none, so it is also the key of rows a 2D encoding cannot tell apart.
        - The structure ships as `SMILES` (CLEAN-24 as amended, Lennart, 2026-11-01), declared in `smiles_columns`, so a benchmark encodes it as a structure and never as text; the recommended encoding is `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts: 1,407 columns on these compounds). The values are RDKit's canonical form (`canonical_smiles`) of the whole structure as published, every fragment kept. The NSC and the CAS RN are dropped (identifiers; 999-99-9 marks an unknown CAS RN). The draft of the same day shipped RDKit's descriptors in place of the string; on that draft's encoding (383 descriptor columns, before the charge repair) the whole structure scored as well as its largest fragment (untuned LightGBM log loss 0.1563 against 0.1578, ROC AUC 0.908 against 0.898 for confirmed active against the rest; 2 seeds x 3 scaffold-grouped folds).
        - Salt forms and copies (LEAK-19, LEAK-20): 3,130 of the 42,075 readable structures hold more than one fragment (counter-ions, which the file draws as bare cations such as `[Na+]`, solvents, complex partners). Salt forms of one compound are merged on the structure without RDKit's list of common salts and solvents (`FragmentRemover`: halides, metal ions, water, sulfate, ammonia, mesylate and others; organic counter-ions stay). The largest fragment is no such key here: in 57 groups (136 compounds) it would merge different compounds, such as dicyclohexylamine salts of different acids or crown-ether complexes of different tin compounds. 1,706 readable compounds share the key with another; the 46 compounds tested with different conclusions are dropped, all 119 rows (decision table), and of the others the first NSC is kept (823 rows dropped). 41,133 compounds remain: 386 CA, 1,011 CM, 39,736 CI, no two with one SMILES. 549 of them keep an organic counter-ion or a second component; the largest fragment of 47 of these is shipped as a compound of its own (a free form or another salt), 26 of them in another scaffold group, so a few near copies can sit across the split.
        - Split (SPLIT-31 as amended): grouped on the Bemis-Murcko scaffold of the compound, its structure without common salts and solvents (`scaffold_groups`): 20,772 groups, 15,993 compounds alone (1,566 without a ring, 3.8%) and 4,779 series of 2 to 2,086. No scaffold holds a tenth of the compounds, so the bare benzene ring (2,086, 5.1%) stays one group. Under the groups 15.3% of the test compounds of repeat 0 have a training analog at Tanimoto 0.7 or more (Morgan radius 2, 2,048 bits, on the structure without its salts; median nearest 0.516), against 32.4% under a random split (0.607); for the actives 29.2% against 49.8%. MoleculeNet and OGB split this screen by scaffold too, and a scaffold split leaves this screen similar across the split either way: 76.9% of our test compounds have a training compound above Tanimoto 0.4, against the 56% Lo-Hi (Steshin 2023, Sec. 5.2) measured on MoleculeNet's cut, so the test side is a series not yet tested, not a new chemical class. The NSC number counts submission batches that the groups do not hold out; the splits comment has the numbers.
        - Note: `hiva_agnostic` is the 2007 Agnostic Learning vs. Prior Knowledge challenge's cut of these compounds: its 4,229 labelled and 38,449 test compounds make 42,678, against the 42,682 conclusions with a structure here, and both are 3.52% active (149 of 4,229; 1,503 of 42,682). This release labels every compound and keeps the three conclusions; the curator decides which of the two ships (PROV-6).
        - Note: MoleculeNet's HIV.csv (41,127 compounds: 404 CA, 1,039 CM, 39,684 CI) is this SD file read by an older RDKit, salts and the stereo of the coordinates kept, and it carries the charge-code artefact repaired here: 413 `[NaH]`, 24 `[KH]` and 254 `[PH]` against 16 `[Na+]`, 11 `[K+]` and 56 `[P+]` (PROV-15, a problem of that copy; another collection's version is no reason to keep ours damaged, EV-4). So after the repair our structures differ from MoleculeNet's, and from OGB's `ogbg-molhiv` built on it, on the 690 compounds the repair touched: 40,385 of MoleculeNet's 41,116 InChIKey skeletons are among ours, where 41,077 were before the repair. Its conclusions agree with ours for 40,311 of the 40,343 stereo-free SMILES both hold; the other 32 are structures entered here under several NSC numbers with different conclusions, of which MoleculeNet kept one.
        - Licence: the DTP page states no terms.
    """

    # Task
    target = "screen_conclusion"
    problem_type = "multiclass_classification"
    metric = Metric.fallback(
        reason=(
            "The DTP release scores nothing: the screen concludes per compound. The benchmarks that defined a task "
            "on it merge CA and CM into one active class: MoleculeNet (Wu et al. 2018) and OGB score ROC-AUC on that "
            "binary label under a scaffold split ('for ogbg-molhiv, we use ROC-AUC for evaluation', "
            "ogb.stanford.edu/docs/graphprop), and the 2007 HIVA challenge ranked its binary cut by the balanced error "
            "rate. Both score a different target from the one shipped here: a ROC-AUC or a balanced error rate on CA "
            "and CM merged does not score how well the two active classes are told apart, and a metric keeps its "
            "meaning only when the target does (MET-2, third bullet). A macro or one-vs-rest ROC AUC is well defined "
            "on three classes, but it is not what either source scored. log_loss is the multiclass fallback (MET-11)."
        ),
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the compounds whose structure, without common salts and solvents, shares one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit. A compound without a ring (3.8%) is a group of its own; no scaffold holds more than a tenth of the compounds (the bare benzene ring 5.1%), so none is split up (SPLIT-31). A team that screens for antivirals meets new compounds, many of a series not yet tested, so whole series are held out, as MoleculeNet and OGB split this screen. Each row is one prediction, made from the structure alone.
        """,
    )
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold of the compound (its structure without common salts and solvents): all compounds of one series stay on one side, so a model predicts compounds of a series it has not seen; compounds without a ring are held out one by one. The bare benzene ring (5.1% of the compounds) is one group, below the tenth of the compounds above which a scaffold counts as no series. Compounds with similar but not identical scaffolds can be on both sides.

        The split still leaves the test compounds close to the training ones: 76.9% of the test compounds of repeat 0 have a training compound above Tanimoto 0.4 (86.5% of the actives), the median nearest is 0.516, and 15.3% have one at 0.7 or more (Morgan radius 2, 2,048 bits, on the structure without its salts). Lo-Hi (Steshin 2023, arXiv 2310.06399, Sec. 5.2) measured the same on MoleculeNet's cut of this screen, "56% of HIV test molecules have a train neighbor with a Tanimoto similarity > 0.4", and concludes it is unsuitable for hit identification. So the scores stand for a compound of a series that has not been tested; finding a chemical class nobody has seen is a harder task than this split measures.

        Potential leak, kept on purpose: the NSC number counts the compounds in the order they were registered, so neighbouring numbers are usually analogs submitted together. For two consecutive NSC numbers P(the next compound is active | this one is active) is 0.343 against a base rate of 0.034, and still 0.283 when the two sit in different scaffold groups; 81.6% of the test compounds of repeat 0 have a training compound within 5 NSC numbers, 7.6% one that is also a close analog (11.3% of the actives). The batch stays out of the group key because the NSC number is not shipped (the one feature column is the structure), so no model can recognise a submission batch; the only channel is structural resemblance, which the series grouping already holds out. Holding the batches out as well (the series key plus every NSC-adjacent pair that is also a close analog) lowers macro ROC AUC from 0.8215 to 0.8184, inside the 0.012 to 0.013 standard deviation over the folds (untuned LightGBM over the nine splits, measured on the frame before the charge repair); grouping whole runs of consecutive numbers instead gives 0.7961 with a fold spread of 0.023, and makes the folds uneven. sarcoma discloses its tissue source site the same way instead of grouping on it. Revisit if a release ships the NSC number or another submission key as a column.
    """

    smiles_columns = ("SMILES",)
    prepared_raw_files = (PREPARED_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        _read_structures(raw_dir / SD_FILE).to_csv(raw_dir / PREPARED_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        return {
            "conclusions": _read_table(raw_dir / CONCLUSION_FILE),
            "structures": pd.read_csv(raw_dir / PREPARED_FILE, dtype=str, keep_default_na=False),
            "ec50": _read_table(raw_dir / EC50_FILE),
            "ic50": _read_table(raw_dir / IC50_FILE),
        }

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        # The conclusions joined to the structures by NSC number, the source's key; 1,168 conclusions have none
        df = raw["conclusions"].merge(raw["structures"], on="NSC", how="inner", validate="one_to_one")
        # Structures whose valences RDKit rejects (mostly metal complexes and boron compounds)
        df = df[df["smiles"].ne("")]
        df = df.assign(**{self.target: df["Conclusion"].map(CONCLUSIONS)})
        # Salt forms and copies of one compound (the structure without common salts and solvents, LEAK-19): compounds
        # tested with different conclusions are dropped, the others keep the row of their first NSC number
        df = _one_row_per_compound(df, self.target)
        # The structure as tested, salts included, ships as a SMILES column (`smiles_columns`) in RDKit's canonical
        # form; its stereo, read from coordinates built without any, was removed in `_read_structures`
        # The split groups: the chemical series (Bemis-Murcko scaffold of the compound); a compound without a ring alone
        return pd.DataFrame(
            {
                "SMILES": canonical_smiles(df["smiles"]),
                self.target: df[self.target],
                "scaffold": scaffold_groups(df["compound"]),
            }
        )

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The SMILES is typed by `smiles_columns`. The target is an ordered category (CLEAN-25): the screen's three
        # conclusions are a potency scale, inactive < moderately active < active (decision table 2).
        del df
        return FeatureTypes(
            ordinal={self.target: ["confirmed inactive", "confirmed moderately active", "confirmed active"]}
        )

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        conclusions = raw["conclusions"]
        joined = conclusions.merge(raw["structures"], on="NSC", how="left")
        readable = joined[joined["smiles"].fillna("").ne("")]
        n_conclusions = readable.groupby("compound")["Conclusion"].transform("nunique")
        kept = _one_row_per_compound(readable, "Conclusion")
        order = list(CONCLUSIONS)
        steps = pd.DataFrame(
            {
                "conclusions": conclusions["Conclusion"].value_counts(),
                "with a structure (NSC)": joined.loc[joined["smiles"].notna(), "Conclusion"].value_counts(),
                "structure read by RDKit": readable["Conclusion"].value_counts(),
                "compound with one conclusion": readable.loc[n_conclusions.eq(1), "Conclusion"].value_counts(),
                "shipped, one per compound": kept["Conclusion"].value_counts(),
            }
        ).reindex(order)
        steps.loc["total"] = steps.sum()
        steps.index = [
            f"{CONCLUSIONS.get(code, code)} ({code})" if code in CONCLUSIONS else code for code in steps.index
        ]
        steps.index.name = "conclusion"

        ec50, ic50 = _reached(raw["ec50"], "Log10EC50"), _reached(raw["ic50"], "Log10IC50")
        by_class = conclusions.set_index("NSC")["Conclusion"]
        potency = pd.DataFrame(
            {
                "compounds": by_class.value_counts(),
                "with an EC50 in molar units": by_class[by_class.index.isin(ec50.index)].value_counts(),
                "EC50 reached (share)": ec50["reached"].groupby(by_class).mean().round(3),
                "median log10 EC50 where reached": ec50.loc[ec50["reached"], "log10"].groupby(by_class).median(),
                "IC50 reached (share)": ic50["reached"].groupby(by_class).mean().round(3),
                "median log10 IC50 where reached": ic50.loc[ic50["reached"], "log10"].groupby(by_class).median(),
            }
        ).reindex(order)
        potency.index = [f"{CONCLUSIONS[code]} ({code})" for code in potency.index]
        potency.index.name = "conclusion"

        active = readable.assign(active=readable["Conclusion"].isin(["CA", "CM"]))
        binary = _one_row_per_compound(active, "active")
        mixed = readable[n_conclusions.gt(1)]
        combination = mixed.groupby("compound")["Conclusion"].agg(lambda codes: " and ".join(sorted(set(codes))))
        conflicts = pd.DataFrame(
            {
                "compounds": combination.value_counts(),
                "NSC numbers": mixed["compound"].map(combination).value_counts(),
            }
        )
        conflicts.index.name = "conclusions of one compound"
        conflicts.loc["total"] = conflicts.sum()
        return [
            Decision(
                "From the screen's conclusions to the shipped compounds",
                "The conclusions are joined to the structures by NSC number; structures RDKit cannot read are "
                "dropped; a compound (the structure without common salts and solvents) tested with different "
                f"conclusions is dropped, and one NSC number per compound is kept. {len(df):,} compounds remain.",
                steps,
            ),
            Decision(
                "The three conclusions are kept",
                "The two active classes differ in how potent the compound is: the moderately active compounds reach "
                "their EC50 (half protection of the infected cells) less often and at higher concentrations, and "
                "their IC50 (half growth inhibition of uninfected cells) lies closer to it. The EC50 and IC50 are "
                "averages per highest tested concentration; a compound counts as reached when one average is not "
                "censored at the highest concentration. They are evidence only, never features. Merged into one "
                f"active class, as MoleculeNet, OGB and HIVA do, the recipe gives {len(binary):,} compounds, "
                f"{int(binary['active'].sum()):,} of them active.",
                potency,
            ),
            Decision(
                "Compounds tested with different conclusions are dropped",
                "A salt and its free form, or one compound under two NSC numbers, that the screen concluded "
                "differently: one compound with no single conclusion, so all its rows go (LEAK-20). CA, CM and CI are "
                "the screen's codes.",
                conflicts,
            ),
        ]


def _one_row_per_compound(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """Drop the compounds whose rows carry different ``label`` values, and keep the row of the first NSC of the others."""
    df = df.sort_values("NSC", key=lambda nsc: nsc.astype(int), kind="stable")
    df = df[df.groupby("compound")[label].transform("nunique").eq(1)]
    return df[~df["compound"].duplicated()]


def _reached(table: pd.DataFrame, column: str) -> pd.DataFrame:
    """Per NSC, whether an EC50 or IC50 file reached the value in molar units, and the lowest log10 value reached.

    The files hold one average per compound and highest tested concentration; the flag `>` marks an average censored
    at the highest concentration in at least one experiment, `=` and `<` a value reached.
    """
    molar = table[table["ConcUnit"].eq("M")].assign(log10=lambda t: t[column].astype(float))
    reached = molar[molar["Flag"].ne(">")]
    out = pd.DataFrame(index=pd.Index(molar["NSC"].unique(), name="NSC"))
    out["reached"] = out.index.isin(reached["NSC"])
    out["log10"] = reached.groupby("NSC")["log10"].min()
    return out


def _read_table(path: Path) -> pd.DataFrame:
    """A DTP text file: comma separated, every line padded with spaces to 80 characters; all values as text."""
    table = pd.read_csv(path, dtype=str)
    table.columns = table.columns.str.strip()
    return table.apply(lambda column: column.str.strip())


def _plus_one_charge_codes(table: str) -> str:
    """The connection table with charge code 4 in its atom block rewritten to code 3, the code for +1.

    The V2000 charge field (columns 37 to 39 of an atom line, `[36:39]` counted from zero) holds a code, not a charge:
    3 is +1, 5 is -1, and 4 is a doublet radical. This file does not follow that spec, since it also writes codes 8,
    9 and -1, which V2000 does not define; and it writes code 4 on the motifs it writes code 3 on, four-bonded
    phosphorus (538 atoms against 81 with code 3), bare sodium (426 against 25) and bare potassium (24 against 11).
    Those are cations in a screening sample, so code 4 is +1 here. Read as the spec reads it, the atom comes out
    neutral and RDKit fills its free valence with hydrogens the file does not draw (`[NaH]`,
    `[PH](c1ccccc1)(c1ccccc1)c1ccccc1`), so the code is rewritten before the block is parsed and sanitized.

    A connection table whose counts line does not parse is returned unchanged; reading it then fails as before.
    """
    lines = table.split("\n")
    try:
        n_atoms = int(lines[3][:3])
    except (IndexError, ValueError):
        return table
    atoms = [
        line[:36] + "  3" + line[39:] if len(line) >= 39 and line[36:39].strip() == "4" else line
        for line in lines[4 : 4 + n_atoms]
    ]
    return "\n".join(lines[:4] + atoms + lines[4 + n_atoms :])


def _read_structures(path: Path) -> pd.DataFrame:
    """Each record of the SD file as its NSC, CAS RN, its SMILES without stereochemistry, and that SMILES without common
    salts and solvents.

    The records end their connection table without the `M  END` line that closes a V2000 block, which RDKit needs,
    so it is added before the block is read, and the charge code 4 the file writes for a cation is rewritten to the
    code RDKit reads as +1 (`_plus_one_charge_codes`). The source built the 3D coordinates with Corina without
    stereochemical information ("No stereochemical information was used in the build"), so the stereo that RDKit
    reads from the coordinates is arbitrary and is removed, with the hydrogens that only carried it. `compound` drops
    the fragments of RDKit's list of common salts and solvents (`FragmentRemover`: halides, metal ions, water,
    sulfate, ammonia and others; organic counter-ions stay), so a salt and its free form share it. A record whose
    valences RDKit rejects gets empty SMILES and the error.
    """
    from rdkit import Chem, RDLogger, __version__
    from rdkit.Chem.MolStandardize import rdMolStandardize

    if __version__ != RDKIT_VERSION:
        msg = f"The structures need RDKit {RDKIT_VERSION}, found {__version__}."
        raise ValueError(msg)
    RDLogger.DisableLog("rdApp.*")
    remover = rdMolStandardize.FragmentRemover()
    rows = []
    for block in path.read_text(encoding="ascii").split("$$$$\n"):
        if not block.strip():
            continue
        table, _, fields = block.partition("\n> <")
        data = dict(re.findall(r"<([^>]+)>\n([^\n]*)", "> <" + fields))
        block_v2000 = _plus_one_charge_codes(table.rstrip("\n")) + "\nM  END\n"
        molecule = Chem.MolFromMolBlock(block_v2000, sanitize=False, removeHs=False)
        row = {
            "NSC": data["NSC"].strip(),
            "CAS_RN": data["CAS_RN"].strip(),
            "smiles": "",
            "compound": "",
            "rdkit_error": "",
        }
        try:
            if molecule is None:
                msg = "the connection table does not parse"
                raise ValueError(msg)
            Chem.SanitizeMol(molecule)
            Chem.RemoveStereochemistry(molecule)
            molecule = Chem.RemoveHs(molecule)
            row["smiles"] = Chem.MolToSmiles(molecule)
            row["compound"] = Chem.MolToSmiles(remover.remove(molecule))
        except ValueError as problem:  # RDKit's sanitization errors are ValueErrors
            row["rdkit_error"] = str(problem)
        rows.append(row)
    return pd.DataFrame(rows)
