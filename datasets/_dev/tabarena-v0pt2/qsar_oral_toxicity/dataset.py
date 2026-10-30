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
    TaskSummary,
    drop_columns,
    rdkit_descriptors,
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
        known=(
            "The chemical's structure, with salts, solvents and stereochemistry removed, as 1,024 on/off fingerprint "
            "bits and 208 descriptors computed from it."
        ),
        split=(
            "Whole chemical series are held out: chemicals that share a ring skeleton stay on one side, so a test "
            "chemical belongs to a family the model has not seen. Chemicals without a ring and those whose skeleton "
            "is the bare benzene ring are held out one by one. Salt forms and hydrates of one compound are kept once."
        ),
        changes=(
            "We add the project's evaluation set to the calibration set UCI holds, compute descriptors from the "
            "structure in place of its text, and drop exact copies, the fingerprints that occur with both classes "
            "and second rows of a parent structure, and split by chemical series; the source fixed one training, test "
            "and evaluation set."
        ),
        fit="approximate",
        fit_reason=(
            "The screening is simulated: the test rows are tested chemicals, held out by series but still closer to "
            "the training chemicals than the untested ones a screener faces (16.3% against 11.0% have a close analog,"
            " Tanimoto 0.7 or more; 24.7% under a random split). The score follows that distance (random forest ROC "
            "AUC 0.715 for distant chemicals, 0.945 for close ones, under the random split)."
        ),
    )

    # Dataset
    unique_name = "qsar_oral_toxicity"
    year = "2019"
    domain = "chemistry & material science"
    source = "Other"  # the Milano group's package of the paper; UCI 508 is a copy of two of its three sets
    source_url = "https://michem.unimib.it/download/data/acute-oral-systemic-toxicity/"
    license = "Freeware, to be used with a reference to the paper (the package's readme); the UCI copy is CC BY 4.0"
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
    bibtex = """
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
    """
    curation_comments = """
        We start with vt_data.mat of the authors' package: the very toxic (VT) endpoint of the ICCVAM "Predictive Models for Acute Oral Systemic Toxicity" project (rat oral LD50 data; its consensus models became CATMoS) with the fingerprints of Ballabio et al. (2019). It holds the project's three sets, 11,886 chemicals (6,744 training, 2,248 test, 2,894 evaluation), each with 1,024 ECFP bits in two variants, the class, and the chemical's CASRN, name, QSAR-ready SMILES and InChIKey. UCI 508 is the ECFP_1024_02 block of the first two sets: its 8,992 rows and classes equal them row by row (decision table), so the dataset UCI gives is this one without the evaluation set (Lennart, 2026-10-21: extend, and use the further feature data).

        - Prediction point: a chemical without an acute oral toxicity test, before any animal test. Every feature is computed from its QSAR-ready structure (salts, solvents and stereochemistry removed), so all of them exist at prediction time.
        - Target: `very_toxic` is "Yes" when the rat oral LD50 is 50 mg/kg or less (the package's class 1, the UCI file's "positive"; paper, Sec. 2.1; CATMoS Methods, "LD50<=50mg/kg"). On the evaluation set the label equals the project's EPA category 1 on all 2,894 rows and `LD50 <= 50` on every row that carries a dose; 2,845 of the kept chemicals (26%) carry the category without a point LD50.
        - Reading the raw file: MATLAB stores the text fields as `string` objects, which `scipy.io.loadmat` leaves undecoded, so `_prepare_raw_files` reads them out of the file's subsystem data (the decoder is documented in `_matlab_strings`) and writes bits, class and text per chemical into vt_data_02.csv. Checks of that step: the decoded "very toxic" field agrees with the `class_*` vectors on all 11,886 rows; the InChIKey has the right shape on every row and is reproduced by RDKit from the row's own SMILES for 99.8% of rows (99.99% on the skeleton, the one exception being the repaired silicon carbide below), so the SMILES is the structure the row is about; the evaluation rows match the project's public `validationset.txt` by its RowID on all 2,894 rows, with the same InChIKey, class and QSAR-ready SMILES, and the calibration rows match `trainingset_171130.txt` by CASRN (8,837) or, where a CASRN was mangled into a date by spreadsheet software, by InChIKey (155), with 100% class agreement.
        - Features, the fingerprint: binary extended connectivity fingerprints (paper, Sec. 2.2) computed with Dragon 7 (Sec. 2.7), radius 2 with 2 bits per fragment, the package's ECFP_1024_02 block (the variant its models use for this endpoint), 1,024 hashed bits, named `ecfp_1` to `ecfp_1024` in file order and typed categorical, the house form for 0/1 presence flags (CLEAN-14; Lennart, 2026-10-21). No bit is constant and no two bits are equal.
        - Features, the structure: RDKit's 2D descriptors of the QSAR-ready SMILES as `rdkit_*` columns (`rdkit_descriptors`, RDKit 2026.03.6), 208 of the 217, the others constant here or copies; values RDKit cannot compute (partial charges and BCUT descriptors of 12 chemicals) are missing. They decide: default LightGBM's ROC AUC over the 9 shipped splits is 0.885 on the bits alone and 0.901 with the descriptors added (better on 9 of 9 splits); the descriptors alone give 0.897, a random forest (500 trees) on repeat 0 0.901 against 0.912.
        - `rdkit_Ipc_log10`: RDKit's information content of the molecular graph grows exponentially with the molecule (five chemicals above 1e38, the largest 6e166), beyond any float32 pipeline, so `rdkit_descriptors` ships it as log10(1 + Ipc) for every SMILES dataset (Lennart, 2026-10-21); a tree model sees the same order.
        - `smiles` dropped, as in every SMILES dataset (2026-10-14).
        - Repaired row, 1: the QSAR-ready SMILES of silicon carbide (CASRN 409-21-2) gives silicon five bonds and no toolkit reads it; we use PubChem's structure for that CASRN. Its bits stay the package's.
        - 122 of the kept QSAR-ready structures still carry stereo markers, which the fingerprint ignores (two stereo forms can share a vector).
        - Duplicates dropped: the salt forms, hydrates and stereoisomers of one compound share the QSAR-ready parent structure and so the bit vector (594 repeated vectors over 1,314 rows; a few are hash collisions of different chemicals rather than one parent). We drop the 732 exact copies and then every row of the 20 bit vectors that occur with both classes (52 rows), as for wine_quality and jm1; nine parents still keep two rows with different vectors (tautomer or salt entries, all "No"), of which we drop the later row, so a test chemical never has its parent structure in train. 11,105 chemicals remain (931 very toxic, 8.4%; decision tables). The source kept the copies: 237 evaluation rows repeat a calibration vector (236 repeat a calibration InChIKey).
        - Note: the class depends on the counter-ion in some cases (sodium and potassium cyanide are very toxic, silver cyanide is not), which the parent structure does not show.
        - Split (Lennart, CC 2026-10-26, SPLIT-31 as amended; reopened from IID): grouped on the Bemis-Murcko scaffold of the QSAR-ready SMILES (`scaffold_groups`), 3 folds with 3 repeats. Chemicals without a ring (2,577, 23%) and those whose skeleton is the bare benzene ring (1,969, 18%: more than a tenth of the set and no series) are groups of their own. Since the extension of 2026-10-21 every row has its own QSAR-ready structure (InChIKey reproduced for 99.8%), so the scaffold is exact; the earlier reason for IID, structures linked by row order, no longer holds. All three source sets are random draws ("without supervised sampling of the chemicals based on structures", Mansouri et al. 2021), and the package's fixed training and test sets are not kept.
        - Note: the score depends on how close a test chemical is to the training chemicals, the applicability domain of any QSAR model (random forest ROC AUC 0.715 below a Tanimoto similarity of 0.5 to the nearest training chemical, 9.6% of test rows, and 0.945 above 0.7). Chemotypes carry part of that: held out by their Murcko scaffold (2,577 acyclic chemicals each its own group, benzenes grouped) a random forest fell from 0.900 to 0.852 over 2 x 3 folds, with the model ranking unchanged (2026-10-21).
        - Fit: approximate (Lennart, 2026-10-21: "a more simulated use case than a direct real case"). The test chemicals are members of the tested reference set; the untested chemicals of the project's 48,137-chemical prediction set have fewer close analogs: 11.0% at Tanimoto 0.7 or more (Morgan radius 2, 2,048 bits; median nearest similarity 0.486), against 16.3% for the test chemicals under the scaffold groups (median 0.519) and 24.7% under a random split (0.573).
        - Scope: the features are a vectorised molecular graph, as in qsar_tid_11. On repeat 0 of the shipped splits a random forest on the bits (ROC AUC 0.901) and LightGBM (0.885) match a similarity-weighted nearest-neighbour model of the paper's N3 kind (Tanimoto, weight sim^10: 0.893).
        - Licence: the package's readme states it is freeware to be used with a reference to the paper; the UCI copy of the two calibration sets is CC BY 4.0.
    """

    # Task
    target = "very_toxic"
    problem_type = "binary_classification"
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

    accepted_check_warnings = {
        "dataset_pure_feature_value": "rdkit_fr_Ar_COO = 1 (one aromatic carboxylic acid group) marks 212 chemicals, "
        "1 of them very toxic: a fragment count of the QSAR-ready structure, computed before any animal test, so it "
        "cannot carry the outcome; aromatic acids are rarely acutely lethal (Lennart, 2026-10-21).",
    }

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
        # Salt forms, hydrates and stereoisomers of one parent structure share the bit vector: keep one row per
        # vector, and drop every vector that occurs with both classes.
        df = df.drop_duplicates(subset=[*BITS, self.target])
        df = df[~df.duplicated(subset=BITS, keep=False)]
        # A few parents keep two rows whose bits differ (a tautomer or salt entry under a second CASRN): keep the
        # first row of each InChIKey of the QSAR-ready structure.
        df = df[~df["inchikey"].duplicated()]
        # One QSAR-ready SMILES RDKit cannot read (a pentavalent silicon): PubChem's structure of the same chemical.
        df["smiles"] = df["smiles"].replace(SMILES_REPAIRS)
        # The structure as numbers: RDKit's 2D descriptors in place of the SMILES (data_foundry.v2.chemistry).
        df = pd.concat([df, rdkit_descriptors(df["smiles"])], axis=1)
        # The split groups: the chemical series (Bemis-Murcko scaffold); no ring or the bare benzene ring alone
        df = df.assign(scaffold=scaffold_groups(df["smiles"]))
        return drop_columns(df, ["set", "id", "casrn", "name", "smiles", "inchikey", "class"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        # The 1,024 bits are 0/1 presence flags: categorical (CLEAN-14). The descriptors stay numeric, the RDKit
        # fragment counts too where only 0 and 1 occur; the target becomes a category.
        del df
        return FeatureTypes(categorical=BITS)

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

        vector = pd.util.hash_pandas_object(package[BITS], index=False)
        copies = vector.map(vector.value_counts())
        classes = positive.groupby(vector).transform("nunique")
        kind = pd.Series("bit vector occurs once", index=package.index)
        kind[(copies > 1) & (classes == 1)] = "repeated bit vector, one class"
        kind[classes > 1] = "repeated bit vector, both classes"
        order = ["bit vector occurs once", "repeated bit vector, one class", "repeated bit vector, both classes"]
        duplicates = pd.DataFrame(
            {
                "rows": kind.value_counts(),
                "distinct bit vectors": vector.groupby(kind).nunique(),
                "distinct InChIKeys": package["inchikey"].groupby(kind).nunique(),
                "very toxic rows": positive.groupby(kind).sum(),
            }
        ).reindex(order)
        duplicates["rows kept"] = [
            duplicates.loc[order[0], "rows"],
            duplicates.loc[order[1], "distinct bit vectors"],
            0,
        ]
        duplicates.loc["total"] = duplicates.sum()
        duplicates.index.name = "rows of the package"

        kept = package[~package.duplicated(subset=[*BITS, "class"])]
        kept = kept[~kept.duplicated(subset=BITS, keep=False)]
        twice = kept[kept["inchikey"].duplicated(keep=False)]
        pairs = pd.DataFrame(
            [
                {
                    "InChIKey": key,
                    "row kept": f"{group['set'].iloc[0]} {group['casrn'].iloc[0]}",
                    "row dropped": f"{group['set'].iloc[1]} {group['casrn'].iloc[1]}",
                    "bits in common": int((group[BITS].iloc[0].to_numpy() & group[BITS].iloc[1].to_numpy()).sum()),
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
                "The bits are computed from the QSAR-ready parent structure, so salts, hydrates and stereoisomers "
                "of one compound share the bit vector (a few repeated vectors are hash collisions of different "
                "chemicals instead). One row per vector is kept, and vectors with both classes are dropped, which "
                f"leaves {len(kept):,} chemicals before the rows of the next decision.",
                duplicates,
            ),
            Decision(
                "Parents that survive twice reduced to one row",
                "The InChIKeys of the QSAR-ready structures show parents in two kept rows whose bits differ (a free "
                f"acid and its salt or tautomer under two CASRNs). We keep the first row of each, so {len(df):,} "
                "chemicals remain.",
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
