"""Curated dataset definition for `france_dvf_property_sales_1m` (data-foundry v2). Evidence: README.md."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from data_foundry.v2 import (
    AbstractCuratedDataset,
    Decision,
    FeatureTypes,
    Metric,
    RowBudget,
    TaskSummary,
    Temporal,
    TemporalSplits,
)

GEO_DIR = "geo-dvf-2025-12"  # Etalab's geolocated DVF, release folder 2025-12 (DGFiP's April 2026 delivery)
YEARS = (2023, 2024, 2025)
DGFIP_2025 = "dgfip-2026-10/valeursfoncieres-2025.txt.zip"  # DGFiP's October 2026 release, read only for evidence
MUTATIONS_FILE = "dvf_mutations_2023_2025.parquet"  # prepared: one row per mutation (sale) of the three years
COMPLETENESS_FILE = "dvf_2025_completeness.csv"  # prepared: the 2025 months in this release against October 2026's
# The sales of November and December 2025 are incomplete in this release (DGFiP's delivery of April 2026).
FIRST_INCOMPLETE_DAY = "2025-11-01"
DWELLINGS = ("Maison", "Appartement")
# Mutations whose price is a sale price of an existing property: ordinary sales and auctions. Off-plan sales (VEFA)
# are left out: their dwelling enters the land register only when the building is finished, after the sale.
SALE_NATURES = ("Vente", "Adjudication")
VEFA = "Vente en l'état futur d'achèvement"
# A declared price of 1,000 EUR or less is a symbolic or non-market amount, not the price of a dwelling (decision table).
PRICE_FLOOR = 1_000
# Fixed boxes (latitude, longitude) of the parcel coordinates per territory; Saint-Martin and Saint-Barthélemy are
# filed under Guadeloupe (971). Metropolitan France includes Corsica.
METRO_BOX = ((41.3, 51.2), (-5.3, 9.7))
OVERSEAS_BOXES = {
    "971": ((15.8, 18.2), (-63.2, -60.9)),
    "972": ((14.3, 14.9), (-61.3, -60.7)),
    "973": ((2.0, 6.0), (-54.7, -51.5)),
    "974": ((-21.5, -20.8), (55.1, 56.0)),
}
MIN_M2_PER_ROOM = 4  # fewer square metres of floor area per main room than this is not a dwelling's room count
# Land use codes of the cadastre (notice, "Nature de culture"), grouped: built land, garden or amenity, building land.
LAND_GROUPS = {"sols": ("S",), "jardins": ("J", "AG"), "a_batir": ("AB",)}

LINE_STR = [
    "id_mutation",
    "date_mutation",
    "numero_disposition",
    "nature_mutation",
    "code_postal",
    "code_commune",
    "code_departement",
    "id_parcelle",
    "numero_volume",
    "type_local",
    "code_nature_culture",
    "code_nature_culture_speciale",
]
LINE_NUM = [
    "valeur_fonciere",
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "surface_terrain",
    "nombre_lots",
    "longitude",
    "latitude",
    *[f"lot{i}_surface_carrez" for i in range(1, 6)],
]


def _aggregate_mutations(lines):
    """One row per mutation from DVF's lines (one line per local x land-use piece; the price repeated on each)."""
    import polars as pl

    # Land: one line per distinct piece (parcel, land use, special use, area); the locals repeat it.
    land = lines.filter(pl.col("code_nature_culture").is_not_null()).unique(
        subset=["id_mutation", "id_parcelle", "code_nature_culture", "code_nature_culture_speciale", "surface_terrain"],
        maintain_order=True,
    )
    pieces = land.group_by(["id_mutation", "id_parcelle"], maintain_order=True).agg(n_pieces=pl.len())
    use = pl.col("code_nature_culture")
    grouped = [c for codes in LAND_GROUPS.values() for c in codes]
    land_per_sale = land.group_by("id_mutation", maintain_order=True).agg(
        surface_terrain=pl.col("surface_terrain").sum(),
        **{
            f"surface_terrain_{name}": pl.col("surface_terrain").filter(use.is_in(list(codes))).sum()
            for name, codes in LAND_GROUPS.items()
        },
        surface_terrain_autres=pl.col("surface_terrain").filter(~use.is_in(grouped)).sum(),
    )
    # Locals: n locals on a parcel with p land-use pieces give n x p lines (notice, section 4), so each line of a
    # parcel counts 1/p of a local.
    locals_ = (
        lines.filter(pl.col("type_local").is_not_null())
        .join(pieces, on=["id_mutation", "id_parcelle"], how="left")
        .with_columns(share=1.0 / pl.col("n_pieces").fill_null(1))
    )
    is_dwelling = pl.col("type_local").is_in(list(DWELLINGS))
    counts = locals_.group_by("id_mutation", maintain_order=True).agg(
        n_dwellings=(pl.col("share") * is_dwelling).sum(),
        n_dependances=(pl.col("share") * (pl.col("type_local") == "Dépendance")).sum().round(0),
        n_commercial=(pl.col("share") * pl.col("type_local").str.starts_with("Local")).sum(),
    )
    carrez = [pl.col(f"lot{i}_surface_carrez") for i in range(1, 6)]
    dwelling = (
        locals_.filter(is_dwelling)
        .with_columns(
            # The Carrez (private floor) area of the lots on the dwelling's line; missing when no lot states one.
            surface_carrez=pl.when(pl.any_horizontal([c.is_not_null() for c in carrez])).then(pl.sum_horizontal(carrez))
        )
        .group_by("id_mutation", maintain_order=True)
        .agg(
            pl.col(
                "type_local",
                "surface_reelle_bati",
                "nombre_pieces_principales",
                "nombre_lots",
                "surface_carrez",
                "id_parcelle",
                "code_postal",
                "code_commune",
                "code_departement",
                "longitude",
                "latitude",
            ).first()
        )
    )
    sale = lines.group_by("id_mutation", maintain_order=True).agg(
        pl.col("date_mutation", "nature_mutation", "valeur_fonciere").first(),
        n_prices=pl.col("valeur_fonciere").n_unique(),
        n_parcelles=pl.col("id_parcelle").n_unique(),
        n_lines=pl.len(),
    )
    out = (
        sale.join(counts, on="id_mutation", how="left")
        .join(dwelling, on="id_mutation", how="left")
        .join(land_per_sale, on="id_mutation", how="left")
    )
    return out.sort("id_mutation")


def _completeness(raw_dir: Path):
    """Dwelling lines of 2025 per month: this release (April 2026 data) against DGFiP's October 2026 release."""
    import polars as pl

    key = ["date_mutation", "cents", "id_parcelle", "type_local", "lot1_numero"]
    geo = (
        pl.read_csv(
            raw_dir / GEO_DIR / "full_2025.csv.gz",
            columns=["date_mutation", "valeur_fonciere", "id_parcelle", "type_local", "lot1_numero"],
            infer_schema_length=0,
        )
        .filter(pl.col("type_local").is_in(list(DWELLINGS)))
        .with_columns(cents=(pl.col("valeur_fonciere").cast(pl.Float64) * 100).round().cast(pl.Int64))
        .select(key)
        .unique(maintain_order=True)
        .with_columns(in_release=pl.lit(True))
    )
    with zipfile.ZipFile(raw_dir / DGFIP_2025) as archive:
        (member,) = archive.namelist()
        text = archive.read(member)
    later = pl.read_csv(io.BytesIO(text), separator="|", infer_schema_length=0).filter(
        pl.col("Type local").is_in(list(DWELLINGS))
    )
    price = pl.col("Valeur fonciere").str.replace(",", ".").cast(pl.Float64)
    later = later.select(
        date_mutation=pl.col("Date mutation").str.slice(6, 4)
        + "-"
        + pl.col("Date mutation").str.slice(3, 2)
        + "-"
        + pl.col("Date mutation").str.slice(0, 2),
        cents=(price * 100).round().cast(pl.Int64),
        id_parcelle=pl.col("Code departement")
        + pl.col("Code commune").str.zfill(3)
        + pl.col("Prefixe de section").fill_null("000").str.zfill(3)
        + pl.col("Section").str.zfill(2)
        + pl.col("No plan").str.zfill(4),
        type_local=pl.col("Type local"),
        lot1_numero=pl.col("1er lot"),
        price_per_m2=price / pl.col("Surface reelle bati").cast(pl.Float64),
    )
    later = later.join(geo, on=key, how="left", nulls_equal=True).with_columns(pl.col("in_release").fill_null(False))
    present = pl.col("in_release")
    return (
        later.group_by(month=pl.col("date_mutation").str.slice(0, 7), maintain_order=True)
        .agg(
            lines_october_2026=pl.len(),
            share_in_this_release=present.mean().round(3),
            median_price_per_m2_present=pl.col("price_per_m2").filter(present).median().round(0),
            median_price_per_m2_missing=pl.col("price_per_m2").filter(~present).median().round(0),
        )
        .sort("month")
    )


def _sales(raw: pd.DataFrame) -> pd.DataFrame:
    """The task's sales before the price floor: one dwelling and no commercial premises, the kinds kept, a price,
    the months this release holds nearly in full.
    """
    # The local counts are sums of 1/p shares (`_aggregate_mutations`).
    df = raw[np.isclose(raw["n_dwellings"].fillna(0.0), 1.0) & np.isclose(raw["n_commercial"].fillna(0.0), 0.0)]
    df = df[df["nature_mutation"].isin(SALE_NATURES)]
    df = df[df["valeur_fonciere"].notna()]  # CLEAN-15
    return df[df["date_mutation"] < FIRST_INCOMPLETE_DAY]


def _outside_territory(df: pd.DataFrame) -> pd.Series:
    """Rows whose coordinates lie outside the fixed box of their territory (metropolitan France or the overseas
    department), a geocoding error.
    """
    dept = df["code_departement"]

    def bound(axis: int, end: int) -> pd.Series:
        return dept.map({code: box[axis][end] for code, box in OVERSEAS_BOXES.items()}).fillna(METRO_BOX[axis][end])

    lat, lon = df["latitude"], df["longitude"]
    inside = lat.between(bound(0, 0), bound(0, 1)) & lon.between(bound(1, 0), bound(1, 1))
    return lat.notna() & lon.notna() & ~inside


def _local_level(sales: pd.DataFrame) -> pd.Series:
    """Each sale's price per m2 as a share of its local level: the median price per m2 of the sales above 30,000 EUR
    of the same commune and property type (evidence only, never a feature).
    """
    per_m2 = sales["valeur_fonciere"] / sales["surface_reelle_bati"].where(sales["surface_reelle_bati"] > 0)
    keys = [sales["code_commune"], sales["type_local"]]
    level = per_m2.where(sales["valeur_fonciere"] > 30_000).groupby(keys).transform("median")
    return per_m2 / level


class FranceDvfPropertySales1m(AbstractCuratedDataset):
    task_summary = TaskSummary(
        question=(
            "What market price does the land registry's description of a house or an apartment just sold in France "
            "point to, for a tax office checking the price its deed declares?"
        ),
        use_case=(
            "A tax-office (DGFiP) valuer checks the price declared in a deed as the deed is published, against a "
            "market price estimated from the land registry's description and the place, to flag under-declared "
            "values, with a model refit every quarter on the sales published until a month earlier."
        ),
        row=(
            "One sale of a single existing house or apartment in France (without Alsace-Moselle and Mayotte), January "
            "2023 to October 2025, with its garages, cellars and land: DVF's lines of one sale collapsed into one row."
        ),
        predicted="The declared sale price, on a log scale.",
        known=(
            "The sale date and kind (ordinary sale or auction), the property type, its floor area, rooms, "
            "condominium lots and their private area, the outbuildings and land by use, and the location: "
            "department, commune, postcode, cadastral section and the parcel's coordinates."
        ),
        split=(
            "Each test window is three months of sales, February to October 2025, newest first; training is a "
            "random million of the sales up to one month before the window, the time a deed takes to be published."
        ),
        changes=(
            "We collapse DVF's lines into one row per sale and keep only sales of exactly one existing dwelling; we "
            "drop off-plan sales (in the register only once built), exchanges, expropriations and declared prices of "
            "1,000 EUR or less, and cut November and December 2025, which this release holds only in part."
        ),
        fit="approximate",
        fit_reason=(
            "The inputs are the land registry's description at the sale and the place, from which a valuer starts. "
            "The registry holds no year built, condition, floor or energy rating, and the declared price includes "
            "partial-rights and family transfers that DVF does not mark: 1.1% of the sales are priced below a fifth "
            "of their commune's level per m2."
        ),
    )

    # Dataset
    unique_name = "france_dvf_property_sales_1m"
    version_of = "france_dvf_property_sales"
    version_comment = """
        We sample per test window (v2 split protocol): each three-month window keeps all of its rows (194,513 to 217,561, under the 500k budget), and its train side is a random 1M of the sales up to one month before it, drawn in one random order for all windows; the frame keeps only the rows a split uses. Random sampling keeps sales of every month since January 2023 in each train side, as a model refit on the whole history would see them.
    """
    year = "2026"
    domain = "business & marketing"
    source = "GOV Website"
    source_url = "https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/"
    license = (
        "Licence Ouverte / Open Licence v2.0 (Etalab), with DGFiP's terms of use (CGU): a reuse only for the "
        "legislator's purpose, 'concourir à la transparence des marchés fonciers et immobiliers' (CGU p. 2); no "
        "re-identification of the persons concerned; no indexing by search engines"
    )
    data_tags = ("Spatial",)
    download_description = """
        DVF (Demandes de valeurs foncières) is published by the Direction générale des Finances publiques (DGFiP) on data.gouv.fr since April 2019, twice a year (April and October), as one pipe-separated file per year over a rolling five-year window. We read Etalab's geolocated copy of the same lines (Demandes de valeurs foncières géolocalisées, https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees): UTF-8 CSV with a mutation id and the parcel's coordinates, release folder 2025-12, built from DGFiP's April 2026 delivery (Etalab's history: "20/04/2026 : nouvelles données DVF d'avril 2026"). We take 2023 to 2025 only; 2021 and 2022 are not downloaded (the train sides are sampled to 1M rows from 2023 on already). DGFiP's October 2026 file of 2025 is read only for the completeness check of the newest months (decision table); its 2026-S1 file was downloaded too and is not read.

        Etalab published its next release, built from DGFiP's October 2026 delivery (November and December 2025 complete, 2026-S1 added), on 2026-10-20 as data.gouv.fr resources, and labels the 2025-12 folder for deletion on 30 November 2026 ("suppression au 31/11/2026"); DGFiP replaces its files at every delivery. The wget lines below work until then. The reference copy of these files is the archive in the local warehouse (local-data-warehouse/france_dvf_property_sales/), checked by the sha256 values below; a re-source to the October 2026 release is a later version.

        mkdir -p local-data-warehouse/france_dvf_property_sales/geo-dvf-2025-12 local-data-warehouse/france_dvf_property_sales/dgfip-2026-10
        for y in 2023 2024 2025; do wget -O local-data-warehouse/france_dvf_property_sales/geo-dvf-2025-12/full_$y.csv.gz https://files.data.gouv.fr/geo-dvf/2025-12/csv/$y/full.csv.gz; done
        wget -O local-data-warehouse/france_dvf_property_sales/dgfip-2026-10/valeursfoncieres-2025.txt.zip https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20261012-171642/valeursfoncieres-2025.txt.zip

        sha256 of the archived files (downloads of 2026-11-09): geo-dvf-2025-12/full_2023.csv.gz 9ecfee4de5cc1e34e9dbe438cb02b2957ecee2e4cd8cad9d28291e947611b5c6, geo-dvf-2025-12/full_2024.csv.gz f702185bb169c53627cf3619760e0a93d5e39912d3fded30d587e8033e083cc7, geo-dvf-2025-12/full_2025.csv.gz bf80533b27c44471287026e9ce679fa803ecdd9efd8267cf5710d40fd7a22980, dgfip-2026-10/valeursfoncieres-2025.txt.zip 86ee8bfb32372daf8c668b414628dbbf6f3c750ca330f2ca27ef2896d6fa49f0, dgfip-2026-10/valeursfoncieres-2026-s1.txt.zip (not read) 79387dcae02dd0e1f98525482fe8f36cc3e137f679da38ac4b83f631af5845ea. The first build writes dvf_mutations_2023_2025.parquet (one row per mutation) and dvf_2025_completeness.csv into the same folder.
    """
    bibtex = r"""
        @misc{dgfip2019dvf,
          author = {{Direction g{\'e}n{\'e}rale des Finances publiques}},
          title = {Demandes de valeurs fonci{\`e}res},
          year = {2019},
          howpublished = {\url{https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/}},
          note = {Open since April 2019 under d{\'e}cret n\textsuperscript{o} 2018-1350; updated every April and October}
        }
        @misc{etalab2025geodvf,
          author = {{Etalab}},
          title = {Demandes de valeurs fonci{\`e}res g{\'e}olocalis{\'e}es},
          year = {2025},
          howpublished = {\url{https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees}},
          note = {Release folder 2025-12, \url{https://files.data.gouv.fr/geo-dvf/2025-12/}}
        }
    """
    curation_comments = """
        We start with full_2023.csv.gz, full_2024.csv.gz and full_2025.csv.gz of Etalab's geolocated DVF (release folder 2025-12, DGFiP's April 2026 delivery): 11.0M lines of 3.90M mutations (sales, exchanges, expropriations, auctions) recorded by France's land registry offices.

        - Prediction point: as a deed is published, a tax-office (DGFiP) valuer checks the price it declares against the market price of the home, estimated from what the land registry describes (type, floor area, rooms, lots, outbuildings, land) and where it is, with a model refit every quarter on the sales published up to a month earlier. Only the property, the place, the kind of sale and its date are inputs. A valuer who prices before the sale (a lender, a notary) works at the compromis, about 3 months before the deed's date, which a gap of one month does not cover (USE-3, SPLIT-10).
        - One row per sale (LEAK-16): DVF writes one line per local and per land-use piece of a mutation, n locals on a parcel with p land-use pieces as n x p lines, with the price repeated on each (notice, section 4). `_prepare_raw_files` collapses the lines into one row per `id_mutation` (`_aggregate_mutations`): each local line of a parcel counts 1/p of a local, and each distinct land piece (parcel, use, special use, area) counts once. Every mutation carries one price (no mutation has two). The rule is not exact where DVF did not write every n x p line: 143 kept sales hold more than one distinct dwelling line (68 with two floor areas, so two dwellings), and 1,214 sales with one dwelling line leave on a non-integer count; both under 0.1% of the sales.
        - We keep the sales of exactly one dwelling (one `Maison` or `Appartement`) with no commercial or industrial premises, with any number of outbuildings (`Dépendance`) and land pieces (2,360,591 of 3,904,877 mutations). A sale of several dwellings, or of a dwelling with a shop, has one price for all of them, which no input could split; sales of outbuildings or land alone are not the task (decision table).
        - Kind of sale: we keep `Vente` and `Adjudication` (auction, 5,896 sales), each a price paid for an existing property and known as a kind before the sale, as the feature `nature_mutation`. We drop `Echange` (exchange, 3,017), `Expropriation` (47) and `Vente terrain à bâtir` (403, building land with a dwelling on it), whose price is a compensation or a land price, and `Vente en l'état futur d'achèvement` (off-plan, 33,807 sales that would be rows, LEAK-10): an off-plan dwelling enters the land register only when the building is finished, after the sale, so which off-plan sales hold one dwelling depends on a later completion. 2,544 of the 7,972 off-plan sales of 2025 with a dwelling in DGFiP's October 2026 delivery had none in this release (ordinary sales: 44 of 874,021), and the off-plan share falls from 1.4%-2.8% of the single-dwelling sales in 2023-2024 to 0.5% in 2025-H2 (decision table); perth_house_prices dropped its off-the-plan sales the same way.
        - We drop the 1,247 single-dwelling sales without a price (CLEAN-15).
        - We cut the sales from 1 November 2025 on. Most deeds enter DVF within days of their signature (73% of those signed on 31 December 2025 are in this release) and about a tenth months later, the cheaper ones: against DGFiP's October 2026 delivery the release holds 89.0% of December's dwelling lines and 95.2% of November's (97.6% to 98.4% in January to October: the ceiling of a match on date, price, parcel, type and first lot), and December's present lines have a median price of 3,153 EUR per m2 against 2,579 to 2,846 in January to October, so the newest months are selected by price (decision table; SPLIT-10, LEAK-24).
        - The target is the natural log of `valeur_fonciere`, the declared price (agency fees paid by the seller and VAT included; notary fees, buyer-paid agency fees and furniture excluded: notice, column 11), renamed `log_valeur_fonciere`.
        - We drop the 3,213 sales whose declared price is 1,000 EUR or less, on the raw `valeur_fonciere` before the log (USE-5): 1,073 at 1 EUR, 1,267 below 100 EUR, 2,588 below 1,000 and 625 at exactly 1,000. The source calls the field a "montant ou évaluation déclaré(e)" (notice, column 11), and these amounts are not prices of a dwelling: against the median price per m2 of the commune's sales of the same type above 30,000 EUR, the band from 100 to 1,000 EUR sits at a median 0.3% of that level, as the band below 100 EUR sits near 0, and 0.1% of it reaches a fifth (decision table). They were about 0.1% of the test rows and about a quarter of an untuned LightGBM's squared log error (two windows). The floor takes only what is certainly not a price: from 1,000 to 3,000 EUR a tenth to a quarter of the sales reach 5% of the local level, real cheap sales begin there, and they stay. The 173 sales at 10M EUR or more stay too (a single dwelling with up to 312 parcels: estates, farms), at most 0.2% of the error.
        - Anomaly: the declared price still includes partial-rights and family transfers (a bare ownership, a share bought out by a co-heir) that DVF does not mark (the rights sold are not given: notice, p. 3): 24,036 sales (1.1%) are priced per m2 below a fifth of their commune's median for the type. No input tells them from real cheap sales, and a floor relative to the local level would filter on the target by a rule of our own, so they stay, named in the fit.
        - The dwelling's attributes are the land registry's at the deed's publication: `surface_reelle_bati` (floor area, outbuildings excluded), `nombre_pieces_principales` (main rooms), `nombre_lots` (condominium lots of the disposition), `surface_carrez` (the sum of the Carrez private areas the dwelling's line lists for its first five lots; missing when none is stated, as for most houses). For existing dwellings they are not refreshed at later releases: for the 906,747 dwelling lines of 2025 matched between this release and DGFiP's October 2026 one, the floor area and the rooms agree on every line (LEAK-10); an off-plan dwelling enters at completion (dropped above).
        - We set to missing, by fixed rules within the row (CLEAN-11): 0 main rooms (2,210 sales; every dwelling has one) and a room count that leaves under 4 m2 of floor area per main room (294 sales, up to 198 rooms: a 92 m2 house with 95); a Carrez area that contradicts the dwelling's floor area, below 8 m2 beside a floor area of 20 m2 or more, or above 3 times the floor area and above 200 m2 (390 sales, every value above 1,000 m2 among them). The other 299 Carrez areas below 8 m2 stay, beside a floor area as small: they lie under the 8 m2 the Carrez definition counts (notice, lexicon) but are the room's real size, as the 983 floor areas below 9 m2 that stay (mostly apartments: attic rooms sold as dwellings).
        - Built from the lines: `n_dependances` (outbuildings: garages, cellars, parking spaces), `n_parcelles` (parcels in the sale), and the land area in m2 by the cadastre's use codes: `surface_terrain` (all), `surface_terrain_sols` (S, built land), `surface_terrain_jardins` (J and AG, gardens and amenity land), `surface_terrain_a_batir` (AB, building land) and `surface_terrain_autres` (fields, woods, water and the rest); all missing for a sale without land (most apartments), 0 for a group the sale has none of (CLEAN-19: a sale's lines to one row).
        - Location: `code_departement`, `code_commune` (INSEE code), `code_postal`, `code_section` and `longitude`, `latitude` (Etalab's centroid of the dwelling's parcel). The coordinates are missing for 0.76% of the sales, 1.19% in 2023 and 0.30% in 2025, where Etalab's later cadastre no longer holds the parcel (split or renumbered after the sale), not by price. We set them missing outside a fixed box per territory (metropolitan France with Corsica; Guadeloupe with Saint-Martin and Saint-Barthélemy; Martinique; French Guiana; La Réunion): 62 sales in four communes of Hauts-de-Seine geocoded at latitudes 40.88 to 83.52 (CLEAN-11; a fixed rule, no statistic over rows, CLEAN-7).
        - `code_section` is the commune, prefix and cadastral section of the dwelling's parcel: one or more neighbourhoods or lieux-dits (notice, lexicon), 217,672 in the data, about 10 sales each. zillow_prize dropped its census block group of the same grain as a near-identifier whose place the coordinates hold; the section stays because it is the domain's own price unit: Etalab, the publisher of the copy we read, publishes DVF's sales counts and mean and median prices per m2 at five scales, the finest the cadastral section (Statistiques DVF, https://www.data.gouv.fr/datasets/statistiques-dvf; nation, department, EPCI, commune, section), and a census block group has no such role in Zillow's data (CLEAN-14, CLEAN-3).
        - We drop the identifiers and the address: `id_mutation`, `id_parcelle` (the parcel number), the street number and name, the lot numbers and the dispositions (CLEAN-3). A row stays as identifying as the published record, no more: the 6-decimal coordinates map one to one onto the parcels, and (date, price, commune, floor area, type) alone is unique for 99.91% of the rows, so a row links back to its published record, address included, with or without the coordinates. DGFiP's terms of use allow that degree ("ne doivent pas aboutir à un degré d'identification ... plus important que celui caractérisant le jeu de données mis à disposition") and limit a reuse to the legislator's purpose, "concourir à la transparence des marchés fonciers et immobiliers" (CGU p. 2), which a benchmark of price models serves as public research (CGU p. 1). A hosted copy must not be indexable by search engines (CGU p. 3). The coordinates stay at Etalab's published precision.
        - Note: 1,120 sales share the date, price, parcel, type, floor area and rooms with another sale under another id (twin units or one deed recorded twice); each group has one date, so it is never split between train and test (LEAK-16).
        - Note: 62,195 dwelling keys (same parcel, type, floor area, rooms and Carrez area) recur in 2023-2025 (143,425 sales), an upper bound on resales: 29,785 of the 37,780 apartment keys hold more than one first-lot number, so they are twin units of one building, and by (parcel, first lot) 20,841 apartments were resold (41,969 sales). An earlier sale is in the past of the later one under the temporal split, as a valuer would know it (SPLIT-13, USE-10, as house_sales).
        - Categorical: `nature_mutation`, `type_local`, `code_departement`, `code_commune`, `code_postal`, `code_section`; `date_mutation` (the deed's signature date) is a datetime, the time column and a feature.
        - The data covers metropolitan France without Bas-Rhin, Haut-Rhin and Moselle (their land books are kept apart) and the overseas departments without Mayotte (notice, section 2): Guadeloupe, Martinique, French Guiana and La Réunion hold 27,415 of the single-dwelling mutations of 2023-2025 of every kind, and 24,861 of the sales kept.
    """

    # Task
    target = "log_valeur_fonciere"
    problem_type = "regression"
    metric = Metric.from_context(
        "rmsle",
        reason=(
            "DGFiP publishes DVF for the transparency of property markets and defines no task or metric (the "
            "notice, the terms of use, the data.gouv.fr page); Etalab's geolocated copy defines none either. For a "
            "sale price the error that matters is relative to the price (declared prices run from just over 1,000 "
            "EUR to over 10M EUR), so RMSLE on the price, as for the other house-price datasets of the collection."
        ),
        target_transform="log",
    )

    # Splits
    temporal = Temporal(on="date_mutation", splits=TemporalSplits(window=3, unit="months", n_windows=3, gap=1))
    row_budget = RowBudget(train=1_000_000, test=500_000)
    splits_comment = """
        A check of declared prices refit every quarter on the sales published so far: 3 test windows of three calendar months (August-October, May-July and February-April 2025), newest first, each trained on the sales up to one month before the window (a gap of one month). The gap is the delay before a deed is published and enters DVF: most deeds are recorded within days and about a tenth months later, the cheaper ones; against DGFiP's October 2026 delivery this release holds 95.2% of November 2025's dwelling sales and 89.0% of December's, the present ones dearer (decision table), so a refit at a window's start knows the month before only in part. The tax-office valuer's prediction point is the deed's publication, so the gap counts from the deed's date; a valuer pricing before the sale, at the compromis about 3 months earlier, would need a gap of 3. The windows end on 31 October 2025, the last month the release holds nearly in full, and never test November to January (the cut and the gap month). Training history from January 2023 (2021-2022 not used). Each test window keeps all its sales (194,513 to 217,561); each train side is a random 1M of the earlier sales (1,508,398 to 1,886,698 before sampling, 69% to 86% of the 2,185,254 rows), drawn in one random order for all windows. The sample is uniform per quarter, but the shipped file holds only the rows some split uses: 2023-2024 at about 66% of the sales (the union of the train samples) and February to October 2025 in full (the test windows), so its rows per month jump in 2025. Protocol: a model predicts each test row from the train rows and that row's own features; counting same-day sales at a place over the test rows is worth 0.003 to 0.005 RMSLE, and a model that reads the test block that way is called out (LEAK-9). Three windows are the 1 x 3 splits an IID task of this size gets.
    """

    prepared_raw_files = (MUTATIONS_FILE, COMPLETENESS_FILE)

    def _prepare_raw_files(self, raw_dir: Path) -> None:
        import polars as pl

        schema = dict.fromkeys(LINE_STR, pl.Utf8) | dict.fromkeys(LINE_NUM, pl.Float64)
        lines = pl.concat(
            [
                pl.read_csv(
                    raw_dir / GEO_DIR / f"full_{year}.csv.gz", columns=LINE_STR + LINE_NUM, schema_overrides=schema
                )
                for year in YEARS
            ]
        )
        _aggregate_mutations(lines).write_parquet(raw_dir / MUTATIONS_FILE)
        del lines
        _completeness(raw_dir).write_csv(raw_dir / COMPLETENESS_FILE)

    def _load_raw(self, raw_dir: Path) -> pd.DataFrame:
        return pd.read_parquet(raw_dir / MUTATIONS_FILE)

    def _clean(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 1-4. One existing dwelling, ordinary sales and auctions, a price, the months held nearly in full.
        df = _sales(raw)
        # 5. A declared price of 1,000 EUR or less is not a price of a dwelling (USE-5); on the raw price.
        df = df[df["valeur_fonciere"] > PRICE_FLOOR]
        # 6. Impossible values to missing, by fixed rules within the row (CLEAN-11): 0 main rooms or under 4 m2 per
        # room; a Carrez area that contradicts the floor area; coordinates outside the territory's box.
        rooms = df["nombre_pieces_principales"].mask(df["nombre_pieces_principales"] == 0)
        area, carrez = df["surface_reelle_bati"], df["surface_carrez"]
        df["nombre_pieces_principales"] = rooms.mask(area / rooms < MIN_M2_PER_ROOM)
        df["surface_carrez"] = carrez.mask(((carrez < 8) & (area >= 20)) | ((carrez > 3 * area) & (carrez > 200)))
        outside = _outside_territory(df)
        df.loc[outside, ["longitude", "latitude"]] = np.nan
        # 7. The cadastral section: commune (5), prefix (3) and section (2) of the dwelling's parcel id.
        df["code_section"] = df["id_parcelle"].str.slice(0, 10)
        # 8. Target: the log of the declared price, renamed in place.
        df = df.rename(columns={"valeur_fonciere": "log_valeur_fonciere"})
        df["log_valeur_fonciere"] = np.log(df["log_valeur_fonciere"])
        # 9. Identifiers and the bookkeeping columns of the collapse.
        return df.drop(columns=["id_mutation", "id_parcelle", "n_dwellings", "n_commercial", "n_prices", "n_lines"])

    def _feature_types(self, df: pd.DataFrame) -> FeatureTypes:
        return FeatureTypes(
            categorical=[
                "nature_mutation",
                "type_local",
                "code_departement",
                "code_commune",
                "code_postal",
                "code_section",
            ],
            datetime={"date_mutation": "%Y-%m-%d"},
        )

    def _decisions(self, raw: pd.DataFrame, df: pd.DataFrame) -> list[Decision]:
        dwellings = raw["n_dwellings"].fillna(0.0)
        single = np.isclose(dwellings, 1.0)
        commercial = raw["n_commercial"].fillna(0.0) > 1e-9
        kind = pd.Series(
            np.select(
                [single & ~commercial, single & commercial, dwellings > 1.0 + 1e-9],
                ["one dwelling (kept)", "one dwelling with commercial premises", "several dwellings"],
                default="no dwelling (outbuildings, premises or land only)",
            ),
            index=raw.index,
        )
        mutations = pd.crosstab(kind, raw["nature_mutation"], margins=True, margins_name="all")
        mutations.index.name = "mutation holds"

        month = raw["date_mutation"].str.slice(5, 7).astype(int)
        quarter = raw["date_mutation"].str.slice(0, 4) + "-Q" + ((month - 1) // 3 + 1).astype(str)
        offplan = raw["nature_mutation"] == VEFA
        sold_one = single & ~commercial & raw["valeur_fonciere"].notna()
        sold_one &= raw["nature_mutation"].isin((*SALE_NATURES, VEFA))
        vefa = pd.DataFrame(
            {
                "off-plan mutations": offplan.groupby(quarter).sum(),
                "share holding a dwelling": (dwellings > 1e-9)[offplan].groupby(quarter[offplan]).mean(),
                "off-plan share of the single-dwelling sales": (offplan & sold_one).groupby(quarter).sum()
                / sold_one.groupby(quarter).sum(),
            }
        ).round(3)
        vefa.index.name = "quarter of sale"

        completeness = pd.read_csv(self.raw_dir / COMPLETENESS_FILE).set_index("month")

        sales = _sales(raw)
        price = sales["valeur_fonciere"]
        labels = [
            "under 100",
            "100 to 1,000",
            "over 1,000 to 2,000",
            "over 2,000 to 3,000",
            "over 3,000 to 5,000",
            "over 5,000 to 10,000",
            "over 10,000, under 10M",
            "10M and over",
        ]
        limits = [price < 100, price <= 1_000, price <= 2_000, price <= 3_000, price <= 5_000, price <= 10_000]
        band = np.select([*limits, price < 1e7], labels[:-1], default=labels[-1])
        per_m2 = price / sales["surface_reelle_bati"].where(sales["surface_reelle_bati"] > 0)
        frame = pd.DataFrame({"band": pd.Categorical(band, categories=labels, ordered=True), "per_m2": per_m2})
        frame["share"] = _local_level(sales).to_numpy()
        grouped = frame.groupby("band", observed=True)
        prices = pd.DataFrame(
            {
                "sales": grouped.size(),
                "kept": ["no", "no", *["yes"] * (len(labels) - 2)],
                "median EUR per m2": grouped["per_m2"].median().round(2),
                "median share of the local level": grouped["share"].median().round(3),
                "share at 5% of the local level or more": grouped["share"].agg(lambda s: s.dropna().ge(0.05).mean()),
                "share at a fifth or more": grouped["share"].agg(lambda s: s.dropna().ge(0.2).mean()),
            }
        ).round(3)
        prices.index.name = "declared price (EUR)"
        return [
            Decision(
                title="One row per sale of a single dwelling",
                why=(
                    "DVF repeats a sale's price on every line of its locals and land pieces; a sale of several "
                    "dwellings, or with commercial premises, has one price no input can split. Mutations of "
                    "2023-2025 by what they hold and their kind, before the date cut."
                ),
                evidence=mutations,
            ),
            Decision(
                title="Off-plan sales (VEFA) dropped",
                why=(
                    "An off-plan dwelling enters the land register only when the building is finished, after the "
                    "sale, so whether an off-plan sale holds one dwelling depends on a completion after the "
                    "prediction point (LEAK-10). Off-plan mutations by quarter of sale in this release: the share "
                    "already holding a dwelling falls with recency, and so does their share of the single-dwelling "
                    "sales."
                ),
                evidence=vefa,
            ),
            Decision(
                title="November and December 2025 cut",
                why=(
                    "Most deeds enter DVF within days of their signature and about a tenth months later, the "
                    "cheaper ones. Dwelling lines of 2025 per month in DGFiP's October 2026 release, the share this "
                    "release (DGFiP's April 2026 delivery) holds (about 98% is the matching's ceiling), and the "
                    "median price per m2 of the lines it holds and misses."
                ),
                evidence=completeness,
            ),
            Decision(
                title="Declared prices of 1,000 EUR or less dropped",
                why=(
                    "DVF's price is a 'montant ou évaluation déclaré(e)' (notice, column 11), and no input marks a "
                    "symbolic or non-market transfer. Sales before the floor by declared price, with the price per "
                    "m2 against the local level (the median price per m2 of the commune's sales of the same type "
                    "above 30,000 EUR). Up to 1,000 EUR the amounts sit at a few thousandths of it, as below 100 "
                    "EUR, and almost none reaches a fifth: they are not prices of a dwelling (USE-5). Above, real "
                    "cheap sales begin, and they stay, as do the sales of 10M EUR or more."
                ),
                evidence=prices,
            ),
        ]
