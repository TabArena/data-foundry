"""Curated dataset definition for `chromophore_optical_properties_db`. Evidence: README.md."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize

from data_foundry.definition import (
    AbstractCuratedDataset,
    FeatureTypes,
    Metric,
    Smiles,
    Source,
    TaskSummary,
    Temporal,
    TemporalSplits,
    canonical_smiles,
)

RAW_FILE = "raw/DB_for_chromophore_v3.csv"
RAW_SHA256 = "f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c"
YEARS_FILE = "raw/crossref_years.csv"
"""The Crossref `issued` year of each distinct raw Reference (empty when Crossref has none), written once by the
recipe in `download_description`, so the build reads pinned years and never calls Crossref."""
YEARS_SHA256 = "3c617cb17b159439c95d74415c6643c6c86e34ba6caf23ec6ce42f05e9748c9c"
BETAINE_30 = "[O-]c1c(-c2ccccc2)cc(-[n+]2c(-c3ccccc3)cc(-c3ccccc3)cc2-c2ccccc2)cc1-c1ccccc1"
"""Reichardt's betaine dye 30 as the source writes it (the dye of the ET(30) solvent polarity scale)."""


def canonical_values(values: pd.Series, *, stereo: bool = True) -> pd.Series:
    """Canonicalize distinct structures once while preserving source-row indices."""
    unique = pd.Series(values.dropna().unique(), dtype="string")
    mapping = dict(zip(unique, canonical_smiles(unique, stereo=stereo), strict=True))
    return values.map(mapping).astype("string")


class ChromophoreOpticalPropertiesDb(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question="At what wavelength will a proposed dye have its first absorption peak in a specified environment?",
        use_case=(
            "A chemist screens proposed chromophore structures and their solvent or host environments before "
            "synthesis and spectroscopy, to choose candidates with useful light absorption."
        ),
        row="One literature-reported dye and environment measurement with a recorded first absorption-peak wavelength.",
        predicted="The first absorption-peak position, measured in nanometres, without a target transformation.",
        known=(
            "The dye structure and the solvent or host structure, or the source's neat-solid or gas-state designation."
        ),
        split=(
            "Each dye is dated by the year of its first paper, and each publication year from 2015 to 2020 is "
            "tested on the dyes first reported before it; every environment and measurement of a dye goes with "
            "its first year. Solvents may recur across training and testing."
        ),
        changes=(
            "Use the absorption target alone, omit other measured optical outcomes and provenance identifiers, "
            "canonicalize the structures, remove duplicate input-target records, drop the betaine dye's "
            "extrapolated gas-phase value and replace random-row splitting with windows by each dye's first "
            "publication year (Crossref year of its papers). Decode gas separately from a molecular solvent."
        ),
        fit="approximate",
        fit_reason=(
            "The structures exist before measurement, but literature selection and unrecorded conditions limit "
            "transport to new designs; the archive mixes solutions, hosts and neat solids, which a structure alone "
            "does not specify. The solvent moves the peak little next to the dye (SD 19.9 nm within a dye, 108.7 nm "
            "between dyes; LightGBM RMSE 53.9 nm with the solvent, 54.0 without, on scaffold folds), so scores "
            "mostly rank dye-structure models."
        ),
    )
    unique_name = "chromophore_optical_properties_db"
    sources = (
        Source(
            role="publication",
            platform="Other",
            url="https://doi.org/10.6084/m9.figshare.12045567.v3",
            license="CC BY 4.0",
            year="2020",
            bibtex="""
        @article{joung2020experimental,
          title={Experimental database of optical properties of organic compounds},
          author={Joung, Joonyoung F. and Han, Minhi and Jeong, Minseok and Park, Sungnam},
          journal={Scientific Data},
          volume={7},
          pages={295},
          year={2020},
          doi={10.1038/s41597-020-00634-8}
        }
    """,
        ),
    )
    domain = "chemistry & material science"
    download_description = """
        Download the publisher's v3 CSV (file 49887156), not the unversioned search webpage:

        mkdir -p local-data-warehouse/chromophore_optical_properties_db/raw
        curl -L --fail https://ndownloader.figshare.com/files/49887156 -o local-data-warehouse/chromophore_optical_properties_db/raw/DB_for_chromophore_v3.csv

        Publisher MD5: 565dbb010480d94e8bb41af1bfb75ea8. SHA256:
        f92a55144c46ca0a0ef063c5ea82996161d65ea5c21643796cdeb897e173994c.
        The downloaded CSV has 20,836 rows; the 2020 paper's 20,236 rows describe v2.

        Then date each paper once: the Crossref `issued` year of every distinct Reference string, written to
        raw/crossref_years.csv (Reference, year; empty where Crossref answers 400 or 404). The build reads this
        file and never calls Crossref:

        cd local-data-warehouse/chromophore_optical_properties_db
        python - <<'EOF'
        import csv, json, re, time, urllib.error, urllib.parse, urllib.request
        import pandas as pd
        def year(ref):
            doi = re.sub(r"^https?://(dx\\.)?doi\\.org/", "", ref.strip())
            url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
            for attempt in range(6):
                try:
                    request = urllib.request.Request(url, headers={"User-Agent": "dataset-curation/0.1"})
                    with urllib.request.urlopen(request, timeout=30) as f:
                        parts = (json.load(f)["message"].get("issued") or {}).get("date-parts") or [[None]]
                    return parts[0][0]
                except urllib.error.HTTPError as e:
                    if e.code in (400, 404):
                        return None
                except OSError:
                    pass
                time.sleep(2**attempt)
            raise RuntimeError(f"Crossref gave no answer for {ref!r}; run again")
        refs = sorted(pd.read_csv("raw/DB_for_chromophore_v3.csv")["Reference"].dropna().astype(str).unique())
        with open("raw/crossref_years.csv", "w", newline="") as f:
            writer = csv.writer(f, lineterminator="\\n")
            writer.writerow(["Reference", "year"])
            writer.writerows((ref, year(ref) or "") for ref in refs)
        EOF

        Written on 2026-11-24: 1,354 References, 1,240 with a year; SHA256
        3c617cb17b159439c95d74415c6643c6c86e34ba6caf23ec6ce42f05e9748c9c (pinned in `_load_raw`). It equals the
        table measured on 2026-11-21 except four References Crossref did not answer then (2011, 2011, 2013, 2017
        now). A later run that differs fails the pin: Crossref changed a record, and the windows must be checked again.
    """
    curation_comments = """
        - Prediction point: before synthesizing or measuring a candidate dye in its planned solvent, host or gas
          environment. Only the two structures and decoded medium state enter prediction.
        - The publisher's Figshare v3 file contains 20,836 rows and 17,703 nonmissing absorption values. Pin its exact
          bytes rather than reuse the paper's or metadata card's historical counts. Target values stay in nm.
        - The v3 source population includes small nonorganic species, metal complexes and structures with up to
          225 nonhydrogen atoms. Its scope is broader than the historical organic/150-atom description. Preserve
          published rows with absorption labels unless an origin-supported correction establishes an error.
        - Emission peak, both absorption/emission bandwidth representations, quantum yield, lifetime and extinction
          coefficient are other experimental outcomes, not inputs known at this prediction point. Tag is a row
          number and Reference a source DOI; both leave the inputs. Molecular weight leaves as a structure-derived
          quantity rather than an independent measurement needed by this task.
        - Both structures ship as typed SMILES in RDKit's canonical form, with fragments and stereochemistry kept.
          The benchmark encodes them; no descriptor or fingerprint chosen by the curator ships as a raw feature.
        - The source uses gas instead of solvent SMILES in 20 labeled rows. Preserve the 19 measured ones:
          medium_state is gas and Solvent_SMILES is missing because there is no solvent molecule. They come from
          papers of 1967-2006 (the 13 with a dated DOI); the small molecules at 128-143 nm (vacuum UV) are
          measurements kept at the margin of the dye use case. The twentieth, at 1,055 nm, is not a measurement
          and is dropped (dye 30 note below). When the source writes the same
          structure for dye and environment it denotes a neat solid; other structures can denote solvent or host.
          The latter state remains solvent or host because the release supplies no independent phase column.
          About 20 rows are doped films in OLED host matrices (such as CBP, mCP or DPEPO in the solvent column);
          the paper uses the solid matrix as the solvent, so they stay solvent or host, mixed with solutions.
        - Protonation and charge forms of one molecule (a merocyanine as phenol or phenolate/quinoid form, an
          oxime or its oximate, an acid or its anion) are distinct species with different wavelengths. They are
          separate dyes and may get different first years; aliases of one species share one.
        - Remove exact repeated model-input and target records after canonicalization. Distinct observed wavelengths
          for one dye/environment remain separate measurements: laboratory conditions and literature disagreement
          may reflect physical-condition variation or literature/transcription disagreement; this cause is not verified.
          No averaging or target-dependent conflict filtering is invented.
        - Input/target deduplication removes 193 labeled records (17,509 rows remain after the gas row below). Only 50 excess labeled rows also match every raw
          field except Tag; the other 143 removals are a weighting policy, not proven copies of physical experiments.
          Myunghwan approved that weighting on 2026-11-10 separately from retaining differing wavelengths.
        - Split by first publication year (Andrej, 2026-11-24): each dye (structure without stereochemistry,
          aliases with one nonempty InChIKey or one canonical tautomer joined) takes the earliest Crossref year over
          the papers of all its labeled rows, deduplicated ones included, and every row of the dye goes with that
          year (`first_year`, which orders and splits the rows and is no input). 6,367 of 6,498 dyes (98.0%;
          98.9% of rows) have a dated paper; the other 131 dyes (194 rows) take the earliest year, 1967, so they
          always train. The alias join moves 5 dyes (30 rows) to an alias's earlier year. The year is the
          literature entry, not the catalogue entry, as for apistox. Measured on 2026-11-21 with this dating
          (before the dedup-inclusive and alias refinements), the forward split leaves 4.8-8.9% of test dyes a
          close training analogue (Morgan radius 2, Tanimoto at least 0.7) against 58.3-63.1% for a random draw of
          the same number of dyes, and 0-11% of test rows a row of their own paper in training, against 58-65%
          under the former scaffold folds. Solvents recur; the test stands for the dyes the literature reports
          next, not new solvents.
        - The source paper compiles experimental values, not simulated quantum-chemistry labels. Most were read from
          the spectra of the cited papers; the 335 rows of Reichardt's betaine dye 30 (334 shipped) come from one
          review's ET(30) table instead (next note). Its model follow-up (JACS Au 2021, doi:10.1021/jacsau.1c00035)
          reports RMSE for absorption peak positions in nm. Its random-row scores and expanded database are not
          qualification results for our temporal release.
        - Reichardt's betaine dye 30 had 335 rows, all citing Reichardt, Chem. Rev. 1994 (doi:10.1021/cr00032a005).
          334 of them equal 28591/ET(30). ET(30) is defined from this dye's measured long-wavelength
          charge-transfer peak in kcal/mol, so these rows are measured peaks converted back to nm, rounded to the
          table's 0.1 kcal/mol (0.2-1.6 nm). Whether every tabulated solvent value was measured on dye 30 itself
          or derived from a secondary standard is unverified. The gas row (1,055 nm, ET(30) = 27.1), the scale's
          extrapolated gas-phase value, is dropped (Andrej, 2026-11-24); 334 rows of the dye remain, all first
          dated 1994, so the dye always trains.
        - Literature selection and missing temperature, concentration and some physical-state detail remain limits;
          no row is removed simply for an extreme wavelength. The 17,703 observed targets are positive and finite.
        - Curator decision (2026-11-10, Myunghwan), issues 1A and 2A: keep one row per canonical input and wavelength,
          and retain the 61 input sets with differing published responses. Apply the genuine-ambiguity clause for
          continuous measurements under incomplete conditions; the cause of each disagreement remains unverified.
          Grouping does not validate labels. Repair any later demonstrated source error from its original reference.
        - Myunghwan checked the declared fallback RMSE in untransformed nm and accepted the gas/no-solvent warning
          on 2026-11-10. These are scientific review decisions; no model-only gas accuracy claim follows.
        - Scoring per row, kept on purpose (Andrej, 2026-11-24): a dye measured in several media counts once per row, as in the source's RMSE. Under the six windows the dyes with 10 or more rows (5-10% of test dyes) carry 9-38% of a window's score, the 5 largest test dyes 3.4-18.5%, the largest 11-27 rows; Reichardt's betaine dye (334 rows) always trains. The solvent moves the peak little next to the dye (SD 19.9 nm within a dye against 108.7 nm between dyes), so the score measures dye structure either way.
        - Split walk (the split decision tree, SPLIT-36, from the record's collection type Expanding Science Catalogue): [CAT.next-items] the source aims at newly designed chromophores before synthesis, the items the catalogue adds next: yes → [CAT.entry-date] each dye is dated by the earliest Crossref year of its papers (98.0% of dyes), and the record has no `Target: Revised Later`: yes → [CAT.arrival] a forward split by that year leaves clearly fewer close training analogues than a random draw (4.8-8.9% against 58.3-63.1% of test dyes at Tanimoto 0.7): yes → [CAT.windows] one-year windows 2015 to 2020 each train on at least half the rows (51.1-98.3%): yes → leaf L-CAT.entry-date, Temporal · entry date, the split the definition ships (`split_leaf`; Andrej, 2026-11-24, issue 3 B and the Horizon B).
    """
    accepted_check_warnings = {
        "splits_dimensions_off_protocol": (
            "Accepted by Andrej on 2026-11-24 with the six one-year windows 2015-2020: 6 windows against the 9 an "
            "IID split of 17,509 rows would get; the 2014 window would train on 44.4% of the rows, under the "
            "half-the-rows floor, and the one-year length is the curator's sign-off (splits comment)."
        ),
        "dataset_smiles_column": (
            "Accepted by Myunghwan on 2026-11-10 for the 20 gas rows, 19 since Andrej dropped the betaine dye's "
            "extrapolated gas row on 2026-11-24: the gas-state observations have no solvent molecule. "
            "Solvent_SMILES is therefore absent by definition, with medium_state=gas explicitly retained; "
            "these are not rows with an unexplained missing molecular input."
        ),
    }
    target = "Absorption max (nm)"
    problem_type = "regression"
    special_features = (Smiles(column="Chromophore_SMILES"), Smiles(column="Solvent_SMILES"))
    metric = Metric.fallback(
        reason=(
            "The 2020 Scientific Data descriptor defines no predictive metric. Joung et al. 2021 "
            "(https://doi.org/10.1021/jacsau.1c00035) report RMSE and Pearson R-squared and optimize joint "
            "standardized MSE over seven targets; a unique absorption-only model-selection metric is not "
            "established. Use regression fallback RMSE on the retained absorption wavelengths in nm."
        )
    )
    temporal = Temporal(
        on="first_year",
        splits=TemporalSplits(window=1, unit="unique", cutoffs=(2020, 2019, 2018, 2017, 2016, 2015)),
        horizon=1,
        horizon_unit="years",
        time_unit="years",
        time_of="label",
    )
    split_leaf = "L-CAT.entry-date"
    splits_comment = """
        Windows on each dye's first publication year (`first_year`, no input), leaf L-CAT.entry-date of the split
        tree, with no gap (a published label is final when its paper appears). The one-year length is the
        finest step the year gives, and the curator signed it off (Andrej, 2026-11-24); the use case sets no
        other. SPLIT-33's target is 9 splits for 17,509 rows; 6 are reached, because the 2014 window would train
        on 44.4% of the rows, under the half-the-rows floor. The 131 undated dyes (194 rows) train in every
        window; without them 2015 still trains on 50.5%. All rows of a dye stay in one window.
    """

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        path = raw_dir / RAW_FILE
        if hashlib.sha256(path.read_bytes()).hexdigest() != RAW_SHA256:
            raise ValueError("Source CSV differs from the pinned Figshare v3 release")
        years_path = raw_dir / YEARS_FILE
        if hashlib.sha256(years_path.read_bytes()).hexdigest() != YEARS_SHA256:
            raise ValueError("The Crossref year table differs from the pinned one (download_description)")
        raw = pd.read_csv(path)
        years = pd.read_csv(years_path, dtype={"Reference": str}).rename(columns={"year": "paper_year"})
        # The publication year of each row's paper, joined on the source's own Reference string.
        raw = raw.merge(years, on="Reference", how="left", validate="m:1", indicator=True)
        if raw.loc[raw["Reference"].notna(), "_merge"].ne("both").any():
            raise ValueError("A Reference of the source is missing from the Crossref year table")
        return raw.drop(columns="_merge")

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        df = raw.loc[raw[self.target].notna()].copy()
        # Gas is an observed physical state, not an invalid molecular structure to discard.
        gas = df["Solvent"].eq("gas")
        dye = canonical_values(df["Chromophore"])
        solvent = canonical_values(df["Solvent"].mask(gas))
        state = pd.Series("solvent or host", index=df.index, dtype="string")
        state = state.mask(gas, "gas").mask(~gas & dye.eq(solvent).fillna(False), "neat solid")
        # Reichardt's betaine dye 30 in gas (1,055 nm) is the ET(30) scale's extrapolated gas-phase value, not a
        # measured peak: it leaves (Andrej, 2026-11-24). Its 334 solvent rows are measured peaks and stay.
        extrapolated = dye.eq(canonical_smiles(pd.Series([BETAINE_30]))[0]) & state.eq("gas")
        assert extrapolated.sum() == 1, "expected exactly one gas row of the betaine dye 30"
        df = pd.DataFrame(
            {
                "Chromophore_SMILES": dye,
                "Solvent_SMILES": solvent,
                "medium_state": state,
                self.target: df[self.target],
                "paper_year": df["paper_year"],
            },
            index=df.index,
        ).loc[~extrapolated]
        # The first year of a dye comes from every labeled row of it, also the repeats deduplicated below.
        first_year = self._first_years(df)
        df = df.drop_duplicates(subset=["Chromophore_SMILES", "Solvent_SMILES", "medium_state", self.target])
        df = df.drop(columns="paper_year").assign(first_year=first_year.loc[df.index])
        # The split column orders the rows (`temporal`, time_of="label"); it is no model input.
        return df.sort_values("first_year", kind="stable").reset_index(drop=True)

    @staticmethod
    def _first_years(df: pd.DataFrame) -> pd.Series:
        """The earliest Crossref year over the papers of each row's dye; undated dyes take the earliest year.

        A dye is its structure without stereochemistry, with aliases joined: structures with one nonempty InChIKey
        or one canonical tautomer are one dye, so a later alias of a dye never tests against its own earlier entry.
        """
        key = canonical_values(df["Chromophore_SMILES"], stereo=False)
        unique = list(pd.unique(key.dropna()))
        parent = {structure: structure for structure in unique}

        def find(structure: str) -> str:
            while parent[structure] != structure:
                parent[structure] = parent[parent[structure]]
                structure = parent[structure]
            return structure

        enumerator = rdMolStandardize.TautomerEnumerator()
        for identify in (
            Chem.MolToInchiKey,
            lambda mol: Chem.MolToSmiles(enumerator.Canonicalize(mol)),
        ):
            seen: dict[str, str] = {}
            for structure in unique:
                identity = identify(Chem.MolFromSmiles(structure)) or structure
                if identity in seen:
                    left, right = find(structure), find(seen[identity])
                    parent[max(left, right)] = min(left, right)
                else:
                    seen[identity] = structure
        dye = key.map({structure: find(structure) for structure in unique})
        first = df["paper_year"].groupby(dye).transform("min")
        return first.fillna(first.min()).astype("int64")

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        del df
        return FeatureTypes(categorical=["medium_state"])
