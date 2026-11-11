"""Curated dataset definition for `qsar_oral_toxicity` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Grouping,
    Metric,
    Smiles,
    Source,
    TaskSummary,
    canonical_smiles,
    drop_columns,
    scaffold_groups,
)

PACKAGE_FILE = "vt_data.mat"
"""The very toxic data of the authors' package: per set the ECFP bits, the class and the molecules' text fields."""

PREPARED_FILE = "vt_data_02.csv"
"""`_prepare_raw_files` writes the three sets of `vt_data.mat` into this file, one row per chemical."""

UCI_FILE = "qsar_oral_toxicity.csv"
"""The UCI copy of the training and test sets (1,024 bits, then the class); only the decision tables read it."""

N_BITS = 1024
"""The ECFP_1024_02 block holds 1,024 bits."""

BITS = [f"ecfp_{i + 1}" for i in range(N_BITS)]
"""The bit columns, named in the package's order."""

SETS = ("train", "test", "validation")
"""The package's three sets, in the order the prepared file stores them: the calibration set's training and test
part (the UCI file, in this order), then the project's evaluation set."""

TEXT_COLUMNS = {
    "train": {"id": 0, "casrn": 1, "name": 3, "smiles": 5, "inchikey": 8},
    "test": {"id": 0, "casrn": 1, "name": 3, "smiles": 5, "inchikey": 8},
    "validation": {"id": 0, "casrn": 1, "name": 3, "smiles": 6, "inchikey": 9},
}
"""Positions of the text fields we keep in the package's 11-column `molecules_<set>` arrays.

The readme names the columns IDS, CASRN, DTXSID, Chemical_Name, Structure_Source, Canonical_QSARr, Salt_Solvent,
InChI_Code_QSARr, InChI_Key_QSARr, LD50_mgkg and very toxic. In the validation set they are shifted by one: column 6
holds the original SMILES, column 7 the QSAR-ready one and so on, and the LD50 is missing (the project's
`validationset.txt` has the same values in the order RowID, CASRN, DTXSID, Name, Structure_Source, SMILES_Original,
Canonical_QSARr, ...). The CASRN is shown in the decision tables only; spreadsheet software turned 206 of them into
dates.
"""

SMILES_REPAIRS = {"C#[SiH2+]": "[C-]#[Si+]"}
"""Silicon carbide (CASRN 409-21-2): the package's QSAR-ready SMILES gives silicon five bonds, which RDKit rejects;
PubChem's SMILES for the CASRN (checked 2026-10-21) replaces it. The bits stay the package's."""


class QsarOralToxicity(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="Is a chemical very toxic when swallowed, judged from its structure alone?",
        use_case=(
            "A regulator or a chemical maker screens chemicals without animal test data and flags the very toxic "
            "ones, to set priorities and labels without new animal tests (the US ICCVAM project behind the CATMoS "
            "models)."
        ),
        row=(
            "One chemical of the calibration and evaluation sets of the US ICCVAM acute oral toxicity project, with "
            "rat test data (11,105 chemicals after removing salt forms and copies)."
        ),
        predicted=(
            "Whether the swallowed dose that kills half of the rats is 50 mg per kg of body weight or less, the top "
            "acute oral hazard category (8% are very toxic). A quarter of the chemicals carry that category without "
            "a measured dose."
        ),
        known=("The chemical's structure, with salts, solvents and stereochemistry removed, as a SMILES string."),
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side, so a test "
            "chemical belongs to a family the model has not seen. Chemicals without a ring and those whose skeleton "
            "is the bare benzene ring are held out one by one. Salt forms and hydrates of one compound are kept once."
        ),
        changes=(
            "We add the project's evaluation set to the calibration set UCI holds, ship the structure as a SMILES "
            "string in place of the authors' fingerprint, drop exact copies, the structures that occur with both "
            "classes and second rows of a compound, and split by chemical series; the source fixed one training, test "
            "and evaluation set."
        ),
        fit="approximate",
        fit_reason=(
            "The screening is simulated: the test rows are tested chemicals, held out by series (16.3% have a close "
            "analog at Tanimoto 0.7 or more, against 24.7% under a random split). The project's untested "
            "prediction set is a weaker reference than it looks: a fifth of it is not untested, since 9,588 of its "
            "48,137 chemicals share a QSAR-ready InChIKey with one here, and 31.4% of it has a close analog among "
            "them. The score follows the distance to training (random forest ROC AUC 0.715 for distant chemicals, "
            "0.945 for close ones, under the random split)."
        ),
    )

    # Dataset
    unique_name = "qsar_oral_toxicity"
    domain = "chemistry & material science"
    sources = (
        Source(
            role="publication",
            platform="Other",  # the Milano group's package of the paper; UCI 508 is a copy of two of its three sets
            url="https://michem.unimib.it/download/data/acute-oral-systemic-toxicity/",
            license="Freeware, to be used with a reference to the paper (the package's readme)",
            year="2019",
            bibtex="""
                @article{ballabio2019integrated,
                  title={Integrated {QSAR} Models to Predict Acute Oral Systemic Toxicity},
                  author={Ballabio, Davide and Grisoni, Francesca and Consonni, Viviana and Todeschini, Roberto},
                  journal={Molecular Informatics},
                  volume={38},
                  number={8-9},
                  pages={1800124},
                  year={2019},
                  doi={10.1002/minf.201800124}
                }
                @article{mansouri2021catmos,
                  title={{CATMoS}: Collaborative Acute Toxicity Modeling Suite},
                  author={Mansouri, Kamel and Karmaus, Agnes L. and Fitzpatrick, Jeremy and Patlewicz, Grace and Pradeep, Prachi and others},
                  journal={Environmental Health Perspectives},
                  volume={129},
                  number={4},
                  pages={047013},
                  year={2021},
                  doi={10.1289/EHP8495}
                }
            """,
        ),
        Source(
            role="copy",
            platform="UCI",
            url="https://archive.ics.uci.edu/dataset/508/qsar+oral+toxicity",
            license="CC BY 4.0",
            name="UCI 508, two of the package's three sets",
        ),
    )
    download_description = """
        The data comes from the Milano Chemometrics and QSAR Research Group's package of Ballabio et al. (2019):
        download form on their site (source_url; freeware, cite the paper). The package is a RAR archive of MATLAB
        code and data; we use only vt_data.mat, the very toxic endpoint. Ours is a copy the curator provided.
        Extract vt_data.mat into local-data-warehouse/qsar_oral_toxicity/ (any RAR tool, for example
        `unrar e oral_toxicity_data.rar vt_data.mat local-data-warehouse/qsar_oral_toxicity/`).

        sha256 of oral_toxicity_data.rar: 27ef3dffd32c515ba0963fdced5fb27d57d2547f2bffb2770cacda9240769a68
        sha256 of vt_data.mat: 2c0b1e35a05781ac0e181134e22a7008a20726c945e8f9a3e0cba3c4ba6e7f57

        The decision tables also read the UCI copy of the training and test sets (dataset 508, donated by the same
        group in 2019, CC BY 4.0):

        wget -P local-data-warehouse/qsar_oral_toxicity/ https://archive.ics.uci.edu/static/public/508/qsar+oral+toxicity.zip && unzip local-data-warehouse/qsar_oral_toxicity/qsar+oral+toxicity.zip -d local-data-warehouse/qsar_oral_toxicity/ && rm local-data-warehouse/qsar_oral_toxicity/qsar+oral+toxicity.zip

        sha256 of qsar_oral_toxicity.csv: c8ec16179f505370c13491a2c98e0918aae3680270aad0a6f95de3aeb300c874

        On first use, `_prepare_raw_files` decodes the three sets of vt_data.mat (bits, classes and the text fields,
        which MATLAB stores as string objects) into vt_data_02.csv.
    """
    curation_comments = """
        We start with vt_data.mat of the authors' package: the very toxic (VT) endpoint of the ICCVAM "Predictive Models for Acute Oral Systemic Toxicity" project (rat oral LD50 data; its consensus models became CATMoS) with the fingerprints of Ballabio et al. (2019). It holds the project's three sets, 11,886 chemicals (6,744 training, 2,248 test, 2,894 evaluation), each with 1,024 ECFP bits in two variants, the class, and the chemical's CASRN, name, QSAR-ready SMILES and InChIKey. UCI 508 is the ECFP_1024_02 block of the first two sets: its 8,992 rows and classes equal them row by row (decision table), so the dataset UCI gives is this one without the evaluation set (Lennart, 2026-10-21: extend, and use the further feature data).

        - Prediction point: a chemical without an acute oral toxicity test, before any animal test. Every feature is computed from its QSAR-ready structure (salts, solvents and stereochemistry removed), so all of them exist at prediction time.
        - Target: `very_toxic` is "Yes" when the rat oral LD50 is 50 mg/kg or less (the package's class 1, the UCI file's "positive"; paper, Sec. 2.1; CATMoS Methods, "LD50<=50mg/kg"). On the evaluation set the label equals the project's EPA category 1 on all 2,894 rows and `LD50 <= 50` on every row that carries a dose; 2,845 of the kept chemicals (26%) carry the category without a point LD50.
        - Reading the raw file: MATLAB stores the text fields as `string` objects, which `scipy.io.loadmat` leaves undecoded, so `_prepare_raw_files` reads them out of the file's subsystem data (the decoder is documented in `_matlab_strings`) and writes bits, class and text per chemical into vt_data_02.csv. Checks of that step: the decoded "very toxic" field agrees with the `class_*` vectors on all 11,886 rows; the InChIKey has the right shape on every row and is reproduced by RDKit from the row's own SMILES for 99.8% of rows (99.99% on the skeleton, the one exception being the repaired silicon carbide below), so the SMILES is the structure the row is about; the evaluation rows match the project's public `validationset.txt` by its RowID on all 2,894 rows, with the same InChIKey, class and QSAR-ready SMILES, and the calibration rows match `trainingset_171130.txt` by CASRN (8,837) or, where a CASRN was mangled into a date by spreadsheet software, by InChIKey (155), with 100% class agreement.
        - The authors' fingerprint leaves (Lennart, 2026-11-01, as for qsar_tid_11: the task goes from the structure to a prediction, and the bits are one modelling choice of the authors): 1,024 binary extended connectivity bits (paper, Sec. 2.2) computed with Dragon 7 (Sec. 2.7), radius 2 with 2 bits per fragment, the package's ECFP_1024_02 block. Until 2026-11-01 they shipped as `ecfp_1` to `ecfp_1024`; the definition still reads them, to check the package against the UCI file.
        - The structure ships as `SMILES`, the one feature: the QSAR-ready SMILES in RDKit's canonical form (`canonical_smiles`), declared in `special_features` (CLEAN-24 as amended, Lennart, 2026-11-01), so a benchmark encodes it as a structure and never as text; the recommended encoding is `data_foundry.v2.chemistry.encode_smiles` (RDKit's 2D descriptors, `Ipc` as log10(1 + Ipc) since the largest reaches 6e166, the 166 MACCS keys and the ECFP4 counts). Measured before 2026-11-01 on the shipped splits: default LightGBM's ROC AUC was 0.885 on the authors' bits, 0.897 on RDKit's descriptors alone and 0.901 on both; the MACCS keys next to bits and descriptors changed it by +0.009 (LightGBM) and -0.003 (random forest).
        - Accepted on 2026-10-21 and now outside the frame: the descriptor `rdkit_fr_Ar_COO` = 1 (one aromatic carboxylic acid group) marks 212 chemicals, 1 of them very toxic, a pure feature value; a fragment count of the QSAR-ready structure, computed before any animal test, so it cannot carry the outcome (Lennart, 2026-10-21). The recommended encoding still holds it.
        - Repaired row, 1: the QSAR-ready SMILES of silicon carbide (CASRN 409-21-2) gives silicon five bonds and no toolkit reads it; we use PubChem's structure for that CASRN.
        - 83 of the kept QSAR-ready structures still carry stereo marks (double-bond geometry); a 2D encoding ignores them.
        - Duplicates dropped, by structure (since 2026-11-01; by bit vector before): the salt forms, hydrates and stereoisomers of one compound share the QSAR-ready parent structure, the same 2D structure once the stereo marks are set aside (`canonical_smiles(..., stereo=False)`; 605 repeated structures over 1,345 rows). We drop the 720 exact copies and then every row of the 20 structures that occur with both classes (52 rows), as for wine_quality and jm1; ten compounds still keep two rows that are one InChIKey (tautomers the SMILES writes differently, all "No"), of which we drop the later row, so a test chemical never has its parent structure in train. 11,116 chemicals remain (933 very toxic, 8.4%; decision tables), 11 more than with the bit vectors, whose collisions had joined different chemicals. The source kept the copies: 233 evaluation rows repeat a calibration structure.
        - Note: the class depends on the counter-ion in some cases (sodium and potassium cyanide are very toxic, silver cyanide is not), which the parent structure does not show.
        - Split (Lennart, CC 2026-10-26, SPLIT-31 as amended; reopened from IID): grouped on the Bemis-Murcko scaffold of the QSAR-ready SMILES (`scaffold_groups`), 3 folds with 3 repeats. Chemicals without a ring (2,579, 23%) and those whose skeleton is the bare benzene ring (1,973, 18%: more than a tenth of the set and no series) are groups of their own. Since the extension of 2026-10-21 every row has its own QSAR-ready structure (InChIKey reproduced for 99.8%), so the scaffold is exact; the earlier reason for IID, structures linked by row order, no longer holds. All three source sets are random draws ("without supervised sampling of the chemicals based on structures", Mansouri et al. 2021), and the package's fixed training and test sets are not kept.
        - Time basis: Timeless: whether a chemical is very toxic when swallowed is a property of the chemical, and the use case fills in an inventory that already exists rather than predicting for chemicals made later. The chemicals can be dated (7,927 of 11,116, 71.3%, from the RTECS citation years EPA's ToxValDB keeps per ChemIDplus record, 1932 to 2023, median about 1979), and a split by that year was measured against the scaffold folds: it holds out less chemistry, not more. Trained on the earlier years, the test chemicals keep a close training analog as often as a random draw of the same size (12.4% against 13.1%, and 8.6% when the training side is drawn scaffold-disjoint), and 31.5% of them share a scaffold with training, against none under the shipped split; ROC AUC is 0.770 forward and 0.770 scaffold-disjoint (random forest). The report year separates when somebody ran the test, not which chemistry a screener has not met. What the split cannot test is a chemical class that enters the inventory later (Andrej, 2026-11-11; evidence in the record's review).
        - Note: the score depends on how close a test chemical is to the training chemicals, the applicability domain of any QSAR model (random forest ROC AUC 0.715 below a Tanimoto similarity of 0.5 to the nearest training chemical, 9.6% of test rows, and 0.945 above 0.7). Chemotypes carry part of that: held out by their Murcko scaffold (2,577 acyclic chemicals each its own group, benzenes grouped) a random forest fell from 0.900 to 0.852 over 2 x 3 folds, with the model ranking unchanged (2026-10-21).
        - Fit: approximate (Lennart, 2026-10-21: "a more simulated use case than a direct real case"). The test chemicals are members of the tested reference set, held out by series: 16.3% have a close analog in training (Tanimoto 0.7 or more, Morgan radius 2, 2,048 bits; median nearest similarity 0.519), against 24.7% under a random split (0.573). The project's 48,137-chemical prediction set was read as the screening population at 11.0% (median 0.486), but it overlaps this data: 9,588 of its chemicals (19.9%) share a QSAR-ready InChIKey with one here and 7,295 a CASRN, 22.4% of it matches one of them on the fingerprint exactly, and 31.4% has a close analog among them (median 0.571). The 11.0% holds only once the identical chemicals are set aside, so the gap to a real screening population is less well pinned down than that one number suggests (2026-11-11).
        - Scope: the input is the molecular structure, as in qsar_tid_11. Before 2026-11-01, on repeat 0 of the shipped splits, a random forest on the authors' bits (ROC AUC 0.901) and LightGBM (0.885) match a similarity-weighted nearest-neighbour model of the paper's N3 kind (Tanimoto, weight sim^10: 0.893).
        - Licence: the package's readme states it is freeware to be used with a reference to the paper; the UCI copy of the two calibration sets is CC BY 4.0.
    """

    # Task
    target = "very_toxic"
    problem_type = "binary_classification"
    data_tags = ("Timeless",)
    special_features = (Smiles(column="SMILES"),)
    metric = Metric.fallback(
        reason=(
            "Ballabio et al. 2019 report the non-error rate with sensitivity and specificity, the group's "
            "house measure, without costs; 8.4% very toxic. Original rejected: NER. roc_auc is the binary "
            "fallback."
        ),
    )

    grouping = Grouping(
        on="scaffold",
        labels="per_sample",
        prediction_unit="row",
        context="none",
        definition="""
            One group is a chemical series: the chemicals that share one Bemis-Murcko scaffold (ring systems and the chains linking them; Bemis and Murcko 1996), computed with RDKit from the QSAR-ready SMILES. A chemical without a ring (23%), or with the bare benzene ring (18%, more than a tenth of the set), is a group of its own (SPLIT-31). The screen meets untested chemicals, many of series without animal data, so whole series are held out. Each row is one prediction, made from the chemical's structure alone.
        """,
    )
    splits_comment = """
        Grouped splits on the Bemis-Murcko scaffold: all chemicals of one series stay on one side, so a model predicts chemicals of a series it has not seen; chemicals without a ring and those with the bare benzene ring are held out one by one. Chemicals with similar but not identical scaffolds can be on both sides.
    """

    prepared_raw_files = (PREPARED_FILE,)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        frames = [_package_set(raw_dir / PACKAGE_FILE, name) for name in SETS]
        pd.concat(frames, ignore_index=True).to_csv(raw_dir / PREPARED_FILE, index=False)

    def _load_raw(self, raw_dir: Path) -> dict[str, pd.DataFrame]:
        package = pd.read_csv(raw_dir / PREPARED_FILE, dtype={"casrn": str, "name": str}, keep_default_na=False)
        uci = pd.read_csv(raw_dir / UCI_FILE, sep=";", header=None)
        return {"package": package, "uci": uci}

    def _clean(self, raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        df = raw["package"]
        df = pd.concat([df, df["class"].map({1: "Yes", 2: "No"}).rename(self.target)], axis=1)
        # One QSAR-ready SMILES RDKit cannot read (a pentavalent silicon): PubChem's structure of the same chemical.
        df["smiles"] = df["smiles"].replace(SMILES_REPAIRS)
        # Salt forms, hydrates and stereoisomers of one compound are one 2D structure: keep one row per structure,
        # and drop every structure that occurs with both classes.
        flat = canonical_smiles(df["smiles"], stereo=False)
        keep = ~pd.DataFrame({"structure": flat, "class": df["class"]}).duplicated()
        df, flat = df[keep], flat[keep]
        df = df[~flat.duplicated(keep=False)]
        # Tautomers the SMILES writes differently are one compound to its InChIKey: keep the first row of each.
        df = df[~df["inchikey"].duplicated()]
        # The structure ships as a SMILES column (`special_features`), in RDKit's canonical form; the authors' bits
        # leave, one modelling choice of the structure (curation_comments)
        df = df.assign(SMILES=canonical_smiles(df["smiles"]))
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring or the bare benzene ring alone
        df = df.assign(scaffold=scaffold_groups(df["SMILES"]))
        return drop_columns(df, ["set", "id", "casrn", "name", "smiles", "inchikey", "class", *BITS])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The SMILES is typed by `special_features`; the target becomes a category.
        del df
        return FeatureTypes()

    def _decisions(self, raw: dict[str, pd.DataFrame], df: pd.DataFrame) -> list[Decision]:
        package, uci = raw["package"], raw["uci"]
        positive = package["class"].eq(1)

        calibration = package.iloc[: len(uci)]
        equal = (calibration[BITS].to_numpy() == uci.iloc[:, :N_BITS].to_numpy()).all(axis=1) & (
            positive.iloc[: len(uci)].to_numpy() == uci[N_BITS].eq("positive").to_numpy()
        )
        sets = pd.DataFrame(
            {
                "rows": package["set"].value_counts(sort=False),
                "very toxic": positive.groupby(package["set"], sort=False).sum(),
                "rows equal to the UCI file": pd.Series(equal).groupby(calibration["set"].to_numpy()).sum(),
            }
        ).reindex(list(SETS))
        sets["rows equal to the UCI file"] = sets["rows equal to the UCI file"].astype("Int64").astype(str)
        sets.loc["validation", "rows equal to the UCI file"] = "not in UCI"
        sets.index.name = "set of the package"

        flat = canonical_smiles(package["smiles"].replace(SMILES_REPAIRS), stereo=False)
        copies = flat.map(flat.value_counts())
        classes = positive.groupby(flat).transform("nunique")
        kind = pd.Series("structure occurs once", index=package.index)
        kind[(copies > 1) & (classes == 1)] = "repeated structure, one class"
        kind[classes > 1] = "repeated structure, both classes"
        order = ["structure occurs once", "repeated structure, one class", "repeated structure, both classes"]
        duplicates = pd.DataFrame(
            {
                "rows": kind.value_counts(),
                "distinct structures": flat.groupby(kind).nunique(),
                "distinct InChIKeys": package["inchikey"].groupby(kind).nunique(),
                "very toxic rows": positive.groupby(kind).sum(),
            }
        ).reindex(order)
        duplicates["rows kept"] = [
            duplicates.loc[order[0], "rows"],
            duplicates.loc[order[1], "distinct structures"],
            0,
        ]
        duplicates.loc["total"] = duplicates.sum()
        duplicates.index.name = "rows of the package"

        kept = package[~pd.DataFrame({"structure": flat, "class": package["class"]}).duplicated()]
        kept = kept[~flat[kept.index].duplicated(keep=False)]
        twice = kept[kept["inchikey"].duplicated(keep=False)]
        pairs = pd.DataFrame(
            [
                {
                    "InChIKey": key,
                    "row kept": f"{group['set'].iloc[0]} {group['casrn'].iloc[0]}",
                    "row dropped": f"{group['set'].iloc[1]} {group['casrn'].iloc[1]}",
                    "SMILES kept": group["smiles"].iloc[0],
                    "SMILES dropped": group["smiles"].iloc[1],
                    "very toxic": bool(group["class"].eq(1).any()),
                }
                for key, group in twice.groupby("inchikey", sort=False)
            ]
        ).set_index("InChIKey")
        return [
            Decision(
                "The package's three sets, of which UCI holds two",
                "The training and test sets of the package's ECFP_1024_02 block equal the UCI file row by row; the "
                "validation set is the project's evaluation set, which UCI lacks. Both were drawn at random, so the "
                "scaffold-grouped cross-validation runs over all three.",
                sets,
            ),
            Decision(
                "Copies of a parent structure dropped",
                "The QSAR-ready structure drops salts and solvents, and a 2D encoding drops the stereo marks, so "
                "salts, hydrates and stereoisomers of one compound are one structure. One row per structure is kept, "
                f"and structures with both classes are dropped, which leaves {len(kept):,} chemicals before the rows "
                "of the next decision.",
                duplicates,
            ),
            Decision(
                "Parents that survive twice reduced to one row",
                "The InChIKeys of the QSAR-ready structures show compounds in two kept rows whose SMILES differ "
                f"(tautomers under two CASRNs). We keep the first row of each, so {len(df):,} chemicals remain.",
                pairs,
            ),
        ]


def _package_set(path: Path, name: str) -> pd.DataFrame:
    """One set of the package's `vt_data.mat` as a frame: the text fields we keep, the class and the 1,024 bits."""
    from scipy.io import loadmat

    mat = loadmat(path)
    strings = _matlab_strings(mat["__function_workspace__"].tobytes())
    molecules = mat[f"molecules_{name}"]
    text = {
        field: [_matlab_cell(row[column], strings) for row in molecules] for field, column in TEXT_COLUMNS[name].items()
    }
    out = pd.DataFrame({"set": name, **text, "class": mat[f"class_{name}"].ravel().astype("int64")})
    bits = pd.DataFrame(mat[f"ECFP_1024_02_{name}"].astype("int64"), columns=BITS)
    return pd.concat([out, bits], axis=1)


def _matlab_cell(value: np.ndarray, strings: dict[int, str]) -> str:
    """A cell of a `molecules_<set>` array as text: a number (the IDS column) or a MATLAB string object."""
    if value.dtype.names is None:
        return str(value.ravel()[0])
    reference = value[0]["arr"].ravel()  # (0xdd000000, dims, 1, 1, object id, class id)
    return strings[int(reference[4])]


def _matlab_strings(workspace: bytes) -> dict[int, str]:
    """Decode the MATLAB `string` objects of a MAT file's subsystem data, by object id.

    MATLAB keeps the content of objects in the `__function_workspace__` of the file: a small MAT stream whose first
    variable holds one cell array (MCOS FileWrapper__). Cell 0 is the metadata: after a version and a count, eight
    byte offsets to its regions; region 1 lists each object's saved properties (count, then name, flag, value per
    property, padded to 8 bytes), region 2 each object's class and property block (six integers). The property value
    of a `string` object points at cell `value + 2`, a uint64 array: version 1, the number of dimensions, the
    dimensions, the length of each string, then the UTF-16 characters.
    """
    from scipy.io import loadmat

    size = int(np.frombuffer(workspace[12:16], "<u4")[0])
    stream = io.BytesIO(b" " * 116 + b"\x00" * 8 + workspace[:4] + workspace[8 : 16 + size])
    cells = loadmat(stream)["__function_workspace__"][0, 0]["MCOS"][0]["arr"].ravel()
    metadata = np.frombuffer(cells[0].ravel().tobytes(), "<u4")
    offsets = metadata[2:10] // 4
    saved = metadata[offsets[1] : offsets[2]]
    objects = metadata[offsets[2] : offsets[3]].reshape(-1, 6)
    blocks, position = [], 2
    while position < len(saved):
        count = int(saved[position])
        blocks.append(saved[position + 1 : position + 1 + 3 * count].reshape(-1, 3))
        position += 1 + 3 * count + (1 + 3 * count) % 2
    out = {}
    for object_id in range(1, len(objects)):
        (_, flag, value), *rest = blocks[int(objects[object_id, 3]) - 1]
        if rest or flag != 1:
            msg = f"MATLAB object {object_id} is not a string with one saved property."
            raise ValueError(msg)
        data = cells[int(value) + 2].ravel()
        if data[0] != 1 or int(np.prod(data[2 : 2 + data[1]])) != 1:
            msg = f"MATLAB object {object_id} is not a single string."
            raise ValueError(msg)
        length = int(data[2 + data[1]])
        out[object_id] = data[3 + data[1] :].tobytes()[: 2 * length].decode("utf-16-le")
    return out
